#!/usr/bin/env python3
"""m3_scal_v2.py -- pk03 (code/pk03/). The scalar layer of the certified M3 entries (PLAN_M3_CODE_v1_2 sect. A).
REVISION of m3_scal_v1.py (518fccf0): ive1 summed until the tail is negligible, the tail by t_k r_k/(1 - r_k); the mp.iv <-> arb crossings
(signed endpoints) with their round-trip test; spoly/spoly_iv/ka for the kernel (arb coefficients only); precision_line. Imported as
the generic name m3_scal by the job scripts. Everything else is v1.
Every scalar is an mp.iv interval at 40 digits (M-b): exact conversions of binary64, int and Fraction inputs; directed rounding of an
interval's ends to binary64; roots of nonnegative quantities; the tail, tree and far terms of riglap2; and small interval linear algebra
(Gauss-Jordan inverse, elimination determinant, interval Cholesky). The transcendentals are mpmath's native iv.exp, iv.log, iv.sqrt and
iv.pi; erfc enters only through the upper bound exp(-x^2)/(x sqrt pi) for x > 0 (ADD1 b); ive(1, x) by its positive series (ADD1 c);
expm1 as iv.exp(x) - 1 (ADD1 N2); no libm, scipy or *_series function is called on a certified quantity.
Conventions: functions named *_up return [0, U], where only U is a bound (U >= the true value, and the true value is >= 0); every other
function returns an enclosure. A NaN or an infinite end raises FloatingPointError (iv maps NaN to [-inf, inf] silently).
No compute of its own: imported by a frozen job script, which calls setup() before anything else.
"""
import math
from fractions import Fraction
from mpmath import iv, libmp

DPS = 40


def setup(dps=DPS):
    """iv.dps = 40 (iv.prec 136 bits); returns iv.prec."""
    iv.dps = dps
    return iv.prec


def finite(x):
    """x if both ends are finite, else FloatingPointError."""
    a, b = x._mpi_
    if a in (libmp.finf, libmp.fninf, libmp.fnan) or b in (libmp.finf, libmp.fninf, libmp.fnan):
        raise FloatingPointError('non-finite interval end: %r' % (x,))
    return x


def I(x):
    """an exact interval for an int, a binary64 float or a dyadic Fraction; an outward one for any other Fraction; intervals pass."""
    if hasattr(x, '_mpi_'):
        return finite(x)
    if isinstance(x, bool):
        raise TypeError('bool is not a number here')
    if isinstance(x, int):
        return iv.mpf(x)
    if isinstance(x, float):
        if not math.isfinite(x):
            raise FloatingPointError('non-finite input %r' % x)
        return iv.mpf(x)
    if isinstance(x, Fraction):
        return iv.mpf(x.numerator) / x.denominator
    raise TypeError('type %r' % type(x))


def up(x):
    """the smallest binary64 >= the upper end of x."""
    b = finite(I(x)).b
    f = float(b)
    if iv.mpf(f) < b:
        f = math.nextafter(f, math.inf)
    if not math.isfinite(f):
        raise FloatingPointError('upper end overflows binary64')
    return f


def down(x):
    """the largest binary64 <= the lower end of x."""
    a = finite(I(x)).a
    f = float(a)
    if iv.mpf(f) > a:
        f = math.nextafter(f, -math.inf)
    if not math.isfinite(f):
        raise FloatingPointError('lower end overflows binary64')
    return f


def certainly_pos(x):
    return bool(I(x).a > 0)


def nonneg(x):
    """x with its lower end raised to 0, for a quantity that is >= 0 by construction; a certainly negative x is an error."""
    x = I(x)
    if x.b < 0:
        raise ValueError('a nonnegative quantity is certainly negative: %r' % (x,))
    if x.a >= 0:
        return x
    return iv.mpf([iv.mpf(0), x.b])


def root(x, p):
    """the p-th root (integer p >= 1) of a nonnegative quantity: exp(log(.)/p) at each end, the lower end clipped at 0."""
    assert isinstance(p, int) and p >= 1
    x = nonneg(x)
    if p == 1:
        return x
    if x.b == 0:
        return iv.mpf(0)
    hi = iv.exp(iv.log(x.b) / p).b
    lo = iv.mpf(0) if x.a == 0 else iv.exp(iv.log(x.a) / p).a
    return finite(iv.mpf([lo, hi]))


def sqrt_nn(x):
    x = nonneg(x)
    return finite(iv.sqrt(x))


def ipow(x, k):
    """x^k for an integer k >= 0 by repeated multiplication (no pow)."""
    assert isinstance(k, int) and k >= 0
    out = iv.mpf(1)
    for _ in range(k):
        out = out * x
    return out


def isum(xs):
    out = iv.mpf(0)
    for x in xs:
        out = out + x
    return out


def chi_tail_up(s, n):
    """[0, U] with U >= P(chi^2_n > s), n = 2 or 3 (riglap2.chi_tail): exp(-s/2) for n = 2; for n = 3, erfc(x) + sqrt(2s/pi) exp(-s/2)
    with x = sqrt(s/2) > 0 asserted and erfc(x) <= exp(-x^2)/(x sqrt pi)."""
    s = I(s)
    if n == 2:
        u = iv.exp(-s / 2)
    elif n == 3:
        x = iv.sqrt(s / 2)
        if not x.a > 0:
            raise ValueError('chi_tail: s/2 not certainly > 0: %r' % (s,))
        u = iv.exp(-(x * x)) / (x * iv.sqrt(iv.pi)) + iv.sqrt(2 * s / iv.pi) * iv.exp(-s / 2)
    else:
        raise ValueError('n = %r' % n)
    return finite(iv.mpf([iv.mpf(0), finite(u).b]))


def ive1(x):
    """I_1(x) e^-x for x > 0 (x an interval; x <= 0 raises): the positive series sum_k t_k, t_k = (x/2)^(2k+1)/(k! (k+1)!), summed until
    the step ratio r_k = (x/2)^2/((k+1)(k+2)) at the upper end of x is below 1/2 AND the next term is below 1e-35 of the sum. The ratios
    decrease in k, so the omitted tail sum_{j>k} t_j <= t_k r_k/(1 - r_k) (r_k taken at the first omitted index), then times e^-x."""
    x = I(x)
    if not x.a > 0:
        raise ValueError('ive1 needs x > 0: %r' % (x,))
    h = x / 2
    h2 = h * h
    hb2 = h.b * h.b
    term = h
    acc = iv.mpf(0)
    k = 0
    while True:
        acc = acc + term
        r = hb2 / ((k + 1) * (k + 2))
        nxt = term * h2 / ((k + 1) * (k + 2))
        if r.b < iv.mpf(0.5) and nxt.b < acc.a * iv.mpf(1e-35):
            break
        term = nxt
        k += 1
        if k > 200000:
            raise ArithmeticError('ive1 series did not settle')
    tail = iv.mpf([iv.mpf(0), (term * r / (1 - r)).b])
    return finite((acc + tail) * iv.exp(-x))


def logtree(Jp, tree, N):
    """log of the tree bound for Z (riglap2.bound's logtree): N = 4: sum log(2 ive1(Jp c)/(Jp c)); N = 3: sum log((1 - e^(-2 Jp c))/(2 Jp c))."""
    Jp = I(Jp)
    out = iv.mpf(0)
    for c in tree:
        x = Jp * I(c)
        if N == 4:
            out = out + iv.log(2 * ive1(x) / x)
        elif N == 3:
            out = out + iv.log((1 - iv.exp(-2 * x)) / (2 * x))
        else:
            raise ValueError('N = %r' % N)
    return finite(out)


def logmain(J, V, N, log_tau):
    """riglap2.Graph.logmain: -(V-1) log(area) + (n/2)(V-1) log(2 pi/J) - (n/2) log tau, tau = det(Lsub)/V = det of the reduced Laplacian
    (matrix-tree), area = 2 pi^2 (N = 4) or 4 pi (N = 3), n = N - 1."""
    n = N - 1
    area = 2 * iv.pi * iv.pi if N == 4 else 4 * iv.pi
    J = I(J)
    return finite(-(V - 1) * iv.log(area) + iv.mpf(n) / 2 * (V - 1) * iv.log(2 * iv.pi / J) - iv.mpf(n) / 2 * I(log_tau))


def far_base(J, theta, ap, Gdiag, tree, N, V, log_tau):
    """exp of the far exponent at one theta (riglap2.bound l.374-376, riglap5b.Prep5): sum_v exp(-theta J ap/(2 G_vv)) times the tree bound at
    (1 - theta) J over main(J). Any theta in (0, 1) gives a valid bound."""
    J, th, ap = I(J), I(theta), I(ap)
    s = isum(iv.exp(-th * J * ap / (2 * I(g))) for g in Gdiag)
    return finite(iv.exp(iv.log(s) + logtree((1 - th) * J, tree, N) - logmain(J, V, N, log_tau)))


def ex_q(Gvv, q, n):
    """E[X^q] for X = |phi|^2, phi ~ N(0, Gvv I_n): (2 Gvv)^q prod_{i<q} (n/2 + i), exact rational factors (no lgamma)."""
    out = ipow(2 * I(Gvv), q)
    for i in range(q):
        out = out * (iv.mpf(n) / 2 + i)
    return out


# ------------------------------------------------------------------ small interval linear algebra (lists of lists of intervals)
def mat(rows):
    return [[I(x) for x in r] for r in rows]


def matmul(A, B):
    m, k, n = len(A), len(B), len(B[0])
    assert all(len(r) == k for r in A)
    return [[isum(A[i][l] * B[l][j] for l in range(k)) for j in range(n)] for i in range(m)]


def transpose(A):
    return [list(r) for r in zip(*A)]


def _pivot(M, col, rows):
    """the row in rows whose entry in col has the largest |midpoint|; its interval must exclude 0."""
    best = max(rows, key=lambda r: abs(M[r][col].mid))
    p = M[best][col]
    if p.a <= 0 <= p.b:
        raise ArithmeticError('pivot interval contains 0 in column %d: %r' % (col, p))
    return best


def inverse(A):
    """Gauss-Jordan with partial pivoting in mp.iv; every pivot interval must exclude 0."""
    n = len(A)
    M = [[I(x) for x in r] + [iv.mpf(1) if j == i else iv.mpf(0) for j in range(n)] for i, r in enumerate(A)]
    for c in range(n):
        p = _pivot(M, c, range(c, n))
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [[finite(x) for x in r[n:]] for r in M]


def det(A):
    """the determinant by elimination with partial pivoting in mp.iv; every pivot interval must exclude 0."""
    n = len(A)
    M = [[I(x) for x in r] for r in A]
    d = iv.mpf(1)
    for c in range(n):
        p = _pivot(M, c, range(c, n))
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        pv = M[c][c]
        d = d * pv
        for r in range(c + 1, n):
            f = M[r][c] / pv
            M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return finite(d)


def cholesky_pd(A):
    """interval Cholesky: (True, smallest pivot's lower end) if every pivot is certainly positive (then every symmetric matrix in A is
    positive definite), else (False, that pivot's lower end)."""
    n = len(A)
    Lm = [[iv.mpf(0)] * n for _ in range(n)]
    low = None
    for j in range(n):
        d = I(A[j][j]) - isum(Lm[j][k] * Lm[j][k] for k in range(j))
        low = d.a if low is None or d.a < low else low
        if not d.a > 0:
            return False, d.a
        Lm[j][j] = iv.sqrt(d)
        for i in range(j + 1, n):
            Lm[i][j] = (I(A[i][j]) - isum(Lm[i][k] * Lm[j][k] for k in range(j))) / Lm[j][j]
    return True, low


# ------------------------------------------------------------------ the mp.iv <-> arb crossings (tested by round trip in C-AK)
def _signed(raw):
    """(signed mantissa, exponent) of a raw mpf; libmp.to_man_exp drops the sign, which is raw[0]."""
    sign, man, exp, bc = raw
    return (-man if sign else man), exp


def iv_to_arb(x):
    """an arb ball containing the mp.iv interval x, from its exact signed endpoints (python-flint arb at the caller's ctx.prec)."""
    from flint import arb
    x = finite(I(x))
    a, b = x._mpi_
    (ma, ea), (mb, eb) = _signed(a), _signed(b)
    lo = arb(int(ma)) * arb(2) ** int(ea)
    hi = arb(int(mb)) * arb(2) ** int(eb)
    out = lo.union(hi)
    if not out.is_finite():
        raise FloatingPointError('iv_to_arb: non-finite ball')
    return out


def arb_to_iv(x):
    """an mp.iv interval containing the arb ball x: its exact lower and upper ends, each converted through (mantissa, exponent),
    then joined; the sign of each end is checked against the ball."""
    from mpmath import libmp as _lm
    if not x.is_finite():
        raise FloatingPointError('arb_to_iv: non-finite ball')
    ends = []
    for e in (x.lower(), x.upper()):
        m, ex = e.man_exp() if e != 0 else (0, 0)
        v = iv.make_mpf((_lm.from_man_exp(int(m), int(ex)), _lm.from_man_exp(int(m), int(ex))))
        if (e > 0 and not v.a > 0) or (e < 0 and not v.b < 0):
            raise ArithmeticError('arb_to_iv: sign lost in an endpoint')
        ends.append(v)
    return finite(iv.mpf([ends[0].a, ends[1].b]))


def ka(v):
    """a kernel coefficient as an arb ball: arb as is; mp.iv by iv_to_arb; Fraction, int, binary64 exactly (a Fraction outward)."""
    from flint import arb
    if isinstance(v, arb):
        return v
    if hasattr(v, '_mpi_'):
        return iv_to_arb(v)
    if isinstance(v, Fraction):
        return arb(v.numerator) / v.denominator
    if isinstance(v, bool):
        raise TypeError('bool coefficient')
    if isinstance(v, int):
        return arb(v)
    if isinstance(v, float):
        if not math.isfinite(v):
            raise FloatingPointError('non-finite coefficient')
        return arb(v)
    raise TypeError('coefficient type %r' % type(v))


def spoly(kern, d, nv):
    """the kernel polynomial with every coefficient passed as an arb ball (the stub's own mp.iv conversion is never used)."""
    return kern.SPoly.from_dict({tuple(e): ka(c) for e, c in d.items()}, nv) if d else kern.SPoly(nv)


def spoly_iv(P):
    """the kernel polynomial's coefficients as mp.iv intervals, through arb_to_iv."""
    return {e: arb_to_iv(c) for e, c in P.to_arb_dict().items()}


def arb_mat_of(M):
    from flint import arb_mat
    n, m = len(M), len(M[0])
    A = arb_mat(n, m)
    for i in range(n):
        for j in range(m):
            A[i, j] = ka(M[i][j])
    return A


def precision_line():
    import flint
    return 'iv.dps %d (iv.prec %d); flint ctx.prec %d, ctx.cap %d' % (iv.dps, iv.prec, flint.ctx.prec, flint.ctx.cap)


def crossings_test():
    """C-AK's crossing checks: values of both signs, zero, tiny and huge, through iv_to_arb and arb_to_iv; each round trip must contain
    its source. Also the plant: an unsigned conversion (the stub's to_man_exp form) must fail on a negative value. Returns (ok, plant_fired)."""
    from flint import arb
    vals = [iv.mpf(1) / 3, -iv.mpf(1) / 3, iv.mpf(0), iv.mpf(['-1e-300', '2e-300']), -iv.exp(iv.mpf(700)) / 7, iv.mpf([-2, 5]),
            iv.mpf(-0.4409407) * iv.sqrt(21)]
    ok = True
    for v in vals:
        a = iv_to_arb(v)
        back = arb_to_iv(a)
        ok = ok and bool(back.a <= v.a) and bool(v.b <= back.b)
        ok = ok and bool(iv_to_arb(back).contains(a))
    neg = -iv.mpf(1) / 3
    sa, sb = neg._mpi_
    man, ex = sa[1], sa[2]
    bad = arb(int(man)) * arb(2) ** int(ex)
    fired = not bool(bad.contains(iv_to_arb(neg)))
    return ok, fired
