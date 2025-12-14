from data import runtests
from collections import defaultdict, deque
from math import log
from sympy.ntheory import factorint

scores = [(6, 5), (9, 1), (10, 6), (15, 7), (13, 6), (17, 5)]


def gen_res_graph(scores):
    M = defaultdict(lambda: defaultdict(int))

    for divider, luck in scores:
        prev = (0, 0)  # (0, 0) - sink, (1, 0) - hole
        factors = factorint(divider)
        for factor, cnt in factors.items():
            for i in range(1, cnt + 1):
                M[prev][(factor, i)] += luck
                prev = (factor, i)
        M[prev][(1, 0)] += luck

    for u, dict in M.items():
        print(u, dict)


def bfs(M, Parents, s, t):
    V = defaultdict(int)
    V[s] = 1
    Q = deque()
    Q.append(s)

    while Q:
        u = Q.popleft()

        for v, wgt in M[u].items():
            if M[u][v] > 0 and not V[v]:
                V[v] = 1
                Parents[v] = u
                Q.append(v)

    return V[t]


def solve(scores):
    M = gen_res_graph(scores)
    s = (0, 0)
    t = (1, 0)
    Parents = {}
    maxFlow = 0
    used_ind = set()

    while bfs(M, Parents, s, t):
        pathFlow = float("inf")
        log_val = 1
        u = t
        while u != s:
            parent = Parents[u]
            log_val *= u[0]
            pathFlow = min(pathFlow, M[parent][u])
            u = parent

        found_path = False
        if pathFlow - 5 * log(log_val, 10) > 0:
            maxFlow += pathFlow - 5 * log(log_val, 10)
            found_path = True

        u = t
        path = [u]
        while u != s:
            parent = Parents[u]
            M[parent][u] -= pathFlow
            M[u][parent] += pathFlow
            u = parent

        if found_path:
            for node in path:
                used_ind.add(node)
    res = 1
    for ind in used_ind:
        res *= ind[0]
    return res


# print(solve(scores))
# print(gen_res_graph(scores))
# print(prime_factors(1947))
runtests(solve)
