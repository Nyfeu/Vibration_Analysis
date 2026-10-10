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

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
MANIFESTO = RAIZ / "data" / "raw" / "manifesto.csv"

# Posição do defeito em pista externa, em horas, com a zona de carga em 6 h
# (Smith & Randall, 2015, p. 104). @6 é a única posição com os três diâmetros
# (0.007", 0.014", 0.021") e deixa as classes equilibradas (12 IR, 12 B, 12 OR).
# @3 (ortogonal) e @12 (oposta) mudam a amplitude e a modulação do sinal, por isso
# ficam fora do experimento principal: servem para testar se um modelo treinado
# em @6 generaliza para outra posição. Ver docs/arquivos_excluidos.md (C5).
POSICAO_OR_PRINCIPAL = "6"
POSICOES_OR_GENERALIZACAO = ("3", "12")

CONJUNTOS = ("principal", "generalizacao")


def catalogo(conjunto: str = "principal") -> pd.DataFrame:
    """Registros de um conjunto do experimento, lidos de data/raw/manifesto.csv.

    - ``"principal"``: normais, IR, B e OR na posição ``POSICAO_OR_PRINCIPAL``
      (40 registros).
    - ``"generalizacao"``: só OR nas posições ``POSICOES_OR_GENERALIZACAO``
      (16 registros).

    Nenhum registro é excluído por qualidade; as ressalvas da auditoria estão em
    docs/arquivos_excluidos.md.
    """
    if conjunto not in CONJUNTOS:
        raise ValueError(f"conjunto deve ser um de {CONJUNTOS}, não {conjunto!r}")
    # dtype=str em posicao_or_h: sem isso o pandas lê "6" como 6.0 e o filtro falha.
    m = pd.read_csv(MANIFESTO, dtype={"posicao_or_h": str, "diametro_pol": str})
    eh_or = m["classe"] == "OR"
    if conjunto == "principal":
        sel = ~eh_or | (m["posicao_or_h"] == POSICAO_OR_PRINCIPAL)
    else:
        sel = eh_or & m["posicao_or_h"].isin(POSICOES_OR_GENERALIZACAO)
    return m[sel].reset_index(drop=True)
