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

def optimal_coloring(G, visit_order, V):
    # Tablica kolorów: 0 oznacza brak koloru
    colors = {i: 0 for i in range(1, V + 1)}
    max_color_used = 0

    # Iterujemy zgodnie z LexBFS
    for v in visit_order:
        neighbors = G[v].out
        # Zbiór kolorów użytych przez sąsiadów
        used_colors = {colors[u] for u in neighbors if colors[u] != 0}
        
        # Znajdź najmniejszy wolny kolor (startując od 1)
        c = 1
        while c in used_colors:
            c += 1
            
        colors[v] = c
        max_color_used = max(max_color_used, c)
        
    return max_color_used

def run_tests():
    directory = os.path.join("graphs-lab4", "coloring")
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
        result = optimal_coloring(G, order, V)
        
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