#!/usr/bin/env python3
"""r0asm_lib_v1_3_1.py -- pk02 (code/pk02/). The library of kt_r0asm_v1_3_1 (DESIGN_ROUTE0_ASM_v1 a673cfbb, ADD1 9e77cb72); the
driver pins it by its full sha256. No file I/O. REVISION of r0asm_lib_v1_3.py (6f2debcd, never run in a driver) for the review
(REVIEW_KT_R0ASM_v1_2_rv03.md 5f51acfa) as main folded it into v1_3 (13:11Z):
- t^2 on a piece interval by endpoints (sq), never ** (the J_hi = inf piece's t-interval touches 0); the derivative stays c_1 + 2 c_2 t;
- piece_T: the t-ends as the hull of both readings of each J string (decimal and binary64), as kt_p2_assembly's C-GRID-HULL;
- eval_r0: a negative upper end of beta^T M beta stops the evaluation (never clipped); B may be a dict {(graph, key): bar} for the
  per-entry sensitivity (others 0).
Everything else is r0asm_lib_v1_3's:
- Dual: a value ball and a t-derivative ball (arb, 512 bits), arithmetic by the chain rule (inclusion isotone).
- chain_r0 / chain_bp: route 0 (b) and (b') over any entry function E(g, k) returning arb balls or Duals (kt_r0asm_v1_2's formulas);
  squares by endpoints; every Z ball must be positive.
- eval_r0 / eval_bp: the centered form over a piece T (ADD1 sect. 2): Q(T) in Q(t_c; Theta) + dQ/dt(T x Theta) [-Delta, Delta], with
  the remainder Rbar = |c_3|_hi t_hi^3 + bar + trick + B a constant of the piece; PD by the minors of the centered G box and positive
  pivots in both chains. A point T (the hull of 1/J_lo's two readings) is the point evaluation.
- dec_round / dec_ok: outward decimal strings at 17 significant digits from exact rationals by integer arithmetic; re-read check.
- fin / record_problems: the finiteness checks of C-FINITE.
- FloatReader (the ent files' ak, coefficient points, bar 0) and CertReader (m3 records through a pinned reader module's entry_ball:
  coefficient hulls [LO_k, HI_k] and bar err_b, CLAIM_BALL's form)."""
import math
import re
from fractions import Fraction
from flint import arb, arb_mat

UNIT = arb(0, 1)
ZERO = arb(0)
SPAN3 = [0, 1, 2, 3]
KEYS_R0 = ([('W2', 'Z'), ('W2', 'CE'), ('W2', 'CF')] + [('W2', 'G,%d,%d' % (a, b)) for a in range(4) for b in range(a, 4)]
           + [('W2', '%s,%d' % (p, a)) for p in ('V', 'KE', 'K1') for a in range(4)] + [('W3f', k) for k in ('Z', 'FF', 'F1', 'F2')]
           + [('W3e', 'Z'), ('W3e', 'ME2')] + [('W3e', 'M,%d,%d,%s' % (a, b, s)) for a in range(4) for b in range(a, 4)
                                                for s in ('ee', 'e1', 'e2', '00')])


def keys_bp(g):
    return [(g, '%s,%d' % (p, j)) for p in ('1', 'T', 'B', 'X') for j in range(10)]


class Dual:
    """value v and t-derivative d, both arb balls."""
    __slots__ = ('v', 'd')

    def __init__(self, v, d):
        self.v, self.d = v, d

    def lower(self):
        return self.v.lower()

    def __add__(self, o):
        o = lift(o)
        return Dual(self.v + o.v, self.d + o.d)

    __radd__ = __add__

    def __sub__(self, o):
        o = lift(o)
        return Dual(self.v - o.v, self.d - o.d)

    def __rsub__(self, o):
        o = lift(o)
        return Dual(o.v - self.v, o.d - self.d)

    def __mul__(self, o):
        o = lift(o)
        return Dual(self.v * o.v, self.v * o.d + self.d * o.v)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = lift(o)
        q = self.v / o.v
        return Dual(q, (self.d - q * o.d) / o.v)

    def __rtruediv__(self, o):
        return lift(o) / self

    def __neg__(self):
        return Dual(-self.v, -self.d)

    def sqrt(self):
        r = self.v.sqrt()
        return Dual(r, self.d / (2 * r))


def lift(o):
    if isinstance(o, Dual):
        return o
    return Dual(o if isinstance(o, arb) else arb(o), ZERO)


def lo_of(x):
    return x.v.lower() if isinstance(x, Dual) else x.lower()


def zsum(xs, zero=ZERO):
    xs = list(xs)
    if not xs:
        return zero
    acc = xs[0]
    for x in xs[1:]:
        acc = acc + x
    return acc


def amax(xs):
    m = xs[0]
    for x in xs[1:]:
        if x > m:
            m = x
    return m


def sq(x):
    """x^2 by endpoints (python-flint's ** 2 is NaN on a ball that contains 0); a Dual squares its value so and its derivative by
    2 v d."""
    if isinstance(x, Dual):
        return Dual(sq(x.v), 2 * x.v * x.d)
    if x.lower() > 0 or x.upper() < 0:
        return x * x
    m = amax([abs(x.lower()), abs(x.upper())])
    return arb(0).union(m * m)


def minors(Gm, n):
    res = []
    for m in range(1, n + 1):
        A = arb_mat(m, m)
        for i in range(m):
            for j in range(m):
                A[i, j] = Gm[i][j]
        res.append(A.det())
    return res


def chol(Gm, n):
    L = [[ZERO] * n for _ in range(n)]
    for j in range(n):
        s = Gm[j][j] - zsum(sq(L[j][k]) for k in range(j))
        if not (lo_of(s) > 0):
            return None
        L[j][j] = s.sqrt()
        for i in range(j + 1, n):
            L[i][j] = (Gm[i][j] - zsum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    return L


def flat(x):
    """the arb balls of an arb or a Dual."""
    return [x.v, x.d] if isinstance(x, Dual) else [x]


def chain_r0(E, plant_g=False):
    Z = {g: E(g, 'Z') for g in ('W2', 'W3f', 'W3e')}
    res = dict(pd=True, why='', all=[b for z in Z.values() for b in flat(z)])
    if not all(lo_of(z) > 0 for z in Z.values()):
        res.update(pd=False, why='a window Z ball not positive')
        return res
    Rr = lambda g, k: E(g, k) / Z[g]
    c_e2, c_f2, c_e3, c_f3 = Rr('W2', 'CE'), Rr('W2', 'CF'), Rr('W3e', 'ME2'), Rr('W3f', 'F2')
    n = len(SPAN3)
    G0 = [[Rr('W2', 'G,%d,%d' % (min(a, b), max(a, b))) for b in SPAN3] for a in SPAN3]
    Gm = [row[:] for row in G0]
    if plant_g:
        d = 2 * (Gm[1][1] * Gm[2][2]).sqrt()
        Gm[1][2] = Gm[1][2] + d
        Gm[2][1] = Gm[2][1] + d
    v = [Rr('W2', 'V,%d' % a) - c_f2 * G0[0][i] for i, a in enumerate(SPAN3)]
    KE = [Rr('W2', 'KE,%d' % a) - c_e2 * Rr('W2', 'K1,%d' % a) for a in SPAN3]
    Mm = [[None] * n for _ in range(n)]
    for i, a in enumerate(SPAN3):
        for j, b in enumerate(SPAN3):
            k_ = 'M,%d,%d,' % (min(a, b), max(a, b))
            Mm[i][j] = (Rr('W3e', k_ + 'ee') - c_e3 * (Rr('W3e', k_ + 'e1') + Rr('W3e', k_ + 'e2')) + c_e3 * c_e3 * Rr('W3e', k_ + '00')
                        - KE[i] * KE[j])
    Eh2 = Rr('W3f', 'FF') - c_f3 * (Rr('W3f', 'F1') + Rr('W3f', 'F2')) + c_f3 * c_f3
    res.update(c_e2=c_e2, c_e3=c_e3, G=Gm, Eh2=Eh2)
    res['all'] += [b for x in [c_e2, c_f2, c_e3, c_f3, Eh2] + [g for row in Gm for g in row] + v + KE + [m for row in Mm for m in row]
                   for b in flat(x)]
    L = chol(Gm, n)
    if L is None:
        res.update(pd=False, why='a Cholesky pivot not positive')
        return res
    y = [ZERO] * n
    for i in range(n):
        y[i] = (v[i] - zsum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    vGv = zsum(sq(yi) for yi in y)
    beta = [ZERO] * n
    for i in reversed(range(n)):
        beta[i] = (y[i] - zsum(L[k][i] * beta[k] for k in range(i + 1, n))) / L[i][i]
    bMb = zsum(beta[i] * Mm[i][j] * beta[j] for i in range(n) for j in range(n))
    hp2 = Eh2 - vGv
    res.update(vGv=vGv, bMb=bMb, hp2=hp2)
    res['all'] += [b for x in [vGv, bMb, hp2] + y + beta + [L[i][j] for i in range(n) for j in range(i + 1)] for b in flat(x)]
    return res


def chain_bp(E, g):
    Z = E(g, '1,0')
    res = dict(ok=bool(lo_of(Z) > 0), all=flat(Z))
    if not res['ok']:
        return res
    Rr = lambda k: E(g, k) / Z
    c_t, c_b = Rr('T,0'), Rr('B,0')
    EX = [Rr('X,%d' % j) - c_b * Rr('T,%d' % j) - c_t * Rr('B,%d' % j) + c_t * c_b * Rr('1,%d' % j) for j in range(10)]
    v = [EX[j] - Rr('1,%d' % j) * EX[0] for j in range(1, 10)]
    res.update(v=v, E0Xc=EX[0])
    res['all'] += [b for x in [c_t, c_b] + EX + v for b in flat(x)]
    return res


def rbar(c, bar, trem, B):
    """the piece's remainder bound: |c_3|_hi t_hi^3 + bar + B, an exact upper point."""
    return (abs(c[3]).upper() * (trem * trem * trem) + bar + B).upper()


def entry_center(c, bar, tc, trem, B, thin=False):
    v = c[0] + c[1] * tc + c[2] * sq(tc)
    return v if thin else v + UNIT * rbar(c, bar, trem, B)


def entry_dual(c, bar, T, trem, B, thin=False):
    v = c[0] + c[1] * T + c[2] * sq(T)
    if not thin:
        v = v + UNIT * rbar(c, bar, trem, B)
    return Dual(v, c[1] + 2 * c[2] * T)


def t_of(js):
    """1/J over both readings of the string js: the decimal and its binary64 value."""
    return (1 / arb(js)).union(1 / arb(float(js)))


def piece_T(jlo, jhi):
    """t-ball of a piece from the export's strings: [1/J_hi, 1/J_lo] over both readings (0 for J_hi 'inf'); jhi None gives the point
    ball 1/J_lo (both readings)."""
    t_hi = t_of(jlo)
    if jhi is None:
        return t_hi
    t_lo = ZERO if jhi == 'inf' else t_of(jhi)
    return arb(t_lo.lower()).union(arb(t_hi.upper()))


def eval_r0(rd, T, A, B=0.0, trick=ZERO, plant_g=False):
    """the route-0 (b) quantities over the piece T (centered form, ADD1 sect. 2); B a float for every entry or a dict per entry."""
    tc, Dl, trem = T.mid(), T.rad(), T.upper()
    Bx = (lambda gk: B.get(gk, 0.0)) if isinstance(B, dict) else (lambda gk: B)
    co = {gk: rd.entry(*gk) for gk in KEYS_R0}
    Ec = {gk: entry_center(c, bar + trick, tc, trem, Bx(gk)) for gk, (c, bar) in co.items()}
    Ed = {gk: entry_dual(c, bar + trick, T, trem, Bx(gk)) for gk, (c, bar) in co.items()}
    rc = chain_r0(lambda g, k: Ec[(g, k)], plant_g)
    rv = chain_r0(lambda g, k: Ed[(g, k)], plant_g)
    DEL = UNIT * Dl
    cen = lambda a, b: a + b.d * DEL
    res = dict(pd=rc['pd'] and rv['pd'], why=('center chain: ' + rc['why']) if not rc['pd'] else ('Dual chain: ' + rv['why']) if not rv['pd']
               else '', allb=[b for x in Ec.values() for b in flat(x)] + [b for x in Ed.values() for b in flat(x)] + rc['all'] + rv['all'],
               tc=tc, Delta=Dl, rc=rc, rv=rv)
    if 'G' not in rc or 'G' not in rv:
        res['mins'] = []
        return res
    Gb = [[cen(rc['G'][i][j], rv['G'][i][j]) for j in range(4)] for i in range(4)]
    mins = minors(Gb, 4)
    c_e2, c_e3, Eh2 = cen(rc['c_e2'], rv['c_e2']), cen(rc['c_e3'], rv['c_e3']), cen(rc['Eh2'], rv['Eh2'])
    res.update(G=Gb, mins=mins, c_e2=c_e2, c_e3=c_e3, Eh2=Eh2)
    res['allb'] += [b for row in Gb for b in row] + mins + [c_e2, c_e3, Eh2]
    if res['pd'] and not all(m.lower() > 0 for m in mins):
        res.update(pd=False, why='a leading minor of the piece G box not positive')
    if not res['pd']:
        return res
    vGv, bMb, hp2 = cen(rc['vGv'], rv['vGv']), cen(rc['bMb'], rv['bMb']), cen(rc['hp2'], rv['hp2'])
    ce = amax([abs(c.lower()) for c in (c_e2, c_e3)] + [abs(c.upper()) for c in (c_e2, c_e3)])
    K_e = (A + ce).upper()
    res.update(vGv=vGv, bMb=bMb, hp2=hp2, K_e_hi=K_e, stop=bool(hp2.upper() < 0 or bMb.upper() < 0))
    res['allb'] += [vGv, bMb, hp2, K_e]
    if res['stop']:
        res['why'] = 'the upper end of %s below 0' % ('||h_perp||^2' if hp2.upper() < 0 else 'beta^T M beta')
        return res
    qW = bMb.upper().sqrt().upper()
    hp = hp2.upper().sqrt().upper()
    res.update(q_W_hi=qW, hp_hi=hp, q_b_hi=(qW + K_e * hp).upper())
    res['allb'] += [qW, hp, res['q_b_hi']]
    return res


def eval_bp(rd, T, g, B=0.0):
    """(b') v_j and E_0[X_c] over the piece T (centered form)."""
    tc, Dl, trem = T.mid(), T.rad(), T.upper()
    co = {gk: rd.entry(*gk) for gk in keys_bp(g)}
    Ec = {gk: entry_center(c, bar, tc, trem, B) for gk, (c, bar) in co.items()}
    Ed = {gk: entry_dual(c, bar, T, trem, B) for gk, (c, bar) in co.items()}
    bc = chain_bp(lambda gg, k: Ec[(gg, k)], g)
    bv = chain_bp(lambda gg, k: Ed[(gg, k)], g)
    res = dict(ok=bc['ok'] and bv['ok'], allb=[b for x in Ec.values() for b in flat(x)] + [b for x in Ed.values() for b in flat(x)]
               + bc['all'] + bv['all'])
    if not res['ok']:
        return res
    DEL = UNIT * Dl
    res.update(v=[bc['v'][j] + bv['v'][j].d * DEL for j in range(9)], E0Xc=bc['E0Xc'] + bv['E0Xc'].d * DEL)
    res['allb'] += res['v'] + [res['E0Xc']]
    return res


def fin(x):
    return all(b.is_finite() for b in flat(x))


def end_frac(x):
    """the exact rational value of an exact arb point (signed fmpz mantissa and exponent)."""
    m, e = x.man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def dec_round(f, up):
    """f (a Fraction) to 17 significant decimal digits, rounded up (ceil) or down (floor), as a string."""
    if f == 0:
        return '0'
    a = -f if f < 0 else f
    k = len(str(a.numerator)) - len(str(a.denominator))
    while Fraction(10) ** k > a:
        k -= 1
    while Fraction(10) ** (k + 1) <= a:
        k += 1
    e = k - 16
    s = a / Fraction(10) ** e
    if f < 0:
        n = -math.floor(s) if up else -math.ceil(s)
    else:
        n = math.ceil(s) if up else math.floor(s)
    d = str(abs(n))
    return '%s%s.%se%d' % ('-' if n < 0 else '', d[0], d[1:], e + len(d) - 1)


def dec_ok(s, f, up):
    """s brackets the exact end f outward (up: s >= f; else s <= f) and lies within 1e-16 relative of it."""
    try:
        q = Fraction(s)
    except (ValueError, ZeroDivisionError):
        return False
    if (q < f) if up else (q > f):
        return False
    return abs(q - f) <= Fraction(1, 10 ** 16) * abs(f)


NUMRE = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$')
BADRE = re.compile(r'^[-+]?(nan|inf(inity)?)$', re.I)


def record_problems(obj, path='', allow_inf=()):
    """C-FINITE on a record: every float finite, no string 'nan'/'inf' outside the allowed paths, numeric strings parse."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out += record_problems(v, '%s.%s' % (path, k), allow_inf)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += record_problems(v, '%s[%d]' % (path, i), allow_inf)
    elif isinstance(obj, float):
        if not math.isfinite(obj):
            out.append('%s float %r' % (path, obj))
    elif isinstance(obj, str):
        if BADRE.match(obj) and path not in allow_inf:
            out.append('%s string %r' % (path, obj))
        elif NUMRE.match(obj):
            try:
                Fraction(obj)
            except (ValueError, ZeroDivisionError):
                out.append('%s unparsable %r' % (path, obj))
    return out


class FloatReader:
    """the float entries: coefficient points ak[0..3] of the ent files, bar 0."""
    mode = 'float'

    def __init__(self, ents):
        self.ak = {}
        for ent in ents:
            for g, gd in ent['graphs'].items():
                for k, v in gd['ak'].items():
                    self.ak[(g, k)] = [float(x) for x in v[:4]]

    def fl(self, g, k):
        return self.ak[(g, k)]

    def entry(self, g, k):
        return [arb(a) for a in self.ak[(g, k)]], ZERO


def arb_frac(f):
    f = Fraction(f)
    return arb(f.numerator) / arb(f.denominator)


class CertReader:
    """m3 records through a pinned reader module R: entry_ball(rec, key) = (LO[0..3], HI[0..3], err_b) exact Fractions; for t in
    [0, 1/J_REF] the entry lies in sum_k [LO_k, HI_k] t^k + [-err_b, err_b] (CLAIM_BALL). recs: {graph: loaded record};
    key_format: the record's item key, e.g. '{g}:{k}'."""
    mode = 'certified'

    def __init__(self, R, recs, key_format):
        self.R, self.recs, self.key_format = R, recs, key_format

    def entry(self, g, k):
        LO, HI, eb = self.R.entry_ball(self.recs[g], self.key_format.format(g=g, k=k))
        if len(LO) != 4 or len(HI) != 4 or any(Fraction(l_) > Fraction(h_) for l_, h_ in zip(LO, HI)) or Fraction(eb) < 0:
            raise ValueError('%s:%s: entry_ball is not 4 ordered coefficient pairs and a bar >= 0' % (g, k))
        c = [arb(arb_frac(l_).lower()).union(arb(arb_frac(h_).upper())) for l_, h_ in zip(LO, HI)]
        return c, arb_frac(eb).upper()
