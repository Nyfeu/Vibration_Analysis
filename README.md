# Detecção e Diagnóstico de Anomalias em Sinais de Vibração

Projeto Desafio do 2º semestre — ECM514 Ciência de Dados.
Detecção de anomalias e diagnóstico do tipo de falha em rolamentos, sobre o dataset
público **CWRU (Case Western Reserve University)**.

**Status:** pipeline completo (dados, features, validação física, detecção e
classificação); relatório em revisão pelo grupo.

## Grupo

| Nome | RA |
|---|---|
| André Solano F. R. Maiolini | 19.02012-0 |
| Durval Consorti Soranz de Barros Santos | 22.01097-0 |
| Leonardo Roberto Amadio | 22.01300-8 |
| Lucas Castanho Paganotto Carvalho | 22.00921-3 |
| Estevan Delazari Feher | 21.00586-9 |

---

## Sumário das entregas

> Exigido pelo enunciado (item 6.5). Preencher conforme as entregas ficarem prontas.

| Entrega | Onde |
|---|---|
| Notebook executável no Colab | [`notebooks/projeto.ipynb`](notebooks/projeto.ipynb) · [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Nyfeu/Vibration_Analysis/blob/main/notebooks/projeto.ipynb) |
| Dados empregados | [`data/raw/`](data/raw/) |
| Relatório técnico (LaTeX/ABNT) | fonte em [`docs/relatorio/`](docs/relatorio/) · PDF: [https://nyfeu.github.io/Vibration_Analysis/](https://nyfeu.github.io/Vibration_Analysis/) |
| Apresentação (vídeo, máx. 5 min) | _TODO: link do YouTube_ |
| Slides | fonte em [`docs/apresentacao/slides.tex`](docs/apresentacao/slides.tex) · PDF: [https://nyfeu.github.io/Vibration_Analysis/slides.pdf](https://nyfeu.github.io/Vibration_Analysis/slides.pdf) |
| Declaração de uso de IA | [`docs/uso_de_ia.md`](docs/uso_de_ia.md) |
| Auditoria de arquivos descartados | [`docs/arquivos_excluidos.md`](docs/arquivos_excluidos.md) |
| Fichamentos das referências | [`docs/records/`](docs/records/README.md) |

---

## Dataset

CWRU Bearing Data Center — sensor **drive end**, taxa de **12 kHz**, rolamento
SKF 6205-2RS JEM.

- Classes: normal, pista interna, pista externa, esfera.
- Cargas: 0 a 3 HP.
- Diâmetros de defeito: 0.007", 0.014", 0.021".

Os 56 arquivos `.mat` originais (179 MB) estão versionados em
[`data/raw/`](data/raw/), baixados das páginas oficiais do CWRU. O inventário com
classe, carga, rotação, nº de amostras e SHA-256 está em
[`data/raw/manifesto.csv`](data/raw/manifesto.csv). Para refazer o download e
conferir a integridade: `python scripts/download_cwru.py`.

> **Atenção:** os arquivos normais (97–100) foram gravados a **48 kHz**, não a
> 12 kHz, e `99.mat` traz por engano as variáveis de `98.mat`. Detalhes e evidência
> em [`data/raw/README.md`](data/raw/README.md).

Descrição completa do setup experimental, quantidade de amostras por classe e
origem dos dados: ver relatório técnico.

A auditoria gravação por gravação, com base em Smith & Randall (2015), está em
[`docs/arquivos_excluidos.md`](docs/arquivos_excluidos.md): nenhum registro foi
excluído; 20 são usados com ressalva.

---

## Ambiente de desenvolvimento

O repositório traz um **devcontainer** com Python 3.11 e a distribuição TeX já
montados. É o caminho recomendado: todo mundo trabalha no mesmo ambiente e
ninguém precisa instalar LaTeX na própria máquina.

- VS Code: abrir a pasta e aceitar *Reopen in Container*.
- Sem VS Code: `devcontainer up --workspace-folder .` (CLI `@devcontainers/cli`).

Instalação manual, como alternativa:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# LaTeX (Debian/Ubuntu), apenas se for compilar o relatório localmente:
sudo apt install texlive-latex-recommended texlive-latex-extra texlive-publishers \
                 texlive-bibtex-extra texlive-lang-portuguese texlive-science \
                 lmodern latexmk biber
```

## Reprodutibilidade

```bash
git clone https://github.com/Nyfeu/Vibration_Analysis.git
cd Vibration_Analysis
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/projeto.ipynb
```

**Todo o código está no notebook** (`notebooks/projeto.ipynb`). Ele grava em
`results/metrics/` e `results/figures/` as tabelas, figuras e matrizes de confusão
que o relatório lê, e termina com uma seção de verificações automáticas
(frequências do rolamento, decimação, ausência de vazamento) que interrompe a
execução se algo falhar.

O notebook segue o roteiro das aulas (*Clean Data* → *Pre-Processing* →
*Select Models* → *GridSearch* → *Melhor modelo* → *Predição*) e está salvo
**com as saídas** da última execução. A CNN 1D exige PyTorch (já instalado no
Colab; localmente, `pip install torch`); sem ele, é ignorada.

**Colab:** [abrir o notebook](https://colab.research.google.com/github/Nyfeu/Vibration_Analysis/blob/main/notebooks/projeto.ipynb). A primeira célula clona o repositório
(os `.mat` estão versionados nele) e instala as dependências; não há download
manual.

**Seeds:** `SEED = 42`, declarada no início do notebook e usada por todos os modelos. A etapa de
dados é determinística.

---

## Relatório

Escrito em LaTeX com a classe `abntex2` (padrão ABNT de trabalho acadêmico) e
bibliografia `biblatex-abnt` com backend `biber`.

```bash
cd docs/relatorio
make            # gera build/relatorio.pdf
make watch      # recompila a cada salvamento
make check      # falha se ainda houver TODO(grupo) pendente
make entrega    # copia o PDF final para docs/relatorio/relatorio.pdf
```

Cada capítulo mora em um arquivo separado sob `docs/relatorio/secoes/`, para
reduzir conflito de merge quando várias pessoas escrevem ao mesmo tempo.
As figuras são lidas direto de `results/figures/` — não copie figura na mão.

### Formatação

Padrão ABNT: corpo 12 pt em Times, espaçamento 1,5, títulos diferenciados de forma
progressiva (NBR 6024) — seção primária em caixa alta e negrito, secundária em
negrito, terciária sem negrito, quaternária em itálico. Links do sumário e das
citações em preto, porque o trabalho é para impressão.

Para trocar a família por Arial, se a instituição exigir, é uma linha no
preâmbulo de `relatorio.tex` (está comentado onde).

### Onde ler o PDF sem compilar nada

| Quero | Onde |
|---|---|
| A versão atual de `main`, no navegador | [https://nyfeu.github.io/Vibration_Analysis/](https://nyfeu.github.io/Vibration_Analysis/) |
| Baixar o PDF direto | [https://nyfeu.github.io/Vibration_Analysis/relatorio.pdf](https://nyfeu.github.io/Vibration_Analysis/relatorio.pdf) |
| O PDF de um pull request | Aba **Actions** → execução do PR → artifact `relatorio-pdf` |
| O PDF da entrega | Anexo da release da tag `v*` |

O Pages é atualizado a cada push em `main` que toque em `docs/relatorio/`.

> **Configuração única, antes do primeiro push:** ligar o Pages em
> **Settings → Pages → Source: "GitHub Actions"**. Sem isso o job `deploy` falha
> (o PDF continua acessível pelo artifact).

---

## Metodologia (resumo)

- **Split:** por condição de carga (treino em 0/1/2 HP, teste em 3 HP), nunca
  aleatório em nível de janela, para evitar vazamento entre segmentos da mesma
  gravação.
- **Detecção:** one-class, treinada apenas com dados normais.
- **Validação física:** o pico do espectro de envelope cai na frequência de defeito
  prevista? Sinal bruto, pré-branqueamento cepstral e kurtograma, comparados à
  auditoria de Smith & Randall (2015).
- **Diagnóstico:** roteiro das aulas — `Pipeline` (scaler + classificador),
  seleção de modelos por validação cruzada (agrupada por carga, para não vazar
  janelas da mesma gravação), `GridSearchCV`, `classification_report` e matriz de
  confusão completa; CNN 1D como contraponto.

Detalhes e justificativa bibliográfica no relatório técnico.

---

## Backlog

O backlog mora em [`scripts/backlog.json`](scripts/backlog.json) — versionado, revisável
em pull request. As issues e o quadro do GitHub Projects são **gerados** a partir dele:

```bash
gh auth login -s project          # o escopo 'project' é obrigatório para o quadro
python scripts/seed_backlog.py --dry-run   # confere o que seria criado
python scripts/seed_backlog.py             # cria de verdade
```

O seeder é idempotente: acrescente um item no `backlog.json`, rode de novo, e só o
que falta é criado. Nada é apagado.

Organização: 6 milestones (M0 a M5) seguindo o pipeline, labels por frente de
trabalho e a label `peso-2` marcando o que a rubrica mais valoriza — detecção e
discussão crítica.

---

## Resultados

> Tabela exigida pelo enunciado (item 6.2). Preencher apenas com valores obtidos de
> execuções reais.

Teste em 3 HP (10 gravações, 581 janelas), treino em 0/1/2 HP. Os classificadores
são `Pipeline(StandardScaler, modelo)`, escolhidos por validação cruzada por carga
(`LeaveOneGroupOut`) entre Regressão Logística, KNN, Random Forest e SVM, com
hiperparâmetros por `GridSearchCV`. TPR/FPR tratam "falha" como qualquer classe ≠
normal; acurácia por classe na ordem normal / pista interna / esfera / pista externa.

| Dataset | Técnica (features) | Tipo de falha identificada | Taxa de detecção (TPR) | Falso positivo (FPR) | Acurácia por classe |
|---|---|---|---|---|---|
| CWRU | Mahalanobis (tempo+envelope) | não se aplica | 1,00 | 0,12 | — |
| CWRU | Isolation Forest (tempo+envelope) | não se aplica | 0,90 | 0,07 | — |
| CWRU | One-Class SVM (tempo+envelope) | não se aplica | 1,00 | 0,81 | — |
| CWRU | Autoencoder (tempo+envelope) | não se aplica | 1,00 | 0,17 | — |
| CWRU | Mahalanobis (envelope) | não se aplica | 0,58 | 0,14 | — |
| CWRU | Mahalanobis (forma, sem RMS/pico) | não se aplica | 0,83 | 0,24 | — |
| CWRU | Random Forest (tempo+envelope) | normal, IR, B, OR | 1,00 | 0,00 | 1,00 / 0,98 / 0,99 / 0,89 |
| CWRU | SVM (tempo+envelope) | normal, IR, B, OR | 0,99 | 0,00 | 1,00 / 0,99 / 0,97 / 0,87 |
| CWRU | Random Forest (envelope) | normal, IR, B, OR | 0,96 | 1,00 | 0,00 / 0,94 / 0,65 / 0,67 |
| CWRU | CNN 1D (sinal bruto) | normal, IR, B, OR | 1,00 | 0,00 | 1,00 / 0,90 / 1,00 / 1,00 |
| CWRU | CNN 1D (sinal normalizado) | normal, IR, B, OR | 1,00 | 0,00 | 1,00 / 0,99 / 1,00 / 1,00 |

**Leitura crítica (detalhes no relatório, cap. 5 e 6):** os valores próximos de
100% não vêm de vazamento (verificado em código), mas de um atalho de amplitude:
o RMS sozinho separa normal de falha (AUC = 1,00), inclusive nas gravações sem
assinatura física do defeito. A validação física pelo espectro de envelope
confirma o defeito em 12/12 gravações de pista interna e 8/12 de pista externa
(@6), e em **nenhuma** de esfera pelo envelope bruto (duas com pré-branqueamento)
— a classe que o Random Forest acerta em 99%. O modelo só com envelope acerta
menos no teste (68%) e generaliza melhor para o defeito em outra posição (76%
contra 40%). A CNN 1D chega a 99,7%, mas acerta até as gravações sem assinatura
e generaliza pior (64%): aprende a montagem, não o defeito.

**Precisão e recall.** Na detecção, 90% das janelas de teste são de falha:
alarmar sempre já daria precisão 0,90 e F1 0,947, então TPR, FPR e AUC são as
métricas que importam. No diagnóstico, a esfera tem recall 0,99 e precisão 0,88:
vira uma classe-refúgio. Uma árvore de decisão com critério de entropia define a
esfera como uma faixa de amplitude, sem usar o escore de BSF (o de menor ganho
de informação).

**Teste decisivo — montagem nova.** Cada defeito do CWRU foi ensaiado numa única
montagem, presente nas quatro cargas. Deixando um diâmetro (montagem) inteiro
fora do treino, todos os modelos treinados caem para perto do acaso (26–55%,
acaso = 33%), enquanto uma **regra física sem treino** — classe pela frequência
de defeito dominante no envelope — acerta 65,7% do tipo de falha e 99,8% da
pista externa em outra posição.

**Estatística aplicada.** A unidade estatística é a gravação (as janelas de uma
gravação são correlacionadas):

- *Análise exploratória*: Kruskal–Wallis por gravação mostra diferença entre
  classes em 7 de 8 features (ε² de 0,31 a 0,54); a exceção é o escore da esfera
  (p = 0,07). RMS e pico são redundantes (ρ de Spearman = 0,95).
- *Pressupostos*: as features normais não são normais (Shapiro–Wilk); o limiar
  qui-quadrado do Mahalanobis daria 6,2% de falsos alarmes no treino em vez de 1%.
- *Intervalos (bootstrap por gravação)*: acurácia do Random Forest 0,957
  [0,894; 1,000]; diferença para o modelo só de envelope 0,28 [0,20; 0,36]. A FPR
  (0,12 [0,06; 0,23], Wilson) vem de uma única gravação normal.
- *Montagem nova*: só a regra física acerta mais montagens que o acaso (6/9,
  p = 0,042, binomial); Random Forest 4/9 (p = 0,35).
- *Sementes*: a generalização do Random Forest com amplitude varia de 0,40 a 0,72
  entre 10 sementes; a do modelo de envelope, de 0,755 a 0,762.

Matrizes de confusão completas: `results/metrics/classificacao_matriz_*.csv` e
Apêndice C do relatório.

---

## Estrutura do repositório

```
.devcontainer/ ambiente de desenvolvimento (Python + TeX Live)
.github/       CI: geração automática do PDF do relatório
data/          dados brutos (raw) e derivados (processed, não versionado)
docs/          enunciado, relatório LaTeX/ABNT, declarações
notebooks/     notebook com todo o código do projeto, executável no Colab
scripts/       download e verificação dos dados (SHA-256) e backlog do GitHub
results/       figuras e métricas gravadas pelo notebook
```

---

## Referências

- RANDALL, R. B. *Vibration-based Condition Monitoring*. Wiley, 2011.
- RANDALL, R. B.; ANTONI, J. Rolling element bearing diagnostics: a tutorial.
  *Mechanical Systems and Signal Processing*, v. 25, n. 2, p. 485–520, 2011.
- SMITH, W. A.; RANDALL, R. B. Rolling element bearing diagnostics using the Case
  Western Reserve University data: a benchmark study. *Mechanical Systems and Signal
  Processing*, v. 64–65, p. 100–131, 2015.
- ISO 20816-1:2016. Mechanical vibration: measurement and evaluation of machine
  vibration.

_Referências específicas de cada técnica (mínimo 2 por técnica) no relatório._
