"""Carregamento dos arquivos .mat do CWRU, segmentação em janelas e montagem dos splits.

Responsabilidades previstas:
- parser dos arquivos .mat (sinal do drive end, 12 kHz);
- segmentação em janelas cobrindo várias revoluções do eixo (tamanho derivado da
  rotação e da taxa de amostragem, não escolhido por conveniência);
- split por condição de carga (treino: 0/1/2 HP; teste: 3 HP), nunca aleatório em
  nível de janela;
- seeds fixas e declaradas.

Ver CLAUDE.md, seção 3 (regras metodológicas) e seção 4 (pipeline).
"""
