#!/usr/bin/env python3
# pk10 (code): conditional expectations E[P | sigma] as dense vectors over monomials in the Gram variables g_rs of phi_sigma
# (order (0,0),(0,1),(0,2),(1,1),(1,2),(2,2)); sigma X-forms are g_00, g_11, g_22.  Total degree is preserved.
import numpy as np

GV = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
XG = {0: 0, 1: 3, 2: 5}           # sigma X_r -> g index


class GSpace:
    def __init__(self, D):
        self.D, self.B = D, D + 1
        self.pw = np.array([self.B ** i for i in range(6)], dtype=np.int64)
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            codes.append(np.unique((codes[-1][:, None] + self.pw[None, :]).ravel()))
        self.codes = np.unique(np.concatenate(codes))
        self.n = len(self.codes)
        self.deg = self.decode(self.codes).sum(axis=1)
        self._sh = {}

    def decode(self, c):
        return np.stack([(c // self.pw[i]) % self.B for i in range(6)], axis=1)

    def code(self, e):
        return int(sum(int(x) * int(p) for x, p in zip(e, self.pw)))

    def index(self, cs):
        idx = np.searchsorted(self.codes, cs)
        assert np.all(idx < self.n) and np.array_equal(self.codes[idx], cs)
        return idx

    def to_dict(self, v):
        ex = self.decode(self.codes)
        return {tuple(int(x) for x in ex[i]): float(v[i]) for i in np.flatnonzero(v != 0.0)}

    def from_dict(self, P):
        v = np.zeros(self.n)
        if P:
            ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, 6)
            np.add.at(v, self.index(ex @ self.pw), np.array(list(P.values())))
        return v


class CondG:
    def __init__(self, cm, Dout):
        """cm: condexp2.CondMom (gvars GV); output space of total degree <= Dout."""
        self.cm = cm
        self.tab = GSpace(cm.Dc)
        self.out = GSpace(Dout)
        self.vec = {}
        for e2, poly in cm.table.items():
            self.vec[e2] = self.tab.from_dict(poly)
        self.vec[tuple([0] * cm.F)] = self.tab.from_dict({tuple([0] * 6): 1.0})
        self._sh = {}

    def shift(self, eg):
        """map table index -> output index for multiplication by the g-monomial eg (only table entries with deg + |eg| <= Dout)."""
        if eg not in self._sh:
            d = sum(eg)
            src = np.flatnonzero(self.tab.deg + d <= self.out.D)
            ex = self.tab.decode(self.tab.codes[src]) + np.array(eg)[None, :]
            dst = self.out.index(ex @ self.out.pw)
            self._sh[eg] = (src, dst)
        return self._sh[eg]

    def condE(self, P12):
        """P12: dict {12-tuple (sigma X 0-2, sigma Q 3-5 (must be 0), sigma'' 6-11): coeff} -> dense vector over g-monomials."""
        res = np.zeros(self.out.n)
        for e, c in P12.items():
            assert e[3] == e[4] == e[5] == 0, "sigma Q-forms not expected"
            eg = [0] * 6
            for r in range(3):
                eg[XG[r]] = e[r]
            src, dst = self.shift(tuple(eg))
            v = self.vec.get(tuple(e[6:]))
            if v is None:
                raise KeyError(tuple(e[6:]))
            res[dst] += c * v[src]
        return res


def sigma_to_g(P6):
    """polynomial in sigma forms (X_T X_M X_B Q_TM Q_MB Q_TB) -> g variables: X_r = g_rr, Q_rs = g_rr + g_ss - 2 g_rs."""
    lin = {0: {(1, 0, 0, 0, 0, 0): 1.0}, 1: {(0, 0, 0, 1, 0, 0): 1.0}, 2: {(0, 0, 0, 0, 0, 1): 1.0},
           3: {(1, 0, 0, 0, 0, 0): 1.0, (0, 0, 0, 1, 0, 0): 1.0, (0, 1, 0, 0, 0, 0): -2.0},
           4: {(0, 0, 0, 1, 0, 0): 1.0, (0, 0, 0, 0, 0, 1): 1.0, (0, 0, 0, 0, 1, 0): -2.0},
           5: {(1, 0, 0, 0, 0, 0): 1.0, (0, 0, 0, 0, 0, 1): 1.0, (0, 0, 1, 0, 0, 0): -2.0}}
    def mul(P, Q):
        out = {}
        for e1, c1 in P.items():
            for e2, c2 in Q.items():
                e = tuple(x + y for x, y in zip(e1, e2))
                out[e] = out.get(e, 0.0) + c1 * c2
        return out
    cache = {}
    res = {}
    for e, c in P6.items():
        poly = {tuple([0] * 6): 1.0}
        for i, m in enumerate(e):
            for _ in range(m):
                poly = mul(poly, lin[i])
        for eg, cc in poly.items():
            res[eg] = res.get(eg, 0.0) + c * cc
    return {e: c for e, c in res.items() if c != 0.0}
