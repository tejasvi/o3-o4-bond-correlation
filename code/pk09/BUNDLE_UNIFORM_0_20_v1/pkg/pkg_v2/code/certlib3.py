# Interval (numpy) assembly of the 3-row transfer and of its first and second J-derivatives, for the Taylor-model
# interval scheme (wave 18 pilot).  The column map is cached as quadruples (s', s, a, b) with nonnegative coefficients
# c = sum over hub paths of exact 6j^2 (times g+1), converted to float64 (relative error <= (paths+1) u, recorded).
# Terms of S(s',s): sqrtC(s') sqrtC(s) W_a W_b c, times e in {1, r_a, r_b, r_a r_b} for S, T_X, T_Y, T_XY.
# With rho = cs + r_a + r_b (cs = (R(s)+R(s'))/2, R = sum of r over the 3 labels), rho' = c1s + r1_a + r1_b:
#   (base e)'  = base (rho e + e'),   (base e)'' = base ((rho^2 + rho') e + 2 rho e' + e'').
# All arithmetic is interval arithmetic on (lo, hi) float arrays with outward margins: every result is widened by
# 1e-9 (relative to the sum of absolute values of its terms), which dominates float rounding for <= 1e5 terms per entry.
import math, os
import numpy as np
from flint import arb

MARGIN = 1e-9


def quad_struct(st, cache=None):
    """Quadruple arrays from certlib2.build_struct (exact 6j values); cached to an .npz file if given."""
    if cache and os.path.exists(cache):
        z = np.load(cache)
        return dict(sp=z['sp'], s=z['s'], a=z['a'], b=z['b'], c=z['c'], cnt=z['cnt'], nS=int(z['nS']), L=int(z['L']))
    nS = len(st['states']); n_ = st['L'] + 1
    A2np = {}
    for key, lst in st['A2'].items():
        A2np[key] = (np.array([x[0] for x in lst], dtype=np.int64), np.array([float(x[1].mid()) for x in lst]),
                     np.array([x[2] for x in lst], dtype=np.int64))
    S_, A_, SP_, B_, C_, N_ = [], [], [], [], [], []
    for s, lst in st['A1'].items():
        # per source state: merge equal (s', a, b) over hub paths (keeps the peak memory small at L >= 14)
        sp_l, a_l, b_l, c_l = [], [], [], []
        for (key, v1, a) in lst:
            if key not in A2np:
                continue
            sp, v2, b = A2np[key]
            sp_l.append(sp); a_l.append(np.full(len(sp), a, dtype=np.int64)); b_l.append(b); c_l.append(float(v1.mid()) * v2)
        if not sp_l:
            continue
        sp = np.concatenate(sp_l); a = np.concatenate(a_l); b = np.concatenate(b_l); c = np.concatenate(c_l)
        key = (sp * n_ + a) * n_ + b
        uk, inv = np.unique(key, return_inverse=True)
        C_.append(np.bincount(inv, weights=c)); N_.append(np.bincount(inv).astype(np.int32))
        B_.append((uk % n_).astype(np.int16)); r_ = uk // n_
        A_.append((r_ % n_).astype(np.int16)); SP_.append((r_ // n_).astype(np.int32))
        S_.append(np.full(len(uk), s, dtype=np.int32))
    out = dict(sp=np.concatenate(SP_), s=np.concatenate(S_), a=np.concatenate(A_), b=np.concatenate(B_), c=np.concatenate(C_),
               cnt=np.concatenate(N_), nS=nS, L=st['L'])
    if cache:
        np.savez(cache, **out)
    return out


def lohi(x):
    """Outward float interval of an arb ball."""
    lo = float(x.lower()); hi = float(x.upper())
    return np.nextafter(lo, -np.inf), np.nextafter(hi, np.inf)


def bessel_derivs(Ja, nmax):
    """k_l, W_l, r_l, r'_l, r''_l, r'''_l (l = 0..nmax) as arb balls for J in the ball Ja (r = d/dJ log k_l).
    r = l/J + u with u = I_{nu+1}/I_nu (nu = l + 1), u' = 1 - (2 nu + 1) u/J - u^2 (Riccati).  Over a ball, u (increasing)
    and w = u/J (decreasing) are enclosed by the hull of their endpoint values (monotonicity from Amos's bounds
    x/(nu+1+sqrt(x^2+(nu+1)^2)) <= u <= x/(nu+1/2+sqrt(x^2+(nu+1/2)^2))), as is k (increasing); the derivatives follow
    from the Riccati equation with w' = (1 - (2 nu + 2) w - u^2)/J, w'' = (u'' - 2 w')/J, so no cancellation blows up."""
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
    res = {'k': [], 'W': [], 'r': [], 'r1': [], 'r2': [], 'r3': []}
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
        res['k'].append(k); res['W'].append((l + 1) * k)
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


def reduce_entries(vals, idx, n, cq):
    """Sum c_q * vals_q over entries idx (flattened), interval, with an outward rounding margin."""
    lo = np.bincount(idx, weights=cq * vals.lo, minlength=n)
    hi = np.bincount(idx, weights=cq * vals.hi, minlength=n)
    ab = np.bincount(idx, weights=cq * vals.absmax(), minlength=n)
    return IV(lo - MARGIN * ab, hi + MARGIN * ab)


def widen(x, rel=1e-12):
    m = rel * x.absmax()
    return IV(x.lo - m, x.hi + m)


def assemble_derivs(Q, states, J, order, chunk=1500000, kshift=0.0, fac=None):
    """Interval matrices (flattened, entry sp*nS + s) for J in the arb ball J: S, TX, TY, TXY and their derivatives up to
    'order' (suffix 1, 2, 3); b and its derivatives; per-row r, r1, r2 (and r3).  With kshift = kappa and fac (arb ball),
    the four matrices and their derivatives are those of X(J) e^{-kappa (J - J0)} times fac, where the caller passes fac
    enclosing c e^{-kappa (J - J0)} over the ball (c a constant); b and r are unchanged."""
    nS, L = Q['nS'], Q['L']
    B = bessel_derivs(J, L)
    W, r, r1, r2, r3, k = ivec(B['W']), ivec(B['r']), ivec(B['r1']), ivec(B['r2']), ivec(B['r3']), ivec(B['k'])
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
    # order-0 margin: the bincount sums of <= nmax products per entry, each with (cnt + 1) u relative error in c and
    # <= 4 roundings in WW e, are within (nmax + cmax + 8) u of the abs sum; orders >= 1 keep MARGIN (cancellation)
    nmax = int(np.bincount(Q['sp'].astype(np.int64) * nS + Q['s'].astype(np.int64), minlength=nS * nS).max())
    margs = [4 * (nmax + int(Q['cnt'].max()) + 8) * 2.0 ** -53] + [MARGIN] * order
    two, three = IV(2.0), IV(3.0)
    for c0 in range(0, nq, chunk):
        sl = slice(c0, min(c0 + chunk, nq))
        a = Q['a'][sl].astype(np.int64); b = Q['b'][sl].astype(np.int64)
        idx = Q['sp'][sl].astype(np.int64) * nS + Q['s'][sl].astype(np.int64)
        cq = Q['c'][sl]
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
                acc[(nm, o, 'lo')] += np.bincount(idx, weights=cq * v.lo, minlength=n2)
                acc[(nm, o, 'hi')] += np.bincount(idx, weights=cq * v.hi, minlength=n2)
                acc[(nm, o, 'ab')] += np.bincount(idx, weights=cq * v.absmax(), minlength=n2)
    rows = np.repeat(np.arange(nS), nS); cols = np.tile(np.arange(nS), nS)
    half = IV(0.5)
    cs = half * (R.take(rows) + R.take(cols)) - IV(float(kshift)); c1s = half * (R1.take(rows) + R1.take(cols)); c2s = half * (R2.take(rows) + R2.take(cols))
    prem = sqC.take(rows) * sqC.take(cols)
    if fac is not None:
        flo, fhi = lohi(fac)
        prem = prem * IV(flo, fhi)
    out = {}
    U16 = 16 * 2.0 ** -53
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
    bv = sqC * k.take(t_) * k.take(bb_)
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
