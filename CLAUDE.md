# CLAUDE.md — ECM514 Ciência de Dados / Projeto Desafio 2º Semestre

Detecção e diagnóstico de anomalias em sinais de vibração de máquinas rotativas.

Este arquivo é lido automaticamente pelo Claude Code no início de cada sessão. Ele
registra as decisões já fechadas pelo grupo. **Se uma decisão mudar, edite este
arquivo no mesmo commit da mudança.**

---

## 1. Contexto do trabalho

- Disciplina: ECM514 — Ciência de Dados.
- Enunciado completo: `docs/enunciado.pdf`. Consulte-o antes de propor qualquer
  entrega; ele define entregáveis e rubrica.
- Grupo de 4 a 5 alunos.
- Problema aberto, sem gabarito: o enunciado pede exploração de técnicas além das
  vistas em sala, com fundamentação bibliográfica.

### Prazos

| Data | Item |
|---|---|
| 17/09/2026 | Cadastro do dataset escolhido — **feito** |
| a definir | Entrega final: repositório, notebook, relatório, vídeo |

### Rubrica (pesos) — orienta onde investir esforço

| Critério | Peso |
|---|---|
| Levantamento e seleção dos métodos | 1 |
| Aplicação dos métodos e métricas | 2 |
| Resultados de **detecção** | 2 |
| Resultados de **classificação** | 1 |
| **Qualidade da discussão crítica** | 2 |
| Relatório, repositório e código | 1 |
| Apresentação | 1 |

Detecção e discussão crítica valem 2 cada. Um resultado de 97% sem análise de erro
vale menos que 88% com investigação de onde e por que o modelo falha. Priorize
análise sobre número.

---

## 2. Dataset

### Principal: CWRU (Case Western Reserve University)

Configuração fixada pelo grupo — **não altere sem discussão**:

- **Sensor:** drive end (DE). É onde os defeitos foram induzidos por eletroerosão,
  logo tem a melhor relação sinal-ruído.
- **Taxa de amostragem:** 12 kHz. (O conjunto DE a 48 kHz cobre as mesmas
  condições — Smith & Randall, Tab. A3 —; o de 12 kHz foi escolhido por ter menos
  problemas de aquisição: 2 gravações vs 11 na Tab. 3 do artigo.) **Exceção verificada:** os
  arquivos normais (97–100) estão a **48 kHz** e precisam ser decimados para
  12 kHz antes de qualquer uso — sem isso o detector separa pela taxa de
  amostragem, não pela falha. Evidência em `data/raw/README.md`.
- **Banda comum (decidido):** depois da decimação, **todas** as gravações passam
  pelo mesmo passa-baixas (Chebyshev I, ordem 8, 4,8 kHz, fase zero). O filtro
  padrão do `decimate` deixa resíduo de aliasing em 4,8–6 kHz nos normais;
  sem a banda comum essa faixa diferencia normal de falha por artefato. Banda
  útil do projeto: 0–4,8 kHz. Evidência: `sec:banda-comum` e
  `results/metrics/energia_banda_4k8_6k_por_classe.csv`.
- **Janela (decidido):** 4096 amostras (0,341 s), 50% de sobreposição. Derivada
  de 3 períodos da FTF na menor rotação do manifesto (1718 rpm) → 3157,
  arredondado para potência de 2. Conta em `tamanho_janela()` e `sec:janelas`.
- **`99.mat`** contém também as variáveis de `98.mat`: ler sempre a variável
  pelo número do arquivo (`X099_DE_time`).
- **Classes-alvo (4):** normal, defeito em pista interna (IR), defeito em pista
  externa (OR), defeito em esfera (B).
- **Rolamento DE:** SKF 6205-2RS JEM.
- **Diâmetros de defeito:** 0.007", 0.014", 0.021" — tratados como *eixo de
  severidade*, análise secundária. Não explodir em 10+ classes na primeira volta.
- **Cargas:** 0 a 3 HP (rotação nominal aproximada de 1797 a 1730 rpm).
- **Pista externa:** **decidido — @6 (centrada na zona de carga) é a posição
  principal**; é a única com os três diâmetros e equilibra as classes (12 IR,
  12 B, 12 OR). @3 e @12 formam um conjunto de generalização (treinar em @6,
  testar em @3/@12). A zona de carga fica em 6 h (Smith & Randall, 2015, p. 104).
- **Auditoria (decidido):** nenhum registro é excluído por qualidade. Os registros
  sem evidência física do defeito no DE (118–120, 224, 225, 200) ficam **com
  ressalva**, e as métricas são reportadas também estratificadas por categoria
  Y/P/N de Smith & Randall. Detalhes em `docs/arquivos_excluidos.md`.

> Todos os parâmetros numéricos acima devem ser conferidos contra a documentação
> oficial do CWRU Bearing Data Center antes de entrarem no relatório. Não copie
> deste arquivo para o texto final sem verificar na fonte.

### Secundário (opcional): MFPT

Usado apenas como teste de generalização entre datasets (treinar no CWRU, testar no
MFPT). É um extra de discussão crítica — se o cronograma apertar, corte sem dó. O
projeto está completo sem ele.

### Restrições do enunciado

- Dataset público e documentado (setup, taxa de amostragem, tipos de falha,
  condições de operação).
- **Dados sintéticos são proibidos.**
- Dados no repositório; se ultrapassarem o limite do GitHub, usar drive público
  e documentar o link no README.

---

## 3. Regras metodológicas (não negociáveis)

Estas regras existem para evitar os erros clássicos deste dataset. Se alguma
sugestão sua conflitar com elas, **aponte o conflito em vez de contornar
silenciosamente**.

1. **Sem vazamento de dados.** Nunca dividir treino/teste em nível de janela. Um
   sinal longo cortado em janelas gera segmentos quase idênticos; espalhá-los entre
   treino e teste faz o modelo memorizar a gravação, não a falha, e a acurácia sobe
   para ~99% sem significado.
2. **Split por condição de carga.** Treino com 0, 1 e 2 HP; teste com 3 HP. A
   pergunta que interessa é se o modelo generaliza para uma condição de operação
   não vista.
3. **Detecção é one-class.** O detector de anomalia é treinado **somente com dados
   normais**, sem ver nenhuma falha. É o cenário real de manutenção preditiva: na
   fábrica não existem exemplos rotulados de falha antes da falha acontecer. A
   classificação supervisionada é uma etapa separada, posterior à detecção.
4. **Auditoria de arquivos (Smith & Randall, 2015).** O artigo audita gravação por
   gravação e separa os arquivos em utilizáveis, parcialmente utilizáveis e
   problemáticos — alguns têm ruído elétrico dominante ou não mostram a falha nem
   sob análise de envelope. Os arquivos excluídos devem estar listados
   explicitamente em `docs/arquivos_excluidos.md`, com a justificativa e a
   referência. Exclusão não documentada não vale.
5. **Baseline antes de modelo pesado.** A ordem é: features de tempo + classificador
   clássico → análise de envelope → detecção one-class → modelo profundo. Cada
   camada é comparada contra a anterior. Sem baseline não existe comparação, e sem
   comparação a discussão crítica fica vazia.
6. **Janela cobrindo várias revoluções do eixo.** O tamanho da janela é derivado da
   rotação e da taxa de amostragem, não escolhido por conveniência.
7. **Reprodutibilidade.** Seeds fixas e declaradas. O enunciado exige código 100%
   executável e reprodutível no Colab.
8. **Erros são artefato de entrega.** Guarde os casos classificados errado desde o
   primeiro experimento, não só as métricas agregadas. São eles que sustentam os
   2 pontos de discussão crítica.

---

## 4. Pipeline

1. **Dados e protocolo** — parser dos arquivos `.mat`, segmentação em janelas,
   montagem dos splits por carga, seeds.
2. **Features**
   - Tempo: RMS, curtose, fator de crista, assimetria, valor de pico.
   - Frequência: FFT e, principalmente, **análise de envelope (Hilbert)**.
   - Físico: frequências características do rolamento (BPFO, BPFI, BSF, FTF)
     calculadas a partir da geometria do 6205 e da rotação do eixo. Mostrar que o
     pico do envelope cai na frequência prevista pela teoria é o argumento mais
     forte disponível para o relatório — priorize isso.
     **Convenção decidida:** BSF como em Smith & Randall (2,357 × f_r no DE); o
     "Rolling Element" da página do CWRU (4,7135 × f_r) é 2 × BSF (`bsf_2x`).
   - Tempo-frequência (se houver tempo): STFT, wavelet, kurtograma/spectral
     kurtosis para escolher a banda de demodulação.
3. **Detecção** — baseline com Isolation Forest e distância de Mahalanobis;
   comparação com One-Class SVM e autoencoder. Métricas: ROC, TPR, FPR.
4. **Classificação** — Random Forest ou SVM sobre as features; matriz de confusão
   completa com todas as classes. CNN 1D sobre o sinal bruto como contraponto, se
   sobrar tempo.

### Tabela de resultados exigida pelo enunciado

Todo experimento relevante alimenta esta tabela, que deve aparecer no README e no
relatório:

| Dataset | Técnica | Tipo de falha identificada | TPR | FPR | Acurácia por classe |
|---|---|---|---|---|---|

Técnicas que só detectam deixam a coluna de tipo de falha como "não se aplica".

---

## 5. Estrutura do repositório

```
.
├── CLAUDE.md                  # este arquivo (fora do versionamento)
├── README.md                  # sumário apontando para cada entrega (exigido)
├── requirements.txt
├── .gitignore
├── .devcontainer/
│   ├── devcontainer.json      # extensões e settings do VS Code
│   └── Dockerfile             # Python 3.11 + TeX Live (subconjunto)
├── .github/workflows/
│   └── relatorio.yml          # compila o PDF a cada push
├── data/
│   ├── raw/                   # .mat originais do CWRU (versionados)
│   └── processed/             # derivados — NÃO versionar
├── docs/
│   ├── enunciado.pdf
│   ├── arquivos_excluidos.md  # auditoria Smith & Randall
│   ├── uso_de_ia.md           # declaração exigida pelo enunciado
│   └── relatorio/             # LaTeX, classe abntex2
│       ├── relatorio.tex      # documento principal — não escreva seção aqui
│       ├── referencias.bib    # biblatex, backend biber
│       ├── secoes/*.tex       # um arquivo por capítulo
│       ├── latexmkrc
│       ├── Makefile           # make / watch / check / entrega
│       └── build/             # saída do latexmk — NÃO versionar
├── notebooks/
│   └── projeto.ipynb          # executável no Colab, ponta a ponta
├── src/
│   ├── data.py                # carregamento, segmentação, splits
│   ├── features.py            # tempo, frequência, envelope, frequências do rolamento
│   ├── detection.py           # one-class
│   ├── classification.py      # pipelines, seleção de modelos, GridSearchCV
│   ├── cnn.py                 # CNN 1D (PyTorch opcional)
│   ├── experimentos.py        # orquestra detecção e classificação
│   └── evaluation.py          # métricas e matrizes de confusão
├── scripts/                   # download, backlog e geração de artefatos
├── tests/                     # pytest; rodar da raiz: python -m pytest tests
└── results/
    ├── figures/
    └── metrics/
```

Lógica pesada mora em `src/`; o notebook importa e orquestra. Isso evita um
notebook de 3000 linhas impossível de revisar — e o critério de qualidade de código
vale 1 ponto.

---

## 6. Convenções de código

- Python 3.11+, `numpy`, `scipy`, `pandas`, `scikit-learn`, `matplotlib`.
- O notebook precisa rodar no Colab do zero, incluindo a obtenção dos dados.
- Caminhos relativos à raiz do repositório. Nada de caminho absoluto de máquina
  pessoal.
- Funções com docstring curta explicando **o parâmetro físico** quando houver
  (por que essa janela, por que essa banda).
- Figuras salvas em `results/figures/` com nome descritivo, não `fig1.png`.
  São **versionadas**: o CI compila o PDF sem rodar o pipeline.
- Identificadores em português (`features_tempo`, `catalogo`); siglas físicas
  ficam como na literatura (`bpfo`, `rms`).
- Commits em português, no imperativo: "adiciona parser dos arquivos .mat".

### Relatório

- Escrito em LaTeX, classe `abntex2`, bibliografia `biblatex-abnt` com backend
  `biber` (e não bibtex — o `biber` lida com UTF-8 na `.bib` sem escape).
- **Um capítulo por arquivo** em `docs/relatorio/secoes/`. Nunca escreva conteúdo
  de seção em `relatorio.tex`; isso serializa o grupo em conflitos de merge.
- Figuras vêm de `results/figures/` via `\graphicspath` — não copie figura para
  dentro de `docs/relatorio/`.
  Exceção: imagens externas ao pipeline (ex.: foto da bancada do CWRU) ficam em
  `docs/relatorio/assets/`, também no `\graphicspath`.
- Toda referência nova entra em `referencias.bib` com chave `autor+ano`.
- `make check` falha enquanto houver `TODO(grupo)` no texto. Rode antes da entrega.
- Formatação ABNT já ajustada no preâmbulo: corpo 12 pt em Times (`mathptmx`),
  títulos com diferenciação progressiva (NBR 6024) e links em preto. **Não volte
  aos defaults do abntex2** (títulos sem serifa em `\Huge`, links azuis) — foi
  exatamente o que o grupo pediu para corrigir.
- Fonte via `mathptmx` e não `newtx` de propósito: o `newtx` só existe no
  `texlive-fonts-extra` (1,7 GB), que dobraria a imagem do devcontainer.
- O PDF publicado sai no GitHub Pages a cada push em `main`; artifact serve para
  pull request; release para a entrega.

### Ambiente

- O ambiente canônico é o devcontainer (`.devcontainer/`). Dependência nova de
  Python vai em `requirements.txt`; pacote LaTeX novo vai no `Dockerfile`.
  **Nunca `tlmgr install` dentro do container** — quebra a reprodutibilidade.
- O notebook ainda precisa rodar no Colab do zero, independentemente do
  devcontainer.

---

## 7. Instruções para o Claude Code

- **Não invente resultados.** Nunca escreva números de acurácia, TPR ou FPR que não
  vieram de uma execução real neste repositório. Se um valor for placeholder, marque
  como `TODO` explicitamente.
- **Não pule o baseline** mesmo que um modelo mais sofisticado pareça óbvio.
- Se uma métrica vier suspeitamente alta (≥ 98%), a primeira hipótese é vazamento
  de dados, não sucesso. Investigue o split antes de comemorar.
- Ao propor uma técnica nova, traga **2 referências bibliográficas**, que é o mínimo
  exigido pelo enunciado por técnica.
- Prefira editar `src/` a acumular código no notebook.
- Ao terminar uma tarefa relevante, atualize a seção 8 deste arquivo.
- **Registre o uso de IA.** Toda contribuição sua que entrar no repositório deve ser
  anotada em `docs/uso_de_ia.md` (o que foi pedido, o que foi aproveitado, o que foi
  revisado pelo grupo). O enunciado exige essa declaração.

---

## 8. Estado atual

**Fase:** pipeline completo e relatório redigido; falta revisão do grupo e a apresentação.

Feito:

- [x] Estrutura de pastas, `requirements.txt`, `docs/uso_de_ia.md` e
      `docs/arquivos_excluidos.md` (esqueletos, sem conteúdo)
- [x] Esqueleto do relatório em LaTeX/ABNT (`abntex2` + `biblatex-abnt`),
      compilando localmente com `make`
- [x] Devcontainer (Python 3.11 + TeX Live) e workflow de geração do PDF
- [x] Repositório criado em github.com/Nyfeu/Vibration_Analysis
- [x] Backlog escrito em `scripts/backlog.json` (35 itens, 6 milestones)
- [x] Dataset cadastrado (prazo 17/09/2026)
- [x] CWRU baixado (issue #3): 56 `.mat` em `data/raw/` (179 MB, versionados),
      `scripts/download_cwru.py` + `data/raw/manifesto.csv` (SHA-256). Taxa e nº
      de arquivos por classe conferidos contra o site oficial; inconsistências
      documentadas em `data/raw/README.md`

Próximos passos:

- [ ] Popular o backlog no GitHub: `python scripts/seed_backlog.py`
      (fonte em `scripts/backlog.json`; exige `gh auth login -s project`)
- [x] Fichamento de Smith & Randall (2015) em `docs/records/smith2015.md`
- [x] `docs/arquivos_excluidos.md` e Apêndice B preenchidos: 40 registros
      utilizados, 0 excluídos, 20 com ressalva; OR @6 declarada em
      `02-dataset.tex`
- [x] Posição OR (issue #5): @6 principal, @3/@12 generalização — Tabela 1 de
      `02-dataset.tex` e `src/data.py` (`catalogo()`)
- [ ] **Discutir no grupo:** o split por carga não separa montagens (Smith &
      Randall: a montagem domina o sinal) — avaliar split por diâmetro como
      experimento complementar
- [x] Dados (issues #6–#9) em `src/data.py`: parser pelo manifesto, decimação,
      banda comum, janelas, split por carga com verificação de vazamento,
      `SEED = 42`, contagem em `results/metrics/`; testes em `tests/test_data.py`.
      Artefatos: `python -m scripts.gerar_artefatos_dados`
- [x] Esqueleto de `notebooks/projeto.ipynb` (clone no Colab + etapa de dados)
- [x] Envelope (#11) e validação física (#13): SES "método 1", escores por
      família com harmônicos sem colisão (BPFO/BPFI ×1,2; BSF ×2,4).
      Resultado: concorda com Smith & Randall (M1) em 50/52 falhas; **esfera:
      0/12 confirmadas** — acerto do classificador em B é suspeito de atalho.
      Auditoria transcrita em `data/auditoria_smith2015.csv` (Tab. B2)
- [x] Detecção (#15–#18): Mahalanobis, Isolation Forest, One-Class SVM,
      autoencoder (MLPRegressor, sem torch) × 4 conjuntos de features (tempo,
      envelope, tempo+envelope, forma = sem RMS/pico). Limiar = p99 dos normais
      de treino. **Achado:** AUC 1,00 com tempo vem do RMS (AUC 1,00 sozinho),
      não de vazamento; gravações sem assinatura (200, 225) dão alarme em 100%
- [x] Classificação (#19, #20, #22): RF e SVM. RF tempo+envelope 95,7%, mas
      esfera 99% sem assinatura física e generalização @3/@12 só 46%; RF só
      envelope 67,6% no teste e 76% na generalização. Matrizes geradas em
      `results/metrics/matrizes_confusao.tex` (Apêndice C via \input)
- [x] Relatório: resultados, discussão crítica e conclusão redigidos; README com
      a tabela de resultados
- [ ] Pendências do grupo: responsáveis por capítulo, Apêndice A (uso de IA),
      vídeo e slides; revisar referências escritas de memória (técnicas one-class
      e classificação)
- [x] Roteiro das aulas (pedido do grupo): `Pipeline(StandardScaler, clf)`,
      seleção de modelos (LogReg, KNN 3/9, RF, SVM) por `cross_val_score` com
      **`LeaveOneGroupOut` por carga** (StratifiedKFold embaralhado só como
      contraste de vazamento), `GridSearchCV`, `classification_report`; notebook
      reorganizado nas seções da prova e salvo com saídas
- [x] Kurtograma (#14): SK por STFT + pré-branqueamento cepstral. Pré-branq.
      recupera B 222/223 (= Smith M2); kurtograma sem DRS é frágil (197: SK≈0,1)
- [x] CNN 1D (#21, `src/cnn.py`, PyTorch opcional): 99,7% normalizada, mas acerta
      200/225 e generaliza 64% → aprende a montagem
- [x] MFPT (#23): **não feito** — site oficial saiu do ar (redireciona à ASNT);
      só há cópias não oficiais
- [x] Split por montagem (LeaveOneGroupOut por diâmetro, só falhas): todos os
      modelos treinados 26–55% (acaso 33%); **regra física sem treino 65,7%**,
      99,8% na generalização. Seção `sec:res-montagem`
- [x] Revisão do relatório: \paragraph sem número, validação física como 5.2,
      2+ referências por técnica (pré-branqueamento, detectores, KNN/LogReg,
      features de tempo), Apêndice A consolidado
- [x] `docs/articles/` fora do Git (PDFs com direitos autorais; `.gitignore`) e
      removido do histórico com `git filter-repo` (backup em
      `../Vibration_Analysis_backup_2026-10-10.bundle`)
- [x] Fichamento de cada referência do `.bib` em `docs/records/` (índice em
      `docs/records/README.md`); os feitos com IA têm aviso e pendências de conferência
- [ ] Extras possíveis: features só de razões entre famílias de envelope,
      normalização de amplitude por gravação, DRS antes do kurtograma
- [x] Features de tempo (issue #10) e frequências características do
      rolamento (issue #12) em `src/features.py`, com testes em `tests/`;
      BSF na convenção de Smith & Randall
- [x] `sec:features` (metodologia) declara a curtose de Pearson, a remoção da
      média por janela, a convenção de BSF, a rotação medida (nominal em 98/99)
      e a tolerância de ±2%; envelope ainda `TODO(grupo)`
- [x] Relatório: foto da bancada (cap. 2), frequências características e
      decimação na fundamentação (cap. 3), pré-processamento na metodologia
      (cap. 4)
- [ ] Baseline: features de tempo + Random Forest

Divisão de frentes (4–5 pessoas):

1. Dados e protocolo (garante a reprodutibilidade)
2. Features clássicas e envelope
3. Detecção one-class
4. Classificação
5. Relatório, repositório e apresentação — mas a escrita é de todos

---

## 9. Referências de partida

- RANDALL, R. B. *Vibration-based Condition Monitoring*. Wiley, 2011.
- RANDALL, R. B.; ANTONI, J. Rolling element bearing diagnostics: a tutorial.
  *Mechanical Systems and Signal Processing*, v. 25, n. 2, p. 485–520, 2011.
- SMITH, W. A.; RANDALL, R. B. Rolling element bearing diagnostics using the Case
  Western Reserve University data: a benchmark study. *Mechanical Systems and Signal
  Processing*, v. 64–65, p. 100–131, 2015. **Leitura obrigatória antes de usar o
  CWRU.**
- ISO 20816-1:2016. Mechanical vibration: measurement and evaluation of machine
  vibration.
