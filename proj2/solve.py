from data import runtests
import sys
from functools import lru_cache

sys.setrecursionlimit(300000)


def get_peo(n, adj):
    buckets = [set() for _ in range(n)]
    buckets[0] = set(range(n))

    weights = [0] * n
    processed = [False] * n

    peo = []
    max_weight = 0

    for _ in range(n):
        while max_weight >= 0 and not buckets[max_weight]:
            max_weight -= 1

        u = buckets[max_weight].pop()
        processed[u] = True
        peo.append(u)

        for v in adj[u]:
            if not processed[v]:
                old_w = weights[v]
                buckets[old_w].remove(v)

                new_w = old_w + 1
                weights[v] = new_w
                buckets[new_w].add(v)

                if new_w > max_weight:
                    max_weight = new_w

    return peo


def solve(edges, weights):
    n = len(weights)

    adj = [set() for _ in range(n)]
    for u, v in edges:
        u, v = u - 1, v - 1
        adj[u].add(v)
        adj[v].add(u)

    peo = get_peo(n, adj)

    rev_peo = peo[::-1]
    rank = {node: i for i, node in enumerate(rev_peo)}

    tree_adj = [[] for _ in range(n)]
    roots = []

    for u in rev_peo:
        parent = -1
        min_rank = float("inf")

        for v in adj[u]:
            r_v = rank[v]
            if r_v > rank[u] and r_v < min_rank:
                min_rank = r_v
                parent = v

        if parent != -1:
            tree_adj[parent].append(u)
        else:
            roots.append(u)

    @lru_cache(maxsize=None)
    def get_max_independent(u, blocker):
        val_exclude = 0
        for child in tree_adj[u]:
            if blocker != -1 and blocker in adj[child]:
                next_blocker = blocker
            else:
                next_blocker = -1
            val_exclude += get_max_independent(child, next_blocker)

        val_include = -1
        if blocker == -1 or blocker not in adj[u]:
            val_include = weights[u]
            for child in tree_adj[u]:
                if u in adj[child]:
                    next_blocker_inc = u
                else:
                    next_blocker_inc = -1
                val_include += get_max_independent(child, next_blocker_inc)

        return max(val_exclude, val_include)

    total_mwis = 0
    for r in roots:
        total_mwis += get_max_independent(r, -1)

    return sum(weights) - total_mwis


runtests(solve)
