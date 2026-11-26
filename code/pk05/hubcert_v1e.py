#!/usr/bin/env python3
# hubcert_v1e.py: certified cover of [20, J1] for the uniform P3 x P3 box, N = 3, 4, by the hub trace (route H).
# Design DESIGN_COVER_P3P3_v1.md (c7731655); lemmas LEMMA_HUB_P3P3_v1_1.md (e880fe49): Lemma H, Corollary I, Lemma N,
# Lemma K (kernel block), Lemma T (Taylor inputs), Lemma LT (label tails).  Usage: hubcert_v1e.py <item> <CAP_S> (items: smoke, pilot*, cover:N:a:b:q:k).
# Arithmetic: float64 mid-rad (MR) with explicit rounding bounds; Taylor models (TM) of degree k in t = beta - beta0,
# |t| <= h; final scalar steps in arb (python-flint).  No *_series call is used anywhere.
import sys, os, time, math, hashlib
import numpy as np
from flint import arb, ctx

ctx.prec = 128          # set after all imports (BRIEF_W18_ADD1 item 5)
ctx.cap = 64            # no *_series is used; set anyway (ADD1 item 1)

U = 2.0 ** -53          # unit roundoff
ETA = 2.0 ** -1070      # per-term underflow allowance (>= 8 x the smallest subnormal)


def gam(n):
    """gamma_n = n u / (1 - n u)"""
    return n * U / (1.0 - n * U)


def up(x):
    return np.nextafter(x, np.inf)


class MR:
    """Mid-rad float64 array: the true value lies in [m - r, m + r] entrywise (r >= 0)."""
    __slots__ = ('m', 'r')

    def __init__(self, m, r=None):
        self.m = np.asarray(m, dtype=np.float64)
        self.r = np.zeros_like(self.m) if r is None else np.asarray(r, dtype=np.float64)

    def absu(self):
        """entrywise upper bound of |value|"""
        return up(np.abs(self.m) + self.r)

    def sub(self, rows=None, cols=None):
        if cols is None:
            return MR(self.m[rows], self.r[rows])
        return MR(self.m[rows][:, cols], self.r[rows][:, cols])


def mr_add(A, B, sign=1.0):
    """A + sign*B, sign in {+1, -1} (exact scaling)."""
    m = A.m + sign * B.m
    r = up((A.r + B.r) * (1.0 + 8 * U) + 2 * U * np.abs(m))
    return MR(m, r)


def mr_scale(A, c):
    """A * c with c an MR scalar (0-d MR) or a python float (exact)."""
    if isinstance(c, MR):
        cm, cr = float(c.m), float(c.r)
    else:
        cm, cr = float(c), 0.0
    m = A.m * cm
    r = up((A.r * (abs(cm) + cr) + np.abs(A.m) * cr) * (1.0 + 16 * U) + 2 * U * np.abs(m) + ETA)
    return MR(m, r)


def mr_mul(A, B):
    """entrywise product with numpy broadcasting."""
    m = A.m * B.m
    r = up((A.r * (np.abs(B.m) + B.r) + np.abs(A.m) * B.r) * (1.0 + 16 * U) + 2 * U * np.abs(m) + ETA)
    return MR(m, r)


def mr_matmul(A, B):
    """A @ B.  |fl(Am Bm) - Am Bm| <= gamma_p |Am||Bm| (any summation order), plus the interval part
    |Am| Br + Ar (|Bm| + Br); the nonnegative radius products are inflated by (1 + 4 gamma_{p+2}) and rounded up."""
    p = A.m.shape[-1]
    g = gam(p + 2)
    m = A.m @ B.m
    R = np.abs(A.m) @ (B.r + g * np.abs(B.m)) + A.r @ (np.abs(B.m) + B.r)
    return MR(m, up(R * (1.0 + 4 * g) + p * ETA))


def mr_trace_prod(A, B):
    """Tr(A B) = sum_ij A_ij B_ji as a 0-d MR."""
    n2 = A.m.size
    g = gam(n2 + 2)
    Bt_m, Bt_r = B.m.T, B.r.T
    m = float(np.sum(A.m * Bt_m))
    R = float(np.sum(np.abs(A.m) * (Bt_r + g * np.abs(Bt_m)) + A.r * (np.abs(Bt_m) + Bt_r)))
    return MR(np.float64(m), np.float64(up(R * (1.0 + 4 * g) + n2 * ETA)))


def arb_to_mr(x):
    """0-d MR enclosing the arb ball x (lower/upper, then nextafter outward)."""
    lo = np.nextafter(float(x.lower()), -np.inf)
    hi = np.nextafter(float(x.upper()), np.inf)
    m = 0.5 * lo + 0.5 * hi
    r = up(max(hi - m, m - lo))
    return MR(np.float64(m), np.float64(r))


def arbs_to_mr(xs):
    ms, rs = [], []
    for x in xs:
        y = arb_to_mr(x)
        ms.append(float(y.m)); rs.append(float(y.r))
    return MR(np.array(ms), np.array(rs))


def mr_to_arb(m, r):
    return arb(float(m)) + arb(0, float(r)) if r > 0 else arb(float(m))


def fup_arb(x):
    """float >= every point of the arb ball x"""
    return float(np.nextafter(float(x.upper()), np.inf))


def fdn_arb(x):
    return float(np.nextafter(float(x.lower()), -np.inf))


def x_offdiag(N, m, lmax):
    """MR vector of X^{(m)}_{l,l+1}, l = m..lmax-1 (LEMMA_HUB F4):
    sqrt((l-m+1)(l+m+2 lam) / (4 (l+lam)(l+lam+1))), lam = (N-2)/2.  num and den are exact in float
    (integers or halves, small); one division and one sqrt: relative error <= 2u, enclosed with 3u."""
    lam = 0.5 * (N - 2)
    l = np.arange(m, lmax, dtype=np.float64)
    num = (l - m + 1.0) * (l + m + 2.0 * lam)
    den = 4.0 * (l + lam) * (l + lam + 1.0)
    x = np.sqrt(num / den)
    return MR(x, up(3 * U * x))


def t_coeffs(N, lmax):
    """MR vectors alpha_l = T_{l,l+1} = (l+2 lam)/(2l+2 lam), gamma_l = T_{l,l-1} = l/(2l+2 lam), l = 0..lmax
    (LEMMA_HUB F3).  One division each: relative error <= u, enclosed with 2u."""
    lam = 0.5 * (N - 2)
    l = np.arange(0, lmax + 1, dtype=np.float64)
    al = (l + 2 * lam) / (2 * l + 2 * lam)
    ga = l / (2 * l + 2 * lam)
    return MR(al, up(2 * U * al)), MR(ga, up(2 * U * ga))


def tri_rows(sub, sup, A, dshift):
    """Y = (Xtri + dshift I) A acting on the row index, where Xtri has Y_l = sub_l A_{l-1} + sup_l A_{l+1}.
    sub, sup: MR vectors of length n (sub_0 and sup_{n-1} must be 0: the operator is truncated there).
    dshift: python float (exact) or 0-d MR.  A: MR array with n rows.  Returns MR with n rows."""
    n = A.m.shape[0]
    shp = (n,) + (1,) * (A.m.ndim - 1)
    sm, sr = sub.m.reshape(shp), sub.r.reshape(shp)
    pm, pr = sup.m.reshape(shp), sup.r.reshape(shp)
    Am_dn = np.zeros_like(A.m); Ar_dn = np.zeros_like(A.r)      # A_{l-1}
    Am_dn[1:] = A.m[:-1]; Ar_dn[1:] = A.r[:-1]
    Am_up = np.zeros_like(A.m); Ar_up = np.zeros_like(A.r)      # A_{l+1}
    Am_up[:-1] = A.m[1:]; Ar_up[:-1] = A.r[1:]
    if isinstance(dshift, MR):
        dm, dr = float(dshift.m), float(dshift.r)
    else:
        dm, dr = float(dshift), 0.0
    t1, t2, t3 = sm * Am_dn, pm * Am_up, dm * A.m
    m = t1 + t2 + t3
    rad = (np.abs(sm) * Ar_dn + sr * (np.abs(Am_dn) + Ar_dn) + np.abs(pm) * Ar_up + pr * (np.abs(Am_up) + Ar_up)
           + abs(dm) * A.r + dr * (np.abs(A.m) + A.r))
    absum = np.abs(t1) + np.abs(t2) + np.abs(t3)
    return MR(m, up(rad * (1.0 + 32 * U) + 6 * U * absum + 3 * ETA))


def tri_cols(sub, sup, A, dshift):
    """Y = A (Xtri + dshift I) acting on the column index (Xtri symmetric: (A X)_{.,l} = A_{.,l-1} X_{l-1,l} +
    A_{.,l+1} X_{l+1,l}), so with sub_l = X_{l-1,l} and sup_l = X_{l,l+1} it is tri_rows on the transpose."""
    Y = tri_rows(sub, sup, MR(A.m.T, A.r.T), dshift)
    return MR(Y.m.T, Y.r.T)


class TM:
    """Taylor model of an array in t, |t| <= h: value(t) = sum_{d<=k} c[d] t^d + e(t), |e(t)| <= R entrywise
    for every |t| <= h (c[d]: MR arrays; R: nonnegative float array)."""
    __slots__ = ('c', 'R', 'h', 'k')

    def __init__(self, c, R, h, k):
        self.c, self.R, self.h, self.k = c, R, h, k

    def absP(self):
        """entrywise upper bound of |sum_d c[d] t^d| over |t| <= h"""
        acc = np.zeros_like(self.c[0].m)
        hp = 1.0
        for d in range(self.k + 1):
            acc = acc + self.c[d].absu() * hp
            hp = up(hp * self.h)
        return up(acc * (1.0 + 4 * (self.k + 2) * U))

    def sub(self, rows=None, cols=None):
        if cols is None:
            return TM([c.sub(rows) for c in self.c], self.R[rows], self.h, self.k)
        return TM([c.sub(rows, cols) for c in self.c], self.R[rows][:, cols], self.h, self.k)


def _hpow(h, d):
    v = 1.0
    for _ in range(d):
        v = up(v * h)
    return v


def tm_binop(A, B, op, absop, k, h):
    """Generic truncated TM product: op(MR, MR) -> MR (bilinear), absop(nonneg, nonneg) -> nonneg bound of
    |op(x, y)| for |x| <= a, |y| <= b.  Degrees > k go to the remainder (bounded by absop of the coefficient bounds
    times h^(a+b)); remainder: absop(|P_A|, R_B) + absop(R_A, |P_B|) + absop(R_A, R_B)."""
    c = []
    for d in range(k + 1):
        acc = None
        for a in range(d + 1):
            t = op(A.c[a], B.c[d - a])
            acc = t if acc is None else mr_add(acc, t)
        c.append(acc)
    aA = [A.c[a].absu() for a in range(k + 1)]
    aB = [B.c[b].absu() for b in range(k + 1)]
    # suffix sums of |B_b| h^b for b >= s
    suf = [None] * (k + 2)
    suf[k + 1] = np.zeros_like(aB[0])
    for b in range(k, -1, -1):
        suf[b] = up(suf[b + 1] + aB[b] * _hpow(h, b))
    trunc = None
    for a in range(1, k + 1):
        s = k + 1 - a
        t = absop(up(aA[a] * _hpow(h, a)), suf[s])
        trunc = t if trunc is None else up(trunc + t)
    pA, pB = A.absP(), B.absP()
    rem = absop(pA, B.R) + absop(A.R, pB) + absop(A.R, B.R)
    if trunc is not None:
        rem = rem + trunc
    return TM(c, up(rem * (1.0 + 16 * U)), h, k)


def _abs_matmul(a, b):
    p = a.shape[-1]
    g = gam(p + 2)
    return up((a @ b) * (1.0 + 4 * g) + p * ETA)


def _abs_mul(a, b):
    return up(a * b * (1.0 + 4 * U) + ETA)


def tm_matmul(A, B):
    return tm_binop(A, B, mr_matmul, _abs_matmul, A.k, A.h)


def tm_mul(A, B):
    """entrywise (broadcast) product, e.g. matrix times a column-scaling row vector B[None, :]."""
    return tm_binop(A, B, mr_mul, _abs_mul, A.k, A.h)


def tm_add(A, B, sign=1.0):
    return TM([mr_add(a, b, sign) for a, b in zip(A.c, B.c)], up((A.R + B.R) * (1.0 + 4 * U)), A.h, A.k)


def tm_scale(A, s):
    """multiply by an exact python float s"""
    return TM([mr_scale(a, s) for a in A.c], up(A.R * abs(s) * (1.0 + 4 * U)), A.h, A.k)


def tm_rowvec(v):
    """view a vector TM (length n) as a row (1, n) for column scaling."""
    return TM([MR(c.m[None, :], c.r[None, :]) for c in v.c], v.R[None, :], v.h, v.k)


def tm_trace(A, B):
    """scalar TM (0-d arrays) of Tr(A B)."""
    def op(x, y):
        return mr_trace_prod(x, y)

    def absop(a, b):
        n2 = a.size
        g = gam(n2 + 2)
        return np.float64(up(float(np.sum(a * b.T)) * (1.0 + 4 * g) + n2 * ETA))
    return tm_binop(A, B, op, absop, A.k, A.h)


def lam_of(N):
    return arb(N - 2) / 2


def bessel_ratios(N, beta, lmax):
    """arb list a_l(beta)/a_0(beta) = I_{l+lam}(beta)/I_lam(beta), l = 0..lmax (LEMMA_HUB F2)."""
    lam = lam_of(N)
    b = arb(beta) if not isinstance(beta, arb) else beta
    I0 = b.bessel_i(lam)
    return [b.bessel_i(lam + l) / I0 for l in range(lmax + 1)]


def taylor_tail_const(h, Kb):
    """(2h)^(Kb+1) e^(2h) / (Kb+1)!  (Lemma T), as a float rounded up."""
    H = arb(h)
    v = (2 * H) ** (Kb + 1) * (2 * H).exp() / arb(Kb + 2).gamma()
    return fup_arb(v)


def choose_Kb(h, k):
    Kb = k + 4
    while taylor_tail_const(h, Kb) > 1e-25:
        Kb += 1
    return Kb


def series_tail(beta0, n1):
    """e^-b b^(n1+1) / ((n1+1)! (1 - b/(n1+2)))  (Lemma K (ii)), arb ball; needs n1 + 2 > b."""
    b = arb(beta0)
    return (-b).exp() * b ** (n1 + 1) / (arb(n1 + 2).gamma() * (1 - b / (n1 + 2)))


def choose_n1(beta0, tol=1e-25):
    n1 = int(math.ceil(beta0)) + 1
    while True:
        if n1 + 2 > beta0:
            lt = -beta0 + (n1 + 1) * math.log(beta0) - math.lgamma(n1 + 2) - math.log(1 - beta0 / (n1 + 2))
            if lt < math.log(tol) - 2.0 and fup_arb(series_tail(beta0, n1)) <= tol:
                return n1
        n1 += 1


def corner_tm(N, beta0, h, k, Kb, L):
    """TM of a~(beta0 + t) = e^-t a(beta0 + t)/a_0(beta0) on labels 0..L+2 (Lemma T (T1)).
    Coefficients v_j = (T - 1)^j a~(beta0)/j!, exact from the arb ratios on 0..L+2+Kb; degrees k < j <= Kb go to
    the remainder at their computed size; beyond Kb the proven bound (2h)^(Kb+1) e^(2h)/(Kb+1)! (a~_0(beta0) = 1)."""
    La = L + 2 + Kb
    v = arbs_to_mr(bessel_ratios(N, beta0, La))
    al, ga = t_coeffs(N, La)
    sub = MR(ga.m.copy(), ga.r.copy())
    sup = MR(al.m.copy(), al.r.copy())
    coefs = [v.sub(slice(0, L + 3))]
    rem = np.zeros(L + 3)
    cur = v
    for j in range(1, Kb + 1):
        n = cur.m.shape[0]
        sub_j = MR(sub.m[:n].copy(), sub.r[:n].copy())
        sup_j = MR(sup.m[:n].copy(), sup.r[:n].copy())
        sup_j.m[n - 1] = 0.0; sup_j.r[n - 1] = 0.0
        nxt = tri_rows(sub_j, sup_j, cur, -1.0)
        nxt = mr_scale(nxt, arb_to_mr(arb(1) / j))
        cur = nxt.sub(slice(0, n - 1))           # the last entry used a truncated neighbour: drop it
        part = cur.sub(slice(0, L + 3))
        if j <= k:
            coefs.append(part)
        else:
            rem = up(rem + part.absu() * _hpow(h, j))
    rem = up(rem * (1.0 + 4 * (Kb + 2) * U) + taylor_tail_const(h, Kb))
    return TM(coefs, rem, h, k)


def kernel_tm(N, m, beta0, h, k, Kb, L, n1, emb, tail_f):
    """Sector m: TM of E~(beta0 + t) = e^-(beta0+t) exp((beta0+t) X^{(m)}) on rows m..L+2, cols m..L.
    (1) Lemma K: E~(beta0) on rows m..L+2 x cols m..Lc (Lc = L+Kb+1) from e^-b0 sum_{j<=n1} b0^j X^j/j! computed on
        levels m..Lmax, Lmax = L+Kb+2+ceil(n1/2) >= Lc + n1/2: exact block up to the series tail tail_f.
        All terms are >= 0, so the plain float recursion M_j = fl(fl(b0/j) fl(sub M_{j-1}^dn + sup M_{j-1}^up))
        has relative error <= (1+u)^8 per step (5 roundings + the 3u error of each X entry), and the sum adds
        (1+u)^n1: |fl(S) - S| <= gamma_{9 n1 + 4} fl(S) / (1 - gamma) entrywise; the relative error of e^-b0 is added.
        Underflow (at most about 10 n1 x 2^-1074 per entry, since every entry is a sum of nonnegative terms) is
        absorbed by the per-entry tail_f added to the radius, which is far larger (printed as sertail; the review n2).
    (2) Lemma T (T2): C_j = E~(beta0)(X - 1)^j / j! by MR column steps; degrees k < j <= Kb to the remainder,
        plus the proven bound (2h)^(Kb+1) e^(2h)/(Kb+1)! per entry."""
    Lc = L + Kb + 1
    Lmax = L + Kb + 2 + (n1 + 1) // 2
    nr, nc = Lmax - m + 1, Lc - m + 1
    x = x_offdiag(N, m, Lmax)
    xs = x.m                                              # X_{l,l+1}, l = m..Lmax-1
    Mt = np.zeros((nr, nc))
    Mt[np.arange(nc), np.arange(nc)] = float(emb.m)
    S = Mt.copy()
    sub = xs[:, None]                                     # row i+1 gets X_{i,i+1} M_i ; row i gets X_{i,i+1} M_{i+1}
    for j in range(1, n1 + 1):
        nxt = np.zeros_like(Mt)
        nxt[1:] = sub * Mt[:-1]
        nxt[:-1] += sub * Mt[1:]
        Mt = nxt * (beta0 / j)
        S += Mt
    rel = gam(9 * n1 + 8) + float(emb.r) / float(emb.m) * (1.0 + 1e-6)
    S = S[:L + 3 - m]                                     # rows m..L+2
    E0 = MR(S, up(S * rel * (1.0 + 4 * U) + tail_f))
    # (2) Taylor coefficients by column steps with (X - 1)
    xc = MR(x.m[:nc].copy(), x.r[:nc].copy())             # X_{l,l+1}, l = m..m+nc-1
    coefs = [E0.sub(slice(None), slice(0, L + 1 - m))]
    rem = np.zeros((L + 3 - m, L + 1 - m))
    cur = E0
    for j in range(1, Kb + 1):
        n = cur.m.shape[1]
        subc = MR(np.concatenate(([0.0], xc.m[:n - 1])), np.concatenate(([0.0], xc.r[:n - 1])))
        supc = MR(np.concatenate((xc.m[:n - 1], [0.0])), np.concatenate((xc.r[:n - 1], [0.0])))
        nxt = tri_cols(subc, supc, cur, -1.0)
        nxt = mr_scale(nxt, arb_to_mr(arb(1) / j))
        cur = nxt.sub(slice(None), slice(0, n - 1))       # the last column used a truncated neighbour: drop it
        part = cur.sub(slice(None), slice(0, L + 1 - m))
        if j <= k:
            coefs.append(part)
        else:
            rem = up(rem + part.absu() * _hpow(h, j))
    rem = up(rem * (1.0 + 4 * (Kb + 2) * U) + taylor_tail_const(h, Kb))
    return TM(coefs, rem, h, k)


def label_tail(N, beta0, h, L):
    """Lemma LT with the majorants of LEMMA_HUB v1_1 §7 (pk09's S18REV01 r1).  Raw diagonals a~(T^p a~), p = 0,1,2,
    and (Ta~)(Ta~): delta(l) <= A^2 (a_l/a_0)(a_{l-p}/a_0) or A^2 (a_{l-1}/a_0)^2 at b0+h, A = sup a~_0 = e^h a_0(b0-h)/a_0(b0).
    S_p <= d_{L+1}(a_{L+1}/a_0)(a_{L+1-p}/a_0)/(1 - (d_{L+2}/d_{L+1}) q_L q_{L-p}); S_11 <= d_{L+1}(a_L/a_0)^2/(1 - (d_{L+2}/d_{L+1}) q_{L-1}^2),
    q_j = b/(j+lam+1/2+sqrt((j+lam+1/2)^2+b^2)) from (B-up).  Every denominator must be > 0.
    Returns (4 A^8 S_max, A) as floats rounded up, or (inf, A)."""
    lam = lam_of(N)
    b0, bl, bh = arb(beta0), arb(beta0) - arb(h), arb(beta0) + arb(h)
    A = arb(h).exp() * (b0 / bl) ** lam * bl.bessel_i(lam) / b0.bessel_i(lam)
    I0 = bh.bessel_i(lam)

    def rat(l):
        return bh.bessel_i(lam + l) / I0

    def q(j):
        nu = lam + j + arb(1) / 2
        return bh / (nu + (nu * nu + bh * bh).sqrt())
    d = (lambda l: arb(2 * l + 1)) if N == 3 else (lambda l: arb((l + 1) ** 2))
    dr = d(L + 2) / d(L + 1)
    sums = []
    for p in (0, 1, 2):
        den = 1 - dr * q(L) * q(L - p)
        if not (den.lower() > 0):
            return float('inf'), fup_arb(A)
        sums.append(fup_arb(d(L + 1) * rat(L + 1) * rat(L + 1 - p) / den))
    den = 1 - dr * q(L - 1) * q(L - 1)
    if not (den.lower() > 0):
        return float('inf'), fup_arb(A)
    sums.append(fup_arb(d(L + 1) * rat(L) * rat(L) / den))
    return fup_arb(4 * A ** 8 * arb(max(sums))), fup_arb(A)


def tm_lin_rows(sub, sup, A, dshift):
    """TM of (Xtri + dshift) A on the row index (exact up to the dropped last row).  Remainder |Xtri + dshift| R."""
    c = [tri_rows(sub, sup, x, dshift) for x in A.c]
    n = A.R.shape[0]
    shp = (n,) + (1,) * (A.R.ndim - 1)
    Rdn = np.zeros_like(A.R); Rdn[1:] = A.R[:-1]
    Rup = np.zeros_like(A.R); Rup[:-1] = A.R[1:]
    dabs = abs(float(dshift.m)) + float(dshift.r) if isinstance(dshift, MR) else abs(float(dshift))
    R = up((sub.absu().reshape(shp) * Rdn + sup.absu().reshape(shp) * Rup + dabs * A.R) * (1.0 + 8 * U))
    out = TM(c, R, A.h, A.k)
    return out.sub(slice(0, n - 1))


def float_prepass(N, L, avec, Ems, rho_x):
    """float estimates of E[r] and E[x] at t = 0 (centring constants; any value is valid, Lemma N)."""
    lam = 0.5 * (N - 2)
    l = np.arange(0, L + 2, dtype=np.float64)
    al = (l + 2 * lam) / (2 * l + 2 * lam); ga = l / (2 * l + 2 * lam)
    a = avec[:L + 3]
    Ta = ga[:L + 1] * np.concatenate(([0.0], a[:L])) + al[:L + 1] * a[1:L + 2]
    Kv, KRv = a[:L + 1] ** 2, a[:L + 1] * Ta
    Z = Zc = Zs = 0.0
    for m, (E, xs) in enumerate(Ems):
        Dm = (1 if m == 0 else 2) if N == 3 else 2 * m + 1
        n = L + 1 - m
        Esq = E[:n, :n]
        XE = np.zeros((n, n))
        XE[1:] += xs[:n - 1, None] * E[:n - 1, :n]
        XE += xs[:n, None] * E[1:n + 1, :n]
        V = Esq * Kv[m:][None, :]
        V2 = V @ V
        Z += Dm * np.sum(V2 * V2.T)
        Zc += Dm * np.sum(((Esq * KRv[m:][None, :]) @ V) * V2.T)
        Zs += Dm * np.sum(((XE * Kv[m:][None, :]) @ V) * V2.T)
    return Zc / Z, Zs / Z


# traces: name -> (number of first-order corner insertions, of spoke insertions) for the tail weights
TRACES = {'Z': (0, 0), 'Zc': (1, 0), 'Zs': (0, 1), 'CCadj': (2, 0), 'CCopp': (2, 0), 'CSadj': (1, 1),
          'CSfar': (1, 1), 'CSfar2': (1, 1), 'CSadj2': (1, 1), 'Varb': (2, 0), 'Same': (2, 0), 'Vars': (0, 2),
          'SSadj': (0, 2), 'SSopp': (0, 2)}


def run_interval(N, beta0, h, k, L=None, n1=None, ctl=False, log=None):
    """All scalar TMs (sector-summed, label tails added) for one interval; returns dict name -> TM and info."""
    t0 = time.time()
    if L is None:
        L = int(math.ceil(math.sqrt(40.0 * (beta0 + h)))) + 2
    Kb = choose_Kb(h, k)
    if n1 is None:
        n1 = choose_n1(beta0)
    ser_tail = series_tail(beta0, n1)
    tail_f = fup_arb(ser_tail)
    emb = arb_to_mr((-arb(beta0)).exp())
    atm = corner_tm(N, beta0, h, k, Kb, L)                  # labels 0..L+2
    t_in = time.time()
    # pass 1: kernel Taylor models per sector, and float data for the centring constants
    ktms, Ems = [], []
    for m in range(L + 1):
        E = kernel_tm(N, m, beta0, h, k, Kb, L, n1, emb, tail_f)
        ktms.append(E)
        xs = x_offdiag(N, m, L + 3).m
        Ems.append((E.c[0].m, xs))
    t_k = time.time()
    rho, xi = float_prepass(N, L, atm.c[0].m, Ems, None)
    rho_mr, xi_mr = MR(np.float64(rho)), MR(np.float64(xi))
    # corner vectors (labels 0..L): K = a*a, C = a*(T-rho)a, C2 = a*(T-rho)^2 a, C11 = ((T-rho)a)^2
    al, ga = t_coeffs(N, L + 2)
    def tlin(v):
        n = v.R.shape[0]
        sub = MR(ga.m[:n].copy(), ga.r[:n].copy()); sup = MR(al.m[:n].copy(), al.r[:n].copy())
        sup.m[n - 1] = 0.0; sup.r[n - 1] = 0.0
        return tm_lin_rows(sub, sup, v, MR(np.float64(-rho)))
    a1 = tlin(atm)                                          # (T - rho) a on 0..L+1
    a2 = tlin(a1)                                           # (T - rho)^2 a on 0..L
    aL = atm.sub(slice(0, L + 1))
    Kv = tm_mul(aL, aL)
    Cv = tm_mul(aL, a1.sub(slice(0, L + 1)))
    C2v = tm_mul(aL, a2) if ctl else None
    C11v = tm_mul(a1.sub(slice(0, L + 1)), a1.sub(slice(0, L + 1))) if ctl else None
    acc = {}
    for m in range(L + 1):
        Dm = (1 if m == 0 else 2) if N == 3 else 2 * m + 1
        E = ktms[m]                                         # rows m..L+2, cols m..L
        n = L + 1 - m
        x = x_offdiag(N, m, L + 3)                          # X_{l,l+1}, l = m..L+2
        nr = E.R.shape[0]
        sub = MR(np.concatenate(([0.0], x.m[:nr - 1])), np.concatenate(([0.0], x.r[:nr - 1])))
        sup = MR(np.concatenate((x.m[:nr - 1], [0.0])), np.concatenate((x.r[:nr - 1], [0.0])))
        S1 = tm_lin_rows(sub, sup, E, MR(np.float64(-xi)))  # rows m..L+1
        Es = E.sub(slice(0, n))
        S1s = S1.sub(slice(0, n))
        kv, cv = tm_rowvec(Kv.sub(slice(m, L + 1))), tm_rowvec(Cv.sub(slice(m, L + 1)))
        V, Vc, Vs, Vsc = tm_mul(Es, kv), tm_mul(Es, cv), tm_mul(S1s, kv), tm_mul(S1s, cv)
        P2 = tm_matmul(V, V); P3 = tm_matmul(V, P2)
        Qc = tm_matmul(Vc, V); Qs = tm_matmul(Vs, V); Qcc = tm_matmul(Vc, Vc)
        tr = {'Z': tm_trace(P2, P2), 'Zc': tm_trace(Qc, P2), 'Zs': tm_trace(Qs, P2), 'CCadj': tm_trace(Qcc, P2),
              'CCopp': tm_trace(Qc, Qc), 'CSfar': tm_trace(Qc, Qs), 'CSadj': tm_trace(Vsc, P3)}
        if ctl:
            sub2 = MR(sub.m[:nr - 1].copy(), sub.r[:nr - 1].copy()); sup2 = MR(sup.m[:nr - 1].copy(), sup.r[:nr - 1].copy())
            sup2.m[nr - 2] = 0.0; sup2.r[nr - 2] = 0.0
            S2s = tm_lin_rows(sub2, sup2, S1, MR(np.float64(-xi))).sub(slice(0, n))
            c2v, c11v = tm_rowvec(C2v.sub(slice(m, L + 1))), tm_rowvec(C11v.sub(slice(m, L + 1)))
            tr['Varb'] = tm_trace(tm_mul(Es, c2v), P3)
            tr['Same'] = tm_trace(tm_mul(Es, c11v), P3)
            tr['Vars'] = tm_trace(tm_mul(S2s, kv), P3)
            tr['SSadj'] = tm_trace(tm_matmul(Vs, Vs), P2)
            tr['SSopp'] = tm_trace(Qs, Qs)
            tr['CSfar2'] = tm_trace(Qc, tm_matmul(V, Vs))
            tr['CSadj2'] = tm_trace(tm_matmul(Vc, Vs), P2)
        for nm, val in tr.items():
            sc = tm_scale(val, float(Dm))
            acc[nm] = sc if nm not in acc else tm_add(acc[nm], sc)
    t_p = time.time()
    tail1, Abound = label_tail(N, beta0, h, L)
    for nm in acc:
        ac, sp = TRACES[nm]
        w = up(tail1 * (1.0 + abs(rho)) ** ac * (1.0 + abs(xi)) ** sp * (1.0 + 16 * U))
        acc[nm] = TM(acc[nm].c, up(acc[nm].R + w), h, k)
    info = dict(N=N, beta0=beta0, h=h, k=k, L=L, Kb=Kb, n1=n1, Lmax=L + Kb + 2 + (n1 + 1) // 2, rho=rho, xi=xi,
                ser_tail=tail_f, lab_tail=tail1, A=Abound, t_in=t_in - t0, t_k=t_k - t_in, t_p=t_p - t_k,
                t_tot=time.time() - t0)
    return acc, info


DELTA2 = {'CCadj': arb(1) / 36, 'CCopp': arb(1) / 144, 'CSadj': arb(25) / 144, 'CSfar': arb(1) / 144}
PAIRS = {'CCadj': ('Zc', 'Zc'), 'CCopp': ('Zc', 'Zc'), 'CSadj': ('Zc', 'Zs'), 'CSfar': ('Zc', 'Zs'),
         'CSfar2': ('Zc', 'Zs'), 'CSadj2': ('Zc', 'Zs'), 'Varb': ('Zc', 'Zc'), 'Same': ('Zc', 'Zc'),
         'Vars': ('Zs', 'Zs'), 'SSadj': ('Zs', 'Zs'), 'SSopp': ('Zs', 'Zs')}


def tm_arb(T, with_rem=True):
    cs = [mr_to_arb(c.m, c.r) for c in T.c]
    rem = arb(0, float(T.R)) if (with_rem and float(T.R) > 0) else arb(0)
    return cs, rem


def ev(cs, rem, t):
    v = arb(0)
    for c in reversed(cs):
        v = v * t + c
    return v + rem


def subballs(h, nsub):
    H = arb(h)
    return [(-H + 2 * H * i / nsub).union(-H + 2 * H * (i + 1) / nsub) for i in range(nsub)]


def decide(acc, tau, h, nsub=16, shift=None):
    """N_tau = Z_tau Z - Z_e Z_f > 0 on |t| <= h (16 subintervals, arb).  shift: P1's delta (certify N - delta Z^2).
    lowD (v1c): min over subintervals of N_lo,i / Z_hi,i^2, a lower bound of D_tau on the interval when ok."""
    e, f = PAIRS[tau]
    T, Z, Ze, Zf = (tm_arb(acc[x]) for x in (tau, 'Z', e, f))
    ok, lowD = True, None
    for tb in subballs(h, nsub):
        zt, zz, ze, zf = (ev(c, r, tb) for (c, r) in (T, Z, Ze, Zf))
        n = zt * zz - ze * zf
        if shift is not None:
            n = n - shift * zz * zz
        if not (n.lower() > 0) or not (zz.lower() > 0):
            ok = False
        else:
            ld = (n.lower() / (zz.upper() * zz.upper())).lower()
            lowD = ld if lowD is None else (ld if ld < lowD else lowD)
    return ok, (lowD if ok else None)


def point_D(acc, tau, t=0.0, with_rem=True):
    e, f = PAIRS[tau]
    tb = arb(t)
    zt, zz, ze, zf = (ev(*tm_arb(acc[x], with_rem), tb) for x in (tau, 'Z', e, f))
    return zt / zz - ze * zf / (zz * zz)


def coef(acc, name, d):
    return mr_to_arb(acc[name].c[d].m, acc[name].c[d].r)


def sum_rule(acc, which, swap=False):
    """C1 on the truncated system (exact identity there; no label tail): d/dbeta E[s_e] = sum_f D_ef at t = 0."""
    Z0, Z1 = coef(acc, 'Z', 0), coef(acc, 'Z', 1)
    def D(tau):
        e, f = PAIRS[tau]
        return coef(acc, tau, 0) / Z0 - coef(acc, e, 0) * coef(acc, f, 0) / (Z0 * Z0)
    far = 'CSadj' if swap else 'CSfar'
    if which == 'rim':
        lhs = (coef(acc, 'Zc', 1) * Z0 - coef(acc, 'Zc', 0) * Z1) / (Z0 * Z0)
        rhs = D('Varb') + D('Same') + 4 * D('CCadj') + 2 * D('CCopp') + 2 * D('CSadj') + 2 * D(far)
    else:
        lhs = (coef(acc, 'Zs', 1) * Z0 - coef(acc, 'Zs', 0) * Z1) / (Z0 * Z0)
        rhs = D('Vars') + 2 * D('SSadj') + D('SSopp') + 4 * D('CSadj') + 4 * D(far)
    diff = lhs - rhs
    return diff.contains(0), lhs, rhs, diff


def fmt(x, nd=10):
    return x.str(nd, radius=True) if isinstance(x, arb) else str(x)


TYPES = ('CSfar', 'CCopp', 'CCadj', 'CSadj')


def report_interval(acc, info, h, out):
    """one IV line; returns dict tau -> (ok, lowD)."""
    N, b0 = info['N'], info['beta0']
    res = {}
    parts = []
    for tau in TYPES:
        ok, lowD = decide(acc, tau, h)
        D0 = point_D(acc, tau)
        lead = arb(N - 1) * DELTA2[tau] / (8 * arb(b0) ** 2)
        res[tau] = (ok, lowD)
        parts.append('%s %s lowD %s D0 %s ratio %s' % (tau, 'CERT' if ok else 'FAIL',
                     fmt(lowD, 6) if lowD is not None else '-', fmt(D0, 12), fmt(D0 / lead, 8)))
    remZ = float(acc['Z'].R) / abs(float(acc['Z'].c[0].m))
    out('IV N=%d b0=%r h=%r k=%d L=%d Kb=%d n1=%d Lmax=%d rho=%.12g xi=%.12g sertail=%.3e labtail=%.3e A=%.6g '
        'remZrel=%.3e t_in=%.2f t_k=%.2f t_p=%.2f t=%.2f' % (N, b0, h, info['k'], info['L'], info['Kb'], info['n1'],
        info['Lmax'], info['rho'], info['xi'], info['ser_tail'], info['lab_tail'], info['A'], remZ, info['t_in'],
        info['t_k'], info['t_p'], info['t_tot']))
    for p in parts:
        out('   ' + p)
    return res


def controls_C1C2(acc, out, tag):
    good = True
    for which in ('rim', 'spoke'):
        ok, lhs, rhs, diff = sum_rule(acc, which)
        out('C1 %s %s: dE/dbeta %s  sum_f D %s  diff %s -> %s' % (tag, which, fmt(lhs, 14), fmt(rhs, 14),
            fmt(diff, 4), 'PASS' if ok else 'FAIL'))
        good = good and ok
    for a, b in (('CSfar', 'CSfar2'), ('CSadj', 'CSadj2')):
        ov = all(coef(acc, a, d).overlaps(coef(acc, b, d)) for d in range(acc[a].k + 1))
        out('C2 %s %s vs %s: all %d coefficients overlap -> %s' % (tag, a, b, acc[a].k + 1, 'PASS' if ov else 'FAIL'))
        good = good and ov
    return good


def plants_on(acc, info, out):
    """P1 (shifted target) and P5 (type swap in C1) on an existing interval; returns True if both fire."""
    h = info['h']
    D0 = point_D(acc, 'CSfar')
    delta = arb(fup_arb(D0)) * 3 / 2
    ok, _ = decide(acc, 'CSfar', h, shift=delta)
    out('P1 shifted target (delta = 1.5 x upper D0 = %s): certified=%s -> %s' % (fmt(delta, 8), ok,
        'FIRED' if not ok else 'DID NOT FIRE'))
    ok5, _, _, diff = sum_rule(acc, 'rim', swap=True)
    out('P5 type swap in C1 (CSadj for CSfar): identity holds=%s diff %s -> %s' % (ok5, fmt(diff, 4),
        'FIRED' if not ok5 else 'DID NOT FIRE'))
    return (not ok) and (not ok5)


def plant_P6(out):
    x = arb(0, 1e-30)
    fired = (not (x > 0)) and (not (x < 0)) and x.contains(0)
    out('P6 flint: zero-centred ball (x > 0)=%s (x < 0)=%s contains(0)=%s; ctx.prec=%d -> %s' % (
        x > 0, x < 0, x.contains(0), ctx.prec, 'FIRED' if fired else 'DID NOT FIRE'))
    return fired


def uncert_plant(N, b0, h, k, out, name, **kw):
    acc, info = run_interval(N, b0, h, k, **kw)
    ok, _ = decide(acc, 'CSfar', h)
    out('%s (%s): CSfar certified=%s sertail=%.3e labtail=%.3e remZrel=%.3e -> %s' % (name, kw if kw else 'k=%d' % k,
        ok, info['ser_tail'], info['lab_tail'], float(acc['Z'].R) / abs(float(acc['Z'].c[0].m)),
        'FIRED' if not ok else 'DID NOT FIRE'))
    return not ok


def make_interval(ell, qq):
    """floats (b0, h) with b0 = ell/(1-qq) and h >= b0 - ell in exact arithmetic, so [b0-h, b0+h] contains ell."""
    b0 = ell / (1.0 - qq)
    h = b0 - ell
    while not (arb(b0) - arb(h) <= arb(ell)):
        h = float(np.nextafter(h, np.inf))
    return b0, h


def cover_item(N, a, b, q, k, cap, T0, out):
    """v1c production item: consecutive intervals from a until b is covered.  Each interval must certify all four
    types; on a failure the same left end is retried with q/2, then q/4.  v1d: the first certified interval
    also runs P1, P5 (plants_on) and P2, P3, P4 at the item's own N and beta0 (the condition);
    v1e: P4 (k = 1) runs on 10x the production half-width, where Z itself varies by a factor of several, so a
    degree-1 model is expected to fail at every N and beta0 (v1d's P4 at q = 0.01 still certified at N=3, beta0 = 20.2).  Ledger lines carry the exact endpoints
    (b0, h as float.hex) so the union can be rechecked independently.  Returns (all_ok, controls_ok, plants_ok)."""
    ell, last, nint, ctl_ok, plants_ok = a, 0.0, 0, True, True
    first_lo, hi = None, None
    while True:
        if time.time() - T0 + 2.0 * last > 0.8 * cap:
            out('COVER_STOP N=%d next_left=%r (time) intervals=%d' % (N, ell, nint))
            return False, ctl_ok, plants_ok
        t1 = time.time()
        done = False
        for qq in (q, q / 2, q / 4):
            b0, h = make_interval(ell, qq)
            ctl = (nint == 0)
            acc, info = run_interval(N, b0, h, k, ctl=ctl)
            res = report_interval(acc, info, h, out)
            if ctl:
                ctl_ok = controls_C1C2(acc, out, 'N=%d b0=%r' % (N, b0)) and ctl_ok
                if all(res[t][0] for t in TYPES):
                    pl = plants_on(acc, info, out)
                    pl = uncert_plant(N, b0, h, k, out, 'P2 series cut', n1=int(math.ceil(b0))) and pl
                    pl = uncert_plant(N, b0, h, k, out, 'P3 label cut', L=info['L'] // 2) and pl
                    pl = uncert_plant(N, b0, 10.0 * h, 1, out, 'P4 degree cut k=1 on 10h') and pl
                    plants_ok = plants_ok and pl
            if all(res[t][0] for t in TYPES):
                lo, hi = arb(b0) - arb(h), arb(b0) + arb(h)
                out('LEDGER N=%d lo=%s hi=%s b0hex=%s hhex=%s q=%r lowD_CSfar=%s' % (N, lo.str(25, radius=False),
                    hi.str(25, radius=False), b0.hex(), h.hex(), qq, fmt(res['CSfar'][1], 6)))
                first_lo = lo if first_lo is None else first_lo
                done = True
                break
            out('RETRY N=%d left=%r q=%r failed' % (N, ell, qq))
        if not done:
            out('COVER_FAIL N=%d left=%r (q/4 failed)' % (N, ell))
            return False, ctl_ok, plants_ok
        nint += 1
        last = time.time() - t1
        if not (hi < arb(b)):
            out('COVER_DONE N=%d intervals=%d first_lo=%s last_hi=%s target_b=%r' % (N, nint, first_lo.str(25, radius=False),
                hi.str(25, radius=False), b))
            return True, ctl_ok, plants_ok
        ell = float(np.nextafter(float(hi.lower()), -np.inf))


PONE4 = {19.811: {'CCopp': 6.887775e-06, 'CSfar': 7.790747e-06, 'CCadj': 2.743242e-05, 'CSadj': 1.700434e-04},
         28.1503: {'CCopp': 3.372639e-06, 'CSfar': 3.681412e-06, 'CCadj': 1.345190e-05, 'CSadj': 8.359199e-05},
         40.0: {'CCopp': 1.657315e-06, 'CSfar': 1.763492e-06, 'CCadj': 6.616400e-06, 'CSadj': 4.118653e-05}}

# named items: list of (N, beta0, q, k, ctl); pone points are added for N = 4 in the 'a' items
ITEMS = {
    'smoke': [(4, 20.2, 0.01, 6, True), (3, 20.2, 0.01, 6, False)],
    'pilot4a': [(4, 20.2, 0.01, 8, True), (4, 40.4, 0.01, 8, True)],
    'pilot4b': [(4, 80.8, 0.01, 8, True)],
    'pilot4c': [(4, 151.5, 0.01, 8, True)],
    'pilot3a': [(3, 20.2, 0.01, 8, True), (3, 40.4, 0.01, 8, True)],
    'pilot3b': [(3, 80.8, 0.01, 8, True)],
    'pilot3c': [(3, 151.5, 0.01, 8, True)],
}


def main():
    item, cap = sys.argv[1], float(sys.argv[2])
    T0 = time.time()
    with open(os.path.abspath(__file__), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    lines = []

    def out(s):
        print(s, flush=True)
        lines.append(s)
    out('hubcert_v1e sha256 %s item %s cap_s %g' % (sha, item, cap))
    out('python %s numpy %s ctx.prec %d ctx.cap %d utc_start %s' % (sys.version.split()[0], np.__version__, ctx.prec,
        ctx.cap, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
    allok, ctl_ok, plants_ok = True, True, True
    p6 = plant_P6(out)
    plants_ok = plants_ok and p6
    if item in ITEMS:
        last = 0.0
        for (N, b0, q, k, ctl) in ITEMS[item]:
            if time.time() - T0 + 2.0 * last > 0.8 * cap:
                out('STOPPED before N=%d b0=%r (time)' % (N, b0)); allok = False; break
            t1 = time.time()
            h = q * b0
            acc, info = run_interval(N, b0, h, k, ctl=ctl)
            res = report_interval(acc, info, h, out)
            allok = allok and res['CSfar'][0]
            if ctl:
                ctl_ok = controls_C1C2(acc, out, 'N=%d b0=%r' % (N, b0)) and ctl_ok
                if b0 == 40.4 or item == 'smoke':
                    plants_ok = plants_on(acc, info, out) and plants_ok
            last = time.time() - t1
        if item == 'pilot4a':
            for J, ref in sorted(PONE4.items()):
                acc, info = run_interval(4, J, 0.01 * J, 8)
                for tau in TYPES:
                    D0 = point_D(acc, tau)
                    rel = abs(D0 / ref[tau] - 1)
                    ok = rel.upper() < 1e-3
                    out('C3 pone N=4 J=%r %s: D %s pone %.6e rel %s -> %s' % (J, tau, fmt(D0, 12), ref[tau],
                        fmt(rel, 3), 'PASS' if ok else 'FAIL'))
                    ctl_ok = ctl_ok and ok
        if item in ('pilot4b', 'pilot3b'):
            N = 4 if item == 'pilot4b' else 3
            b0 = 80.8; h = 0.01 * b0
            base, bi = run_interval(N, b0, h, 8)
            for kw, name in ((dict(L=bi['L'] + 8), 'L+8'), (dict(k=10), 'k+2')):
                k2 = kw.pop('k', 8)
                acc, info = run_interval(N, b0, h, k2, **kw)
                for tau in TYPES:
                    a, b = point_D(base, tau), point_D(acc, tau)
                    ov = a.overlaps(b) and (b.rad() <= 2 * a.rad() + arb(1e-300))
                    out('C4 N=%d b0=%r %s %s: base %s new %s -> %s' % (N, b0, name, tau, fmt(a, 12), fmt(b, 12),
                        'PASS' if ov else 'FAIL'))
                    ctl_ok = ctl_ok and ov
        if item == 'pilot4a':
            b0 = 40.4; h = 0.01 * b0
            Ld = int(math.ceil(math.sqrt(40.0 * (b0 + h)))) + 2
            plants_ok = uncert_plant(4, b0, h, 8, out, 'P2 series cut', n1=int(math.ceil(b0))) and plants_ok
            plants_ok = uncert_plant(4, b0, h, 8, out, 'P3 label cut', L=Ld // 2) and plants_ok
            plants_ok = uncert_plant(4, b0, h, 1, out, 'P4 degree cut k=1') and plants_ok
    elif item.startswith('cover:'):
        parts = item.split(':')
        if len(parts) == 6:
            N, a, b, q, k = int(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), int(parts[5])
            ok, c_ok, p_ok = cover_item(N, a, b, q, k, cap, T0, out)
            plants_ok = plants_ok and p_ok
            allok = allok and ok
            ctl_ok = ctl_ok and c_ok
        else:
            out('BAD COVER ITEM'); allok = False
    else:
        out('UNKNOWN ITEM'); allok = False
    out('SUMMARY item %s CSfar_all_certified %s controls %s plants %s elapsed %.1f' % (item, allok, ctl_ok, plants_ok,
        time.time() - T0))
    out('VERDICT %s' % ('VALID' if (allok and ctl_ok and plants_ok) else 'NOT VALID'))


if __name__ == '__main__':
    main()
