# Dados brutos — CWRU Bearing Data Center

Arquivos `.mat` originais, sem nenhuma modificação, baixados em **2026-10-06** das
páginas oficiais do CWRU Bearing Data Center:

- [Apparatus & Procedures](https://engineering.case.edu/bearingdatacenter/apparatus-and-procedures)
- [Normal Baseline Data](https://engineering.case.edu/bearingdatacenter/normal-baseline-data)
- [12k Drive End Bearing Fault Data](https://engineering.case.edu/bearingdatacenter/12k-drive-end-bearing-fault-data)

O inventário completo, com classe, carga, rotação, nº de amostras e SHA-256 de cada
arquivo, está em [`manifesto.csv`](manifesto.csv). Para reproduzir o download
do zero e conferir a integridade:

```bash
python scripts/download_cwru.py               # baixa o que faltar e confere SHA-256
python scripts/download_cwru.py --manifesto   # regenera manifesto.csv a partir dos arquivos
```

Tamanho total: 179 MB (56 arquivos; o maior tem 15,5 MB). Isso fica abaixo do
limite de 100 MB por arquivo do GitHub, então **os dados ficam no próprio
repositório**, sem drive externo.

## Subconjunto baixado

Escopo: sensor drive end, 12 kHz, diâmetros 0.007", 0.014" e 0.021", cargas de
0 a 3 HP, mais a linha de base normal. Os defeitos de 0.028" (arquivos 3001–3008)
ficaram fora porque não estão no escopo do projeto. Além disso, nesse diâmetro os
rolamentos são NTN e não SKF, e não existe gravação de pista externa.

| Classe | Diâmetro | Posição (OR) | 0 HP | 1 HP | 2 HP | 3 HP | Arquivos |
|---|---|---|---|---|---|---|---|
| Normal | — | — | 97 | 98 | 99 | 100 | 4 |
| Pista interna (IR) | 0.007" | — | 105 | 106 | 107 | 108 | 4 |
| Esfera (B) | 0.007" | — | 118 | 119 | 120 | 121 | 4 |
| Pista externa (OR) | 0.007" | @6 | 130 | 131 | 132 | 133 | 4 |
| Pista externa (OR) | 0.007" | @3 | 144 | 145 | 146 | 147 | 4 |
| Pista externa (OR) | 0.007" | @12 | 156 | 158 | 159 | 160 | 4 |
| Pista interna (IR) | 0.014" | — | 169 | 170 | 171 | 172 | 4 |
| Esfera (B) | 0.014" | — | 185 | 186 | 187 | 188 | 4 |
| Pista externa (OR) | 0.014" | @6 | 197 | 198 | 199 | 200 | 4 |
| Pista interna (IR) | 0.021" | — | 209 | 210 | 211 | 212 | 4 |
| Esfera (B) | 0.021" | — | 222 | 223 | 224 | 225 | 4 |
| Pista externa (OR) | 0.021" | @6 | 234 | 235 | 236 | 237 | 4 |
| Pista externa (OR) | 0.021" | @3 | 246 | 247 | 248 | 249 | 4 |
| Pista externa (OR) | 0.021" | @12 | 258 | 259 | 260 | 261 | 4 |

**Arquivos por classe:** normal 4 · IR 12 · B 12 · OR 28 (12 em @6, 8 em @3,
8 em @12). Total: 56. A página oficial marca como "data not available" as
posições @3 e @12 para 0.014". O desbalanceamento em OR depende da posição
escolhida (issue sobre a posição do defeito em pista externa).

Rotação aproximada pela tabela oficial: 1797 / 1772 / 1750 / 1730 rpm para
0 / 1 / 2 / 3 HP. A rotação medida, quando o arquivo traz a variável `XnnnRPM`,
está no manifesto e varia alguns rpm em torno do valor nominal.

Cada arquivo de falha traz três canais: `XnnnDE_time` (drive end, o que usamos),
`XnnnFE_time` (fan end) e `XnnnBA_time` (base). Os arquivos normais não têm `BA`.

## Inconsistências encontradas — ler antes de usar

### 1. Os arquivos normais estão a 48 kHz, não a 12 kHz

A página *Apparatus & Procedures* diz que os dados foram coletados a 12 kHz e,
para falhas no drive end, também a 48 kHz. A página *Normal Baseline Data* não
declara a taxa. Os arquivos mostram o seguinte:

| | Normais (97–100) | Falhas (105–261) |
|---|---|---|
| Amostras no canal DE | 243 938 a 485 643 | 121 265 a 122 917 |
| Duração se lidos a 12 kHz | 20 a 40 s | ≈ 10 s |
| Duração se lidos a 48 kHz | 5 a 10 s | ≈ 2,5 s |
| Linha de 120 Hz (2× a rede de 60 Hz) cai em 120,0 Hz quando lido a | **48 kHz** | **12 kHz** |

A linha de 120 Hz vem da alimentação elétrica, não depende da carga e funciona
como régua independente. Nos quatro normais ela aparece em 119,83 a 120,03 Hz
quando o sinal é lido a 48 kHz. A 12 kHz o pico mais próximo varia de forma
errática entre 112 e 130 Hz.

Smith e Randall (2015, Tabela A1) confirmam de forma independente: *"48 k normal
baseline data; fs = 48 kHz"*. Ver [`docs/records/smith2015.md`](../../docs/records/smith2015.md).

**Consequência:** antes de qualquer comparação com as falhas, os normais precisam
ser **decimados de 48 kHz para 12 kHz (fator 4, com filtro anti-aliasing)**. Se
forem misturados sem isso, todo o conteúdo espectral do normal fica comprimido 4×,
e um detector separa normal de falha pela taxa de amostragem, não pela falha. A
correção é feita na leitura dos dados, no notebook. É também material para a discussão crítica e
deve ser conferida contra a auditoria de Smith & Randall (2015).

### 2. `99.mat` contém as variáveis de `98.mat`

`99.mat` traz `X098_DE_time` e `X098_FE_time`, idênticos bit a bit aos de
`98.mat`, além de `X099_*` e de uma variável espúria `ans`. **O carregador tem
que ler a variável pelo número do arquivo** (`X099_DE_time`), nunca "a primeira
chave que termina em `DE_time`".

### 3. `98.mat` e `99.mat` não têm a variável de rotação

Nesses dois casos vale só a rotação nominal da tabela (1772 e 1750 rpm). O
`97.mat` registra 1796 rpm e o `100.mat`, 1725 rpm.

### 4. Posição do defeito em pista externa: a documentação se contradiz

- O cabeçalho da tabela de 12 kHz diz *"Load Zone Centered at 6:00"* e chama @6 de
  *Centered*, @3 de *Orthogonal* e @12 de *Opposite*.
- O texto de *Apparatus & Procedures* diz o contrário para 3 e 6 horas:
  *"3 o'clock (directly in the load zone), at 6 o'clock (orthogonal to the load
  zone)"*.

**Resolução:** Smith e Randall (2015, p. 5) afirmam que a única carga radial é a
gravitacional, atuando em **6 horas**, *"not the 3.00 o'clock position, as stated in
one section of the CWRU website"*. Vale portanto a tabela: **@6 = centrada na zona de
carga, @3 = ortogonal, @12 = oposta**. Os arquivos e o manifesto mantêm o rótulo
numérico da tabela. Ao declarar a posição escolhida no relatório, citar a contradição
do site e a resolução pelo artigo.

### 5. Saturação em 236 e 237

Smith e Randall (2015, Tabela 3) apontam trechos saturados (*clipped*) em 236DE e
237DE (OR 0,021" @6, 2 e 3 HP). Conferido aqui: 7 e 5 amostras no teto de ±6,65. O
237 é de 3 HP, ou seja, está no conjunto de teste. Tratamento a definir na auditoria
(`docs/arquivos_excluidos.md`).

### Conferência com a literatura

A curtose do canal DE dos 56 arquivos reproduz as Tabelas B1 e B2 de Smith e Randall
(2015), com desvio máximo de 0,28%. Os arquivos são os mesmos analisados no artigo.
