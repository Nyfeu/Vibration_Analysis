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
from sklearn.covariance import EmpiricalCovariance
from sklearn.ensemble import IsolationForest
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM

from src.data import SEED

# Limiar: percentil 99 dos escores normais de treino, isto é, uma taxa de
# falsos positivos de cerca de 1% esperada nos dados de treino.
PERCENTIL_LIMIAR = 99.0

BASELINES = ("mahalanobis", "isolation_forest")
DETECTORES = BASELINES + ("ocsvm", "autoencoder")


class _Mahalanobis:
    """Distância de Mahalanobis à média dos normais (Mahalanobis, 1936)."""

    def fit(self, x):
        self.cov_ = EmpiricalCovariance().fit(x)
        return self

    def score(self, x):
        return np.sqrt(self.cov_.mahalanobis(x))


class _IsolationForest:
    """Isolation Forest (Liu; Ting; Zhou, 2008): menos cortes = mais anômalo."""

    def fit(self, x):
        self.m_ = IsolationForest(n_estimators=300, random_state=SEED).fit(x)
        return self

    def score(self, x):
        return -self.m_.score_samples(x)


class _OCSVM:
    """One-Class SVM com kernel RBF (Schölkopf et al., 2001).

    nu = 0,05: fração máxima de normais de treino fora da fronteira.
    """

    def fit(self, x):
        self.m_ = OneClassSVM(kernel="rbf", gamma="scale", nu=0.05).fit(x)
        return self

    def score(self, x):
        return -self.m_.score_samples(x)


class _Autoencoder:
    """Autoencoder raso (Hinton; Salakhutdinov, 2006): MLP treinada para
    reconstruir a própria entrada por um gargalo de 3 neurônios; o escore é o
    erro quadrático médio de reconstrução. Implementado com o MLPRegressor do
    scikit-learn, suficiente para 8 features e sem exigir PyTorch no Colab.
    """

    def fit(self, x):
        self.m_ = MLPRegressor(
            hidden_layer_sizes=(6, 3, 6),
            activation="tanh",
            alpha=1e-3,
            max_iter=5000,
            random_state=SEED,
        ).fit(x, x)
        return self

    def score(self, x):
        return np.mean((self.m_.predict(x) - x) ** 2, axis=1)


_FABRICA = {
    "mahalanobis": _Mahalanobis,
    "isolation_forest": _IsolationForest,
    "ocsvm": _OCSVM,
    "autoencoder": _Autoencoder,
}


@dataclass
class Detector:
    """Detector treinado: padronização + modelo + limiar de alarme."""

    nome: str
    features: list[str]
    escalador: StandardScaler
    modelo: object
    limiar: float

    def escore(self, f: pd.DataFrame) -> np.ndarray:
        return self.modelo.score(self.escalador.transform(f[self.features].to_numpy()))

    def alarme(self, f: pd.DataFrame) -> np.ndarray:
        return self.escore(f) > self.limiar


def treinar_detector(
    nome: str, f_treino: pd.DataFrame, classes_treino, features: list[str]
) -> Detector:
    """Treina um detector one-class. Falha se houver janela não normal no treino.

    A padronização (média e desvio) também é estimada só com os normais.
    """
    classes = pd.Series(np.asarray(classes_treino))
    if len(classes) != len(f_treino):
        raise ValueError("classes_treino e f_treino têm tamanhos diferentes")
    if not (classes == "normal").all():
        outras = sorted(set(classes) - {"normal"})
        raise ValueError(f"treino one-class com classes não normais: {outras}")

    x = f_treino[features].to_numpy()
    esc = StandardScaler().fit(x)
    modelo = _FABRICA[nome]().fit(esc.transform(x))
    limiar = float(np.percentile(modelo.score(esc.transform(x)), PERCENTIL_LIMIAR))
    return Detector(nome, list(features), esc, modelo, limiar)
