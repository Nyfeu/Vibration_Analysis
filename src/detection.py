"""Detecção de anomalia one-class, treinada somente com dados normais.

- baseline: distância de Mahalanobis e Isolation Forest (issue #15);
- comparação: One-Class SVM e autoencoder (issue #16).

Regra não negociável: o detector não vê nenhum exemplo de falha no treino
(CLAUDE.md, seção 3, item 3). `treinar_detector` verifica isso e falha se o
conjunto de treino tiver qualquer janela que não seja normal.

Todos os detectores devolvem um escore de anomalia em que MAIOR = mais anômalo.
O limiar de alarme é um percentil alto dos escores das próprias janelas normais
de treino (`PERCENTIL_LIMIAR`): é o único dado disponível para calibrá-lo numa
planta real, onde ainda não existem falhas rotuladas.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, OutlierMixin
from sklearn.covariance import EmpiricalCovariance
from sklearn.ensemble import IsolationForest
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM

from src.data import SEED

# Limiar: percentil 99 dos escores normais de treino, isto é, uma taxa de
# falsos positivos de cerca de 1% esperada nos dados de treino.
PERCENTIL_LIMIAR = 99.0

BASELINES = ("mahalanobis", "isolation_forest")
DETECTORES = BASELINES + ("ocsvm", "autoencoder")


class Mahalanobis(OutlierMixin, BaseEstimator):
    """Distância de Mahalanobis à média dos normais (Mahalanobis, 1936).
    `score_samples` segue a convenção do scikit-learn: maior = mais normal."""

    def fit(self, x, y=None):
        self.cov_ = EmpiricalCovariance().fit(x)
        return self

    def score_samples(self, x):
        return -np.sqrt(self.cov_.mahalanobis(x))


class Autoencoder(OutlierMixin, BaseEstimator):
    """Autoencoder raso (Hinton; Salakhutdinov, 2006): MLP treinada para
    reconstruir a própria entrada por um gargalo de 3 neurônios; o escore é o
    erro quadrático médio de reconstrução. Implementado com o MLPRegressor do
    scikit-learn, suficiente para 8 features e sem exigir PyTorch."""

    def fit(self, x, y=None):
        self.mlp_ = MLPRegressor(
            hidden_layer_sizes=(6, 3, 6), activation="tanh", alpha=1e-3,
            max_iter=5000, random_state=SEED,
        ).fit(x, x)
        return self

    def score_samples(self, x):
        return -np.mean((self.mlp_.predict(x) - x) ** 2, axis=1)


def novo_detector(nome: str):
    """Modelo one-class não treinado (último passo do pipeline)."""
    if nome == "mahalanobis":
        return Mahalanobis()
    if nome == "isolation_forest":
        # Liu; Ting; Zhou (2008): menos cortes até isolar = mais anômalo.
        return IsolationForest(n_estimators=300, random_state=SEED)
    if nome == "ocsvm":
        # Schölkopf et al. (2001); nu = fração máxima de normais fora da fronteira.
        return OneClassSVM(kernel="rbf", gamma="scale", nu=0.05)
    if nome == "autoencoder":
        return Autoencoder()
    raise ValueError(f"detector desconhecido: {nome}")


@dataclass
class Detector:
    """Pipeline treinado (scaler + modelo one-class) e limiar de alarme."""

    nome: str
    features: list[str]
    pipeline: Pipeline
    limiar: float

    def escore(self, f: pd.DataFrame) -> np.ndarray:
        """Escore de anomalia: maior = mais anômalo."""
        return -self.pipeline.score_samples(f[self.features])

    def alarme(self, f: pd.DataFrame) -> np.ndarray:
        return self.escore(f) > self.limiar


def treinar_detector(
    nome: str, f_treino: pd.DataFrame, classes_treino, features: list[str]
) -> Detector:
    """Treina um detector one-class. Falha se houver janela não normal no treino.

    O pipeline padroniza as features com o StandardScaler ajustado só nos
    normais de treino.
    """
    classes = pd.Series(np.asarray(classes_treino))
    if len(classes) != len(f_treino):
        raise ValueError("classes_treino e f_treino têm tamanhos diferentes")
    if not (classes == "normal").all():
        outras = sorted(set(classes) - {"normal"})
        raise ValueError(f"treino one-class com classes não normais: {outras}")

    x = f_treino[list(features)]
    pipe = Pipeline([("scaler", StandardScaler()), ("modelo", novo_detector(nome))]).fit(x)
    det = Detector(nome, list(features), pipe, np.nan)
    det.limiar = float(np.percentile(det.escore(f_treino), PERCENTIL_LIMIAR))
    return det
