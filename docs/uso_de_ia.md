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
| Claude Code | Claude Opus 5.5 (`claude-opus-5-5`) | Download e verificação dos dados, scripts, documentação, depuração de bugs e escrita de código |

---

## 2. Registro de uso

| # | Data | Ferramenta | O que foi pedido | O que foi aproveitado | O que foi descartado / corrigido | Revisado por | Onde está no repo |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-06 | Claude Code | Baixar o subconjunto DE/12 kHz do CWRU (issue #3) e conferir taxa de amostragem e nº de arquivos por classe contra a documentação oficial | 56 `.mat` em `data/raw/`; `scripts/download_cwru.py` (download + SHA-256 + manifesto); `data/raw/manifesto.csv`; `data/raw/README.md` com as inconsistências encontradas (normais a 48 kHz, `99.mat` com variáveis de `98.mat`, contradição na posição do defeito OR) | _a preencher pelo grupo_ | _pendente_ | `data/raw/`, `scripts/download_cwru.py`, `README.md` |
| 2 | 2026-10-06 | Claude Code | Propor um template (estrutura) para os fichamentos de artigos | Estrutura do fichamento: cabeçalho com referência ABNT, chave `.bib`, arquivo, autor, revisor e motivo da leitura; convenções (citação direta com página e "tradução nossa", paráfrase, marcador "→ Projeto:" para implicações); seções "Resumo em cinco pontos", "Implicações para o projeto", "Pendências e dúvidas para o grupo" e "Referências do artigo a seguir" | _a preencher pelo grupo_ | _pendente_ | `docs/records/smith2015.md` |
| 3 | 2026-10-06 | Claude Code | Preencher a auditoria de arquivos a partir do fichamento de Smith & Randall (2015), seguindo a decisão do grupo (marcar e não excluir os registros sem evidência física; OR @6 como posição principal) | Critérios C1–C6, tabela de excluídos (nenhum por qualidade; @3/@12 como conjunto de generalização), tabela de 20 registros com ressalva, resumo quantitativo e composição do conjunto de teste; Apêndice B do relatório; posição OR declarada em `02-dataset.tex` | _a preencher pelo grupo_ | _pendente_ | `docs/arquivos_excluidos.md`, `docs/relatorio/secoes/apendice-b-arquivos-excluidos.tex`, `docs/relatorio/secoes/02-dataset.tex` |
| 4 | 2026-10-06 | Claude Code | Refletir a decisão da posição do defeito em pista externa (issue #5) no carregamento e na Tabela 1 do relatório | `src/data.py`: constantes `POSICAO_OR_PRINCIPAL` (@6) e `POSICOES_OR_GENERALIZACAO` (@3, @12) e função `catalogo()`, que seleciona os registros dos conjuntos principal (40) e de generalização (16) a partir do manifesto; linha de @3/@12 na Tabela 1 de `02-dataset.tex` | _a preencher pelo grupo_ | _pendente_ | `src/data.py`, `docs/relatorio/secoes/02-dataset.tex` |
| 5 | 2026-10-06 | Claude Code | Ajudar a redigir o capítulo de descrição do dataset | Rascunho completo de `02-dataset.tex` (origem e setup, justificativa da configuração, registros utilizados, taxa de 48 kHz dos normais, gravações e duração por classe, resumo da auditoria), a partir de fontes já conferidas; data de acesso do CWRU no `.bib`. Contagem de janelas mantida como `TODO(grupo)` | _a preencher pelo grupo_ | _pendente_ | `docs/relatorio/secoes/02-dataset.tex`, `docs/relatorio/referencias.bib` |
| 6 | 2026-10-10 | Claude Code | Revisar os módulos de features dos PRs #36 e #37 e alinhá-los à estrutura de pastas planejada pelo grupo e à referência bibliográfica | Revisão (fórmulas conferidas contra o CWRU e Smith & Randall, testes de casos-limite); código de `src/bearing_frequencies.py` e `src/time_features.py` movido sem mudança de lógica para `src/features.py`; convenção de BSF (Smith & Randall) declarada nos comentários do código; imports dos testes atualizados | _a preencher pelo grupo_ | _pendente_ | `src/features.py` e `tests/` (código depois incorporado ao notebook) |
| 7 | 2026-10-10 | Claude Code | Assistência para depuração de bugs e assistência na escrita de código | _a preencher pelo grupo_ | _a preencher pelo grupo_ | _pendente_ | `src/`, `scripts/`, `tests/`, `notebooks/projeto.ipynb` |

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
