"""Features de domínio do tempo por janela (issue #10).

Entrada: matriz (n_janelas, tamanho_da_janela), uma janela de vibração por linha.
Saída: DataFrame com UMA LINHA POR JANELA, na mesma ordem da entrada. Assim a
linha i das features continua alinhada ao rótulo e ao split da janela i
(passe o índice/metadados das janelas em `index` para carregar esse vínculo).

Definições (x = janela, N = número de amostras):

    rms          = sqrt(mean(x^2))
    peak         = max(|x|)
    crest_factor = peak / rms
    skewness     = E[(x - mu)^3] / sigma^3
    kurtosis     = E[(x - mu)^4] / sigma^4     (Pearson: sinal gaussiano -> 3)

Duas decisões de projeto, para citar na seção 4.3 do relatório:

1. Curtose de Pearson (gaussiana = 3), e não "em excesso" (gaussiana = 0).
   É a convenção usual em diagnóstico de rolamentos: impactos periódicos
   deixam o sinal mais "pontudo", e a curtose sobe bem acima de 3.
2. Por padrão, a média de cada janela é removida antes de calcular rms, pico e
   fator de crista. O offset (DC) do acelerômetro é um artefato de cada
   gravação e não do defeito; deixá-lo entrar poderia dar ao modelo um atalho
   para reconhecer a gravação em vez da falha. Assimetria e curtose já não
   dependem da média.
"""

import warnings

import numpy as np
import pandas as pd
from scipy import stats

FEATURE_NAMES = ["rms", "kurtosis", "crest_factor", "skewness", "peak"]


def time_domain_features(
    windows: np.ndarray,
    index=None,
    remove_mean: bool = True,
) -> pd.DataFrame:
    """Calcula RMS, curtose, fator de crista, assimetria e pico de cada janela.

    Parâmetros
    ----------
    windows : array (n_janelas, tamanho_da_janela)
    index : opcional. Índice do DataFrame de saída (por exemplo, o dos metadados
        das janelas), para manter o alinhamento com rótulos e split.
    remove_mean : se True (padrão), subtrai a média de cada janela antes de
        calcular rms, pico e fator de crista.

    Janela constante (rms = 0) gera fator de crista, assimetria e curtose NaN.
    """
    x = np.asarray(windows, dtype=float)
    if x.ndim != 2:
        raise ValueError(
            f"windows deve ser 2D (n_janelas, tamanho_da_janela); recebido ndim={x.ndim}"
        )
    if index is not None and len(index) != x.shape[0]:
        raise ValueError(
            f"index tem {len(index)} itens, mas há {x.shape[0]} janelas"
        )

    xc = x - x.mean(axis=1, keepdims=True) if remove_mean else x

    rms = np.sqrt(np.mean(xc**2, axis=1))
    peak = np.max(np.abs(xc), axis=1)
    crest = np.divide(peak, rms, out=np.full_like(rms, np.nan), where=rms > 0)

    # Janela constante: o scipy avisa e devolve NaN. Já está documentado acima.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        skewness = stats.skew(x, axis=1)
        kurtosis = stats.kurtosis(x, axis=1, fisher=False)

    return pd.DataFrame(
        {
            "rms": rms,
            "kurtosis": kurtosis,
            "crest_factor": crest,
            "skewness": skewness,
            "peak": peak,
        },
        index=index,
    )[FEATURE_NAMES]
