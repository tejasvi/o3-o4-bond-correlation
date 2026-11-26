# Sparse version of strip_engine for larger label cutoffs (large uniform J): squared 6j symbols stored as COO tuples,
# column half-steps as scipy.sparse products.  Same conventions as strip_engine.py / pairs2.py (see there).
import math
import numpy as np
import scipy.sparse as sp
from scipy.special import ive


def _adm(x, y, z):
    return ((x + y + z) % 2 == 0) & (np.abs(x - y) <= z) & (z <= x + y)


def sixj_sq_coo(r123, r456):
    """COO lists of {x1 x2 x3; x4 x5 x6}^2 for x1..x3 in the box r123 = (n1,n2,n3), x4..x6 in r456 = (n4,n5,n6).
    Triangles (x1,x2,x3), (x1,x5,x6), (x4,x2,x6), (x4,x5,x3).  Returns (idx[6, nnz] int32, val[nnz])."""
    n1, n2, n3 = r123
    n4, n5, n6 = r456
    top = 2 * max(n1, n2, n3, n4, n5, n6) + 6
    fact = np.array([float(math.factorial(k)) for k in range(top + 2)])
    D, E, F = np.meshgrid(np.arange(n4), np.arange(n5), np.arange(n6), indexing='ij')
    def d2(x, y, z):
        return fact[(x + y - z) // 2] * fact[(x - y + z) // 2] * fact[(-x + y + z) // 2] / fact[(x + y + z) // 2 + 1]
    I = []; V = []
    for a in range(n1):
        for b in range(n2):
            for c in range(abs(a - b), min(a + b, n3 - 1) + 1, 2):
                m = _adm(a, E, F) & _adm(D, b, F) & _adm(D, E, c)
                if not m.any():
                    continue
                dd, ee, ff = D[m], E[m], F[m]
                al1 = (a + b + c) // 2
                al2 = (a + ee + ff) // 2
                al3 = (dd + b + ff) // 2
                al4 = (dd + ee + c) // 2
                be1 = (a + b + dd + ee) // 2
                be2 = (b + c + ee + ff) // 2
                be3 = (c + a + ff + dd) // 2
                zmin = np.maximum(np.maximum(al1, al2), np.maximum(al3, al4))
                zmax = np.minimum(np.minimum(be1, be2), be3)
                s = np.zeros(dd.shape)
                for z in range(int(zmin.min()), int(zmax.max()) + 1):
                    ok = (z >= zmin) & (z <= zmax)
                    if not ok.any():
                        continue
                    den = (fact[np.clip(z - al1, 0, None)] * fact[np.clip(z - al2, 0, None)] * fact[np.clip(z - al3, 0, None)]
                           * fact[np.clip(z - al4, 0, None)] * fact[np.clip(be1 - z, 0, None)] * fact[np.clip(be2 - z, 0, None)]
                           * fact[np.clip(be3 - z, 0, None)])
                    s += np.where(ok, ((-1.0) ** z) * fact[z + 1] / den, 0.0)
                val = d2(a, b, c) * d2(a, ee, ff) * d2(dd, b, ff) * d2(dd, ee, c) * s * s
                k = val != 0
                cnt = int(k.sum())
                I.append(np.stack([np.full(cnt, a), np.full(cnt, b), np.full(cnt, c), dd[k], ee[k], ff[k]]).astype(np.int32))
                V.append(val[k])
    return np.concatenate(I, axis=1), np.concatenate(V)


class SparseStrip:
    def __init__(self, L, gcap=None):
        self.L = L
        n = L + 1
        self.n = n
        self.gcap = 2 * L if gcap is None else min(gcap, 2 * L)
        ng = self.gcap + 1
        self.ng = ng
        # T1 tuples (bb, g, tp, a, t, h); T2 tuples (tp, hp, bbp, b, bb, g)
        self.I1, self.V1 = sixj_sq_coo((n, ng, n), (n, n, n))
        self.I2, self.V2 = sixj_sq_coo((n, n, n), (n, n, ng))
        bb, g, tp, a, t, h = self.I1
        self.r1 = ((bb * ng + g) * n + tp).astype(np.int64)        # F1 index
        self.c1 = ((t * n + h) * n + bb).astype(np.int64)          # state index
        self.a1 = a.astype(np.int64)
        self.g1 = g.astype(np.float64) + 1.0
        tp2, hp, bbp, b, bb2, g2 = self.I2
        self.r2 = ((tp2 * n + hp) * n + bbp).astype(np.int64)      # state index (output)
        self.c2 = ((bb2 * ng + g2) * n + tp2).astype(np.int64)     # F1 index
        self.b2 = b.astype(np.int64)
        self.nS = n ** 3
        self.nF1 = n * ng * n
        lab = np.arange(n)
        self.adm3 = _adm(lab[:, None, None], lab[None, :, None], lab[None, None, :]).astype(float).ravel()
        self.nnz1, self.nnz2 = len(self.V1), len(self.V2)

    def k(self, J):
        l = np.arange(self.L + 1)
        return 2.0 * ive(l + 1, J) / J

    def r(self, J):
        l = np.arange(self.L + 1)
        return (ive(l, J) + ive(l + 2, J)) / (2.0 * ive(l + 1, J)) - 1.0 / J

    # sparse operators for given vertical weights
    def A1(self, Wa):
        return sp.csr_matrix((self.V1 * self.g1 * Wa[self.a1], (self.r1, self.c1)), shape=(self.nF1, self.nS))

    def A1pin(self):
        return sp.csr_matrix((self.V1 * self.g1, (self.a1 * self.nF1 + self.r1, self.c1)), shape=(self.n * self.nF1, self.nS))

    def A2(self, Wb):
        return sp.csr_matrix((self.V2 * Wb[self.b2], (self.r2, self.c2)), shape=(self.nS, self.nF1))

    def A2pin(self):
        return sp.csr_matrix((self.V2, (self.b2 * self.nS + self.r2, self.c2)), shape=(self.n * self.nS, self.nF1))

    def cutw(self, w):
        wt, wh, wb = w
        return (wt[:, None, None] * wh[None, :, None] * wb[None, None, :]).ravel()

    def weights(self, Jd, n):
        lab = np.arange(self.L + 1) + 1.0
        cut = []
        for j in range(n - 1):
            wt = lab * self.k(Jd[('t', j)]); wh = lab * self.k(Jd[('h', j)]); wb = lab * self.k(Jd[('bb', j)])
            if j == 0:
                wt = wt * self.k(Jd[('a', 0)]); wb = wb * self.k(Jd[('b', 0)])
            if j == n - 2:
                wt = wt * self.k(Jd[('a', n - 1)]); wb = wb * self.k(Jd[('b', n - 1)])
            cut.append(self.cutw((wt, wh, wb)))
        vert = {j: (lab * self.k(Jd[('a', j)]), lab * self.k(Jd[('b', j)])) for j in range(1, n - 1)}
        return cut, vert

    def forward(self, Jd, n):
        cut, vert = self.weights(Jd, n)
        F = [self.adm3.copy()]
        ops = {}
        for j in range(n - 2):
            Wa, Wb = vert[j + 1]
            ops[j + 1] = (self.A1(Wa), self.A2(Wb))
            G = F[j] * cut[j]
            F.append(ops[j + 1][1] @ (ops[j + 1][0] @ G))
        return F, cut, vert, ops

    @staticmethod
    def mirror(Jd, n):
        M = {}
        for (kind, j), v in Jd.items():
            M[(kind, n - 2 - j) if kind in ('t', 'h', 'bb') else (kind, n - 1 - j)] = v
        return M

    @staticmethod
    def flip(Jd):
        sw = {'t': 'bb', 'bb': 't', 'h': 'h', 'a': 'b', 'b': 'a'}
        return {(sw[kind], j): v for (kind, j), v in Jd.items()}

    def Z(self, Jd, n):
        F, cut, vert, ops = self.forward(Jd, n)
        return float(np.sum(F[n - 2] * cut[n - 2]))
