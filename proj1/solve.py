from data import runtests
from collections import defaultdict, deque
from math import log

# scores = [(6, 5), (9, 1), (10, 6), (15, 7), (13, 6), (17, 5)]
primes = []


def prime_factors(n, global_dict):
    divider_dict = defaultdict(int)
    ind = 0

    while n > 1:
        prime = primes[ind]
        if n % prime == 0:
            divider_dict[prime] += 1
            global_dict[prime] = max(global_dict[prime], divider_dict[prime])
            n //= primes[ind]
        else:
            ind += 1

    return divider_dict


def gen_res_graph(scores):
    global_dict = defaultdict(int)
    factors = []

    for divider, _ in scores:
        # for updating global dict
        factors.append(prime_factors(divider, global_dict))

    n = sum(map(lambda x: x[1], global_dict.items()))
    n += 2
    # 0th node is sink - s
    # (n-1)th node is hole - t

    ind_dict = {}  # index of node (x, cnt) in M
    ind = 1
    ind_val = [1 for _ in range(n)]
    for factor, cnt in global_dict.items():
        while cnt > 0:
            ind_dict[(factor, cnt)] = ind
            ind_val[ind] = factor
            cnt -= 1
            ind += 1

    M = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(len(scores)):
        divider, wgt = scores[i]
        divider_dict = factors[i]

        prev_ind = 0
        for factor, cnt in divider_dict.items():
            tmp_cnt = 1
            while tmp_cnt <= cnt:
                ind = ind_dict[(factor, tmp_cnt)]
                M[prev_ind][ind] += wgt
                tmp_cnt += 1
                prev_ind = ind

        M[prev_ind][n - 1] += wgt

    #    for row in M:
    #        print(row)
    #
    #    for item in ind_dict.items():
    #        print(item)

    return M, ind_val


def bfs(M, Parents, s, t):
    n = len(M)
    V = [False for _ in range(n)]
    V[s] = True
    Q = deque()
    Q.append(s)

    while Q:
        u = Q.popleft()

        for v in range(n):
            if M[u][v] > 0 and not V[v]:
                V[v] = True
                Parents[v] = u
                Q.append(v)

    return V[t]


def solve(scores):
    M, ind_val = gen_res_graph(scores)
    n = len(M)
    s = 0
    t = n - 1
    Parents = [-1 for _ in range(n)]
    maxFlow = 0
    used_ind = set()

    while bfs(M, Parents, s, t):
        pathFlow = float("inf")
        log_val = 1
        u = t
        while u != s:
            parent = Parents[u]
            log_val *= ind_val[u]
            pathFlow = min(pathFlow, M[parent][u])
            u = parent

        found_path = False
        if pathFlow - 5 * log(log_val, 10) > 0:
            maxFlow += pathFlow - 5 * log(log_val, 10)
            found_path = True

        u = t
        path = [u]
        while u != s:
            parent = Parents[u]
            M[parent][u] -= pathFlow
            M[u][parent] += pathFlow
            u = parent
            path.append(u)

        if found_path:
            for node in path:
                used_ind.add(node)
    res = 1
    for ind in used_ind:
        # print(ind, ind_val[ind])
        res *= ind_val[ind]
    return res


# print(solve(scores))
# print(gen_res_graph(scores))
# print(prime_factors(1947))
runtests(solve)
