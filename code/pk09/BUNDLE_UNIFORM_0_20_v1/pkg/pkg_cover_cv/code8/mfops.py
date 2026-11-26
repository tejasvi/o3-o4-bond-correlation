# Wave 18, matrix-free certifier: rigorous mid-rad (MR) operators for the N = 4 three-row transfer
#   S(J) = D(J) A2(W(J)) A1(W(J)) D(J),   D = diag(sqrt(W_t W_h W_bb)),   W_l = (l + 1) k_l(J),
# and its energy insertions T_X (r on the top bond: A1 with W r), T_Y (r on the bottom bond: A2 with W r), T_XY (both),
# with J-derivatives up to order 3, for J in an arb ball (a point ball at J0 or the whole interval).  Every product is
# done in MR arithmetic with explicit rounding bounds (centre + radius, as certint4's MR class), so results enclose the
# exact operator applied to every vector in the input box.  Derivatives distribute over the four factors (multinomial),
# and the A1 and A2 products are shared between all derivative orders applied to the same vector.
# v2 (certint6): optional shift kap and factor fac: the operators are then the derivatives of X(J) e^{-kap (J - J0)} times
# fac, where fac encloses c e^{-kap (J - J0)} over the ball (as certlib3.assemble_derivs with kshift, fac).  The shift is
# split over the five weight factors (kap/5 for W_a and W_b, 3 kap/10 for each D, exact in arb), so the derivative
# families cancel inside each factor.  Lazy output orders, a per-vector cache shared between kinds, float centre applies.
import math
import numpy as np
from flint import arb
import scipy.sparse as sp
import certlib3                       # bessel_derivs (N = 4 Riccati/monotone hulls), lohi

U = 2.0 ** -53
INF = 1 + 1e-12


class MR:
    __slots__ = ('c', 'r')
    def __init__(self, c, r=None):
        self.c = np.asarray(c, dtype=float)
        self.r = np.zeros_like(self.c) if r is None else np.asarray(r, dtype=float)
    def __add__(self, o):
        c = self.c + o.c
        return MR(c, (self.r + o.r) * INF + 4 * U * np.abs(c))
    def __sub__(self, o):
        c = self.c - o.c
        return MR(c, (self.r + o.r) * INF + 4 * U * np.abs(c))
    def scale(self, s):               # exact float s
        c = self.c * s
        return MR(c, self.r * abs(s) * INF + 4 * U * np.abs(c) + 1e-300)
    def absup(self):
        return (np.abs(self.c) + self.r) * INF


def iv_from_arb(lst):
    lo, hi = zip(*[certlib3.lohi(x) for x in lst])
    return np.array(lo), np.array(hi)


def mr_from_iv(lo, hi):
    c = 0.5 * (lo + hi)
    r = 0.5 * (hi - lo) * INF + 2 * U * (np.abs(lo) + np.abs(hi)) + 1e-300
    return MR(c, r)


def dmul(d, x):
    """diagonal MR d times MR x"""
    c = d.c * x.c
    return MR(c, (np.abs(d.c) * x.r + d.r * (np.abs(x.c) + x.r)) * INF + 4 * U * np.abs(c) + 1e-300)


def ascale(x, a):
    """MR x times the arb ball a"""
    lo, hi = certlib3.lohi(a)
    ac = 0.5 * (lo + hi); ar = 0.5 * (hi - lo) * INF + U * abs(ac)
    c = x.c * ac
    return MR(c, (abs(ac) * x.r + ar * (np.abs(x.c) + x.r)) * INF + 4 * U * np.abs(c) + 1e-300)


class SpMR:
    """interval sparse factor A(w) for vertical weights w in [wlo, whi] (per label), as CSR centre and radius data
    (three CSR passes per product; a fused two-column pass was slower in scipy, out/bench_fast_L25.txt)"""
    def __init__(self, F, wlo, whi):
        wc = 0.5 * (wlo + whi)
        wr = 0.5 * (whi - wlo) * INF + U * np.abs(wc)
        wabs = np.maximum(np.abs(wlo), np.abs(whi))
        dc = F.data(wc)
        dabs = F.data(wabs)                                   # coef >= 0
        rad = (F.data(wr) + (F.terms + 3) * U * dabs) * INF
        self.Mc = F.matrix(dc)
        self.Mabs = F.matrix(np.abs(dc) + rad)
        gam = (F.rowcount + 2) * U
        self.Mrg = F.matrix(rad + gam * np.abs(dc))
        self.relrad = float(np.max(rad / np.maximum(np.abs(dc) + rad, 1e-300))) if len(rad) else 0.0   # entrywise |A - Mc| <= relrad |A|_up
        self.rowcount = F.rowcount
    def mv(self, x):
        c = self.Mc @ x.c
        r = self.Mabs @ x.r + self.Mrg @ np.abs(x.c)
        return MR(c, r * INF + 1e-300)


def bessel_derivs4(Ja, nmax):
    """certlib3.bessel_derivs plus r'''' (labels 0..nmax): u'''' = -(2 nu + 1) w''' - 6 u' u'' - 2 u u''',
    w''' = (u''' - 3 w'')/J (Riccati, as certlib3), r'''' = 24 l/J^5 + u''''"""
    lo, hi = Ja.lower(), Ja.upper()
    if not (lo > 0):
        raise ValueError('J ball must be positive')
    def hull(a, b):
        l_ = a.lower() if a.lower() < b.lower() else b.lower()
        u_ = a.upper() if a.upper() > b.upper() else b.upper()
        return (l_ + u_) / 2 + (u_ - l_) / 2 * arb(0, 1)
    Il = [lo.bessel_i(n) for n in range(nmax + 3)]
    Ih = [hi.bessel_i(n) for n in range(nmax + 3)]
    x = 1 / Ja
    res = {'k': [], 'W': [], 'r': [], 'r1': [], 'r2': [], 'r3': [], 'r4': []}
    for l in range(nmax + 1):
        nu = l + 1
        k = hull(2 * Il[nu] / lo, 2 * Ih[nu] / hi)
        u = hull(Il[nu + 1] / Il[nu], Ih[nu + 1] / Ih[nu])
        w = hull(Il[nu + 1] / (Il[nu] * lo), Ih[nu + 1] / (Ih[nu] * hi))
        u1 = 1 - (2 * nu + 1) * w - u * u
        w1 = (1 - (2 * nu + 2) * w - u * u) * x
        u2 = -(2 * nu + 1) * w1 - 2 * u * u1
        w2 = (u2 - 2 * w1) * x
        u3 = -(2 * nu + 1) * w2 - 2 * u1 * u1 - 2 * u * u2
        w3 = (u3 - 3 * w2) * x
        u4 = -(2 * nu + 1) * w3 - 6 * u1 * u2 - 2 * u * u3
        res['k'].append(k); res['W'].append((l + 1) * k)
        res['r'].append(l * x + u)
        res['r1'].append(-l * x * x + u1)
        res['r2'].append(2 * l * x * x * x + u2)
        res['r3'].append(-6 * l * x * x * x * x + u3)
        res['r4'].append(24 * l * x ** 5 + u4)
    return res


def wfamilies(B, s=None, kmax=3):
    """per-label arb weight families of the factor weight W e^{-s t} (s an arb shift or None), k = 0..kmax (<= 4):
    plain W p_k(rho) and X-inserted W sum_j C(k,j) p_j(rho) r^(k-j), rho = r - s, with p_k the complete Bell
    polynomials in (rho, r', r'', r''') (Leibniz for (W e^{-s t}) r; s = 0 gives (W r)^(k))"""
    W, r, r1, r2, r3 = B['W'], B['r'], B['r1'], B['r2'], B['r3']
    r4 = B.get('r4')
    plain, ins = [], []
    for i in range(len(W)):
        rho = r[i] if s is None else r[i] - s
        p = [arb(1), rho, rho * rho + r1[i], rho ** 3 + 3 * rho * r1[i] + r2[i]]
        rd = [r[i], r1[i], r2[i], r3[i]]
        if kmax >= 4:
            p.append(rho ** 4 + 6 * rho * rho * r1[i] + 3 * r1[i] * r1[i] + 4 * rho * r2[i] + r3[i])
            rd.append(r4[i])
        plain.append([W[i] * p[k] for k in range(kmax + 1)])
        ins.append([W[i] * sum((math.comb(k, j) * p[j] * rd[k - j] for j in range(k + 1)), arb(0)) for k in range(kmax + 1)])
    return plain, ins


class OpSet:
    """MR operators for J in the arb ball Ja: factors A1^(k), A2^(j) (plain and inserted), diagonals D^(i), up to
    'order'; with kap (float) and fac (arb), the derivatives of X(J) e^{-kap (J - J0)} times fac"""
    def __init__(self, st, Ja, order, kap=0.0, fac=None, fams=('p', 'x'), mvbox=None):
        """mvbox = (J0, h, fac0) with Ja = [J0 - h, J0 + h] gives the TIGHT interval operators: the shifted factors
        W~_l = W_l e^{-kap (J - J0)/5} and D~ = D e^{-3 kap (J - J0)/10} are enclosed over I by the mean-value boxes
        W_l(J0) exp([-h, h] sup_I |r_l - kap/5|) and D(J0) exp([-h, h] sup_I |R/2 - 3 kap/10|) (log-derivatives), the
        derivative families multiply these boxes by the Bell polynomials of the shifted log-derivatives over I, and the
        constant factor is fac0 (the e^{-kap (J - J0)} is inside the factors).  Without mvbox: the plain ball
        evaluation W_l(J) over Ja, times fac."""
        self.st, self.order = st, order
        L = st['L']
        Lv = st.get("Lv", L)                  # vertical labels 0..Lv (weights of A1, A2); D uses labels 0..L
        if order > 4:
            raise ValueError("orders <= 4")
        B = bessel_derivs4(Ja, Lv) if order >= 4 else certlib3.bessel_derivs(Ja, Lv)
        self.B = B
        sW = None if kap == 0.0 else arb(kap) / 5
        t, h, bb, adm = st['t'], st['h'], st['bb'], st['adm']
        rl, rh = iv_from_arb(B['r']); r1l, r1h = iv_from_arb(B['r1']); r2l, r2h = iv_from_arb(B['r2'])
        Rlo = rl[t] + rl[h] + rl[bb]; Rhi = rh[t] + rh[h] + rh[bb]
        R1lo = r1l[t] + r1l[h] + r1l[bb]; R1hi = r1h[t] + r1h[h] + r1h[bb]
        R2lo = r2l[t] + r2l[h] + r2l[bb]; R2hi = r2h[t] + r2h[h] + r2h[bb]
        if order >= 4:
            r3l, r3h = iv_from_arb(B["r3"]); R3lo = r3l[t] + r3l[h] + r3l[bb]; R3hi = r3h[t] + r3h[h] + r3h[bb]
        if mvbox is not None:
            J0f, hh, fac = mvbox
            B0 = certlib3.bessel_derivs(arb(J0f), Lv)
            Hb = arb(0, 1) * arb(hh)
            Wt = []
            for i in range(Lv + 1):
                rho = B['r'][i] if sW is None else B['r'][i] - sW
                Wt.append(B0['W'][i] * (Hb * arb(certlib3.lohi(abs(rho))[1])).exp())
            Bw = dict(B); Bw['W'] = Wt
            # D~ box per state: D(J0) exp([-h, h] m_s), m_s >= sup_I |R/2 - 3 kap/10|
            s0l, s0h = iv_from_arb([B0['W'][i].sqrt() for i in range(L + 1)])
            P0lo = s0l[t] * s0l[h] * s0l[bb] * (1 - 8 * U); P0hi = s0h[t] * s0h[h] * s0h[bb] * (1 + 8 * U)
            slo, shi = (0.0, 0.0) if kap == 0.0 else certlib3.lohi(3 * arb(kap) / 10)
            alo = 0.5 * Rlo - shi; ahi = 0.5 * Rhi - slo
            ms = np.maximum(np.abs(alo), np.abs(ahi)) * (1 + 16 * U) + 8 * U * (np.abs(Rlo) + np.abs(Rhi) + abs(shi))
            D0lo = P0lo * np.exp(-hh * ms) * (1 - 16 * U); D0hi = P0hi * np.exp(hh * ms) * (1 + 16 * U)
        else:
            Bw = B
            swl, swh = iv_from_arb([B['W'][i].sqrt() for i in range(L + 1)])
            D0lo = swl[t] * swl[h] * swl[bb] * (1 - 8 * U); D0hi = swh[t] * swh[h] * swh[bb] * (1 + 8 * U)
        plain, ins = wfamilies(Bw, sW, max(order, 3))
        self.A1 = {}; self.A2 = {}
        for k in range(order + 1):
            if 'p' in fams:
                lo, hi = iv_from_arb([plain[i][k] for i in range(Lv + 1)])
                self.A1[('p', k)] = SpMR(st['A1'], lo, hi); self.A2[('p', k)] = SpMR(st['A2'], lo, hi)
            if 'x' in fams:
                lo, hi = iv_from_arb([ins[i][k] for i in range(Lv + 1)])
                self.A1[('x', k)] = SpMR(st['A1'], lo, hi); self.A2[('x', k)] = SpMR(st['A2'], lo, hi)
        # diagonals: D^(i) = D0 * Bell_i(a, R1/2, R2/2, R3/2), a = R/2 - 3 kap/10 (per-label arb, then per state)
        D0 = mr_from_iv(np.where(adm, D0lo, 0.0), np.where(adm, D0hi, 0.0))
        a = mr_from_iv(0.5 * Rlo, 0.5 * Rhi); a1 = mr_from_iv(0.5 * R1lo, 0.5 * R1hi); a2 = mr_from_iv(0.5 * R2lo, 0.5 * R2hi)
        a3 = mr_from_iv(0.5 * R3lo, 0.5 * R3hi) if order >= 4 else None
        # widen the R sums for their own rounding (3 additions)
        for v in ((a, a1, a2) if order < 4 else (a, a1, a2, a3)):
            v.r = v.r * INF + 8 * U * np.abs(v.c)
        if kap != 0.0:
            slo, shi = certlib3.lohi(3 * arb(kap) / 10)
            sc_, sr_ = 0.5 * (slo + shi), 0.5 * (shi - slo) * INF + U * abs(0.5 * (slo + shi))
            c = a.c - sc_
            a = MR(c, (a.r + sr_) * INF + 4 * U * np.abs(c) + 1e-300)
        aa = dmul(a, a)
        self.D = {0: D0, 1: dmul(D0, a)}
        if order >= 2:
            self.D[2] = dmul(D0, aa + a1)
        if order >= 3:
            self.D[3] = dmul(D0, dmul(aa, a) + dmul(a, a1).scale(3.0) + a2)
        if order >= 4:
            self.D[4] = dmul(D0, dmul(aa, aa) + dmul(aa, a1).scale(6.0) + dmul(a1, a1).scale(3.0) + dmul(a, a2).scale(4.0) + a3)
        self.Dl = self.D if fac is None else {i: ascale(self.D[i], fac) for i in self.D}
        self.Dc = {i: self.D[i].c for i in self.D}; self.Dlc = {i: self.Dl[i].c for i in self.Dl}
        self.r = (rl, rh); self.r1 = (r1l, r1h); self.r2 = (r2l, r2h)

    def apply(self, x, kind='S', orders=None, cache=None):
        """dict {n: X^(n) x} for n in 'orders' (default 0..order) and X in S, TX, TY, TXY; derivatives distribute over
        D A2 A1 D with multinomial coefficients; the A1 and A2 products (and, through 'cache', the A1 products of the
        same x for other kinds) are shared"""
        orders = list(range(self.order + 1)) if orders is None else list(orders)
        m = max(orders)
        f1 = 'x' if kind in ('TX', 'TXY') else 'p'
        f2 = 'x' if kind in ('TY', 'TXY') else 'p'
        if cache is None:
            cache = {}
        def Dx(l):
            if ('D', l) not in cache:
                cache[('D', l)] = dmul(self.D[l], x)
            return cache[('D', l)]
        def y(k, l):
            if ('y', f1, k, l) not in cache:
                cache[('y', f1, k, l)] = self.A1[(f1, k)].mv(Dx(l))
            return cache[('y', f1, k, l)]
        z = {}
        out = {}
        for nn in orders:
            acc = None
            for i in range(nn + 1):
                for j in range(nn + 1 - i):
                    for k in range(nn + 1 - i - j):
                        l = nn - i - j - k
                        if (j, k, l) not in z:
                            z[(j, k, l)] = self.A2[(f2, j)].mv(y(k, l))
                        coef = math.factorial(nn) // (math.factorial(i) * math.factorial(j) * math.factorial(k) * math.factorial(l))
                        term = dmul(self.Dl[i], z[(j, k, l)])
                        if coef != 1:
                            term = term.scale(float(coef))
                        acc = term if acc is None else acc + term
            out[nn] = acc
        return out

    def apply_c(self, x, kind='S', orders=(0,)):
        """float centre version of apply (no enclosure; for eigensolvers and frames)"""
        f1 = 'x' if kind in ('TX', 'TXY') else 'p'
        f2 = 'x' if kind in ('TY', 'TXY') else 'p'
        Dx = {}; y = {}; z = {}; out = {}
        for nn in orders:
            acc = 0.0
            for i in range(nn + 1):
                for j in range(nn + 1 - i):
                    for k in range(nn + 1 - i - j):
                        l = nn - i - j - k
                        if (j, k, l) not in z:
                            if (k, l) not in y:
                                if l not in Dx:
                                    Dx[l] = self.Dc[l] * x
                                y[(k, l)] = self.A1[(f1, k)].Mc @ Dx[l]
                            z[(j, k, l)] = self.A2[(f2, j)].Mc @ y[(k, l)]
                        coef = math.factorial(nn) // (math.factorial(i) * math.factorial(j) * math.factorial(k) * math.factorial(l))
                        acc = acc + coef * (self.Dlc[i] * z[(j, k, l)])
            out[nn] = acc
        return out

    def apply0(self, x, kind='S'):
        """order-0 operator (with mvbox: encloses X(J) e^{-kap (J - J0)} fac0 x for every J in I)"""
        return self.apply(x, kind, (0,))[0]
