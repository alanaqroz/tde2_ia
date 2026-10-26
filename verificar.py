import math
import random
from lig4 import Lig4, Contador, minimax, alfabeta

SEMENTE, N_POSICOES, LANCES = 2026, 30, 10


def posicoes(jogo, rng):
    res = []
    while len(res) < N_POSICOES:
        s = jogo.inicial()
        for _ in range(LANCES):
            s = jogo.resultado(s, rng.choice(jogo.acoes(s)))
        if not jogo.terminal(s):
            res.append(s)
    return res


def main():
    jogo = Lig4(linhas=4, colunas=5)
    rng = random.Random(SEMENTE)
    iguais, tot_mm, tot_ab, sinais = 0, 0, 0, {"MAX vence": 0, "empate": 0, "MIN vence": 0}
    print(f"{'pos':>3} {'valor Minimax':>14} {'valor alfa-beta':>16} {'nos Minimax':>12} {'nos alfa-beta':>14}")
    for i, s in enumerate(posicoes(jogo, rng)):
        c1, c2 = Contador(), Contador()
        v1 = minimax(jogo, s, None, c1)
        v2 = alfabeta(jogo, s, None, -math.inf, math.inf, c2)
        iguais += v1 == v2
        tot_mm += c1.nos
        tot_ab += c2.nos
        sinais["MAX vence" if v1 > 0 else "MIN vence" if v1 < 0 else "empate"] += 1
        print(f"{i:>3} {v1:>14} {v2:>16} {c1.nos:>12} {c2.nos:>14}")
    print(f"\nValores identicos: {iguais}/{N_POSICOES}")
    print(f"Distribuicao dos valores verdadeiros: {sinais}")
    print(f"Nos totais: Minimax {tot_mm}, alfa-beta {tot_ab} ({100 * tot_ab / tot_mm:.2f}% do Minimax)")
    assert iguais == N_POSICOES, "ERRO: alfa-beta divergiu do Minimax"
    print("OK: alfa-beta devolve exatamente o mesmo valor que Minimax.")


if __name__ == "__main__":
    main()
