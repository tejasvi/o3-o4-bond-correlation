#!/usr/bin/env python3
"""px08_trbhcert_v1_2.py -- pk08, SH4 of HZ_PLAN_v1_1: the certified TRB_H(r) = tr_H P_L/lambda_h^2 for the rows r in {T, M}, option (i),
for every J >= 300, in the record form of S4_U_CERTIFIED_v2 (F2): TRB_H(r, t) <= U3_p(r)(t) + R_cert(r). U3_p is an exact cubic in t with
certified ball coefficients, which the consumer evaluates at its own t; R_cert is the certified remainder at t = 1/300, and by the REASON
lines it bounds every t <= 1/300. Design S4_TRBH_DESIGN_v1_1 (70962463; the review DELTA b62a082d: SOUND); dry runs px08_trbhscan_v2 (ac843025;
outputs b818f039 and 8a24ce8e).
Why option (i): the dry run's VERDICT line names (iii); that is the script's frozen rule. Option (i) is chosen under the rule from
14:12Z, set before the result: (iii) needs 1.2 x remainder <= 0.8 TOL, and N4 row T sits at 96.1%.
Chain (design §3, option (i); delta = 0.12 for both groups, eps = 0.65; B_Y = B_{Y_M} + B_{Y_T}, Y_M = X4, Y_T = YT_X (X1 + X3) - c with
YT_X = 1/2 + kappa_T (a1 + a3), kappa_T = 1/(2 (sqrt(1 - a1) + sqrt(1 - a3))^2)):
  U3_p(r)(t) = sum_{k<=3} t^k d_k(r), d_k = I[f_k], f_k = sum_{i+j=k} p_i E_j (E_0 = 1; E_1, E_2, E_3 as twrig6z l.32), exact Gaussian
    moments: group P, the plain Q with the 11th form c = phi1.phi3, an 11-form table to degree 7;
  R_cross = sum_{i+j>=4; i,j<=3} t^(i+j) (I[p_i^2] I[E_j^2])^(1/2);  R_ins = t^4 sum_{j<=3} t^j (I[pbar_4^2] I[E_j^2])^(1/2);
  R_main = ((N-1)/2) (R_E + rho4) + alpha1 (R_E^(delta) + rho4^(delta)), alpha1 = 1/(e delta) for row T, 1/(2 e delta) for row M. Here
    R_E + rho4 is U's certified PREF2_RE + PREF2_RHO4, and R_E^(delta), rho4^(delta) are the certified U chain's readings (px08_m2bb4
    l.1516-1529 and px08_m2bc4 l.1655-1666) on the measure e^{delta Y} nu: group D has the matrix Q - 2 delta B_Y and group T the matrix
    Q - 2 T(1/300, 0.65) - 2 delta B_Y, so the weight enters once. This holds because |p| <= (N-1)/2 + alpha1 e^{delta Y} on
    Omega (Young; design §3; C-MAJ checks it in floats), and U's |R| <= R_E's integrand + |rho4| pointwise on Omega;
  tail^(p) = PR L2^(p) Chern^(1/2), L2^(p) = I[p_0^2]^(1/2) + sum_{1<=i+j<=3} t^(i+j) (I[p_i^4] I[E_j^4])^(1/4), with Chern U's certified
    Chernoff sum (the PIECES line of px08_px03_v4's asm); off-Omega = ((N-1)/2 + J/2) (U's M3_ANNULUS + M3_FAR + M3_EQUATOR);
  the L2 norm of E_3 and the L4 norms of E_2, E_3 by Minkowski and per-node hypercontractivity with integer powers, so that every node
    function stays analytic: E[H2^4] <= 3^12 E[H2^2]^2, E[H1^6] <= 5^12 E[H1^2]^3, E[H1^8] <= 7^16 E[H1^2]^4, E[H3^4] <= 3^16 E[H3^2]^2,
    E[H1^4 H2^4] <= 7^20 E[H1^2]^2 E[H2^2]^2, E[H1^12] <= 11^24 E[H1^2]^6 (H1, H2, H3 have Gaussian degrees 4, 6, 8); E_2^4 <= 8 H2^4
    + H1^8/2 and E_3^4 <= 27 (H3^4 + H1^4 H2^4 + H1^12/6^4) by convexity. The small-piece integrals use group D's measure, which majorizes
    the plain one since e^{delta Y} >= 1;
  I[f] = PR^2 int dmu w det(Q_g)^{-1/2} E_g[f] for the group g of f; PR = pref_arb(N).
Each integral is TW on M nodes (k = 0..M/2, evenness) plus the N = 3 reflection atom (weight 1/2), with the error 2 G/(e^{sigma M} - 1),
where G = sup |w det_g^{-1/2} E_g[f]| on Im al = sigma, by maximum modulus on the closed strip where Re det of all three group matrices is
> 0 (C-COVER). C-PROP certifies Q - 2 delta B_Y and Q - 2 T - 2 delta B_Y positive definite on al-intervals tiling [0, pi] and at the N = 3
reflection (k(2 pi - al) is similar to k(al), as in px08_trbcert_v1_1).
Uniform in J >= 300 (one REASON per piece): U3_p is an exact cubic in t (the (P) form); R_cross and R_ins are t^m (m >= 4) times J-free
integrals; R_main's first term is U's (nonincreasing in J by U's reasons), and its second is a chain whose integrands are hbar_j at
t = 1/300 (majorizing every t' <= t) on the matrices Q - 2 delta B_Y and Q - 2 T(t) - 2 delta B_Y (Loewner-decreasing in t: the t-part of
T is PSD and delta B_Y is J-free); the tail is t-powers times J-free norms times U's Chernoff sum (nonincreasing in J); the off-Omega term
is ((N-1)/2 + J/2) times U's annulus, far and equator J-bounds, nonincreasing for J >= 300 by C-FAR-H; PR is free of J; every TW error
sits inside the J = 300 enclosures; each J-bound is valid at its own Omega(J) and tilt T(1/J) (Z4).
Items: cov | nodes0..nodes8 (all three groups, at most 4 nodes each) | gP0..gP7, gD0..gD7, gT0..gT7 (the G of one group on one eighth of [0, pi]) | asm.
Copied blocks: every block between '# ==== COPY <file>:<sha8> l.<a>-<b> BEGIN ====' and '# ==== COPY END ====' equals lines a..b of that
file byte for byte (C-COPY at the asm, with PLANT-COPY).
v1_1 (after v1's n4 gP1 stopped at G_MAXEV = 10): G_MAXEV = 28, and the CPU projection still guards LIM before every
evaluation. v1's outputs are reused: the cov outputs, the node partials of both N and n4 gP0. header_ok and read_parts accept a partial
from either producer (script name, full sha256) in PRODUCERS: v1 (V1_FILE in the asm part) or this file. C-ITEMCODE (asm, with
PLANT-ITEMCODE) shows that v1 and this file are byte-identical from the line 'GPARTS = ...' to the asm part's first line, except two
lines: the output header and the G constants. G_MAXEV decides only whether a G item stops, never what a PART-DONE item prints, so v1's
partials are what this file prints for them. To keep that region byte-identical, header_ok keeps its v1 text there and is redefined in
the asm part, before main runs, and the usage text still names v1. C-FAR-H cites the source of its 1/5, and every lam
line must parse, into U's m3 families ann1..ann3 and far at v0..v5 (PLANT-FAR-FMT, PLANT-FAR-FAM). Two further checks wait for a
version that changes the evaluation code.
v1_2 (after v1_1's n4 gD0 CPU-STOP at LIM 230): the LIM ceiling rises from 240 to 360, so that the n4 D and T items
can run at LIM 350 under the exception; n3 items and the asm stay at LIM 230. LIM decides only whether an item stops, never
what a PART-DONE item prints. PRODUCERS adds this file. C-ITEMCODE compares v1 and v1_1 each with this file over the same region, and
the lines allowed to differ are named per producer: the output header and the LIM ceiling, and for v1 also the G constants.
Usage: px08_trbhcert_v1_2.py n4|n3 cov LIM | n4|n3 nodes0..nodes8 LIM SIGC | n4|n3 gP0..gT7 LIM SIGC NODE_MANIFEST | n4|n3 asm LIM SIGC MANIFEST
"""
import resource, sys, time, math, hashlib, signal, os, re
from fractions import Fraction as Fr
GPARTS = ['g%s%d' % (g, j) for g in 'PDT' for j in range(8)]
PARTS = ['cov'] + ['nodes%d' % j for j in range(9)] + GPARTS + ['asm']
NEXTRA = dict([('cov', 0)] + [('nodes%d' % j, 1) for j in range(9)])
if len(sys.argv) < 4 or sys.argv[1] not in ('n4', 'n3') or sys.argv[2] not in PARTS:
    print('usage: px08_trbhcert_v1.py n4|n3 cov LIM | n4|n3 nodes0..nodes8 LIM SIGC | n4|n3 gP0..gT7 LIM SIGC NODE_MANIFEST | n4|n3 asm LIM '
          'SIGC MANIFEST')
    sys.exit(2)
MODE, PART, LIM = sys.argv[1], sys.argv[2], int(sys.argv[3])
if not (5 <= LIM <= 360) or len(sys.argv) != 4 + NEXTRA.get(PART, 2) or (len(sys.argv) > 4 and sys.argv[4] not in ('0.5', '0.375', '0.25')):
    print('bad LIM %d or arguments' % LIM)
    sys.exit(2)
SIGC = sys.argv[4] if len(sys.argv) > 4 else '-'
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
STAGE = ['start']

# ==== COPY px08_m2bc4.py:6527d21b l.33-47 BEGIN ====
def cpu():
    return time.process_time()


def out(line):
    print(line, flush=True)


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
# ==== COPY END ====

SCR = '/mnt/g2/release/root/code/pk10/scripts'
SOURCES = {
    'twlib.py': ('/mnt/g2/release/root/code/pk10/scripts/twlib.py', '29bca6b268050911e23c4429a9cc4a26668e5ea3fa694db2926996297b8d1527'),
    'twlib2.py': ('/mnt/g2/release/root/code/pk10/scripts/twlib2.py', 'cdf024cc8ebf76d7b9ac581ffa15dea78526e0fd3694acca6c7c8dd92b11a4c4'),
    'gfmom.py': ('/mnt/g2/release/root/code/pk10/scripts/gfmom.py', 'c8cadafec97a92071b7f90d66a69b0f24fc91a7bd6ec751c1327a8218c9a2768'),
    'lapl2.py': ('/mnt/g2/release/root/code/pk10/scripts/lapl2.py', 'b28ffbdb86fab237564f2db9ea8b3e904481fba31ad79e39421de7b8a9dfe116'),
    'vacmod2.py': ('/mnt/g2/release/root/code/pk10/scripts/vacmod2.py', '533546b173af147a56e9531e26afa64cb3dbaccefd5fb7b1283f03baff06a000'),
    'pseries.py': ('/mnt/g2/release/root/code/pk10/scripts/pseries.py', '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e'),
    'g2sw_core_snapshot.py': ('/mnt/g2/release/root/code/pk10/scripts/g2sw_core_snapshot.py', 'f1b51241c54e496a8de699cc3160de3281bf98c67d019f4e92459a222d3d003a'),
    'u_record': ('/mnt/g2/release/root/code/pk08/S4_U_CERTIFIED_v2.md', 'cd2b32d72a49b37feece322e2018c071281c8e93ae9feb6b6349abe24e8a6aa4'),
    'hz_plan': ('/mnt/g2/release/root/code/pk15/HZ_PLAN_v1_1_l143.txt', '7a5027221570b708ca3bd6b5b203ae84a67a88fb3300e3ee048d56c173eee7b7'),
    'm3_asm_n4': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n4_asm.out', 'f55df5922eb0a026b2d814f2a7c665d7e1ff416a8a6a52aabbd8a90d3bcbd4df'),
    'm3_asm_n3': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n3_asm.out', 'b5c8bb3f56a63b6b1146ec5576ddf16ea5778a8be6bd8e25924c2352de617965'),
    'm3_n4_sh1': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v3_n4_sh1.out', '5503ca6eb5a38e021fad78fd17f5cede8b3e061a82dfb7a22c5b719a99ac4fd8'),
    'm3_n4_sh2a': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n4_sh2a.out', '29ac168affb6945a6f7718717347775a0c115847fcad1d64cb92945f8ac0e749'),
    'm3_n4_sh2b': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n4_sh2b.out', '979350944fdce8be0384c2af683918a8bf2e2169a06c00c9557b436c4030b424'),
    'm3_n4_sh3a': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n4_sh3a.out', 'ebb54d1e4ec2f9c79c80cdf80254d0f6615ffdc5c85ebb7733d93fc48ea82712'),
    'm3_n4_sh3b': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n4_sh3b.out', 'b05027b89673da8f671da27dd9f99d0b43e5ed8b772e6418012a115bed7e42bf'),
    'm3_n4_far': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n4_far.out', '9162ef85095624019586207a2e1281ec76509dd19b92feed19d9c23002b02211'),
    'm3_n3_sh1a': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n3_sh1a.out', '38c8a12a2417ce6cc5cef370a13612fe428cc649648e38dff393cf35f39d292e'),
    'm3_n3_sh1b': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n3_sh1b.out', 'e543d95a1c7c7b6d05a89cfa01d22cd20cf3efa4c4cd978410c661f20a880fa8'),
    'm3_n3_sh2a': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n3_sh2a.out', 'a0f91f84ac413f0e911949f4d12c1b22cb85a62c5a14cb79b785cc6efbc499d2'),
    'm3_n3_sh2b': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n3_sh2b.out', '6f97a90a0a126848e53b966c29e18788a658c84aa5279883aa2ddcac7e2afce7'),
    'm3_n3_sh3a': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n3_sh3a.out', 'c1389825ad98f6923345df29dd7f605b9153ec1d191d9f0085183bfe0210a0a9'),
    'm3_n3_sh3b': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n3_sh3b.out', '9f5e7f390f64b3b6244663c6cffdad1dd1f28a3906d7c112e89da5d8a96aa536'),
    'm3_n3_far': ('/mnt/g2/release/root/code/pk08/out/px08_px03_v4_n3_far.out', '6c5b68ec84f70673c5d8ba0bd834396054c0bbbc68b9b3aeb4268e48fafd5e51'),
    'scan_n4': ('/mnt/g2/release/root/code/pk08/out/px08_trbhscan_v2_n4_i.out', 'cda6f19d32954abb906e423685add9f0ab332878b945649f43047b257707d322'),
    'scan_n3': ('/mnt/g2/release/root/code/pk08/out/px08_trbhscan_v2_n3_i_r2.out', '6160ba66c24a4bc1712a8d7985e70d81765812d509e8a15b205529c2e3ec125a'),
}
COPY_SRC = {
    'px08_m2bc4.py': ('/mnt/g2/release/root/code/pk08/px08_m2bc4.py', '6527d21b7661a355c6534cc055f1fb8f3ae74be9256dbd6a3c65067ca6a34a17'),
    'px08_trbcert_v1_1.py': ('/mnt/g2/release/root/code/pk08/px08_trbcert_v1_1.py', '6a85137435ccbcbcc29d879adae74d7642ae44306116da924100995f9ba61453'),
}

# ==== COPY px08_m2bc4.py:6527d21b l.57-62 BEGIN ====
def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'
# ==== COPY END ====



out('px08_trbhcert_v1_2 sha256 %s ITEM=%s %s LIM=%d SIGC=%s' % (sha_file(os.path.abspath(__file__)), MODE, PART, LIM, SIGC))
_bad = ['%s %s' % (n_, sha_file(p_)) for n_, (p_, h_) in sorted(SOURCES.items()) if sha_file(p_) != h_]
_bad += ['%s %s' % (n_, sha_file(p_)) for n_, (p_, h_) in sorted(COPY_SRC.items()) if sha_file(p_) != h_]
out('C-HASH %s (%d sources)%s' % ('PASS' if not _bad else 'FAIL', len(SOURCES) + len(COPY_SRC), (': ' + '; '.join(_bad)) if _bad else ''))
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
PI = arb.pi()
J_ = 300
X6F = ['X1', 'X2', 'X3', 'X4', 'X5', 'Z']
AV_A = [arb(1) / 5, arb(1) / 5] + [arb(3) / 10] * 4      # U's radii^2 for X1..X5, Z (sp0; S4_U_CERTIFIED_v2)
AV_F = [0.2, 0.2, 0.3, 0.3, 0.3, 0.3]
T_A, T_F = arb(1) / 300, 1.0 / 300
TT = T_A                                                # t = 1/300 in T_block
EPS_A, EPS_F = arb(13) / 20, 0.65                       # group T's eps (dry run v2: eps* 0.65 for option (i))
DELTA_A, DELTA_F = arb(3) / 25, 0.12                    # the Young weight's delta, both groups
EJ_M0, SPLIT = 400, 3
HBAR_TOL, PORT_TOL, FLT_TOL, SER_TOL = 1e-12, 1e-13, 1e-9, 1e-15
KX, KY, CDMAX = 32, 4, 12
SIG_LADDER = {'0.5': 64, '0.375': 88, '0.25': 128}
SIG = float(SIGC) if SIGC != '-' else None             # 0.5, 0.375 and 0.25 are exact binary fractions
M_ = SIG_LADDER.get(SIGC)
G_E = {j: (Fr(j, 8), Fr(j + 1, 8)) for j in range(8)}  # G on the eighths of [0, pi]
G_K, G_DSUB, G_DEPTH, G_MAXEV = 4, 8, 2, 28            # 4 boxes per eighth; at most 28 evaluations per G item (with the CPU guard)
PROP_K, PROP_DEPTH, PROP_MAXEV = 32, 8, 2048
TOL_MAIN, TOL_REM = arb(1) / 1000, arb(1) / 10          # relative TW targets (caps, TARGET line): group P, the rest
CERT_MARGIN = arb(1) / 4                                # TOL(r) = (1/4) (U3_p(r)(1/300) - h_r): the consumer tolerance (dry run v2)

# ==== COPY px08_m2bc4.py:6527d21b l.92-93 BEGIN ====
class NotCert(Exception):
    pass
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.97-103 BEGIN ====
FORMS2 = ['X1', 'X2', 'X3', 'X4', 'X5', 'Z', 'aT', 'bT', 'aB', 'bB']
IX2 = {f: i for i, f in enumerate(FORMS2)}
NF = len(FORMS2)
ROOT_BONDS = ['X1', 'X2', 'X4']
PAIR_BONDS = [('X1', 'X3'), ('X2', 'X5'), ('X3', 'X4'), ('X4', 'X5'), ('X4', 'Z')]
TWISTED = [('X1', 'X3', 'aT', 'bT'), ('X2', 'X5', 'aB', 'bB')]
Z0 = tuple([0] * NF)
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.106-110 BEGIN ====
def m2(**kw):
    e = [0] * NF
    for f, p in kw.items():
        e[IX2[f]] += p
    return tuple(e)
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.113-138 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.141-176 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.179-214 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.217-235 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.238-239 BEGIN ====
def to_arb(P):
    return {e: arb(c.numerator) / c.denominator for e, c in P.items()}
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.243-347 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.351-397 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.448-533 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.639-686 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.689-738 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.741-755 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.758-760 BEGIN ====
def fixz(m, F):
    m[(0,) * F] = m.pop(Z0)
    return m
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.801-812 BEGIN ====
def ex(x):
    m, e = x.man_exp()
    return '%s %s' % (m, e)


def unex(m, e):
    e = int(e)
    return arb(fmpz(m)) * arb(2) ** e if e >= 0 else arb(fmpz(m)) / arb(2) ** (-e)


def node_line(tag, v):
    return 'NODE %s %s' % (tag, ' '.join('%s %s' % (ex(x.lower()), ex(x.upper())) for x in v))
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.843-866 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1117-1135 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1145-1149 BEGIN ====
def minlow(D):
    m = D[0].lower()
    for x in D[1:]:
        m = x.lower() if x.lower() < m else m
    return m
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1204-1210 BEGIN ====
def dndec(x, sig=12):
    """a decimal string <= x (W1), from the exact lower end"""
    m, e = x.lower().man_exp()
    u = Fr(int(m)) * Fr(2) ** int(e)
    if u == 0:
        return '0'
    return _dec(u, sig, True) if u > 0 else '-' + _dec(-u, sig, False)
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1239-1262 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1265-1290 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1314-1333 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1487-1489 BEGIN ====
def tiling_ok(keys, x0, x1):
    ks = sorted(keys)
    return bool(ks) and ks[0][0] == x0 and ks[-1][1] == x1 and all(ks[i][1] == ks[i + 1][0] for i in range(len(ks) - 1))
# ==== COPY END ====


# ==== COPY px08_trbcert_v1_1.py:6a851374 l.1249-1278 BEGIN ====
def c_copy(plant=False):
    """C-COPY: every block between a COPY BEGIN marker and the next COPY END marker of this file equals the named lines of its source,
    whose sha256 must be COPY_SRC's. plant=True (PLANT-COPY) appends one byte to the last line of the middle block"""
    with open(os.path.abspath(__file__), 'rb') as fh:
        mine = fh.read().split(b'\n')
    beg = [i for i, x in enumerate(mine) if x.startswith(b'# ==== COPY ') and x.endswith(b' BEGIN ====')]
    end = [i for i, x in enumerate(mine) if x == b'# ==== COPY END ====']
    if not beg or len(beg) != len(end) or not all(b < e for b, e in zip(beg, end)) or not all(end[j] < beg[j + 1] for j in range(len(beg) - 1)):
        return False, 'markers'
    src, nl = {}, 0
    for j, (b, e) in enumerate(zip(beg, end)):
        tag = mine[b][len(b'# ==== COPY '):-len(b' BEGIN ====')].decode()
        fname, rest = tag.split(':', 1)
        sha8, rng = rest.split(' l.')
        lo, hi = (int(x) for x in rng.split('-'))
        if fname not in src:
            path, sha = COPY_SRC[fname]
            with open(path, 'rb') as fh:
                raw = fh.read()
            if hashlib.sha256(raw).hexdigest() != sha or not sha.startswith(sha8):
                return False, 'source %s' % fname
            src[fname] = raw.split(b'\n')
        blk = mine[b + 1:e]
        if plant and j == len(beg) // 2:
            blk = blk[:-1] + [blk[-1] + b'#']
        if blk != src[fname][lo - 1:hi]:
            return False, 'block %s' % tag
        nl += len(blk)
    return True, '%d blocks, %d lines' % (len(beg), nl)

# ==== COPY END ====


# ==== COPY px08_trbcert_v1_1.py:6a851374 l.1330-1336 BEGIN ====
def control(name, res, fails, fires, plant_res):
    """print one control line, record a failure, and record its plant (plant_res True = the plant failed the test, as it must)"""
    ok = res[0] if isinstance(res, tuple) else res
    out('%s: %s%s' % (name, 'PASS' if ok else 'FAIL', (' (worst %.3e)' % res[1]) if isinstance(res, tuple) and len(res) > 1 else ''))
    if not ok:
        fails.append(name.split()[0])
    fires.append(('PLANT-' + name.split()[0][2:], plant_res))
# ==== COPY END ====



# ------------------------------------------------------------------ gfmom with an F-long zero key: the one change against gfmom_lists
def gfmom_F(BC, D):
    """gfmom_lists (px08_m2bc4 l.351-384, copied above) with the zero key of length F = len(BC) in place of the 10-form Z0. gfmom_lists'
    Z0 would cut the exponents of an 11-form table to 10 entries in zip; here every key has F entries, so no fixz is needed.
    C-GFM checks it against gfmom_lists at F = 10"""
    F = len(BC)
    ZF = tuple([0] * F)
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
    Ms = [{ZF: acb(1)}]
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


# ------------------------------------------------------------------ the 11th form c = phi1.phi3 and the tilt form B_Y of option (i)
NN = 4 if MODE == 'n4' else 3
HALF = acb(arb(1) / 2)
KAPPA_T = 1 / (2 * ((1 - AV_A[0]).sqrt() + (1 - AV_A[2]).sqrt()) ** 2)
YT_X = arb(1) / 2 + KAPPA_T * (AV_A[0] + AV_A[2])


def Bc_block():
    """the 6 x 6 block of B_c (c = phi1.phi3; k-free, so the same in every block of the split)"""
    B = zeros(6)
    B[0, 2], B[2, 0] = HALF, HALF
    return B


def BY_block():
    """the 6 x 6 block of B_Y, Y = YT_X (X1 + X3) - c + X4 (k-free)"""
    B = zeros(6)
    B[0, 0], B[2, 2], B[3, 3] = acb(YT_X), acb(YT_X), acb(1)
    B[0, 2], B[2, 0] = -HALF, -HALF
    return B


def Bc_full(n):
    B = zeros(6 * n)
    addblk(B, n, 0, 2, eye(n) * HALF)
    addblk(B, n, 2, 0, eye(n) * HALF)
    return B


def BY_full(n):
    B = zeros(6 * n)
    I = eye(n)
    addblk(B, n, 0, 0, I * acb(YT_X))
    addblk(B, n, 2, 2, I * acb(YT_X))
    addblk(B, n, 3, 3, I)
    addblk(B, n, 0, 2, I * (-HALF))
    addblk(B, n, 2, 0, I * (-HALF))
    return B


GROUPS = ('P', 'D', 'T')
NFORMS = {'P': 11, 'D': 11, 'T': 10}


def grp_block(g, kap, kapT, plant=False):
    """the 6 x 6 block of the group's matrix: P = Q, D = Q - 2 delta B_Y, T = Q - 2 T(1/300, eps) - 2 delta B_Y. plant=True (PLANT-BLOCK)
    moves the (0, 0) entry by 1e-10"""
    Q = Q_block(kap, kapT)
    if g != 'P':
        Q = Q - BY_block() * acb(2 * DELTA_A)
    if g == 'T':
        Q = Q - T_block(kap, kapT) * 2
    if plant:
        Q[0, 0] = Q[0, 0] + acb(arb('1e-10'))
    return Q


def grp_full(g, k):
    """the full 6n x 6n matrix of the group"""
    Q = Qmat2(k)
    if g != 'P':
        Q = Q - BY_full(k.nrows()) * acb(2 * DELTA_A)
    if g == 'T':
        Q = Q - tilt2_full(k, TT, AV_A, EPS_A) * 2
    return Q


def bc_at(N, al, g, plant=False):
    """(w, det, BC) of group g at al (acb; al None = the N = 3 reflection, full matrices); BC[f] is the list of the blocks of B_f C over the
    split, for the first NFORMS[g] forms of (X1..X5, Z, aT, bT, aB, bB, c); a failed inverse raises ZeroDivisionError"""
    nf = NFORMS[g]
    if al is None:
        k, w = kw(N, None)
        Q = grp_full(g, k)
        det, C = Q.det(), Q.inv()
        Bs = forms2(k) + [Bc_full(k.nrows())]
        return w, det, [[Bs[f] * C] for f in range(nf)]
    w, det, BC = kw(N, al)[1], acb(1), [[] for _ in range(nf)]
    for b, (kap, kapT) in enumerate(comps(N, al)):
        Qb = grp_block(g, kap, kapT, plant and b == 0)
        det = det * Qb.det()
        Cb = Qb.inv()
        Bb = B_blocks(kap, kapT) + [Bc_block()]
        for f in range(nf):
            BC[f].append(Bb[f] * Cb)
    return w, det, BC


# ------------------------------------------------------------------ the insertion series (exact) and the families of the three groups
F11 = FORMS2 + ['c']
Z11 = tuple([0] * 11)
A0F = Fr(NN - 1, 2)


def m11(**kw_):
    e = [0] * 11
    for f, p in kw_.items():
        e[F11.index(f)] += p
    return tuple(e)


def ext11(P):
    return {tuple(e) + (0,): c for e, c in P.items()}


def proj(P, idx):
    """P (keys on the 11 forms) on the table forms idx; every exponent outside idx must be 0"""
    o = {}
    for e, c in P.items():
        assert all(e[i] == 0 for i in range(len(e)) if i not in idx), 'a form outside the table'
        k_ = tuple(e[i] for i in idx)
        o[k_] = o[k_] + c if k_ in o else c
    return o


def ck_arb(k, a):
    """C_k(a) = sum_{m>=k} cm(m) a^(m-k): the sum to m < EJ_M0 plus [0, cm(EJ_M0) a^(EJ_M0-k)/(1 - a)]; cm(m+1)/cm(m) = (2m-1)/(2m+2) < 1,
    so every later term ratio is below a"""
    s = arb(0)
    for m in range(k, EJ_M0):
        s += fr2a(cm_fr(m)) * a ** (m - k)
    tail = (fr2a(cm_fr(EJ_M0)) * a ** (EJ_M0 - k) / (1 - a)).upper()
    return s + arb(0).union(tail)


_X1, _X3, _X4, _C = {m11(X1=1): Fr(1)}, {m11(X3=1): Fr(1)}, {m11(X4=1): Fr(1)}, {m11(c=1): Fr(1)}
_QQ = padd({Z11: A0F}, _C)                               # (N-1)/2 + c
_DD = padd(_X1, pscale(_X3, Fr(-1)))                     # X1 - X3
PS = {'T': [padd({Z11: A0F}, pscale(_X1, Fr(-1, 2)), pscale(_X3, Fr(-1, 2)), _C),
            padd(pscale(_X1, -A0F / 2), pscale(_X3, -A0F / 2), pscale(_C, A0F),
                 pscale(pmul(padd(_C, pscale(_X1, Fr(-1))), padd(_C, pscale(_X3, Fr(-1)))), Fr(1, 2))),
            pscale(pmul(_QQ, pmul(_DD, _DD)), Fr(-1, 8)),
            pscale(pmul(pmul(_QQ, padd(_X1, _X3)), pmul(_DD, _DD)), Fr(-1, 16))],
      'M': [padd({Z11: A0F}, pscale(_X4, Fr(-1, 2)))] + [{m11(X4=k): -A0F * cm_fr(k)} for k in (1, 2, 3)]}
_E3 = padd(HX[3], pmul(HX[1], HX[2]), pscale(pmul(_H1sq, HX[1]), Fr(1, 6)))
EJ = [{Z11: Fr(1)}, ext11(HX[1]), ext11(_E2), ext11(_E3)]
FK = {r: [padd(*[pmul(PS[r][i], EJ[k - i]) for i in range(k + 1)]) for k in range(4)] for r in 'TM'}
assert all(max(sum(e) for e in FK[r][k]) <= 2 * k + 1 for r in 'TM' for k in range(4)), 'f_k above degree 2k + 1'
_a1, _a3, _a4 = AV_A[0], AV_A[2], AV_A[3]
S4BAR = apadd({m11(X1=4): ck_arb(4, _a1)}, {m11(X3=4): ck_arb(4, _a3)}, {m11(X1=3, X3=1): ck_arb(3, _a1) / 2},
              {m11(X1=2, X3=2): ck_arb(2, _a1) / 8}, {m11(X1=1, X3=3): ck_arb(1, _a1) * ck_arb(3, _a3)})
PBAR = {'T': apmul(apadd({Z11: fr2a(A0F)}, {m11(X1=1): arb(1) / 2}, {m11(X3=1): arb(1) / 2}), S4BAR),
        'M': {m11(X4=4): fr2a(A0F) * ck_arb(4, _a4)}}
SMALL_IDX = {'T': [0, 2, 10], 'M': [3]}                 # each row's insertion forms: (X1, X3, c) and (X4)
SP2 = {r: [proj(to_arb(pmul(PS[r][i], PS[r][i])), SMALL_IDX[r]) for i in range(4)] for r in 'TM'}
SP4 = {r: [proj(to_arb(pmul(pmul(PS[r][i], PS[r][i]), pmul(PS[r][i], PS[r][i]))), SMALL_IDX[r]) for i in range(4)] for r in 'TM'}
SPB = {r: proj(apmul(PBAR[r], PBAR[r]), SMALL_IDX[r]) for r in 'TM'}
assert all(max(sum(e) for e in P) <= 16 for r in 'TM' for P in SP4[r] + SP2[r] + [SPB[r]]), 'a small family above degree 16'
P_FAMS = [('1', {Z11: arb(1)}), ('E1', to_arb(EJ[1])), ('E2', to_arb(EJ[2])), ('E3', to_arb(EJ[3]))] + [
    ('f%s%d' % (r, k), to_arb(FK[r][k])) for r in 'TM' for k in range(4)]
PRODS = ['(E H2^2)^2', '(E H1^2)^3', '(E H1^2)^4', '(E H3^2)^2', '(E H1^2)^2 (E H2^2)^2', '(E H1^2)^6']
NAMES = {'P': ['P:' + nm for nm, P in P_FAMS],
         'D': ['D:' + nm for nm in N10] + ['D:' + nm for nm in N6] + ['D:%s^%d' % (X6F[v], m) for v, m in V1M]
         + [x for r in 'TM' for x in (['D:p%s%d_2' % (r, i) for i in range(4)] + ['D:p%s%d_4' % (r, i) for i in range(4)]
                                         + ['D:pbar%s_2' % r])]
         + ['D:' + nm for nm in PRODS],
         'T': ['T:H1^4', 'T:h_lo^4'] + ['T:%s^%d' % (X6F[v], m) for v, m in V1M]}
ALL = NAMES['P'] + NAMES['D'] + NAMES['T']
NV = len(ALL)
GIDX = {g: [ALL.index(nm) for nm in NAMES[g]] for g in GROUPS}
ONEF = sorted({v for v, m in V1M})
assert N10[:5] == ['1', 'H1^2', 'H1^4', 'H2^2', 'H3^2'] and N6[3] == 'h_lo^4' and len(set(ALL)) == NV


def tables(N, al, g, plant=False):
    """(w, det, [E_g P for the group's families]) at al (acb), al None = the N = 3 reflection. Group P: the 11-form table to degree 7.
    Group D: the 10-form table to degree 8, the 6-form table to degree 12, the one-forms to degree 20, each row's small table to degree 16,
    then the products. Group T: px08_m2bc4's tables_c (H1^4, h_lo^4, the one-forms) on its own matrix"""
    w, det, BC = bc_at(N, al, g, plant)
    if g == 'P':
        m = gfmom_F(BC, 7)
        return w, det, [pe(P, m) for nm, P in P_FAMS]
    m10 = gfmom_F(BC[:10], 8)
    m6 = gfmom_F(BC[:6], 12)
    m1 = {v: gfmom_F([BC[v]], 20) for v in ONEF}
    if g == 'T':
        return w, det, [pe(P10[2], m10), pe(P6[3], m6)] + [m1[v][(m,)] for v, m in V1M]
    e10 = [pe(P, m10) for P in P10]
    e = e10 + [pe(P, m6) for P in P6] + [m1[v][(m,)] for v, m in V1M]
    for r in 'TM':
        ms = gfmom_F([BC[i] for i in SMALL_IDX[r]], 16)
        e += [pe(P, ms) for P in SP2[r]] + [pe(P, ms) for P in SP4[r]] + [pe(SPB[r], ms)]
    h1, h2, h3 = e10[1], e10[3], e10[4]
    return w, det, e + [h2 * h2, h1 * h1 * h1, (h1 * h1) * (h1 * h1), h3 * h3, (h1 * h1) * (h2 * h2), (h1 * h1 * h1) * (h1 * h1 * h1)]


def ev_group(N, al, g):
    """the group's node values w det_g^{-1/2} E_g P (real parts)"""
    w, det, e = tables(N, al, g)
    a = w * posre(det, 'det Q_' + g).rsqrt()
    return [(a * x).real for x in e]


def ev_node(N, al):
    return ev_group(N, al, 'P') + ev_group(N, al, 'D') + ev_group(N, al, 'T')


# ------------------------------------------------------------------ G on Im al = SIG, one group at a time (px08_trbcert_v1_1's method)
def det_lower(N, u0, u1, y, g, plant=False):
    """an exact lower bound of |det| of the group's matrix on the box: the minimum over G_DSUB sub-boxes of prod_b abs_lower(det of the
    block); a block det that is not finite counts as 0. plant=True (PLANT-DET) widens the first block det of the first sub-box to contain 0"""
    lo = None
    for i in range(G_DSUB):
        al = acb(xball(u0 + (u1 - u0) * i / G_DSUB, u0 + (u1 - u0) * (i + 1) / G_DSUB), y)
        p = arb(1)
        for b, (kap, kapT) in enumerate(comps(N, al)):
            d = grp_block(g, kap, kapT).det()
            if plant and i == 0 and b == 0:
                d = acb(d.real.union(arb(0)), d.imag.union(arb(0)))
            p = p * (d.abs_lower() if d.is_finite() else arb(0))
        p = p.lower()
        lo = p if (lo is None or p < lo) else lo
    return lo


def prefactor(N, u0, u1, y, g, plant=False):
    """a = |w| det_lower^{-1/2} on the box, an exact upper end; None (the box bound is not finite) when the det bound is 0"""
    dlo = det_lower(N, u0, u1, y, g, plant)
    if not (dlo > 0):
        return None
    a = (kw(N, acb(xball(u0, u1), y))[1].abs_upper() / dlo.sqrt()).upper()
    return a if a.is_finite() else None


def eval_box(N, u0, u1, y, g, plant=False):
    """the group's family bounds a |E_g P| on the box, or None when one is not finite"""
    a = prefactor(N, u0, u1, y, g, plant)
    if a is None:
        return None
    try:
        w, det, e = tables(N, acb(xball(u0, u1), y), g)
    except (ZeroDivisionError, ValueError, NotCert):
        return None
    gb = [(a * x.abs_upper()).upper() for x in e]
    return gb if all(z.is_finite() for z in gb) else None


# ------------------------------------------------------------------ the CPU projection (after px08_trbhscan_v2 n3)
EVAL_PRIOR = {'node': {4: 60.0, 3: 40.0}, 'P': {4: 15.0, 3: 10.0}, 'D': {4: 28.0, 3: 18.0}, 'T': {4: 26.0, 3: 17.0},
              'flt': {4: 100.0, 3: 70.0}}     # seconds, a prior for an evaluation of each kind (dry runs and U's node items)


def guard(kind, N, tmax):
    """before every evaluation, the first included: stop with a CPU-STOP (VERDICT INCOMPLETE) unless cpu() + 1.25 max(the slowest
    evaluation of this kind so far, the prior) + 8 s <= LIM"""
    need = 1.25 * max(tmax, EVAL_PRIOR[kind][N]) + 8
    if cpu() + need > LIM:
        raise NotCert('CPU-STOP: a %s evaluation is projected past LIM (cpu %.1f s + %.1f s > %d s)' % (kind, cpu(), need, LIM))


# ------------------------------------------------------------------ the node items: all three groups at each node, at most 4 nodes per item
def node_parts():
    K = M_ // 2
    ch = -(-(K + 1) // 9)
    return {'nodes%d' % j: list(range(j * ch, min((j + 1) * ch, K + 1))) for j in range(9)}


def run_nodes(N):
    """the TW nodes al = 2 pi k / M of this item, C-EVEN at one of them (al and 2 pi - al), and the N = 3 reflection in nodes0; every
    evaluation behind the CPU projection"""
    ks = node_parts()[PART]
    if not ks:
        raise NotCert('no node in this item')
    keep, tmax = {}, [0.0]

    def timed(al):
        guard('node', N, tmax[0])
        t0 = cpu()
        v = ev_node(N, al)
        tmax[0] = max(tmax[0], cpu() - t0)
        return v
    for k in ks:
        STAGE[0] = 'node %d' % k
        keep[k] = timed(acb(PI * (2 * k) / M_))
        out(node_line(str(k), keep[k]))
    k = ks[0] if ks[0] > 0 else ks[-1]
    STAGE[0] = 'C-EVEN'
    mir = timed(acb(PI * (2 * (M_ - k)) / M_))
    out('CHECK C-EVEN k=%d %s' % (k, 'PASS' if all(x.overlaps(y) for x, y in zip(keep[k], mir)) else 'FAIL'))
    if PART == 'nodes0' and N == 3:
        STAGE[0] = 'reflection'
        out(node_line('refl', timed(None)))


# ------------------------------------------------------------------ the G items: one group on one eighth of [0, pi]
def tol_of(i):
    return TOL_MAIN if ALL[i].startswith('P:') else TOL_REM


def caps_from_tm(TM):
    """cap_i = TOL_i |T_M,i| (e^{SIG M} - 1)/2, as exact lower ends"""
    f = ((arb(SIG) * M_).exp() - 1) / 2
    return [(tol_of(i) * TM[i].abs_lower() * f).lower() for i in range(NV)]


def node_parse(lines, nodes, refl):
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


def tm_of(nodes):
    K = M_ // 2
    return [(nodes[0][i] + nodes[K][i] + 2 * sum((nodes[k][i] for k in range(1, K)), arb(0))) / M_ for i in range(NV)]


def header_ok(hd, parts):
    me = sha_file(os.path.abspath(__file__))
    return hd[0] == 'px08_trbhcert_v1' and hd[2] == me and hd[3] == 'ITEM=' + MODE and hd[6] == 'SIGC=' + SIGC and hd[4] in parts


def node_caps(N, man):
    """T_M from the node partials of this file at this SIGC (paths and sha256 in man; header and PART-DONE checked), and the caps"""
    nodes, refl, seen = {}, [None], []
    for line in open(man):
        h, p = line.split()
        assert sha_file(p) == h, 'sha mismatch %s' % p
        lines = open(p).read().split('\n')
        assert header_ok(lines[0].split(), node_parts()), 'header %s' % p
        assert any(x.strip() == 'VERDICT PART-DONE' for x in lines), 'not done %s' % p
        seen.append(lines[0].split()[4])
        node_parse(lines, nodes, refl)
    assert sorted(seen) == sorted(node_parts()) and sorted(nodes) == list(range(M_ // 2 + 1)) and (refl[0] is not None) == (N == 3)
    TM = tm_of(nodes)
    return TM, caps_from_tm(TM)


def g_loop(N, a0, a1, y, k, g, caps=None, plant=False, emit=True):
    """k boxes of width (a1 - a0)/k pi on Im al = y, in x order; a box is replaced in place by its halves while it fails or (caps given)
    a bound of group g exceeds its cap, to depth G_DEPTH; a box at depth G_DEPTH is kept whatever its bound. G-STOP: a failure at depth
    G_DEPTH, or more than G_MAXEV evaluations in this item. Returns (boxes, failed evaluations, evaluations)"""
    gi = GIDX[g]
    todo = [(a0 + (a1 - a0) * i / k, a0 + (a1 - a0) * (i + 1) / k, 0) for i in range(k)]
    nbox = nfail = nev = 0
    tmax = 0.0
    while todo:
        if nev >= G_MAXEV:
            raise NotCert('G-STOP: more than %d evaluations in this item' % G_MAXEV)
        u0, u1, d = todo.pop(0)
        nev += 1
        STAGE[0] = 'G box %s %s %s' % (g, u0, u1)
        if not plant:
            guard(g, N, tmax)
        t0 = cpu()
        gb = eval_box(N, u0, u1, y, g, plant)
        tmax = max(tmax, cpu() - t0)
        if gb is None:
            nfail += 1
            if emit:
                out('BOXFAIL %s %s depth %d' % (u0, u1, d))
            if d >= G_DEPTH:
                raise NotCert('G-STOP: box [%s, %s] pi failed at depth %d' % (u0, u1, d))
        if gb is None or (caps is not None and d < G_DEPTH and any(not (gb[j] <= caps[gi[j]]) for j in range(len(gi)))):
            um = (u0 + u1) / 2
            todo = [(u0, um, d + 1), (um, u1, d + 1)] + todo
            continue
        nbox += 1
        if emit:
            out('BOX %s %s %s' % (u0, u1, ' '.join(ex(z) for z in gb)))
    return nbox, nfail, nev


def run_g(N):
    g, j = PART[1], int(PART[2])
    a0, a1 = G_E[j]
    y = arb(SIG)
    TM, caps = node_caps(N, sys.argv[5])
    gi = GIDX[g]
    out('CAPS N=%d group %s (TOL |T_M| (e^{%g M} - 1)/2, M = %d): %s' % (N, g, SIG, M_, ', '.join('%s %s' % (ALL[i], updec(caps[i]))
                                                                                                  for i in gi)))
    STAGE[0] = 'PLANT-DET'
    try:
        g_loop(N, a0, a0 + (a1 - a0) / G_K, y, 1, g, plant=True, emit=False)
        fired = False
    except NotCert as stop:
        fired = str(stop).startswith('G-STOP')
    out('CHECK PLANT-DET %s' % ('FIRED' if fired else 'DID-NOT-FIRE'))
    if not fired:
        raise NotCert('PLANT-DET did not fire')
    nbox, nfail, nev = g_loop(N, a0, a1, y, G_K, g, caps)
    out('GSTAT %s: %d boxes, %d failed, %d evaluations (group %s, Im al = %g; value split on its %d families; %d det sub-boxes)' % (
        PART, nbox, nfail, nev, g, SIG, len(gi), G_DSUB))
    if j == 0:
        STAGE[0] = 'C-CONJ'
        vals = []
        for s in (1, -1):
            guard(g, N, 0.0)
            w, det, e = tables(N, acb(PI / 3, s * arb(SIG)), g)
            a = w * posre(det, 'det Q_' + g).rsqrt()
            vals.append([a * x for x in e])
        out('CHECK C-CONJ %s' % ('PASS' if all(x.overlaps(z.conjugate()) for x, z in zip(*vals)) else 'FAIL'))


# ------------------------------------------------------------------ the cov item: C-PROP (D, T), C-COVER (P, D, T) and the model checks
PROP_FAM = {'P': 'Q', 'D': 'Q - 2 delta B_Y', 'T': 'Q - 2 T(1/300, 0.65) - 2 delta B_Y'}


def q_real(N, al, g):
    """the full real matrix of group g at a real al (an arb point or interval), or at the N = 3 reflection (al None), as rows of arb"""
    k = kw(N, None)[0] if al is None else kw(N, acb(al))[0]
    Q = grp_full(g, k)
    return [[Q[i, j].real for j in range(Q.ncols())] for i in range(Q.nrows())]


def c_prop(N, g):
    """C-PROP: interval LDL^T of group g's matrix on al-intervals tiling [0, pi] (PROP_K of them, halved on failure), and at the N = 3
    reflection; k(2 pi - al) = P k(al) P (P = diag(1, -1) or diag(1, -1, 1)), and B_c, B_Y are k-free, so [0, pi] covers [0, 2 pi).
    Stop rule: a failure at depth PROP_DEPTH, or more than PROP_MAXEV evaluations. Returns (ok, intervals, smallest pivot, where)"""
    todo = [(Fr(i, PROP_K), Fr(i + 1, PROP_K), 0) for i in range(PROP_K)]
    nint, nev, dmin, where = 0, 0, None, None
    while todo:
        if nev >= PROP_MAXEV:
            return False, nint, dmin, 'PROP-STOP: more than %d evaluations' % PROP_MAXEV
        u0, u1, d = todo.pop()
        nev += 1
        D = ldlt(q_real(N, xball(u0, u1), g))
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
    if N == 3 and ldlt(q_real(N, None, g)) is None:
        return False, nint, dmin, 'the reflection failed'
    return True, nint, dmin, where


def plant_prop(N, where, g):
    """PLANT-PROP: at the midpoint of the interval with the smallest pivot, c = min_j (upper end of pivot j) >= lambda_min, so the matrix
    minus 2 c I is indefinite; its LDL^T must fail. True when it fails as it must"""
    u = (where[0] + where[1]) / 2
    A = q_real(N, PI * u.numerator / u.denominator, g)
    D = ldlt(A)
    if D is None:
        return False
    c = D[0].upper()
    for x in D[1:]:
        c = x.upper() if x.upper() < c else c
    return ldlt([[A[i][j] - (2 * c if i == j else 0) for j in range(len(A))] for i in range(len(A))]) is None


def det_all(N, al):
    """the three groups' dets (products of block dets) at al; C-COVER needs Re > 0 for each"""
    ds = []
    for g in GROUPS:
        d = acb(1)
        for (kap, kapT) in comps(N, al):
            d = d * grp_block(g, kap, kapT).det()
        ds.append(d)
    return ds


def plant_strip(N, sig):
    """m1c's PLANT-STRIP on group T: F' = det Q_T (cosh(c sigma) - cos al), c = 3/4, negative at al = i (1 + c) sigma / 2: the cover must
    fail"""
    c = arb(3) / 4
    ch = (c * arb(sig)).cosh()
    fp = lambda N_, al: [det_all(N_, al)[2] * (ch - al.cos())]
    neg_ok = fp(N, acb(0, (1 + c) * arb(sig) / 2))[0].real < 0
    ok, nb, bad = cover(N, sig, fp, CDMAX)
    return neg_ok and ok is False and bad is not None


KAPPA_T_F = 1.0 / (2 * (math.sqrt(1 - AV_F[0]) + math.sqrt(1 - AV_F[2])) ** 2)
YT_F = 0.5 + KAPPA_T_F * (AV_F[0] + AV_F[2])


def float_mats(N, al):
    """the float matrices of an independent construction: twlib2.mats, numpy B_c and B_Y, twlib2.tilt2"""
    kn = k_np_of(N, al)
    n = kn.shape[0]
    Qf, Bsf, _ = T2.mats(kn)
    Bcf = np.zeros((6 * n, 6 * n))
    Bcf[0:n, 2 * n:3 * n] = np.eye(n) / 2
    Bcf[2 * n:3 * n, 0:n] = np.eye(n) / 2
    BYf = YT_F * (Bsf[0] + Bsf[2]) - Bcf + Bsf[3]
    Tf = T2.tilt2(kn, T_F, AV_F, EPS_F)
    QG = {'P': Qf, 'D': Qf - 2 * DELTA_F * BYf, 'T': Qf - 2 * Tf - 2 * DELTA_F * BYf}
    return kn, list(Bsf) + [Bcf], BYf, QG


def c_port(N, plant=None):
    """C-PORT: Q, the ten forms, B_c, B_Y and the matrices of groups D and T against float_mats, entrywise, |a - f| <= PORT_TOL max(1, |f|),
    at al = 0.7, 2.3 and the N = 3 reflection. plant 'Y' (PLANT-PORT-Y) moves one entry of B_Y and plant 'T' (PLANT-PORT-T) one entry of
    group T's matrix, each by 1e-10"""
    worst = 0.0
    for al in [0.7, 2.3] + ([None] if N == 3 else []):
        k = kw(N, None)[0] if al is None else kw(N, acb(al))[0]
        kn, B11f, BYf, QG = float_mats(N, al)
        n = kn.shape[0]
        BY = BY_full(n)
        if plant == 'Y':
            BY[0, 0] = BY[0, 0] + acb(arb('1e-10'))
        GT = grp_full('T', k)
        if plant == 'T':
            GT[1, 1] = GT[1, 1] + acb(arb('1e-10'))
        pairs = ([(Qmat2(k), QG['P'])] + list(zip(forms2(k) + [Bc_full(n)], B11f)) + [(BY, BYf), (grp_full('D', k), QG['D']),
                                                                                        (GT, QG['T'])])
        for A, F in pairs:
            for i in range(A.nrows()):
                for j in range(A.ncols()):
                    a = A[i, j]
                    worst = max(worst, abs(float(a.real.mid()) - F[i, j]) / max(1.0, abs(F[i, j])), abs(float(a.imag.mid())))
    return worst <= PORT_TOL, worst


def c_block(N, plant=False):
    """C-BLOCK: for each group, at al = 0.3 + 0.2i, the block split against the full 6n x 6n matrices: the det (product of the block dets)
    and every moment of degree <= 3 of the group's forms (gfmom_F on the blocks, gfmom_F on the full B_f C) must overlap.
    plant=True (PLANT-BLOCK) moves the (0, 0) entry of group D's first block by 1e-10"""
    al = acb(arb('0.3'), arb('0.2'))
    for g in GROUPS:
        w, det, BC = bc_at(N, al, g, plant and g == 'D')
        k = kw(N, al)[0]
        Q = grp_full(g, k)
        C = Q.inv()
        Bs = forms2(k) + [Bc_full(k.nrows())]
        mb = gfmom_F(BC, 3)
        mf = gfmom_F([[Bs[f] * C] for f in range(NFORMS[g])], 3)
        if not Q.det().overlaps(det) or set(mb) != set(mf) or not all(mb[e].overlaps(mf[e]) for e in mf):
            return False
    return True


def float_values(N, al):
    """every family value w det^{-1/2} E P at the real al, from float_mats and pk10's float GFMom (degrees as the arb tables)"""
    kn, B11f, BYf, QG = float_mats(N, al)
    wf = (1 - math.cos(al)) if N == 4 else 0.5
    fa = lambda P: {e: float(c.mid()) for e, c in P.items()}
    vals = []
    for g in GROUPS:
        C = np.linalg.inv(QG[g])
        a = wf * np.linalg.det(QG[g]) ** -0.5
        if g == 'P':
            g11 = GFMom(B11f, C, 7)
            e = [g11.E(fa(P)) for nm, P in P_FAMS]
        else:
            g10, g6 = GFMom(B11f[:10], C, 8), GFMom(B11f[:6], C, 12)
            g1 = {v: GFMom([B11f[v]], C, 20) for v in ONEF}
            if g == 'T':
                e = [g10.E(fa(P10[2])), g6.E(fa(P6[3]))] + [g1[v].E({(m,): 1.0}) for v, m in V1M]
            else:
                e10 = [g10.E(fa(P)) for P in P10]
                e = e10 + [g6.E(fa(P)) for P in P6] + [g1[v].E({(m,): 1.0}) for v, m in V1M]
                for r in 'TM':
                    gs = GFMom([B11f[i] for i in SMALL_IDX[r]], C, 16)
                    e += [gs.E(fa(P)) for P in SP2[r]] + [gs.E(fa(P)) for P in SP4[r]] + [gs.E(fa(SPB[r]))]
                h1, h2, h3 = e10[1], e10[3], e10[4]
                e += [h2 * h2, h1 ** 3, h1 ** 4, h3 * h3, h1 * h1 * h2 * h2, h1 ** 6]
        vals += [a * x for x in e]
    return vals


def c_flt(N):
    """C-FLT: every family value at al = 0.7 against float_values, each value against itself: |a - f| <= FLT_TOL |f|. PLANT-FLT: the same
    test with the first arb value times 1 + 1e-7 must fail. Returns (ok, worst ratio, the family with the worst ratio, plant fired)"""
    av = [float(x.mid()) for x in ev_node(N, acb(arb('0.7')))]
    fv = float_values(N, 0.7)
    ratio = lambda a_: [abs(a - f) / abs(f) if f != 0 else abs(a) for a, f in zip(a_, fv)]
    rs = ratio(av)
    rp = ratio([av[0] * (1 + 1e-7)] + av[1:])
    i = max(range(NV), key=lambda q: rs[q])
    return rs[i] <= FLT_TOL, rs[i], ALL[i], max(rp) > FLT_TOL


def c_gfm(N, plant=False):
    """C-GFM: gfmom_F against the copied gfmom_lists at F = 10 (group P's ten U forms) to degree 4 at al = 0.7: the same keys, and every
    moment overlaps (the same arithmetic in the same order). plant=True (PLANT-GFM) adds 1e-10 to the first block of the first form"""
    w, det, BC = bc_at(N, acb(arb('0.7')), 'P')
    BC10 = [list(x) for x in BC[:10]]
    BCp = [list(x) for x in BC10]
    if plant:
        BCp[0] = [BCp[0][0] + eye(6) * acb(arb('1e-10'))] + BCp[0][1:]
    mF, mL = gfmom_F(BCp, 4), gfmom_lists(BC10, 4)
    return set(mF) == set(mL) and all(mF[e].overlaps(mL[e]) for e in mL)


def run_cov(N):
    for g in GROUPS:
        STAGE[0] = 'C-PROP ' + g
        t0 = cpu()
        ok, nint, dmin, where = c_prop(N, g)
        wh = ('[%s, %s]' % where) if isinstance(where, tuple) else str(where)
        out('C-PROP N=%d group %s (%s, interval LDL^T): %s, %d al-intervals tiling [0, pi]%s; smallest pivot >= %s on x in %s pi (%.1f s)'
            % (N, g, PROP_FAM[g], 'PASS' if ok else 'FAIL', nint, ' and the reflection' if N == 3 else '',
               dndec(dmin) if dmin is not None else '-', wh, cpu() - t0))
        out('CHECK C-PROP-%s %s' % (g, 'PASS' if ok else 'FAIL'))
        out('CHECK PLANT-PROP-%s %s' % (g, 'FIRED' if (ok and plant_prop(N, where, g)) else 'DID-NOT-FIRE'))
    STAGE[0] = 'cover ladder'
    t0 = cpu()
    sig, nb, tc = ladder(N, (0.5, 0.375, 0.25), det_all, CDMAX)
    out('COVER N=%d Re det > 0 for groups P, D, T: %s (%d boxes, %.1f s)' % (
        N, ('certified at sigma %g, M = %d' % (sig, SIG_LADDER[str(sig)])) if sig else 'no sigma of the ladder certified', nb, cpu() - t0))
    out('CHECK C-COVER %s' % ('PASS' if sig else 'FAIL'))
    out('CHECK PLANT-STRIP %s' % ('FIRED' if (sig and plant_strip(N, sig)) else 'DID-NOT-FIRE'))
    STAGE[0] = 'model checks'
    for name, res, plant_res in (('C-PORT', c_port(N), not c_port(N, 'Y')[0] and not c_port(N, 'T')[0]),
                                 ('C-BLOCK', (c_block(N),), not c_block(N, True)),
                                 ('C-GFM', (c_gfm(N),), not c_gfm(N, True))):
        out('%s N=%d: %s%s' % (name, N, 'PASS' if res[0] else 'FAIL', (' (worst %.3e)' % res[1]) if len(res) > 1 else ''))
        out('CHECK %s %s' % (name, 'PASS' if res[0] else 'FAIL'))
        out('CHECK PLANT-%s %s' % (name[2:], 'FIRED' if plant_res else 'DID-NOT-FIRE'))
    STAGE[0] = 'C-FLT'
    guard('flt', N, 0.0)
    t0 = cpu()
    ok, worst, wf, pf = c_flt(N)
    out('C-FLT N=%d (%d family values at al = 0.7 against float GFMom; worst %.3e at %s) (%.1f s)' % (N, NV, worst, wf, cpu() - t0))
    out('CHECK C-FLT %s' % ('PASS' if ok else 'FAIL'))
    out('CHECK PLANT-FLT %s' % ('FIRED' if pf else 'DID-NOT-FIRE'))


# ------------------------------------------------------------------ the assembly item: inputs read from sha-pinned files
# v1_1, v1_2: the producers whose partials are read (v1 wrote the cov outputs, the node partials and n4 gP0,
# v1_1 the other n4 group P items and the n3 G items), and C-ITEMCODE, which shows that their partials are what this file prints for them
V1_FILE = ('/mnt/g2/release/root/code/pk08/px08_trbhcert_v1.py',
           'f69581ad0a566167abaad7efd145541872335eb74d41139c4be3e6c3aa66f5e7')
V11_FILE = ('/mnt/g2/release/root/code/pk08/px08_trbhcert_v1_1.py',
            '2937ba65fe66fea11c3ef58fc30fb1715e910e1424857a857e306c087ac0401a')
PRODUCERS = [('px08_trbhcert_v1', V1_FILE[1]), ('px08_trbhcert_v1_1', V11_FILE[1]),
             ('px08_trbhcert_v1_2', sha_file(os.path.abspath(__file__)))]
ITEMCODE_MARK = b'# ' + b'-' * 66 + b' the assembly item: inputs read from sha-pinned files'


def itemcode_code(x):
    """a source line without its comment"""
    return x.split(b'#')[0].rstrip()


def itemcode_rest(old, new):
    """the rule: the line starts with old in the producer and with new here, and the rest of the line is the same"""
    return lambda x, y: x.startswith(old) and y == new + x[len(old):]


ITEMCODE_RULES = [
    (V1_FILE, [('output header', itemcode_rest(b"out('px08_trbhcert_v1 sha256 ", b"out('px08_trbhcert_v1_2 sha256 ")),
               ('G constants', lambda x, y: (itemcode_code(x) == b'G_K, G_DSUB, G_DEPTH, G_MAXEV = 4, 8, 2, 10'
                                             and itemcode_code(y) == b'G_K, G_DSUB, G_DEPTH, G_MAXEV = 4, 8, 2, 28')),
               ('LIM ceiling', itemcode_rest(b'if not (5 <= LIM <= 240) ', b'if not (5 <= LIM <= 360) '))]),
    (V11_FILE, [('output header', itemcode_rest(b"out('px08_trbhcert_v1_1 sha256 ", b"out('px08_trbhcert_v1_2 sha256 ")),
                ('LIM ceiling', itemcode_rest(b'if not (5 <= LIM <= 240) ', b'if not (5 <= LIM <= 360) '))])]


def header_ok(hd, parts):
    """v1_1, v1_2: this redefines the C-ITEMCODE region's header_ok (node_caps calls it by name) before main runs. A node partial is
    accepted from any producer (script name, full sha256) of PRODUCERS, at this ITEM and SIGC, if it is one of the parts"""
    return (hd[0], hd[2]) in PRODUCERS and hd[3] == 'ITEM=' + MODE and hd[6] == 'SIGC=' + SIGC and hd[4] in parts


def itemcode_region(raw):
    """(index of the line 'GPARTS = ...', the lines from it through ITEMCODE_MARK) of a file's bytes, or None"""
    L = raw.split(b'\n')
    i0 = [i for i, x in enumerate(L) if x.startswith(b'GPARTS = ')]
    i1 = [i for i, x in enumerate(L) if x == ITEMCODE_MARK]
    if len(i0) != 1 or len(i1) != 1 or i1[0] < i0[0]:
        return None
    return i0[0], L[i0[0]:i1[0] + 1]


def c_itemcode(plant=False):
    """C-ITEMCODE: each earlier producer (V1_FILE, V11_FILE: path and full sha256) and this file are byte-identical from the line
    'GPARTS = ...' to the asm part's first line (ITEMCODE_MARK), except the lines that ITEMCODE_RULES names for that producer, each rule
    matching exactly one differing line: the output header, which names the script; the LIM ceiling, 240 in v1 and v1_1 and 360 here; and,
    for v1, the G constants, where only G_MAXEV changes, from 10 to 28, with its comment. So the cov, node and G code that wrote v1's and
    v1_1's partials is this file's: LIM and G_MAXEV decide only whether an item stops (CPU-STOP, G-STOP: VERDICT INCOMPLETE), never what a
    PART-DONE item prints, and header_ok and read_parts read the header line. plant=True (PLANT-ITEMCODE) appends one byte to the region's
    second line in this file. Returns (ok, info)"""
    with open(os.path.abspath(__file__), 'rb') as fh:
        mine = itemcode_region(fh.read())
    if mine is None:
        return False, 'region bounds in this file'
    b0, b = mine
    if plant:
        b = b[:1] + [b[1] + b'#'] + b[2:]
    ok, info = True, []
    for (path, sha), rules in ITEMCODE_RULES:
        name = os.path.basename(path)
        with open(path, 'rb') as fh:
            raw = fh.read()
        if hashlib.sha256(raw).hexdigest() != sha:
            return False, '%s sha256' % name
        theirs = itemcode_region(raw)
        if theirs is None or len(theirs[1]) != len(b):
            return False, '%s region' % name
        a0, a = theirs
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        hits = [sum(1 for i in diff if rule(a[i], b[i])) for nm, rule in rules]
        ok = ok and len(diff) == len(rules) and all(h == 1 for h in hits)
        info.append('%s l.%d-%d against this file l.%d-%d, %d lines differ (%s): %s' % (
            name, a0 + 1, a0 + len(a), b0 + 1, b0 + len(b), len(diff), ', '.join('l.%d' % (b0 + i + 1) for i in diff) or 'none',
            ', '.join('%s %d' % (nm, h) for (nm, rule), h in zip(rules, hits))))
    return ok, '; '.join(info)


def rec_vals(path):
    d = {}
    for line in open(path, encoding='utf-8'):
        if line.startswith('#') or ' = ' not in line:
            continue
        k, v = line.rstrip('\n').split(' = ', 1)
        d[k.strip()] = v.strip()
    return d


def dec_arb(s):
    """the exact decimal s as an arb ball (Fraction route)"""
    q = Fr(s)
    return arb(q.numerator) / q.denominator


def asm_inputs(N):
    """U's certified pieces (S4_U_CERTIFIED_v2), U's Chernoff sum (px08_px03_v4 asm, PIECES line), the harmonic h_r (HZ_PLAN_v1_1 l.143)
    and the dry run's C-PL0 references (px08_trbhscan_v2 outputs), each parsed from its sha-pinned file"""
    UR = rec_vals(SOURCES['u_record'][0])
    g = lambda k: UR['N%d_%s' % (N, k)]
    inp = dict(R_U=dec_arb(g('PREF2_RE')) + dec_arb(g('PREF2_RHO4')),
               M3_OFF=dec_arb(g('M3_ANNULUS')) + dec_arb(g('M3_FAR')) + dec_arb(g('M3_EQUATOR')),
               LEAD=dec_arb(g('LEAD_LO')).union(dec_arb(g('LEAD_HI'))),
               C=[dec_arb(g('C%d_LO' % i)).union(dec_arb(g('C%d_HI' % i))) for i in (1, 2, 3)])
    m = re.search(r'Chernoff sum ([0-9.e+-]+);', open(SOURCES['m3_asm_n%d' % N][0]).read())
    inp['CHERN'] = dec_arb(m.group(1))
    hz = re.search(r'= ([0-9.]+) \(t\) and ([0-9.]+) \(h\) at N = 4; ([0-9.]+) and ([0-9.]+) at N = 3',
                   open(SOURCES['hz_plan'][0], encoding='utf-8').read())
    inp['H'] = {'T': dec_arb(hz.group(1 if N == 4 else 3)), 'M': dec_arb(hz.group(2 if N == 4 else 4))}
    pl = re.search(r'C-PL0 N=%d \(M = 32\):.*lead_p/lead_U: T ([0-9.]+), M ([0-9.]+);' % N, open(SOURCES['scan_n%d' % N][0]).read())
    inp['PL0'] = {'T': float(pl.group(1)), 'M': float(pl.group(2))}
    return inp


M3_LAM = {4: ['m3_n4_sh1', 'm3_n4_sh2a', 'm3_n4_sh2b', 'm3_n4_sh3a', 'm3_n4_sh3b', 'm3_n4_far'],
          3: ['m3_n3_sh1a', 'm3_n3_sh1b', 'm3_n3_sh2a', 'm3_n3_sh2b', 'm3_n3_sh3a', 'm3_n3_sh3b', 'm3_n3_far']}


M3_FAM = sorted((f, 'v%d' % v) for f in ('ann1', 'ann2', 'ann3', 'far') for v in range(6))


def c_far_h(N, scale=1, plant=None):
    """C-FAR-H: every off-Omega term of U's m3 has the form J^p e^{-kappa J} times a factor nonincreasing in J, and
    ((N-1)/2 + J/2) J^p e^{-kappa J} is nonincreasing for every J >= 300 iff kappa >= 1/(N - 1 + 300) + p/300. Annulus (kappa = lam_sv
    prev_sv, p = 0) and far (kappa = lam'_v avp_v, p = 0): kappa >= lam_min/5, lam_min the smallest lam on the annulus and far lam lines
    of U's m3 outputs (the lam each family used is among them) and 1/5 the smallest prev or avp; equator: kappa = 1 - cos 0.685, p = 1/2.
    The 1/5: U's annulus exponent uses PREV_A[s][v] and its far exponent AVP_A[v] (px08_px03_v4 a236ed42 l.1577-1580);
    PREV_A = [AV_A] + SH_A[:-1] >= 1/5, since AV_A >= 1/5 (l.659) and SH_A lies between AV_A and AVP_A (l.865, l.867); AVP_A >= 0.45
    (l.862). The count: every line of these outputs that contains 'lam' must parse, and the parsed (family, v) pairs must be
    U's m3 families, ann1..ann3 (NSH = 3, l.864) and far, each at v0..v5 (l.1578-1580), so that a changed output format cannot drop a
    smaller lam silently. scale = 1/100 is PLANT-FAR-H (every kappa divided by 100); plant 'fmt' (PLANT-FAR-FMT) changes the format of
    the first lam line and plant 'fam' (PLANT-FAR-FAM) skips the far file. Returns (ok, lam_min, lines with lam, parsed lam lines,
    parsed families)"""
    lams, fams, nlam = [], set(), 0
    for key in M3_LAM[N]:
        if plant == 'fam' and key.endswith('_far'):
            continue
        for line in open(SOURCES[key][0]):
            if plant == 'fmt' and nlam == 0 and 'lam' in line:
                line = line.replace(', lam ', ', lam= ')
            nlam += ('lam' in line)
            m = re.match(r'\s+(ann\d+|far)\s+(v\d+): theta [0-9/]+, lam (\d+)/(\d+) ', line)
            if m:
                lams.append(Fr(int(m.group(3)), int(m.group(4))))
                fams.add((m.group(1), m.group(2)))
    lmin = min(lams)
    thr = 1 / arb(N - 1 + J_)
    k_af = arb(lmin.numerator) / lmin.denominator / 5 * scale
    k_eq = (1 - arb('0.685').cos()) * scale
    cnt = nlam == len(lams) and sorted(fams) == M3_FAM
    return bool(cnt and k_af >= thr and k_eq >= thr + arb(1) / 600), lmin, nlam, len(lams), len(fams)


def c_series_p(plant=False):
    """C-SERIES-P: (1) the exact p_k against an independent t-series of p_L at 20 rational points (exact Fractions): row T from
    s1 s3 = (sum_m b_m X1^m t^m)(sum_m b_m X3^m t^m), b_0 = 1, b_m = -cm(m), and p_T = ((N-1)/2)(t c + s1 s3) - (X1 + X3)/2 + c s1 s3
    + t (X1 X3 + c^2)/2; row M from p_M = ((N-1)/2) s4 - X4/2; every coefficient of t^0..t^3 must agree. (2) In floats, at 24 points of Omega:
    |p_L - sum_k t^k p_k| <= t^4 pbar_4 (pbar_4 with its arb coefficients' upper ends). plant=True (PLANT-SERIES-P) moves the X1^2
    coefficient of row T's p_2 by 2^-40, which (1) must reject. Returns (ok, worst float ratio)"""
    import random
    rnd = random.Random(20261107)
    P2 = dict(PS['T'][2])
    if plant:
        e0 = m11(X1=2)
        P2[e0] = P2[e0] + Fr(1, 2 ** 40)
    PT = [PS['T'][0], PS['T'][1], P2, PS['T'][3]]
    ev = lambda P, pt: sum((c * Fr(pt[0]) ** e[0] * Fr(pt[2]) ** e[2] * Fr(pt[3]) ** e[3] * Fr(pt[10]) ** e[10] for e, c in P.items()), Fr(0))
    bser = lambda X: [Fr(1)] + [-cm_fr(m) * X ** m for m in (1, 2, 3)]
    mul = lambda a, b: [sum((a[i] * b[k - i] for i in range(k + 1)), Fr(0)) for k in range(4)]
    for _ in range(20):
        X1, X3, X4 = Fr(rnd.randint(0, 600), 10), Fr(rnd.randint(0, 900), 10), Fr(rnd.randint(0, 900), 10)
        c = Fr(rnd.randint(-100, 100), 100) * (X1 + X3) / 2
        pt = [X1, 0, X3, X4, 0, 0, 0, 0, 0, 0, c]
        S = mul(bser(X1), bser(X3))
        sT = [A0F * (c * (1 if k == 1 else 0) + S[k]) - ((X1 + X3) / 2 if k == 0 else 0) + c * S[k]
              + ((X1 * X3 + c * c) / 2 if k == 1 else 0) for k in range(4)]
        sM = [A0F * b - (X4 / 2 if k == 0 else 0) for k, b in enumerate(bser(X4))]
        if any(ev(PT[k], pt) != sT[k] for k in range(4)) or any(ev(PS['M'][k], pt) != sM[k] for k in range(4)):
            return False, float('inf')
    worst = 0.0
    A0 = float(A0F)
    for _ in range(24):
        X1, X3, X4 = rnd.uniform(0, 0.9 * J_ * AV_F[0]), rnd.uniform(0, 0.9 * J_ * AV_F[2]), rnd.uniform(0, 0.9 * J_ * AV_F[3])
        c = rnd.uniform(-1.0, 1.0) * math.sqrt(X1 * X3)
        fv = [X1, 0, X3, X4, 0, 0, 0, 0, 0, 0, c]
        for r in 'TM':
            x = T_F * c + math.sqrt(1 - T_F * X1) * math.sqrt(1 - T_F * X3) if r == 'T' else math.sqrt(1 - T_F * X4)
            exact = A0 * x - (1 - x * x) / (2 * T_F)
            ser = sum(T_F ** k * sum(float(cc) * math.prod(fv[i] ** e[i] for i in range(11) if e[i]) for e, cc in PS[r][k].items())
                      for k in range(4))
            b = T_F ** 4 * sum(float(cc.upper()) * math.prod(fv[i] ** e[i] for i in range(11) if e[i]) for e, cc in PBAR[r].items())
            if abs(exact - ser) > b + 1e-12 * (1 + abs(exact)):
                return False, abs(exact - ser) / b
            worst = max(worst, abs(exact - ser) / b if b > 0 else 0.0)
    return True, worst


def c_maj(plant=False):
    """C-MAJ: |p_r| <= (N-1)/2 + alpha1_r e^{delta Y}, Y = YT_X (X1 + X3) - c + X4, at 4000 random points of Omega(t = 1/300) and at the 30
    points X1 = X3 = X, c = -X, X4 = 0 (X = 1..30), where the Young step is nearly tight for row T; p from the exact chart formulas.
    plant=True (PLANT-MAJ) halves alpha1. Returns (ok, the largest |p| / bound)"""
    import random
    rnd = random.Random(20261107)
    A0, d = float(A0F), DELTA_F
    a1 = {'T': 1 / (math.e * d), 'M': 0.5 / (math.e * d)}
    if plant:
        a1 = {r: v / 2 for r, v in a1.items()}
    pts = [(float(X), float(X), -float(X), 0.0) for X in range(1, 31)]
    for _ in range(4000):
        X1, X3, X4 = rnd.uniform(0, J_ * AV_F[0]), rnd.uniform(0, J_ * AV_F[2]), rnd.uniform(0, J_ * AV_F[3])
        pts.append((X1, X3, rnd.uniform(-1.0, 1.0) * math.sqrt(X1 * X3), X4))
    worst = 0.0
    for X1, X3, c, X4 in pts:
        Y = YT_F * (X1 + X3) - c + X4
        xT = T_F * c + math.sqrt(1 - T_F * X1) * math.sqrt(1 - T_F * X3)
        xM = math.sqrt(1 - T_F * X4)
        for r, x in (('T', xT), ('M', xM)):
            p = A0 * x - (1 - x * x) / (2 * T_F)
            worst = max(worst, abs(p) / (A0 + a1[r] * math.exp(d * Y)))
    return worst <= 1.0, worst


def multiset_ok(checks):
    """C-MULTISET: the partial items printed exactly their CHECK lines (C-EVEN per node item, C-CONJ in gP0, gD0, gT0, PLANT-DET per G item)"""
    return sorted(c for c, r in checks) == sorted(['C-CONJ'] * 3 + ['C-EVEN'] * len(node_parts()) + ['PLANT-DET'] * len(GPARTS))


COV_CHECKS = ['C-PROP-P', 'C-PROP-D', 'C-PROP-T', 'PLANT-PROP-P', 'PLANT-PROP-D', 'PLANT-PROP-T', 'C-COVER', 'PLANT-STRIP', 'C-PORT',
              'PLANT-PORT', 'C-BLOCK', 'PLANT-BLOCK', 'C-GFM', 'PLANT-GFM', 'C-FLT', 'PLANT-FLT']


def read_parts(N, man):
    """the cov output, the 9 node partials and the 24 G partials (paths and sha256 in man), each from a producer of PRODUCERS (v1_1, v1_2), at
    this SIGC (the cov item at SIGC '-'); returns (nodes, refl, boxes per group, partial CHECK lines, cov CHECK lines, the cov's certified
    sigma, the parts read from each producer)"""
    nodes, refl, boxes, checks, cov, seen = {}, [None], {g: [] for g in GROUPS}, [], {}, []
    cov_sig = None
    prod = {nm: [] for nm, h in PRODUCERS}
    for line in open(man):
        h, p = line.split()
        assert sha_file(p) == h, 'sha mismatch %s' % p
        lines = open(p).read().split('\n')
        hd = lines[0].split()
        assert (hd[0], hd[2]) in PRODUCERS and hd[3] == 'ITEM=' + MODE, 'header %s' % p
        assert any(x.strip() == 'VERDICT PART-DONE' for x in lines), 'not done %s' % p
        seen.append(hd[4])
        prod[hd[0]].append(hd[4])
        if hd[4] == 'cov':
            for x in lines:
                w_ = x.split()
                if w_ and w_[0] == 'CHECK':
                    cov[w_[1]] = w_[-1]
                ms = re.search(r'certified at sigma ([0-9.]+), M', x)
                if x.startswith('COVER ') and ms:
                    cov_sig = ms.group(1)
            continue
        assert hd[6] == 'SIGC=' + SIGC, 'sigma %s' % p
        node_parse(lines, nodes, refl)
        for x in lines:
            w_ = x.split()
            if w_ and w_[0] == 'BOX':
                g = hd[4][1]
                gb = [unex(w_[i], w_[i + 1]) for i in range(3, len(w_), 2)]
                assert len(gb) == len(GIDX[g])
                boxes[g].append(((Fr(w_[1]), Fr(w_[2])), gb))
            elif w_ and w_[0] == 'CHECK':
                checks.append((w_[1], w_[-1]))
    assert sorted(seen) == sorted(['cov'] + list(node_parts()) + GPARTS), seen
    assert sorted(nodes) == list(range(M_ // 2 + 1)) and (refl[0] is not None) == (N == 3)
    for g in GROUPS:
        keys = [k for k, gb in boxes[g]]
        assert len(set(keys)) == len(keys) and tiling_ok(keys, 0, 1), 'box tiling of [0, 1], group %s' % g
        boxes[g].sort()
    return nodes, refl[0], boxes, checks, cov, cov_sig, prod


def run_asm(N):
    fails, fires = [], []
    K = M_ // 2
    nodes, refl, boxes, checks, cov, cov_sig, prod = read_parts(N, sys.argv[5])
    out('PARTITION N=%d: nodes 0..%d once each, reflection %s; G boxes tiling [0, 1] pi: P %d, D %d, T %d: PASS' % (
        N, K, 'yes' if refl else 'no', len(boxes['P']), len(boxes['D']), len(boxes['T'])))
    fires.append(('PLANT-TILE', not tiling_ok([k for k, gb in boxes['D']][1:], 0, 1)))
    ok = multiset_ok(checks)
    out('C-MULTISET N=%d (C-EVEN per node item, C-CONJ per group, PLANT-DET per G item): %s' % (N, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-MULTISET')
    fires.append(('PLANT-MULTISET', not multiset_ok([c for c in checks if c[0] != 'C-CONJ'])))
    for c, r in checks:
        if r != ('FIRED' if c == 'PLANT-DET' else 'PASS'):
            fails.append(c)
    okc = sorted(cov) == sorted(COV_CHECKS) and all(cov[c] == ('FIRED' if c.startswith('PLANT-') else 'PASS') for c in COV_CHECKS)
    out('COV N=%d (the cov item\'s %d CHECK lines: C-PROP P/D/T, C-COVER, C-PORT, C-BLOCK, C-GFM, C-FLT and their plants): %s; certified '
        'sigma %s, this run %s' % (N, len(cov), 'PASS' if okc and cov_sig == SIGC else 'FAIL', cov_sig, SIGC))
    if not (okc and cov_sig == SIGC):
        fails.append('COV')
    ok, info = c_copy()
    out('C-COPY (every COPY block = its source lines, byte for byte): %s, %s' % ('PASS' if ok else 'FAIL', info))
    if not ok:
        fails.append('C-COPY')
    fires.append(('PLANT-COPY', not c_copy(True)[0]))
    ok, info = c_itemcode()
    out('C-ITEMCODE (v1 and v1_1 each byte-identical to this file from GPARTS to the asm part, except the lines named per producer): %s, %s'
        % ('PASS' if ok else 'FAIL', info))
    if not ok:
        fails.append('C-ITEMCODE')
    fires.append(('PLANT-ITEMCODE', not c_itemcode(True)[0]))
    out('PRODUCERS N=%d (script, sha256: the parts read from it): %s' % (N, '; '.join('%s %s: %s' % (
        nm, h, ' '.join(sorted(prod[nm])) or 'none') for nm, h in PRODUCERS)))
    TM = tm_of(nodes)
    TH = [(nodes[0][i] + nodes[K][i] + 2 * sum((nodes[k][i] for k in range(2, K, 2)), arb(0))) * 2 / M_ for i in range(NV)]
    caps = caps_from_tm(TM)

    def stop_ok(kk, gb, g):
        return kk[1] - kk[0] <= Fr(1, 128) or all(gb[j] <= caps[GIDX[g][j]] for j in range(len(gb)))
    ok = all(stop_ok(kk, gb, g) for g in GROUPS for kk, gb in boxes[g])
    out('C-REFINE N=%d (every box of width pi/128 or within the caps): %s' % (N, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-REFINE')
    gp = list(boxes['D'][0][1])
    gp[0] = caps[GIDX['D'][0]] * 2 + 1
    fires.append(('PLANT-REFINE', not stop_ok((Fr(0), Fr(1, 32)), gp, 'D')))
    G = [arb(0)] * NV
    for g in GROUPS:
        for j, i in enumerate(GIDX[g]):
            G[i] = maxup([gb[j] for kk, gb in boxes[g]])
    err = [(2 * G[i] / ((arb(SIG) * M_).exp() - 1)).upper() for i in range(NV)]
    errh = [(2 * G[i] / ((arb(SIG) * (M_ // 2)).exp() - 1)).upper() for i in range(NV)]
    out('G line N=%d: Im al = %g (the boundary line of the C-COVER strip), M = %d' % (N, SIG, M_))
    half = all((TM[i] + (-err[i]).union(err[i])).overlaps(TH[i] + (-errh[i]).union(errh[i])) for i in range(NV))
    out('C-HALF N=%d: %s' % (N, 'PASS' if half else 'FAIL'))
    if not half:
        fails.append('C-HALF')
    Jv = [TM[i] + (-err[i]).union(err[i]) + (refl[i] / 2 if N == 3 else 0) for i in range(NV)]
    PR = pref_arb(N)
    I = {nm: PR * PR * Jv[i] for i, nm in enumerate(ALL)}
    miss = []
    for i, nm in enumerate(ALL):
        tl = TM[i].abs_lower()
        within = err[i] <= tol_of(i) * tl
        if not within:
            miss.append(nm)
        out('  N=%d I[%s] = %s; G %s, TW error %s, error/|T_M| %s%s' % (N, nm, I[nm].str(12), updec(G[i]), updec(err[i]),
                                                                    updec(err[i] / tl) if tl > 0 else 'inf', '' if within else ' TARGET-MISS'))
    out('TARGET N=%d (TW error <= 1e-3 |T_M| for group P, <= 1e-1 |T_M| else): %s; misses, reported: %s' % (
        N, 'all within' if not miss else '%d of %d miss' % (len(miss), NV), ', '.join(miss) or 'none'))
    STAGE[0] = 'controls'
    inp = asm_inputs(N)
    control('C-SERIES-H (H1..H3 against twlib2)', c_series(HX)[:2], fails, fires, not c_series(HX, True)[0])
    control('C-SERIES-P (the insertion series, exact and float)', c_series_p(), fails, fires, not c_series_p(True)[0])
    control('C-HBAR (per-degree scale)', c_hbar(), fails, fires, not c_hbar(True)[0])
    control('C-MAJ (|p| <= (N-1)/2 + alpha1 e^{delta Y} on Omega, floats)', c_maj(), fails, fires, not c_maj(True)[0])
    ok, lmin, nl, npar, nfam = c_far_h(N)
    out('C-FAR-H N=%d (kappa >= 1/(N - 1 + 300) + p/300; lam_min %s over %d lam lines of U\'s m3, %d of them parsed, %d of its '
        '%d families; kappa_af >= lam_min/5; equator 1 - cos 0.685): %s' % (N, lmin, nl, npar, nfam, len(M3_FAM), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-FAR-H')
    fires.append(('PLANT-FAR-H', not c_far_h(N, arb(1) / 100)[0]))
    fires.append(('PLANT-FAR-FMT', not c_far_h(N, plant='fmt')[0]))
    fires.append(('PLANT-FAR-FAM', not c_far_h(N, plant='fam')[0]))
    lead = I['P:1']
    rep = lead.overlaps(inp['LEAD']) and all((I['P:E%d' % j] / lead).overlaps(inp['C'][j - 1]) for j in (1, 2, 3))
    out('C-REPRO N=%d (group P against S4_U_CERTIFIED_v2: I[1] %s vs LEAD, I[E_j]/I[1] %s vs C1..C3): %s' % (
        N, lead.str(14), ', '.join((I['P:E%d' % j] / lead).str(12) for j in (1, 2, 3)), 'PASS' if rep else 'FAIL'))
    if not rep:
        fails.append('C-REPRO')
    fires.append(('PLANT-REPRO', not (lead * (1 + arb('1e-6'))).overlaps(inp['LEAD'])))
    pl = {r: I['P:f%s0' % r] / lead for r in 'TM'}
    pl_ok = lambda q: all(abs(float(q[r].mid()) - inp['PL0'][r]) <= 1e-9 for r in 'TM')
    ok = pl_ok(pl)
    out('C-PL0 N=%d (lead_p/lead_U against the dry run px08_trbhscan_v2, M = 32 floats, <= 1e-9): T %s vs %.12f, M %s vs %.12f: %s' % (
        N, pl['T'].str(14), inp['PL0']['T'], pl['M'].str(14), inp['PL0']['M'], 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-PL0')
    fires.append(('PLANT-PL', not pl_ok({'T': pl['M'], 'M': pl['T']})))
    rooted = [i for i, nm in enumerate(ALL) if not nm.startswith('P:')] + [ALL.index('P:1')]
    pos = all(Jv[i].upper() > 0 for i in rooted)
    out('C-POS N=%d (every upper end > 0 for the families under a root or a log in the reading): %s' % (N, 'PASS' if pos else 'FAIL'))
    fires.append(('PLANT-POS', not all(x.upper() > 0 for x in [arb(0)] + [Jv[i] for i in rooted])))
    if not pos:
        out('CHECKS FAIL: %s' % '; '.join(fails + ['C-POS']))
        out('VERDICT INVALID')
        return
    STAGE[0] = 'reading'
    U = {nm: I[nm].upper() for nm in ALL}
    t = T_A
    A0 = fr2a(A0F)

    def n4_of(pre):
        hi = arb(0)
        for e, c in HHI.items():
            term = c.abs_upper()
            for vv in range(6):
                if e[vv]:
                    term = term * (U['%s:%s^%d' % (pre, X6F[vv], 4 * sum(e))].log() * e[vv] / (4 * sum(e))).exp()
            hi = hi + term
        return U['%s:h_lo^4' % pre].sqrt().sqrt() + hi
    N4d, N4t = n4_of('D'), n4_of('T')
    REd = (t ** 4 / 24 * U['D:hbar4'] + t ** 4 / 2 * U['D:H2^2'] + t ** 6 / 72 * U['D:hbar3^2'] + t ** 4 / 6 * (U['D:H1^2'] * U['D:hbar3^2']).sqrt()
           + t ** 5 / 6 * (U['D:H2^2'] * U['D:hbar3^2']).sqrt() + t ** 4 / 4 * (U['D:H1^4'] * U['D:hbar2^2']).sqrt()
           + t ** 5 / 8 * U['D:H1^2'].sqrt() * N4d ** 2 + t ** 6 / 48 * N4d ** 3 * U['D:1'].sqrt().sqrt())
    rhod = (t * U['T:H1^4'].sqrt().sqrt() + t * t / 2 * N4t) ** 4 / 24
    e_ = arb(1).exp()
    a1 = {'T': 1 / (e_ * DELTA_A), 'M': 1 / (2 * e_ * DELTA_A)}
    E3L2 = U['D:H3^2'].sqrt() + 27 * (U['D:H1^4'] * U['D:(E H2^2)^2']).sqrt().sqrt() + arb(5) ** 6 / 6 * U['D:(E H1^2)^3'].sqrt()
    IE2 = [U['D:1'], U['D:H1^2'], U['D:E2^2'], E3L2 * E3L2]
    IE4 = [U['D:1'], U['D:H1^4'], 8 * arb(3) ** 12 * U['D:(E H2^2)^2'] + arb(7) ** 16 / 2 * U['D:(E H1^2)^4'],
           27 * (arb(3) ** 16 * U['D:(E H3^2)^2'] + arb(7) ** 20 * U['D:(E H1^2)^2 (E H2^2)^2'] + arb(11) ** 24 / 1296 * U['D:(E H1^2)^6'])]
    res = {}
    for r in 'TM':
        Rmain = A0 * inp['R_U'] + a1[r] * (REd + rhod)
        Rcross = sum((t ** (i + j) * (U['D:p%s%d_2' % (r, i)] * IE2[j]).sqrt() for i, j in [(i, j) for i in range(4) for j in range(4) if i + j >= 4]),
                     arb(0))
        Rins = t ** 4 * sum((t ** j * (U['D:pbar%s_2' % r] * IE2[j]).sqrt() for j in range(4)), arb(0))
        L2p = U['D:p%s0_2' % r].sqrt() + sum((t ** (i + j) * (U['D:p%s%d_4' % (r, i)] * IE4[j]).sqrt().sqrt()
                                              for i in range(4) for j in range(4) if 1 <= i + j <= 3), arb(0))
        tail = PR * L2p * inp['CHERN'].sqrt()
        off = (A0 + arb(J_) / 2) * inp['M3_OFF']
        R = Rcross + Rins + Rmain + tail + off
        d = [I['P:f%s%d' % (r, k)] for k in range(4)]
        U3t = d[0] + t * (d[1] + t * (d[2] + t * d[3]))
        tol = CERT_MARGIN * (U3t - inp['H'][r])
        res[r] = dict(Rmain=Rmain, Rcross=Rcross, Rins=Rins, L2p=L2p, tail=tail, off=off, R=R, d=d, U3t=U3t, tol=tol)
    tok = lambda frac: all(res[r]['R'].upper() <= (res[r]['tol'] * frac).lower() for r in 'TM')
    ok = tok(arb(1))
    out('C-TOL N=%d (the consumer tolerance: R_cert(r) <= TOL(r) = (1/4) (U3_p(r)(1/300) - h_r), both rows): %s; R/TOL %s (T), %s (M)' % (
        N, 'PASS' if ok else 'FAIL', (res['T']['R'] / res['T']['tol']).str(4), (res['M']['R'] / res['M']['tol']).str(4)))
    if not ok:
        fails.append('C-TOL')
    fires.append(('PLANT-TOL', not tok(arb(1) / 100)))
    out('REASON U3_p: an exact cubic in t, the (P) form; the consumer evaluates it at its t')
    out('REASON R_cross and R_ins: t^m (m >= 4) times J-free integrals on group D\'s measure, which majorizes the plain one: nondecreasing in t')
    out('REASON R_main: ((N-1)/2) U\'s R_E + rho4 (nonincreasing in J by U\'s reasons) plus alpha1 times the U chain on Q - 2 delta B_Y and '
        'Q - 2 T(t) - 2 delta B_Y, with hbar_j at t = 1/300 (majorizing every t\' <= t) and the matrices Loewner-decreasing in t (the t-part of '
        'T is PSD, delta B_Y is J-free): nondecreasing in t')
    out('REASON tail: t-powers times J-free norms, times U\'s Chernoff sum (nonincreasing in J by U\'s reasons)')
    out('REASON off-Omega: ((N-1)/2 + J/2) times U\'s annulus, far and equator J-bounds, nonincreasing for J >= 300 by C-FAR-H')
    out('REASON PR: PR = pref_arb(N), a ratio of reduced Laplacian determinants of fixed strip graphs, does not depend on J')
    out('REASON TW: every TW error sits inside the certified J = 300 enclosures; each reason compares exact J-bounds with the exact '
        'J = 300 bound, which the enclosure upper end majorizes')
    out('REASON Z4: each J-bound is the chain at its own Omega(J) and tilt T(1/J) before the comparison, so the comparison is between valid '
        'bounds, pointwise in J')
    out('CHECKS %s' % ('all PASS' if not fails else 'FAIL: ' + '; '.join(fails)))
    out('PLANTS %s' % ' '.join('%s:%s' % (nm, 'FIRED' if f else 'DID-NOT-FIRE') for nm, f in fires))
    valid = not fails and all(f for nm, f in fires)
    out('R_U^(delta) N=%d: R_E^(delta) <= %s (N4_D <= %s), rho4^(delta) <= %s (N4_T <= %s); alpha1 T %s, M %s; PR <= %s; Chern <= %s' % (
        N, updec(REd), updec(N4d), updec(rhod), updec(N4t), updec(a1['T']), updec(a1['M']), updec(PR), updec(inp['CHERN'])))
    for r in 'TM':
        x = res[r]
        out('U3_P N=%d row %s: d_0 %s, d_1 %s, d_2 %s, d_3 %s; U3_p(1/300) %s' % (N, r, x['d'][0].str(15), x['d'][1].str(15), x['d'][2].str(15),
                                                                            x['d'][3].str(12), x['U3t'].str(15)))
        out('READING N=%d row %s (t = 1/300, every J >= 300): R_cert <= %s; R_main <= %s, R_cross <= %s, R_ins <= %s, tail <= %s (L2^(p) <= %s), '
            'off-Omega <= %s; TOL >= %s' % (N, r, updec(x['R']), updec(x['Rmain']), updec(x['Rcross']), updec(x['Rins']), updec(x['tail']),
                                             updec(x['L2p']), updec(x['off']), dndec(x['tol'])))
    out('VERDICT %s' % ('VALID' if valid else 'INVALID'))


def main():
    N = 4 if MODE == 'n4' else 3
    try:
        if PART == 'cov':
            run_cov(N)
        elif PART in GPARTS:
            run_g(N)
        elif PART == 'asm':
            run_asm(N)
            out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
            return
        else:
            run_nodes(N)
    except NotCert as e:
        out('NOTCERT %s' % e)
        out('VERDICT INCOMPLETE')
        return
    out('VERDICT PART-DONE')
    out('CPU %.1f s maxrss_kb %d' % (cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    main()
