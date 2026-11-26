#!/usr/bin/env python3
"""px08_m2bb4.py -- pk08, S4 port, milestone 2, group (b) of route I: the G refinement (2026-11-07, after the n4 and
n3 asm items of px08_m2bb3 3f9bd819: VERDICT VALID, but pref^2 R_E <= 3e13 because a few pi/32 boxes next to the inverse-failure region
have finite but huge bounds, e.g. H1^4 up to 10^31 against 10^10-11.7 on the halved boxes beside them).
naming this file's sha8; the review does a delta check first.
Base: px08_m2bb3. The node core, the G constants and the G code are copied byte for
byte (C-CORE, C-GBLOCK). The G partials of px08_m2bb2 (976819c8) stay the base; this file adds refine items and a new asm.
Refine items r0..r7, one per eighth [j/8, (j+1)/8] pi of [0, pi]:
- read the two node partials and the base G partial of the quarter that holds the eighth (manifest, sha256 and Y1 pairing checked);
- caps: cap_i = TOLV |T_M,i| (e^{SIG_G M_B} - 1)/2 for the d8/d12 families REFINE = H1^4, H2^2, H3^2, E2^2, hbar4, hbar3^2, hbar2^2,
  h_lo^4, with T_M the node sum (as the asm) and TOLV = 1/10, the accepted relative target (R_E's float 1.1e-5 against the
  margin D = 8.8e-4 leaves the room);
- every base box of the eighth with a REFINE bound above its cap is printed as REPLACE u0 u1 and recomputed by halves, each halved again
  while it fails or a REFINE bound exceeds its cap, to depth R_DEPTH = 2 below the base box; a box at depth 2 is kept whatever its bound
  (the asm reports its TW error, X6), a failure at depth 2 is a G-STOP, and so is a refine item that needs more than R_MAXEV evaluations;
  new boxes get BOX and SUB lines exactly as in px08_m2bb2 (eval_box, eval_sub, det_lower: plan v1);
- each refine item first runs PLANT-DET (px08_m2bb2's g_loop on one box with a block det widened to contain 0: it must end in G-STOP).
asm: reads the 14 partial outputs (2 node, 4 base G, 8 refine; manifest), applies every REPLACE (the named box must be a base box, its new
boxes must tile it), and checks:
- C-REFINE: the REPLACE set equals the set of base boxes above the caps, recomputed here from the same node partials;
- PLANT-TILE: a planted REPLACE whose new boxes leave half of the box uncovered must make the same tiling check fail;
- the final boxes tile [0, 1] and each has its G_SUB sub-boxes; G = max over boxes of min(box bound, max of its sub-box bounds) (CHEAP);
- TARGET at TOLV = 1/10 (TGT_V), the tail-only products accepted as before;
- U1: C-HBAR scales each coefficient by the largest |f| of its own degree; PLANT-HBAR as before;
- U4: C-POS, every upper end J_i^+ > 0, before the logs and roots of the reading, with PLANT-POS;
- and every control of px08_m2bb3 (C-FLT per value, PLANT-FLT, C-CORE per node producer, C-GBLOCK, PLANT-CORE, PLANT-GBLOCK, ...).
Inside the node core, gbound, integral, ev_g and G_SETS are not called; they stay for the byte identity.
Usage: px08_m2bb4.py n4|n3 r0..r7|asm LIM MANIFEST.
"""
import resource, sys, time, math, hashlib, signal, os
from fractions import Fraction as Fr
PARTS = ('r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'asm')
if len(sys.argv) < 4 or sys.argv[1] not in ('n4', 'n3') or sys.argv[2] not in PARTS:
    print('usage: px08_m2bb4.py n4|n3 r0..r7|asm LIM MANIFEST')
    sys.exit(2)
MODE, PART, LIM = sys.argv[1], sys.argv[2], int(sys.argv[3])
if not (5 <= LIM <= 240) or len(sys.argv) != 5:
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


out('px08_m2bb4 sha256 %s ITEM=%s %s LIM=%d' % (sha_file(os.path.abspath(__file__)), MODE, PART, LIM))
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
# m2bb2 (pk08's G plan v1): quarters of [0, pi] for the G items, boxes of width pi/32, sub-boxes of width pi/128, det sub-boxes, G-STOP
G_Q = {'g0': (Fr(0), Fr(1, 4)), 'g1': (Fr(1, 4), Fr(1, 2)), 'g2': (Fr(1, 2), Fr(3, 4)), 'g3': (Fr(3, 4), Fr(1))}
G_K, G_SUB, G_DSUB, G_DEPTH, G_PROJ = 8, 4, 8, 2, 48
SIG_G = SIG_B       # m2bb2: the G line is Im al = 0.5, the boundary line of the closed strip that C-COVER certifies (plan v1 item 1)
TGT = 1e-3          # the TW error target of S4_M2_DESIGN_v3 (relative); a target, not a condition of validity (X6)
TAIL_ONLY = ('(E H2^2)^2', '(E H1^2)^3')
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


# ------------------------------------------------------------------ m2bb2: the G items (pk08's per-family G plan v1)
I1 = len(P10) + len(P6)
CHEAP = [0, 1] + list(range(I1, I1 + len(V1M))) + [NV - 1]
assert NAMES[0] == '1' and NAMES[1] == 'H1^2' and NAMES[NV - 1] == '(E H1^2)^3' and NV == I1 + len(V1M) + 2
assert max(sum(e) for e in P10[1]) <= 4 and all(nm in NAMES for nm in TAIL_ONLY)


def det_lower(N, u0, u1, y, plant=False):
    """an exact lower bound of |det Q_k| on the box x in [u0, u1] pi, Im al = y (plan v1 item 2): |det Q_k| = prod_b |det Q_b|, so the
    minimum over G_DSUB sub-boxes of prod_b abs_lower(det Q_b) is one; a block det that is not finite counts as 0.
    plant=True (PLANT-DET) widens the first block det of the first sub-box to contain 0"""
    lo = None
    for i in range(G_DSUB):
        al = acb(xball(u0 + (u1 - u0) * i / G_DSUB, u0 + (u1 - u0) * (i + 1) / G_DSUB), y)
        p = arb(1)
        for b, (kap, kapT) in enumerate(comps(N, al)):
            d = Q_block(kap, kapT).det()
            if plant and i == 0 and b == 0:
                d = acb(d.real.union(arb(0)), d.imag.union(arb(0)))
            p = p * (d.abs_lower() if d.is_finite() else arb(0))
        p = p.lower()
        lo = p if (lo is None or p < lo) else lo
    return lo


def prefactor(N, u0, u1, y, plant=False):
    """a = |w| det_lower^{-1/2} on the box, an exact upper end; None (the box bound is not finite) when det_lower is 0 or a is not finite"""
    dlo = det_lower(N, u0, u1, y, plant)
    if not (dlo > 0):
        return None
    a = (kw(N, acb(xball(u0, u1), y))[1].abs_upper() / dlo.sqrt()).upper()
    return a if a.is_finite() else None


def tables_cheap(N, al):
    """E[P] of the CHEAP families on a sub-box, in CHEAP order: tables()' block loop, the 10-form table to degree 4 (H1^2 has degree 4;
    pe raises KeyError on a missing moment) and the one-form tables to degree 20, as in tables()"""
    BC = [[] for _ in range(NF)]
    for (kap, kapT) in comps(N, al):
        Qb = Q_block(kap, kapT)
        Cb = Qb.inv()
        for f, Bb in enumerate(B_blocks(kap, kapT)):
            BC[f].append(Bb * Cb)
    m4 = gfmom_lists(BC, 4)
    m1 = {v: fixz(gfmom_lists([BC[v]], 20), 1) for v in sorted({v for v, m in V1M})}
    e1 = pe(P10[1], m4)
    return [pe(P10[0], m4), e1] + [m1[v][(m,)] for v, m in V1M] + [e1 ** 3]


def eval_box(N, u0, u1, y, plant=False):
    """the NV family bounds a |E[P]| on the box (plan v1 item 3; s4c_m2bb1's tables()), or None when one is not finite"""
    a = prefactor(N, u0, u1, y, plant)
    if a is None:
        return None
    try:
        w, det, e = tables(N, acb(xball(u0, u1), y))
    except (ZeroDivisionError, ValueError):
        return None
    g = [(a * x.abs_upper()).upper() for x in e]
    return g if all(z.is_finite() for z in g) else None


def eval_sub(N, s0, s1, y):
    """the CHEAP family bounds a |E[P]| on a sub-box (plan v1 item 4), or None when one is not finite"""
    a = prefactor(N, s0, s1, y)
    if a is None:
        return None
    try:
        e = tables_cheap(N, acb(xball(s0, s1), y))
    except (ZeroDivisionError, ValueError):
        return None
    g = [(a * x.abs_upper()).upper() for x in e]
    return g if all(z.is_finite() for z in g) else None


def g_loop(N, a0, a1, y, k, plant=False, emit=True):
    """k boxes of width (a1 - a0)/k pi on Im al = y, in x order; a failed box is replaced in place by its halves (depth <= G_DEPTH).
    G-STOP (b): a box that fails at depth G_DEPTH, or a projected count len(G_Q) x (boxes of this part) above G_PROJ.
    emit: print BOX, SUB and BOXFAIL lines. Returns (boxes, failed evaluations)"""
    todo = [(a0 + (a1 - a0) * i / k, a0 + (a1 - a0) * (i + 1) / k, 0) for i in range(k)]
    nbox = nfail = 0
    while todo:
        proj = len(G_Q) * (nbox + len(todo))
        if proj > G_PROJ:
            raise NotCert('G-STOP: projected box count %d > %d per N' % (proj, G_PROJ))
        u0, u1, d = todo.pop(0)
        STAGE[0] = 'G box %s %s' % (u0, u1)
        g = eval_box(N, u0, u1, y, plant)
        if g is None:
            nfail += 1
            if emit:
                out('BOXFAIL %s %s depth %d' % (u0, u1, d))
            if d >= G_DEPTH:
                raise NotCert('G-STOP: box [%s, %s] pi failed at depth %d' % (u0, u1, d))
            um = (u0 + u1) / 2
            todo = [(u0, um, d + 1), (um, u1, d + 1)] + todo
            continue
        nbox += 1
        if emit:
            out('BOX %s %s %s' % (u0, u1, ' '.join(ex(z) for z in g)))
            for i in range(G_SUB):
                s0, s1 = u0 + (u1 - u0) * i / G_SUB, u0 + (u1 - u0) * (i + 1) / G_SUB
                STAGE[0] = 'G sub-box %s %s' % (s0, s1)
                h = eval_sub(N, s0, s1, y)
                out('SUB %s %s %s %s %s' % (u0, u1, s0, s1, ' '.join(ex(z) for z in h) if h is not None else 'FAIL'))
    return nbox, nfail


def run_g(N):
    a0, a1 = G_Q[PART]
    y = arb(SIG_G)
    STAGE[0] = 'PLANT-DET'
    try:
        g_loop(N, a0, a0 + (a1 - a0) / G_K, y, 1, plant=True, emit=False)
        fired = False
    except NotCert as stop:
        fired = str(stop).startswith('G-STOP')
    out('CHECK PLANT-DET %s' % ('FIRED' if fired else 'DID-NOT-FIRE'))
    if not fired:
        raise NotCert('PLANT-DET did not fire')
    nbox, nfail = g_loop(N, a0, a1, y, G_K)
    out('GSTAT %s: %d boxes, %d failed evaluations (Im al = %g; %d sub-boxes per box; %d det sub-boxes)' % (PART, nbox, nfail, SIG_G,
                                                                                                         G_SUB, G_DSUB))
    if PART == 'g0':
        STAGE[0] = 'C-CONJ'
        vals = []
        for s in (1, -1):
            w, det, e = tables(N, acb(PI / 3, s * arb(SIG_G)))
            a = w * posre(det, 'det Q').rsqrt()
            vals.append([a * x for x in e])
        out('CHECK C-CONJ %s' % ('PASS' if all(x.overlaps(z.conjugate()) for x, z in zip(*vals)) else 'FAIL'))


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
    """C-HBAR (V7, X5; U1 of the REVIEW_PX08_M2BC2): the arb hbar_j against twlib2.hbar2 (float, av 0.2/0.3),
    |a_mid - f| <= HBAR_TOL (|f| + S_d), S_d = the largest |f| among the coefficients of the same total degree d; a degree with no float
    coefficient makes the test fail. plant=True (PLANT-HBAR) adds 1e-9 (|a| + S_d) to the first coefficient of hbar2, a move of at least
    1e-9 S_d >= 5e-10 (|f| + S_d), far above HBAR_TOL"""
    worst = 0.0
    for j in (2, 3, 4):
        F = {tuple(e[:6]): c for e, c in T2.hbar2(j, AV_F, T_F).items()}
        A = dict(HB[j])
        Sd = {}
        for e, c in F.items():
            Sd[sum(e)] = max(Sd.get(sum(e), 0.0), abs(c))
        if plant and j == 2:
            e0 = sorted(A)[0]
            A[e0] = A[e0] + arb('1e-9') * (abs(A[e0]) + Sd.get(sum(e0), 1.0))
        for e in set(F) | set(A):
            a = float(A[e].mid()) if e in A else 0.0
            den = abs(F.get(e, 0.0)) + Sd.get(sum(e), 0.0)
            worst = max(worst, abs(a - F.get(e, 0.0)) / den if den > 0 else float('inf'))
    return worst <= HBAR_TOL, worst


def c_flt(N, plant=False):
    """C-FLT (V3; m2bb3 fix): the E[P] values at al = 0.7, 2.3 against pk10's float GFMom on twlib2.mats, each value against itself:
    |a - f| <= FLT_TOL |f| (all 22 values are moments of nonnegative quantities, f > 0). Unplanted, it prints the largest ratio
    |a - f|/|f| per family. plant=True (PLANT-FLT) multiplies the H1^4 value by 1 + 1e-7, which this test must reject"""
    pm = T2.pmul
    F10 = [{e: float(c.mid()) for e, c in P.items()} for P in P10]
    Fh = {j: {tuple(e[:6]): c for e, c in T2.hbar2(j, AV_F, T_F).items()} for j in (2, 3, 4)}
    flo = {e: c for e, c in Fh[2].items() if sum(e) <= SPLIT}
    flo2 = pm(flo, flo)
    F6 = [Fh[4], pm(Fh[3], Fh[3]), pm(Fh[2], Fh[2]), pm(flo2, flo2)]
    ratio = [0.0] * NV
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
        ratio = [max(r, abs(a - f) / abs(f)) for r, a, f in zip(ratio, av, fv)]
    if not plant:
        out('C-FLT ratios N=%d (largest |a - f|/|f| at al = 0.7, 2.3): %s' % (N, ', '.join('%s %.2e' % (nm, r) for nm, r in zip(NAMES, ratio))))
    worst = max(ratio)
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


M2BB2_SHA = '911fbd96163ebf8f297d44c98ea983d533503c4ec9c6bad32300454a183fea97'   # sha256 of pk08/px08_m2bb2.py, the producer of the G partials (written by the build from sha256sum)
# ------------------------------------------------------------------ m2bb4: C-CORE per producer and C-GBLOCK (px08_m2bb3, byte for byte)
NODE_SRC = '/mnt/g2/release/root/code/pk05/s4c_m2bb.py'
M2BB2_SRC = '/mnt/g2/release/root/code/pk08/px08_m2bb2.py'
CORE_MARKS = ('# ==== NODE CORE A BEGIN (s4c_m2bb.py lines 84-636, byte for byte) ====', '# ==== NODE CORE A END ====',
              '# ==== NODE CORE B BEGIN (s4c_m2bb.py lines 638-836, byte for byte) ====', '# ==== NODE CORE B END ====')
CORE_REF = ((84, 636), (638, 836)); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_OF = {'s4c_m2bb': 'fc68d59431d3a6d9800f7882b0974a8c537e9883bbfb203204f1f493fcbc760f', 'px08_m2bb2': '976819c87e242c87f43342b7f9483c09df0ed2985f2876ff0363e01874b930f5', 'px08_m2bb4': '56db85be02ca14cfd932a9d705038b7d9360aa50eab6328c72e7d4e7092aa7d8'}  # G-ORIG: option (C), acc2 two-producer acceptance
G_MARKS = ('# ==== NODE CORE A END ====', '# ==== NODE CORE B BEGIN (s4c_m2bb.py lines 638-836, byte for byte) ====',
           '# ==== NODE CORE B END ====', '# ------------------------------------------------------------------ the assembly item and its controls')


def blocks_between(lines, marks):
    """the lines strictly between marks[0] and marks[1] and between marks[2] and marks[3] (exact whole lines, in this order), or None"""
    idx = [lines.index(m.encode()) if m.encode() in lines else -1 for m in marks]
    if min(idx) < 0 or not (idx[0] < idx[1] < idx[2] < idx[3]):
        return None
    return [lines[idx[0] + 1:idx[1]], lines[idx[2] + 1:idx[3]]]


def c_core_file(path, sha, plant=False):
    """C-CORE (d) for the script at path, whose sha256 must be sha: its lines between the NODE CORE markers equal lines 84-636 and 638-836
    of s4c_m2bb.py (sha256 NODE_SHA); s4c_m2bb.py itself, the reference, passes by its sha. plant=True (PLANT-CORE) appends one byte to the
    middle line of block B. Returns (ok, block line counts)"""
    with open(path, 'rb') as fh:
        raw = fh.read()
    with open(NODE_SRC, 'rb') as fh:
        ref_raw = fh.read()
    if hashlib.sha256(ref_raw).hexdigest() != NODE_SHA or hashlib.sha256(raw).hexdigest() != sha:
        return False, 'sha'
    if path == NODE_SRC and not plant:
        return True, 'reference'
    bl = blocks_between(raw.split(b'\n'), CORE_MARKS)
    if bl is None:
        return False, 'markers'
    if plant:
        j = len(bl[1]) // 2
        bl[1] = bl[1][:j] + [bl[1][j] + b'#'] + bl[1][j + 1:]
    ref = ref_raw.split(b'\n')
    return bl == [ref[a - 1:b] for a, b in CORE_REF], [len(x) for x in bl]


def c_gblock(plant=False):
    """C-GBLOCK: the G-item code of px08_m2bb2 (sha256 M2BB2_SHA; its lines between NODE CORE A END and NODE CORE B BEGIN, and between
    NODE CORE B END and the controls header) equals this file's, byte for byte; plant=True (PLANT-GBLOCK) appends one byte to the middle
    line of this file's second block. Returns (ok, block line counts)"""
    with open(M2BB2_SRC, 'rb') as fh:
        raw2 = fh.read()
    with open(os.path.abspath(__file__), 'rb') as fh:
        mine = fh.read().split(b'\n')
    a, b = blocks_between(raw2.split(b'\n'), G_MARKS), blocks_between(mine, G_MARKS)
    if a is None or b is None:
        return False, 'markers'
    if plant:
        j = len(b[1]) // 2
        b[1] = b[1][:j] + [b[1][j] + b'#'] + b[1][j + 1:]
    return hashlib.sha256(raw2).hexdigest() == M2BB2_SHA and a == b, [len(x) for x in b]


# ------------------------------------------------------------------ m2bb4: refine items and the assembly with REPLACE
R_PARTS = {'r%d' % j: (Fr(j, 8), Fr(j + 1, 8)) for j in range(8)}     # the eighths of [0, pi] the refine items cover
REFINE = list(range(2, 10))                                           # the d8/d12 families the caps act on
TOLV = arb(1) / 10            # the relative TW target accepted for group (b) (also TGT_V of the TARGET line)
R_DEPTH, R_MAXEV = 2, 19
assert [NAMES[i] for i in REFINE] == ['H1^4', 'H2^2', 'H3^2', 'E2^2', 'hbar4', 'hbar3^2', 'hbar2^2', 'h_lo^4']


def load(p, h):
    """the lines of one partial output after its sha256 check; it must say VERDICT PART-DONE"""
    assert sha_file(p) == h, 'sha mismatch %s' % p
    lines = open(p).read().split('\n')
    assert any(x.strip() == 'VERDICT PART-DONE' for x in lines), 'not done %s' % p
    return lines[0].split(), lines


def parse_items(lines):
    """the BOX, SUB, REPLACE and CHECK lines of one output, in order"""
    items = []
    for x in lines:
        w_ = x.split()
        if not w_:
            continue
        if w_[0] == 'BOX':
            g = [unex(w_[i], w_[i + 1]) for i in range(3, len(w_), 2)]
            assert len(g) == NV
            items.append(('BOX', Fr(w_[1]), Fr(w_[2]), g))
        elif w_[0] == 'SUB':
            g = None if w_[5:] == ['FAIL'] else [unex(w_[i], w_[i + 1]) for i in range(5, len(w_), 2)]
            assert g is None or len(g) == len(CHEAP)
            items.append(('SUB', Fr(w_[1]), Fr(w_[2]), (Fr(w_[3]), Fr(w_[4]), g)))
        elif w_[0] == 'REPLACE':
            assert len(w_) == 3
            items.append(('REPLACE', Fr(w_[1]), Fr(w_[2]), None))
        elif w_[0] == 'CHECK':
            items.append(('CHECK', w_[1], w_[-1], None))
    return items


def parse_nodes(lines, nodes, refl):
    for x in lines:
        w_ = x.split()
        if w_ and w_[0] == 'NODE':
            vv = [unex(w_[i], w_[i + 1]) for i in range(2, len(w_), 2)]
            v = [vv[2 * i].union(vv[2 * i + 1]) for i in range(len(vv) // 2)]
            assert len(v) == NV
            if w_[1] == 'refl':
                assert refl[0] is None
                refl[0] = v
            else:
                assert int(w_[1]) not in nodes
                nodes[int(w_[1])] = v


def boxes_of(items):
    """{(u0, u1): [g, [sub-boxes]]} from the BOX and SUB lines (a SUB line must follow its BOX line)"""
    bx = {}
    for it in items:
        if it[0] == 'BOX':
            assert (it[1], it[2]) not in bx
            bx[(it[1], it[2])] = [it[3], []]
        elif it[0] == 'SUB':
            bx[(it[1], it[2])][1].append(it[3])
    return bx


def groups_of(items):
    """[((u0, u1), {(a0, a1): [g, [sub-boxes]]}), ...] from the REPLACE, BOX and SUB lines of one refine output"""
    gr, cur = [], None
    for it in items:
        if it[0] == 'REPLACE':
            cur = ((it[1], it[2]), [])
            gr.append(cur)
        elif it[0] in ('BOX', 'SUB'):
            assert cur is not None, 'BOX or SUB before any REPLACE'
            cur[1].append(it)
    return [(key, boxes_of(its)) for key, its in gr]


def apply_replacements(boxes, groups):
    """each REPLACE must name a box present, and its new boxes must tile it exactly (and be new); returns (ok, the final boxes)"""
    fin = dict(boxes)
    for key, new in groups:
        ks = sorted(new)
        if key not in fin or not ks or ks[0][0] != key[0] or ks[-1][1] != key[1] or any(ks[i][1] != ks[i + 1][0] for i in range(len(ks) - 1)):
            return False, None
        del fin[key]
        for k2 in ks:
            if k2 in fin:
                return False, None
            fin[k2] = new[k2]
    return True, fin


def tm_of(nodes):
    v = [[nodes[k][i] for k in range(KN + 1)] for i in range(NV)]
    return [(v[i][0] + v[i][KN] + 2 * sum(v[i][1:KN], arb(0))) / M_B for i in range(NV)]


def caps_of(TM):
    """cap_i = TOLV |T_M,i| (e^{SIG_G M_B} - 1)/2 for i in REFINE, as exact lower ends"""
    f = ((arb(SIG_G) * M_B).exp() - 1) / 2
    return {i: (TOLV * TM[i].abs_lower() * f).lower() for i in REFINE}


def over_cap(g, caps):
    return any(not (g[i] <= caps[i]) for i in REFINE)


def refine_loop(N, u0, u1, y, caps, st):
    """the boxes that replace the base box [u0, u1]: its halves, each halved again while it fails or a REFINE bound exceeds its cap, to depth
    R_DEPTH below the base box; a box at depth R_DEPTH is kept whatever its bound; a failure at depth R_DEPTH, or more than R_MAXEV
    evaluations in this item, is a G-STOP"""
    um = (u0 + u1) / 2
    todo = [(u0, um, 1), (um, u1, 1)]
    while todo:
        if st[0] >= R_MAXEV:
            raise NotCert('G-STOP: more than %d evaluations in refine item %s' % (R_MAXEV, PART))
        a0, a1, d = todo.pop(0)
        st[0] += 1
        STAGE[0] = 'refine box %s %s' % (a0, a1)
        g = eval_box(N, a0, a1, y)
        if g is None:
            out('BOXFAIL %s %s depth %d' % (a0, a1, d))
            if d >= R_DEPTH:
                raise NotCert('G-STOP: refine box [%s, %s] pi failed at depth %d' % (a0, a1, d))
        if g is None or (d < R_DEPTH and over_cap(g, caps)):
            am = (a0 + a1) / 2
            todo = [(a0, am, d + 1), (am, a1, d + 1)] + todo
            continue
        st[1] += 1
        out('BOX %s %s %s' % (a0, a1, ' '.join(ex(z) for z in g)))
        for i in range(G_SUB):
            s0, s1 = a0 + (a1 - a0) * i / G_SUB, a0 + (a1 - a0) * (i + 1) / G_SUB
            STAGE[0] = 'refine sub-box %s %s' % (s0, s1)
            h = eval_sub(N, s0, s1, y)
            out('SUB %s %s %s %s %s' % (a0, a1, s0, s1, ' '.join(ex(z) for z in h) if h is not None else 'FAIL'))


def run_refine(N):
    x0, x1 = R_PARTS[PART]
    y = arb(SIG_G)
    sha_of = {'s4c_m2bb': NODE_SHA, 'px08_m2bb2': M2BB2_SHA}
    nodes, refl, base, seen = {}, [None], {}, []
    for line in open(sys.argv[4]):
        h, p = line.split()
        hd, lines = load(p, h)
        assert hd[0] in sha_of and ACC.ok(p, hd[2], sha_of[hd[0]], ORIG_OF[hd[0]]) and hd[3] == 'ITEM=' + MODE, 'header %s' % p
        seen.append(hd[4])
        if hd[4] in NODE_SETS:
            parse_nodes(lines, nodes, refl)
        else:
            assert hd[0] == 'px08_m2bb2' and hd[4] in G_Q and G_Q[hd[4]][0] <= x0 and x1 <= G_Q[hd[4]][1], 'base partial %s' % p
            base = {k: v for k, v in boxes_of(parse_items(lines)).items() if x0 <= k[0] and k[1] <= x1}
    assert sorted(seen) == sorted(list(NODE_SETS) + [q for q in G_Q if G_Q[q][0] <= x0 and x1 <= G_Q[q][1]]), seen
    assert sorted(nodes) == list(range(KN + 1)) and (refl[0] is not None) == (N == 3)
    ks = sorted(base)
    assert ks and ks[0][0] == x0 and ks[-1][1] == x1 and all(ks[i][1] == ks[i + 1][0] for i in range(len(ks) - 1)), 'base tiling'
    caps = caps_of(tm_of(nodes))
    out('CAPS N=%d (TOLV |T_M| (e^{%g M} - 1)/2): %s' % (N, SIG_G, ', '.join('%s %s' % (NAMES[i], updec(caps[i])) for i in REFINE)))
    STAGE[0] = 'PLANT-DET'
    try:
        g_loop(N, x0, x0 + (x1 - x0) / 4, y, 1, plant=True, emit=False)
        fired = False
    except NotCert as stop:
        fired = str(stop).startswith('G-STOP')
    out('CHECK PLANT-DET %s' % ('FIRED' if fired else 'DID-NOT-FIRE'))
    if not fired:
        raise NotCert('PLANT-DET did not fire')
    st, nrep = [0, 0], 0
    for k in ks:
        if over_cap(base[k][0], caps):
            nrep += 1
            out('REPLACE %s %s' % k)
            refine_loop(N, k[0], k[1], y, caps, st)
    out('RSTAT %s: %d base boxes in [%s, %s] pi, %d replaced by %d boxes, %d evaluations' % (PART, len(ks), x0, x1, nrep, st[1], st[0]))


def read_parts(N, man):
    """the 14 partial outputs (paths and sha256 in man). Y1: each script name pairs with its sha. Node partials of s4c_m2bb or px08_m2bb2;
    the four base G partials of px08_m2bb2; the eight refine partials of this file"""
    me = sha_file(os.path.abspath(__file__))
    sha_of = {'s4c_m2bb': NODE_SHA, 'px08_m2bb2': M2BB2_SHA, 'px08_m2bb4': me}
    nodes, refl, base, groups, checks, seen = {}, [None], {}, [], [], []
    prods = set()
    for line in open(man):
        h, p = line.split()
        hd, lines = load(p, h)
        assert hd[0] in sha_of and ACC.ok(p, hd[2], sha_of[hd[0]], ORIG_OF[hd[0]]) and hd[3] == 'ITEM=' + MODE, 'header %s' % p
        part = hd[4]
        seen.append(part)
        items = parse_items(lines)
        checks += [(it[1], it[2]) for it in items if it[0] == 'CHECK']
        if part in NODE_SETS:
            assert hd[0] in ('s4c_m2bb', 'px08_m2bb2'), 'node partial producer %s' % p
            prods.add(hd[0])
            parse_nodes(lines, nodes, refl)
        elif part in G_Q:
            assert hd[0] == 'px08_m2bb2', 'base G partial producer %s' % p
            bx = boxes_of(items)
            assert not (set(bx) & set(base)), 'base boxes repeated %s' % p
            base.update(bx)
        else:
            assert part in R_PARTS and hd[0] == 'px08_m2bb4', 'refine partial %s' % p
            x0, x1 = R_PARTS[part]
            gr = groups_of(items)
            assert all(x0 <= key[0] and key[1] <= x1 for key, new in gr), 'REPLACE outside its eighth %s' % p
            groups += gr
    assert sorted(seen) == sorted(list(NODE_SETS) + list(G_Q) + list(R_PARTS)), seen
    assert sorted(nodes) == list(range(KN + 1)) and (refl[0] is not None) == (N == 3)
    assert sorted(c for c, r in checks) == sorted(['C-CONJ', 'C-EVEN', 'C-EVEN'] + ['PLANT-DET'] * (len(G_Q) + len(R_PARTS)))
    return nodes, refl[0], base, groups, checks, prods


def run_asm(N):
    fails, fires = [], []
    me_path = os.path.abspath(__file__)
    me = sha_file(me_path)
    nodes, refl, base, groups, checks, prods = read_parts(N, sys.argv[4])
    for c, r in checks:
        out('%s (partial item): %s' % (c, r))
        if r != ('FIRED' if c == 'PLANT-DET' else 'PASS'):
            fails.append(c)
    src_of = {'s4c_m2bb': (NODE_SRC, NODE_SHA), 'px08_m2bb2': (M2BB2_SRC, M2BB2_SHA), 'px08_m2bb4': (me_path, me)}
    for name in sorted(prods | {'px08_m2bb4'}):
        ok, info = c_core_file(*src_of[name])
        out('C-CORE N=%d (node code of %s = s4c_m2bb.py lines 84-636 and 638-836): %s, %s' % (N, name, 'PASS' if ok else 'FAIL', info))
        if not ok:
            fails.append('C-CORE %s' % name)
    fires.append(('PLANT-CORE', not c_core_file(me_path, me, True)[0]))
    ok, info = c_gblock()
    out('C-GBLOCK N=%d (G-item code of px08_m2bb2 = this file): %s, block lines %s' % (N, 'PASS' if ok else 'FAIL', info))
    if not ok:
        fails.append('C-GBLOCK')
    fires.append(('PLANT-GBLOCK', not c_gblock(True)[0]))
    TM = tm_of(nodes)
    TH = [(v_[0] + v_[KN] + 2 * sum((v_[k] for k in range(2, KN, 2)), arb(0))) * 2 / M_B
          for v_ in [[nodes[k][i] for k in range(KN + 1)] for i in range(NV)]]
    caps = caps_of(TM)
    over = sorted(k for k in base if over_cap(base[k][0], caps))
    keys = sorted(key for key, new in groups)
    ok = over == keys
    out('C-REFINE N=%d: %d base boxes above the caps, %d REPLACE lines, the same set: %s' % (N, len(over), len(keys), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-REFINE')
    ok, fin = apply_replacements(base, groups)
    k0 = sorted(base)[0]
    planted = [(k0, {(k0[0], (k0[0] + k0[1]) / 2): base[k0]})]
    fires.append(('PLANT-TILE', not apply_replacements(base, planted)[0]))
    assert ok, 'a REPLACE does not tile its box'
    ks = sorted(fin)
    assert ks[0][0] == 0 and ks[-1][1] == 1 and all(ks[i][1] == ks[i + 1][0] for i in range(len(ks) - 1)), 'final tiling of [0, 1]'
    for k in ks:
        sb = sorted(fin[k][1], key=lambda s: s[0])
        assert len(sb) == G_SUB and sb[0][0] == k[0] and sb[-1][1] == k[1] and all(sb[i][1] == sb[i + 1][0] for i in range(G_SUB - 1))
        fin[k][1] = sb
    out('PARTITION N=%d: nodes 0..%d once each, reflection %s, %d base boxes, %d replaced by %d, %d final boxes tiling [0, 1] pi, %d '
        'sub-boxes tiling each: PASS' % (N, KN, 'yes' if refl else 'no', len(base), len(keys), len(ks) - len(base) + len(keys), len(ks), G_SUB))
    G = []
    for i in range(NV):
        per_box = []
        for k in ks:
            g, sb = fin[k]
            c = g[i]
            if i in CHEAP and all(s[2] is not None for s in sb):
                m = maxup([s[2][CHEAP.index(i)] for s in sb])
                c = m if m < c else c
            per_box.append(c)
        G.append(maxup(per_box))
    err = [(2 * G[i] / ((arb(SIG_G) * M_B).exp() - 1)).upper() for i in range(NV)]
    errh = [(2 * G[i] / ((arb(SIG_G) * (M_B // 2)).exp() - 1)).upper() for i in range(NV)]
    out('G line N=%d: Im al = %g (the boundary line of the C-COVER strip %g), %d boxes, %d sub-boxes each' % (N, SIG_G, SIG_B, len(ks), G_SUB))
    half = all((TM[i] + (-err[i]).union(err[i])).overlaps(TH[i] + (-errh[i]).union(errh[i])) for i in range(NV))
    out('C-HALF N=%d: %s' % (N, 'PASS' if half else 'FAIL'))
    if not half:
        fails.append('C-HALF')
    J = [TM[i] + (-err[i]).union(err[i]) + (refl[i] / 2 if N == 3 else 0) for i in range(NV)]
    miss = []
    for i in range(NV):
        tl = TM[i].abs_lower()
        within = err[i] <= TOLV * tl
        if not within:
            miss.append(NAMES[i])
        out('  N=%d I[%s] = %s; G %s, TW error %s, error/|T_M| %s%s' % (N, NAMES[i], J[i].str(12), updec(G[i]), updec(err[i]),
                                                                       updec(err[i] / tl) if tl > 0 else 'inf', '' if within else ' TARGET-MISS'))
    tail = [nm for nm in miss if nm in TAIL_ONLY]
    hard = [nm for nm in miss if nm not in TAIL_ONLY]
    out('TARGET N=%d (TW error <= 1/10 |T_M|, TGT_V): %s; tail-only misses, accepted: %s; other misses, reported: %s' % (
        N, 'all within' if not miss else '%d of %d miss' % (len(miss), NV), ', '.join(tail) or 'none', ', '.join(hard) or 'none'))
    STAGE[0] = 'controls'
    pref = pref_arb(N)
    sig, nb, tc = ladder(N, (SIG_B,), det_Q, CDMAX)
    out('C-COVER N=%d det Q_k at sigma %g: %s (%d boxes)' % (N, SIG_B, 'PASS' if sig else 'FAIL', nb))
    if not sig:
        fails.append('C-COVER')
    fires.append(('PLANT-STRIP', plant_strip(N, SIG_B)))
    lead = pref * pref * J[0]
    ok = (lead - arb(LEAD_REF)).abs_upper() <= arb(NORM_TOL)
    out('C-NORM N=%d: pref^2 I[1] = %s: %s' % (N, lead.str(15), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-NORM')
    fires.append(('PLANT-NORM', (pref * pref * (1 + arb('1e-8')) ** 2 * J[0] - arb(LEAD_REF)).abs_lower() > arb(NORM_TOL)))
    for nm, fn in (('C-HBAR', c_hbar), ('C-PORT', lambda p=None: c_port(N, p)), ('C-FLT', lambda p=False: c_flt(N, p))):
        ok, w_ = fn()
        out('%s N=%d: worst %.3e: %s' % (nm, N, w_, 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append(nm)
    fires.append(('PLANT-HBAR', not c_hbar(True)[0]))
    fires.append(('PLANT-PORT', not c_port(N, 'B')[0]))
    fires.append(('PLANT-PORT-T', not c_port(N, 'T')[0]))
    fires.append(('PLANT-FLT', not c_flt(N, True)[0]))
    ok = not (set(HLO) & set(HHI)) and set(HLO) | set(HHI) == set(HB[2]) and all((HLO.get(e) or HHI.get(e)) is HB[2][e] for e in HB[2])
    out('C-SPLIT: %s' % ('PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-SPLIT')
    drop = dict(HHI)
    drop.pop(sorted(drop)[0])
    fires.append(('PLANT-SPLIT', set(HLO) | set(drop) != set(HB[2])))
    need = [(10, max(sum(e) for P in P10 for e in P)), (6, max(sum(e) for P in P6 for e in P)), (1, max(m for v, m in V1M))]
    plan = {10: 8, 6: 12, 1: 20}
    ok = all(d <= plan[F] for F, d in need)
    out('C-COVERS: needed degrees %s against %s: %s' % (need, plan, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-COVERS')
    short = dict(plan)
    short[6] = 11
    fires.append(('PLANT-COVERS', not all(d <= short[F] for F, d in need)))
    ok = c_hb4()
    out('C-HB4 (X3): %s' % ('PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-HB4')
    pos = all(J[i].upper() > 0 for i in range(NV))
    out('C-POS N=%d (U4: every upper end J_i^+ > 0, before the logs and roots of the reading): %s' % (N, 'PASS' if pos else 'FAIL'))
    fires.append(('PLANT-POS', not all(x.upper() > 0 for x in [arb(0)] + J[1:])))
    if not pos:
        out('CHECKS FAIL: %s' % '; '.join(fails + ['C-POS']))
        out('VERDICT INVALID')
        return
    STAGE[0] = 'reading'
    U = {nm: J[i].upper() for i, nm in enumerate(NAMES)}
    hi = arb(0)
    for e, c in HHI.items():
        term = c.abs_upper()
        for vv in range(6):
            if e[vv]:
                term = term * (U['%s^%d' % (X6F[vv], 4 * sum(e))].log() * e[vv] / (4 * sum(e))).exp()
        hi = hi + term
    N4 = U['h_lo^4'].sqrt().sqrt() + hi
    t = T_A
    RE = (t ** 4 / 24 * U['hbar4'] + t ** 4 / 2 * U['H2^2'] + t ** 6 / 72 * U['hbar3^2'] + t ** 4 / 6 * (U['H1^2'] * U['hbar3^2']).sqrt()
          + t ** 5 / 6 * (U['H2^2'] * U['hbar3^2']).sqrt() + t ** 4 / 4 * (U['H1^4'] * U['hbar2^2']).sqrt() + t ** 5 / 8 * U['H1^2'].sqrt() * N4 ** 2
          + t ** 6 / 48 * N4 ** 3 * U['1'].sqrt().sqrt())
    L2 = t * U['H1^2'].sqrt() + t ** 2 * U['E2^2'].sqrt() + t ** 3 * (U['H3^2'].sqrt() + 27 * U['H1^4'].sqrt().sqrt() * U['(E H2^2)^2'].sqrt().sqrt()
                                                                      + arb(25) ** 3 / 6 * U['(E H1^2)^3'].sqrt())
    out('CHECKS %s' % ('all PASS' if not fails else 'FAIL: ' + '; '.join(fails)))
    out('PLANTS %s' % ' '.join('%s:%s' % (nm, 'FIRED' if f else 'DID-NOT-FIRE') for nm, f in fires))
    valid = not fails and all(f for nm, f in fires)
    out('READING N=%d (t = 1/300, every J >= 300): pref^2 R_E <= %s; N4 <= %s; L2 = (int nu l2^2)^{1/2} <= %s; pref^2 <= %s' % (
        N, updec(pref * pref * RE), updec(N4), updec(L2), updec(pref * pref)))
    out('VERDICT %s' % ('VALID' if valid else 'INVALID'))


def main():
    N = 4 if MODE == 'n4' else 3
    try:
        if PART in R_PARTS:
            run_refine(N)
        else:
            run_asm(N)
            out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            return
    except NotCert as e:
        out('NOTCERT %s' % e)
        out('VERDICT INCOMPLETE')
        return
    out('VERDICT PART-DONE')
    out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    main()
