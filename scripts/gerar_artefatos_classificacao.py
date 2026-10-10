"""Gera os artefatos da classificação (issues #19, #20, #22).

- results/metrics/classificacao_*.csv: métricas, por gravação, severidade,
  generalização, erros, importâncias e as matrizes de confusão;
- results/metrics/matrizes_confusao.tex: as matrizes em LaTeX, incluídas no
  Apêndice C do relatório sem transcrição manual.

Uso (da raiz do repositório):  python -m scripts.gerar_artefatos_classificacao
"""

from __future__ import annotations

from src.data import RAIZ
from src.experimentos import dados_deteccao, rodar_classificacao

DIR_METRICS = RAIZ / "results" / "metrics"

NOMES_CLASSE = {"normal": "Normal", "IR": "Pista interna", "B": "Esfera", "OR": "Pista externa"}
NOMES_CLF = {"random_forest": "Random Forest", "svm": "SVM"}


def matriz_latex(m, conj: str, clf: str) -> str:
    rotulo = f"tab:confusao-{clf}-{conj}".replace("_", "-").replace("+", "-")
    cab = " & ".join(rf"\textbf{{{NOMES_CLASSE[c]}}}" for c in m.columns)
    linhas = [
        rf"    {NOMES_CLASSE[i]} & " + " & ".join(str(v) for v in m.loc[i]) + r" \\"
        for i in m.index
    ]
    return "\n".join(
        [
            r"\begin{table}[htb]",
            r"  \centering",
            rf"  \caption{{Matriz de confusão: {NOMES_CLF[clf]}, features ``{conj}'', teste em \SI{{3}}{{\hp}} (janelas).}}",
            rf"  \label{{{rotulo}}}",
            r"  \begin{tabular}{lcccc}",
            r"    \toprule",
            rf"    \textbf{{Verdadeira $\backslash$ Predita}} & {cab} \\",
            r"    \midrule",
            *linhas,
            r"    \bottomrule",
            r"  \end{tabular}",
            r"  \fonte{Gerada por \texttt{scripts/gerar\_artefatos\_classificacao.py}.}",
            r"\end{table}",
            "",
        ]
    )


def main() -> None:
    DIR_METRICS.mkdir(parents=True, exist_ok=True)
    F, meta, Fg, meta_g = dados_deteccao()
    r = rodar_classificacao(F, meta, Fg, meta_g)
    r["metricas"].to_csv(DIR_METRICS / "classificacao_metricas.csv", index=False, float_format="%.4f")
    for chave in ("por_registro", "severidade", "generalizacao", "erros", "importancias"):
        r[chave].to_csv(DIR_METRICS / f"classificacao_{chave}.csv", index=False, float_format="%.4f")
    blocos = ["% Gerado automaticamente. Não editar: rode o script."]
    for (conj, clf), m in r["matrizes"].items():
        m.to_csv(DIR_METRICS / f"classificacao_matriz_{clf}_{conj.replace('+', '_')}.csv")
        blocos.append(matriz_latex(m, conj, clf))
    (DIR_METRICS / "matrizes_confusao.tex").write_text("\n".join(blocos), encoding="utf-8")


if __name__ == "__main__":
    main()
