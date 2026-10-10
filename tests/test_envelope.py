import itertools

import numpy as np
import pytest

from src.data import FS_HZ, carregar_sinal, ler_manifesto
from src.evaluation import resumo_validacao, validacao_fisica
from src.features import (
    HARMONICOS,
    NOMES_FEATURES_ENVELOPE,
    espectro_envelope,
    features_envelope,
    frequencias_caracteristicas,
)


@pytest.fixture(scope="module")
def manifesto():
    return ler_manifesto().set_index("id", drop=False)


def _escore(manifesto, rid):
    reg = manifesto.loc[rid]
    janelas = carregar_sinal(reg)[None, :]
    return features_envelope(janelas, reg["rpm"], FS_HZ).iloc[0]


def test_harmonicos_das_familias_nao_colidem_na_tolerancia():
    fc = frequencias_caracteristicas(60.0)  # múltiplos de f_r
    pares = [(fam, h * getattr(fc, fam)) for fam, hs in HARMONICOS.items() for h in hs]
    for (fa, a), (fb, b) in itertools.combinations(pares, 2):
        if fa != fb:
            assert abs(a - b) / min(a, b) > 0.04, (fa, a, fb, b)


def test_ses_tem_resolucao_fs_sobre_n_e_sem_pico_em_zero(manifesto):
    x = carregar_sinal(manifesto.loc[131])[:4096]
    f, ses = espectro_envelope(x, FS_HZ)
    assert f[1] == pytest.approx(FS_HZ / 4096)
    assert ses[0] < ses.max() / 100  # média do envelope removida


@pytest.mark.parametrize("rid, familia", [(131, "env_bpfo"), (210, "env_bpfi"), (105, "env_bpfi")])
def test_falhas_classicas_dominam_na_frequencia_prevista(manifesto, rid, familia):
    # Registros Y1/Y2 em Smith & Randall (2015, Tab. B2).
    e = _escore(manifesto, rid)
    assert e.idxmax() == familia
    assert e[familia] > 15


def test_features_envelope_por_janela(manifesto):
    reg = manifesto.loc[131]
    janelas = carregar_sinal(reg)[: 4096 * 3].reshape(3, 4096)
    df = features_envelope(janelas, np.full(3, reg["rpm"]), FS_HZ, indice=["a", "b", "c"])
    assert list(df.columns) == NOMES_FEATURES_ENVELOPE
    assert list(df.index) == ["a", "b", "c"]
    assert (df.idxmax(axis=1) == "env_bpfo").all()


def test_validacao_fisica_concorda_com_smith_e_randall():
    r = resumo_validacao(validacao_fisica())
    assert r.loc["IR", "confirmadas"] == 12
    assert r.loc["OR @6", "confirmadas"] == r.loc["OR @6", "smith_m1_Y"]
    assert r["concorda_com_m1"].sum() >= 48  # de 52 gravações de falha


def test_kurtograma_respeita_banda_minima_e_banda_comum(manifesto):
    from src.features import BANDA_MIN_HZ, banda_kurtograma

    x = carregar_sinal(manifesto.loc[105])
    f_baixa, f_alta, sk = banda_kurtograma(x, FS_HZ)
    assert f_alta - f_baixa >= BANDA_MIN_HZ - 1e-6
    assert 0 < f_baixa < f_alta <= 4800
    assert np.isfinite(sk)


def test_prebranqueamento_iguala_a_magnitude_do_espectro(manifesto):
    from src.features import prebranquear

    y = prebranquear(carregar_sinal(manifesto.loc[130])[:8192])
    mag = np.abs(np.fft.rfft(y))[1:-1]
    assert np.allclose(mag, 1.0, atol=1e-6)


def test_prebranqueamento_recupera_bsf_em_222_e_223():
    # Smith & Randall (2015, Tab. B2): 222 e 223 são Y2 pelo método 2.
    v = validacao_fisica(preprocessamento="prebranqueado").set_index("registro")
    assert v.loc[222, "confirmada"] and v.loc[223, "confirmada"]
