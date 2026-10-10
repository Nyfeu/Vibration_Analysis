"""Gera os artefatos da validação física pelo espectro de envelope (issues #11 e #13).

- results/metrics/validacao_fisica.csv: escores por gravação e veredito;
- results/metrics/validacao_fisica_resumo.csv: confirmadas por classe, lado a
  lado com Smith & Randall (2015, Tab. B2);
- results/figures/envelope_por_classe_1hp.png: SES de uma gravação por classe
  com as frequências teóricas marcadas.

Uso (da raiz do repositório):  python -m scripts.gerar_artefatos_envelope
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from src.data import FS_HZ, RAIZ, carregar_sinal, ler_manifesto  # noqa: E402
from src.evaluation import resumo_validacao, validacao_fisica  # noqa: E402
from src.features import HARMONICOS, espectro_envelope, frequencias_caracteristicas  # noqa: E402

DIR_METRICS = RAIZ / "results" / "metrics"
DIR_FIGURES = RAIZ / "results" / "figures"

# Uma gravação por classe, todas a 1 HP. Falhas de 0,021" (IR, OR @6) e a
# esfera 223, a única que Smith & Randall diagnosticam com o envelope simples.
EXEMPLOS = [(98, "Normal"), (210, "Pista interna"), (223, "Esfera"), (131, "Pista externa")]

# Paleta categórica de referência, validada para daltonismo.
CORES = {"bpfo": "#2a78d6", "bpfi": "#eb6834", "bsf": "#1baf7a"}
ROTULOS = {"bpfo": "BPFO", "bpfi": "BPFI", "bsf": "BSF"}
COR_SES = "#3d3d3a"
F_MAX_HZ = 360.0


def figura() -> None:
    m = ler_manifesto().set_index("id")
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, eixos = plt.subplots(len(EXEMPLOS), 1, figsize=(7.2, 7.4), sharex=True, constrained_layout=True)
    for ax, (rid, nome) in zip(eixos, EXEMPLOS):
        reg = m.loc[rid].copy()
        reg["id"] = rid
        f, ses = espectro_envelope(carregar_sinal(reg), FS_HZ)
        faixa = (f > 2) & (f <= F_MAX_HZ)
        ses_n = ses / np.median(ses[faixa])
        ax.plot(f[faixa], ses_n[faixa], color=COR_SES, lw=0.7)
        fc = frequencias_caracteristicas(reg["rpm"])
        topo = ses_n[faixa].max()
        for familia, hs in HARMONICOS.items():
            base = getattr(fc, familia)
            for h in hs:
                ax.axvline(h * base, color=CORES[familia], lw=1.0, ls="--", zorder=0)
                rot = ROTULOS[familia] if h == 1 else f"{h}×{ROTULOS[familia]}"
                ax.text(h * base, topo * 1.02, rot, color="#5f5e5a", fontsize=7, ha="center", va="bottom")
        ax.set_ylim(0, topo * 1.18)
        ax.set_title(f"{nome} (registro {rid}, {reg['rpm']:.0f} rpm)", fontsize=9, loc="left")
        ax.set_ylabel("SES / mediana")
    eixos[-1].set_xlabel("Frequência (Hz)")
    eixos[-1].set_xlim(0, F_MAX_HZ)
    fig.savefig(DIR_FIGURES / "envelope_por_classe_1hp.png", dpi=200)


def main() -> None:
    DIR_METRICS.mkdir(parents=True, exist_ok=True)
    DIR_FIGURES.mkdir(parents=True, exist_ok=True)
    v = validacao_fisica()
    v.to_csv(DIR_METRICS / "validacao_fisica.csv", index=False, float_format="%.2f")
    resumo_validacao(v).to_csv(DIR_METRICS / "validacao_fisica_resumo.csv")
    figura()


if __name__ == "__main__":
    main()
