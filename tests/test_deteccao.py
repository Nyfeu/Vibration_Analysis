import numpy as np
import pandas as pd
import pytest

from src.detection import DETECTORES, PERCENTIL_LIMIAR, treinar_detector
from src.evaluation import erros_deteccao, metricas_deteccao
from src.features import CONJUNTOS_FEATURES


def _features(n, deslocamento=0.0, seed=0):
    # Matriz de teste para o contrato dos detectores (não é dado do projeto).
    rng = np.random.default_rng(seed)
    cols = CONJUNTOS_FEATURES["tempo+envelope"]
    return pd.DataFrame(rng.normal(deslocamento, 1.0, (n, len(cols))), columns=cols)


def test_treino_one_class_recusa_janela_de_falha():
    f = _features(10)
    classes = ["normal"] * 9 + ["IR"]
    with pytest.raises(ValueError, match="não normais"):
        treinar_detector("mahalanobis", f, classes, list(f.columns))


@pytest.mark.parametrize("nome", DETECTORES)
def test_detector_da_escore_maior_ao_que_foge_do_normal(nome):
    f = _features(200)
    det = treinar_detector(nome, f, ["normal"] * 200, list(f.columns))
    longe = _features(50, deslocamento=6.0, seed=1)
    assert np.median(det.escore(longe)) > np.median(det.escore(_features(50, seed=2)))
    # limiar calibrado nos normais de treino: ~1% de alarmes neles
    assert det.alarme(f).mean() <= 1 - PERCENTIL_LIMIAR / 100 + 0.01


def test_metricas_deteccao():
    m = metricas_deteccao([1, 1, 0, 0], [0.9, 0.2, 0.1, 0.8], [True, False, False, True])
    assert m["auc"] == pytest.approx(0.75)
    assert m["tpr"] == 0.5 and m["fpr"] == 0.5
    assert m["precisao"] == 0.5 and m["prevalencia"] == 0.5


def test_detector_que_sempre_alarma_tem_precisao_igual_a_prevalencia():
    eh_falha = [1] * 9 + [0]
    m = metricas_deteccao(eh_falha, [1.0] * 10, [True] * 10)
    assert m["tpr"] == 1.0 and m["precisao"] == pytest.approx(m["prevalencia"]) == pytest.approx(0.9)


def test_erros_guardam_fn_e_fp_com_metadados():
    meta = pd.DataFrame(
        {
            "registro": [100, 108, 108],
            "janela": [0, 0, 1],
            "classe": ["normal", "IR", "IR"],
            "diametro_pol": [None, "0.007", "0.007"],
            "posicao_or_h": [None, None, None],
            "carga_hp": [3, 3, 3],
        }
    )
    e = erros_deteccao(meta, [5.0, 0.1, 9.0], [True, False, True], limiar=1.0)
    assert list(e["tipo_erro"]) == ["FP", "FN"]
    assert {"carga_hp", "classe", "diametro_pol", "predito", "escore"} <= set(e.columns)
