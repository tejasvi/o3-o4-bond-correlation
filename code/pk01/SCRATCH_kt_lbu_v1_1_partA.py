#!/usr/bin/env python3
"""kt_lbu_v1_1.py -- pk01 (code/pk01/). Revision of kt_lbu_v1.py (b1fdda19; frozen, never run, never sent) for the review items of
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
"""
import resource, sys, time, math, os, hashlib, random, itertools

MODES = {'v1': (20, 300), 'v2': (60, 900), 'cert': (60, 3000)}
if len(sys.argv) < 3 or sys.argv[1] not in MODES:
    print('usage: kt_lbu_v1_1.py MODE LIM [K [SET]]   (MODE v1 | v2 | cert; LIM = RLIMIT_CPU soft limit in s, hard LIM + 2; '
          'K for cert, 3..5; SET for cert, O4 or all)')
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2])
if not (MODES[MODE][0] <= LIM <= MODES[MODE][1]):
    print('bad LIM %d for mode %s (need %d..%d)' % (LIM, MODE, MODES[MODE][0], MODES[MODE][1]))
    sys.exit(2)
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
LIT = os.path.join(HERE, 'lbu_lit_v1')
LIT_SHA = {'riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
           'pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
           'npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
           'amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc'}


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
