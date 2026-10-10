"""Extração de features de tempo, frequência e envelope.

Responsabilidades previstas:
- tempo: RMS, curtose, fator de crista, assimetria, valor de pico;
- frequência: FFT e análise de envelope (transformada de Hilbert);
- físico: frequências características do rolamento (BPFO, BPFI, BSF, FTF)
  a partir da geometria do SKF 6205-2RS JEM e da rotação do eixo;
- tempo-frequência (opcional): STFT, wavelet, kurtograma / spectral kurtosis
  para escolha da banda de demodulação.

Ver CLAUDE.md, seção 4.2.
"""

import warnings
from dataclasses import dataclass
from math import cos, radians

import numpy as np
import pandas as pd
from scipy import stats

# =============================================================================
# Domínio do tempo (issue #10)
# =============================================================================
#
# Entrada: matriz (n_janelas, tamanho_da_janela), uma janela de vibração por
# linha. Saída: DataFrame com UMA LINHA POR JANELA, na mesma ordem da entrada.
# Assim a linha i das features continua alinhada ao rótulo e ao split da janela
# i (passe o índice/metadados das janelas em `indice` para carregar esse vínculo).
#
# Definições (x = janela, N = número de amostras):
#
#     rms          = sqrt(mean(x^2))
#     pico         = max(|x|)
#     fator_crista = pico / rms
#     assimetria   = E[(x - mu)^3] / sigma^3
#     curtose      = E[(x - mu)^4] / sigma^4     (Pearson: sinal gaussiano -> 3)
#
# Duas decisões de projeto, declaradas no relatório (sec:features-tempo):
#
# 1. Curtose de Pearson (gaussiana = 3), e não "em excesso" (gaussiana = 0).
#    Impactos periódicos deixam o sinal mais impulsivo, e a curtose sobe bem
#    acima de 3.
# 2. Por padrão, a média de cada janela é removida antes de calcular rms, pico
#    e fator de crista. O offset (DC) do acelerômetro é um artefato de cada
#    gravação e não do defeito; deixá-lo entrar poderia dar ao modelo um atalho
#    para reconhecer a gravação em vez da falha. Assimetria e curtose já não
#    dependem da média.

NOMES_FEATURES_TEMPO = ["rms", "curtose", "fator_crista", "assimetria", "pico"]


def features_tempo(
    janelas: np.ndarray,
    indice=None,
    remover_media: bool = True,
) -> pd.DataFrame:
    """Calcula RMS, curtose, fator de crista, assimetria e pico de cada janela.

    Parâmetros
    ----------
    janelas : array (n_janelas, tamanho_da_janela)
    indice : opcional. Índice do DataFrame de saída (por exemplo, o dos
        metadados das janelas), para manter o alinhamento com rótulos e split.
    remover_media : se True (padrão), subtrai a média de cada janela antes de
        calcular rms, pico e fator de crista.

    Janela constante (rms = 0) gera fator de crista, assimetria e curtose NaN.
    """
    x = np.asarray(janelas, dtype=float)
    if x.ndim != 2:
        raise ValueError(
            f"janelas deve ser 2D (n_janelas, tamanho_da_janela); recebido ndim={x.ndim}"
        )
    if indice is not None and len(indice) != x.shape[0]:
        raise ValueError(
            f"indice tem {len(indice)} itens, mas há {x.shape[0]} janelas"
        )

    xc = x - x.mean(axis=1, keepdims=True) if remover_media else x

    rms = np.sqrt(np.mean(xc**2, axis=1))
    pico = np.max(np.abs(xc), axis=1)
    fator_crista = np.divide(pico, rms, out=np.full_like(rms, np.nan), where=rms > 0)

    # Janela constante: o scipy avisa e devolve NaN. Já está documentado acima.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        assimetria = stats.skew(x, axis=1)
        curtose = stats.kurtosis(x, axis=1, fisher=False)

    return pd.DataFrame(
        {
            "rms": rms,
            "curtose": curtose,
            "fator_crista": fator_crista,
            "assimetria": assimetria,
            "pico": pico,
        },
        index=indice,
    )[NOMES_FEATURES_TEMPO]


# =============================================================================
# Frequências características do rolamento (issue #12)
# =============================================================================
#
# Rolamento: SKF 6205-2RS JEM, drive end. Declarado no relatório em
# sec:features-frequencias.
#
# Fórmulas cinemáticas (Smith & Randall, 2015, p. 102), com f_r a rotação do eixo
# em Hz, n o número de esferas, d o diâmetro da esfera, D o diâmetro primitivo
# e phi o ângulo de contato:
#
#     BPFO = (n * f_r / 2) * (1 - (d / D) * cos(phi))     pista externa
#     BPFI = (n * f_r / 2) * (1 + (d / D) * cos(phi))     pista interna
#     FTF  = (f_r / 2)     * (1 - (d / D) * cos(phi))     gaiola
#     BSF  = (D * f_r / (2 * d)) * (1 - ((d / D) * cos(phi)) ** 2)   esfera
#
# Atenção: as fórmulas supõem ausência de escorregamento. Na prática, desvios
# de 1% a 2% em relação ao valor calculado são comuns (Smith & Randall, 2015,
# p. 102), por isso use `banda_tolerancia` ao procurar picos no espectro.
#
# Convenção da frequência da esfera: BSF é a da literatura (Smith & Randall,
# 2015, Tab. 2, p. 103): 2,357 x f_r no DE. O valor que a página do CWRU chama de
# "Rolling Element" (4,7135 x f_r) é 2 x BSF, exposto em `bsf_2x` só para
# conferência e para a busca do harmônico par.


@dataclass(frozen=True)
class GeometriaRolamento:
    """Geometria do rolamento. Comprimentos na mesma unidade (aqui, polegadas)."""

    n_esferas: int
    diametro_esfera: float  # d
    diametro_primitivo: float  # D
    angulo_contato_graus: float = 0.0  # phi


# Fontes:
#  - d e D: CWRU Bearing Data Center, página "Bearing Specifications"
#    (drive end: ball diameter 0.3126 in, pitch diameter 1.537 in).
#  - n = 9: Smith & Randall (2015), p. 109. Essa página do CWRU não informa n.
SKF_6205_DE = GeometriaRolamento(
    n_esferas=9, diametro_esfera=0.3126, diametro_primitivo=1.537
)


@dataclass(frozen=True)
class FrequenciasCaracteristicas:
    """Frequências em Hz."""

    bpfo: float  # pista externa
    bpfi: float  # pista interna
    bsf: float  # esfera (ball spin frequency), convenção de Smith & Randall
    ftf: float  # gaiola

    @property
    def bsf_2x(self) -> float:
        """2 x BSF: o "Rolling Element" da página do CWRU (4,7135 x f_r).

        Não é a frequência de referência do projeto (ver BSF acima). Fisicamente,
        a esfera com defeito bate nas duas pistas a cada giro, e por isso os
        harmônicos pares de BSF costumam dominar o espectro de envelope (Smith &
        Randall, 2015, Tab. 1, p. 103). Use este valor para procurar esse
        harmônico, sem trocar a convenção.
        """
        return 2.0 * self.bsf


def frequencias_caracteristicas(
    rpm: float, geometria: GeometriaRolamento = SKF_6205_DE
) -> FrequenciasCaracteristicas:
    """Calcula BPFO, BPFI, BSF e FTF (em Hz) a partir da rotação em rpm.

    Prefira a rotação medida em cada arquivo .mat (variável XnnnRPM) à nominal,
    porque a rotação real cai com a carga. 98.mat e 99.mat não trazem essa
    variável: neles use a nominal (1772 e 1750 rpm; ver data/raw/README.md).
    """
    if rpm <= 0:
        raise ValueError(f"rpm deve ser positivo, recebido {rpm!r}")

    f_r = rpm / 60.0
    n = geometria.n_esferas
    d = geometria.diametro_esfera
    big_d = geometria.diametro_primitivo
    razao = (d / big_d) * cos(radians(geometria.angulo_contato_graus))

    return FrequenciasCaracteristicas(
        bpfo=n * f_r / 2.0 * (1.0 - razao),
        bpfi=n * f_r / 2.0 * (1.0 + razao),
        bsf=big_d * f_r / (2.0 * d) * (1.0 - razao**2),
        ftf=f_r / 2.0 * (1.0 - razao),
    )


def banda_tolerancia(freq_hz: float, tol: float = 0.02) -> tuple[float, float]:
    """Janela de busca em torno de uma frequência teórica (padrão: +-2%).

    Os 2% vêm do escorregamento típico de 1% a 2% (Smith & Randall, 2015, p. 102).
    """
    return freq_hz * (1.0 - tol), freq_hz * (1.0 + tol)
