#!/usr/bin/env python3
# pk10 (code): formal second-order Laplace expansion of small-graph O(N) integrals (normalized uniform measures on S^{N-1}),
#   I(J) = int prod_v dsigma_v  prod_{i in ins} (sigma_u.sigma_v)  exp(J sum_e c_e sigma_u.sigma_v),
# rooted at one vertex (global rotation exact), hemisphere chart sigma = (pi, sqrt(1-|pi|^2)), phi = sqrt(J) pi:
#   log I = J sum c - (V-1) log|S^{N-1}| + (n(V-1)/2) log(2 pi / J) - (n/2) log det L + log(1 + A1/J + A2/J^2 + O(J^-3)),
#   A1 = E[P1 + U1],  A2 = E[P2 + P1 U1 + U2 + U1^2/2],  Gaussian E with covariance L^{-1} (x) I_n,
#   U1 = sum_v |phi_v|^2/2 - sum_e c_e D_e^2/8,  U2 = sum_v |phi_v|^4/4 - sum_e c_e (|phi_u|^2+|phi_v|^2) D_e^2/16,  D_e = |phi_u|^2 - |phi_v|^2,
#   P1 = -sum_i |phi_u - phi_v|^2/2,  P2 = sum_{i<j} |.|_i^2 |.|_j^2 / 4 - sum_i D_i^2/8.
# Uses the G2WOLFF cumulant core (moments of products of Gaussian quadratic forms).
import math
import sys
import numpy as np
sys.path.insert(0, "/mnt/g2/release/root/code/pk10/scripts")
from g2sw_core_snapshot import E as Epoly, mul


def expand(nverts, edges, root, ins, N=4):
    """edges: dict (u,v) -> c (units of J); ins: list of (u,v) dot-product insertions. Returns (logpref_without_J_terms, A1, A2, sum_c)."""
    n = N - 1
    free = [v for v in range(nverts) if v != root]
    ix = {v: i for i, v in enumerate(free)}
    m = len(free)
    Lap = np.zeros((m, m))
    for (u, v), c in edges.items():
        for (p, q) in ((u, v), (v, u)):
            if p != root:
                Lap[ix[p], ix[p]] += c
                if q != root:
                    Lap[ix[p], ix[q]] -= c
    G = np.linalg.inv(Lap)
    I = np.eye(m)

    def Ex(v):
        return np.zeros((m, m)) if v == root else np.outer(I[ix[v]], I[ix[v]])

    def Dm(u, v):
        d = (np.zeros(m) if u == root else I[ix[u]]) - (np.zeros(m) if v == root else I[ix[v]])
        return np.outer(d, d)

    U1 = [(0.5, [Ex(v)]) for v in free]
    U2 = [(0.25, [Ex(v), Ex(v)]) for v in free]
    for (u, v), c in edges.items():
        Bd = Ex(u) - Ex(v)
        U1.append((-c / 8.0, [Bd, Bd]))
        U2.append((-c / 16.0, [Ex(u) + Ex(v), Bd, Bd]))
    P1 = [(-0.5, [Dm(u, v)]) for (u, v) in ins]
    P2 = []
    for i in range(len(ins)):
        for j in range(i + 1, len(ins)):
            P2.append((0.25, [Dm(*ins[i]), Dm(*ins[j])]))
    for (u, v) in ins:
        Bd = Ex(u) - Ex(v)
        P2.append((-0.125, [Bd, Bd]))
    E1 = lambda P: Epoly(P, G, n) if P else 0.0
    A1 = E1(P1) + E1(U1)
    A2 = E1(P2) + (E1(mul(P1, U1)) if P1 else 0.0) + E1(U2) + 0.5 * E1(mul(U1, U1))
    sign, logdet = np.linalg.slogdet(Lap)
    area = 2.0 * math.pi ** (N / 2) / math.gamma(N / 2)
    logpref = -(m) * math.log(area) + (n * m / 2.0) * math.log(2 * math.pi) - (n / 2.0) * logdet
    return logpref, A1, A2, sum(edges.values()), m


def strip_graph(ncols, end_ab, mid_c=1.0):
    """3-row strip with ncols columns; end columns are triangles with couplings (a, a, b) (T-M, M-B, T-B); interior columns verticals mid_c;
    horizontals 1.  Vertex id = 3*col + row (row 0 = T, 1 = M, 2 = B)."""
    a, b = end_ab
    E = {}
    for j in range(ncols):
        T, Mv, B = 3 * j, 3 * j + 1, 3 * j + 2
        if j == 0 or j == ncols - 1:
            E[(T, Mv)] = a; E[(Mv, B)] = a
            if b > 0:
                E[(T, B)] = b
        else:
            E[(T, Mv)] = mid_c; E[(Mv, B)] = mid_c
        if j < ncols - 1:
            for r in range(3):
                E[(3 * j + r, 3 * (j + 1) + r)] = 1.0
    return 3 * ncols, E


if __name__ == "__main__":
    outf = sys.argv[1]
    a, b = float(sys.argv[2]), float(sys.argv[3])
    lines = ["# lapl2: formal 2nd-order Laplace expansion, triangle end columns (a, a, b) = (%g, %g, %g), N = 4" % (a, a, b)]
    for nc in (2, 3, 4):
        V, Ed = strip_graph(nc, (a, b))
        lp, A1, A2, sc, m = expand(V, Ed, root=1, ins=[])
        lines.append("ncols %d: V = %d, sum c = %.6f, logpref = %.10f, n m/2 = %.1f, A1 = %.10f, A2 = %.10f" % (nc, V, sc, lp, 1.5 * m, A1, A2))
    open(outf, "w").write("\n".join(lines) + "\n")
