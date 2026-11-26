"""majfix_v1_1.py -- pk02 (code/pk02/). REVISION of majfix_v1.py (46adb7b7) on the review REVIEW_MAJFIX_V1_rv01.md aed209b4
(majfix_v1 SOUND) and the F-2b rule (every trade takes the region's radius vector explicitly, with an assertion).
Changes, and nothing else (DIFF_majfix_v1_to_v1_1.txt); on today's callers (point t, pairs with u < v, a_e < a_pp exactly) they give the
same polynomials as v1:
  - evaluate raises t to the power k by repeated multiplication (tpow), never t ** k (python-flint 0.9 returns NaN when the t-ball holds 0).
  - atoms are keyed by (min(u, v), max(u, v)).
  - radv_for orders aa and a_e by a certain comparison (balls: aa > a_e or aa <= a_e must hold certainly; otherwise ValueError).
  check_radv(radv, aa, a_m, a_e): every factor certainly >= the region's radius for its variable (a_m, 4 a_m on sigma; max(a_e, aa),
       4 max(a_e, aa) on sigma''); RadiusError otherwise. The engines call it on each radius vector before any cap (C-RADV).
  tmono_bad(p): the number of coefficients of a form-basis polynomial that are not certainly >= 0 (C-TMONO on the capped pis before
       evaluation: with every coefficient >= 0 in (X, Q, d, t) and the cap's choices depending only on exponents and budgets, never on t's
       value, each capped pis_j is nondecreasing in t on the chart for fixed X: certified in the form basis before substitution).
majfix_v1 was: pk02 (code/pk02/). The trade fix shared by kt_cert_v1_8 and m2b_cert_v1_3, in balls.
The defects (pk02's F-2b):
  - kt_c_v2_3's radius trade (kt_cert_v1_7 l.790-810, m2b_cert_v1_2 l.459-480) lowers exponents monomial by monomial and keeps the
        coefficient's sign. For c < 0 that is a lower bound, so through D2 = (X_u - X_v)^2's cross term the xibar and xibar_cross l = 0
        entries and pi_vac's traded products fall below the functions they should majorize.
  - the annulus majorant pi0'' (aa = a_pp, region t X'' <= a_pp) was traded with AVt's a_e on sigma''.
The fix (float estimates kt_c_t_trade_v1 b4f85207, v1_1 242ab329, m2b_trade_est_v1 0ed5ef6c, v1_1 e5250506):
  1. Every majorant is built untraded, in M3's form (m3_major_v2 l.88-93, l.122; riglap2.Majorants):
       xibar_rs^(0)       = Q_rs/2 + t cfac(aa, 1) d_rs/8,
       xibar_rs^(l)       = l!/8 cfac(aa, l + 1) d_rs (X_r^(l-1) + X_s^(l-1))      (l >= 1; X^0 + X^0 read as 1),
       xibar_cross^(0)    = X_u + X_v + t cfac(aa, 1) d_uv/8                          (Q_uv/2 <= X_u + X_v),
       pi_vac^(j)         = [j = 0] + sum_{i=1..3} sum_b |q_i[b]| sum_{l <= min(i, j)} C(j, l) i!/(i - l)! t^(i - l) fbd(xibar, mono_b, j - l),
       pi_state^(j)       = [j = 0] |S_0b| + sum_b' |S_b'b| fbd(xibar, mono_b', j),
       pi_cross^(j)       = sum_l C(j, l) xibar_cross^(l) pi_vac^(j - l)               (pi_t: row T, pi_h: row M),
       pi_cross_state^(j) = sum_l C(j, l) xibar_cross^(l) pi_state^(j - l)            (kt_cert's pi_hb: h1, h3),
     in the form basis: polynomials in the 12 X/Q variables, one atom d_uv per pair (d_uv stands for (X_u - X_v)^2 >= 0) and a formal t.
     Every coefficient is a ball that is certainly >= 0 (C-TRADE-POS checks it before any trade).
  2. A cap (cap) trades each monomial only until its total degree (X/Q exponents plus 2 per atom) is at most a budget B. Each step consumes
     one formal t and is one of the fb steps on the chart Omega (t X_v <= r_v):
       lower an X:  t c d^beta X^alpha <= c d^beta r_v X^(alpha - e_v)   (smallest radius first, then largest exponent, then largest index),
       else a Q:    t Q_rs <= 4 r on the within-column pairs              (largest exponent, then largest index),
       else split:  t c d_uv d^beta' <= c d^beta' (r_u X_u + r_v X_v)     (d <= X_u^2 + X_v^2 since -2 X_u X_v <= 0; the atom whose pair (u, v) is largest).
     Unconsumed t powers stay exact. With B at today's degree no monomial is over budget with no formal t left (each of today's trades
     consumed one t); if one were, the cap stops (CapError). The radii are the region's (radv): a_m on sigma, max(a_e, aa) on sigma'',
     4x for Q (aa = a_pp on the annulus).
  3. evaluate sets the formal t to the item's t and expands each atom to D2 = (X_u - X_v)^2, giving the engine's NPolyA. evaluate_order
     keeps one formal-t order (nD's per-order law).
t-monotonicity: before evaluation a capped polynomial has coefficients >= 0 in (X, Q, d, t), and t enters only as explicit
nonnegative powers, so on the chart it is nondecreasing in t for fixed X; the traded factors are t-free.
Gates provided here (the engines call them and merge the failures into their verdicts):
  C-TRADE-POS  cap raises TradePosError on a coefficient ball that is not certainly >= 0 (a negative ball or one that straddles 0).
  C-P0SUB      p0sub: an untraded entry, evaluated, contains (ball-wise) the engine's own expansion of the same entry.
  C-MAJ-SAMPLE sample_check: at seeded points of the chart (and of the annulus' extended chart) plus the fixed point (X_r = 1, phi_s = 0),
               each majorant evaluated in float at the coefficient midpoints is >= |f^(l)(tau0)| for tau0 in {0, t/2, t}, f's derivatives
               from its float Taylor series (w(x, y) = (sqrt(1 - x) + sqrt(1 - y))^-2 by binomial series). A sampled check, not a proof.
Arithmetic: FormBasis(num=A) works in balls (the certified engines), FormBasis(num=float) in binary64 (the float twins, which are the
C-REP references): the same algorithm, the same steps in the same order, in two arithmetics.
No run of its own: imported by the engines (C-IMPORT pins this file's sha256).
"""
import math
import numpy as np
from flint import arb


class TradePosError(Exception):
    """C-TRADE-POS: a coefficient ball that is not certainly >= 0 reached the cap."""


class CapError(Exception):
    """a monomial over its budget with no formal t left."""


class RadiusError(Exception):
    """C-RADV: a radius factor below the region's radius for its variable."""


def A(x):
    return x if isinstance(x, arb) else arb(x)


def fval(x):
    """a float for sorting and comparing radii: a ball's midpoint, a float itself."""
    return float(x.mid()) if isinstance(x, arb) else float(x)


def cf_rad(aa, k, num=A):
    """cfac(aa, k) = (1 - aa)^-k (num = A: a ball; num = float: binary64)."""
    return 1 / (1 - num(aa)) ** k


class FormBasis:
    """form-basis polynomials: dicts {key: ball}, key = (12 X/Q exponents, NA atom exponents, formal-t exponent)."""

    def __init__(self, nv, xidx, qidx, na=12, num=A):
        self.num = num                       # A: balls (the certified engines); float: the float twins
        self.nv, self.X, self.Q, self.NA = nv, list(xidx), list(qidx), na
        self.TI = nv + na
        self.L = nv + na + 1
        self.ZK = (0,) * self.L
        self.atoms, self.pairs = {}, []
        self.cache = {}

    # ---- constructors and ring operations
    def atom(self, iu, iv):
        key = (min(iu, iv), max(iu, iv))                  # v1_1: one atom per unordered pair
        a = self.atoms.get(key)
        if a is None:
            if len(self.pairs) >= self.NA:
                raise ValueError('more than %d atoms' % self.NA)
            a = len(self.pairs)
            self.atoms[key] = a
            self.pairs.append(key)
        return a

    def mono(self, xs=(), atom=None, tk=0, c=1):
        e = [0] * self.L
        for i, k in xs:
            e[i] += k
        if atom is not None:
            e[self.nv + self.atom(*atom)] += 1
        e[self.TI] += tk
        return {tuple(e): self.num(c)}

    def one(self, c=1):
        return {self.ZK: self.num(c)}

    @staticmethod
    def add(*ps):
        res = {}
        for p in ps:
            for k, c in p.items():
                res[k] = res[k] + c if k in res else c
        return res

    def scale(self, p, s):
        s = self.num(s)
        return {k: c * s for k, c in p.items()}

    @staticmethod
    def mul(p, q):
        res = {}
        for k1, c1 in p.items():
            for k2, c2 in q.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                v = c1 * c2
                res[k] = res[k] + v if k in res else v
        return res

    def Mk(self, i, j, k):
        return self.one() if k == 0 else self.add(self.mono(((i, k),)), self.mono(((j, k),)))

    # ---- the untraded majorants (M3's form)
    def xibar(self, Xi, Qi, pairs, aa, nmax):
        res = []
        for p_, (r, s) in enumerate(pairs):
            d = self.mono(atom=(Xi[r], Xi[s]))
            lst = [self.add(self.mono(((Qi[p_], 1),), c=self.num(1) / 2), self.scale(self.mul(self.mono(tk=1), d), cf_rad(aa, 1, self.num) / 8))]
            for l in range(1, nmax + 1):
                lst.append(self.scale(self.mul(d, self.Mk(Xi[r], Xi[s], l - 1)),
                                      self.num(math.factorial(l)) / 8 * cf_rad(aa, l + 1, self.num)))
            res.append(lst)
        return res

    def xibar_cross(self, iu, iv, aa, nmax):
        d = self.mono(atom=(iu, iv))
        lst = [self.add(self.mono(((iu, 1),)), self.mono(((iv, 1),)), self.scale(self.mul(self.mono(tk=1), d), cf_rad(aa, 1, self.num) / 8))]
        for l in range(1, nmax + 1):
            lst.append(self.scale(self.mul(d, self.Mk(iu, iv, l - 1)), self.num(math.factorial(l)) / 8 * cf_rad(aa, l + 1, self.num)))
        return lst

    def fbd(self, xd, mono_, n):
        if len(mono_) == 1:
            return xd[mono_[0]][n]
        e1, e2 = mono_
        res = {}
        for l in range(n + 1):
            res = self.add(res, self.scale(self.mul(xd[e1][l], xd[e2][n - l]), math.comb(n, l)))
        return res

    def pi_vac(self, j, Xi, Qi, pairs, aa, QV, basis):
        key = ('vac', j, tuple(Xi), tuple(Qi), fval(aa))
        if key not in self.cache:
            xd = self.xibar(Xi, Qi, pairs, aa, j)
            res = self.one() if j == 0 else {}
            for i in (1, 2, 3):
                for cb, mono_ in zip(QV[i], basis):
                    if cb == 0.0:
                        continue
                    for l in range(0, min(i, j) + 1):
                        coef = self.num(math.comb(j, l) * (math.factorial(i) // math.factorial(i - l))) * abs(self.num(cb))
                        res = self.add(res, self.mul(self.mono(tk=i - l), self.scale(self.fbd(xd, mono_, j - l), coef)))
            self.cache[key] = res
        return self.cache[key]

    def pi_state(self, j, Xi, Qi, pairs, aa, s0, scol, basis):
        xd = self.xibar(Xi, Qi, pairs, aa, j)
        res = self.one(abs(self.num(s0))) if j == 0 else {}
        for cb, mono_ in zip(scol, basis):
            if cb != 0.0:
                res = self.add(res, self.scale(self.fbd(xd, mono_, j), abs(self.num(cb))))
        return res

    def pi_cross_state(self, j, iu, iv, aa_cross, Xi, Qi, pairs, aa_e, s0, scol, basis):
        """pi_hb (kt_cert's h1, h3): the cross pair's xibar times pi_state, untraded."""
        xh = self.xibar_cross(iu, iv, aa_cross, j)
        res = {}
        for l in range(j + 1):
            res = self.add(res, self.scale(self.mul(xh[l], self.pi_state(j - l, Xi, Qi, pairs, aa_e, s0, scol, basis)), math.comb(j, l)))
        return res

    def pi_cross(self, j, iu, iv, aa_cross, Xi, Qi, pairs, aa_e, QV, basis):
        xh = self.xibar_cross(iu, iv, aa_cross, j)
        res = {}
        for l in range(j + 1):
            res = self.add(res, self.scale(self.mul(xh[l], self.pi_vac(j - l, Xi, Qi, pairs, aa_e, QV, basis)), math.comb(j, l)))
        return res

    # ---- the cap (the fb steps, only as many as the budget needs)
    def cap(self, p, B, radv, stats=None):
        res = {}
        if stats is not None:
            stats['calls'] = stats.get('calls', 0) + 1
        for key, c in p.items():
            if not (c >= 0):
                raise TradePosError('coefficient %s at %r is not certainly >= 0' % (c.str(5, radius=True) if isinstance(c, arb) else repr(c), key))
            work = [(list(key), c)]
            while work:
                k, cc = work.pop()
                deg = sum(k[:self.nv]) + 2 * sum(k[self.nv:self.TI])
                if deg <= B:
                    kt = tuple(k)
                    res[kt] = res[kt] + cc if kt in res else cc
                    continue
                if k[self.TI] == 0:
                    raise CapError('degree %d > budget %d with no formal t left at %r' % (deg, B, key))
                if stats is not None:
                    stats['steps'] = stats.get('steps', 0) + 1
                k = list(k)
                k[self.TI] -= 1
                xs = [i for i in self.X if k[i] > 0]
                if xs:
                    i = min(xs, key=lambda q: (fval(radv[q]), -k[q], -q))
                    k[i] -= 1
                    work.append((k, cc * radv[i]))
                    continue
                qs = [i for i in self.Q if k[i] > 0]
                if qs:
                    i = max(qs, key=lambda q: (k[q], q))
                    k[i] -= 1
                    work.append((k, cc * radv[i]))
                    continue
                a = max((self.pairs[a_], a_) for a_ in range(len(self.pairs)) if k[self.nv + a_] > 0)[1]   # the largest pair (u, v)
                if stats is not None:
                    stats['splits'] = stats.get('splits', 0) + 1
                for w in self.pairs[a]:
                    k2 = list(k)
                    k2[self.nv + a] -= 1
                    k2[w] += 1
                    work.append((k2, cc * radv[w]))
        return res

    # ---- evaluation into the engine's NPolyA
    def evaluate(self, p, t, NPolyA, BB, D2, order=None):
        """the formal t set to t (a ball), each atom expanded by the engine's D2(u, v); order: keep only that formal-t exponent."""
        t = self.num(t)
        tp = [self.num(1)]                                # v1_1: t^k by repeated multiplication
        groups = {}
        for k, c in p.items():
            if order is not None and k[self.TI] != order:
                continue
            g = groups.setdefault(k[self.nv:self.TI], {})
            kk = k[:self.nv]
            while len(tp) <= k[self.TI]:
                tp.append(tp[-1] * t)
            v = c * tp[k[self.TI]] if k[self.TI] else c
            g[kk] = g[kk] + v if kk in g else v
        res = NPolyA(self.nv, BB)
        pw = {}
        for de, xs in groups.items():
            P = NPolyA.from_dict(xs, self.nv, BB)
            for a, e in enumerate(de):
                if e:
                    if (a, e) not in pw:
                        Q_ = D2(*self.pairs[a])
                        for _ in range(e - 1):
                            Q_ = Q_.mul(D2(*self.pairs[a]))
                        pw[(a, e)] = Q_
                    P = P.mul(pw[(a, e)])
            res = res.add(P)
        return res

    def max_t_order(self, p):
        return max((k[self.TI] for k in p), default=0)


def _greater(x, y, num):
    """x > y certainly (balls) or as binary64; ValueError when two balls are not certainly ordered (v1_1)."""
    if num is A:
        if A(x) > A(y):
            return True
        if A(x) <= A(y):
            return False
        raise ValueError('radv_for: %s and %s are not certainly ordered' % (A(x).str(8, radius=True), A(y).str(8, radius=True)))
    return float(x) > float(y)


def radv_for(aa, a_m, a_e, num=A):
    """the cap's radius factors by region: sigma X_v a_m (Q 4 a_m), sigma'' X_v max(a_e, aa) (Q 4 max(a_e, aa)); balls (num = A) or
    binary64 (num = float)."""
    ri = aa if _greater(aa, a_e, num) else a_e
    return [num(a_m)] * 3 + [4 * num(a_m)] * 3 + [num(ri)] * 3 + [4 * num(ri)] * 3


def check_radv(radv, aa, a_m, a_e, num=A):
    """C-RADV: every factor of radv certainly >= the region's radius for its variable; raises RadiusError."""
    need = radv_for(aa, a_m, a_e, num)
    for i, (r, q) in enumerate(zip(radv, need)):
        ok = bool(A(r) >= A(q)) if num is A else float(r) >= float(q)
        if not ok:
            raise RadiusError('radius factor %d below the region radius' % i)
    return True


def tmono_bad(p):
    """C-TMONO: the number of coefficients of a form-basis polynomial that are not certainly >= 0 (balls) or are negative (binary64)."""
    return sum(1 for c in p.values() if not (c >= 0))


def ydegs(h, n, ONE, NPolyA, BB, nv):
    """the largest total degree of Dbar's Y[m], m = 0..n (Dbar's recursion)."""
    Y = [ONE]
    for mm in range(n):
        acc = NPolyA(nv, BB)
        for i in range(mm + 1):
            acc = acc.add(h[i + 1].mul(Y[mm - i]).scale(math.comb(mm, i)))
        Y.append(acc)
    return [int(P.degrees().max()) if len(P.codes) else 0 for P in Y]


def p0sub(entry_eval, entry_engine):
    """C-P0SUB: every coefficient of entry_engine (the engine's own expansion) lies in the ball of entry_eval's, and both have the same
    support. Returns the number of mismatches."""
    a, b = entry_eval.to_dict(), entry_engine.to_dict()
    bad = 0
    for k in set(a) | set(b):
        ca, cb = a.get(k), b.get(k)
        if ca is None or cb is None or not (ca - cb).contains(0):
            bad += 1
    return bad


# ---------------------------------------------------------------- C-MAJ-SAMPLE (float, sampled)
KS = 6


def _s_mul(a, b):
    c = np.zeros_like(a)
    for k in range(KS + 1):
        c[:, k] = sum(a[:, i] * b[:, k - i] for i in range(k + 1))
    return c


def _s_inv(a):
    b = np.zeros_like(a)
    b[:, 0] = 1.0 / a[:, 0]
    for k in range(1, KS + 1):
        b[:, k] = -sum(a[:, i] * b[:, k - i] for i in range(1, k + 1)) / a[:, 0]
    return b


def _s_sqrt1(X, tau0):
    Ap = 1.0 - tau0 * X
    r = np.zeros((len(X), KS + 1))
    bk = 1.0
    for k in range(KS + 1):
        if k:
            bk *= (0.5 - (k - 1)) / k
        r[:, k] = np.sqrt(Ap) * bk * (-X / Ap) ** k
    return r


def _s_tau(n, tau0):
    r = np.zeros((n, KS + 1))
    r[:, 0] = tau0
    r[:, 1] = 1.0
    return r


def s_xi(Q, Xu, Xv, tau0):
    """the Taylor series in h of xi(tau0 + h) = Q/2 + ((tau0 + h)/2) (Xu - Xv)^2 w((tau0 + h) Xu, (tau0 + h) Xv)."""
    S = _s_sqrt1(Xu, tau0) + _s_sqrt1(Xv, tau0)
    w = _s_inv(_s_mul(S, S))
    r = 0.5 * ((Xu - Xv) ** 2)[:, None] * _s_mul(_s_tau(len(Q), tau0), w)
    r[:, 0] += Q / 2.0
    return r


def _s_prod(xs, mono_):
    r = xs[mono_[0]]
    for p in mono_[1:]:
        r = _s_mul(r, xs[p])
    return r


def s_pi(xs, tau0, QV, basis):
    n = xs[0].shape[0]
    r = np.zeros((n, KS + 1))
    r[:, 0] = 1.0
    T = _s_tau(n, tau0)
    Ti = np.zeros((n, KS + 1))
    Ti[:, 0] = 1.0
    for i in (1, 2, 3):
        Ti = _s_mul(Ti, T)
        for cb, mono_ in zip(QV[i], basis):
            if cb != 0.0:
                r = r + float(cb) * _s_mul(Ti, _s_prod(xs, mono_))
    return r


def s_state(xs, s0, scol, basis):
    n = xs[0].shape[0]
    r = np.zeros((n, KS + 1))
    r[:, 0] = float(s0)
    for cb, mono_ in zip(scol, basis):
        if cb != 0.0:
            r = r + float(cb) * _s_prod(xs, mono_)
    return r


def deriv(sr, l):
    return math.factorial(l) * sr[:, l]


def peval(P, Xp):
    """an NPolyA (or float NPoly) at the points Xp, coefficients at their midpoints."""
    if len(P.codes) == 0:
        return np.zeros(Xp.shape[0])
    ex = np.stack([(P.codes // P.pw[i]) % P.B for i in range(P.nv)], axis=1)
    co = np.array([float(c.mid()) if isinstance(c, arb) else float(c) for c in P.coeffs])
    V = np.ones((Xp.shape[0], len(P.codes)))
    for i in range(P.nv):
        if ex[:, i].any():
            V *= Xp[:, [i]] ** ex[:, i][None, :]
    return V @ co


def sample_points(J, a_out, a_in, nn, pairs, XS, QS, XD, QD, seed, npt=500):
    """chart points (phi in R^nn per site; outer at a_out, inner at a_in; X = |phi|^2 <= J a; Q_rs = |phi_r - phi_s|^2), the first three
    the fixed points (phi_r = e_1 at outer and inner site r of PAIRS[p], every other phi 0). Returns (X, QC) with QC the cross Q's."""
    rng = np.random.default_rng(seed)
    pts = []
    for p_, (r, s) in enumerate(pairs):
        phS = np.zeros((3, nn)); phD = np.zeros((3, nn))
        phS[r, 0] = 1.0; phD[r, 0] = 1.0
        pts.append((phS, phD))
    for _ in range(npt):
        ph = []
        for a in (a_out, a_in):
            P = rng.normal(size=(3, nn))
            P /= np.linalg.norm(P, axis=1, keepdims=True)
            u = rng.random(3) ** rng.choice([1.0, 2.0, 4.0])
            if rng.random() < 0.1:
                u[rng.integers(3)] = 1.0
            P *= np.sqrt(J * float(a) * u)[:, None]
            ph.append(P)
        pts.append((ph[0], ph[1]))
    X = np.zeros((len(pts), 12))
    QC = np.zeros((len(pts), 3))
    for n_, (phS, phD) in enumerate(pts):
        for r in range(3):
            X[n_, XS[r]] = phS[r] @ phS[r]
            X[n_, XD[r]] = phD[r] @ phD[r]
            QC[n_, r] = (phS[r] - phD[r]) @ (phS[r] - phD[r])
        for p_, (r, s) in enumerate(pairs):
            X[n_, QS[p_]] = (phS[r] - phS[s]) @ (phS[r] - phS[s])
            X[n_, QD[p_]] = (phD[r] - phD[s]) @ (phD[r] - phD[s])
    return X, QC


def sample_check(cells, nfixed=3):
    """cells: (name, majorant values (npts,), [f^(l) values per tau0]). A cell fails where M < |f| - 1e-12 max(1, |f|). Returns
    (failing cells [(name, count, worst |f|/M)], fixed-point failures of the cells named '* l0' among xibar_in/xibar_out)."""
    bad, fixed = [], 0
    for name, M, fl in cells:
        nb, wr = 0, 0.0
        for f in fl:
            af = np.abs(f)
            fail = M < af - 1e-12 * np.maximum(1.0, af)
            nb += int(np.count_nonzero(fail))
            with np.errstate(divide='ignore', invalid='ignore'):
                ratio = np.where(M > 0, af / M, np.where(af > 0, np.inf, 0.0))
            wr = max(wr, float(np.max(ratio)))
            if (name.startswith('xibar_in') or name.startswith('xibar_out')) and name.endswith(' l0'):
                fixed += int(np.count_nonzero(fail[:nfixed]))
        if nb:
            bad.append((name, nb, wr))
    return bad, fixed
