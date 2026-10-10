import numpy as np
import pandas as pd
import pytest

from src.data import (
    FS_HZ,
    N_PERIODOS_FTF,
    carregar_sinal,
    catalogo,
    contagem_janelas,
    ler_manifesto,
    montar_janelas,
    segmentar,
    split_por_carga,
    tamanho_janela,
    verificar_sem_vazamento,
)
from src.features import frequencias_caracteristicas


@pytest.fixture(scope="module")
def manifesto():
    return ler_manifesto()


@pytest.fixture(scope="module")
def principal():
    return montar_janelas("principal")


def _registro(manifesto, rid):
    return manifesto[manifesto["id"] == rid].iloc[0]


def test_carrega_todos_os_registros_a_12_khz(manifesto):
    for _, reg in manifesto.iterrows():
        x = carregar_sinal(reg)
        esperado = reg["n_amostras_de"] * FS_HZ / reg["fs_hz"]
        assert len(x) == pytest.approx(esperado, abs=1), reg["arquivo"]
        assert np.isfinite(x).all()


def test_99_le_a_propria_variavel_e_nao_a_do_98(manifesto):
    x98 = carregar_sinal(_registro(manifesto, 98))
    x99 = carregar_sinal(_registro(manifesto, 99))
    n = min(len(x98), len(x99))
    assert not np.allclose(x98[:n], x99[:n])


def test_rpm_nominal_quando_o_arquivo_nao_traz(manifesto):
    assert _registro(manifesto, 98)["rpm"] == 1772
    assert _registro(manifesto, 99)["rpm"] == 1750
    assert _registro(manifesto, 100)["rpm"] == 1725  # medido


@pytest.mark.parametrize("rid", [97, 98, 99, 100])
def test_normal_decimado_tem_a_linha_de_120_hz_no_lugar(manifesto, rid):
    # 120 Hz = 2 x rede de 60 Hz, independe da carga: régua da taxa de
    # amostragem (data/raw/README.md, item 1). Lido a 48 kHz e decimado para
    # 12 kHz, o pico tem de continuar em 120 Hz.
    x = carregar_sinal(_registro(manifesto, rid))
    espectro = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1 / FS_HZ)
    faixa = (f > 110) & (f < 130)
    pico = f[faixa][np.argmax(espectro[faixa])]
    assert pico == pytest.approx(120.0, abs=0.5)


def test_banda_comum_iguala_a_cadeia_de_normais_e_falhas(manifesto):
    # Acima de 4,8 kHz, normais (decimados) e falhas (filtradas) ficam com
    # fração de potência desprezível: nenhum dos dois grupos guarda essa faixa.
    from scipy.signal import welch

    for rid in (97, 100, 130, 198):
        f, p = welch(carregar_sinal(_registro(manifesto, rid)), fs=FS_HZ, nperseg=4096)
        assert p[f > 5200].sum() / p.sum() < 1e-4, rid


def test_tamanho_da_janela_cobre_3_periodos_da_gaiola(manifesto):
    rpm_min = manifesto["rpm"].min()
    n = tamanho_janela(rpm_min)
    ftf = frequencias_caracteristicas(rpm_min).ftf
    assert n == 4096
    assert n & (n - 1) == 0  # potência de 2
    assert n / FS_HZ * ftf >= N_PERIODOS_FTF
    assert n / FS_HZ * (rpm_min / 60) > 9  # várias revoluções do eixo


def test_segmentar():
    w = segmentar(np.arange(10.0), tamanho=4, passo=2)
    assert w.tolist() == [[0, 1, 2, 3], [2, 3, 4, 5], [4, 5, 6, 7], [6, 7, 8, 9]]
    assert segmentar(np.arange(3.0), tamanho=4, passo=2).shape == (0, 4)


def test_meta_alinhada_as_janelas(principal):
    X, meta = principal
    assert len(X) == len(meta)
    assert set(meta["registro"]) == set(catalogo("principal")["id"])


def test_split_sem_registro_em_treino_e_teste(principal):
    _, meta = principal
    treino, teste = split_por_carga(meta)
    assert not (treino & teste).any()
    assert (treino | teste).all()
    assert set(meta.loc[teste, "carga_hp"]) == {3}
    assert set(meta.loc[treino, "registro"]).isdisjoint(meta.loc[teste, "registro"])


def test_verificacao_detecta_vazamento():
    meta = pd.DataFrame({"registro": [105, 105, 106], "carga_hp": [0, 0, 1]})
    with pytest.raises(AssertionError):
        verificar_sem_vazamento(meta.iloc[:2], meta.iloc[1:])


def test_cargas_sobrepostas_sao_rejeitadas(principal):
    _, meta = principal
    with pytest.raises(ValueError):
        split_por_carga(meta, cargas_treino=(0, 1, 3), cargas_teste=(3,))


def test_contagem_bate_com_o_total(principal):
    _, meta = principal
    t = contagem_janelas(meta)
    assert t.loc["total", "total"] == len(meta)
    assert list(t.index) == ["normal", "IR", "B", "OR", "total"]
