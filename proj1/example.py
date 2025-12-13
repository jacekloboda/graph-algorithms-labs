from data import runtests

def solve(scores):
    for d, luck in scores:
        print(f"{d} przynosi {luck} szczęścia")

    return 7


runtests(solve)
