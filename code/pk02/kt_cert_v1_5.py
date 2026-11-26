#!/usr/bin/env python3
"""kt_cert_v1_5.py -- pk02 (code/pk02/). REVISION of kt_cert_v1_4.py (f414c3b9; CONFIRMED by the review, REVIEW de8c7c5b), on
kt_radprobe_v1 (920034c7; output cfa355c6, VERDICT H SUPPORTED) and the pre-approval. Changes, and nothing else:
  (1) The joint tail tables use arbeng_c2b_v2 (arbeng_c2b_v1 a70d0cc4 plus one option): the ten forms span six coordinates, and a subset A
      with exact integer rank(W10[:, A]) < |A| has det(Gam_A) = 0 for every G, so AllMom2A leaves it out (its det ball must contain 0).
      kt_cert_v1_4's X2 table had singular minors with det balls [+/- 0.556] at 256 and 512 bits alike (row-pivoted elimination, then a
      Hadamard bound over the remaining rows), which gave X2 its relative radius 1.1e-11 (e1) and 1.5e-4 (h). C-SING checks every table:
      the kept det balls are identical to the direct computation, the dropped subsets are rank-deficient with det balls containing 0, all
      allowed subsets are covered, and degree-4 tables with and without the rule overlap. PLANT-SING (W10's X0 column zeroed) must stop.
  (2) S1: C-REP's reference bound also replaces v2_3's tailB with this engine's.
  (3) S2 (same review): the gate C-R, |log R| <= 1e-10, in the g pieces of engine A.
  Names: records out_kt_cert_v1_5_*, hand-offs hand_kt_cert_v1_5_*; nothing of v1_2, v1_3 or v1_4 is read.
kt_cert_v1_4 (f414c3b9) was the REVISION of kt_cert_v1_3.py (31e29648; CONFIRMED by the review, REVIEW a8e5ed5b; never run), on
the decision after kt_cert_v1_2's smokes (xsmoke 3e73c02a, gsmoke 49cb6c93, xhsmoke 7a3296b0 VALID; ghsmoke 7af1e21d INVALID by C-RAD
only: the bound's relative radius 8.4e-12, from the tail tables, whose moment recursion and E2 lose about 70 digits at 256 bits).
Single change: ctx.prec = 512 in every piece (SPEC_M1_CERT_v1_1_ADD2_v1_3), with the file, record and hand-off names kt_cert_v1_4.
Everything else is kt_cert_v1_3's, as the rest of this docstring describes.
kt_cert_v1_3 (31e29648) was the REVISION of kt_cert_v1_2.py (6e476206) on the REVIEW of kt_cert_v1 (f8c685eb)
and its ADD1 (f71ae3e8); the spec side of F1 and F2 is SPEC_M1_CERT_v1_1_ADD2_v1_2. Changes:
  F1  tailB is an L2 bound: tailB = (sum_r e^{-lam J kappa} N_r E_r[T^2])^{1/2}, E_r under the Chernoff tilt lam Q_rr'' = lam |x_r - x''_r|^2,
      passed to the joint tilted covariance as an extra quadratic form (three joint-moment tables, each guarded by surely_pd), as tailX does
      for X''_v. kt_cert_v1_1's normT sum_r P(B_r)^{1/2} (and its base table) are gone.
  F2  far_out keeps every cross term: hf^2 o4/R + 2 hf sum_g |m_g(t)| o3_g + sum_{g,g'} |m_g(t)| |m_g'(t)| oD_gg' (hf = 2J for the hook kinds,
      else 1), o3_g by outer_far3 on G3 (vacrig11f's E3: the source column 0-2, phi_g on 6-8) and oD_gg' on D, with mixed factor lists;
      kind a: all three kinds of term on D. R = main_N^2/(main_D main_4) from riglap2's main terms (FLOAT, printed; kt_c_v2_3 took R = 1).
      The A1 note's Minkowski step is withdrawn (ADD2 v1_2).
  F3  P = r0 + t r1 + t^2 r2 + t^3 r3 for every kind (engine A and the a-engine).
  F4  every FLOAT number the bound uses is printed with repr (the far parts and log R, gBb, eps_r, Z's inputs); far_out is formed in arb.
  F6  nsqrt stops the item on a certainly negative ball.
  (F5, at the source) VALUE and F2A print a 10-digit decimal that arb checks to be >= the ball.
  Pieces. Engine A is cut into stages, and an item <suffix> (e1n4 ... an3; smoke = e1n4, hsmoke = hn4) runs as pieces <piece>.<suffix>:
    x   the explicit part (orders 0-3: the m_g and r0..r3), written to a hand-off;
    c   D4, its conditional expectation and nD (optional);
    tX, tB, tA, or tX0 ... tA2 (one table each)   the Chernoff tables of tailX, tailB and ann (optional);
    g   reads x's hand-off and the hand-off of every optional piece that was run, computes in-line each stage whose piece was not run, then
        the L0 remainder, nP, nR0, far_out, gB, the bound, the value and the checks. Kind a: x and g only.
  Hand-offs (part 6): own folder, created once, under 2 MB, an END line with the body's sha256. The producing piece prints the file's sha256 in
  its record out_kt_cert_v1_5_<piece>.<suffix>.out. The reader requires that record's VERDICT VALID, and checks the file's sha256 against
  the record, the body checksum and the header (this script's sha256, piece, kind, N, precision). PLANT-HANDOFF (g): three tampered copies in
  memory, each caught by its own check. STAGE-CPU lines after every stage; C-TILT (b) in every piece but x.
  C-REP: tailB is not compared (F1); the bound is compared with v2_3's bound after v2_3's far is replaced by this engine's far_out (F2).
kt_cert_v1_2 (6e476206): kt_cert_v1_1 split into an x and a g process, with STAGE-CPU lines. kt_cert_v1_1 (91be74ce): its smoke (eb3e055d)
passed C-TILT, PLANT-TILT and the explicit part (140 s) and stopped at its 540 s cap inside engine A.
kt_cert_v1_1 was the REVISION of kt_cert_v1.py (3e1f2d4e) on the ADD2 review (43eb7b39), item A5, with the A1 note
SPEC_M1_CERT_v1_1_ADD2_v1_1 (34722fc0: the quadrature (near^2 + far_out)^{1/2} is exact; no engine change). New: C-TILT, in arb, before the engine:
  (a) domination: each tilt rate meets rate >= -log(1 - a)/(2a) for its radius (c_m: a_m, c_e: a_e, c_pp: a_pp), and a_pp >= sin^2(asin rho_m +
      delta); (b) admissibility: every tilted covariance the engine forms (tilted_cov_a, the Chernoff lambda tilts of the tails and the annulus,
      and A - 2 c_e t I) is certainly positive definite (logged with its smallest leading minor; a failure stops the item as before) and every
      Chernoff lambda is positive. PLANT-TILT: (a) with c_m (1 - 1e-9) and (b) with a lambda = 1e3 tilt must both fail.
  Everything else is kt_cert_v1's.
kt_cert_v1 (pk02, code/pk02/): M1 of SPEC_M1_CERT_v1_1 (c81c956f) with ADD1 (badf0f57) and SPEC_M1_CERT_v1_1_ADD2_v1 (ddd85cfd):
engine A (KT-C) in ball arithmetic (python-flint arb; no *_series function), ported from kt_c_v2_3.py (71a224a2) part for part, with the xi hook
(kinds h1 = xi_h p_e1, h3 = xi_h p_e3; h = xi_h p0 is kt_c_v2_3's kind) and the F2(a) / C-BAD lines of ADD2 v1 sect. 6 and 8.
Built from pk01's scratch parts p1, p2a, p2b1, p2b2a (copied read-only as SRC_pk01_kt_cert_v1_p*.py) and its port map; arb layer
arbeng_c2b_v1.py = pk01's arbeng_v1.py draft (a70d0cc4), frozen under this name.

Model (ADD2 sect. 1): every certified quantity is an arb ball; exact binary64 inputs (json data, radii, the m_g) are exact balls; the couplings A, B,
  X0, Y0 and DELTA are computed in arb; covariances come from arb_mat Laplacians with an exact gauge basis; index arithmetic is numpy int64.
  Precision: ctx.prec = 512 (kt_cert_v1_4, ADD2 v1_3; ADD2 sect. 1 named 128 to 256 bits, and kt_cert_v1 to v1_3 used 256). C-RAD gates the
  outcome.
  Free choices, exact binary64 from the point they are made: the m_g (midpoints of ball solutions; any real m_g is allowed, (C1)), the radii
  RHO_M, RHO_E, the Chernoff lambdas 0.45 and 0.5. Derived parameters rounded UP from their arb values (pk01's C-RATE, C-APP): the tilt
  rates c_m, c_e, c_pp and the annulus radius a_pp.
FLOAT inputs (ADD2 sect. 3), printed with repr and marked: the outer far parts (with the cross terms and log R) and gB (riglap2/riglap3,
  part 4b; M3); eps_r (vacscale; M2) and the Gram lower bounds Z (kt_s9b_v1's J = 170 entries; M3), on the FLOAT-IN lines.
Items: <piece>.<suffix> as above, J = 300; smoke = e1n4 with C-REP and C-RAD; hsmoke = hn4 with C-HOOK0, C-RAD and PLANT-HOOK0; C-REP on the
  g pieces of e1, e3, h and a at N = 3 and 4. C-REP: each compared part to half a unit of its last printed digit (kt_c_v2_3 prints them with
  3 or 4 digits), the bound to 1e-6 relative as above. C-RAD: relative radii of the bound, nP, nD, nR0 (nR) at most 1e-12.
Prices [E], from kt_cert_v1_2's STAGE-CPU lines at 256 bits (e1n4: explicit 147 s; CondMomA 201 s, condE 10 s, nD 13 s; nP 4 s; a
  degree-16 tail table 61 s, degree 14 40 s; far 5 s), times about 1.3 for 512 bits; every piece runs under LIM <= 540.
Run (own folder, a producing piece before the g piece that reads it): D=/mnt/g2/release/root/code/pk02;
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=$D/tmp_kt_s9b3 OMP_NUM_THREADS=1 timeout 580 nice -n 10
  prlimit --as=8589934592 -- python3 -I -B $D/kt_cert_v1_5.py <item> <LIM> > $D/out_kt_cert_v1_5_<item>.out
  2> $D/out_kt_cert_v1_5_<item>.err
"""
import resource, sys, time, math, hashlib, signal, os, traceback, re, json, itertools

SUFFIXES = tuple(k + s for k in ('e1', 'e3', 'h', 'h1', 'h3', 'a') for s in ('n4', 'n3')) + ('smoke', 'hsmoke')
TAILP = tuple('t' + f for f in 'XBA') + tuple('t%s%d' % (f, i) for f in 'XBA' for i in range(3))
ITEMS = tuple('%s.%s' % (p, s) for s in SUFFIXES for p in ('x', 'c') + TAILP + ('g',) if not (s[0] == 'a' and p not in ('x', 'g')))
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: kt_cert_v1_5.py ITEM LIM   (ITEM = <piece>.<suffix>, piece x, c, tX, tB, tA, tX0..tA2 or g (kind a: x or g), suffix <kind>n4, '
          '<kind>n3 (kind e1, e3, h, h1, h3, a), smoke or hsmoke; LIM = RLIMIT_CPU soft limit in s, hard LIM + 5)')
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


class CapStop(Exception):
    pass


SCR = '/mnt/g2/release/root/code/pk10/scripts'
INP = '/mnt/g2/release/root/code/pk10/scratch'
SRC = '/mnt/g2/release/root/code/pk01'
OWN = '/mnt/g2/release/root/code/pk02'
ENGINE = {
    'amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc',
    'npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
    'pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
    'riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
    'riglap3.py': 'e394f81567e62222240050c7cbc70c480b0804d929a8713a7b30e70ebbf1ea69',
}
OWNFILES = {
    'arbeng_c2b_v2.py': '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0',
}
SRCFILES = {
    'out_kt_c_v2_3_e1n4.out': 'f38d2d62c50bdb136aeb7399a6c04dc9112137cba199e17a622adcd6f4e2e3c9',
    'out_kt_c_v2_3_e3n4.out': '8d1053659fff5e4a7ae1841c0e6f48aea65245f447fab5e438a854382aa7ee2a',
    'out_kt_c_v2_3_hn4.out': '75795b6b1c5fea53d3341e346c1d8aa2d13a1fc5ac16ef79b33e03201bc9f688',
    'out_kt_c_v2_3_an4.out': '324fab52a7c469bf696e08c22a5134d99ff531516573150586562fa2cc516cc5',
    'out_kt_c_v2_3_e1n3.out': 'cee0e054ab2b800d8a6bcd6cbb7e88bbb0c3b34d81c0e5748c8e2dc0494fc1e5',
    'out_kt_c_v2_3_e3n3.out': '8433814c3f7bdf25f78c19e583d2edaa3af13b0010c5990adbc60ae7e7f63825',
    'out_kt_c_v2_3_hn3.out': '6ec2a250c79ded297b6d6122f902060792dc096b62f253a17a12ee951a425486',
    'out_kt_c_v2_3_an3.out': 'ebaad15a140d05cf42fb8cb318a9db97de1748e93f4fa5b632ac6a53f805f5ff',
    'out_kt_s9b_v1_n3.out': '1e3aa09ef3a828d5ffc3a14bebb610958ee7c5e815b933f0f8442b640ce7eebc',
    'out_kt_s9b_v1_n4.out': 'ab1273ab55f8e1d1a9160eb35c5620a706b837aefd16ed430f4126eb3d0b97f0',
}
INPUTS = {
    'ts_N3_S.json': '26e20e76fbce80c205703f5ba27395ebddaeaa2713bb129b0b4e5902a2061955',
    'ts_N4_J170_D_S.json': 'd6d104ea1f2f64a82f051ce2872f1fbbd0628c9875b0743e4815bf74643fea8c',
    'vacres_K3_N3.json': 'ebcbd08ca532642188071c964039808a318038020bb1a788a7fa3a49cb357426',
    'vacres_K3_N4.json': '516b2501c37a65b21b617fba3cb1d7b02adf9966f409bc5105418822dfa0e765',
    'vacscale_N3.txt': '7b73541c465a7d1642f0ebaf848a462dd3c113e63184723682462c003d0dd607',
    'vacscale_N4.txt': '75810250a306804bfba13237ab2eb128dc62323f7b5a660f93d1698d9ade95b1',
}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


SELF_SHA = sha_file(os.path.abspath(__file__))
out('kt_cert_v1_5 sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (SELF_SHA, MODE, LIM, LIM, LIM + 5))
_bad = []
for _d, _tab in ((SCR, ENGINE), (OWN, OWNFILES), (SRC, SRCFILES), (INP, INPUTS)):
    for _n in sorted(_tab):
        _got = sha_file(os.path.join(_d, _n))
        if _got != _tab[_n]:
            _bad.append('%s %s' % (_n, _got))
out('C-HASH %s (%d engine files, %d own files, %d predecessor outputs, %d inputs)%s' % (
    'PASS' if not _bad else 'FAIL', len(ENGINE), len(OWNFILES), len(SRCFILES), len(INPUTS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, SCR)
sys.path.insert(0, OWN)

import numpy as np
import flint
from flint import arb, arb_mat, ctx
ctx.prec = 512                   # kt_cert_v1_4 (ADD2 v1_3): kt_cert_v1_2's ghsmoke failed C-RAD at 256 bits through the tail tables
import arbeng_c2b_v2 as ae
out('ENV: python-flint %s, numpy %s, python %s, ctx.prec %d' % (flint.__version__, np.__version__, sys.version.split()[0], ctx.prec))

PIECE, SUFFIX = MODE.split('.', 1)               # the pieces of an item and their hand-offs: part 6
SMOKE = SUFFIX if SUFFIX in ('smoke', 'hsmoke') else None
KIND = {'smoke': 'e1', 'hsmoke': 'h'}[SMOKE] if SMOKE else SUFFIX[:-2]
NN = 4 if SMOKE else int(SUFFIX[-1])
nn = NN - 1
SQ5, SQ21 = arb(5).sqrt(), arb(21).sqrt()
A_ = (3 + SQ21) / 6
B_ = (3 * SQ5 - SQ21) / 12
TRI = [A_, A_, B_]
PAIRS = [(0, 1), (1, 2), (0, 2)]
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]
X0 = (7 - 3 * SQ5) / 2
Y0 = (23 - 5 * SQ21) / 2
SFILE = {4: 'ts_N4_J170_D_S.json', 3: 'ts_N3_S.json'}[NN]
VFILE = {4: 'vacres_K3_N4.json', 3: 'vacres_K3_N3.json'}[NN]
VSFILE = {4: 'vacscale_N4.txt', 3: 'vacscale_N3.txt'}[NN]
RHO_M, RHO_E = 0.55, 0.6                    # free radii (exact binary64)
DELTA = arb.pi() * 40 / 180                 # 40 degrees, in arb
J_MAIN = 300
EVEN = (0, 1, 3)
KX, NVX = 3, 14
XS, QS, XD, QD = [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]
QH, QT = 12, 13
QGROUPS, QCAPS = [0, 0, 0, 1, 1, 1, 2, 3], {1: 2, 2: 1, 3: 1}
NV12, BB = 12, 26




# ====================================================================================== part 2a: the conditioning (kt_c_v2_3 l.300-332)
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
    """kt_c_v2_3.build_conditioning in balls: phi'' = A^-1 phi + zeta, zeta ~ N(0, A^-1), A = I + L_tri; forms X'' (0-2), Q'' (3-5), QH (6),
    QT (7); the W matrix is exact (entries 0, +-1)."""
    Ainv = (arb_mat(3, 3, [1 if i == j else 0 for i in range(3) for j in range(3)]) + tri_laplacian()).inv()
    Mm = arb_mat(6, 3)
    Cm = arb_mat(6, 6)
    for i in range(3):
        for j in range(3):
            Mm[i, j] = Ainv[i, j]
            Cm[i, j] = Ainv[i, j]
        Mm[3 + i, i] = 1
    Wc = arb_mat(6, 8)
    for r in range(3):
        Wc[r, r] = 1
    for p, (r, s) in enumerate(PAIRS):
        Wc[r, 3 + p] = 1
        Wc[s, 3 + p] = -1
    Wc[1, 6] = 1
    Wc[3 + 1, 6] = -1
    Wc[0, 7] = 1
    Wc[3 + 0, 7] = -1
    return ae.CondMomA(Mm, Cm, Wc, nn, 2 * KX + 2, groups=QGROUPS, caps=QCAPS)


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
    """the conditioned monomial e2 (forms X'' 0-2, Q'' 3-5, QH 6, QT 7) is inside the caps of build_conditioning."""
    return all(sum(x for x, g in zip(e2, QGROUPS) if g == k) <= cap for k, cap in QCAPS.items())




# ====================================================================================== part 2b1: series helpers (kt_c_v2_3 l.234-299)
Series, padd, pscale, pmul, pconst, pvar = ae.Series, ae.padd, ae.pscale, ae.pmul, ae.pconst, ae.pvar
WX = ae.w_coeffs(KX)                         # exact rationals as balls


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


Smat = np.array(load_json(os.path.join(INP, SFILE))['S'])      # exact binary64 data
lam0 = load_json(os.path.join(INP, SFILE))['lam0']
R3 = load_json(os.path.join(INP, VFILE))
QV = [None, R3['q1'], R3['q2'], R3['q3']]


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


def state_poly(xs, b):
    res = one().scale(arb(float(Smat[0, b])))
    for cb, mono_ in zip(Smat[1:, b], BASIS):
        if cb != 0.0:
            res = res + mono_series(xs, mono_).scale(arb(float(cb)))
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
    assert len(cm.gvars) == 6
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
        assert sum(e2) <= D and qcap_ok(e2), e2
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
                assert sum(e) <= D, e
                mult(condvec(tuple(e[6:])), tuple(e[:6]), ae.A(c), acc)
            res.append({tuple(int(x) for x in sexp[k]): v for k, v in acc.items() if not v.is_zero()})
        return res
    return condE


# ====================================================================================== part 2b2b: B0 engines, projections, explicit part
# (kt_c_v2_3 l.436-637, per item kind; the m_g are the midpoints of ball solutions, then exact binary64: any real m_g is allowed, (C1))
deg = ae.deg


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
            assert sum(e[6:]) == 0, e
            k = tuple(e[:6])
            acc[k] = acc[k] + c if k in acc else ae.A(c)
        res.append({e: c for e, c in acc.items() if not c.is_zero()})
    return res


def strip2_laplacian():
    """the Laplacian of lapl2.strip_graph(2, (A, B)) in arb: vertex 3 col + row; triangles (A, A, B); horizontals 1."""
    L = arb_mat(6, 6)
    edges = []
    for j in range(2):
        T, Mv, Bv = 3 * j, 3 * j + 1, 3 * j + 2
        edges += [((T, Mv), A_), ((Mv, Bv), A_), ((T, Bv), B_)]
    edges += [((r, 3 + r), arb(1)) for r in range(3)]
    for (u, v), c in edges:
        L[u, u] += c
        L[v, v] += c
        L[u, v] -= c
        L[v, u] -= c
    return L


def gauge_pinv(L):
    """B (B^T L B)^-1 B^T with the exact basis B = [e_s - e_0] of the complement of the constant vector; equal to the float code's
    Qb (Qb^T L Qb)^-1 Qb^T for any basis Qb of that complement (ADD2 sect. 1)."""
    V = L.nrows()
    Bm = arb_mat(V, V - 1)
    for s in range(1, V):
        Bm[s, s - 1] = 1
        Bm[0, s - 1] = -1
    return Bm * (Bm.transpose() * L * Bm).inv() * Bm.transpose()


def make_B0c(c0, c1):
    """B0(f, h) = E_D[f(sigma) h(sigma')] for deg f <= c0 (first column) and deg h <= c1 (second column), in balls."""
    Gp = gauge_pinv(strip2_laplacian())
    WD = arb_mat(6, 12)
    for col in range(2):
        for r in range(3):
            WD[3 * col + r, 6 * col + r] = 1
        for p, (r, s) in enumerate(PAIRS):
            WD[3 * col + r, 6 * col + 3 + p] = 1
            WD[3 * col + s, 6 * col + 3 + p] = -1
    am = ae.AllMom2A(WD.transpose() * Gp * WD, nn, c0 + c1, groups=[0] * 6 + [1] * 6, caps={0: c0, 1: c1})
    z6 = (0,) * 6

    def B0(f, h):
        assert deg(f) <= c0 and deg(h) <= c1, (deg(f), deg(h), c0, c1)
        return am.E2({tuple(e) + z6: c for e, c in f.items()}, {z6 + tuple(e): c for e, c in h.items()})
    return B0


def solve_mid(Gb, vb):
    """the float choice m: the midpoints of the ball solution of Gb m = vb, as binary64 numbers (exact from here on)."""
    nb = len(vb)
    Gm, vm = arb_mat(nb, nb), arb_mat(nb, 1)
    for i in range(nb):
        vm[i, 0] = vb[i]
        for j in range(nb):
            Gm[i, j] = Gb[i][j]
    sol = Gm.solve(vm)
    return [float(sol[i, 0].mid()) for i in range(nb)]


def project(B0, f, basis):
    """kt_c_v2_3.project with m = solve_mid (free choice, (C1)); r = f - sum m_i b_i in balls; returns m, r and the ball B0(r, r)."""
    nb = len(basis)
    m = solve_mid([[B0(basis[i], basis[j]) for j in range(nb)] for i in range(nb)], [B0(basis[i], f) for i in range(nb)])
    r = padd(f, *[pscale(basis[i], -m[i]) for i in range(nb)])
    return m, r, B0(r, r)


def project_nonorm(B0low, B0mix, f, basis):
    nb = len(basis)
    m = solve_mid([[B0low(basis[i], basis[j]) for j in range(nb)] for i in range(nb)], [B0mix(basis[i], f) for i in range(nb)])
    r = padd(f, *[pscale(basis[i], -m[i]) for i in range(nb)])
    return m, r


def xfrac(P):
    big = max([fup(c) for c in P.values()] + [0.0])
    xs = max([fup(c) for e, c in P.items() if sum(e[:3]) > 0] + [0.0])
    return xs / big if big > 0 else 0.0


STATE_OF = {'e1': 'e1', 'e3': 'e3', 'h': 'psi', 'h1': 'e1', 'h3': 'e3', 'a': 'psi'}
HOOK = ('h', 'h1', 'h3')


def explicit_part(kind, fails, fires):
    """orders 0-3 of the item's source in balls: m (4 orders x basis psi, e1, e3), r0..r3 (sigma polynomials), T3 (the series before the
    conditional expectation, for the inner tails), bas (the basis series). Checks as kt_c_v2_3 for the item's kind."""
    t0 = cpu()
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
    EL, E0 = HL.exp(), H0.exp()
    xiD, xiS = xis(XD, QD), xis(XS, QS)
    xih = xi_pair(XS[1], XD[1], QH)
    G = ('psi', 'e1', 'e3')
    pS = {'psi': vac_poly(xiS), 'e1': state_poly(xiS, 1), 'e3': state_poly(xiS, 3)}
    bas = {g: restrict6(E0 * pS[g]) for g in G}
    if kind == 'a':
        T3 = None
        src = restrict6(E0 * ((xiS[0] + xiS[1]).scale(arb(1) / 2)) * pS['psi'])
    else:
        b = STATE_OF[kind]
        pD = vac_poly(xiD) if b == 'psi' else state_poly(xiD, {'e1': 1, 'e3': 3}[b])
        T3 = EL * xih * pD if kind in HOOK else EL * pD
        src = make_condE(build_conditioning())(T3)
    out('EXPLICIT N=%d %s: series and conditional expectations to order %d, %.1f s' % (NN, kind, KX, cpu() - t0))
    degs2 = max([deg(src[o]) for o in range(3)] + [deg(bas[g][o]) for g in G for o in range(3)])
    degs3 = max([deg(src[3])] + [deg(bas[g][3]) for g in G])
    B0a = make_B0c(degs2, degs2)
    B0b = make_B0c(2, max(degs3, degs2))
    b0 = [bas[g][0] for g in G]
    n11, n33, o13 = B0a(b0[1], b0[1]), B0a(b0[2], b0[2]), B0a(b0[1], b0[2])
    ok = fup(n11 - 1) <= 1e-9 and fup(n33 - 1) <= 1e-9 and fup(o13) <= 1e-9
    out('K-ORTH N=%d: |B0(e1,e1) - 1| <= %.2e, |B0(e3,e3) - 1| <= %.2e, |B0(e1,e3)| <= %.2e -> %s (%.1f s)' % (
        NN, fup(n11 - 1), fup(n33 - 1), fup(o13), 'PASS' if ok else 'FAIL', cpu() - t0))
    if not ok:
        fails.append('K-ORTH')
    nb = 3
    bk = [[bas[g][o] for g in G] for o in range(4)]
    s = src
    m0, r0, n0 = project(B0a, s[0], bk[0])
    f1 = padd(s[1], *[pscale(bk[1][i], -m0[i]) for i in range(nb)])
    m1, r1, n1 = project(B0a, f1, bk[0])
    f2 = padd(s[2], *[pscale(bk[2][i], -m0[i]) for i in range(nb)], *[pscale(bk[1][i], -m1[i]) for i in range(nb)])
    m2, r2, n2 = project(B0a, f2, bk[0])
    f3 = padd(s[3], *[pscale(bk[3][i], -m0[i]) for i in range(nb)], *[pscale(bk[2][i], -m1[i]) for i in range(nb)],
              *[pscale(bk[1][i], -m2[i]) for i in range(nb)])
    m3, r3 = project_nonorm(B0a, B0b, f3, bk[0])
    rn = [fup(nsqrt(x)) for x in (n0, n1, n2)]
    ex = dict(G=G, m=[m0, m1, m2, m3], r0=r0, r1=r1, r2=r2, r3=r3, n=rn, T3=T3, bas=bas)
    out('EXPLICIT N=%d %-3s: m0 %s | m1 %s | m2 %s | m3 %s; |r0| <= %.2e |r1| <= %.6e |r2| <= %.6e; deg r3 %d (%.1f s)' % (
        NN, kind, ' '.join(repr(x) for x in m0), ' '.join(repr(x) for x in m1), ' '.join(repr(x) for x in m2), ' '.join(repr(x) for x in m3),
        rn[0], rn[1], rn[2], deg(r3), cpu() - t0))
    if kind in ('e1', 'e3'):
        idx, lm = {'e1': (1, lam0[1]), 'e3': (2, lam0[3])}[kind]
        others = max(abs(m0[i]) for i in range(3) if i != idx)
        ok = rn[0] <= 1e-8 and abs(m0[idx] - lm) <= 1e-9 and others <= 1e-8
        out('K-EIG N=%d %s: |r0| <= %.2e, m_diag %.12f vs lam0 %.12f, others %.2e -> %s' % (NN, kind, rn[0], m0[idx], lm, others,
                                                                                          'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('K-EIG %s' % kind)
    if kind in ('h', 'a'):
        s21, s5 = SQ21, SQ5
        ref = float((nn * (1 - 2 / s21) / 2).mid()) if kind == 'h' else float((nn * (3 / (2 * s21) + 1 / (2 * s5)) / 2).mid())
        ok = rn[0] <= 1e-8 and abs(m0[0] / ref - 1) <= 1e-9 and ((abs(m0[1]) <= 1e-8) if kind == 'h' else True)
        out('K-%s0 N=%d: |r0| <= %.2e, psi coefficient %.12f vs exact %.12f, e1 coefficient %.2e -> %s' % (
            kind.upper(), NN, rn[0], m0[0], ref, m0[1], 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('K-%s0' % kind.upper())
    if kind in ('h1', 'h3'):
        out('INFO N=%d %s: order-0 residual |r0|_B0 <= %.6e (not zero for the hook kinds; enters nP as t^0 r0, ADD2 sect. 3)' % (NN, kind, rn[0]))
    lead = next((o for o in (0, 1, 2) if rn[o] > 1e-8), None)
    if lead is not None:
        xf = xfrac([r0, r1, r2][lead])
        ok = xf <= 1e-9
        if kind in ('h1', 'h3'):
            out('INFO K-INV N=%d %s: leading residual order %d, X share %.1e (not gated for the hook kinds)' % (NN, kind, lead, xf))
        else:
            out('K-INV N=%d %s: leading residual order %d, X share %.1e -> %s' % (NN, kind, lead, xf, 'PASS' if ok else 'FAIL'))
            if not ok:
                fails.append('K-INV')
    return ex


# ====================================================================================== part 3: majorants (kt_c_v2_3 l.629-762), NPolyA in balls
# Derived free parameters (pk01's C-RATE, C-APP): the tilt rates and the annulus radius are binary64 numbers rounded UP from their arb
# values, so every inequality the proof needs (rate >= -log(1 - a)/(2a), a_pp >= sin^2(asin rho_m + delta)) holds by construction.
def up_float(x):
    """a binary64 number >= every point of the ball x."""
    u = x.upper()
    f = float(u)
    if not (arb(f) >= u):
        f = math.nextafter(f, math.inf)
    assert arb(f) >= u
    return f


a_m, a_e = RHO_M ** 2, RHO_E ** 2
c_m, c_e = (up_float(-(1 - arb(x)).log() / (2 * arb(x))) for x in (a_m, a_e))
_rho_pp = (arb(RHO_M).asin() + DELTA).sin()
a_pp = up_float(_rho_pp * _rho_pp)
c_pp = up_float(-(1 - arb(a_pp)).log() / (2 * arb(a_pp)))
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


def xibar_cross(iu, iv, aa, t, nmax, cfac):
    """majorants of xi_h(tau) derivatives for the cross pair (sigma_M, sigma''_M), with Q_MM''/2 <= X_M + X''_M."""
    Dx = D2(iu, iv)
    lst = [xv(iu).add(xv(iv)).add(trade(Dx.scale(cfac(aa, 1) / 8), t, 1))]
    for l in range(1, nmax + 1):
        lst.append(Dx.mul(Mk(iu, iv, l - 1)).scale(arb(math.factorial(l)) / 8 * cfac(aa, l + 1)))
    return lst


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


def pi_state(j, Xi, Qi, aa, t, cfac, b):
    xd = xibar(Xi, Qi, aa, t, j, cfac)
    res = ONE_P.scale(abs(float(Smat[0, b]))) if j == 0 else ae.NPolyA(NV12, BB)
    for cb, mono_ in zip(Smat[1:, b], BASIS):
        if cb != 0.0:
            res = res.add(fbd(xd, mono_, j).scale(abs(float(cb))))
    return res


def pi_h(j, aa_cross, aa_e, t, cfac):
    xh = xibar_cross(XS[1], XD[1], aa_cross, t, j, cfac)
    res = ae.NPolyA(NV12, BB)
    for l in range(j + 1):
        res = res.add(xh[l].mul(pi_vac(j - l, XD, QD, aa_e, t, cfac)).scale(math.comb(j, l)))
    return res


def pi_hb(j, aa_cross, aa_e, t, cfac, b):
    """the hook kinds h1, h3 (ADD2 sect. 3): Leibniz of xibar_cross with pi_state of the inner state b, as pi_h does with pi_vac."""
    xh = xibar_cross(XS[1], XD[1], aa_cross, t, j, cfac)
    res = ae.NPolyA(NV12, BB)
    for l in range(j + 1):
        res = res.add(xh[l].mul(pi_state(j - l, XD, QD, aa_e, t, cfac, b)).scale(math.comb(j, l)))
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
    assert x > 0
    return (-(x * x)).exp() / (x * arb.pi().sqrt()) + (2 * s / arb.pi()).sqrt() * (-s / 2).exp()


E9 = [((6 + r, 6 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((6 + r, r), 1) for r in range(3)] + [((r, 3 + r), 1) for r in range(3)] + [((0, 1), 1), ((1, 2), 1)]
L9 = lap_a(E9, 9)
B9 = gauge_basis_a(9, range(6))
ED_ = [((r, s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
      [((r, 3 + r), 1) for r in range(3)]
LD = lap_a(ED_, 6)
BD = gauge_basis_a(6, range(6))
W10 = arb_mat(6, 10)
for r in range(3):
    W10[r, r] = 1
    W10[3 + r, 3 + r] = 1
for p_, (r, s) in enumerate(PAIRS):
    W10[3 + r, 6 + p_] = 1
    W10[3 + s, 6 + p_] = -1
W10[1, 9] = 1
W10[3 + 1, 9] = -1
W10_INT = [[0] * 10 for _ in range(6)]       # W10's exact integers, for AllMom2A's exact zeros (kt_cert_v1_5)
for r in range(3):
    W10_INT[r][r] = 1
    W10_INT[3 + r][3 + r] = 1
for p_, (r, s) in enumerate(PAIRS):
    W10_INT[3 + r][6 + p_] = 1
    W10_INT[3 + s][6 + p_] = -1
W10_INT[1][9] = 1
W10_INT[3 + 1][9] = -1
assert all(W10[i, j] == W10_INT[i][j] for i in range(6) for j in range(10))
PLANTED = [False]                            # PLANT-SING runs once per piece, on its first table
MAP10 = {0: 0, 1: 1, 2: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8, QH: 9}


def to10(P, nv):
    res = {}
    for e, c in P.items():
        assert all(e[i] == 0 for i in range(nv) if i not in MAP10), e
        e10 = [0] * 10
        for i, j in MAP10.items():
            if i < nv:
                e10[j] = e[i]
        e10 = tuple(e10)
        res[e10] = res[e10] + c if e10 in res else ae.A(c)
    return {e: c for e, c in res.items() if not c.is_zero()}


def sub_mat(M, idx):
    S = arb_mat(len(idx), len(idx))
    for a_, i in enumerate(idx):
        for b_, j in enumerate(idx):
            S[a_, b_] = M[i, j]
    return S


def joint_moments_a(rates9, Dmax, qcap, extra=None, label='tilted_cov'):
    """the joint tilted moments of the ten forms (sigma X, sigma'' X, sigma'' Q, Q_MM''); extra: an optional 9 x 9 quadratic tilt (F1's
    lam Q_rr''). kt_cert_v1_5: the ten forms span six coordinates, so AllMom2A gets W10's exact integers (W_int) and treats the minors of
    rank-deficient subsets as exact zeros (arbeng_c2b_v2). Returns (table, N, G9, Gam)."""
    G9, N9 = tilted_cov_a(L9, B9, rates9, extra=extra, label=label)
    if G9 is None:
        return None, None, None, None
    G6 = sub_mat(G9, [0, 1, 2, 6, 7, 8])
    Gam = W10.transpose() * G6 * W10
    return ae.AllMom2A(Gam, nn, Dmax, groups=[0] * 6 + [1] * 4, caps={1: qcap}, W_int=W10_INT), N9, G9, Gam


SING_FAILS, SING_FIRES = [], []         # C-SING failures and unfired PLANT-SING, merged into the item's verdict in main()


def det_sub(Gam, A):
    """det(Gam_A) by the same arithmetic as AllMom2A (an arb_mat of the entries, then det)."""
    sub = arb_mat(len(A), len(A))
    for a_, fa in enumerate(A):
        for b_, fb in enumerate(A):
            sub[a_, b_] = Gam[fa, fb]
    return sub.det()


def c_sing(am, Gam, qcap, label):
    """C-SING (arbeng_c2b_v2's exact zeros, on this table's own Gram matrix): (i) every subset the table kept is of full exact rank and its
    stored (-2)^|A| det(Gam_A) is identical (midpoint and radius) to the direct computation; every subset it dropped is rank-deficient and
    its det ball contains 0; kept and dropped together are all the subsets of sizes up to min(10, D) the caps allow; (ii) degree-4 tables
    with and without the rule overlap in every moment."""
    ok, nk, seen = True, 0, set()
    for j in range(1, len(am.Dj)):
        cj, vj = am.Dj[j]
        if len(cj) == 0:
            continue
        for row, v in zip(am.decode(cj), vj):
            A = tuple(int(f) for f in np.flatnonzero(row))
            d = arb(-2) ** len(A) * det_sub(Gam, A)
            ok = ok and len(A) == j and ae.int_rank(W10_INT, A) == j and d.mid() == v.mid() and d.rad() == v.rad()
            seen.add(A)
            nk += 1
    for A, dv in am.dropped:
        ok = ok and ae.int_rank(W10_INT, A) < len(A) and dv.contains(0)
        seen.add(tuple(A))
    allowed = set(A for j in range(1, min(10, am.D) + 1) for A in itertools.combinations(range(10), j) if sum(1 for f in A if f >= 6) <= qcap)
    ok = ok and seen == allowed
    kw = dict(groups=[0] * 6 + [1] * 4, caps={1: qcap})
    t_rule, t_free = ae.AllMom2A(Gam, nn, 4, W_int=W10_INT, **kw), ae.AllMom2A(Gam, nn, 4, **kw)
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
    """PLANT-SING: the rule with X0's column of W10 set to zero (so every subset with X0 counts as rank-deficient) must stop, since
    det(Gam_{X0}) = Var(X0) > 0 excludes 0."""
    bad = [row[:] for row in W10_INT]
    for i in range(6):
        bad[i][0] = 0
    try:
        ae.AllMom2A(Gam, nn, 2, groups=[0] * 6 + [1] * 4, caps={1: qcap}, W_int=bad)
        fired = False
    except ValueError:
        fired = True
    out('PLANT-SING N=%d: the rule with X0\'s column of W10 zeroed %s -> %s' % (NN, 'stops' if fired else 'passes',
                                                                               'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        SING_FIRES.append('PLANT-SING')


def supF_a(kind, J):
    """sup |F| of the item's source in balls (an upper bound by the triangle inequality on [0, 2J]^3)."""
    t = arb(1) / J
    if kind in ('h', 'a'):
        sup0 = 1 + sum(t ** i * abs(cb) * arb(2 * J) ** len(mono_) for i, coef in ((1, QV[1]), (2, QV[2]), (3, QV[3]))
                       for cb, mono_ in zip(coef, BASIS))
        return 2 * J * sup0 if kind == 'h' else sup0
    b = {'e1': 1, 'e3': 3, 'h1': 1, 'h3': 3}[kind]
    supb = abs(float(Smat[0, b])) + sum(abs(float(cb)) * arb(2 * J) ** len(mono_) for cb, mono_ in zip(Smat[1:, b], BASIS))
    return 2 * J * supb if kind in ('h1', 'h3') else supb


def l0_remainder(G, m, t):
    """L0 side: sum_g sum_{j<=3} |m_gj| t^j t^{4-j}/(4-j)! Dbar_{4-j}(E0 p_g) (sigma variables), and the h0 majorants."""
    h0 = {k: hk(k, [], bonds0, cf_rad) for k in range(1, 5)}
    R0 = ae.NPolyA(NV12, BB)
    for gi, g in enumerate(G):
        for j in range(4):
            n_ = 3 - j
            if g == 'psi':
                pis0 = [pi_vac(i, XS, QS, a_m, t, cf_rad) for i in range(n_ + 2)]
            else:
                pis0 = [pi_state(i, XS, QS, a_m, t, cf_rad, {'e1': 1, 'e3': 3}[g]) for i in range(n_ + 2)]
            R0 = R0.add(Dbar(n_ + 1, h0, pis0).scale(abs(m[j][gi]) * t ** j * t ** (n_ + 1) / math.factorial(n_ + 1)))
    return R0, h0


def source_pis(kind, t):
    if kind == 'h':
        return [pi_h(j, max(a_m, a_e), a_e, t, cf_rad) for j in range(5)]
    b = {'e1': 1, 'e3': 3, 'h1': 1, 'h3': 3}[kind]
    if kind in ('h1', 'h3'):
        return [pi_hb(j, max(a_m, a_e), a_e, t, cf_rad, b) for j in range(5)]
    return [pi_state(j, XD, QD, a_e, t, cf_rad, b) for j in range(5)]


# ====================================================================================== part 4b: FLOAT inputs (ADD2 sect. 3; milestone M3)
# The outer far parts and gB, verbatim from kt_c_v2_3 l.763-969 in binary64 (riglap2/riglap3 majorants, tree bounds, ive), with the float
# couplings; every value they return is printed and marked FLOAT. factors_for gains the hook kinds h1, h3 (ADD2 sect. 3).
import riglap2
import riglap3 as _r3
from amom2b import AllMom2
from npoly import NPoly
from scipy.special import ive

A_f = (3 + math.sqrt(21)) / 6
B_f = (3 * math.sqrt(5) - math.sqrt(21)) / 12
TRI_f = [A_f, A_f, B_f]
DELTA_f = math.radians(40.0)
RHO_P = 0.9
A_P = RHO_P ** 2
C_P = -math.log(1 - A_P) / (2 * A_P)


def lap_f(edges, V):
    L = np.zeros((V, V))
    for (u, v), c in edges:
        L[u, u] += c; L[v, v] += c; L[u, v] -= c; L[v, u] -= c
    return L


def gauge_basis_f(V, S):
    u = np.zeros(V); u[list(S)] = 1.0
    return np.linalg.svd(np.eye(V) - np.outer(u, u) / u.dot(u))[0][:, :V - 1]


def tilted_cov_f(L, Bm, rates, extra=None):
    Lr = Bm.T @ L @ Bm
    Lx = L - 2 * np.diag(rates)
    if extra is not None:
        Lx = Lx - 2 * extra
    Lt = Bm.T @ Lx @ Bm
    if np.linalg.eigvalsh(Lt).min() <= 0:
        return None, float('inf')
    return Bm @ np.linalg.inv(Lt) @ Bm.T, (np.linalg.det(Lr) / np.linalg.det(Lt)) ** (0.5 * nn)


ED_f = [((r, s), TRI_f[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), TRI_f[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
       [((r, 3 + r), 1.0) for r in range(3)]
E4_f = [((r, s), TRI_f[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((9 + r, 9 + s), TRI_f[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
       [((r, 3 + r), 1.0) for r in range(3)] + [((3 + r, 6 + r), 1.0) for r in range(3)] + [((6 + r, 9 + r), 1.0) for r in range(3)] + \
       [((3, 4), 1.0), ((4, 5), 1.0), ((6, 7), 1.0), ((7, 8), 1.0)]


def npoly_base(F):
    b = 10
    while float(b) ** F >= 9.0e18:
        b -= 1
    return b


def outer_far3(edges, V, S, factors, pairs, J):
    """vacrig11f's outer_far with riglap3 factors (FLOAT; kt_c_v2_3 l.844-881 verbatim)."""
    t = 1.0 / J
    L = lap_f(edges, V)
    Bm_ = gauge_basis_f(V, S)
    g_ = riglap2.Graph(V, dict(edges), pairs, N=NN)
    m_ = _r3.Model3(g_, 3, factors)
    mj_ = _r3.Majorants3(m_, [A_P] * V, t, B=npoly_base(g_.F))
    P0 = mj_.Fbar(0)
    degP = int(P0.degrees().max())
    qP = int(np.stack([(P0.codes // P0.pw[i]) % P0.B for i in range(P0.nv)], axis=1)[:, V:].sum(axis=1).max()) if g_.F > V else 0
    exP = np.stack([(P0.codes // P0.pw[i]) % P0.B for i in range(P0.nv)], axis=1)
    used = np.flatnonzero(exP.any(axis=0))
    assert P0.nv == g_.F and len(used) > 0 and 0 <= int(used.min()) and int(used.max()) < g_.F, (P0.nv, g_.F, used)
    Bu = max(degP, 1) + 1
    P0u = NPoly(len(used), Bu, exP[:, used] @ np.array([Bu ** k for k in range(len(used))], dtype=np.int64), P0.coeffs)
    Wu, gu = g_.W[:, used], [g_.groups[i] for i in used]
    lam = 0.5
    acc = 0.0
    for v in S:
        rates = np.full(V, C_P * t); rates[v] += lam
        G_, N_ = tilted_cov_f(L, Bm_, rates)
        if G_ is None:
            return float('inf')
        am_ = AllMom2(G_, nn, max(degP, 1), W=Wu, groups=gu, caps={1: max(qP, 1)})
        acc += math.exp(-lam * J * a_m) * N_ * riglap2.expect_np(am_, P0u)
    GS = Bm_ @ np.linalg.inv(Bm_.T @ L @ Bm_) @ Bm_.T
    tree = riglap2.tree_couplings(g_)
    if NN == 4:
        lt = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        lt = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    farp = math.exp(min(math.log(sum(math.exp(-th * J * A_P / (2 * GS[v, v])) for v in range(V))) + lt((1 - th) * J) - g_.logmain(J)
                        for th in np.linspace(0.01, 0.99, 197)))
    return acc + _r3.sup_F3(factors, J) * farp


def factors_for(kind, cols4):
    """riglap3 factor list (and pairs) of the source on the outer columns of G4; the hook kinds h1, h3 add the xi factor to their state."""
    fac, prs = [], []
    for col, mid in cols4:
        T_, M_, B_v = col
        prs += [(T_, M_), (M_, B_v), (T_, B_v)]
        if kind in ('e1', 'e3', 'h1', 'h3'):
            b = {'e1': 1, 'e3': 3, 'h1': 1, 'h3': 3}[kind]
            fac.append(('xi', col, float(Smat[0, b]), [float(x) for x in Smat[1:, b]]))
        else:
            fac.append(('p', col, QV[1], QV[2], QV[3]))
        if kind in ('h', 'h1', 'h3'):
            fac.append(('xi', (M_, mid, B_v), 0.0, [1.0] + [0.0] * 8))
            prs.append((M_, mid))
    return fac, prs


def gB_base(J):
    """kt_c_v2_3.gB_base verbatim (FLOAT; riglap2.bound on G4 minus one horizontal bond)."""
    t = 1.0 / J
    th = 0.95
    acc = 0.0
    for r in range(3):
        edges_r = [(e_, c_) for (e_, c_) in E4_f if e_ != (r, 3 + r)]
        Lfull = lap_f(E4_f, 12); Lr_ = lap_f(edges_r, 12)
        Q12 = np.linalg.svd(np.eye(12) - np.ones((12, 12)) / 12)[0][:, :11]
        ratio_main = (np.linalg.det(Q12.T @ Lfull @ Q12) / np.linalg.det(Q12.T @ Lr_ @ Q12)) ** (0.5 * nn)
        gR = riglap2.Graph(12, dict(edges_r), [], N=NN)
        akR, BR = riglap2.bound(gR, [], 1, J, [math.sqrt(min(60.0 * gR.G[v, v] / J, 0.5)) for v in range(12)], 0.9)
        zR = sum(x * t ** k for k, x in enumerate(akR)) + sum(BR.values())
        acc += math.exp(-th * J * (1 - math.cos(DELTA_f))) * ratio_main * zR
    return math.sqrt(acc)


E3_f = [((r, s), TRI_f[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((6 + r, 6 + s), TRI_f[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
       [((r, 3 + r), 1.0) for r in range(3)] + [((3 + r, 6 + r), 1.0) for r in range(3)] + [((3, 4), 1.0), ((4, 5), 1.0)]


def src_factors(kind, col):
    """riglap3 factors (and pairs) of the item's source on one column: xi_a+ p0 for kind a; else the source state (e1, e3; p0 for h; the hook
    kinds by their state, the hook factor |xi_h| <= 2J being taken out as hf in far_mixed, as kt_c_v2_3 does for h on G4)."""
    if kind == 'a':
        T_, M_, B_v = col
        return [('xi', col, 0.0, [0.5, 0.5] + [0.0] * 7), ('p', col, QV[1], QV[2], QV[3])], [(T_, M_), (M_, B_v), (T_, B_v)]
    return factors_for({'h': 'psi', 'h1': 'e1', 'h3': 'e3'}.get(kind, kind), ((col, 0),))


def far_mixed(kind, G, m, t, J):
    """F2: the far side of the two-column domain with every cross term. Pointwise
    |g| <= hf |S| + sum_g |m_g(t)| |phi_g| (hf = 2J for the hook kinds, else 1), so with X_ab = int_U |h_a| K |h_b| (U = Omega_out^c; each
    X_ab the integral of a nonnegative function, X_ab = X_ba by the symmetry of K and U):
        int_U |g| K |g| <= hf^2 X_SS + 2 hf sum_g |m_g| X_Sg + sum_{g,g'} |m_g| |m_g'| X_gg'.
    outer_far3 bounds each X relative to its graph's main term: X_SS on G4 (o4; kind a: on D), X_Sg on G3 (source column 0-2, phi_g on 6-8;
    vacrig11f's E3, l.389; kind a: on D, source on 0-2, phi_g on 3-5), X_gg' on D (phi_g on 0-2, phi_g' on 3-5; computed once per pair).
    Units (engine A; kind a has every X on D, relative to main_D): lambda_h = main_N/main_D (kt_c_v2_3's log_lambda_h), so
    X_Sg/(lambda_h main_D) = X_Sg/main_N = o3, X_gg'/main_D = oD, and X_SS/(lambda_h^2 main_D) = o4/R with R = main_N^2/(main_D main_4);
    kt_c_v2_3 used R = 1; here R is computed from riglap2's main terms (FLOAT, printed) and divided out.
    The FLOAT values are returned for the repr prints (F4); far_out is formed in arb from them. Returns (far_out, {name: FLOAT value})."""
    hf = arb(2 * J) if kind in HOOK else arb(1)
    mg = [abs(sum((arb(m[j][gi]) * t ** j for j in range(4)), arb(0))) for gi in range(len(G))]
    fl = {}
    if kind == 'a':
        fa, pa = src_factors('a', (0, 1, 2))
        fb, pb = src_factors('a', (3, 4, 5))
        fl['oSS'] = outer_far3(ED_f, 6, list(range(6)), fa + fb, pa + pb, J)
        far = arb(fl['oSS'])
    else:
        f4, p4 = factors_for({'h': 'psi', 'h1': 'e1', 'h3': 'e3'}.get(kind, kind), (((0, 1, 2), 4), ((9, 10, 11), 7)))
        fl['oSS'] = outer_far3(E4_f, 12, list(range(3, 9)), f4, p4, J)
        lm = {V: riglap2.Graph(V, dict(edges), [], N=NN).logmain(J) for V, edges in ((6, ED_f), (9, E3_f), (12, E4_f))}
        fl['logR'] = 2 * lm[9] - lm[6] - lm[12]
        far = hf * hf * arb(fl['oSS']) * (-arb(fl['logR'])).exp()
    for gi, g in enumerate(G):
        if mg[gi].is_zero():
            continue
        fa, pa = src_factors(kind, (0, 1, 2))
        if kind == 'a':
            fb, pb = factors_for(g, (((3, 4, 5), 0),))
            fl['oS_%s' % g] = outer_far3(ED_f, 6, list(range(6)), fa + fb, pa + pb, J)
        else:
            fb, pb = factors_for(g, (((6, 7, 8), 0),))
            fl['oS_%s' % g] = outer_far3(E3_f, 9, list(range(3, 9)), fa + fb, pa + pb, J)
        far += 2 * hf * mg[gi] * arb(fl['oS_%s' % g])
    for gi, g in enumerate(G):
        for hi in range(gi, len(G)):
            if mg[gi].is_zero() or mg[hi].is_zero():
                continue
            fa, pa = factors_for(g, (((0, 1, 2), 0),))
            fb, pb = factors_for(G[hi], (((3, 4, 5), 0),))
            fl['oD_%s_%s' % (g, G[hi])] = outer_far3(ED_f, 6, list(range(6)), fa + fb, pa + pb, J)
            far += (1 if hi == gi else 2) * mg[gi] * mg[hi] * arb(fl['oD_%s_%s' % (g, G[hi])])
    return far, fl


# ====================================================================================== part 5: engine A in stages, and the a-engine
# (kt_c_v2_3 l.970-1130) in balls; the far parts and gB are FLOAT inputs (part 4b), printed with repr (F4) and entering as exact binary64 numbers.
# kt_cert_v1_3: engine A is cut into stages that the pieces of an item share (part 6): stage_c (D4, its conditional expectation, nD),
# tail_term (one Chernoff table each: tailX, tailB by F1, ann), stage_g (L0 remainder, nP with t^0 r0 by F3, nR0, far_out with its cross terms
# by F2, gB, the bound). The arithmetic of every stage is kt_cert_v1_1's except F1, F2, F3.
LAM_T = 0.45          # the Chernoff lambda of tailX, tailB and ann (free choice, exact binary64)


def mark(kind, label):
    """a stage line with the CPU time so far (locates the cost of each part)."""
    out('STAGE-CPU N=%d %s: %s done at cpu %.1f s' % (NN, kind, label, cpu()))


def eye3():
    return arb_mat(3, 3, [1 if i == j else 0 for i in range(3) for j in range(3)])


def residual_P(ex, t):
    """F3: P = r0 + t r1 + t^2 r2 + t^3 r3 for every kind (the free binary64 m0 leave r0 != 0, and (C1) needs the residual of the
    chosen m_g in full)."""
    return padd(ex['r0'], pscale(ex['r1'], t), pscale(ex['r2'], t * t), pscale(ex['r3'], t ** 3))


def stage_c(kind, J):
    """engine A's derivative part: D4 (the order-4 majorant of L1 F on the near region), its conditional expectation given sigma, and
    nD = (t^4/24) detf (n2 E[E_t[D4|s]^2])^{1/2}. Returns {nD, deg2, tot, nterms, cpu}."""
    t = arb(1) / J
    c0 = cpu()
    hL = {k: hk(k, [(v, a_e) for v in XD], bondsL, cf_rad) for k in range(1, 5)}
    D4 = Dbar(4, hL, source_pis(kind, t))
    ex4 = D4.exponents()
    assert ex4[:, 3:6].sum() == 0
    deg2 = int(ex4[:, 6:].sum(axis=1).max())
    qdeg = int(ex4[:, 9:].sum(axis=1).max())
    tot = int(ex4.sum(axis=1).max())
    mark(kind, 'D4 (%d terms)' % len(D4.codes))
    Amat = eye3() + tri_laplacian()
    Ainv = Amat.inv()
    W2 = arb_mat(3, 6)
    for r in range(3):
        W2[r, r] = 1
    for p_, (r, s) in enumerate(PAIRS):
        W2[r, 3 + p_] = 1
        W2[s, 3 + p_] = -1
    At = Amat - eye3() * (2 * c_e * t)
    assert surely_pd(At, 'A - 2 c_e t I')
    Ati = At.inv()
    detf = ((Amat.det() / At.det()).log() * nn / 2).exp()
    Delta = Ati - Ainv
    cmT = ae.CondMomA(Ati, Ati, W2, nn, deg2, groups=[0, 0, 0, 1, 1, 1], caps={1: max(qdeg, 1)})
    mark(kind, 'CondMomA (Dc %d)' % deg2)
    cgT = ae.CondGA(cmT, tot)
    ED = cgT.out.to_dict(cgT.condE(D4.to_dict()))
    mark(kind, 'conditional expectation of D4 (%d terms)' % len(ED))
    ext = arb_mat(6, 6)
    for i in range(3):
        for j in range(3):
            ext[i, j] = Delta[i, j]
    G2, n2 = tilted_cov_a(LD, BD, [c_m * t] * 6, extra=ext)
    w2 = ae.WishartA(sub_mat(G2, [0, 1, 2]), nn, 2 * max(sum(e) for e in ED))
    nD = (t ** 4 / 24) * detf * nsqrt(n2 * w2.E2(ED, ED))
    mark(kind, 'nD')
    return dict(nD=nD, deg2=deg2, tot=tot, nterms=len(D4.codes), cpu=cpu() - c0)


def tail_poly(T3, t):
    """the explicit series T3 at t as a polynomial in the ten joint forms, with its degree and its Q degree."""
    T10 = to10(padd(*[pscale(T3.c[k], t ** k) for k in range(KX + 1)]), NVX)
    return T10, max(sum(e) for e in T10), max(sum(e[6:]) for e in T10)


def ann_poly(kind, t):
    """pi0'' (the annulus majorant of L1 F) in the ten joint forms, with its degree and its Q degree."""
    if kind == 'h':
        pi0pp = pi_h(0, a_pp, a_pp, t, cf_rad)
    elif kind in ('h1', 'h3'):
        pi0pp = pi_hb(0, a_pp, a_pp, t, cf_rad, {'h1': 1, 'h3': 3}[kind])
    else:
        pi0pp = pi_state(0, XD, QD, a_pp, t, cf_rad, {'e1': 1, 'e3': 3}[kind])
    P0d = to10(pi0pp.to_dict(), NV12)
    return P0d, max(sum(e) for e in P0d), max(sum(e[6:]) for e in P0d)


def kappa_B():
    """kappa = 2 (1 - cos delta) - a^2/(4 (1 - a)), a = max(a_m, a_e): a bad bond r inside Omega'' has Q_rr'' > J kappa (vacrig11f l.350)."""
    amax = max(a_m, a_e)
    kap = 2 * (1 - DELTA.cos()) - arb(amax) ** 2 / (4 * (1 - arb(amax)))
    assert kap > 0
    return kap


def tail_term(fam, idx, kind, J, poly):
    """one Chernoff table of the inner tails in balls, e^{-lam J c} N E[F^2] under the tilt (N E[.] relative to the untilted joint Gaussian):
    fam 'X': F = T (the explicit series), tilt lam X''_idx on the base rates (c_m t on the six outer vertices), c = a_e (as kt_cert_v1_1);
    fam 'B' (F1): F = T, tilt lam Q_rr'' = lam |x_r - x''_r|^2, r = idx (the extra form lam (e_r - e_{6+r})(e_r - e_{6+r})^T),
        on the base rates, c = kappa: on the bad set B_r of bond r inside Omega'', Q_rr'' > J kappa, so E[T^2 1_{B_r}] <= e^{-lam J kappa} N_r E_r[T^2];
    fam 'A': F = pi0'', tilt lam X''_idx on the annulus rates (c_m t outer, 2 c_pp t inner), c = a_e (as kt_cert_v1_1).
    Every tilt passes surely_pd (C-TILT (b)); the item stops otherwise."""
    t = arb(1) / J
    P, dP, qP = poly
    lam = arb(LAM_T)
    rates = [c_m * t] * 6 + ([2 * c_pp * t] * 3 if fam == 'A' else [arb(0)] * 3)
    extra = None
    if fam in ('X', 'A'):
        rates[6 + idx] = rates[6 + idx] + lam
        cexp = arb(a_e)
    else:
        extra = arb_mat(9, 9)
        extra[idx, idx] = lam
        extra[6 + idx, 6 + idx] = lam
        extra[idx, 6 + idx] = -lam
        extra[6 + idx, idx] = -lam
        cexp = kappa_B()
    am9, N9, _, Gam = joint_moments_a(rates, 2 * dP, max(2 * qP, 1), extra=extra, label='tilt %s%d' % (fam, idx))
    if am9 is None:
        raise ValueError('the Chernoff tilt %s%d is not certainly positive definite (kind %s)' % (fam, idx, kind))
    term = (-lam * J * cexp).exp() * N9 * am9.E2(P, P)
    mark(kind, 'tail table %s%d (degree %d; %d rank-deficient subsets as exact zeros)' % (fam, idx, 2 * dP, am9.zeroed))
    c_sing(am9, Gam, max(2 * qP, 1), '%s %s%d' % (kind, fam, idx))
    if not PLANTED[0]:
        plant_sing(Gam, max(2 * qP, 1))
        PLANTED[0] = True
    return term


def stage_g(kind, J, ex, cres, tails, gBb):
    """engine A's last stage: the L0 remainder, nP (F3), nR0, the tails from their nine tables, far_out (F2), gB, and
    bound = (near^2 + far_out)^{1/2} + gB >= ||K^{1/2} |f_kind| ||/(lambda_h main_D^{1/2}) (ADD2 sect. 6). Returns (bound, parts)."""
    t = arb(1) / J
    G, m = ex['G'], ex['m']
    tm = {}
    c0 = cpu()
    P = residual_P(ex, t)
    G1, n1 = tilted_cov_a(LD, BD, [c_m * t] * 6)
    R0, h0 = l0_remainder(G, m, t)
    mark(kind, 'L0 remainder (%d terms)' % len(R0.codes))
    R0g = ae.sigma_to_g({e[:6]: c for e, c in R0.to_dict().items()})
    Pg = ae.sigma_to_g(P)
    w1 = ae.WishartA(sub_mat(G1, [0, 1, 2]), nn, 2 * max([sum(e) for e in Pg] + [sum(e) for e in R0g]))
    nP = nsqrt(n1 * w1.E2(Pg, Pg))
    nR0 = nsqrt(n1 * w1.E2(R0g, R0g))
    tm['wish'] = cpu() - c0
    mark(kind, 'nP, nR0')
    c0 = cpu()
    tailX, tailB, ann = (nsqrt(tails[(f, 0)] + tails[(f, 1)] + tails[(f, 2)]) for f in ('X', 'B', 'A'))
    near = nP + cres['nD'] + nR0 + tailX + tailB + ann
    gB = supF_a(kind, J) * gBb                                               # FLOAT factor gBb
    far_out, fl = far_mixed(kind, G, m, t, J)                                # FLOAT parts, formed in arb
    tm['far'] = cpu() - c0
    mark(kind, 'far (FLOAT parts with the cross terms)')
    bound = (near * near + far_out).sqrt() + gB
    parts = dict(nP=nP, nD=cres['nD'], nR0=nR0, tailX=tailX, tailB=tailB, ann=ann, near=near, gB=gB, far=far_out, fl=fl, deg2=cres['deg2'],
                 tot=cres['tot'], nterms=cres['nterms'], tm=tm)
    return bound, parts


def a_engine(J, ex):
    """bound on ||K^{1/2} f_a||/main_D^{1/2}, f_a = E0 (xi_a+ p0 - sum_g m_g(t) p_g), in balls (kt_c_v2_3 l.1085-1128), with F3 (t^0 r0 in P)
    and F2 (far_out with its cross terms)."""
    t = arb(1) / J
    G, m = ex['G'], ex['m']
    tm = {}
    c0 = cpu()
    P = residual_P(ex, t)
    G1, n1 = tilted_cov_a(LD, BD, [c_m * t] * 6)
    R0, h0 = l0_remainder(G, m, t)
    xd = xibar(XS, QS, a_m, t, 4, cf_rad)
    xa = [xd[0][l].add(xd[1][l]).scale(arb(1) / 2) for l in range(5)]
    pis_a = []
    for j in range(5):
        acc = ae.NPolyA(NV12, BB)
        for l in range(j + 1):
            acc = acc.add(xa[l].mul(pi_vac(j - l, XS, QS, a_m, t, cf_rad)).scale(math.comb(j, l)))
        pis_a.append(acc)
    Da = Dbar(4, h0, pis_a)
    Ra = Da.scale(t ** 4 / 24).add(R0)
    exa = Ra.exponents()
    assert exa[:, 6:].sum() == 0
    tm['D4'] = cpu() - c0
    mark('a', 'Da (%d terms)' % len(Da.codes))
    c0 = cpu()
    Rag = ae.sigma_to_g({e[:6]: c for e, c in Ra.to_dict().items()})
    Pg = ae.sigma_to_g(P)
    w1 = ae.WishartA(sub_mat(G1, [0, 1, 2]), nn, 2 * max([sum(e) for e in Pg] + [sum(e) for e in Rag]))
    nP = nsqrt(n1 * w1.E2(Pg, Pg))
    nR = nsqrt(n1 * w1.E2(Rag, Rag))
    tm['wish'] = cpu() - c0
    mark('a', 'nP, nR')
    c0 = cpu()
    far_out, fl = far_mixed('a', G, m, t, J)                                # FLOAT parts, formed in arb
    tm['far'] = cpu() - c0
    mark('a', 'far (FLOAT parts with the cross terms)')
    near = nP + nR
    bound = (near * near + far_out).sqrt()
    return bound, dict(nP=nP, nR=nR, near=near, far=far_out, fl=fl, nterms=len(Da.codes), deg=int(exa.sum(axis=1).max()), tm=tm)


# ====================================================================================== part 6: values, checks, items, main
def vacscale_eval(J):
    """PK10's vacscale formula (kt_c_v2_3 l.1131-1146 verbatim; FLOAT, milestone M2)."""
    txt = open(os.path.join(INP, VSFILE)).read().splitlines()[0]
    keys = ['nP', 'D5', 'R0', 'tailX', 'tailB', 'ann', 'far', 'gB', 'Z2min', 'Rtr', 'a_e']
    vals = {}
    for k in keys:
        mt = re.search(r'\b%s ([0-9.e+-]+)' % re.escape(k), txt)
        vals[k] = float(mt.group(1))
    s = 150.0 / J
    dec = math.exp(-0.3 * vals['a_e'] * (J - 150) / 2)
    near = vals['nP'] * s ** 2 + (vals['D5'] + vals['R0']) * s ** 5 + (vals['tailX'] + vals['ann']) * dec + vals['tailB']
    g = vals['gB'] * (J / 150.0) * math.exp(-0.95 * (1 - math.cos(math.radians(40))) * (J - 150) / 2)
    eps = (math.sqrt(near ** 2 + vals['far']) + g) / math.sqrt(vals['Z2min'])
    gap = vals['Rtr'] - 1 + eps
    return eps, eps / (1 - gap)


def kts9b_entries():
    """kt_c_v2_3.kts9b_entries: the J = 170 G entries of kt_s9b_v1 (a_k and remainders; FLOAT, milestone M3)."""
    txt = open(os.path.join(SRC, 'out_kt_s9b_v1_n%d.out' % NN)).read().splitlines()
    E = {}
    for ln in txt:
        mt = re.match(r'ENTRY N=%d J=170 (\S+) ak=\[([^\]]*)\] rem=(\S+) tail=(\S+) ann=(\S+) far=(\S+) r=' % NN, ln)
        if mt:
            E[mt.group(1)] = ([float(x) for x in mt.group(2).split(',')], sum(float(mt.group(k)) for k in (3, 4, 5, 6)))
    return E


def engine_value(kind, J, bnd):
    """R_b = bound/(lambda~_0 Z_b^{1/2}) (b = e1, e3); A_h, A_a, and the hook's R^xi_b = bound/Z_b^{1/2}, in balls. lambda~_0's eps_r (M2) and
    Z (M3) are FLOAT inputs, returned for the repr prints (F4). Returns (value, eps_r, (a_k, remainder), Z)."""
    eps = vacscale_eval(J)[0]
    mh = 1 + arb(R3['m1']) / J + arb(R3['m2']) / J ** 2 + arb(R3['m3']) / J ** 3
    lt0 = (1 - arb(eps)) * mh
    ak, r = kts9b_entries()[{'e1': 'G,1,1', 'e3': 'G,3,3', 'h': 'G,0,0', 'h1': 'G,1,1', 'h3': 'G,3,3', 'a': 'G,0,0'}[kind]]
    Z = sum((arb(a) * (arb(1) / J) ** k for k, a in enumerate(ak)), arb(0)) - arb(r)
    assert Z > 0
    val = bnd / (lt0 * Z.sqrt()) if kind in ('e1', 'e3') else bnd / Z.sqrt()
    return val, eps, (ak, r), Z


def bstr(x):
    """a ball as 'mid +- rad (rel r)'."""
    mid, rad = float(x.mid()), float(x.rad())
    return '%.9e +- %.1e (rel %.1e)' % (mid, rad, rad / abs(mid) if mid != 0 else float('inf'))


def dec_up(x):
    """a 10-digit decimal >= every point of the ball x (checked in arb; F5's upward rounding, done at the source)."""
    s = '%.9e' % (up_float(x) * (1 + 2e-9))
    assert arb(s) >= x
    return s


def v23_line(kind):
    """kt_c_v2_3's printed engine line for this item's kind and N (pk01's frozen outputs)."""
    name = 'out_kt_c_v2_3_%sn%d.out' % (kind, NN)
    txt = open(os.path.join(SRC, name)).read().splitlines()
    pat = r'AENGINE N=%d J=300 a: ' % NN if kind == 'a' else r'ENGINE N=%d J=300 %s: ' % (NN, kind)
    lines = [ln for ln in txt if ln.startswith(pat)]
    assert len(lines) == 1, (name, len(lines))
    return name, lines[0]


def printed(line, key):
    mt = re.search(r'\b%s ([0-9.]+e[+-][0-9]+)' % re.escape(key), line)
    return None if mt is None else mt.group(1)


def rep_check(kind, bnd, parts, tag, fails, scale_nP=1.0, quiet=False):
    """C-REP / C-HOOK0: the ball midpoints against kt_c_v2_3's printed values. Each part printed with d digits after the point to half a unit
    of its last printed digit (plus 1e-9 relative); tailB is not compared (F1 changed its form; printed beside v2_3's). The bound to 1e-6
    relative against v2_3's bound with v2_3's far and tailB replaced by this engine's (F2, F1; S1 of the REVIEW_kt_cert_v1_3):
    near_v23 = ((B - gB)^2 - far)^{1/2}, B_ref = ((near_v23 - tailB_v23 + tailB_new)^2 + far_new)^{1/2} + gB_new, from v2_3's printed B, gB,
    far, tailB (their rounding moves B_ref by about 7e-8 relative). Returns True if every key agrees."""
    name, line = v23_line(kind)
    keys = ['nP', 'nR'] if kind == 'a' else ['nP', 'nD', 'nR0', 'tailX', 'ann']
    vals = dict(parts)
    vals['nP'] = parts['nP'] * scale_nP
    res, ok = [], True
    sb, sf = float(printed(line, 'bound')), float(printed(line, 'far'))
    sg = 0.0 if kind == 'a' else float(printed(line, 'gB'))
    gnew = 0.0 if kind == 'a' else float(parts['gB'].mid())
    tb_old = 0.0 if kind == 'a' else float(printed(line, 'tailB'))
    tb_new = 0.0 if kind == 'a' else float(parts['tailB'].mid())
    near_v23 = math.sqrt((sb - sg) ** 2 - sf)
    bref = math.sqrt((near_v23 - tb_old + tb_new) ** 2 + float(parts['far'].mid())) + gnew
    devb = abs(float(bnd.mid()) / bref - 1)
    okb = devb <= 1e-6
    ok &= okb
    res.append('bound %.9e vs %.9e (v2_3 %s with far %s -> %.3e and tailB %s -> %.3e; rel %.1e)' % (
        float(bnd.mid()), bref, printed(line, 'bound'), printed(line, 'far'), float(parts['far'].mid()),
        '0' if kind == 'a' else printed(line, 'tailB'), tb_new, devb))
    for k in keys:
        s = printed(line, k)
        v = float(vals[k].mid())
        d = len(s.split('e')[0].split('.')[1]) if '.' in s.split('e')[0] else 0
        tol = 0.5 * 10.0 ** (int(s.split('e')[1]) - d) + 1e-9 * abs(float(s))
        good = abs(v - float(s)) <= tol
        ok &= good
        res.append('%s %.4e vs %s%s' % (k, v, s, '' if good else ' (OFF)'))
    if kind != 'a':
        res.append('tailB %.4e (F1 form; v2_3 printed %s, not compared)' % (fup(parts['tailB']), printed(line, 'tailB')))
    if not quiet:
        out('%s N=%d %s against %s: %s -> %s' % (tag, NN, kind, name, '; '.join(res), 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('%s %s' % (tag, kind))
    return ok


def rad_check(bnd, parts, fails):
    worst = 0.0
    for k, x in [('bound', bnd)] + [(k, parts[k]) for k in ('nP', 'nD', 'nR0', 'nR') if k in parts]:
        mid = abs(float(x.mid()))
        if mid > 0:
            worst = max(worst, float(x.rad()) / mid)
    ok = worst <= 1e-12
    out('C-RAD N=%d: worst relative radius over the bound and the main parts %.2e -> %s' % (NN, worst, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-RAD')


def series_T3(kind):
    """the explicit series T3 of explicit_part (before the conditional expectation), recomputed where the tails need it; None for kind a."""
    if kind == 'a':
        return None
    HL = zero()
    for r in range(3):
        HL = HL + meas(XD[r])
    for p, (r, s) in enumerate(PAIRS):
        HL = HL + anh(XD[r], XD[s], TRI[p])
    for r in range(3):
        HL = HL + anh(XS[r], XD[r], 1)
    HL = HL + anh(XS[0], XS[1], 1) + anh(XS[1], XS[2], 1)
    EL = HL.exp()
    xiD = xis(XD, QD)
    xih = xi_pair(XS[1], XD[1], QH)
    b = STATE_OF[kind]
    pD = vac_poly(xiD) if b == 'psi' else state_poly(xiD, {'e1': 1, 'e3': 3}[b])
    return EL * xih * pD if kind in HOOK else EL * pD


# ---------------------------------------------------------------------------- hand-offs between the pieces of an item
# A piece's hand-off: hand_kt_cert_v1_5_<piece>.<suffix>.txt in the own folder, created once (exclusive create), under 2 MB: a HEAD line (this
# script's sha256, the piece, kind, N, precision), the rows, and an END line with the sha256 of the body. The producing piece prints the file's
# sha256 in its record (out_kt_cert_v1_5_<piece>.<suffix>.out, line HANDOFF). A reading piece takes the sha256 from that record, whose VERDICT
# line must read VALID, and checks (1) the file's sha256 against it, (2) the body checksum, (3) the header. PLANT-HANDOFF (g pieces): three
# tampered copies, in memory, each caught by its own check. Balls are written by arb's str with the radius (80 digits), whose parse contains
# the ball; the m_g as repr floats (exact).
HANDOFF_MAX = 2 * 1024 * 1024


def handoff_path(piece):
    return os.path.join(OWN, 'hand_kt_cert_v1_5_%s.%s.txt' % (piece, SUFFIX))


def record_path(piece):
    return os.path.join(OWN, 'out_kt_cert_v1_5_%s.%s.out' % (piece, SUFFIX))


def write_handoff(piece, rows):
    path = handoff_path(piece)
    assert os.path.dirname(os.path.realpath(path)) == os.path.realpath(OWN) and not os.path.exists(path), path
    body = '\n'.join(['HEAD kt_cert_v1_5 %s piece %s kind %s N %d prec %d' % (SELF_SHA, piece, KIND, NN, ctx.prec)] + rows) + '\n'
    data = (body + 'END %s\n' % hashlib.sha256(body.encode()).hexdigest()).encode()
    assert len(data) < HANDOFF_MAX, len(data)
    with open(path, 'xb') as fh:
        fh.write(data)
    sh = hashlib.sha256(data).hexdigest()
    out('HANDOFF N=%d %s %s: %s sha256 %s (%d bytes, %d rows; cpu %.1f s)' % (NN, KIND, piece, os.path.basename(path), sh, len(data), len(rows),
                                                                             cpu()))
    return sh


def verify_handoff_bytes(data, want, piece):
    """the three checks; returns the body rows after the HEAD line, raises ValueError naming the first check that fails."""
    if hashlib.sha256(data).hexdigest() != want:
        raise ValueError('sha256 differs from the record')
    txt = data.decode()
    body, endline = txt.rsplit('END ', 1)
    if hashlib.sha256(body.encode()).hexdigest() != endline.strip():
        raise ValueError('body checksum')
    rows = body.splitlines()
    head = rows[0].split()
    if not (len(head) == 11 and head[0] == 'HEAD' and head[1] == 'kt_cert_v1_5' and head[2] == SELF_SHA and head[4] == piece and
            head[6] == KIND and head[8] == str(NN) and head[10] == str(ctx.prec)):
        raise ValueError('header')
    return rows[1:]


def producer_sha(piece):
    """the hand-off's sha256 from its producing run's record, whose VERDICT line must read VALID."""
    with open(record_path(piece)) as fh:
        rec = fh.read().splitlines()
    hl = [ln for ln in rec if ln.startswith('HANDOFF N=%d %s %s: ' % (NN, KIND, piece))]
    vl = [ln for ln in rec if ln.startswith('VERDICT ')]
    if len(hl) != 1 or vl != ['VERDICT VALID']:
        raise ValueError('record of piece %s: %d HANDOFF lines, VERDICT lines %r' % (piece, len(hl), vl))
    return hl[0].split(' sha256 ')[1].split()[0]


def read_handoff(piece):
    want = producer_sha(piece)
    with open(handoff_path(piece), 'rb') as fh:
        data = fh.read()
    rows = verify_handoff_bytes(data, want, piece)
    out('HANDOFF-READ N=%d %s %s: %s sha256 %s equals its record (%s); body checksum and header PASS' % (
        NN, KIND, piece, os.path.basename(handoff_path(piece)), want, os.path.basename(record_path(piece))))
    return rows, data, want


def plant_handoff(piece, data, want, fires):
    """PLANT-HANDOFF: three tampered copies of the hand-off, in memory, must each fail verify_handoff_bytes at its own check:
    (a) the last digit of the first row changed, END line kept, the sha256 taken from the tampered bytes (only the body checksum can catch it);
    (b) the same change with a recomputed END line, against the record's sha256 (only the sha256 check can catch it);
    (c) the header's kind changed, END line recomputed, the sha256 taken from the tampered bytes (only the header check can catch it)."""
    txt = data.decode()
    body, endline = txt.rsplit('END ', 1)
    rows = body.splitlines()
    pos = max(p for p, ch in enumerate(rows[1]) if ch.isdigit())
    row1 = rows[1][:pos] + str((int(rows[1][pos]) + 1) % 10) + rows[1][pos + 1:]
    body_t = '\n'.join([rows[0], row1] + rows[2:]) + '\n'
    other = 'e3' if KIND != 'e3' else 'e1'
    body_h = '\n'.join([rows[0].replace(' kind %s ' % KIND, ' kind %s ' % other)] + rows[1:]) + '\n'

    def sealed(b):
        return (b + 'END %s\n' % hashlib.sha256(b.encode()).hexdigest()).encode()
    da = (body_t + 'END ' + endline).encode()
    db, dc = sealed(body_t), sealed(body_h)
    cases = (('a', da, hashlib.sha256(da).hexdigest(), 'body checksum'), ('b', db, want, 'sha256 differs from the record'),
             ('c', dc, hashlib.sha256(dc).hexdigest(), 'header'))
    res, fired = [], True
    for tag, d, w, expect in cases:
        try:
            verify_handoff_bytes(d, w, piece)
            res.append('(%s) accepted' % tag)
            fired = False
        except ValueError as e:
            res.append('(%s) rejected: %s' % (tag, e))
            fired = fired and str(e) == expect
    out('PLANT-HANDOFF N=%d %s %s: %s -> %s' % (NN, KIND, piece, '; '.join(res), 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-HANDOFF')


def parse_x(rows):
    m = [[None] * 3 for _ in range(4)]
    r = [dict() for _ in range(4)]
    for ln in rows:
        f = ln.split(' ', 8)
        if f[0] == 'M':
            m[int(f[1])][int(f[2])] = float(f[3])
        elif f[0] == 'R':
            r[int(f[1])][tuple(int(x) for x in f[2:8])] = arb(f[8])
        else:
            raise ValueError('x row %r' % ln[:40])
    assert all(x is not None for row in m for x in row)
    return dict(G=('psi', 'e1', 'e3'), m=m, r0=r[0], r1=r[1], r2=r[2], r3=r[3])


def resolve_c(J):
    """stage_c's results from piece c's hand-off when piece c was run (its record exists), else computed in-line."""
    if os.path.exists(record_path('c')):
        rows = read_handoff('c')[0]
        got = {}
        for ln in rows:
            f = ln.split(' ', 1)
            got[f[0]] = f[1]
        ints = [int(x) for x in got['INT'].split()]
        return dict(nD=arb(got['NDB']), deg2=ints[0], tot=ints[1], nterms=ints[2], src='hand-off c')
    STAGE[0] = 'stage_c %s (in-line)' % KIND
    cres = stage_c(KIND, J)
    cres['src'] = 'in-line'
    return cres


def resolve_tails(J):
    """the nine tail terms: for each family F, from piece tF's hand-off, or from tF0, tF1, tF2's, or (no record) computed in-line."""
    t = arb(1) / J
    tails, src, polys, cache = {}, {}, {}, {}
    for fam in ('X', 'B', 'A'):
        whole = os.path.exists(record_path('t' + fam))
        single = [os.path.exists(record_path('t%s%d' % (fam, i))) for i in range(3)]
        if whole and any(single):
            raise ValueError('records of both t%s and a t%s<i> piece exist' % (fam, fam))
        for i in range(3):
            pc = ('t' + fam) if whole else (('t%s%d' % (fam, i)) if single[i] else None)
            if pc is None:
                if fam not in polys:
                    STAGE[0] = 'tail polynomial %s (in-line)' % fam
                    if fam == 'A':
                        polys[fam] = ann_poly(KIND, t)
                    else:
                        if 'T' not in polys:
                            polys['T'] = tail_poly(series_T3(KIND), t)
                        polys[fam] = polys['T']
                STAGE[0] = 'tail table %s%d (in-line)' % (fam, i)
                tails[(fam, i)] = tail_term(fam, i, KIND, J, polys[fam])
                src[(fam, i)] = 'in-line'
                continue
            if pc not in cache:
                cache[pc] = read_handoff(pc)[0]
            hit = [ln for ln in cache[pc] if ln.startswith('TAIL %s %d ' % (fam, i))]
            if len(hit) != 1:
                raise ValueError('hand-off %s has %d rows for tail %s%d' % (pc, len(hit), fam, i))
            tails[(fam, i)] = arb(hit[0].split(' ', 3)[3])
            src[(fam, i)] = 'hand-off ' + pc
    return tails, src


def run_piece(fails, fires):
    J = J_MAIN
    t0 = cpu()
    if PIECE == 'x':
        STAGE[0] = 'explicit %s' % KIND
        ex = explicit_part(KIND, fails, fires)
        rows = ['M %d %d %r' % (j, i, ex['m'][j][i]) for j in range(4) for i in range(3)]
        for j in range(4):
            for e, c in sorted(ex['r%d' % j].items()):
                rows.append('R %d %s %s' % (j, ' '.join(str(int(x)) for x in e), c.str(80, radius=True)))
        write_handoff('x', rows)
        return None
    if PIECE == 'c':
        STAGE[0] = 'stage_c %s' % KIND
        cres = stage_c(KIND, J)
        out('STAGE-C N=%d %s: nD %s | D4 %d terms, deg2 %d, tot %d (cpu %.1f s)' % (NN, KIND, bstr(cres['nD']), cres['nterms'], cres['deg2'],
                                                                                    cres['tot'], cres['cpu']))
        write_handoff('c', ['NDB %s' % cres['nD'].str(80, radius=True), 'INT %d %d %d' % (cres['deg2'], cres['tot'], cres['nterms'])])
        return None
    if PIECE[0] == 't':
        fam = PIECE[1]
        idxs = (int(PIECE[2]),) if len(PIECE) == 3 else (0, 1, 2)
        t = arb(1) / J
        STAGE[0] = 'tail polynomial %s' % fam
        poly = tail_poly(series_T3(KIND), t) if fam in ('X', 'B') else ann_poly(KIND, t)
        mark(KIND, 'tail polynomial %s (%d terms, degree %d, Q degree %d)' % (fam, len(poly[0]), poly[1], poly[2]))
        rows = []
        for i in idxs:
            STAGE[0] = 'tail table %s%d' % (fam, i)
            term = tail_term(fam, i, KIND, J, poly)
            out('TAIL N=%d %s %s%d: e^{-lam J c} N E[F^2] = %s' % (NN, KIND, fam, i, bstr(term)))
            rows.append('TAIL %s %d %s' % (fam, i, term.str(80, radius=True)))
        write_handoff(PIECE, rows)
        return None
    STAGE[0] = 'read x'
    rows, data, want = read_handoff('x')
    ex = parse_x(rows)
    STAGE[0] = 'PLANT-HANDOFF'
    plant_handoff('x', data, want, fires)
    if KIND == 'a':
        STAGE[0] = 'a-engine'
        bnd, parts = a_engine(J, ex)
        gBb = None
    else:
        cres = resolve_c(J)
        tails, tsrc = resolve_tails(J)
        STAGE[0] = 'gB (FLOAT)'
        gBb = gB_base(J)
        STAGE[0] = 'stage_g %s' % KIND
        bnd, parts = stage_g(KIND, J, ex, cres, tails, gBb)
        out('SOURCES N=%d %s: nD from %s; tails %s' % (NN, KIND, cres['src'], ', '.join('%s%d from %s' % (f, i, tsrc[(f, i)]) for f in 'XBA'
                                                                                         for i in range(3))))
    STAGE[0] = 'value'
    val, eps, (ak, rem), Z = engine_value(KIND, J, bnd)
    tm = parts['tm']
    vname = {'e1': 'R_e1', 'e3': 'R_e3', 'h': 'A_h', 'h1': 'R^xi_e1', 'h3': 'R^xi_e3', 'a': 'A_a'}[KIND]
    if KIND == 'a':
        out('AENGINE N=%d J=%d a: bound %s | nP %s | nR %s | far %s (FLOAT parts) | Da %d terms, deg %d | cpu D4 %.1f wish %.1f far %.1f '
            '(%.1f s)' % (NN, J, bstr(bnd), bstr(parts['nP']), bstr(parts['nR']), bstr(parts['far']), parts['nterms'], parts['deg'], tm['D4'],
                          tm['wish'], tm['far'], cpu() - t0))
    else:
        out('ENGINE N=%d J=%d %s: bound %s | nP %s | nD %s | nR0 %s | tailX %.3e tailB %.3e ann %.3e | gB %.3e | far %s (FLOAT parts) | '
            'D4 %d terms, deg2 %d, tot %d | cpu wish %.1f far %.1f (%.1f s)' % (
                NN, J, KIND, bstr(bnd), bstr(parts['nP']), bstr(parts['nD']), bstr(parts['nR0']), fup(parts['tailX']), fup(parts['tailB']),
                fup(parts['ann']), fup(parts['gB']), bstr(parts['far']), parts['nterms'], parts['deg2'], parts['tot'], tm['wish'], tm['far'],
                cpu() - t0))
    out('FLOAT-IN N=%d %s (repr; F4, for M2/M3): %s%s | eps_r %r%s | Z: a_k [%s] remainder %r -> Z %s' % (
        NN, KIND, ' | '.join('%s %r' % (k, v) for k, v in parts['fl'].items()), '' if gBb is None else ' | gBb %r' % gBb, eps,
        '' if KIND in ('e1', 'e3') else ' (not used by this kind)', ', '.join(repr(a) for a in ak), rem, bstr(Z)))
    out('VALUE N=%d J=%d %s: %s <= %s (ball %s; rounded up; eps_r, s and Z FLOAT)' % (NN, J, KIND, vname, dec_up(val), bstr(val)))
    if KIND in ('e1', 'e3'):
        out('F2A N=%d %s: R_%s^{|f|} <= %s, the same ball as R_%s (SPEC ADD2 v1 sect. 6; check C-F holds with equality)' % (
            NN, KIND, KIND, dec_up(val), KIND))
    if KIND in HOOK:
        out('C-BAD-HOOK N=%d %s (SPEC ADD2 v1 sect. 8; W2 weights them by X): gB %.3e, far_out %.3e (FLOAT parts, (2J)^2 on G4, 2J on G3), '
            'tailX %.3e tailB %.3e ann %.3e' % (NN, KIND, fup(parts['gB']), fup(parts['far']), fup(parts['tailX']), fup(parts['tailB']),
                                               fup(parts['ann'])))
    if not (val > 0 and val.is_finite()):
        fails.append('K-FIN %s' % KIND)
    return bnd, parts, val


def c_tilt_a(fails, fires):
    """C-TILT (a): domination of the tilt rates and the annulus radius, positivity of the Chernoff lambdas; PLANT-TILT."""
    def rate_ok(c, a):
        return arb(c) >= -(1 - arb(a)).log() / (2 * arb(a))
    rates = (('c_m', c_m, a_m), ('c_e', c_e, a_e), ('c_pp', c_pp, a_pp))
    okr = all(rate_ok(c, a) for _, c, a in rates)
    app = (arb(RHO_M).asin() + DELTA).sin() ** 2
    oka = arb(a_pp) >= app
    lams = (LAM_T, 0.5)
    okl = all(x > 0 for x in lams)
    ok = okr and oka and okl
    out('C-TILT (a) N=%d: %s; a_pp %.17g >= sin^2(asin rho_m + delta) = %s; Chernoff lambdas %s > 0 -> %s' % (
        NN, ', '.join('%s %.17g >= -log(1 - a)/(2a) = %s (a %.17g)' % (nm, c, (-(1 - arb(a)).log() / (2 * arb(a))).str(12, radius=False), a)
                      for nm, c, a in rates), a_pp, app.str(12, radius=False), ' '.join('%g' % x for x in lams), 'PASS' if ok else 'FAIL'))
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


def main():
    fails, fires = [], []
    complete = False
    try:
        c_tilt_a(fails, fires)
        res = run_piece(fails, fires)
        if PIECE == 'g':
            bnd, parts, val = res
            if SMOKE:
                rep_check(KIND, bnd, parts, 'C-REP' if SMOKE == 'smoke' else 'C-HOOK0', fails)
            elif KIND in ('e1', 'e3', 'h', 'a'):
                rep_check(KIND, bnd, parts, 'C-REP', fails)
            rad_check(bnd, parts, fails)
            if KIND != 'a':
                lr = parts['fl']['logR']
                okr = abs(lr) <= 1e-10
                out('C-R N=%d %s: |log R| = %.2e <= 1e-10 (R = main_N^2/(main_D main_4) = 1 by the matrix-tree theorem; S2 of the REVIEW_'
                    'kt_cert_v1_3) -> %s' % (NN, KIND, abs(lr), 'PASS' if okr else 'FAIL'))
                if not okr:
                    fails.append('C-R')
            if SMOKE == 'hsmoke':
                okp = rep_check(KIND, bnd, parts, 'PLANT-HOOK0', [], scale_nP=1.01, quiet=True)
                out('PLANT-HOOK0 N=%d: nP of kind h with the xi factor scaled by 1.01 (the explicit part is linear in the source) against kt_c_v2_3: '
                    '%s -> %s' % (NN, 'agrees' if okp else 'disagrees', 'DOES NOT FIRE' if okp else 'FIRES'))
                if okp:
                    fires.append('PLANT-HOOK0')
        if PIECE != 'x':
            c_tilt_b(fails)
        fails += SING_FAILS
        fires += SING_FIRES
        complete = True
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


if __name__ == '__main__':
    sys.exit(main())
