# Declaração de uso de IA

> Entregável exigido pelo enunciado (item 6.3, "Referências e declare usos de IA").
>
> **Como preencher:** toda contribuição de ferramenta de IA que entrar no
> repositório vira uma linha na tabela abaixo. Registre no mesmo commit da
> mudança. Nada de preencher tudo na véspera da entrega.
>
> Regra do grupo: **nenhuma saída de IA entra no repositório sem revisão humana
> nomeada.** A coluna "Revisado por" não pode ficar vazia.

---

## 1. Ferramentas utilizadas

| Ferramenta | Versão / modelo | Usada para |
|---|---|---|
| Claude Code | Claude Opus 5.5 (`claude-opus-5-5`) | Download e verificação dos dados, scripts, documentação |

---

## 2. Registro de uso

| # | Data | Ferramenta | O que foi pedido | O que foi aproveitado | O que foi descartado / corrigido | Revisado por | Onde está no repo |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-06 | Claude Code | Baixar o subconjunto DE/12 kHz do CWRU (issue #3) e conferir taxa de amostragem e nº de arquivos por classe contra a documentação oficial | 56 `.mat` em `data/raw/`; `scripts/download_cwru.py` (download + SHA-256 + manifesto); `data/raw/manifesto.csv`; `data/raw/README.md` com as inconsistências encontradas (normais a 48 kHz, `99.mat` com variáveis de `98.mat`, contradição na posição do defeito OR) | _a preencher pelo grupo_ | _pendente_ | `data/raw/`, `scripts/download_cwru.py`, `README.md` |

---

## 3. O que **não** foi feito com IA

> Liste explicitamente as partes de autoria integral do grupo — escolha do dataset,
> decisões metodológicas, interpretação dos resultados, discussão crítica.

- _preencher_

---

## 4. Limites acordados pelo grupo

> Ex.: IA não é usada para gerar dados, para produzir números de resultado, nem para
> redigir a discussão crítica sem revisão. Ajuste conforme a decisão do grupo.

- Nenhum número de métrica (acurácia, TPR, FPR) vem de IA: todos saem de execução
  real do código deste repositório.
- Dados sintéticos são proibidos pelo enunciado (item 3) e não são gerados por
  nenhuma ferramenta.
- _preencher o restante_
