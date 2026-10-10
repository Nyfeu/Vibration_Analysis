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
from scipy.signal import hilbert

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


# =============================================================================
# Espectro de envelope (issue #11)
# =============================================================================
#
# Envelope ao quadrado do sinal analítico, |x + j H{x}|^2, e seu espectro (SES,
# squared envelope spectrum), como no "método 1" de Smith & Randall (2015,
# p. 104): sem filtro de banda, sobre todo o sinal. Aqui o sinal já chega
# limitado a 0-4,8 kHz pela banda comum (src/data.py). A taxa de repetição
# dos impactos aparece como pico na frequência característica do defeito.

# Harmônicos procurados para cada família. Escolhidos para que nenhum caia a
# menos de 2% (a tolerância) de um harmônico de outra família: 3 x BPFO e
# 2 x BPFI diferem 0,7%, e 2 x BPFO e 3 x BSF, 1,4%; com esses conjuntos as
# famílias ficam disjuntas. Na esfera, só os pares, que costumam dominar
# (Smith & Randall, 2015, Tab. 1, p. 103).
HARMONICOS = {"bpfo": (1, 2), "bpfi": (1, 2), "bsf": (2, 4)}

# Vizinhança usada para o nível de fundo local: +-20% em torno de cada
# harmônico, excluída a própria banda de tolerância.
VIZINHANCA_FUNDO = 0.20


def espectro_envelope(x: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray]:
    """Espectro do envelope ao quadrado (SES) ao longo do último eixo.

    Aceita um sinal 1D ou uma matriz (n_janelas, tamanho). A média do envelope
    é removida (senão o pico em 0 Hz domina) e uma janela de Hann reduz o
    vazamento espectral. Devolve (f, amplitude), com resolução fs / tamanho.
    """
    x = np.asarray(x, dtype=float)
    env2 = np.abs(hilbert(x, axis=-1)) ** 2
    env2 = env2 - env2.mean(axis=-1, keepdims=True)
    n = x.shape[-1]
    ses = np.abs(np.fft.rfft(env2 * np.hanning(n), axis=-1)) * 2.0 / n
    return np.fft.rfftfreq(n, 1.0 / fs), ses


def pico_na_banda(
    f: np.ndarray, ses: np.ndarray, freq_hz: float, tol: float = 0.02
) -> np.ndarray:
    """Maior amplitude do SES em freq_hz +- tol (ao menos +- 1 raia espectral)."""
    df = f[1] - f[0]
    meia = max(freq_hz * tol, df)
    banda = (f >= freq_hz - meia) & (f <= freq_hz + meia)
    return ses[..., banda].max(axis=-1)


def escores_envelope(
    f: np.ndarray, ses: np.ndarray, rpm, geometria: GeometriaRolamento = SKF_6205_DE
) -> pd.DataFrame:
    """Força de cada família de defeito no SES, em dB acima do fundo local.

    Para cada harmônico de `HARMONICOS`, razão entre o pico na banda de
    tolerância e a mediana do SES na vizinhança de +-`VIZINHANCA_FUNDO`; a
    família recebe a média dessas razões, em dB. O fundo local compensa a
    queda do SES com a frequência. `rpm` é escalar ou um valor por linha de
    `ses` (a rotação de cada janela).
    """
    ses = np.atleast_2d(ses)
    rpm = np.broadcast_to(np.asarray(rpm, dtype=float), (ses.shape[0],))

    saida = {}
    for familia, hs in HARMONICOS.items():
        valores = np.empty(ses.shape[0])
        for i, (linha, r) in enumerate(zip(ses, rpm)):
            base = getattr(frequencias_caracteristicas(r, geometria), familia)
            razoes = []
            for h in hs:
                fc = h * base
                viz = (np.abs(f - fc) <= VIZINHANCA_FUNDO * fc) & (np.abs(f - fc) > 0.02 * fc)
                razoes.append(pico_na_banda(f, linha, fc) / np.median(linha[viz]))
            valores[i] = np.mean(razoes)
        saida[f"env_{familia}"] = 10 * np.log10(valores)
    return pd.DataFrame(saida)


NOMES_FEATURES_ENVELOPE = [f"env_{familia}" for familia in HARMONICOS]


def features_envelope(janelas: np.ndarray, rpm, fs: float, indice=None) -> pd.DataFrame:
    """Escores de envelope por janela (uma linha por janela, mesma ordem)."""
    f, ses = espectro_envelope(janelas, fs)
    df = escores_envelope(f, ses, rpm)
    if indice is not None:
        df.index = indice
    return df


# =============================================================================
# Matriz de features completa
# =============================================================================

NOMES_FEATURES = NOMES_FEATURES_TEMPO + NOMES_FEATURES_ENVELOPE

# Conjuntos usados nos experimentos. "forma" exclui rms e pico, que dependem da
# amplitude absoluta do sinal: serve para testar se um modelo reage ao defeito
# ou só ao nível de vibração (que também muda com a montagem e o sensor).
CONJUNTOS_FEATURES = {
    "tempo": NOMES_FEATURES_TEMPO,
    "envelope": NOMES_FEATURES_ENVELOPE,
    "tempo+envelope": NOMES_FEATURES,
    "forma": ["curtose", "fator_crista", "assimetria"] + NOMES_FEATURES_ENVELOPE,
}


def matriz_features(janelas: np.ndarray, rpm, fs: float, indice=None) -> pd.DataFrame:
    """Features de tempo e de envelope por janela, na ordem de NOMES_FEATURES."""
    tempo = features_tempo(janelas)
    env = features_envelope(janelas, rpm, fs)
    df = pd.concat([tempo, env], axis=1)[NOMES_FEATURES]
    if indice is not None:
        df.index = indice
    return df


# =============================================================================
# Curtose espectral e kurtograma (issue #14)
# =============================================================================
#
# A curtose espectral (SK) mede, para cada frequência, quão impulsivo é o sinal
# naquela faixa (Antoni, 2006). Impactos de defeito excitam ressonâncias e
# elevam a SK na banda delas; ruído estacionário tem SK ~ 0. O kurtograma
# calcula a SK para várias resoluções (larguras de banda) e escolhe a banda de
# maior SK como banda de demodulação (Antoni; Randall, 2006; Antoni, 2007).
# Aqui a SK é estimada pela STFT: SK(f) = <|X(t,f)|^4> / <|X(t,f)|^2>^2 - 2.

# Comprimentos de janela da STFT avaliados. A largura de banda de cada raia é
# ~ fs / Nw: a 12 kHz, 1500, 750 e 375 Hz.
JANELAS_SK = (8, 16, 32)

# Banda mínima: 3 x a maior BPFI do conjunto (~162 Hz a 1797 rpm), para que a
# banda filtrada contenha a portadora e as bandas laterais da modulação.
BANDA_MIN_HZ = 3 * 5.4152 * 1797 / 60


def curtose_espectral(x: np.ndarray, fs: float, nw: int) -> tuple[np.ndarray, np.ndarray]:
    """SK(f) de um sinal 1D pela STFT com janela de Hann de nw amostras."""
    from scipy.signal import stft

    f, _, z = stft(x, fs=fs, window="hann", nperseg=nw, noverlap=3 * nw // 4, boundary=None)
    p2 = np.mean(np.abs(z) ** 2, axis=1)
    p4 = np.mean(np.abs(z) ** 4, axis=1)
    return f, p4 / p2**2 - 2.0


def banda_kurtograma(
    x: np.ndarray, fs: float, f_max: float = 4800.0, janelas=JANELAS_SK
) -> tuple[float, float, float]:
    """Banda (f_baixa, f_alta) de maior curtose espectral e o valor da SK.

    Percorre as resoluções de `janelas`, descarta bandas mais estreitas que
    BANDA_MIN_HZ ou que ultrapassem f_max (a banda comum), e devolve a melhor.
    """
    melhor = (np.nan, np.nan, -np.inf)
    for nw in janelas:
        largura = fs / nw
        if largura < BANDA_MIN_HZ:
            continue
        f, sk = curtose_espectral(x, fs, nw)
        validas = (f - largura / 2 > 0) & (f + largura / 2 <= f_max)
        if not validas.any():
            continue
        i = np.argmax(np.where(validas, sk, -np.inf))
        if sk[i] > melhor[2]:
            melhor = (f[i] - largura / 2, f[i] + largura / 2, float(sk[i]))
    return melhor


def filtrar_banda(x: np.ndarray, fs: float, f_baixa: float, f_alta: float) -> np.ndarray:
    """Passa-banda Butterworth de ordem 4, fase zero."""
    from scipy.signal import butter, sosfiltfilt

    sos = butter(4, [f_baixa, f_alta], btype="bandpass", fs=fs, output="sos")
    return sosfiltfilt(sos, x, axis=-1)


def prebranquear(x: np.ndarray) -> np.ndarray:
    """Pré-branqueamento cepstral: espectro com magnitude unitária e a fase
    original ("método 2" de Smith & Randall, 2015, p. 104). Iguala o peso de
    todas as faixas, de modo que as mais impulsivas passam a dominar o sinal,
    e remove os picos discretos fortes que mascaram o defeito."""
    espectro = np.fft.rfft(x, axis=-1)
    return np.fft.irfft(espectro / np.maximum(np.abs(espectro), 1e-12), n=x.shape[-1], axis=-1)


PREPROCESSAMENTOS = ("bruto", "prebranqueado", "kurtograma")


def preprocessar_envelope(x: np.ndarray, fs: float, metodo: str) -> np.ndarray:
    """Sinal pronto para o envelope, segundo o pré-processamento escolhido:
    - "bruto": o sinal na banda comum (método 1 de Smith & Randall);
    - "prebranqueado": pré-branqueamento cepstral (método 2);
    - "kurtograma": filtro na banda de maior curtose espectral, sem a separação
      de componentes discretos (DRS) que o método 3 do artigo aplica antes.
    """
    if metodo == "bruto":
        return x
    if metodo == "prebranqueado":
        return prebranquear(x)
    if metodo == "kurtograma":
        f_baixa, f_alta, _ = banda_kurtograma(x, fs)
        return filtrar_banda(x, fs, f_baixa, f_alta)
    raise ValueError(f"pré-processamento desconhecido: {metodo}")
