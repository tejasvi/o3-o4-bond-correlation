#!/usr/bin/env python3
# pk10 (code): ALL Gaussian moments of rank-one quadratic forms Q_f = |sum_v W[v,f] phi_v|^2 (n-component isotropic Gaussian,
# covariance G (x) I_n), for monomials of total degree <= D (optionally with per-group degree caps, e.g. <= 2 in edge forms).
#   M(s) = E exp(sum_f s_f Q_f) = det(I - 2 S Gamma)^{-n/2},  Gamma = W^T G W  (F x F Gram matrix of the forms).
#   det(I - 2 S Gamma) = sum_{subsets A} (-2)^{|A|} det(Gamma_A) s^A  is MULTILINEAR (principal minors), so with D_j its degree-j part
#   (Euler identity D * E(M) = alpha * M * E(D), alpha = -n/2):   k M_k = sum_{j=1}^{min(k,F)} ((1 - n/2) j - k) D_j M_{k-j},
#   moments m_e = e! [s^e] M.  Truncation by total degree and by group degrees is a ring quotient, so the recursion stays exact.
import itertools
import math
import numpy as np


class AllMom2:
    def __init__(self, G, n, D, W=None, groups=None, caps=None, chunk=4000000):
        G = np.asarray(G, dtype=float)
        V = G.shape[0]
        W = np.eye(V) if W is None else np.asarray(W, dtype=float)
        F = W.shape[1]
        self.V, self.F, self.D, self.n, self.chunk = V, F, D, n, chunk
        self.groups = np.zeros(F, dtype=np.int64) if groups is None else np.asarray(groups, dtype=np.int64)
        self.caps = {} if caps is None else dict(caps)
        B = D + 1
        assert float(B) ** F < 9.0e18
        self.B = B
        self.pw = np.array([B ** f for f in range(F)], dtype=np.int64)
        Gam = W.T @ G @ W
        self.Gam = Gam
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            c = np.unique((codes[-1][:, None] + self.pw[None, :]).ravel())
            codes.append(c[self.ok(c)])
        self.codes = codes
        Dj = [None] + [([], []) for j in range(min(F, D))]
        for j in range(1, min(F, D) + 1):
            cs, vs = [], []
            for A in itertools.combinations(range(F), j):
                c = int(sum(self.pw[f] for f in A))
                if not self.ok(np.array([c], dtype=np.int64))[0]:
                    continue
                cs.append(c); vs.append((-2.0) ** j * np.linalg.det(Gam[np.ix_(A, A)]))
            Dj[j] = (np.array(cs, dtype=np.int64), np.array(vs, dtype=float))
        M = [np.ones(1)] + [None] * D
        for k in range(1, D + 1):
            acc = np.zeros(len(codes[k]))
            for j in range(1, min(k, F) + 1):
                cj, vj = Dj[j]
                if len(cj) == 0:
                    continue
                acc += ((1.0 - n / 2.0) * j - k) * self.sprod(cj, vj, M[k - j], k - j, k)
            M[k] = acc / k
        fact = np.array([math.factorial(i) for i in range(D + 1)], dtype=float)
        self.mom = [M[d] * np.prod(fact[self.decode(codes[d])], axis=1) for d in range(D + 1)]

    def ok(self, c):
        if not self.caps:
            return np.ones(len(c), dtype=bool)
        ex = self.decode(c)
        good = np.ones(len(c), dtype=bool)
        for g, cap in self.caps.items():
            good &= ex[:, self.groups == g].sum(axis=1) <= cap
        return good

    def decode(self, c):
        return np.stack([(c // self.pw[f]) % self.B for f in range(self.F)], axis=1)

    def index(self, k, cs):
        idx = np.searchsorted(self.codes[k], cs)
        assert np.all(idx < len(self.codes[k])) and np.array_equal(self.codes[k][idx], cs)
        return idx

    def sprod(self, ca, a, b, db, k):
        """degree-k part of (sparse a with codes ca) * (dense degree-db array b), truncated to the allowed monomials."""
        out = np.zeros(len(self.codes[k]))
        cb = self.codes[db]
        rows = max(1, self.chunk // max(1, len(cb)))
        ck = self.codes[k]
        for s in range(0, len(ca), rows):
            cs = (ca[s:s + rows, None] + cb[None, :]).ravel()
            w = (a[s:s + rows, None] * b[None, :]).ravel()
            idx = np.searchsorted(ck, cs)
            idx[idx >= len(ck)] = 0
            hit = ck[idx] == cs
            out += np.bincount(idx[hit], weights=w[hit], minlength=len(out))
        return out

    def arr(self, P):
        ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, self.F)
        return ex.sum(axis=1), ex @ self.pw, np.array(list(P.values()), dtype=float)

    def E(self, P):
        deg, cs, co = self.arr(P)
        assert deg.max() <= self.D
        return float(sum(np.dot(co[deg == d], self.mom[d][self.index(d, cs[deg == d])]) for d in np.unique(deg)))

    def E2(self, P, Q):
        """E[P Q] without forming the product."""
        dP, cP, aP = self.arr(P)
        dQ, cQ, aQ = self.arr(Q)
        tot = 0.0
        for d1 in np.unique(dP):
            ca, a = cP[dP == d1], aP[dP == d1]
            for d2 in np.unique(dQ):
                cb, b = cQ[dQ == d2], aQ[dQ == d2]
                k = int(d1 + d2)
                assert k <= self.D
                rows = max(1, self.chunk // len(cb))
                for s in range(0, len(ca), rows):
                    idx = self.index(k, (ca[s:s + rows, None] + cb[None, :]).ravel())
                    tot += float(np.dot((a[s:s + rows, None] * b[None, :]).ravel(), self.mom[k][idx]))
        return tot
