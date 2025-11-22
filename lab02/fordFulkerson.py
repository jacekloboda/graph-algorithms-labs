from checker import check1
from collections import deque

def edgesToMatrix(E):
    n = 0
    
    for u, v, _ in E:
        n = max(n, u, v)
    
    M = [[0 for _ in range(n)] for _ in range(n)]
    for u, v, w in E:
        u-=1
        v-=1
        M[u][v] = w;

    return M

def dfs(M, Parents, s, t):
    n = len(M)
    V = [False for _ in range(n)]
    
    def dfs_visit(u, parent):
        nonlocal t
        nonlocal n
        V[u] = True
        Parents[u] = parent
        if u == t:
            return True

        for v in range(n):
            if M[u][v] and not V[v]:
                dfs_visit(v, u)

    dfs_visit(s, -1)
    return V[t]

def fordFulkerson(E):
    M = edgesToMatrix(E)
    n = len(M)
    s = 0
    t = n-1
    Parents = [-1 for _ in range(n)]
    maxFlow = 0

    while dfs(M, Parents, s, t):
        pathFlow = float("inf")
        u = t
        while u != s:
            parent = Parents[u]
            pathFlow = min(pathFlow, M[parent][u])
            u = parent

        maxFlow += pathFlow

        u = t
        while u != s:
            parent = Parents[u]
            M[parent][u] -= pathFlow
            M[u][parent] += pathFlow
            u = parent

    return maxFlow

check1(fordFulkerson)
