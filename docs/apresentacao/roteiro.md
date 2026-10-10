# Roteiro da apresentação (máx. 5 min)

Slides: [`slides.tex`](slides.tex) → `make` gera `build/slides.pdf`.

**Orçamento de tempo:** ~130 palavras por minuto em ritmo calmo. O texto abaixo
soma ~590 palavras, cerca de **4 min 35 s**, deixando ~25 s de folga para as
trocas de slide. Se um ensaio passar de 4 min 50 s, cortem primeiro as frases
marcadas com *(opcional)*.

| Integrante | Slides | Tema | Tempo |
|---|---|---|---|
| André | 1–2 | Abertura, problema, dados e protocolo | 0:00–1:00 |
| Durval | 3–4 | Limpeza dos dados e física do defeito | 1:00–2:05 |
| Leonardo | 5–6 | Validação física e detecção | 2:05–3:10 |
| Lucas | 7 | Classificação (roteiro das aulas) | 3:10–3:55 |
| Estevan | 8–9 | Teste com montagem nova e conclusões | 3:55–4:35 |

Todos os números são os do relatório (`results/metrics/`). Na fala, arredondar
para inteiro é aceitável (45,7% → 46%); nos slides ficam os valores exatos.

---

## André — slides 1 e 2 (≈ 60 s, ~125 palavras)

**[Slide 1 — título]**

> Olá! Somos o grupo do projeto de detecção e diagnóstico de defeitos em
> rolamentos. O título já adianta a nossa conclusão: neste dataset, alta acurácia
> é fácil — e diz pouco.

**[Slide 2]**

> Trabalhamos duas perguntas separadas. Detecção: o comportamento da máquina
> mudou? Aqui o modelo só pode ver sinais normais, como numa fábrica antes da
> primeira falha. E diagnóstico: qual é o defeito — pista interna, pista externa
> ou esfera?
>
> Os dados são do CWRU, a bancada da foto, com o acelerômetro do lado do
> acionamento. O protocolo foi a nossa maior preocupação: treinamos com as cargas
> de zero a dois HP e testamos em três, sem nunca dividir janelas da mesma
> gravação entre treino e teste. O Durval explica o que fizemos com os dados.

---

## Durval — slides 3 e 4 (≈ 65 s, ~135 palavras)

**[Slide 3]**

> Antes de qualquer modelo, os dados tinham uma armadilha: as gravações normais
> estão a 48 quilohertz, e as de falha a 12. Se misturássemos assim, o modelo
> separaria normal de falha pela taxa de amostragem. Então decimamos os normais
> por quatro, com filtro anti-aliasing. Ao conferir o espectro, achamos um resíduo
> de aliasing entre 4,8 e 6 quilohertz, e passamos todas as gravações pela mesma
> banda.

**[Slide 4]**

> Agora a física. Cada tipo de defeito gera impactos numa frequência própria,
> calculada pela geometria do rolamento e pela rotação. O espectro do envelope
> mostra essa repetição — vejam a pista externa, com o pico exatamente na linha
> prevista. *(opcional: a janela de 4096 amostras cobre três voltas da gaiola.)*
> Extraímos cinco features do tempo, como RMS e curtose, e três escores de
> envelope. O Leonardo mostra o que isso revelou.

---

## Leonardo — slides 5 e 6 (≈ 65 s, ~135 palavras)

**[Slide 5]**

> Antes de treinar qualquer coisa, verificamos gravação por gravação se o pico do
> envelope cai onde a teoria prevê. Na pista interna, sim, nas doze. Na pista
> externa, em oito de doze. E na esfera, em nenhuma. Isso concorda com a auditoria
> de referência de Smith e Randall em 50 de 52 gravações. Guardem esse zero da
> esfera.

**[Slide 6]**

> Na detecção, treinamos quatro detectores só com dados normais e obtivemos AUC
> de 1,00. Um resultado perfeito num problema real é suspeito. Conferimos o
> vazamento e não havia. A causa era outra: o RMS sozinho já dá AUC 1,00. Como
> mostra o gráfico, toda gravação de falha vibra mais que toda gravação normal —
> até as que não mostram defeito nenhum. Só com o envelope, o AUC cai, mas passa a
> seguir a física. Com o Lucas, a classificação.

---

## Lucas — slide 7 (≈ 45 s, ~100 palavras)

**[Slide 7]**

> Na classificação seguimos o roteiro das aulas: pipeline com StandardScaler,
> seleção de modelos por validação cruzada e GridSearch. A diferença é que a
> validação foi agrupada por carga, e não embaralhada, para não vazar janelas da
> mesma gravação.
>
> O Random Forest venceu e acertou 95,7% no teste; a CNN, 99,7%. Mas os dois
> acertam quase toda a esfera — a classe em que a física não encontrou o defeito.
> E, quando o defeito aparece em outra posição, a acurácia despenca para 40 e 64%.
> RMS e pico somam mais da metade da importância. O Estevan mostra o teste
> decisivo.

---

## Estevan — slides 8 e 9 (≈ 40 s, ~95 palavras)

**[Slide 8]**

> No CWRU, cada defeito foi ensaiado numa única montagem, repetida nas quatro
> cargas. Então treinamos em dois diâmetros e testamos no terceiro: uma montagem
> nunca vista. Todos os modelos caíram para perto do acaso — o Random Forest para
> 46%, a CNN para 50%. E uma regra física simples, sem treino nenhum, foi a
> melhor: 66%, e quase 100% na pista externa em outra posição.

**[Slide 9]**

> Conclusão: neste dataset os modelos aprendem amplitude e montagem, não o
> defeito. A física generaliza onde o aprendizado não generaliza. Código,
> notebook e relatório estão no repositório. Obrigado!

---

## Checklist de gravação

- [ ] Ensaiar com cronômetro; meta 4 min 35 s, limite **5 min**.
- [ ] Cada integrante aparece em vídeo ou áudio na sua parte.
- [ ] Gravar com os slides em tela cheia (`build/slides.pdf`).
- [ ] Subir no YouTube (pode ser "não listado") e colocar o link e o PDF dos
      slides na tabela de entregas do README (issue #34).
