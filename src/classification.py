"""Classificação supervisionada do tipo de falha (normal, IR, B, OR).

Etapa separada e posterior à detecção (CLAUDE.md, seção 4). Segue o roteiro
das aulas: pipeline (scaler + classificador), seleção de modelos por validação
cruzada no treino, ajuste de hiperparâmetros por GridSearchCV, e avaliação do
melhor modelo no teste com classification_report e matriz de confusão.

Validação cruzada: LeaveOneGroupOut com o grupo = carga. Cada fold deixa uma
carga inteira de fora (0, 1 ou 2 HP), a mesma lógica do teste em 3 HP. Um
StratifiedKFold embaralhado espalharia janelas da mesma gravação entre treino
e validação e mediria memorização da gravação, não generalização
(`cv_embaralhado` existe só para mostrar esse vazamento).

Modelos candidatos (os das aulas, mais SVM):
- Regressão Logística, KNN (k=3 e k=9), Random Forest (Breiman, 2001) e
  SVM com kernel RBF (Cortes; Vapnik, 1995).
Todos com `class_weight="balanced"` quando disponível: o treino tem 144
janelas normais contra cerca de 520 de cada falha.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    GridSearchCV,
    LeaveOneGroupOut,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.data import ORDEM_CLASSES, SEED


def pipeline(classificador) -> Pipeline:
    """Scaler + classificador. O StandardScaler é ajustado só no treino de cada
    fold, dentro do pipeline, o que evita vazamento da padronização."""
    return Pipeline([("scaler", StandardScaler()), ("clf", classificador)])


def modelos_candidatos() -> dict[str, Pipeline]:
    """Os modelos comparados na seleção, com hiperparâmetros padrão."""
    return {
        "Regressão Logística": pipeline(
            LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED)
        ),
        "KNN (k=3)": pipeline(KNeighborsClassifier(n_neighbors=3)),
        "KNN (k=9)": pipeline(KNeighborsClassifier(n_neighbors=9)),
        "Random Forest": pipeline(
            RandomForestClassifier(class_weight="balanced", random_state=SEED, n_jobs=-1)
        ),
        "SVM (RBF)": pipeline(SVC(kernel="rbf", class_weight="balanced", random_state=SEED)),
    }


# Grades do GridSearchCV para os dois modelos estudados em detalhe.
GRADES = {
    "Random Forest": {
        "clf__n_estimators": [100, 300, 500],
        "clf__max_depth": [None, 5, 10],
        "clf__min_samples_leaf": [1, 5],
    },
    "SVM (RBF)": {
        "clf__C": [0.1, 1, 10, 100],
        "clf__gamma": ["scale", 0.01, 0.1, 1],
    },
}


def cv_por_carga() -> LeaveOneGroupOut:
    """Validação cruzada que deixa uma carga de fora por fold."""
    return LeaveOneGroupOut()


def cv_embaralhado() -> StratifiedKFold:
    """Validação INCORRETA para este problema (janelas embaralhadas): usada só
    para quantificar o vazamento na discussão."""
    return StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)


def selecionar_modelos(x: pd.DataFrame, y, cargas) -> pd.DataFrame:
    """Acurácia média de cada candidato na validação cruzada do treino.

    Calcula as duas validações: por carga (a correta) e embaralhada (a que
    vaza), para comparar.
    """
    linhas = []
    for nome, modelo in modelos_candidatos().items():
        por_carga = cross_val_score(modelo, x, y, groups=cargas, cv=cv_por_carga(), scoring="accuracy")
        embaralhado = cross_val_score(modelo, x, y, cv=cv_embaralhado(), scoring="accuracy")
        linhas.append(
            {
                "modelo": nome,
                "cv_por_carga": por_carga.mean(),
                "cv_por_carga_desvio": por_carga.std(),
                "cv_embaralhado": embaralhado.mean(),
            }
        )
    return pd.DataFrame(linhas).sort_values("cv_por_carga", ascending=False).reset_index(drop=True)


def ajustar_hiperparametros(nome: str, x: pd.DataFrame, y, cargas) -> GridSearchCV:
    """GridSearchCV do modelo `nome` sobre sua grade, com CV por carga. O
    melhor pipeline é reajustado com todo o treino (refit)."""
    busca = GridSearchCV(
        modelos_candidatos()[nome],
        GRADES[nome],
        cv=cv_por_carga(),
        scoring="accuracy",
        n_jobs=-1,
        refit=True,
    )
    return busca.fit(x, y, groups=cargas)


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
