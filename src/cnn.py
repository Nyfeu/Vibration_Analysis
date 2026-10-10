"""CNN 1D sobre o sinal bruto das janelas, como contraponto às features (issue #21).

Arquitetura no estilo WDCNN (Zhang et al., 2017): a primeira convolução tem
kernel largo (64 amostras, passo 16), que funciona como um banco de filtros
aprendido sobre o sinal cru; as camadas seguintes são convoluções pequenas com
pooling. É o tipo de rede usado em diagnóstico de rolamentos a partir do sinal
bruto (Ince et al., 2016; Zhang et al., 2017).

Duas variantes de entrada, para manter a ablação de amplitude dos demais
experimentos:
- "bruto": a janela como lida (a rede vê a amplitude absoluta);
- "normalizado": cada janela com média 0 e desvio 1 (a rede só vê a forma).

PyTorch é opcional no projeto: este módulo só o importa quando chamado.
"""

from __future__ import annotations

import numpy as np

from src.data import ORDEM_CLASSES, SEED

ENTRADAS = ("bruto", "normalizado")
EPOCAS = 30
LOTE = 64
TAXA_APRENDIZADO = 1e-3


def _preparar(janelas: np.ndarray, entrada: str) -> np.ndarray:
    x = np.asarray(janelas, dtype=np.float32)
    if entrada == "normalizado":
        x = (x - x.mean(axis=1, keepdims=True)) / (x.std(axis=1, keepdims=True) + 1e-8)
    elif entrada != "bruto":
        raise ValueError(f"entrada desconhecida: {entrada}")
    return x[:, None, :]


def _rede(n_classes: int):
    import torch.nn as nn

    def bloco(c_in, c_out, k, s=1):
        return [nn.Conv1d(c_in, c_out, k, stride=s, padding=k // 2), nn.BatchNorm1d(c_out), nn.ReLU(), nn.MaxPool1d(2)]

    return nn.Sequential(
        *bloco(1, 16, 64, 16),  # 4096 -> 256 -> 128
        *bloco(16, 32, 3),  # -> 64
        *bloco(32, 64, 3),  # -> 32
        *bloco(64, 64, 3),  # -> 16
        nn.AdaptiveAvgPool1d(1),
        nn.Flatten(),
        nn.Dropout(0.3),
        nn.Linear(64, n_classes),
    )


class ClassificadorCNN:
    """Interface tipo scikit-learn (fit/predict) para a CNN 1D."""

    def __init__(self, entrada: str = "bruto", epocas: int = EPOCAS, seed: int = SEED):
        self.entrada = entrada
        self.epocas = epocas
        self.seed = seed
        self.classes_ = list(ORDEM_CLASSES)

    def fit(self, janelas: np.ndarray, y) -> "ClassificadorCNN":
        import torch

        torch.manual_seed(self.seed)
        torch.use_deterministic_algorithms(True, warn_only=True)
        rng = np.random.default_rng(self.seed)

        x = torch.from_numpy(_preparar(janelas, self.entrada))
        idx = {c: i for i, c in enumerate(self.classes_)}
        yi = torch.tensor([idx[c] for c in np.asarray(y)])
        # Pesos inversos à frequência: o treino tem 144 normais contra ~520 por falha.
        contagem = torch.bincount(yi, minlength=len(self.classes_)).float()
        pesos = contagem.sum() / (len(self.classes_) * contagem.clamp(min=1))

        self.modelo_ = _rede(len(self.classes_))
        otim = torch.optim.Adam(self.modelo_.parameters(), lr=TAXA_APRENDIZADO)
        perda = torch.nn.CrossEntropyLoss(weight=pesos)
        self.modelo_.train()
        for _ in range(self.epocas):
            ordem = rng.permutation(len(x))
            for i in range(0, len(x), LOTE):
                lote = ordem[i : i + LOTE]
                otim.zero_grad()
                perda(self.modelo_(x[lote]), yi[lote]).backward()
                otim.step()
        return self

    def predict(self, janelas: np.ndarray) -> np.ndarray:
        import torch

        self.modelo_.eval()
        x = torch.from_numpy(_preparar(janelas, self.entrada))
        with torch.no_grad():
            saida = torch.cat([self.modelo_(x[i : i + 256]) for i in range(0, len(x), 256)])
        return np.asarray(self.classes_)[saida.argmax(dim=1).numpy()]
