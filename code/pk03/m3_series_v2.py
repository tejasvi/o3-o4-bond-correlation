#!/usr/bin/env python3
"""m3_series_v2.py -- pk03 (code/pk03/). Truncated t-series of polynomials on the kernel's SPoly (PLAN_M3_CODE_v1_2 sect. A):
REVISION of m3_series_v1.py (8479ca30): imports the generic module names (m3_scal, m3_graph, m3_series, m3_major), which the job scripts load from sha-pinned files;
kernel polynomials take arb coefficients only (m3_scal.spoly/ka) and mp.iv views come through m3_scal.arb_to_iv, since arbeng_ma_stub_v1's mpi_to_arb drops the sign of negative ends (m3_smoke_v2 d4).
riglap2's Model (meas, Faddeev-Popov, anh, xi, H) and riglap3's Model3.Fser for the factor kinds 'p', 'xi' and 'const' (the kinds of
M3_ENTRY_LIST_v1_1; 'dot' is refused), term for term as pk10's pseries / riglap2 / riglap3. Rational constants are exact Fractions
(w_coeffs, 1/(2k), C(2k,k)/(4^k (2k-1)), -n/m, 1/k); couplings are mp.iv intervals; trial coefficients and kbar enter as exact binary64.
The kernel module (arbeng_ma_stub_v1 or arbeng_ma_v1, pinned by the job script) is passed in; this module has no compute of its own.
"""
import math
from fractions import Fraction
import m3_scal as S

BASIS9 = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]


def w_coeffs(K):
    """pseries.w_coeffs exactly: w(x, y) = (sqrt(1 - x) + sqrt(1 - y))^-2 = (1/4) sum_m (m + 1) (-d/2)^m, d = s(x) + s(y) - 2,
    s(x) = sqrt(1 - x) = 1 - sum_k C(2k, k) x^k/(4^k (2k - 1)), truncated at total degree K."""
    s = [Fraction(1)] + [Fraction(-math.comb(2 * k, k), 4 ** k * (2 * k - 1)) for k in range(1, K + 1)]
    d = {}
    for k in range(1, K + 1):
        d[(k, 0)] = d.get((k, 0), Fraction(0)) + s[k]
        d[(0, k)] = d.get((0, k), Fraction(0)) + s[k]

    def mul2(A, B):
        out = {}
        for (i1, j1), c1 in A.items():
            for (i2, j2), c2 in B.items():
                if i1 + i2 + j1 + j2 <= K:
                    key = (i1 + i2, j1 + j2)
                    out[key] = out.get(key, Fraction(0)) + c1 * c2
        return out
    w = {(0, 0): Fraction(1, 4)}
    pw = {(0, 0): Fraction(1)}
    hd = {k: -v / 2 for k, v in d.items()}
    for m in range(1, K + 1):
        pw = mul2(pw, hd)
        for k, v in pw.items():
            w[k] = w.get(k, Fraction(0)) + Fraction(m + 1, 4) * v
    return w


class Series:
    """sum_{k <= K} t^k P_k with P_k SPoly polynomials in nv variables (pseries.Series)."""
    def __init__(self, kern, K, nv, coeffs=None):
        self.kern, self.K, self.nv = kern, K, nv
        c = list(coeffs) if coeffs is not None else []
        while len(c) < K + 1:
            c.append(kern.SPoly(nv))
        assert len(c) == K + 1 and all(p.nv == nv for p in c)
        self.c = c

    def __add__(self, o):
        return Series(self.kern, self.K, self.nv, [a.add(b) for a, b in zip(self.c, o.c)])

    def __sub__(self, o):
        return Series(self.kern, self.K, self.nv, [a.sub(b) for a, b in zip(self.c, o.c)])

    def scale(self, s):
        return Series(self.kern, self.K, self.nv, [a.scale(S.ka(s)) for a in self.c])

    def __mul__(self, o):
        out = [self.kern.SPoly(self.nv) for _ in range(self.K + 1)]
        for i in range(self.K + 1):
            if not self.c[i].to_arb_dict():
                continue
            for j in range(self.K + 1 - i):
                if o.c[j].to_arb_dict():
                    out[i + j] = out[i + j].add(self.c[i].mul(o.c[j]))
        return Series(self.kern, self.K, self.nv, out)

    def shift(self, sh):
        """t^sh times the series, truncated at K."""
        return Series(self.kern, self.K, self.nv, [self.kern.SPoly(self.nv) for _ in range(sh)] + self.c[:self.K + 1 - sh])

    def exp(self):
        """exp of a series with zero constant term (checked): k E_k = sum_{j=1}^k j H_j E_{k-j} (pseries.Series.exp)."""
        assert not self.c[0].to_arb_dict(), 'exp needs H_0 = 0'
        E = [S.spoly(self.kern, {tuple([0] * self.nv): 1}, self.nv)] + [self.kern.SPoly(self.nv) for _ in range(self.K)]
        for k in range(1, self.K + 1):
            acc = self.kern.SPoly(self.nv)
            for j in range(1, k + 1):
                if self.c[j].to_arb_dict() and E[k - j].to_arb_dict():
                    acc = acc.add(self.c[j].mul(E[k - j]).scale(S.ka(j)))
            E[k] = acc.div_int(k)
        return Series(self.kern, self.K, self.nv, E)


class Model:
    """riglap2.Model and riglap3.Model3 on a GraphIV g; factors: ('p', (T, M, B), q1, q2, q3), ('xi', (T, M, B), c0, c9), ('const', c)."""
    def __init__(self, kern, g, K, factors):
        self.kern, self.g, self.K, self.factors = kern, g, K, list(factors)
        self.NV = g.F
        self.w = w_coeffs(K + 2)

    def poly(self, d):
        return S.spoly(self.kern, d, self.NV)

    def xv(self, i, k=1, c=1):
        e = [0] * self.NV
        e[i] = k
        return self.poly({tuple(e): c})

    def const(self, c):
        return self.poly({tuple([0] * self.NV): c}) if c != 0 else self.kern.SPoly(self.NV)

    def S(self, coeffs, K=None):
        return Series(self.kern, self.K if K is None else K, self.NV, coeffs)

    def anh(self, iu, iv_, c, K):
        """sum_k t^k (-c/2) sum_{1+i+j=k} w_ij (X_u - X_v)^2 X_u^i X_v^j (riglap2.Model.anh), coefficients combined exactly in mp.iv."""
        cc = S.I(c)
        out = [dict() for _ in range(K + 1)]
        for (i, j), cw in self.w.items():
            k = 1 + i + j
            if k > K:
                continue
            coef = -cc * S.I(cw) / 2
            for pu, pv, sg in ((2, 0, 1), (1, 1, -2), (0, 2, 1)):
                e = [0] * self.NV
                e[iu] += i + pu
                e[iv_] += j + pv
                e = tuple(e)
                out[k][e] = out[k][e] + coef * sg if e in out[k] else coef * sg
        return self.S([self.poly(d) for d in out], K)

    def xi(self, u, v, K):
        """xi_uv = Q_uv/2 - anh(u, v, 1) (riglap2.Model.xi)."""
        base = self.S([self.xv(self.g.qidx(u, v), 1, Fraction(1, 2))], K)
        return base - self.anh(u, v, 1, K)

    def H(self, K):
        V, n = self.g.V, self.g.n
        Hs = self.S(None, K)
        for v in range(V):
            Hs = Hs + self.S([self.kern.SPoly(self.NV)] + [self.xv(v, k, Fraction(1, 2 * k)) for k in range(1, K + 1)], K)
        b = [Fraction(0)] + [Fraction(math.comb(2 * k, k), 4 ** k * (2 * k - 1)) for k in range(1, K + 1)]
        y = self.S(None, K)
        for v in range(V):
            y = y + self.S([self.kern.SPoly(self.NV)] + [self.xv(v, k, b[k] / V) for k in range(1, K + 1)], K)
        y_m = y
        FP = self.S(None, K)
        for m in range(1, K + 1):
            FP = FP + y_m.scale(S.ka(Fraction(-n, m)))
            y_m = y_m * y
        Hs = Hs + FP
        for (u, v), c in self.g.c.items():
            Hs = Hs + self.anh(u, v, c, K)
        return Hs

    def Fser(self, K):
        """the product of the factors' series (riglap2.Model.Fser for 'const' and 'p', then riglap3.Model3's 'xi' factors)."""
        one = self.S([self.const(1)], K)
        Fs = one
        for f in self.factors:
            if f[0] == 'const':
                Fs = Fs.scale(S.ka(f[1]))
            elif f[0] == 'p':
                _, col, q1, q2, q3 = f
                T, M, B = col
                xs = [self.xi(T, M, K), self.xi(M, B, K), self.xi(T, B, K)]
                P = one
                for coef, sh in ((q1, 1), (q2, 2), (q3, 3)):
                    for cb, mono in zip(coef, BASIS9):
                        if cb == 0.0 or sh > K:
                            continue
                        fbs = one
                        for p_ in mono:
                            fbs = fbs * xs[p_]
                        P = P + fbs.shift(sh).scale(S.ka(cb))
                Fs = Fs * P
            elif f[0] != 'xi':
                raise ValueError('factor kind %r is not supported' % (f[0],))
        for f in self.factors:
            if f[0] != 'xi':
                continue
            _, col, c0, c9 = f
            T, M, B = col
            prs = [(T, M), (M, B), (T, B)]
            need = sorted({p_ for cb, mono in zip(c9, BASIS9) if cb != 0.0 for p_ in mono})
            xs = {p_: self.xi(prs[p_][0], prs[p_][1], K) for p_ in need}
            P = self.S([self.const(c0)], K)
            for cb, mono in zip(c9, BASIS9):
                if cb == 0.0:
                    continue
                fbs = one
                for p_ in mono:
                    fbs = fbs * xs[p_]
                P = P + fbs.scale(S.ka(cb))
            Fs = Fs * P
        return Fs
