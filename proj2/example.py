from data import runtests
import sys
from collections import defaultdict

sys.setrecursionlimit(300000)


class Bucket:
    def __init__(self, items):
        self.data = set(items)
        self.left = None  # Dawniej prev
        self.right = None  # Dawniej next

    def detach(self):
        if self.left:
            self.left.right = self.right
        if self.right:
            self.right.left = self.left


def get_peo(n, adj):
    start_guard = Bucket([])
    end_guard = Bucket([])

    first_bucket = Bucket(range(n))

    start_guard.right = first_bucket
    first_bucket.left = start_guard
    first_bucket.right = end_guard
    end_guard.left = first_bucket

    location = [first_bucket] * n

    order = []

    while start_guard.right is not end_guard:
        current = end_guard.left

        u = current.data.pop()

        if not current.data:
            current.detach()

        order.append(u)
        location[u] = None

        to_split = {}

        for v in adj[u]:
            bucket_ptr = location[v]
            if bucket_ptr is not None:
                bid = id(bucket_ptr)
                if bid not in to_split:
                    to_split[bid] = (bucket_ptr, [])
                to_split[bid][1].append(v)

        for _, (old_bucket, moving_nodes) in to_split.items():
            if len(moving_nodes) == len(old_bucket.data):
                continue

            movers = set(moving_nodes)
            old_bucket.data.difference_update(movers)

            new_bucket = Bucket(movers)
            new_bucket.left = old_bucket
            new_bucket.right = old_bucket.right

            if old_bucket.right:
                old_bucket.right.left = new_bucket
            old_bucket.right = new_bucket

            for node in movers:
                location[node] = new_bucket

    return order


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

    tree = defaultdict(list)
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
            tree[parent].append(u)
        else:
            roots.append(u)

    memo = {}

    def get_max_independent(u, blocker):
        key = (u, blocker)
        if key in memo:
            return memo[key]

        val_exclude = 0
        for child in tree[u]:
            if blocker != -1 and blocker in adj[child]:
                next_blocker = blocker
            else:
                next_blocker = -1
            val_exclude += get_max_independent(child, next_blocker)

        val_include = -1
        if blocker == -1:
            val_include = weights[u]
            for child in tree[u]:
                val_include += get_max_independent(child, u)

        res = max(val_exclude, val_include)
        memo[key] = res
        return res

    total_mwis = 0
    for r in roots:
        total_mwis += get_max_independent(r, -1)

    return sum(weights) - total_mwis


runtests(solve)
