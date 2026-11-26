# W2's last mile (pk21, step 1, component A): reuse check, export pin, per-piece checks, records and claim texts

Nothing is claimed before the review. Paths are
relative to /mnt/g2/release/root/code/. Numbers are copied from the outputs named with them. A carries the MUST M2
(D5 and D6), MUST M3 (the reuse check) and N1 (one pinned export pair); sections 1, 2 and 5 answer them.

## 0. Answer first

- MUST M3: none of the three later rules (K3; Q-1; the E_main base item) touches R4's t, joint
  or means exports or R5's sweep (section 1).
- N1: the record pins R4's v1_37_1 exports. R5 read the v1_37 exports, whose data rows equal v1_37_1's byte for byte (section 2).
- Per-piece checks on the certified exports, in outward interval arithmetic: every check is positive on all 904 pieces per N for S9(j),
  S9(g), S9(d'), S9(e), and S9(f) for D3, D4, D4M, D5 and D6 (section 3).
- MUST M2: D5 and D6 need no new export rows. In the bulk, the k = 0 inequality X_lo - ||P_perp v_t|| ||P_perp v_a|| - ||v_t^-|| ||v_a^-|| > 0
  follows from the t export and the S_V export and covers them (smallest lower end 6.12e-4 at N = 4, 4.99e-4 at N = 3; section 5).
  This replaces plan row P2-8's new D5/D6 entries.
- Section 6 drafts the claim texts and the coverage table as a module for a later paper version; nothing goes into v4_39.

## 1. MUST M3: the three later rules against R4's exports and R5's sweep

R4 = pk15/out/out_kt_p2_assembly_v1_37_1_cert.out (f5410931) and its exports; R5 = pk07/out/export_c2a_kt_s9h_v1_3_2_sweep.kv (65b4fba3,
code pk07/kt_s9h_v1_3_2.py 23a06d7d).

- K3. It rules on S9(i)'s engine
  (pk12's kt_p212_cert v1_3): its interior-bond factor in a chain, and the rest bounds of W3e, W3f, D4L0 and D4ML0.
  - Neither R4's code (pk15/kt_p2_assembly_v1_37_1.py) nor R5's code has an interior-bond rest factor. In R4, "K3" occurs only in
    the vacres file names and "interior" only in "interior verticals 1" of the graph couplings; R5 has neither.
  - R4's run pins 90 files (C-HASH PASS, l.2). The file paths named in R4's code lie in pk01, pk02, pk15, pk03,
    pk07, pk08 and pk11 (there: the trial sets, the vacres files and two S8 float outputs). None lies in pk12, the
    folder of S9(i)'s engine.
  - R5's eight input tags are pk03 e55c5de1, pk02 13cc0d9a, pk08 e870cbe5, 91109301 and bb53005c, and pk15 90568696 (twice)
    and 0b841e06 (export header l.18-33). None is S9(i)'s.
- Q-1. At S9(i)'s rows with d_L <= 0, the base lo = Cov - R used
  the harmonic t = 0 covariance as a FLOAT stand-in, so it was not a certified lower end.
  - R4 runs with FLOAT_IN none: its C-FLOATIN and C-FLOATIN-EMPTY gates pass, and every export says FLOAT_IN = none.
  - R5 reads only certified tags (all eight lines say certified). Its joint kind's base is R4's Cov_inf_lo, a certified lower end
    (C-COV-POS in R4).
- E_main base (ERRATUM 4f34050b). The issue: E[X_c] with
  X_c = (e - c_e)(f - c_f) at bulk centres is Cov + (E[e] - c_e)(E[f] - c_f), not the truncated covariance, near the ends. Row 2599's
  question (c) asked about the same centring in R5's C2-a.
  - Row 2607 (pk07): R5's fourth kind already subtracts the means product, so it certifies the truncated covariance
    (kt_s9h_v1_3_2.py joint_slack l.4788-4813).
  - Row 2609: "NO GAP in C2a.4 reading ... -> of 6e38bd40 scope only P2-12 needs the fix; nothing open."
  - R4's joint export is a bulk quantity. Its bounds hold over the centre ball, which contains the bulk means, where E[X_c] = Cov
    exactly (the reasoning of the review).
- Finding: none of the three rules reaches the t, joint or means exports or the sweep. The review should confirm this.

## 2. N1: the pinned export pair

pk21/p2/a/out/n1_export_pair_compare_v1.txt (job27):

| export | v1_37 (read by R5) | v1_37_1 (pinned) | data rows | rows equal |
|---|---|---|---|---|
| t | 90568696 | b05b09ad | 1810 | yes |
| joint | 0b841e06 | 5586a81d | 5430 | yes |
| means | db731c93 | 1120b129 | 5430 | yes |

The headers differ only in the comment, CODE and TAG lines (the producer's name and sha8). The record pins v1_37_1, the outputs of
R4's certified run, and states that R5 read v1_37, whose data rows are identical.

## 3. Per-piece checks (pk21/p2/a/a3_bulk_checks_v1.py, bce02e7c; output pk21/p2/a/out/a3_bulk_checks_v1.out)

Inputs, sha256 checked by the script: R4's t export b05b09ad and joint export 5586a81d, the S_V export 761084be, R4's run output
f5410931. Each decimal is read as the tightest interval that contains it, with mpmath iv at 256 bits. Each row holds for every J of
its piece (the exports' J_UNIFORMITY). The t and S_V grids are identical (904 pieces per N, the same jlo and jhi strings). Smallest
lower ends over the pieces (all at the first piece [300, 300.75], the joint ones at piece 116):

| step | quantity (must be > 0) | N = 4 | N = 3 |
|---|---|---|---|
| S9(j) | Xta_lo (and Xtb_lo, the flip) | 4.1135e-3 | 2.7713e-3 |
| S9(g) | At_lo^2 / (1.05 Ot_hi) (must be > 1) | 3.0130 | 3.1553 |
| S9(g) | At_lo^2 - Ot_hi | 1.0602e-3 | 7.3471e-4 |
| S9(g) | s_x,low - tau_up, tau_up = S6's rho (R4's KT-MARGINS line) | 6.1451e-2 | 6.1715e-2 |
| S9(d') | Xta_lo - Pt_hi pi_a | 3.5441e-3 | 2.4254e-3 |
| S9(e) | Xta_lo - Pt_hi pi_a r2_hi - Ot_hi^(1/2) vm2_hi^(1/2) ro_hi (k = 1) | 2.2161e-3 | 1.5384e-3 |
| S9(f), k = 0 | Xta_lo - Pt_hi pi_a - Ot_hi^(1/2) vm2_hi^(1/2) | 6.1231e-4 | 4.9857e-4 |
| cross-check | the same with At_lo Aa_lo in place of Xta_lo (R5's mixed kind at e = 0) | 6.1271e-4 | 4.9861e-4 |
| decay rates | 1 - r2_hi; 1 - ro_hi | 0.6463; 0.4215 | 0.6490; 0.4232 |
| S9(f) | Cov_inf_lo, D3 | 4.4382e-3 | 3.6290e-3 |
| S9(f) | Cov_inf_lo, D4 and D4M | 3.1109e-3 | 2.4833e-3 |

Definitions:
- pi_a = (vp2_hi - Aa_lo^2)^(1/2) >= ||P_perp v_a^+||, since ||P_perp v^+||^2 = ||v^+||^2 - e_x^2 (C5_RESCUE_v1_1 sect. 4);
- Pt_hi >= ||P_perp v_t^+|| (R4's joint Gram form, PT_FORM; NOTE_P2_11_C2A_v1_1 N-1);
- Ot_hi >= ||v_t^-||^2; vm2_hi >= ||v_a^-||^2 (S_V export);
- r2_hi and ro_hi bound the even-complement and odd decay rates relative to s_x (S7's mode inputs). Both are below 1, so in units of
  s_x^k the subtracted terms do not increase in k.

## 4. Records of the steps already certified on disk

- S4(c), crude half (plan row P2-9). R4 reads S6's rho_hi as Lemma A's tau (C-TAU-READ PASS, l.105). Its C-GAP gate passes Lemma A's
  hypotheses, Davis-Kahan gaps included, on 904 of 904 pieces at each N (l.120). The smallest s_x,low - tau_up is 6.145e-2 (N = 4) and
  6.171e-2 (N = 3) (l.121-122). The tight half is piece S (pk21/p2/s4c/S4C_TIGHT_METHOD_v1.md, 57e50736).
- S9(b). R4's t export holds, per piece: At_lo = |t~_x| - dt_x, Aa_lo = |a~_x| - da_x, dtx_hi, Qvt_hi and tz_hi. They are built on the
  Ritz records pk03 c14756e9 (N = 4) and 4f05913c (N = 3), per piece over the t-ball (RITZ_SOURCE), with C-GAP above.
- S9(h), separated and joint kinds (R5, 65b4fba3; EXPORT_STATUS CERTIFIED, RUN_VERDICT VALID; all eight tags certified):
  - thresholds DH_N<N>_<K> on both end exponents: N = 4 flip 2, same 1, mixed 3, D3 3, D4 3, D4M 3; N = 3 flip 2, same 1, mixed 2,
    D3 3, D4 3, D4M 3;
  - every kind is one inequality checked at k = 0; its subtracted terms do not increase in k (CLAIM_RULE; NOTE_P2_11_C2A_v1 l.7);
  - the slack does not increase in e = R_w rho1^d, so a threshold covers every larger end exponent (checked to DH_MAX = 6);
  - the review checked the code and the run, and R5 is certified;
  - pinned pair as in section 2; reuse check as in section 1.

## 5. MUST M2: D5 and D6 without new export rows

- D5 and D6 are the bulk pairs of a top- or bottom-row edge with a vertical edge at k = 0 (no plain step between the two insertions;
  NOTE_P2_11_C2A_v1_1 sect. 0, j = i + 2 and j = i - 1).
- At k = 0, J^2 Cov = <v_t, v_f> = t_x f_x + <P_perp v_t^+, P_perp v_f^+> + <v_t^-, v_f^->. By S9(j) and Cauchy-Schwarz,
  J^2 Cov >= Xta_lo - Pt_hi pi_a - Ot_hi^(1/2) vm2_hi^(1/2), smallest lower end 6.12e-4 (N = 4) and 4.99e-4 (N = 3), positive on every
  piece. The flip images follow by the flip (Xtb_lo = Xta_lo).
- The same inequality, with the decay rates r2_hi, ro_hi < 1, gives J^2 Cov > 0 at every k >= 0 for each bulk mixed pair. It is R5's
  mixed kind at e = 0, which is why the review read R5 as implying these steps above the thresholds (ADD1 sect. 0).
- Plan row P2-8 built D5/D6 from inner products of insertion vectors (new entries). This route needs none. It uses the same certified
  quantities as S9(d') and S9(e).

## 6. Claim texts and coverage (P2-16 draft; a module for a later paper version)

For N in {3, 4} and every J >= 300 (each claim holds per piece of the common grid, uniformly in J):
- S4(c), crude half: ||QSQ|| <= tau with tau = S6's rho, and tau < s_x - c-bar (R4's C-GAP); the tight half is piece S.
- S9(b): for t, a and b, the residuals, the coupling and ||Qv|| have certified bounds, and Lemma A gives the x amplitudes' errors
  (R4's t export: At_lo, Aa_lo, dtx_hi, Qvt_hi).
- S9(j): X_lo = t~_x a~_x - R_c^{ta} > 0 (Xta_lo > 0 on every piece; X_tb = X_ta by the flip).
- S9(g): ||v_t^+||^2 >= A_t^2 >= 1.05 O_t >= 1.05 ||v_t^-||^2, and rho <= s_x,lo (section 3).
- S9(d'): X_lo > ||P_perp v_e^+|| ||P_perp v_f^+|| for a top- or bottom-row edge e and a vertical edge f; with the even-complement
  rate below s_x (r2_hi < 1), the flip-even part is positive at every k >= 0.
- S9(e): for every k >= 1, |<v_e^-, S^k v_f^->| is smaller than the flip-even lower bound at the same k (section 3, k = 1, and the
  decay rates).
- S9(f): in the bulk, D3, D4 and D4M have Cov > 0 (Cov_inf_lo > 0), and so do a top- or bottom-row edge and a vertical edge at k = 0
  (section 5).
- S9(h): every pair of P_3 x P_n, n >= 6, outside S0, with a top- or bottom-row edge and no middle-row horizontal edge, whose two end
  exponents are at least its kind's threshold (section 4), has Cov > 0; the overlapping pairs D3, D4, D4M by the joint kind.

Coverage (supplement v5b l.393-404, with the certified steps): S9(b), (d'), (e), (g), (j) cover the bulk pairs of a top- or
bottom-row edge without a middle-row horizontal edge, columns not overlapping, k >= 1 for a vertical partner (same-type pairs exact);
S9(f) the bulk pairs with a vertical partner at k = 0 or in overlapping columns; S9(h) the finite strips n >= 6 above the thresholds,
separated and overlapping; S9(i) (certified, Proposition B.1) the near-end rows below the thresholds except O5. Still open for W2: the
separated t/bb pairs near the ends (B), O5 (C) and n = 5 (D0).

## 7. What the review should check, and what is left

1. Section 1, the reuse finding for each rule.
2. Section 3: that the five per-piece forms are the plan's statements (P2-4 to P2-8) with these export fields, units included (P2's
   units in both exports; the script reads them as they are).
3. Section 5: the k = 0 decomposition for D5/D6, and that the bulk vectors at k = 0 are the export's (as in R5's mixed kind at k = 0).
4. Whether the claim texts of section 6 are what P2-16 should record.
- Left after the review: the record entries (one file per step or one S_TB' record, as the review prefers) and the module in .tex form.
- Cost so far, all of step 1: 0.74 h from 07:41Z to 08:25:44Z (date -u), and 0.069 core-h, of which A's jobs 27
  and 28 used 0.000.
