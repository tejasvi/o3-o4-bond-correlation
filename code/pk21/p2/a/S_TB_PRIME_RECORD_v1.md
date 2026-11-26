# S_TB_PRIME_RECORD_v1: the S_TB' record (plan row P2-16): W2's bulk steps for top- and bottom-row pairs, N = 3 and 4, J >= 300

pk21, component A of step 1. Review:
SOUND, with fixes F1 and F2, applied here, and notes N-a to N-d,
folded in. Status: a record of certified per-piece checks. Before anything is reported as proved, the review checks the final claim texts
and this record against the outputs (the rule). Nothing here goes into v4_39 or another folder. Paths are relative to
/mnt/g2/release/root/code/. Numbers are copied from the outputs named with them; lower ends come from outward interval
arithmetic (mpmath iv, 256 bits, every decimal read as the tightest interval that contains it).

## 0. The claim S_TB'

For N in {3, 4} and every J >= 300, on every piece of the common grid (904 pieces per N; the last piece runs to J = infinity, t = 0):
- **S4(c), crude half:** ||QSQ|| <= tau with tau = S6's rho, and tau < s_x - c-bar (R4's C-GAP). The tight half is piece S
  (pk21/p2/s4c/S4C_TIGHT_RECORD_v1.md, 3b7334fa).
- **S9(b):** for t, a and b, the residuals, the coupling and ||Qv|| have certified bounds, and Lemma A gives the x amplitudes' errors
  (R4's t export: At_lo, Aa_lo, dtx_hi, Qvt_hi).
- **S9(j):** X_lo = t~_x a~_x - R_c^{ta} > 0 (Xta_lo > 0 on every piece; X_tb = X_ta by the flip).
- **S9(g):** ||v_t^+||^2 >= A_t^2 >= 1.05 O_t >= 1.05 ||v_t^-||^2, and rho <= s_x,lo.
- **S9(d'):** X_lo > ||P_perp v_e^+|| ||P_perp v_f^+|| for a top- or bottom-row edge e and a vertical edge f. With the even-complement
  rate below s_x (r2_hi < 1), the flip-even part is positive at every k >= 0.
- **S9(e):** for every k >= 1, |<v_e^-, S^k v_f^->| is smaller than the flip-even lower bound at the same k. The check is made at k = 1.
  It covers every k >= 1 because r2_hi < 1 and ro_hi < 1: in units of s_x^k the subtracted terms do not increase in k (N-c).
- **S9(f):** in the bulk, D3, D4 and D4M have Cov > 0 (Cov_inf_lo > 0). So does a top- or bottom-row edge with a vertical edge at
  k = 0 (D5, D6).
- **S9(h):** every pair of P_3 x P_n, n >= 6, outside S0, with a top- or bottom-row edge and no middle-row horizontal edge, has Cov > 0
  when both its end exponents are at least its kind's threshold. The overlapping pairs D3, D4 and D4M are covered by the joint kind.

## 1. Inputs, pinned

- **R4**, pk15's certified run: pk15/out/out_kt_p2_assembly_v1_37_1_cert.out (f5410931), code pk15/kt_p2_assembly_v1_37_1.py
  (f40a0d1e). Its exports, pinned (N1, sect. 4):
  - pk15/out/export_p2_t_cert_kt_p2_assembly_v1_37_1.kv (b05b09ad);
  - pk15/out/export_p2_14_joint_cert_kt_p2_assembly_v1_37_1.kv (5586a81d);
  - pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37_1.kv (1120b129).
- **S_V**, pk07's vsweep: pk07/out/export_kt_s9h_v1_2_vsweep.kv (761084be; CODE pk07/kt_s9h_v1_2.py 848d7376, RUN vsweep,
  RUN_VERDICT VALID, EXPORT_STATUS CERTIFIED). Its run output pk07/out/out_kt_s9h_v1_2_vsweep.out (f18072f4) names the export with
  its full sha256 on the EXPORT line (l.146) and ends VERDICT VALID (l.149).
- **R5**, pk07's C2-a sweep: pk07/out/export_c2a_kt_s9h_v1_3_2_sweep.kv (65b4fba3), code pk07/kt_s9h_v1_3_2.py (23a06d7d).
  Its eight input tags are all certified.
- **This record's checks:**
  - pk21/p2/a/a3_bulk_checks_v1.py (bce02e7c), output pk21/p2/a/out/a3_bulk_checks_v1.out (27e25648), rows
    pk21/p2/a/out/a3_rows_N4_v1.tsv (32623d2d) and a3_rows_N3_v1.tsv (31ea1900);
  - the N1 comparison pk21/p2/a/out/n1_export_pair_compare_v1.txt (79139ff6) with its six row files (.rows_*);
  - the units cross-check pk21/p2/a/a4_units_crosscheck_v1_1.py (aeff7f11), output pk21/p2/a/out/a4_units_crosscheck_v1_1.out
    (d3802c02). Its v1 (224dc730, output 9ab623f3) stopped on the N<N>_PIECES header line and is kept, unused.
- The reviewed note pk21/p2/a/A_W2_LAST_MILE_v1.md (2d4f2dc1), kept as reviewed.

## 2. Uniformity in J (F2)

- The t and joint exports state it on their J_UNIFORMITY lines (t export l.13, joint export l.17): "UNIFORM-J PER-PIECE (M4): every row
  holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf (t = 0)".
- The S_V export has no J_UNIFORMITY line. Its per-piece fields used here (rho_hi, vp2_hi, vm2_hi, r2_hi, ro_hi) hold on the whole
  piece by the sweep's own per-piece forms:
  - an interval evaluation over the piece's t-interval and the bar box (the naive form);
  - for the smooth forms, a centred mean-value form over the piece.
  C-MV checks the centred forms on every piece (vsweep output l.93 and l.115: 904 pieces x 4 smooth forms x 9 points, failures on
  0 pieces, at each N). C-PIECE, C-UNIF and C-MV-B check the binding pieces (l.124-129). The engine states this design in its docstring
  (kt_s9h_v1_2.py l.226-231), and the piece S review (5fbe1230) sect. 2 reads it.
- Correction to the reviewed files. The note's l.65 and the a3 script's docstring l.4 say that every row holds by "the exports'
  J_UNIFORMITY". For the S_V fields the basis is the one above. The files stay as reviewed (frozen, sect. 13); this record carries
  the correction.
- R5's export states its own uniformity rule (DMIN_RULE): every piece's threshold is at most the header threshold, uniformly in J.

## 3. The reuse check (MUST M3)

None of three later rules reaches R4's exports or R5's sweep; the review confirmed this (review sect. 1).
- K3 (RULING_K3 965f72f0) concerns S9(i)'s engine (pk12's kt_p212_cert v1_3) and pk08's operator-bound draft.
  R4's and R5's code name pk12 on no line and have no interior-bond or rest factor.
- Q-1 (RULING_Q1 a21b717c) concerns a FLOAT base in S9(i)'s d_L <= 0 rows. R4 runs with FLOAT_IN none (C-FLOATIN gates pass),
  and R5's tags are all certified.
- The E_main base (ERRATUM 4f34050b) concerns centring at bulk centres near the ends. R5's fourth kind subtracts the
  means product, the review found no gap, and R4's joint export is a bulk quantity over the centre ball, which
  contains the bulk means.

## 4. The pinned export pair (N1)

| export | v1_37 (read by R5) | v1_37_1 (pinned here) | lines compared | rows identical |
|---|---|---|---|---|
| t | 90568696 | b05b09ad | 1810 | yes |
| joint | 0b841e06 | 5586a81d | 5430 | yes |
| means | db731c93 | 1120b129 | 5430 | yes |

- The counts include the PIECES lines (N-a): 1810 is 1808 piece rows plus 2 PIECES lines, and 5430 is 5424 piece rows plus 6.
- The headers differ only in the comment, CODE and TAG lines. This record pins v1_37_1, the outputs of R4's certified run. R5 read
  v1_37, whose data rows are byte for byte the same.

## 5. S4(c), crude half (plan row P2-9)

- R4 reads S6's rho_hi as Lemma A's tau (C-TAU-READ PASS, R4 l.105). Its C-GAP gate passes Lemma A's hypotheses, Davis-Kahan gaps
  included, on 904 of 904 pieces at each N (l.120).
- The smallest s_x,low - tau_up is 6.1450707616678445e-02 (N = 4) and 6.1714795365126737e-02 (N = 3) (a3 output, the CR KT-MARGINS
  lines, reading R4's l.121-122).

## 6. S9(b)

R4's t export holds, per piece: At_lo = |t~_x| - dt_x, Aa_lo = |a~_x| - da_x, dtx_hi, Qvt_hi and tz_hi. They are built on the Ritz
records pk03 c14756e9 (N = 4) and 4f05913c (N = 3), per piece over the t-ball (RITZ_SOURCE), with C-GAP as in sect. 5.

## 7. S9(j), S9(g), S9(d'), S9(e): the per-piece checks

Smallest lower ends over the 904 pieces (a3 output, 27e25648; all at the first piece [300, 300.75]):

| step | quantity (must be > 0, or > 1 for the ratio) | N = 4 | N = 3 |
|---|---|---|---|
| S9(j) | Xta_lo (and Xtb_lo, the flip) | 4.1135050910e-03 | 2.7712523531e-03 |
| S9(g) | At_lo^2 / (1.05 Ot_hi) | 3.0130144045 | 3.1553481029 |
| S9(g) | At_lo^2 - Ot_hi | 1.0601616371e-03 | 7.3470536213e-04 |
| S9(d') | Xta_lo - Pt_hi pi_a | 3.5441013886e-03 | 2.4254153310e-03 |
| S9(e), k = 1 | Xta_lo - Pt_hi pi_a r2_hi - Ot_hi^(1/2) vm2_hi^(1/2) ro_hi | 2.2161103501e-03 | 1.5384159017e-03 |
| decay rates | 1 - r2_hi; 1 - ro_hi | 6.4630579440e-01; 4.2151501568e-01 | 6.4903151210e-01; 4.2317306339e-01 |

- Definitions: pi_a = (vp2_hi - Aa_lo^2)^(1/2) >= ||P_perp v_a^+||; Pt_hi >= ||P_perp v_t^+|| (R4's joint Gram form, PT_FORM);
  Ot_hi >= ||v_t^-||^2 and vm2_hi >= ||v_a^-||^2 (S_V export); r2_hi and ro_hi are the decay ratios against s_x,lo (C2-a note v1
  l.129).
- The bulk covariance at k steps is exactly the x channel plus the flip-even complement plus the odd part: S commutes with the flip,
  so there are no cross terms. The x channel is bounded below by Xta_lo; the other two are bounded by
  Cauchy-Schwarz with the export norms.
- S9(e)'s reduction (N-c): the check at k = 1 covers every k >= 1, since r2_hi < 1 and ro_hi < 1 make the subtracted terms nonincreasing
  in units of s_x^k.

## 8. S9(f): D3, D4, D4M, D5 and D6

- D3, D4 and D4M (R4's joint export, Cov_inf_lo, nonpositive on 0 of 904 pieces per class and N; minima at piece 116):

| class | N = 4 | N = 3 |
|---|---|---|
| D3 | 4.4382159204841565e-03 | 3.6290409889135444e-03 |
| D4, D4M | 3.1109269630542669e-03 | 2.4832709501796070e-03 |

- D5 and D6 (MUST M2). They are the bulk pairs of a top- or bottom-row edge with a vertical edge at k = 0. There,
  J^2 Cov = t_x f_x + <P_perp v_t^+, P_perp v_f^+> + <v_t^-, v_f^->, so
  J^2 Cov >= Xta_lo - Pt_hi pi_a - Ot_hi^(1/2) vm2_hi^(1/2): smallest lower end 6.1230540998e-04 (N = 4) and 4.9856607312e-04 (N = 3),
  positive on every piece. The flip images follow by the flip. No new export rows are needed (plan row P2-8's entries are not used).
- The same inequality with At_lo Aa_lo in place of Xta_lo is R5's mixed kind at e = 0 (R5's correction term vanishes at e = 0; C2-a note
  v1 l.105, l.131): smallest lower end 6.1270923465e-04 (N = 4) and 4.9861100974e-04 (N = 3) (f0R).
- **Units cross-check (N-b).** R5's certified mixed-kind slack at its threshold (d = 3 at N = 4, d = 2 at N = 3) lies between 0.7756 and
  0.8346 of f0R at N = 4 and between 0.1602 and 0.2485 at N = 3, on all 904 + 904 pieces, and never above it (a4_units_crosscheck_v1_1
  output, VERDICT VALID; the review sect. 2 gives 0.776-0.835 and 0.160-0.248). This fits the slack's monotonicity in e and the
  same units in both forms.

## 9. S9(h)

R5 (65b4fba3; EXPORT_STATUS CERTIFIED, RUN_VERDICT VALID; all eight tags certified):
- thresholds DH_N<N>_<K> on both end exponents: N = 4 flip 2, same 1, mixed 3, D3 3, D4 3, D4M 3; N = 3 flip 2, same 1, mixed 2,
  D3 3, D4 3, D4M 3;
- every kind is one inequality checked at k = 0, whose subtracted terms do not increase in k (CLAIM_RULE; C2-a note v1 l.7);
- the slack does not increase in e = R_w rho1^d, so a threshold covers every larger end exponent (checked to DH_MAX = 6);
- the review checked the code and the run, and R5 is certified.

## 10. Coverage

| pairs | step |
|---|---|
| bulk pairs of a top- or bottom-row edge without a middle-row horizontal edge, columns not overlapping, k >= 1 for a vertical partner (same-type pairs exact) | S9(b), S9(d'), S9(e), S9(g), S9(j) |
| bulk pairs with a vertical partner at k = 0 or in overlapping columns | S9(f) |
| finite strips n >= 6 above the thresholds, separated and overlapping | S9(h) |
| near-end rows below the thresholds, except O5 | S9(i) (certified, Proposition B.1) |
| still open for W2: separated t/bb pairs near the ends | B |
| still open for W2: O5 (N = 4) | C |
| still open: n = 5 | W1 (D0, D1) |

The list follows the supplement's list, with the
certified steps.

## 11. What the review should check

1. The claim texts of sect. 0 against the outputs named in sect. 5-9.
2. The uniformity basis of sect. 2, including the correction.
3. The N1 pin and its counts (sect. 4), and the units cross-check (sect. 8).

## 12. Cost

Component A: 0.74 h from 07:41Z to the note at 08:25:44Z for all of step 1, and this record's fixes and cross-check
after the review. Compute: jobs 27, 28, 51 and 52 used 0.000 core-h (guard logs).

## 13. Files and freeze (F1)

Frozen (mode a-w) and listed with their sha256 in pk21/p2/a/MANIFEST_S_TB_PRIME_RECORD_v1.sha256: this record; the reviewed note;
the a3 script, output and row TSVs; the N1 comparison and its six row files; the a4 scripts and outputs; the job scripts 27, 28, 51
and 52; their guard logs.
