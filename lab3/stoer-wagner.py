from queue import PriorityQueue
from checker import check


class Node:
    def __init__(self):
        self.edges = {}

    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight

    def delEdge(self, to):
        del self.edges[to]


def gen_adj_list(L):
    n = 0
    for x, y, _ in L:
        n = max(n, x, y)
    G = [Node() for _ in range(n)]
    for x, y, w in L:
        x -= 1
        y -= 1
        G[x].addEdge(y, w)
        G[y].addEdge(x, w)
    return G


def min_cut_phase(G):
    weights = [0 for _ in range(len(G))]
    Q = PriorityQueue()
    Q.put((0, G[0]))
    processed = set()
    while not Q.empty():
        _, u = Q.get()
        if u in processed:
            continue
        processed.add(u)
        for v, w in u.edges.items():
            if v not in processed:
                weights[v] += w
                Q.put((-weights[v], v))
    s = processed[-1]
    t = processed[-2]
    cut_weight = sum(s.edges.values())
    return t, s, cut_weight


def mergeVerticles(G, x, y):
    for u, w in list(y.edges.items()):
        if u != x:
            x.addEdge(u, w)
            u.delEdge(y)
            u.addEdge(x, w)
    if y in x.edges:
        x.delEdge(y)
    G.remove(y)


def stoer_wagner(L):
    G = gen_adj_list(L)
    min_cut = float("inf")
    while len(G) > 1:
        v, u, w = min_cut_phase(G)
        min_cut = min(min_cut, w)
        mergeVerticles(G, v, u)
    return min_cut


check(stoer_wagner)
