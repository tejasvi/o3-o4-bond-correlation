# S4_RTR_CERTIFIED_v1: the single record of S4's certified Rtr, M2's bound for sup over J >= 300 of tr_H(T)/mu-hat(t), one constant
# per N, for pk02's M2(b) (P2's vac_float uses it only through s = eps/(2 - Rtr - eps)) and the paper.
# Format S4U_KV_v1: one "KEY = value" per line; lines starting with # are comments; blank lines carry nothing.
# Numbers are decimal upper ends as printed by the producing asm output (one-sided, W1; *_HEADROOM, *_DMIN and *_MHAT_LOW are lower
# ends), the exact binary64 literals of the vacres JSON (*_MHAT_M1..M3), or exact bc results from printed values (keys *_REL). File
# tokens are path:sha8, with paths relative to /mnt/g2/release/root/code/; several tokens are separated by " ; ". Every
# sha8 below was computed by sha256sum when this file was assembled; every REASON_* value is copied from the asm outputs' REASON lines
# (identical at both N) when this file was assembled.
FORMAT = S4U_KV_v1
RECORD = S4_RTR_CERTIFIED_v1
AUTHOR = pk08
WRITTEN_UTC = 2026-11-07T13:26:23Z
CLAIM = for N in {3, 4} and every t in (0, 1/300] (J = 1/t >= 300): tr_H(T)/mu-hat(t) <= N*_RTR, one constant per N; T is the plain one-column transfer that twrig3 traces (no insertion), mu-hat(t) = lambda_h mhat(t), mhat(t) = 1 + m1 t + m2 t^2 + m3 t^3 with (m1, m2, m3) = N*_MHAT_M1..M3, lambda_h as in S4_TRB_CERTIFIED_v1
DOMAIN = J >= 300 (t -> 0 included), N in {3, 4}; a = aZ = 1/4, eps = 9/20, lam = 17/40, 17/40, 119/200 (theta 17/20); TW at sigma 0.5 with M = 64
J_MIN = 300
CHAIN = RTR = main(1/300)/mhat(1/300) + R3 + R_cub + tail + far, all at t = 1/300 (S4_RTR_DESIGN_v1_1 items 2-3, the joint form); main = I[1] + t I[H1] + t^2 I[P2]; no R_F (tr(T) has no insertion)
MAPPING = one to one with pk10/scripts/twrig3.py:5124f785: main = its second-order value, R3 = R3 signed-part, R_cub = R3 tilted cubic, tail = tail, far = far
MHAT_SOURCE_N4 = pk11/out/vacres_K3_N4_sym_v1.json:b40859de
MHAT_SOURCE_N3 = pk11/out/vacres_K3_N3_sym_v1.json:e5a9b49f
N4_MHAT_M1 = 0.4110342096146122
N4_MHAT_M2 = 0.21439445218778858
N4_MHAT_M3 = 0.13250737666638984
N3_MHAT_M1 = 0.3639110188717423
N3_MHAT_M2 = 0.19020873542681713
N3_MHAT_M3 = 0.1312176314326442
MHAT_RULE = N*_MHAT_M1..M3 are the binary64 values of the keys "m1", "m2", "m3" in MHAT_SOURCE_N*, written as the JSON literals (shortest round-trip decimals; the asm C-MHAT lines print the same strings); the code parses them with json from bytes whose sha256 it checks and uses them exactly (arb of a binary64); M2 must use the same m's from the same file
TARGET_FLOAT = N4 1.332042 ; N3 1.331271
TARGET_FLOAT_SOURCE = pk10/scratch/vacgap_N4.txt:2a98ef95 ; pk10/scratch/vacgap_N3.txt:2f157dc9 ; pk10/scripts/vacgap.py:09746c72 l.49-54 (pk02: any certified Rtr at or below these is safe for the x1.186 gate on s)
CODE = pk08/px08_rtrcert_v1.py:80726a83
CODE_MANIFEST = pk08/MANIFEST_px08_rtrcert_v1.sha256:013ff51c
CODE_DIFF = pk08/diff_px08_trbcert_v1_1_px08_rtrcert_v1.txt:a077a8c4 ; pk08/px08_trbcert_v1_1.py:6baa4535
COPIED_BLOCKS = pk08/COPIED_BLOCKS_px08_rtrcert_v1.txt:17e40035 ; pk08/px08_m2bc4.py:5b72a593
REVIEW = rv01/REVIEW_PX08_RTRCERT_V1_rv01.md:7ab2f551 ; rv01/MANIFEST_REVIEW_PX08_RTRCERT_V1_rv01.sha256:13656e2b
DESIGN = pk08/S4_RTR_DESIGN_v1_1.md:1f5c37a5 ; pk08/MANIFEST_S4_RTR_DESIGN_v1_1.sha256:01ea7909 (v1_1 rewords only C-MONO in item 3 of v1)
BASE_RECORD = pk08/S4_TRB_CERTIFIED_v1.md:91109301 (the reused machinery and its REASON lines for R3, R_cub, tail and far)
CORE_H = 0.0459

# ---- N = 4 ----
N4_RTR = 1.33103977243e+0
N4_RTR_RATIO = 1.33089436283e+0
N4_RTR_MAIN = 1.33272101681e+0
N4_RTR_MHAT_LOW = 1.00137250110e+0
N4_RTR_R3 = 1.72747253403e-5
N4_RTR_RCUB = 1.28124051573e-4
N4_RTR_TAIL = 1.08158508603e-8
N4_RTR_FAR = 3.87334475082e-12
N4_PR = 4.44264196945e+1
N4_TV = 4.20642701144e+1
N4_S1 = [0.56962905 +/- 1.62e-9]
N4_S2 = [0.42528820 +/- 6.44e-9]
N4_DMIN = 2.10593450135e-1
N4_TARGET_FLOAT = 1.332042
N4_GATE_RESULT = PASS
N4_HEADROOM = 1.00222757367e-3
N4_HEADROOM_REL = 7.523e-4
N4_SIGMA = 0.5
N4_M = 64
N4_G_BOXES = 32
N4_TARGET_MISSES = none
N4_C_SCAN_WORST_EXCESS = 0.000e+00
N4_C_SCAN_LEAD_REL = 2.938e-11
N4_VERDICT = VALID
N4_ASM_OUTPUT = pk08/out/px08_rtrcert_v1_n4_asm.out:6e43ca81
N4_ASM_MANIFEST = pk08/MANIFEST_px08_rtrcert_v1_n4_asm_out.sha256:e702289d
N4_PARTS = pk08/MANIFEST_parts_n4_rtrcert_v1.sha256:574e2679 ; pk08/MANIFEST_nodes_n4_rtrcert_v1.sha256:062bcb5d
N4_COV_OUTPUT = pk08/out/px08_rtrcert_v1_n4_cov.out:b2bbfda8

# ---- N = 3 ----
N3_RTR = 1.33071322604e+0
N3_RTR_RATIO = 1.33067291709e+0
N3_RTR_MAIN = 1.33228989096e+0
N3_RTR_MHAT_LOW = 1.00121515501e+0
N3_RTR_R3 = 7.44693043185e-6
N3_RTR_RCUB = 3.28577900854e-5
N3_RTR_TAIL = 4.23174132349e-9
N3_RTR_FAR = 7.91355623696e-14
N3_PR = 1.25437544346e+1
N3_TV = 1.33018901674e+1
N3_S1 = [0.47268301 +/- 3.97e-9]
N3_S2 = [0.33931784 +/- 6.26e-9]
N3_DMIN = 1.44380919830e-1
N3_TARGET_FLOAT = 1.331271
N3_GATE_RESULT = PASS
N3_HEADROOM = 5.57773963701e-4
N3_HEADROOM_REL = 4.189e-4
N3_SIGMA = 0.5
N3_M = 64
N3_G_BOXES = 32
N3_TARGET_MISSES = none
N3_C_SCAN_WORST_EXCESS = 0.000e+00
N3_C_SCAN_LEAD_REL = 2.938e-11
N3_VERDICT = VALID
N3_ASM_OUTPUT = pk08/out/px08_rtrcert_v1_n3_asm.out:c9379724
N3_ASM_MANIFEST = pk08/MANIFEST_px08_rtrcert_v1_n3_asm_out.sha256:2247fc81
N3_PARTS = pk08/MANIFEST_parts_n3_rtrcert_v1.sha256:123597d5 ; pk08/MANIFEST_nodes_n3_rtrcert_v1.sha256:db7bf79f
N3_COV_OUTPUT = pk08/out/px08_rtrcert_v1_n3_cov.out:f58e869e

# ---- rules and reasons ----
RTR_RULE = N*_RTR is the asm READING's upper end of main(1/300)/mhat(1/300) + R3 + R_cub + tail + far (each piece an upper end, PR included; mhat(1/300) enters as a ball); N*_RTR_RATIO is the upper end of main/mhat at t = 1/300, N*_RTR_MAIN the upper end of main(1/300), N*_RTR_MHAT_LOW the lower end of mhat(1/300)
MONO_RULE = C-MONO evaluates D(t) = main'(t) mhat(t) - main(t) mhat'(t) in ball arithmetic on 8 t-balls covering [0, 1/300] (ball j is the arb union of the end balls of [j/2400, (j+1)/2400]; the coefficients are the certified balls of I[1], I[H1], I[P2]), not on a grid; N*_DMIN is the smallest lower end, and PASS needs every lower end > 0
GATE_RULE = C-GATE PASS means N*_RTR <= the lower end of the exact decimal N*_TARGET_FLOAT; N*_HEADROOM is the printed lower end of target - RTR; the code's stop (VERDICT INVALID above the target) was armed in both runs
HEADROOM_REL_RULE = N*_HEADROOM_REL = N*_HEADROOM / N*_TARGET_FLOAT (bc), rounded down at 4 digits
USE = P2's vac_float (pk07 kt_s67_cert_v2_1 l.627-654) uses N*_RTR only through s = eps/(2 - Rtr - eps) at J >= 300 (pk02); M2(b) pins this record by path:sha8 and reads N*_RTR
REASON_MHAT = C-MHAT gives m1, m2, m3 > 0, so mhat(t) >= 1 on (0, 1/300] and B(t)/mhat(t) <= main(t)/mhat(t) + Rb(t) with Rb = R3 + R_cub + tail + far >= 0
REASON_MAIN = C-MONO gives D > 0 on [0, 1/300], so main(t)/mhat(t) is nondecreasing; its t = 1/300 value bounds every t in (0, 1/300]
REASON_R3 = t^3 and t^4 times untilted integrals of fixed polynomials (twlib hbar(j, a, aZ) has no t): nondecreasing in t
REASON_RCUB = Q_t(t') >= Q_t(1/300) in the Loewner order for t' <= 1/300 (the t-part t cfun(a_v) of the tilt is PSD), the integrands 1, H1^4, hhat^4 are >= 0, hhat(t') <= hhat(1/300) monomialwise, and t^3 grows: nondecreasing in t
REASON_TAIL = e^{-lam_v J a_v} decreases in J; T_v <= (1 - theta2)^{-d/2} I[1] is free of J (C-PROP, C-RANK); L2 is t, t^2 times untilted integrals: nonincreasing in J
REASON_FAR = v1_1's PR 2J (2 far_one(a) + far_one(aZ)) majorizes the plain trace's PR (2 far_one(a) + far_one(aZ)), as 2J >= 1; C-FAR (p/J < c(a), c(aZ) for J >= 300), so J^p e^{-c J} decreases in J
REASON_PR = PR = pref_arb(N), a ratio of reduced Laplacian determinants of fixed strip graphs, does not depend on J
REASON_TW = every TW error sits inside the certified J = 300 enclosures; each reason compares exact J-bounds with the exact J = 300 bound, which the enclosure upper end majorizes
REASON_Z4 = each J-bound is twrig3's chain at its own Omega(J) and tilt T(1/J) before the comparison, so the comparison is between valid bounds, pointwise in J
CONSTANT_PER_N = a constant per N is right for Rtr: main/mhat is nondecreasing on (0, 1/300] (C-MONO), mhat >= 1 (C-MHAT), and every remainder bound is nondecreasing in t, i.e. nonincreasing in J, by its REASON line
END = S4_RTR_CERTIFIED_v1
