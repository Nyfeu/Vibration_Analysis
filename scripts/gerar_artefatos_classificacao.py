"""Gera os artefatos da classificação (issues #19, #20, #21, #22).

- results/metrics/classificacao_selecao_modelos.csv: acurácia de cada modelo
  candidato na validação cruzada do treino (por carga e embaralhada);
- results/metrics/classificacao_melhores_parametros.csv: GridSearchCV;
- results/metrics/classificacao_*.csv: métricas no teste, por gravação,
  severidade, generalização, erros, importâncias, matrizes de confusão e
  classification_report de cada configuração;
- results/metrics/matrizes_confusao.tex: matrizes em LaTeX para o Apêndice C;
- CNN 1D (se o PyTorch estiver instalado): linhas extras nas métricas e matrizes.

Uso (da raiz do repositório):  python -m scripts.gerar_artefatos_classificacao
"""

from __future__ import annotations

import pandas as pd

from src.data import RAIZ
from src.experimentos import dados_deteccao, rodar_classificacao

DIR_METRICS = RAIZ / "results" / "metrics"

NOMES_CLASSE = {"normal": "Normal", "IR": "Pista interna", "B": "Esfera", "OR": "Pista externa"}


def _slug(texto: str) -> str:
    return (
        texto.lower().replace(" (rbf)", "").replace(" ", "_").replace("+", "_").replace("(", "").replace(")", "")
    )


def matriz_latex(m, conj: str, clf: str) -> str:
    rotulo = f"tab:confusao-{_slug(clf)}-{_slug(conj)}".replace("_", "-")
    cab = " & ".join(rf"\textbf{{{NOMES_CLASSE[c]}}}" for c in m.columns)
    linhas = [
        rf"    {NOMES_CLASSE[i]} & " + " & ".join(str(v) for v in m.loc[i]) + r" \\" for i in m.index
    ]
    entrada = f"entrada ``{conj}''" if conj.startswith("sinal") else f"features ``{conj}''"
    return "\n".join(
        [
            r"\begin{table}[htb]",
            r"  \centering",
            rf"  \caption{{Matriz de confusão: {clf}, {entrada}, teste em \SI{{3}}{{\hp}} (janelas).}}",
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
    for antigo in DIR_METRICS.glob("classificacao_matriz_*.csv"):
        antigo.unlink()
    for antigo in DIR_METRICS.glob("classificacao_relatorio_*.csv"):
        antigo.unlink()

    F, meta, Fg, meta_g = dados_deteccao()
    r = rodar_classificacao(F, meta, Fg, meta_g)
    metricas, matrizes = r["metricas"], dict(r["matrizes"])

    try:
        from src.experimentos import rodar_cnn

        m_cnn, mat_cnn, reg_cnn = rodar_cnn()
        metricas = pd.concat([metricas, m_cnn], ignore_index=True)
        matrizes.update(mat_cnn)
        reg_cnn.to_csv(DIR_METRICS / "classificacao_cnn_por_registro.csv", index=False, float_format="%.4f")
    except ImportError:
        print("PyTorch não instalado: CNN 1D ignorada.")

    metricas.to_csv(DIR_METRICS / "classificacao_metricas.csv", index=False, float_format="%.4f")
    r["selecao"].to_csv(DIR_METRICS / "classificacao_selecao_modelos.csv", index=False, float_format="%.4f")
    r["melhores_parametros"].to_csv(
        DIR_METRICS / "classificacao_melhores_parametros.csv", index=False, float_format="%.4f"
    )
    for chave in ("por_registro", "severidade", "generalizacao", "erros", "importancias"):
        r[chave].to_csv(DIR_METRICS / f"classificacao_{chave}.csv", index=False, float_format="%.4f")
    for (conj, clf), rel in r["relatorios"].items():
        rel.to_csv(DIR_METRICS / f"classificacao_relatorio_{_slug(clf)}_{_slug(conj)}.csv", float_format="%.4f")

    blocos = ["% Gerado automaticamente. Não editar: rode o script."]
    for (conj, clf), m in matrizes.items():
        m.to_csv(DIR_METRICS / f"classificacao_matriz_{_slug(clf)}_{_slug(conj)}.csv")
        blocos.append(matriz_latex(m, conj, clf))
    (DIR_METRICS / "matrizes_confusao.tex").write_text("\n".join(blocos), encoding="utf-8")


if __name__ == "__main__":
    main()
