"""Carregamento dos arquivos .mat do CWRU, segmentação em janelas e montagem dos splits.

- parser dos arquivos .mat (sinal do drive end), com decimação 48 -> 12 kHz dos
  normais (issue #6);
- segmentação em janelas cobrindo várias revoluções do eixo, com tamanho
  derivado da rotação e da taxa de amostragem (issue #7);
- split por condição de carga (treino: 0/1/2 HP; teste: 3 HP), nunca aleatório
  em nível de janela, e seeds fixas (issue #8);
- contagem de janelas por classe e carga (issue #9).

Ver CLAUDE.md, seção 3 (regras metodológicas) e seção 4 (pipeline).
"""

from __future__ import annotations

import random
from math import ceil
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.signal import cheby1, decimate, sosfiltfilt

from src.features import SKF_6205_DE, frequencias_caracteristicas

RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ / "data" / "raw"
MANIFESTO = DIR_RAW / "manifesto.csv"

# Semente única do projeto. Toda aleatoriedade (modelos, embaralhamento) parte
# dela, via `fixar_seeds`.
SEED = 42

# Taxa de amostragem de trabalho: a das gravações de falha do DE. Os normais
# (97-100) estão a 48 kHz e são decimados para ela (sec:decimacao-normais).
FS_HZ = 12_000

# Banda comum de análise: 0 a 4,8 kHz em TODAS as gravações. 4,8 kHz é o corte
# do filtro anti-aliasing do scipy.signal.decimate (0,8 x Nyquist de 12 kHz).
# Aplicado a todas as gravações depois da decimação (ver carregar_sinal). Sem isso, a faixa de 4,8-6 kHz ficaria atenuada
# só nos normais, e um modelo poderia separar as classes pelo pré-processamento
# (sec:decimacao-normais; results/figures/espectro_normal_decimado_vs_falhas.png).
CORTE_BANDA_COMUM_HZ = 4_800.0
_SOS_BANDA_COMUM = cheby1(8, 0.05, CORTE_BANDA_COMUM_HZ / (FS_HZ / 2), output="sos")

CARGAS_TREINO = (0, 1, 2)
CARGAS_TESTE = (3,)

# Posição do defeito em pista externa, em horas, com a zona de carga em 6 h
# (Smith & Randall, 2015, p. 104). @6 é a única posição com os três diâmetros
# (0.007", 0.014", 0.021") e deixa as classes equilibradas (12 IR, 12 B, 12 OR).
# @3 (ortogonal) e @12 (oposta) mudam a amplitude e a modulação do sinal, por isso
# ficam fora do experimento principal: servem para testar se um modelo treinado
# em @6 generaliza para outra posição. Ver docs/arquivos_excluidos.md (C5).
POSICAO_OR_PRINCIPAL = "6"
POSICOES_OR_GENERALIZACAO = ("3", "12")

CONJUNTOS = ("principal", "generalizacao")


def catalogo(conjunto: str = "principal") -> pd.DataFrame:
    """Registros de um conjunto do experimento, lidos de data/raw/manifesto.csv.

    - ``"principal"``: normais, IR, B e OR na posição ``POSICAO_OR_PRINCIPAL``
      (40 registros).
    - ``"generalizacao"``: só OR nas posições ``POSICOES_OR_GENERALIZACAO``
      (16 registros).

    Nenhum registro é excluído por qualidade; as ressalvas da auditoria estão em
    docs/arquivos_excluidos.md.
    """
    if conjunto not in CONJUNTOS:
        raise ValueError(f"conjunto deve ser um de {CONJUNTOS}, não {conjunto!r}")
    m = ler_manifesto()
    eh_or = m["classe"] == "OR"
    if conjunto == "principal":
        sel = ~eh_or | (m["posicao_or_h"] == POSICAO_OR_PRINCIPAL)
    else:
        sel = eh_or & m["posicao_or_h"].isin(POSICOES_OR_GENERALIZACAO)
    return m[sel].reset_index(drop=True)


# =============================================================================
# Leitura e decimação (issue #6)
# =============================================================================


def ler_manifesto() -> pd.DataFrame:
    """Manifesto completo (56 registros), com a coluna `rpm` já resolvida.

    `rpm` é a rotação medida no arquivo (variável XnnnRPM) ou, se o arquivo não
    a traz (98 e 99), a nominal da carga (data/raw/README.md, item 3).
    """
    # dtype=str em posicao_or_h: sem isso o pandas lê "6" como 6.0 e o filtro falha.
    m = pd.read_csv(MANIFESTO, dtype={"posicao_or_h": str, "diametro_pol": str})
    m["rpm"] = m["rpm_arquivo"].fillna(m["rpm_nominal"]).astype(float)
    return m


def carregar_sinal(registro: pd.Series, banda_comum: bool = True) -> np.ndarray:
    """Sinal do DE de um registro do manifesto, sempre a FS_HZ (12 kHz).

    A variável é lida pelo nome gravado no manifesto (`variavel_de`, ex.:
    X099_DE_time), nunca pela "primeira chave que termina em DE_time": o 99.mat
    traz também as variáveis do 98.

    Registros a 48 kHz (os normais) são decimados por 4 com
    `scipy.signal.decimate` padrão: IIR Chebyshev I de ordem 8, corte em
    0,8 x 6 kHz = 4,8 kHz, aplicado nos dois sentidos (fase zero, preserva a
    forma dos impulsos). Ver sec:decimacao no relatório.

    Com `banda_comum=True` (padrão), todo registro passa ainda, já a 12 kHz,
    pelo mesmo passa-baixas (Chebyshev I, ordem 8, 4,8 kHz, fase zero). Nas
    falhas ele faz o papel do filtro da decimação; nos normais, remove o resto
    de aliasing que o filtro do `decimate` deixa em 4,8-6 kHz (a 48 kHz há
    energia de 6 a 24 kHz que ele não atenua o bastante). Assim normais e falhas
    chegam ao modelo com a mesma banda. `False` devolve o sinal só decimado, ou
    como gravado (usado na figura de comparação).
    """
    var = registro["variavel_de"]
    mat = loadmat(DIR_RAW / registro["arquivo"], variable_names=[var])
    if var not in mat:
        raise KeyError(f"{registro['arquivo']} não tem a variável {var}")
    x = np.asarray(mat[var], dtype=float).ravel()

    fs = int(registro["fs_hz"])
    if fs != FS_HZ:
        q, resto = divmod(fs, FS_HZ)
        if resto:
            raise ValueError(f"{registro['arquivo']}: {fs} Hz não é múltiplo de {FS_HZ} Hz")
        x = decimate(x, q)
    if banda_comum:
        x = sosfiltfilt(_SOS_BANDA_COMUM, x)
    return x


# =============================================================================
# Segmentação em janelas (issue #7)
# =============================================================================

# Número de períodos da gaiola (FTF) que cada janela deve conter. É a
# modulação mais lenta das assinaturas de defeito (esfera: bandas laterais
# espaçadas de FTF; relatório, tab:assinaturas). Com 3 períodos, a resolução do
# espectro, fs/N, fica em no máximo FTF/3, o que separa essas bandas laterais
# dos picos vizinhos.
N_PERIODOS_FTF = 3


def tamanho_janela(
    rpm_min: float, fs: int = FS_HZ, n_periodos_ftf: int = N_PERIODOS_FTF
) -> int:
    """Número de amostras por janela, derivado da rotação e da taxa de amostragem.

    N_min = n_periodos_ftf * fs / FTF(rpm_min), arredondado para a potência de 2
    seguinte (FFT). Usa a menor rotação do conjunto, que dá a FTF mais baixa e
    portanto o período mais longo.

    Com os dados do projeto (rpm_min = 1718, registro 261; fs = 12 kHz):
        f_r = 1718 / 60          = 28,63 Hz
        FTF = 0,3983 * f_r       = 11,40 Hz
        N_min = 3 * 12000 / 11,40 = 3157 amostras
        N = 4096 amostras = 0,341 s
          = 9,8 revoluções do eixo a 1718 rpm (10,2 a 1797 rpm)
          = 3,9 períodos da gaiola; resolução fs/N = 2,93 Hz
    """
    ftf = frequencias_caracteristicas(rpm_min, SKF_6205_DE).ftf
    n_min = ceil(n_periodos_ftf * fs / ftf)
    return 1 << (n_min - 1).bit_length()


def segmentar(x: np.ndarray, tamanho: int, passo: int) -> np.ndarray:
    """Janelas (n_janelas, tamanho) de um sinal 1D; a sobra final é descartada."""
    if len(x) < tamanho:
        return np.empty((0, tamanho))
    return np.lib.stride_tricks.sliding_window_view(x, tamanho)[::passo].copy()


def montar_janelas(
    conjunto: str = "principal",
    tamanho: int | None = None,
    passo: int | None = None,
) -> tuple[np.ndarray, pd.DataFrame]:
    """Janelas de todos os registros de um conjunto e os metadados de cada uma.

    `tamanho` padrão: `tamanho_janela` com a menor rotação do manifesto inteiro,
    para que o conjunto principal e o de generalização usem a mesma janela.
    `passo` padrão: metade da janela (sobreposição de 50%). A sobreposição não
    cria vazamento porque o split é por registro, nunca por janela.

    Devolve (X, meta): a linha i de `meta` descreve a janela X[i]
    (registro, classe, diâmetro, posição OR, carga, rpm, índice da janela).
    """
    if tamanho is None:
        tamanho = tamanho_janela(ler_manifesto()["rpm"].min())
    if passo is None:
        passo = tamanho // 2

    cat = catalogo(conjunto)
    blocos, metas = [], []
    for _, reg in cat.iterrows():
        w = segmentar(carregar_sinal(reg), tamanho, passo)
        blocos.append(w)
        metas.append(
            pd.DataFrame(
                {
                    "registro": reg["id"],
                    "classe": reg["classe"],
                    "diametro_pol": reg["diametro_pol"],
                    "posicao_or_h": reg["posicao_or_h"],
                    "carga_hp": reg["carga_hp"],
                    "rpm": reg["rpm"],
                    "janela": np.arange(len(w)),
                }
            )
        )
    return np.vstack(blocos), pd.concat(metas, ignore_index=True)


# =============================================================================
# Split por carga e seeds (issue #8)
# =============================================================================


def fixar_seeds(seed: int = SEED) -> np.random.Generator:
    """Fixa as seeds do `random` e do `numpy` e devolve um Generator com a mesma."""
    random.seed(seed)
    np.random.seed(seed)
    return np.random.default_rng(seed)


def verificar_sem_vazamento(meta_treino: pd.DataFrame, meta_teste: pd.DataFrame) -> None:
    """Falha se algum registro tiver janelas no treino e no teste ao mesmo tempo."""
    comuns = set(meta_treino["registro"]) & set(meta_teste["registro"])
    if comuns:
        raise AssertionError(f"registros em treino e teste: {sorted(comuns)}")


def split_por_carga(
    meta: pd.DataFrame,
    cargas_treino: tuple[int, ...] = CARGAS_TREINO,
    cargas_teste: tuple[int, ...] = CARGAS_TESTE,
) -> tuple[np.ndarray, np.ndarray]:
    """Máscaras booleanas (treino, teste) sobre as janelas de `meta`.

    O split é por condição de carga, logo por registro: cada registro tem uma
    única carga, e todas as suas janelas caem do mesmo lado. A pergunta é se o
    modelo generaliza para uma carga não vista (CLAUDE.md, regras 1 e 2).
    """
    if set(cargas_treino) & set(cargas_teste):
        raise ValueError("cargas de treino e teste se sobrepõem")
    treino = meta["carga_hp"].isin(cargas_treino).to_numpy()
    teste = meta["carga_hp"].isin(cargas_teste).to_numpy()
    verificar_sem_vazamento(meta[treino], meta[teste])
    return treino, teste


# =============================================================================
# Contagem (issue #9)
# =============================================================================

ORDEM_CLASSES = ["normal", "IR", "B", "OR"]


def contagem_janelas(meta: pd.DataFrame) -> pd.DataFrame:
    """Janelas por classe (linhas) e carga (colunas), com totais."""
    t = pd.crosstab(meta["classe"], meta["carga_hp"], margins=True, margins_name="total")
    ordem = [c for c in ORDEM_CLASSES if c in t.index] + ["total"]
    return t.loc[ordem]
