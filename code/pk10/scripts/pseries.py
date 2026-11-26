#!/usr/bin/env python3
# pk10 (code): truncated power series in t whose coefficients are polynomials (dicts {exponent tuple: coeff}) in nv variables.
import math


def padd(*Ps):
    out = {}
    for P in Ps:
        for e, c in P.items():
            out[e] = out.get(e, 0.0) + c
    return {e: c for e, c in out.items() if c != 0.0}


def pscale(P, s):
    return {e: c * s for e, c in P.items()} if s != 0.0 else {}


def pmul(P, Q):
    out = {}
    for e1, c1 in P.items():
        for e2, c2 in Q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, 0.0) + c1 * c2
    return {e: c for e, c in out.items() if c != 0.0}


def pconst(c, nv):
    return {tuple([0] * nv): c} if c != 0.0 else {}


def pvar(i, nv, c=1.0):
    e = [0] * nv; e[i] = 1
    return {tuple(e): c}


class Series:
    """sum_{k=0}^K t^k P_k, P_k polynomials in nv variables."""
    def __init__(self, K, nv, coeffs=None):
        self.K, self.nv = K, nv
        self.c = [dict(p) for p in coeffs] if coeffs is not None else [{} for _ in range(K + 1)]
        while len(self.c) < K + 1:
            self.c.append({})

    def copy(self):
        return Series(self.K, self.nv, self.c)

    def __add__(self, o):
        return Series(self.K, self.nv, [padd(a, b) for a, b in zip(self.c, o.c)])

    def __sub__(self, o):
        return Series(self.K, self.nv, [padd(a, pscale(b, -1.0)) for a, b in zip(self.c, o.c)])

    def scale(self, s):
        return Series(self.K, self.nv, [pscale(a, s) for a in self.c])

    def __mul__(self, o):
        out = [{} for _ in range(self.K + 1)]
        for i in range(self.K + 1):
            if not self.c[i]:
                continue
            for j in range(self.K + 1 - i):
                if o.c[j]:
                    out[i + j] = padd(out[i + j], pmul(self.c[i], o.c[j]))
        return Series(self.K, self.nv, out)

    def exp(self):
        """exp of a series with zero constant term (checked): E = sum, k E_k = sum_{j=1}^k j H_j E_{k-j}."""
        assert not any(abs(c) > 0 for c in self.c[0].values()), "exp needs H_0 = 0"
        E = [pconst(1.0, self.nv)] + [{} for _ in range(self.K)]
        for k in range(1, self.K + 1):
            acc = {}
            for j in range(1, k + 1):
                if self.c[j] and E[k - j]:
                    acc = padd(acc, pscale(pmul(self.c[j], E[k - j]), float(j)))
            E[k] = pscale(acc, 1.0 / k)
        return Series(self.K, self.nv, E)


def w_coeffs(K):
    """w(x, y) = (sqrt(1 - x) + sqrt(1 - y))^{-2} = sum w[i][j] x^i y^j, total degree <= K (exact rational arithmetic via floats)."""
    sq = [math.comb(2 * k, k) * (-1) ** 0 / (4 ** k * (2 * k - 1)) * (-1.0) for k in range(K + 1)]
    # sqrt(1 - x) = 1 - sum_{k>=1} C(2k,k) x^k / (4^k (2k - 1))
    s = [1.0] + [-math.comb(2 * k, k) / (4 ** k * (2 * k - 1)) for k in range(1, K + 1)]
    # u(x, y) = s(x) + s(y) = 2 + d(x, y), d with zero constant; w = (2 + d)^{-2} = (1/4) sum_m (m + 1) (-d/2)^m
    d = {}
    for k in range(1, K + 1):
        d[(k, 0)] = d.get((k, 0), 0.0) + s[k]
        d[(0, k)] = d.get((0, k), 0.0) + s[k]
    def mul2(A, Bp):
        out = {}
        for (i1, j1), c1 in A.items():
            for (i2, j2), c2 in Bp.items():
                if i1 + i2 + j1 + j2 <= K:
                    out[(i1 + i2, j1 + j2)] = out.get((i1 + i2, j1 + j2), 0.0) + c1 * c2
        return out
    w = {(0, 0): 0.25}
    pw = {(0, 0): 1.0}
    hd = {k: -v / 2.0 for k, v in d.items()}
    for m in range(1, K + 1):
        pw = mul2(pw, hd)
        for k, v in pw.items():
            w[k] = w.get(k, 0.0) + 0.25 * (m + 1) * v
    return w
