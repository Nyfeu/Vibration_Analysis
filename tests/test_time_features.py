import numpy as np
import pytest

from src.time_features import FEATURE_NAMES, time_domain_features


def _senoide(amplitude=2.0, n=1000, ciclos=10):
    t = np.arange(n) / n
    return amplitude * np.sin(2 * np.pi * ciclos * t)


def test_senoide_tem_valores_teoricos():
    a = 2.0
    f = time_domain_features(_senoide(a)[None, :]).iloc[0]
    assert f["rms"] == pytest.approx(a / np.sqrt(2), rel=1e-6)
    assert f["peak"] == pytest.approx(a, rel=1e-6)
    assert f["crest_factor"] == pytest.approx(np.sqrt(2), rel=1e-6)
    assert f["skewness"] == pytest.approx(0.0, abs=1e-9)
    assert f["kurtosis"] == pytest.approx(1.5, rel=1e-6)  # curtose de Pearson


def test_gaussiana_tem_curtose_3_e_assimetria_0():
    rng = np.random.default_rng(0)
    f = time_domain_features(rng.normal(size=(1, 400_000))).iloc[0]
    assert f["kurtosis"] == pytest.approx(3.0, abs=0.05)
    assert f["skewness"] == pytest.approx(0.0, abs=0.02)


def test_impactos_aumentam_a_curtose():
    rng = np.random.default_rng(1)
    ruido = rng.normal(size=(1, 4000))
    com_impactos = ruido.copy()
    com_impactos[0, ::400] += 15.0
    k0 = time_domain_features(ruido).iloc[0]["kurtosis"]
    k1 = time_domain_features(com_impactos).iloc[0]["kurtosis"]
    assert k1 > k0 + 3


def test_formato_colunas_e_ordem_das_linhas():
    w = np.vstack([_senoide(1.0), _senoide(3.0), _senoide(5.0)])
    df = time_domain_features(w, index=["a", "b", "c"])
    assert list(df.columns) == FEATURE_NAMES
    assert list(df.index) == ["a", "b", "c"]
    # a linha i corresponde à janela i (pico cresce com a amplitude)
    assert df["peak"].tolist() == pytest.approx([1.0, 3.0, 5.0], rel=1e-6)


def test_remove_mean_ignora_offset_do_sensor():
    base = _senoide(2.0)[None, :]
    deslocado = base + 7.5
    a = time_domain_features(base).iloc[0]
    b = time_domain_features(deslocado).iloc[0]
    for nome in FEATURE_NAMES:
        assert b[nome] == pytest.approx(a[nome], rel=1e-6, abs=1e-9)
    # sem remover a média, o offset entra no rms
    c = time_domain_features(deslocado, remove_mean=False).iloc[0]
    assert c["rms"] > a["rms"] * 2


def test_janela_constante_nao_quebra():
    df = time_domain_features(np.full((1, 100), 3.0))
    assert df.iloc[0]["rms"] == 0.0
    assert np.isnan(df.iloc[0]["crest_factor"])


def test_entrada_1d_e_index_com_tamanho_errado():
    with pytest.raises(ValueError):
        time_domain_features(np.zeros(100))
    with pytest.raises(ValueError):
        time_domain_features(np.zeros((3, 100)), index=[0, 1])
