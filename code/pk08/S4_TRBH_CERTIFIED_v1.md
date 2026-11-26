# S4_TRBH_CERTIFIED_v1: the single record of S4's certified TRB_H(r) = tr_H P_L/lambda_h^2 (SH4 of HZ_PLAN_v1_1) for the rows
# r in {T, M}, in the F2 form TRB_H(r, t) <= U3_p(r)(t) + R_cert(r), for SH4's consumer and the paper.
# Format S4U_KV_v1: one "KEY = value" per line; lines starting with # are comments; blank lines carry nothing.
# Numbers are decimal upper ends as printed by the producing asm output (one-sided, W1; *_TOL is a lower end). Enclosure keys give the
# printed ball and its exact ends *_LO = midpoint - radius and *_HI = midpoint + radius (bc). File tokens are path:sha8, with paths
# relative to /mnt/g2/release/root/code/; several tokens are separated by " ; ". Every sha8 below was computed by
# sha256sum when this file was assembled (gen_s4_trbh_record_v1.sh); every REASON_* value is copied from the asm outputs' REASON lines,
# which are identical at both N.
FORMAT = S4U_KV_v1
RECORD = S4_TRBH_CERTIFIED_v1
AUTHOR = pk08
WRITTEN_UTC = 2026-11-07T19:41:29Z
CLAIM = for N in {3, 4}, r in {T, M} and every t = 1/J in (0, 1/300]: TRB_H(r, t) = tr_H P_L(r)/lambda_h^2 <= U3_p(r)(t) + N*_<r>_R_CERT, where U3_p(r)(t) = d_0 + d_1 t + d_2 t^2 + d_3 t^3 with d_k in the certified balls N*_<r>_D<k> (at t >= 0, sum_k t^k N*_<r>_D<k>_HI is an upper end), and P_L(r) is U's two-column twisted trace T^2 with p_L(xi_e) = (N-1) x/2 - J (1 - x^2)/2 on one horizontal bond e of row r between the two columns: x = t c + s1 s3 with c = phi1.phi3 (row T), x = s4 (row M)
DOMAIN = J >= 300 (t -> 0 included), N in {3, 4}, r in {T, M}; option (i): delta = 0.12 for both groups, eps = 0.65; TW on Im al = 0.5 with M_TW = 128 (v2)
J_MIN = 300
CHAIN = R_cert(r) = R_main + R_cross + R_ins + tail + off-Omega, all at t = 1/300 (S4_TRBH_DESIGN_v1_1 sect. 3, option (i)); R_main = ((N-1)/2) (U's PREF2_RE + PREF2_RHO4) + alpha1 (R_E^(delta) + rho4^(delta)), alpha1 = 1/(e delta) for row T and 1/(2 e delta) for row M; tail = PR L2^(p) Chern^(1/2); off-Omega = ((N-1)/2 + J/2) (U's M3_ANNULUS + M3_FAR + M3_EQUATOR)
OPTION = (i): the dry run's VERDICT line names (iii) — the script's frozen rule; option (i) is chosen under the rule from 14:12Z, set before the result: (iii) needs 1.2 x remainder <= 0.8 TOL, and N4 row T sits at 96.1%.
TOL_RULE = TOL(r) = (1/4) (U3_p(r)(1/300) - h_r), h_r from HZ_PLAN_v1_1 l.143; it rests on HZ_PLAN_v1_1's l.461 kill rule (beta_H <= 1.5 x float) in the binding u-perp case. C-TOL requires R_cert(r) <= TOL(r) at both rows. The 0.8 TOL rule chose the option; the certificate's test is C-TOL
TRIAL_PINS = none. The certified bound reads no trial or vacres file: its inputs are U's record (S4_U_CERTIFIED_v2, which pins none), U's m3 outputs (Chernoff sum, lam lines) and exact model constants; lambda_h enters only through PR = pref_arb(N), an exact ratio of reduced Laplacian determinants of fixed strip graphs. It bounds the true tr_H P_L/lambda_h^2 and stands alone next to z9sym-based records. h_r (HZ_PLAN_v1_1) enters only the consumer tolerance TOL, and the dry-run references only the float control C-PL0
CODE = pk08/px08_trbhcert_v2.py:10662078
CODE_MANIFEST = pk08/MANIFEST_px08_trbhcert_v2.sha256:55b70ddd
CODE_DIFF = pk08/diff_px08_trbhcert_v1_2_v2.txt:1e33eb98 ; pk08/diff_px08_trbhcert_v1_1_v1_2.txt:5c111aca ; pk08/diff_px08_trbhcert_v1_v1_1.txt:b1c0c4db
PRODUCERS = pk08/px08_trbhcert_v1.py:f69581ad (cov, nodes0..nodes8, n4 gP0) ; pk08/px08_trbhcert_v1_1.py:2937ba65 (n4 gP1..gP7, n3 gP0..gP7) ; pk08/px08_trbhcert_v1_2.py:990b46d0 (gD0..gD7, gT0..gT7 at both N, LIM 350 under the exception) ; pk08/px08_trbhcert_v2.py:10662078 (odd0..odd7 at both N, the asm); C-ITEMCODE in v2's asm shows each earlier producer byte-identical to v2 from GPARTS to the asm part except the lines it names
PRODUCER_MANIFESTS = pk08/MANIFEST_px08_trbhcert_v1.sha256:4c13637d ; pk08/MANIFEST_px08_trbhcert_v1_1.sha256:f70c7d99 ; pk08/MANIFEST_px08_trbhcert_v1_2.sha256:24464676
COPIED_BLOCKS = pk08/COPIED_BLOCKS_px08_trbhcert_v2.txt:8a8b9166 ; pk08/px08_m2bc4.py:6527d21b ; pk08/px08_trbcert_v1_1.py:6a851374
REVIEW = rv01/REVIEW_PX08_TRBHCERT_V1_rv01.md:40f0dea8 ; rv01/MANIFEST_REVIEW_PX08_TRBHCERT_V1_rv01.sha256:7637ce72 ; rv01/DELTA_PX08_TRBHCERT_V1_1_rv01.md:cf677708 ; rv01/MANIFEST_DELTA_PX08_TRBHCERT_V1_1_rv01.sha256:b36078bc ; rv01/DELTA_PX08_TRBHCERT_V1_2_rv01.md:daaad5f7 ; rv01/MANIFEST_DELTA_PX08_TRBHCERT_V1_2_rv01.sha256:d4cd411e ; rv01/DELTA_PX08_TRBHCERT_V2_rv01.md:b527345e ; rv01/MANIFEST_DELTA_PX08_TRBHCERT_V2_rv01.sha256:a258f360
DESIGN = pk08/S4_TRBH_DESIGN_v1_1.md:70962463 ; pk08/MANIFEST_S4_TRBH_DESIGN_v1_1.sha256:a2f54507 ; rv01/DELTA_S4_TRBH_DESIGN_v1_1_rv01.md:b62a082d ; pk08/S4_TRBH_DESIGN_v2_DELTA.md:3280de6d (v2: the TW sums at M_TW = 128 on the same line)
DRY_RUN = pk08/px08_trbhscan_v2.py:ac843025 ; pk08/out/px08_trbhscan_v2_n4_i.out:cda6f19d ; pk08/out/px08_trbhscan_v2_n3_i_r2.out:6160ba66
SUPERSEDED = pk08/out/px08_trbhcert_v1_2_n4_asm.out:3c5156a4 (v1_2's asm n4, VERDICT INVALID on C-TOL, R/TOL 1.878 (T) and 1.877 (M) at M = 64: the TW error of (E H1^2)^4, (E H1^2)^2 (E H2^2)^2 and (E H1^2)^6 set the tail through E_3's L4 bound; v2 takes the TW sums at M_TW = 128)
BASE_RECORD = pk08/S4_U_CERTIFIED_v2.md:cd2b32d7 (PREF2_RE, PREF2_RHO4, M3_ANNULUS, M3_FAR, M3_EQUATOR; LEAD and C1..C3 for C-REPRO) ; pk15/HZ_PLAN_v1_1.md:ebee9574 (h_r, l.143) ; pk08/out/px08_px03_v4_n4_asm.out:f55df592 ; pk08/out/px08_px03_v4_n3_asm.out:b5c8bb3f (U's Chernoff sum)
CORE_H = 3.1937 (every px08_trbhcert run, v1 to v2, the stopped and the INVALID ones included)

# ---- N = 4 ----
N4_T_D0 = [0.526805749833724 +/- 1.05e-16]
N4_T_D0_LO = 0.526805749833723895
N4_T_D0_HI = 0.526805749833724105
N4_T_D1 = [-0.263293871181523 +/- 4.22e-16]
N4_T_D1_LO = -0.263293871181523422
N4_T_D1_HI = -0.263293871181522578
N4_T_D2 = [-0.315658828624080 +/- 9.78e-17]
N4_T_D2_LO = -0.3156588286240800978
N4_T_D2_HI = -0.3156588286240799022
N4_T_D3 = [-0.267938955821 +/- 3.83e-13]
N4_T_D3_LO = -0.267938955821383
N4_T_D3_HI = -0.267938955820617
N4_T_U3P_1_300 = [0.525924586352469 +/- 2.84e-16]
N4_T_U3P_1_300_LO = 0.525924586352468716
N4_T_U3P_1_300_HI = 0.525924586352469284
N4_T_R_CERT = 7.56187267355e-4
N4_T_R_MAIN = 5.17556230711e-4
N4_T_R_CROSS = 1.17779721820e-4
N4_T_R_INS = 6.58812858971e-7
N4_T_TAIL = 1.18701147930e-4
N4_T_L2P = 6.93710884411e+0
N4_T_OFF_OMEGA = 1.49135403614e-6
N4_T_TOL = 6.70614658811e-3
N4_T_R_OVER_TOL = [0.1128 +/- 3.97e-5]
N4_T_R_OVER_TOL_LO = 0.1127603
N4_T_R_OVER_TOL_HI = 0.1128397
N4_M_D0 = [0.679035470880718 +/- 4.24e-16]
N4_M_D0_LO = 0.679035470880717576
N4_M_D0_HI = 0.679035470880718424
N4_M_D1 = [-0.218510274647549 +/- 3.41e-16]
N4_M_D1_LO = -0.218510274647549341
N4_M_D1_HI = -0.218510274647548659
N4_M_D2 = [-0.369398687293724 +/- 1.97e-17]
N4_M_D2_LO = -0.3693986872937240197
N4_M_D2_HI = -0.3693986872937239803
N4_M_D3 = [-0.384263600470 +/- 3.91e-13]
N4_M_D3_LO = -0.384263600470391
N4_M_D3_HI = -0.384263600469609
N4_M_U3P_1_300 = [0.678302984636716 +/- 9.40e-17]
N4_M_U3P_1_300_LO = 0.6783029846367159060
N4_M_U3P_1_300_HI = 0.6783029846367160940
N4_M_R_CERT = 5.13068772076e-4
N4_M_R_MAIN = 2.94951849276e-4
N4_M_R_CROSS = 1.09283721436e-4
N4_M_R_INS = 1.65894113861e-8
N4_M_TAIL = 1.07325257917e-4
N4_M_L2P = 6.27228134587e+0
N4_M_OFF_OMEGA = 1.49135403614e-6
N4_M_TOL = 5.90074615917e-3
N4_M_R_OVER_TOL = [0.08695 +/- 1.90e-7]
N4_M_R_OVER_TOL_LO = 0.086949810
N4_M_R_OVER_TOL_HI = 0.086950190
N4_R_E_DELTA = 3.48523616311e-5
N4_N4_D = 5.40686176288e+3
N4_RHO4_DELTA = 1.10371985167e-4
N4_N4_T = 1.41737902691e+4
N4_ALPHA1_T = 3.06566200977e+0
N4_ALPHA1_M = 1.53283100489e+0
N4_PR = 4.44264196945e+1
N4_CHERN = 1.48344070050e-13
N4_G_BOXES = P 72, D 127, T 71
N4_REFLECTION = no
N4_TARGET_MISSES = none
N4_SIGMA = 0.5
N4_M_TW = 128
N4_NODES = 0..64 once each: the even ones from nodes0..nodes8 (M = 64, node k is node 2k), the odd ones from odd0..odd7
N4_TOL_RESULT = C-TOL PASS, R/TOL [0.1128 +/- 3.97e-5] (T), [0.08695 +/- 1.90e-7] (M)
N4_CHECKS = all PASS
N4_PLANTS = 18 of 18 FIRED
N4_VERDICT = VALID
N4_ASM_OUTPUT = pk08/out/px08_trbhcert_v2_n4_asm.out:11019b7c
N4_ASM_MANIFEST = pk08/MANIFEST_asm_n4_trbhcert_v2.sha256:144e2d9b
N4_NODE_MANIFEST = pk08/MANIFEST_nodes_n4_trbhcert_v1.sha256:80abcb81
N4_COV_OUTPUT = pk08/out/px08_trbhcert_v1_n4_cov.out:9b593a14

# ---- N = 3 ----
N3_T_D0 = [0.355417332135483 +/- 6.75e-17]
N3_T_D0_LO = 0.3554173321354829325
N3_T_D0_HI = 0.3554173321354830675
N3_T_D1 = [-0.0236740740091098 +/- 2.63e-17]
N3_T_D1_LO = -0.0236740740091098263
N3_T_D1_HI = -0.0236740740091097737
N3_T_D2 = [-0.0711712670900703 +/- 2.39e-17]
N3_T_D2_LO = -0.0711712670900703239
N3_T_D2_HI = -0.0711712670900702761
N3_T_D3 = [-0.0743963983578 +/- 2.06e-14]
N3_T_D3_LO = -0.0743963983578206
N3_T_D3_HI = -0.0743963983577794
N3_T_U3P_1_300 = [0.355337625008174 +/- 1.52e-16]
N3_T_U3P_1_300_LO = 0.355337625008173848
N3_T_U3P_1_300_HI = 0.355337625008174152
N3_T_R_CERT = 1.70234446690e-4
N3_T_R_MAIN = 1.05033142460e-4
N3_T_R_CROSS = 2.36321430148e-5
N3_T_R_INS = 3.07992490233e-7
N3_T_TAIL = 4.07500711123e-5
N3_T_L2P = 2.73081579684e+0
N3_T_OFF_OMEGA = 5.11097612556e-7
N3_T_TOL = 5.65940625204e-3
N3_T_R_OVER_TOL = [0.03008 +/- 8.74e-8]
N3_T_R_OVER_TOL_LO = 0.0300799126
N3_T_R_OVER_TOL_HI = 0.0300800874
N3_M_D0 = [0.454218823501121 +/- 1.03e-16]
N3_M_D0_LO = 0.454218823501120897
N3_M_D0_HI = 0.454218823501121103
N3_M_D1 = [0.00794755613661297 +/- 1.79e-18]
N3_M_D1_LO = 0.00794755613661296821
N3_M_D1_HI = 0.00794755613661297179
N3_M_D2 = [-0.0686230139834240 +/- 3.13e-17]
N3_M_D2_LO = -0.0686230139834240313
N3_M_D2_HI = -0.0686230139834239687
N3_M_D3 = [-0.0831751210207 +/- 9.89e-15]
N3_M_D3_LO = -0.08317512102070989
N3_M_D3_HI = -0.08317512102069011
N3_M_U3P_1_300 = [0.454244549796416 +/- 4.21e-16]
N3_M_U3P_1_300_LO = 0.454244549796415579
N3_M_U3P_1_300_HI = 0.454244549796416421
N3_M_R_CERT = 1.13601068544e-4
N3_M_R_MAIN = 5.93483125294e-5
N3_M_R_CROSS = 1.71516379128e-5
N3_M_R_INS = 5.26755368096e-9
N3_M_TAIL = 3.65847529350e-5
N3_M_L2P = 2.45168213236e+0
N3_M_OFF_OMEGA = 5.11097612556e-7
N3_M_TOL = 4.46113744910e-3
N3_M_R_OVER_TOL = [0.02546 +/- 4.60e-6]
N3_M_R_OVER_TOL_LO = 0.02545540
N3_M_R_OVER_TOL_HI = 0.02546460
N3_R_E_DELTA = 1.20452421461e-5
N3_N4_D = 3.84416649528e+3
N3_RHO4_DELTA = 1.77589761828e-5
N3_N4_T = 8.43916450660e+3
N3_ALPHA1_T = 3.06566200977e+0
N3_ALPHA1_M = 1.53283100489e+0
N3_PR = 1.25437544346e+1
N3_CHERN = 1.41519681443e-12
N3_G_BOXES = P 76, D 128, T 73
N3_REFLECTION = yes
N3_TARGET_MISSES = none
N3_SIGMA = 0.5
N3_M_TW = 128
N3_NODES = 0..64 once each: the even ones from nodes0..nodes8 (M = 64, node k is node 2k), the odd ones from odd0..odd7; the reflection atom (weight 1/2) from nodes0
N3_TOL_RESULT = C-TOL PASS, R/TOL [0.03008 +/- 8.74e-8] (T), [0.02546 +/- 4.60e-6] (M)
N3_CHECKS = all PASS
N3_PLANTS = 18 of 18 FIRED
N3_VERDICT = VALID
N3_ASM_OUTPUT = pk08/out/px08_trbhcert_v2_n3_asm.out:9663347f
N3_ASM_MANIFEST = pk08/MANIFEST_asm_n3_trbhcert_v2.sha256:20da31a4
N3_NODE_MANIFEST = pk08/MANIFEST_nodes_n3_trbhcert_v1.sha256:6f1613f9
N3_COV_OUTPUT = pk08/out/px08_trbhcert_v1_n3_cov.out:f7c3c231

# ---- rules and reasons ----
U3P_RULE = N*_<r>_D0..D3 are the asm U3_P line's balls d_k = I[f_k], f_k = sum_{i+j=k} p_i E_j (exact Gaussian moments, group P, the 11-form table); N*_<r>_U3P_1_300 is U3_p(r)(1/300), the value C-TOL uses
R_CERT_RULE = N*_<r>_R_CERT is the asm READING's upper end of R_main + R_cross + R_ins + tail + off-Omega at t = 1/300, each piece an upper end with PR included; by the REASON lines it bounds every t in (0, 1/300]
USE = SH4's consumer pins this record by path:sha8 and reads N*_<r>_D0..D3 (balls) and N*_<r>_R_CERT: TRB_H(r, t) <= U3_p(r)(t) + N*_<r>_R_CERT for t = 1/J <= 1/300
REASON_U3P = an exact cubic in t, the (P) form; the consumer evaluates it at its t
REASON_RCROSS_RINS = t^m (m >= 4) times J-free integrals on group D's measure, which majorizes the plain one: nondecreasing in t
REASON_RMAIN = ((N-1)/2) U's R_E + rho4 (nonincreasing in J by U's reasons) plus alpha1 times the U chain on Q - 2 delta B_Y and Q - 2 T(t) - 2 delta B_Y, with hbar_j at t = 1/300 (majorizing every t' <= t) and the matrices Loewner-decreasing in t (the t-part of T is PSD, delta B_Y is J-free): nondecreasing in t
REASON_TAIL = t-powers times J-free norms, times U's Chernoff sum (nonincreasing in J by U's reasons)
REASON_OFF_OMEGA = ((N-1)/2 + J/2) times U's annulus, far and equator J-bounds, nonincreasing for J >= 300 by C-FAR-H
REASON_PR = PR = pref_arb(N), a ratio of reduced Laplacian determinants of fixed strip graphs, does not depend on J
REASON_TW = every TW error sits inside the certified J = 300 enclosures; each reason compares exact J-bounds with the exact J = 300 bound, which the enclosure upper end majorizes
REASON_Z4 = each J-bound is the chain at its own Omega(J) and tilt T(1/J) before the comparison, so the comparison is between valid bounds, pointwise in J
END = S4_TRBH_CERTIFIED_v1
