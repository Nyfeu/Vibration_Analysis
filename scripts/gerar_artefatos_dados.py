"""Gera os artefatos da etapa de dados para o relatório.

- results/metrics/contagem_janelas_{principal,generalizacao}.csv (issue #9);
- results/metrics/energia_banda_4k8_6k.csv: fração da potência de cada registro
  na faixa de 4,8-6 kHz, antes (normais só decimados, falhas como gravadas) e
  depois do passa-baixas da banda comum;
- results/metrics/energia_banda_4k8_6k_por_classe.csv: mínimo e máximo por classe;
- results/figures/espectro_normal_decimado_vs_falhas.png.

Uso (da raiz do repositório):  python -m scripts.gerar_artefatos_dados
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.signal import welch  # noqa: E402

from src.data import (  # noqa: E402
    FS_HZ,
    RAIZ,
    carregar_sinal,
    catalogo,
    contagem_janelas,
    montar_janelas,
)

DIR_METRICS = RAIZ / "results" / "metrics"
DIR_FIGURES = RAIZ / "results" / "figures"

# Corte do filtro de scipy.signal.decimate (q = 4): 0,8 x 6 kHz.
CORTE_HZ = 4800.0
NYQUIST_HZ = FS_HZ / 2

# Paleta categórica de referência (validada para daltonismo); cinza = referência.
COR_NORMAL = "#8a8a85"
CORES = {"IR": "#eb6834", "B": "#1baf7a", "OR": "#2a78d6"}
NOMES = {"normal": "Normal", "IR": "Pista interna", "B": "Esfera", "OR": "Pista externa"}


def psd(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """PSD de Welch com segmentos de 4096 amostras (a janela de análise)."""
    return welch(x, fs=FS_HZ, nperseg=4096)


def fracao_na_banda(f: np.ndarray, p: np.ndarray) -> float:
    banda = (f >= CORTE_HZ) & (f <= NYQUIST_HZ)
    return float(p[banda].sum() / p.sum())


def contagens() -> None:
    for conjunto in ("principal", "generalizacao"):
        _, meta = montar_janelas(conjunto)
        contagem_janelas(meta).to_csv(DIR_METRICS / f"contagem_janelas_{conjunto}.csv")


def energia_e_figura() -> None:
    cat = catalogo("principal")
    linhas, espectros = [], {}
    for _, reg in cat.iterrows():
        f, p = psd(carregar_sinal(reg, banda_comum=False))
        f2, p2 = psd(carregar_sinal(reg))
        espectros[reg["id"]] = (f, p)
        linhas.append(
            {
                "registro": reg["id"],
                "classe": reg["classe"],
                "diametro_pol": reg["diametro_pol"],
                "carga_hp": reg["carga_hp"],
                "fracao_antes": fracao_na_banda(f, p),
                "fracao_depois": fracao_na_banda(f2, p2),
            }
        )
    energia = pd.DataFrame(linhas)
    energia.to_csv(DIR_METRICS / "energia_banda_4k8_6k.csv", index=False)
    (
        energia.groupby("classe")[["fracao_antes", "fracao_depois"]]
        .agg(["min", "max"])
        .loc[["normal", "IR", "B", "OR"]]
        .to_csv(DIR_METRICS / "energia_banda_4k8_6k_por_classe.csv")
    )

    # Mesma carga (0 HP) e menor diâmetro (0.007"): a comparação mais próxima
    # do normal 97.
    ref = cat[(cat["classe"] == "normal") & (cat["carga_hp"] == 0)]["id"].item()
    falhas = {
        c: cat[(cat["classe"] == c) & (cat["carga_hp"] == 0) & (cat["diametro_pol"] == "0.007")][
            "id"
        ].item()
        for c in ("IR", "B", "OR")
    }

    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, eixos = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True, constrained_layout=True)
    fn, pn = espectros[ref]
    for ax, (classe, rid) in zip(eixos, falhas.items()):
        f, p = espectros[rid]
        ax.axvspan(CORTE_HZ / 1e3, NYQUIST_HZ / 1e3, color="#e8e7e2", lw=0)
        ax.plot(fn / 1e3, 10 * np.log10(pn), color=COR_NORMAL, lw=1.0, label=f"Normal ({ref}, decimado)")
        ax.plot(f / 1e3, 10 * np.log10(p), color=CORES[classe], lw=1.0, label=f"{NOMES[classe]} ({rid})")
        ax.set_title(f"{NOMES[classe]} ({rid}) × normal ({ref})", fontsize=9)
        ax.set_xlim(0, NYQUIST_HZ / 1e3)
        ax.set_xlabel("Frequência (kHz)")
        ax.grid(axis="y", color="#e8e7e2", lw=0.6)
        ax.legend(loc="lower left", fontsize=7, frameon=False)
    eixos[0].set_ylabel("PSD (dB re 1 unidade²/Hz)")
    eixos[0].text(5.4, eixos[0].get_ylim()[1], "4,8–6 kHz", ha="center", va="top", fontsize=7, color="#5f5e5a")
    fig.savefig(DIR_FIGURES / "espectro_normal_decimado_vs_falhas.png", dpi=200)


def main() -> None:
    DIR_METRICS.mkdir(parents=True, exist_ok=True)
    DIR_FIGURES.mkdir(parents=True, exist_ok=True)
    contagens()
    energia_e_figura()


if __name__ == "__main__":
    main()
