#!/usr/bin/env python3
# cs33h_1_rh_cert.py (pk05, P-RH Stage B v1_8 of cs33h_rh_cert 4120f9ee): certified cover of GKS-II on
# the uniform 3 x n strip, N = 3, 4, J in [20, 300], for every pair of edges of every strip with n >= 4 columns, by the coverage table below.
# v1_1 (cs33b): family Taylor models of degree K_F, each interval certified in two items (part A far pairs, part B near pairs, or B as
# Bh + Bv), each recomputing the spectral part; inner products from one BLAS Gram product. v1_2 (cs33c): same-column pairs left to the
# shared-vertex theorem (scope change after the cs33b smoke, out/cs33b_smoke.out feab303a). V1_3 (cs33d), after
# the cs33c pilot at J = 300 (out/cs33c_pilotA.out 78127b83: FAR balls containing 0, no negatives) and the diagnostic dg2 (d12f5641,
# out/dg2_far_budget.out a94471d4: the error is degree truncation growing with p, amplified by centring; not the a~ remainder):
# (NORM) every propagation step is multiplied by a positive scalar polynomial p(t) ~ 1/mu_0(t) (inf p > 0 certified per interval, C-POS);
# (PAR) odd-mode coefficients of rho-even objects are set to exactly 0; the TM degree K (kernels, modes, family) is an item parameter,
# K in {3, 4}; P-NODE scales every E~_m by (1 + 1e-6). Facts (NORM) and (PAR) are proved below; LEMMA_STRIP_RH_v1_2 will carry them.
# v1_4 (cs33e), after the cs33d pilots at J = 300 (out/cs33d_pilotA_K4.out ecd5d38e: 112 FAR failures, exactly the pairs (mh, p),
# (mh, inf), where the mh lead (c_mh)^2 ~ 2e-6 lies below the mh INF Delta tail 8.75e-6 at depth 6): (DEPTH) the mh objects run to
# p < 9 and the INF mh object starts at p = 9 (PE[mh] = 9; 6 for the other types), so its Delta bound shrinks by about 0.146^3.
# v1_5 (cs33f): the truncation is accounted by the proved bound of LEMMA_STRIP_R9_v1 (TR1-TR7), replacing cs33e's unproved inner-product
# slack (all cs33e certificates superseded, LEDGER_NOTES_pk05 31fd26f3): slack_f per interval from eps_T, eps_e, eps_W, kappa, rho, c
# (TRUNC line, control C-SLACK); Davis-Kahan sines carry sqrt(nu0/nu_a); delta_bounds uses |R' T~| for the remainder and the
# tail norms of R' chi_a, T' chi_a. v1_6 (cs33g): the TRUNC line also prints rho per object type; the insertion factor of every
# horizontal object is max(Rop_e, 1) (R9 v1_1), which cs33f's code already used. v1_7 (cs33h): the vertical enclosure
# num in delta_bounds adds 2^-52 |alpha_e mu_a(0)| |u_a| for the float coefficient fl(alpha_e mu_a(0)) of XC (R9 TR7);
# v1_8 (this file), the review of R10 (f0c81dbc): Z1 the Davis-Kahan gap of R4 (iii) is g - eps_j (sb_spectral); Z3 Rop rounded up
# in delta_bounds; Z4 the gap minimum takes the lower ends (lmin); Z5 the INF error multipliers |J_Y||I_Y| carry (1 + slack_f); Z7
# comments (J >= 0 below; Wc_* unused). No other change.
# COVERAGE TABLE (pairs of distinct edges e, f of the 3 x n strip, J in [20, 300], N = 3, 4):
#  n = 1: a tree (Cov = 0). n = 2: the 3 x 2 grid, a ladder: LAD (RV21_55, RV22_47). n = 3: the 3 x 3 box (done).
#  n >= 4, e and f the two vertical edges of one column: they share the middle vertex; the shared-vertex theorem (the E10 adjacent-pair
#   reduction via Dunlop; the paper's sections 2-3) covers every graph, every coupling J >= 0 and N = 3, 4.
#  n >= 4, every other pair: e precedes f with k >= 0 complete factors T~ between their insertions; NEAR checks (k < K_EX, part B or
#   Bh + Bv) and FAR checks (k >= K_EX, part A) below. In particular the three same-gap horizontal pairs (th_x, mh_x), (th_x, bh_x),
#   (mh_x, bh_x) share no vertex and stay in the verdict: they are the NEAR checks at k = 0 with both objects horizontal (part B or Bh;
#   n = p + q + 2, the two insertions multiply one kernel).
# Math: LEMMA_STRIP_RH_v1_1 (2d0e7bea) R1-R6 and the facts below [S] (R7-R9 notes follow). Core: cs33b_rh_core.py (929ab8a0, unchanged,
# sha-checked), which loads route H's hubcert_v1e (c08d33c1).
