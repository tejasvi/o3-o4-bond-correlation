#!/usr/bin/env python3
"""s4c_m2bb.py -- pk05, S4 port, milestone 2, group (b) of route I: the untilted remainder R_E and the tail's l2 chain, certified for every
t in [0, 1/300] (S4_M2_DESIGN_v3 caa32045 with X1-X6).

Integrals (nu = dmu det(Q_k)^{-1/2}, TW on sigma = 0.5, M = 64): I[P] = int nu E_k[P] for
- P in the 10-form table to degree 8: 1, H1^2, H1^4, H2^2, H3^2, E2^2;
- P in the 6-form table (X1..X5, Z) to degree 12: hbar4, hbar3^2, hbar2^2, h_lo^4, where h_lo is the part of hbar2 of degree <= 3;
- X_v^m for the (v, m = 4|e|) of the terms e of h_hi = hbar2 - h_lo, from one-form tables to degree 20 (block entries, X4);
- the products (E H2^2)^2 and (E H1^2)^3.
hbar_j is an arb port of twlib2.hbar2 at av = (1/5, 1/5, 3/10, 3/10, 3/10, 3/10) and t = 1/300. Zbar(0) is in closed form, and Ej is summed to m < 400
with a certified geometric tail (V7). There is no *_series function.
Readings, all at upper ends:
- N4 = I[h_lo^4]^{1/4} + sum_e |c_e| prod_v I[X_v^{4|e|}]^{e_v/(4|e|)};
- R_E <= (t^4/24) I[hbar4] + (t^4/2) I[H2^2] + (t^6/72) I[hbar3^2] + (t^4/6)(I[H1^2] I[hbar3^2])^{1/2} + (t^5/6)(I[H2^2] I[hbar3^2])^{1/2}
  + (t^4/4)(I[H1^4] I[hbar2^2])^{1/2} + (t^5/8) I[H1^2]^{1/2} N4^2 + (t^6/48) N4^3 I[1]^{1/4};
- L2 = t I[H1^2]^{1/2} + t^2 I[E2^2]^{1/2} + t^3 (I[H3^2]^{1/2} + 27 I[H1^4]^{1/4} I[(E H2^2)^2]^{1/4} + (25^3/6) I[(E H1^2)^3]^{1/2}),
  the tail's (int nu l2^2)^{1/2} (V2; the Chernoff factor is milestone 3's).
The functions above and N4 increase in t on [0, 1/300], so their values at t = 1/300 are the suprema. They are multiplied by pref^2 in the
READING.
Items (each <= 4 min CPU), per N:
- nodes0: nodes k = 0..16 (with the N = 3 reflection and C-EVEN); nodes1: k = 17..32;
- g0: G boxes on x in [0, 1/2] pi (with C-CONJ); g1: x in [1/2, 1] pi;
- asm: reads the four outputs (paths and sha256 in the manifest given as the fourth argument) and the controls.
Partial items print exact outward ends (mantissa, exponent) of every value (X1). The asm item asserts the node partition {0..32}, the
reflection term (N = 3 only) and the G partition [0, 1]. It takes G as a max, and checks the half rule, C-EVEN and C-CONJ.
G (v3): |f| <= |w| (abs_lower det)^{-1/2} |E[P]| on boxes of Im al = sigma. This is valid because the cover certifies Re det Q_k > 0 on the
closed strip (maximum modulus). The TW error is whatever TW gives (X6).
Controls in asm:
- C-HASH; C-COVER with PLANT-STRIP (m1c's F_p' on det_blocks); C-NORM with PLANT-NORM;
- C-HBAR (mixed tolerance, X5) with PLANT-HBAR; C-SPLIT with PLANT-SPLIT; C-COVERS with PLANT-COVERS;
- C-PORT with PLANT-PORT and PLANT-PORT-T: Q_k, B_f and tilt2 at t = 1/300 and t = 0, with eps = 0.35 (X2);
- C-FLT on the E[P] values at al = 0.7 and 2.3 (V3), with PLANT-FLT;
- C-HB4 (X3): hbar4 >= 0 for X >= 0 by construction, since every term is a product of nonnegative factors. It is asserted at the 64 vertices of
  {0, 2}^6 and on the diagonal.
Usage: s4c_m2bb.py n4|n3 nodes0|nodes1|g0|g1|asm LIM [MANIFEST of the four partial outputs, for asm].
"""
import resource, sys, time, math, hashlib, signal, os
from fractions import Fraction as Fr
PARTS = ('nodes0', 'nodes1', 'g0', 'g1', 'asm')
if len(sys.argv) < 4 or sys.argv[1] not in ('n4', 'n3') or sys.argv[2] not in PARTS:
    print('usage: s4c_m2bb.py n4|n3 nodes0|nodes1|g0|g1|asm LIM [MANIFEST]')
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


out('s4c_m2bb sha256 %s ITEM=%s %s LIM=%d' % (sha_file(os.path.abspath(__file__)), MODE, PART, LIM))
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
G_K, G_MAXEV = 4, 20
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


def run_g(N):
    a0, a1 = G_SETS[PART]
    y = arb(SIG_B)
    todo = [(a0 + (a1 - a0) * i / G_K, a0 + (a1 - a0) * (i + 1) / G_K, 0) for i in range(G_K)]
    nev = nfail = 0
    while todo:
        u0, u1, d = todo.pop(0)
        nev += 1
        if nev > G_MAXEV:
            raise NotCert('G-STOP: more than %d evaluations on this half (projected count above 40)' % G_MAXEV)
        STAGE[0] = 'G box %s %s' % (u0, u1)
        try:
            g = ev_g(N, acb(xball(u0, u1), y))
            okv = all(z.is_finite() for z in g)
        except (NotCert, ZeroDivisionError, ValueError):
            okv = False
        if okv:
            out('BOX %s %s %s' % (u0, u1, ' '.join(ex(z) for z in g)))
            continue
        nfail += 1
        if d >= GDMAX:
            raise NotCert('G box [%s, %s] failed at depth %d' % (u0, u1, d))
        um = (u0 + u1) / 2
        todo += [(u0, um, d + 1), (um, u1, d + 1)]
    out('GSTAT %s: %d evaluations, %d failed' % (PART, nev, nfail))
    if PART == 'g0':
        STAGE[0] = 'C-CONJ'
        vals = []
        for s in (1, -1):
            w, det, e = tables(N, acb(PI / 3, s * arb(SIG_B)))
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


def read_parts(N, man):
    me = sha_file(os.path.abspath(__file__))
    nodes, refl, boxes, checks, seen = {}, None, [], [], []
    for line in open(man):
        h, p = line.split()
        assert sha_file(p) == h, 'sha mismatch %s' % p
        lines = open(p).read().split('\n')
        hd = lines[0].split()
        assert hd[0] == 's4c_m2bb' and hd[2] == me and hd[3] == 'ITEM=' + MODE, 'header %s' % p
        seen.append(hd[4])
        assert any(x.strip() == 'VERDICT PART-DONE' for x in lines), 'not done %s' % p
        for x in lines:
            w_ = x.split()
            if w_ and w_[0] == 'NODE':
                vv = [unex(w_[i], w_[i + 1]) for i in range(2, len(w_), 2)]
                v = [vv[2 * i].union(vv[2 * i + 1]) for i in range(len(vv) // 2)]
                assert len(v) == NV
                if w_[1] == 'refl':
                    assert refl is None
                    refl = v
                else:
                    assert int(w_[1]) not in nodes
                    nodes[int(w_[1])] = v
            elif w_ and w_[0] == 'BOX':
                g = [unex(w_[i], w_[i + 1]) for i in range(3, len(w_), 2)]
                assert len(g) == NV
                boxes.append((Fr(w_[1]), Fr(w_[2]), g))
            elif w_ and w_[0] == 'CHECK':
                checks.append((w_[1], w_[-1]))
    assert sorted(seen) == ['g0', 'g1', 'nodes0', 'nodes1'], seen
    assert sorted(nodes) == list(range(KN + 1)) and (refl is not None) == (N == 3)
    boxes.sort(key=lambda b: b[0])
    assert boxes[0][0] == 0 and boxes[-1][1] == 1 and all(boxes[i][1] == boxes[i + 1][0] for i in range(len(boxes) - 1))
    assert sorted(c for c, r in checks) == ['C-CONJ', 'C-EVEN', 'C-EVEN']
    return nodes, refl, boxes, checks


def run_asm(N):
    fails, fires = [], []
    nodes, refl, boxes, checks = read_parts(N, sys.argv[4])
    out('PARTITION N=%d: nodes 0..%d once each, reflection %s, %d G boxes tiling [0, 1] pi: PASS' % (N, KN, 'yes' if refl else 'no',
                                                                                                    len(boxes)))
    for c, r in checks:
        out('%s (partial item): %s' % (c, r))
        if r != 'PASS':
            fails.append(c)
    v = [[nodes[k][i] for k in range(KN + 1)] for i in range(NV)]
    TM = [(v[i][0] + v[i][KN] + 2 * sum(v[i][1:KN], arb(0))) / M_B for i in range(NV)]
    TH = [(v[i][0] + v[i][KN] + 2 * sum((v[i][k] for k in range(2, KN, 2)), arb(0))) * 2 / M_B for i in range(NV)]
    G = [maxup([b[2][i] for b in boxes]) for i in range(NV)]
    err = [(2 * G[i] / ((arb(SIG_B) * M_B).exp() - 1)).upper() for i in range(NV)]
    errh = [(2 * G[i] / ((arb(SIG_B) * (M_B // 2)).exp() - 1)).upper() for i in range(NV)]
    half = all((TM[i] + (-err[i]).union(err[i])).overlaps(TH[i] + (-errh[i]).union(errh[i])) for i in range(NV))
    out('C-HALF N=%d: %s' % (N, 'PASS' if half else 'FAIL'))
    if not half:
        fails.append('C-HALF')
    J = [TM[i] + (-err[i]).union(err[i]) + (refl[i] / 2 if N == 3 else 0) for i in range(NV)]
    for i in range(NV):
        out('  N=%d I[%s] = %s; G %s, TW error %s' % (N, NAMES[i], J[i].str(12), G[i].str(3), err[i].str(3)))
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
        if PART in NODE_SETS:
            run_nodes(N)
        elif PART in G_SETS:
            run_g(N)
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
