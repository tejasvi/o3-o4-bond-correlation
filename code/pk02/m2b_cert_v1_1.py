#!/usr/bin/env python3
"""m2b_cert_v1_1.py -- pk02 (code/pk02/). REVISION of m2b_cert_v1.py (c47e59df, never run) on the review
REVIEW_M2B_CERT_v1_rv03_v1.md (8c943f19). Changes, and nothing else (DIFF_m2b_cert_v1_to_v1_1.txt):
  (1) sect. 1: the piece functions return their rows, and main() writes the hand-off only after every gate of the piece has passed
      (C-IMPORT, BOUND, C-TILT (a) and (b), C-R0, PLANT-R0, C-RAD-MA, the C-SING and PLANT-SING merges), with fails and fires empty and
      the piece complete, through a guarded writer; PLANT-NOWRITE (as pk03's m3_run_v1_6_1): with a failed gate and a recording opener
      that raises when called, the writer must return without opening anything. A piece that fails leaves no hand-off.
  (2) sect. 3: the hand-off HEAD carries the exact boundaries a_m, a_e, a_pp ('p/q') and RHO_PP_HEX; every assert is an explicit raise
      (make_condE's caps check, restrict6, up_float, the exactness of a_m, a_e, a_pp, chi_tail's x > 0, W9 and W2 against their integer
      forms, to9, the hand-off path and size, kappa_B > 0, D5's and R0's variables, surely_pd of A - 2 c_e t I); C-IMPORT: the imported
      arbeng_c2b_v2 and arbeng_ma_v1_3 are the hashed files.
  Names: records out_m2b_cert_v1_1_*, hand-offs hand_m2b_cert_v1_1_*; the header line names m2b_cert_v1_1.
m2b_cert_v1 was: M2(b)'s port items in balls: the pieces that compute the near-region parameters of the
certified vacuum record M2B_KV_v1, per SPEC_M2B_CERT_v1.md (ffd842a2) with ADD1 (2c97391f) and ADD2 (48d5fa54)
(sect. 3 SOUND) and the review c897cdd7, 41eaf157, 6fb765fd (sect. 4). The assembly (M3's entries, pk08's Rtr, LAW v1's C-FMT values, the
record) is m2b_asm_v1.py, and the comparison with the FLOAT references (C-REP) is m2b_rep_v1.py; both read these pieces' hand-offs.
Trial vacuum: vacres_K3_N<N>_sym_v1.json (pk11/out; q1..q3 and m1..m3 exact binary64, free choices; its r2 and r3 keys are not used).
The engine is kt_cert_v1_7's (efe4c40d), cut to the vacuum: arbeng_c2b_v2 (fb8cd1b5) in arb at ctx.prec 512, and for D5's conditional
expectation the closed M-a layer arbeng_ma_v1_3 (075e3586; the review CLOSE 9a290b50: pinned, at prec 512, MAFallback the only exception
caught). The boundaries are exact (ADD1 sect. 1, ADD2 sect. 2): a_m = Fraction(0.55)^2, a_e = Fraction(0.6)^2, a_pp = Fraction(rho_pp)^2
with rho_pp the binary64 rounded up from the arb value of sin(asin 0.55 + 40 deg) (RHO_PP_HEX); every piece prints them on its BOUND line.
Pieces (argv[1] = <piece>.n<N>, N in {3, 4}; argv[2] = LIM, the RLIMIT_CPU soft limit in s, hard LIM + 5):
  x     the explicit part: L1 and L0 to order KX = 4 (vacmod2.Builder in balls), r_k = E[L1_k | s] - sum_{j <= k} m_j L0_{k-j} for k = 0..4
        (m_0 = 1, m_4 = 0; the conditional expectation through CondMomA at Dc 8, Q'' degree <= 2); C-R0 (r_0 is the exact zero polynomial)
        with PLANT-R0 (m_0 = 1 + 2^-52 must leave r_0 nonzero). At J1 = 150, Wishart norms under the tilted covariance G1 (rates c_m t):
        nP = sum_{k=2..4} t1^k ||r_k|| (Minkowski) and R1 = t1 ||r1||. At J0 = 170, for w in (wt, dl) (vacrig11w's split |w| <= |lin_w| + B_w,
        lin_wt = (Q_TM + Q_MB)/4 - kbar with m2's kbar of this N, lin_dl = (Q_TM - Q_MB)/4, B_w = t ((X_T - X_M)^2 + (X_M - X_B)^2)/(16 (1 - a_m))):
        nPM_w = sum_{k=2..4} t0^k (||lin_w r_k|| + ||B_w r_k||) and R1_w = t0 (||lin_w r1|| + ||B_w r1||).
  d5    D5 at J1 (vacrig11f l.294-313): Dbar(5, h, pis) at a_e in balls; its conditional expectation through arbeng_ma_v1_3's CondTable (K2)
        at (deg'', qdeg) = (11, 2) with chunk 40000000 (m2b_probe_v1_1: 15,176,954 entries, 266 s, 6.4 GB); nD = (t1^5/120) detf (n2 E2(ED,
        ED))^{1/2} by WishartA on G2 (rates c_m t, the quadratic term Delta = (A - 2 c_e t)^-1 - A^-1 on the sigma block).
  dw    D5 at J0, weighted: D5w_w = (t0^5/120) detf (||lin_w ED|| + ||B_w ED||) for w in (wt, dl).
  r0    R0 at J1 (vacrig11f l.316-327: sum_j |m_j| t^j t^{5-j}/(5-j)! Dbar_{5-j}(h0, L0 side at a_m)) and R0w_w at J0 (weighted norms).
  tX0, tX1, tX2   tailX at J1 for lambda = 0.3, 0.45, 0.6 (one piece each): three tables (tilt lambda X''_v, v = 0..2, on the rates c_m t)
        of degree 2 dT; per order k the norm E2(L_k, L_k) (Minkowski per order, vacmono l.119-131): acc = sum_v e^{-lambda J a_e} N_v
        (sum_k t^k E2_v(L_k, L_k)^{1/2})^2. The assembly takes tX = min over lambda of acc^{1/2} and freezes lambda* (LAW v1 needs >= 0.3).
  tB    tailB at J1 in kt_cert's F1 per-bond form (lambda 0.45, the quadratic tilt lambda Q_rr'', c = KAPPA_B in arb), Minkowski per order:
        three tables (r = 0..2), acc = sum_r e^{-0.45 J kappa} N_r (sum_k t^k E2_r(L_k, L_k)^{1/2})^2, tB = acc^{1/2}.
  tA    ann at J1 (vacrig11f l.375-388): pi0'' at a_pp; for each lambda three tables (rates c_m t outer, 2 c_pp t inner, tilt lambda X''_v);
        ann = min over lambda of (sum_v e^{-lambda J a_e} N_v E2(P0'', P0''))^{1/2}, lambda* frozen.
  The tail tables are arb AllMom2A tables with W9's exact zeros (C-SING, PLANT-SING), as kt_cert_v1_7's (SPEC sect. 2 allows M-a or arb).
Every piece: C-HASH, the BOUND line, C-TILT (rates rounded up, a_pp >= sin^2(asin rho_m + delta) in arb, PLANT-TILT), and a hand-off
(hand_m2b_cert_v1_1_<piece>.n<N>.txt: HEAD, rows of balls written by arb's str with radius (80 digits), END with the body's sha256) named
with its sha256 in the record (out_m2b_cert_v1_1_<piece>.n<N>.out); every record prints FORMAT M2B_PIECE_v1 CERTIFIED, the KERNEL line and
the LAYER line, and exactly one VERDICT line.
Run (own folder; a NEW record path each): D=/mnt/g2/release/root/code/pk02;
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=<AS> --
  python3 -I -B $D/m2b_cert_v1_1.py <piece>.n<N> <LIM> > $D/out_m2b_cert_v1_1_<piece>.n<N>.out
  2> $D/out_m2b_cert_v1_1_<piece>.n<N>.err
  (AS 16 GiB for d5 and dw, 8 GiB otherwise.)

"""
import resource, sys, time, math, hashlib, signal, os, traceback, re, json, itertools
from fractions import Fraction

PIECES = ('x', 'd5', 'dw', 'r0', 'tX0', 'tX1', 'tX2', 'tB', 'tA')
ITEMS = tuple('%s.n%d' % (p, n) for n in (4, 3) for p in PIECES)
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: m2b_cert_v1_1.py ITEM LIM   (ITEM = <piece>.n<N>, piece in %s, N 4 or 3; LIM = RLIMIT_CPU soft limit in s)' % ', '.join(PIECES))
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,4}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r (need 5 <= LIM <= 540)' % sys.argv[2])
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

OWN = '/mnt/g2/release/root/code/pk02'
WOUT = '/mnt/g2/release/root/code/pk11/out'          # the trial vacuum (read only)
SCRATCH = '/mnt/g2/release/root/code/pk10/scratch'    # m2's kbar (read only)
OWNFILES = {
    'arbeng_c2b_v2.py': '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0',
    'arbeng_ma_v1_3.py': '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be',
}
VALIDATION = [
    ('out/out_kt_ma_val_v1_5_v1.out', '5ccbb6d006f5365f219eb6221b7e66b76e7e7799e977148df94f34b0c3d86216'),
    ('out/out_kt_ma_val_v1_5_v2.out', 'a61d893e6424b9ea524d944e40f625c934de04a2faeaa741e3fd333e97f48817'),
    ('out/out_kt_ma_val_v1_5_v3.out', 'd613fe804a030be397fefa46ed1424063f794400b7d9618e12db8af046e09d93'),
    ('out/out_kt_ma_val_v1_5_v4.out', '2ad13ec3cac14ef919f5e34fa19664f70eece05c3c3f208dcfec36a93cdd4473'),
    ('../rv01/CLOSE_ARBENG_MA_V1_3_rv01.md', 'a8a5e8d020d2d1e1127c3ee8f400496011ddbd022af83180025ac3185ba22f95'),
]
TRIAL = {
    'vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    'vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
}
KBARF = {
    'm2_N3_J170.json.b': '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    'm2_N4_J170.json.b': '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


SELF_SHA = sha_file(os.path.abspath(__file__))
out('m2b_cert_v1_1 sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (SELF_SHA, MODE, LIM, LIM, LIM + 5))
_bad = []
for _d, _tab in ((OWN, OWNFILES), (WOUT, TRIAL), (SCRATCH, KBARF), (OWN, dict(VALIDATION))):
    for _n in sorted(_tab):
        _got = sha_file(os.path.join(_d, _n))
        if _got != _tab[_n]:
            _bad.append('%s %s' % (_n, _got))
out('C-HASH %s (%d engine files, %d trial-vacuum files, %d kbar files, %d validation records of the M-a layer)%s' % (
    'PASS' if not _bad else 'FAIL', len(OWNFILES), len(TRIAL), len(KBARF), len(VALIDATION), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, OWN)

import numpy as np
import flint
from flint import arb, arb_mat, ctx
ctx.prec = 512
import arbeng_c2b_v2 as ae
import arbeng_ma_v1_3 as ma
out('ENV: python-flint %s, numpy %s, python %s, ctx.prec %d' % (flint.__version__, np.__version__, sys.version.split()[0], ctx.prec))
out('FORMAT M2B_PIECE_v1 CERTIFIED')
out('KERNEL arbeng_c2b_v2.py %s ctx.prec %d' % (OWNFILES['arbeng_c2b_v2.py'], ctx.prec))
out('LAYER arbeng_ma_v1_3.py %s prec %d validation %s' % (OWNFILES['arbeng_ma_v1_3.py'], ma.PREC, ' '.join(h for _, h in VALIDATION)))

PIECE, SUFFIX = MODE.split('.', 1)
NN = int(SUFFIX[1])
nn = NN - 1
SQ5, SQ21 = arb(5).sqrt(), arb(21).sqrt()
A_ = (3 + SQ21) / 6
B_ = (3 * SQ5 - SQ21) / 12
TRI = [A_, A_, B_]
PAIRS = [(0, 1), (1, 2), (0, 2)]
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]
VFILE = {4: 'vacres_K3_N4_sym_v1.json', 3: 'vacres_K3_N3_sym_v1.json'}[NN]
KFILE = {4: 'm2_N4_J170.json.b', 3: 'm2_N3_J170.json.b'}[NN]
RHO_M, RHO_E = 0.55, 0.6                    # free radii (exact binary64)
DELTA = arb.pi() * 40 / 180                 # 40 degrees, in arb
J1, J0 = 150, 170                           # LAW v1's base and vacrig11w's J0
KX, NVX = 4, 12                             # the explicit series to order 4 in the twelve forms (no cross forms for the vacuum)
XS, QS, XD, QD = [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]
QGROUPS, QCAPS = [0, 0, 0, 1, 1, 1], {1: 2}   # vacrig11f's cm8: the Q'' degree capped at 2
NV12, BB = 12, 26
LAMS = (0.3, 0.45, 0.6)                     # tailX's and ann's Chernoff lambdas (free choices, exact binary64; lambda* frozen at J1)
LAM_B = 0.45                                # tailB's F1 lambda (kt_cert's LAM_T)
CHUNK = 40000000                            # the CondTable chunk (an int: the review, ADD2 sect. 3)
W2_INT = [[1, 0, 0, 1, 0, 1], [0, 1, 0, -1, 1, 0], [0, 0, 1, 0, -1, -1]]   # W2's exact integers (X_r -> e_r, Q_rs -> e_r - e_s)




# ====================================================================================== part 2a: the conditioning (vacrig11f's cm8)
def tri_laplacian():
    """the triangle Laplacian (A, A, B) as an arb_mat (couplings in arb)."""
    L = arb_mat(3, 3)
    for p, (r, s) in enumerate(PAIRS):
        c = TRI[p]
        L[r, r] += c
        L[s, s] += c
        L[r, s] -= c
        L[s, r] -= c
    return L



def build_conditioning():
    """vacrig11f's cm8 in balls (as kt_cert_v1_7's stage_c builds its CondMomA): phi'' = A^-1 phi + zeta, zeta ~ N(0, A^-1), A = I + L_tri;
    the six forms X'' (0-2) and Q'' (3-5) through the exact W2 (entries 0, +-1); degree Dc = 2 KX = 8, the Q'' degree capped at 2."""
    Ainv = (eye3() + tri_laplacian()).inv()
    return ae.CondMomA(Ainv, Ainv, w2_arb(), nn, 2 * KX, groups=QGROUPS, caps=QCAPS)


def w2_arb():
    """W2 (3 x 6): X_r -> e_r, Q_rs -> e_r - e_s (vacrig11f l.42-45), as an arb_mat of exact integers."""
    W2 = arb_mat(3, 6)
    for r in range(3):
        W2[r, r] = 1
    for p_, (r, s) in enumerate(PAIRS):
        W2[r, 3 + p_] = 1
        W2[s, 3 + p_] = -1
    return W2


def eye3():
    return arb_mat(3, 3, [1 if i == j else 0 for i in range(3) for j in range(3)])

def lin_g(cm, gi):
    """g_rr = X_r, g_rs = (X_r + X_s - Q_rs)/2 (exact halves)."""
    r, s = cm.gvars[gi]
    if r == s:
        return {tuple(1 if q == XS[r] else 0 for q in range(6)): arb(1)}
    qi = QS[PAIRS.index((r, s))]
    half = arb(1) / 2
    return {tuple(1 if q == XS[r] else 0 for q in range(6)): half, tuple(1 if q == XS[s] else 0 for q in range(6)): half,
            tuple(1 if q == qi else 0 for q in range(6)): -half}


def qcap_ok(e2):
    """the conditioned monomial e2 (forms X'' 0-2, Q'' 3-5) is inside the caps of build_conditioning."""
    return all(sum(x for x, g in zip(e2, QGROUPS) if g == k) <= cap for k, cap in QCAPS.items())






# ====================================================================================== part 2b1: series helpers (kt_c_v2_3 l.234-299)
Series, padd, pscale, pmul, pconst, pvar = ae.Series, ae.padd, ae.pscale, ae.pmul, ae.pconst, ae.pvar
WX = ae.w_coeffs(KX)                         # exact rationals as balls


def load_json(path):
    with open(path) as fh:
        return json.load(fh)

R3 = load_json(os.path.join(WOUT, VFILE))                       # the trial vacuum (exact binary64 data, sha256 pinned in TRIAL)
QV = [None, R3['q1'], R3['q2'], R3['q3']]
MSER = [1.0, R3['m1'], R3['m2'], R3['m3']]                       # m_0 = 1; the m_j are free choices (exact binary64), as pk08's MHAT_RULE


def ser(coeffs):
    return Series(KX, NVX, coeffs)


def zero():
    return ser([{} for _ in range(KX + 1)])


def one():
    return ser([pconst(1, NVX)] + [{} for _ in range(KX)])


def meas(i):
    return ser([{}] + [{tuple(k if j == i else 0 for j in range(NVX)): arb(1) / (2 * k)} for k in range(1, KX + 1)])


def anh(iu, iv, c):
    res = [{} for _ in range(KX + 1)]
    d2 = padd(pmul(pvar(iu, NVX), pvar(iu, NVX)), pscale(pmul(pvar(iu, NVX), pvar(iv, NVX)), -2), pmul(pvar(iv, NVX), pvar(iv, NVX)))
    for (i, j), cw in WX.items():
        k = 1 + i + j
        if k > KX:
            continue
        mono_ = {tuple((i if q == iu else 0) + (j if q == iv else 0) for q in range(NVX)): arb(1)}
        res[k] = padd(res[k], pscale(pmul(d2, mono_), -ae.A(c) * cw / 2))
    return ser(res)


def xi_pair(iu, iv, iq):
    return ser([pvar(iq, NVX, arb(1) / 2)] + [{} for _ in range(KX)]) - anh(iu, iv, 1)


def xis(Xi, Qi):
    return [xi_pair(Xi[r], Xi[s], Qi[p]) for p, (r, s) in enumerate(PAIRS)]


def mono_series(xs, mono_):
    res = one()
    for p in mono_:
        res = res * xs[p]
    return res


def shift(sr, sh):
    return ser([{} for _ in range(sh)] + [dict(P) for P in sr.c[:KX + 1 - sh]])


def vac_poly(xs):
    res = one()
    for coef, sh in ((QV[1], 1), (QV[2], 2), (QV[3], 3)):
        if sh > KX:
            continue
        for cb, mono_ in zip(coef, BASIS):
            if cb != 0.0:
                res = res + shift(mono_series(xs, mono_), sh).scale(arb(cb))
    return res


# ====================================================================================== part 2b2a: make_condE (kt_c_v2_3 l.333-396), sparse
def make_condE(cm):
    """kt_c_v2_3.make_condE in balls: E[. | sigma] of series coefficients as sigma polynomials of degree <= cm.Dc, through the g -> sigma map
    (g_rr = X_r, g_rs = (X_r + X_s - Q_rs)/2). Same sums as the float version; the g -> sigma rows are kept sparse (dicts of balls) instead
    of the dense matrix G2F, so no ball is ever formed for a structural zero."""
    D = cm.Dc
    Bs = D + 1
    pw = [Bs ** i for i in range(6)]
    lay = [np.zeros(1, dtype=np.int64)]
    for d in range(1, D + 1):
        lay.append(np.unique((lay[-1][:, None] + np.array(pw, dtype=np.int64)[None, :]).ravel()))
    scodes = np.unique(np.concatenate(lay))
    sexp = np.stack([(scodes // pw[i]) % Bs for i in range(6)], axis=1)
    sdeg = sexp.sum(axis=1).tolist()
    sidx = {int(c): k for k, c in enumerate(scodes.tolist())}
    scl = scodes.tolist()

    def mult(vec, e6, c, acc):
        """acc += c * (vec shifted by the sigma monomial e6), keeping total degree <= D."""
        de, ce = sum(e6), sum(int(x) * p for x, p in zip(e6, pw))
        for k, x in vec.items():
            if sdeg[k] + de <= D:
                d = sidx[scl[k] + ce]
                v = c * x
                acc[d] = acc[d] + v if d in acc else v

    lin = [lin_g(cm, gi) for gi in range(len(cm.gvars))]
    if len(cm.gvars) != 6:
        raise ValueError('make_condE: %d g variables, expected 6' % len(cm.gvars))
    rows = {tuple([0] * 6): {0: arb(1)}}

    def grow(gexp):
        if gexp not in rows:
            i = next(j for j, m in enumerate(gexp) if m > 0)
            prev = list(gexp)
            prev[i] -= 1
            base = grow(tuple(prev))
            v = {}
            for e6, c in lin[i].items():
                mult(base, e6, c, v)
            rows[gexp] = v
        return rows[gexp]
    cache = {}

    def condvec(e2):
        if not (sum(e2) <= D and qcap_ok(e2)):
            raise ValueError('make_condE: the conditioned monomial %r is outside the degree or the caps (no silent drop)' % (e2,))
        if e2 not in cache:
            acc = {}
            for g, val in cm.cond(e2).items():
                for k, x in grow(tuple(g)).items():
                    v = val * x
                    acc[k] = acc[k] + v if k in acc else v
            cache[e2] = acc
        return cache[e2]

    def condE(sr):
        res = []
        for P in sr.c:
            acc = {}
            for e, c in P.items():
                if sum(e) > D:
                    raise ValueError('condE: a term of degree %d > %d: %r' % (sum(e), D, e))
                mult(condvec(tuple(e[6:])), tuple(e[:6]), ae.A(c), acc)
            res.append({tuple(int(x) for x in sexp[k]): v for k, v in acc.items() if not v.is_zero()})
        return res
    return condE




# ---------------------------------------------------------------------------- small helpers (kt_cert_v1_7 l.510-534)
def nsqrt(x):
    """an enclosure of sqrt(max(x, 0)) for a ball x. F6: every argument is a second moment or a squared norm, never negative, so a
    certainly negative ball is a defect and stops the item (nonnegative_part would map it to 0 silently)."""
    if x < 0:
        raise ValueError('nsqrt of a certainly negative ball %s (F6)' % x.str(10, radius=True))
    return x.nonnegative_part().sqrt()


def fup(x):
    """an upper bound of |x| as a binary64 number (for printing and for the K-checks' tolerances)."""
    return float(x.abs_upper())


def restrict6(sr):
    res = []
    for P in sr.c:
        acc = {}
        for e, c in P.items():
            if sum(e[6:]) != 0:
                raise ValueError('restrict6: a sigma\'\' variable in %r' % (e,))
            k = tuple(e[:6])
            acc[k] = acc[k] + c if k in acc else ae.A(c)
        res.append({e: c for e, c in acc.items() if not c.is_zero()})
    return res




# ====================================================================================== part 3: majorants (kt_c_v2_3 l.629-762), NPolyA in balls
# Derived free parameters (pk01's C-RATE, C-APP): the tilt rates and the annulus radius are binary64 numbers rounded UP from their arb
# values, so every inequality the proof needs (rate >= -log(1 - a)/(2a), a_pp >= sin^2(asin rho_m + delta)) holds by construction.
def up_float(x):
    """a binary64 number >= every point of the ball x."""
    u = x.upper()
    f = float(u)
    if not (arb(f) >= u):
        f = math.nextafter(f, math.inf)
    if not (arb(f) >= u):
        raise ValueError('up_float: no binary64 at or above the ball')
    return f

# SPEC_M2B_CERT_v1_ADD1 sect. 1 and ADD2 sect. 2: one exact boundary per radius. a_m = Fraction(0.55)^2 and a_e = Fraction(0.6)^2, formed
# in arb at 512 bits from the binary64 radii (106-bit products, exact); rho_pp = the binary64 rounded UP from the arb value of
# sin(asin 0.55 + 40 deg), fixed by RHO_PP_HEX, and a_pp = Fraction(rho_pp)^2 (exact in arb). The tilt rates stay binary64 numbers rounded
# up from their arb values (C-RATE). kt_cert's binary64-rounded squares are not used.
a_m = arb(RHO_M) * arb(RHO_M)
a_e = arb(RHO_E) * arb(RHO_E)
if not (a_m.rad() == 0 and a_e.rad() == 0):
    raise ValueError('a_m or a_e is not exact in arb')
RHO_PP = up_float((arb(RHO_M).asin() + DELTA).sin())
RHO_PP_HEX = RHO_PP.hex()
a_pp = arb(RHO_PP) * arb(RHO_PP)
if not (a_pp.rad() == 0):
    raise ValueError('a_pp is not exact in arb')
c_m, c_e, c_pp = (up_float(-(1 - x).log() / (2 * x)) for x in (a_m, a_e, a_pp))
AVt = [a_m] * 3 + [None] * 3 + [a_e] * 3 + [None] * 3
ONE_P = ae.NPolyA(NV12, BB, np.zeros(1, dtype=np.int64), [arb(1)])


def mono(e, c=1):
    return ae.NPolyA(NV12, BB, np.array([int(sum(int(x) * BB ** i for i, x in enumerate(e)))], dtype=np.int64), [ae.A(c)])


def xv(i, k=1, c=1):
    e = [0] * NV12
    e[i] = k
    return mono(e, c)


def D2(i, j):
    return xv(i, 2).add(xv(i, 1).mul(xv(j, 1)).scale(-2)).add(xv(j, 2))


def Mk(i, j, k):
    return ONE_P if k == 0 else xv(i, k).add(xv(j, k))


def trade(p, t, nt):
    """kt_c_v2_3.trade: lower the largest exponent nt times, each time times its radius factor (a_m, a_e; 4 a_m, 4 a_e for Q); t if none."""
    ex = p.exponents()
    out_e, out_c = [], []
    qa = {3: 4 * a_m, 4: 4 * a_m, 5: 4 * a_m, 9: 4 * a_e, 10: 4 * a_e, 11: 4 * a_e}
    for row, c in zip(ex, p.coeffs):
        row = row.copy()
        fac = c
        for _ in range(nt):
            cand = [(row[i], i) for i in range(NV12) if row[i] > 0]
            if not cand:
                fac = fac * t
                continue
            _, i = max(cand)
            row[i] -= 1
            fac = fac * (AVt[i] if AVt[i] is not None else qa[i])
        out_e.append(row)
        out_c.append(fac)
    res = ae.NPolyA(NV12, BB, np.array(out_e, dtype=np.int64).reshape(-1, NV12) @ p.pw, out_c)
    res._normalize()
    return res


def cf_rad(aa, k):
    return 1 / (1 - arb(aa)) ** k


def hk(k, meas_vertices, bonds, cfac):
    res = ae.NPolyA(NV12, BB)
    for (v, av) in meas_vertices:
        res = res.add(xv(v, k, arb(math.factorial(k - 1)) / 2 * cfac(av, k)))
    for (iu, iv, c, aa) in bonds:
        res = res.add(D2(iu, iv).mul(Mk(iu, iv, k - 1)).scale((ae.A(c) / 2) * arb(math.factorial(k)) / 4 * cfac(aa, k + 1)))
    return res


def xibar(Xi, Qi, aa, t, nmax, cfac):
    res = []
    for p_, (r, s) in enumerate(PAIRS):
        Dx = D2(Xi[r], Xi[s])
        lst = [xv(Qi[p_], 1, arb(1) / 2).add(trade(Dx.scale(cfac(aa, 1) / 8), t, 1))]
        for l in range(1, nmax + 1):
            lst.append(Dx.mul(Mk(Xi[r], Xi[s], l - 1)).scale(arb(math.factorial(l)) / 8 * cfac(aa, l + 1)))
        res.append(lst)
    return res


def fbd(xd, mono_, n):
    if len(mono_) == 1:
        return xd[mono_[0]][n]
    e1, e2 = mono_
    res = ae.NPolyA(NV12, BB)
    for l in range(n + 1):
        res = res.add(xd[e1][l].mul(xd[e2][n - l]).scale(math.comb(n, l)))
    return res


def pi_vac(j, Xi, Qi, aa, t, cfac):
    xd = xibar(Xi, Qi, aa, t, j, cfac)
    res = ONE_P if j == 0 else ae.NPolyA(NV12, BB)
    for i in (1, 2, 3):
        for cb, mono_ in zip(QV[i], BASIS):
            if cb == 0.0:
                continue
            for l in range(0, min(i, j) + 1):
                coef = arb(math.comb(j, l) * (math.factorial(i) // math.factorial(i - l))) * abs(cb)
                term = fbd(xd, mono_, j - l).scale(coef)
                res = res.add(trade(term, t, i - l) if i - l > 0 else term)
    return res




def Dbar(n, h, pis):
    Y = [ONE_P]
    for mm in range(n):
        acc = ae.NPolyA(NV12, BB)
        for i in range(mm + 1):
            acc = acc.add(h[i + 1].mul(Y[mm - i]).scale(math.comb(mm, i)))
        Y.append(acc)
    res = ae.NPolyA(NV12, BB)
    for j in range(n + 1):
        res = res.add(pis[j].mul(Y[n - j]).scale(math.comb(n, j)))
    return res


bondsL = [(XD[r], XD[s], TRI[p_], a_e) for p_, (r, s) in enumerate(PAIRS)] + \
         [(XS[r], XD[r], 1, max(a_m, a_e)) for r in range(3)] + [(XS[0], XS[1], 1, a_m), (XS[1], XS[2], 1, a_m)]
bonds0 = [(XS[r], XS[s], TRI[p_], a_m) for p_, (r, s) in enumerate(PAIRS)]




# ====================================================================================== part 4a: covariances, joint moments, tails, L0 side
# (kt_c_v2_3 l.763-969 in balls; the gauge basis is exact (ADD2 sect. 1); positivity by Sylvester's criterion on certain balls)
def lap_a(edges, V):
    L = arb_mat(V, V)
    for (u, v), c in edges:
        c = ae.A(c)
        L[u, u] += c
        L[v, v] += c
        L[u, v] -= c
        L[v, u] -= c
    return L


def gauge_basis_a(V, S):
    """an exact basis of the orthogonal complement of u = 1_S: e_s - e_s0 for s in S \\ {s0}, and e_k for k not in S (ADD2 sect. 1)."""
    S = sorted(S)
    cols = [(s, S[0]) for s in S[1:]] + [(k, None) for k in range(V) if k not in S]
    Bm = arb_mat(V, len(cols))
    for j, (a_, b_) in enumerate(cols):
        Bm[a_, j] = 1
        if b_ is not None:
            Bm[b_, j] = -1
    return Bm


TILT_LOG = []          # (label, certified, smallest leading minor's lower end) for every positive-definiteness test (C-TILT (b))


def surely_pd(M, label='pd'):
    """Sylvester's criterion: every leading principal minor certainly positive; logged in TILT_LOG."""
    n = M.nrows()
    low = None
    for k in range(1, n + 1):
        sub = arb_mat(k, k)
        for i in range(k):
            for j in range(k):
                sub[i, j] = M[i, j]
        d = sub.det()
        lo = float(d.lower())
        low = lo if low is None else min(low, lo)
        if not (d > 0):
            TILT_LOG.append((label, False, lo))
            return False
    TILT_LOG.append((label, True, low))
    return True


def tilted_cov_a(L, Bm, rates, extra=None, label='tilted_cov'):
    """kt_c_v2_3.tilted_cov in balls: (B Lt^-1 B^T, (det(B^T L B)/det Lt)^(nn/2)), Lt = B^T (L - 2 diag(rates) - 2 extra) B; (None, None)
    unless Lt is certainly positive definite."""
    V = L.nrows()
    Lx = arb_mat(V, V)
    for i in range(V):
        for j in range(V):
            Lx[i, j] = L[i, j] - (2 * ae.A(rates[i]) if i == j else 0) - (2 * extra[i, j] if extra is not None else 0)
    Lr = Bm.transpose() * L * Bm
    Lt = Bm.transpose() * Lx * Bm
    if not surely_pd(Lt, label):
        return None, None
    ratio = Lr.det() / Lt.det()
    return Bm * Lt.inv() * Bm.transpose(), (ratio.log() * nn / 2).exp()


def chi_tail_a(s):
    """P(chi_nn^2 > s) bound in balls: exp(-s/2) (nn = 2); erfc(sqrt(s/2)) + sqrt(2s/pi) exp(-s/2) (nn = 3), with erfc(x) <= exp(-x^2)/(x sqrt pi)
    (x > 0 asserted; nonnegative coefficient, ADD1 b)."""
    if nn == 2:
        return (-s / 2).exp()
    x = (s / 2).sqrt()
    if not (x > 0):
        raise ValueError('chi_tail_a: x is not certainly positive')
    return (-(x * x)).exp() / (x * arb.pi().sqrt()) + (2 * s / arb.pi()).sqrt() * (-s / 2).exp()


E9 = [((6 + r, 6 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((6 + r, r), 1) for r in range(3)] + [((r, 3 + r), 1) for r in range(3)] + [((0, 1), 1), ((1, 2), 1)]
L9 = lap_a(E9, 9)
B9 = gauge_basis_a(9, range(6))
ED_ = [((r, s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
      [((r, 3 + r), 1) for r in range(3)]
LD = lap_a(ED_, 6)
BD = gauge_basis_a(6, range(6))
W9 = arb_mat(6, 9)                           # vacrig11f's W12[:, IDX9F]: sigma X (0-2), sigma'' X (3-5), sigma'' Q (6-8) over 6 coordinates
for r in range(3):
    W9[r, r] = 1
    W9[3 + r, 3 + r] = 1
for p_, (r, s) in enumerate(PAIRS):
    W9[3 + r, 6 + p_] = 1
    W9[3 + s, 6 + p_] = -1
W9_INT = [[0] * 9 for _ in range(6)]         # W9's exact integers, for AllMom2A's exact zeros (kt_cert_v1_5's rule)
for r in range(3):
    W9_INT[r][r] = 1
    W9_INT[3 + r][3 + r] = 1
for p_, (r, s) in enumerate(PAIRS):
    W9_INT[3 + r][6 + p_] = 1
    W9_INT[3 + s][6 + p_] = -1
if not all(W9[i, j] == W9_INT[i][j] for i in range(6) for j in range(9)):
    raise ValueError('W9 differs from its integer form')
PLANTED = [False]                            # PLANT-SING runs once per piece, on its first table
MAP9 = {0: 0, 1: 1, 2: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8}     # vacrig11f's IDX9F
GROUPS9 = [0] * 6 + [1] * 3


def to9(P, nv=NV12):
    """vacrig11f.to9 in balls: a 12-variable polynomial without sigma Q forms as a polynomial in the nine joint forms."""
    res = {}
    for e, c in P.items():
        if not all(e[i] == 0 for i in range(nv) if i not in MAP9):
            raise ValueError('to9: a variable outside the nine forms in %r' % (e,))
        e9 = [0] * 9
        for i, j in MAP9.items():
            if i < nv:
                e9[j] = e[i]
        e9 = tuple(e9)
        res[e9] = res[e9] + c if e9 in res else ae.A(c)
    return {e: c for e, c in res.items() if not c.is_zero()}


def sub_mat(M, idx):
    S = arb_mat(len(idx), len(idx))
    for a_, i in enumerate(idx):
        for b_, j in enumerate(idx):
            S[a_, b_] = M[i, j]
    return S


def joint_moments_a(rates9, Dmax, qcap, extra=None, label='tilted_cov'):
    """vacrig11f.joint_moments in balls: the joint tilted moments of the nine forms; extra: an optional 9 x 9 quadratic tilt (F1's
    lam Q_rr''). The nine forms span six coordinates, so AllMom2A gets W9's exact integers (W_int) and treats the minors of rank-deficient
    subsets as exact zeros (arbeng_c2b_v2). Returns (table, N, G9, Gam)."""
    G9, N9 = tilted_cov_a(L9, B9, rates9, extra=extra, label=label)
    if G9 is None:
        return None, None, None, None
    G6 = sub_mat(G9, [0, 1, 2, 6, 7, 8])
    Gam = W9.transpose() * G6 * W9
    return ae.AllMom2A(Gam, nn, Dmax, groups=GROUPS9, caps={1: qcap}, W_int=W9_INT), N9, G9, Gam


SING_FAILS, SING_FIRES = [], []         # C-SING failures and unfired PLANT-SING, merged into the piece's verdict in main()


def det_sub(Gam, A):
    """det(Gam_A) by the same arithmetic as AllMom2A (an arb_mat of the entries, then det)."""
    sub = arb_mat(len(A), len(A))
    for a_, fa in enumerate(A):
        for b_, fb in enumerate(A):
            sub[a_, b_] = Gam[fa, fb]
    return sub.det()


def c_sing(am, Gam, qcap, label):
    """C-SING (kt_cert_v1_7's, on the nine forms): (i) every subset the table kept is of full exact rank and its stored (-2)^|A| det(Gam_A)
    is identical (midpoint and radius) to the direct computation; every subset it dropped is rank-deficient and its det ball contains 0;
    kept and dropped together are all the subsets of sizes up to min(9, D) the caps allow; (ii) degree-4 tables with and without the rule
    overlap in every moment."""
    ok, nk, seen = True, 0, set()
    for j in range(1, len(am.Dj)):
        cj, vj = am.Dj[j]
        if len(cj) == 0:
            continue
        for row, v in zip(am.decode(cj), vj):
            A = tuple(int(f) for f in np.flatnonzero(row))
            d = arb(-2) ** len(A) * det_sub(Gam, A)
            ok = ok and len(A) == j and ae.int_rank(W9_INT, A) == j and d.mid() == v.mid() and d.rad() == v.rad()
            seen.add(A)
            nk += 1
    for A, dv in am.dropped:
        ok = ok and ae.int_rank(W9_INT, A) < len(A) and dv.contains(0)
        seen.add(tuple(A))
    allowed = set(A for j in range(1, min(9, am.D) + 1) for A in itertools.combinations(range(9), j) if sum(1 for f in A if f >= 6) <= qcap)
    ok = ok and seen == allowed
    kw = dict(groups=GROUPS9, caps={1: qcap})
    t_rule, t_free = ae.AllMom2A(Gam, nn, 4, W_int=W9_INT, **kw), ae.AllMom2A(Gam, nn, 4, **kw)
    nm = 0
    for d_ in range(5):
        for x_, y_ in zip(t_rule.mom[d_], t_free.mom[d_]):
            ok = ok and x_.overlaps(y_)
            nm += 1
    out('C-SING N=%d %s: %d subsets kept (full rank; det balls identical to direct), %d dropped (rank-deficient; det balls contain 0, '
        'largest radius %.2e), all %d allowed subsets covered; degree-4 tables with and without the rule overlap in %d moments -> %s' % (
            NN, label, nk, am.zeroed, am.max_zero_rad, len(allowed), nm, 'PASS' if ok else 'FAIL'))
    if not ok:
        SING_FAILS.append('C-SING %s' % label)


def plant_sing(Gam, qcap):
    """PLANT-SING: the rule with X0's column of W9 set to zero (so every subset with X0 counts as rank-deficient) must stop, since
    det(Gam_{X0}) = Var(X0) > 0 excludes 0."""
    bad = [row[:] for row in W9_INT]
    for i in range(6):
        bad[i][0] = 0
    try:
        ae.AllMom2A(Gam, nn, 2, groups=GROUPS9, caps={1: qcap}, W_int=bad)
        fired = False
    except ValueError:
        fired = True
    out('PLANT-SING N=%d: the rule with X0\'s column of W9 zeroed %s -> %s' % (NN, 'stops' if fired else 'passes',
                                                                              'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        SING_FIRES.append('PLANT-SING')


# ====================================================================================== part 5: hand-off, checks, the pieces
# A piece's hand-off: hand_m2b_cert_v1_1_<piece>.n<N>.txt in the own folder, created once (exclusive create), under 8 MB: a HEAD line (this
# script's sha256, the piece, N, precision and, v1_1, the exact boundaries a_m, a_e, a_pp as 'p/q' and RHO_PP_HEX), the rows, and an END
# line with the sha256 of the body. v1_1: main() writes it only after every gate of the piece has passed (BOUND,
# C-TILT (a) and (b), C-R0 and PLANT-R0, C-RAD-MA, the C-SING and PLANT-SING merges), with nothing in fails or fires and the piece
# complete; PLANT-NOWRITE checks that the guarded writer never opens a file when a gate has failed. The record names the file's sha256 on
# its HANDOFF line. Balls are written by arb's str with the radius (80 digits), whose parse contains the ball.
HANDOFF_MAX = 8 * 1024 * 1024


def handoff_path(piece):
    return os.path.join(OWN, 'hand_m2b_cert_v1_1_%s.%s.txt' % (piece, SUFFIX))


def head_line(piece):
    return 'HEAD m2b_cert_v1_1 %s piece %s kind vac N %d prec %d a_m %s a_e %s a_pp %s rho_pp_hex %s' % (
        SELF_SHA, piece, NN, ctx.prec, Fraction(RHO_M) ** 2, Fraction(RHO_E) ** 2, Fraction(RHO_PP) ** 2, RHO_PP_HEX)


def write_handoff(piece, rows, fails, fires, complete, opener=open):
    """the guarded writer: writes only when fails and fires are empty and the piece is complete; returns the sha256 or None."""
    if fails or fires or not complete or rows is None:
        out('HANDOFF N=%d vac %s: not written (a gate failed or the piece is incomplete)' % (NN, piece))
        return None
    path = handoff_path(piece)
    if not (os.path.dirname(os.path.realpath(path)) == os.path.realpath(OWN) and not os.path.exists(path)):
        raise ValueError('hand-off path %s outside the own folder or existing' % path)
    body = '\n'.join([head_line(piece)] + rows) + '\n'
    data = (body + 'END %s\n' % hashlib.sha256(body.encode()).hexdigest()).encode()
    if not (len(data) < HANDOFF_MAX):
        raise ValueError('hand-off of %d bytes exceeds HANDOFF_MAX' % len(data))
    with opener(path, 'xb') as fh:
        fh.write(data)
    sh = hashlib.sha256(data).hexdigest()
    out('HANDOFF N=%d vac %s: %s sha256 %s (%d bytes, %d rows; cpu %.1f s)' % (NN, piece, os.path.basename(path), sh, len(data), len(rows),
                                                                              cpu()))
    return sh


def plant_nowrite(fires):
    """PLANT-NOWRITE (as pk03's m3_run_v1_6_1): the guarded writer, given a failed gate and a recording opener
    that raises if called, must return without opening anything."""
    calls = []

    def opener(path, mode):
        calls.append(path)
        raise RuntimeError('PLANT-NOWRITE: the opener was called')
    try:
        got = write_handoff(PIECE, ['V PLANT 0'], ['PLANT'], [], True, opener=opener)
        fired = got is None and not calls
    except RuntimeError:
        fired = False
    out('PLANT-NOWRITE N=%d: the guarded writer with a failed gate opened %d files -> %s' % (NN, len(calls), 'FIRES' if fired else
                                                                                               'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-NOWRITE')


def ball(x):
    return x.str(80, radius=True)


def bstr(x):
    """a ball as 'mid +- rad (rel r)' (a print, not an enclosure: read balls from the hand-off)."""
    mid, rad = float(x.mid()), float(x.rad())
    return '%.9e +- %.1e (rel %.1e)' % (mid, rad, rad / abs(mid) if mid != 0 else float('inf'))


def mark(label):
    """a stage line with the CPU time so far."""
    out('STAGE-CPU N=%d %s: %s done at cpu %.1f s' % (NN, PIECE, label, cpu()))


def kappa_B():
    """kappa = 2 (1 - cos delta) - a^2/(4 (1 - a)), a = max(a_m, a_e): a bad bond r inside Omega'' has Q_rr'' > J kappa (vacrig11f l.350)."""
    amax = max(a_m, a_e)
    kap = 2 * (1 - DELTA.cos()) - arb(amax) ** 2 / (4 * (1 - arb(amax)))
    if not (kap > 0):
        raise ValueError('kappa_B is not certainly positive')
    return kap


def c_import(fails):
    """C-IMPORT: the imported engine modules are the files C-HASH hashed."""
    want = [os.path.realpath(os.path.join(OWN, f)) for f in ('arbeng_c2b_v2.py', 'arbeng_ma_v1_3.py')]
    got = [os.path.realpath(m.__file__) for m in (ae, ma)]
    ok = got == want
    out('C-IMPORT N=%d: arbeng_c2b_v2 from %s, arbeng_ma_v1_3 from %s -> %s' % (NN, got[0], got[1], 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-IMPORT')


def bound_line(fails):
    """ADD1 sect. 1 and ADD2 sect. 2: the exact boundaries this piece uses, as Fractions, checked equal to the arb values."""
    fa, fe, fp = Fraction(RHO_M) ** 2, Fraction(RHO_E) ** 2, Fraction(RHO_PP) ** 2

    def same(f, x):
        return bool(arb(f.numerator) / f.denominator == x)
    app = (arb(RHO_M).asin() + DELTA).sin() ** 2
    ok = same(fa, a_m) and same(fe, a_e) and same(fp, a_pp) and bool(a_pp >= app) and float.fromhex(RHO_PP_HEX) == RHO_PP
    out('BOUND N=%d: a_m %s a_e %s a_pp %s RHO_PP_HEX %s (a_pp >= sin^2(asin rho_m + delta) = %s) -> %s' % (
        NN, fa, fe, fp, RHO_PP_HEX, app.str(20, radius=False), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('BOUND')


def c_tilt_a(fails, fires):
    """C-TILT (a): domination of the tilt rates (rounded up from arb), a_pp's inequality, positivity of the Chernoff lambdas; PLANT-TILT."""
    def rate_ok(c, a):
        return arb(c) >= -(1 - a).log() / (2 * a)
    rates = (('c_m', c_m, a_m), ('c_e', c_e, a_e), ('c_pp', c_pp, a_pp))
    okr = all(rate_ok(c, a) for _, c, a in rates)
    okl = all(x > 0 for x in LAMS + (LAM_B,)) and min(LAMS) >= 0.3
    ok = okr and okl
    out('C-TILT (a) N=%d: %s; Chernoff lambdas %s > 0, tailX/ann lambdas >= 0.3 (LAW v1) -> %s' % (
        NN, ', '.join('%s %.17g >= -log(1 - a)/(2a) = %s' % (nm, c, (-(1 - a).log() / (2 * a)).str(12, radius=False)) for nm, c, a in rates),
        ' '.join('%g' % x for x in LAMS + (LAM_B,)), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-TILT (a)')
    p_rate = rate_ok(c_m * (1 - 1e-9), a_m)
    n0 = len(TILT_LOG)
    p_pd = tilted_cov_a(LD, BD, [arb(1000)] + [arb(0)] * 5, label='PLANT')[0] is not None
    del TILT_LOG[n0:]
    fired = (not p_rate) and (not p_pd)
    out('PLANT-TILT N=%d: c_m (1 - 1e-9) passes the rate test: %s; a lambda = 1e3 tilt certified positive definite: %s -> %s' % (
        NN, p_rate, p_pd, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-TILT')


def c_tilt_b(fails):
    """C-TILT (b): every positive-definiteness test of this piece certified (the piece stops otherwise); count and smallest minor."""
    ok = all(c for _, c, _ in TILT_LOG) and len(TILT_LOG) > 0
    labels = sorted(set(lab for lab, _, _ in TILT_LOG))
    out('C-TILT (b) N=%d: %d positive-definiteness tests (%s), all certified: %s; smallest leading minor lower end %.3e -> %s' % (
        NN, len(TILT_LOG), ', '.join(labels), ok, min((lo for _, _, lo in TILT_LOG), default=float('nan')), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-TILT (b)')


def vac_series():
    """vacmod2.Builder(4).L1 and .L0 in balls: L1 = p(xi'') e^{HL}, L0 = p(xi) e^{H0}, orders 0..KX."""
    HL = zero()
    for r in range(3):
        HL = HL + meas(XD[r])
    for p, (r, s) in enumerate(PAIRS):
        HL = HL + anh(XD[r], XD[s], TRI[p])
    for r in range(3):
        HL = HL + anh(XS[r], XD[r], 1)
    HL = HL + anh(XS[0], XS[1], 1) + anh(XS[1], XS[2], 1)
    H0 = zero()
    for p, (r, s) in enumerate(PAIRS):
        H0 = H0 + anh(XS[r], XS[s], TRI[p])
    return HL.exp() * vac_poly(xis(XD, QD)), H0.exp() * vac_poly(xis(XS, QS))


def resid(src, l0, m, ks):
    """r_k = E[L1_k | s] - sum_{j <= min(k, 3)} m_j L0_{k-j} (sigma polynomials) for k in ks."""
    return {k: padd(src[k], *[pscale(l0[k - j], -m[j]) for j in range(min(k, 3) + 1)]) for k in ks}


def maxdeg(polys):
    return max([sum(e) for P in polys for e in P] + [0])


def wishart(t, deg, extra=None, label='G1'):
    """the tilted covariance (rates c_m t on the six outer vertices; optional quadratic term) and WishartA on its sigma block."""
    G, n = tilted_cov_a(LD, BD, [c_m * t] * 6, extra=extra, label=label)
    if G is None:
        raise ValueError('the tilt %s is not certainly positive definite' % label)
    return ae.WishartA(sub_mat(G, [0, 1, 2]), nn, deg), n


def lin_w(w, kbar):
    """vacrig11w's lin: (Q_TM + Q_MB)/4 - kbar (wt) or (Q_TM - Q_MB)/4 (dl), in the g variables."""
    q = arb(1) / 4
    d = {(0, 0, 0, 1, 0, 0): q, (0, 0, 0, 0, 1, 0): q if w == 'wt' else -q}
    if w == 'wt':
        d[(0, 0, 0, 0, 0, 0)] = -arb(kbar)
    return ae.sigma_to_g(d)


def b_w(t):
    """vacrig11w's B_w = t ((X_T - X_M)^2 + (X_M - X_B)^2)/(16 (1 - a_m)) >= 0, in the g variables (a_m exact)."""
    cB = t / (16 * (1 - a_m))
    return ae.sigma_to_g({(2, 0, 0, 0, 0, 0): cB, (1, 1, 0, 0, 0, 0): -2 * cB, (0, 2, 0, 0, 0, 0): 2 * cB, (0, 1, 1, 0, 0, 0): -2 * cB,
                          (0, 0, 2, 0, 0, 0): cB})


def wnorm(w2, n, P, lw, bw):
    """||w P|| <= ||lin_w P|| + ||B_w P|| (exact Wishart moments, vacrig11w)."""
    PL, PB = ae.pmul(lw, P), ae.pmul(bw, P)
    return nsqrt(n * w2.E2(PL, PL)) + nsqrt(n * w2.E2(PB, PB))


def piece_x(fails, fires):
    STAGE[0] = 'series'
    L1, L0 = vac_series()
    mark('series to order %d (L1 terms %s, L0 terms %s)' % (KX, [len(c) for c in L1.c], [len(c) for c in L0.c]))
    STAGE[0] = 'conditional expectation'
    src = make_condE(build_conditioning())(L1)
    l0 = restrict6(L0)
    mark('conditional expectations to Dc %d' % (2 * KX))
    r = resid(src, l0, MSER, range(KX + 1))
    okr0 = len(r[0]) == 0
    out('C-R0 N=%d: r_0 = E[L1_0 | s] - L0_0 has %d terms (must be the exact zero polynomial) -> %s' % (NN, len(r[0]), 'PASS' if okr0 else
                                                                                                        'FAIL'))
    if not okr0:
        fails.append('C-R0')
    rp = resid(src, l0, [1.0 + 2.0 ** -52] + MSER[1:], (0,))[0]
    out('PLANT-R0 N=%d: m_0 = 1 + 2^-52 leaves r_0 with %d terms -> %s' % (NN, len(rp), 'FIRES' if rp else 'DOES NOT FIRE'))
    if not rp:
        fires.append('PLANT-R0')
    rg = {k: ae.sigma_to_g(r[k]) for k in range(1, KX + 1)}
    dmax = maxdeg(rg.values())
    out('RESIDUALS N=%d: r_1..r_4 terms %s, degrees %s' % (NN, [len(r[k]) for k in range(1, KX + 1)],
                                                           [maxdeg([r[k]]) for k in range(1, KX + 1)]))
    STAGE[0] = 'norms at J1'
    t1 = arb(1) / J1
    w1, n1 = wishart(t1, 2 * dmax, label='G1 J1')
    nk = {k: nsqrt(n1 * w1.E2(rg[k], rg[k])) for k in range(1, KX + 1)}
    vals = dict(NP=sum((t1 ** k * nk[k] for k in (2, 3, 4)), arb(0)), R1=t1 * nk[1])
    mark('nP, R1 at J1')
    STAGE[0] = 'weighted norms at J0'
    t0 = arb(1) / J0
    w0, n0 = wishart(t0, 2 * dmax + 4, label='G1 J0')
    kbar = load_json(os.path.join(SCRATCH, KFILE))['kbar']
    bw = b_w(t0)
    for w in ('wt', 'dl'):
        lw = lin_w(w, kbar)
        wn = {k: wnorm(w0, n0, rg[k], lw, bw) for k in range(1, KX + 1)}
        vals['NPM_' + w] = sum((t0 ** k * wn[k] for k in (2, 3, 4)), arb(0))
        vals['R1_' + w] = t0 * wn[1]
    mark('nPM, R1 weighted at J0')
    out('EXPLICIT-V N=%d: nP %s | R1 %s | at J0 = %d: nPM_wt %s R1_wt %s | nPM_dl %s R1_dl %s (kbar %r)' % (
        NN, bstr(vals['NP']), bstr(vals['R1']), J0, bstr(vals['NPM_wt']), bstr(vals['R1_wt']), bstr(vals['NPM_dl']), bstr(vals['R1_dl']),
        kbar))
    rows = ['KBAR %r' % kbar]
    for k in range(KX + 1):
        for e, c in sorted(r[k].items()):
            rows.append('R %d %s %s' % (k, ' '.join(str(int(x)) for x in e), ball(c)))
    rows += ['V %s %s' % (k, ball(v)) for k, v in sorted(vals.items())]
    return rows


def d5_ed(t):
    """D5 at t (vacrig11f l.294-313) and its conditional expectation through the M-a CondTable; returns (ED, detf, ext, info)."""
    hL = {k: hk(k, [(v, a_e) for v in XD], bondsL, cf_rad) for k in range(1, 6)}
    pis = [pi_vac(j, XD, QD, a_e, t, cf_rad) for j in range(6)]
    D5 = Dbar(5, hL, pis)
    ex5 = D5.exponents()
    if ex5[:, 3:6].sum() != 0:
        raise ValueError('D5 has a sigma Q form')
    deg2, qdeg, tot = int(ex5[:, 6:].sum(axis=1).max()), int(ex5[:, 9:].sum(axis=1).max()), int(ex5.sum(axis=1).max())
    mark('D5 (%d terms, deg2 %d, Q degree %d, total %d)' % (len(D5.codes), deg2, qdeg, tot))
    Amat = eye3() + tri_laplacian()
    Ainv = Amat.inv()
    At = Amat - eye3() * (2 * c_e * t)
    if not surely_pd(At, 'A - 2 c_e t I'):
        raise ValueError('A - 2 c_e t I is not certainly positive definite')
    Ati = At.inv()
    detf = ((Amat.det() / At.det()).log() * nn / 2).exp()
    Delta = Ati - Ainv
    W2 = w2_arb()
    if not all(W2[i, j] == W2_INT[i][j] for i in range(3) for j in range(6)):
        raise ValueError('W2 differs from its integer form')
    STAGE[0] = 'CondTable (M-a)'
    tab = ma.condmom(Ati, Ati, W2, W2_INT, nn, deg2, groups=[0, 0, 0, 1, 1, 1], caps={1: max(qdeg, 1)}, chunk=CHUNK)
    mark('CondTable (arbeng_ma_v1_3; Dc %d, %d entries, chunk %d)' % (deg2, tab.entries, CHUNK))
    STAGE[0] = 'condE (M-a)'
    ED, kmax = tab.condE(D5.to_dict(), tot)
    mark('conditional expectation of D5 (%d g-monomials, largest count %d)' % (len(ED), kmax))
    ext = arb_mat(6, 6)
    for i in range(3):
        for j in range(3):
            ext[i, j] = Delta[i, j]
    return ED, detf, ext, dict(nterms=len(D5.codes), deg2=deg2, qdeg=qdeg, tot=tot, entries=tab.entries, kmax=kmax)


def piece_d5(fails, weighted):
    J = J0 if weighted else J1
    t = arb(1) / J
    try:
        ED, detf, ext, info = d5_ed(t)
    except ma.MAFallback as e:
        out('MAFALLBACK N=%d: %r; a Dc %d CondTable in arb is out of reach (memory), so the piece stops (close condition (ii): no M-a value '
            'is used after a fallback)' % (NN, e, 11))
        fails.append('MAFALLBACK')
        return None
    dED = maxdeg([ED])
    w2, n2 = wishart(t, 2 * dED + (4 if weighted else 0), extra=ext, label='G2 J%d' % J)
    vals = {}
    if not weighted:
        vals['D5'] = (t ** 5 / 120) * detf * nsqrt(n2 * w2.E2(ED, ED))
        nd0 = (t ** 5 / 120) * detf * nsqrt(n2 * w2.E2(*([{g: arb(b.mid()) for g, b in ED.items()}] * 2)))
        relw = float(vals['D5'].rad()) / float(vals['D5'].mid())
        okr = relw <= 1e-5
        out('C-RAD-MA N=%d: nD %s, relative width %.2e (<= 1e-5); the M-a part %.2e (radius with the M-a radii minus without) -> %s' % (
            NN, bstr(vals['D5']), relw, float(vals['D5'].rad()) - float(nd0.rad()), 'PASS' if okr else 'FAIL'))
        if not okr:
            fails.append('C-RAD-MA')
    else:
        kbar = load_json(os.path.join(SCRATCH, KFILE))['kbar']
        bw = b_w(t)
        for w in ('wt', 'dl'):
            vals['D5W_' + w] = (t ** 5 / 120) * detf * wnorm(w2, n2, ED, lin_w(w, kbar), bw)
        for k, v in vals.items():
            relw = float(v.rad()) / float(v.mid())
            okr = relw <= 1e-5
            out('C-RAD-MA N=%d %s: %s, relative width %.2e (<= 1e-5) -> %s' % (NN, k, bstr(v), relw, 'PASS' if okr else 'FAIL'))
            if not okr:
                fails.append('C-RAD-MA %s' % k)
    out('D5-V N=%d J=%d: %s | D5 %d terms, deg2 %d, Q degree %d, total %d; CondTable %d entries; ED %d g-monomials' % (
        NN, J, ' | '.join('%s %s' % (k, bstr(v)) for k, v in sorted(vals.items())), info['nterms'], info['deg2'], info['qdeg'], info['tot'],
        info['entries'], len(ED)))
    return ['INT %d %d %d %d %d %d' % (info['nterms'], info['deg2'], info['qdeg'], info['tot'], info['entries'], info['kmax'])] + \
        ['V %s %s' % (k, ball(v)) for k, v in sorted(vals.items())]


def r0_poly(t):
    """vacrig11f l.316-327 in balls: sum_j |m_j| t^j t^{5-j}/(5-j)! Dbar_{5-j}(h0, pi_j of L0 at a_m), j = 0..4 (m_4 = 0)."""
    h0 = {k: hk(k, [], bonds0, cf_rad) for k in range(1, 6)}
    mfull = MSER + [0.0]
    R0 = ae.NPolyA(NV12, BB)
    for j in range(5):
        if mfull[j] == 0.0:
            continue
        n_ = 4 - j
        pis0 = [pi_vac(i, XS, QS, a_m, t, cf_rad) for i in range(n_ + 2)]
        R0 = R0.add(Dbar(n_ + 1, h0, pis0).scale(abs(arb(mfull[j])) * t ** j * t ** (n_ + 1) / math.factorial(n_ + 1)))
    ex = R0.exponents()
    if ex[:, 6:].sum() != 0:
        raise ValueError('R0 has a sigma\'\' variable')
    return ae.sigma_to_g({e[:6]: c for e, c in R0.to_dict().items()}), len(R0.codes)


def piece_r0(fails):
    vals = {}
    t1 = arb(1) / J1
    R0g, nt1 = r0_poly(t1)
    w1, n1 = wishart(t1, 2 * maxdeg([R0g]), label='G1 J1')
    vals['R0'] = nsqrt(n1 * w1.E2(R0g, R0g))
    mark('R0 at J1 (%d terms)' % nt1)
    t0 = arb(1) / J0
    R0g0, nt0 = r0_poly(t0)
    w0, n0 = wishart(t0, 2 * maxdeg([R0g0]) + 4, label='G1 J0')
    kbar = load_json(os.path.join(SCRATCH, KFILE))['kbar']
    bw = b_w(t0)
    for w in ('wt', 'dl'):
        vals['R0W_' + w] = wnorm(w0, n0, R0g0, lin_w(w, kbar), bw)
    mark('R0 weighted at J0 (%d terms)' % nt0)
    out('R0-V N=%d: %s' % (NN, ' | '.join('%s %s' % (k, bstr(v)) for k, v in sorted(vals.items()))))
    return ['INT %d %d' % (nt1, nt0)] + ['V %s %s' % (k, ball(v)) for k, v in sorted(vals.items())]


def tail_polys(t):
    """the orders L1_k (k = 0..4) of the explicit series in the nine joint forms, with their largest degree and Q'' degree."""
    L1, _ = vac_series()
    Lk = [to9(L1.c[k]) for k in range(KX + 1)]
    return Lk, maxdeg(Lk), max([sum(e[6:]) for P in Lk for e in P] + [0])


def tail_tables(fam, lam, Lk, dP, qP, t, J):
    """one Chernoff family at one lambda: three tables, and for each sum_k t^k E2(L_k, L_k)^{1/2} (or E2(P0'', P0'')^{1/2} for 'A');
    returns the terms e^{-lam J c} N (.)^2 per table."""
    terms = []
    for idx in range(3):
        rates = [c_m * t] * 6 + ([2 * c_pp * t] * 3 if fam == 'A' else [arb(0)] * 3)
        extra = None
        if fam in ('X', 'A'):
            rates[6 + idx] = rates[6 + idx] + arb(lam)
            cexp = a_e
        else:
            extra = arb_mat(9, 9)
            extra[idx, idx] = arb(lam)
            extra[6 + idx, 6 + idx] = arb(lam)
            extra[idx, 6 + idx] = -arb(lam)
            extra[6 + idx, idx] = -arb(lam)
            cexp = kappa_B()
        am9, N9, _, Gam = joint_moments_a(rates, 2 * dP, max(2 * qP, 1), extra=extra, label='tilt %s%d lam %g' % (fam, idx, lam))
        if am9 is None:
            raise ValueError('the Chernoff tilt %s%d (lambda %g) is not certainly positive definite' % (fam, idx, lam))
        s = sum((t ** k * nsqrt(am9.E2(P, P)) for k, P in enumerate(Lk) if P), arb(0))
        term = (-arb(lam) * J * cexp).exp() * N9 * s * s
        mark('tail table %s%d lambda %g (degree %d; %d rank-deficient subsets as exact zeros): %s' % (fam, idx, lam, 2 * dP, am9.zeroed,
                                                                                                  bstr(term)))
        c_sing(am9, Gam, max(2 * qP, 1), '%s%d lam %g' % (fam, idx, lam))
        if not PLANTED[0]:
            plant_sing(Gam, max(2 * qP, 1))
            PLANTED[0] = True
        terms.append(term)
    return terms


def piece_tail(fails):
    t = arb(1) / J1
    if PIECE == 'tA':
        P0d = to9(pi_vac(0, XD, QD, a_pp, t, cf_rad).to_dict())
        polys, dP, qP = [P0d], maxdeg([P0d]), max([sum(e[6:]) for e in P0d] + [0])
        fam, lams = 'A', LAMS
    elif PIECE == 'tB':
        polys, dP, qP = tail_polys(t)
        fam, lams = 'B', (LAM_B,)
    else:
        polys, dP, qP = tail_polys(t)
        fam, lams = 'X', (LAMS[int(PIECE[2])],)
    mark('tail polynomials (%s terms, degree %d, Q degree %d)' % ([len(P) for P in polys], dP, qP))
    rows = ['INT %d %d' % (dP, qP)]
    for lam in lams:
        if fam == 'A':
            terms = tail_tables_ann(lam, polys[0], dP, qP, t, J1)
        else:
            terms = tail_tables(fam, lam, polys, dP, qP, t, J1)
        acc = sum(terms, arb(0))
        out('TAIL N=%d %s lambda %g: sum over the three tables %s, root %s' % (NN, fam, lam, bstr(acc), bstr(nsqrt(acc))))
        rows += ['T %s %r %d %s' % (fam, lam, i, ball(x)) for i, x in enumerate(terms)] + ['A %s %r %s' % (fam, lam, ball(acc))]
    return rows


def tail_tables_ann(lam, P0d, dP, qP, t, J):
    """ann's three tables at one lambda: e^{-lam J a_e} N E2(P0'', P0'') (vacrig11f l.375-388)."""
    terms = []
    for idx in range(3):
        rates = [c_m * t] * 6 + [2 * c_pp * t] * 3
        rates[6 + idx] = rates[6 + idx] + arb(lam)
        am9, N9, _, Gam = joint_moments_a(rates, 2 * dP, max(2 * qP, 1), label='tilt A%d lam %g' % (idx, lam))
        if am9 is None:
            raise ValueError('the annulus tilt A%d (lambda %g) is not certainly positive definite' % (idx, lam))
        term = (-arb(lam) * J * a_e).exp() * N9 * am9.E2(P0d, P0d)
        c_sing(am9, Gam, max(2 * qP, 1), 'A%d lam %g' % (idx, lam))
        if not PLANTED[0]:
            plant_sing(Gam, max(2 * qP, 1))
            PLANTED[0] = True
        terms.append(term)
    return terms


def main():
    fails, fires = [], []
    complete = False
    try:
        c_import(fails)
        bound_line(fails)
        c_tilt_a(fails, fires)
        plant_nowrite(fires)
        if PIECE == 'x':
            rows = piece_x(fails, fires)
        elif PIECE in ('d5', 'dw'):
            rows = piece_d5(fails, PIECE == 'dw')
        elif PIECE == 'r0':
            rows = piece_r0(fails)
        else:
            rows = piece_tail(fails)
        c_tilt_b(fails)
        fails += SING_FAILS
        fires += SING_FIRES
        complete = True
        STAGE[0] = 'hand-off'
        write_handoff(PIECE, rows, fails, fires, complete)
    except CapStop as e:
        out('CAP-STOP before %s at cpu %.1f s (LIM %d)' % (e, cpu(), LIM))
    except Exception as e:
        traceback.print_exc()
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        out('VERDICT INVALID (ERROR)')
        return 1
    why = fails + ['%s did not fire' % x for x in fires] + ([] if complete else ['INCOMPLETE'])
    out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (MODE, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
    out('VERDICT %s%s' % ('VALID' if not why else ('INCOMPLETE' if why == ['INCOMPLETE'] else 'INVALID'), '' if not why else ' (%s)' % ', '.join(why)))
    return 0


class CapStop(Exception):
    pass


if __name__ == '__main__':
    sys.exit(main())
