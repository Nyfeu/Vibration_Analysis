import pytest

from src.bearing_frequencies import (
    SKF_6205_DE,
    characteristic_frequencies,
    tolerance_band,
)

RPM_1HZ = 60.0  # f_r = 1 Hz: as frequências saem como múltiplos de f_r


def test_multiplos_de_fr_conferem_com_smith_e_randall_tabela_2():
    f = characteristic_frequencies(RPM_1HZ)
    assert f.bpfi == pytest.approx(5.415, rel=5e-4)
    assert f.bpfo == pytest.approx(3.585, rel=5e-4)
    assert f.ftf == pytest.approx(0.3983, rel=5e-4)
    assert f.bsf == pytest.approx(2.357, rel=5e-4)


def test_multiplos_de_fr_conferem_com_pagina_do_cwru():
    # CWRU "Bearing Specifications", drive end: 5.4152 / 3.5848 / 0.39828 / 4.7135
    f = characteristic_frequencies(RPM_1HZ)
    assert f.bpfi == pytest.approx(5.4152, rel=1e-4)
    assert f.bpfo == pytest.approx(3.5848, rel=1e-4)
    assert f.ftf == pytest.approx(0.39828, rel=2e-4)
    assert f.bsf_2x == pytest.approx(4.7135, rel=1e-4)  # "Rolling Element" do CWRU


def test_exemplo_1797_rpm_do_fichamento():
    f = characteristic_frequencies(1797)
    assert f.bpfi == pytest.approx(162.2, abs=0.1)
    assert f.bpfo == pytest.approx(107.4, abs=0.1)
    assert f.bsf == pytest.approx(70.6, abs=0.1)
    assert f.ftf == pytest.approx(11.9, abs=0.1)


@pytest.mark.parametrize("rpm", [1797, 1772, 1750, 1730])
def test_identidades_independem_da_rotacao(rpm):
    f = characteristic_frequencies(rpm)
    f_r = rpm / 60.0
    n = SKF_6205_DE.n_balls
    assert f.bpfo + f.bpfi == pytest.approx(n * f_r)  # Smith & Randall, p. 10
    assert f.bpfo == pytest.approx(n * f.ftf)


@pytest.mark.parametrize("rpm", [0, -10])
def test_rpm_invalida(rpm):
    with pytest.raises(ValueError):
        characteristic_frequencies(rpm)


def test_tolerance_band():
    low, high = tolerance_band(100.0)
    assert (low, high) == pytest.approx((98.0, 102.0))
