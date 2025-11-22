from dimacs import *
import os
from time import time

def check1(f):
    dir = os.listdir("lab2/flow")

    for i in range(len(dir)):
        if dir[i] == "grid100x100":
            dir[i], dir[-1] = dir[-1], dir[i]
        elif dir[i] == "clique200":
            dir[i], dir[-2] = dir[-2], dir[i]

    i = 0
    a = time()
    for graph in dir:
        if graph == "grid100x100": continue
        n, E = loadDirectedWeightedGraph("lab2/flow/" + graph)
        print(graph)
        time1 = time()
        result = f(E)
        time2 = time() - time1
        sol = int(readSolution("lab2/flow/" + graph))
        if result == sol:
            print("Test " + str(i) + ": Passed, in  %.2f" % time2)
        else:
            print("Test " + str(i) + ": WRONG answer, result = " + str(result) + ", should be: " + str(sol) + ", in %.2f" % time2)
        i += 1
    
    print("Time: " + str(time() - a) + " s")


def check2(f, name = ''):
    dir = os.listdir("graphs-lab2/connectivity")

    for i in range(len(dir)):
        if dir[i] == "grid100x100":
            dir[i], dir[-1] = dir[-1], dir[i]
        elif dir[i] == "clique200":
            dir[i], dir[-2] = dir[-2], dir[i]    

    i = 0
    a = time()

    if len(name) > 0:
        n, E = loadWeightedGraph("graphs-lab2/connectivity/" + name)
        result = f(E)
        sol = int(readSolution("graphs-lab2/connectivity/" + name))
        if result == sol:
            print("Test " + str(i) + ": Passed")
        else:
            print("Test " + str(i) + ": WRONG answer, result = " + str(result) + ", should be: " + str(sol))
        i += 1
        print("Time: " + str(time() - a) + " s")
        return

    for graph in dir:
        print(graph)
        n, E = loadWeightedGraph("graphs-lab2/connectivity/" + graph)
        result = f(E)
        sol = int(readSolution("graphs-lab2/connectivity/" + graph))
        if result == sol:
            print("Test " + str(i) + ": Passed")
        else:
            print("Test " + str(i) + ": WRONG answer, result = " + str(result) + ", should be: " + str(sol))
        i += 1
    
    print("Time: " + str(time() - a) + " s")
