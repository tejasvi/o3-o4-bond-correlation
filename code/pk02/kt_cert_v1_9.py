#!/usr/bin/env python3
"""kt_cert_v1_9.py -- pk02 (code/pk02/). REVISION of kt_cert_v1_8.py (2bd634d6; production 60/60 VALID) for
DESIGN_KT_CERT_v1_9.md (668529c4): every FLOAT-IN input of piece g certified (the word of 2026-11-08). Changes, and nothing else:
  (1) far: far_cert reads FAR_CRUDE_v1_N<N>.json through far_crude_reader_v1.load (NOTE_FAR_CRUDE_v1 6b0693f0; the option (b)): far_mixed's
      sum hf^2 X_SS + 2 hf sum_g |m_g(t)| X_S_g + sum_{g<=h} w_gh |m_g(t)| |m_h(t)| X_D_gh with each X(300) <= its record's X300 (exact) and
      R = 1 exactly (matrix-tree): logR is gone. Part 4b (outer_far3, gB_base, factors_for, src_factors, riglap2/riglap3, amom2b,
      npoly, ive) is removed; C-NORIG asserts none of those modules is loaded (the packing audit 89f7a0d0 item (1)).
  (2) gBb (certified): (sum_r e^{-0.95 J (1 - cos 40 deg)} ratio_main_r zR_r^up)^{1/2} at J = 300, zR_r^up ADD4's J-uniform upper form of
      pk03's vacuum items G4R_r (m3_reader_v5.load bound to the asm output; a_0 = 1 exactly), ratio_main_r in arb with the exact
      couplings (m2b_asm_v1's ratio_main and j_uniform). gB = supF_a(kind, 300) gBb as before.
  (3) eps_r (certified): M2B_KV_v1 through m2b_reader_v1.load (binding, C-PINS) and law_v1(rec, N, 300), the upper end of its decimal
      (kt_rb_v1_6's read_m2b); lambda~_0 = (1 - eps_r) mhat as before.
  (4) Z (certified): the S9 records (J_REF 300) through m3_reader_v4_4.load bound to their asm outputs: Z_b = sum_k LO_k 300^-k - err_b of
      entry G,b,b (b = 0 for t, h, a, am; 1 for e1, h1; 3 for e3, h3), a lower end; C-Z requires Z_b > 0.
  (5) RESULT reads 'FLOAT-IN none' (C-NOFLOAT, PLANT-NOFLOAT); a CERT-IN line names the four sources. VALUE drops its FLOAT wording.
  (6) pieces: v1_9 runs g (12 items) and cN2 (kinds t, e1, e3, h; the review v1_8 N-2): cN2 runs kt_cert_v1_8's own construction of D4 and its
      per-order parts D4_k (importing the pinned kt_cert_v1_8.py), checks every D4_k against the bounds of piece c's tables
      (tot, deg2, max(qdeg, 1)), ties D4 to v1_8's c hand-off (term count, deg2, tot, orders), prints per-order counts and exponent digests,
      and writes a hand-off that g requires. c and the tail pieces are kt_cert_v1_8's certified runs: producer() names kt_cert_v1_8 (full
      sha256 pinned, its records pinned in V18REC) for c, tX0-tX2, tB, tA; g never computes them in-line. PLANT-PRODUCER also relabels c.
  (7) N-1: g's C-MAJ-SAMPLE gains 'L0 pi_state <b> j' cells for every non-psi state of the kind's basis.
  (8) mono() raises ValueError when an exponent >= BB, before packing (packing audit item (2)); PLANT-NPGUARD.
  (9) C-REP-V18: g's near parts (nP, nD, nR0 balls; tailX, tailB, ann printed) against kt_cert_v1_8's g records (pinned); gB and far are
      printed beside v1_8's FLOAT values (INFO).
  (10) names: records out_kt_cert_v1_9_*, hand-offs hand_kt_cert_v1_9_cN2.*, header, HEAD and FORMAT name kt_cert_v1_9.
  (11) the design review: cN2 imports kt_cert_v1_8 itself, its part 4b imports bound to inert
      stubs (C-CN2-V18, C-NORIG), with PLANT-CN2 (a D4_k with one monomial past tot must fail); INPUT lines give the full sha256 of every file a
      piece reads; look-alike refusals PLANT-FAR-HAND, PLANT-VAC-LOOK and PLANT-S9-LOOK (format _PRECERT, _STUB, _MOCK, with an accepted
      control); C-R1 computes R = 1 exactly in Q(sqrt 5, sqrt 21) from the matrix-tree determinants (PLANT-R1); the FORMAT line drops
      CERTIFIED, which only a g piece's final STATUS line carries, and only when every gate passed and every plant fired.

kt_cert_v1_8 was: pk02 (code/pk02/). REVISION of kt_cert_v1_7.py (efe4c40d; production 20/20 VALID) for the two trade fixes
(the radius trade gives a lower bound on monomials with c < 0; the annulus was traded with a_e
where t X'' <= a_pp) with the fix main chose ('prop' 253a52c3; the shared module majfix_v1_1),
and M4's law, stage 1 (DESIGN_M4_LAW_v1 e494e4c5 sect. 4). Changes, and nothing else (DIFF_kt_cert_v1_7_to_v1_8.txt):
  (1) the majorants, from majfix_v1_1 in balls: built untraded (M3's form: xibar l = 0 is Q/2 + t cfac d/8, pi_vac's terms carry
      t^(i - l)), in the form basis (d_uv atoms, a formal t), evaluated after the cap; nothing coefficient-wise happens after evaluation
      (Dbar multiplies by hk's products, whose D2 Mk factors are >= 0 pointwise; no gate reads their expanded coefficients):
        D4 (piece c): capped at TOT - maxdeg(Y[4 - j]), TOT = max(today's D4 total degree, 10): t, h today's 10; e1, e3 one more than
          today's 9, where no step is taken (CondMomA at Dc 10 for e1, e3, as for t); C-DEG stops the piece above the budget;
        the L0 side R0 (g) and the a-engine (g of a, am): untraded (Wishart only);
        ann's pi0'' (tA): capped at today's degree with the annulus radii (a_pp on sigma'');
      a cap step lowers an X (smallest radius first), else a Q, else splits one atom (the largest pair) into X_u^2 + X_v^2, each step consuming
      one formal t; the radius vector is passed explicitly and asserted (C-RADV). The old trade stays only for today's degrees and the plant.
      t-monotonicity: each capped pis_j has coefficients >= 0 in (X, Q, d, t) and the cap's choices depend only on exponents and
      budgets, never on t, so it is nondecreasing in t on the chart; C-TMONO certifies the coefficients in the form basis before substitution.
  (2) gates (before the piece computes, pieces c, tA, g): C-RADV and PLANT-RADV (today's AVt on the annulus must fail), PLANT-TRADE-POS (the
      d-expanded D2 must trip C-TRADE-POS), C-P0SUB (xibar, inner and outer, l = 0..5, evaluated vs the direct expansion), C-MAJ-SAMPLE on the
      majorants the piece uses (D4's capped pis, ann's pi0'' at annulus points, the L0 pi_vac, the a-engine's pis; 500 seeded points plus
      the fixed points, tau0 in {0, t/2, t}) and PLANT-MAJ-SAMPLE (today's xibar l = 0 must fail); C-TRADE-POS stops the piece on a
      coefficient ball not certainly >= 0 (VERDICT INVALID (C-TRADE-POS)); C-TMONO at the end.
  (3) nD per formal-t order (piece c): D4 = sum_k t^k D4_k, nD_k = (t^4/24) detf (n2 E2(ED_k, ED_k))^{1/2} on the same CondMomA table, one
      conditional expectation per order; C-NDK (their sum not certainly below nD); hand-off rows 'NDK k ball'; M4's per-order law
      nD(J) <= sum_k (300/J)^(4 + k) nD_k(300) (Minkowski per order with the key fact) takes their upper ends.
  (4) C-REP-FIX in place of C-REP: piece c's nD and nD_k and piece g's nP, nD, nR0, tailX, ann (a, am: nP, nR) against the majfix twin
      kt_c_t_trade_v1_3 (mode prop, the same algorithm in binary64), its J = 300 JTERMS2 and NDK lines (FIXREFS, full sha256; header and
      VERDICT exact): 1e-9 relative, printed %.6e values 1e-6; tailB is not compared (the twin's chi3 form against this engine's F1 form).
  (5) producers: only x is read, from the VALID runs that made it (kt_cert_v1_7 for t and am; kt_cert_v1_6 for e1, e3, h, a); its path has
      no trade. PLANT-PRODUCER. c, the tail pieces and g are this file's.
  (6) items: kinds e1, e3, t, am (M4) and h, a (kt_rb's A_h, A_a) at n4 and n3; pieces c, tX, tB, tA, tX0..tA2 and g (a, am: g only).
      h1 and h3 are not re-run: nothing live reads them, and RECORD_INDEX_F2_pk02.md marks their g records withdrawn under F-2.
  (7) M4 stage 1: tail pieces X and B also give the Minkowski-per-order term (rows TAILM, C-TAILM, PLANT-TAILM); g gives nP's orders M_k
      (C-NPK, PLANT-NPK), the tail bases TXm, TBm, and the LAWBASE line (17-digit upper ends, with nD_k) for m4_asm_v1; FLOAT-IN unchanged
      (stage 2, kt_cert_v1_9, replaces it).
  (8) lambda~_0 stays (1 - eps_r) mhat: Lemma 19.2 (c) (Rayleigh quotient; the angle enters only the upper side).
      lambda_0 enters only through this lower end (R_e = bound/(lambda~_0 Z_e^{1/2}) in engine_value; K-EIG compares m_diag with the
      float lam0 as a check and bounds nothing); no upper end of lambda_0 is used here, in kt_c_t_trade_v1_3 or in M4's law (D_k).
  (9) names: records out_kt_cert_v1_8_*, hand-offs hand_kt_cert_v1_8_*, header, HEAD and FORMAT name kt_cert_v1_8.

kt_cert_v1_7 was: pk02 (code/pk02/). REVISION of kt_cert_v1_6.py (7e48fd63; production 12/12
VALID), for P2-1's certified step (DESIGN_KT_CERT_v1_7.md 8d5560f5; the approval 2026-11-07): kinds t and am, the hunks of pk15's float fork
kt_c_t_v1_1 (DIFF_kt_c_v2_3z_to_kt_c_t_v1_1.txt 0fa97202) ported to the arb engine, on the same z9sym pins, kernel and precision. Changes,
and nothing else (DIFF_kt_cert_v1_6_to_v1_7.txt lists every line):
  (1) kind t (h-type pieces x, c, tX0-2, tB, tA, g): the top-row insertion source xi_t p0(xi''), xi_t = J(1 - sigma_T . sigma''_T), projected
      on P_4 = (psi, e1, e3, e2). ROWX = 0 for t (1 otherwise) puts the cross form on row T in W10 and W10_INT (the exact-zero rule reads
      W10_INT), and MAP10 maps QT for t (QH otherwise); pi_t is pi_h with xibar_cross(XS[0], XD[0], ...); T3 = EL xit pD['psi'] with
      xit = xi_pair(XS[0], XD[0], QT); t joins HOOK (sup|F| = 2J supp0, |xi_t| <= 2J on the outer far part, pi_t in source_pis and pi0'').
  (2) kind am (a-type pieces x, g): the odd vertical source E0 ((xi_TM - xi_MB)/2) p0 projected on (e2,); a_engine(J, ex, sgn) with the far
      parts' xi factor [0.5, 0.5 sgn] (sgn = -1 for am; the majorants use |coefficients|, so am's majorants are a's).
  (3) bases per kind: (psi, e1, e3, e2) for t, (e2,) for am, (psi, e1, e3) otherwise; pS gains 'e2'; the projections, the x hand-off rows
      and parse_x run over len(G); factors_for, pi_state's maps and l0_remainder know e2 (b = 2).
  (4) checks: K-T0 (|r0(t)| <= 1e-8 and t's psi coefficient against nn (1 - 1/(2 sqrt 21) - 1/(2 sqrt 5))/2 to 1e-9 relative); K-AM0
      (|r0(am)|_B0 <= 1e-8); C-KTC0 (t's C = |r1|_B0, from the midpoint of the B0 ball since the printed upper value can be loose, against
      out_kt_c0_v1_1's READ C_t, two-sided to 5e-7 relative as kt_c's K-C0); K-INV for t as for h.
  (5) C-REP of the g pieces of t and am against pk15's out/out_kt_c_t_v1_1_<kind>n<N>.out (TREFS, full sha256 from its
      MANIFEST_STB_P2_PREP_v1_2); C-REFHEAD requires the header 'kt_c_t_v1_1 sha256 <full> ITEM=<kind>n<N> ' and VERDICT lines equal to
      exactly ['VERDICT VALID'].
  (6) records (pk15's reader, T48): every record prints 'FORMAT KT_CERT_RECORD_v1_7 CERTIFIED' and 'KERNEL arbeng_c2b_v2.py <sha256>
      ctx.prec 512'; the g pieces print 'RESULT N=<N> J=300 <kind>: <name> [lo, hi] bound [lo, hi] FLOAT-IN <tokens>', 17 significant digits
      rounded outward and checked in arb.
  (7) rep_check's docstring: B_ref's rounding is up to about 5.5e-7 (e3n4), not 7e-8.
  Not changed: make_B0c keeps AllMom2A without W_int (its printed B0 norms can be loose upper values; they never enter the bound), so the
  old kinds' code paths stay byte-identical; C-REGR reruns x.hn4, tX0.hn4, x.an4 and g.an4 and compares them with kt_cert_v1_6's.
  Names: records out_kt_cert_v1_7_*, hand-offs hand_kt_cert_v1_7_*; nothing of kt_cert_v1_6 is read.
kt_cert_v1_6 (7e48fd63) was the REVISION of kt_cert_v1_5.py (bf1995af), on the
decisions of 2026-11-07: one trial set (z9sym) in every certified run, production C-REP against float prints on that set, the e1n4 replay
smoke, eps_r and Z left as FLOAT inputs of VALUE. The engine, the precision, the pieces and the gates are kt_cert_v1_5's. Changes, and
nothing else:
  (1) Trial set z9sym (pk11 zero_states_v2_1, record out_zero_states_v2_1_all.out 168106e0 VALID) for the twelve production items
      <kind>n4, <kind>n3 (kind e1, e3, h, h1, h3, a): ts_N4_J170_D_S_z9sym_v1.json, ts_N3_S_z9sym_v1.json, vacres_K3_N4_sym_v1.json and
      vacres_K3_N3_sym_v1.json, read from code/pk11/out/ and pinned in TRIAL (C-HASH). z9sym zeroes the S entries below 1e-9 (states 1-3
      become exactly linear in xi, state 0 constant) and symmetrizes; kt_c_v2_3z (f2497cf7, 8/8 VALID) printed every engine value of
      kt_c_v2_3 unchanged on it, with e1's and e3's D4 down from 34353 terms to 6463 and 11354.
  (2) C-REP on z9sym: the g pieces of e1, e3, h and a at N = 3 and 4 compare with kt_c_v2_3z's prints (out/out_kt_c_v2_3z_<kind>n<N>.out,
      pinned in REFS). C-REFHEAD, inside C-REP: the reference's first line names the float engine's sha256 and this kind and N, and its only
      VERDICT line is VERDICT VALID. h1 and h3 have no float reference, as in kt_cert_v1_5.
  (3) smoke = the e1n4 REPLAY on kt_cert_v1_5's pinned inputs (INPUTS, unchanged): C-REP against kt_c_v2_3's print as before (now with
      C-REFHEAD), and C-REPLAY against kt_cert_v1_5's VALID g.e1n4 record (08d26e20, pinned in PREV; header and VERDICT checked). That record
      prints balls for the bound, nP, nD, nR0, far and the value, and 4-digit upper values for tailX, tailB, ann and gB: each ball, widened by
      its print rounding, must overlap this run's ball, and each upper value must agree to half a unit of its last digit. hsmoke and
      PLANT-HOOK0 are dropped (the hook code is unchanged, and h passed C-REP in kt_cert_v1_5's production).
  (4) eps_r (vacscale) and Z (kt_s9b_v1's J = 170 entries) stay FLOAT inputs of VALUE. Both come from the old trial set and are marked
      indicative on the FLOAT-IN and VALUE lines; W2 v2 assembles S9(c) from the bound records with M2(b)'s certified eps_r and M3's
      certified Z on z9sym.
  h1 and h3 run on kt_cert_v1_5's code unchanged: the explicit part still requires T3's degree to be at most Dc = 2 KX + 2 (kt_cert_v1_5's
  x.h1n4 stopped there on the old trial set); kt_h1probe_v2 counts z9sym's degrees and table sizes before production.
  Names: records out_kt_cert_v1_6_*, hand-offs hand_kt_cert_v1_6_*; of kt_cert_v1_5, only the g.e1n4 record is read (by the smoke).
kt_cert_v1_5 (bf1995af) was the REVISION of kt_cert_v1_4.py (f414c3b9), on
kt_radprobe_v1 (920034c7; output cfa355c6, VERDICT H SUPPORTED) and the pre-approval. Changes, and nothing else:
  (1) The joint tail tables use arbeng_c2b_v2 (arbeng_c2b_v1 a70d0cc4 plus one option): the ten forms span six coordinates, and a subset A
      with exact integer rank(W10[:, A]) < |A| has det(Gam_A) = 0 for every G, so AllMom2A leaves it out (its det ball must contain 0).
      kt_cert_v1_4's X2 table had singular minors with det balls [+/- 0.556] at 256 and 512 bits alike (row-pivoted elimination, then a
      Hadamard bound over the remaining rows), which gave X2 its relative radius 1.1e-11 (e1) and 1.5e-4 (h). C-SING checks every table:
      the kept det balls are identical to the direct computation, the dropped subsets are rank-deficient with det balls containing 0, all
      allowed subsets are covered, and degree-4 tables with and without the rule overlap. PLANT-SING (W10's X0 column zeroed) must stop.
  (2) S1: C-REP's reference bound also replaces v2_3's tailB with this engine's.
  (3) S2 (same review): the gate C-R, |log R| <= 1e-10, in the g pieces of engine A.
  Names: records out_kt_cert_v1_5_*, hand-offs hand_kt_cert_v1_5_*; nothing of v1_2, v1_3 or v1_4 is read.
kt_cert_v1_4 (f414c3b9) was the REVISION of kt_cert_v1_3.py (31e29648; never run), on
the decision after kt_cert_v1_2's smokes (xsmoke 3e73c02a, gsmoke 49cb6c93, xhsmoke 7a3296b0 VALID; ghsmoke 7af1e21d INVALID by C-RAD
only: the bound's relative radius 8.4e-12, from the tail tables, whose moment recursion and E2 lose about 70 digits at 256 bits).
Single change: ctx.prec = 512 in every piece (SPEC_M1_CERT_v1_1_ADD2_v1_3), with the file, record and hand-off names kt_cert_v1_4.
Everything else is kt_cert_v1_3's, as the rest of this docstring describes.
kt_cert_v1_3 (31e29648) was the REVISION of kt_cert_v1_2.py (6e476206) on the REVIEW of kt_cert_v1 (f8c685eb)
and its ADD1 (f71ae3e8); the spec side of F1 and F2 is SPEC_M1_CERT_v1_1_ADD2_v1_2. Changes:
  F1  tailB is an L2 bound: tailB = (sum_r e^{-lam J kappa} N_r E_r[T^2])^{1/2}, E_r under the Chernoff tilt lam Q_rr'' = lam |x_r - x''_r|^2,
      passed to the joint tilted covariance as an extra quadratic form (three joint-moment tables, each guarded by surely_pd), as tailX does
      for X''_v. kt_cert_v1_1's normT sum_r P(B_r)^{1/2} (and its base table) are gone.
  F2  far_out keeps every cross term: hf^2 o4/R + 2 hf sum_g |m_g(t)| o3_g + sum_{g,g'} |m_g(t)| |m_g'(t)| oD_gg' (hf = 2J for the hook kinds,
      else 1), o3_g by outer_far3 on G3 (vacrig11f's E3: the source column 0-2, phi_g on 6-8) and oD_gg' on D, with mixed factor lists;
      kind a: all three kinds of term on D. R = main_N^2/(main_D main_4) from riglap2's main terms (FLOAT, printed; kt_c_v2_3 took R = 1).
      The A1 note's Minkowski step is withdrawn (ADD2 v1_2).
  F3  P = r0 + t r1 + t^2 r2 + t^3 r3 for every kind (engine A and the a-engine).
  F4  every FLOAT number the bound uses is printed with repr (the far parts and log R, gBb, eps_r, Z's inputs); far_out is formed in arb.
  F6  nsqrt stops the item on a certainly negative ball.
  (F5, at the source) VALUE and F2A print a 10-digit decimal that arb checks to be >= the ball.
  Pieces. Engine A is cut into stages, and an item <suffix> (e1n4 ... an3; smoke = the e1n4 replay) runs as pieces <piece>.<suffix>:
    x   the explicit part (orders 0-3: the m_g and r0..r3), written to a hand-off;
    c   D4, its conditional expectation and nD (optional);
    tX, tB, tA, or tX0 ... tA2 (one table each)   the Chernoff tables of tailX, tailB and ann (optional);
    g   reads x's hand-off and the hand-off of every optional piece that was run, computes in-line each stage whose piece was not run, then
        the L0 remainder, nP, nR0, far_out, gB, the bound, the value and the checks. Kind a: x and g only.
  Hand-offs (part 6): own folder, created once, under 2 MB, an END line with the body's sha256. The producing piece prints the file's sha256 in
  its record out_kt_cert_v1_6_<piece>.<suffix>.out. The reader requires that record's VERDICT VALID, and checks the file's sha256 against
  the record, the body checksum and the header (this script's sha256, piece, kind, N, precision). PLANT-HANDOFF (g): three tampered copies in
  memory, each caught by its own check. STAGE-CPU lines after every stage; C-TILT (b) in every piece but x.
  C-REP: tailB is not compared (F1); the bound is compared with v2_3's bound after v2_3's far is replaced by this engine's far_out (F2).
kt_cert_v1_2 (6e476206): kt_cert_v1_1 split into an x and a g process, with STAGE-CPU lines. kt_cert_v1_1 (91be74ce): its smoke (eb3e055d)
passed C-TILT, PLANT-TILT and the explicit part (140 s) and stopped at its 540 s cap inside engine A.
kt_cert_v1_1 was the REVISION of kt_cert_v1.py (3e1f2d4e) on the ADD2 review (43eb7b39), item A5, with the A1 note
SPEC_M1_CERT_v1_1_ADD2_v1_1 (34722fc0: the quadrature (near^2 + far_out)^{1/2} is exact; no engine change). New: C-TILT, in arb, before the engine:
  (a) domination: each tilt rate meets rate >= -log(1 - a)/(2a) for its radius (c_m: a_m, c_e: a_e, c_pp: a_pp), and a_pp >= sin^2(asin rho_m +
      delta); (b) admissibility: every tilted covariance the engine forms (tilted_cov_a, the Chernoff lambda tilts of the tails and the annulus,
      and A - 2 c_e t I) is certainly positive definite (logged with its smallest leading minor; a failure stops the item as before) and every
      Chernoff lambda is positive. PLANT-TILT: (a) with c_m (1 - 1e-9) and (b) with a lambda = 1e3 tilt must both fail.
  Everything else is kt_cert_v1's.
kt_cert_v1 (pk02, code/pk02/): M1 of SPEC_M1_CERT_v1_1 (c81c956f) with ADD1 (badf0f57) and SPEC_M1_CERT_v1_1_ADD2_v1 (ddd85cfd):
engine A (KT-C) in ball arithmetic (python-flint arb; no *_series function), ported from kt_c_v2_3.py (71a224a2) part for part, with the xi hook
(kinds h1 = xi_h p_e1, h3 = xi_h p_e3; h = xi_h p0 is kt_c_v2_3's kind) and the F2(a) / C-BAD lines of ADD2 v1 sect. 6 and 8.
Built from pk01's scratch parts p1, p2a, p2b1, p2b2a (copied read-only as SRC_pk01_kt_cert_v1_p*.py) and its port map; arb layer
arbeng_c2b_v1.py = pk01's arbeng_v1.py draft (a70d0cc4), frozen under this name.

Model (ADD2 sect. 1): every certified quantity is an arb ball; exact binary64 inputs (json data, radii, the m_g) are exact balls; the couplings A, B,
  X0, Y0 and DELTA are computed in arb; covariances come from arb_mat Laplacians with an exact gauge basis; index arithmetic is numpy int64.
  Precision: ctx.prec = 512 (kt_cert_v1_4, ADD2 v1_3; ADD2 sect. 1 named 128 to 256 bits, and kt_cert_v1 to v1_3 used 256). C-RAD gates the
  outcome.
  Free choices, exact binary64 from the point they are made: the m_g (midpoints of ball solutions; any real m_g is allowed, (C1)), the radii
  RHO_M, RHO_E, the Chernoff lambdas 0.45 and 0.5. Derived parameters rounded UP from their arb values (pk01's C-RATE, C-APP): the tilt
  rates c_m, c_e, c_pp and the annulus radius a_pp.
FLOAT inputs (ADD2 sect. 3), printed with repr and marked: the outer far parts (with the cross terms and log R) and gB (riglap2/riglap3,
  part 4b; M3); eps_r (vacscale; M2) and the Gram lower bounds Z (kt_s9b_v1's J = 170 entries; M3), on the FLOAT-IN lines.
Items: <piece>.<suffix> as above, J = 300: the twelve production items on z9sym, and smoke (the e1n4 replay on kt_cert_v1_5's inputs).
  C-REP on the g pieces of e1, e3, h and a at N = 3 and 4 (against kt_c_v2_3z) and of the smoke (against kt_c_v2_3): each compared part to
  half a unit of its last printed digit (the float engines print them with 3 or 4 digits), the bound to 1e-6 relative as above, C-REFHEAD
  inside it. C-REPLAY on the smoke's g piece. C-RAD: relative radii of the bound, nP, nD, nR0 (nR) at most 1e-12.
Prices [E], from kt_cert_v1_5's production records at 512 bits on the old trial set (CPU s per piece; e1n4: x 173, c 229, tX0-tX2 64, 60, 61,
  tB 190, tA 0.3, g 17; hn4: x 155, c 244, tX0-tX2 37, 39, 36, tB 111, g 17; an4: x 35, g 74). z9sym lowers e1's and e3's D4 degree
  (kt_c_v2_3z), so their c and tail pieces should cost less. Every piece runs under LIM <= 540.
Run (own folder; kt_cert_v1_9: cN2.<suffix> before g.<suffix> for kinds t, e1, e3, h): D=/mnt/g2/release/root/code/pk02;
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=$D/tmp_kt_s9b3 OMP_NUM_THREADS=1 timeout 580 nice -n 10
  prlimit --as=8589934592 -- python3 -I -B $D/kt_cert_v1_9.py <item> <LIM> > $D/out_kt_cert_v1_9_<item>.out
  2> $D/out_kt_cert_v1_9_<item>.err
"""
import resource, sys, time, math, hashlib, signal, os, traceback, re, json, itertools
import io, contextlib, types                     # kt_cert_v1_9: cN2 imports kt_cert_v1_8 itself (the review a50a005a Q1 (a))

SUFFIXES = tuple(k + s for k in ('e1', 'e3', 't', 'am', 'h', 'a') for s in ('n4', 'n3'))   # kt_cert_v1_8: M4's four kinds, and h, a (kt_rb)
TAILP = tuple('t' + f for f in 'XBA') + tuple('t%s%d' % (f, i) for f in 'XBA' for i in range(3))
CN2KINDS = ('t', 'e1', 'e3', 'h')                 # kt_cert_v1_9: the kinds with a piece c (the review v1_8 N-2)
ITEMS = tuple('g.%s' % s for s in SUFFIXES) + tuple('cN2.%s' % s for s in SUFFIXES if s[:-2] in CN2KINDS)   # v1_9: c, tails from v1_8
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: kt_cert_v1_9.py ITEM LIM   (ITEM = g.<suffix> or cN2.<suffix> (kinds t, e1, e3, h), suffix <kind>n4, <kind>n3 (kind e1, '
          'e3, t, am, h, a); x, c and the tail pieces are read from their producers; LIM = RLIMIT_CPU soft limit in s, hard LIM + 5)')
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,4}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r (need 5 <= LIM <= 540)' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
STAGE = ['start']


def cpu():
    return time.process_time()


def out(line):
    print(line, flush=True)


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)


class CapStop(Exception):
    pass


SCR = '/mnt/g2/release/root/code/pk10/scripts'
INP = '/mnt/g2/release/root/code/pk10/scratch'
SRC = '/mnt/g2/release/root/code/pk01'
OWN = '/mnt/g2/release/root/code/pk02'
WOUT = '/mnt/g2/release/root/code/pk11/out'      # kt_cert_v1_6: the trial set z9sym (read only)
REFDIR = os.path.join(OWN, 'out')                                   # kt_cert_v1_6: kt_c_v2_3z's prints
ENGINE = {}                                       # kt_cert_v1_9: no pk10 module is imported (part 4b removed; C-NORIG)
W18 = '/mnt/g2/release/root/code'
V18_SHA = '2bd634d64511bf083a2104be0bdcffc7138a28a65125e4b50886245b5e2336f2'                            # kt_cert_v1_9: kt_cert_v1_8.py, the producer of c and the tail pieces
V19DIR = '/mnt/g2/release/root/code/pk02'                             # kt_cert_v1_9: where this file's pieces (cN2, g) write hand-offs and are read (the own folder)
CERTIN = {
    'pk02/kt_cert_v1_8.py': '2bd634d64511bf083a2104be0bdcffc7138a28a65125e4b50886245b5e2336f2',
    'pk02/far_crude_reader_v1.py': 'd657eac2c432007ed12c24566f3c72a8d5aced995d3013bb878606845356daf8',
    'pk03/m3_reader_v5.py': '44b95cfdd4dbffdeb8e970a9ef5dc6cd94320f89e36790a215f7dc710746956c',
    'pk02/m2b_reader_v1.py': 'a9f15db48e9fa51629448181d8a83679c1b93cd2b5696c8ed1e6b41d60df8b02',
    'pk03/m3_reader_v4_4.py': 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0',
    'pk02/M2B_KV_v1.txt': '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',
    'pk02/out/out_m2b_asm_v1.out': 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391',
    'pk03/out/m3_vac_N4_J150_v2_1.json': '5628ba351d2f0dbd0f36f463e3a3bc4c9c02b96d1c194e4f23098357988732a4',
    'pk03/out/m3_vac_v2_1_asm.4.out': '9cb620ecfba0ec3891455ef309e27c77bc666bdefb122b94061f582ae9a16473',
    'pk03/MANIFEST_m3_vac_v2_1_asm.4.sha256': '12accf80a35e40b3d86003679ee8f1a0890b6ad313c6ecff92dae8694d343333',
    'pk03/out/m3_s9_N4_J300_v1_8_3.json': 'bcc6434c6a03eecb232f10504b63f1ce10a94a489d5a2ba9cf3fe09c8018b831',
    'pk03/out/m3_run_v1_8_3_asm9.4.out': 'a41763a35f405668c748cdd1aaccfff681aacf5fb096342a791659ccb49c07a7',
    'pk03/MANIFEST_m3_run_v1_8_3_asm9.4.sha256': '79078c2f9a0ef392f03cc4ccbeeaba3f9fb99d311fa2f702637f9e268f4c51df',
    'pk02/FAR_CRUDE_v1_N4.json': '6ed3623cc97d872a05e486cab9fb9d9b12ba5e301c1e3a857d3970e444f6fbb4',
    'pk02/out/far_crude_v1.N4.out': 'c859c361eb0a34be0a30bcfc57f73d4d1875b891b3f6bcd439c8277e0aa4c38f',
    'pk03/out/m3_vac_N3_J150_v2_1.json': '57fbe83fb2640831768f3bc10d736653e423a5a7177099746afbf7a3d0f9f97a',
    'pk03/out/m3_vac_v2_1_asm.3.out': '27600d6dcb634a3c00af82f47ee013fcb7e949dd216899330618db90cdfac1c7',
    'pk03/MANIFEST_m3_vac_v2_1_asm.3.sha256': '9d664da26f170cb9a7f0266d744f8e8cf603f71540bdf11fecce75228da92cd9',
    'pk03/out/m3_s9_N3_J300_v1_8_3.json': 'd287d3dcbd4bd988aa8061fbe11b3da1609e0ab4d27ae1a619eadcee963e8fa5',
    'pk03/out/m3_run_v1_8_3_asm9.3.out': 'e7f09f7381919a8aef322adfae9ada7506bda4db527faba01b8deacdf6542655',
    'pk03/MANIFEST_m3_run_v1_8_3_asm9.3.sha256': 'b5f6ff01661279798afba898eb8788ac8abc94907ce5a474438265d68ddef5dc',
    'pk02/FAR_CRUDE_v1_N3.json': '596c4664a6465e3aa186a1810ee0625378bbc90616245512d2f78d1e81550bc9',
    'pk02/out/far_crude_v1.N3.out': '283e4fe77f36789f7009bc3d4b52f388bc9f1e4a8101860c3fdb3dcdd1b45396',
    'pk02/out_kt_cert_v1_8_c.tn4.out': '295bd8435af458130a1e9c35ed6446a66987d55a16eecfbd3d7614576741a73e',
    'pk02/out_kt_cert_v1_8_tX0.tn4.out': 'b71c672de7f6ed7d665c19a8ae3783a6a5af42feefc2b9bb122636e75b42c2ea',
    'pk02/out_kt_cert_v1_8_tX1.tn4.out': '7c1c4704558b77739b94a06f073e121f5d3b157e7171e51d283775a8314ffca6',
    'pk02/out_kt_cert_v1_8_tX2.tn4.out': 'e135e1ec6757f2099fab5dd75740f9934c5c3bf813310049b3ca7ac9d39c4d11',
    'pk02/out_kt_cert_v1_8_tB.tn4.out': '9a4784421d04987af70d8fc8f27ef3258974f9f4ac394b4590960736a5f04b0a',
    'pk02/out_kt_cert_v1_8_tA.tn4.out': '876d62facdf733f0796168e0c36c0a988a7487fec6e692c0ad099a6a2e45f71e',
    'pk02/out_kt_cert_v1_8_c.tn3.out': '8abb8068a45ef8c2ecab7b62ecc5435b2c0c573340e72cb2655c5b0eb9108a28',
    'pk02/out_kt_cert_v1_8_tX0.tn3.out': '013eac94b5355ff3214ba9f7eae434b1f7179d9413a85a98648e721f7fc141bf',
    'pk02/out_kt_cert_v1_8_tX1.tn3.out': '52c49c05b083ec0b235124c662cc6604f106aa0d1db560975aeb2f1c7b2169b0',
    'pk02/out_kt_cert_v1_8_tX2.tn3.out': '5e6c5a08135f5bfe33ced513b72a19bcc3cd162bf93186037dc029633a15e9a3',
    'pk02/out_kt_cert_v1_8_tB.tn3.out': '2eb77cdbb9a3c4e65306c7fd8b13c39306e86f69ee274dbf7f88149e62f1ad03',
    'pk02/out_kt_cert_v1_8_tA.tn3.out': '907a4c34a39a77e2c2522721c3d74044f517a8e0afc712b47d7e145f25fef600',
    'pk02/out_kt_cert_v1_8_c.e1n4.out': 'c3f0b0bde26a7f42b5bc0818da5f8e2e3f25e2955133dfdb88c30a3a65c43ad4',
    'pk02/out_kt_cert_v1_8_tX0.e1n4.out': '543abdac45c6f724b84c7b53adc590bf04ade761f53693f4ce27cf1e16832c85',
    'pk02/out_kt_cert_v1_8_tX1.e1n4.out': 'c1aa3fa4850468f9e1f597852396ce938e3ce667d5297f112c9d3efeeb1f0fce',
    'pk02/out_kt_cert_v1_8_tX2.e1n4.out': '95785502521c7dd3accb414902cac9ff3de836b0f8bbc3a556c4a9f8512fce2c',
    'pk02/out_kt_cert_v1_8_tB.e1n4.out': '2a8572127dfe1ef2b0f2ca997a451cfd311ecb8fac8cc5a7d3166ef3b1c79f26',
    'pk02/out_kt_cert_v1_8_tA.e1n4.out': '1e6faf5375950926735a027bdee6c0ca701a6e377e426ceb2372b26f63b39ea1',
    'pk02/out_kt_cert_v1_8_c.e1n3.out': '2d0359969b5431a55017fac9bd03907fd42e0f7f24fcff1cc25ae972bf96f4a0',
    'pk02/out_kt_cert_v1_8_tX0.e1n3.out': 'c9f8b79f37d8595e550e489330017ab35b58d9f03327d999e39933d44981aea4',
    'pk02/out_kt_cert_v1_8_tX1.e1n3.out': '1a66a1bd813cfdf4b03281e7f31b66b6d3a3cd5552c06dfa9950cd2f6c7e6af0',
    'pk02/out_kt_cert_v1_8_tX2.e1n3.out': '8300a55a6a6f9819558dee7b6e16921362ca776e7575c961136b4cd1debc7df8',
    'pk02/out_kt_cert_v1_8_tB.e1n3.out': 'ee1a9a1b85c10b1aabcf0dee55aad159ab66f7389c2fd704c8217d97182b15ba',
    'pk02/out_kt_cert_v1_8_tA.e1n3.out': '407bb457cb47b6898eb2510f4cfb9b099df948a96b8246e45e7539aa141693f3',
    'pk02/out_kt_cert_v1_8_c.e3n4.out': '6c31c32395b0b8d64f7d903686416b1c7b7dfa71dd0fcf4dcdf79715a847aa20',
    'pk02/out_kt_cert_v1_8_tX0.e3n4.out': 'b26fdb86148a66759a551d103271cd70e9fc5c6f95531d402bbb2536dfe7aac7',
    'pk02/out_kt_cert_v1_8_tX1.e3n4.out': '518e4918d09e6365fc9e5f977088379266ba1dc878434e283c7666d263ff40c0',
    'pk02/out_kt_cert_v1_8_tX2.e3n4.out': 'c55052347f8482a637c9749d6a8f41edb85416a2964f02560f73dd6e95db0e3a',
    'pk02/out_kt_cert_v1_8_tB.e3n4.out': '7537af5adf84e2d842e00aa1493802ab3d0b9ee1a76baa3c4e1fc67becc74682',
    'pk02/out_kt_cert_v1_8_tA.e3n4.out': '4630e09d529c8e4700f4c43d13a74129daa21a0ad3a9386fedccc4d6c3956020',
    'pk02/out_kt_cert_v1_8_c.e3n3.out': '5662bdae132cadf3c5fe5a56e2826a05cc7e2eb91d6902af773b3b4051fe170b',
    'pk02/out_kt_cert_v1_8_tX0.e3n3.out': '028d86be723d7119e38f11a3ef873eec969c37211a123bdf59e13b054df86c99',
    'pk02/out_kt_cert_v1_8_tX1.e3n3.out': 'd8b82c913246465da00aaa5d36a7292ae50555b61462b3c68f6a62d62db92f93',
    'pk02/out_kt_cert_v1_8_tX2.e3n3.out': 'da8fe36cdbcf412c6a99483c272a4773924100ad140cc0d8f4ea1171fd31dab3',
    'pk02/out_kt_cert_v1_8_tB.e3n3.out': '591f930dd423b1ae471437192b510171e665d7504f67bb86a19d704788411d79',
    'pk02/out_kt_cert_v1_8_tA.e3n3.out': '6e3b5dfd40ea51e6f93e22d1bbe55fe603b9fea5cd144acafa89e8588be98d25',
    'pk02/out_kt_cert_v1_8_c.hn4.out': '55728f4866228347f85300c349390e4a42179f52a32ac6c33720fa93d2c9d0d9',
    'pk02/out_kt_cert_v1_8_tX0.hn4.out': '1158028245854efbd6ad373556908912b70f171e4628de53d98a50c8cb93e715',
    'pk02/out_kt_cert_v1_8_tX1.hn4.out': '9a3d6b463287ec1054b5a493e8fd3cd7e70867036ae28c9f4c47d7bc83d4a1da',
    'pk02/out_kt_cert_v1_8_tX2.hn4.out': 'ace1e5521c8c2ea3b0eda3f62f3009a74220bb868252cc79b1c351e121c7bf73',
    'pk02/out_kt_cert_v1_8_tB.hn4.out': 'cceb7a7c9eba845b5acc45430d0331775e4b171ebb8633146c8b0fc1442d167f',
    'pk02/out_kt_cert_v1_8_tA.hn4.out': 'd2af51f19b6fd02aa8faf5107f7d6c6565cb190dede95c4cb3d506fe01a69638',
    'pk02/out_kt_cert_v1_8_c.hn3.out': '5f40936b2e3be7992c7f43d478ad5425d1fc0336d47d554b2774b06685641bf7',
    'pk02/out_kt_cert_v1_8_tX0.hn3.out': '353aedf87c9c3ac550f345f82c22847dd5e18d992dea2bb920f84341ebb59f9d',
    'pk02/out_kt_cert_v1_8_tX1.hn3.out': '5c42486bfb4542129b0042a770f2494372fbeaee2897dbc51d4468cb02d38af9',
    'pk02/out_kt_cert_v1_8_tX2.hn3.out': 'a58a561effd8b741fcda7ecc607923a471b11000674702b77245c9a05fba84bd',
    'pk02/out_kt_cert_v1_8_tB.hn3.out': 'ae81447051848e52b889f35078e74e7207231074b588d186323a5bc0619dee52',
    'pk02/out_kt_cert_v1_8_tA.hn3.out': 'c938a7aea185cd98603a575f3a298dcdfb02fd4afa9d20e5986112222e34dc0b',
    'pk02/out_kt_cert_v1_8_g.e1n4.out': '121618dfc020678995a4d5f845504e1bd054a275af9ec257b28dc5e9c597e9c9',
    'pk02/out_kt_cert_v1_8_g.e1n3.out': 'a5eadde0a3c51b2f477aad55ecf0029607baf7487f5ed65cdbe152a69c913475',
    'pk02/out_kt_cert_v1_8_g.e3n4.out': 'bd071e8bcc0544a6a23abbac570b694de217210e7c3f8711a3cdcac5819c65b1',
    'pk02/out_kt_cert_v1_8_g.e3n3.out': '99ce07c7a930e4b130e4e083d814c9ea3657bdd64884a282bbe7c08c72dc7873',
    'pk02/out_kt_cert_v1_8_g.tn4.out': '58383b2280a046702385ff787358216214816cb91fb099e11e89c74be3a5b392',
    'pk02/out_kt_cert_v1_8_g.tn3.out': '4c029fa27519b78e20cecf869506f908055c4896ef7f046f228260e7c3461078',
    'pk02/out_kt_cert_v1_8_g.amn4.out': '66ffa2fa3169b0bce83d2388982c074232da0aa61d94322faab5bac2c87da7fd',
    'pk02/out_kt_cert_v1_8_g.amn3.out': '3aba707a3a4e1e2c99b5776c54e5d3cf114534e6363af5cb5eb4a130d24d61b7',
    'pk02/out_kt_cert_v1_8_g.hn4.out': '576c9977c2fea5541ecd855ef4779a64048f2516fb2798ac3fbc25a8985dac16',
    'pk02/out_kt_cert_v1_8_g.hn3.out': '8d16ee81133574a3f315d116df015ae64b2cd4a03d07666d45c847294afe8fdc',
    'pk02/out_kt_cert_v1_8_g.an4.out': '8cb0256d336567c81652c0f5369d1bc013ad482a9605bc1ab86629d6e19acd1c',
    'pk02/out_kt_cert_v1_8_g.an3.out': 'beb3edf4381d926cdd55b4437085713e4da426f0c7d2720b73645064ca1cfcc3',
    'pk02/out_kt_cert_v1_6_x.e1n4.out': '1e0aa13ee35d748c75c67e3af4f786f4df858d93f01e709933203a916e4b70aa',
    'pk02/out_kt_cert_v1_6_x.e1n3.out': 'dc9111f62519c3cce00eaa51c81845b5535b8aab8f9e6a69158ea8003e748b81',
    'pk02/out_kt_cert_v1_6_x.e3n4.out': '4bb4ba5694aad31c4596af291f1089d4b5074f00afec72da9d4089fbc83a708d',
    'pk02/out_kt_cert_v1_6_x.e3n3.out': '28cfd89dbba2b7d2be5cdcaa6c5010873b677ed3f97f9f4eb15475691a580817',
    'pk02/out_kt_cert_v1_7_x.tn4.out': '357ca5b1c5cfa7bb8863f761e5d7a9b312f84dbf3b5572b40bda299c6b2acfb5',
    'pk02/out_kt_cert_v1_7_x.tn3.out': '931ee6b39d7b86280fa7d3e0b768cf2b0f6adde456193f34f3c88864ec517ed4',
    'pk02/out_kt_cert_v1_7_x.amn4.out': '9eb9ea6bd0b42c6a12935a615c92a6e9cab6432eecd9e02c0177e215d298b874',
    'pk02/out_kt_cert_v1_7_x.amn3.out': 'a7d563884b9da3b895bd7aca6863a0002532f9cae4a209bfdf04e6ba34e9d319',
    'pk02/out_kt_cert_v1_6_x.hn4.out': 'c438010d52db212b1df748b546bd989ceb9ee950778b6ed668d4f9ad3015b3ec',
    'pk02/out_kt_cert_v1_6_x.hn3.out': '5e031536823aecaa7a2e308192f7f231768cb79801ede09c886b4618dba0258a',
    'pk02/out_kt_cert_v1_6_x.an4.out': '8e665614dfb534d255a8849a94300eeacf83ee8469c5afee9d50a1775f9e244b',
    'pk02/out_kt_cert_v1_6_x.an3.out': 'a11dddceb52dd289f91cffa096a89505ef9f183d40ed64764837350e445675f3',
}
FARF = {4: ('pk02/FAR_CRUDE_v1_N4.json', 'pk02/out/far_crude_v1.N4.out'), 3: ('pk02/FAR_CRUDE_v1_N3.json', 'pk02/out/far_crude_v1.N3.out')}   # kt_cert_v1_9: FAR_CRUDE_v1 record and its run output (under CODEDIR)
VACF = {n: ('pk03/out/m3_vac_N%d_J150_v2_1.json' % n, 'pk03/out/m3_vac_v2_1_asm.%d.out' % n,
            'pk03/MANIFEST_m3_vac_v2_1_asm.%d.sha256' % n) for n in (3, 4)}               # kt_cert_v1_9: gBb's G4R_r
S9F = {n: ('pk03/out/m3_s9_N%d_J300_v1_8_3.json' % n, 'pk03/out/m3_run_v1_8_3_asm9.%d.out' % n,
           'pk03/MANIFEST_m3_run_v1_8_3_asm9.%d.sha256' % n) for n in (3, 4)}            # kt_cert_v1_9: Z's G,b,b
M2BF = ('pk02/M2B_KV_v1.txt', 'pk02/out/out_m2b_asm_v1.out')                          # kt_cert_v1_9: eps_r
READERS = {'far': 'pk02/far_crude_reader_v1.py', 'vac': 'pk03/m3_reader_v5.py', 'm2b': 'pk02/m2b_reader_v1.py',
           's9': 'pk03/m3_reader_v4_4.py'}
V18PIECES = ('c', 'tX0', 'tX1', 'tX2', 'tB', 'tA')                                             # kt_cert_v1_9: read from kt_cert_v1_8
OWNFILES = {
    'arbeng_c2b_v2.py': '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0',
    'majfix_v1_1.py': 'e57ca554dff8604985bbe2222bd5b60d5d8ea83e9743cc3d07e1828bd63322b4',          # kt_cert_v1_8: the shared F-2 fix
}
SRCFILES = {
    'out_kt_c_v2_3_e1n4.out': 'f38d2d62c50bdb136aeb7399a6c04dc9112137cba199e17a622adcd6f4e2e3c9',
    'out_kt_c_v2_3_e3n4.out': '8d1053659fff5e4a7ae1841c0e6f48aea65245f447fab5e438a854382aa7ee2a',
    'out_kt_c_v2_3_hn4.out': '75795b6b1c5fea53d3341e346c1d8aa2d13a1fc5ac16ef79b33e03201bc9f688',
    'out_kt_c_v2_3_an4.out': '324fab52a7c469bf696e08c22a5134d99ff531516573150586562fa2cc516cc5',
    'out_kt_c_v2_3_e1n3.out': 'cee0e054ab2b800d8a6bcd6cbb7e88bbb0c3b34d81c0e5748c8e2dc0494fc1e5',
    'out_kt_c_v2_3_e3n3.out': '8433814c3f7bdf25f78c19e583d2edaa3af13b0010c5990adbc60ae7e7f63825',
    'out_kt_c_v2_3_hn3.out': '6ec2a250c79ded297b6d6122f902060792dc096b62f253a17a12ee951a425486',
    'out_kt_c_v2_3_an3.out': 'ebaad15a140d05cf42fb8cb318a9db97de1748e93f4fa5b632ac6a53f805f5ff',
    'out_kt_c0_v1_1.out': '995fa111f5ba203feb3b2328120c56a7e6caf657561fc37c9c3fe28f98d5329c',     # kt_cert_v1_7: C-KTC0's C_t (READ lines)
}
INPUTS = {
    'ts_N3_S.json': '26e20e76fbce80c205703f5ba27395ebddaeaa2713bb129b0b4e5902a2061955',
    'ts_N4_J170_D_S.json': 'd6d104ea1f2f64a82f051ce2872f1fbbd0628c9875b0743e4815bf74643fea8c',
    'vacres_K3_N3.json': 'ebcbd08ca532642188071c964039808a318038020bb1a788a7fa3a49cb357426',
    'vacres_K3_N4.json': '516b2501c37a65b21b617fba3cb1d7b02adf9966f409bc5105418822dfa0e765',
}
TRIAL = {                                         # kt_cert_v1_6: the trial set z9sym of the production items (pk11 zero_states_v2_1, 168106e0)
    'ts_N3_S_z9sym_v1.json': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    'ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    'vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    'vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
}
REFS = {                                          # kt_cert_v1_6: kt_c_v2_3z's prints on z9sym, in REFDIR (C-REP of the production items)
    'out_kt_c_v2_3z_e1n4.out': '5d09f736c263be8063b27e0a71b739bc6eb1ef097bac1426135f68dce25ce766',
    'out_kt_c_v2_3z_e3n4.out': '61bbfc000d2bcc58f2dfc9cfc4f5c6b682ebfac820c7e881f2dd73cb5e999b3e',
    'out_kt_c_v2_3z_hn4.out': '06793b56f80b7d2c7f7dd38fed2220ec8c3414243dc69137e68ddbdcdc143d17',
    'out_kt_c_v2_3z_an4.out': '3f21a85cf5d60f8e15657c63a0a0fffe687284473e8201d1c8e4a6891759eb0e',
    'out_kt_c_v2_3z_e1n3.out': '074ed824fc97f7b2a70303c280e386323766236971d819dfc0e8b8d603eb38c0',
    'out_kt_c_v2_3z_e3n3.out': '6738069336f99f510fdb5582d1342837d86bacaf439ea11ba6ab863404676d45',
    'out_kt_c_v2_3z_hn3.out': '9bcc1039626455b8b432be60b26ee3c61708e574c3898e82597988c26cca1a5d',
    'out_kt_c_v2_3z_an3.out': 'bd3637f6a6e37313cd69a223a9a594699aaa2cc926b1e9c1dbab5a1c43c6aa3b',
}
TREFDIR = '/mnt/g2/release/root/code/pk15/out'   # kt_cert_v1_7: kt_c_t_v1_1's prints (C-REP of kinds t and am)
TREFS = {                                         # full sha256 as in pk15's MANIFEST_STB_P2_PREP_v1_2.sha256
    'out_kt_c_t_v1_1_tn3.out': '9aa65751e3b8b5deb6634077aa5b8bbc6e4500f1627dc677b0065138e7240f8f',
    'out_kt_c_t_v1_1_tn4.out': '20799d7b93a45fedbb4db06994f45e765452849ffd0e03c1b8a9a0c9cd0f241c',
    'out_kt_c_t_v1_1_amn3.out': 'e64520920ef87d249e33f26835c92d9bd4013b7b3fbcacef6117f6e9af02ef1f',
    'out_kt_c_t_v1_1_amn4.out': '8d1dd472ddc735ebe60587f8016b4f6fad176d761f24469d798fbda88fb7d214',
}
VT_SHA = 'ba197fed6234b2723c907551d00a1c09e44940c23d8c07e16f4bec71bc2e744d'     # kt_c_t_v1_1.py (pk15): t's and am's float reference
PREV = {                                          # kt_cert_v1_6: kt_cert_v1_5's VALID g.e1n4 record, in OWN (C-REPLAY of the smoke)
    'out_kt_cert_v1_5_g.e1n4.out': '08d26e2080812b089787bdd723179ad0d6bd809447af377a492c939da17e8c73',
}
V23_SHA = '71a224a24d07b0ba77cb57c1e02cc82fcffbdf0d52cff5872c0993249f4ce946'    # kt_c_v2_3.py (pk01): the smoke's float reference
V23Z_SHA = 'f2497cf7d67403f78b010976d4e622231acd9e5c18ac880e7dfa743fc25464a7'   # kt_c_v2_3z.py: the production items' float reference
V15_SHA = '33423b592a1770ef9b7737c682187503a85840d193207771dda0a0c1f35c0495'    # kt_cert_v1_5.py: the replayed engine
FIXREF_SHA = 'b9efad1a700fa28bdb7a13c413c62408a3082008c6801e5f358504ea2d04a59e'   # kt_cert_v1_8: the C-REP-FIX twin (majfix_v1, binary64; its J = 300 rows)
FIXREFS = {                                       # kt_cert_v1_8: its records in REFDIR (j: the M4 scan; r: the J = 300 references)
    'out_kt_c_t_trade_v1_3_jtn4.out': '9ee9e865421e984c1fefca9deb972d66bc03400fef370f0d2741b4adea86ab1b',
    'out_kt_c_t_trade_v1_3_jtn3.out': '3a37de73933ad01f74a8a7f17ad73530317f1ee2871e43432cd55a6e035a840f',
    'out_kt_c_t_trade_v1_3_jamn4.out': 'e495bf279f25b92f78a02a28e79bacfa5ad454b41af552860a2361b342d156c1',
    'out_kt_c_t_trade_v1_3_jamn3.out': 'ef8eed45202f9ef85850f6ab35f4b354634b081d333c0e06b7b92f98911aa333',
    'out_kt_c_t_trade_v1_3_je1n4.out': '5f6d9b9b22621d66e999742c1de43ab77edc52d9fe9cbb24e155b96ea711f259',
    'out_kt_c_t_trade_v1_3_je1n3.out': '69e42a83cc46140b8688f0d538ec1d1812ea32c72a8c23e7f9f9d993cefd6e3f',
    'out_kt_c_t_trade_v1_3_je3n4.out': '864aa3929517e3bc7e822404685bfe8e70435af84c843685659a73175d2a1084',
    'out_kt_c_t_trade_v1_3_je3n3.out': '8e15beeae457c8fe8e835adf62ee996907b09c77b95c104fa8d214edca335611',
    'out_kt_c_t_trade_v1_3_rhn4.out': '7183da09969d8f9fc975419a438e68f7f9a85ebee0d3c6e3e437666cc99456a5',
    'out_kt_c_t_trade_v1_3_rhn3.out': 'f031a08fa658eff5c24710a88cf8faaec6fb7354bc3a3fc0da8322f407cdabbe',
    'out_kt_c_t_trade_v1_3_ran4.out': 'f349735faab1fe348d62f81f5408ed03dfab4ac87ad1ef4291ff542e500f889d',
    'out_kt_c_t_trade_v1_3_ran3.out': 'b3b49ea1b7a1f112deb35c3de27420124f70d7ad533d4da95d890b5c55a46dd5',
}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


SELF_SHA = sha_file(os.path.abspath(__file__))
out('kt_cert_v1_9 sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (SELF_SHA, MODE, LIM, LIM, LIM + 5))
_bad = []
for _d, _tab in ((OWN, OWNFILES), (SRC, SRCFILES), (INP, INPUTS), (WOUT, TRIAL), (REFDIR, REFS), (OWN, PREV),
                  (TREFDIR, TREFS), (REFDIR, FIXREFS), (W18, CERTIN)):    # kt_cert_v1_9: CERTIN (the certified inputs, v1_8's records)
    for _n in sorted(_tab):
        _got = sha_file(os.path.join(_d, _n))
        if _got != _tab[_n]:
            _bad.append('%s %s' % (_n, _got))
_need = ({'pk02/kt_cert_v1_8.py'} | set(READERS.values()) | set(M2BF) | {p for n in (3, 4) for p in VACF[n] + S9F[n] + FARF[n]} |
         {'pk02/out_kt_cert_v1_8_%s.%sn%d.out' % (p, k, n) for p in V18PIECES for k in CN2KINDS for n in (3, 4)} |
         {'pk02/out_kt_cert_v1_8_g.%s.out' % s for s in SUFFIXES})
_miss = sorted(_need - set(CERTIN))
if CERTIN.get('pk02/kt_cert_v1_8.py') != V18_SHA:
    _miss.append('kt_cert_v1_8.py pin differs from V18_SHA')
out('C-HASH %s (%d own files, %d predecessor outputs, %d inputs, %d trial-set files, %d float references, %d replay record, %d certified '
    'inputs and kt_cert_v1_8 records; every path v1_9 reads is pinned: %s)%s' % (
        'PASS' if not (_bad or _miss) else 'FAIL', len(OWNFILES), len(SRCFILES), len(INPUTS), len(TRIAL), len(REFS) + len(TREFS), len(PREV),
        len(CERTIN), 'yes' if not _miss else 'NO', (': ' + '; '.join(_bad + _miss)) if (_bad or _miss) else ''))
if _bad or _miss:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, OWN)

import importlib.util
import numpy as np
import flint
from flint import arb, arb_mat, ctx


def load_reader(key):
    """kt_cert_v1_9: a certified input's reader from its pinned file (CERTIN), executed in its own module."""
    sp = importlib.util.spec_from_file_location('rdr_' + key, os.path.join(W18, READERS[key]))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


RD_FAR, RD_VAC, RD_M2B, RD_S9 = (load_reader(k) for k in ('far', 'vac', 'm2b', 's9'))   # m2b_reader_v1 sets ctx.prec 256 at import
ctx.prec = 512                   # kt_cert_v1_4 (ADD2 v1_3): kt_cert_v1_2's ghsmoke failed C-RAD at 256 bits through the tail tables
import arbeng_c2b_v2 as ae
import majfix_v1_1 as mf
out('ENV: python-flint %s, numpy %s, python %s, ctx.prec %d' % (flint.__version__, np.__version__, sys.version.split()[0], ctx.prec))
out('FORMAT KT_CERT_RECORD_v1_9')                 # kt_cert_v1_9: CERTIFIED only on the STATUS line at the end (the review a50a005a Q3 (2))
out('KERNEL arbeng_c2b_v2.py %s ctx.prec %d' % (OWNFILES['arbeng_c2b_v2.py'], ctx.prec))

PIECE, SUFFIX = MODE.split('.', 1)               # the pieces of an item and their hand-offs: part 6
SMOKE = SUFFIX if SUFFIX == 'smoke' else None    # kt_cert_v1_6: the e1n4 replay on kt_cert_v1_5's inputs (hsmoke dropped)
KIND = 'e1' if SMOKE else SUFFIX[:-2]
NN = 4 if SMOKE else int(SUFFIX[-1])
nn = NN - 1
SQ5, SQ21 = arb(5).sqrt(), arb(21).sqrt()
A_ = (3 + SQ21) / 6
B_ = (3 * SQ5 - SQ21) / 12
TRI = [A_, A_, B_]
PAIRS = [(0, 1), (1, 2), (0, 2)]
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]
X0 = (7 - 3 * SQ5) / 2
Y0 = (23 - 5 * SQ21) / 2
SFILE = ({4: 'ts_N4_J170_D_S.json', 3: 'ts_N3_S.json'} if SMOKE else {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'})[NN]
VFILE = ({4: 'vacres_K3_N4.json', 3: 'vacres_K3_N3.json'} if SMOKE else {4: 'vacres_K3_N4_sym_v1.json', 3: 'vacres_K3_N3_sym_v1.json'})[NN]
DDIR = INP if SMOKE else WOUT                # kt_cert_v1_6: the smoke replays kt_cert_v1_5's inputs; the production items read z9sym
RHO_M, RHO_E = 0.55, 0.6                    # free radii (exact binary64)
DELTA = arb.pi() * 40 / 180                 # 40 degrees, in arb
J_MAIN = 300
EVEN = (0, 1, 3)
KX, NVX = 3, 14
XS, QS, XD, QD = [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]
QH, QT = 12, 13
ROWX = 0 if KIND == 't' else 1              # kt_cert_v1_7: the row of the horizontal insertion (T for kind t, M as before otherwise)
QGROUPS, QCAPS = [0, 0, 0, 1, 1, 1, 2, 3], {1: 2, 2: 1, 3: 1}
NV12, BB = 12, 26




# ====================================================================================== part 2a: the conditioning (kt_c_v2_3 l.300-332)
def tri_laplacian():
    """the triangle Laplacian (A, A, B) as an arb_mat (couplings in arb)."""
    L = arb_mat(3, 3)
    for p, (r, s) in enumerate(PAIRS):
        c = TRI[p]
        L[r, r] += c
        L[s, s] += c
        L[r, s] -= c
        L[s, r] -= c
    return L


def build_conditioning():
    """kt_c_v2_3.build_conditioning in balls: phi'' = A^-1 phi + zeta, zeta ~ N(0, A^-1), A = I + L_tri; forms X'' (0-2), Q'' (3-5), QH (6),
    QT (7); the W matrix is exact (entries 0, +-1)."""
    Ainv = (arb_mat(3, 3, [1 if i == j else 0 for i in range(3) for j in range(3)]) + tri_laplacian()).inv()
    Mm = arb_mat(6, 3)
    Cm = arb_mat(6, 6)
    for i in range(3):
        for j in range(3):
            Mm[i, j] = Ainv[i, j]
            Cm[i, j] = Ainv[i, j]
        Mm[3 + i, i] = 1
    Wc = arb_mat(6, 8)
    for r in range(3):
        Wc[r, r] = 1
    for p, (r, s) in enumerate(PAIRS):
        Wc[r, 3 + p] = 1
        Wc[s, 3 + p] = -1
    Wc[1, 6] = 1
    Wc[3 + 1, 6] = -1
    Wc[0, 7] = 1
    Wc[3 + 0, 7] = -1
    return ae.CondMomA(Mm, Cm, Wc, nn, 2 * KX + 2, groups=QGROUPS, caps=QCAPS)


def lin_g(cm, gi):
    """g_rr = X_r, g_rs = (X_r + X_s - Q_rs)/2 (exact halves)."""
    r, s = cm.gvars[gi]
    if r == s:
        return {tuple(1 if q == XS[r] else 0 for q in range(6)): arb(1)}
    qi = QS[PAIRS.index((r, s))]
    half = arb(1) / 2
    return {tuple(1 if q == XS[r] else 0 for q in range(6)): half, tuple(1 if q == XS[s] else 0 for q in range(6)): half,
            tuple(1 if q == qi else 0 for q in range(6)): -half}


def qcap_ok(e2):
    """the conditioned monomial e2 (forms X'' 0-2, Q'' 3-5, QH 6, QT 7) is inside the caps of build_conditioning."""
    return all(sum(x for x, g in zip(e2, QGROUPS) if g == k) <= cap for k, cap in QCAPS.items())




# ====================================================================================== part 2b1: series helpers (kt_c_v2_3 l.234-299)
Series, padd, pscale, pmul, pconst, pvar = ae.Series, ae.padd, ae.pscale, ae.pmul, ae.pconst, ae.pvar
WX = ae.w_coeffs(KX)                         # exact rationals as balls


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


Smat = np.array(load_json(os.path.join(DDIR, SFILE))['S'])     # exact binary64 data
lam0 = load_json(os.path.join(DDIR, SFILE))['lam0']
R3 = load_json(os.path.join(DDIR, VFILE))
QV = [None, R3['q1'], R3['q2'], R3['q3']]


def ser(coeffs):
    return Series(KX, NVX, coeffs)


def zero():
    return ser([{} for _ in range(KX + 1)])


def one():
    return ser([pconst(1, NVX)] + [{} for _ in range(KX)])


def meas(i):
    return ser([{}] + [{tuple(k if j == i else 0 for j in range(NVX)): arb(1) / (2 * k)} for k in range(1, KX + 1)])


def anh(iu, iv, c):
    res = [{} for _ in range(KX + 1)]
    d2 = padd(pmul(pvar(iu, NVX), pvar(iu, NVX)), pscale(pmul(pvar(iu, NVX), pvar(iv, NVX)), -2), pmul(pvar(iv, NVX), pvar(iv, NVX)))
    for (i, j), cw in WX.items():
        k = 1 + i + j
        if k > KX:
            continue
        mono_ = {tuple((i if q == iu else 0) + (j if q == iv else 0) for q in range(NVX)): arb(1)}
        res[k] = padd(res[k], pscale(pmul(d2, mono_), -ae.A(c) * cw / 2))
    return ser(res)


def xi_pair(iu, iv, iq):
    return ser([pvar(iq, NVX, arb(1) / 2)] + [{} for _ in range(KX)]) - anh(iu, iv, 1)


def xis(Xi, Qi):
    return [xi_pair(Xi[r], Xi[s], Qi[p]) for p, (r, s) in enumerate(PAIRS)]


def mono_series(xs, mono_):
    res = one()
    for p in mono_:
        res = res * xs[p]
    return res


def shift(sr, sh):
    return ser([{} for _ in range(sh)] + [dict(P) for P in sr.c[:KX + 1 - sh]])


def vac_poly(xs):
    res = one()
    for coef, sh in ((QV[1], 1), (QV[2], 2), (QV[3], 3)):
        if sh > KX:
            continue
        for cb, mono_ in zip(coef, BASIS):
            if cb != 0.0:
                res = res + shift(mono_series(xs, mono_), sh).scale(arb(cb))
    return res


def state_poly(xs, b):
    res = one().scale(arb(float(Smat[0, b])))
    for cb, mono_ in zip(Smat[1:, b], BASIS):
        if cb != 0.0:
            res = res + mono_series(xs, mono_).scale(arb(float(cb)))
    return res




# ====================================================================================== part 2b2a: make_condE (kt_c_v2_3 l.333-396), sparse
def make_condE(cm):
    """kt_c_v2_3.make_condE in balls: E[. | sigma] of series coefficients as sigma polynomials of degree <= cm.Dc, through the g -> sigma map
    (g_rr = X_r, g_rs = (X_r + X_s - Q_rs)/2). Same sums as the float version; the g -> sigma rows are kept sparse (dicts of balls) instead
    of the dense matrix G2F, so no ball is ever formed for a structural zero."""
    D = cm.Dc
    Bs = D + 1
    pw = [Bs ** i for i in range(6)]
    lay = [np.zeros(1, dtype=np.int64)]
    for d in range(1, D + 1):
        lay.append(np.unique((lay[-1][:, None] + np.array(pw, dtype=np.int64)[None, :]).ravel()))
    scodes = np.unique(np.concatenate(lay))
    sexp = np.stack([(scodes // pw[i]) % Bs for i in range(6)], axis=1)
    sdeg = sexp.sum(axis=1).tolist()
    sidx = {int(c): k for k, c in enumerate(scodes.tolist())}
    scl = scodes.tolist()

    def mult(vec, e6, c, acc):
        """acc += c * (vec shifted by the sigma monomial e6), keeping total degree <= D."""
        de, ce = sum(e6), sum(int(x) * p for x, p in zip(e6, pw))
        for k, x in vec.items():
            if sdeg[k] + de <= D:
                d = sidx[scl[k] + ce]
                v = c * x
                acc[d] = acc[d] + v if d in acc else v

    lin = [lin_g(cm, gi) for gi in range(len(cm.gvars))]
    assert len(cm.gvars) == 6
    rows = {tuple([0] * 6): {0: arb(1)}}

    def grow(gexp):
        if gexp not in rows:
            i = next(j for j, m in enumerate(gexp) if m > 0)
            prev = list(gexp)
            prev[i] -= 1
            base = grow(tuple(prev))
            v = {}
            for e6, c in lin[i].items():
                mult(base, e6, c, v)
            rows[gexp] = v
        return rows[gexp]
    cache = {}

    def condvec(e2):
        assert sum(e2) <= D and qcap_ok(e2), e2
        if e2 not in cache:
            acc = {}
            for g, val in cm.cond(e2).items():
                for k, x in grow(tuple(g)).items():
                    v = val * x
                    acc[k] = acc[k] + v if k in acc else v
            cache[e2] = acc
        return cache[e2]

    def condE(sr):
        res = []
        for P in sr.c:
            acc = {}
            for e, c in P.items():
                assert sum(e) <= D, e
                mult(condvec(tuple(e[6:])), tuple(e[:6]), ae.A(c), acc)
            res.append({tuple(int(x) for x in sexp[k]): v for k, v in acc.items() if not v.is_zero()})
        return res
    return condE


# ====================================================================================== part 2b2b: B0 engines, projections, explicit part
# (kt_c_v2_3 l.436-637, per item kind; the m_g are the midpoints of ball solutions, then exact binary64: any real m_g is allowed, (C1))
deg = ae.deg


def nsqrt(x):
    """an enclosure of sqrt(max(x, 0)) for a ball x. F6: every argument is a second moment or a squared norm, never negative, so a
    certainly negative ball is a defect and stops the item (nonnegative_part would map it to 0 silently)."""
    if x < 0:
        raise ValueError('nsqrt of a certainly negative ball %s (F6)' % x.str(10, radius=True))
    return x.nonnegative_part().sqrt()


def fup(x):
    """an upper bound of |x| as a binary64 number (for printing and for the K-checks' tolerances)."""
    return float(x.abs_upper())


def restrict6(sr):
    res = []
    for P in sr.c:
        acc = {}
        for e, c in P.items():
            assert sum(e[6:]) == 0, e
            k = tuple(e[:6])
            acc[k] = acc[k] + c if k in acc else ae.A(c)
        res.append({e: c for e, c in acc.items() if not c.is_zero()})
    return res


def strip2_laplacian():
    """the Laplacian of lapl2.strip_graph(2, (A, B)) in arb: vertex 3 col + row; triangles (A, A, B); horizontals 1."""
    L = arb_mat(6, 6)
    edges = []
    for j in range(2):
        T, Mv, Bv = 3 * j, 3 * j + 1, 3 * j + 2
        edges += [((T, Mv), A_), ((Mv, Bv), A_), ((T, Bv), B_)]
    edges += [((r, 3 + r), arb(1)) for r in range(3)]
    for (u, v), c in edges:
        L[u, u] += c
        L[v, v] += c
        L[u, v] -= c
        L[v, u] -= c
    return L


def gauge_pinv(L):
    """B (B^T L B)^-1 B^T with the exact basis B = [e_s - e_0] of the complement of the constant vector; equal to the float code's
    Qb (Qb^T L Qb)^-1 Qb^T for any basis Qb of that complement (ADD2 sect. 1)."""
    V = L.nrows()
    Bm = arb_mat(V, V - 1)
    for s in range(1, V):
        Bm[s, s - 1] = 1
        Bm[0, s - 1] = -1
    return Bm * (Bm.transpose() * L * Bm).inv() * Bm.transpose()


def make_B0c(c0, c1):
    """B0(f, h) = E_D[f(sigma) h(sigma')] for deg f <= c0 (first column) and deg h <= c1 (second column), in balls."""
    Gp = gauge_pinv(strip2_laplacian())
    WD = arb_mat(6, 12)
    for col in range(2):
        for r in range(3):
            WD[3 * col + r, 6 * col + r] = 1
        for p, (r, s) in enumerate(PAIRS):
            WD[3 * col + r, 6 * col + 3 + p] = 1
            WD[3 * col + s, 6 * col + 3 + p] = -1
    am = ae.AllMom2A(WD.transpose() * Gp * WD, nn, c0 + c1, groups=[0] * 6 + [1] * 6, caps={0: c0, 1: c1})
    z6 = (0,) * 6

    def B0(f, h):
        assert deg(f) <= c0 and deg(h) <= c1, (deg(f), deg(h), c0, c1)
        return am.E2({tuple(e) + z6: c for e, c in f.items()}, {z6 + tuple(e): c for e, c in h.items()})
    return B0


def solve_mid(Gb, vb):
    """the float choice m: the midpoints of the ball solution of Gb m = vb, as binary64 numbers (exact from here on)."""
    nb = len(vb)
    Gm, vm = arb_mat(nb, nb), arb_mat(nb, 1)
    for i in range(nb):
        vm[i, 0] = vb[i]
        for j in range(nb):
            Gm[i, j] = Gb[i][j]
    sol = Gm.solve(vm)
    return [float(sol[i, 0].mid()) for i in range(nb)]


def project(B0, f, basis):
    """kt_c_v2_3.project with m = solve_mid (free choice, (C1)); r = f - sum m_i b_i in balls; returns m, r and the ball B0(r, r)."""
    nb = len(basis)
    m = solve_mid([[B0(basis[i], basis[j]) for j in range(nb)] for i in range(nb)], [B0(basis[i], f) for i in range(nb)])
    r = padd(f, *[pscale(basis[i], -m[i]) for i in range(nb)])
    return m, r, B0(r, r)


def project_nonorm(B0low, B0mix, f, basis):
    nb = len(basis)
    m = solve_mid([[B0low(basis[i], basis[j]) for j in range(nb)] for i in range(nb)], [B0mix(basis[i], f) for i in range(nb)])
    r = padd(f, *[pscale(basis[i], -m[i]) for i in range(nb)])
    return m, r


def xfrac(P):
    big = max([fup(c) for c in P.values()] + [0.0])
    xs = max([fup(c) for e, c in P.items() if sum(e[:3]) > 0] + [0.0])
    return xs / big if big > 0 else 0.0


def c_ktc0_ref():
    """kt_cert_v1_7, C-KTC0: C_t from out_kt_c0_v1_1's READ line at this N (pk01, pinned in SRCFILES; old trial set, K-C0's 5e-7 covers
    z9sym's change of S, kt_c_v2_3z's note)."""
    with open(os.path.join(SRC, 'out_kt_c0_v1_1.out')) as fh:
        lines = fh.read().splitlines()
    hit = [mt for mt in (re.match(r'READ N=%d: .*\bC_t ([0-9.]+e[+-][0-9]+)' % NN, ln) for ln in lines) if mt]
    if len(hit) != 1:
        raise ValueError('out_kt_c0_v1_1.out: %d READ lines with C_t at N = %d' % (len(hit), NN))
    return float(hit[0].group(1))


def ktc0_gate(c, cref):
    """kt_cert_v1_7, C-KTC0's comparison (two-sided, 5e-7 relative, as kt_c's K-C0); returns (ok, relative difference)."""
    rel = abs(c / cref - 1)
    return rel <= 5e-7, rel


STATE_OF = {'e1': 'e1', 'e3': 'e3', 'h': 'psi', 'h1': 'e1', 'h3': 'e3', 'a': 'psi', 't': 'psi', 'am': 'psi'}
HOOK = ('h', 'h1', 'h3', 't')                                           # kt_cert_v1_7: t is a hook kind (|xi_t| <= 2J)
GK = {'t': ('psi', 'e1', 'e3', 'e2'), 'am': ('e2',)}                    # kt_cert_v1_7: P_4 for t, {e2} for am; (psi, e1, e3) otherwise


def explicit_part(kind, fails, fires):
    """orders 0-3 of the item's source in balls: m (4 orders x basis psi, e1, e3), r0..r3 (sigma polynomials), T3 (the series before the
    conditional expectation, for the inner tails), bas (the basis series). Checks as kt_c_v2_3 for the item's kind."""
    t0 = cpu()
    HL = zero()
    for r in range(3):
        HL = HL + meas(XD[r])
    for p, (r, s) in enumerate(PAIRS):
        HL = HL + anh(XD[r], XD[s], TRI[p])
    for r in range(3):
        HL = HL + anh(XS[r], XD[r], 1)
    HL = HL + anh(XS[0], XS[1], 1) + anh(XS[1], XS[2], 1)
    H0 = zero()
    for p, (r, s) in enumerate(PAIRS):
        H0 = H0 + anh(XS[r], XS[s], TRI[p])
    EL, E0 = HL.exp(), H0.exp()
    xiD, xiS = xis(XD, QD), xis(XS, QS)
    xih = xi_pair(XS[ROWX], XD[ROWX], QT if kind == 't' else QH)       # kt_cert_v1_7: xi_t on row T for kind t (xi_h on row M otherwise)
    G = GK.get(kind, ('psi', 'e1', 'e3'))                               # kt_cert_v1_7: the kind's basis
    pS = {'psi': vac_poly(xiS), 'e1': state_poly(xiS, 1), 'e3': state_poly(xiS, 3)}
    if 'e2' in G:
        pS['e2'] = state_poly(xiS, 2)
    bas = {g: restrict6(E0 * pS[g]) for g in pS}
    if kind == 'a':
        T3 = None
        src = restrict6(E0 * ((xiS[0] + xiS[1]).scale(arb(1) / 2)) * pS['psi'])
    elif kind == 'am':                                                  # kt_cert_v1_7: the odd vertical source (xi_TM - xi_MB)/2
        T3 = None
        src = restrict6(E0 * ((xiS[0] - xiS[1]).scale(arb(1) / 2)) * pS['psi'])
    else:
        b = STATE_OF[kind]
        pD = vac_poly(xiD) if b == 'psi' else state_poly(xiD, {'e1': 1, 'e3': 3}[b])
        T3 = EL * xih * pD if kind in HOOK else EL * pD
        src = make_condE(build_conditioning())(T3)
    out('EXPLICIT N=%d %s: series and conditional expectations to order %d, %.1f s' % (NN, kind, KX, cpu() - t0))
    degs2 = max([deg(src[o]) for o in range(3)] + [deg(bas[g][o]) for g in G for o in range(3)] + [deg(bas[g][0]) for g in ('e1', 'e3')])
    degs3 = max([deg(src[3])] + [deg(bas[g][3]) for g in G])
    B0a = make_B0c(degs2, degs2)
    B0b = make_B0c(2, max(degs3, degs2))
    n11, n33, o13 = B0a(bas['e1'][0], bas['e1'][0]), B0a(bas['e3'][0], bas['e3'][0]), B0a(bas['e1'][0], bas['e3'][0])
    ok = fup(n11 - 1) <= 1e-9 and fup(n33 - 1) <= 1e-9 and fup(o13) <= 1e-9
    out('K-ORTH N=%d: |B0(e1,e1) - 1| <= %.2e, |B0(e3,e3) - 1| <= %.2e, |B0(e1,e3)| <= %.2e -> %s (%.1f s)' % (
        NN, fup(n11 - 1), fup(n33 - 1), fup(o13), 'PASS' if ok else 'FAIL', cpu() - t0))
    if not ok:
        fails.append('K-ORTH')
    nb = len(G)
    bk = [[bas[g][o] for g in G] for o in range(4)]
    s = src
    m0, r0, n0 = project(B0a, s[0], bk[0])
    f1 = padd(s[1], *[pscale(bk[1][i], -m0[i]) for i in range(nb)])
    m1, r1, n1 = project(B0a, f1, bk[0])
    f2 = padd(s[2], *[pscale(bk[2][i], -m0[i]) for i in range(nb)], *[pscale(bk[1][i], -m1[i]) for i in range(nb)])
    m2, r2, n2 = project(B0a, f2, bk[0])
    f3 = padd(s[3], *[pscale(bk[3][i], -m0[i]) for i in range(nb)], *[pscale(bk[2][i], -m1[i]) for i in range(nb)],
              *[pscale(bk[1][i], -m2[i]) for i in range(nb)])
    m3, r3 = project_nonorm(B0a, B0b, f3, bk[0])
    rn = [fup(nsqrt(x)) for x in (n0, n1, n2)]
    ex = dict(G=G, m=[m0, m1, m2, m3], r0=r0, r1=r1, r2=r2, r3=r3, n=rn, T3=T3, bas=bas)
    out('EXPLICIT N=%d %-3s: m0 %s | m1 %s | m2 %s | m3 %s; |r0| <= %.2e |r1| <= %.6e |r2| <= %.6e; deg r3 %d (%.1f s)' % (
        NN, kind, ' '.join(repr(x) for x in m0), ' '.join(repr(x) for x in m1), ' '.join(repr(x) for x in m2), ' '.join(repr(x) for x in m3),
        rn[0], rn[1], rn[2], deg(r3), cpu() - t0))
    if kind in ('e1', 'e3'):
        idx, lm = {'e1': (1, lam0[1]), 'e3': (2, lam0[3])}[kind]
        others = max(abs(m0[i]) for i in range(3) if i != idx)
        ok = rn[0] <= 1e-8 and abs(m0[idx] - lm) <= 1e-9 and others <= 1e-8
        out('K-EIG N=%d %s: |r0| <= %.2e, m_diag %.12f vs lam0 %.12f, others %.2e -> %s' % (NN, kind, rn[0], m0[idx], lm, others,
                                                                                          'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('K-EIG %s' % kind)
    if kind in ('h', 'a'):
        s21, s5 = SQ21, SQ5
        ref = float((nn * (1 - 2 / s21) / 2).mid()) if kind == 'h' else float((nn * (3 / (2 * s21) + 1 / (2 * s5)) / 2).mid())
        ok = rn[0] <= 1e-8 and abs(m0[0] / ref - 1) <= 1e-9 and ((abs(m0[1]) <= 1e-8) if kind == 'h' else True)
        out('K-%s0 N=%d: |r0| <= %.2e, psi coefficient %.12f vs exact %.12f, e1 coefficient %.2e -> %s' % (
            kind.upper(), NN, rn[0], m0[0], ref, m0[1], 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('K-%s0' % kind.upper())
    if kind == 't':                                                     # kt_cert_v1_7: K-T0 (kt_c_v2_3's) and C-KTC0
        ref = float((nn * (1 - 1 / (2 * SQ21) - 1 / (2 * SQ5)) / 2).mid())
        ok = rn[0] <= 1e-8 and abs(m0[0] / ref - 1) <= 1e-9
        out('K-T0 N=%d: |r0| <= %.2e, psi coefficient %.12f vs exact %.12f, e1 coefficient %.2e -> %s' % (
            NN, rn[0], m0[0], ref, m0[1], 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('K-T0')
        ctm = c_ktc0_ref()
        cmid = math.sqrt(max(float(n1.mid()), 0.0))
        okc, rel_c = ktc0_gate(cmid, ctm)
        out('C-KTC0 N=%d: t\'s C = |r1|_B0 %.6e (from the midpoint of the B0 ball; the printed upper value is %.6e) vs out_kt_c0_v1_1\'s C_t '
            '%.6e: rel %.1e (tolerance 5e-7) -> %s' % (NN, cmid, rn[1], ctm, rel_c, 'PASS' if okc else 'FAIL'))
        if not okc:
            fails.append('C-KTC0')
    if kind == 'am':                                                    # kt_cert_v1_7: K-AM0
        ok = rn[0] <= 1e-8
        out('K-AM0 N=%d: |r0(am)|_B0 <= %.2e against {e2}, e2 coefficient %.12f -> %s' % (NN, rn[0], m0[0], 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('K-AM0')
    if kind in ('h1', 'h3'):
        out('INFO N=%d %s: order-0 residual |r0|_B0 <= %.6e (not zero for the hook kinds; enters nP as t^0 r0, ADD2 sect. 3)' % (NN, kind, rn[0]))
    lead = next((o for o in (0, 1, 2) if rn[o] > 1e-8), None)
    if lead is not None:
        xf = xfrac([r0, r1, r2][lead])
        ok = xf <= 1e-9
        if kind in ('h1', 'h3'):
            out('INFO K-INV N=%d %s: leading residual order %d, X share %.1e (not gated for the hook kinds)' % (NN, kind, lead, xf))
        elif kind == 'am':
            out('INFO K-INV N=%d am: leading residual order %d, X share %.1e (not gated: the float fork gates K-INV on psi, e1, e3, h, t and a '
                'only)' % (NN, lead, xf))
        else:
            out('K-INV N=%d %s: leading residual order %d, X share %.1e -> %s' % (NN, kind, lead, xf, 'PASS' if ok else 'FAIL'))
            if not ok:
                fails.append('K-INV')
    return ex


# ====================================================================================== part 3: majorants (kt_c_v2_3 l.629-762), NPolyA in balls
# Derived free parameters (pk01's C-RATE, C-APP): the tilt rates and the annulus radius are binary64 numbers rounded UP from their arb
# values, so every inequality the proof needs (rate >= -log(1 - a)/(2a), a_pp >= sin^2(asin rho_m + delta)) holds by construction.
def up_float(x):
    """a binary64 number >= every point of the ball x."""
    u = x.upper()
    f = float(u)
    if not (arb(f) >= u):
        f = math.nextafter(f, math.inf)
    assert arb(f) >= u
    return f


a_m, a_e = RHO_M ** 2, RHO_E ** 2
c_m, c_e = (up_float(-(1 - arb(x)).log() / (2 * arb(x))) for x in (a_m, a_e))
_rho_pp = (arb(RHO_M).asin() + DELTA).sin()
a_pp = up_float(_rho_pp * _rho_pp)
c_pp = up_float(-(1 - arb(a_pp)).log() / (2 * arb(a_pp)))
AVt = [a_m] * 3 + [None] * 3 + [a_e] * 3 + [None] * 3
ONE_P = ae.NPolyA(NV12, BB, np.zeros(1, dtype=np.int64), [arb(1)])


def mono(e, c=1):
    if len(e) != NV12 or any(not 0 <= int(x) < BB for x in e):          # kt_cert_v1_9: the packing audit 89f7a0d0 item (2)
        raise ValueError('mono: exponents %s are not %d values in [0, %d): the base-%d code would alias' % (list(e), NV12, BB, BB))
    return ae.NPolyA(NV12, BB, np.array([int(sum(int(x) * BB ** i for i, x in enumerate(e)))], dtype=np.int64), [ae.A(c)])


def xv(i, k=1, c=1):
    e = [0] * NV12
    e[i] = k
    return mono(e, c)


def D2(i, j):
    return xv(i, 2).add(xv(i, 1).mul(xv(j, 1)).scale(-2)).add(xv(j, 2))


def Mk(i, j, k):
    return ONE_P if k == 0 else xv(i, k).add(xv(j, k))


def trade(p, t, nt):
    """kt_c_v2_3.trade: lower the largest exponent nt times, each time times its radius factor (a_m, a_e; 4 a_m, 4 a_e for Q); t if none."""
    ex = p.exponents()
    out_e, out_c = [], []
    qa = {3: 4 * a_m, 4: 4 * a_m, 5: 4 * a_m, 9: 4 * a_e, 10: 4 * a_e, 11: 4 * a_e}
    for row, c in zip(ex, p.coeffs):
        row = row.copy()
        fac = c
        for _ in range(nt):
            cand = [(row[i], i) for i in range(NV12) if row[i] > 0]
            if not cand:
                fac = fac * t
                continue
            _, i = max(cand)
            row[i] -= 1
            fac = fac * (AVt[i] if AVt[i] is not None else qa[i])
        out_e.append(row)
        out_c.append(fac)
    res = ae.NPolyA(NV12, BB, np.array(out_e, dtype=np.int64).reshape(-1, NV12) @ p.pw, out_c)
    res._normalize()
    return res


def cf_rad(aa, k):
    return 1 / (1 - arb(aa)) ** k


def hk(k, meas_vertices, bonds, cfac):
    res = ae.NPolyA(NV12, BB)
    for (v, av) in meas_vertices:
        res = res.add(xv(v, k, arb(math.factorial(k - 1)) / 2 * cfac(av, k)))
    for (iu, iv, c, aa) in bonds:
        res = res.add(D2(iu, iv).mul(Mk(iu, iv, k - 1)).scale((ae.A(c) / 2) * arb(math.factorial(k)) / 4 * cfac(aa, k + 1)))
    return res


def xibar(Xi, Qi, aa, t, nmax, cfac):
    res = []
    for p_, (r, s) in enumerate(PAIRS):
        Dx = D2(Xi[r], Xi[s])
        lst = [xv(Qi[p_], 1, arb(1) / 2).add(trade(Dx.scale(cfac(aa, 1) / 8), t, 1))]
        for l in range(1, nmax + 1):
            lst.append(Dx.mul(Mk(Xi[r], Xi[s], l - 1)).scale(arb(math.factorial(l)) / 8 * cfac(aa, l + 1)))
        res.append(lst)
    return res


def xibar_cross(iu, iv, aa, t, nmax, cfac):
    """majorants of xi_h(tau) derivatives for the cross pair (sigma_M, sigma''_M), with Q_MM''/2 <= X_M + X''_M."""
    Dx = D2(iu, iv)
    lst = [xv(iu).add(xv(iv)).add(trade(Dx.scale(cfac(aa, 1) / 8), t, 1))]
    for l in range(1, nmax + 1):
        lst.append(Dx.mul(Mk(iu, iv, l - 1)).scale(arb(math.factorial(l)) / 8 * cfac(aa, l + 1)))
    return lst


def fbd(xd, mono_, n):
    if len(mono_) == 1:
        return xd[mono_[0]][n]
    e1, e2 = mono_
    res = ae.NPolyA(NV12, BB)
    for l in range(n + 1):
        res = res.add(xd[e1][l].mul(xd[e2][n - l]).scale(math.comb(n, l)))
    return res


def pi_vac(j, Xi, Qi, aa, t, cfac):
    xd = xibar(Xi, Qi, aa, t, j, cfac)
    res = ONE_P if j == 0 else ae.NPolyA(NV12, BB)
    for i in (1, 2, 3):
        for cb, mono_ in zip(QV[i], BASIS):
            if cb == 0.0:
                continue
            for l in range(0, min(i, j) + 1):
                coef = arb(math.comb(j, l) * (math.factorial(i) // math.factorial(i - l))) * abs(cb)
                term = fbd(xd, mono_, j - l).scale(coef)
                res = res.add(trade(term, t, i - l) if i - l > 0 else term)
    return res


def pi_state(j, Xi, Qi, aa, t, cfac, b):
    xd = xibar(Xi, Qi, aa, t, j, cfac)
    res = ONE_P.scale(abs(float(Smat[0, b]))) if j == 0 else ae.NPolyA(NV12, BB)
    for cb, mono_ in zip(Smat[1:, b], BASIS):
        if cb != 0.0:
            res = res.add(fbd(xd, mono_, j).scale(abs(float(cb))))
    return res


def pi_h(j, aa_cross, aa_e, t, cfac):
    xh = xibar_cross(XS[1], XD[1], aa_cross, t, j, cfac)
    res = ae.NPolyA(NV12, BB)
    for l in range(j + 1):
        res = res.add(xh[l].mul(pi_vac(j - l, XD, QD, aa_e, t, cfac)).scale(math.comb(j, l)))
    return res


def pi_hb(j, aa_cross, aa_e, t, cfac, b):
    """the hook kinds h1, h3 (ADD2 sect. 3): Leibniz of xibar_cross with pi_state of the inner state b, as pi_h does with pi_vac."""
    xh = xibar_cross(XS[1], XD[1], aa_cross, t, j, cfac)
    res = ae.NPolyA(NV12, BB)
    for l in range(j + 1):
        res = res.add(xh[l].mul(pi_state(j - l, XD, QD, aa_e, t, cfac, b)).scale(math.comb(j, l)))
    return res


def pi_t(j, aa_cross, aa_e, t, cfac):
    """kt_cert_v1_7 (pk15's pi_t): pi_h with the top-row cross pair (sigma_T, sigma''_T), Q_TT''/2 <= X_T + X''_T."""
    xh = xibar_cross(XS[0], XD[0], aa_cross, t, j, cfac)
    res = ae.NPolyA(NV12, BB)
    for l in range(j + 1):
        res = res.add(xh[l].mul(pi_vac(j - l, XD, QD, aa_e, t, cfac)).scale(math.comb(j, l)))
    return res


def Dbar(n, h, pis):
    Y = [ONE_P]
    for mm in range(n):
        acc = ae.NPolyA(NV12, BB)
        for i in range(mm + 1):
            acc = acc.add(h[i + 1].mul(Y[mm - i]).scale(math.comb(mm, i)))
        Y.append(acc)
    res = ae.NPolyA(NV12, BB)
    for j in range(n + 1):
        res = res.add(pis[j].mul(Y[n - j]).scale(math.comb(n, j)))
    return res


# -------------------------------------------------------------------------------------- kt_cert_v1_8: the two trade fixes, majfix_v1_1
# The trade above (trade, xibar, xibar_cross, pi_vac, pi_state, pi_h, pi_hb, pi_t) stays only to give today's degrees (D4's total degree,
# pi0''s degree) and the plant of C-MAJ-SAMPLE. Every majorant a piece uses comes from majfix_v1_1: built untraded (M3's form) in the form
# basis (d_uv atoms, a formal t), capped where a budget applies, evaluated after the cap; nothing coefficient-wise happens after evaluation.
FB = mf.FormBasis(NV12, XS + XD, QS + QD)
RADV_MAIN = mf.radv_for(a_e, a_m, a_e)                # a_m on sigma, a_e on sigma'' (4x for Q): the main chart
RADV_ANN = mf.radv_for(a_pp, a_m, a_e)                # the annulus: a_pp on sigma''
PROP_TOT = 10                                         # D4's total degree budget: max(today's, 10) (t, h: today's 10; e1, e3: 9 + 1)
FIXSTAT = {}
TMONO = {}


def tmono_note(polys, label):
    """C-TMONO, per path: every capped (or untraded) form-basis polynomial has all coefficients certainly >= 0 before substitution; the
    cap's choices depend only on exponents and budgets, never on t, so each is nondecreasing in t on the chart (the place-2)."""
    n, bad = TMONO.get(label, (0, 0))
    TMONO[label] = (n + len(polys), bad + sum(mf.tmono_bad(p) for p in polys))


def c_tmono(fails):
    bad = sum(b for _, b in TMONO.values())
    out('C-TMONO N=%d %s %s: %s -> %s' % (NN, KIND, PIECE, '; '.join('%s: %d polynomials, %d coefficients not certainly >= 0' % (k, n, b)
                                                                   for k, (n, b) in sorted(TMONO.items())) or 'no polynomial',
                                         'PASS' if bad == 0 else 'FAIL'))
    if bad:
        fails.append('C-TMONO')


def g_source(kind, j, aa_cross, aa_e):
    """the untraded form-basis majorant of the j-th tau-derivative of the kind's source factor: pi_t (row T), pi_h (row M), pi_hb (h1, h3)
    or pi_state (e1, e3), at aa_cross on the cross pair and aa_e on the inner triangle."""
    if kind in ('t', 'h'):
        row = 0 if kind == 't' else 1
        return FB.pi_cross(j, XS[row], XD[row], aa_cross, XD, QD, PAIRS, aa_e, QV, BASIS)
    b = {'e1': 1, 'e3': 3, 'h1': 1, 'h3': 3}[kind]
    if kind in ('h1', 'h3'):
        return FB.pi_cross_state(j, XS[1], XD[1], aa_cross, XD, QD, PAIRS, aa_e, float(Smat[0, b]), [float(x) for x in Smat[1:, b]], BASIS)
    return FB.pi_state(j, XD, QD, PAIRS, aa_e, float(Smat[0, b]), [float(x) for x in Smat[1:, b]], BASIS)


PIS_CACHE = {}


def fix_pis_c(kind, t, hL):
    """D4's pis: g_source capped at TOT - maxdeg(Y[4 - j]), TOT = max(today's D4 total degree, PROP_TOT); returns (pis, pis by formal-t
    order, TOT, budgets, today's Q degree). Kept per t (the gates and the piece use the same pis)."""
    key = (kind, float(t.mid()))
    if key in PIS_CACHE:
        return PIS_CACHE[key]
    D4old = Dbar(4, hL, source_pis(kind, t))           # today's degrees only
    eo = D4old.exponents()
    tot = max(int(eo.sum(axis=1).max()), PROP_TOT)
    qold = int(eo[:, 9:].sum(axis=1).max())
    yd = mf.ydegs(hL, 4, ONE_P, ae.NPolyA, BB, NV12)
    budgets = [tot - yd[4 - j] for j in range(5)]
    caps = [FB.cap(g_source(kind, j, max(a_m, a_e), a_e), budgets[j], RADV_MAIN, FIXSTAT) for j in range(5)]
    tmono_note(caps, 'D4 pis (capped)')
    pis = [FB.evaluate(c, t, ae.NPolyA, BB, D2) for c in caps]
    kmax = max(FB.max_t_order(c) for c in caps)
    byord = {k: [FB.evaluate(c, t, ae.NPolyA, BB, D2, order=k) for c in caps] for k in range(kmax + 1)}
    out('MAJFIX N=%d %s %s: D4 budgets %s (TOT %d = max(today\'s, %d)); cap calls %d, steps %d, atom splits %d; formal-t orders 0..%d '
        '(cpu %.1f s)' % (NN, KIND, PIECE, ','.join(str(b) for b in budgets), tot, PROP_TOT, FIXSTAT.get('calls', 0), FIXSTAT.get('steps', 0),
                          FIXSTAT.get('splits', 0), kmax, cpu()))
    PIS_CACHE[key] = (pis, byord, tot, budgets, qold)
    return PIS_CACHE[key]


def fix_pis0(g, i, t):
    """the L0 side's pis: majfix_v1_1's untraded pi_vac (psi) or pi_state (e1, e3, e2) on the sigma triangle at a_m; no cap (Wishart only)."""
    if g == 'psi':
        p = FB.pi_vac(i, XS, QS, PAIRS, a_m, QV, BASIS)
    else:
        bb = {'e1': 1, 'e3': 3, 'e2': 2}[g]
        p = FB.pi_state(i, XS, QS, PAIRS, a_m, float(Smat[0, bb]), [float(x) for x in Smat[1:, bb]], BASIS)
    tmono_note([p], 'L0 pis0 (untraded)')
    return FB.evaluate(p, t, ae.NPolyA, BB, D2)


def fix_pi0pp(kind, t):
    """ann's pi0'': g_source at a_pp (j = 0), capped at today's pi0'' degree, radii a_pp on sigma''."""
    if kind == 'h':
        old = pi_h(0, a_pp, a_pp, t, cf_rad)
    elif kind == 't':
        old = pi_t(0, a_pp, a_pp, t, cf_rad)
    elif kind in ('h1', 'h3'):
        old = pi_hb(0, a_pp, a_pp, t, cf_rad, {'h1': 1, 'h3': 3}[kind])
    else:
        old = pi_state(0, XD, QD, a_pp, t, cf_rad, {'e1': 1, 'e3': 3}[kind])
    dA = int(old.degrees().max())
    cap = FB.cap(g_source(kind, 0, a_pp, a_pp), dA, RADV_ANN, FIXSTAT)
    tmono_note([cap], 'ann pi0pp (capped)')
    out('MAJFIX N=%d %s %s: pi0\'\' budget %d (today\'s degree), radii a_pp on sigma\'\'' % (NN, KIND, PIECE, dA))
    return FB.evaluate(cap, t, ae.NPolyA, BB, D2)


def fix_pis_a(t):
    """the a-engine's pis: xi_a+'s majorants (the mean of the TM and MB entries) times pi_vac's, untraded (majfix_v1_1, sigma triangle)."""
    xd = FB.xibar(XS, QS, PAIRS, a_m, 4)
    xa = [FB.scale(FB.add(xd[0][l], xd[1][l]), arb(1) / 2) for l in range(5)]
    res = []
    for j in range(5):
        acc = {}
        for l in range(j + 1):
            acc = FB.add(acc, FB.scale(FB.mul(xa[l], FB.pi_vac(j - l, XS, QS, PAIRS, a_m, QV, BASIS)), math.comb(j, l)))
        res.append(acc)
    tmono_note(res, 'a-engine pis (untraded)')
    return [FB.evaluate(p, t, ae.NPolyA, BB, D2) for p in res]


def c_radv(fails, fires):
    """C-RADV: each radius vector given to the cap is certainly >= its region's radii; PLANT-RADV: today's AVt on the
    annulus must fail."""
    try:
        mf.check_radv(RADV_MAIN, a_e, a_m, a_e)
        mf.check_radv(RADV_ANN, a_pp, a_m, a_e)
        ok = True
    except mf.RadiusError as e:
        ok = False
        out('C-RADV detail: %s' % e)
    try:
        mf.check_radv([a_m] * 3 + [4 * a_m] * 3 + [a_e] * 3 + [4 * a_e] * 3, a_pp, a_m, a_e)
        fired = False
    except mf.RadiusError:
        fired = True
    out('C-RADV N=%d: main chart (a_m, 4 a_m; a_e, 4 a_e) and annulus (a_m, 4 a_m; a_pp, 4 a_pp) vectors -> %s; PLANT-RADV (today\'s AVt on '
        'the annulus) -> %s' % (NN, 'PASS' if ok else 'FAIL', 'FIRES' if fired else 'DOES NOT FIRE'))
    if not ok:
        fails.append('C-RADV')
    if not fired:
        fires.append('PLANT-RADV')


SAMPLE_SEED = 20261107


def majfix_gates(fails, fires):
    """the F-2 gates of a piece that uses majorants (c, tA, g), before it computes: C-RADV, PLANT-TRADE-POS, C-P0SUB (xibar, the piece's
    triangle, l = 0..5), C-MAJ-SAMPLE on the majorants this piece uses (seeded chart points, annulus points for tA, the fixed points) and
    PLANT-MAJ-SAMPLE (today's xibar l = 0). C-TRADE-POS stops inside FB.cap (main catches it)."""
    c_radv(fails, fires)
    neg = FB.mul(FB.mono(tk=1), FB.add(FB.mono(((XD[0], 2),)), FB.mono(((XD[0], 1), (XD[1], 1)), c=-2), FB.mono(((XD[1], 2),))))
    try:
        FB.cap(neg, 1, RADV_MAIN)
        fired = False
    except mf.TradePosError:
        fired = True
    out('PLANT-TRADE-POS N=%d: the expanded D2 (cross coefficient -2) given to the cap -> %s' % (NN, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-TRADE-POS')
    J = J_MAIN
    t = arb(1) / J
    tf = 1.0 / J
    bad = 0
    for Xi, Qi, aa in ((XD, QD, a_e), (XS, QS, a_m)):
        xd = FB.xibar(Xi, Qi, PAIRS, aa, 5)
        xo = xibar(Xi, Qi, aa, t, 5, cf_rad)
        for p_, (r, s) in enumerate(PAIRS):
            bad += mf.p0sub(FB.evaluate(xd[p_][0], t, ae.NPolyA, BB, D2),
                            xv(Qi[p_], 1, arb(1) / 2).add(D2(Xi[r], Xi[s]).scale(t * cf_rad(aa, 1) / 8)))
            for l in range(1, 6):
                bad += mf.p0sub(FB.evaluate(xd[p_][l], t, ae.NPolyA, BB, D2), xo[p_][l])
    out('C-P0SUB N=%d %s %s: xibar (inner and outer, l = 0..5) evaluated vs the direct expansion (l = 0: Q/2 + t cfac D2/8; l >= 1: today\'s '
        'entries): %d mismatches -> %s' % (NN, KIND, PIECE, bad, 'PASS' if bad == 0 else 'FAIL'))
    if bad:
        fails.append('C-P0SUB')
    a_in = a_pp if PIECE[:2] == 'tA' else a_e
    Xp, QC = mf.sample_points(J, float(a_m), float(a_in), nn, PAIRS, XS, QS, XD, QD, SAMPLE_SEED + NN)
    taus = (0.0, 0.5 * tf, tf)
    xs_in = [[mf.s_xi(Xp[:, QD[p_]], Xp[:, XD[r]], Xp[:, XD[s]], tau0) for p_, (r, s) in enumerate(PAIRS)] for tau0 in taus]
    xs_out = [[mf.s_xi(Xp[:, QS[p_]], Xp[:, XS[r]], Xp[:, XS[s]], tau0) for p_, (r, s) in enumerate(PAIRS)] for tau0 in taus]
    pi_in = [mf.s_pi(x_, tau0, QV, BASIS) for x_, tau0 in zip(xs_in, taus)]
    pi_out = [mf.s_pi(x_, tau0, QV, BASIS) for x_, tau0 in zip(xs_out, taus)]

    def src_series(kind, x_in, pin, tau0):
        if kind in ('t', 'h'):
            row = 0 if kind == 't' else 1
            return mf._s_mul(mf.s_xi(QC[:, row], Xp[:, XS[row]], Xp[:, XD[row]], tau0), pin)
        b = {'e1': 1, 'e3': 3}[kind]
        return mf.s_state(x_in, float(Smat[0, b]), [float(x) for x in Smat[1:, b]], BASIS)
    cells = []
    if PIECE == 'c':
        hL = {k: hk(k, [(v, a_e) for v in XD], bondsL, cf_rad) for k in range(1, 5)}
        pis = fix_pis_c(KIND, t, hL)[0]
        fv = [src_series(KIND, x_, p_, tau0) for x_, p_, tau0 in zip(xs_in, pi_in, taus)]
        for j in range(5):
            cells.append(('D4 pis j%d' % j, mf.peval(pis[j], Xp), [mf.deriv(f, j) for f in fv]))
    elif PIECE[:2] == 'tA':
        P = fix_pi0pp(KIND, t)
        fv = [src_series(KIND, x_, p_, tau0) for x_, p_, tau0 in zip(xs_in, pi_in, taus)]
        cells.append(('ann pi0pp j0', mf.peval(P, Xp), [mf.deriv(f, 0) for f in fv]))
    elif PIECE == 'g':
        for j in range(5):
            cells.append(('L0 pi_vac j%d' % j, mf.peval(fix_pis0('psi', j, t), Xp), [mf.deriv(f, j) for f in pi_out]))
        for b in GK.get(KIND, ('psi', 'e1', 'e3')):                      # kt_cert_v1_9 (the review v1_8 N-1): the L0 pi_state majorants
            if b == 'psi':
                continue
            bb = {'e1': 1, 'e3': 3, 'e2': 2}[b]
            fs = [mf.s_state(x_, float(Smat[0, bb]), [float(x) for x in Smat[1:, bb]], BASIS) for x_ in xs_out]
            for j in range(5):
                cells.append(('L0 pi_state %s j%d' % (b, j), mf.peval(fix_pis0(b, j, t), Xp), [mf.deriv(f, j) for f in fs]))
        if KIND in ('a', 'am'):
            pa = fix_pis_a(t)
            fa = [mf._s_mul(0.5 * (x_[0] + x_[1]), p_) for x_, p_ in zip(xs_out, pi_out)]
            for j in range(5):
                cells.append(('a-engine pis j%d' % j, mf.peval(pa[j], Xp), [mf.deriv(f, j) for f in fa]))
    badc, _ = mf.sample_check(cells)
    for name, nb, wr in badc[:6]:
        out('C-MAJ-SAMPLE-FAIL N=%d %s %s: %s at %d (point, tau0) pairs, worst |f|/M %.6f' % (NN, KIND, PIECE, name, nb, wr))
    xo0 = xibar(XD, QD, a_e, t, 0, cf_rad)
    Xm, _ = mf.sample_points(J, float(a_m), float(a_e), nn, PAIRS, XS, QS, XD, QD, SAMPLE_SEED + NN)
    xsm = [[mf.s_xi(Xm[:, QD[p_]], Xm[:, XD[r]], Xm[:, XD[s]], tau0) for p_, (r, s) in enumerate(PAIRS)] for tau0 in taus]
    badp, fixed = mf.sample_check([('xibar_in p%d l0' % p_, mf.peval(xo0[p_][0], Xm), [mf.deriv(x_[p_], 0) for x_ in xsm]) for p_ in range(3)])
    out('C-MAJ-SAMPLE N=%d %s %s: %d cells x %d points x 3 tau0 (seed %d; %s), %d failing -> %s; PLANT-MAJ-SAMPLE (today\'s xibar l0): %d '
        'failing cells, %d at the fixed points -> %s' % (NN, KIND, PIECE, len(cells), Xp.shape[0], SAMPLE_SEED + NN,
                                                             'annulus' if a_in is a_pp else 'main chart', len(badc), 'PASS' if not badc else 'FAIL',
                                                             len(badp), fixed, 'FIRES' if (badp and fixed) else 'DOES NOT FIRE'))
    if badc:
        fails.append('C-MAJ-SAMPLE')
    if not (badp and fixed):
        fires.append('PLANT-MAJ-SAMPLE')


bondsL = [(XD[r], XD[s], TRI[p_], a_e) for p_, (r, s) in enumerate(PAIRS)] + \
         [(XS[r], XD[r], 1, max(a_m, a_e)) for r in range(3)] + [(XS[0], XS[1], 1, a_m), (XS[1], XS[2], 1, a_m)]
bonds0 = [(XS[r], XS[s], TRI[p_], a_m) for p_, (r, s) in enumerate(PAIRS)]


# ====================================================================================== part 4a: covariances, joint moments, tails, L0 side
# (kt_c_v2_3 l.763-969 in balls; the gauge basis is exact (ADD2 sect. 1); positivity by Sylvester's criterion on certain balls)
def lap_a(edges, V):
    L = arb_mat(V, V)
    for (u, v), c in edges:
        c = ae.A(c)
        L[u, u] += c
        L[v, v] += c
        L[u, v] -= c
        L[v, u] -= c
    return L


def gauge_basis_a(V, S):
    """an exact basis of the orthogonal complement of u = 1_S: e_s - e_s0 for s in S \\ {s0}, and e_k for k not in S (ADD2 sect. 1)."""
    S = sorted(S)
    cols = [(s, S[0]) for s in S[1:]] + [(k, None) for k in range(V) if k not in S]
    Bm = arb_mat(V, len(cols))
    for j, (a_, b_) in enumerate(cols):
        Bm[a_, j] = 1
        if b_ is not None:
            Bm[b_, j] = -1
    return Bm


TILT_LOG = []          # (label, certified, smallest leading minor's lower end) for every positive-definiteness test (C-TILT (b))


def surely_pd(M, label='pd'):
    """Sylvester's criterion: every leading principal minor certainly positive; logged in TILT_LOG."""
    n = M.nrows()
    low = None
    for k in range(1, n + 1):
        sub = arb_mat(k, k)
        for i in range(k):
            for j in range(k):
                sub[i, j] = M[i, j]
        d = sub.det()
        lo = float(d.lower())
        low = lo if low is None else min(low, lo)
        if not (d > 0):
            TILT_LOG.append((label, False, lo))
            return False
    TILT_LOG.append((label, True, low))
    return True


def tilted_cov_a(L, Bm, rates, extra=None, label='tilted_cov'):
    """kt_c_v2_3.tilted_cov in balls: (B Lt^-1 B^T, (det(B^T L B)/det Lt)^(nn/2)), Lt = B^T (L - 2 diag(rates) - 2 extra) B; (None, None)
    unless Lt is certainly positive definite."""
    V = L.nrows()
    Lx = arb_mat(V, V)
    for i in range(V):
        for j in range(V):
            Lx[i, j] = L[i, j] - (2 * ae.A(rates[i]) if i == j else 0) - (2 * extra[i, j] if extra is not None else 0)
    Lr = Bm.transpose() * L * Bm
    Lt = Bm.transpose() * Lx * Bm
    if not surely_pd(Lt, label):
        return None, None
    ratio = Lr.det() / Lt.det()
    return Bm * Lt.inv() * Bm.transpose(), (ratio.log() * nn / 2).exp()


def chi_tail_a(s):
    """P(chi_nn^2 > s) bound in balls: exp(-s/2) (nn = 2); erfc(sqrt(s/2)) + sqrt(2s/pi) exp(-s/2) (nn = 3), with erfc(x) <= exp(-x^2)/(x sqrt pi)
    (x > 0 asserted; nonnegative coefficient, ADD1 b)."""
    if nn == 2:
        return (-s / 2).exp()
    x = (s / 2).sqrt()
    assert x > 0
    return (-(x * x)).exp() / (x * arb.pi().sqrt()) + (2 * s / arb.pi()).sqrt() * (-s / 2).exp()


E9 = [((6 + r, 6 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((6 + r, r), 1) for r in range(3)] + [((r, 3 + r), 1) for r in range(3)] + [((0, 1), 1), ((1, 2), 1)]
L9 = lap_a(E9, 9)
B9 = gauge_basis_a(9, range(6))
ED_ = [((r, s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
      [((r, 3 + r), 1) for r in range(3)]
LD = lap_a(ED_, 6)
BD = gauge_basis_a(6, range(6))
W10 = arb_mat(6, 10)
for r in range(3):
    W10[r, r] = 1
    W10[3 + r, 3 + r] = 1
for p_, (r, s) in enumerate(PAIRS):
    W10[3 + r, 6 + p_] = 1
    W10[3 + s, 6 + p_] = -1
W10[ROWX, 9] = 1                             # kt_cert_v1_7: the cross form on the insertion's row (T for kind t, M otherwise)
W10[3 + ROWX, 9] = -1
W10_INT = [[0] * 10 for _ in range(6)]       # W10's exact integers, for AllMom2A's exact zeros (kt_cert_v1_5)
for r in range(3):
    W10_INT[r][r] = 1
    W10_INT[3 + r][3 + r] = 1
for p_, (r, s) in enumerate(PAIRS):
    W10_INT[3 + r][6 + p_] = 1
    W10_INT[3 + s][6 + p_] = -1
W10_INT[ROWX][9] = 1
W10_INT[3 + ROWX][9] = -1
assert all(W10[i, j] == W10_INT[i][j] for i in range(6) for j in range(10))
PLANTED = [False]                            # PLANT-SING runs once per piece, on its first table
MAP10 = {0: 0, 1: 1, 2: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8, (QT if KIND == 't' else QH): 9}     # kt_cert_v1_7: QT for kind t


def to10(P, nv):
    res = {}
    for e, c in P.items():
        assert all(e[i] == 0 for i in range(nv) if i not in MAP10), e
        e10 = [0] * 10
        for i, j in MAP10.items():
            if i < nv:
                e10[j] = e[i]
        e10 = tuple(e10)
        res[e10] = res[e10] + c if e10 in res else ae.A(c)
    return {e: c for e, c in res.items() if not c.is_zero()}


def sub_mat(M, idx):
    S = arb_mat(len(idx), len(idx))
    for a_, i in enumerate(idx):
        for b_, j in enumerate(idx):
            S[a_, b_] = M[i, j]
    return S


def joint_moments_a(rates9, Dmax, qcap, extra=None, label='tilted_cov'):
    """the joint tilted moments of the ten forms (sigma X, sigma'' X, sigma'' Q, Q_MM''); extra: an optional 9 x 9 quadratic tilt (F1's
    lam Q_rr''). kt_cert_v1_5: the ten forms span six coordinates, so AllMom2A gets W10's exact integers (W_int) and treats the minors of
    rank-deficient subsets as exact zeros (arbeng_c2b_v2). Returns (table, N, G9, Gam)."""
    G9, N9 = tilted_cov_a(L9, B9, rates9, extra=extra, label=label)
    if G9 is None:
        return None, None, None, None
    G6 = sub_mat(G9, [0, 1, 2, 6, 7, 8])
    Gam = W10.transpose() * G6 * W10
    return ae.AllMom2A(Gam, nn, Dmax, groups=[0] * 6 + [1] * 4, caps={1: qcap}, W_int=W10_INT), N9, G9, Gam


SING_FAILS, SING_FIRES = [], []         # C-SING failures and unfired PLANT-SING, merged into the item's verdict in main()


def det_sub(Gam, A):
    """det(Gam_A) by the same arithmetic as AllMom2A (an arb_mat of the entries, then det)."""
    sub = arb_mat(len(A), len(A))
    for a_, fa in enumerate(A):
        for b_, fb in enumerate(A):
            sub[a_, b_] = Gam[fa, fb]
    return sub.det()


def c_sing(am, Gam, qcap, label):
    """C-SING (arbeng_c2b_v2's exact zeros, on this table's own Gram matrix): (i) every subset the table kept is of full exact rank and its
    stored (-2)^|A| det(Gam_A) is identical (midpoint and radius) to the direct computation; every subset it dropped is rank-deficient and
    its det ball contains 0; kept and dropped together are all the subsets of sizes up to min(10, D) the caps allow; (ii) degree-4 tables
    with and without the rule overlap in every moment."""
    ok, nk, seen = True, 0, set()
    for j in range(1, len(am.Dj)):
        cj, vj = am.Dj[j]
        if len(cj) == 0:
            continue
        for row, v in zip(am.decode(cj), vj):
            A = tuple(int(f) for f in np.flatnonzero(row))
            d = arb(-2) ** len(A) * det_sub(Gam, A)
            ok = ok and len(A) == j and ae.int_rank(W10_INT, A) == j and d.mid() == v.mid() and d.rad() == v.rad()
            seen.add(A)
            nk += 1
    for A, dv in am.dropped:
        ok = ok and ae.int_rank(W10_INT, A) < len(A) and dv.contains(0)
        seen.add(tuple(A))
    allowed = set(A for j in range(1, min(10, am.D) + 1) for A in itertools.combinations(range(10), j) if sum(1 for f in A if f >= 6) <= qcap)
    ok = ok and seen == allowed
    kw = dict(groups=[0] * 6 + [1] * 4, caps={1: qcap})
    t_rule, t_free = ae.AllMom2A(Gam, nn, 4, W_int=W10_INT, **kw), ae.AllMom2A(Gam, nn, 4, **kw)
    nm = 0
    for d_ in range(5):
        for x_, y_ in zip(t_rule.mom[d_], t_free.mom[d_]):
            ok = ok and x_.overlaps(y_)
            nm += 1
    out('C-SING N=%d %s: %d subsets kept (full rank; det balls identical to direct), %d dropped (rank-deficient; det balls contain 0, '
        'largest radius %.2e), all %d allowed subsets covered; degree-4 tables with and without the rule overlap in %d moments -> %s' % (
            NN, label, nk, am.zeroed, am.max_zero_rad, len(allowed), nm, 'PASS' if ok else 'FAIL'))
    if not ok:
        SING_FAILS.append('C-SING %s' % label)


def plant_sing(Gam, qcap):
    """PLANT-SING: the rule with X0's column of W10 set to zero (so every subset with X0 counts as rank-deficient) must stop, since
    det(Gam_{X0}) = Var(X0) > 0 excludes 0."""
    bad = [row[:] for row in W10_INT]
    for i in range(6):
        bad[i][0] = 0
    try:
        ae.AllMom2A(Gam, nn, 2, groups=[0] * 6 + [1] * 4, caps={1: qcap}, W_int=bad)
        fired = False
    except ValueError:
        fired = True
    out('PLANT-SING N=%d: the rule with X0\'s column of W10 zeroed %s -> %s' % (NN, 'stops' if fired else 'passes',
                                                                               'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        SING_FIRES.append('PLANT-SING')


def supF_a(kind, J):
    """sup |F| of the item's source in balls (an upper bound by the triangle inequality on [0, 2J]^3)."""
    t = arb(1) / J
    if kind in ('h', 'a', 't', 'am'):                                    # kt_cert_v1_7: t as h (2J supp0), am as a
        sup0 = 1 + sum(t ** i * abs(cb) * arb(2 * J) ** len(mono_) for i, coef in ((1, QV[1]), (2, QV[2]), (3, QV[3]))
                       for cb, mono_ in zip(coef, BASIS))
        return 2 * J * sup0 if kind in ('h', 't') else sup0
    b = {'e1': 1, 'e3': 3, 'h1': 1, 'h3': 3}[kind]
    supb = abs(float(Smat[0, b])) + sum(abs(float(cb)) * arb(2 * J) ** len(mono_) for cb, mono_ in zip(Smat[1:, b], BASIS))
    return 2 * J * supb if kind in ('h1', 'h3') else supb


def l0_remainder(G, m, t):
    """L0 side: sum_g sum_{j<=3} |m_gj| t^j t^{4-j}/(4-j)! Dbar_{4-j}(E0 p_g) (sigma variables), and the h0 majorants."""
    h0 = {k: hk(k, [], bonds0, cf_rad) for k in range(1, 5)}
    R0 = ae.NPolyA(NV12, BB)
    for gi, g in enumerate(G):
        for j in range(4):
            n_ = 3 - j
            pis0 = [fix_pis0(g, i, t) for i in range(n_ + 2)]                # kt_cert_v1_8: majfix_v1_1, untraded
            R0 = R0.add(Dbar(n_ + 1, h0, pis0).scale(abs(m[j][gi]) * t ** j * t ** (n_ + 1) / math.factorial(n_ + 1)))
    return R0, h0


def source_pis(kind, t):
    if kind == 'h':
        return [pi_h(j, max(a_m, a_e), a_e, t, cf_rad) for j in range(5)]
    if kind == 't':                                                     # kt_cert_v1_7
        return [pi_t(j, max(a_m, a_e), a_e, t, cf_rad) for j in range(5)]
    b = {'e1': 1, 'e3': 3, 'h1': 1, 'h3': 3}[kind]
    if kind in ('h1', 'h3'):
        return [pi_hb(j, max(a_m, a_e), a_e, t, cf_rad, b) for j in range(5)]
    return [pi_state(j, XD, QD, a_e, t, cf_rad, b) for j in range(5)]


# ====================================================================================== part 4b: the certified inputs of piece g (kt_cert_v1_9)
# DESIGN_KT_CERT_v1_9 sect. 1: far (FAR_CRUDE_v1), gBb (the vacuum items G4R_r), eps_r (M2B_KV_v1) and Z (the S9 records), each through its own
# pinned reader bound to the run that wrote it (CERTIN, C-HASH); the readers compute nothing transcendental. Every input is used at J = 300.
# kt_cert_v1_8's part 4b (the FLOAT outer_far3, gB_base, factors_for, src_factors and their riglap2/riglap3/amom2b/npoly/ive imports) is gone.
from fractions import Fraction
J_CERT = 300
CI = {}                                         # the certified inputs of this g piece (certin), read by stage_g, a_engine and engine_value
S9_KEY = {'e1': 'G,1,1', 'e3': 'G,3,3', 'h': 'G,0,0', 'h1': 'G,1,1', 'h3': 'G,3,3', 'a': 'G,0,0', 't': 'G,0,0', 'am': 'G,0,0'}


def farb(f):
    """an exact Fraction (or binary64) as an arb ball: exact when the denominator is a power of 2 and the numerator fits the precision, else
    a ball containing it."""
    f = Fraction(f)
    return arb(f.numerator) / f.denominator


def wpath(rel):
    return os.path.join(W18, rel)


def manifest_has(man_rel, pairs):
    """the side manifest man_rel lists each (path, full sha256) of pairs, by base name."""
    with open(wpath(man_rel)) as fh:
        rows = [ln.split() for ln in fh.read().splitlines() if len(ln.split()) == 2]
    names = {os.path.basename(p): h for h, p in rows}
    return all(names.get(os.path.basename(p)) == h for p, h in pairs)


def far_load():
    """FAR_CRUDE_v1 of N through far_crude_reader_v1.load (its run output, the pinned sha256, N)."""
    rec, outp = FARF[NN]
    return RD_FAR.load(wpath(rec), wpath(outp), CERTIN[rec], NN)


def far_cert(kind, G, m, t, J, far):
    """kt_cert_v1_9 (DESIGN sect. 1; NOTE_FAR_CRUDE_v1 sect. 3): far_mixed's sum with R = 1 and every X(300) bounded by its record's X300:
    hf^2 X_SS + 2 hf sum_g |m_g(t)| X_S_g + sum_{g <= h} w_gh |m_g(t)| |m_h(t)| X_D_g_h, hf = 2J for the hook kinds, else 1; kinds a and am have
    every term on ED (their oSS without hf). The names are kt_cert_v1_8 far_mixed's (l.1583-1612), mapped to call keys by the record.
    Returns (far_out, {name: (call key, X300)})."""
    if J != J_CERT:
        raise ValueError('far_cert: the FAR_CRUDE_v1 items are used at J = 300 only')
    names = far['names'][kind]
    used = {}

    def X(name):
        key = names[name]
        x = far['items'][key][0]
        used[name] = (key, x)
        return farb(x)
    hf = arb(2 * J) if kind in HOOK else arb(1)
    mg = [abs(sum((arb(m[j][gi]) * t ** j for j in range(4)), arb(0))) for gi in range(len(G))]
    far_out = X('oSS') if kind in ('a', 'am') else hf * hf * X('oSS')
    for gi, g in enumerate(G):
        if mg[gi].is_zero():
            continue
        far_out += 2 * hf * mg[gi] * X('oS_%s' % g)
    for gi, g in enumerate(G):
        for hi in range(gi, len(G)):
            if mg[gi].is_zero() or mg[hi].is_zero():
                continue
            far_out += (1 if hi == gi else 2) * mg[gi] * mg[hi] * X('oD_%s_%s' % (g, G[hi]))
    return far_out, used


E4_A = [((r, s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((9 + r, 9 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
       [((r, 3 + r), 1) for r in range(3)] + [((3 + r, 6 + r), 1) for r in range(3)] + [((6 + r, 9 + r), 1) for r in range(3)] + \
       [((3, 4), 1), ((4, 5), 1), ((6, 7), 1), ((7, 8), 1)]       # vacrig11f's G4 (m2b_asm_v1's E4), the exact couplings in arb


def ratio_main(r):
    """m2b_asm_v1's ratio_main: (det(B^T L_E4 B)/det(B^T L_{E4 - (r, 3 + r)} B))^{nn/2} in arb, B an exact basis of the sum-zero subspace
    (the ratio does not depend on it)."""
    Bm = gauge_basis_a(12, range(12))
    edges_r = [(e_, c_) for (e_, c_) in E4_A if e_ != (r, 3 + r)]
    d1 = (Bm.transpose() * lap_a(E4_A, 12) * Bm).det()
    d2 = (Bm.transpose() * lap_a(edges_r, 12) * Bm).det()
    if not (d1 > 0 and d2 > 0):
        raise ValueError('ratio_main: a determinant is not certainly positive')
    return ((d1 / d2).log() * nn / 2).exp()


def j_uniform_up(ball):
    """m2b_asm_v1's j_uniform (upper): 1 + sum_{k=1..3} max(HI_k, 0) 150^-k + err_b on m3_reader_v5's exact entry ball (LO, HI, err_b), an
    upper bound of I_r/main_r for every J >= 150 (PLAN_M3_CODE_v1_2_ADD4 sect. 4); a_0 = 1 exactly is required."""
    LO, HI, eb = ball
    if not (Fraction(LO[0]) == 1 and Fraction(HI[0]) == 1):
        raise ValueError('G4R: a_0 is not exactly 1')
    tq = Fraction(1, 150)
    return 1 + sum(max(Fraction(HI[k]), 0) * tq ** k for k in (1, 2, 3)) + Fraction(eb)


def vac_load():
    """pk03's vacuum record of N through m3_reader_v5.load (bound to its asm output, J_REF 150), its asm manifest, and zR_r^up."""
    pj, po, pm = VACF[NN]
    rec = RD_VAC.load(wpath(pj), wpath(po), 150, NN)
    okm = manifest_has(pm, [(pj, CERTIN[pj]), (po, CERTIN[po])])
    return rec, okm, [j_uniform_up(RD_VAC.entry_ball(rec, 'G4R_%d' % r)) for r in range(3)]


def gbb_cert(J, zr):
    """kt_cert_v1_9: gBb(J) = (sum_r e^{-0.95 J (1 - cos 40 deg)} ratio_main_r zR_r^up)^{1/2}: kt_cert_v1_8's gB_base with each riglap2 bound
    of I_r/main_r replaced by its certified upper end zR_r^up (m2b_asm_v1 l.430 has the same sum at J = 150)."""
    s = sum(((-arb('0.95') * J * (1 - DELTA.cos())).exp() * ratio_main(r) * farb(zr[r]) for r in range(3)), arb(0))
    if not s > 0:
        raise ValueError('gbb_cert: the sum is not certainly positive')
    return s.sqrt()


def m2b_load():
    """kt_rb_v1_6's read_m2b: M2B_KV_v1 through m2b_reader_v1.load (binding to its asm output, every record check, C-PINS), then
    law_v1(rec, N, 300). Returns (eps_r's upper end as an exact Fraction, its decimal string)."""
    rec = RD_M2B.load(wpath(M2BF[0]), wpath(M2BF[1]), expected_sha256=CERTIN[M2BF[0]])
    law = RD_M2B.law_v1(rec, NN, J_CERT)
    return Fraction(law['eps_r']), law['eps_r']


def s9_load():
    """the S9 record of N through m3_reader_v4_4.load (bound to its asm output, J_REF 300), and its side manifest."""
    pj, po, pm = S9F[NN]
    rec = RD_S9.load(wpath(pj), wpath(po), 300, NN)
    return rec, manifest_has(pm, [(pj, CERTIN[pj]), (po, CERTIN[po])])


def z_cert(rec, kind):
    """Z_b(300) = sum_k LO_k 300^-k - err_b of entry G,b,b (m3_reader_v4_4.entry_ball: exact rational ends, err_b the bar without rnd, valid
    for t in [0, 1/300]): a lower end, since t^k > 0. Returns (Z as an exact Fraction, the entry key)."""
    key = S9_KEY[kind]
    LO, HI, eb = RD_S9.entry_ball(rec, key)
    tq = Fraction(1, J_CERT)
    return sum((Fraction(LO[k]) * tq ** k for k in range(len(LO))), Fraction(0)) - Fraction(eb), key


class QK:
    """kt_cert_v1_9 (C-R1): exact arithmetic in Q(sqrt 5, sqrt 21): a + b sqrt5 + c sqrt21 + d sqrt105, Fraction coefficients."""
    __slots__ = ('v',)

    def __init__(self, a=0, b=0, c=0, d=0):
        self.v = (Fraction(a), Fraction(b), Fraction(c), Fraction(d))

    def __add__(self, o):
        return QK(*(x + y for x, y in zip(self.v, qk(o).v)))

    def __sub__(self, o):
        return QK(*(x - y for x, y in zip(self.v, qk(o).v)))

    def __neg__(self):
        return QK(*(-x for x in self.v))

    def __mul__(self, o):
        a1, b1, c1, d1 = self.v
        a2, b2, c2, d2 = qk(o).v
        return QK(a1 * a2 + 5 * b1 * b2 + 21 * c1 * c2 + 105 * d1 * d2, a1 * b2 + b1 * a2 + 21 * (c1 * d2 + d1 * c2),
                  a1 * c2 + c1 * a2 + 5 * (b1 * d2 + d1 * b2), a1 * d2 + d1 * a2 + b1 * c2 + c1 * b2)

    def conj(self, s5, s21):
        a, b, c, d = self.v
        return QK(a, s5 * b, s21 * c, s5 * s21 * d)

    def is_zero(self):
        return all(x == 0 for x in self.v)

    def inv(self):
        num = self.conj(-1, 1) * self.conj(1, -1) * self.conj(-1, -1)
        nrm = self * num
        if not (nrm.v[1] == 0 and nrm.v[2] == 0 and nrm.v[3] == 0 and nrm.v[0] != 0):
            raise ValueError('QK.inv: the norm is not a nonzero rational')
        return QK(*(x / nrm.v[0] for x in num.v))

    def __float__(self):
        return float(self.v[0]) + float(self.v[1]) * math.sqrt(5) + float(self.v[2]) * math.sqrt(21) + float(self.v[3]) * math.sqrt(105)


def qk(x):
    return x if isinstance(x, QK) else QK(x)


def tau_exact(edges, V):
    """the weighted spanning-tree count (matrix-tree: the determinant of the Laplacian without row and column 0), exactly in Q(sqrt 5,
    sqrt 21) by Gaussian elimination with exact pivots."""
    L = [[QK() for _ in range(V)] for _ in range(V)]
    for (u, v), c in edges:
        L[u][u] = L[u][u] + c
        L[v][v] = L[v][v] + c
        L[u][v] = L[u][v] - c
        L[v][u] = L[v][u] - c
    M = [row[1:] for row in L[1:]]
    n, det = V - 1, QK(1)
    for i in range(n):
        p = next((r for r in range(i, n) if not M[r][i].is_zero()), None)
        if p is None:
            return QK()
        if p != i:
            M[i], M[p] = M[p], M[i]
            det = -det
        det = det * M[i][i]
        piv = M[i][i].inv()
        for r in range(i + 1, n):
            if not M[r][i].is_zero():
                f = M[r][i] * piv
                M[r] = [M[r][j] - f * M[i][j] for j in range(n)]
    return det


QA = QK(Fraction(1, 2), 0, Fraction(1, 6), 0)                 # A = (3 + sqrt 21)/6, exactly (TRI's first entries)
QB = QK(0, Fraction(1, 4), Fraction(-1, 12), 0)               # B = (3 sqrt 5 - sqrt 21)/12, exactly (TRI's last entry)


def r1_graphs(A, B):
    """far_mixed's three graphs with exact couplings: ED_f, E3_f, E4_f's edge structure (kt_cert_v1_8 l.1470-1474, l.1555-1556), the vac
    triangles' couplings (A, A, B) and 1 elsewhere."""
    T, one = [A, A, B], QK(1)
    ED = [((r, s), T[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), T[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
         [((r, 3 + r), one) for r in range(3)]
    E3 = [((r, s), T[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((6 + r, 6 + s), T[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
         [((r, 3 + r), one) for r in range(3)] + [((3 + r, 6 + r), one) for r in range(3)] + [((3, 4), one), ((4, 5), one)]
    E4 = [((r, s), T[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((9 + r, 9 + s), T[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
         [((r, 3 + r), one) for r in range(3)] + [((3 + r, 6 + r), one) for r in range(3)] + [((6 + r, 9 + r), one) for r in range(3)] + \
         [((3, 4), one), ((4, 5), one), ((6, 7), one), ((7, 8), one)]
    return ED, E3, E4


def r1_exact(A=QA, B=QB):
    """C-R1 (the review a50a005a Q3 (3)): far_mixed's R = main_N^2/(main_D main_4). With riglap2's main term (logmain: -(V - 1) log area +
    (n (V - 1)/2) log(2 pi/J) - (n/2) log tau, tau = det(Lsub)/V the weighted spanning-tree count), the area and 2 pi/J powers cancel
    (2 (9 - 1) = (6 - 1) + (12 - 1)), so R = (tau_D tau_4 / tau_N^2)^(n/2). Returns (tau_N^2 - tau_D tau_4, (tau_D, tau_N, tau_4)), all
    exact; R = 1 iff the first is zero."""
    ED, E3, E4 = r1_graphs(A, B)
    tD, tN, t4 = tau_exact(ED, 6), tau_exact(E3, 9), tau_exact(E4, 12)
    return tN * tN - tD * t4, (tD, tN, t4)


def lookalikes(loads_fn, rec_rel, out_rel, extra):
    """Copies of a certified record whose format carries _PRECERT, _STUB or _MOCK, each with the asm RECORD line re-bound
    to the copy's bytes, must be refused by the certified reader; the unchanged re-dumped copy, re-bound the same way, must be accepted (the
    control). Returns (control accepted, [refused per suffix])."""
    with open(wpath(rec_rel)) as fh:
        rec_text = fh.read()
    with open(wpath(out_rel)) as fh:
        out_text = fh.read()
    name = os.path.basename(rec_rel)

    def try_copy(suffix):
        obj = json.loads(rec_text)
        if suffix:
            obj['format'] = obj['format'] + suffix
        text = json.dumps(obj)
        sha = hashlib.sha256(text.encode()).hexdigest()
        otext = '\n'.join(('RECORD %s %s' % (name, sha)) if ln.startswith('RECORD %s ' % name) else ln for ln in out_text.splitlines()) + '\n'
        return refused(loads_fn, text, otext, *(extra + (name,)))
    return (not try_copy('')), [try_copy(s) for s in ('_PRECERT', '_STUB', '_MOCK')]


def refused(fn, *a):
    try:
        fn(*a)
        return False
    except ValueError:
        return True


def certin(kind, fails, fires):
    """kt_cert_v1_9: load and gate the certified inputs of piece g (C-FAR, C-GBB, C-EPSR, C-Z with PLANT-FAR, PLANT-GBB, PLANT-EPSR,
    PLANT-Z); fills CI with far, gBb (kinds other than a, am), zR, eps_r and Z."""
    far = far_load()
    G = GK.get(kind, ('psi', 'e1', 'e3'))
    okn = RD_FAR.G_OF.get(kind, ('psi', 'e1', 'e3')) == G and far['names'][kind] == RD_FAR.NAMES[kind]
    out('C-FAR N=%d %s: %s (sha256 %s) through far_crude_reader_v1.load, bound to %s: %d call items; the record\'s G for the kind equals GK '
        '%s and its names map is far_mixed\'s -> %s' % (NN, kind, os.path.basename(FARF[NN][0]), CERTIN[FARF[NN][0]][:8],
                                                       os.path.basename(FARF[NN][1]), len(far['items']), list(G), 'PASS' if okn else 'FAIL'))
    if not okn:
        fails.append('C-FAR')
    with open(wpath(FARF[NN][0]), 'rb') as fh:
        fdata = fh.read()
    with open(wpath(FARF[NN][1])) as fh:
        ftext = fh.read()
    fired = refused(RD_FAR.loads, fdata.replace(b'"X300": "', b'"X300": "1', 1), ftext, os.path.basename(FARF[NN][0]),
                    CERTIN[FARF[NN][0]], NN)
    out('PLANT-FAR N=%d %s: the record with a digit put in front of one X300, not re-bound, must be refused -> %s' % (
        NN, kind, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-FAR')
    fc_dirs = [d for d in ('pk02/SCRATCH_fc_d1', 'pk02/SCRATCH_fc_d2') if '%s/FAR_CRUDE_v1_N%d.json' % (d, NN) != FARF[NN][0]]
    refs = [refused(RD_FAR.load, wpath('%s/FAR_CRUDE_v1_N%d.json' % (d, NN)), wpath('%s/out_n%d.txt' % (d, NN)), CERTIN[FARF[NN][0]], NN)
            for d in fc_dirs]
    fired = bool(refs) and all(refs)
    out('PLANT-FAR-HAND N=%d %s: the hand records of %s through the pinned path (expected sha256 %s) must be refused: %s -> %s' % (
        NN, kind, ', '.join(fc_dirs), CERTIN[FARF[NN][0]][:8], refs, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-FAR-HAND')
    CI['far'] = far
    if kind not in ('a', 'am'):
        _vrec, okm, zr = vac_load()
        gbb = gbb_cert(J_CERT, zr)
        okg = okm and all(z >= 1 for z in zr)
        out('C-GBB N=%d %s: %s through m3_reader_v5.load (J_REF 150, bound to its asm output; manifest %s); zR_r^up (r = 0, 1, 2) %s; gBb(300) '
            '= %s -> %s' % (NN, kind, os.path.basename(VACF[NN][0]), 'PASS' if okm else 'FAIL', ', '.join('%.12f' % float(z) for z in zr),
                           bstr(gbb), 'PASS' if okg else 'FAIL'))
        if not okg:
            fails.append('C-GBB')
        fired = bool(gbb_cert(J_CERT, [zr[0] + 1] + zr[1:]) > gbb)
        out('PLANT-GBB N=%d %s: zR_0^up + 1 must give a certainly larger gBb -> %s' % (NN, kind, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-GBB')
        ctl, refs = lookalikes(RD_VAC.loads, VACF[NN][0], VACF[NN][1], (150, NN))
        fired = ctl and all(refs)
        out('PLANT-VAC-LOOK N=%d %s: %s with format _PRECERT, _STUB, _MOCK (asm RECORD re-bound) refused by m3_reader_v5: %s; control (unchanged '
            'copy, re-bound) accepted: %s -> %s' % (NN, kind, os.path.basename(VACF[NN][0]), refs, ctl, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-VAC-LOOK')
        CI['gBb'], CI['zr'] = gbb, zr
    eps, epsd = m2b_load()
    oke = 0 < eps < Fraction(1, 1000)
    out('C-EPSR N=%d %s: M2B_KV_v1 through m2b_reader_v1.load (binding, C-PINS), law_v1(rec, %d, 300): eps_r <= %s -> %s' % (
        NN, kind, NN, epsd, 'PASS' if oke else 'FAIL'))
    if not oke:
        fails.append('C-EPSR')
    with open(wpath(M2BF[0])) as fh:
        mtext = fh.read()
    with open(wpath(M2BF[1])) as fh:
        matext = fh.read()
    pos = mtext.index('_EPS_R_300 = ') + len('_EPS_R_300 = ')
    mbad = mtext[:pos] + ('2' if mtext[pos] != '2' else '3') + mtext[pos + 1:]
    fired = refused(RD_M2B.loads, mbad, os.path.basename(M2BF[0]), matext, CERTIN[M2BF[0]])
    out('PLANT-EPSR N=%d %s: M2B_KV_v1 with the first digit of an EPS_R_300 value changed must be refused -> %s' % (
        NN, kind, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-EPSR')
    srec, oks = s9_load()
    Z, zkey = z_cert(srec, kind)
    okz = oks and Z > 0
    out('C-Z N=%d %s: %s through m3_reader_v4_4.load (J_REF 300, bound to its asm output; side manifest %s); %s: Z_b = sum_k LO_k 300^-k - '
        'err_b = %s -> %s' % (NN, kind, os.path.basename(S9F[NN][0]), 'PASS' if oks else 'FAIL', zkey, '%.15f' % float(Z),
                              'PASS' if okz else 'FAIL'))
    if not okz:
        fails.append('C-Z')
    with open(wpath(S9F[NN][0])) as fh:
        stext = fh.read()
    with open(wpath(S9F[NN][1])) as fh:
        sotext = fh.read()
    fired = refused(RD_S9.loads, stext, sotext.replace('VERDICT VALID', 'VERDICT VALID-PRECERT'), 300, NN, os.path.basename(S9F[NN][0]))
    out('PLANT-Z N=%d %s: the S9 asm output with VERDICT VALID-PRECERT must be refused -> %s' % (NN, kind, 'FIRES' if fired else
                                                                                               'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-Z')
    ctl, refs = lookalikes(RD_S9.loads, S9F[NN][0], S9F[NN][1], (300, NN))
    fired = ctl and all(refs)
    out('PLANT-S9-LOOK N=%d %s: %s with format _PRECERT, _STUB, _MOCK (asm RECORD re-bound) refused by m3_reader_v4_4: %s; control accepted: %s '
        '-> %s' % (NN, kind, os.path.basename(S9F[NN][0]), refs, ctl, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-S9-LOOK')
    CI.update(eps=eps, eps_dec=epsd, Z=Z, zkey=zkey)
    return CI


# ====================================================================================== part 5: engine A in stages, and the a-engine
# (kt_c_v2_3 l.970-1130) in balls; the far parts and gB are FLOAT inputs (part 4b), printed with repr (F4) and entering as exact binary64 numbers.
# kt_cert_v1_3: engine A is cut into stages that the pieces of an item share (part 6): stage_c (D4, its conditional expectation, nD),
# tail_term (one Chernoff table each: tailX, tailB by F1, ann), stage_g (L0 remainder, nP with t^0 r0 by F3, nR0, far_out with its cross terms
# by F2, gB, the bound). The arithmetic of every stage is kt_cert_v1_1's except F1, F2, F3.
LAM_T = 0.45          # the Chernoff lambda of tailX, tailB and ann (free choice, exact binary64)


def mark(kind, label):
    """a stage line with the CPU time so far (locates the cost of each part)."""
    out('STAGE-CPU N=%d %s: %s done at cpu %.1f s' % (NN, kind, label, cpu()))


def eye3():
    return arb_mat(3, 3, [1 if i == j else 0 for i in range(3) for j in range(3)])


def residual_P(ex, t):
    """F3: P = r0 + t r1 + t^2 r2 + t^3 r3 for every kind (the free binary64 m0 leave r0 != 0, and (C1) needs the residual of the
    chosen m_g in full)."""
    return padd(ex['r0'], pscale(ex['r1'], t), pscale(ex['r2'], t * t), pscale(ex['r3'], t ** 3))


def stage_c(kind, J):
    """engine A's derivative part: D4 (the order-4 majorant of L1 F on the near region), its conditional expectation given sigma, and
    nD = (t^4/24) detf (n2 E[E_t[D4|s]^2])^{1/2}. Returns {nD, deg2, tot, nterms, cpu}."""
    t = arb(1) / J
    c0 = cpu()
    hL = {k: hk(k, [(v, a_e) for v in XD], bondsL, cf_rad) for k in range(1, 5)}
    pis, byord, TOT, budgets, qold = fix_pis_c(kind, t, hL)              # kt_cert_v1_8: majfix_v1_1's capped pis
    D4 = Dbar(4, hL, pis)
    ex4 = D4.exponents()
    assert ex4[:, 3:6].sum() == 0
    deg2 = int(ex4[:, 6:].sum(axis=1).max())
    qdeg = int(ex4[:, 9:].sum(axis=1).max())
    tot = int(ex4.sum(axis=1).max())
    okd = tot <= TOT and deg2 <= TOT and qdeg <= max(qold, 2)
    out('C-DEG N=%d %s: D4 deg2 %d, total %d (budget %d), Q degree %d (today\'s %d) -> %s' % (NN, kind, deg2, tot, TOT, qdeg, qold,
                                                                                        'PASS' if okd else 'FAIL (STOP)'))
    if not okd:
        raise ValueError('C-DEG: D4 above its budget')
    mark(kind, 'D4 (%d terms)' % len(D4.codes))
    Amat = eye3() + tri_laplacian()
    Ainv = Amat.inv()
    W2 = arb_mat(3, 6)
    for r in range(3):
        W2[r, r] = 1
    for p_, (r, s) in enumerate(PAIRS):
        W2[r, 3 + p_] = 1
        W2[s, 3 + p_] = -1
    At = Amat - eye3() * (2 * c_e * t)
    assert surely_pd(At, 'A - 2 c_e t I')
    Ati = At.inv()
    detf = ((Amat.det() / At.det()).log() * nn / 2).exp()
    Delta = Ati - Ainv
    cmT = ae.CondMomA(Ati, Ati, W2, nn, deg2, groups=[0, 0, 0, 1, 1, 1], caps={1: max(qdeg, 1)})
    mark(kind, 'CondMomA (Dc %d)' % deg2)
    cgT = ae.CondGA(cmT, tot)
    ED = cgT.out.to_dict(cgT.condE(D4.to_dict()))
    mark(kind, 'conditional expectation of D4 (%d terms)' % len(ED))
    ext = arb_mat(6, 6)
    for i in range(3):
        for j in range(3):
            ext[i, j] = Delta[i, j]
    G2, n2 = tilted_cov_a(LD, BD, [c_m * t] * 6, extra=ext)
    w2 = ae.WishartA(sub_mat(G2, [0, 1, 2]), nn, 2 * max(sum(e) for e in ED))
    nD = (t ** 4 / 24) * detf * nsqrt(n2 * w2.E2(ED, ED))
    mark(kind, 'nD')
    nDk = {}                                                            # kt_cert_v1_8: nD's parts per formal-t order (M4's law)
    for k, pk in sorted(byord.items()):
        D4k = Dbar(4, hL, pk)
        if len(D4k.codes) == 0:
            nDk[k] = arb(0)
            continue
        EDk = cgT.out.to_dict(cgT.condE(D4k.to_dict()))
        nDk[k] = (t ** 4 / 24) * detf * nsqrt(n2 * w2.E2(EDk, EDk))
    msum = sum(nDk.values(), arb(0))
    okk = not bool(msum < nD)
    out('C-NDK N=%d %s: sum over the formal-t orders of nD_k %s, not certainly below nD %s (the triangle inequality) -> %s' % (
        NN, kind, bstr(msum), bstr(nD), 'PASS' if okk else 'FAIL'))
    if not okk:
        NDK_FAILS.append('C-NDK')
    mark(kind, 'nD per formal-t order (%d orders)' % len(nDk))
    return dict(nD=nD, deg2=deg2, tot=tot, nterms=len(D4.codes), cpu=cpu() - c0, nDk=nDk, budgets=budgets, TOT=TOT)


NDK_FAILS = []                                  # kt_cert_v1_8: C-NDK, merged into the item's verdict by main()


def tail_poly(T3, t):
    """the explicit series T3 at t as a polynomial in the ten joint forms, with its degree and its Q degree."""
    T10 = to10(padd(*[pscale(T3.c[k], t ** k) for k in range(KX + 1)]), NVX)
    return T10, max(sum(e) for e in T10), max(sum(e[6:]) for e in T10)


def ann_poly(kind, t):
    """pi0'' (the annulus majorant of L1 F) in the ten joint forms, with its degree and its Q degree. kt_cert_v1_8: majfix_v1_1's g_source at
    a_pp, capped at today's pi0'' degree with radii a_pp on sigma'' (F-2, F-2b)."""
    pi0pp = fix_pi0pp(kind, t)
    P0d = to10(pi0pp.to_dict(), NV12)
    return P0d, max(sum(e) for e in P0d), max(sum(e[6:]) for e in P0d)


def kappa_B():
    """kappa = 2 (1 - cos delta) - a^2/(4 (1 - a)), a = max(a_m, a_e): a bad bond r inside Omega'' has Q_rr'' > J kappa (vacrig11f l.350)."""
    amax = max(a_m, a_e)
    kap = 2 * (1 - DELTA.cos()) - arb(amax) ** 2 / (4 * (1 - arb(amax)))
    assert kap > 0
    return kap


def tail_orders(T3, t):
    """kt_cert_v1_8: the orders T_k of the explicit series (unscaled), each as a polynomial in the ten joint forms with its degree and Q
    degree; tail_term's Minkowski-per-order form is sum_k t^k E[T_k^2]^{1/2}."""
    res = []
    for k in range(KX + 1):
        Tk = to10(T3.c[k], NVX)
        res.append((Tk, max([sum(e) for e in Tk] + [0]), max([sum(e[6:]) for e in Tk] + [0])))
    return res


def tail_term(fam, idx, kind, J, poly, orders=None):
    """kt_cert_v1_8: returns (term, termm), termm the Minkowski-per-order term e^{-lam J c} N (sum_k t^k E[T_k^2]^{1/2})^2 on the same
    table when orders is given (families X and B), else None. The rest is kt_cert_v1_7's:"""
    return _tail_term(fam, idx, kind, J, poly, orders)


def _tail_term(fam, idx, kind, J, poly, orders):
    """one Chernoff table of the inner tails in balls, e^{-lam J c} N E[F^2] under the tilt (N E[.] relative to the untilted joint Gaussian):
    fam 'X': F = T (the explicit series), tilt lam X''_idx on the base rates (c_m t on the six outer vertices), c = a_e (as kt_cert_v1_1);
    fam 'B' (F1): F = T, tilt lam Q_rr'' = lam |x_r - x''_r|^2, r = idx (the extra form lam (e_r - e_{6+r})(e_r - e_{6+r})^T),
        on the base rates, c = kappa: on the bad set B_r of bond r inside Omega'', Q_rr'' > J kappa, so E[T^2 1_{B_r}] <= e^{-lam J kappa} N_r E_r[T^2];
    fam 'A': F = pi0'', tilt lam X''_idx on the annulus rates (c_m t outer, 2 c_pp t inner), c = a_e (as kt_cert_v1_1).
    Every tilt passes surely_pd (C-TILT (b)); the item stops otherwise."""
    t = arb(1) / J
    P, dP, qP = poly
    if orders is not None:                                              # kt_cert_v1_8: the table also covers every order T_k
        dP = max([dP] + [d for _, d, _ in orders])
        qP = max([qP] + [q for _, _, q in orders])
    lam = arb(LAM_T)
    rates = [c_m * t] * 6 + ([2 * c_pp * t] * 3 if fam == 'A' else [arb(0)] * 3)
    extra = None
    if fam in ('X', 'A'):
        rates[6 + idx] = rates[6 + idx] + lam
        cexp = arb(a_e)
    else:
        extra = arb_mat(9, 9)
        extra[idx, idx] = lam
        extra[6 + idx, 6 + idx] = lam
        extra[idx, 6 + idx] = -lam
        extra[6 + idx, idx] = -lam
        cexp = kappa_B()
    am9, N9, _, Gam = joint_moments_a(rates, 2 * dP, max(2 * qP, 1), extra=extra, label='tilt %s%d' % (fam, idx))
    if am9 is None:
        raise ValueError('the Chernoff tilt %s%d is not certainly positive definite (kind %s)' % (fam, idx, kind))
    term = (-lam * J * cexp).exp() * N9 * am9.E2(P, P)
    termm = None
    if orders is not None:                                              # kt_cert_v1_8: Minkowski per order on the same table
        s = sum((t ** k * nsqrt(am9.E2(Pk, Pk)) for k, (Pk, _, _) in enumerate(orders) if Pk), arb(0))
        termm = (-lam * J * cexp).exp() * N9 * s * s
    mark(kind, 'tail table %s%d (degree %d; %d rank-deficient subsets as exact zeros)' % (fam, idx, 2 * dP, am9.zeroed))
    c_sing(am9, Gam, max(2 * qP, 1), '%s %s%d' % (kind, fam, idx))
    if not PLANTED[0]:
        plant_sing(Gam, max(2 * qP, 1))
        PLANTED[0] = True
    return term, termm


def stage_g(kind, J, ex, cres, tails, gBb):
    """engine A's last stage: the L0 remainder, nP (F3), nR0, the tails from their nine tables, far_out (F2), gB, and
    bound = (near^2 + far_out)^{1/2} + gB >= ||K^{1/2} |f_kind| ||/(lambda_h main_D^{1/2}) (ADD2 sect. 6). Returns (bound, parts)."""
    t = arb(1) / J
    G, m = ex['G'], ex['m']
    tm = {}
    c0 = cpu()
    P = residual_P(ex, t)
    G1, n1 = tilted_cov_a(LD, BD, [c_m * t] * 6)
    R0, h0 = l0_remainder(G, m, t)
    mark(kind, 'L0 remainder (%d terms)' % len(R0.codes))
    R0g = ae.sigma_to_g({e[:6]: c for e, c in R0.to_dict().items()})
    Pg = ae.sigma_to_g(P)
    rkg = [ae.sigma_to_g(ex['r%d' % k]) for k in range(4)]                  # kt_cert_v1_8: the orders of P, for M_k
    w1 = ae.WishartA(sub_mat(G1, [0, 1, 2]), nn, 2 * max([sum(e) for e in Pg] + [sum(e) for e in R0g] + [sum(e) for q in rkg for e in q]))
    nP = nsqrt(n1 * w1.E2(Pg, Pg))
    nPk = [t ** k * nsqrt(n1 * w1.E2(q, q)) if q else arb(0) for k, q in enumerate(rkg)]
    nR0 = nsqrt(n1 * w1.E2(R0g, R0g))
    tm['wish'] = cpu() - c0
    mark(kind, 'nP, its orders M_0..M_3, nR0')
    c0 = cpu()
    tailX, tailB, ann = (nsqrt(tails[(f, 0)] + tails[(f, 1)] + tails[(f, 2)]) for f in ('X', 'B', 'A'))
    if not all((f, i) in TAILSM for f in ('X', 'B') for i in range(3)):  # kt_cert_v1_8: the Minkowski bases of the tails
        raise ValueError('the Minkowski-per-order tail terms are missing (TAILM rows of kt_cert_v1_8 tail pieces, or in-line)')
    TXm, TBm = (nsqrt(TAILSM[(f, 0)] + TAILSM[(f, 1)] + TAILSM[(f, 2)]) for f in ('X', 'B'))
    near = nP + cres['nD'] + nR0 + tailX + tailB + ann
    gB = supF_a(kind, J) * gBb                                               # kt_cert_v1_9: gBb certified (gbb_cert)
    far_out, fl = far_cert(kind, G, m, t, J, CI['far'])                      # kt_cert_v1_9: FAR_CRUDE_v1's X300, R = 1
    tm['far'] = cpu() - c0
    mark(kind, 'far (FAR_CRUDE_v1 items with the cross terms)')
    bound = (near * near + far_out).sqrt() + gB
    parts = dict(nP=nP, nD=cres['nD'], nR0=nR0, tailX=tailX, tailB=tailB, ann=ann, near=near, gB=gB, far=far_out, fl=fl, deg2=cres['deg2'],
                 tot=cres['tot'], nterms=cres['nterms'], tm=tm, nPk=nPk, TXm=TXm, TBm=TBm, nDk=cres['nDk'])        # kt_cert_v1_8: nDk
    return bound, parts


def a_engine(J, ex, kind='a'):
    """bound on ||K^{1/2} f_a||/main_D^{1/2}, f_a = E0 (xi_a+ p0 - sum_g m_g(t) p_g), in balls (kt_c_v2_3 l.1085-1128), with F3 (t^0 r0 in P)
    and F2 (far_out with its cross terms). kt_cert_v1_7: kind am (xi_a- = (xi_TM - xi_MB)/2, basis (e2,)) runs the same engine; its
    majorants are a's (they use |coefficients|), and its far parts take am's source factors (src_factors, pk15's sgn)."""
    t = arb(1) / J
    G, m = ex['G'], ex['m']
    tm = {}
    c0 = cpu()
    P = residual_P(ex, t)
    G1, n1 = tilted_cov_a(LD, BD, [c_m * t] * 6)
    R0, h0 = l0_remainder(G, m, t)
    pis_a = fix_pis_a(t)                                                # kt_cert_v1_8: majfix_v1_1, untraded
    Da = Dbar(4, h0, pis_a)
    Ra = Da.scale(t ** 4 / 24).add(R0)
    exa = Ra.exponents()
    assert exa[:, 6:].sum() == 0
    tm['D4'] = cpu() - c0
    mark(kind, 'Da (%d terms)' % len(Da.codes))
    c0 = cpu()
    Rag = ae.sigma_to_g({e[:6]: c for e, c in Ra.to_dict().items()})
    Pg = ae.sigma_to_g(P)
    rkg = [ae.sigma_to_g(ex['r%d' % k]) for k in range(4)]                  # kt_cert_v1_8: the orders of P, for M_k
    w1 = ae.WishartA(sub_mat(G1, [0, 1, 2]), nn, 2 * max([sum(e) for e in Pg] + [sum(e) for e in Rag] + [sum(e) for q in rkg for e in q]))
    nP = nsqrt(n1 * w1.E2(Pg, Pg))
    nPk = [t ** k * nsqrt(n1 * w1.E2(q, q)) if q else arb(0) for k, q in enumerate(rkg)]
    nR = nsqrt(n1 * w1.E2(Rag, Rag))
    tm['wish'] = cpu() - c0
    mark(kind, 'nP, nR')
    c0 = cpu()
    far_out, fl = far_cert(kind, G, m, t, J, CI['far'])                     # kt_cert_v1_9: FAR_CRUDE_v1's X300 (kinds a, am: all on ED)
    tm['far'] = cpu() - c0
    mark(kind, 'far (FAR_CRUDE_v1 items with the cross terms)')
    near = nP + nR
    bound = (near * near + far_out).sqrt()
    return bound, dict(nP=nP, nR=nR, near=near, far=far_out, fl=fl, nterms=len(Da.codes), deg=int(exa.sum(axis=1).max()), tm=tm, nPk=nPk)


# ====================================================================================== part 6: values, checks, items, main
def engine_value(kind, J, bnd):
    """R_b = bound/(lambda~_0 Z_b^{1/2}) (b = e1, e3); A_h, A_a, and the hook's R^xi_b = bound/Z_b^{1/2}, in balls. kt_cert_v1_9: lambda~_0 =
    (1 - eps_r) mhat with eps_r M2B_KV_v1's certified upper end at 300 (law_v1), and Z_b the S9 record's certified lower end (z_cert; G,0,0
    for t, h, a, am, G,1,1 for e1, h1, G,3,3 for e3, h3), both from certin (CI). Returns (value, eps_r ball, Z ball)."""
    if J != J_CERT:
        raise ValueError('engine_value: the certified eps_r and Z are used at J = 300 only')
    eps = farb(CI['eps'])
    mh = 1 + arb(R3['m1']) / J + arb(R3['m2']) / J ** 2 + arb(R3['m3']) / J ** 3
    lt0 = (1 - eps) * mh
    Z = farb(CI['Z'])
    if not (Z > 0 and lt0 > 0):
        raise ValueError('engine_value: Z_b or lambda~_0 is not certainly positive')
    val = bnd / (lt0 * Z.sqrt()) if kind in ('e1', 'e3') else bnd / Z.sqrt()
    return val, eps, Z


def bstr(x):
    """a ball as 'mid +- rad (rel r)'."""
    mid, rad = float(x.mid()), float(x.rad())
    return '%.9e +- %.1e (rel %.1e)' % (mid, rad, rad / abs(mid) if mid != 0 else float('inf'))


def dec_out(x):
    """kt_cert_v1_7: [lo, hi] as 17-significant-digit decimals with lo <= every point of the ball x <= hi, each checked in arb."""
    lo, hi = x.lower(), x.upper()
    fh = up_float(x)
    sh = '%.16e' % fh
    while not (arb(sh) >= hi):
        fh = math.nextafter(fh, math.inf)
        sh = '%.16e' % fh
    fl = float(lo)
    if not (arb(fl) <= lo):
        fl = math.nextafter(fl, -math.inf)
    sl = '%.16e' % fl
    while not (arb(sl) <= lo):
        fl = math.nextafter(fl, -math.inf)
        sl = '%.16e' % fl
    return sl, sh


def law_bases(parts, fails, fires):
    """kt_cert_v1_8 (DESIGN_KT_CERT_v1_8 sect. 1 item 3): the per-order nP norms M_0..M_3 with C-NPK and PLANT-NPK, the Minkowski tail
    bases TXm and TBm (kinds t, e1, e3), and the LAWBASE line of rounded-up 17-digit decimals that m4_asm_v1 reads."""
    nPk = parts['nPk']
    msum = nPk[0] + nPk[1] + nPk[2] + nPk[3]
    okn = not bool(msum < parts['nP'])
    out('C-NPK N=%d %s: M_0 + M_1 + M_2 + M_3 = %s, not certainly below the joint nP %s (the triangle inequality) -> %s' % (
        NN, KIND, bstr(msum), bstr(parts['nP']), 'PASS' if okn else 'FAIL'))
    if not okn:
        fails.append('C-NPK')
    big = max(range(4), key=lambda k: float(nPk[k].upper()))
    bad = msum - nPk[big] + nPk[big] * arb(10) ** -3                       # the largest order cut to 1/1000
    pl = bool(bad < parts['nP'])
    out('PLANT-NPK N=%d %s: M_%d cut to 1/1000 makes the sum certainly below nP: %s -> %s' % (NN, KIND, big, pl, 'FIRES' if pl else
                                                                                               'DOES NOT FIRE'))
    if not pl:
        fires.append('PLANT-NPK')
    vals = [('M%d' % k, nPk[k]) for k in range(4)]
    if KIND in ('a', 'am'):
        vals.append(('nR', parts['nR']))
    else:
        vals += [('nD', parts['nD'])] + [('nD_k%d' % k, v) for k, v in sorted(parts['nDk'].items())] + \
                [('nR0', parts['nR0']), ('TXm', parts['TXm']), ('TBm', parts['TBm']), ('ann', parts['ann'])]   # kt_cert_v1_8: nD_k
        out('TAILBASE N=%d %s: TXm %s (joint tailX %s), TBm %s (joint tailB %s)' % (NN, KIND, bstr(parts['TXm']), bstr(parts['tailX']),
                                                                                    bstr(parts['TBm']), bstr(parts['tailB'])))
    out('LAWBASE N=%d %s: %s' % (NN, KIND, ' '.join('%s %s' % (k, dec_out(v)[1]) for k, v in vals)))


def dec_up(x):
    """a 10-digit decimal >= every point of the ball x (checked in arb; F5's upward rounding, done at the source)."""
    s = '%.9e' % (up_float(x) * (1 + 2e-9))
    assert arb(s) >= x
    return s


def v23_line(kind):
    """the float engine's printed engine line for this item's kind and N (kt_cert_v1_6): kt_c_v2_3z's print on z9sym (REFS, in own out/) for
    the production items, kt_c_v2_3's (pk01's frozen outputs, SRCFILES) for the smoke. C-REFHEAD: the record's first line names that
    engine's sha256 and this kind and N, and its only VERDICT line is VERDICT VALID. Returns (name, line, C-REFHEAD outcome)."""
    if SMOKE:
        name, base, head = 'out_kt_c_v2_3_%sn%d.out' % (kind, NN), SRC, 'kt_c_v2_3 sha256 %s ITEM=%sn%d ' % (V23_SHA, kind, NN)
    elif kind in ('t', 'am'):                                           # kt_cert_v1_7: pk15's kt_c_t_v1_1 prints (TREFS)
        name, base, head = 'out_kt_c_t_v1_1_%sn%d.out' % (kind, NN), TREFDIR, 'kt_c_t_v1_1 sha256 %s ITEM=%sn%d ' % (VT_SHA, kind, NN)
    else:
        name, base, head = 'out_kt_c_v2_3z_%sn%d.out' % (kind, NN), REFDIR, 'kt_c_v2_3z sha256 %s ITEM=%sn%d ' % (V23Z_SHA, kind, NN)
    txt = open(os.path.join(base, name)).read().splitlines()
    okh = bool(txt) and txt[0].startswith(head) and [ln for ln in txt if ln.startswith('VERDICT')] == ['VERDICT VALID']
    pat = r'AENGINE N=%d J=300 %s: ' % (NN, kind) if kind in ('a', 'am') else r'ENGINE N=%d J=300 %s: ' % (NN, kind)
    lines = [ln for ln in txt if ln.startswith(pat)]
    assert len(lines) == 1, (name, len(lines))
    return name, lines[0], okh


def printed(line, key):
    mt = re.search(r'\b%s ([0-9.]+e[+-][0-9]+)' % re.escape(key), line)
    return None if mt is None else mt.group(1)


def fix_ref_lines():
    """kt_cert_v1_8, C-REP-FIX: the twin's record for this kind and N (kt_c_t_trade_v1_3, mode prop): its J = 300 JTERMS2 line and, for
    t, e1, e3, h, its NDK line. The record's first line must name the twin's full sha256 and the item, its VERDICT lines read exactly
    ['VERDICT VALID'] (T48)."""
    item = ('j' if KIND in ('t', 'am', 'e1', 'e3') else 'r') + KIND + 'n%d' % NN
    name = 'out_kt_c_t_trade_v1_3_%s.out' % item
    with open(os.path.join(REFDIR, name)) as fh:
        txt = fh.read().splitlines()
    okh = bool(txt) and txt[0].startswith('kt_c_t_trade_v1_3 sha256 %s ITEM=%s MODES=prop ' % (FIXREF_SHA, item)) and \
        [ln for ln in txt if ln.startswith('VERDICT')] == ['VERDICT VALID']
    jt = [ln for ln in txt if ln.startswith('JTERMS2 N=%d J=300 %s: ' % (NN, KIND))]
    nk = [ln for ln in txt if ln.startswith('NDK N=%d J=300 %s: ' % (NN, KIND))]
    if not okh or len(jt) != 1 or (KIND not in ('a', 'am') and len(nk) != 1):
        raise ValueError('C-REP-FIX: twin record %s refused (header/verdict %s, %d JTERMS2 lines, %d NDK lines)' % (name, okh, len(jt), len(nk)))
    return name, jt[0], (nk[0] if nk else None)


def rel_ok(cert, s, tol):
    v = float(cert.mid())
    return abs(v / float(s) - 1) <= tol, v


def rep_fix_c(cres, fails):
    """C-REP-FIX of piece c: nD against the twin's J = 300 nD (1e-9 relative) and each nD_k against its NDK line (printed %.6e: 1e-6)."""
    name, jt, nk = fix_ref_lines()
    res, ok = [], True
    good, v = rel_ok(cres['nD'], printed(jt, 'nD'), 1e-9)
    ok &= good
    res.append('nD %.12e vs %s%s' % (v, printed(jt, 'nD'), '' if good else ' (OFF)'))
    ref = dict((int(k), s) for k, s in re.findall(r'\bk([0-9]+) ([0-9.]+e[+-][0-9]+)', nk.split(':', 1)[1].split(';')[0]))
    if set(ref) != set(cres['nDk']):
        ok = False
        res.append('orders %s vs %s (OFF)' % (sorted(cres['nDk']), sorted(ref)))
    else:
        for k in sorted(ref):
            good, v = (True, 0.0) if float(ref[k]) == 0.0 and cres['nDk'][k].contains(0) else rel_ok(cres['nDk'][k], ref[k], 1e-6)
            ok &= good
            res.append('nD_k%d %.6e vs %s%s' % (k, v, ref[k], '' if good else ' (OFF)'))
    out('C-REP-FIX N=%d %s c against %s: %s -> %s' % (NN, KIND, name, '; '.join(res), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-REP-FIX c')


def rep_fix_g(kind, parts, fails):
    """C-REP-FIX of piece g: nP, nD, nR0 (am, a: nP, nR) against the twin's J = 300 JTERMS2 line to 1e-9 relative; tailX and ann (printed
    %.6e) to 1e-6; tailB is not compared (the twin's is the chi3 form, this engine's kt_cert's F1 per-bond form)."""
    name, jt, _nk = fix_ref_lines()
    keys = (('nP', 1e-9), ('nR', 1e-9)) if kind in ('a', 'am') else (('nP', 1e-9), ('nD', 1e-9), ('nR0', 1e-9), ('tailX', 1e-6), ('ann', 1e-6))
    res, ok = [], True
    for k, tol in keys:
        s = printed(jt, k)
        if s is None:
            ok = False
            res.append('%s missing (OFF)' % k)
            continue
        good, v = rel_ok(parts[k], s, tol)
        ok &= good
        res.append('%s %.12e vs %s%s' % (k, v, s, '' if good else ' (OFF)'))
    out('C-REP-FIX N=%d %s g against %s: %s -> %s' % (NN, kind, name, '; '.join(res), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-REP-FIX g')


def rep_check(kind, bnd, parts, tag, fails, scale_nP=1.0, quiet=False):
    """C-REP / C-HOOK0: the ball midpoints against kt_c_v2_3's printed values. Each part printed with d digits after the point to half a unit
    of its last printed digit (plus 1e-9 relative); tailB is not compared (F1 changed its form; printed beside v2_3's). The bound to 1e-6
    relative against v2_3's bound with v2_3's far and tailB replaced by this engine's (F2, F1; S1 of the REVIEW_kt_cert_v1_3):
    near_v23 = ((B - gB)^2 - far)^{1/2}, B_ref = ((near_v23 - tailB_v23 + tailB_new)^2 + far_new)^{1/2} + gB_new, from v2_3's printed B, gB,
    far, tailB (their rounding moves B_ref by up to about 5.5e-7 relative, at e3n4, against the 1e-6 gate). Returns
    True if every key agrees."""
    name, line, okh = v23_line(kind)
    keys = ['nP', 'nR'] if kind in ('a', 'am') else ['nP', 'nD', 'nR0', 'tailX', 'ann']
    vals = dict(parts)
    vals['nP'] = parts['nP'] * scale_nP
    res, ok = ['C-REFHEAD %s' % ('PASS' if okh else 'FAIL')], okh
    sb, sf = float(printed(line, 'bound')), float(printed(line, 'far'))
    sg = 0.0 if kind in ('a', 'am') else float(printed(line, 'gB'))
    gnew = 0.0 if kind in ('a', 'am') else float(parts['gB'].mid())
    tb_old = 0.0 if kind in ('a', 'am') else float(printed(line, 'tailB'))
    tb_new = 0.0 if kind in ('a', 'am') else float(parts['tailB'].mid())
    near_v23 = math.sqrt((sb - sg) ** 2 - sf)
    bref = math.sqrt((near_v23 - tb_old + tb_new) ** 2 + float(parts['far'].mid())) + gnew
    devb = abs(float(bnd.mid()) / bref - 1)
    okb = devb <= 1e-6
    ok &= okb
    res.append('bound %.9e vs %.9e (v2_3 %s with far %s -> %.3e and tailB %s -> %.3e; rel %.1e)' % (
        float(bnd.mid()), bref, printed(line, 'bound'), printed(line, 'far'), float(parts['far'].mid()),
        '0' if kind in ('a', 'am') else printed(line, 'tailB'), tb_new, devb))
    for k in keys:
        s = printed(line, k)
        v = float(vals[k].mid())
        d = len(s.split('e')[0].split('.')[1]) if '.' in s.split('e')[0] else 0
        tol = 0.5 * 10.0 ** (int(s.split('e')[1]) - d) + 1e-9 * abs(float(s))
        good = abs(v - float(s)) <= tol
        ok &= good
        res.append('%s %.4e vs %s%s' % (k, v, s, '' if good else ' (OFF)'))
    if kind not in ('a', 'am'):
        res.append('tailB %.4e (F1 form; v2_3 printed %s, not compared)' % (fup(parts['tailB']), printed(line, 'tailB')))
    if not quiet:
        out('%s N=%d %s against %s: %s -> %s' % (tag, NN, kind, name, '; '.join(res), 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('%s %s' % (tag, kind))
    return ok


def replay_check(bnd, parts, val, fails):
    """C-REPLAY (kt_cert_v1_6, smoke only): this run repeats kt_cert_v1_5's g.e1n4 on the same pinned inputs. That record (PREV) must name
    kt_cert_v1_5's sha256 and ITEM=g.e1n4 on its first line and have VERDICT VALID as its only VERDICT line. It prints balls 'mid +- rad'
    (mid with 10 digits, rad with 2) for the bound, nP, nD, nR0 and far (ENGINE line) and the value (VALUE line): each, widened by half a unit
    of its last printed digits, must overlap this run's ball. It prints tailX, tailB, ann and gB as upper values with 4 digits: each must agree
    with this run's to half a unit of its last digit (plus 1e-9 relative). Also prints the largest relative difference of the midpoints."""
    name = 'out_kt_cert_v1_5_g.e1n4.out'
    txt = open(os.path.join(OWN, name)).read().splitlines()
    okh = (bool(txt) and txt[0].startswith('kt_cert_v1_5 sha256 %s ITEM=g.e1n4 ' % V15_SHA) and
           [ln for ln in txt if ln.startswith('VERDICT')] == ['VERDICT VALID'])
    eng = [ln for ln in txt if ln.startswith('ENGINE N=4 J=300 e1: ')]
    vln = [ln for ln in txt if ln.startswith('VALUE N=4 J=300 e1: ')]
    assert len(eng) == 1 and len(vln) == 1, (len(eng), len(vln))

    def half_unit(s, digits):
        return 0.5 * 10.0 ** (int(s.split('e')[1]) - digits)

    res, ok, worst = ['C-REFHEAD %s' % ('PASS' if okh else 'FAIL')], okh, 0.0
    balls = [(k, eng[0], r'\b%s ' % k, x) for k, x in (('bound', bnd), ('nP', parts['nP']), ('nD', parts['nD']), ('nR0', parts['nR0']),
                                                       ('far', parts['far']))] + [('value', vln[0], r'\(ball ', val)]
    for k, line, lead, x in balls:
        mt = re.search(lead + r'([0-9.]+e[+-][0-9]+) \+- ([0-9.]+e[+-][0-9]+)', line)
        ms, rs = mt.group(1), mt.group(2)
        old = arb(ms) + arb(0, float(rs) + half_unit(rs, 1) + half_unit(ms, 9))
        good = old.overlaps(x)
        ok &= good
        worst = max(worst, abs(float(x.mid()) / float(ms) - 1))
        res.append('%s %s vs %s +- %s%s' % (k, bstr(x), ms, rs, '' if good else ' (NO OVERLAP)'))
    for k in ('tailX', 'tailB', 'ann', 'gB'):
        s = printed(eng[0], k)
        v = fup(parts[k])
        good = abs(v - float(s)) <= half_unit(s, 3) + 1e-9 * abs(float(s))
        ok &= good
        res.append('%s %.3e vs %s%s' % (k, v, s, '' if good else ' (OFF)'))
    out('C-REPLAY N=%d e1 against %s (kt_cert_v1_5 on the same inputs): %s; largest relative midpoint difference %.1e -> %s' % (
        NN, name, '; '.join(res), worst, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-REPLAY')


def rad_check(bnd, parts, fails):
    worst = 0.0
    for k, x in [('bound', bnd)] + [(k, parts[k]) for k in ('nP', 'nD', 'nR0', 'nR') if k in parts]:
        mid = abs(float(x.mid()))
        if mid > 0:
            worst = max(worst, float(x.rad()) / mid)
    ok = worst <= 1e-12
    out('C-RAD N=%d: worst relative radius over the bound and the main parts %.2e -> %s' % (NN, worst, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-RAD')


def series_T3(kind):
    """the explicit series T3 of explicit_part (before the conditional expectation), recomputed where the tails need it; None for kinds a, am."""
    if kind in ('a', 'am'):
        return None
    HL = zero()
    for r in range(3):
        HL = HL + meas(XD[r])
    for p, (r, s) in enumerate(PAIRS):
        HL = HL + anh(XD[r], XD[s], TRI[p])
    for r in range(3):
        HL = HL + anh(XS[r], XD[r], 1)
    HL = HL + anh(XS[0], XS[1], 1) + anh(XS[1], XS[2], 1)
    EL = HL.exp()
    xiD = xis(XD, QD)
    xih = xi_pair(XS[ROWX], XD[ROWX], QT if kind == 't' else QH)       # kt_cert_v1_7: as explicit_part
    b = STATE_OF[kind]
    pD = vac_poly(xiD) if b == 'psi' else state_poly(xiD, {'e1': 1, 'e3': 3}[b])
    return EL * xih * pD if kind in HOOK else EL * pD


# ---------------------------------------------------------------------------- hand-offs between the pieces of an item
# A piece's hand-off: hand_kt_cert_v1_6_<piece>.<suffix>.txt in the own folder, created once (exclusive create), under 2 MB: a HEAD line (this
# script's sha256, the piece, kind, N, precision), the rows, and an END line with the sha256 of the body. The producing piece prints the file's
# sha256 in its record (out_kt_cert_v1_6_<piece>.<suffix>.out, line HANDOFF). A reading piece takes the sha256 from that record, whose VERDICT
# line must read VALID, and checks (1) the file's sha256 against it, (2) the body checksum, (3) the header. PLANT-HANDOFF (g pieces): three
# tampered copies, in memory, each caught by its own check. Balls are written by arb's str with the radius (80 digits), whose parse contains
# the ball; the m_g as repr floats (exact).
HANDOFF_MAX = 2 * 1024 * 1024


PRODUCERS = {'kt_cert_v1_7': '765ed898af05c3a59c6f5bc87f5fd92cbbfaf05dc0dd54c545b5bf7f032ba95a', 'kt_cert_v1_6': '7e48fd63d42b1c87448432f8c8403dce517c7bb8469834f9103ccfe4bed01982'}   # kt_cert_v1_8: the x producers


def producer(piece):
    """kt_cert_v1_8: (name, full sha256) of the run whose hand-off of this piece is read: x from kt_cert_v1_7 (kinds t, am) or kt_cert_v1_6
    (kinds e1, e3, h, a; z9sym production), its path has no trade. kt_cert_v1_9: c and every tail piece from kt_cert_v1_8 (V18_SHA, its
    certified F-2 production); cN2 and g from this file."""
    if piece == 'x':                                                  # kt_cert_v1_8: only x is read (no trade on its path)
        name = 'kt_cert_v1_7' if KIND in ('t', 'am') else 'kt_cert_v1_6'
        return name, PRODUCERS[name]
    if piece == 'c' or piece[:1] == 't':                              # kt_cert_v1_9: c, tX, tB, tA, tX0..tA2
        return 'kt_cert_v1_8', V18_SHA
    return 'kt_cert_v1_9', SELF_SHA


def handoff_path(piece):
    base = V19DIR if producer(piece)[0] == 'kt_cert_v1_9' else OWN       # kt_cert_v1_9: this file's pieces in V19DIR (= OWN)
    return os.path.join(base, 'hand_%s_%s.%s.txt' % (producer(piece)[0], piece, SUFFIX))


def record_path(piece):
    base = V19DIR if producer(piece)[0] == 'kt_cert_v1_9' else OWN
    return os.path.join(base, 'out_%s_%s.%s.out' % (producer(piece)[0], piece, SUFFIX))


def write_handoff(piece, rows):
    path = handoff_path(piece)
    if producer(piece)[0] != 'kt_cert_v1_9':
        raise ValueError('kt_cert_v1_9 writes no %s hand-off (its producer is %s)' % (piece, producer(piece)[0]))
    if not (os.path.dirname(os.path.realpath(path)) == os.path.realpath(V19DIR) and not os.path.exists(path)):
        raise ValueError('hand-off path %s is outside %s or exists' % (path, V19DIR))
    body = '\n'.join(['HEAD kt_cert_v1_9 %s piece %s kind %s N %d prec %d' % (SELF_SHA, piece, KIND, NN, ctx.prec)] + rows) + '\n'
    data = (body + 'END %s\n' % hashlib.sha256(body.encode()).hexdigest()).encode()
    assert len(data) < HANDOFF_MAX, len(data)
    with open(path, 'xb') as fh:
        fh.write(data)
    sh = hashlib.sha256(data).hexdigest()
    out('HANDOFF N=%d %s %s: %s sha256 %s (%d bytes, %d rows; cpu %.1f s)' % (NN, KIND, piece, os.path.basename(path), sh, len(data), len(rows),
                                                                             cpu()))
    return sh


def verify_handoff_bytes(data, want, piece):
    """the three checks; returns the body rows after the HEAD line, raises ValueError naming the first check that fails."""
    if hashlib.sha256(data).hexdigest() != want:
        raise ValueError('sha256 differs from the record')
    txt = data.decode()
    body, endline = txt.rsplit('END ', 1)
    if hashlib.sha256(body.encode()).hexdigest() != endline.strip():
        raise ValueError('body checksum')
    rows = body.splitlines()
    head = rows[0].split()
    pname, psha = producer(piece)                                        # kt_cert_v1_8: the piece's producer, not this file
    if not (len(head) == 11 and head[0] == 'HEAD' and head[1] == pname and head[2] == psha and head[4] == piece and
            head[6] == KIND and head[8] == str(NN) and head[10] == str(ctx.prec)):
        raise ValueError('header')
    return rows[1:]


def producer_sha(piece):
    """the hand-off's sha256 from its producing run's record, whose VERDICT line must read VALID."""
    with open(record_path(piece)) as fh:
        rec = fh.read().splitlines()
    hl = [ln for ln in rec if ln.startswith('HANDOFF N=%d %s %s: ' % (NN, KIND, piece))]
    vl = [ln for ln in rec if ln.startswith('VERDICT ')]
    if len(hl) != 1 or vl != ['VERDICT VALID']:
        raise ValueError('record of piece %s: %d HANDOFF lines, VERDICT lines %r' % (piece, len(hl), vl))
    return hl[0].split(' sha256 ')[1].split()[0]


def read_handoff(piece):
    want = producer_sha(piece)
    with open(handoff_path(piece), 'rb') as fh:
        data = fh.read()
    rows = verify_handoff_bytes(data, want, piece)
    out('HANDOFF-READ N=%d %s %s: %s sha256 %s equals its record (%s); body checksum and header PASS' % (
        NN, KIND, piece, os.path.basename(handoff_path(piece)), want, os.path.basename(record_path(piece))))
    return rows, data, want


def plant_handoff(piece, data, want, fires):
    """PLANT-HANDOFF: three tampered copies of the hand-off, in memory, must each fail verify_handoff_bytes at its own check:
    (a) the last digit of the first row changed, END line kept, the sha256 taken from the tampered bytes (only the body checksum can catch it);
    (b) the same change with a recomputed END line, against the record's sha256 (only the sha256 check can catch it);
    (c) the header's kind changed, END line recomputed, the sha256 taken from the tampered bytes (only the header check can catch it)."""
    txt = data.decode()
    body, endline = txt.rsplit('END ', 1)
    rows = body.splitlines()
    pos = max(p for p, ch in enumerate(rows[1]) if ch.isdigit())
    row1 = rows[1][:pos] + str((int(rows[1][pos]) + 1) % 10) + rows[1][pos + 1:]
    body_t = '\n'.join([rows[0], row1] + rows[2:]) + '\n'
    other = 'e3' if KIND != 'e3' else 'e1'
    body_h = '\n'.join([rows[0].replace(' kind %s ' % KIND, ' kind %s ' % other)] + rows[1:]) + '\n'

    def sealed(b):
        return (b + 'END %s\n' % hashlib.sha256(b.encode()).hexdigest()).encode()
    da = (body_t + 'END ' + endline).encode()
    db, dc = sealed(body_t), sealed(body_h)
    cases = (('a', da, hashlib.sha256(da).hexdigest(), 'body checksum'), ('b', db, want, 'sha256 differs from the record'),
             ('c', dc, hashlib.sha256(dc).hexdigest(), 'header'))
    res, fired = [], True
    for tag, d, w, expect in cases:
        try:
            verify_handoff_bytes(d, w, piece)
            res.append('(%s) accepted' % tag)
            fired = False
        except ValueError as e:
            res.append('(%s) rejected: %s' % (tag, e))
            fired = fired and str(e) == expect
    out('PLANT-HANDOFF N=%d %s %s: %s -> %s' % (NN, KIND, piece, '; '.join(res), 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-HANDOFF')


def plant_producer(data, fires, piece='x'):
    """kt_cert_v1_8 PLANT-PRODUCER: the x hand-off with its HEAD relabelled (END recomputed, its own sha256) must fail the header check,
    since x's producer is kt_cert_v1_7 (t, am) or kt_cert_v1_6 (e1, e3). kt_cert_v1_9: relabelled kt_cert_v1_9, and the same for c's
    hand-off (its producer is kt_cert_v1_8)."""
    txt = data.decode()
    body, _endline = txt.rsplit('END ', 1)
    rows = body.splitlines()
    pname, psha = producer(piece)
    body_r = '\n'.join([rows[0].replace(' %s %s ' % (pname, psha), ' kt_cert_v1_9 %s ' % SELF_SHA, 1)] + rows[1:]) + '\n'
    d = (body_r + 'END %s\n' % hashlib.sha256(body_r.encode()).hexdigest()).encode()
    try:
        verify_handoff_bytes(d, hashlib.sha256(d).hexdigest(), piece)
        fired, why = False, 'accepted'
    except ValueError as e:
        fired, why = str(e) == 'header', str(e)
    fired = fired and body_r != body
    out('PLANT-PRODUCER N=%d %s: the %s hand-off relabelled kt_cert_v1_9 -> %s -> %s' % (NN, KIND, piece, why, 'FIRES' if fired else
                                                                                         'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-PRODUCER %s' % piece)


def parse_x(rows):
    G = GK.get(KIND, ('psi', 'e1', 'e3'))                               # kt_cert_v1_7: the kind's basis
    m = [[None] * len(G) for _ in range(4)]
    r = [dict() for _ in range(4)]
    for ln in rows:
        f = ln.split(' ', 8)
        if f[0] == 'M':
            m[int(f[1])][int(f[2])] = float(f[3])
        elif f[0] == 'R':
            r[int(f[1])][tuple(int(x) for x in f[2:8])] = arb(f[8])
        else:
            raise ValueError('x row %r' % ln[:40])
    assert all(x is not None for row in m for x in row)
    return dict(G=G, m=m, r0=r[0], r1=r[1], r2=r[2], r3=r[3])


def resolve_c(J):
    """stage_c's results from piece c's hand-off when piece c was run (its record exists), else computed in-line. kt_cert_v1_9: always from
    kt_cert_v1_8's c hand-off (never in-line)."""
    if not os.path.exists(record_path('c')):
        raise ValueError('kt_cert_v1_9: no kt_cert_v1_8 record of piece c (%s); g computes no stage in-line' % record_path('c'))
    if os.path.exists(record_path('c')):
        rows = read_handoff('c')[0]
        got, ndk = {}, {}
        for ln in rows:
            f = ln.split(' ', 1)
            if f[0] == 'NDK':                                           # kt_cert_v1_8: nD's parts per formal-t order
                g = ln.split(' ', 2)
                ndk[int(g[1])] = arb(g[2])
            else:
                got[f[0]] = f[1]
        ints = [int(x) for x in got['INT'].split()]
        if not ndk:
            raise ValueError('hand-off c has no NDK rows')
        return dict(nD=arb(got['NDB']), deg2=ints[0], tot=ints[1], nterms=ints[2], src='hand-off c', nDk=ndk)
    STAGE[0] = 'stage_c %s (in-line)' % KIND
    cres = stage_c(KIND, J)
    cres['src'] = 'in-line'
    return cres


def resolve_tails(J):
    """kt_cert_v1_8: (tails, tailsm, src); tailsm holds the Minkowski-per-order terms of families X and B (TAILM rows, or in-line)."""
    tails, src = _resolve_tails(J)
    return tails, TAILSM, src


TAILSM = {}                                     # kt_cert_v1_8: (fam, idx) -> the Minkowski-per-order term, filled by _resolve_tails


def _resolve_tails(J):
    """the nine tail terms: for each family F, from piece tF's hand-off, or from tF0, tF1, tF2's, or (no record) computed in-line."""
    t = arb(1) / J
    tails, src, polys, cache = {}, {}, {}, {}
    for fam in ('X', 'B', 'A'):
        whole = os.path.exists(record_path('t' + fam))
        single = [os.path.exists(record_path('t%s%d' % (fam, i))) for i in range(3)]
        if whole and any(single):
            raise ValueError('records of both t%s and a t%s<i> piece exist' % (fam, fam))
        for i in range(3):
            pc = ('t' + fam) if whole else (('t%s%d' % (fam, i)) if single[i] else None)
            if pc is None:                                              # kt_cert_v1_9: every tail from kt_cert_v1_8's records
                raise ValueError('kt_cert_v1_9: tail %s%d has no kt_cert_v1_8 record; g computes no tail in-line' % (fam, i))
            if pc is None:
                if fam not in polys:
                    STAGE[0] = 'tail polynomial %s (in-line)' % fam
                    if fam == 'A':
                        polys[fam] = ann_poly(KIND, t)
                    else:
                        if 'T' not in polys:
                            T3 = series_T3(KIND)
                            polys['T'] = tail_poly(T3, t)
                            polys['O'] = tail_orders(T3, t)
                        polys[fam] = polys['T']
                STAGE[0] = 'tail table %s%d (in-line)' % (fam, i)
                tails[(fam, i)], tm_ = tail_term(fam, i, KIND, J, polys[fam], polys.get('O') if fam in ('X', 'B') else None)
                if tm_ is not None:
                    TAILSM[(fam, i)] = tm_
                src[(fam, i)] = 'in-line'
                continue
            if pc not in cache:
                cache[pc] = read_handoff(pc)[0]
            hit = [ln for ln in cache[pc] if ln.startswith('TAIL %s %d ' % (fam, i))]
            if len(hit) != 1:
                raise ValueError('hand-off %s has %d rows for tail %s%d' % (pc, len(hit), fam, i))
            tails[(fam, i)] = arb(hit[0].split(' ', 3)[3])
            if fam in ('X', 'B'):                                       # kt_cert_v1_8: the Minkowski row beside it
                hm = [ln for ln in cache[pc] if ln.startswith('TAILM %s %d ' % (fam, i))]
                if len(hm) != 1:
                    raise ValueError('hand-off %s has %d TAILM rows for tail %s%d' % (pc, len(hm), fam, i))
                TAILSM[(fam, i)] = arb(hm[0].split(' ', 3)[3])
            src[(fam, i)] = 'hand-off ' + pc
    return tails, src


def run_piece(fails, fires):
    J = J_MAIN
    t0 = cpu()
    if PIECE == 'c' or PIECE[:2] == 'tA' or PIECE == 'g':                # kt_cert_v1_8: the F-2 gates before the piece computes
        STAGE[0] = 'majfix gates'
        majfix_gates(fails, fires)
        if fails or fires:
            raise ValueError('a gate failed before the piece: %s' % ', '.join(fails + fires))
    if PIECE == 'x':
        STAGE[0] = 'explicit %s' % KIND
        ex = explicit_part(KIND, fails, fires)
        rows = ['M %d %d %r' % (j, i, ex['m'][j][i]) for j in range(4) for i in range(len(ex['G']))]     # kt_cert_v1_7: len(G)
        for j in range(4):
            for e, c in sorted(ex['r%d' % j].items()):
                rows.append('R %d %s %s' % (j, ' '.join(str(int(x)) for x in e), c.str(80, radius=True)))
        write_handoff('x', rows)
        return None
    if PIECE == 'c':
        STAGE[0] = 'stage_c %s' % KIND
        cres = stage_c(KIND, J)
        out('STAGE-C N=%d %s: nD %s | D4 %d terms, deg2 %d, tot %d (cpu %.1f s)' % (NN, KIND, bstr(cres['nD']), cres['nterms'], cres['deg2'],
                                                                                    cres['tot'], cres['cpu']))
        out('NDK N=%d %s: nD per formal-t order: %s (budgets %s, TOT %d)' % (NN, KIND, ' | '.join('k%d %s' % (k, bstr(v)) for k, v in
                                                                                             sorted(cres['nDk'].items())),
                                                                       ','.join(str(b) for b in cres['budgets']), cres['TOT']))
        rep_fix_c(cres, fails)                                           # kt_cert_v1_8: C-REP-FIX of nD and nD_k
        if fails or NDK_FAILS:
            raise ValueError('a check of piece c failed: %s' % ', '.join(fails + NDK_FAILS))
        write_handoff('c', ['NDB %s' % cres['nD'].str(80, radius=True), 'INT %d %d %d' % (cres['deg2'], cres['tot'], cres['nterms'])] +
                      ['NDK %d %s' % (k, v.str(80, radius=True)) for k, v in sorted(cres['nDk'].items())])
        return None
    if PIECE[0] == 't':
        fam = PIECE[1]
        idxs = (int(PIECE[2]),) if len(PIECE) == 3 else (0, 1, 2)
        t = arb(1) / J
        STAGE[0] = 'tail polynomial %s' % fam
        if fam in ('X', 'B'):
            T3 = series_T3(KIND)
            poly, orders = tail_poly(T3, t), tail_orders(T3, t)
        else:
            poly, orders = ann_poly(KIND, t), None
        mark(KIND, 'tail polynomial %s (%d terms, degree %d, Q degree %d)' % (fam, len(poly[0]), poly[1], poly[2]))
        rows = []
        for i in idxs:
            STAGE[0] = 'tail table %s%d' % (fam, i)
            term, termm = tail_term(fam, i, KIND, J, poly, orders)
            out('TAIL N=%d %s %s%d: e^{-lam J c} N E[F^2] = %s' % (NN, KIND, fam, i, bstr(term)))
            rows.append('TAIL %s %d %s' % (fam, i, term.str(80, radius=True)))
            if termm is not None:                                       # kt_cert_v1_8: C-TAILM and the TAILM row
                okm = not bool(termm < term)
                out('C-TAILM N=%d %s %s%d: Minkowski-per-order term %s, not certainly below the joint term (the triangle inequality) -> %s' % (
                    NN, KIND, fam, i, bstr(termm), 'PASS' if okm else 'FAIL'))
                if not okm:
                    fails.append('C-TAILM %s%d' % (fam, i))
                pl = not (not bool((term / 2) < term))                  # C-TAILM applied to a planted TAILM = TAIL/2 must fail
                out('PLANT-TAILM N=%d %s %s%d: C-TAILM on a planted Minkowski term TAIL/2 fails: %s -> %s' % (
                    NN, KIND, fam, i, pl, 'FIRES' if pl else 'DOES NOT FIRE'))
                if not pl:
                    fires.append('PLANT-TAILM %s%d' % (fam, i))
                rows.append('TAILM %s %d %s' % (fam, i, termm.str(80, radius=True)))
        write_handoff(PIECE, rows)
        return None
    if PIECE == 'cN2':                                                   # kt_cert_v1_9 (the review v1_8 N-2)
        STAGE[0] = 'cN2 %s' % KIND
        cn2_piece(fails, fires)
        return None
    STAGE[0] = 'certified inputs'
    certin(KIND, fails, fires)                                           # kt_cert_v1_9: C-FAR, C-GBB, C-EPSR, C-Z and their plants
    STAGE[0] = 'read x'
    rows, data, want = read_handoff('x')
    ex = parse_x(rows)
    STAGE[0] = 'PLANT-HANDOFF'
    plant_handoff('x', data, want, fires)
    plant_producer(data, fires)                                          # kt_cert_v1_8
    if KIND in ('a', 'am'):                                             # kt_cert_v1_7: am runs the a-engine
        STAGE[0] = 'a-engine'
        bnd, parts = a_engine(J, ex, KIND)
    else:
        STAGE[0] = 'read cN2, c, tails'
        cn2 = read_handoff('cN2')[0]                                    # kt_cert_v1_9: piece cN2's VALID record and hand-off first
        cres = resolve_c(J)                                             # kt_cert_v1_9: kt_cert_v1_8's c hand-off
        crow = [ln.split() for ln in cn2 if ln.startswith('CN2 ')]
        okc = len(crow) == 1 and [int(x) for x in crow[0][1:]] == [cres['tot'], cres['deg2'], int(crow[0][3]), cres['nterms']]
        out('C-CN2-READ N=%d %s: hand-off cN2 (kt_cert_v1_9, record VALID) names D4 with (tot, deg2, terms) = kt_cert_v1_8 c\'s (%d, %d, %d) '
            '-> %s' % (NN, KIND, cres['tot'], cres['deg2'], cres['nterms'], 'PASS' if okc else 'FAIL'))
        if not okc:
            fails.append('C-CN2-READ')
        _rc, cdata, _cw = read_handoff('c')
        plant_producer(cdata, fires, piece='c')                         # kt_cert_v1_9: c relabelled kt_cert_v1_9 must fail
        tails, _tailsm, tsrc = resolve_tails(J)                       # kt_cert_v1_8: the Minkowski terms land in TAILSM
        STAGE[0] = 'stage_g %s' % KIND
        bnd, parts = stage_g(KIND, J, ex, cres, tails, CI['gBb'])
        out('SOURCES N=%d %s: nD from %s; tails %s' % (NN, KIND, cres['src'], ', '.join('%s%d from %s' % (f, i, tsrc[(f, i)]) for f in 'XBA'
                                                                                         for i in range(3))))
    STAGE[0] = 'value'
    val, eps, Z = engine_value(KIND, J, bnd)
    tm = parts['tm']
    vname = {'e1': 'R_e1', 'e3': 'R_e3', 'h': 'A_h', 'h1': 'R^xi_e1', 'h3': 'R^xi_e3', 'a': 'A_a', 't': 'A_t', 'am': 'A_am'}[KIND]
    if KIND in ('a', 'am'):
        out('AENGINE N=%d J=%d %s: bound %s | nP %s | nR %s | far %s (FAR_CRUDE_v1) | Da %d terms, deg %d | cpu D4 %.1f wish %.1f far %.1f '
            '(%.1f s)' % (NN, J, KIND, bstr(bnd), bstr(parts['nP']), bstr(parts['nR']), bstr(parts['far']), parts['nterms'], parts['deg'],
                          tm['D4'], tm['wish'], tm['far'], cpu() - t0))
    else:
        out('ENGINE N=%d J=%d %s: bound %s | nP %s | nD %s | nR0 %s | tailX %.3e tailB %.3e ann %.3e | gB %.3e | far %s (FAR_CRUDE_v1) | '
            'D4 %d terms, deg2 %d, tot %d | cpu wish %.1f far %.1f (%.1f s)' % (
                NN, J, KIND, bstr(bnd), bstr(parts['nP']), bstr(parts['nD']), bstr(parts['nR0']), fup(parts['tailX']), fup(parts['tailB']),
                fup(parts['ann']), fup(parts['gB']), bstr(parts['far']), parts['nterms'], parts['deg2'], parts['tot'], tm['wish'], tm['far'],
                cpu() - t0))
    big = max(parts['fl'].items(), key=lambda kv: kv[1][1])
    out('CERT-IN N=%d %s: far from %s %s (%d items: %s; largest X300 %.3e at %s); R = 1 exactly; %seps_r <= %s (M2B_KV_v1, law_v1 at 300%s); '
        'Z %s from %s %s (lower end)' % (
            NN, KIND, os.path.basename(FARF[NN][0]), CERTIN[FARF[NN][0]][:8], len(parts['fl']), ', '.join(sorted(parts['fl'])),
            float(big[1][1]), big[1][0], '' if KIND in ('a', 'am') else 'gBb %s (vacuum G4R_r, zR^up %s); ' % (
                bstr(CI['gBb']), ', '.join('%.9f' % float(z) for z in CI['zr'])), CI['eps_dec'],
            '' if KIND in ('e1', 'e3') else '; not used by this kind', bstr(Z), os.path.basename(S9F[NN][0]), CI['zkey']))
    for rel in input_paths_g():                                          # kt_cert_v1_9: provenance (the review a50a005a Q2, Q3 (2))
        out('INPUT %s %s' % (rel, sha_file(wpath(rel))))
    out('VALUE N=%d J=%d %s: %s <= %s (ball %s; rounded up; every input certified: CERT-IN)' % (NN, J, KIND, vname, dec_up(val), bstr(val)))
    vl, vh = dec_out(val)                                                # kt_cert_v1_7: the RESULT line (pk15's reader)
    bl, bh = dec_out(bnd)
    rline = 'RESULT N=%d J=%d %s: %s [%s, %s] bound [%s, %s] FLOAT-IN none' % (NN, J, KIND, vname, vl, vh, bl, bh)
    out(rline)
    nofloat(rline, fails, fires)                                         # kt_cert_v1_9: C-NOFLOAT, PLANT-NOFLOAT
    law_bases(parts, fails, fires)                                       # kt_cert_v1_8: M4's law inputs at J = 300
    if KIND in ('e1', 'e3'):
        out('F2A N=%d %s: R_%s^{|f|} <= %s, the same ball as R_%s (SPEC ADD2 v1 sect. 6; check C-F holds with equality)' % (
            NN, KIND, KIND, dec_up(val), KIND))
    if KIND in HOOK:
        out('C-BAD-HOOK N=%d %s (SPEC ADD2 v1 sect. 8; W2 weights them by X): gB %.3e, far_out %.3e (FAR_CRUDE_v1, (2J)^2 on G4, 2J on G3), '
            'tailX %.3e tailB %.3e ann %.3e' % (NN, KIND, fup(parts['gB']), fup(parts['far']), fup(parts['tailX']), fup(parts['tailB']),
                                               fup(parts['ann'])))
    if not (val > 0 and val.is_finite()):
        fails.append('K-FIN %s' % KIND)
    return bnd, parts, val


def input_paths_g():
    """kt_cert_v1_9: every file piece g reads, under CODEDIR, for its INPUT lines: the FAR_CRUDE_v1 record, run output and reader; the vacuum
    record, asm output, manifest and reader (kinds other than a, am); M2B_KV_v1, its asm output and reader; the S9 record, asm output,
    manifest and reader; x's producer record and hand-off; for kinds with a piece c, kt_cert_v1_8's c and tail records and hand-offs and
    this file's cN2 record and hand-off; kt_cert_v1_8's g record (C-REP-V18)."""
    rel = lambda p: os.path.relpath(p, W18)
    paths = list(FARF[NN]) + [READERS['far']]
    if KIND not in ('a', 'am'):
        paths += list(VACF[NN]) + [READERS['vac']]
    paths += list(M2BF) + [READERS['m2b']] + list(S9F[NN]) + [READERS['s9'], rel(record_path('x')), rel(handoff_path('x'))]
    if KIND not in ('a', 'am'):
        for pc in V18PIECES + ('cN2',):
            paths += [rel(record_path(pc)), rel(handoff_path(pc))]
    return paths + ['pk02/out_kt_cert_v1_8_g.%s.out' % SUFFIX]


def float_tokens(rline):
    """kt_cert_v1_9: the FLOAT-IN token list of a RESULT line (None if the line has no FLOAT-IN field)."""
    if ' FLOAT-IN ' not in rline:
        return None
    return rline.split(' FLOAT-IN ', 1)[1].split()


def nofloat(rline, fails, fires):
    """C-NOFLOAT: this RESULT line's FLOAT-IN list is exactly ['none']; PLANT-NOFLOAT: the same test on kt_cert_v1_8's form of the line
    (FLOAT-IN far logR gBb eps_r Z) must fail."""
    ok = float_tokens(rline) == ['none']
    out('C-NOFLOAT N=%d %s: the RESULT line\'s FLOAT-IN list is %s -> %s' % (NN, KIND, float_tokens(rline), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-NOFLOAT')
    old = rline.rsplit(' FLOAT-IN ', 1)[0] + ' FLOAT-IN far logR gBb eps_r Z'
    fired = float_tokens(old) != ['none']
    out('PLANT-NOFLOAT N=%d %s: kt_cert_v1_8\'s form (FLOAT-IN far logR gBb eps_r Z) fails the test -> %s' % (
        NN, KIND, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-NOFLOAT')


STUB_NAMES = ('riglap2', 'riglap3', 'amom2b', 'npoly', 'scipy', 'scipy.special')
STUB_CALLS = []                                 # kt_cert_v1_9: any use of a stub (C-NORIG requires none)
V18MOD = []                                     # kt_cert_v1_9: kt_cert_v1_8 as imported by cN2


class _Stub(types.ModuleType):
    """kt_cert_v1_9 (cN2): an inert stand-in for a module that kt_cert_v1_8 imports at module level only for its FLOAT part 4b; any use of an
    attribute raises and is counted (C-NORIG)."""
    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)

        def _forbidden(*a, **k):
            STUB_CALLS.append('%s.%s' % (self.__name__, name))
            raise RuntimeError('kt_cert_v1_9 cN2: %s.%s is not available' % (self.__name__, name))
        return _forbidden


def relay(buf):
    for ln in buf.getvalue().splitlines():
        out('V18> ' + ln)


def import_v18():
    """kt_cert_v1_9 cN2 (the review a50a005a Q1 (a)): kt_cert_v1_8.py itself (CERTIN, full sha256), imported as a module with the item c.<suffix>
    and this piece's LIM. Its module-level setup runs on its own pinned inputs (its C-HASH, the z9sym data, ctx.prec 512, majfix_v1_1); its
    main() does not run. The modules its part 4b imports (riglap2, riglap3, amom2b, npoly, scipy.special) bind to inert stubs. Its prints
    go to this record prefixed 'V18> '."""
    for nm in STUB_NAMES:
        if nm in sys.modules:
            raise ValueError('C-NORIG: %s is loaded before kt_cert_v1_8 is imported' % nm)
        sys.modules[nm] = _Stub(nm)
    argv, buf = sys.argv, io.StringIO()
    sys.argv = [wpath('pk02/kt_cert_v1_8.py'), 'c.' + SUFFIX, str(LIM)]
    try:
        sp = importlib.util.spec_from_file_location('kt_cert_v1_8_mod', wpath('pk02/kt_cert_v1_8.py'))
        v18 = importlib.util.module_from_spec(sp)
        with contextlib.redirect_stdout(buf):
            sp.loader.exec_module(v18)
    except SystemExit as e:
        relay(buf)
        raise ValueError('kt_cert_v1_8 stopped at import (exit %r)' % (e.code,))
    finally:
        sys.argv = argv
    signal.signal(signal.SIGXCPU, _on_xcpu)                             # this file's cap handler again
    relay(buf)
    V18MOD.append(v18)
    return v18


def cn2_degs(P):
    """(total degree, deg2 = degree in the forms 6-11, Q degree = degree in the forms 9-11, mass on the sigma pair forms 3-5) of an NPolyA."""
    e = P.exponents()
    return int(e.sum(axis=1).max()), int(e[:, 6:].sum(axis=1).max()), int(e[:, 9:].sum(axis=1).max()), int(e[:, 3:6].sum())


def cn2_digest(P):
    """a digest of an NPolyA's exponent set: the first 16 hex digits of the sha256 of its sorted exponent tuples."""
    rows = sorted(tuple(int(x) for x in r) for r in P.exponents())
    return hashlib.sha256(repr(rows).encode()).hexdigest()[:16]


def cn2_violations(P, bounds):
    """how P exceeds the bounds (tot, deg2, Q) piece c's tables were built with, or carries a sigma pair form; [] if it does not."""
    tk, dk, qk, sk = cn2_degs(P)
    bad = []
    if tk > bounds[0]:
        bad.append('total %d > %d' % (tk, bounds[0]))
    if dk > bounds[1]:
        bad.append('deg2 %d > %d' % (dk, bounds[1]))
    if qk > bounds[2]:
        bad.append('Q degree %d > %d' % (qk, bounds[2]))
    if sk != 0:
        bad.append('sigma pair forms present')
    return bad


def cn2_piece(fails, fires):
    """kt_cert_v1_9, piece cN2:
    (a) kt_cert_v1_8's own construction (hk, fix_pis_c with majfix_v1_1's cap and evaluate, Dbar, the per-order split byord), from its pinned
        file as imported by import_v18, on its pinned inputs at ctx.prec 512: D4 and every D4_k;
    (b) ties D4 to v1_8's c hand-off (INT: deg2, tot, terms; the NDK orders), prints each D4_k's term count and the exponent digests of D4 and
        each D4_k (c's record has no per-order term counts, only the NDK balls);
    (c) checks every D4_k against the bounds piece c's tables were built with: CondGA(cmT, tot) with D4's tot, CondMomA(.., deg2, caps
        {1: max(qdeg, 1)}) (kt_cert_v1_8 l.1671-1673), and no sigma pair form (l.1648's assertion);
    (d) explicit raises; PLANT-CN2: the top D4_k with one monomial of total degree tot + 1 added must fail the same test.
    Writes hand-off cN2 (rows CN2, CN2D, CN2K), which g requires."""
    v18 = import_v18()
    okv = v18.SELF_SHA == V18_SHA and v18.KIND == KIND and v18.NN == NN and v18.PIECE == 'c' and ctx.prec == 512
    out('C-CN2-V18 N=%d %s: kt_cert_v1_8 imported from its pinned file (sha256 %s), item c.%s (KIND %s, N %d), ctx.prec %d; its part 4b '
        'imports bound to inert stubs -> %s' % (NN, KIND, v18.SELF_SHA, SUFFIX, v18.KIND, v18.NN, ctx.prec, 'PASS' if okv else 'FAIL'))
    if not okv:
        fails.append('C-CN2-V18')
        raise ValueError('kt_cert_v1_8 import is not the pinned file for this item')
    J = v18.J_MAIN
    t = arb(1) / J
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        hL = {k: v18.hk(k, [(v, v18.a_e) for v in v18.XD], v18.bondsL, v18.cf_rad) for k in range(1, 5)}
        pis, byord, TOT, budgets, qold = v18.fix_pis_c(v18.KIND, t, hL)
        D4 = v18.Dbar(4, hL, pis)
        D4ks = {k: v18.Dbar(4, hL, byord[k]) for k in sorted(byord)}
    relay(buf)
    tot, deg2, qdeg, s0 = cn2_degs(D4)
    bounds = (tot, deg2, max(qdeg, 1))
    mark(KIND, 'cN2: kt_cert_v1_8\'s D4 (%d terms) and %d orders D4_k' % (len(D4.codes), len(D4ks)))
    rows_c = read_handoff('c')[0]
    got = dict(ln.split(' ', 1) for ln in rows_c if not ln.startswith('NDK '))
    cint = [int(x) for x in got['INT'].split()]
    corders = sorted(int(ln.split(' ', 2)[1]) for ln in rows_c if ln.startswith('NDK '))
    okt = cint == [deg2, tot, len(D4.codes)] and corders == sorted(D4ks) and s0 == 0
    out('C-CN2-TIE N=%d %s: kt_cert_v1_8\'s D4 has deg2 %d, tot %d, Q degree %d, %d terms (exponent digest %s) and formal-t orders %s; its c '
        'hand-off: INT (deg2, tot, terms) %s, NDK orders %s (c\'s record has no per-order term counts) -> %s' % (
            NN, KIND, deg2, tot, qdeg, len(D4.codes), cn2_digest(D4), sorted(D4ks), cint, corders, 'PASS' if okt else 'FAIL'))
    if not okt:
        fails.append('C-CN2-TIE')
    bad, rows = [], ['CN2 %d %d %d %d' % (tot, deg2, qdeg, len(D4.codes)), 'CN2D %s' % cn2_digest(D4)]
    for k, P in D4ks.items():
        if len(P.codes) == 0:
            rows.append('CN2K %d 0 0 0 0 -' % k)
            out('CN2K N=%d %s k%d: empty' % (NN, KIND, k))
            continue
        v = cn2_violations(P, bounds)
        if v:
            bad.append('k%d: %s' % (k, ', '.join(v)))
        tk, dk, qk, _ = cn2_degs(P)
        rows.append('CN2K %d %d %d %d %d %s' % (k, len(P.codes), tk, dk, qk, cn2_digest(P)))
        out('CN2K N=%d %s k%d: %d terms, (total, deg2, Q degree) (%d, %d, %d), exponent digest %s' % (NN, KIND, k, len(P.codes), tk, dk, qk,
                                                                                                  cn2_digest(P)))
    out('C-CN2 N=%d %s: every D4_k within the bounds of piece c\'s tables (tot %d, deg2 %d, Q %d = max(D4\'s Q degree %d, 1)) and free of '
        'sigma pair forms: %s -> %s' % (NN, KIND, bounds[0], bounds[1], bounds[2], qdeg, 'yes' if not bad else 'NO: ' + '; '.join(bad),
                                         'PASS' if not bad else 'FAIL'))
    if bad:
        fails.append('C-CN2')
    top = max(k for k, P in D4ks.items() if len(P.codes))
    e_bad = [0] * NV12
    e_bad[XS[0]] = tot + 1
    fired = bool(cn2_violations(D4ks[top].add(mono(e_bad)), bounds))
    out('PLANT-CN2 N=%d %s: D4_k%d with one monomial X_%d^%d (total degree tot + 1) added must fail the same test -> %s' % (
        NN, KIND, top, XS[0], tot + 1, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-CN2')
    for rel in ('pk02/kt_cert_v1_8.py', 'pk02/out_kt_cert_v1_8_c.%s.out' % SUFFIX, 'pk02/hand_kt_cert_v1_8_c.%s.txt' % SUFFIX):
        out('INPUT %s %s' % (rel, sha_file(wpath(rel))))
    if fails or fires:
        raise ValueError('a check of piece cN2 failed: %s' % ', '.join(fails + fires))
    write_handoff('cN2', rows)


def c_tilt_a(fails, fires):
    """C-TILT (a): domination of the tilt rates and the annulus radius, positivity of the Chernoff lambdas; PLANT-TILT."""
    def rate_ok(c, a):
        return arb(c) >= -(1 - arb(a)).log() / (2 * arb(a))
    rates = (('c_m', c_m, a_m), ('c_e', c_e, a_e), ('c_pp', c_pp, a_pp))
    okr = all(rate_ok(c, a) for _, c, a in rates)
    app = (arb(RHO_M).asin() + DELTA).sin() ** 2
    oka = arb(a_pp) >= app
    lams = (LAM_T, 0.5)
    okl = all(x > 0 for x in lams)
    ok = okr and oka and okl
    out('C-TILT (a) N=%d: %s; a_pp %.17g >= sin^2(asin rho_m + delta) = %s; Chernoff lambdas %s > 0 -> %s' % (
        NN, ', '.join('%s %.17g >= -log(1 - a)/(2a) = %s (a %.17g)' % (nm, c, (-(1 - arb(a)).log() / (2 * arb(a))).str(12, radius=False), a)
                      for nm, c, a in rates), a_pp, app.str(12, radius=False), ' '.join('%g' % x for x in lams), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-TILT (a)')
    p_rate = rate_ok(c_m * (1 - 1e-9), a_m)
    n0 = len(TILT_LOG)
    p_pd = tilted_cov_a(LD, BD, [arb(1000)] + [arb(0)] * 5, label='PLANT')[0] is not None
    del TILT_LOG[n0:]
    fired = (not p_rate) and (not p_pd)
    out('PLANT-TILT N=%d: c_m (1 - 1e-9) passes the rate test: %s; a lambda = 1e3 tilt certified positive definite: %s -> %s' % (
        NN, p_rate, p_pd, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-TILT')


def c_tilt_b(fails):
    """C-TILT (b): every positive-definiteness test of this piece certified (the piece stops otherwise); count and smallest minor."""
    ok = all(c for _, c, _ in TILT_LOG) and len(TILT_LOG) > 0
    labels = sorted(set(lab for lab, _, _ in TILT_LOG))
    out('C-TILT (b) N=%d: %d positive-definiteness tests (%s), all certified: %s; smallest leading minor lower end %.3e -> %s' % (
        NN, len(TILT_LOG), ', '.join(labels), ok, min((lo for _, _, lo in TILT_LOG), default=float('nan')), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-TILT (b)')


def rep_v18(kind, bnd, parts, val, fails):
    """kt_cert_v1_9, C-REP-V18: the near parts against kt_cert_v1_8's g record of this item (CERTIN; first line naming V18_SHA and the item,
    VERDICT lines exactly ['VERDICT VALID']). nP, nD, nR0 (a, am: nP, nR) were printed as balls 'mid +- rad': each, widened by half a unit
    of its printed digits, must overlap this run's ball; tailX, tailB and ann (printed %.3e) must print the same. gB and far, whose inputs
    v1_9 certifies, are printed beside v1_8's FLOAT-based values (INFO)."""
    name = 'out_kt_cert_v1_8_g.%s.out' % SUFFIX
    with open(os.path.join(OWN, name)) as fh:
        txt = fh.read().splitlines()
    okh = bool(txt) and txt[0].startswith('kt_cert_v1_8 sha256 %s ITEM=g.%s ' % (V18_SHA, SUFFIX)) and \
        [ln for ln in txt if ln.startswith('VERDICT')] == ['VERDICT VALID']
    pat = ('AENGINE' if kind in ('a', 'am') else 'ENGINE') + ' N=%d J=300 %s: ' % (NN, kind)
    eng = [ln for ln in txt if ln.startswith(pat)]
    if len(eng) != 1:
        raise ValueError('C-REP-V18: %s has %d %s lines' % (name, len(eng), pat.split()[0]))

    def half_unit(s, digits):
        return 0.5 * 10.0 ** (int(s.split('e')[1]) - digits)
    res, ok = ['header/verdict %s' % ('PASS' if okh else 'FAIL')], okh
    for k in (('nP', 'nR') if kind in ('a', 'am') else ('nP', 'nD', 'nR0')):
        mt = re.search(r'\b%s ([0-9.]+e[+-][0-9]+) \+- ([0-9.]+e[+-][0-9]+)' % k, eng[0])
        ms, rs = mt.group(1), mt.group(2)
        old = arb(ms) + arb(0, float(rs) + half_unit(rs, 1) + half_unit(ms, 9))
        good = old.overlaps(parts[k])
        ok &= good
        res.append('%s %s vs %s +- %s%s' % (k, bstr(parts[k]), ms, rs, '' if good else ' (NO OVERLAP)'))
    if kind not in ('a', 'am'):
        for k in ('tailX', 'tailB', 'ann'):
            s_old, s_new = printed(eng[0], k), '%.3e' % fup(parts[k])
            good = s_old == s_new
            ok &= good
            res.append('%s %s vs %s%s' % (k, s_new, s_old, '' if good else ' (OFF)'))
        res.append('INFO gB %.3e (v1_8 FLOAT gBb: %s)' % (fup(parts['gB']), printed(eng[0], 'gB')))
    mf_ = re.search(r'\bfar ([0-9.]+e[+-][0-9]+)', eng[0])
    res.append('INFO far %s (v1_8 FLOAT parts: %s)' % (bstr(parts['far']), mf_.group(1) if mf_ else '?'))
    out('C-REP-V18 N=%d %s against %s: %s -> %s' % (NN, kind, name, '; '.join(res), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-REP-V18')


def norig(fails):
    """C-NORIG: kt_cert_v1_8's FLOAT path (part 4b) is gone, so no module it imported is loaded (the packing audit 89f7a0d0 item (1)).
    In piece cN2, which imports kt_cert_v1_8 itself, those modules are the inert stubs of import_v18, and none was used."""
    if PIECE == 'cN2':
        stubs = all(isinstance(sys.modules.get(nm), _Stub) for nm in STUB_NAMES)
        ok = stubs and not STUB_CALLS and 'pseries' not in sys.modules
        out('C-NORIG N=%d: cN2 imports kt_cert_v1_8, whose part 4b imports %s: all inert stubs: %s; stub uses: %s; pseries loaded: %s -> %s' % (
            NN, ', '.join(STUB_NAMES), stubs, STUB_CALLS or 'none', 'pseries' in sys.modules, 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-NORIG')
        return
    loaded = [m for m in ('riglap2', 'riglap3', 'amom2b', 'npoly', 'pseries', 'scipy.special') if m in sys.modules]
    out('C-NORIG N=%d: loaded among riglap2, riglap3, amom2b, npoly, pseries, scipy.special: %s -> %s' % (
        NN, ', '.join(loaded) if loaded else 'none', 'PASS' if not loaded else 'FAIL'))
    if loaded:
        fails.append('C-NORIG')


def r1_check(fails, fires):
    """C-R1 and PLANT-R1 (the review a50a005a Q3 (3)): tau_N^2 = tau_D tau_4 exactly in Q(sqrt 5, sqrt 21), so R = 1 exactly; the same identity
    with B + 1/1000 must fail."""
    diff, (tD, tN, t4) = r1_exact()
    ok = diff.is_zero()
    out('C-R1 N=%d %s: exact spanning-tree counts tau_D %.12f, tau_N %.12f, tau_4 %.12f in Q(sqrt 5, sqrt 21); tau_N^2 - tau_D tau_4 = %s, so '
        'R = (tau_D tau_4 / tau_N^2)^(n/2) %s -> %s' % (NN, KIND, float(tD), float(tN), float(t4), 'exactly 0' if ok else
                                                     'NONZERO %r' % (diff.v,), '= 1 exactly' if ok else '!= 1', 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-R1')
    fired = not r1_exact(QA, QB + Fraction(1, 1000))[0].is_zero()
    out('PLANT-R1 N=%d %s: the identity with B + 1/1000 must fail -> %s' % (NN, KIND, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-R1')


def npguard(fires):
    """PLANT-NPGUARD (packing audit item (2)): mono with an exponent equal to BB must raise before packing."""
    try:
        mono([BB] + [0] * (NV12 - 1))
        fired = False
    except ValueError:
        fired = True
    out('PLANT-NPGUARD N=%d: mono with an exponent equal to BB = %d raises -> %s' % (NN, BB, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-NPGUARD')


def prec_check(fails):
    """C-PREC: flint's precision is still 512 at the end (m2b_reader_v1 sets 256 at import; the readers are loaded before ctx.prec = 512)."""
    ok = ctx.prec == 512
    out('C-PREC N=%d: flint ctx.prec %d at the end of the piece -> %s' % (NN, ctx.prec, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-PREC')


def main():
    fails, fires = [], []
    complete = False
    try:
        c_tilt_a(fails, fires)
        out('C-IMPORT N=%d: majfix_v1_1 from %s -> %s' % (NN, mf.__file__, 'PASS' if os.path.realpath(mf.__file__) ==
                                                         os.path.realpath(os.path.join(OWN, 'majfix_v1_1.py')) else 'FAIL'))
        if os.path.realpath(mf.__file__) != os.path.realpath(os.path.join(OWN, 'majfix_v1_1.py')):
            fails.append('C-IMPORT')
        res = run_piece(fails, fires)
        if PIECE == 'g':
            bnd, parts, val = res
            rep_fix_g(KIND, parts, fails)                               # kt_cert_v1_8: C-REP-FIX against the majfix twin
            rad_check(bnd, parts, fails)
            rep_v18(KIND, bnd, parts, val, fails)                       # kt_cert_v1_9: C-REP-V18 against kt_cert_v1_8's g record
            r1_check(fails, fires)                                      # kt_cert_v1_9: C-R1, R = 1 exactly in the run
        if PIECE not in ('x', 'cN2'):                                    # kt_cert_v1_9: cN2 forms no tilted covariance
            c_tilt_b(fails)
        if PIECE == 'cN2':                                               # kt_cert_v1_9: the capped pis are kt_cert_v1_8's (its own C-TMONO)
            V18MOD[0].c_tmono(fails)
        elif PIECE in ('c', 'g') or PIECE[:2] == 'tA':                   # kt_cert_v1_8
            c_tmono(fails)
        norig(fails)                                                     # kt_cert_v1_9: C-NORIG, PLANT-NPGUARD, C-PREC
        npguard(fires)
        prec_check(fails)
        fails += SING_FAILS + NDK_FAILS
        fires += SING_FIRES
        complete = True
    except CapStop as e:
        out('CAP-STOP before %s at cpu %.1f s (LIM %d)' % (e, cpu(), LIM))
    except (mf.TradePosError, mf.CapError, mf.RadiusError) as e:      # kt_cert_v1_8: C-TRADE-POS (or C-RADV, or a cap with no t) stops
        out('C-TRADE-POS N=%d %s %s: %s -> FAIL (STOP)' % (NN, KIND, PIECE, e))
        out('VERDICT INVALID (C-TRADE-POS)')
        return 1
    except Exception as e:
        traceback.print_exc()
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        out('VERDICT INVALID (ERROR)')
        return 1
    why = fails + ['%s did not fire' % x for x in fires] + ([] if complete else ['INCOMPLETE'])
    if PIECE == 'g':                                                     # kt_cert_v1_9: the only CERTIFIED tag (the review a50a005a Q3 (2))
        out('STATUS N=%d %s: %s' % (NN, KIND, 'CERTIFIED (FLOAT-IN none; every input read through its certified reader, bound to its run and '
                                               'pinned: the INPUT lines)' if not why else 'NOT CERTIFIED (%s)' % ', '.join(why)))
    out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (MODE, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
    out('VERDICT %s%s' % ('VALID' if not why else ('INCOMPLETE' if why == ['INCOMPLETE'] else 'INVALID'), '' if not why else ' (%s)' % ', '.join(why)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
