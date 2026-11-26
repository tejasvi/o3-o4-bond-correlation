#!/usr/bin/env python3
# pk10 (code): numpy polynomials in nv variables (exponent codes in base B), products by outer code sums.
import numpy as np


class NPoly:
    def __init__(self, nv, B, codes=None, coeffs=None):
        self.nv, self.B = nv, B
        self.pw = np.array([B ** i for i in range(nv)], dtype=np.int64)
        self.codes = np.zeros(0, dtype=np.int64) if codes is None else codes
        self.coeffs = np.zeros(0) if coeffs is None else coeffs

    @classmethod
    def from_dict(cls, P, nv, B):
        p = cls(nv, B)
        if P:
            ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, nv)
            assert ex.max() < B
            p.codes = ex @ p.pw
            p.coeffs = np.array(list(P.values()), dtype=float)
            p._normalize()
        return p

    def _normalize(self):
        if len(self.codes):
            u, inv = np.unique(self.codes, return_inverse=True)
            c = np.bincount(inv, weights=self.coeffs)
            keep = c != 0.0
            self.codes, self.coeffs = u[keep], c[keep]

    def degrees(self):
        return np.stack([(self.codes // self.pw[i]) % self.B for i in range(self.nv)], axis=1).sum(axis=1) if len(self.codes) else np.zeros(0, dtype=np.int64)

    def mul(self, o, chunk=4000000):
        out = NPoly(self.nv, self.B)
        if len(self.codes) == 0 or len(o.codes) == 0:
            return out
        cs, vs = [], []
        rows = max(1, chunk // len(o.codes))
        for s in range(0, len(self.codes), rows):
            cc = (self.codes[s:s + rows, None] + o.codes[None, :]).ravel()
            vv = (self.coeffs[s:s + rows, None] * o.coeffs[None, :]).ravel()
            u, inv = np.unique(cc, return_inverse=True)
            cs.append(u); vs.append(np.bincount(inv, weights=vv))
        out.codes = np.concatenate(cs); out.coeffs = np.concatenate(vs)
        out._normalize()
        return out

    def power(self, k):
        res = NPoly(self.nv, self.B, np.zeros(1, dtype=np.int64), np.ones(1))
        base = self
        while k > 0:
            if k & 1:
                res = res.mul(base)
            k >>= 1
            if k:
                base = base.mul(base)
        return res

    def scale(self, s):
        return NPoly(self.nv, self.B, self.codes.copy(), self.coeffs * s)

    def add(self, o):
        out = NPoly(self.nv, self.B, np.concatenate([self.codes, o.codes]), np.concatenate([self.coeffs, o.coeffs]))
        out._normalize()
        return out

    def to_dict(self):
        ex = np.stack([(self.codes // self.pw[i]) % self.B for i in range(self.nv)], axis=1)
        return {tuple(int(x) for x in row): float(c) for row, c in zip(ex, self.coeffs)}

    def project(self, idx):
        """keep only variables idx (asserting the others have exponent 0); returns NPoly in len(idx) variables, same base."""
        ex = np.stack([(self.codes // self.pw[i]) % self.B for i in range(self.nv)], axis=1)
        other = [i for i in range(self.nv) if i not in idx]
        if len(self.codes) and other and ex[:, other].max() > 0:
            return None
        p = NPoly(len(idx), self.B)
        p.codes = ex[:, idx] @ p.pw if len(self.codes) else np.zeros(0, dtype=np.int64)
        p.coeffs = self.coeffs.copy()
        p._normalize()
        return p
