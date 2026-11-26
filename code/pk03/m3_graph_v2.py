#!/usr/bin/env python3
"""m3_graph_v2.py -- pk03 (code/pk03/). Graphs of the certified M3 entries in mp.iv (PLAN_M3_CODE_v1_2; M3_ENTRY_LIST_v1_1).
REVISION of m3_graph_v1.py (9aefad9c): imports the generic module names (m3_scal, m3_graph, m3_series, m3_major), which the job scripts load from sha-pinned files;
no other change.
- Edge lists in the producers' dict order (it fixes riglap2.tree_couplings' choice among equal couplings, a free choice that only changes
  the far term's value): strip(columns) as lapl2.strip_graph for vac/int/free column types; endw_mix and endw_free as endw l.16-19; minus(r)
  for G4 without the horizontal bond (r, 3 + r) (vacmono l.144-146).
- Couplings: 'A' = (3 + sqrt 21)/6 and 'B' = (3 sqrt 5 - sqrt 21)/12 exactly in mp.iv (kt_cert_v1_5), 1 exact; their binary64 values
  (vacmod2's) are used only for choices (the tree order).
- GraphIV: Laplacian L; integer gauge basis Bm = [e_v - e_0] (centre-of-mass gauge on all vertices); integer form matrix W (vertex forms, then
  the pair forms phi_u - phi_v); W_int = Bm^T W; Lr = Bm^T L Bm, certainly positive definite (interval Cholesky); G_y = Lr^-1; Gam = W_int^T
  G_y W_int (the forms' Gram matrix, riglap2's W^T G W); the vertex variances G_vv; log tau = log det of L without row and column 0
  (matrix-tree: tau = det(Lsub)/V, riglap2.logmain); tilted(rates): Lt = Bm^T (L - 2 diag(rates)) Bm with a certain positive-definiteness
  test (C-TILT b), its Gam, G_vv and normalization N = (det Lr/det Lt)^(n/2) (riglap2.Graph.tilted, basis-free). No compute of its own.
"""
import math
from mpmath import iv
import m3_scal as S

A_F = (3 + math.sqrt(21)) / 6
B_F = (3 * math.sqrt(5) - math.sqrt(21)) / 12


def coupling(tag):
    """the exact coupling as an interval: 'A', 'B', or an int / binary64 / Fraction."""
    if tag == 'A':
        return S.finite((3 + iv.sqrt(21)) / 6)
    if tag == 'B':
        return S.finite((3 * iv.sqrt(5) - iv.sqrt(21)) / 12)
    return S.I(tag)


def coupling_float(tag):
    return A_F if tag == 'A' else B_F if tag == 'B' else float(tag)


def strip(columns):
    """(V, [((u, v), tag)]) in lapl2.strip_graph's order; columns: list of 'vac', 'int', 'free'."""
    E = []
    nc = len(columns)
    for j, ty in enumerate(columns):
        T, Mv, Bv = 3 * j, 3 * j + 1, 3 * j + 2
        if ty == 'vac':
            E += [((T, Mv), 'A'), ((Mv, Bv), 'A'), ((T, Bv), 'B')]
        elif ty in ('int', 'free'):
            E += [((T, Mv), 1), ((Mv, Bv), 1)]
        else:
            raise ValueError('column type %r' % ty)
        if j < nc - 1:
            E += [((3 * j + r, 3 * (j + 1) + r), 1) for r in range(3)]
    return 3 * nc, E


def endw_mix():
    """endw l.16-18: H then the vac column (0, 1, 2) and the free column's verticals."""
    E = [((0, 3), 1), ((1, 4), 1), ((2, 5), 1), ((0, 1), 'A'), ((1, 2), 'A'), ((0, 2), 'B'), ((3, 4), 1), ((4, 5), 1)]
    return 6, E


def endw_free():
    """endw l.16-19 (Efree)."""
    E = [((0, 3), 1), ((1, 4), 1), ((2, 5), 1), ((0, 1), 1), ((1, 2), 1), ((3, 4), 1), ((4, 5), 1)]
    return 6, E


def minus(V, E, edge):
    """E without one edge (vacmono l.144-146: edges_r = [e for e in E4 if e != (r, 3 + r)])."""
    out = [(e, c) for (e, c) in E if e != edge]
    assert len(out) == len(E) - 1
    return V, out


class GraphIV:
    def __init__(self, V, edges, pairs, N):
        assert N in (3, 4)
        self.V, self.N, self.n = V, N, N - 1
        self.edges = list(edges)
        self.pairs = [tuple(p) for p in pairs]
        self.F = V + len(self.pairs)
        self.groups = [0] * V + [1] * len(self.pairs)
        self.c = {e: coupling(t) for e, t in self.edges}
        self.cf = {e: coupling_float(t) for e, t in self.edges}
        zero = iv.mpf(0)
        L = [[zero] * V for _ in range(V)]
        for (u, v), cc in self.c.items():
            L[u][u] = L[u][u] + cc
            L[v][v] = L[v][v] + cc
            L[u][v] = L[u][v] - cc
            L[v][u] = L[v][u] - cc
        self.L = L
        self.Bm = [[(1 if v == j + 1 else -1 if v == 0 else 0) for j in range(V - 1)] for v in range(V)]
        W = [[0] * self.F for _ in range(V)]
        for v in range(V):
            W[v][v] = 1
        for i, (u, v) in enumerate(self.pairs):
            W[u][V + i] = 1
            W[v][V + i] = -1
        self.W = W
        self.W_int = [[sum(self.Bm[v][r] * W[v][f] for v in range(V)) for f in range(self.F)] for r in range(V - 1)]
        self.Lr = self._congruence(L)
        ok, low = S.cholesky_pd(self.Lr)
        if not ok:
            raise ArithmeticError('Bm^T L Bm is not certainly positive definite (lowest pivot %r)' % (low,))
        self.Gy = S.inverse(self.Lr)
        self.Gam = self._gram(self.Gy)
        self.Gvv = self._vertex_var(self.Gy)
        Lred = [[L[i][j] for j in range(1, V)] for i in range(1, V)]
        self.log_tau = S.finite(iv.log(S.det(Lred)))
        self.log_det_Lr = S.finite(iv.log(S.det(self.Lr)))

    def _congruence(self, M):
        V = self.V
        BM = [[S.isum(self.Bm[k][i] * M[k][j] for k in range(V) if self.Bm[k][i] != 0) for j in range(V)] for i in range(V - 1)]
        return [[S.isum(BM[i][k] * self.Bm[k][j] for k in range(V) if self.Bm[k][j] != 0) for j in range(V - 1)] for i in range(V - 1)]

    def _gram(self, Gy):
        R, F = self.V - 1, self.F
        WG = [[S.isum(self.W_int[k][f] * Gy[k][j] for k in range(R) if self.W_int[k][f] != 0) for j in range(R)] for f in range(F)]
        return [[S.isum(WG[f][k] * self.W_int[k][g] for k in range(R) if self.W_int[k][g] != 0) for g in range(F)] for f in range(F)]

    def _vertex_var(self, Gy):
        R = self.V - 1
        g0 = S.isum(Gy[i][j] for i in range(R) for j in range(R))
        return [g0] + [Gy[v - 1][v - 1] for v in range(1, self.V)]

    def qidx(self, u, v):
        for i, p in enumerate(self.pairs):
            if p == (u, v) or p == (v, u):
                return self.V + i
        raise KeyError((u, v))

    def logmain(self, J):
        return S.logmain(J, self.V, self.N, self.log_tau)

    def tree(self):
        """riglap2.tree_couplings: Kruskal on the edges sorted by decreasing binary64 coupling (stable, so ties keep the edge order);
        returns the chosen edges' exact couplings. Any spanning tree bounds Z (dropped bonds have factor <= 1)."""
        par = list(range(self.V))

        def find(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x
        out = []
        for e, tag in sorted(self.edges, key=lambda kv: -coupling_float(kv[1])):
            ru, rv = find(e[0]), find(e[1])
            if ru != rv:
                par[ru] = rv
                out.append(self.c[e])
        assert len(out) == self.V - 1
        return out

    def tilted(self, rates):
        """rates: binary64 per vertex (rounded up by the caller). None if Bm^T (L - 2 diag(rates)) Bm is not certainly positive definite."""
        V = self.V
        Lx = [[self.L[i][j] - (2 * S.I(rates[i]) if i == j else 0) for j in range(V)] for i in range(V)]
        Lt = self._congruence(Lx)
        ok, low = S.cholesky_pd(Lt)
        if not ok:
            return None
        Gty = S.inverse(Lt)
        lognorm = (iv.mpf(self.n) / 2) * (self.log_det_Lr - iv.log(S.det(Lt)))
        return {'Gam': self._gram(Gty), 'Gvv': self._vertex_var(Gty), 'N': S.finite(iv.exp(lognorm)), 'low': low}

    def restrict(self, Gam, idx):
        """the Gram matrix, W_int columns and groups of the forms idx (riglap4._restrict's support)."""
        idx = list(idx)
        return ([[Gam[f][g] for g in idx] for f in idx], [[r[f] for f in idx] for r in self.W_int], [self.groups[f] for f in idx])
