# TDE2 · Busca Competitiva · Lig 4 (ID2.3)

Agente alfa-beta para o Lig 4 (Connect Four, 6 linhas × 7 colunas) e avaliação do seu desempenho contra outros agentes, conforme o indicador ID2.3.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `lig4.py` | Jogo (estado com jogador da vez, ações, resultado, teste terminal, utilidade do ponto de vista de MAX), Minimax, alfa-beta, agentes. Executado diretamente, roda uma partida ao vivo com o contador de nós visível |
| `verificar.py` | Minimax e alfa-beta em profundidade completa numa instância pequena: os valores devem ser idênticos |
| `experimento.py` | Protocolo do ID2.3. Gera `partidas.csv`, `lances.csv` e `resultados.md` |

Requer apenas Python 3, sem bibliotecas externas.

```
python3 verificar.py        # ~10 s, saída em verificacao.txt
python3 experimento.py      # ~90 s
python3 lig4.py 6 3         # demonstração: AlfaBeta(d=6) x AlfaBeta(d=3), nós por lance na tela
```

## Agente avaliado

- **Busca:** alfa-beta com **profundidade fixa d = 6** (mecanismo de parada). Nos nós de corte, usa a função de avaliação.
- **Ordenação de jogadas:** colunas do centro para as bordas (3, 2, 4, 1, 5, 0, 6). Isso também define o desempate.
- **Avaliação (do ponto de vista de MAX):** para cada janela de 4 casas sem peça adversária, 3 peças valem +5 e 2 peças valem +2 (simétrico para MIN), e cada peça na coluna central vale ±3. Os pesos foram fixados a priori e **não foram calibrados**.
- **Utilidade terminal:** vitória de MAX = +(10⁶ + casas vazias), vitória de MIN = −(10⁶ + casas vazias), empate = 0. É um único número, do ponto de vista de MAX, e o bônus por casas vazias faz o agente preferir vencer mais cedo.

## Verificação de corretude (pré-requisito)

`verificar.py` usa um tabuleiro 4×5 (4 em linha) e 30 posições geradas por 10 lances aleatórios (semente 2026), com Minimax e alfa-beta em profundidade completa.

- **Valores idênticos: 30/30.** Os valores verdadeiros incluem 10 vitórias de MAX, 13 empates e 7 vitórias de MIN. Instâncias com valores variados são necessárias porque, se todos os valores fossem 0, um alfa-beta que poda demais também passaria no teste.
- Nós visitados: Minimax 1.157.447, alfa-beta 57.953 (5,0%).

## Protocolo experimental (seção 4 da ficha)

| Item | Decisão |
|---|---|
| **Adversários** | (1) **Aleatório**: escolhe uma jogada legal com probabilidade uniforme (linha de base trivial). (2) **AlfaBeta(d=3)**: o próprio agente, com a mesma avaliação e a mesma ordenação, mas profundidade menor |
| **Unidade de custo** | **Nós visitados**: cada chamada da busca conta 1, incluindo a raiz. O Aleatório não faz busca, então seu custo é 0 nós. Não são medidos tempo nem gerações |
| **Partidas** | 98 por confronto, 196 no total |
| **Aberturas** | As 7 × 7 = **49 aberturas de 2 lances**, todas enumeradas (sem sorteio). Os 2 lances são impostos e não contam como lances dos agentes |
| **Quem começa** | Cada abertura é jogada **duas vezes, trocando quem é o primeiro jogador**. Isso evita a armadilha de dois agentes determinísticos repetirem a mesma partida |
| **Semente** | O Aleatório da partida *i* usa a semente 2026 + *i*. Os alfa-beta são determinísticos. Duas execuções geram CSVs idênticos (conferido por md5) |
| **Calibração** | **Simétrica, sem calibração em nenhum lado**: os dois alfa-beta compartilham a avaliação, a ordenação e os pesos. Só a profundidade difere, e ela é a variável do experimento. As profundidades 6 e 3 foram escolhidas antes de rodar, por orçamento computacional, sem varrer configurações |
| **Métricas** | V/E/D com taxa de vitória e intervalo de 95% (Wilson), separados por lado. Nós por lance: média, desvio-padrão, mediana, P95 e máximo (pior caso). Nós por partida. Duração das partidas |

## Resultados

Resultados do AlfaBeta(d=6), com V/E/D do ponto de vista do agente avaliado:

| Confronto | Lado do agente | Partidas | V | E | D | Taxa de vitória | IC 95% (Wilson) |
|---|---|---|---|---|---|---|---|
| × Aleatório | 1º a jogar | 49 | 49 | 0 | 0 | 100,0% | [92,7%, 100,0%] |
| × Aleatório | 2º a jogar | 49 | 49 | 0 | 0 | 100,0% | [92,7%, 100,0%] |
| × Aleatório | ambos | 98 | 98 | 0 | 0 | 100,0% | [96,2%, 100,0%] |
| × AlfaBeta(d=3) | 1º a jogar | 49 | 39 | 6 | 4 | 79,6% | [66,4%, 88,5%] |
| × AlfaBeta(d=3) | 2º a jogar | 49 | 41 | 4 | 4 | 83,7% | [71,0%, 91,5%] |
| × AlfaBeta(d=3) | ambos | 98 | 80 | 10 | 8 | 81,6% | [72,8%, 88,1%] |

Custo em nós visitados por lance:

| Confronto | Agente | Lances | Média | DP | Mediana | P95 | Máximo | Nós/partida |
|---|---|---|---|---|---|---|---|---|
| × Aleatório | AlfaBeta(d=6) | 483 | 2.652 | 2.767 | 2.076 | 6.497 | 33.441 | 13.069 |
| × Aleatório | Aleatório | 434 | 0 | 0 | 0 | 0 | 0 | 0 |
| × AlfaBeta(d=3) | AlfaBeta(d=6) | 1.214 | 2.206 | 3.476 | 1.652 | 6.345 | 61.915 | 27.333 |
| × AlfaBeta(d=3) | AlfaBeta(d=3) | 1.179 | 85 | 47 | 84 | 164 | 237 | 1.020 |

Duração média das partidas: 11,4 plies contra o Aleatório (de 7 a 24) e 26,4 plies contra o d=3 (de 7 a 42).

## Análise

- **Contra a linha de base trivial**, o agente venceu as 98 partidas, com média de 11,4 plies por partida. Isso confirma que o agente supera a linha de base, mas um adversário tão fraco discrimina pouco. Por isso o confronto informativo é o seguinte.
- **Contra o próprio agente com d=3**, o d=6 vence 81,6% (IC 95% de 72,8% a 88,1%) e, no pior caso, perde 8 de 98 partidas (4 de cada lado). O lado em que começa quase não altera o resultado: 79,6% como primeiro e 83,7% como segundo, com intervalos sobrepostos.
- **O preço da vantagem, na mesma unidade:** o d=6 visita em média 2.206 nós por lance, contra 85 do d=3, cerca de 26 vezes mais. A distribuição tem cauda longa: a mediana é 1.652, mas o pior lance custou 61.915 nós, 28 vezes a média. Por isso a média sozinha não descreve o custo.
- **De onde vem a vantagem:** 16 das 80 vitórias terminam em 7 plies, todas com o d=6 começando. Reproduzindo uma delas, o d=3 não bloqueia três peças abertas na linha de baixo: a ameaça dupla só aparece a 4 plies, além do seu horizonte de 3.

## O que não funcionou e garantias ausentes

- **O agente não é ótimo.** O Lig 4 6×7 é um jogo resolvido, em que o primeiro jogador vence com jogo perfeito. Ainda assim, o d=6 perdeu 4 partidas começando e 4 jogando em segundo contra um adversário mais fraco. Essas 8 derrotas foram longas (26 a 40 plies). A hipótese, **não verificada** partida a partida, é efeito horizonte: uma ameaça a mais de 6 plies que a avaliação não enxerga.
- **A corretude do alfa-beta foi verificada por amostra, não provada.** Os valores foram iguais em 30 posições do tabuleiro 4×5 em profundidade completa. O código é o mesmo no 6×7 com corte, mas no tabuleiro real não houve comparação em profundidade completa, que é inviável.
- **A avaliação não foi calibrada.** Os pesos 5/2/3 são intuitivos, não ajustados, e nada garante que sejam bons. Isso vale igualmente para os dois alfa-beta, então a comparação entre eles é justa, mas a força absoluta do agente pode estar subestimada.
- **O alcance dos resultados é limitado.** Os resultados valem para estas 49 aberturas e estes dois adversários. Não dizem nada sobre adversários humanos ou mais fortes. Contra o d=3, as partidas são determinísticas dada a abertura, então o intervalo de confiança descreve a variação entre aberturas, não aleatoriedade do agente.
- **100% não significa "nunca perde".** Contra o Aleatório, o limite inferior do IC é 96,2%: com 98 partidas, uma taxa real de derrota de até cerca de 4% não pode ser descartada.
- **Nós visitados não são tempo.** Os nós não incluem o custo da avaliação por nó nem medem tempo de relógio. O Aleatório tem custo 0 por construção, e não porque seja eficiente.
