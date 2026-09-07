"""Detecção de anomalia one-class, treinada somente com dados normais.

Responsabilidades previstas:
- baseline: Isolation Forest e distância de Mahalanobis;
- comparação: One-Class SVM e autoencoder;
- métricas: ROC, TPR, FPR.

Regra não negociável: o detector não vê nenhum exemplo de falha no treino
(CLAUDE.md, seção 3, item 3).
"""
