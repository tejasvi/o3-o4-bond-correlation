#!/usr/bin/env python3
"""px08_a2cert_v1.py -- pk08, S4 port: the certified A2 = tr_H(K^(1/2) V xi_b^2 K^(1/2))/lambda_h, one constant per N, uniform for every
J >= 300 (S4_A2_DESIGN_v1 0eca31ca, a delta on px08_trbcert_v1_1 6baa4535). xi_b is the MB vertical; by the T <-> B mirror A2 equals the same
trace with xi_TM, TRB's insertion, so the chart and the form X_T are TRB's. For Lemma D4/D4m of HS_NORMX_LEMMA_NOTE_v1 (1340a52c).

Insertion G = xi_TM^2 = X_T^2 phi(t X_T)^2, phi(u) = 1/(1 + sqrt(1 - u)): G0 = X_T^2/4, G1 = X_T^3/8, G2 = 5 X_T^4/64 (G0 = F0^2, G1 = 2 F0 F1,
G2 = F1^2 + 2 F0 F2); on Omega G <= c_a^2 X_T^2 and 0 <= G - G0 - t G1 - t^2 G2 <= K_G t^3 X_T^5, K_G = (phi(a)^2 - 1/4 - a/8 - 5 a^2/64)/a^3
(phi^2 has nonnegative coefficients).
Claim: A2_N = main + R3 + R_cub + R_F + tail + far at t = 1/300 (design item 3), with
  main = I[GE0] + t max(I[GE1], 0) + t^2 max(I[GE2], 0), GE0 = G0, GE1 = G1 + G0 H1, GE2 = G2 + G1 H1 + G0 P2;
  R3 = t^3 ((I[G1^2] I[P2^2])^1/2 + (I[G2^2] I[H1^2])^1/2) + t^4 (I[G2^2] I[P2^2])^1/2
       + c_a^2 (t^3/6 I[X_T^2 hbar3] + t^3/2 (16 I[G0^2 H1^2] I[hbar2^2])^1/2 + t^4/8 I[X_T^2 hbar2^2]);
  R_cub = (c_a^2/6) I_t[X_T^8]^1/4 (t (I_t[H1^4]^1/4 + I_t[hhat^4]^1/4))^3;  R_F = t^3 K_G I_t[X_T^5];
  tail = L2 (sum_v e^{-lam_v J a_v} T_v)^1/2 with L2 = I[G0^2]^1/2 + t (I[G1^2]^1/2 + I[G0^2 H1^2]^1/2)
       + t^2 (I[G2^2]^1/2 + 3^5 I[E G1^2 E H1^2]^1/2 + 3^4 I[G0^4]^1/4 I[(E P2^2)^2]^1/4) (hypercontractivity per Gaussian, node products);
  far = PR (2J)^2 (2 far_one(N, J, a) + far_one(N, J, aZ));
  I[f] = PR int dmu w det(Q)^{-1/2} E[f], I_t[f] = PR int dmu w det(Q_t)^{-1/2} E_t[f], Q_t = Q - 2 T(1/300, eps), PR = pref_arb(N).
Each integral is TW on M nodes (k = 0..M/2, evenness) plus the N = 3 reflection atom (weight 1/2), with the error 2 G/(e^{sigma M} - 1),
G = sup |w det^{-1/2} E[f]| on Im al = sigma by maximum modulus on the closed strip where Re det Q > 0 and Re det Q_t > 0 (C-COVER).
Parameters as TRB: a = aZ = 1/4, eps = 9/20, t = 1/300, J = 300; lam = 17/40, 17/40, 119/200 (theta 17/20).
Uniform in J >= 300 (one reason per remainder piece; design item 3):
  for t' <= t, I[GE0] + t' I[GE1] + t'^2 I[GE2] <= main, with no sign condition (C-SIGN is INFO only);
  R3 and L2: powers of t times untilted integrals (hbar_j(a, aZ) majorizes for every t' <= t; twlib hbar has no t);
  R_cub, R_F: the tilt fixed at t = 1/300 (its t-part t cfun(a_v) on the diagonal is PSD; the integrands are >= 0; hhat grows with t);
  tail: e^{-lam J a} decreases in J and T_v does not depend on J;
  far: decreases for J >= 300 iff (p+1)/300 < c(a) and (p+1)/300 < c(aZ) (C-FAR; p + 1 = 5/2 at N = 4, 2 at N = 3; c(a) = 1 - sqrt(1 - a)).
  Also as TRB: PR is free of J; every TW error sits inside the J = 300 enclosures; each J-bound is the chain's at its own Omega(J) and tilt
  T(1/J) before the comparison (Z4). The asm prints one REASON line per piece and these three.
As TRB: the Chernoff masses T_v = PR int dmu w det(Q - 2 lam_v B_v)^{-1/2} are bounded by T_v <= (1 - theta2)^{-d/2} I[1] through C-PROP
  (theta2 = 9/10, al-intervals tiling [0, pi] and the N = 3 reflection) and C-RANK (rank B_v = d = N - 1). G on the eighths of [0, pi].
  The moments use TRB's 7-form table (X_T, X_B, Z, a2T, a3T, a2B, a3B) to degree 8 for the H and G families and the 5-form table (X_T, X_B,
  Z, W_T, W_B) to degree 8 for the hbar families; no family needs more. C-SCAN compares the integrals shared with TRB's dry run (I[GE0] =
  I[F0^2], P2^2, H1^2, (E P2^2)^2, I_t[H1^4], I_t[hhat^4]) and I[1] with twrig4's lead (a gross-error check, not part of the bound).
  No sub-boxes.
Controls of the asm (each with a plant that must fire): C-MULTISET, C-COPY, C-PROP (four families), C-COVER/PLANT-STRIP, C-REFINE, C-HALF,
  C-BLOCK, C-PORT (B, T, P), C-SERIES (H1, H2, P2, GE), C-HBAR, C-HHAT, C-FLT, C-SCAN, C-POS, C-RANK, C-KG, C-FAR (plant at J = 5), C-A2T;
  the partial items carry C-EVEN, C-CONJ and PLANT-DET, and PLANT-TILE checks the box tiling.
Gate: STOP (VERDICT INVALID) if A2_4 > 12 or A2_3 > 28 (C-A2T, D4's needs; PLANT-A2T at 1/100 of the target).
Copied blocks: every block between '# ==== COPY <file>:<sha8> l.<a>-<b> BEGIN ====' and '# ==== COPY END ====' equals lines a..b of that
file byte for byte (C-COPY at the asm, with PLANT-COPY).
Usage: px08_a2cert_v1.py n4|n3 cov LIM | n4|n3 nodes0|nodes1 LIM SIGC | n4|n3 g0..g7 LIM SIGC NODE_MANIFEST | n4|n3 asm LIM SIGC MANIFEST.
"""
import resource, sys, time, math, hashlib, signal, os
from fractions import Fraction as Fr
PARTS = ('cov', 'nodes0', 'nodes1', 'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'asm')
NEXTRA = {'cov': 0, 'nodes0': 1, 'nodes1': 1}
if len(sys.argv) < 4 or sys.argv[1] not in ('n4', 'n3') or sys.argv[2] not in PARTS:
    print('usage: px08_a2cert_v1.py n4|n3 cov LIM | n4|n3 nodes0|nodes1 LIM SIGC | n4|n3 g0..g7 LIM SIGC NODE_MANIFEST | n4|n3 asm LIM SIGC '
          'MANIFEST')
    sys.exit(2)
MODE, PART, LIM = sys.argv[1], sys.argv[2], int(sys.argv[3])
if not (5 <= LIM <= 240) or len(sys.argv) != 4 + NEXTRA.get(PART, 2) or (len(sys.argv) > 4 and sys.argv[4] not in ('0.5', '0.375', '0.25')):
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
    'gfmom.py': ('/mnt/g2/release/root/code/pk10/scripts/gfmom.py', 'c8cadafec97a92071b7f90d66a69b0f24fc91a7bd6ec751c1327a8218c9a2768'),
    'lapl2.py': ('/mnt/g2/release/root/code/pk10/scripts/lapl2.py', 'b28ffbdb86fab237564f2db9ea8b3e904481fba31ad79e39421de7b8a9dfe116'),
    'vacmod2.py': ('/mnt/g2/release/root/code/pk10/scripts/vacmod2.py', '533546b173af147a56e9531e26afa64cb3dbaccefd5fb7b1283f03baff06a000'),
    'pseries.py': ('/mnt/g2/release/root/code/pk10/scripts/pseries.py', '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e'),
    'g2sw_core_snapshot.py': ('/mnt/g2/release/root/code/pk10/scripts/g2sw_core_snapshot.py', 'f1b51241c54e496a8de699cc3160de3281bf98c67d019f4e92459a222d3d003a'),
    'scan_n4': ('/mnt/g2/release/root/code/pk08/out/px08_trbscan_v2_n4.out', 'b612df5b21a81a0cb849273dbae3279ee0b46cf5a272eab75e08612ba0af5992'),
    'scan_n3': ('/mnt/g2/release/root/code/pk08/out/px08_trbscan_v2_n3.out', '11472c2f9a3fdced5701331784dd7c12528de26b6aa2e09569c41f27d14266cf'),
}
COPY_SRC = {
    'px08_m2bc4.py': ('/mnt/g2/release/root/code/pk08/px08_m2bc4.py', '6527d21b7661a355c6534cc055f1fb8f3ae74be9256dbd6a3c65067ca6a34a17'),
}

# ==== COPY px08_m2bc4.py:6527d21b l.57-62 BEGIN ====
def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'
# ==== COPY END ====



out('px08_a2cert_v1 sha256 %s ITEM=%s %s LIM=%d SIGC=%s' % (sha_file(os.path.abspath(__file__)), MODE, PART, LIM, SIGC))
_bad = ['%s %s' % (n_, sha_file(p_)) for n_, (p_, h_) in sorted(SOURCES.items()) if sha_file(p_) != h_]
_bad += ['%s %s' % (n_, sha_file(p_)) for n_, (p_, h_) in sorted(COPY_SRC.items()) if sha_file(p_) != h_]
out('C-HASH %s (%d sources)%s' % ('PASS' if not _bad else 'FAIL', len(SOURCES) + len(COPY_SRC), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
import re
import numpy as np
from flint import arb, acb, arb_mat, acb_mat, ctx, fmpz
sys.path.insert(0, SCR)
import twlib as TL
from gfmom import GFMom
ctx.prec = 128
PI = arb.pi()
A_, AZ_ = arb(1) / 4, arb(1) / 4                    # a = aZ = 1/4 (twrig4's run)
EPS_, T_, J_ = arb(9) / 20, arb(1) / 300, 300       # eps = 0.45 (dry run), t = 1/300
LAM = [arb(17) / 40, arb(17) / 40, arb(119) / 200]  # X_T, X_B, Z: theta 17/20 over 2 Lmax, Lmax = 1, 1, 5/7 (dry run)
THETA2 = arb(9) / 10                                # C-PROP on Q - 2 (lam_v/theta2) B_v gives 2 lam_v C^1/2 B_v C^1/2 < theta2
A2_TARGET = {4: Fr(12), 3: Fr(28)}                  # the gate (D4's needs, HS2 <= 86.5 with the v1_2 boxes): certified A2_N <= these
A_F, EPS_F, T_F = 0.25, 0.45, 1.0 / 300            # the same, as floats, for the twlib checks
KX, KY, CDMAX = 32, 4, 12
EJ_M0 = 400
HBAR_TOL, PORT_TOL, FLT_TOL, SER_TOL, SCAN_TOL, LEAD_TOL = 1e-12, 1e-13, 1e-9, 1e-15, 1e-3, 1e-8
SIG_LADDER = {'0.5': 64, '0.375': 88, '0.25': 128}
SIG = float(SIGC) if SIGC != '-' else None          # 0.5, 0.375 and 0.25 are exact binary fractions
M_ = SIG_LADDER.get(SIGC)
G_E = {'g%d' % j: (Fr(j, 8), Fr(j + 1, 8)) for j in range(8)}     # G on the eighths of [0, pi] (CPU per item, as px08_m2bc4)
G_K, G_DSUB, G_DEPTH, G_MAXEV = 4, 8, 2, 28                       # 4 boxes of width pi/32 per eighth; 4 (1 + 2 + 4) = 28 at most
PROP_K, PROP_DEPTH, PROP_MAXEV = 32, 8, 2048

# ==== COPY px08_m2bc4.py:6527d21b l.92-93 BEGIN ====
class NotCert(Exception):
    pass
# ==== COPY END ====



# ------------------------------------------------------------------ the one-column model: twlib's nine forms, exact polynomials
FORMS1 = ['XT', 'XB', 'Z', 'a2T', 'a3T', 'a2B', 'a3B', 'WT', 'WB']     # twlib.FORMS, in its order
IX1 = {f: i for i, f in enumerate(FORMS1)}
NF = len(FORMS1)
Z0 = tuple([0] * NF)
F7 = [0, 1, 2, 3, 4, 5, 6]      # the 7-form table: X_T, X_B, Z, a2T, a3T, a2B, a3B (H1, H2 and the F's use only these)
F5 = [0, 1, 2, 7, 8]            # the 5-form table: X_T, X_B, Z, W_T, W_B (hbar and hhat use only these, times powers of X_T)


def m1(**kw):
    e = [0] * NF
    for f, p in kw.items():
        e[IX1[f]] += p
    return tuple(e)

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



# twlib l.87-90 (H1) and l.190-193 (H2), exact; twrig4 l.19-21 (P2, F0, F1, F2, FE)
H1 = padd({m1(XT=1): Fr(1, 2), m1(XB=1): Fr(1, 2), m1(Z=1): Fr(1, 2)},
          {m1(XT=2): Fr(-1, 8), m1(XB=2): Fr(-1, 8), m1(Z=2): Fr(-3, 8)},
          *[{m1(**{'X' + r: 1, 'a2' + r: 1}): Fr(-1, 2), m1(**{'X' + r: 1, 'a3' + r: 1}): Fr(1, 2),
             m1(**{'a2' + r: 1, 'a3' + r: 1}): Fr(-1, 2), m1(**{'X' + r: 1, 'Z': 1}): Fr(1, 2)} for r in ('T', 'B')])
H2 = padd({m1(XT=2): Fr(1, 4), m1(XB=2): Fr(1, 4), m1(Z=2): Fr(1, 4)},
          {m1(XT=3): Fr(-1, 16), m1(XB=3): Fr(-1, 16), m1(Z=3): Fr(-3, 16)},
          *[{m1(**{'X' + r: 2, 'a2' + r: 1}): Fr(-1, 8), m1(**{'X' + r: 2, 'a3' + r: 1}): Fr(1, 8),
             m1(**{'a2' + r: 1, 'a3' + r: 1, 'Z': 1}): Fr(-1, 8), m1(**{'X' + r: 1, 'Z': 2}): Fr(1, 8)} for r in ('T', 'B')])
P2 = padd(H2, pscale(pmul(H1, H1), Fr(1, 2)))
F0, F1, F2 = {m1(XT=1): Fr(1, 2)}, {m1(XT=2): Fr(1, 8)}, {m1(XT=3): Fr(1, 16)}
G0, G1, G2 = pmul(F0, F0), pscale(pmul(F0, F1), Fr(2)), padd(pmul(F1, F1), pscale(pmul(F0, F2), Fr(2)))    # xi^2 = X_T^2 phi(t X_T)^2
GE = [G0, padd(G1, pmul(G0, H1)), padd(G2, pmul(G1, H1), pmul(G0, P2))]
FAM_U7 = [('1', {Z0: Fr(1)}), ('GE0', GE[0]), ('GE1', GE[1]), ('GE2', GE[2]), ('G1^2', pmul(G1, G1)), ('G2^2', pmul(G2, G2)),
          ('P2^2', pmul(P2, P2)), ('H1^2', pmul(H1, H1)), ('G0^2', pmul(G0, G0)), ('G0^2 H1^2', pmul(pmul(G0, H1), pmul(G0, H1))),
          ('G0^4', pmul(pmul(G0, G0), pmul(G0, G0)))]
FAM_T7 = [('X_T^8', {m1(XT=8): Fr(1)}), ('X_T^5', {m1(XT=5): Fr(1)}), ('H1^4', pmul(pmul(H1, H1), pmul(H1, H1)))]
assert all(sum(e) <= 8 for nm, P in FAM_U7 + FAM_T7 for e in P), 'a family above degree 8'

# ==== COPY px08_m2bc4.py:6527d21b l.243-272 BEGIN ====
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
# ==== COPY END ====



def forms1(k):
    """arb port of twlib.forms (l.38-48): the nine 3n x 3n forms X_T, X_B, Z, a2T, a3T, a2B, a3B, W_T, W_B"""
    n = k.nrows()
    I = eye(n)
    M = I - k
    half = arb(1) / 2

    def blk(i, j, Bm):
        B = zeros(3 * n)
        addblk(B, n, i, j, Bm)
        if i != j:
            addblk(B, n, j, i, Bm.transpose())
        return B
    return [blk(0, 0, I), blk(1, 1, I), blk(2, 2, I), blk(0, 2, I * half), blk(0, 2, k.transpose() * half), blk(1, 2, I * half),
            blk(1, 2, k.transpose() * half), blk(0, 0, M.transpose() * M), blk(1, 1, M.transpose() * M)]


def Qmat1(k):
    """arb port of twlib.Qmat (l.51-56)"""
    n = k.nrows()
    I = eye(n)
    M = I - k
    Q = zeros(3 * n)
    for r in (0, 1):
        addblk(Q, n, r, r, I + M.transpose() * M)
        addblk(Q, n, r, 2, M.transpose() * (-1))
        addblk(Q, n, 2, r, M * (-1))
    addblk(Q, n, 2, 2, I * 3)
    return Q


def dkap(a, aZ):
    """twlib.delta_kappa (l.105-106)"""
    return 1 - (1 - a).sqrt() + (a * aZ).sqrt() / (1 + (1 - aZ).sqrt())


def tilt1(k, t, eps):
    """arb port of twlib.tilt (l.109-121) with a = aZ = A_"""
    n = k.nrows()
    I = eye(n)
    M = I - k
    k2 = (1 / eps - 1) * dkap(A_, AZ_) ** 2 / 2
    T = zeros(3 * n)
    for r in (0, 1):
        addblk(T, n, r, r, I * acb(t * cfun_a(A_)) + M.transpose() * M * acb(eps / 2))
        addblk(T, n, r, 2, M.transpose() * acb(-eps / 2))
        addblk(T, n, 2, r, M * acb(-eps / 2))
    addblk(T, n, 2, 2, I * acb(t * cfun_a(AZ_) + eps + 2 * k2))
    return T


def Qt_full(k):
    """the full Q_t = Qmat1(k) - 2 tilt1(k, 1/300, 9/20)"""
    return Qmat1(k) - tilt1(k, T_, EPS_) * 2

# ==== COPY px08_m2bc4.py:6527d21b l.311-316 BEGIN ====
def comps(N, al, plant=False):
    """(k, k^T) values of the blocks: '+' (e^{i al}, e^{-i al}), '-' (e^{-i al}, e^{i al}), and the axis (1, 1) at N = 4"""
    z = (acb(0, 1) * al).exp()
    zi = 1 / z
    c = [(z, z if plant else zi), (zi, z)]
    return c + [(acb(1), acb(1))] if N == 4 else c
# ==== COPY END ====



# ------------------------------------------------------------------ the 3 x 3 blocks of the split: every matrix of the model is a polynomial in k
# and k^T = k^{-1}, so on the eigenvector of k with eigenvalue kap it is the 3 x 3 matrix with k -> kap, k^T -> kapT = 1/kap and
# M^T M -> (1 - kapT)(1 - kap); the traces of the moment recursion are sums over the blocks (C-BLOCK checks this against the full matrices)
def Q1_block(kap, kapT):
    """twlib.Qmat on one eigenvector of k"""
    mu = (1 - kapT) * (1 - kap)
    Q = zeros(3)
    for r in (0, 1):
        Q[r, r] = 1 + mu
        Q[r, 2] = -(1 - kapT)
        Q[2, r] = -(1 - kap)
    Q[2, 2] = 3
    return Q


def B1_blocks(kap, kapT):
    """twlib.forms (X_T, X_B, Z, a2T, a3T, a2B, a3B, W_T, W_B) on one eigenvector of k"""
    h = acb(arb(1) / 2)
    mu = (1 - kapT) * (1 - kap)
    Bs = []
    for v in range(3):
        B = zeros(3)
        B[v, v] = 1
        Bs.append(B)
    for (i, cij, cji) in ((0, h, h), (0, kapT * h, kap * h), (1, h, h), (1, kapT * h, kap * h)):
        B = zeros(3)
        B[i, 2], B[2, i] = cij, cji
        Bs.append(B)
    for v in (0, 1):
        B = zeros(3)
        B[v, v] = mu
        Bs.append(B)
    return Bs


def T1_block(kap, kapT, plant=False):
    """twlib.tilt at t = 1/300, eps = 9/20, a = aZ = 1/4 on one eigenvector of k. plant=True (PLANT-BLOCK) adds 1e-10 to the (0, 0) entry"""
    mu = (1 - kapT) * (1 - kap)
    e2 = acb(EPS_ / 2)
    k2 = (1 / EPS_ - 1) * dkap(A_, AZ_) ** 2 / 2
    T = zeros(3)
    for r in (0, 1):
        T[r, r] = acb(T_ * cfun_a(A_)) + e2 * mu
        T[r, 2] = -e2 * (1 - kapT)
        T[2, r] = -e2 * (1 - kap)
    T[2, 2] = acb(T_ * cfun_a(AZ_) + EPS_ + 2 * k2)
    if plant:
        T[0, 0] = T[0, 0] + acb(arb('1e-10'))
    return T


def Qt_block(kap, kapT, plant=False):
    return Q1_block(kap, kapT) - T1_block(kap, kapT, plant) * 2

# ==== COPY px08_m2bc4.py:6527d21b l.343-347 BEGIN ====
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


# ==== COPY px08_m2bc4.py:6527d21b l.448-484 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.488-533 BEGIN ====
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



def hbar1_arb(j):
    """arb port of twlib.hbar(j, a, aZ) (l.93-102) at a = aZ = 1/4, term by term (Ej by ej_arb with its tail bound, Cj by cj_arb)"""
    f = arb(math.factorial(j - 1))
    P = {m1(Z=j): f / (2 * (1 - AZ_) ** j), m1(Z=j + 1): 3 * ej_arb(j, AZ_)}
    for r in ('T', 'B'):
        X, W = 'X' + r, 'W' + r
        P = apadd(P, {m1(**{X: j}): f / (2 * (1 - A_) ** j), m1(**{X: j + 1}): ej_arb(j, A_), m1(**{X: j, W: 1}): cj_arb(j, A_) / 2,
                      m1(**{X: j, 'Z': 1}): cj_arb(j, A_) / 2, m1(**{X: 1, 'Z': j}): 2 * cj_arb(j, AZ_)})
    return P


def hhat_traded(h2, t):
    """twrig4's hhat_tw (l.27-45): t hhat >= (t^2/2) hbar2 on Omega = {t X_r <= a, t Z <= aZ}; a degree-2 monomial c m goes to (c t/2) m;
    a degree-3 monomial loses one Z (factor aZ) if it has one, else one X_T (factor a), else one X_B (factor a), with c/2"""
    o = {}
    for e, c in h2.items():
        if sum(e) == 2:
            o = apadd(o, {e: c * t / 2})
            continue
        e2 = list(e)
        if e2[IX1['Z']] > 0:
            e2[IX1['Z']] -= 1
            fac = AZ_
        elif e2[IX1['XT']] > 0:
            e2[IX1['XT']] -= 1
            fac = A_
        else:
            e2[IX1['XB']] -= 1
            fac = A_
        o = apadd(o, {tuple(e2): c * fac / 2})
    assert all(sum(e) == 2 for e in o), 'hhat not of degree 2'
    return o


def to_arb_fr(P):
    return {e: arb(c.numerator) / c.denominator for e, c in P.items()}


def proj(P, idx):
    """P (keys on the nine forms) on the table forms idx; every exponent outside idx must be 0"""
    o = {}
    for e, c in P.items():
        assert all(e[i] == 0 for i in range(NF) if i not in idx), 'a form outside the table'
        k_ = tuple(e[i] for i in idx)
        o[k_] = o[k_] + c if k_ in o else c
    return o


HB2, HB3 = hbar1_arb(2), hbar1_arb(3)
HH = hhat_traded(HB2, T_)
XT2 = {m1(XT=2): arb(1)}
FAM_U5 = [('X_T^2 hbar3', apmul(XT2, HB3)), ('hbar2^2', apmul(HB2, HB2)), ('X_T^2 hbar2^2', apmul(XT2, apmul(HB2, HB2)))]
FAM_T5 = [('hhat^4', apmul(apmul(HH, HH), apmul(HH, HH)))]
assert all(sum(e) <= 8 for nm, P in FAM_U5 + FAM_T5 for e in P), 'an hbar family above degree 8'
P7_U = [proj(to_arb_fr(P), F7) for nm, P in FAM_U7]
P5_U = [proj(P, F5) for nm, P in FAM_U5]
P7_T = [proj(to_arb_fr(P), F7) for nm, P in FAM_T7]
P5_T = [proj(P, F5) for nm, P in FAM_T5]
NAMES_U = [nm for nm, P in FAM_U7] + [nm for nm, P in FAM_U5] + ['(E P2^2)^2', 'E G1^2 E H1^2']
NAMES_T = [nm for nm, P in FAM_T7] + [nm for nm, P in FAM_T5]
NAMES = NAMES_U + NAMES_T
NV = len(NAMES)
IP2SQ, IG1SQ, IH1SQ = NAMES_U.index('P2^2'), NAMES_U.index('G1^2'), NAMES_U.index('H1^2')
TOLV = [arb(1) / 1000] * 4 + [arb(1) / 10] * (NV - 4)     # relative TW targets (caps, TARGET line): 1e-3 for 1, GE0-GE2; 1e-1 else
assert NAMES[:4] == ['1', 'GE0', 'GE1', 'GE2'] and NV == 20

# ==== COPY px08_m2bc4.py:6527d21b l.758-760 BEGIN ====
def fixz(m, F):
    m[(0,) * F] = m.pop(Z0)
    return m
# ==== COPY END ====



# ------------------------------------------------------------------ the node functions at one point (the 16 untilted and 4 tilted families)
def bc_at(N, al, blockfn, fullfn):
    """(w, det, BC) at al (acb) for the matrix family blockfn/fullfn (Q or Q_t); al None = the N = 3 reflection (full matrices); a failed
    inverse raises ZeroDivisionError"""
    if al is None:
        k, w = kw(N, None)
        Q = fullfn(k)
        det, C = Q.det(), Q.inv()
        return w, det, [[Bf * C] for Bf in forms1(k)]
    w, det, BC = kw(N, al)[1], acb(1), [[] for _ in range(NF)]
    for (kap, kapT) in comps(N, al):
        Qb = blockfn(kap, kapT)
        det = det * Qb.det()
        Cb = Qb.inv()
        for f, Bb in enumerate(B1_blocks(kap, kapT)):
            BC[f].append(Bb * Cb)
    return w, det, BC


def moments(BC):
    """the 7-form and the 5-form moment tables to degree 8 (gfmom_lists, no *_series)"""
    return fixz(gfmom_lists([BC[i] for i in F7], 8), 7), fixz(gfmom_lists([BC[i] for i in F5], 8), 5)


def tables(N, al):
    """(w, det Q, [E P: the 16 untilted families], det Q_t, [E_t P: the 4 tilted families]) at al; (E P2^2)^2 is the square of E P2^2, and
    E G1^2 E H1^2 is the product of the E G1^2 and E H1^2 values (the hypercontractive tail term)"""
    w, det, BC = bc_at(N, al, Q1_block, Qmat1)
    m7, m5 = moments(BC)
    eu = [pe(P, m7) for P in P7_U] + [pe(P, m5) for P in P5_U]
    eu.append(eu[IP2SQ] * eu[IP2SQ])
    eu.append(eu[IG1SQ] * eu[IH1SQ])
    wt, dett, BCt = bc_at(N, al, Qt_block, Qt_full)
    m7t, m5t = moments(BCt)
    et = [pe(P, m7t) for P in P7_T] + [pe(P, m5t) for P in P5_T]
    return w, det, eu, dett, et


def ev_node(N, al):
    """the 20 node values w det^{-1/2} E P (real parts), untilted with det Q, tilted with det Q_t"""
    w, det, eu, dett, et = tables(N, al)
    a = w * posre(det, 'det Q').rsqrt()
    at = w * posre(dett, 'det Q_t').rsqrt()
    return [(a * x).real for x in eu] + [(at * x).real for x in et]

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



def node_parts():
    K = M_ // 2
    h = (K + 1) // 2
    return {'nodes0': list(range(0, h)), 'nodes1': list(range(h, K + 1))}


def run_nodes(N):
    """the TW nodes al = 2 pi k / M of this item, C-EVEN at one of them (al and 2 pi - al), and the N = 3 reflection in nodes0"""
    ks = node_parts()[PART]
    keep = {}
    for k in ks:
        STAGE[0] = 'node %d' % k
        keep[k] = ev_node(N, acb(PI * (2 * k) / M_))
        out(node_line(str(k), keep[k]))
    k = ks[0] if ks[0] > 0 else ks[1]
    STAGE[0] = 'C-EVEN'
    mir = ev_node(N, acb(PI * (2 * (M_ - k)) / M_))
    out('CHECK C-EVEN k=%d %s' % (k, 'PASS' if all(x.overlaps(y) for x, y in zip(keep[k], mir)) else 'FAIL'))
    if PART == 'nodes0' and N == 3:
        STAGE[0] = 'reflection'
        out(node_line('refl', ev_node(N, None)))


# ------------------------------------------------------------------ G on Im al = SIG (px08_m2bc4's method, l.952-1113, on Q and Q_t together)
def det_lower(N, u0, u1, y, blockfn, plant=False):
    """an exact lower bound of |det| on the box for blockfn (Q1_block or Qt_block): the minimum over G_DSUB sub-boxes of prod_b
    abs_lower(det of the block); a block det that is not finite counts as 0. plant=True (PLANT-DET) widens the first block det of the
    first sub-box to contain 0"""
    lo = None
    for i in range(G_DSUB):
        al = acb(xball(u0 + (u1 - u0) * i / G_DSUB, u0 + (u1 - u0) * (i + 1) / G_DSUB), y)
        p = arb(1)
        for b, (kap, kapT) in enumerate(comps(N, al)):
            d = blockfn(kap, kapT).det()
            if plant and i == 0 and b == 0:
                d = acb(d.real.union(arb(0)), d.imag.union(arb(0)))
            p = p * (d.abs_lower() if d.is_finite() else arb(0))
        p = p.lower()
        lo = p if (lo is None or p < lo) else lo
    return lo


def prefactor(N, u0, u1, y, blockfn, plant=False):
    """a = |w| det_lower^{-1/2} on the box, an exact upper end; None (the box bound is not finite) when the det bound is 0"""
    dlo = det_lower(N, u0, u1, y, blockfn, plant)
    if not (dlo > 0):
        return None
    a = (kw(N, acb(xball(u0, u1), y))[1].abs_upper() / dlo.sqrt()).upper()
    return a if a.is_finite() else None


def eval_box(N, u0, u1, y, plant=False):
    """the 20 family bounds a |E P| on the box (untilted with det Q, tilted with det Q_t), or None when one is not finite"""
    a = prefactor(N, u0, u1, y, Q1_block, plant)
    at = prefactor(N, u0, u1, y, Qt_block)
    if a is None or at is None:
        return None
    try:
        w, det, eu, dett, et = tables(N, acb(xball(u0, u1), y))
    except (ZeroDivisionError, ValueError):
        return None
    g = [(a * x.abs_upper()).upper() for x in eu] + [(at * x.abs_upper()).upper() for x in et]
    return g if all(z.is_finite() for z in g) else None


def caps_from_tm(TM):
    """cap_i = TOLV_i |T_M,i| (e^{SIG M} - 1)/2, as exact lower ends"""
    f = ((arb(SIG) * M_).exp() - 1) / 2
    return [(TOLV[i] * TM[i].abs_lower() * f).lower() for i in range(NV)]


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
    return hd[0] == 'px08_a2cert_v1' and hd[2] == me and hd[3] == 'ITEM=' + MODE and hd[6] == 'SIGC=' + SIGC and hd[4] in parts


def node_caps(N, man):
    """T_M from the two node partials of this file at this SIGC (paths and sha256 in man; header and PART-DONE checked), and the caps"""
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


def g_loop(N, a0, a1, y, k, caps=None, plant=False, emit=True):
    """k boxes of width (a1 - a0)/k pi on Im al = y, in x order; a box is replaced in place by its halves while it fails or (caps given)
    a family bound exceeds its cap, to depth G_DEPTH; a box at depth G_DEPTH is kept whatever its bound. G-STOP: a failure at depth
    G_DEPTH, or more than G_MAXEV evaluations in this item. Returns (boxes, failed evaluations, evaluations)"""
    todo = [(a0 + (a1 - a0) * i / k, a0 + (a1 - a0) * (i + 1) / k, 0) for i in range(k)]
    nbox = nfail = nev = 0
    while todo:
        if nev >= G_MAXEV:
            raise NotCert('G-STOP: more than %d evaluations in this item' % G_MAXEV)
        u0, u1, d = todo.pop(0)
        nev += 1
        STAGE[0] = 'G box %s %s' % (u0, u1)
        g = eval_box(N, u0, u1, y, plant)
        if g is None:
            nfail += 1
            if emit:
                out('BOXFAIL %s %s depth %d' % (u0, u1, d))
            if d >= G_DEPTH:
                raise NotCert('G-STOP: box [%s, %s] pi failed at depth %d' % (u0, u1, d))
        if g is None or (caps is not None and d < G_DEPTH and any(not (g[i] <= caps[i]) for i in range(NV))):
            um = (u0 + u1) / 2
            todo = [(u0, um, d + 1), (um, u1, d + 1)] + todo
            continue
        nbox += 1
        if emit:
            out('BOX %s %s %s' % (u0, u1, ' '.join(ex(z) for z in g)))
    return nbox, nfail, nev


def run_g(N):
    a0, a1 = G_E[PART]
    y = arb(SIG)
    TM, caps = node_caps(N, sys.argv[5])
    out('CAPS N=%d (TOLV |T_M| (e^{%g M} - 1)/2, M = %d): %s' % (N, SIG, M_, ', '.join('%s %s' % (nm, updec(c)) for nm, c in zip(NAMES, caps))))
    STAGE[0] = 'PLANT-DET'
    try:
        g_loop(N, a0, a0 + (a1 - a0) / G_K, y, 1, plant=True, emit=False)
        fired = False
    except NotCert as stop:
        fired = str(stop).startswith('G-STOP')
    out('CHECK PLANT-DET %s' % ('FIRED' if fired else 'DID-NOT-FIRE'))
    if not fired:
        raise NotCert('PLANT-DET did not fire')
    nbox, nfail, nev = g_loop(N, a0, a1, y, G_K, caps)
    out('GSTAT %s: %d boxes, %d failed, %d evaluations (Im al = %g; value split on all %d families; %d det sub-boxes)' % (
        PART, nbox, nfail, nev, SIG, NV, G_DSUB))
    if PART == 'g0':
        STAGE[0] = 'C-CONJ'
        vals = []
        for s in (1, -1):
            w, det, eu, dett, et = tables(N, acb(PI / 3, s * arb(SIG)))
            a = w * posre(det, 'det Q').rsqrt()
            at = w * posre(dett, 'det Q_t').rsqrt()
            vals.append([a * x for x in eu] + [at * x for x in et])
        out('CHECK C-CONJ %s' % ('PASS' if all(x.overlaps(z.conjugate()) for x, z in zip(*vals)) else 'FAIL'))

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



# ------------------------------------------------------------------ C-PROP (px08_m2bc4 l.1152-1190 on four matrix families), the ladder, cov
PROP_NAMES = {'t': 'Q_t = Q - 2 T(1/300, 9/20)', 0: 'Q - 2 (lam_XT/theta2) B_XT', 1: 'Q - 2 (lam_XB/theta2) B_XB',
              2: 'Q - 2 (lam_Z/theta2) B_Z'}


def q_real(N, al, which):
    """the full real matrix of family which ('t': Q_t; v = 0, 1, 2: Q - 2 (lam_v/theta2) B_v) at a real al (an arb point or interval),
    or at the N = 3 reflection (al None), as rows of arb (real parts)"""
    k = kw(N, None)[0] if al is None else kw(N, acb(al))[0]
    Mx = Qt_full(k) if which == 't' else Qmat1(k) - forms1(k)[which] * acb(2 * LAM[which] / THETA2)
    return [[Mx[i, j].real for j in range(Mx.ncols())] for i in range(Mx.nrows())]


def c_prop(N, which):
    """C-PROP: interval LDL^T of family which on al-intervals tiling [0, pi] (PROP_K of them, halved on failure), and at the N = 3
    reflection. Stop rule: an interval that fails at depth PROP_DEPTH, or more than PROP_MAXEV LDL^T evaluations, ends C-PROP as FAIL.
    Returns (ok, intervals, smallest pivot lower end, the interval (u0, u1) where it occurs, or the reason of the stop)"""
    todo = [(Fr(i, PROP_K), Fr(i + 1, PROP_K), 0) for i in range(PROP_K)]
    nint, nev, dmin, where = 0, 0, None, None
    while todo:
        if nev >= PROP_MAXEV:
            return False, nint, dmin, 'PROP-STOP: more than %d evaluations' % PROP_MAXEV
        u0, u1, d = todo.pop()
        nev += 1
        D = ldlt(q_real(N, xball(u0, u1), which))
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
    if N == 3 and ldlt(q_real(N, None, which)) is None:
        return False, nint, dmin, 'the reflection failed'
    return True, nint, dmin, where


def plant_prop(N, where, which):
    """PLANT-PROP: at the midpoint al* of the interval with the smallest pivot, c = min_j (upper end of pivot j) >= d_min >= lambda_min,
    so the matrix at al* minus 2 c I has lambda_min - 2 c <= -lambda_min < 0; its LDL^T must fail. True when it fails as it must"""
    u = (where[0] + where[1]) / 2
    A = q_real(N, PI * u.numerator / u.denominator, which)
    D = ldlt(A)
    if D is None:
        return False
    c = D[0].upper()
    for x in D[1:]:
        c = x.upper() if x.upper() < c else c
    return ldlt([[A[i][j] - (2 * c if i == j else 0) for j in range(len(A))] for i in range(len(A))]) is None


def blockdet(N, al, blockfn):
    d = acb(1)
    for (kap, kapT) in comps(N, al):
        d = d * blockfn(kap, kapT).det()
    return d


def det_both(N, al):
    return [blockdet(N, al, Q1_block), blockdet(N, al, Qt_block)]


def plant_strip(N, sig):
    """m1c's PLANT-STRIP on det Q_t: F_p' = det Q_t (cosh(c sigma) - cos al), c = 3/4, negative at al = i (1 + c) sigma / 2: the cover
    must fail"""
    c = arb(3) / 4
    ch = (c * arb(sig)).cosh()
    fp = lambda N_, al: [blockdet(N_, al, Qt_block) * (ch - al.cos())]
    neg_ok = fp(N, acb(0, (1 + c) * arb(sig) / 2))[0].real < 0
    ok, nb, bad = cover(N, sig, fp, CDMAX)
    return neg_ok and ok is False and bad is not None


def prop_line(N, which):
    t0 = cpu()
    ok, nint, dmin, where = c_prop(N, which)
    wh = ('[%s, %s]' % where) if isinstance(where, tuple) else str(where)
    out('C-PROP N=%d (%s, interval LDL^T): %s, %d al-intervals tiling [0, pi], hence all of [0, 2 pi) (k(2 pi - al) = P k(al) P with P '
        '= diag(1, -1) or diag(1, -1, 1), so each family at 2 pi - al is (I_3 (x) P)-similar to the one at al)%s; smallest pivot >= %s on '
        'x in %s pi (%.1f s)' % (
        N, PROP_NAMES[which], 'PASS' if ok else 'FAIL', nint, ' and the reflection' if N == 3 else '',
        dndec(dmin) if dmin is not None else '-', wh, cpu() - t0))
    return ok, where


def run_cov(N):
    for which in ('t', 0, 1, 2):
        STAGE[0] = 'C-PROP %s' % which
        ok, where = prop_line(N, which)
        if not ok:
            raise NotCert('C-PROP failed (%s)' % PROP_NAMES[which])
        out('CHECK PLANT-PROP %s' % ('FIRED' if plant_prop(N, where, which) else 'DID-NOT-FIRE'))
    STAGE[0] = 'cover ladder'
    t0 = cpu()
    sig, nb, tc = ladder(N, (0.5, 0.375, 0.25), det_both, CDMAX)
    out('COVER N=%d Re det Q > 0 and Re det Q_t > 0: %s (%d boxes, %.1f s)' % (
        N, ('certified at sigma %g, M = %d' % (sig, SIG_LADDER[str(sig)])) if sig else 'no sigma of the ladder certified', nb, cpu() - t0))
    if sig:
        out('CHECK PLANT-STRIP %s' % ('FIRED' if plant_strip(N, sig) else 'DID-NOT-FIRE'))
    STAGE[0] = 'table timing'
    t0 = cpu()
    tables(N, acb(arb(7) / 10))
    out('TIMING N=%d: one point (untilted and tilted tables) %.1f s' % (N, cpu() - t0))

# ==== COPY px08_m2bc4.py:6527d21b l.1204-1210 BEGIN ====
def dndec(x, sig=12):
    """a decimal string <= x (W1), from the exact lower end"""
    m, e = x.lower().man_exp()
    u = Fr(int(m)) * Fr(2) ** int(e)
    if u == 0:
        return '0'
    return _dec(u, sig, True) if u > 0 else '-' + _dec(-u, sig, False)
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1239-1266 BEGIN ====
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
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1286-1290 BEGIN ====
def k_np_of(N, al):
    if al is None:
        return np.array([[1.0, 0.0], [0.0, -1.0]])
    c, s = math.cos(al), math.sin(al)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]) if N == 4 else np.array([[c, -s], [s, c]])
# ==== COPY END ====


# ==== COPY px08_m2bc4.py:6527d21b l.1487-1489 BEGIN ====
def tiling_ok(keys, x0, x1):
    ks = sorted(keys)
    return bool(ks) and ks[0][0] == x0 and ks[-1][1] == x1 and all(ks[i][1] == ks[i + 1][0] for i in range(len(ks) - 1))
# ==== COPY END ====



# ------------------------------------------------------------------ the controls of the assembly item
def c_port(N, plant=None):
    """C-PORT: Qmat1, forms1 and tilt1 (t = 1/300, eps 9/20) against twlib's Qmat, forms and tilt entrywise (<= PORT_TOL max(1, |f|)) at
    al = 0.7, 2.3 and the N = 3 reflection, and pref_arb(N) against twlib.pref(N) (relative <= 1e-12). plant 'B' moves one a3T entry,
    'T' one tilt entry, 'P' pref, each by about 1e-10 or more (PLANT-PORT-B, -T, -P)"""
    worst = 0.0
    for al in [0.7, 2.3] + ([None] if N == 3 else []):
        k = kw(N, None)[0] if al is None else kw(N, acb(al))[0]
        kn = k_np_of(N, al)
        pairs = [(Qmat1(k), TL.Qmat(kn))] + list(zip(forms1(k), TL.forms(kn))) + [(tilt1(k, T_, EPS_), TL.tilt(kn, T_F, A_F, A_F, EPS_F))]
        for idx, (Ma, Mf) in enumerate(pairs):
            for i in range(Ma.nrows()):
                for j in range(Ma.ncols()):
                    a = Ma[i, j]
                    if (plant == 'B' and idx == 5 or plant == 'T' and idx == len(pairs) - 1) and (i, j) == (0, 0):
                        a = a + acb(arb('1e-10'))
                    worst = max(worst, float((a - acb(float(Mf[i, j]))).abs_upper()) / max(1.0, abs(float(Mf[i, j]))))
    pa, pf = pref_arb(N), TL.pref(N)
    if plant == 'P':
        pa = pa * (1 + arb('1e-9'))
    rel = float((pa - pf).abs_upper()) / abs(pf)
    return worst <= PORT_TOL and rel <= 1e-12, max(worst, rel)


def c_series(plant=False):
    """C-SERIES: the exact H1, H2 against twlib's H1, H2, and P2, GE against the same built from twlib's polynomials and twrig4's f0, f1, f2
    (l.19-21) with g0 = f0^2, g1 = 2 f0 f1, g2 = f1^2 + 2 f0 f2: equal monomial sets and |a - f| <= SER_TOL max(1, |f|) per coefficient
    (twlib's coefficients are exact binary fractions). plant=True (PLANT-SERIES) moves one H2 coefficient by 2^-40"""
    tp2 = TL.padd(TL.H2, TL.pscale(TL.pmul(TL.H1, TL.H1), 0.5))
    f0, f1, f2 = {TL.mono(XT=1): 0.5}, {TL.mono(XT=2): 1 / 8}, {TL.mono(XT=3): 1 / 16}
    g0 = TL.pmul(f0, f0)
    g1 = TL.pscale(TL.pmul(f0, f1), 2.0)
    g2 = TL.padd(TL.pmul(f1, f1), TL.pscale(TL.pmul(f0, f2), 2.0))
    tge = [g0, TL.padd(g1, TL.pmul(g0, TL.H1)), TL.padd(g2, TL.pmul(g1, TL.H1), TL.pmul(g0, tp2))]
    mine = [H1, dict(H2), P2] + GE
    if plant:
        e0 = sorted(H2)[0]
        mine[1][e0] = H2[e0] + Fr(1, 2 ** 40)
    worst = 0.0
    for A, F in zip(mine, [TL.H1, TL.H2, tp2] + tge):
        Fz = {e: c for e, c in F.items() if c != 0}
        if set(A) != set(Fz):
            return False, float('inf')
        for e in A:
            worst = max(worst, abs(float(A[e]) - Fz[e]) / max(1.0, abs(Fz[e])))
    return worst <= SER_TOL, worst


def c_kg(plant=False):
    """C-KG: K_G = (phi(a)^2 - d_0 - d_1 a - d_2 a^2)/a^3 with phi(a) = (1 - sqrt(1 - a))/a and d_0, d_1, d_2 the first coefficients of
    phi^2 = sum_k d_k u^k (every d_k >= 0, as the coefficients of 1 - sqrt(1 - u) are > 0); (d_0, d_1, d_2) must equal the exact G0, G1, G2
    (one X_T power each, G = X_T^2 phi(t X_T)^2) and K_G must be > 0. Then 0 <= G - G0 - t G1 - t^2 G2 <= K_G t^3 X_T^5 on Omega.
    plant=True (PLANT-KG) uses d_2 = 1/16, which this test must reject"""
    d = [Fr(1, 4), Fr(1, 8), Fr(1, 16) if plant else Fr(5, 64)]
    ok = len(G0) == len(G1) == len(G2) == 1 and d == [G0.get(m1(XT=2)), G1.get(m1(XT=3)), G2.get(m1(XT=4))]
    phi = (1 - (1 - A_).sqrt()) / A_
    KG = (phi * phi - fr2a(d[0]) - fr2a(d[1]) * A_ - fr2a(d[2]) * A_ * A_) / A_ ** 3
    return ok and KG > 0, KG


def c_block(N, plant=False):
    """C-BLOCK: at al = 0.7, 2.3 and the complex point 0.3 + 0.2i (off the axis kapT = 1/kap differs from conj(kap)), the products of the
    Q and Q_t block dets against the full dets, and E H1^2 (7-form table to degree 4) from the Q_t blocks against the full Q_t; each
    pair must overlap, with radii <= 1e-20 relative. plant=True (PLANT-BLOCK) moves one T1_block entry of the first block by 1e-10"""
    ok = True
    h1sq = proj(to_arb_fr(pmul(H1, H1)), F7)
    for al in (acb(arb(7) / 10), acb(arb(23) / 10), acb(arb(3) / 10, arb(2) / 10)):
        k = kw(N, al)[0]
        d1, dt, BC = acb(1), acb(1), [[] for _ in range(NF)]
        for b, (kap, kapT) in enumerate(comps(N, al)):
            d1 = d1 * Q1_block(kap, kapT).det()
            Qb = Qt_block(kap, kapT, plant and b == 0)
            dt = dt * Qb.det()
            Cb = Qb.inv()
            for f, Bb in enumerate(B1_blocks(kap, kapT)):
                BC[f].append(Bb * Cb)
        Qt = Qt_full(k)
        C = Qt.inv()
        Bf = forms1(k)
        mb = fixz(gfmom_lists([BC[i] for i in F7], 4), 7)
        mf = fixz(gfmom_lists([[Bf[i] * C] for i in F7], 4), 7)
        for x, z in ((d1, Qmat1(k).det()), (dt, Qt.det()), (pe(h1sq, mb), pe(h1sq, mf))):
            tight = zrad(x) <= x.abs_lower() / 10 ** 20 and zrad(z) <= z.abs_lower() / 10 ** 20
            ok = ok and tight and x.overlaps(z)
    return ok


def zrad(z):
    return z.real.rad().max(z.imag.rad())


def flt_polys():
    """the 18 family polynomials as float dicts on the nine forms (exact ones from Fractions, hbar ones from arb midpoints); the two node
    products are formed from the values"""
    fl = lambda P: {e: float(c) for e, c in P.items()}
    fa = lambda P: {e: float(c.mid()) for e, c in P.items()}
    return [fl(P) for nm, P in FAM_U7] + [fa(P) for nm, P in FAM_U5], [fl(P) for nm, P in FAM_T7] + [fa(P) for nm, P in FAM_T5]


def c_flt(N, plant=False):
    """C-FLT: the 20 E P values at al = 0.7 and 2.3 against pk10's float GFMom (gfmom.py, degree 8 on all nine forms) on twlib's Qmat,
    forms and Qmat - 2 tilt(k, 1/300, 0.25, 0.25, 0.45), each value against itself: |a - f| <= FLT_TOL |f|, the node products formed from the
    float values. plant=True (PLANT-FLT) multiplies the E GE0 value by 1 + 1e-7, which this test must reject"""
    PU, PT = flt_polys()
    ratio = [0.0] * NV
    for al in (0.7, 2.3):
        kn = k_np_of(N, al)
        Qf, Bsf = TL.Qmat(kn), TL.forms(kn)
        g = GFMom(Bsf, np.linalg.inv(Qf), 8)
        fv = [g.E(P) for P in PU]
        fv.append(fv[IP2SQ] ** 2)
        fv.append(fv[IG1SQ] * fv[IH1SQ])
        gt = GFMom(Bsf, np.linalg.inv(Qf - 2 * TL.tilt(kn, T_F, A_F, A_F, EPS_F)), 8)
        fv += [gt.E(P) for P in PT]
        w, det, eu, dett, et = tables(N, acb(al))
        av = [float(x.real.mid()) for x in eu + et]
        if plant:
            av[1] *= 1 + 1e-7
        ratio = [max(r, abs(a - f) / abs(f)) for r, a, f in zip(ratio, av, fv)]
    if not plant:
        out('C-FLT ratios N=%d (largest |a - f|/|f| at al = 0.7, 2.3): %s' % (N, ', '.join('%s %.2e' % (nm, r) for nm, r in zip(NAMES, ratio))))
    worst = max(ratio)
    return worst <= FLT_TOL, worst


def c_hbar(plant=False):
    """C-HBAR: the arb hbar_j (j = 2, 3) against twlib.hbar(j, 0.25, 0.25): equal monomial sets and |a_mid - f| <= HBAR_TOL (|f| + S_d),
    S_d the largest |f| of the same total degree. plant=True (PLANT-HBAR) adds 1e-9 (|a| + S_d) to one hbar2 coefficient"""
    worst = 0.0
    for j, HB in ((2, HB2), (3, HB3)):
        F = TL.hbar(j, A_F, A_F)
        A = dict(HB)
        Sd = {}
        for e, c in F.items():
            Sd[sum(e)] = max(Sd.get(sum(e), 0.0), abs(c))
        if plant and j == 2:
            e0 = sorted(A)[0]
            A[e0] = A[e0] + arb('1e-9') * (abs(A[e0]) + Sd.get(sum(e0), 1.0))
        if set(A) != set(F):
            return False, float('inf')
        for e in A:
            worst = max(worst, abs(float(A[e].mid()) - F[e]) / (abs(F[e]) + Sd[sum(e)]))
    return worst <= HBAR_TOL, worst


def c_hhat(plant=False):
    """C-HHAT: (1) every monomial of hbar2 has total degree 2 or 3, so the trading map covers it; (2) hhat equals the
    image of (t/2) hbar2 under the trading map (twrig4 l.36-43: degree 2 times t/2; degree 3 loses one Z, else one X_T, else one X_B,
    with factor aZ or a over 2), recomputed here in floats from twlib.hbar(2, 0.25, 0.25): equal monomial sets and |a_mid - f| <=
    HBAR_TOL (|f| + S). Every monomial of hbar2 is a product of X, Z, W >= 0 with a positive coefficient, so the image majorizes
    (t^2/2) hbar2 on Omega monomial by monomial. plant=True (PLANT-HHAT) halves one hhat coefficient"""
    F = TL.hbar(2, A_F, A_F)
    if any(sum(e) not in (2, 3) for e in list(F) + list(HB2)) or any(not (c > 0) for c in HB2.values()):
        return False, float('inf')
    img = {}
    for e, c in F.items():
        e2, fac = list(e), T_F
        if sum(e) == 3:
            v = 'Z' if e2[TL.IX['Z']] > 0 else ('XT' if e2[TL.IX['XT']] > 0 else 'XB')
            e2[TL.IX[v]] -= 1
            fac = A_F
        img[tuple(e2)] = img.get(tuple(e2), 0.0) + c * fac / 2
    A = dict(HH)
    if plant:
        e0 = sorted(A)[0]
        A[e0] = A[e0] / 2
    if set(A) != set(img):
        return False, float('inf')
    S = max(abs(c) for c in img.values())
    worst = max(abs(float(A[e].mid()) - img[e]) / (abs(img[e]) + S) for e in img)
    return worst <= HBAR_TOL, worst


SCAN_SHARED = {'I[F0^2]': 'GE0', 'I[P2^2]': 'P2^2', 'I[H1^2]': 'H1^2', 'I[(E P2^2)^2]': '(E P2^2)^2', 'I_t[H1^4]': 'H1^4',
               'I_t[hhat^4]': 'hhat^4'}


def c_scan(N, Ival, slack, plant=False):
    """C-SCAN (a gross-error check of the families and the normalization, not part of the bound): the certified integrals that TRB's dry run
    also printed (px08_trbscan_v2 INTEGRALS line, twrig4's 32-point rule, 7 digits; I[GE0] = I[F0^2] since G0 = F0^2) against those floats:
    |mid - f| <= SCAN_TOL |f| + rad + slack_i (rad = the certified radius, TW error included; slack_i = 2 PR errh_i with errh_i the 32-node TW
    error bound of C-HALF, as TRB); and I[1] against twrig4's 'lead (no insertion)' (9 digits), relative <= LEAD_TOL. plant=True (PLANT-SCAN)
    moves the certified I[GE0] by 1e-1. Returns (ok, worst excess ratio, lead ratio, count)"""
    lines = open(SOURCES['scan_n%d' % N][0]).read().split('\n')
    integ = [x for x in lines if x.startswith('INTEGRALS N=%d ' % N)]
    lead = [x for x in lines if x.startswith('# twrig4:') and 'lead (no insertion)' in x]
    if len(integ) != 1 or len(lead) != 1:
        return False, float('inf'), float('inf'), 0
    pairs = re.findall(r'(I(?:_t)?\[[^\]]*\]) ([-+0-9.e]+)', integ[0])
    got = dict(Ival)
    if plant:
        got['GE0'] = got['GE0'] * (1 + arb('1e-1'))
    worst, n = 0.0, 0
    for lab, val in pairs:
        if lab not in SCAN_SHARED:
            continue
        nm = SCAN_SHARED[lab]
        f = float(val)
        worst = max(worst, (abs(float(got[nm].mid()) - f) - float(got[nm].rad()) - float(slack[nm])) / abs(f))
        n += 1
    fl = float(re.search(r'lead \(no insertion\) ([0-9.]+)', lead[0]).group(1))
    lrel = abs(float(got['1'].mid()) - fl) / fl
    return n == len(SCAN_SHARED) and worst <= SCAN_TOL and lrel <= LEAD_TOL, worst, lrel, n


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


def c_rank(N, plant=False):
    """C-RANK: for v = X_T, X_B, Z the full B_v (forms1, at al = 0.7 and at the N = 3 reflection) is E_vv (x) I_d exactly: d = N - 1
    nonzero entries, at (v d + p, v d + p), each equal to 1. So rank B_v = d, which the Chernoff bound T_v <= (1 - theta2)^{-d/2} I[1]
    uses. plant=True (PLANT-RANK) adds one off-diagonal 1 to B_Z, which this test must reject"""
    d = N - 1
    for al in [0.7] + ([None] if N == 3 else []):
        k = kw(N, None)[0] if al is None else kw(N, acb(al))[0]
        Bs = forms1(k)
        for v in range(3):
            B = Bs[v] * 1
            if plant and v == 2:
                B[0, 3 * d - 1] = 1
            nz = sorted((i, j) for i in range(B.nrows()) for j in range(B.ncols()) if not B[i, j].is_zero())
            if nz != [(v * d + p, v * d + p) for p in range(d)] or not all(B[i, j] == 1 for i, j in nz):
                return False
    return True


def multiset_ok(checks):
    """C-MULTISET: the partial items printed exactly their CHECK lines (C-EVEN per node item, C-CONJ once, PLANT-DET per G item)"""
    return sorted(c for c, r in checks) == sorted(['C-CONJ'] + ['C-EVEN'] * len(node_parts()) + ['PLANT-DET'] * len(G_E))


# ------------------------------------------------------------------ the assembly item
def read_parts(N, man):
    """the ten partial outputs (2 node, 8 G; paths and sha256 in man), all of this file at this SIGC"""
    nodes, refl, boxes, checks, seen = {}, [None], [], [], []
    for line in open(man):
        h, p = line.split()
        assert sha_file(p) == h, 'sha mismatch %s' % p
        lines = open(p).read().split('\n')
        assert header_ok(lines[0].split(), list(node_parts()) + list(G_E)), 'header %s' % p
        seen.append(lines[0].split()[4])
        assert any(x.strip() == 'VERDICT PART-DONE' for x in lines), 'not done %s' % p
        node_parse(lines, nodes, refl)
        for x in lines:
            w_ = x.split()
            if w_ and w_[0] == 'BOX':
                g = [unex(w_[i], w_[i + 1]) for i in range(3, len(w_), 2)]
                assert len(g) == NV
                boxes.append(((Fr(w_[1]), Fr(w_[2])), g))
            elif w_ and w_[0] == 'CHECK':
                checks.append((w_[1], w_[-1]))
    assert sorted(seen) == sorted(list(node_parts()) + list(G_E)), seen
    assert sorted(nodes) == list(range(M_ // 2 + 1)) and (refl[0] is not None) == (N == 3)
    keys = [k for k, g in boxes]
    assert len(set(keys)) == len(keys) and tiling_ok(keys, 0, 1), 'box tiling of [0, 1]'
    return nodes, refl[0], sorted(boxes), checks


def control(name, res, fails, fires, plant_res):
    """print one control line, record a failure, and record its plant (plant_res True = the plant failed the test, as it must)"""
    ok = res[0] if isinstance(res, tuple) else res
    out('%s: %s%s' % (name, 'PASS' if ok else 'FAIL', (' (worst %.3e)' % res[1]) if isinstance(res, tuple) and len(res) > 1 else ''))
    if not ok:
        fails.append(name.split()[0])
    fires.append(('PLANT-' + name.split()[0][2:], plant_res))


def run_asm(N):
    fails, fires = [], []
    K = M_ // 2
    nodes, refl, boxes, checks = read_parts(N, sys.argv[5])
    keys = [k for k, g in boxes]
    out('PARTITION N=%d: nodes 0..%d once each, reflection %s, %d G boxes tiling [0, 1] pi: PASS' % (N, K, 'yes' if refl else 'no', len(boxes)))
    fires.append(('PLANT-TILE', not tiling_ok(keys[1:], 0, 1)))
    ok = multiset_ok(checks)
    out('C-MULTISET N=%d (C-EVEN per node item, C-CONJ once, PLANT-DET per G item): %s' % (N, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-MULTISET')
    fires.append(('PLANT-MULTISET', not multiset_ok([c for c in checks if c[0] != 'C-CONJ'])))
    for c, r in checks:
        out('%s (partial item): %s' % (c, r))
        if r != ('FIRED' if c == 'PLANT-DET' else 'PASS'):
            fails.append(c)
    ok, info = c_copy()
    out('C-COPY (every COPY block = its source lines, byte for byte): %s, %s' % ('PASS' if ok else 'FAIL', info))
    if not ok:
        fails.append('C-COPY')
    fires.append(('PLANT-COPY', not c_copy(True)[0]))
    for which in ('t', 0, 1, 2):
        STAGE[0] = 'C-PROP %s' % which
        ok, where = prop_line(N, which)
        if not ok:
            fails.append('C-PROP(%s)' % which)
        fires.append(('PLANT-PROP(%s)' % which, ok and plant_prop(N, where, which)))
    STAGE[0] = 'C-COVER'
    sig, nb, tc = ladder(N, (SIG,), det_both, CDMAX)
    out('C-COVER N=%d Re det Q > 0 and Re det Q_t > 0 at sigma %g: %s (%d boxes)' % (N, SIG, 'PASS' if sig else 'FAIL', nb))
    if not sig:
        fails.append('C-COVER')
    fires.append(('PLANT-STRIP', plant_strip(N, SIG)))
    TM = tm_of(nodes)
    TH = [(nodes[0][i] + nodes[K][i] + 2 * sum((nodes[k][i] for k in range(2, K, 2)), arb(0))) * 2 / M_ for i in range(NV)]
    caps = caps_from_tm(TM)

    def stop_ok(k, g):
        return k[1] - k[0] <= Fr(1, 128) or all(g[i] <= caps[i] for i in range(NV))
    ok = all(stop_ok(k, g) for k, g in boxes)
    out('C-REFINE N=%d (every box of width pi/128 or within the caps): %s' % (N, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-REFINE')
    gp = list(boxes[0][1])
    gp[0] = caps[0] * 2 + 1
    fires.append(('PLANT-REFINE', not stop_ok((Fr(0), Fr(1, 32)), gp)))
    G = [maxup([g[i] for k, g in boxes]) for i in range(NV)]
    err = [(2 * G[i] / ((arb(SIG) * M_).exp() - 1)).upper() for i in range(NV)]
    errh = [(2 * G[i] / ((arb(SIG) * (M_ // 2)).exp() - 1)).upper() for i in range(NV)]
    out('G line N=%d: Im al = %g (the boundary line of the C-COVER strip), M = %d, %d boxes' % (N, SIG, M_, len(boxes)))
    half = all((TM[i] + (-err[i]).union(err[i])).overlaps(TH[i] + (-errh[i]).union(errh[i])) for i in range(NV))
    out('C-HALF N=%d: %s' % (N, 'PASS' if half else 'FAIL'))
    if not half:
        fails.append('C-HALF')
    J = [TM[i] + (-err[i]).union(err[i]) + (refl[i] / 2 if N == 3 else 0) for i in range(NV)]
    PR = pref_arb(N)
    Ival = {nm: PR * J[i] for i, nm in enumerate(NAMES)}
    miss = []
    for i, nm in enumerate(NAMES):
        tl = TM[i].abs_lower()
        within = err[i] <= TOLV[i] * tl
        if not within:
            miss.append(nm)
        out('  N=%d I[%s] = %s; G %s, TW error %s, error/|T_M| %s%s' % (N, nm, Ival[nm].str(12), updec(G[i]), updec(err[i]),
                                                                     updec(err[i] / tl) if tl > 0 else 'inf', '' if within else ' TARGET-MISS'))
    out('TARGET N=%d (TW error <= 1e-3 |T_M| for 1, GE0-GE2; <= 1e-1 |T_M| else): %s; misses, reported: %s' % (
        N, 'all within' if not miss else '%d of %d miss' % (len(miss), NV), ', '.join(miss) or 'none'))
    STAGE[0] = 'controls'
    control('C-BLOCK N=%d' % N, c_block(N), fails, fires, not c_block(N, True))
    res = c_port(N)
    control('C-PORT N=%d' % N, res, fails, fires, not c_port(N, 'B')[0])
    fires.append(('PLANT-PORT-T', not c_port(N, 'T')[0]))
    fires.append(('PLANT-PORT-P', not c_port(N, 'P')[0]))
    control('C-SERIES (H1, H2, P2, GE against twlib)', c_series(), fails, fires, not c_series(True)[0])
    control('C-HBAR (per-degree scale)', c_hbar(), fails, fires, not c_hbar(True)[0])
    control('C-HHAT (N-b: hhat = the traded image of (t/2) hbar2)', c_hhat(), fails, fires, not c_hhat(True)[0])
    control('C-FLT N=%d' % N, c_flt(N), fails, fires, not c_flt(N, True)[0])
    slack = {nm: (2 * PR * errh[i]).upper() for i, nm in enumerate(NAMES)}
    ok, w1, w2, n = c_scan(N, Ival, slack)
    out('C-SCAN N=%d (%d certified integrals shared with the dry run, worst %.3e <= %g; I[1] against twrig4 lead, %.3e <= %g): %s' % (
        N, n, w1, SCAN_TOL, w2, LEAD_TOL, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-SCAN')
    fires.append(('PLANT-SCAN', not c_scan(N, Ival, slack, True)[0]))
    pos = all(J[i].upper() > 0 for i in range(NV))
    out('C-POS N=%d (every upper end J_i^+ > 0, before the roots of the reading): %s' % (N, 'PASS' if pos else 'FAIL'))
    fires.append(('PLANT-POS', not all(x.upper() > 0 for x in [arb(0)] + J[1:])))
    out('C-SIGN N=%d (INFO only: s1 = I[GE1]/I[GE0] = %s, s2 = I[GE2]/I[GE0] = %s; main is sign-free, design item 3)' % (
        N, (J[2] / J[1]).str(8), (J[3] / J[1]).str(8)))
    control('C-RANK N=%d (B_v = E_vv (x) I_d for v = X_T, X_B, Z, so rank B_v = d = N - 1, as the Chernoff bound uses)' % N, c_rank(N), fails,
            fires, not c_rank(N, True))
    ok, KG0 = c_kg()
    out('C-KG (K_G = (phi(a)^2 - 1/4 - a/8 - 5 a^2/64)/a^3 = %s > 0; d_0, d_1, d_2 = 1/4, 1/8, 5/64 = the exact G0, G1, G2): %s' % (
        KG0.str(10), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-KG')
    fires.append(('PLANT-KG', not c_kg(True)[0]))
    p = arb(5) / 2 if N == 4 else arb(2)
    ca_ = 1 - (1 - A_).sqrt()
    farok = lambda Jx: p / Jx < ca_ and p / Jx < 1 - (1 - AZ_).sqrt()
    ok = farok(arb(J_))
    out('C-FAR N=%d (far = PR (2J)^2 (2 far_one(a) + far_one(aZ)) ~ J^(p+1) e^{-c J}, p + 1 = %s, decreases for J >= 300 iff (p+1)/300 < '
        'c(a), c(aZ) = %s): %s' % (N, p.str(3), ca_.str(8), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-FAR')
    fires.append(('PLANT-FAR', not farok(arb(5))))
    if not pos:
        out('CHECKS FAIL: %s' % '; '.join(fails + ['C-POS']))
        out('VERDICT INVALID')
        return
    STAGE[0] = 'reading'
    U = {nm: Ival[nm].upper() for nm in NAMES}
    t = T_
    c_a = 1 / (1 + (1 - A_).sqrt())
    q4 = lambda x: x.sqrt().sqrt()
    pos0 = lambda x: x if x > 0 else arb(0)
    KG = KG0.upper()
    main = U['GE0'] + t * pos0(U['GE1']) + t * t * pos0(U['GE2'])
    R3 = (t ** 3 * ((U['G1^2'] * U['P2^2']).sqrt() + (U['G2^2'] * U['H1^2']).sqrt()) + t ** 4 * (U['G2^2'] * U['P2^2']).sqrt()
          + c_a ** 2 * (t ** 3 / 6 * U['X_T^2 hbar3'] + t ** 3 / 2 * (16 * U['G0^2 H1^2'] * U['hbar2^2']).sqrt()
                        + t ** 4 / 8 * U['X_T^2 hbar2^2']))
    Rcub = c_a ** 2 / 6 * q4(U['X_T^8']) * (t * (q4(U['H1^4']) + q4(U['hhat^4']))) ** 3
    RF = t ** 3 * KG * U['X_T^5']
    L2 = (U['G0^2'].sqrt() + t * (U['G1^2'].sqrt() + U['G0^2 H1^2'].sqrt())
          + t * t * (U['G2^2'].sqrt() + 243 * U['E G1^2 E H1^2'].sqrt() + 81 * q4(U['G0^4']) * q4(U['(E P2^2)^2'])))
    Tv = (1 - THETA2) ** (-arb(N - 1) / 2) * U['1']
    chern = sum(((-LAM[v] * J_ * (AZ_ if v == 2 else A_)).exp() * Tv for v in range(3)), arb(0))
    tail = L2 * chern.sqrt()
    far1 = ((2 * arb(J_) / PI).sqrt() if N == 4 else arb(1)) * (-J_ * ca_).exp()
    farZ = ((2 * arb(J_) / PI).sqrt() if N == 4 else arb(1)) * (-J_ * (1 - (1 - AZ_).sqrt())).exp()
    far = PR * (2 * arb(J_)) ** 2 * (2 * far1 + farZ)
    A2 = main + R3 + Rcub + RF + tail + far
    tgt = arb(A2_TARGET[N].numerator) / A2_TARGET[N].denominator
    t2ok = lambda x, c: x.upper() <= c.lower()
    ok = t2ok(A2, tgt)
    out('C-A2T N=%d (gate, D4\'s need: certified A2_%d <= %s): %s; headroom >= %s' % (N, N, updec(tgt, 7), 'PASS' if ok else 'FAIL',
                                                                                    dndec(tgt.lower() - A2.upper())))
    if not ok:
        fails.append('C-A2T')
    fires.append(('PLANT-A2T', not t2ok(A2, tgt / 100)))
    out('REASON main: for every t\' <= t = 1/300, I[GE0] + t\' I[GE1] + t\'^2 I[GE2] <= I[GE0] + t max(I[GE1], 0) + t^2 max(I[GE2], 0) = main, '
        'with no sign condition; its value bounds every J >= 300')
    out('REASON R3: t^3 and t^4 times untilted integrals of fixed polynomials (twlib hbar(j, a, aZ) has no t; G <= c_a^2 X_T^2 on Omega): '
        'nondecreasing in t')
    out('REASON R_cub: Q_t(t\') >= Q_t(1/300) in the Loewner order for t\' <= 1/300 (the t-part t cfun(a_v) of the tilt is PSD), the '
        'integrands X_T^8, H1^4, hhat^4 are >= 0, hhat(t\') <= hhat(1/300) monomialwise, and t^3 grows: nondecreasing in t')
    out('REASON R_F: t^3 K_G I_t[X_T^5] (0 <= G - G0 - t G1 - t^2 G2 <= K_G t^3 X_T^5 on Omega, C-KG), with I_t nondecreasing in t as for '
        'R_cub: nondecreasing in t')
    out('REASON tail: e^{-lam_v J a_v} decreases in J; T_v <= (1 - theta2)^{-d/2} I[1] is free of J (C-PROP, C-RANK); L2 is 1, t, t^2 '
        'times untilted integrals: nonincreasing in J')
    out('REASON far: C-FAR ((p+1)/J < c(a), c(aZ) for J >= 300), so J^(p+1) e^{-c J} decreases in J')
    out('REASON PR: PR = pref_arb(N), a ratio of reduced Laplacian determinants of fixed strip graphs, does not depend on J')
    out('REASON TW: every TW error sits inside the certified J = 300 enclosures; each reason compares exact J-bounds with the exact '
        'J = 300 bound, which the enclosure upper end majorizes')
    out('REASON Z4: each J-bound is the chain\'s at its own Omega(J) and tilt T(1/J) before the comparison, so the comparison is between '
        'valid bounds, pointwise in J')
    out('CHECKS %s' % ('all PASS' if not fails else 'FAIL: ' + '; '.join(fails)))
    out('PLANTS %s' % ' '.join('%s:%s' % (nm, 'FIRED' if f else 'DID-NOT-FIRE') for nm, f in fires))
    valid = not fails and all(f for nm, f in fires)
    out('READING N=%d (t = 1/300, every J >= 300; S4_A2_DESIGN_v1 item 3): A2_%d <= %s; main <= %s, R3 <= %s, R_cub <= %s, R_F <= %s, '
        'tail <= %s, far <= %s; PR <= %s; T_v <= %s; K_G <= %s' % (N, N, updec(A2), updec(main), updec(R3), updec(Rcub), updec(RF),
                                                                   updec(tail), updec(far), updec(PR), updec(Tv), updec(KG)))
    out('VERDICT %s' % ('VALID' if valid else 'INVALID'))


def main():
    N = 4 if MODE == 'n4' else 3
    try:
        if PART == 'cov':
            run_cov(N)
        elif PART in G_E:
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
