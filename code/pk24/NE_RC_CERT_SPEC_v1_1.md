# NE_RC_CERT_SPEC_v1_1: the certified form of NE's RC engine (pk24)

Written by pk24 for pk22, which builds the engine, and for its review. Written 2026-11-18T01:54:29Z (UTC, by the
assembling tool). A specification: it adds no bound and changes none. Paths are relative to /mnt/g2/release/root/code/.
The bar readings in sect. 10 and the checksums in sect. 11 were copied by tools/assemble_spec_v1_1.py in the run that wrote this file.
This revision of pk24/NE_RC_CERT_SPEC_v1.md (7128a21c) answers its review
which found v1 sound with two must-fixes. Changes: the certificate of every piece constant (sect. 2, the new table);
the gate C-DUAL-KEYS with two plants (sects. 5 and 8); C-MHAT's certificate (sect. 4); and the record's new prints
(sect. 9). Everything else is v1's text. Build from this document.

## 0. What to build
- A certified engine for NE's rows, the FLIP/SAME and MIXED classes on the horizontal chain. It reads RC (Lemma RC, reviewed
  as sound) on certified inputs, over every J piece: N = 4 from piece 61 (J >= 349.356, the
  piece that holds 350), N = 3 from piece 0 (J >= 300), both through piece 903, the last piece, which reaches t = 0.
- The base is the float engine rcm6, which the review closed for the float reading:
  pk24/ne/kt_s8hf_rcm4_pk24.py (d3d59ce2), plus rcm5's four filters (n >= 5) and rcm6's control C-REPRO-RC5. Like rcm4, the new
  engine imports pk11's certified S8 engine kt_s8_cert_v1_14_3 for the vertical chain, the records and the pieces.
- The open items, each in its own section: C-1, the mean-value form over each piece (sect. 2); C-2, certified horizontal entries and
  their bar targets (sect. 3); C-3, the eigenvalue ratio in tau' (sect. 4); C-4, the dual run (sect. 5); MUST-FIX N5-1 and the other
  conditions for n = 5 (sect. 6). Then the coverage list (sect. 7), the controls and
  plants (sect. 8), and the record and its verdict (sect. 9).

## 1. Source map
- RC's code, in pk24/ne/src/ (checksums in sect. 11): rc_block_v1.py holds opt_a_chain_mb (the bottom row mirrored, the F-a fix),
  rc_chain, rc_setup, frob_up, sf_pair2_rc, s1_rows_rc, rows_mixed_rc, rows_h_rc (every slot of DN, the F-b fix) and rcsum;
  rc2_block_add_v1.py and rc2_t0_v1.py hold C-HARM-RC, PLANT-RC, RCXW and RCIN. The float engine's code: rcm_block_v1.py holds tau_cert,
  chain_h_fix, rc_chain_m and rc_setup_m, and rcm_scan_v1.py the scan. rcm6's prints are rcm6_fn_v1.py, rcm6_loop_v1.py and
  rcm6_end_v1.py.
- Line numbers below without a file are those of pk24/ne/kt_s8hf_rcm6.py (4d9fda54), which holds all of the above:
  sf_pair2_rc l.1056, rows_mixed_rc l.1151, rows_h_rc l.1192, chain_h_fix l.1388, rc_chain_m l.1442, rc_setup_m l.1491, the scan
  from l.1818.
- The rest is pk22's float engine as rcm4 carries it (setup_h, cov2_2, dk_class2, dk_class_h, far_lo2_h, the harmonic checks),
  with the two side findings fixed: F-a (v2d l.665 against l.294) and F-b (v2d l.1228 and l.1267).

## 2. C-1: the mean-value form over each J piece
- The rule is S8's (SPEC_S8_CERT_v1 sect. 9; pk11/kt_s8_cert_v1_14_3.py docstring, the argument for the allowance vector). Each
  piece gets one entry box: t in T = [1/J_hi, 1/J_lo] as slot 0, and each entry's bar offset in [-err_b, err_b] as one more slot.
  Each chain quantity is computed twice, in duals over the box and at the midpoints (entries at t_m = mid(T), bar offsets 0). The two
  runs are combined leaf by leaf by s8core's _cen (s8core_v1_11 l.967-984). By the mean value theorem in (t, bars), the centered ball
  holds the true value at every point of the box.
- Quantities that need derivative bounds (they enter the duals), with the certified source of each:
  - (a) The ten horizontal entries of sect. 3, from the new certified records (C-2). Their t-gradient is sum_k k a_k t^(k-1) over the
    record's coefficient spans, exactly as s8core's entry_duals forms it (l.1055-1077).
  - (b) S8's vertical entries that the horizontal chain reads directly: g_ab, e_a and Z4 (chain_h_fix l.1398-1399 and l.1426), from
    S8's records, in the same box. rcm4 evaluates them at the point t = 1/J_lo through CM.entry_vals; the certified engine must not.
  - (c) S8's chain quantities that the horizontal chain reads: C, lam0, g00, the plain states l(d) (chV['L']), R (for R^k), and the
    prm fields e, rn1 and cerr. They come from S8's own dual run, the W3 chain that piece_eval_RB returns with its 'dual'
    (chain_dual_t, s8core l.1080-1088). The duals of (a) to (c) must share one box and one key order: either S8's chain is rerun on
    the combined entry box, or its gradients are padded with zeros on the horizontal bar slots, which is exact because the vertical
    chain reads no horizontal entry.
  - (d) Everything the horizontal chain computes from (a) to (c): y(0) and y(1), slot 0's norms (n2y, n21, crs, Ap2y0), RC's centres
    (base and cen_i, rc_chain_m l.1455-1461), the bulk vector pc, and the pair form's Num and Z at the centres (cov2_2), with gL and gR.
- Quantities that need no derivative: t-independent constants of the piece, carried as balls with zero gradient. S8's allowance
  argument requires each of them to be one number per piece and a bound over the whole piece (pk11/kt_s8_cert_v1_14_3.py a6eea55f
  l.240). The table names, for each constant, the certificate that makes it valid on the whole piece, or how the engine
  bounds it. A value certified only at J_lo does not qualify without a monotonicity argument, which the table gives where one is used.

| constant | source | why it holds on the whole piece |
|---|---|---|
| kappa = (N - 1)/2 - c_fix | c_fix, one rational per piece | exact; Lemma RC holds for any fixed c |
| the c box [ce_lo, ce_hi], and w = ce_hi - ce_lo | pk15's certified export EXPORT_P2_T_v1 (pk15/out/export_p2_t_cert_kt_p2_assembly_v1_37_1.kv, b05b09ad), the piece's row | the export's CLAIM and J_UNIFORMITY lines (l.10, l.13): every row holds for every J in [jlo, jhi] of its piece, and the last piece runs to t = 0 |
| Qvt_hi, and pc_H = Qvt_hi + w sp | the same row; sp as below | the same two lines; pc_H increases in Qvt_hi, w and sp, each an upper end |
| rho_1 (rho1_hi) | pk07's certified export EXPORT_KT_S67_v1 (pk07/out/export_kt_s9h_v1_2_vsweep.kv, 761084be), the piece's row | its producer kt_s9h_v1_2 (848d7376) bounds each field over the piece and its box (l.942, l.1548; field list l.2952-2956); S8's own setup reads the same row (s8core l.478-489) |
| R_w, the cap on \|v_i\| (Rw_hi, S8's e[0]) | the same P2 row | as for rho_1 |
| delta, s, sp | S8's vac for the piece, from the M2(b) law at J_lo | S8's argument: one t-independent number per piece, a bound on the whole piece (a6eea55f l.240); the law's eps falls in J while eps_r and s rise with eps (kt_s9h_v1_2 l.3991-3992, C-VACMONO), so the values at J_lo bound J >= J_lo |
| TRB_H | the J-uniform value for row T: 0.527562 at N4, 0.355588 at N3 | J-uniform by construction: D0_HI + sum_{k=1..3} max(Dk_HI, 0) 300^-k + R_CERT bounds TRB_H(T, t) for every t in (0, 1/300] (kt_s9h_v1_2 bh_bound, l.3988-3989; C-BH, l.4106; (b) and B-2) |
| eps_H = c_N / J_lo | c_N, a constant | c_N t increases in t, so its value at t = 1/J_lo bounds the piece |
| alpha_lo, at (ce_hi, t_max = 1/J_lo) | the c box and the piece's J_lo | alpha(c, t) = (N - 1)/2 - c (1 + (N - 1) t / 2) + c^2 t / 2 decreases in t when c < N - 1 (gate J1) and in c when c < 1/t_max + (N - 1)/2 (gate J2), so (ce_hi, t_max) is its minimum over the piece's (c, t) box |
| tau' | the rows for eps_H, rho_1, TRB_H, delta and alpha_lo | tau' increases in eps_H, rho_1, TRB_H and delta and decreases in alpha_lo, each an end over the whole piece |
| pn_SH4 = sqrt(kappa_S tau'), with kappa_S = (N - 1)/2 - ce_lo | the c box and tau' | it increases in both factors, each an upper end over the piece |
| RC's radii rho[i], rho[inf], r_u and alw | the dual run | upper ends over the box (S8's upper-end rule, next item) |

- RC's radii depend on t through the chain: rho[i], rho[inf], r_u and the place-2 allowance alw (rc_chain_m l.1462-1476). Compute
  them once per piece, in the dual run, as upper ends over the whole box, and pass the same constants to the midpoint run. This is S8's
  the upper-end rule for its allowances a1 and a_ (s8core l.104-111, the allow argument). The centered chain then carries each radius as a ball
  with zero t-derivative.
- The pair form gets S8's class-level branch (s8core sf_pair l.683-719). C1 = t1 + ddet + lin and dz are fixed upper ends over the
  box, where lin is RC's linear and bilinear term (sf_pair2_rc l.1069-1075). Then Cov >= (Num_c - C1)/(|Z_c| + dz)^2 when Num_c - C1
  >= 0, and the same with |Z_c| - dz otherwise; Num_c and Z_c are duals over the box from the centres chains of both sides, combined by
  _cen. The larger of this and the plain lower end is kept. Both sides' duals must live on the same box, with one key order (sect. 5).
- Why the full form, and not a naive interval in t: rcm4 takes the horizontal parts at J_lo only (pk24/NE_RC_M1_v1.md l.30). On the
  first piece, the ten entries move by at most 5.3e-6 each at N4 and 4.1e-6 at N3 (spec/out/hent_coef_v1.out), about 5% of the 1e-4
  target. Num = Z F1 - F2 F3 cancels, though, which is why S8 uses the class-level form; Num and Z must not be taken as naive intervals.
- Checks, S8's family on the horizontal chain (gates; sect. 8): C-MV-H, C-MV-BAR-H, C-UNIF-H, C-PIECE-H and C-TARGET-H, with
  PLANT-MV-H, PLANT-UNIF-SLACK-H and PLANT-PIECE-H.

## 3. C-2: certified horizontal entries and the bar targets
- The ten entries per N: fT,a for a = 0..3 (on E3T), hT,a for a = 0..3 (on H4T), and the 4-strip entries S4,x,0,HT and
  S4,xy,0,HT,2,HT (chain_h_fix l.1401-1402 and l.1427). Today they exist only in float, in pk11's s8h_mk tables
  (s8h_float_v1.<N>.small, .h4 and s8h_float_v1_3.<N>.s4h). The bottom-row entries are not separate: the flip classes use the parity
  mirror (F-a, sect. 7).
- Format and producer as S8's H and S4 records (SPEC_S8_CERT_v1 sect. 8-9): pk03 produces them, in M3's format with its sha-pinned
  reader and C-FMT with key-swap plants. Each entry is sum_{k<=3} [LO_k, HI_k] t^k plus one constant bar err_b, valid for every
  J >= 300 including t = 0, with each bar part nonincreasing in J.
- The bar of a reading is the total radius of an entry at a point of the piece: the coefficient spans' part plus err_b. rcm4's barF
  (each fT and hT entry) and barS (each 4-strip entry) stand for it.
- What the readings show (sect. 10; float, certified inputs, 18 pieces per N). From a bar of (1.5e-4, 5e-5) on, the binding row
  at both N is the n = 5 class HV (0, 1, flip, 1), the orbit a3,bb1. Per unit, the 4-strip bar costs about four times the headroom of
  the fT/hT bar: at N4, (1e-4, 1e-4) reads 2.237, the same as (3e-4, 5e-5) at 2.236.
- Targets for headroom >= 2 on every row, n = 5 included (bars written as (fT/hT, S4 HT)):
  - N4: S4 HT <= 5e-5 with fT/hT <= 3e-4 (2.236), or S4 HT <= 1e-4 with fT/hT <= 2e-4 (2.029, no margin). S4 HT = 2e-4 fails even
    with fT/hT at 1e-4 (1.674).
  - N3: fT/hT <= 3e-4 with S4 HT <= 1e-4 (2.265), or S4 HT <= 2e-4 with fT/hT <= 1e-4 (2.148); (5e-4, 1.5e-4) fails (1.699).
  - Without the n = 5 rows, rcm4's reading passes at N4 up to (3e-4, 1e-4) (2.592) and at N3 up to (1e-3, 3e-4) (2.109).
- Recommended build target: fT/hT <= 1e-4 and S4 HT <= 5e-5 at both N, which reads 2.893 at N4 and 3.728 at N3. That is about twice
  the largest per-entry bars of S8's own H and S4 records (5.2e-5 and 2.4e-5 at N4), so records of S8's quality would read above these
  values. The mean-value spread of C-1 takes a little of the margin: on the first piece the entries' own t-width is at most 5.3e-6 per
  entry (sect. 2). At (3e-5, 2e-5), N4's smallest row is 2.956 (a
  class with n >= 6), and the n = 5 rows read 4.24 or more, with a1,bb2 = HV (2, -1, flip, 1) then the thinnest
  (pk24/n5/out/n5map_v1.out).
- The four orbits that only NE covers (G15, G11, G16, G08) stay at 4.0 or more at N4 for every bar up to (3e-4, 5e-5) and up to
  (1e-4, 1e-4); G08 = bb1,t4 is their thinnest (4.018 at (1e-4, 1e-4)).
- The certified run prints the n = 5 rows' headroom at its actual bars.

## 4. C-3: the eigenvalue ratio in tau'
- tau' = eps_H rho_1^2 + TRB_H / (1 - delta)^2 - alpha_lo, with delta = (eps_r / sqrt(1 - s^2)).upper(). delta is S8's own constant
  for place 1 (lambda_0 in m-hat [1 -+ delta], SPEC_S8_CERT_v1 l.320), which S8's vac_from_law returns from the M2(b) law at J_lo
  (kt_s8_cert_v1_14_3's docstring on delta). Read it from S8's vac for the piece rather than recomputing it, so that tau' and the chain
  use the same number.
- The ratio: (lambda_h/lambda_0)^2 <= 1/(m-hat (1 - delta))^2 <= (1 - delta)^-2, by C-MHAT (m-hat >= 1 for every J >= 300; rv01/
  RULING_P3_BETAH_TRBH_rv01.md 19f74c2b l.22). rcm4's tau_cert used TRB_H / (1 - eps_r)^2 (rcm_block_v1.py); replace eps_r by delta.
- C-MHAT's check: pk07's kt_s9h_v1_2 (848d7376, l.3975-3976) writes m-hat(t) = 1 + m1 t + m2 t^2 + m3 t^3 and requires m1, m2,
  m3 >= 0 by exact comparison, so m-hat >= 1 for every t >= 0; m1, m2 and m3 are the numbers of the pinned vacuum-residual record that
  its C-TRIAL returns. None of the kt_s9h_v1_2 run outputs in pk07/out/ prints C-MHAT, so the engine either cites a run output that
  does, or runs the same exact comparison itself on that pinned record, as a gate.
- The same factor appears in pk07's beta_H (kt_s9h_v1_2 bh_bound, l.3987-3993), which notes the erratum e48d0812: lambda_0 >=
  (1 - eps_r) m-hat already holds by Lemma 19.2 (c), so 1/(1 - eps_r)^2 would also do. The delta form is kept here for the same reason
  as there: it is sound, negligibly looser, and the number S8's chain uses.
- Gates per piece: delta < 1; tau' > 0; and the float engine's J1 and J2 (Jensen; they also carry alpha_lo's monotonicity, sect. 2), B3, TR and T0.
- The other inputs stay as in the float engine: eps_H = c_N / J_lo; rho_1 the certified P2 row's rho1_hi; alpha_lo = (N - 1)/2 - chi (1 + (N - 1)
  t_max / 2) + chi^2 t_max / 2 at chi = ce_hi, pk15's certified upper end of c; TRB_H the rule's J-uniform value for row T
  (0.527562 at N4, 0.355588 at N3).

## 5. C-4: the dual run
- No horizontal chain may carry the vertical chain's ch['dual'], because s8core's sf_pair reads it (s8core l.683-691). Every
  chain dict built from S8's chain (dict(chV), dict(chU); chain_h_fix l.1421, the scan's chHe) either drops it, as the float readings
  do, or replaces it by its own triple (chd_H, chm_H, rad) from sect. 2's two runs. The certified engine does the second.
- C-DUAL-OWN (gate, each piece): the horizontal chain's midpoint run reproduces its own centered slot-0 and slot-1 states (chm_H's
  y(0) and y(1) inside chc_H's), and chd_H's value balls hold them. PLANT-DUAL-SWAP: the vertical chain's dual placed in the horizontal
  chain must fail C-DUAL-OWN. The float engine shows what the slip does: with the vertical dual, the FLIP/SAME rows read 1.04 to 1.48
  instead of 3.69 or more (rcm1 and rcm2, against rcm3).
- C-DUAL-KEYS (gate). S8core's _cen pairs each gradient with its radius by position, through zip (s8core l.967-984),
  and zip stops silently at the shorter list. So every dual run carries its slot key list: 't' first, then each entry's bar slot, in the
  box's key order. Before every _cen, and before every combination of duals from two runs (the pair form's Num and Z take a left and a
  right side), the engine checks that each dual's slot keys equal the run's box key list in length and in order. It does so on both
  sides of every pair, the vertical side included after its zero padding. A mismatch raises ValueError and fails the piece.
- Plants for C-DUAL-KEYS: PLANT-DUAL-KEYS-SWAP (a dual with two slots swapped) and PLANT-DUAL-KEYS-DROP (a dual with one slot dropped)
  must each fail. C-MV-H cannot stand in for this gate, because a permutation of slots whose radii differ little passes it (as the review's
  note found).
- Checklist (last sentence): find every site in pk22's engines where a chain dict is copied from the certified chain,
  and confirm at each that 'dual' is replaced or dropped.

## 6. n = 5 (Q1 yes, Q2 the four filters, MUST-FIX N5-1)
- Filters: n = dL + dR + m + 3 >= 5 for H2 and n = iH + dV + m + 3 >= 5 for M2 HV, in the four row builders (rcm5's diff
  pk24/ne/diff_rcm5_vs_rcm4_v1.txt, 34983345). Nothing else in the reading depends on n (Q2).
- N5-1: the t = 0 harmonic controls must enumerate n in {5, 6, 7, 8}. Four sites list (6, 7, 8) today (rcm5 6fce793b l.1282 and
  l.1294 in harm_check_rc, l.1566 in harm_check_m, l.1627 in the C-HARM-H block); harm() evaluates n = 5 too. With n = 5 in the lists,
  PLANT-RC, PLANT-RES-M and PLANT-RES-H must still fire.
- C-REPRO-RC5 goes into the certified engine (the form of rcm6's block, src/rcm6_loop_v1.py): at the first piece of each N, P2-13's
  exact float value of each of the 18 n = 5 keys must lie inside RC's certified [lo, hi]. PLANT-REPRO-RC5: the same check with each
  exact value replaced by hi + |hi| / 100 must fail for every key.
- The record carries the map from the 58 separated D0 pairs to their classes (pk24/n5/n5map_v1.py, built from C-REPRO-H's and
  C-REPRO-M's maps) and prints every n = 5 key's row on every piece. No n = 5 key may rest on a top-mode cover: N5ABSENT = 0 is a gate.
- The docstrings must lose every "n >= 6". The 22 joint D0 pairs at n = 5 (m <= 0) are no chain class; they stay with the
  box, with W1a's joint routes as their fallback.

## 7. Coverage list: what the record must carry, for each N and each piece
- FLIP/SAME, both edges horizontal in the top and bottom rows (rows_h_rc):
  - H2 (dL, dR, kind, m): dL and dR in {0, 1, 2} for flip and in {0, 1} for same; every m >= 1 with n >= 5 and m < m0(dL, dR, kind);
    from m0 on, the top-mode form (dk_class).
  - Hinf (dL, inf, kind, m) for m < m0(dL, inf, kind); the top-mode form beyond.
  - H1 (dL, far, kind, m): the larger lower end of route A (the far bound from DF[kind]) and route B (DF..DF+2 explicit, the far bound
    from DF + 3), with DF = 3 for flip and 2 for same; for m < m0(dL, far, kind) (dk_class_h), the top-mode form beyond.
  - F-b: every dL of DN[kind]. pk22's v2d scanned slot 1 only under option (a') (v2d l.1228 and l.1267).
- MIXED, one horizontal and one vertical edge (rows_mixed_rc; T_M = 3 at N4 and 2 at N3; same = t with a, flip = t with b):
  - M2 HV (iH, dV, kind, m): iH in 0..T_M, dV in -1..T_M - 1, n >= 5, m < m0; the top-mode form (dk_class2) beyond.
  - Minf HV (iH, inf, kind, m), and M1 HV (iH, far, kind, m) with S8's vertical far bound from DF_V = T_M (route B where its slots
    exist).
  - Minf VH (dV, inf, kind, m), and M1 VH (dV, far, kind, m) with far_lo2_h from DF_H = T_M + 1 (route B where its slots exist).
- F-a: every flip class takes the bottom-row vectors as the parity mirror of the top-row ones (mir with the chain's parity signs, as
  rc_chain_m does for BH at l.1479-1483, and opt_a_chain_mb), in the centres and in the boxes. v2d's unmirrored MB (l.665 against
  l.294) is wrong.
- Slots: horizontal slots 0 and 1 from the exact entries, slots 2..7 by RC (rc_chain_m l.1460), and inf (pc with radius rho[inf]);
  vertical slots -1 up to S8's DMAX.
- Every class needs a top-mode cover with m0 <= MM; a class without one fails its piece (S8's KILL rule).
- Pieces: P2's grid as S8's (piece ratio <= 1.0025 on [300, 400] and <= 1.01 beyond, J_max >= 1e6, then [J_max, inf) as one piece to
  t = 0).

## 8. Controls and plants (gates unless marked INFO)
- Kept from the float engine: C-HASH (every input by full sha256); C-GRID (S8's pieces and pk15's export share every J_lo); C-HARM-RC with
  PLANT-RC (tau' = 0); C-HARM-H-M with PLANT-RES-M; C-HARM-H with PLANT-RES-H and PLANT-END-H, all three on n = 5..8 (sect. 6); RCXW
  (INFO: the W'-block eigenvalues of R lie in [0, tau']); C-MIXED-REG with its plant; C-REPRO-H; C-REPRO-M; C-REPRO-RC5 with its plant;
  and the consistency gate (each row's centre value inside its [lo, hi], M1CONS in rcm4).
- New, for sect. 2: C-MV-H (thin point chains at 9 sample t of the piece, zero bars, inside the centered horizontal chain leaf by
  leaf, under the 2^-20 rule); C-MV-BAR-H (each bar offset pinned in END_MODES); C-UNIF-H (the ten entries' enclosures over the box
  against thin entry values); C-PIECE-H (on each half of a piece, no row's lower end below the parent's and no m0 larger); C-TARGET-H
  (the centered RC rows of smallest headroom against thin points). Plants: PLANT-MV-H (t-gradients set to 0 must fail),
  PLANT-UNIF-SLACK-H and PLANT-PIECE-H (the parent's box collapsed to its right end must fail on rows).
- New, for sects. 3 to 5: C-FMT on the new records (key-swap plants); C-DUAL-OWN with PLANT-DUAL-SWAP; C-DUAL-KEYS with
  PLANT-DUAL-KEYS-SWAP and PLANT-DUAL-KEYS-DROP; C-MHAT (sect. 4); per piece the gates of sect. 4,
  c_fix inside the certified c box, route (b)'s tau_B > 0 (S8's), and s8core's C5 and C6 errors (_pos, _nz, _cen), each of which fails
  its piece.

## 9. The record and its verdict
- Per piece: the gates, then every row with its family, class key, m, certified lower end, upper end, centre value (INFO) and headroom.
  Rows with headroom below 2 print RISK lines; the rule for the readings is headroom >= 2 on every row.
- A piece fails (verdict INVALID) on any row with lower end <= 0, any class without a top-mode cover, any failing gate, or a C5 or C6
  error.
- Per class and per N: the smallest headroom and its piece; the n = 5 rows at the actual bars; N5ABSENT = 0.
- For the review: per class and piece, the pair form's constants t1, ddet, lin and dz, with the duals' centred Num and Z,
  as S8's class-level record prints them (s8core sf_pair's info dict), so that each lower end can be rebuilt by hand.
- The pair-to-class map: for each pair, the class and the image that reaches it (direct, left-right reflection, T <-> B
  flip, or both), so that each two-sided VH pair shows as the mirrored HV class it is.
- The run goes in chunks as S8's certified run (each job under 10 minutes), with a final item that runs C-PIECE-H at each family's
  binding piece and at the first and last covered pieces. The record is frozen with chmod a-w and a manifest.

## 10. Bar readings (float; certified inputs; 18 pieces per N)
```
spec/out/bar7_sum_v1.out (rcm7, twelve bar readings per N):
cols: N | bar fT/hT, S4 HT | all rows: failing / rows, smallest (row) | n = 5 rows: failing pieces, smallest (class) | non-box orbits G15 G11 G16 G08
N4 | 0.0001, 5e-05 | 0 / 5378, 2.852 (M1 ('VH', 2, 'far', 'flip', 1)) | 0, 2.893 (M2 ('HV', 0, 1, 'flip', 1)) | G15 7.434 G11 9.757 G16 6.535 G08 5.784
N4 | 0.00015, 5e-05 | 0 / 5394, 2.691 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.691 (M2 ('HV', 0, 1, 'flip', 1)) | G15 6.947 G11 9.379 G16 6.281 G08 5.326
N4 | 0.0002, 5e-05 | 0 / 5422, 2.518 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.518 (M2 ('HV', 0, 1, 'flip', 1)) | G15 6.525 G11 9.034 G16 6.05 G08 4.938
N4 | 0.00025, 5e-05 | 0 / 5472, 2.367 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.367 (M2 ('HV', 0, 1, 'flip', 1)) | G15 6.158 G11 8.718 G16 5.839 G08 4.604
N4 | 0.0003, 5e-05 | 0 / 5494, 2.236 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.236 (M2 ('HV', 0, 1, 'flip', 1)) | G15 5.833 G11 8.428 G16 5.645 G08 4.314
N4 | 0.0001, 0.0001 | 0 / 5448, 2.237 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.237 (M2 ('HV', 0, 1, 'flip', 1)) | G15 5.886 G11 8.381 G16 5.613 G08 4.018
N4 | 0.0001, 0.0002 | 18 / 5515, 1.674 (M2 ('HV', 0, 1, 'flip', 1)) | 18, 1.674 (M2 ('HV', 0, 1, 'flip', 1)) | G15 4.496 G11 6.917 G16 4.632 G08 2.606
N4 | 0.0002, 0.0001 | 0 / 5504, 2.029 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.029 (M2 ('HV', 0, 1, 'flip', 1)) | G15 5.358 G11 7.898 G16 5.29 G08 3.613
N4 | 0.0003, 0.0001 | 18 / 5532, 1.858 (M2 ('HV', 0, 1, 'flip', 1)) | 18, 1.858 (M2 ('HV', 0, 1, 'flip', 1)) | G15 4.922 G11 7.474 G16 5.006 G08 3.282
N4 | 0.0005, 0.00015 | 18 / 5599, 1.433 (M2 ('HV', 0, 1, 'flip', 1)) | 18, 1.433 (M2 ('HV', 0, 1, 'flip', 1)) | G15 3.842 G11 6.259 G16 4.192 G08 2.344
N4 | 0.0007, 0.0002 | 36 / 5779, 1.19 (M2 ('HV', 0, 1, 'flip', 1)) | 36, 1.19 (M2 ('HV', 0, 1, 'flip', 1)) | G15 3.209 G11 5.464 G16 3.659 G08 1.838
N4 | 0.001, 0.0003 | 70 / 5968, 0.9434 (M2 ('HV', 0, 1, 'flip', 1)) | 36, 0.9434 (M2 ('HV', 0, 1, 'flip', 1)) | G15 2.561 G11 4.568 G16 3.059 G08 1.342
N3 | 0.0001, 5e-05 | 0 / 3362, 3.728 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 3.728 (M2 ('HV', 0, 1, 'flip', 1)) | G15 7.94 G11 10.81 G16 7.237 G08 5.722
N3 | 0.00015, 5e-05 | 0 / 3397, 3.401 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 3.401 (M2 ('HV', 0, 1, 'flip', 1)) | G15 7.341 G11 10.31 G16 6.905 G08 5.234
N3 | 0.0002, 5e-05 | 0 / 3432, 3.13 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 3.13 (M2 ('HV', 0, 1, 'flip', 1)) | G15 6.832 G11 9.864 G16 6.606 G08 4.825
N3 | 0.00025, 5e-05 | 0 / 3451, 2.902 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.902 (M2 ('HV', 0, 1, 'flip', 1)) | G15 6.395 G11 9.46 G16 6.335 G08 4.476
N3 | 0.0003, 5e-05 | 0 / 3470, 2.706 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.706 (M2 ('HV', 0, 1, 'flip', 1)) | G15 6.014 G11 9.091 G16 6.088 G08 4.175
N3 | 0.0001, 0.0001 | 0 / 3434, 2.872 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.872 (M2 ('HV', 0, 1, 'flip', 1)) | G15 6.197 G11 9.131 G16 6.115 G08 3.886
N3 | 0.0001, 0.0002 | 0 / 3462, 2.148 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.148 (M2 ('HV', 0, 1, 'flip', 1)) | G15 4.687 G11 7.423 G16 4.971 G08 2.473
N3 | 0.0002, 0.0001 | 0 / 3459, 2.531 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.531 (M2 ('HV', 0, 1, 'flip', 1)) | G15 5.561 G11 8.513 G16 5.701 G08 3.47
N3 | 0.0003, 0.0001 | 0 / 3488, 2.265 (M2 ('HV', 0, 1, 'flip', 1)) | 0, 2.265 (M2 ('HV', 0, 1, 'flip', 1)) | G15 5.048 G11 7.98 G16 5.344 G08 3.135
N3 | 0.0005, 0.00015 | 18 / 3619, 1.699 (M2 ('HV', 0, 1, 'flip', 1)) | 18, 1.699 (M2 ('HV', 0, 1, 'flip', 1)) | G15 3.865 G11 6.549 G16 4.385 G08 2.206
N3 | 0.0007, 0.0002 | 36 / 3697, 1.384 (M2 ('HV', 0, 1, 'flip', 1)) | 36, 1.384 (M2 ('HV', 0, 1, 'flip', 1)) | G15 3.189 G11 5.637 G16 3.775 G08 1.714
N3 | 0.001, 0.0003 | 50 / 3884, 1.077 (M2 ('HV', 0, 1, 'flip', 1)) | 50, 1.077 (M2 ('HV', 0, 1, 'flip', 1)) | G15 2.514 G11 4.641 G16 3.108 G08 1.24

ne/out/out_kt_s8hf_rcm6_n4_scan.out, rcm6 (n >= 5): the READING lines
READING M1 bar (fT/hT 0.0001, S4 HT 5e-05) (primary): 0 of 5378 rows fail the rule; smallest headroom 2.852 at piece 61 M1 ('VH', 2, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 3e-05, S4 HT 2e-05) (INFO): 0 of 5337 rows fail the rule; smallest headroom 2.956 at piece 61 M1 ('VH', 2, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 0.0003, S4 HT 0.0001) (INFO): 18 of 5532 rows fail the rule; smallest headroom 1.858 at piece 61 M2 ('HV', 0, 1, 'flip', 1); failing classes [('M2', 'HV', 0, 1, 'flip')]
READING M1 bar (fT/hT 0.001, S4 HT 0.0003) (INFO): 70 of 5968 rows fail the rule; smallest headroom 0.9434 at piece 61 M2 ('HV', 0, 1, 'flip', 1); failing classes [('H1', 0, 'far', 'same'), ('H2', 0, 0, 'flip'), ('M1', 'VH', 1, 'far', 'flip'), ('M1', 'VH', 2, 'far', 'flip'), ('M2', 'HV', 0, 1, 'flip')]
READING M1 bar (fT/hT 0, S4 HT 0) (INFO): 0 of 5314 rows fail the rule; smallest headroom 3.003 at piece 61 M1 ('VH', 2, 'far', 'flip', 1); failing classes none

ne/out/out_kt_s8hf_rcm6_n3_scan.out, rcm6 (n >= 5): the READING lines
READING M1 bar (fT/hT 0.0001, S4 HT 5e-05) (primary): 0 of 3362 rows fail the rule; smallest headroom 3.728 at piece 0 M2 ('HV', 0, 1, 'flip', 1); failing classes none
READING M1 bar (fT/hT 3e-05, S4 HT 2e-05) (INFO): 0 of 3311 rows fail the rule; smallest headroom 4.316 at piece 0 M1 ('VH', 1, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 0.0003, S4 HT 0.0001) (INFO): 0 of 3488 rows fail the rule; smallest headroom 2.265 at piece 0 M2 ('HV', 0, 1, 'flip', 1); failing classes none
READING M1 bar (fT/hT 0.001, S4 HT 0.0003) (INFO): 50 of 3884 rows fail the rule; smallest headroom 1.077 at piece 0 M2 ('HV', 0, 1, 'flip', 1); failing classes [('H2', 0, 0, 'flip'), ('H2', 0, 0, 'same'), ('M2', 'HV', 0, 1, 'flip')]
READING M1 bar (fT/hT 0, S4 HT 0) (INFO): 0 of 3267 rows fail the rule; smallest headroom 4.438 at piece 0 M1 ('VH', 1, 'far', 'flip', 1); failing classes none

ne/out/out_kt_s8hf_rcm4_pk24_n4_scan.out, rcm4 (n >= 6): the READING lines
READING M1 bar (fT/hT 0.0001, S4 HT 5e-05) (primary): 0 of 5054 rows fail the rule; smallest headroom 2.852 at piece 61 M1 ('VH', 2, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 3e-05, S4 HT 2e-05) (INFO): 0 of 5013 rows fail the rule; smallest headroom 2.956 at piece 61 M1 ('VH', 2, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 0.0003, S4 HT 0.0001) (INFO): 0 of 5208 rows fail the rule; smallest headroom 2.592 at piece 61 M1 ('VH', 2, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 0.001, S4 HT 0.0003) (INFO): 34 of 5644 rows fail the rule; smallest headroom 1.842 at piece 61 H1 (0, 'far', 'same', 7); failing classes [('H1', 0, 'far', 'same'), ('M1', 'VH', 1, 'far', 'flip'), ('M1', 'VH', 2, 'far', 'flip')]
READING M1 bar (fT/hT 0, S4 HT 0) (INFO): 0 of 4990 rows fail the rule; smallest headroom 3.003 at piece 61 M1 ('VH', 2, 'far', 'flip', 1); failing classes none

ne/out/out_kt_s8hf_rcm4_pk24_n3_scan.out, rcm4 (n >= 6): the READING lines
READING M1 bar (fT/hT 0.0001, S4 HT 5e-05) (primary): 0 of 3038 rows fail the rule; smallest headroom 4.056 at piece 0 M1 ('VH', 1, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 3e-05, S4 HT 2e-05) (INFO): 0 of 2987 rows fail the rule; smallest headroom 4.316 at piece 0 M1 ('VH', 1, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 0.0003, S4 HT 0.0001) (INFO): 0 of 3164 rows fail the rule; smallest headroom 3.46 at piece 0 M1 ('VH', 1, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 0.001, S4 HT 0.0003) (INFO): 0 of 3560 rows fail the rule; smallest headroom 2.109 at piece 0 M1 ('HV', 0, 'far', 'flip', 1); failing classes none
READING M1 bar (fT/hT 0, S4 HT 0) (INFO): 0 of 2943 rows fail the rule; smallest headroom 4.438 at piece 0 M1 ('VH', 1, 'far', 'flip', 1); failing classes none

spec/out/hent_coef_v1.out: the header and WORST lines (the ten entries' naive t-width on the first piece)
N4: 76 float entries loaded; first piece J_lo 349.356, rad(T) 3.5691e-06 (J_hi = 1.002 J_lo)
N4 WORST naive width over the ten entries: 5.343e-06
N3: 76 float entries loaded; first piece J_lo 300, rad(T) 4.1563e-06 (J_hi = 1.002 J_lo)
N3 WORST naive width over the ten entries: 4.127e-06
```

## 11. Files (sha256, size in bytes, path)
```
8bbbab28897f8b0acee960a16a4ef0f63f82402e2584ba11f12e5750adc34007  22952  pk24/notes_src/NE_RC_CERT_SPEC_body_v1_1.md
74188a3a9bace50e6c5fe19be22333ac8c13b7c88ccb84e90dde48d33efecec4  4974  pk24/tools/assemble_spec_v1_1.py
7128a21c8a3ee0ee863f3c2b4cc287d0808b830dc6d39691a6e1bef35d5721cd  30243  pk24/NE_RC_CERT_SPEC_v1.md
f686a83d52dfa94fa3ba471d2bb91b9ccda569a4f331ce1154b326e0dc73859a  4495  pk24/MANIFEST_NE_RC_CERT_SPEC_v1.sha256
d3d59ce22e288a4a5145d8bc09de166066b37b5701448c8fc0fff8cf84c217e2  113512  pk24/ne/kt_s8hf_rcm4_pk24.py
6fce793bfd0046aaf3db75f27e1798000bcfb154f2239f9301584a0aabb6d2c9  113731  pk24/ne/kt_s8hf_rcm5_pk24.py
4d9fda545a061b0034e5fb1f9f3fdaecaf1e9fd78c27d806978c036671ad33c7  117986  pk24/ne/kt_s8hf_rcm6.py
9f0369f7c814b831b6c6d9d32e1899305664721d97c17058ccc5e2f3ab9abde1  118514  pk24/ne/kt_s8hf_rcm7_pk24.py
349833459544e01feae785fb344795114c9d6a7e752cd109745a430f4ae191bc  2080  pk24/ne/diff_rcm5_vs_rcm4_v1.txt
3f8676322d2422f5f77c1af0f4c0ea8618d4868ad6258ef281dff261922d6c17  5714  pk24/ne/diff_rcm6_vs_rcm5_v1.txt
47a80bb6d2d7cbb3ac239417a9a098748ad8a7a601855824981268f45013b09c  1847  pk24/ne/diff_rcm7_vs_rcm6_v1.txt
210768e6e1af2dc2ccd7e8a231fef2e68282b533d7b38924b7b103dded092366  3033  pk24/ne/make_rcm7_v1.py
079b932c18409d9c5ca5860c7ccf10b8e0e5d496399044e33c7a10044f9edfee  17773  pk24/ne/src/rc_block_v1.py
b80eaf8fa3c035568cfd7c8cd7a3a90a8b1e8fdd167be1396032fe5de84eb3d7  3869  pk24/ne/src/rc2_block_add_v1.py
47aa746cc194f268a44e011111e2de0119a27cc8ac207dcafc04f3a37be4980b  1746  pk24/ne/src/rc2_t0_v1.py
4e5119339b9b9f409837ee2798857540817c00c7ac1af0cd698d5da0e8651a2a  7702  pk24/ne/src/rcm_block_v1.py
ff3ac97247d4ce504ae12500488a03d31c808284b4cdb2f5bd164a6e697bcc48  6369  pk24/ne/src/rcm_scan_v1.py
54df62e08d47c7f4ca5dc9ca11a0a7cfc8197575a1e678e4b13c7c6659c7760d  995  pk24/ne/src/rcm6_fn_v1.py
398db642671c619e8a1d2cd3bdbcb009a0d8273610be36db3a5519db60caa088  1940  pk24/ne/src/rcm6_loop_v1.py
4906cc3070616d16ca3cb88b15bdbe7492e6cb6a9426c487303b672fbc18bd26  1125  pk24/ne/src/rcm6_end_v1.py
4de02e4ce30900739b204d9d3ee9160e8aae55331cab804bfa609908a4773a49  257539  pk24/ne/kt_s8_cert_v1_14_3_pk24.py
fa5fa825531d862dc0c90cf125ad0c451685c024ccde4e5225c3e1b440e53779  56514  pk24/ne/out/out_kt_s8hf_rcm4_pk24_n4_scan.out
10fead680b684811597da8255cc34f7dfc5c41d1eeb31b3b17f4f62052092134  53840  pk24/ne/out/out_kt_s8hf_rcm4_pk24_n3_scan.out
e25b81b0cf07de01367a2b5f4002d04e546f77a46e3e10b70412fe2b1717232e  77099  pk24/ne/out/out_kt_s8hf_rcm6_n4_scan.out
de9142c4df39a48639540bb25d8205507ea1363553de81bbba43987c01592f10  74165  pk24/ne/out/out_kt_s8hf_rcm6_n3_scan.out
33e695d1179e536b329e9447f8325f03e8327921651962f6835045b3c62f8842  132778  pk24/ne/out/out_kt_s8hf_rcm7_pk24_n4_scan.out
e66f8f551d45c6749dd5ed1865993bdf1ec63c5fa952602f062fb676a6122079  129621  pk24/ne/out/out_kt_s8hf_rcm7_pk24_n3_scan.out
3fd59e589b1d2a2bc96564e536d668c57f9b767e9f8c4198318806480e2509a3  2370  pk24/spec/hent_coef_v1.py
49553837045df87915f96f409ee122430b63ab577e1f4a4b564e134e0407df32  3226  pk24/spec/out/hent_coef_v1.out
32822514aade87bec25cc40ecc609fe1095b6417d6d24aa9e1fa567b9caf19fb  2418  pk24/spec/bar7_sum_v1.py
9bcbbed119e72146407e081dbef75fc311efec7dcccb0b2c7ee9349813ef78ba  3731  pk24/spec/out/bar7_sum_v1.out
05473cd1bb215f0214e23bcdb631ab75991f970f3b73b7ab17d4386f25f391a6  8053  pk24/n5/n5map_v1.py
359c33418a268abcb4d8bc698573ea3fa5ce347c4a5ee49c30b2c3ff7ea7e144  22685  pk24/n5/out/n5map_v1.out
865eb3aea94eda3dba8ed71910c92aa608d88d9c5bd8b3830fe479dbb24bc06a  5539  pk24/NE_RC_M1_v1.md
8fb19e9a33cfe5278ca7e75779d931754a0ab3b0800b5a5a65dc8abeb8de9b34  15039  pk24/N5_ROUTES_v1_1_ADD1.md
718ba6b92fdb054e56e45b1c7fcd65ef135a6399acb8aa981ce7c26c5a72dd32  949  pk24/jobs/job16_hent_v1.sh
fb69099f67df4243adbd28da2f6b6528d3d290d7ed83b351b7e80cf4bc18a2ba  2104  pk24/jobs/job17_rcm7_v1.sh
5a3d6ab938e5080d876af22555eb88b5329b9e057c931da29eb2ae9dba9fb324  2595  pk24/jobs/job17_rcm7_v1.console
3d4276002e175d5db717cbfed07deab5b9f779b791972b9b95b0a17bc851ffc1  39125  pk11/SPEC_S8_CERT_v1.md
c82036d8d788e2605154fe0e496955d012df014b3881db61041d70576a6e108a  90177  pk11/s8core_v1_11.py
a6eea55f1f05d1809b7f81be8cbc4aef10d66e9a0e2705a0ba2b93a60bdec604  257027  pk11/kt_s8_cert_v1_14_3.py
7147e76610b6c8ebc5aae056cb9fc88641924c98921b13d74d5ce0b75db476ba  4140  rv01/RULING_P3_BETAH_TRBH_rv01.md
d8ed634143a5118889480c9e9967ea0b43ef82c8adb6367280d35d9e512015bb  5846  (the design review)
9a0a2ffebec9ed9c82e33cba9497ff2f40891314c5a64de1ad369c8d5733865a  3568  (the float engine's review)
280d63c10d3437d1edc72d4f97168af3d4247f4cd654d25e087419c47879d340  5121  (the review of N5_ROUTES)
e215386084879b9f5ccb939f0bb844d55d2509f36d60584f16dd688119fd10d1  5822  (the review of spec v1)
1524a13c45dbfde3edaf507cab31c483ac8286659200713f721a6d017aa4c5af  82460  pk22/w1/s8hf_a/kt_s8hf_v2d_px22.py
848d737688040ca9408b9c06d39cde853132fbbe9b2461a48f5daa2bfa5b1bd9  387702  pk07/kt_s9h_v1_2.py
761084be2333dfe0525c47e5294d62daaa702dcd101312ea5a182cf23574c2c8  671297  pk07/out/export_kt_s9h_v1_2_vsweep.kv
ad7e863d44d48bd59946f48c1de261f51751cd064f6129fc56d85cad9c7ee844  586560  pk15/out/export_p2_t_cert_kt_p2_assembly_v1_37_1.kv
```
MANIFEST_NE_RC_CERT_SPEC_v1_1.sha256 lists the same files and this note, with paths relative to code/ (check it with sha256sum -c from
code/).
