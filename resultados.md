## Resultados do AlfaBeta(d=6) (V/E/D do ponto de vista do agente avaliado)

| Confronto | Lado do agente | Partidas | V | E | D | Taxa de vitoria | IC 95% (Wilson) |
|---|---|---|---|---|---|---|---|
| AlfaBeta(d=6) x Aleatorio | 1o a jogar | 49 | 49 | 0 | 0 | 100.0% | [92.7%, 100.0%] |
| AlfaBeta(d=6) x Aleatorio | 2o a jogar | 49 | 49 | 0 | 0 | 100.0% | [92.7%, 100.0%] |
| AlfaBeta(d=6) x Aleatorio | ambos | 98 | 98 | 0 | 0 | 100.0% | [96.2%, 100.0%] |
| AlfaBeta(d=6) x AlfaBeta(d=3) | 1o a jogar | 49 | 39 | 6 | 4 | 79.6% | [66.4%, 88.5%] |
| AlfaBeta(d=6) x AlfaBeta(d=3) | 2o a jogar | 49 | 41 | 4 | 4 | 83.7% | [71.0%, 91.5%] |
| AlfaBeta(d=6) x AlfaBeta(d=3) | ambos | 98 | 80 | 10 | 8 | 81.6% | [72.8%, 88.1%] |

## Custo: nos visitados por lance

| Confronto | Agente | Lances | Media | Desvio-padrao | Mediana | P95 | Maximo (pior caso) | Nos por partida (media) |
|---|---|---|---|---|---|---|---|---|
| AlfaBeta(d=6) x Aleatorio | AlfaBeta(d=6) | 483 | 2652 | 2767 | 2076 | 6497 | 33441 | 13069 |
| AlfaBeta(d=6) x Aleatorio | Aleatorio | 434 | 0 | 0 | 0 | 0 | 0 | 0 |
| AlfaBeta(d=6) x AlfaBeta(d=3) | AlfaBeta(d=6) | 1214 | 2206 | 3476 | 1652 | 6345 | 61915 | 27333 |
| AlfaBeta(d=6) x AlfaBeta(d=3) | AlfaBeta(d=3) | 1179 | 85 | 47 | 84 | 164 | 237 | 1020 |

## Duracao das partidas (plies, incluindo os 2 da abertura)

| Confronto | Media | Minimo | Maximo |
|---|---|---|---|
| AlfaBeta(d=6) x Aleatorio | 11.4 | 7 | 24 |
| AlfaBeta(d=6) x AlfaBeta(d=3) | 26.4 | 7 | 42 |
