# Auditoria de arquivos do CWRU — gravações excluídas

> Exigido pela regra metodológica. Base: a auditoria gravação por
> gravação de **Smith & Randall (2015)**, fichada em
> [`docs/records/smith2015.md`](records/smith2015.md). Os arquivos e as
> inconsistências da fonte oficial estão em [`data/raw/README.md`](../data/raw/README.md).
>
> **Exclusão não documentada não vale.** Toda gravação descartada precisa de
> justificativa e referência nas tabelas abaixo.
>
> **Status:** preenchido em 2026-10-06. Decisões do grupo: (A) os registros sem
> evidência física do defeito são **mantidos com ressalva**, não excluídos;
> (B) a posição principal do defeito em pista externa é **@6**.

---

## 1. Configuração auditada

| Parâmetro | Valor |
|---|---|
| Sensor | Drive end (DE) |
| Taxa de amostragem | 12 kHz. Exceção: os normais foram gravados a 48 kHz e são decimados para 12 kHz (critério C6) |
| Rolamento | SKF 6205-2RS JEM |
| Classes | normal, pista interna (IR), pista externa (OR), esfera (B) |
| Cargas | 0–3 HP. Treino em 0, 1 e 2 HP; teste em 3 HP |
| Diâmetros de defeito | 0.007", 0.014", 0.021" |
| Posição do defeito em OR | **@6, centrada na zona de carga.** É a única posição com os três diâmetros, e com ela as classes ficam equilibradas (12 IR, 12 B, 12 OR). A zona de carga fica em 6 h segundo Smith & Randall (2015, p. 5), que corrigem uma seção do site do CWRU. Os registros @3 e @12 formam um conjunto separado de generalização (seção 3.2). |

Todos os valores foram conferidos contra as páginas oficiais do CWRU (ver
`data/raw/README.md`) e contra as Tabelas A1 e A2 de Smith & Randall (2015).

---

## 2. Critérios adotados

Os diagnósticos citados são os do **canal DE** na Tabela B2 de Smith & Randall
(2015), obtidos com três métodos: M1, o envelope do sinal bruto; M2, o
pré-branqueamento cepstral; e M3, a sequência DRS + kurtograma + envelope. As
categorias vão de Y1 a N2, conforme a Tabela 4 do artigo.

| ID | Critério | Origem | Efeito |
|---|---|---|---|
| C1 | Nenhum dos três métodos diagnostica o defeito declarado no canal DE (só N1/N2) | Smith & Randall (2015), Tab. B2 e Tab. 6 | Mantido com ressalva (decisão A) |
| C2 | O melhor diagnóstico no DE é só parcial (P1/P2) | Smith & Randall (2015), Tab. B2 e Tab. 4 | Mantido com ressalva |
| C3 | O envelope do sinal bruto (M1) não detecta o defeito; ele só aparece com pré-processamento (M2/M3) | Smith & Randall (2015), Tab. B2 | Mantido com ressalva |
| C4 | O sinal tem trechos saturados (*clipping*) | Smith & Randall (2015), Tab. 3; conferido nos arquivos | Mantido com ressalva |
| C5 | Fora do escopo do experimento principal | Decisão do grupo (`CLAUDE.md`, seção 2) | Fora do experimento principal |
| C6 | Taxa de amostragem diferente das falhas, ou variáveis inconsistentes no `.mat` | Smith & Randall (2015), Tab. A1; `data/raw/README.md` | Mantido; corrigido no carregador |

**Por que C1 não exclui.** No nosso subconjunto não há arquivo corrompido. Os
registros C1 são gravações reais de rolamentos com defeito que não mostram a
assinatura física esperada. Excluí-los teria três efeitos ruins:

1. **Inflaria o TPR do detector**, porque removeria justamente as falhas difíceis.
2. **Quebraria o split por carga.** A esfera de 0,007" ficaria sem treino (só
   restaria o 121, que é de teste). A esfera de 0,021" e a OR de 0,014" ficariam
   sem teste.
3. **Esconderia o caso mais informativo.** Se o modelo "acertar" um registro C1,
   ele está usando algo que não é o defeito (a montagem ou a EMI do dinamômetro;
   ver Smith & Randall, 2015, p. 6–8).

Por isso as métricas serão reportadas **também estratificadas** por categoria de
diagnóstico (Y, P, N).

---

## 3. Arquivos excluídos

### 3.1 Excluídos por qualidade do sinal

| Arquivo (.mat) | Classe | Diâmetro | Carga (HP) | Critério | Justificativa | Referência |
|---|---|---|---|---|---|---|
| — | — | — | — | — | **Nenhum.** Nenhum registro do subconjunto tem defeito de aquisição que impeça o uso: a pior saturação atinge 7 de ~122 mil amostras (critério C4). Os registros sem evidência física do defeito ficam com ressalva (seção 4). | Smith & Randall (2015), Tab. 3 e B2 |

### 3.2 Fora do experimento principal (critério C5)

Estes registros não são exclusões por qualidade. Ficam fora por decisão de escopo.

| Arquivos | Classe | Motivo | Destino |
|---|---|---|---|
| 144–147, 246–249 | OR @3 (ortogonal) | Posição @6 adotada como principal | **Conjunto de generalização**: treinar em @6 e testar em @3. Todos têm diagnóstico Y2 no DE (Tab. B2). |
| 156, 158–160, 258–261 | OR @12 (oposta) | Posição @6 adotada como principal | **Conjunto de generalização**: treinar em @6 e testar em @12. Em teoria, fora da zona de carga não deveria haver resposta; o artigo atribui a resposta observada a folga mecânica (p. 14–15). |
| 3001–3008 | IR e B 0,028" | Rolamento NTN, não SKF; sem gravação de OR. IR 3001–3004 não diagnosticável (Tab. 6). | Não baixados |
| Canais FE e BA | — | O sensor adotado é o DE | Ignorados pelo carregador |

---

## 4. Arquivos parcialmente utilizáveis (mantidos com ressalva)

> Gravações usadas apesar de problemas conhecidos. A ressalva precisa aparecer
> também na discussão crítica do relatório.

Diagnóstico no formato M1 / M2 / M3, no canal DE. Um traço significa que o artigo
não aplicou o método, porque M2 e M3 só foram usados quando M1 ficou em P1 ou abaixo.

| Arquivo (.mat) | Classe | Diâm. | Carga (HP) | Critério | Ressalva | Impacto esperado na análise |
|---|---|---|---|---|---|---|
| 118 | B | 0,007" | 0 | C1 | N1 / N1 / N1. O envelope mostra só harmônicos de 0,2 f_r; a FTF parece travada em 0,4 f_r (p. 10, Fig. 8) | Sem assinatura de BSF: acerto do classificador indica atalho |
| 119 | B | 0,007" | 1 | C1 | N1 / N2 / N1 | Idem |
| 120 | B | 0,007" | 2 | C1 | N1 / N2 / N1 | Idem |
| 224 | B | 0,021" | 2 | C1 | N1 / N1 / N1 | Idem |
| 225 | B | 0,021" | **3 (teste)** | C1 | N1 / N1 / N1 | Idem; afeta diretamente o TPR e a acurácia de B no teste |
| 200 | OR @6 | 0,014" | **3 (teste)** | C1 | N1 / N1 / N1. Pulsos aleatórios atribuídos a folga mecânica (p. 11, Fig. 12) | Sem assinatura de BPFO: erro esperado e explicável |
| 185 | B | 0,014" | 0 | C2 | P2 / P2 / N1. BSF "borrada" por modulação de amplitude aleatória e impulsiva (p. 11) | Features em BSF fracas; confusão B ↔ outras classes plausível |
| 186 | B | 0,014" | 1 | C2 | P2 / P2 / P2 | Idem |
| 187 | B | 0,014" | 2 | C2 | N1 / P2 / N1 | Idem |
| 188 | B | 0,014" | **3 (teste)** | C2 | P2 / P2 / P2 | Idem, no conjunto de teste |
| 198 | OR @6 | 0,014" | 1 | C2 | P2 / N2 / N2 | Montagem do 0,014" com folga (p. 11) |
| 199 | OR @6 | 0,014" | 2 | C2 | P1 / N2 / N1 | Idem |
| 121 | B | 0,007" | **3 (teste)** | C3 | N1 / N1 / Y2. Só o M3 (DRS + kurtograma) diagnostica | O envelope simples (nosso baseline) não deve encontrar a BSF |
| 197 | OR @6 | 0,014" | 0 | C3 | N1 / N1 / Y2. Só o M3 diagnostica (p. 11, Fig. 13) | Idem, para BPFO |
| 236 | OR @6 | 0,021" | 2 | C4 | Saturação: 7 amostras no teto de ±6,65 (Tab. 3). Diagnóstico Y2 | Pode distorcer pico e fator de crista; impacto pequeno |
| 237 | OR @6 | 0,021" | **3 (teste)** | C4 | Saturação: 5 amostras no teto de ±6,65 (Tab. 3). Diagnóstico Y2 | Idem, no conjunto de teste |
| 97 | normal | — | 0 | C6 | Gravado a 48 kHz (Tab. A1); só 5,1 s | Decimar para 12 kHz; sem isso, o detector separa as classes pela taxa de amostragem |
| 98 | normal | — | 1 | C6 | 48 kHz; sem variável de rotação | Decimar; usar a rotação nominal (1772 rpm) |
| 99 | normal | — | 2 | C6 | 48 kHz; o arquivo também contém as variáveis de `98.mat` e não tem variável de rotação | Decimar; ler `X099_DE_time` pelo número; usar 1750 rpm |
| 100 | normal | — | **3 (teste)** | C6 | 48 kHz | Decimar. É a **única** gravação normal do teste: o FPR é estimado nela |

Além desses, dois registros merecem nota, embora sejam diagnosticáveis: o 171 (IR
0,014", 2 HP) e o 222 (B 0,021", 0 HP) ficam em P1 no M1 e chegam a Y2 com o M2.

---

## 5. Resumo quantitativo

| | Nº de gravações |
|---|---|
| Disponíveis na configuração auditada | 40 (4 normais + 12 IR + 12 B + 12 OR @6) |
| Excluídas | 0 |
| Mantidas com ressalva | 20 (C1: 6 · C2: 6 · C3: 2 · C4: 2 · C6: 4) |
| Utilizadas | 40 |
| Conjunto de generalização (C5, OR @3 e @12) | 16 |

### Diagnosticabilidade por classe (melhor resultado no DE, entre os três métodos)

| Classe | Y (sucesso) | P (parcial) | N (não) | Total |
|---|---|---|---|---|
| IR | 12 | 0 | 0 | 12 |
| B | 3 (121, 222, 223) | 4 (185–188) | 5 (118–120, 224, 225) | 12 |
| OR @6 | 9 (130–133, 197, 234–237) | 2 (198, 199) | 1 (200) | 12 |

### Composição do conjunto de teste (3 HP)

| Classe | Registros | Situação |
|---|---|---|
| Normal | 100 | 48 kHz → decimado |
| IR | 108, 172, 212 | Todos Y |
| B | 121, 188, 225 | Y só com M3 · P · **N** |
| OR @6 | 133, 200, 237 | Y · **N** · Y (saturado) |

Dois dos nove registros de falha do teste (200 e 225) não têm evidência física do
defeito, e um terceiro (121) só tem com pré-processamento. Esse é o teto realista
de qualquer método baseado na física do envelope, e deve ser citado ao discutir o
TPR e a acurácia de B e OR.

---

## Referência

SMITH, W. A.; RANDALL, R. B. Rolling element bearing diagnostics using the Case
Western Reserve University data: a benchmark study. *Mechanical Systems and Signal
Processing*, v. 64–65, p. 100–131, 2015. DOI: 10.1016/j.ymssp.2015.04.021.
