# Interval (numpy) assembly of the O(3) (N = 3) 3-row transfer and of its J-derivatives, for the Taylor-model interval
# scheme (wave 18; the O(3) counterpart of code4/certlib3.py, same output dict).  The column map is the quadruple table
# of code5/o3struct.py: (s', s, a, b) with SIGNED float coefficients c (error <= (cnt + 16) u cabs) and cabs = sum of the
# absolute values of the merged terms; a = vertical label of the bond rows 1-2 (T_X), b = rows 2-3 (T_Y).
# Terms of S(s',s): sqrtC(s') sqrtC(s) W_a W_b c, times e in {1, r_a, r_b, r_a r_b} for S, T_X, T_Y, T_XY, with
# C(s) = W_t W_h W_bb and W_l = i_l(J) = sqrt(pi/2J) I_{l+1/2}(J).  With rho = cs + r_a + r_b (cs = (R(s)+R(s'))/2):
#   (base e)'  = base (rho e + e'),   (base e)'' = base ((rho^2 + rho') e + 2 rho e' + e'').
# Interval arithmetic on (lo, hi) float arrays as in certlib3: a signed coefficient multiplies (lo, hi) in the order of
# its sign; the outward margins are relative to sum cabs |term| and cover the error of c, the float products and the sums
# (order 0: 4 (nmax + cmax + 18) u; orders >= 1: MARGIN = 1e-9, which dominates float rounding for <= 1e5 terms per entry).
# Boundary vector b = K^{1/2} M |000>: b(t, h, bb) = sqrtC W_t W_bb g(t, h, bb), g(a,b,c) = sqrt((2a+1)(2b+1)(2c+1)) (a b c; 000)
# (only p = t, q = bb reach |000>; checked against the quadruple table in code5/o3check.py).
import math
import numpy as np
from flint import arb
from o3struct import gval

MARGIN = 1e-9
U = 2.0 ** -53


def lohi(x):
    """Outward float interval of an arb ball."""
    lo = float(x.lower()); hi = float(x.upper())
    return np.nextafter(lo, -np.inf), np.nextafter(hi, np.inf)


def bessel_derivs(Ja, nmax):
    """O(3) weights k_l = W_l = i_l(J) = sqrt(pi/2J) I_{l+1/2}(J) and r_l, r'_l, r''_l, r'''_l (l = 0..nmax) as arb balls for
    J in the ball Ja (r = d/dJ log i_l).  r = l/J + u with u = I_{nu+1}/I_nu (nu = l + 1/2), u' = 1 - (2 nu + 1) u/J - u^2
    (Riccati).  Over a ball, u (increasing: u' > 0 is Amos's upper bound u < x/(nu+1/2+sqrt(x^2+(nu+1/2)^2)), nu >= 0) and
    w = u/J (decreasing: ratio of power series in x^2 with coefficient ratio 1/(k+nu+1)) are enclosed by the hull of their
    endpoint values, as is i_l (increasing, r > 0); the derivatives follow from the Riccati equation with
    w' = (1 - (2 nu + 2) w - u^2)/J, w'' = (u'' - 2 w')/J."""
    lo, hi = Ja.lower(), Ja.upper()
    if not (lo > 0):
        raise ValueError('J ball must be positive')
    def hull(a, b):
        l_ = a.lower() if a.lower() < b.lower() else b.lower()
        u_ = a.upper() if a.upper() > b.upper() else b.upper()
        return (l_ + u_) / 2 + (u_ - l_) / 2 * arb(0, 1)
    half = arb(1) / 2
    Il = [lo.bessel_i(arb(n) + half) for n in range(nmax + 2)]
    Ih = [hi.bessel_i(arb(n) + half) for n in range(nmax + 2)]
    plo = (arb.pi() / (2 * lo)).sqrt(); phi_ = (arb.pi() / (2 * hi)).sqrt()
    x = 1 / Ja
    res = {'k': [], 'W': [], 'r': [], 'r1': [], 'r2': [], 'r3': []}
    for l in range(nmax + 1):
        nu = arb(l) + half
        k = hull(plo * Il[l], phi_ * Ih[l])
        u = hull(Il[l + 1] / Il[l], Ih[l + 1] / Ih[l])
        w = hull(Il[l + 1] / (Il[l] * lo), Ih[l + 1] / (Ih[l] * hi))
        u1 = 1 - (2 * nu + 1) * w - u * u
        w1 = (1 - (2 * nu + 2) * w - u * u) * x
        u2 = -(2 * nu + 1) * w1 - 2 * u * u1
        w2 = (u2 - 2 * w1) * x
        u3 = -(2 * nu + 1) * w2 - 2 * u1 * u1 - 2 * u * u2
        res['k'].append(k); res['W'].append(k)
        res['r'].append(l * x + u)
        res['r1'].append(-l * x * x + u1)
        res['r2'].append(2 * l * x * x * x + u2)
        res['r3'].append(-6 * l * x * x * x * x + u3)
    return res


class IV:
    """Interval arrays (lo, hi) with numpy broadcasting; abs-sum tracking for rounding margins is done at reduction."""
    def __init__(self, lo, hi=None):
        self.lo = np.asarray(lo, dtype=float); self.hi = self.lo if hi is None else np.asarray(hi, dtype=float)
    def __add__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        return IV(self.lo + o.lo, self.hi + o.hi)
    __radd__ = __add__
    def __sub__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        return IV(self.lo - o.hi, self.hi - o.lo)
    def __mul__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return IV(np.minimum(np.minimum(p[0], p[1]), np.minimum(p[2], p[3])), np.maximum(np.maximum(p[0], p[1]), np.maximum(p[2], p[3])))
    __rmul__ = __mul__
    def sq(self):
        lo2, hi2 = self.lo ** 2, self.hi ** 2
        lo = np.where((self.lo >= 0) | (self.hi <= 0), np.minimum(lo2, hi2), 0.0)
        return IV(lo, np.maximum(lo2, hi2))
    def absmax(self):
        return np.maximum(np.abs(self.lo), np.abs(self.hi))
    def take(self, idx):
        return IV(self.lo[idx], self.hi[idx])


def ivec(lst):
    lo, hi = zip(*[lohi(x) for x in lst])
    return IV(np.array(lo), np.array(hi))


def widen(x, rel=1e-12):
    m = rel * x.absmax()
    return IV(x.lo - m, x.hi + m)


def assemble_derivs(Q, states, J, order, chunk=1500000, kshift=0.0, fac=None):
    """Interval matrices (flattened, entry sp*nS + s) for J in the arb ball J: S, TX, TY, TXY and their derivatives up to
    'order' (suffix 1, 2, 3); b and its derivatives; per-row r, r1, r2, r3.  With kshift = kappa and fac (arb ball), the
    four matrices and their derivatives are those of X(J) e^{-kappa (J - J0)} times fac, where the caller passes fac
    enclosing c e^{-kappa (J - J0)} over the ball (c a constant); b and r are unchanged."""
    nS, L = Q['nS'], Q['L']
    B = bessel_derivs(J, L)
    W, r, r1, r2, r3 = ivec(B['W']), ivec(B['r']), ivec(B['r1']), ivec(B['r2']), ivec(B['r3'])
    st = np.array(states)
    t_, h_, bb_ = st[:, 0], st[:, 1], st[:, 2]
    sqW = IV(np.sqrt(np.maximum(W.lo, 0)) * (1 - 1e-15), np.sqrt(W.hi) * (1 + 1e-15))
    sqC = sqW.take(t_) * sqW.take(h_) * sqW.take(bb_)
    R = r.take(t_) + r.take(h_) + r.take(bb_)
    R1 = r1.take(t_) + r1.take(h_) + r1.take(bb_)
    R2 = r2.take(t_) + r2.take(h_) + r2.take(bb_)
    n2 = nS * nS
    names = ['S', 'TX', 'TY', 'TXY']
    acc = {(nm, o, w): np.zeros(n2) for nm in names for o in range(order + 1) for w in ('lo', 'hi', 'ab')}
    nq = len(Q['c'])
    nmax = int(np.bincount(Q['sp'].astype(np.int64) * nS + Q['s'].astype(np.int64), minlength=nS * nS).max())
    margs = [4 * (nmax + int(Q['cnt'].max()) + 18) * U] + [MARGIN] * order
    two, three = IV(2.0), IV(3.0)
    for c0 in range(0, nq, chunk):
        sl = slice(c0, min(c0 + chunk, nq))
        a = Q['a'][sl].astype(np.int64); b = Q['b'][sl].astype(np.int64)
        idx = Q['sp'][sl].astype(np.int64) * nS + Q['s'][sl].astype(np.int64)
        cq = Q['c'][sl]; ca = Q['cabs'][sl]; pos = cq >= 0
        ra, rb, r1a, r1b, r2a, r2b = r.take(a), r.take(b), r1.take(a), r1.take(b), r2.take(a), r2.take(b)
        WW = W.take(a) * W.take(b)
        q = ra + rb; q1 = r1a + r1b; q2 = r2a + r2b
        qs = q.sq()
        one = IV(np.ones(len(a))); zero = IV(np.zeros(len(a)))
        exts = {'S': (one, zero, zero, zero), 'TX': (ra, r1a, r2a, r3.take(a)), 'TY': (rb, r1b, r2b, r3.take(b)),
                'TXY': (ra * rb, r1a * rb + ra * r1b, r2a * rb + two * r1a * r1b + ra * r2b,
                        r3.take(a) * rb + three * r2a * r1b + three * r1a * r2b + ra * r3.take(b))}
        for nm in names:
            e, e1, e2, e3 = exts[nm]
            terms = [WW * e, WW * (q * e + e1)]
            if order >= 2:
                terms.append(WW * ((qs + q1) * e + two * q * e1 + e2))
            if order >= 3:
                terms.append(WW * ((qs * q + three * q * q1 + q2) * e + three * (qs + q1) * e1 + three * q * e2 + e3))
            for o, v in enumerate(terms):
                acc[(nm, o, 'lo')] += np.bincount(idx, weights=np.where(pos, cq * v.lo, cq * v.hi), minlength=n2)
                acc[(nm, o, 'hi')] += np.bincount(idx, weights=np.where(pos, cq * v.hi, cq * v.lo), minlength=n2)
                acc[(nm, o, 'ab')] += np.bincount(idx, weights=ca * v.absmax(), minlength=n2)
    rows = np.repeat(np.arange(nS), nS); cols = np.tile(np.arange(nS), nS)
    half = IV(0.5)
    cs = half * (R.take(rows) + R.take(cols)) - IV(float(kshift)); c1s = half * (R1.take(rows) + R1.take(cols)); c2s = half * (R2.take(rows) + R2.take(cols))
    prem = sqC.take(rows) * sqC.take(cols)
    if fac is not None:
        flo, fhi = lohi(fac)
        prem = prem * IV(flo, fhi)
    out = {}
    U16 = 16 * U
    acs, ac1, ac2, apr = cs.absmax() + abs(float(kshift)), c1s.absmax(), c2s.absmax(), prem.absmax()
    def pad(x, a):
        """explicit rounding margin for the final combination (relative to the sum of absolute values of its terms)"""
        m = U16 * apr * a
        return IV(x.lo - m, x.hi + m)
    for nm in names:
        V = [IV(acc[(nm, o, 'lo')] - margs[o] * acc[(nm, o, 'ab')], acc[(nm, o, 'hi')] + margs[o] * acc[(nm, o, 'ab')]) for o in range(order + 1)]
        aV = [x.absmax() for x in V]
        out[nm] = pad(prem * V[0], aV[0])
        out[nm + '1'] = pad(widen(prem * (cs * V[0] + V[1])), acs * aV[0] + aV[1])
        if order >= 2:
            out[nm + '2'] = pad(widen(prem * ((cs.sq() + c1s) * V[0] + two * cs * V[1] + V[2])), (acs * acs + ac1) * aV[0] + 2 * acs * aV[1] + aV[2])
        if order >= 3:
            out[nm + '3'] = pad(widen(prem * ((cs.sq() * cs + three * cs * c1s + c2s) * V[0] + three * (cs.sq() + c1s) * V[1] + three * cs * V[2] + V[3])),
                                (acs ** 3 + 3 * acs * ac1 + ac2) * aV[0] + 3 * (acs * acs + ac1) * aV[1] + 3 * acs * aV[2] + aV[3])
    g = np.array([gval(int(s[0]), int(s[1]), int(s[2])) for s in states])
    gI = IV(g - 4 * U * np.abs(g), g + 4 * U * np.abs(g))
    bv = sqC * W.take(t_) * W.take(bb_) * gI
    rb_ = half * R + r.take(t_) + r.take(bb_)
    rb1 = half * R1 + r1.take(t_) + r1.take(bb_)
    rb2 = half * R2 + r2.take(t_) + r2.take(bb_)
    out['b'] = widen(bv); out['b1'] = widen(bv * rb_)
    if order >= 2:
        out['b2'] = widen(bv * (rb_.sq() + rb1))
    if order >= 3:
        out['b3'] = widen(bv * (rb_.sq() * rb_ + three * rb_ * rb1 + rb2))
    out['r'] = {'t': r.take(t_), 'h': r.take(h_), 'bb': r.take(bb_)}
    out['r1'] = {'t': r1.take(t_), 'h': r1.take(h_), 'bb': r1.take(bb_)}
    out['r2'] = {'t': r2.take(t_), 'h': r2.take(h_), 'bb': r2.take(bb_)}
    out['r3'] = {'t': r3.take(t_), 'h': r3.take(h_), 'bb': r3.take(bb_)}
    return out
