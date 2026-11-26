#!/usr/bin/env python3
# pk10 (code): moments of the Gram matrix g = sum_{c=1}^n phi^(c) phi^(c)T, phi^(c) ~ N(0, G) i.i.d. (Wishart), variables g_rs (r <= s).
#   E exp(sum_{r<=s} s_rs g_rs) = det(I - 2 S G)^{-n/2},  S_rr = s_rr, S_rs = s_rs / 2;  D(s) = det(I - 2 S G) is a polynomial of
#   degree <= m (m = G.shape[0]); Euler identity: k M_k = sum_j ((1 - n/2) j - k) D_j M_{k-j};  E[prod g^e] = e! [s^e] M.
import math, itertools
import numpy as np


class Wishart:
    def __init__(self, G, n, D, chunk=4000000):
        G = np.asarray(G, dtype=float)
        m = G.shape[0]
        self.vars = [(r, s) for r in range(m) for s in range(r, m)]
        F = len(self.vars)
        self.F, self.D, self.n = F, D, n
        B = D + 1
        self.B = B
        self.pw = np.array([B ** i for i in range(F)], dtype=np.int64)
        # polynomial entries of I - 2 S G: dict {exponent tuple: coeff}
        def var(i, c):
            e = [0] * F; e[i] = 1
            return {tuple(e): c}
        Sm = [[{} for _ in range(m)] for _ in range(m)]
        for i, (r, s) in enumerate(self.vars):
            if r == s:
                Sm[r][r] = var(i, 1.0)
            else:
                Sm[r][s] = var(i, 0.5); Sm[s][r] = var(i, 0.5)
        def padd(*Ps):
            out = {}
            for P in Ps:
                for e, c in P.items():
                    out[e] = out.get(e, 0.0) + c
            return {e: c for e, c in out.items() if c != 0.0}
        def pmul(P, Q):
            out = {}
            for e1, c1 in P.items():
                for e2, c2 in Q.items():
                    e = tuple(x + y for x, y in zip(e1, e2))
                    out[e] = out.get(e, 0.0) + c1 * c2
            return out
        zero = tuple([0] * F)
        Mx = [[padd({zero: 1.0} if r == s else {}, *[{e: -2.0 * c * G[k, s] for e, c in Sm[r][k].items()} for k in range(m)]) for s in range(m)] for r in range(m)]
        det = {}
        for perm in itertools.permutations(range(m)):
            sign = np.linalg.det(np.eye(m)[list(perm)])
            term = {zero: float(round(sign))}
            for r in range(m):
                term = pmul(term, Mx[r][perm[r]])
            det = padd(det, term)
        Dj = {}
        for e, c in det.items():
            Dj.setdefault(sum(e), []).append((e, c))
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            codes.append(np.unique((codes[-1][:, None] + self.pw[None, :]).ravel()))
        self.codes = codes
        Dc = {j: (np.array([sum(int(x) * int(p) for x, p in zip(e, self.pw)) for e, c in lst], dtype=np.int64),
                  np.array([c for e, c in lst])) for j, lst in Dj.items() if j > 0}
        M = [np.ones(1)] + [None] * D
        for k in range(1, D + 1):
            acc = np.zeros(len(codes[k]))
            for j, (cj, vj) in Dc.items():
                if j > k:
                    continue
                ck = codes[k - j]
                rows = max(1, chunk // len(ck))
                for s0 in range(0, len(cj), rows):
                    cs = (cj[s0:s0 + rows, None] + ck[None, :]).ravel()
                    w = (vj[s0:s0 + rows, None] * M[k - j][None, :]).ravel()
                    idx = np.searchsorted(codes[k], cs)
                    acc += ((1.0 - n / 2.0) * j - k) * np.bincount(idx, weights=w, minlength=len(acc))
            M[k] = acc / k
        fact = np.array([math.factorial(i) for i in range(D + 1)], dtype=float)
        self.mom = [M[d] * np.prod(fact[self.decode(codes[d])], axis=1) for d in range(D + 1)]

    def decode(self, c):
        return np.stack([(c // self.pw[i]) % self.B for i in range(self.F)], axis=1)

    def index(self, k, cs):
        idx = np.searchsorted(self.codes[k], cs)
        assert np.all(idx < len(self.codes[k])) and np.array_equal(self.codes[k][idx], cs)
        return idx

    def E(self, P):
        if not P:
            return 0.0
        ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, self.F)
        deg = ex.sum(axis=1); cs = ex @ self.pw; co = np.array(list(P.values()))
        return float(sum(np.dot(co[deg == d], self.mom[d][self.index(d, cs[deg == d])]) for d in np.unique(deg)))

    def E2(self, P, Q, chunk=4000000):
        ex1 = np.array(list(P.keys()), dtype=np.int64).reshape(-1, self.F); c1 = np.array(list(P.values()))
        ex2 = np.array(list(Q.keys()), dtype=np.int64).reshape(-1, self.F); c2 = np.array(list(Q.values()))
        d1, d2 = ex1.sum(axis=1), ex2.sum(axis=1)
        k1, k2 = ex1 @ self.pw, ex2 @ self.pw
        tot = 0.0
        for a_ in np.unique(d1):
            ca, va = k1[d1 == a_], c1[d1 == a_]
            for b_ in np.unique(d2):
                cb, vb = k2[d2 == b_], c2[d2 == b_]
                k = int(a_ + b_)
                assert k <= self.D
                rows = max(1, chunk // len(cb))
                for s0 in range(0, len(ca), rows):
                    idx = self.index(k, (ca[s0:s0 + rows, None] + cb[None, :]).ravel())
                    tot += float(np.dot((va[s0:s0 + rows, None] * vb[None, :]).ravel(), self.mom[k][idx]))
        return tot
