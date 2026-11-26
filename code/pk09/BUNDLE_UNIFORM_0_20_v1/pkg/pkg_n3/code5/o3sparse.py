# O(3) (N = 3) label-space sparse engine for 3-row strips P3 x Pn (wave 18).  Spins on S^2 with the normalized measure:
#   e^{J s.t} = sum_l i_l(J) sum_m e_lm(s) e_lm(t)^*,  i_l(J) = sqrt(pi/2J) I_{l+1/2}(J),  e_lm = sqrt(4 pi) Y_lm.
# Cut states |a b c> = sum_m (a b c; m1 m2 m3) e_{a m1}(s_t) e_{b m2}(s_h) e_{c m3}(s_bb), integer spins with triangle(a,b,c):
# an orthonormal basis of the rotation-invariant functions of one column.  Only a + b + c even occurs (the inversion
# s -> -s acts by (-1)^{a+b+c}, commutes with the transfer, and fixes |000>).  Horizontal bonds act as K = diag(i_a i_b i_c).
# Column map M = <a'b'c'| f(s_t.s_h) f(s_h.s_bb) |abc> = A2 A1 (scalar products of the tensor operators e_p, Edmonds 7.1.6,
# with <l'||e_p||l> = (-1)^{l'} g(l',p,l); the (12)- and (23)-coupled bases equal |abc> for even a + b + c):
#   A1[(a, b2, c'), (a, b, c)]   = sum_q W_q (-1)^{a+c+c'} g(b2,q,b) g(c',q,c) {b2 c' a; c b q}    (bond rows 2-3)
#   A2[(a', b', c'), (a, b2, c')] = sum_p W_p (-1)^{a+b'} g(a',p,a) g(b',p,b2) {a' b' c'; b2 a p}   (bond rows 1-2)
# g(l1,l2,l3) = sqrt((2l1+1)(2l2+1)(2l3+1)) (l1 l2 l3; 0 0 0), W_l = i_l(J), vertical labels p, q <= L.  The intermediate
# states (a, b2, c') run over a, c' <= L and b2 <= 2L, so M is the exact compression of the truncated vertical operator.
# S = K^{1/2} M K^{1/2}, b = K^{1/2} M |000>, Z(P3 x Pn) = <b, S^{n-2} b>.  Float 6j symbols by the Racah sum in log space,
# for numerics and validation (code5/o3brute.py compares with an m-basis computation).
import math
import numpy as np
import scipy.sparse as sp
from scipy.special import ive


def _tri(a, b, c):
    return abs(a - b) <= c <= a + b


class O3Strip:
    def __init__(self, L):
        self.L = L
        n = L + 1
        self.n = n
        lf = [math.lgamma(k + 1.0) for k in range(12 * n + 16)]
        self.lf = lf
        st = [(a, b, c) for a in range(n) for b in range(n) for c in range(n) if _tri(a, b, c) and (a + b + c) % 2 == 0]
        self.states = st
        self.idx = {s: i for i, s in enumerate(st)}
        self.nS = len(st)
        F = [(a, b2, c2) for a in range(n) for b2 in range(2 * n - 1) for c2 in range(n) if _tri(a, b2, c2) and (a + b2 + c2) % 2 == 0]
        self.F = F
        self.fidx = {s: i for i, s in enumerate(F)}
        self.nF = len(F)
        self._six = {}
        r1, c1, q1, v1 = [], [], [], []
        for (a, b, c) in st:
            for q in range(n):
                for c2 in range(abs(c - q), min(c + q, L) + 1, 2):
                    for b2 in range(abs(b - q), b + q + 1, 2):
                        if not _tri(a, b2, c2):
                            continue
                        x = (-1) ** (a + c + c2) * self.g(b2, q, b) * self.g(c2, q, c) * self.sixj(b2, c2, a, c, b, q)
                        if x != 0.0:
                            r1.append(self.fidx[(a, b2, c2)]); c1.append(self.idx[(a, b, c)]); q1.append(q); v1.append(x)
        self.r1, self.c1, self.q1, self.v1 = np.array(r1), np.array(c1), np.array(q1), np.array(v1)
        r2, c2_, p2, v2 = [], [], [], []
        for (a, b2, c2) in F:
            for p in range(n):
                for a1 in range(abs(a - p), min(a + p, L) + 1, 2):
                    for b1 in range(abs(b2 - p), min(b2 + p, L) + 1, 2):
                        if not _tri(a1, b1, c2):
                            continue
                        x = (-1) ** (a + b1) * self.g(a1, p, a) * self.g(b1, p, b2) * self.sixj(a1, b1, c2, b2, a, p)
                        if x != 0.0:
                            r2.append(self.idx[(a1, b1, c2)]); c2_.append(self.fidx[(a, b2, c2)]); p2.append(p); v2.append(x)
        self.r2, self.c2, self.p2, self.v2 = np.array(r2), np.array(c2_), np.array(p2), np.array(v2)
        self.lab = np.array(st)

    def three0(self, a, b, c):
        """(a b c; 0 0 0) for integer a, b, c"""
        if (a + b + c) % 2 or not _tri(a, b, c):
            return 0.0
        g = (a + b + c) // 2
        lf = self.lf
        lg = 0.5 * (lf[a + b - c] + lf[a - b + c] + lf[-a + b + c] - lf[a + b + c + 1]) + lf[g] - lf[g - a] - lf[g - b] - lf[g - c]
        return (-1) ** g * math.exp(lg)

    def g(self, a, b, c):
        return math.sqrt((2 * a + 1) * (2 * b + 1) * (2 * c + 1)) * self.three0(a, b, c)

    def sixj(self, j1, j2, j3, j4, j5, j6):
        """{j1 j2 j3; j4 j5 j6} for integer spins (Racah formula, log-space terms)"""
        key = (j1, j2, j3, j4, j5, j6)
        if key in self._six:
            return self._six[key]
        lf = self.lf
        if not (_tri(j1, j2, j3) and _tri(j1, j5, j6) and _tri(j4, j2, j6) and _tri(j4, j5, j3)):
            self._six[key] = 0.0
            return 0.0
        def ld(a, b, c):
            return 0.5 * (lf[a + b - c] + lf[a - b + c] + lf[-a + b + c] - lf[a + b + c + 1])
        pre = ld(j1, j2, j3) + ld(j1, j5, j6) + ld(j4, j2, j6) + ld(j4, j5, j3)
        al = [j1 + j2 + j3, j1 + j5 + j6, j4 + j2 + j6, j4 + j5 + j3]
        be = [j1 + j2 + j4 + j5, j2 + j3 + j5 + j6, j3 + j1 + j6 + j4]
        s = 0.0
        for z in range(max(al), min(be) + 1):
            t = lf[z + 1] - sum(lf[z - x] for x in al) - sum(lf[y - z] for y in be)
            s += (-1) ** z * math.exp(t + pre)
        self._six[key] = s
        return s

    def i(self, J):
        l = np.arange(self.n)
        return ive(l + 0.5, J) * math.sqrt(math.pi / (2 * J))          # e^{-J} i_l(J): a common factor per bond

    def r(self, J):
        l = np.arange(self.n)
        return ive(l + 1.5, J) / ive(l + 0.5, J) + l / J                 # d/dJ log i_l(J)

    def A1(self, W):
        return sp.csr_matrix((self.v1 * W[self.q1], (self.r1, self.c1)), shape=(self.nF, self.nS))

    def A2(self, W):
        return sp.csr_matrix((self.v2 * W[self.p2], (self.r2, self.c2)), shape=(self.nS, self.nF))

    def cut(self, W):
        a, b, c = self.lab.T
        return W[a] * W[b] * W[c]

    def vac(self):
        v = np.zeros(self.nS); v[self.idx[(0, 0, 0)]] = 1.0
        return v

    def Z(self, J, ncol, ins=None):
        """Z(P3 x Pn) at uniform J; ins = 'X' or 'Y' puts the energy insertion r on the first column's top (rows 1-2)
        or bottom (rows 2-3) vertical bond, i.e. returns dZ/dJ_e for that bond"""
        W = self.i(J); Wr = W * self.r(J)
        A1, A2 = self.A1(W), self.A2(W)
        sq = np.sqrt(self.cut(W))
        B1 = self.A1(Wr) if ins == 'Y' else A1
        B2 = self.A2(Wr) if ins == 'X' else A2
        b0 = sq * (A2 @ (A1 @ self.vac()))
        b = sq * (B2 @ (B1 @ self.vac()))
        x = b0
        for _ in range(ncol - 2):
            x = sq * (A2 @ (A1 @ (sq * x)))
        return float(b @ x)
