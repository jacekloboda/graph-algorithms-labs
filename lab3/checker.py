from dimacs import *
import os
from time import time


def check(f, name = ''):
    dir = os.listdir("graphs-lab3")

    for i in range(len(dir)):
        if dir[i] == "grid100x100":
            dir[i], dir[-1] = dir[-1], dir[i]
            break

    i = 0
    a = time()

    if len(name) > 0:
        n, E = loadWeightedGraph("graphs-lab3/" + name)
        result = f(E)
        sol = int(readSolution("graphs-lab3/" + name))
        if result == sol:
            print("Test " + str(i) + ": Passed")
        else:
            print("Test " + str(i) + ": WRONG answer, result = " + str(result) + ", should be: " + str(sol))
        i += 1
        print("Time: " + str(time() - a) + " s")
        return

    for graph in dir:
        print(graph)
        n, E = loadWeightedGraph("graphs-lab3/" + graph)
        result = f(E)
        sol = int(readSolution("graphs-lab3/" + graph))
        if result == sol:
            print("Test " + str(i) + ": Passed")
        else:
            print("Test " + str(i) + ": WRONG answer, result = " + str(result) + ", should be: " + str(sol))
        i += 1
    
    print("Time: " + str(time() - a) + " s")