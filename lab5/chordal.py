import os
import sys
from dimacs import loadWeightedGraph, readSolution

class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()

    def connect_to(self, v):
        self.out.add(v)

def lex_bfs(G, V):
    # Lista zbiorów wierzchołków - początkowo jeden zbiór ze wszystkimi wierzchołkami
    sets = [{i for i in range(1, V + 1)}]
    visit_order = []
    
    while sets:
        # Pobieramy wierzchołek z ostatniego zbioru
        current_set = sets[-1]
        v_idx = current_set.pop()
        
        # Jeśli zbiór pusty, usuwamy go
        if not current_set:
            sets.pop()
            
        visit_order.append(v_idx)
        
        # Aktualizacja zbiorów (Refinement)
        neighbors_v = G[v_idx].out
        new_sets = []
        for s in sets:
            Y = s & neighbors_v  # Część wspólna (sąsiedzi v)
            K = s - neighbors_v  # Reszta (nie-sąsiedzi)
            
            if K:
                new_sets.append(K)
            if Y:
                new_sets.append(Y)
        sets = new_sets
        
    return visit_order

def is_chordal(G, visit_order):
    # Mapa: wierzchołek -> pozycja w odwiedzonej kolejności (im mniejsza, tym wcześniej odwiedzony)
    pos = {v: i for i, v in enumerate(visit_order)}
    
    for v_idx in visit_order:
        # RN(v) - sąsiedzi v, którzy występują wcześniej w kolejności LexBFS
        rn = {u for u in G[v_idx].out if pos[u] < pos[v_idx]}
        
        if not rn:
            continue
            
        # parent(v) - sąsiad z RN(v), który występuje w kolejności najpóźniej (największy indeks w pos)
        parent = max(rn, key=lambda x: pos[x])
        
        # Warunek PEO: RN(v) \ {parent(v)} musi być podzbiorem sąsiadów parent(v)
        # Czyli wszyscy wcześniejsi sąsiedzi v muszą być też sąsiadami jego rodzica
        rn_diff = rn - {parent}
        if not rn_diff.issubset(G[parent].out):
            return False
            
    return True

def run_tests():
    directory = os.path.join("graphs-lab4", "chordal")
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

        # Wczytywanie grafu
        try:
            V, L = loadWeightedGraph(path)
        except ValueError:
             # Obsługa błędu jeśli plik nie ma wag (format e u v zamiast e u v w)
            print(f"{filename:<30} | BŁĄD FORMATU (wymagane wagi)")
            continue

        if V == 0: continue

        # Budowa grafu (listy sąsiedztwa na zbiorach)
        G = [None] + [Node(i) for i in range(1, V + 1)]
        for u, v, w in L:
            G[u].connect_to(v)
            G[v].connect_to(u)

        # Algorytm
        order = lex_bfs(G, V)
        result = is_chordal(G, order)
        
        # Odczyt wyniku z pliku
        expected_str = readSolution(path)
        
        # Normalizacja wyniku oczekiwanego
        expected = None
        if expected_str in ["1", "True", "true", "True"]: expected = True
        elif expected_str in ["0", "False", "false", "False"]: expected = False
        
        # Status
        status = "OK" if result == expected else "BŁĄD"
        
        print(f"{filename:<30} | {str(result):<10} | {str(expected_str):<10} | {status}")

if __name__ == "__main__":
    run_tests()