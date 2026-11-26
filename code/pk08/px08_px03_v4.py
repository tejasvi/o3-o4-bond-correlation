#!/usr/bin/env python3
"""px08_px03_v4.py -- pk08, S4 port, milestone 3: the tail's Chernoff factor, the graded annulus, far and the equator, certified for
every J >= 300. px08_px03_v3 (38dccfd8; the DELTA_PX08_PX03_V3 2fe50a0b: sound) with option A (2026-11-07): v3's
n4 sh1 took 214.6 s of the 230 s item limit (the covers of the nearly singular theta = 17/20 matrices need up to 1.5e5 boxes), so the
outer shells would not fit one item. What changes against px08_px03_v3, and nothing else:
- half-shell items sh1a, sh1b, sh2a, sh2b, sh3a, sh3b (families v0-v2 and v3-v5 of each shell); the whole-shell items stay; the theta
  order 17/20, 7/10, 1/2 is unchanged (option A keeps the annulus near float size);
- run_item: sh1a carries C-BLOCK-M and C-PORT-M, as sh1 does; expected_checks counts len(families(part)) (the cosmetic note);
- asm: accepts item outputs of px08_px03_v3 (sha256 M3V3_SHA, written by the build from sha256sum) as well as of this file, each script
  name paired with its sha (Y1), so v3's n4 tail and n4 sh1 outputs are reused; it requires every family exactly once, whether a shell
  comes as a whole item or as its two halves; C-ITEMCODE-M3 checks that v3's evaluation code equals this file's byte for byte (the lines
  from NODE CORE A BEGIN to 'def families(part):' and from 'def cfun_f(x):' to 'def run_item(N):': the core, the parameters, the matrix
  families, lam_of, C-PROP, the covers, TW, G, the controls' functions and eval_family), with PLANT-ITEMCODE-M3; a PRODUCERS line.
  C-ITEMCODE-M3 pins the evaluation code only: families() and run_item differ between v3 and v4 by the half-shell additions of the reviewed
  diff, and for the whole-shell parts they behave as in v3 (the N1 lesson).

Design: S4_M3_DESIGN_v1 (f368c2c6) with the CHECK (f38d2b57: valid; M3a-M3e) and v3's M1-M4. Parameters from the float scan
px08_m3scan_v1 (a517bb1c, output d9db7717): eps_s = 0.65 on every shell; each lam = theta/(2 Lmax) floored to a multiple of 1e-6, Lmax
recomputed here in float exactly as the scan does (257 al-points on [0, pi] and the N = 3 reflection, M3a); theta = 17/20, 7/10, 1/2 in
that order, the first whose matrix C-PROP certifies and (integrated families) whose cover ladder certifies (M2); any certified lam is valid.
The pieces (each J-bound is twrig6z's with its own t = 1/J; the comparison at t = 1/300 is the group (c) argument, CHECK f38d2b57 (2)):
- tail <= pref^2 L2 (sum_v e^{-lam_v J a_v} T_v)^{1/2}, T_v = int dmu w det(Q - 2 lam_v B_v)^{-1/2} (+ the N = 3 reflection atom); L2 is
  group (b)'s upper end, read from px08_m2bb4's n4/n3 asm output (VERDICT VALID required);
- annulus <= pref^2 sum_s sum_v e^{-lam_sv J prev_sv} A_sv, A_sv = int dmu w det(Q - 2 T(1/300, sh_s, eps_s) - 2 lam_sv B_v)^{-1/2};
- far <= pref^2 64 sum_v e^{-lam'_v J avp_v} det(Qf - 2 lam'_v B_v)^{-1/2}, Qf = Qnt - 2 cfun(0.96) (1/300) I (one constant matrix);
- equator <= pref^2 12 (2J/pi)^{1/2} e^{-J (1 - cos 0.685)}; all at J = 300, and each decreases in J.
Every integrand is w det(.)^{-1/2} of one matrix family (no moment tables). Per family: C-PROP (interval LDL^T of the full real matrix on
al-intervals over [0, pi], halved on failure to depth 8, at most PROP_MAXEV evaluations, and at the N = 3 reflection; M3e: the families are
P-covariant, so this covers the circle), the cover ladder of Re det > 0 (sigma 0.5, 0.375, 0.25 with M = 64, 88, 128), TW on the M nodes
(+ the reflection atom), and G on Im al = sigma (boxes of width pi/32, |w| det_lower^{-1/2}, det_lower by sub-box block products, halved on
failure to depth 2), with C-EVEN, C-CONJ and C-HALF.
Items, per N: tail (6 families), sh1, sh2, sh3 (6 each), far (the 6 far matrices; the equator is closed form, evaluated in the asm), each
with PLANT-PROP and, for integrated families, PLANT-STRIP and
PLANT-DET on its first family; tail and sh1 run C-BLOCK-M (blocks against the full matrix at al = 0.7, 2.3 and 0.3 + 0.2i, with a plant)
on their first family, far runs it on its constant matrices (M3d); sh1 runs C-PORT-M (tilt2 at the shell radii against twlib2, entrywise,
with a plant); every item runs C-FLT-M (each family's det at al = 0.7 and 2.3 against numpy, per value, with a plant).
Half-shell items sh1a ... sh3b run three families each, with PLANT-PROP, PLANT-STRIP and PLANT-DET on their first family; sh1a runs
C-BLOCK-M and C-PORT-M as sh1 does.
asm: reads the item outputs (each family exactly once: tail, far, and each shell whole or as its two halves; of v3 or of this file) and
the group (b) asm output (manifest; sha256 and headers checked), checks each item's CHECK and PLANT lines against the expected multiset
(M3), C-ITEMCODE-M3, and prints the four pieces and their sum at J = 300 (upper ends, one-sided decimals, W1), with group (b)'s TARGET line
quoted (M4).
Usage: px08_px03_v4.py n4|n3 tail|sh1|sh2|sh3|sh1a|sh1b|sh2a|sh2b|sh3a|sh3b|far LIM | n4|n3 asm LIM MANIFEST.
"""
import resource, sys, time, math, hashlib, signal, os
from fractions import Fraction as Fr
PARTS = ('tail', 'sh1', 'sh2', 'sh3', 'sh1a', 'sh1b', 'sh2a', 'sh2b', 'sh3a', 'sh3b', 'far', 'asm')
if len(sys.argv) < 4 or sys.argv[1] not in ('n4', 'n3') or sys.argv[2] not in PARTS:
    print('usage: px08_px03_v4.py n4|n3 tail|sh1|sh2|sh3|sh1a|sh1b|sh2a|sh2b|sh3a|sh3b|far LIM | n4|n3 asm LIM MANIFEST')
    sys.exit(2)
MODE, PART, LIM = sys.argv[1], sys.argv[2], int(sys.argv[3])
if not (5 <= LIM <= 240) or (PART == 'asm') != (len(sys.argv) == 5):
    print('bad LIM %d or arguments' % LIM)
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
STAGE = ['start']


def cpu():
    return time.process_time()


def out(line):
    print(line, flush=True)


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
SCR = '/mnt/g2/release/root/code/pk10/scripts'
SOURCES = {'twlib.py': '29bca6b268050911e23c4429a9cc4a26668e5ea3fa694db2926996297b8d1527',
           'twlib2.py': 'cdf024cc8ebf76d7b9ac581ffa15dea78526e0fd3694acca6c7c8dd92b11a4c4',
           'twrig6z.py': 'db1220448bae51acebe0d7b0aa29a9f44e72f2c04264de32f6fe04c4ef3de5ec',
           'gfmom.py': 'c8cadafec97a92071b7f90d66a69b0f24fc91a7bd6ec751c1327a8218c9a2768',
           'lapl2.py': 'b28ffbdb86fab237564f2db9ea8b3e904481fba31ad79e39421de7b8a9dfe116',
           'vacmod2.py': '533546b173af147a56e9531e26afa64cb3dbaccefd5fb7b1283f03baff06a000'}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('px08_px03_v4 sha256 %s ITEM=%s %s LIM=%d' % (sha_file(os.path.abspath(__file__)), MODE, PART, LIM))
# ==== NODE CORE A BEGIN (s4c_m2bb.py lines 84-636, byte for byte) ====
_bad = ['%s %s' % (n_, sha_file(os.path.join(SCR, n_))) for n_ in sorted(SOURCES) if sha_file(os.path.join(SCR, n_)) != SOURCES[n_]]
out('C-HASH %s (%d sources)%s' % ('PASS' if not _bad else 'FAIL', len(SOURCES), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
import numpy as np
from flint import arb, acb, arb_mat, acb_mat, ctx, fmpz
sys.path.insert(0, SCR)
import twlib2 as T2
from gfmom import GFMom
import functools
T2.Ej = functools.lru_cache(maxsize=None)(T2.Ej)
ctx.prec = 128

SIG_LEAD = (0.5, 0.375, 0.25)
M_MOM, K0, BMAX, TOL = 96, 8, 48, 1e-12
KX, KY, CDMAX, GDMAX = 32, 4, 12, 8
LEAD_REF, NORM_TOL = '1.0302393041', '1e-9'
C12_REF = {4: ('0.846041', '0.639526'), 3: ('0.742488', '0.537950')}
C12_TOL = '1e-6'
TW3 = {4: '1.0331520608', 3: '1.0327952789'}           # twrig6z third order at J = 300 (sp0 outputs 55824efe, 98761475), FLOAT
C3F = {4: '0.498944', 3: '0.438039'}
PI = arb.pi()


class NotCert(Exception):
    pass


# ------------------------------------------------------------------ the series H1..H3 in exact rationals (twlib2.H_series)
FORMS2 = ['X1', 'X2', 'X3', 'X4', 'X5', 'Z', 'aT', 'bT', 'aB', 'bB']
IX2 = {f: i for i, f in enumerate(FORMS2)}
NF = len(FORMS2)
ROOT_BONDS = ['X1', 'X2', 'X4']
PAIR_BONDS = [('X1', 'X3'), ('X2', 'X5'), ('X3', 'X4'), ('X4', 'X5'), ('X4', 'Z')]
TWISTED = [('X1', 'X3', 'aT', 'bT'), ('X2', 'X5', 'aB', 'bB')]
Z0 = tuple([0] * NF)


def m2(**kw):
    e = [0] * NF
    for f, p in kw.items():
        e[IX2[f]] += p
    return tuple(e)


def padd(*Ps):
    o = {}
    for P in Ps:
        for e, c in P.items():
            o[e] = o[e] + c if e in o else c
    return {e: c for e, c in o.items() if c != 0}


def pmul(P, Q):
    o = {}
    for e1, c1 in P.items():
        for e2, c2 in Q.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            o[e] = o[e] + c1 * c2 if e in o else c1 * c2
    return {e: c for e, c in o.items() if c != 0}


def pscale(P, c):
    return {e: c * v for e, v in P.items() if c * v != 0}


def cm_fr(m):
    df = 1
    for q in range(2 * m - 3, 0, -2):
        df *= q
    return Fr(df, 2 ** m * math.factorial(m))


def s_add(a, b):
    return [padd(x, y) for x, y in zip(a, b)]


def s_scale(a, c):
    return [pscale(x, c) for x in a]


def s_mul(a, b, K):
    o = [{} for _ in range(K + 1)]
    for i in range(K + 1):
        for j in range(K + 1 - i):
            if a[i] and b[j]:
                o[i + j] = padd(o[i + j], pmul(a[i], b[j]))
    return o


def s_sqrt1m(var, K):
    o = [{Z0: Fr(1)}] + [{} for _ in range(K)]
    for m_ in range(1, K + 1):
        o[m_] = {m2(**{var: m_}): -cm_fr(m_)}
    return o


def s_const(P, K):
    return [dict(P)] + [{} for _ in range(K)]


def s_inv1pc(K):
    w = [{}] + [{m2(Z=m_): cm_fr(m_)} for m_ in range(1, K + 1)]
    o = s_const({Z0: Fr(1, 2)}, K)
    pw = s_const({Z0: Fr(1)}, K)
    for k in range(1, K + 1):
        pw = s_mul(pw, s_scale(w, Fr(1, 2)), K)
        o = s_add(o, s_scale(pw, Fr(1, 2)))
    return o


def H_series_exact(K):
    KK = K + 1
    H = [{} for _ in range(K + 1)]

    def add_shift(S, extra=None):
        for k in range(1, KK + 1):
            if k - 1 <= K and S[k]:
                H[k - 1] = padd(H[k - 1], S[k])
        if extra:
            H[0] = padd(H[0], extra)
    for v in FORMS2[:6]:
        for m_ in range(1, K + 1):
            H[m_] = padd(H[m_], {m2(**{v: m_}): Fr(1, 2 * m_)})
    for v in ROOT_BONDS:
        S = s_sqrt1m(v, KK)
        S[0] = {}
        add_shift(S, {m2(**{v: 1}): Fr(1, 2)})
    for (u, v) in PAIR_BONDS:
        S = s_mul(s_sqrt1m(u, KK), s_sqrt1m(v, KK), KK)
        S[0] = padd(S[0], {Z0: Fr(-1)})
        add_shift(S, {m2(**{u: 1}): Fr(1, 2), m2(**{v: 1}): Fr(1, 2)})
    for (x, xp, a, b) in TWISTED:
        S = s_mul(s_mul(s_sqrt1m('Z', KK), s_sqrt1m(x, KK), KK), s_sqrt1m(xp, KK), KK)
        S[0] = padd(S[0], {Z0: Fr(-1)})
        add_shift(S, {m2(**{x: 1}): Fr(1, 2), m2(**{xp: 1}): Fr(1, 2), m2(Z=1): Fr(1, 2)})
        ab = {m2(**{a: 1, b: 1}): Fr(1)}
        inv = s_inv1pc(K)
        for k in range(K):
            if inv[k]:
                H[k + 1] = padd(H[k + 1], pscale(pmul(ab, inv[k]), Fr(-1)))
        sx, sxp = s_sqrt1m(x, K), s_sqrt1m(xp, K)
        for k in range(1, K + 1):
            H[k] = padd(H[k], pmul(sx[k], {m2(**{a: 1}): Fr(1)}))
            H[k] = padd(H[k], pscale(pmul(sxp[k], {m2(**{b: 1}): Fr(1)}), Fr(-1)))
    assert not H[0], H[0]
    return H


def c_series(HX, plant=False):
    """C-SERIES: exact H1..H3 against twlib2's float series (same support, coefficient error <= 2^-50 max(1, |c|))"""
    HF = T2.H_series(3)
    worst, bad = 0.0, []
    for k in (1, 2, 3):
        ex = dict(HX[k])
        if plant and k == 2:
            e0 = sorted(ex)[0]
            ex[e0] = ex[e0] + Fr(1, 2 ** 40) * max(Fr(1), abs(ex[e0]))
        if set(ex) != set(HF[k]):
            bad.append('H%d support (%d exact, %d float)' % (k, len(ex), len(HF[k])))
            continue
        for e, c in ex.items():
            d = abs(Fr(HF[k][e]) - c)
            tol = Fr(1, 2 ** 50) * max(Fr(1), abs(c))
            worst = max(worst, float(d / max(Fr(1), abs(c))))
            if d > tol:
                bad.append('H%d %s' % (k, e))
    return (not bad), worst, bad[:3]


def to_arb(P):
    return {e: arb(c.numerator) / c.denominator for e, c in P.items()}


# ------------------------------------------------------------------ full matrices in acb (s4c_m1c, unchanged)
def zeros(n):
    return acb_mat(n, n)


def eye(n):
    M = acb_mat(n, n)
    for i in range(n):
        M[i, i] = 1
    return M


def kw(N, al):
    if al is None:
        K = zeros(2)
        K[0, 0], K[1, 1] = 1, -1
        return K, acb(1)
    c, s = al.cos(), al.sin()
    if N == 4:
        K = zeros(3)
        K[0, 0], K[0, 1], K[1, 0], K[1, 1], K[2, 2] = c, -s, s, c, 1
        return K, 1 - c
    K = zeros(2)
    K[0, 0], K[0, 1], K[1, 0], K[1, 1] = c, -s, s, c
    return K, acb(arb(1) / 2)


def addblk(Q, n, i, j, B):
    for p in range(n):
        for q in range(n):
            Q[i * n + p, j * n + q] = Q[i * n + p, j * n + q] + B[p, q]


def gram(Q, n, parts):
    for (u, cu) in parts:
        for (v, cv) in parts:
            addblk(Q, n, u, v, cu.transpose() * cv)


def Qmat2(k):
    n = k.nrows()
    I, mI, mk = eye(n), eye(n) * (-1), k * (-1)
    Q = zeros(6 * n)
    for parts in ([(0, I)], [(1, I)], [(0, I), (2, mI)], [(3, I)], [(1, I), (4, mI)], [(2, I), (3, mI)], [(3, I), (4, mI)],
                  [(2, I), (0, mk), (5, mI)], [(3, I), (5, mI)], [(4, I), (1, mk), (5, mI)]):
        gram(Q, n, parts)
    return Q


def forms2(k):
    n = k.nrows()
    I = eye(n)
    half = arb(1) / 2

    def blk(i, j, Bm):
        B = zeros(6 * n)
        addblk(B, n, i, j, Bm)
        if i != j:
            addblk(B, n, j, i, Bm.transpose())
        return B
    return [blk(v, v, I) for v in range(6)] + [blk(2, 5, I * half), blk(0, 5, k.transpose() * half), blk(4, 5, I * half),
                                               blk(1, 5, k.transpose() * half)]


# ------------------------------------------------------------------ the 6 x 6 blocks of the split (2)
PARTS_Q = ([(0, 1)], [(1, 1)], [(0, 1), (2, -1)], [(3, 1)], [(1, 1), (4, -1)], [(2, 1), (3, -1)], [(3, 1), (4, -1)],
           [(2, 1), (0, 'k'), (5, -1)], [(3, 1), (5, -1)], [(4, 1), (1, 'k'), (5, -1)])


def comps(N, al, plant=False):
    """(k, k^T) values of the blocks: '+' (e^{i al}, e^{-i al}), '-' (e^{-i al}, e^{i al}), and the axis (1, 1) at N = 4"""
    z = (acb(0, 1) * al).exp()
    zi = 1 / z
    c = [(z, z if plant else zi), (zi, z)]
    return c + [(acb(1), acb(1))] if N == 4 else c


def Q_block(kap, kapT):
    Q = zeros(6)
    for parts in PARTS_Q:
        cs = [(v, (-kap if c == 'k' else acb(c)), (-kapT if c == 'k' else acb(c))) for v, c in parts]
        for (u, cu, cuT) in cs:
            for (v, cv, cvT) in cs:
                Q[u, v] = Q[u, v] + cuT * cv
    return Q


def B_blocks(kap, kapT):
    h = acb(arb(1) / 2)
    Bs = []
    for v in range(6):
        B = zeros(6)
        B[v, v] = 1
        Bs.append(B)
    for (i, j, cij, cji) in ((2, 5, h, h), (0, 5, kapT * h, kap * h), (4, 5, h, h), (1, 5, kapT * h, kap * h)):
        B = zeros(6)
        B[i, j], B[j, i] = cij, cji
        Bs.append(B)
    return Bs


def trace(M):
    s = acb(0)
    for i in range(M.nrows()):
        s += M[i, i]
    return s


# ------------------------------------------------------------------ GFMom (pk10 gfmom.py's recursion; twcert's gfmom), blocks summed
def gfmom_lists(BC, D):
    """BC[f] = list of square acb matrices (the blocks of B_f C); traces are summed over the list"""
    F = len(BC)
    unit = [tuple(1 if i == f else 0 for i in range(F)) for f in range(F)]
    A = {unit[f]: BC[f] for f in range(F)}
    Fl = {1: {unit[f]: sum((trace(M) for M in BC[f]), acb(0)) for f in range(F)}}
    for m in range(2, D + 1):
        new = {}
        for e, Am in A.items():
            for f in range(F):
                e2 = tuple(x + (1 if i == f else 0) for i, x in enumerate(e))
                P = [Ab * Bb for Ab, Bb in zip(Am, BC[f])]
                new[e2] = [x + y for x, y in zip(new[e2], P)] if e2 in new else P
        A = new
        cf = arb(2) ** m / (2 * m)
        Fl[m] = {e: cf * sum((trace(M) for M in Am), acb(0)) for e, Am in A.items()}
    Ms = [{Z0: acb(1)}]
    for kk in range(1, D + 1):
        acc = {}
        for j in range(1, kk + 1):
            for e1, c1 in Fl[j].items():
                for e2, c2 in Ms[kk - j].items():
                    e = tuple(x + y for x, y in zip(e1, e2))
                    v = j * c1 * c2
                    acc[e] = acc[e] + v if e in acc else v
        Ms.append({e: v / kk for e, v in acc.items()})
    mom = {}
    for kk in range(D + 1):
        for e, v in Ms[kk].items():
            fe = 1
            for x in e:
                fe *= math.factorial(x)
            mom[e] = v * fe
    return mom


def pe(P, mom):
    s = acb(0)
    for e, c in P.items():
        s += c * mom[e]
    return s


def posre(d, what):
    if not (d.real > 0):
        raise NotCert(what)
    return d


def det_blocks(N, al, plant=False):
    d = acb(1)
    for (kap, kapT) in comps(N, al, plant):
        d = d * Q_block(kap, kapT).det()
    return d


def det_Q(N, al):
    return [det_blocks(N, al)]


def moments_at(N, al, plant=False):
    """(w, det Q_k, E_k H1, E_k P2, E_k E3) at al (acb); al None = the N = 3 reflection (full matrices)"""
    if al is None:
        k, w = kw(N, None)
        Q = Qmat2(k)
        det = Q.det()
        C = Q.inv()
        BC = [[Bf * C] for Bf in forms2(k)]
    else:
        w = kw(N, al)[1]
        det, BC = acb(1), [[] for _ in range(NF)]
        for (kap, kapT) in comps(N, al, plant):
            Qb = Q_block(kap, kapT)
            det = det * Qb.det()
            Cb = Qb.inv()
            for f, Bb in enumerate(B_blocks(kap, kapT)):
                BC[f].append(Bb * Cb)
    mom = gfmom_lists(BC, 6)
    return w, det, pe(PH1, mom), pe(PP2, mom), pe(PE3, mom)


def moments_full(N, al):
    """the same quantities from the full 6n x 6n matrices (for C-BLOCK)"""
    k, w = kw(N, al)
    Q = Qmat2(k)
    C = Q.inv()
    mom = gfmom_lists([[Bf * C] for Bf in forms2(k)], 6)
    return w, Q.det(), pe(PH1, mom), pe(PP2, mom), pe(PE3, mom)


def ev_mom(N, al):
    w, det, e1, e2, e3 = moments_at(N, al)
    a = w * posre(det, 'det Q').rsqrt()
    return [a, a * e1, a * e2, a * e3]


# ------------------------------------------------------------------ pref (s4c_m1c)
AEX = (3 + arb(21).sqrt()) / 6
BEX = (3 * arb(5).sqrt() - arb(21).sqrt()) / 12


def strip_graph(ncols, a, b):
    E = {}
    for j in range(ncols):
        T, Mv, B = 3 * j, 3 * j + 1, 3 * j + 2
        if j == 0 or j == ncols - 1:
            E[(T, Mv)] = a
            E[(Mv, B)] = a
            if b > 0:
                E[(T, B)] = b
        else:
            E[(T, Mv)] = arb(1)
            E[(Mv, B)] = arb(1)
        if j < ncols - 1:
            for r in range(3):
                E[(3 * j + r, 3 * (j + 1) + r)] = arb(1)
    return 3 * ncols, E


def pref_arb(N):
    def detred(ncols):
        V, Ed = strip_graph(ncols, AEX, BEX)
        L = arb_mat(V, V)
        for (u, v), c in Ed.items():
            L[u, u] += c
            L[v, v] += c
            L[u, v] -= c
            L[v, u] -= c
        S = arb_mat(V - 1, V - 1)
        for i in range(V - 1):
            for j in range(V - 1):
                S[i, j] = L[i + 1, j + 1]
        return S.det()
    return (detred(3) / detred(2)) ** (arb(N - 1) / 2)


# ------------------------------------------------------------------ boxes, cover, G, node sums (s4c_m1c)
def xball(u0, u1):
    return (PI * u0.numerator / u0.denominator).union(PI * u1.numerator / u1.denominator)


def yball(v0, v1, sig):
    s = arb(sig)
    return (s * v0.numerator / v0.denominator).union(s * v1.numerator / v1.denominator)


def cover(N, sig, detfn, dmax):
    todo = [(Fr(2 * i, KX), Fr(2 * (i + 1), KX), Fr(2 * j, KY) - 1, Fr(2 * (j + 1), KY) - 1, 0) for i in range(KX) for j in range(KY)]
    nbox = 0
    while todo:
        u0, u1, v0, v1, dp = todo.pop()
        try:
            ok = all(d.real > 0 for d in detfn(N, acb(xball(u0, u1), yball(v0, v1, sig))))
        except (ZeroDivisionError, ValueError):
            ok = False
        if ok:
            nbox += 1
            continue
        if dp >= dmax:
            return False, nbox, (u0, u1, v0, v1, dp)
        if (u1 - u0) * math.pi >= (v1 - v0) * sig:
            um = (u0 + u1) / 2
            todo += [(u0, um, v0, v1, dp + 1), (um, u1, v0, v1, dp + 1)]
        else:
            vm = (v0 + v1) / 2
            todo += [(u0, u1, v0, vm, dp + 1), (u0, u1, vm, v1, dp + 1)]
    return True, nbox, None


def ladder(N, sigs, detfn, dmax):
    for sig in sigs:
        t0 = cpu()
        ok, nb, bad = cover(N, sig, detfn, dmax)
        if ok:
            return sig, nb, cpu() - t0
    return None, 0, 0.0


def maxup(xs):
    m = xs[0]
    for x in xs[1:]:
        m = m.max(x)
    return m.upper()


def gbound(N, fn, sig, M, n):
    den = (arb(sig) * M).exp() - 1
    y = arb(sig)
    st = [0, 0]

    def evseg(u0, u1, dp, acc):
        todo = [(u0, u1, dp)]
        while todo:
            a0, a1, d = todo.pop()
            st[0] += 1
            try:
                av = [z.abs_upper() for z in fn(N, acb(xball(a0, a1), y))]
                okv = all(z.is_finite() for z in av)
            except (NotCert, ZeroDivisionError, ValueError):
                okv = False
            if okv:
                acc.append((a0, a1, d, av))
                continue
            st[1] += 1
            if d >= GDMAX:
                raise NotCert('G box x in [%s, %s] pi, y = %g failed at depth %d' % (a0, a1, sig, d))
            am = (a0 + a1) / 2
            todo += [(a0, am, d + 1), (am, a1, d + 1)]
    boxes = []
    for i in range(K0):
        evseg(Fr(i, K0), Fr(i + 1, K0), 0, boxes)
    while True:
        G = [maxup([b[3][i] for b in boxes]) for i in range(n)]
        err = [(2 * G[i] / den).upper() for i in range(n)]
        bad = [i for i in range(n) if not (err[i] <= TOL)]
        if not bad or len(boxes) >= BMAX:
            break
        i = bad[0]
        j = max(range(len(boxes)), key=lambda q: float(boxes[q][3][i]))
        a0, a1, d, av = boxes[j]
        if d >= GDMAX:
            break
        boxes.pop(j)
        am = (a0 + a1) / 2
        evseg(a0, am, d + 1, boxes)
        evseg(am, a1, d + 1, boxes)
    return G, err, len(boxes), st[0], st[1]


def integral(N, sig, M, fn, names, fails):
    n = len(names)
    t0 = cpu()
    full = [fn(N, acb(PI * (2 * k) / M)) for k in range(M // 2 + 1)]
    vals = [[z.real for z in v] for v in full]
    TM = [(vals[0][i] + vals[M // 2][i] + 2 * sum(vals[k][i] for k in range(1, M // 2))) / M for i in range(n)]
    TH = [(vals[0][i] + vals[M // 2][i] + 2 * sum(vals[k][i] for k in range(2, M // 2, 2))) * 2 / M for i in range(n)]
    tn = cpu() - t0
    ev_ok = True
    for k in (1, M // 4):
        mir = fn(N, acb(PI * (2 * (M - k)) / M))
        ev_ok = ev_ok and all(x.overlaps(z) for x, z in zip(full[k], mir))
    up, dn = fn(N, acb(PI / 3, arb(sig))), fn(N, acb(PI / 3, -arb(sig)))
    cj_ok = all(x.overlaps(z.conjugate()) for x, z in zip(up, dn))
    t1 = cpu()
    G, err, nb, nev, nfail = gbound(N, fn, sig, M, n)
    tg = cpu() - t1
    errh = [(2 * G[i] / ((arb(sig) * (M // 2)).exp() - 1)).upper() for i in range(n)]
    half_ok = all((TM[i] + (-err[i]).union(err[i])).overlaps(TH[i] + (-errh[i]).union(errh[i])) for i in range(n))
    Js = [TM[i] + (-err[i]).union(err[i]) for i in range(n)]
    if N == 3:
        rv = fn(N, None)
        Js = [Js[i] + rv[i].real / 2 for i in range(n)]
    out('INT N=%d: sigma %g, M %d (%d nodes, %.1f s); G on %d boxes (%d evaluations, %d failed, %.1f s); C-EVEN %s, C-CONJ %s, C-HALF %s'
        % (N, sig, M, M // 2 + 1, tn, nb, nev, nfail, tg, 'PASS' if ev_ok else 'FAIL', 'PASS' if cj_ok else 'FAIL', 'PASS' if half_ok else 'FAIL'))
    for i in range(n):
        out('  N=%d %s: %s; T_M %s, T_M/2 %s, G %s, error %s' % (N, names[i], Js[i].str(15), TM[i].str(15), TH[i].str(15), G[i].str(4),
                                                              err[i].str(4)))
    for ok, nm in ((ev_ok, 'C-EVEN'), (cj_ok, 'C-CONJ'), (half_ok, 'C-HALF')):
        if not ok:
            fails.append('%s N=%d' % (nm, N))
    return Js


# ------------------------------------------------------------------ group (b) (S4_M2_DESIGN_v3)
SIG_B, M_B = 0.5, 64
KN = M_B // 2
NODE_SETS = {'nodes0': list(range(0, 16)), 'nodes1': list(range(16, KN + 1))}
EVEN_K = {'nodes0': 1, 'nodes1': M_B // 4}
G_SETS = {'g0': (Fr(0), Fr(1, 2)), 'g1': (Fr(1, 2), Fr(1))}
# ==== NODE CORE A END ====
# m3: parameters (S4_M3_DESIGN_v1; scan px08_m3scan_v1)
THETAS = (Fr(17, 20), Fr(7, 10), Fr(1, 2))      # tried in this order per family; the first one C-PROP certifies is used
EPS_SH_F = 0.65
GRID_M3 = 257
SIGS_M3 = (0.5, 0.375, 0.25)
M_OF = {0.5: 64, 0.375: 88, 0.25: 128}
PROP_K, PROP_DEPTH, PROP_MAXEV = 32, 8, 2048
G_K3, G_DSUB3, G_DEPTH3 = 32, 8, 2
J_REF = 300
NODE_SHA = 'd5e1aeea75ad11f94864d1c2297c22a9f9038cf8db64689f2c25bc536c167cbe'   # nodes0/nodes1 outputs of v1 are reused (node code unchanged)
# ==== NODE CORE B BEGIN (s4c_m2bb.py lines 638-836, byte for byte) ====
X6F = FORMS2[:6]
AV_A = [arb(1) / 5, arb(1) / 5] + [arb(3) / 10] * 4
AV_F = [0.2, 0.2, 0.3, 0.3, 0.3, 0.3]
T_A, T_F, EPS_A, EPS_F = arb(1) / 300, 1.0 / 300, arb(35) / 100, 0.35
EJ_M0, SPLIT = 400, 3
HBAR_TOL, PORT_TOL, FLT_TOL = 1e-12, 1e-13, 1e-9


def apadd(*Ps):
    o = {}
    for P in Ps:
        for e, c in P.items():
            o[e] = o[e] + c if e in o else c
    return o


def apmul(P, Q):
    o = {}
    for e1, c1 in P.items():
        for e2, c2 in Q.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            o[e] = o[e] + c1 * c2 if e in o else c1 * c2
    return o


def apscale(P, c):
    return {e: c * v for e, v in P.items()}


def fr2a(c):
    return arb(c.numerator) / c.denominator


_EJ = {}


def ej_arb(j, x):
    """Ej(j, x) = sum_{m >= j+1} cm(m) (m-1)!/(m-1-j)! x^{m-1-j}: the sum to m < EJ_M0 plus [0, T_M0/(1 - r)], r = x M0/(M0 - j), which
    bounds every later term ratio ((2m-1)/(2m+2) m/(m-j) x <= r) (V7)"""
    key = (j, float(x.mid()))
    if key not in _EJ:
        s = arb(0)
        for m in range(j + 1, EJ_M0):
            s += fr2a(cm_fr(m)) * math.perm(m - 1, j) * x ** (m - 1 - j)
        r = x * EJ_M0 / (EJ_M0 - j)
        assert r < 1
        tail = (fr2a(cm_fr(EJ_M0)) * math.perm(EJ_M0 - 1, j) * x ** (EJ_M0 - 1 - j) / (1 - r)).upper()
        _EJ[key] = s + arb(0).union(tail)
    return _EJ[key]


def cj_arb(j, x):
    df = 1
    for q in range(2 * j - 3, 0, -2):
        df *= q
    return arb(df) / 2 ** j * (1 - x).sqrt() / (1 - x) ** j


def mono6(**kw_):
    e = [0] * 6
    for f, p in kw_.items():
        e[X6F.index(f)] += p
    return tuple(e)


def hbar_arb(j, av, t):
    """arb port of twlib2.hbar2 (l.145-186), term by term; Zbar(0) in closed form t (1 - a/2 - sqrt(1 - a))/a^2 (V7); no term dropped"""
    A = dict(zip(X6F, av))
    f = math.factorial
    P = {}
    for v in X6F:
        P = apadd(P, {mono6(**{v: j}): arb(f(j - 1)) / (2 * (1 - A[v]) ** j)})
    for v in ROOT_BONDS:
        P = apadd(P, {mono6(**{v: j + 1}): ej_arb(j, A[v])})

    def D2(u, v):
        return {mono6(**{u: 2}): arb(1), mono6(**{u: 1, v: 1}): arb(-2), mono6(**{v: 2}): arb(1)}

    def Mk(u, v, kk):
        return {mono6(): arb(1)} if kk == 0 else apadd({mono6(**{u: kk}): arb(1)}, {mono6(**{v: kk}): arb(1)})

    def Abar(u, v, i):
        ae = A[u] if A[u] > A[v] else A[v]
        if i == 0:
            return apscale(D2(u, v), t / 2 / (4 * (1 - ae)))
        return apscale(apmul(D2(u, v), Mk(u, v, i - 1)), arb(f(i)) / 2 / (4 * (1 - ae) ** (i + 1)))

    def Zbar(i):
        if i == 0:
            a = A['Z']
            return {mono6(Z=2): t * (1 - a / 2 - (1 - a).sqrt()) / (a * a)}
        return {mono6(Z=i + 1): ej_arb(i, A['Z'])}
    for (u, v) in PAIR_BONDS:
        P = apadd(P, Abar(u, v, j))
    for (x, xp, a_, b_) in TWISTED:
        P = apadd(P, Abar(x, xp, j), Zbar(j))
        if j == 1:
            P = apadd(P, {mono6(**{x: 1, 'Z': 1}): arb(1) / 4}, {mono6(**{xp: 1, 'Z': 1}): arb(1) / 4})
        sx = apadd({mono6(**{x: 1}): arb(1) / 2}, {mono6(**{xp: 1}): arb(1) / 2})
        G1 = lambda i: apmul(sx, Zbar(i))
        G2 = lambda i: apmul({mono6(Z=1): arb(1) / 2}, Abar(x, xp, i))
        G3 = lambda i: apadd(*[apscale(apmul(Abar(x, xp, l), Zbar(i - l)), math.comb(i, l)) for l in range(i + 1)])
        for G in (G1, G2, G3):
            P = apadd(P, apscale(G(j), t), apscale(G(j - 1), j))
        P = apadd(P, {mono6(**{x: j, xp: 1}): cj_arb(j, A[x]) / 2}, {mono6(**{x: j, 'Z': 1}): cj_arb(j, A[x]) / 2})
        P = apadd(P, {mono6(**{xp: j, x: 1}): cj_arb(j, A[xp]) / 2}, {mono6(**{xp: j, 'Z': 1}): cj_arb(j, A[xp]) / 2})
        P = apadd(P, {mono6(**{x: 1, 'Z': j}): cj_arb(j, A['Z']) / 2}, {mono6(**{xp: 1, 'Z': j}): cj_arb(j, A['Z']) / 2})
    return P


HX = H_series_exact(3)
_H1sq = pmul(HX[1], HX[1])
_E2 = padd(HX[2], pscale(_H1sq, Fr(1, 2)))
P10 = [to_arb({Z0: Fr(1)}), to_arb(_H1sq), to_arb(pmul(_H1sq, _H1sq)), to_arb(pmul(HX[2], HX[2])), to_arb(pmul(HX[3], HX[3])),
       to_arb(pmul(_E2, _E2))]
N10 = ['1', 'H1^2', 'H1^4', 'H2^2', 'H3^2', 'E2^2']
HB = {j: hbar_arb(j, AV_A, T_A) for j in (2, 3, 4)}
HLO = {e: c for e, c in HB[2].items() if sum(e) <= SPLIT}
HHI = {e: c for e, c in HB[2].items() if sum(e) > SPLIT}
_hlo2 = apmul(HLO, HLO)
P6 = [HB[4], apmul(HB[3], HB[3]), apmul(HB[2], HB[2]), apmul(_hlo2, _hlo2)]
N6 = ['hbar4', 'hbar3^2', 'hbar2^2', 'h_lo^4']
V1M = sorted({(v, 4 * sum(e)) for e in HHI for v in range(6) if e[v]})
NAMES = N10 + N6 + ['%s^%d' % (X6F[v], m) for v, m in V1M] + ['(E H2^2)^2', '(E H1^2)^3']
NV = len(NAMES)


def fixz(m, F):
    m[(0,) * F] = m.pop(Z0)
    return m


def tables(N, al):
    """(w, det, [E_k P for P in NAMES]) at al (acb), al None = the N = 3 reflection (full matrices)"""
    if al is None:
        k, w = kw(N, None)
        Q = Qmat2(k)
        det, C = Q.det(), Q.inv()
        BC = [[Bf * C] for Bf in forms2(k)]
    else:
        w, det, BC = kw(N, al)[1], acb(1), [[] for _ in range(NF)]
        for (kap, kapT) in comps(N, al):
            Qb = Q_block(kap, kapT)
            det = det * Qb.det()
            Cb = Qb.inv()
            for f, Bb in enumerate(B_blocks(kap, kapT)):
                BC[f].append(Bb * Cb)
    m10 = gfmom_lists(BC, 8)
    m6 = fixz(gfmom_lists(BC[:6], 12), 6)
    m1 = {v: fixz(gfmom_lists([BC[v]], 20), 1) for v in sorted({v for v, m in V1M})}
    e = [pe(P, m10) for P in P10] + [pe(P, m6) for P in P6] + [m1[v][(m,)] for v, m in V1M]
    return w, det, e + [e[3] * e[3], e[1] ** 3]


def ev_node(N, al):
    w, det, e = tables(N, al)
    a = w * posre(det, 'det Q').rsqrt()
    return [(a * x).real for x in e]


def ev_g(N, al):
    """upper bounds of |w det^{-1/2} E[P]| on a box: |det^{-1/2}| = |det|^{-1/2} on every branch; analyticity from C-COVER"""
    w, det, e = tables(N, al)
    ad = det.abs_lower()
    if not (ad > 0):
        raise NotCert('det enclosure meets 0')
    a = w.abs_upper() / ad.sqrt()
    return [(a * x.abs_upper()).upper() for x in e]


def ex(x):
    m, e = x.man_exp()
    return '%s %s' % (m, e)


def unex(m, e):
    e = int(e)
    return arb(fmpz(m)) * arb(2) ** e if e >= 0 else arb(fmpz(m)) / arb(2) ** (-e)


def node_line(tag, v):
    return 'NODE %s %s' % (tag, ' '.join('%s %s' % (ex(x.lower()), ex(x.upper())) for x in v))


def run_nodes(N):
    keep = {}
    for k in NODE_SETS[PART]:
        STAGE[0] = 'node %d' % k
        keep[k] = ev_node(N, acb(PI * (2 * k) / M_B))
        out(node_line(str(k), keep[k]))
    k = EVEN_K[PART]
    STAGE[0] = 'C-EVEN'
    mir = ev_node(N, acb(PI * (2 * (M_B - k)) / M_B))
    out('CHECK C-EVEN k=%d %s' % (k, 'PASS' if all(x.overlaps(y) for x, y in zip(keep[k], mir)) else 'FAIL'))
    if PART == 'nodes0' and N == 3:
        STAGE[0] = 'reflection'
        out(node_line('refl', ev_node(N, None)))


# ==== NODE CORE B END ====


# ------------------------------------------------------------------ m3: the matrix families (S4_M3_DESIGN_v1; CHECK f38d2b57)
TT = T_A                                                    # t = 1/300
AVP_A = [arb(45) / 100] * 2 + [arb(55) / 100] * 4           # sp0's annulus outer radii^2
AVP_F = [0.45, 0.45, 0.55, 0.55, 0.55, 0.55]
NSH = 3
SH_A = [[AV_A[v] + (AVP_A[v] - AV_A[v]) * (s + 1) / NSH for v in range(6)] for s in range(NSH)]
SH_F = [[AV_F[v] + (AVP_F[v] - AV_F[v]) * (s + 1) / NSH for v in range(6)] for s in range(NSH)]
PREV_A = [AV_A] + SH_A[:-1]
EPS_SH = arb(65) / 100


def fam_name(fam):
    kind, s, v = fam
    return '%s%s v%d' % (kind, '' if s is None else str(s + 1), v)


def families(part):
    if part == 'tail':
        return [('tail', None, v) for v in range(6)]
    if part in ('sh1', 'sh2', 'sh3'):
        return [('ann', int(part[2]) - 1, v) for v in range(6)]
    if part in ('sh1a', 'sh2a', 'sh3a'):
        return [('ann', int(part[2]) - 1, v) for v in range(3)]
    if part in ('sh1b', 'sh2b', 'sh3b'):
        return [('ann', int(part[2]) - 1, v) for v in range(3, 6)]
    return [('far', None, v) for v in range(6)]


def cfun_f(x):
    return -math.log(1 - x) / (2 * x)


def fam_float(fam, kn):
    """(the unshifted float matrix, the float B_v) of a family at the numpy k (twlib2.mats, twlib2.tilt2)"""
    kind, s, v = fam
    Qf_, Bsf, Qnt_ = T2.mats(kn)
    if kind == 'tail':
        A = Qf_
    elif kind == 'ann':
        A = Qf_ - 2 * T2.tilt2(kn, T_F, SH_F[s], EPS_SH_F)
    else:
        A = Qnt_ - 2 * cfun_f(0.96) * T_F * np.eye(Qnt_.shape[0])
    return A, Bsf[v]


def lam_of(N, fam, theta):
    """lam = theta / (2 Lmax), rounded down to a multiple of 1e-6 (an exact Fraction); Lmax = the largest eigenvalue of the v-block of the
    inverse of the unshifted float matrix over GRID_M3 al-points on [0, pi] and the N = 3 reflection (the far matrix is constant)"""
    n = 3 if N == 4 else 2
    v = fam[2]
    als = [0.0] if fam[0] == 'far' else [math.pi * i / (GRID_M3 - 1) for i in range(GRID_M3)] + ([None] if N == 3 else [])
    L = 0.0
    for al in als:
        A, B = fam_float(fam, k_np_of(N, al))
        C = np.linalg.inv(A)
        L = max(L, float(np.linalg.eigvalsh(C[v * n:(v + 1) * n, v * n:(v + 1) * n]).max()))
    return Fr(math.floor(float(theta) / (2 * L) * 10 ** 6), 10 ** 6), L


def fr_arb(q):
    return arb(q.numerator) / q.denominator


def T_block_g(kap, kapT, t, av, eps):
    """twlib2.tilt2 at (t, av, eps) in the 6 x 6 block form of Q_block (as px08_m2bc2's T_block, with parameters)"""
    T = zeros(6)
    for v in range(6):
        T[v, v] = T[v, v] + acb(t * cfun_a(av[v]))
    for parts in (PARTS_Q[7], PARTS_Q[9]):
        cs = [(v, (-kap if c == 'k' else acb(c)), (-kapT if c == 'k' else acb(c))) for v, c in parts]
        for (u, cu, cuT) in cs:
            for (v, cv, cvT) in cs:
                T[u, v] = T[u, v] + cuT * cv * acb(eps / 2)
    for (vr, vp) in ((0, 2), (1, 4)):
        a, aZ = av[vr], av[5]
        dk = 1 - (1 - a).sqrt() + (a * aZ).sqrt() / (1 + (1 - aZ).sqrt())
        T[5, 5] = T[5, 5] + acb((1 / eps - 1) * dk * dk / 2)
    return T


def qnt_block():
    """the 6 x 6 block of Qnt (twlib2.mats: Q without the two twisted bonds); Qnt = this block on each of the n components"""
    Q = zeros(6)
    for parts in ([(0, 1)], [(1, 1)], [(0, 1), (2, -1)], [(3, 1)], [(1, 1), (4, -1)], [(2, 1), (3, -1)], [(3, 1), (4, -1)], [(3, 1), (5, -1)]):
        for (u, cu) in parts:
            for (v, cv) in parts:
                Q[u, v] = Q[u, v] + cu * cv
    return Q


def qnt_full(n):
    I, mI = eye(n), eye(n) * (-1)
    Q = zeros(6 * n)
    for parts in ([(0, I)], [(1, I)], [(0, I), (2, mI)], [(3, I)], [(1, I), (4, mI)], [(2, I), (3, mI)], [(3, I), (4, mI)], [(3, I), (5, mI)]):
        gram(Q, n, parts)
    return Q


def fam_block(fam, lam, kap, kapT, plant=False):
    """the 6 x 6 block of the family's matrix for the eigenvalue pair (kap, kapT) of k; lam an arb. plant=True adds 1e-10 to entry (0, 0)"""
    kind, s, v = fam
    if kind == 'far':
        Q = qnt_block() - eye(6) * acb(2 * cfun_a(arb(96) / 100) * TT)
    else:
        Q = Q_block(kap, kapT)
        if kind == 'ann':
            Q = Q - T_block_g(kap, kapT, TT, SH_A[s], EPS_SH) * 2
    Q[v, v] = Q[v, v] - acb(2 * lam)
    if plant:
        Q[0, 0] = Q[0, 0] + acb(arb('1e-10'))
    return Q


def fam_full(fam, lam, k):
    """the family's full 6n x 6n matrix at k (acb_mat)"""
    kind, s, v = fam
    n = k.nrows()
    if kind == 'far':
        Q = qnt_full(n) - eye(6 * n) * acb(2 * cfun_a(arb(96) / 100) * TT)
    else:
        Q = Qmat2(k)
        if kind == 'ann':
            Q = Q - tilt2_full(k, TT, SH_A[s], EPS_SH) * 2
    return Q - forms2(k)[v] * acb(2 * lam)


def det_fam(N, fam, lam, al):
    d = acb(1)
    for (kap, kapT) in comps(N, al):
        d = d * fam_block(fam, lam, kap, kapT).det()
    return d


def ldlt(A):
    """interval LDL^T of the symmetric matrix A (rows of arb; the lower triangle is used): the pivots (D entries, D6), or None at the first
    pivot that is not certainly > 0. Success proves every symmetric matrix with entries in A positive definite (inclusion)"""
    n = len(A)
    L = [[arb(0)] * n for _ in range(n)]
    D = []
    for j in range(n):
        s = A[j][j]
        for q in range(j):
            s = s - L[j][q] * L[j][q] * D[q]
        if not (s > 0):
            return None
        D.append(s)
        for i in range(j + 1, n):
            r = A[i][j]
            for q in range(j):
                r = r - L[i][q] * L[j][q] * D[q]
            L[i][j] = r / s
    return D


def minlow(D):
    m = D[0].lower()
    for x in D[1:]:
        m = x.lower() if x.lower() < m else m
    return m


def zrad(z):
    return z.real.rad().max(z.imag.rad())


def dndec(x, sig=12):
    """a decimal string <= x (W1), from the exact lower end"""
    m, e = x.lower().man_exp()
    u = Fr(int(m)) * Fr(2) ** int(e)
    if u == 0:
        return '0'
    return _dec(u, sig, True) if u > 0 else '-' + _dec(-u, sig, False)


def real_full(N, fam, lam, al):
    """the family's full real matrix at a real al (an arb point or interval), or at the N = 3 reflection (al None), as rows of arb"""
    k = kw(N, None)[0] if al is None else kw(N, acb(al))[0]
    Q = fam_full(fam, lam, k)
    return [[Q[i, j].real for j in range(Q.ncols())] for i in range(Q.nrows())]


def cprop_fam(N, fam, lam):
    """C-PROP for one family: interval LDL^T on al-intervals tiling [0, pi] (halved on failure; stop rule: a failure at depth PROP_DEPTH or
    more than PROP_MAXEV evaluations is a FAIL) and at the N = 3 reflection; the far matrix is constant: one LDL^T.
    Returns (ok, intervals, smallest pivot lower end, the interval of the smallest pivot or the reason of the stop)"""
    if fam[0] == 'far':
        D = ldlt(real_full(N, fam, lam, arb(0)))
        return D is not None, 1, (minlow(D) if D is not None else None), 'constant'
    todo = [(Fr(i, PROP_K), Fr(i + 1, PROP_K), 0) for i in range(PROP_K)]
    nint, nev, dmin, where = 0, 0, None, None
    while todo:
        if nev >= PROP_MAXEV:
            return False, nint, dmin, 'PROP-STOP: more than %d evaluations' % PROP_MAXEV
        u0, u1, d = todo.pop()
        nev += 1
        D = ldlt(real_full(N, fam, lam, xball(u0, u1)))
        if D is None:
            if d >= PROP_DEPTH:
                return False, nint, dmin, 'PROP-STOP: x in [%s, %s] pi failed at depth %d' % (u0, u1, d)
            um = (u0 + u1) / 2
            todo += [(u0, um, d + 1), (um, u1, d + 1)]
            continue
        nint += 1
        m = minlow(D)
        if dmin is None or m < dmin:
            dmin, where = m, (u0, u1)
    if N == 3 and ldlt(real_full(N, fam, lam, None)) is None:
        return False, nint, dmin, 'the reflection failed'
    return True, nint, dmin, where


def plant_prop_fam(N, fam, lam, where):
    """PLANT-PROP (D6) at the point of the smallest pivot: c = min_j (upper end of pivot j) >= lambda_min, so the matrix minus 2 c I is
    indefinite and its LDL^T must fail. True when it fails as it must"""
    if fam[0] == 'far':
        al = arb(0)
    else:
        u = (where[0] + where[1]) / 2
        al = PI * u.numerator / u.denominator
    A = real_full(N, fam, lam, al)
    D = ldlt(A)
    if D is None:
        return False
    c = D[0].upper()
    for x in D[1:]:
        c = x.upper() if x.upper() < c else c
    return ldlt([[A[i][j] - (2 * c if i == j else 0) for j in range(len(A))] for i in range(len(A))]) is None


def node_val(N, fam, lam, al):
    return kw(N, al)[1] * posre(det_fam(N, fam, lam, al), 'det ' + fam_name(fam)).rsqrt()


def tw_fam(N, fam, lam, sig, M):
    """TW on the M nodes (k = 0..M/2, evenness) of w det^{-1/2}, the half rule, C-EVEN (k = 1), C-CONJ (pi/3 +- i sig), and the N = 3
    reflection value det^{-1/2}"""
    K = M // 2
    vals = [node_val(N, fam, lam, acb(PI * (2 * k) / M)).real for k in range(K + 1)]
    TM = (vals[0] + vals[K] + 2 * sum(vals[1:K], arb(0))) / M
    TH = (vals[0] + vals[K] + 2 * sum((vals[k] for k in range(2, K, 2)), arb(0))) * 2 / M
    ceven = vals[1].overlaps(node_val(N, fam, lam, acb(PI * (2 * (M - 1)) / M)).real)
    up, dn = node_val(N, fam, lam, acb(PI / 3, arb(sig))), node_val(N, fam, lam, acb(PI / 3, -arb(sig)))
    cconj = up.overlaps(dn.conjugate())
    refl = posre(fam_full(fam, lam, kw(N, None)[0]).det(), 'det refl').rsqrt().real if N == 3 else None
    return TM, TH, ceven, cconj, refl


def det_lower_fam(N, fam, lam, u0, u1, y, plant=False):
    """the minimum over G_DSUB3 sub-boxes of prod_b abs_lower(block det); plant=True widens the first block det of the first sub-box to
    contain 0 (PLANT-DET)"""
    lo = None
    for i in range(G_DSUB3):
        al = acb(xball(u0 + (u1 - u0) * i / G_DSUB3, u0 + (u1 - u0) * (i + 1) / G_DSUB3), y)
        p = arb(1)
        for b, (kap, kapT) in enumerate(comps(N, al)):
            d = fam_block(fam, lam, kap, kapT).det()
            if plant and i == 0 and b == 0:
                d = acb(d.real.union(arb(0)), d.imag.union(arb(0)))
            p = p * (d.abs_lower() if d.is_finite() else arb(0))
        p = p.lower()
        lo = p if (lo is None or p < lo) else lo
    return lo


def g_fam(N, fam, lam, sig, plant=False, nbox=None):
    """G = the largest |w| det_lower^{-1/2} over boxes of width pi/G_K3 on Im al = sig over [0, pi] (nbox boxes from the left if given),
    halved on failure to depth G_DEPTH3; a failure at that depth is a G-STOP. Returns (G, boxes)"""
    y = arb(sig)
    todo = [(Fr(i, G_K3), Fr(i + 1, G_K3), 0) for i in range(G_K3 if nbox is None else nbox)]
    G, nb = arb(0), 0
    while todo:
        u0, u1, d = todo.pop(0)
        dlo = det_lower_fam(N, fam, lam, u0, u1, y, plant)
        a = (kw(N, acb(xball(u0, u1), y))[1].abs_upper() / dlo.sqrt()).upper() if dlo > 0 else None
        if a is None or not a.is_finite():
            if d >= G_DEPTH3:
                raise NotCert('G-STOP: %s box [%s, %s] pi failed at depth %d' % (fam_name(fam), u0, u1, d))
            um = (u0 + u1) / 2
            todo = [(u0, um, d + 1), (um, u1, d + 1)] + todo
            continue
        G = G.max(a)
        nb += 1
    return G.upper(), nb


def plant_strip_fam(N, fam, lam, sig):
    """m1c's PLANT-STRIP on the family's det: F_p' = det (cosh(c sigma) - cos al), c = 3/4, negative at al = i (1 + c) sigma/2"""
    c = arb(3) / 4
    ch = (c * arb(sig)).cosh()
    fp = lambda N_, al: [det_fam(N_, fam, lam, al) * (ch - al.cos())]
    neg_ok = fp(N, acb(0, (1 + c) * arb(sig) / 2))[0].real < 0
    ok, nb, bad = cover(N, sig, fp, CDMAX)
    return neg_ok and ok is False and bad is not None


def c_block_m(N, fam, lam, plant=False):
    """C-BLOCK-M: the product of the block dets against det of the full matrix, at al = 0.7, 2.3 and 0.3 + 0.2i (the far matrix: at one
    point, i.e. det(block)^n against det(full)); overlap with radii <= 1e-20 relative. plant=True moves one entry of the first block"""
    pts = [acb(0)] if fam[0] == 'far' else [acb(arb(7) / 10), acb(arb(23) / 10), acb(arb(3) / 10, arb(2) / 10)]
    ok = True
    for al in pts:
        dprod = acb(1)
        for b, (kap, kapT) in enumerate(comps(N, al)):
            dprod = dprod * fam_block(fam, lam, kap, kapT, plant and b == 0).det()
        dfull = fam_full(fam, lam, kw(N, al)[0]).det()
        tight = zrad(dprod) <= dprod.abs_lower() / 10 ** 20 and zrad(dfull) <= dfull.abs_lower() / 10 ** 20
        ok = ok and tight and dprod.overlaps(dfull)
    return ok


def c_port_m(N, plant=False):
    """C-PORT-M: tilt2_full at t = 1/300 and the shell radii (eps 0.65) against twlib2.tilt2, entrywise, <= PORT_TOL max(1, |f|), at
    al = 0.7 and 2.3; plant=True moves one entry by 1e-10"""
    worst = 0.0
    for s in range(NSH):
        for al in (0.7, 2.3):
            Ta = tilt2_full(kw(N, acb(al))[0], TT, SH_A[s], EPS_SH)
            Tf = T2.tilt2(k_np_of(N, al), T_F, SH_F[s], EPS_SH_F)
            for i in range(Ta.nrows()):
                for j in range(Ta.ncols()):
                    a = Ta[i, j]
                    if plant and s == 0 and al == 0.7 and (i, j) == (0, 0):
                        a = a + acb(arb('1e-10'))
                    worst = max(worst, float((a - acb(float(Tf[i, j]))).abs_upper()) / max(1.0, abs(float(Tf[i, j]))))
    return worst <= PORT_TOL, worst


def c_flt_m(N, fams_lams):
    """C-FLT-M: each family's det (block product) at al = 0.7 and 2.3 (far: its one value) against numpy's det of the twlib2 matrix, each
    value against itself, |a - f| <= FLT_TOL |f| (dets are positive there). Returns (ok, worst, planted ok): PLANT-FLT-M moves the first
    value by 1e-7 relative and runs the same test"""
    av, fv = [], []
    for fam, lam in fams_lams:
        for al in ((0.0,) if fam[0] == 'far' else (0.7, 2.3)):
            A, B = fam_float(fam, k_np_of(N, al))
            fv.append(float(np.linalg.det(A - 2 * float(lam) * B)))
            av.append(float(det_fam(N, fam, fr_arb(lam), acb(al)).real.mid()))
    worst = max(abs(a - f) / abs(f) for a, f in zip(av, fv))
    avp = [av[0] * (1 + 1e-7)] + av[1:]
    worst_p = max(abs(a - f) / abs(f) for a, f in zip(avp, fv))
    return worst <= FLT_TOL, worst, worst_p <= FLT_TOL


def eval_family(N, fam, first):
    """one family: lam by theta (THETAS in order; the first theta whose matrix C-PROP certifies and, for an integrated family, whose cover
    ladder certifies, is used: M2), then TW, G and its checks; prints its FAMILY line (exact ends of its value) and its CHECK lines, each
    once; on the first family of the item also PLANT-PROP, PLANT-STRIP and PLANT-DET"""
    t0 = cpu()
    pok, sig, nb = False, None, 0
    for theta in THETAS:
        lam, L = lam_of(N, fam, theta)
        la = fr_arb(lam)
        ok, nint, dmin, where = cprop_fam(N, fam, la)
        wh = ('[%s, %s]' % where) if isinstance(where, tuple) else str(where)
        out('  %s: theta %s, lam %s (Lmax %.6g); C-PROP %s, %d intervals, smallest pivot >= %s on %s' % (
            fam_name(fam), theta, lam, L, 'PASS' if ok else 'FAIL', nint, dndec(dmin) if dmin is not None else '-', wh))
        if not ok:
            continue
        pok = True
        if fam[0] == 'far':
            break
        sig, nb, tc = ladder(N, SIGS_M3, lambda N_, al: [det_fam(N_, fam, la, al)], CDMAX)
        out('  %s: theta %s, cover ladder: %s' % (fam_name(fam), theta, ('sigma %g, %d boxes' % (sig, nb)) if sig else 'no sigma certified'))
        if sig:
            break
    out('CHECK C-PROP %s' % ('PASS' if pok else 'FAIL'))
    if not pok:
        raise NotCert('C-PROP failed for %s at every theta' % fam_name(fam))
    if fam[0] != 'far':
        out('CHECK C-COVER %s' % ('PASS' if sig else 'FAIL'))
        if not sig:
            raise NotCert('no sigma of the ladder certified for %s at any theta' % fam_name(fam))
    if first:
        out('CHECK PLANT-PROP %s' % ('FIRED' if plant_prop_fam(N, fam, la, where) else 'DID-NOT-FIRE'))
    if fam[0] == 'far':
        val = posre(fam_full(fam, la, kw(N, acb(0))[0]).det(), 'det far').rsqrt().real
        out('FAMILY far - %d %d %d %s %s' % (fam[2], lam.numerator, lam.denominator, ex(val.lower()), ex(val.upper())))
        out('  %s: det^{-1/2} in %s (%.1f s)' % (fam_name(fam), val.str(12), cpu() - t0))
        return fam, lam
    if first:
        out('CHECK PLANT-STRIP %s' % ('FIRED' if plant_strip_fam(N, fam, la, sig) else 'DID-NOT-FIRE'))
    M = M_OF[sig]
    TM, TH, ceven, cconj, refl = tw_fam(N, fam, la, sig, M)
    if first:
        try:
            g_fam(N, fam, la, sig, plant=True, nbox=1)
            fired = False
        except NotCert as stop:
            fired = str(stop).startswith('G-STOP')
        out('CHECK PLANT-DET %s' % ('FIRED' if fired else 'DID-NOT-FIRE'))
    G, nbx = g_fam(N, fam, la, sig)
    err = (2 * G / ((arb(sig) * M).exp() - 1)).upper()
    errh = (2 * G / ((arb(sig) * (M // 2)).exp() - 1)).upper()
    half = (TM + (-err).union(err)).overlaps(TH + (-errh).union(errh))
    Jv = TM + (-err).union(err) + (refl / 2 if N == 3 else 0)
    out('CHECK C-EVEN %s' % ('PASS' if ceven else 'FAIL'))
    out('CHECK C-CONJ %s' % ('PASS' if cconj else 'FAIL'))
    out('CHECK C-HALF %s' % ('PASS' if half else 'FAIL'))
    out('FAMILY %s %s %d %d %d %s %s' % (fam[0], '-' if fam[1] is None else fam[1], fam[2], lam.numerator, lam.denominator,
                                         ex(Jv.lower()), ex(Jv.upper())))
    out('  %s: sigma %g, M %d, cover %d boxes; I = %s; G %s on %d boxes, TW error %s (%.1f s)' % (fam_name(fam), sig, M, nb, Jv.str(12),
                                                                                             updec(G), nbx, updec(err), cpu() - t0))
    return fam, lam


def run_item(N):
    fls = []
    for idx, fam in enumerate(families(PART)):
        STAGE[0] = fam_name(fam)
        fls.append(eval_family(N, fam, idx == 0))
    STAGE[0] = 'controls'
    for fam, lam in (fls if PART == 'far' else fls[:1] if PART in ('tail', 'sh1', 'sh1a') else []):
        out('CHECK C-BLOCK-M %s' % ('PASS' if c_block_m(N, fam, fr_arb(lam)) else 'FAIL'))
        out('CHECK PLANT-BLOCK-M %s' % ('FIRED' if not c_block_m(N, fam, fr_arb(lam), True) else 'DID-NOT-FIRE'))
    if PART in ('sh1', 'sh1a'):
        ok, w_ = c_port_m(N)
        out('  C-PORT-M worst %.3e' % w_)
        out('CHECK C-PORT-M %s' % ('PASS' if ok else 'FAIL'))
        out('CHECK PLANT-PORT-M %s' % ('FIRED' if not c_port_m(N, True)[0] else 'DID-NOT-FIRE'))
    ok, w_, okp = c_flt_m(N, fls)
    out('  C-FLT-M worst %.3e' % w_)
    out('CHECK C-FLT-M %s' % ('PASS' if ok else 'FAIL'))
    out('CHECK PLANT-FLT-M %s' % ('FIRED' if not okp else 'DID-NOT-FIRE'))
# ------------------------------------------------------------------ the assembly item and its controls
def _dec(u, sig, down):
    """decimal string of a positive Fraction u, rounded up (down False) or down to sig significant digits"""
    p = 0
    while Fr(10) ** p > u:
        p -= 1
    while Fr(10) ** (p + 1) <= u:
        p += 1
    q = u * Fr(10) ** (sig - 1 - p)
    n = q.numerator // q.denominator
    if not down and n < q:
        n += 1
    if n == 10 ** sig:
        n, p = 10 ** (sig - 1), p + 1
    s = str(n)
    return '%s.%se%+d' % (s[0], s[1:], p)


def updec(x, sig=12):
    """a decimal string >= x (W1), from the exact upper end"""
    m, e = x.upper().man_exp()
    u = Fr(int(m)) * Fr(2) ** int(e)
    if u == 0:
        return '0'
    return _dec(u, sig, False) if u > 0 else '-' + _dec(-u, sig, True)


def cfun_a(x):
    return -(1 - x).log() / (2 * x)


def tilt2_full(k, t, av, eps):
    """arb port of twlib2.tilt2 (l.128-142), full 6n x 6n"""
    n = k.nrows()
    I = eye(n)
    T = zeros(6 * n)
    for v in range(6):
        addblk(T, n, v, v, I * acb(t * cfun_a(av[v])))
    for (vr, vp) in ((0, 2), (1, 4)):
        Gm = zeros(6 * n)
        gram(Gm, n, [(vp, I), (vr, k * (-1)), (5, I * (-1))])
        T = T + Gm * acb(eps / 2)
        a, aZ = av[vr], av[5]
        dk = 1 - (1 - a).sqrt() + (a * aZ).sqrt() / (1 + (1 - aZ).sqrt())
        addblk(T, n, 5, 5, I * acb((1 / eps - 1) * dk * dk / 2))
    return T


def k_np_of(N, al):
    if al is None:
        return np.array([[1.0, 0.0], [0.0, -1.0]])
    c, s = math.cos(al), math.sin(al)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]) if N == 4 else np.array([[c, -s], [s, c]])


def c_port(N, plant=None):
    """C-PORT (M1, V4, X2): Q_k, B_f and tilt2 (t = 1/300 and t = 0, eps 0.35) against twlib2, entrywise, <= PORT_TOL max(1, |f|)"""
    worst = 0.0
    for al in [0.7, 2.3] + ([None] if N == 3 else []):
        k = kw(N, None)[0] if al is None else kw(N, acb(al))[0]
        kn = k_np_of(N, al)
        Qf, Bsf, _ = T2.mats(kn)
        pairs = [(Qmat2(k), Qf)] + list(zip(forms2(k), Bsf))
        pairs += [(tilt2_full(k, tt, AV_A, EPS_A), T2.tilt2(kn, tf, AV_F, EPS_F)) for tt, tf in ((T_A, T_F), (arb(0), 0.0))]
        for idx, (Ma, Mf) in enumerate(pairs):
            for i in range(Ma.nrows()):
                for j in range(Ma.ncols()):
                    a = Ma[i, j]
                    if plant == 'B' and idx == 2 and (i, j) == (0, 0):
                        a = a + acb(arb('1e-10'))
                    if plant == 'T' and idx == len(pairs) - 2 and (i, j) == (0, 0):
                        a = a + acb(arb('1e-10'))
                    worst = max(worst, float((a - acb(float(Mf[i, j]))).abs_upper()) / max(1.0, abs(float(Mf[i, j]))))
    return worst <= PORT_TOL, worst


def c_hbar(plant=False):
    """C-HBAR (V7, X5): the arb hbar_j against twlib2.hbar2 (float, av 0.2/0.3), |a_mid - f| <= HBAR_TOL (|f| + S), S = max |f|"""
    worst = 0.0
    for j in (2, 3, 4):
        F = {tuple(e[:6]): c for e, c in T2.hbar2(j, AV_F, T_F).items()}
        A = dict(HB[j])
        if plant and j == 2:
            e0 = sorted(A)[0]
            A[e0] = A[e0] * (1 + arb('1e-9')) + arb('1e-9') * max(abs(c) for c in F.values())
        S = max(abs(c) for c in F.values())
        for e in set(F) | set(A):
            a = float(A[e].mid()) if e in A else 0.0
            worst = max(worst, abs(a - F.get(e, 0.0)) / (abs(F.get(e, 0.0)) + S))
    return worst <= HBAR_TOL, worst


def c_flt(N, plant=False):
    """C-FLT (V3): the E[P] values at al = 0.7, 2.3 against pk10's float GFMom on twlib2.mats, |a - f| <= FLT_TOL max(|f|, S)"""
    pm = T2.pmul
    F10 = [{e: float(c.mid()) for e, c in P.items()} for P in P10]
    Fh = {j: {tuple(e[:6]): c for e, c in T2.hbar2(j, AV_F, T_F).items()} for j in (2, 3, 4)}
    flo = {e: c for e, c in Fh[2].items() if sum(e) <= SPLIT}
    flo2 = pm(flo, flo)
    F6 = [Fh[4], pm(Fh[3], Fh[3]), pm(Fh[2], Fh[2]), pm(flo2, flo2)]
    worst = 0.0
    for al in (0.7, 2.3):
        Qf, Bsf, _ = T2.mats(k_np_of(N, al))
        C = np.linalg.inv(Qf)
        g10, g6 = GFMom(Bsf, C, 8), GFMom(Bsf[:6], C, 12)
        fv = [g10.E(P) for P in F10] + [g6.E(P) for P in F6]
        fv += [GFMom([Bsf[v]], C, 20).E({(m,): 1.0}) for v, m in V1M]
        fv += [fv[3] ** 2, fv[1] ** 3]
        av = [float(x.real.mid()) for x in tables(N, acb(al))[2]]
        if plant:
            av[2] *= 1 + 1e-7
        S = max(abs(x) for x in fv)
        worst = max(worst, max(abs(a - f) / max(abs(f), S) for a, f in zip(av, fv)))
    return worst <= FLT_TOL, worst


def c_hb4():
    """X3: hbar4 >= 0 on X >= 0 by construction (products of nonnegative factors); asserted at {0, 2}^6 and on the diagonal"""
    pts = [tuple(2 * ((i >> b) & 1) for b in range(6)) for i in range(64)] + [(s,) * 6 for s in (0.5, 1, 4)]
    for p in pts:
        v = sum((c * math.prod(arb(x) ** k for x, k in zip(p, e)) for e, c in HB[4].items()), arb(0))
        if not (v >= 0):
            return False
    return True


def plant_strip(N, sig):
    c = arb(3) / 4
    ch = (c * arb(sig)).cosh()
    fp = lambda N_, al: [det_Q(N_, al)[0] * (ch - al.cos())]
    neg_ok = fp(N, acb(0, (1 + c) * arb(sig) / 2))[0].real < 0
    ok, nb, bad = cover(N, sig, fp, CDMAX)
    return neg_ok and ok is False and bad is not None


M2BB4_SHA = 'e6a974a7a56ae224518b5ecd2b215e8c5582ae06bd126c327552e3c17191d41c'   # sha256 of pk08/px08_m2bb4.py, the producer of the group (b) asm output read for L2 (written by the build from sha256sum)
M3V3_SHA = '068e308d7e4ff0144cf6c2fc81c19a596ff2794b484c373d3a71f5b0629922f1'   # sha256 of pk08/px08_px03_v3.py, whose item outputs this file accepts (written by the build from sha256sum)
# ------------------------------------------------------------------ m3: the assembly item (C-CORE as in px08_m2bb2, byte for byte)
NODE_SRC = '/mnt/g2/release/root/code/pk05/s4c_m2bb.py'
CORE_MARKS = ('# ==== NODE CORE A BEGIN (s4c_m2bb.py lines 84-636, byte for byte) ====', '# ==== NODE CORE A END ====',
              '# ==== NODE CORE B BEGIN (s4c_m2bb.py lines 638-836, byte for byte) ====', '# ==== NODE CORE B END ====')
CORE_REF = ((84, 636), (638, 836)); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_PAIR = {'px08_px03_v3': '38dccfd84d53f311a8274e3ffb69fd3f22afafa5b7ef671e6660c9966fb474a5', 'px08_px03_v4': 'a236ed429580d462e3034edd7069f3fb783b82d3ad66b76378b47124aad0f98b'}  # G-ORIG: option (C), acc2 two-producer acceptance


def c_core(plant=False):
    """C-CORE (d): the lines between the NODE CORE markers of this file equal lines 84-636 and 638-836 of s4c_m2bb.py, whose sha256 must
    be NODE_SHA; plant=True (PLANT-CORE) appends one byte to the middle line of block B. Returns (ok, block line counts)"""
    with open(os.path.abspath(__file__), 'rb') as fh:
        mine = fh.read().split(b'\n')
    with open(NODE_SRC, 'rb') as fh:
        raw = fh.read()
    idx = [mine.index(m.encode()) if m.encode() in mine else -1 for m in CORE_MARKS]
    if min(idx) < 0 or not (idx[0] < idx[1] < idx[2] < idx[3]):
        return False, idx
    blocks = [mine[idx[0] + 1:idx[1]], mine[idx[2] + 1:idx[3]]]
    if plant:
        j = len(blocks[1]) // 2
        blocks[1] = blocks[1][:j] + [blocks[1][j] + b'#'] + blocks[1][j + 1:]
    ref = raw.split(b'\n')
    ok = hashlib.sha256(raw).hexdigest() == NODE_SHA and blocks == [ref[a - 1:b] for a, b in CORE_REF]
    return ok, [len(bl) for bl in blocks]


M3V3_SRC = '/mnt/g2/release/root/code/pk08/px08_px03_v3.py'
ITEM_PARTS = PARTS[:-1]
WHOLE = ('tail', 'sh1', 'sh2', 'sh3', 'far')
PRODS3 = []


def expected_checks(part):
    """M3: the multiset of CHECK and PLANT lines an item must print (eval_family and run_item): for each integrated family C-PROP, C-COVER,
    C-EVEN, C-CONJ and C-HALF; for each far matrix C-PROP; PLANT-PROP (and for integrated items PLANT-STRIP and PLANT-DET) on the first
    family; C-BLOCK-M with its plant on the first family of tail, sh1 and sh1a and on every far matrix; C-PORT-M with its plant in sh1 and
    sh1a; C-FLT-M with its plant in every item"""
    nf = len(families(part))
    if part == 'far':
        e = ['C-PROP'] * nf + ['PLANT-PROP'] + ['C-BLOCK-M', 'PLANT-BLOCK-M'] * nf
    else:
        e = ['C-PROP', 'C-COVER', 'C-EVEN', 'C-CONJ', 'C-HALF'] * nf + ['PLANT-PROP', 'PLANT-STRIP', 'PLANT-DET']
        if part in ('tail', 'sh1', 'sh1a'):
            e += ['C-BLOCK-M', 'PLANT-BLOCK-M']
        if part in ('sh1', 'sh1a'):
            e += ['C-PORT-M', 'PLANT-PORT-M']
    return sorted(e + ['C-FLT-M', 'PLANT-FLT-M'])


def c_itemcode_m3(plant=False):
    """C-ITEMCODE-M3: px08_px03_v3 (sha256 M3V3_SHA) and this file have the same evaluation code, byte for byte: the lines after NODE CORE
    A BEGIN up to 'def families(part):', and from 'def cfun_f(x):' up to 'def run_item(N):'. plant=True (PLANT-ITEMCODE-M3) appends one byte
    to the middle line of this file's second region. Returns (ok, region line counts)"""
    def regions(lines):
        def one(pred):
            r = [i for i, x in enumerate(lines) if pred(x)]
            return r[0] if len(r) == 1 else None
        a = one(lambda x: x == b'# ==== NODE CORE A BEGIN (s4c_m2bb.py lines 84-636, byte for byte) ====')
        b = one(lambda x: x == b'def families(part):')
        c = one(lambda x: x == b'def cfun_f(x):')
        d = one(lambda x: x == b'def run_item(N):')
        if None in (a, b, c, d) or not (a < b < c < d):
            return None
        return [lines[a + 1:b], lines[c:d]]
    with open(M3V3_SRC, 'rb') as fh:
        raw3 = fh.read()
    with open(os.path.abspath(__file__), 'rb') as fh:
        mine = fh.read().split(b'\n')
    r3, r4 = regions(raw3.split(b'\n')), regions(mine)
    if r3 is None or r4 is None:
        return False, 'regions'
    if plant:
        j = len(r4[1]) // 2
        r4[1] = r4[1][:j] + [r4[1][j] + b'#'] + r4[1][j + 1:]
    return hashlib.sha256(raw3).hexdigest() == M3V3_SHA and r3 == r4, [len(x) for x in r4]


def read_m3(N, man):
    """the item outputs (of px08_px03_v3 or of this file; each family exactly once) and the group (b) asm output of px08_m2bb4 (paths and
    sha256 in man; headers checked). Returns ({(kind, s, v): (lam, I)}, {part: [(check, result)]}, L2 (an exact upper end), group (b)'s
    TARGET line)"""
    from decimal import Decimal
    me = sha_file(os.path.abspath(__file__))
    pair = {'px08_px03_v3': M3V3_SHA, 'px08_px03_v4': me}
    fams, checks, nb, L2, tgt = {}, {}, 0, None, None
    for line in open(man):
        h, p = line.split()
        assert sha_file(p) == h, 'sha mismatch %s' % p
        lines = open(p).read().split('\n')
        hd = lines[0].split()
        if hd[0] == 'px08_m2bb4':
            assert hd[2] == M2BB4_SHA and hd[3] == 'ITEM=' + MODE and hd[4] == 'asm', 'header %s' % p
            assert any(x.strip() == 'VERDICT VALID' for x in lines), 'group (b) asm not VALID %s' % p
            rd = [x for x in lines if x.startswith('READING N=%d ' % N)]
            assert len(rd) == 1 and 'L2 = (int nu l2^2)^{1/2} <= ' in rd[0], 'READING line %s' % p
            L2 = Fr(Decimal(rd[0].split('L2 = (int nu l2^2)^{1/2} <= ')[1].split(';')[0].strip()))
            tl_ = [x for x in lines if x.startswith('TARGET N=%d ' % N)]
            assert len(tl_) == 1, 'TARGET line %s' % p
            tgt = tl_[0]
            nb += 1
            continue
        assert hd[0] in pair and ACC.ok(p, hd[2], pair[hd[0]], ORIG_PAIR[hd[0]]) and hd[3] == 'ITEM=' + MODE and hd[4] in ITEM_PARTS, 'header %s' % p
        assert hd[4] not in checks, 'item repeated %s' % p
        assert any(x.strip() == 'VERDICT PART-DONE' for x in lines), 'not done %s' % p
        PRODS3.append((hd[4], hd[0]))
        checks[hd[4]] = []
        for x in lines:
            w_ = x.split()
            if w_ and w_[0] == 'FAMILY':
                key = (w_[1], None if w_[2] == '-' else int(w_[2]), int(w_[3]))
                assert key not in fams and key in families(hd[4]), 'family %s in %s' % (key, p)
                fams[key] = (Fr(int(w_[4]), int(w_[5])), unex(w_[6], w_[7]).union(unex(w_[8], w_[9])))
            elif w_ and w_[0] == 'CHECK':
                checks[hd[4]].append((w_[1], w_[-1]))
    assert nb == 1, 'group (b) asm output count %d' % nb
    assert sorted(fams) == sorted(f for part in WHOLE for f in families(part)), 'every family exactly once'
    return fams, checks, L2, tgt


def run_asm_m3(N):
    fails, fires = [], []
    fams, checks, L2, tgt = read_m3(N, sys.argv[4])
    out('PRODUCERS N=%d: %s' % (N, ', '.join('%s %s' % pp for pp in PRODS3)))
    ms_ok = all(sorted(c for c, r in checks[part]) == expected_checks(part) for part in checks)
    out('C-MULTISET N=%d (M3: each item printed exactly its expected CHECK and PLANT lines): %s' % (N, 'PASS' if ms_ok else 'FAIL'))
    if not ms_ok:
        fails.append('C-MULTISET')
    fires.append(('PLANT-MULTISET', not (sorted(c for c, r in checks['tail'][1:]) == expected_checks('tail'))))
    ok, info = c_itemcode_m3()
    out('C-ITEMCODE-M3 N=%d (evaluation code of px08_px03_v3 = this file): %s, region lines %s' % (N, 'PASS' if ok else 'FAIL', info))
    if not ok:
        fails.append('C-ITEMCODE-M3')
    fires.append(('PLANT-ITEMCODE-M3', not c_itemcode_m3(True)[0]))
    nctl = npl = 0
    for part in checks:
        for c, r in checks[part]:
            if c.startswith('PLANT-'):
                npl += 1
                fires.append(('%s(%s)' % (c, part), r == 'FIRED'))
            else:
                nctl += 1
                if r != 'PASS':
                    fails.append('%s(%s)' % (c, part))
    out('ITEM CHECKS N=%d: %d controls, %d plants; failed: %s' % (N, nctl, npl, ', '.join(fails) or 'none'))
    ok, info = c_core()
    out('C-CORE N=%d (shared core = s4c_m2bb.py lines 84-636 and 638-836): %s, block lines %s' % (N, 'PASS' if ok else 'FAIL', info))
    if not ok:
        fails.append('C-CORE')
    fires.append(('PLANT-CORE', not c_core(True)[0]))
    J = arb(J_REF)
    pref2 = pref_arb(N) ** 2
    up = {k: v[1].upper() for k, v in fams.items()}
    pos = all(x > 0 for x in up.values())
    out('C-POS N=%d (every upper end > 0): %s' % (N, 'PASS' if pos else 'FAIL'))
    if not pos:
        out('VERDICT INVALID')
        return
    tail_sum = sum(((-fr_arb(fams[('tail', None, v)][0]) * J * AV_A[v]).exp() * up[('tail', None, v)] for v in range(6)), arb(0))
    ann_sum = sum(((-fr_arb(fams[('ann', s, v)][0]) * J * PREV_A[s][v]).exp() * up[('ann', s, v)] for s in range(NSH) for v in range(6)),
                  arb(0))
    far_sum = 64 * sum(((-fr_arb(fams[('far', None, v)][0]) * J * AVP_A[v]).exp() * up[('far', None, v)] for v in range(6)), arb(0))
    tail = pref2 * fr_arb(L2) * tail_sum.sqrt()
    annulus = pref2 * ann_sum
    far = pref2 * far_sum
    equ = pref2 * 12 * (2 * J / PI).sqrt() * (-J * (1 - (arb(685) / 1000).cos())).exp()
    total = tail + annulus + far + equ
    out('PIECES N=%d (J = 300, every J >= 300): L2 <= %s (group (b)); Chernoff sum %s; tail <= %s; annulus <= %s; far <= %s; equator <= %s'
        % (N, updec(fr_arb(L2)), updec(tail_sum), updec(tail), updec(annulus), updec(far), updec(equ)))
    out('GROUP-B %s' % tgt)
    out('CHECKS %s' % ('all PASS' if not fails else 'FAIL: ' + '; '.join(fails)))
    out('PLANTS %s' % ' '.join('%s:%s' % (nm, 'FIRED' if f else 'DID-NOT-FIRE') for nm, f in fires))
    valid = not fails and all(f for nm, f in fires)
    out('READING N=%d (t = 1/300, every J >= 300): pref^2 (tail + annulus) + far + equator <= %s' % (N, updec(total)))
    out('VERDICT %s' % ('VALID' if valid else 'INVALID'))


def main():
    N = 4 if MODE == 'n4' else 3
    try:
        if PART == 'asm':
            run_asm_m3(N)
            out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            return
        run_item(N)
    except NotCert as e:
        out('NOTCERT %s' % e)
        out('VERDICT INCOMPLETE')
        return
    out('VERDICT PART-DONE')
    out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    main()
