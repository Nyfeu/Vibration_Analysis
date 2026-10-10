import numpy as np
import pandas as pd
import pytest

from src.classification import (
    GRADES,
    cv_por_carga,
    matriz_confusao,
    modelos_candidatos,
    selecionar_modelos,
)
from src.data import ORDEM_CLASSES, montar_janelas, split_por_carga


def test_cv_por_carga_nunca_mistura_cargas():
    cargas = np.repeat([0, 1, 2], 10)
    for tr, va in cv_por_carga().split(np.zeros(30), groups=cargas):
        assert set(cargas[tr]).isdisjoint(cargas[va])
        assert len(set(cargas[va])) == 1


def test_todo_candidato_e_pipeline_com_scaler():
    for nome, modelo in modelos_candidatos().items():
        assert modelo.steps[0][0] == "scaler", nome
    assert set(GRADES) <= set(modelos_candidatos())


def test_matriz_confusao_tem_todas_as_classes():
    m = matriz_confusao(["IR", "IR"], ["IR", "B"])
    assert list(m.index) == ORDEM_CLASSES and list(m.columns) == ORDEM_CLASSES
    assert m.values.sum() == 2


def test_selecao_de_modelos_roda_no_treino_real():
    from src.features import CONJUNTOS_FEATURES, features_tempo

    X, meta = montar_janelas()
    tr, _ = split_por_carga(meta)
    f = features_tempo(X[tr])
    sel = selecionar_modelos(f, meta.loc[tr, "classe"], meta.loc[tr, "carga_hp"])
    assert len(sel) == len(modelos_candidatos())
    assert sel["cv_por_carga"].between(0, 1).all()
    assert sel["cv_por_carga"].is_monotonic_decreasing


def test_cnn_treina_e_preve_todas_as_classes():
    pytest.importorskip("torch")
    from src.cnn import ClassificadorCNN

    X, meta = montar_janelas()
    idx = meta.groupby("classe").head(8).index
    clf = ClassificadorCNN("normalizado", epocas=1).fit(X[idx], meta.loc[idx, "classe"])
    p = clf.predict(X[idx])
    assert len(p) == len(idx) and set(p) <= set(ORDEM_CLASSES)
