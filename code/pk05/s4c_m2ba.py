#!/usr/bin/env python3
"""s4c_m2ba.py -- pk05, S4 port (PK10 19.4, two-column twisted trace), milestone 2, group (a) of route I (S4_M2_DESIGN_v2, 4b7cc35f):
the third-order part pref^2 int dmu det(Q_k)^-1/2 E_k[1 + t E1 + t^2 E2 + t^3 E3] (E1 = H1, E2 = P2 = H2 + H1^2/2, E3 = H3 + H1 H2 + H1^3/6),
with E3 exact (degree 6), certified for every t in [0, 1/300]. Extends s4c_m2a1
(443c52c2, VALID at both N, outputs b2647cf9) whose parts f1b, f3 it reuses unchanged; f2 becomes g2 (moments to degree 6 with E3).

SPEC (as s4c_m2a1, with these changes).
(1)-(2) Series and block split: unchanged; E3 is formed exactly from H1, H2, H3 (Fractions), then converted to arb.
(3) Moments: GFMom to degree 6 (E3 has degree <= 6 in the forms).
(4) Quadrature: the four integrals J0, J1, J2, J3 = int dmu dq E_k[1, E1, E2, E3] by TW on the leading strip (sigma the first of SIG_LEAD whose
  cover certifies), G by direct acb evaluation on boxes of Im al = sigma (each integrand is w det^{-1/2} times a moment formula, rational in
  the entries of Q_k, hence analytic where Re det Q_k > 0).
(5) Uniformity: with c_i = J_i/J0 certified > 0 (C-POS), pref^2 J0 (1 + c1 t + c2 t^2 + c3 t^3) increases in t, so its value at t = 1/300 is its
  supremum over [0, 1/300] (PK10's m1 argument, now certified).
Checks: C-HASH; C-SERIES (with PLANT-SERIES, 2^-40 max(1, |c|)); C-PORT; C-BLOCK (det Q_k, E H1, E P2, E E3; with PLANT-BLOCK); C-FINITE
  (the N4 on REVIEW_S4_M1: pref and J0..J3 are finite balls); C-COVER, C-EVEN, C-CONJ, C-HALF (each integral); C-NORM; C-C123 (c1, c2, c3
  within 1e-6 of twrig6z's 0.846041, 0.639526, 0.498944 at N = 4 and 0.742488, 0.537950, 0.438039 at N = 3, as sp0 printed them), with
  PLANT-C123 (c3 x (1 + 1e-4) leaves the window); C-POS (c1, c2, c3 > 0); C-FLT (E3 at al = 0.7 and 2.3 from the acb blocks against pk10's
  float GFMom on twlib2.mats, both loaded read-only after C-HASH, relative 1e-9), with PLANT-FLT (the acb value x (1 + 1e-7) fails);
  C-TW3 (the third order at t = 1/300 within 1e-8 of twrig6z's 1.0331520608 (N = 4) and 1.0327952789 (N = 3), sp0's outputs; evidence that the
  same quantity is computed).
Reading: J0..J3, c1..c3, and the certified third-order bound U3 = pref^2 J0 (1 + c1/300 + c2/300^2 + c3/300^3), valid for every J >= 300.
Items: n4, n3. Usage: s4c_m2ba.py n4|n3 LIM (5 <= LIM <= 540).
"""
import resource, sys, time, math, hashlib, signal, os
from fractions import Fraction as Fr
ITEMS = ('n4', 'n3')
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: s4c_m2ba.py n4|n3 LIM')
    sys.exit(2)
MODE, LIM = sys.argv[1], int(sys.argv[2])
if not (5 <= LIM <= 540):
    print('bad LIM %d' % LIM)
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


out('s4c_m2ba sha256 %s ITEM=%s LIM=%d' % (sha_file(os.path.abspath(__file__)), MODE, LIM))
_bad = ['%s %s' % (n_, sha_file(os.path.join(SCR, n_))) for n_ in sorted(SOURCES) if sha_file(os.path.join(SCR, n_)) != SOURCES[n_]]
out('C-HASH %s (%d sources)%s' % ('PASS' if not _bad else 'FAIL', len(SOURCES), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
import numpy as np
from flint import arb, acb, arb_mat, acb_mat, ctx
sys.path.insert(0, SCR)
import twlib2 as T2
from gfmom import GFMom
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


HX = H_series_exact(3)
PH1 = to_arb(HX[1])
PP2 = to_arb(padd(HX[2], pscale(pmul(HX[1], HX[1]), Fr(1, 2))))
PE3 = to_arb(padd(HX[3], pmul(HX[1], HX[2]), pscale(pmul(pmul(HX[1], HX[1]), HX[1]), Fr(1, 6))))
C123_REF = {4: ('0.846041', '0.639526', '0.498944'), 3: ('0.742488', '0.537950', '0.438039')}
TW3_TOL = '1e-8'
FLT_TOL = 1e-9


def c_port(N):
    """the acb Q_k and B_f against twlib2.mats (floats) at al = 0.7, 2.3 and the N = 3 reflection, entrywise"""
    worst = 0.0
    for al in [0.7, 2.3] + ([None] if N == 3 else []):
        if al is None:
            k_np, k = np.array([[1.0, 0.0], [0.0, -1.0]]), kw(N, None)[0]
        else:
            c, s = math.cos(al), math.sin(al)
            k_np = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]) if N == 4 else np.array([[c, -s], [s, c]])
            k = kw(N, acb(al))[0]
        Qf, Bsf, _ = T2.mats(k_np)
        for Ma, Mf in [(Qmat2(k), Qf)] + list(zip(forms2(k), Bsf)):
            for i in range(Ma.nrows()):
                for j in range(Ma.ncols()):
                    worst = max(worst, float((Ma[i, j] - acb(float(Mf[i, j]))).abs_upper()))
    return worst <= 1e-13, worst


def c_block(N, plant=False):
    """det Q_k, E_k H1, E_k P2, E_k E3 from the full matrices against the 6 x 6 blocks, at al = 0.7 and 0.3 + 0.2 i"""
    ok, worst = True, 0.0
    for al in (acb(arb('0.7')), acb(arb('0.3'), arb('0.2'))):
        f = moments_full(N, al)[1:]
        b = moments_at(N, al, plant)[1:]
        for x, y in zip(f, b):
            ok = ok and x.overlaps(y)
            worst = max(worst, float((x - y).abs_upper()))
    return ok, worst


def c_flt(N, plant=False):
    """E_k E3 at al = 0.7 and 2.3: the acb blocks against pk10's float GFMom on twlib2.mats (relative FLT_TOL)"""
    HF = T2.H_series(3)
    pm, pa, ps = T2.pmul, T2.padd, T2.pscale
    E3f = pa(HF[3], pm(HF[1], HF[2]), ps(pm(pm(HF[1], HF[1]), HF[1]), 1.0 / 6))
    ok, worst, vals = True, 0.0, []
    for al in (0.7, 2.3):
        c, s = math.cos(al), math.sin(al)
        k_np = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]) if N == 4 else np.array([[c, -s], [s, c]])
        Qf, Bsf, _ = T2.mats(k_np)
        vf = GFMom(Bsf, np.linalg.inv(Qf), 6).E(E3f)
        va = moments_at(N, acb(al))[4].real
        if plant:
            va = va * (1 + arb('1e-7'))
        rel = abs(float(va.mid()) - vf) / abs(vf)
        worst = max(worst, rel)
        ok = ok and rel <= FLT_TOL
        vals.append('%.12g / %.12g' % (float(va.mid()), vf))
    return ok, worst, vals


def certify(N, fails, fires):
    STAGE[0] = 'N=%d series' % N
    t0 = cpu()
    ok, worst, bad = c_series(HX)
    out('C-SERIES N=%d: H1, H2, H3 with %d, %d, %d terms; E3 with %d terms; max relative coefficient error %.2e: %s%s' % (
        N, len(HX[1]), len(HX[2]), len(HX[3]), len(PE3), worst, 'PASS' if ok else 'FAIL', '' if ok else ' ' + '; '.join(bad)))
    if not ok:
        fails.append('C-SERIES')
    pok, pw, pbad = c_series(HX, plant=True)
    out('PLANT-SERIES N=%d: one H2 coefficient moved by 2^-40 max(1, |c|): C-SERIES %s: %s' % (N, 'passes' if pok else 'fails',
                                                                                             'DID-NOT-FIRE' if pok else 'FIRED'))
    fires.append(('PLANT-SERIES N=%d' % N, not pok))
    STAGE[0] = 'N=%d port' % N
    ok, worst = c_port(N)
    out('C-PORT N=%d: Q_k and the ten B_f against twlib2.mats, max entry difference %.2e: %s' % (N, worst, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-PORT N=%d' % N)
    STAGE[0] = 'N=%d block' % N
    t1 = cpu()
    ok, worst = c_block(N)
    out('C-BLOCK N=%d: det Q_k, E H1, E P2, E E3 full against blocks at al = 0.7, 0.3 + 0.2 i: max |difference| %.2e: %s (%.1f s)' % (
        N, worst, 'PASS' if ok else 'FAIL', cpu() - t1))
    if not ok:
        fails.append('C-BLOCK N=%d' % N)
    pok, pw = c_block(N, plant=True)
    out('PLANT-BLOCK N=%d: the + block with k^T -> e^{i al}: C-BLOCK %s: %s' % (N, 'passes' if pok else 'fails', 'DID-NOT-FIRE' if pok else 'FIRED'))
    fires.append(('PLANT-BLOCK N=%d' % N, not pok))
    STAGE[0] = 'N=%d flt' % N
    ok, worst, vals = c_flt(N)
    out('C-FLT N=%d: E E3 acb / pk10 float at al = 0.7, 2.3: %s; max relative difference %.2e (tolerance %g): %s' % (
        N, ', '.join(vals), worst, FLT_TOL, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-FLT N=%d' % N)
    pok, pw, pv = c_flt(N, plant=True)
    out('PLANT-FLT N=%d: the acb value x (1 + 1e-7): max relative difference %.2e: C-FLT %s: %s' % (N, pw, 'passes' if pok else 'fails',
                                                                                              'DID-NOT-FIRE' if pok else 'FIRED'))
    fires.append(('PLANT-FLT N=%d' % N, not pok))
    STAGE[0] = 'N=%d cover' % N
    pref = pref_arb(N)
    sig, nb, tc = ladder(N, SIG_LEAD, det_Q, CDMAX)
    out('C-COVER N=%d det Q_k (blocks): %s' % (N, ('PASS: sigma %g certified on %d boxes (%.1f s)' % (sig, nb, tc)) if sig else 'FAIL'))
    if not sig:
        fails.append('C-COVER N=%d' % N)
        return
    STAGE[0] = 'N=%d integrals' % N
    Js = integral(N, sig, M_MOM, ev_mom, ('J0 = int dmu dq', 'J1 = int dmu dq E E1', 'J2 = int dmu dq E E2', 'J3 = int dmu dq E E3'), fails)
    fin = pref.is_finite() and all(x.is_finite() for x in Js)
    out('C-FINITE N=%d: pref and J0..J3 finite: %s' % (N, 'PASS' if fin else 'FAIL'))
    if not fin:
        fails.append('C-FINITE N=%d' % N)
        return
    J0 = Js[0]
    lead = pref * pref * J0
    nok = (lead - arb(LEAD_REF)).abs_upper() <= arb(NORM_TOL)
    out('C-NORM N=%d: pref^2 J0 = %s: %s' % (N, lead.str(15), 'PASS' if nok else 'FAIL'))
    if not nok:
        fails.append('C-NORM N=%d' % N)
    cs = [Js[i] / J0 for i in (1, 2, 3)]
    tol = arb(C12_TOL)
    cok = all((cs[i] - arb(C123_REF[N][i])).abs_upper() <= tol for i in range(3))
    out('C-C123 N=%d: c1 = %s, c2 = %s, c3 = %s (twrig6z %s), window %s: %s' % (N, cs[0].str(12), cs[1].str(12), cs[2].str(12),
                                                                           ', '.join(C123_REF[N]), C12_TOL, 'PASS' if cok else 'FAIL'))
    if not cok:
        fails.append('C-C123 N=%d' % N)
    pc = (cs[2] * (1 + arb('1e-4')) - arb(C123_REF[N][2])).abs_lower() > tol
    out('PLANT-C123 N=%d: c3 x (1 + 1e-4) = %s: %s' % (N, (cs[2] * (1 + arb('1e-4'))).str(12), 'FIRED' if pc else 'DID-NOT-FIRE'))
    fires.append(('PLANT-C123 N=%d' % N, pc))
    pos = all(x > 0 for x in cs)
    out('C-POS N=%d: c1, c2, c3 > 0: %s' % (N, 'PASS' if pos else 'FAIL'))
    if not pos:
        fails.append('C-POS N=%d' % N)
    t = arb(1) / 300
    U3 = lead * (1 + cs[0] * t + cs[1] * t * t + cs[2] * t ** 3)
    tw_ok = (U3 - arb(TW3[N])).abs_upper() <= arb(TW3_TOL)
    out('C-TW3 N=%d: U3 = pref^2 J0 (1 + c1 t + c2 t^2 + c3 t^3) at t = 1/300 = %s; twrig6z %s: |difference| <= %s: %s' % (
        N, U3.str(15), TW3[N], (U3 - arb(TW3[N])).abs_upper().str(3), 'PASS' if tw_ok else 'FAIL'))
    if not tw_ok:
        fails.append('C-TW3 N=%d' % N)
    out('READING N=%d: J0 %s, J1 %s, J2 %s, J3 %s; certified third-order bound for every J >= 300 (c_i > 0, so the sup over t in [0, 1/300] is at'
        ' t = 1/300): U3 <= %s' % (N, Js[0].str(15), Js[1].str(15), Js[2].str(15), Js[3].str(15), U3.upper().str(15)))
    out('TIME N=%d: %.1f s' % (N, cpu() - t0))


def main():
    N = 4 if MODE == 'n4' else 3
    fails, fires = [], []
    try:
        certify(N, fails, fires)
    except NotCert as e:
        fails.append('NotCert: %s' % e)
    out('CHECKS %s' % ('all PASS' if not fails else 'FAIL: ' + '; '.join(fails)))
    out('PLANTS %s' % ' '.join('%s:%s' % (nm, 'FIRED' if f else 'DID-NOT-FIRE') for nm, f in fires))
    valid = not fails and fires and all(f for nm, f in fires)
    out('VERDICT %s' % ('VALID' if valid else 'INVALID'))
    out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    main()
