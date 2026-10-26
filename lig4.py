import math
import random

VITORIA = 1_000_000


class Lig4:
    def __init__(self, linhas=6, colunas=7, k=4):
        self.L, self.C, self.k = linhas, colunas, k
        # Ordenacao de jogadas (heuristica barata): colunas centrais primeiro.
        meio = (colunas - 1) / 2
        self.ordem = sorted(range(colunas), key=lambda c: (abs(c - meio), c))
        self.janelas = self._janelas()
        self.col_centro = [colunas // 2] if colunas % 2 else [colunas // 2 - 1, colunas // 2]

    def _janelas(self):
        """Todas as sequencias de k casas alinhadas (horizontal, vertical, duas diagonais)."""
        L, C, k = self.L, self.C, self.k
        js = []
        for c in range(C):
            for r in range(L):
                for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
                    cf, rf = c + dc * (k - 1), r + dr * (k - 1)
                    if 0 <= cf < C and 0 <= rf < L:
                        js.append(tuple((c + dc * i) * L + (r + dr * i) for i in range(k)))
        return js

    # ---------------- formalizacao ----------------
    def inicial(self):
        return (tuple([0] * (self.L * self.C)), 1)

    def jogador(self, s):
        return s[1]

    def acoes(self, s):
        casas, L = s[0], self.L
        return [c for c in self.ordem if casas[c * L + L - 1] == 0]

    def resultado(self, s, a):
        casas, p = s
        base = a * self.L
        i = next(base + r for r in range(self.L) if casas[base + r] == 0)
        nova = list(casas)
        nova[i] = p
        return (tuple(nova), 3 - p)

    def vencedor(self, s):
        casas = s[0]
        for j in self.janelas:
            v = casas[j[0]]
            if v and all(casas[i] == v for i in j[1:]):
                return v
        return 0

    def terminal(self, s):
        return self.vencedor(s) != 0 or 0 not in s[0]

    def utilidade(self, s):
        """Um unico numero, do ponto de vista de MAX. Vitoria mais rapida vale mais
        (bonus = casas vazias), o que continua sendo funcao do estado."""
        w = self.vencedor(s)
        if w == 0:
            return 0
        bonus = s[0].count(0)
        return VITORIA + bonus if w == 1 else -(VITORIA + bonus)

    # ---------------- funcao de avaliacao (corte de profundidade) ----------------
    def avaliar(self, s):
        """Janela de k casas sem peca adversaria: k-1 pecas -> 5, k-2 pecas -> 2.
        Peca na coluna central -> 3 (participa de mais janelas). Pesos fixados a priori."""
        casas, L, k = s[0], self.L, self.k
        h = 0
        for j in self.janelas:
            n1 = n2 = 0
            for i in j:
                v = casas[i]
                if v == 1:
                    n1 += 1
                elif v == 2:
                    n2 += 1
            if n2 == 0:
                h += 5 if n1 == k - 1 else 2 if n1 == k - 2 else 0
            elif n1 == 0:
                h -= 5 if n2 == k - 1 else 2 if n2 == k - 2 else 0
        for c in self.col_centro:
            for r in range(L):
                v = casas[c * L + r]
                h += 3 if v == 1 else -3 if v == 2 else 0
        return h


# ---------------- busca ----------------
class Contador:
    def __init__(self):
        self.nos = 0


def minimax(jogo, s, prof, cont):
    """prof=None -> profundidade completa."""
    cont.nos += 1
    if jogo.terminal(s):
        return jogo.utilidade(s)
    if prof == 0:
        return jogo.avaliar(s)
    p = None if prof is None else prof - 1
    vals = [minimax(jogo, jogo.resultado(s, a), p, cont) for a in jogo.acoes(s)]
    return max(vals) if jogo.jogador(s) == 1 else min(vals)


def alfabeta(jogo, s, prof, alfa, beta, cont):
    """prof=None -> profundidade completa."""
    cont.nos += 1
    if jogo.terminal(s):
        return jogo.utilidade(s)
    if prof == 0:
        return jogo.avaliar(s)
    p = None if prof is None else prof - 1
    if jogo.jogador(s) == 1:
        v = -math.inf
        for a in jogo.acoes(s):
            v = max(v, alfabeta(jogo, jogo.resultado(s, a), p, alfa, beta, cont))
            if v >= beta:
                return v
            alfa = max(alfa, v)
        return v
    v = math.inf
    for a in jogo.acoes(s):
        v = min(v, alfabeta(jogo, jogo.resultado(s, a), p, alfa, beta, cont))
        if v <= alfa:
            return v
        beta = min(beta, v)
    return v


# ---------------- agentes ----------------
class AgenteAlfaBeta:
    """Alfa-beta com profundidade fixa (mecanismo de parada) e desempate pela ordem das colunas."""

    def __init__(self, jogo, prof):
        self.jogo, self.prof = jogo, prof
        self.nome = f"AlfaBeta(d={prof})"

    def jogar(self, s):
        jogo, cont = self.jogo, Contador()
        cont.nos += 1  # a raiz
        maxi = jogo.jogador(s) == 1
        alfa, beta = -math.inf, math.inf
        melhor_a, melhor_v = None, (-math.inf if maxi else math.inf)
        for a in jogo.acoes(s):
            v = alfabeta(jogo, jogo.resultado(s, a), self.prof - 1, alfa, beta, cont)
            if (maxi and v > melhor_v) or (not maxi and v < melhor_v):
                melhor_a, melhor_v = a, v
            if maxi:
                alfa = max(alfa, v)
            else:
                beta = min(beta, v)
        return melhor_a, cont.nos


class AgenteAleatorio:
    """Linha de base trivial: jogada legal uniforme. Nao busca: custo 0 nos."""

    def __init__(self, jogo, semente):
        self.jogo, self.rng = jogo, random.Random(semente)
        self.nome = "Aleatorio"

    def jogar(self, s):
        return self.rng.choice(self.jogo.acoes(s)), 0


def mostrar(jogo, s):
    simb = {0: ".", 1: "X", 2: "O"}
    linhas = []
    for r in range(jogo.L - 1, -1, -1):
        linhas.append(" ".join(simb[s[0][c * jogo.L + r]] for c in range(jogo.C)))
    linhas.append(" ".join(str(c) for c in range(jogo.C)))
    return "\n".join(linhas)


if __name__ == "__main__":
    # Demonstracao ao vivo com o contador de custo visivel: AlfaBeta(d=5) (X) contra AlfaBeta(d=2) (O).
    import sys
    d1 = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    d2 = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    jogo = Lig4()
    agentes = {1: AgenteAlfaBeta(jogo, d1), 2: AgenteAlfaBeta(jogo, d2)}
    s, total = jogo.inicial(), {1: 0, 2: 0}
    while not jogo.terminal(s):
        p = jogo.jogador(s)
        a, nos = agentes[p].jogar(s)
        total[p] += nos
        s = jogo.resultado(s, a)
        print(f"\n{agentes[p].nome} ({'X' if p == 1 else 'O'}) joga coluna {a} | nos neste lance: {nos} | acumulado: {total[p]}")
        print(mostrar(jogo, s))
    w = jogo.vencedor(s)
    print("\nResultado:", "empate" if w == 0 else f"vence {agentes[w].nome}")
