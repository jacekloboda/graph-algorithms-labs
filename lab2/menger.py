from checker import check2
from collections import deque
import copy


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


def desmondKarp(M_, s, t):
    M = copy.deepcopy(M_)
    n = len(M)
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

def menger(E):
    M = edgesToMatrix(E)
    n = len(M)

    min_amount = float("inf")

    for t in range (1, n):
        min_amount  = min(min_amount, desmondKarp(M, 0, t))

    return min_amount

check2(menger)
