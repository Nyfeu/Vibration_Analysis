#!/usr/bin/env python3
"""Cria labels, milestones, issues e o quadro do GitHub Projects a partir de backlog.json.

Idempotente: roda quantas vezes for preciso. Nada é apagado nem sobrescrito —
o que já existe é reaproveitado, e só o que falta é criado. Assim dá para
acrescentar item novo no backlog.json e rodar de novo sem duplicar o que já está lá.

Uso:
    python scripts/seed_backlog.py --dry-run    # mostra o que faria, sem tocar no GitHub
    python scripts/seed_backlog.py              # cria de verdade

Requisitos:
    gh auth login -s project
      O escopo `project` é obrigatório para o quadro do Projects v2. Sem ele as
      issues são criadas mas o quadro não.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BACKLOG = Path(__file__).resolve().parent / "backlog.json"


class ErroGh(RuntimeError):
    pass


def gh(*args: str, entrada: str | None = None) -> str:
    """Chama o gh e devolve stdout. Levanta ErroGh com a mensagem real do gh."""
    proc = subprocess.run(
        ["gh", *args],
        input=entrada,
        capture_output=True,
        text=True,
        cwd=RAIZ,
    )
    if proc.returncode != 0:
        raise ErroGh((proc.stderr or proc.stdout).strip())
    return proc.stdout.strip()


def confere_ambiente() -> tuple[str, str]:
    """Devolve (owner, repo) e falha cedo se o gh não estiver utilizável."""
    try:
        gh("auth", "status")
    except ErroGh as e:
        sys.exit(
            f"gh não autenticado:\n{e}\n\n"
            "Rode primeiro:  gh auth login -s project\n"
            "(o escopo 'project' é necessário para criar o quadro do Projects)"
        )
    alvo = gh("repo", "view", "--json", "owner,name")
    dados = json.loads(alvo)
    return dados["owner"]["login"], dados["name"]


# --------------------------------------------------------------------------- #
# Labels
# --------------------------------------------------------------------------- #
def cria_labels(labels: list[dict], dry: bool) -> None:
    print("\n== labels ==")
    for lab in labels:
        if dry:
            print(f"  [dry] {lab['nome']}")
            continue
        # --force faz o create virar upsert: não quebra se a label já existir.
        gh(
            "label", "create", lab["nome"],
            "--color", lab["cor"],
            "--description", lab["descricao"],
            "--force",
        )
        print(f"  ok   {lab['nome']}")


# --------------------------------------------------------------------------- #
# Milestones (o gh não tem subcomando próprio; vai pela API REST)
# --------------------------------------------------------------------------- #
def cria_milestones(milestones: list[dict], owner: str, repo: str, dry: bool) -> dict[str, int]:
    print("\n== milestones ==")
    existentes: dict[str, int] = {}
    if not dry:
        atuais = json.loads(
            gh("api", f"repos/{owner}/{repo}/milestones",
               "--method", "GET", "-f", "state=all", "--paginate")
        )
        existentes = {m["title"]: m["number"] for m in atuais}

    numeros: dict[str, int] = {}
    for ms in milestones:
        titulo = ms["titulo"]
        if titulo in existentes:
            numeros[titulo] = existentes[titulo]
            print(f"  --   {titulo} (já existe)")
            continue
        if dry:
            print(f"  [dry] {titulo}")
            continue
        args = ["api", f"repos/{owner}/{repo}/milestones", "--method", "POST",
                "-f", f"title={titulo}", "-f", f"description={ms['descricao']}"]
        if ms.get("prazo"):
            args += ["-f", f"due_on={ms['prazo']}"]
        criado = json.loads(gh(*args))
        numeros[titulo] = criado["number"]
        print(f"  ok   {titulo}")
    return numeros


# --------------------------------------------------------------------------- #
# Issues
# --------------------------------------------------------------------------- #
def issues_existentes(dry: bool) -> set[str]:
    if dry:
        return set()
    bruto = gh("issue", "list", "--state", "all", "--limit", "500", "--json", "title")
    return {i["title"] for i in json.loads(bruto)}


def cria_issues(issues: list[dict], dry: bool) -> list[str]:
    print("\n== issues ==")
    ja_existem = issues_existentes(dry)
    urls: list[str] = []
    for iss in issues:
        titulo = iss["titulo"]
        if titulo in ja_existem:
            print(f"  --   {titulo[:62]} (já existe)")
            if not dry:
                url = gh("issue", "list", "--state", "all", "--limit", "500",
                         "--json", "title,url",
                         "--jq", f'.[] | select(.title == {json.dumps(titulo)}) | .url')
                if url:
                    urls.append(url.splitlines()[0])
            continue
        if dry:
            print(f"  [dry] {titulo}")
            continue
        args = ["issue", "create", "--title", titulo, "--body", iss["corpo"]]
        for lab in iss.get("labels", []):
            args += ["--label", lab]
        if iss.get("milestone"):
            args += ["--milestone", iss["milestone"]]
        urls.append(gh(*args).splitlines()[-1])
        print(f"  ok   {titulo[:62]}")
    return urls


# --------------------------------------------------------------------------- #
# Projects v2
# --------------------------------------------------------------------------- #
def cria_projeto(projeto: dict, owner: str, urls: list[str], dry: bool) -> None:
    print("\n== quadro (Projects v2) ==")
    titulo = projeto["titulo"]
    if dry:
        print(f"  [dry] projeto '{titulo}' + {len(urls)} itens")
        return

    try:
        lista = json.loads(
            gh("project", "list", "--owner", owner, "--format", "json", "--limit", "100")
        )["projects"]
    except ErroGh as e:
        print(f"  !! não consegui listar projetos: {e}")
        print("     As issues foram criadas. Para o quadro, rode:  gh auth refresh -s project")
        return

    numero = next((p["number"] for p in lista if p["title"] == titulo), None)
    if numero is None:
        criado = json.loads(
            gh("project", "create", "--owner", owner, "--title", titulo, "--format", "json")
        )
        numero = criado["number"]
        print(f"  ok   projeto criado: {criado.get('url', '')}")
    else:
        print(f"  --   projeto '{titulo}' já existe (#{numero})")

    for url in urls:
        try:
            gh("project", "item-add", str(numero), "--owner", owner, "--url", url)
        except ErroGh as e:
            print(f"  !! {url}: {e}")
    print(f"  ok   {len(urls)} issues adicionadas ao quadro")
    print("\n  O campo 'Status' do projeto já vem com Todo / In Progress / Done.")
    print("  Para ver como Kanban: abra o projeto e troque a view para Board.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="mostra o que seria criado, sem tocar no GitHub")
    args = ap.parse_args()

    dados = json.loads(BACKLOG.read_text(encoding="utf-8"))

    if args.dry_run:
        owner, repo = "<owner>", "<repo>"
        print("MODO DRY-RUN — nada será criado no GitHub.")
    else:
        owner, repo = confere_ambiente()
        print(f"Repositório alvo: {owner}/{repo}")

    cria_labels(dados["labels"], args.dry_run)
    cria_milestones(dados["milestones"], owner, repo, args.dry_run)
    urls = cria_issues(dados["issues"], args.dry_run)
    cria_projeto(dados["projeto"], owner, urls, args.dry_run)

    print(f"\nTotal no backlog: {len(dados['issues'])} issues, "
          f"{len(dados['milestones'])} milestones, {len(dados['labels'])} labels.")


if __name__ == "__main__":
    main()
