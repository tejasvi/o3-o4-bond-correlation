#!/usr/bin/env python3
# pk10 (code): builders for the vacuum residual function (shared by vacres*.py).  See vacres.py for the setting.
# Variables (12): sigma forms X_T X_M X_B Q_TM Q_MB Q_TB (0-5), sigma'' forms (6-11).
import math
import numpy as np
from pseries import Series, padd, pscale, pmul, pconst, pvar, w_coeffs

A_EX = (3 + math.sqrt(21)) / 6
B_EX = (3 * math.sqrt(5) - math.sqrt(21)) / 12
NV = 12
XS, QS, XD, QD = [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]
PAIRS = [(0, 1), (1, 2), (0, 2)]
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]


class Builder:
    def __init__(self, K, a=A_EX, b=B_EX):
        self.K, self.a, self.b = K, a, b
        self.w = w_coeffs(K)

    def S(self, coeffs):
        return Series(self.K, NV, coeffs)

    def zero(self):
        return self.S([{} for _ in range(self.K + 1)])

    def one(self):
        return self.S([pconst(1.0, NV)] + [{} for _ in range(self.K)])

    def meas(self, i):
        return self.S([{}] + [{tuple(k if j == i else 0 for j in range(NV)): 1.0 / (2 * k)} for k in range(1, self.K + 1)])

    def anh(self, iu, iv, c):
        K = self.K
        out = [{} for _ in range(K + 1)]
        d2 = padd(pmul(pvar(iu, NV), pvar(iu, NV)), pscale(pmul(pvar(iu, NV), pvar(iv, NV)), -2.0), pmul(pvar(iv, NV), pvar(iv, NV)))
        for (i, j), cw in self.w.items():
            k = 1 + i + j
            if k > K:
                continue
            mono = {tuple((i if q == iu else 0) + (j if q == iv else 0) for q in range(NV)): 1.0}
            out[k] = padd(out[k], pscale(pmul(d2, mono), -0.5 * c * cw))
        return self.S(out)

    def xi(self, Xi, Qi):
        res = []
        for p, (r, s) in enumerate(PAIRS):
            base = self.S([pvar(Qi[p], NV, 0.5)] + [{} for _ in range(self.K)])
            res.append(base - self.anh(Xi[r], Xi[s], 1.0))
        return res

    def fb(self, xis, mono):
        out = self.one()
        for p in mono:
            out = out * xis[p]
        return out

    def HL(self):
        a, b = self.a, self.b
        H = self.zero()
        for r in range(3):
            H = H + self.meas(XD[r])
        for p, (r, s) in enumerate(PAIRS):
            H = H + self.anh(XD[r], XD[s], [a, a, b][p])
        for r in range(3):
            H = H + self.anh(XS[r], XD[r], 1.0)
        return H + self.anh(XS[0], XS[1], 1.0) + self.anh(XS[1], XS[2], 1.0)

    def H0(self):
        a, b = self.a, self.b
        H = self.zero()
        for p, (r, s) in enumerate(PAIRS):
            H = H + self.anh(XS[r], XS[s], [a, a, b][p])
        return H

    def poly_p(self, xis, q1, q2, q3=None):
        """p = 1 + t q1(xi) + t^2 q2(xi) + t^3 q3(xi) as a series."""
        P = self.one()
        for coef, sh in ((q1, 1), (q2, 2), (q3 if q3 is not None else [0.0] * len(BASIS), 3)):
            for cb, mono in zip(coef, BASIS):
                if cb == 0.0 or sh > self.K:
                    continue
                f = self.fb(xis, mono).scale(cb)
                shifted = [{} for _ in range(sh)] + f.c[:self.K + 1 - sh]
                P = P + self.S(shifted)
        return P

    def L1(self, q1, q2, q3=None):
        return self.poly_p(self.xi(XD, QD), q1, q2, q3) * self.HL().exp()

    def L0(self, q1, q2, q3=None):
        return self.poly_p(self.xi(XS, QS), q1, q2, q3) * self.H0().exp()


def ltri(a=A_EX, b=B_EX):
    L = np.zeros((3, 3))
    for p, (r, s) in enumerate(PAIRS):
        c = [a, a, b][p]
        L[r, r] += c; L[s, s] += c; L[r, s] -= c; L[s, r] -= c
    return L


def dgraph_cov(a=A_EX, b=B_EX):
    from lapl2 import strip_graph
    V, Ed = strip_graph(2, (a, b))
    L = np.zeros((V, V))
    for (u, v), c in Ed.items():
        L[u, u] += c; L[v, v] += c; L[u, v] -= c; L[v, u] -= c
    ev, evec = np.linalg.eigh(L); Qb = evec[:, 1:]
    return Qb @ np.linalg.inv(Qb.T @ L @ Qb) @ Qb.T


def joint6_cov(a=A_EX, b=B_EX):
    """covariance of (phi_sigma (3), phi_sigma'' (3)) per component under gamma_4 (gauge CM of the two middle columns)."""
    Gd = dgraph_cov(a, b)
    Sss = Gd[:3, :3]
    Ainv = np.linalg.inv(np.eye(3) + ltri(a, b))
    C = np.zeros((6, 6))
    C[:3, :3] = Sss
    C[3:, :3] = Ainv @ Sss
    C[:3, 3:] = Sss @ Ainv
    C[3:, 3:] = Ainv @ Sss @ Ainv + Ainv
    return C


def forms12():
    """W (6 x 12): rank-one forms on (sigma (vertices 0-2), sigma'' (vertices 3-5)) in the variable order of NV."""
    W = np.zeros((6, 12))
    for blk in range(2):
        for r in range(3):
            W[3 * blk + r, 6 * blk + r] = 1.0
        for p, (r, s) in enumerate(PAIRS):
            W[3 * blk + r, 6 * blk + 3 + p] = 1.0; W[3 * blk + s, 6 * blk + 3 + p] = -1.0
    return W
