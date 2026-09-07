"""Classificação supervisionada do tipo de falha (normal, IR, OR, B).

Responsabilidades previstas:
- baseline: Random Forest ou SVM sobre as features extraídas;
- contraponto (se houver tempo): CNN 1D sobre o sinal bruto;
- severidade (0.007" / 0.014" / 0.021") como análise secundária.

Etapa posterior e separada da detecção. Ver CLAUDE.md, seção 4.4.
"""
