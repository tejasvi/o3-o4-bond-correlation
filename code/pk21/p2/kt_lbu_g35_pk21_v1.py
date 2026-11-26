#!/usr/bin/env python3
"""kt_lbu_g35_pk21_v1.py -- pk21 (code/pk21/p2/), Phase 2 item 2 pilot (P_3 x P_5). A copy of pk06/kt_lbu_g34_pk06_v1.py
(sha8 8b7aff00) with three PK21 CHANGES only: this banner line, grid COLS up to 5 (was 4), and TAU_GRID[(3, 5)] = 30305 (the
spanning-tree count of P_3 x P_5 by the matrix-tree theorem, pk21/p2/tau_grid_v1.py, which reproduces the four existing entries).
The rest is byte-identical. pk06 docstring:
kt_lbu_g34_pk06_v1.py -- pk06 (code/pk06/), item P2-13 (short strips, n = 4). A copy of pk01/kt_lbu_v1_1.py (sha8 d3226092,
the engine of the certified 3 x 3 run pk01/out_kt_lbu_v1_1_cert.out, 309fb3fb) with the changes listed under PK06 CHANGES at the end
of this docstring; DIFF_kt_lbu_v1_1_to_g34_pk06_v1.txt is the full diff. The base docstring follows unchanged.
kt_lbu_v1_1.py -- pk01 (code/pk01/). Revision of kt_lbu_v1.py (b1fdda19; frozen, never run, never sent) for the review items of
2026-11-02 (r1 and nits n2, n3, n4, n6, n7, ADD1 39592664) and
the target through the review: with R1 (RV19_65) the uniform problem is the single covariance class (b0, sN) u (b0, sW); orbit O4 first.
The engine of LBU_SPEC_v1 (44974154; manifest 09ff07ae).
Lines 75-719, 863-929, 949-1017 and 1108-1214 of kt_lbu_v1.py are copied verbatim (COPIED_RANGES_KT_LBU_v1_1.txt: ranges and sha256 in
both files); the rest is new or changed.
Object. J^2 Cov(E_e, E_f) = Cov(xi_e, xi_f), xi_x = J (1 - sigma_a.sigma_b), from the four integrals I_F / main, F in {1, xi_e, xi_f,
  xi_e xi_f}, each bounded by PK10 Lemma 19.1 (sec. 19.1; analytic part REVIEWED in RV12_3, its nits L1-L4 adopted) with the three
  changes of the spec: (C1) fixed rational radii a_v = 1 - r_v^2, with rho'^2 > max a_v asserted; (C2) per-vertex Chernoff tails in
  B_tail and B_ann; (C3) the J-free far constant tau(G)^{n/2} (1 - theta)^{-n(V-1)/2}. The error terms are evaluated once at J1 and are
  nonincreasing in J (spec sec. 3); the lower bound Phi (spec sec. 2, vertex form) is evaluated on 64 t-cells covering [0, 1/J1].
Arithmetic. Exact rationals (python-flint 0.9.0 fmpq, fmpq_mat, fmpq_mpoly) for L+, the Gram matrices (untilted and tilted), principal
  minors, the Gaussian moments and every series, majorant and expectation; python-flint arb (prec 256) only for scalars. No python-flint
  *_series type is used anywhere (the review n3): every series is a list of fmpq_mpoly truncated explicitly at t-order K (szero, smul,
  sexp). The moment recursion k M_k = sum_j ((1 - n/2) j - k) D_j M_{k-j} (amom2b's, exact) runs in the quotient ring with Q_e-degree <= 1,
  partner degree <= 1 and X-degree caps per Q-pattern that do not increase with the Q-degree (a monomial ideal closed under the Euler
  operator); every product D_j M_{k-j} is homogeneous, so no term beyond a cap is ever formed (the truncation remark).
(H), exactly as checked (RV12_3 L1; the review r1). Graph.tilt(rates) forms A = B^T (L - 2 diag(rates)) B with B = [e_i - e_{V-1}], a basis
  of 1-perp, and requires every leading principal minor of A to be > 0 (Sylvester); the tilted covariance is B A^{-1} B^T and the
  normalization is ratio^{n/2}, ratio = det(B^T L B) / det A. Per (graph, N, K) build: T1 rates C35 / Jmin on every vertex; T2_v rates
  lambda_v = KAPPA / (2 L+_vv) at v; T3_v rates c'_up / Jmin on every vertex plus lambda'_v = kappa_a / (2 L+_vv) at v (kappa_a = 1/2,
  halved until (H) holds). On P3 x P3 that is 19 tilted Gram matrices per (N, K), each with its own C-H line. C35 >= c(3/5) and
  c'_up >= -log(1 - rho'^2)/(2 rho'^2) are the rational upper bounds used in the tilts and in (H) (the review n7).
The four bound terms as coded (Build.errors), at J1, t1 = 1/J1, radii a_v of sigma:
  B_rem  = t1^{K+1}/(K+1)! N_c (e_0 + e_1 t1 + e_2 t1^2), e_i = E_T1[t^i-part of Dbar_{K+1}] (Lemma 19.1's Dbar with the xi majorants);
  B_tail = sum_{k<=K} t1^k sum_v exp(-lambda_v J1 a_v) N2_v E_T2v[|P_k|], P_k = (F e^H)_k, |P| = P with absolute coefficients;
  B_ann  = sum_v exp(-lambda'_v J1 a_v) N3_v E_T3v[F0'(t1)], F0' the annulus majorant of |F| (radii rho'^2);
  B_far  = (2 J1)^{d_F} tau^{n/2} (1 - th)^{-n(V-1)/2} sum_v exp(-th J1 rho'^2 / (2 L+_vv)), th on k/400 (far_bound), with
           J1 > 2 max L+ d_F / (th rho'^2) asserted (B_far decreases beyond).
The vertex step per t-cell (the review n2). With i_F ranging over the cell box [A_F(cell) - E_F, A_F(cell) + E_F] (A_F
  evaluated with t an arb ball over the cell), phi_scan requires i_1,lo > 0, i_e,lo > 0, i_f,lo > 0, i_ef,lo > 0 and
  2 i_e,lo i_f,lo > i_ef,hi i_1,hi (the whole-box form of n2's inequality), and returns Phi_lo = i_ef,lo / i_1,lo - i_e,hi i_f,hi /
  i_1,lo^2; a cell that fails a condition counts as negative.
Tables per (graph, N, K): T0 untilted, X-degree <= 2K; T1 the common B_rem tilt, caps 2K+6 / 2K+4 / 2K+2; T2_v caps 2K; T3_v caps
  4 / 2 / 0. They do not depend on J1 >= Jmin or on the radii, so the (sigma, J1) grid costs scalar and polynomial work only.
Parameters. JGRID = 50, 55, 60, 65, 70, 75, 80, 90, 100, 110, 120, 135, 150, 175, 200 (Jmin = 50); radii a_v <= min(sigma L+_vv, 3/5)
  with sigma in SIGMAS = 1/4, 1/3, 2/5, 1/2, 3/5; KAPPA = 4/5; rho'^2 = 9801/10000; theta for B_far on the grid k/400.
Modes.
  v1    validation 1: the checks and plants below; reading R-SERIES (exact c2, c3, c4 of J^2 Cov = c2 + c3 t + c4 t^2 + ...) for O1..O5
        and the mirror pairs M1 = (b0, b3), M2 = (b0, b5), at N = 3 and 4.
  v2    validation 2 (sizing): O4 = (b0, sN) at N = 4, K = 3 and 4: every table, the bound terms per F on the (sigma, J1) grid, Phi,
        the smallest certified J1, CPU and peak RSS per step.
  cert  the certificate at order K (third argument, 3..5) for SET (fourth argument): O4 (default; the class (b0, sN) u (b0, sW) by R1)
        or all (O1..O5), at N = 3 and 4: R-J1 per orbit and N (the smallest certified J1 on JGRID, the lower bound L, the bound terms,
        the parameters); C-DATA on O3 when SET = all.
Checks (must PASS) and plants (must FIRE).
  v1    C-SER (w row sums 1/4, symmetric). C-GRAPH (L+ diagonal 13/36, 13/24, 2/9; tau = 192; Foster 8; Delta^2 per orbit as in
        438317a3). C-TREE (P3, K = 5, exact asymptotic series, N = 3, 4) + PLANT-FP (FP coefficient n + 1). C-EXACT (40 random monomials
        of each untilted P3 x P3 table against the alpha-permanent 2^k per_{n/2}, exact; and the monomial X_0^2 explicitly) + PLANT-MOM
        (X_0^2's moment + 1e-20, compared exactly as C-EXACT does). C-GAUSS (a_0's; c2 = (N-1) Delta^2 / 8). C-ROW0
        (the review n4: A_b(0) = 17n/48, A_s(0) = 7n/24, a_1 of F = 1 = 5/6 (N = 3) and 31/64 (N = 4), and A_ef(0), c2, c3 per orbit, exact,
        from the NOTE_SPINWAVE (a4e09eb6) through the REMAINDER_SHEET_LBU_v1 (c6f9cf3e) sec. 3). C-ECON (the review n6: a_k of
        xi_x equal for the rim edges b0, b2, b3, b4, b5 and for the spokes sE, sN, sW, all k <= K). C-R1 (R1, RV19_65: the covariance
        series of O4 and O5, O1 and M1, O2 and M2, O3 and (b1, sE) agree exactly to order K). C-SYM (a second member of each orbit, a_k for
        k <= 2) + PLANT-SYM (O2 against O1). C-H (the P3 x P3 tilts of v2/cert) + PLANT-H (a Chernoff tilt with kappa = 2) + PLANT-H-ANN
        (an annulus tilt with kappa_a = 2; the review r1). C-LIT (below). C-BOUND + PLANT-BOUND (below). PLANT-NEG (a planted dip in Phi is
        reported as negative cells).
  every build with tilts: C-H for each of its tilted Gram matrices; C-EXACT on T1, T2_v0 and T3_v0 (10 monomials each).
  cert, SET = all: C-DATA (O3 at J = 100, 150, 200: the certified bound <= the float data of 438317a3; the central value within 1e-3 of
        it at J = 200).
C-BOUND and PLANT-BOUND parameters. Graph P3 (edges (0, 1), (1, 2)), e = (0, 1), f = (1, 2), F in {1, xi_e, xi_e xi_f};
  K = 4 (PLANT-BOUND: K = 0, B_rem dropped); sigma = 2, so a_v = 1 - r_v^2 with r_v = m/256 the smallest with r_v^2 >= max(1 - 2 L+_vv,
  2/5) (L+ = 5/9, 2/9, 5/9; the radii are printed on the SIGMA line); rho'^2 = 9801/10000; Jmin = 10, so T1 rates C35/10, T2_v
  lambda_v = (4/5)/(2 L+_vv), T3_v c'_up/10 + lambda'_v, with (H) checked for all 7 tilted Gram matrices (C-H lines). At each test J in
  {10, 20, 40} (PLANT-BOUND: 40) the four terms are evaluated with J1 := J; the tables are valid for every J >= Jmin. C-BOUND needs the
  closed form (arb; N = 3 elementary, N = 4 through bessel_i) inside [A_F(1/J) - E_F, A_F(1/J) + E_F] in all 18 enclosures.
C-LIT. The riglap2/pseries/npoly/amom2b are whole-file verbatim copies (line ranges 1..end) in lbu_lit_v1/, sha256-checked at run
  time (C-LIT-COPY). Compared on P3 x P3 with pairs (b0, b4), N = 4: the series (F e^H)_k for F = 1 (k <= 3) and F = xi_e xi_f (k <= 2;
  riglap2 with two 'dot' factors c = 1, shifted by t^2); h_k (k <= 4), Dbar_4 (F = 1) and xibar_l of b0 (l <= 4) at sigma = 1/2,
  t = 1/120; the moments a_k (F = 1, k <= 3) through amom2b in floats. Relative tolerance 1e-12 (moments 1e-10).
Review coverage: the proofs of spec sec. 2 ((C1)-(C3), the vertex step, the insertion paragraph) are reviewed by the review
  (REVIEW_LBU_SPEC_v1_ADD1, 39592664); the code review checks this code against the spec and this header.
Line map: LINEMAP_KT_LBU_v1_1.txt (frozen with this file) maps each spec item to its functions and lines.
CPU. RLIMIT_CPU soft LIM, hard LIM + 2; guard() before each heavy step stops at LIM - 4 s with VERDICT INCOMPLETE. Peak RSS is printed
  after every table and in the summary.
Run (in code/pk01): env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=<own tmp> timeout <LIM+60>
  nice -n 10 prlimit --as=8589934592 --cpu=<LIM+2> -- python3 -I -B kt_lbu_v1_1.py MODE LIM [K [SET]] > <out>
PK06 CHANGES (pk06, 2026-11-11; brief notes/BRIEF_PK06_v1.md, 240b8cd8). The method, the bound terms, the tables, KAPPA,
  RHO2, SIGMAS, C35, the vertex step and every function of the base are unchanged; modes v1, v2 and cert run as before on P3 x P3 (the
  banner now names this file and carries its sha256). Added:
  (g1) mode grid: grid LIM K ROWS COLS N J1 ORBS SIGS [CONTROLS [MEMSTOP]] on P_ROWS x P_COLS (vertex (r, c) = r COLS + c; h<r><c>
       joins (r, c) and (r, c + 1), v<r><c> joins (r, c) and (r + 1, c)). Graph, pair list and J1 are the only inputs that differ
       from the 3 x 3 cert: Jmin = J1 (the tilts of T1 and T3 are taken at t = 1/J1) and JGRID = [J1] (the four terms are
       nonincreasing in J, spec sec. 3, and the vertex step covers [0, 1/J1] in 64 cells). The P2-13 targets are N = 3 with J1 = 300
       and N = 4 with J1 = 350. SIGS = all (SIGMAS) or a comma list of members of SIGMAS.
  (g2) the pair list: every pair of distinct edges with a horizontal edge, no common vertex, and neither edge the image of the other
       under the top-bottom or the left-right reflection (Lemma 6.1 covers those); orbits under the group of the two reflections.
       C-ENUM compares (pairs, orbits, orbits with a middle-row edge) with the ASSESS_SHORT_STRIPS_REACH_rv02.md (d9381662),
       (72, 19, 8) for P3 x P4. ORBS = all, far (the middle-row orbit with the smallest Delta^2, ties to the larger distance; on a
       grid without a middle row the orbit with the smallest Delta^2) or a comma list of names G01, G02, ... (sorted by representative).
  (g3) checks added in grid mode: C-GRAPH-G (spanning trees; Foster sum V - 1; L+ invariant under both reflections), C-ENUM,
       C-ORBIT-DELTA (Delta^2 equal over each orbit); per orbit C-GAUSS (c2 = (N-1) Delta^2 / 8 from the untilted table), C-EXACT on
       the untilted table, C-SYM (a second member, oriented by its group element, gives the same a_k for k <= 2) and C-CELLS (the
       per-cell report reproduces phi_scan's minimum and negative count). Every check of the 3 x 3 cert run is kept: each build still
       runs C-H for every tilt and C-EXACT on T1, T2_v0 and T3_v0.
  (g4) plants (must FIRE): PLANT-MOM on T0 and on T1 (c_exact with perturb=True: one moment + 1e-20), PLANT-FALSE-MOM (A_ef(0)
       lowered by 2 c2, so that the covariance's leading term is -c2: phi_scan must find negative cells; once with zero errors before
       the tilted build, once with the errors of the reported point after it). CONTROLS = 'desk' adds C-CONTROL33 (the certified point
       R-J1 O4 N=3 K=4, J1 80, sigma 3/5, L 2.241485e-04 of out_kt_lbu_v1_1_cert.out l.89, rebuilt with Jmin 50, reproduced to the
       printed digits), c_bound() (C-BOUND must PASS, PLANT-BOUND must FIRE) and C-CERT-CONTROL (the selected orbit must certify).
  (g5) readings: R-SERIES (exact c2, c3, c4; the central value at t = 1/J1), R-CERT (certified or not at J1; sigma, L, c2, L / c2, the
       four E_F and their terms) and one CELL line per t-cell (Phi_lo, Phi_lo / c2, the series at the cell midpoint).
  (g6) bookkeeping only: in grid mode each T1 recursion prints one MOMDEG line per degree (terms, cpu, peak RSS) and raises GuardStop
       before a degree (or the factorial pass) whose predicted peak RSS exceeds MEMSTOP MB (default 6500; 0 = off); SIGXCPU raises
       GuardStop, so a run at its CPU limit ends with a SUMMARY (VERDICT INCOMPLETE) instead of a core dump.
"""
import resource, sys, time, math, os, hashlib, random, itertools, signal

MODES = {'v1': (20, 300), 'v2': (60, 900), 'cert': (60, 3000), 'grid': (30, 3600)}
if len(sys.argv) < 3 or sys.argv[1] not in MODES:
    print('usage: kt_lbu_g34_pk06_v1.py MODE LIM [K [SET]]   (MODE v1 | v2 | cert; LIM = RLIMIT_CPU soft limit in s, hard LIM + 2; '
          'K for cert, 3..5; SET for cert, O4 or all)')
    print('       kt_lbu_g34_pk06_v1.py grid LIM K ROWS COLS N J1 ORBS SIGS [CONTROLS [MEMSTOP]]   (PK06 CHANGES (g1))')
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2])
if not (MODES[MODE][0] <= LIM <= MODES[MODE][1]):
    print('bad LIM %d for mode %s (need %d..%d)' % (LIM, MODE, MODES[MODE][0], MODES[MODE][1]))
    sys.exit(2)
if MODE == 'grid':
    if len(sys.argv) < 10:
        print('grid needs LIM K ROWS COLS N J1 ORBS SIGS [CONTROLS [MEMSTOP]]')
        sys.exit(2)
    KCERT, G_ROWS, G_COLS, G_N, G_J1 = (int(x) for x in sys.argv[3:8])
    G_ORBS, G_SIGS = sys.argv[8], sys.argv[9]
    G_CONTROLS = sys.argv[10] if len(sys.argv) > 10 else 'none'
    G_MEMSTOP = int(sys.argv[11]) if len(sys.argv) > 11 else 6500
    SET = 'grid'
    if not (3 <= KCERT <= 5 and 2 <= G_ROWS <= 3 and 3 <= G_COLS <= 5 and G_N in (3, 4) and 50 <= G_J1 <= 2000  # PK21 COLS <= 5
            and G_CONTROLS in ('none', 'desk') and 0 <= G_MEMSTOP <= 8000):
        print('bad grid arguments %s' % sys.argv[3:])
        sys.exit(2)
else:
    KCERT = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    if not (3 <= KCERT <= 5):
        print('bad K %d (need 3..5)' % KCERT)
        sys.exit(2)
    SET = sys.argv[4] if len(sys.argv) > 4 else 'O4'
    if SET not in ('O4', 'all'):
        print('bad SET %s (need O4 or all)' % SET)
        sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 2))

import flint
from flint import fmpq, fmpq_mat, fmpq_mpoly_ctx, arb
from flint import ctx as FLINT
FLINT.prec = 256

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.abspath(__file__), 'rb') as _fh:
    SELF_SHA = hashlib.sha256(_fh.read()).hexdigest()
LIT = os.path.join(HERE, 'lbu_lit_v1')
LIT_SHA = {'riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
           'pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
           'npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
           'amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc'}


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

# ---------------------------------------------------------------- bookkeeping
def cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def out(s=''):
    print(s, flush=True)


class GuardStop(Exception):
    pass


def guard(tag):
    if cpu() > LIM - 4:
        raise GuardStop(tag)


CHECKS = {}
PLANTS = {}


def check(name, ok, detail=''):
    ok = bool(ok)
    CHECKS[name] = CHECKS.get(name, True) and ok
    out('CHECK %s %s %s' % (name, 'PASS' if ok else 'FAIL', detail))


def plant(name, fired, detail=''):
    fired = bool(fired)
    PLANTS[name] = PLANTS.get(name, True) and fired
    out('PLANT %s %s %s' % (name, 'FIRED' if fired else 'SILENT', detail))


FACT = [1]
for _i in range(1, 80):
    FACT.append(FACT[-1] * _i)


def mfact(m):
    r = 1
    for e in m:
        r *= FACT[e]
    return r


def dfact(m):
    r = 1
    while m > 1:
        r *= m
        m -= 2
    return r


def q_ceil(x, den):
    """the smallest k/den >= x (x an fmpq)."""
    return fmpq(int((x * den).ceil()), den)


def up_q(x):
    """an exact rational upper bound of the arb x."""
    return x.upper().fmpq()


def f6(x):
    return '%.6e' % float(x)


# ---------------------------------------------------------------- univariate exact series (lists of fmpq)
def us_mul(a, b, K):
    res = [fmpq(0)] * (K + 1)
    for i in range(min(K + 1, len(a))):
        if a[i] == 0:
            continue
        for j in range(min(K + 1 - i, len(b))):
            res[i + j] += a[i] * b[j]
    return res


def us_inv(a, K):
    res = [fmpq(0)] * (K + 1)
    res[0] = 1 / a[0]
    for k in range(1, K + 1):
        acc = fmpq(0)
        for j in range(1, min(k, len(a) - 1) + 1):
            acc += a[j] * res[k - j]
        res[k] = -acc / a[0]
    return res


def cov_series(A1, Ae, Af, Aef, K):
    i1 = us_inv(A1, K)
    x = us_mul(Aef, i1, K)
    y = us_mul(us_mul(Ae, Af, K), us_mul(i1, i1, K), K)
    return [p - q for p, q in zip(x, y)]


# ---------------------------------------------------------------- graphs (exact)
class Graph:
    def __init__(s, V, edges):
        s.V, s.edges = V, list(edges)
        L = fmpq_mat(V, V)
        for (a, b) in s.edges:
            L[a, a] = L[a, a] + 1
            L[b, b] = L[b, b] + 1
            L[a, b] = L[a, b] - 1
            L[b, a] = L[b, a] - 1
        s.L = L
        B = fmpq_mat(V, V - 1)
        for i in range(V - 1):
            B[i, i] = 1
            B[V - 1, i] = -1
        s.B, s.Bt = B, B.transpose()
        s.A0 = s.Bt * L * B
        s.detA0 = s.A0.det()
        s.Lp = s.B * s.A0.inv() * s.Bt
        red = fmpq_mat(V - 1, V - 1)
        for i in range(V - 1):
            for j in range(V - 1):
                red[i, j] = L[i, j]
        s.tau = red.det()
        s.Lpd = [s.Lp[v, v] for v in range(V)]

    def R(s, a, b):
        return s.Lp[a, a] + s.Lp[b, b] - 2 * s.Lp[a, b]

    def tilt(s, rates):
        """gamma tilted by exp(sum_v rates_v X_v): (C, ratio, ok). C = B A^{-1} B^T with A = B^T (L - 2 diag(rates)) B on the basis B of
        1-perp; ratio = det A0 / det A, so E_gamma[exp(sum rates X)] = ratio^{n/2}; ok = hypothesis (H) (RV12_3 L1) by Sylvester."""
        V = s.V
        Dm = fmpq_mat(V, V)
        for v in range(V):
            Dm[v, v] = rates[v]
        A_ = s.Bt * (s.L - 2 * Dm) * s.B
        for k in range(1, V):
            sub = fmpq_mat(k, k)
            for i in range(k):
                for j in range(k):
                    sub[i, j] = A_[i, j]
            if not (sub.det() > 0):
                return None, None, False
        return s.B * A_.inv() * s.Bt, s.detA0 / A_.det(), True


def evec_of(V, pair):
    e = [0] * V
    e[pair[0]] = 1
    e[pair[1]] = -1
    return e


KAPPA_A = fmpq(1, 2)


def ann_rates(g, tau_a, v):
    """the annulus tilt: tau_a on every vertex plus lambda'_v = kappa_a / (2 L+_vv) at v, kappa_a = 1/2 halved until (H) holds."""
    ka = KAPPA_A
    for _ in range(8):
        lam = ka / (2 * g.Lpd[v])
        rates = [tau_a] * g.V
        rates[v] = tau_a + lam
        C, r, ok = g.tilt(rates)
        if ok:
            return C, r, lam, ka
        ka = ka / 2
    return None, None, None, None


# ---------------------------------------------------------------- the pattern ring: X polynomials times Q_e^a Q_{f_b}^[b > 0]
class PR:
    def __init__(s, V, nb):
        s.V, s.nb = V, nb
        s.ctx = fmpq_mpoly_ctx.get(('x', V))
        s.zero = s.ctx.from_dict({})
        s.one = s.ctx.constant(1)
        s.pats = [(a, b) for a in (0, 1) for b in range(nb + 1)]

    @staticmethod
    def q(P):
        return P[0] + (1 if P[1] else 0)

    @staticmethod
    def pmul(P1, P2):
        a = P1[0] + P2[0]
        if a > 1 or (P1[1] and P2[1]):
            return None
        return (a, P1[1] or P2[1])

    @staticmethod
    def splits(P3):
        a3, b3 = P3
        res = []
        for a1 in range(a3 + 1):
            if b3 == 0:
                res.append(((a1, 0), (a3 - a1, 0)))
            else:
                res.append(((a1, b3), (a3 - a1, 0)))
                res.append(((a1, 0), (a3 - a1, b3)))
        return res

    def X(s, v, k=1, c=1):
        e = [0] * s.V
        e[v] = k
        return s.ctx.from_dict({tuple(e): c})

    def D2(s, u, v):
        return s.X(u, 2) - s.X(u, 1) * s.X(v, 1) * 2 + s.X(v, 2)

    def Mk(s, u, v, k):
        return s.one if k == 0 else s.X(u, k) + s.X(v, k)


def padd(*Ps):
    res = {}
    for P in Ps:
        for k, v in P.items():
            res[k] = res[k] + v if k in res else v
    return {k: v for k, v in res.items() if not v.is_zero()}


def pscale(P, c):
    if c == 0:
        return {}
    return {k: v * c for k, v in P.items()}


def pmulp(R, P1, P2):
    res = {}
    for k1, v1 in P1.items():
        for k2, v2 in P2.items():
            k = R.pmul(k1, k2)
            if k is None:
                raise ValueError('forbidden Q product %s * %s' % (k1, k2))
            pr = v1 * v2
            res[k] = res[k] + pr if k in res else pr
    return {k: v for k, v in res.items() if not v.is_zero()}


def pabs(R, P):
    return {k: R.ctx.from_dict({m: abs(c) for m, c in zip(v.monoms(), v.coeffs())}) for k, v in P.items()}


def pnterms(P):
    return sum(len(v) for v in P.values())


def szero(K):
    return [dict() for _ in range(K + 1)]


def sadd(A_, B_):
    return [padd(a, b) for a, b in zip(A_, B_)]


def sscale(A_, c):
    return [pscale(a, c) for a in A_]


def smul(R, A_, B_, K):
    res = szero(K)
    for i in range(K + 1):
        if not A_[i]:
            continue
        for j in range(K + 1 - i):
            if B_[j]:
                res[i + j] = padd(res[i + j], pmulp(R, A_[i], B_[j]))
    return res


def sexp(R, H, K):
    assert not H[0]
    E = [{(0, 0): R.one}] + [dict() for _ in range(K)]
    for k in range(1, K + 1):
        acc = {}
        for j in range(1, k + 1):
            if H[j] and E[k - j]:
                acc = padd(acc, pscale(pmulp(R, H[j], E[k - j]), j))
        E[k] = pscale(acc, fmpq(1, k))
    return E


def tp_add(A_, B_):
    m = max(len(A_), len(B_))
    return [padd(A_[i] if i < len(A_) else {}, B_[i] if i < len(B_) else {}) for i in range(m)]


def tp_mul(R, A_, B_):
    res = [dict() for _ in range(len(A_) + len(B_) - 1)]
    for i, x in enumerate(A_):
        for j, y in enumerate(B_):
            if x and y:
                res[i + j] = padd(res[i + j], pmulp(R, x, y))
    return res


def tp_scale(A_, c):
    return [pscale(x, c) for x in A_]


# ---------------------------------------------------------------- exact series of the chart (PK10 sec. 19.1)
def w_exact(Kw):
    """w(x, y) = (sqrt(1 - x) + sqrt(1 - y))^{-2} to total degree Kw, exact: w = (1/4) sum_m (m + 1) (-d/2)^m, d = s(x) + s(y) - 2."""
    s_ = [fmpq(1)] + [fmpq(-math.comb(2 * k, k), 4 ** k * (2 * k - 1)) for k in range(1, Kw + 1)]
    hd = {}
    for k in range(1, Kw + 1):
        hd[(k, 0)] = hd.get((k, 0), fmpq(0)) - s_[k] / 2
        hd[(0, k)] = hd.get((0, k), fmpq(0)) - s_[k] / 2

    def mul2(P1, P2):
        res = {}
        for (i1, j1), c1 in P1.items():
            for (i2, j2), c2 in P2.items():
                if i1 + i2 + j1 + j2 <= Kw:
                    key = (i1 + i2, j1 + j2)
                    res[key] = res.get(key, fmpq(0)) + c1 * c2
        return res
    w = {(0, 0): fmpq(1, 4)}
    pw = {(0, 0): fmpq(1)}
    for m in range(1, Kw + 1):
        pw = mul2(pw, hd)
        for key, v in pw.items():
            w[key] = w.get(key, fmpq(0)) + fmpq(m + 1, 4) * v
    return w


def wpoly(R, wd, a, b, m):
    d = {}
    for (i, j), c in wd.items():
        if i + j == m and c != 0:
            e = [0] * R.V
            e[a] += i
            e[b] += j
            d[tuple(e)] = d.get(tuple(e), fmpq(0)) + c
    return R.ctx.from_dict(d)


def H_series(R, g, n, K, wd, fpc=None):
    """H = sum_v meas_v + FP + sum_x anh_x to order K: meas_v = -1/2 log(1 - t X_v), FP = fpc log(1 - y) (fpc = n; PLANT-FP: n + 1),
    y = (1/V) sum_v (1 - sqrt(1 - t X_v)), anh_x = -(1/2) t D_x w(t X_a, t X_b), D_x = (X_a - X_b)^2."""
    fpc = n if fpc is None else fpc
    V = g.V
    H = szero(K)
    for k in range(1, K + 1):
        p = R.zero
        for v in range(V):
            p = p + R.X(v, k, fmpq(1, 2 * k))
        H[k] = padd(H[k], {(0, 0): p})
    y = szero(K)
    for k in range(1, K + 1):
        bk = fmpq(math.comb(2 * k, k), 4 ** k * (2 * k - 1) * V)
        p = R.zero
        for v in range(V):
            p = p + R.X(v, k, bk)
        y[k] = {(0, 0): p}
    ym = y
    for m in range(1, K + 1):
        H = sadd(H, sscale(ym, fmpq(-fpc, m)))
        ym = smul(R, ym, y, K)
    for (a, b) in g.edges:
        D = R.D2(a, b)
        for k in range(1, K + 1):
            H[k] = padd(H[k], {(0, 0): D * wpoly(R, wd, a, b, k - 1) * fmpq(-1, 2)})
    return H


def xi_series(R, wd, a, b, P, K):
    """xi_x = Q_x / 2 + (1/2) D_x t w(t X_a, t X_b); Q_x is the pattern P."""
    S = szero(K)
    S[0] = {P: R.ctx.constant(fmpq(1, 2))}
    D = R.D2(a, b)
    for k in range(1, K + 1):
        S[k] = {(0, 0): D * wpoly(R, wd, a, b, k - 1) * fmpq(1, 2)}
    return S


# ---------------------------------------------------------------- exact Gaussian moments (amom2b's recursion, exact, quotient ring)
def det_sub(Gl, S):
    k = len(S)
    M = fmpq_mat(k, k)
    for i in range(k):
        for j in range(k):
            M[i, j] = Gl[S[i]][S[j]]
    return M.det()


class Moments:
    """E_C[X^alpha Q_e^a Q_f^b] for the Gaussian with covariance C (x) I_n on 1-perp; forms X_v = |phi_v|^2, Q_e, Q_{f_b} = |phi_u - phi_w|^2.
    M(s) = det(I - 2 S Gamma)^{-n/2}; k M_k = sum_j ((1 - n/2) j - k) D_j M_{k-j}; moments = alpha! [s^alpha] M."""
    def __init__(s, R, g, C, ratio, n, evec, fvecs, caps, tag):
        t0 = cpu()
        V = g.V
        s.R, s.n, s.ratio, s.caps, s.tag = R, n, ratio, dict(caps), tag
        s.rss0 = rss_mb()
        assert caps[0] >= caps[1] >= caps[2]
        vecs = [[1 if u == v else 0 for u in range(V)] for v in range(V)] + [evec] + list(fvecs)
        m = len(vecs)
        U = fmpq_mat(V, m)
        for i, vec in enumerate(vecs):
            for u in range(V):
                U[u, i] = vec[u]
        Gm = U.transpose() * C * U
        s.Gl = [[Gm[i, j] for j in range(m)] for i in range(m)]
        s.D = {}
        for P in R.pats:
            extra = ([V] if P[0] else []) + ([V + P[1]] if P[1] else [])
            lst = []
            for j in range(V + 1):
                d = {}
                for Asub in itertools.combinations(range(V), j):
                    S_ = list(Asub) + extra
                    if not S_:
                        continue
                    dt = det_sub(s.Gl, S_)
                    if dt != 0:
                        e = [0] * V
                        for i in Asub:
                            e[i] = 1
                        d[tuple(e)] = dt * (-2) ** (j + len(extra))
                lst.append(R.ctx.from_dict(d))
            s.D[P] = lst
        cap = {P: caps[R.q(P)] for P in R.pats}
        M = {P: [None] * (cap[P] + 1) for P in R.pats}
        M[(0, 0)][0] = R.one
        kmax = max(cap[P] + R.q(P) for P in R.pats)
        for k in range(1, kmax + 1):
            guard('moments %s k=%d' % (tag, k))
            for P3 in R.pats:
                d3 = k - R.q(P3)
                if d3 < 0 or d3 > cap[P3]:
                    continue
                acc = R.zero
                for j in range(1, k + 1):
                    part = R.zero
                    for (P1, P2) in R.splits(P3):
                        dj1 = j - R.q(P1)
                        if dj1 < 0 or dj1 > V:
                            continue
                        d2 = d3 - dj1
                        if d2 < 0:
                            continue
                        Dp = s.D[P1][dj1]
                        if Dp.is_zero():
                            continue
                        part = part + Dp * M[P2][d2]
                    if not part.is_zero():
                        acc = acc + part * fmpq((2 - n) * j - 2 * k, 2)
                M[P3][d3] = acc * fmpq(1, k)
            if MOM_PROGRESS:
                mom_progress(s, R, M, cap, k, kmax, V, tag, t0)
        s.mom = {}
        s.nterms = 0
        for P in R.pats:
            s.mom[P] = []
            for d in range(cap[P] + 1):
                p = M[P][d]
                s.mom[P].append(R.ctx.from_dict({mm: c * mfact(mm) for mm, c in zip(p.monoms(), p.coeffs())}))
                s.nterms += len(p)
            M[P] = None
        s.cpu = cpu() - t0
        out('TABLE %s: n %d, caps %s, %d moments, cpu %.2f s' % (tag, n, caps, s.nterms, s.cpu))

    def E(s, PP):
        tot = fmpq(0)
        for P, p in PP.items():
            if p.is_zero():
                continue
            tab = s.mom[P]
            for mm, c in zip(p.monoms(), p.coeffs()):
                d = sum(mm)
                if d >= len(tab):
                    raise ValueError('%s: degree %d beyond cap %d in pattern %s' % (s.tag, d, len(tab) - 1, P))
                tot += c * tab[d][mm]
        return tot

    def Narb(s):
        r = arb(s.ratio)
        return r if s.n == 2 else r * r.sqrt()


def aperm(Gl, idx, alpha):
    """the alpha-permanent sum_pi alpha^{cyc(pi)} prod_i Gl[idx_i][idx_pi(i)] (exact)."""
    k = len(idx)
    tot = fmpq(0)
    for perm in itertools.permutations(range(k)):
        pr = fmpq(1)
        for i in range(k):
            pr *= Gl[idx[i]][idx[perm[i]]]
        if pr == 0:
            continue
        seen = [False] * k
        cyc = 0
        for i in range(k):
            if not seen[i]:
                cyc += 1
                j = i
                while not seen[j]:
                    seen[j] = True
                    j = perm[j]
        tot += pr * alpha ** cyc
    return tot


def c_exact(mo, V, rng, nmono, maxdeg, perturb=False):
    """C-EXACT: E[prod of forms] = 2^k per_{n/2}(Gamma) for random monomials of total degree <= maxdeg (independent formula)."""
    alpha = fmpq(mo.n, 2)
    bad = done = 0
    for _ in range(nmono):
        P = mo.R.pats[rng.randrange(len(mo.R.pats))]
        qd = mo.R.q(P)
        dmax = min(mo.caps[qd], maxdeg - qd)
        if dmax < 0:
            continue
        d = rng.randint(0, dmax)
        e = [0] * V
        for _r in range(d):
            e[rng.randrange(V)] += 1
        idx = [v for v in range(V) for _r in range(e[v])] + ([V] if P[0] else []) + ([V + P[1]] if P[1] else [])
        want = aperm(mo.Gl, idx, alpha) * 2 ** len(idx)
        have = mo.mom[P][d][tuple(e)]
        if perturb and done == 0:
            have = have + fmpq(1, 10 ** 20)
        done += 1
        if have != want:
            bad += 1
    return bad, done


# ---------------------------------------------------------------- Lemma 19.1's majorants (exact, given rational radii)
def partial_bell(R, k, m, xs):
    memo = {}

    def rec(kk, mm):
        if (kk, mm) in memo:
            return memo[(kk, mm)]
        if kk == 0 and mm == 0:
            res = R.one
        elif kk == 0 or mm == 0:
            res = R.zero
        else:
            res = R.zero
            for i in range(1, kk - mm + 2):
                res = res + xs[i] * rec(kk - i, mm - 1) * math.comb(kk - 1, i - 1)
        memo[(kk, mm)] = res
        return res
    return rec(k, m)


class Maj:
    """h_k (k <= K + 1), complete Bell Y_m (m <= K + 1), xi majorants as t-polynomials, Fbar_j, Dbar_{K+1} (PK10 sec. 19.1)."""
    def __init__(s, R, g, n, avec, rvec, K):
        s.R, s.g, s.n, s.a, s.r, s.K = R, g, n, list(avec), list(rvec), K
        s.h = {k: s.hbar(k) for k in range(1, K + 2)}
        Y = [{(0, 0): R.one}]
        for m in range(K + 1):
            acc = {}
            for i in range(m + 1):
                acc = padd(acc, pscale(pmulp(R, s.h[i + 1], Y[m - i]), math.comb(m, i)))
            Y.append(acc)
        s.Y = Y

    def hbar(s, k):
        R, g, a, r, V = s.R, s.g, s.a, s.r, s.g.V
        p = R.zero
        for v in range(V):
            p = p + R.X(v, k, fmpq(FACT[k - 1]) / (2 * (1 - a[v]) ** k))
        for (u, v) in g.edges:
            ae = max(a[u], a[v])
            p = p + R.D2(u, v) * R.Mk(u, v, k - 1) * (fmpq(FACT[k], 8) / (1 - ae) ** (k + 1))
        ymax = sum((a[v] / (2 - a[v]) for v in range(V)), fmpq(0)) / V
        ys = [None]
        for j in range(1, k + 1):
            cj = fmpq(dfact(2 * j - 3), 2 ** j)
            yj = R.zero
            for v in range(V):
                yj = yj + R.X(v, j, cj / (r[v] ** (2 * j - 1) * V))
            ys.append(yj)
        fp = R.zero
        for mm in range(1, k + 1):
            fp = fp + partial_bell(R, k, mm, ys) * (fmpq(s.n * FACT[mm - 1]) / (1 - ymax) ** mm)
        return {(0, 0): p + fp}

    def xibar(s, a_, b_, P, l):
        R = s.R
        ax = max(s.a[a_], s.a[b_])
        D = R.D2(a_, b_)
        if l == 0:
            return [{P: R.ctx.constant(fmpq(1, 2))}, {(0, 0): D * (fmpq(1, 8) / (1 - ax))}]
        return [{(0, 0): D * R.Mk(a_, b_, l - 1) * (fmpq(FACT[l], 8) / (1 - ax) ** (l + 1))}]

    def Fbar(s, F, j, ep, fp):
        if F == '1':
            return [{(0, 0): s.R.one}] if j == 0 else [dict()]
        if F == 'e':
            return s.xibar(ep[0], ep[1], ep[2], j)
        if F == 'f':
            return s.xibar(fp[0], fp[1], fp[2], j)
        res = [dict()]
        for i in range(j + 1):
            res = tp_add(res, tp_scale(tp_mul(s.R, s.xibar(ep[0], ep[1], ep[2], i), s.xibar(fp[0], fp[1], fp[2], j - i)), math.comb(j, i)))
        return res

    def Dbar(s, F, ep, fp):
        K1 = s.K + 1
        res = [dict()]
        for j in range(K1 + 1):
            fb = s.Fbar(F, j, ep, fp)
            term = [pmulp(s.R, x, s.Y[K1 - j]) if x else {} for x in fb]
            res = tp_add(res, tp_scale(term, math.comb(K1, j)))
        return res


def F0p(R, F, ep, fp, rho2):
    """the annulus majorant of |F| (all radii rho'^2) as a t-polynomial."""
    def xb(a_, b_, P):
        return [{P: R.ctx.constant(fmpq(1, 2))}, {(0, 0): R.D2(a_, b_) * (fmpq(1, 8) / (1 - rho2))}]
    if F == '1':
        return [{(0, 0): R.one}]
    if F == 'e':
        return xb(*ep)
    if F == 'f':
        return xb(*fp)
    return tp_mul(R, xb(*ep), xb(*fp))


def radii(g, sigma):
    """(C1): a_v = 1 - r_v^2 <= min(sigma L+_vv, 3/5), r_v = m/256 the smallest with r_v^2 >= max(1 - sigma L+_vv, 2/5)."""
    avec, rvec = [], []
    for v in range(g.V):
        x = max(1 - sigma * g.Lpd[v], fmpq(2, 5))
        m = math.isqrt(int((x * 65536).floor()))
        while fmpq(m * m, 65536) < x:
            m += 1
        r = fmpq(m, 256)
        assert 0 < r < 1
        avec.append(1 - r * r)
        rvec.append(r)
    return avec, rvec


def cslope(a, r):
    """c = -log(1 - a)/(2a) = -log(r)/a (arb)."""
    return -(arb(r).log()) / arb(a)


C35 = q_ceil(up_q(-(arb(fmpq(2, 5)).log()) / arb(fmpq(6, 5))), 64)     # >= c(3/5): every radius is capped at 3/5


# ---------------------------------------------------------------- the J1-independent part for one graph, N, K and partner list
FNAMES = ('1', 'e', 'f', 'ef')
DF = {'1': 0, 'e': 1, 'f': 1, 'ef': 2}


class Build:
    def __init__(s, g, n, K, epair, fpairs, Jmin, kappa, rho2, label, need_tilts=True):
        t0 = cpu()
        s.g, s.n, s.K, s.label, s.Jmin, s.kappa, s.rho2 = g, n, K, label, Jmin, kappa, rho2
        V = g.V
        nb = len(fpairs)
        R = PR(V, nb)
        s.R = R
        wd = w_exact(max(K, 1) + 1)
        H = H_series(R, g, n, K, wd)
        E = sexp(R, H, K)
        s.ep = (epair[0], epair[1], (1, 0))
        s.fps = [(f[0], f[1], (0, b + 1)) for b, f in enumerate(fpairs)]
        xe = xi_series(R, wd, epair[0], epair[1], (1, 0), K)
        xfs = [xi_series(R, wd, f[0], f[1], (0, b + 1), K) for b, f in enumerate(fpairs)]
        one = szero(K)
        one[0] = {(0, 0): R.one}
        s.PS = {('1', 0): smul(R, one, E, K), ('e', 0): smul(R, xe, E, K)}
        for b in range(1, nb + 1):
            s.PS[('f', b)] = smul(R, xfs[b - 1], E, K)
            s.PS[('ef', b)] = smul(R, smul(R, xe, xfs[b - 1], K), E, K)
        s.keys = list(s.PS.keys())
        out('SERIES %s: K %d, terms per key %s, cpu %.2f s' % (label, K, {k: [pnterms(p) for p in v] for k, v in s.PS.items() if k[1] <= 1},
                                                             cpu() - t0))
        s.evec = evec_of(V, epair)
        s.fvecs = [evec_of(V, f) for f in fpairs]
        guard('T0 ' + label)
        s.T0 = Moments(R, g, g.Lp, fmpq(1), n, s.evec, s.fvecs, {0: 2 * K, 1: 2 * K, 2: 2 * K}, label + ' T0')
        out('RSS %s T0: peak %.0f MB' % (label, rss_mb()))
        s.a = {key: [s.T0.E(s.PS[key][k]) for k in range(K + 1)] for key in s.keys}
        if not need_tilts:
            return
        rng = random.Random(7)
        # T1: the common B_rem tilt exp(C35 t_max sum X), valid for every radius (a_v <= 3/5) and every J1 >= Jmin
        s.tau_c = C35 / Jmin
        C1, r1, ok1 = g.tilt([s.tau_c] * V)
        check('C-H %s T1' % label, ok1, 'tilt %s' % s.tau_c)
        if not ok1:
            raise ValueError('T1 tilt violates (H)')
        guard('T1 ' + label)
        s.T1 = Moments(R, g, C1, r1, n, s.evec, s.fvecs, {0: 2 * K + 6, 1: 2 * K + 4, 2: 2 * K + 2}, label + ' T1')
        out('RSS %s T1: peak %.0f MB' % (label, rss_mb()))
        bad, done = c_exact(s.T1, V, rng, 10, 6)
        check('C-EXACT %s T1' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
        s.Nc = s.T1.Narb()
        # T2_v: the Chernoff tilts lambda_v = kappa / (2 L+_vv); tail expectations of |(F e^H)_k|
        s.lam = [kappa / (2 * g.Lpd[v]) for v in range(V)]
        s.N2, s.TL = [], {key: [[None] * V for _ in range(K + 1)] for key in s.keys}
        pab = {key: [pabs(R, s.PS[key][k]) for k in range(K + 1)] for key in s.keys}
        for v in range(V):
            rates = [fmpq(0)] * V
            rates[v] = s.lam[v]
            C2, r2, ok2 = g.tilt(rates)
            check('C-H %s T2 v%d' % (label, v), ok2, 'lambda %s' % s.lam[v])
            if not ok2:
                raise ValueError('T2 tilt violates (H)')
            guard('T2 %s v%d' % (label, v))
            T2 = Moments(R, g, C2, r2, n, s.evec, s.fvecs, {0: 2 * K, 1: 2 * K, 2: 2 * K}, '%s T2 v%d' % (label, v))
            if v == 0:
                bad, done = c_exact(T2, V, rng, 10, 6)
                check('C-EXACT %s T2 v0' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
            s.N2.append(T2.Narb())
            for key in s.keys:
                for k in range(K + 1):
                    s.TL[key][k][v] = T2.E(pab[key][k])
            del T2
        out('RSS %s T2: peak %.0f MB' % (label, rss_mb()))
        # T3_v: the annulus tilts; expectations of the annulus majorant (t-polynomial parts)
        cp = -(arb(1 - rho2).log()) / (2 * arb(rho2))
        s.cprime = q_ceil(up_q(cp), 64)
        s.tau_a = s.cprime / Jmin
        s.N3, s.lam_a, s.AN = [], [], {key: [None] * V for key in s.keys}
        f0 = {}
        for key in s.keys:
            F, b = key
            f0[key] = F0p(R, F, s.ep, s.fps[b - 1] if b else None, rho2)
        for v in range(V):
            C3, r3, lam_a, ka = ann_rates(g, s.tau_a, v)
            check('C-H %s T3 v%d' % (label, v), C3 is not None, 'tilt %s + kappa_a %s' % (s.tau_a, ka))
            if C3 is None:
                raise ValueError('no annulus tilt satisfies (H)')
            guard('T3 %s v%d' % (label, v))
            T3 = Moments(R, g, C3, r3, n, s.evec, s.fvecs, {0: 4, 1: 2, 2: 0}, '%s T3 v%d' % (label, v))
            if v == 0:
                bad, done = c_exact(T3, V, rng, 10, 6)
                check('C-EXACT %s T3 v0' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
            s.N3.append(T3.Narb())
            s.lam_a.append(lam_a)
            for key in s.keys:
                s.AN[key][v] = [T3.E(part) for part in f0[key]]
            del T3
        s.sig = {}
        out('BUILD %s done, cpu %.2f s, peak RSS %.0f MB' % (label, cpu() - t0, rss_mb()))

    def add_sigma(s, sigma):
        """radii for sigma and the expectations E_T1[Dbar_{K+1}] (t-parts) per key."""
        t0 = cpu()
        g, R = s.g, s.R
        avec, rvec = radii(g, sigma)
        assert s.rho2 > max(avec)
        cmax = max(up_q(cslope(avec[v], rvec[v])) for v in range(g.V))
        assert cmax <= C35
        mj = Maj(R, g, s.n, avec, rvec, s.K)
        ED, nt = {}, {}
        for key in s.keys:
            guard('Dbar %s sigma %s %s' % (s.label, sigma, key))
            F, b = key
            parts = mj.Dbar(F, s.ep, s.fps[b - 1] if b else None)
            nt[key] = sum(pnterms(p) for p in parts)
            vals = [s.T1.E(p) for p in parts]
            for x in vals:
                assert x >= 0
            ED[key] = vals + [fmpq(0)] * (3 - len(vals))
        s.sig[sigma] = (avec, rvec, ED)
        out('SIGMA %s %s: radii %s, max slope %s, Dbar terms %s, cpu %.2f s, peak RSS %.0f MB' % (s.label, sigma, [f6(x) for x in avec],
            f6(cmax), {k: nt[k] for k in s.keys if k[1] <= 1}, cpu() - t0, rss_mb()))

    def errors(s, sigma, J1, key, drop_rem=False):
        """(B_rem, B_tail, B_ann, B_far) for key at J1 (arb upper bounds), radii of sigma."""
        avec, rvec, ED = s.sig[sigma]
        K, V, n = s.K, s.g.V, s.n
        t1 = fmpq(1, J1)
        assert t1 <= fmpq(1, s.Jmin)
        F = key[0]
        e = ED[key]
        brem = arb(0) if drop_rem else arb(t1 ** (K + 1) / FACT[K + 1]) * s.Nc * arb(e[0] + e[1] * t1 + e[2] * t1 * t1)
        ch = [(-(arb(s.lam[v] * J1 * avec[v]))).exp() for v in range(V)]
        cha = [(-(arb(s.lam_a[v] * J1 * avec[v]))).exp() for v in range(V)]
        btail = arb(0)
        for k in range(K + 1):
            for v in range(V):
                btail += arb(t1 ** k) * ch[v] * s.N2[v] * arb(s.TL[key][k][v])
        bann = arb(0)
        for v in range(V):
            val = fmpq(0)
            for i, x in enumerate(s.AN[key][v]):
                val += x * t1 ** i
            bann += cha[v] * s.N3[v] * arb(val)
        bfar, th = far_bound(s.g, n, J1, DF[F], s.rho2)
        return [arb(up_q(x)) for x in (brem, btail, bann, bfar)], th


def far_bound(g, n, J1, dF, rho2):
    """(C3): B_far <= (2 J1)^dF tau^{n/2} (1 - th)^{-n(V-1)/2} sum_v exp(-th J1 rho'^2 / (2 L+_vv)); th chosen on k/400 in floats, the
    bound evaluated in arb at that rational th; B_far is decreasing in J for J > 2 max L+ dF / (th rho'^2) (asserted)."""
    V = g.V
    best = None
    for k in range(1, 400):
        th = k / 400.0
        xs = [-th * J1 * float(rho2) / (2 * float(g.Lpd[v])) for v in range(V)]
        mx = max(xs)
        val = (dF * math.log(2 * J1) + 0.5 * n * math.log(float(g.tau)) - 0.5 * n * (V - 1) * math.log(1 - th)
               + mx + math.log(sum(math.exp(x - mx) for x in xs)))
        if best is None or val < best[0]:
            best = (val, k)
    th = fmpq(best[1], 400)
    assert J1 > 2 * max(g.Lpd) * dF / (th * rho2)
    sm = arb(0)
    for v in range(V):
        sm += (-(arb(th * J1 * rho2 / (2 * g.Lpd[v])))).exp()
    tauN = arb(g.tau) if n == 2 else arb(g.tau) * arb(g.tau).sqrt()
    ex = n * (V - 1)
    om = arb(1 - th)
    fac = om ** (ex // 2)
    if ex % 2:
        fac = fac * om.sqrt()
    return arb(2 * J1) ** dF * tauN * sm / fac, th


def horner(coefs, x):
    r = arb(0)
    for c in reversed(coefs):
        r = r * x + arb(c)
    return r


def phi_scan(Acoef, Eu, t1, ncell=64):
    """min over t-cells of [0, t1] of the vertex lower bound of Cov = i_ef/i_1 - i_e i_f / i_1^2, i_F in A_F(t) +- E_F, with the
    monotonicity in i_1 (2 i_e i_f > i_ef i_1) checked on every box. Returns (min lower bound (arb), monotone ok, negative cells)."""
    worst = None
    mono = True
    nneg = 0
    for i in range(ncell):
        lo_t = t1 * i / ncell
        hi_t = t1 * (i + 1) / ncell
        tb = arb((lo_t + hi_t) / 2) + arb(0, (hi_t - lo_t) / 2)
        val = {F: horner(Acoef[F], tb) for F in FNAMES}
        i1l = (val['1'] - Eu['1']).lower()
        i1h = (val['1'] + Eu['1']).upper()
        iel = (val['e'] - Eu['e']).lower()
        ieh = (val['e'] + Eu['e']).upper()
        ifl = (val['f'] - Eu['f']).lower()
        ifh = (val['f'] + Eu['f']).upper()
        iefl = (val['ef'] - Eu['ef']).lower()
        iefh = (val['ef'] + Eu['ef']).upper()
        if not (i1l > 0 and iel > 0 and ifl > 0 and iefl > 0):
            mono = False
            ph = arb(-1)
        else:
            if not (2 * iel * ifl - iefh * i1h > 0):
                mono = False
            ph = (iefl / i1l - ieh * ifh / (i1l * i1l)).lower()
        if worst is None or ph < worst:
            worst = ph
        if not (ph > 0):
            nneg += 1
    return worst, mono, nneg


# ---------------------------------------------------------------- the 3 x 3 grid
NAMES = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW', 'C']
EDGES = {'b0': (0, 1), 'b1': (1, 2), 'b2': (2, 3), 'b3': (3, 4), 'b4': (4, 5), 'b5': (5, 6), 'b6': (6, 7), 'b7': (7, 0),
         'sS': (8, 0), 'sE': (8, 2), 'sN': (8, 4), 'sW': (8, 6)}
ELIST = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'sS', 'sE', 'sN', 'sW']
# (name, e, f, Delta^2 from out_kt_c2unif_v1_full.out 438317a3 l.4-12, second member (sigma e, sigma f) for C-SYM)
ORBITS = [('O1', 'b0', 'b2', fmpq(1, 36), ('b2', 'b4')), ('O2', 'b0', 'b4', fmpq(1, 144), ('b1', 'b5')),
          ('O3', 'b0', 'sE', fmpq(25, 144), ('b6', 'sS')), ('O4', 'b0', 'sN', fmpq(1, 144), ('b2', 'sW')),
          ('O5', 'b0', 'sW', fmpq(1, 144), ('b2', 'sS'))]
G9 = Graph(9, [EDGES[x] for x in ELIST])
JGRID = [50, 55, 60, 65, 70, 75, 80, 90, 100, 110, 120, 135, 150, 175, 200]
SIGMAS = [fmpq(1, 4), fmpq(1, 3), fmpq(2, 5), fmpq(1, 2), fmpq(3, 5)]
KAPPA = fmpq(4, 5)
RHO2 = fmpq(9801, 10000)
# out_kt_c2unif_v1_full.out (438317a3) l.61-66: D(J_f = beta) for c2's pair (b6, sS) in O3, float quadrature
CDATA = {(3, 100): 4.361620e-06, (3, 150): 1.935314e-06, (3, 200): 1.087723e-06,
         (4, 100): 6.541862e-06, (4, 150): 2.902814e-06, (4, 200): 1.631521e-06}
# the NOTE_SPINWAVE_P3P3_v1 (a4e09eb6) through the REMAINDER_SHEET_LBU_v1 (c6f9cf3e) l.63-69: (A_ef(0), c2, c3) at N = 3, 4
ROW0 = {'O1': ((fmpq(293, 576), fmpq(1, 144), fmpq(1, 216)), (fmpq(875, 768), fmpq(1, 96), fmpq(245, 36864))),
        'O3': ((fmpq(263, 576), fmpq(25, 576), fmpq(73, 3456)), (fmpq(191, 192), fmpq(25, 384), fmpq(1151, 36864))),
        'O2': ((fmpq(145, 288), fmpq(1, 576), fmpq(1, 864)), (fmpq(869, 768), fmpq(1, 384), fmpq(17, 9216))),
        'O4': ((fmpq(239, 576), fmpq(1, 576), fmpq(13, 3456)), (fmpq(179, 192), fmpq(1, 384), fmpq(311, 36864))),
        'O5': ((fmpq(239, 576), fmpq(1, 576), fmpq(13, 3456)), (fmpq(179, 192), fmpq(1, 384), fmpq(311, 36864)))}
# the same sheet l.55: a_1 of F = 1 (A'(0) = E_gamma[H_1]), keyed by n = N - 1
A1ROW0 = {2: fmpq(5, 6), 3: fmpq(31, 64)}
# v1's partner list: the partners of O1..O5 in order, then b3 (M1) and b5 (M2)
PARTNERS_V1 = ['b2', 'b4', 'sE', 'sN', 'sW', 'b3', 'b5']


def delta_of(g, e, f):
    (a, b), (u, w) = e, f
    return g.R(a, u) + g.R(b, w) - g.R(a, w) - g.R(b, u)


def certify(bd, b, sigmas, jgrid, tagline):
    """for partner b: the smallest J1 in jgrid with min Phi > 0 (over sigmas); prints every evaluated point. Returns a dict or None."""
    best = None
    for J1 in jgrid:
        t1 = fmpq(1, J1)
        Acoef = {F: bd.a[(F, 0) if F in ('1', 'e') else (F, b)] for F in FNAMES}
        for sigma in sigmas:
            guard('certify %s J1 %d' % (tagline, J1))
            Eu, terms, ths = {}, {}, {}
            for F in FNAMES:
                key = (F, 0) if F in ('1', 'e') else (F, b)
                tt, th = bd.errors(sigma, J1, key)
                terms[F] = tt
                ths[F] = str(th)
                Eu[F] = arb(up_q(tt[0] + tt[1] + tt[2] + tt[3]))
            L, mono, nneg = phi_scan(Acoef, Eu, t1)
            ok = mono and nneg == 0 and L > 0
            out('POINT %s J1 %d sigma %s: L %s mono %s neg %d | %s' % (tagline, J1, sigma, f6(L), mono, nneg,
                '; '.join('%s rem %s tail %s ann %s far %s (th %s)' % (F, f6(terms[F][0]), f6(terms[F][1]), f6(terms[F][2]),
                                                                       f6(terms[F][3]), ths[F]) for F in FNAMES)))
            if ok and (best is None or J1 < best['J1'] or (J1 == best['J1'] and L > best['L'])):
                best = dict(J1=J1, sigma=sigma, L=L, terms=terms, ths=ths, Eu=Eu)
        if best is not None and best['J1'] == J1:
            break
    return best


# ---------------------------------------------------------------- v1: validation 1
def tree_expect(n, K):
    """P3 with e = (0, 1), f = (1, 2): the exact asymptotic series of I/main = r^2, I_xi_e/main = <xi> r^2, I_xi_e xi_f/main = <xi>^2 r^2,
    r = 1 (N = 3: 1 - e^{-2J}) or sqrt(2 pi J) e^{-J} I_1(J) ~ sum_k (-1)^k a_k(1) t^k (N = 4); <xi> = n/2 + t d/dt log r."""
    r = [fmpq(1)]
    for k in range(1, K + 1):
        if n == 2:
            r.append(fmpq(0))
        else:
            num = 1
            for i in range(1, k + 1):
                num *= (4 - (2 * i - 1) ** 2)
            r.append(fmpq((-1) ** k * num, FACT[k] * 8 ** k))
    u = [fmpq(0)] + r[1:]
    lg = [fmpq(0)] * (K + 1)
    um = u[:]
    for m in range(1, K + 1):
        lg = [x + y * fmpq((-1) ** (m + 1), m) for x, y in zip(lg, um)]
        um = us_mul(um, u, K)
    xi = [fmpq(n, 2)] + [k * lg[k] for k in range(1, K + 1)]
    r2 = us_mul(r, r, K)
    return {'1': r2, 'e': us_mul(xi, r2, K), 'ef': us_mul(us_mul(xi, xi, K), r2, K)}


def tree_truth(n, J):
    Ja = arb(J)
    if n == 2:
        r = 1 - (-2 * Ja).exp()
        xi = 1 - 2 * Ja * (-2 * Ja).exp() / r
    else:
        i1 = Ja.bessel_i(1, scaled=True)
        i0 = Ja.bessel_i(0, scaled=True)
        r = (2 * arb.pi() * Ja).sqrt() * i1
        xi = Ja + 2 - Ja * i0 / i1
    return {'1': r * r, 'e': xi * r * r, 'ef': xi * xi * r * r}


def run_v1():
    rng = random.Random(20261102)
    # C-SER
    wd = w_exact(8)
    rows = all(sum((c for (i, j), c in wd.items() if i + j == m), fmpq(0)) == fmpq(1, 4) for m in range(9))
    sym = all(wd.get((j, i), fmpq(0)) == c for (i, j), c in wd.items())
    check('C-SER', rows and sym, 'w row sums 1/4 to degree 8: %s; symmetric: %s' % (rows, sym))
    # C-GRAPH
    g = G9
    want = [fmpq(13, 36), fmpq(13, 24)] * 4 + [fmpq(2, 9)]
    okL = all(g.Lpd[v] == want[v] for v in range(9))
    foster = sum((g.R(*EDGES[x]) for x in ELIST), fmpq(0))
    okD = True
    for (nm, e, f, d2, _) in ORBITS:
        dd = delta_of(g, EDGES[e], EDGES[f])
        okD = okD and dd * dd == d2
        out('ORBIT %s (%s, %s): Delta %s, Delta^2 %s (table %s)' % (nm, e, f, dd, dd * dd, d2))
    check('C-GRAPH', okL and g.tau == 192 and foster == 8 and okD,
          'L+ diag %s; tau %s; Foster %s; Delta^2 match %s' % (okL, g.tau, foster, okD))
    # C-TREE (+ PLANT-FP): P3, K = 5
    gt = Graph(3, [(0, 1), (1, 2)])
    KT = 5
    for n in (2, 3):
        exp_ = tree_expect(n, KT)
        for fpc, isplant in ((n, False), (n + 1, True)):
            Rt = PR(3, 1)
            wdt = w_exact(KT + 1)
            H = H_series(Rt, gt, n, KT, wdt, fpc=fpc)
            E = sexp(Rt, H, KT)
            xe = xi_series(Rt, wdt, 0, 1, (1, 0), KT)
            xf = xi_series(Rt, wdt, 1, 2, (0, 1), KT)
            one = szero(KT)
            one[0] = {(0, 0): Rt.one}
            T0 = Moments(Rt, gt, gt.Lp, fmpq(1), n, evec_of(3, (0, 1)), [evec_of(3, (1, 2))], {0: 2 * KT, 1: 2 * KT, 2: 2 * KT},
                         'tree N=%d fpc=%d' % (n + 1, fpc))
            got = {'1': [T0.E(p) for p in smul(Rt, one, E, KT)], 'e': [T0.E(p) for p in smul(Rt, xe, E, KT)],
                   'ef': [T0.E(p) for p in smul(Rt, smul(Rt, xe, xf, KT), E, KT)]}
            okT = all(got[F] == exp_[F] for F in got)
            if isplant:
                plant('PLANT-FP N=%d' % (n + 1), not okT, 'FP coefficient n + 1 breaks the exact tree series')
            else:
                check('C-TREE N=%d' % (n + 1), okT, ' | '.join('%s: %s' % (F, [str(x) for x in got[F]]) for F in got))
    # the untilted P3 x P3 tables at K = 4, both N, partners PARTNERS_V1: C-EXACT (+ PLANT-MOM), C-GAUSS, C-ROW0, C-ECON, C-R1,
    # R-SERIES; C-SYM (+ PLANT-SYM) at K = 2
    K = 4
    fpairs = [EDGES[x] for x in PARTNERS_V1]
    series = {}
    for n in (2, 3):
        guard('v1 main N=%d' % (n + 1))
        bd = Build(G9, n, K, EDGES['b0'], fpairs, JGRID[0], KAPPA, RHO2, 'P3xP3 N=%d' % (n + 1), need_tilts=False)
        bad, done = c_exact(bd.T0, 9, rng, 40, 6)
        check('C-EXACT N=%d T0' % (n + 1), bad == 0 and done > 0, '%d of %d monomials match the alpha-permanent' % (done - bad, done))
        wx = aperm(bd.T0.Gl, [0, 0], fmpq(n, 2)) * 4
        hx = bd.T0.mom[(0, 0)][2][tuple([2] + [0] * 8)]
        check('C-EXACT N=%d X0^2' % (n + 1), hx == wx, 'E[X_0^2] %s, 4 per_{n/2} %s' % (hx, wx))
        plant('PLANT-MOM N=%d' % (n + 1), hx + fmpq(1, 10 ** 20) != wx, 'E[X_0^2] + 1e-20 against the same alpha-permanent')
        A1, Ae = bd.a[('1', 0)], bd.a[('e', 0)]
        cs_of = {}
        for b, x in enumerate(PARTNERS_V1, start=1):
            cs_of[x] = cov_series(A1, Ae, bd.a[('f', b)], bd.a[('ef', b)], K)
        for b, (nm, e, f, d2, _) in enumerate(ORBITS, start=1):
            Af, Aef = bd.a[('f', b)], bd.a[('ef', b)]
            cs = cs_of[f]
            series[(nm, n + 1)] = cs
            okG = (A1[0] == 1 and Ae[0] == fmpq(n, 2) * G9.R(*EDGES[e]) and Af[0] == fmpq(n, 2) * G9.R(*EDGES[f])
                   and cs[0] == fmpq(n, 8) * d2)
            check('C-GAUSS %s N=%d' % (nm, n + 1), okG, 'c2 = %s = (N-1) Delta^2 / 8: %s' % (cs[0], cs[0] == fmpq(n, 8) * d2))
            r0 = ROW0[nm][n - 2]
            okR = (Aef[0] == r0[0] and cs[0] == r0[1] and cs[1] == r0[2])
            check('C-ROW0 %s N=%d' % (nm, n + 1), okR, 'A_ef(0) %s (reference %s), c2 %s (%s), c3 %s (%s)' % (
                Aef[0], r0[0], cs[0], r0[1], cs[1], r0[2]))
            out('R-SERIES %s N=%d: c2 %s (%s), c3 %s (%s), c4 %s (%s); a_k(1) %s' % (nm, n + 1, cs[0], f6(cs[0]), cs[1], f6(cs[1]),
                cs[2], f6(cs[2]), [f6(x) for x in A1]))
        for nm, x in (('M1', 'b3'), ('M2', 'b5')):
            cs = cs_of[x]
            series[(nm, n + 1)] = cs
            out('R-SERIES %s N=%d: c2 %s (%s), c3 %s (%s), c4 %s (%s)' % (nm, n + 1, cs[0], f6(cs[0]), cs[1], f6(cs[1]), cs[2], f6(cs[2])))
        okA = (A1[1] == A1ROW0[n] and Ae[0] == fmpq(17 * n, 48)
               and all(bd.a[('f', b)][0] == (fmpq(17 * n, 48) if x[0] == 'b' else fmpq(7 * n, 24)) for b, x in enumerate(PARTNERS_V1, start=1)))
        check('C-ROW0 N=%d a_1, A_b(0), A_s(0)' % (n + 1), okA, 'a_1(F = 1) %s (reference %s); A_b0(0) %s (17n/48 = %s); spokes 7n/24' % (
            A1[1], A1ROW0[n], Ae[0], fmpq(17 * n, 48)))
        rims = [b for b, x in enumerate(PARTNERS_V1, start=1) if x[0] == 'b']
        spk = [b for b, x in enumerate(PARTNERS_V1, start=1) if x[0] == 's']
        okE = all(bd.a[('f', b)] == Ae for b in rims) and all(bd.a[('f', b)] == bd.a[('f', spk[0])] for b in spk)
        check('C-ECON N=%d' % (n + 1), okE, 'a_k (k <= %d) of xi_x equal for b0 and %s, and for %s' % (
            K, [PARTNERS_V1[b - 1] for b in rims], [PARTNERS_V1[b - 1] for b in spk]))
        b1se = Build(G9, n, K, EDGES['b1'], [EDGES['sE']], JGRID[0], KAPPA, RHO2, 'R1 (b1, sE) N=%d' % (n + 1), need_tilts=False)
        cs13 = cov_series(b1se.a[('1', 0)], b1se.a[('e', 0)], b1se.a[('f', 1)], b1se.a[('ef', 1)], K)
        r1s = (cs_of['sN'] == cs_of['sW'], cs_of['b2'] == cs_of['b3'], cs_of['b4'] == cs_of['b5'], cs_of['sE'] == cs13)
        check('C-R1 N=%d' % (n + 1), all(r1s), 'O4 = O5 %s; O1 = M1 %s; O2 = M2 %s; O3 = (b1, sE) %s (series to order %d)' % (r1s + (K,)))
        for b, (nm, e, f, d2, (e2, f2)) in enumerate(ORBITS, start=1):
            bs = Build(G9, n, 2, EDGES[e2], [EDGES[f2]], JGRID[0], KAPPA, RHO2, 'sym %s (%s, %s) N=%d' % (nm, e2, f2, n + 1),
                       need_tilts=False)
            okS = all(bs.a[(F, 0 if F in ('1', 'e') else 1)][k] == bd.a[(F, 0 if F in ('1', 'e') else b)][k] for F in FNAMES for k in range(3))
            check('C-SYM %s N=%d' % (nm, n + 1), okS, 'second member (%s, %s): a_k (k <= 2) equal' % (e2, f2))
        okP = all(bd.a[('ef', 2)][k] == bd.a[('ef', 1)][k] for k in range(3))
        plant('PLANT-SYM N=%d' % (n + 1), not okP, 'O2 against O1 (different orbits) differ')
        del bd, b1se
    # C-H (+ PLANT-H, PLANT-H-ANN) for the tilts of v2/cert
    okc = G9.tilt([C35 / JGRID[0]] * 9)[2]
    okl = all(G9.tilt([KAPPA / (2 * G9.Lpd[v]) if u == v else fmpq(0) for u in range(9)])[2] for v in range(9))
    cpr = q_ceil(up_q(-(arb(1 - RHO2).log()) / (2 * arb(RHO2))), 64)
    oka = all(ann_rates(G9, cpr / JGRID[0], v)[0] is not None for v in range(9))
    check('C-H P3xP3', okc and okl and oka, 'T1 %s, T2 %s, T3 %s' % (okc, okl, oka))
    plant('PLANT-H', not G9.tilt([1 / G9.Lpd[1] if u == 1 else fmpq(0) for u in range(9)])[2], 'kappa = 2 violates (H)')
    plant('PLANT-H-ANN', not G9.tilt([cpr / JGRID[0] + (1 / G9.Lpd[1] if u == 1 else 0) for u in range(9)])[2],
          'annulus tilt with kappa_a = 2 at v1 violates (H)')
    # C-LIT
    c_lit()
    # C-BOUND on P3 (+ PLANT-BOUND)
    c_bound()
    # PLANT-NEG
    t1 = fmpq(1, 100)
    c2 = fmpq(1, 1000)
    Asyn = {'1': [fmpq(1)], 'e': [fmpq(1)], 'f': [fmpq(1)], 'ef': [1 + c2, -8 * c2 / t1, 8 * c2 / (t1 * t1)]}
    L, mono, nneg = phi_scan(Asyn, {F: arb(0) for F in FNAMES}, t1)
    plant('PLANT-NEG', nneg > 0, 'planted dip: %d negative cells, min %s' % (nneg, f6(L)))
    out('READINGS R-SERIES: ' + '; '.join('%s N=%d c2 %s c3 %s c4 %s' % (k[0], k[1], f6(v[0]), f6(v[1]), f6(v[2]))
                                         for k, v in sorted(series.items())))


def c_lit():
    """C-LIT: the riglap2 (RV12_3: matches Lemma 19.1 term by term), float, against this engine on P3 x P3 with pairs (b0, b4)."""
    okc = True
    for fn, want in LIT_SHA.items():
        with open(os.path.join(LIT, fn), 'rb') as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        okc = okc and h == want
    check('C-LIT-COPY', okc, 'lbu_lit_v1 sha256 match: %s' % okc)
    if not okc:
        return
    sys.path.insert(0, LIT)
    import riglap2
    import pseries
    from amom2b import AllMom2
    wf = pseries.w_coeffs(6)
    wd = w_exact(6)
    dw = max(abs(float(wd.get(k, fmpq(0))) - wf.get(k, 0.0)) for k in set(wd) | set(wf))
    check('C-LIT w', dw <= 1e-14, 'max |w exact - w reference| %.2e' % dw)
    KL, n, N = 3, 3, 4
    e, f = EDGES['b0'], EDGES['b4']
    gr = riglap2.Graph(9, {EDGES[x]: 1.0 for x in ELIST}, [e, f], N)
    bd = Build(G9, n, KL, e, [f], JGRID[0], KAPPA, RHO2, 'lit N=4', need_tilts=False)
    R = bd.R

    def to_rig(P, sg):
        d = {}
        for (a, b), p in P.items():
            for m, c in zip(p.monoms(), p.coeffs()):
                d[tuple(m) + (a, 1 if b else 0)] = sg * float(c)
        return d

    def cmp(dr, dm):
        keys = set(dr) | set(dm)
        scale = max([abs(v) for v in dr.values()] + [1e-300])
        return max([abs(dr.get(k, 0.0) - dm.get(k, 0.0)) for k in keys] + [0.0]) / scale
    worst = 0.0
    for F, factors, sh, kmax in (('1', [], 0, KL), ('ef', [('dot', e[0], e[1], 1.0), ('dot', f[0], f[1], 1.0)], 2, 2)):
        guard('C-LIT series ' + F)
        coef = riglap2.Model(gr, kmax + sh, factors).exact()
        key = ('1', 0) if F == '1' else ('ef', 1)
        for k in range(kmax + 1):
            worst = max(worst, cmp(coef[k + sh], to_rig(bd.PS[key][k], 1.0)))
    check('C-LIT series', worst <= 1e-12, 'max relative difference of (F e^H)_k (F = 1, k <= %d; xi_e xi_f, k <= 2): %.2e' % (KL, worst))
    avec, rvec = radii(G9, fmpq(1, 2))
    t = fmpq(1, 120)
    mj = Maj(R, G9, n, avec, rvec, KL)
    mr = riglap2.Majorants(riglap2.Model(gr, KL, []), [float(x) for x in avec], float(t))
    wm = 0.0
    for k in range(1, KL + 2):
        wm = max(wm, cmp(mr.hbar(k).to_dict(), to_rig(mj.h[k], 1.0)))
    db = mj.Dbar('1', bd.ep, None)
    wm = max(wm, cmp(mr.Dbar(KL + 1).to_dict(), to_rig(db[0], 1.0)))
    aa = float(max(avec[e[0]], avec[e[1]]))
    for l in range(0, KL + 2):
        xb = mj.xibar(e[0], e[1], (1, 0), l)
        mine = padd(xb[0], pscale(xb[1], t)) if len(xb) > 1 else xb[0]
        wm = max(wm, cmp(mr.xibar(e[0], e[1], l, aa).to_dict(), to_rig(mine, 1.0)))
    check('C-LIT majorants', wm <= 1e-12, 'max relative difference of h_k, Dbar_%d (F = 1), xibar_l (b0): %.2e' % (KL + 1, wm))
    am = AllMom2(gr.G, gr.n, 2 * KL)
    wa = 0.0
    for k in range(KL + 1):
        P = bd.PS[('1', 0)][k]
        d = {}
        for m, c in zip(P[(0, 0)].monoms(), P[(0, 0)].coeffs()):
            d[tuple(m)] = float(c)
        x = am.E(d) if d else 0.0
        y = float(bd.a[('1', 0)][k])
        wa = max(wa, abs(x - y) / max(abs(y), 1e-300))
    check('C-LIT moments', wa <= 1e-10, 'a_k (F = 1, k <= %d): max relative difference %.2e' % (KL, wa))


def c_bound():
    """C-BOUND: on P3 (exact closed forms) the certified enclosure A_F(t) +- E_F contains the truth (J = 10, 20, 40; N = 3, 4; K = 4);
    PLANT-BOUND: K = 0 without B_rem at N = 4, J = 40 must miss."""
    gt = Graph(3, [(0, 1), (1, 2)])
    sigma = fmpq(2)
    viol = 0
    tot = 0
    for n in (2, 3):
        for K, plantcase in ((4, False), (0, True)):
            if plantcase and n == 2:
                continue
            guard('C-BOUND N=%d K=%d' % (n + 1, K))
            bd = Build(gt, n, K, (0, 1), [(1, 2)], 10, KAPPA, RHO2, 'P3 N=%d K=%d' % (n + 1, K))
            bd.add_sigma(sigma)
            for J in ((40,) if plantcase else (10, 20, 40)):
                tr = tree_truth(n, J)
                t = fmpq(1, J)
                miss = 0
                for F in ('1', 'e', 'ef'):
                    key = (F, 0) if F in ('1', 'e') else (F, 1)
                    tt, th = bd.errors(sigma, J, key, drop_rem=plantcase)
                    Et = tt[0] + tt[1] + tt[2] + tt[3]
                    A = horner(bd.a[key], arb(t))
                    inside = ((A - Et).lower() <= tr[F].lower()) and (tr[F].upper() <= (A + Et).upper())
                    out('BOUND P3 N=%d K=%d J=%d F=%s: A %s, E %s (rem %s tail %s ann %s far %s), truth %s, inside %s' % (
                        n + 1, K, J, F, f6(A), f6(Et), f6(tt[0]), f6(tt[1]), f6(tt[2]), f6(tt[3]), f6(tr[F]), inside))
                    if not inside:
                        miss += 1
                if plantcase:
                    plant('PLANT-BOUND', miss > 0, 'K = 0 without B_rem at J = 40 misses %d of 3' % miss)
                else:
                    viol += miss
                    tot += 3
    check('C-BOUND', viol == 0 and tot > 0, '%d violations in %d enclosures' % (viol, tot))


# ---------------------------------------------------------------- v2 and cert
def run_v2():
    n = 3
    e, f = EDGES['b0'], EDGES['sN']
    for K in (3, 4):
        t0 = cpu()
        bd = Build(G9, n, K, e, [f], JGRID[0], KAPPA, RHO2, 'O4 N=4 K=%d' % K)
        for sigma in SIGMAS:
            bd.add_sigma(sigma)
        best = certify(bd, 1, SIGMAS, JGRID, 'O4 N=4 K=%d' % K)
        if best is None:
            out('R-J1 O4 N=4 K=%d: none on the grid' % K)
        else:
            out('R-J1 O4 N=4 K=%d: J1 %d, sigma %s, L %s; E %s; theta %s' % (K, best['J1'], best['sigma'], f6(best['L']),
                {F: f6(best['Eu'][F]) for F in FNAMES}, best['ths']))
        out('CPU O4 N=4 K=%d: %.2f s; peak RSS %.0f MB' % (K, cpu() - t0, rss_mb()))
        del bd


def run_cert():
    K = KCERT
    orbs = [o for o in ORBITS if SET == 'all' or o[0] == 'O4']
    fpairs = [EDGES[o[2]] for o in orbs]
    res = {}
    for n in (2, 3):
        t0 = cpu()
        bd = Build(G9, n, K, EDGES['b0'], fpairs, JGRID[0], KAPPA, RHO2, 'cert %s N=%d K=%d' % (SET, n + 1, K))
        for sigma in SIGMAS:
            bd.add_sigma(sigma)
        for b, (nm, e, f, d2, _) in enumerate(orbs, start=1):
            best = certify(bd, b, SIGMAS, JGRID, '%s N=%d K=%d' % (nm, n + 1, K))
            res[(nm, n + 1)] = best
            if best is None:
                out('R-J1 %s N=%d K=%d: none on the grid' % (nm, n + 1, K))
                continue
            out('R-J1 %s N=%d K=%d: J1 %d, sigma %s, L %s (c2 %s); E %s; theta %s' % (nm, n + 1, K, best['J1'], best['sigma'],
                f6(best['L']), f6(fmpq(n, 8) * d2), {F: f6(best['Eu'][F]) for F in FNAMES}, best['ths']))
            if nm == 'O3':
                Acoef = {F: bd.a[(F, 0) if F in ('1', 'e') else (F, b)] for F in FNAMES}
                cs = cov_series(Acoef['1'], Acoef['e'], Acoef['f'], Acoef['ef'], K)
                for J in (100, 150, 200):
                    if J < best['J1']:
                        continue
                    t = fmpq(1, J)
                    Lj, mono, nneg = phi_scan(Acoef, best['Eu'], t, ncell=1)
                    cen = sum((cs[k] * t ** k for k in range(K + 1)), fmpq(0))
                    data = CDATA[(n + 1, J)] * J * J
                    ok = float(Lj) <= data * (1 + 1e-5) and (J != 200 or abs(float(cen) - data) <= 1e-3 * data)
                    check('C-DATA O3 N=%d J=%d' % (n + 1, J), ok, 'certified %s <= data %.6e; central %s' % (f6(Lj), data, f6(cen)))
        out('CPU cert N=%d: %.2f s; peak RSS %.0f MB' % (n + 1, cpu() - t0, rss_mb()))
        del bd
    js = [v['J1'] for v in res.values() if v is not None]
    allc = all(v is not None for v in res.values())
    out('READINGS R-J1: ' + '; '.join('%s N=%d %s' % (k[0], k[1], v['J1'] if v else 'none') for k, v in sorted(res.items())))
    out('READINGS LB_u J1 (SET %s) = %s (all certified on the grid: %s)' % (SET, max(js) if js and allc else 'none', allc))


# ---------------------------------------------------------------- pk06: P2-13 short strips on the grid P_R x P_C (PK06 CHANGES)
MOM_PROGRESS = False
MEM_STOP_MB = 0
# ASSESS_SHORT_STRIPS_REACH_rv02.md (d9381662): (pairs, orbits, orbits with a middle-row edge)
REV_ENUM = {(3, 4): (72, 19, 8), (3, 5): (138, 36, 15)}
TAU_GRID = {(2, 3): 15, (2, 4): 56, (3, 3): 192, (3, 4): 2415, (3, 5): 30305}  # PK21 (3, 5)
# out_kt_lbu_v1_1_cert.out (309fb3fb) l.89: R-J1 O4 N=3 K=4: J1 80, sigma 3/5, L 2.241485e-04 (its tables use Jmin = JGRID[0] = 50)
CONTROL33 = ('b0', 'sN', 2, 4, 50, 80, fmpq(3, 5), '2.241485e-04')


def mom_progress(mo, R, M, cap, k, kmax, V, tag, t0):
    """PK06 (g6), T1 tables only: one MOMDEG line per degree k, the CPU guard, and the memory stop before degree k + 1 (predicted
    peak = rss + 4 (rss - rss0) next / done) or before the factorial pass (rss + 1.5 (rss - rss0) largest pattern / done)."""
    if ' T1' not in tag:
        return
    done = sum(len(p) for P in R.pats for p in M[P] if p is not None)
    if k < kmax:
        nxt, fac = 0, 4.0
        for P in R.pats:
            d = k + 1 - R.q(P)
            if 0 <= d <= cap[P]:
                nxt += math.comb(V + d - 1, d)
    else:
        nxt, fac = max(sum(len(p) for p in M[P] if p is not None) for P in R.pats), 1.5
    r = rss_mb()
    pred = r + fac * max(r - mo.rss0, 1.0) * nxt / max(done, 1)
    out('MOMDEG %s k=%d: %d terms, cpu %.2f s, peak RSS %.0f MB; next %d terms, predicted peak %.0f MB' % (
        tag, k, done, cpu() - t0, r, nxt, pred))
    if MEM_STOP_MB and pred > MEM_STOP_MB:
        raise GuardStop('memory stop after %s k=%d (predicted peak %.0f MB > %d MB)' % (tag, k, pred, MEM_STOP_MB))
    guard('moments %s after k=%d' % (tag, k))


def xcpu_stop(signum, frame):
    raise GuardStop('SIGXCPU at cpu %.1f s' % cpu())


def grid_build(R_, C_):
    """PK06 (g1): P_R x P_C, vertex (r, c) = r C + c; h<r><c> = ((r, c), (r, c + 1)), v<r><c> = ((r, c), (r + 1, c))."""
    ed = {}
    for r in range(R_):
        for c in range(C_ - 1):
            ed['h%d%d' % (r, c)] = (r * C_ + c, r * C_ + c + 1)
    for r in range(R_ - 1):
        for c in range(C_):
            ed['v%d%d' % (r, c)] = (r * C_ + c, (r + 1) * C_ + c)
    names = list(ed)
    return Graph(R_ * C_, [ed[x] for x in names]), ed, names


def grid_maps(R_, C_, ed):
    """the top-bottom and the left-right reflection, on vertices and on edge names."""
    tbv = [(R_ - 1 - v // C_) * C_ + v % C_ for v in range(R_ * C_)]
    lrv = [(v // C_) * C_ + (C_ - 1 - v % C_) for v in range(R_ * C_)]
    inv = {frozenset(p): x for x, p in ed.items()}
    tb = {x: inv[frozenset((tbv[p[0]], tbv[p[1]]))] for x, p in ed.items()}
    lr = {x: inv[frozenset((lrv[p[0]], lrv[p[1]]))] for x, p in ed.items()}
    return tbv, lrv, tb, lr


def grid_orbits(ed, names, tb, lr):
    """PK06 (g2): the pair list and its orbits under {id, tb, lr, tb lr}."""
    pairs = []
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            if x[0] != 'h' and y[0] != 'h':
                continue
            if set(ed[x]) & set(ed[y]):
                continue
            if tb[x] == y or lr[x] == y:
                continue
            pairs.append(frozenset((x, y)))
    pset = set(pairs)
    group = [lambda z: z, lambda z: tb[z], lambda z: lr[z], lambda z: tb[lr[z]]]
    seen, orbits = set(), []
    for p in pairs:
        if p in seen:
            continue
        orb = {frozenset(gm(z) for z in p) for gm in group}
        assert orb <= pset
        seen |= orb
        orbits.append(sorted(orb, key=sorted))
    return pairs, orbits, group


def edge_dist(C_, p, q):
    """the smallest grid distance between an endpoint of p and an endpoint of q."""
    return min(abs(u // C_ - w // C_) + abs(u % C_ - w % C_) for u in p for w in q)


def phi_cells(Acoef, Eu, t1, ncell=64):
    """phi_scan's cells and per-cell lower bound, unchanged, as a list of (lo_t, hi_t, Phi_lo, the cell passes) (PK06 (g5))."""
    res = []
    for i in range(ncell):
        lo_t = t1 * i / ncell
        hi_t = t1 * (i + 1) / ncell
        tb = arb((lo_t + hi_t) / 2) + arb(0, (hi_t - lo_t) / 2)
        val = {F: horner(Acoef[F], tb) for F in FNAMES}
        i1l = (val['1'] - Eu['1']).lower()
        i1h = (val['1'] + Eu['1']).upper()
        iel = (val['e'] - Eu['e']).lower()
        ieh = (val['e'] + Eu['e']).upper()
        ifl = (val['f'] - Eu['f']).lower()
        ifh = (val['f'] + Eu['f']).upper()
        iefl = (val['ef'] - Eu['ef']).lower()
        iefh = (val['ef'] + Eu['ef']).upper()
        if not (i1l > 0 and iel > 0 and ifl > 0 and iefl > 0):
            res.append((lo_t, hi_t, arb(-1), False))
            continue
        mono = bool(2 * iel * ifl - iefh * i1h > 0)
        ph = (iefl / i1l - ieh * ifh / (i1l * i1l)).lower()
        res.append((lo_t, hi_t, ph, mono and bool(ph > 0)))
    return res


def run_grid():
    global MOM_PROGRESS, MEM_STOP_MB
    signal.signal(signal.SIGXCPU, xcpu_stop)
    K, Rr, Cc, N, J1 = KCERT, G_ROWS, G_COLS, G_N, G_J1
    n = N - 1
    t1 = fmpq(1, J1)
    out('ARGS grid: K %d, P_%d x P_%d, N %d, J1 %d (t in (0, 1/%d]), ORBS %s, SIGS %s, CONTROLS %s, MEMSTOP %d MB' % (
        K, Rr, Cc, N, J1, J1, G_ORBS, G_SIGS, G_CONTROLS, G_MEMSTOP))
    sigmas = SIGMAS if G_SIGS == 'all' else [fmpq(*(int(x) for x in s_.split('/'))) for s_ in G_SIGS.split(',')]
    assert all(sg in SIGMAS for sg in sigmas), 'sigmas must come from SIGMAS'
    rng = random.Random(20261111)
    if G_CONTROLS == 'desk':
        e3, f3, n3, K3, Jm3, J3, s3, L3 = CONTROL33
        lab = 'control33 O4 N=%d K=%d' % (n3 + 1, K3)
        bdc = Build(G9, n3, K3, EDGES[e3], [EDGES[f3]], Jm3, KAPPA, RHO2, lab)
        bdc.add_sigma(s3)
        bc = certify(bdc, 1, [s3], [J3], lab)
        check('C-CONTROL33', bc is not None and f6(bc['L']) == L3, 'J1 %d sigma %s: L %s; certified run l.89: %s' % (
            J3, s3, f6(bc['L']) if bc else 'none', L3))
        del bdc
        c_bound()
    g, ed, names = grid_build(Rr, Cc)
    V = g.V
    tbv, lrv, tb, lr = grid_maps(Rr, Cc, ed)
    foster = sum((g.R(*ed[x]) for x in names), fmpq(0))
    okS = all(g.Lp[u, w] == g.Lp[tbv[u], tbv[w]] and g.Lp[u, w] == g.Lp[lrv[u], lrv[w]] for u in range(V) for w in range(V))
    check('C-GRAPH-G', g.tau == TAU_GRID.get((Rr, Cc)) and foster == V - 1 and okS,
          'P_%d x P_%d: tau %s (expected %s); Foster %s (V - 1 = %d); L+ invariant under both reflections %s' % (
              Rr, Cc, g.tau, TAU_GRID.get((Rr, Cc)), foster, V - 1, okS))
    pairs, orbits, group = grid_orbits(ed, names, tb, lr)
    midrow = 'h%d' % (Rr // 2) if Rr % 2 == 1 else None
    table = []
    okD = True
    for o in orbits:
        cands = []
        for q in o:
            a_, b_ = sorted(q)
            for (x, y) in ((a_, b_), (b_, a_)):
                if x[0] == 'h':
                    cands.append((x, y))
        e_, f_ = min(cands)
        d_ = delta_of(g, ed[e_], ed[f_])
        okD = okD and all(delta_of(g, ed[sorted(q)[0]], ed[sorted(q)[1]]) ** 2 == d_ * d_ for q in o)
        ism = midrow is not None and any(z.startswith(midrow) for q in o for z in q)
        table.append([e_, f_, len(o), ism, d_, edge_dist(Cc, ed[e_], ed[f_]), o])
    table.sort(key=lambda r: (r[0], r[1]))
    got = (len(pairs), len(orbits), sum(1 for r in table if r[3]))
    want = REV_ENUM.get((Rr, Cc))
    if want is not None:
        check('C-ENUM', got == want, 'pairs %d, orbits %d, orbits with a middle-row edge %d; reference counts %s' % (got + (want,)))
    else:
        out('ENUM P_%d x P_%d: pairs %d, orbits %d, orbits with a middle-row edge %d (no reference count)' % ((Rr, Cc) + got))
    check('C-ORBIT-DELTA', okD, 'Delta^2 equal over every orbit: %s' % okD)
    for i, r in enumerate(table, start=1):
        r.insert(0, 'G%02d' % i)
        nm, e_, f_, size, ism, d_, dist, o = r
        out('ORBIT %s (%s, %s): size %d, middle-row %s, distance %d, Delta %s, Delta^2 %s, c2(N=%d) %s (%s); members %s' % (
            nm, e_, f_, size, ism, dist, d_, d_ * d_, N, fmpq(n, 8) * d_ * d_, f6(fmpq(n, 8) * d_ * d_),
            ' '.join('(%s, %s)' % tuple(sorted(q)) for q in o)))
        if d_ == 0:
            out('WARNING %s: Delta = 0, the leading term vanishes' % nm)
    if G_ORBS == 'all':
        sel = table
    elif G_ORBS == 'far':
        pool = [r for r in table if r[4]] or table
        sel = [min(pool, key=lambda r: (r[5] * r[5], -r[6]))]
    else:
        wn = G_ORBS.split(',')
        sel = [r for r in table if r[0] in wn]
        assert len(sel) == len(wn), 'unknown orbit name in %s' % G_ORBS
    out('SELECT %s' % ', '.join('%s (%s, %s)' % (r[0], r[1], r[2]) for r in sel))
    res = {}
    for (nm, e_, f_, size, ism, d_, dist, o) in sel:
        t0 = cpu()
        tag = '%s (%s, %s) N=%d K=%d' % (nm, e_, f_, N, K)
        c2 = fmpq(n, 8) * d_ * d_
        bd0 = Build(g, n, K, ed[e_], [ed[f_]], J1, KAPPA, RHO2, 'series ' + tag, need_tilts=False)
        A0 = {F: bd0.a[(F, 0) if F in ('1', 'e') else (F, 1)] for F in FNAMES}
        cs = cov_series(A0['1'], A0['e'], A0['f'], A0['ef'], K)
        okG = (A0['1'][0] == 1 and A0['e'][0] == fmpq(n, 2) * g.R(*ed[e_]) and A0['f'][0] == fmpq(n, 2) * g.R(*ed[f_])
               and cs[0] == c2)
        check('C-GAUSS %s' % tag, okG, 'c2 = %s = (N-1) Delta^2 / 8: %s' % (cs[0], cs[0] == c2))
        cen = sum((cs[k] * t1 ** k for k in range(K + 1)), fmpq(0))
        out('R-SERIES %s: c2 %s (%s), c3 %s (%s), c4 %s (%s); central value at t = 1/%d %s = %s c2' % (
            tag, cs[0], f6(cs[0]), cs[1], f6(cs[1]), cs[2], f6(cs[2]), J1, f6(cen), f6(cen / cs[0]) if cs[0] != 0 else 'inf'))
        bad, done = c_exact(bd0.T0, V, rng, 10, 6)
        check('C-EXACT %s T0' % tag, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
        bad, done = c_exact(bd0.T0, V, rng, 10, 6, perturb=True)
        plant('PLANT-MOM %s T0' % tag, bad > 0, 'one moment + 1e-20: %d of %d differ' % (bad, done))
        Af0 = dict(A0)
        Af0['ef'] = [A0['ef'][0] - 2 * c2] + list(A0['ef'][1:])
        Lz, mz, nz = phi_scan(Af0, {F: arb(0) for F in FNAMES}, t1)
        plant('PLANT-FALSE-MOM %s E=0' % tag, nz > 0, 'A_ef(0) - 2 c2, zero errors: %d negative cells, min %s' % (nz, f6(Lz)))
        q0 = frozenset((e_, f_))
        oth = [q for q in o if q != q0]
        if oth:
            gm = [h for h in group if frozenset((h(e_), h(f_))) == oth[0]][0]
            x2, y2 = gm(e_), gm(f_)
            bs = Build(g, n, 2, ed[x2], [ed[y2]], J1, KAPPA, RHO2, 'sym %s (%s, %s) N=%d' % (nm, x2, y2, N), need_tilts=False)
            okS = all(bs.a[(F, 0) if F in ('1', 'e') else (F, 1)][k] == A0[F][k] for F in FNAMES for k in range(3))
            check('C-SYM %s' % tag, okS, 'second member (%s, %s): a_k (k <= 2) equal' % (x2, y2))
            del bs
        del bd0
        MOM_PROGRESS, MEM_STOP_MB = True, G_MEMSTOP
        bd = Build(g, n, K, ed[e_], [ed[f_]], J1, KAPPA, RHO2, 'cert ' + tag)
        MOM_PROGRESS, MEM_STOP_MB = False, 0
        for sigma in sigmas:
            bd.add_sigma(sigma)
        best = certify(bd, 1, sigmas, [J1], tag)
        Acoef = {F: bd.a[(F, 0) if F in ('1', 'e') else (F, 1)] for F in FNAMES}
        pts = []
        for sigma in sigmas:
            Eu, terms = {}, {}
            for F in FNAMES:
                tt, th = bd.errors(sigma, J1, (F, 0) if F in ('1', 'e') else (F, 1))
                terms[F] = tt
                Eu[F] = arb(up_q(tt[0] + tt[1] + tt[2] + tt[3]))
            cells = phi_cells(Acoef, Eu, t1)
            pts.append((min(c_[2] for c_ in cells), sigma, Eu, cells, terms))
        if best is not None:
            pt = [p_ for p_ in pts if p_[1] == best['sigma']][0]
        else:
            pt = max(pts, key=lambda p_: p_[0])
        Lc, sg, Eu, cells, terms = pt
        Ls, ms, ns = phi_scan(Acoef, Eu, t1)
        check('C-CELLS %s' % tag, Ls == Lc and ns == sum(1 for c_ in cells if not c_[2] > 0),
              'per-cell minimum %s, phi_scan %s; negative cells %d' % (f6(Lc), f6(Ls), ns))
        okc = best is not None
        cs2 = cov_series(Acoef['1'], Acoef['e'], Acoef['f'], Acoef['ef'], K)
        out('R-CERT %s J1 %d: certified %s; sigma %s; L %s; c2 %s; L / c2 %s; E %s; terms (rem, tail, ann, far) %s' % (
            tag, J1, okc, sg, f6(Lc), f6(c2), f6(Lc / arb(c2)) if c2 != 0 else 'inf', {F: f6(Eu[F]) for F in FNAMES},
            {F: [f6(x) for x in terms[F]] for F in FNAMES}))
        for i, (lo_t, hi_t, ph, okp) in enumerate(cells):
            tm = (lo_t + hi_t) / 2
            sv = sum((cs2[k] * tm ** k for k in range(K + 1)), fmpq(0))
            out('CELL %s %02d t [%s, %s]: Phi_lo %s, Phi_lo / c2 %s, series at mid %s, pass %s' % (
                nm, i, f6(lo_t), f6(hi_t), f6(ph), f6(ph / arb(c2)) if c2 != 0 else 'inf', f6(sv), okp))
        Af1 = dict(Acoef)
        Af1['ef'] = [Acoef['ef'][0] - 2 * c2] + list(Acoef['ef'][1:])
        Lf, mf, nf = phi_scan(Af1, Eu, t1)
        plant('PLANT-FALSE-MOM %s' % tag, nf > 0, 'A_ef(0) - 2 c2 with the errors at sigma %s: %d negative cells, min %s' % (
            sg, nf, f6(Lf)))
        bad, done = c_exact(bd.T1, V, rng, 10, 6, perturb=True)
        plant('PLANT-MOM %s T1' % tag, bad > 0, 'one T1 moment + 1e-20: %d of %d differ' % (bad, done))
        if G_CONTROLS == 'desk':
            check('C-CERT-CONTROL %s' % tag, okc, 'the selected orbit certifies at J1 %d: %s' % (J1, okc))
        res[nm] = (okc, Lc, c2)
        out('CPU %s: %.2f s; peak RSS %.0f MB' % (tag, cpu() - t0, rss_mb()))
        del bd
    out('READINGS CERT P_%d x P_%d N=%d K=%d J1 %d: %s' % (Rr, Cc, N, K, J1, '; '.join('%s certified %s L/c2 %s' % (
        k_, v[0], f6(v[1] / arb(v[2])) if v[2] != 0 else 'inf') for k_, v in res.items())))


# ---------------------------------------------------------------- main
def main():
    out('kt_lbu_g34_pk06_v1 mode %s LIM %d K %d SET %s | python %s | python-flint %s | prec %d | sha256 %s' % (MODE, LIM, KCERT,
        SET, sys.version.split()[0], flint.__version__, FLINT.prec, SELF_SHA))
    status = 'DONE'
    try:
        if MODE == 'v1':
            run_v1()
        elif MODE == 'v2':
            run_v2()
        elif MODE == 'grid':
            run_grid()
        else:
            run_cert()
    except GuardStop as ex:
        status = 'INCOMPLETE (guard stop at %s)' % ex
    allc = all(CHECKS.values()) if CHECKS else False
    allp = all(PLANTS.values()) if PLANTS else (MODE not in ('v1', 'grid'))
    out('CHECKS %s' % CHECKS)
    out('PLANTS %s' % PLANTS)
    if status != 'DONE':
        verdict = 'INCOMPLETE'
    else:
        verdict = 'VALID' if allc and allp else 'INVALID'
    out('SUMMARY mode %s: status %s; checks %d/%d; plants %d/%d; VERDICT %s; cpu %.2f s; wall %.2f s; peak RSS %.0f MB' % (
        MODE, status, sum(CHECKS.values()), len(CHECKS), sum(PLANTS.values()), len(PLANTS), verdict, cpu(), time.time() - T_START,
        rss_mb()))


T_START = time.time()
main()
