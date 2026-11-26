#!/usr/bin/env python3
"""arbeng_ma_v1_4.py -- pk02 (code/pk02/). REVISION of arbeng_ma_v1_3.py (075e3586) by DESIGN_ARBENG_MA_v1_4.md (f01a6429
SOUND 53de1c0d; the approval of 2026-11-08 for pk03's certified D16 H/S4 records). Every function and class of v1_3 is kept byte-identical,
so existing callers get identical results; VERSION and this docstring change, and one section is added at the end:
  (A) MomTableU: MomTable's recursion computed in destination code blocks (the pull form: base-B codes add without carry, so the q of a
      block [lo, hi) for subset A are codes_(k-j) in [lo - cA, hi - cA), a contiguous range), with one seg_pairwise tree per destination,
      products by _prod (tiny rule), D_j pre-scaled by the exact nonzero half-integer coef_j(k), div_int(k) and the factorial scaling as
      v1_3; C-PAIRS: the candidate pairs generated equal plan()'s exact count block by block, and no destination has more than
      2^|supp c| - 1 terms;
  (B) resumable units (level k, block range) with verified state: npz files of raw arrays carrying their codes, written atomically (a
      temporary name, then a rename that never overwrites; the hand-off JSON last), hand-offs with each file's size and sha256, the parameter
      hash H_par (exact Gam entries, n, D, F, groups, caps, W_int, block, VERSION, this file's sha256), the kernel's sha256 and the code arrays'
      sha256; loaders recompute the codes and require exact equality with the stored ones, and level assembly requires the units to
      partition the blocks in code order with one H_par, level and kernel sha; any mismatch is a ValueError (C-STATE); units stop between
      blocks on an optional CPU budget, never inside one; MomTableView, a read-only MomTable;
  (C) blocked E2 (E2_plan with a deterministic order and blocks that partition P, E2_check_plan, E2_block returning a lossless M-a scalar
      after MA.check and the block's ball conversion, E2_combine with one MAFallback relative-error test on the total), scalar_sum_fast
      (bit-identical to scalar_sum on one segment), ma_scalar_dump/load, and compare_float (INFO only).
arbeng_ma_v1_3 was: the REVISION of arbeng_ma_v1_2.py (da68ebcb), by the rule on ADD3 (DELTA_SPEC_MA_LAYER_
v1_2_ADD3_rv01 c738f014) and SPEC_MA_LAYER_v1_2_ADD3b. Changes, and nothing else:
  - the einsum allowances are added with an upward step, Xr := nextafter(Xr0 + nextafter(n a, +inf), +inf) and the same for GSr: in
       round-to-nearest a (about 1e-323) vanished from every kept entry, leaving a band just above TINY covered by neither the allowance
       nor gamma's slack;
  - Y's allowance uses 1 + max(Pmax, Smax) (Smax = max Sr at that level), since the einsum may form (P P) S first, scaling the first
       eta by an S entry; the allowance itself is rounded up;
  every einsum call passes optimize=False explicitly; C-UF also reports Smax (self.smax).
arbeng_ma_v1_2 was the REVISION of arbeng_ma_v1_1.py (2968dd9f; its validation's piece v1 stopped on a subnormal
shadow product from the structural zeros of A's 0 <-> 2 symmetry), by SPEC_MA_LAYER_v1_2_ADD3 (12091946; the approval 2026-11-07). Changes,
and nothing else:
  (1) the tiny rule (_tiny_rule, _prod) at every product, scaling and integer-division site, after each multiplication: a term with lower
      shadow <= TINY = 2^-969 becomes error-only (mid 0, sa 0, sr >= 2 TINY); an exact-zero factor (sr = 0) keeps the term exactly 0; it
      replaces v1_1's subnormal MAFallback (_check_range, removed) and closes the sr-underflow gap (ADD3 Claims A-E);
  (2) CondTable's two einsum contractions add n (1 + Pmax) 2^-1073 (Y) and n 2^-1073 (GS) to the upper shadow per entry, n the exact count
      of all-nonzero products, then apply the rule (ADD3 sect. 3);
  (3) present() tests sr too, so error-only entries [0 +- r] are never dropped; exact inputs (rad = 0) keep sr = sa, so exact zeros stay
      absent (MA.inputs, mat_in, condE's and SPoly.scale's coefficient);
  (4) the int64 monomial-code guard is exact (B**nv < 2**63 in integers) at every encoder (MomTable, CondTable, condE, npoly_mul, _merge,
      SPoly.codes) and raises ValueError, never MAFallback (_code_guard).
  The interface (SPEC_MA_LAYER_v1_3_API) is unchanged; MAFallback no longer covers subnormal products.
arbeng_ma_v1_1 was the REVISION of arbeng_ma_v1.py (453c3ab3, frozen and never run): mpi_to_arb read
libmp.to_man_exp's unsigned mantissa, so a negative mp.iv endpoint entered arb as positive (found by pk03 in the stub's identical
code; main checked). Changes, and nothing else: mpi_to_arb reads the sign from mpmath's raw tuple (sign, man, exp, bc) and raises
MAFallback on infinite or nan endpoints; arb_to_mpi raises MAFallback on a non-finite ball. The interface is frozen in
SPEC_MA_LAYER_v1_3_API.md.
arbeng_ma_v1 was the M-a layer of SPEC_MA_LAYER_v1_2 (d8b05870),
whose conditions are folded in (SPEC_MA_LAYER_v1_2_ADD1). Interface of its sect. 6, as the build target arbeng_ma_stub_v1.py (0cfd5f65)
has it, plus the keyword W= beside W_int. Binary64 kernels with rounding counts and shadows under SPEC_M1_CERT_v1_1 (c81c956f) sect. 1
(M-a to M-e) with ADD1 (badf0f57):
  K1 MomTable, allmom2, AllMom2   amom2b.AllMom2 (moments from the principal minors; exact zeros for rank-deficient subsets)
  K2 CondTable, condmom           condexp2.CondMom, with condE (condg.CondG.condE)
  K3 MomTable.E, .E2              amom2b.E / E2, riglap2.expect_np
  K4 npoly_mul, npoly_pow, SPoly  npoly.NPoly.mul, pseries.pmul (products with interval coefficients)
  K5 lp_norm, pos_norm            riglap4.lp_norm (p even), riglap4.pos_norm
Model. Each computed binary64 quantity carries a rounding count k and a shadow: |fl(x) - x| <= gamma_k X. Three passes side by side: the
  midpoint (mid), the shadow at a = |x_mid| (sa) and at a point >= a + rad (sr). Counts per M-a: k(x +- y) = max + 1, k(x y) = k_x + k_y
  + 1. C-TREE: every sum of many terms is an explicit pairwise tree (seg_pairwise, tree_sum), never numpy's sequential or blocked
  reductions on values, and the count that enters gamma_k is the one TRACKED per element by that rule, never a formula in the number of
  terms (merging trees of sizes that are not powers of 2 can exceed ceil(log2 n) by one); tree_check() is the self-test. Small
  contractions (einsum over at most F^2 terms) are counted as sequential sums (n - 1 additions), an upper bound for any order. Division
  only by exact integers. Interval inputs from arb balls: x_mid the binary64 rounding of the midpoint, rad an upward radius covering the
  ball and that rounding. Error of an entry: sr/(1 - g) - sa/(1 + g) + g sa/(1 - g) with g = gamma_k (formed in arb, rounded up),
  evaluated in binary64 with the margin 4u (A + B + C) for its own roundings; scalar results are formed in arb. Every returned ball
  contains the exact value for every input in the input balls, M-a error included.
Errors. MAFallback, a plain Exception and not an ArithmeticError, is the only exception a caller may catch to recompute
  in arb: an M-a result whose relative error exceeds FALLBACK_REL, or an arb ball outside binary64's range at conversion (v1_2: subnormal
  products go through the tiny rule instead). Every other exception stops the run, and no soundness condition rests on
  assert. condmom and allmom2 take W_int together with W (the forms as an arb_mat): every W ball must be an exact integer equal to W_int
  (ValueError otherwise); that Gam is W^T C W is the caller's part.
arb conditions. No python-flint series function and no change of ctx.cap (static_check() reads this file); ctx.prec must be
  PREC = 512, checked at every kernel entry; scalar results are checked finite; logs and roots only on balls with a positive lower end,
  and for a nonnegative ball touching 0 the monotone endpoint form (the root of the upper end, rounded up). The layer uses no erfc and no
  ive (those belong to pk03's scalar module). M-d: errstate raises; arrays checked finite. M-e: env_probes(), which also prints
  ctx.prec, ctx.cap and the static check.
C-BUDGET (budget()) is quality control, not a soundness gate: the balls already include the M-a error. Its form per entry and the
  definition of "the M-a part" (assemble twice in arb, with and without the kernels' M-a radii) are in SPEC_MA_LAYER_v1_2_ADD1.
No compute of its own: imported by a frozen job script that pins this file's sha256.
"""
import math, itertools, os, re
from fractions import Fraction
import numpy as np
from flint import arb, arb_mat, ctx
from mpmath import iv

VERSION = 'arbeng_ma_v1_4'
PREC = 512
U = 2.0 ** -53
TINY = 2.0 ** -1022 / U
TWO_TINY = 2.0 * TINY
UF_ALLOW = 2.0 ** -1073      # 4 x 2^-1075 per nonzero product of an einsum: mid's underflow, sr's down and sa's up
HUGE = 2.0 ** 1000
FALLBACK_REL = 1e-3
TINY_COUNT = [0]             # terms made error-only by the tiny rule (reported by the validation's C-TINY)


class MAFallback(Exception):
    """the only exception a caller may catch to recompute in arb (sect. 4): an M-a result whose relative error exceeds FALLBACK_REL, or a
    ball outside binary64's range at conversion. Every other exception stops the run."""


def _check_prec():
    if ctx.prec != PREC:
        raise RuntimeError('ctx.prec is %d, the layer needs %d' % (ctx.prec, PREC))


def _tiny_rule(mid, sa, sr, zero):
    """the tiny rule (arbeng_ma_v1_2; SPEC_MA_LAYER_v1_2_ADD3), applied to the terms of every product, scaling and integer division: a
    term whose lower shadow is at most TINY becomes error-only (mid = 0, sa = 0), and its upper shadow is raised to 2 TINY when it is at
    most TINY; exact zeros (zero: a factor with upper shadow 0, or a zero scale) stay 0. A term kept as it is has sa > TINY, so its mid and
    both shadows are normal numbers and M-a's relative model holds without underflow."""
    t = (sa <= TINY) & ~zero
    if not np.any(t):
        return mid, sa, sr
    TINY_COUNT[0] += int(np.count_nonzero(t))
    return np.where(t, 0.0, mid), np.where(t, 0.0, sa), np.where(t & (sr <= TINY), TWO_TINY, sr)


def _code_guard(B, nv, where):
    """ADD3 sect. 5: monomial codes are int64 integers in [0, B^nv); the check B**nv < 2**63 is in exact integer arithmetic, and a failure
    is a ValueError (a hard stop, never MAFallback): the caller must split the forms."""
    if not (int(B) ** int(nv) < 2 ** 63):
        raise ValueError('%s: monomial codes would overflow int64 (%d^%d >= 2^63): split the forms' % (where, int(B), int(nv)))


def up(x):
    """a binary64 number >= every point of the arb ball x; MAFallback if x is not finite or leaves binary64's range."""
    if not x.is_finite():
        raise MAFallback('a non-finite ball at conversion')
    u = x.upper()
    if u > HUGE or u < -HUGE:
        raise MAFallback('a ball outside binary64 range at conversion')
    f = float(u)
    if not (arb(f) >= u):
        f = math.nextafter(f, math.inf)
    if not (arb(f) >= u):
        raise RuntimeError('upward rounding failed')
    return f


_GAMMA = {}


def gamma_up(k):
    k = int(k)
    if k not in _GAMMA:
        ka = arb(k) * arb(2) ** -53
        if not (ka < 1):
            raise RuntimeError('rounding count %d out of range' % k)
        _GAMMA[k] = up(ka / (1 - ka))
    return _GAMMA[k]


def gamma_arr(k):
    ks, inv = np.unique(np.asarray(k, dtype=np.int64), return_inverse=True)
    return np.array([gamma_up(int(x)) for x in ks])[inv]


def ball_to_in(x):
    """(x_mid, rad) of an arb ball: the binary64 midpoint and an upward radius covering the ball and that rounding; MAFallback if the ball
    is not finite or leaves binary64's range."""
    if not x.is_finite():
        raise MAFallback('a non-finite ball at conversion')
    mid = x.mid()
    if mid > HUGE or mid < -HUGE:
        raise MAFallback('a ball outside binary64 range at conversion')
    m = float(mid)
    return m, up(x.rad() + abs(mid - arb(m)))


def static_check():
    """C-TREE's static part: this file never calls a python-flint series function, never sets ctx.cap,
    and never uses numpy's weighted bin counts or reduce-at / add-at accumulations (the tokens are built at runtime)."""
    with open(os.path.abspath(__file__)) as fh:
        src = fh.read()
    bad = [tok for tok in ('_' + 'series', 'bin' + 'count', 'reduce' + 'at', '.add' + '.at(', 'setattr(' + 'ctx') if tok in src]
    if re.search(r'ctx\s*\.\s*cap\s*=(?!=)', src):
        bad.append('assignment to ctx.cap')
    if bad:
        raise RuntimeError('static check failed: %s' % ', '.join(bad))
    return 'static check PASS (no series function, no ctx.cap assignment, no sequential numpy accumulation)'


def env_probes():
    """M-e: round-to-nearest (both signs) and no flush-to-zero / denormals-are-zero, with operands built at runtime; ctx.prec must be
    PREC; prints ctx.prec, ctx.cap and the static check."""
    a = math.ldexp(3, -54)
    ok1 = (1.0 + a) == 1.0 + 2.0 ** -52
    ok2 = (-1.0 - a) == -(1.0 + 2.0 ** -52)
    ok3 = math.ldexp(1, -1074) > 0 and math.ldexp(1, -1022) / 2 != 0
    z = np.array([math.ldexp(1, -1022)]) / 2.0
    ok4 = bool(z[0] != 0.0)
    if not (ok1 and ok2 and ok3 and ok4):
        raise RuntimeError('M-e probe failed: nearest %s %s, subnormals %s, numpy subnormals %s' % (ok1, ok2, ok3, ok4))
    _check_prec()
    return ('M-e probes PASS (round-to-nearest both signs; subnormals kept in python and numpy); numpy %s; %s; ctx.prec %d, ctx.cap %d; %s'
            % (np.__version__, VERSION, ctx.prec, ctx.cap, static_check()))


def budget(err, bar):
    """C-BUDGET, quality control only and not a soundness gate (the balls already include the M-a error): the M-a part err at most 0.1
    of the bar it is held against (the bar per entry: SPEC_MA_LAYER_v1_2_ADD1)."""
    return float(err) <= 0.1 * float(bar)


class MA:
    """M-a values on an index set: mid, sa, sr (float64), k (int64)."""
    __slots__ = ('mid', 'sa', 'sr', 'k')

    def __init__(self, mid, sa, sr, k):
        self.mid, self.sa, self.sr, self.k = mid, sa, sr, k

    @staticmethod
    def zeros(n):
        return MA(np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n, dtype=np.int64))

    @staticmethod
    def inputs(mids, rads):
        """interval inputs: sa = |x_mid|, sr = sa + rad rounded up; an exact input (rad = 0) keeps sr = sa, so an exact zero stays
        absent (arbeng_ma_v1_2)."""
        mids = np.asarray(mids, dtype=float)
        rads = np.asarray(rads, dtype=float)
        sa = np.abs(mids)
        return MA(mids, sa, np.where(rads == 0.0, sa, np.nextafter(sa + rads, np.inf)), np.zeros(len(mids), dtype=np.int64))

    @staticmethod
    def exact(vals):
        vals = np.asarray(vals, dtype=float)
        return MA(vals, np.abs(vals), np.abs(vals), np.zeros(len(vals), dtype=np.int64))

    def take(self, idx):
        return MA(self.mid[idx], self.sa[idx], self.sr[idx], self.k[idx])

    def present(self):
        """an entry is present unless it is an exact zero (value and both shadows 0); error-only entries (mid = sa = 0 < sr) are present
        (arbeng_ma_v1_2: v1_1 tested mid and sa only, and dropped them)."""
        return (self.mid != 0.0) | (self.sa != 0.0) | (self.sr != 0.0)

    def scale(self, c):
        a = abs(float(c))
        mid, sa, sr = _tiny_rule(self.mid * c, self.sa * a, self.sr * a, (self.sr == 0.0) | (a == 0.0))
        return MA(mid, sa, sr, self.k + 1)

    def div_int(self, n):
        n = np.asarray(n)
        if not (np.all(n > 0) and np.all(n <= 2 ** 53)):
            raise ValueError('division by an integer outside [1, 2^53]')
        nf = n.astype(float)
        mid, sa, sr = _tiny_rule(self.mid / nf, self.sa / nf, self.sr / nf, self.sr == 0.0)
        return MA(mid, sa, sr, self.k + 1)

    def check(self, label):
        for arr in (self.mid, self.sa, self.sr):
            if not np.all(np.isfinite(arr)):
                raise FloatingPointError('non-finite value in %s' % label)
        if not (np.all(self.sa >= 0) and np.all(self.sr >= self.sa)):
            raise RuntimeError('shadow order violated in %s' % label)

    def radius(self):
        g = gamma_arr(self.k)
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            A = self.sr / (1.0 - g)
            B = self.sa / (1.0 + g)
            C = g * self.sa / (1.0 - g)
            return (A - B + C) + 4.0 * U * (A + B + C)

    def shadow_max(self):
        """C-SHADOW: the largest gamma_k sa/|mid| over the entries with a nonzero midpoint."""
        nz = self.mid != 0.0
        if not np.any(nz):
            return 0.0
        return float(np.max(gamma_arr(self.k[nz]) * self.sa[nz] / np.abs(self.mid[nz])))


def ma_add(x, y):
    """x + y entrywise (one addition where both are present)."""
    px, py = x.present(), y.present()
    k = np.where(px & py, np.maximum(x.k, y.k) + 1, np.where(px, x.k, y.k))
    return MA(x.mid + y.mid, x.sa + y.sa, x.sr + y.sr, k)


def tree_sum(arrs):
    """pairwise sum of a list of MA arrays of equal length (count per entry by the addition rule)."""
    arrs = [a for a in arrs if a is not None]
    if not arrs:
        return None
    while len(arrs) > 1:
        nxt = [ma_add(arrs[i], arrs[i + 1]) for i in range(0, len(arrs) - 1, 2)]
        if len(arrs) % 2:
            nxt.append(arrs[-1])
        arrs = nxt
    return arrs[0]


def seg_pairwise(dst, mid, sa, sr, k, n_out):
    """the per-destination pairwise sums of terms (dst, mid, sa, sr, k) into an MA of length n_out: the terms are sorted by destination
    and adjacent terms of a segment are added level by level, each addition counted max + 1 per element."""
    out = MA.zeros(n_out)
    if len(dst) == 0:
        return out
    order = np.argsort(dst, kind='stable')
    d, m, a, r, kk = dst[order], mid[order], sa[order], sr[order], k[order].astype(np.int64)
    while True:
        new = np.empty(len(d), dtype=bool)
        new[0] = True
        new[1:] = d[1:] != d[:-1]
        starts = np.flatnonzero(new)
        sid = np.cumsum(new) - 1
        pos = np.arange(len(d)) - starts[sid]
        slen = np.diff(np.append(starts, len(d)))
        if slen.max() == 1:
            break
        i = np.flatnonzero((pos % 2 == 0) & (pos + 1 < slen[sid]))
        m[i] = m[i] + m[i + 1]
        a[i] = a[i] + a[i + 1]
        r[i] = r[i] + r[i + 1]
        kk[i] = np.maximum(kk[i], kk[i + 1]) + 1
        keep = pos % 2 == 0
        d, m, a, r, kk = d[keep], m[keep], a[keep], r[keep], kk[keep]
    out.mid[d], out.sa[d], out.sr[d], out.k[d] = m, a, r, kk
    return out


def scalar_sum(mid, sa, sr, k):
    """pairwise sum of one array to a single MA value (returned as an MA of length 1)."""
    return seg_pairwise(np.zeros(len(mid), dtype=np.int64), mid, sa, sr, k, 1)


def tree_check(ms=(1, 2, 3, 5, 8, 12)):
    """C-TREE: a sum of 2^m + 1 unit terms must report the tracked count m + 1 (seg_pairwise), and tree_sum of that sum
    with a 3-term sum must report m + 2, one more than ceil(log2(2^m + 4)) for m >= 2: the tracked count, not the formula, enters gamma_k.
    Returns (ok, lines)."""
    ok, lines = True, []
    for m in ms:
        n = 2 ** m + 1
        a = scalar_sum(np.ones(n), np.ones(n), np.ones(n), np.zeros(n, dtype=np.int64))
        b = scalar_sum(np.ones(3), np.ones(3), np.ones(3), np.zeros(3, dtype=np.int64))
        c = tree_sum([a, b])
        ka, kc, formula = int(a.k[0]), int(c.k[0]), math.ceil(math.log2(n + 3))
        okm = ka == m + 1 and float(a.mid[0]) == n and kc == m + 2 and float(c.mid[0]) == n + 3 and (m < 2 or kc == formula + 1)
        ok = ok and okm
        lines.append('m %d: %d terms k %d (want %d); merged with 3 terms k %d (want %d; formula %d)' % (m, n, ka, m + 1, kc, m + 2, formula))
    return ok, lines


def _prod(fa, fb, extra=None):
    """the terms of an entrywise product of MA factors given as (mid, sa, sr) triples (two or three), with the tiny rule after each
    multiplication (ADD3 sect. 2); zero marks a factor with upper shadow 0 (an exact zero), taken from the factors, never the product."""
    mid, sa, sr = fa
    zero = fa[2] == 0.0
    for m2, a2, r2 in [fb] + ([extra] if extra is not None else []):
        zero = zero | (r2 == 0.0)
        mid, sa, sr = _tiny_rule(mid * m2, sa * a2, sr * r2, zero)
    return mid, sa, sr


def scatter_prod(n_out, supk, ca, a, cb, b, chunk=4000000):
    """sum over pairs (p, q) with ca[p] + cb[q] = c (c in supk) of a[p] b[q]: amom2b.sprod / condexp2._acc in M-a, pairwise per
    destination within a chunk and across chunks; the terms through the tiny rule (_prod)."""
    pb = np.flatnonzero(b.present())
    cb, b = cb[pb], b.take(pb)
    parts = []
    if len(cb) == 0 or len(ca) == 0:
        return MA.zeros(n_out)
    rows = max(1, chunk // len(cb))
    for s0 in range(0, len(ca), rows):
        cs = (ca[s0:s0 + rows, None] + cb[None, :]).ravel()
        idx = np.searchsorted(supk, cs)
        idx[idx >= len(supk)] = 0
        hit = np.flatnonzero(supk[idx] == cs)
        if len(hit) == 0:
            continue
        p = s0 + hit // len(cb)
        q = hit % len(cb)
        mid, sa, sr = _prod((a.mid[p], a.sa[p], a.sr[p]), (b.mid[q], b.sa[q], b.sr[q]))
        parts.append(seg_pairwise(idx[hit], mid, sa, sr, a.k[p] + b.k[q] + 1, n_out))
    s = tree_sum(parts)
    return s if s is not None else MA.zeros(n_out)


def int_rank(W_int, cols):
    """exact rank of W_int[:, cols] (Fraction elimination; arbeng_c2b_v2's rule)."""
    M = [[Fraction(int(W_int[i][c])) for c in cols] for i in range(len(W_int))]
    rk = 0
    for c in range(len(cols)):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[rk])]
        rk += 1
    return rk


def _arb_of(mid, rad):
    return arb(float(mid)) + arb(0, float(rad))


def _scalar_ball(one):
    """the arb ball of a length-1 MA value: midpoint plus the M-a bound formed in arb (checked finite)."""
    g = arb(gamma_up(int(one.k[0])))
    err = arb(float(one.sr[0])) / (1 - g) - arb(float(one.sa[0])) / (1 + g) + g * arb(float(one.sa[0])) / (1 - g)
    e = up(err)
    ball = arb(float(one.mid[0])) + arb(0, e)
    if not ball.is_finite():
        raise RuntimeError('a non-finite scalar result')
    return ball, e


def _check_W(W, W_int):
    """the exact-zero rule presupposes that the forms W are exactly the integers W_int; ValueError otherwise."""
    if W is None:
        raise ValueError('W_int given without the forms W')
    if W.nrows() != len(W_int) or any(W.ncols() != len(row) for row in W_int):
        raise ValueError('W and W_int differ in shape')
    for i in range(W.nrows()):
        for j in range(W.ncols()):
            w = W[i, j]
            if not (w.is_exact() and w == arb(int(W_int[i][j]))):
                raise ValueError('W[%d, %d] = %s is not the exact integer W_int = %d' % (i, j, w.str(5), int(W_int[i][j])))


class MomTable:
    """K1 + K3: amom2b.AllMom2 in M-a (the minors (-2)^j det(Gam_A) formed in arb as inputs; rank-deficient subsets dropped after their
    det ball is checked to contain 0), with E and E2 returning arb balls. With W_int, W (the forms, arb_mat) is required and checked
    against it exactly (_check_W); Gam = W^T C W is the caller's. plant_scale = (j, i, f): PLANT-MA-INPUT only."""
    def __init__(self, Gam, n, D, groups=None, caps=None, W_int=None, chunk=4000000, plant_scale=None, W=None):
        _check_prec()
        if W_int is not None:
            _check_W(W, W_int)
            if W.ncols() != Gam.nrows():
                raise ValueError('W has %d forms, Gam %d' % (W.ncols(), Gam.nrows()))
        F = Gam.nrows()
        self.F, self.D, self.n, self.chunk = F, D, n, chunk
        self.groups = np.zeros(F, dtype=np.int64) if groups is None else np.asarray(groups, dtype=np.int64)
        self.caps = {} if caps is None else dict(caps)
        B = D + 1
        _code_guard(B, F, 'MomTable')
        self.B = B
        self.pw = np.array([B ** f for f in range(F)], dtype=np.int64)
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            c = np.unique((codes[-1][:, None] + self.pw[None, :]).ravel())
            codes.append(c[self.ok(c)])
        self.codes = codes
        self.zeroed, self.max_zero_rad, self.dropped = 0, 0.0, []
        Dj = [None] * (min(F, D) + 1)
        for j in range(1, min(F, D) + 1):
            cs, mids, rads = [], [], []
            sign = arb(-2) ** j
            for A in itertools.combinations(range(F), j):
                c = int(sum(int(self.pw[f]) for f in A))
                if not self.ok(np.array([c], dtype=np.int64))[0]:
                    continue
                sub = arb_mat(j, j)
                for a_, fa in enumerate(A):
                    for b_, fb in enumerate(A):
                        sub[a_, b_] = Gam[fa, fb]
                d = sub.det()
                if W_int is not None and int_rank(W_int, A) < j:
                    if not d.contains(0):
                        raise ValueError('det of the singular subset %s excludes 0' % (A,))
                    self.zeroed += 1
                    self.max_zero_rad = max(self.max_zero_rad, float(d.rad()))
                    self.dropped.append((A, d))
                    continue
                m, r = ball_to_in(sign * d)
                cs.append(c)
                mids.append(m)
                rads.append(r)
            if plant_scale is not None and plant_scale[0] == j and len(mids) > plant_scale[1]:
                mids[plant_scale[1]] *= plant_scale[2]
            Dj[j] = (np.array(cs, dtype=np.int64), MA.inputs(mids, rads))
        self.Dj = Dj
        if not (float(n) == n):
            raise ValueError('check failed: float(n) == n')
        M = [MA.exact([1.0])] + [None] * D
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            for k in range(1, D + 1):
                nk = len(codes[k])
                terms = []
                for j in range(1, min(k, F) + 1):
                    cj, vj = Dj[j]
                    if len(cj) == 0:
                        continue
                    coef = float(Fraction(2 - n, 2) * j - k)
                    terms.append(scatter_prod(nk, codes[k], cj, vj, codes[k - j], M[k - j], chunk).scale(coef))
                acc = tree_sum(terms)
                M[k] = (acc if acc is not None else MA.zeros(nk)).div_int(k)
                M[k].check('MomTable level %d' % k)
            self.mom = []
            for d in range(D + 1):
                ex = self.decode(codes[d])
                f = [math.prod(math.factorial(int(x)) for x in row) for row in ex]
                fl = np.array([float(x) for x in f])
                kf = np.array([1 if x > 2 ** 53 else 0 for x in f], dtype=np.int64)
                mm = MA(M[d].mid * fl, M[d].sa * fl, M[d].sr * fl, M[d].k + kf + 1)
                mm.check('MomTable moments %d' % d)
                self.mom.append(mm)

    def ok(self, c):
        if not self.caps:
            return np.ones(len(c), dtype=bool)
        ex = self.decode(c)
        good = np.ones(len(c), dtype=bool)
        for g, cap in self.caps.items():
            good &= ex[:, self.groups == g].sum(axis=1) <= cap
        return good

    def decode(self, c):
        return np.stack([(c // self.pw[f]) % self.B for f in range(self.F)], axis=1)

    def index(self, k, cs):
        idx = np.searchsorted(self.codes[k], cs)
        if not (np.all(idx < len(self.codes[k])) and np.array_equal(self.codes[k][idx], cs)):
            raise ValueError('check failed: np.all(idx < len(self.codes[k])) and np.array_equal(self.codes[k][idx], cs)')
        return idx

    def shadow_max(self):
        return max(m.shadow_max() for m in self.mom)

    def _arr(self, P):
        """(degrees, codes, MA coefficients) of P: an SPoly keeps its own shadows and counts; a dict's values enter as inputs."""
        if isinstance(P, SPoly):
            if not (P.nv == self.F):
                raise ValueError('check failed: P.nv == self.F')
            return P.ex.sum(axis=1), P.ex @ self.pw, P.v
        ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, self.F)
        mr = [ball_to_in(to_arb(v)) for v in P.values()]
        return ex.sum(axis=1), ex @ self.pw, MA.inputs([x[0] for x in mr], [x[1] for x in mr])

    def E(self, P, fallback=True):
        """E[P] (amom2b.E, riglap2.expect_np) as an arb ball."""
        if not P:
            return arb(0)
        dg, cs, co = self._arr(P)
        if not (dg.max() <= self.D):
            raise ValueError('check failed: dg.max() <= self.D')
        mids, sas, srs, ks = [], [], [], []
        for d in np.unique(dg):
            sel = np.flatnonzero(dg == d)
            idx = self.index(int(d), cs[sel])
            m = self.mom[int(d)]
            tm, ta, tr = _prod((co.mid[sel], co.sa[sel], co.sr[sel]), (m.mid[idx], m.sa[idx], m.sr[idx]))
            mids.append(tm)
            sas.append(ta)
            srs.append(tr)
            ks.append(co.k[sel] + m.k[idx] + 1)
        one = scalar_sum(np.concatenate(mids), np.concatenate(sas), np.concatenate(srs), np.concatenate(ks))
        ball, err = _scalar_ball(one)
        if fallback and float(one.mid[0]) != 0 and err > FALLBACK_REL * abs(float(one.mid[0])):
            raise MAFallback('E: M-a error %.2e of %.2e' % (err, abs(float(one.mid[0]))))
        return ball

    def E2(self, P, Q, fallback=True):
        """E[P Q] (amom2b.E2) without forming the product, as an arb ball; pairwise over all pairs."""
        dP, cP, aP = self._arr(P)
        dQ, cQ, aQ = self._arr(Q)
        parts = []
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            for d1 in np.unique(dP):
                s1 = np.flatnonzero(dP == d1)
                for d2 in np.unique(dQ):
                    s2 = np.flatnonzero(dQ == d2)
                    kd = int(d1 + d2)
                    if not (kd <= self.D):
                        raise ValueError('check failed: kd <= self.D')
                    mom = self.mom[kd]
                    rows = max(1, self.chunk // len(s2))
                    for s0 in range(0, len(s1), rows):
                        pi = s1[s0:s0 + rows]
                        idx = self.index(kd, (cP[pi][:, None] + cQ[s2][None, :]).ravel())
                        pp = np.repeat(pi, len(s2))
                        qq = np.tile(s2, len(pi))
                        tm, ta, tr = _prod((aP.mid[pp], aP.sa[pp], aP.sr[pp]), (aQ.mid[qq], aQ.sa[qq], aQ.sr[qq]),
                                           (mom.mid[idx], mom.sa[idx], mom.sr[idx]))
                        parts.append(scalar_sum(tm, ta, tr, aP.k[pp] + aQ.k[qq] + mom.k[idx] + 2))
        if not parts:
            return arb(0)
        one = tree_sum(parts)
        one.check('E2')
        ball, err = _scalar_ball(one)
        if fallback and float(one.mid[0]) != 0 and err > FALLBACK_REL * abs(float(one.mid[0])):
            raise MAFallback('E2: M-a error %.2e of %.2e' % (err, abs(float(one.mid[0]))))
        return ball


def allmom2(Gam, n, D, groups=None, caps=None, W_int=None, chunk=4000000, W=None):
    """interface (sect. 6): K1 moment table; with W_int, the forms W are required (_check_W)."""
    return MomTable(Gam, n, D, groups=groups, caps=caps, W_int=W_int, chunk=chunk, W=W)


GV = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
XG = {0: 0, 1: 3, 2: 5}


def mat_in(M):
    r, c = M.nrows(), M.ncols()
    mids, rads = np.zeros((r, c)), np.zeros((r, c))
    for i in range(r):
        for j in range(c):
            mids[i, j], rads[i, j] = ball_to_in(M[i, j])
    sa = np.abs(mids)
    return mids, sa, np.where(rads == 0.0, sa, np.nextafter(sa + rads, np.inf))


class CondTable:
    """K2: condexp2.CondMom in M-a; table self.ent[s-exponent] = (g-exponent rows, MA values) with e! included. P = W^T M and Gam = W^T C W
    are formed in arb and enter as interval inputs; the inner unconditional moments by MomTable with W's exact zeros. W's balls must be
    the exact integers W_int (_check_W). Small contractions (einsum over at most F^2 terms) are counted as sequential sums (n - 1); the
    large sums are pairwise."""
    def __init__(self, Mmat, Cmat, W, W_int, n, Dc, groups=None, caps=None, chunk=4000000):
        _check_prec()
        _check_W(W, W_int)
        F = W.ncols()
        n1 = Mmat.ncols()
        self.F, self.n1, self.Dc, self.n = F, n1, Dc, n
        self.groups = np.zeros(F, dtype=np.int64) if groups is None else np.asarray(groups, dtype=np.int64)
        self.caps = {} if caps is None else dict(caps)
        self.gvars = [(r, s) for r in range(n1) for s in range(r, n1)]
        NG = len(self.gvars)
        self.NG = NG
        nv = F + NG
        B = Dc + 1
        _code_guard(B, nv, 'CondTable')
        self.B = B
        self.pw = np.array([B ** i for i in range(nv)], dtype=np.int64)
        BF = int(self.pw[F])
        Wt = W.transpose()
        Pm, Pa, Pr = mat_in(Wt * Mmat)
        Gm, Ga, Gr = mat_in(Wt * Cmat * W)
        Pmax = float(np.max(Pr)) if Pr.size else 0.0          # the einsum allowance's propagation factor (ADD3 sect. 3)
        self.uf_max = 0.0                                      # the largest einsum allowance added (C-UF)
        self.smax = 0.0                                        # the largest Sr factor met (C-UF, v1_3)
        sc = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            c = np.unique((sc[-1][:, None] + self.pw[None, :F]).ravel())
            sc.append(c[self.s_ok(c)])
        gc = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            gc.append(np.unique((gc[-1][:, None] + self.pw[None, F:]).ravel()))
        gle = [np.unique(np.concatenate(gc[:d + 1])) for d in range(Dc + 1)]
        sup = [np.sort((sc[k][:, None] + gle[k][None, :]).ravel()) for k in range(Dc + 1)]
        sfull = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            sfull.append(np.unique((sfull[-1][:, None] + self.pw[None, :F]).ravel()))
        n1s = len(sfull[1])
        Sm, Sa, Sr = np.zeros((n1s, F, F)), np.zeros((n1s, F, F)), np.zeros((n1s, F, F))
        Sk = np.zeros((n1s, F, F), dtype=np.int64)
        for f in range(F):
            i = int(np.searchsorted(sfull[1], self.pw[f]))
            Sm[i, f, f] = Sa[i, f, f] = Sr[i, f, f] = 1.0
        Y = [None] * (Dc + 1)
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            for k in range(0, Dc):
                d = k + 1
                sc2 = 2.0 ** k
                Smax = float(np.max(Sr)) if Sr.size else 0.0
                nzP = (Pr > 0.0).astype(float)
                cnt = np.einsum('fr,mfg,gs->mrs', nzP, (Sr > 0.0).astype(float), nzP, optimize=False)   # nonzero products per entry
                aY = float(np.nextafter(UF_ALLOW * (1.0 + max(Pmax, Smax)), np.inf))     # v1_3: the first eta may be scaled by P or S
                Xm = sc2 * np.einsum('fr,mfg,gs->mrs', Pm, Sm, Pm, optimize=False)
                Xa = sc2 * np.einsum('fr,mfg,gs->mrs', Pa, Sa, Pa, optimize=False)
                Xr0 = np.einsum('fr,mfg,gs->mrs', Pr, Sr, Pr, optimize=False)
                Xr = sc2 * np.where(cnt > 0.0, np.nextafter(Xr0 + np.nextafter(cnt * aY, np.inf), np.inf), Xr0)   # v1_3: upward
                if cnt.size:
                    self.uf_max = max(self.uf_max, sc2 * float(cnt.max()) * aY)
                    self.smax = max(self.smax, Smax)
                kX = Sk.reshape(len(Sk), -1).max(axis=1) + 2 + (F * F - 1) + 1
                codes, mids, sas, srs, ks, cts = [], [], [], [], [], []
                for gi, (r, s) in enumerate(self.gvars):
                    if r == s:
                        vm, va, vr, vk, vc = Xm[:, r, r], Xa[:, r, r], Xr[:, r, r], kX, cnt[:, r, r]
                    else:
                        vm, va, vr, vk = Xm[:, r, s] + Xm[:, s, r], Xa[:, r, s] + Xa[:, s, r], Xr[:, r, s] + Xr[:, s, r], kX + 1
                        vc = cnt[:, r, s] + cnt[:, s, r]
                    codes.append(sfull[d] + self.pw[F + gi])
                    mids.append(vm)
                    sas.append(va)
                    srs.append(vr)
                    ks.append(vk)
                    cts.append(vc)
                codes = np.concatenate(codes)
                mids, sas, srs, ks, cts = (np.concatenate(x) for x in (mids, sas, srs, ks, cts))
                mids, sas, srs = _tiny_rule(mids, sas, srs, cts == 0.0)
                keep = ((mids != 0.0) | (sas != 0.0) | (srs != 0.0)) & self.s_ok(codes % BF)
                Y[d] = (codes[keep], MA(mids[keep], sas[keep], srs[keep], ks[keep]))
                if d < Dc:
                    cGS = np.einsum('fh,mhg->mfg', (Gr > 0.0).astype(float), (Sr > 0.0).astype(float), optimize=False)
                    if cGS.size:
                        self.uf_max = max(self.uf_max, float(cGS.max()) * UF_ALLOW)
                    GSr0 = np.einsum('fh,mhg->mfg', Gr, Sr, optimize=False)
                    GSr1 = np.where(cGS > 0.0, np.nextafter(GSr0 + np.nextafter(cGS * UF_ALLOW, np.inf), np.inf), GSr0)   # v1_3
                    GSm, GSa, GSr = _tiny_rule(np.einsum('fh,mhg->mfg', Gm, Sm, optimize=False),
                                               np.einsum('fh,mhg->mfg', Ga, Sa, optimize=False), GSr1, cGS == 0.0)
                    kGS = np.broadcast_to(Sk.max(axis=1)[:, None, :] + 1 + (F - 1), GSm.shape)
                    nn_ = len(sfull[d + 1])
                    Nm, Na, Nr = np.zeros((nn_, F, F)), np.zeros((nn_, F, F)), np.zeros((nn_, F, F))
                    Nk = np.zeros((nn_, F, F), dtype=np.int64)
                    for f in range(F):
                        idx = np.searchsorted(sfull[d + 1], sfull[d] + self.pw[f])
                        if not (len(np.unique(idx)) == len(idx)):
                            raise ValueError('check failed: len(np.unique(idx)) == len(idx)')
                        Nm[idx, f, :] += GSm[:, f, :]
                        Na[idx, f, :] += GSa[:, f, :]
                        Nr[idx, f, :] += GSr[:, f, :]
                        Nk[idx, f, :] = np.maximum(Nk[idx, f, :], kGS[:, f, :])
                    Sm, Sa, Sr, Sk = Nm, Na, Nr, Nk
            E = [MA.exact([1.0])]
            for k in range(1, Dc + 1):
                terms = []
                for j in range(1, k + 1):
                    cj, vj = Y[j]
                    if len(cj) == 0:
                        continue
                    terms.append(scatter_prod(len(sup[k]), sup[k], cj, vj.scale(float(j)), sup[k - j], E[k - j], chunk))
                acc = tree_sum(terms)
                E.append((acc if acc is not None else MA.zeros(len(sup[k]))).div_int(k))
                E[-1].check('CondTable E %d' % k)
        self.am = MomTable(Wt * Cmat * W, n, Dc, groups=self.groups, caps=self.caps, W_int=W_int, chunk=chunk, W=W)
        am = self.am
        Mser = []
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            for k in range(Dc + 1):
                terms = []
                for j in range(0, k + 1):
                    cj = am.codes[j]
                    fe = np.array([math.prod(math.factorial(int(x)) for x in row) for row in am.decode(cj)], dtype=np.int64)
                    vj = am.mom[j].div_int(fe)
                    terms.append(scatter_prod(len(sup[k]), sup[k], cj, vj, sup[k - j], E[k - j], chunk))
                acc = tree_sum(terms)
                Mser.append(acc if acc is not None else MA.zeros(len(sup[k])))
                Mser[-1].check('CondTable Mser %d' % k)
        self.ent = {}
        for k in range(Dc + 1):
            u, v = sup[k], Mser[k]
            nz = np.flatnonzero(v.present())
            u, v = u[nz], v.take(nz)
            spart, gpart = u % BF, u // BF
            order = np.argsort(spart, kind='stable')
            spart, gpart, v = spart[order], gpart[order], v.take(order)
            if len(spart) == 0:
                continue
            bounds = np.flatnonzero(np.diff(spart)) + 1
            starts = np.concatenate([[0], bounds])
            ends = np.concatenate([bounds, [len(spart)]])
            for a0, a1 in zip(starts, ends):
                e = tuple(int(x) for x in self.decode_s(int(spart[a0])))
                ef = math.prod(math.factorial(x) for x in e)
                if not (ef <= 2 ** 53):
                    raise ValueError('check failed: ef <= 2 ** 53')
                vv = v.take(np.arange(a0, a1))
                self.ent[e] = (self.decode_g_arr(gpart[a0:a1]), MA(vv.mid * ef, vv.sa * ef, vv.sr * ef, vv.k + 1))
        self.entries = sum(len(x[0]) for x in self.ent.values())

    def s_ok(self, c):
        if not self.caps:
            return np.ones(len(c), dtype=bool)
        ex = np.stack([(c // self.pw[f]) % self.B for f in range(self.F)], axis=1)
        good = np.ones(len(c), dtype=bool)
        for g, cap in self.caps.items():
            good &= ex[:, self.groups == g].sum(axis=1) <= cap
        return good

    def decode_s(self, c):
        return [(c // self.B ** f) % self.B for f in range(self.F)]

    def decode_g_arr(self, cs):
        return np.stack([(cs // self.B ** j) % self.B for j in range(self.NG)], axis=1)

    def shadow_max(self):
        return max([v.shadow_max() for _, v in self.ent.values()] + [0.0])

    def condE(self, P12, Dout, batch=4000000):
        """condg.CondG.condE in M-a: {12-tuple: arb} -> {g-exponent: arb} over the g-monomials of total degree <= Dout. Terms c v are one
        rounding each; contributions are collected in batches, summed pairwise per output monomial, and the batches tree-summed."""
        Bo = Dout + 1
        _code_guard(Bo, 6, 'condE')
        pw = np.array([Bo ** i for i in range(6)], dtype=np.int64)
        gl = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dout + 1):
            gl.append(np.unique((gl[-1][:, None] + pw[None, :]).ravel()))
        oc = np.unique(np.concatenate(gl))
        n_out = len(oc)
        one = (np.zeros((1, 6), dtype=np.int64), MA.exact([1.0]))
        parts, buf, nbuf = [], [], 0

        def flush():
            if not buf:
                return
            dst = np.concatenate([x[0] for x in buf])
            parts.append(seg_pairwise(dst, np.concatenate([x[1] for x in buf]), np.concatenate([x[2] for x in buf]),
                                      np.concatenate([x[3] for x in buf]), np.concatenate([x[4] for x in buf]), n_out))
            buf.clear()
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            for e, c in P12.items():
                if not (e[3] == e[4] == e[5] == 0):
                    raise ValueError('sigma Q-forms not expected')
                eg = np.zeros(6, dtype=np.int64)
                for r in range(3):
                    eg[XG[r]] = e[r]
                e2 = tuple(e[6:])
                gd, v = one if sum(e2) == 0 else self.ent.get(e2, (None, None))
                if gd is None:
                    raise KeyError(e2)
                rows = gd + eg[None, :]
                keep = np.flatnonzero(rows.sum(axis=1) <= Dout)
                if len(keep) == 0:
                    continue
                codes = rows[keep] @ pw
                dst = np.searchsorted(oc, codes)
                if not (np.array_equal(oc[dst], codes)):
                    raise ValueError('check failed: np.array_equal(oc[dst], codes)')
                cm_, cr = ball_to_in(c)
                ca = abs(cm_)
                crr = ca if cr == 0.0 else float(np.nextafter(ca + cr, np.inf))
                if crr == 0.0:
                    continue
                vv = v.take(keep)
                nk = len(keep)
                tm, ta, tr = _prod((np.full(nk, cm_), np.full(nk, ca), np.full(nk, crr)), (vv.mid, vv.sa, vv.sr))
                buf.append((dst, tm, ta, tr, vv.k + 1))
                nbuf += len(dst)
                if nbuf >= batch:
                    flush()
                    nbuf = 0
            flush()
        acc = tree_sum(parts)
        if acc is None:
            return {}, 0
        acc.check('condE')
        rad = acc.radius()
        ex = np.stack([(oc // pw[i]) % Bo for i in range(6)], axis=1)
        out = {}
        for i in np.flatnonzero(acc.present()):
            out[tuple(int(x) for x in ex[i])] = _arb_of(acc.mid[i], rad[i])
        return out, int(acc.k.max())


def condmom(Mmat, Cmat, W, W_int, n, Dc, groups=None, caps=None, chunk=4000000):
    """interface (sect. 6): K2 conditional-moment table."""
    return CondTable(Mmat, Cmat, W, W_int, n, Dc, groups=groups, caps=caps, chunk=chunk)


def npoly_mul(P, Q, keep=None):
    """K4: P Q for polynomials {exponent tuple: arb}; keep(exponent array) -> bool array truncates (a ring quotient: degree or caps).
    Each coefficient of the product is a pairwise sum of coefficient products (one rounding each). Returns {exponent tuple: arb}."""
    _check_prec()
    if not P or not Q:
        return {}
    eP = np.array(list(P.keys()), dtype=np.int64)
    eQ = np.array(list(Q.keys()), dtype=np.int64)
    nv = eP.shape[1]
    if not (eQ.shape[1] == nv):
        raise ValueError('check failed: eQ.shape[1] == nv')
    mP = [ball_to_in(v) for v in P.values()]
    mQ = [ball_to_in(v) for v in Q.values()]
    aP = MA.inputs([x[0] for x in mP], [x[1] for x in mP])
    aQ = MA.inputs([x[0] for x in mQ], [x[1] for x in mQ])
    B = int(max(eP.max(), 0) + max(eQ.max(), 0) + 1)
    _code_guard(B, nv, 'npoly_mul')
    pw = np.array([B ** i for i in range(nv)], dtype=np.int64)
    pp = np.repeat(np.arange(len(eP)), len(eQ))
    qq = np.tile(np.arange(len(eQ)), len(eP))
    ex = eP[pp] + eQ[qq]
    if keep is not None:
        sel = np.flatnonzero(keep(ex))
        pp, qq, ex = pp[sel], qq[sel], ex[sel]
    if len(pp) == 0:
        return {}
    cs = ex @ pw
    uc, dst = np.unique(cs, return_inverse=True)
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        tm, ta, tr = _prod((aP.mid[pp], aP.sa[pp], aP.sr[pp]), (aQ.mid[qq], aQ.sa[qq], aQ.sr[qq]))
        acc = seg_pairwise(dst, tm, ta, tr, aP.k[pp] + aQ.k[qq] + 1, len(uc))
    acc.check('npoly_mul')
    rad = acc.radius()
    uex = np.stack([(uc // pw[i]) % B for i in range(nv)], axis=1)
    return {tuple(int(x) for x in uex[i]): _arb_of(acc.mid[i], rad[i]) for i in range(len(uc)) if acc.present()[i]}


def npoly_pow(P, k, keep=None):
    """K4: P^k by repeated npoly_mul (each product's balls feed the next as inputs)."""
    if not (k >= 1):
        raise ValueError('check failed: k >= 1')
    out = P
    for _ in range(k - 1):
        out = npoly_mul(out, P, keep)
    return out


def _root_ball(x, p):
    """x^(1/p) for an arb ball x enclosing a nonnegative quantity, in arb: exp(log(x)/p) when x's lower end
    is positive; for a ball touching 0 the monotone endpoint form [0, (upper end)^(1/p)], the root of the upper end rounded up; a ball
    entirely below 0 is an error. Checked finite."""
    if not x.is_finite():
        raise RuntimeError('a non-finite ball under a root')
    if x.lower() > 0:
        r = (x.log() / p).exp()
    else:
        hi = x.upper()
        if hi < 0:
            raise RuntimeError('a negative ball for a nonnegative quantity')
        if hi == 0:
            return arb(0)
        hu = up((hi.log() / p).exp())
        r = arb(hu) / 2 + arb(0, up(arb(hu) / 2))
    if not r.is_finite():
        raise RuntimeError('a non-finite root')
    return r


def lp_norm(table, P, p):
    """K5: (E|P|^p)^(1/p), p even (riglap4.lp_norm): E2 of P^(p/2) by K4/K3, the root in arb (_root_ball)."""
    _check_prec()
    if not (p % 2 == 0 and p >= 2):
        raise ValueError('lp_norm needs an even p >= 2')
    if not P:
        return arb(0)
    Pk = npoly_pow(P, p // 2)
    return _root_ball(table.E2(Pk, Pk), p)


def pos_norm(table, P, p):
    """K5: (E[P^p])^(1/p) for a pointwise-nonnegative polynomial P (riglap4.pos_norm), the root in arb (_root_ball)."""
    _check_prec()
    if not (p >= 1):
        raise ValueError('pos_norm needs p >= 1')
    if not P:
        return arb(0)
    Pk = npoly_pow(P, p)
    return _root_ball(table.E(Pk), p)


# ---------------------------------------------------------------------------- pk03's interface (PLAN_M3_CODE_v1 sect. 2a)
def mpi_to_arb(x):
    """an mp.iv interval as an arb ball containing it. Each endpoint is mpmath's raw tuple (sign, man, exp, bc), whose value is
    (-1)^sign man 2^exp exactly (arbeng_ma_v1_1: the sign is read from the tuple; libmp.to_man_exp returns the unsigned mantissa, which
    arbeng_ma_v1 and the stub used, so a negative endpoint turned positive). mpmath's special values (infinities, nan) have man = 0 and
    exp != 0: MAFallback."""
    ends = []
    for t in x._mpi_:
        sign, man, exp, bc = t
        if not man and exp:
            raise MAFallback('an infinite or nan mp.iv endpoint')
        ends.append(arb(-int(man) if sign else int(man)) * arb(2) ** int(exp))
    return ends[0].union(ends[1])


def arb_to_mpi(x):
    """an arb ball as an mp.iv interval containing it (python-flint's man_exp of the midpoint is signed; mp.iv rounds outward)."""
    if not x.is_finite():
        raise MAFallback('a non-finite ball at conversion to mp.iv')
    mm, me = x.mid().man_exp()
    rm, rexp = x.rad().man_exp()
    return iv.mpf(int(mm)) * iv.mpf(2) ** int(me) + (iv.mpf(int(rm)) * iv.mpf(2) ** int(rexp)) * iv.mpf([-1, 1])


def to_arb(v):
    """a coefficient as an arb ball: (mid, rad) floats, mp.iv, arb, Fraction, int or float."""
    if isinstance(v, arb):
        return v
    if isinstance(v, tuple):
        return arb(float(v[0])) + arb(0, float(v[1]))
    if isinstance(v, Fraction):
        return arb(v.numerator) / v.denominator
    if isinstance(v, (int, np.integer)):
        return arb(int(v))
    if isinstance(v, float):
        return arb(float(v))
    if hasattr(v, '_mpi_'):
        return mpi_to_arb(v)
    raise TypeError('coefficient type %r' % type(v))


class SPoly:
    """the kernel polynomial type in M-a: exponents ex (m x nv int64) and coefficients v (MA). Shadows at |x_mid| and at the N1 point and
    the rounding counts are carried through add, sub, scale, div_int, mul and power; a coefficient is dropped only when its value and both
    shadows are 0. Products and merges are pairwise per monomial."""
    def __init__(self, nv, ex=None, v=None):
        self.nv = nv
        if ex is None:
            ex, v = np.zeros((0, nv), dtype=np.int64), MA.zeros(0)
        keep = np.flatnonzero((v.mid != 0.0) | (v.sa != 0.0) | (v.sr != 0.0))
        self.ex, self.v = ex[keep], v.take(keep)

    @classmethod
    def from_dict(cls, P, nv=None):
        if nv is None:
            nv = len(next(iter(P))) if P else 0
        if not P:
            return cls(nv)
        ex = np.array([tuple(int(x) for x in e) for e in P.keys()], dtype=np.int64).reshape(-1, nv)
        mr = [ball_to_in(to_arb(c)) for c in P.values()]
        return cls(nv, *_merge(ex, MA.inputs([x[0] for x in mr], [x[1] for x in mr])))

    def _base(self, *others):
        mx = max([int(self.ex.max()) if len(self.ex) else 0] + [int(o.ex.max()) if len(o.ex) else 0 for o in others])
        return mx

    @property
    def codes(self):
        B = (int(self.ex.max()) + 1) if len(self.ex) else 1
        _code_guard(B, self.nv, 'SPoly.codes')
        return self.ex @ np.array([B ** i for i in range(self.nv)], dtype=np.int64)

    mid = property(lambda self: self.v.mid)
    sa = property(lambda self: self.v.sa)
    sr = property(lambda self: self.v.sr)
    k = property(lambda self: self.v.k)

    def to_arb_dict(self):
        rad = self.v.radius()
        return {tuple(int(x) for x in self.ex[i]): _arb_of(self.v.mid[i], rad[i]) for i in range(len(self.ex))}

    def to_dict(self):
        return {e: arb_to_mpi(c) for e, c in self.to_arb_dict().items()}

    def add(self, Q):
        if not (Q.nv == self.nv):
            raise ValueError('check failed: Q.nv == self.nv')
        ex = np.concatenate([self.ex, Q.ex])
        v = MA(np.concatenate([self.v.mid, Q.v.mid]), np.concatenate([self.v.sa, Q.v.sa]), np.concatenate([self.v.sr, Q.v.sr]),
               np.concatenate([self.v.k, Q.v.k]))
        return SPoly(self.nv, *_merge(ex, v))

    def sub(self, Q):
        return self.add(Q.scale(-1))

    __add__, __sub__ = add, sub

    def scale(self, c):
        """times c: an exact binary64 or integer (one rounding), or an interval (an input with its own shadows)."""
        if isinstance(c, (int, np.integer)) and abs(int(c)) <= 2 ** 53 or isinstance(c, float):
            return SPoly(self.nv, self.ex, self.v.scale(float(c)))
        cm, cr = ball_to_in(to_arb(c))
        ca = abs(cm)
        crr = ca if cr == 0.0 else float(np.nextafter(ca + cr, np.inf))
        n = len(self.ex)
        tm, ta, tr = _prod((self.v.mid, self.v.sa, self.v.sr), (np.full(n, cm), np.full(n, ca), np.full(n, crr)))
        return SPoly(self.nv, self.ex, MA(tm, ta, tr, self.v.k + 1))

    def div_int(self, n):
        if not (isinstance(n, (int, np.integer)) and 0 < abs(int(n)) <= 2 ** 53):
            raise ValueError('check failed: isinstance(n, (int, np.integer)) and 0 < abs(int(n)) <= 2 ** 53')
        n = int(n)
        v = self.v.div_int(abs(n))
        return SPoly(self.nv, self.ex, v if n > 0 else MA(-v.mid, v.sa, v.sr, v.k))

    def mul(self, Q, keep=None):
        if not (Q.nv == self.nv):
            raise ValueError('check failed: Q.nv == self.nv')
        if len(self.ex) == 0 or len(Q.ex) == 0:
            return SPoly(self.nv)
        pp = np.repeat(np.arange(len(self.ex)), len(Q.ex))
        qq = np.tile(np.arange(len(Q.ex)), len(self.ex))
        ex = self.ex[pp] + Q.ex[qq]
        if keep is not None:
            sel = np.flatnonzero(keep(ex))
            pp, qq, ex = pp[sel], qq[sel], ex[sel]
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            tm, ta, tr = _prod((self.v.mid[pp], self.v.sa[pp], self.v.sr[pp]), (Q.v.mid[qq], Q.v.sa[qq], Q.v.sr[qq]))
            v = MA(tm, ta, tr, self.v.k[pp] + Q.v.k[qq] + 1)
        return SPoly(self.nv, *_merge(ex, v))

    def power(self, k, keep=None):
        if not (k >= 1):
            raise ValueError('check failed: k >= 1')
        out = self
        for _ in range(k - 1):
            out = out.mul(self, keep)
        return out


def _merge(ex, v):
    """sum the coefficients of equal exponents pairwise; returns (unique exponents, MA)."""
    if len(ex) == 0:
        return ex, v
    B = int(ex.max()) + 1
    nv = ex.shape[1]
    _code_guard(B, nv, '_merge')
    codes = ex @ np.array([B ** i for i in range(nv)], dtype=np.int64)
    uc, dst = np.unique(codes, return_inverse=True)
    s = seg_pairwise(dst, v.mid, v.sa, v.sr, v.k, len(uc))
    uex = np.stack([(uc // B ** i) % B for i in range(nv)], axis=1)
    return uex, s


class AllMom2(MomTable):
    """pk03's interface: Gam as an F x F list of mp.iv (or an arb_mat), E and E2 out as mp.iv enclosures; with W_int, the forms W
    (arb_mat, or an integer list of lists) are required and checked against it exactly."""
    def __init__(self, Gam, n, D, groups=None, caps=None, W_int=None, chunk=4000000, W=None):
        if not isinstance(Gam, arb_mat):
            F = len(Gam)
            G = arb_mat(F, F)
            for i in range(F):
                for j in range(F):
                    G[i, j] = to_arb(Gam[i][j])
            Gam = G
        if W is not None and not isinstance(W, arb_mat):
            Wm = arb_mat(len(W), len(W[0]))
            for i in range(len(W)):
                for j in range(len(W[0])):
                    Wm[i, j] = to_arb(W[i][j])
            W = Wm
        MomTable.__init__(self, Gam, n, D, groups=groups, caps=caps, W_int=W_int, chunk=chunk, W=W)

    def E(self, P, fallback=True):
        return arb_to_mpi(MomTable.E(self, P, fallback))

    def E2(self, P, Q, fallback=True):
        return arb_to_mpi(MomTable.E2(self, P, Q, fallback))


def lp_moment(table, P, p):
    """E[P^(p/2) P^(p/2)], p even, as table.E2 returns it (mp.iv for AllMom2)."""
    if not (p % 2 == 0 and p >= 2):
        raise ValueError('check failed: p % 2 == 0 and p >= 2')
    P = P if isinstance(P, SPoly) else SPoly.from_dict(P)
    Pk = P.power(p // 2)
    return table.E2(Pk, Pk)


def pos_moment(table, P, p):
    """E[P^p] for a pointwise-nonnegative P, as table.E returns it."""
    if not (p >= 1):
        raise ValueError('check failed: p >= 1')
    P = P if isinstance(P, SPoly) else SPoly.from_dict(P)
    return table.E(P.power(p))


# ---------------------------------------------------------------------------- arbeng_ma_v1_4 (DESIGN_ARBENG_MA_v1_4): unit-built tables, blocked E2
import hashlib, json, time


def _sha_file(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


KERNEL_SHA = _sha_file(os.path.abspath(__file__))
BLOCK = 50000                  # destinations per block of a level (MomTableU): about 1e7 terms, 1.3 GB peak, at level 16 of D16 F12


def scalar_sum_fast(mid, sa, sr, k):
    """v1_4: seg_pairwise's single-segment case without the sort and the index bookkeeping. Level by level the pairs (2i, 2i + 1) are added
    with count max + 1 and an odd last element is carried: the same pairs in the same order as seg_pairwise with one destination, hence
    bit-identical to scalar_sum (C-FASTSUM). Returns an MA of length 1."""
    m = np.array(mid, dtype=float)
    a = np.array(sa, dtype=float)
    r = np.array(sr, dtype=float)
    kk = np.array(k, dtype=np.int64)
    if len(m) == 0:
        return MA.zeros(1)
    while len(m) > 1:
        h = len(m) // 2
        m2 = m[0:2 * h:2] + m[1:2 * h:2]
        a2 = a[0:2 * h:2] + a[1:2 * h:2]
        r2 = r[0:2 * h:2] + r[1:2 * h:2]
        k2 = np.maximum(kk[0:2 * h:2], kk[1:2 * h:2]) + 1
        if len(m) % 2:
            m2, a2, r2, k2 = np.append(m2, m[-1]), np.append(a2, a[-1]), np.append(r2, r[-1]), np.append(k2, kk[-1])
        m, a, r, kk = m2, a2, r2, k2
    return MA(m, a, r, kk)


def ma_scalar_dump(x):
    """v1_4: a length-1 MA as a lossless dict (float hex, int count), for a caller's memo."""
    return {'mid': float(x.mid[0]).hex(), 'sa': float(x.sa[0]).hex(), 'sr': float(x.sr[0]).hex(), 'k': int(x.k[0])}


def ma_scalar_load(d):
    """v1_4: the inverse of ma_scalar_dump; checks the shadow order."""
    x = MA(np.array([float.fromhex(d['mid'])]), np.array([float.fromhex(d['sa'])]), np.array([float.fromhex(d['sr'])]),
           np.array([int(d['k'])], dtype=np.int64))
    x.check('ma_scalar_load')
    return x


def E2_plan(table, P, Q, max_pairs):
    """v1_4: blocks of P's terms for E2_block. The order is v1_3's E2 order (by degree, then the term's own index within P), cut into
    contiguous blocks whose pair counts (each P term against every Q term) stay at or below max_pairs; a single term is never split.
    Returns {'blocks': [(start, end), ...], 'order': index array, 'pairs': total}."""
    dP, cP, aP = table._arr(P)
    dQ, cQ, aQ = table._arr(Q)
    order = np.concatenate([np.flatnonzero(dP == d1) for d1 in np.unique(dP)]) if len(dP) else np.zeros(0, dtype=np.int64)
    per = len(cQ)
    if per == 0 or len(order) == 0:
        return {'blocks': [], 'order': order, 'pairs': 0}
    rows = max(1, int(max_pairs) // per)
    blocks = [(s, min(s + rows, len(order))) for s in range(0, len(order), rows)]
    E2_check_plan(table, P, Q, {'blocks': blocks, 'order': order})
    return {'blocks': blocks, 'order': order, 'pairs': per * len(order)}


def E2_check_plan(table, P, Q, plan):
    """v1_4: the blocks' P ranges partition P (contiguous, no gap, no overlap, every term once) and the order is the
    deterministic one E2_plan builds; ValueError otherwise."""
    dP, cP, aP = table._arr(P)
    want = np.concatenate([np.flatnonzero(dP == d1) for d1 in np.unique(dP)]) if len(dP) else np.zeros(0, dtype=np.int64)
    if not np.array_equal(np.asarray(plan['order']), want):
        raise ValueError('E2 plan: the order is not E2_plan\'s')
    pos = 0
    for s, e in plan['blocks']:
        if s != pos or not (e > s):
            raise ValueError('E2 plan: the blocks do not partition P')
        pos = e
    if pos != len(want):
        raise ValueError('E2 plan: the blocks do not cover P')


def E2_block(table, P, Q, plan, b):
    """v1_4: v1_3's E2 loop (MomTable.E2) restricted to the P terms of block b of plan; returns the block's sum as an MA of length 1, before
    any ball or fallback test (E2_combine does both once). A one-block plan reproduces v1_3's E2 sum exactly (same parts, same trees;
    scalar_sum_fast is bit-identical to scalar_sum)."""
    E2_check_plan(table, P, Q, plan)
    dP, cP, aP = table._arr(P)
    dQ, cQ, aQ = table._arr(Q)
    s0, s1_ = plan['blocks'][b]
    inblock = np.zeros(len(dP), dtype=bool)
    inblock[plan['order'][s0:s1_]] = True
    parts = []
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        for d1 in np.unique(dP):
            s1 = np.flatnonzero((dP == d1) & inblock)
            if len(s1) == 0:
                continue
            for d2 in np.unique(dQ):
                s2 = np.flatnonzero(dQ == d2)
                kd = int(d1 + d2)
                if not (kd <= table.D):
                    raise ValueError('check failed: kd <= table.D')
                mom = table.mom[kd]
                rows = max(1, table.chunk // len(s2))
                for st in range(0, len(s1), rows):
                    pi = s1[st:st + rows]
                    idx = table.index(kd, (cP[pi][:, None] + cQ[s2][None, :]).ravel())
                    pp = np.repeat(pi, len(s2))
                    qq = np.tile(s2, len(pi))
                    tm, ta, tr = _prod((aP.mid[pp], aP.sa[pp], aP.sr[pp]), (aQ.mid[qq], aQ.sa[qq], aQ.sr[qq]),
                                       (mom.mid[idx], mom.sa[idx], mom.sr[idx]))
                    parts.append(scalar_sum_fast(tm, ta, tr, aP.k[pp] + aQ.k[qq] + mom.k[idx] + 2))
    one = tree_sum(parts)
    if one is None:
        return MA.zeros(1)
    one.check('E2_block')
    _scalar_ball(one)                   # the block's validity (finite, in binary64's range); no relative-error test here
    return one


def E2_combine(parts, plan=None):
    """v1_4: the blocks' sums (MA scalars, in block order; with plan, one per block of it) by tree_sum with tracked counts, then MA.check,
    the ball and the MAFallback test once, on the total (a single block may cancel). Returns the arb ball, as v1_3's E2."""
    if plan is not None and len(parts) != len(plan['blocks']):
        raise ValueError('E2_combine: %d parts for %d blocks' % (len(parts), len(plan['blocks'])))
    if not parts:
        return arb(0)
    one = tree_sum(list(parts))
    one.check('E2')
    ball, err = _scalar_ball(one)
    if float(one.mid[0]) != 0 and err > FALLBACK_REL * abs(float(one.mid[0])):
        raise MAFallback('E2: M-a error %.2e of %.2e' % (err, abs(float(one.mid[0]))))
    return ball


def _arb_exact_str(x):
    """the exact (mid, rad) of an arb ball as integer mantissa/exponent pairs (for the parameter hash)."""
    m, e = x.mid().man_exp()
    rm, re_ = x.rad().man_exp()
    return '%d,%d,%d,%d' % (int(m), int(e), int(rm), int(re_))


class MomTableView(MomTable):
    """v1_4: a read-only MomTable built from MomTableU's verified files (MomTableU.load); E, E2, index, _arr and shadow_max are MomTable's."""
    def __init__(self, F, D, n, groups, caps, B, pw, codes, mom, chunk=4000000):
        self.F, self.D, self.n, self.chunk = F, D, n, chunk
        self.groups, self.caps, self.B, self.pw = groups, caps, B, pw
        self.codes, self.mom = codes, mom
        self.zeroed, self.max_zero_rad, self.dropped = None, None, None


class MomTableU(MomTable):
    """v1_4 (DESIGN_ARBENG_MA_v1_4 sect. 1-2): MomTable's recursion in destination code blocks, built in resumable units with verified state.
    Only ok, decode and index are used from MomTable (its __init__ is not called). Usage: U = MomTableU(Gam, n, D, ...); U.start(dir);
    for unit in U.plan(dir, unit_pairs): U.run_unit(dir, unit); U.finish(dir); then MomTableU.load(dir, Gam, n, D, ...) or U.load_view(dir)."""
    def __init__(self, Gam, n, D, groups=None, caps=None, W_int=None, W=None, block=BLOCK, chunk=4000000):
        _check_prec()
        if W_int is not None:
            _check_W(W, W_int)
            if W.ncols() != Gam.nrows():
                raise ValueError('W has %d forms, Gam %d' % (W.ncols(), Gam.nrows()))
        if not (float(n) == n):
            raise ValueError('check failed: float(n) == n')
        F = Gam.nrows()
        self.F, self.D, self.n, self.chunk, self.block = F, D, n, chunk, int(block)
        self.groups = np.zeros(F, dtype=np.int64) if groups is None else np.asarray(groups, dtype=np.int64)
        self.caps = {} if caps is None else dict(caps)
        self.Gam, self.W_int, self.W = Gam, W_int, W
        B = D + 1
        _code_guard(B, F, 'MomTableU')
        self.B = B
        self.pw = np.array([B ** f for f in range(F)], dtype=np.int64)
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            c = np.unique((codes[-1][:, None] + self.pw[None, :]).ravel())
            codes.append(c[self.ok(c)])
        self.codes = codes
        self.codes_sha = [hashlib.sha256(c.tobytes()).hexdigest() for c in codes]
        self.hpar = self._hpar()

    def _hpar(self):
        """H_par: sha256 over the exact Gam entries, n, D, F, groups, caps, W_int, the block size, VERSION and the kernel's sha256."""
        F = self.F
        parts = ['arbeng_ma_v1_4 MomTableU', 'VERSION=%s' % VERSION, 'KERNEL=%s' % KERNEL_SHA, 'F=%d' % F, 'D=%d' % self.D,
                 'n=%s' % Fraction(self.n), 'groups=%s' % ','.join(str(int(g)) for g in self.groups),
                 'caps=%s' % ';'.join('%d:%d' % (int(g), int(c)) for g, c in sorted(self.caps.items())), 'block=%d' % self.block,
                 'Gam=' + ';'.join(_arb_exact_str(self.Gam[i, j]) for i in range(F) for j in range(F))]
        if self.W_int is not None:
            parts.append('W_int=' + ';'.join(','.join(str(int(x)) for x in row) for row in np.asarray(self.W_int)))
        return hashlib.sha256('|'.join(parts).encode()).hexdigest()

    # ----- the minors (v1_3's MomTable loop, l.431-457, unchanged in substance)
    def minors(self):
        F, D = self.F, self.D
        zeroed, max_zero_rad, dropped = 0, 0.0, []
        Dj = [None] * (min(F, D) + 1)
        for j in range(1, min(F, D) + 1):
            cs, mids, rads = [], [], []
            sign = arb(-2) ** j
            for A in itertools.combinations(range(F), j):
                c = int(sum(int(self.pw[f]) for f in A))
                if not self.ok(np.array([c], dtype=np.int64))[0]:
                    continue
                sub = arb_mat(j, j)
                for a_, fa in enumerate(A):
                    for b_, fb in enumerate(A):
                        sub[a_, b_] = self.Gam[fa, fb]
                d = sub.det()
                if self.W_int is not None and int_rank(self.W_int, A) < j:
                    if not d.contains(0):
                        raise ValueError('det of the singular subset %s excludes 0' % (A,))
                    zeroed += 1
                    max_zero_rad = max(max_zero_rad, float(d.rad()))
                    dropped.append(A)
                    continue
                m, r = ball_to_in(sign * d)
                cs.append(c)
                mids.append(m)
                rads.append(r)
            Dj[j] = (np.array(cs, dtype=np.int64), MA.inputs(mids, rads))
        return Dj, zeroed, max_zero_rad, dropped

    # ----- files and hand-offs (atomic writes, a temporary name then a rename, the hand-off JSON last)
    @staticmethod
    def _atomic(path, write):
        if os.path.exists(path):
            raise ValueError('C-STATE: %s exists; a state file is never overwritten' % os.path.basename(path))
        tmp = '%s.tmp.%d.%d' % (path, os.getpid(), time.time_ns())
        with open(tmp, 'xb') as fh:
            write(fh)
            fh.flush()
            os.fsync(fh.fileno())
        if os.path.exists(path):
            raise ValueError('C-STATE: %s appeared during the write' % os.path.basename(path))
        os.rename(tmp, path)

    @staticmethod
    def _write_npz(path, arrays):
        MomTableU._atomic(path, lambda fh: np.savez(fh, **arrays))
        return {'size': os.path.getsize(path), 'sha256': _sha_file(path)}

    @staticmethod
    def _write_json(path, obj):
        MomTableU._atomic(path, lambda fh: fh.write(json.dumps(obj, sort_keys=True, indent=1).encode()))
        return _sha_file(path)

    def _read_handoff(self, path):
        with open(path) as fh:
            h = json.load(fh)
        if h.get('hpar') != self.hpar:
            raise ValueError('C-STATE: %s carries another parameter hash' % os.path.basename(path))
        return h

    @staticmethod
    def _read_npz(state_dir, name, entry):
        path = os.path.join(state_dir, name)
        if not (os.path.getsize(path) == entry['size'] and _sha_file(path) == entry['sha256']):
            raise ValueError('C-STATE: %s differs from its hand-off (size or sha256)' % name)
        with np.load(path, allow_pickle=False) as z:
            return dict((k, z[k]) for k in z.files)

    @staticmethod
    def _ma(arrs, prefix=''):
        x = MA(arrs[prefix + 'mid'].astype(float), arrs[prefix + 'sa'].astype(float), arrs[prefix + 'sr'].astype(float),
               arrs[prefix + 'k'].astype(np.int64))
        x.check('MomTableU file')
        return x

    def nblocks(self, k):
        return -(-len(self.codes[k]) // self.block)

    def start(self, state_dir):
        """state 0: the minors D_j (raw MA fields per j) and the hand-off with H_par and the code hashes."""
        Dj, zeroed, mzr, dropped = self.minors()
        arrays = {}
        for j in range(1, len(Dj)):
            cj, vj = Dj[j]
            arrays.update({'c%d' % j: cj, 'mid%d' % j: vj.mid, 'sa%d' % j: vj.sa, 'sr%d' % j: vj.sr, 'k%d' % j: vj.k})
        ent = self._write_npz(os.path.join(state_dir, 'state0.npz'), arrays)
        h = {'kind': 'MomTableU state0', 'hpar': self.hpar, 'kernel_sha': KERNEL_SHA, 'F': self.F, 'D': self.D, 'block': self.block,
             'codes_sha': self.codes_sha, 'files': {'state0.npz': ent}, 'zeroed': zeroed, 'max_zero_rad': mzr,
             'dropped': [list(A) for A in dropped]}
        return self._write_json(os.path.join(state_dir, 'handoff_state0.json'), h)

    def _load_Dj(self, state_dir):
        h = self._read_handoff(os.path.join(state_dir, 'handoff_state0.json'))
        if h.get('codes_sha') != self.codes_sha:
            raise ValueError('C-STATE: state0 was built on other code arrays')
        z = self._read_npz(state_dir, 'state0.npz', h['files']['state0.npz'])
        Dj = [None] * (min(self.F, self.D) + 1)
        for j in range(1, len(Dj)):
            v = MA(z['mid%d' % j].astype(float), z['sa%d' % j].astype(float), z['sr%d' % j].astype(float), z['k%d' % j].astype(np.int64))
            v.check('MomTableU D_j')
            Dj[j] = (z['c%d' % j].astype(np.int64), v)
        return Dj

    def block_pairs(self, k, b, Dj):
        """the exact candidate pair count of block b of level k (two searchsorted per (j, A)), before any arithmetic."""
        ck = self.codes[k]
        i0, i1 = b * self.block, min((b + 1) * self.block, len(ck))
        lo, hi = int(ck[i0]), int(ck[i1 - 1]) + 1
        tot = 0
        for j in range(1, min(k, self.F) + 1):
            cj = Dj[j][0]
            if len(cj) == 0:
                continue
            cq = self.codes[k - j]
            tot += int((np.searchsorted(cq, hi - cj, 'left') - np.searchsorted(cq, lo - cj, 'left')).sum())
        return tot

    def plan(self, state_dir, unit_pairs):
        """the units (k, b0, b1, pairs) in build order: per level, consecutive blocks packed up to unit_pairs (at least one block each)."""
        Dj = self._load_Dj(state_dir)
        units = []
        for k in range(1, self.D + 1):
            cur, acc = None, 0
            for b in range(self.nblocks(k)):
                p = self.block_pairs(k, b, Dj)
                if cur is not None and acc + p > unit_pairs:
                    units.append((k, cur, b, acc))
                    cur, acc = None, 0
                if cur is None:
                    cur = b
                acc += p
            if cur is not None:
                units.append((k, cur, self.nblocks(k), acc))
        return units

    def _codes_equal(self, z, k, name):
        """the review 53de1c0d Q3 (a): the stored codes must equal the codes recomputed from (F, D, groups, caps), exactly."""
        if 'codes' not in z or not np.array_equal(z['codes'].astype(np.int64), self.codes[k]):
            raise ValueError('C-STATE: %s does not carry this table\'s codes of level %d' % (name, k))

    def _load_level(self, state_dir, k):
        if k == 0:
            return MA.exact([1.0])
        h = self._read_handoff(os.path.join(state_dir, 'handoff_level_k%02d.json' % k))
        if h.get('level') != k or h.get('codes_sha') != self.codes_sha[k] or h.get('kernel_sha') != KERNEL_SHA:
            raise ValueError('C-STATE: level %d hand-off does not match' % k)
        name = 'level_k%02d.npz' % k
        z = self._read_npz(state_dir, name, h['files'][name])
        self._codes_equal(z, k, name)
        x = self._ma(z)
        if len(x.mid) != len(self.codes[k]):
            raise ValueError('C-STATE: level %d has %d entries, %d codes' % (k, len(x.mid), len(self.codes[k])))
        return x

    def _block(self, k, b, Dj, M):
        """block b of level k in the pull form (DESIGN sect. 1): all terms of its destinations, one seg_pairwise tree per destination,
        then div_int(k). Returns (MA, terms, candidate pairs, the largest terms / (2^|supp c| - 1) over the block's destinations)."""
        ck = self.codes[k]
        i0, i1 = b * self.block, min((b + 1) * self.block, len(ck))
        lo, hi = int(ck[i0]), int(ck[i1 - 1]) + 1
        dsts, mids, sas, srs, ks = [], [], [], [], []
        cand = 0
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            for j in range(1, min(k, self.F) + 1):
                cj, vj = Dj[j]
                if len(cj) == 0:
                    continue
                coef = float(Fraction(2 - self.n, 2) * j - k)
                vs = vj.scale(coef)
                cq = self.codes[k - j]
                Mq = M[k - j]
                left = np.searchsorted(cq, lo - cj, 'left')
                right = np.searchsorted(cq, hi - cj, 'left')
                cnt = right - left
                sel = np.flatnonzero(cnt > 0)
                if len(sel) == 0:
                    continue
                cs = cnt[sel]
                tot = int(cs.sum())
                cand += tot
                A = np.repeat(sel, cs)
                q = np.repeat(left[sel], cs) + (np.arange(tot, dtype=np.int64) - np.repeat(np.cumsum(cs) - cs, cs))
                keep = Mq.present()[q]
                A, q = A[keep], q[keep]
                dest = cj[A] + cq[q]
                idx = np.searchsorted(ck, dest)
                idx[idx >= len(ck)] = 0
                hit = ck[idx] == dest
                A, q, idx = A[hit], q[hit], idx[hit]
                if len(A) == 0:
                    continue
                mid, sa, sr = _prod((vs.mid[A], vs.sa[A], vs.sr[A]), (Mq.mid[q], Mq.sa[q], Mq.sr[q]))
                dsts.append(idx - i0)
                mids.append(mid)
                sas.append(sa)
                srs.append(sr)
                ks.append(vs.k[A] + Mq.k[q] + 1)
            nb = i1 - i0
            ratio = 0.0
            if dsts:
                dall = np.concatenate(dsts)
                acc = seg_pairwise(dall, np.concatenate(mids), np.concatenate(sas), np.concatenate(srs), np.concatenate(ks), nb)
                u, cnts = np.unique(dall, return_counts=True)          # C-PAIRS: terms per destination <= 2^|supp c| - 1
                supp = (self.decode(ck[i0:i1][u]) > 0).sum(axis=1)
                bound = np.left_shift(np.ones(len(u), dtype=np.int64), supp) - 1
                if np.any(cnts > bound):
                    raise ValueError('C-PAIRS: a destination of level %d block %d has more terms than 2^|supp c| - 1' % (k, b))
                ratio = float(np.max(cnts / bound))
            else:
                acc = MA.zeros(nb)
            res = acc.div_int(k)
        res.check('MomTableU level %d block %d' % (k, b))
        return res, int(sum(len(x) for x in dsts)), cand, ratio

    def run_unit(self, state_dir, unit, cpu_budget=None):
        """one unit (k, b0, b1[, pairs]): loads the levels it needs (verified), computes its blocks, writes them and a hand-off, and
        assembles and saves the level when the unit ends it. With cpu_budget (s), it stops between blocks, never inside one, before a block
        whose expected CPU (the previous block's CPU per pair times this block's pairs) would cross the budget; the report's 'end' is then
        the first block not done, which the caller's next unit starts from. C-PAIRS: the candidate pairs generated equal plan()'s exact
        count block by block, and no destination has more than 2^|supp c| - 1 terms. Returns the report dict."""
        t0 = time.process_time()
        tiny0 = TINY_COUNT[0]
        k, b0, b1 = int(unit[0]), int(unit[1]), int(unit[2])
        if not (1 <= k <= self.D and 0 <= b0 < b1 <= self.nblocks(k)):
            raise ValueError('a unit outside the table: %s' % (unit,))
        Dj = self._load_Dj(state_dir)
        M = [None] * (self.D + 1)
        for kk in range(max(0, k - min(k, self.F)), k):
            M[kk] = self._load_level(state_dir, kk)
        outs, terms, cands, planned, ratio, rate, end = [], 0, 0, 0, 0.0, None, b0
        for b in range(b0, b1):
            p = self.block_pairs(k, b, Dj)
            if cpu_budget is not None and outs and rate is not None and (time.process_time() - t0) + rate * p > cpu_budget:
                break
            tb = time.process_time()
            r, nt, cand, rt = self._block(k, b, Dj, M)
            if cand != p:
                raise ValueError('C-PAIRS: level %d block %d generated %d candidate pairs, plan() counted %d' % (k, b, cand, p))
            rate = (time.process_time() - tb) / max(p, 1)
            outs.append(r)
            terms, cands, planned, ratio, end = terms + nt, cands + cand, planned + p, max(ratio, rt), b + 1
        cat = MA(np.concatenate([o.mid for o in outs]), np.concatenate([o.sa for o in outs]), np.concatenate([o.sr for o in outs]),
                 np.concatenate([o.k for o in outs]))
        i0, i1 = b0 * self.block, min(end * self.block, len(self.codes[k]))
        name = 'unit_k%02d_b%05d_%05d.npz' % (k, b0, end)
        ent = self._write_npz(os.path.join(state_dir, name), {'codes': self.codes[k][i0:i1], 'mid': cat.mid, 'sa': cat.sa, 'sr': cat.sr,
                                                              'k': cat.k})
        rep = {'unit': [k, b0, end], 'asked': [k, b0, b1], 'pairs': planned, 'cand': cands, 'terms': terms, 'blocks': end - b0,
               'max_terms_ratio': ratio, 'check_ok': True, 'k_max': int(cat.k.max()) if len(cat.k) else 0,
               'shadow_max': float(cat.shadow_max()), 'tiny': TINY_COUNT[0] - tiny0, 'cpu': round(time.process_time() - t0, 3),
               'end': end, 'level_done': end == self.nblocks(k)}
        h = {'kind': 'MomTableU unit', 'hpar': self.hpar, 'kernel_sha': KERNEL_SHA, 'level': k, 'blocks': [b0, end], 'files': {name: ent},
             'report': rep}
        self._write_json(os.path.join(state_dir, 'handoff_unit_k%02d_b%05d_%05d.json' % (k, b0, end)), h)
        if end == self.nblocks(k):
            self._assemble(state_dir, k)
        return rep

    def _assemble(self, state_dir, k):
        """level k from its units: every unit hand-off of the level, contiguous from block 0, files verified, concatenated in order."""
        hs = []
        for fn in sorted(os.listdir(state_dir)):
            if fn.startswith('handoff_unit_k%02d_' % k) and fn.endswith('.json'):
                hs.append(self._read_handoff(os.path.join(state_dir, fn)))
        hs.sort(key=lambda h: h['blocks'][0])
        pos, parts = 0, []
        for h in hs:                                  # The review 53de1c0d Q3 (b): the unit ranges partition the destinations in code order
            if h.get('level') != k or h.get('kernel_sha') != KERNEL_SHA or h['blocks'][0] != pos or not (h['blocks'][1] > pos):
                raise ValueError('C-STATE: the units of level %d do not partition its blocks (gap, overlap, level or kernel)' % k)
            (name, ent), = h['files'].items()
            z = self._read_npz(state_dir, name, ent)
            j0, j1 = h['blocks'][0] * self.block, min(h['blocks'][1] * self.block, len(self.codes[k]))
            if not np.array_equal(z['codes'].astype(np.int64), self.codes[k][j0:j1]):
                raise ValueError('C-STATE: unit %s does not carry the codes of its blocks' % name)
            parts.append(self._ma(z))
            pos = h['blocks'][1]
        if pos != self.nblocks(k):
            raise ValueError('C-STATE: level %d is incomplete' % k)
        x = MA(np.concatenate([p.mid for p in parts]), np.concatenate([p.sa for p in parts]), np.concatenate([p.sr for p in parts]),
               np.concatenate([p.k for p in parts]))
        if len(x.mid) != len(self.codes[k]):
            raise ValueError('C-STATE: level %d assembled %d entries for %d codes' % (k, len(x.mid), len(self.codes[k])))
        x.check('MomTableU level %d' % k)
        name = 'level_k%02d.npz' % k
        ent = self._write_npz(os.path.join(state_dir, name), {'codes': self.codes[k], 'mid': x.mid, 'sa': x.sa, 'sr': x.sr, 'k': x.k})
        h = {'kind': 'MomTableU level', 'hpar': self.hpar, 'kernel_sha': KERNEL_SHA, 'level': k, 'codes_sha': self.codes_sha[k],
             'files': {name: ent}, 'units': [h_['blocks'] for h_ in hs]}
        return self._write_json(os.path.join(state_dir, 'handoff_level_k%02d.json' % k), h)

    def finish(self, state_dir):
        """the moments: each level times its rows' exponent factorials (v1_3's MomTable l.475-483), saved per level, and the table hand-off."""
        files = {}
        smax = 0.0
        for d in range(self.D + 1):
            Md = self._load_level(state_dir, d)
            ex = self.decode(self.codes[d])
            f = [math.prod(math.factorial(int(x)) for x in row) for row in ex]
            fl = np.array([float(x) for x in f])
            kf = np.array([1 if x > 2 ** 53 else 0 for x in f], dtype=np.int64)
            mm = MA(Md.mid * fl, Md.sa * fl, Md.sr * fl, Md.k + kf + 1)
            mm.check('MomTableU moments %d' % d)
            smax = max(smax, mm.shadow_max())
            name = 'mom_k%02d.npz' % d
            files[name] = self._write_npz(os.path.join(state_dir, name), {'codes': self.codes[d], 'mid': mm.mid, 'sa': mm.sa, 'sr': mm.sr,
                                                                          'k': mm.k})
        h = {'kind': 'MomTableU table', 'hpar': self.hpar, 'kernel_sha': KERNEL_SHA, 'F': self.F, 'D': self.D, 'codes_sha': self.codes_sha,
             'files': files, 'shadow_max': smax}
        return self._write_json(os.path.join(state_dir, 'handoff_table.json'), h)

    def load_view(self, state_dir, expected_sha256=None):
        """the finished table as a MomTableView, after verifying the table hand-off (its sha256 when given), H_par, the code hashes and
        every moment file."""
        path = os.path.join(state_dir, 'handoff_table.json')
        if expected_sha256 is not None and _sha_file(path) != expected_sha256:
            raise ValueError('C-STATE: the table hand-off is not the expected one')
        h = self._read_handoff(path)
        if h.get('codes_sha') != self.codes_sha or h.get('kernel_sha') != KERNEL_SHA:
            raise ValueError('C-STATE: the table was built on other code arrays or by another kernel')
        mom = []
        for d in range(self.D + 1):
            name = 'mom_k%02d.npz' % d
            z = self._read_npz(state_dir, name, h['files'][name])
            self._codes_equal(z, d, name)
            x = self._ma(z)
            if len(x.mid) != len(self.codes[d]):
                raise ValueError('C-STATE: moments of level %d have %d entries' % (d, len(x.mid)))
            mom.append(x)
        return MomTableView(self.F, self.D, self.n, self.groups, self.caps, self.B, self.pw, self.codes, mom, self.chunk)

    @staticmethod
    def load(state_dir, Gam, n, D, groups=None, caps=None, W_int=None, W=None, block=BLOCK, expected_sha256=None):
        """the consumer's entry: H_par recomputed from the caller's inputs, then load_view."""
        return MomTableU(Gam, n, D, groups=groups, caps=caps, W_int=W_int, W=W, block=block).load_view(state_dir, expected_sha256)


def compare_float(table, npz_path, code_key='codes', value_key='moments'):
    """v1_4 INFO: a float moment table (codes and values, the codes in base B = D + 1 with pw = B^f) against the certified one: the largest
    |mid - float| / rad over the codes both hold, and the coverage (float values inside the balls). Returns a dict; never a gate."""
    with np.load(npz_path, allow_pickle=False) as z:
        cf, vf = z[code_key].astype(np.int64), z[value_key].astype(float)
    allc = np.concatenate(table.codes)                  # distinct across levels: a code fixes the exponents, hence the degree
    allm = np.concatenate([m.mid for m in table.mom])
    allr = np.concatenate([m.radius() for m in table.mom])
    order = np.argsort(allc, kind='stable')
    sc = allc[order]
    pos = np.searchsorted(sc, cf)
    pos[pos >= len(sc)] = 0
    hit = np.flatnonzero(sc[pos] == cf)
    g = order[pos[hit]]
    diff = np.abs(allm[g] - vf[hit])
    rad = allr[g]
    with np.errstate(divide='ignore', invalid='ignore'):
        q = np.where(rad > 0, diff / np.where(rad > 0, rad, 1.0), np.where(diff == 0, 0.0, np.inf))
    return {'compared': int(len(hit)), 'float_codes': int(len(cf)), 'inside': int(np.count_nonzero(diff <= rad)),
            'worst_diff_over_rad': float(q.max()) if len(q) else 0.0}
