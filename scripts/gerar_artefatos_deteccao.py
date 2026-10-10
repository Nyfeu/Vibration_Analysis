"""Gera os artefatos da detecção one-class (issues #15–#18).

- results/metrics/deteccao_metricas.csv: AUC, TPR, FPR por detector e conjunto
  de features (teste em 3 HP) e TPR no conjunto de generalização;
- results/metrics/deteccao_por_registro.csv: taxa de alarme por gravação;
- results/metrics/deteccao_tpr_por_grupo_smith.csv: TPR por categoria Y/P/N;
- results/metrics/deteccao_erros.csv: janelas erradas de cada experimento;
- results/figures/deteccao_roc_por_conjunto_de_features.png;
- results/figures/rms_por_gravacao.png.

Uso (da raiz do repositório):  python -m scripts.gerar_artefatos_deteccao
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import roc_curve  # noqa: E402

from src.data import RAIZ  # noqa: E402
from src.detection import DETECTORES  # noqa: E402
from src.experimentos import dados_deteccao, rodar_deteccao, tpr_por_grupo_smith  # noqa: E402
from src.features import CONJUNTOS_FEATURES  # noqa: E402

DIR_METRICS = RAIZ / "results" / "metrics"
DIR_FIGURES = RAIZ / "results" / "figures"

# Paleta categórica de referência (ordem fixa), validada para daltonismo.
CORES_DET = dict(zip(DETECTORES, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]))
NOMES_DET = {
    "mahalanobis": "Mahalanobis",
    "isolation_forest": "Isolation Forest",
    "ocsvm": "One-Class SVM",
    "autoencoder": "Autoencoder",
}
CORES_CLASSE = {"normal": "#8a8a85", "IR": "#eb6834", "B": "#1baf7a", "OR": "#2a78d6"}
NOMES_CLASSE = {"normal": "Normal", "IR": "Pista interna", "B": "Esfera", "OR": "Pista externa"}

plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})


def figura_roc(metricas: pd.DataFrame, eh_falha: np.ndarray, escores: dict) -> None:
    fig, eixos = plt.subplots(2, 2, figsize=(7.2, 6.6), sharex=True, sharey=True, constrained_layout=True)
    for ax, conj in zip(eixos.ravel(), CONJUNTOS_FEATURES):
        ax.plot([0, 1], [0, 1], color="#c3c2b7", lw=0.8, ls=":")
        for nome in DETECTORES:
            fpr, tpr, _ = roc_curve(eh_falha, escores[(conj, nome)])
            auc = metricas.query("features == @conj and detector == @nome")["auc"].item()
            ax.plot(fpr, tpr, color=CORES_DET[nome], lw=1.5, label=f"{NOMES_DET[nome]} (AUC {auc:.2f})".replace(".", ","))
        ax.set_title(f"Features: {conj}", fontsize=9, loc="left")
        ax.legend(loc="lower right", fontsize=7, frameon=False)
        ax.set_aspect("equal")
    for ax in eixos[1]:
        ax.set_xlabel("FPR")
    for ax in eixos[:, 0]:
        ax.set_ylabel("TPR")
    fig.savefig(DIR_FIGURES / "deteccao_roc_por_conjunto_de_features.png", dpi=200)


def figura_rms(F: pd.DataFrame, meta: pd.DataFrame) -> None:
    """RMS mediano de cada gravação: mostra que a amplitude sozinha separa
    normal de falha, inclusive nas gravações sem assinatura física."""
    d = pd.concat([meta[["registro", "classe", "carga_hp"]], F["rms"]], axis=1)
    g = d.groupby(["registro", "classe", "carga_hp"])["rms"].median().reset_index()
    ordem = ["normal", "IR", "B", "OR"]
    fig, ax = plt.subplots(figsize=(7.2, 2.8), constrained_layout=True)
    teto_normal = g.loc[g["classe"] == "normal", "rms"].max()
    ax.axhline(teto_normal, color="#8a8a85", lw=0.8, ls="--")
    ax.text(3.45, teto_normal, " maior RMS normal", va="bottom", ha="right", fontsize=7, color="#5f5e5a")
    for i, c in enumerate(ordem):
        s = g[g["classe"] == c].sort_values("registro")
        x = i + np.linspace(-0.3, 0.3, len(s))
        teste = s["carga_hp"] == 3
        ax.scatter(x[~teste.to_numpy()], s["rms"][~teste], s=28, color=CORES_CLASSE[c], edgecolor="white", lw=0.8, label=None)
        ax.scatter(x[teste.to_numpy()], s["rms"][teste], s=28, facecolor="white", edgecolor=CORES_CLASSE[c], lw=1.4)
        for xi, (_, r) in zip(x, s.iterrows()):
            if r["registro"] in (200, 225):  # teste, sem assinatura física
                ax.annotate(str(r["registro"]), (xi, r["rms"]), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=6.5, color="#5f5e5a")
    ax.set_xticks(range(len(ordem)), [NOMES_CLASSE[c] for c in ordem])
    ax.set_yscale("log")
    ticks = [0.05, 0.1, 0.2, 0.5, 1.0]
    ax.set_yticks(ticks, [f"{t:g}".replace(".", ",") for t in ticks])
    ax.minorticks_off()
    ax.set_ylabel("RMS mediano por gravação")
    ax.scatter([], [], s=28, color="#5f5e5a", label="treino (0–2 HP)")
    ax.scatter([], [], s=28, facecolor="white", edgecolor="#5f5e5a", lw=1.4, label="teste (3 HP)")
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    fig.savefig(DIR_FIGURES / "rms_por_gravacao.png", dpi=200)


def main() -> None:
    DIR_METRICS.mkdir(parents=True, exist_ok=True)
    DIR_FIGURES.mkdir(parents=True, exist_ok=True)
    F, meta, Fg, meta_g = dados_deteccao()
    metricas, por_registro, erros, (eh_falha, escores) = rodar_deteccao(F, meta, Fg, meta_g)
    metricas.to_csv(DIR_METRICS / "deteccao_metricas.csv", index=False, float_format="%.4f")
    por_registro.to_csv(DIR_METRICS / "deteccao_por_registro.csv", index=False, float_format="%.4f")
    tpr_por_grupo_smith(por_registro).to_csv(DIR_METRICS / "deteccao_tpr_por_grupo_smith.csv", float_format="%.4f")
    erros.to_csv(DIR_METRICS / "deteccao_erros.csv", index=False, float_format="%.4f")
    figura_roc(metricas, eh_falha, escores)
    figura_rms(F, meta)


if __name__ == "__main__":
    main()
