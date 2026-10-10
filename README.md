# Detecção e Diagnóstico de Anomalias em Sinais de Vibração

Projeto Desafio do 2º semestre — ECM514 Ciência de Dados (Instituto Mauá de Tecnologia).
Detecção de anomalias e diagnóstico do tipo de falha em rolamentos, sobre o dataset
público **CWRU (Case Western Reserve University)**.

| Nome | RA |
|---|---|
| André Solano F. R. Maiolini | 19.02012-0 |
| Durval Consorti Soranz de Barros Santos | 22.01097-0 |
| Leonardo Roberto Amadio | 22.01300-8 |
| Lucas Castanho Paganotto Carvalho | 22.00921-3 |
| Estevan Delazari Feher | 21.00586-9 |

## Entregas

| Entrega | Onde |
|---|---|
| Notebook (todo o código) | [`notebooks/projeto.ipynb`](notebooks/projeto.ipynb) · [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Nyfeu/Vibration_Analysis/blob/main/notebooks/projeto.ipynb) |
| Relatório técnico (PDF) | [nyfeu.github.io/Vibration_Analysis](https://nyfeu.github.io/Vibration_Analysis/) · fonte LaTeX em [`docs/relatorio/`](docs/relatorio/) |
| Slides (PDF) | [slides.pdf](https://nyfeu.github.io/Vibration_Analysis/slides.pdf) · fonte em [`docs/apresentacao/`](docs/apresentacao/) |
| Vídeo (máx. 5 min) | _TODO: link do YouTube_ |
| Dados empregados | [`data/raw/`](data/raw/) |
| Auditoria dos arquivos | [`docs/arquivos_excluidos.md`](docs/arquivos_excluidos.md) |
| Declaração de uso de IA | [`docs/uso_de_ia.md`](docs/uso_de_ia.md) |
| Fichamentos das referências | [`docs/records/`](docs/records/README.md) |

## Como executar

**No Colab:** abrir o notebook pelo botão acima e executar tudo. A primeira célula
clona o repositório (os dados estão versionados nele) e instala só as
dependências que faltarem.

**Localmente:**

```bash
git clone https://github.com/Nyfeu/Vibration_Analysis.git && cd Vibration_Analysis
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/projeto.ipynb
```

O notebook grava as figuras e métricas em `results/` e termina com verificações
automáticas (`assert`) de frequências, decimação e ausência de vazamento. Semente
fixa: `SEED = 42`. A CNN 1D exige PyTorch, que já vem instalado no Colab.
Execução: cerca de 2 min numa CPU de 32 núcleos; no Colab é mais lenta (_tempo
a medir_). Para o relatório, há um devcontainer (`.devcontainer/`) com Python e
TeX Live, e o PDF é compilado com `make` em `docs/relatorio/`.

## Dataset

CWRU Bearing Data Center: sensor **drive end**, **12 kHz**, rolamento SKF 6205-2RS
JEM, cargas de 0 a 3 HP, defeitos de 0,007", 0,014" e 0,021" na pista interna, na
pista externa (@6) e na esfera. São 56 arquivos `.mat` (179 MB), com o inventário e
o SHA-256 em [`data/raw/manifesto.csv`](data/raw/manifesto.csv)
(`python scripts/download_cwru.py` refaz o download e confere a integridade).

Os arquivos normais (97–100) foram gravados a **48 kHz** e são decimados para
12 kHz; o `99.mat` contém também as variáveis do `98.mat`
([`data/raw/README.md`](data/raw/README.md)). Nenhum registro foi excluído, e 20
são usados com ressalva, segundo a auditoria de Smith & Randall (2015).

## Metodologia

- **Split por carga:** treino em 0/1/2 HP e teste em 3 HP, sempre por gravação,
  nunca por janela.
- **Detecção one-class:** treinada só com dados normais (Mahalanobis, Isolation
  Forest, One-Class SVM, autoencoder).
- **Validação física:** verifica se o pico do espectro de envelope cai na
  frequência de defeito prevista pela geometria do rolamento.
- **Diagnóstico:** `Pipeline(StandardScaler, modelo)`, seleção de modelos por
  validação cruzada agrupada por carga, `GridSearchCV` e CNN 1D como contraponto.
- **Montagem nova:** validação deixando um diâmetro (uma montagem) inteiro fora
  do treino.

## Resultados

Teste em 3 HP (10 gravações, 581 janelas). TPR e FPR tratam "falha" como
qualquer classe diferente de normal; a acurácia por classe segue a ordem normal /
pista interna / esfera / pista externa.

| Dataset | Técnica (features) | Tipo de falha identificada | Taxa de detecção (TPR) | Falso positivo (FPR) | Acurácia por classe |
|---|---|---|---|---|---|
| CWRU | Mahalanobis (tempo+envelope) | não se aplica | 1,00 | 0,12 | — |
| CWRU | Isolation Forest (tempo+envelope) | não se aplica | 0,90 | 0,07 | — |
| CWRU | One-Class SVM (tempo+envelope) | não se aplica | 1,00 | 0,81 | — |
| CWRU | Autoencoder (tempo+envelope) | não se aplica | 1,00 | 0,17 | — |
| CWRU | Mahalanobis (envelope) | não se aplica | 0,58 | 0,14 | — |
| CWRU | **Autoencoder (envelope) — detector recomendado** | não se aplica | 0,54 | 0,03 | — |
| CWRU | Mahalanobis (forma, sem RMS/pico) | não se aplica | 0,83 | 0,24 | — |
| CWRU | Random Forest (tempo+envelope) | normal, IR, B, OR | 1,00 | 0,00 | 1,00 / 0,98 / 0,99 / 0,89 |
| CWRU | SVM (tempo+envelope) | normal, IR, B, OR | 0,99 | 0,00 | 1,00 / 0,99 / 0,97 / 0,87 |
| CWRU | Random Forest (envelope) | normal, IR, B, OR | 0,96 | 1,00 | 0,00 / 0,94 / 0,65 / 0,67 |
| CWRU | CNN 1D (sinal bruto) | normal, IR, B, OR | 1,00 | 0,00 | 1,00 / 0,90 / 1,00 / 1,00 |
| CWRU | CNN 1D (sinal normalizado) | normal, IR, B, OR | 1,00 | 0,00 | 1,00 / 0,99 / 1,00 / 1,00 |
| CWRU | Regra física, sem treino (envelope)¹ | IR, B, OR | n. a. | n. a. | — / 1,00 / 0,22 / 0,71 |
| CWRU | Regra física — **montagem nova**² | IR, B, OR | n. a. | n. a. | — / 1,00 / 0,24 / 0,73 |
| CWRU | Random Forest (tempo+envelope) — montagem nova² | IR, B, OR | n. a. | n. a. | — / 0,25 / 0,87 / 0,25 |

¹ A regra física decide só entre os três tipos de falha (não prevê "normal").
² Um diâmetro (montagem) inteiro fora do treino, só falhas, acaso = 0,33. Regra
física 0,657 (6/9 montagens, p = 0,042); Random Forest 0,457 (4/9, p = 0,35).

### Principais conclusões

1. **A detecção é resolvida pela amplitude.** O RMS sozinho separa normal de falha
   (AUC = 1,00), inclusive nas gravações sem assinatura física do defeito. Não há
   vazamento, o que foi verificado em código. Só com o envelope, o AUC fica entre
   0,69 e 0,83. Detector recomendado: autoencoder sobre envelope (FPR 0,034), mas a
   escolha foi feita olhando o teste, então essa FPR é uma estimativa otimista.
2. **A acurácia de 95,7% (IC 95% [0,89; 1,00]) não indica diagnóstico.** A esfera
   é acertada em 99% sem que o defeito apareça no envelope (0/12 gravações), e o
   modelo reconhece só 40% da pista externa em outra posição.
3. **Com uma montagem nova, os modelos treinados ficam perto do acaso**
   (26–55%). Só a regra física sem treino supera o acaso (65,7%, p = 0,042).
4. **Origem da dependência da montagem (análise exploratória).** Retirar a
   amplitude não basta, mas, sem a classe esfera, modelos treinados só com o
   envelope reconhecem montagens novas de pista interna e externa (0,83–0,95,
   acaso 0,50).
5. **A unidade estatística é a gravação.** Intervalos por bootstrap de gravações,
   teste binomial por montagem e variação entre sementes estão no relatório
   (Seção 5.7).

Discussão completa nos capítulos 5 e 6 do relatório; matrizes de confusão no
Apêndice C e em `results/metrics/`.

## Estrutura do repositório

```
data/raw/      arquivos .mat originais do CWRU e manifesto (SHA-256)
docs/          enunciado, relatório (LaTeX/ABNT), slides, fichamentos e declarações
notebooks/     notebook com todo o código, executável no Colab
results/       figuras e métricas gravadas pelo notebook
scripts/       download e verificação dos dados
```

## Referências principais

- SMITH, W. A.; RANDALL, R. B. Rolling element bearing diagnostics using the Case
  Western Reserve University data: a benchmark study. *Mechanical Systems and Signal
  Processing*, v. 64–65, p. 100–131, 2015.
- RANDALL, R. B.; ANTONI, J. Rolling element bearing diagnostics: a tutorial.
  *Mechanical Systems and Signal Processing*, v. 25, n. 2, p. 485–520, 2011.
- RANDALL, R. B. *Vibration-based Condition Monitoring*. Wiley, 2011.

As referências de cada técnica (no mínimo duas por técnica) estão no relatório.
