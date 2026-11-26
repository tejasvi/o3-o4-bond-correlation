# pk10 (code): snapshot of the cumulant core of G2WOLFF's g2sw.py (lines 10-52, source sha8 recorded in PROGRESS.md),
# without its g2env import.  Rooted large-J expansion: Cov(q_a.q_b, q_u.q_v) = c2/J^2 + c3/J^3 + O(J^-4).
import itertools
import numpy as np
def kappa(Bs, G, n):
    k = len(Bs)
    if k == 1: return n*np.trace(Bs[0]@G)
    tot = 0.0
    for perm in itertools.permutations(range(1, k)):
        M = Bs[0]@G
        for j in perm: M = M@Bs[j]@G
        tot += np.trace(M)
    return 2**(k-1)*n*tot
def set_partitions(lst):
    if not lst: yield []; return
    first, rest = lst[0], lst[1:]
    for p in set_partitions(rest):
        yield [[first]] + p
        for i in range(len(p)): yield p[:i] + [[first]+p[i]] + p[i+1:]
def moment(Bs, G, n):
    if not Bs: return 1.0
    return sum(np.prod([kappa([Bs[i] for i in blk], G, n) for blk in p]) for p in set_partitions(list(range(len(Bs)))))
def E(poly, G, n): return sum(cf*moment(Bs, G, n) for cf, Bs in poly)
def mul(*polys):
    out = [(1.0, [])]
    for P in polys: out = [(c1*c2, B1+B2) for c1, B1 in out for c2, B2 in P]
    return out
def cov(P, Q, G, n): return E(mul(P, Q), G, n) - E(P, G, n)*E(Q, G, n)
def k3(X, Y, V, G, n):
    return (E(mul(X, Y, V), G, n) - E(mul(X, Y), G, n)*E(V, G, n) - E(mul(X, V), G, n)*E(Y, G, n)
            - E(mul(Y, V), G, n)*E(X, G, n) + 2*E(X, G, n)*E(Y, G, n)*E(V, G, n))
def coeffs(m, edges, b, u, v, n):
    # free sites 0..m-1; edges: dict (x,y)->c with y = -1 meaning the root
    L = np.zeros((m, m))
    for (x, y), c in edges.items():
        L[x, x] += c
        if y >= 0: L[y, y] += c; L[x, y] -= c; L[y, x] -= c
    G = np.linalg.inv(L)
    Ex = lambda x: np.outer(np.eye(m)[x], np.eye(m)[x])
    d = np.eye(m)[u] - np.eye(m)[v]; Dm = np.outer(d, d)
    X = [(1.0, [Ex(b)])]; Y = [(1.0, [Dm])]; P2 = [(1.0, [Ex(u)-Ex(v), Ex(u)-Ex(v)])]; X2 = [(1.0, [Ex(b), Ex(b)])]
    V = [(0.5, [Ex(x)]) for x in range(m)]
    for (x, y), c in edges.items():
        Bd = Ex(x) - (Ex(y) if y >= 0 else 0*Ex(x)); V.append((-c/8.0, [Bd, Bd]))
    c2 = 0.25*cov(X, Y, G, n)
    c3 = (cov(X, P2, G, n) + cov(X2, Y, G, n))/16.0 + 0.25*k3(X, Y, V, G, n)
    return c2, c3, G
