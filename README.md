# Detecção e Diagnóstico de Anomalias em Sinais de Vibração

Projeto Desafio do 2º semestre — ECM514 Ciência de Dados.
Detecção de anomalias e diagnóstico do tipo de falha em rolamentos, sobre o dataset
público **CWRU (Case Western Reserve University)**.

**Status:** em desenvolvimento.

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
| Notebook executável no Colab | [`notebooks/projeto.ipynb`](notebooks/projeto.ipynb) — _TODO: badge do Colab_ |
| Dados empregados | [`data/raw/`](data/raw/) |
| Relatório técnico (LaTeX/ABNT) | fonte em [`docs/relatorio/`](docs/relatorio/) · PDF: _TODO — link do GitHub Pages_ |
| Apresentação (vídeo, máx. 5 min) | _TODO: link do YouTube_ |
| Slides | _TODO_ |
| Declaração de uso de IA | [`docs/uso_de_ia.md`](docs/uso_de_ia.md) |
| Auditoria de arquivos descartados | [`docs/arquivos_excluidos.md`](docs/arquivos_excluidos.md) |

---

## Dataset

CWRU Bearing Data Center — sensor **drive end**, taxa de **12 kHz**, rolamento
SKF 6205-2RS JEM.

- Classes: normal, pista interna, pista externa, esfera.
- Cargas: 0 a 3 HP.
- Diâmetros de defeito: 0.007", 0.014", 0.021".

Descrição completa do setup experimental, quantidade de amostras por classe e
origem dos dados: ver relatório técnico.

Arquivos descartados com base na auditoria de Smith & Randall (2015) estão listados
em [`docs/arquivos_excluidos.md`](docs/arquivos_excluidos.md).

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

> _TODO: preencher quando o pipeline estiver rodando._

```bash
git clone <url-do-repo>
cd <repo>
pip install -r requirements.txt
```

Para rodar no Colab: _TODO — link e instruções de obtenção dos dados._

Seeds fixas em: _TODO._

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
| A versão atual de `main`, no navegador | GitHub Pages — _TODO: link_ |
| Baixar o PDF direto | `<url-do-pages>/relatorio.pdf` |
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
- **Diagnóstico:** classificação supervisionada multiclasse, com matriz de confusão
  completa.

Detalhes e justificativa bibliográfica no relatório técnico.

---

## Resultados

> Tabela exigida pelo enunciado (item 6.2). Preencher apenas com valores obtidos de
> execuções reais.

| Dataset | Técnica | Tipo de falha identificada | Taxa de detecção (TPR) | Falso positivo (FPR) | Acurácia por classe |
|---|---|---|---|---|---|
| CWRU | _TODO_ | | | | |

Matrizes de confusão completas: `results/metrics/`.

---

## Estrutura do repositório

```
.devcontainer/ ambiente de desenvolvimento (Python + TeX Live)
.github/       CI: geração automática do PDF do relatório
data/          dados brutos (raw) e derivados (processed, não versionado)
docs/          enunciado, relatório LaTeX/ABNT, declarações
notebooks/     notebook principal, executável no Colab
src/           código do pipeline (dados, features, detecção, classificação)
results/       figuras e métricas
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
