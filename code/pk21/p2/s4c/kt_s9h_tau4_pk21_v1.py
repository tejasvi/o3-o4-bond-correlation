#!/usr/bin/env python3
"""kt_s9h_v1_2.py (FROZEN, the file for the VERTICAL mode's certified run (S_V first): kt_s9h_v1_1 (7bcc32d2: kt_s9h_v1 +
code = m28 a5adef9b) + the C-VERT-ONLY (tested in the mock snapshot m29 00a1c0b3, whose
only other change is M2B_MODE). Its vertical inputs (S4-U, S4-TRB, M2(b), M3) are all certified; the S_TB' inputs (t, joint, beta_H's
status) stay MOCK or FLOAT and the vertical mode reads none of them, gated. P-2 (the certified t and joint records) goes into a file
of a new name. Every run here needs the approval naming this file's sha8) -- pk07.
  - v1_2, C-VERT-ONLY: in the vertical mode no S_TB' provider runs (provide_sh1, provide_joint, provide_tin and provide_bh each
    record themselves in STB_READS on entry), the module-level C-HASH leaves FILES_STB (SH1's outputs and reference parser, KT-S9B's
    FLOAT bars, the TRB_H record and its asm outputs) unopened, and SH1, the joint and the t inputs do not exist; a gate after the
    providers and again at the end, with PLANT-VERT-ONLY's three cases (a record of provide_tin having run, t inputs present, one
    FILES_STB file opened). The full mode prints the providers that ran as INFO.
  - v1_1 P-3, the beta_H provider (provide_bh; the rule 19f74c2b on (a), (b), (d); c_e by pk15's route B): pk08's
    S4_TRBH_CERTIFIED_v1 (bb53005c) read with the S4-TRB provider's checks (C-HASH, C-FMT, C-SRC against the U3_P and READING lines of
    both asm outputs), C-DIAG (each row's t = 0 term >= its harmonic diagonal: row T is the t bond), C-MHAT (m1..m3 >= 0, so m-hat >= 1)
    and C-BH per N: beta_H = max((N-1)/2 - c_e_lo, [D0_HI + sum_k max(Dk_HI, 0) 300^-k + R_CERT(T)] / (1 - delta)^2), delta =
    eps_r/sqrt(1 - s^2) at J = 300, J-uniform,
    one full-norm bound for both parities and the u-perp case, gated by SH4's validity c_e_hi <= (N-1)/2 - c_N/300 (H-BESSEL's c_N)
    and HZ_PLAN_v1_1 l.461's kill line. c_e is the t inputs' ce_lo/ce_hi (FIELDS, read by t_read) when the record has them, else the
    harmonic c_t as a FLOAT stand-in. Plants: PLANT-FMT-TRBH, PLANT-HSRC, PLANT-PRECERT-TRBH, PLANT-ROWSWAP, PLANT-MHAT, PLANT-BHVALID.
    The beta_H tag reads CERTIFIED only with certified t inputs carrying ce_lo/ce_hi and a certified M2 vacuum tag (eps_r).
The certified snapshot of kt_s9h_s4 (b186e54c), with v2_3 folded in (the Q2). Everything not listed here is s4's.
  - Modes (argv[1]): vsweep and vscan, the VERTICAL-only mode: the S5-S7 providers alone (S4-U, S4-TRB, M2(b), M3); no t, A_a, beta_H
    or joint provider is called, C-EXP and the C2-a/P2-14 parts are skipped, and vsweep writes EXPORT_KT_S67_v1 only (S8's export,
    CERTIFIED when every vertical input tag is). sweep and scan, the full mode: the same plus S9's providers and parts; sweep writes
    EXPORT_KT_S9H_v1, and builds EXPORT_KT_S67_v1's text without writing it: C-VERT-MODES requires its piece lines and shared header
    lines to equal, string for string, the vertical run's export (by default this file's own vsweep outputs, bound through their run
    output: first line naming this file's sha256 and ITEM=vsweep, VERDICT VALID, the EXPORT line's sha256; VMODE_PIN for a later file),
    with PLANT-VERT-MODES.
  - Readers: EXPORT_KT_S67_v1 through S8's pinned bound reader kt_s67_export_reader_v2_1 (b0a23237; C-EXPORT reads the text as S8 will:
    loads with the run output's EXPORT and VERDICT lines when CERTIFIED, else loads_noncert; rule V1, jlo and jhi as the grid floats).
    pk15's records through rule V2 (bound_ok: the producing output's VERDICT lines exactly ['VERDICT VALID'] and one EXPORT line
    naming the record with its sha256).
  - M3 provider (provide_m3): pk03's records only through m3_reader_v4_4.load(path, asm_out, 300, N); balls into Ctx.entry.
  - M2(b) provider (provide_m2b): pk02's M2B_KV_v1 (LAW v1; SPEC_M2B_CERT_v1 ffd842a2, ADD1, ADD2; its final layout) through its
    pinned reader, bound to m2b_asm_v1's output; vac_law_v1 evaluates LAW v1 in mp.iv at the piece's left end (C-VACMONO: every term
    nonincreasing in J for J >= 300, and the lambda* >= 0.3) and returns
    each term as [0, its upper end]; C-FMT M2B, C-LAW300 (an independent evaluation of the record's J = 300 values, 1e-9) with
    PLANT-M2B-SWAP, PLANT-VACMONO; hooks z2 and Rtr (SPEC_MA_LAYER_v1_2_ADD1 sect. 2) in the distance table. The FLOAT reproductions
    keep vac_float (float_m3).
  - t provider (provide_tin; the Q1): pk15's kt_p2_assembly export EXPORT_P2_T_v1 (the agreed layout, with Aa_lo), bound
    (C-BIND T), FIELDS read by name, C-FLIP a declaration check (XTB_SOURCE = FLIP_OF_XTA, Xtb_lo = Xta_lo string for string:
    sound); A_a from the record's Aa_lo (else S9(b)'s FLOAT stand-in); beta_H FLOAT until P2-10's record. Joint provider: pk15's
    assembly export (JOINT_MODE; the v1_11 MOCK export, pX_hi rounded up, until the certified one). The scan's INFO C2-a CORNER line
    gives pk15's width budget (A_t and A_a lowered together, pi_a and pi_t recomputed); the sweep's C2a.4 JOINT DH line prints each
    class's claim threshold as the joint record's inputs give it (the route-A rule: no constant) and C-DHJ gates agreement with any
    DH the record states.
  - Tags: TAG_PINS slots for 'M3 entries', 'M2 vacuum', 't inputs' and 'joint inputs', each set only by its provider in certified mode
    with every check passing; c2a_tags gives each C2-a verdict the tags it rests on ('A_a', 'beta_H' read FLOAT
    until they have providers). C-EXPORT2 fails on a missing DH key, with PLANT-EXPORT2-DH; c2a_add, c2a_acc and the new
    verdict-path functions are in VERDICT_FUNCS. THIN: a claim threshold below its hand-off level prints its smallest slack.
  - The sweep's INFO S7 ROOM line (the paper's all-piece S7 distances): per N the smallest flip of S7 over the 92 grid pieces for
    R_w, the joint group and the bars (the first piece's flip, every other piece checked at it / 1.004, a failing piece's own flip),
    and the last piece's. The notes: m4 N-1..N-5 (C-GRID-ALL, the C-EXPORT control, VERTICAL-TIE, string-built plants, the J >= 300
    guard), m5 N-1..N-4 (the reader's __file__ self-pin, a local FORMAT and VERDICT test, PLANT-DHJ, no other DH_ key)
    (PLANT-M2B-MOCK); C-C2's certified form and the ADD1 N_delta plant's FLOAT-copy fallback; the FLOAT_IN status rule. Also:
    C-M2B-LOCAL wants exactly one line starting CLAIM, holding M2B_CLAIM_G once, and PLANT-M2B-LOCAL has four cases; in mock mode both
    run on a certified-form copy of the mock built here (and the mock itself must be refused), so the code runs before its certified use.
  - C-TRIAL: the S7 records' trial_set names the z9sym trial states and the symmetrized vacres of TRIAL_SET (full sha256),
    and m-hat's m1..m3 are read from that same vacres; the FLOAT reproductions keep the author's pk10 vacres (same m1..m3). The chain
    (c_trial_chain, pk03): each record's engine.m3_run_v1_7 = its asm output's line-1 script sha256 = M3_RUN, one C-HASH PASS line
    per asm output, and the script's INPUTS pin TRIAL_SET's four files by the same full sha256s. S4-U and S4-TRB read no trial or
    vacres file (pk08, via main), so they need no trial match.
  - C-PARITY: the Ritz blocks drop the cross-parity entries, so for certified records every field of B5's g(0,2),
    g(1,2), g(2,3) (a_k, ak_rad, B, Bp, err) must be exactly zero, and clT's T(0,2), T(1,2), T(2,3) absent or all zero; a gate per
    certified N, with a plant for each field, for a dropped field, a None field and a bool field (False == 0), and for a
    present nonzero T entry. C-C2's certified form tests containment.
  - Input state: M3 certified at both N (pk03's m3_run_v1_7 records, M3_MODE certified, TAG_PINS['M3 entries'] e55c5de1); S4-U
    and S4-TRB certified; M2(b) certified (v1_1 P-1: pk02's M2B_KV_v1 13cc0d9a through m2b_reader_v1, with C-M2B-LOCAL and
    C-TRIAL M2B, the record's PIN_TRIAL naming TRIAL_SET's vacres); the t inputs from pk15's MOCK assembly run v1_24 (with ce_lo,
    ce_hi), the joint inputs from its MOCK run v1_11. So the vertical results can read CERTIFIED; the C2-a results wait for
    T_REC['certified'] and JOINT_RECS['certified'] (P-2), and beta_H's tag for the certified t inputs (A_a has no provider beyond the
    t record's Aa_lo).
S_TB' row P2-11, C2-a = S9(h) for t/bb pairs and their vertical partners in finite strips away from the ends: a fork of
kt_s67_cert_v2_2.py (0718efcc) to the plan pk07/PLAN_P2_11_C2A_v1.md (301d05a4) and the derivation notes
pk07/NOTE_P2_11_C2A_v1.md (272ba327) and NOTE_P2_11_C2A_v1_1.md (f96f1692). The
step-3 code (kt_s9h_s3 86b1368c) is the dd054da8. P2-11 claims the pairs with k >= 0 only: t/bb pairs
with |i - i'| >= 2, mixed pairs (t_i, a_j), (t_i, b_j) with j not in {i, i+1}, every end exponent >= the kind's threshold; P2-14's
joint kind (here) takes the overlapping pairs without a common vertex, D3 (t_i, bb_i+-1), D4 (t_i, b_i), D4M (t_i, b_i+1), at window
end exponents >= its threshold; i = i' for the flip is Lemma 19.6a; P2-12 covers everything below the thresholds at n >= 6.
  - Thresholds (the rules): the claim threshold DH_N<N>_<K> is the smallest d at which the kind's slack is certainly > 0 on every
    piece at d and every larger d (no headroom factor; larger d than DH_MAX follow, the slack being nonincreasing in e);
    the planning threshold DH_PLAN_N<N>_<K> needs every input's distance to flip >= HANDOFF_HR on every piece (1.2 flip, same and
    joint, 1.05 mixed); the headroom table by d (HR_LEVELS) goes into the export EXPORT_KT_S9H_v1 for P2-12 and P2-16.
  - The joint kind (NOTE_P2_11_C2A_v1_1 sect. 2; joint_slack): Cov D >= Cov_inf_lo - 2 e pX - e^2 normX - (2 e p1 + e^2 B1)(2 e p2 +
    e^2 B2)/(1 - rho1^w_X e^2), on pk15's joint record (provide_joint: C-HASH, C-FMT, C-SRC, C-GRID, C-SRC-J, T48, the certified
    requirements of the points 2-4; joint_scan; C2a.4 in the sweep).
  - The kinds (step 3; KINDS, kind_slack): each is one inequality in units of the exact s_x^k, checked once at k = 0, which covers
    every k >= 0 because every subtracted term is nonincreasing in k under kind_hyp (r2, ro, rho1 < 1, rho1^(w_e+w_f) e^2 < 1):
      flip (t_i, bb_i'), w = (2, 2):  F = (A_t - bH e)^2 - 2 bH^2 e^2 - (O_t^1/2 + bH e)^2 - T_(2,2)(0, e)   (P-1);
      same (t_i, t_i'), w = (2, 2):  S = (A_t - bH e)^2 - 2 bH^2 e^2 - T_(2,2)(0, e)   (the single form on W = u-perp, e_x-perp);
      mixed (t_i, a_j), (t_i, b_j), w = (2, 1) (the mirrors by C-MIRROR):
        M = (A_t - bH e)(A_a - nBp e) - (pi_t + bH e)(pi_a + nBp e) - (O_t^1/2 + bH e)(v_m + nBm e) - T_(2,1)(0, e),
    with the t inputs as true-vacuum bounds (pk15's rows; FLOAT stand-ins now, t_float_inputs), beta_H H-NORM's full ||B_t||
    bound, A_a S9(b)'s Lemma A amplitude (C-AA), and the mixed x part's sign derived (SIGN).
  - Scan item (c2a_scan, [300, 303]): per N and kind the threshold d^h, the slacks by d, the distances to flip, C-KIND0 with
    PLANT-KIND0, C-MIRROR with PLANT-MIRROR, PLANT-NONX, PLANT-W, PLANT-BH, PLANT-PAIR, the margin plants and the C2-a kill.
  - Sweep item: per piece and kind (and joint class) the smallest d at which it holds at every larger d up to DH_MAX and the headroom
    levels; C2a.1, C2a.2 (claim thresholds), C2a.3 (headroom table, planning thresholds) and C2a.4 (joint classes) per N; the export
    EXPORT_KT_S9H_v1 with C-EXPORT2 (C-DMIN) and PLANT-EXPORT2.
  - Width shift: width_exps gives the S powers of the second-order end terms (bracket terms k + w_a and
    k + w_b, D's k + w_a + w_b, k plain steps strictly between the insertions); tw_abs (the Jensen form, absolute units) and tw_mode
    (the T_w, units of s_x^k) take two sides and two widths; pj, pm, s7mono_hyp, coverage and coverage_claim take w (default
    (1, 1)) and side (default None, the vertical insertion), and at their defaults repeat v2_2's arithmetic operation for operation.
  - C-EXP: the EXPONENT TABLE lines for (w_e, w_f) in (1,1), (2,1), (1,2), (2,2), read from width_exps, and tw_abs and tw_mode at
    rho1 = 1/2, e = 1 against the formulas written out in exact rationals; PLANT-EXP (a swapped power in copies) must fail it.
  - C-WIDTH: v2_2's S7 functions, pinned as one source block (l.936-1015, by sha256), against the fork's width-aware ones at their
    defaults: the claimed-pair coverage tables on every piece, and on sampled pieces the slack values of pj and pm (a variant of each
    block whose final returns give the slack interval instead of its sign) and s7mono_hyp's verdicts, endpoint for endpoint;
    PLANT-WIDTH (D's power over-shifted by one in a copy) must differ.
  - C-VERT: the fork's export rows of the vertical sweep against v2_2's export (2520bfb9, pinned), string for string; PLANT-VERT.
  - The FLOAT t provider: kt_sh1_v1's ENTRY lines (pk15/out/out_kt_sh1_v1_n4.out 7ef515a9, _n3.out dc36d557) with C-HASH, C-FMT
    against the separate reference reader sh1_entry_ref_v1.py (no shared code) and C-SRC (their C-HARM lines PASS, VERDICT VALID, the
    code sha in their headers); PLANT-FMT-SH1 and PLANT-SRC-SH1. pk15's FLOAT bar stand-ins (KT-S9B's r and kt_sh1_v1's O_t) are
    read with their hash and header checks. Its values are not used yet.
  - the review T48 (427dccbe), in every reader of this file: a producing output is accepted only if its VERDICT lines are exactly
    ['VERDICT VALID'] (verdict_lines_ok, by equality, not substring), and a record whose FORMAT, RECORD, END or claim marks it PRECERT
    or STUB is refused (marked_precert); PLANT-PRECERT-S4U, PLANT-PRECERT-S4T and PLANT-PRECERT-SH1.
Everything below is kt_s67_cert_v2_2's, unchanged except where marked P2-11.
kt_s67_cert_v2_2.py (no run without the approval naming this file's sha8) -- pk07 (code/pk07/).
v2_2 of kt_s67_cert_v2_1.py (98cde3a0; runs 42dd5429, 759af4b9), plan and the kbar argument in
FREEZE_NOTE_kt_s67_cert_v2_2.md:
  - (1) endw's r_main enters q as its matrix-tree enclosure in mp.iv (r_main_iv, moved out of C-HARM), not as the
    stored float; C-HARM keeps comparing the two, and PLANT-HARM swaps the closed-form conductances;
  - (2) m2's kbar is a free centering constant of the construction, not an input (the freeze note gives the
    argument from PK10_NOTES 19.5.1, 19.5.4, 19.6.2-3); C-KBAR gates kbar >= 0, u_h >= its centering term and t1 >= kbar (1 + eps_r),
    with PLANT-KBAR;
  - (3) the sweep writes a per-piece export for S8, EXPORT_KT_S67_v1 (S4U_KV_v1), with the J ends
    and pk11's 17 bounds (EXPORT_FIELDS) as directed decimals, the claimed pairs' Jensen and mode indices, the input tags with their
    status and EXPORT_STATUS; C-EXPORT reads it back with both S4U_KV_v1 readers and the sha-pinned producer's reader
    kt_s67_export_reader_v1.py before it is written, with PLANT-EXPORT; the run prints the export's sha256 for the importer's pin.
v2_1 of kt_s67_cert_v2.py (da3837e1; runs b04b2d1a, 5afcd1ce), plan in FREEZE_NOTE_kt_s67_cert_v2_1.md:
  - the S4-TRB provider for pk08's S4_TRB_CERTIFIED_v1 (91109301): C-HASH, C-FMT against the same S4U_KV_v1
    reference parser, C-SRC of N*_TRB, its pieces, PR and T_v against the READING lines of the sha-pinned asm outputs, PLANT-TSRC and
    PLANT-FMT-S4T; the tag 'CERTIFIED pk08 91109301' is set by provide_s4trb only. Ctx.TRB takes the record's N*_TRB, one constant
    per N for every J >= 300 (CONSTANT_PER_N); path A's reproductions keep the FLOAT TRB with the FLOAT U (float_s4). KR4 adds TRB
    (N*_TRB <= 1.02 x the FLOAT TRB, a gate), and C-TARGETS takes the certified TRB in place of its target;
  - N-a, C-TAG expects the run's tags to read CERTIFIED exactly when every input has a pin; N-c, the TARGETS line
    drops "S4-TRB, pending"; N-d, the scan's distances are stated as measured from the certified S4 values (INFO), also in the d = 3
    INFO line. M2 and M3 stay FLOAT (no pin) until pk02's records exist.
v2 (below) was written to pk11's plan PLAN_P2_CERT_FIXES_v1 (ca2637a7). Base: pk11's kt_s67_cert_v1_2.py (e7e973d0), which is v1_1 (b0b30114) with the d = 3 CLAIM
(NOTE1_d3, e64e90cf). v2 is the certified-item revision. It folds in the P2 review (ec33e7dd: F1, F2, S1-S3, N-a to N-c) and
d = 3 review (961b21b3: D1, D2, N-b). The changes, by item:
  - F1: a tag reads certified only as 'CERTIFIED <producer> <sha8>' with that input's pins (tag_certified, an allowlist). Only a
    provider sets it, after its C-HASH, C-FMT, C-SRC and C-POS pass. verdict_word gives CERTIFIED only when every tag is certified,
    FLOAT-PASS otherwise (P4's partial flips). PLANT-TAG has three cases: FLOAT tags, a non-FLOAT non-CERTIFIED tag ('S4-TRB,
    pending'), and a well-formed CERTIFIED tag with a wrong sha8.
  - F2: Ctx.U is U(t) = LEAD_HI (1 + C1_HI t + C2_HI t^2 + C3_HI t^3) + R_CERT per N, from pk08's S4_U_CERTIFIED_v3 (e870cbe5, its
    CLAIM_F2 form; v1_1: v3 replaces v2 b1b6b99b with the same values), through provide_s4u. C-POS
    certifies LEAD_LO, C1_LO, C2_LO, C3_LO > 0, so the HI ends bound U3 from above for t > 0. The dual kind's derivative is LEAD_HI
    (C1_HI + 2 C2_HI t + 3 C3_HI t^2); R_CERT is a constant with zero derivative; point and dual kinds use the same polynomial. KR3 reads N*_QUAD_TW_PART. KR4 and an INFO line bound certified minus float U on every
    piece. The FLOAT U of PARAMS (trt2, rem(170)) stays only for path A's reproductions (C-REPRO, C-REPRO300, C-FLIP170: float_s4)
    and for that comparison.
  - S1, D2: self-calibrating margin plants on [300, 303]: per N for U (additive), R_w and TRB (scale factors) on S7, and at N = 4
    for the d = 3 binding direction (C_1 = c5 / F, bars x F; the loss is required of the flip d = 3 pair). F is the scan's bisected
    flip; each plant needs a hold at F / 1.1 and a loss at 1.1 F (margin_plant, shared, as ADD1's S5 plants). No flip in the
    bracket: DOES NOT FIRE.
  - S2: PLANT-PARITY sets one cross-parity coefficient of the symmetrized copy to 1e-12, and C-PARITY must flag it. C-PARITY gates
    once M3's tag is certified (INFO before).
  - S3: the S4-U reader of the port, with C-HASH, C-FMT against the separate sha-pinned reference parser s4u_kv_ref_v1.py (no shared
    code), C-SRC against s4c_m2ba's C-NORM / C-C123 lines (ball strings, exact *_LO / *_HI = mid -+ rad, R_CERT_RULE) and the plants
    PLANT-FMT-S4U, PLANT-KEYSWAP and PLANT-POS. M2's vacuum tuple and wt, dl, S4-TRB and M3's files keep their FLOAT PARAMS and tags
    until their formats are cited (SPEC sect. 3).
  - N-a: C-MODULE adds pt() and the S4-U provider, readers and tag functions. N-b: PLANT-MVB is judged on S5 Dd, where the bars
    enter at full weight. N-c: M3's tag stays FLOAT; its provider will need a key stating the bars for every J >= 300, t = 0 included.
  - D1: C-FLIP170 runs on the own claim (FLIP170_CLAIM) with C_1 = Cov_1 at [170, 171.7], whatever CLAIM is, and stays a gate;
    the d = 3 distances at [300, 303] are set beside NOTE1_d3's recorded run as INFO. N-b (d = 3): the label in the header and
    OUT_PATH come from this file's own name.
  - D-1, C-SRC also checks N*_PREF2_RE, N*_PREF2_RHO4 and N*_M3_SUM against the READING lines of
    their sha-pinned asm outputs, R_CERT as their exact sum and QUAD_TW_PART by its rule, with PLANT-RSRC; D-2, KR4 (and KR3) are
    gates in both items, and C-TARGETS runs with the certified U in place of its target; D-3, S4-TRB's future reader (comment at
    TAG_PINS); C-POS includes LEAD_LO, and Ctx.U says how the last piece meets t = 0; margin_plant states the search's
    bracket and tolerance; the record pinned is v2 b1b6b99b (v3 e870cbe5 from v1_1 on).
M6 P2: the port of Theorem S's S5 (Prop. 19.3, the binding pair), S6 (Prop. 19.5b) and S7 (Prop. 19.6) on J >= 300, N = 3, 4, per
SPEC_M6_S67_v1_2 (76e14cc3), which folds in the S5 addendum and the two reviews (5f1d091b, 3416f328).
S4-U and, since v2_1, S4-TRB enter through their certified providers. M3's entries and M2's vacuum stay FLOAT-tagged (today's J = 170
entries and parameters, as in P0), so the verdicts read FLOAT-PASS or FAIL until their providers exist (C-TAG).
Arithmetic (SPEC v1_1 sect. 2):
  - mp.iv with outward rounding for everything that enters a verdict;
  - float64 only for the eigh preconditioner (used as an exact matrix), the fixed index order (any choice is valid), the FLOAT providers
    (vac_float; the certified item replaces it) and INFO prints;
  - no numpy.linalg, no libm, no erfc, no fractional power in a verdict path, no python-flint (C-MODULE scans the sources);
  - M-d: finiteness asserts, and a nonnegative quantity whose enclosure lies below 0 stops the evaluation (nn); M-e probes at start
    and end.
Pieces: t = 1/J on [300, 400] at ratio 1.0025, on [400, 1e6] at ratio 1.01, and a last piece [0, 1e-6]. Endpoints are rounded outward:
  t_lo = (1/J_hi).a and t_hi = (1/J_lo).b (RV13_1 N1).
Centered forms (SPEC v1_2 sect. 2): for f in {rho^2, the L1 argument, the L2 argument, S5's even - odd}, f(P) is contained in
  F(t_m) + D(P)[-h, h]; for the three U-sensitive forms the bound used is the smaller of this upper end and the naive one (N-e), for S5
  the intersection of two true enclosures. Here:
  - F(t_m) is the naive value at the point t_m, with the bars; h covers t_m's distance to both ends of the piece;
  - D(P) is d f/dt by forward-mode interval differentiation (class D below), with value inputs c(P) + B and derivative inputs c'(P);
  - the four port conditions hold by construction: one bar box per piece, D(P) without derivatives for delta, the same function and
    constants in F(t_m) and D(P) (fixed index order, constant radius), and a kink or a non-finite D(P) falls back to the naive bound
    (counted, N-d).
  Smooth forms:
  - rho^2 uses sum_i A'_ii^2 (Schur);
  - L1 uses the fixed diagonal i0 and the fixed row iy with the constant radius R_y (N-d), mu_y = A'_yy - R_y. It is used only if
    C-ORDER holds on the whole piece and box: row iy certified as the minimizing Gershgorin row (F2), and A_00, mu_z and A'_yy - R_y
    positive (the form squares them);
  - L2 uses the 2 x 2 (i0, ix) interlacing bound, only if A_00 and mu_z are positive and mu_x's square-root argument stays positive
    (mu_x > 0 is asserted).
  The centered forms remove the t-dependency only; the bars enter F(t_m) at full weight.
Path A, the reference: the author's functions, sliced by line ranges and checked by sha256 before exec:
  - m2_unif3.py l.31-130;
  - endpairs4.py l.31-246;
  - assemble_binding_unif4.py l.19-35 (VQ, KAPPA, chi3, vac) and l.38-78 (item, cov_lower).
Controls, both items (gates unless INFO):
  - C-HASH, C-BLOCK, C-ENV;
  - the S4-U provider (F2, S3): C-HASH on the bytes it parses, C-FMT (the port's reader against the reference parser, every key; the
    header keys as pinned), C-SRC (s4c_m2ba's lines), C-POS; PLANT-FMT-S4U, PLANT-KEYSWAP, PLANT-POS; INFO U at t = 1/300 and t -> 0;
  - C-REPRO at [170, 171.7]: path A rebuilds the author's printed lines (m2_unif3, endpairs4 "J = 170", assemble_unif4) and the review's
    coverage lines; path B (naive enclosures, the author's forms, path A's FLOAT U) equals A to 1e-10 on every S5, S6 and S7 quantity and on all 24
    coverage pairs; path B with the production forms (RV13_1 N3) never beats A beyond 1e-12 (R+, rho, rho1, c_x, c5). This one-sided
    test applies to the naive enclosures: the centered forms are tighter by design and are checked by C-MV and C-PIECE instead.
    PLANT-S2UP (S2_even from the upper ends) fires through the one-sided test, not through the R+/rho check (SPEC v1_1 sect. 4 has it
    backwards: upper ends make rho smaller, so the R+/rho check passes more easily). PLANT-PATHB (sp = 0) fires through the two-sided test;
  - C-C2: the central S5 assembly at t = 0 equals c2 = (N-1)T^2/2 to 1e-10; PLANT-ODDSIGN, PLANT-T;
  - C-HARM (matrix-tree r_main, q^2(t=0)), C-IP3 (a_0, a_1, a_2 to 1e-12);
  - C-PARITY on the cross-parity Gram entries g(0,2), g(1,2), g(2,3): INFO while M3's tag is FLOAT, as today's files are
    unsymmetrized, a gate once it is certified; its control (a symmetrized copy passes) and PLANT-PARITY (S2: the symmetrized copy with
    one coefficient set to 1e-12 must fail) gate. A_2 is the genuine odd amplitude (0.132 at N = 4), not a parity zero, so ADD1 sect. 2's
    mention of it is left out;
  - C-MODULE (source scan of the verdict-path functions and classes; PLANT-MODULE), C-TAG (wording control with control pins;
    PLANT-TAG's three cases, F1);
  - C-FMT (S2): the port's reader against the author's item() on every stored entry; PLANT-FMT (a copy with two coefficient lists
    swapped).
Item sweep: every piece of [300, inf), both N, S5 first (its per-piece c5 is S7's C_1 at m = 1), then S6 and S7 with the interval pass
  tests (the claim check: the first mode success k <= KMAX, then Jensen for m = 1..k with Dm1 < 1) and the Lemma S7-mono (a) hypotheses;
  C-MV on every piece (4 smooth forms x 9 points); C-REPRO300 on every 100th piece and the last; on the binding pieces C-PIECE
  (term-level, naive: halves inside the parent, the parent around its end and midpoint values, no final bound outward beyond 1e-15),
  C-UNIF and C-MV-B (the gradient-sign corners of B); PLANT-RIGHTEND (C-UNIF and C-PIECE), PLANT-MV, PLANT-MVB (B = 0 in F(t_m); it
  must fail S5 Dd, N-b); INFO at the first and last pieces, and the fallback counts; KR1, KR5a (c5 > 0 part), KR5b.
Item scan: distances to flip at [300, 303] (P0's binding width; S5, S6 and S7, both N, naive enclosures) and at the last piece (joint,
  bars, U, TRB); the margin plants from those flips (S1: U, R_w, TRB on S7, both N; D2: C_1 and bars at N = 4 against the flip d = 3
  pair); ADD1's S5 plants (N_delta bar, TRB: S5 holds at F/1.1 and fails at 1.1F); C-FLIP170 (the claim and distances to 1%; D1)
  with the d = 3 regression (INFO); C-TARGETS (F1: the set T2 at lambda = 1 and 1.25 on every piece, naive; certified inputs enter
  with their certified values instead of their targets, SPEC sect. 4); certified minus float U on every piece (F2, INFO); the v1_2
  targets and the single-input headrooms (INFO); KR2, KR3 (the record's QUAD_TW_PART <= 3.9e-4), KR4 (S4-U against T2's +7.8e-4),
  KR5a (joint part), KR-J.
Cost [E]: sweep 70-150 s (1808 piece evaluations in mp.iv, C-MV doubling each), LIM 400; scan 40-100 s (C-TARGETS: 3616 naive piece
  evaluations), LIM 250. One core each, AS 8 GiB, run one after the other in the foreground. The script writes only
  pk07/out/out_<this file's name>_<mode>[_TAG].out (a few kB) and, after a complete sweep, the export as a new file: vsweep
  pk07/out/export_<this file's name>_vsweep[_TAG].kv (EXPORT_KT_S67_v1, about 0.7 MB), sweep
  pk07/out/export_c2a_<this file's name>_sweep[_TAG].kv (EXPORT_KT_S9H_v1, about 0.4 MB). A full sweep reads the vsweep outputs.
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, time, math, hashlib, signal, traceback, json, re, types, inspect
from fractions import Fraction

LABEL = os.path.basename(__file__)[:-3] if os.path.basename(__file__).endswith('.py') else ''   # N-b (d = 3): label and OUT_PATH
if not re.fullmatch(r'[A-Za-z0-9_]{1,40}', LABEL):
    print('bad file name %r for the label' % os.path.basename(__file__))
    sys.exit(2)
if len(sys.argv) < 3 or sys.argv[1] not in ('sweep', 'scan', 'vsweep', 'vscan'):
    print('usage: %s.py sweep|scan|vsweep|vscan LIM [TAG]   (LIM = RLIMIT_CPU soft limit in s, hard LIM + 5; v = VERTICAL only)' % LABEL)
    sys.exit(2)
MODE = sys.argv[1]
VERT = MODE in ('vsweep', 'vscan')      # the Q2: the VERTICAL-only mode reads the S5-S7 inputs alone and writes EXPORT_KT_S67_v1
ITEM = MODE[1:] if VERT else MODE       # the item, sweep or scan, in either mode
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
TAG = sys.argv[3] if len(sys.argv) > 3 else ''
if not (5 <= LIM <= 550) or not (TAG == '' or (TAG.isalnum() and len(TAG) <= 8)):
    print('bad LIM %r (need 5 <= LIM <= 550) or bad TAG %r' % (sys.argv[2], TAG))
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))
STAGE = ['start']

CODEDIR = '/mnt/g2/release/root/code'
SCR = CODEDIR + '/pk10/scripts'
SC = CODEDIR + '/pk10/scratch'
OWN = CODEDIR + '/pk21/p2/s4c'    # PK21 copy (kill test (i) of step 1): outputs in pk21's folder only
OUTD = OWN + '/out'
OUT_PATH = os.path.join(OUTD, 'out_%s_%s%s.out' % (LABEL, MODE, ('_' + TAG) if TAG else ''))   # N-b (d = 3): from the file's name
if not (os.path.isdir(OUTD) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUTD)
        and os.path.realpath(OUTD).startswith(os.path.realpath(OWN) + os.sep)):
    print('output directory check failed for %s' % OUT_PATH)
    sys.exit(2)
FH = open(OUT_PATH, 'x')


def cpu():
    return time.process_time()


def out(line):
    FH.write(line + '\n')
    FH.flush()


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)

FILES = {
    'pk10/scripts/m2_unif3.py': '8a693b9b', 'pk10/scripts/endpairs4.py': '0760d96e', 'pk10/scripts/vacmod2.py': '533546b1',
    'pk10/scripts/assemble_binding_unif4.py': '8e346bb0',
    'pk10/scratch/m2_N4_J170.json.b': '7c0d4316', 'pk10/scratch/m2_N3_J170.json.b': '55da99fd',
    'pk10/scratch/b5_N4_J170.json': 'f19d1e08', 'pk10/scratch/b5_N3_J170.json': '567f5543',
    'pk10/scratch/clT_N4_J170.json': 'cfd2ab7c', 'pk10/scratch/clT_N3_J170.json': '7d62c303',
    'pk10/scratch/binding4_N4_J170.json': '46a47036', 'pk10/scratch/binding4_N3_J170.json': 'f5e90b08',
    'pk10/scratch/endw_N4_J170.json': 'e8b1fe30', 'pk10/scratch/endw_N3_J170.json': '0db59cc3',
    'pk10/scratch/vacres_K3_N4.json': '516b2501', 'pk10/scratch/vacres_K3_N3.json': 'ebcbd08c',
    'pk10/scratch/m2_unif3_N4.txt': '91f6f1a4', 'pk10/scratch/m2_unif3_N3.txt': '643b702d',
    'pk10/scratch/endpairs4_N4.txt': '6b2702ef', 'pk10/scratch/endpairs4_N3.txt': '540b079f',
    'pk10/scratch/assemble_unif4_N4.txt': 'c1a0fc55', 'pk10/scratch/assemble_unif4_N3.txt': '600ee8bf',
    'pk20/rv13/c5/rc_m2_sens_N4.txt': '63af92fe', 'pk20/rv13/c5/rc_m2_sens_N3.txt': '37cf94c7',
    'pk20/rv13/c6/rc_end_sens_N4.txt': '973a64ca', 'pk20/rv13/c6/rc_end_sens_N3.txt': '5ecf4865',
    'pk20/rv13/c6/rc_end_sens.py': '8b496a35', 'pk20/rv13/c5/rc_m2_sens.py': 'f894df02',
    'pk08/S4_U_CERTIFIED_v3.md': 'eb989483', 'pk05/out/s4c_m2ba_n4.out': '553395a3', 'pk05/out/s4c_m2ba_n3.out': '32ade026',
    'pk07/s4u_kv_ref_v1.py': '5a786edb', 'pk11/out/out_kt_s67_cert_v1_1_scan_d3.out': 'd8a514be',
    'pk08/out/px08_m2bb4_n4_asm.out': 'a563d888', 'pk08/out/px08_m2bc3_n4_asm.out': 'f181a623',
    'pk08/out/px08_px03_v4_n4_asm.out': 'f55df592', 'pk08/out/px08_m2bb4_n3_asm.out': '29773c44',
    'pk08/out/px08_m2bc4_n3_asm.out': 'fc41f247', 'pk08/out/px08_px03_v4_n3_asm.out': 'b5c8bb3f',
    'pk08/S4_TRB_CERTIFIED_v1.md': '2c17c287', 'pk08/out/px08_trbcert_v1_1_n4_asm.out': '9d3e8f62',
    'pk08/out/px08_trbcert_v1_1_n3_asm.out': 'ff2d93d0', 'pk07/kt_s67_export_reader_v1.py': 'c697418b',
    'pk07/kt_s67_cert_v2_2.py': 'f3884819', 'pk07/out/export_kt_s67_cert_v2_2_sweep.kv': '6fe9ab65',       # P2-11: C-WIDTH, C-VERT
    'pk15/out/out_kt_sh1_v1_n4.out': '85bcd36e', 'pk15/out/out_kt_sh1_v1_n3.out': 'be79b01a',               # P2-11: FLOAT t inputs
    'pk07/sh1_entry_ref_v1.py': 'd393e431',
    'pk01/out_kt_s9b_v2_n4.out': 'e7ffff8b', 'pk01/out_kt_s9b_v2_n3.out': '3c7b2d2e',            # P2-11: FLOAT bar stand-ins
    'pk08/S4_TRBH_CERTIFIED_v1.md': 'd38cf34c', 'pk08/out/px08_trbhcert_v2_n4_asm.out': '11019b7c',   # v1_1 P-3: beta_H
    'pk08/out/px08_trbhcert_v2_n3_asm.out': '9663347f',
}
FILES_STB = frozenset(('pk15/out/out_kt_sh1_v1_n4.out', 'pk15/out/out_kt_sh1_v1_n3.out', 'pk07/sh1_entry_ref_v1.py',
                       'pk01/out_kt_s9b_v2_n4.out', 'pk01/out_kt_s9b_v2_n3.out', 'pk08/S4_TRBH_CERTIFIED_v1.md',
                       'pk08/out/px08_trbhcert_v2_n4_asm.out', 'pk08/out/px08_trbhcert_v2_n3_asm.out'))
#                         v1_2: the S_TB' inputs among FILES (SH1's outputs and reference parser, KT-S9B's FLOAT bars, the TRB_H
#                         record and its asm outputs); the vertical mode leaves them unread, C-VERT-ONLY gates it
STB_READS = []            # v1_2: the S_TB' providers that ran (each appends its name on entry); C-VERT-ONLY needs it empty
# F2, S3: the S4-U record, its C-FMT reference parser and the C-SRC outputs, by full sha256
S4U = dict(path='pk08/S4_U_CERTIFIED_v3.md', sha256='eb98948365fa35498206c9f1b80c6d98d421f69b9dca6c245f3f2d1198112751',
           producer='pk08', fmt='S4U_KV_v1', record='S4_U_CERTIFIED_v3')       # v1_1, the review v1 P-4: v3 replaces v2 b1b6b99b
S4U_REF = ('pk07/s4u_kv_ref_v1.py', '5a786edb1eb62608ecf7440b70124044d6207d87523b9c957394666ab4448c98')
S4U_SRC = {4: ('pk05/out/s4c_m2ba_n4.out', '553395a32dcfbf62777db22dca6a9e18aaad6d56ab343077c674f98972d8c735'),
           3: ('pk05/out/s4c_m2ba_n3.out', '32ade026f587cf3fc69fff607856eb9887013d741733e318102cb3c73dc5321f')}
# D-1: the asm outputs whose READING lines give the remainder pieces R_CERT sums (the record's N*_PREF2_RE_OUTPUT, N*_PREF2_RHO4_OUTPUT
# and N*_M3_OUTPUT tokens)
S4U_ASM = {(4, 'PREF2_RE'): ('pk08/out/px08_m2bb4_n4_asm.out', 'a563d888dd062b93d7c284c720513687fb619c10d554caa297405881b6c2094b'),
           (4, 'PREF2_RHO4'): ('pk08/out/px08_m2bc3_n4_asm.out', 'f181a623b671c06515207e0e20126e71f13b5d23cb8e7014f34d85375dc78c1d'),
           (4, 'M3_SUM'): ('pk08/out/px08_px03_v4_n4_asm.out', 'f55df5922eb0a026b2d814f2a7c665d7e1ff416a8a6a52aabbd8a90d3bcbd4df'),
           (3, 'PREF2_RE'): ('pk08/out/px08_m2bb4_n3_asm.out', '29773c441cbcb7e72818e4a8379410283a21e8702ca0688ed5277e5c69f1319c'),
           (3, 'PREF2_RHO4'): ('pk08/out/px08_m2bc4_n3_asm.out', 'fc41f24724922f2f7fd3b8d385936254c7550ff01b40408c41e4009c51e00053'),
           (3, 'M3_SUM'): ('pk08/out/px08_px03_v4_n3_asm.out', 'b5c8bb3f56a63b6b1146ec5576ddf16ea5778a8be6bd8e25924c2352de617965')}
# v2_1: the S4-TRB record and the asm outputs whose READING lines it copies, by full sha256
S4T = dict(path='pk08/S4_TRB_CERTIFIED_v1.md', sha256='2c17c287c0affbfe0e0fcbd8097edff2258ea1109d91381d6206a11d4efdd694',
           producer='pk08', fmt='S4U_KV_v1', record='S4_TRB_CERTIFIED_v1')
S4T_ASM = {4: ('pk08/out/px08_trbcert_v1_1_n4_asm.out', '9d3e8f622c6bf01ec26c75dfc414be730dbbfb87761af78b40cca2e75f2db9a2'),
           3: ('pk08/out/px08_trbcert_v1_1_n3_asm.out', 'ff2d93d01bdf2303e51d8d6f0499fd359a872db6f13132fc7d9f95c28aac08fe')}
# v1_1: the TRB_H record for beta_H (closed f49e746c) and its asm outputs, by full sha256
S4H = dict(path='pk08/S4_TRBH_CERTIFIED_v1.md', sha256='d38cf34ca945a40daad639a0517f62d5c1d837f93515f0be29cbc78f3388cb9d',
           producer='pk08', fmt='S4U_KV_v1', record='S4_TRBH_CERTIFIED_v1')
S4H_ASM = {4: ('pk08/out/px08_trbhcert_v2_n4_asm.out', '11019b7c6975e7cab42c497b3d8044c7948ad06345a7fd3654a93691a004e99d'),
           3: ('pk08/out/px08_trbhcert_v2_n3_asm.out', '9663347f9778e7d34af713a20077bbb0b6cfad74cefd987318a6ffee4bf0281b')}
D3_REF = 'pk11/out/out_kt_s67_cert_v1_1_scan_d3.out'     # D1: NOTE1_d3's recorded scan (v1_2 under TAG d3)
# v2_2 (3): the producer's reader of the per-piece export the sweep writes for S8, by full sha256;
# the certified snapshot reads it with the bound reader v2_1 (S8's pin; self-test reader_v2_1_selftest_v1 VALID, runs 2a9716c3)
EXPORT_READER = ('pk07/kt_s67_export_reader_v2_1.py', '4c6949462ca8c5dda337027b7dc5bada51102a063dc5ff6f8a1c2def01eaf49d')
VMODE_PIN = None    # C-VERT-MODES' vertical run: None = this file's own vsweep outputs (same TAG); else (export path, its sha256, run output
                    # path, its sha256), paths from code/, for a full mode in a later file
EXPORT_FIELDS = ('jlo jhi c5_lo vSv_p_lo vSv_m_hi rp_lo rho_hi rho1_hi vp2_lo vp2_hi vm2_hi Bp_hi Bm_hi cx_lo r2_hi ro_hi Rw_hi c_lo '
                 'c_hi')                                     # pk11's list for S8 (its 15 numbers, then c_lo c_hi), after jlo jhi
EXPORT_PAIR_FIELDS = 'kind d m_checked k_mode holds'
EXPORT_ROWS = {4: [], 3: []}
# P2-11 harness: v2_2's S7 functions (pj, pm, s7mono_hyp, coverage, coverage_claim, claim_holds) as one pinned source block, v2_2's
# export for C-VERT, and the FLOAT t inputs (kt_sh1_v1's outputs, header code sha pinned) with their C-FMT reference reader
V22_S7 = ('pk07/kt_s67_cert_v2_2.py', 936, 1015, '7650b7ec726728f15603792a6d2f89b2ababfd86820f4a208cfc0d771e795ac6')
V22_EXPORT = ('pk07/out/export_kt_s67_cert_v2_2_sweep.kv', '6fe9ab65f5207dc3658c98ff4f3696bd2db6aa784b0dec84b33881b2da579c34')
SH1_OUT = {4: ('pk15/out/out_kt_sh1_v1_n4.out', '85bcd36eb029d17473e1f7bc49c5a6668bb739964b018d219ab5165deb57182f'),
           3: ('pk15/out/out_kt_sh1_v1_n3.out', 'be79b01afd9d714da6b0a6d27c9da3bc0fc540292f855db02bb8ad4aec8d9a1c')}
SH1_CODE = 'b7757b7e681f86fc9ac339781d028ee0aa2a8b9999b986a36cfa590643ad742a'      # kt_sh1_v1.py, as both outputs' headers print it
SH1_REF = ('pk07/sh1_entry_ref_v1.py', 'd393e4318001687e1bbe01588d97d15678003f2f014a4e10c0449d4be57f041a')
SH1_NAMES = ('XBT', 'XTB', 'XTT', 'Geps', 'Gxbb,0,0', 'G00|DT', 'Gxt,0,0', 'Gxt,0,1', 'Gxt,0,3', 'Gxt,1,1', 'Gxt,1,3', 'Gxt,3,3',
             'Ihh,0', 'Ihh,1', 'Ihh,3', 'Iht,0', 'Iht,1', 'Iht,3', 'IhTt,0', 'IhTt,1', 'IhTt,3')
WIDTH_STEP = 10                                     # C-WIDTH's slack grid runs on every WIDTH_STEP-th piece and on the last one
# pk15's FLOAT bar stand-ins for the t entries (its answer to Q1): KT-S9B's same-graph h entries, r = rem + tail + ann + far at
# J_REF = 300 radii (pk01's kt_s9b_v2 outputs, header code sha pinned)
S9B_OUT = {4: ('pk01/out_kt_s9b_v2_n4.out', 'e7ffff8b54188e7c114df47e4b44bf382877af2298092edeb018c6ecc35a27cd'),
           3: ('pk01/out_kt_s9b_v2_n3.out', '3c7b2d2e6d461674b11a2e0554f8ce2294de6c644b5922ee722a159a01659cbf')}
S9B_CODE = '710ad713289dd232f2ea51414e99bcb75f8493ba76d664793f256e0b9bcfcbc7'      # kt_s9b_v2.py, as both outputs' headers print it
S9B_NAMES = ('G,0,0', 'G,0,1', 'G,0,3', 'G,1,1', 'G,1,3', 'G,3,3', 'Ih,0', 'Ih,1', 'Ih,3')
BLOCKS = {
    'm2u3': ('pk10/scripts/m2_unif3.py', 31, 130, 'e5ccf3b4d3504b7d2f599d465d6acbffe9e9f3aa381bb2df6dd3a33e3140a63e'),
    'ep4': ('pk10/scripts/endpairs4.py', 31, 246, 'a95912cd172920204ea40b1cb8ea24f231144a55a1b25b4df4b0a5a4dc1c070d'),
    'ab4a': ('pk10/scripts/assemble_binding_unif4.py', 19, 35, '7edaaa88c230f1bc45570eb71370fe5cc22296fa3c12c91b1985016392a6bf85'),
    'ab4b': ('pk10/scripts/assemble_binding_unif4.py', 38, 78, 'af85ba2d045cce877397cda419cdeca8a6b1c18b25802e62a4ba153c7a2cb951'),
}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return sha_bytes(fh.read())
    except OSError:
        return 'MISSING'


def env_probe():
    """M-e: round-to-nearest, no flush-to-zero, no denormals-are-zero (operands built at runtime)."""
    e = math.ldexp(3, -54)
    ok = (1.0 + e == 1.0 + math.ldexp(1, -52)) and (-1.0 - e == -(1.0 + math.ldexp(1, -52)))
    ok = ok and math.ldexp(1, -1074) > 0 and math.ldexp(1, -1022) / 2 != 0
    return ok


out('%s sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d) TAG=%r' % (LABEL, sha_file(os.path.abspath(__file__)), MODE, LIM,
                                                                           LIM, LIM + 5, TAG))          # N-b (d = 3): LABEL
STB_UNREAD = FILES_STB if VERT else frozenset()       # v1_2: the vertical mode does not open the S_TB' files
_bad = [n for n in sorted(FILES) if n not in STB_UNREAD and sha_file(os.path.join(CODEDIR, n))[:8] != FILES[n]]
out('C-HASH %s (%d files%s)%s' % ('PASS' if not _bad else 'FAIL', len(FILES) - len(STB_UNREAD),
                                  '; the %d S_TB\' files left unread in the vertical mode' % len(STB_UNREAD) if STB_UNREAD else '',
                                  (': ' + ', '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
SRC = {}
_badb = []
for _k, (_p, _lo, _hi, _sha) in BLOCKS.items():
    with open(os.path.join(CODEDIR, _p)) as _fh:
        _lines = _fh.read().split('\n')
    SRC[_k] = '\n'.join(_lines[_lo - 1:_hi]) + '\n'
    if sha_bytes(SRC[_k].encode()) != _sha:
        _badb.append(_k)
out('C-BLOCK %s (author slices by sha256)%s' % ('PASS' if not _badb else 'FAIL', (': ' + ', '.join(_badb)) if _badb else ''))
if _badb:
    out('VERDICT INVALID (C-BLOCK)')
    sys.exit(2)

import numpy as np
import scipy.linalg as sla
import mpmath as mp
from scipy.special import erfc
iv = mp.iv
iv.dps = 25
IVT = type(iv.mpf(1))
_env0 = env_probe()
out('C-ENV start: %s (numpy %s, mpmath %s, python %s)' % ('PASS' if _env0 else 'FAIL', np.__version__, mp.__version__, sys.version.split()[0]))
if not _env0:
    out('VERDICT INVALID (C-ENV)')
    sys.exit(2)

# ------------------------------------------------------------------ inputs (FLOAT providers; tags)
# PARAMS: the FLOAT inputs of M2 (vac, wt, dl) and the J >= 170 Cov_1, which the verdicts still use until their providers exist (S3);
# trt2, S4's FLOAT U, and TRB, S4's FLOAT TRB, serve since v2 and v2_1 only path A's reproductions (float_s4) and the KR4 comparisons:
# the verdicts take U from provide_s4u (F2) and TRB from provide_s4trb (v2_1).
PARAMS = {
    4: dict(TRB='1.312607', vac=(2.6744e-06, 1.6450e-04, 4.2950e-06, 7.4706e-06, 3.837e-10, 1.1950e-06, 7.250e-11, 1.8816e-05, 0.999993,
                                 1.332042, 0.360),
            wt=(3.4712e-06, 5.287e-05, 7.487e-06, 170.0), dl=(2.4733e-06, 5.027e-05, 6.219e-06, 170.0),
            trt2=(1.0302393041, 0.846041, 0.639530, 0.498940, 6.509e-4), cov1=1.1765e-4),
    3: dict(TRB='0.942262', vac=(1.1426e-06, 5.2050e-05, 1.9050e-06, 2.5677e-06, 1.361e-10, 6.2950e-07, 5.250e-17, 1.4354e-05, 0.999998,
                                 1.331271, 0.360),
            wt=(1.2665e-06, 1.631e-05, 3.322e-06, 170.0), dl=(9.8425e-07, 1.515e-05, 2.752e-06, 170.0),
            trt2=(1.0302393041, 0.742488, 0.53795, 0.43804, 1.592e-4), cov1=2.2043e-4),
}
TAGS = {'M3 entries': 'FLOAT (pk10/scratch J = 170 JSONs)', 'M2 vacuum': 'FLOAT (vacscale parameters, rc_end_sens d3e142f3)',
        'S4 U': 'FLOAT (trace polynomial and rem(170))', 'S4 TRB': 'FLOAT (twrig4 at J = 170)'}
# F1: the pins of the inputs that have a provider. A tag reads certified only as 'CERTIFIED <producer> <sha8>' with these (tag_certified),
# and only the provider sets it (provide_s4u, provide_s4trb). M3 and M2 have no provider in v2_1, so no pin: their tags cannot read
# certified. D-3 (v2_1): S4-TRB's provider has C-HASH and C-FMT against the same S4U_KV_v1 reference parser, and C-SRC.
TAG_PINS = {'S4 U': (S4U['producer'], S4U['sha256'][:8]), 'S4 TRB': (S4T['producer'], S4T['sha256'][:8])}
CXI = 0.6594
VQ = [0.66767, 0.56373]
KAPPA = 0.41729
DS = list(range(0, 9)) + [10, 12, 15, 20]
MMAX, KMAX = 3000, 60
CLAIM = {4: (('flip', 3), ('same', 1)), 3: (('flip', 3), ('same', 1))}
FLIP170_CLAIM = {4: (('flip', 4), ('same', 1)), 3: (('flip', 3), ('same', 1))}   # D1: the own claim at J = 170, for C-FLIP170 only
TOL_B = 1e-10
MCAP = 2048.0


def jl(name):
    with open(os.path.join(SC, name)) as fh:
        return json.load(fh)


def load(N, S4, ST, M3, M2B, VAC):
    """this N's inputs; U5 is the S4-U provider's U tuple (F2), quad and umf the record's N*_QUAD_TW_PART and N*_U_MINUS_FLOAT; TRBv
    is the S4-TRB provider's N*_TRB as an exact-decimal enclosure and trb its string (v2_1); r_iv is r_main by the matrix-tree theorem
    in mp.iv (v2_2 (1)). M2, B5, CT, B4 and EW are the M3 provider's records (their JSON), balls their entries as mp.iv balls
    (Ctx.entry's certified path), FLOAT_M3 the FLOAT J = 170 JSONs that path A and the reproductions read (float_s4). M2B is the M2(b)
    provider's LAW v1 keys (vac_terms takes LAW v1 from them). mser is the symmetrized trial vacres of TRIAL_SET, the file the M3
    records name (C-TRIAL); mser_float the author's pk10 vacres, which the FLOAT reproductions keep (float_m3; the same m1..m3)."""
    return dict(N=N, M2=M3[N]['M2'], B5=M3[N]['B5'], CT=M3[N]['CT'], B4=M3[N]['B4'], EW=M3[N]['EW'], balls=M3[N]['balls'],
                FLOAT_M3=M3[N]['FLOAT_M3'], m3_cert=M3[N]['m3_cert'], mser=VAC[N], mser_float=jl('vacres_K3_N%d.json' % N), P=PARAMS[N],
                M2B=M2B[N], U5=S4['U5'][N], quad=S4['quad'][N], umf=S4['umf'][N], TRBv=ST['TRBv'][N], trb=ST['trb'][N],
                r_iv=r_main_iv(N))


def float_m3(inp):
    """the same inputs with the M3 entries back on the FLOAT J = 170 JSONs, no balls and the FLOAT vacuum (vac_float; v2_2's inputs:
    certified S4, FLOAT M3 and M2); C-VERT compares the export rows of these inputs, on sampled pieces, with v2_2's export."""
    return dict(inp, balls={}, M2B=None, m3_cert=False, mser=inp['mser_float'], **inp['FLOAT_M3'])


def float_s4(inp):
    """the same inputs with S4's FLOAT U (PARAMS trt2: lead, c1, c2, c3, rem(170)) and FLOAT TRB (PARAMS TRB), path A's: for the
    reproductions of the author's lines and of the distances (C-REPRO, C-REPRO300, C-FLIP170) and for the KR4 comparison (F2;
    v2_1 adds TRB, which was float_u's U only in v2). The M3 entries go back to the FLOAT J = 170 JSONs (float_m3), so path B reads the
    same entries as path A (the certified snapshot's M3 provider)."""
    return dict(float_m3(inp), U5=inp['P']['trt2'], TRBv=inp['P']['TRB'])


def path_a(inp, which):
    """the author's slices in a fresh namespace with this N's inputs ('m2u3', 'ep4', or 'ab4' = l.19-35 then l.38-78); the M3 entries
    are the FLOAT J = 170 JSONs (float_s4), as the author's scripts read them."""
    inp = float_s4(inp)
    P = inp['P']
    ns = dict(math=math, json=json, np=np, sla=sla, mp=mp, iv=iv, erfc=erfc, sys=types.SimpleNamespace(argv=[]), NN=inp['N'], J1=170.0,
              kbar=inp['M2']['kbar'], mser=inp['mser'], M2=inp['M2'], B5=inp['B5'], CT=inp['CT'], B4=inp['B4'], EW=inp['EW'],
              TRB=mp.mpf(P['TRB']), cxi=CXI, COV1=P['cov1'], RATIO=1.01)
    for k, v in zip(('nP', 'D5', 'R0', 'tX', 'tB', 'ann', 'far', 'gB', 'z2', 'Rtr', 'ae'), P['vac']):
        ns[k] = v
    for k, v in zip(('nPwM', 'D5w', 'R0w', 'J0w'), P['wt']):
        ns[k] = v
    for k, v in zip(('nPdM', 'D5d', 'R0d', 'J0d'), P['dl']):
        ns[k] = v
    for k, v in zip(('lead', 'c1', 'c2', 'c3', 'remT'), P['trt2']):
        ns[k] = v
    if which == 'ab4':
        ns['cxi'] = mp.mpf(repr(CXI))
        exec(compile(SRC['ab4a'], BLOCKS['ab4a'][0] + ':19-35', 'exec'), ns)
        exec(compile(SRC['ab4b'], BLOCKS['ab4b'][0] + ':38-78', 'exec'), ns)
    else:
        exec(compile(SRC[which], BLOCKS[which][0], 'exec'), ns)
    return ns


# ------------------------------------------------------------------ interval helpers and forward-mode differentiation
def pt(x):
    """a point interval (exact for floats, ints, strings rounded outward)."""
    return x if isinstance(x, IVT) else iv.mpf(x)


def ivlo(x):
    return pt(x).a


def ivhi(x):
    return pt(x).b


def isect(x, y):
    a = x.a if (x.a > y.a) is True else y.a
    b = x.b if (x.b < y.b) is True else y.b
    if (a > b) is True:
        raise AssertionError('empty intersection of two enclosures')
    return iv.mpf([a, b])


def finite(x, what):
    """M-d: an enclosure must have finite ends."""
    s = str(x)
    if 'inf' in s or 'nan' in s:
        raise ArithmeticError('non-finite %s: %s' % (what, s))
    return x


def pmax(xs):
    """the largest of point intervals, by exact comparison."""
    best = xs[0]
    for x in xs[1:]:
        if (x > best) is True:
            best = x
    return best


def pmin(xs):
    """the smallest of point intervals, by exact comparison (ties keep the first, which is equal)."""
    best = xs[0]
    for x in xs[1:]:
        if (x < best) is True:
            best = x
    return best


def contains(outer, inner):
    return (inner.a >= outer.a) is True and (inner.b <= outer.b) is True


class D:
    """value and t-derivative, both mp.iv intervals."""
    __slots__ = ('v', 'd')

    def __init__(self, v, d=0):
        self.v = pt(v)
        self.d = pt(d)

    def __add__(s, o):
        o = lift(o)
        return D(s.v + o.v, s.d + o.d)

    __radd__ = __add__

    def __sub__(s, o):
        o = lift(o)
        return D(s.v - o.v, s.d - o.d)

    def __rsub__(s, o):
        return lift(o) - s

    def __mul__(s, o):
        o = lift(o)
        return D(s.v * o.v, s.d * o.v + s.v * o.d)

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = lift(o)
        q = s.v / o.v
        return D(q, (s.d - q * o.d) / o.v)

    def __rtruediv__(s, o):
        return lift(o) / s

    def __neg__(s):
        return D(-s.v, -s.d)

    def __pow__(s, k):
        assert isinstance(k, int) and k >= 1
        r = s
        for _ in range(k - 1):
            r = r * s
        return r


def lift(x):
    return x if isinstance(x, D) else D(x, 0)


def dsum(xs):
    """a sum with no interval start value: mp.iv raises (it does not return NotImplemented) when a dual number is its right operand."""
    r = None
    for x in xs:
        if r is None:
            r = x
        elif isinstance(x, D) and not isinstance(r, D):
            r = x + r
        else:
            r = r + x
    return pt(0) if r is None else r


def nn(x, what):
    """[0, x.b] for a quantity that is >= 0 by construction (the author's max(., 0) keeps only the upper end); an enclosure entirely
    below 0 is an input inconsistency and stops the evaluation (M-d)."""
    if (x.b < 0) is True:
        raise ArithmeticError('the enclosure of the nonnegative %s lies below 0' % what)
    return iv.mpf([0, x.b])


def sqrt_any(x):
    if isinstance(x, D):
        r = iv.sqrt(x.v)
        return D(r, x.d / (2 * r))
    return iv.sqrt(pt(x))


def chol(G, m):
    L = [[pt(0)] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1):
            s = G[i][j] - dsum((L[i][k] * L[j][k] for k in range(j)))
            L[i][j] = sqrt_any(s) if i == j else s / L[j][j]
    return L


def lsolve(L, b, m):
    w = [pt(0)] * m
    for i in range(m):
        w[i] = (b[i] - dsum((L[i][k] * w[k] for k in range(i)))) / L[i][i]
    return w


def congruent(L, A, m):
    Y = [[pt(0)] * m for _ in range(m)]
    for j in range(m):
        for i in range(m):
            Y[i][j] = (A[i][j] - dsum((L[i][k] * Y[k][j] for k in range(i)))) / L[i][i]
    Ap = [[pt(0)] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            Ap[i][j] = (Y[i][j] - dsum((L[j][k] * Ap[i][k] for k in range(j)))) / L[j][j]
    return Ap


# ------------------------------------------------------------------ pieces
def pieces():
    out_ = []
    J = 300.0
    while J < 1e6:
        Jn = J * (1.0025 if J < 400.0 else 1.01)
        out_.append((J, Jn))
        J = Jn
    out_.append((J, None))
    return out_


def t_interval(Jlo, Jhi):
    """outward: [(1/J_hi).a, (1/J_lo).b], or [0, (1/J_lo).b] for the last piece."""
    hi_ = (pt(1) / pt(Jlo)).b
    lo_ = pt(0) if Jhi is None else (pt(1) / pt(Jhi)).a
    return iv.mpf([lo_, hi_])


# ------------------------------------------------------------------ entries as naive intervals, point values or dual numbers
class Ctx:
    """one N and one piece: entry and polynomial evaluation in the kinds 'naive' (over tI, with bars), 'point' (at t_m, with bars) and
    'dual' (value c(tI) + B, derivative c'(tI)); 'cnaive', 'central' and 'cdual' are the same without bars; 'offset' is a point input
    c(t_m) + delta at a corner of the bar box (C-MV-B). sc holds the scan hooks and the plants."""

    def __init__(self, inp, Jlo, Jhi, sc):
        self.inp, self.Jlo, self.Jhi, self.sc = inp, Jlo, Jhi, sc
        self.tI = t_interval(Jlo, Jhi)
        self.tm = self.tI.mid                                   # the rounded midpoint, inside tI; h covers its distance to both ends
        self.h = iv.mpf([0, pmax([pt((self.tm - self.tI.a).b), pt((self.tI.b - self.tm).b)])])
        self.tc = 1.0 / Jlo
        self.cache = {}

    def tvar(self, kind):
        """t for the kind: the point t_m, or the piece tI (PLANT-RIGHTEND: its right end in J, t = t_lo, for the naive kind)."""
        if kind in ('point', 'central', 'offset'):
            return self.tm
        if kind in ('naive', 'cnaive') and self.sc.get('right_end'):
            return iv.mpf([self.tI.a, self.tI.a])
        return self.tI

    def bar(self, src, name, d):
        """the bar's upper end: the stored components summed outward, times the scan hooks (all 1 outside the scans)."""
        sc = self.sc
        m = sc.get('bar_all', 1.0)
        if (src == 'B5' and name.startswith('g,')) or src == 'CT':
            m *= sc.get('bar_ritz', 1.0)
        if src == 'B5' and name.startswith('A,'):
            m *= sc.get('bar_amp', 1.0)
        if src in ('M2', 'B5', 'B4') and name in ('I3p', 'Ip3', 'Nw', 'Ndel', 'I_N'):
            m *= sc.get('bar_' + name, 1.0)
        if src == 'EW':
            m *= sc.get('bar_endw', 1.0)
        ball = self.inp.get('balls', {}).get((src, name))
        if ball is not None:                       # the M3 provider's record: err_b, the bar without rnd (the ball holds the a_k radii)
            e = ball[1]
        else:
            e = pt(d['err']) if 'err' in d else sum((pt(v) for v in d['B'].values()), pt(0))
        return (e * m).b

    def cmul(self, src, name):
        sc = self.sc
        if src == 'M2' and name == 'I3p':
            return 1.0 - sc.get('I3p_c', 0.0)
        if src == 'M2' and name == 'Ip3':
            return 1.0 + sc.get('Ip3_c', 0.0)
        if src == 'M2' and name == 'Nw':
            return 1.0 - sc.get('Nw_c', 0.0)
        return 1.0

    def entry(self, src, name, kind='naive'):
        key = (src, name, kind)
        if key in self.cache:
            return self.cache[key]
        d = self.inp['B4'][name] if src == 'B4' else self.inp[src]['items'][name]
        c = pt(self.cmul(src, name))
        ball = self.inp.get('balls', {}).get((src, name))
        ak = [x * c for x in ball[0]] if ball is not None else [pt(a) * c for a in d['ak']]   # certified: [LO_k, HI_k]
        e = self.bar(src, name, d)
        if kind == 'offset':                       # C-MV-B: a corner of the bar box, sc['offsets'][(src, name)] in {-1, 0, 1} times the bar
            B = e * self.sc.get('offsets', {}).get((src, name), 0)
        else:
            B = iv.mpf([-e, e]) if kind in ('naive', 'point', 'dual') else pt(0)
        t = self.tvar(kind)
        val = sum((ak[k] * t ** k for k in range(len(ak))), pt(0)) + B
        if kind in ('dual', 'cdual'):
            der = sum((k * ak[k] * self.tI ** (k - 1) for k in range(1, len(ak))), pt(0))
            r = D(val, der)
        else:
            r = val
        self.cache[key] = r
        return r

    def poly(self, coeffs, kind='naive'):
        """sum c_k t^k for t-polynomials such as m-hat and U's polynomial part."""
        cs = [pt(c) for c in coeffs]
        t = self.tvar(kind)
        val = sum((cs[k] * t ** k for k in range(len(cs))), pt(0))
        if kind in ('dual', 'cdual'):
            return D(val, sum((k * cs[k] * self.tI ** (k - 1) for k in range(1, len(cs))), pt(0)))
        return val

    def mhat(self, kind='naive'):
        ms = self.inp['mser']
        return self.poly([1.0, ms['m1'], ms['m2'], ms['m3']], kind)

    def U(self, kind='naive'):
        """F2: U(t) = lead (1 + c1 t + c2 t^2 + c3 t^3) + rem from the tuple inp['U5']: the S4-U provider's (LEAD_HI, C1_HI, C2_HI, C3_HI,
        R_CERT), or path A's FLOAT tuple under float_s4. The dual kind's derivative is lead (c1 + 2 c2 t + 3 c3 t^2); rem is a constant
        with zero derivative (port condition (ii)); point and dual kinds use the same polynomial (condition (iii)). The record's
        CLAIM_F2 holds for t in (0, 1/300]; the last piece [0, (1/J_lo).b] meets t = 0 only as the closure of that range, where the
        bound is its limit LEAD_HI + R_CERT (the record's U_T_RULE_AT_0)."""
        lead, c1, c2, c3, remT = self.inp['U5']
        ld = pt(lead)
        pu = self.poly([ld, ld * pt(c1), ld * pt(c2), ld * pt(c3)], kind)
        rest = pt(remT) * self.sc.get('remT', 1.0) + self.sc.get('U_add', 0.0)
        return pu + rest

    def TRB(self):
        """v2_1: inp['TRBv'], the S4-TRB provider's N*_TRB as an exact-decimal enclosure (one constant per N for every J >= 300, the
        record's CONSTANT_PER_N), or path A's FLOAT decimal under float_s4, enclosed outward; only its upper end enters beta."""
        return pt(self.inp['TRBv']) * self.sc.get('TRB', 1.0)


def chi3(s, N):
    return math.exp(-s / 2) if N == 3 else erfc(math.sqrt(s / 2)) + math.sqrt(2 * s / math.pi) * math.exp(-s / 2)


def vac_float(inp, J, sc):
    """the M2 FLOAT vacuum terms at the piece's left end (the author's vac(J) with hooks); returned as point intervals."""
    N = inp['N']
    nP, D5, R0, tX, tB, ann, far, gB, z2, Rtr, ae = inp['P']['vac']
    k = sc.get('vac_all', 1.0)
    nP, D5, R0, tX, tB, ann, far, gB = (x * k for x in (nP, D5, R0, tX, tB, ann, far, gB))
    D5 *= sc.get('D5', 1.0)
    gB *= sc.get('gB', 1.0)
    s_ = 150.0 / J
    dec = math.exp(-0.3 * ae * (J - 150) / 2)
    tBJ = tB * max(math.sqrt(chi3(J * KAPPA / v, N) / chi3(150 * KAPPA / v, N)) for v in VQ)
    tails = (tX + ann) * dec + tBJ
    near = nP * s_ ** 2 + (D5 + R0) * s_ ** 5 + tails
    fJ = far * (J / 150.0) ** 2 * math.exp(-0.5 * 0.3025 * (J - 150))
    g = gB * (J / 150.0) * math.exp(-0.95 * (1 - math.cos(math.radians(40))) * (J - 150) / 2)
    eps = (math.sqrt(near ** 2 + fJ) + g) / math.sqrt(z2)
    s = eps / (2 - Rtr - eps)

    def wres(cw, Wg):
        return (math.sqrt((cw * J * near) ** 2 + (Wg * J) ** 2 * fJ) + Wg * J * g) / math.sqrt(z2)

    def ew(nPM, D5x, R0x, J0, cw, Wg):
        sw = J0 / J
        nw = nPM * sw ** 2 + (D5x + R0x) * sw ** 5 + cw * J * tails
        return (math.sqrt(nw ** 2 + (Wg * J) ** 2 * fJ) + Wg * J * g) / math.sqrt(z2)
    kw = sc.get('eps_w', 1.0)
    return dict(eps_r=pt(eps), s=pt(s), eps_a=pt(wres(CXI, 2.0) * sc.get('eps_a', 1.0)), eps_ds5=pt(wres(CXI / 2, 1.0) * sc.get('eps_ds5', 1.0)),
                eps_w=pt(ew(*inp['P']['wt'], CXI, 2.0) * kw), eps_d=pt(ew(*inp['P']['dl'], CXI / 2, 1.0) * kw), tag=TAGS['M2 vacuum'])


# ------------------------------------------------------------------ the Ritz blocks and the U-sensitive differences
def ritz_basis(cx):
    """the float eigh preconditioners at t_c (exact matrices afterwards)."""
    Ub = {}
    for idx, nm in (([0, 1, 3], 'even'), ([2], 'odd')):
        kg = lambda a, b: 'g,%d,%d' % (min(a, b), max(a, b))
        kt = lambda a, b: 'T,%d,%d' % (min(a, b), max(a, b))
        cen = lambda d: sum(a * cx.tc ** k for k, a in enumerate(d['ak']))
        Gc = np.array([[cen(cx.inp['B5']['items'][kg(a, b)]) for b in idx] for a in idx])
        Tc = np.array([[cen(cx.inp['CT']['items'][kt(a, b)]) for b in idx] for a in idx])
        nu, Uv = sla.eigh(Tc, Gc)
        Ub[nm] = (idx, [[pt(float(Uv[i, j])) for j in range(len(idx))] for i in range(len(idx))])
    return Ub


def ritz_matrix(cx, Ub, nm, kind):
    """L^-1 (U^T T U) L^-T with L = chol(U^T G U), U the exact preconditioner; the congruence as U^T (X U), which gives the same
    enclosure as the termwise sum (each stored entry still enters each product once). Cached per piece and kind."""
    key = ('rm', nm, kind)
    if key in cx.cache:
        return cx.cache[key]
    idx, Ui = Ub[nm]
    m = len(idx)
    kg = lambda a, b: 'g,%d,%d' % (min(a, b), max(a, b))
    kt = lambda a, b: 'T,%d,%d' % (min(a, b), max(a, b))
    GI = [[cx.entry('B5', kg(idx[a], idx[b]), kind) for b in range(m)] for a in range(m)]
    TI = [[cx.entry('CT', kt(idx[a], idx[b]), kind) for b in range(m)] for a in range(m)]

    def cg(X):
        W = [[dsum((X[a][b] * Ui[b][j] for b in range(m))) for j in range(m)] for a in range(m)]
        return [[dsum((W[a][j] * Ui[a][i] for a in range(m))) for j in range(m)] for i in range(m)]
    Mm, Am = cg(GI), cg(TI)
    r = congruent(chol(Mm, m), Am, m)
    cx.cache[key] = r
    return r


def gersh_lo(Ap, i, m):
    """A'_ii - sum_{j != i} |A'_ij| as an interval (naive)."""
    r = sum((abs(Ap[i][j]) for j in range(m) if j != i), pt(0))
    return Ap[i][i] - r, r


def order_from_central(cx, Ub):
    """the fixed index choices (i0 top, ix second, iy lowest) from the central diagonal at t_m. Any fixed choice gives valid bounds for
    mu_0 and mu_x; iy's Gershgorin row is used only after C-ORDER (in quantities) shows its disc lowest on the whole piece and box."""
    if 'order' not in cx.cache:
        Ac = ritz_matrix(cx, Ub, 'even', 'central')
        cen = [float(Ac[i][i].mid) for i in range(3)]
        o = sorted(range(3), key=lambda i: cen[i])
        cx.cache['order'] = (o[2], o[1], o[0])
    return cx.cache['order']


def radius_const(cx, Ub):
    """N-d: the fixed row iy's Gershgorin radius as a constant on the piece, the naive upper end of sum_{j != iy} |A'_iy,j| over P x B.
    Shared by every kind of the piece (condition (iii)); sub-contexts of the same piece receive it."""
    if 'R_iy' not in cx.cache:
        iy = order_from_central(cx, Ub)[2]
        cx.cache['R_iy'] = pt(gersh_lo(ritz_matrix(cx, Ub, 'even', 'naive'), iy, 3)[1].b)
    return cx.cache['R_iy']


def udiffs(cx, Ub, kind):
    """the three U-sensitive differences as smooth functions (fixed index choices from the central diagonal), plus what the naive bound
    adds; kind 'naive'|'point'|'dual'|'central'|'cdual'."""
    Ae = ritz_matrix(cx, Ub, 'even', kind)
    Ao = ritz_matrix(cx, Ub, 'odd', kind)
    U = cx.U(kind)
    diag = [Ae[i][i] for i in range(3)]
    f_rho2 = U - dsum((x * x for x in diag))
    i0, ix, iy = order_from_central(cx, Ub)
    a_, c_, b_ = Ae[i0][i0], Ae[ix][ix], Ae[i0][ix]
    mux = (a_ + c_) / 2 - sqrt_any(((a_ - c_) / 2) ** 2 + b_ * b_)
    muz = Ao[0][0]
    f_L1s = U - Ae[i0][i0] ** 2 - (Ae[iy][iy] - radius_const(cx, Ub)) ** 2 - muz ** 2      # N-d: mu_y = A'_yy - R_y, R_y constant
    f_L2 = U - Ae[i0][i0] ** 2 - mux ** 2 - muz ** 2
    return dict(Ae=Ae, Ao=Ao, U=U, f_rho2=f_rho2, f_L1s=f_L1s, f_L2=f_L2, i0=i0, ix=ix, iy=iy, mux=mux, muz=muz)


def ud_kind(cx, Ub, kind):
    key = 'ud_' + kind
    if key not in cx.cache:
        cx.cache[key] = udiffs(cx, Ub, kind)
    return cx.cache[key]


def centered(cx, Ub, key, naive_val):
    """the upper end of a U-sensitive difference over the piece and box, as a point: the smaller of the naive bound's and of
    [F(t_m) + D(P)[-h, h]] (SPEC v1_2 sect. 2, N-e). Where F(t_m) or D(P) is not finite, or the evaluation meets a kink, the naive upper
    end is used and the fallback is counted (N-d)."""
    try:
        Fm = ud_kind(cx, Ub, 'point')[key]
        Dp = ud_kind(cx, Ub, 'dual')[key]
        cen = finite(Fm + finite(Dp.d, 'D(P) of ' + key) * cx.h * iv.mpf([-1, 1]), key)
    except (ArithmeticError, ValueError, ZeroDivisionError):
        cx.cache['fallbacks'] = cx.cache.get('fallbacks', 0) + 1
        return pt(naive_val.b), None
    return pmin([naive_val.b, cen.b]), cen


MV_KEYS = ('f_rho2', 'f_L1s', 'f_L2', 'S5 Dd')


def mv_values(cx, Ub, kind):
    """the four smooth functions of the centered forms (bar-free kinds 'central' and 'cdual'), with the piece's fixed index order."""
    r = dict(udiffs(cx, Ub, kind))
    r['S5 Dd'] = s5_parts(cx, dict(eps_ds5=pt(0)), kind)['Dd']
    return r


def mv_check(cx, Ub, zero_derivative=False):
    """C-MV: each bar-free f_c at 9 equispaced points of the piece lies in f_c(t_m) + D_c(P)[-h, h]; returns the keys that fail.
    zero_derivative is PLANT-MV (D_c replaced by 0)."""
    fm = mv_values(cx, Ub, 'central')
    dc = mv_values(cx, Ub, 'cdual')
    enc = {k: fm[k] + (pt(0) if zero_derivative else dc[k].d) * cx.h * iv.mpf([-1, 1]) for k in MV_KEYS}
    bad = set()
    for j in range(9):
        tj = cx.tI.a + (cx.tI.b - cx.tI.a) * j / 8
        sub = Ctx(cx.inp, cx.Jlo, cx.Jhi, cx.sc)
        sub.tm = iv.mpf([tj.a, tj.a])
        sub.cache['order'] = order_from_central(cx, Ub)
        sub.cache['R_iy'] = radius_const(cx, Ub)
        fj = mv_values(sub, Ub, 'central')
        bad.update(k for k in MV_KEYS if not contains(enc[k], fj[k]))
    return sorted(bad)


# ------------------------------------------------------------------ S6 and S7 quantities (rigorous intervals; naive form = P0 path B)
def quantities(cx, Ub, V, use_centered=True):
    inp, sc = cx.inp, cx.sc
    mh = cx.mhat()
    er = V['eps_r']
    s = V['s']
    if sc.get('drop_sp'):
        s = pt(0)
    c = iv.sqrt(1 - s * s)
    sp = s * iv.sqrt(2 / (1 + c))
    kbar = pt(inp['M2']['kbar'])
    g00 = cx.entry('M2', 'g00')
    gb00 = cx.entry('B5', 'g,0,0')
    alpha = cx.entry('B5', 'A,0') / (mh * gb00)
    Bu2 = (2 * cx.entry('B5', 'Ia') / mh - cx.entry('B5', 'Na')) / gb00 + iv.mpf([0, (V['eps_a'] ** 2).b])
    vtr = iv.sqrt(nn(Bu2 - alpha ** 2, 'Bu2 - alpha^2'))
    Dm = cx.TRB() - alpha
    beta = pt(((alpha + Dm) / 2 + iv.sqrt(((Dm - alpha) / 2) ** 2 + vtr ** 2)).b)
    kb = pt((kbar * (1 + er)).b)
    Bop = pmax([beta, kb])
    nv = udiffs(cx, Ub, 'naive')
    Ae, Ao = nv['Ae'], nv['Ao']
    s2end = (lambda x: x.b) if sc.get('s2_upper') else (lambda x: x.a)                  # PLANT-S2UP takes S2_even from the upper ends
    de = [pt(0) if (Ae[i][i].a < 0) is True else pt(s2end(Ae[i][i])) for i in range(3)]
    gl = [gersh_lo(Ae, i, 3)[0] for i in range(3)]
    mu0 = pmax(de)
    muy_n = pmin([pt(g.a) for g in gl])
    muy_n = pt(0) if (muy_n < 0) is True else muy_n
    muz = pt(0) if (Ao[0][0].a < 0) is True else pt(Ao[0][0].a)
    U = cx.U()
    rho2_n = U - sum((x * x for x in de), pt(0))
    L1s_n = U - mu0 ** 2 - muy_n ** 2 - muz ** 2
    rho2, L1arg = rho2_n, L1s_n
    order_ok = None
    if use_centered:
        rho2, _ = centered(cx, Ub, 'f_rho2', rho2_n)                     # Schur: valid whatever the signs
        i0, iy = nv['i0'], nv['iy']
        gy = gersh_lo(Ae, iy, 3)[0]
        # C-ORDER (F2, E4): row iy certified as the minimizing Gershgorin row (up(g_iy) < lo(g_j)), and A_00, mu_z and A_yy - R_y positive
        # on the whole piece and box, since the smooth L1 form squares them; otherwise L1 keeps its naive bound (the minimum over rows)
        order_ok = ((Ae[i0][i0].a > 0) is True and (Ao[0][0].a > 0) is True and ((Ae[iy][iy] - radius_const(cx, Ub)).a > 0) is True
                    and all((gersh_lo(Ae, j, 3)[0].a > gy.b) is True for j in range(3) if j != iy))
        if order_ok:
            L1arg, _ = centered(cx, Ub, 'f_L1s', L1s_n)
    L1o = iv.sqrt(nn(rho2, 'rho^2 lambda_0^2'))
    L1 = iv.sqrt(nn(L1arg, 'the L1 argument'))
    L1 = L1 if (L1.b >= L1o.b) is True else L1o
    L1 = pt(L1.b)
    L1o = pt(L1o.b)
    lam0 = pt((mh * (1 - er)).a) if sc.get('author_forms') else pt((mh * (1 - er / c)).a)   # RV13_1/C5/C6 n1 (N3)
    lam0 = pmax([mu0, lam0])
    rho1 = pt((L1 / lam0).b)
    rho = pt((L1o / lam0).b)
    HT = cx.entry('M2', 'I3p') / (g00 * mh)
    Nw = cx.entry('M2', 'Nw')
    ew = V['eps_w']
    Dn2 = (2 * cx.entry('M2', 'Ip3') / mh - Nw) / g00 + ew ** 2
    Dn = iv.sqrt(nn(Dn2, 'Dn^2'))
    uh = abs(cx.entry('M2', 'kn') - kbar * g00) / g00 + sp * iv.sqrt(Nw / g00)
    ua = abs(cx.entry('M2', 'A0w')) / (mh * g00) + sp * Dn
    NT2 = pt((HT - 2 * ew * (iv.sqrt(L1 * HT / mh) + (1 + er) * uh) - (1 + er) * ua ** 2).a)
    nt = pt(0) if (NT2 < 0) is True else NT2
    num = pt((iv.sqrt(nt) - s * iv.sqrt(L1 / mh.a) * Bop).a)
    num = pt(0) if (num < 0) is True else num
    Rp = pt((num ** 2 / ((1 + er) * (pt(Dn.b) + s * Bop) ** 2)).a)
    vSv_p = pt((num ** 2 / (1 + er) ** 3).a)
    vp = pt(((pt(Dn.b) + s * Bop) / (c * (1 - er))).b)
    Hd = pt((cx.entry('M2', 'I3m') / (g00 * mh)).b)
    rp_ = pt((L1o / mh.a).b)
    ed = V['eps_d']
    vSv_m = pt(((iv.sqrt(Hd + 2 * ed * iv.sqrt(rp_ * Hd) + rp_ * ed ** 2) + s * iv.sqrt(rp_) * beta / 2) ** 2
                / (c * c * (1 - er) ** 3)).b)
    odd2 = pt(((2 * cx.entry('B4', 'I_N') / mh - cx.entry('B5', 'Ndel')) / g00 + ed ** 2).b)
    vm = pt(((iv.sqrt(nn(odd2, '|v-|^2')) + s * beta / 2) / (c * (1 - er))).b)
    Ew = pt(((abs(cx.entry('M2', 'A0w')) / (mh * g00) + sp * (2 * Dn + Bop * sp)) / (1 - er)).b)
    t1 = pt(((kbar + Ew) * (1 + er)).b)
    nBp = pt(((beta if (beta.b >= t1.b) is True else t1) / (1 - er)).b)
    nBm = pt((beta / 2 / (1 - er)).b)
    q = (cx.entry('EW', 'I_mix') * iv.sqrt(inp['r_iv'] / (pt(g00.b) * pt(cx.entry('EW', 'I_free').b)))).a   # v2_2 (1): r_main in mp.iv
    Rw = pt(iv.sqrt(nn(1 / (pt(q) - sp) ** 2 - 1, 'R_w^2')).b)
    return dict(rho1=rho1, rho=rho, Rp=Rp, vSv_p=vSv_p, vp=vp, vSv_m=vSv_m, vm=vm, nBp=nBp, nBm=nBm, Rw=Rw, L1=L1, L1o=L1o, beta=beta,
                lam0=lam0, mu0=mu0, muz=muz, mh=mh, s=s, sp=sp, er=er, c=c, Bu2=Bu2, alpha=alpha, vtr=vtr, nv=nv, rho2=rho2,
                rho2_naive=rho2_n, L1arg=L1arg, L1_naive=L1s_n, U=U, order_ok=order_ok, uh=uh, Ew=Ew, t1=t1, kb=kb)   # v2_2 (2): C-KBAR INFO


def mode(cx, Ub, Q, V, use_centered=True):
    inp = cx.inp
    mh, s, sp, er, c = Q['mh'], Q['s'], Q['sp'], Q['er'], Q['c']
    idx = [0, 1, 3]
    Ge = [[cx.entry('B5', 'g,%d,%d' % (min(a, b), max(a, b))) for b in idx] for a in idx]
    Te = [[cx.entry('CT', 'T,%d,%d' % (min(a, b), max(a, b))) for b in idx] for a in idx]
    Aa = [cx.entry('B5', 'A,%d' % a) for a in idx]
    L = chol(Ge, 3)
    w = lsolve(L, Aa, 3)
    g00 = Ge[0][0]
    ax = abs(w[1] / (mh * iv.sqrt(g00)))
    Tm = congruent(L, Te, 3)
    qx = pt(Tm[1][1].a)
    nv = Q['nv']
    i0, ix = nv['i0'], nv['ix']
    Ae = nv['Ae']
    mux_n = pt(((Ae[i0][i0].a + Ae[ix][ix].a) / 2 - iv.sqrt(((pt(Ae[i0][i0].a) - Ae[ix][ix].a) / 2) ** 2 + pt(abs(Ae[i0][ix]).b) ** 2)).a)
    if (mux_n > 0) is not True:                                         # the L2 bound squares it
        raise ArithmeticError('the mu_x lower bound is not positive')
    mux = mux_n
    U = Q['U']
    L2arg_n = U - Q['mu0'] ** 2 - mux ** 2 - Q['muz'] ** 2
    L2arg = L2arg_n
    sq_arg = ((Ae[i0][i0] - Ae[ix][ix]) / 2) ** 2 + Ae[i0][ix] ** 2
    if (use_centered and (Ae[i0][i0].a > 0) is True and (Q['muz'] > 0) is True    # the smooth L2 form squares A_00 and mu_z too,
            and (sq_arg.a > 0) is True):                                          # and mu_x's square root must stay off its kink (N-d)
        L2arg, _ = centered(cx, Ub, 'f_L2', L2arg_n)
    L2 = pt(iv.sqrt(nn(L2arg, 'the L2 argument')).b)
    alpha_ = cx.entry('B5', 'A,0') / (mh * g00)
    Bu2 = (2 * cx.entry('B5', 'Ia') / mh - cx.entry('B5', 'Na')) / g00 + iv.mpf([0, (V['eps_a'] ** 2).b])
    vtr = iv.sqrt(nn(Bu2 - alpha_ ** 2, 'Bu2 - alpha^2'))
    Dm = cx.TRB() - alpha_
    beta = pt(((alpha_ + Dm) / 2 + iv.sqrt(((Dm - alpha_) / 2) ** 2 + vtr ** 2)).b)
    den3 = (1 - er) if cx.sc.get('author_forms') else (c - er)                                  # RV13_1 N3
    Dlt = pt((sp * (beta + alpha_ + 2 * iv.sqrt(Bu2) + beta * sp) / (1 - er) + vtr * er / den3).b)
    lam_ = Q['lam0']
    L1 = Q['rho1'] * lam_
    qxp = pt((qx - (1 + er) * mh.b * sp * sp).a)
    al2 = ((qxp - L2) / (L1 - L2)).a
    al2 = pt(0) if (pt(al2) < 0) is True else (pt(1) if (pt(al2) > 1) is True else pt(al2))
    axl = pt((pt(ax.a) - Dlt).a)
    cx_ = (iv.sqrt(al2) * axl - iv.sqrt(1 - al2) * iv.sqrt(nn(Q['vp'] ** 2 - axl ** 2, '|v+|^2 - a_x^2'))).a
    return dict(cx=pt(cx_), r2=pt((L2 / mux).b), ro=pt((Q['rho'] * lam_ / mux).b), al2=al2, L2=L2, mux=mux, qx=qx, ax=pt(ax.a), Dlt=Dlt,
                simple=(L2 < mux) is True, L2arg=L2arg, L2_naive=L2arg_n)


def width_exps(wa, wb, k):
    """P2-11: the S powers of the second-order end terms, with k plain transfer steps strictly between the two
    insertions, wa the width of the left insertion and wb that of the right one. 'A': the bracket term with the left amplitude bare,
    <a,u><eps_L, S^(k+wa) Q0 b>; 'B': the one with the right amplitude bare, <Q0 a, S^(k+wb) eps_R><u,b>; 'D': the normalization
    D = <L, S^(k+wa+wb) R> = 1 + <eps_L, S^(k+wa+wb) eps_R>, which also sets the 1 - 1/D term. w = (1, 1) gives v2_2's powers; the
    EXPONENT TABLE lines print these per width pair."""
    return dict(A=k + wa, B=k + wb, D=k + wa + wb)


def tw_abs(r1, e, pa, Ba, pb, Bb, k, w):
    """P2-11: the second-order end terms of the Jensen form, in absolute units. A is the left insertion
    (pa >= ||Q0 B_a u||, Ba >= ||B_a||), b the right one, ||eps_L||, ||eps_R|| <= e, rho1 >= the top of S on u-perp, k plain steps,
    w = (w_a, w_b). Returns (rho1^D e^2, t2), or (None, None) unless rho1^D e^2 < 1 certainly. At w = (1, 1) with equal sides this is
    v2_2's pj arithmetic, operation for operation (C-WIDTH)."""
    ex = width_exps(w[0], w[1], k)
    Dm1 = r1 ** ex['D'] * e * e
    if (Dm1 < 1) is not True:
        return None, None
    aua, aub = e * pa, e * pb
    qa, qb = pa + Ba * e, pb + Bb * e
    t2 = aua * aub * Dm1 / (1 - Dm1) + (aua * r1 ** ex['A'] * e * qb + aub * r1 ** ex['B'] * e * qa
                                        + (r1 ** ex['B'] * e * qa) * (r1 ** ex['A'] * e * qb)) / (1 - Dm1)
    return Dm1, t2


def tw_mode(r1, e, pa, Ba, pb, Bb, k, w):
    """P2-11: the T_w(k, e) (dbd501bc sect. 2), the second-order end terms in units of s_x^k, with tw_abs's inputs. The main term
    keeps S^k, so the three k-free terms carry the powers less k (s_x <= rho1) and the last one rho1^D. Returns (rho1^D e^2, T_w), or
    (None, None) unless rho1^D e^2 < 1 certainly. At w = (1, 1) with equal sides this is v2_2's pm arithmetic, operation for operation."""
    ex = width_exps(w[0], w[1], k)
    Dm1 = r1 ** ex['D'] * e * e
    if (Dm1 < 1) is not True:
        return None, None
    qa, qb = pa + Ba * e, pb + Bb * e
    T = (r1 ** (ex['D'] - k) * ((e * pa) * (e * pb)) * e * e + (r1 ** (ex['A'] - k) * e * pa * e * qb + r1 ** (ex['B'] - k) * e * pb * e * qa)
         + r1 ** ex['D'] * ((e * qa) * (e * qb))) / (1 - Dm1)
    return Dm1, T


def pj(Q, d, m, kind, sc, C1, w=(1, 1), side=None):
    """Jensen inequality (endpairs4 passes_jensen) in intervals; True only if the lower end of the left side is > 0. P2-11: m - 1 plain
    steps strictly between the insertions and widths w (tw_abs). side None is the vertical insertion (v2_2's form at w = (1, 1)); else a
    horizontal insertion's dict (p, Bp and P: m -> the main term's lower bound), for the same type only."""
    e = Q['Rw'] * sc.get('Rw', 1.0) * Q['rho1'] ** d
    r1, r = Q['rho1'], Q['rho']
    if side is None:
        pX = iv.sqrt(Q['vp'] ** 2 + Q['vm'] ** 2)
        nBp, nBm = Q['nBp'] * sc.get('nB', 1.0), Q['nBm'] * sc.get('nB', 1.0)
    elif kind == 'flip':
        raise ValueError('pj: a horizontal side is for the same type only')
    else:
        pX, nBp = side['p'], side['Bp']
    Dm1, t2 = tw_abs(r1, e, pX, nBp, pX, nBp, m - 1, w)
    if Dm1 is None:
        return False
    hm = lambda x: iv.sqrt(x) ** (m - 1) if m > 1 else pt(1)
    if kind == 'flip':
        Cm = C1 if m == 1 else Q['vSv_p'] * Q['Rp'] ** (m - 2) - Q['vSv_m'] * r ** (m - 2)
        ep = hm(r1) * nBp * e
        em = hm(r) * nBm * e
        err = hm(r1) * Q['vp'] * 2 * ep + ep * ep + hm(r) * Q['vm'] * 2 * em + em * em
        return ((Cm - err - t2) > 0) is True
    if side is None:
        P = iv.sqrt(Q['vSv_p'] / r1) if m == 1 else iv.sqrt(Q['vSv_p'] * Q['Rp'] ** (m - 2))
    else:
        P = side['P'](m)
    et = hm(r1) * nBp * e
    return (P >= et) is True and ((P * (P - 2 * et) - et * et - t2) > 0) is True


def pm(Q, Mq, d, k, kind, sc, w=(1, 1), side=None):
    """mode inequality M(k, e) of SPEC v1_1 sect. 1a in intervals. P2-11: k plain steps and widths w (tw_mode, units of s_x^k). side None
    is the vertical insertion (v2_2's form at w = (1, 1)); else a horizontal insertion's dict (cx: the x amplitude's lower end; p, vp, vm,
    Bp, Bm), for the same type only."""
    e = Q['Rw'] * sc.get('Rw', 1.0) * Q['rho1'] ** d
    if side is None:
        nBp, nBm = Q['nBp'] * sc.get('nB', 1.0), Q['nBm'] * sc.get('nB', 1.0)
        cx, pX, vp, vm = Mq['cx'] / sc.get('cx_div', 1.0), iv.sqrt(Q['vp'] ** 2 + Q['vm'] ** 2), Q['vp'], Q['vm']
    elif kind == 'flip':
        raise ValueError('pm: a horizontal side is for the same type only')
    else:
        nBp, nBm, cx, pX, vp, vm = side['Bp'], side['Bm'], side['cx'], side['p'], side['vp'], side['vm']
    X = cx - nBp * e
    if (X > 0) is not True:
        return False
    r1 = Q['rho1']
    E = Mq['r2'] ** k * (vp + nBp * e) ** 2
    O = Mq['ro'] ** k * ((vm + nBm * e) ** 2 if kind == 'flip' else 2 * vm * nBm * e + (nBm * e) ** 2)
    Dm1, T = tw_mode(r1, e, pX, nBp, pX, nBp, k, w)
    if Dm1 is None:
        return False
    return ((X * X - E - O - T) > 0) is True


def s7mono_hyp(Q, Mq, d, k0, sc, w=(1, 1), side=None):
    """the hypotheses of Lemma S7-mono (a) at the claimed d: r2, ro, rho1 < 1, X > 0, rho1^(k0+2) e^2 < 1. P2-11: D's power is
    k0 + w_a + w_b (width_exps); side as in pm."""
    e = Q['Rw'] * sc.get('Rw', 1.0) * Q['rho1'] ** d
    X = (Mq['cx'] / sc.get('cx_div', 1.0) - Q['nBp'] * sc.get('nB', 1.0) * e) if side is None else side['cx'] - side['Bp'] * e
    return ((Mq['r2'] < 1) is True and (Mq['ro'] < 1) is True and (Q['rho1'] < 1) is True and (X > 0) is True
            and (Q['rho1'] ** width_exps(w[0], w[1], k0)['D'] * e * e < 1) is True)


def coverage(Q, Mq, sc, C1, pairs, w=(1, 1), side=None):
    res = {}
    for kd, d in pairs:
        m = 1
        while m <= MMAX and pj(Q, d, m, kd, sc, C1, w, side):
            m += 1
        k = 1
        while k <= KMAX and not pm(Q, Mq, d, k, kd, sc, w, side):
            k += 1
        res[(kd, d)] = (m - 1, k)
    return res


def coverage_claim(Q, Mq, sc, C1, pairs, w=(1, 1), side=None):
    """the same verdict as coverage() for the claimed pairs, with less work: k = the first mode success (Lemma S7-mono covers m >= k + 1),
    then Jensen only for m = 1..k. Returns (m checked, k); the claim holds iff m checked >= k (m checked stops at k). P2-11: w and side
    pass to pj and pm (m - 1 and k count plain steps)."""
    res = {}
    for kd, d in pairs:
        k = 1
        while k <= KMAX and not pm(Q, Mq, d, k, kd, sc, w, side):
            k += 1
        m = 1
        while k <= KMAX and m <= k and pj(Q, d, m, kd, sc, C1, w, side):
            m += 1
        res[(kd, d)] = (m - 1, k)
    return res


def claim_holds(cv, p):
    """Jensen for m = 1..k and the mode inequality at k <= KMAX (so Lemma S7-mono covers m >= k + 1)."""
    return cv[p][1] <= KMAX and cv[p][0] >= cv[p][1]


# ------------------------------------------------------------------ S5 (binding pair) with the centered even - odd
def s5_parts(cx, V, kind):
    mh = cx.mhat(kind)
    idx = [0, 1, 3]
    Ge = [[cx.entry('B5', 'g,%d,%d' % (min(a, b), max(a, b)), kind) for b in idx] for a in idx]
    Aa = [cx.entry('B5', 'A,%d' % a, kind) for a in idx]
    L = chol(Ge, 3)
    w = lsolve(L, Aa, 3)
    g00 = Ge[0][0]
    sg = sqrt_any(g00)
    ax = w[1] / (mh * sg)
    ay = w[2] / (mh * sg)
    even = ax * ax + ay * ay
    edl = V['eps_ds5'] if kind in ('naive', 'point', 'dual', 'offset', 'cnaive') else pt(0)
    odd = (2 * cx.entry('B4', 'I_N', kind) / mh - cx.entry('B5', 'Ndel', kind)) / g00 + edl * edl
    if cx.sc.get('odd_sign'):
        odd = -odd
    return dict(even=even, odd=odd, Dd=even - odd, g00=g00, mh=mh)


def s5_bound(cx, V, use_centered=True):
    nv = s5_parts(cx, V, 'naive')
    Dd = nv['Dd']
    if use_centered:
        try:
            Fm = s5_parts(cx, V, 'point')['Dd']
            Dp = s5_parts(cx, V, 'dual')['Dd']
            cen = finite(Fm + finite(Dp.d, 'D(P) of S5 even - odd') * cx.h * iv.mpf([-1, 1]), 'S5 even - odd')
        except (ArithmeticError, ValueError, ZeroDivisionError):           # a kink or a non-finite D(P): the naive enclosure (N-d)
            cx.cache['fallbacks'] = cx.cache.get('fallbacks', 0) + 1
            cen = None
        if cen is not None:
            Dd = isect(nv['Dd'], cen)                                        # both are true two-sided enclosures here
    mh, g00 = nv['mh'], nv['g00']
    er, s = V['eps_r'], V['s']
    c = iv.sqrt(1 - s * s)
    sp = s * iv.sqrt(2 / (1 + c))
    Bu2 = (2 * cx.entry('B5', 'Ia') / mh - cx.entry('B5', 'Na')) / g00 + iv.mpf([0, (V['eps_a'] ** 2).b])
    alpha = cx.entry('B5', 'A,0') / (mh * g00)
    vtr = iv.sqrt(nn(Bu2 - alpha ** 2, 'Bu2 - alpha^2'))
    Dm = cx.TRB() - alpha
    beta = pt(((alpha + Dm) / 2 + iv.sqrt(((Dm - alpha) / 2) ** 2 + vtr ** 2)).b)
    den3 = (1 - er) if cx.sc.get('author_forms') else (c - er)                                  # RV13_1 N3
    Dlt = sp * (beta + alpha + 2 * iv.sqrt(Bu2) + beta * sp) / (1 - er) + vtr * er / den3
    vacT = Dlt * (2 * vtr + Dlt)
    low = (Dd - vacT).a
    return dict(c5=pt(low), even=nv['even'], odd=nv['odd'], vacT=vacT, beta=beta, Dd=Dd, Dd_naive=nv['Dd'], Dlt=Dlt)   # Dlt: v2_2 export


# ------------------------------------------------------------------ one piece: S5, S6 and S7, and the verdicts of the scans
def piece_eval(inp, Jlo, Jhi, sc, use_centered=True, Ub=None, Jvac=None, order=None, C1=None, full=False, pairs=None):
    """S5, S6 and S7 on one piece. Ub, Jvac and order let C-PIECE reuse the parent piece's preconditioner, vacuum point and index order.
    C1 = None takes the piece's own c5 for S7's m = 1 Jensen test (ADD1 sect. 1); a number takes that constant (path A's Cov_1, for
    C-REPRO). full = True runs the full coverage search (Jensen to its first failure) instead of the claim check."""
    cx = Ctx(inp, Jlo, Jhi, sc)
    if order is not None:
        cx.cache['order'] = order
    V = vac_terms(inp, Jlo if Jvac is None else Jvac, sc)          # the certified snapshot: LAW v1 on the M2(b) record (vac_terms)
    S5 = s5_bound(cx, V, use_centered)
    Ub = ritz_basis(cx) if Ub is None else Ub
    Q = quantities(cx, Ub, V, use_centered)
    Mq = mode(cx, Ub, Q, V, use_centered)
    c1 = (S5['c5'] if C1 is None else pt(C1)) / sc.get('cov1_div', 1.0)
    prs = CLAIM[inp['N']] if pairs is None else pairs
    cv = (coverage if full else coverage_claim)(Q, Mq, sc, c1, prs)
    return dict(cx=cx, V=V, S5=S5, Ub=Ub, Q=Q, Mq=Mq, cv=cv)


def verdict_one(inp, Jlo, Jhi, sc, which, use_centered=False, claim=None):
    """S5: c5 > 0; S6: R+/rho > 1; S7: the claimed coverage (CLAIM, or the pairs in claim: D1's FLIP170_CLAIM, D2's flip d = 3 pair), with
    C_1 = the piece's c5 (path A's Cov_1 under the hook 'C1_const'). A numeric breakdown under a large hook counts as a failed verdict;
    programming errors and empty intersections are not caught."""
    try:
        cx = Ctx(inp, Jlo, Jhi, sc)
        V = vac_terms(inp, Jlo, sc)
        if which == 'S5':
            return (s5_bound(cx, V, use_centered)['c5'] > 0) is True
        Ub = ritz_basis(cx)
        Q = quantities(cx, Ub, V, use_centered)
        if which == 'S6':
            return ((Q['Rp'] / Q['rho']).a > 1) is True
        Mq = mode(cx, Ub, Q, V, use_centered)
        c1 = pt(inp['P']['cov1']) if sc.get('C1_const') else s5_bound(cx, V, use_centered)['c5']
        prs = CLAIM[inp['N']] if claim is None else claim                  # D1, D2
        cv = coverage_claim(Q, Mq, sc, c1 / sc.get('cov1_div', 1.0), prs)
        return all(claim_holds(cv, p) for p in prs)
    except (ValueError, ZeroDivisionError, ArithmeticError):
        return False


def flip_search(fn, kind, cap):
    """smallest hook value at which fn is False: 'mul' (k >= 1), 'add' (delta >= 0), 'rel' (r in [0, 1)); None if never below cap; 0.0 if
    the baseline fails. Bisection to 0.4 per cent (INFO for the targets)."""
    if not fn(1.0 if kind == 'mul' else 0.0):
        return 0.0
    if kind == 'mul':
        lo, hi = 1.0, 2.0
        while fn(hi):
            lo, hi = hi, hi * 2
            if hi > cap:
                return None
        while hi / lo > 1.004:
            mid = math.sqrt(lo * hi)
            lo, hi = (mid, hi) if fn(mid) else (lo, mid)
        return hi
    if kind == 'add':
        lo, hi = 0.0, 1e-4
        while fn(hi):
            lo, hi = hi, hi * 2
            if hi > cap:
                return None
        while hi - lo > 0.004 * hi:
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if fn(mid) else (lo, mid)
        return hi
    lo, hi = 0.0, 0.01
    while fn(hi):
        lo, hi = hi, min(hi * 2, cap)
        if lo >= cap:
            return None
    while hi - lo > 2e-4:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if fn(mid) else (lo, mid)
    return hi


def fmt_f(v):
    return 'never (cap)' if v is None else ('baseline fails' if v == 0.0 else '%.4g' % v)


JOINT = 'joint: bars, vacuum, eps_w, rem'
GROUPS = [  # (label, hook maker, kind, cap, part, verdicts it can move)
    ('19.1c bars, all', lambda x: {'bar_all': x}, 'mul', MCAP, 'M3', 'S5 S6 S7'),
    ('19.1c bars, Ritz (B5 Gram, CT)', lambda x: {'bar_ritz': x}, 'mul', MCAP, 'M3', 'S5 S6 S7'),
    ('19.1c bars, amplitudes A_a', lambda x: {'bar_amp': x}, 'mul', MCAP, 'M3', 'S5 S6 S7'),
    ('19.1c bar I3p', lambda x: {'bar_I3p': x}, 'mul', MCAP, 'M3', 'S6 S7'),
    ('19.1c bar Ip3', lambda x: {'bar_Ip3': x}, 'mul', MCAP, 'M3', 'S6 S7'),
    ('19.1c bar N_w', lambda x: {'bar_Nw': x}, 'mul', MCAP, 'M3', 'S6 S7'),
    ('19.1c bar N_delta', lambda x: {'bar_Ndel': x}, 'mul', MCAP, 'M3', 'S5 S7'),
    ('19.1c bar I_N', lambda x: {'bar_I_N': x}, 'mul', MCAP, 'M3', 'S5 S7'),
    ('19.1c bars endw (I_mix, I_free)', lambda x: {'bar_endw': x}, 'mul', MCAP, 'M3', 'S7'),
    ('central I3p lowered (relative)', lambda x: {'I3p_c': x}, 'rel', 0.99, 'M3', 'S6 S7'),
    ('central Ip3 raised (relative)', lambda x: {'Ip3_c': x}, 'rel', 0.99, 'M3', 'S6 S7'),
    ('central N_w lowered (relative)', lambda x: {'Nw_c': x}, 'rel', 0.99, 'M3', 'S6 S7'),
    ('vacuum, all', lambda x: {'vac_all': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),
    ('vacuum D5', lambda x: {'D5': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),
    ('vacuum gB', lambda x: {'gB': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),
    ('vacuum Z2 (divided by; LAW v1 only)', lambda x: {'z2': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),      # SPEC_MA_LAYER_v1_2_ADD1 sect. 2:
    ('vacuum Rtr (LAW v1 only)', lambda x: {'Rtr': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),               # M2(b)'s record quotes these two
    ('eps_delta of S5 (wres c_xi J/2, J)', lambda x: {'eps_ds5': x}, 'mul', MCAP, 'M2', 'S5 S7'),
    ('eps_a (wres c_xi J, 2J)', lambda x: {'eps_a': x}, 'mul', MCAP, 'M2', 'S5 S6 S7'),
    ('Lemma 19.5w eps_w, eps_d', lambda x: {'eps_w': x}, 'mul', MCAP, 'P3', 'S6 S7'),
    ('Lemma 19.4 rem', lambda x: {'remT': x}, 'mul', MCAP, 'S4', 'S6 S7'),
    ('U raised by (absolute)', lambda x: {'U_add': x}, 'add', 1.0, 'S4', 'S6 S7'),
    ('TRB (beta)', lambda x: {'TRB': x}, 'mul', MCAP, 'S4', 'S5 S6 S7'),
    (JOINT, lambda x: {'bar_all': x, 'vac_all': x, 'eps_w': x, 'remT': x}, 'mul', MCAP, 'all', 'S5 S6 S7'),
    ('R_w', lambda x: {'Rw': x}, 'mul', MCAP, 'S7', 'S7'),
    ('||B+-||', lambda x: {'nB': x}, 'mul', MCAP, 'S7', 'S7'),
    ('c_x (divided by)', lambda x: {'cx_div': x}, 'mul', MCAP, 'S7', 'S7'),
    ('C_1 = c5 (divided by)', lambda x: {'cov1_div': x}, 'mul', MCAP, 'S5', 'S7'),
]
GMAP = {g[0]: g for g in GROUPS}
LAST_GROUPS = ((JOINT, 'S5'), (JOINT, 'S6'), (JOINT, 'S7'), ('19.1c bars, all', 'S6'), ('U raised by (absolute)', 'S6'), ('TRB (beta)', 'S6'))

REVMAP = {  # the review label -> (hook maker, kind, cap), as P0
    'eps_w x': (lambda x: {'eps_w': x}, 'mul', MCAP), 'D5 (eps_r, s) x': (lambda x: {'D5': x}, 'mul', MCAP),
    'gB (eps_r and eps_w bad-bond part) x': (lambda x: {'gB': x}, 'mul', MCAP),
    'all Lemma 19.1c error bars (M2, B5, CT) x': (lambda x: {'bar_all': x}, 'mul', MCAP),
    'Ritz error bars (B5 Gram + CT T) x': (lambda x: {'bar_ritz': x}, 'mul', MCAP),
    'I3p error bar x': (lambda x: {'bar_I3p': x}, 'mul', MCAP), 'Ip3 error bar x': (lambda x: {'bar_Ip3': x}, 'mul', MCAP),
    'Nw error bar x': (lambda x: {'bar_Nw': x}, 'mul', MCAP), 'Lemma 19.4 remainder rem x': (lambda x: {'remT': x}, 'mul', MCAP),
    'TRB x': (lambda x: {'TRB': x}, 'mul', MCAP), 'U raised by (absolute)': (lambda x: {'U_add': x}, 'add', 1.0),
    'I3p central lowered by (relative)': (lambda x: {'I3p_c': x}, 'rel', 0.99),
    'Ip3 central raised by (relative)': (lambda x: {'Ip3_c': x}, 'rel', 0.99),
    'Nw central lowered by (relative)': (lambda x: {'Nw_c': x}, 'rel', 0.99),
    'R_w x': (lambda x: {'Rw': x}, 'mul', MCAP), '||B+||, ||B-|| x': (lambda x: {'nB': x}, 'mul', MCAP),
    'c_x /': (lambda x: {'cx_div': x}, 'mul', MCAP), 'Cov_1 /': (lambda x: {'cov1_div': x}, 'mul', MCAP),
    'U raised by': (lambda x: {'U_add': x}, 'add', 1.0),
}


# ------------------------------------------------------------------ C-REPRO: path B against path A
ALLPAIRS = [(kd, d) for kd in ('flip', 'same') for d in DS]
QKEYS = ('rho1', 'rho', 'Rp', 'vSv_p', 'vp', 'vSv_m', 'vm', 'nBp', 'nBm', 'Rw')
MKEYS = ('cx', 'r2', 'ro', 'al2', 'L2', 'mux', 'qx', 'ax', 'Dlt')
TOL_ONE = 1e-12


def rel(b, a):
    return abs(b - a) / max(abs(a), 1e-300)


def fnum(x):
    """a point interval (or a float) as a float, for the comparisons with path A."""
    return float(x.mid) if isinstance(x, IVT) else float(x)


def nf(x, n=6):
    """a short decimal of an interval's midpoint or a float (prints only)."""
    return '%.*g' % (n, fnum(x))


def cover_a(ns, Qa, Ma, pairs):
    """the author's coverage search (endpairs4 passes_jensen, passes_mode, with its Cov_1)."""
    res = {}
    for kd, d in pairs:
        m = 1
        while m <= MMAX and ns['passes_jensen'](Qa, d, m, kd):
            m += 1
        k = 1
        while k <= KMAX and not ns['passes_mode'](Qa, Ma, d, k, kd):
            k += 1
        res[(kd, d)] = (m - 1, k)
    return res


def never_better(rows):
    """names whose production bound beats path A's beyond TOL_ONE (a lower bound higher, an upper bound lower)."""
    bad = []
    for name, side, b, a in rows:
        b, a = fnum(b), fnum(a)
        if (side == 'lo' and b > a + TOL_ONE * abs(a)) or (side == 'hi' and b < a - TOL_ONE * abs(a)):
            bad.append(name)
    return bad


def repro_compare(inp, nsm, nse, nsb, Jlo, Jhi, sc=None, pairs=None):
    """C-REPRO on one piece (SPEC v1_1 sect. 4, ADD1 sect. 5). Path B with the naive enclosures and the author's forms against path A
    on every S5, S6 and S7 quantity (two-sided, relative TOL_B) and on the coverage tables (C_1 = path A's Cov_1); then path B with the
    production forms (RV13_1 N3), which must never beat path A beyond TOL_ONE. Returns (worst, its key, the violations, tables equal).
    Path B takes path A's FLOAT U and TRB here (float_s4): the comparison is of the arithmetic, on the same inputs (F2, v2_1)."""
    sc = {} if sc is None else sc
    inp = float_s4(inp)
    pairs = CLAIM[inp['N']] if pairs is None else pairs
    Rp_a, rho_a, er_a, ew_a, L1e_a, be_a, cr_a = nsm['check'](Jlo, Jhi)
    Qa = nse['quantities'](Jlo, Jhi)
    Ma = nse['mode_data'](Jlo, Jhi, Qa)
    cA, evA, odA, vtA, erA, svA, beA = nsb['cov_lower'](Jlo, Jhi)
    B = piece_eval(inp, Jlo, Jhi, dict(sc, author_forms=True), use_centered=False, C1=inp['P']['cov1'], full=True, pairs=pairs)
    Qb, Mb, Sb, Vb = B['Q'], B['Mq'], B['S5'], B['V']
    rows = [('S6 R+', Qb['Rp'], Rp_a), ('S6 rho', Qb['rho'], rho_a), ('S6 L1e', Qb['L1'], L1e_a), ('S6 beta', Qb['beta'], be_a),
            ('S6 eps_r', Vb['eps_r'], er_a), ('S6 eps_w', Vb['eps_w'], ew_a), ('S7 eps_w', Vb['eps_w'], Qa['eps_w']),
            ('S7 eps_d', Vb['eps_d'], Qa['eps_d'])]
    rows += [('S7 ' + k, Qb[k], Qa[k]) for k in QKEYS] + [('S7 ' + k, Mb[k], Ma[k]) for k in MKEYS]
    rows += [('S5 c5', Sb['c5'], cA.a), ('S5 even', Sb['even'].a, evA.a), ('S5 odd', Sb['odd'].b, odA.b), ('S5 vacT', Sb['vacT'].b, vtA.b),
             ('S5 beta', Sb['beta'], beA.b), ('S5 eps_r', Vb['eps_r'], erA), ('S5 s', Vb['s'], svA)]
    worst, wk = 0.0, ''
    for name, b, a in rows:
        r_ = rel(fnum(b), fnum(a))
        if r_ > worst:
            worst, wk = r_, name
    cov_same = B['cv'] == cover_a(nse, Qa, Ma, pairs)
    P_ = piece_eval(inp, Jlo, Jhi, dict(sc), use_centered=False, C1=inp['P']['cov1'], pairs=pairs)
    viol = never_better([('R+', 'lo', P_['Q']['Rp'], Rp_a), ('rho', 'hi', P_['Q']['rho'], rho_a), ('rho1', 'hi', P_['Q']['rho1'], Qa['rho1']),
                         ('c_x', 'lo', P_['Mq']['cx'], Ma['cx']), ('c5', 'lo', P_['S5']['c5'], cA.a)])
    return worst, wk, viol, cov_same


# ------------------------------------------------------------------ C-PIECE, C-UNIF, C-PARITY, C-MODULE, C-TAG
LOWER_KEYS = ('Rp', 'vSv_p', 'mux', 'qx', 'ax', 'al2', 'cx', 'c5', 'even')
UPPER_KEYS = ('rho1', 'rho', 'L1', 'beta', 'vp', 'vSv_m', 'vm', 'nBp', 'nBm', 'Rw', 'L2', 'r2', 'ro', 'Dlt', 'odd', 'vacT')


def piece_str(Jlo, Jhi):
    return '%.2f, %s' % (Jlo, 'inf' if Jhi is None else '%.2f' % Jhi)


def bounds_of(E):
    """a piece evaluation's one-sided bounds: lower ends of the lower bounds, upper ends of the upper bounds."""
    src = dict(E['Q'])
    src.update(E['Mq'])
    src.update(c5=E['S5']['c5'], even=E['S5']['even'], odd=E['S5']['odd'], vacT=E['S5']['vacT'])
    b = {k: ('lo', pt(src[k]).a) for k in LOWER_KEYS}
    b.update({k: ('hi', pt(src[k]).b) for k in UPPER_KEYS})
    return b


def outward(fb, hb):
    """the largest relative outward move of a half piece's bounds against the piece's own (> 0: moved outward), and its key."""
    worst, wk = -1.0, ''
    for k, (side, fv) in fb.items():
        hv = hb[k][1]
        d = (fv - hv) if side == 'lo' else (hv - fv)
        den = abs(fv) if (abs(fv) > 0) is True else pt(1e-300)
        r_ = float((d / den).b)
        if r_ > worst:
            worst, wk = r_, k
    return worst, wk


def entry_names(inp):
    return ([('M2', n) for n in sorted(inp['M2']['items'])] + [('B5', n) for n in sorted(inp['B5']['items'])]
            + [('CT', n) for n in sorted(inp['CT']['items'])] + [('B4', 'I_N')] + [('EW', n) for n in sorted(inp['EW']['items'])])


def piece_terms(cx, Ub, V, kind):
    """the terms C-PIECE compares (S3): every stored entry, U, m-hat, the even and odd Ritz matrices and S5's parts, in one kind ('naive'
    over the piece, or 'point' at cx.tm, both with bars). The naive differences of rho^2, L1 and L2 are left out: only their upper ends
    are bounds, and those enter the final bounds, which are compared separately."""
    T = {'%s %s' % nm: cx.entry(nm[0], nm[1], kind) for nm in entry_names(cx.inp)}
    T['U'], T['m-hat'] = cx.U(kind), cx.mhat(kind)
    Ae, Ao = ritz_matrix(cx, Ub, 'even', kind), ritz_matrix(cx, Ub, 'odd', kind)
    T.update(('Ritz even %d%d' % (i, j), Ae[i][j]) for i in range(3) for j in range(3))
    T['Ritz odd'] = Ao[0][0]
    S5 = s5_parts(cx, V, kind)
    T.update({'S5 even': S5['even'], 'S5 odd': S5['odd'], 'S5 even - odd': S5['Dd']})
    return T


def piece_check(inp, Jlo, Jhi, sc=None):
    """C-PIECE (S3, N-f), on the naive enclosures. Every term of each half piece (with the piece's preconditioner, vacuum point and index
    order) lies in the piece's own enclosure, and no final bound moves outward beyond 1e-15. The piece's enclosure contains the point
    evaluations, with bars, at its two ends and its midpoint (computed without the PLANT-RIGHTEND hook). Returns (the failing terms, the
    largest relative outward move of a final bound, its key)."""
    sc = {} if sc is None else sc
    full = piece_eval(inp, Jlo, Jhi, sc, use_centered=False)
    cx, Ub, V = full['cx'], full['Ub'], full['V']
    Tf = piece_terms(cx, Ub, V, 'naive')
    fb = bounds_of(full)
    order = order_from_central(cx, Ub)
    Jm = 2 * Jlo if Jhi is None else math.sqrt(Jlo * Jhi)
    bad, worst, wk = set(), -1.0, ''
    for a, b in ((Jlo, Jm), (Jm, Jhi)):
        h = piece_eval(inp, a, b, sc, use_centered=False, Ub=Ub, Jvac=Jlo, order=order)
        Th = piece_terms(h['cx'], Ub, h['V'], 'naive')
        bad.update('half [%s] %s' % (piece_str(a, b), k) for k in Tf if not contains(Tf[k], Th[k]))
        w, k = outward(fb, bounds_of(h))
        if w > worst:
            worst, wk = w, k
    clean = {k: v for k, v in sc.items() if k != 'right_end'}
    for tv in (cx.tI.a, cx.tm, cx.tI.b):
        sub = Ctx(inp, Jlo, Jhi, clean)
        sub.tm = iv.mpf([pt(tv).a, pt(tv).a])
        sub.cache['order'] = order
        Tp = piece_terms(sub, Ub, V, 'point')
        bad.update('point t = %s %s' % (nf(tv, 8), k) for k in Tp if not contains(Tf[k], Tp[k]))
    return sorted(bad), worst, wk


MVB_ENTRIES = ([('B5', 'g,%d,%d' % ab) for ab in ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3), (2, 2))]
               + [('CT', 'T,%d,%d' % ab) for ab in ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3), (2, 2))]
               + [('B5', 'A,0'), ('B5', 'A,1'), ('B5', 'A,3'), ('B4', 'I_N'), ('B5', 'Ndel')])


def mvb_values(cx, Ub, V, tval, offsets):
    """the four smooth functions at the point inputs c(tval) + delta, delta = offsets x bars (kind 'offset'), with the piece's fixed index
    order and constant radius."""
    sub = Ctx(cx.inp, cx.Jlo, cx.Jhi, dict(cx.sc, offsets=offsets))
    sub.tm = tval
    sub.cache['order'] = order_from_central(cx, Ub)
    sub.cache['R_iy'] = radius_const(cx, Ub)
    r = dict(udiffs(sub, Ub, 'offset'))
    r['S5 Dd'] = s5_parts(sub, V, 'offset')['Dd']
    return r


def mvb_check(cx, Ub, V, bar_free=False):
    """C-MV-B (S4): at 9 equispaced points t_j, f(c(t_j) + delta) with point inputs, for delta = 0 and delta = +-(bar x sign of the
    gradient of f at c(t_m)) per function, lies in F(t_m) + D(P)[-h, h]. The signs come from symmetric differences of one bar per entry.
    bar_free is the plant (F(t_m) evaluated with B = 0). Returns the failing functions."""
    kindF = 'central' if bar_free else 'point'
    Fm = dict(udiffs(cx, Ub, kindF))
    Fm['S5 Dd'] = s5_parts(cx, V, kindF)['Dd']
    Dp = dict(ud_kind(cx, Ub, 'dual'))
    Dp['S5 Dd'] = s5_parts(cx, V, 'dual')['Dd']
    enc = {k: Fm[k] + Dp[k].d * cx.h * iv.mpf([-1, 1]) for k in MV_KEYS}
    sg = {k: {} for k in MV_KEYS}
    for e in MVB_ENTRIES:
        vp, vm = mvb_values(cx, Ub, V, cx.tm, {e: 1}), mvb_values(cx, Ub, V, cx.tm, {e: -1})
        for k in MV_KEYS:
            d = fnum(vp[k]) - fnum(vm[k])
            sg[k][e] = 1 if d > 0 else (-1 if d < 0 else 0)
    bad = set()
    for j in range(9):
        tj = cx.tI.a + (cx.tI.b - cx.tI.a) * j / 8
        tval = iv.mpf([tj.a, tj.a])
        v0 = mvb_values(cx, Ub, V, tval, {})
        bad.update(k for k in MV_KEYS if not contains(enc[k], v0[k]))
        for k in MV_KEYS:
            for s_ in (1, -1):
                if not contains(enc[k], mvb_values(cx, Ub, V, tval, {e: s_ * sg[k][e] for e in MVB_ENTRIES})[k]):
                    bad.add(k)
    return sorted(bad)


def unif_check(cx):
    """C-UNIF: on the piece, the bar-free interval enclosures ('cnaive') of every stored entry, of U and of m-hat contain their values at
    9 equispaced t (computed without the PLANT-RIGHTEND hook). Returns the names that fail."""
    inp = cx.inp
    names = entry_names(inp)
    enc = {'%s %s' % nm: cx.entry(nm[0], nm[1], 'cnaive') for nm in names}
    enc['U'], enc['m-hat'] = cx.U('cnaive'), cx.mhat('cnaive')
    clean = {k: v for k, v in cx.sc.items() if k != 'right_end'}
    bad = set()
    for j in range(9):
        sub = Ctx(inp, cx.Jlo, cx.Jhi, clean)
        tj = cx.tI.a + (cx.tI.b - cx.tI.a) * j / 8
        sub.tm = iv.mpf([tj.a, tj.a])
        val = {'%s %s' % nm: sub.entry(nm[0], nm[1], 'central') for nm in names}
        val['U'], val['m-hat'] = sub.U('central'), sub.mhat('central')
        bad.update(k for k in enc if not contains(enc[k], val[k]))
    return sorted(bad)


PARITY_KEYS = ('g,0,2', 'g,1,2', 'g,2,3')
PARITY_T_KEYS = ('T,0,2', 'T,1,2', 'T,2,3')     # clT's cross-parity entries: absent from the records, refused if present and nonzero
PARITY_FIELDS = ('ak', 'ak_rad', 'B', 'Bp', 'err')


def parity_max(B5):
    """C-PARITY: the largest |a_k| of the cross-parity Gram entries; exactly 0 for symmetrized trial vectors (v1_1 sect. 4)."""
    return max(abs(a) for k in PARITY_KEYS for a in B5['items'][k]['ak'])


def parity_zero(v):
    """an item field is exactly zero: a number 0, or a list or dict whose every value is exactly zero; None is not zero (
    a None anywhere fails the gate)."""
    if v is None or isinstance(v, bool):                 # False == 0 in Python, so a bool is refused before the test
        return False
    if isinstance(v, dict):
        return all(parity_zero(x) for x in v.values())
    if isinstance(v, (list, tuple)):
        return all(parity_zero(x) for x in v)
    return v == 0


def parity_bad(B5, CT):
    """the Ritz blocks drop the cross-parity entries, which is valid only if each is exactly 0 with its bars. Every
    PARITY_KEYS item of B5 must be present with a_k, ak_rad, B, Bp and err all exactly zero; a PARITY_T_KEYS item of CT, if present,
    likewise. Returns the problems."""
    bad = []
    for src, rec, keys, need in (('B5', B5, PARITY_KEYS, True), ('CT', CT, PARITY_T_KEYS, False)):
        for k in keys:
            it = rec['items'].get(k)
            if it is None:
                if need:
                    bad.append('%s %s missing' % (src, k))
                continue
            for f in PARITY_FIELDS:
                if f not in it:
                    bad.append('%s %s: no %s' % (src, k, f))
                elif not parity_zero(it[f]):
                    bad.append('%s %s: %s nonzero' % (src, k, f))
    return bad


VERDICT_FUNCS = ('Ctx', 'D', 'lift', 'dsum', 'nn', 'sqrt_any', 'chol', 'lsolve', 'congruent', 'pieces', 't_interval', 'ritz_matrix',
                 'gersh_lo', 'radius_const', 'udiffs', 'ud_kind', 'centered', 'quantities', 'mode', 'pj', 'pm', 's7mono_hyp', 'coverage',
                 'coverage_claim', 'claim_holds', 's5_parts', 's5_bound', 'piece_eval', 'isect', 'pmax', 'pmin', 'finite',
                 'pt', 'dec_frac', 'dec_iv', 's4u_read_port', 's4u_ball', 's4u_src_check', 's4u_pos', 'provide_s4u', 'tag_certified',
                 'verdict_word', 'u_minus_float', 'ceil_sig', 's4_kr34',    # N-a: pt(), the S4-U provider, its readers, the tag functions
                 's4t_src_check', 'provide_s4trb',                         # v2_1: the S4-TRB provider and its source check
                 'r_main_iv', 'det_iv',                                    # v2_2 (1): r_main in mp.iv
                 'verdict_lines_ok', 'marked_precert',                     # P2-11 draft: the exact VERDICT and PRECERT tests
                 'width_exps', 'tw_abs', 'tw_mode',                        # P2-11: the width-aware second-order terms
                 'kind_hyp', 'kind_slack', 'kind_holds', 'kind_profile', 'kind_dmin', 'kind_scale',   # P2-11 step 3: the C2-a kinds
                 'kind_hr_dmin',                                           # the hand-off rule
                 'joint_slack', 'joint_holds', 'joint_profile', 'joint_hr_dmin', 'joint_grid', 'joint_read',   # P2-14: the joint kind
                 'kind_level', 'joint_level', 'plan_dh',                   # the claim and planning thresholds, the headroom table
                 'frac_end', 'm3_iv', 'm3_contains', 'provide_m3',         # the M3 provider (certified snapshot)
                 't_read', 't_scan_inputs',                                # the certified snapshot's t provider
                 'c2a_add', 'c2a_acc',                                     # the C2-a accumulators
                 'vac_law_v1', 'vac_terms', 'm2b_monotone', 'm2b_keys', 'm2b_law300', 'provide_m2b',   # the M2(b) provider, LAW v1
                 'm2b_end', 'm2b_list',
                 'bound_ok', 'c2a_tags',                                   # rule V2 for pk15's records; the C2-a input tags
                 'provide_tin', 'provide_joint', 's4u_bump', 'dec_half',   # their plant copies are built from strings
                 'float_in_empty',                                         # the FLOAT_IN status rule for pk15's exports
                 'c_trial',                                                # the C-TRIAL: one trial set for M3 and m-hat
                 'parity_zero', 'parity_bad',                              # C-PARITY on every field, bars included
                 'c_trial_chain',                                          # main, pk03: C-TRIAL's record -> asm -> script chain
                 'm2b_local_ok', 'm2b_local_plants',                       # the certified M2(b) branch's local second check
                 's4h_src_check', 's4h_diag_bad', 's4h_rowswap', 'mhat_bad', 'bh_bound', 'provide_bh',   # v1_1 P-3: the beta_H provider
                 'm2b_trial_bad',                                          # v1_1 P-1: C-TRIAL on the certified M2(b) record
                 'vert_only_bad', 'c_vert_only')                           # v1_2: C-VERT-ONLY
FORBIDDEN = (r'\bnp\.linalg', r'\bsla\.', r'\bmath\.', r'\berfc\b', r'(?<![\w.])float\(', r'\*\* *0?\.5', r'(?<![\w.])pow\(',
             r'\bnumpy\b', r'\bscipy\b', r'\bflint\b')


def module_scan(srcs):
    """C-MODULE: no libm, numpy, scipy, erfc, python-flint, float conversion or fractional power in a verdict-path function or class.
    The allowed float uses sit outside: the eigh preconditioner (ritz_basis, an exact matrix afterwards), the index order
    (order_from_central, any fixed choice is valid) and the FLOAT providers (vac_float), which the certified item replaces."""
    return [(name, pat) for name, src in sorted(srcs.items()) for pat in FORBIDDEN if re.search(pat, src)]


def tag_certified(name, tag, pins=None):
    """F1, the allowlist: a tag is certified only if it equals 'CERTIFIED <producer> <sha8>' exactly, with that input's pinned producer
    and sha8 (TAG_PINS, or the control's pins). Anything else reads not certified: 'FLOAT ...', 'S4-TRB, pending', 'PENDING', a typo,
    another producer or sha8, an input without a pin."""
    pins = TAG_PINS if pins is None else pins
    return name in pins and tag == 'CERTIFIED %s %s' % pins[name]


def verdict_word(tags, passed, pins=None):
    """C-TAG: FAIL if the verdict fails; CERTIFIED only when every input tag is certified (tag_certified); FLOAT-PASS otherwise, which
    covers P4's partial flips. (v1_2's 'declared' argument is gone: the tags alone decide, through the allowlist.)"""
    if not passed:
        return 'FAIL'
    return 'CERTIFIED' if (len(tags) > 0 and all(tag_certified(k, v, pins) for k, v in tags.items())) else 'FLOAT-PASS'


class BudgetShort(Exception):
    pass


def budget(need, what):
    """stop cleanly (INCOMPLETE) when fewer than need CPU seconds remain before the soft cap."""
    if cpu() + need > LIM - 2:
        raise BudgetShort('%s at cpu %.1f s' % (what, cpu()))


# ------------------------------------------------------------------ the S4-U provider (F1, F2, S3) and the margin plants (S1, D2)
S4U_BALLS = ('LEAD', 'C1', 'C2', 'C3')
S4U_HEADER = dict(FORMAT=S4U['fmt'], RECORD=S4U['record'], END=S4U['record'], AUTHOR=S4U['producer'], J_MIN='300',
                  TARGET_U_MINUS_FLOAT='7.8e-4', TARGET_QUAD='3.9e-4')
# D-1: R_CERT's pieces, each with its record keys for the output and the code, and the READING line of that asm output (N filled in)
S4U_PIECES = (('PREF2_RE', 'PREF2_RE_OUTPUT', 'PREF2_RE_CODE',
               r'READING N=%d \(t = 1/300, every J >= 300\): pref\^2 R_E <= ([0-9.e+-]+); .*'),
              ('PREF2_RHO4', 'PREF2_RHO4_OUTPUT', 'PREF2_RHO4_CODE',
               r'READING N=%d \(t = 1/300, every J >= 300; S4_M2C_DESIGN_v1\): pref\^2 rho4 <= ([0-9.e+-]+); .*'),
              ('M3_SUM', 'M3_OUTPUT', 'M3_CODE',
               r'READING N=%d \(t = 1/300, every J >= 300\): pref\^2 \(tail \+ annulus\) \+ far \+ equator <= ([0-9.e+-]+)'))
S4U_PER_N = (tuple(b + e for b in S4U_BALLS for e in ('', '_LO', '_HI')) + tuple(k for pc in S4U_PIECES for k in pc[:3])
             + ('R_CERT', 'QUAD_TW_PART', 'QUAD_TW_PART_EXACT', 'U_MINUS_FLOAT', 'U_EXACT', 'COEF_OUTPUT', 'U3_CODE'))
S4U_USED = tuple(S4U_HEADER) + tuple('N%d_%s' % (N, k) for N in (4, 3) for k in S4U_PER_N)


def dec_frac(s):
    """an S4U_KV_v1 number (a decimal with optional sign, fraction and exponent) as an exact rational; anything else is an error."""
    if not isinstance(s, str) or re.fullmatch(r'-?[0-9]+(\.[0-9]+)?(e[+-]?[0-9]+)?', s) is None:
        raise ValueError('not a decimal number: %r' % (s,))
    return Fraction(s)


def dec_iv(s):
    """the exact decimal s as an mp.iv enclosure: numerator / denominator in outward interval arithmetic (no decimal string rounding)."""
    q = dec_frac(s)
    return pt(q.numerator) / pt(q.denominator)


def verdict_lines_ok(lines):
    """a producing output is accepted only if its VERDICT lines are exactly ['VERDICT VALID'], by equality; a variant
    such as 'VERDICT VALID-PRECERT' or 'VERDICT VALID-STUB', or a second VERDICT line, refuses it."""
    return [ln for ln in lines if ln.startswith('VERDICT')] == ['VERDICT VALID']


def precert_copy(text, tag='PRECERT'):
    """the plants: a copy of a producing output whose VERDICT VALID line reads VERDICT VALID-<tag>."""
    return '\n'.join(('VERDICT VALID-' + tag) if ln == 'VERDICT VALID' else ln for ln in text.split('\n'))


def marked_precert(rec):
    """a record whose FORMAT, RECORD, END or any CLAIM* key marks it PRECERT or STUB is refused. True if marked."""
    return any(('PRECERT' in v.upper() or 'STUB' in v.upper()) for k, v in rec.items()
               if k in ('FORMAT', 'RECORD', 'END') or k.startswith('CLAIM'))


def s4u_read_port(text):
    """the port's reader of format S4U_KV_v1 (S3): the text split at newlines; a line starting with # is a comment and a blank line
    carries nothing; every other line is KEY = value with KEY of [A-Z][A-Z0-9_]*, cut at its first ' = ', the value kept as it stands;
    any other line or a repeated KEY is an error. It shares no code with the reference parser (S4U_REF), which C-FMT holds it against."""
    rec = {}
    for no, ln in enumerate(text.split('\n'), 1):
        if ln.startswith('#') or ln.strip() == '':
            continue
        key, sep, val = ln.partition(' = ')
        if sep != ' = ' or re.fullmatch(r'[A-Z][A-Z0-9_]*', key) is None or key in rec:
            raise ValueError('S4U_KV_v1, port reader: line %d is not a new KEY = value' % no)
        rec[key] = val
    return rec


def s4u_ball(s):
    """a printed ball '[mid +/- rad]' of s4c_m2ba as the exact pair (mid, rad)."""
    m = re.fullmatch(r'\[([0-9.e+-]+) \+/- ([0-9.e+-]+)\]', s) if isinstance(s, str) else None
    if m is None:
        raise ValueError('not a ball: %r' % (s,))
    return dec_frac(m.group(1)), dec_frac(m.group(2))


def ceil_sig(x, n):
    """the smallest decimal with n significant digits that is >= x, for x > 0, exactly (the record's 'rounded up at 3 digits')."""
    e = 0
    while x >= Fraction(10) ** (e + n):
        e += 1
    while x < Fraction(10) ** (e + n - 1):
        e -= 1
    q = x / Fraction(10) ** e
    return -((-q.numerator) // q.denominator) * Fraction(10) ** e


def s4u_src_check(rec, srcs, asm):
    """C-SRC (S3, D-1), per N, against sha-pinned producing outputs. (a) The balls N*_LEAD and N*_C1..C3 equal, as strings, those of
    s4c_m2ba's C-NORM and C-C123 lines (srcs[N]: each line found once and reading PASS; its C-POS line PASS, its verdict VALID, its
    header ITEM n<N>); N*_COEF_OUTPUT names that output and N*_U3_CODE the code sha8 of its header; every *_LO and *_HI equals
    mid - rad and mid + rad exactly. (b) D-1: N*_PREF2_RE, N*_PREF2_RHO4 and N*_M3_SUM equal, as strings, the READING lines of their asm
    outputs (asm[(N, key)]: each line found once, with CHECKS all PASS, VERDICT VALID and the header ITEM=n<N> asm); the record's
    _OUTPUT token names that output and its first _CODE token the program and code sha8 of that header; N*_R_CERT is their exact sum
    (R_CERT_RULE); N*_QUAD_TW_PART_EXACT is 0.071 (PREF2_RE + PREF2_RHO4) + M3_SUM + 1e-11 exactly and N*_QUAD_TW_PART is it rounded up
    at 3 significant digits (QUAD_TW_PART_RULE). Returns the failures."""
    bad = []
    for N in (4, 3):
        p = 'N%d_' % N
        lines = srcs[N].split('\n')
        pats = dict(norm=r'C-NORM N=%d: pref\^2 J0 = (\[[^\]]*\]): PASS' % N,
                    c123=r'C-C123 N=%d: c1 = (\[[^\]]*\]), c2 = (\[[^\]]*\]), c3 = (\[[^\]]*\]) \(twrig6z [^)]*\), window 1e-6: PASS' % N,
                    pos=r'C-POS N=%d: c1, c2, c3 > 0: PASS' % N,
                    head=r's4c_m2ba sha256 ([0-9a-f]{64}) ITEM=n%d LIM=[0-9]+' % N)
        hit = {}
        for k, pat in pats.items():
            ms = [m for m in (re.fullmatch(pat, ln) for ln in lines) if m is not None]
            if len(ms) == 1:
                hit[k] = ms[0]
            else:
                bad.append('%ss4c line %s found %d times' % (p, k, len(ms)))
        if not verdict_lines_ok(lines):                                      # T48: exact VERDICT lines
            bad.append('%ss4c VERDICT lines not exactly VERDICT VALID' % p)
        if 'norm' in hit and rec.get(p + 'LEAD') != hit['norm'].group(1):
            bad.append(p + 'LEAD against C-NORM')
        for i in (1, 2, 3):
            if 'c123' in hit and rec.get(p + 'C%d' % i) != hit['c123'].group(i):
                bad.append(p + 'C%d against C-C123' % i)
        if rec.get(p + 'COEF_OUTPUT') != '%s:%s' % (S4U_SRC[N][0], S4U_SRC[N][1][:8]):
            bad.append(p + 'COEF_OUTPUT')
        if 'head' in hit and rec.get(p + 'U3_CODE') != 'pk05/s4c_m2ba.py:%s' % hit['head'].group(1)[:8]:
            bad.append(p + 'U3_CODE against the header')
        for b in S4U_BALLS:
            try:
                mid, rad = s4u_ball(rec.get(p + b))
                if dec_frac(rec.get(p + b + '_LO')) != mid - rad:
                    bad.append(p + b + '_LO')
                if dec_frac(rec.get(p + b + '_HI')) != mid + rad:
                    bad.append(p + b + '_HI')
            except ValueError:
                bad.append(p + b + ' unreadable')
        for key, okey, ckey, rpat in S4U_PIECES:                         # D-1
            lines = asm[(N, key)].split('\n')
            pats = dict(reading=rpat % N, checks=r'CHECKS all PASS',
                        head=r'(px08_[a-z0-9_]+) sha256 ([0-9a-f]{64}) ITEM=n%d asm LIM=[0-9]+.*' % N)
            hit = {}
            for k, pat in pats.items():
                ms = [m for m in (re.fullmatch(pat, ln) for ln in lines) if m is not None]
                if len(ms) == 1:
                    hit[k] = ms[0]
                else:
                    bad.append('%s%s: asm line %s found %d times' % (p, key, k, len(ms)))
            if not verdict_lines_ok(lines):                                  # T48: exact VERDICT lines
                bad.append('%s%s: asm VERDICT lines not exactly VERDICT VALID' % (p, key))
            if 'reading' in hit and rec.get(p + key) != hit['reading'].group(1):
                bad.append(p + key + ' against its READING')
            if rec.get(p + okey) != '%s:%s' % (S4U_ASM[(N, key)][0], S4U_ASM[(N, key)][1][:8]):
                bad.append(p + okey)
            if 'head' in hit and str(rec.get(p + ckey)).split(' ; ')[0] != 'pk08/%s.py:%s' % (hit['head'].group(1),
                                                                                                hit['head'].group(2)[:8]):
                bad.append(p + ckey + ' against the header')
        try:
            r_e, r_h, m_3 = (dec_frac(rec.get(p + k)) for k in ('PREF2_RE', 'PREF2_RHO4', 'M3_SUM'))
            if dec_frac(rec.get(p + 'R_CERT')) != r_e + r_h + m_3:
                bad.append(p + 'R_CERT (R_CERT_RULE)')
            qx = dec_frac(rec.get(p + 'QUAD_TW_PART_EXACT'))
            if qx != dec_frac('0.071') * (r_e + r_h) + m_3 + dec_frac('1e-11'):
                bad.append(p + 'QUAD_TW_PART_EXACT (QUAD_TW_PART_RULE)')
            if qx <= 0 or dec_frac(rec.get(p + 'QUAD_TW_PART')) != ceil_sig(qx, 3):
                bad.append(p + 'QUAD_TW_PART (rounded up at 3 digits)')
        except ValueError:
            bad.append(p + 'R_CERT or QUAD_TW_PART unreadable')
    return bad


def s4u_pos(rec):
    """C-POS (F2): N*_LEAD_LO, N*_C1_LO, N*_C2_LO, N*_C3_LO > 0 exactly. With lead in [LEAD_LO, LEAD_HI] and c_i in [C_i_LO, C_i_HI]
    this gives lead (1 + c1 t + c2 t^2 + c3 t^3) <= LEAD_HI (1 + C1_HI t + C2_HI t^2 + C3_HI t^3) for every t > 0. Returns the failing
    keys; an unreadable value fails."""
    bad = []
    for N in (4, 3):
        for b in S4U_BALLS:
            k = 'N%d_%s_LO' % (N, b)
            try:
                if not dec_frac(rec.get(k)) > 0:
                    bad.append(k)
            except ValueError:
                bad.append(k)
    return bad


def s4u_swap(text, k1, k2):
    """a copy of the record's text with the values of the keys k1 and k2 exchanged (PLANT-FMT-S4U, PLANT-KEYSWAP)."""
    lines = text.split('\n')
    i1 = [i for i, ln in enumerate(lines) if ln.startswith(k1 + ' = ')]
    i2 = [i for i, ln in enumerate(lines) if ln.startswith(k2 + ' = ')]
    assert len(i1) == 1 and len(i2) == 1, 'the keys to swap are not each on one line'
    v1, v2 = lines[i1[0]][len(k1) + 3:], lines[i2[0]][len(k2) + 3:]
    lines[i1[0]], lines[i2[0]] = k1 + ' = ' + v2, k2 + ' = ' + v1
    return '\n'.join(lines)


def s4u_bump(s):
    """the decimal string s with the last digit of its mantissa moved by one (PLANT-RSRC)."""
    m = re.fullmatch(r'([^e]*)([0-9])(e[+-]?[0-9]+)?', s)
    return m.group(1) + str((int(m.group(2)) + 1) % 10) + (m.group(3) or '')


def dec_half(s):
    """half of the decimal string s, as an exact decimal string (the denominator stays 2^a 5^b, so the loop ends; PLANT-SRC-J)."""
    q = dec_frac(s) / 2
    k = 0
    while (q * 10 ** k).denominator != 1:
        k += 1
    return '%de-%d' % ((q * 10 ** k).numerator, k)


def provide_s4u(fails, fires):
    """the S4-U provider (F1, F2, S3, D-1). It reads pk08's record once and checks the bytes it parses (C-HASH, full sha256), parses
    them with the port's reader and with the reference parser (executed only after its own sha256 matches), and requires C-FMT (the
    two readers give the same keys and values, every key the port uses is present, the header keys are as pinned), C-SRC (s4c_m2ba's
    outputs and the three asm outputs per N, all sha-pinned) and C-POS, and that PLANT-FMT-S4U, PLANT-KEYSWAP, PLANT-RSRC and PLANT-POS
    fire. Only then does it set TAGS['S4 U'] to 'CERTIFIED <producer> <sha8>'. Returns, per N, the port's U tuple (LEAD_HI, C1_HI,
    C2_HI, C3_HI, R_CERT as exact-decimal enclosures) and the record's N*_QUAD_TW_PART and N*_U_MINUS_FLOAT strings."""
    with open(os.path.join(CODEDIR, S4U['path']), 'rb') as fh:
        raw = fh.read()
    with open(os.path.join(CODEDIR, S4U_REF[0]), 'rb') as fh:
        refb = fh.read()
    srcb, asmb = {}, {}
    for N in (4, 3):
        with open(os.path.join(CODEDIR, S4U_SRC[N][0]), 'rb') as fh:
            srcb[N] = fh.read()
    for nk, (path, _) in S4U_ASM.items():
        with open(os.path.join(CODEDIR, path), 'rb') as fh:
            asmb[nk] = fh.read()
    ok_h = (sha_bytes(raw) == S4U['sha256'], sha_bytes(refb) == S4U_REF[1], all(sha_bytes(srcb[N]) == S4U_SRC[N][1] for N in (4, 3)),
            all(sha_bytes(asmb[nk]) == S4U_ASM[nk][1] for nk in S4U_ASM))
    out('C-HASH S4-U (full sha256 of the bytes read here): record %s %s, reference parser %s %s, s4c_m2ba outputs %s, the %d asm '
        'outputs %s -> %s' % (S4U['path'], 'matches' if ok_h[0] else 'DIFFERS', S4U_REF[0], 'matches' if ok_h[1] else 'DIFFERS',
                              'match' if ok_h[2] else 'DIFFER', len(S4U_ASM), 'match' if ok_h[3] else 'DIFFER',
                              'PASS' if all(ok_h) else 'FAIL'))
    if not all(ok_h):
        fails.append('C-HASH S4-U')
        raise RuntimeError('S4-U provider: a pinned file differs from its pin; nothing is read from it')
    text = raw.decode('utf-8')
    srcs = {N: srcb[N].decode('utf-8') for N in (4, 3)}
    asm = {nk: asmb[nk].decode('utf-8') for nk in S4U_ASM}
    ns = {}
    exec(compile(refb.decode('utf-8'), S4U_REF[0], 'exec'), ns)
    ref_parse = ns['parse_s4u_kv']
    port, ref = s4u_read_port(text), ref_parse(text)
    diff = sorted(k for k in set(port) | set(ref) if port.get(k) != ref.get(k))
    miss = [k for k in S4U_USED if k not in port]
    hdr = [k for k, v in S4U_HEADER.items() if port.get(k) != v]
    prec = marked_precert(port)                                         # T48: a PRECERT or STUB record is refused
    ok_fmt = not diff and not miss and not hdr and not prec
    out('C-FMT S4-U (format %s): %d keys; the port\'s reader against the reference parser (%s, sha256 %s): %s; the %d keys the port uses '
        'present: %s; header keys %s as pinned: %s; marked PRECERT or STUB (T48): %s -> %s' % (
            S4U['fmt'], len(port), S4U_REF[0], S4U_REF[1][:8], 'identical' if not diff else 'DIFFER on %s' % ', '.join(diff[:6]),
            len(S4U_USED), 'yes' if not miss else 'NO (%s)' % ', '.join(miss[:6]), ', '.join(S4U_HEADER),
            'yes' if not hdr else 'NO (%s)' % ', '.join(hdr), prec, 'PASS' if ok_fmt else 'FAIL'))
    if not ok_fmt:
        fails.append('C-FMT S4-U')
    src_bad = s4u_src_check(port, srcs, asm)
    out('C-SRC S4-U: N*_LEAD and N*_C1..C3 against the C-NORM and C-C123 lines of %s and %s (C-POS PASS and VERDICT VALID there), '
        'COEF_OUTPUT and U3_CODE, the 16 _LO/_HI ends as mid -+ rad exactly; D-1: N*_PREF2_RE, N*_PREF2_RHO4 and N*_M3_SUM against the '
        'READING lines of %s (CHECKS all PASS and VERDICT VALID there), their _OUTPUT and _CODE tokens, R_CERT = PREF2_RE + PREF2_RHO4 '
        '+ M3_SUM exactly, QUAD_TW_PART_EXACT = 0.071 (PREF2_RE + PREF2_RHO4) + M3_SUM + 1e-11 exactly and QUAD_TW_PART = it rounded up '
        'at 3 digits -> %s' % (S4U_SRC[4][0], S4U_SRC[3][0], ', '.join(S4U_ASM[nk][0] for nk in sorted(S4U_ASM)),
                              'PASS' if not src_bad else 'FAIL (%s)' % ', '.join(src_bad[:6])))
    if src_bad:
        fails.append('C-SRC S4-U')
    pos_bad = s4u_pos(port)
    out('C-POS S4-U: N*_LEAD_LO, N*_C1_LO, N*_C2_LO, N*_C3_LO > 0 exactly, so the HI ends bound U3 from above for t > 0 -> %s' % (
        'PASS' if not pos_bad else 'FAIL (%s)' % ', '.join(pos_bad)))
    if pos_bad:
        fails.append('C-POS S4-U')
    sw = s4u_swap(text, 'N4_C1_HI', 'N4_C2_HI')
    port_sw, ref_sw = s4u_read_port(sw), ref_parse(sw)
    fired_f = sw != text and port_sw != ref
    out('PLANT-FMT-S4U (the port reads a copy with N4_C1_HI and N4_C2_HI swapped, the reference parser reads the record): C-FMT %s -> %s'
        % ('differs' if port_sw != ref else 'agrees', 'FIRES' if fired_f else 'DOES NOT FIRE'))
    if not fired_f:
        fires.append('PLANT-FMT-S4U')
    sw_bad = s4u_src_check(port_sw, srcs, asm)
    fired_k = sw != text and port_sw == ref_sw and bool(sw_bad)
    out('PLANT-KEYSWAP (both readers read the swapped copy): they agree: %s; C-SRC fails on %s -> %s' % (
        port_sw == ref_sw, ', '.join(sw_bad) if sw_bad else 'nothing', 'FIRES' if fired_k else 'DOES NOT FIRE'))
    if not fired_k:
        fires.append('PLANT-KEYSWAP')
    bumped = s4u_bump(port.get('N4_PREF2_RE', '0'))
    rs_bad = s4u_src_check(dict(port, N4_PREF2_RE=bumped), srcs, asm)
    fired_r = bumped != port.get('N4_PREF2_RE') and 'N4_PREF2_RE against its READING' in rs_bad
    out('PLANT-RSRC (D-1: N4_PREF2_RE set to %s in a copy): C-SRC fails on %s -> %s' % (
        bumped, ', '.join(rs_bad) if rs_bad else 'nothing', 'FIRES' if fired_r else 'DOES NOT FIRE'))
    if not fired_r:
        fires.append('PLANT-RSRC')
    neg_bad = s4u_pos(dict(port, N4_C1_LO='-' + port.get('N4_C1_LO', '')))
    fired_p = 'N4_C1_LO' in neg_bad
    out('PLANT-POS (N4_C1_LO negated in a copy): C-POS flags %s -> %s' % (', '.join(neg_bad) or 'nothing',
                                                                          'FIRES' if fired_p else 'DOES NOT FIRE'))
    if not fired_p:
        fires.append('PLANT-POS')
    pr_rec = marked_precert(dict(port, CLAIM=port.get('CLAIM', '') + ' (PRECERT)'))       # T48: one plant for this reader
    pr_src = s4u_src_check(port, {**srcs, 4: precert_copy(srcs[4])}, asm)
    fired_pr = pr_rec and any('VERDICT' in b for b in pr_src)
    out('PLANT-PRECERT-S4U (T48: a copy of the record with its CLAIM marked PRECERT, and a copy of s4c_m2ba_n4.out reading VERDICT '
        'VALID-PRECERT): record refused %s, output refused %s -> %s' % (pr_rec, any('VERDICT' in b for b in pr_src),
                                                                       'FIRES' if fired_pr else 'DOES NOT FIRE'))
    if not fired_pr:
        fires.append('PLANT-PRECERT-S4U')
    U5, quad, umf = {}, {}, {}
    for N in (4, 3):
        p = 'N%d_' % N
        U5[N] = tuple(dec_iv(port[p + k]) for k in ('LEAD_HI', 'C1_HI', 'C2_HI', 'C3_HI', 'R_CERT'))
        quad[N], umf[N] = port[p + 'QUAD_TW_PART'], port[p + 'U_MINUS_FLOAT']
        ld, c1, c2, c3, rc = U5[N]
        t3 = pt(1) / 300
        u300 = ld * (1 + c1 * t3 + c2 * t3 * t3 + c3 * t3 * t3 * t3) + rc
        ue = dec_iv(port[p + 'U_EXACT'])
        out('INFO S4-U N=%d: the port\'s U at t = 1/300 is %s, below the record\'s U_EXACT %s: %s; as t -> 0 it tends to LEAD_HI + '
            'R_CERT = %s' % (N, str(u300), port[p + 'U_EXACT'], (u300.b <= ue.a) is True, str(ld + rc)))
    if ok_fmt and not src_bad and not pos_bad and fired_f and fired_k and fired_r and fired_p and fired_pr:
        TAGS['S4 U'] = 'CERTIFIED %s %s' % (S4U['producer'], sha_bytes(raw)[:8])
    out('S4-U provider: tag %r (reads certified: %s)' % (TAGS['S4 U'], tag_certified('S4 U', TAGS['S4 U'])))
    return dict(U5=U5, quad=quad, umf=umf)


# ------------------------------------------------------------------ the S4-TRB provider (v2_1)
S4T_HEADER = dict(FORMAT=S4T['fmt'], RECORD=S4T['record'], END=S4T['record'], AUTHOR=S4T['producer'], J_MIN='300',
                  TARGET_T2='N4 1.338859 ; N3 0.961107')
S4T_READ = ('TRB', 'TRB_MAIN', 'TRB_R3', 'TRB_RCUB', 'TRB_RF', 'TRB_TAIL', 'TRB_FAR', 'PR', 'TV')   # the READING line's values, in order
S4T_USED = tuple(S4T_HEADER) + ('CODE', 'CONSTANT_PER_N') + tuple('N%d_%s' % (N, k) for N in (4, 3)
                                                                  for k in S4T_READ + ('ASM_OUTPUT', 'VERDICT', 'T2_RESULT'))
S4T_READING = (r'READING N=%d \(t = 1/300, every J >= 300; S4_TRB_DESIGN_v2 item 2\): TRB_%d <= ([0-9.e+-]+); main <= ([0-9.e+-]+), '
               r'R3 <= ([0-9.e+-]+), R_cub <= ([0-9.e+-]+), R_F <= ([0-9.e+-]+), tail <= ([0-9.e+-]+), far <= ([0-9.e+-]+); '
               r'PR <= ([0-9.e+-]+); T_v <= ([0-9.e+-]+)')


def s4t_src_check(rec, asm):
    """C-SRC S4-TRB (v2_1), per N: N*_TRB, its pieces N*_TRB_MAIN .. N*_TRB_FAR, N*_PR and N*_TV equal, as strings,
    the nine values of the READING line of the sha-pinned asm output asm[N] (found once, with CHECKS all PASS, VERDICT VALID and the
    header ITEM=n<N> asm, whose code sha8 is the record's CODE sha8); N*_ASM_OUTPUT names that output; N*_VERDICT reads VALID and
    N*_T2_RESULT PASS. Returns the failures."""
    bad = []
    for N in (4, 3):
        p = 'N%d_' % N
        lines = asm[N].split('\n')
        pats = dict(reading=S4T_READING % (N, N), checks=r'CHECKS all PASS',
                    head=r'px08_trbcert_[a-z0-9_]+ sha256 ([0-9a-f]{64}) ITEM=n%d asm LIM=[0-9]+.*' % N)
        hit = {}
        for k, pat in pats.items():
            ms = [m for m in (re.fullmatch(pat, ln) for ln in lines) if m is not None]
            if len(ms) == 1:
                hit[k] = ms[0]
            else:
                bad.append('%sasm line %s found %d times' % (p, k, len(ms)))
        if not verdict_lines_ok(lines):                                      # T48: exact VERDICT lines
            bad.append('%sasm VERDICT lines not exactly VERDICT VALID' % p)
        if 'reading' in hit:
            for i, k in enumerate(S4T_READ):
                if rec.get(p + k) != hit['reading'].group(i + 1):
                    bad.append(p + k + ' against its READING')
        if rec.get(p + 'ASM_OUTPUT') != '%s:%s' % (S4T_ASM[N][0], S4T_ASM[N][1][:8]):
            bad.append(p + 'ASM_OUTPUT')
        if 'head' in hit and str(rec.get('CODE')).split(' ; ')[0].rpartition(':')[2] != hit['head'].group(1)[:8]:
            bad.append('CODE against the %sasm header' % p)
        if rec.get(p + 'VERDICT') != 'VALID' or rec.get(p + 'T2_RESULT') != 'PASS':
            bad.append(p + 'VERDICT or T2_RESULT')
    return bad


def provide_s4trb(fails, fires):
    """the S4-TRB provider (v2_1), built like provide_s4u. It reads pk08's TRB record once (C-HASH on the bytes it parses, with the
    reference parser and both asm outputs, full sha256), parses it with the port's S4U_KV_v1 reader and with the same reference parser
    (executed only after its sha256 matches), and requires C-FMT (identical keys and values, the keys the port uses present, the header
    keys as pinned) and C-SRC (s4t_src_check), and that PLANT-FMT-S4T and PLANT-TSRC fire. Only then does it set TAGS['S4 TRB'] to
    'CERTIFIED <producer> <sha8>'. Returns per N the record's N*_TRB as an exact-decimal enclosure (TRBv) and as its string (trb)."""
    with open(os.path.join(CODEDIR, S4T['path']), 'rb') as fh:
        raw = fh.read()
    with open(os.path.join(CODEDIR, S4U_REF[0]), 'rb') as fh:
        refb = fh.read()
    asmb = {}
    for N in (4, 3):
        with open(os.path.join(CODEDIR, S4T_ASM[N][0]), 'rb') as fh:
            asmb[N] = fh.read()
    ok_h = (sha_bytes(raw) == S4T['sha256'], sha_bytes(refb) == S4U_REF[1], all(sha_bytes(asmb[N]) == S4T_ASM[N][1] for N in (4, 3)))
    out('C-HASH S4-TRB (full sha256 of the bytes read here): record %s %s, reference parser %s %s, the 2 asm outputs %s -> %s' % (
        S4T['path'], 'matches' if ok_h[0] else 'DIFFERS', S4U_REF[0], 'matches' if ok_h[1] else 'DIFFERS',
        'match' if ok_h[2] else 'DIFFER', 'PASS' if all(ok_h) else 'FAIL'))
    if not all(ok_h):
        fails.append('C-HASH S4-TRB')
        raise RuntimeError('S4-TRB provider: a pinned file differs from its pin; nothing is read from it')
    text = raw.decode('utf-8')
    asm = {N: asmb[N].decode('utf-8') for N in (4, 3)}
    ns = {}
    exec(compile(refb.decode('utf-8'), S4U_REF[0], 'exec'), ns)
    ref_parse = ns['parse_s4u_kv']
    port, ref = s4u_read_port(text), ref_parse(text)
    diff = sorted(k for k in set(port) | set(ref) if port.get(k) != ref.get(k))
    miss = [k for k in S4T_USED if k not in port]
    hdr = [k for k, v in S4T_HEADER.items() if port.get(k) != v]
    prec = marked_precert(port)                                         # T48: a PRECERT or STUB record is refused
    ok_fmt = not diff and not miss and not hdr and not prec
    out('C-FMT S4-TRB (format %s): %d keys; the port\'s reader against the reference parser (%s, sha256 %s): %s; the %d keys the port '
        'uses present: %s; header keys %s as pinned: %s; marked PRECERT or STUB (T48): %s -> %s' % (
            S4T['fmt'], len(port), S4U_REF[0], S4U_REF[1][:8], 'identical' if not diff else 'DIFFER on %s' % ', '.join(diff[:6]),
            len(S4T_USED), 'yes' if not miss else 'NO (%s)' % ', '.join(miss[:6]), ', '.join(S4T_HEADER),
            'yes' if not hdr else 'NO (%s)' % ', '.join(hdr), prec, 'PASS' if ok_fmt else 'FAIL'))
    if not ok_fmt:
        fails.append('C-FMT S4-TRB')
    src_bad = s4t_src_check(port, asm)
    out('C-SRC S4-TRB: N*_TRB, N*_TRB_MAIN .. N*_TRB_FAR, N*_PR and N*_TV against the READING lines of %s and %s (CHECKS all PASS and '
        'VERDICT VALID there, the header\'s code sha8 = the record\'s CODE), N*_ASM_OUTPUT, N*_VERDICT VALID, N*_T2_RESULT PASS -> %s' % (
            S4T_ASM[4][0], S4T_ASM[3][0], 'PASS' if not src_bad else 'FAIL (%s)' % ', '.join(src_bad[:6])))
    if src_bad:
        fails.append('C-SRC S4-TRB')
    sw = s4u_swap(text, 'N4_TRB', 'N3_TRB')
    port_sw = s4u_read_port(sw)
    fired_f = sw != text and port_sw != ref
    out('PLANT-FMT-S4T (the port reads a copy with N4_TRB and N3_TRB swapped, the reference parser reads the record): C-FMT %s -> %s' % (
        'differs' if port_sw != ref else 'agrees', 'FIRES' if fired_f else 'DOES NOT FIRE'))
    if not fired_f:
        fires.append('PLANT-FMT-S4T')
    bumped = s4u_bump(port.get('N4_TRB', '0'))
    ts_bad = s4t_src_check(dict(port, N4_TRB=bumped), asm)
    fired_t = bumped != port.get('N4_TRB') and 'N4_TRB against its READING' in ts_bad
    out('PLANT-TSRC (N4_TRB set to %s in a copy): C-SRC fails on %s -> %s' % (
        bumped, ', '.join(ts_bad) if ts_bad else 'nothing', 'FIRES' if fired_t else 'DOES NOT FIRE'))
    if not fired_t:
        fires.append('PLANT-TSRC')
    pr_rec = marked_precert(dict(port, FORMAT=port.get('FORMAT', '') + '-STUB'))           # T48: one plant for this reader
    pr_src = s4t_src_check(port, {**asm, 4: precert_copy(asm[4])})
    fired_pr = pr_rec and any('VERDICT' in b for b in pr_src)
    out('PLANT-PRECERT-S4T (T48: a copy of the record with FORMAT S4U_KV_v1-STUB, and a copy of the N4 asm output reading VERDICT '
        'VALID-PRECERT): record refused %s, output refused %s -> %s' % (pr_rec, any('VERDICT' in b for b in pr_src),
                                                                       'FIRES' if fired_pr else 'DOES NOT FIRE'))
    if not fired_pr:
        fires.append('PLANT-PRECERT-S4T')
    TRBv, trb = {}, {}
    for N in (4, 3):
        trb[N] = port['N%d_TRB' % N]
        TRBv[N] = dec_iv(trb[N])
        out('INFO S4-TRB N=%d: certified TRB %s, enclosed as %s, for every J >= 300 (CONSTANT_PER_N); the FLOAT TRB of PARAMS was %s' % (
            N, trb[N], str(TRBv[N]), PARAMS[N]['TRB']))
    if ok_fmt and not src_bad and fired_f and fired_t and fired_pr:
        TAGS['S4 TRB'] = 'CERTIFIED %s %s' % (S4T['producer'], sha_bytes(raw)[:8])
    out('S4-TRB provider: tag %r (reads certified: %s)' % (TAGS['S4 TRB'], tag_certified('S4 TRB', TAGS['S4 TRB'])))
    return dict(TRBv=TRBv, trb=trb)


# ------------------------------------------------------------------ the M3 provider (v2_3's item, for the certified snapshot): pk03's records
M3_LOADER = ('pk03/m3_reader_v4_4.py', 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0')   # the bound loader
M3_FAMILIES = (('M2', 'm2'), ('B5', 'b5'), ('CT', 'clT'), ('B4', 'binding4'), ('EW', 'endw'))   # (the port's source, the record's family)
M3_MODE = 'certified'     # 'mock': pk07's STUB records (mocks/, FLOAT J = 170 values) read by load_noncert; 'certified': M3_CERT by
                          # load for every N; 'mixed': M3_CERT by load for the N it holds, the mocks for the rest (the tag stays MOCK)
M3_MOCK = {N: dict(asm=None, files={f: ('pk07/mocks/m3_%s_N%d_J300_mock.json' % (f, N), s) for f, s in shas.items()})
           for N, shas in ((4, dict(m2='3cbbbec9d2068e5365457676d02bcc3acc8eb6e353968802e2414ecc5d98cbf8',
                                    b5='5dd99c5f599752cf68b7b1b89731557cc88f013630a90b87090877775a16e904',
                                    clT='51643c4b2520c7918607fddd625d320f9b300405d826419d12a658f0a4a2e9e8',
                                    binding4='8b07872868544cb124ce17e5b2c46b26124766c514a50de4a9cd44bfc63e7b38',
                                    endw='ad8f10715df9d186e9079847a009486d5bd5f2b65fb3426d70b88262dcf74df3')),
                               (3, dict(m2='593b9463f4aedef2eb5958e276a9155922778d7f01289864c087957656d6d270',
                                    b5='40d52ecde818ed6150dd4821de9204c4a67f7db7cd88d1f1ea35eee419530dbe',
                                    clT='2ec56da14ec98b0438fd9168c1a6dfa6096169b508967b2e2cbd34151151d9b6',
                                    binding4='75e0d03c6fb598d50c1768fba9f1806487691dfadc72972f0641289338554902',
                                    endw='7b598087953a4e66fb9371f12f26593bfcce1ed7867751b688fc952f46188ae4')))}
M3_CERT = {4: dict(asm=('pk03/out/m3_run_v1_7_asm.4.out', 'a5b294f364f9399b9d12f89af6ce1a1e598b8b424bc6e60d35e122ebd1391b97'),
                   files=dict(m2=('pk03/out/m3_m2_N4_J300_v1_7.json',                  # m3_run_v1_7 e55c5de1, VERDICT VALID; side
                                  'b543699f75af68cec436daf5eeed7cde49a6b1368c738bc9e6de4ddea10e5603'),   # manifest
                              b5=('pk03/out/m3_b5_N4_J300_v1_7.json',                  # MANIFEST_m3_run_v1_7_asm.4.sha256 f8fe854a
                                  '77f83bc79060bae4c34de47884f00d48e6403fee995e3e54dab6781e4c527b3a'),
                              clT=('pk03/out/m3_clT_N4_J300_v1_7.json',
                                   '583c855de6fc7b7a91455092b4aebb57fb9686f1dccb086d1966bc7e5eed80e7'),
                              binding4=('pk03/out/m3_binding4_N4_J300_v1_7.json',
                                        '168b4d7e68c61c6822158d653f7a0f69c606ba7d663ab39f90ef191662328300'),
                              endw=('pk03/out/m3_endw_N4_J300_v1_7.json',
                                    '436a143918fa2ebaa68ee3d16fab632c27bd29b822d4c7052c92dc257eaf88af'))),
           3: dict(asm=('pk03/out/m3_run_v1_7_asm.3.out', '18964e97c320395f44b5923d132b1ac65c95b935cc8708a50e197076cc24e0dc'),
                   files=dict(m2=('pk03/out/m3_m2_N3_J300_v1_7.json',                  # m3_run_v1_7 e55c5de1, VERDICT VALID; side
                                  '6e0d7e498bae8d87c9f0af49fb63704f29207929089e05d4da1fbfac5c72778b'),   # manifest
                              b5=('pk03/out/m3_b5_N3_J300_v1_7.json',                  # MANIFEST_m3_run_v1_7_asm.3.sha256 a4e1681b
                                  '411913043ce7c90970f8fc35918e6c221af2eb025b728dde6f55b755646ab8d3'),
                              clT=('pk03/out/m3_clT_N3_J300_v1_7.json',
                                   '789df4d0054b51f8426f3bbf6f0cac31ebb74deed0684505ed5c9dde6135153e'),
                              binding4=('pk03/out/m3_binding4_N3_J300_v1_7.json',
                                        '887f4a16098695d6052b1ce197b855ffa8e4e0967e9e422d57829c0b09f1db6e'),
                              endw=('pk03/out/m3_endw_N3_J300_v1_7.json',
                                    '5e94d11eea2e6f55e7db781e02c197649ec6f10d8ab15a8f3508805642ed7885')))}
#                           pk03's certified records, {N: dict(asm=(path, sha256), files={family: (path, sha256)})}
M3_TAG_PIN = ('pk03', '64533925')   # TAG_PINS['M3 entries']: the run m3_run_v1_7 (script sha256 e55c5de1..., in both asm outputs'
#                                         headers) that wrote every pinned record; the records and asm outputs are pinned by full sha256
M3_CONV_TESTS = ((Fraction('-0.4409') - Fraction('1e-12'), Fraction('-0.4409') + Fraction('1e-12')),   # a negative ball,
                 (Fraction('1e-13') - Fraction('1e-12'), Fraction('1e-13') + Fraction('1e-12')),     # one straddling zero,
                 (Fraction(-1, 4), Fraction(1, 4)), (Fraction(0), Fraction(1, 2)), (Fraction(-1, 2), Fraction(0)))   # symmetric, zero ends


def frac_end(t):
    """an mp.iv endpoint's raw tuple (sign, man, exp, bc) as an exact Fraction, the sign kept (libmp.to_man_exp would drop it); a
    special value (inf, nan) raises."""
    sign, man, exp, bc = t
    if not man:
        if exp:
            raise ValueError('special value %r' % (t,))
        return Fraction(0)
    v = Fraction(int(man)) * Fraction(2) ** int(exp)
    return -v if sign else v


def m3_iv(lo, hi):
    """M3's exact ball ends [lo, hi] (Fractions, lo <= hi) as an mp.iv interval: numerator / denominator in outward interval arithmetic,
    the signs kept."""
    a = pt(lo.numerator) / pt(lo.denominator)
    b = pt(hi.numerator) / pt(hi.denominator)
    return iv.mpf([a.a, b.b])


def m3_contains(I, lo, hi):
    """C-FMT M3's conversion test: the interval I contains the exact ends lo and hi (exact Fraction comparisons of I's raw ends)."""
    l, h = I._mpi_
    return frac_end(l) <= lo and hi <= frac_end(h)


TRIAL_SET = {4: dict(ts=('pk11/out/ts_N4_J170_D_S_z9sym_v1.json', 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d'),
                     vacres=('pk11/out/vacres_K3_N4_sym_v1.json', 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e')),
             3: dict(ts=('pk11/out/ts_N3_S_z9sym_v1.json', 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6'),
                     vacres=('pk11/out/vacres_K3_N3_sym_v1.json', 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0'))}
#            the C-TRIAL: the z9sym trial states and the symmetrized trial vacres that pk03's S7 records name (trial_set), full
#            sha256 of the files read here (pk03 to confirm them through m3_run_v1_7's manifest)


M3_RUN = ('pk03/m3_run_v1_7.py', '645339250075b69103748f55c789c7772c91cc1ab3619323c98978e7988333a9')
#         the script both the records' engine.m3_run_v1_7 and the asm outputs' line 1 name; its INPUTS (l.161-164) pin TRIAL_SET's four
#         files by full sha256 (pk03; MANIFEST_m3_run_v1_7.sha256 096e442b l.21-24)


def c_trial_chain(M3, fails, fires):
    """C-TRIAL, the chain (pk03): for each certified N, every record's engine.m3_run_v1_7 and its asm output's line-1 script
    sha256 equal M3_RUN's full sha256 (the loader does not compare them); the asm output has exactly one 'C-HASH ... -> PASS' line (the
    script's check of its 37 inputs, the four trial files among them); and the script, read here with its sha256 = M3_RUN's, pins each
    of TRIAL_SET's four files by the same full sha256 on exactly one INPUTS line, so the records' trial_set sha8s are prefixes of the
    pins this file holds. PLANT-TRIAL-ENGINE (a record copy with engine.m3_run_v1_7 changed) and PLANT-TRIAL-SCRIPT (a script copy with
    one INPUTS pin changed) must fail."""
    certN = [N for N in (4, 3) if M3[N].get('m3_cert')]
    if not certN:
        out('C-TRIAL chain: no certified M3 records (INFO)')
        return
    with open(os.path.join(CODEDIR, M3_RUN[0]), 'rb') as fh:
        sb = fh.read()
    asms, ok_h = {}, sha_bytes(sb) == M3_RUN[1]
    for N in certN:
        with open(os.path.join(CODEDIR, M3_CERT[N]['asm'][0]), 'rb') as fh:
            ab = fh.read()
        ok_h = ok_h and sha_bytes(ab) == M3_CERT[N]['asm'][1]
        asms[N] = ab.decode('utf-8')
    if not ok_h:
        out('C-TRIAL chain: C-HASH of %s or an asm output -> FAIL' % M3_RUN[0])
        fails.append('C-HASH TRIAL chain')
        return
    stext = sb.decode('utf-8')

    def chain_bad(recs, script):
        bad = []
        for N in certN:
            lines = asms[N].split('\n')
            if ('; script sha256 %s;' % M3_RUN[1]) not in lines[0]:
                bad.append('N=%d asm line 1' % N)
            ch = [ln for ln in lines if ln.startswith('C-HASH (')]    # the script's input check ('C-HASH-REF' lines are its references')
            if len(ch) != 1 or not ch[0].endswith('-> PASS'):
                bad.append('N=%d asm C-HASH line' % N)
            bad += ['N=%d %s engine' % (N, src) for src, _ in M3_FAMILIES
                    if (recs[N][src].get('engine') or {}).get('m3_run_v1_7') != M3_RUN[1]]
        for N in (4, 3):
            for k in ('ts', 'vacres'):
                name, sha = os.path.basename(TRIAL_SET[N][k][0]), TRIAL_SET[N][k][1]
                if script.count("'%s'): '%s'" % (name, sha)) != 1:
                    bad.append('script INPUTS %s' % name)
        return bad
    recs = {N: {src: M3[N][src] for src, _ in M3_FAMILIES} for N in certN}
    bad = chain_bad(recs, stext)
    N0, src0 = certN[0], M3_FAMILIES[0][0]
    e0 = dict(M3[N0][src0])
    e0['engine'] = dict(e0.get('engine') or {}, m3_run_v1_7=M3_RUN[1][:-1] + ('0' if M3_RUN[1][-1] != '0' else '1'))
    rp = {N: dict(recs[N]) for N in certN}                       # the records with one engine field changed (int keys: no ** here)
    rp[N0][src0] = e0
    pe = ('N=%d %s engine' % (N0, src0)) in chain_bad(rp, stext)
    n0, s0 = os.path.basename(TRIAL_SET[4]['ts'][0]), TRIAL_SET[4]['ts'][1]
    st_p = stext.replace("'%s'): '%s'" % (n0, s0), "'%s'): '%s'" % (n0, s0[:-1] + ('0' if s0[-1] != '0' else '1')), 1)
    ps = st_p != stext and ('script INPUTS %s' % n0) in chain_bad(recs, st_p)
    out('C-TRIAL chain (pk03): %s sha256 %s; for N = %s every record\'s engine.m3_run_v1_7 and the asm output\'s line-1 script '
        'sha256 equal it, one C-HASH ... -> PASS line in each asm output; the script\'s INPUTS pin the four TRIAL_SET files by the same full '
        'sha256 -> %s; PLANT-TRIAL-ENGINE %s; PLANT-TRIAL-SCRIPT %s' % (
            M3_RUN[0], M3_RUN[1][:8], ', '.join(str(N) for N in certN), 'PASS' if not bad else 'FAIL (%s)' % ', '.join(bad[:6]),
            'FIRES' if pe else 'DOES NOT FIRE', 'FIRES' if ps else 'DOES NOT FIRE'))
    if bad:
        fails.append('C-TRIAL chain')
    for nm, f in (('PLANT-TRIAL-ENGINE', pe), ('PLANT-TRIAL-SCRIPT', ps)):
        if not f:
            fires.append(nm)


def c_trial(M3, fails, fires):
    """C-TRIAL: every input on one trial set. C-HASH TRIAL: the four files of TRIAL_SET, full sha256 of the bytes read. Every
    certified M3 record (an N whose records come through load) must carry trial_set == {'ts': '<ts file name>:<its sha8>', 'vacres':
    '<vacres file name>:<its sha8>'} exactly, and this file's own trial vacuum (m-hat's m1..m3, inp['mser']) is read from the same pinned
    vacres file (returned for load). Mock records carry no trial set (INFO). PLANT-TRIAL: a copy of one record's trial_set with the vacres
    sha8 changed must fail. Returns {N: the vacres JSON}."""
    raws, ok_h = {}, True
    for N in (4, 3):
        for k in ('ts', 'vacres'):
            with open(os.path.join(CODEDIR, TRIAL_SET[N][k][0]), 'rb') as fh:
                raws[(N, k)] = fh.read()
            ok_h = ok_h and sha_bytes(raws[(N, k)]) == TRIAL_SET[N][k][1]
    out('C-HASH TRIAL (full sha256 of the bytes read here): %s -> %s' % (
        ', '.join(TRIAL_SET[N][k][0] for N in (4, 3) for k in ('ts', 'vacres')), 'PASS' if ok_h else 'FAIL'))
    if not ok_h:
        fails.append('C-HASH TRIAL')
        raise RuntimeError('C-TRIAL: a pinned trial file differs from its pin; nothing is read from it')
    want = {N: {k: '%s:%s' % (os.path.basename(TRIAL_SET[N][k][0]), TRIAL_SET[N][k][1][:8]) for k in ('ts', 'vacres')} for N in (4, 3)}
    certN = [N for N in (4, 3) if M3[N].get('m3_cert')]

    def trial_bad(m3):                                  # the record loop, run on the records and on the plant's copy
        return ['N=%d %s carries %r' % (N, src, m3[N][src].get('trial_set')) for N in certN for src, _ in M3_FAMILIES
                if m3[N][src].get('trial_set') != want[N]]
    bad = trial_bad(M3)
    N0, src0 = (certN[0] if certN else 4), M3_FAMILIES[0][0]
    fired = False
    if certN:                                           # PLANT-TRIAL: a copy of the M3 dict whose N0 src0 record's vacres sha8 is changed
        r0 = dict(M3[N0][src0])
        ts0 = dict(r0.get('trial_set') or {})
        v = ts0.get('vacres', want[N0]['vacres'])
        ts0['vacres'] = v[:-1] + ('0' if v[-1] != '0' else '1')
        r0['trial_set'] = ts0
        m3p = {N: dict(M3[N]) for N in (4, 3)}
        m3p[N0][src0] = r0
        fired = any(b.startswith('N=%d %s ' % (N0, src0)) for b in trial_bad(m3p))
    out('C-TRIAL: every certified S7 record (%s) names the pinned trial set, trial_set = %s; this file\'s m-hat reads the same '
        'vacres; mock records carry none (%s) -> %s; PLANT-TRIAL (the record loop on a copy whose N=%d %s record has its vacres sha8 '
        'changed) -> %s' % (
            ', '.join('N=%d: %d records' % (N, len(M3_FAMILIES)) for N in certN) or 'none certified',
            '; '.join('N=%d %s, %s' % (N, want[N]['ts'], want[N]['vacres']) for N in (4, 3)),
            ', '.join('N=%d' % N for N in (4, 3) if N not in certN) or 'none', 'PASS' if not bad else 'FAIL (%s)' % ', '.join(bad[:4]),
            N0, M3_FAMILIES[0][0], 'FIRES' if fired else 'DOES NOT FIRE'))
    if bad:
        fails.append('C-TRIAL')
    if not fired:
        fires.append('PLANT-TRIAL')
    return {N: json.loads(raws[(N, 'vacres')].decode('utf-8')) for N in (4, 3)}


def provide_m3(fails, fires):
    """the M3 provider (v2_3's item; M3 records only through pk03's bound loader m3_reader_v4_4.load(path, asm_out, 300, N)).
    C-HASH: the loader, every record and (certified) the asm output, full sha256 of the bytes read. The loader runs only after its own
    sha256 matches; certified records go through load (the asm output's exact VERDICT VALID and its RECORD line with the file's sha256),
    mock records (M3_MODE 'mock') through load_noncert. C-FMT M3: every record loads; it holds every entry the FLOAT files name (the
    port's key set); kbar_exact equals kbar exactly; every ball [LO_k, HI_k] converts to an mp.iv interval that contains both exact
    ends (m3_iv, m3_contains), with the test balls (negative, straddling, symmetric, zero ends) and PLANT-M3CONV (a converter
    that drops the sign must fail the negative ball). Returns {N: dict(M2=..., B5=..., CT=..., B4=..., EW=... (the records' JSON),
    balls={(source, key): ([coefficient intervals], err_b upper end)})} and sets TAGS['M3 entries'] (CERTIFIED only in certified mode
    with every check passing and a pin). M3_MODE 'mixed' reads the N that M3_CERT holds through load and the others' mocks through
    load_noncert (the tag stays MOCK). For each certified N, PLANT-M3-BIND (loads with the asm output's VERDICT VALID read as VALID-PRECERT)
    and PLANT-M3-SHA (its RECORD line's sha256 changed) must be refused by the loader."""
    if M3_MODE == 'certified' and any(N not in M3_CERT for N in (4, 3)):
        raise RuntimeError('M3 provider: certified mode without records for every N')
    cert = {N: M3_MODE == 'certified' or (M3_MODE == 'mixed' and N in M3_CERT) for N in (4, 3)}
    recs = {N: M3_CERT[N] if cert[N] else M3_MOCK[N] for N in (4, 3)}
    with open(os.path.join(CODEDIR, M3_LOADER[0]), 'rb') as fh:
        lsrc = fh.read()
    raws, asms, ok_h = {}, {}, sha_bytes(lsrc) == M3_LOADER[1]
    for N in (4, 3):
        for src, f in M3_FAMILIES:
            path, sha = recs[N]['files'][f]
            with open(os.path.join(CODEDIR, path), 'rb') as fh:
                raws[(N, f)] = fh.read()
            ok_h = ok_h and sha_bytes(raws[(N, f)]) == sha
        if recs[N]['asm'] is not None:
            with open(os.path.join(CODEDIR, recs[N]['asm'][0]), 'rb') as fh:
                asms[N] = fh.read()
            ok_h = ok_h and sha_bytes(asms[N]) == recs[N]['asm'][1]
    out('C-HASH M3 (%s mode: %s; full sha256 of the bytes read here): the loader %s, %d records%s -> %s' % (
        M3_MODE, ', '.join('N=%d %s' % (N, 'certified' if cert[N] else 'mock') for N in (4, 3)), M3_LOADER[0], len(raws),
        ' and the certified N\'s asm outputs' if asms else '', 'PASS' if ok_h else 'FAIL'))
    if not ok_h:
        fails.append('C-HASH M3')
        raise RuntimeError('M3 provider: a pinned file differs from its pin; nothing is read from it')
    ns = {}
    exec(compile(lsrc.decode('utf-8'), M3_LOADER[0], 'exec'), ns)
    res, bad, nconv = {}, [], 0
    for N in (4, 3):
        d, balls = {}, {}
        for src, f in M3_FAMILIES:
            path = os.path.join(CODEDIR, recs[N]['files'][f][0])
            try:
                if cert[N]:
                    rec = ns['load'](path, os.path.join(CODEDIR, recs[N]['asm'][0]), 300, N)
                else:
                    rec = ns['load_noncert'](path, 300, N)
            except ValueError as e:
                bad.append('N=%d %s refused: %s' % (N, f, e))
                continue
            d[src] = json.loads(raws[(N, f)].decode('utf-8'))
            for key in rec['balls']:
                LO, HI, eb = ns['entry_ball'](rec, key)
                ivs = [m3_iv(lo, hi) for lo, hi in zip(LO, HI)]
                nconv += len(ivs)
                if not all(m3_contains(I, lo, hi) for I, lo, hi in zip(ivs, LO, HI)):
                    bad.append('N=%d %s %s conversion' % (N, f, key))
                balls[(src, key)] = (ivs, pt((pt(eb.numerator) / pt(eb.denominator)).b))
        fl = dict(M2=jl('m2_N%d_J170.json.b' % N), B5=jl('b5_N%d_J170.json' % N), CT=jl('clT_N%d_J170.json' % N),
                  B4=jl('binding4_N%d_J170.json' % N), EW=jl('endw_N%d_J170.json' % N))
        for src, _ in M3_FAMILIES:
            want = ['I_N'] if src == 'B4' else list(fl[src]['items'])
            bad += ['N=%d %s %s missing' % (N, src, k) for k in want if (src, k) not in balls]
        m2 = d.get('M2', {})
        if 'kbar_exact' not in m2 or m2.get('kbar') is None or dec_frac(m2['kbar_exact']) != Fraction(m2['kbar']):
            bad.append('N=%d kbar_exact against kbar' % N)
        res[N] = dict(d, balls=balls, FLOAT_M3=fl, m3_cert=cert[N])
    tb = [i for i, (lo, hi) in enumerate(M3_CONV_TESTS) if not m3_contains(m3_iv(lo, hi), lo, hi)]
    out('C-FMT M3 (%s mode): every record through %s (%s); every FLOAT entry name present; kbar_exact = kbar exactly; %d ball ends '
        'converted to mp.iv and contained; the test balls (negative, straddling, symmetric 0 +- 1/4, zero ends) contained: %s -> %s' % (
            M3_MODE, os.path.basename(M3_LOADER[0]), ', '.join('N=%d %s' % (N, 'load' if cert[N] else 'load_noncert') for N in (4, 3)), nconv,
            'yes' if not tb else 'NO (%s)' % tb, 'PASS' if not (bad or tb) else 'FAIL (%s)' % ', '.join((bad + ['T44 %s' % tb])[:6])))
    if bad or tb:
        fails.append('C-FMT M3')
    lo, hi = M3_CONV_TESTS[0]
    pl = not m3_contains(m3_iv(min(abs(lo), abs(hi)), max(abs(lo), abs(hi))), lo, hi)
    out('PLANT-M3CONV (a converter that drops the sign, on the negative test ball): refused %s -> %s' % (pl, 'FIRES' if pl else 'DOES NOT FIRE'))
    if not pl:
        fires.append('PLANT-M3CONV')
    for N in (4, 3):                                    # T48 on the certified binding, in memory with the loader's own loads
        if not cert[N]:
            continue
        f = M3_FAMILIES[0][1]
        name, text, otext = os.path.basename(recs[N]['files'][f][0]), raws[(N, f)].decode('utf-8'), asms[N].decode('utf-8')
        sha = recs[N]['files'][f][1]
        res_p = []
        for lab, ot in (('PLANT-M3-BIND', '\n'.join(('VERDICT VALID-PRECERT' if ln == 'VERDICT VALID' else ln) for ln in otext.split('\n'))),
                        ('PLANT-M3-SHA', otext.replace(sha, ('0' if sha[0] != '0' else '1') + sha[1:]))):
            try:
                ns['loads'](text, ot, 300, N, name)
                refused = False
            except ValueError:
                refused = True
            refused = refused and ot != otext
            res_p.append('%s %s' % (lab, 'FIRES' if refused else 'DOES NOT FIRE'))
            if not refused:
                fires.append('%s N=%d' % (lab, N))
        try:
            ns['loads'](text, otext, 300, N, name)
            ctrl = 'accepted'
        except ValueError as e:
            ctrl = 'REFUSED (%s)' % e
            bad.append('N=%d loads control' % N)
            fails.append('C-FMT M3 loads control N=%d' % N)
        out('PLANT-M3-BIND, PLANT-M3-SHA (N=%d, %s through the loader\'s loads with its asm output %s; the unchanged pair %s): %s' % (
            N, name, os.path.basename(recs[N]['asm'][0]), ctrl, '; '.join(res_p)))
    if M3_MODE == 'certified' and not (bad or tb) and M3_TAG_PIN is not None:
        TAG_PINS['M3 entries'] = M3_TAG_PIN
        TAGS['M3 entries'] = 'CERTIFIED %s %s' % M3_TAG_PIN
    else:
        TAGS['M3 entries'] = '%s (%s records: %s)' % ('MOCK' if M3_MODE in ('mock', 'mixed') else 'FLOAT', M3_MODE, '; '.join(
            'N=%d %s' % (N, 'pk03 certified, %s' % os.path.basename(recs[N]['asm'][0]) if cert[N] else
                         'pk07 STUB copies of the FLOAT J = 170 JSONs') for N in (4, 3)))
    return res


# ------------------------------------------------------------------ the M2(b) provider (certified snapshot; v2_3's item, the Q2)
M2B_MODE = 'certified'    # 'mock': pk07's mock record (FLOAT vacscale keys) read by this file's KV port; 'certified': pk02's
                          # frozen M2B_KV_v1 through its sha-pinned reader, load(path, asm_out, expected_sha256), bound to m2b_asm_v1's output
M2B_MOCK = ('pk07/mocks/m2b_mock_v2.kv', '78f503464487d03734aabc745b9902d78da3055a91e83b380c5cdb7cd408204a')   # mk_m2b_mock_v2.awk
M2B_CERT = dict(record=('pk02/M2B_KV_v1.txt', '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d'),
                asm=('pk02/out/out_m2b_asm_v1.out', 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391'),
                reader=('pk02/m2b_reader_v1.py', 'a9f15db48e9fa51629448181d8a83679c1b93cd2b5696c8ed1e6b41d60df8b02'))
#                         v1_1 P-1: pk02's certified M2B_KV_v1 on the F-2-fixed pieces (m2b_cert_v1_4, majfix_v1_1), written by
#                         m2b_asm_v1 (6acd83d3 = the record's ASM_SHA256; the review 8d465b64 OK TO RUN, the approval); side manifest 797c7a59
M2B_TAG_PIN = ('pk02', '01ffc2aa')   # TAG_PINS['M2 vacuum'], set only when every M2(b) check passes and every plant fires
M2B_KEYS = ('NP', 'R1', 'D5', 'R0', 'TX', 'TX_LAMSTAR', 'TB', 'ANN', 'ANN_LAMSTAR', 'FAR', 'MHAT_UP', 'GB', 'Z2', 'RTR', 'AE', 'WT', 'DL',
            'WT_R1', 'DL_R1')           # per N, pk02's final layout (WT and DL the lists [nPM, D5w, R0w])
M2B_CONSTK = ('J1', 'J0', 'J_MIN', 'CXI', 'VQ', 'KAPPA', 'KAPPA_B', 'A_M', 'A_E', 'A_PP', 'RHO_PP_HEX', 'LAW')     # global
M2B_LISTS = dict(WT=3, DL=3, VQ=2)          # the list-valued keys and their lengths (' ; '-separated in the KV text)
M2B_LOWER = ('Z2', 'AE', 'KAPPA_B')         # SPEC_M2B_CERT_v1 sect. 3a: lower ends
M2B_EXACT = ('TX_LAMSTAR', 'ANN_LAMSTAR') + tuple(k for k in M2B_CONSTK if k != 'KAPPA_B')   # frozen choices and constants: exact
M2B_FMT = (('EPS_R_300', 'eps_r'), ('S_300', 's'), ('EPS_A_300', 'eps_a'), ('EPS_DS5_300', 'eps_ds5'), ('EPS_W_300', 'eps_w'),
           ('EPS_D_300', 'eps_d'))
M2B_CONST = (('LAW', 'v1'), ('J1', '150'), ('J0', '170'), ('J_MIN', '300'), ('CXI', '0.6594'))
M2B_TOL = Fraction(1, 10 ** 9)              # C-LAW300: the record's J = 300 values against this file's LAW, relative
M2B_CLAIM_G = '||K^{1/2} |g| || <= eps_r mhat ||psihat||'  # the C1: the |g| form S5-S7's weighted eps's rely on, the exact 41-byte
#                                                           substring of the reader's CLAIM (pk02, draft e2, read with ast; once)


def m2b_local_ok(rlines, alines, rname, rsha):
    """the certified M2(b) branch's local second check (the C1), independent of the reader's return shape.
    The KV record: its lines starting 'FORMAT' are exactly ['FORMAT = M2B_KV_v1'], those starting 'VERDICT' exactly ['VERDICT = VALID'],
    and exactly one line starts 'CLAIM': a 'CLAIM = ' line holding M2B_CLAIM_G exactly once. The asm output: its VERDICT lines exactly
    ['VERDICT VALID'] and exactly one 'RECORD <record name> <record sha256>' line. Returns (record ok, asm output ok)."""
    claims = [ln for ln in rlines if ln.startswith('CLAIM')]
    rec_ok = ([ln for ln in rlines if ln.startswith('FORMAT')] == ['FORMAT = M2B_KV_v1']
              and [ln for ln in rlines if ln.startswith('VERDICT')] == ['VERDICT = VALID']
              and len(claims) == 1 and claims[0].startswith('CLAIM = ') and claims[0].count(M2B_CLAIM_G) == 1)
    asm_ok = verdict_lines_ok(alines) and alines.count('RECORD %s %s' % (rname, rsha)) == 1
    return rec_ok, asm_ok


def m2b_trial_bad(rlines):
    """C-TRIAL M2B (v1_1 P-1; the C-TRIAL extended to the certified M2(b) record): the record's one PIN_TRIAL line names, for both N,
    TRIAL_SET's symmetrized vacres as 'path:full sha256' exactly once, and no other vacres file. Returns the failures."""
    pl = [ln for ln in rlines if ln.startswith('PIN_TRIAL')]
    if len(pl) != 1 or not pl[0].startswith('PIN_TRIAL = '):
        return ['%d PIN_TRIAL lines' % len(pl)]
    toks = pl[0][len('PIN_TRIAL = '):].split(' ; ')
    want = {N: '%s:%s' % TRIAL_SET[N]['vacres'] for N in (4, 3)}
    bad = ['N=%d: %s named %d times' % (N, w, toks.count(w)) for N, w in want.items() if toks.count(w) != 1]
    return bad + ['another vacres pin %s' % t for t in toks if 'vacres' in t and t not in want.values()]


def m2b_local_plants(rlines, alines, rname, rsha):
    """PLANT-M2B-LOCAL: m2b_local_ok on four altered copies of a pair, each sure to fail. Returns (label, fires)."""
    lp = []
    for lab, rl, al in (('record VERDICT = VALID-PRECERT', [('VERDICT = VALID-PRECERT' if ln == 'VERDICT = VALID' else ln)
                                                             for ln in rlines], alines),
                        ('record CLAIM without the |g| form', [ln.replace(M2B_CLAIM_G, '||K^{1/2} g|| <= eps_r') for ln in rlines],
                         alines),
                        ('a second CLAIM line', rlines + ['CLAIM = ' + M2B_CLAIM_G], alines),
                        ('asm output without its RECORD line', rlines, [ln for ln in alines if not ln.startswith('RECORD ')])):
        lp.append((lab, m2b_local_ok(rl, al, rname, rsha) != (True, True)))
    return lp


def m2b_end(key):
    """SPEC_M2B_CERT_v1 sect. 3a's end of a key: 'lower', 'exact' or 'upper'."""
    return 'lower' if key in M2B_LOWER else ('exact' if key in M2B_EXACT else 'upper')


def m2b_list(val, n):
    """a list-valued key's entries: the reader's list of strings, or the KV text's ' ; '-separated string; n entries, else ValueError."""
    xs = list(val) if isinstance(val, (list, tuple)) else val.split(' ; ')
    if len(xs) != n:
        raise ValueError('a list key with %d entries, not %d' % (len(xs), n))
    return xs


def vac_law_v1(inp, J, sc):
    """the certified snapshot's vacuum terms: pk02's LAW v1 (SPEC_M2B_CERT_v1 ffd842a2 sect. 3, ADD1, ADD2) at J in mp.iv, on the
    M2(b) record's keys (inp['M2B']: each key's exact decimal as an outward enclosure, at its safe end: upper, except Z2, AE and KAPPA_B,
    lower). For J >= 300 every term is nonincreasing in J (C-VACMONO), so its value at the piece's left end bounds it on the piece, the
    last piece included (t -> 0). Each result is returned as [0, its upper end], an enclosure of the true term (>= 0), so no use of it
    needs to be monotone. Hooks: vac_float's (vac_all on NP, R1, D5, R0, TX, TB, ANN, FAR, GB; D5; gB; eps_a; eps_ds5; eps_w on eps_w
    and eps_d) and SPEC_MA_LAYER_v1_2_ADD1 sect. 2's z2 (Z2 divided by it) and Rtr (Rtr times it). Z2 > 0 and 2 - Rtr - eps > 0 must be
    certain, else ArithmeticError (a failed verdict under a hook)."""
    if (pt(J) >= 300) is not True:                  # LAW v1 and C-VACMONO hold for J >= 300 only; a logic error, not a
        raise RuntimeError('LAW v1 at J = %r < 300' % (J,))      # failed verdict, so not an ArithmeticError
    K = inp['M2B']
    k = sc.get('vac_all', 1.0)
    nP, R1, D5, R0, tX, tB, ann, far, gB = (K[x] * k for x in ('NP', 'R1', 'D5', 'R0', 'TX', 'TB', 'ANN', 'FAR', 'GB'))
    D5 = D5 * sc.get('D5', 1.0)
    gB = gB * sc.get('gB', 1.0)
    Z2 = K['Z2'] / sc.get('z2', 1.0)
    Rtr = K['RTR'] * sc.get('Rtr', 1.0)
    if (Z2 > 0) is not True:
        raise ArithmeticError('LAW v1: Z2 is not certainly > 0')
    Ji = pt(J)
    sig, sig7 = pt(150) / Ji, pt(170) / Ji
    dec = iv.exp(-dec_iv('0.3') * K['AE'] * (Ji - 150) / 2)
    tails = (tX + ann) * dec + tB * iv.exp(-dec_iv('0.45') * K['KAPPA_B'] * (Ji - 150) / 2)
    near = nP * sig * sig + R1 * sig + (D5 + R0) * sig ** 5 + tails
    fJ = far * (Ji / 150) ** 2 * iv.exp(-dec_iv('0.5') * dec_iv('0.3025') * (Ji - 150))
    g = gB * (Ji / 150) * iv.exp(-dec_iv('0.95') * (1 - iv.cos(iv.pi * 40 / 180)) * (Ji - 150) / 2)
    rz = iv.sqrt(Z2)
    eps = (iv.sqrt(near * near + fJ) + g) / rz
    den = 2 - Rtr - eps
    if (den > 0) is not True:
        raise ArithmeticError('LAW v1: 2 - Rtr - eps is not certainly > 0')
    cw = dec_iv('0.6594')

    def wres(c_, wg):
        return (iv.sqrt((c_ * Ji * near) ** 2 + (wg * Ji) ** 2 * fJ) + wg * Ji * g) / rz

    def ew(t4, c_, wg):
        nPM, R1w, D5w, R0w = t4
        nw = nPM * sig7 * sig7 + R1w * sig7 + (D5w + R0w) * sig7 ** 5 + c_ * Ji * tails
        return (iv.sqrt(nw * nw + (wg * Ji) ** 2 * fJ) + wg * Ji * g) / rz
    kw = sc.get('eps_w', 1.0)
    vals = dict(eps_r=eps, s=eps / den, eps_a=wres(cw, 2) * sc.get('eps_a', 1.0), eps_ds5=wres(cw / 2, 1) * sc.get('eps_ds5', 1.0),
                eps_w=ew(K['WT'], cw, 2) * kw, eps_d=ew(K['DL'], cw / 2, 1) * kw)
    return dict({name: iv.mpf([0, v.b]) for name, v in vals.items()}, tag=TAGS['M2 vacuum'])


def vac_terms(inp, J, sc):
    """the piece's vacuum terms: LAW v1 on the M2(b) record when the inputs carry one (the snapshot's production inputs), else vac_float
    (the FLOAT inputs of the reproductions and of C-VERT, float_m3)."""
    return vac_law_v1(inp, J, sc) if inp.get('M2B') is not None else vac_float(inp, J, sc)


def m2b_monotone(K):
    """C-VACMONO, the lemma that lets vac_law_v1 take the piece's left end: for J >= 300 each LAW v1 term is nonincreasing in J. sig, sig7
    fall; J near = NP 150^2/J + 150 R1 + (D5 + R0) 150^5/J^4 + J tails falls when J e^{-0.15 AE (J - 150)} and J e^{-0.225 KAPPA_B (J -
    150)} do, i.e. when 45 AE > 1 and 67.5 KAPPA_B > 1 (d/dJ log <= 1/300 - rate); fJ and J^2 fJ fall when 4/300 < 0.15125; g and J g
    fall when 2/300 < 0.95 (1 - cos 40 deg)/2; eps, s (2 - Rtr - eps > 0 at J = 300, the largest eps), wres and ew are nondecreasing in
    these. The law's own rate for (TX + ANN) dec needs the frozen lambda* >= 0.3 (SPEC sect. 3), checked on TX_LAMSTAR and ANN_LAMSTAR.
    Exact comparisons on the keys' decimals (AE, KAPPA_B: lower ends) and one certain interval comparison. Returns the failures."""
    bad = []
    for key in ('TX_LAMSTAR', 'ANN_LAMSTAR'):
        if not Fraction(K[key + '_dec']) >= Fraction(3, 10):
            bad.append('%s >= 0.3' % key)
    if not Fraction(K['AE_dec']) * 45 > 1:
        bad.append('45 AE > 1')
    if not Fraction(K['KAPPA_B_dec']) * Fraction(135, 2) > 1:
        bad.append('67.5 KAPPA_B > 1')
    if not Fraction(4, 300) < Fraction('0.15125'):
        bad.append('4/300 < 0.5 x 0.3025')
    if ((dec_iv('0.95') * (1 - iv.cos(iv.pi * 40 / 180)) / 2).a > pt(2) / 300) is not True:
        bad.append('2/300 < 0.95 (1 - cos 40 deg)/2')
    return bad


def m2b_keys(d, const, N):
    """one N's LAW v1 keys from the record's {key: (value, end)} (d: the N's keys, const: the global ones): each key of M2B_KEYS present
    with sect. 3a's end, every decimal (and every list entry) finite and >= 0; each as an mp.iv enclosure of its exact decimal; WT and DL
    as the quadruples (nPM, R1w, D5w, R0w) with R1w from WT_R1, DL_R1; KAPPA_B (global, a lower end); the decimals of AE, KAPPA_B and
    the lambda* for C-VACMONO. Raises ValueError (or KeyError) on anything else."""
    K = {}
    for key in M2B_KEYS:
        if key not in d:
            raise ValueError('N=%d: %s missing' % (N, key))
        val, end = d[key]
        if end != m2b_end(key):
            raise ValueError('N=%d: %s carries the %r end' % (N, key, end))
        vals = m2b_list(val, M2B_LISTS[key]) if key in M2B_LISTS else [val]
        if any(dec_frac(v) < 0 for v in vals):
            raise ValueError('N=%d: %s < 0' % (N, key))
        K[key] = [dec_iv(v) for v in vals] if key in M2B_LISTS else dec_iv(val)
    kb, kend = const['KAPPA_B']
    if kend != 'lower' or dec_frac(kb) < 0:
        raise ValueError('KAPPA_B carries the %r end or is < 0' % kend)
    K['KAPPA_B'] = dec_iv(kb)
    K['WT'] = (K['WT'][0], K['WT_R1'], K['WT'][1], K['WT'][2])
    K['DL'] = (K['DL'][0], K['DL_R1'], K['DL'][1], K['DL'][2])
    K['AE_dec'], K['KAPPA_B_dec'] = d['AE'][0], kb
    K['TX_LAMSTAR_dec'], K['ANN_LAMSTAR_dec'] = d['TX_LAMSTAR'][0], d['ANN_LAMSTAR'][0]
    return K


def m2b_law300(K, fmt):
    """C-LAW300 on one N: LAW v1 at J = 300 by vac_law_v1 on the keys K against the record's *_300 values fmt ({name: decimal}): each
    upper end within M2B_TOL relative of the record's value (exact Fraction comparisons of the raw interval ends). Returns the failures."""
    V = vac_law_v1(dict(M2B=K), 300.0, {})
    bad = []
    for key, name in M2B_FMT:
        rec = dec_frac(fmt[key])
        mine = frac_end(V[name]._mpi_[1])
        if not abs(mine - rec) <= M2B_TOL * abs(rec):
            bad.append('%s %s against %s' % (key, nf(V[name].b), fmt[key]))
    return bad


def m2b_info(KS):
    """INFO (prints only): LAW v1's upper ends at J = 300 against the FLOAT vac_float, per N."""
    for N in (4, 3):
        Vl = vac_law_v1(dict(M2B=KS[N]), 300.0, {})
        Vf = vac_float(dict(N=N, P=PARAMS[N]), 300.0, {})
        out('INFO M2B N=%d at J = 300, LAW v1 upper end / vac_float (FLOAT): %s' % (N, ', '.join(
            '%s %.6g' % (name, fnum(pt(Vl[name].b)) / fnum(Vf[name])) for _, name in M2B_FMT)))


def provide_m2b(fails, fires):
    """the M2(b) provider (the Q2: the VERTICAL mode reads M2(b)), on pk02's final layout: rec = {'const': {key: (value, end)},
    'N4': {...}, 'N3': {...}}, keys without the N prefix, WT and DL lists [nPM, D5w, R0w], KAPPA_B global. Certified mode: pk02's
    reader (M2B_CERT), executed only after its own sha256 matches, load(record, m2b_asm_v1's output, expected_sha256): the asm binding
    (its exact VERDICT VALID and one RECORD line with the record's sha256), FORMAT, CLAIM, LAW, the key allow-list, C-MONO and C-FMT are
    the reader's, and MOCK, PRECERT and STUB records are refused there. Mock mode: pk07's mock record (M2B_MOCK) read by this file's
    S4U_KV_v1 port, FORMAT M2B_KV_v1 MOCK, RECORD and END checked here and sect. 3a's ends assigned by key (the mock carries none).
    C-HASH: the record (and the asm output and reader), full sha256 of the bytes read. C-FMT M2B, in both modes: LAW v1 and the constants
    J1, J0, J_MIN, CXI exactly, A_M and A_E the exact squares of binary64 0.55 and 0.6 (ADD1 sect. 1), every global key and every key of
    M2B_KEYS per N with sect. 3a's end, finite decimals >= 0, the six *_300 values. C-VACMONO (m2b_monotone, with the lambda* >= 0.3) with
    PLANT-VACMONO (AE = 0.02 must fail it). C-LAW300 (m2b_law300: this file's mp.iv LAW against the record's values, an independent
    evaluation) with PLANT-M2B-SWAP (N4's NP and D5 exchanged must fail it). INFO: LAW v1 against vac_float at J = 300. Certified mode
    also runs C-M2B-LOCAL (m2b_local_ok, PLANT-M2B-LOCAL), PLANT-M2B-MOCK and C-TRIAL M2B (m2b_trial_bad, PLANT-M2B-TRIAL). Sets
    TAGS['M2 vacuum'] (CERTIFIED only in certified mode with every check passing and a pin). Returns {N: K} for load."""
    if M2B_MODE == 'certified':
        if M2B_CERT is None:
            raise RuntimeError('M2(b) provider: certified mode without M2B_CERT')
        rpath, rsha = M2B_CERT['record']
    else:
        rpath, rsha = M2B_MOCK
    with open(os.path.join(CODEDIR, rpath), 'rb') as fh:
        raw = fh.read()
    ok_h = sha_bytes(raw) == rsha
    if M2B_MODE == 'certified':
        with open(os.path.join(CODEDIR, M2B_CERT['reader'][0]), 'rb') as fh:
            rsrc = fh.read()
        with open(os.path.join(CODEDIR, M2B_CERT['asm'][0]), 'rb') as fh:
            ok_h = ok_h and sha_bytes(rsrc) == M2B_CERT['reader'][1] and sha_bytes(fh.read()) == M2B_CERT['asm'][1]
    out('C-HASH M2B (%s mode; full sha256 of the bytes read here): the record %s%s -> %s' % (
        M2B_MODE, rpath, ', its asm output %s and its reader %s' % (M2B_CERT['asm'][0], M2B_CERT['reader'][0])
        if M2B_MODE == 'certified' else '', 'PASS' if ok_h else 'FAIL'))
    if not ok_h:
        fails.append('C-HASH M2B')
        raise RuntimeError('M2(b) provider: a pinned file differs from its pin; nothing is read from it')
    bad, trial_ok = [], False
    if M2B_MODE == 'certified':                 # pk02's reader: the asm binding, FORMAT, CLAIM, LAW, the allow-list, C-MONO, C-FMT
        ns = {'__file__': os.path.join(CODEDIR, M2B_CERT['reader'][0]), '__name__': 'm2b_reader'}   # pk02's reader also
        exec(compile(rsrc.decode('utf-8'), M2B_CERT['reader'][0], 'exec'), ns)                  # takes reader_sha256 for its C-PINS
        try:
            got = ns['load'](os.path.join(CODEDIR, rpath), os.path.join(CODEDIR, M2B_CERT['asm'][0]), expected_sha256=rsha,
                             reader_sha256=M2B_CERT['reader'][1])
        except ValueError as e:
            raise RuntimeError('M2(b) provider: the reader refuses the record: %s' % e)
        with open(os.path.join(CODEDIR, M2B_CERT['asm'][0]), 'rb') as fh:
            araw = fh.read()
        rlines, alines = raw.decode('utf-8').split('\n'), araw.decode('utf-8').split('\n')     # a local second line
        rname = os.path.basename(rpath)
        rec_ok, asm_ok = m2b_local_ok(rlines, alines, rname, rsha)
        lp = m2b_local_plants(rlines, alines, rname, rsha)              # the local check's plants, on copies
        out('C-M2B-LOCAL (the C1): the record\'s FORMAT = M2B_KV_v1 and VERDICT = VALID lines, its one CLAIM line holding the |g| '
            'form once; the asm output\'s exact VERDICT VALID and its RECORD line for %s -> %s; PLANT-M2B-LOCAL: %s' % (
                rname, 'PASS' if (rec_ok and asm_ok) else 'FAIL', '; '.join('%s %s' % (lab, 'fires' if f else 'DOES NOT FIRE')
                                                                          for lab, f in lp)))
        if not all(f for _, f in lp):
            fires.append('PLANT-M2B-LOCAL')
        if not (rec_ok and asm_ok):
            bad.append('local check: %s%s' % ('' if rec_ok else 'the record\'s FORMAT line is not exactly FORMAT = M2B_KV_v1, its VERDICT '
                                                                'key not exactly VERDICT = VALID, or its CLAIM line lacks the |g| form '
                                                                'M2B_CLAIM_G; ',
                                              '' if asm_ok else 'the asm output\'s VERDICT lines are not exactly [\'VERDICT VALID\'] or it '
                                                                'has no single RECORD line with the record\'s name and sha256'))
        tb = m2b_trial_bad(rlines)
        v4 = '%s:%s' % TRIAL_SET[4]['vacres']
        w4 = '%s:%s%s' % (TRIAL_SET[4]['vacres'][0], '0' if TRIAL_SET[4]['vacres'][1][0] != '0' else '1', TRIAL_SET[4]['vacres'][1][1:])
        tp = any(b.startswith('N=4') for b in m2b_trial_bad([ln.replace(v4, w4) if ln.startswith('PIN_TRIAL') else ln for ln in rlines]))
        trial_ok = not tb and tp
        out('C-TRIAL M2B (the C-TRIAL, v1_1 P-1): the record\'s PIN_TRIAL names TRIAL_SET\'s vacres %s:%s and %s:%s once each and no '
            'other vacres -> %s; PLANT-M2B-TRIAL (N4\'s vacres sha256 changed in a copy) -> %s' % (
                os.path.basename(TRIAL_SET[4]['vacres'][0]), TRIAL_SET[4]['vacres'][1][:8], os.path.basename(TRIAL_SET[3]['vacres'][0]),
                TRIAL_SET[3]['vacres'][1][:8], 'PASS' if not tb else 'FAIL (%s)' % ', '.join(tb), 'FIRES' if tp else 'DOES NOT FIRE'))
        if tb:
            fails.append('C-TRIAL M2B')
        if not tp:
            fires.append('PLANT-M2B-TRIAL')
        recs = {N: dict(got['N%d' % N]) for N in (4, 3)}
        const = dict(got['const'])
        with open(os.path.join(CODEDIR, M2B_MOCK[0]), 'rb') as fh:            # the reader must refuse the mock record
            mraw = fh.read()
        if sha_bytes(mraw) != M2B_MOCK[1]:
            raise RuntimeError('M2(b) provider: the mock record for PLANT-M2B-MOCK differs from its pin')
        try:
            ns['loads'](mraw.decode('utf-8'), os.path.basename(M2B_MOCK[0]), araw.decode('utf-8'))    # loads has no reader_sha256 (pk02)
            pm = False
        except ValueError:
            pm = True
        out('PLANT-M2B-MOCK (the reader\'s loads on pk07\'s mock record with the certified asm output) -> %s' % (
            'FIRES' if pm else 'DOES NOT FIRE'))
        if not pm:
            fires.append('PLANT-M2B-MOCK')
    else:                                       # the mock: this file's KV port, sect. 3a's ends assigned by key
        rec = s4u_read_port(raw.decode('utf-8'))
        recs = {N: {k: (rec[('N%d_' % N) + k], m2b_end(k)) for k in M2B_KEYS + tuple(f for f, _ in M2B_FMT) if ('N%d_' % N) + k in rec}
                for N in (4, 3)}
        const = {k: (rec[k], m2b_end(k)) for k in M2B_CONSTK if k in rec}
        bad += ['%s = %r' % (k, rec.get(k)) for k, v in (('FORMAT', 'M2B_KV_v1 MOCK'), ('RECORD', 'M2B_KV_v1'), ('END', 'M2B_KV_v1'))
                if rec.get(k) != v] + (['marked PRECERT or STUB'] if marked_precert(rec) else [])
        mlines, mname = raw.decode('utf-8').split('\n'), os.path.basename(rpath)    # the local check run here before its certified use:
        syn_a = ['VERDICT VALID', 'RECORD %s %s' % (mname, rsha)]                     # a two-line asm text, and a certified-form copy
        syn_r = ['FORMAT = M2B_KV_v1', 'VERDICT = VALID', 'CLAIM = ' + M2B_CLAIM_G] + [
            ln for ln in mlines if not ln.startswith(('FORMAT', 'VERDICT', 'CLAIM'))]
        m_ref = m2b_local_ok(mlines, syn_a, mname, rsha)[0] is False
        s_ok = m2b_local_ok(syn_r, syn_a, mname, rsha) == (True, True)
        lp = m2b_local_plants(syn_r, syn_a, mname, rsha)
        out('C-M2B-LOCAL (mock mode: the certified branch\'s local check and PLANT-M2B-LOCAL on text built here): the mock record (FORMAT '
            '... MOCK, a CLAIM without the |g| form) refused: %s; a copy with FORMAT = M2B_KV_v1, VERDICT = VALID and CLAIM = M2B_CLAIM_G, '
            'with the asm text VERDICT VALID and RECORD %s <sha256>, passes: %s -> %s; PLANT-M2B-LOCAL: %s' % (
                m_ref, mname, s_ok, 'PASS' if (m_ref and s_ok) else 'FAIL',
                '; '.join('%s %s' % (lab, 'fires' if f else 'DOES NOT FIRE') for lab, f in lp)))
        if not (m_ref and s_ok):
            fails.append('C-M2B-LOCAL (mock self-test)')
        if not all(f for _, f in lp):
            fires.append('PLANT-M2B-LOCAL')
    bad += ['%s = %r' % (k, const.get(k, (None,))[0]) for k, v in M2B_CONST if const.get(k, (None,))[0] != v]
    bad += ['%s missing' % k for k in M2B_CONSTK if k not in const]
    for k, v in (('A_M', Fraction(0.55) ** 2), ('A_E', Fraction(0.6) ** 2)):     # ADD1 sect. 1: the exact squares of the binary64 values
        if k in const and (re.fullmatch(r'[0-9]+/[0-9]+', const[k][0]) is None or Fraction(const[k][0]) != v):
            bad.append('%s is not the exact square of its binary64 value' % k)
    KS, fmts = {}, {}
    for N in (4, 3):
        try:
            KS[N] = m2b_keys(recs[N], const, N)
            fmts[N] = {f: recs[N][f][0] for f, _ in M2B_FMT}
            for f, _ in M2B_FMT:
                if dec_frac(fmts[N][f]) < 0:
                    bad.append('N=%d %s < 0' % (N, f))
        except (KeyError, ValueError) as e:
            bad.append('N=%d keys: %r' % (N, e))
    out('C-FMT M2B (%s mode): %sLAW v1, J1 150, J0 170, J_MIN 300, CXI 0.6594, A_M and A_E the exact binary64 squares; the %d keys per N '
        '(WT, DL lists of 3) and the 6 J = 300 values, finite decimals >= 0; the %d global keys (KAPPA_B a lower end); sect. 3a\'s ends'
        '%s -> %s' % (M2B_MODE, 'FORMAT, RECORD, END; ' if M2B_MODE == 'mock' else '', len(M2B_KEYS), len(M2B_CONSTK),
                      ' (assigned by key: the mock carries none)' if M2B_MODE == 'mock' else ' (the reader\'s)',
                      'PASS' if not bad else 'FAIL (%s)' % ', '.join(bad[:6])))
    if bad:
        fails.append('C-FMT M2B')
        raise RuntimeError('M2(b) provider: C-FMT M2B failed; nothing is used')
    mono = {N: m2b_monotone(KS[N]) for N in (4, 3)}
    pv = m2b_monotone(dict(KS[4], AE_dec='0.02'))
    out('C-VACMONO (LAW v1 terms nonincreasing in J for J >= 300, so the piece\'s left end bounds the piece): N=4 %s, N=3 %s -> %s; '
        'PLANT-VACMONO (AE = 0.02) -> %s' % (
            'yes' if not mono[4] else 'NO (%s)' % ', '.join(mono[4]), 'yes' if not mono[3] else 'NO (%s)' % ', '.join(mono[3]),
            'PASS' if not (mono[4] or mono[3]) else 'FAIL', 'FIRES' if pv else 'DOES NOT FIRE'))
    if mono[4] or mono[3]:
        fails.append('C-VACMONO')
    if not pv:
        fires.append('PLANT-VACMONO')
    law = {N: m2b_law300(KS[N], fmts[N]) for N in (4, 3)}
    sw = m2b_law300(dict(KS[4], NP=KS[4]['D5'], D5=KS[4]['NP']), fmts[4])
    out('C-LAW300 (this file\'s mp.iv LAW v1 at J = 300 against the record\'s six values per N, each within %s relative): N=4 %s, N=3 %s -> '
        '%s; PLANT-M2B-SWAP (N4\'s NP and D5 exchanged) -> %s' % (
            nf(M2B_TOL), 'agree' if not law[4] else 'NO (%s)' % ', '.join(law[4][:3]), 'agree' if not law[3] else 'NO (%s)' % ', '.join(law[3][:3]),
            'PASS' if not (law[4] or law[3]) else 'FAIL', 'FIRES' if sw else 'DOES NOT FIRE'))
    if law[4] or law[3]:
        fails.append('C-LAW300')
    if not sw:
        fires.append('PLANT-M2B-SWAP')
    m2b_info(KS)
    if M2B_MODE == 'certified' and M2B_TAG_PIN is not None and not (mono[4] or mono[3] or law[4] or law[3]) and pv and sw and trial_ok:
        TAG_PINS['M2 vacuum'] = M2B_TAG_PIN
        TAGS['M2 vacuum'] = 'CERTIFIED %s %s' % M2B_TAG_PIN
    else:
        TAGS['M2 vacuum'] = '%s (%s M2B_KV_v1, %s)' % ('MOCK' if M2B_MODE == 'mock' else 'FLOAT', M2B_MODE,
                                                      'pk07 mock: FLOAT vacscale keys' if M2B_MODE == 'mock' else 'no pin')
    return KS


def u_minus_float(inp, Jlo, Jhi):
    """F2 INFO and KR4: an enclosure, over the piece, of the certified U(t) minus the FLOAT U(t) = lead_f (1 + c1_f t + c2_f t^2 + c3_f t^3)
    + rem(170) of PARAMS (T2's baseline, SPEC sect. 3), as one polynomial in t with the coefficient differences (the naive enclosure
    over the piece, without the dependency loss of two separate evaluations)."""
    cu = [pt(x) for x in inp['U5']]
    fu = [pt(x) for x in inp['P']['trt2']]
    cs = [cu[0] - fu[0]] + [cu[0] * cu[k] - fu[0] * fu[k] for k in (1, 2, 3)]
    return Ctx(inp, Jlo, Jhi, {}).poly(cs, 'cnaive') + (cu[4] - fu[4])


def s4_kr34(INP, fails):
    """F2, D-2, v2_1: with S4-U and S4-TRB certified, KR3 (the record's N*_QUAD_TW_PART <= U_t/2 = 3.9e-4) and KR4 (joint form: certified
    U - float U <= +7.8e-4, T2's target, on every piece, float U = PARAMS trt2 with rem(170); and certified TRB <= 1.02 x PARAMS TRB,
    T2's target, exact decimals) are gates. A failure stops the port, naming the part (SPEC sect. 3 l.204-206, sect. 5 l.291), and
    enters the run's verdict. Prints F2's INFO (the per-piece extremes, beside the record's own N*_U_MINUS_FLOAT) and both KILL lines;
    returns (kr3, kr4). Called by both items."""
    STAGE[0] = 'KR3, KR4: S4-U and S4-TRB against their targets'
    ucert, tcert = tag_certified('S4 U', TAGS['S4 U']), tag_certified('S4 TRB', TAGS['S4 TRB'])
    ext = {}
    for N in (4, 3):
        hi_, lo_ = None, None
        for (Jlo, Jhi) in pieces():
            d = u_minus_float(INP[N], Jlo, Jhi)
            if hi_ is None or (d.b > hi_[0]) is True:
                hi_ = (pt(d.b), Jlo, Jhi)
            if lo_ is None or (d.a < lo_[0]) is True:
                lo_ = (pt(d.a), Jlo, Jhi)
        ext[N] = hi_
        out('INFO S4-U N=%d (F2): certified U(t) - float U(t) (float U = lead(1 + c1 t + c2 t^2 + c3 t^3) + rem(170), T2\'s baseline) over '
            'the %d pieces: at most %s (on [%s]), at least %s (on [%s]); beside it the record\'s own key N%d_U_MINUS_FLOAT = %s (its '
            'constant U minus S4\'s float U at J = 300, rem(170) not in it)' % (
                N, len(pieces()), nf(hi_[0], 8), piece_str(hi_[1], hi_[2]), nf(lo_[0], 8), piece_str(lo_[1], lo_[2]), N, INP[N]['umf']))
    kr3 = ucert and all(dec_frac(INP[N]['quad']) <= dec_frac(TGT_DEC['U']) / 2 for N in (4, 3))
    out('KILL KR3 (v1_2 form, pk08\'s quadrature error <= U_t/2 = %s; a gate): N=4 %s, N=3 %s (%s N*_QUAD_TW_PART, exact decimals; '
        'S4-U tag certified: %s) -> %s' % (TGT_DEC['QUAD'], INP[4]['quad'], INP[3]['quad'], S4U['record'], ucert,
                                           'PASS' if kr3 else 'KILL: S4 U (part pk08)'))
    kr4u = ucert and all((ext[N][0] <= dec_iv(TGT_DEC['U']).a) is True for N in (4, 3))
    kr4t = tcert and all(dec_frac(INP[N]['trb']) <= dec_frac(TGT_DEC['TRB']) * dec_frac(INP[N]['P']['TRB']) for N in (4, 3))
    kr4 = kr4u and kr4t
    out('KILL KR4 (joint form, a gate: a certified input looser than its T2 target stops the port): S4 U (part pk08): certified U - '
        'float U <= %s on every piece: N=4 at most %s, N=3 at most %s -> %s; S4 TRB (part pk08, v2_1): certified TRB <= %s x the FLOAT '
        'TRB, exact decimals: N=4 %s against %s x %s, N=3 %s against %s x %s (S4-TRB tag certified: %s) -> %s; M3 entries, M2 vacuum: '
        'FLOAT, not applicable -> %s' % (
            TGT_DEC['U'], nf(ext[4][0], 8), nf(ext[3][0], 8), 'PASS' if kr4u else 'KILL: S4 U looser than its target (part pk08)',
            TGT_DEC['TRB'], INP[4]['trb'], TGT_DEC['TRB'], INP[4]['P']['TRB'], INP[3]['trb'], TGT_DEC['TRB'], INP[3]['P']['TRB'], tcert,
            'PASS' if kr4t else 'KILL: S4 TRB looser than its target (part pk08)', 'PASS' if kr4 else 'KILL'))
    if not kr3:
        fails.append('KR3 (S4 U, part pk08)')
    if not kr4u:
        fails.append('KR4 (S4 U, part pk08)')
    if not kr4t:
        fails.append('KR4 (S4 TRB, part pk08)')
    return kr3, kr4


# ------------------------------------------------------------------ v2_2 (3): the per-piece export for S8
def dec_dir(x, up, sig=12):
    """a decimal string of sig significant digits that bounds the interval x from above (up) or from below (not up), certified by an
    exact interval comparison of its enclosure (dec_iv) with that end of x; it steps one unit in the last place until the comparison
    holds. float() only seeds the search."""
    v = pt(x).b if up else pt(x).a
    mant, ex = ('%.*e' % (sig - 1, float(v))).split('e')
    M, E = int(mant.replace('.', '')), int(ex) - (sig - 1)
    for _ in range(8):
        digits = str(abs(M))
        txt = ('-' if M < 0 else '') + digits[0] + ('.' + digits[1:] if len(digits) > 1 else '') + 'e%d' % (E + len(digits) - 1)
        d = dec_iv(txt)
        if ((d >= v) is True) if up else ((d <= v) is True):
            return txt
        M += 1 if up else -1
    raise ArithmeticError('no directed decimal found for %s' % str(v))


def export_row(Jlo, Jhi, N, E):
    """one piece's export values (strings) in EXPORT_FIELDS order, pk11's list for S8, in P2's units; *_lo are lower ends rounded
    down and *_hi upper ends rounded up (dec_dir):
    - jlo, jhi: the grid's float J ends (repr; 'inf' for the last piece's open end);
    - c5_lo: S5's bound, the flip m = 1 bulk covariance times J^2;
    - vSv_p_lo, vSv_m_hi: <v+, S v+> and <v-, S v-> (quantities' vSv_p, vSv_m); rp_lo, rho_hi, rho1_hi: R+, rho, rho1;
    - vp2_lo: |v+|^2 >= (sqrt(even) - Dlt)_+^2, from S5's Bessel term even = a_x^2 + a_y^2 on the trial vacuum (PK10_NOTES 19.3.3
      (iii)) and |v+ - v+^tr| <= |v - v^tr| <= Dlt (19.3.3 (vi); the flip projection does not increase norms); vp2_hi = |v+|^2 <= vp^2
      and vm2_hi = |v-|^2 <= vm^2 (quantities' vp, vm);
    - Bp_hi, Bm_hi: ||B+||, ||B-|| (quantities' nBp, nBm); cx_lo, r2_hi, ro_hi: the S7 mode inputs (mode); Rw_hi: R_w;
    - c_lo, c_hi: the bulk mean c = <u, T_xi+ u> / lam0 = kbar + <u, T_w~ u> / lam0, inside kbar -+ E_w with E_w as in t1; c_lo is kept
      >= 0 since xi+ >= 0.
    Then, per claimed pair, EXPORT_PAIR_FIELDS: kind, d, Jensen checked to m, the first mode success k (Lemma S7-mono covers
    m >= k + 1), and whether the claim holds."""
    Q, Mq, S5, cv, inp = E['Q'], E['Mq'], E['S5'], E['cv'], E['cx'].inp
    ev = S5['even'].a
    vpl = (iv.sqrt(pt(ev)) - pt(S5['Dlt'].b)).a if (ev > 0) is True else pt(0)
    vpl = pt(0) if (vpl < 0) is True else pt(vpl)
    kb = pt(inp['M2']['kbar'])
    cl = (kb - Q['Ew']).a
    cl = pt(0) if (cl < 0) is True else pt(cl)
    vals = [repr(Jlo), 'inf' if Jhi is None else repr(Jhi), dec_dir(S5['c5'], False), dec_dir(Q['vSv_p'], False),
            dec_dir(Q['vSv_m'], True), dec_dir(Q['Rp'], False), dec_dir(Q['rho'], True), dec_dir(Q['rho1'], True),
            dec_dir(vpl * vpl, False), dec_dir(Q['vp'] * Q['vp'], True), dec_dir(Q['vm'] * Q['vm'], True), dec_dir(Q['nBp'], True),
            dec_dir(Q['nBm'], True), dec_dir(Mq['cx'], False), dec_dir(Mq['r2'], True), dec_dir(Mq['ro'], True), dec_dir(Q['Rw'], True),
            dec_dir(cl, False), dec_dir(kb + Q['Ew'], True)]
    if len(vals) != len(EXPORT_FIELDS.split()):
        raise AssertionError('the export row does not match EXPORT_FIELDS')
    pairs = ['%s %d %d %d %s' % (p[0], p[1], cv[p][0], cv[p][1], 'yes' if claim_holds(cv, p) else 'no') for p in CLAIM[N]]
    return ' '.join(vals) + ' | ' + ' ; '.join(pairs)


def export_text(why):
    """the EXPORT_KT_S67_v1 text of this sweep (format S4U_KV_v1; kt_s67_export_reader_v1 states it). RUN_VERDICT is the run's validity
    so far (every control and plant of the sweep), EXPORT_STATUS the verdict word of the tags (CERTIFIED only when every input is
    certified and the run is valid), and each input's tag is written with its status."""
    key = lambda k: 'TAG_' + re.sub(r'[^A-Z0-9]+', '_', k.upper())
    lines = ['# EXPORT_KT_S67_v1: the per-piece S5, S6 and S7 bounds of %s (%s) for S8; format S4U_KV_v1 ("KEY = value", lines '
             'starting with # are comments, blank lines carry nothing); the reader is %s.' % (LABEL, MODE, EXPORT_READER[0]),
             '# Piece lines: N<N>_P<index> = FIELDS values | the claimed pairs, " ; "-separated, each the PAIR_FIELDS values. *_lo are lower',
             '# bounds rounded down, *_hi upper bounds rounded up (certified by exact interval comparisons); jlo, jhi are the grid floats.',
             'FORMAT = S4U_KV_v1', 'RECORD = EXPORT_KT_S67_v1', 'PRODUCER = pk07',
             'CODE = pk21/p2/s4c/%s.py:%s' % (LABEL, sha_file(os.path.abspath(__file__))[:8]), 'RUN = %s' % MODE,
             'RUN_VERDICT = %s' % ('VALID' if not why else 'INVALID'), 'EXPORT_STATUS = %s' % verdict_word(TAGS, not why),
             'FIELDS = %s' % EXPORT_FIELDS, 'PAIR_FIELDS = %s' % EXPORT_PAIR_FIELDS]
    for k, v in TAGS.items():
        lines += ['%s = %s' % (key(k), v), '%s_STATUS = %s' % (key(k), 'certified' if tag_certified(k, v) else 'FLOAT')]
    for N in (4, 3):
        lines += ['CLAIM_N%d = %s' % (N, ' ; '.join('%s %d' % p for p in CLAIM[N])), 'N%d_PIECES = %d' % (N, len(EXPORT_ROWS[N]))]
    for N in (4, 3):
        lines += ['N%d_P%04d = %s' % (N, i, row) for i, row in enumerate(EXPORT_ROWS[N])]
    return '\n'.join(lines + ['END = EXPORT_KT_S67_v1']) + '\n'


def c_export(text):
    """C-EXPORT (v2_2 (3)), on the export text before it is written. C-FMT: the port's S4U_KV_v1 reader and the reference parser give
    the same keys and values. The producer's reader (EXPORT_READER, S8's pin kt_s67_export_reader_v2_1, executed only after its sha256
    matches) reads the text as S8 will: through loads, with a run output stub of this export's EXPORT line and 'VERDICT VALID', when it
    reads EXPORT_STATUS = CERTIFIED, and through loads_noncert otherwise. It must return, for both N, every piece written, each bound
    equal to the row's decimal, jlo and jhi equal to the row's floats (rule V1) and each pair as written. The control,
    so that both branches run in every run: a copy with the other status (CERTIFIED when the text is not, FLOAT-PASS when it is) must
    give the same rows through its branch, and loads_noncert must refuse the CERTIFIED one of the two. PLANT-EXPORT: a copy with one
    value moved by one unit in its last digit must fail that comparison. Returns (the failures, whether the plant fired)."""
    srcs = {}
    for path, sha in (EXPORT_READER, S4U_REF):
        with open(os.path.join(CODEDIR, path), 'rb') as fh:
            srcs[path] = fh.read()
        if sha_bytes(srcs[path]) != sha:
            return ['%s differs from its pin' % path], False
    ns, ns2 = {}, {}
    exec(compile(srcs[EXPORT_READER[0]].decode('utf-8'), EXPORT_READER[0], 'exec'), ns)
    exec(compile(srcs[S4U_REF[0]].decode('utf-8'), S4U_REF[0], 'exec'), ns2)
    bad = [] if s4u_read_port(text) == ns2['parse_s4u_kv'](text) else ['C-FMT: the two S4U_KV_v1 readers differ']
    name = os.path.basename(export_path())

    def compare(t):
        try:
            if 'EXPORT_STATUS = CERTIFIED' in t.split('\n'):
                stub = 'EXPORT pk07/out/%s sha256 %s (C-EXPORT stub)\nVERDICT VALID\n' % (name, sha_bytes(t.encode('utf-8')))
                got = ns['loads'](t, stub, name)
            else:
                got = ns['loads_noncert'](t)
        except ValueError as e:
            return ['reader: %s' % e]
        diff = []
        for N in (4, 3):
            P = got['pieces'].get(N, {})
            if len(P) != len(EXPORT_ROWS[N]):
                diff.append('N=%d: %d pieces read, %d written' % (N, len(P), len(EXPORT_ROWS[N])))
            for i, row in enumerate(EXPORT_ROWS[N]):
                left, _, right = row.partition(' | ')
                want = {nm: ((math.inf if tk == 'inf' else float(tk)) if nm in ('jlo', 'jhi') else Fraction(tk))
                        for nm, tk in zip(EXPORT_FIELDS.split(), left.split(' '))}
                want['pairs'] = [dict(kind=g[0], d=int(g[1]), m_checked=int(g[2]), k_mode=int(g[3]), holds=g[4])
                                 for g in (grp.split(' ') for grp in right.split(' ; '))]
                if P.get(i) != want:
                    diff.append('N%d_P%04d' % (N, i))
        return diff
    bad += compare(text)
    st = [ln for ln in text.split('\n') if ln.startswith('EXPORT_STATUS = ')]       # both reader branches run in
    if len(st) == 1:                                                                 # every run, on the text and on a copy whose
        other = text.replace(st[0], 'EXPORT_STATUS = %s' % ('FLOAT-PASS' if st[0] == 'EXPORT_STATUS = CERTIFIED' else 'CERTIFIED'), 1)
        certified = text if st[0] == 'EXPORT_STATUS = CERTIFIED' else other          # status is the other one (CERTIFIED or not)
        try:
            ns['loads_noncert'](certified)
            refused = False
        except ValueError:
            refused = True
        if compare(other) or not refused:
            bad.append('C-EXPORT control: the other-status copy%s%s' % (' gives other rows' if compare(other) else '',
                                                                        '; loads_noncert accepts the CERTIFIED one' if not refused else ''))
    else:
        bad.append('C-EXPORT control: EXPORT_STATUS not found once')
    row0 = EXPORT_ROWS[4][0]
    toks = row0.split(' ')
    planted = text.replace('N4_P0000 = ' + row0, 'N4_P0000 = ' + ' '.join(toks[:2] + [s4u_bump(toks[2])] + toks[3:]), 1)
    fired = planted != text and 'N4_P0000' in compare(planted)
    return bad, fired


VMODE_OWN = ('CODE', 'RUN', 'RUN_VERDICT', 'EXPORT_STATUS')     # header keys each run writes for itself (not compared by C-VERT-MODES)


def c_vert_modes(text):
    """the Q2, C-VERT-MODES (full sweep only): the vertical run's EXPORT_KT_S67_v1 against this run's export text. The vertical run is
    taken only through its run output: with VMODE_PIN None, this file's own out_<label>_vsweep[_TAG].out, whose first line must name this
    file's sha256 and ITEM=vsweep; with VMODE_PIN, the pinned output and export by full sha256. Its VERDICT lines must be exactly
    ['VERDICT VALID'] and exactly one EXPORT line must name the export with the sha256 of the bytes read (EXPORT_READER's own binding
    _bound, rule V2). Compared string for string: every piece line, and every header line both runs write (FORMAT, RECORD, PRODUCER,
    FIELDS, PAIR_FIELDS, each TAG_* line, CLAIM_N*, N*_PIECES, END); the keys of VMODE_OWN and the comments are each run's own.
    PLANT-VERT-MODES: a copy of the vertical export with one digit of N3's last piece line moved must differ there. Returns (the
    failures, whether the plant fired, a description of the vertical run)."""
    if VMODE_PIN is None:
        epath, opath, pins = export_path('vsweep'), os.path.join(OUTD, 'out_%s_vsweep%s.out' % (LABEL, ('_' + TAG) if TAG else '')), None
    else:
        epath, opath, pins = os.path.join(CODEDIR, VMODE_PIN[0]), os.path.join(CODEDIR, VMODE_PIN[2]), (VMODE_PIN[1], VMODE_PIN[3])
    try:
        with open(epath, 'rb') as fh:
            eb = fh.read()
        with open(opath, 'rb') as fh:
            ob = fh.read()
    except OSError as e:
        return ['no vertical run (%s: %s)' % (e.__class__.__name__, os.path.relpath(opath, CODEDIR))], False, 'none', None
    with open(os.path.join(CODEDIR, EXPORT_READER[0]), 'rb') as fh:
        rsrc = fh.read()
    if sha_bytes(rsrc) != EXPORT_READER[1]:
        return ['%s differs from its pin' % EXPORT_READER[0]], False, 'none', None
    ns = {}
    exec(compile(rsrc.decode('utf-8'), EXPORT_READER[0], 'exec'), ns)
    otext, vtext = ob.decode('utf-8'), eb.decode('utf-8')
    head = otext.split('\n', 1)[0].split(' ')
    bad = []
    if pins is None and head[:4] != [LABEL, 'sha256', sha_file(os.path.abspath(__file__)), 'ITEM=vsweep']:
        bad.append('the run output\'s first line does not name this file\'s sha256 and ITEM=vsweep')
    if pins is not None and (sha_bytes(eb) != pins[0] or sha_bytes(ob) != pins[1] or head[3:4] != ['ITEM=vsweep']):
        bad.append('the vertical export or its run output differs from VMODE_PIN, or the output is not a vsweep')
    try:
        ns['_bound'](os.path.basename(epath), eb, otext)
    except ValueError as e:
        bad.append('binding: %s' % e)

    def keyed(t):
        keep, dup = {}, []
        for ln in t.split('\n'):
            if ln[:1] == '#' or not ln.strip():
                continue
            k, _, v = ln.partition(' = ')
            if k in VMODE_OWN:
                continue
            if k in keep:
                dup.append(k)
            keep[k] = v
        return keep, dup
    mine, dmine = keyed(text)

    def compare(t):
        theirs, dtheirs = keyed(t)
        return sorted(set(dmine + dtheirs)) + sorted(k for k in set(mine) | set(theirs) if mine.get(k) != theirs.get(k))
    diff = compare(vtext)
    bad += ['%s differs' % k for k in diff]
    k3 = 'N3_P%04d' % (len(EXPORT_ROWS[3]) - 1)
    lines = vtext.split('\n')
    hit = [i for i, ln in enumerate(lines) if ln.startswith(k3 + ' = ')]
    fired = False
    if len(hit) == 1:
        toks = lines[hit[0]].split(' ')
        lines[hit[0]] = ' '.join(toks[:4] + [s4u_bump(toks[4])] + toks[5:])          # k3, '=', jlo, jhi, then c5_lo
        fired = k3 in compare('\n'.join(lines))
    src = '%s sha256 %s, run output %s sha256 %s; %d lines compared' % (
        os.path.relpath(epath, CODEDIR), sha_bytes(eb)[:8], os.path.relpath(opath, CODEDIR), sha_bytes(ob)[:8], len(mine))
    return bad, fired, src, (os.path.relpath(epath, CODEDIR), sha_bytes(eb), os.path.relpath(opath, CODEDIR), sha_bytes(ob))


def export_path(mode=None):
    """the EXPORT_KT_S67_v1 path of this file's run of <mode> (default this run's MODE), in this folder's out/."""
    return os.path.join(OUTD, 'export_%s_%s%s.kv' % (LABEL, MODE if mode is None else mode, ('_' + TAG) if TAG else ''))


def write_export(text):
    """writes the export as a new file in this folder's out/ (never over an existing one) and reads it back. Returns (path, the sha256 of
    the bytes read back, the line count)."""
    path = export_path()
    if os.path.realpath(os.path.dirname(path)) != os.path.realpath(OUTD):
        raise RuntimeError('the export path is outside out/')
    with open(path, 'x') as fh:
        fh.write(text)
    with open(path, 'rb') as fh:
        back = fh.read()
    if back != text.encode('utf-8'):
        raise RuntimeError('the export read back differs from the text written')
    return path, sha_bytes(back), text.count('\n')


C2A_COVERAGE = ('P2-11 covers a pair of kind K (FLIP, SAME, MIXED) at N iff both of its end exponents are >= DH_N<N>_<K>, and P2-14\'s '
                'joint kind covers the overlapping pairs D3, D4, D4M at N iff both end exponents of the window are >= DH_N<N>_OVERLAP; '
                'P2-12 covers the rest at n >= 6 and P2-13 covers n <= 5')
C2A_END_RULE = ('columns are counted 1..n from each end, 1 at the end column; a vertical edge at column j from that end has end exponent '
                'd = j - 2 there, so an end column has d = -1 (S8\'s convention, SPEC_S8_CERT_v1 c0f95398 sect. 1); a t or bb edge takes its '
                'column nearer that end; a joint window takes its outer column on each side; e = R_w rho1^d with d the smaller of the two end '
                'exponents. Example: in an n = 6 strip a vertical on column 1 or column 6 has d = -1, and a t edge on columns 2-3 has d_L = 0 '
                'and d_R = 2')


def c2a_tags(SH1, TIN, JIN, kind):
    """the input tags a C2-a verdict rests on (full mode): the vertical inputs' TAGS, the t inputs and P2-10's
    beta_H for every kind; S9(b)'s A_a for the mixed kind; the joint inputs for a joint class; all of them for the export ('all'). Each
    reads certified only through TAG_PINS (tag_certified): 't inputs' from provide_tin with T_TAG_PIN, 'joint inputs' from provide_joint
    with JOINT_TAG_PIN; 'A_a' and 'beta_H' have no provider yet, so they read FLOAT."""
    t = {k: (TIN[k] if TIN is not None else SH1['tag']) for k in ('_tag', '_aa_tag', '_bh_tag')}
    tags = {**TAGS, 't inputs': t['_tag'], 'beta_H': t['_bh_tag']}
    if kind in ('mixed', 'all'):
        tags['A_a'] = t['_aa_tag']
    if kind in ('joint', 'all') and JIN is not None:
        tags['joint inputs'] = JIN.get('_tag', 'FLOAT')
    return tags


def export_c2a_text(res, SH1, JIN, TIN, why):
    """P2-11 step 6: the EXPORT_KT_S9H_v1 text (format S4U_KV_v1) for P2-12 and P2-16 (pk11's and the fields). Header: the coverage
    rule, the end-exponent rule, the claim and planning rules; per N and kind (and joint class) the claim threshold DH_N<N>_<K> (the
    largest of the pieces' own thresholds; certified run: certified slack > 0, no headroom factor), the planning threshold
    DH_PLAN_N<N>_<K> at HANDOFF_HR, the headroom table HEADROOM_N<N>_<K>; DH_N<N>_overlap (the largest over the joint classes); the
    inputs' tags. Piece lines: N<N>_P<index> = jlo jhi | per kind or class 'name dmin slack_lo' (the piece's own threshold, 'none' above
    DH_MAX; the k = 0 slack's lower end at the header DH, rounded down, J^2Cov units; n/a when the header DH is none)."""
    key = lambda k: 'TAG_' + re.sub(r'[^A-Z0-9]+', '_', k.upper())
    tags = c2a_tags(SH1, TIN, JIN, 'all')
    names = [k for k, _ in KINDS] + ([c for c, _ in JOINT_CLASSES] if JIN is not None else [])
    dhs = lambda v: str(v) if v <= DH_MAX else 'none'
    lines = ['# EXPORT_KT_S9H_v1: the C2-a thresholds and per-piece slacks of %s (sweep), for P2-12 and P2-16; format S4U_KV_v1 ("KEY = '
             'value"; # lines are comments). Piece lines: N<N>_P<index> = jlo jhi | name dmin slack_lo ; ... per kind and joint class.' % LABEL,
             'FORMAT = S4U_KV_v1', 'RECORD = EXPORT_KT_S9H_v1', 'PRODUCER = pk07',
             'CODE = pk21/p2/s4c/%s.py:%s' % (LABEL, sha_file(os.path.abspath(__file__))[:8]), 'RUN = %s' % MODE,
             'RUN_VERDICT = %s' % ('VALID' if not why else 'INVALID'), 'EXPORT_STATUS = %s' % verdict_word(tags, not why),
             'COVERAGE_RULE = %s' % C2A_COVERAGE, 'END_EXPONENT_RULE = %s' % C2A_END_RULE,
             'CLAIM_RULE = DH_N<N>_<K> is the smallest d at which the kind\'s k = 0 slack is certainly > 0 on every piece at d and at every '
             'larger d (checked for d <= DH_MAX; larger d follow, the slack being nonincreasing in e); no headroom factor; FLOAT inputs '
             'make these planning values until the certified run',
             'DMIN_RULE = every piece\'s own threshold dmin is <= the header DH_N<N>_<K>, so P2-12 can cover every pair below the header DH '
             'uniformly in J',
             'PLAN_RULE = DH_PLAN_N<N>_<K> is the smallest d from which every input\'s distance to flip is >= HANDOFF_HR_<K> on every piece '
             '(the planning rule); size P2-12 to the larger of DH_PLAN and the certified DH',
             'KINDS = %s' % ' '.join(k for k, _ in KINDS), 'JOINT_CLASSES = %s' % (' '.join(c for c, _ in JOINT_CLASSES) if JIN else ''),
             'DH_MAX = %d' % DH_MAX, 'HR_LEVELS = %s' % ' '.join('%g' % x for x in HR_LEVELS)]
    for k, v in tags.items():
        lines += ['%s = %s' % (key(k), v), '%s_STATUS = %s' % (key(k), 'certified' if tag_certified(k, v) else 'FLOAT')]
    for name in names:
        lines.append('HANDOFF_HR_%s = %g' % (name.upper(), HANDOFF_HR['joint'] if name in JOINT_W else HANDOFF_HR[name]))
    for N in (4, 3):
        R = res[N]
        for name in names:
            C = R['joint'][name] if name in JOINT_W else R['c2a'][name]
            dh, dp = R['handoff'][name]
            lines += ['DH_N%d_%s = %s' % (N, name.upper(), dhs(dh)), 'DH_PLAN_N%d_%s = %s' % (N, name.upper(), dhs(dp)),
                      'HEADROOM_N%d_%s = %s' % (N, name.upper(), ' '.join('d=%d %g' % (d, C['lev'][d]) for d in range(DH_MAX + 1)))]
        if JIN is not None:
            lines.append('DH_N%d_OVERLAP = %s' % (N, dhs(R['joint_dh'])))
        lines.append('N%d_PIECES = %d' % (N, len(EXPORT_ROWS[N])))
    for N in (4, 3):
        R = res[N]
        for i, row in enumerate(EXPORT_ROWS[N]):
            grp = []
            for name in names:
                C = R['joint'][name] if name in JOINT_W else R['c2a'][name]
                dh = R['handoff'][name][0]
                dmn, lows = C['rows'][i]
                s = lows[dh] if dh <= DH_MAX else None
                grp.append('%s %s %s' % (name, dhs(dmn), dec_dir(s, False) if s is not None else 'n/a'))
            lines.append('N%d_P%04d = %s | %s' % (N, i, ' '.join(row.split(' ')[:2]), ' ; '.join(grp)))
    return '\n'.join(lines + ['END = EXPORT_KT_S9H_v1']) + '\n'


def c_export_c2a(text, res, names):
    """P2-11 C-EXPORT2 on the C2-a export text before it is written: the two S4U_KV_v1 readers agree; every DH_N<N>_<K> and
    DH_PLAN_N<N>_<K> key is present once and reads an integer or 'none', and so does DH_N<N>_OVERLAP when joint classes are exported
    (a missing key is a failure, not a skip); every piece line is present and parses into (name, dmin, slack) groups
    in the order of names; C-DMIN: every piece's dmin is <= its header DH_N<N>_<K> (DMIN_RULE, on the written text). PLANT-EXPORT2: a copy
    with N4_P0000's first dmin set to none must fail C-DMIN; PLANT-EXPORT2-DH: a copy without the first DH_N4_<K> line must fail the key
    check. Returns (the failures, whether both plants fired)."""
    with open(os.path.join(CODEDIR, S4U_REF[0]), 'rb') as fh:
        refb = fh.read()
    if sha_bytes(refb) != S4U_REF[1]:
        return ['%s differs from its pin' % S4U_REF[0]], False
    ns = {}
    exec(compile(refb.decode('utf-8'), S4U_REF[0], 'exec'), ns)
    joint = [nm for nm in names if nm in JOINT_W]

    def check(t):
        rec = s4u_read_port(t)
        bad = [] if rec == ns['parse_s4u_kv'](t) else ['C-FMT: the two S4U_KV_v1 readers differ']
        for N in (4, 3):
            keys = (['DH_N%d_%s' % (N, nm.upper()) for nm in names] + ['DH_PLAN_N%d_%s' % (N, nm.upper()) for nm in names]
                    + (['DH_N%d_OVERLAP' % N] if joint else []))
            bad += ['C-DHKEY %s' % k for k in keys if rec.get(k) != 'none' and re.fullmatch(r'[0-9]+', rec.get(k) or '') is None]
            dh = {nm: rec.get('DH_N%d_%s' % (N, nm.upper())) for nm in names}
            for i in range(len(EXPORT_ROWS[N])):
                v = rec.get('N%d_P%04d' % (N, i), '')
                left, sep, right = v.partition(' | ')
                gs = [g.split(' ') for g in right.split(' ; ')] if sep else []
                if len(gs) != len(names) or any(len(g) != 3 or g[0] != nm for g, nm in zip(gs, names)):
                    bad.append('N%d_P%04d malformed' % (N, i))
                    continue
                for g in gs:
                    if dh[g[0]] in (None, 'none'):
                        continue
                    if g[1] == 'none' or int(g[1]) > int(dh[g[0]]):
                        bad.append('C-DMIN N%d_P%04d %s' % (N, i, g[0]))
        return bad
    bad = check(text)
    k0 = 'N4_P0000 = '
    ln = [x for x in text.split('\n') if x.startswith(k0)]
    planted = text
    if ln:
        left, _, right = ln[0][len(k0):].partition(' | ')
        g = right.split(' ; ')
        g0 = g[0].split(' ')
        planted = text.replace(ln[0], k0 + left + ' | ' + ' ; '.join([' '.join([g0[0], 'none', g0[2]])] + g[1:]), 1)
    fired = planted != text and any(b.startswith('C-DMIN N4_P0000') for b in check(planted))
    k1 = 'DH_N4_%s' % names[0].upper()
    dropped = '\n'.join(x for x in text.split('\n') if not x.startswith(k1 + ' = '))
    fired2 = dropped != text and ('C-DHKEY %s' % k1) in check(dropped)
    return bad, fired and fired2


def write_export_c2a(text):
    """writes the C2-a export as a new file in this folder's out/ (never over an existing one) and reads it back. Returns (path, the sha256
    of the bytes read back, the line count)."""
    path = os.path.join(OUTD, 'export_c2a_%s_%s%s.kv' % (LABEL, MODE, ('_' + TAG) if TAG else ''))
    if os.path.realpath(os.path.dirname(path)) != os.path.realpath(OUTD):
        raise RuntimeError('the C2-a export path is outside out/')
    with open(path, 'x') as fh:
        fh.write(text)
    with open(path, 'rb') as fh:
        back = fh.read()
    if back != text.encode('utf-8'):
        raise RuntimeError('the C2-a export read back differs from the text written')
    return path, sha_bytes(back), text.count('\n')


# ------------------------------------------------------------------ P2-11 harness: C-WIDTH, C-VERT and the FLOAT t provider
SLACK_RETURNS = (('        return ((Cm - err - t2) > 0) is True\n', '        return Cm - err - t2\n'),
                 ('    return (P >= et) is True and ((P * (P - 2 * et) - et * et - t2) > 0) is True\n',
                  '    return (P >= et) is True and (P * (P - 2 * et) - et * et - t2)\n'),
                 ('    return ((X * X - E - O - T) > 0) is True\n', '    return X * X - E - O - T\n'))
PLANT_WIDTH_EDIT = ('    return dict(A=k + wa, B=k + wb, D=k + wa + wb)\n', '    return dict(A=k + wa, B=k + wb, D=k + wa + wb + 1)\n')


def s7_namespace(src, slack=False, plant=False):
    """P2-11: executes a source text of S7 functions in a fresh namespace with the globals they read. slack: pj and pm return the slack
    interval of their final test instead of its sign (SLACK_RETURNS, each found exactly once); their early returns stay False. plant
    (PLANT-WIDTH): D's power over-shifted by one in width_exps (PLANT_WIDTH_EDIT). Returns the namespace."""
    edits = (SLACK_RETURNS if slack else ()) + ((PLANT_WIDTH_EDIT,) if plant else ())
    for old, new in edits:
        if src.count(old) != 1:
            raise RuntimeError('S7 source edit not found exactly once: %r' % old.strip())
        src = src.replace(old, new)
    ns = dict(iv=iv, pt=pt, MMAX=MMAX, KMAX=KMAX)
    exec(compile(src, 'S7 block (%s%s)' % ('slack' if slack else 'original', ', planted' if plant else ''), 'exec'), ns)
    return ns


def width_sides():
    """P2-11: the two sides of C-WIDTH. v2_2's side is its pinned S7 block (V22_S7, by sha256 of the slice). The fork's side is its own
    width-aware functions (inspect: width_exps, tw_abs, tw_mode, pj, pm, s7mono_hyp, coverage, coverage_claim, claim_holds), called at
    their defaults w = (1, 1) and side None. Returns dict(v22=..., v22s=..., fork=..., forks=..., forkp=...): originals, slack variants
    and the planted fork slack variant."""
    with open(os.path.join(CODEDIR, V22_S7[0])) as fh:
        lines = fh.read().split('\n')
    src = '\n'.join(lines[V22_S7[1] - 1:V22_S7[2]]) + '\n'
    if sha_bytes(src.encode()) != V22_S7[3]:
        raise RuntimeError('C-WIDTH: v2_2\'s S7 block differs from its pin')
    fsrc = '\n\n\n'.join(inspect.getsource(f) for f in (width_exps, tw_abs, tw_mode, pj, pm, s7mono_hyp, coverage, coverage_claim,
                                                        claim_holds))
    return dict(v22=s7_namespace(src), v22s=s7_namespace(src, slack=True), fork=s7_namespace(fsrc), forks=s7_namespace(fsrc, slack=True),
                forkp=s7_namespace(fsrc, slack=True, plant=True))


def same_value(a, b):
    """P2-11: two slack results agree bit for bit: both False, or both intervals with equal ends (certain comparisons only)."""
    if a is False or b is False:
        return a is False and b is False
    return ((a.a <= b.a) is True and (b.a <= a.a) is True and (a.b <= b.b) is True and (b.b <= a.b) is True)


def width_grid(S, side_a, side_b, Q, Mq, c1):
    """P2-11: the slack grid of C-WIDTH on one piece, between two slack namespaces: pj for both kinds, d in DS and m = 1..6; pm for both
    kinds, d in DS and k = 1..6; s7mono_hyp for d in DS and k0 = 1..6. Returns (the points that differ, the number of points)."""
    bad, n = [], 0
    for kind in ('flip', 'same'):
        for d in DS:
            for m in range(1, 7):
                n += 2
                if not same_value(S[side_a]['pj'](Q, d, m, kind, {}, c1), S[side_b]['pj'](Q, d, m, kind, {}, c1)):
                    bad.append('pj %s d=%d m=%d' % (kind, d, m))
                if not same_value(S[side_a]['pm'](Q, Mq, d, m, kind, {}), S[side_b]['pm'](Q, Mq, d, m, kind, {})):
                    bad.append('pm %s d=%d k=%d' % (kind, d, m))
    for d in DS:
        for k0 in range(1, 7):
            n += 1
            if S[side_a]['s7mono_hyp'](Q, Mq, d, k0, {}) is not S[side_b]['s7mono_hyp'](Q, Mq, d, k0, {}):
                bad.append('s7mono_hyp d=%d k0=%d' % (d, k0))
    return bad, n


def c_width_piece(S, N, E, grid):
    """P2-11 C-WIDTH on one piece: v2_2's coverage_claim against the fork's claimed-pair table (every piece), and with grid the slack
    grid between v2_2's and the fork's slack variants. Returns the differences."""
    c1 = E['S5']['c5']
    bad = [] if S['v22']['coverage_claim'](E['Q'], E['Mq'], {}, c1, CLAIM[N]) == E['cv'] else ['claimed-pair table']
    return bad + (width_grid(S, 'v22s', 'forks', E['Q'], E['Mq'], c1)[0] if grid else [])


WIDTH_CASES = ((1, 1), (2, 1), (1, 2), (2, 2))       # P2-11: (w_e, w_f), w_e the width of the left insertion
EXP_PROBES = ((1, 0, 1, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 1, 0, 1))      # (pa, Ba, pb, Bb): together they fix every power of both forms
PLANT_EXP_EDITS = (("aua * r1 ** ex['A'] * e * qb", "aua * r1 ** ex['B'] * e * qb"),
                   ("r1 ** (ex['A'] - k) * e * pa * e * qb", "r1 ** (ex['B'] - k) * e * pa * e * qb"))


def exp_table():
    """P2-11: the EXPONENT TABLE lines, read from width_exps (the powers the code uses) at k = 0, with a check that each
    power is k plus a constant (k = 0 against k = 1). Returns (lines, linear)."""
    lines, lin = [], True
    for wa, wb in WIDTH_CASES:
        e0, e1 = width_exps(wa, wb, 0), width_exps(wa, wb, 1)
        lin = lin and all(e1[x] - e0[x] == 1 for x in 'ABD')
        lines.append('EXPONENT TABLE (w_e, w_f) = (%d, %d): Jensen form (absolute units): <a,u><eps_L, S^p Q0 b> rho1^(k+%d), '
                     '<Q0 a, S^p eps_R><u,b> rho1^(k+%d), their product term rho1^(2k+%d), D and the 1 - 1/D term rho1^(k+%d); mode form '
                     'T_w (units of s_x^k): term 1 (1 - 1/D) rho1^%d, term 2 (left amplitude bare) rho1^%d, term 3 (right amplitude bare) '
                     'rho1^%d, term 4 rho1^(k+%d), denominator 1 - rho1^(k+%d) e^2' % (
                         wa, wb, e0['A'], e0['B'], e0['A'] + e0['B'], e0['D'], e0['D'], e0['A'], e0['B'], e0['D'], e0['D']))
    return lines, lin


def tw_expect(form, wa, wb, k, pa, Ba, pb, Bb):
    """P2-11 C-EXP: the formulas (dbd501bc sect. 2) written out at rho1 = 1/2 and e = 1 in exact rationals, without width_exps:
    form 'abs' (the Jensen form) or 'mode' (T_w)."""
    h = lambda n: Fraction(1, 2 ** n)
    A, B, D = k + wa, k + wb, k + wa + wb
    qa, qb = pa + Ba, pb + Bb
    if form == 'abs':
        return (pa * pb * h(D) + pa * h(A) * qb + pb * h(B) * qa + h(B) * qa * h(A) * qb) / (1 - h(D))
    return (h(wa + wb) * pa * pb + h(wa) * pa * qb + h(wb) * pb * qa + h(D) * qa * qb) / (1 - h(D))


def exp_probe(fns):
    """P2-11 C-EXP: tw_abs and tw_mode from the namespace fns at rho1 = 1/2, e = 1, on the EXP_PROBES, every pair of WIDTH_CASES and
    k = 0..3, against tw_expect: the result and an enclosure of the exact value must overlap and both be narrower than 1e-15 (certain
    comparisons; a power off by one moves a value by more than 2^-13 here). Returns the points that differ."""
    bad = []
    r1, e = pt(1) / 2, pt(1)
    for wa, wb in WIDTH_CASES:
        for k in range(4):
            for pr in EXP_PROBES:
                for form in ('abs', 'mode'):
                    _, got = fns['tw_' + form](r1, e, pt(pr[0]), pt(pr[1]), pt(pr[2]), pt(pr[3]), k, (wa, wb))
                    x = tw_expect(form, wa, wb, k, *pr)
                    want = pt(x.numerator) / x.denominator
                    if not (got is not None and (got.a <= want.b) is True and (want.a <= got.b) is True
                            and (got.b - got.a < 1e-15) is True and (want.b - want.a < 1e-15) is True):
                        bad.append('%s w=(%d,%d) k=%d probe %s' % (form, wa, wb, k, ''.join(str(v) for v in pr)))
    return bad


def c_exp(fails, fires):
    """P2-11: prints the EXPONENT TABLE and runs C-EXP on the fork's tw_abs and tw_mode. PLANT-EXP: copies of the two with
    the left-bare bracket term on the right width's power (PLANT_EXP_EDITS, each found exactly once) must fail C-EXP in both forms."""
    lines, lin = exp_table()
    for ln in lines:
        out(ln)
    bad = exp_probe({'tw_abs': tw_abs, 'tw_mode': tw_mode})
    ok = lin and not bad
    out('C-EXP (P2-11): every tabled power is k plus a constant: %s; tw_abs and tw_mode at rho1 = 1/2, e = 1 against the formulas '
        'written out (exact rationals; %d width pairs x k = 0..3 x %d probes x 2 forms): %s -> %s' % (
            'yes' if lin else 'NO', len(WIDTH_CASES), len(EXP_PROBES),
            'identical' if not bad else '%d differ (%s)' % (len(bad), ', '.join(bad[:4])), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-EXP')
    src = '\n\n\n'.join(inspect.getsource(f) for f in (width_exps, tw_abs, tw_mode))
    for old, new in PLANT_EXP_EDITS:
        if src.count(old) != 1:
            raise RuntimeError('PLANT-EXP: source edit not found exactly once: %r' % old)
        src = src.replace(old, new)
    ns = dict(iv=iv, pt=pt)
    exec(compile(src, 'PLANT-EXP copy', 'exec'), ns)
    pb = exp_probe(ns)
    fa, fm = any(b.startswith('abs ') for b in pb), any(b.startswith('mode ') for b in pb)
    out('PLANT-EXP (copies of tw_abs and tw_mode with the left-bare bracket term on the right width\'s power): C-EXP differs at %d '
        'points (Jensen form %s, mode form %s) -> %s' % (len(pb), fa, fm, 'FIRES' if (fa and fm) else 'DOES NOT FIRE'))
    if not (fa and fm):
        fires.append('PLANT-EXP')


VERT_ROWS = {4: {}, 3: {}}     # the certified snapshot: C-VERT's rows on v2_2's inputs (float_m3), on the sampled pieces


def c_vert(fires):
    """P2-11 C-VERT: the fork's export rows against v2_2's export (V22_EXPORT, full sha256 of the bytes read), string for string. With
    the M3 provider's records the production rows differ from v2_2's by design, so the rows compared are VERT_ROWS: each sampled
    piece's row on v2_2's inputs (float_m3: certified S4, the FLOAT M3 JSONs), the regression of the code at w = (1, 1); every piece
    when VERT_ROWS is empty (no M3 provider). PLANT-VERT: a copy of one compared row with a digit moved must differ. Returns the
    differences."""
    with open(os.path.join(CODEDIR, V22_EXPORT[0]), 'rb') as fh:
        raw = fh.read()
    if sha_bytes(raw) != V22_EXPORT[1]:
        return ['v2_2\'s export differs from its pin']
    rec = s4u_read_port(raw.decode('utf-8'))
    if any(VERT_ROWS.values()):
        mine = {'N%d_P%04d' % (N, i): row for N in (4, 3) for i, row in VERT_ROWS[N].items()}
    else:
        mine = {'N%d_P%04d' % (N, i): row for N in (4, 3) for i, row in enumerate(EXPORT_ROWS[N])}
    want = {k: v for k, v in rec.items() if re.fullmatch(r'N[34]_P[0-9]{4}', k) and (k in mine or not any(VERT_ROWS.values()))}
    bad = sorted(k for k in set(mine) | set(want) if mine.get(k) != want.get(k))
    k0 = 'N4_P0000'
    toks = mine.get(k0, '0 0 0').split(' ')
    planted = dict(mine, **{k0: ' '.join(toks[:2] + [s4u_bump(toks[2])] + toks[3:])})
    if not (planted[k0] != want.get(k0)):
        fires.append('PLANT-VERT')
    return bad


def sh1_read_port(text):
    """P2-11: the fork's reader of kt_sh1_v1's ENTRY lines: {(N, name): (graph, [coefficient strings])}; a repeated entry or a malformed
    ENTRY line is an error. It shares no code with the reference reader (SH1_REF)."""
    out_ = {}
    for ln in text.split('\n'):
        m = re.fullmatch(r'ENTRY N=([34]) (\S+) \(graph ([^,]+), Dn [0-9]+, Q-degree [0-9]+; series [0-9.]+ s, sums [0-9.]+ s\): '
                         r'ak=\[([^\]]*)\]', ln)
        if m is None:
            if ln.startswith('ENTRY'):
                raise ValueError('kt_sh1_v1 port reader: malformed ENTRY line %r' % ln[:80])
            continue
        key = (int(m.group(1)), m.group(2))
        if key in out_:
            raise ValueError('kt_sh1_v1 port reader: ENTRY N=%d %s repeated' % key)
        out_[key] = (m.group(3), [c.strip() for c in m.group(4).split(',')])
    return out_


def sh1_src_check(text, N):
    """P2-11 C-SRC of one kt_sh1_v1 output: its header prints SH1_CODE and ITEM=n<N>; C-HASH and C-CORE read PASS; every C-HARM N=<N>
    line (at least 15) reads PASS; its VERDICT lines are exactly ['VERDICT VALID'] (T48). Returns the failures."""
    lines = text.split('\n')
    bad = []
    if not re.fullmatch(r'kt_sh1_v1 sha256 %s ITEM=n%d LIM=[0-9]+ .*' % (SH1_CODE, N), lines[0]):
        bad.append('header')
    for pat in (r'C-HASH PASS \(.*', r'C-CORE PASS \(.*'):
        if sum(1 for ln in lines if re.fullmatch(pat, ln)) != 1:
            bad.append(pat.split(' ')[0])
    if not verdict_lines_ok(lines):
        bad.append('VERDICT lines')
    harm = [ln for ln in lines if ln.startswith('C-HARM N=%d ' % N)]
    if len(harm) < 15 or not all(ln.endswith('-> PASS') for ln in harm):
        bad.append('C-HARM lines')
    return bad


def provide_sh1(fails, fires):
    """P2-11, the FLOAT t provider's plumbing (its values are not used before the verdict on the plan). It reads kt_sh1_v1's two
    outputs and the reference reader once (C-HASH, full sha256), parses the outputs with the fork's reader and with the reference reader
    (executed only after its sha256 matches) and requires C-FMT (the same entries, graphs and coefficient strings, and every name of
    SH1_NAMES at both N) and C-SRC (sh1_src_check); PLANT-FMT-SH1 (the fork's reader on a copy with two ak lists swapped) and
    PLANT-SRC-SH1 (a copy with one C-HARM line FAIL) must fire. Returns {N: {name: [a_k floats]}} with the tag FLOAT."""
    STB_READS.append('provide_sh1')                             # v1_2: C-VERT-ONLY
    raws, s9b = {}, {}
    for N in (4, 3):
        with open(os.path.join(CODEDIR, SH1_OUT[N][0]), 'rb') as fh:
            raws[N] = fh.read()
        with open(os.path.join(CODEDIR, S9B_OUT[N][0]), 'rb') as fh:
            s9b[N] = fh.read()
    with open(os.path.join(CODEDIR, SH1_REF[0]), 'rb') as fh:
        refb = fh.read()
    ok_h = (all(sha_bytes(raws[N]) == SH1_OUT[N][1] and sha_bytes(s9b[N]) == S9B_OUT[N][1] for N in (4, 3))
            and sha_bytes(refb) == SH1_REF[1])
    out('C-HASH SH1 (P2-11, full sha256 of the bytes read here): kt_sh1_v1 outputs %s and %s, KT-S9B outputs %s and %s (the FLOAT bar '
        'stand-ins), reference reader %s -> %s' % (SH1_OUT[4][0], SH1_OUT[3][0], S9B_OUT[4][0], S9B_OUT[3][0], SH1_REF[0],
                                                  'PASS' if ok_h else 'FAIL'))
    if not ok_h:
        fails.append('C-HASH SH1')
        raise RuntimeError('SH1 provider: a pinned file differs from its pin; nothing is read from it')
    ns = {}
    exec(compile(refb.decode('utf-8'), SH1_REF[0], 'exec'), ns)
    texts = {N: raws[N].decode('utf-8') for N in (4, 3)}
    port, ref = {}, {}
    for N in (4, 3):
        port.update(sh1_read_port(texts[N]))
        ref.update(ns['read_entries'](texts[N]))
    miss = ['N%d %s' % (N, nm) for N in (4, 3) for nm in SH1_NAMES if (N, nm) not in port]
    ok_f = port == ref and not miss and len(port) == 2 * len(SH1_NAMES)
    out('C-FMT SH1: %d ENTRY lines; the fork\'s reader against the reference reader (%s, sha256 %s): %s; every SH1 name at both N: %s '
        '-> %s' % (len(port), SH1_REF[0], SH1_REF[1][:8], 'identical' if port == ref else 'DIFFER', 'yes' if not miss else
                  'NO (%s)' % ', '.join(miss[:6]), 'PASS' if ok_f else 'FAIL'))
    if not ok_f:
        fails.append('C-FMT SH1')
    src_bad = ['N=%d %s' % (N, b) for N in (4, 3) for b in sh1_src_check(texts[N], N)]
    out('C-SRC SH1: both outputs print kt_sh1_v1\'s code sha %s and their ITEM, C-HASH and C-CORE PASS, every C-HARM line PASS (t_0, '
        't_x^2, t_y^2, O_t, ...), VERDICT VALID -> %s' % (SH1_CODE[:8], 'PASS' if not src_bad else 'FAIL (%s)' % ', '.join(src_bad)))
    if src_bad:
        fails.append('C-SRC SH1')
    a, b = 'ENTRY N=4 Gxt,0,1 ', 'ENTRY N=4 Gxt,0,3 '
    la = [ln for ln in texts[4].split('\n') if ln.startswith(a)]
    lb = [ln for ln in texts[4].split('\n') if ln.startswith(b)]
    sw = texts[4]
    if len(la) == 1 and len(lb) == 1:
        sw = sw.replace(la[0], la[0].split('ak=')[0] + 'ak=' + lb[0].split('ak=')[1]).replace(
            lb[0], lb[0].split('ak=')[0] + 'ak=' + la[0].split('ak=')[1])
    pf = sw != texts[4] and {**port, **sh1_read_port(sw)} != ref
    out('PLANT-FMT-SH1 (the fork\'s reader on a copy with the ak lists of Gxt,0,1 and Gxt,0,3 swapped at N = 4): C-FMT %s -> %s' % (
        'differs' if pf else 'agrees', 'FIRES' if pf else 'DOES NOT FIRE'))
    if not pf:
        fires.append('PLANT-FMT-SH1')
    harm4 = [ln for ln in texts[4].split('\n') if ln.startswith('C-HARM N=4 ')]
    bad4 = sh1_src_check(texts[4].replace(harm4[0], harm4[0][:-len('PASS')] + 'FAIL', 1), 4) if harm4 else []
    ps = 'C-HARM lines' in bad4
    out('PLANT-SRC-SH1 (a copy with its first C-HARM line reading FAIL): C-SRC flags %s -> %s' % (', '.join(bad4) or 'nothing',
                                                                                             'FIRES' if ps else 'DOES NOT FIRE'))
    if not ps:
        fires.append('PLANT-SRC-SH1')
    pr_sh1 = 'VERDICT lines' in sh1_src_check(precert_copy(texts[4], 'STUB'), 4)          # T48: one plant per reader
    pr_s9b = not verdict_lines_ok(precert_copy(s9b[4].decode('utf-8')).split('\n'))
    out('PLANT-PRECERT-SH1 (T48: copies of kt_sh1_v1\'s and KT-S9B\'s N4 outputs reading VERDICT VALID-STUB and VALID-PRECERT): refused '
        '%s and %s -> %s' % (pr_sh1, pr_s9b, 'FIRES' if (pr_sh1 and pr_s9b) else 'DOES NOT FIRE'))
    if not (pr_sh1 and pr_s9b):
        fires.append('PLANT-PRECERT-SH1')
    vals = {N: {nm: [float(c) for c in port[(N, nm)][1]] for nm in SH1_NAMES} for N in (4, 3)}
    rs, ot, s9b_bad = {}, {}, []                                  # pk15's FLOAT stand-ins: KT-S9B's r and kt_sh1_v1's O_t at J = 300
    for N in (4, 3):
        lines = s9b[N].decode('utf-8').split('\n')
        if not re.fullmatch(r'kt_s9b_v2 sha256 %s ITEM=n%d LIM=[0-9]+ .*' % (S9B_CODE, N), lines[0]):
            s9b_bad.append('N=%d header' % N)
        if not verdict_lines_ok(lines):                                     # T48: exact VERDICT lines
            s9b_bad.append('N=%d verdict' % N)
        rs[N] = {}
        for ln in lines:
            m = re.fullmatch(r'ENTRY N=%d J=300 (\S+) ak=\[[^\]]*\] rem=\S+ tail=\S+ ann=\S+ far=\S+ r=([0-9.e+-]+) \(.*' % N, ln)
            if m is not None and m.group(1) in S9B_NAMES:
                rs[N][m.group(1)] = m.group(2)
        s9b_bad += ['N=%d %s missing' % (N, nm) for nm in S9B_NAMES if nm not in rs[N]]
        c7 = [m.group(1) for m in (re.fullmatch(r'READ C7 N=%d J=300: \|t_x\| \S+, dt_x \S+, A_t \S+; O_t ([0-9.e+-]+); .*' % N, ln)
                                   for ln in texts[N].split('\n')) if m is not None]
        if len(c7) == 1:
            ot[N] = c7[0]
        else:
            s9b_bad.append('N=%d READ C7 O_t' % N)
    out('C-SRC SH1 bars (P2-11, pk15\'s FLOAT stand-ins): KT-S9B outputs print kt_s9b_v2\'s code sha %s and their ITEM, VERDICT VALID, '
        'the r of %s at both N; kt_sh1_v1\'s READ C7 lines give O_t -> %s; e.g. r(Ih,1) N=4 %s, O_t N=4 %s, N=3 %s' % (
            S9B_CODE[:8], ', '.join(S9B_NAMES), 'PASS' if not s9b_bad else 'FAIL (%s)' % ', '.join(s9b_bad),
            rs[4].get('Ih,1'), ot.get(4), ot.get(3)))
    if s9b_bad:
        fails.append('C-SRC SH1 bars')
    out('INFO SH1 (FLOAT, not used before the verdict): N=4 t-entries %s; e.g. Gxt,0,1 a_0 %s, IhTt,1 a_0 %s' % (
        len(vals[4]), port[(4, 'Gxt,0,1')][1][0], port[(4, 'IhTt,1')][1][0]))
    s9t = {N: s9b[N].decode('utf-8') for N in (4, 3)}
    tin, tbad = t_float_inputs(texts, s9t)
    if tbad:
        fails.append('T-FLOAT parse')
        out('T-FLOAT parse failures: %s' % ', '.join(tbad))
    for N in (4, 3):
        if N in tin:
            T = tin[N]
            out('INFO T-FLOAT N=%d (P2-11 FLOAT stand-ins from kt_sh1_v1\'s READ lines at J = 300, J-constant; trial frame, margins '
                'TF_MARGIN): A_t >= %s, O_t <= %s, V_t <= %s, pi_t <= %s (t_y^2 %s, QSI %s, dt_x %s), A_a >= %s, beta_H <= %s; h for t '
                '(PLANT-PAIR): A_h >= %s' % (N, nf(T['At']), nf(T['Ot']), nf(T['Vt']), nf(T['Pt']), nf(T['ty2']), nf(T['Q']),
                                             nf(T['dtx']), nf(T['Aa']), nf(T['bH']), nf(T['Ah'])))
    aa = {N: tin[N]['aa_ok'] for N in tin}
    ok_aa = len(aa) == 2 and all(aa.values())
    out('C-AA (P2-11: the FLOAT A_a record): a_x from kt_sh1_v1\'s C-READ line against KT-S9B\'s READ line, both '
        'files pinned in C-HASH SH1, to KT-S9B\'s printed digits (relative 1e-7): %s -> %s' % (
            '; '.join('N=%d %s / %s' % (N, tin[N]['ax_s'][0], tin[N]['ax_s'][1]) for N in sorted(tin)), 'PASS' if ok_aa else 'FAIL'))
    if not ok_aa:
        fails.append('C-AA')
    pa_ = 4 in tin and not aa_agree(tin[4]['ax_s'][0], '%.8g' % (float(tin[4]['ax_s'][1]) * 1.0001))
    out('PLANT-AA (KT-S9B\'s N=4 a_x moved by 1e-4 relative): C-AA %s -> %s' % ('refuses it' if pa_ else 'accepts it',
                                                                              'FIRES' if pa_ else 'DOES NOT FIRE'))
    if not pa_:
        fires.append('PLANT-AA')
    out('SIGN (P2-11): the mixed x part needs <e_x, v_t><e_x, v_a> > 0. P2-5\'s bulk sign is for the Ritz '
        'amplitudes (X_ta = t~_x a~_x > 0); the true components carry those signs because A_t = |t~_x| - dt_x > 0 and A_a = |a~_x| - da_x '
        '> 0 (Lemma A\'s delta below |amplitude|): %s -> %s' % (
            '; '.join('N=%d X_ta > 0, A_t > 0, A_a > 0: %s' % (N, tin[N]['sign']) for N in sorted(tin)),
            'DERIVED' if (len(tin) == 2 and all(tin[N]['sign'] for N in tin)) else 'NOT DERIVED (the mixed kind is not claimed)'))
    return dict(vals=vals, r=rs, O_t=ot, tin=tin, tag='FLOAT (kt_sh1_v1 exact a_k %s / %s; bars from KT-S9B %s / %s)' % (
        SH1_OUT[4][1][:8], SH1_OUT[3][1][:8], S9B_OUT[4][1][:8], S9B_OUT[3][1][:8]))


TF_MARGIN = dict(At=Fraction(98, 100), Ot=Fraction(105, 100), Vt=Fraction(102, 100), Pt2=Fraction(105, 100), Aa=Fraction(98, 100),
                 bH=Fraction(11, 10))
TF_NUM = r'(-?[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)'


def tf_scale(x, f):
    """x (mp.iv) times the exact rational f."""
    return x * pt(f.numerator) / pt(f.denominator)


def aa_agree(s1, s2):
    """P2-11 C-AA: two printed decimals of a_x agree to relative 1e-7 of the second (certain comparison on exact decimals)."""
    x1, x2 = dec_iv(s1), dec_iv(s2)
    return (abs(x1 - x2) <= abs(x2) * pt(1) / 10 ** 7) is True


def t_float_inputs(texts, s9t):
    """P2-11: the FLOAT stand-ins of the t inputs per N (NOTE_P2_11_C2A_v1 sect. 1, pk15's FLOAT rule), from kt_sh1_v1's lines at
    J = 300 (texts: provide_sh1's C-HASH'd outputs; s9t: KT-S9B's, for C-AA), one J-constant value per N. They are trial-frame
    references without the rows' conversion bars, so they carry the margins TF_MARGIN:
      A_t = READ C7's A_t x 0.98;  O_t = READ C7's O_t x 1.05;
      V_t = (|t_x|^2 + t_y^2 + QSI^2) x 1.02 (pk15's (t_x^2 + t_y^2 + |Q4 v_t|^2)/(1 - s'^2), QSI in place of |Q4 v_t|);
      pi_t = ((2 |t_x| dt_x + t_y^2 + QSI^2) x 1.05)^1/2 >= |P_perp v_t|, the joint form |v+|^2 - (|t~_x| - dt_x)^2 <= t~0^2
        + 2 |t~_x| dt_x + t~_y^2 + |Qv+|^2 (no V_t - A_t^2 cancellation; t~0^2 <= s'^2 V_t inside the margin);
      t_y^2 = (h_y t_y)(t_y a_y)/(h_y a_y) from the three READ C5 products; QSI and dt_x from READ INPUTS;
      A_a = (|a_x| - da_x) x 0.98, a_x from the C-READ line (C-AA: against KT-S9B's READ line), da_x from READ INPUTS;
      A_h = (|h_x| - dh_x) x 0.98, for PLANT-PAIR (h in place of t);
      beta_H = 1.1 x the harmonic H-NORM value (N - 1)(5^-1/2 + 21^-1/2)/4;
      sign: X_ta > 0 (READ KT-C8) with A_t > 0 and A_a > 0.
    Every value comes from exact decimals in mp.iv, the lower or upper end as the bound needs. Returns ({N: dict}, parse failures)."""
    res, bad = {}, []
    for N in (4, 3):
        lines, lines9 = texts[N].split('\n'), s9t[N].split('\n')

        def grab(pat, n, src=None):
            ms = [m for m in (re.match(pat % N, ln) for ln in (lines if src is None else src)) if m is not None]
            if len(ms) != 1:
                bad.append('N=%d %s' % (N, pat.split(' N=')[0]))
                return None
            return [ms[0].group(i + 1) for i in range(n)]
        inp = grab(r'READ INPUTS N=%d J=300: .*? QSI ' + TF_NUM + r'; dh_x ' + TF_NUM + r' da_x ' + TF_NUM + r' dt_x ' + TF_NUM + r';', 4)
        c7 = grab(r'READ C7 N=%d J=300: \|t_x\| ' + TF_NUM + r', dt_x \S+, A_t ' + TF_NUM + r'; O_t ' + TF_NUM + r'; ', 3)
        c8 = grab(r'READ KT-C8 N=%d J=300: X_ta = t_x a_x ' + TF_NUM + r' \(', 1)
        ht = grab(r'READ C5 N=%d J=300 \(h, t\): e_y f_y ' + TF_NUM + r', ', 1)
        ha = grab(r'READ C5 N=%d J=300 \(h, a\): e_y f_y ' + TF_NUM + r', ', 1)
        ta = grab(r'READ C5 N=%d J=300 \(t, a\): e_y f_y ' + TF_NUM + r', ', 1)
        cr = grab(r'C-READ N=%d: h_x ' + TF_NUM + r', a_x ' + TF_NUM + r', x_R ', 2)
        r9 = grab(r'READ N=%d J=300: h_x ' + TF_NUM + r', a_x ' + TF_NUM + r', x_R ', 2, lines9)
        if None in (inp, c7, c8, ht, ha, ta, cr, r9):
            continue
        Q, dh, da, dtx = (dec_iv(s) for s in inp)
        tx, At, Ot = (dec_iv(s) for s in c7)
        Xta, hx, ax = dec_iv(c8[0]), abs(dec_iv(cr[0])), abs(dec_iv(cr[1]))
        ty2 = dec_iv(ht[0]) * dec_iv(ta[0]) / dec_iv(ha[0])
        if (ty2.a > 0) is not True:
            bad.append('N=%d t_y^2 not positive' % N)
            continue
        Atl = pt(tf_scale(At, TF_MARGIN['At']).a)
        Aal = pt(tf_scale(ax - da, TF_MARGIN['Aa']).a)
        res[N] = dict(At=Atl, Ot=pt(tf_scale(Ot, TF_MARGIN['Ot']).b), Vt=pt(tf_scale(tx * tx + ty2 + Q * Q, TF_MARGIN['Vt']).b),
                      Pt=pt(iv.sqrt(tf_scale(2 * tx * dtx + ty2 + Q * Q, TF_MARGIN['Pt2'])).b), Aa=Aal,
                      Ah=pt(tf_scale(hx - dh, TF_MARGIN['At']).a),
                      bH=pt(tf_scale(pt(N - 1) * (1 / iv.sqrt(5) + 1 / iv.sqrt(21)) / 4, TF_MARGIN['bH']).b),
                      sign=(Xta > 0) is True and (Atl > 0) is True and (Aal > 0) is True, ty2=ty2, Q=Q, dtx=dtx,
                      aa_ok=aa_agree(cr[1], r9[1]), ax_s=(cr[1], r9[1]))
    return res, bad


# ------------------------------------------------------------------ the certified snapshot's t provider: pk15's kt_p2_assembly export
T_FIELDS_NEED = ('jlo', 'jhi', 'At_lo', 'Vt_hi', 'Ot_hi', 'Xta_lo', 'Xtb_lo', 'Pt_hi', 'dtx_hi')   # read by name; Aa_lo optional
T_MODE = 'mock'          # 'float': kt_sh1_v1's J-constant stand-ins only; 'mock': pk15's MOCK t export; 'certified': T_REC['certified']
T_REC = dict(mock=dict(path='pk15/mocks/out/export_p2_t_mock_kt_p2_assembly_v1_24.kv',         # kt_p2_assembly_v1_24 ded07b5e, MOCK
                       sha256='25f7c6af3264c4741ffbe2330223a3c7aeded71ad2a9bf5401abd097f336f414',  # run; EXPORT_P2_T_v1 with Aa_lo, FLOAT_IN
                       out=('pk15/mocks/out/out_kt_p2_assembly_v1_24_mock.out',                 # with the assembly's own tokens, and
                            'c5bc08c5ceb4683a5fcb69f6ebea41c51f5a4ab291a4365e65164edecfc38c54'),    # (v1_1 P-3) ce_lo ce_hi, route B
                       record='EXPORT_P2_T_v1', fmt='S4U_KV_v1 MOCK', status='MOCK', producer='pk15'),
             certified=None)   # the same keys, fmt 'S4U_KV_v1' and status 'CERTIFIED', once pk15's certified run is frozen (the Q1)
T_TAG_PIN = None         # ('pk15', the record's sha8) for TAG_PINS['t inputs'] once T_REC['certified'] is filled


def bound_ok(name, sha, otext):
    """rule V2 for a producing output (EXPORT_READER's binding, here for pk15's records): its VERDICT lines are exactly
    ['VERDICT VALID'] and exactly one 'EXPORT <path> sha256 <hex> ...' line has the record's base name as <path>'s, with <hex> its sha256."""
    lines = otext.split('\n')
    hits = [h for h in (ln.split() for ln in lines if ln.startswith('EXPORT ')) if len(h) >= 4 and h[2] == 'sha256'
            and os.path.basename(h[1]) == name]
    return verdict_lines_ok(lines) and len(hits) == 1 and hits[0][3] == sha


def t_read(rec, grid, R, aa):
    """the t inputs from a parsed EXPORT_P2_TPROV_v1 record (pk15's kt_p2_assembly export; the Q1): ({(N, i): dict(At, Vt, Ot, Pt,
    Xta, Xtb, Aa)}, problems). Header: RECORD and END EXPORT_P2_TPROV_v1, FORMAT and EXPORT_STATUS the mode's (R: S4U_KV_v1 and
    CERTIFIED, or S4U_KV_v1 MOCK and MOCK), RUN_VERDICT VALID, FIELDS naming every field of T_FIELDS_NEED once (read by name), PRECERT or
    STUB refused; a CERTIFIED record must carry T_CERT_REQUIRE's keys and values. C-GRID: every row
    present with jlo, jhi string for string as the grid. C-FLIP, a declaration check (pk15's XTB_SOURCE = FLIP_OF_XTA
    ): the header declares FLIP_OF_XTA and every Xtb_lo equals its Xta_lo string for string. SIGN: A_t, A_a and X_ta certainly
    > 0. A_a is the record's Aa_lo when FIELDS names it, else aa[N] (S9(b)'s FLOAT stand-in, J-constant). v1_1 P-3: when FIELDS names
    ce_lo and ce_hi (pk15's route B), each row's c_e ball (ce_lo <= ce_hi) is kept as 'ce' for provide_bh."""
    bad, T = [], {}
    fields = rec.get('FIELDS', '').split(' ')
    idx = {f: k for k, f in enumerate(fields)}
    if (rec.get('RECORD') != R['record'] or rec.get('END') != R['record'] or rec.get('FORMAT') != R['fmt']
            or rec.get('EXPORT_STATUS') != R['status'] or rec.get('RUN_VERDICT') != 'VALID' or fields[:2] != ['jlo', 'jhi']
            or len(idx) != len(fields) or any(f not in idx for f in T_FIELDS_NEED)):
        bad.append('header')
        return T, bad
    if marked_precert(rec) or 'PRECERT' in rec.get('TAG', '').upper() or 'STUB' in rec.get('TAG', '').upper():
        bad.append('marked PRECERT or STUB')
    if rec.get('EXPORT_STATUS') == 'CERTIFIED' or rec.get('TAG', '').startswith('CERTIFIED'):
        bad += ['certified requirement %s' % k for k, v in T_CERT_REQUIRE.items() if rec.get(k) != v]
        if not float_in_empty(rec.get('FLOAT_IN')):                       # the rule: no FLOAT input under a CERTIFIED status
            bad.append('certified requirement FLOAT_IN empty')
    if rec.get('XTB_SOURCE') != 'FLIP_OF_XTA':
        bad.append('C-FLIP declaration XTB_SOURCE %r' % rec.get('XTB_SOURCE'))
    for N in (4, 3):
        if rec.get('N%d_PIECES' % N) != str(len(grid)):
            bad.append('N%d_PIECES' % N)
        for i, (jlo, jhi) in enumerate(grid):
            v = rec.get('N%d_P%04d' % (N, i), '').split(' ')
            if len(v) != len(fields) or v[0] != jlo or v[1] != jhi:
                bad.append('C-GRID N%d_P%04d' % (N, i))
                continue
            At, Vt, Ot, Pt, Xta, Xtb, dtx = (dec_iv(v[idx[f]]) for f in ('At_lo', 'Vt_hi', 'Ot_hi', 'Pt_hi', 'Xta_lo', 'Xtb_lo', 'dtx_hi'))
            Aa = dec_iv(v[idx['Aa_lo']]) if 'Aa_lo' in idx else aa[N]
            if v[idx['Xtb_lo']] != v[idx['Xta_lo']]:
                bad.append('C-FLIP N%d_P%04d' % (N, i))
            if not ((At > 0) is True and (Aa > 0) is True and (Xta > 0) is True):
                bad.append('SIGN N%d_P%04d' % (N, i))
            T[(N, i)] = dict(At=pt(At.a), Vt=pt(Vt.b), Ot=pt(Ot.b), Pt=pt(Pt.b), Xta=pt(Xta.a), Xtb=pt(Xtb.a), Aa=pt(Aa.a), dtx=pt(dtx.b))
            if 'ce_lo' in idx and 'ce_hi' in idx:                  # v1_1 P-3: c_e's ball for beta_H (pk15's route B)
                ce = (pt(dec_iv(v[idx['ce_lo']]).a), pt(dec_iv(v[idx['ce_hi']]).b))
                if not ((ce[0] <= ce[1]) is True):
                    bad.append('CE N%d_P%04d' % (N, i))
                T[(N, i)]['ce'] = ce
    return T, bad


def provide_tin(SH1, fails, fires):
    """the certified snapshot's t provider (T_MODE; the Q1: pk15's kt_p2_assembly export through a bound reader, never
    kt_cert_v1_7's records directly): the per-piece t inputs from EXPORT_P2_TPROV_v1, certified or MOCK. C-HASH: the record and its
    producing output, full sha256 of the bytes read. C-BIND T (rule V2, bound_ok): the output's VERDICT lines exactly ['VERDICT VALID'] and
    one EXPORT line naming the record with its sha256. C-FMT T: the port's reader against s4u_kv_ref_v1. t_read's header, C-GRID, C-FLIP
    (a declaration check) and SIGN. Plants: PLANT-BIND-T (the EXPORT line's sha256 changed), PLANT-FLIP (one Xtb_lo moved by 1%),
    PLANT-GRID-T (two rows' values swapped), PLANT-CERTREQ-T (a CERTIFIED copy without T_CERT_REQUIRE). A_a is the record's Aa_lo when
    it has one, else S9(b)'s FLOAT stand-in (SH1; tag _aa_tag); beta_H starts at SH1's FLOAT value (tag _bh_tag), which provide_bh
    (v1_1, P-3) replaces after C-TRIAL. The t tag reads CERTIFIED only in certified mode with every check passing and T_TAG_PIN set (TAG_PINS['t inputs'],
    ). Returns {(N, i): T} (t_float_inputs' keys, sign included) or None in float mode."""
    STB_READS.append('provide_tin')                             # v1_2: C-VERT-ONLY
    if T_MODE == 'float':
        out('INFO t provider: FLOAT mode, kt_sh1_v1\'s J-constant stand-ins (t_float_inputs)')
        return None
    R = T_REC[T_MODE]
    with open(os.path.join(CODEDIR, R['path']), 'rb') as fh:
        raw = fh.read()
    with open(os.path.join(CODEDIR, S4U_REF[0]), 'rb') as fh:
        refb = fh.read()
    with open(os.path.join(CODEDIR, R['out'][0]), 'rb') as fh:
        rawo = fh.read()
    ok_h = sha_bytes(raw) == R['sha256'] and sha_bytes(refb) == S4U_REF[1] and sha_bytes(rawo) == R['out'][1]
    out('C-HASH T (%s mode; full sha256 of the bytes read here): %s and its producing output %s, reference parser -> %s' % (
        T_MODE, R['path'], R['out'][0], 'PASS' if ok_h else 'FAIL'))
    if not ok_h:
        fails.append('C-HASH T')
        raise RuntimeError('t provider: a pinned file differs from its pin; nothing is read from it')
    text, texto, name = raw.decode('utf-8'), rawo.decode('utf-8'), os.path.basename(R['path'])
    ok_b = bound_ok(name, R['sha256'], texto)
    ns = {}
    exec(compile(refb.decode('utf-8'), S4U_REF[0], 'exec'), ns)
    port, ref = s4u_read_port(text), ns['parse_s4u_kv'](text)
    grid = joint_grid()
    aa = {N: SH1['tin'][N]['Aa'] for N in (4, 3)}
    T, bad = t_read(port, grid, R, aa)
    ok = port == ref and ok_b and not bad
    out('C-BIND T, C-FMT T, C-GRID, C-FLIP, SIGN (%s mode): the producing output\'s VERDICT lines exactly [\'VERDICT VALID\'] and one EXPORT '
        'line naming %s with its sha256: %s; %d keys, the two S4U_KV_v1 readers %s; %d piece rows on the grid; C-FLIP declared %s, Xtb_lo = '
        'Xta_lo string for string; A_t, A_a, X_ta > 0 (A_a: %s); header as agreed -> %s' % (
            T_MODE, name, ok_b, len(port), 'identical' if port == ref else 'DIFFER', len(T), port.get('XTB_SOURCE'),
            'the record\'s Aa_lo' if 'Aa_lo' in port.get('FIELDS', '').split(' ') else 'S9(b)\'s FLOAT stand-in, J-constant',
            'PASS' if ok else 'FAIL (%s)' % ', '.join(bad[:6])))
    if not ok:
        fails.append('C-BIND/C-FMT/C-GRID/C-FLIP T')
    k0, k1 = 'N4_P0000', 'N4_P0001'
    fields = port.get('FIELDS', '').split(' ')
    v = port.get(k0, '').split(' ')
    ix = fields.index('Xtb_lo') if 'Xtb_lo' in fields else -1
    moved = dict(port, **{k0: ' '.join(v[:ix] + [s4u_bump(v[ix])] + v[ix + 1:])}) if 0 <= ix < len(v) else port   # built from strings
    pf = any(b.startswith('C-FLIP N4_P0000') for b in t_read(moved, grid, R, aa)[1])
    pg = any(b.startswith('C-GRID') for b in t_read(dict(port, **{k0: port.get(k1, ''), k1: port.get(k0, '')}), grid, R, aa)[1])
    stripped = {k: x for k, x in port.items() if k not in T_CERT_REQUIRE}
    pc = any(b.startswith('certified requirement') for b in t_read(
        dict(stripped, EXPORT_STATUS='CERTIFIED', FORMAT='S4U_KV_v1', TAG='CERTIFIED pk15 00000000'), grid,
        dict(R, fmt='S4U_KV_v1', status='CERTIFIED'), aa)[1])
    fi = port.get('FLOAT_IN') if not float_in_empty(port.get('FLOAT_IN')) else 'planted: far'
    pfi = 'certified requirement FLOAT_IN empty' in t_read(
        dict(port, EXPORT_STATUS='CERTIFIED', FORMAT='S4U_KV_v1', TAG='CERTIFIED pk15 00000000', FLOAT_IN=fi, **T_CERT_REQUIRE), grid,
        dict(R, fmt='S4U_KV_v1', status='CERTIFIED'), aa)[1]
    bsha = ('0' if R['sha256'][0] != '0' else '1') + R['sha256'][1:]
    pb = not bound_ok(name, R['sha256'], texto.replace(R['sha256'], bsha))
    out('PLANT-BIND-T (the EXPORT line\'s sha256 changed) %s; PLANT-FLIP (N4_P0000\'s Xtb_lo, its last digit moved) %s; PLANT-GRID-T (two rows\' values '
        'swapped) %s; PLANT-CERTREQ-T (a CERTIFIED copy without %s) %s; PLANT-FLOATIN-T (a CERTIFIED copy with every requirement but a '
        'FLOAT_IN token) %s' % (
            'FIRES' if pb else 'DOES NOT FIRE', 'FIRES' if pf else 'DOES NOT FIRE', 'FIRES' if pg else 'DOES NOT FIRE',
            ', '.join(T_CERT_REQUIRE), 'FIRES' if pc else 'DOES NOT FIRE', 'FIRES' if pfi else 'DOES NOT FIRE'))
    for nm, f in (('PLANT-BIND-T', pb), ('PLANT-FLIP', pf), ('PLANT-GRID-T', pg), ('PLANT-CERTREQ-T', pc), ('PLANT-FLOATIN-T', pfi)):
        if not f:
            fires.append(nm)
    for (N, i), t in T.items():
        t['bH'] = SH1['tin'][N]['bH']                                       # SH1's FLOAT beta_H; provide_bh (v1_1) replaces it
        t['sign'] = (t['Xta'] > 0) is True and (t['At'] > 0) is True and (t['Aa'] > 0) is True
    if T_MODE == 'certified' and ok and T_TAG_PIN is not None:
        TAG_PINS['t inputs'] = T_TAG_PIN
        T['_tag'] = 'CERTIFIED %s %s' % T_TAG_PIN
    else:
        T['_tag'] = '%s (%s)' % ('MOCK' if T_MODE == 'mock' else 'FLOAT', port.get('TAG', 'no TAG'))
    T['_aa_tag'] = T['_tag'] if 'Aa_lo' in fields else 'FLOAT (S9(b)\'s A_a stand-in: kt_sh1_v1 READ lines, J-constant)'
    T['_bh_tag'] = 'FLOAT (P2-10\'s beta_H: 1.1 x the harmonic H-NORM value)'
    return T


def t_scan_inputs(TIN, SH1, N, idx):
    """the t inputs of the scan's [300, 303]: the per-piece inputs combined over the grid pieces idx that meet it (lowest lower bounds,
    highest upper bounds), or SH1's J-constant stand-ins in float mode."""
    if TIN is None:
        return SH1['tin'][N]
    ts = [TIN[(N, i)] for i in idx]
    T = {k: pmin([t[k] for t in ts]) for k in ('At', 'Aa', 'Xta', 'Xtb')}
    T.update({k: pmax([t[k] for t in ts]) for k in ('Vt', 'Ot', 'Pt', 'bH', 'dtx')})
    T['sign'] = all(t['sign'] for t in ts)
    T['Ah'] = SH1['tin'][N]['Ah']
    return T


# ------------------------------------------------------------------ the beta_H provider (v1_1)
S4H_HEADER = dict(FORMAT=S4H['fmt'], RECORD=S4H['record'], END=S4H['record'], AUTHOR=S4H['producer'], J_MIN='300')
S4H_ROWS = ('T', 'M')                    # rule (a): row T is the t bond (kind t, and bb by the flip), row M the h bond
S4H_BALLS = ('D0', 'D1', 'D2', 'D3', 'U3P_1_300')
S4H_READ = ('R_CERT', 'R_MAIN', 'R_CROSS', 'R_INS', 'TAIL', 'L2P', 'OFF_OMEGA', 'TOL')     # the READING line's values, in order
S4H_USED = tuple(S4H_HEADER) + ('CODE',) + tuple('N%d_%s' % (N, k) for N in (4, 3) for k in ('ASM_OUTPUT', 'VERDICT', 'CHECKS',
                                                                                            'TOL_RESULT')) + tuple(
    'N%d_%s_%s' % (N, r, k) for N in (4, 3) for r in S4H_ROWS for k in tuple(b + e for b in S4H_BALLS for e in ('', '_LO', '_HI')) + S4H_READ)
S4H_U3P = r'U3_P N=%d row %s: d_0 (\[[^\]]*\]), d_1 (\[[^\]]*\]), d_2 (\[[^\]]*\]), d_3 (\[[^\]]*\]); U3_p\(1/300\) (\[[^\]]*\])'
S4H_READING = (r'READING N=%d row %s \(t = 1/300, every J >= 300\): R_cert <= ([0-9.e+-]+); R_main <= ([0-9.e+-]+), '
               r'R_cross <= ([0-9.e+-]+), R_ins <= ([0-9.e+-]+), tail <= ([0-9.e+-]+) \(L2\^\(p\) <= ([0-9.e+-]+)\), '
               r'off-Omega <= ([0-9.e+-]+); TOL >= ([0-9.e+-]+)')
S4H_HARM = {(4, 'T'): '0.4991', (4, 'M'): '0.6547', (3, 'T'): '0.3327', (3, 'M'): '0.4364'}   # SH4 l.143: the harmonic diagonal
#                                         <u, P_L u>/lambda_0^2 = (N-1)/2 - c_e at t = 0 of the t and h bonds (hand numbers, the guard's)


def s4h_src_check(rec, asm):
    """C-SRC TRB_H (v1_1), per N against the sha-pinned asm output asm[N] (its header ITEM=n<N> asm, whose program and code sha8 are the
    record's CODE; CHECKS all PASS; its C-TOL line PASS; VERDICT lines exactly ['VERDICT VALID']): per row, N*_<r>_D0..D3 and
    N*_<r>_U3P_1_300 equal, as strings, the balls of the row's U3_P line, every *_LO and *_HI is mid -+ rad exactly, and N*_<r>_R_CERT ..
    N*_<r>_TOL equal the eight values of the row's READING line; N*_ASM_OUTPUT names that output; N*_VERDICT VALID, N*_CHECKS all PASS and
    N*_TOL_RESULT a C-TOL PASS. Returns the failures."""
    bad = []
    for N in (4, 3):
        p = 'N%d_' % N
        lines = asm[N].split('\n')
        pats = dict(checks=r'CHECKS all PASS', tol=r'C-TOL N=%d \(.*\): PASS; .*' % N,
                    head=r'(px08_trbhcert_[a-z0-9_]+) sha256 ([0-9a-f]{64}) ITEM=n%d asm LIM=[0-9]+.*' % N)
        for r in S4H_ROWS:
            pats['u3p ' + r] = S4H_U3P % (N, r)
            pats['reading ' + r] = S4H_READING % (N, r)
        hit = {}
        for k, pat in pats.items():
            ms = [m for m in (re.fullmatch(pat, ln) for ln in lines) if m is not None]
            if len(ms) == 1:
                hit[k] = ms[0]
            else:
                bad.append('%sasm line %s found %d times' % (p, k, len(ms)))
        if not verdict_lines_ok(lines):                                      # T48: exact VERDICT lines
            bad.append('%sasm VERDICT lines not exactly VERDICT VALID' % p)
        for r in S4H_ROWS:
            q = '%s%s_' % (p, r)
            if 'u3p ' + r in hit:
                for i, b in enumerate(S4H_BALLS):
                    if rec.get(q + b) != hit['u3p ' + r].group(i + 1):
                        bad.append(q + b + ' against its U3_P line')
            if 'reading ' + r in hit:
                for i, k in enumerate(S4H_READ):
                    if rec.get(q + k) != hit['reading ' + r].group(i + 1):
                        bad.append(q + k + ' against its READING')
            for b in S4H_BALLS:
                try:
                    mid, rad = s4u_ball(rec.get(q + b))
                    if dec_frac(rec.get(q + b + '_LO')) != mid - rad:
                        bad.append(q + b + '_LO')
                    if dec_frac(rec.get(q + b + '_HI')) != mid + rad:
                        bad.append(q + b + '_HI')
                except ValueError:
                    bad.append(q + b + ' unreadable')
        if rec.get(p + 'ASM_OUTPUT') != '%s:%s' % (S4H_ASM[N][0], S4H_ASM[N][1][:8]):
            bad.append(p + 'ASM_OUTPUT')
        if 'head' in hit and rec.get('CODE') != 'pk08/%s.py:%s' % (hit['head'].group(1), hit['head'].group(2)[:8]):
            bad.append('CODE against the %sasm header' % p)
        if (rec.get(p + 'VERDICT') != 'VALID' or rec.get(p + 'CHECKS') != 'all PASS'
                or not str(rec.get(p + 'TOL_RESULT')).startswith('C-TOL PASS')):
            bad.append(p + 'VERDICT, CHECKS or TOL_RESULT')
    return bad


def s4h_diag_bad(rec):
    """C-DIAG TRB_H, rule (a)'s guard: a trace is at least its diagonal, so each row's t = 0 term N*_<r>_D0_LO must be >= the
    harmonic diagonal S4H_HARM of the bond it is read for (exact decimals). Returns the failures."""
    bad = []
    for (N, r), h in S4H_HARM.items():
        k = 'N%d_%s_D0_LO' % (N, r)
        try:
            if not dec_frac(rec.get(k)) >= dec_frac(h):
                bad.append('N%d row %s: D0_LO %s < %s' % (N, r, rec.get(k), h))
        except ValueError:
            bad.append('N%d row %s: D0_LO unreadable' % (N, r))
    return bad


def s4h_rowswap(rec):
    """PLANT-ROWSWAP's copy: rows T and M exchanged in every N*_<r>_* key of a parsed record."""
    sw, cp = {'_T_': '_M_', '_M_': '_T_'}, {}
    for k, v in rec.items():
        m = re.fullmatch(r'(N[34])(_[TM]_)(.*)', k)
        cp[(m.group(1) + sw[m.group(2)] + m.group(3)) if m else k] = v
    return cp


def mhat_bad(VAC):
    """C-MHAT (rule B-1 rests on m-hat >= 1 for every J >= 300): m-hat(t) = 1 + m1 t + m2 t^2 + m3 t^3 (Ctx.mhat), with m1, m2, m3 the
    numbers of the pinned vacres C-TRIAL returns, each >= 0 by exact comparison (a bool or a non-number fails), so m-hat >= 1 for t >= 0.
    Returns the failures."""
    bad = []
    for N in (4, 3):
        for k in ('m1', 'm2', 'm3'):
            v = VAC[N].get(k)
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not v >= 0:
                bad.append('N=%d %s = %r' % (N, k, v))
    return bad


def bh_bound(rec, K, N, ce):
    """rule (b), B-1..B-3, kind t (row T), J-uniform (B-2): beta_H = max((N-1)/2 - ce_lo, tr x fac), where tr = D0_HI + sum_{k=1..3}
    max(Dk_HI, 0) 300^-k + R_CERT bounds TRB_H(T, t) for every t in (0, 1/300] whatever the cubic's shape, and fac = 1/(1 - delta)^2 >=
    (lambda_h/lambda_0)^2 (B-1 as corrected: lambda_0 lies in m-hat [1 -+ delta], delta = eps_r/sqrt(1 - s^2),
    SPEC_S8_CERT_v1 l.320 and RV13_1 N3; m-hat >= 1 by C-MHAT), eps_r and s by LAW v1 at J = 300 from the M2(b) keys K (their largest
    values: both rise with eps, which falls in J, C-VACMONO). The erratum e48d0812: lambda_0 >= (1 - eps_r) m-hat already holds by
    Lemma 19.2 (c), s entering only the upper side, so 1/(1 - eps_r)^2 would do; this delta form is kept, sound and negligibly looser.
    SH4's validity (B-3): ce_hi <= (N-1)/2 - c_N/300, c_N = 2 + (N-1)(N-3)/8
    (H-BESSEL). Ce = (ce_lo, ce_hi), point intervals. Returns the parts, beta_H (bh, a point interval) and the validity
    flag."""
    q = 'N%d_T_' % N
    tr = dec_iv(rec[q + 'D0_HI']) + dec_iv(rec[q + 'R_CERT'])
    for k in (1, 2, 3):
        if dec_frac(rec[q + 'D%d_HI' % k]) > 0:
            tr = tr + dec_iv(rec[q + 'D%d_HI' % k]) / pt(300) ** k
    V = vac_law_v1(dict(M2B=K), 300.0, {})
    er, sv = pt(V['eps_r'].b), pt(V['s'].b)
    if not ((sv < 1) is True):
        raise ArithmeticError('beta_H: s(300) is not certainly < 1')
    dl = pt((er / iv.sqrt(1 - sv * sv)).b)
    if not ((dl < 1) is True):
        raise ArithmeticError('beta_H: 1 - delta(300) is not certainly > 0')
    fac = 1 / ((1 - dl) * (1 - dl))
    term = pt((tr * fac).b)
    first = pt((pt(N - 1) / 2 - ce[0]).b)
    cN = Fraction(2) + Fraction((N - 1) * (N - 3), 8)
    vmax = pt(N - 1) / 2 - pt(cN.numerator) / pt(cN.denominator) / 300
    return dict(tr=tr, er=er, sv=sv, dl=dl, fac=fac, term=term, first=first, bh=pmax([first, term]), cN=cN, vmax=vmax,
                valid=(ce[1] <= vmax) is True)


def provide_bh(KS, TIN, VAC, fails, fires):
    """the beta_H provider (v1_1), built like provide_s4trb. It reads pk08's TRB_H record once
    (C-HASH on the bytes it parses, with the reference parser and both asm outputs, full sha256), parses it with the port's reader and the
    reference parser, and requires C-FMT (identical keys and values, the keys used present, the header as pinned, T48), C-SRC
    (s4h_src_check), C-DIAG (s4h_diag_bad, rule (a)'s guard) and C-MHAT (mhat_bad); then per N, C-BH (bh_bound), with SH4's validity
    and HZ_PLAN_v1_1 l.461's kill line (beta_H <= 1.5 x its harmonic value) as gates. Plants: PLANT-FMT-TRBH, PLANT-HSRC,
    PLANT-PRECERT-TRBH, PLANT-ROWSWAP, PLANT-MHAT, PLANT-BHVALID. c_e is the t inputs' ce_lo/ce_hi over every grid piece of the N when
    FIELDS names them (pk15's route B), else the harmonic c_t as a FLOAT stand-in. Every piece's bH becomes its N's J-uniform beta_H
    (rule (d): one full-norm bound for both parities and the u-perp case), and TIN['_bh_tag'] reads CERTIFIED only when every check
    passes, every plant fires, c_e comes from the record's ce_lo/ce_hi with the t tag certified and the M2 vacuum tag (eps_r) is
    certified; TAG_PINS['beta_H'] is set then and only then. Returns {N: beta_H}."""
    STB_READS.append('provide_bh')                              # v1_2: C-VERT-ONLY
    with open(os.path.join(CODEDIR, S4H['path']), 'rb') as fh:
        raw = fh.read()
    with open(os.path.join(CODEDIR, S4U_REF[0]), 'rb') as fh:
        refb = fh.read()
    asmb = {}
    for N in (4, 3):
        with open(os.path.join(CODEDIR, S4H_ASM[N][0]), 'rb') as fh:
            asmb[N] = fh.read()
    ok_h = (sha_bytes(raw) == S4H['sha256'], sha_bytes(refb) == S4U_REF[1], all(sha_bytes(asmb[N]) == S4H_ASM[N][1] for N in (4, 3)))
    out('C-HASH TRB_H (full sha256 of the bytes read here): record %s %s, reference parser %s %s, the 2 asm outputs %s -> %s' % (
        S4H['path'], 'matches' if ok_h[0] else 'DIFFERS', S4U_REF[0], 'matches' if ok_h[1] else 'DIFFERS',
        'match' if ok_h[2] else 'DIFFER', 'PASS' if all(ok_h) else 'FAIL'))
    if not all(ok_h):
        fails.append('C-HASH TRB_H')
        raise RuntimeError('beta_H provider: a pinned file differs from its pin; nothing is read from it')
    text = raw.decode('utf-8')
    asm = {N: asmb[N].decode('utf-8') for N in (4, 3)}
    ns = {}
    exec(compile(refb.decode('utf-8'), S4U_REF[0], 'exec'), ns)
    ref_parse = ns['parse_s4u_kv']
    port, ref = s4u_read_port(text), ref_parse(text)
    diff = sorted(k for k in set(port) | set(ref) if port.get(k) != ref.get(k))
    miss = [k for k in S4H_USED if k not in port]
    hdr = [k for k, v in S4H_HEADER.items() if port.get(k) != v]
    prec = marked_precert(port)                                         # T48: a PRECERT or STUB record is refused
    ok_fmt = not diff and not miss and not hdr and not prec
    out('C-FMT TRB_H (format %s): %d keys; the port\'s reader against the reference parser (%s, sha256 %s): %s; the %d keys used present: '
        '%s; header keys %s as pinned: %s; marked PRECERT or STUB (T48): %s -> %s' % (
            S4H['fmt'], len(port), S4U_REF[0], S4U_REF[1][:8], 'identical' if not diff else 'DIFFER on %s' % ', '.join(diff[:6]),
            len(S4H_USED), 'yes' if not miss else 'NO (%s)' % ', '.join(miss[:6]), ', '.join(S4H_HEADER),
            'yes' if not hdr else 'NO (%s)' % ', '.join(hdr), prec, 'PASS' if ok_fmt else 'FAIL'))
    if not ok_fmt:
        fails.append('C-FMT TRB_H')
    src_bad = s4h_src_check(port, asm)
    out('C-SRC TRB_H: per row T, M the balls N*_<r>_D0..D3 and U3P_1_300 against the U3_P lines (and *_LO, *_HI = mid -+ rad exactly), '
        'N*_<r>_R_CERT .. TOL against the READING lines of %s and %s (CHECKS all PASS, C-TOL PASS and VERDICT VALID there, the header\'s '
        'program and code sha8 = the record\'s CODE), N*_ASM_OUTPUT, N*_VERDICT, N*_CHECKS, N*_TOL_RESULT -> %s' % (
            S4H_ASM[4][0], S4H_ASM[3][0], 'PASS' if not src_bad else 'FAIL (%s)' % ', '.join(src_bad[:6])))
    if src_bad:
        fails.append('C-SRC TRB_H')
    dg_bad = s4h_diag_bad(port)
    out('C-DIAG TRB_H (rule (a)\'s guard: a trace is at least its diagonal; row T is the t bond, row M the h bond): %s -> %s' % (
        '; '.join('N=%d row %s D0_LO %s >= %s' % (N, r, port.get('N%d_%s_D0_LO' % (N, r)), h) for (N, r), h in S4H_HARM.items()),
        'PASS' if not dg_bad else 'FAIL (%s)' % ', '.join(dg_bad)))
    if dg_bad:
        fails.append('C-DIAG TRB_H')
    mh_bad = mhat_bad(VAC)
    out('C-MHAT (rule B-1: m-hat >= 1 for t >= 0): m1, m2, m3 of the pinned vacres >= 0 exactly: %s -> %s' % (
        '; '.join('N=%d %s' % (N, ', '.join('%s %r' % (k, VAC[N].get(k)) for k in ('m1', 'm2', 'm3'))) for N in (4, 3)),
        'PASS' if not mh_bad else 'FAIL (%s)' % ', '.join(mh_bad)))
    if mh_bad:
        fails.append('C-MHAT')
    sw = s4u_swap(text, 'N4_T_D0_HI', 'N4_M_D0_HI')
    port_sw = s4u_read_port(sw)
    sw_bad = [b for b in s4h_src_check(port_sw, asm) if b in ('N4_T_D0_HI', 'N4_M_D0_HI')]     # the check must catch it
    fired_f = sw != text and port_sw != ref and bool(sw_bad)
    bumped = s4u_bump(port.get('N4_T_R_CERT', '0'))
    fired_s = bumped != port.get('N4_T_R_CERT') and 'N4_T_R_CERT against its READING' in s4h_src_check(dict(port, N4_T_R_CERT=bumped), asm)
    pr_rec = marked_precert(dict(port, FORMAT=port.get('FORMAT', '') + '-STUB'))           # T48: one plant for this reader
    fired_pr = pr_rec and any('VERDICT' in b for b in s4h_src_check(port, {**asm, 4: precert_copy(asm[4])}))
    fired_rs = bool(s4h_diag_bad(s4h_rowswap(port)))
    fired_mh = any(b.startswith('N=4 m2') for b in mhat_bad({**VAC, 4: dict(VAC[4], m2=-1e-12)}))
    BH, ok_bh, have_ce, fired_v = {}, True, True, True
    for N in (4, 3):
        rows = [t for k, t in TIN.items() if isinstance(k, tuple) and k[0] == N]
        if rows and all('ce' in t for t in rows):
            ce = (pmin([t['ce'][0] for t in rows]), pmax([t['ce'][1] for t in rows]))
            src = 'the t inputs\' ce_lo/ce_hi over %d pieces' % len(rows)
        else:
            hc = pt(N - 1) / 2 - pt(N - 1) * (1 / iv.sqrt(5) + 1 / iv.sqrt(21)) / 4
            ce, src, have_ce = (pt(hc.a), pt(hc.b)), 'FLOAT stand-in: the harmonic c_t (N - 1)/2 - (N - 1)(5^-1/2 + 21^-1/2)/4', False
        B = bh_bound(port, KS[N], N, ce)
        fired_v = fired_v and not bh_bound(port, KS[N], N, (ce[0], pt((B['vmax'] + pt('1e-9')).b)))['valid']
        harm = pt((pt(N - 1) * (1 / iv.sqrt(5) + 1 / iv.sqrt(21)) / 4).b)
        kill = (B['bh'] <= 3 * harm / 2) is True
        old = rows[0]['bH'] if rows else None
        out('C-BH N=%d (kind t = row T, J-uniform): beta_H = max((N-1)/2 - c_e_lo, [D0_HI + sum_k max(Dk_HI, 0) 300^-k + '
            'R_CERT] / (1 - delta)^2) = max(%s, %s x %s) = %s (delta = eps_r/sqrt(1 - s^2) <= %s at J = 300, eps_r <= %s, s <= %s, '
            'LAW v1); SH4 validity c_e_hi %s <= (N-1)/2 - c_N/300 = %s (c_N = %s): %s; KILL l.461 beta_H <= 1.5 x the harmonic %s: %s; '
            'c_e from %s; the FLOAT value it replaces %s -> %s' % (
                N, nf(B['first'], 7), nf(B['tr'], 7), nf(B['fac'], 12), nf(B['bh'], 7), nf(B['dl'], 4), nf(B['er'], 4), nf(B['sv'], 4),
                nf(ce[1], 7), nf(B['vmax'], 7), B['cN'], B['valid'], nf(harm, 5), kill, src, nf(old) if old is not None else 'none',
                'PASS' if (B['valid'] and kill) else 'FAIL'))
        if not (B['valid'] and kill):
            fails.append('C-BH N=%d' % N)
            ok_bh = False
        BH[N] = B['bh']
    plants = (('PLANT-FMT-TRBH', fired_f), ('PLANT-HSRC', fired_s), ('PLANT-PRECERT-TRBH', fired_pr), ('PLANT-ROWSWAP', fired_rs),
              ('PLANT-MHAT', fired_mh), ('PLANT-BHVALID', fired_v))
    out('PLANT-FMT-TRBH (a copy with N4_T_D0_HI and N4_M_D0_HI swapped: the port\'s reading differs from the reference parser\'s and C-SRC '
        'on it fails on %s) %s; PLANT-HSRC (N4_T_R_CERT\'s last digit moved) %s; PLANT-PRECERT-TRBH (T48: FORMAT -STUB, and the N4 asm output '
        'reading VERDICT VALID-PRECERT) %s; PLANT-ROWSWAP (rows T and M exchanged: C-DIAG must fail) %s; PLANT-MHAT (N4 m2 = -1e-12) %s; '
        'PLANT-BHVALID (c_e_hi 1e-9 above the validity bound) %s' % ((', '.join(sw_bad) or 'nothing',) + tuple(
            'FIRES' if f else 'DOES NOT FIRE' for _, f in plants)))
    for nm, f in plants:
        if not f:
            fires.append(nm)
    for k, t in TIN.items():
        if isinstance(k, tuple):
            t['bH'] = BH[k[0]]
    sha8 = sha_bytes(raw)[:8]
    why = [w for w, c in (('c_e is the harmonic FLOAT stand-in', not have_ce), ('the t inputs are not certified',
                                                                                not tag_certified('t inputs', TIN['_tag'])),
                          ('eps_r comes from an M2 vacuum tag that is not certified', not tag_certified('M2 vacuum', TAGS['M2 vacuum'])),
                          ('a check failed or a plant did not fire', not (ok_fmt and not src_bad and not dg_bad and not mh_bad and ok_bh
                                                                          and all(f for _, f in plants)))) if c]
    if not why:
        TAG_PINS['beta_H'] = (S4H['producer'], sha8)
        TIN['_bh_tag'] = 'CERTIFIED %s %s' % TAG_PINS['beta_H']
    else:
        TIN['_bh_tag'] = 'FLOAT (beta_H from TRB_H %s %s: %s)' % (S4H['producer'], sha8, '; '.join(why))
    out('beta_H provider: tag %r (reads certified: %s); every t piece\'s bH set to its N\'s beta_H: N=4 %s, N=3 %s' % (
        TIN['_bh_tag'], tag_certified('beta_H', TIN['_bh_tag']), nf(BH[4], 7), nf(BH[3], 7)))
    return BH


# ------------------------------------------------------------------ P2-11 step 3: the C2-a kinds (NOTE_P2_11_C2A_v1 272ba327)
KINDS = (('flip', (2, 2)), ('same', (2, 2)), ('mixed', (2, 1)))    # (kind, (w_e, w_f)), t on the left; a joint kind (P2-14) would join here
KIND_W = dict(KINDS)
DH_MAX = 6                                                         # end exponents d = 0..DH_MAX (plan sect. 3, step 4)


def kind_hyp(Q, Mq, e, w):
    """P2-11: the monotonicity hypotheses of NOTE_P2_11_C2A_v1 sect. 1, certain comparisons: r2, ro, rho1 < 1 and
    rho1^(w_e+w_f) e^2 < 1, which keep every D denominator positive for every k >= 0."""
    return ((Mq['r2'] < 1) is True and (Mq['ro'] < 1) is True and (Q['rho1'] < 1) is True
            and (Q['rho1'] ** width_exps(w[0], w[1], 0)['D'] * e * e < 1) is True)


def kind_slack(kind, Q, Mq, T, d, sc):
    """P2-11 step 3: the kind's value at k = 0 (units of s_x^0), whose lower end must be > 0 (NOTE_P2_11_C2A_v1 sect. 3; every
    subtracted term is nonincreasing in k, so under kind_hyp the k = 0 check covers every k >= 0):
      flip   F = (A_t - bH e)^2 - 2 bH^2 e^2 - (O_t^1/2 + bH e)^2 - T_(2,2)(0, e);
      same   S = (A_t - bH e)^2 - 2 bH^2 e^2 - T_(2,2)(0, e)                     (r_W^0 = 1);
      mixed  M = (A_t - bH e)(A_a - nBp e) - (pi_t + bH e)(pi_a + nBp e) - (O_t^1/2 + bH e)(v_m + nBm e) - T_(2,1)(0, e),
    with e = R_w rho1^d, p_t = (V_t + O_t)^1/2, pi_a = (v_p^2 - A_a^2)^1/2 and v2_2's vertical v_p, v_m, nBp, nBm. The mixed x part is a
    product of two positive factors: P2-5's bulk sign is for the Ritz amplitudes (X_ta = t~_x a~_x > 0), and the true components
    <e_x, v_t>, <e_x, v_a> carry those signs because A_t = |t~_x| - dt_x > 0 and A_a = |a~_x| - da_x > 0 (T['sign']
    holds all three). T: the t inputs (At, Vt, Ot, Pt, Aa, bH, sign). sc: plant and distance scalings (Rw, bH, At_div, Ot, Aa_div, nB,
    nonx: no P-1 term, w: other widths). Returns the slack interval, or False when kind_hyp or a positive x factor is not certain."""
    w = sc.get('w', KIND_W[kind])
    e = Q['Rw'] * sc.get('Rw', 1.0) * Q['rho1'] ** d
    if not kind_hyp(Q, Mq, e, w):
        return False
    r1 = Q['rho1']
    bH = T['bH'] * sc.get('bH', 1.0)
    Lc = sc.get('corner', 1.0)          # INFO, pk15's width budget: A_t and A_a lowered together, pi_t at the matching dt_x
    At = T['At'] / sc.get('At_div', 1.0) / Lc
    Ot = T['Ot'] * sc.get('Ot', 1.0)
    be = bH * e
    x = At - be
    if (x > 0) is not True:
        return False
    p_t = iv.sqrt(T['Vt'] + Ot)
    p1 = pt(0) if sc.get('nonx') else 2 * be * be
    if kind in ('flip', 'same'):
        _, T22 = tw_mode(r1, e, p_t, bH, p_t, bH, 0, w)
        if T22 is None:
            return False
        if kind == 'flip':
            return x * x - p1 - (iv.sqrt(Ot) + be) ** 2 - T22
        return x * x - p1 - T22
    if kind != 'mixed' or not T['sign']:
        return False
    Aa = T['Aa'] / sc.get('Aa_div', 1.0) / Lc
    nBp, nBm = Q['nBp'] * sc.get('nB', 1.0), Q['nBm'] * sc.get('nB', 1.0)
    y = Aa - nBp * e
    if (y > 0) is not True:
        return False
    pa = iv.sqrt(Q['vp'] ** 2 + Q['vm'] ** 2)
    pia = pt(iv.sqrt(nn(Q['vp'] ** 2 - Aa * Aa, '|v_a+|^2 - A_a^2')).b)
    Pt = T['Pt'] if Lc == 1.0 else pt(iv.sqrt(T['Pt'] ** 2 + 2 * (T['At'] + T['dtx']) * T['At'] * (1 - pt(1) / Lc)).b)
    _, T21 = tw_mode(r1, e, p_t, bH, pa, nBp, 0, w)
    if T21 is None:
        return False
    return x * y - (Pt + be) * (pia + nBp * e) - (iv.sqrt(Ot) + be) * (Q['vm'] + nBm * e) - T21


def kind_holds(kind, Q, Mq, T, d, sc):
    """P2-11: the kind holds at end exponent d (its k = 0 slack certainly > 0)."""
    s = kind_slack(kind, Q, Mq, T, d, sc)
    return s is not False and (s > 0) is True


def kind_profile(kind, Q, Mq, T, sc):
    """P2-11: the kind on one piece for every end exponent: (dmin, slacks). slacks[d] is kind_slack at d = 0..DH_MAX; dmin is the
    smallest d such that the kind holds at every d' in [d, DH_MAX], DH_MAX + 1 if it fails at DH_MAX. The code checks d <= DH_MAX only;
    every larger d follows: each kind's slack is nonincreasing in e = R_w rho1^d (the x parts fall as e grows,
    the subtracted terms rise, and T_w rises, its numerator coefficients being nonnegative over 1 - rho1^D e^2), and kind_hyp and the
    positive x factors only get easier as e falls; so holding at DH_MAX means holding at every d >= DH_MAX."""
    sl = [kind_slack(kind, Q, Mq, T, d, sc) for d in range(DH_MAX + 1)]
    dmin = DH_MAX + 1
    for d in range(DH_MAX, -1, -1):
        if not (sl[d] is not False and (sl[d] > 0) is True):
            break
        dmin = d
    return dmin, sl


def kind_dmin(kind, Q, Mq, T, sc):
    """P2-11: kind_profile's dmin, with the slack at that d (None if there is none)."""
    dmin, sl = kind_profile(kind, Q, Mq, T, sc)
    return dmin, (sl[dmin] if dmin <= DH_MAX else None)


def kind_scale(kind, T):
    """P2-11: the kind's printing scale, A_t^2 (flip, same) or A_t A_a (mixed)."""
    return T['At'] * T['At'] if kind != 'mixed' else T['At'] * T['Aa']


HANDOFF_HR = dict(flip=1.2, same=1.2, mixed=1.05, joint=1.2)   # the hand-off rule: the headroom a claimed threshold needs


def kind_hr_dmin(kind, Q, Mq, T, hr):
    """P2-11, the hand-off rule: the smallest end exponent d in 0..DH_MAX such that at every d' in [d, DH_MAX] the kind holds with each
    of its inputs (C2A_INPUTS) moved against it by the factor hr, one input at a time (every distance to flip >= hr there); DH_MAX + 1
    if there is none. A kind's hand-off threshold at N is its largest value over the pieces (C2a.3, the export's DH_N<N>_<kind>);
    P2-12 covers the pairs below it."""
    dmin = DH_MAX + 1
    for d in range(DH_MAX, -1, -1):
        if not all(kind_holds(kind, Q, Mq, T, d, {key: hr}) for key in C2A_INPUTS[kind]):
            break
        dmin = d
    return dmin


HR_LEVELS = (1.0, 1.05, 1.1, 1.2, 1.5, 2.0)     # the headroom table's levels; 2.0 reads 'at least 2'


def kind_level(kind, Q, Mq, T, d, cap):
    """P2-11, the headroom table: the largest level of HR_LEVELS not above cap at which the kind holds at end exponent d with each of its
    inputs (C2A_INPUTS) moved against it by that level, one input at a time; 1.0 when only the unscaled kind holds (the caller has
    checked that). Descending from cap suffices: the slack is monotone in each input's scale."""
    for lv in sorted((x for x in HR_LEVELS if 1.0 < x <= cap), reverse=True):
        if all(kind_holds(kind, Q, Mq, T, d, {key: lv}) for key in C2A_INPUTS[kind]):
            return lv
    return 1.0


def plan_dh(lev, hr):
    """P2-11: the smallest d such that lev[d'] >= hr at every d' in [d, DH_MAX]; DH_MAX + 1 if there is none. With hr = 1.0 it is the
    claim threshold (the largest of the pieces' own thresholds); with HANDOFF_HR, the planning threshold."""
    dh = DH_MAX + 1
    for d in range(DH_MAX, -1, -1):
        if lev[d] < hr:
            break
        dh = d
    return dh


def c2a_acc():
    """P2-11: a kind's (or joint class's) accumulator over the sweep's pieces."""
    return dict(dmax=-1, at=None, hist={}, worst=[None] * (DH_MAX + 1), worst_abs=[None] * (DH_MAX + 1), lev=[HR_LEVELS[-1]] * (DH_MAX + 1),
                mono=0, rows=[])


def c2a_add(C, dmn, sl, scale, lev_of, Jlo, Jhi):
    """P2-11: one piece into an accumulator: its own threshold dmn; its slacks sl (d = 0..DH_MAX), the worst over the printing scale per
    d; the headroom levels (lev_of(d, cap) at every d where it holds, 0 where it fails; the running minimum over pieces); the count of
    places where the slack's lower end falls from d - 1 to d (the monotonicity rule, INFO); and the export row (dmn, the lower ends)."""
    C['hist'][dmn] = C['hist'].get(dmn, 0) + 1
    if dmn > C['dmax']:
        C['dmax'], C['at'] = dmn, (Jlo, Jhi)
    for d in range(DH_MAX + 1):
        s = sl[d]
        held = s is not False and (s > 0) is True
        if s is not False:
            r = pt(s.a) / scale
            if C['worst'][d] is None or (r < C['worst'][d][0]) is True:
                C['worst'][d] = (r, Jlo, Jhi)
            if C['worst_abs'][d] is None or (s.a < C['worst_abs'][d][0]) is True:
                C['worst_abs'][d] = (s.a, Jlo, Jhi)
            if d > 0 and sl[d - 1] is not False and (s.a < sl[d - 1].a) is True:
                C['mono'] += 1
        C['lev'][d] = min(C['lev'][d], lev_of(d, C['lev'][d]) if held else 0.0)
    C['rows'].append((dmn, [None if s is False else s.a for s in sl]))


PLANT_KIND0_EDIT = ('            return x * x - p1 - (iv.sqrt(Ot) + be) ** 2 - T22\n', '            return x * x - p1 - T22\n')
C2A_DIST = (('A_t (divided by)', 'At_div'), ('O_t (times)', 'Ot'), ('beta_H (times)', 'bH'), ('R_w (times)', 'Rw'),
            ('A_a (divided by)', 'Aa_div'))
C2A_INPUTS = dict(flip=('At_div', 'Ot', 'bH', 'Rw'), same=('At_div', 'bH', 'Rw'), mixed=('At_div', 'Ot', 'bH', 'Rw', 'Aa_div'))
C2A_MPLANT = dict(flip=('At_div', 'Ot', 'bH'), same=('At_div', 'bH'), mixed=('At_div', 'Ot', 'bH', 'Aa_div'))


def kind0_bad(fn, Q, Mq, T):
    """P2-11 C-KIND0 on one piece: with e = 0 (R_w scaled to 0) the kinds computed by fn (kind_slack or a planted copy) must equal their
    bulk forms written out here, flip A_t^2 - O_t, same A_t^2, mixed A_t A_a - pi_t pi_a - O_t^1/2 v_m (C7's and C5_RESCUE + C6's
    k = 0 forms): enclosures that overlap, each narrower than 1e-12 of the kind's scale. Returns the kinds that differ."""
    pia = pt(iv.sqrt(nn(Q['vp'] ** 2 - T['Aa'] * T['Aa'], '|v_a+|^2 - A_a^2')).b)
    want = dict(flip=T['At'] * T['At'] - T['Ot'], same=T['At'] * T['At'],
                mixed=T['At'] * T['Aa'] - T['Pt'] * pia - iv.sqrt(T['Ot']) * Q['vm'])
    bad = []
    for kind, _ in KINDS:
        g, wv, sc_ = fn(kind, Q, Mq, T, 0, {'Rw': 0.0}), want[kind], kind_scale(kind, T) * pt(1) / 10 ** 12
        if not (g is not False and (g.a <= wv.b) is True and (wv.a <= g.b) is True and (g.b - g.a < sc_) is True
                and (wv.b - wv.a < sc_) is True):
            bad.append(kind)
    return bad


def c2a_controls(Q, Mq, T, N, fails, fires):
    """P2-11 step 3 controls on the scan piece: C-KIND0 with PLANT-KIND0 (a copy of kind_slack without the flip's odd term, from
    PLANT_KIND0_EDIT, must fail it), C-MIRROR (T_(1,2) with the sides swapped equals T_(2,1), endpoint for endpoint, d = 0..DH_MAX) with
    PLANT-MIRROR (T_(1,2) with the sides unswapped must differ), and C-FLIP (INFO until a record carries X_tb)."""
    bad = kind0_bad(kind_slack, Q, Mq, T)
    out('C-KIND0 N=%d (P2-11): at e = 0 the kinds equal their bulk forms (flip A_t^2 - O_t, same A_t^2, mixed A_t A_a - pi_t pi_a - '
        'O_t^1/2 v_m) -> %s' % (N, 'PASS' if not bad else 'FAIL (%s)' % ', '.join(bad)))
    if bad:
        fails.append('C-KIND0 N=%d' % N)
    src = inspect.getsource(kind_slack)
    if src.count(PLANT_KIND0_EDIT[0]) != 1:
        raise RuntimeError('PLANT-KIND0: source edit not found exactly once')
    ns = dict(iv=iv, pt=pt, nn=nn, tw_mode=tw_mode, kind_hyp=kind_hyp, KIND_W=KIND_W)
    exec(compile(src.replace(PLANT_KIND0_EDIT[0], PLANT_KIND0_EDIT[1]), 'PLANT-KIND0 copy', 'exec'), ns)
    pb = kind0_bad(ns['kind_slack'], Q, Mq, T)
    out('PLANT-KIND0 N=%d (a copy of kind_slack without the flip\'s odd term): C-KIND0 flags %s -> %s' % (
        N, ', '.join(pb) or 'nothing', 'FIRES' if 'flip' in pb else 'DOES NOT FIRE'))
    if 'flip' not in pb:
        fires.append('PLANT-KIND0 N=%d' % N)
    p_t, pa = iv.sqrt(T['Vt'] + T['Ot']), iv.sqrt(Q['vp'] ** 2 + Q['vm'] ** 2)
    mb, md = [], 0
    for d in range(DH_MAX + 1):
        e = Q['Rw'] * Q['rho1'] ** d
        t21 = tw_mode(Q['rho1'], e, p_t, T['bH'], pa, Q['nBp'], 0, (2, 1))[1]
        t12 = tw_mode(Q['rho1'], e, pa, Q['nBp'], p_t, T['bH'], 0, (1, 2))[1]
        t12u = tw_mode(Q['rho1'], e, p_t, T['bH'], pa, Q['nBp'], 0, (1, 2))[1]
        if not same_value(t21 if t21 is not None else False, t12 if t12 is not None else False):
            mb.append('d=%d' % d)
        if not same_value(t21 if t21 is not None else False, t12u if t12u is not None else False):
            md += 1
    out('C-MIRROR N=%d (P2-11): T_(1,2) with the sides swapped against T_(2,1), d = 0..%d, endpoint for endpoint: %s -> %s; PLANT-MIRROR '
        '(T_(1,2) with the sides unswapped) differs at %d of %d -> %s' % (
            N, DH_MAX, 'identical' if not mb else 'differs at %s' % ', '.join(mb), 'PASS' if not mb else 'FAIL', md, DH_MAX + 1,
            'FIRES' if md else 'DOES NOT FIRE'))
    if mb:
        fails.append('C-MIRROR N=%d' % N)
    if not md:
        fires.append('PLANT-MIRROR N=%d' % N)
    out('INFO C-FLIP N=%d (P2-11): the FLOAT stand-ins carry X_ta only; (t, b) and the flip images (bb, b), (bb, a), (bb, bb\') take t\'s '
        'and a\'s norms by the flip (v_bb = F v_t, B_bb = F B_t F; b_x = a_x), NOTE_P2_11_C2A_v1 sect. 3; the gate X_tb = X_ta starts with '
        'the assembly record' % N)


def c2a_scan(INP, SH1, TIN, fails, fires):
    """P2-11 step 3, the float scan at [300, 303] (plan sect. 3, step 4): per N and kind the threshold d^h (kind_dmin), the slacks at d^h
    and below it, the distances to flip at d^h (flip_search on the kind's inputs), the controls (c2a_controls), and the plants:
    PLANT-NONX (P-1's term dropped: the beta_H distance at d = 1 or d^h must move by more than 1%, flip or same), PLANT-W (w = (1, 1)
    powers for t: some slack at d = 1..3 certainly lower, none certainly higher), PLANT-BH (beta_H x 3 must raise a threshold),
    PLANT-PAIR (h in place of t must fail flip and same at their thresholds) and the margin plants (hold at F / 1.1, lost at 1.1 F).
    The C2-a kill: a kind with no d^h <= DH_MAX is reported and stops."""
    J3, J3h = 300.0, 303.0
    STAGE[0] = 'C2-a scan [300, 303]'
    th, nonx, wl, wh, bhup, pair, ho = {}, [], [], [], [], {}, {}
    idx = [i for i, (jlo, _) in enumerate(joint_grid()) if float(jlo) < J3h]        # the grid pieces meeting [300, 303] (an index choice)
    for N in (4, 3):
        T = t_scan_inputs(TIN, SH1, N, idx)
        E = piece_eval(INP[N], J3, J3h, {})
        Q, Mq = E['Q'], E['Mq']
        c2a_controls(Q, Mq, T, N, fails, fires)
        for kind, w in KINDS:
            budget(4.0, 'C2-a scan N=%d %s' % (N, kind))
            dh, sl = kind_profile(kind, Q, Mq, T, {})
            th[(N, kind)] = dh
            scl = kind_scale(kind, T)
            rows = ['d=%d %s' % (d, 'n/a' if sl[d] is False else '%+.4g' % fnum(pt(sl[d].a) / scl)) for d in range(DH_MAX + 1)]
            dist = {}
            if dh <= DH_MAX:
                for lab, key in C2A_DIST:
                    if key in C2A_INPUTS[kind]:
                        dist[key] = flip_search(lambda x: kind_holds(kind, Q, Mq, T, dh, {key: x}), 'mul', MCAP)
            out('C2-a SCAN N=%d %s (w = (%d, %d)), [300, 303]: d^h = %s; slack / %s by d: %s; distances to flip at d^h: %s' % (
                N, kind, w[0], w[1], dh if dh <= DH_MAX else 'none <= %d' % DH_MAX, 'A_t^2' if kind != 'mixed' else 'A_t A_a',
                ', '.join(rows), '; '.join('%s %s' % (lab, fmt_f(dist[key])) for lab, key in C2A_DIST if key in dist) or 'n/a'))
            for key in (C2A_MPLANT[kind] if dh <= DH_MAX else ()):
                F = dist.get(key)
                fired = bool(F) and kind_holds(kind, Q, Mq, T, dh, {key: F / 1.1}) and not kind_holds(kind, Q, Mq, T, dh, {key: F * 1.1})
                out('PLANT-C2A-%s N=%d %s (d^h = %d): flip F = %s; holds at F / 1.1 and is lost at 1.1 F -> %s' % (
                    key, N, kind, dh, fmt_f(F), 'FIRES' if fired else 'DOES NOT FIRE'))
                if not fired:
                    fires.append('PLANT-C2A-%s N=%d %s' % (key, N, kind))
            hrd = {}                                                   # the hand-off rule: the headroom by d and the threshold
            for d in range(min(dh, DH_MAX + 1), DH_MAX + 1):
                ds = [v for v in (flip_search(lambda x: kind_holds(kind, Q, Mq, T, d, {key: x}), 'mul', MCAP)
                                  for key in C2A_INPUTS[kind]) if v is not None]
                hrd[d] = min(ds) if ds else None
            ho[(N, kind)] = kind_hr_dmin(kind, Q, Mq, T, HANDOFF_HR[kind])
            out('C2-a HEADROOM N=%d %s ([300, 303]): smallest distance to flip over %s, by d: %s; hand-off threshold at HR %.2f: %s' % (
                N, kind, ', '.join(lab for lab, key in C2A_DIST if key in C2A_INPUTS[kind]),
                ', '.join('d=%d %s' % (d, fmt_f(v)) for d, v in sorted(hrd.items())) or 'n/a', HANDOFF_HR[kind],
                ho[(N, kind)] if ho[(N, kind)] <= DH_MAX else 'none <= %d' % DH_MAX))
            if kind == 'mixed' and 'dtx' in T and dh <= DH_MAX:            # INFO, pk15's width budget: M at the joint corner
                cor = {d: flip_search(lambda x: kind_holds(kind, Q, Mq, T, d, {'corner': x}), 'mul', MCAP)
                       for d in sorted({dh, min(dh + 1, DH_MAX)})}
                out('INFO C2-a CORNER N=%d mixed ([300, 303]; pk15\'s width budget): A_t and A_a divided together by L, pi_a = (v_p^2 - '
                    'A_a^2)^1/2 recomputed and pi_t^2 raised by 2 (A_t + dt_x) A_t (1 - 1/L), the dt_x that lowers A_t (|t~_x| as At_lo + '
                    'dtx_hi): M flips at L = %s; one input at a time at d^h: A_t %s (pi_t fixed), A_a %s' % (
                        N, ', '.join('%s at d = %d' % (fmt_f(v), d) for d, v in sorted(cor.items())),
                        fmt_f(dist.get('At_div')), fmt_f(dist.get('Aa_div'))))
            if kind in ('flip', 'same'):
                for d in sorted({1, dh} & set(range(DH_MAX + 1))):
                    f1 = flip_search(lambda x: kind_holds(kind, Q, Mq, T, d, {'bH': x}), 'mul', MCAP)
                    f0 = flip_search(lambda x: kind_holds(kind, Q, Mq, T, d, {'bH': x, 'nonx': True}), 'mul', MCAP)
                    moved = (f1 is None) != (f0 is None) or (f1 is not None and (f1 == 0.0) != (f0 == 0.0)) or (
                        f1 and f0 and abs(f0 / f1 - 1) > 0.01)
                    nonx.append((N, kind, d, f1, f0, moved))
            for d in range(1, 4):
                s2, s1 = sl[d], kind_slack(kind, Q, Mq, T, d, {'w': (1, 1)})
                if s2 is not False and s1 is not False:
                    if (s1.b < s2.a) is True:
                        wl.append('N%d %s d=%d' % (N, kind, d))
                    if (s1.a > s2.b) is True:
                        wh.append('N%d %s d=%d' % (N, kind, d))
            d3, _ = kind_profile(kind, Q, Mq, T, {'bH': 3.0})
            if d3 > dh:
                bhup.append('N%d %s %d -> %s' % (N, kind, dh, d3 if d3 <= DH_MAX else 'none'))
        Th = dict(T, At=T['Ah'])
        pair[N] = all(not kind_holds(k, Q, Mq, Th, min(th[(N, k)], DH_MAX), {}) for k in ('flip', 'same'))
    tin_tag = TIN['_tag'] if TIN is not None else SH1['tag']
    out('C2-a SCAN THRESHOLDS ([300, 303], t inputs %s): %s' % (tin_tag, '; '.join(
        'N=%d %s' % (N, ', '.join('%s %s' % (k, th[(N, k)] if th[(N, k)] <= DH_MAX else 'none') for k, _ in KINDS)) for N in (4, 3))))
    out('C2-a HAND-OFF THRESHOLDS ([300, 303], t inputs as above, HANDOFF_HR %s; the sweep\'s C2a.3 sets the claim over every piece): %s' % (
        ', '.join('%s %.2f' % (k, HANDOFF_HR[k]) for k, _ in KINDS), '; '.join(
            'N=%d %s' % (N, ', '.join('%s %s' % (k, ho[(N, k)] if ho[(N, k)] <= DH_MAX else 'none') for k, _ in KINDS)) for N in (4, 3))))
    fn_ = any(r[5] for r in nonx)
    out('PLANT-NONX (P2-11: P-1\'s term dropped): beta_H distances %s -> %s' % ('; '.join(
        'N%d %s d=%d %s -> %s%s' % (N, k, d, fmt_f(f1), fmt_f(f0), ' (moved)' if mv else '') for N, k, d, f1, f0, mv in nonx),
        'FIRES' if fn_ else 'DOES NOT FIRE'))
    if not fn_:
        fires.append('PLANT-NONX')
    fw = bool(wl) and not wh
    out('PLANT-W (P2-11: w = (1, 1) powers for t): slack certainly lower at %s; certainly higher at %s -> %s' % (
        ', '.join(wl) or 'nowhere', ', '.join(wh) or 'nowhere', 'FIRES' if fw else 'DOES NOT FIRE'))
    if not fw:
        fires.append('PLANT-W')
    out('PLANT-BH (P2-11: beta_H x 3): thresholds raised at %s -> %s' % (', '.join(bhup) or 'nowhere', 'FIRES' if bhup else 'DOES NOT FIRE'))
    if not bhup:
        fires.append('PLANT-BH')
    fp = all(pair.values())
    out('PLANT-PAIR (P2-11: h in place of t, A_h = (|h_x| - dh_x) x 0.98): flip and same fail at their thresholds: N=4 %s, N=3 %s -> %s' % (
        pair[4], pair[3], 'FIRES' if fp else 'DOES NOT FIRE'))
    if not fp:
        fires.append('PLANT-PAIR')
    for kind, _ in KINDS:
        dead = [N for N in (4, 3) if th[(N, kind)] > DH_MAX]
        out('KILL C2-a %s (HZ_PLAN_v1_1 sect. 5: a threshold d^h <= %d at [300, 303] at both N): %s' % (
            kind, DH_MAX, 'PASS' if not dead else 'KILL at N=%s: reported, the kind stops' % ', '.join(str(N) for N in dead)))
    return th


# ------------------------------------------------------------------ P2-14: the fourth kind, one joint insertion (NOTE_P2_11_C2A_v1_1 sect. 2)
JOINT_CLASSES = (('D3', 3), ('D4', 2), ('D4M', 2))   # (class, w_X): D3 (t_i, bb_i+-1), D4 (t_i, b_i), D4M (t_i, b_i+1); flip images by symmetry
JOINT_W = dict(JOINT_CLASSES)
JOINT_FIELDS = 'jlo jhi Cov_inf_lo pX_hi normX_hi E2_hi'
JOINT_INPUTS = ('C_div', 'pX', 'normX', 'bH', 'Rw')       # the joint kind's scalings, each against it at values > 1
JOINT_RECS = dict(float=dict(path='pk15/out/export_p2_14_joint_float_v1_2.kv',     # pk15's FLOAT joint record (kt_p2_14f_v1
                             sha256='39d08be920a031ac33aeab936f63aa743611578e94e342e83b72a030abcbfc3e',   # aefc981e; v1_2: D4M keys)
                             out=('pk15/out/export_p2_14_joint_float_v1_2.out',
                                  '3933571972dfb01c4d895428a88a34b7261f2f222b2426401247600f251c5069'),
                             fmt='S4U_KV_v1', status='FLOAT', record='EXPORT_P2_14_JOINT_v1', producer='pk15'),
                  mock=dict(path='pk15/mocks/out/export_p2_14_joint_mock_kt_p2_assembly_v1_11.kv',    # kt_p2_assembly_v1_11 f5352655,
                            sha256='0b813460a11199d6c52db0b23677e784f5bac264033b5c5ef88f3fd375ba4b3a',    # its MOCK run: pX_hi rounded up,
                            out=('pk15/mocks/out/out_kt_p2_assembly_v1_11_mock.out',                   # route (A)'s Lemma E on E2,
                                 '146733c4cd7fe7fb6e7709ab9325d765e5aa1d6100018835263344d292487b44'),      # Lemma S' normX, MOCK P2-8 Cov
                            fmt='S4U_KV_v1 MOCK', status='MOCK', record='EXPORT_P2_14_JOINT_v1', producer='pk15'),
                  certified=None)     # the same keys, fmt 'S4U_KV_v1' and status 'CERTIFIED', once pk15's certified assembly run is frozen
JOINT_MODE = 'mock'       # pk15's v1_8 MOCK export rounds pX_hi up (its v1_3/v1_5 exports failed the exact C-SRC-J at 1467 of 5424
JOINT_REC = JOINT_RECS[JOINT_MODE]                  # rows, m3's scan); 'float' is the FLOAT kt_p2_14f_v1 record with its 1e-6 margin
JOINT_TAG_PIN = None      # ('pk15', the record's sha8) for TAG_PINS['joint inputs'] once JOINT_RECS['certified'] is filled


def joint_slack(cls, Q, T, J, d, sc):
    """P2-14, the fourth kind (NOTE_P2_11_C2A_v1_1 sect. 2): the pair as one joint centred insertion X_c on its window of w_X columns, the
    members t (p_t, beta_H) and b (v2_2's p_a, nBp; D4, D4M) or bb (p_t, beta_H; D3), the window's end states u + eps with
    |eps| <= e = R_w rho1^d (d from the window's outer columns):
      Cov D >= Cov_inf_lo - 2 e pX - e^2 normX - (2 e p1 + e^2 B1)(2 e p2 + e^2 B2)/(1 - rho1^w_X e^2),  D >= 1 - rho1^w_X e^2 > 0.
    J: the piece's inputs (Cov, pX, normX). sc: scalings (C_div, pX, normX, bH, Rw, nB; nofirst: the first-order term dropped,
    PLANT-JOINT). Returns the slack interval, whose lower end must be > 0, or False unless rho1 < 1 and rho1^w_X e^2 < 1 certainly.
    The centring is the exact bulk means: <u, B'u> = 0 and <u, X_c u> = Cov_inf need it, and with other
    constants (mu_e mu_f eta - mu_e delta_2 - mu_f delta_1)/D would enter. So E2_hi, normX_hi and the members' B (beta_H, nB_p) are
    certified at that centring, uniformly over the means' certified intervals (a certified record's CENTRING = CERTIFIED_BALLS). The
    members' p do not depend on it; p_X does: its bound pX_hi^2 >= E2_hi - Cov_inf_lo^2 inherits the centring
    through E_bulk[X_c^2], so pX_hi is certified over the same balls (pk15: with the smallest |Cov| over the ball)."""
    wX = JOINT_W[cls]
    e = Q['Rw'] * sc.get('Rw', 1.0) * Q['rho1'] ** d
    Dm1 = Q['rho1'] ** wX * e * e
    if (Q['rho1'] < 1) is not True or (Dm1 < 1) is not True:
        return False
    bH = T['bH'] * sc.get('bH', 1.0)
    p1 = iv.sqrt(T['Vt'] + T['Ot'])
    if cls == 'D3':
        p2, B2 = p1, bH
    else:
        p2, B2 = iv.sqrt(Q['vp'] ** 2 + Q['vm'] ** 2), Q['nBp'] * sc.get('nB', 1.0)
    first = pt(0) if sc.get('nofirst') else 2 * e * J['pX'] * sc.get('pX', 1.0)
    return (J['Cov'] / sc.get('C_div', 1.0) - first - e * e * J['normX'] * sc.get('normX', 1.0)
            - (2 * e * p1 + e * e * bH) * (2 * e * p2 + e * e * B2) / (1 - Dm1))


def joint_holds(cls, Q, T, J, d, sc):
    """P2-14: the joint kind holds at end exponent d (its slack certainly > 0)."""
    s = joint_slack(cls, Q, T, J, d, sc)
    return s is not False and (s > 0) is True


def joint_profile(cls, Q, T, J, sc):
    """P2-14: (dmin, slacks) as kind_profile: dmin is the smallest d in 0..DH_MAX such that the joint kind holds at every d' in [d, DH_MAX],
    DH_MAX + 1 if it fails at DH_MAX. Larger d follow as in kind_profile: the joint slack is nonincreasing in e (every subtracted term
    is a polynomial in e with nonnegative coefficients over 1 - rho1^w_X e^2), and its hypotheses only get easier as e falls."""
    sl = [joint_slack(cls, Q, T, J, d, sc) for d in range(DH_MAX + 1)]
    dmin = DH_MAX + 1
    for d in range(DH_MAX, -1, -1):
        if not (sl[d] is not False and (sl[d] > 0) is True):
            break
        dmin = d
    return dmin, sl


def joint_hr_dmin(cls, Q, T, J, hr):
    """P2-14, the hand-off rule as kind_hr_dmin: the smallest d such that at every d' in [d, DH_MAX] the joint kind holds with each of
    JOINT_INPUTS moved against it by hr, one at a time; DH_MAX + 1 if there is none."""
    dmin = DH_MAX + 1
    for d in range(DH_MAX, -1, -1):
        if not all(joint_holds(cls, Q, T, J, d, {key: hr}) for key in JOINT_INPUTS):
            break
        dmin = d
    return dmin


def joint_level(cls, Q, T, J, d, cap):
    """P2-14: kind_level for the joint kind, its inputs JOINT_INPUTS."""
    for lv in sorted((x for x in HR_LEVELS if 1.0 < x <= cap), reverse=True):
        if all(joint_holds(cls, Q, T, J, d, {key: lv}) for key in JOINT_INPUTS):
            return lv
    return 1.0


def joint_grid():
    """P2-14: the piece grid as strings, [(jlo, jhi)] in piece order, from v2_2's pinned export (V22_EXPORT, full sha256 of the bytes read):
    fields 1 and 2 of its N4 piece rows (the grid is the same for both N)."""
    with open(os.path.join(CODEDIR, V22_EXPORT[0]), 'rb') as fh:
        raw = fh.read()
    if sha_bytes(raw) != V22_EXPORT[1]:
        raise RuntimeError('P2-14: v2_2\'s export differs from its pin')
    rec = s4u_read_port(raw.decode('utf-8'))
    n = int(rec['N4_PIECES'])
    return [tuple(rec['N4_P%04d' % i].split(' ')[:2]) for i in range(n)]


JOINT_CERT_REQUIRE = dict(VACUUM_CORRECTION='S3_LEMMA_E', CENTRING='LEMMA_E_MEAN_BALLS', NORMX_BOUND='OPERATOR_BOX_PLUS_SCHUR_TAIL')
#                         route (A) (the rule on NOTE_P2_14_S3_v1): kt_p2_assembly_v1_8's names for the points 2-4, the
#                         exact certified strings (pk15 confirmed, 2026-11-07); no other header key of the record is read by value
T_CERT_REQUIRE = dict(VT_FORM='GRAM_PLUS_Q4', PT_FORM='JOINT_GRAM')


def float_in_empty(v):
    """the status rule for pk15's exports: a CERTIFIED record carries FLOAT_IN = none, exactly (pk15's empty form, what its
    export_status writes for all-empty lists; an allow-list). Anything else, an absent FLOAT_IN included, is not empty: such
    a record reads CERTIFIED_GIVEN_FLOAT_IN with '<record>: <tokens>' entries and is refused as certified."""
    return v == 'none'
# the certified inputs' points as reader requirements: a CERTIFIED joint record states that E2_hi and Cov_inf_lo
# carry S3's vacuum correction (2), that every input depending on the centrings c_e, c_f holds over the certified balls of the bulk means
# (3), and that normX_hi is an operator-norm bound, the box part sup|f| <= Lam Lam' by positivity and the tail by an operator bound such
# as Schur (4); a CERTIFIED t record (kt_p2_assembly) states V_t = c^T G^-1 c + |Q4 v_t|^2_hi with the complement (1) and pi_t in the
# joint Gram-corrected form with its t~0^2 content, and carries Xtb_lo, so that C-FLIP (X_tb = X_ta) gates
#. FLOAT records are not held to them.


def joint_read(rec, grid):
    """P2-14: the joint inputs from a parsed record: ({(cls, N, i): dict(Cov, pX, normX, E2)}, problems). C-GRID: every row present with
    jlo, jhi string for string as the grid; C-SRC-J: pX_hi^2 >= E2_hi - Cov_inf_lo^2 where Cov_inf_lo > 0 (certain comparisons on exact
    decimals); the header's FIELDS, CLASSES, WX_* and RUN_VERDICT = VALID (T48 for KV records) as agreed; PRECERT or STUB refused; a
    record whose TAG reads CERTIFIED must carry JOINT_CERT_REQUIRE's keys and values."""
    bad, J = [], {}
    want = dict(FIELDS=JOINT_FIELDS, CLASSES=' '.join(c for c, _ in JOINT_CLASSES), RUN_VERDICT='VALID',
                **{'WX_%s' % c: str(w) for c, w in JOINT_CLASSES})
    bad += ['header %s' % k for k, v in want.items() if rec.get(k) != v]
    if marked_precert(rec) or 'PRECERT' in rec.get('TAG', '').upper() or 'STUB' in rec.get('TAG', '').upper():
        bad.append('marked PRECERT or STUB')
    if rec.get('EXPORT_STATUS') == 'CERTIFIED' or rec.get('TAG', '').startswith('CERTIFIED'):
        bad += ['certified requirement %s' % k for k, v in JOINT_CERT_REQUIRE.items() if rec.get(k) != v]
        if not float_in_empty(rec.get('FLOAT_IN')):                       # the rule: no FLOAT input under a CERTIFIED status
            bad.append('certified requirement FLOAT_IN empty')
    for cls, _ in JOINT_CLASSES:
        for N in (4, 3):
            if rec.get('N%d_%s_PIECES' % (N, cls)) != str(len(grid)):
                bad.append('N%d_%s_PIECES' % (N, cls))
            for i, (jlo, jhi) in enumerate(grid):
                v = rec.get('N%d_%s_P%04d' % (N, cls, i), '').split(' ')
                if len(v) != 6 or v[0] != jlo or v[1] != jhi:
                    bad.append('C-GRID N%d_%s_P%04d' % (N, cls, i))
                    continue
                cov, px, nx, e2 = dec_iv(v[2]), dec_iv(v[3]), dec_iv(v[4]), dec_iv(v[5])
                if (cov > 0) is not True:                                   # the C-S check needs Cov_inf_lo > 0
                    bad.append('C-SRC-J Cov_inf_lo not > 0 N%d_%s_P%04d' % (N, cls, i))
                elif (px * px >= e2 - cov * cov) is not True:
                    bad.append('C-SRC-J N%d_%s_P%04d' % (N, cls, i))
                J[(cls, N, i)] = dict(Cov=pt(cov.a), pX=pt(px.b), normX=pt(nx.b), E2=pt(e2.b))
    return J, bad


def provide_joint(fails, fires):
    """P2-14, the joint inputs' provider (pk15's record, NOTE_P2_11_C2A_v1_1 sect. 2): C-HASH (the record, its producing run's output
    and the reference parser, full sha256), C-FMT (the port's reader against s4u_kv_ref_v1), C-SRC (the producing output's VERDICT lines
    exactly ['VERDICT VALID'] and the record's full sha256 printed there), and joint_read's C-GRID, C-SRC-J and header checks; plants
    PLANT-FMT-J (two rows' values swapped), PLANT-SRC-J (one pX_hi halved) and PLANT-PRECERT-J (RECORD marked PRECERT). Returns the
    inputs, or None while no record is pinned (JOINT_REC)."""
    STB_READS.append('provide_joint')                           # v1_2: C-VERT-ONLY
    if JOINT_REC is None:
        out('INFO P2-14 joint kind: no input record pinned yet (pk15\'s FLOAT set from kt_p2_14f_v1); the fourth kind is not evaluated')
        return None
    with open(os.path.join(CODEDIR, JOINT_REC['path']), 'rb') as fh:
        raw = fh.read()
    with open(os.path.join(CODEDIR, JOINT_REC['out'][0]), 'rb') as fh:
        rawo = fh.read()
    with open(os.path.join(CODEDIR, S4U_REF[0]), 'rb') as fh:
        refb = fh.read()
    ok_h = (sha_bytes(raw) == JOINT_REC['sha256'] and sha_bytes(rawo) == JOINT_REC['out'][1] and sha_bytes(refb) == S4U_REF[1])
    out('C-HASH JOINT (P2-14, full sha256 of the bytes read here): record %s, producing output %s, reference parser %s -> %s' % (
        JOINT_REC['path'], JOINT_REC['out'][0], S4U_REF[0], 'PASS' if ok_h else 'FAIL'))
    if not ok_h:
        fails.append('C-HASH JOINT')
        raise RuntimeError('P2-14 provider: a pinned file differs from its pin; nothing is read from it')
    text, texto = raw.decode('utf-8'), rawo.decode('utf-8')
    ns = {}
    exec(compile(refb.decode('utf-8'), S4U_REF[0], 'exec'), ns)
    port, ref = s4u_read_port(text), ns['parse_s4u_kv'](text)
    ok_f = (port == ref and port.get('FORMAT') == JOINT_REC['fmt'] and port.get('RECORD') == JOINT_REC['record']
            and port.get('END') == JOINT_REC['record'] and port.get('EXPORT_STATUS') == JOINT_REC['status'])
    ok_s = bound_ok(os.path.basename(JOINT_REC['path']), JOINT_REC['sha256'], texto)
    out('C-FMT JOINT (%s mode): %d keys; the port\'s reader against the reference parser: %s; FORMAT, RECORD, END and EXPORT_STATUS as '
        'pinned (%s, %s): %s; C-SRC JOINT (rule V2, bound_ok): the producing output\'s VERDICT lines exactly [\'VERDICT VALID\'] and one '
        'EXPORT line naming the record with its sha256: %s -> %s' % (
            JOINT_MODE, len(port), 'identical' if port == ref else 'DIFFER', JOINT_REC['fmt'], JOINT_REC['status'], ok_f, ok_s,
            'PASS' if (ok_f and ok_s) else 'FAIL'))
    if not (ok_f and ok_s):
        fails.append('C-FMT/C-SRC JOINT')
    grid = joint_grid()
    J, bad = joint_read(port, grid)
    out('C-GRID, C-SRC-J (P2-14): %d rows on the grid of %d pieces x %d classes x 2 N, jlo and jhi string for string; pX_hi^2 >= E2_hi - '
        'Cov_inf_lo^2; header as agreed; not PRECERT or STUB -> %s' % (len(J), len(grid), len(JOINT_CLASSES),
                                                                     'PASS' if not bad else 'FAIL (%s)' % ', '.join(bad[:6])))
    if bad:
        fails.append('C-GRID/C-SRC-J')
    k0, k1 = 'N4_D3_P0000', 'N4_D3_P0001'
    sw = dict(port, **{k0: port.get(k1, ''), k1: port.get(k0, '')})
    pf = bool(joint_read(sw, grid)[1])
    v = port.get(k0, '').split(' ')
    halved = dict(port, **{k0: ' '.join(v[:3] + [dec_half(v[3])] + v[4:])}) if len(v) == 6 else port   # exact, from strings
    ps = any(b.startswith('C-SRC-J N') for b in joint_read(halved, grid)[1])
    negc = dict(port, **{k0: ' '.join(v[:2] + ['-' + v[2]] + v[3:])}) if len(v) == 6 else port
    pn = any(b.startswith('C-SRC-J Cov_inf_lo not > 0 N4_D3_P0000') for b in joint_read(negc, grid)[1])
    pp = 'marked PRECERT or STUB' in joint_read(dict(port, RECORD=port.get('RECORD', '') + '_PRECERT'), grid)[1]
    stripped = {k: v for k, v in port.items() if k not in JOINT_CERT_REQUIRE}
    pc = any(b.startswith('certified requirement') for b in joint_read(dict(stripped, TAG='CERTIFIED %s 00000000' % JOINT_REC['producer']),
                                                                         grid)[1])
    out('INFO P2-14 certified-record requirements (%s): this record\'s TAG is %r, so they are %s; present: '
        '%s' % (', '.join('%s = %s' % kv for kv in JOINT_CERT_REQUIRE.items()), port.get('TAG'),
                'required' if port.get('TAG', '').startswith('CERTIFIED') else 'not yet required (FLOAT)',
                ', '.join(k for k in JOINT_CERT_REQUIRE if k in port) or 'none'))
    fi = port.get('FLOAT_IN') if not float_in_empty(port.get('FLOAT_IN')) else 'planted: far'
    pfi = 'certified requirement FLOAT_IN empty' in joint_read(
        dict(port, EXPORT_STATUS='CERTIFIED', TAG='CERTIFIED %s 00000000' % JOINT_REC['producer'], FLOAT_IN=fi, **JOINT_CERT_REQUIRE), grid)[1]
    out('PLANT-FMT-J (two rows\' values swapped) %s; PLANT-SRC-J (N4_D3_P0000\'s pX_hi halved) %s; PLANT-COVPOS-J (its Cov_inf_lo '
        'negated) %s; PLANT-PRECERT-J (RECORD marked PRECERT) %s; PLANT-CERTREQ-J (a copy tagged CERTIFIED without the requirement keys) '
        '%s; PLANT-FLOATIN-J (a CERTIFIED copy with every requirement but a FLOAT_IN token) %s' % (
            'FIRES' if pf else 'DOES NOT FIRE', 'FIRES' if ps else 'DOES NOT FIRE', 'FIRES' if pn else 'DOES NOT FIRE',
            'FIRES' if pp else 'DOES NOT FIRE', 'FIRES' if pc else 'DOES NOT FIRE', 'FIRES' if pfi else 'DOES NOT FIRE'))
    for name, f in (('PLANT-FMT-J', pf), ('PLANT-SRC-J', ps), ('PLANT-COVPOS-J', pn), ('PLANT-PRECERT-J', pp), ('PLANT-CERTREQ-J', pc),
                    ('PLANT-FLOATIN-J', pfi)):
        if not f:
            fires.append(name)
    if JOINT_MODE == 'certified' and ok_f and ok_s and not bad and JOINT_TAG_PIN is not None:     # 
        TAG_PINS['joint inputs'] = JOINT_TAG_PIN
        J['_tag'] = 'CERTIFIED %s %s' % JOINT_TAG_PIN
    else:
        J['_tag'] = '%s (%s)' % (JOINT_REC['status'], port.get('TAG', 'no TAG'))
    J['_dh'] = {(cls, N): port.get('DH_N%d_%s' % (N, cls)) for cls, _ in JOINT_CLASSES for N in (4, 3)}   # the assembly's own, if any
    J['_dh_other'] = sorted(k for k in port if k.startswith('DH_') and re.fullmatch(r'DH_N[34]_(%s)' % '|'.join(c for c, _ in JOINT_CLASSES),
                                                                                     k) is None)        # any other DH_ key
    return J


PLANT_JOINT0_EDIT = ("    first = pt(0) if sc.get('nofirst') else 2 * e * J['pX'] * sc.get('pX', 1.0)\n",
                     "    first = pt(0) if sc.get('nofirst') else 2 * J['pX'] * sc.get('pX', 1.0)\n")


def joint_scan(INP, SH1, JIN, TIN, fails, fires):
    """P2-14, the joint kind's part of the float scan at [300, 303]: the inputs combined over the grid pieces that meet [300, 303] (lowest
    Cov_inf_lo, highest pX_hi and normX_hi), the vertical and t inputs of [300, 303]; per N and class the threshold d^h, the slacks by d,
    the distances to flip at d^h, the hand-off threshold (HANDOFF_HR['joint']); C-JOINT0 (at e = 0 the kind is Cov_inf_lo exactly) with
    PLANT-JOINT0 (a copy of joint_slack whose first-order term lacks its factor e must fail it); PLANT-JOINT (the first-order term
    dropped: the pX distance at d^h must move); margin plants on C_div, pX and normX; the joint kill."""
    J3, J3h = 300.0, 303.0
    STAGE[0] = 'P2-14 joint scan [300, 303]'
    grid = joint_grid()
    idx = [i for i, (jlo, _) in enumerate(grid) if float(jlo) < J3h]       # the pieces meeting [300, 303] (an index choice only)
    src = inspect.getsource(joint_slack)
    if src.count(PLANT_JOINT0_EDIT[0]) != 1:
        raise RuntimeError('PLANT-JOINT0: source edit not found exactly once')
    ns = dict(iv=iv, pt=pt, JOINT_W=JOINT_W)
    exec(compile(src.replace(PLANT_JOINT0_EDIT[0], PLANT_JOINT0_EDIT[1]), 'PLANT-JOINT0 copy', 'exec'), ns)
    th, ho, live, j0bad, j0fire = {}, {}, [], [], []
    for N in (4, 3):
        T = t_scan_inputs(TIN, SH1, N, idx)
        Q = piece_eval(INP[N], J3, J3h, {})['Q']
        for cls, wX in JOINT_CLASSES:
            budget(4.0, 'P2-14 joint scan N=%d %s' % (N, cls))
            Js = [JIN[(cls, N, i)] for i in idx]
            J = dict(Cov=pmin([x['Cov'] for x in Js]), pX=pmax([x['pX'] for x in Js]), normX=pmax([x['normX'] for x in Js]))
            if not same_value(joint_slack(cls, Q, T, J, 0, {'Rw': 0.0}), J['Cov']):
                j0bad.append('N%d %s' % (N, cls))
            if same_value(ns['joint_slack'](cls, Q, T, J, 0, {'Rw': 0.0}), J['Cov']):
                j0fire.append('N%d %s' % (N, cls))
            dh, sl = joint_profile(cls, Q, T, J, {})
            th[(N, cls)] = dh
            dist = {}
            if dh <= DH_MAX:
                for key in JOINT_INPUTS:
                    dist[key] = flip_search(lambda x: joint_holds(cls, Q, T, J, dh, {key: x}), 'mul', MCAP)
                f0 = flip_search(lambda x: joint_holds(cls, Q, T, J, dh, {'pX': x, 'nofirst': True}), 'mul', MCAP)
                live.append((N, cls, dist['pX'], f0, f0 != dist['pX']))
            ho[(N, cls)] = joint_hr_dmin(cls, Q, T, J, HANDOFF_HR['joint'])
            out('P2-14 SCAN N=%d %s (w_X = %d), [300, 303] (inputs over grid pieces %s): Cov_inf_lo %s, pX_hi %s, normX_hi %s; d^h = %s; '
                'slack / Cov_inf_lo by d: %s; distances to flip at d^h: %s; hand-off threshold at HR %.2f: %s' % (
                    N, cls, wX, ','.join(str(i) for i in idx), nf(J['Cov']), nf(J['pX']), nf(J['normX']),
                    dh if dh <= DH_MAX else 'none <= %d' % DH_MAX,
                    ', '.join('d=%d %s' % (d, 'n/a' if sl[d] is False else '%+.4g' % fnum(pt(sl[d].a) / J['Cov'])) for d in range(DH_MAX + 1)),
                    '; '.join('%s %s' % (k, fmt_f(v)) for k, v in dist.items()) or 'n/a', HANDOFF_HR['joint'],
                    ho[(N, cls)] if ho[(N, cls)] <= DH_MAX else 'none'))
            for key in (('C_div', 'pX', 'normX') if dh <= DH_MAX else ()):
                F, raised = dist.get(key), ''
                if F is None:                                   # a term too small at d^h to flip it below MCAP (normX at a large d^h):
                    F = flip_search(lambda x: joint_holds(cls, Q, T, J, dh, {key: x}), 'mul', MCAP * 2 ** 16)   # the plant only
                    raised = ', the plant\'s cap raised to MCAP x 2^16'                                          # needs a flip
                fired = bool(F) and joint_holds(cls, Q, T, J, dh, {key: F / 1.1}) and not joint_holds(cls, Q, T, J, dh, {key: F * 1.1})
                out('PLANT-J-%s N=%d %s (d^h = %d%s): flip F = %s; holds at F / 1.1 and is lost at 1.1 F -> %s' % (
                    key, N, cls, dh, raised, fmt_f(F), 'FIRES' if fired else 'DOES NOT FIRE'))
                if not fired:
                    fires.append('PLANT-J-%s N=%d %s' % (key, N, cls))
    out('C-JOINT0 (P2-14): at e = 0 the joint kind equals Cov_inf_lo, endpoint for endpoint -> %s; PLANT-JOINT0 (a copy whose first-order '
        'term lacks its factor e) caught at %d of %d -> %s' % ('PASS' if not j0bad else 'FAIL (%s)' % ', '.join(j0bad),
                                                            2 * len(JOINT_CLASSES) - len(j0fire), 2 * len(JOINT_CLASSES),
                                                            'FIRES' if not j0fire else 'DOES NOT FIRE'))
    if j0bad:
        fails.append('C-JOINT0')
    if j0fire:
        fires.append('PLANT-JOINT0')
    fl = bool(live) and all(r[4] for r in live)
    out('PLANT-JOINT (P2-14: the first-order term dropped): pX distances at d^h %s -> %s' % (
        '; '.join('N%d %s %s -> %s' % (N, c, fmt_f(a), fmt_f(b)) for N, c, a, b, _ in live) or 'none', 'FIRES' if fl else 'DOES NOT FIRE'))
    if not fl:
        fires.append('PLANT-JOINT')
    out('P2-14 THRESHOLDS ([300, 303]): d^h %s; hand-off (HR %.2f) %s' % (
        '; '.join('N=%d %s' % (N, ', '.join('%s %s' % (c, th[(N, c)] if th[(N, c)] <= DH_MAX else 'none') for c, _ in JOINT_CLASSES))
                  for N in (4, 3)), HANDOFF_HR['joint'],
        '; '.join('N=%d %s' % (N, ', '.join('%s %s' % (c, ho[(N, c)] if ho[(N, c)] <= DH_MAX else 'none') for c, _ in JOINT_CLASSES))
                  for N in (4, 3))))
    for cls, _ in JOINT_CLASSES:
        dead = [N for N in (4, 3) if th[(N, cls)] > DH_MAX]
        out('KILL P2-14 %s (a threshold d^h <= %d at [300, 303] at both N): %s' % (
            cls, DH_MAX, 'PASS' if not dead else 'KILL at N=%s: reported, the class stops' % ', '.join(str(N) for N in dead)))
    return th


def margin_plant(inp, Jlo, Jhi, mk, F, which, lose=None):
    """S1, D2 (the form of ADD1's S5 plants): F is the flip distance the scan bisected for the hook maker mk on this piece and verdict.
    The plant fires when the verdict holds at F / 1.1 and is lost at 1.1 F; with lose (D2), the loss is required of those pairs alone.
    A search that found no flip in its bracket (F None) or a failing baseline (F = 0) does not fire. The search (flip_search,
    unchanged from v1_2): 'mul' starts from the bracket [1, 2] and doubles it up to the cap MCAP = 2048, 'add' from [0, 1e-4] up to
    1.0; it then bisects until hi / lo <= 1.004 ('mul') or hi - lo <= 0.004 hi ('add'), and F = hi is the first failing value found.
    So F lies within relative 0.4% above the flip, and F / 1.1 and 1.1 F sit about 9% and 10% from it, over twenty times the
    search's resolution."""
    if not F:
        return False
    hold = verdict_one(inp, Jlo, Jhi, mk(F / 1.1), which)
    lost = not verdict_one(inp, Jlo, Jhi, mk(F * 1.1), which, claim=lose)
    return hold and lost


# ------------------------------------------------------------------ exact controls
def transfer_current_binding():
    """T(a_j, b_{j+1}) on the infinite unit-conductance 3-row strip, mode form (PK10 sect. 1); SPEC ADD1 C-C2."""
    def g(lam):
        ch = 1 + pt(lam) / 2
        sh = iv.sqrt(ch * ch - 1)
        return (ch - sh) / (2 * sh)
    return g(1) / 2 - 3 * g(3) / 2


def det_iv(A):
    """determinant of an interval matrix by Gaussian elimination (SPD here, no pivoting)."""
    n = len(A)
    M = [row[:] for row in A]
    det = pt(1)
    for i in range(n):
        det *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for c in range(i, n):
                M[r][c] = M[r][c] - f * M[i][c]
    return det


# ------------------------------------------------------------------ controls (both items)
def c_repro170(INP, NSM, NSE, NSB, fails, fires):
    """C-REPRO at [170, 171.7]: path A rebuilds the author's printed lines (m2_unif3, endpairs4, assemble_unif4) and the coverage
    lines; path B equals path A (repro_compare, all 24 coverage pairs); PLANT-S2UP and PLANT-PATHB fire."""
    J0, J0h = 170.0, 170.0 * 1.01
    for N in (4, 3):
        inp = INP[N]
        m2t = open(os.path.join(SC, 'm2_unif3_N%d.txt' % N)).read().split('\n')
        ept = open(os.path.join(SC, 'endpairs4_N%d.txt' % N)).read()
        ab4t = open(os.path.join(SC, 'assemble_unif4_N%d.txt' % N)).read().split('\n')
        rct = open(os.path.join(CODEDIR, 'pk20/rv13/c6/rc_end_sens_N%d.txt' % N)).read().split('# N = %d, J in [2e4' % N)[0]
        Rp, rho, er, ew, L1e, be, cr = NSM[N]['check'](J0, J0h)
        lineA = ('J in [%.1f, %s]: R+ >= %.5f, rho_odd <= %.5f (ratio %.4f) | eps_r %.2e eps_w %.3e L1e %.5f beta %.4f cross/H_T %.4f'
                 % (J0, '%.1f' % J0h, Rp, rho, Rp / rho, er, ew, L1e, be, cr))
        Qa = NSE[N]['quantities'](J0, J0h)
        Ma = NSE[N]['mode_data'](J0, J0h, Qa)
        lineE = ('J = %g: R_w <= %.5f, rho1 <= %.5f, rho <= %.5f, R+ >= %.5f; mode: q_x >= %.5f, L2 <= %.5f, mu_x >= %.5f, alpha^2 >= %.4f, '
                 '|a_x| >= %.5f, Dlt <= %.2e, c_x >= %.5f (|v+| <= %.5f), r2 <= %.4f, ro <= %.4f'
                 % (170.0, Qa['Rw'], Qa['rho1'], Qa['rho'], Qa['Rp'], Ma['qx'], Ma['L2'], Ma['mux'], Ma['al2'], Ma['ax'], Ma['Dlt'], Ma['cx'],
                    Qa['vp'], Ma['r2'], Ma['ro']))
        cA, evA, odA, vtA, erA, svA, beA = NSB[N]['cov_lower'](J0, J0h)
        lineB = ('J in [%.1f, %s]: Cov J^2 >= %.4e (even >= %.6f, odd <= %.6f, vac <= %.2e, eps_r %.2e, s %.2e, beta <= %.4f)'
                 % (J0, '%.1f' % J0h, float(cA.a), float(evA.a), float(odA.b), float(vtA.b), erA, svA, float(beA.b)))
        oks = (lineA == m2t[1], ('\n' + lineE + '\n') in ('\n' + ept), lineB == ab4t[1])
        rows = re.findall(r"  (flip|same) d=(\d+): own Jensen m<=(\d+), mode m>=(\d+), (?:FULL|not full) \| author's tests: Jensen m<=(\d+), "
                          r"mode m>=(\d+)", rct)
        cva = cover_a(NSE[N], Qa, Ma, [(kd, int(d)) for kd, d, _, _, _, _ in rows])
        okc = len(rows) >= 4 and all(cva[(kd, int(d))] == (int(mj), int(mm) - 1) for kd, d, _, _, mj, mm in rows)
        w, wk, viol, cs = repro_compare(inp, NSM[N], NSE[N], NSB[N], J0, J0h, pairs=ALLPAIRS)
        ok = all(oks) and okc and w <= TOL_B and not viol and cs
        wd = ['identical' if o else 'DIFFERS' for o in oks]
        out('C-REPRO N=%d [170, 171.7]: author lines m2_unif3 %s, endpairs4 J = 170 %s, assemble_unif4 %s; reference coverage lines (%d) %s; '
            'path B (naive, author forms) vs A: worst relative %.2e (%s), coverage tables (%d pairs) %s; production forms never better than '
            'A: %s -> %s' % (N, wd[0], wd[1], wd[2], len(rows), 'match' if okc else 'DIFFER', w, wk, len(ALLPAIRS),
                             'identical' if cs else 'DIFFER', 'yes' if not viol else 'NO (%s)' % ', '.join(viol), 'PASS' if ok else 'FAIL'))
        for o, mine, theirs in ((oks[0], lineA, m2t[1]), (oks[1], lineE, '(see endpairs4_N%d.txt)' % N), (oks[2], lineB, ab4t[1])):
            if not o:
                out('  mine:   %s' % mine)
                out('  author: %s' % theirs)
        if not ok:
            fails.append('C-REPRO N=%d' % N)
        out('INFO N=%d: S5 at [170, 171.7] by path A %.4e; the J >= 170 values: author (FLOAT Cov_1) %.4e, RV13_1 outward-endpoint arb %s' % (
            N, float(cA.a), inp['P']['cov1'], '1.1735e-4' if N == 4 else '2.2036e-4'))
        _, _, viol2, _ = repro_compare(inp, NSM[N], NSE[N], NSB[N], J0, J0h, sc={'s2_upper': True})
        fired = 'rho' in viol2
        out('PLANT-S2UP N=%d (S2_even from the upper ends of the diagonal): production bounds beat path A on %s -> %s' % (
            N, ', '.join(viol2) if viol2 else 'nothing', 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-S2UP N=%d' % N)
        w3, wk3, _, cs3 = repro_compare(inp, NSM[N], NSE[N], NSB[N], J0, J0h, sc={'drop_sp': True})
        fired = not (w3 <= TOL_B and cs3)
        out('PLANT-PATHB N=%d (path B with sp = 0): worst relative B-A %.2e (%s) -> %s' % (N, w3, wk3, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-PATHB N=%d' % N)


def c_c2(INP, fails, fires):
    """C-C2 (ADD1 sect. 5): the S5 assembly at t = 0 equals c2 = (N - 1) T^2 / 2; PLANT-ODDSIGN and PLANT-T fire. FLOAT (mock) entries:
    the central assembly within 1e-10 relative. Certified entries (inp['m3_cert']: the a_k are balls, and an entry is a_0 + r(0) with
    |r(0)| <= err at t = 0): c2 must lie inside the assembly with the bars ('point' kind), by a certain comparison (a true statement of
    the enclosures, however wide the bars make it), and the central assembly of the a_k balls must be within 1e-8 of it (the consistency
    of the certified a_0 with the harmonic limit, the control's teeth). A plant fires when its value fails that test."""
    T = transfer_current_binding()
    V0 = dict(eps_ds5=pt(0))

    def assess(cx, c2, cert):
        cen = s5_parts(cx, V0, 'central')['Dd']
        rel_c = float((abs(cen - c2).b / c2.a).b)
        if not cert:
            return rel_c <= 1e-10, 'central even - odd at t = 0: %s, largest relative distance %.1e (within 1e-10)' % (nf(cen, 10), rel_c)
        pnt = s5_parts(cx, V0, 'point')['Dd']
        inside = (pnt.a <= c2.a) is True and (c2.b <= pnt.b) is True             # containment, not overlap
        return inside and rel_c <= 1e-8, ('even - odd at t = 0 with the bars: [%s, %s] (relative width %.1e), c2 inside: %s; central: %s, '
                                          'largest relative distance %.1e (within 1e-8)' % (
                                              nf(pt(pnt.a), 10), nf(pt(pnt.b), 10), float(((pnt.b - pnt.a) / c2.a).b), inside,
                                              nf(cen, 10), rel_c))
    for N in (4, 3):
        c2 = (N - 1) * T * T / 2
        cert = bool(INP[N].get('m3_cert'))
        cx = Ctx(INP[N], 1e30, None, {})
        cx.tm = iv.mpf([0, 0])
        ok, txt = assess(cx, c2, cert)
        out('C-C2 N=%d (%s): T = %s, c2 = (N-1)T^2/2 = %s; %s -> %s' % (
            N, 'certified entries' if cert else 'FLOAT entries', nf(T, 12), nf(c2, 10), txt, 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-C2 N=%d' % N)
        cxp = Ctx(INP[N], 1e30, None, {'odd_sign': True})
        cxp.tm = iv.mpf([0, 0])
        fired = not assess(cxp, c2, cert)[0]
        out('PLANT-ODDSIGN N=%d: C-C2 with the odd part added -> %s' % (N, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-ODDSIGN N=%d' % N)
    ch2 = 1 + pt(3) / 2
    Tbad = T + 3 * (ch2 - iv.sqrt(ch2 * ch2 - 1)) / (2 * iv.sqrt(ch2 * ch2 - 1))      # mode 2 weight +3/2 instead of -3/2
    cxb = Ctx(INP[4], 1e30, None, {})
    cxb.tm = iv.mpf([0, 0])
    c2bad = 3 * Tbad * Tbad / 2
    fired = not assess(cxb, c2bad, bool(INP[4].get('m3_cert')))[0]
    out('PLANT-T (N=4): C-C2 against the transfer current with mode 2 weight +3/2 -> %s' % ('FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-T')


def r_main_iv(N, swap=False):
    """v2_2 (1): endw's r_main by the matrix-tree theorem in mp.iv, (sqrt(det L_D det L_free) / det L_mix)^(N - 1), with
    the reduced Laplacians of the three 2-column graphs: closed-form triangle conductances A_EX = (3 + sqrt 21)/6 and B_EX =
    (3 sqrt 5 - sqrt 21)/12 (vacmod2 l.8-9, source-checked by C-HARM), unit verticals and horizontals. q (quantities) uses it in place
    of endw's stored float, and C-HARM compares the two. swap exchanges the two conductances (PLANT-HARM)."""
    a_ = (3 + iv.sqrt(21)) / 6
    b_ = (3 * iv.sqrt(5) - iv.sqrt(21)) / 12
    if swap:
        a_, b_ = b_, a_

    def lap(edges):
        L = [[pt(0)] * 6 for _ in range(6)]
        for (u, v), cc in edges:
            L[u][u] += cc
            L[v][v] += cc
            L[u][v] -= cc
            L[v][u] -= cc
        return [row[1:] for row in L[1:]]
    tri = lambda o: [((o, o + 1), a_), ((o + 1, o + 2), a_), ((o, o + 2), b_)]
    ver = lambda o: [((o, o + 1), pt(1)), ((o + 1, o + 2), pt(1))]
    hor = [((r, 3 + r), pt(1)) for r in range(3)]
    tD, tmix, tfree = det_iv(lap(tri(0) + tri(3) + hor)), det_iv(lap(tri(0) + ver(3) + hor)), det_iv(lap(ver(0) + ver(3) + hor))
    return finite((iv.sqrt(tD * tfree) / tmix) ** (N - 1), 'r_main')


def c_harm(INP, fails, fires):
    """C-HARM (v1_1 sect. 4): r_main by the matrix-tree theorem in mp.iv (r_main_iv, which q uses since v2_2) against endw's stored
    value, and q^2(t = 0) = r_main, to 1e-10, with vacmod2's closed forms source-checked; PLANT-HARM (v2_2): the two conductances
    swapped must fail the comparison."""
    vm2 = open(os.path.join(SCR, 'vacmod2.py')).read().split('\n')
    okf = (vm2[7].strip() == 'A_EX = (3 + math.sqrt(21)) / 6' and vm2[8].strip() == 'B_EX = (3 * math.sqrt(5) - math.sqrt(21)) / 12')
    for N in (4, 3):
        inp = INP[N]
        r_iv = r_main_iv(N)
        r_st = inp['EW']['r_main']
        d1 = float(abs(r_iv - r_st).b) / r_st
        a0 = lambda d: d['ak'][0]
        q0 = a0(inp['EW']['items']['I_mix']) ** 2 * r_st / (a0(inp['M2']['items']['g00']) * a0(inp['EW']['items']['I_free']))
        d2 = abs(q0 - r_st) / r_st
        ok = okf and d1 <= 1e-10 and d2 <= 1e-10
        out('C-HARM N=%d: r_main by matrix-tree %s vs stored %.12f (relative %.1e); q^2(t=0) %.12f (relative %.1e); vacmod2 closed forms %s '
            '-> %s' % (N, nf(r_iv, 13), r_st, d1, q0, d2, 'match' if okf else 'DIFFER', 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-HARM N=%d' % N)
        d3 = float(abs(r_main_iv(N, swap=True) - r_st).b) / r_st
        out('PLANT-HARM N=%d (v2_2: the conductances A_EX and B_EX swapped in the matrix-tree value): relative %.1e against the stored '
            'r_main -> %s' % (N, d3, 'FIRES' if d3 > 1e-10 else 'DOES NOT FIRE'))
        if not d3 > 1e-10:
            fires.append('PLANT-HARM N=%d' % N)
        it = inp['M2']['items']
        out('INFO-HARM N=%d: trial R+ at t = 0, I3p_0/N_w_0 = %.5f (harmonic 0.61 x 0.146 + 0.39 x 0.044 = %.4f)' % (
            N, it['I3p']['ak'][0] / it['Nw']['ak'][0], 0.61 * 0.146 + 0.39 * 0.044))


def c_ip3(INP, fails):
    """C-IP3 (v1_1 sect. 4): I_p3 = m-hat N_w (the eigen trick) at a_0, a_1 and a_2, to 1e-12 max(1, |a|); INFO a_3, J = 170."""
    for N in (4, 3):
        inp = INP[N]
        it, ms = inp['M2']['items'], inp['mser']
        mh = [1.0, ms['m1'], ms['m2'], ms['m3']]
        ip, nw = it['Ip3']['ak'], it['Nw']['ak']
        mn = [sum(mh[i] * nw[k - i] for i in range(k + 1)) for k in range(4)]
        dk = [ip[k] - mn[k] for k in range(4)]
        ok = all(abs(dk[k]) <= 1e-12 * max(1.0, abs(ip[k])) for k in (0, 1, 2))
        tt = 1.0 / 170
        dv = sum(ip[k] * tt ** k for k in range(4)) - sum(mn[k] * tt ** k for k in range(4))
        out('C-IP3 N=%d: I_p3 - m-hat N_w a_0 %.2e, a_1 %.2e, a_2 %.2e (tolerance 1e-12) -> %s; INFO a_3 %.3e; at J = 170 %.3e' % (
            N, dk[0], dk[1], dk[2], 'PASS' if ok else 'FAIL', dk[3], dv))
        if not ok:
            fails.append('C-IP3 N=%d' % N)


def c_kbar(INP, fails, fires):
    """C-KBAR (v2_2 (2), the argument is in FREEZE_NOTE_kt_s67_cert_v2_2 sect. 2). k-bar is a free centering constant
    of the construction, not an input to certify: v+ = Q0 T_{xi+ - kbar} u / lam0 for every constant kbar (PK10_NOTES 19.5.1). The
    bounds that use it hold for every kbar >= 0: B_op = max(beta, kbar (1 + eps_r)) rests on -kbar T <= T_w~, that is kbar >= 0
    (19.5.4); the mismatch between kbar and the exact centering enters S6 through u_h's |k_n - kbar g00| / g00, and S7 through E_w in
    t1 = (kbar + E_w)(1 + eps_r), since the exact bulk mean is kbar + <u, T_w~ u> / lam0 (19.6.2-3); both carry the entries' bars. So
    it needs kbar >= 0 and the same kbar as m2's w~ integrals N_w, I3p, I_p3 and A_0w, which come from the same m2 file. Gate: kbar >= 0
    exactly, and on [300, 303] u_h >= its centering term and t1 >= kbar (1 + eps_r). PLANT-KBAR: kbar negated must fail the sign gate."""
    for N in (4, 3):
        inp = INP[N]
        kb = pt(inp['M2']['kbar'])
        cx = Ctx(inp, 300.0, 303.0, {})
        g00, kn = cx.entry('M2', 'g00'), cx.entry('M2', 'kn')
        mm = abs(kn - kb * g00) / g00
        Q = piece_eval(inp, 300.0, 303.0, {})['Q']
        sign_ok = (kb >= 0) is True
        cover_u = (Q['uh'].b >= mm.b) is True
        cover_t = (Q['t1'] >= kb * (1 + Q['er'])) is True
        ok = sign_ok and cover_u and cover_t
        fired = not ((pt(-inp['M2']['kbar']) >= 0) is True)
        out('C-KBAR N=%d (v2_2: k-bar a free centering constant): kbar = %r, m2\'s own (pk10/scratch/m2_N%d_J170.json.b, the constant its '
            'N_w, I3p, I_p3 and A_0w integrate w~ = xi+ - kbar with); kbar >= 0: %s; on [300, 303] the S6 centering term |k_n - kbar g00|/g00 '
            '<= %s lies inside u_h <= %s: %s; S7: E_w <= %s and t1 = (kbar + E_w)(1 + eps_r) <= %s, >= kbar (1 + eps_r): %s -> %s; '
            'PLANT-KBAR (kbar negated) must fail the sign gate -> %s' % (
                N, inp['M2']['kbar'], N, sign_ok, nf(mm.b, 6), nf(Q['uh'].b, 6), cover_u, nf(Q['Ew'], 6), nf(Q['t1'], 6), cover_t,
                'PASS' if ok else 'FAIL', 'FIRES' if fired else 'DOES NOT FIRE'))
        if not ok:
            fails.append('C-KBAR N=%d' % N)
        if not fired:
            fires.append('PLANT-KBAR N=%d' % N)


def c_guards(INP, fails, fires):
    """C-PARITY (INFO while M3's tag is FLOAT, a gate once it is certified; its control and plant gate), C-MODULE and C-TAG, with
    their plants."""
    for N in (4, 3):
        cert = bool(INP[N].get('m3_cert'))                               # a gate for an N whose records are certified
        B5, CT = INP[N]['B5'], INP[N]['CT']
        pmx = parity_max(B5)
        pb = parity_bad(B5, CT)
        sym = json.loads(json.dumps(B5))                                 # the control: every cross-parity field zeroed
        for k in PARITY_KEYS:
            it = sym['items'][k]
            for f in ('ak', 'ak_rad'):
                it[f] = [0.0] * len(it['ak'])
            for f in ('B', 'Bp'):
                it[f] = {x: 0.0 for x in it[f]} if isinstance(it.get(f), dict) else 0.0
            it['err'] = 0.0
        ok_sym = not parity_bad(sym, {'items': {}})
        plants = []                                                      # S2: one nonzero part in a symmetrized copy each
        for lab, fld in (('a_0', 'ak'), ('ak_rad_0', 'ak_rad'), ('bar B.rem', 'B'), ('err', 'err')):
            pl = json.loads(json.dumps(sym))
            it = pl['items'][PARITY_KEYS[0]]
            if fld in ('ak', 'ak_rad'):
                it[fld][0] = 1e-12
            elif fld == 'B':
                it['B'] = dict(it['B'], rem=1e-12) if isinstance(it['B'], dict) else 1e-12
            else:
                it['err'] = 1e-12
            plants.append((lab, bool(parity_bad(pl, {'items': {}}))))
        for lab in ('err dropped', 'B.rem None', 'B.rem False'):        # a missing or None field fails too;
            pl = json.loads(json.dumps(sym))                             # and a bool (False == 0)
            it = pl['items'][PARITY_KEYS[0]]
            if lab == 'err dropped':
                del it['err']
            else:
                v = None if lab == 'B.rem None' else False
                it['B'] = dict(it['B'], rem=v) if isinstance(it['B'], dict) else v
            plants.append((lab, bool(parity_bad(pl, {'items': {}}))))
        ct_pl = {'items': {PARITY_T_KEYS[0]: dict(kind='entry', ak=[0.0, 1e-12], ak_rad=[0.0, 0.0], B={'rem': 0.0}, Bp={'rem': 0.0},
                                                  err=0.0)}}
        plants.append(('a present clT %s with a_1 = 1e-12' % PARITY_T_KEYS[0], bool(parity_bad(sym, ct_pl))))
        fired = all(f for _, f in plants)
        out('C-PARITY N=%d (%s): the cross-parity Gram entries %s: max |a_k| = %.2e, and a_k, ak_rad, B, Bp and err all exactly zero; clT\'s '
            '%s absent or all zero: %s; control, a symmetrized copy -> %s; PLANT-PARITY (one nonzero part in that copy: %s) -> %s' % (
                N, 'a gate, the N\'s records are certified' if cert else 'INFO: mock records copy the unsymmetrized FLOAT files',
                ', '.join(PARITY_KEYS), pmx, ', '.join(PARITY_T_KEYS), 'yes' if not pb else 'NO (%s)' % ', '.join(pb[:4]),
                'PASS' if ok_sym else 'FAIL', ', '.join('%s %s' % (lab, 'fires' if f else 'DOES NOT FIRE') for lab, f in plants),
                'FIRES' if fired else 'DOES NOT FIRE'))
        if cert and pb:
            fails.append('C-PARITY N=%d' % N)
        if not ok_sym:
            fails.append('C-PARITY control N=%d' % N)
        if not fired:
            fires.append('PLANT-PARITY N=%d' % N)
    srcs = {n: inspect.getsource(globals()[n]) for n in VERDICT_FUNCS}
    hits = module_scan(srcs)
    out('C-MODULE: %d verdict-path functions and classes against %d forbidden patterns: %s -> %s' % (
        len(srcs), len(FORBIDDEN), 'none' if not hits else '; '.join('%s: %s' % h for h in hits), 'PASS' if not hits else 'FAIL'))
    if hits:
        fails.append('C-MODULE')
    qs = srcs['quantities']
    planted = qs.replace('iv.sqrt(1 - s * s)', 'math.sqrt(1 - s * s)', 1)
    fired = planted != qs and bool(module_scan({'quantities, planted': planted}))
    out('PLANT-MODULE: a libm sqrt planted in quantities -> %s' % ('FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-MODULE')
    ctl = {k: ('ctl%d' % i, '%08x' % (0x5eed0000 + i)) for i, k in enumerate(sorted(TAGS))}      # control pins, one per input
    cert = {k: 'CERTIFIED %s %s' % ctl[k] for k in TAGS}
    full = all(k in TAG_PINS for k in TAGS)                             # N-a (v2_1): every input has a provider and a pin
    ok = (verdict_word(cert, True, ctl) == 'CERTIFIED' and verdict_word(cert, False, ctl) == 'FAIL'
          and verdict_word({**cert, 'M3 entries': 'FLOAT (control)'}, True, ctl) == 'FLOAT-PASS'
          and verdict_word(TAGS, True) == ('CERTIFIED' if full else 'FLOAT-PASS'))
    wrong = ctl['S4 U'][1][:7] + ('1' if ctl['S4 U'][1][7] == '0' else '0')
    cases = (('FLOAT tags', {k: 'FLOAT (plant)' for k in TAGS}),
             ('S4 TRB = "S4-TRB, pending"', {**cert, 'S4 TRB': 'S4-TRB, pending'}),
             ('S4 U = CERTIFIED with a wrong sha8', {**cert, 'S4 U': 'CERTIFIED %s %s' % (ctl['S4 U'][0], wrong)}))
    res = [(lab, verdict_word(tg, True, ctl)) for lab, tg in cases]
    out('C-TAG: wording control (control pins: all certified -> CERTIFIED, a failed verdict -> FAIL, one FLOAT tag -> FLOAT-PASS; this '
        'run\'s tags -> CERTIFIED exactly when every input has a pin, here %s: %s) -> %s; PLANT-TAG (F1), each with every other tag '
        'certified, must not read CERTIFIED: %s' % (
            'CERTIFIED' if full else 'FLOAT-PASS', 'every input has a pin' if full else 'no pin for %s' % ', '.join(
                sorted(k for k in TAGS if k not in TAG_PINS)),
            'PASS' if ok else 'FAIL', '; '.join('%s -> %s -> %s' % (lab, w, 'FIRES' if w != 'CERTIFIED' else 'DOES NOT FIRE')
                                                for lab, w in res)))
    if not ok:
        fails.append('C-TAG')
    for i, (lab, w) in enumerate(res):
        if w == 'CERTIFIED':
            fires.append('PLANT-TAG case %d (%s)' % (i + 1, lab))


def c_fmt(INP, NSB, fails, fires):
    """C-FMT (S2), FLOAT form: the port's reader (Ctx.entry, naive, over [300, 303]) against the author's reader (assemble_binding_unif4's
    item(), the convention m2_unif3 and endpairs4 share) on every stored entry of every file. PLANT-FMT: the port reading a copy with two
    entries' coefficient lists swapped must fail."""
    def worst_diff(inp_port, inp_prod, item):
        cx = Ctx(inp_port, 300.0, 303.0, {})
        w, wk, n = 0.0, '', 0
        for src, name in entry_names(inp_prod):
            a = item(name, {'I_N': inp_prod['B4']['I_N']} if src == 'B4' else inp_prod[src]['items'], cx.tI)
            b = cx.entry(src, name, 'naive')
            r_ = float((abs(a.a - b.a) + abs(a.b - b.b)).b) / max(1.0, abs(fnum(a)))
            n += 1
            if r_ > w:
                w, wk = r_, '%s %s' % (src, name)
        return w, wk, n
    for N in (4, 3):
        FI = float_s4(INP[N])                 # the FLOAT JSONs both readers read (the M3 provider has its own C-FMT M3 for the records)
        w, wk, n = worst_diff(FI, FI, NSB[N]['item'])
        ok = w <= 1e-15
        out('C-FMT N=%d: %d stored entries, the port\'s reader against the author\'s item() over [300, 303]: worst difference %.1e (%s) -> %s' % (
            N, n, w, wk or 'none', 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-FMT N=%d' % N)
        sw = json.loads(json.dumps({k: v for k, v in FI.items() if k not in ('U5', 'TRBv', 'r_iv')}))   # mp.iv values left out
        it_ = sw['B5']['items']
        it_['g,0,1']['ak'], it_['g,1,1']['ak'] = it_['g,1,1']['ak'], it_['g,0,1']['ak']
        w, wk, _ = worst_diff(sw, FI, NSB[N]['item'])
        fired = w > 1e-15
        out('PLANT-FMT N=%d (the port reads a copy with the g,0,1 and g,1,1 coefficient lists swapped): worst difference %.1e (%s) -> %s' % (
            N, w, wk, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-FMT N=%d' % N)


TGT = dict(err=1.186, U=7.8e-4, TRB=1.02)     # SPEC v1_2 sect. 3, the set T2: errors = bars, vacuum, eps_w. "float U" is today's
                                              # U = lead(1 + c1 t + c2 t^2 + c3 t^3) + rem(170), and T2 raises it, rem included, by +7.8e-4
TGT_DEC = dict(U='7.8e-4', QUAD='3.9e-4', TRB='1.02')    # the same targets as exact decimals, for KR3 and KR4; S4U_HEADER pins the
                                                          # record's copies of the first two, S4T_HEADER the TRB target's decimals


def certified_inputs():
    """the inputs whose tags read certified (F1)."""
    return {k for k, v in TAGS.items() if tag_certified(k, v)}


def tgt_hooks(lam, cert=()):
    """every input at lambda times its target excess (lambda = 1: the v1_2 targets). A certified input enters with its certified value
    instead of its target (SPEC sect. 4): S4 U drops U_add, S4 TRB drops TRB, M3 drops bar_all, M2 drops vac_all and eps_w."""
    x = 1 + lam * (TGT['err'] - 1)
    h = {}
    if 'M3 entries' not in cert:
        h['bar_all'] = x
    if 'M2 vacuum' not in cert:
        h.update(vac_all=x, eps_w=x)
    if 'S4 U' not in cert:
        h['U_add'] = lam * TGT['U']
    if 'S4 TRB' not in cert:
        h['TRB'] = 1 + lam * (TGT['TRB'] - 1)
    return h


def tgt_text(lam, cert):
    """the C-TARGETS line's statement of the inputs at lambda."""
    x, s = 1 + lam * (TGT['err'] - 1), []
    s.append('bars %s' % ('certified (M3)' if 'M3 entries' in cert else 'x%.4g' % x))
    s.append('vacuum and eps_w %s' % ('certified (M2)' if 'M2 vacuum' in cert else 'x%.4g' % x))
    s.append('U %s' % ('certified (S4-U, U3(t) + R_CERT, no target added)' if 'S4 U' in cert else
                       '+ %.3g on today\'s U, rem(170) included' % (lam * TGT['U'])))
    s.append('TRB %s' % ('certified (S4-TRB)' if 'S4 TRB' in cert else 'x%.4g' % (1 + lam * (TGT['TRB'] - 1))))
    return ', '.join(s)


def tgt_piece(inp, Jlo, Jhi, sc, use_centered):
    """S5, S6 and S7 with the Lemma S7-mono hypotheses and lambda_1^e simple on one piece: (verdict, c5, R+/rho lower end)."""
    try:
        E = piece_eval(inp, Jlo, Jhi, sc, use_centered=use_centered)
        c5, r6 = E['S5']['c5'], (E['Q']['Rp'] / E['Q']['rho']).a
        hold = ((c5 > 0) is True and (r6 > 1) is True and E['Mq']['simple']
                and all(claim_holds(E['cv'], p) and s7mono_hyp(E['Q'], E['Mq'], p[1], E['cv'][p][1], sc) for p in CLAIM[inp['N']]))
        return hold, c5, r6
    except (ValueError, ZeroDivisionError, ArithmeticError):
        return False, None, None


def c_targets(INP):
    """C-TARGETS (F1): every input at its v1_2 target at once (lambda = 1), then at lambda = 1.25, on every piece of the grid, S5, S6 and
    S7 at both N, with the naive enclosures; a piece that fails naive is re-evaluated with the production forms (centered), and
    the production result decides. Returns {(lam, N): (all hold in production form, worst c5 (value, piece), worst R+/rho, pieces failing
    naive, pieces failing in production form)}. Certified inputs enter with their certified values (tgt_hooks; F2: S4-U)."""
    res = {}
    cert = certified_inputs()
    for lam in (1.0, 1.25):
        sc = tgt_hooks(lam, cert)
        for N in (4, 3):
            STAGE[0] = 'C-TARGETS lambda=%.2f N=%d' % (lam, N)
            w5, w6, badn, badp = None, None, [], []
            for (Jlo, Jhi) in pieces():
                budget(1.0, STAGE[0])
                hold, c5, r6 = tgt_piece(INP[N], Jlo, Jhi, sc, False)
                if not hold:
                    badn.append(Jlo)
                    hold, c5p, r6p = tgt_piece(INP[N], Jlo, Jhi, sc, True)
                    c5, r6 = (c5p, r6p) if c5p is not None else (c5, r6)
                    if not hold:
                        badp.append(Jlo)
                if c5 is not None and (w5 is None or (c5 < w5[0]) is True):
                    w5 = (c5, Jlo, Jhi)
                if r6 is not None and (w6 is None or (r6 < w6[0]) is True):
                    w6 = (r6, Jlo, Jhi)
            res[(lam, N)] = (not badp, w5, w6, badn, badp)
    return res


# ------------------------------------------------------------------ PK21: the tight Hilbert-Schmidt bound over P_4, per piece
# Kill test (i) of pk21's step 1, a reading, not a certified record. tau_inf^2 <= tr T^2 - sum_k theta_k^2 over
# the four trial states (supplement v5b l.307). In S6's quantities: rho2 = U - sum of the squared even Ritz diagonal entries (upper end,
# the same number S6's rho uses), muz = the odd trial state's Ritz value (lower end), lam0 = the lower bound of lambda_0; units lambda_h.
TAU4_ROWS = {4: [], 3: []}


def tau4_row(Jlo, Jhi, Q):
    """(Jlo, Jhi, rho2_hi, muz_lo, lam0_lo, tau4_hi, rho_hi); tau4_hi = upper end of sqrt(rho2 - muz^2) / lam0, None if rho2 < muz^2."""
    r2, mz, l0 = pt(Q['rho2']), pt(Q['muz']), pt(Q['lam0'])
    arg = r2 - mz * mz
    t4 = None
    if (arg.b < 0) is not True:
        t4 = (iv.sqrt(iv.mpf([0, arg.b])) / l0).b
    return (Jlo, Jhi, r2.b, mz.a, l0.a, t4, pt(Q['rho']).b)


def tau4_summary(N):
    """the per-N summary line and the TSV of every piece (pk21's folder)."""
    rows = TAU4_ROWS[N]
    good = [r for r in rows if r[5] is not None]
    if not rows:
        out('PK21 TAU4 N=%d: no rows' % N)
        return
    worst = max(good, key=lambda r: fnum(r[5])) if good else None
    nbad = sum(1 for r in rows if r[5] is None or fnum(r[5]) >= 0.04)
    out('PK21 TAU4 N=%d: %d pieces; max tau4_hi %s on [%s] (rho_hi there %s); first piece [%s] tau4_hi %s; last piece [%s] tau4_hi %s; '
        'pieces with tau4_hi >= 0.04 or undefined: %d' % (
            N, len(rows), nf(worst[5], 8) if worst else 'NONE', piece_str(worst[0], worst[1]) if worst else '-',
            nf(worst[6], 8) if worst else '-', piece_str(rows[0][0], rows[0][1]), nf(rows[0][5], 8) if rows[0][5] is not None else 'NONE',
            piece_str(rows[-1][0], rows[-1][1]), nf(rows[-1][5], 8) if rows[-1][5] is not None else 'NONE', nbad))
    path = os.path.join(OUTD, 'tau4_%s_N%d.tsv' % (LABEL, N))
    with open(path, 'x') as fh:
        fh.write('jlo\tjhi\trho2_hi\tmuz_lo\tlam0_lo\ttau4_hi\trho_hi\n')
        for r in rows:
            fh.write('%s\t%s\t%r\t%r\t%r\t%s\t%r\n' % (repr(r[0]), 'inf' if r[1] is None else repr(r[1]), fnum(r[2]), fnum(r[3]),
                                                     fnum(r[4]), 'NONE' if r[5] is None else repr(fnum(r[5])), fnum(r[6])))
    out('PK21 TAU4 N=%d: TSV %s (%d rows)' % (N, path, len(rows)))


# ------------------------------------------------------------------ item sweep: every piece of [300, inf), both N
def item_sweep(INP, NSM, NSE, NSB, fails, fires, SH1, JIN, TIN):
    PCS = pieces()
    res = {}
    WS = width_sides()                                                      # P2-11: C-WIDTH's two sides
    for N in (4, 3):
        STAGE[0] = 'sweep N=%d' % N
        inp = INP[N]
        R = dict(n=0, w5=None, w6=None, holds=True, simple=True, mono=True, mvbad=0, mvkeys=set(), ofb=0, cov={}, rep=(0.0, ''), viol=[],
                 covsame=True, nrep=0, wbad=[], wgrid=0, c2a={}, handoff={}, joint={})
        for i, (Jlo, Jhi) in enumerate(PCS):
            budget(1.0, 'sweep N=%d piece %d' % (N, i))
            E = piece_eval(inp, Jlo, Jhi, {})
            Q, Mq, S5, cv = E['Q'], E['Mq'], E['S5'], E['cv']
            TAU4_ROWS[N].append(tau4_row(Jlo, Jhi, Q))                          # PK21: kill test (i)
            EXPORT_ROWS[N].append(export_row(Jlo, Jhi, N, E))                 # v2_2 (3): the piece's export line
            grid = i % WIDTH_STEP == 0 or Jhi is None
            if grid and inp.get('balls'):                                   # C-VERT's row on v2_2's inputs (the M3 provider's records)
                VERT_ROWS[N][i] = export_row(Jlo, Jhi, N, piece_eval(float_m3(inp), Jlo, Jhi, {}))
            R['wbad'] += ['%s at J = %.1f' % (b, Jlo) for b in c_width_piece(WS, N, E, grid)]     # P2-11: C-WIDTH
            R['wgrid'] += 1 if grid else 0
            if i == 0 and N == 4:                                           # P2-11: PLANT-WIDTH on the first piece's slack grid
                pw, npw = width_grid(WS, 'v22s', 'forkp', Q, Mq, S5['c5'])
                out('PLANT-WIDTH (P2-11; N=4, [%s]: the fork\'s slack copy with D\'s power over-shifted, k + w_a + w_b -> k + w_a + w_b + 1 '
                    'in width_exps): the slack grid differs at %d of %d points -> %s' % (piece_str(Jlo, Jhi), len(pw), npw,
                                                                                          'FIRES' if pw else 'DOES NOT FIRE'))
                if not pw:
                    fires.append('PLANT-WIDTH')
            T_ = None if VERT else (TIN[(N, i)] if TIN is not None else SH1['tin'][N])     # the VERTICAL mode has no t inputs
            if grid and T_ is not None and 'dtx' in T_:                     # the corner line's pieces (in every full run)
                R.setdefault('corner_pcs', []).append((Jlo, Jhi, Q, Mq, T_))
            if grid:                                                        # the S7 room line's pieces (both modes)
                R.setdefault('s7_pcs', []).append((Jlo, Jhi))
            for kind, _ in (() if VERT else KINDS):                         # P2-11 step 3: the C2-a kinds on this piece
                dmn, sl = kind_profile(kind, Q, Mq, T_, {})
                c2a_add(R['c2a'].setdefault(kind, c2a_acc()), dmn, sl, kind_scale(kind, T_),
                        lambda d, cap: kind_level(kind, Q, Mq, T_, d, cap), Jlo, Jhi)
            for cls, _ in (JOINT_CLASSES if JIN is not None else ()):         # P2-14: the joint kind on this piece
                Jp = JIN[(cls, N, i)]
                dmn, sl = joint_profile(cls, Q, T_, Jp, {})
                c2a_add(R['joint'].setdefault(cls, c2a_acc()), dmn, sl, Jp['Cov'], lambda d, cap: joint_level(cls, Q, T_, Jp, d, cap),
                        Jlo, Jhi)
            r6 = (Q['Rp'] / Q['rho']).a
            if R['w6'] is None or (r6 < R['w6'][0]) is True:
                R['w6'] = (r6, Jlo, Jhi)
            if R['w5'] is None or (S5['c5'] < R['w5'][0]) is True:
                R['w5'] = (S5['c5'], Jlo, Jhi)
            for p in CLAIM[N]:
                mj, km = R['cov'].get(p, (MMAX, 0))
                R['cov'][p] = (min(mj, cv[p][0]), max(km, cv[p][1]))
                R['holds'] = R['holds'] and claim_holds(cv, p)
                R['mono'] = R['mono'] and s7mono_hyp(Q, Mq, p[1], cv[p][1], {})
            R['simple'] = R['simple'] and Mq['simple']
            R['ofb'] += 0 if Q['order_ok'] else 1
            R['kink'] = R.get('kink', 0) + E['cx'].cache.get('fallbacks', 0)
            bad = mv_check(E['cx'], E['Ub'])
            if bad:
                R['mvbad'] += 1
                R['mvkeys'].update(bad)
            if i % 100 == 0 or Jhi is None:
                out('  sweep N=%d: piece %d [%s] at cpu %.1f s' % (N, i, piece_str(Jlo, Jhi), cpu()))
                w, wk, viol, cs = repro_compare(inp, NSM[N], NSE[N], NSB[N], Jlo, Jhi)
                R['nrep'] += 1
                if w > R['rep'][0]:
                    R['rep'] = (w, '%s at J = %.1f' % (wk, Jlo))
                R['viol'] += ['%s at J = %.1f' % (v, Jlo) for v in viol]
                R['covsame'] = R['covsame'] and cs
            R['n'] += 1
        R['last_rho'] = E['Q']['rho']
        res[N] = R
        ok5 = (R['w5'][0] > 0) is True
        ok6 = (R['w6'][0] > 1) is True and ok5
        ok7 = R['holds'] and R['simple'] and R['mono'] and R['mvbad'] == 0
        out('S5 N=%d: c5 = min over %d pieces of [even_lo - odd_up - vacT_up] = %s on [%s] -> %s' % (
            N, R['n'], nf(R['w5'][0]), piece_str(R['w5'][1], R['w5'][2]), verdict_word(TAGS, ok5)))        # F1: the tags decide
        out('S6 N=%d: min R+/rho (lower end) %s on [%s]; sign condition c5 > 0 (S5) %s -> %s' % (
            N, nf(R['w6'][0]), piece_str(R['w6'][1], R['w6'][2]), ok5, verdict_word(TAGS, ok6)))
        out('S7 N=%d: claimed coverage %s on every piece %s (worst over pieces: %s); lambda_1^e simple on all pieces %s; Lemma S7-mono (a) '
            'hypotheses %s; C-MV clean %s -> %s' % (
                N, ', '.join('%s d>=%d' % p for p in CLAIM[N]), 'HOLDS' if R['holds'] else 'FAILS',
                '; '.join('%s d=%d: Jensen checked to m=%d, mode from m=%d' % (p[0], p[1], R['cov'][p][0], R['cov'][p][1] + 1) for p in CLAIM[N]),
                R['simple'], R['mono'], R['mvbad'] == 0, verdict_word(TAGS, ok7)))
        okmv = R['mvbad'] == 0
        out('C-MV N=%d: %d pieces x 4 smooth forms x 9 points: failures on %d pieces (%s) -> %s' % (
            N, R['n'], R['mvbad'], ', '.join(sorted(R['mvkeys'])) or 'none', 'PASS' if okmv else 'FAIL'))
        if not okmv:
            fails.append('C-MV N=%d' % N)
        out('C-WIDTH N=%d (P2-11): v2_2\'s S7 block (%s l.%d-%d, sha256 %s) against the fork\'s width-aware S7 functions at w = (1, 1): '
            'the claimed-pair tables on %d pieces, the slack grid (pj, pm: both kinds, d in DS, m and k 1..6; s7mono_hyp: d in DS, k0 1..6) '
            'on %d pieces, endpoint for endpoint: %s -> %s' % (
                N, V22_S7[0], V22_S7[1], V22_S7[2], V22_S7[3][:8], R['n'], R['wgrid'],
                'identical' if not R['wbad'] else '%d differences (%s)' % (len(R['wbad']), ', '.join(R['wbad'][:4])),
                'PASS' if not R['wbad'] else 'FAIL'))
        if R['wbad']:
            fails.append('C-WIDTH N=%d' % N)
        if not VERT:                                                        # P2-11 step 3: C2a.1 and C2a.2 per kind (full mode)
            T = SH1['tin'][N] if TIN is None else TIN[(N, 0)]
            out('C2a.1 N=%d (P2-11): ||B_t|| <= beta_H = %s (%s), the full-norm bound used for both parities and the u-perp case (the review '
                '19f74c2b (d)) -> %s' % (
                    N, nf(T['bH'], 7), SH1['tag'] if TIN is None else TIN['_bh_tag'], verdict_word(c2a_tags(SH1, TIN, JIN, 'flip'), True)))
        rows_ = [] if VERT else [(kind, 'C2a.2', 'kind', 'w = (%d, %d), NOTE_P2_11_C2A_v1 sect. 3, one check at k = 0 for every k' % w,
                                  'A_t^2' if kind != 'mixed' else 'A_t A_a', HANDOFF_HR[kind], R['c2a'][kind], c2a_tags(SH1, TIN, JIN, kind))
                                 for kind, w in KINDS]
        rows_ += [(cls, 'C2a.4', 'joint class', 'P2-14 joint kind, w_X = %d, NOTE_P2_11_C2A_v1_1 sect. 2' % wX, 'Cov_inf_lo',
                   HANDOFF_HR['joint'], R['joint'][cls], c2a_tags(SH1, TIN, JIN, 'joint'))
                  for cls, wX in (JOINT_CLASSES if JIN is not None else ())]
        for name, lab, what, desc, scl, hr, C, tg_ in rows_:
            dh = C['dmax']
            ok = dh <= DH_MAX and plan_dh(C['lev'], 1.0) == dh
            dp = plan_dh(C['lev'], hr)
            wv = C['worst'][dh] if dh <= DH_MAX else None
            R['handoff'][name] = (dh, dp)
            out('%s N=%d %s (%s): on every one of %d pieces the %s holds at every d >= %s (checked for d <= %d; larger d follow because the '
                'slack is nonincreasing in e = R_w rho1^d), so every piece\'s own threshold is <= this claim threshold '
                'DH_N%d_%s (pieces by their own threshold: %s; the largest first on [%s]); worst slack / %s at d = %s: %s on [%s] -> %s' % (
                    lab, N, name, desc, R['n'], what, dh if dh <= DH_MAX else 'none <= %d' % DH_MAX, DH_MAX, N, name.upper(),
                    ', '.join('d=%s: %d' % (d if d <= DH_MAX else 'none', n_) for d, n_ in sorted(C['hist'].items())),
                    piece_str(*C['at']) if C['at'] else '-', scl, dh if dh <= DH_MAX else '-',
                    nf(wv[0]) if wv else 'n/a', piece_str(wv[1], wv[2]) if wv else '-', verdict_word(tg_, ok)))
            out('C2a.3 N=%d %s (headroom table, the rules): by d, the largest level of %s at which it holds on every piece with each input '
                'moved against it by that level (0: fails unscaled): %s; claim threshold (certified slack > 0, no headroom factor) %s; '
                'planning threshold at HR %.2f: %s; INFO the slack\'s lower end falls from d - 1 to d at %d places (the monotonicity rule predicts none)' % (
                    N, name, '/'.join('%g' % x for x in HR_LEVELS), ', '.join('d=%d %g' % (d, C['lev'][d]) for d in range(DH_MAX + 1)),
                    dh if dh <= DH_MAX else 'none', hr, dp if dp <= DH_MAX else 'none', C['mono']))
            if dh <= DH_MAX and C['lev'][dh] < hr:                         # a thin claim prints the slack it rests on
                wa = C['worst_abs'][dh]
                out('THIN N=%d %s: the claim threshold DH_N%d_%s = %d rests on its slack > 0 alone (headroom level %g < HR %.2f; the '
                    'planning threshold is %s): the smallest slack at d = %d is %s (lower end, J^2Cov units) on [%s], %s of %s at its worst '
                    'piece [%s]' % (N, name, N, name.upper(), dh, C['lev'][dh], hr, dp if dp <= DH_MAX else 'none', dh,
                                    dec_dir(wa[0], False) if wa else 'n/a', piece_str(wa[1], wa[2]) if wa else '-', nf(wv[0]) if wv else 'n/a',
                                    scl, piece_str(wv[1], wv[2]) if wv else '-'))
        R['joint_dh'] = max((R['handoff'][c][0] for c, _ in JOINT_CLASSES), default=None) if JIN is not None else None
        if not VERT and R.get('corner_pcs') and R['handoff']['mixed'][0] <= DH_MAX:       # INFO, pk15's width budget (in every
            dh = R['handoff']['mixed'][0]                                                 # full run, scan and sweep)
            cors = []
            for d in sorted({dh, min(dh + 1, DH_MAX)}):
                budget(3.0, 'corner N=%d d=%d' % (N, d))
                vs = [(flip_search(lambda x: kind_holds('mixed', Qc, Mc, Tc, d, {'corner': x}), 'mul', MCAP), a, b)
                      for a, b, Qc, Mc, Tc in R['corner_pcs']]
                vs = [v for v in vs if v[0] is not None]
                w_ = min(vs) if vs else None
                cors.append('L = %s at d = %d on [%s]' % (fmt_f(w_[0]), d, piece_str(w_[1], w_[2])) if w_ else 'never below cap at d = %d' % d)
            out('INFO C2a.CORNER N=%d mixed (sweep, the %d grid pieces; pk15\'s width budget): A_t and A_a divided together by L, pi_a '
                'recomputed, pi_t^2 raised by 2 (A_t + dt_x) A_t (1 - 1/L); the smallest flip over the pieces at the claim threshold DH_N%d_MIXED '
                '= %d and one above: %s' % (N, len(R['corner_pcs']), N, dh, '; '.join(cors)))
        if JIN is not None:                                     # the route-A rule: the joint DH from the record, no constant, printed
            got = {c: R['handoff'][c][0] for c, _ in JOINT_CLASSES}
            recd = {c: JIN['_dh'].get((c, N)) for c, _ in JOINT_CLASSES}
            dhs_ = lambda g: str(g) if g <= DH_MAX else 'none'

            def dhj_bad(rd):
                return [c for c in got if rd[c] is not None and rd[c] != dhs_(got[c])] + ['other key %s' % k for k in JIN['_dh_other']]
            dif = dhj_bad(recd)
            c0 = JOINT_CLASSES[0][0]                            # PLANT-DHJ, one class's stated DH this run's + 1
            pdhj = c0 in dhj_bad(dict(recd, **{c0: dhs_(got[c0] + 1)}))
            out('C2a.4 JOINT DH N=%d (the route-A rule: no constant; each class\'s claim threshold from the joint record\'s per-piece '
                'inputs, %s): %s; DH_N%d_OVERLAP %s; C-DHJ, the record\'s own DH keys: %s, and no other DH_ key -> %s; PLANT-DHJ (%s\'s stated '
                'DH set to this run\'s + 1 in a copy) -> %s' % (
                    N, JIN['_tag'], ', '.join('%s %s' % (c, dhs_(g)) for c, g in got.items()), N, dhs_(R['joint_dh']),
                    ', '.join('%s %s' % (c, v) for c, v in recd.items() if v is not None) or 'none (this run\'s DH stands)',
                    'AGREE' if not dif else 'FAIL (%s)' % ', '.join(dif), c0, 'FIRES' if pdhj else 'DOES NOT FIRE'))
            if dif:
                fails.append('C-DHJ N=%d' % N)
            if not pdhj:
                fires.append('PLANT-DHJ N=%d' % N)
        if R.get('s7_pcs'):                                     # INFO, the paper's all-piece S7 distances (R_w, joint group, bars)
            pcs, rooms = R['s7_pcs'], []
            (a0, b0), (al, bl) = pcs[0], pcs[-1]
            for lab in ('R_w', JOINT, '19.1c bars, all'):
                _, mk, kind, cap, _, _ = GMAP[lab]
                budget(3.0, 'S7 room N=%d %s' % (N, lab))
                F0 = flip_search(lambda x: verdict_one(inp, a0, b0, mk(x), 'S7'), kind, cap)
                Fl = flip_search(lambda x: verdict_one(inp, al, bl, mk(x), 'S7'), kind, cap)
                low = []                                        # verdict monotone in the hook: a piece that holds at F0/1.004 flips above
                for a, b in (pcs[1:] if F0 else ()):            # it, so without a failing piece the minimum lies in [F0/1.004, F0]
                    if not verdict_one(inp, a, b, mk(F0 / 1.004), 'S7'):
                        low.append((flip_search(lambda x: verdict_one(inp, a, b, mk(x), 'S7'), kind, cap), a, b))
                cand = [(F0, a0, b0)] + [v for v in low if v[0] is not None] if F0 else []
                w_ = min(cand) if cand else None
                rooms.append('%s: min %s on [%s] (%d of %d other pieces fail at the first piece\'s flip / 1.004); last piece %s' % (
                    lab, fmt_f(w_[0]) if w_ else 'never below cap', piece_str(w_[1], w_[2]) if w_ else '-', len(low), len(pcs) - 1,
                    fmt_f(Fl)))
            out('INFO S7 ROOM N=%d (sweep, the %d grid pieces, naive enclosures as the scan\'s; the paper\'s all-piece S7 distances to '
                'flip): %s' % (N, len(pcs), '; '.join(rooms)))
        out('INFO C-ORDER N=%d: the L1 centered form fell back to the naive bound (minimizing row or positivity not certified) on %d of %d '
            'pieces; centered forms that met a kink or a non-finite D(P) and kept the naive bound: %d' % (N, R['ofb'], R['n'], R.get('kink', 0)))
        out('INFO-HARM N=%d: rho on the last piece [%s] %s (harmonic odd 2-phonon lambda_z/lambda_0 = 0.0797)' % (
            N, piece_str(*PCS[-1]), nf(R['last_rho'])))
        tau4_summary(N)                                                     # PK21: kill test (i)
        okr = R['rep'][0] <= TOL_B and not R['viol'] and R['covsame']
        out('C-REPRO300 N=%d: path A on %d sampled pieces: worst relative B-A %.2e (%s); production forms never better than A: %s; claimed-pair '
            'coverage %s -> %s' % (N, R['nrep'], R['rep'][0], R['rep'][1], 'yes' if not R['viol'] else 'NO (%s)' % ', '.join(R['viol'][:6]),
                                   'identical' if R['covsame'] else 'DIFFERS', 'PASS' if okr else 'FAIL'))
        if not okr:
            fails.append('C-REPRO300 N=%d' % N)
        for (Jlo, Jhi) in (PCS[0], PCS[-1]):
            E = piece_eval(inp, Jlo, Jhi, {}, full=True)
            Q, Mq, S5 = E['Q'], E['Mq'], E['S5']
            g6 = nf
            out('INFO N=%d [%s]: c5 %s (even %s, odd %s, vacT %s); R+ %s, rho %s, rho1 %s, R_w %s, |v+| %s, |v-| %s, ||B+|| %s, ||B-|| %s; '
                'q_x %s, L2 %s, mu_x %s, alpha^2 %s, |a_x| %s, c_x %s, r2 %s, ro %s; full coverage: %s' % (
                    N, piece_str(Jlo, Jhi), g6(S5['c5']), g6(S5['even'].a), g6(S5['odd'].b), g6(S5['vacT'].b), g6(Q['Rp']), g6(Q['rho']),
                    g6(Q['rho1']), g6(Q['Rw']), g6(Q['vp']), g6(Q['vm']), g6(Q['nBp']), g6(Q['nBm']), g6(Mq['qx']), g6(Mq['L2']), g6(Mq['mux']),
                    g6(Mq['al2']), g6(Mq['ax']), g6(Mq['cx']), g6(Mq['r2']), g6(Mq['ro']),
                    '; '.join('%s d=%d: Jensen m<=%d, mode m>=%d' % (p[0], p[1], E['cv'][p][0], E['cv'][p][1] + 1) for p in CLAIM[N])))

    STAGE[0] = 'C-GRID-ALL'                 # TIN, JIN and the export rows pair by the pieces() index; check every pair
    jg = joint_grid()

    def grid_bad(rows):
        return (['N%d: %d rows, %d grid pieces' % (N, len(rows[N]), len(jg)) for N in (4, 3) if len(rows[N]) != len(jg)]
                + ['N%d_P%04d' % (N, i) for N in (4, 3) for i, row in enumerate(rows[N][:len(jg)]) if tuple(row.split(' ')[:2]) != jg[i]])
    gbad = grid_bad(EXPORT_ROWS)
    sw = {N: list(EXPORT_ROWS[N]) for N in (4, 3)}
    sw[4][0], sw[4][1] = sw[4][1], sw[4][0]
    gfired = any(b.startswith('N4_P0000') for b in grid_bad(sw))
    out('C-GRID-ALL: every export row\'s jlo, jhi (fields 1-2) against the pinned grid (v2_2\'s export %s, joint_grid: the '
        'grid of pk15\'s records, which their readers hold to it string for string), both N, %d pieces each, the lengths equal -> %s; '
        'PLANT-GRID-ALL (N4 rows 0 and 1 swapped in a copy) -> %s' % (V22_EXPORT[1][:8], len(jg), 'PASS' if not gbad else
                                                                       'FAIL (%s)' % ', '.join(gbad[:6]), 'FIRES' if gfired else 'DOES NOT FIRE'))
    if gbad:
        fails.append('C-GRID-ALL')
    if not gfired:
        fires.append('PLANT-GRID-ALL')

    STAGE[0] = 'C-PIECE, C-UNIF'
    for N in (4, 3):
        R = res[N]
        binding = []
        for pc in (PCS[0], (R['w5'][1], R['w5'][2]), (R['w6'][1], R['w6'][2]), PCS[-1]):
            if pc not in binding:
                binding.append(pc)
        tbad, wn, ubad, mbad = [], (-1.0, ''), [], []
        for (Jlo, Jhi) in binding:
            budget(5.0, 'C-PIECE, C-UNIF, C-MV-B N=%d' % N)
            b_, w, k = piece_check(INP[N], Jlo, Jhi)
            tbad += ['%s on [%s]' % (x, piece_str(Jlo, Jhi)) for x in b_]
            if w > wn[0]:
                wn = (w, '%s on [%s]' % (k, piece_str(Jlo, Jhi)))
            ubad += ['%s on [%s]' % (x, piece_str(Jlo, Jhi)) for x in unif_check(Ctx(INP[N], Jlo, Jhi, {}))]
            E = piece_eval(INP[N], Jlo, Jhi, {})
            mbad += ['%s on [%s]' % (x, piece_str(Jlo, Jhi)) for x in mvb_check(E['cx'], E['Ub'], E['V'])]
        ok = not tbad and wn[0] <= 1e-15
        out('C-PIECE N=%d: %d binding pieces halved, naive enclosures (the piece\'s preconditioner, vacuum point and index order): terms '
            'outside the parent %d%s; parent against its end and midpoint values included; largest outward move of a final bound %.2e (%s) '
            '-> %s' % (N, len(binding), len(tbad), (' (%s)' % ', '.join(tbad[:4])) if tbad else '', wn[0], wn[1], 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-PIECE N=%d' % N)
        out('C-UNIF N=%d: the same pieces, every stored entry, U and m-hat against 9 points each -> %s' % (
            N, 'PASS' if not ubad else 'FAIL (%s)' % ', '.join(ubad[:6])))
        if ubad:
            fails.append('C-UNIF N=%d' % N)
        out('C-MV-B N=%d: the same pieces, 4 smooth forms at 9 points, delta = 0 and the two gradient-sign corners of B -> %s' % (
            N, 'PASS' if not mbad else 'FAIL (%s)' % ', '.join(mbad[:6])))
        if mbad:
            fails.append('C-MV-B N=%d' % N)

    STAGE[0] = 'PLANT-RIGHTEND, PLANT-MV, PLANT-MVB'
    Jlo, Jhi = PCS[0]
    bad = unif_check(Ctx(INP[4], Jlo, Jhi, {'right_end': True}))
    tb, _, _ = piece_check(INP[4], Jlo, Jhi, {'right_end': True})
    fired = bool(bad) and bool(tb)
    out('PLANT-RIGHTEND (N=4, [%s]): the piece\'s t replaced by its right end in J -> C-UNIF fails on %d names, C-PIECE on %d terms -> %s' % (
        piece_str(Jlo, Jhi), len(bad), len(tb), 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-RIGHTEND')
    E = piece_eval(INP[4], Jlo, Jhi, {})
    bad = mv_check(E['cx'], E['Ub'], zero_derivative=True)
    out('PLANT-MV (N=4, [%s]): D_c(P) replaced by 0 -> C-MV fails on %s -> %s' % (
        piece_str(Jlo, Jhi), ', '.join(bad) if bad else 'nothing', 'FIRES' if bad else 'DOES NOT FIRE'))
    if not bad:
        fires.append('PLANT-MV')
    bad = mvb_check(E['cx'], E['Ub'], E['V'], bar_free=True)
    fired = 'S5 Dd' in bad                                  # N-b: judged on S5 Dd, where the bars enter at full weight
    out('PLANT-MVB (N=4, [%s]): F(t_m) evaluated with B = 0 -> C-MV-B fails on %s; S5 Dd among them: %s -> %s' % (
        piece_str(Jlo, Jhi), ', '.join(bad) if bad else 'nothing', fired, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        fires.append('PLANT-MVB')

    STAGE[0] = 'KILL (sweep part)'
    kr1 = all((res[N]['w6'][0] >= 1.05) is True for N in (4, 3))
    out('KILL KR1 (S6 R+/rho >= 1.05 on every piece): N=4 %s, N=3 %s -> %s' % (
        nf(res[4]['w6'][0]), nf(res[3]['w6'][0]), 'PASS' if kr1 else 'KILL'))
    kr3, kr4 = s4_kr34(INP, fails)              # F2, D-2: KR3 and KR4 are gates in this item too (its U and TRB are the certified ones)
    STAGE[0] = 'KILL (sweep part)'
    kr5a = all((res[N]['w5'][0] > 0) is True for N in (4, 3))
    out('KILL KR5a, sweep part (c5 > 0 on every piece): N=4 %s, N=3 %s -> %s (the joint-headroom part is in the scan item)' % (
        nf(res[4]['w5'][0]), nf(res[3]['w5'][0]), 'PASS' if kr5a else 'KILL'))
    tg = {N: pt(INP[N]['P']['cov1']) / 1.51 for N in (4, 3)}
    kr5b = all((res[N]['w5'][0] >= tg[N]) is True for N in (4, 3))
    out('KILL KR5b (c5 >= v1_1\'s S5 target Cov_1/1.51 = %s at N=4, %s at N=3) -> %s' % (
        nf(tg[4], 4), nf(tg[3], 4), 'PASS' if kr5b else 'FAIL: nothing claimed for S7 until it is re-run with C_1 = c5'))
    out('KILL RULE, sweep part: %s' % ('no kill (KR1, KR3, KR4, KR5a part, KR5b pass)' if (kr1 and kr3 and kr4 and kr5a and kr5b)
                                       else 'KILL: stop and report'))
    STAGE[0] = 'C-VERT (P2-11)'
    vbad = c_vert(fires)
    nv = sum(len(r) for r in VERT_ROWS.values())
    out('C-VERT (P2-11): the fork\'s %d export rows (%s) against v2_2\'s export (%s, sha256 %s), key for key and string for string: %s -> '
        '%s; PLANT-VERT (one row with a digit moved) -> %s' % (
            nv or sum(len(r) for r in EXPORT_ROWS.values()), 'on v2_2\'s inputs, the sampled pieces; the production rows read the M3 '
            'provider\'s records' if nv else 'this vertical sweep', V22_EXPORT[0], V22_EXPORT[1][:8],
            'identical' if not vbad else '%d differ (%s)' % (len(vbad), ', '.join(vbad[:4])), 'PASS' if not vbad else 'FAIL',
            'DOES NOT FIRE' if 'PLANT-VERT' in fires else 'FIRES'))
    if vbad:
        fails.append('C-VERT')
    return res


# ------------------------------------------------------------------ item scan: plants at [300, 303], distances to flip, targets
def item_scan(INP, fails, fires):
    J3, J3h = 300.0, 303.0                      # S1: E6's fixed plants (U + 1.3e-3, R_w x 1.30, TRB x 1.50) give way to margin_plant
    STAGE[0] = 'SCAN [300, 303]'
    scan = {}
    for N in (4, 3):
        for lab, mk, kind, cap, lane, app in GROUPS:
            for which in app.split():
                budget(4.0, 'SCAN N=%d %s %s' % (N, which, lab))
                scan[(N, which, lab)] = flip_search(lambda x: verdict_one(INP[N], J3, J3h, mk(x), which), kind, cap)
    for lab, mk, kind, cap, lane, app in GROUPS:
        out('SCAN [300, 303] %-36s part %-3s: %s' % (lab, lane, '; '.join(
            '%s N%d %s' % (w, N, fmt_f(scan[(N, w, lab)])) for N in (4, 3) for w in app.split())))
    out('INFO SCAN base: these distances, here and on the last piece, are measured from the certified S4 values: '
        '\'Lemma 19.4 rem\' and the joint group scale R_CERT (not rem(170)), \'U raised by (absolute)\' adds to the certified U(t), '
        '\'TRB (beta)\' scales the certified TRB; the M3 and M2 inputs are their providers\' (TAGS: %s, %s), M2 through LAW v1, which alone '
        'reads the Z2 and Rtr hooks. They read as headroom over those values.' % (TAGS['M3 entries'], TAGS['M2 vacuum']))
    STAGE[0] = 'SCAN last piece'
    PL = pieces()[-1]
    scanL = {}
    for N in (4, 3):
        for lab, which in LAST_GROUPS:
            budget(4.0, 'SCAN last N=%d %s %s' % (N, which, lab))
            _, mk, kind, cap, _, _ = GMAP[lab]
            scanL[(N, which, lab)] = flip_search(lambda x: verdict_one(INP[N], PL[0], PL[1], mk(x), which), kind, cap)
    out('SCAN last piece [%s]: %s' % (piece_str(*PL), '; '.join(
        '%s %s N%d %s' % (lab, w, N, fmt_f(scanL[(N, w, lab)])) for lab, w in LAST_GROUPS for N in (4, 3))))

    STAGE[0] = 'margin plants (S1, D2)'
    out('INFO margin plants (S1, D2): F is the scan\'s flip on [300, 303]: bracket [1, 2] doubled up to %g (factors) or [0, 1e-4] '
        'doubled up to 1.0 (U, additive), then bisection to relative 0.4%% (hi/lo <= 1.004, or hi - lo <= 0.004 hi); each plant needs a '
        'hold at F / 1.1 and a loss at 1.1 F' % MCAP)
    for N in (4, 3):                                            # S1: E6's margins, self-calibrating, on the scan's binding piece per N
        for lab, key in (('U raised by (absolute)', 'U'), ('R_w', 'RW'), ('TRB (beta)', 'TRB')):
            budget(2.0, 'PLANT-%s N=%d' % (key, N))
            F = scan[(N, 'S7', lab)]
            fired = margin_plant(INP[N], J3, J3h, GMAP[lab][1], F, 'S7')
            out('PLANT-%s N=%d ([300, 303], S7 claimed coverage, %s): flip F = %s; holds at F / 1.1 and is lost at 1.1 F -> %s' % (
                key, N, lab, fmt_f(F), 'FIRES' if fired else 'DOES NOT FIRE'))
            if not fired:
                fires.append('PLANT-%s N=%d' % (key, N))
    d3 = ('flip', 3)                                            # D2: the d = 3 binding direction at N = 4
    for lab, key in (('C_1 = c5 (divided by)', 'C1'), ('19.1c bars, all', 'BARS')):
        budget(2.0, 'PLANT-D3-%s' % key)
        F = scan[(4, 'S7', lab)]
        fired = d3 in CLAIM[4] and margin_plant(INP[4], J3, J3h, GMAP[lab][1], F, 'S7', lose=(d3,))
        out('PLANT-D3-%s (N=4, [300, 303], %s): flip F = %s of the claim %s; the claim holds at F / 1.1 and the pair flip d=3 is lost at '
            '1.1 F -> %s' % (key, lab, fmt_f(F), ', '.join('%s d>=%d' % p for p in CLAIM[4]), 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            fires.append('PLANT-D3-%s' % key)

    STAGE[0] = 'ADD1 plants'
    for N in (4, 3):
        for lab, key in (('19.1c bar N_delta', 'bar_Ndel'), ('TRB (beta)', 'TRB')):
            F, inp_p, where = scan[(N, 'S5', lab)], INP[N], ''
            if F is None and key == 'bar_Ndel' and INP[N].get('m3_cert'):    # a certified bar too small to flip S5 below the cap: the
                inp_p, where = float_m3(INP[N]), ' on the FLOAT M3 copy (the certified N_delta bar never flips S5 below the cap)'
                _, mk_, kind_, cap_, _, _ = GMAP[lab]                          # plant then shows the hook path on FLOAT bars
                F = flip_search(lambda x: verdict_one(inp_p, J3, J3h, mk_(x), 'S5'), kind_, cap_)
            fired = margin_plant(inp_p, J3, J3h, GMAP[lab][1], F, 'S5')       # shared with S1 (a missing flip does not fire)
            out('PLANT-S5 %s N=%d ([300, 303]%s): S5 holds at %s / 1.1 and fails at x 1.1 -> %s' % (
                key, N, where, fmt_f(F), 'FIRES' if fired else 'DOES NOT FIRE'))
            if not fired:
                fires.append('PLANT-S5 %s N=%d' % (key, N))

    STAGE[0] = 'C-FLIP170'
    J0, J0h = 170.0, 170.0 * 1.01
    for N in (4, 3):                                            # D1: the own claim and C_1 = Cov_1, path A's FLOAT U and TRB
        inf_ = float_s4(INP[N])
        okall, n_ = True, 0
        for fname, which in (('pk20/rv13/c5/rc_m2_sens_N%d.txt' % N, 'S6'), ('pk20/rv13/c6/rc_end_sens_N%d.txt' % N, 'S7')):
            txt = open(os.path.join(CODEDIR, fname)).read()
            if which == 'S6':
                rows = re.findall(r'^(.+?) +flips at (> )?([0-9.e+-]+)\s*$', txt, re.M)
            else:
                rows = [(lab.strip(), '', v) for lab, v in re.findall(
                    r'^  ((?:R_w|\|\|B\+\|\|, \|\|B-\|\||c_x|Cov_1) [x/]|U raised by) +([0-9.e+-]+)', txt, re.M)]
            for lab, gt, val in rows:
                lab = lab.strip()
                if lab not in REVMAP:
                    okall = False
                    out('  C-FLIP170 N=%d: unmapped label %r' % (N, lab))
                    continue
                budget(4.0, 'C-FLIP170 N=%d %s' % (N, lab))
                mk, kind, cap = REVMAP[lab]
                f = flip_search(lambda x: verdict_one(inf_, J0, J0h, dict(mk(x), author_forms=True, C1_const=True), which,
                                                      claim=FLIP170_CLAIM[N]), kind, cap)
                v = float(val)
                ok = (f is None or f > v) if gt else (f is not None and abs(f / v - 1) <= 0.01)
                okall = okall and ok
                n_ += 1
                out('  C-FLIP170 N=%d %s %-45s reference %s%s, mine %s -> %s' % (N, which, lab, gt, val, fmt_f(f), 'ok' if ok else 'DIFFERS'))
        out('C-FLIP170 N=%d (the claim %s, C_1 = Cov_1): %d distances to flip against the reference values -> %s' % (
            N, ', '.join('%s d>=%d' % p for p in FLIP170_CLAIM[N]), n_, 'PASS' if okall else 'FAIL'))
        if not okall:
            fails.append('C-FLIP170 N=%d' % N)
    d3txt = open(os.path.join(CODEDIR, D3_REF)).read().split('\n')       # D1, INFO: the d = 3 distances against NOTE1_d3's recorded run
    reg = []
    for lab in ('19.1c bars, all', JOINT, 'C_1 = c5 (divided by)', 'vacuum, all', 'U raised by (absolute)', 'TRB (beta)', 'R_w', '||B+-||',
                'c_x (divided by)'):
        ms = [m for m in (re.fullmatch(r'SCAN \[300, 303\] %s +part [^:]*: (.*)' % re.escape(lab), ln) for ln in d3txt) if m is not None]
        rv = re.search(r'(?:^|; )S7 N4 ([^;]+)', ms[0].group(1)) if len(ms) == 1 else None
        reg.append('%s %s (recorded %s)' % (lab, fmt_f(scan[(4, 'S7', lab)]), rv.group(1) if rv else 'not found'))
    ms = [m for m in (re.search(r'%s S7 N4 ([^;]+)' % re.escape(JOINT), ln) for ln in d3txt if ln.startswith('SCAN last piece')) if m]
    reg.append('last piece %s %s (recorded %s)' % (JOINT, fmt_f(scanL[(4, 'S7', JOINT)]), ms[0].group(1) if len(ms) == 1 else 'not found'))
    out('INFO C-FLIP170 d=3 (D1): S7 N=4 under the production claim %s, distances to flip now, measured from the certified S4 values '
        '(N-d), against NOTE1_d3\'s recorded run (%s, sha8 %s, all inputs FLOAT then; differences from this change of base are expected '
        'and are not a C-FLIP170 failure): %s' % (', '.join('%s d>=%d' % p for p in CLAIM[4]), D3_REF, FILES[D3_REF], '; '.join(reg)))

    STAGE[0] = 'C-TARGETS'
    ct = c_targets(INP)
    cert = certified_inputs()
    for (lam, N), (okt, w5, w6, badn, badp) in sorted(ct.items()):
        out('C-TARGETS lambda=%.2f N=%d (every FLOAT input at lambda x its v1_2 target excess, every certified input at its certified '
            'value: %s; every piece): naive enclosures fail on %d pieces%s; with the production forms there %s; min c5 %s on '
            '[%s], min R+/rho %s on [%s]' % (
                lam, N, tgt_text(lam, cert), len(badn),
                (' (J from %s)' % ', '.join('%.1f' % x for x in badn[:6])) if badn else '',
                'ALL HOLD' if okt else 'FAIL on %d pieces (J from %s)' % (len(badp), ', '.join('%.1f' % x for x in badp[:6])),
                nf(w5[0]) if w5 else 'n/a', piece_str(w5[1], w5[2]) if w5 else '-', nf(w6[0]) if w6 else 'n/a',
                piece_str(w6[1], w6[2]) if w6 else '-'))

    STAGE[0] = 'TARGETS'
    out('TARGETS v1_2 (SPEC sect. 3, the set T2, every input at its target at once): M3 bars, M2 vacuum and P3 eps_w <= x%.3f; S4 U: '
        'certified U - float U <= %.2g (rem included; S4-U from its provider here, see KR4); S4-TRB: certified TRB <= x%.2f (N=4 %.6f, '
        'N=3 %.6f; S4-TRB from its provider here, see KR4); S5: computed here' % (                # N-c (v2_1): "pending" dropped
            TGT['err'], TGT['U'], TGT['TRB'], float(INP[4]['P']['TRB']) * TGT['TRB'], float(INP[3]['P']['TRB']) * TGT['TRB']))

    def fmin(lab):
        v = [x for d_ in (scan, scanL) for (N, w, l_), x in d_.items() if l_ == lab and x is not None]
        return min(v) if v else None
    for lab, mk, kind, cap, lane, app in GROUPS:
        out('INFO headroom (single input, smallest over the scanned verdicts and pieces) %-36s part %-4s: %s' % (lab, lane, fmt_f(fmin(lab))))

    STAGE[0] = 'KILL (scan part)'
    hR, hB = scan[(4, 'S7', 'R_w')], scan[(4, 'S7', '||B+-||')]
    kr2 = (hR is None or hR >= 1.05) and (hB is None or hB >= 1.05)
    out('KILL KR2 (N = 4 headroom in R_w and ||B+-|| >= 1.05 at [300, 303]): %s, %s -> %s' % (fmt_f(hR), fmt_f(hB), 'PASS' if kr2 else 'KILL'))
    kr3, kr4 = s4_kr34(INP, fails)              # F2, D-2: KR3 and KR4 are gates once S4-U (and S4-TRB) are certified
    STAGE[0] = 'KILL (scan part)'
    j5 = {N: scan[(N, 'S5', JOINT)] for N in (4, 3)}
    kr5a = all(v is None or v >= 1.5 for v in j5.values())
    out('KILL KR5a, scan part (S5 joint headroom >= 1.5 at [300, 303]): N=4 %s, N=3 %s -> %s (the c5 > 0 part is in the sweep item)' % (
        fmt_f(j5[4]), fmt_f(j5[3]), 'PASS' if kr5a else 'KILL'))
    krj = all(ct[key][0] for key in ct)
    out('KILL KR-J (C-TARGETS holds at lambda = 1 and 1.25 on every piece, both N): %s' % ('PASS' if krj else 'FAIL: re-split the targets'))
    out('KILL RULE, scan part: %s' % ('no kill (KR2, KR3, KR4, KR5a part, KR-J pass)' if (kr2 and kr3 and kr4 and kr5a and krj)
                                      else 'KILL or FAIL: stop and report'))


# ------------------------------------------------------------------ C-VERT-ONLY (v1_2, the certified vertical mode reads no S_TB' input)
def vert_only_bad(reads, unread, sh1, jin, tin):
    """C-VERT-ONLY: in the VERTICAL mode no S_TB' provider ran (reads: STB_READS), the module-level C-HASH left every FILES_STB file
    unopened (unread: STB_UNREAD), and SH1, the joint inputs and the t inputs do not exist. Returns the failures."""
    bad = ['%s ran' % r for r in reads]
    bad += ['%s opened' % f for f in sorted(FILES_STB) if f not in unread]
    return bad + ['%s present' % n for n, v in (('SH1', sh1), ('joint inputs', jin), ('t inputs', tin)) if v is not None]


def c_vert_only(sh1, jin, tin, fails, fires, when):
    """C-VERT-ONLY (v1_2) and PLANT-VERT-ONLY's three cases (a record of provide_tin having run, t inputs present, one FILES_STB
    file opened); in the full mode an INFO line naming the S_TB' providers that ran."""
    if not VERT:
        out('INFO C-VERT-ONLY %s (full mode): the S_TB\' providers run: %s' % (when, ', '.join(STB_READS) or 'none'))
        return
    bad = vert_only_bad(STB_READS, STB_UNREAD, sh1, jin, tin)
    one = sorted(FILES_STB)[0]
    pl = (('provide_tin ran', vert_only_bad(STB_READS + ['provide_tin'], STB_UNREAD, sh1, jin, tin)),
          ('t inputs present', vert_only_bad(STB_READS, STB_UNREAD, sh1, jin, {'planted': True})),
          ('%s opened' % one, vert_only_bad(STB_READS, STB_UNREAD - {one}, sh1, jin, tin)))
    fired = all(len(b) > len(bad) for _, b in pl)
    out('C-VERT-ONLY %s (the certified vertical mode reads no S_TB\' input): S_TB\' providers run: %s; the %d FILES_STB files left '
        'unopened by C-HASH: %s; SH1, joint and t inputs: %s -> %s; PLANT-VERT-ONLY (%s) -> %s' % (
            when, ', '.join(STB_READS) or 'none', len(FILES_STB), 'yes' if FILES_STB <= STB_UNREAD else 'NO',
            'none' if (sh1 is None and jin is None and tin is None) else 'PRESENT', 'PASS' if not bad else 'FAIL (%s)' % ', '.join(bad),
            '; '.join(lab for lab, _ in pl), 'FIRES' if fired else 'DOES NOT FIRE'))
    if bad:
        fails.append('C-VERT-ONLY %s' % when)
    if not fired:
        fires.append('PLANT-VERT-ONLY %s' % when)


# ------------------------------------------------------------------ main
def main():
    fails, fires = [], []
    complete = False
    SH1 = JIN = TIN = SW = None
    try:
        out('MODE %s: %s' % (MODE, 'VERTICAL only (the Q2): the S5-S7 providers alone (S4-U, S4-TRB, M2(b), M3); no t, A_a, beta_H '
                                   'or joint provider is called, and the sweep writes EXPORT_KT_S67_v1 only' if VERT else
                             'full: the S5-S7 providers and S9\'s (SH1, joint, t); the sweep writes EXPORT_KT_S67_v1, checked against the '
                             'vertical run by C-VERT-MODES, and EXPORT_KT_S9H_v1'))
        STAGE[0] = 'S4-U provider'
        S4 = provide_s4u(fails, fires)          # F1, F2, S3: with provide_s4trb, the only places a tag can become certified
        STAGE[0] = 'S4-TRB provider'
        ST = provide_s4trb(fails, fires)        # v2_1
        STAGE[0] = 'M2(b) provider'
        M2B = provide_m2b(fails, fires)         # the certified snapshot: pk02's LAW v1 record (mock record until it exists)
        if not VERT:
            STAGE[0] = 'SH1 provider (P2-11)'
            SH1 = provide_sh1(fails, fires)     # P2-11: the FLOAT t inputs
            STAGE[0] = 'joint provider (P2-14)'
            JIN = provide_joint(fails, fires)   # P2-14: pk15's joint inputs, None until a record is pinned
            STAGE[0] = 't provider (certified snapshot)'
            TIN = provide_tin(SH1, fails, fires)    # the per-piece t inputs (kt_p2_assembly's export; mock record until it exists)
        STAGE[0] = 'M3 provider'
        M3 = provide_m3(fails, fires)           # the certified snapshot: M3 records through m3_reader_v4_4 (mock records until frozen)
        STAGE[0] = 'C-TRIAL'
        VAC = c_trial(M3, fails, fires)         # M3's records, and this file's m-hat, on one pinned trial set
        c_trial_chain(M3, fails, fires)         # main, pk03: record -> asm output -> script sha -> the script's four trial pins
        if not VERT and TIN is not None:
            STAGE[0] = 'beta_H provider (v1_1)'
            provide_bh(M2B, TIN, VAC, fails, fires)     # beta_H from the TRB_H record
        STAGE[0] = 'C-VERT-ONLY'
        c_vert_only(SH1, JIN, TIN, fails, fires, 'after the providers')     # v1_2: no S_TB' read in the vertical mode
        INP = {N: load(N, S4, ST, M3, M2B, VAC) for N in (4, 3)}
        NSM = {N: path_a(INP[N], 'm2u3') for N in (4, 3)}
        NSE = {N: path_a(INP[N], 'ep4') for N in (4, 3)}
        NSB = {N: path_a(INP[N], 'ab4') for N in (4, 3)}
        STAGE[0] = 'C-REPRO at [170, 171.7]'
        c_repro170(INP, NSM, NSE, NSB, fails, fires)
        STAGE[0] = 'C-C2'
        c_c2(INP, fails, fires)
        STAGE[0] = 'C-HARM, C-IP3, C-KBAR'
        c_harm(INP, fails, fires)               # v2_2 (1): with PLANT-HARM
        c_ip3(INP, fails)
        c_kbar(INP, fails, fires)               # v2_2 (2)
        STAGE[0] = 'C-PARITY, C-MODULE, C-TAG'
        c_guards(INP, fails, fires)
        STAGE[0] = 'C-FMT'
        c_fmt(INP, NSB, fails, fires)
        if not VERT:
            STAGE[0] = 'C-EXP (P2-11)'
            c_exp(fails, fires)                 # P2-11: the EXPONENT TABLE, C-EXP and PLANT-EXP
        out('controls done at cpu %.1f s' % cpu())
        if ITEM == 'sweep':
            SW = item_sweep(INP, NSM, NSE, NSB, fails, fires, SH1, JIN, TIN)
        else:
            item_scan(INP, fails, fires)
            if not VERT:
                c2a_scan(INP, SH1, TIN, fails, fires)      # P2-11 step 3: the kinds' thresholds, distances, controls and plants
                if JIN is not None:
                    joint_scan(INP, SH1, JIN, TIN, fails, fires)    # P2-14: the joint kind's part of the scan
        STAGE[0] = 'C-VERT-ONLY end'
        c_vert_only(SH1, JIN, TIN, fails, fires, 'at the end')             # v1_2: still none after the item
        STAGE[0] = 'C-ENV end'
        _env1 = env_probe()
        out('C-ENV end: %s' % ('PASS' if _env1 else 'FAIL'))
        if not _env1:
            fails.append('C-ENV end')
        out('TAGS: %s' % '; '.join('%s = %s (%s)' % (k, v, 'certified' if tag_certified(k, v) else 'not certified')     # F1
                                   for k, v in TAGS.items()))
        complete = True
    except BudgetShort as e:
        out('INCOMPLETE: the CPU budget ran short in stage %s (%s)' % (STAGE[0], e))
    except Exception as e:
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        for ln in traceback.format_exc().splitlines()[-14:]:
            out('TRACE ' + ln)
        out('VERDICT INVALID (ERROR)')
        return 1
    why = fails + ['%s did not fire' % x for x in fires] + ([] if complete else ['INCOMPLETE'])
    if ITEM == 'sweep' and complete:                                    # v2_2 (3): the per-piece export for S8, checked before it is written
        STAGE[0] = 'export (v2_2)'
        try:
            text = export_text(why)
            bad, fired = c_export(text)
            out('C-EXPORT: the export text (%d piece lines) read back before writing: the two S4U_KV_v1 readers and the producer\'s reader %s '
                '(sha256 %s: loads with the run output\'s VERDICT and EXPORT lines when CERTIFIED, else loads_noncert) against the rows, and '
                'the control (a copy with the other status gives the same rows through the other branch; loads_noncert refuses the CERTIFIED '
                'one) -> %s; PLANT-EXPORT (N4_P0000\'s c5_lo moved one unit in its last digit) -> %s' % (
                    sum(len(r) for r in EXPORT_ROWS.values()), EXPORT_READER[0], EXPORT_READER[1][:8],
                    'PASS' if not bad else 'FAIL (%s)' % ', '.join(bad[:6]), 'FIRES' if fired else 'DOES NOT FIRE'))
            if bad:
                why.append('C-EXPORT')
            if not fired:
                why.append('PLANT-EXPORT did not fire')
            if not VERT:                                                # the Q2: S8's EXPORT_KT_S67_v1 is the vertical run's
                STAGE[0] = 'C-VERT-MODES'
                vbad, vfired, vsrc, vtie = c_vert_modes(text)
                out('C-VERT-MODES (the Q2): this full sweep\'s EXPORT_KT_S67_v1 text against the vertical run\'s export (%s), every '
                    'piece line and the shared header lines, string for string -> %s; PLANT-VERT-MODES (one digit of N3\'s last piece line '
                    'moved in a copy of the vertical export) -> %s' % (
                        vsrc, 'PASS (identical)' if not vbad else 'FAIL (%s)' % ', '.join(vbad[:6]), 'FIRES' if vfired else 'DOES NOT FIRE'))
                if vtie is not None:                                    # the tie, full sha256, one fixed line for S8
                    out('VERTICAL-TIE export %s sha256 %s run_output %s sha256 %s C-VERT-MODES %s' % (
                        vtie[0], vtie[1], vtie[2], vtie[3], 'PASS' if not vbad else 'FAIL'))
                if vbad:
                    why.append('C-VERT-MODES')
                if not vfired:
                    why.append('PLANT-VERT-MODES did not fire')
                out('EXPORT_KT_S67_v1 is not written by the full mode: S8 pins the vertical run\'s export, and C-VERT-MODES ties these rows '
                    'to it')
            elif not bad and fired:
                path, sh, nl = write_export(text)
                out('EXPORT %s sha256 %s (%d lines; RUN_VERDICT %s, EXPORT_STATUS %s)' % (
                    os.path.relpath(path, CODEDIR), sh, nl, 'VALID' if not why else 'INVALID', verdict_word(TAGS, not why)))
            else:
                out('EXPORT not written (C-EXPORT or its plant failed)')
        except Exception as e:
            out('ERROR in the export at cpu %.1f s: %r' % (cpu(), e))
            why.append('EXPORT ERROR')
    if ITEM == 'sweep' and complete and not VERT:
        STAGE[0] = 'C2-a export (P2-11 step 6)'
        try:
            names = [k for k, _ in KINDS] + ([c for c, _ in JOINT_CLASSES] if JIN is not None else [])
            text2 = export_c2a_text(SW, SH1, JIN, TIN, why)
            bad2, fired2 = c_export_c2a(text2, SW, names)
            out('C-EXPORT2 (P2-11 step 6): the C2-a export text (%d piece lines) read back before writing: the two S4U_KV_v1 readers, every '
                'DH key present (integer or none), every piece line\'s groups (%s) and C-DMIN (every piece\'s own threshold <= its '
                'header DH) -> %s; PLANT-EXPORT2 (N4_P0000\'s first dmin set to none) and PLANT-EXPORT2-DH (the first DH_N4_<K> line dropped) '
                '-> %s' % (sum(len(r) for r in EXPORT_ROWS.values()), ', '.join(names),
                           'PASS' if not bad2 else 'FAIL (%s)' % ', '.join(bad2[:6]), 'BOTH FIRE' if fired2 else 'NOT BOTH FIRE'))
            if bad2:
                why.append('C-EXPORT2')
            if not fired2:
                why.append('PLANT-EXPORT2 or PLANT-EXPORT2-DH did not fire')
            if not bad2 and fired2:
                path2, sh2, nl2 = write_export_c2a(text2)
                out('EXPORT C2A %s sha256 %s (%d lines; RUN_VERDICT %s)' % (os.path.relpath(path2, CODEDIR), sh2, nl2,
                                                                            'VALID' if not why else 'INVALID'))
            else:
                out('EXPORT C2A not written (C-EXPORT2 or its plant failed)')
        except Exception as e:
            out('ERROR in the C2-a export at cpu %.1f s: %r' % (cpu(), e))
            why.append('EXPORT C2A ERROR')
    out('ITEM %s cpu %.1f s, peak resident memory %.0f MiB' % (MODE, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
    out('NOTE the VERDICT line below is run validity (controls, plants and completeness); results read CERTIFIED only when every input '
        'tag is certified, FLOAT-PASS otherwise')
    out('VERDICT %s' % ('VALID' if not why else 'INVALID (%s)' % ', '.join(why)))   # T48 format: a bare verdict, the note above
    return 0


if __name__ == '__main__':
    sys.exit(main())
