# P4_LEMMA_NOTE_v1_1: route (B) for MR_INSERT v5's last h row (Way A): the windowed x amplitude as entry terms plus O(t) remainders

Written 2026-11-21T16:50:22Z by pk25/jobs/job161_p4_lemma_note_v1_1.sh (numbers and hashes read by tools there), for the review, main and pk24.
Authority: the rows 4636, 4640 and 4644. Marks: [D] from the files named, [E] estimate, [float] float data.
v1_1 = v1 (pk25/P4_LEMMA_NOTE_v1.md (d45df794)) with one change: the NIH
entry next to psi-hat carries one S, so h~ = <u~_x, S M_h psi-hat_n> and R_1 = <u~_x, S M_h (u - psi-hat_n)>, and the proof splits S M_h u
directly. The bound, the exact t^0 zero and the numbers are unchanged. P4's tool states this one-S form in its docstring.

## 0. Why a new route on the last piece
- MR_INSERT's h-row x amplitude is S9(c)-h's budget (pk25/asm/src/kt_s9h_ins_v2_4.py.in (c5066002), s9c_htx). Its bad-part constants are
  J-uniform by S9C_BADPART_LEMMA_v1 sect. 2, because the Lam split sits in rescaled units. So on the last piece (t -> 0) it keeps a floor.
- v4b's Way B rows [D, pk25/mr/v4b/MR_INSERT.kv (54691bc1)]: N4 xc [1.8232352899268831e-01, 2.8575335392144141e-01], xf 1.3524173932003794e-11, vx [-1.3524704817050890e-11, 2.8325750237466216e-07], C_hi 4.4301516759807038e+00; N3 xc [9.3073129023039977e-02, 1.4098492387923067e-01], xf 8.4537635035507779e-12, vx [-8.4540710855081688e-12, 1.3975530249701541e-07], C_hi 2.1162612995807457e+00.
- The certified run's lines [D, pk25/asm/out/out_kt_s9h_ins_v2_4_cert_c2.out (1166488c)]: N4 xc = [1.8232352914894101e-01, 2.8575335376518873e-01], xf = 1.3524173932003794e-11 (F0 1.3495598593456141e-11, 171 sub-pieces, ratio 11/10); the sign holds for J < 1.3481306145988560e+10; N3 xc = [9.3073129076734540e-02, 1.4098492382553610e-01], xf = 8.4537635035507779e-12 (F0 8.4396650096036502e-12, 171 sub-pieces, ratio 11/10); the sign holds for J < 1.1009667947020479e+10.

## 1. The lemma (one N, the last piece t in [0, t_1], t_1 = 1/J_lo)
Notation as G6 v1_6_7 sect. 1: S = T/lambda_0 with top unit vector u (S u = u, |S| = 1), M_c = M_h - c_h with c_h = <u, M_h u>, B^w = S M_c S.
MR_INSERT's h vector is v = M_c u (unwindowed: v_y(0) = h_y0, C13), and the windowed vector is S v = S M_c u = B^w u. Ritz data on
W = span{psi-hat, psi_1, psi_3}: u~_k = sum_b c_kb psi_b with c^T G c = 1, oriented as MR_LEMMAP (u~_x along sign(S[3][1]) psi_1);
psi-hat_n = psi-hat/|psi-hat|. Then
  s_x v_x = <u_x, S v> = <u_x, B^w u> = h~ + R_1 - c_h R_2 + E_A,
with
- h~ = <u~_x, S M_h psi-hat_n> = F sum_b c_xb Ih_b, with ONE S: the NIH entries Ih_b = [cp b 0] [xh M 1 8] [cp 0 2] are
  three-column entries with the insertion on the bond next to psi-hat (pk25/m3/out/m3_s9h_NIH_N4_J300_v1.json (343f7abe) and its N3 twin,
  laws in m3_lawcert_s9h_v1_1). In the records' frame the entry is <psi_b, V^1/2 K V (K o xi) V^1/2 psi_0> = lambda_0^2 <phi_b, S M_h phi_0>,
  with phi = K^1/2 V^1/2 psi / lambda_0^1/2 and K o xi = K^1/2 M_h K^1/2. F = mhat/(G_00^1/2 lambda_0^2) is the records' conversion of R4's
  amplitude (ritz_piece's amp, p = 2), a positive O(1) factor with a certified ball on the piece; its lambda_0^2 shows the two bonds;
- R_1 = <u~_x, S M_h (u - psi-hat_n)>, |R_1| <= |S M_h| |u - psi-hat_n| <= (C + |c_h|) |u - psi-hat_n|, since |S M_h| <= |S M_c| + |c_h| |S|
  <= C + |c_h| (C = MR_INSERT's C_hi >= |M_c S| = |S M_c|, the N-1 constant, for the uncentred M_h);
- R_2 = <u~_x, u> = <u~_x, u - u~_0> (u~_x and u~_0 are orthonormal), |R_2| <= delta_0 = |u - u~_0|;
- E_A: Lemma A at level x for w = B^w u (C6a's form), |<u_x, w> - <u~_x, w>| <= dh_x = q_x Q + eps_0x |<u~_0, w>| + eps_yx |<u~_y, w>|
  + (q_x^2 + eps_0x^2 + eps_yx^2) |<u~_x, w>|, with Q >= |Q_W w|.
Proof. s_x v_x = <u_x, S v> by the symmetry of S, and S v = S M_c S u = S M_c u = S M_h u - c_h u (S u = u). So
<u~_x, B^w u> = <u~_x, S M_h u> - c_h <u~_x, u>, and writing u = psi-hat_n + (u - psi-hat_n) in S M_h u directly splits it as
h~ + R_1 - c_h R_2. Lemma A turns <u~_x, w> into <u_x, w> with the error dh_x. QED
- |u - psi-hat_n| <= delta_0 + |uhat_00 - 1| + |uhat_01| + |uhat_03| (u~_0 = sum_b uhat_0b psi_b/|psi_b|, triangle inequality), and
  delta_0 <= (2 (q_0^2 + eps_x0^2 + eps_y0^2))^1/2 (G6 sect. 1, Ritz data).

## 2. Every term is t times an enclosed coefficient (so xf = 0)
- h~: at t^0 the combination is exact zero. With C10's exact order-0 Ritz data (u~_x(0) = u_x0, psi-hat(0) = u0) the t^0 value of
  sum_b c_xb Ih_b is proportional to <u_x0, S M_h u0> = s_x0 <u_x0, M_h u0> = s_x0 (<u_x0, M_c u0> + c_h0 <u_x0, u0>) = s_x0 h_y0 <u_x0, u_y0> = 0
  (C13's C-BH0: M_c0 u0 = h_y0 u_y0; the modes orthonormal, P1's C-T0-EXACT and C-HARM). So
    sum_b c_xb Ih_b = t [sum_b dc_b Ih_b(t) + sum_b c_x0,b Ih1_b(t)],
  with dc = (c_x - c_x0)/t from P2's last-piece form and Ih1_b = (Ih_b(t) - Ih_b(0))/t
  from the NIH laws' coefficient balls k >= 1 plus R/t (P2's law form; the true a_0 is not needed, only the exact zero of the combination).
- R_1, R_2: delta_0/t and |uhat_0b - uhat_0b(0)|/t (uhat_0(0) = (1, 0, 0)) from P2's table; C and |c_h| are O(1) balls.
- E_A: q_x/t and eps_kx/t from P2's table; Q and |<u~_k, w>| are O(1) per-piece bounds of v2_4's computation on the last piece (Q = qv4(A_h,
  ...) may carry t-free parts; they multiply q_x = O(t), so dh_x/t stays finite and no bridge is needed here).
- Hence on [0, t_1]:
    xc = v_x/t in ( F [sum_b dc_b Ih_b + sum_b c_x0,b Ih1_b] +- ((C + |c_h|) |u - psi-hat_n|/t + |c_h| delta_0/t + dh_x/t) ) / [s_x,lo, s_x,hi],
  finite at t = 0, with xf_hi = 0, and vx refreshed to [min(0, t_1 xc_lo), max(0, t_1 xc_hi)] (pk24's check_m2_cols_v2).
- The orientation enters once, through the oriented c_x (P1, P2); v2_4's sigma_x flip of the unoriented R4 amplitude is not applied again.

## 3. Sizes on the last piece [E, P2's dry table pk25/p2/dry_d2/MR_LEMMAP_V3F.kv (4a464522); C from v4b; c_h0 from C13 (7542c2da)]
- N4 (C 4.4301516759807038e+00, c_h0 3/2 - sqrt(21)/7 = 0.845346): delta_0/t <= 3.013e-07, |u~_0 - psi-hat_n|/t <= 7.741e-06, R1/t <= 4.243e-05, |c_h| R2/t <= 2.547e-07; q_x/t 1.1852535924610159e+00, eps_yx/t 7.7654827334888873e-07.
- N3 (C 2.1162612995807457e+00, c_h0 1 - 2*sqrt(21)/21 = 0.563564): delta_0/t <= 1.146e-07, |u~_0 - psi-hat_n|/t <= 4.541e-06, R1/t <= 1.248e-05, |c_h| R2/t <= 6.457e-08; q_x/t 6.9604128349712968e-01, eps_yx/t 2.8793151888918979e-07.
- So the remainders are of order 1e-5 to 1e-4 against a windowed amplitude s_x v_x/t near 0.0338 at N4 (s_x0 times the neighbour piece
  N4_P0902_h xc midpoint in v4b): xc keeps its sign with a narrow enclosure, and the floor is gone.

## 4. P4's tool
- kt_s9h_ins_v2_5 = v2_4 with this block on the last h row only: every other row and field byte-identical to v4b (job153-style compare), the
  last h row's xc_lo, xc_hi from section 2, xf_hi = 0, vx_lo, vx_hi refreshed; FIELDS, X_POWER, X_DEFINITION unchanged. Its docstring
  states the one-S form h~ = <u~_x, S M_h psi-hat_n>.
- Gates and plants: C-WAYA-T0 (the t^0 balls of sum_b c_x0,b Ih_b contain 0, a control of the exact zero), C-WAYA (xc certainly signed on the
  last piece), C-FACTX (t xc inside vx at both ends), PLANT-WAYA-ZERO (a nonzero t^0 combination must be refused as not O(t)), PLANT-ORIENT.
- Inputs: P2's certified table (q/t, eps/t, u0 /t), C10 (c_x0), the NIH laws, v2_4's last-piece quantities. P4's cert follows P2's.
