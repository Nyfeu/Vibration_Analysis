"""Classificação supervisionada do tipo de falha (normal, IR, B, OR).

Etapa separada e posterior à detecção (CLAUDE.md, seção 4). Treino com as
cargas de 0, 1 e 2 HP e teste com 3 HP, pelo mesmo split da detecção.

- Random Forest (Breiman, 2001): classificador principal; dá a importância de
  cada feature, para verificar se a decisão tem sentido físico;
- SVM com kernel RBF (Cortes; Vapnik, 1995): contraponto.

As classes são balanceadas por peso (`class_weight="balanced"`): há 144
janelas normais no treino contra cerca de 520 de cada falha.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.data import ORDEM_CLASSES, SEED

CLASSIFICADORES = ("random_forest", "svm")


def novo_classificador(nome: str):
    """Classificador não treinado. A padronização faz parte do pipeline, logo é
    estimada só com o treino."""
    if nome == "random_forest":
        return RandomForestClassifier(
            n_estimators=500, class_weight="balanced", random_state=SEED, n_jobs=-1
        )
    if nome == "svm":
        return make_pipeline(
            StandardScaler(), SVC(kernel="rbf", C=10.0, gamma="scale", class_weight="balanced")
        )
    raise ValueError(f"classificador desconhecido: {nome}")


def acuracia_por_classe(y_true, y_pred, classes=ORDEM_CLASSES) -> pd.Series:
    """Fração de acertos dentro de cada classe verdadeira (recall por classe)."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    return pd.Series(
        {c: (y_pred[y_true == c] == c).mean() if (y_true == c).any() else np.nan for c in classes}
    )


def matriz_confusao(y_true, y_pred, classes=ORDEM_CLASSES) -> pd.DataFrame:
    """Matriz completa, com todas as classes nas linhas (verdadeira) e colunas
    (predita), mesmo as que não aparecem nas previsões."""
    m = pd.crosstab(
        pd.Categorical(y_true, categories=classes),
        pd.Categorical(y_pred, categories=classes),
        dropna=False,
    )
    m.index.name, m.columns.name = "verdadeira", "predita"
    return m


def erros_classificacao(meta: pd.DataFrame, y_pred) -> pd.DataFrame:
    """Janelas classificadas errado, com carga, classe verdadeira, predita e
    severidade (CLAUDE.md, regra 8)."""
    y_pred = np.asarray(y_pred)
    errou = meta["classe"].to_numpy() != y_pred
    e = meta.loc[errou, ["registro", "janela", "classe", "diametro_pol", "posicao_or_h", "carga_hp"]].copy()
    e = e.rename(columns={"classe": "verdadeira"})
    e["predita"] = y_pred[errou]
    return e
