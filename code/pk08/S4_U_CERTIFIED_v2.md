# S4_U_CERTIFIED_v2: S4's certified U (two-column twisted trace, O(3) and O(4)) in two forms, for S6/S7 (C-FMT) and the paper.
# It keeps every key of S4_U_CERTIFIED_v1 (the J = 300 constant N*_U, still true; v1 stays as it is) and adds the F2 form of the P2
# review (FIX F2): U(t) <= U3(t) + N*_R_CERT for every t = 1/J in (0, 1/300], with U3(t) = lead (1 + c1 t + c2 t^2 + c3 t^3) from the
# certified enclosures N*_LEAD, N*_C1, N*_C2, N*_C3, and R_CERT the sum of the remainder pieces' certified J = 300 upper ends, each piece
# nonincreasing in J for J >= 300 by its REASON key.
# Format S4U_KV_v1: one "KEY = value" per line; lines starting with # are comments; blank lines carry nothing.
# Numbers are decimal upper ends as printed by the producing output (one-sided, W1), or exact bc sums of them (keys *_EXACT, *_MINUS_*,
# *_R_CERT); enclosure keys give the printed ball and its exact ends *_LO = midpoint - radius, *_HI = midpoint + radius.
# File tokens are path:sha8, with paths relative to /mnt/g2/release/root/code/; several tokens are separated by " ; ".
# Every sha8 below was computed by sha256sum when this file was assembled.
FORMAT = S4U_KV_v1
RECORD = S4_U_CERTIFIED_v2
EXTENDS = pk08/S4_U_CERTIFIED_v1.md:dae3d6d4
AUTHOR = pk08
WRITTEN_UTC = 2026-11-07T10:30:32Z
CLAIM = for N in {3, 4} and every J >= 300 (t = 1/J <= 1/300): tr_H(T^2)/lambda_h^2 <= U_N, with U_N = U3 + PREF2_RE + PREF2_RHO4 + M3_SUM
CLAIM_F2 = for N in {3, 4} and every t = 1/J in (0, 1/300]: tr_H(T^2)/lambda_h^2 <= N*_LEAD_HI (1 + N*_C1_HI t + N*_C2_HI t^2 + N*_C3_HI t^3) + N*_R_CERT
J_MIN = 300
DESIGN = pk05/S4_M2_DESIGN_v3.md:caa32045 ; rv01/CHECK_S4_M2_DESIGN_v3_rv01.md:7625f367 ; pk08/S4_M2C_DESIGN_v1.md:57f33661 ; rv01/CHECK_S4_M2C_DESIGN_v1_rv01.md:895792aa ; pk08/S4_M3_DESIGN_v1.md:f368c2c6 ; rv01/CHECK_S4_M3_DESIGN_v1_rv01.md:f38d2b57
TARGET_U_MINUS_FLOAT = 7.8e-4
TARGET_U_MINUS_FLOAT_SOURCE = T2 of pk11 joint P0 v1_2 bdbe992f (rem(170) included), held on the fine grid (pk11 out e3bb3dc6); both sha8s
TARGET_QUAD = 3.9e-4
TARGET_QUAD_SOURCE = KR3
F2_SOURCE = the review REVIEW_KT_S67_CERT_V1_1 ec33e7dd FIX F2

# ---- N = 4 ----
N4_U3 = 1.03315206077942
N4_U3_PRINTED = [1.03315206077941 +/- 3.34e-15]
N4_U3_OUTPUT = pk05/out/s4c_m2ba_n4.out:553395a3
N4_U3_MANIFEST = pk05/MANIFEST_s4c_m2ba_out.sha256:c972c30c
N4_U3_CODE = pk05/s4c_m2ba.py:e86784a3
N4_U3_REVIEW = rv01/REVIEW_S4_M2BA_rv01.md:6801391d ; rv01/REVIEW_S4_M2BA_rv01_ADD1.md:bd1cbcc7
N4_LEAD = [1.03023930410320 +/- 1.16e-15]
N4_LEAD_LO = 1.03023930410319884
N4_LEAD_HI = 1.03023930410320116
N4_C1 = [0.846041371764 +/- 4.42e-13]
N4_C1_LO = 0.846041371763558
N4_C1_HI = 0.846041371764442
N4_C2 = [0.639526360689 +/- 2.99e-13]
N4_C2_LO = 0.639526360688701
N4_C2_HI = 0.639526360689299
N4_C3 = [0.498944147013 +/- 7.69e-13]
N4_C3_LO = 0.498944147012231
N4_C3_HI = 0.498944147013769
N4_COEF_OUTPUT = pk05/out/s4c_m2ba_n4.out:553395a3
N4_COEF_LINES = C-NORM N=4 (lead = pref^2 J0) and C-C123 N=4 (c_i = J_i / J0), with C-POS N=4 (c1, c2, c3 > 0) and C-TW3 N=4
N4_PREF2_RE = 1.31803364014e-5
N4_PREF2_RE_OUTPUT = pk08/out/px08_m2bb4_n4_asm.out:a563d888
N4_PREF2_RE_MANIFEST = pk08/MANIFEST_px08_m2bb4_n4_asm_out.sha256:7c2e58bf
N4_PREF2_RE_PARTS = pk08/MANIFEST_parts_n4_m2bb4.sha256:a618af8a
N4_PREF2_RE_CODE = pk08/px08_m2bb4.py:e6a974a7 ; pk08/px08_m2bb2.py:911fbd96 ; pk05/s4c_m2bb.py:d5e1aeea
N4_PREF2_RE_REVIEW = rv01/REVIEW_PX08_M2BB2_rv01.md:7d3c8209 ; rv01/REVIEW_PX08_M2BB2_rv01_ADD1.md:9a329b0a ; rv01/DELTA_PX08_M2BB4_M2BC3_rv01.md:20e27fdb
N4_PREF2_RHO4 = 3.50513088259e-5
N4_PREF2_RHO4_OUTPUT = pk08/out/px08_m2bc3_n4_asm.out:f181a623
N4_PREF2_RHO4_MANIFEST = pk08/MANIFEST_px08_m2bc3_n4_asm_out.sha256:1fec9ff0
N4_PREF2_RHO4_PARTS = pk08/MANIFEST_parts_n4_m2bc3.sha256:767fb58f
N4_PREF2_RHO4_CODE = pk08/px08_m2bc3.py:0e8f2c20
N4_PREF2_RHO4_REVIEW = rv01/DELTA_PX08_M2BB4_M2BC3_rv01.md:20e27fdb
N4_M3_TAIL = 3.82173457095e-7
N4_M3_ANNULUS = 9.84391049981e-9
N4_M3_FAR = 1.05308028035e-14
N4_M3_EQUATOR = 1.33166701908e-24
N4_M3_SUM = 3.92017378126e-7
N4_M3_OUTPUT = pk08/out/px08_px03_v4_n4_asm.out:f55df592
N4_M3_MANIFEST = pk08/MANIFEST_px08_px03_v4_n4_asm_out.sha256:f7fb32a3
N4_M3_PARTS = pk08/MANIFEST_parts_n4_px03_v4.sha256:ee7ba7fa
N4_M3_CODE = pk08/px08_px03_v4.py:824a3ca2 ; pk08/px08_px03_v3.py:068e308d
N4_M3_REVIEW = rv01/REVIEW_PX08_PX03_V2_rv01.md:de0cdbcc ; rv01/DELTA_PX08_PX03_V3_rv01.md:2fe50a0b ; rv01/DELTA_PX08_PX03_V4_rv01.md:d1db3d42
N4_VERDICTS = s4c_m2ba VALID ; px08_m2bb4 asm VALID ; px08_m2bc3 asm VALID ; px08_px03_v4 asm VALID
N4_R_CERT = 4.8623662605426e-5
N4_U_EXACT = 1.033200684442025426
N4_U = 1.033200684443
N4_U_FLOAT = 1.0331806
N4_U_FLOAT_SOURCE = pk05/out/sp0_twrig6z_N4_J300.txt:81c761e1 ; pk05/MANIFEST_sp0_out.sha256:db9b200c
N4_U_MINUS_FLOAT = 2.0084443e-5
N4_U_MINUS_FLOAT_WITHIN_TARGET = yes
N4_QUAD_TW_PART_EXACT = 3.8164741892643e-6
N4_QUAD_TW_PART = 3.82e-6
N4_QUAD_WITHIN_TARGET = yes

# ---- N = 3 ----
N3_U3 = 1.03279527894289
N3_U3_PRINTED = [1.03279527894288 +/- 4.90e-15]
N3_U3_OUTPUT = pk05/out/s4c_m2ba_n3.out:32ade026
N3_U3_MANIFEST = pk05/MANIFEST_s4c_m2ba_out.sha256:c972c30c
N3_U3_CODE = pk05/s4c_m2ba.py:e86784a3
N3_U3_REVIEW = rv01/REVIEW_S4_M2BA_rv01.md:6801391d ; rv01/REVIEW_S4_M2BA_rv01_ADD1.md:bd1cbcc7
N3_LEAD = [1.03023930410320 +/- 1.16e-15]
N3_LEAD_LO = 1.03023930410319884
N3_LEAD_HI = 1.03023930410320116
N3_C1 = [0.742487735443 +/- 4.07e-13]
N3_C1_LO = 0.742487735442593
N3_C1_HI = 0.742487735443407
N3_C2 = [0.537949701615 +/- 4.15e-13]
N3_C2_LO = 0.537949701614585
N3_C2_HI = 0.537949701615415
N3_C3 = [0.438039172601 +/- 3.70e-13]
N3_C3_LO = 0.438039172600630
N3_C3_HI = 0.438039172601370
N3_COEF_OUTPUT = pk05/out/s4c_m2ba_n3.out:32ade026
N3_COEF_LINES = C-NORM N=3 (lead = pref^2 J0) and C-C123 N=3 (c_i = J_i / J0), with C-POS N=3 (c1, c2, c3 > 0) and C-TW3 N=3
N3_PREF2_RE = 5.19975087371e-6
N3_PREF2_RE_OUTPUT = pk08/out/px08_m2bb4_n3_asm.out:29773c44
N3_PREF2_RE_MANIFEST = pk08/MANIFEST_px08_m2bb4_n3_asm_out.sha256:abaa6e8a
N3_PREF2_RE_PARTS = pk08/MANIFEST_parts_n3_m2bb4.sha256:22a1620f
N3_PREF2_RE_CODE = pk08/px08_m2bb4.py:e6a974a7 ; pk08/px08_m2bb2.py:911fbd96
N3_PREF2_RE_REVIEW = rv01/REVIEW_PX08_M2BB2_rv01.md:7d3c8209 ; rv01/REVIEW_PX08_M2BB2_rv01_ADD1.md:9a329b0a ; rv01/DELTA_PX08_M2BB4_M2BC3_rv01.md:20e27fdb
N3_PREF2_RHO4 = 8.46373172498e-6
N3_PREF2_RHO4_OUTPUT = pk08/out/px08_m2bc4_n3_asm.out:fc41f247
N3_PREF2_RHO4_MANIFEST = pk08/MANIFEST_px08_m2bc4_n3_asm_out.sha256:a541196f
N3_PREF2_RHO4_PARTS = pk08/MANIFEST_parts_n3_m2bc4.sha256:6fb20587
N3_PREF2_RHO4_CODE = pk08/px08_m2bc4.py:6527d21b ; pk08/px08_m2bc3.py:0e8f2c20
N3_PREF2_RHO4_REVIEW = rv01/DELTA_PX08_M2BB4_M2BC3_rv01.md:20e27fdb ; rv01/DELTA_PX08_M2BC4_rv01.md:7223a2fc
N3_M3_TAIL = 1.98068592778e-7
N3_M3_ANNULUS = 3.38475118044e-9
N3_M3_FAR = 1.22059226169e-15
N3_M3_EQUATOR = 1.06161757712e-25
N3_M3_SUM = 2.01453345179e-7
N3_M3_OUTPUT = pk08/out/px08_px03_v4_n3_asm.out:b5c8bb3f
N3_M3_MANIFEST = pk08/MANIFEST_px08_px03_v4_n3_asm_out.sha256:b82bede6
N3_M3_PARTS = pk08/MANIFEST_parts_n3_px03_v4.sha256:eb6586bc
N3_M3_CODE = pk08/px08_px03_v4.py:824a3ca2
N3_M3_REVIEW = rv01/REVIEW_PX08_PX03_V2_rv01.md:de0cdbcc ; rv01/DELTA_PX08_PX03_V3_rv01.md:2fe50a0b ; rv01/DELTA_PX08_PX03_V4_rv01.md:d1db3d42
N3_VERDICTS = s4c_m2ba VALID ; px08_m2bb4 asm VALID ; px08_m2bc4 asm VALID ; px08_px03_v4 asm VALID
N3_R_CERT = 1.3864935943869e-5
N3_U_EXACT = 1.032809143878833869
N3_U = 1.032809143879
N3_U_FLOAT = 1.0328035
N3_U_FLOAT_SOURCE = pk05/out/sp0_twrig6z_N3_J300.txt:2056f9fb ; pk05/MANIFEST_sp0_out.sha256:db9b200c
N3_U_MINUS_FLOAT = 5.643879e-6
N3_U_MINUS_FLOAT_WITHIN_TARGET = yes
N3_QUAD_TW_PART_EXACT = 1.17157060968599e-6
N3_QUAD_TW_PART = 1.18e-6
N3_QUAD_WITHIN_TARGET = yes

# ---- how the numbers combine ----
U_RULE = N*_U_EXACT = N*_U3 + N*_PREF2_RE + N*_PREF2_RHO4 + N*_M3_SUM (bc); N*_U = N*_U_EXACT rounded up at the 12th decimal; N*_U_MINUS_FLOAT = N*_U - N*_U_FLOAT (bc)
U3_RULE = N*_U3 is the upper end of N*_U3_PRINTED (midpoint + radius), rounded up at the 14th decimal
M3_RULE = N*_M3_SUM is the asm READING (an upper end of the exact sum); the four printed pieces are each rounded up, so their own sum may exceed it in the last digit
R_CERT_RULE = N*_R_CERT = N*_PREF2_RE + N*_PREF2_RHO4 + N*_M3_SUM (bc): the certified J = 300 upper ends of the pieces R_E, rho4 and the m3 tail, annulus, far and equator (M3_SUM is the certified upper end of the four m3 pieces together); it is not computed as N*_U - U3(300)
U_T_RULE = for every t = 1/J in (0, 1/300]: U(t) <= U3(t) + N*_R_CERT <= N*_LEAD_HI (1 + N*_C1_HI t + N*_C2_HI t^2 + N*_C3_HI t^3) + N*_R_CERT
U_T_RULE_WHY = at every t in (0, 1/300] the S4 chain gives U(t) <= U3(t) + pref^2 R_E(t) + pref^2 rho4(t) + m3(t), each bound valid at its own J (M2C check Z4); each remainder piece's J-bound is nonincreasing in J for J >= 300 by its REASON key, so it is at most its J = 300 value, which the certified upper end majorizes (TW error included); and U3(t) <= the upper-end polynomial because lead > 0, c1, c2, c3 > 0 (C-POS) and t > 0
U_T_RULE_AT_300 = at t = 1/300 the upper-end polynomial plus N*_R_CERT is <= N*_U_EXACT (bc, rounded up at the 16th decimal: N4 1.0332006844420188 <= 1.033200684442025426; N3 1.0328091438788190 <= 1.032809143878833869)
U_T_RULE_AT_0 = as t -> 0 the F2 bound tends to N*_LEAD_HI + N*_R_CERT (bc: N4 1.030287927765806586; N3 1.030253169039145029)
REASON_PREF2 = pref^2 does not depend on J (ratio of Laplacian determinants of fixed graphs), so each piece's monotonicity is that of its pref^2-free part
REASON_PREF2_RE = nonincreasing in J for J >= 300: R_E <= (t^4/24) I[hbar4] + (t^4/2) I[H2^2] + (t^6/72) I[hbar3^2] + ... + (t^6/48) N4^3 I[1]^{1/4} is a sum of explicit powers t^4..t^6 times untilted integrals; hbar_j(a, t) majorizes for every t' <= t, so the J = 300 majorants serve every J >= 300; reviewed: rv01/CHECK_S4_M2_DESIGN_v3_rv01.md:7625f367 l.38
REASON_PREF2_RHO4 = nonincreasing in J for J >= 300: in rho4(J) <= (1/24) (t I_t[H1^4]^{1/4} + (t^2/2) N4_t)^4 every ingredient is nondecreasing in t (t, t^2; each I_t, since Q_t = Q - 2 T_eps - 2 t D decreases in t in the Loewner order with D > 0 and the integrands are >= 0; h_lo free of t; the h_hi coefficients carry t, t^2), so the t = 1/300 value bounds every J >= 300; reviewed: rv01/CHECK_S4_M2C_DESIGN_v1_rv01.md:895792aa l.13-25
REASON_M3_TAIL = nonincreasing in J for J >= 300: pref^2 L2 (sum_v e^{-lam_v J a_v} T_v)^{1/2} with e^{-lam_v J a_v} decreasing in J, T_v = int dmu w det(Q - 2 lam_v B_v)^{-1/2} free of J, and L2 increasing in t; reviewed: rv01/CHECK_S4_M3_DESIGN_v1_rv01.md:f38d2b57 l.26
REASON_M3_ANNULUS = nonincreasing in J for J >= 300: pref^2 sum_s sum_v e^{-lam_sv J prev_s} A_sv, where M(t) = Q - 2 T_eps,sh - 2 lam B_v - 2 t D_sh decreases in the Loewner order as t grows (D_sh > 0), so det M(t)^{-1/2} and A_sv increase in t and A_sv(1/300) bounds every t <= 1/300 (C-PROP at t = 1/300), and e^{-lam J prev} decreases in J; reviewed: rv01/CHECK_S4_M3_DESIGN_v1_rv01.md:f38d2b57 l.16 and l.37-42
REASON_M3_FAR = nonincreasing in J for J >= 300: pref^2 64 sum_v e^{-lam' J avp_v} det(Qf - 2 lam' B_v)^{-1/2} with Qf = Qnt - 2 cfun(0.96) t I decreasing in t, so the t = 1/300 determinants bound t <= 1/300, and e^{-lam' J avp_v} decreases in J; reviewed: rv01/CHECK_S4_M3_DESIGN_v1_rv01.md:f38d2b57 l.30-33
REASON_M3_EQUATOR = nonincreasing in J for J >= 300: pref^2 12 (2J/pi)^{1/2} e^{-J (1 - cos 0.685)} decreases for J > 1/(2 (1 - cos 0.685)) = 2.22; reviewed: rv01/CHECK_S4_M3_DESIGN_v1_rv01.md:f38d2b57 l.17-18
REASON_TW_PART = no separate J-dependence: the TW errors sit inside the certified enclosures of the J = 300 integrals; each REASON compares exact J-bounds with the exact J = 300 bound, which the enclosure's upper end majorizes
NOT_MONOTONE = none; no fallback at extra t points is needed
QUAD_ARGUMENT = every trapezoidal (TW) error is inside the certified enclosures (each integral = TW sum +/- (TW error + ball radius)), so U_N needs no extra quadrature term
QUAD_TW_PART_RULE = N*_QUAD_TW_PART_EXACT = 0.071 x (N*_PREF2_RE + N*_PREF2_RHO4) + N*_M3_SUM + 1e-11 (bc); N*_QUAD_TW_PART rounded up at 3 digits
QUAD_TW_PART_WHY = the R_E and rho4 readings are increasing and homogeneous of degree 1 in the integrals, and every family entering them has TW error <= 0.071 |T_M| (largest I_c[h_lo^4]: 6.71e-2 at N = 4, 7.05e-2 at N = 3; group (b) families <= 5.18e-2), so their TW part is <= 0.071 x (PREF2_RE + PREF2_RHO4); the whole M3_SUM is counted (its only TARGET miss is the tail-only (E H2^2)^2); U3's TW errors are <= 6.0e-16 absolute on integrals >= 2.6e-4 (relative <= 2.3e-12), counted as 1e-11
QUAD_NOTE = N3_QUAD_TW_PART = 1.18e-6 replaces the 1.17e-6 in pk08's earlier message, which was rounded down from 1.1716e-6

# ---- reuse across code versions (N1) ----
REUSE_GROUP_B = N = 4 uses pk05 s4c_m2bb nodes0/nodes1 and px08_m2bb2 G items g0-g3; N = 3 uses px08_m2bb2 nodes0/nodes1 and G items g0-g3; both N use px08_m2bb4 refine items r0-r7 (all in the PARTS manifests). Pinned by C-CORE (node code byte-identical to s4c_m2bb.py l.84-636 and l.638-836, block lines [553, 199]) and C-GBLOCK (G-item code of px08_m2bb2 = px08_m2bb4, block lines [7, 135]), both PASS with plants fired in the asm outputs, together with the reviewed diffs pk08/diff_s4c_m2bb1_px08_m2bb2.txt:a963e8ce ; pk08/diff_px08_m2bb2_px08_m2bb3.txt:f2154287 ; pk08/diff_px08_m2bb3_px08_m2bb4.txt:1907a4d1
REUSE_GROUP_C = N = 3 (px08_m2bc4 asm) reuses the px08_m2bc3 partials cov, nodes0-3, g0, g1 and g3-g7 (g2 was rerun under px08_m2bc4). N1: C-ITEMCODE pins only the evaluation code (937 lines, 1 differing: G_MAXEV_C); the reuse rests on C-ITEMCODE together with the reviewed diff pk08/diff_px08_m2bc3_px08_m2bc4.txt:df0978cd (DELTA_PX08_M2BC4). N = 4 is px08_m2bc3 throughout.
REUSE_M3 = N = 4 (px08_px03_v4 asm) reuses the px08_px03_v3 outputs pk08/out/px08_px03_v3_n4_tail.out:22436518 ; pk08/out/px08_px03_v3_n4_sh1.out:5503ca6e. N1: C-ITEMCODE-M3 pins only the evaluation code (regions of 783 and 377 lines byte-identical); the reuse rests on it together with the reviewed diff pk08/diff_px08_px03_v3_v4.txt:bb962211 (DELTA_PX08_PX03_V4). N = 3 uses v4 outputs only.
END = S4_U_CERTIFIED_v2
