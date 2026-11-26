#!/usr/bin/env python3
"""kt_p212_cert_v1_3_6_2.py -- pk12: kt_p212_cert_v1_3_6_1 (3e368a5e) with the two cert-mode fixes found by its cert
pre (37a77c7f, VERDICT INVALID): PLANT-UHAT-KEYS plants MOCK = TRUE in cert mode, and C-ESEMI-BASE checks in cert mode that no stand-in
base exists instead of calling esemi_base outside refuses. The v1_3_6_2 section at the end of this docstring lists the changes.
v1_3_6_1's header:
kt_p212_cert_v1_3_6_1.py -- pk12: kt_p212_cert_v1_3_6 (9db6bf5c) with UHAT_CERT pinned (the orders on the u-hat
records, pins only): pk02's certified u-hat records from kt_uhat_asm_v1_8 (a69672f3), each bound to its run output by the ruled
RECORD line, all four files pinned in C-HASH. The v1_3_6_1 section at the end of this docstring lists the changes. v1_3_6's header:
kt_p212_cert_v1_3_6.py -- pk12: kt_p212_cert_v1_3_5_5 (ebef74b1) with the cert wiring of the E_main records:
ESEMI_CERT holds pk04's twelve certified records, bound to their asm outputs (ESW_CERT), all pinned in C-HASH; UHAT_CERT stays a
refused slot until pk02's certified u-hat records exist (v1_3_6_1). The v1_3_6 section at the end of this docstring lists the
changes. v1_3_5_5's header:
kt_p212_cert_v1_3_5_5.py -- pk12: kt_p212_cert_v1_3_5_4 (a3e6a2c9) with the two-sided damping of Route 1's
N-error (C-TWO-SIDED), the break-even fix on damped rows and the r1..r49 stray-tag
fallback; the v1_3_5_5 section at the end of this docstring lists the changes. v1_3_5_4's header:
kt_p212_cert_v1_3_5_4.py -- pk12: kt_p212_cert_v1_3_5_3 (ed5c6464) with J-3 closed (tau_1 = C_N tail_h1 fills the TAU1 slot:
pk15 ed0ae46c Claim T), C-MHAT-SRC, the damped q, Q1, Y_1, Y_c and route (ii) at d_L = 0 (
C-Q-DAMP) and the T0 level power on midpoints (the orders of 01:42Z to 01:54Z); the v1_3_5_4 section at the end of this docstring
lists the changes. v1_3_5_3's header:
kt_p212_cert_v1_3_5_3.py -- pk12: kt_p212_cert_v1_3_5_2 (fd1b5081, frozen and never run) with the 01:31Z rule for
C-ESEMI-T0-LEVEL: a gate only at the rows where the T0 plant shows power, INFO elsewhere, with the three misses printed (the v1_3_5_3
section at the end of this docstring). v1_3_5_2's header:
kt_p212_cert_v1_3_5_2.py -- pk12: kt_p212_cert_v1_3_5_1 (3c8b71a9) with D3 at d_L = 0 by Route 1 of the review's
RULING_D3_DL0_CHAIN_LEVEL 90d302d8 (the choice), C-LEVEL, the T0 level plant, the RULING_T202_QS_TD_SG1_V2 141eb691 (F-A, F-B,
J-1, J-2 and the TD single-bond g-terms), the TAU1 slot and the reviewed production runner pin (the orders after the v1_3_5_1 pre);
the v1_3_5_2 section at the end of this docstring lists the changes. v1_3_5_1's header:
kt_p212_cert_v1_3_5_1.py -- pk12: kt_p212_cert_v1_3_5 (ce668ab3) with the vertical bond's U from the CONFIRM_UV_VERTICAL_BOND
851f6ba4 sect. 3, pk02's N*_QE_HI and N*_QF_HI at d_L = -1 (QEF_DLM1_v1_1_r2) and pk04's six N4 MOCK E_main records from
E_semi v1_3 (the messages after the v1_3_5 freeze); the v1_3_5_1 section at the end of this docstring lists the changes. v1_3_5's
header:
kt_p212_cert_v1_3_5.py -- pk12: kt_p212_cert_v1_3_4 (35cc2da6) with the truncated-Cov error terms (the approval after pk12's hand
correction, cap 1.5 h): R_e and R_f at the d_L <= 0 E_main rows and the product term at d_L >= 1 (the erratum 4f34050b and
rule 6e38bd40); the v1_3_5 section at the end of this docstring lists the changes. v1_3_4's header:
kt_p212_cert_v1_3_4.py -- pk12: kt_p212_cert_v1_3_3 (46e37091) with the E_main code under the v1_3 cap (the approval, the reply to
pk12's SEND_042 9698593a), the final's RECORD line in the ruled form; the v1_3_4 section at the end of this
docstring lists the changes. v1_3_3's header:
kt_p212_cert_v1_3_3.py -- pk12: kt_p212_cert_v1_3_2 (7b0f954d) with the u-hat MOCK pins moved to pk02's re-issued records
(kt_uhat_asm_v1_5, ea857895: outward rounding fixed, C-DEC-UP), per the decision of 21:24Z, option (a); the reader's strict check stays
and nothing else changes (pins-only). v1_3_2's header:
kt_p212_cert_v1_3_2.py -- pk12 (code/pk12/), the reader revision of kt_p212_cert_v1_3_1 (52700ed4
5724f3e1 and the review b1048ba8), the approval of 2026-11-08 21:03Z (cap 2.0 h), written by a pinned generator from v1_3_1. v1_3_1's
text follows unchanged up to the v1_3_2 section at its end. v1_3_1's header: kt_p212_cert_v1_3 (224c7353,
pk11, frozen, never run) with the claim rule of 2026-11-08 19:41Z folded in (handoff 8cb27b10 items 1 and 3; the brief to
pk12), written by a pinned generator from v1_3. v1_3's text follows unchanged up to the v1_3_1 section at its end.
v1_3: the cert revision of kt_p212_cert_v1_2_2 (24a59e32), the approval of 2026-11-08
(19:2xZ, cap raised to 2.5 h at 19:38Z), per PLAN_P2_12_R6_5_v2 (d4361948) with ADD1..ADD10 and ADD11 (this revision's addendum).
It folds in the review (b5c9684f) and the e2efe981 with the rules:
- PLANT-L0-HI-DOWN counts only a refusal by C-L0-HI (every plant now names the gate whose refusal it needs).
- C-CV at every piece (||C^ v||^2 against v^T Gq^-1 v from the piece's own g entries at the box centre, as balls that must
  overlap) with a self-calibrating PLANT-CV; C-T-CS in plan v1's cross-input form, |alpha . C^ v-hat| <= ||alpha||_2 q_use(D4-L0), with
  PLANT-T-CS (a dot of 1.1 times the bound must fail).
- the d_L = 0 readings are checked by value after any override (Q1 is the piece's Qa ball, q is U + nX Qa, beta's E_semi is
  Cov_inf_hi + Qa U from the means export); each plant feeds a wrong value.
- (revised; pk02 ADD3 5e8bce50 l.77-78): C-CENTRES reads centres.source (the means export by full sha256) and
  centres.pieces (P0000..P<last>) and checks both against the engine's pinned means export and piece range, with plants.
- rule V2 for the u-hat record (its writer's run output pinned: VERDICT lines exactly [VERDICT VALID] and a RECORD line naming the
  record's full sha256); the same strict form for R4's and record 895634f5's run outputs. Cert mode takes kappa as an upper
  end from v1_37_1's C-NA line (kappa_max, dec_hi) and Phi_eps from its PHI-EPS line (f5410931, rule V2); C-KAPPA-GE1 is never read.
- q_hat_hi, m_hat_s_hi, eps_r and T_v must be >= 0 (PLANT-NEG-INPUT). From e2efe981: the 64-column 'far' and
  'inf' rows' Cov carries a truncation radius R_TRUNC = 1e-20 (source: e2efe981, the gapped modes mu = 1, 3 feel the end at
  about 8e-26).
- C-F4 per piece (F4 inside the HS D3 box value), C-HS-MIN (pre, every export piece), PLANT-F4 and PLANT-ROW.
- the record carries FAILING_ROWS and is written only after the last gate, with VERDICT VALID. Also, the
  kill rule's INFO line and the break-evens' second column read ADD10 sect. 5's tolerances (8aa8160f), not ADD9's.
- the review a21b717c (Q-1) with the approval of 19:38Z: the d_L <= 0 base is esemi_base(): cert mode needs E_semi's certified lower end per
  piece from pk03's entry record (S8 entry form, rule V2; not pinned yet, so cert mode is refused); mock mode keeps the row's t = 0
  harmonic Cov as a labelled stand-in. C-ESEMI-BASE refuses the harmonic Cov in the base slot in cert mode (PLANT-ESEMI-BASE); C-ESEMI-T0
  is INFO. esemi_transfer() is the replaceable u-hat-to-true step, the identity until the review rules (the hold). v1_3's threshold
  Cov(0)/2 is withdrawn in v1_3_1 (below).
Break-evens as v1_2_2 (ADD10 sect. 2) in v1_3; v1_3_1 moves them to lo = 0 (below). Everything else as v1_2_2.
v1_3_1 (the claim rule, 19:41Z; pk14's THMS_MODULE_v2_7.tex l.472-475 claims only Cov > 0, and pk15 traced the factor 2 to
a planning table, pk07/kt_s9h_v1_3_2.py l.119-124, l.3438):
- A row passes iff lo_lo > 0 at every evaluated piece (judge()); there is no Cov/2 threshold. The headroom Cov/(Cov - lo) and the
  margin lo_lo/Cov_hi are INFO. PIECE, ROWMIN, ROW and the record carry the smallest margin with its piece; C-FINAL-REPRO reproduces
  the margins of the three tightest rows per N at their binding pieces; C-ROWMIN-PARSE checks that the final parses every ROWMIN line
  and finds every row.
- Break-evens: the largest x with lo_lo >= theta Cov_hi, at theta = 0 (the claim, lo = 0) and, as an INFO column 'be12', at the
  planning level h = 1.2 (theta = 1/6, lo = Cov/6), every other input at the record's value. B3 and A2, lo = a - b x:
  x* = (a_lo - theta Cov_hi) / b. d_L <= 0, lo = base - (c1 x + c0) / den: x* = (Rmax den - c0_hi) / c1 with Rmax = base_lo -
  theta Cov_hi (den_lo when Rmax >= 0, den_hi otherwise). sdiv() divides a numerator >= 0 by b_hi and a negative one by b_lo, so x* is
  on the safe side in both cases. A negative x* means that no x >= 0 passes; 'inf' means no limit. TB, TC and TD as v1_2_2 (U* from
  q*). 'tol' keeps ADD10 sect. 5's q_tol for the other window (8aa8160f, as v1_3). New 'alt', for the A2 rows that read both windows:
  the D4-L0 q* with D4M-L0 at the record's value, per piece (ADD10 sect. 4.4's chord values below the record are
  not safe); in D4M (d,far) the far T_FA's D4-L0 term enters its slope.
- T_v break-even: in the A2 rows whose T_FA reads the dot term (D4 at every d_R, D4M at finite d_R), lo_lo = r +
  T_FA_lo(T_v) with T_FA_lo = min(x, fac x) and x = dot_lo - ||alpha||_2 T_v (tfa_lo), piecewise affine in T_v: T_v* = (dot_lo + r) /
  ||alpha|| when r >= 0 and (dot_lo + r / fac) / ||alpha|| when r < 0, r being the rest of lo_lo less theta Cov_hi (tv_star). Column
  'tv' in ROWMIN, ROW and ROWBE (A2 rows), and a BE-MIN line.
- PLANT-ROW calibrates its factor at lo = 0: F = Cov_lo / R_hi with R = Cov - lo.
- E_semi frame as v1_3 (the brief to pk12). The rule 2414bd75 sect. 1: no transfer, so esemi_transfer stays the
  identity; E_main = N/D and C-ESEMI-NORM wait for pk03's entry record.
- Paths: pk11's frozen inputs are read in place (SRC); the outputs go to code/pk12/ (OWN). The pinned S8 cert module (a6eea55f)
  has its own OWN fixed, so its import stray still goes to pk11/out/, as in every earlier run.
v1_3_2 (the approval 21:03Z): the reader of INTERFACE_UHAT_R65_v1_4 (81c7561f) and the rules since v1_3_1.
- The u-hat reader follows interface v1_4 sect. 5's reader list: the header's tags (MOCK TRUE in mock mode, FALSE in cert mode;
  VERDICT_OF_WRITER VALID; N), exact pins of INTERFACE, ROWS (R65_D3_ROUTE0_ROWS_v1, 6afdb5dd), M2B, centres.source, centres.pieces and
  J_RANGE per N, a whitelist of keys (info.* skipped; any wmat_hat key refused), the forms of sect. 1 (dec, up, ball
  "lo hi", tag, src), END as the last line and the WORLD lists exactly. eps_r and s come from M2B and must lie in [0, 1); every up value
  is >= 0, and T_s and T_U4 are > 0 (widened by the review).
- Route 0 per row: each D3 route-0 row of ROWS_N<N> reads its own block route0b_hat.<row> (route P with formula ROUTE_P_UHAT_v1 and T_s
  only, or route H with ROUTE_H_NB1 and T_U4 only), recomputes q_b_hi by its formula, and takes the max; eval_rows takes the row's own U.
  C-ROWS: the engine's own B3/TB/TD row set equals ROWS_N<N> and COUNT_N<N>; PLANT-ROWS drops one row.
- Rule V2, strict: the writer's run output has exactly one RECORD line naming the record, in the form
  "RECORD <file name> sha256 <full sha256>", and exactly one VERDICT line, "VERDICT VALID", as its last line.
- The crude (1,1) reading (the review 1920fa90 (3) and 803aab31 (d)): N3's D4 (1,1) and D4M (1,1) are A2 rows marked by the
  crude cross-term bound nX e_L e_R; N4's two stay wait-W, with their crude margin printed as INFO (CRUDE11).
- at d_L <= 0, R = [q rn1_R + s' q + (s'^2/2)|E| + sigma_g + |E| (Q1 rn1_R + delta_tr)] / (1 - Q1 rn1_R - delta_tr), with
  delta_tr = s' Q1 + s'^2 (+ u^2 eps_r Y_1 for TD) and |E| the row's |E_semi| ball (TD's term multiplies |E|, not the harmonic Cov).
- C-S8-STAGEA: run_A's stage-A lists come back empty; PLANT-S8-STAGEA.
- sdiv returns NEG_MARKER when a negative numerator meets a b with b_lo <= 0; PLANT-F4 plants an F4 above
  box_f4; C-FIELDS (the FIELDS lines of both exports and of the HS records, and v3's type-A boxes equal to v2's) and
  C-S8-PAREXACT (both of S8's chains parity-exact at every piece; the set used is printed), each with a plant.
- The 'far' side: efar = Rw_hi rho1_hi^7 bounds rn1 and |eps_W| at every level >= 6, i.e. every d_R >= 7 (SPEC_S8_CERT_v1 c0f95398
  l.106, l.122-123, l.200: e_d = min(R_w rho1^d, |Q0 l(d-1)|) with d = level + 1; the review 803aab31 (b)); C-FAR-CITE checks those lines.
- R_TRUNC's source: the review 1920fa90 (1), |T_64 - T_inf| <= 8.3e-48.
- KILL-RULE INFO gives way to COMPARE INFO: the record's values against this run's own lo = 0 minima (ADD11 sect. 7).
v1_3_4 (the approval, the reply to SEND_042; under the v1_3 cap):
- E_main records (pk04, in the layout of pk12's SEND_029/033/036): one per class, d_L and N; keys ES,<mono>,<k> with mono in
  1, e, f, ef and k = 0..3, raw monomial windows I(J)/main(J) in S8's entry form. They are read through m3_reader_v6_3: its binding
  (_bound: VERDICT lines exactly ['VERDICT VALID'] and one 'RECORD <name> <sha256>' line), in mock mode its item check (_items) on the
  MOCK form (M3_RECORD_v1_MOCK, claim 'MOCK ' + CERT_CLAIM, EXPORT_STATUS MOCK), in cert mode loads. Gates: C-ESEMI-SRC, -FORM-M, -KEYS,
  -USES (each item lists the use the engine reads it for), -NORM (each item's shape is the header's, so one main(J) per record; the norm
  twin ES,1,0 is the shape's W1,0), -BONDS (each item's factors against the engine's bonds() in the record's orientation) and -SHARED
  (one window id, one entry), with PLANT-ESEMI-SRC, -ITEMS and -MOCKCERT (the certified parse refuses the MOCK record); C-ESEMI-S8TWIN:
  ES,1,k against S8's own entry of the same window (E3's f,k on V9, the D16 H record's h,k on V12), the a_k balls overlap, with
  PLANT-ESEMI-S8TWIN (another k's twin must not overlap).
- Per piece and record, the windows in s8core's mean-value form (entry_duals, with two more slots for the bulk centres c_e, c_f, the
  means export's balls of the row's family): W_X = W[ef] - c_f W[e] - c_e W[f] + c_e c_f W[1], W_e = W[e] - c_e W[1], W_f = W[f] -
  c_f W[1] and W_1, each with N = W[cp_0] + alpha . C^ v-hat[W] at S8's right level (2414bd75 sect. 1): E_X = N_X/D, m_e = N_e/D,
  m_f = N_f/D, with D = N_1 and a lower end of D > 0 (C-ESEMI-DPOS).
- The base is the truncated covariance that S9(i) claims, Cov_main = E_X - m_e m_f = N_ef/D - (N_e/D)(N_f/D) (pk12 SEND_042: the
  bulk-centred E_X exceeds it by (E[e] - c_e)(E[f] - c_f), 1.29e-2 against Cov 1.13e-2 at N4 D4 d_L = -1). R_X as ruled (1920fa90
  ), with |E| the upper end of |E_X|, the ball that R_X bounds. 'far' reads the vacuum term, with nc = e_far ||C^ v-hat[W_X]||/D in
  R_X's numerator and nd = e_far ||C^ v-hat[W_1]||/D in its numerator (times |E|) and its denominator (1920fa90 sect. 2); 'inf' reads
  the vacuum term alone. R_e and R_f, the errors of the two single-bond means, are a slot: cert mode refuses (C-ESEMI-RE) until the review
  rules and q_e, q_f are pinned; mock mode leaves them out under the label MOCK-NO-RE-RF.
- C-ESEMI-T0 at the last piece: every E_main row's harm_ball (t = 0) lies in [Cov_main_lo - R_hi, Cov_main_hi + R_hi] (in mock mode R
  is R_X alone), with PLANT-ESEMI-T0-BASE (E_X in place of Cov_main must fail). 2414bd75's in-span plant has no power at the last piece
  (the finite-strip correction, about 1.1e-5 at D4 (0,2), is far below R, 6.9e-4 there), so the vacuum-only deviations print as INFO.
- Rows without a pinned record keep v1_3_3's t = 0 stand-in in mock mode; cert mode needs a record for every row. The d_L >= 1 forms
  are unchanged (until the review answers on a product term there).
- The final writes the record's line in the ruled form "RECORD <file name> sha256 <full sha256>" on its own line; the other
  lines about the record start with JOINT-RECORD.
- the u-hat record's CODE and LIB srcs must not start with '/' or hold a '..' segment; PLANT-UHAT-PIN adds the case.
v1_3_5 (the approval after pk12's hand correction):
- Per bond, in the chain's normalization over lambda_0 (bond_uw): the horizontal bonds t and bb (bb by the top-bottom reflection) read
  U = p_t = (Vt_hi + Ot_hi)^(1/2), an outward upper end, from pk15's certified t export (pk07's pointer; bound by rule V2 to
  R4OUT's EXPORT line, C-R4-SRC; its rows on the means export's grid, C-UH-PIECE) and W = A + |c| (F4); the vertical bond b reads
  U = N*_TRB r / 2 (v1_3_5_1; v1_3_5 read U = 1 under a citation that does not hold) and W = N*_TRB r + |c| with r =
  1/lam0_lo (pk08's certified TRB run output, C-TRB-SRC). C-UE-LE-WE: U <= W for both bonds of every class.
- d_L >= 1 (A2, B3 and the wait-W INFO rows): lo less the crude product |m_e|_hi |m_f|_hi of the two single-bond mean shifts, |m| <= [O +
  W e_L e_R + (rn1_L + rn1_R) U + W (rn1_L e_R + e_L rn1_R + rn1_L rn1_R)] / (1 - (e_L + rn1_L)(e_R + rn1_R)), O = (e_L + e_R) U
  (prod_term; the break-evens' constants carry it too); PLANT-PROD (the binding row with its product scaled past its lo must fail).
- d_L <= 0, the E_main rows: R_e and R_f, the second reading of the single centred bonds with q_e, |m_e| in place of |E|, the same Q1,
  rn1_R, s', delta_tr and denominator, nc_e = e_far ||C^ v-hat[W_e]||/D on 'far' rows, and for TD the single-trick g-term; lo =
  Cov_main - [R_X + |m_e| R_f + |m_f| R_e + R_e R_f]. q_e at d_L = 0 by route (ii), U + W Qa, checked by value (C-QE-ROUTE2, with its
  plant); at d_L = -1 pk02's N*_QE_HI and N*_QF_HI, a slot (C-QE-SLOT: cert mode refuses; mock mode reads the route (ii) form,
  labelled MOCK-QE-DLM1). The TD single-bond g-term is a slot too (C-SG1-SLOT: cert mode refuses until the review gives its form; mock
  mode reads the joint sigma_g, labelled MOCK-SG1).
- C-ESEMI-T0 reads the full R, in both modes.
v1_3_5_1 (the messages after the v1_3_5 freeze; the review CONFIRM_UV_VERTICAL_BOND_rv02.md 851f6ba4):
- The vertical bond's U is N*_TRB r / 2 per piece, an outward upper end (851f6ba4 sect. 3: xi_b >= 0 gives A_X >= 0, the TRB trace
  bound gives ||A_X|| <= N*_TRB r, and Bhatia-Davis gives ||Q0 A_X u||^2 <= (N*_TRB r)^2 / 4), in the chain's normalization (sect. 1).
  No lemma of S8 is cited for it. UV_CERT is True with no new input; C-UV-BD (by value, at most W, with PLANT-UV-BD) replaces C-UV-SLOT.
- q_e and q_f at d_L = -1 read pk02's QEF_DLM1_v1_1_r2.kv, bound by strict rule V2 to its run output's ruled RECORD line (VERDICT
  counted at line starts only), with C-QEF-SRC, C-QE-DLM1 (by value) and their plants. N*_QF_HI_D4MA already holds the lambda_h/lambda_0
  ratio and is read as it stands. TRICK_DLM1 stays bound as before (two binding forms coexist).
- The MOCK E_main records are pk04's six N4 records from E_semi v1_3 (D4, D4M and D3 at d_L = -1 and 0), and C-ESEMI-RUN's mock
  runner is m3_run_es_v1_3; the D4M and D3 paths run for the first time. ESRUN_CERT stays unset until the review clears.
- The MOCK stand-in labels come from the slot flags (es_standins); the TD single-bond g-term stays a slot (SG1_CERT) until the review gives
  its form. The joint record names the U source and the stand-ins in force.
v1_3_5_2 (the orders after the v1_3_5_1 pre):
- D3 at d_L = 0 by Route 1 (the choice; 90d302d8 sect. 3). The single trick's window [free | int | int | cp_k] puts cp_k on the
  observable's own last column, so alpha sits at level d_R, where X's q and Q1 do not bound the residual (sects. 1-2). The rows keep
  level d_R - 1 and X throughout: E_X, m_e and m_f are the vacuum term alone (es_row's cv0 form), and all of Q0 b(d_R - 1) goes into R,
  with q, q_e, q_f and Q1 times sqrt(e_R^2 + rn1_R^2) in place of rn1_R and the in-span terms ('far': e_R = rn1_R = efar). The v1_3_5_1
  reading (alpha at level d_R - 1) missed harm by 4.0e-5 at D3 (0,2) (its pre, l.371).
- C-LEVEL derives each d_L <= 0 class's pairing from its window (the cp column against the observable's nearest column, from es_bonds)
  and checks the engine's table LEVTREAT, which the rows read (lev_treat). PLANT-LEVEL: D3 at d_L = 0 in span at level d_R with X's q
  and Q1 (the unsound mix), and in span at level d_R - 1, must each be refused.
- C-ESEMI-T0-LEVEL and PLANT-ESEMI-T0-LEVEL (the sect. 5 NOTE): at the finite 'span' rows of the last piece, alpha one level up
  and one level down must miss harm by more than T0_FRAC R (T0_FRAC = 1/1000), and the engine's level must miss less than either.
  INFO C-LEVEL-T0 prints the 'vac' rows' misses with alpha at level d_R - 1 and at level d_R.
- F-A: the s'^2/2 term of R_X reads Es_alpha, the row's pre-E_main bound of the true-vacuum window, and in R_e and R_f it reads
  W sqrt(1 + Qa^2). F-B: q, Q1 and the trick terms are in D_u units, so nc and nd carry k = 1 + delta_tr + Q1 e_R and the denominator
  is 1 - 2 delta_tr - Q1 (e_R + rn1_R) - nd k, the same for R_e and R_f (e_R = 0 where D_m is the vacuum term: 'far', 'inf', 'vac').
- J-1: sigma_g's exact side is Y_c <= sqrt(E2_t - 2 b_lo^2 + b_hi^2) + (A_N + b_hi) Qa (sigma_parts), with no t tail. J-2: C-SG-CENTRE
  (b_lo >= 0, L at least the upper end of |c_bb|) at every TD row, with PLANT-SG-CENTRE.
- The TD single-bond g-terms of sect. 3 (sg_single): sigma_g,e = u^2 (eps Y_c + eps^2)/(1 - s^2), sigma_g,f = u^2 (eps L Y_1 + eps^2 L^2)
  /(1 - s^2) + tau_bb(L); C-SG1 replaces C-SG1-SLOT, and SG1_CERT is True. tau_bb rests on the J-3.
- ESRUN_CERT is m3_run_es_v1_3 3d638b75 with its parts.
- C-TAU1-SLOT (owner pk02): cert mode refuses the TD g-term until tau_bb's one-sided justification is in
  place (TAU1_CERT); mock mode reads the coded tau_bb, labelled MOCK-TAU-BB on the STANDINS line, with its plant.
- C-ESEMI-T0 prints each row's midpoint deviation beside R (INFO C-ESEMI-T0-DEV); the SPAN and THIN lines cover the 'span' rows, and
  the THIN line names the rows where the in-span sum moves the midpoint away from harm.
v1_3_5_3 (before any v1_3_5_2 run):
- C-ESEMI-T0-LEVEL is a gate only at the finite 'span' rows where the T0 plant shows power: both one-level shifts of alpha (down and
  up, inside S8's levels 0 to 5) miss harm by more than T0_FRAC R as ball gaps. There the engine's level must miss less than either
  shift (midpoints). At the other rows the comparison is INFO (INFO C-ESEMI-T0-LEVEL-NOPOWER). Every row prints its three misses.
- PLANT-ESEMI-T0-LEVEL: every 'span' class with a finite row at the last piece has power at one row at least.
v1_3_5_4 (pk15 ed0ae46c; which needs no code change):
- J-3 closed: the TD bb tail is Y tau_1(L), tau_1(L) = C_N tail_h1(N, L), C_N = u kappa^(1/2) (1 + kappa) Phi_eps^(1/2) with
  u = 1/(1 - eps_r(300)), rounded outward (cn_ball): Y_c in the joint form, Y_1 in sigma_g,f, no tail for e = t. kappa_max and Phi_eps
  are the certified upper ends (v1_37_1's cert output f5410931, rule V2) in both modes, and eps_r(300) is M2B's; the rows keep their
  per-piece eps_r in the first term. C-SG-CENTRE adds c_bb's lower end >= 0 (Claim T step T1). C-TAU1 with PLANT-TAU1, and INFO
  C-TAU1-XCHECK against pk15's C_4 and C_3. TAU1_CERT is True, so STANDINS lists nothing.
- C-MHAT-SRC: m-hat >= 1 (step T6) from pk02's out_m2b_asm_v1.out (pinned), which binds M2B by its RECORD line: one passing C-MHAT
  line per N with m1..m3 >= 0. PLANT-MHAT-SRC drops the N4 line.
- C-Q-DAMP: at d_L = 0, Q0 a = eps_0 with ||eps_0|| = R_w, and X*'s first factor Z* damps it. With
  qw = (R_w e_1)^(1/2) and e_1 = min(R_w rho1, sqrt(e(0)^2 + rn1(0)^2)): q = U + min(F4 qw, nX R_w) for D3 and U + min(nHS qw, nX R_w)
  for D4M (Lemma D4's HS bound on Z M); D4 is unchanged. For D3 also Q1 = e_3 = min(R_w rho1^3, sqrt(e(2)^2 + rn1(2)^2)),
  Y_1 = sqrt(1 + R_w e_3) (in delta_tr and sigma_g,f), Y_c's w part (A + |c_t|) qw, and route (ii)'s t term W qw. PLANT-Q-DAMP: e_1 from
  the chain's level 1 is refused, and with e_1 = R_w the damping loses its power.
- C-ESEMI-T0-LEVEL's power is measured on midpoints, the gate's own footing: the certified records' errs widen the
  Cov_main balls past R/1000 (estimate 9a0754ec).
v1_3_5_5:
- Two-sided damping for D3 (0, d_R) under Route 1: X = Z G_T G_B Z*/lambda_0^3 has Z* at both ends, and ||Z* Q0 b||^2 <= lambda_0
  ||Q0 b(d_R - 1)|| ||Q0 b(d_R)|| by the chain recursion S Q0 b(d) = Q0 b(d + 1). The N-error q rnX becomes
  min(U rnX, F4 (rnX rnX')^(1/2)) + min(F4 qw (rnX rnX')^(1/2), nX R_w rnX), with rnX' = min(sqrt(e(d_R)^2 + rn1(d_R)^2), R_w rho1^(d_R+1))
  up to level 5 and R_w rho1^(d_R+1) (efar) beyond, 'far' efar and 'inf' 0 (rnx2). R_e and R_f take the same step with W_H in place of
  F4 and U_b in place of U, for t and bb. D's error stays Q1 rnX with Q1 = e_3. C-TWO-SIDED recomputes rnX' from the chain at the pre's
  pieces; PLANT-TWO-SIDED (rnX' from level d_R - 1) must be refused. Other classes are unchanged (ask before widening).
- The break-even "be" (INFO) subtracts the row's own X part q - U, the damped one at D3 and D4M, and at the two-sided rows it solves
  for U on the branch where U rnX is the smaller term.
- The stray tag for S8's import falls back to r1..r49 for this chunk name once r50..r99 are used; the IMPORT line names the pool.
v1_3_6 (cert wiring, step 1):
- ESEMI_CERT: pk04's twelve certified E_main records (E_semi v1_3 production, m3_run_es_v1_3 3d638b75), N4 and N3, each class and
  d_L, read in cert mode through m3_reader_v6_3.loads with their asm output (ESW_CERT, .4 and .3). ESW is the mode's binding outputs:
  ESW_MOCK in mock mode (the MOCK records' output, as before), ESW_CERT in cert mode. Every record and both asm outputs are pinned by
  full sha256 in C-HASH, so mock runs check them too. ESRUN_CERT is as set in v1_3_5_2.
- The cert-mode check names the unset slots; with ESEMI_CERT set, only UHAT_CERT remains.
- The mock path is unchanged, so the mock readings equal v1_3_5_5's.
v1_3_6_1 (cert wiring, step 2, pins only):
- UHAT_CERT: pk02's certified u-hat records UHAT_ASM_v1_8_N4_c1.kv and UHAT_ASM_v1_8_N3_c1.kv (kt_uhat_asm_v1_8 a69672f3, interface
  v1_4 81c7561f; read VALID by the review b33d44e5 and the review 0478fe02), each with the run output out_kt_uhat_asm_v1_8_n<N>_c1.out that
  binds it by the ruled RECORD line (strict rule V2, C-UHAT-V2). Both records pin the reader's INTERFACE, ROWS, M2B and centres.source,
  with centres.pieces P0061..P0903 (N4) and P0000..P0903 (N3). The flag at the top passes the slot check; the dict below, after CODEDIR,
  replaces it. All four files are pinned in C-HASH, so the mock runs check them too. No other change: with every cert slot set, cert
  mode runs.
v1_3_6_2 (the cert pre of v1_3_6_1, 37a77c7f, read VERDICT INVALID on two cert-mode-only paths):
- PLANT-UHAT-KEYS: the tag sub-plant sets MOCK to the wrong value for the mode, FALSE in mock mode and TRUE in cert mode, so it is refused
  in both modes (in cert mode MOCK = FALSE is the correct value, and v1_3_6_1's plant could not fire there).
- C-ESEMI-BASE: in cert mode the gate checks that esemi_base refuses (C-ESEMI-SRC: every row needs a certified record, and no stand-in
  base exists); mock mode keeps its check of the stand-in's label. v1_3_6_1 called esemi_base outside refuses, and the refusal it raises
  by design in cert mode stopped the pre.
Run: D=/mnt/g2/release/root/code/pk12; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_p212_cert_v1_3_6_2.py mock pre 400 > $D/mocks/out/p212_v1_3_6_2/kt_p212_cert_v1_3_6_2_mock_pre.log 2>&1
  (chunk: ... mock chunk 570 4 61 904; final: ... mock final 300)"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, hashlib, re, math, traceback, importlib.util, json
from fractions import Fraction

USAGE = ('usage: kt_p212_cert_v1_3_6_2.py mock|cert pre|final LIM [rK] | mock|cert grid LIM N [rK] | mock|cert chunk LIM N A B [S] [rK]   '
         '(LIM 10..570)')
_args = sys.argv[1:]
if len(_args) < 3 or _args[0] not in ('mock', 'cert') or _args[1] not in ('pre', 'grid', 'chunk', 'final'):
    print(USAGE)
    sys.exit(2)
MODE, ITEM = _args[0], _args[1]
UHAT_CERT = True    # v1_3_6_1: set; below, after CODEDIR, the dict of pk02's certified records and their run outputs replaces this flag
ESEMI_CERT = True   # v1_3_6: set; below, after CODEDIR, the dict of the twelve pinned certified records replaces this flag
QEF_CERT = True     # v1_3_5_1: pk02's N*_QE_HI and N*_QF_HI per kind at d_L = -1 are pinned (QEF, QEFO below; C-QEF-SRC)
UV_CERT = True      # v1_3_5_1: the vertical U = N*_TRB r / 2 (the review CONFIRM_UV_VERTICAL_BOND 851f6ba4 sect. 3), from pinned inputs
SG1_CERT = True     # v1_3_5_2: the TD single-bond g-terms of the RULING_T202_QS_TD_SG1_V2 141eb691 sect. 3 (tau_bb rests on J-3)
TAU1_CERT = True    # v1_3_5_4: J-3 closed, tau_1 = C_N tail_h1 (pk15 ed0ae46c Claim T; C-TAU1, C-MHAT-SRC)
_unset = [n_ for n_, v_ in (('UHAT_CERT', UHAT_CERT), ('ESEMI_CERT', ESEMI_CERT), ('QEF_CERT', QEF_CERT), ('UV_CERT', UV_CERT),
                            ('SG1_CERT', SG1_CERT), ('TAU1_CERT', TAU1_CERT)) if not v_]   # v1_3_6: the cert check names its unset slots
if MODE == 'cert' and _unset:
    print('cert mode is not in v1_3_6_2: unset cert slots: %s; no file opened' % ', '.join(_unset))
    sys.exit(2)
LIM = int(_args[2]) if re.fullmatch(r'[0-9]{1,3}', _args[2]) else -1
if not (10 <= LIM <= 570):
    print('bad LIM %r (need 10 <= LIM <= 570)' % _args[2])
    sys.exit(2)
_rest = _args[3:]
GRIDN, CHUNK, STRIDE, RTAG = None, None, 1, ''
if ITEM == 'grid':
    if not _rest or _rest[0] not in ('3', '4'):
        print(USAGE)
        sys.exit(2)
    GRIDN = int(_rest[0])
    _rest = _rest[1:]
if ITEM == 'chunk':
    if len(_rest) < 3 or not all(re.fullmatch(r'[0-9]{1,3}', x) for x in _rest[:3]):
        print(USAGE)
        sys.exit(2)
    CHUNK = (int(_rest[0]), int(_rest[1]), int(_rest[2]))
    _rest = _rest[3:]
    if _rest and re.fullmatch(r'[0-9]{1,3}', _rest[0]):
        STRIDE = int(_rest[0])
        _rest = _rest[1:]
    if CHUNK[0] not in (3, 4) or not (0 <= CHUNK[1] < CHUNK[2] <= 904) or not (1 <= STRIDE <= 64):
        print('bad chunk %r stride %d' % (CHUNK, STRIDE))
        sys.exit(2)
if _rest:
    if len(_rest) != 1 or re.fullmatch(r'r[1-9][0-9]?', _rest[0]) is None:
        print(USAGE)
        sys.exit(2)
    RTAG = '_' + _rest[0]

CODEDIR = '/mnt/g2/release/root/code'
SRC = CODEDIR + '/pk11'    # v1_3_1: pk11's frozen inputs, read in place
OWN = CODEDIR + '/pk12'   # v1_3_1: this run's outputs
OUTD = SRC + '/out'
HFD = OUTD + '/s8hf_v1'
OUTP = (OWN + '/mocks/out/p212_v1_3_6_2') if MODE == 'mock' else (OWN + '/out/p212_v1_3_6_2')
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
TAGNAME = ('grid_n%d' % GRIDN) if GRIDN else (('c%d_%04d_%04d_s%d' % (CHUNK + (STRIDE,))) if CHUNK else ITEM)
OUT_PATH = os.path.join(OUTP, 'out_%s_%s_%s%s.out' % (LABEL, MODE, TAGNAME, RTAG))
REC_PATH = os.path.join(OUTP, 'P2_12_JOINT_RECORD_v1%s_%s%s.kv' % ('_MOCK' if MODE == 'mock' else '', LABEL, RTAG))
for p_ in (OUT_PATH, REC_PATH):
    if not (os.path.isdir(OUTP) and os.path.realpath(os.path.dirname(p_)) == os.path.realpath(OUTP)
            and os.path.realpath(OUTP).startswith(os.path.realpath(OWN) + os.sep)):
        print('output directory check failed for %s' % p_)
        sys.exit(2)
FH = open(OUT_PATH, 'x')


def out(line):
    FH.write(line + '\n')
    FH.flush()


def cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


OWN_SHA = sha_file(os.path.abspath(__file__)); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_SELF = '44add3bd4876a3f07b75f5d03368eacf03c397b4765da3ebbd26604a6958e448'; ORIG_DIGEST = '82b8fffd531c5ad33492ad7856ab8891453bbfb0f4b1d6497c6b2a5b2ac3b0ee'; ORIG_UHATKV = {4: 'c839743aef90c629bff13819226ec5877f658bf27db05a6cf99efd80a84e8dfe', 3: '66c4d1e86e7598e70a091b85daea602d1dcbf59c68d5bcf416e9db552bae9705'}  # G-ORIG: option (C), acc2 two-producer acceptance
out('%s sha256 %s MODE=%s ITEM=%s%s LIM=%d%s' % (LABEL, OWN_SHA, MODE, ITEM, (' N=%d' % GRIDN) if GRIDN else
                                               ((' N=%d A=%d B=%d S=%d' % (CHUNK + (STRIDE,))) if CHUNK else ''), LIM, RTAG))

# ---- inputs (full sha256 pins)
CERT = SRC + '/kt_s8_cert_v1_14_3.py'
CORE = SRC + '/s8core_v1_11.py'
S8REC = OUTD + '/s8_record_cert_kt_s8_cert_v1_14_3.kv'
JX = CODEDIR + '/pk15/out/export_p2_14_joint_cert_kt_p2_assembly_v1_37.kv'
MX = CODEDIR + '/pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37.kv'
R4OUT = CODEDIR + '/pk15/out/out_kt_p2_assembly_v1_37_cert.out'
SIGG = CODEDIR + '/pk15/out/out_kt_p2_assembly_v1_37_1_cert.out'
DL1 = CODEDIR + '/pk02/out/TRICK_DLM1_v1_4_r1.kv'
DL1OUT = CODEDIR + '/pk02/out/out_kt_trick_dlm1_v1_4_r1.out'
HS2 = CODEDIR + '/pk08/out/HS_INV_NORMX_v1_d3d4b.kv'
HS3 = CODEDIR + '/pk08/out/HS_INV_NORMX_v1_d3d4ba.kv'
HS1 = CODEDIR + '/pk08/out/HS_INV_NORMX_v1.kv'
TAUR = CODEDIR + '/pk08/out/TAU_D3B_v1.kv'
NOTEB = CODEDIR + '/pk08/HS_TYPEB_LEMMA_NOTE_v1_1.md'
NOTEA = CODEDIR + '/pk08/HS_TYPEB_LEMMA_NOTE_v1_1_ADD1.md'
ADD21 = CODEDIR + '/pk15/SPEC_HS_INV_NORMX_v1_2_ADD2_1.md'
ADD3S = CODEDIR + '/pk15/SPEC_HS_INV_NORMX_v1_2_ADD3.md'
M2B = CODEDIR + '/pk02/M2B_KV_v1.txt'
MHATO = CODEDIR + '/pk02/out/out_m2b_asm_v1.out'   # v1_3_5_4: the M2(b) assembly output that binds M2B; its C-MHAT lines (C-MHAT-SRC)
HZ_CN = {4: ('1988.6420217782920', '1988.642021778291987'), 3: ('169.03428235097744', '169.034282350977434')}   # v1_3_5_4: pk15 01:45Z (with its correction), INFO C-TAU1-XCHECK
SPEC12 = CODEDIR + '/pk02/DESIGN_UHAT_ASM_v1_2.md'
ADD1P = SRC + '/PLAN_P2_12_R6_5_v2_ADD1.md'
ADD10P = SRC + '/PLAN_P2_12_R6_5_v2_ADD10.md'
R0T = {4: HFD + '/TABLE_P2_12_JOINT_SCREEN_ROUTE0_kt_s8rf_v1_n4.tsv', 3: HFD + '/TABLE_P2_12_JOINT_SCREEN_ROUTE0_kt_s8rf_v1_n3.tsv'}
TRK = {4: HFD + '/TABLE_TRICK_kt_trick_v1_n4.tsv', 3: HFD + '/TABLE_TRICK_kt_trick_v1_n3.tsv'}
TRKO = {4: HFD + '/out_kt_trick_v1_n4.out', 3: HFD + '/out_kt_trick_v1_n3.out'}
HJ = {4: HFD + '/out_kt_s8hj_v1_n4.out', 3: HFD + '/out_kt_s8hj_v1_n3.out'}
CFAO = {4: OUTD + '/b4c_v1/out_kt_p212_cfa_v1_n4.out', 3: OUTD + '/b4c_v1/out_kt_p212_cfa_v1_n3.out'}
UHM = {4: CODEDIR + '/pk02/out/UHAT_ASM_v1_5_N4_m1.kv', 3: CODEDIR + '/pk02/out/UHAT_ASM_v1_5_N3_m1.kv'}   # v1_3_3: pk02's MOCK
UHW = {4: CODEDIR + '/pk02/out/out_kt_uhat_asm_v1_5_n4_m1.out', 3: CODEDIR + '/pk02/out/out_kt_uhat_asm_v1_5_n3_m1.out'}   # v1_5 + outputs
UHAT_CERT = {4: (CODEDIR + '/pk02/out/UHAT_ASM_v1_8_N4_c1.kv', CODEDIR + '/pk02/out/out_kt_uhat_asm_v1_8_n4_c1.out'),   # v1_3_6_1: pk02's
             3: (CODEDIR + '/pk02/out/UHAT_ASM_v1_8_N3_c1.kv', CODEDIR + '/pk02/out/out_kt_uhat_asm_v1_8_n3_c1.out')}   # certified records, run outputs
IFACE = CODEDIR + '/pk02/INTERFACE_UHAT_R65_v1_4.md'   # v1_3_2: the frozen interface
ROWSF = OWN + '/R65_D3_ROUTE0_ROWS_v1.kv'              # v1_3_2: the pinned D3 route-0 rows
ADD6 = CODEDIR + '/pk02/DESIGN_UHAT_ASM_v1_3_ADD6.md'  # v1_3_2: T_v's source (T_v = beta-hat s')
SPECS8 = SRC + '/SPEC_S8_CERT_v1.md'                   # v1_3_2: the far bound's lemma lines (C-FAR-CITE)
CT2 = CODEDIR + '/pk15/mocks/out/out_SCRATCH_kt_p2_assembly_v1_34_covtest2_mock.out'
ESM = {(4, 'D4', -1): CODEDIR + '/pk03/out/m3_es_D4_dLm1_N4_J300_MOCK_v1_3.json',    # v1_3_5_1: pk04's six N4 MOCK E_main
       (4, 'D4', 0): CODEDIR + '/pk03/out/m3_es_D4_dL0_N4_J300_MOCK_v1_3.json',      # records from the frozen E_semi v1_3
       (4, 'D4M', -1): CODEDIR + '/pk03/out/m3_es_D4M_dLm1_N4_J300_MOCK_v1_3.json',  # (m3_run_es_v1_3 3d638b75, item ESm.4;
       (4, 'D4M', 0): CODEDIR + '/pk03/out/m3_es_D4M_dL0_N4_J300_MOCK_v1_3.json',    # exact decimals of binary64
       (4, 'D3', -1): CODEDIR + '/pk03/out/m3_es_D3_dLm1_N4_J300_MOCK_v1_3.json',    #
       (4, 'D3', 0): CODEDIR + '/pk03/out/m3_es_D3_dL0_N4_J300_MOCK_v1_3.json'}
ESW_MOCK = {4: CODEDIR + '/pk04/tmp/desk_es_v1_3_ESm.4_d1.out'}                    # v1_3_5_1: the MOCK records' binding run output
ESEMI_CERT = {(4, 'D4', -1): CODEDIR + '/pk03/out/m3_es_D4_dLm1_N4_J300_v1_3.json',     # v1_3_6: pk04's twelve
              (4, 'D4', 0): CODEDIR + '/pk03/out/m3_es_D4_dL0_N4_J300_v1_3.json',       # certified E_main records from the E_semi
              (4, 'D4M', -1): CODEDIR + '/pk03/out/m3_es_D4M_dLm1_N4_J300_v1_3.json',   # v1_3 production (m3_run_es_v1_3 3d638b75;
              (4, 'D4M', 0): CODEDIR + '/pk03/out/m3_es_D4M_dL0_N4_J300_v1_3.json',     # the review, the review), read in cert mode
              (4, 'D3', -1): CODEDIR + '/pk03/out/m3_es_D3_dLm1_N4_J300_v1_3.json',     # through m3_reader_v6_3.loads
              (4, 'D3', 0): CODEDIR + '/pk03/out/m3_es_D3_dL0_N4_J300_v1_3.json',
              (3, 'D4', -1): CODEDIR + '/pk03/out/m3_es_D4_dLm1_N3_J300_v1_3.json',
              (3, 'D4', 0): CODEDIR + '/pk03/out/m3_es_D4_dL0_N3_J300_v1_3.json',
              (3, 'D4M', -1): CODEDIR + '/pk03/out/m3_es_D4M_dLm1_N3_J300_v1_3.json',
              (3, 'D4M', 0): CODEDIR + '/pk03/out/m3_es_D4M_dL0_N3_J300_v1_3.json',
              (3, 'D3', -1): CODEDIR + '/pk03/out/m3_es_D3_dLm1_N3_J300_v1_3.json',
              (3, 'D3', 0): CODEDIR + '/pk03/out/m3_es_D3_dL0_N3_J300_v1_3.json'}
ESW_CERT = {4: CODEDIR + '/pk03/out/m3_run_es_v1_3_asm.4.out', 3: CODEDIR + '/pk03/out/m3_run_es_v1_3_asm.3.out'}   # v1_3_6: their asm outputs
ESW = ESW_MOCK if MODE == 'mock' else ESW_CERT   # v1_3_6: the binding outputs of the mode's records
TX = CODEDIR + '/pk15/out/export_p2_t_cert_kt_p2_assembly_v1_37.kv'   # v1_3_5: p_t = (Vt_hi + Ot_hi)^(1/2), bound by R4OUT (pk07)
TRBO = {4: CODEDIR + '/pk08/out/px08_trbcert_v1_1_n4_asm.out', 3: CODEDIR + '/pk08/out/px08_trbcert_v1_1_n3_asm.out'}   # v1_3_5: N*_TRB
QEF = CODEDIR + '/pk02/out/QEF_DLM1_v1_1_r2.kv'       # v1_3_5_1: N*_QE_HI and N*_QF_HI per kind at d_L = -1 (pk02)
QEFO = CODEDIR + '/pk02/out/out_kt_qef_dlm1_v1_1_r2.out'   # v1_3_5_1: its run output, bound by strict rule V2 (the ruled RECORD line)
PINS = {
    CERT: '34b2e59aa32be4204484d2815c7d4a39311278f2ab12e3a9759aebbe6f019b18',
    CORE: '2648d2a1629ad1362598f8e47759fa15e5e3fa43ac558541fb4aa2567e5a47d9',
    S8REC: '1a2bb9cd059cc6d995446aa19fcea657caa26da6d61ccd073daed9babc647518',
    JX: '01a1347cf845e270358ff9b3de7537b6b510a303928bf8ad8296b164af98bbec',
    MX: 'd6df054024d73630b19b99c575443f2ddb95cd5bd7a9804c1370a7cf733024f0',
    R4OUT: '08954d9a9d525399d80b971f5bd526878e012e4f99791144c47391dc30cbc2d8',
    SIGG: 'b4a1dea6e7dddaad535c92bc491e0b8c2ffb23851c6b2f7fc2901605f9a45a12',
    DL1: 'd6afc761daf44d69c49926a6dfdc08d836698fcfcc76e3d6892d5ff6581424d5',
    HS2: 'b80760c5b79f121a0c39d3302308816064a482fb47c90341938d52f9420772a3',
    HS1: '90bbc6f2eaa35cee6b01a77c77995d35659028c9806d5e21278f1899a6c2e67e',
    TAUR: '24aaccc0890421d5ba533b42067b182a3a1f8014a85c9ad2c04a9e2f99218b95',
    NOTEB: '801099463aa4dff112c1bc2078c943f8aff15ecdcf9738aed1a7d9f2f03f0e53',
    ADD21: '89216d7961dc7df87110c96fd4776993b646270cc26e3e0e2ccc439046de2c7e',
    M2B: '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',
    MHATO: 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391',
    # pin dropped by G-v2: provenance-only document, not shipped (option C)
    # pin dropped by G-v2: provenance-only document, not shipped (option C)
    ADD10P: '0d322b4db7de4f0ce2676b903d10ef251431d057727e5ad6cc280a934cf5278a',
    HS3: 'a8862b08e8666d6118af850c36a7bee7393d13c89c38ee92726717d5054556f0',
    NOTEA: '799cf99e7386dbf04dabbcb8b8bb49bff20cd498d9b8913a7ca949743c9c9ce3',
    ADD3S: '94a2570e6db76809c9fab60c052805d9e378e2f5cca09cc74bcc4ecba90b298f',
    DL1OUT: '9a6b769495fed5336b85bf78b6a0f92c4a496b7badecdd8b6176dca6b39501ae',
    CFAO[4]: '08ed2f793df43fc9683bbb88b800e99aaf1396b66850127ced68ee0a24970bc2',
    CFAO[3]: '7477cec007ecfaae13e2881c3d67a51062dbf96c984d2caf80210a05e3b00b0b',
    UHM[4]: '9a4a403231fa2cab65216180cec1ad2be70e77150f64810499fffcb44d6cda4e',
    UHM[3]: 'e2f87746a2df47c605da3b3d643be547abd8e1216bfaabc9853900eea1e06901',
    UHW[4]: '7bf368f9c615af4aaf8bbf2e28edce04c234ea317b937ae4daf159a0764c0ffd',
    UHW[3]: 'b9e8ea638529b1033c574a4a710e78b547ac29ae168b5f6be02632dd2b1c4a2c',
    UHAT_CERT[4][0]: '38acdb92b926428f4d02c8d9b30ac8894c311c4215fe00337e01bf4df33a57dd',
    UHAT_CERT[4][1]: 'fe6885e53b70c6f83c1ff0a119c455ae54dcbeb44082e6cc0f7ead9dd3f70fee',
    UHAT_CERT[3][0]: 'fe85a9338d4f6e625e2b52fb00d75137e685680e239fb76ed6329b13867bd0bc',
    UHAT_CERT[3][1]: 'cc31b1031e36f5bf475423f15bfd33ad26923387ea1fc4fba86332e8dfb4b799',
    IFACE: '7ef0e195f95a2559558b254bd72ff54356e254b2899f2d6ce8fce00b58ab5706',
    ROWSF: 'c6822a6d3355b819813f78f561d16a745e016de757da968e78391c81fc7e48f1',
    ADD6: 'a0fbebdd6da733c7538c609a9af737438c1b199c69b6da505763beee16fe60ad',
    SPECS8: '3d4276002e175d5db717cbfed07deab5b9f779b791972b9b95b0a17bc851ffc1',
    CT2: '131996fe352e75e7cac874240791ed7b7162fa86761b4ae5920affdb19f38c58',
    R0T[4]: '4c9e65a0c2dfad5ddef7257059b22eba350191ca61fb2b6c8a220e821bfe6f89',
    R0T[3]: 'bffa65e7ca574dbdc4aa8331e87f9722c10caa201845a55d35b6511d42ef4f8f',
    TRK[4]: '66f77ae67f6ee9cf166f261dbe50c27be472feae3e7b22930e7d1d08997a6e5b',
    TRK[3]: '26b308600edd9d42e0b56011000c6654fbed32daea5272c9fc16e525a8b879fe',
    TRKO[4]: '896651137d5b984f49b0989ea39d1bb221b38f6912b0cdb015daf9bf2f68bd4a',
    TRKO[3]: '29c2073c88c8947da3bab6dedf53ee5fbf7ff46b789b16eba73c2a352d06d113',
    HJ[4]: 'fca8ed98ddee48c13214f15a91f069defbbc4edb092b62990fa10345ed64f3e5',
    HJ[3]: 'c3b8615c51bfa0e68a1bb3e66992c8f23365693b29daa35a147b58bd4c711acf',
    ESM[(4, 'D4', -1)]: 'b0dc8c1b33bba0936a5f0bad1837a6afe60ab91bcb1943ed2b0124703c5a3386',
    ESM[(4, 'D4', 0)]: 'dc7cd42dcb6123a676282154725d3f5452a1252d16be8f2ec0c9ecaad3d025b0',
    ESM[(4, 'D4M', -1)]: '428c8aa6565b4df5b9e9ce021e3c753711cb12538e586e85a72d873af94ad521',
    ESM[(4, 'D4M', 0)]: 'ed7e6b52cf8303e9ee85009ff34b0f5cab71e1ed0794693edb41baca065d23f5',
    ESM[(4, 'D3', -1)]: '955bd44f362b295521dab9e6530000f6403b27170614e55465fd70596f6fd2be',
    ESM[(4, 'D3', 0)]: 'a9f3ebc260df0a6ea6f638a4e51452071ab4e2bb9518e80f4718e95718c10c00',
    ESW_MOCK[4]: '9fff38b402f990977b1b062e813302f743858100bfb32e0fe7347b16b0e879a9',
    ESEMI_CERT[(4, 'D4', -1)]: '5573b0b6544c0cf294e8e85968a1d017b9cc963705aa8f138d9e794774200b87',
    ESEMI_CERT[(4, 'D4', 0)]: 'b15a4fcfdf685b394348c75b1a0304a0ff7c493b17e4f91aba120caa84fdd28d',
    ESEMI_CERT[(4, 'D4M', -1)]: '289f4c2be4e09664ab55594dc2a66d827bff073d7a9d8db5fa54325488b813b2',
    ESEMI_CERT[(4, 'D4M', 0)]: '0a2371f7ed88b9c548eb7131fccd84425537ed463753549faf8298c2de5b3870',
    ESEMI_CERT[(4, 'D3', -1)]: '58c119f9087a7c08d8804aca19bf2b675a96689eb9ad542e9b8db697a2212731',
    ESEMI_CERT[(4, 'D3', 0)]: '6be2a6f5518b71b151f95d31f798095a348045ece715aced9ebe0ba7df54e1a2',
    ESEMI_CERT[(3, 'D4', -1)]: '08a02e2a4dc7618eb975eb1feb30231787b90c0b0f658ecd6bfa16bcf5801151',
    ESEMI_CERT[(3, 'D4', 0)]: 'e5088576fc08ef4b6ec262bee177d122e220cb6a7a960b8df98f97530c5d28d4',
    ESEMI_CERT[(3, 'D4M', -1)]: 'bc33033c45767b4c0231f4f7b8a2993f9a156a70a2bf1f2c7b109ca1039c9472',
    ESEMI_CERT[(3, 'D4M', 0)]: 'b821482325ee54eb4ef2c406801c2111c56302c0bf62293ab995a511c96a4a1d',
    ESEMI_CERT[(3, 'D3', -1)]: 'b615dfdf5f8c97e96d73555c3dc7ddabeb54b79b66ea87d6f89dd4b73e30a424',
    ESEMI_CERT[(3, 'D3', 0)]: 'b532d309815c6d4b1d478c9ec0f9c7e613ad08137b3c13b5dee7e4239daaf143',
    ESW_CERT[4]: 'd033225cdb6c207a8aa9860fd798de6c4ccd2e7cc78d7c8e1ac1f64dac6cd65d',
    ESW_CERT[3]: '911de041dfbfee4a1c4843b3e525fc2d38a1a81a78a185e8c569c5fd3b8ff72c',
    TX: 'f515bc38a8fe4094a406a3a6b5fcf2deb4b8d863d8aae79c7e3383d93cfd6c03',
    TRBO[4]: '9d3e8f622c6bf01ec26c75dfc414be730dbbfb87761af78b40cca2e75f2db9a2',
    TRBO[3]: 'ff2d93d01bdf2303e51d8d6f0499fd359a872db6f13132fc7d9f95c28aac08fe',
    QEF: '2f3ea26f1cf0140b990ffe3d6c9dcfa312c7df5573c25de04d98d7102e99d63b',
    QEFO: 'abf53f2f49be3c28ff7d1ab170b98e9955959616d48aefe15edaebe371dc70ad',
}
_bad = ['%s %s' % (os.path.relpath(p, CODEDIR), sha_file(p)[:8]) for p in sorted(PINS) if sha_file(p) != PINS[p]]
out('C-HASH %s (%d files)%s' % ('PASS' if not _bad else 'FAIL', len(PINS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)

NS = GRIDN or (CHUNK[0] if CHUNK else 4)
STRAY = OUTD + '/out_kt_s8_cert_v1_14_3_cert_c%d_0000_0001_r%d.out'
_free = [k for k in range(50, 100) if not os.path.exists(STRAY % (NS, k))]
_pool = 'r50..r99'
if not _free:   # v1_3_5_5: the fallback pool r1..r49 for this chunk name, which no S8 run of pk11 uses
    _free = [k for k in range(1, 50) if not os.path.exists(STRAY % (NS, k))]
    _pool = 'r1..r49 (the fallback pool)'
if not _free:
    out('VERDICT INVALID (no free stray tag r1..r99 for the cert module\'s import)')
    sys.exit(2)
out('IMPORT: kt_s8_cert_v1_14_3 in its cert namespace, chunk c%d_0000_0001 with tag r%d (the first free of %s; a stray, not counted '
    'by S8\'s final)' % (NS, _free[0], _pool))
sys.argv = [CERT, 'cert', 'chunk', str(LIM), str(NS), '0', '1', 'r%d' % _free[0]]
_spec = importlib.util.spec_from_file_location('kt_s8_cert_v1_14_3', CERT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)
CM = mod.CM
arb = mod.arb
ZERO, ONE = CM.ZERO, CM.ONE
fails, nofire = [], []
NP = mod.NPIECES
WX = {'D3': 3, 'D4': 2, 'D4M': 2}
KIND = {'D3': 'D3B', 'D4': 'D4A', 'D4M': 'D4MA'}
REL_FORM = Fraction(1, 10 ** 9)
R_TRUNC = Fraction(1, 10 ** 20)
PENDING_REC = []


class Refused(Exception):
    """a reader or gate refusing its input (the plants expect it)."""


def gate(name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


def plant(name, fired):
    if not fired:
        nofire.append(name)
    return 'FIRES' if fired else 'DOES NOT FIRE'


def refuses(fn, *a, tag=None, **k):
    """True when fn(*a, **k) raises Refused whose text names the gate tag (any Refused when tag is None); other exceptions propagate."""
    try:
        fn(*a, **k)
    except Refused as ex:
        return tag is None or tag in str(ex)
    return False


def F(x):
    return Fraction(x)


def B(x):
    return CM.fr(Fraction(x))


def fl(x):
    return float(x.mid()) if isinstance(x, arb) else float(x)


def upf(x):
    return mod.up_frac(x)


def lof(x):
    m, e = x.lower().man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def bmin(a, b):
    return a if a.upper() <= b.upper() else b


def kv(path):
    d = {}
    for ln in open(path).read().split('\n'):
        if ln and not ln.startswith('#') and ' = ' in ln:
            k, v = ln.split(' = ', 1)
            d.setdefault(k.strip(), v.strip())
    return d


def kv_strict(path):
    """the u-hat reader: a repeated key is refused."""
    d = {}
    for ln in open(path).read().split('\n'):
        if ln and not ln.startswith('#') and ' = ' in ln:
            k, v = ln.split(' = ', 1)
            if k.strip() in d:
                raise Refused('C-UHAT-SRC: key %s repeated' % k.strip())
            d[k.strip()] = v.strip()
    return d


def tsv(path):
    rows, hdr = [], None
    for ln in open(path).read().split('\n'):
        if not ln or ln.startswith('#'):
            continue
        f = ln.split('\t')
        if hdr is None:
            hdr = f
            continue
        rows.append(dict(zip(hdr, f)))
    return rows


def export_rows(path):
    res = {}
    for ln in open(path).read().split('\n'):
        mm = re.match(r'^N([34])_(D3|D4M|D4)_P(\d{4}) = (.*)$', ln)
        if mm:
            res[(int(mm.group(1)), mm.group(2), int(mm.group(3)))] = mm.group(4).split()
    return res


def rule_v2(lines, rec_name=None, rec_sha=None, where='RULE-V2'):
    """rule V2 (ADD11 sect. 2): the VERDICT lines are exactly [VERDICT VALID]; with rec_name, a line 'RECORD <rec_name> sha256 <rec_sha>'."""
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise Refused('%s: the VERDICT lines are not exactly [VERDICT VALID]' % where)
    if rec_name is not None and ('RECORD %s sha256 %s' % (rec_name, rec_sha)) not in lines:
        raise Refused('%s: no RECORD line names %s with its full sha256' % (where, rec_name))


def rule_v2_strict(lines, rec_name, rec_sha, where='RULE-V2'):
    """v1_3_2: rule V2, strict (interface v1_4 sect. 5): exactly one VERDICT line, 'VERDICT VALID', as the last
    non-empty line, and exactly one RECORD line naming rec_name, equal to 'RECORD <rec_name> sha256 <rec_sha>'."""
    ne = [ln for ln in lines if ln.strip()]
    if [ln for ln in ne if ln.startswith('VERDICT')] != ['VERDICT VALID'] or ne[-1] != 'VERDICT VALID':
        raise Refused('%s: not exactly one VERDICT line, "VERDICT VALID", as the last line' % where)
    named = [ln for ln in ne if ln.startswith('RECORD ') and len(ln.split()) > 1 and ln.split()[1] == rec_name]
    if named != ['RECORD %s sha256 %s' % (rec_name, rec_sha)]:
        raise Refused('%s: not exactly one line "RECORD %s sha256 <its full sha256>"' % (where, rec_name))


def rows_check(N, rlist, rcount):
    """v1_3_2, C-ROWS: the engine's own D3 route-0 rows (types B3, TB, TD) at N equal ROWS_N<N> as a set, and COUNT_N<N>
    is their number."""
    own = [rowid(r) for r in G['ROWS'][N] if r['fam'] == 'D3' and r['typ'] in ('B3', 'TB', 'TD')]
    if sorted(own) != sorted(rlist) or len(set(rlist)) != len(rlist) or str(len(own)) != str(rcount):
        raise Refused('C-ROWS: N%d has %d own route-0 rows against %d listed (COUNT %s)' % (N, len(own), len(rlist), rcount))


def stagea_ok(fl, nl):
    """v1_3_2, C-S8-STAGEA: run_A's stage-A failing and no-fire lists must come back empty."""
    if fl or nl:
        raise Refused('C-S8-STAGEA: run_A reports failing %s, not firing %s' % (sorted(set(fl)), sorted(set(nl))))


# ---- the row's t = 0 harmonic Cov (kt_s8hj_v1's strip formula) in balls
def vpair(e):
    c, b = e
    return {'TM': (3 * c, 3 * c + 1), 'MB': (3 * c + 1, 3 * c + 2), 'HT': (3 * c, 3 * c + 3), 'HM': (3 * c + 1, 3 * c + 4),
            'HB': (3 * c + 2, 3 * c + 5)}[b]


def strip_T_ball(n, e, f):
    pi = arb.pi()
    s3, s2, s6 = arb(3).sqrt(), arb(2).sqrt(), arb(6).sqrt()
    mus = [(ZERO, [ONE / s3] * 3), (ONE, [ONE / s2, ZERO, -ONE / s2]), (arb(3), [ONE / s6, -2 / s6, ONE / s6])]
    lams = []
    for m in range(n):
        nrm = (ONE / arb(n)).sqrt() if m == 0 else (arb(2) / arb(n)).sqrt()
        lams.append((2 - 2 * (pi * m / n).cos(), [nrm * (pi * m * (2 * j + 1) / (2 * n)).cos() for j in range(n)]))

    def amp(b, k, m):
        u, v = vpair(b)
        ph, ps = mus[k][1], lams[m][1]
        return ph[u % 3] * ps[u // 3] - ph[v % 3] * ps[v // 3]
    tot = ZERO
    for k in range(3):
        for m in range(n):
            if (k, m) != (0, 0):
                tot = tot + amp(e, k, m) * amp(f, k, m) / (mus[k][0] + lams[m][0])
    return tot


def bonds(fam, c0):
    if fam == 'D3':
        return (c0, 'HT'), (c0 + 1, 'HB')
    if fam == 'D4':
        return (c0, 'HT'), (c0, 'MB')
    return (c0, 'HT'), (c0 + 1, 'MB')


def harm_ball(N, fam, dL, dR):
    """v1_3: the 64-column 'far' and 'inf' rows carry the truncation radius R_TRUNC. V1_3_2: R_TRUNC's source is the review
    1920fa90 (1), an image-sum bound |T_64 - T_inf| <= 8.3e-48; for 'far' (d_R >= 7) the 64-column value is a representative that no
    certified bound reads in cert mode (1920fa90 (2))."""
    n = 64 if dR in ('inf', 'far') else dL + int(dR) + WX[fam] + 2
    e_, f_ = bonds(fam, dL + 1)
    T_ = strip_T_ball(n, e_, f_)
    c = arb(N - 1) * T_ * T_ / 2
    return c + CM.pm(R_TRUNC) if dR in ('inf', 'far') else c


TVSRC_OK = {ADD6}   # v1_3_2: interface v1_4 names ADD6 as T_v's source
TWSRC_OK = set()
DEC_RE = re.compile(r'[-+]?[0-9]+(\.[0-9]*)?([eE][-+]?[0-9]+)?')   # v1_3_2: interface v1_4 sect. 1's dec
R0F = ('route', 'formula', 'q_hat_hi', 'beta_hat_s', 'm_hat_s_hi', 'm_hat_s_source', 'xu_hi', 'T_s', 'T_U4', 'q_b_hi')
L0F = ('route', 'L0_hi', 'q_hat_hi', 'm_hat_s_hi', 'beta_hat', 'xu_hi', 'xsu_hi', 'xsu_source', 'T_U4', 'q_hi')
BPF = ('basis', 'v_hat_raw.0', 'v_hat_raw.1', 'v_hat_raw.2', 'v_hat_raw.3', 'T_v', 'T_v_source')
HDRK = ('RECORD', 'FORMAT', 'EXPORT_STATUS', 'MOCK', 'VERDICT_OF_WRITER', 'N', 'INTERFACE', 'ROWS', 'J_RANGE', 'J_UNIFORMITY',
        'centres.source', 'centres.pieces', 'M2B', 'CODE', 'LIB', 'WORLD_U_HAT', 'WORLD_TRUE_U', 'END')
CRUDE11 = {3: True, 4: False}   # v1_3_2: the (1,1) rows take the crude reading at N3; N4 stays wait-W
FAR_EXP = 7                     # v1_3_2: 'far' is d_R >= 7, level >= 6; S8's tail at distance d is R_w rho1^d (C-FAR-CITE)
NEG_MARKER = -Fraction(10) ** 60   # v1_3_2: sdiv's marker for a quotient unbounded below


def uhat_path(N):
    return UHM[N] if MODE == 'mock' else UHAT_CERT[N][0]


def uhat_out(N):
    """v1_3_2: the writer's run output that rule V2 binds to the record (one per N under interface v1_4)."""
    return UHW[N] if MODE == 'mock' else UHAT_CERT[N][1]


def rowid(row):
    """v1_3_2 (interface v1_4 sect. 3): the row name rname written as <fam>_<dL>_<dR>, with '-' as 'm'."""
    return '%s_%s_%s' % (row['fam'], str(row['dL']).replace('-', 'm'), row['dR'])


def m2b_vals(N, M2=None):
    """v1_3_2: eps_r = N<N>_EPS_R_300 and s = N<N>_S_300 from the pinned M2B
    record, each a decimal in [0, 1)."""
    M2 = G['M2B'] if M2 is None else M2
    vals = []
    for k in ('N%d_EPS_R_300' % N, 'N%d_S_300' % N):
        v = M2.get(k)
        if v is None or not dec_ok(v) or not (0 <= F(v) < 1):
            raise Refused('C-M2B-RANGE: %s = %r is not a decimal in [0, 1)' % (k, v))
        vals.append(F(v))
    return vals[0], vals[1]


def uhat_check(d, N, lines):
    """v1_3_2 (interface v1_4 sect. 2-5): the header's tags and exact pins, the whitelist of keys, the
    WORLD lists and END as the last line. Raises Refused naming the failing check."""
    if d.get('RECORD') != 'UHAT_ASM_v1' or d.get('END') != 'UHAT_ASM_v1' or d.get('FORMAT') != 'S4U_KV_v1':
        raise Refused('C-UHAT-TAGS: RECORD/END/FORMAT')
    ne = [ln for ln in lines if ln.strip()]
    if not ne or ne[-1] != 'END = UHAT_ASM_v1':
        raise Refused('C-UHAT-TAGS: END is not the last line')
    want = ('MOCK', 'TRUE') if MODE == 'mock' else ('CERTIFIED', 'FALSE')
    if (d.get('EXPORT_STATUS'), d.get('MOCK')) != want:
        raise Refused('C-UHAT-TAGS: EXPORT_STATUS %r with MOCK %r in %s mode' % (d.get('EXPORT_STATUS'), d.get('MOCK'), MODE))
    if d.get('VERDICT_OF_WRITER') != 'VALID' or d.get('N') != str(N):
        raise Refused('C-UHAT-TAGS: VERDICT_OF_WRITER %r, N %r' % (d.get('VERDICT_OF_WRITER'), d.get('N')))
    if not str(d.get('J_UNIFORMITY', '')).startswith('UNIFORM-J'):
        raise Refused('C-UHAT-TAGS: J_UNIFORMITY')
    for k, p in (('INTERFACE', IFACE), ('ROWS', ROWSF), ('M2B', M2B), ('centres.source', MX)):
        if d.get(k) != os.path.relpath(p, CODEDIR) + ':' + PINS[p]:
            raise Refused('C-UHAT-PIN: %s %r is not the reader\'s pin' % (k, str(d.get(k))[-80:]))
    if d.get('centres.pieces') != 'P%04d..P%04d' % (G['RSTART'][N], NP - 1):
        raise Refused('C-UHAT-PIN: centres.pieces %r is not P%04d..P%04d' % (d.get('centres.pieces'), G['RSTART'][N], NP - 1))
    if d.get('J_RANGE') != G['JR'][N]:
        raise Refused('C-UHAT-PIN: J_RANGE %r is not %r' % (d.get('J_RANGE'), G['JR'][N]))
    for k in ('CODE', 'LIB'):
        m = re.fullmatch(r'([A-Za-z0-9_./-]+):([0-9a-f]{64})', str(d.get(k, '')))
        if m is None or m.group(1).startswith('/') or '..' in m.group(1).split('/'):   # v1_3_4: no '..' segment
            raise Refused('C-UHAT-PIN: %s %r is not a src under code/ without a .. segment' % (k, str(d.get(k))[-80:]))
        if sha_file(os.path.join(CODEDIR, m.group(1))) != m.group(2):
            raise Refused('C-UHAT-PIN: %s %r is not a src that hashes to its file' % (k, str(d.get(k))[-80:]))
    rids = G['ROWSL']['ROWS_N%d' % N].split()
    allowed = set(HDRK) | set('route0b_hat.%s.%s' % (r, f) for r in rids for f in R0F) | \
        set('l0_hat.%s.%s' % (w, f) for w in ('D4L0', 'D4ML0') for f in L0F) | set('bprime_hat.FA.' + f for f in BPF)
    extra = sorted(k for k in d if k not in allowed and not k.startswith('info.'))
    if extra:
        raise Refused('C-UHAT-KEYS: keys outside interface v1_4 (a wmat_hat key included): %s' % extra[:4])
    miss = sorted(k for k in HDRK if k not in d)
    if miss:
        raise Refused('C-UHAT-KEYS: header keys missing: %s' % miss)
    hat = set('route0b_hat.%s.%s' % (r, f) for r in rids for f in ('q_hat_hi', 'm_hat_s_hi', 'xu_hi')) | \
        set('l0_hat.%s.%s' % (w, f) for w in ('D4L0', 'D4ML0') for f in ('L0_hi', 'q_hat_hi', 'm_hat_s_hi', 'xu_hi', 'xsu_hi')) | \
        set('bprime_hat.FA.v_hat_raw.%d' % j for j in range(4))
    tru = set('route0b_hat.%s.q_b_hi' % r for r in rids) | set('l0_hat.%s.q_hi' % w for w in ('D4L0', 'D4ML0'))
    wu, wt = d.get('WORLD_U_HAT', '').split(), d.get('WORLD_TRUE_U', '').split()
    if set(wu) != hat or len(wu) != len(hat) or set(wt) != tru or len(wt) != len(tru):
        raise Refused('C-WORLD-U: the WORLD lists are not exactly the hat and true keys of interface v1_4 sect. 3')


def uhat_src(d, N):
    """C-UHAT-SRC (v1_3_2): uhat_check on the record and its lines; the problems found (none when it passes)."""
    try:
        uhat_check(d, N, G['UHL'][N])
    except Refused as ex:
        return [str(ex)]
    return []


def jrange(d):
    """J_RANGE 'J_lo inf' (or 'J_lo J_hi') -> (J_lo, J_hi or None); v1_3_2 (the review hardening): a malformed value is refused."""
    f_ = str(d.get('J_RANGE', '')).split()
    if len(f_) != 2 or not dec_ok(f_[0]) or not (f_[1] == 'inf' or dec_ok(f_[1])):
        raise Refused('C-UD3-PIECE: J_RANGE %r is not "J_lo J_hi" or "J_lo inf"' % d.get('J_RANGE'))
    return F(f_[0]), (None if f_[1] == 'inf' else F(f_[1]))


def piece_in_range(d, jlo, jhi):
    """C-UD3-PIECE: the record's J range holds the piece. v1_3_2: J_RANGE's J_lo is the first piece's J_lo as written in the means
    export (interface v1_4), so the lower ends compare as the same binary64 value."""
    a, b = jrange(d)
    if a < 300 or float(jlo) < float(a) or (b is not None and (jhi == float('inf') or F(jhi) > b)):
        raise Refused('C-UD3-PIECE: the record\'s J range %s does not hold the piece [%s, %s]' % (d.get('J_RANGE'), jlo, jhi))


def centres_read(d, first, last):
    """C-CENTRES (v1_3_2 with interface v1_4): centres.source is exactly the engine's pinned means export, and
    centres.pieces is exactly P<first>..P<last>, the engine's pieces at the record's N."""
    src = d.get('centres.source', '')
    if src != os.path.relpath(MX, CODEDIR) + ':' + PINS[MX]:
        raise Refused('C-CENTRES: centres.source %r is not the pinned means export' % src[-90:])
    if d.get('centres.pieces') != 'P%04d..P%04d' % (first, last):
        raise Refused('C-CENTRES: centres.pieces %r is not P%04d..P%04d' % (d.get('centres.pieces'), first, last))


def world(d, key, w):
    lst = d.get('WORLD_TRUE_U' if w == 'true' else 'WORLD_U_HAT', '').split()
    if key not in lst:
        raise Refused('C-WORLD-U: %s is not listed as %s' % (key, 'true-u' if w == 'true' else 'u-hat'))


def dec_ok(s):
    """v1_3_2: interface v1_4 sect. 1's dec (DEC_RE), exact as written."""
    return isinstance(s, str) and DEC_RE.fullmatch(s) is not None


def need(d, key, where):
    v = d.get(key)
    if v is None or not dec_ok(v):
        raise Refused('%s: %s missing or not a finite decimal (%r)' % (where, key, v))
    return F(v)


def need_up(d, key, where):
    """v1_3_2: an up value of interface v1_4 sect. 3 must be >= 0."""
    v = need(d, key, where)
    if v < 0:
        raise Refused('%s: %s is negative (%s)' % (where, key, d.get(key)))
    return v


def need_pos(d, key, where):
    """v1_3_2: T_s and T_U4 must be > 0."""
    v = need(d, key, where)
    if not (v > 0):
        raise Refused('%s: %s must be > 0 (%s)' % (where, key, d.get(key)))
    return v


def nb1_h(qhat, eps, mhs, T, s):
    return ONE / (ONE - B(s) * B(s)).sqrt() * qhat + B(eps) * B(mhs) / (ONE - B(eps)) + B(T)


def l0_read(d, w, s, eps, round_down=False):
    """C-L0-HI and C-L0-POST (v1_3_2, interface v1_4 sect. 3): the window's parts, with eps_r and s from M2B; q_hi is recomputed by N-B1's
    route H and checked two-sided at 1e-9, and q_use = max(recorded, recomputed)."""
    pre = 'l0_hat.%s.' % w
    L0s = d.get(pre + 'L0_hi')
    if L0s is None or not dec_ok(L0s):
        raise Refused('C-L0-HI: %sL0_hi %r is not a finite decimal' % (pre, L0s))
    L0 = F(L0s)
    if L0 < 0:
        raise Refused('C-L0-HI: %sL0_hi %s is negative' % (pre, L0s))
    sq = B(L0).sqrt()
    qh = lof(sq) if round_down else upf(sq)
    if qh * qh < L0:
        raise Refused('C-L0-HI: q_hi^2 < L0_hi exactly (%s)' % pre)
    if d.get(pre + 'route') != 'H':
        raise Refused('C-L0-POST: %sroute is %r, not H' % (pre, d.get(pre + 'route')))
    if d.get(pre + 'xsu_source') not in ('adjoint_same_c', 'beta-hat_fallback'):
        raise Refused('C-L0-POST: %sxsu_source %r is not a tag of the table' % (pre, d.get(pre + 'xsu_source')))
    qhr = need_up(d, pre + 'q_hat_hi', 'C-L0-POST')
    if qhr < lof(sq):
        raise Refused('C-L0-POST: %sq_hat_hi %s is below L0_hi^(1/2)' % (pre, d.get(pre + 'q_hat_hi')))
    for k in ('beta_hat', 'xu_hi', 'xsu_hi'):
        need_up(d, pre + k, 'C-L0-POST')
    T = need_pos(d, pre + 'T_U4', 'C-L0-POST')
    mhs = need_up(d, pre + 'm_hat_s_hi', 'C-L0-POST')
    qrec = need_up(d, pre + 'q_hi', 'C-L0-POST')
    for k in ('L0_hi', 'q_hat_hi', 'm_hat_s_hi', 'xu_hi', 'xsu_hi'):
        world(d, pre + k, 'hat')
    world(d, pre + 'q_hi', 'true')
    qu = max(qh, qhr)
    qout = upf(nb1_h(B(qu), eps, mhs, T, s))
    if abs(qrec - qout) > REL_FORM * qout:
        raise Refused('C-L0-POST: q_hi %.12g against the recomputed %.12g (relative %.2e > 1e-9)' % (
            float(qrec), float(qout), float(abs(qrec - qout) / qout)))
    return {'L0': L0, 'qh': qu, 'T': T, 'mhs': mhs, 'eps': eps, 'qrec': qrec, 'qout': qout, 'quse': max(qrec, qout)}


def r0_read(d, rid, s, eps):
    """C-UD3-POST (v1_3_2, interface v1_4 sect. 3): the row's own block route0b_hat.<rid>: route P with ROUTE_P_UHAT_v1 and T_s only, or
    route H with ROUTE_H_NB1 and T_U4 only; q_b_hi recomputed by the formula (route H with eps_r and s from M2B), checked two-sided at
    1e-9; U_use = max(recorded, recomputed)."""
    pre = 'route0b_hat.%s.' % rid
    if d.get('RECORD') != 'UHAT_ASM_v1':
        raise Refused('C-R0ASM / PLANT-SAME-WORLD: the route-0 value does not come from a UHAT_ASM_v1 record')
    route, form = d.get(pre + 'route'), d.get(pre + 'formula')
    if (route, form) not in (('P', 'ROUTE_P_UHAT_v1'), ('H', 'ROUTE_H_NB1')):
        raise Refused('C-UD3-POST: %s has route %r with formula %r' % (rid, route, form))
    if d.get(pre + 'm_hat_s_source') not in ('beta-hat_fallback', 'certified_mean'):
        raise Refused('C-UD3-POST: %s m_hat_s_source %r is not a tag of the table' % (rid, d.get(pre + 'm_hat_s_source')))
    qh = need_up(d, pre + 'q_hat_hi', 'C-UD3-POST')
    for k in ('beta_hat_s', 'xu_hi'):
        need_up(d, pre + k, 'C-UD3-POST')
    mhs = need_up(d, pre + 'm_hat_s_hi', 'C-UD3-POST')
    rec = need_up(d, pre + 'q_b_hi', 'C-UD3-POST')
    for k in ('q_hat_hi', 'm_hat_s_hi', 'xu_hi'):
        world(d, pre + k, 'hat')
    world(d, pre + 'q_b_hi', 'true')
    if route == 'P':
        if (pre + 'T_U4') in d:
            raise Refused('C-UD3-POST: route P row %s carries T_U4' % rid)
        uo = upf(B(qh) + B(need_pos(d, pre + 'T_s', 'C-UD3-POST')))
    else:
        if (pre + 'T_s') in d:
            raise Refused('C-UD3-POST: route H row %s carries T_s' % rid)
        uo = upf(nb1_h(B(qh), eps, mhs, need_pos(d, pre + 'T_U4', 'C-UD3-POST'), s))
    if abs(rec - uo) > REL_FORM * uo:
        raise Refused('C-UD3-POST: %s q_b_hi %.12g against the recomputed %.12g (relative %.2e > 1e-9)' % (
            rid, float(rec), float(uo), float(abs(rec - uo) / uo)))
    return {'qh': qh, 'rec': rec, 'out': uo, 'use': max(rec, uo), 'route': route}


def tsrc_ok(line, allowed):
    if not line or ':' not in line:
        raise Refused('C-T-SRC: no source line')
    p, sh = line.rsplit(':', 1)
    ap = os.path.join(CODEDIR, p)
    if ap not in allowed or PINS.get(ap) != sh or sha_file(ap) != sh:
        raise Refused('C-T-SRC: the source %s is not a pinned file with that sha256' % line[-80:])


def bp_read(d, K):
    """C-BASIS-RAW and C-TV-SRC (v1_3_2, interface v1_4 sect. 3): basis raw, v_hat_raw.<j> (j = 0..K) as balls "lo hi" with lo <= hi,
    T_v >= 0 with its source pinned (ADD6)."""
    if d.get('bprime_hat.FA.basis') != 'raw':
        raise Refused('C-BASIS-RAW: bprime_hat.FA.basis is %r, not raw' % d.get('bprime_hat.FA.basis'))
    raw = []
    for j in range(K + 1):
        key = 'bprime_hat.FA.v_hat_raw.%d' % j
        f_ = (d.get(key) or '').split()
        if len(f_) != 2 or not (dec_ok(f_[0]) and dec_ok(f_[1])) or F(f_[0]) > F(f_[1]):
            raise Refused('C-BASIS-RAW: %s is not a ball "lo hi"' % key)
        world(d, key, 'hat')
        raw.append(CM.span(F(f_[0]), F(f_[1])))
    Tv = need_up(d, 'bprime_hat.FA.T_v', 'C-TV-SRC')
    tsrc_ok(d.get('bprime_hat.FA.T_v_source'), TVSRC_OK)
    return raw, Tv


def w_read(d, fam):
    """v1_3_2 (interface v1_4 sect. 3): the table defines no wmat_hat key; any such key is refused, and a missing one is
    WAIT-W (None)."""
    if any(k.startswith('wmat_hat.') for k in d):
        raise Refused('C-TW-SRC: a wmat_hat key is outside interface v1_4')
    return None


def centre_coef(src):
    if src != 'S8:g_j0/g00':
        raise Refused('C-CENTRE-R65: centring by %s, not S8\'s g_j0/g00' % src)


def sigg_cert(text, N):
    """v1_3: kappa's upper end from the C-NA line (kappa_max, dec_hi) and Phi_eps's from the PHI-EPS line; C-KAPPA-GE1 (a lower
    end) is never read."""
    mk = re.search(r'^C-NA N=%d: .* with kappa_max (\S+); ' % N, text, re.M)
    mp = re.search(r'^PHI-EPS N=%d .*Phi_eps <= (\S+),' % N, text, re.M)
    if mk is None or mp is None:
        raise Refused('C-SIGG-SRC: no C-NA kappa_max or PHI-EPS line for N=%d' % N)
    return F(mk.group(1)), F(mp.group(1))


def mhat_src(text, m2b_sha):
    """v1_3_5_4, C-MHAT-SRC: m-hat >= 1, on which tau_1's step
    c_K / mu-hat <= kappa rests, from the M2(b) assembly output that binds the pinned M2B record (pk02's out_m2b_asm_v1.out, as
    v1_37_1 reads it with PLANT-TP-MHAT-SRC): its VERDICT lines exactly [VERDICT VALID], its RECORD lines exactly one, naming
    M2B_KV_v1.txt with its full sha256, and per N exactly one passing C-MHAT line whose m1..m3 are decimals >= 0, so that
    m-hat = 1 + m1 t + m2 t^2 + m3 t^3 >= 1 for t >= 0 (R6a l.43). Returns {N: (m1, m2, m3)}."""
    lines = text.split('\n')
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise Refused('C-MHAT-SRC: the M2B asm output\'s VERDICT lines are not exactly [VERDICT VALID]')
    if [ln for ln in lines if ln.startswith('RECORD ')] != ['RECORD M2B_KV_v1.txt %s' % m2b_sha]:
        raise Refused('C-MHAT-SRC: the M2B asm output does not bind M2B_KV_v1.txt by its full sha256')
    res = {}
    for N in (4, 3):
        hit = [ln for ln in lines if ln.startswith('C-MHAT N=%d: m1..m3 = [' % N) and ln.endswith('-> PASS')]
        if len(hit) != 1:
            raise Refused('C-MHAT-SRC: the M2B asm output has no single passing C-MHAT line for N=%d' % N)
        try:
            m = tuple(Fraction(x.strip()) for x in hit[0].split('[', 1)[1].split(']', 1)[0].split(','))
        except (ValueError, ZeroDivisionError):
            raise Refused('C-MHAT-SRC: the C-MHAT line for N=%d does not parse' % N)
        if len(m) != 3 or min(m) < 0:
            raise Refused('C-MHAT-SRC: the C-MHAT line for N=%d does not hold three nonnegative m' % N)
        res[N] = m
    return res


def cn_full(kap, phi, epsr):
    """v1_3_5_4 (pk15 NOTE_J3_TAIL_ONESIDED_G1_v1 ed0ae46c, Claim T,
    01:52Z): the ball of tau_1's constant C_N = u kappa^(1/2) (1 + kappa) Phi_eps^(1/2), u = 1/(1 - eps_r(300)), from kappa_max and
    Phi_eps (upper ends from the pinned v1_37_1 cert output) and M2B's N<N>_EPS_R_300, which holds for every J >= 300."""
    if not (kap >= 0 and phi >= 0 and 0 <= epsr < 1):
        raise Refused('C-TAU1: kappa %s, Phi_eps %s or eps_r %s out of range' % (kap, phi, epsr))
    return (ONE / (ONE - B(epsr))) * B(kap).sqrt() * (ONE + B(kap)) * B(phi).sqrt()


def cn_ball(kap, phi, epsr):
    """v1_3_5_4: C_N rounded outward, the upper end of cn_full's ball as an exact Fraction."""
    return upf(cn_full(kap, phi, epsr))


def dl1_vals(DL, N, fam, kind):
    if kind != KIND[fam]:
        raise Refused('C-DLM1-SRC: a %s row read with %s\'s keys' % (fam, kind))
    km = DL.get('KEYMAP_%s' % kind, '')
    keys = dict((x.split()[0], x.split()[1]) for x in km.split(' ; ') if len(x.split()) >= 2)
    if set(keys) != {'E', 'Q', 'Q1'}:
        raise Refused('C-DLM1-SRC: KEYMAP_%s %r' % (kind, km))
    return tuple(F(DL[keys[k].replace('N*', 'N%d' % N)]) for k in ('E', 'Q', 'Q1'))


def q_hi_power(kind, power):
    if kind == 'D4MA' and power != 0:
        raise Refused('C-LAMBDA-ONCE: Q_HI_D4MA read at power %s' % power)


def v3_power(V3, kind, power):
    if F(V3.get('LAMBDA_POWER_%s' % kind, '0')) != F(power):
        raise Refused('v3: %s QA_CRUDE read at power %s, not LAMBDA_POWER %s' % (kind, power, V3.get('LAMBDA_POWER_%s' % kind)))


def q1_plane(fam, level):
    if level != WX[fam] - 2:
        raise Refused('C-Q1-PLANE: %s reads l(%d), not l(%d)' % (fam, level, WX[fam] - 2))


def same_ball(a, b):
    return a.mid() == b.mid() and a.rad() == b.rad()


def esemi_form(N, fam, dR, form):
    beta = (N, fam, dR) == (3, 'D3', '1')
    if form != ('beta' if beta else 'alpha'):
        raise Refused('C-ESEMI-FORM: N%d %s (0,%s) in form %s' % (N, fam, dR, form))


def den_pos(den):
    if not (den.lower() > 0):
        raise Refused('C-DEN-POS: 1 - Q1 rn1_R has lower end %s' % den.lower())


def esemi_transfer(x):
    """the u-hat-to-true step for E_semi: the identity, kept as a replaceable function. v1_3_1: the rule 2414bd75 sect. 1 is no
    transfer (R's sigma_s and sigma_n, and sigma_g for the single trick, carry the step from u-hat to the true vacuum)."""
    return x


ESMONO = ('1', 'e', 'f', 'ef')   # v1_3_4: the E_main monomials; e is the row's first bond factor (xi_t), f its second (SEND_029)
ESNAME = {'D4': {'1': 'E000', 'e': 'E100', 'f': 'E001', 'ef': 'E101'}, 'D4M': {'1': 'S0000', 'e': 'S1000', 'f': 'S0100', 'ef': 'S1100'},
          'D3': {'1': '1', 'e': 'xi_t', 'f': 'xi_bb', 'ef': 'xi_t xi_bb'}}
ESKEYS = sorted('ES,%s,%d' % (mo, k) for mo in ESMONO for k in range(4))
ESTWIN = {'V9': 'f', 'V12': 'h'}   # v1_3_4: S8's own entry of the shape's W1,k (E3's f,k on V9, the D16 H record's h,k on V12)
ESRUN = (CODEDIR + '/pk04', 'm3_run_es_v1_3', '1deb61e1dc6a74d383b5b4e7ee648444a76abd6ca732ffb68be07dd1f23e471f',   # v1_3_5_1: the MOCK records' runner, moved to v1_3
         {'m3_run_es_v1_3_ent.py': 'd54c8be0c33c34a63dfd1f5e17b017b94b9cbd086634b8a4c1cfaebf9c81fbc7',
          'm3_run_es_v1_3_asm.py': 'e5f675a0fcc32569a845010e767b29165d56bb11b33aa802bc59fe52eeb4f38f'})
ESRUN_CERT = (CODEDIR + '/pk04', 'm3_run_es_v1_3', '1deb61e1dc6a74d383b5b4e7ee648444a76abd6ca732ffb68be07dd1f23e471f',   # v1_3_5_2: the reviewed production runner
              {'m3_run_es_v1_3_ent.py': 'd54c8be0c33c34a63dfd1f5e17b017b94b9cbd086634b8a4c1cfaebf9c81fbc7',   #
               'm3_run_es_v1_3_asm.py': 'e5f675a0fcc32569a845010e767b29165d56bb11b33aa802bc59fe52eeb4f38f'})


def es_shape(fam, dL):
    """v1_3_4: the record's shape and its column count: V9 for D4 and D4M at d_L = -1, V12 otherwise (2414bd75 sect. 1)."""
    return ('V9', 3) if (fam in ('D4', 'D4M') and dL == -1) else ('V12', 4)


def es_bonds(fam, dL, nc, mono):
    """v1_3_4: the xi bonds of monomial mono in the record's orientation (vac column 0, the free end last: the free-left vertex 3c + r is
    3(nc - 1 - c) + r there), from the engine's own bonds(fam, d_L + 1)."""
    def fl_(x):
        return 3 * (nc - 1 - x // 3) + x % 3
    e_, f_ = bonds(fam, dL + 1)
    return sorted(sorted([fl_(vpair(b)[0]), fl_(vpair(b)[1])]) for b in {'1': [], 'e': [e_], 'f': [f_], 'ef': [e_, f_]}[mono])


def es_rebind(out_text, name, data):
    """v1_3_4, for the plants: the binding output with the record's RECORD line naming the sha256 of other bytes."""
    return '\n'.join(('RECORD %s %s' % (name, hashlib.sha256(data).hexdigest())) if (
        ln.startswith('RECORD ') and len(ln.split()) == 3 and ln.split()[1] == name) else ln for ln in out_text.split('\n'))


def es_check(data, out_text, name, N, fam, dL):
    """v1_3_4: one E_main record (data: its bytes; out_text: the binding run output) through the pinned M3 reader m3_reader_v6_3:
    C-ESEMI-SRC (the reader's binding _bound), the form (C-ESEMI-FORM-M in mock mode: M3_RECORD_v1_MOCK, the claim 'MOCK ' + CERT_CLAIM,
    EXPORT_STATUS MOCK, J_REF 300 and N, the items through the reader's _items; cert mode: loads), C-ESEMI-KEYS, C-ESEMI-NORM,
    C-ESEMI-USES and C-ESEMI-BONDS. Returns ({key: (LO, HI, err_b)}, {key: window id}); raises Refused naming the failing check."""
    R3 = mod.M3R
    try:
        R3._bound(name, data, out_text)
    except Exception as ex:
        raise Refused('C-ESEMI-SRC: %s' % ex)
    try:
        raw = json.loads(data.decode('utf-8'))
    except ValueError as ex:
        raise Refused('C-ESEMI-SRC: %s is not JSON (%s)' % (name, ex))
    es_runner(out_text, raw, ESRUN if MODE == 'mock' else ESRUN_CERT)   # v1_3_5: C-ESEMI-RUN
    if MODE == 'mock':
        if (raw.get('format'), raw.get('claim'), raw.get('EXPORT_STATUS'), raw.get('J_REF'), raw.get('N')) != (
                'M3_RECORD_v1_MOCK', 'MOCK ' + R3.CERT_CLAIM, 'MOCK', 300, N):
            raise Refused('C-ESEMI-FORM-M: %s is not a MOCK record of N = %d in S8\'s MOCK form' % (name, N))
        try:
            items, ents, _ofs = R3._items(raw, name, 300, N - 1)
        except Exception as ex:
            raise Refused('C-ESEMI-FORM-M: item check: %s' % ex)
        balls = {k: ([Fraction(a) - Fraction(r) for a, r in zip(v[0], v[2])], [Fraction(a) + Fraction(r) for a, r in zip(v[0], v[2])],
                     sum(Fraction(x) for x in items[k]['Bp'].values())) for k, v in ents.items()}
    else:
        if raw.get('EXPORT_STATUS') == 'MOCK':
            raise Refused('C-ESEMI-SRC: a MOCK record in cert mode')
        try:
            balls = R3.loads(data.decode('utf-8'), out_text, 300, N, name)['balls']
        except Exception as ex:
            raise Refused('C-ESEMI-SRC: m3_reader_v6_3.loads: %s' % ex)
    sh, nc = es_shape(fam, dL)
    hs, its, wh = raw.get('shape') or {}, raw.get('items') or {}, raw.get('windows') or {}
    if (raw.get('class'), raw.get('d_L'), hs.get('name'), hs.get('V'), len(hs.get('columns') or [])) != (fam, dL, sh, 3 * nc, nc):
        raise Refused('C-ESEMI-KEYS: header class %r, d_L %r, shape %r, not %s, %d, %s' % (raw.get('class'), raw.get('d_L'), hs.get('name'),
                                                                                         fam, dL, sh))
    if sorted(balls) != ESKEYS or sorted(its) != ESKEYS:
        raise Refused('C-ESEMI-KEYS: the keys are not exactly ES,<mono>,<k> for mono in 1, e, f, ef and k = 0..3')
    if raw.get('norm_twin') != 'ES,1,0' or not str(wh.get('ES,1,0', '')).endswith(':W1,0'):
        raise Refused('C-ESEMI-NORM: the norm twin %r (window %r) is not ES,1,0, the shape\'s W1,0' % (raw.get('norm_twin'), wh.get('ES,1,0')))
    wins = {}
    for mo in ESMONO:
        for k in range(4):
            key = 'ES,%s,%d' % (mo, k)
            it = its[key]
            w = it.get('window')
            if it.get('shape') != sh or not isinstance(w, str) or wh.get(key) != w or it.get('alias_of') not in (None, w):
                raise Refused('C-ESEMI-NORM: %s carries shape %r, window %r, alias_of %r (the header: shape %s, window %r)' % (
                    key, it.get('shape'), w, it.get('alias_of'), sh, wh.get(key)))
            if (it.get('class'), it.get('d_L'), it.get('mono'), it.get('k')) != (fam, dL, mo, k):
                raise Refused('C-ESEMI-KEYS: %s names (%r, %r, %r, %r)' % (key, it.get('class'), it.get('d_L'), it.get('mono'), it.get('k')))
            use = '%s d_L %d %s cp_%d' % (fam, dL, ESNAME[fam][mo], k)
            if use not in (it.get('uses') or []):
                raise Refused('C-ESEMI-USES: %s does not list %r' % (key, use))
            fac = it.get('factors') or []
            cps = [x for x in fac if isinstance(x, list) and x[:1] == ['cp']]
            xis = sorted(sorted(x[1]) for x in fac if isinstance(x, list) and x[:1] == ['xi'] and len(x) == 2 and isinstance(x[1], list))
            if cps != [['cp', k, 0]] or len(cps) + len(xis) != len(fac) or xis != es_bonds(fam, dL, nc, mo):
                raise Refused('C-ESEMI-BONDS: %s factors %r, expected cp %d and xi %s' % (key, fac, k, es_bonds(fam, dL, nc, mo)))
            wins[key] = w
    return balls, wins


def es_shared(items):
    """v1_3_5: C-ESEMI-SHARED over [(N, balls, windows)]: a window id carries one entry in every record that holds it."""
    seen = {}
    for N, balls, wins in items:
        for key, w in wins.items():
            if seen.setdefault((N, w), balls[key]) != balls[key]:
                raise Refused('C-ESEMI-SHARED: window %s differs between records' % w)


def es_runner(out_text, raw, run):
    """v1_3_5: the E_main records are bound to their runner. The binding output's first line names the runner and
    its full sha256, the record's engine field names the same runner and its parts, and the files hash to them. run = (folder, runner,
    full sha256, {part: full sha256}); None in cert mode until the reviewed production runner is pinned."""
    if run is None:
        raise Refused('C-ESEMI-RUN: the reviewed E_semi runner is not pinned')
    fold, name, sha, parts = run
    mm = re.match(r'^(\S+) item \S+ LIM \d+; script sha256 ([0-9a-f]{64});', out_text.split('\n', 1)[0])
    if mm is None or mm.group(1) != name or mm.group(2) != sha:
        raise Refused('C-ESEMI-RUN: the binding output\'s first line does not name %s with its full sha256' % name)
    eng = raw.get('engine') or {}
    if eng.get(name) != sha or eng.get('parts') != parts:
        raise Refused('C-ESEMI-RUN: the record\'s engine field does not name %s and its parts' % name)
    if sha_file(os.path.join(fold, name + '.py')) != sha or any(sha_file(os.path.join(fold, k)) != v for k, v in parts.items()):
        raise Refused('C-ESEMI-RUN: the runner\'s files do not hash to the pinned shas')


def es_load_all():
    """v1_3_4: every pinned E_main record (ESM in mock mode, ESEMI_CERT in cert mode) through es_check; v1_3_5: then es_shared over all of
    them (C-ESEMI-SHARED). Returns {(N, class, d_L): (balls, windows, the record's sha8)}."""
    res = {}
    for (N, fam, dL), p in sorted((ESM if MODE == 'mock' else ESEMI_CERT).items()):
        balls, wins = es_check(open(p, 'rb').read(), open(ESW[N]).read(), os.path.basename(p), N, fam, dL)
        res[(N, fam, dL)] = (balls, wins, sha_file(p)[:8])
    es_shared([(k[0], v[0], v[1]) for k, v in sorted(res.items())])
    return res


def pre_r123(A, pcs):
    """v1_3_5: PLANT-ESEMI-SHARED, PLANT-ESEMI-DPOS and C-ESEMI-RUN with PLANT-ESEMI-RUN, each through the
    reader's own functions (es_shared, es_row, es_runner). v1_3_5_2: C-LEVEL and PLANT-LEVEL first."""
    try:
        lw = ', '.join('%s %d: %d' % (f, d, lev_shift_window(f, d)) for f in ('D3', 'D4', 'D4M') for d in (-1, 0))
    except Refused as ex:
        lw = str(ex)
    out('C-LEVEL (v1_3_5_2; Route 1 of the review 90d302d8): each d_L <= 0 class\'s window puts cp_k on the first column after the '
        'observable (shift 0: the in-span sum at level d_R - 1 with X\'s q and Q1, \'span\') or on its own last column (shift 1: alpha at '
        'level d_R, so the vacuum term alone with Q0 b(d_R - 1) in R, \'vac\'); window shifts %s; the engine\'s table %s -> %s' % (
            lw, ', '.join('%s %d: %s' % (f, d, lev_treat(f, d)) for f in ('D3', 'D4', 'D4M') for d in (-1, 0)),
            gate('C-LEVEL', not refuses(level_check, LEVTREAT))))
    out('PLANT-LEVEL: the table with D3 at d_L = 0 in span at level d_R with X\'s q and Q1 (the review sect. 2\'s unsound mix), and in span '
        'at level d_R - 1 (the v1_3_5_1 reading), must each be refused -> %s' % plant('PLANT-LEVEL', refuses(
            level_check, {('D3', 0): 'span+1'}, tag='C-LEVEL') and refuses(level_check, {('D3', 0): 'span'}, tag='C-LEVEL')))
    recs = sorted(G['ES'].items())
    if not recs:
        return
    (N, fam, dL), (balls, wins, s8) = recs[0]
    k0 = sorted(balls)[0]
    LO, HI, err = balls[k0]
    dl = (HI[0] - LO[0]) + Fraction(1, 10 ** 9)
    b2 = dict(balls)
    b2[k0] = ([LO[0] + dl] + list(LO[1:]), [HI[0] + dl] + list(HI[1:]), err)
    out('PLANT-ESEMI-SHARED: two copies of the record %s, one with the a_0 of its window %s moved, must be refused, and two equal '
        'copies pass -> %s' % (s8, wins[k0], plant('PLANT-ESEMI-SHARED', refuses(es_shared, [(N, balls, wins), (N, b2, wins)],
                                                                                tag='C-ESEMI-SHARED')
                                                     and not refuses(es_shared, [(N, balls, wins), (N, balls, wins)]))))
    p = pcs[N]
    pre = es_prep(p, balls, fam)
    w0d, w0m = pre['d']['1'][0][0], pre['m']['1'][0][0]
    s_ = abs(arb(w0d.v.mid())) + arb(w0d.v.rad())
    pre2 = {'rad': pre['rad'], 'd': dict(pre['d']), 'm': dict(pre['m'])}
    pre2['d']['1'] = ([CM.D(w0d.v - s_, w0d.g)] + list(pre['d']['1'][0][1:]), pre['d']['1'][1])
    pre2['m']['1'] = ([w0m - s_] + list(pre['m']['1'][0][1:]), pre['m']['1'][1])
    out('PLANT-ESEMI-DPOS: es_row on the record\'s windows with W[1][0] shifted down by its value plus its radius must be refused, '
        'and the unshifted windows pass -> %s' % plant('PLANT-ESEMI-DPOS', refuses(es_row, pre2, p, 'inf', tag='C-ESEMI-DPOS')
                                                        and not refuses(es_row, pre, p, 'inf')))
    run = ESRUN if MODE == 'mock' else ESRUN_CERT
    pth = (ESM if MODE == 'mock' else ESEMI_CERT)[(N, fam, dL)]
    data, otxt = open(pth, 'rb').read(), open(ESW[N]).read()
    raw = json.loads(data.decode('utf-8'))
    out('C-ESEMI-RUN: the binding output\'s first line names the runner %s with its full sha256, the record\'s engine field names it '
        'and its parts, and the files hash to them -> %s' % (run[1] if run else '-', gate('C-ESEMI-RUN', not refuses(es_runner, otxt, raw, run))))
    if run:
        lines = otxt.split('\n')
        o2 = '\n'.join([lines[0].replace(run[2], '0' * 64)] + lines[1:])
        r2 = json.loads(data.decode('utf-8'))
        r2['engine'] = dict(r2['engine'], parts=dict(r2['engine']['parts'], **{sorted(run[3])[0]: '0' * 64}))
        out('PLANT-ESEMI-RUN: the binding output naming another runner sha on its first line, and a record whose engine field names another '
            'part sha, must each be refused -> %s' % plant('PLANT-ESEMI-RUN', refuses(es_runner, o2, raw, run, tag='C-ESEMI-RUN')
                                                            and refuses(es_runner, otxt, r2, run, tag='C-ESEMI-RUN')))


def cvd(pc, raw):
    """v1_3_4: cv_vec's contraction C^ v-hat (C^ = sqrt(g00) C, raw_j - (g_j0/g00) raw_0), with the window value first in every product
    so that it takes duals as well as balls."""
    K, sg = pc['K'], pc['g00'].sqrt()
    v = [raw[a + 1] - raw[0] * pc['kap'][a] for a in range(K)]
    res = []
    for k in range(K):
        s = v[0] * pc['C'][k][0]
        for a in range(1, K):
            s = s + v[a] * pc['C'][k][a]
        res.append(s * sg)
    return res


def es_prep(pc, E, fam):
    """v1_3_4: one record's windows on the piece box in s8core's mean-value form (entry_duals: slot 0 is t, then one slot per key's bar
    offset), with two more slots for the bulk centres c_e and c_f (the means export's balls of the row's family); the combinations
    W_X = W[ef] - c_f W[e] - c_e W[f] + c_e c_f W[1], W_e = W[e] - c_e W[1], W_f = W[f] - c_f W[1] and W_1, each with its contraction
    C^ v-hat[W], as duals ('d') and at the box centre ('m'), and the box radii ('rad')."""
    keys, Vd, Vm, rad = CM.entry_duals(E, pc['T'])
    n = len(rad) + 2
    Vd = {k: CM.D(v.v, list(v.g) + [ZERO, ZERO]) for k, v in Vd.items()}
    (el, eh), (gl, gh) = pc[fam]['ce'], pc[fam]['cf']
    cs = {'d': (CM.D(CM.span(el, eh), [ZERO] * (n - 2) + [ONE, ZERO]), CM.D(CM.span(gl, gh), [ZERO] * (n - 1) + [ONE])),
          'm': (CM.fr((el + eh) / 2), CM.fr((gl + gh) / 2))}
    res = {'rad': list(rad) + [CM.fr((eh - el) / 2), CM.fr((gh - gl) / 2)]}
    for tag, V in (('d', Vd), ('m', Vm)):
        ce, cf = cs[tag]
        W = {mo: [V['ES,%s,%d' % (mo, k)] for k in range(4)] for mo in ESMONO}
        ws = {'X': [W['ef'][k] - W['e'][k] * cf - W['f'][k] * ce + W['1'][k] * (ce * cf) for k in range(4)],
              'e': [W['e'][k] - W['1'][k] * ce for k in range(4)], 'f': [W['f'][k] - W['1'][k] * cf for k in range(4)], '1': W['1']}
        res[tag] = {q: (w, cvd(pc, w)) for q, w in ws.items()}
    return res


def es_rows(N, pc):
    """v1_3_4: es_prep of every pinned E_main record of N at the piece, kept on the piece's dict."""
    if 'es' not in pc:
        pc['es'] = {(f, d): (es_prep(pc, b, f), s8) for (n, f, d), (b, w, s8) in G['ES'].items() if n == N}
    return pc['es']


def es_row(pre, pc, dR):
    """v1_3_4: one row's E_main values (centred balls over the box): cm, the base Cov_main = E_X - m_e m_f = N_ef/D - (N_e/D)(N_f/D)
    (the approval after SEND_042); ex, E_X = N_X/D, the bulk-centred ball that R_X bounds; me, mf, the single-bond means less the centres;
    dd, D; with N = W[cp_0] + alpha . C^ v-hat[W] at S8's level d_R - 1 (2414bd75 sect. 1). 'far' and 'inf' read the vacuum term only;
    for 'far' the in-span parts go into R through e_far: nc = e_far ||C^ v-hat[W_X]||/D and nd = e_far ||C^ v-hat[W_1]||/D (1920fa90
    sect. 2), and (v1_3_5) nce and ncf likewise from W_e and W_f for R_e and R_f. cv0 is the vacuum-only Cov_main (INFO at
    C-ESEMI-T0)."""
    lev = None if dR in ('far', 'inf') else int(dR) - 1
    rad = pre['rad']

    def vals(tag, lv):
        P_ = pre[tag]

        def tot(q):
            w, cw = P_[q]
            s = w[0]
            if lv is not None:
                for k in range(pc['K']):
                    s = s + cw[k] * pc['al'][lv][k]
            return s
        d_ = tot('1')
        ex, me, mf = tot('X') / d_, tot('e') / d_, tot('f') / d_
        return [ex - me * mf, ex, me, mf, d_]
    try:
        r = dict(zip(('cm', 'ex', 'me', 'mf', 'dd'), [CM._cen(a, b, rad) for a, b in zip(vals('d', lev), vals('m', lev))]))
        r['cv0'] = CM._cen(vals('d', None)[0], vals('m', None)[0], rad)
        r['nc'], r['nd'], r['nce'], r['ncf'] = ZERO, ZERO, ZERO, ZERO
        if dR == 'far':
            nrm = {q: CM._cen([c / pre['d']['1'][0][0] for c in pre['d'][q][1]], [c / pre['m']['1'][0][0] for c in pre['m'][q][1]], rad)
                   for q in ('X', '1', 'e', 'f')}
            r['nc'], r['nd'] = pc['efar'] * CM.norm_up(nrm['X']), pc['efar'] * CM.norm_up(nrm['1'])
            r['nce'], r['ncf'] = pc['efar'] * CM.norm_up(nrm['e']), pc['efar'] * CM.norm_up(nrm['f'])
    except ValueError as ex:
        raise Refused('C-ESEMI-DPOS: %s' % ex)
    if not (r['dd'].lower() > 0):
        raise Refused('C-ESEMI-DPOS: D has lower end %s' % r['dd'].lower())
    return r


def es_ref(mode):
    """v1_3_5: R_e and R_f are in (the approval); their pending inputs are slots of their own (q_single, sg_single, bond_uw)."""
    return 'R_e and R_f in (v1_3_5)'


def tx_rows(path):
    """v1_3_5: pk15's certified t export, rows N<N>_P<i> = jlo jhi At_lo Vt_hi Ot_hi ... (its FIELDS line), as {(N, i): fields}."""
    res = {}
    for ln in open(path).read().split('\n'):
        mm = re.match(r'^N([34])_P(\d{4}) = (.*)$', ln)
        if mm:
            res[(int(mm.group(1)), int(mm.group(2)))] = mm.group(3).split()
    return res


def trb_read(N, text=None):
    """v1_3_5: N*_TRB from pk08's certified TRB run output (px08_trbcert_v1_1, asm item): VERDICT lines exactly [VERDICT VALID] and one
    READING line 'TRB_<N> <= <value>' (every J >= 300). Returns the value as a Fraction; raises Refused (C-TRB-SRC)."""
    lines = (open(TRBO[N]).read() if text is None else text).split('\n')
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise Refused('C-TRB-SRC: the TRB output of N=%d does not read exactly [VERDICT VALID]' % N)
    mm = [m for m in (re.match(r'^READING N=%d \(.*?\): TRB_%d <= ([0-9.eE+-]+);' % (N, N), ln) for ln in lines) if m]
    if len(mm) != 1:
        raise Refused('C-TRB-SRC: not exactly one READING line for TRB_%d' % N)
    v = F(mm[0].group(1))
    if not (v > 0):
        raise Refused('C-TRB-SRC: TRB_%d <= %s is not positive' % (N, v))
    return v


def ux_t(N, pc, tx=None):
    """v1_3_5: U for the horizontal bonds, p_t = (Vt_hi + Ot_hi)^(1/2) at the piece as an outward upper end, from pk15's certified
    t export (pk07: it bounds ||Q0 B_t u|| in the chain's normalization over lambda_0); C-UH-PIECE: the row exists, its jlo and jhi
    are the means export's, and Vt_hi, Ot_hi >= 0. Kept on the piece's dict (tx: PLANT-UH-PIECE's input)."""
    if tx is None and 'UH' in pc:
        return pc['UH']
    r = (G['TX'] if tx is None else tx).get((N, pc['i']))
    mr = G['MX'].get((N, 'D3', pc['i']))
    if r is None or mr is None or r[0:2] != mr[0:2]:
        raise Refused('C-UH-PIECE: the t export has no row N%d_P%04d on the means export\'s grid' % (N, pc['i']))
    v, o = F(r[3]), F(r[4])
    if v < 0 or o < 0:
        raise Refused('C-UH-PIECE: Vt_hi or Ot_hi is below 0 at N%d_P%04d' % (N, pc['i']))
    u = B(upf((B(v) + B(o)).sqrt()))
    if tx is None:
        pc['UH'] = u
    return u


def bond_uw(N, pc, fam, which, mode=None):
    """v1_3_5 (rule 6e38bd40 (a), erratum 4f34050b sect. 3): U >= ||Q0 b' u|| and W >= ||b'||_op for the row's bond 'e' or 'f', in the
    chain's normalization over lambda_0. Horizontal (every D3 bond and the t of D4 and D4M): U = p_t (ux_t; bb by the top-bottom
    reflection), W = A + |c| (F4). Vertical (the b of D4 and D4M): W = N*_TRB r + |c| with r = 1/lam0_lo, the trace bound; v1_3_5_1:
    U = N*_TRB r / 2, an outward upper end (the CONFIRM_UV_VERTICAL_BOND_rv02.md 851f6ba4 sect. 3: xi_b >= 0 gives A_X >= 0,
    the trace bound gives ||A_X|| <= N*_TRB r, and Bhatia-Davis gives ||Q0 A_X u||^2 <= (N*_TRB r)^2 / 4). mode stays for the callers."""
    if fam == 'D3' or which == 'e':
        c_ = pc[fam]['ce'] if which == 'e' else pc[fam]['cf']
        return ux_t(N, pc), B(F(G['H2']['N%d_A' % N]) + max(abs(c_[0]), abs(c_[1])))
    c_ = pc[fam]['cf']
    a_ = B(G['TRB'][N]) * B(pc['rhi'])
    return B(upf(a_ / 2)), a_ + B(max(abs(c_[0]), abs(c_[1])))


def uv_ok(N, pc, U):
    """v1_3_5_1, C-UV-BD: the vertical U equals N*_TRB r / 2 rounded up (851f6ba4 sect. 3), by value."""
    return upf(U) == upf(B(G['TRB'][N]) * B(pc['rhi']) / 2)


def es_standins(dL=None, typ=None):
    """v1_3_5_1: the MOCK stand-ins in force for a row (all of them when dL and typ are None), from the slot flags: q_e at d_L = -1 while
    N*_QE_HI and N*_QF_HI are not pinned (QEF_CERT), and the TD single-bond g-term while its form is not ruled (SG1_CERT); v1_3_5_2:
    the coded tau_bb at TD rows while its one-sided justification (J-3) is not in place (TAU1_CERT)."""
    if MODE != 'mock':
        return []
    out_ = []
    if QEF_CERT is None and (dL is None or dL == -1):
        out_.append('MOCK-QE-DLM1')
    if SG1_CERT is None and (typ is None or typ == 'TD'):
        out_.append('MOCK-SG1')
    if TAU1_CERT is None and (typ is None or typ == 'TD'):
        out_.append('MOCK-TAU-BB')
    return out_


def prod_term(N, pc, fam, rnL, eL, rnR, eR, scale=1):
    """v1_3_5 (erratum 4f34050b sect. 3; rule 6e38bd40 (b); the approval): the crude bound on the product of the row's two single-bond mean
    shifts at c*, |m| <= [O + W e_L e_R + (rn1_L + rn1_R) U + W (rn1_L e_R + e_L rn1_R + rn1_L rn1_R)] / (1 - (e_L + rn1_L)(e_R + rn1_R))
    with the crude one-sided part O = (e_L + e_R) U, per bond (bond_uw). Returns the upper ends (|m_e|, |m_f|, scale |m_e| |m_f|), scale
    being PLANT-PROD's input."""
    den = ONE - (eL + rnL) * (eR + rnR)
    if not (den.lower() > 0):
        raise Refused('C-PROD-DEN: 1 - (e_L + rn1_L)(e_R + rn1_R) has lower end %s' % den.lower())
    m = []
    for which in ('e', 'f'):
        U, W = bond_uw(N, pc, fam, which)
        m.append(upf(((eL + eR) * U + W * eL * eR + (rnL + rnR) * U + W * (rnL * eR + eL * rnR + rnL * rnR)) / den))
    return m[0], m[1], m[0] * m[1] * F(scale)


def qef_load(data=None, out_text=None):
    """v1_3_5_1: pk02's QEF_DLM1 record (N*_QE_HI and N*_QF_HI per kind at d_L = -1; the math with
    The review), bound by strict rule V2 to its run output, with its tags, its TRICK_DLM1 input named by the engine's DL1 pin, the three
    KEYMAP lines and the twelve values (exact decimals, > 0). N*_QF_HI_D4MA already holds the exact lambda_h/lambda_0 ratio (
    the record's NOTE_LAMBDA), so every value is read as the final bound, with no second lambda factor. Raises Refused (C-QEF-SRC)."""
    data = open(QEF, 'rb').read() if data is None else data
    wl = (open(QEFO).read() if out_text is None else out_text).split('\n')
    rule_v2_strict(wl, os.path.basename(QEF), hashlib.sha256(data).hexdigest(), where='C-QEF-SRC')
    d = {}
    for ln in data.decode('utf-8').split('\n'):
        k, sep, v = ln.partition(' = ')
        if sep and not ln.startswith('#'):
            d.setdefault(k, []).append(v)

    def one(k):
        return d[k][0] if len(d.get(k, [])) == 1 else None
    if (one('RECORD'), one('END'), one('FORMAT'), one('EXPORT_STATUS'), one('VERDICT_OF_WRITER')) != (
            'QEF_DLM1_v1', 'QEF_DLM1_v1', 'S4U_KV_v1', 'CERTIFIED', 'VALID'):
        raise Refused('C-QEF-SRC: the record\'s tags')
    if os.path.relpath(DL1, CODEDIR) + ':' + PINS[DL1] not in d.get('INPUT', []):
        raise Refused('C-QEF-SRC: the record does not name the engine\'s TRICK_DLM1 by its full sha256')
    vals = {}
    for kind, bf in (('D3B', 'bb'), ('D4A', 'b'), ('D4MA', 'b')):
        if not str(one('KEYMAP_' + kind)).startswith('QE N*_QE_HI_%s (bond t) ; QF N*_QF_HI_%s (bond %s)' % (kind, kind, bf)):
            raise Refused('C-QEF-SRC: KEYMAP_%s' % kind)
        for N in (4, 3):
            for qn in ('QE', 'QF'):
                s = one('N%d_%s_HI_%s' % (N, qn, kind))
                if s is None or not DEC_RE.fullmatch(s) or not (F(s) > 0):
                    raise Refused('C-QEF-SRC: N%d_%s_HI_%s' % (N, qn, kind))
                vals[(N, qn, kind)] = F(s)
    return vals


def q_damp(pc, e1=None):
    """v1_3_5_4: at d_L = 0, a = w-hat = l(-1), so Q0 a = eps_0 with
    ||eps_0|| = R_w and S eps_0 = eps_1 = Q0 l(0) (S8 l.106). X*'s first factor Z* damps it: ||Z* eps_0||^2 = lambda_0 <eps_0, S eps_0>
    <= lambda_0 R_w e_1, with e_1 = min(R_w rho1, sqrt(e(0)^2 + rn1(0)^2)), S8's certified bound on ||Q0 l(0)|| (l.200), both parts at the
    chain's level 0. Also e_3 = min(R_w rho1^3, sqrt(e(2)^2 + rn1(2)^2)) >= ||eps_3||. Returns the upper ends R_w, e_1, e_3,
    qw = sqrt(R_w e_1) and Y_1 = sqrt(1 + R_w e_3); e1 (plants only) replaces e_1."""
    Rw = B(upf(pc['Rw']))
    if e1 is None:
        e1 = B(min(upf(Rw * pc['rho1']), upf(CM.sqrt_up(pc['e'][0] * pc['e'][0] + pc['rn'][0] * pc['rn'][0]))))
    e3 = B(min(upf(Rw * CM.ipow(pc['rho1'], 3)), upf(CM.sqrt_up(pc['e'][2] * pc['e'][2] + pc['rn'][2] * pc['rn'][2]))))
    return {'Rw': Rw, 'e1': e1, 'e3': e3, 'qw': CM.sqrt_up(Rw * e1), 'y1': CM.sqrt_up(ONE + Rw * e3)}


def q_dl0(N, pc, fam, U, nX, Qa, e1=None):
    """v1_3_5_4, C-Q-DAMP: the d_L = 0 q. D3: U + min(F4 qw, nX R_w), F4 = (A + |c_t|)
    (A + |c_bb|) (HSN F4, with X* = Z G_B G_T Z*/lambda_0^3 and ||Z||_H = lambda_0^(1/2)). D4M: U + min(nHS qw, nX R_w), through Lemma
    D4's HS bound on Z M: X(D4m)* = Z M G_T Z*/lambda_0^2, so ||X* eps_0|| <= ||Z M||_HS (A + |c_t|) lambda_0 (lambda_0 R_w e_1)^(1/2)
    / lambda_0^2 <= nHS qw. The other branch uses ||Q0 a|| = R_w in place of Qa. D4: U + nX Qa, unchanged (M stands next to Z* in its X*)."""
    if fam == 'D4':
        return U + nX * Qa
    d_ = q_damp(pc, e1)
    lead = B(pc['F4']) if fam == 'D3' else pc[fam]['nHS']
    return U + bmin(lead * d_['qw'], nX * d_['Rw'])


def qdamp_check(pc, d_):
    """v1_3_5_4, C-Q-DAMP: a q_damp result against the form recomputed here from the piece's own sources (S8's R_w and rho1, the chain's
    level-0 and level-2 e and rn1): e_1, e_3, qw and Y_1 by value."""
    Rw = B(upf(pc['Rw']))
    e1 = min(upf(Rw * pc['rho1']), upf(CM.sqrt_up(pc['e'][0] * pc['e'][0] + pc['rn'][0] * pc['rn'][0])))
    e3 = min(upf(Rw * CM.ipow(pc['rho1'], 3)), upf(CM.sqrt_up(pc['e'][2] * pc['e'][2] + pc['rn'][2] * pc['rn'][2])))
    if upf(d_['e1']) != e1 or upf(d_['e3']) != e3:
        raise Refused('C-Q-DAMP: e_1 or e_3 is not the bound from the chain\'s level 0 or level 2')
    if upf(d_['qw']) != upf(CM.sqrt_up(Rw * B(e1))) or upf(d_['y1']) != upf(CM.sqrt_up(ONE + Rw * B(e3))):
        raise Refused('C-Q-DAMP: qw or Y_1 is not the damped form')


def rnx2(pc, dR):
    """v1_3_5_5: rnX' >= ||Q0 b(d_R)||, the chain's level-d_R bound
    min(sqrt(e(d_R)^2 + rn1(d_R)^2), R_w rho1^(d_R + 1)) up to level 5 (S8 holds levels -1 to 5) and R_w rho1^(d_R + 1), which is efar,
    beyond; 'far' reads efar (levels >= 7) and 'inf' 0. The row's own rnX sits at level d_R - 1, and S Q0 b(d) = Q0 b(d + 1)."""
    if dR == 'inf':
        return ZERO
    if dR == 'far':
        return B(upf(pc['efar']))
    lev = int(dR)
    bw = upf(B(upf(pc['Rw'])) * CM.ipow(pc['rho1'], lev + 1))
    if lev > 5:
        return B(bw)
    return B(min(upf(CM.sqrt_up(pc['e'][lev] * pc['e'][lev] + pc['rn'][lev] * pc['rn'][lev])), bw))


def ts_check(pc, dR, val):
    """v1_3_5_5, C-TWO-SIDED: a row's rnX' against the chain's level-d_R bound recomputed here from S8's R_w and rho1 and the chain's
    level-d_R e and rn1 (levels up to 5; R_w rho1^(d_R + 1) beyond), by value."""
    lev = int(dR)
    bw = upf(B(upf(pc['Rw'])) * CM.ipow(pc['rho1'], lev + 1))
    ref = bw if lev > 5 else min(upf(CM.sqrt_up(pc['e'][lev] * pc['e'][lev] + pc['rn'][lev] * pc['rn'][lev])), bw)
    if upf(val) != ref:
        raise Refused('C-TWO-SIDED: rnX\' of (0,%s) is not the chain\'s level-%d bound' % (dR, lev))


def q_single(N, pc, fam, dL, which, Qa, ov=None, mode=None):
    """v1_3_5: q_e = ||Q0 e'^* a-hat|| for R_e (q_f likewise). d_L = 0: route (ii) with one bond (rule 6e38bd40 (a)), q_e <= U + W Qa,
    checked by value after any override (C-QE-ROUTE2); v1_3_5_4 (C-Q-DAMP): D3's t bond reads U + W qw, its X*
    starting with Z*. d_L = -1 (v1_3_5_1): pk02's N*_QE_HI or N*_QF_HI of the row's kind from QEF_DLM1 (qef_load). Each bounds
    ||X_e^* a-hat|| with a-hat = S'^-1 w-hat, so <a-hat, X_1 u> = 1, the normalization of TRICK_DLM1's Q_HI. The value is checked by
    value after any override (C-QE-DLM1); N*_QF_HI_D4MA already holds the lambda_h/lambda_0 ratio and is read as it stands."""
    ov = ov or {}
    if dL == 0:
        U, W = bond_uw(N, pc, fam, which, mode)
        qx = U + W * (q_damp(pc)['qw'] if (fam == 'D3' and which == 'e') else Qa)
        qv = ov.get('qe_dl0', qx)
        if not same_ball(qv, qx):
            raise Refused('C-QE-ROUTE2: the d_L = 0 q_%s of %s is not U + W Qa (U + W qw for D3\'s t)' % (which, fam))
        return qv
    qx = B(G['QEF'][(N, 'QE' if which == 'e' else 'QF', KIND[fam])])
    qv = ov.get('qe_dlm1', qx)
    if not same_ball(qv, qx):
        raise Refused('C-QE-DLM1: the d_L = -1 q_%s of %s is not the record\'s value for kind %s' % (which, fam, KIND[fam]))
    return qv


def sg_single(typ, which, sgp, Qa, eps, s):
    """v1_3_5_2: the single-bond g-term of R_e (which 'e', the t bond) and R_f ('f', the bb bond) at TD rows.
    sigma_g,e = u^2 (eps Y_c + eps^2)/(1 - s^2): no bond on the right gap, so L -> 1 and no tail. sigma_g,f = u^2 (eps L Y_1 + eps^2 L^2)
    /(1 - s^2) + Y_1 tau_1(L), with the joint's L; v1_3_5_4: Y_1 tau_1(L) in place of the coded tau_bb (pk15 ed0ae46c Claim T
    53ec0d98), and Y_1 from sigma_parts (sqrt(1 + R_w e_3) at the TD rows, C-Q-DAMP). Zero at the other row types; Qa stays for the
    callers' interface."""
    if typ != 'TD':
        return ZERO
    u, epb, dn = sgp['u'], B(eps), ONE - B(s) * B(s)
    if which == 'e':
        return u * u * (epb * sgp['Yc'] + epb * epb) / dn
    Lb, y1 = B(sgp['L']), sgp['Y1']
    return u * u * (epb * Lb * y1 + epb * epb * Lb * Lb) / dn + y1 * sgp['tau1']


def pre_prod(pcs):
    """v1_3_5: the d_L >= 1 product term (INFO share, PLANT-PROD) and the d_L = 0 route (ii) check (PLANT-QE-ROUTE2) at the first piece of
    each N, through eval_rows."""
    for N in (4, 3):
        p, uv = pcs[N], G['UV'][N]
        rows = eval_rows(N, p, uv)
        jd = [judge(lo, cov) for (row, lo, cov, info) in rows]
        sh = [(float(info['prod'][2]) / float(j[2]), rname(row)) for (row, lo, cov, info), j in zip(rows, jd)
              if 'prod' in info and row['typ'] in ('A2', 'B3') and j[2] is not None and j[2] > 0]
        top = max(sh) if sh else (None, '-')
        out('C-PROD N=%d (erratum 4f34050b sect. 3, crude O_e): the product term at the first piece, largest share of lo_lo %s at %s (INFO)' % (
            N, ('%.3e' % top[0]) if top[0] is not None else '-', top[1]))
        cand = [(j[1], k) for k, j in enumerate(jd) if j[0] and rows[k][0]['typ'] in ('A2', 'B3')]
        if cand:
            h0, k0 = min(cand)
            row, lo, cov, info = rows[k0]
            sc = 2 * jd[k0][2] / info['prod'][2] + 1
            rows2 = eval_rows(N, p, uv, {'prod_scale': sc})
            out('PLANT-PROD N=%d: the binding row %s with its product term scaled by %.3g (past its lo) must fail -> %s' % (
                N, rname(row), float(sc), plant('PLANT-PROD', not judge(rows2[k0][1], rows2[k0][2])[0])))
        if any(k[0] == N and k[2] == 0 for k in G['ES']):
            out('PLANT-QE-ROUTE2 N=%d: a d_L = 0 q_e other than U + W Qa must be refused (C-QE-ROUTE2) -> %s' % (
                N, plant('PLANT-QE-ROUTE2', refuses(eval_rows, N, p, uv, {'qe_dl0': ZERO}, tag='C-QE-ROUTE2'))))


def es_t0(N, ev):
    """v1_3_4: C-ESEMI-T0 (2414bd75 sect. 1, with the centre-free base) at the last piece, t from 0 to 1/J_lo: every E_main row's
    harmonic Cov (harm_ball, the t = 0 stand-in) lies in [Cov_main_lo - R_hi, Cov_main_hi + R_hi]; v1_3_5: R is the full
    R_X + |m_e| R_f + |m_f| R_e + R_e R_f in both modes (mock mode with its labelled stand-ins). PLANT-ESEMI-T0-BASE: the bulk-centred E_X
    in place of Cov_main must leave the window at one row at least. INFO: the vacuum-only Cov's deviation over R at the finite rows
    (2414bd75's in-span plant, which has no power here); the thin comparison of midpoints (the optional note). v1_3_5_2 (
    The review 90d302d8 sect. 5 NOTE): R covered the D3 level defect, so the window alone cannot see a wrong main term; alpha is read one
    level down and one level up (where S8's chain has the level, 0 to 5) at every finite 'span' row. v1_3_5_3: a row has
    power when both shifted readings miss harm by more than T0_FRAC R (v1_3_5_4: midpoints). C-ESEMI-T0-LEVEL is a gate at the
    rows with power: the engine's level misses harm by less than either shift (midpoints). At the other rows it is INFO
    (INFO C-ESEMI-T0-LEVEL-NOPOWER). Each row prints its three misses. PLANT-ESEMI-T0-LEVEL: every 'span' class with a finite row has
    power at one row at least, so that T0 tests each class's main term. INFO: each row's midpoint deviation beside R; at the 'vac' rows
    (Route 1, the vacuum main term) the miss with alpha at level d_R - 1 and at level d_R, the data side of C-LEVEL."""
    pc, rows, jd, bad, kills = ev
    er = [(row, cov, info) for (row, lo, cov, info) in rows if 'es' in info] if rows else []
    if not er:
        if MODE == 'mock' and not any(k[0] == N for k in G['ES']):
            out('C-ESEMI-T0 N=%d: no E_main record is pinned at N=%d in this mock (its rows keep the stand-in) -> N/A' % (N, N))
        else:
            out('C-ESEMI-T0 N=%d: no E_main row at the last piece -> %s' % (N, gate('C-ESEMI-T0', False)))
        return

    def inside(x, cov, R):
        return lof(cov) <= upf(x) + upf(R) and lof(x) - upf(R) <= upf(cov)

    def dmid(x, cov):
        return abs(float(x.mid()) - float(cov.mid()))
    res, pb, inf_, thin, devs, vac = [], [], [], [], [], []
    lvg, lvg_t, lvn_t, cls = [], [], [], {}
    for row, cov, info in er:
        em, R = info['es'][0], info['R']
        ok = inside(em['cm'], cov, R)
        dm, Rf = dmid(em['cm'], cov), float(upf(R))
        res.append((ok, '%s dev %.2e R %.2e %s' % (rname(row), dm, Rf, 'in' if ok else 'OUT')))
        pb.append(not inside(em['ex'], cov, R))
        devs.append('%s %.2e (%.2g R)' % (rname(row), dm, dm / Rf if Rf > 0 else float('inf')))
        if row['dR'] in ('far', 'inf'):
            continue
        pre_, d_ = es_rows(N, pc)[(row['fam'], row['dL'])][0], int(row['dR'])
        if lev_treat(row['fam'], row['dL']) == 'vac':
            up_ = ('%.2e' % dmid(es_row(pre_, pc, str(d_ + 1))['cm'], cov)) if d_ + 1 <= 6 else 'n/a'
            vac.append('%s %.2e at level %d, %s at level %d' % (rname(row), dmid(es_row(pre_, pc, str(d_))['cm'], cov), d_ - 1, up_, d_))
            continue
        dv = dmid(em['cv0'], cov)
        inf_.append('%s %.2e' % (rname(row), dv / Rf))
        thin.append((dv, dm, rname(row)))
        sh = []
        for d2 in (d_ - 1, d_ + 1):
            if 1 <= d2 <= 6:
                c2 = es_row(pre_, pc, str(d2))['cm']
                sh.append((d2 - 1, dmid(c2, cov), dmid(c2, cov) > float(T0_FRAC) * Rf))   # v1_3_5_4: power on midpoints
        pw = len(sh) == 2 and all(p_ for l_, m_, p_ in sh)
        txt = '%s own %.2e, %s, R %.2e' % (rname(row), dm, ', '.join('level %d %.2e (%.2g R)' % (l_, m_, m_ / Rf) for l_, m_, p_ in sh), Rf)
        cls.setdefault((row['fam'], row['dL']), []).append(pw)
        if pw:
            g_ = all(dm < m_ for l_, m_, p_ in sh)
            lvg.append(g_)
            lvg_t.append('%s: %s' % (txt, 'less' if g_ else 'NOT LESS'))
        else:
            lvn_t.append(txt)
    out('C-ESEMI-T0 N=%d (last piece %d; R is the full R_X + |m_e| R_f + |m_f| R_e + R_e R_f%s): %s -> %s' % (
        N, pc['i'], ', with the mock stand-ins' if MODE == 'mock' else '', '; '.join(l for o, l in res),
        gate('C-ESEMI-T0', all(o for o, l in res))))
    out('PLANT-ESEMI-T0-BASE N=%d: the bulk-centred E_X in place of Cov_main must leave the window at one row at least (%d of %d) -> %s' % (
        N, sum(pb), len(pb), plant('PLANT-ESEMI-T0-BASE', any(pb))))
    out('C-ESEMI-T0-LEVEL N=%d (v1_3_5_3): at the finite \'span\' rows with power (both one-level '
        'shifts of alpha miss harm by more than R/%d), the engine\'s level misses harm by less than either shift (%d of %d rows): %s -> %s' % (
            N, T0_FRAC.denominator, sum(lvg), len(lvg), '; '.join(lvg_t) or 'none', gate('C-ESEMI-T0-LEVEL', bool(lvg) and all(lvg))))
    out('INFO C-ESEMI-T0-LEVEL-NOPOWER N=%d (not gated): the finite \'span\' rows without power (a shift outside S8\'s levels 0 to 5, or a '
        'shifted miss of at most R/%d): %s' % (N, T0_FRAC.denominator, '; '.join(lvn_t) or 'none'))
    out('PLANT-ESEMI-T0-LEVEL N=%d: every \'span\' class with a finite row at the last piece must have power at one row at least (rows with '
        'power by class: %s) -> %s' % (N, ', '.join('%s %d: %d of %d' % (f, d, sum(v), len(v)) for (f, d), v in sorted(cls.items())),
                                       plant('PLANT-ESEMI-T0-LEVEL', bool(cls) and all(any(v) for v in cls.values()))))
    out('INFO C-ESEMI-T0-DEV N=%d (v1_3_5_2, main): each row\'s midpoint deviation from harm, beside R: %s' % (N, ', '.join(devs)))
    out('INFO C-LEVEL-T0 N=%d (v1_3_5_2): the \'vac\' rows (Route 1) with alpha at level d_R - 1 and at level d_R, midpoint misses: %s' % (
        N, '; '.join(vac) or 'none'))
    out('INFO C-ESEMI-T0-SPAN N=%d: |vacuum-only Cov - harm| / R at the finite \'span\' rows: %s' % (N, ', '.join(inf_) or 'none'))
    if thin:
        w = max(thin)
        away = [nm_ for dv, dm, nm_ in thin if dm >= dv]
        out('INFO C-ESEMI-T0-THIN N=%d: the in-span sum moves the midpoint closer to harm at %d of %d finite \'span\' rows (away at: %s); '
            'the largest vacuum-only deviation %.3e (at %s) goes to %.3e' % (N, len(thin) - len(away), len(thin), ', '.join(away) or 'none',
                                                                             w[0], w[2], w[1]))


def pre_esemi(A, pcs):
    """v1_3_4: the E_main records' gates and plants, each through the reader's own functions (es_check, es_load_all), and C-ESEMI-S8TWIN
    against S8's own entries A['EP']. v1_3_5: the slots' gates and plants (C-QE-SLOT, C-UV-SLOT, C-SG1-SLOT) in place of C-ESEMI-RE, and
    C-TRB-SRC, C-UH-PIECE and C-UE-LE-WE at the first pieces pcs, each with a plant."""
    recs = sorted(G['ES'].items())
    out('C-ESEMI-SRC (m3_reader_v6_3, %s mode): %s; binding output %s -> %s' % (
        MODE, ', '.join('N%d %s d_L %d %s' % (k[0], k[1], k[2], v[2]) for k, v in recs) or 'none',
        ', '.join('N%d %s' % (n, sha_file(p)[:8]) for n, p in sorted(ESW.items())), gate('C-ESEMI-SRC', bool(recs))))
    out('C-ESEMI-FORM-M, -KEYS, -USES, -NORM, -BONDS and -SHARED: every pinned record passed es_check and es_load_all (a refusal stops the '
        'run); windows shared between records %d -> %s' % (sum(1 for k, v in recs for w in v[1].values()) - len(
            set((k[0], w) for k, v in recs for w in v[1].values())), gate('C-ESEMI-KEYS', bool(recs))))
    if recs:
        (N, fam, dL), (balls, wins, s8) = recs[0]
        p = (ESM if MODE == 'mock' else ESEMI_CERT)[(N, fam, dL)]
        data, otxt, nm = open(p, 'rb').read(), open(ESW[N]).read(), os.path.basename(p)

        def mod_(fn):
            r2 = json.loads(data.decode('utf-8'))
            fn(r2)
            d2 = json.dumps(r2).encode('utf-8')
            return (d2, es_rebind(otxt, nm, d2), nm, N, fam, dL)
        ps = [refuses(es_check, data, '\n'.join(ln for ln in otxt.split('\n') if not ln.startswith('RECORD %s ' % nm)), nm, N, fam, dL,
                      tag='C-ESEMI-SRC'),
              refuses(es_check, data, otxt + '\nVERDICT VALID\n', nm, N, fam, dL, tag='C-ESEMI-SRC'),
              refuses(es_check, data + b' ', otxt, nm, N, fam, dL, tag='C-ESEMI-SRC')]
        out('PLANT-ESEMI-SRC (%s): the binding output without the record\'s RECORD line, with a second VERDICT line, and the record with '
            'one byte more, must each be refused -> %s' % (nm, plant('PLANT-ESEMI-SRC', all(ps))))
        k0 = 'ES,ef,1'
        pk = [refuses(es_check, *mod_(lambda r: r['items'].pop('ES,f,3')), tag='C-ESEMI-KEYS'),
              refuses(es_check, *mod_(lambda r: r['items'][k0].update(uses=[])), tag='C-ESEMI-USES'),
              refuses(es_check, *mod_(lambda r: r['items'][k0].update(shape='V9' if r['shape']['name'] == 'V12' else 'V12')),
                      tag='C-ESEMI-NORM'),
              refuses(es_check, *mod_(lambda r: r.update(norm_twin='ES,1,1')), tag='C-ESEMI-NORM'),
              refuses(es_check, *mod_(lambda r: r['items'][k0].update(factors=[x if x[:1] != ['xi'] else ['xi', [0, 1]]
                                                                               for x in r['items'][k0]['factors']])), tag='C-ESEMI-BONDS')]
        if MODE == 'mock':
            pk.append(refuses(es_check, *mod_(lambda r: r.update(format='M3_RECORD_v1')), tag='C-ESEMI-FORM-M'))
        out('PLANT-ESEMI-ITEMS (%s, rebound to the planted bytes): a missing key, an item without its use, an item with the other shape, '
            'a norm twin ES,1,1, an item with a wrong bond%s, must each be refused -> %s' % (
                nm, ', and the certified FORMAT in mock mode' if MODE == 'mock' else '', plant('PLANT-ESEMI-ITEMS', all(pk))))
        if MODE == 'mock':
            def _mc():
                try:
                    mod.M3R.loads(data.decode('utf-8'), otxt, 300, N, nm)
                except Exception as ex:
                    raise Refused('C-ESEMI-MOCKCERT: %s' % str(ex)[:120])
            out('PLANT-ESEMI-MOCKCERT: m3_reader_v6_3\'s certified parse (loads) must refuse the MOCK record -> %s' % plant(
                'PLANT-ESEMI-MOCKCERT', refuses(_mc, tag='C-ESEMI-MOCKCERT')))
        tw = []
        for (n_, f_, d_), (b_, w_, s_) in recs:
            sh = es_shape(f_, d_)[0]
            for k in range(4):
                a, s = b_['ES,1,%d' % k], A['EP'][n_]['%s,%d' % (ESTWIN[sh], k)]
                tw.append(all(a[0][j] <= s[1][j] and s[0][j] <= a[1][j] for j in range(4)))
        out('C-ESEMI-S8TWIN: ES,1,k of each record against S8\'s own entry of the same window (f,k on V9, h,k on V12): the a_k balls '
            'overlap at %d of %d -> %s' % (sum(tw), len(tw), gate('C-ESEMI-S8TWIN', bool(tw) and all(tw))))
        a, s = balls['ES,1,1'], A['EP'][N]['%s,3' % ESTWIN[es_shape(fam, dL)[0]]]
        out('PLANT-ESEMI-S8TWIN: ES,1,1 against S8\'s entry of k = 3 must not overlap -> %s' % plant(
            'PLANT-ESEMI-S8TWIN', not all(a[0][j] <= s[1][j] and s[0][j] <= a[1][j] for j in range(4))))
    p4 = pcs[4]
    qa4 = p4['Q'][-1]
    qd, qo = open(QEF, 'rb').read(), open(QEFO).read()
    out('C-QEF-SRC (v1_3_5_1): %s (%s) bound by strict rule V2 to %s (%s); the tags, the TRICK_DLM1 input pin, the KEYMAP lines and the '
        'twelve values -> %s' % (os.path.basename(QEF), sha_file(QEF)[:8], os.path.basename(QEFO), sha_file(QEFO)[:8],
                                 gate('C-QEF-SRC', not refuses(qef_load, qd, qo))))
    qlines = qo.split('\n')
    pq = [refuses(qef_load, qd, '\n'.join(ln for ln in qlines if not ln.startswith('RECORD ')), tag='C-QEF-SRC'),
          refuses(qef_load, qd + b'\n', qo, tag='C-QEF-SRC'),
          not refuses(qef_load, qd, '\n'.join(qlines[:1] + ['C-MIDLINE: a line that carries VERDICT VALID inside it'] + qlines[1:]))]
    out('PLANT-QEF-SRC: the run output without its RECORD line, and the record with one byte more, must each be refused; an output with a '
        'line carrying VERDICT mid-line must still be accepted, since only a line start counts -> %s' % plant('PLANT-QEF-SRC', all(pq)))
    okq = all(same_ball(q_single(4, p4, f_, -1, w_, qa4), B(G['QEF'][(4, 'QE' if w_ == 'e' else 'QF', KIND[f_])]))
              for f_ in ('D3', 'D4', 'D4M') for w_ in ('e', 'f'))
    out('C-QE-DLM1 (v1_3_5_1): q_e and q_f at d_L = -1 are the record\'s N*_QE_HI and N*_QF_HI of the row\'s kind, read as final bounds '
        '(N*_QF_HI_D4MA holds the lambda ratio already) -> %s' % gate('C-QE-DLM1', okq))
    out('PLANT-QE-DLM1: a D4M row\'s q_f fed the D4A value must be refused -> %s' % plant('PLANT-QE-DLM1', refuses(
        q_single, 4, p4, 'D4M', -1, 'f', qa4, {'qe_dlm1': B(G['QEF'][(4, 'QF', 'D4A')])}, tag='C-QE-DLM1')))
    for n_ in (4, 3):
        pn = pcs[n_]
        uv_, wv_ = bond_uw(n_, pn, 'D4', 'f')
        out('C-UV-BD N=%d (v1_3_5_1): the vertical U = N*_TRB r / 2 = %s by value, at most W = %s, below 1 (%s) '
            '-> %s' % (n_, fstr(upf(uv_), 8), fstr(upf(wv_), 8), upf(uv_) < 1, gate('C-UV-BD', uv_ok(n_, pn, uv_) and upf(uv_) <= lof(wv_))))
        out('PLANT-UV-BD N=%d: a vertical U half as large must fail the by-value check -> %s' % (
            n_, plant('PLANT-UV-BD', not uv_ok(n_, pn, uv_ / 2))))
    sp4 = p4['s'] * (1 + p4['s'])
    dq4 = q_damp(p4)   # v1_3_5_4: the TD rows' damped Y_c and Y_1 (C-Q-DAMP)
    sgp4 = sigma_parts(4, p4, dq4['qw'], p4['eps'], p4['s'], sp4, y1=dq4['y1'])
    sge4 = sg_single('TD', 'e', sgp4, qa4, p4['eps'], p4['s'])
    sgf4 = sg_single('TD', 'f', sgp4, qa4, p4['eps'], p4['s'])
    out('C-SG1 (v1_3_5_2): the TD single-bond g-terms at N4 piece %d: sigma_g,e %.3e and sigma_g,f %.3e, beside '
        'the joint %.3e (L %s; Y_c %.4f; J-1) -> %s' % (p4['i'], float(upf(sge4)), float(upf(sgf4)), float(upf(sgp4['sg'])), fstr(sgp4['L'], 6),
                                                       float(upf(sgp4['Yc'])), gate('C-SG1', all(
            math.isfinite(float(x.mid())) and lof(x) >= 0 for x in (sge4, sgf4, sgp4['sg'])))))
    pb1 = dict(p4, D3=dict(p4['D3'], ce=(-Fraction(1, 10 ** 6), p4['D3']['ce'][1])))
    pb2 = dict(p4, D3=dict(p4['D3'], cf=(p4['D3']['cf'][0], Fraction(10 ** 3))))
    pb3 = dict(p4, D3=dict(p4['D3'], cf=(-Fraction(1, 10 ** 6), p4['D3']['cf'][1])))
    out('C-SG-CENTRE (J-2; v1_3_5_4: Claim T step T1): the means balls for t and bb start at %s and %s, both >= 0, and L = %s is at least '
        'the upper end %s of c_bb -> %s' % (fstr(p4['D3']['ce'][0], 8), fstr(p4['D3']['cf'][0], 8), fstr(sgp4['L'], 6),
                                          fstr(p4['D3']['cf'][1], 8), gate('C-SG-CENTRE', p4['D3']['ce'][0] >= 0 and p4['D3']['cf'][0] >= 0
                                                                           and sgp4['L'] >= p4['D3']['cf'][1])))
    out('PLANT-SG-CENTRE: a means ball for t below 0, a c_bb ball above every L on the grid, and a c_bb ball below 0, must each be '
        'refused -> %s' % plant('PLANT-SG-CENTRE', all(refuses(sigma_parts, 4, pb_, qa4, p4['eps'], p4['s'], sp4, tag='C-SG-CENTRE')
                                                        for pb_ in (pb1, pb2, pb3))))
    st_ = open(SIGG).read()
    cnv = {n: (sigg_cert(st_, n), m2b_vals(n)[0]) for n in (4, 3)}
    out('C-TAU1 (v1_3_5_4; J-3 closed by pk15/NOTE_J3_TAIL_ONESIDED_G1_v1.md ed0ae46c Claim T and '
        'rv02/CHECK_J3_TAIL_ONESIDED_G1_rv02.md 53ec0d98): the bb tail is Y tau_1(L), tau_1 = C_N tail_h1(N, L), C_N = u kappa^(1/2) '
        '(1 + kappa) Phi_eps^(1/2) with u = 1/(1 - eps_r(300)); kappa_max and Phi_eps from %s (%s, rule V2), eps_r(300) from %s (%s); '
        'C_4 <= %s, C_3 <= %s (outward), formed again from the sources -> %s' % (
            os.path.basename(SIGG), sha_file(SIGG)[:8], os.path.basename(M2B), sha_file(M2B)[:8], fstr(G['CN'][4], 20),
            fstr(G['CN'][3], 20), gate('C-TAU1', all(G['CN'][n] == cn_ball(cnv[n][0][0], cnv[n][0][1], cnv[n][1]) for n in (4, 3)))))
    out('PLANT-TAU1: C_N with eps_r = 1 must be refused -> %s' % plant('PLANT-TAU1', refuses(
        cn_ball, cnv[4][0][0], cnv[4][0][1], Fraction(1), tag='C-TAU1')))
    xc = []
    for n in (4, 3):
        b_ = cn_full(cnv[n][0][0], cnv[n][0][1], cnv[n][1])
        xc.append('C_%d upper end %s at or below %s: %s; midpoint %.2g relative from %s' % (
            n, fstr(upf(b_), 20), HZ_CN[n][0], upf(b_) <= Fraction(HZ_CN[n][0]),
            abs(float(b_.mid()) - float(Fraction(HZ_CN[n][1]))) / float(Fraction(HZ_CN[n][1])), HZ_CN[n][1]))
    out('INFO C-TAU1-XCHECK (pk15 01:45Z with its correction): %s' % '; '.join(xc))
    mt = open(MHATO).read()
    out('C-MHAT-SRC (v1_3_5_4; the review 53ec0d98 T6: c_K/mu-hat <= kappa rests on m-hat >= 1): %s (%s) binds %s by its RECORD line, with one '
        'passing C-MHAT line per N, m1..m3 >= 0 (%s) -> %s' % (
            os.path.basename(MHATO), sha_file(MHATO)[:8], os.path.basename(M2B),
            '; '.join('N%d %s' % (n, ', '.join(fstr(x, 6) for x in G['MHAT'][n])) for n in (4, 3)),
            gate('C-MHAT-SRC', not refuses(mhat_src, mt, PINS[M2B]))))
    out('PLANT-MHAT-SRC: the M2B asm output without its C-MHAT N=4 line must be refused -> %s' % plant('PLANT-MHAT-SRC', refuses(
        mhat_src, '\n'.join(ln for ln in mt.split('\n') if not ln.startswith('C-MHAT N=4')), PINS[M2B], tag='C-MHAT-SRC')))
    qd_ok, qd_txt, qd_pw = [], [], []
    for n in (4, 3):
        pn = pcs[n]
        dn = q_damp(pn)
        qd_ok.append(not refuses(qdamp_check, pn, dn))
        qd_txt.append('N%d piece %d: R_w %.4e, rho1 %.6f, e_1 %.3e, e_3 %.3e; D3 X part min(F4 qw %.4f, nX R_w %.4f) against nX Qa %.4f; '
                      'D4M nHS qw %.4f against nX Qa %.4f; D3 Q1 %.3e against Qa %.3e; Y_1 %.8f' % (
                          n, pn['i'], fl(dn['Rw']), fl(pn['rho1']), fl(dn['e1']), fl(dn['e3']), fl(B(pn['F4']) * dn['qw']),
                          fl(pn['D3']['nX'] * dn['Rw']), fl(pn['D3']['nX'] * pn['Q'][-1]), fl(pn['D4M']['nHS'] * dn['qw']),
                          fl(pn['D4M']['nX'] * pn['Q'][-1]), fl(dn['e3']), fl(pn['Q'][-1]), fl(dn['y1'])))
        qd_pw.append(upf(q_dl0(n, pn, 'D3', ZERO, pn['D3']['nX'], pn['Q'][-1], e1=dn['Rw']))
                     > upf(q_dl0(n, pn, 'D3', ZERO, pn['D3']['nX'], pn['Q'][-1])))
    out('C-Q-DAMP (v1_3_5_4; rv02/SCOPE_D3_DL0_SHARP_Q_rv02.md 1ab6f209): the damped d_L = 0 q for D3 and D4M, and for D3 '
        'Q1 = e_3, Y_1 = sqrt(1 + R_w e_3), Y_c\'s w part and route (ii)\'s t term with qw = sqrt(R_w e_1); e_1 and e_3 recomputed from '
        'S8\'s R_w and rho1 and the chain\'s level-0 and level-2 e and rn1: %s -> %s' % ('; '.join(qd_txt), gate('C-Q-DAMP', all(qd_ok))))
    e1p = B(min(upf(B(upf(p4['Rw'])) * CM.ipow(p4['rho1'], 2)), upf(CM.sqrt_up(p4['e'][1] * p4['e'][1] + p4['rn'][1] * p4['rn'][1]))))
    out('PLANT-Q-DAMP: a q_damp result whose e_1 comes from the chain\'s level 1 must be refused, and with e_1 = R_w the D3 q must rise '
        'at both N (the damping loses its power) -> %s' % plant('PLANT-Q-DAMP', all(qd_pw) and refuses(
            qdamp_check, p4, dict(q_damp(p4), e1=e1p), tag='C-Q-DAMP')))
    ts_ok, ts_txt = [], []
    for n in (4, 3):
        pn = pcs[n]
        for d_ in [str(k) for k in range(1, 7)]:
            v_ = rnx2(pn, d_)
            ts_ok.append(not refuses(ts_check, pn, d_, v_))
            if d_ in ('1', '2'):
                r_, e_ = side(pn, d_)
                ts_txt.append('N%d piece %d (0,%s): rnX %.3e, rnX\' %.3e' % (n, pn['i'], d_, fl(CM.sqrt_up(e_ * e_ + r_ * r_)), fl(v_)))
    out('C-TWO-SIDED (v1_3_5_5; rv02/RULING_TWO_SIDED_DAMPING_V2_rv02.md 83db00da): rnX\' for d_R = 1 to 6 at the pre\'s '
        'pieces of both N, recomputed from S8\'s R_w and rho1 and the chain\'s level-d_R e and rn1 (levels up to 5), equals rnx2 (%s) -> %s' % (
            '; '.join(ts_txt), gate('C-TWO-SIDED', bool(ts_ok) and all(ts_ok))))
    w1 = B(min(upf(CM.sqrt_up(p4['e'][1] * p4['e'][1] + p4['rn'][1] * p4['rn'][1])), upf(B(upf(p4['Rw'])) * CM.ipow(p4['rho1'], 2))))
    out('PLANT-TWO-SIDED: rnX\' of (0,2) taken from level 1 (d_R - 1) instead of level 2 must be refused -> %s' % plant(
        'PLANT-TWO-SIDED', refuses(ts_check, p4, '2', w1, tag='C-TWO-SIDED')))
    out('C-TRB-SRC: N*_TRB from pk08\'s certified TRB run outputs, N4 %s (%s), N3 %s (%s), each with VERDICT lines exactly [VERDICT '
        'VALID] and one READING line -> %s' % (fstr(G['TRB'][4], 12), sha_file(TRBO[4])[:8], fstr(G['TRB'][3], 12), sha_file(TRBO[3])[:8],
                                               gate('C-TRB-SRC', all(G['TRB'][n] > 0 for n in (4, 3)))))
    t4 = open(TRBO[4]).read()
    pt = [refuses(trb_read, 4, t4 + '\nVERDICT VALID\n', tag='C-TRB-SRC'),
          refuses(trb_read, 4, '\n'.join(ln for ln in t4.split('\n') if not ln.startswith('READING')), tag='C-TRB-SRC')]
    out('PLANT-TRB-SRC: the N4 output with a second VERDICT line, and without its READING line, must each be refused -> %s' % plant(
        'PLANT-TRB-SRC', all(pt)))
    for N in (4, 3):
        p = pcs[N]
        uh = ux_t(N, p)
        tx2 = dict(G['TX'])
        r2 = list(tx2[(N, p['i'])])
        r2[0] = r2[0] + '1'
        tx2[(N, p['i'])] = r2
        out('C-UH-PIECE N=%d piece %d: p_t = (Vt_hi + Ot_hi)^(1/2) <= %s from the t export, its row on the means export\'s grid -> %s' % (
            N, p['i'], fstr(upf(uh), 6), gate('C-UH-PIECE', upf(uh) > 0)))
        out('PLANT-UH-PIECE N=%d: a t-export row whose jlo is not the means export\'s must be refused -> %s' % (
            N, plant('PLANT-UH-PIECE', refuses(ux_t, N, {k: v for k, v in p.items() if k != 'UH'}, tx2, tag='C-UH-PIECE'))))
        uw = [(fam, which) + bond_uw(N, p, fam, which) for fam in ('D3', 'D4', 'D4M') for which in ('e', 'f')]
        okw = all(upf(U) <= lof(W) for (fam, which, U, W) in uw)
        out('C-UE-LE-WE N=%d piece %d: U <= W for both bonds of every class (%s) -> %s' % (N, p['i'], ', '.join(
            '%s %s U %.4f W %.4f' % (fam, which, float(upf(U)), float(upf(W))) for (fam, which, U, W) in uw), gate('C-UE-LE-WE', okw)))


def esemi_base(N, pc, row, cov):
    """the d_L <= 0 base at a row without a pinned E_main record (v1_3_4): mock mode keeps the row's t = 0 harmonic Cov as a labelled
    stand-in; cert mode refuses, since every row needs pk04's record."""
    if MODE == 'mock':
        return cov, 'stand-in:harmonic-Cov(0)'
    raise Refused('C-ESEMI-SRC: no certified E_main record is pinned for this row')


def esemi_base_ok(src, mode):
    """C-ESEMI-BASE: in cert mode the base must be E_semi's certified lower end; the harmonic Cov in that slot is refused."""
    if mode == 'cert' and 'harmonic' in src:
        raise Refused('C-ESEMI-BASE: the harmonic Cov in the base slot (cert mode)')


G = {}


def row_type(N, fam, dL, dR):
    """v1_3_2: N3's D4/D4M (1,1) rows are A2 rows read with the crude cross-term bound (CRUDE11);
    N4's stay wait-W."""
    if (N, fam, dL, dR) in ((4, 'D3', 0, '1'), (4, 'D3', 1, '1')):
        return 'OUT'
    if dL >= 1:
        return 'B3' if fam == 'D3' else ('W' if ((dL, dR) == (1, '1') and not CRUDE11[N]) else 'A2')
    if dL == -1:
        return 'TB' if fam == 'D3' else 'TA'
    return 'TD' if fam == 'D3' else 'TC'


def load_all():
    G['JX'], G['MX'] = export_rows(JX), export_rows(MX)
    G['JXH'], G['MXH'] = kv(JX), kv(MX)
    G['DL'], G['H2'], G['H3'], G['H1'], G['TU'], G['M2B'] = kv(DL1), kv(HS2), kv(HS3), kv(HS1), kv(TAUR), kv(M2B)
    G['UH'] = {N: kv_strict(uhat_path(N)) for N in (4, 3)}
    G['UHL'] = {N: open(uhat_path(N)).read().split('\n') for N in (4, 3)}   # v1_3_2: END must be the last line
    G['ROWSL'] = kv(ROWSF)                                                  # v1_3_2: ROWS_N<N> and COUNT_N<N>
    G['JR'] = {N: G['MXH']['N%d_D3_P%04d' % (N, G['RSTART'][N])].split()[0] + ' inf' for N in (4, 3)}   # v1_3_2: J_RANGE per N
    G['ROWS'], G['COV'], G['COVTAB'] = {}, {}, {}
    for N in (4, 3):
        rows = []
        for r in tsv(R0T[N]):
            dL = int(r['d_L'])
            if dL >= 1:
                rows.append((r['family'], dL, r['d_R']))
                G['COVTAB'][(N, r['family'], dL, r['d_R'])] = float(r['Cov'])
        for r in tsv(TRK[N]):
            key = (r['class'], int(r['d_L']), r['d_R'])
            if key not in rows:
                rows.append(key)
                G['COVTAB'][(N,) + key] = float(r['Cov'])
        G['ROWS'][N] = [{'fam': f, 'dL': dL, 'dR': dR, 'typ': row_type(N, f, dL, dR)} for (f, dL, dR) in rows]
        for x in G['ROWS'][N]:
            G['COV'][(N, x['fam'], x['dL'], x['dR'])] = harm_ball(N, x['fam'], x['dL'], x['dR'])
    ct2 = open(CT2).read()
    mk = re.search(r'^C-KAPPA: .*matrix-tree theorem: N4 (\S+), N3 (\S+);', ct2, re.M)
    G['KAP'] = {4: F(mk.group(1)), 3: F(mk.group(2))}
    G['PHI'] = {n: F(re.search(r'^INFO LEMMA-E N=%d \(Lemma E-prime, MOCK Z ratio\): Phi_eps <= (\S+),' % n, ct2, re.M).group(1))
                for n in (4, 3)}
    if MODE == 'cert':
        st = open(SIGG).read()
        rule_v2(st.split('\n'), where='C-SIGG-SRC')
        for n in (4, 3):
            G['KAP'][n], G['PHI'][n] = sigg_cert(st, n)
    st = open(SIGG).read()   # v1_3_5_4: tau_1's C_N from the certified kappa_max and Phi_eps in both modes
    rule_v2(st.split('\n'), where='C-SIGG-SRC')
    G['MHAT'] = mhat_src(open(MHATO).read(), PINS[M2B])   # v1_3_5_4: m-hat >= 1, on which C_N's step T6 rests (C-MHAT-SRC)
    G['CN'] = {n: cn_ball(*sigg_cert(st, n), m2b_vals(n)[0]) for n in (4, 3)}   # v1_3_5_4: eps_r(300) from M2B
    add10 = open(ADD10P).read()
    G['QTOL'] = {}
    for n, w, pat in ((4, 'D4ML0', r'\| 4 \| D4M-L0 \| (\S+) \|'), (4, 'D4L0', r'\| 4 \| D4-L0 \| (\S+) \|'),
                      (3, 'D4ML0', r'\| 3 \| D4M-L0 \| (\S+) \|'), (3, 'D4L0', r'\| 3 \| D4-L0 \| (\S+) \|')):
        G['QTOL'][(n, w)] = re.search(pat, add10).group(1)
    G['ES'] = es_load_all()   # v1_3_4: the pinned E_main records, through es_check (a refusal stops the run)
    G['TX'] = tx_rows(TX)                         # v1_3_5: pk15's certified t export (C-R4-SRC binds it)
    G['TRB'] = {n: trb_read(n) for n in (4, 3)}   # v1_3_5: N*_TRB from pk08's certified run outputs (C-TRB-SRC)
    G['QEF'] = qef_load()                         # v1_3_5_1: pk02's N*_QE_HI and N*_QF_HI (C-QEF-SRC)


def nhs(N, fam, rhi):
    f_ = G['H2']['N%d_%s_R000' % (N, fam)].split()
    lp = int(G['H2']['LAMBDA_POWER_%s' % fam])
    return (B(f_[6]) * CM.ipow(B(rhi), lp)).sqrt()


def gk(a, b):
    return ('g', min(a, b), max(a, b))


def piece_data(N, i, A):
    r = mod.piece_eval_RB(N, A, i, rows=False)
    if r is None:
        return None
    ch, prm, T, P2row = r['chW'], r['prm'], r['T'], r['P2row']
    K = ch['K']
    al = {d: ch['L'][d][0][1] for d in range(-1, 6)}
    e = {d: CM.norm_up(al[d]) for d in al}
    rn = {d: prm['rn1'][d] for d in al}
    Eg = {k: v for k, v in r['Ech'].items() if isinstance(k, tuple) and len(k) == 3 and k[0] == 'g' and k[1] == 0}
    _k, Vd, Vm, rad = CM.entry_duals(Eg, T)
    kap = [CM._cen(Vd[('g', 0, j)] / Vd[('g', 0, 0)], Vm[('g', 0, j)] / Vm[('g', 0, 0)], rad) for j in range(1, K + 1)]
    Ega = {k: v for k, v in r['Ech'].items() if isinstance(k, tuple) and len(k) == 3 and k[0] == 'g' and k[1] <= K and k[2] <= K}
    Gq, kapm = None, None
    if all(gk(a, b) in Ega for a in range(K + 1) for b in range(K + 1)):
        _k2, _Vd2, Vm2, _r2 = CM.entry_duals(Ega, T)
        g00 = Vm2[gk(0, 0)]
        Gq = [[Vm2[gk(a, b)] / g00 - Vm2[gk(a, 0)] * Vm2[gk(0, b)] / (g00 * g00) for b in range(1, K + 1)] for a in range(1, K + 1)]
        kapm = [Vm2[gk(0, j)] / g00 for j in range(1, K + 1)]
    law = mod.law_at(A, N, P2row['jlo'])
    if law.get('s') in (None, 'inf'):
        return None
    rhi = upf(ONE / ch['lam0'])
    pc = {'i': i, 'jlo': P2row['jlo'], 'jhi': P2row['jhi'], 'T': T, 'K': K, 'al': al, 'e': e, 'rn': rn,
          'Q': {d: e[d] + rn[d] for d in al}, 'efar': prm['Rw'] * CM.ipow(prm['rho1'], FAR_EXP), 'kap': kap, 'g00': ch['g00'], 'C': ch['C'],
          'Rw': prm['Rw'], 'rho1': prm['rho1'],   # v1_3_5_4: S8's R_w and rho1 upper ends, for C-Q-DAMP
          'lam0': ch['lam0'], 'rhi': rhi, 'eps': F(law['eps_r']), 's': F(law['s']), 'Gq': Gq, 'kapm': kapm,
          's8set': r.get('basis'), 'parx': (ch.get('par_exact'), (r.get('chB') or {}).get('par_exact'))}   # v1_3_2
    for fam in WX:
        jr, mr = G['JX'][(N, fam, i)], G['MX'][(N, fam, i)]
        pc[fam] = {'cilo': F(jr[2]), 'pX': F(jr[3]), 'nXS': F(jr[4]), 'E2': F(jr[5]), 'ce': (F(mr[2]), F(mr[3])), 'cf': (F(mr[4]), F(mr[5])),
                   'mcilo': F(mr[6]), 'cihi': F(mr[7]), 'nHS': nhs(N, fam, rhi)}
        pc[fam]['nX'] = bmin(B(pc[fam]['nXS']), pc[fam]['nHS'])
    A_ = F(G['H2']['N%d_A' % N])
    ce, cf = pc['D3']['ce'], pc['D3']['cf']
    pc['F4'] = (A_ + max(abs(ce[0]), abs(ce[1]))) * (A_ + max(abs(cf[0]), abs(cf[1])))
    pc['W'] = bmin(pc['D3']['nHS'], B(pc['F4']))
    return pc


def cv_vec(pc, raw, src='S8:g_j0/g00'):
    centre_coef(src)
    K, sg = pc['K'], pc['g00'].sqrt()
    v = [raw[a + 1] - pc['kap'][a] * raw[0] for a in range(K)]
    return [sg * sum((pc['C'][k][a] * v[a] for a in range(K)), ZERO) for k in range(K)]


def gsolve(M, b):
    n = len(b)
    A_ = [list(M[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(float(A_[r][c].mid())))
        A_[c], A_[p] = A_[p], A_[c]
        for r in range(n):
            if r != c:
                f = A_[r][c] / A_[c][c]
                A_[r] = [A_[r][q] - f * A_[c][q] for q in range(n + 1)]
    return [A_[i][n] / A_[i][i] for i in range(n)]


def cv_check(pc, raw, scale=None):
    """C-CV (kt_p212_cfa_v1 l.282-284): ||C^ v-hat||^2 (the engine's C^ v-hat, centred over the box) against v-hat_c^T Gq^-1
    v-hat_c from the piece's own g entries at the box centre; the two balls must overlap. Returns (ok, relative midpoint gap, relative
    width), or (False, None, None) when the piece's g entries are not all present."""
    if pc['Gq'] is None:
        return False, None, None
    cv = cv_vec(pc, raw)
    if scale is not None:
        cv = [x * B(scale) for x in cv]
    n2 = sum((x * x for x in cv), ZERO)
    K = pc['K']
    vc = [raw[a + 1] - pc['kapm'][a] * raw[0] for a in range(K)]
    x = gsolve(pc['Gq'], vc)
    w = sum((vc[a] * x[a] for a in range(K)), ZERO)
    mw = abs(float(w.mid()))
    return n2.overlaps(w), abs(float(n2.mid()) - float(w.mid())) / mw, (float(n2.rad()) + float(w.rad())) / mw


def tcs_ok(dot, na, qFA):
    """C-T-CS (plan v1 l.67-68): |alpha . C^ v-hat| <= ||alpha||_2 q_FA,hi across inputs (S8's alpha; pk02's v and L0)."""
    return upf(abs(dot)) <= upf(na * qFA)


LEVTREAT = {('D3', 0): 'vac'}   # v1_3_5_2 (Route 1 of the review 90d302d8 sect. 3): the E_main treatment per d_L <= 0 class ('span' when absent)
T0_FRAC = Fraction(1, 1000)   # v1_3_5_2 (the review 90d302d8 sect. 5 NOTE; main): the fixed fraction of R that PLANT-ESEMI-T0-LEVEL's misses exceed


def lev_treat(fam, dL, table=None):
    """v1_3_5_2 (Route 1 of the review RULING_D3_DL0_CHAIN_LEVEL 90d302d8 sect. 3): a d_L <= 0 class's E_main treatment. 'span': the
    main term carries the in-span sum alpha . C^ v-hat[W] at level d_R - 1, the level that X's q and Q1 pair with (the rule since v1_3_4).
    'vac', for D3 at d_L = 0: the window [free | int | int | cp_k] puts cp_k on the observable's own last column, so alpha sits at level
    d_R (sect. 1), where the residual pairs with X_L and X's q and Q1 do not bound it (sect. 2). The main term is then the vacuum term
    alone, and all of Q0 b(d_R - 1) goes into R: q and Q1 multiply sqrt(e_R^2 + rn1_R^2), read at level d_R - 1 (side)."""
    return (LEVTREAT if table is None else table).get((fam, dL), 'span')


def lev_shift_window(fam, dL):
    """v1_3_5_2, C-LEVEL: a d_L <= 0 class's level shift, derived from its window. In the record's orientation the cp column is
    column 0, so the observable's column nearest the right chain is the smallest column its bonds touch (es_bonds, the engine's own
    geometry, which C-ESEMI-BONDS ties to the records' factors). Column 0 (the observable reaches into the cp column: the single trick)
    gives shift 1, alpha at level d_R; column 1 (the cp column is the first column after the observable) gives 0, alpha at d_R - 1."""
    sh, nc = es_shape(fam, dL)
    c_ = min(v // 3 for pair in es_bonds(fam, dL, nc, 'ef') for v in pair)
    if c_ not in (0, 1):
        raise Refused('C-LEVEL: %s at d_L = %d: the observable\'s column nearest the cp column is %d' % (fam, dL, c_))
    return 1 - c_


def level_check(table):
    """v1_3_5_2, C-LEVEL: the engine's treatment table against the pairing that each d_L <= 0 class's window allows. Shift 0 takes
    'span'; shift 1 takes 'vac' (Route 1). Anything else is refused: 'span' at a shift-1 class reads alpha one level short (the v1_3_5_1
    defect), and 'span+1' (alpha, e_R and rn1_R at level d_R with X's q and Q1) is the unsound mix of the sect. 2."""
    need = {0: 'span', 1: 'vac'}
    bad = ['%s d_L %d: table %s, window shift %d needs %s' % (f, d, lev_treat(f, d, table), lev_shift_window(f, d),
                                                            need[lev_shift_window(f, d)])
           for f in ('D3', 'D4', 'D4M') for d in (-1, 0) if lev_treat(f, d, table) != need[lev_shift_window(f, d)]]
    if bad:
        raise Refused('C-LEVEL: %s' % '; '.join(bad))


def side(pc, d):
    """v1_3_2: d = 'far' stands for every finite d >= 7, levels >= 6; efar = Rw_hi rho1_hi^FAR_EXP (FAR_EXP = 7) bounds rn1 and |eps_W|
    there (SPEC_S8_CERT_v1 c0f95398 l.106, l.122-123, l.200: e_d = min(R_w rho1^d, |Q0 l(d-1)|), d = level + 1; C-FAR-CITE
    803aab31 (b)). v1_3_5_2: every d_L <= 0 row reads level d_R - 1 here, D3 at d_L = 0 included (Route 1; lev_treat)."""
    if d == 'inf':
        return ZERO, ZERO
    if d == 'far':
        return pc['efar'], pc['efar']
    lev = int(d) - 1
    return pc['rn'][lev], pc['e'][lev]


def tfa_lo(pc, fam, dL, dR, cv, Tv, qFA, sM):
    """T_FA's lower end; returns (Fraction, (dot, ||alpha||_2) for C-T-CS, or None for 'far' and 'inf')."""
    if fam == 'D4':
        lev = dL - 1
    elif dR == 'inf':
        return Fraction(0), None
    elif dR == 'far':
        return -upf(pc['efar'] * B(qFA)), None
    else:
        lev = int(dR) - 1
    a = pc['al'][lev]
    dot = sum((a[k] * cv[k] for k in range(pc['K'])), ZERO)
    na = CM.norm_up(a)
    x = lof(dot) - upf(na * B(Tv))
    fac = lof(CM.ipow(ONE - B(sM) * B(sM), 2))
    return min(x, fac * x), (dot, na)


LGRID = [Fraction(8 + k, 4) for k in range(313)]


def tail_h1(N, L):
    Lb = B(L)
    if N == 3:
        return (Lb + 1) * (-Lb).exp() / (ONE - arb(-600).exp())
    sq = Lb.sqrt()
    g = sq * (-Lb).exp() + arb.pi().sqrt() / 2 * sq.erfc()
    s300 = arb(300).sqrt()
    low4 = arb.pi().sqrt() / 2 * s300.erf() - s300 * arb(-300).exp()
    return arb(2).sqrt() * (Lb * sq * (-Lb).exp() + B(Fraction(3, 2)) * g) / low4


def sigma_parts(N, pc, qa, eps, s, sp, mode=None, y1=None):
    """v1_3_5_2 (the review RULING_T202_QS_TD_SG1_V2 141eb691 sects. 3-4): the TD single trick's g-term pieces. J-1: the exact side is
    Y_c <= sqrt(E2_t - 2 b_lo^2 + b_hi^2) + (A_N + b_hi) qa, with A_N = (N - 1)/2, [b_lo, b_hi] the means export's ball for t and E2_t the
    upper end of E_Omega[xi_t^2] (no t tail: F4 covers the unbounded t bond). J-2 (C-SG-CENTRE): b_lo >= 0 and L >= c_bb's upper end.
    v1_3_5_4 (J-3 closed by pk15 NOTE_J3_TAIL_ONESIDED_G1_v1 ed0ae46c, Claim T, and the review CHECK_J3_TAIL_ONESIDED_G1
    53ec0d98): the bb tail is Y tau_1(L), tau_1(L) = C_N tail_h1(N, L) (C_N from cn_ball, G['CN']), in place of the coded tau_bb, so the
    joint term is u^2 (eps L Y_c + eps^2 L^2)/(1 - s^2) + Y_c tau_1(L), with L chosen in float on LGRID and evaluated in balls; Claim T's
    step T1 needs c_bb's lower end >= 0 as well (C-SG-CENTRE). C-Q-DAMP: the TD callers pass qa = qw =
    sqrt(R_w e_1) for Y_c's w part and y1 = sqrt(1 + R_w e_3); y1 defaults to sqrt(1 + qa^2). Returns {'sg', 'L', 'tau1', 'Yc', 'Y1', 'u'};
    sp and mode stay for the callers' interface."""
    bl, bh = pc['D3']['ce']
    cl, ch_ = pc['D3']['cf']
    if bl < 0:
        raise Refused('C-SG-CENTRE: the means ball for t has lower end %s below 0' % bl)
    if cl < 0:
        raise Refused('C-SG-CENTRE: the means ball for bb has lower end %s below 0 (Claim T, step T1)' % cl)
    AN = B(Fraction(N - 1, 2))
    yc = (B(pc['D3']['E2']) - 2 * B(bl) * B(bl) + B(bh) * B(bh)).sqrt() + (AN + B(bh)) * qa
    Y1 = (ONE + qa * qa).sqrt() if y1 is None else y1
    u = ONE / (ONE - B(eps))
    CN = B(G['CN'][N])

    def tau1(L):
        return CN * tail_h1(N, L)

    def val(L):
        Lb = B(L)
        return u * u * (B(eps) * Lb * yc + B(eps) * B(eps) * Lb * Lb) / (ONE - B(s) * B(s)) + yc * tau1(L)

    def tail_f(L):
        if N == 3:
            return (L + 1.0) * math.exp(-L) / (1.0 - math.exp(-600.0))
        sq_ = math.sqrt(L)
        low4 = math.sqrt(math.pi) / 2.0 * math.erf(math.sqrt(300.0)) - math.sqrt(300.0) * math.exp(-300.0)
        return math.sqrt(2.0) * (L * sq_ * math.exp(-L) + 1.5 * (sq_ * math.exp(-L) + math.sqrt(math.pi) / 2.0 * math.erfc(sq_))) / low4
    ef, sf, ycf, cnf = float(eps), float(s), fl(yc), float(G['CN'][N])
    uf = 1.0 / (1.0 - ef)
    vf = lambda L: uf * uf * (ef * L * ycf + ef * ef * L * L) / (1.0 - sf * sf) + ycf * cnf * tail_f(L)
    grid = [L for L in LGRID if L >= ch_]
    if not grid:
        raise Refused('C-SG-CENTRE: no L on the grid reaches the upper end %s of c_bb' % ch_)
    best = min(grid, key=lambda L: vf(float(L)))
    return {'sg': val(best), 'L': best, 'tau1': tau1(best), 'Yc': yc, 'Y1': Y1, 'u': u}


def sigma_g(N, pc, qa, eps, s, sp):
    """v1_3_5_2: the joint TD g-term and its L from sigma_parts (J-1, J-2, the TAU1 slot); the callers' interface since v1_3."""
    p_ = sigma_parts(N, pc, qa, eps, s, sp)
    return p_['sg'], p_['L']


def prepare_uhat(N):
    """v1_3_2 (interface v1_4): the record's checks, then the readings: the two L0 windows, route 0 per row of ROWS_N<N>, and B'."""
    d = G['UH'][N]
    eps, sM = m2b_vals(N)
    uhat_check(d, N, G['UHL'][N])
    centres_read(d, G['RSTART'][N], NP - 1)
    rids = G['ROWSL']['ROWS_N%d' % N].split()
    rows_check(N, rids, G['ROWSL'].get('COUNT_N%d' % N))
    G.setdefault('UV', {})[N] = {'sM': sM, 'eps': eps, 'L0': {w: l0_read(d, w, sM, eps) for w in ('D4L0', 'D4ML0')},
                                 'R0': {r: r0_read(d, r, sM, eps) for r in rids}, 'BP': bp_read(d, 3)}


def qb_vals(N):
    f_ = G['H2']['N%d_D3B_R000' % N].split()
    return F(f_[6]), F(f_[7])


THETAS = (Fraction(0), Fraction(1, 6))   # v1_3_1: the claim lo > 0 (theta 0) and the planning level h = 1.2 (theta 1/6, INFO)


def sdiv(num, b):
    """v1_3_1: a lower end of num / b for a positive ball b: over b_hi when num >= 0, over b_lo (when > 0) when num < 0; None when
    b_hi <= 0. v1_3_2: a negative num over a b with b_lo <= 0 has no finite lower end, and sdiv returns NEG_MARKER, a
    marker meaning that no x >= 0 passes."""
    bh = upf(b)
    if bh <= 0:
        return None
    if num >= 0:
        return num / bh
    bl = lof(b)
    return num / bl if bl > 0 else NEG_MARKER


def lin_lo_star(a, b, covhi, theta):
    """B3 and A2, lo = a - b x: the largest x with lo_lo >= theta Cov_hi, on the safe side (v1_3_1: theta 0 or 1/6)."""
    return sdiv(lof(a) - theta * covhi, b)


def lin_star(base, covhi, theta, den, c0, c1):
    """d_L <= 0, lo = base - (c1 x + c0) / den: the largest x with lo_lo >= theta Cov_hi, on the safe side (v1_3_1)."""
    Rmax = lof(base) - theta * covhi
    return sdiv(Rmax * (lof(den) if Rmax >= 0 else upf(den)) - upf(c0), c1)


def tv_star(r, cs, fac):
    """v1_3_1: the largest T_v with r + T_FA_lo(T_v) >= 0, where T_FA_lo = min(x, fac x), x = dot_lo - ||alpha||_2 T_v
    (tfa_lo) and r is the rest of lo_lo less theta Cov_hi; piecewise affine in T_v, so T_v* = (dot_lo + r) / ||alpha|| for r >= 0 and
    (dot_lo + r / fac) / ||alpha|| for r < 0 (0 < fac < 1). None when T_v does not enter (cs is None: D4M (d,far) and (d,inf))."""
    if cs is None:
        return None
    return sdiv(lof(cs[0]) + (r if r >= 0 else r / fac), cs[1])


def eval_rows(N, pc, uv, ov=None):
    """every row at the piece -> [(row, lo ball or None, Cov ball, info)]; ov: plant overrides of single inputs ('centre', 'kind',
    'power', 'plane', 'Q1_dlm1' at d_L = -1; 'q_dl0', 'Q1_dl0', 'es_beta' at d_L = 0, each checked by value after the override)."""
    ov = ov or {}
    res = []
    qL0 = {w: uv['L0'][w]['quse'] for w in ('D4L0', 'D4ML0')}
    R0 = uv['R0']   # v1_3_2: route 0 per row (interface v1_4)
    raw, Tv = uv['BP']
    cv = cv_vec(pc, raw, ov.get('centre', 'S8:g_j0/g00'))
    sM = uv['sM']
    QBC, QBS = qb_vals(N)
    qt = F(G['QTOL'][(N, 'D4L0')])
    for row in G['ROWS'][N]:
        fam, dL, dR, typ = row['fam'], row['dL'], row['dR'], row['typ']
        cov = G['COV'][(N, fam, dL, dR)]
        covhi = upf(cov)
        info = {}
        U = R0[rowid(row)]['use'] if rowid(row) in R0 else None   # v1_3_2: the row's own route-0 block
        if typ == 'A2' and (dL, dR) == (1, '1'):
            info['crude11'] = True
        if typ == 'OUT':
            res.append((row, None, cov, {'mark': 'out'}))
            continue
        if typ in ('B3', 'A2', 'W'):
            rnL, eL = side(pc, str(dL))
            rnR, eR = side(pc, dR)
            nX = pc[fam]['nX']
            cde = nX * (rnL * eR + eL * rnR + rnL * rnR)
            pr = prod_term(N, pc, fam, rnL, eL, rnR, eR, ov.get('prod_scale', 1))   # v1_3_5 (erratum 4f34050b sect. 3): |m_e| |m_f|
            info['prod'] = pr
            P = B(pr[2])
            if typ == 'B3':
                q = B(U)
                lo = B(pc['D3']['cilo']) - ((rnL + rnR) * q + cde) - ((eL + eR) * q + pc['W'] * eL * eR) - P
                info['be'] = [('U_D3', lin_lo_star(B(pc['D3']['cilo']) - cde - pc['W'] * eL * eR - P, rnL + rnR + eL + eR, covhi, th), None,
                               None, None) for th in THETAS]
            else:
                qLf, qRf = (qL0['D4L0'], qL0['D4ML0']) if fam == 'D4' else (qL0['D4ML0'], qL0['D4L0'])
                qL, qR = B(qLf), B(qRf)
                tFB = eR * qR if fam == 'D4' else eL * qL
                tfa, cs = tfa_lo(pc, fam, dL, dR, cv, Tv, qL0['D4L0'], sM)
                lo = B(pc[fam]['cilo']) + B(tfa) - tFB - (rnL * qL + rnR * qR + cde) - nX * eL * eR - P
                info['tfa'], info['cs'] = tfa, cs
                if typ == 'W':
                    info['mark'] = 'wait-W'
                else:
                    base = B(pc[fam]['cilo']) - cde - nX * eL * eR - P
                    rest = B(pc[fam]['cilo']) - tFB - (rnL * qL + rnR * qR + cde) - nX * eL * eR - P
                    fac = lof(CM.ipow(ONE - B(sM) * B(sM), 2))
                    info['be'] = []
                    for th in THETAS:
                        tvs = tv_star(lof(rest) - th * covhi, cs, fac)
                        if fam == 'D4':
                            bb = eR + rnR
                            xs = lin_lo_star(base + B(tfa) - rnL * qL, bb, covhi, th)
                            if xs is None:
                                info['be'].append(('D4L0', lin_lo_star(base + B(tfa), rnL, covhi, th), None, None, tvs))
                            else:
                                info['be'].append(('D4ML0', xs, lin_lo_star(base + B(tfa) - rnL * B(qt), bb, covhi, th),
                                                   lin_lo_star(base + B(tfa) - bb * qR, rnL, covhi, th), tvs))
                        else:
                            tfat = tfa_lo(pc, fam, dL, dR, cv, Tv, qt, sM)[0] if dR == 'far' else tfa
                            bb = eL + rnL
                            if dR == 'inf':
                                alt = None
                            elif dR == 'far':
                                alt = lin_lo_star(base - bb * qL, rnR + pc['efar'], covhi, th)
                            else:
                                alt = lin_lo_star(base + B(tfa) - bb * qL, rnR, covhi, th)
                            info['be'].append(('D4ML0', lin_lo_star(base + B(tfa) - rnR * qR, bb, covhi, th),
                                               lin_lo_star(base + B(tfat) - rnR * B(qt), bb, covhi, th), alt, tvs))
        else:
            rnR, _x = side(pc, dR)
            Qa = pc['Q'][-1]
            eps, s = pc['eps'], pc['s']
            sp = s * (1 + s)
            beta, cih, nX = False, None, pc[fam]['nX']
            if typ in ('TA', 'TB'):
                kind = ov.get('kind', KIND[fam])
                Es_, Qh, Q1h = dl1_vals(G['DL'], N, fam, kind)
                q_hi_power(kind, ov.get('power', 0))
                lev = ov.get('plane', WX[fam] - 2)
                q1_plane(fam, lev)
                Q1 = ov.get('Q1_dlm1', bmin(B(Q1h), pc['Q'][lev]))
                q = bmin(B(QBC), B(U) + B(QBS)) if typ == 'TB' else B(Qh)
                Es = B(Es_)
                info['Q1'] = (Q1h, upf(pc['Q'][lev]))
            else:
                Uw = B(U) if typ == 'TD' else B(qL0['D4ML0' if fam == 'D4' else 'D4L0'])
                q_exp = q_dl0(N, pc, fam, Uw, nX, Qa)   # v1_3_5_4: the damped q for D3 and D4M (C-Q-DAMP); D4 keeps U + nX Qa
                q = ov.get('q_dl0', q_exp)
                if not same_ball(q, q_exp):
                    raise Refused('C-DL0-NO-QHI: the d_L = 0 q of %s (0,%s) is not the C-Q-DAMP form' % (fam, dR))
                dq = q_damp(pc) if typ == 'TD' else None
                Q1x = dq['e3'] if typ == 'TD' else pc['Q'][-1]   # v1_3_5_4: D3's Q1 = ||eps_3|| <= e_3 (X_1 = T^3/lambda_0^3)
                Q1 = ov.get('Q1_dl0', Q1x)
                if not same_ball(Q1, Q1x):
                    raise Refused('C-DL0-Q1: the d_L = 0 Q1 of %s (0,%s) is not %s' % (fam, dR, 'e_3' if typ == 'TD' else 'the piece\'s Qa'))
                info['qd'] = (float(upf(q)), float(upf(Uw + nX * Qa)))   # v1_3_5_4: q with and without the damping (INFO)
                if typ == 'TD' and (N, dR) == (3, '1'):
                    esemi_form(N, fam, dR, ov.get('form', 'beta'))
                    m_ = pc['D3']
                    cih = m_['cihi'] if m_['mcilo'] > 0 else max(abs(m_['mcilo']), m_['cihi'])
                    es_exp = B(cih) + Qa * B(U)
                    Es = ov.get('es_beta', es_exp)
                    if not same_ball(Es, es_exp):
                        raise Refused('C-ESEMI-FORM: beta\'s E_semi of N3 D3 (0,1) is not Cov_inf_hi + Qa U from the means export')
                    info['beta'] = (m_['mcilo'] > 0, cih)
                    beta = True
                else:
                    esemi_form(N, fam, dR, ov.get('form', 'alpha'))
                    xop = bmin(B(pc['F4']), pc['D3']['nHS']) if typ == 'TD' else pc[fam]['nHS']
                    Es = xop * (ONE + Qa * Qa).sqrt()
            spb = B(sp)
            dtr = spb * Q1 + spb * spb   # v1_3_2: the trick's relative error on D
            sgt = ZERO
            sgp = None
            if typ == 'TD':
                sgp = sigma_parts(N, pc, dq['qw'], eps, s, sp, y1=dq['y1'])   # v1_3_5_4: Y_c's w part and Y_1 damped (C-Q-DAMP)
                sg, Lg = sgp['sg'], sgp['L']
                u = ONE / (ONE - B(eps))
                dtr = dtr + u * u * B(eps) * dq['y1']   # v1_3_5_4: Y_1 = sqrt(1 + R_w e_3)
                sgt = sg
                info['sg'] = (fl(sg), float(Lg))
            esr = es_rows(N, pc).get((fam, dL))   # v1_3_4: the row's E_main record, when one is pinned
            rnX = rnR
            tsd = None   # v1_3_5_5: (X term, X part) of a two-sided Route 1 row, for its break-even
            if esr is not None:
                # v1_3_5_2: R_X in D_u units. F-A: the s'^2/2 term reads Es_alpha, the row's pre-E_main bound
                # of the true-vacuum window (the alpha form at d_L = 0, the beta form at N3 D3 (0,1), the record's N*_E_SEMI_HI at
                # d_L = -1). F-B: D_m/D_u lies in [1 - dtr - Q1 e_R, 1 + dtr + Q1 e_R], so nc and nd carry k = 1 + dtr + Q1 e_R and the
                # denominator is 1 - 2 dtr - Q1 (e_R + rn1_R) - nd k, with e_R = 0 where D_m is the vacuum term ('far', 'inf', 'vac').
                # v1_3_5_2 (Route 1 of the review RULING_D3_DL0_CHAIN_LEVEL 90d302d8 sect. 3; C-LEVEL): at a 'vac' class (D3 at
                # d_L = 0) E_X, m_e and m_f are the vacuum term alone (es_row's 'inf' reading, the cv0 form, so nc = nd = 0), and all of
                # Q0 b(d_R - 1) goes into R: rn1_R becomes sqrt(e_R^2 + rn1_R^2) at level d_R - 1 in every term of R_X, R_e and R_f
                # ('far': e_R = rn1_R = efar; 'inf': 0).
                tr = lev_treat(fam, dL)
                if tr == 'vac':
                    em = es_row(esr[0], pc, 'inf')
                    rnX, eR = CM.sqrt_up(_x * _x + rnR * rnR), ZERO
                    sq2 = CM.sqrt_up(rnX * rnx2(pc, dR))   # v1_3_5_5: (rnX rnX')^(1/2), Z* at both ends (83db00da; C-TWO-SIDED)
                elif tr == 'span':
                    em = es_row(esr[0], pc, dR)
                    eR = ZERO if dR in ('far', 'inf') else _x
                else:
                    raise Refused('C-LEVEL: %s at d_L = %d has the treatment %r' % (fam, dL, tr))
                Esa = Es
                info['es'] = (em, upf(Esa), esr[1], es_ref(MODE))
                Es = B(upf(abs(em['ex'])))   # v1_3_4: |E| in R_X is the upper end of |E_X|, the ball that R_X bounds (2414bd75)
                k_ = ONE + dtr + Q1 * eR
                ndk = em['nd'] * k_
                den = ONE - 2 * dtr - Q1 * (eR + rnX) - ndk
                den_pos(den)
                base = em['cm']
                bsrc = ('Cov_vac:%s (Route 1, sqrt(e_R^2 + rn1_R^2) %.3e)' % (esr[1], float(upf(rnX)))) if tr == 'vac' else 'Cov_main:%s' % esr[1]
                beta = False
                c0 = em['nc'] * k_ + spb * spb / 2 * Esa + sgt + Es * (Q1 * rnX + ndk + dtr)
                if tr == 'vac':
                    # v1_3_5_5: the N-error q rnX becomes
                    # min(U rnX, F4 (rnX rnX')^(1/2)) + min(F4 qw (rnX rnX')^(1/2), nX R_w rnX); D's error stays Q1 rnX
                    xt = bmin(B(pc['F4']) * dq['qw'] * sq2, nX * dq['Rw'] * rnX)
                    ner = bmin(Uw * rnX, B(pc['F4']) * sq2) + xt
                    tsd = (xt, q - Uw)
                    bsrc = bsrc + ' (two-sided: rnX\' %.3e, N-error %.3e for q rnX %.3e)' % (float(upf(rnx2(pc, dR))), float(upf(ner)),
                                                                                             float(upf(q * rnX)))
                else:
                    ner = q * rnX
                Rx = (ner + spb * q + c0) / den
                rr = []
                for which, mk, nk in (('e', 'me', 'nce'), ('f', 'mf', 'ncf')):
                    qb = q_single(N, pc, fam, dL, which, Qa, ov)
                    mb_ = B(upf(abs(em[mk])))
                    Ub, Wb = bond_uw(N, pc, fam, which)
                    Tb = spb * qb + spb * spb / 2 * Wb * (ONE + Qa * Qa).sqrt() + sg_single(typ, which, sgp, Qa, eps, s) + mb_ * dtr
                    # v1_3_5_5 (83db00da): at the two-sided rows the single bonds take the same step, W_H for F4 and U_b for U, t and bb
                    nb = (bmin(Ub * rnX, Wb * sq2) + bmin(Wb * dq['qw'] * sq2, Wb * dq['Rw'] * rnX)) if tr == 'vac' else qb * rnX
                    rr.append((nb + em[nk] * k_ + mb_ * (Q1 * rnX + ndk) + Tb) / den)
                ext = B(upf(abs(em['me']))) * rr[1] + B(upf(abs(em['mf']))) * rr[0] + rr[0] * rr[1]
                info['Ref'] = (rr[0], rr[1], Rx, '; '.join(es_standins(dL, typ)) or 'none')
                info['FB'] = (float(upf(k_)), float(lof(den)))
            else:
                base, bsrc = esemi_base(N, pc, row, cov)
                den = ONE - Q1 * rnR - dtr
                den_pos(den)
                c0 = Es * Q1 * rnR + spb * spb / 2 * Es + sgt + Es * dtr
                Rx = ((rnR + spb) * q + c0) / den
                ext = ZERO
            esemi_base_ok(bsrc, MODE)
            base = esemi_transfer(base)
            info['base'] = bsrc
            info['R'] = Rx + ext
            lo = base - Rx - ext
            bbase = base - ext   # v1_3_5: R_e and R_f do not depend on the break-even's variable
            info['be'] = []
            for th in THETAS:
                if typ == 'TB':
                    qs = lin_star(bbase, covhi, th, den, c0, rnX + spb)
                    info['be'].append(('U_D3', None if (qs is None or qs >= QBC) else qs - QBS, None, None, None))
                elif typ in ('TC', 'TD'):
                    if beta:   # v1_3_5_5: the X part is the row's own q - U (damped at D3)
                        Kc = Q1 * rnX + spb * spb / 2 + dtr
                        xs = lin_star(bbase, covhi, th, den, (rnX + spb) * (q - Uw) + Kc * B(cih) + sgt, (rnX + spb) + Kc * Qa)
                    elif tsd is not None:   # v1_3_5_5: lo is linear in U while U rnX is the smaller term of the two-sided N-error
                        xs = lin_star(bbase, covhi, th, den, tsd[0] + spb * tsd[1] + c0, rnX + spb)
                    else:   # v1_3_5_5 (INFO fix): subtract the row's own X part q - U, the damped one at D3 and D4M
                        qs = lin_star(bbase, covhi, th, den, c0, rnX + spb)
                        xs = None if qs is None else qs - upf(q - Uw)
                    var = 'U_D3' if typ == 'TD' else ('D4ML0' if fam == 'D4' else 'D4L0')
                    info['be'].append((var, xs, xs if var == 'D4ML0' else None, None, None))
            if not info['be']:
                del info['be']
        res.append((row, lo, cov, info))
    return res


def judge(lo, cov):
    """v1_3_1 (the claim rule, 19:41Z): pass iff lo_lo > 0; the headroom Cov/(Cov - lo) is INFO (no Cov/2 threshold)."""
    if lo is None or not (math.isfinite(float(lo.mid())) and math.isfinite(float(lo.rad()))):
        return False, 0.0, None, None
    ll, ch_ = lof(lo), upf(cov)
    ok = ll > 0
    cm = float(cov.mid())
    h = (cm / (cm - float(ll)) if cm - float(ll) > 0 else float('inf')) if ll > 0 else 0.0
    return ok, h, ll, ch_


def margin_of(j):
    """v1_3_1: the claim's quantity lo_lo / Cov_hi from a judge() tuple (an INFO float; the decision is lo_lo > 0, exactly); inf when
    lo is absent."""
    return float(j[2] / j[3]) if (j[2] is not None and j[3] is not None and j[3] > 0) else float('inf')


def rname(row):
    return '%s (%d,%s)' % (row['fam'], row['dL'], row['dR'])


def box_f4(N):
    f_ = G['H2']['N%d_D3_R000' % N].split()
    A_ = F(G['H2']['N%d_A' % N])
    return (A_ + max(abs(F(f_[2])), abs(F(f_[3])))) * (A_ + max(abs(F(f_[4])), abs(F(f_[5]))))


def piece_gates(N, pc):
    """the per-piece gates: C-LAMBDA-R, C-HS-CBOX, C-HS-J, C-UD3-PIECE, C-F4 (v1_3), C-CV (v1_3) and C-S8-PAREXACT (v1_3_2
    both of S8's chains parity-exact, as S8 requires of a set, kt_s8_cert_v1_14_3 l.2223)."""
    bad = []
    if not (pc['rhi'] <= F(G['DL']['N%d_LAMBDA_RATIO_HI' % N])):
        bad.append('C-LAMBDA-R')
    for fam, key in (('D3', 'D3'), ('D3', 'D3B'), ('D4', 'D4'), ('D4M', 'D4M')):
        f_ = G['H2']['N%d_%s_R000' % (N, key)].split()
        ce, cf = pc[fam]['ce'], pc[fam]['cf']
        if not (F(f_[2]) <= ce[0] and ce[1] <= F(f_[3]) and F(f_[4]) <= cf[0] and cf[1] <= F(f_[5])):
            bad.append('C-HS-CBOX %s' % key)
    if F(pc['jlo']) < 300:
        bad.append('C-HS-J')
    try:
        piece_in_range(G['UH'][N], pc['jlo'], pc['jhi'])
    except Refused:
        bad.append('C-UD3-PIECE')
    if not (pc['F4'] <= box_f4(N)):
        bad.append('C-F4')
    okc, _rm, _rw = cv_check(pc, G['UV'][N]['BP'][0])
    if not okc:
        bad.append('C-CV')
    px = pc.get('parx') or (None, None)
    if not (px[0] is True and px[1] is True):
        bad.append('C-S8-PAREXACT')
    return bad


def eval_piece(N, i, A):
    pc = piece_data(N, i, A)
    if pc is None:
        return None, [], [], [], ['S8 returned None (no law, or no basis set with tau_B > 0)']
    bad = piece_gates(N, pc)
    try:
        rows = eval_rows(N, pc, G['UV'][N])
    except Refused as ex:
        return pc, [], [], bad, ['a reader refused at the piece: %s' % ex]
    jd = [judge(lo, cov) for (row, lo, cov, info) in rows]
    kills = ['%s lo is not finite' % rname(r[0]) for r, j in zip(rows, jd) if r[1] is not None and j[2] is None]
    qFA = B(G['UV'][N]['L0']['D4L0']['quse'])
    for (row, lo, cov, info) in rows:
        if info.get('cs') is not None and not tcs_ok(info['cs'][0], info['cs'][1], qFA):
            bad.append('C-T-CS %s' % rname(row))
    return pc, rows, jd, bad, kills


def mark_of(row, ok, info):
    if row['typ'] == 'OUT':
        return 'out'
    if row['typ'] == 'W':
        return 'wait-W'
    return 'pass' if ok else 'fail'


def piece_report(N, i, ev):
    pc, rows, jd, bad, kills = ev
    if kills:
        for k in kills:
            out('KILL N=%d i=%d: %s' % (N, i, k))
    if pc is None or not rows:
        out('PIECE N=%d i=%d ok=0: no rows (%s); gates failing %s' % (N, i, '; '.join(kills), bad or 'none'))
        for b in bad:
            fails.append(b)
        return {}
    res, cnt, worst, wmg, failing = {}, {'pass': 0, 'fail': 0, 'wait-W': 0, 'out': 0}, (float('inf'), ''), (float('inf'), ''), []
    for (row, lo, cov, info), j in zip(rows, jd):
        ok, h = j[0], j[1]
        mg = margin_of(j)
        mk = mark_of(row, ok, info)
        cnt[mk] += 1
        res[rname(row)] = (h, mk, row['typ'], info.get('be'), mg)
        if mk in ('pass', 'fail') and h < worst[0]:
            worst = (h, rname(row))
        if mk in ('pass', 'fail') and mg < wmg[0]:
            wmg = (mg, rname(row))
        if mk == 'fail':
            failing.append('%s %.4g' % (rname(row), mg))
    for b in bad:
        fails.append(b)
    out('PIECE N=%d i=%d ok=%d: J [%s, %s]; rows %d: pass %d, fail %d, wait-W %d, out %d; min lo_lo/Cov_hi %.6g at %s; min headroom %.6g '
        'at %s; r %.8f; S8 set %s; fails (lo_lo/Cov_hi) %s; gates failing %s' % (
            N, i, int(not bad and not kills), pc['jlo'], pc['jhi'], len(rows), cnt['pass'], cnt['fail'], cnt['wait-W'], cnt['out'], wmg[0],
            wmg[1], worst[0], worst[1], float(pc['rhi']), pc.get('s8set'), failing[:12] or 'none', bad or 'none'))
    return res


def flr(x, k=6):
    if x is None:
        return 'inf'
    x = Fraction(x)
    if x == 0:
        return '0'
    a = abs(x)
    e = 0
    while a >= 10:
        a /= 10
        e += 1
    while a < 1:
        a *= 10
        e -= 1
    y = a * 10 ** (k - 1)
    if x > 0:
        return '%de%d' % (y.numerator // y.denominator, e - k + 1)
    return '-%de%d' % (-(-y.numerator // y.denominator), e - k + 1)


def be_merge(cur, x, i):
    if x is None:
        return cur
    if cur is None or x < cur[0]:
        return (x, i)
    return cur


def be_acc(cur, b, i):
    """v1_3_1: merge one piece's (var, rec, tol, alt, tv) into the running minima, each (x, piece) or None."""
    cur = cur or (b[0], None, None, None, None)
    return (b[0],) + tuple(be_merge(cur[k], b[k], i) for k in (1, 2, 3, 4))


def be_str(bv):
    f_ = lambda x: ('%s@%d' % (flr(x[0]), x[1])) if x else 'inf'
    return '%s rec %s tol %s alt %s tv %s' % (bv[0], f_(bv[1]), f_(bv[2]), f_(bv[3]), f_(bv[4]))


def rowmin_lines(N, acc, beacc):
    for nm in sorted(acc):
        h, i, mk_all, typ, mg, im = acc[nm]
        bv = beacc.get(nm)
        bs = ('; be %s; be12 %s' % (be_str(bv[0]), be_str(bv[1]))) if bv is not None else ''
        out('ROWMIN N=%d %s %s: min lo_lo/Cov_hi %.9g at piece %d; min headroom %.9g at piece %d; marks %s%s' % (
            N, nm, typ, mg, im, h, i, ','.join(sorted(mk_all)), bs))


def run_pieces(N, A, pieces):
    acc, beacc = {}, {}
    t0 = cpu()
    for i in pieces:
        ev = eval_piece(N, i, A)
        res = piece_report(N, i, ev)
        for nm, (h, mk, typ, be, mg) in res.items():
            c = acc.setdefault(nm, [h, i, set(), typ, mg, i])
            if h < c[0]:
                c[0], c[1] = h, i
            if mg < c[4]:
                c[4], c[5] = mg, i
            c[2].add(mk)
            if be is not None:
                cur = beacc.get(nm, [None] * len(be))
                beacc[nm] = [be_acc(c_, b_, i) for c_, b_ in zip(cur, be)]
    rowmin_lines(N, acc, beacc)
    out('PIECES N=%d: %d evaluated, cpu %.1f s' % (N, len(pieces), cpu() - t0))
    return acc


def fstr(x, k=30):
    x = Fraction(x)
    if x == 0:
        return '0'
    sgn = '-' if x < 0 else ''
    x = abs(x)
    e = 0
    while x >= 10:
        x /= 10
        e += 1
    while x < 1:
        x *= 10
        e -= 1
    n = round(x * 10 ** (k - 1))
    return '%s%de%d' % (sgn, n, e - k + 1)


def inputs_digest():
    lines_ = ['S8 %s' % mod.A_DIGEST[0]] + ['%s %s' % (os.path.relpath(p, CODEDIR), PINS[p]) for p in sorted(PINS)] + \
             ['UHAT %d %s' % (n, sha_file(uhat_path(n))) for n in (4, 3)]
    return hashlib.sha256('\n'.join(lines_).encode('utf-8')).hexdigest()


def pre_inputs():
    tcount = {}
    for N in (4, 3):
        for r in G['ROWS'][N]:
            tcount[(N, r['typ'])] = tcount.get((N, r['typ']), 0) + 1
    ok = (len(G['ROWS'][4]) == 104 and len(G['ROWS'][3]) == 86
          and all((N, f, i) in G['JX'] and (N, f, i) in G['MX'] for N in (4, 3) for f in WX for i in range(NP)))
    out('C-INPUTS: rows N4 %d, N3 %d; by type %s; both exports hold every piece 0..903 of D3, D4, D4M at both N -> %s' % (
        len(G['ROWS'][4]), len(G['ROWS'][3]), ', '.join('N%d %s %d' % (k[0], k[1], v) for k, v in sorted(tcount.items())), gate('C-INPUTS', ok)))
    rel = max(abs(fl(G['COV'][k]) - G['COVTAB'][k]) / G['COVTAB'][k] for k in G['COV'])
    out('C-COV: the strip formula in balls against the tables\' Cov over %d rows: largest relative difference %.2e (tolerance 1e-3); the '
        '64-column far/inf rows carry R_TRUNC %s (proof the review 1920fa90 (1)) -> %s' % (
            len(G['COV']), rel, fstr(R_TRUNC, 2), gate('C-COV', rel <= 1e-3)))
    r4 = open(R4OUT).read().split('\n')
    G['TXH'] = kv(TX)
    okr = (not refuses(rule_v2, r4) and all(any(PINS[p] in ln for ln in r4 if ln.startswith('EXPORT')) for p in (JX, MX, TX))
           and all(h.get('EXPORT_STATUS') == 'CERTIFIED' and h.get('RUN_VERDICT') == 'VALID' and h.get('FORMAT') == 'S4U_KV_v1'
                   for h in (G['JXH'], G['MXH'], G['TXH'])) and G['TXH'].get('FIELDS', '').split()[3:5] == ['Vt_hi', 'Ot_hi'])
    out('C-R4-SRC: the joint, means and (v1_3_5) t exports CERTIFIED, RUN_VERDICT VALID, FORMAT S4U_KV_v1, named by full sha256 on EXPORT '
        'lines of their run output, whose VERDICT lines are exactly [VERDICT VALID] (rule V2); the t export\'s FIELDS hold Vt_hi '
        'and Ot_hi fourth and fifth -> %s' % gate('C-R4-SRC', okr))

    def cov_mismatch(Jr, Mr):
        return sorted(k for k in set(Jr) | set(Mr) if k not in Jr or k not in Mr or Jr[k][2] != Mr[k][6])
    mm = cov_mismatch(G['JX'], G['MX'])
    out('C-COV-MATCH: the means export\'s Cov_inf_lo equals the joint export\'s on %d rows: differing %s -> %s' % (
        len(G['JX']), mm[:3] or 'none', gate('C-COV-MATCH', not mm)))
    k0 = sorted(G['MX'])[0]
    M2 = dict(G['MX'])
    s_ = M2[k0][6]
    mant, ex_ = (s_.split('e') + [''])[:2]
    s2 = mant[:-1] + ('1' if mant[-1] != '1' else '2') + (('e' + ex_) if ex_ else '')
    M2[k0] = M2[k0][:6] + [s2] + M2[k0][7:]
    out('PLANT-COV-MATCH: one decimal changed in its last digit must be refused -> %s' % plant('PLANT-COV-MATCH', bool(cov_mismatch(G['JX'], M2))))
    cc = G['MXH'].get('COV_CENTRING', '')
    out('C-COV-CENTRING: COV_CENTRING %s -> %s' % (cc[:40], gate('C-COV-CENTRING', cc.startswith('TRUE_BULK_MEANS'))))
    ok_min, info = True, []
    for N in (4, 3):
        for fam in WX:
            coef = F(G['H2']['N%d_%s_R000' % (N, fam)].split()[6])
            nmin = min(F(G['JX'][(N, fam, i)][4]) for i in range(NP))
            ok_min = ok_min and nmin * nmin <= coef
            info.append('N%d %s %.6f <= %.6f' % (N, fam, float(nmin), math.sqrt(float(coef))))
    out('C-HS-MIN (as kt_p212_joint_v1_2): the smallest normX_S over all export pieces at most normX_HS at r = 1 (%s) -> %s' % (
        '; '.join(info), gate('C-HS-MIN', ok_min)))
    fexp = {('JX', 'FIELDS'): 'jlo jhi Cov_inf_lo pX_hi normX_hi E2_hi ROUTE',
            ('MX', 'FIELDS'): 'jlo jhi ce_lo ce_hi cf_lo cf_hi Cov_inf_lo Cov_inf_hi',
            ('H2', 'FIELDS'): 'jlo jhi ce_lo ce_hi cf_lo cf_hi COEF',
            ('H2', 'FIELDS_D3B'): 'jlo jhi ce_lo ce_hi cf_lo cf_hi QB_CRUDE QB_SLOPE',
            ('H3', 'FIELDS_D4A'): 'jlo jhi ce_lo ce_hi cf_lo cf_hi QA_CRUDE',
            ('H3', 'FIELDS_D4MA'): 'jlo jhi ce_lo ce_hi cf_lo cf_hi QA_CRUDE'}
    fsrc = {'JX': G['JXH'], 'MX': G['MXH'], 'H2': G['H2'], 'H3': G['H3']}
    def fields_bad(fs):
        return ['%s %s' % k for k, v in sorted(fexp.items()) if fs[k[0]].get(k[1]) != v]
    badf = fields_bad(fsrc)
    boxes = all(G['H3']['N%d_%s_R000' % (N, a)].split()[2:6] == G['H2']['N%d_%s_R000' % (N, b)].split()[2:6]
                for N in (4, 3) for a, b in (('D4A', 'D4'), ('D4MA', 'D4M')))
    out('C-FIELDS (v1_3_2): the FIELDS lines of both exports, of HS v2 (FIELDS, FIELDS_D3B) and of HS v3 (FIELDS_D4A, '
        'FIELDS_D4MA) name the positions the engine reads (differing %s); v3\'s D4A and D4MA boxes equal v2\'s D4 and D4M boxes at both N '
        '(%s) -> %s' % (badf or 'none', boxes, gate('C-FIELDS', not badf and boxes)))
    swap = dict(fsrc, JX=dict(fsrc['JX'], FIELDS='jlo jhi pX_hi Cov_inf_lo normX_hi E2_hi ROUTE'))
    out('PLANT-FIELDS: the joint export with two FIELDS names swapped must fail C-FIELDS -> %s' % plant(
        'PLANT-FIELDS', 'JX FIELDS' in fields_bad(swap)))
    sl = open(SPECS8).read().split('\n')
    cites = ((106, 'eps_d = S^d Q0 w-hat, with |eps_0| = R_w'), (123, 'e_R = R_w rho1^{d_R}'), (200, 'e_d = min(R_w rho1^d, |Q0 l(d-1)|'))
    okc = all(len(sl) >= n and t in sl[n - 1] for n, t in cites) and FAR_EXP == 6 + 1
    out('C-FAR-CITE (v1_3_2, the review 803aab31 (b)): SPEC_S8_CERT_v1 (c0f95398) l.106, l.123 and l.200 state S8\'s tail at distance d as '
        'R_w rho1^d (d = level + 1), and the engine\'s far exponent FAR_EXP = %d is level 6 + 1 -> %s' % (FAR_EXP, gate('C-FAR-CITE', okc)))


def pre_hs():
    H1, H2, H3, TU = G['H1'], G['H2'], G['H3'], G['TU']
    ok = all(H.get('RECORD') == 'HS_INV_NORMX_v1' and H.get('FORMAT') == 'S4U_KV_v1' and H.get('EXPORT_STATUS') == 'CERTIFIED' for H in (H2, H3))
    out('C-HS-SRC: v2 and v3 RECORD HS_INV_NORMX_v1, FORMAT S4U_KV_v1, CERTIFIED -> %s' % gate('C-HS-SRC', ok))
    d3k = sorted(k for k in H1 if re.match(r'^N[34]_D3_', k))
    diff3 = [k for k in d3k if H2.get(k) != H1[k]]
    out('C-HS-D3-SAME: %d N*_D3_* keys of v1 against v2: differing %s -> %s' % (len(d3k), diff3 or 'none', gate('C-HS-D3-SAME', bool(d3k) and not diff3)))
    v2s = [k for k in H2 if k not in ('CODE', 'END') and H3.get(k) != H2[k]]
    out('C-HS-V2-SAME: every key of v2 but CODE and END unchanged in v3: differing %s -> %s' % (v2s[:4] or 'none', gate('C-HS-V2-SAME', not v2s)))
    okn = (H2.get('LEMMA_NOTE_D3B') == 'pk08/HS_TYPEB_LEMMA_NOTE_v1_1.md:' + PINS[NOTEB]
           and H3.get('LEMMA_NOTE_D4A') == H3.get('LEMMA_NOTE_D4MA') == 'pk08/HS_TYPEB_LEMMA_NOTE_v1_1_ADD1.md:' + PINS[NOTEA])
    out('C-HS-NOTE: the lemma notes named by full sha256 -> %s' % gate('C-HS-NOTE', okn))
    specs = {'D3B': (ADD21, H2), 'D4A': (ADD3S, H3), 'D4MA': (ADD3S, H3)}
    opok, plok = True, True
    for kd, (sp_, H) in specs.items():
        lines_ = [ln for ln in open(sp_).read().split('\n') if ln.startswith('OPERATOR_%s = X = ' % kd)]
        op = 'OPERATOR_%s = %s' % (kd, H.get('OPERATOR_%s' % kd, ''))
        opok = opok and len(lines_) == 1 and op == lines_[0]
        bad_op = op[:40] + ('x' if op[40] != 'x' else 'y') + op[41:]
        plok = plok and bool(lines_) and bad_op != lines_[0]
    out('C-HS-OP: the three operator strings symbol by symbol -> %s' % gate('C-HS-OP', opok))
    out('PLANT-HS-OP: one character changed must fail -> %s' % plant('PLANT-HS-OP', plok))
    okl = H2.get('LAMBDA_POWER_D3B') == '0' and H3.get('LAMBDA_POWER_D4A') == '0' and H3.get('LAMBDA_POWER_D4MA') == '1/2'
    out('C-HS-LAMBDA: LAMBDA_POWER_D3B, _D4A, _D4MA = 0, 0, 1/2 -> %s' % gate('C-HS-LAMBDA', okl))
    out('PLANT-HS-LAMBDA: a D4MA row read with LAMBDA_POWER_D4MA = 0 must be refused -> %s' % plant(
        'PLANT-HS-LAMBDA', refuses(v3_power, H3, 'D4MA', 0, tag='QA_CRUDE')))
    okj, okt, okb, oka, okc = True, True, True, True, True
    for N in (4, 3):
        for kd, H in (('D3', H2), ('D3B', H2), ('D4', H2), ('D4M', H2), ('D4A', H3), ('D4MA', H3)):
            f_ = H.get('N%d_%s_R000' % (N, kd), '').split()
            okj = okj and H.get('N%d_%s_METHOD' % (N, kd)) == 'LEMMA' and H.get('N%d_%s_ROWS' % (N, kd)) == '1' and f_[:2] == ['300', 'inf']
        tau = F(H2['N%d_TAU_HI' % N])
        okt = okt and H2.get('TAU_SOURCE') == 'pk08/out/TAU_D3B_v1.kv:' + PINS[TAUR] and tau == F(TU['N%d_TAU_HI' % N])
        A_ = F(H2['N%d_A' % N])
        b = H2['N%d_D3B_R000' % N].split()
        ct, cb = max(abs(F(b[2])), abs(F(b[3]))), max(abs(F(b[4])), abs(F(b[5])))
        qbc, qbs = F(b[6]), F(b[7])
        okb = okb and qbc * qbc >= (A_ + ct) ** 2 * (A_ + cb) ** 2 * (1 + tau * tau) and qbs >= (A_ + ct) * (A_ + cb) * tau
        a4, m4 = H3['N%d_D4A_R000' % N].split(), H3['N%d_D4MA_R000' % N].split()
        A2, A0 = F(H2['N%d_A2' % N]), F(H2['N%d_A0_HI' % N])
        oka = (oka and F(a4[6]) ** 2 >= (A_ + F(a4[3])) ** 2 * (1 + tau * tau) * ((A_ - F(a4[4])) ** 2 + A_ * A_)
               and F(m4[6]) ** 2 >= (A_ + F(m4[3])) ** 2 * (1 + tau * tau) * (A2 + F(m4[5]) ** 2 * A0))
        okc = okc and F(a4[5]) <= A_ and F(m4[4]) >= 0 and F(a4[2]) >= 0 and F(m4[2]) >= 0
    out('C-HS-J: every row METHOD LEMMA, ROWS 1, J range [300, inf) -> %s' % gate('C-HS-J', okj))
    out('C-HS-TAU: TAU_SOURCE pinned and N*_TAU_HI equal to the TAU record\'s -> %s' % gate('C-HS-TAU', okt))

    def tau_read(H, T_, N):
        if F(H['N%d_TAU_HI' % N]) != F(T_['N%d_TAU_HI' % N]):
            raise Refused('C-HS-TAU: N%d_TAU_HI differs from the TAU record' % N)
    out('PLANT-HS-TAU (through a reader): TAU_HI + 1e-12 must be refused -> %s' % plant('PLANT-HS-TAU', refuses(
        tau_read, dict(H2, N4_TAU_HI=fstr(F(H2['N4_TAU_HI']) + Fraction(1, 10 ** 12))), TU, 4, tag='C-HS-TAU')))
    out('C-HS-BFORM: QB_CRUDE and QB_SLOPE at least ADD2_1\'s formulas -> %s' % gate('C-HS-BFORM', okb))
    out('C-HS-AFORM: QA_CRUDE of D4A and D4MA at least ADD3\'s formulas -> %s' % gate('C-HS-AFORM', oka))
    out('C-HS-CBOX: the record boxes\' sides; per piece the centre balls inside the boxes -> %s' % gate('C-HS-CBOX', okc))


def pre_dlm1():
    DL, H2, H3, TU, M2 = G['DL'], G['H2'], G['H3'], G['TU'], G['M2B']
    wo = open(DL1OUT).read().split('\n')
    oks = (DL.get('RECORD') == 'TRICK_DLM1_v1' and DL.get('END') == 'TRICK_DLM1_v1' and DL.get('EXPORT_STATUS') == 'CERTIFIED'
           and DL.get('VERDICT_OF_WRITER') == 'VALID' and all('KEYMAP_%s' % k in DL for k in ('D3B', 'D4A', 'D4MA'))
           and not refuses(rule_v2, wo) and any(PINS[DL1] in ln for ln in wo if 'RECORD' in ln))
    out('C-DLM1-SRC: record 895634f5 CERTIFIED, VERDICT_OF_WRITER VALID, KEYMAP per kind; its run output\'s VERDICT lines exactly '
        '[VERDICT VALID] and a RECORD line with the full sha256 (rule V2) -> %s' % gate('C-DLM1-SRC', oks))
    out('PLANT-DLM1-KIND: a D4 row read with D4MA\'s keys must be refused -> %s' % plant('PLANT-DLM1-KIND', refuses(
        dl1_vals, DL, 4, 'D4', 'D4MA', tag='C-DLM1-SRC')))
    out('PLANT-DLM1-KIND-UNSAFE: a D4M row read with D4A\'s keys must be refused -> %s' % plant('PLANT-DLM1-KIND-UNSAFE', refuses(
        dl1_vals, DL, 4, 'D4M', 'D4A', tag='C-DLM1-SRC')))
    out('C-LAMBDA-ONCE: Q_HI_D4MA is read at power 0 -> %s' % gate('C-LAMBDA-ONCE', not refuses(q_hi_power, 'D4MA', 0)))
    out('PLANT-LAMBDA-TWICE: power 1/2 on top must be refused -> %s' % plant('PLANT-LAMBDA-TWICE', refuses(
        q_hi_power, 'D4MA', Fraction(1, 2), tag='C-LAMBDA-ONCE')))
    out('PLANT-LAMBDA-DROP: v3\'s QA_CRUDE of D4MA at power 0 must be refused -> %s' % plant('PLANT-LAMBDA-DROP', refuses(
        v3_power, H3, 'D4MA', 0, tag='QA_CRUDE')))
    okv, okq, okq1 = True, True, True
    for N in (4, 3):
        a4, m4 = H3['N%d_D4A_R000' % N].split(), H3['N%d_D4MA_R000' % N].split()
        qa_s, qm_s = DL['N%d_Q_HI_D4A' % N], DL['N%d_Q_HI_D4MA' % N]
        bound = F(m4[6]) ** 2 / (F(TU['N%d_I_FREE_LO' % N]) * F(TU['N%d_RQH_LO' % N]))
        mant = qm_s.split('e')[0]
        ulp = Fraction(1, 10 ** (len(mant.split('.')[1]) if '.' in mant else 0)) * (Fraction(10) ** int(qm_s.split('e')[1]) if 'e' in qm_s else 1)
        okv = okv and qa_s == a4[6] and F(qm_s) ** 2 >= bound and (F(qm_s) - ulp) ** 2 < bound
        b = H2['N%d_D3B_R000' % N].split()
        okq = okq and F(DL['N%d_Q_HI_D3B' % N]) == F(b[6]) and all(
            F(DL['N%d_E_SEMI_HI_%s' % (N, k)]) <= F(DL['N%d_Q_HI_%s' % (N, k)]) for k in ('D3B', 'D4A', 'D4MA'))
        eps = B(M2['N%d_EPS_R_300' % N])
        g = (B(H2['N%d_RTR' % N]) - 1 + eps) / (ONE - eps)
        tau = B(TU['N%d_TAU_HI' % N])
        for k, p in (('D3B', 3), ('D4A', 2), ('D4MA', 2)):
            okq1 = okq1 and upf(CM.ipow(g, p - 1) * g.sqrt() * tau) <= F(DL['N%d_Q1_HI_%s' % (N, k)])
    out('C-DLM1-V3: Q_HI_D4A = v3\'s QA_CRUDE; Q_HI_D4MA^2 at least the exact bound, one unit lower fails -> %s' % gate('C-DLM1-V3', okv))
    out('C-DLM1-QB: Q_HI_D3B = QB_CRUDE and E_SEMI_HI <= Q_HI -> %s' % gate('C-DLM1-QB', okq))
    out('C-Q1-RECOMP: Q1_HI recomputed in balls at or below the record\'s -> %s' % gate('C-Q1-RECOMP', okq1))


def pre_uhat(pcs):
    """v1_3_2: the u-hat records of interface v1_4, per N: strict rule V2 on the writer's run output, the record's checks (uhat_check,
    C-CENTRES, C-ROWS, C-M2B-RANGE), the readings, and the plants, each run through the reader's own functions."""
    for N in (4, 3):
        d = G['UH'][N]
        errs = uhat_src(d, N)
        out('C-UHAT-SRC N=%d (interface v1_4): %s (%s), EXPORT_STATUS %s, MOCK %s: problems %s -> %s' % (
            N, os.path.basename(uhat_path(N)), sha_file(uhat_path(N))[:8], d.get('EXPORT_STATUS'), d.get('MOCK'), errs or 'none',
            gate('C-UHAT-SRC', not errs)))
        wl = open(uhat_out(N)).read().split('\n')
        nm, sh = os.path.basename(uhat_path(N)), sha_file(uhat_path(N))
        out('C-UHAT-V2 N=%d (strict rule V2): the writer\'s run output %s (%s) has one RECORD line naming %s with its full sha256, and one '
            'VERDICT line, "VERDICT VALID", as its last line -> %s' % (N, os.path.basename(uhat_out(N)), sha_file(uhat_out(N))[:8], nm,
                                                                     gate('C-UHAT-V2', not refuses(rule_v2_strict, wl, nm, ORIG_UHATKV[N] if ACC.carried(uhat_out(N)) else sh))))
        wn = [ln for ln in wl if ln.strip()]
        p0 = refuses(rule_v2_strict, [ln for ln in wl if not ln.startswith('RECORD %s' % nm)], nm, sh, tag='RULE-V2')
        p1 = refuses(rule_v2_strict, wn[:-1] + ['VERDICT VALID', 'VERDICT VALID'], nm, sh, tag='RULE-V2')
        p2 = refuses(rule_v2_strict, wn + ['a line after the verdict'], nm, sh, tag='RULE-V2')
        p3 = refuses(rule_v2_strict, wn[:1] + ['RECORD %s sha256 %s' % (nm, sh)] + wn[1:], nm, sh, tag='RULE-V2')
        out('PLANT-UHAT-V2 N=%d: the output without its RECORD line, with two VERDICT lines, with a line after the verdict, and with a second '
            'RECORD line, must each be refused -> %s' % (N, plant('PLANT-UHAT-V2', p0 and p1 and p2 and p3)))
        try:
            prepare_uhat(N)
            uv = G['UV'][N]
        except Refused as ex:
            out('C-UHAT-READ N=%d: refused: %s -> %s' % (N, ex, gate('C-UHAT-READ', False)))
            continue
        rids = G['ROWSL']['ROWS_N%d' % N].split()
        out('C-UHAT-READ N=%d (interface v1_4): the tags, the exact pins (INTERFACE, ROWS, M2B, centres.source, centres.pieces %s, J_RANGE '
            '%s), the key whitelist, the forms, the WORLD lists and END as the last line; eps_r %s and s %s from M2B, in [0, 1) -> PASS' % (
                N, d.get('centres.pieces'), d.get('J_RANGE'), fstr(uv['eps'], 12), fstr(uv['sM'], 12)))
        out('C-ROWS N=%d: the engine\'s own B3/TB/TD rows equal ROWS_N%d (%d rows; COUNT_N%d %s) -> PASS' % (
            N, N, len(rids), N, G['ROWSL'].get('COUNT_N%d' % N)))
        for w in ('D4L0', 'D4ML0'):
            x = uv['L0'][w]
            out('C-L0-HI, C-L0-POST N=%d %s: L0_hi %s; q-hat %.12g; q_hi recorded %.12g, recomputed %.12g (relative %.2e); q_use %.12g -> '
                'PASS' % (N, w, fstr(x['L0'], 12), float(x['qh']), float(x['qrec']), float(x['qout']),
                          float(abs(x['qrec'] - x['qout']) / x['qout']), float(x['quse'])))
        r0s = list(uv['R0'].values())
        out('C-UD3-POST N=%d (route 0 per row): %d rows, routes %s; q_b_hi recorded max %.12g, recomputed max %.12g; U_use from %.12g to '
            '%.12g -> PASS' % (N, len(r0s), ','.join(sorted(set(x['route'] for x in r0s))), float(max(x['rec'] for x in r0s)),
                               float(max(x['out'] for x in r0s)), float(min(x['use'] for x in r0s)), float(max(x['use'] for x in r0s))))
        sM, eps = uv['sM'], uv['eps']
        x4 = uv['L0']['D4ML0']
        f0, l0 = G['RSTART'][N], NP - 1
        rid0 = 'D3_1_2'
        L = G['UHL'][N]
        p_c1 = refuses(centres_read, dict(d, **{'centres.source': d['centres.source'][:-8] + '00000000'}), f0, l0, tag='C-CENTRES')
        p_c2 = refuses(centres_read, dict(d, **{'centres.pieces': 'P%04d..P0800' % f0}), f0, l0, tag='C-CENTRES')
        out('PLANT-CENTRES N=%d: a centres.source naming another sha, and centres.pieces ending at P0800, must be refused -> %s' % (
            N, plant('PLANT-CENTRES', p_c1 and p_c2)))
        pp = [refuses(uhat_check, dict(d, **{k: v}), N, L, tag='C-UHAT-PIN') for k, v in (
            ('INTERFACE', d['INTERFACE'][:-8] + '00000000'), ('ROWS', 'pk12/ROWS_OTHER.kv:' + PINS[ROWSF]),
            ('M2B', d['M2B'][:-8] + '00000000'), ('J_RANGE', '300 inf' if N == 3 else '300.0 inf'),
            ('CODE', '../' + os.path.basename(CODEDIR) + '/' + d['CODE']))]
        out('PLANT-UHAT-PIN N=%d: INTERFACE and M2B naming another sha, ROWS naming another path with the right sha, a '
            'J_RANGE other than %r, and (v1_3_4) a CODE src reaching its own file through a .. segment, must each be refused '
            '-> %s' % (N, G['JR'][N], plant('PLANT-UHAT-PIN', all(pp))))
        pk = [refuses(uhat_check, dict(d, **{k: v}), N, L, tag=t) for k, v, t in (
            ('route0b_hat.D3_9_9.q_b_hi', '0.1', 'C-UHAT-KEYS'), ('wmat_hat.D4.form', 'vector', 'C-UHAT-KEYS'),
            ('MOCK', 'FALSE' if MODE == 'mock' else 'TRUE', 'C-UHAT-TAGS'), ('VERDICT_OF_WRITER', 'INVALID', 'C-UHAT-TAGS'))]   # v1_3_6_2: per mode
        pk.append(refuses(uhat_check, d, N, [ln for ln in L if ln.strip()] + ['INFO = a line after END'], tag='C-UHAT-TAGS'))
        pk.append(refuses(uhat_check, dict(d, WORLD_U_HAT=' '.join(d['WORLD_U_HAT'].split()[1:])), N, L, tag='C-WORLD-U'))
        out('PLANT-UHAT-KEYS N=%d: a key outside the table, a wmat_hat key, MOCK %s in %s mode, VERDICT_OF_WRITER INVALID, a line '
            'after END, and a WORLD_U_HAT list short of one key, must each be refused -> %s' % (
                N, 'FALSE' if MODE == 'mock' else 'TRUE', MODE, plant('PLANT-UHAT-KEYS', all(pk))))
        rl = rids[1:]
        out('PLANT-ROWS N=%d: ROWS_N%d with one row dropped must be refused by C-ROWS -> %s' % (N, N, plant(
            'PLANT-ROWS', refuses(rows_check, N, rl, str(len(rl)), tag='C-ROWS'))))
        out('PLANT-M2B-RANGE N=%d: eps_r = 1 and s = -1e-9 from M2B must be refused -> %s' % (N, plant('PLANT-M2B-RANGE', refuses(
            m2b_vals, N, dict(G['M2B'], **{'N%d_EPS_R_300' % N: '1.0'}), tag='C-M2B-RANGE') and refuses(
            m2b_vals, N, dict(G['M2B'], **{'N%d_S_300' % N: '-1e-9'}), tag='C-M2B-RANGE'))))
        p1 = refuses(l0_read, dict(d, **{'l0_hat.D4ML0.L0_hi': '-1e-6'}), 'D4ML0', sM, eps, tag='C-L0-HI')
        p2 = all(refuses(l0_read, dict(d, **{'l0_hat.D4ML0.L0_hi': v}), 'D4ML0', sM, eps, tag='C-L0-HI') for v in ('nan', 'inf', ''))
        dn = dict(d, **{'l0_hat.D4ML0.L0_hi': '0.000131'})
        p3 = refuses(l0_read, dn, 'D4ML0', sM, eps, round_down=True, tag='C-L0-HI')
        c3 = not refuses(l0_read, dn, 'D4ML0', sM, eps, tag='C-L0-HI')
        out('PLANT-L0-NEG N=%d: a negative L0_hi must be refused by C-L0-HI -> %s' % (N, plant('PLANT-L0-NEG', p1)))
        out('PLANT-L0-NONFINITE N=%d: L0_hi nan, inf or empty must be refused by C-L0-HI -> %s' % (N, plant('PLANT-L0-NONFINITE', p2)))
        out('PLANT-L0-HI-DOWN N=%d: q_hi rounded down at L0_hi = 0.000131 must be refused by C-L0-HI itself, and rounded up C-L0-HI '
            'must not refuse (control %s) -> %s' % (N, 'ok' if c3 else 'FAILED', plant('PLANT-L0-HI-DOWN', p3 and c3)))
        qno = upf(nb1_h(B(x4['qh']), eps, x4['mhs'], Fraction(0), sM) + ZERO)
        ql0 = upf(ONE / (ONE - B(sM) * B(sM)).sqrt() * (B(x4['L0']) + B(x4['T'])).sqrt() + B(eps) * B(x4['mhs']) / (ONE - B(eps)))
        p4 = refuses(l0_read, dict(d, **{'l0_hat.D4ML0.q_hi': fstr(qno)}), 'D4ML0', sM, eps, tag='C-L0-POST')
        p5 = refuses(l0_read, dict(d, **{'l0_hat.D4ML0.q_hi': fstr(ql0)}), 'D4ML0', sM, eps, tag='C-L0-POST')
        out('PLANT-L0-POST N=%d: q_hi with T left out, and with T on the L0 scale, must be refused by C-L0-POST -> %s' % (
            N, plant('PLANT-L0-POST', p4 and p5)))
        p6 = refuses(l0_read, dict(d, **{'l0_hat.D4ML0.m_hat_s_hi': '-4e-3'}), 'D4ML0', sM, eps, tag='negative')
        p7 = refuses(bp_read, dict(d, **{'bprime_hat.FA.T_v': '-3.63e-6'}), 3, tag='negative')
        p7b = refuses(l0_read, dict(d, **{'l0_hat.D4ML0.xsu_hi': '-1e-3'}), 'D4ML0', sM, eps, tag='negative')
        p7c = refuses(r0_read, dict(d, **{'route0b_hat.%s.T_s' % rid0: '0'}), rid0, sM, eps, tag='> 0')
        out('PLANT-NEG-INPUT N=%d: a negative m_hat_s_hi, T_v and xsu_hi, and T_s = 0, must each be '
            'refused -> %s' % (N, plant('PLANT-NEG-INPUT', p6 and p7 and p7b and p7c)))
        qlow = x4['qout'] * (1 - Fraction(1, 10 ** 10))
        rq = l0_read(dict(d, **{'l0_hat.D4ML0.q_hi': fstr(qlow)}), 'D4ML0', sM, eps)
        out('PLANT-L0-QUSE N=%d: a record q 1e-10 below q_out leaves q_use = q_out -> %s' % (N, plant('PLANT-L0-QUSE', rq['quse'] == rq['qout'])))
        r0 = uv['R0'][rid0]
        p8 = refuses(r0_read, dict(d, **{'route0b_hat.%s.q_b_hi' % rid0: d['route0b_hat.%s.q_hat_hi' % rid0]}), rid0, sM, eps,
                     tag='C-UD3-POST')
        out('PLANT-UD3-NO-T N=%d: %s\'s q_b_hi equal to its q_hat_hi must be refused by C-UD3-POST -> %s' % (N, rid0, plant(
            'PLANT-UD3-NO-T', p8)))
        rr = r0_read(dict(d, **{'route0b_hat.%s.q_b_hi' % rid0: fstr(r0['out'] * (1 - Fraction(1, 10 ** 10)))}), rid0, sM, eps)
        out('PLANT-UD3-QUSE N=%d: a record value 1e-10 below U_out leaves U_use = U_out -> %s' % (N, plant('PLANT-UD3-QUSE', rr['use'] == rr['out'])))
        pr = [refuses(r0_read, dict(d, **{'route0b_hat.%s.T_U4' % rid0: '1e-5'}), rid0, sM, eps, tag='C-UD3-POST'),
              refuses(r0_read, dict(d, **{'route0b_hat.%s.formula' % rid0: 'ROUTE_H_NB1'}), rid0, sM, eps, tag='C-UD3-POST')]
        out('PLANT-ROUTE-FORM N=%d: a route P row with a T_U4 key, and a route P row with formula ROUTE_H_NB1, must be refused -> %s' % (
            N, plant('PLANT-ROUTE-FORM', all(pr))))
        out('PLANT-SAME-WORLD N=%d: a route-0 value from a non-u-hat record must be refused -> %s' % (N, plant('PLANT-SAME-WORLD', refuses(
            r0_read, dict(d, RECORD='R0ASM_v1'), rid0, sM, eps, tag='C-R0ASM'))))
        pcN = pcs[N]
        out('PLANT-UD3-PIECE N=%d: a J range ending below piece %d must be refused -> %s' % (N, pcN['i'], plant('PLANT-UD3-PIECE', refuses(
            piece_in_range, dict(d, J_RANGE='300 %s' % fstr(F(pcN['jlo']) - 1, 12)), pcN['jlo'], pcN['jhi'], tag='C-UD3-PIECE'))))
        out('PLANT-WORLD-LIST N=%d: a q_hi not listed under WORLD_TRUE_U must be refused -> %s' % (N, plant('PLANT-WORLD-LIST', refuses(
            l0_read, dict(d, WORLD_TRUE_U='route0b_hat.%s.q_b_hi' % rid0), 'D4ML0', sM, eps, tag='C-WORLD-U'))))
        pb = [refuses(bp_read, dict(d, **{'bprime_hat.FA.basis': 'C^'}), 3, tag='C-BASIS-RAW'),
              refuses(bp_read, dict(d, **{'bprime_hat.FA.v_hat_raw.1': '0.002 0.001'}), 3, tag='C-BASIS-RAW'),
              refuses(bp_read, dict(d, **{'bprime_hat.FA.v_hat_raw.1': '-6.7e-3'}), 3, tag='C-BASIS-RAW')]
        out('PLANT-BASIS-RAW N=%d: a record in C^ coordinates, a ball with lo > hi, and a single number in place of a ball, must be '
            'refused -> %s' % (N, plant('PLANT-BASIS-RAW', all(pb))))
        dno = dict(d)
        dno.pop('bprime_hat.FA.T_v_source', None)
        src = d['bprime_hat.FA.T_v_source']
        p9 = refuses(bp_read, dno, 3, tag='C-T-SRC') and refuses(bp_read, dict(d, **{'bprime_hat.FA.T_v_source': src[:-8] + '00000000'}), 3,
                                                                tag='C-T-SRC')
        out('PLANT-TV-SRC N=%d: T_v with no source line, and naming another sha, must be refused -> %s' % (N, plant('PLANT-TV-SRC', p9)))
        out('PLANT-WMAT N=%d: a wmat_hat key must be refused by w_read -> %s' % (N, plant('PLANT-WMAT', refuses(
            w_read, dict(d, **{'wmat_hat.D4.form': 'vector'}), 'D4', tag='C-TW-SRC'))))
    out('C-TW-SRC: no wmat_hat key in either record; N4\'s two (1,1) rows read WAIT-W, and N3\'s two take the crude reading (CRUDE11) '
        '-> %s' % gate('C-TW-SRC', all(not refuses(w_read, G['UH'][N], f) for N in (4, 3) for f in ('D4', 'D4M'))))
    out('PLANT-CENTRE: R(1, j) centring must be refused -> %s' % plant('PLANT-CENTRE', refuses(centre_coef, 'R(1,j)', tag='C-CENTRE-R65')))
    st = open(SIGG).read()
    okv2 = not refuses(rule_v2, st.split('\n'))
    vals = {n: sigg_cert(st, n) for n in (4, 3)}
    eq = all(vals[n] == (G['KAP'][n], G['PHI'][n]) for n in (4, 3))
    out('C-SIGG-SRC: v1_37_1\'s cert output (f5410931) under rule V2 %s; kappa_max (C-NA, dec_hi) N4 %s, N3 %s; Phi_eps (PHI-EPS) N4 %s, '
        'N3 %s; equal to the mock source\'s values: %s (INFO) -> %s' % (okv2, fstr(vals[4][0], 17), fstr(vals[3][0], 17), fstr(vals[4][1], 17),
                                                                    fstr(vals[3][1], 17), eq, gate('C-SIGG-SRC', okv2)))
    ge1 = '\n'.join(ln for ln in st.split('\n') if ln.startswith('C-KAPPA-GE1') or ln.startswith('PHI-EPS'))
    out('PLANT-KAPPA-GE1: a source with C-KAPPA-GE1 (a lower end) in place of C-NA must be refused -> %s' % plant('PLANT-KAPPA-GE1', refuses(
        sigg_cert, ge1, 4, tag='C-SIGG-SRC')))


def pre_forms(pcs):
    pc, uv = pcs[4], G['UV'][4]
    out('PLANT-Q1-PLANE: d_L = -1 reads of l(-1) and of l(2) must be refused -> %s' % plant(
        'PLANT-Q1-PLANE', refuses(eval_rows, 4, pc, uv, {'plane': -1}, tag='C-Q1-PLANE') and refuses(eval_rows, 4, pc, uv, {'plane': 2}, tag='C-Q1-PLANE')))
    Qh = dl1_vals(G['DL'], 4, 'D4', 'D4A')[1]
    Q1h = dl1_vals(G['DL'], 4, 'D4', 'D4A')[2]
    out('PLANT-DL0-QHI (by value): Q_HI\'s value fed as a d_L = 0 q must be refused -> %s' % plant(
        'PLANT-DL0-QHI', refuses(eval_rows, 4, pc, uv, {'q_dl0': B(Qh)}, tag='C-DL0-NO-QHI')))
    out('PLANT-DL0-Q1 (by value): Q1_HI\'s value fed as a d_L = 0 Q1 must be refused -> %s' % plant(
        'PLANT-DL0-Q1', refuses(eval_rows, 4, pc, uv, {'Q1_dl0': B(Q1h)}, tag='C-DL0-Q1')))
    rnRs = [side(pc, r['dR'])[0] for r in G['ROWS'][4] if r['dL'] == -1 and r['dR'] != 'inf']
    rmin = min(rnRs, key=lambda x: float(x.mid()))
    out('PLANT-DEN-POS: Q1 = 1/rn1_R at the d_L = -1 rows must be refused by C-DEN-POS -> %s' % plant(
        'PLANT-DEN-POS', refuses(eval_rows, 4, pc, uv, {'Q1_dlm1': ONE / rmin.lower()}, tag='C-DEN-POS')))
    pc3, uv3 = pcs[3], G['UV'][3]
    m_, Qa3, U3 = pc3['D3'], pc3['Q'][-1], uv3['R0']['D3_0_1']['use']
    out('PLANT-ESEMI (by value): beta with Cov_inf_lo in place of Cov_inf_hi, and without Cov_inf_hi, must be refused -> %s' % plant(
        'PLANT-ESEMI', refuses(eval_rows, 3, pc3, uv3, {'es_beta': B(m_['mcilo']) + Qa3 * B(U3)}, tag='C-ESEMI-FORM')
        and refuses(eval_rows, 3, pc3, uv3, {'es_beta': Qa3 * B(U3)}, tag='C-ESEMI-FORM')))
    out('PLANT-ESEMI-FORMS: alpha forced on N3 D3 (0,1) must be refused -> %s' % plant(
        'PLANT-ESEMI-FORMS', refuses(eval_rows, 3, pc3, uv3, {'form': 'alpha'}, tag='C-ESEMI-FORM')))
    out('PLANT-DLM1-KIND-ROW: a d_L = -1 row evaluated with another kind\'s keys must be refused -> %s' % plant(
        'PLANT-DLM1-KIND-ROW', refuses(eval_rows, 4, pc, uv, {'kind': 'D4MA'}, tag='C-DLM1-SRC')))
    out('PLANT-CENTRE-ROW: the rows with R(1, j) centring must be refused -> %s' % plant(
        'PLANT-CENTRE-ROW', refuses(eval_rows, 4, pc, uv, {'centre': 'R(1,j)'}, tag='C-CENTRE-R65')))
    out('PLANT-ESEMI-BASE (a21b717c): the harmonic Cov in the d_L <= 0 base slot must be refused in cert mode -> %s' % plant(
        'PLANT-ESEMI-BASE', refuses(esemi_base_ok, 'harmonic-Cov(0)', 'cert', tag='C-ESEMI-BASE')))
    out('C-ESEMI-BASE: mode %s; the d_L <= 0 base at a row without a pinned E_main record is %s (cert mode refuses the harmonic Cov and '
        'needs pk04\'s record for every row); esemi_transfer is the identity (2414bd75 sect. 1) -> %s' % (
            MODE, esemi_base(4, pc, None, ONE)[1] if MODE == 'mock' else 'refused (C-ESEMI-SRC)',
            gate('C-ESEMI-BASE', (not refuses(esemi_base_ok, esemi_base(4, pc, None, ONE)[1], MODE)) if MODE == 'mock'
                 else refuses(esemi_base, 4, pc, None, ONE, tag='C-ESEMI-SRC'))))   # v1_3_6_2: cert mode, no stand-in base exists
    out('C-ESEMI-T0 (v1_3_4): at the last piece of each N, after its rows (es_t0)')
    for N in (4, 3):
        p = pcs[N]
        okc, rm, rw = cv_check(p, G['UV'][N]['BP'][0])
        out('C-CV N=%d piece %d: ||C^ v||^2 and v^T Gq^-1 v overlap %s; relative midpoint gap %s, relative width %s -> %s' % (
            N, p['i'], okc, ('%.2e' % rm) if rm is not None else '-', ('%.2e' % rw) if rw is not None else '-', 'PASS' if okc else 'FAIL'))
        dl = max(1e-6, 4 * (rw or 0.0))
        okp, _a, _b = cv_check(p, G['UV'][N]['BP'][0], scale=Fraction(1) + Fraction(dl).limit_denominator(10 ** 12))
        out('PLANT-CV N=%d: C^ v scaled by 1 + %.2e (4 times the relative width, at least 1e-6) must break C-CV -> %s' % (
            N, dl, plant('PLANT-CV', okc and not okp)))
        rows = eval_rows(N, p, G['UV'][N])
        jd = [judge(lo, cov) for (row, lo, cov, info) in rows]
        cs = [(row, info['cs']) for (row, lo, cov, info) in rows if info.get('cs') is not None]
        qFA = B(G['UV'][N]['L0']['D4L0']['quse'])
        if cs:
            row0, (dot0, na0) = cs[0]
            fake = B(Fraction(11, 10) * upf(na0 * qFA))
            out('PLANT-T-CS N=%d (%s): a dot of 1.1 times ||alpha||_2 q_FA must fail C-T-CS, and the row\'s own dot passes (%s) -> %s' % (
                N, rname(row0), tcs_ok(dot0, na0, qFA), plant('PLANT-T-CS', tcs_ok(dot0, na0, qFA) and not tcs_ok(fake, na0, qFA))))
        bad0 = piece_gates(N, p)
        badf = piece_gates(N, dict(p, F4=box_f4(N) + Fraction(1, 10 ** 6)))
        out('PLANT-F4 N=%d: an F4 1e-6 above box_f4 (%.6f) must fail C-F4, and the piece\'s own F4 (%.6f) passes -> %s' % (
            N, float(box_f4(N)), float(p['F4']), plant('PLANT-F4', 'C-F4' in badf and 'C-F4' not in bad0)))
        badp = piece_gates(N, dict(p, parx=(True, False)))
        out('PLANT-S8-PAREXACT N=%d: a piece whose B chain is not parity-exact must fail C-S8-PAREXACT, and the piece itself (set '
            '%s, par_exact %s) passes -> %s' % (N, p.get('s8set'), p.get('parx'), plant(
                'PLANT-S8-PAREXACT', 'C-S8-PAREXACT' in badp and 'C-S8-PAREXACT' not in bad0)))
        cand = [(j[1], k) for k, j in enumerate(jd) if j[0] and rows[k][0]['typ'] not in ('OUT', 'W')]
        if cand:
            h0, k0 = min(cand)
            row, lo, cov, info = rows[k0]
            Rb = cov - lo
            Fb = lof(cov) / upf(Rb)
            ok_a = judge(cov - B(Fb / Fraction(11, 10)) * Rb, cov)[0]
            ok_b = judge(cov - B(Fb * Fraction(11, 10)) * Rb, cov)[0]
            out('PLANT-ROW N=%d (plan v1 l.74, self-calibrating; v1_3_1: F at lo = 0, F = Cov_lo / R_hi): binding passing row %s (headroom '
                '%.6g), bound factor F %.6f: holds at F/1.1 (%s), fails at 1.1 F (%s) -> %s' % (N, rname(row), h0, float(Fb), ok_a, not ok_b,
                                                                                              plant('PLANT-ROW', ok_a and not ok_b)))
    out('C-Q1-PLANE, C-DL0-NO-QHI, C-DL0-Q1, C-ESEMI-FORM, C-DEN-POS, C-ESEMI-BASE run at every piece by value (a refusal is a KILL line); '
        'C-CV, C-F4, C-T-CS and C-S8-PAREXACT run at every piece')


def row_lines(N, i, ev):
    pc, rows, jd, bad, kills = ev
    for (row, lo, cov, info), (ok, h, ll, ch_) in zip(rows, jd):
        extra = []
        if 'tfa' in info:
            extra.append('T_FA_lo %.6e' % float(info['tfa']))
        if info.get('crude11'):
            extra.append('crude (1,1): nX e_L e_R in place of T_W (1920fa90 (3))')
        if row['typ'] == 'W':
            extra.append('wait-W: the margin is the crude reading, INFO (W-matrix deferred)')
        if 'Q1' in info:
            extra.append('Q1_HI %s, Q(p-2) %.6e' % (fstr(info['Q1'][0], 6), float(info['Q1'][1])))
        if 'beta' in info:
            extra.append('beta: Cov_inf_lo > 0 %s, Cov_inf_hi used %s' % (info['beta'][0], fstr(info['beta'][1], 8)))
        if 'sg' in info:
            extra.append('sigma_g %.4e at L %.2f' % info['sg'])
        if 'base' in info:
            extra.append('base %s' % info['base'])
        if 'es' in info:
            em, es_old, s8_, lab = info['es']
            extra.append('Cov_main [%.6e, %.6e], E_X [%.6e, %.6e], m_e %.4e, m_f %.4e, D [%.6e, %.6e], |E| %.4e (record or alpha form %.4e), '
                         'nc %.2e, nd %.2e, R %.3e' % (
                             float(lof(em['cm'])), float(upf(em['cm'])), float(lof(em['ex'])), float(upf(em['ex'])), float(em['me'].mid()),
                             float(em['mf'].mid()), float(lof(em['dd'])), float(upf(em['dd'])), float(upf(abs(em['ex']))), float(es_old),
                             float(upf(em['nc'])), float(upf(em['nd'])), float(upf(info['R']))))
        if 'Ref' in info:
            extra.append('R_X %.3e, R_e %.3e, R_f %.3e, stand-ins %s' % (float(upf(info['Ref'][2])), float(upf(info['Ref'][0])),
                                                                        float(upf(info['Ref'][1])), info['Ref'][3]))
        if 'prod' in info:
            extra.append('product |m_e| %.3e x |m_f| %.3e = %.3e (crude O_e)' % tuple(float(x) for x in info['prod']))
        if info.get('be') is not None:
            a2 = row['typ'] == 'A2'
            for lab, (var, xs, xt, xa, xv) in zip(('be', 'be12'), info['be']):
                extra.append('%s %s rec %s tol %s alt %s tv %s' % (lab, var, flr(xs), flr(xt) if var == 'D4ML0' else '-',
                                                                   flr(xa) if (a2 and var == 'D4ML0') else '-', flr(xv) if a2 else '-'))
        out('ROW N=%d i=%d %s %s: lo_lo %s, Cov_hi %s, lo_lo/Cov_hi %.6g, headroom %.6g (INFO) -> %s%s' % (
            N, i, rname(row), row['typ'], ('%.6e' % float(ll)) if ll is not None else '-', ('%.6e' % float(ch_)) if ch_ is not None else '-',
            margin_of((ok, h, ll, ch_)), h, mark_of(row, ok, info), ('; ' + '; '.join(extra)) if extra else ''))


def run_pre(A):
    pre_inputs()
    pre_hs()
    pre_dlm1()
    pcs = {}
    for N in (4, 3):
        pcs[N] = piece_data(N, A['RSTART'][N], A)
        if pcs[N] is None:
            raise ValueError('S8 returned None at the first piece of N=%d' % N)
    pre_uhat(pcs)
    if not all(N in G.get('UV', {}) for N in (4, 3)):
        out('PRE: the u-hat readings were refused; the reading plants and the pieces are skipped')
        return
    pre_forms(pcs)
    pre_esemi(A, pcs)   # v1_3_4: the E_main records' gates and plants; v1_3_5: the slots, C-TRB-SRC, C-UH-PIECE, C-UE-LE-WE
    pre_r123(A, pcs)    # v1_3_5: PLANT-ESEMI-SHARED, PLANT-ESEMI-DPOS, C-ESEMI-RUN with its plant
    pre_prod(pcs)       # v1_3_5: C-PROD (INFO), PLANT-PROD, PLANT-QE-ROUTE2
    for N in (4, 3):
        qx = float(re.search(r'<= \|\|Q0 a\|\| = \(1/r_inf - 1\)\^\(1/2\) (\S+) \(ADD1', open(TRKO[N]).read()).group(1))
        qa = lof(pcs[N]['Q'][-1])
        out('C-QA N=%d: Qa lower end %.6f at least kt_trick_v1\'s ||Q0 l(-1)|| %.6f -> %s' % (N, float(qa), qx, gate('C-QA', float(qa) >= qx)))
        for i in (A['RSTART'][N], NP - 1):
            ev = eval_piece(N, i, A)
            piece_report(N, i, ev)
            row_lines(N, i, ev)
            if i == NP - 1:
                es_t0(N, ev)   # v1_3_4: C-ESEMI-T0 and its plant at the last piece
    out('C-ADD10 (INFO): the break-evens\' tol column reads ADD10 sect. 5\'s q_tol (8aa8160f): %s' % ', '.join(
        'N%d %s q_tol %s' % (k[0], k[1], v) for k, v in sorted(G['QTOL'].items())))
    out('C-WAITW-CORNER: PENDING at N4 (no W-matrix; deferred): N4\'s two (1,1) rows read WAIT-W; N3\'s two take the crude '
        'reading (the review 1920fa90 (3), 803aab31 (d))')


def grid_pieces(N, A):
    i0 = A['RSTART'][N]
    return sorted(set([i0, i0 + 1, i0 + 10, i0 + 40, 150, 250, 400, 600, 800, 903]))


def run_grid(A):
    N = GRIDN
    hj = sorted(int(m.group(1)) for m in re.finditer(r'^PIECE (\d+) J_lo', open(HJ[N]).read(), re.M))
    g = grid_pieces(N, A)
    out('C-GRID N=%d: the grid %s against kt_s8hj_v1\'s PIECE lines %s -> %s' % (N, g, hj, gate('C-GRID', g == hj)))
    run_pieces(N, A, g)


def run_chunk(A):
    N, a, b = CHUNK
    st = A['RSTART'][N]
    if a < st:
        out('C-RANGE: the chunk starts at %d, below S8\'s range start %d at N=%d; it evaluates from %d' % (a, st, N, st))
    run_pieces(N, A, list(range(max(a, st), b, STRIDE)))


ROWMIN_RE = re.compile(r'^ROWMIN N=([34]) (D3|D4M|D4) \((-?\d+),(\w+)\) (\w+): min lo_lo/Cov_hi (\S+) at piece (\d+); min headroom (\S+) '
                       r'at piece (\d+); marks ([^;\s]+)(?:; be (\S+) rec (\S+) tol (\S+) alt (\S+) tv (\S+); be12 (\S+) rec (\S+) tol (\S+) '
                       r'alt (\S+) tv (\S+))?$')
PIECE_RE = re.compile(r'^PIECE N=([34]) i=(\d+) ok=([01]):')


def be_parse(s):
    if s in (None, 'inf'):
        return None
    v, i = s.split('@')
    return (Fraction(v), int(i))


def run_final(A):
    pat = re.compile(r'^out_%s_%s_(pre|grid_n[34]|c([34])_(\d{4})_(\d{4})_s(\d+))%s\.out$' % (re.escape(LABEL), MODE, re.escape(RTAG)))
    files = sorted(f for f in os.listdir(OUTP) if pat.match(f))
    pre, chunks, grids, bad = [], [], [], []
    for f in files:
        lines = open(os.path.join(OUTP, f)).read().split('\n')
        okf = lines[0].startswith('%s sha256 %s ' % (LABEL, ACC.expect(os.path.join(OUTP, f), OWN_SHA, ORIG_SELF))) and lines.count('INPUTS %s' % (DIGEST if ACC.expect(os.path.join(OUTP, f), OWN_SHA, ORIG_SELF) == OWN_SHA else ORIG_DIGEST)) == 1 and 'VERDICT VALID' in lines
        m = pat.match(f)
        kind = 'pre' if m.group(1) == 'pre' else ('grid' if m.group(1).startswith('grid') else 'chunk')
        if not okf:
            bad.append(f)
        (pre if kind == 'pre' else (grids if kind == 'grid' else chunks)).append((f, lines, okf, m))
    out('FINAL inputs: %d pre, %d chunk, %d grid outputs; not matching (sha, digest or VERDICT): %s' % (len(pre), len(chunks), len(grids), bad or 'none'))
    out('C-PRE: exactly one pre output, VALID, same sha256 and INPUTS digest -> %s' % gate('C-PRE', len(pre) == 1 and pre[0][2]))
    kills = [ln for (f, lines, okf, m) in chunks for ln in lines if ln.startswith('KILL ')]
    out('C-NOKILL: KILL lines in the chunk outputs: %d %s -> %s' % (len(kills), kills[:3], gate('C-NOKILL', not kills)))
    acc, cov, beacc = {}, {}, {}
    n_rowmin = 0
    for (f, lines, okf, m) in chunks:
        if not okf:
            continue
        N, st = int(m.group(2)), int(m.group(5))
        for ln in lines:
            pm_ = PIECE_RE.match(ln)
            if pm_:
                cov.setdefault((N, st == 1), set()).add(int(pm_.group(2)))
            n_rowmin += ln.startswith('ROWMIN ')
            rm = ROWMIN_RE.match(ln)
            if rm:
                key = (int(rm.group(1)), rm.group(2), int(rm.group(3)), rm.group(4))
                mg, im = float(rm.group(6)), int(rm.group(7))
                h, i, mks = float(rm.group(8)), int(rm.group(9)), set(rm.group(10).split(','))
                c = acc.setdefault(key, [h, i, set(), rm.group(5), mg, im])
                if h < c[0]:
                    c[0], c[1] = h, i
                if mg < c[4]:
                    c[4], c[5] = mg, im
                c[2] |= mks
                if rm.group(11):
                    cur = beacc.setdefault(key, [None, None])
                    for t, g0 in ((0, 11), (1, 16)):
                        vals = [be_parse(rm.group(g0 + k)) for k in (1, 2, 3, 4)]
                        old = cur[t] or (rm.group(g0), None, None, None, None)
                        cur[t] = (rm.group(g0),) + tuple(o_ if (v_ is None or (o_ is not None and o_[0] <= v_[0])) else v_
                                                         for o_, v_ in zip(old[1:], vals))
    n_parsed = sum(1 for (f, lines, okf, m) in chunks if okf for ln in lines if ROWMIN_RE.match(ln))
    n_rows = {n: len([k for k in acc if k[0] == n]) for n in (4, 3)}
    out('C-ROWMIN-PARSE (v1_3_1): ROWMIN lines parsed %d of %d; rows found N4 %d, N3 %d against the inputs\' %d and %d (an N with no '
        'chunk is C-COVER\'s) -> %s' % (n_parsed, n_rowmin, n_rows[4], n_rows[3], len(G['ROWS'][4]), len(G['ROWS'][3]), gate(
            'C-ROWMIN-PARSE', n_parsed == n_rowmin and all(n_rows[n] in (0, len(G['ROWS'][n])) for n in (4, 3)))))
    status = {}
    for N in (4, 3):
        need_ = set(range(A['RSTART'][N], NP))
        full = cov.get((N, True), set())
        status[N] = 'COMPLETE' if need_ <= full else ('SAMPLED' if (full or cov.get((N, False))) else 'NONE')
    out('C-COVER: N4 %s, N3 %s -> %s' % (status[4], status[3], gate('C-COVER', (MODE == 'mock' and all(status[n] != 'NONE' for n in (4, 3)))
                                                                     or all(status[n] == 'COMPLETE' for n in (4, 3)))))
    marks = {}
    for key, (h, i, mks, typ, mg, im) in sorted(acc.items()):
        mk = 'out' if 'out' in mks else ('wait-W' if 'wait-W' in mks else ('pass' if mks == {'pass'} else 'fail'))
        marks[key] = (mg, im, mk, typ, h)
    rep = []
    for N in (4, 3):
        for mg, k in sorted((v[0], k) for k, v in marks.items() if k[0] == N and v[2] in ('pass', 'fail'))[:3]:
            pc, rows, jd, b_, kl = eval_piece(N, marks[k][1], A)
            mm = [margin_of(j) for (r, lo, c, inf), j in zip(rows, jd) if (r['fam'], r['dL'], r['dR']) == k[1:]]
            rep.append((k, mg, mm[0] if mm else None))
    okr = bool(rep) and all(x[2] is not None and abs(x[2] - x[1]) <= 1e-6 * max(1.0, abs(x[1])) for x in rep)
    out('C-FINAL-REPRO (v1_3_1: the margin lo_lo/Cov_hi): the binding pieces of the three tightest rows per N reproduce their chunk '
        'margin (%s) -> %s' % ('; '.join('N%d %s (%d,%s) %.6g/%s' % (k[0], k[1], k[2], k[3], mg, ('%.6g' % m2) if m2 is not None else '-')
                                         for k, mg, m2 in rep), gate('C-FINAL-REPRO', okr)))
    failing = []
    for N in (4, 3):
        cnt = {}
        for k, v in marks.items():
            if k[0] == N:
                cnt[v[2]] = cnt.get(v[2], 0) + 1
        fl_ = ['%s (%d,%s) %.4g at %d' % (k[1], k[2], k[3], v[0], v[1]) for k, v in sorted(marks.items()) if k[0] == N and v[2] == 'fail']
        failing += ['N%d_%s_(%d,%s)' % (k[0], k[1], k[2], k[3]) for k, v in sorted(marks.items()) if k[0] == N and v[2] == 'fail']
        out('ROWS N=%d: %s; failing (min lo_lo/Cov_hi at piece) %s' % (N, ', '.join('%s %d' % kv_ for kv_ in sorted(cnt.items())), fl_ or 'none'))
    def rowbe_str(bv, typ):
        var, rec, tol, alt, tv = bv
        f_ = lambda x: ('%s at piece %d' % (flr(x[0]), x[1])) if x else 'inf'
        return '%s rec %s%s%s%s' % (var, f_(rec), ('; tol %s' % f_(tol)) if (var == 'D4ML0' and tol) else '',
                                    ('; alt D4L0 %s' % f_(alt)) if (var == 'D4ML0' and typ == 'A2') else '',
                                    ('; T_v %s' % f_(tv)) if typ == 'A2' else '')
    for key in sorted(beacc):
        mk_ = marks.get(key, (0, 0, '-', '-', 0))
        out('ROWBE N=%d %s (%d,%s) %s %s: lo = 0: %s | INFO h = 1.2: %s' % (key[0], key[1], key[2], key[3], mk_[3], mk_[2],
                                                                         rowbe_str(beacc[key][0], mk_[3]), rowbe_str(beacc[key][1], mk_[3])))
    for N in (4, 3):
        for t, tl in ((0, 'lo = 0'), (1, 'INFO h = 1.2')):
            def mn(var, which, typ):
                c = [(beacc[k][t][which], k) for k in beacc if k[0] == N and beacc[k][t] is not None
                     and (var is None or beacc[k][t][0] == var) and (typ is None or marks.get(k, (0, 0, 'x', '-'))[3] == typ)
                     and marks.get(k, (0, 0, 'x'))[2] in ('pass', 'fail') and beacc[k][t][which] is not None]
                return min(c, key=lambda t_: t_[0][0]) if c else None
            for var, which, typ, lab in (('D4ML0', 1, None, 'D4M-L0 q*, D4-L0 at its record value'),
                                         ('D4ML0', 2, None, 'D4M-L0 q*, D4-L0 at ADD10\'s q_tol'),
                                         ('D4ML0', 3, 'A2', 'D4-L0 q*, joint A2 rows, D4M-L0 at its record value'), ('U_D3', 1, None, 'U_D3*'),
                                         ('D4L0', 1, None, 'D4-L0 q*, rows that read only D4-L0'), (None, 4, 'A2', 'T_v*, A2 rows')):
                r_ = mn(var, which, typ)
                out('BE-MIN N=%d %s %s: %s' % (N, tl, lab, ('%s at piece %d, row %s (%d,%s)' % (flr(r_[0][0]), r_[0][1], r_[1][1], r_[1][2],
                                                                                                 r_[1][3])) if r_ else 'none'))
    for N in (4, 3):
        uv = G['UV'][N]

        def mn0(var, which, typ=None):
            c = [beacc[k][0][which][0] for k in beacc if k[0] == N and beacc[k][0] is not None
                 and (var is None or beacc[k][0][0] == var) and (typ is None or marks.get(k, (0, 0, 'x', '-'))[3] == typ)
                 and marks.get(k, (0, 0, 'x'))[2] in ('pass', 'fail') and beacc[k][0][which] is not None]
            return min(c) if c else None

        def vs(v, x):
            return '%.6g against %s (ratio %s)' % (float(v), flr(x) if x is not None else 'none',
                                                  ('%.4g' % float(x / v)) if (x is not None and v > 0) else '-')
        um = max(r['use'] for r in uv['R0'].values())
        xl = [x for x in (mn0('D4ML0', 3, 'A2'), mn0('D4L0', 1)) if x is not None]
        out('COMPARE INFO N=%d (v1_3_2; ADD11 sect. 7, this run\'s lo = 0 minima): U_D3 (max over rows) %s; D4M-L0 q_use %s; D4-L0 q_use %s; '
            'T_v %s' % (N, vs(um, mn0('U_D3', 1)), vs(uv['L0']['D4ML0']['quse'], mn0('D4ML0', 1)),
                        vs(uv['L0']['D4L0']['quse'], min(xl) if xl else None), vs(uv['BP'][1], mn0(None, 4, 'A2'))))
    hdr = ['# P2_12_JOINT_RECORD_v1%s (pk12 %s): R6.5\'s per-row marks (pass iff lo_lo > 0 at every evaluated piece); the smallest '
           'lo_lo/Cov_hi with its piece, and the smallest headroom (INFO).' % ('_MOCK' if MODE == 'mock' else '', LABEL),
        'RECORD = P2_12_JOINT_RECORD_v1', 'FORMAT = S4U_KV_v1', 'EXPORT_STATUS = %s' % ('MOCK' if MODE == 'mock' else 'CERTIFIED'),
        'CODE = pk12/%s.py:%s' % (LABEL, OWN_SHA), 'INPUTS = %s' % DIGEST, 'COVERAGE = N4 %s ; N3 %s' % (status[4], status[3]),
        'CLAIM = lo_lo > 0 at every evaluated piece; headroom INFO; no Cov/2 threshold',
        'U_VERTICAL = N*_TRB r / 2 per piece (rv02/CONFIRM_UV_VERTICAL_BOND_rv02.md:851f6ba4 sect. 3: positivity, the trace bound, '
        'Bhatia-Davis)',
        'STANDINS = %s' % (', '.join(es_standins()) or 'none'),
        'R_FORMS = d_L <= 0: Cov_main with R_X + |m_e| R_f + |m_f| R_e + R_e R_f (rv02/ERRATUM_ESEMI_TRUNCATED_COV_V2_rv02.md:4f34050b) '
        'in D_u units with F-A, F-B, J-1, J-2 and the TD single-bond g-terms (rv02/RULING_T202_QS_TD_SG1_V2_rv02.md:141eb691); '
        'D3 at d_L = 0 by Route 1, the vacuum main term with all of Q0 b(d_R - 1) in R (rv02/RULING_D3_DL0_CHAIN_LEVEL_rv02.md:90d302d8; '
        'C-LEVEL); the TD bb tail Y tau_1(L), tau_1 = C_N tail_h1 (pk15/NOTE_J3_TAIL_ONESIDED_G1_v1.md:ed0ae46c, '
        'rv02/CHECK_J3_TAIL_ONESIDED_G1_rv02.md:53ec0d98; C_4 <= %s, C_3 <= %s); at d_L = 0 the damped q (D3, D4M) and D3\'s Q1, Y_1, '
        'Y_c and route (ii) t term (rv02/SCOPE_D3_DL0_SHARP_Q_rv02.md:1ab6f209; C-Q-DAMP); Route 1 two-sided, the N-error with Z* at '
        'both ends of X and of the single bonds (rv02/RULING_TWO_SIDED_DAMPING_V2_rv02.md:83db00da; C-TWO-SIDED); d_L >= 1: lo less '
        'the crude |m_e| |m_f| (4f34050b sect. 3)' % (fstr(G['CN'][4], 20), fstr(G['CN'][3], 20)),
        'CERT_OK = %s' % ('TRUE' if (MODE == 'cert' and all(status[n] == 'COMPLETE' for n in (4, 3))) else 'FALSE'),
        'FAILING_ROWS = %d%s' % (len(failing), (' ; ' + ' '.join(failing)) if failing else ''),
        'FIELDS = N family d_L d_R type worst_lo_over_Cov_hi worst_piece worst_headroom_INFO mark']
    body = ['N%d %s %d %s %s %.9g %d %.9g %s' % (k[0], k[1], k[2], k[3], v[3], v[0], v[1], v[4], v[2]) for k, v in sorted(marks.items())]
    PENDING_REC.append((REC_PATH, '\n'.join(hdr + body + ['END = P2_12_JOINT_RECORD_v1']) + '\n', len(body)))
    out('JOINT-RECORD: prepared (%d row lines, FAILING_ROWS %d); written only after the last gate with VERDICT VALID' % (len(body), len(failing)))


DIGEST = ''
STAGEA = ([], [])   # v1_3_2: run_A's stage-A failing and no-fire lists, kept
try:
    A = mod.run_A(STAGEA[0], STAGEA[1], plants=False)
    G['RSTART'] = A['RSTART']
    load_all()
    DIGEST = inputs_digest()
    out('INPUTS %s' % DIGEST)
    out('CLAIM (v1_3_1): a row passes iff lo_lo > 0 at every evaluated piece; the headroom and lo_lo/Cov_hi are '
        'INFO; break-evens at lo = 0 (be) and at h = 1.2 (be12, INFO)')
    out('C-S8-STAGEA (v1_3_2): run_A\'s stage-A lists come back empty (failing %s, not firing %s) -> %s' % (
        sorted(set(STAGEA[0])) or 'none', sorted(set(STAGEA[1])) or 'none', gate('C-S8-STAGEA', not refuses(stagea_ok, *STAGEA))))
    out('PLANT-S8-STAGEA: one injected stage-A failure must be refused -> %s' % plant(
        'PLANT-S8-STAGEA', refuses(stagea_ok, STAGEA[0] + ['C-RANGE'], STAGEA[1], tag='C-S8-STAGEA')))
    if MODE == 'mock':
        out('MOCK INPUTS: the u-hat records %s (pk02\'s kt_uhat_asm_v1_5, EXPORT_STATUS MOCK, interface v1_4); tau_1 reads the certified '
            'kappa_max and Phi_eps in both modes (v1_3_5_4, C-TAU1); the d_L <= 0 base is Cov_main from pk04\'s MOCK E_main records '
            '%s, with R_e and R_f in under the MOCK stand-ins %s, and the t = 0 Cov (stand-in) at the rows without a record; every other '
            'input certified' % (', '.join('N%d %s' % (n, sha_file(uhat_path(n))[:8]) for n in (4, 3)),
                                 ', '.join('N%d %s d_L %d %s' % (k[0], k[1], k[2], sha_file(p)[:8]) for k, p in sorted(ESM.items())),
                                 ', '.join(es_standins()) or 'none'))
    if ITEM == 'pre':
        run_pre(A)
    else:
        for N in (4, 3):
            prepare_uhat(N)
        if ITEM == 'grid':
            run_grid(A)
        elif ITEM == 'chunk':
            run_chunk(A)
        else:
            run_final(A)
except Exception as ex:
    out('ERROR %s: %s' % (type(ex).__name__, ex))
    for ln in traceback.format_exc().splitlines()[-16:]:
        out('TRACE ' + ln)
    fails.append('ERROR')
out('C-PREC: flint ctx.prec %d at the end, the cert module\'s PREC %d -> %s' % (mod.ctx.prec, mod.PREC, gate('C-PREC', mod.ctx.prec == mod.PREC)))
out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (ITEM, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
out('GATES: failing %s; PLANTS: not firing %s' % (sorted(set(fails)) or 'none', sorted(set(nofire)) or 'none'))
if PENDING_REC and not fails and not nofire:
    rp, txt, nb = PENDING_REC[0]
    with open(rp, 'x') as fh:
        fh.write(txt)
    out('RECORD %s sha256 %s' % (os.path.basename(rp), sha_file(rp)))   # v1_3_4: the ruled form, on its own line
    out('JOINT-RECORD %s: %d row lines' % (os.path.basename(rp), nb))
elif PENDING_REC:
    out('JOINT-RECORD: not written (failing %s; not firing %s)' % (sorted(set(fails)), sorted(set(nofire))))
out('VERDICT %s' % ('VALID' if not fails and not nofire else 'INVALID (%s)' % ', '.join(sorted(set(fails + nofire)))))
