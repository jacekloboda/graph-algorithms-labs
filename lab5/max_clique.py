import os
from dimacs import loadWeightedGraph, readSolution

class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()

    def connect_to(self, v):
        self.out.add(v)

def lex_bfs(G, V):
    sets = [{i for i in range(1, V + 1)}]
    visit_order = []
    while sets:
        current_set = sets[-1]
        v_idx = current_set.pop()
        if not current_set: sets.pop()
        visit_order.append(v_idx)
        neighbors_v = G[v_idx].out
        new_sets = []
        for s in sets:
            Y = s & neighbors_v
            K = s - neighbors_v
            if K: new_sets.append(K)
            if Y: new_sets.append(Y)
        sets = new_sets
    return visit_order

def find_max_clique_size(G, visit_order):
    max_clique = 0
    # Pozycja wierzchołka w kolejności LexBFS
    pos = {v: i for i, v in enumerate(visit_order)}

    for v_idx in visit_order:
        # RN(v) to sąsiedzi, którzy są wcześniej w kolejności LexBFS
        rn = {u for u in G[v_idx].out if pos[u] < pos[v_idx]}
        
        # Rozmiar potencjalnej kliki to |RN(v)| + 1 (sam v)
        current_size = len(rn) + 1
        if current_size > max_clique:
            max_clique = current_size
            
    return max_clique

def run_tests():
    directory = os.path.join("graphs-lab4", "maxclique")
    print(f"Testowanie w katalogu: {directory}")

    try:
        files = sorted(os.listdir(directory))
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono katalogu {directory}")
        return

    print(f"{'PLIK':<30} | {'WYNIK':<10} | {'OCZEKIWANY':<10} | {'STATUS'}")
    print("-" * 70)

    for filename in files:
        path = os.path.join(directory, filename)
        if os.path.isdir(path): continue

        try:
            V, L = loadWeightedGraph(path)
        except ValueError:
            print(f"{filename:<30} | BŁĄD FORMATU")
            continue
            
        if V == 0: continue

        G = [None] + [Node(i) for i in range(1, V + 1)]
        for u, v, w in L:
            G[u].connect_to(v)
            G[v].connect_to(u)

        order = lex_bfs(G, V)
        result = find_max_clique_size(G, order)
        
        expected_str = readSolution(path)
        try:
            expected = int(expected_str)
            status = "OK" if result == expected else "BŁĄD"
        except (ValueError, TypeError):
            status = "?"
            expected = expected_str
        
        print(f"{filename:<30} | {str(result):<10} | {str(expected):<10} | {status}")

if __name__ == "__main__":
    run_tests()