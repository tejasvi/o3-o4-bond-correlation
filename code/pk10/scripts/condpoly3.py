#!/usr/bin/env python3
# pk10 (code): vectorized conditional expectations E[P(sigma forms, sigma'' forms) | sigma] as dense vectors over sigma-form monomials.
# sigma forms (6): X_T X_M X_B Q_TM Q_MB Q_TB; Gram g_rr = X_r, g_rs = (X_r + X_s - Q_rs)/2 (rs = TM, MB, TB).
import math
import numpy as np

PAIRS = [(0, 1), (1, 2), (0, 2)]


class SigmaPolys:
    """dense representation of polynomials of degree <= D in 6 variables."""
    def __init__(self, D):
        self.D = D
        self.B = D + 1
        self.pw = np.array([self.B ** i for i in range(6)], dtype=np.int64)
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            codes.append(np.unique((codes[-1][:, None] + self.pw[None, :]).ravel()))
        self.codes = np.unique(np.concatenate(codes))
        self.n = len(self.codes)
        self.deg = self.decode(self.codes).sum(axis=1)
        self._shifts = {}

    def decode(self, c):
        return np.stack([(c // self.pw[i]) % self.B for i in range(6)], axis=1)

    def code(self, e):
        return int(sum(int(x) * int(p) for x, p in zip(e, self.pw)))

    def index(self, cs):
        idx = np.searchsorted(self.codes, cs)
        assert np.all(idx < self.n) and np.array_equal(self.codes[idx], cs)
        return idx

    def shift(self, e):
        """(src, dst): multiplication by the monomial e maps entry src to dst (sources with deg + |e| <= D)."""
        e = tuple(int(x) for x in e)
        if e not in self._shifts:
            de = sum(e)
            src = np.flatnonzero(self.deg + de <= self.D)
            dst = self.index(self.codes[src] + self.code(e))
            self._shifts[e] = (src, dst)
        return self._shifts[e]

    def from_dict(self, P):
        v = np.zeros(self.n)
        for e, c in P.items():
            v[self.index(np.array([self.code(e)]))[0]] += c
        return v

    def to_dict(self, v):
        ex = self.decode(self.codes)
        return {tuple(int(x) for x in ex[i]): float(v[i]) for i in np.flatnonzero(v != 0.0)}

    def mul_mono(self, v, e, c=1.0):
        out = np.zeros(self.n)
        src, dst = self.shift(e)
        out[dst] = c * v[src]
        return out


class CondSigma:
    def __init__(self, cm, sp):
        """cm: condexp2.CondMom over the 6 sigma'' forms, gvars (0,0),(0,1),(0,2),(1,1),(1,2),(2,2); sp: SigmaPolys(D >= cm.Dc)."""
        self.cm, self.sp = cm, sp
        self.lin = []
        for (r, s) in cm.gvars:
            if r == s:
                self.lin.append({r: 1.0})
            else:
                self.lin.append({r: 0.5, s: 0.5, 3 + PAIRS.index((r, s)): -0.5})
        self.gcache = {}
        self.vec = {}
        for e2, poly in cm.table.items():
            out = np.zeros(sp.n)
            for gexp, c in poly.items():
                out += c * self.gpoly(gexp)
            self.vec[e2] = out
        self.vec[tuple([0] * cm.F)] = self.gpoly(tuple([0] * len(cm.gvars)))

    def gpoly(self, gexp):
        if gexp in self.gcache:
            return self.gcache[gexp]
        if sum(gexp) == 0:
            v = np.zeros(self.sp.n); v[0] = 1.0
        else:
            i = next(j for j, m in enumerate(gexp) if m > 0)
            prev = list(gexp); prev[i] -= 1
            pv = self.gpoly(tuple(prev))
            v = np.zeros(self.sp.n)
            for k, c in self.lin[i].items():
                e = [0] * 6; e[k] = 1
                src, dst = self.sp.shift(e)
                v[dst] += c * pv[src]
        self.gcache[gexp] = v
        return v

    def condE(self, P):
        """P: dict {12-tuple (sigma 6, sigma'' 6): coeff} -> dense vector over sigma monomials."""
        out = np.zeros(self.sp.n)
        for e, c in P.items():
            es, e2 = tuple(e[:6]), tuple(e[6:])
            v = self.vec.get(e2)
            if v is None:
                raise KeyError("conditional moment not tabulated for %s" % (e2,))
            src, dst = self.sp.shift(es)
            out[dst] += c * v[src]
        return out
