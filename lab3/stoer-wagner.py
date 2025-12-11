from queue import PriorityQueue
from checker import check


class Node:
    def __init__(self, idx):
        self.idx = idx
        self.edges = {}

    def __lt__(self, other):
        return self.idx < other.idx

    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight

    def delEdge(self, to):
        del self.edges[to]


def gen_adj_list(L):
    n = 0
    for x, y, _ in L:
        n = max(n, x, y)

    G = [Node(i) for i in range(n)]

    for x, y, w in L:
        x -= 1
        y -= 1
        G[x].addEdge(G[y], w)
        G[y].addEdge(G[x], w)

    return G


def min_cut_phase(G):
    weights = {node: 0 for node in G}
    Q = PriorityQueue()
    processed = set()
    s = None
    t = None

    Q.put((0, G[0]))

    while not Q.empty():
        _, u = Q.get()
        if u in processed:
            continue

        processed.add(u)
        t = s
        s = u

        for v, w in u.edges.items():
            if v not in processed:
                weights[v] += w
                Q.put((-weights[v], v))

    cut_weight = sum(s.edges.values())
    return t, s, cut_weight


def mergeVertices(G, x, y):
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
        t, s, w = min_cut_phase(G)
        min_cut = min(min_cut, w)
        mergeVertices(G, t, s)

    return min_cut


check(stoer_wagner)
