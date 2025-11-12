import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_graph = os.path.join(current_dir, "graphs01", "g1")
from graphs01.dimacs import *

class Node():
    def __init__(self):
        self.parent = self
        self.rank = 0


def find(x):
    if x != x.parent:
        x.parent = find(x.parent)

    return x.parent

def union(x, y):
    x = find(x)
    y = find(y)
    
    if x.rank < y.rank:
        x.parent = y

    else:
        y.parent = x
        
        if x.rank == y.rank:
            x.rank += 1

def dfs(G, s, t):
    n = len(G)
    n+=1
    V = [False]*n
    W = [float("inf")]*n

    def dfs_visit(u, min_): 
        V[u] = True
        W[u] = min_

        for v, wgt in G[u]:
            if not V[v]:
                dfs_visit(v, min(min_, wgt))


    dfs_visit(s, float("inf"))
    return W[t]

def solve():
    n, G = loadWeightedGraph(path_to_graph)
    n+=1
    E = []
    V = [Node() for _ in range(n)]
    E = sorted(G, key=lambda x: x[2], reverse=True)
    MST = [[]for _ in range(n)]

    for u, v, wgt in E:
        if find(V[u]) != find(V[v]):
            MST[u].append((v, wgt))
            MST[v].append((u, wgt))
            union(V[u], V[v])

    min_wgt = dfs(MST, 1, 2)
    #print(min_wgt)
    return min_wgt

print("solved: ", solve())
print("expected: ", readSolution(path_to_graph))
print(solve()==readSolution(path_to_graph))





    


