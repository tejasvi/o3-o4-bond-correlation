#!/usr/bin/env python3
"""m3_major_v2.py -- pk03 (code/pk03/). Positive majorants of riglap2.Majorants and riglap3.Majorants3 on the kernel's SPoly
REVISION of m3_major_v1.py (73c1f820): imports the generic module names (m3_scal, m3_graph, m3_series, m3_major), which the job scripts load from sha-pinned files;
kernel polynomials take arb coefficients only (m3_scal.spoly/ka) and mp.iv views come through m3_scal.arb_to_iv, since arbeng_ma_stub_v1's mpi_to_arb drops the sign of negative ends (m3_smoke_v2 d4).
(PLAN_M3_CODE_v1_2 sect. A): hbar_k, xibar, partial Bell polynomials, factor_bar for 'p', 'xi' and 'const', Fbar (Leibniz over the factors),
Dbar (riglap2's remainder majorant) and riglap5.hhat2, term for term. Every constant ((1 - a)^-k, (1 - a)^(1/2 - j), 1/(1 - ymax)^m, t^i,
factorials, the couplings) is an mp.iv interval, so each coefficient is an enclosure of its exact value; the expectations of these
majorants are taken as enclosures and only their upper ends are used. No compute of its own.
"""
import math
from fractions import Fraction
from mpmath import iv
import m3_scal as S
from m3_series import BASIS9


class Majorants:
    def __init__(self, kern, model, avec, t):
        """model: m3_series_v1.Model (its graph and factors); avec: the radii a_v (binary64); t: an exact Fraction or binary64."""
        self.kern, self.m, self.g = kern, model, model.g
        self.a = [S.I(x) for x in avec]
        self.af = list(avec)
        self.t = S.I(t)
        self.NV = model.NV
        self.ONE = self.mono([0] * self.NV, 1)
        self.ZERO = kern.SPoly(self.NV)

    def mono(self, e, c=1):
        return S.spoly(self.kern, {tuple(e): c}, self.NV)

    def xv(self, i, k=1, c=1):
        e = [0] * self.NV
        e[i] = k
        return self.mono(e, c)

    def D2(self, i, j):
        return self.xv(i, 2).add(self.xv(i, 1).mul(self.xv(j, 1)).scale(S.ka(-2))).add(self.xv(j, 2))

    def Mk(self, i, j, k):
        return self.ONE if k == 0 else self.xv(i, k).add(self.xv(j, k))

    def partial_bell(self, k, m, xs):
        """B_{k,m}(xs[1], xs[2], ...) by B_{k,m} = sum_i C(k-1, i-1) x_i B_{k-i, m-1} (riglap2.Majorants.partial_bell)."""
        memo = {}

        def rec(kk, mm):
            if (kk, mm) in memo:
                return memo[(kk, mm)]
            if kk == 0 and mm == 0:
                r = self.ONE
            elif kk == 0 or mm == 0:
                r = self.ZERO
            else:
                r = self.ZERO
                for i in range(1, kk - mm + 2):
                    r = r.add(xs[i].mul(rec(kk - i, mm - 1)).scale(S.ka(math.comb(kk - 1, i - 1))))
            memo[(kk, mm)] = r
            return r
        return rec(k, m)

    def hbar(self, k):
        """majorant of sup_{tau <= t} |H^(k)(tau)| on Omega(a) (riglap2.Majorants.hbar)."""
        V, a = self.g.V, self.a
        out = self.ZERO
        for v in range(V):
            out = out.add(self.xv(v, k, math.factorial(k - 1) / (2 * S.ipow(1 - a[v], k))))
        for (u, v), c in self.g.c.items():
            ae = a[u] if self.af[u] >= self.af[v] else a[v]
            out = out.add(self.D2(u, v).mul(self.Mk(u, v, k - 1)).scale(S.ka((c / 2) * math.factorial(k) / (4 * S.ipow(1 - ae, k + 1)))))
        ymax = S.isum(a[v] / (2 - a[v]) for v in range(V)) / V

        def cj(j):
            df = 1
            for q in range(2 * j - 3, 0, -2):
                df *= q
            return Fraction(df, 2 ** j)
        ys = [None]
        for j in range(1, k + 1):
            yj = self.ZERO
            for v in range(V):
                yj = yj.add(self.xv(v, j, S.I(cj(j)) * iv.sqrt(1 - a[v]) / S.ipow(1 - a[v], j) / V))
            ys.append(yj)
        fp = self.ZERO
        for mm in range(1, k + 1):
            fp = fp.add(self.partial_bell(k, mm, ys).scale(S.ka(self.g.n * math.factorial(mm - 1) / S.ipow(1 - ymax, mm))))
        return out.add(fp)

    def xibar(self, u, v, l, aa):
        """majorant of xi_uv^(l)(tau), tau <= t (xi = Q/2 + (1/2) D W(tau)) (riglap2.Majorants.xibar)."""
        D = self.D2(u, v)
        if l == 0:
            return self.xv(self.g.qidx(u, v), 1, Fraction(1, 2)).add(D.scale(S.ka(self.t / (8 * (1 - aa)))))
        return D.mul(self.Mk(u, v, l - 1)).scale(S.ka(math.factorial(l) / (8 * S.ipow(1 - aa, l + 1))))

    def _aa(self, u, v):
        return self.a[u] if self.af[u] >= self.af[v] else self.a[v]

    def _fbd(self, prs, mono, n):
        if len(mono) == 1:
            u, v = prs[mono[0]]
            return self.xibar(u, v, n, self._aa(u, v))
        (u1, v1), (u2, v2) = prs[mono[0]], prs[mono[1]]
        out = self.ZERO
        for l in range(n + 1):
            out = out.add(self.xibar(u1, v1, l, self._aa(u1, v1)).mul(self.xibar(u2, v2, n - l, self._aa(u2, v2))).scale(S.ka(math.comb(n, l))))
        return out

    def factor_bar(self, f, j):
        """majorant of the j-th tau-derivative of one factor (riglap2.Majorants.factor_bar for 'const' and 'p', riglap3's for 'xi')."""
        if f[0] == 'const':
            return self.ONE.scale(S.ka(abs(f[1]))) if j == 0 else self.ZERO
        if f[0] == 'p':
            _, col, q1, q2, q3 = f
            T, M, Bv = col
            prs = [(T, M), (M, Bv), (T, Bv)]
            out = self.ONE if j == 0 else self.ZERO
            for i, coef in ((1, q1), (2, q2), (3, q3)):
                for cb, mono in zip(coef, BASIS9):
                    if cb == 0.0:
                        continue
                    for l in range(0, min(i, j) + 1):
                        cf = math.comb(j, l) * (math.factorial(i) // math.factorial(i - l)) * S.ipow(self.t, i - l) * S.I(abs(cb))
                        out = out.add(self._fbd(prs, mono, j - l).scale(S.ka(cf)))
            return out
        if f[0] == 'xi':
            _, col, c0, c9 = f
            T, M, Bv = col
            prs = [(T, M), (M, Bv), (T, Bv)]
            out = self.ONE.scale(S.ka(abs(c0))) if j == 0 else self.ZERO
            for cb, mono in zip(c9, BASIS9):
                if cb != 0.0:
                    out = out.add(self._fbd(prs, mono, j).scale(S.ka(abs(cb))))
            return out
        raise ValueError('factor kind %r is not supported' % (f[0],))

    def Fbar(self, j):
        """Leibniz over the factors (riglap2.Majorants.Fbar)."""
        facs = self.m.factors
        if not facs:
            return self.ONE if j == 0 else self.ZERO
        cache = {}

        def fb(i, jj):
            if (i, jj) not in cache:
                cache[(i, jj)] = self.factor_bar(facs[i], jj)
            return cache[(i, jj)]
        out = self.ZERO
        for js in _compositions(j, len(facs)):
            term = self.ONE.scale(S.ka(Fraction(math.factorial(j), math.prod(math.factorial(x) for x in js))))
            for i, ji in enumerate(js):
                term = term.mul(fb(i, ji))
            out = out.add(term)
        return out

    def Dbar(self, n):
        """riglap2.Majorants.Dbar: Y_0 = 1, Y_{m+1} = sum_i C(m, i) hbar_{i+1} Y_{m-i}; Dbar_n = sum_j C(n, j) Fbar_j Y_{n-j}."""
        h = {k: self.hbar(k) for k in range(1, n + 1)}
        Y = [self.ONE]
        for mm in range(n):
            acc = self.ZERO
            for i in range(mm + 1):
                acc = acc.add(h[i + 1].mul(Y[mm - i]).scale(S.ka(math.comb(mm, i))))
            Y.append(acc)
        out = self.ZERO
        for j in range(n + 1):
            out = out.add(self.Fbar(j).mul(Y[n - j]).scale(S.ka(math.comb(n, j))))
        return out


def _compositions(j, k):
    """all k-tuples of nonnegative integers with sum j, in itertools.product order filtered (riglap2.Fbar's loop order)."""
    out = [()]
    for _ in range(k):
        out = [c + (x,) for c in out for x in range(j + 1)]
    return [c for c in out if sum(c) == j]


def hhat2(kern, g, avec, t, h2):
    """riglap5.hhat2: hhat >= (t/2) hbar2 on Omega with degree <= 2: the degree-2 part of hbar2 times t/2, plus for each bond the traded
    degree-3 part (1/2) K_e (a_u + a_v) (X_u - X_v)^2, K_e = (c/2) 2!/(4 (1 - max(a_u, a_v))^3)."""
    tt = S.I(t)
    NV = g.F
    out = {e: c * tt / 2 for e, c in S.spoly_iv(h2).items() if sum(e) == 2}
    a = [S.I(x) for x in avec]
    for (u, v), c in g.c.items():
        ae = a[u] if avec[u] >= avec[v] else a[v]
        K = (c / 2) * 2 / (4 * S.ipow(1 - ae, 3))
        coef = K * (a[u] + a[v]) / 2
        for (iu, pu, iv_, pv, sg) in ((u, 2, v, 0, 1), (u, 1, v, 1, -2), (u, 0, v, 2, 1)):
            e = [0] * NV
            e[iu] += pu
            e[iv_] += pv
            e = tuple(e)
            out[e] = out[e] + coef * sg if e in out else coef * sg
    assert all(sum(e) <= 2 for e in out)
    return S.spoly(kern, out, NV)
