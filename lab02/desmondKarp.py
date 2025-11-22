from checker import check1
from collections import deque


def edgesToMatrix(E):
    n = 0
    for u, v, _ in E:
        n = max(n, u ,v)

    M = [[0 for _ in range(n)] for _ in range(n)]
    
    for u, v, w in E:
        u -= 1 
        v -= 1
        M[u][v] = w

    return M


def bfs(M, Parents, s, t):
    n = len(M)
    V = [False for _ in range(n)]
    V[s] = True
    Q = deque()
    Q.append(s)

    while Q:
        u = Q.popleft() 

        for v in range(n):
            if M[u][v] and not V[v]:
                V[v] = True
                Parents[v] = u
                Q.append(v)

    return V[t]


def desmondKarp(E):
    M = edgesToMatrix(E)
    n = len(M)
    s = 0
    t = n-1
    Parents = [-1 for _ in range(n)]
    maxFlow = 0

    while bfs(M, Parents, s, t):
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


check1(desmondKarp)
