#!/usr/bin/env python3
"""Baixa o subconjunto do CWRU usado no projeto e confere a integridade dos arquivos.

Subconjunto: drive end, 12 kHz, diâmetros 0.007"/0.014"/0.021", cargas 0–3 HP, mais
os quatro arquivos de linha de base normal. O catálogo abaixo foi transcrito das
páginas oficiais do CWRU Bearing Data Center (consultadas em 2026-10-06):

    https://engineering.case.edu/bearingdatacenter/normal-baseline-data
    https://engineering.case.edu/bearingdatacenter/12k-drive-end-bearing-fault-data

Os .mat ficam versionados em data/raw/; este script serve para reproduzir o
download do zero e para verificar que os arquivos não foram alterados.

Uso:
    python scripts/download_cwru.py               # baixa o que falta e confere SHA-256
    python scripts/download_cwru.py --manifesto   # (re)gera data/raw/manifesto.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
MANIFESTO = RAW / "manifesto.csv"
URL = "https://engineering.case.edu/sites/default/files/{id}.mat"

# Rotação aproximada por carga, conforme a tabela oficial.
RPM_NOMINAL = {0: 1797, 1: 1772, 2: 1750, 3: 1730}

# (classe, diâmetro em polegadas, posição do defeito na pista externa) -> ids por carga 0..3.
# Posição em horas, como no cabeçalho da tabela oficial ("@6", "@3", "@12").
CATALOGO: dict[tuple[str, str, str], tuple[int, int, int, int]] = {
    ("normal", "", ""): (97, 98, 99, 100),
    ("IR", "0.007", ""): (105, 106, 107, 108),
    ("B", "0.007", ""): (118, 119, 120, 121),
    ("OR", "0.007", "6"): (130, 131, 132, 133),
    ("OR", "0.007", "3"): (144, 145, 146, 147),
    ("OR", "0.007", "12"): (156, 158, 159, 160),
    ("IR", "0.014", ""): (169, 170, 171, 172),
    ("B", "0.014", ""): (185, 186, 187, 188),
    ("OR", "0.014", "6"): (197, 198, 199, 200),  # @3 e @12 não existem a 12 kHz
    ("IR", "0.021", ""): (209, 210, 211, 212),
    ("B", "0.021", ""): (222, 223, 224, 225),
    ("OR", "0.021", "6"): (234, 235, 236, 237),
    ("OR", "0.021", "3"): (246, 247, 248, 249),
    ("OR", "0.021", "12"): (258, 259, 260, 261),
}

# Taxa de amostragem real de cada grupo. A página oficial não declara a taxa dos
# arquivos normais; a linha de 120 Hz (2x a rede de 60 Hz) só cai em 120,0 Hz se
# eles forem lidos a 48 kHz. Ver data/raw/README.md.
FS_NORMAL = 48_000
FS_FALHA = 12_000


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def registros():
    for (classe, diametro, posicao), ids in CATALOGO.items():
        for carga, id_ in enumerate(ids):
            yield {"id": id_, "classe": classe, "diametro_pol": diametro,
                   "posicao_or_h": posicao, "carga_hp": carga}


def baixar() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    esperado = {}
    if MANIFESTO.exists():
        with MANIFESTO.open(newline="") as f:
            esperado = {r["arquivo"]: r["sha256"] for r in csv.DictReader(f)}
    erros = 0
    for r in registros():
        destino = RAW / f"{r['id']}.mat"
        if not destino.exists():
            print(f"baixando {destino.name}")
            req = urllib.request.Request(URL.format(id=r["id"]), headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp, destino.open("wb") as f:
                f.write(resp.read())
        if destino.name in esperado and sha256(destino) != esperado[destino.name]:
            print(f"SHA-256 divergente: {destino.name}", file=sys.stderr)
            erros += 1
    print(f"{sum(1 for _ in registros())} arquivos em {RAW.relative_to(RAIZ)}; {erros} divergência(s).")
    return 1 if erros else 0


def gerar_manifesto() -> int:
    import numpy as np
    from scipy.io import loadmat

    linhas = []
    for r in registros():
        caminho = RAW / f"{r['id']}.mat"
        m = loadmat(caminho)
        var_de = f"X{r['id']:03d}_DE_time"
        n = int(np.ravel(m[var_de]).size)
        rpm = [k for k in m if k.endswith("RPM")]
        fs = FS_NORMAL if r["classe"] == "normal" else FS_FALHA
        linhas.append({
            "arquivo": caminho.name, **r,
            "rpm_nominal": RPM_NOMINAL[r["carga_hp"]],
            "rpm_arquivo": int(np.ravel(m[rpm[0]])[0]) if rpm else "",
            "variavel_de": var_de, "n_amostras_de": n, "fs_hz": fs,
            "duracao_s": round(n / fs, 2), "sha256": sha256(caminho),
            "url": URL.format(id=r["id"]),
        })
    with MANIFESTO.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    print(f"{MANIFESTO.relative_to(RAIZ)}: {len(linhas)} arquivos.")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--manifesto", action="store_true", help="(re)gera data/raw/manifesto.csv")
    sys.exit(gerar_manifesto() if p.parse_args().manifesto else baixar())
