# Fichamento — Smith & Randall (2015)

| | |
|---|---|
| **Referência (ABNT)** | SMITH, W. A.; RANDALL, R. B. Rolling element bearing diagnostics using the Case Western Reserve University data: a benchmark study. *Mechanical Systems and Signal Processing*, v. 64–65, p. 100–131, 2015. DOI: [10.1016/j.ymssp.2015.04.021](https://doi.org/10.1016/j.ymssp.2015.04.021). |
| **Chave no `.bib`** | `smith2015` |
| **Arquivo** | `docs/articles/smith2015.pdf` (local, fora do versionamento; obter pelo DOI) |
| **Fichado por** | André Solano Ferreira Rodrigues Maiolini |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-06 |
| **Por que ler** | Leitura obrigatória antes de usar o CWRU. É a auditoria registro a registro que fundamenta `docs/arquivos_excluidos.md`. |

### Convenções

- `>` **Citação direta**, sempre seguida de *(p. N, tradução nossa)*. O artigo está em
  inglês. Pela NBR 10520, a tradução feita pelo grupo precisa ser declarada.
- Texto corrido: **paráfrase/resumo** do grupo.
- **→ Projeto:** implicação para o nosso trabalho (decisão, risco, item de discussão).
- **Paginação:** as páginas citadas são as do PDF *in press* (1–32). A versão final ocupa
  as p. 100–131. **Conversão conferida (2026-10-10): página publicada = página do PDF
  + 99** (ex.: p. 3 → p. 102). O relatório e o código usam a numeração publicada.

---

## Resumo em cinco pontos

1. Os autores aplicam três métodos consagrados, todos baseados no **espectro do envelope
   ao quadrado**, a **todos os 161 registros** do CWRU. Cada registro é classificado em
   seis categorias de diagnóstico (Y1/Y2, P1/P2, N1/N2).
2. **Poucos registros mostram os sintomas clássicos** do defeito declarado. Muitos são
   dominados por outros fenômenos, sobretudo **folga mecânica**.
3. **A montagem pesa mais que o tamanho do defeito ou a carga.** Cada combinação de
   tipo e diâmetro de defeito foi uma montagem diferente do rolamento, e o
   comportamento do sinal acompanha a montagem.
4. A **"carga" do motor quase não carrega o rolamento.** O único efeito relevante é
   reduzir a rotação em até ~4%.
5. Os **defeitos de esfera são os mais difíceis**. Vários registros não são
   diagnosticáveis por nenhum método, e há indícios de defeitos não intencionais nas
   pistas.

---

## 1. Introdução

> "Rolamentos de elementos rolantes (REBs) estão entre os componentes mais presentes em
> máquinas rotativas, e sua falha é uma das razões mais frequentes de parada de
> máquinas. Isso motivou muita pesquisa sobre diagnóstico de REBs baseado em vibração
> nas últimas décadas [...]" (p. 2, tradução nossa)

> "O conjunto de dados fornecido pelo *Case Western Reserve University* (CWRU) *Bearing
> Data Center* tornou-se essa referência padrão no campo de diagnóstico de rolamentos
> [...]" (p. 2, tradução nossa)

Os autores contaram 41 artigos na MSSP que usam o CWRU entre 2004 e o início de 2015.
Mesmo assim, não existia um *benchmark* contra o qual comparar os algoritmos novos. O
artigo se propõe a preencher essa lacuna (p. 2).

**→ Projeto:** é a justificativa de por que este artigo, e não o site do CWRU sozinho,
é a base da nossa auditoria de arquivos.

## 2. Fundamentos de diagnóstico de rolamentos

> "Falhas localizadas em rolamentos de elementos rolantes produzem uma série de
> respostas impulsivas de banda larga no sinal de aceleração, à medida que os
> componentes do rolamento atingem repetidamente a falha." (p. 2, tradução nossa)

> "A principal ferramenta da maioria das técnicas de diagnóstico de rolamentos é o
> espectro do envelope, que revela a frequência de repetição dessa série de respostas
> impulsivas [...] bem como a natureza de qualquer modulação [...]" (p. 2, tradução
> nossa)

A modulação tem duas origens: a passagem do defeito pela zona de carga e a variação do
caminho de transmissão até o sensor (p. 2, citando McFadden e Smith, 1984).

### Frequências características (p. 3)

Com $f_r$ a rotação do eixo, $n$ o número de elementos rolantes, $d$ o diâmetro do
elemento, $D$ o diâmetro primitivo e $\phi$ o ângulo de contato:

$$\text{BPFO} = \frac{n f_r}{2}\left(1 - \frac{d}{D}\cos\phi\right) \qquad
\text{BPFI} = \frac{n f_r}{2}\left(1 + \frac{d}{D}\cos\phi\right)$$

$$\text{FTF} = \frac{f_r}{2}\left(1 - \frac{d}{D}\cos\phi\right) \qquad
\text{BSF} = \frac{D f_r}{2d}\left[1 - \left(\frac{d}{D}\cos\phi\right)^2\right]$$

- As fórmulas são cinemáticas e supõem que não há escorregamento. Na prática quase
  sempre há, e **um desvio de 1–2% em relação ao valor calculado é comum** (p. 3).
- Identidade útil: $\text{BPFO} = n \cdot \text{FTF}$ e
  $\text{BPFI} = n(f_r - \text{FTF})$. Logo **BPFO + BPFI = $n f_r$, qualquer que seja o
  escorregamento** (p. 10).

**Tabela 2 (p. 4): rolamento DE, SKF 6205-2RS JEM, em múltiplos de $f_r$:**

| BPFI | BPFO | FTF | BSF | $n$ |
|---|---|---|---|---|
| 5,415 | 3,585 | 0,3983 | 2,357 | 9 (p. 10) |

Exemplo calculado pelo grupo a 1797 rpm ($f_r$ = 29,95 Hz): BPFI ≈ 162,2 Hz,
BPFO ≈ 107,4 Hz, BSF ≈ 70,6 Hz, FTF ≈ 11,9 Hz.

### O que esperar no espectro do envelope (Tabela 1, p. 4)

| Defeito | Componentes esperados |
|---|---|
| Pista externa | BPFO e harmônicos, **sem** bandas laterais |
| Pista interna | BPFI e harmônicos, bandas laterais espaçadas de $f_r$; harmônicos de $f_r$ |
| Esfera | BSF e harmônicos (pares costumam dominar), bandas laterais espaçadas de FTF; harmônicos de FTF |

**→ Projeto:** a Tabela 2 vai direto para o notebook, sem recalcular a geometria.
A tolerância de 1–2% define a largura da janela de busca em torno de cada frequência
teórica. Já a Tabela 1 é o critério para dizer se um pico de envelope "confirma" a
classe, e é o argumento físico para priorizar.

## 3. Setup experimental (p. 3–4)

- Motor de 2 hp (Reliance Electric), transdutor de torque/encoder e dinamômetro.
- Defeitos de 0,007" a 0,028" (0,18 a 0,71 mm) induzidos por eletroerosão. O rolamento
  DE é SKF 6205-2RS JEM; o FE é SKF 6203-2RS JEM. Os defeitos de 0,028" usam um
  equivalente NTN.
- Aceleração medida na **vertical**, na carcaça do DE e, em alguns ensaios, também no
  FE e na base (BA).
- **Tabela A1 (p. 27): "48 k normal baseline data; $f_s$ = 48 kHz".** Os registros
  normais 97–100 estão a 48 kHz e só têm os canais DE e FE.
- **Tabela A2 (p. 27): os dados de falha DE a 12 kHz têm DE, FE e BA.** Os números de
  registro coincidem com os do nosso `data/raw/manifesto.csv`.
- Em teoria, a única carga radial no rolamento é a **carga gravitacional estática** do
  eixo. Há porém indícios de uma carga dinâmica sobreposta (p. 4).

**→ Projeto:** a Tabela A1 confirma, por fonte independente, o que medimos nos arquivos
(seção 1 de `data/raw/README.md`). Os normais precisam ser decimados para 12 kHz antes
de qualquer comparação com as falhas.

## 4. Uso dos dados do CWRU na literatura (p. 5)

> "[...] muitos artigos ignoram que 'carga', aqui, é praticamente sem significado, uma
> vez que não há mecanismo (por exemplo, engrenagens) que converta o torque em carga
> radial suportada pelos rolamentos. O principal efeito da carga do motor é sobre a
> rotação do eixo, que cai quase 4% no caso de carga máxima [...]" (p. 5, tradução
> nossa)

> "[...] a única carga radial nos rolamentos (em teoria) é a carga gravitacional
> estática, atuando na posição de 6 horas (e não na de 3 horas, como afirmado em uma
> seção do site do CWRU e em vários artigos)." (p. 5, tradução nossa)

> "A maioria dos estudos com os dados do CWRU parece produzir classificações não físicas
> a partir de algoritmos de aprendizado de máquina [...]. Como esses algoritmos não
> identificam características físicas em si — e sim variações em relação a alguma linha
> de base —, permanece a dúvida sobre a aplicabilidade mais ampla de alguns dos métodos
> desenvolvidos [...]" (p. 5, tradução nossa)

Os autores também criticam artigos que **não informam quais registros e pontos de
medição usaram**, o que torna impossível avaliar o método (p. 5).

**→ Projeto:**
- Isso resolve a contradição do site oficial (seção 4 de `data/raw/README.md`): a zona
  de carga fica em **6 h**. As posições são @6 = centrada na zona de carga, @3 =
  ortogonal, @12 = oposta.
- O nosso split por carga (treino 0–2 HP, teste 3 HP) **testa generalização para uma
  mudança de ~4% na rotação, não para uma carga radial diferente**. Ver a seção
  "Implicações" abaixo.
- A crítica às "classificações não físicas" é o argumento para o projeto mostrar que o
  pico do envelope cai na frequência teórica, e não só reportar acurácia.

## 5. Métodos de diagnóstico aplicados (p. 5–6)

> "Todos os métodos usaram o espectro do envelope ao quadrado [...] como ferramenta final
> de diagnóstico, mas com diferentes etapas de pré-processamento antes da obtenção do
> sinal de envelope." (p. 5, tradução nossa)

O protocolo é **incremental**. O Método 1 é aplicado a todos os registros, e os Métodos
2 e 3 só entram quando o resultado do Método 1 fica em P1 ou abaixo (p. 5 e 7).

### Método 1 — Envelope do sinal bruto

> "[...] não há fontes óbvias de mascaramento neste caso e, de fato, muitos defeitos de
> rolamento mostraram-se facilmente diagnosticáveis com este método. Nesses casos, os
> sinais não são muito exigentes em termos de poder de diagnóstico e não constituem um
> bom teste para algoritmos novos [...]" (p. 5, tradução nossa)

### Método 2 — Pré-branqueamento cepstral (*cepstrum prewhitening*, CPW)

Tem duas etapas: (1) o CPW iguala a magnitude de todas as componentes de frequência;
(2) faz-se o envelope do sinal em banda larga. A ideia é que, com todas as bandas na
mesma densidade espectral, **as bandas mais impulsivas passam a dominar** o sinal no
tempo. As ressonâncias também são removidas, o que reduz o mascaramento das bandas com
informação de falha por bandas sem essa informação (p. 5). Foi proposto por Sawalhi e
Randall (2011) e aplicado a velocidade variável por Borghesani *et al.* (2013).

### Método 3 — Método de referência (*benchmark*)

Tem três etapas: (1) **separação discreto/aleatório (DRS)**, que remove as componentes
determinísticas; (2) **curtose espectral (*Fast Kurtogram*, Antoni 2007)**, que escolhe
a banda mais impulsiva para um filtro passa-banda; (3) envelope do sinal filtrado (p. 5).

> "A separação [...] foi realizada utilizando a DRS [...], que se baseia na função de
> transferência entre o sinal e uma versão atrasada dele próprio. Idealmente, essa função
> seria unitária nas frequências das componentes discretas, uma vez que elas permanecem
> correlacionadas independentemente do atraso. As componentes aleatórias tornam-se menos
> correlacionadas à medida que o atraso aumenta [...]" (p. 5, tradução nossa)

Parâmetros da DRS, ajustados por tentativa e erro: **N = 16384 e Δ = 500 amostras para
os dados de 12 kHz**; N = 8192 e Δ = 500 para os de 48 kHz (p. 6).

**→ Projeto:** se quisermos ir além do envelope simples, o **CPW é o melhor custo-benefício**
(ver seção 6.6). É simples de implementar e teve o melhor desempenho geral. Já temos as
duas referências mínimas para ele: Sawalhi e Randall (2011) e Borghesani *et al.* (2013).

## 6. Resultados e discussão

### 6.1 Observações gerais (p. 6–7)

**Componentes discretas em alta frequência.** Têm duas causas:

1. **Harmônicos muito altos da rotação**, proeminentes em 11–14 kHz nos dados de 48 kHz.
   A causa provável é folga mecânica.
2. **Interferência eletromagnética (EMI) do controlador do dinamômetro.** Aparecem
   portadoras em múltiplos de **~4,2 kHz**, com bandas laterais espaçadas de $f_r$ ou um
   pouco menos. O espaçamento depende do escorregamento do dinamômetro, que **cresce com
   a carga** (máximo de ~0,9% a 3 hp).

**Problemas de aquisição (Tabela 3, p. 7):**

| Problema | Registros | No nosso subconjunto? |
|---|---|---|
| Trechos de ruído elétrico | 177, 283 | não (48 kHz e FE) |
| DE e FE idênticos a menos de um fator ~1,0154 | 189, 201, 213, 226, 238 | não (48 kHz) |
| Trechos saturados (*clipped*) | 191DE, 214DE, 215DE, 228DE, 229DE, **236DE, 237DE** | **sim: 236 e 237** (OR 0,021" @6, 2 e 3 HP) |

**→ Projeto:**
- A EMI em ~4,2 kHz cai **dentro da banda dos nossos dados de 12 kHz** (Nyquist em
  6 kHz). Como o espaçamento das bandas laterais muda com a carga, features espectrais
  nessa região podem carregar um artefato correlacionado com a carga e não com o
  defeito. É candidato a explicar erros no teste em 3 HP.
- O registro **237 é de 3 HP, ou seja, está no conjunto de teste**. Precisa ser declarado
  na auditoria.

### 6.2 Categorias de diagnóstico (Tabela 4, p. 8)

| Categoria | Sucesso | Significado |
|---|---|---|
| Y1 | sim | Diagnosticável, com características **clássicas** no tempo e na frequência |
| Y2 | sim | Diagnosticável, mas com características **não clássicas** |
| P1 | parcial | Provavelmente diagnosticável: há componentes na frequência esperada, mas não dominantes |
| P2 | parcial | Potencialmente diagnosticável: há componentes "borrados" que parecem coincidir com o esperado |
| N1 | não | Não diagnosticável para o defeito declarado, mas com **outro problema identificável** (por exemplo, folga) |
| N2 | não | Não diagnosticável e praticamente indistinguível de ruído |

> "[...] os resultados de diagnóstico parecem ser menos função do tamanho do defeito ou
> da velocidade/carga e mais função da montagem, que presumivelmente era a mesma para
> cada tamanho de defeito, mas mudava entre tamanhos quando um novo rolamento era
> instalado." (p. 8, tradução nossa)

### 6.3 Falhas no DE a 12 kHz: o nosso subconjunto (Tabela B2, p. 29)

**Pista interna (p. 8–9).** Os registros 209–212 (0,021") são o caso clássico (Y1),
com BPFI, bandas laterais em $f_r$ e modulação periódica na rotação. Já 169–172
(0,014") têm curtose de ~18 a 22 e pulsos com **modulação impulsiva na rotação**, que os
autores atribuem a folga, mas o envelope ainda acerta o diagnóstico (Y2).

**Esfera (p. 9–11)**, o caso mais difícil:
- No 0,007" (118–121), o envelope mostra tudo em harmônicos de 0,2 $f_r$. A hipótese é
  que o escorregamento "travou" a FTF em 0,4 $f_r$. A **BSF não é identificável** (N1).
- No 0,014" e no 0,021", os componentes de BSF aparecem "borrados" por uma **modulação de
  amplitude aleatória e impulsiva**, e não por escorregamento (p. 11).
- Vários registros de esfera mostram **BPFO e BPFI discretos**. A hipótese é de defeitos
  não intencionais nas pistas, possivelmente por *brinelling* na montagem (p. 10–11).

**Pista externa @6, centrada na zona de carga (p. 11–14).** Os registros 130–133
(0,007") são os **únicos Y1 clássicos** do grupo. Os de 0,014" (197–200) **quase não são
diagnosticáveis**, com pulsos aleatórios atribuídos a folga. Os de 0,021" (234–237) têm
BPFO claro, mas com bandas laterais fortes em $f_r$ (Y2).

**Pista externa @3, ortogonal (p. 14).** Todos são diagnosticáveis com o Método 1, com
modulação por $f_r$ e/ou FTF. Os de 0,021" (246–249) também mostram harmônicos de
0,2 $f_r$.

**Pista externa @12, oposta (p. 14–15).** **Em teoria não deveria haver resposta**, porque
fora da zona de carga não há contato com o defeito. Mesmo assim, o BPFO aparece em
todos os casos. Conclusão dos autores: **a zona de carga não é fixa**, ela se move com o
eixo, o que é coerente com folga mecânica. Os de 0,021" (258–261) têm curtose de 33 a 35.

#### Resumo por registro, canal DE (o que usamos)

"Melhor DE" é a melhor categoria obtida no canal DE entre os três métodos, lida da
Tabela B2. Entre parênteses, o método que a atingiu quando não foi o M1.

| Classe | Diâm. | 0 HP | 1 HP | 2 HP | 3 HP (teste) | Curtose DE |
|---|---|---|---|---|---|---|
| IR | 0,007" | 105: Y2 | 106: Y2 | 107: Y2 | 108: Y2 | 5,3–5,6 |
| IR | 0,014" | 169: Y2 | 170: Y2 | 171: Y2 (M2) | 172: Y2 | 18–22 |
| IR | 0,021" | 209: Y1 | 210: Y1 | 211: Y1 | 212: Y1 | 7,5–8,4 |
| B | 0,007" | **118: N** | **119: N** | **120: N** | 121: Y2 (M3) | 2,8–3,0 |
| B | 0,014" | 185: P2 | 186: P2 | 187: P2 (M2) | 188: P2 | 8,8–17,8 |
| B | 0,021" | 222: Y2 (M2) | 223: Y2 | **224: N** | **225: N** | 3,1–9,4 |
| OR @6 | 0,007" | 130: Y1 | 131: Y1 | 132: Y1 | 133: Y1 | 7,6–8,0 |
| OR @6 | 0,014" | 197: Y2 (M3) | 198: P2 | 199: P1 | **200: N** | 2,9–3,8 |
| OR @6 | 0,021" | 234: Y2 | 235: Y2 | 236: Y2 ✂ | 237: Y2 ✂ | 21–23,5 |
| OR @3 | 0,007" | 144: Y2 | 145: Y2 | 146: Y2 | 147: Y2 | 3,9–4,2 |
| OR @3 | 0,021" | 246: Y2 | 247: Y2 | 248: Y2 | 249: Y2 | 6,4–7,1 |
| OR @12 | 0,007" | 156: Y1 (M2) | 158: Y2 | 159: Y2 | 160: Y2 | 8,0–8,7 |
| OR @12 | 0,021" | 258: Y2 | 259: Y2 | 260: Y2 | 261: Y2 | 33–35 |
| Normal | — | 97 | 98 | 99 | 100 | 2,76–2,96 (Tab. B1) |

**N** = não diagnosticável no DE por nenhum método. ✂ = saturação (Tabela 3).

- **Inconsistência interna do artigo:** a Tabela 5 (p. 26) dá Y1 com o Método 2 para
  144DE–147DE, 159DE e 160DE, mas a Tabela B2 não traz resultado de M2 para esses
  registros. Na tabela acima vale a B2.
- No canal DE, **6 registros são N** (118, 119, 120, 224, 225, 200) e **6 são P**
  (185, 186, 187, 188, 198, 199). Esses são os candidatos naturais para
  `docs/arquivos_excluidos.md`. A decisão de excluir ou só marcar é do grupo; ver
  pendências.

### 6.4 e 6.5 DE a 48 kHz e FE a 12 kHz (p. 15–23): fora do escopo

Lidas por completude. Os padrões se repetem: esfera é o mais difícil, a montagem domina
e há folga. Um ponto interessante do FE: as frequências do 6203 ficam perto de múltiplos
inteiros de $f_r$ (BPFI ≈ 4,947, BPFO ≈ 3,053, BSF ≈ 1,994), o que gera batimentos e
exige cursores harmônicos precisos (p. 19–22).

### 6.6 Discussão (p. 23–24)

- No fim, os dados de 12 kHz e de 48 kHz tiveram desempenho de diagnóstico muito
  parecido.
- **O Método 2 (CPW) teve o melhor desempenho geral**, seguido de perto pelo Método 3.
- A curtose espectral (Método 3) é **vulnerável a ruído impulsivo**: tende a realçar
  impulsos isolados em vez de séries de transientes. Muitos registros do CWRU têm
  impulsos não relacionados ao defeito (p. 24).

### 6.7 Tabelas-resumo (p. 25–26)

> "Os conjuntos de dados da Tabela 5, com sintomas clássicos, podem ser úteis [...] ou
> podem ser considerados conjuntos de treino válidos para algoritmos de aprendizado de
> máquina. Por outro lado, os registros não diagnosticáveis da Tabela 6 podem constituir
> um teste robusto para qualquer algoritmo de diagnóstico novo." (p. 25, tradução nossa)

Tabela 6, DE a 12 kHz (não diagnosticáveis por nenhum método; sem sufixo, o
registro falha em todos os pontos de medição): esfera 118, 119, 120DE, 120BA, 121BA, 187FE, 224DE, 224BA, 225DE, 225FE;
OR centrada 197FE, 197BA, 198FE, 198BA, 199FE, 200; IR 3001–3004 (fora do nosso escopo).

## 7. Conclusões e recomendações (p. 25–26)

> "Uma conclusão central da análise foi que, em muitos casos, a montagem da bancada
> pareceu afetar os resultados de diagnóstico mais do que o próprio defeito, com
> evidência de folga mecânica observada em muitos dos conjuntos de dados." (p. 25,
> tradução nossa)

- Vários registros são **muito não estacionários**: o defeito aparece só em trechos do
  sinal (p. 25).
- O artigo recomenda **informar o número do registro e o ponto de medição** usados
  (p. 25).
- Para gerar dados novos, recomenda taxa de amostragem acima de ~40 kHz e referência
  angular (tacômetro ou encoder) quando a velocidade varia (p. 26).

---

## Verificações feitas nos nossos dados

Executadas em 2026-10-06 sobre `data/raw/`, com scripts descartáveis (não versionados):

- **Curtose do canal DE (momento normalizado, K = 3 para gaussiana)** dos 56 registros
  comparada às Tabelas B1 e B2: o **maior desvio relativo foi de 0,28%**. Os nossos
  arquivos são os mesmos que o artigo analisou.
- **Saturação:** 236DE e 237DE têm 7 e 5 amostras, respectivamente, no teto de
  ±6,65. O 234DE encosta nesse mesmo valor uma vez, mas não aparece na Tabela 3.
- **Taxa dos normais:** a Tabela A1 confirma os 48 kHz que medimos pela linha de
  120 Hz.

## Implicações para o projeto

| # | Achado do artigo | Implicação | Onde agir |
|---|---|---|---|
| 1 | A montagem domina; cada (tipo × diâmetro) foi **uma** montagem, usada nas quatro cargas (p. 8, 25) | **O split por carga não separa montagens.** O registro de teste em 3 HP é a mesma montagem física dos de treino em 0–2 HP, então o modelo pode reconhecer a assinatura da montagem em vez do defeito. É vazamento de outro tipo, que a regra de split por carga não cobre. | Discussão do grupo; ver pendência 1 |
| 2 | A "carga" só reduz a rotação em ~4% (p. 5) | O split por carga mede robustez a uma pequena variação de velocidade, não a uma condição de carga nova. O relatório deve dizer isso explicitamente. | `docs/relatorio/secoes/04-metodologia.tex`, `06-discussao.tex` |
| 3 | Os normais estão a 48 kHz (Tab. A1) | Decimar para 12 kHz no carregador | o notebook |
| 4 | Zona de carga em 6 h; o site erra em uma seção (p. 5) | @6 = centrada, @3 = ortogonal, @12 = oposta. Usar isso na decisão sobre a pista externa. | `data/raw/README.md`, issue da posição OR |
| 5 | Registros N/P no DE (seção 6.3 acima); 236/237 saturados | Insumo direto da auditoria | `docs/arquivos_excluidos.md` |
| 6 | Esfera de 0,007" (118–120) e de 0,021" (224–225) não são diagnosticáveis | Se o classificador acertar esses registros, **desconfiar**: ele pode estar usando algo que não é o defeito (montagem, EMI). Se errar, a explicação física já está aqui. | Análise de erros (regra 8) |
| 7 | Defeitos não intencionais nas pistas em registros de esfera (p. 10–11) | Confusão B → OR/IR pode ser fisicamente justificada, não erro do modelo | Discussão da matriz de confusão |
| 8 | Não estacionariedade: o defeito aparece em trechos (p. 25) | Janelas curtas podem não conter evidência do defeito, o que vira ruído de rótulo no nível da janela | Escolha da janela (regra 6), análise de erros |
| 9 | Tabelas 1 e 2 e tolerância de 1–2% | Features físicas: amplitude do envelope em BPFO/BPFI/BSF ± 2% | o notebook |
| 10 | EMI em ~4,2 kHz dependente da carga (p. 6–7) | Possível atalho espúrio no teste em 3 HP | Análise de erros, importância de features |
| 11 | CPW foi o melhor método; a curtose espectral sofre com ruído impulsivo (p. 23–24) | Candidato para a etapa de envelope, com referências já disponíveis | Fundamentação |

## Pendências e dúvidas 

1. **Split por montagem.** Vale rodar, **além** do split por carga, um split que deixe um
   diâmetro inteiro de fora (por exemplo, treinar em 0,007" e 0,021" e testar em
   0,014")? Isso cruza montagens e testa se o modelo aprendeu o defeito. O custo é
   pequeno, e o contraste entre os dois splits é material forte de discussão crítica.
   Há trabalhos posteriores que discutem exatamente esse vazamento no CWRU, mas eles
   **ainda não foram verificados** e precisam ser lidos antes de serem citados.
2. **Excluir ou marcar?** Os registros N no DE podem sair do treino e do teste, ou
   ficar e ser analisados à parte como "casos sem evidência física". A segunda opção
   rende mais discussão e não esconde dificuldade.
3. **O detector one-class tem pouca linha de base.** Só existem 4 registros normais, um
   por carga. No split por carga, o treino tem 3 gravações normais e o **FPR é estimado
   numa única gravação** (100.mat). Isso precisa aparecer nas limitações.
4. Conferir a paginação na versão final publicada antes de citar.

## Referências do artigo a seguir

Candidatas à fundamentação das técnicas (o enunciado exige pelo menos duas por técnica):

| Técnica | Referências (numeração do artigo) |
|---|---|
| Envelope e modelo do sinal de falha | [1] Randall e Antoni (2011); [3] McFadden e Smith (1984), *J. Sound Vib.* 96, p. 69–82 |
| Pré-branqueamento cepstral | [6] Sawalhi e Randall (2011), COMADEM; [7] Borghesani *et al.* (2013), *MSSP* 36, p. 370–384 |
| Curtose espectral / kurtograma | [10] Antoni (2007), *MSSP* 21, p. 108–124; [14] Antoni (2014), ISMA |
| Separação discreto/aleatório | [9] Antoni e Randall (2004), *MSSP* 18, p. 103–117 |
