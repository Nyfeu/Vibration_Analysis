import numpy as np
import pytest

from src.features import NOMES_FEATURES_TEMPO, features_tempo


def _senoide(amplitude=2.0, n=1000, ciclos=10):
    t = np.arange(n) / n
    return amplitude * np.sin(2 * np.pi * ciclos * t)


def test_senoide_tem_valores_teoricos():
    a = 2.0
    f = features_tempo(_senoide(a)[None, :]).iloc[0]
    assert f["rms"] == pytest.approx(a / np.sqrt(2), rel=1e-6)
    assert f["pico"] == pytest.approx(a, rel=1e-6)
    assert f["fator_crista"] == pytest.approx(np.sqrt(2), rel=1e-6)
    assert f["assimetria"] == pytest.approx(0.0, abs=1e-9)
    assert f["curtose"] == pytest.approx(1.5, rel=1e-6)  # curtose de Pearson


def test_gaussiana_tem_curtose_3_e_assimetria_0():
    rng = np.random.default_rng(0)
    f = features_tempo(rng.normal(size=(1, 400_000))).iloc[0]
    assert f["curtose"] == pytest.approx(3.0, abs=0.05)
    assert f["assimetria"] == pytest.approx(0.0, abs=0.02)


def test_impactos_aumentam_a_curtose():
    rng = np.random.default_rng(1)
    ruido = rng.normal(size=(1, 4000))
    com_impactos = ruido.copy()
    com_impactos[0, ::400] += 15.0
    k0 = features_tempo(ruido).iloc[0]["curtose"]
    k1 = features_tempo(com_impactos).iloc[0]["curtose"]
    assert k1 > k0 + 3


def test_formato_colunas_e_ordem_das_linhas():
    w = np.vstack([_senoide(1.0), _senoide(3.0), _senoide(5.0)])
    df = features_tempo(w, indice=["a", "b", "c"])
    assert list(df.columns) == NOMES_FEATURES_TEMPO
    assert list(df.index) == ["a", "b", "c"]
    # a linha i corresponde à janela i (pico cresce com a amplitude)
    assert df["pico"].tolist() == pytest.approx([1.0, 3.0, 5.0], rel=1e-6)


def test_remover_media_ignora_offset_do_sensor():
    base = _senoide(2.0)[None, :]
    deslocado = base + 7.5
    a = features_tempo(base).iloc[0]
    b = features_tempo(deslocado).iloc[0]
    for nome in NOMES_FEATURES_TEMPO:
        assert b[nome] == pytest.approx(a[nome], rel=1e-6, abs=1e-9)
    # sem remover a média, o offset entra no rms
    c = features_tempo(deslocado, remover_media=False).iloc[0]
    assert c["rms"] > a["rms"] * 2


def test_janela_constante_nao_quebra():
    df = features_tempo(np.full((1, 100), 3.0))
    assert df.iloc[0]["rms"] == 0.0
    assert np.isnan(df.iloc[0]["fator_crista"])


def test_entrada_1d_e_indice_com_tamanho_errado():
    with pytest.raises(ValueError):
        features_tempo(np.zeros(100))
    with pytest.raises(ValueError):
        features_tempo(np.zeros((3, 100)), indice=[0, 1])
