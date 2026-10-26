import csv
import math
import statistics as st
from lig4 import Lig4, AgenteAlfaBeta, AgenteAleatorio

SEMENTE = 2026
D_AGENTE, D_MENOR = 6, 3


def jogar_partida(jogo, abertura, ag1, ag2):
    """ag1 joga com o jogador 1 (MAX, comeca), ag2 com o jogador 2. Os 2 lances da abertura sao impostos."""
    s = jogo.inicial()
    for a in abertura:
        s = jogo.resultado(s, a)
    nos = {1: [], 2: []}
    ag = {1: ag1, 2: ag2}
    while not jogo.terminal(s):
        p = jogo.jogador(s)
        a, n = ag[p].jogar(s)
        nos[p].append(n)
        s = jogo.resultado(s, a)
    plies = jogo.L * jogo.C - s[0].count(0)
    return jogo.vencedor(s), plies, nos


def wilson(x, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - m, c + m)


def resumo_nos(v):
    v = sorted(v)
    p95 = v[min(len(v) - 1, math.ceil(0.95 * len(v)) - 1)]
    return dict(lances=len(v), media=st.mean(v), dp=st.pstdev(v), mediana=st.median(v), p95=p95, max=v[-1])


def main():
    jogo = Lig4()
    aberturas = [(a, b) for a in range(jogo.C) for b in range(jogo.C)]
    confrontos = [
        ("AlfaBeta(d=6) x Aleatorio", lambda i: AgenteAleatorio(jogo, SEMENTE + i)),
        ("AlfaBeta(d=6) x AlfaBeta(d=3)", lambda i: AgenteAlfaBeta(jogo, D_MENOR)),
    ]
    partidas, lances = [], []
    i = 0
    for nome, fabrica in confrontos:
        for ab in aberturas:
            for lado in (1, 2):  # lado em que joga o agente avaliado
                A, B = AgenteAlfaBeta(jogo, D_AGENTE), fabrica(i)
                w, plies, nos = jogar_partida(jogo, ab, A, B) if lado == 1 else jogar_partida(jogo, ab, B, A)
                res = "V" if w == lado else "D" if w == 3 - lado else "E"
                partidas.append(dict(id=i, confronto=nome, abertura=f"{ab[0]}{ab[1]}", lado_agente=lado,
                                     semente_aleatorio=SEMENTE + i if "Aleatorio" in nome else "",
                                     resultado_agente=res, plies=plies,
                                     nos_agente=sum(nos[lado]), nos_adversario=sum(nos[3 - lado])))
                for quem, p in (("agente", lado), ("adversario", 3 - lado)):
                    for n in nos[p]:
                        lances.append(dict(partida=i, confronto=nome, quem=quem, nos=n))
                i += 1

    with open("partidas.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=partidas[0].keys())
        w.writeheader()
        w.writerows(partidas)
    with open("lances.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=lances[0].keys())
        w.writeheader()
        w.writerows(lances)

    out = []
    out.append("## Resultados do AlfaBeta(d=6) (V/E/D do ponto de vista do agente avaliado)\n")
    out.append("| Confronto | Lado do agente | Partidas | V | E | D | Taxa de vitoria | IC 95% (Wilson) |")
    out.append("|---|---|---|---|---|---|---|---|")
    for nome, _ in confrontos:
        for lado, rot in ((1, "1o a jogar"), (2, "2o a jogar"), (None, "ambos")):
            ps = [p for p in partidas if p["confronto"] == nome and (lado is None or p["lado_agente"] == lado)]
            n = len(ps)
            v = sum(p["resultado_agente"] == "V" for p in ps)
            e = sum(p["resultado_agente"] == "E" for p in ps)
            d = sum(p["resultado_agente"] == "D" for p in ps)
            lo, hi = wilson(v, n)
            out.append(f"| {nome} | {rot} | {n} | {v} | {e} | {d} | {100 * v / n:.1f}% | [{100 * lo:.1f}%, {100 * hi:.1f}%] |")

    out.append("\n## Custo: nos visitados por lance\n")
    out.append("| Confronto | Agente | Lances | Media | Desvio-padrao | Mediana | P95 | Maximo (pior caso) | Nos por partida (media) |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for nome, _ in confrontos:
        for quem in ("agente", "adversario"):
            v = [l["nos"] for l in lances if l["confronto"] == nome and l["quem"] == quem]
            r = resumo_nos(v)
            ag = "AlfaBeta(d=6)" if quem == "agente" else nome.split(" x ")[1]
            col = "nos_agente" if quem == "agente" else "nos_adversario"
            por_partida = st.mean(p[col] for p in partidas if p["confronto"] == nome)
            out.append(f"| {nome} | {ag} | {r['lances']} | {r['media']:.0f} | {r['dp']:.0f} | {r['mediana']:.0f} | "
                       f"{r['p95']} | {r['max']} | {por_partida:.0f} |")

    out.append("\n## Duracao das partidas (plies, incluindo os 2 da abertura)\n")
    out.append("| Confronto | Media | Minimo | Maximo |")
    out.append("|---|---|---|---|")
    for nome, _ in confrontos:
        v = [p["plies"] for p in partidas if p["confronto"] == nome]
        out.append(f"| {nome} | {st.mean(v):.1f} | {min(v)} | {max(v)} |")

    texto = "\n".join(out)
    with open("resultados.md", "w") as f:
        f.write(texto + "\n")
    print(texto)


if __name__ == "__main__":
    main()
