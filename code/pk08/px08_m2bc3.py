#!/usr/bin/env python3
"""px08_m2bc3.py -- pk08, S4 port, milestone 2, group (c) of route I: rho4, the tilted remainder, certified for every J >= 300.
px08_m2bc2 (e0f2c4eb; the REVIEW_PX08_M2BC2 583fc982: sound, notes U1-U4) with the G refinement (2026-11-07):
group (b)'s asm items showed that a few pi/32 boxes next to the inverse-failure region have finite but huge bounds, so the G items here
split a box also when a d8/d12 bound is above its cap. m2bc2 was never run.

What changes against px08_m2bc2:
- G items g0..g7, one per eighth of [0, pi] (G_K = 4 boxes of width pi/32 each), read the four node partials (manifest, the sixth
  argument; sha256 and header checked) for T_M, and set cap_i = TOLV |T_M,i| (e^{SIG_C M_C} - 1)/2 for REFINE_C = H1^4, h_lo^4, with
  TOLV = 1/10 (the accepted relative target for group (b)). A box is replaced in place by its halves while it fails or a
  REFINE_C bound exceeds its cap, to depth G_DEPTH = 2 (width pi/128); a box at depth 2 is kept whatever its bound (the asm reports its
  TW error, X6). G-STOP: a failure at depth 2, or more than G_MAXEV_C evaluations in one item. PLANT-DET as before.
- asm: C-REFINE-C (every final box has width pi/128 or all REFINE_C bounds within the caps, recomputed from the same node partials), with
  PLANT-REFINE-C (a planted pi/32 box above a cap must fail it); PLANT-TILE (the same tiling check, with one box removed, must fail);
  TARGET at TOLV = 1/10; U1 (C-HBAR scales each coefficient by the largest |f| of its own degree, as in px08_m2bb4) and U4 (C-POS: every
  upper end J_i^+ > 0 before the log and roots of the reading, with PLANT-POS). U2: the cov output stays in the record.
Everything else is px08_m2bc2's (S4_M2C_DESIGN_v1 57f33661 with the CHECK 895792aa and Z1-Z4):
Integrals (nu_c = dmu det(Q_c)^{-1/2}, Q_c = Q - 2 T(1/300, eps = 35/100), T = twlib2.tilt2 in the block form of Q_block):
  I[P] = int nu_c E_c[P] for P = H1^4 (10-form table to degree 8), h_lo^4 (6-form table to degree 12) and the X_v^{4|e|} of h_hi (one-form
  tables to degree 20), plus the N = 3 reflection atom.
Why t = 1/300 suffices (S4_M2C_DESIGN_v1 section 2; CHECK 895792aa): every P above is >= 0, and at real al det(Q_t)^{-1/2} E_t[P] =
(2 pi)^{-d/2} int P exp(-y^T Q_t y/2) dy with Q_t = Q - 2 T_eps - 2 t D, D = diag(cfun(a_v)) (x) I_n > 0 (PSD and independent of k); so
the integrand increases in t, and Q_{1/300} > 0 gives Q_t > 0 for every t <= 1/300. hbar2 at 1/300 majorizes hbar2 at t' <= 1/300 and the
explicit powers of t increase.
Z4: each J-bound (t = 1/J) is twrig6z's, with its own tilt T(1/J) on its own Omega; only afterwards is its integrand compared, pointwise
in al (and at the reflection), with the integrand at t = 1/300 by the monotonicity above.
Reading, at upper ends: N4_c = I[h_lo^4]^{1/4} + sum_e |c_e| prod_v I[X_v^{4|e|}]^{e_v/(4|e|)};
  rho4 <= (1/24) (t I[H1^4]^{1/4} + (t^2/2) N4_c)^4 at t = 1/300, printed times pref^2 (one-sided decimals, W1).
Items (each <= 4 min CPU), per N; SIGC is the sigma of the ladder 0.5, 0.375, 0.25 (M = 64, 88, 128) that the cov item certifies:
- cov: C-PROP (interval LDL^T of the full real Q_c on al-intervals covering [0, pi], and at the N = 3 reflection; Z3 stop rule) with
  PLANT-PROP, and the cover ladder of Re det Q_c > 0 with PLANT-STRIP; it prints the certified sigma (no partial values);
- nodes0..nodes3: the nodes k = 0..M/2 in four parts (C-EVEN in each; the N = 3 reflection in nodes0);
- g0..g7: the G boxes on the eighths of [0, pi] at Im al = SIGC, as above (PLANT-DET in each, C-CONJ in g0);
- asm: reads the twelve partial outputs (paths and sha256 in the manifest, the sixth argument) and runs the controls.
Controls in asm: C-HASH; C-CORE (the shared core = s4c_m2bb.py fc68d594 lines 84-636 and 638-836) with PLANT-CORE; C-PROP with PLANT-PROP;
C-COVER at SIGC with PLANT-STRIP; C-REFINE-C with PLANT-REFINE-C; PLANT-TILE; C-BLOCK-T (block dets and E[H1^2] from the blocks against
the full 6n x 6n Q_c at al = 0.7, 2.3 and 0.3 + 0.2i, Z1) with PLANT-BLOCK-T; C-PORT (Q_k, B_f, tilt2 entrywise at t = 1/300 and 0, Z2)
with PLANT-PORT and PLANT-PORT-T; C-HBAR (U1) with PLANT-HBAR; C-FLT-T (each value against itself) with PLANT-FLT-T; C-SPLIT with
PLANT-SPLIT; C-COVERS with PLANT-COVERS; C-POS (U4) with PLANT-POS; the partition, the box and sub-box tilings, G as a max, C-HALF,
C-EVEN, C-CONJ and every PLANT-DET (X1); per-family err with TARGET flags (a miss is listed; X6).
Inside the shared core, the untilted tables, ev_node, run_nodes, gbound, integral, ev_g and G_SETS are not called here; nor is the
group (b) c_flt of the controls (it is px08_m2bb3's per-value version).
Usage: px08_m2bc3.py n4|n3 cov LIM | n4|n3 nodes0..nodes3 LIM SIGC | n4|n3 g0..g7 LIM SIGC NODE_MANIFEST | n4|n3 asm LIM SIGC MANIFEST.
"""
import resource, sys, time, math, hashlib, signal, os
from fractions import Fraction as Fr
PARTS = ('cov', 'nodes0', 'nodes1', 'nodes2', 'nodes3', 'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'asm')
NEXTRA = {'cov': 0, 'nodes0': 1, 'nodes1': 1, 'nodes2': 1, 'nodes3': 1}
if len(sys.argv) < 4 or sys.argv[1] not in ('n4', 'n3') or sys.argv[2] not in PARTS:
    print('usage: px08_m2bc3.py n4|n3 cov LIM | n4|n3 nodes0..nodes3 LIM SIGC | n4|n3 g0..g7 LIM SIGC NODE_MANIFEST | n4|n3 asm LIM SIGC '
          'MANIFEST')
    sys.exit(2)
MODE, PART, LIM = sys.argv[1], sys.argv[2], int(sys.argv[3])
if not (5 <= LIM <= 240) or len(sys.argv) != 4 + NEXTRA.get(PART, 2) or (len(sys.argv) > 4 and sys.argv[4] not in ('0.5', '0.375', '0.25')):
    print('bad LIM %d or arguments' % LIM)
    sys.exit(2)
SIGC = sys.argv[4] if len(sys.argv) > 4 else '-'
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


out('px08_m2bc3 sha256 %s ITEM=%s %s LIM=%d SIGC=%s' % (sha_file(os.path.abspath(__file__)), MODE, PART, LIM, SIGC))
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
# m2bc3: G on the eighths of [0, pi] with the value split, and the sigma ladder of S4_M2_DESIGN_v3 for Q_c
G_E = {'g%d' % j: (Fr(j, 8), Fr(j + 1, 8)) for j in range(8)}
G_K, G_SUB, G_DSUB, G_DEPTH, G_MAXEV_C = 4, 4, 8, 2, 19
SIG_LADDER = {'0.5': 64, '0.375': 88, '0.25': 128}
SIG_C = float(SIGC) if SIGC != '-' else None     # 0.5, 0.375 and 0.25 are exact binary fractions
M_C = SIG_LADDER.get(SIGC)
TOLV = arb(1) / 10      # the relative TW target (the caps and the TARGET line); a target, not a condition of validity (X6)
PROP_K, PROP_DEPTH, PROP_MAXEV = 32, 8, 2048    # C-PROP: initial al-intervals, depth cap, evaluation cap (Z3)
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


# ------------------------------------------------------------------ m2bc: group (c) at t = 1/300 (S4_M2C_DESIGN_v1)
I1 = len(P10) + len(P6)
ICF = [2, 9] + list(range(I1, I1 + len(V1M)))       # NAMES indices of the group (c) families
NAMES_C = [NAMES[i] for i in ICF]
NC = len(NAMES_C)
CHEAP_C = list(range(2, NC))                        # the one-forms, also bounded on sub-boxes
assert NAMES_C[:2] == ['H1^4', 'h_lo^4'] and NC == 2 + len(V1M)
TT = T_A            # t = 1/300


def zrad(z):
    return z.real.rad().max(z.imag.rad())


def T_block(kap, kapT, plant=False):
    """twlib2.tilt2 (l.128-142) at t = 1/300, eps = EPS_A, in the 6 x 6 block form of Q_block: t cfun(a_v) on the diagonal; (eps/2) times
    the Gram of Q_block's twisted rows PARTS_Q[7] = [(2,1),(0,'k'),(5,-1)] and PARTS_Q[9] = [(4,1),(1,'k'),(5,-1)], which are twlib2's
    M = sel(vp) - k sel(vr) - sel(5) for (vr, vp) = (0, 2), (1, 4); and (1/eps - 1) dk^2/2 at Z for each of the two bonds.
    plant=True (PLANT-BLOCK-T) adds 1e-10 to the (0, 0) entry"""
    T = zeros(6)
    for v in range(6):
        T[v, v] = T[v, v] + acb(TT * cfun_a(AV_A[v]))
    for parts in (PARTS_Q[7], PARTS_Q[9]):
        cs = [(v, (-kap if c == 'k' else acb(c)), (-kapT if c == 'k' else acb(c))) for v, c in parts]
        for (u, cu, cuT) in cs:
            for (v, cv, cvT) in cs:
                T[u, v] = T[u, v] + cuT * cv * acb(EPS_A / 2)
    for (vr, vp) in ((0, 2), (1, 4)):
        a, aZ = AV_A[vr], AV_A[5]
        dk = 1 - (1 - a).sqrt() + (a * aZ).sqrt() / (1 + (1 - aZ).sqrt())
        T[5, 5] = T[5, 5] + acb((1 / EPS_A - 1) * dk * dk / 2)
    if plant:
        T[0, 0] = T[0, 0] + acb(arb('1e-10'))
    return T


def Qc_block(kap, kapT, plant=False):
    return Q_block(kap, kapT) - T_block(kap, kapT, plant) * 2


def det_blocks_c(N, al):
    d = acb(1)
    for (kap, kapT) in comps(N, al):
        d = d * Qc_block(kap, kapT).det()
    return d


def det_Qc(N, al):
    return [det_blocks_c(N, al)]


def Qc_full(k):
    """the full 6n x 6n Q_c = Qmat2(k) - 2 tilt2_full(k, 1/300, AV_A, EPS_A)"""
    return Qmat2(k) - tilt2_full(k, TT, AV_A, EPS_A) * 2


def bc_c(N, al):
    """(w, det Q_c, BC) at al (acb), al None = the N = 3 reflection (full matrices); a failed inverse raises ZeroDivisionError"""
    if al is None:
        k, w = kw(N, None)
        Q = Qc_full(k)
        det, C = Q.det(), Q.inv()
        return w, det, [[Bf * C] for Bf in forms2(k)]
    w, det, BC = kw(N, al)[1], acb(1), [[] for _ in range(NF)]
    for (kap, kapT) in comps(N, al):
        Qb = Qc_block(kap, kapT)
        det = det * Qb.det()
        Cb = Qb.inv()
        for f, Bb in enumerate(B_blocks(kap, kapT)):
            BC[f].append(Bb * Cb)
    return w, det, BC


def tables_c(N, al):
    """(w, det Q_c, [E_c P for P in NAMES_C]) at al: s4c_m2bb1's tables (10-form to degree 8, 6-form to degree 12, one-forms to degree 20)
    on Q_c, for H1^4, h_lo^4 and the one-forms"""
    w, det, BC = bc_c(N, al)
    m10 = gfmom_lists(BC, 8)
    m6 = fixz(gfmom_lists(BC[:6], 12), 6)
    m1 = {v: fixz(gfmom_lists([BC[v]], 20), 1) for v in sorted({v for v, m in V1M})}
    return w, det, [pe(P10[2], m10), pe(P6[3], m6)] + [m1[v][(m,)] for v, m in V1M]


def tables_c_cheap(N, al):
    """the one-forms (CHEAP_C order) on a sub-box"""
    w, det, BC = bc_c(N, al)
    m1 = {v: fixz(gfmom_lists([BC[v]], 20), 1) for v in sorted({v for v, m in V1M})}
    return [m1[v][(m,)] for v, m in V1M]


def ev_node_c(N, al):
    w, det, e = tables_c(N, al)
    a = w * posre(det, 'det Q_c').rsqrt()
    return [(a * x).real for x in e]


def node_parts():
    K = M_C // 2
    b = [i * (K + 1) // 4 for i in range(5)]
    return {'nodes%d' % i: list(range(b[i], b[i + 1])) for i in range(4)}


def run_nodes_c(N):
    ks = node_parts()[PART]
    keep = {}
    for k in ks:
        STAGE[0] = 'node %d' % k
        keep[k] = ev_node_c(N, acb(PI * (2 * k) / M_C))
        out(node_line(str(k), keep[k]))
    k = ks[0] if ks[0] > 0 else ks[1]
    STAGE[0] = 'C-EVEN'
    mir = ev_node_c(N, acb(PI * (2 * (M_C - k)) / M_C))
    out('CHECK C-EVEN k=%d %s' % (k, 'PASS' if all(x.overlaps(y) for x, y in zip(keep[k], mir)) else 'FAIL'))
    if PART == 'nodes0' and N == 3:
        STAGE[0] = 'reflection'
        out(node_line('refl', ev_node_c(N, None)))


# ------------------------------------------------------------------ m2bc: G on Im al = SIG_C (px08_m2bb2's method on Q_c)
def det_lower_c(N, u0, u1, y, plant=False):
    """an exact lower bound of |det Q_c| on the box: the minimum over G_DSUB sub-boxes of prod_b abs_lower(det of the Q_c block); a block
    det that is not finite counts as 0. plant=True (PLANT-DET) widens the first block det of the first sub-box to contain 0"""
    lo = None
    for i in range(G_DSUB):
        al = acb(xball(u0 + (u1 - u0) * i / G_DSUB, u0 + (u1 - u0) * (i + 1) / G_DSUB), y)
        p = arb(1)
        for b, (kap, kapT) in enumerate(comps(N, al)):
            d = Qc_block(kap, kapT).det()
            if plant and i == 0 and b == 0:
                d = acb(d.real.union(arb(0)), d.imag.union(arb(0)))
            p = p * (d.abs_lower() if d.is_finite() else arb(0))
        p = p.lower()
        lo = p if (lo is None or p < lo) else lo
    return lo


def prefactor_c(N, u0, u1, y, plant=False):
    """a = |w| det_lower_c^{-1/2} on the box, an exact upper end; None (the box bound is not finite) when the det bound is 0"""
    dlo = det_lower_c(N, u0, u1, y, plant)
    if not (dlo > 0):
        return None
    a = (kw(N, acb(xball(u0, u1), y))[1].abs_upper() / dlo.sqrt()).upper()
    return a if a.is_finite() else None


def eval_box_c(N, u0, u1, y, plant=False):
    """the NC family bounds a |E_c[P]| on the box, or None when one is not finite"""
    a = prefactor_c(N, u0, u1, y, plant)
    if a is None:
        return None
    try:
        w, det, e = tables_c(N, acb(xball(u0, u1), y))
    except (ZeroDivisionError, ValueError):
        return None
    g = [(a * x.abs_upper()).upper() for x in e]
    return g if all(z.is_finite() for z in g) else None


def eval_sub_c(N, s0, s1, y):
    """the one-form bounds a |E_c[X_v^m]| on a sub-box, or None when one is not finite"""
    a = prefactor_c(N, s0, s1, y)
    if a is None:
        return None
    try:
        e = tables_c_cheap(N, acb(xball(s0, s1), y))
    except (ZeroDivisionError, ValueError):
        return None
    g = [(a * x.abs_upper()).upper() for x in e]
    return g if all(z.is_finite() for z in g) else None


REFINE_C = [0, 1]          # H1^4, h_lo^4: the d8/d12 families of group (c), on which the caps act
assert [NAMES_C[i] for i in REFINE_C] == ['H1^4', 'h_lo^4']


def caps_from_tm(TM):
    """cap_i = TOLV |T_M,i| (e^{SIG_C M_C} - 1)/2 for i in REFINE_C, as exact lower ends"""
    f = ((arb(SIG_C) * M_C).exp() - 1) / 2
    return {i: (TOLV * TM[i].abs_lower() * f).lower() for i in REFINE_C}


def node_parse(lines, nodes, refl):
    for x in lines:
        w_ = x.split()
        if w_ and w_[0] == 'NODE':
            vv = [unex(w_[i], w_[i + 1]) for i in range(2, len(w_), 2)]
            v = [vv[2 * i].union(vv[2 * i + 1]) for i in range(len(vv) // 2)]
            assert len(v) == NC
            if w_[1] == 'refl':
                assert refl[0] is None
                refl[0] = v
            else:
                assert int(w_[1]) not in nodes
                nodes[int(w_[1])] = v


def tm_c(nodes):
    K = M_C // 2
    return [(nodes[0][i] + nodes[K][i] + 2 * sum((nodes[k][i] for k in range(1, K)), arb(0))) / M_C for i in range(NC)]


def node_caps(N, man):
    """T_M from the four node partials of this file at this SIGC (paths and sha256 in man; header and PART-DONE checked), and the caps"""
    me = sha_file(os.path.abspath(__file__))
    nodes, refl, seen = {}, [None], []
    for line in open(man):
        h, p = line.split()
        assert sha_file(p) == h, 'sha mismatch %s' % p
        lines = open(p).read().split('\n')
        hd = lines[0].split()
        assert hd[0] == 'px08_m2bc3' and ACC.ok(p, hd[2], me, ORIG_SELF) and hd[3] == 'ITEM=' + MODE and hd[6] == 'SIGC=' + SIGC and hd[4] in node_parts(), \
            'header %s' % p
        assert any(x.strip() == 'VERDICT PART-DONE' for x in lines), 'not done %s' % p
        seen.append(hd[4])
        node_parse(lines, nodes, refl)
    assert sorted(seen) == sorted(node_parts()) and sorted(nodes) == list(range(M_C // 2 + 1)) and (refl[0] is not None) == (N == 3)
    TM = tm_c(nodes)
    return TM, caps_from_tm(TM)


def g_loop_c(N, a0, a1, y, k, caps=None, plant=False, emit=True):
    """k boxes of width (a1 - a0)/k pi on Im al = y, in x order; a box is replaced in place by its halves while it fails or (caps given) a
    REFINE_C bound exceeds its cap, to depth G_DEPTH; a box at depth G_DEPTH is kept whatever its bound. G-STOP: a failure at depth
    G_DEPTH, or more than G_MAXEV_C evaluations in this item. Returns (boxes, failed evaluations, evaluations)"""
    todo = [(a0 + (a1 - a0) * i / k, a0 + (a1 - a0) * (i + 1) / k, 0) for i in range(k)]
    nbox = nfail = nev = 0
    while todo:
        if nev >= G_MAXEV_C:
            raise NotCert('G-STOP: more than %d evaluations in this item' % G_MAXEV_C)
        u0, u1, d = todo.pop(0)
        nev += 1
        STAGE[0] = 'G box %s %s' % (u0, u1)
        g = eval_box_c(N, u0, u1, y, plant)
        if g is None:
            nfail += 1
            if emit:
                out('BOXFAIL %s %s depth %d' % (u0, u1, d))
            if d >= G_DEPTH:
                raise NotCert('G-STOP: box [%s, %s] pi failed at depth %d' % (u0, u1, d))
        if g is None or (caps is not None and d < G_DEPTH and any(not (g[i] <= caps[i]) for i in REFINE_C)):
            um = (u0 + u1) / 2
            todo = [(u0, um, d + 1), (um, u1, d + 1)] + todo
            continue
        nbox += 1
        if emit:
            out('BOX %s %s %s' % (u0, u1, ' '.join(ex(z) for z in g)))
            for i in range(G_SUB):
                s0, s1 = u0 + (u1 - u0) * i / G_SUB, u0 + (u1 - u0) * (i + 1) / G_SUB
                STAGE[0] = 'G sub-box %s %s' % (s0, s1)
                h = eval_sub_c(N, s0, s1, y)
                out('SUB %s %s %s %s %s' % (u0, u1, s0, s1, ' '.join(ex(z) for z in h) if h is not None else 'FAIL'))
    return nbox, nfail, nev


def run_g_c(N):
    a0, a1 = G_E[PART]
    y = arb(SIG_C)
    TM, caps = node_caps(N, sys.argv[5])
    out('CAPS N=%d (TOLV |T_M| (e^{%g M} - 1)/2, M = %d): %s' % (N, SIG_C, M_C, ', '.join('%s %s' % (NAMES_C[i], updec(caps[i]))
                                                                                       for i in REFINE_C)))
    STAGE[0] = 'PLANT-DET'
    try:
        g_loop_c(N, a0, a0 + (a1 - a0) / G_K, y, 1, plant=True, emit=False)
        fired = False
    except NotCert as stop:
        fired = str(stop).startswith('G-STOP')
    out('CHECK PLANT-DET %s' % ('FIRED' if fired else 'DID-NOT-FIRE'))
    if not fired:
        raise NotCert('PLANT-DET did not fire')
    nbox, nfail, nev = g_loop_c(N, a0, a1, y, G_K, caps)
    out('GSTAT %s: %d boxes, %d failed, %d evaluations (Im al = %g; value split on %s; %d sub-boxes per box; %d det sub-boxes)' % (
        PART, nbox, nfail, nev, SIG_C, ', '.join(NAMES_C[i] for i in REFINE_C), G_SUB, G_DSUB))
    if PART == 'g0':
        STAGE[0] = 'C-CONJ'
        vals = []
        for s in (1, -1):
            w, det, e = tables_c(N, acb(PI / 3, s * arb(SIG_C)))
            a = w * posre(det, 'det Q_c').rsqrt()
            vals.append([a * x for x in e])
        out('CHECK C-CONJ %s' % ('PASS' if all(x.overlaps(z.conjugate()) for x, z in zip(*vals)) else 'FAIL'))


# ------------------------------------------------------------------ m2bc: C-PROP, the cover ladder and the cov item
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


def qc_real(N, al):
    """the full real Q_c at a real al (an arb point or interval), or at the N = 3 reflection (al None), as rows of arb (real parts)"""
    k = kw(N, None)[0] if al is None else kw(N, acb(al))[0]
    Q = Qc_full(k)
    return [[Q[i, j].real for j in range(Q.ncols())] for i in range(Q.nrows())]


def minlow(D):
    m = D[0].lower()
    for x in D[1:]:
        m = x.lower() if x.lower() < m else m
    return m


def c_prop(N):
    """C-PROP: interval LDL^T of Q_c on al-intervals tiling [0, pi] (PROP_K of them, halved on failure), and at the N = 3 reflection.
    Stop rule (Z3): an interval that fails at depth PROP_DEPTH, or more than PROP_MAXEV LDL^T evaluations, ends C-PROP as FAIL.
    Returns (ok, intervals, smallest pivot lower end, the interval (u0, u1) where it occurs, or the reason of the stop)"""
    todo = [(Fr(i, PROP_K), Fr(i + 1, PROP_K), 0) for i in range(PROP_K)]
    nint, nev, dmin, where = 0, 0, None, None
    while todo:
        if nev >= PROP_MAXEV:
            return False, nint, dmin, 'PROP-STOP: more than %d evaluations' % PROP_MAXEV
        u0, u1, d = todo.pop()
        nev += 1
        D = ldlt(qc_real(N, xball(u0, u1)))
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
    if N == 3 and ldlt(qc_real(N, None)) is None:
        return False, nint, dmin, 'the reflection failed'
    return True, nint, dmin, where


def plant_prop(N, where):
    """PLANT-PROP (D6): at the midpoint al* of the interval with the smallest pivot, c = min_j (upper end of pivot j) >= d_min >= lambda_min,
    so Q_c(al*) - 2 c I has lambda_min - 2 c <= -lambda_min < 0; its LDL^T must fail. True when it fails as it must"""
    u = (where[0] + where[1]) / 2
    A = qc_real(N, PI * u.numerator / u.denominator)
    D = ldlt(A)
    if D is None:
        return False
    c = D[0].upper()
    for x in D[1:]:
        c = x.upper() if x.upper() < c else c
    return ldlt([[A[i][j] - (2 * c if i == j else 0) for j in range(len(A))] for i in range(len(A))]) is None


def plant_strip_c(N, sig):
    """m1c's PLANT-STRIP on det Q_c: F_p' = det Q_c (cosh(c sigma) - cos al), c = 3/4, negative at al = i (1 + c) sigma / 2: the cover
    must fail"""
    c = arb(3) / 4
    ch = (c * arb(sig)).cosh()
    fp = lambda N_, al: [det_Qc(N_, al)[0] * (ch - al.cos())]
    neg_ok = fp(N, acb(0, (1 + c) * arb(sig) / 2))[0].real < 0
    ok, nb, bad = cover(N, sig, fp, CDMAX)
    return neg_ok and ok is False and bad is not None


def dndec(x, sig=12):
    """a decimal string <= x (W1), from the exact lower end"""
    m, e = x.lower().man_exp()
    u = Fr(int(m)) * Fr(2) ** int(e)
    if u == 0:
        return '0'
    return _dec(u, sig, True) if u > 0 else '-' + _dec(-u, sig, False)


def prop_line(N):
    t0 = cpu()
    ok, nint, dmin, where = c_prop(N)
    wh = ('[%s, %s]' % where) if isinstance(where, tuple) else str(where)
    out('C-PROP N=%d (Q_c = Q - 2 T(1/300), interval LDL^T): %s, %d al-intervals tiling [0, pi]%s; smallest pivot >= %s on x in %s pi '
        '(%.1f s)' % (N, 'PASS' if ok else 'FAIL', nint, ' and the reflection' if N == 3 else '', dndec(dmin) if dmin is not None else '-',
                      wh, cpu() - t0))
    return ok, where


def run_cov(N):
    STAGE[0] = 'C-PROP'
    ok, where = prop_line(N)
    if not ok:
        raise NotCert('C-PROP failed')
    out('CHECK PLANT-PROP %s' % ('FIRED' if plant_prop(N, where) else 'DID-NOT-FIRE'))
    STAGE[0] = 'cover ladder'
    t0 = cpu()
    sig, nb, tc = ladder(N, (0.5, 0.375, 0.25), det_Qc, CDMAX)
    out('COVER N=%d Re det Q_c > 0: %s (%d boxes, %.1f s)' % (N, ('certified at sigma %g, M = %d' % (sig, SIG_LADDER[str(sig)]))
                                                            if sig else 'no sigma of the ladder certified', nb, cpu() - t0))
    if sig:
        out('CHECK PLANT-STRIP %s' % ('FIRED' if plant_strip_c(N, sig) else 'DID-NOT-FIRE'))


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


# ------------------------------------------------------------------ m2bc: the assembly item (C-CORE as in px08_m2bb2, byte for byte)
NODE_SRC = '/mnt/g2/release/root/code/pk05/s4c_m2bb.py'
CORE_MARKS = ('# ==== NODE CORE A BEGIN (s4c_m2bb.py lines 84-636, byte for byte) ====', '# ==== NODE CORE A END ====',
              '# ==== NODE CORE B BEGIN (s4c_m2bb.py lines 638-836, byte for byte) ====', '# ==== NODE CORE B END ====')
CORE_REF = ((84, 636), (638, 836)); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_SELF = '16de53b1cc8512611a0373e44a5ec82451210854abcac5705b94bf1cd330da53'  # G-ORIG: option (C), acc2 two-producer acceptance


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


def c_block_t(N, plant=False):
    """C-BLOCK-T: at al = 0.7, 2.3 and the complex point 0.3 + 0.2i (Z1: off the axis kapT = 1/kap differs from conj(kap), so a conj or
    swap error in the block form shows there), the product of the Q_c block dets against det of the full Q_c, and E_c[H1^2] (moments to
    degree 4) from the blocks against the full matrices; each pair must overlap, with radii <= 1e-20 relative, so that a 1e-10 move cannot
    hide. plant=True (PLANT-BLOCK-T) moves one T_block entry of the first block by 1e-10"""
    ok = True
    for al in (acb(arb(7) / 10), acb(arb(23) / 10), acb(arb(3) / 10, arb(2) / 10)):
        dprod, BC = acb(1), [[] for _ in range(NF)]
        for b, (kap, kapT) in enumerate(comps(N, al)):
            Qb = Qc_block(kap, kapT, plant and b == 0)
            dprod = dprod * Qb.det()
            Cb = Qb.inv()
            for f, Bb in enumerate(B_blocks(kap, kapT)):
                BC[f].append(Bb * Cb)
        k = kw(N, al)[0]
        Q = Qc_full(k)
        C = Q.inv()
        pairs = ((dprod, Q.det()), (pe(P10[1], gfmom_lists(BC, 4)), pe(P10[1], gfmom_lists([[Bf * C] for Bf in forms2(k)], 4))))
        for x, z in pairs:
            tight = zrad(x) <= x.abs_lower() / 10 ** 20 and zrad(z) <= z.abs_lower() / 10 ** 20
            ok = ok and tight and x.overlaps(z)
    return ok


def c_flt_t(N):
    """C-FLT-T (V3 on Q_c): E_c[H1^4], E_c[h_lo^4] and the one-forms at al = 0.7 and 2.3 against pk10's float GFMom on twlib2.mats'
    Q - 2 twlib2.tilt2(k, 1/300, AV_F, EPS_F), each value against itself: |a - f| <= FLT_TOL |f| (the float error is about
    eps S_abs/|E P|, at most about 1e-11 here). Returns (ok, worst, planted ok): PLANT-FLT-T multiplies the H1^4 value by 1 + 1e-7 and
    runs the same test"""
    pm = T2.pmul
    F10 = {e: float(c.mid()) for e, c in P10[2].items()}
    Fh2 = {tuple(e[:6]): c for e, c in T2.hbar2(2, AV_F, T_F).items()}
    flo = {e: c for e, c in Fh2.items() if sum(e) <= SPLIT}
    flo2 = pm(flo, flo)
    flo4 = pm(flo2, flo2)
    worst = worst_p = 0.0
    for al in (0.7, 2.3):
        kn = k_np_of(N, al)
        Qf, Bsf, _ = T2.mats(kn)
        Ct = np.linalg.inv(Qf - 2 * T2.tilt2(kn, T_F, AV_F, EPS_F))
        fv = [GFMom(Bsf, Ct, 8).E(F10), GFMom(Bsf[:6], Ct, 12).E(flo4)] + [GFMom([Bsf[v]], Ct, 20).E({(m,): 1.0}) for v, m in V1M]
        av = [float(x.real.mid()) for x in tables_c(N, acb(al))[2]]
        avp = [av[0] * (1 + 1e-7)] + av[1:]
        worst = max(worst, max(abs(a - f) / abs(f) for a, f in zip(av, fv)))
        worst_p = max(worst_p, max(abs(a - f) / abs(f) for a, f in zip(avp, fv)))
    return worst <= FLT_TOL, worst, worst_p <= FLT_TOL


def tiling_ok(keys, x0, x1):
    ks = sorted(keys)
    return bool(ks) and ks[0][0] == x0 and ks[-1][1] == x1 and all(ks[i][1] == ks[i + 1][0] for i in range(len(ks) - 1))


def read_parts_c(N, man):
    """the twelve partial outputs (4 node, 8 G; paths and sha256 in man), all of this file at this SIGC"""
    me = sha_file(os.path.abspath(__file__))
    nodes, refl, boxes, subs, checks, seen = {}, [None], [], {}, [], []
    for line in open(man):
        h, p = line.split()
        assert sha_file(p) == h, 'sha mismatch %s' % p
        lines = open(p).read().split('\n')
        hd = lines[0].split()
        assert hd[0] == 'px08_m2bc3' and ACC.ok(p, hd[2], me, ORIG_SELF) and hd[3] == 'ITEM=' + MODE and hd[6] == 'SIGC=' + SIGC, 'header %s' % p
        seen.append(hd[4])
        assert any(x.strip() == 'VERDICT PART-DONE' for x in lines), 'not done %s' % p
        node_parse(lines, nodes, refl)
        for x in lines:
            w_ = x.split()
            if w_ and w_[0] == 'BOX':
                g = [unex(w_[i], w_[i + 1]) for i in range(3, len(w_), 2)]
                assert len(g) == NC
                boxes.append(((Fr(w_[1]), Fr(w_[2])), g))
            elif w_ and w_[0] == 'SUB':
                g = None if w_[5:] == ['FAIL'] else [unex(w_[i], w_[i + 1]) for i in range(5, len(w_), 2)]
                assert g is None or len(g) == len(CHEAP_C)
                subs.setdefault((Fr(w_[1]), Fr(w_[2])), []).append((Fr(w_[3]), Fr(w_[4]), g))
            elif w_ and w_[0] == 'CHECK':
                checks.append((w_[1], w_[-1]))
    assert sorted(seen) == sorted(list(node_parts()) + list(G_E)), seen
    assert sorted(nodes) == list(range(M_C // 2 + 1)) and (refl[0] is not None) == (N == 3)
    keys = [k for k, g in boxes]
    assert len(set(keys)) == len(keys) and tiling_ok(keys, 0, 1), 'box tiling of [0, 1]'
    assert sorted(subs) == sorted(keys)
    for k in keys:
        sb = sorted(subs[k], key=lambda s: s[0])
        assert len(sb) == G_SUB and tiling_ok([(s[0], s[1]) for s in sb], k[0], k[1]), 'sub-box tiling %s' % (k,)
        subs[k] = sb
    assert sorted(c for c, r in checks) == sorted(['C-CONJ'] + ['C-EVEN'] * len(node_parts()) + ['PLANT-DET'] * len(G_E))
    return nodes, refl[0], sorted(boxes), subs, checks


def run_asm_c(N):
    fails, fires = [], []
    K = M_C // 2
    nodes, refl, boxes, subs, checks = read_parts_c(N, sys.argv[5])
    keys = [k for k, g in boxes]
    out('PARTITION N=%d: nodes 0..%d once each, reflection %s, %d G boxes tiling [0, 1] pi, %d sub-boxes tiling each: PASS' % (
        N, K, 'yes' if refl else 'no', len(boxes), G_SUB))
    fires.append(('PLANT-TILE', not tiling_ok(keys[1:], 0, 1)))
    for c, r in checks:
        out('%s (partial item): %s' % (c, r))
        if r != ('FIRED' if c == 'PLANT-DET' else 'PASS'):
            fails.append(c)
    ok, info = c_core()
    out('C-CORE N=%d (shared core = s4c_m2bb.py lines 84-636 and 638-836): %s, block lines %s' % (N, 'PASS' if ok else 'FAIL', info))
    if not ok:
        fails.append('C-CORE')
    fires.append(('PLANT-CORE', not c_core(True)[0]))
    STAGE[0] = 'C-PROP'
    ok, where = prop_line(N)
    if not ok:
        fails.append('C-PROP')
    fires.append(('PLANT-PROP', ok and plant_prop(N, where)))
    STAGE[0] = 'C-COVER'
    sig, nb, tc = ladder(N, (SIG_C,), det_Qc, CDMAX)
    out('C-COVER N=%d Re det Q_c at sigma %g: %s (%d boxes)' % (N, SIG_C, 'PASS' if sig else 'FAIL', nb))
    if not sig:
        fails.append('C-COVER')
    fires.append(('PLANT-STRIP', plant_strip_c(N, SIG_C)))
    TM = tm_c(nodes)
    TH = [(nodes[0][i] + nodes[K][i] + 2 * sum((nodes[k][i] for k in range(2, K, 2)), arb(0))) * 2 / M_C for i in range(NC)]
    caps = caps_from_tm(TM)

    def stop_ok(k, g):
        return k[1] - k[0] <= Fr(1, 128) or all(g[i] <= caps[i] for i in REFINE_C)
    ok = all(stop_ok(k, g) for k, g in boxes)
    out('C-REFINE-C N=%d (every box of width pi/128 or within the caps %s): %s' % (
        N, ', '.join('%s %s' % (NAMES_C[i], updec(caps[i])) for i in REFINE_C), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-REFINE-C')
    gp = list(boxes[0][1])
    gp[REFINE_C[0]] = caps[REFINE_C[0]] * 2 + 1
    fires.append(('PLANT-REFINE-C', not stop_ok((Fr(0), Fr(1, 32)), gp)))
    G = []
    for i in range(NC):
        per_box = []
        for (k, g) in boxes:
            c = g[i]
            sb = subs[k]
            if i in CHEAP_C and all(s[2] is not None for s in sb):
                m = maxup([s[2][CHEAP_C.index(i)] for s in sb])
                c = m if m < c else c
            per_box.append(c)
        G.append(maxup(per_box))
    err = [(2 * G[i] / ((arb(SIG_C) * M_C).exp() - 1)).upper() for i in range(NC)]
    errh = [(2 * G[i] / ((arb(SIG_C) * (M_C // 2)).exp() - 1)).upper() for i in range(NC)]
    out('G line N=%d: Im al = %g (the boundary line of the C-COVER strip), M = %d, %d boxes, %d sub-boxes each' % (N, SIG_C, M_C,
                                                                                                             len(boxes), G_SUB))
    half = all((TM[i] + (-err[i]).union(err[i])).overlaps(TH[i] + (-errh[i]).union(errh[i])) for i in range(NC))
    out('C-HALF N=%d: %s' % (N, 'PASS' if half else 'FAIL'))
    if not half:
        fails.append('C-HALF')
    J = [TM[i] + (-err[i]).union(err[i]) + (refl[i] / 2 if N == 3 else 0) for i in range(NC)]
    miss = []
    for i in range(NC):
        tl = TM[i].abs_lower()
        within = err[i] <= TOLV * tl
        if not within:
            miss.append(NAMES_C[i])
        out('  N=%d I_c[%s] = %s; G %s, TW error %s, error/|T_M| %s%s' % (N, NAMES_C[i], J[i].str(12), updec(G[i]), updec(err[i]),
                                                                         updec(err[i] / tl) if tl > 0 else 'inf', '' if within else ' TARGET-MISS'))
    out('TARGET N=%d (TW error <= 1/10 |T_M|): %s; misses, reported: %s' % (
        N, 'all within' if not miss else '%d of %d miss' % (len(miss), NC), ', '.join(miss) or 'none'))
    STAGE[0] = 'controls'
    ok = c_block_t(N)
    out('C-BLOCK-T N=%d: %s' % (N, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-BLOCK-T')
    fires.append(('PLANT-BLOCK-T', not c_block_t(N, True)))
    ok, w_ = c_port(N)
    out('C-PORT N=%d: worst %.3e: %s' % (N, w_, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-PORT')
    fires.append(('PLANT-PORT', not c_port(N, 'B')[0]))
    fires.append(('PLANT-PORT-T', not c_port(N, 'T')[0]))
    ok, w_ = c_hbar()
    out('C-HBAR (U1, per-degree scale): worst %.3e: %s' % (w_, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-HBAR')
    fires.append(('PLANT-HBAR', not c_hbar(True)[0]))
    ok, w_, okp = c_flt_t(N)
    out('C-FLT-T N=%d: worst %.3e: %s' % (N, w_, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-FLT-T')
    fires.append(('PLANT-FLT-T', not okp))
    ok = not (set(HLO) & set(HHI)) and set(HLO) | set(HHI) == set(HB[2]) and all((HLO.get(e) or HHI.get(e)) is HB[2][e] for e in HB[2])
    out('C-SPLIT: %s' % ('PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-SPLIT')
    drop = dict(HHI)
    drop.pop(sorted(drop)[0])
    fires.append(('PLANT-SPLIT', set(HLO) | set(drop) != set(HB[2])))
    need = [(10, max(sum(e) for e in P10[2])), (6, max(sum(e) for e in P6[3])), (1, max(m for v, m in V1M))]
    plan = {10: 8, 6: 12, 1: 20}
    ok = all(d <= plan[F] for F, d in need)
    out('C-COVERS: needed degrees %s against %s: %s' % (need, plan, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-COVERS')
    short = dict(plan)
    short[6] = 11
    fires.append(('PLANT-COVERS', not all(d <= short[F] for F, d in need)))
    pos = all(J[i].upper() > 0 for i in range(NC))
    out('C-POS N=%d (U4: every upper end J_i^+ > 0, before the logs and roots of the reading): %s' % (N, 'PASS' if pos else 'FAIL'))
    fires.append(('PLANT-POS', not all(x.upper() > 0 for x in [arb(0)] + J[1:])))
    if not pos:
        out('CHECKS FAIL: %s' % '; '.join(fails + ['C-POS']))
        out('VERDICT INVALID')
        return
    STAGE[0] = 'reading'
    U = {nm: J[i].upper() for i, nm in enumerate(NAMES_C)}
    hi = arb(0)
    for e, c in HHI.items():
        term = c.abs_upper()
        for vv in range(6):
            if e[vv]:
                term = term * (U['%s^%d' % (X6F[vv], 4 * sum(e))].log() * e[vv] / (4 * sum(e))).exp()
        hi = hi + term
    N4c = U['h_lo^4'].sqrt().sqrt() + hi
    t = T_A
    rho4 = (t * U['H1^4'].sqrt().sqrt() + t * t / 2 * N4c) ** 4 / 24
    pref = pref_arb(N)
    out('CHECKS %s' % ('all PASS' if not fails else 'FAIL: ' + '; '.join(fails)))
    out('PLANTS %s' % ' '.join('%s:%s' % (nm, 'FIRED' if f else 'DID-NOT-FIRE') for nm, f in fires))
    valid = not fails and all(f for nm, f in fires)
    out('READING N=%d (t = 1/300, every J >= 300; S4_M2C_DESIGN_v1): pref^2 rho4 <= %s; N4_c <= %s; I_c[H1^4] <= %s; pref^2 <= %s' % (
        N, updec(pref * pref * rho4), updec(N4c), updec(U['H1^4']), updec(pref * pref)))
    out('VERDICT %s' % ('VALID' if valid else 'INVALID'))


def main():
    N = 4 if MODE == 'n4' else 3
    try:
        if PART == 'cov':
            run_cov(N)
        elif PART in G_E:
            run_g_c(N)
        elif PART == 'asm':
            run_asm_c(N)
            out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            return
        else:
            run_nodes_c(N)
    except NotCert as e:
        out('NOTCERT %s' % e)
        out('VERDICT INCOMPLETE')
        return
    out('VERDICT PART-DONE')
    out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    main()
