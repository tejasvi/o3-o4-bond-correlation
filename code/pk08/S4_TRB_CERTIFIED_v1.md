# S4_TRB_CERTIFIED_v1: the single record of S4's certified TRB (beta), twrig4's bound for tr_H(T_xi)/lambda_h, one constant per N,
# for pk11's provider and C-FMT (S6/S7) and the paper.
# Format S4U_KV_v1: one "KEY = value" per line; lines starting with # are comments; blank lines carry nothing.
# Numbers are decimal upper ends as printed by the producing asm output (one-sided, W1; *_HEADROOM is a lower end), or exact bc results
# from them (keys *_MINUS_*, *_REL). File tokens are path:sha8, with paths relative to /mnt/g2/release/root/code/; several
# tokens are separated by " ; ". Every sha8 below was computed by sha256sum when this file was assembled; every REASON_* value is copied
# from the asm outputs' REASON lines (identical at both N) when this file was assembled.
FORMAT = S4U_KV_v1
RECORD = S4_TRB_CERTIFIED_v1
AUTHOR = pk08
WRITTEN_UTC = 2026-11-07T11:24:11Z
CLAIM = for N in {3, 4} and every J >= 300 (t = 1/J <= 1/300): tr_H(T_xi)/lambda_h <= N*_TRB, one constant per N
DOMAIN = J >= 300, N in {3, 4}; a = aZ = 1/4, eps = 9/20, lam = 17/40, 17/40, 119/200 (theta 17/20)
J_MIN = 300
CHAIN = TRB = main + R3 + R_cub + R_F + tail + far at t = 1/300, the moved-out chain of S4_TRB_DESIGN_v2 item 2 with FIX F1; T_v <= (1 - theta2)^{-d/2} I[1], theta2 = 9/10
TARGET_T2 = N4 1.338859 ; N3 0.961107
TARGET_T2_SOURCE = T2 of pk11 joint P0 v1_2 bdbe992f (x1.02 of twrig4's J = 170 float), held to directly (D2); sha8
CODE = pk08/px08_trbcert_v1_1.py:6a851374
CODE_MANIFEST = pk08/MANIFEST_px08_trbcert_v1_1.sha256:944432fa
CODE_DIFF = pk08/diff_px08_trbcert_v1_v1_1.txt:a1fc28bd ; pk08/px08_trbcert_v1.py:26d5fa3d
COPIED_BLOCKS = pk08/COPIED_BLOCKS_px08_trbcert_v1_1.txt:adbdf539 ; pk08/px08_m2bc4.py:6527d21b
REVIEW = rv01/CHECK_S4_TRB_DESIGN_v1_rv01.md:186cc2a3 ; rv01/DELTA_S4_TRB_DESIGN_v2_rv01.md:03847ae7 ; rv01/CHECK_S4_TRB_CODE_PLAN_v1_rv01.md:e242dc82 ; rv01/REVIEW_PX08_TRBCERT_V1_rv01.md:a7a44422
DESIGN = pk08/S4_TRB_DESIGN_v2.md:1d083d7f ; pk08/S4_TRB_CODE_PLAN_v1.md:2811b3a3
DRY_RUN = pk08/out/px08_trbscan_v2_n4.out:b612df5b ; pk08/out/px08_trbscan_v2_n3.out:11472c2f ; pk08/MANIFEST_px08_trbscan_v2_out.sha256:11e03247
CORE_H = 0.0801

# ---- N = 4 ----
N4_TRB = 1.30797171127e+0
N4_TRB_MAIN = 1.30762220403e+0
N4_TRB_R3 = 5.63217192098e-5
N4_TRB_RCUB = 2.87067649157e-4
N4_TRB_RF = 4.36891913165e-6
N4_TRB_TAIL = 1.74895315211e-6
N4_TRB_FAR = 3.87334475082e-12
N4_PR = 4.44264196945e+1
N4_TV = 4.20642701144e+1
N4_S1 = [0.82337948 +/- 3.15e-9]
N4_S2 = [0.81645478 +/- 5.14e-9]
N4_T2_TARGET = 1.338859
N4_T2_RESULT = PASS
N4_T2_HEADROOM = 3.08872887310e-2
N4_T2_HEADROOM_REL = 2.306e-2
N4_DRY_RUN = 1.307970642
N4_CERT_MINUS_DRY = 1.06927e-6
N4_SIGMA = 0.5
N4_M = 64
N4_G_BOXES = 57
N4_TARGET_MISSES = none
N4_C_SCAN_WORST_EXCESS = 0.000e+00
N4_C_SCAN_LEAD_REL = 2.451e-09
N4_VERDICT = VALID
N4_ASM_OUTPUT = pk08/out/px08_trbcert_v1_1_n4_asm.out:9d3e8f62
N4_ASM_MANIFEST = pk08/MANIFEST_px08_trbcert_v1_1_n4_asm_out.sha256:793f2510
N4_PARTS = pk08/MANIFEST_parts_n4_trbcert_v1_1.sha256:2dc3814e ; pk08/MANIFEST_nodes_n4_trbcert_v1_1.sha256:d1dfd97f
N4_COV_OUTPUT = pk08/out/px08_trbcert_v1_1_n4_cov.out:a845eb48

# ---- N = 3 ----
N3_TRB = 9.39977769617e-1
N3_TRB_MAIN = 9.39888415643e-1
N3_TRB_R3 = 2.40694032498e-5
N3_TRB_RCUB = 6.30160611561e-5
N3_TRB_RF = 1.49267852587e-6
N3_TRB_TAIL = 7.75831677767e-7
N3_TRB_FAR = 7.91355623696e-14
N3_PR = 1.25437544346e+1
N3_TV = 1.33018901674e+1
N3_S1 = [0.72713055 +/- 2.73e-9]
N3_S2 = [0.71720344 +/- 4.53e-9]
N3_T2_TARGET = 0.961107
N3_T2_RESULT = PASS
N3_T2_HEADROOM = 2.11292303831e-2
N3_T2_HEADROOM_REL = 2.198e-2
N3_DRY_RUN = 0.939977441
N3_CERT_MINUS_DRY = 3.28617e-7
N3_SIGMA = 0.5
N3_M = 64
N3_G_BOXES = 72
N3_TARGET_MISSES = none
N3_C_SCAN_WORST_EXCESS = 0.000e+00
N3_C_SCAN_LEAD_REL = 2.451e-09
N3_VERDICT = VALID
N3_ASM_OUTPUT = pk08/out/px08_trbcert_v1_1_n3_asm.out:ff2d93d0
N3_ASM_MANIFEST = pk08/MANIFEST_px08_trbcert_v1_1_n3_asm_out.sha256:f3711b04
N3_PARTS = pk08/MANIFEST_parts_n3_trbcert_v1_1.sha256:8610e420 ; pk08/MANIFEST_nodes_n3_trbcert_v1_1.sha256:ccdaf169
N3_COV_OUTPUT = pk08/out/px08_trbcert_v1_1_n3_cov.out:bb189a4d

# ---- rules and reasons ----
TRB_RULE = N*_TRB is the asm READING's upper end of main + R3 + R_cub + R_F + tail + far (each piece an upper end, PR included)
T2_RULE = C-T2 PASS means N*_TRB <= the lower end of the exact decimal target; N*_T2_HEADROOM is the printed lower end of target - TRB; the C-T2 line prints the target's ball upper end rounded up (1.338860e+0, 9.611071e-1), a display rounding only
HEADROOM_REL_RULE = N*_T2_HEADROOM_REL = N*_T2_HEADROOM / N*_T2_TARGET (bc), rounded down at 4 digits
CERT_MINUS_DRY_RULE = N*_CERT_MINUS_DRY = N*_TRB - N*_DRY_RUN (bc); N*_DRY_RUN is the dry run's moved-out value at eps 0.45 (KILL-RULE line)
REASON_MAIN = C-SIGN gives s1, s2 > 0, so main(t) = I[FE0] (1 + s1 t + s2 t^2) increases in t; its t = 1/300 value bounds every J >= 300
REASON_R3 = t^3 and t^4 times untilted integrals of fixed polynomials (twlib hbar(j, a, aZ) has no t): nondecreasing in t
REASON_RCUB = Q_t(t') >= Q_t(1/300) in the Loewner order for t' <= 1/300 (the t-part t cfun(a_v) of the tilt is PSD), the integrands X_T^4, H1^4, hhat^4 are >= 0, hhat(t') <= hhat(1/300) monomialwise, and t^3 grows: nondecreasing in t
REASON_RF = (t^3/6) E3(a) I_t[X_T^4], with I_t nondecreasing in t as for R_cub: nondecreasing in t
REASON_TAIL = e^{-lam_v J a_v} decreases in J; T_v <= (1 - theta2)^{-d/2} I[1] is free of J (C-PROP, C-RANK); L2 is 1, t, t^2 times untilted integrals: nonincreasing in J
REASON_FAR = C-FAR (p/J < c(a), c(aZ) for J >= 300), so J^p e^{-c J} decreases in J
REASON_PR = PR = pref_arb(N), a ratio of reduced Laplacian determinants of fixed strip graphs, does not depend on J
REASON_TW = every TW error sits inside the certified J = 300 enclosures; each reason compares exact J-bounds with the exact J = 300 bound, which the enclosure upper end majorizes
REASON_Z4 = each J-bound is twrig4's at its own Omega(J) and tilt T(1/J) before the comparison, so the comparison is between valid bounds, pointwise in J
CONSTANT_PER_N = a constant per N is right for TRB (the review ec33e7dd l.110): every piece's J-bound is nonincreasing in J for J >= 300 by its REASON line
END = S4_TRB_CERTIFIED_v1
