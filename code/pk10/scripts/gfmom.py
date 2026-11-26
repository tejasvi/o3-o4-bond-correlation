#!/usr/bin/env python3
# pk10 (code): moments of products of GENERAL quadratic forms Q_f = y^T B_f y of a real Gaussian vector y ~ N(0, C) (any dimension),
# for all monomials of degree <= D:  log E exp(sum s_f Q_f) = (1/2) sum_m (2^m/m) tr((sum_f s_f B_f C)^m);  exp by homogeneous recursion.
import math
import numpy as np


class GFMom:
    def __init__(self, Bs, C, D, chunk=4000000):
        F = len(Bs)
        d = C.shape[0]
        self.F, self.D = F, D
        B = D + 1
        self.B = B
        self.pw = np.array([B ** i for i in range(F)], dtype=np.int64)
        codes = [np.zeros(1, dtype=np.int64)]
        for k in range(1, D + 1):
            codes.append(np.unique((codes[-1][:, None] + self.pw[None, :]).ravel()))
        self.codes = codes
        BC = [Bf @ C for Bf in Bs]
        # A_m as array [monomial(deg m), d, d]
        A = np.zeros((len(codes[1]), d, d))
        for f in range(F):
            A[np.searchsorted(codes[1], self.pw[f])] = BC[f]
        Fl = [None] * (D + 1)
        Fl[1] = 0.5 * 2.0 * np.einsum('mii->m', A)
        for m in range(2, D + 1):
            new = np.zeros((len(codes[m]), d, d))
            for f in range(F):
                idx = np.searchsorted(codes[m], codes[m - 1] + self.pw[f])
                new[idx] += A @ BC[f]
            A = new
            Fl[m] = 0.5 * (2.0 ** m / m) * np.einsum('mii->m', A)
        Ms = [np.ones(1)]
        for k in range(1, D + 1):
            acc = np.zeros(len(codes[k]))
            for j in range(1, k + 1):
                ca, a = codes[j], j * Fl[j]
                cb, b = codes[k - j], Ms[k - j]
                rows = max(1, chunk // len(cb))
                for s0 in range(0, len(ca), rows):
                    cs = (ca[s0:s0 + rows, None] + cb[None, :]).ravel()
                    idx = np.searchsorted(codes[k], cs)
                    acc += np.bincount(idx, weights=(a[s0:s0 + rows, None] * b[None, :]).ravel(), minlength=len(acc))
            Ms.append(acc / k)
        fact = np.array([math.factorial(i) for i in range(D + 1)], dtype=float)
        self.mom = [Ms[k] * np.prod(fact[self.decode(codes[k])], axis=1) for k in range(D + 1)]

    def decode(self, c):
        return np.stack([(c // self.pw[i]) % self.B for i in range(self.F)], axis=1)

    def E(self, P):
        if not P:
            return 0.0
        ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, self.F)
        deg = ex.sum(axis=1); cs = ex @ self.pw; co = np.array(list(P.values()))
        tot = 0.0
        for d in np.unique(deg):
            m = deg == d
            idx = np.searchsorted(self.codes[d], cs[m])
            assert np.array_equal(self.codes[d][idx], cs[m])
            tot += float(np.dot(co[m], self.mom[d][idx]))
        return tot
