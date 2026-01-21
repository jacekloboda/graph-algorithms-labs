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

def min_vertex_cover(G, visit_order):
    independent_set = set()
    
    # Iteracja w ODWROTNEJ kolejności LexBFS
    for v in reversed(visit_order):
        neighbors = G[v].out
        
        # Sprawdź czy zbiór niezależny i sąsiedzi są rozłączni
        # (czyli czy żaden sąsiad v nie został już dodany do zbioru niezależnego)
        if independent_set.isdisjoint(neighbors):
            independent_set.add(v)
            
    # Vertex Cover = V - Independent Set
    # Rozmiar VC = |V| - |IS|
    return len(visit_order) - len(independent_set)

def run_tests():
    directory = os.path.join("graphs-lab4", "vcover")
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
        result = min_vertex_cover(G, order)
        
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