# Declaração de uso de IA

> Entregável exigido pelo enunciado (item 6.3, "Referências e declare usos de IA").
>
> Regra do grupo: **nenhuma saída de IA entra no repositório sem revisão humana
> nomeada.** As sessões de trabalho com a ferramenta foram conduzidas por um
> integrante, que pediu, leu e aprovou cada mudança antes do commit; ele consta
> como revisor. Os demais integrantes leram o relatório e a apresentação nas
> partes de que são responsáveis (ver o cabeçalho de cada capítulo em
> `docs/relatorio/secoes/`).

---

## 1. Ferramentas utilizadas

| Ferramenta | Versão / modelo | Usada para |
|---|---|---|
| Claude Code | Claude Opus 5.5 (`claude-opus-5-5`) | Download e verificação dos dados; implementação do código de análise (notebook); depuração; redação de rascunhos do relatório, dos fichamentos e dos slides; infraestrutura do repositório (CI, Pages) |

---

## 2. Registro de uso

| # | Data | Ferramenta | O que foi pedido | O que foi aproveitado | O que foi descartado / corrigido | Revisado por | Onde está no repo |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-06 | Claude Code | Baixar o subconjunto DE/12 kHz do CWRU (issue #3) e conferir taxa de amostragem e nº de arquivos por classe contra a documentação oficial | 56 `.mat` em `data/raw/`; `scripts/download_cwru.py` (download + SHA-256 + manifesto); `data/raw/manifesto.csv`; `data/raw/README.md` com as inconsistências encontradas (normais a 48 kHz, `99.mat` com variáveis de `98.mat`, contradição na posição do defeito OR) | Nenhum descarte; as inconsistências foram conferidas pelo grupo nos próprios arquivos (linha de 120 Hz) | André Maiolini | `data/raw/`, `scripts/download_cwru.py` |
| 2 | 2026-10-06 | Claude Code | Propor um template para os fichamentos de artigos | Estrutura do fichamento (cabeçalho ABNT, convenções de citação, "→ Projeto:", pendências) | O fichamento de Smith & Randall (2015) foi preenchido pelo grupo com o texto completo | André Maiolini | `docs/records/smith2015.md` |
| 3 | 2026-10-06 | Claude Code | Preencher a auditoria de arquivos a partir do fichamento de Smith & Randall (2015), seguindo as decisões do grupo (não excluir registros sem evidência física; OR @6 como posição principal) | Critérios C1–C6, tabela de 20 registros com ressalva, resumo quantitativo; Apêndice B | Nenhum descarte registrado | André Maiolini | `docs/arquivos_excluidos.md`, apêndice B |
| 4 | 2026-10-06 | Claude Code | Refletir a decisão da posição do defeito em pista externa (issue #5) no carregamento e na Tabela 1 | Seleção dos conjuntos principal (40) e de generalização (16) a partir do manifesto | Nenhum descarte registrado | André Maiolini | notebook (seção *Clean Data*), `02-dataset.tex` |
| 5 | 2026-10-06 | Claude Code | Rascunho do capítulo de descrição do dataset | Texto de `02-dataset.tex` a partir de fontes já conferidas | Contagem de janelas deixada para o código; texto revisado pelo grupo | André Maiolini | `docs/relatorio/secoes/02-dataset.tex` |
| 6 | 2026-10-10 | Claude Code | Revisar os módulos de features dos PRs #36 e #37 (escritos por Durval) | Fórmulas conferidas contra o CWRU e Smith & Randall; código reorganizado sem mudança de lógica; convenção de BSF declarada | Identificadores passaram para português; código depois incorporado ao notebook | André Maiolini | notebook (seção *Features*) |
| 7 | 2026-10-10 | Claude Code | Assistência para depuração de bugs e na escrita de código | Correções e implementações aceitas ao longo das sessões | Ver as entradas 8–15, com as correções específicas | André Maiolini | `notebooks/projeto.ipynb` |
| 8 | 2026-10-10 | Claude Code | Implementar leitura, decimação 48→12 kHz, janelas derivadas da FTF e split por carga | Pipeline de dados; verificação espectral da decimação | A verificação revelou resíduo de *aliasing* no filtro padrão do `decimate`; corrigido com a banda comum de 4,8 kHz em todas as gravações | André Maiolini | notebook (*Clean Data*, *Pre-Processing*) |
| 9 | 2026-10-10 | Claude Code | Espectro de envelope, validação física, kurtograma e pré-branqueamento | Escores por família, critério de confirmação, comparação com a Tab. B2 de Smith & Randall | Harmônicos que colidiam dentro da tolerância foram retirados; a "confirmação" do kurtograma na gravação 197 foi reclassificada como frágil | André Maiolini | notebook (*Validação física*) |
| 10 | 2026-10-10 | Claude Code | Detecção one-class, classificação no roteiro das aulas (Pipeline, validação cruzada, GridSearch), CNN 1D, teste entre montagens, precisão/recall e ganho de informação (pedidos do grupo) | Todos os experimentos e artefatos de `results/` | Explicação inicial da FPR do One-Class SVM (atribuída ao RMS) estava errada e foi corrigida (envelope e curtose); números refeitos após o GridSearch | André Maiolini | notebook; `results/` |
| 11 | 2026-10-10 | Claude Code | Análise estatística e exploratória (pedido do grupo) | Kruskal–Wallis por gravação, Spearman, Shapiro–Wilk, limiar qui-quadrado, bootstrap por gravação, teste binomial por montagem, variabilidade entre sementes | A conclusão sobre a generalização foi reescrita com a variabilidade entre sementes (o valor da semente 42 estava no extremo inferior) | André Maiolini | notebook (*Análise exploratória*, *Inferência estatística*) |
| 12 | 2026-10-10 | Claude Code | Redação de rascunhos do relatório: capítulos 1, 3 a 7, resumo, abstract e apêndices | Textos, tabelas e figuras com números lidos de `results/` | Páginas de Smith & Randall corrigidas para a numeração publicada (+99); citações ajustadas à ABNT; referências de memória marcadas para conferência | André Maiolini (texto); responsáveis por capítulo (leitura) | `docs/relatorio/` |
| 13 | 2026-10-10 | Claude Code | Fichamento de cada referência do relatório | 43 fichamentos (todas as referências, exceto Smith & Randall) com ideias principais, uso no projeto e cuidados | Os feitos sem acesso ao texto completo trazem aviso e não têm citação direta nem página | André Maiolini | `docs/records/` |
| 14 | 2026-10-10 | Claude Code | Slides da apresentação (Beamer) e roteiro de fala por integrante | Slides e roteiro (este último só local, fora do Git) | Roteiro ajustado para caber em 5 min após a inclusão de precisão/recall | André Maiolini | `docs/apresentacao/slides.tex` |
| 15 | 2026-10-10 | Claude Code | Infraestrutura: CI do PDF, GitHub Pages, remoção de PDFs com direitos autorais do histórico, consolidação de todo o código no notebook | Workflow, Pages, histórico limpo, notebook único | Deploy travado corrigido (concorrência restrita ao job de deploy) | André Maiolini | `.github/`, `notebooks/` |

---

## 3. O que **não** foi feito com IA

Decisões e trabalho de autoria do grupo:

- **Escolha do dataset** (CWRU) e seu cadastro na disciplina.
- **Configuração do estudo**: sensor DE, taxa de 12 kHz, quatro classes, diâmetros
  como eixo secundário, posição @6 da pista externa, split por carga.
- **Decisões da auditoria**: não excluir registros sem evidência física, mantê-los
  com ressalva e reportar métricas estratificadas.
- **Fichamento de Smith & Randall (2015)**, feito com o texto completo.
- **Módulos iniciais de features** (PRs #36 e #37, de Durval).
- **Direção do trabalho**: pedir o roteiro das aulas (Pipeline, GridSearch), as
  métricas de precisão e recall, o ganho de informação, a ênfase em estatística
  aplicada, a separação entre detectar e diagnosticar, e a concentração do código
  no notebook.
- **Divisão de responsabilidades** pelos capítulos e pelas falas.
- **Gravação e edição do vídeo** da apresentação.

---

## 4. Limites acordados pelo grupo

- Nenhum número de resultado (acurácia, TPR, FPR, AUC, intervalos, valores-*p*)
  foi escrito pela ferramenta: todos saem da execução do notebook deste
  repositório, e cada tabela do relatório indica o arquivo de `results/` de onde
  vem.
- Dados sintéticos são proibidos pelo enunciado (item 3) e não são gerados por
  nenhuma ferramenta.
- Resultado "bom demais" (≥ 98%) é tratado primeiro como suspeita de vazamento ou
  atalho, e investigado antes de ser reportado.
- Fichamentos e referências redigidos sem acesso ao texto completo são marcados
  como tal; nenhuma citação direta ou número de página foi inventado.
- Todo texto produzido com a ferramenta foi lido por um integrante antes do
  commit, e os capítulos têm responsáveis nomeados.
