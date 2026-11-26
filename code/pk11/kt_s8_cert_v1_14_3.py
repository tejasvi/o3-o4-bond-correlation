#!/usr/bin/env python3
"""kt_s8_cert_v1_14_3.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_14_2.py (c1cf041a; its mock pre 1325b553 read VERDICT
INVALID on PLANT-U N=4 alone, and its chunk N4 [61,63) c5701d29 VALID). This is the cert-run version:
- (D16 N3) pk03's certified D16 records for N = 3 (m3_run_v1_9_3's asm.3, VERDICT VALID; pk03's pins of 2026-11-08):
  m3_s8v2_H_N3_J300_v1_9_3.json (66a7883d, 8 keys) and m3_s8v2_S4_N3_J300_v1_9_3.json (0f83c894, 18 keys), their asm output
  out/m3_run_v1_9_3_asm.3.out (358c2c92) and the freeze side manifest MANIFEST_m3_run_v1_9_3_N3_RECORDS.sha256 (209e65e0, 134 files,
  sha256sum -c --strict OK), pinned by full sha256 and read as N4's (m3_reader_v6_3, layer arbeng_ma_v1_4_1). With both N pinned, cert
  mode is enabled (D16_PINNED).
- (PLANT-U) calib's option in_domain, passed by PLANT-U only:
  the hold is checked at F/1.1 when F > 1.1, else at sqrt(F), strictly between 1 and F (1.002 at N4 piece 61, inside the bisection's
  passing side). U's domain starts at the certified U_hi: below the B chain's in-span trace route (b) has no bound (tau_B =
  (U/lambda_0^2 - 1 - |R_B|_F^2)/2 <= 0), so U x F/1.1 with F < 1.1 leaves the evaluation's domain (v1_14_2's mock pre met it at N4
  piece 61: the binding row (1,2,flip,1) loses Cov_lo > 0 at U x 1.004, and at U x 0.913 route (b) has no bound), while max(1, F/1.1)
  would only re-read calib's precondition f_ok(1) and fire even on an evaluation that fails at every perturbed U. A plant changes no
  bound, so nothing is widened; the plant still fires only if the binding row fails at 1.1 F. PLANT-TAUB keeps F/1.1 (its F = 1.079 at
  N4 piece 61, F/1.1 inside tau's domain). The gap itself is not calibrated: that would duplicate PLANT-TAUB.
- (U_hi's fragility, on record) route (b)'s tau at N4 piece 61 rests on a gap U_hi/lambda_0^2 - 1 - |R_B|_F^2 of 2.1e-4 (tau_B
  1.07e-4), and the piece fails at tau_B x 1.079 (PLANT-TAUB). So a relative increase of about 1.7e-5 in U_hi, from pk08's
  S4_U_CERTIFIED_v3 (e870cbe5), would fail the piece; S4-U's own remainder R_CERT is 4.7e-5 of U_hi there. S8's U_hi read
  is exact (the record's decimals as Fractions, 256-bit balls, the F2 form at the piece's t ball, whose coefficients are all > 0, and
  tau_B at its upper end; the only outward steps are 256-bit roundings), so the 1.7e-5 is the record's margin: the certified U_hi
  makes the bound sound, but S4-U must never be loosened. INFO lines, so any re-certification of S4-U shows its
  effect at once: TAUB, wherever it runs (the pre item's pieces, the final's binding pieces), prints per piece the gap, the break-even
  U factor 1 + 2 (TAUB - tau_B) / (U_hi/lambda_0^2) (tau_B grows by x U_hi/(2 lambda_0^2) when U_hi grows by 1 + x) and R_CERT/U_hi;
  the final prints per N the smallest factor over its binding pieces (TAUB-U MIN); TAU-GAP (the pre item, per N at the binding piece)
  prints the gap, the factor from PLANT-TAUB's F, R_CERT/U_hi and PLANT-U's factor.
- C-NSCOPE's line names the core it reads by CORE's base name (it said s8core_v1_9). PLANT-SIDEBAD-SHA and
  PLANT-SIDEBAD-DROP: side_bad on the D16 N4 side manifest's text with the H record's sha256 changed must report it, and with the H
  record's line dropped must report the record unlisted (side_bad takes the manifest text as an option, for the plants only).
- The stale note naming S4_U_CERTIFIED_v2 (b1b6b99b) in v1_9's notes now says that v3 (e870cbe5) replaced it.
Everything else is v1_14_2; v1_14_2's docstring follows.
kt_s8_cert_v1_14_2.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_14_1.py (9e990130; mock pre c17e551e and chunk
d980a1c5 VALID): the D16 pins for N = 4, the one certified M3 reader, and C-PREC (the word of 2026-11-08):
- (D16) pk03's certified D16 records for N = 4 (m3_run_v1_9_3's asm.4, VERDICT VALID; pk03's report of 2026-11-08):
  out/m3_s8v2_H_N4_J300_v1_9_3.json (c6acd6a1; 8 keys, h,2 an exact parity zero) and out/m3_s8v2_S4_N4_J300_v1_9_3.json (c26e8d78;
  18 keys), their asm output out/m3_run_v1_9_3_asm.4.out (591745af) and the freeze side manifest MANIFEST_m3_run_v1_9_3_N4_RECORDS.sha256
  (f8641958; 136 files), every one pinned by its full sha256. rb_entries reads each record by load(path, asm.4, 300, 4), the reader's
  certified entry point (VERDICT lines exactly ['VERDICT VALID'], the RECORD line's sha256, the validated layer arbeng_ma_v1_4_1 and
  claim_ball, every free entry's laws checked), with C-TRIAL on each record and C-SIDEMAN against the side manifest. The records carry
  no law certificate, so their entries enter with laws None and their certified bars, as the MOCK H and S4 entered. They are read in
  both modes (D16_CERT_IN_MOCK, as M2(b) and P2 since v1_12_1 and v1_12_2): in the mock run N4's H and S4 are the certified ones and
  only N3's stay MOCK (every bar times the D16 floor). PLANT-D16-ASM: the H record with route (b)'s asmP output must be refused.
- (reader) every route (b) record and law certificate is read through pk03's m3_reader_v6_3 (628d2059), the one certified M3
  path agreed for the D16 records (pk11, 2026-11-08 01:14Z): v6_2 with the validated layer arbeng_ma_v1_4_1 (the D16 writer's)
  beside v6_2's arbeng_ma_v1_3 (route (b)'s m3_run_v1_8 records) and the claim_ball check; everything else is v6_2's.
- Cert mode needs the D16 records of both N (D16_PINNED); N3's follow from pk03 in a pins-only revision.
- (C-PREC) python-flint's ctx.prec is process-global, and a module that sets it at import changes every later arb operation
  (pk02's finding: m2b_reader_v1.py l.46 sets 256). This run sets ctx.prec = 256 before any module load. Every module it loads,
  grepped at freeze for ctx.prec / ctx.dps assignments (and ctx.cap, mpmath precision):
  - pk03/m3_reader_v6_3.py 628d2059: none (stdlib imports only; KERNEL_PREC = 512 at l.86 is a constant compared with a record's
    layer field at l.280, not a precision setting);
  - pk03/m3_reader_v4_4.py a5ba5c80: none (KERNEL_PREC likewise, l.48);
  - pk07/kt_s67_export_reader_v2_1.py b0a23237: none;
  - pk07/s4u_kv_ref_v1.py ce0ba6f4: none;
  - s8core_v1_11.py c82036d8: none (imports flint's arb only);
  - mocks/m2b_reader_v1_mock.py 0383cf9d: none;
  - pk02/m2b_reader_v1.py 3580bce7: ctx.prec = 256 at l.46, equal to the run's (loaded inside the M2(b) read in cert mode).
- _module() logs every load that changes ctx.prec (PREC_LOG; the change is not undone). C-PREC, at the end of every item, gates
  ctx.prec == 256 with an empty log and prints both; the final item refuses to write the record if that predicate fails before the
  write; PLANT-PREC (pre) checks that the predicate refuses ctx.prec 512 and a logged change.
Everything else is v1_14_1; v1_14_1's docstring follows.
kt_s8_cert_v1_14_1.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_14.py (edb80f3e; not run), still mock runs
only (cert mode waits for the D16 pins). The review of v1_13 (DELTA_KT_S8_CERT_V1_13_rv01.md c17ba702: SOUND) suggested in its
item (c) a cheap improvement of C-MV-S83: Cov J^2 = XY/Z - X Y/Z^2 has sensitivities of mixed sign, so the all-upper and all-lower
modes do not reach its extremes; add per pair the two gradient-sign corners. s83_piece now also evaluates, at each sample t, the
corners G+ and G- (every entry's coefficients and bar offset at the end its sensitivity points to, or away from, by the signs of f's
gradient at the mode-0 point; ent_thin_bar_by), 450 points per piece in place of 270. PLANT-MV-S83's gate stays modes 1 and -1; its
line also prints the corners' failures. Everything else is v1_14; v1_14's docstring follows.
kt_s8_cert_v1_14.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_13.py (e4b5531c; mock sweep VALID: pre 54743bfd,
20 chunks, final 7ec7f7a0, MOCK record 8cb5b41a), still mock runs only: rb_entries refuses cert mode until the D16 pins, which come
with the next version, and the review reviews v1_13 -> that version as one delta, as it was asked. On the word of 2026-11-08 (sf_pair's
thin and C1 target check go into the D16-pin version, through a core revision returning its constants, with a plant):
- The core pin moves to s8core_v1_11.py (diff against v1_10: out/diff_s8core_v1_10_v1_11.txt). sf_pair(..., info=None) records into
  a given dict what it computes anyway: k, t1, t1s, ddet, dz, C1 = t1 + ddet, Zz, num and the plain cov_lo; in the class-level branch
  sg, topc (the centered ball of Num - C1), the centered balls of (Num - C1)/(sg Z + dd)^2 for the dd it evaluates (keys '+dz',
  '-dz'), cl2 and whether cl2 is the returned lower end. No value changes.
- C-MV-SF and C-TARGET-SF (sf_classes, sf_piece, sf_line), on the piece's 3 S8-2 rows and 2 lemma rows of smallest headroom (SF_PICK;
  route (b)'s taken set), sf_pair being evaluated on r['ch'] (the W3 chain with its duals) with the info record:
  - C-MV-SF, the thin check of the class-level form: at mvbar_piece's 27 thin W3 chains (9 t x END_MODES: every coefficient, bar
    offset, wrapped allowance and delta at the same point, on the dual's allow and par; kept from C-MV-BAR's run, keep=True), Num_t
    and Z_t = cov2 on the thin chain with R_t^k; Num_t - C1 must lie in topc and (Num_t - C1)/(sg Z_t + dd)^2 in the centered ball of
    every dd the box evaluated, with the box's own C1, dz and sg, under the 2^-20 rule. A class whose class-level form is not active on
    the piece (Z of no certain sign) is counted, not checked; the line gives how many active classes the class-level lower end binds.
  - C-TARGET-SF, its C1 check: the box's C1 and dz (constants standing for bounds, computed from the box's balls) >= sf_pair's own C1
    and dz on the thin W3 chains at the 3 sample t (the box ends and the centre) x END_MODES, with the same prm, under C-TARGET's float
    allowance (box >= target (1 - 1e-10)).
  Run where C-MV-BAR runs: the first piece of every chunk, the pre pieces and the final's C-PIECE pieces.
- PLANT-MV-SF (pre, each N's first piece): the bar-corner thin W3 chains on the zero-bar run's allowance box against the class-level
  balls from the zero-bar W3 duals (sf_pair on r['ch'] with 'dual' replaced, so C1, dz and sg stay the box's) must fail in mode 1 and
  in mode -1. PLANT-TARGET-SF (same piece): the box C1 times 1e-3 must fail C-TARGET-SF.
- The mock LIM cap is 120 (was 60): v1_13's mock pre took 56.4 s of 60 and the new checks add to it. Cert mode keeps 10 .. 570.
Everything else is v1_13; v1_13's docstring follows.
kt_s8_cert_v1_13.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_12_5.py (c9b91b42; mock sweep VALID: pre 472111df,
20 chunks, final b7f453dd; the review DELTA_KT_S8_CERT_V1_12_5 2b36bfb2: sound). This is the cert-mode version without its D16 pins: mock
runs only until pk03's D16 H and S4 records exist (rb_entries still refuses cert mode; the pins come in the next version). It
carries what it was asked for on 2026-11-08 for the cert-mode version: the thin-chain fix (2b36bfb2), the pin of pk07's (c+) side check,
and the lemma's gaps at the sites the lemma note names
(NOTE_LEMMA_CENTERED_FORM_V2_rv01.md 8ca6c894, conditions C1 .. C6):
- the thin point chains were still ball-valued in the entry coefficients (entry_points' spans). _mv_setup's
  pt(t, vac, allow, par, emode) now builds the entries at t from entry_thin's coefficients in mode emode (each span's midpoint, upper
  end or lower end); on_dual passes emode on, and end_chain gives pt its own mode. So a thin chain pins, in one mode, every coordinate
  the centered chain carries as a ball: delta, the wrapped allowances and the entry coefficients. C-MV, C-MV-B, C-MV-DELTA (-B) and
  C-MV-MID (-B) use it; MV-ASIS (INFO) keeps the balls (emode None).
- C-CPLUS: pk07's certified side check of Lemma 19.2 (c+), pk07/out/cplus_sidecheck_v1.kv, pinned by its full sha256
  (447244b5..., C-HASH; the index of the S_V evidence: notes/SV_EVIDENCE_MANIFEST_v1.sha256 0e9bee51). The S_V export is valid
  only together with it. Stage A reads it after C-P2TAGS: cplus_load (the file present, its sha256 the pin), then cplus_text (FORMAT =
  CPLUS_SIDECHECK_v1 on the first line; the VERDICT lines exactly ['VERDICT = VALID'], by equality; INPUT_EXPORT and INPUT_M2B naming
  this run's own pinned P2 export and M2(b) record by path and full sha256; exactly one CLAIM line, printed), and tags it CERTIFIED. A
  refusal fails C-CPLUS. Plants, each refused: PLANT-CPLUS-VERDICT (VALID changed to INVALID), PLANT-CPLUS-VERDICT-TWO (a second
  VERDICT = VALID line), PLANT-CPLUS-FORMAT (CPLUS_SIDECHECK_v0), PLANT-CPLUS-BIND (INPUT_EXPORT with the export's run output's sha256),
  PLANT-CPLUS-MISSING (no file).
- C5 and C6 (C6; the sites): the core pin moves to s8core_v1_10.py (c43eef9e; diff against v1_9_1
  out/diff_s8core_v1_9_1_v1_10.txt 06b82f9d). v1_9_1 gated only the Cholesky pivots. v1_10 adds _pos(x) (certainly > 0) and _nz(x)
  (certainly > 0 or certainly < 0, so the sign is known); each raises ValueError('C5: ...') otherwise, a NaN ball included:
  - chain(), chain_B() and chain_RB(): g00 positive (sqrt(g00)'s argument and a divisor); T00, lam0 = T00 / g00 (1 + theta delta)
    and, in chain() and chain_B(), e_0 and rmain nonzero;
  - D.sqrt: the argument's value ball positive; D.__truediv__ and D.__rtruediv__: the divisor's value ball nonzero, for dual and plain
    divisors; strip_cov_t: Z nonzero;
  - C6: _cen raises ValueError('C6: ...') when the centered ball and the dual's value ball are disjoint (both hold the true value, so an
    empty intersection is a bug signal), where v1_9_1 returned the ball between the two ends.
  Inside a piece's evaluation, run_chunk's handler (unchanged) catches the ValueError: the piece has no bound, its PIECE line says
  ok=0 with a KILL line, and C-KILL fails. Anywhere else the run stops without a verdict. Plants (core_plants, pre item, each N's first
  piece), each must raise the core's ValueError with its own tag: PLANT-C5-G00 and PLANT-C5-T00 (the W3 chain at the piece's centre
  with g00, resp. T00, replaced by the ball 0 +- 1), PLANT-C5-DSQRT and PLANT-C5-DDIV (a dual whose value is 0 +- 1: its square root,
  and 1 divided by it), PLANT-C6 (_cen with the value ball 0 +- 1 and the centre 15 +- 1).
- C-MV-BAR, C-MV-BAR-B (the bar offsets pinned in the same modes; the review 8ca6c894: the zero-bar C-MV family never
  exercises the bar slots): the piece's own centered chains WITH their banded bars (piece_eval_RB's chW and chB, the chains the rows
  use) contain the thin points at the 9 sample t whose entries take every coefficient and every bar offset at the same point
  (ent_thin_bar: mode 0 the midpoints and offset 0, mode 1 the upper ends and +err_b, mode -1 the lower ends and -err_b), delta at 0, +u
  or -u (_corner) and every wrapped allowance at the same end (end_chain, on the dual's allow and par); leaf by leaf under the 2^-20
  rule, the stand-in met once in every chain. Run at the first piece of every chunk, at the pre pieces (each N's first piece and piece
  903) and at the final's C-PIECE pieces (each family's binding piece, the first and the last covered piece). PLANT-MV-BAR (pre, each
  N's first piece): the same kind of points, on the zero-bar run's own allowance constants (so the bar offsets are the only coordinate
  outside the compared box), against the zero-bar centered chains must fail in mode 1 and in mode -1 on each chain (mode 0 puts every
  bar offset at 0, which the zero-bar chains hold by construction); the line gives the failing leaves by mode.
- C-MV-S83 (beyond the lemma's list; found in the same audit): S8-3's strip enclosure (s8core's strip_cov_t, Cov J^2 = XY/Z - X Y/Z^2 in
  the mean-value form in t and the four bar offsets) is a centered instance that no check exercised. Each of the piece's 10 N4PAIRS
  enclosures (the ones the S8-3 rows use) must contain the function at the thin points, 9 sample t x END_MODES with ent_thin_bar's
  entries, under the 2^-20 rule. The function holds no constant standing for a bound, so its target is itself and this is also the
  instance's C1 check. Same places as C-MV-BAR. PLANT-MV-S83 (pre, each N's first piece): the same points against the enclosures
  recomputed with zero bars must fail in mode 1 and in mode -1.
- C-TARGET (the C1 check; the review 8ca6c894 C1 (c) and (d)): the thin checks compare G with G, so they cannot see a bound
  constant inside G that is too small for the box (both sides use the same constant). C-TARGET compares the piece's box constants,
  computed with every theta coordinate a ball, with their targets at thin admissible inputs (3 sample t, the box ends and the centre,
  x END_MODES: ent_thin_bar's entries, _corner's delta, every wrapped ball pinned; the thin chains compute their own allowance
  constants), in G's own bases (C0, C0B), trial set and choices: every allowance constant (a1 and each a_, the W3 dual run's allow) >=
  the thin chain's own; tau_B and sblk >= routeb_leak's at the thin B chain; eta+ and eta- >= sqrt(lambda_max) of the thin Gl's even
  and odd blocks; Rn >= |R|_2 of the thin W3 R; r_bb >= |R_BB block|_2 of the thin B chain (float64 numpy eigensolvers on the thin
  midpoints; a rounding allowance of 1e-10 relative, fixed in advance). Same places as C-MV-BAR. PLANT-TARGET (pre, each N's first
  piece): the box eta+ times 1e-3 must fail.
- Not covered by a thin or C1 check (as in the review 0226c38c sect. 5): sf_pair's class-level form (its _cen of (Num - C1)/(|Z| + dz)^2 on
  the chain's duals, for the S8-2 and lemma rows). A thin check needs sf_pair's internal constants C1 and dz at a thin chain, which the
  core does not return; adding it means a core revision.
The rule, the module's enclosure-against-value comparisons after v1_13: C-MV, C-MV-B, C-MV-DELTA (-B), C-MV-MID (-B), C-MV-BAR
(-B), C-MV-S83 and C-TARGET compare with thin admissible points in every coordinate the centered form carries as a ball (delta, the
wrapped allowances, the entry coefficients, and in C-MV-BAR, C-MV-S83 and C-TARGET the bar offsets; the C-MV family has zero bars on
both sides); C-UNIF (1) uses thin entry values (v1_12_5); C-UNIF (2), C-UNIF (3) and PLANT-UNIF-SLACK are unchanged; MV-ASIS is INFO;
C-PIECE compares two enclosures (its rows the gate, its leaves INFO).
Everything else is v1_12_5; v1_12_5's docstring follows.
kt_s8_cert_v1_12_5.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_12_4.py (55f735ff; mock pre VALID 57ef2f3e, its 10
N4 chunks VALID; the review DELTA_KT_S8_CERT_V1_12_4 233dcf96: sound), still mock runs only, on the word of 2026-11-08 (thin C-MV; the
C-PIECE change; the rule below) and the RULING_CMV_DELTA_V3_rv01.md (eec50f58). v1_12_4's mock chunk N3 [0, 91) (out 395464b6)
failed C-MV (delta = 0, zero bars) at piece 90 on the W3 leaves /AXm/0/0 and /beta/0/0 (2.0e-11 = 2.05e-5 rad(outer)): C-MV's point
chains were not thin either (delta 0, but the other vacuum allowances balls), so at a box-end sample the t shift uses up the centered
ball's t part and the point ball's own allowance radius decides, as for v1_12_3's endpoints; under the mock law (s ~ 1e-10) these balls
were thin. kt_s8_diag_cmv_v3 (b89c517f, out 96529f4f): ball point chains fail at 75 of 201 pieces (N3 0 .. 120: 72; N4 61 .. 140: 3),
always W3 /beta/kk or /AXm/kk, 2e-6 .. 2.4e-4 rad(outer), the B chain never; thin point chains at none.
The rule (2026-11-08): a check that compares an enclosure with values tests thin admissible points, never ball-valued chains that
carry the same allowances. The comparisons of this kind in the module, and what each now does:
- C-MV, C-MV-B (mv_piece; pre pieces, chunk samples, final binding pieces): thin point chains, end_chain at delta = 0 (the stand-in at
  the point 0, so lambda_0 = m-hat exactly, met once) in each of END_MODES; PLANT-MV and PLANT-MV-B stay (with thin chains they fail
  on 39, 108 and 108 of 144 W3 leaves and 26 of 53 B leaves, kt_s8_diag_cmv_v3);
- C-MV-DELTA, C-MV-DELTA-B (mvd_piece; same places): thin since v1_12_4;
- C-MV-MID, C-MV-MID-B (mvd_piece): the thin theta = 0 chains (delta at 0, END_MODES) inside the delta-kept centered chain, in place of
  v1_12_3's midpoints of the delta-kept ball chains (thin values, but not admissible points);
- C-UNIF (1) (unif_piece): the entry enclosures over the box against thin entry values (entry_thin: every coefficient at its span's
  midpoint, upper end or lower end), in place of entry_points' balls; C-UNIF (2) compares S4-U's upper end over the box with U at the
  9 t, values that are thin already (S4-U's coefficients are points); C-UNIF (3) compares the M2(b) law's exact decimals;
- PLANT-UNIF-SLACK: a thin point beyond each enclosure (unchanged);
- MV-ASIS: the delta-kept ball chains against the delta-kept centered chain, INFO only (no gate);
- C-PIECE: compares two enclosures (each half's centered chains with the parent's), not an enclosure with values: its leaves are INFO,
  its gate the rows (below).
Every other check compares bounds or exact values (C-PIECE's rows, C-BAND, C-RITZ0, C-MIRROR, C-PAREXACT, the record checks).
The review eec50f58's preference: every thin chain runs on the centered chain's own dual allowance constants and parity decision (on_dual:
chc['dual'][0]['allow'] and ['par_exact'], as the midpoint run takes them), so END_MODES sit at the centre and the two corners of the
centered chain's own allowance box (v1_12_4 pinned the point chains' own a1 and a_, interior points). kt_s8_diag_thin_v1 (69a8db2d,
out 83403bd4): over 103 pieces (N3 0 .. 50 and 903, N4 61 .. 110 and 903), W3 and B, no failure of C-MV and C-MV-DELTA on the dual's
allow and par, of the thin theta = 0 C-MV-MID (own and dual) or of C-UNIF with thin entries; the stand-in met once.
The argument, for the full allowance vector: every allowance the centered chain carries is one t-independent constant
on the piece: delta, 4 s^2, 4 sp and |B+| sp are the piece's vac constants, and a1 and the vector allowances a_ are the dual run's
upper ends over the box, passed to the midpoint run through allow (v1_6). So the true quantity at t is G_theta(t) for some theta
in [-1, 1]^m, one coordinate per wrapped pm() call and one for delta, with nothing known of theta(t) but the bound. For each fixed
theta, G_theta(t) is smooth in t; the centered chain carries every allowance as one ball with zero t-derivative, so its value at t_m
encloses G_theta(t_m) and its dual encloses G_theta'(xi) for every theta and every xi in the box; by the mean value theorem the centered
ball contains G_theta(t) for every theta in [-1, 1]^m and every t in the box. A thin chain is one admissible theta (each pinned point
lies in the ball the centered chain carries for that allowance), so the centered ball must hold it, up to the 2^-20 rule.
- C-PIECE's role (the final item), in plain words: S8's claim rests on each piece's own certificate, its full t-box evaluated once in
  a chunk (every row's certified lower end > 0, every top-mode class covered, both chains exactly parity-pure), and on the chunks
  covering S8's range; C-PIECE evaluates the halves of the binding pieces and of the first and last covered pieces only as a
  consistency check, and nothing in the claim or the record uses a half's result. What it asserts: refining a piece's box does not make
  its certificate worse: on each half (the parent's basis, law, U and P2 row), every common row's certified lower end is not below the
  parent's (slack 2^-20 |lo|), every m0 is no larger, and both chains stay exactly parity-pure. A row that fails stops the run (no
  slack is added). The leaf comparison (each half's centered chains inside the parent's) is INFO, with the leaf count, the Gl count and
  the worst excess of the rest: under the certified law it fails at every piece tested (kt_s8_diag_cpiece_v1 c47abec2, out c80ca636;
  no v1_12 final had run), as route (b)'s Gl leaves, R_B3^T R_B3 + tau_B I with tau_B recomputed on each half, move by design (1e2 ..
  1.5e11 rad(outer)), and the other leaves of the two centered enclosures differ by 2e-6 .. 5.7e-4 rad(outer) at J below ~120
  (kt_s8_diag_cpiece_v1_1 6a7771f6, out dbdfad8f: with delta = 0 still at 3 of 18 pieces, B /C/4/4; with delta = 0 and zero bars at
  6, W3 /beta/kk and /AXm/kk): two over-approximations of nested true sets carry no containment between them once the allowance balls
  are wide. No row failed at any of the 18 pieces. PLANT-PIECE (the parent's box collapsed to its right end) must fail on rows (the
  diag: 151 and 138 rows at N4 piece 61 and N3 piece 0).
Everything else is v1_12_4; v1_12_4's docstring follows.
kt_s8_cert_v1_12_4.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_12_3.py (4c0b2c52; mock pre VALID b6b0b576
DELTA_KT_S8_CERT_V1_12_3 d07977e3: sound), still mock runs only, on the word of 2026-11-08 (option (a)) and the review's
RULING_CMV_DELTA_V2_rv01.md (482dbe8c). v1_12_3's mock chunk N4 [61, 63) (out 68df356a) failed C-MV-DELTA at piece 62 on the W3 leaf
/beta/0/0 (3.7e-11 = 9.5e-6 rad(outer)). kt_s8_diag_cmvd_v1 (49d5e388, out e737435d) found the endpoint chains not thin: only delta was
pinned (+-u), and the other vacuum allowances stayed balls, so an endpoint ball of radius ~3.7e-6 met the centered ball's edge where
the delta shift and the t shift add (the centered radius is the allowances plus the delta part plus the t part, so a ball-valued
endpoint is tight there by construction); the central values lay 3.7e-6 inside, and with sp = 0 none failed. The W3 leaves /beta/0/0
and /beta/1/1 failed so at 30 of 61 scanned pieces, the B chain at none. Changes:
- C-MV-DELTA, C-MV-DELTA-B: the endpoint values are thin. end_chain pins every other pm() allowance of the point chain (the wrapped
  allowances below) to a point of its own ball as well, in three modes (END_MODES), with delta at +-u in each: all at their balls'
  midpoints, all at their upper ends, all at their lower ends. s8core's pm(r) is the symmetric ball [-|r|, |r|] (|r| = abs(r).upper(),
  the radius rounded up), so the three points are 0, +|r| and -|r| up to that rounding (the condition: +-r are the ball's true
  endpoints); the gate line counts the wrapped balls whose midpoint is not 0 (none expected; a one-sided or offset ball would be pinned
  to its own midpoint and ends just the same). Each mode is one fixed choice of the allowance parameters inside the balls the centered
  chain carries, so the theta-wise argument (v1_12_3's, below; applied to each allowance as to delta and the bars) gives containment,
  and the 2^-20 rule stays. kt_s8_diag_cmvd_v1_1 (d81c067d, out e4c43393): no failure over 63 pieces (N4 61 .. 100 and 903, N3 0 .. 20
  and 903), both chains, all three modes; the stand-in met once per chain. The once-per-chain check stays, and each line states it.
- The wrapped allowances, and why each pinned value is admissible. Each is a symmetric bound |offset| <= r on a quantity the chain
  cannot compute exactly, and the pinned point lies in the ball the centered chain carries for the same allowance:
  W3 chain (chain(), tt=False): place 2's pm(4 s^2) on each entry of R (setting 1: each entry moves by at most 4 s^2); place 3's
  pm(4 sp) on c (|c - c~| <= 4 sp); place 3's pm(|B+| sp) on each component of BTM (|B_X (u - psi-hat)| <= |B+| sp); the pm(a1) on
  each entry of beta (each entry of B_X's W block moves by at most a1 = 2 s |p_W| + 4 (|B+| + |c|) s^2); place 2's
  vector allowance pm(a_) on each W component of the vectors at d = -1, 0, 1 (a_ = s |x_u|; none on an odd basis vector's components
  when par_exact). The TT branch's pm(4 s^2) on M2 is not reached (tt=False). B chain (chain_RB()): place 2's pm(4 s^2) on each entry
  of R_BB. s, sp and |B+| are the piece's (vac_from_law and the P2 row), so 4 s^2, 4 sp and |B+| sp are the centered chain's own
  constants; a1 and a_ are the point chain's own (from its values at t), each at most the dual run's constant that the centered chain
  carries (inclusion), so the pinned point lies in the centered chain's ball; the choice may vary with t, which is allowed, as the
  argument holds for each fixed choice at each t.
- The condition of the argument: delta is one t-independent number per piece, an upper bound of the allowance on the
  whole piece. vac_from_law returns delta = (eps_r / sqrt(1 - s^2)).upper() from the piece's law values (the M2(b) law at J_lo), and
  the chains use it as the ball pm(delta), with zero t-derivative in the dual. If delta ever became t-dependent inside a piece, the dual
  would have to carry its derivative, or delta would have to be replaced by its supremum over the piece. The same holds for 4 s^2, 4 sp
  and |B+| sp (the piece's constants), and for a1 and a_ in the centered chain (the dual run's constants over the box, passed to the
  midpoint run).
- PLANT-MV-DELTA, PLANT-MV-DELTA-B: each mode must fail against the centered chain computed with delta = 0 (the diag, at the first
  pieces of both N: 20, 79 and 79 of 144 W3 leaves; 7, 11 and 11 of 53 B leaves).
- No theta = 0 chain: main withdrew it, as the d07977e3 counts C-MV-MID's exact midpoints of the delta-kept point chains as
  covering the delta-free values.
Everything else is v1_12_3; v1_12_3's docstring follows.
kt_s8_cert_v1_12_3.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_12_2.py (f03257d1; the review 49264157: sound), still mock
runs only, on the rules of 2026-11-08 and the RULING_CMV_DELTA_rv01.md (0fb1b956). v1_12_2's mock pre (certified M2(b)
law: delta 1.9e-6 .. 2.6e-6 at J = 300) failed C-MV and C-MV-B at the first pieces; kt_s8_diag_cmv_v2 (c13affed, out 2c22cc84) and
v2_1 (b1f75c59, out 408ef10b) traced it to the place-1 allowance delta alone (none fail with delta = 0; s, sp, eps_a and Bp change
nothing): every value divided by lambda_0 = m-hat (1 +- delta) is a ball of relative width ~delta, arb works on it at reduced precision,
and the point chains' midpoints round at about 2^-29 relative (one jumps by exactly 2^-29 at one sample) and their radii widen by ~1e-3,
above inside_r's slack; the centered balls still hold the true values (the delta-free values move ~1e-14 per sample and lie inside).
Changes:
- C-MV and C-MV-B compare the chains with zero bars AND delta = 0 (mv_piece): they test the dual and mean-value machinery on the
  t-dependence, and PLANT-MV and PLANT-MV-B still break it.
- Why delta needs no numerical check: place 1 is lambda_0(t) = m-hat(t) (1 + theta(t) delta), |theta(t)| <= 1, and
  nothing more is known of theta(t), not even continuity. (1) For a fixed theta in [-1, 1], G_theta(t) = F(t, m-hat(t) (1 + theta
  delta)), the chain's quantity, is smooth in t. (2) The centered chain carries (1 +- delta) as one t-independent ball: its value at t_m
  encloses G_theta(t_m), and its dual encloses G_theta'(xi), for every theta and every xi in the box. (3) So, by the mean value
  theorem, the centered ball contains G_theta(t) for every theta and every t in the box. (4) The true quantity at t is G_theta(t)(t) for
  the theta(t) that holds there, so it lies in the centered ball; no derivative of theta enters. The bars, constant offsets, are handled
  the same way, which is why C-MV zeroes them.
- C-MV-DELTA, C-MV-DELTA-B (mvd_piece): at each of the 9 sample t, the point chains at the two exact endpoints
  lambda_0 = m-hat (1 + delta) and m-hat (1 - delta) (thin balls, so arb keeps its full precision) lie in the centered chain computed
  with delta as is, leaf by leaf, up to inside_r's slack (the 2^-20 rule), with zero bars. PLANT-MV-DELTA, PLANT-MV-DELTA-B (the pre
  item, the first piece): the same endpoint chains against the centered chain computed with delta = 0 must fail. No core change:
  end_chain replaces s8core's pm for one point chain at a time by a wrapper that maps a stand-in object, placed in vac['delta'], to the
  exact point +delta or -delta and hands every other argument to s8core's own pm (restored in finally); chain() and chain_RB() read
  vac['delta'] once, in place 1, and the gate also requires the stand-in to be met exactly once per chain.
- C-MV-MID, C-MV-MID-B (the weak gate): each delta-kept point chain's midpoints lie inside the delta-kept centered chain, as a
  certain comparison (it catches a gross error such as an off-centre chain; delta's propagation rests on arb and the argument above).
- MV-ASIS (INFO, the pre item): the delta-kept point chains against the delta-kept centered chain with inside_r, with the largest
  excess relative to the centered radius and to the point ball's own radius (v1_12_2's comparison).
- C-MV-DELTA and C-MV-MID run wherever C-MV runs: the pre item's pieces, each chunk's sampled pieces, the final's binding pieces.
No slack changes; no bound changes; no core change.
Everything else is v1_12_2; v1_12_2's docstring follows.
kt_s8_cert_v1_12_2.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_12_1.py (7470acd2, never run), still mock runs only, on
the word of 2026-11-07 (it crossed v1_12_1) and the NOTE_LOOKALIKE_S4U_KV_FORMAT f8febe6a. Changes:
- (P2) pk07's certified vertical export is read in both modes (P2_CERT_IN_MOCK, main): the bound reader's load (its EXPORT-line
  binding), RECORD = END = EXPORT_KT_S67_v1, the full sha256 pin (C-HASH), EXPORT_STATUS CERTIFIED and every input tag certified
  (p2_text); C-SIDEMAN-P2 on its runs manifest; C-P2TAGS: its TAG_M2_VACUUM, TAG_S4_U and TAG_S4_TRB name this run's own pinned M2(b),
  S4-U and S4-TRB records by sha8; v1_12_1's control C-PX07 is gone (this is the main path now), and the three files are inputs
  (tagged), no longer references; the MOCK-path P2 plants stay. So the mock run's only MOCK inputs are the D16 H and S4 records;
- s4_text also requires END == RECORD, as kt_s9h's S4 headers and the P2 reader do; PLANT-S4U-END, PLANT-TRB-END;
- C-UNIF (the rule): a point ball passes when it lies inside the enclosure up to inside_r's 2^-20 rad(outer) AND its own midpoint
  lies inside the enclosure (unif_ok), so only the point evaluation's own rounding may poke out; kt_s8_diag_unif_v1_1 (9caafcbc) showed
  every v1_12 failure to be of that kind (excess 1e-10 .. 2e-9 of the enclosure's radius and of the point ball's own radius, midpoints
  inside, all at the box's upper t end); PLANT-UNIF-SLACK: a point 2^-10 rad(outer) beyond each entry's enclosure must fail unif_ok.
Everything else is v1_12_1; v1_12_1's docstring follows.
kt_s8_cert_v1_12_1.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_12.py (d4948ee4; mock chunk N4 [61, 63) VALID afe2ef2f,
mock pre VALID ccc38c92; its full mock sweep passed every piece, with C-UNIF failing at four sampled high-J pieces), still mock runs only;
on the REVIEW_S8CORE_V1_9_ROUTEB f812727a (the route (b) design SOUND) and RULING_KT_S8_CERT_V1_12_Q aad21227, and the word of
2026-11-07. Changes:
- the core is s8core_v1_9_1 (v1_9 with setup()'s docstring stating, as required, that its sector split of Gl needs both chains
  exactly parity-pure; no code change);
- (M2B) pk02's certified M2(b) record: M2B_KV_v1.txt, its asm output out/out_m2b_asm_v1.out, the run's side
  manifest MANIFEST_M2B_KV_v1_RUN.sha256 and m2b_reader_v1.py, pinned by full sha256; read through m2b_reader_v1.load(path, asm output,
  expected sha256) in both modes (M2B_CERT_IN_MOCK, the yes: the mock margins now rest on the certified vacuum law); C-SIDEMAN-M2B;
  C-TRIAL-M2B (as kt_s9h_v1_1: the record's one PIN_TRIAL line names both symmetrized vacres files by path and full
  sha256, once each, and no other vacres file); PLANT-M2BCERT-BIND, PLANT-M2BCERT-VERDICT and PLANT-TRIAL-M2B; the MOCK-path plants stay;
- (P2) pk07's certified vertical export (export_kt_s9h_v1_2_vsweep.kv, its run output, the runs manifest) pinned by full sha256 for
  cert mode; mock mode keeps the MOCK export, and the pre item reads the certified one as a control (C-PX07: the bound reader's
  load, p2_text's certified path, the runs manifest, the grid equal to the MOCK export's at both N, a few fields side by side); those
  three files are reference files of the mock run. Cert mode still stops at once: the D16 H and S4 records are not pinned;
- C-UNIF compares the entries with inside_r's slack (2^-20 rad(outer)), as C-MV does since v1_7: kt_s8_diag_unif_v1 (01d978b1) showed
  v1_12's C-UNIF failures (T,4,4 and T,6,6 at high J) to be arb's radius rounding at the box edge, 1e-10 .. 2e-9 of the radius;
- S8CLAIM: the parenthesis (route (b) runs without TT; H and S4 are 4-column entries at dmaxH 16);
- PLANT-TAUB calibrates on the whole piece (every row and top class through rows_at_tau), not on the binding row, which hardly depends
  on tau_B (v1_12: F = 1981 at N4);
- JX4 = 350, the route H junction at N4 as one named constant (settled at 350 by pk08's pre-check; S8's N4 start is piece 61).
Everything else is v1_12; v1_12's docstring follows.
kt_s8_cert_v1_12.py -- pk11 (code/pk11/). DRAFT REVISION of kt_s8_cert_v1_11.py (afd8f0ca) for the S8 route (b) (2026-11-07:
the TT route is out; S8 is route (b) only, U9 from a trial-basis chain, H and S4 from D16, per piece the best of the nested bases; N4
from J = 350, the band [300, 350) being route H's; N3 from J = 300). Freeze nothing certified yet: cert mode stops at once, since
the certified M2(b) record, the P2 export, m2b_reader_v1 and the D16 H and S4 records are not pinned. Changes:
- the core is s8core_v1_9 (1f2d4014, DRAFT, mock runs only): chain(..., tt=False) (the W3 chain reads no TT, carries the place-2 allowance), chain_RB and
  chain_dual_t_RB (the reduced B chain on g and T over the trial states only), routeb_leak (tau_B, Gl = R_B3^T R_B3 + tau_B I, the block
  bound on |Q_3 S Q_3|), setup(..., Gl, sblk), route_b_keys; see its docstring for the route (b) argument;
- (M3) route (b)'s certified records in both modes, through m3_reader_v6_2 (854b6a87) only: the partial asm of m3_run_v1_8_1 (D, E2, E3,
  FF; asmP) and the narrowed N record of m3_run_v1_8_2 (asmN: the 55 T,a,b and the TX,a,b with max(a, b) <= 3), each by load(path, asm
  output, 300, N); their law certificates m3_lawcert_v1_1 (the four partial records) and m3_lawcert_v1_2 (the N record) by
  load_lawcert(path, job output, 300, N, records) (the producer pin, the exact records map); every record, asm output, certificate, job
  output and side manifest pinned by full sha256 (the certificate's sha256 and both side manifests too). Gates: C-M3, C-SIDEMAN
  (each side manifest lists the files read with their sha256), C-TRIAL (full sha256 only; v1_11's chain_bad for sha8 trial sets is
  gone), C-NSCOPE (the N record's scope_keys are exactly its entries, and every N key the core reads, route_b_keys of B6: T,a,b for a, b
  <= 6, TX,a,b for a, b <= 3, lies within them; stage C reads entries only through fetch, which refuses an N key outside the scope),
  C-LAWV (tail and ann carry one pair [a, G] per vertex of the entry's graph). H and S4: the D16 records in cert mode (pending), the MOCK
  records with every bar times the D16 floor (H x11.8, S4 x9.3: pk03's lower bounds) in mock mode; the MOCK path keeps
  m3_reader_v4_4's item checks (M3R4, pinned: the MOCK records carry no laws). Plants: PLANT-M3RB-N, -JREF, -BIND, -PRECERT (the
  reader's refusals on the N4 N record), PLANT-TPOW (rem_tpow 3 refused), PLANT-TPOW-UP (rem_tpow 5: refused, or err_b unchanged),
  PLANT-LAWCERT-RECS, -WRONGREC, -PRODUCER, -VERDICT, PLANT-NSCOPE (fetch of TX,4,4 refused), PLANT-NOREC (a key no record holds),
  PLANT-PARITY-B (a B-chain parity key with a_0 = 1e-12); v1_11's MOCK-path plants stay. The S7 control records (C-PX03, C-TRIAL-
  CTRL) are gone: m3_reader_v6_2 reads only records with laws, and route (b)'s own records carry the certified path's checks now;
- REQUIRED: no TT; g and T to state 6 (B6); PARZ_EXPECTED follows (g, T, e, f, h with one odd state of 2, 5, 8); SYMFAM without TT;
- bars per piece: err_b(J_lo) = min(sum Bp, band4(J_lo)), band4 = rem (300/J)^4 + tail
  sqrt(P(J; tail)/P(300; tail)) + ann sqrt(P(J; ann)/P(300; ann)) + far e^(-far_rate (J - 300)) in arb (chi-square tails: n = 2
  e^(-s/2), n = 3 erfc(sqrt(s/2)) + sqrt(2s/pi) e^(-s/2); numerator up, denominator down), rem's exponent the fixed 4; the entry_ball
  form, no ak_rad term; C-BAND-LE (band4 <= sum Bp on every pre piece) and C-BAND-J300 (band4(300) reproduces
  sum Bp); the MOCK H and S4 keep their bars;
- S4-U: S4_U_CERTIFIED_v3 (e870cbe5), the same F2 form and claim (PLANT-S4U-V2: v3's text under v2's name refused);
- stage B (C-REPF: the W3 TT route against 3g's floats) is gone;
- stage C (piece_eval_RB): the W3 chain with tt=False on the piece's banded entries; per trial set B5, B6, B4 in turn the B chain,
  routeb_leak, setup and rows_cert; the first set whose rows and top classes all pass with both chains exactly parity-pure is taken;
  the PIECE line names the set, its tau_B and the sets tried (after '|', PIECE_RE unchanged); a piece fails (KILL) when no set passes or
  a chain is not exactly parity-pure (C-PAREXACT covers both chains: the sector split of Gl assumes it). S8's range: C-RANGE and
  RSTART (N4 from the piece that contains J = 350, N3 from 0); a chunk below it fails; C-COVER over [RSTART, 904). The pre item
  evaluates the range's first piece and piece 903 with C-UNIF, C-MV, C-MV-B (the B chain's mean-value form), C-PAREXACT, C-BAND and the
  break-even INFO (TAUB); PLANT-MV-B; the self-calibrating plants keep the piece's trial set and basis (PLANT-LEAK with the
  block bound; PLANT-BARS, -VAC, -U move tau_B too; PLANT-TAUB new). C-PIECE's halves keep the parent's set and basis and compare both
  chains' leaves; the final item prints C-MV-B and the break-even at the binding pieces;
- S8CLAIM: N4 J >= 350 and N3 J >= 300 on route (b) (DRAFT text, for the and the review).
Everything else is v1_11; v1_11's docstring follows.
kt_s8_cert_v1_11.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_10.py (faa25e39; mock dry run VALID, final ab2dc188),
the code part of the certified-run revision (the plan of 2026-11-07: v1_10 fixed during the review, which closed two items in
DELTA_KT_S8_CERT_V1_10_rv01.md fc0a9e37; the certified inputs are pinned in the next revision, a configuration change only). Changes:
- every chunk piece whose chain is not exactly parity-pure (ch['par_exact'] not True) fails, with a KILL line and
  ok = 0 on its PIECE line (the sector split, mirror and B_MB assume exact parity on every piece); C-PIECE fails a half whose chain is
  not parity-pure;
- C-PX03 and C-TRIAL-CTRL on all ten of pk03's certified S7 records of m3_run_v1_7 (N4 side manifest f8fe854a, N3 side manifest
  a4e1681b, both 6 OK, main checked), each read through m3_reader_v4_4.load(path, asm_out, 300, N);
- C-TRIAL's chain (pk03's message of 2026-11-07, checked on disk): besides the trial_set names and sha prefixes, chain_bad requires
  the record's engine sha (engine.<script>) to equal the asm output's line-1 script sha256, that engine script, pinned here by its full
  sha256 (m3_run_v1_7.py e55c5de1, MANIFEST_m3_run_v1_7.sha256 096e442b l.1), to pin TSF[N] and VRF[N] in its INPUTS (its l.161-164) by
  this run's full sha256s, and the asm output to hold exactly one 'C-HASH (...) -> PASS' line. So the sha8s of the v1_7 trial_set fields
  are tied to full sha256s; records from m3_vac_v1 on carry the full sha256s themselves. A gate in cert mode on every S8 record (the
  certified-run revision pins its engine); plants PLANT-TRIAL-ENGINE (the engine sha changed) and PLANT-TRIAL-CHASH (the asm output's
  C-HASH PASS line removed) must fail it.
Everything else is v1_10; v1_10's docstring follows.
kt_s8_cert_v1_10.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_9.py (6b0c37ca; mock dry run VALID, final f5f169d7) on
the stage C review (REVIEW_KT_S8_CERT_STAGEC_rv01.md ea6ff691: design SOUND; two required items, three notes):
- the core is s8core_v1_6 (pinned): the midpoint run of every centered chain takes the dual run's W-component allowances (s |x_u|
  upper over the whole box), and an odd basis vector gets none when the parity is exact. C-PAREXACT (pre, pieces 0 and 903): the chain
  of each stage C piece finds its basis and the parity-forced entries exactly F-pure (ch['par_exact']), so the parity treatment is in
  effect where the bounds use it;
- C-TRIAL. Every certified M3 record must carry trial_set = {ts: '<ts file>:<sha>', vacres: '<vacres file>:<sha>'} naming
  TSF[N] and VRF[N] (the files C-SYMIN checks) by base name and by sha256 (full, or its first 8 hex digits until pk03 writes the full
  value; the certified-run revision will require the full one). A gate in cert mode on every S8 record (m3_load_all reads it from the
  certified load); in mock mode the MOCK records carry none (INFO), and the certified path's check is shown on pk03's S7 records,
  which carry it (C-TRIAL-CTRL in pre; PLANT-TRIAL, a changed sha8, and PLANT-TRIAL-N, the N4 field against N = 3, must fail it). With
  C-SYMIN this closes the parity proof's chain from the records to the exactly symmetric stored files;
- (INFO): C0-ZERO, the largest zeroed component of each piece's C0 relative to its row, at pieces 0 and 903 (pre) and at the binding
  pieces (final). Two notes (run v1_8 or later; C-SYMIN the gate, C-MIRROR and C-RITZ0 numerical) need no change.
Everything else is v1_9; v1_9's docstring follows.
kt_s8_cert_v1_9.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_8.py (b4e7d473; mock dry run VALID, final a4fb4c33) on
the parity rule of 2026-11-07 (the treatment accepted, with four conditions):
1. The proof. The z9sym trial states, as stored, are exactly even or odd under the T <-> B reflection F: F swaps the BASIS9 coordinates
   xi_TM and xi_MB, so it swaps S's row pairs (1,2), (4,5), (8,9) and fixes rows 0, 3, 6, 7 (zero_states_v2's layout), and the states
   2, 5, 8 are odd, the rest even. The measure of the graphs g (D), T (N), TT (L), e (E2), f (E3) and h (H) is F-invariant: every
   coupling is F-symmetric (the vacuum end columns carry A on TM and on MB and B on TB, the interior and free columns 1 on TM and MB,
   the window graphs of C-MAINS), the single-site measure is O(N)-invariant, and the vacuum polynomial p = 1 + t q1 + t^2 q2 + t^3 q3
   on a vacuum column is F-symmetric (each q equal on the index pairs (0,1), (3,4), (7,8)). So an entry of those graphs that pairs an
   odd state with even ones (g,a,2, T,a,2, TT,a,2 for a in {0, 1, 3}; e,2; f,2; h,2) is the integral of an F-odd function against an
   F-invariant measure, which is exactly 0 for every J. The graphs with an X or Y insertion on the TM bond (TX, eX, fX, hX, DY) are not
   F-symmetric, and none of their entries is used as a zero. Where the symmetry of the stored data is established: zero_states_v2
   (291c9891) wrote the trial set and the symmetrized vacres files with C-SYM on the read-back files (pairs exactly equal or opposite as
   stored, the fixed rows of the odd states exactly 0.0, each q's pairs exactly equal), and zero_states_v2_1 (bf4bd4c7, record 168106e0,
   VALID) recomputed them byte-equal and passed C-SYM and C-PCLASS (parities [1, 1, -1, 1, 1, -1, 1, 1, -1, 1]) again. v1_9 adds C-SYMIN
   in this run, on the pinned files themselves (ts_*_z9sym_v1, vacres_K3_*_sym_v1): every stored decimal read as an exact rational,
   every state exactly even or odd, the odd states exactly 2, 5, 8, each q exactly symmetric; PLANT-SYMIN and PLANT-SYMIN-Q (one entry
   moved by 1e-15) must fail it. That the M3 records were computed from exactly these files is C-TRIAL, built once pk03 names the
   trial pin of its chain (it was asked pk03 on 2026-11-07).
2. C-PAR is a gate: the run fails whenever a parity-forced record ball excludes 0 anywhere on t in [0, 1/300] (par_bad's test lists
   every such key; it may also list a key whose ball holds 0 only through a cancellation between coefficient intervals, which fails the
   run on the safe side).
3. The zeroed C0 is a new trial basis, and every quantity is recomputed from it (ritz_pure's docstring); no Ritz value or relation of
   the unzeroed float eigenvectors is used.
4. Plants: PLANT-PARITY (a_0 = 1e-12 exactly, no bar: the ball excludes 0 at t = 0) and PLANT-PARITY-T (g,0,2 = -t +- 1e-6: it holds 0
   at t = 0 and excludes it at t = 1/300) must fail C-PAR.
Stage B's gates (run_B, the point J = 300 against 3g v1_2) keep the raw entries and the unzeroed basis, as 3g used them; no bound of the
claim comes from them. Everything else is v1_8; v1_8's docstring follows.
kt_s8_cert_v1_8.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_7.py (ea5a824c). v1_7's full mock sweep was VALID (pre
98e8d31c; 10 chunks covering pieces 0 .. 903 at both N, no KILL, no RISK; cpu 408 s), and its final passed every gate and plant up to the
record, where it stopped on an unpacking error in write_record_C (TAGS maps a path to (sha256, status); out d01146cf, no record
written). Changes, all in the final item's record step (chunk and pre code are v1_7's, unchanged):
- that loop unpacks (path, (sha256, status));
- the record text is rendered in memory (kv_render, the same bytes kv_write writes) and must pass the S8 record reader before any write
  (C-SELF-PRE), so in cert mode CERT_OK is set only after the record itself has been checked; PLANT-SELF-PRE-MOCK (cert mode): the text
  with EXPORT_STATUS MOCK must be refused;
- PLANT-CERTOUT and PLANT-TAGS run in both modes, before CERT_OK could be set (PLANT-TAGS on this run's tag list relabelled).
Everything else is v1_7; v1_7's docstring follows.
kt_s8_cert_v1_7.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_6.py (3b62c3ff; mock pre VALID ea0058aa, chunk c4 [0, 100)
VALID, chunk c4 [100, 280) INVALID on C-MV only, out e43fd473). The diagnostic kt_s8_diag_cmv_v1 (b2698b81, out 81c7c9f2) found the 4
failing leaves at piece 100 at its last sample point t_hi only: /L/4..7/0/1/1, the odd component of the even part of L[d], d = 4..7, balls
with midpoint exactly 0 whose radius is the vacuum allowance (R's cross-parity entries pm(4 s^2) times |k1(t)|). For such a leaf the
enclosure and the point ball are both tight at the box edge to first order, and arb keeps radii with a 30-bit mantissa rounded up at
each operation, so the point ball exceeded the enclosure by 1.6e-22 of a radius 5.15e-14 (3e-9 relative): radius rounding, not a wrong
gradient. Changes:
- C-MV and C-PIECE compare balls with a slack of 2^-20 rad(outer) on each side (inside_r; C-PIECE also 1e-20 |mid|), and C-PIECE's row
  lower ends with a slack of 2^-20 |lo|. A wrong t-gradient shows as an excess of order |g| rad(T), far above it; PLANT-MV and PLANT-PIECE
  still fire;
- the chunk's C-MV line prints the failing leaf paths;
- the final item also runs C-UNIF and C-MV at each binding piece and the first and last covered pieces (with C-PIECE).
Everything else is v1_6; v1_6's docstring follows.
kt_s8_cert_v1_6.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_5.py (b2edbb5b; its mock pre, out ecbc9d5a, read
VERDICT INVALID only because PLANT-LEAK did not fire, at both N). Changes:
- PLANT-LEAK scales the leakage Gram Gl by F^2 (eta scales by F), not eta+ and eta- alone: under T1' the leakage enters the lemma rows
  through the Gram form of Gl, and at m = 2 the eta tail (r + eta)^k - r^k - k r^(k-1) eta vanishes, so v1_5's eta override left the
  binding lemma row unchanged at every F;
- a parity-pure C0 was already in v1_5 (ritz_pure,
  C-PAR): the core is s8core_v1_5 (pinned), whose head() returns a failing value when Cov_lo <= 0: C-REPF prints the rows whose
  ball headroom is inf as INFO: C-REPF is a gate in both modes, on 3g's own data (in cert mode the MOCK records, M2(b) law and P2
  export are loaded as reference files for it, so it stays like for like; the certified inputs give the INFO rows);
- C-PX03 (control, pre item): pk03's first certified M3 records (S7, N4, m3_run_v1_7) through the certified path,
  m3_reader_v4_4.load(path, asm_out, 300, 4) and then m3_text's certified parse and entry_ball, must all be accepted; plants
  PLANT-PX03-N (N = 3), PLANT-PX03-JREF (J_REF 150), PLANT-PX03-MOCKPATH (the MOCK path refuses a certified record),
  PLANT-PX03-BIND (one byte added), PLANT-PX03-PRECERT (the asm output's VERDICT VALID-PRECERT). The note of 2026-11-07: these
  records may exercise the certified path in stage C's mock runs; the outputs stay MOCK.
Everything else is v1_5; v1_5's docstring follows.
kt_s8_cert_v1_5.py -- pk11 (code/pk11/). STAGE C of kt_s8_cert (the OK of 2026-11-07, all three stages): the pieces in J, the
chunked run, the S8 record and the writer's input rule, on the core s8core_v1_4 (pinned), which adds t as a dual slot of the mean-value
form. Stage A's readers and plants and stage B's gates are kept (kt_s8_cert_v1_4 7f12a933, mock VALID 6c6430c7).
Run: MODE ITEM LIM [N A B] [TAG]. MODE mock (MOCK inputs, outputs in pk11/mocks/out) or cert (the certified inputs, outputs in
pk11/out; in this version the certified inputs and pk02's m2b_reader_v1 are not pinned yet, so cert mode stops before it opens
any file: the certified run is a later revision with those pins and its own approval). Items, each one job of one core under 10 min:
- pre: stage A (readers, plants) and stage B (C-DUAL, C-MAINS, the point piece J = 300 with C-REPF against 3g v1_2 (a gate in mock
  mode; in cert mode the same comparison is printed as INFO, since certified bars differ from 3g's float and analog bars), C-SF0,
  PLANT-SF0), then stage C's checks per N: pieces 0 and 903 in full with C-UNIF and C-MV, PLANT-RIGHTEND, PLANT-LAW-JHI, PLANT-MV,
  C-MIRROR, C-RITZ0, and the self-calibrating plants of SPEC sect. 10 on piece 0 (PLANT-LEAK, PLANT-OVERLAP, PLANT-BARS, PLANT-VAC,
  PLANT-U: the factor F at which the binding row or class fails; each must hold at F/1.1 and fail at 1.1 F);
- chunk N A B: pieces A .. B-1 of P2's grid for one N. Per piece: the entries as duals over the piece box (t in [1/J_hi, 1/J_lo], exact
  from P2's float grid ends; each bar offset in [-err_b, err_b]), the parity-pure basis of the center, the M2(b) law at J_lo through the
  reader's law_v1 (nonincreasing in J by its C-MONO), S4-U's upper end over the box, the piece's P2 row; every row of the rule with
  its certified lower end (s8core_v1_4.rows_cert) and the kill rule of ADD1 sect. 1: a piece fails only when some row's lower end is not
  > 0 or some class lacks a top-mode cover with m0 <= 8 (KILL lines, VERDICT INVALID); rows with headroom < 2 print RISK lines; C-UNIF
  and C-MV on the chunk's first and last pieces and on every 100th;
- final: the pre and chunk outputs of this script found in the output folder, each counted only with this script's sha256, the mode,
  this run's INPUTS digest and VERDICT lines exactly ['VERDICT VALID'] (a chunk also with exactly its pieces, all ok; an output holding a
  KILL line fails the final, C-NOKILL); C-COVER (cert: the VALID chunks cover 0 .. 903 once per N; mock: disjoint, the coverage
  printed); the per-N minima per family; C-PIECE at each family's binding piece and the first and last covered pieces (each half of the
  t-box, with the parent's basis, law, U and P2 row, inside the parent: chain leaves, rows' lower ends, m0); plants PLANT-COVER-GAP,
  PLANT-COVER-OVERLAP, PLANT-CHUNK-SUFFIX, PLANT-CHUNK-SHA, PLANT-CHUNK-INPUTS, PLANT-CHUNK-PIECE, PLANT-PIECE; then the record.
Parity (new in stage C): the z9sym trial states are exactly even or odd under T <-> B, so the entries of the reflection-symmetric graphs
(g, T, TT, e, f, h) with exactly one odd state vanish for every J. C-PAR checks that each such record ball holds 0 for every t in
[0, 1/300] (a record that contradicts the symmetry fails), and stage C then uses exact zeros for them; the basis C0 of each piece is made
parity-pure (minority components set to 0). So the chain's sector split of eta, the flip mirror and B_MB rest on exact parity. Stage B's
gates keep the raw entries, as 3g used them (C-REPF stays like for like). PLANT-PARITY: an explicit 1e-12 with no bar must fail C-PAR.
M2(b): pk02's interface (load, loads, check, law_v1(rec, N, J) -> rounded-up decimal strings; agreed 2026-11-07), here through the
MOCK module mocks/m2b_reader_v1_mock.py (pinned; MOCK formats only; mock law q_300 (300/J)^MOCK_RATE, strictly decreasing, so that a
law taken anywhere but J_lo fails C-UNIF); its plants PLANT-MOCK-M2B, PLANT-M2B-VERDICT-SUFFIX, PLANT-M2B-VERDICT-STUB, PLANT-M2B-BIND,
PLANT-M2B-FMT, PLANT-M2B-DUPKEY.
Certified reads: M3 through m3_reader_v4_4.load(path, asm_out, 300, N), P2 through the bound reader's load(export, run),
M2(b) through m2b_reader_v1.load(path, asm_out, expected_sha256), each the reader's file entry point; the texts then pass the same
checks as on the MOCK path.
Writer: every input of the claim is tagged with its path, sha256 and the path that read it (CERTIFIED or MOCK); kv_write
refuses a certified S8 record, before any file is opened, unless every tag reads CERTIFIED, CERT_OK is set and the run is a cert-mode
final in pk11/out. CERT_OK is set only by a cert-mode final with no failed gate, every plant fired and both N covered. The trial
files and 3g's outputs are reference files (pinned, listed in the record, not inputs of the claim). PLANT-TAGS, PLANT-CERTOUT.
Price [E]: mock runs (each <= 60 s CPU, LIM <= 60); the certified run, its own approval: pre + chunks + final.
Run (one job at a time; mock example):
  D=/mnt/g2/release/root/code/pk11; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_s8_cert_v1_5.py mock pre 60 > $D/mocks/out/kt_s8_cert_v1_5_mock_pre.log 2>&1
v1_4's docstring follows.
kt_s8_cert_v1_4.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_3.py (28e601d3; mock INVALID on C-REPF only: 15 of 18 rows
within 1.4% of 3g v1_2 like for like, the three rows on |A_perp(0)| at 0.90-0.96). The one change: the core is s8core_v1_3 (pinned),
which computes |A_perp|^2 at d = -1, 0 inside the chain, so it is centered as one quantity. The C-REPF band [0.97, 1.03] is unchanged.
Everything else is v1_3; v1_3's docstring follows.
kt_s8_cert_v1_3.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_2.py (be6d466a; mock INVALID on C-REPF only). v1_2's
C-REPF found 3g v1_1's propagation flaw (one-sided shifts of quantities clipped at 0); main accepted it and ran 3g v1_2 (cda500ca, VALID;
out b287d9c3 / d4c189f2), the corrected reference. Changes:
- the core is s8core_v1_2 (pinned): sf_pair's class-level mean-value form (Num and Z as duals over the entry box) and the eta override;
- C-REPF (gate), like for like: the ball KEY rows and the family rows at 3g v1_2's own rows, with 3g v1_2's printed eta+ and eta-,
  against 3g v1_2's headrooms, band [0.97, 1.03] (reason in run_B); the ball's own rows (its tighter eta) and the strip (3g's strip bar
  is the Z = 1, N = c approximation) are printed as INFO;
- the stage A notes: PLANT-MOCK-M3-FILE and PLANT-MOCK-P2-FILE through the readers' file entry points; the S4 records'
  own verdict keys in s4_text; PLANT-M3-VERDICT-STUB, PLANT-P2-VERDICT-STUB, PLANT-P2-VERDICT-TWO, PLANT-P2-FLOAT-REBOUND (the FLOAT
  export bound to a planted VALID run output, refused at its status); C-GRIDTOK; one more is stage C's;
- pk07's reader v2_1 (b0a23237) replaces v2 (1b19d393, never run), as the DELTA dba2b393 confirmed.
Everything else is v1_2; v1_2's docstring follows (its C-REPF band is superseded).
kt_s8_cert_v1_2.py -- pk11 (code/pk11/). REVISION of kt_s8_cert_v1_1.py (807d4d7c; its mock output d35699b1 read VERDICT
INVALID on C-REPF only, with C-SF0 and C-MAINS passing). Changes:
- the core is s8core_v1_1 (pinned): the chain and S8-3's strip in the mean-value form (duals over the entry box), against the interval
  dependency that left |p_perp| 46% above 3g's first-order value and the d >= 1 rows up to 27% looser;
- C-REPF compares each family at 3g's own minimizing row (v1_1 compared the minima of different row sets: 3g's S8-1 minimum sits at
  (-1, same, 5), a row the ball top mode already covers);
- C-DUAL (gate): the dual arithmetic against central differences, and an arb + dual sum.
The C-REPF band [0.8, 1.25] is unchanged. Everything else is v1_1; v1_1's docstring follows.
kt_s8_cert_v1_1.py -- pk11 (code/pk11/). STAGE B of kt_s8_cert (the OK of 2026-11-07, all three stages): stage A's readers
and plants (kt_s8_cert_v1 ae5fa8cd, mock VALID 27380cc5) unchanged, now on the mocks of kt_s8_mkmock_v1_2 (c09dfd44: S4 = the 18 strip
entries, so 90 required entries), plus the interval core s8core_v1 (pinned by full sha256), run on one piece per N:
- C-MAINS: the chain's five main-term ratios exactly, from the spanning-tree determinants of the eight window graphs in balls (the vac end
  couplings A = (3 + sqrt 21)/6, B = (3 sqrt 5 - sqrt 21)/12; main ~ tau^(-n/2), n = N - 1), against 3g's float C-MAIN (1e-12);
- the point piece J = 300 (the mock bars as radii, the mock M2 law, P2 piece 0, S4-U at t = 1/300): the chain in balls with the fixed
  binary64 Ritz basis of the midpoints, every row of the rule (crude route), S8-3's strip in balls from the S4 entries, C-SIGN-C4
  (INFO on mocks);
- C-REPF (stage B's gate, main): the ball headrooms of 3g's KEY rows, its crude family minima and its S8-3 strip per pair, against 3g's
  printed values (out_kt_s8f3g_v1_1_n<N>.out, pinned), ratio in [0.8, 1.25]: the ball bounds may differ from 3g's first-order
  propagation of the same bars, but not by more than that band;
- C-SF0 (stage B's gate): at t = 0 with point entries and no vacuum terms, the exact closed form (N - 1) T^2 / 2 inside [Cov_lo, Cov_hi]
  for 3g's 288 classes (slack 1e-9 |exact|); PLANT-SF0: with every truncation term 0 some class falls outside.
The MOCK record now carries stage B's rows per N. Run: as stage A with kt_s8_cert_v1_1.py and LIM 60 (hard 65 s). Stage A's docstring:
kt_s8_cert_v1.py -- pk11 (code/pk11/). The certified S8 assembly of SPEC_S8_CERT_v1 (c0f95398) with its ADD1 (9f38c5e7),
built hand-first on MOCK records, the way pk15 built kt_p2_assembly. STAGE A of three: the readers, the mocks,
the plants and the writer guards. The interval core (stage B) and the pieces in J (stage C) come in later versions; this version
computes nothing of S8 itself. Mode 'mock' only: no certified mode exists in this version, and no output carries a certified FORMAT.
Readers (each has a CERTIFIED path, the one the certified run will use, and a MOCK path):
- (M3) load_m3(path, asm_out, N, mode). CERTIFIED: pk03's bound loader m3_reader_v4_4.load(path, asm_out, 300, N), pinned by its full
  sha256 and imported from its file (ADD1 sect. 3.11). MOCK: the same binding rule (the asm output's VERDICT lines exactly
  ['VERDICT VALID'] and exactly one 'RECORD <name> <sha256>' line naming the file with the sha256 of its bytes), FORMAT
  'M3_RECORD_v1_MOCK' with the claim 'MOCK ' + the reader's certified claim, J_REF 300 and N by exact equality, the reader's kernel
  fields, and the reader's own item checks (_items). Both paths return the entries as entry_ball gives them: exact rational ends LO, HI
  of a_0..a_3 and the bar err_b, so that I(J)/main(J) lies in sum_k [LO_k, HI_k] t^k + [-err_b, err_b] for t in [0, 1/300].
- (M2B) load_m2b(path, mode). CERTIFIED: pk02's m2b_reader_v1 once it is frozen; not pinned yet, so the path refuses after its format
  check. MOCK: strict S4U_KV_v1 with RECORD and END 'M2B_KV_v1_MOCK', TAG and CLAIM starting 'MOCK', and the constant law per N
  (N*_EPS_R_300, N*_S_300, N*_EPS_A_300, N*_EPS_DS5_300, each an upper end for every J >= 300).
- (P2) p2_text(export, run_out, name, mode): pk07's bound reader kt_s67_export_reader_v2 (1b19d393, pinned by full sha256).
  CERTIFIED: its loads, the only certified entry point (rule V2 by exact equality: the run output's VERDICT lines equal ['VERDICT VALID']
  and exactly one EXPORT line names the export's base name with the sha256 of its bytes; then EXPORT_STATUS CERTIFIED and RUN_VERDICT
  VALID), and here also every TAG_*_STATUS certified. MOCK: the reader's same binding (_bound), then loads_noncert (which refuses a
  CERTIFIED export), EXPORT_STATUS MOCK and a TAG starting 'MOCK'. Both: the S8 fields, 904 contiguous pieces per N from 300 to inf, jlo
  and jhi as floats (rule V1, the reader's parse), every other field an exact Fraction.
- (S4) load_s4(path, which): pk08's certified records S4_U_CERTIFIED_v2 (b1b6b99b; replaced since v1_12 by S4_U_CERTIFIED_v3,
  e870cbe5, the same F2 form and claim, which is the one pinned and read) and S4_TRB_CERTIFIED_v1 (91109301) through P2's KV
  layer s4u_kv_ref_v1 (pinned): RECORD exact, the claim text exact, no PRECERT, STUB or MOCK in FORMAT, RECORD, TAG or CLAIM, and the
  keys per N. These records are final, so both modes read them.
Writer: kv_write(path, record, header, rows, certified). A certified FORMAT is refused before any file is opened unless CERT_OK is set,
which only a certified-mode run that has passed every gate and plant may do (no such mode exists here); MOCK outputs carry RECORD
'S8_CERT_RECORD_v1_MOCK', EXPORT_STATUS MOCK and TAG and CLAIM starting 'MOCK', and no status value naming CERTIFIED.
Gates: C-HASH; C-M3 (per N: every mock family read through the MOCK path; the chain's 75 entries present once, AL's AA entries not
among them since AL is on hold; parity zeros exact);
C-M2B; C-P2; C-S4U; C-TRB; C-NOCERT (every output's status keys MOCK); C-SELF (the output re-read by read_s8: MOCK accepts, CERTIFIED
refuses).
Plants (each must fire): PLANT-MOCK-M3 (the certified path refuses each mock record, bound to its mock asm output); PLANT-M3-SMOKE (the
certified path refuses pk03's smoke record m3_smoke_v3_d4_rec.json, a certified-format record with no validated kernel, even when a
run output names it); PLANT-M3-VERDICT-SUFFIX, PLANT-M3-VERDICT-PRECERT, PLANT-M3-VERDICT-TWO (asm outputs with 'VERDICT VALID (...)',
'VERDICT VALID-PRECERT' or two VERDICT lines); PLANT-M3-BIND (a record changed after its RECORD line was written); PLANT-M3-JREF (J_REF
150); PLANT-M3-N (an N = 3 record read as N = 4); PLANT-M3-FMT (FORMAT 'M3_RECORD_v1_PRECERT' on the mock path); PLANT-M3-AKLEN (three
coefficients); PLANT-MOCK-P2 (the certified path refuses the mock export); PLANT-P2-FLOAT (the certified path refuses pk07's FLOAT
export 2520bfb9 with its own run output); PLANT-P2-SUFFIX (a run output whose VERDICT line is suffixed); PLANT-P2-SHA (a run output naming
another sha256); PLANT-P2-DUPKEY; PLANT-P2-GRID (a piece missing); PLANT-MOCK-M2B (the certified path refuses the mock); PLANT-M2B-RECORD
(RECORD M2B_KV_v1 on the mock path); PLANT-M2B-DUPKEY; PLANT-S4U-PRECERT, PLANT-S4U-KEY, PLANT-S4U-CLAIM, PLANT-TRB-PRECERT, PLANT-TRB-KEY
(in-memory variants of the certified records); PLANT-CERTOUT (the writer raises on a certified FORMAT before opening a file).
Inputs: the MOCK files of kt_s8_mkmock_v1_1 (8e0e163a) in pk11/mocks/out/mkmock_v1_1/, pinned below. Writes only
pk11/mocks/out/out_kt_s8_cert_v1_mock.out and the MOCK record s8_record_mock_kt_s8_cert_v1.kv there. Price [E]: seconds (LIM 30,
hard 35 s = 0.0097 core-h), for mock tests. Run (one job at a time):
  D=/mnt/g2/release/root/code/pk11; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_s8_cert_v1.py mock 30 > $D/mocks/out/kt_s8_cert_v1_mock.log 2>&1
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, time, hashlib, signal, traceback, json, re, importlib.util, math, ast
from fractions import Fraction
from flint import arb, ctx
ctx.prec = 256
PREC = 256        # v1_14_2: the run's flint precision; C-PREC gates ctx.prec == PREC at the end of every item
PREC_LOG = []     # (module, ctx.prec before its load, after) for every pinned module load that changed ctx.prec

MODES, ITEMS = ('mock', 'cert'), ('pre', 'chunk', 'final')
USAGE = ('usage: kt_s8_cert_v1_14_2.py MODE ITEM LIM [N A B] [TAG]   (MODE mock|cert; ITEM pre|chunk|final; chunk: N 3 or 4 and pieces A .. B-1, '
         '0 <= A < B <= 904; TAG r1 .. r99 for a re-run; LIM = RLIMIT_CPU soft limit in s, 10..120 in mock mode, 10..570 in cert mode; '
         'hard LIM + 5)')
_args = sys.argv[1:]
if len(_args) < 3 or _args[0] not in MODES or _args[1] not in ITEMS:
    print(USAGE)
    sys.exit(2)
MODE, ITEM = _args[0], _args[1]
LIM = int(_args[2]) if re.fullmatch(r'[0-9]{1,3}', _args[2]) else -1
_rest = _args[3:]
CHUNK = None
if ITEM == 'chunk':
    if len(_rest) < 3 or not all(re.fullmatch(r'[0-9]{1,3}', x) for x in _rest[:3]):
        print(USAGE)
        sys.exit(2)
    CHUNK = (int(_rest[0]), int(_rest[1]), int(_rest[2]))
    _rest = _rest[3:]
    if CHUNK[0] not in (3, 4) or not (0 <= CHUNK[1] < CHUNK[2] <= 904):
        print('bad chunk %r' % (CHUNK,))
        sys.exit(2)
RTAG = ''
if _rest:
    if len(_rest) != 1 or re.fullmatch(r'r[1-9][0-9]?', _rest[0]) is None:
        print(USAGE)
        sys.exit(2)
    RTAG = '_' + _rest[0]
if not (10 <= LIM <= (120 if MODE == 'mock' else 570)):   # v1_14: mock cap 60 -> 120 (v1_13's mock pre took 56.4 s)
    print('bad LIM %r for mode %s' % (_args[2], MODE))
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))
STAGE = ['start']

CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk11'
MOCKS = OWN + '/mocks'
MOUT = MOCKS + '/out'
MKD = MOUT + '/mkmock_v1_2'
MKC = MOUT + '/mkmock_c_v1'
OUTD = OWN + '/out'
OUTDIR = MOUT if MODE == 'mock' else OUTD
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(OUTDIR, 'out_%s_%s_%s%s.out' % (LABEL, MODE, ('c%d_%04d_%04d' % CHUNK) if CHUNK else ITEM, RTAG))
REC_PATH = os.path.join(OUTDIR, 's8_record_%s_%s%s.kv' % (MODE, LABEL, RTAG))
# the certified inputs: pinned by the certified-run revision, once the records exist (the M2(b) record and its asm output; the CERTIFIED
# P2 export and its run output; pk02's frozen m2b_reader_v1; v1_12: the D16 H and S4 records). v1_12 pins route (b)'s certified M3
# records and law certificates below and reads them in both modes; it is a DRAFT (freeze nothing certified yet).
C2F = CODEDIR + '/pk02'   # v1_12_1: pk02's certified M2(b) record, its asm output, side manifest and reader
CERT_M2B = (C2F + '/M2B_KV_v1.txt', C2F + '/out/out_m2b_asm_v1.out')
M2BRD, M2BSIDE = C2F + '/m2b_reader_v1.py', C2F + '/MANIFEST_M2B_KV_v1_RUN.sha256'
M2B_CERT_IN_MOCK = True   # v1_12_1: the certified M2(b) in mock mode too (as M3); P2 and the D16 H/S4 stay MOCK there
# v1_12_1: pk07's certified vertical export (EXPORT_KT_S67_v1 from kt_s9h_v1_2's vsweep; the approval), its run
# output and the runs manifest; v1_12_2: read in both modes (P2_CERT_IN_MOCK), keyed on RECORD = END = EXPORT_KT_S67_v1,
# the full sha256 pin and the reader's EXPORT-line binding, so the D16 H and S4 records are the mock run's only MOCK inputs
CERT_P2 = (CODEDIR + '/pk07/out/export_kt_s9h_v1_2_vsweep.kv', CODEDIR + '/pk07/out/out_kt_s9h_v1_2_vsweep.out')
P2SIDE = CODEDIR + '/pk07/MANIFEST_kt_s9h_v1_2_runs.txt'
P2_CERT_IN_MOCK = True
# v1_14_2: pk03's certified D16 H and S4 records per N, with their asm output and freeze side manifest (v1_14_3: N3's pinned too)
D16 = {4: {'H': CODEDIR + '/pk03/out/m3_s8v2_H_N4_J300_v1_9_3.json', 'S4': CODEDIR + '/pk03/out/m3_s8v2_S4_N4_J300_v1_9_3.json',
           'asm': CODEDIR + '/pk03/out/m3_run_v1_9_3_asm.4.out', 'side': CODEDIR + '/pk03/MANIFEST_m3_run_v1_9_3_N4_RECORDS.sha256'},
       3: {'H': CODEDIR + '/pk03/out/m3_s8v2_H_N3_J300_v1_9_3.json', 'S4': CODEDIR + '/pk03/out/m3_s8v2_S4_N3_J300_v1_9_3.json',
           'asm': CODEDIR + '/pk03/out/m3_run_v1_9_3_asm.3.out', 'side': CODEDIR + '/pk03/MANIFEST_m3_run_v1_9_3_N3_RECORDS.sha256'}}
D16_CERT_IN_MOCK = True   # v1_14_2: the pinned D16 records in mock mode too (v1_14_3: both N's H and S4 certified there)
D16_PINNED = all(D16[n] is not None for n in (4, 3))   # cert mode needs both N


def _under(path, top):
    return os.path.realpath(os.path.dirname(path)) == os.path.realpath(top) and \
        os.path.realpath(top).startswith(os.path.realpath(OWN) + os.sep)


if MODE == 'cert' and not (CERT_M2B and CERT_P2 and M2BRD and D16_PINNED):
    print('cert mode: the D16 H and S4 records of N = %s are not pinned in this version (N4\'s are; N3\'s follow in a pins-only '
          'revision); no file opened' % ', '.join(str(n) for n in (4, 3) if D16[n] is None))
    sys.exit(2)
if not (os.path.isdir(OUTDIR) and _under(OUT_PATH, OUTDIR) and _under(REC_PATH, OUTDIR)):
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

M3RD = CODEDIR + '/pk03/m3_reader_v6_3.py'   # v1_14_2: the one certified M3 path (route (b)'s records and the D16 records)
M3RD4 = CODEDIR + '/pk03/m3_reader_v4_4.py'   # v1_12: the MOCK path's item checks only (the MOCK records carry no laws)
P2RD = CODEDIR + '/pk07/kt_s67_export_reader_v2_1.py'
KVRD = CODEDIR + '/pk07/s4u_kv_ref_v1.py'
S4UF = CODEDIR + '/pk08/S4_U_CERTIFIED_v3.md'
TRBF = CODEDIR + '/pk08/S4_TRB_CERTIFIED_v1.md'
P2X = CODEDIR + '/pk07/out/export_kt_s67_cert_v2_2_sweep.kv'
P2XR = CODEDIR + '/pk07/out/out_kt_s67_cert_v2_2_sweep.out'
SMOKE = CODEDIR + '/pk03/out/m3_smoke_v3_d4_rec.json'
FAMS = ('D', 'N', 'E2', 'E3', 'FF', 'S4', 'H', 'L')   # AL: a named fallback on hold, not needed (ADD1 sect. 2.6)
M3MOCK = {n: [os.path.join(MKD, 'mock_m3_%s.%d.json' % (f, n)) for f in FAMS] for n in (4, 3)}
M3ASM = {n: os.path.join(MKD, 'mock_m3_asm.%d.out' % n) for n in (4, 3)}
P2MOCK = os.path.join(MKD, 'mock_export_kt_s67.kv')
P2MOCKR = os.path.join(MKD, 'mock_p2_run.out')
M2BMOD = MOCKS + '/m2b_reader_v1_mock.py'
M2BREC = MKC + '/mock_m2b_v2.kv'
M2BASM = MKC + '/mock_m2b_asm.out'
PINS = {
    M3RD: '539b613f6a9c07a9bef3d0cbb408c1d41de276a6a59aede8b03149204ce28661',
    M3RD4: 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0',
    P2RD: '4c6949462ca8c5dda337027b7dc5bada51102a063dc5ff6f8a1c2def01eaf49d',
    KVRD: '5a786edb1eb62608ecf7440b70124044d6207d87523b9c957394666ab4448c98',
    S4UF: 'eb98948365fa35498206c9f1b80c6d98d421f69b9dca6c245f3f2d1198112751',
    TRBF: '2c17c287c0affbfe0e0fcbd8097edff2258ea1109d91381d6206a11d4efdd694',
    P2X: '6fe9ab65f5207dc3658c98ff4f3696bd2db6aa784b0dec84b33881b2da579c34',
    P2XR: '4004f39cad1cdc45acd4cb764ed8b2b48021e0c327074caf96e28d4af30d6d81',
    SMOKE: 'f4bb0ac56fb7ee8cb04a249b9d1157d8849718079fadf68e740f9523bb7a1ffd',
}
# the MOCK inputs written by kt_s8_mkmock_v1_1 (8e0e163a), pinned by sha256
MOCKPINS = {
    MKD + '/mock_export_kt_s67.kv': '692b609f66e3b879e32c4541d497c2f47edae158e5f5c077870194875baeba62',
    MKD + '/mock_m3_D.3.json': '8cc2545f73a434b2a6dec62c378a9bfe704637b60b89dfabb7934370487d79ba',
    MKD + '/mock_m3_D.4.json': '489ec986477cdaf7eeccdb1bbd91c5976b4726e2505cdb50202a40050e25b474',
    MKD + '/mock_m3_E2.3.json': 'e7bb74591debbde4da94773ad94bafc853bcff4cf9fac70dbb4ebb9d062ee1c1',
    MKD + '/mock_m3_E2.4.json': '8ef56f2221d6a10f554205c1ec2affd92659143185204464b6b2a91b61118e59',
    MKD + '/mock_m3_E3.3.json': '3d93cc150ca74a67e89fe9b27c4eeb056a3c9384dd2a7d465428381c813cf90c',
    MKD + '/mock_m3_E3.4.json': '9324c42a34e5afde2a620a4c5aa009085834819f27953b308ab041e6249bd8e8',
    MKD + '/mock_m3_FF.3.json': '8c4851955951e07f57618dfb80a7a477455c484e6908b5f70017b0bdd9027f28',
    MKD + '/mock_m3_FF.4.json': '74875643048a99400e1d93cfdd0b4e3e0b08188db6b4f1086299d12e9693516d',
    MKD + '/mock_m3_H.3.json': '41ea876ace45ac1d914288a8113bc0770d8d2027363c5cff128b4af4d3412b77',
    MKD + '/mock_m3_H.4.json': 'e33bc7397dad7df57122e7c8e4fcd2bb211a85682cd2448d9f7de814b95ee4df',
    MKD + '/mock_m3_L.3.json': 'f7d27dc8c20a31cf1cf5df100f36d7707681b2d950668c59b60e2783707c5c4f',
    MKD + '/mock_m3_L.4.json': '2c63822d69d1b64bad0f5ebd9f35175e9131e431af22fd30548d0bf40d764076',
    MKD + '/mock_m3_N.3.json': '96e4ae10f78714806fd5c756bc064951ce701eb6c54bf78829697acec4fdad50',
    MKD + '/mock_m3_N.4.json': '29fe50f547309fb8dc75279816d1e2dd9ab2aed60176f93f62f24f3580edb3d8',
    MKD + '/mock_m3_S4.3.json': 'ee26686b30bf59163de1b9bf675cefcf4cd49914c9bbe0b9b6995efeb3abd57d',
    MKD + '/mock_m3_S4.4.json': '431ef42f55559e3c4f5a85d0f0a197567b42f866f8fb6a84342c6c913349584f',
    MKD + '/mock_m3_asm.3.out': 'e0a9db52204aded53e59c48e57c53ecf88f9b584c06caa0713d48acdb66b3d4d',
    MKD + '/mock_m3_asm.4.out': '2e8ad23297535a77d41ebb43fbc9716dd65d3204106ebf3de555a0d878ea1586',
    MKD + '/mock_p2_run.out': '693052ad8c90f888dd0a59755b3d7eacc083aaf14abc3259bdeb34fbf04b616c',
}
PINS.update(MOCKPINS)
# stage C: the MOCK M2(b) of pk02's interface (the mock module, its record and asm output), pinned by sha256
PINS.update({
    M2BMOD: '18525cc5c62fa1f30f65ba9fd8745c07a8ac5422f101e109deea197ffc655dd2',
    M2BREC: 'eb5af0f1089e4e3e0750ba044a8a74bad685449c8b9fc8c51180ff03ba03c397',
    M2BASM: 'a085e76227bc19d810b00497d85c1dbf353a29292c63beb9ca868d8643bae0cf',
})
# stages B and C: the interval core, 3g's outputs (C-REPF and C-MAIN references) and the z9sym trial sets (odd states, lam0)
CORE = OWN + '/s8core_v1_11.py'   # v1_14: sf_pair's info record (C-MV-SF, C-TARGET-SF); v1_13 (core v1_10): C5 gates, C6 raise
G3OUT = {4: OUTD + '/out_kt_s8f3g_v1_2_n4.out', 3: OUTD + '/out_kt_s8f3g_v1_2_n3.out'}
TSF = {4: OUTD + '/ts_N4_J170_D_S_z9sym_v1.json', 3: OUTD + '/ts_N3_S_z9sym_v1.json'}
PINS.update({
    CORE: '2648d2a1629ad1362598f8e47759fa15e5e3fa43ac558541fb4aa2567e5a47d9',
    G3OUT[4]: 'ce586828e38034b147cd957fc87d761e91819805783d22d5e76f208ab5313681',
    G3OUT[3]: 'b4a17b6498bb2d92706b768c58a9d83c89c2c92e952beeb5111df61c22aacb77',
    TSF[4]: 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    TSF[3]: 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
})
REFS = [G3OUT[4], G3OUT[3], TSF[4], TSF[3]]   # reference files: pinned and listed, not inputs of the claim
# v1_12: route (b)'s certified M3 inputs, pinned by full sha256 (sha256sum when this revision was assembled): the partial asm of
# m3_run_v1_8_1 (D, E2, E3, FF) and the narrowed N record of m3_run_v1_8_2 (asmN: the 55 T,a,b and the TX,a,b with max(a, b) <= 3), each
# with its asm output and side manifest; the law certificates m3_lawcert_v1_1 (the four partial records) and m3_lawcert_v1_2 (the N
# record), each with its job output and side manifest (a reader cannot stop a forged job output that copies the banner, so each
# certificate's sha256 and both side manifests are pinned here too); every record and certificate is read through m3_reader_v6_3
# (v1_14_2; v6_2 before).
M3C = CODEDIR + '/pk03'
RBFAM = ('D', 'E2', 'E3', 'FF', 'N')
CREC = {n: dict([(f, M3C + '/out/m3_s8v3_%s_N%d_J300_v1_8_1.json' % (f, n)) for f in ('D', 'E2', 'E3', 'FF')] +
                [('N', M3C + '/out/m3_s8v3_N_N%d_J300_v1_8_2.json' % n)]) for n in (4, 3)}
CASMOF = {'D': 'P', 'E2': 'P', 'E3': 'P', 'FF': 'P', 'N': 'N'}   # the asm run that wrote each family's record
CASM = {n: {'P': M3C + '/out/m3_run_v1_8_1_asmP.%d.out' % n, 'N': M3C + '/out/m3_run_v1_8_2_asmN.%d.out' % n} for n in (4, 3)}
CSIDE = {n: {'P': M3C + '/MANIFEST_m3_run_v1_8_1_asmP.%d.sha256' % n, 'N': M3C + '/MANIFEST_m3_run_v1_8_2_asmN.%d.sha256' % n}
         for n in (4, 3)}
CLAW = {n: {'P': (M3C + '/out/m3_lawcert_v1_1_N%d.json' % n, M3C + '/out/m3_lawcert_v1_1_%d.out' % n,
                  M3C + '/MANIFEST_m3_lawcert_v1_1_N.%d.sha256' % n, ('D', 'E2', 'E3', 'FF')),
            'N': (M3C + '/out/m3_lawcert_v1_2_N%d.json' % n, M3C + '/out/m3_lawcert_v1_2_%d.out' % n,
                  M3C + '/MANIFEST_m3_lawcert_v1_2_N.%d.sha256' % n, ('N',))} for n in (4, 3)}
PINS.update({
    CREC[4]['D']: '389be198d9fe919e1a097865759691847a9e4dc7553275c083d91bd753819b00',
    CREC[4]['E2']: 'e900cbfed6a8a69e57f849733d4740787c978c58761ea4f0fcffbf95293ee18e',
    CREC[4]['E3']: 'd1df7d4fc1b8e25f266f34c32180ccb771bc1719cc0fa730f240a33179feff0d',
    CREC[4]['FF']: '042e8fc888243ac939fb9be4968f8fc9d42262a1deb7bf690993fc22a82f2a89',
    CREC[4]['N']: '4afe8f5ba75d29cbf89f0c0940c9d7790b9a215cbf1faba6f4759d1fdd7b28d6',
    CASM[4]['P']: '08c8fab3f4b9080424a40c8cb61b7932f557852520e8d49c5915092a8963a127',
    CASM[4]['N']: '66a663de3924e2d8f8af1cdd65bfd88c0edc77cca9313f4dd2ef8cfb09eac3d9',
    CSIDE[4]['P']: 'ce1d15f46dcfb3ebac61a25ba0c7a6b1708e4aad1c7faf10b65e63b393b81868',
    CSIDE[4]['N']: 'f9ea5944653a75fce9364dbdd39cd9451632283a01c545abf844dae50a525f8e',
    CLAW[4]['P'][0]: '5b7cbff9443f4ff69e623caa776646b16629aa2b6436c186e1799e9f4d56ba4c',
    CLAW[4]['P'][1]: 'f814f9f301f8814117dfccbd6715f8ff04e6cd24dcef04e4a95ecaaeb6e37325',
    CLAW[4]['P'][2]: '4b819fb1d0e5d101a5eeaf5d1062a16d0092ddf3a1ed96a2fab6917e3bd80e9d',
    CLAW[4]['N'][0]: '77cb4f7c05df69c5e185ecd14aeea8fb9caca8d98e306b549390d34163f190d6',
    CLAW[4]['N'][1]: '10bc81fc53d21e3a5fff08945a1e890438145bbcee2dcc73033e7c33a37e4bb5',
    CLAW[4]['N'][2]: 'ef278052dcf9908b2da7889b606520d5d138293406fa5116a6455055715551a2',
    CREC[3]['D']: '8707107b0ebc3dea6989d22b6284f9df368c954837c883dc36824edda63c4926',
    CREC[3]['E2']: '3e7f7bf6101bc45282a202d85e3182b2340bff4d7d349bc78eb33d5d9f02f5d5',
    CREC[3]['E3']: '6cd3dffbc6fac0845d05aa4b88f135c28a8091eb9623b779d874dace550a078a',
    CREC[3]['FF']: 'dae3cfa88bf06fd97378108b9ceba0a85044f7790b38e67c0b86eb23d6443008',
    CREC[3]['N']: '87f09d3ee43e44d7572e49b40f7103d2e1ef2b7409a1cb24b67d117b4145315a',
    CASM[3]['P']: 'b6e9c2dd6a6308f6dc8d72124ba37326156983ec3444625d152ab46f28e927ed',
    CASM[3]['N']: 'c1544e32848907c28ea30bf9e6e404fa836176947ce2f6f23e22ae4895c4697e',
    CSIDE[3]['P']: 'fba45a69a1b07922da1a376bcac9148c0ae2287ce1f078e4f15c451a60ec90f1',
    CSIDE[3]['N']: '01d589bdde5ae9ce5e2528417145805b183aab4c2db80c9850ae1de7973683bb',
    CLAW[3]['P'][0]: 'ec50ab52cd88b7b0cbd717c6dc4db295e72a8faf10b378b994a4f83cc5d7cfd4',
    CLAW[3]['P'][1]: '2b7847dc902eed4dda6800ff2118d8c378421179ba4d77242b83dc9086c772d9',
    CLAW[3]['P'][2]: '781fe1f6c7ce204db33c7ccfa0c04adf4c022da08eccd27823add882fb7536de',
    CLAW[3]['N'][0]: '819c100913e917d09bbf7788b9dba75f15584f232784b9601e9a19e266c7f70c',
    CLAW[3]['N'][1]: 'ec6b099bc6517e11af92cfc641592719202bbe2dd234a2f87cce0e0a54276357',
    CLAW[3]['N'][2]: 'a3c03c910c4955d4429f4e86a652ad683601b8f41d8f21ffb4f9a45e84940490',
})
PINS.update({   # v1_12_1: pk02's certified M2(b), pinned by full sha256 (sha256sum when this revision was assembled)
    CERT_M2B[0]: '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',
    CERT_M2B[1]: 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391',
    M2BRD: 'a9f15db48e9fa51629448181d8a83679c1b93cd2b5696c8ed1e6b41d60df8b02',
    M2BSIDE: 'bab46e982597d9b3ebf92b53c59077e85aae96683b0626ad97e8d0e4fc42c787',
    CERT_P2[0]: '10f3c3d9a18b9c7a596121a8dbec7d2b82afb366704845a7c00e066c8bf6d4f6',
    CERT_P2[1]: '58814f7f59dd0d8e9d16b73084b3cc5072f94fb1138300a112e0e49ff017835f',
    P2SIDE: '27d1efa6ed2388617eadda1523570f84c3d228ee230df2686f6cbc621c64ba12',
})
# v1_13: pk07's certified side check of Lemma 19.2 (c+) (the review hand-checked OK, 11e73a7f); the S_V vertical export
# is valid only together with it (the index of the S_V evidence: notes/SV_EVIDENCE_MANIFEST_v1.sha256, 0e9bee51)
CPLUS = CODEDIR + '/pk07/out/cplus_sidecheck_v1.kv'
PINS.update({CPLUS: 'a3d0b24d27b879c00a89757bea19e6c11020ee640569737c589ec6fb66f577eb'})
PINS.update({   # v1_14_2: pk03's certified D16 records for N = 4, their asm output and freeze side manifest (full sha256)
    D16[4]['H']: 'cec396204778d2835cc06bef10964928daad9d81ead35987c2762f26bc2d3b7a',
    D16[4]['S4']: '42af2d76c14bb7d2a9b0d1887fbe683c79b417e1d191d7cbd8de65e7f3280e40',
    D16[4]['asm']: 'd028879d269d03888d98707f7e9220bc5cc0623ada99d4507c7751afa3f66dd3',
    D16[4]['side']: 'd85c08ece527b61af58450bd645fe41793a4aa80a6a0cdf70402676514395d5e'})
PINS.update({   # v1_14_3: pk03's certified D16 records for N = 3, their asm output and freeze side manifest (full sha256)
    D16[3]['H']: '083797ea6b4ef0452f2d8f42f994db58df2093a499281eca336a772316a23308',
    D16[3]['S4']: 'afd54944e6af8ec70779e7cfe5c5ecad0ff4daf4f4a7f8572cbe05241f4ed651',
    D16[3]['asm']: '78f2863f957244472033c34163bcaced0e5a19041d776d7b58b4efc0db5ee59f',
    D16[3]['side']: '8d20c6852dba23142a515c4518d606bc5ff89e45c01e664c5287c354d3ebf649'})
if MODE == 'cert':   # C-REPF stays like for like on 3g's data: the MOCK records, M2(b) law and P2 export are reference files there
    REFS += M3MOCK[4] + M3MOCK[3] + [M3ASM[4], M3ASM[3], P2MOCK, P2MOCKR, M2BMOD, M2BREC, M2BASM]
# v1_9 (the parity condition 1): the symmetrized vacres polynomials written with the trial set by zero_states_v2 (291c9891; re-checked
# byte-equal by zero_states_v2_1 bf4bd4c7, record 168106e0): C-SYMIN reads their stored decimals; reference files, not inputs of the claim
VRF = {4: OUTD + '/vacres_K3_N4_sym_v1.json', 3: OUTD + '/vacres_K3_N3_sym_v1.json'}
PINS.update({
    VRF[4]: 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    VRF[3]: 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
})
REFS += [VRF[4], VRF[3]]
# v1_12_2: the certified P2 export, its run output and the runs manifest are inputs in both modes (tagged by run_A), no longer references


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('%s sha256 %s MODE=%s ITEM=%s%s LIM=%d (RLIMIT_CPU soft %d, hard %d)%s' % (
    LABEL, sha_file(os.path.abspath(__file__)), MODE, ITEM, (' N=%d A=%d B=%d' % CHUNK) if CHUNK else '', LIM, LIM, LIM + 5,
    (' TAG=%s' % RTAG[1:]) if RTAG else ''))
_bad = ['%s %s' % (p, sha_file(p)) for p in sorted(PINS) if sha_file(p) != PINS[p]]; import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_SELF = 'a6eea55f1f05d1809b7f81be8cbc4aef10d66e9a0e2705a0ba2b93a60bdec604'; ORIG_DIGEST = '973e9d68f8277f1623a7534410cfd9f8e61196a86fa37f821eda22e6257999fa'  # G-ORIG: option (C), acc2 two-producer acceptance
out('C-HASH %s (%d files)%s' % ('PASS' if not _bad else 'FAIL', len(PINS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)


def _module(path, name):
    """import a pinned file as a module (its sha256 was checked by C-HASH; checked again here). v1_14_2: a load that changes
    flint's process-global ctx.prec is logged in PREC_LOG (not undone), and C-PREC fails on it at the item's end."""
    if sha_file(path) != PINS[path]:
        raise ValueError('%s does not match its pin' % path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    before = ctx.prec
    spec.loader.exec_module(mod)
    if ctx.prec != before:
        PREC_LOG.append((name, before, ctx.prec))
    return mod


def prec_ok(prec, log):
    """v1_14_2 C-PREC's predicate: the run's precision held, and no module load changed it."""
    return prec == PREC and not log


M3R = _module(M3RD, 'm3_reader_v6_3')
M3R4 = _module(M3RD4, 'm3_reader_v4_4')
P2R = _module(P2RD, 'kt_s67_export_reader_v2')
KVR = _module(KVRD, 's4u_kv_ref_v1')
CM = _module(CORE, 's8core_v1_11')   # imported after ctx.prec = 256, so its module constants are computed at that precision
PM0 = CM.pm   # v1_12_3: s8core's own pm(), which end_chain wraps for one point chain at a time and restores
M2BM = _module(M2BMOD, 'm2b_reader_v1_mock')
BADWORDS = ('PRECERT', 'STUB', 'MOCK')
CERT_OK = [False]   # set only by a cert-mode final after every gate and plant has passed (write_record_C)


class Refused(Exception):
    pass


def read_text(path):
    with open(path) as fh:
        return fh.read()


def gate(fails, name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


def plant(nofire, name, fn):
    """a must-fire plant: fn must raise Refused, the reader's refusal."""
    try:
        fn()
    except Refused as e:
        out('%s: refused (%s) -> FIRES' % (name, str(e)[:160]))
        return
    except Exception as e:
        out('%s: raised %r instead of a refusal -> DOES NOT FIRE' % (name, e))
        nofire.append(name)
        return
    out('%s: accepted -> DOES NOT FIRE' % name)
    nofire.append(name)


# ---------------------------------------------------------------- (M3)
REQUIRED = (['g,%d,%d' % (a, b) for a in range(4) for b in range(a, 4)] + ['DY,%d' % a for a in range(4)] + ['DYY'] +
            ['T,%d,%d' % (a, b) for a in range(4) for b in range(a, 4)] + ['TX,%d,%d' % (a, b) for a in range(4) for b in range(a, 4)] +
            ['e,%d' % a for a in range(4)] + ['eX,%d' % a for a in range(4)] + ['f,%d' % a for a in range(4)] +
            ['fX,%d' % a for a in range(4)] + ['z', 'wXw', 'wXwX'] +
            ['h,%d' % a for a in range(4)] + ['hX,%d' % a for a in range(4)])
# v1_12 (route (b)): no TT entry; the B chain's g and T over the largest trial set B6 (states 0..6)
RB_SETS = {'B4': (0, 1, 2, 3, 4), 'B5': (0, 1, 2, 3, 4, 5), 'B6': (0, 1, 2, 3, 4, 5, 6)}
RB_ORDER = ('B5', 'B6', 'B4')   # per piece B5 or B6, both valid; B4 only if it ever passes (first passing set taken)
JX4 = 350   # v1_12_1: the route H junction at N4 (340, 345 or 350 after pk08's pre-check); S8's N4 range is J >= JX4
REQUIRED = REQUIRED + ['%s,%d,%d' % (nm, a, b) for nm in ('g', 'T') for a in RB_SETS['B6'] for b in RB_SETS['B6'] if a <= b and b >= 4]
# S8 list v2's 18 S4 entries: Z, the seven bonds' x, the ten n = 4 pairs' xy (the chain's Z4, X1, X1X2 are S4,Z, S4,x,1,TM, S4,xy,1,TM,2,TM)
S4BONDS = [(0, 'TM'), (1, 'TM'), (1, 'MB'), (2, 'TM'), (2, 'MB'), (3, 'TM'), (3, 'MB')]
N4PAIRS = [('n4 same 1-2', 'same', (0, 'TM'), (1, 'TM')), ('n4 flip 1-2', 'flip', (0, 'TM'), (1, 'MB')),
           ('n4 same 2-3', 'same', (1, 'TM'), (2, 'TM')), ('n4 flip 2-3', 'flip', (1, 'TM'), (2, 'MB')),
           ('n4 same 1-3', 'same', (0, 'TM'), (2, 'TM')), ('n4 flip 1-3', 'flip', (0, 'TM'), (2, 'MB')),
           ('n4 same 1-4', 'same', (0, 'TM'), (3, 'TM')), ('n4 flip 1-4', 'flip', (0, 'TM'), (3, 'MB')),
           ('n4 same 3-4', 'same', (2, 'TM'), (3, 'TM')), ('n4 flip 3-4', 'flip', (2, 'TM'), (3, 'MB'))]
REQUIRED = REQUIRED + ['S4,Z'] + ['S4,x,%d,%s' % cb for cb in S4BONDS] + ['S4,xy,%d,%s,%d,%s' % (p[2] + p[3]) for p in N4PAIRS]


def _bind(name, data, out_text):
    """m3_reader_v4_4's binding rule, for the MOCK path: VERDICT lines exactly ['VERDICT VALID'], one RECORD line with the sha256."""
    lines = out_text.split('\n')
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise Refused("%s: the asm output's VERDICT lines are not exactly ['VERDICT VALID']" % name)
    hit = [ln.split() for ln in lines if ln.startswith('RECORD ') and len(ln.split()) == 3 and ln.split()[1] == name]
    if len(hit) != 1 or hit[0][2] != hashlib.sha256(data).hexdigest():
        raise Refused('%s: the asm output does not name this file with its sha256 on exactly one RECORD line' % name)


def m3_text(text, out_text, name, N, mode):
    """(M3) on texts: the record file's content, its asm output's content and the record's base name."""
    if mode == 'CERTIFIED':
        try:
            rec = M3R.loads(text, out_text, 300, int(N), name)
        except Exception as e:
            raise Refused('m3_reader_v6_3: %s' % e)
    elif mode == 'MOCK':   # v1_12: the MOCK records carry no laws, so their item checks stay m3_reader_v4_4's (M3R4, pinned)
        _bind(name, text.encode(), out_text)
        try:
            raw = json.loads(text)
        except ValueError as e:
            raise Refused('%s: not JSON (%s)' % (name, e))
        if raw.get('format') != 'M3_RECORD_v1_MOCK' or raw.get('claim') != 'MOCK ' + M3R4.CERT_CLAIM:
            raise Refused('%s: not a MOCK M3 record (format %r)' % (name, raw.get('format')))
        if raw.get('J_REF') != 300 or raw.get('N') != N:
            raise Refused('%s: J_REF %r, N %r' % (name, raw.get('J_REF'), raw.get('N')))
        if (raw.get('kernel_file'), raw.get('kernel_sha256'), raw.get('kernel_prec'), tuple(raw.get('validation') or ())) != (
                M3R4.VALIDATED_LAYER[0], M3R4.VALIDATED_LAYER[1], M3R4.KERNEL_PREC, tuple(M3R4.VALIDATED_LAYER[2])):
            raise Refused('%s: kernel fields differ from the reader\'s' % name)
        try:
            items, ents, ofs = M3R4._items(raw, name, 300)
        except Exception as e:
            raise Refused('%s: item check: %s' % (name, e))
        rec = {'balls': {k: ([Fraction(a) - Fraction(r) for a, r in zip(v[0], v[2])], [Fraction(a) + Fraction(r) for a, r in zip(v[0], v[2])],
                             sum(Fraction(x) for x in items[k]['Bp'].values())) for k, v in ents.items()},
               'parity': {k: items[k]['parity'] for k in ents}}
    else:
        raise ValueError(mode)
    E = {}
    for key in rec['balls']:
        LO, HI, err = M3R.entry_ball(rec, key) if mode == 'CERTIFIED' else rec['balls'][key]
        if len(LO) != 4 or any(lo > hi for lo, hi in zip(LO, HI)) or err < 0:
            raise Refused('%s: entry %s malformed' % (name, key))
        E[key] = (LO, HI, err)
    return E


def load_m3(paths, asm_out, N, mode):
    """(M3) the files of one N, merged; a key met twice is refused."""
    atext = read_text(asm_out)
    E = {}
    for path in paths:
        part = m3_text(read_text(path), atext, os.path.basename(path), N, mode)
        dup = sorted(set(part) & set(E))
        if dup:
            raise Refused('%s: keys met twice %s' % (os.path.basename(path), dup[:4]))
        E.update(part)
    return E


# ---------------------------------------------------------------- strict KV, (M2B) and (S4)
def kv(text, what):
    try:
        d = KVR.parse_s4u_kv(text)
    except ValueError as e:
        raise Refused('%s: %s' % (what, e))
    for k in ('FORMAT', 'RECORD', 'TAG', 'CLAIM', 'EXPORT_STATUS'):
        if k in d and any(w in d[k].upper() for w in ('PRECERT', 'STUB')):
            raise Refused('%s: PRECERT/STUB in %s' % (what, k))
    return d


def m2b_text(text, name, asm_text, mode):
    """(M2B) on texts, pk02's interface (agreed 2026-11-07): CERTIFIED: m2b_reader_v1.loads once it is frozen and pinned (M2BRD; not
    in this version, so this path refuses after the FORMAT line, and the mock is refused by its format); MOCK: the mock module's loads
    (MOCK formats only). Returns (module, rec); every refusal raises Refused."""
    if mode == 'CERTIFIED':
        fm = re.search(r'^FORMAT = (.*)$', text, re.M)
        if fm is None or fm.group(1) != 'M2B_KV_v1':
            raise Refused('M2(b): not a certified M2B_KV_v1 record (FORMAT %r)' % (fm.group(1) if fm else None))
        if M2BRD is None:
            raise Refused('M2(b): m2b_reader_v1 is not pinned in this version')
        mod = _module(M2BRD, 'm2b_reader_v1')
        try:
            return mod, mod.loads(text, name, asm_text)
        except ValueError as e:
            raise Refused('m2b_reader_v1: %s' % e)
    if mode != 'MOCK':
        raise ValueError(mode)
    try:
        return M2BM, M2BM.loads(text, name, asm_text)
    except ValueError as e:
        raise Refused(str(e))


def m2b_trial_bad(text):
    """C-TRIAL M2B (v1_12_1; as kt_s9h_v1_1's m2b_trial_bad): the certified M2(b) record's one PIN_TRIAL line names, for
    both N, the symmetrized vacres VRF[N] (the file C-SYMIN checks) as '<path relative to code>:<its full sha256>' exactly once, and no
    other vacres file. Returns the failures."""
    pl_ = [ln for ln in text.split('\n') if ln.startswith('PIN_TRIAL')]
    if len(pl_) != 1 or not pl_[0].startswith('PIN_TRIAL = '):
        return ['%d PIN_TRIAL lines' % len(pl_)]
    toks = pl_[0][len('PIN_TRIAL = '):].split(' ; ')
    want = {N: '%s:%s' % (os.path.relpath(VRF[N], CODEDIR), PINS[VRF[N]]) for N in (4, 3)}
    bad = ['N=%d: %s named %d times' % (N, w, toks.count(w)) for N, w in want.items() if toks.count(w) != 1]
    return bad + ['another vacres pin %s' % t for t in toks if 'vacres' in t and t not in want.values()]


def m2b_load(path, asm_out, mode):
    """(M2B) from files: CERTIFIED through m2b_reader_v1.load(path, asm_out, expected_sha256), its certified entry point (the binding
    and C-PINS), after the FORMAT check of m2b_text; MOCK through the mock module's load."""
    if mode == 'CERTIFIED':
        fm = re.search(r'^FORMAT = (.*)$', read_text(path), re.M)
        if fm is None or fm.group(1) != 'M2B_KV_v1':
            raise Refused('M2(b): not a certified M2B_KV_v1 record (FORMAT %r)' % (fm.group(1) if fm else None))
        if M2BRD is None:
            raise Refused('M2(b): m2b_reader_v1 is not pinned in this version')
        mod = _module(M2BRD, 'm2b_reader_v1')
        try:
            return mod, mod.load(path, asm_out, PINS[path])
        except ValueError as e:
            raise Refused('m2b_reader_v1.load: %s' % e)
    if mode != 'MOCK':
        raise ValueError(mode)
    try:
        return M2BM, M2BM.load(path, asm_out)
    except ValueError as e:
        raise Refused(str(e))


S4CLAIM = {'S4_U_CERTIFIED_v2': ('CLAIM_F2', 'for N in {3, 4} and every t = 1/J in (0, 1/300]: tr_H(T^2)/lambda_h^2 <= N*_LEAD_HI (1 + N*_C1_HI t + '
                                              'N*_C2_HI t^2 + N*_C3_HI t^3) + N*_R_CERT'),
           'S4_TRB_CERTIFIED_v1': ('CLAIM', 'for N in {3, 4} and every J >= 300 (t = 1/J <= 1/300): tr_H(T_xi)/lambda_h <= N*_TRB, one '
                                            'constant per N')}
S4CLAIM['S4_U_CERTIFIED_v3'] = S4CLAIM['S4_U_CERTIFIED_v2']   # v1_12: v3 carries v2's F2 form with the same claim text
S4KEYS = {'S4_U_CERTIFIED_v2': ('LEAD_HI', 'C1_HI', 'C2_HI', 'C3_HI', 'R_CERT'), 'S4_TRB_CERTIFIED_v1': ('TRB',)}
S4KEYS['S4_U_CERTIFIED_v3'] = S4KEYS['S4_U_CERTIFIED_v2']


def s4_text(text, record):
    d = kv(text, record)
    if d.get('FORMAT') != 'S4U_KV_v1' or d.get('RECORD') != record or d.get('END') != record:   # v1_12_2: END too
        raise Refused('%s: FORMAT/RECORD/END' % record)
    for k in ('FORMAT', 'RECORD', 'TAG', 'CLAIM'):
        if 'MOCK' in d.get(k, '').upper():
            raise Refused('%s: MOCK in %s' % (record, k))
    ck, ctext = S4CLAIM[record]
    if d.get(ck) != ctext:
        raise Refused('%s: %s differs from the pinned claim text' % (record, ck))
    vals = {}
    for n in (4, 3):
        # v1_3: the record's own verdict keys, so a re-pin to a non-VALID record fails here
        if record == 'S4_TRB_CERTIFIED_v1':
            if d.get('N%d_VERDICT' % n) != 'VALID' or d.get('N%d_T2_RESULT' % n) != 'PASS':
                raise Refused('%s: N%d_VERDICT %r, N%d_T2_RESULT %r' % (record, n, d.get('N%d_VERDICT' % n), n, d.get('N%d_T2_RESULT' % n)))
        else:
            ents = [x.strip() for x in d.get('N%d_VERDICTS' % n, '').split(';')]
            if not ents or any(not e or e.split()[-1] != 'VALID' for e in ents):
                raise Refused('%s: N%d_VERDICTS %r' % (record, n, d.get('N%d_VERDICTS' % n)))
        for k in S4KEYS[record]:
            v = d.get('N%d_%s' % (n, k))
            if v is None or re.fullmatch(r'[-+]?[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?', v) is None:
                raise Refused('%s: N%d_%s %r' % (record, n, k, v))
            vals[(n, k)] = Fraction(v)
    return vals


# ---------------------------------------------------------------- (P2)
P2FIELDS = ('jlo', 'jhi', 'c5_lo', 'Bp_hi', 'Bm_hi', 'Rw_hi', 'rho1_hi', 'c_lo', 'c_hi')


def p2_text(text, run_text, name, mode):
    """(P2) on texts; name is the export's base name. CERTIFIED: pk07's bound reader loads (V2 binding, EXPORT_STATUS CERTIFIED,
    RUN_VERDICT VALID). MOCK: the same binding (the reader's _bound), then loads_noncert, which refuses a CERTIFIED export."""
    try:
        if mode == 'CERTIFIED':
            ex = P2R.loads(text, run_text, name)
        elif mode == 'MOCK':
            P2R._bound(name, text.encode('utf-8'), run_text)
            ex = P2R.loads_noncert(text)
        else:
            raise ValueError(mode)
    except ValueError as e:
        raise Refused('P2: %s' % e)
    h = ex['header']
    for k in ('FORMAT', 'RECORD', 'EXPORT_STATUS', 'TAG'):
        if any(w in h.get(k, '').upper() for w in ('PRECERT', 'STUB')):
            raise Refused('P2: PRECERT/STUB in %s' % k)
    if h.get('FORMAT') != 'S4U_KV_v1' or h.get('RECORD') != 'EXPORT_KT_S67_v1' or h.get('END') != 'EXPORT_KT_S67_v1':
        raise Refused('P2: FORMAT/RECORD/END')
    if h.get('RUN_VERDICT') != 'VALID':
        raise Refused('P2: RUN_VERDICT %r' % h.get('RUN_VERDICT'))
    if mode == 'CERTIFIED':
        if h.get('EXPORT_STATUS') != 'CERTIFIED' or 'MOCK' in (h.get('TAG', '') + h.get('EXPORT_STATUS', '')).upper():
            raise Refused('P2: EXPORT_STATUS %r is not CERTIFIED' % h.get('EXPORT_STATUS'))
        st = [k for k in h if k.startswith('TAG_') and k.endswith('_STATUS')]
        if not st or any(h[k] != 'certified' for k in st):
            raise Refused('P2: an input tag is not certified')
    elif mode == 'MOCK':
        if h.get('EXPORT_STATUS') != 'MOCK' or not h.get('TAG', '').startswith('MOCK'):
            raise Refused('P2 mock: EXPORT_STATUS/TAG')
    else:
        raise ValueError(mode)
    fields = ex['fields']
    if any(f not in fields for f in P2FIELDS):
        raise Refused('P2: fields missing %s' % [f for f in P2FIELDS if f not in fields])
    pieces = {}
    for n in (4, 3):
        pe = ex['pieces'].get(n, {})
        if h.get('N%d_PIECES' % n) != '904' or sorted(pe) != list(range(904)):
            raise Refused('P2: N%d pieces %r (%d piece lines)' % (n, h.get('N%d_PIECES' % n), len(pe)))
        rows = []
        for i in range(904):
            row = {f: pe[i][f] for f in P2FIELDS}   # jlo, jhi floats by rule V1 (the reader's parse); the rest exact Fractions
            if not isinstance(row['jlo'], float) or not isinstance(row['jhi'], float):
                raise Refused('P2: N%d piece %d grid ends are not floats' % (n, i))
            rows.append(row)
        if rows[0]['jlo'] != 300.0 or rows[-1]['jhi'] != float('inf') or any(rows[k]['jhi'] != rows[k + 1]['jlo'] for k in range(903)) or \
                any(r['jlo'] >= r['jhi'] for r in rows):
            raise Refused('P2: N%d grid not contiguous from 300 to inf' % n)
        pieces[n] = rows
    return pieces, h


# ---------------------------------------------------------------- input tags, loaders, the writer and the S8 record reader
STATUS_KEYS = ('FORMAT', 'RECORD', 'TAG', 'CLAIM', 'EXPORT_STATUS')
PARZ_EXPECTED = sorted(k for k in REQUIRED if k.split(',')[0] in ('g', 'T', 'e', 'f', 'h') and
                       sum(1 for x in k.split(',')[1:] if int(x) in (2, 5, 8)) == 1)   # v1_12: route (b)'s keys (no TT; g, T to state 6)
S8CLAIM = ('for N = 4 and every J >= 350, and for N = 3 and every J >= 300 (every piece of P2\'s grid from the piece that contains that J): '
           'Cov(X, Y) > 0 for every vertical pair of SPEC_S8_CERT_v1 sect. 1 in S8-1, S8-2 and S8-3 (n = 4): on route (b) (U9 from a '
           'trial-basis chain B4, B5 or B6 per piece on g and T alone; the W3 chain with H and S4 at dmaxH 16 and without TT) each row of '
           'the route rule has a certified lower end > 0 and each class\'s top mode covers every m >= m0 with m0 <= 8 (kt_s8_cert; '
           'SPEC_S8_CERT_v1 with ADD1 and ADD2; the N = 4 band [300, 350) is route H\'s)')   # v1_12_1: the review aad21227's parenthesis
TAGS = {}        # path -> (sha256, 'CERTIFIED' or 'MOCK'): every input of the claim, by the path that read it
A_DIGEST = ['']  # this run's INPUTS digest: the tags, the reference files and the core


def tag(path, status):
    TAGS[path] = (sha_file(path), status)


def cert_tags_ok(tags):
    """a certified S8 record needs every input of the claim read through a certified path."""
    return bool(tags) and all(st == 'CERTIFIED' for p, sh, st in tags)


TRIAL = {}   # v1_10: certified M3 record path -> C-TRIAL failures (v1_12: filled by rb_load)


def trial_bad(top, N):
    """C-TRIAL (v1_10, v1_12: the full sha256 only): a certified M3 record's trial_set must be {'ts': '<base name>:<sha256>',
    'vacres': '<base name>:<sha256>'} naming TSF[N] and VRF[N] (the files C-SYMIN checks) with their full sha256s. Route (b)'s records
    (m3_run_v1_8_1, m3_run_v1_8_2) carry the full sha256s themselves, so v1_11's engine chain for sha8 trial sets (chain_bad) is not
    needed and is gone. Returns the failures."""
    ts = top.get('trial_set')
    if not isinstance(ts, dict) or set(ts) != {'ts', 'vacres'}:
        return ['trial_set %r' % (ts,)]
    bad = []
    for key, path in (('ts', TSF[N]), ('vacres', VRF[N])):
        v = ts[key]
        m = re.fullmatch(r'([A-Za-z0-9_.]+):([0-9a-f]{64})', v) if isinstance(v, str) else None
        if m is None or m.group(1) != os.path.basename(path) or PINS[path] != m.group(2):
            bad.append('%s %r is not %s:<its full sha256>' % (key, v, os.path.basename(path)))
    return bad


# ---- v1_12: route (b)'s M3 inputs. The families pk03 has certified (D, E2, E3, FF of m3_run_v1_8_1's partial asm; the narrowed N of
# m3_run_v1_8_2's asmN) are read through the certified path in both modes, with their law certificates; H and S4 come from D16 records
# in cert mode (pending: not pinned, so cert mode stops) and from the MOCK records, every bar times the D16 floor, in mock mode.
# v1_14_2: D16 (the certified D16 records per N), D16_CERT_IN_MOCK and D16_PINNED are set with the run's other certified inputs above
D16BAD = {}   # v1_14_2: N -> C-SIDEMAN failures of the D16 side manifest (filled by rb_entries)
D16FLOOR = {'h': Fraction('11.8'), 'hX': Fraction('11.8'), 'S4': Fraction('9.3')}   # pk03 2026-11-07: lower bounds of D16's multipliers
M3MOCKHS = {n: [os.path.join(MKD, 'mock_m3_%s.%d.json' % (f, n)) for f in ('H', 'S4')] for n in (4, 3)}
NFAM = ('T', 'TX')   # the N family's graphs (C-NSCOPE)


def side_bad(side, files, text=None):
    """C-SIDEMAN: a pinned side manifest (sha256sum lines, paths relative to pk03/): every listed file has the listed sha256, and
    every file of files is listed. Returns the failures. v1_14_3: text, the manifest's text in place of the file's, is
    PLANT-SIDEBAD's only."""
    bad, seen = [], set()
    for ln in (read_text(side) if text is None else text).split('\n'):
        if not ln.strip():
            continue
        p = ln.split()
        if len(p) != 2 or re.fullmatch('[0-9a-f]{64}', p[0]) is None:
            bad.append('line %r' % ln[:60])
            continue
        path = os.path.join(M3C, p[1])
        if sha_file(path) != p[0]:
            bad.append('%s: sha256 differs' % p[1])
        seen.add(os.path.realpath(path))
    return bad + ['%s not listed' % os.path.basename(f) for f in files if os.path.realpath(f) not in seen]


def rb_load(N):
    """route (b)'s certified M3 inputs of one N, through m3_reader_v6_3 only: the five records (D, E2, E3, FF of the partial asm, N of
    asmN), each by load(path, asm output, 300, N), the reader's only certified entry point (VERDICT lines exactly ['VERDICT VALID'], the
    RECORD line's sha256, the certified FORMAT and claim, the validated layer, each free entry's laws checked); the two law certificates
    by load_lawcert(path, job output, 300, N, {family: record}) (the producer pin: m3_lawcert_v1_1 for the four partial records,
    m3_lawcert_v1_2 for the N record; the exact records map); C-TRIAL on every record; the four side manifests (C-SIDEMAN). Every file
    is pinned above by its full sha256 and tagged CERTIFIED. Returns (records by family, certificates by asm, C-SIDEMAN failures)."""
    recs, bad = {}, []
    for f in RBFAM:
        path, asm = CREC[N][f], CASM[N][CASMOF[f]]
        try:
            recs[f] = M3R.load(path, asm, 300, N)
        except Exception as e:
            raise Refused('m3_reader_v6_3.load: %s: %s' % (os.path.basename(path), e))
        TRIAL[path] = trial_bad(recs[f]['top'], N)
        tag(path, 'CERTIFIED')
    for k in ('P', 'N'):
        tag(CASM[N][k], 'CERTIFIED')
        tag(CSIDE[N][k], 'CERTIFIED')
        bad += ['%s: %s' % (os.path.basename(CSIDE[N][k]), b) for b in
                side_bad(CSIDE[N][k], [CREC[N][f] for f in RBFAM if CASMOF[f] == k] + [CASM[N][k]])]
    certs = {}
    for k in ('P', 'N'):
        cpath, jout, side, fams = CLAW[N][k]
        try:
            certs[k] = M3R.load_lawcert(cpath, jout, 300, N, {f: recs[f] for f in fams})
        except Exception as e:
            raise Refused('m3_reader_v6_3.load_lawcert: %s: %s' % (os.path.basename(cpath), e))
        for p in (cpath, jout, side):
            tag(p, 'CERTIFIED')
        bad += ['%s: %s' % (os.path.basename(side), b) for b in side_bad(side, [cpath, jout])]
    return recs, certs, bad


def d16_use(N, mode):
    """v1_14_2: whether N's H and S4 come from its pinned D16 records (cert mode; mock mode too with D16_CERT_IN_MOCK)."""
    return D16[N] is not None and (mode == 'CERTIFIED' or D16_CERT_IN_MOCK)


def rb_entries(N, recs, certs, mode):
    """every entry the records hold, {record key: (LO, HI, err_b)} (entry_ball: ak -+ ak_rad exactly, err_b the sum of Bp), with
    {record key: the certificate's law (entry_law; None for H and S4)} and {record key: family}. v1_14_2: H and S4 from N's pinned D16
    records where d16_use (load(path, asm, 300, N) through m3_reader_v6_3; C-TRIAL on each; no law certificate, so laws None and the
    certified bars; the side manifest's failures in D16BAD[N]); in cert mode without them refused; else from the MOCK records with every
    bar times the D16 floor (tagged MOCK)."""
    allE, laws, fam = {}, {}, {}
    for f in RBFAM:
        for key in recs[f]['balls']:
            if key in allE:
                raise Refused('key %s in two records' % key)
            allE[key] = M3R.entry_ball(recs[f], key)
            laws[key] = M3R.entry_law(certs[CASMOF[f]], f, key)
            fam[key] = f
    if d16_use(N, mode):
        for f in ('H', 'S4'):
            path = D16[N][f]
            try:
                rec = M3R.load(path, D16[N]['asm'], 300, N)
            except Exception as e:
                raise Refused('m3_reader_v6_3.load: %s: %s' % (os.path.basename(path), e))
            TRIAL[path] = trial_bad(rec['top'], N)
            for key in rec['balls']:
                if key in allE:
                    raise Refused('key %s in two records' % key)
                allE[key], laws[key], fam[key] = M3R.entry_ball(rec, key), None, f
            tag(path, 'CERTIFIED')
        tag(D16[N]['asm'], 'CERTIFIED')
        tag(D16[N]['side'], 'CERTIFIED')
        D16BAD[N] = side_bad(D16[N]['side'], [D16[N]['H'], D16[N]['S4'], D16[N]['asm']])
        return allE, laws, fam
    if mode == 'CERTIFIED':
        raise Refused('the D16 H and S4 records of N = %d are not pinned in this version (pending)' % N)
    for key, (LO, HI, err) in load_m3(M3MOCKHS[N], M3ASM[N], N, 'MOCK').items():
        g = key.split(',')[0]
        if g not in D16FLOOR or key in allE:
            raise Refused('MOCK H/S4 key %s' % key)
        allE[key], laws[key], fam[key] = (LO, HI, err * D16FLOOR[g]), None, ('S4' if g == 'S4' else 'H')
    for p in M3MOCKHS[N] + [M3ASM[N]]:
        tag(p, 'MOCK')
    return allE, laws, fam


def fetch(allE, keys, scope):
    """the entries stage C reads, by record key: a key of the N family outside the N record's scope_keys, and any key no record holds,
    is refused (C-NSCOPE's teeth; PLANT-NSCOPE asks for TX,4,4)."""
    res = {}
    for k in keys:
        if k.split(',')[0] in NFAM and k not in scope:
            raise Refused('%s is outside the N record\'s scope_keys' % k)
        if k not in allE:
            raise Refused('%s is in no record' % k)
        res[k] = allE[k]
    return res


def fq(x):
    """an exact rational (Fraction or int) as an arb ball."""
    x = Fraction(x)
    return arb(x.numerator) / arb(x.denominator)


def up_frac(x):
    """the upper end of the arb ball x as an exact Fraction (python-flint 0.9: arb.upper().man_exp() is signed and exact)."""
    m, e = x.upper().man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def qchi(n, s):
    """Prob(chi^2_n > s) in arb (reader v6_2's forms): n = 2: e^(-s/2); n = 3: erfc(sqrt(s/2)) + sqrt(2 s/pi) e^(-s/2)."""
    if n == 2:
        return (-s / 2).exp()
    if n == 3:
        return (s / 2).sqrt().erfc() + (2 * s / arb.pi()).sqrt() * (-s / 2).exp()
    raise Refused('chi-square order %r' % (n,))


def band4(law, J, tpow=4):
    """Lemma U's banded bar at J >= 300 (reader v6_2's LAWCERT_CLAIM without its ak_rad term, the
    entry_ball form): rem (300/J)^4 + tail sqrt(P(J; tail)/P(300; tail)) + ann sqrt(P(J; ann)/P(300; ann)) + far e^(-far_rate (J -
    300)), P(J; x) = sum over x's pairs [a, G] of Prob(chi^2_n > J a/G). rem's exponent is the fixed 4 of U3, never the record's
    (tpow: PLANT-TPOW-UP's input only); each ratio is the numerator's upper end over the denominator's lower end. The upper end, as an
    exact Fraction."""
    Jb = fq(J)
    J0 = fq(300)
    pt, lw = law['parts'], law['laws']
    tot = fq(pt['rem']) * CM.ipow(J0 / Jb, tpow)
    for part in ('tail', 'ann'):
        g = lw[part]
        num = sum((qchi(g['n'], Jb * fq(a) / fq(G)) for a, G in g['a_G']), CM.ZERO).upper()
        den = sum((qchi(g['n'], J0 * fq(a) / fq(G)) for a, G in g['a_G']), CM.ZERO).lower()
        if not den > 0:
            raise Refused('%s: P(300) is not > 0' % part)
        tot = tot + fq(pt[part]) * (num / den).sqrt()
    tot = tot + fq(pt['far']) * (-(fq(lw['far_rate']) * (Jb - J0))).exp()
    return up_frac(tot)


EPC = {}   # (N, piece) -> the piece's banded entries


def ep_at(A, N, i):
    """stage C's entries on piece i (v1_12): A['EP'][N] (parity-forced keys exact 0) with each certified free entry's bar at the piece's
    J_lo, err_b = min(the record's sum of Bp, band4(J_lo)) (both valid on the piece: the record's claim for J >= 300 and Lemma U's laws,
    each term nonincreasing in J); the MOCK H and S4 keep their bars (times the D16 floors). Cached per piece."""
    if (N, i) in EPC:
        return EPC[(N, i)]
    J = Fraction(A['pieces'][N][i]['jlo'])
    E = {}
    for k, (LO, HI, err) in A['EP'][N].items():
        law = A['LAW'][N].get(k)
        if law is None or law['parity'] == 'zero' or err == 0:
            E[k] = (LO, HI, err)
        else:
            b = band4(law, J)
            E[k] = (LO, HI, b if b < err else err)
    EPC[(N, i)] = E
    return E


CPLUS_FORMAT = 'CPLUS_SIDECHECK_v1'


def cplus_text(text):
    """v1_13 (C-CPLUS): pk07's (c+) side check of Lemma 19.2: FORMAT = CPLUS_SIDECHECK_v1 on its first line, its
    VERDICT lines exactly ['VERDICT = VALID'], and its INPUT_EXPORT and INPUT_M2B lines naming this run's own pinned P2 export and M2(b)
    record by path and full sha256 (its claim is about exactly those inputs). Returns its one CLAIM line; raises Refused otherwise."""
    lines = [ln for ln in text.split('\n') if ln.strip()]
    if not lines or lines[0] != 'FORMAT = %s' % CPLUS_FORMAT:
        raise Refused('(c+) side check: the first line is not FORMAT = %s' % CPLUS_FORMAT)
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT = VALID']:
        raise Refused("(c+) side check: the VERDICT lines are not exactly ['VERDICT = VALID']")
    kv = {}
    for ln in lines:
        k, sep, v = ln.partition(' = ')
        if sep:
            kv.setdefault(k, []).append(v)
    want = {'INPUT_EXPORT': '%s:%s' % (os.path.relpath(CERT_P2[0], CODEDIR), PINS[CERT_P2[0]]),
            'INPUT_M2B': '%s:%s' % (os.path.relpath(CERT_M2B[0], CODEDIR), PINS[CERT_M2B[0]])}
    for k, v in want.items():
        if kv.get(k) != [v]:
            raise Refused('(c+) side check: %s is %s, not this run\'s %s' % (k, kv.get(k), v))
    if len(kv.get('CLAIM', [])) != 1:
        raise Refused('(c+) side check: not exactly one CLAIM line')
    return kv['CLAIM'][0]


def cplus_load(path):
    """v1_13: the (c+) side check from its file: present, its full sha256 the pin (C-HASH checked it at the start; checked again), then
    cplus_text."""
    if not os.path.isfile(path):
        raise Refused('(c+) side check: %s is missing' % os.path.basename(path))
    if sha_file(path) != PINS[CPLUS]:
        raise Refused('(c+) side check: %s does not match its pin' % os.path.basename(path))
    return cplus_text(read_text(path))


def p2_load(mode):
    """(P2) the export and its run output: CERTIFIED first through the bound reader's file entry point load, then
    p2_text's checks on the same files; tagged."""
    path, run_path = CERT_P2 if mode == 'CERTIFIED' else (P2MOCK, P2MOCKR)
    if mode == 'CERTIFIED':
        try:
            P2R.load(path, run_path)
        except ValueError as e:
            raise Refused('kt_s67_export_reader_v2_1.load: %s' % e)
    pieces, h = p2_text(read_text(path), read_text(run_path), os.path.basename(path), mode)
    tag(path, mode)
    tag(run_path, mode)
    return pieces, h


def vac_from_law(law, Bp_hi):
    """the vacuum places' inputs from one M2(b) law (decimal strings at or above the law's values): delta = eps_r / sqrt(1 - s^2), s,
    sp = s sqrt(2 / (1 + sqrt(1 - s^2))) (P2 l.813-814), eps_a, |B+|; None when s is 'inf' or not below 1 (no bound)."""
    if law['s'] == 'inf':
        return None
    s = CM.fr(Fraction(law['s']))
    if not s < 1:
        return None
    c_ = (1 - s * s).sqrt()
    return {'delta': (CM.fr(Fraction(law['eps_r'])) / c_).upper(), 's': s.upper(), 'sp': (s * (2 / (1 + c_)).sqrt()).upper(),
            'eps_a': CM.fr(Fraction(law['eps_a'])).upper(), 'Bp': CM.fr(Bp_hi).upper()}


def kv_write(path, record, header, rows, certified=False, tags=None):
    """the only writer of S8 records. A certified record (certified, RECORD S8_CERT_RECORD_v1 or EXPORT_STATUS CERTIFIED) is refused
    before any file is opened unless every input tag reads CERTIFIED, CERT_OK is set, the run is a cert-mode final, the
    path is in pk11/out and the header is the certified one; a MOCK record must carry the MOCK header and go to pk11/mocks/out."""
    if certified or record == 'S8_CERT_RECORD_v1' or header.get('EXPORT_STATUS') == 'CERTIFIED':
        if not cert_tags_ok(tags or []):
            raise ValueError('an input of the certified S8 record was not read through a certified path')
        if not CERT_OK[0]:
            raise ValueError('a certified S8 record before every gate and plant has passed')
        if MODE != 'cert' or ITEM != 'final' or not _under(path, OUTD):
            raise ValueError('a certified S8 record outside a cert-mode final or outside pk11/out')
        if record != 'S8_CERT_RECORD_v1' or header.get('FORMAT') != 'S4U_KV_v1' or header.get('RECORD') != record or \
                header.get('EXPORT_STATUS') != 'CERTIFIED' or header.get('CLAIM') != S8CLAIM or \
                any(w in header.get(k, '').upper() for k in STATUS_KEYS for w in BADWORDS):
            raise ValueError('not the certified S8 header')
        note = kv_note(record, True)
    else:
        if not _under(path, MOUT):
            raise ValueError('a MOCK record outside pk11/mocks/out')
        if record != 'S8_CERT_RECORD_v1_MOCK' or header.get('FORMAT') != 'S4U_KV_v1' or header.get('RECORD') != record or \
                header.get('EXPORT_STATUS') != 'MOCK' or not header.get('TAG', '').startswith('MOCK') or \
                not header.get('CLAIM', '').startswith('MOCK'):
            raise ValueError('not a MOCK header')
        for k in STATUS_KEYS:
            if 'CERTIFIED' in header.get(k, '').upper():
                raise ValueError('CERTIFIED in the status key %s' % k)
        note = kv_note(record, False)
    keys = list(header) + [k for k, v in rows]
    if len(set(keys)) != len(keys) or any(re.fullmatch(r'[A-Z][A-Z0-9_]*', k) is None for k in keys):
        raise ValueError('duplicate or malformed keys')
    with open(path, 'x') as fh:
        fh.write(kv_render(note, record, header, rows))
    return sha_file(path)


def kv_note(record, certified):
    if certified:
        return '# %s: written by %s (cert-mode final, every gate and plant passed, every input CERTIFIED).\n' % (record, LABEL)
    return '# %s (MOCK): written by %s from MOCK records only; never a certified record, never a C-REP reference.\n' % (record, LABEL)


def kv_render(note, record, header, rows):
    """the bytes kv_write writes (v1_8: also rendered in memory, so the record reader checks a record before any certified file exists)."""
    return note + ''.join('%s = %s\n' % (k, v) for k, v in header.items()) + ''.join('%s = %s\n' % (k, v) for k, v in rows) + \
        'END = %s\n' % record


def read_s8(text, mode):
    d = kv(text, 'S8 record')
    if mode == 'MOCK':
        if d.get('RECORD') != 'S8_CERT_RECORD_v1_MOCK' or d.get('END') != d.get('RECORD') or d.get('EXPORT_STATUS') != 'MOCK' or \
                not d.get('TAG', '').startswith('MOCK') or not d.get('CLAIM', '').startswith('MOCK'):
            raise Refused('S8 record: not a MOCK record')
    elif mode == 'CERTIFIED':
        if d.get('RECORD') != 'S8_CERT_RECORD_v1' or d.get('END') != d.get('RECORD') or d.get('EXPORT_STATUS') != 'CERTIFIED' or \
                d.get('CLAIM') != S8CLAIM or any('MOCK' in d.get(k, '').upper() for k in STATUS_KEYS):
            raise Refused('S8 record: not a certified record')
    else:
        raise ValueError(mode)
    return d


def run_A(fails, nofire, plants=True):
    """stage A: every input through its reader (CERTIFIED in cert mode, MOCK in mock mode), tagged with the path that read it
    ; stage A's plants and the M2(b) plants when plants is set (the pre item); the trial files' odd states and lam0; the main-term
    ratios; C-PAR and the parity-treated entries EP of stage C; the INPUTS digest of this run."""
    RM = 'CERTIFIED' if MODE == 'cert' else 'MOCK'
    pl = (lambda name, fn: plant(nofire, name, fn)) if plants else (lambda name, fn: None)
    STAGE[0] = 'M3'
    E, LAW, FAM, SCOPE, RECS, CERTS = {}, {}, {}, {}, {}, {}
    for N in (4, 3):
        recs, certs, sbad = rb_load(N)
        allE, laws, fam = rb_entries(N, recs, certs, RM)
        RECS[N], CERTS[N], SCOPE[N] = recs, certs, set(recs['N']['top'].get('scope_keys') or ())
        E[N] = fetch(allE, REQUIRED, SCOPE[N])
        LAW[N] = {k: laws[k] for k in REQUIRED}
        FAM[N] = {k: fam[k] for k in REQUIRED}
        zeros = sorted(k for k, (LO, HI, err) in E[N].items() if all(x == 0 for x in LO + HI) and err == 0)
        hs = ('from the certified D16 records %s and %s through m3_reader_v6_3.load with asm output %s (laws None: no law certificate, '
              'so their certified bars)' % (os.path.basename(D16[N]['H']), os.path.basename(D16[N]['S4']), os.path.basename(D16[N]['asm']))
              if d16_use(N, RM) else 'from the MOCK records, every bar times the D16 floor (H x%s, S4 x%s)' % (D16FLOOR['h'], D16FLOOR['S4']))
        out('C-M3 N=%d (route (b)): the certified records %s through m3_reader_v6_3.load and their law certificates %s through load_lawcert '
            '(producers %s); H and S4 %s; the %d required keys fetched (no TT; g and T to state 6), exact zeros %d -> %s' % (
                N, ' '.join(os.path.basename(CREC[N][f]) for f in RBFAM), ' '.join(os.path.basename(CLAW[N][k][0]) for k in ('P', 'N')),
                ' '.join(certs[k]['producer'] for k in ('P', 'N')), hs, len(E[N]), len(zeros), gate(fails, 'C-M3', True)))
        out('C-SIDEMAN N=%d: the four side manifests (asmP, asmN, lawcert v1_1, lawcert v1_2; pinned) list every record, asm output, '
            'certificate and job output read with its sha256; failing %s -> %s' % (N, sbad or 'none', gate(fails, 'C-SIDEMAN', not sbad)))
        if d16_use(N, RM):
            out('C-SIDEMAN N=%d (D16): pk03\'s freeze side manifest %s (pinned) lists the two D16 records and asm output read, every '
                'listed file with its sha256; failing %s -> %s' % (N, os.path.basename(D16[N]['side']), D16BAD[N] or 'none',
                                                                 gate(fails, 'C-SIDEMAN', not D16BAD[N])))
        readN = sorted(k for k in CM.route_b_keys(RB_SETS['B6']) if k.split(',')[0] in NFAM)
        reqN = sorted(k for k in REQUIRED if k.split(',')[0] in NFAM)
        scok = SCOPE[N] == set(recs['N']['entries']) and set(readN) <= SCOPE[N] and set(reqN) <= SCOPE[N]
        out('C-NSCOPE N=%d: the N record\'s scope_keys (%d) are exactly its entries; the N keys the core reads (%s route_b_keys '
            'of B6, %d: T,a,b for a, b <= 6 and TX,a,b for a, b <= 3) and the required N keys (%d) lie within them; every key stage C reads '
            'is fetched through that scope -> %s' % (N, len(SCOPE[N]), os.path.splitext(os.path.basename(CORE))[0], len(readN), len(reqN),
                                                     gate(fails, 'C-NSCOPE', scok)))
        lv = []
        for k in REQUIRED:
            lw = LAW[N][k]
            if lw is None or lw['parity'] == 'zero':
                continue
            top = recs[FAM[N][k]]['top']
            V = len(top['families'][top['graph_m3']]['a_v'])
            if len(lw['laws']['tail']['a_G']) != V or len(lw['laws']['ann']['a_G']) != V:
                lv.append(k)
        nfree = sum(1 for k in REQUIRED if LAW[N][k] is not None and LAW[N][k]['parity'] == 'free')
        out('C-LAWV N=%d: every certified free entry read (%d) carries tail and ann laws with one pair [a, G] per vertex of its graph '
            '(the reader checks the rest: rem_tpow 4, n = N - 1, J_REF 300, far_rate > 0, far_cF); failing %s -> %s' % (
                N, nfree, lv or 'none', gate(fails, 'C-LAWV', not lv)))
    tb = {os.path.basename(p): b for p, b in TRIAL.items() if b}
    ntrial = 2 * len(RBFAM) + 2 * sum(1 for n in (4, 3) if d16_use(n, RM))   # v1_14_2: the D16 records count too
    out('C-TRIAL: the %d certified M3 records name their trial set (%s, %s at N = 4; %s, %s at N = 3) by base name and full sha256; '
        'failing %s -> %s' % (len(TRIAL), os.path.basename(TSF[4]), os.path.basename(VRF[4]), os.path.basename(TSF[3]),
                              os.path.basename(VRF[3]), tb or 'none', gate(fails, 'C-TRIAL', not tb and len(TRIAL) == ntrial)))
    if d16_use(4, RM):   # v1_14_2: the D16 record's binding to its own asm output (the reader's RECORD-line check)

        def _d16_wrong_asm():
            try:
                M3R.load(D16[4]['H'], CASM[4]['P'], 300, 4)
            except Exception as e:
                raise Refused('m3_reader_v6_3.load: %s' % str(e)[:120])
        pl('PLANT-D16-ASM', _d16_wrong_asm)
        # v1_14_3: side_bad's own power, on the D16 N4 side manifest's text (the files on disk unchanged)
        stx = read_text(D16[4]['side'])
        hsha, hrel = sha_file(D16[4]['H']), os.path.relpath(D16[4]['H'], M3C)
        sfiles = [D16[4]['H'], D16[4]['S4'], D16[4]['asm']]

        def _side_sha():
            t_ = stx.replace(hsha + '  ' + hrel, ('0' if hsha[0] != '0' else '1') + hsha[1:] + '  ' + hrel, 1)
            b_ = side_bad(D16[4]['side'], sfiles, text=t_)
            if t_ != stx and ('%s: sha256 differs' % hrel) in b_:
                raise Refused('side_bad: %s' % '; '.join(b_)[:120])

        def _side_drop():
            t_ = '\n'.join(ln for ln in stx.split('\n') if ln.split()[1:] != [hrel])
            b_ = side_bad(D16[4]['side'], sfiles, text=t_)
            if t_ != stx and ('%s not listed' % os.path.basename(D16[4]['H'])) in b_:
                raise Refused('side_bad: %s' % '; '.join(b_)[:120])
        pl('PLANT-SIDEBAD-SHA', _side_sha)
        pl('PLANT-SIDEBAD-DROP', _side_drop)
    # the MOCK path's plants (H and S4 in mock mode): v1_11's, on the MOCK files
    atext4 = read_text(M3ASM[4])
    texts4 = {os.path.basename(p): read_text(p) for p in M3MOCK[4]}
    for name, text in sorted(texts4.items()):
        pl('PLANT-MOCK-M3 %s' % name, lambda t=text, n=name: m3_text(t, atext4, n, 4, 'CERTIFIED'))
    smoke = read_text(SMOKE)
    fake = 'RECORD %s %s\nVERDICT VALID\n' % (os.path.basename(SMOKE), hashlib.sha256(smoke.encode()).hexdigest())
    pl('PLANT-M3-SMOKE', lambda: m3_text(smoke, fake, os.path.basename(SMOKE), 4, 'CERTIFIED'))
    n0 = os.path.basename(M3MOCK[4][0])
    t0 = texts4[n0]
    pl('PLANT-M3-VERDICT-SUFFIX', lambda: m3_text(t0, atext4.replace('VERDICT VALID', 'VERDICT VALID (run validity: planted)'), n0, 4, 'MOCK'))
    pl('PLANT-M3-VERDICT-PRECERT', lambda: m3_text(t0, atext4.replace('VERDICT VALID', 'VERDICT VALID-PRECERT'), n0, 4, 'MOCK'))
    pl('PLANT-M3-VERDICT-TWO', lambda: m3_text(t0, atext4 + 'VERDICT VALID\n', n0, 4, 'MOCK'))
    tb_ = t0.replace('"J_REF": 300', '"J_REF": 300 ', 1)
    pl('PLANT-M3-BIND', lambda: m3_text(tb_, atext4, n0, 4, 'MOCK'))

    def rebound(text, name=n0):
        return text, 'RECORD %s %s\nVERDICT VALID\n' % (name, hashlib.sha256(text.encode()).hexdigest())
    pl('PLANT-M3-JREF', lambda: m3_text(*rebound(t0.replace('"J_REF": 300', '"J_REF": 150', 1)), n0, 4, 'MOCK'))
    t3 = read_text(M3MOCK[3][0])
    n3 = os.path.basename(M3MOCK[3][0])
    pl('PLANT-M3-N', lambda: m3_text(t3, read_text(M3ASM[3]), n3, 4, 'MOCK'))
    pl('PLANT-M3-FMT', lambda: m3_text(*rebound(t0.replace('"M3_RECORD_v1_MOCK"', '"M3_RECORD_v1_PRECERT"', 1)), n0, 4, 'MOCK'))
    raw = json.loads(t0)
    k1 = sorted(raw['items'])[0]
    raw['items'][k1]['ak'] = raw['items'][k1]['ak'][:3]
    pl('PLANT-M3-AKLEN', lambda: m3_text(*rebound(json.dumps(raw, sort_keys=True, indent=1) + '\n'), n0, 4, 'MOCK'))
    if plants:
        # v1_12: route (b)'s certified path, on its own records (N4): the reader's refusals, the law certificate's binding, the scope
        STAGE[0] = 'C-M3RB plants'
        pn, an = CREC[4]['N'], CASM[4]['N']
        tn, atn, nn = read_text(pn), read_text(an), os.path.basename(pn)

        def v62(text, out_text, N=4, J=300):
            def f():
                try:
                    M3R.loads(text, out_text, J, N, nn)
                except ValueError as e:
                    raise Refused('m3_reader_v6_3.loads: %s' % str(e)[:120])
            return f

        def out_text_for(asm_path, name, text):
            """the asm output with this record's RECORD line rebound to the planted text's sha256 (so the plant reaches the parse)."""
            lines = read_text(asm_path).split('\n')
            return '\n'.join(('RECORD %s %s' % (name, hashlib.sha256(text.encode()).hexdigest())) if ln.startswith('RECORD %s ' % name)
                             else ln for ln in lines)
        pl('PLANT-M3RB-N', v62(tn, atn, N=3))
        pl('PLANT-M3RB-JREF', v62(tn, atn, J=150))
        pl('PLANT-M3RB-BIND', v62(tn + ' ', atn))
        pl('PLANT-M3RB-PRECERT', v62(tn, atn.replace('VERDICT VALID', 'VERDICT VALID-PRECERT')))
        rn = json.loads(tn)
        kf = sorted(k for k, d in rn['items'].items() if d.get('parity') == 'free')[0]
        rlo = json.loads(tn)
        rlo['items'][kf]['laws']['rem_tpow'] = 3
        tlo = json.dumps(rlo)
        pl('PLANT-TPOW', v62(tlo, out_text_for(an, nn, tlo)))
        rhi = json.loads(tn)
        rhi['items'][kf]['laws']['rem_tpow'] = 5
        thi = json.dumps(rhi)
        try:
            lw_hi = M3R.loads(thi, out_text_for(an, nn, thi), 300, 4, nn)['laws'][kf]
            same = band4(lw_hi, Fraction(400)) == band4(M3R.entry_law(CERTS[4]['N'], 'N', kf), Fraction(400))
            fires(nofire, 'PLANT-TPOW-UP', same, 'N4 %s with rem_tpow 5 accepted by the reader; err_b at J = 400 unchanged (the fixed '
                  'exponent 4): %s' % (kf, same))
        except ValueError as e:
            fires(nofire, 'PLANT-TPOW-UP', True, 'N4 %s with rem_tpow 5: refused by m3_reader_v6_3 (%s), so err_b cannot change' % (kf, str(e)[:80]))
        cpath, jout = CLAW[4]['N'][0], CLAW[4]['N'][1]

        def lc(recs_, out_text=None):
            def f():
                try:
                    M3R.loads_lawcert(read_text(cpath), out_text if out_text is not None else read_text(jout), 300, 4, recs_,
                                      os.path.basename(cpath))
                except ValueError as e:
                    raise Refused('m3_reader_v6_3.loads_lawcert: %s' % str(e)[:120])
            return f
        pl('PLANT-LAWCERT-RECS', lc({'N': RECS[4]['N'], 'D': RECS[4]['D']}))
        pl('PLANT-LAWCERT-WRONGREC', lc({'N': RECS[4]['D']}))
        jt = read_text(jout)
        pl('PLANT-LAWCERT-PRODUCER', lc({'N': RECS[4]['N']}, jt.replace('m3_lawcert_v1_2 N 4', 'm3_lawcert_v1_1 N 4', 1)))
        pl('PLANT-LAWCERT-VERDICT', lc({'N': RECS[4]['N']}, jt.replace('VERDICT VALID', 'VERDICT VALID-PRECERT')))
        allE4 = rb_entries(4, RECS[4], CERTS[4], RM)[0]
        pl('PLANT-NSCOPE', lambda: fetch(allE4, ['TX,4,4'], SCOPE[4]))
        pl('PLANT-NOREC', lambda: fetch(allE4, ['T,4,4', 'TXX,4,4'], SCOPE[4]))
    STAGE[0] = 'P2'
    ptext, prun = read_text(P2MOCK), read_text(P2MOCKR)
    pname = os.path.basename(P2MOCK)
    PM = 'CERTIFIED' if (RM == 'CERTIFIED' or P2_CERT_IN_MOCK) else 'MOCK'   # v1_12_2: the certified export in mock mode too
    pieces, ph = p2_load(PM)
    first = {n: pieces[n][0] for n in (4, 3)}
    out('C-P2: the %s export %s through the %s path (the bound reader\'s load: its EXPORT-line binding; RECORD = END = EXPORT_KT_S67_v1; '
        'the full sha256 pin): 904 contiguous pieces per N from 300 to inf; fields %s; first piece N4 Bp_hi %s, N3 Bp_hi %s -> %s' % (
            PM, os.path.basename(CERT_P2[0] if PM == 'CERTIFIED' else P2MOCK), PM, ' '.join(P2FIELDS), first[4]['Bp_hi'], first[3]['Bp_hi'],
            gate(fails, 'C-P2', True)))
    if PM == 'CERTIFIED':
        tag(P2SIDE, 'CERTIFIED')
        sbp = side_bad(P2SIDE, list(CERT_P2))
        out('C-SIDEMAN-P2: the runs manifest (pinned) lists the export and its run output with their sha256 (and every other listed file '
            'matches); failing %s -> %s' % (sbp or 'none', gate(fails, 'C-SIDEMAN', not sbp)))
        own_ = {'TAG_M2_VACUUM': PINS[CERT_M2B[0]][:8], 'TAG_S4_U': PINS[S4UF][:8], 'TAG_S4_TRB': PINS[TRBF][:8]}
        tg = {k: (ph.get(k) or '').split() for k in own_}
        tbad = [k for k, v in own_.items() if not tg[k] or tg[k][0] != 'CERTIFIED' or tg[k][-1] != v]
        out('C-P2TAGS: the export\'s M2(b), S4-U and S4-TRB inputs are this run\'s own pinned records: %s -> %s' % (
            ', '.join('%s %s (this run: %s)' % (k, ' '.join(tg[k]), own_[k]) for k in own_), gate(fails, 'C-P2TAGS', not tbad)))
        STAGE[0] = 'C-CPLUS'   # v1_13: the S_V export is valid only together with pk07's (c+) side check
        try:
            cclaim, cok = cplus_load(CPLUS), True
            tag(CPLUS, 'CERTIFIED')
        except Refused as e:
            cclaim, cok = str(e), False
        out('C-CPLUS: pk07\'s (c+) side check %s (full sha256 pin; FORMAT %s; VERDICT lines exactly [\'VERDICT = VALID\']; INPUT_EXPORT '
            'and INPUT_M2B this run\'s own pins): %s -> %s' % (os.path.basename(CPLUS), CPLUS_FORMAT, cclaim[:160], gate(fails, 'C-CPLUS', cok)))
        ctext = read_text(CPLUS)
        pl('PLANT-CPLUS-VERDICT', lambda: cplus_text(ctext.replace('VERDICT = VALID', 'VERDICT = INVALID')))
        pl('PLANT-CPLUS-VERDICT-TWO', lambda: cplus_text(ctext.rstrip('\n') + '\nVERDICT = VALID\n'))
        pl('PLANT-CPLUS-FORMAT', lambda: cplus_text(ctext.replace('FORMAT = %s' % CPLUS_FORMAT, 'FORMAT = CPLUS_SIDECHECK_v0', 1)))
        pl('PLANT-CPLUS-BIND', lambda: cplus_text(ctext.replace(PINS[CERT_P2[0]], PINS[CERT_P2[1]], 1)))
        pl('PLANT-CPLUS-MISSING', lambda: cplus_load(CPLUS + '.missing'))
    pl('PLANT-MOCK-P2', lambda: p2_text(ptext, prun, pname, 'CERTIFIED'))
    pl('PLANT-P2-FLOAT', lambda: p2_text(read_text(P2X), read_text(P2XR), os.path.basename(P2X), 'CERTIFIED'))
    pl('PLANT-P2-SUFFIX', lambda: p2_text(ptext, prun.replace('VERDICT VALID', 'VERDICT VALID (run validity: planted)'), pname, 'MOCK'))
    pl('PLANT-P2-SHA', lambda: p2_text(ptext.replace('MOCK_SOURCE', 'MOCK_SOURCE_X', 1), prun, pname, 'MOCK'))

    def rerun(text):
        return text, 'EXPORT pk11/mocks/out/mkmock_v1_1/%s sha256 %s (planted)\nVERDICT VALID\n' % (pname, hashlib.sha256(text.encode()).hexdigest())
    pl('PLANT-P2-DUPKEY', lambda: p2_text(*rerun(ptext.replace('EXPORT_STATUS = MOCK', 'EXPORT_STATUS = MOCK\nEXPORT_STATUS = MOCK', 1)),
                                                     pname, 'MOCK'))
    pl('PLANT-P2-GRID', lambda: p2_text(*rerun('\n'.join(ln for ln in ptext.split('\n') if not ln.startswith('N4_P0450 '))), pname,
                                                   'MOCK'))
    # v1_3: VALID-STUB verdicts, a second VERDICT line, and the FLOAT export rebound to a planted VALID run output, so the
    # certified path's status check (EXPORT_STATUS FLOAT-PASS) is reached past the binding
    pl('PLANT-M3-VERDICT-STUB', lambda: m3_text(t0, atext4.replace('VERDICT VALID', 'VERDICT VALID-STUB'), n0, 4, 'MOCK'))
    pl('PLANT-P2-VERDICT-STUB', lambda: p2_text(ptext, prun.replace('VERDICT VALID', 'VERDICT VALID-STUB'), pname, 'MOCK'))
    pl('PLANT-P2-VERDICT-TWO', lambda: p2_text(ptext, prun + 'VERDICT VALID\n', pname, 'MOCK'))
    ftext = read_text(P2X)
    frun = 'EXPORT pk07/out/%s sha256 %s (planted VALID run)\nVERDICT VALID\n' % (os.path.basename(P2X), hashlib.sha256(ftext.encode()).hexdigest())
    pl('PLANT-P2-FLOAT-REBOUND', lambda: p2_text(ftext, frun, os.path.basename(P2X), 'CERTIFIED'))

    # v1_3: the certified paths through the readers' file entry points, on the mock files
    def m3_load_file():
        try:
            M3R.load(M3MOCK[4][0], M3ASM[4], 300, 4)
        except ValueError as e:
            raise Refused('m3_reader_v6_3.load: %s' % e)

    def p2_load_file():
        try:
            P2R.load(P2MOCK, P2MOCKR)
        except ValueError as e:
            raise Refused('kt_s67_export_reader_v2_1.load: %s' % e)
    pl('PLANT-MOCK-M3-FILE', m3_load_file)
    pl('PLANT-MOCK-P2-FILE', p2_load_file)
    # v1_3: every grid token of the export is the shortest repr of its float, and the pieces chain by float ==
    gtext = read_text(CERT_P2[0]) if PM == 'CERTIFIED' else ptext   # the export this run reads (v1_12_2: PM)
    toks = [m.groups() for m in re.finditer(r'^N[34]_P[0-9]{4} = (\S+) (\S+) ', gtext, re.M)]
    okt = len(toks) == 2 * 904 and all((a == repr(float(a))) and (b == 'inf' or b == repr(float(b))) for a, b in toks)
    out('C-GRIDTOK: %d piece lines; every jlo and jhi token equals repr(float(token)) (\'inf\' for the last jhi), so the floats are the '
        'producer\'s grid ends; they enter bounds only through exact conversions (arb(x)) -> %s' % (len(toks), gate(fails, 'C-GRIDTOK', okt)))

    STAGE[0] = 'M2B'
    MM = 'CERTIFIED' if (RM == 'CERTIFIED' or M2B_CERT_IN_MOCK) else 'MOCK'   # v1_12_1: the certified M2(b) in mock mode too
    mpath, masm = CERT_M2B if MM == 'CERTIFIED' else (M2BREC, M2BASM)
    m2b = m2b_load(mpath, masm, MM)
    tag(mpath, MM)
    tag(masm, MM)
    if MM == 'CERTIFIED':
        tag(M2BSIDE, 'CERTIFIED')
        sb2 = side_bad(M2BSIDE, [mpath, masm])
        out('C-SIDEMAN-M2B: the M2(b) run\'s side manifest (pinned) lists the record and its asm output with their sha256 (and every other '
            'listed file matches); failing %s -> %s' % (sb2 or 'none', gate(fails, 'C-SIDEMAN', not sb2)))
        ctext_, catext_ = read_text(mpath), read_text(masm)
        cname_ = os.path.basename(mpath)
        tb2 = m2b_trial_bad(ctext_)
        out('C-TRIAL-M2B: the certified M2(b) record\'s PIN_TRIAL names %s and %s by path and full sha256, once each, and no other vacres '
            'file; failing %s -> %s' % (os.path.basename(VRF[4]), os.path.basename(VRF[3]), tb2 or 'none', gate(fails, 'C-TRIAL-M2B', not tb2)))
        pl('PLANT-M2BCERT-BIND', lambda: m2b_text(ctext_ + '# planted\n', cname_, catext_, 'CERTIFIED'))
        pl('PLANT-M2BCERT-VERDICT', lambda: m2b_text(ctext_, cname_, catext_.replace('VERDICT VALID', 'VERDICT VALID-PRECERT'), 'CERTIFIED'))
        if plants:
            vt = '%s:%s' % (os.path.relpath(VRF[4], CODEDIR), PINS[VRF[4]])
            ft = m2b_trial_bad(ctext_.replace(vt, vt[:-8] + ('0' * 8 if not vt.endswith('0' * 8) else '1' * 8), 1))
            fires(nofire, 'PLANT-TRIAL-M2B', len(ft) > 0, 'the M2(b) record with the N4 vacres sha256 changed in its PIN_TRIAL: '
                  'C-TRIAL-M2B fails on %s' % (ft or 'nothing'))
    law300 = {n: law_at({'m2b': m2b}, n, 300.0) for n in (4, 3)}
    law6 = {n: law_at({'m2b': m2b}, n, 1.0e6) for n in (4, 3)}
    okl = all(law300[n]['s'] != 'inf' for n in (4, 3))
    out('C-M2B: the %s M2(b) record %s through the %s path (pk02\'s interface): law_v1 at J = 300 %s; at J = 1e6 %s -> %s' % (
        MM, os.path.basename(mpath), MM, '; '.join('N%d %s' % (n, ' '.join('%s %.4g' % (k, float(Fraction(v)) if v != 'inf' else float('inf'))
                                                                           for k, v in sorted(law300[n].items()))) for n in (4, 3)),
        '; '.join('N%d eps_r %.4g s %.4g' % (n, float(Fraction(law6[n]['eps_r'])), float(Fraction(law6[n]['s'])) if law6[n]['s'] != 'inf'
                                              else float('inf')) for n in (4, 3)), gate(fails, 'C-M2B', okl)))
    mtext, matext = read_text(M2BREC), read_text(M2BASM)
    mname = os.path.basename(M2BREC)

    def mre(text):
        """a MOCK M2(b) text with an asm output rebound to it (its sha256), so a plant reaches the record's own checks."""
        return text, mname, 'm2b_asm_v1_MOCK sha256 %s (planted)\nRECORD %s %s\nVERDICT VALID\n' % (
            PINS[M2BMOD], mname, hashlib.sha256(text.encode('utf-8')).hexdigest())
    pl('PLANT-MOCK-M2B', lambda: m2b_text(mtext, mname, matext, 'CERTIFIED'))
    pl('PLANT-M2B-VERDICT-SUFFIX', lambda: m2b_text(mtext, mname, matext.replace('VERDICT VALID', 'VERDICT VALID (planted)'), 'MOCK'))
    pl('PLANT-M2B-VERDICT-STUB', lambda: m2b_text(mtext, mname, matext.replace('VERDICT VALID', 'VERDICT VALID-STUB'), 'MOCK'))
    pl('PLANT-M2B-BIND', lambda: m2b_text(mtext + '# planted\n', mname, matext, 'MOCK'))
    pl('PLANT-M2B-FMT', lambda: m2b_text(*mre(mtext.replace('FORMAT = M2B_KV_v1_MOCK', 'FORMAT = M2B_KV_v1_PRECERT', 1)), 'MOCK'))
    pl('PLANT-M2B-DUPKEY', lambda: m2b_text(*mre(mtext + 'N4_S_300 = 1.3e-10\n'), 'MOCK'))
    # v1_12: stage B (C-REPF, the W3 TT route against 3g's floats) is gone with the TT route, and with it C-REPF's reference data

    STAGE[0] = 'S4'
    s4u = s4_text(read_text(S4UF), 'S4_U_CERTIFIED_v3')   # v1_12: v3 (e870cbe5) replaces v2 (b1b6b99b); the same F2 form and keys
    trb = s4_text(read_text(TRBF), 'S4_TRB_CERTIFIED_v1')
    tag(S4UF, 'CERTIFIED')   # pk08's final certified records, read by the same path in both modes
    tag(TRBF, 'CERTIFIED')
    out('C-S4U: S4_U_CERTIFIED_v3 through the KV layer: %s -> %s' % (
        '; '.join('N%d %s' % (n, ' '.join('%s %.12g' % (k, float(s4u[(n, k)])) for k in S4KEYS['S4_U_CERTIFIED_v3'])) for n in (4, 3)),
        gate(fails, 'C-S4U', True)))
    out('C-TRB: S4_TRB_CERTIFIED_v1 through the KV layer: N4 TRB %.12g, N3 TRB %.12g -> %s' % (
        float(trb[(4, 'TRB')]), float(trb[(3, 'TRB')]), gate(fails, 'C-TRB', True)))
    su, st = read_text(S4UF), read_text(TRBF)
    pl('PLANT-S4U-PRECERT', lambda: s4_text(su.replace('RECORD = S4_U_CERTIFIED_v3', 'RECORD = S4_U_CERTIFIED_v3_PRECERT', 1),
                                                       'S4_U_CERTIFIED_v3'))
    pl('PLANT-S4U-KEY', lambda: s4_text('\n'.join(ln for ln in su.split('\n') if not ln.startswith('N4_R_CERT ')), 'S4_U_CERTIFIED_v3'))
    pl('PLANT-S4U-CLAIM', lambda: s4_text(su.replace('<= N*_LEAD_HI', '< N*_LEAD_HI', 1), 'S4_U_CERTIFIED_v3'))
    pl('PLANT-S4U-V2', lambda: s4_text(su.replace('RECORD = S4_U_CERTIFIED_v3', 'RECORD = S4_U_CERTIFIED_v2', 1), 'S4_U_CERTIFIED_v3'))
    pl('PLANT-S4U-END', lambda: s4_text(su.replace('END = S4_U_CERTIFIED_v3', 'END = S4_U_CERTIFIED_v2', 1), 'S4_U_CERTIFIED_v3'))
    pl('PLANT-TRB-END', lambda: s4_text(st.replace('END = S4_TRB_CERTIFIED_v1', 'END = S4_TRB_CERTIFIED_v0', 1), 'S4_TRB_CERTIFIED_v1'))
    pl('PLANT-TRB-PRECERT', lambda: s4_text(st.replace('RECORD = S4_TRB_CERTIFIED_v1', 'RECORD = S4_TRB_CERTIFIED_v1_STUB', 1),
                                                       'S4_TRB_CERTIFIED_v1'))
    pl('PLANT-TRB-KEY', lambda: s4_text('\n'.join(ln for ln in st.split('\n') if not ln.startswith('N3_TRB ')), 'S4_TRB_CERTIFIED_v1'))

    STAGE[0] = 'parity'
    odd, lam0, mains, EP = {}, {}, {}, {}
    for N in (4, 3):
        # v1_9 (the parity condition 1): the stored decimals of the trial set and the vacres polynomial, exactly symmetric
        sb = symin_bad(json.loads(read_text(TSF[N]), parse_float=Fraction), json.loads(read_text(VRF[N]), parse_float=Fraction))
        out('C-SYMIN N=%d: the stored decimals of %s and %s as exact rationals: every trial state exactly T <-> B even or odd, the odd '
            'states 2, 5, 8, the vacres q1, q2, q3 exactly symmetric; failing %s -> %s' % (
                N, os.path.basename(TSF[N]), os.path.basename(VRF[N]), sb or 'none', gate(fails, 'C-SYMIN', not sb)))
        SJ = json.loads(read_text(TSF[N]))
        S = SJ['S']
        odd[N] = [a for a in range(1, 10) if all(S[r][a] == 0.0 for r in (0, 3, 6, 7)) and any(S[r][a] != 0.0 for r in range(10))]
        lam0[N] = [float(x) for x in SJ['lam0'][:4]]
        mains[N] = mains_exact(N)
        pz = parity_zeros(E[N], odd[N])
        bad = par_bad(E[N], pz)
        exact = [k for k in pz if all(x == 0 for x in E[N][k][0] + E[N][k][1]) and E[N][k][2] == 0]
        out('C-PAR N=%d: the parity-forced entries (odd trial states %s; graphs g, T, e, f, h; v1_12: g and T to state 6, no TT): %s; each '
            'record ball holds 0 for every t in [0, 1/300], so stage C uses exact zeros; exact zeros in the records %d, balls around 0 %d '
            '(%s); failing %s -> %s' % (
                N, [a for a in odd[N] if a <= 6], ' '.join(pz), len(exact), len(pz) - len(exact), ' '.join(k for k in pz if k not in exact),
                bad or 'none', gate(fails, 'C-PAR', not bad and pz == PARZ_EXPECTED)))
        EP[N] = dict(E[N])
        for k in pz:
            EP[N][k] = ([Fraction(0)] * 4, [Fraction(0)] * 4, Fraction(0))
    if plants:
        Ep = dict(E[4])
        one = [Fraction(1, 10 ** 12), Fraction(0), Fraction(0), Fraction(0)]
        Ep['T,0,2'] = (one, list(one), Fraction(0))
        fb = par_bad(Ep, parity_zeros(Ep, odd[4]))
        fires(nofire, 'PLANT-PARITY', fb == ['T,0,2'], 'T,0,2 with a_0 = 1e-12 exactly and no bar: C-PAR fails on %s' % (fb or 'nothing'))
        # v1_9 (the condition 4, away from t = 0): a ball that holds 0 at t = 0 but excludes it at t = 1/300 must fail C-PAR
        Eq = dict(E[4])
        m1 = [Fraction(0), Fraction(-1), Fraction(0), Fraction(0)]
        Eq['g,0,2'] = (m1, list(m1), Fraction(1, 10 ** 6))
        fq_ = par_bad(Eq, parity_zeros(Eq, odd[4]))
        fires(nofire, 'PLANT-PARITY-T', fq_ == ['g,0,2'], 'g,0,2 = -t +- 1e-6 (0 at t = 0, excluded at t = 1/300): C-PAR fails on %s' % (
            fq_ or 'nothing'))
        # v1_12: the same on a B-chain key (state 5 odd, state 4 even)
        Er = dict(E[4])
        Er['T,4,5'] = (one, list(one), Fraction(0))
        fr_ = par_bad(Er, parity_zeros(Er, odd[4]))
        fires(nofire, 'PLANT-PARITY-B', fr_ == ['T,4,5'], 'T,4,5 with a_0 = 1e-12 exactly and no bar: C-PAR fails on %s' % (fr_ or 'nothing'))
        SJ4 = json.loads(read_text(TSF[4]), parse_float=Fraction)
        VJ4 = json.loads(read_text(VRF[4]), parse_float=Fraction)
        SJs = dict(SJ4)
        SJs['S'] = [list(row) for row in SJ4['S']]
        SJs['S'][1][1] = SJs['S'][1][1] + Fraction(1, 10 ** 15)
        fs = symin_bad(SJs, VJ4)
        fires(nofire, 'PLANT-SYMIN', any('state 1 ' in x for x in fs), 'state 1, row 1 moved by 1e-15: C-SYMIN fails on %s' % (fs or 'nothing'))
        VJs = dict(VJ4)
        VJs['q1'] = list(VJ4['q1'])
        VJs['q1'][0] = VJs['q1'][0] + Fraction(1, 10 ** 15)
        fv = symin_bad(SJ4, VJs)
        fires(nofire, 'PLANT-SYMIN-Q', any('q1' in x for x in fv), 'vacres q1[0] moved by 1e-15: C-SYMIN fails on %s' % (fv or 'nothing'))
    lines_ = (['%s %s %s' % (os.path.relpath(p, CODEDIR), sh, st) for p, (sh, st) in sorted(TAGS.items())] +
              ['%s %s REFERENCE' % (os.path.relpath(p, CODEDIR), PINS[p]) for p in sorted(REFS)] +
              ['%s %s CORE' % (os.path.relpath(CORE, CODEDIR), PINS[CORE])])
    A_DIGEST[0] = hashlib.sha256('\n'.join(lines_).encode('utf-8')).hexdigest()
    out('INPUTS %s' % A_DIGEST[0])
    out('C-TAGS: %d inputs of the claim, each read through the %s path (%s); %d reference files and the core -> %s' % (
        len(TAGS), RM, ', '.join(sorted(set(st for sh, st in TAGS.values()))), len(REFS),
        gate(fails, 'C-TAGS', all(st == ('CERTIFIED' if RM == 'CERTIFIED' else st) for sh, st in TAGS.values()))))
    # v1_12: S8's range is J >= JX4 at N4 (the band below is route H's) and J >= 300 at N3; at N4 stage C starts at the
    # piece that contains J = JX4, so the pieces from there cover [JX4, inf) (the overlap below JX4 is margin)
    RSTART = {4: max(i for i, p in enumerate(pieces[4]) if Fraction(p['jlo']) <= JX4), 3: 0}
    out('C-RANGE: S8 covers J >= %d at N4 from piece %d (J [%r, %r]) and J >= 300 at N3 from piece 0 -> %s' % (
        JX4, RSTART[4], pieces[4][RSTART[4]]['jlo'], pieces[4][RSTART[4]]['jhi'], gate(fails, 'C-RANGE',
                                                                                        Fraction(pieces[4][RSTART[4]]['jhi']) > JX4)))
    return {'E': E, 'EP': EP, 'pieces': pieces, 'law': law300, 's4u': s4u, 'trb': trb, 'm2b': m2b, 'odd': odd, 'lam0': lam0,
            'mains': mains, 'LAW': LAW, 'FAM': FAM, 'SCOPE': SCOPE, 'RSTART': RSTART}


# ---------------------------------------------------------------- stage C's helpers (v1_12: stage B, C-REPF on the W3 TT route, is gone)
DNEAR, DFAR = {'flip': (-1, 0, 1, 2), 'same': (-1, 0)}, {'flip': 3, 'same': 1}


def chain_key(k):
    """an M3 record key -> the chain's key (None for the S4 strip entries the chain does not use)."""
    p = k.split(',')
    if p[0] in ('g', 'T', 'TX', 'TT') and len(p) == 3:
        return (p[0], int(p[1]), int(p[2]))
    if p[0] in ('e', 'eX', 'f', 'fX', 'DY', 'h', 'hX') and len(p) == 2:
        return (p[0], int(p[1]))
    if p[0] in ('z', 'wXw', 'wXwX', 'DYY') and len(p) == 1:
        return (p[0],)
    return {'S4,Z': ('Z4',), 'S4,x,1,TM': ('X1',), 'S4,xy,1,TM,2,TM': ('X1X2',)}.get(k)


def mains_exact(N):
    """the five main-term ratios of the chain (rhoE, rmain, rho4, rhob, rhoH) exactly: main(G) ~ tau(G)^(-n/2) (riglap2's logmain;
    n = N - 1; the area and J factors cancel since each ratio balances sum c (V - 1) = 0), tau(G) = det of the weighted Laplacian with
    row and column 0 removed (matrix-tree), the vac end couplings A = (3 + sqrt 21)/6, B = (3 sqrt 5 - sqrt 21)/12 as balls."""
    A = (arb(3) + arb(21).sqrt()) / 6
    B = (3 * arb(5).sqrt() - arb(21).sqrt()) / 12

    def tau(ncols, left, right):
        E = {}
        for j in range(ncols):
            t_, m_, b_ = 3 * j, 3 * j + 1, 3 * j + 2
            if j == 0 or j == ncols - 1:
                E[(t_, m_)], E[(m_, b_)], E[(t_, b_)] = A, A, B
            else:
                E[(t_, m_)], E[(m_, b_)] = arb(1), arb(1)
            if j < ncols - 1:
                for r in range(3):
                    E[(3 * j + r, 3 * (j + 1) + r)] = arb(1)
        for side, c_ in ((left, 0), (right, ncols - 1)):
            if side == 'free':
                E[(3 * c_, 3 * c_ + 1)], E[(3 * c_ + 1, 3 * c_ + 2)] = arb(1), arb(1)
                E.pop((3 * c_, 3 * c_ + 2), None)
        V = 3 * ncols
        L = [[arb(0)] * V for _ in range(V)]
        for (u, v), c in E.items():
            L[u][u] += c
            L[v][v] += c
            L[u][v] -= c
            L[v][u] -= c
        M = [list(r[1:]) for r in L[1:]]
        det = arb(1)
        for i in range(V - 1):
            p = M[i][i]
            if not p > 0:
                raise ValueError('a pivot of the reduced Laplacian is not positive')
            det = det * p
            for r in range(i + 1, V - 1):
                f = M[r][i] / p
                for c_ in range(i, V - 1):
                    M[r][c_] = M[r][c_] - f * M[i][c_]
        return det, V
    G = {'D': (2, 'vac', 'vac'), 'N': (3, 'vac', 'vac'), 'E2': (2, 'vac', 'free'), 'E3': (3, 'vac', 'free'), 'FF': (2, 'free', 'free'),
         'S4': (4, 'free', 'free'), 'H': (4, 'vac', 'free'), 'L': (4, 'vac', 'vac')}
    tv = {k: tau(*v) for k, v in G.items()}

    def ratio(coef):
        if sum(c * (tv[k][1] - 1) for k, c in coef.items()) != 0:
            raise ValueError('a main-term ratio that does not balance V - 1')
        return (-(arb(N - 1) / 2) * sum((c * tv[k][0].log() for k, c in coef.items()), arb(0))).exp()
    return (ratio({'E3': 1, 'D': 1, 'N': -1, 'E2': -1}), ratio({'E2': 2, 'D': -1, 'FF': -1}), ratio({'S4': 1, 'D': 3, 'N': -2, 'E2': -2}),
            ratio({'L': 1, 'D': 1, 'N': -2}), ratio({'H': 1, 'D': 2, 'N': -2, 'E2': -1}))


def ritz_float(gm, Tm, nst=3):
    """3g's ritz on the midpoints: the rows of C are G''-orthonormal Ritz vectors of T'' (binary64); the basis C0 of the piece."""
    import numpy as np
    g00 = gm[0][0]

    def p2(M, a, b):
        return M[a][b] - gm[a][0] / g00 * M[0][b] - gm[b][0] / g00 * M[a][0] + gm[a][0] * gm[b][0] / g00 ** 2 * M[0][0]
    idx = list(range(1, nst + 1))
    G2 = np.array([[p2(gm, a, b) for b in idx] for a in idx])
    T2 = np.array([[p2(Tm, a, b) for b in idx] for a in idx])
    Li = np.linalg.inv(np.linalg.cholesky(G2))
    th, Yv = np.linalg.eigh(Li @ T2 @ Li.T)
    order = np.argsort(-th)
    C = (Li.T @ Yv[:, order]).T
    return [[float(x) for x in row] for row in C]


# ---------------------------------------------------------------- stage C: the pieces in J (s8core_v1_4)
TWO_CLS = [(dL, dR, kind, m) for kind in ('flip', 'same') for dL in DNEAR[kind] for dR in DNEAR[kind] for m in range(1, CM.MM + 1)
           if dL + dR + m + 3 >= 4]
FAMS4 = ('S8-1', 'S8-2', 'S8-3', 'lemma')
NPIECES = 904
SAMPLE_EVERY = 100   # C-UNIF and C-MV on the first and last piece of each chunk and on every piece i with i % 100 == 0
SYMFAM = {'g': 2, 'T': 2, 'e': 1, 'f': 1, 'h': 1}   # the reflection-symmetric graphs read (no X or Y insertion; v1_12: no TT)
RISK_PRINT = 200     # RISK lines printed per output (all are counted)


def parity_zeros(E, odd):
    """the parity-forced zero entries: a reflection-symmetric family (SYMFAM) with exactly one odd trial state among its indices. The
    z9sym states are exactly even or odd under T <-> B (zero_states_v2's C-SYM) and those graphs are T <-> B symmetric, so these
    entries vanish exactly for every J."""
    res = []
    for k in E:
        p = k.split(',')
        if p[0] in SYMFAM and len(p) == 1 + SYMFAM[p[0]] and all(x.isdigit() for x in p[1:]) and \
                sum(1 for x in p[1:] if int(x) in odd) == 1:
            res.append(k)
    return sorted(res)


PAIRS_S, FIXED_S, PAIRS_Q = ((1, 2), (4, 5), (8, 9)), (0, 3, 6, 7), ((0, 1), (3, 4), (7, 8))   # zero_states_v2's T <-> B maps


def symin_bad(SJ, VJ):
    """C-SYMIN (v1_9, the parity condition 1), on the stored decimals read as exact rationals (json parse_float=Fraction): S's rows
    are a state's constant and its BASIS9 coefficients, and T <-> B swaps the row pairs (1,2), (4,5), (8,9) and fixes rows 0, 3, 6, 7
    (zero_states_v2's layout); each state must be exactly even (every pair equal) or exactly odd (every pair opposite, the fixed rows
    0), the odd states exactly 2, 5, 8; each vacres q1, q2, q3 equal on its index pairs (0,1), (3,4), (7,8). Returns the failures."""
    S = SJ['S']
    bad, odd = [], []
    for a in range(10):
        col = [Fraction(S[r][a]) for r in range(10)]
        ev = all(col[i] == col[j] for i, j in PAIRS_S)
        od = all(col[i] == -col[j] for i, j in PAIRS_S) and all(col[r] == 0 for r in FIXED_S)
        if od and not ev:
            odd.append(a)
        elif not ev:
            bad.append('state %d is neither exactly even nor exactly odd' % a)
    if odd != [2, 5, 8]:
        bad.append('odd states %s, not [2, 5, 8]' % odd)
    for k in ('q1', 'q2', 'q3'):
        if any(Fraction(VJ[k][i]) != Fraction(VJ[k][j]) for i, j in PAIRS_Q):
            bad.append('vacres %s is not exactly symmetric' % k)
    return bad


def par_bad(E, keys):
    """C-PAR: the keys whose record ball does not hold 0 for every t in [0, 1/300] (sum_k dist(0, [LO_k, HI_k]) 300^-k > err_b). The
    ball at t is [sum_k LO_k t^k - err_b, sum_k HI_k t^k + err_b] (t >= 0). If it excludes 0 at some t in [0, 1/300], then sum_k
    max(LO_k, 0) 300^-k or sum_k max(-HI_k, 0) 300^-k exceeds err_b, so the key is listed (v1_9, the condition 2: the gate fails
    whenever a parity-forced ball excludes 0 anywhere on the range); a key that is not listed holds 0 at every t."""
    bad = []
    for k in keys:
        LO, HI, err = E[k]
        d = sum((max(LO[j], -HI[j], Fraction(0)) / Fraction(300) ** j for j in range(4)), Fraction(0))
        if d > err:
            bad.append(k)
    return bad


def ritz_pure(Vm, odd):
    """the piece's basis C0: 3g's Ritz vectors of the bar-free center values (binary64), each row then made parity-pure (its
    minority-parity components set to exactly 0; any basis is a valid trial basis), so every basis vector's parity is exact and the
    chain's sector split, mirror and B_MB rest on exact parity. v1_9 (the condition 3): the zeroed C0 is a new trial basis, and the
    chain recomputes everything from it in balls (C0 G'' C0^T and its Cholesky orthonormalization, R, B, beta, every component, every
    Gram form, the parity pi by majority on the zeroed rows); the float eigen-solve only proposes the rows, and none of its Ritz values or
    relations is used anywhere."""
    sym = lambda nm, a, b: float(Vm[(nm, min(a, b), max(a, b))].mid())
    C0 = ritz_float([[sym('g', a, b) for b in range(4)] for a in range(4)], [[sym('T', a, b) for b in range(4)] for a in range(4)])
    res = []
    for row in C0:
        wo = sum(x * x for x, n in zip(row, (1, 2, 3)) if n in odd)
        we = sum(x * x for x, n in zip(row, (1, 2, 3)) if n not in odd)
        res.append([x if ((n in odd) == (wo > we)) else 0.0 for x, n in zip(row, (1, 2, 3))])
    return res


def c0_zero_rel(Vm, odd):
    """v1_10, INFO: the largest component ritz_pure sets to 0, relative to the Euclidean norm of its row (ritz_float's rows)."""
    sym = lambda nm, a, b: float(Vm[(nm, min(a, b), max(a, b))].mid())
    worst = 0.0
    for row in ritz_float([[sym('g', a, b) for b in range(4)] for a in range(4)], [[sym('T', a, b) for b in range(4)] for a in range(4)]):
        wo = sum(x * x for x, n in zip(row, (1, 2, 3)) if n in odd)
        we = sum(x * x for x, n in zip(row, (1, 2, 3)) if n not in odd)
        nrm = math.sqrt(wo + we)
        for x, n in zip(row, (1, 2, 3)):
            if (n in odd) != (wo > we):
                worst = max(worst, abs(x) / nrm)
    return worst


def parity_lines(fails, N, i, r):
    """v1_10: C-PAREXACT (the chain of piece i finds its basis and the parity-forced entries exactly F-pure, so the odd components carry
    no allowance there) and C0-ZERO (INFO). V1_12: also route (b)'s B chain (its basis rows each in one sector,
    its g and T parity-forced entries exactly 0), which the sector split of Gl = R_B3^T R_B3 + tau_B I assumes."""
    pb = r['chB']['par_exact'] if 'chB' in r else None
    out('C-PAREXACT N=%d piece %d: the W3 chain\'s par_exact %s, the B chain\'s (%s) %s -> %s; C0-ZERO (INFO): the largest zeroed C0 '
        'component relative to its row %.1e' % (N, i, r['ch']['par_exact'], r.get('basis'), pb,
                                                gate(fails, 'C-PAREXACT', r['ch']['par_exact'] is True and pb is True),
                                                c0_zero_rel(CM.entry_points(r['Ech'], arb(r['T'].mid())), r['odd'])))


def law_at(A, N, J):
    """the M2(b) law at J (a grid end as a float, converted exactly) through the reader's law_v1: decimal strings at or above it."""
    mod, rec = A['m2b']
    return mod.law_v1(rec, N, Fraction(J))


def u_poly(s4u, N, t):
    """S4-U's F2 form (P2's): LEAD_HI (1 + C1_HI t + C2_HI t^2 + C3_HI t^3) + R_CERT, at the ball t."""
    f = lambda k: CM.fr(s4u[(N, k)])
    return f('LEAD_HI') * (1 + f('C1_HI') * t + f('C2_HI') * t * t + f('C3_HI') * t * t * t) + f('R_CERT')


def w3_keys(E):
    """the W3 chain's entries by chain key: every key chain_key maps whose trial states are all <= 3 (chain(..., tt=False) reads no TT)."""
    res = {}
    for k, v in E.items():
        ck = chain_key(k)
        if ck is not None and ck[0] != 'TT' and all(x <= 3 for x in ck[1:] if isinstance(x, int)):
            res[ck] = v
    return res


def b_entries(E, SL):
    """the B chain's entries for the trial set SL: g and T over SL x SL (record keys g,a,b and T,a,b, a <= b), renamed to the chain states
    0..len(SL)-1 in order (an order-preserving map, so a <= b is kept and the odd states map with them)."""
    ren = {s: j for j, s in enumerate(SL)}
    return {(nm, ren[a], ren[b]): E['%s,%d,%d' % (nm, a, b)] for nm in ('g', 'T') for a in SL for b in SL if a <= b}


def basis_RB(Vm, C0, oddc, K):
    """the B chain's binary64 basis over its states 1..K (kt_s8_diag_B_v1's construction): C0's W3 rows padded with zeros, then per parity
    sector the Ritz rows of the G''-orthogonal complement of those rows at the center, by decreasing Ritz value. Each row lies in one
    sector (exactly parity-pure); any rows are a valid trial basis, since chain_RB recomputes everything from them in balls."""
    import numpy as np
    g00 = Vm[('g', 0, 0)]
    sym = lambda nm, a, b: Vm[(nm, min(a, b), max(a, b))]
    p2 = lambda nm, a, b: float((sym(nm, a, b) - sym('g', a, 0) / g00 * sym(nm, 0, b) - sym('g', b, 0) / g00 * sym(nm, a, 0) +
                                 sym('g', a, 0) * sym('g', b, 0) / (g00 * g00) * sym(nm, 0, 0)).mid())
    idx = list(range(1, K + 1))
    G = np.array([[p2('g', a, b) for b in idx] for a in idx])
    Tm = np.array([[p2('T', a, b) for b in idx] for a in idx])
    rows = [list(r_) + [0.0] * (K - 3) for r_ in C0]
    extra = []
    for want_odd in (False, True):
        pos = [j for j in range(K) if ((j + 1) in oddc) == want_odd]
        if not pos:
            continue
        Gs, Ts = G[np.ix_(pos, pos)], Tm[np.ix_(pos, pos)]
        Y = [[r_[j] for j in pos] for r_ in rows[:3] if any(r_[j] != 0.0 for j in pos)]
        Z = np.linalg.svd(np.array(Y) @ Gs)[2][len(Y):] if Y else np.eye(len(pos))
        if Z.shape[0] == 0:
            continue
        Li = np.linalg.inv(np.linalg.cholesky(Z @ Gs @ Z.T))
        th, Yv = np.linalg.eigh(Li @ (Z @ Ts @ Z.T) @ Li.T)
        Cz = (Li.T @ Yv).T @ Z
        for j in range(len(th)):
            full = [0.0] * K
            for jj, q in enumerate(pos):
                full[q] = float(Cz[j][jj])
            extra.append((float(th[j]), full))
    extra.sort(key=lambda x: -x[0])
    return rows + [r_ for th, r_ in extra]


def piece_eval_RB(N, A, i, T=None, C0=None, vac=None, Uh=None, bars=1, vacf=1, uf=1, rows=True, bases=None, C0B=None, tau=None):
    """piece i of stage C on route (b) (v1_12; s8core_v1_9): the W3 chain (chain_dual_t with tt=False: no TT) on the piece box with
    the piece's banded entries (ep_at), S8-3's strips; then for each trial set of bases (default RB_ORDER: B5, B6, B4) the reduced B
    chain on its g and T (chain_dual_t_RB), routeb_leak (tau_B, Gl = R_B3^T R_B3 + tau_B I, the block bound), setup(..., Gl, sblk) and
    rows_cert, until a set whose rows and top-mode classes all pass with both chains exactly parity-pure: each set is valid (U9 holds for
    any trial set), so the first passing set is taken; otherwise the last set evaluated. The result has piece_eval_C's fields ('ch' is the
    W3 chain with route (b)'s Gl) and 'i', 'chW', 'basis', 'SL', 'chB', 'C0B', 'leak', 'tried' [(set, ok, tau_B upper)]. Defaults: the
    piece's own t-box, the parity-pure basis of its center, the M2(b) law at J_lo, S4-U's upper end over the box, the piece's P2 row;
    C-PIECE passes the parent's T-half, C0, vac, Uh, set and C0B. bars, vacf, uf, tau: the margin plants only, never a bound. rows=False:
    the chains and setup of the first set only. None when the law's s is not below 1, or when no set has tau_B > 0 (no bound)."""
    P2row = A['pieces'][N][i]
    if T is None:
        T = CM.tball(P2row['jlo'], P2row['jhi'])
    if vac is None:
        vac = vac_from_law(law_at(A, N, P2row['jlo']), P2row['Bp_hi'])
        if vac is None:
            return None
    if vacf != 1:
        vac = {k: (v if k == 'Bp' else (v * arb(vacf)).upper()) for k, v in vac.items()}
    if Uh is None:
        Uh = u_poly(A['s4u'], N, T).upper()
    if uf != 1:
        Uh = (Uh * arb(uf)).upper()
    E = ep_at(A, N, i)
    if bars != 1:
        E = {k: (LO, HI, err * Fraction(bars)) for k, (LO, HI, err) in E.items()}
    Ech = w3_keys(E)
    if C0 is None:
        C0 = ritz_pure(CM.entry_points(Ech, arb(T.mid())), A['odd'][N])
    chW = CM.chain_dual_t(Ech, T, A['mains'][N], A['odd'][N], vac, C0, tt=False)
    P2r = {k: CM.fr(P2row[k]) for k in ('Bp_hi', 'Bm_hi', 'Rw_hi', 'rho1_hi')}
    s83 = []
    for lab, kind, (cx, bx), (cy, by) in N4PAIRS:
        E4 = {'Z': E['S4,Z'], 'X': E['S4,x,%d,%s' % (cx, bx)], 'Y': E['S4,x,%d,%s' % (cy, by)],
              'XY': E['S4,xy,%d,%s,%d,%s' % (cx, bx, cy, by)]}
        cl = (cx - 1, 2 - cy, kind, cy - cx)
        s83.append((lab, CM.strip_cov_t(E4, T), cl if (cl[0] in DNEAR[kind] and cl[1] in DNEAR[kind]) else None))
    res = {'i': i, 'T': T, 'C0': C0, 'vac': vac, 'Uh': Uh, 'P2row': P2row, 'P2r': P2r, 'chW': chW, 'E': E, 'Ech': Ech,
           'odd': A['odd'][N], 's83': s83, 'tried': []}
    got = None
    for b in (bases or RB_ORDER):
        SL = RB_SETS[b]
        EB = b_entries(E, SL)
        oddc = set(j for j, s in enumerate(SL) if s in A['odd'][N])
        c0b = C0B if C0B is not None else basis_RB(CM.entry_points(EB, arb(T.mid())), C0, oddc, len(SL) - 1)
        chB = CM.chain_dual_t_RB(EB, T, vac, c0b, oddc, len(SL) - 1)
        tb = (((Uh / (chB['lam0'] * chB['lam0'])).upper() - 1 - chB['R99F2'].lower()) / 2).upper()
        leak = CM.routeb_leak(chB, Uh, tau=tau)
        if leak is None:
            res['tried'].append((b, False, tb))
            continue
        chU = dict(chW, Gl=leak['Gl'])
        prm = CM.setup(chU, P2r, Uh, vac, Gl=leak['Gl'], sblk=leak['sblk'])
        cand = {'basis': b, 'SL': SL, 'chB': chB, 'C0B': c0b, 'leak': leak, 'ch': chU, 'prm': prm}
        if not rows:
            res.update(cand)
            return res
        RkC = {}
        rws, tops, m0, top, dkf = CM.rows_cert(chU, prm, TWO_CLS, s83, RkC)
        cand.update({'rows': rws, 'tops': tops, 'm0': m0, 'top': top, 'dkf': dkf, 'RkC': RkC})
        ok = all(x[4] for x in rws) and all(x[2] for x in tops) and chW['par_exact'] is True and chB['par_exact'] is True
        res['tried'].append((b, ok, tb))
        got = cand
        if ok:
            break
    if got is None:
        return None
    res.update(got)
    return res


def rows_at_tau(r, tau):
    """route (b)'s rows on an evaluated piece r with tau_B replaced by tau (its chains kept): True when every row and top class passes.
    The break-even INFO's evaluation only, never a bound."""
    leak = CM.routeb_leak(r['chB'], r['Uh'], tau=tau)
    if leak is None:
        return False
    prm = CM.setup(dict(r['chW'], Gl=leak['Gl']), r['P2r'], r['Uh'], r['vac'], Gl=leak['Gl'], sblk=leak['sblk'])
    rws, tops = CM.rows_cert(dict(r['chW'], Gl=leak['Gl']), prm, TWO_CLS, r['s83'], {})[:2]
    return all(x[4] for x in rws) and all(x[2] for x in tops)


TAUBU = {}   # v1_14_3: (piece, break-even U factor, R_CERT/U_hi) per N, for the final's TAUB-U MIN


def taub_info(N, r, A):
    """TAUB (INFO): the break-even tau_B of the piece's taken set, the largest tau at which every row and top class
    passes (bisection in log tau over [1e-8, tau_B], or up to 0.1 when the piece passes), against its tau_B. v1_14_3 (
    main): with route (b)'s gap U_hi/lambda_0^2 - 1 - |R_B|_F^2 (= 2 tau_B), the break-even U factor 1 + 2 (TAUB - tau_B) /
    (U_hi/lambda_0^2) (tau_B grows by x U_hi/(2 lambda_0^2) when U_hi grows by the factor 1 + x, the B chain kept) and S4-U's
    R_CERT/U_hi at the piece; the factor goes to TAUBU for the final's minimum."""
    tb = r['leak']['tau']
    chB_ = r['chB']
    uq = float(((r['Uh'] / (chB_['lam0'] * chB_['lam0'])).upper()).mid())
    rcu = float((CM.fr(A['s4u'][(N, 'R_CERT')]) / r['Uh']).mid())
    tbf = float(tb.mid())
    ext = '; gap %.4e, U_hi/lambda_0^2 %.12f, S4-U R_CERT/U_hi %.3e' % (2.0 * tbf, uq, rcu)
    ok0 = rows_at_tau(r, tb)
    lo_, hi_ = arb(1e-8), (arb(1e-1) if ok0 else tb)
    if not rows_at_tau(r, lo_):
        return 'TAUB N=%d piece %d %s (INFO): fails even at tau_B = 1e-8 (tau_B %.4e)%s' % (N, r['i'], r['basis'], tbf, ext)
    if ok0 and rows_at_tau(r, hi_):
        return 'TAUB N=%d piece %d %s (INFO): passes up to tau_B = 0.1 (tau_B %.4e)%s; break-even U factor above 1 + %.3e' % (
            N, r['i'], r['basis'], tbf, ext, 2.0 * (0.1 - tbf) / uq)
    for _ in range(22):
        mid = (lo_ * hi_).sqrt()
        if rows_at_tau(r, mid):
            lo_ = mid
        else:
            hi_ = mid
    fac = 1.0 + 2.0 * (float(lo_.mid()) - tbf) / uq
    TAUBU.setdefault(N, []).append((r['i'], fac, rcu))
    return 'TAUB N=%d piece %d %s (INFO): the rows pass up to tau_B = %.4e (the piece\'s tau_B %.4e, ratio %.3f)%s; break-even U factor ' \
        '1 + %.3e (R_CERT/U_hi %.3g x that margin)' % (N, r['i'], r['basis'], float(lo_.mid()), tbf, float((lo_ / tb).mid()), ext, fac - 1.0,
                                                     (rcu / (fac - 1.0)) if fac > 1.0 else float('nan'))


def piece_summary(r):
    """(family minima {family: (headroom, class)}, failing rows, failing top-mode classes, RISK rows (passing, headroom < 2), the
    largest m0)."""
    fm = {}
    for fam, cl, h, lo_, ok in r['rows']:
        if fam not in fm or h < fm[fam][0]:
            fm[fam] = (h, cl)
    bad = [(fam, cl, lo_) for fam, cl, h, lo_, ok in r['rows'] if not ok]
    badtop = [(k, v) for k, v, ok in r['tops'] if not ok]
    risk = [(fam, cl, h) for fam, cl, h, lo_, ok in r['rows'] if ok and h < 2.0]
    m0max = max((v for k, v, ok in r['tops'] if v is not None), default=None)
    return fm, bad, badtop, risk, m0max


def lo_str(lo_):
    if isinstance(lo_, tuple):
        return '(strip %s, chain %s)' % tuple('n/a' if x is None else '%.6e' % float(x.mid()) for x in lo_)
    return '%.6e' % float(lo_.mid())


def piece_line(N, i, P2row, summ, pe=True, r=None):
    """v1_11: pe, the chain's par_exact: a piece whose chain is not exactly parity-pure is not ok. v1_12: with r (a
    piece_eval_RB result), route (b)'s taken set, its tau_B and the sets tried, after the '|' (PIECE_RE's fields are unchanged)."""
    fm, bad, badtop, risk, m0max = summ
    ok = not bad and not badtop and all(f_ in fm for f_ in FAMS4) and pe
    hd = lambda f_: fm[f_][0] if f_ in fm else float('nan')
    rb = '' if r is None else '; route (b) %s tau_B %.4e (tried %s)' % (r['basis'], float(r['leak']['tau'].mid()), ' '.join(
        '%s:%s' % (b_, 'ok' if ok_ else 'no') for b_, ok_, tb_ in r['tried']))
    return 'PIECE %d %04d h81=%.6g h82=%.6g h83=%.6g hlem=%.6g m0=%s risk=%d ok=%d | J [%r, %r]; minima at %s%s' % (
        N, i, hd('S8-1'), hd('S8-2'), hd('S8-3'), hd('lemma'), m0max, len(risk), int(ok), P2row['jlo'], P2row['jhi'],
        '; '.join('%s %s' % (f_, fm[f_][1] if f_ in fm else 'no rows') for f_ in FAMS4), rb)


def entry_thin(E, t, mode):
    """v1_12_5 (the rule): the bar-free entry values at t with every coefficient at a point of its span [LO_k, HI_k] (the record's
    independent coefficient intervals): the span's midpoint (mode 0), upper end (1) or lower end (-1), each an admissible entry; C-UNIF's
    thin values, {key: sum_k c_k t^k}."""
    tk = [CM.ONE, t, t * t, t * t * t]
    res = {}
    for key, (LO, HI, err) in E.items():
        bs = [CM.span(LO[k], HI[k]) for k in range(4)]
        cs = [arb(b.mid()) if mode == 0 else (arb(b.upper()) if mode > 0 else arb(b.lower())) for b in bs]
        res[key] = sum((cs[k] * tk[k] for k in range(4)), CM.ZERO)
    return res


def unif_piece(N, A, i, right_end=False, law_jhi=False):
    """C-UNIF on piece i: (1) the bar-free entry balls over the t-box contain their values at 9 equispaced t; (2) S4-U's upper end over
    the box is >= U at those t; (3) the M2(b) law used (at J_lo) is >= the law at 9 equispaced J of the piece (the last piece: J_lo 2^j).
    right_end: the box replaced by its right end in J (PLANT-RIGHTEND); law_jhi: the law taken at J_hi, or 2 J_lo on the last piece
    (PLANT-LAW-JHI). Returns the failing names. v1_12_2 (the rule, 2026-11-07): (1) holds for a point ball v when v lies inside the
    enclosure up to inside_r's slack (2^-20 rad(outer), C-MV's since v1_7) AND v's own midpoint lies inside the enclosure, so only the
    point evaluation's own rounding may poke out (unif_ok). kt_s8_diag_unif_v1 (01d978b1) and v1_1 (9caafcbc) found v1_12's C-UNIF
    failures (T,4,4 and T,6,6 at high J) to be point balls whose midpoints lie inside the enclosure and whose upper ends pass its upper
    end by 1e-10 .. 2e-9 of the enclosure's radius and of their own (at the box's upper t end): arb's radius rounding, not a wrong
    enclosure. PLANT-UNIF-SLACK (the pre item): a point ball 2^-10 rad(outer) beyond the upper end must fail unif_ok. v1_12_5 (the
    rule): (1) compares the enclosures with thin admissible entry values (entry_thin: every coefficient at its span's midpoint, upper end
    or lower end, at each of the 9 t), no longer with entry_points' balls, which carry the same coefficient spans as the enclosure; (2)
    compares thin values already (S4-U's coefficients are points)."""
    P2row = A['pieces'][N][i]
    jlo, jhi = P2row['jlo'], P2row['jhi']
    tp = CM.tpoints(jlo, jhi)
    T = tp[0] if right_end else CM.tball(jlo, jhi)
    enc = CM.entry_points(A['EP'][N], T)
    bad = sorted(set('entry ' + k for t in tp for mode in END_MODES for k, v in entry_thin(A['EP'][N], t, mode).items()
                     if not unif_ok(enc[k], v)))
    Uh = u_poly(A['s4u'], N, T).upper()
    if any(not (u_poly(A['s4u'], N, t).upper() <= Uh) for t in tp):
        bad.append('U')
    finite = not math.isinf(jhi)
    jl, jh = Fraction(jlo), (Fraction(jhi) if finite else None)
    lu = law_at(A, N, (jhi if finite else 2 * jlo) if law_jhi else jlo)
    Js = [jl + (jh - jl) * j / 8 for j in range(9)] if finite else [jl * 2 ** j for j in range(9)]
    for J in Js:
        lj = law_at(A, N, J)
        for nm in sorted(lj):
            if lu[nm] == 'inf':
                continue
            if lj[nm] == 'inf' or Fraction(lj[nm]) > Fraction(lu[nm]):
                bad.append('law ' + nm)
    return sorted(set(bad))


RSLACK = arb(1) / (1 << 20)   # v1_7: 2^-20, the comparison slack of C-MV and C-PIECE (arb's radii: a 30-bit mantissa, rounded up)


def inside_r(outer, inner, rel_rad=RSLACK, rel_mid=0):
    """inner inside outer up to a slack of rel_rad rad(outer) + rel_mid |mid(outer)| on each side (False for NaN or infinite ends)."""
    s = arb(outer.rad()) * rel_rad
    if rel_mid:
        s = s + abs(arb(outer.mid())) * rel_mid
    s = s.upper()
    return bool(inner.lower() >= (outer.lower() - s).lower() and inner.upper() <= (outer.upper() + s).upper())


def unif_ok(enc, v):
    """C-UNIF's test (v1_12_2, the rule): the point ball v inside the enclosure enc up to inside_r's slack, and v's own midpoint inside
    enc (so whatever pokes out is the point evaluation's own radius)."""
    m = arb(v.mid())
    return inside_r(enc, v) and bool(m >= enc.lower() and m <= enc.upper())


def _mv_setup(N, A, i, C0, SL=None, C0B=None):
    """C-MV's chains on piece i: (the piece's 9 sample t, cen(vac, zero_tgrad) the centered chain with zero bars, pt(t, vac) the bar-free
    point chain at t), on the W3 chain with tt=False or, with SL and C0B, route (b)'s B chain (chain_dual_t_RB and chain_RB) for the
    trial set SL with its basis C0B (v1_12_3: mv_piece's v1_12_2 body, shared with mvd_piece). v1_12_5: pt(t, vac, allow, par) takes
    the allowance constants and the parity decision to use (on_dual passes the centered chain's dual run's), as chain() and chain_RB()
    do. v1_13: pt(..., emode) builds the entries at t from entry_thin's coefficients in mode emode (each span's
    midpoint, upper end or lower end) instead of entry_points' balls, so the point chains are thin in the entry coefficients too;
    emode None keeps the balls (MV-ASIS, INFO)."""
    P2row = A['pieces'][N][i]
    T = CM.tball(P2row['jlo'], P2row['jhi'])

    def ent(E, t, emode):
        return CM.entry_points(E, t) if emode is None else entry_thin(E, t, emode)
    if SL is None:
        Ech = w3_keys(A['EP'][N])
        cen = lambda vac, ztg=False: CM.chain_dual_t(Ech, T, A['mains'][N], A['odd'][N], vac, C0, zero_bars=True, zero_tgrad=ztg, tt=False)
        pt = lambda t, vac, allow=None, par=None, emode=None: CM.chain(ent(Ech, t, emode), A['mains'][N], A['odd'][N], vac, C0,
                                                                       allow=allow, par=par, tt=False)
    else:
        EB = b_entries(A['EP'][N], SL)
        oddc = set(j for j, s in enumerate(SL) if s in A['odd'][N])
        cen = lambda vac, ztg=False: CM.chain_dual_t_RB(EB, T, vac, C0B, oddc, len(SL) - 1, zero_bars=True, zero_tgrad=ztg)
        pt = lambda t, vac, allow=None, par=None, emode=None: CM.chain_RB(ent(EB, t, emode), vac, C0B, oddc, len(SL) - 1, allow=allow,
                                                                          par=par)
    return CM.tpoints(P2row['jlo'], P2row['jhi']), cen, pt


def on_dual(pt, chc):
    """v1_12_5: the point chain pt(t, vac) on the allowance constants and the parity decision of the centered chain
    chc's dual run (chc['dual'][0]['allow'], ['par_exact']), as its midpoint run takes them: end_chain's modes then sit at the centre and
    the two corners of the centered chain's own allowance box. v1_13: and the entries' mode emode."""
    chd = chc['dual'][0]
    return lambda t, vac, emode=None: pt(t, vac, chd['allow'], chd['par_exact'], emode)


def mv_piece(N, A, i, C0, vac, zero_tgrad=False, SL=None, C0B=None):
    """C-MV on piece i (bar-free, the t slot only): the centered chain (s8core's chain_dual_t with zero bars) contains the bar-free point
    chains at the piece's 9 sample t, leaf by leaf, up to inside_r's slack (v1_7; s8core's mv_check compares with none). Returns (number
    of chain leaves, the failing leaf paths); zero_tgrad is PLANT-MV. v1_12: the W3 chain with tt=False; with SL and C0B, C-MV-B, the
    same check on route (b)'s B chain (chain_dual_t_RB against chain_RB) for the trial set SL with its basis C0B. v1_12_3 (main
    0fb1b956): both chains with the place-1 allowance delta set to 0, as the bars are: the point chains' balls of relative width ~delta
    make arb round their midpoints at about 2^-29 relative and widen their radii by ~1e-3 (kt_s8_diag_cmv_v2 c13affed, v2_1 b1f75c59),
    above inside_r's slack; delta's own checks are mvd_piece's. v1_12_5: the point chains are thin, as C-MV-DELTA's are since
    v1_12_4: at each sample t and in each of END_MODES, end_chain at delta = 0 (the stand-in at the point 0, so lambda_0 = m-hat
    exactly; it must be met once, else the pseudo-leaf '(stand-in met k times)' fails) with every wrapped allowance at its ball's
    midpoint, upper end or lower end. With the allowances as balls, the point ball met the centered ball's edge at the box-end samples
    on the W3 leaves /beta/kk and /AXm/kk (kt_s8_diag_cmv_v3 b89c517f: 75 of 201 pieces; thin, none)."""
    tp, cen, pt = _mv_setup(N, A, i, C0, SL, C0B)
    vac0 = dict(vac, delta=arb(0))
    chc = cen(vac0, zero_tgrad)
    cl = dict(CM.leaves(chc))
    ptd = on_dual(pt, chc)   # v1_12_5: the thin chains on the centered chain's own allowance box
    bad = set()
    for t in tp:
        for mode in END_MODES:
            ch, hits, nw, na = end_chain(ptd, t, vac0, 1, mode)
            if hits != 1:
                bad.add('(stand-in met %d times)' % hits)
            bad |= set(p for p, v in CM.leaves(ch) if p not in cl or not inside_r(cl[p], v))
    return len(cl), sorted(bad)


class _DeltaEnd(object):
    """C-MV-DELTA's stand-in for vac['delta'] (v1_12_3, no core change): while end_chain runs, pm() maps this object to the exact point
    sign u, u = abs(delta).upper() (the end of pm(delta), s8core's place-1 ball), so place 1 gives the thin lambda_0 = m-hat (1 + sign u)."""

    def __init__(self, delta, sign):
        u = abs(delta).upper()
        self.point = u if sign > 0 else -u
        self.hits = 0


END_MODES = (0, 1, -1)   # v1_12_4: end_chain's wrapped allowances all at their balls' midpoints, all at the upper ends, all at the lower ends


def end_chain(pt, t, vac, sign, mode):
    """the thin point chain pt(t, .) at the exact place-1 endpoint lambda_0 = m-hat (1 + sign u) (C-MV-DELTA): s8core's pm is replaced
    by a wrapper for this one call (restored in finally). The stand-in goes to the point sign u. v1_12_4: every other pm(r) of the
    chain (the wrapped allowances, module docstring) goes to a point of its own ball b = pm(r) too: b's midpoint (mode 0), b's upper end
    (mode 1) or b's lower end (mode -1). s8core's pm(r) is the symmetric ball [-|r|, |r|] (|r| = abs(r).upper(), its radius rounded up),
    so these points are 0 and +-|r| up to that rounding; the wrapped balls whose midpoint is not 0 are counted (none expected). Each mode
    is one fixed choice of the allowance parameters inside the balls the centered chain carries, and the chain is thin. chain() and
    chain_RB() read vac['delta'] once, in place 1, so the stand-in must be met exactly once. Returns (the chain, the stand-in meetings,
    the wrapped pm calls, the wrapped balls with a nonzero midpoint). v1_13: pt also receives the mode for the entries'
    coefficients (on_dual's emode), so the chain is thin in every coordinate set the centered chain carries as a ball: delta, the wrapped
    allowances and the entry coefficients."""
    if CM.pm is not PM0:
        raise ValueError('s8core\'s pm is not its own before an endpoint chain')
    mk = _DeltaEnd(vac['delta'], sign)
    cnt = [0, 0]

    def pm_end(r):
        if r is mk:
            mk.hits += 1
            return mk.point
        b = PM0(r)
        cnt[0] += 1
        if b.mid() != 0:
            cnt[1] += 1
        return arb(b.mid()) if mode == 0 else (arb(b.upper()) if mode > 0 else arb(b.lower()))
    CM.pm = pm_end
    try:
        ch = pt(t, dict(vac, delta=mk), mode)   # v1_13: the entries' coefficients in the same mode
    finally:
        CM.pm = PM0
    return ch, mk.hits, cnt[0], cnt[1]


def mvd_piece(N, A, i, C0, vac, SL=None, C0B=None, plant=False):
    """v1_12_3, the place-1 allowance delta on piece i, on the W3 chain or, with SL
    and C0B, the B chain (as mv_piece), with zero bars:
    - C-MV-DELTA: at each of the 9 sample t, the point chains at the two exact endpoints lambda_0 = m-hat (1 + u) and
      m-hat (1 - u), with every wrapped allowance at a point of its ball in each of END_MODES (end_chain; v1_12_4: thin, so arb keeps
      its full precision and no allowance ball of the point chain meets the centered ball's edge), lie in the centered chain computed
      with delta as is, up to inside_r's slack (the 2^-20 rule), leaf by leaf, with the stand-in met once in every chain;
      plant=True (PLANT-MV-DELTA) compares the same endpoint chains with the centered chain computed with delta = 0 instead, which must
      fail in every mode, and skips the rest;
    - C-MV-MID (the theta = 0 values): v1_12_5 (the rule): the thin theta = 0 chains, end_chain at delta = 0 (the stand-in at the
      point 0) in each of END_MODES, lie inside the delta-kept centered chain under the 2^-20 rule, in place of v1_12_3's midpoints of
      the delta-kept ball chains (thin values, but not admissible points);
    - MV-ASIS (INFO): the delta-kept ball point chains (their own allowances) against the delta-kept centered chain with inside_r, the
      largest excess relative to the centered radius and to the point ball's own radius (v1_12_2's comparison; information only).
    v1_12_5: every thin chain runs on the delta-kept centered chain's dual allowance constants and parity decision
    (on_dual), so the modes sit at the centre and the corners of the centered chain's own allowance box.
    Returns {'nl': the centered chain's leaves, 'u': float(u), 'end', 'mid', 'asis': the failing leaf paths (sets), 'endm': the failing
    leaf paths per mode, 'xo', 'xp': MV-ASIS's largest excesses, 'hits': the set of end_chain's meeting counts, 'nend': the endpoint
    chains, 'nmid': the theta = 0 chains, 'wrap': the set of the endpoint chains' wrapped pm counts, 'asym': the wrapped balls with a
    nonzero midpoint, summed}."""
    tp, cen, pt = _mv_setup(N, A, i, C0, SL, C0B)
    chcd = cen(vac)   # the delta-kept centered chain
    vac0 = dict(vac, delta=arb(0))
    cl = dict(CM.leaves(cen(vac0) if plant else chcd))
    ptd = on_dual(pt, chcd)
    d = {'nl': len(cl), 'u': float(abs(vac['delta']).upper()), 'end': set(), 'mid': set(), 'asis': set(), 'xo': 0.0, 'xp': 0.0,
         'hits': set(), 'endm': {m: set() for m in END_MODES}, 'nend': 0, 'nmid': 0, 'wrap': set(), 'asym': 0}
    for t in tp:
        for sign in (1, -1):
            for mode in END_MODES:
                ch, hits, nw, na = end_chain(ptd, t, vac, sign, mode)
                d['hits'].add(hits)
                d['nend'] += 1
                d['wrap'].add(nw)
                d['asym'] += na
                b_ = set(p for p, v in CM.leaves(ch) if p not in cl or not inside_r(cl[p], v))
                d['end'] |= b_
                d['endm'][mode] |= b_
        if plant:
            continue
        for mode in END_MODES:   # v1_12_5: C-MV-MID, the thin theta = 0 chains
            ch, hits, nw, na = end_chain(ptd, t, vac0, 1, mode)
            d['hits'].add(hits)
            d['nmid'] += 1
            d['mid'] |= set(p for p, v in CM.leaves(ch) if p not in cl or not inside_r(cl[p], v))
        for p, v in CM.leaves(pt(t, vac)):
            o = cl.get(p)
            if o is None:
                d['asis'].add(p)
                continue
            if not inside_r(o, v):
                d['asis'].add(p)
                ex = max(float((v.upper() - o.upper()).mid()), float((o.lower() - v.lower()).mid()))
                d['xo'] = max(d['xo'], ex / float(o.rad()) if o.rad() > 0 else float('inf'))
                d['xp'] = max(d['xp'], ex / float(v.rad()) if v.rad() > 0 else float('inf'))
    return d


def mvd_line(fails, N, i, sfx, lab, d):
    """the C-MV-DELTA and C-MV-MID line of one chain (sfx '' for the W3 chain, '-B' for the B chain) from mvd_piece's result d; the
    endpoint gate also needs the stand-in met exactly once in every endpoint chain, and the line states it; v1_12_5:
    the theta = 0 chains of C-MV-MID too."""
    eb, mb = sorted(d['end']), sorted(d['mid'])
    once = d['hits'] == {1}
    return ('C-MV-DELTA%s N=%d piece %d %s: %d thin point chains (9 t, lambda_0 = m-hat (1 +- %.3e) exactly, on the dual run\'s allow '
            'and par, the wrapped allowances (%s per chain, %s) and the entry coefficients (v1_13) at their midpoints, upper ends and '
            'lower ends) against the '
            'delta-kept centered chain: %d leaves, failing %d%s -> %s; C-MV-MID%s: %d thin theta = 0 chains (delta at 0, the same modes) '
            'inside it: failing %d%s -> %s; the place-1 stand-in met %s' % (
                sfx, N, i, lab, d['nend'], d['u'], '/'.join(str(x) for x in sorted(d['wrap'])),
                'all symmetric' if not d['asym'] else '%d balls with a nonzero midpoint' % d['asym'], d['nl'], len(eb),
                (' (%s)' % ', '.join(eb[:4])) if eb else '', gate(fails, 'C-MV-DELTA' + sfx, not eb and once), sfx, d['nmid'], len(mb),
                (' (%s)' % ', '.join(mb[:4])) if mb else '', gate(fails, 'C-MV-MID' + sfx, not mb and once),
                'once in every chain' if once else '%s times, not once' % sorted(d['hits'])))


def ent_thin_bar(E, t, mode):
    """v1_13: the entries at t with every coefficient at a point of its span (entry_thin,
    mode) and every bar offset at the same point of its bar box [-err_b, err_b]: 0 (mode 0), +err_b (1), -err_b (-1); E's err are the
    piece's banded bars (ep_at)."""
    th = entry_thin(E, t, mode)
    if mode == 0:
        return th
    return {k: th[k] + (CM.fr(Fraction(E[k][2])) if mode > 0 else -CM.fr(Fraction(E[k][2]))) for k in th}


def _corner(vac, mode):
    """the place-1 choice of a thin point in mode m: delta at 0 (mode 0, the stand-in at the point 0) or at m u (modes +-1)."""
    return (dict(vac, delta=arb(0)), 1) if mode == 0 else (vac, mode)


def mvbar_piece(N, A, r, plant=False, keep=False):
    """v1_14: keep=True also returns the thin W3 chains, res['thinW'] = [(index of t, mode, chain)] in loop order, and the compared W3
    centered chain, res['cW'] (C-MV-SF and C-TARGET-SF reuse them; nothing else changes).
    v1_13 C-MV-BAR, C-MV-BAR-B (the bar slots are never exercised by the zero-bar C-MV
    family): the piece's own centered chains WITH its banded bars (piece_eval_RB's chW and chB) contain the thin point chains at the 9
    sample t whose entries take ent_thin_bar's coefficients and bar corners, delta _corner's point and every wrapped allowance the same
    mode (end_chain on the dual's allow and par), leaf by leaf under inside_r's 2^-20 rule. plant=True (PLANT-MV-BAR): the same kind
    of points, on the zero-bar run's own allowance constants and parity decision (so the bar offsets are the only coordinate outside the
    compared chains' box), against the zero-bar centered chains, which must fail in modes 1 and -1 on each chain (mode 0 puts every bar
    offset at 0, a point the zero-bar chains hold by construction). Returns {'W3': (leaves, failing), 'B': (leaves, failing), ('bym', 'W3') and ('bym', 'B'):
    {mode: failing leaves}, 'hits': set}."""
    i = r['i']
    P2row = A['pieces'][N][i]
    T = r['T']
    tp = CM.tpoints(P2row['jlo'], P2row['jhi'])
    E = r['E']
    Ech = r['Ech']
    EB = b_entries(E, r['SL'])
    oddc = set(j for j, s in enumerate(r['SL']) if s in A['odd'][N])
    nst = len(r['SL']) - 1
    vac = r['vac']
    if plant:
        cW = CM.chain_dual_t(Ech, T, A['mains'][N], A['odd'][N], vac, r['C0'], zero_bars=True, tt=False)
        cB = CM.chain_dual_t_RB(EB, T, vac, r['C0B'], oddc, nst, zero_bars=True)
    else:
        cW, cB = r['chW'], r['chB']
    dW, dB = cW['dual'][0], cB['dual'][0]   # the compared chains' own allowance box (the plant: the zero-bar run's, so only bars differ)
    ptW = lambda t, v, emode: CM.chain(ent_thin_bar(Ech, t, emode), A['mains'][N], A['odd'][N], v, r['C0'], allow=dW['allow'],
                                       par=dW['par_exact'], tt=False)
    ptB = lambda t, v, emode: CM.chain_RB(ent_thin_bar(EB, t, emode), v, r['C0B'], oddc, nst, allow=dB['allow'], par=dB['par_exact'])
    res = {'hits': set()}
    for lab, cen, pt in (('W3', cW, ptW), ('B', cB, ptB)):
        cl = dict(CM.leaves(cen))
        bad, bym = set(), {m: set() for m in END_MODES}
        for it, t in enumerate(tp):
            for m in END_MODES:
                vx, sg = _corner(vac, m)
                ch, hits, nw, na = end_chain(pt, t, vx, sg, m)
                res['hits'].add(hits)
                b_ = set(p for p, v in CM.leaves(ch) if p not in cl or not inside_r(cl[p], v))
                bad |= b_
                bym[m] |= b_
                if keep and lab == 'W3':
                    res.setdefault('thinW', []).append((it, m, ch))
        res[lab] = (len(cl), sorted(bad))
        res['bym', lab] = {m: len(bym[m]) for m in END_MODES}
    if keep:
        res['cW'] = cW
    return res


def mvbar_line(fails, N, i, d):
    """the C-MV-BAR line of a piece from mvbar_piece's result d."""
    once = d['hits'] == {1}
    (nw, bw), (nb, bb) = d['W3'], d['B']
    return ('C-MV-BAR N=%d piece %d (the centered chains with the piece\'s banded bars against thin points at 9 t with every bar offset, '
            'coefficient, wrapped allowance and delta at its midpoint, upper or lower end; the stand-in met %s): W3 %d leaves, failing %d%s '
            '-> %s; B %d leaves, failing %d%s -> %s' % (
                N, i, 'once in every chain' if once else '%s times, not once' % sorted(d['hits']), nw, len(bw),
                (' (%s)' % ', '.join(bw[:4])) if bw else '', gate(fails, 'C-MV-BAR', not bw and once), nb, len(bb),
                (' (%s)' % ', '.join(bb[:4])) if bb else '', gate(fails, 'C-MV-BAR-B', not bb and once)))


def target_piece(N, A, r, etap_scale=None):
    """v1_13 C-TARGET, the C1 check (the review NOTE_LEMMA_CENTERED_FORM_V2 8ca6c894, C1 (c) and (d)): the
    thin checks compare G with G and cannot catch a bound constant inside G that is too small; this compares the piece's box constants,
    computed with every theta coordinate a ball in G's own basis and choices, with their targets at thin admissible inputs (3 sample t:
    the box ends and the centre; END_MODES with ent_thin_bar's coefficients and bar corners, _corner's delta and pinned allowances),
    in the same bases (C0, C0B), parity split and choices:
    - the allowance constants: every centered constant (a1 and each a_, the W3 dual run's allow) >= the thin point chain's own;
    - route (b)'s leakage: tau_B and the block bound sblk of the piece >= routeb_leak at the thin B chain;
    - spectral targets by an independent eigensolver (numpy.linalg, float64 on the thin balls' midpoints): eta+ and eta- (setup's) >=
      sqrt(lambda_max) of the thin Gl's even and odd blocks; Rn >= |R|_2 of the thin W3 R; r_bb (a Gershgorin norm) >= |R_BB block|_2
      of the thin B chain.
    Every comparison is box >= target (1 - 1e-10): the 1e-10 relative is a float64 rounding allowance fixed before any run (float64
    eigenvalues are good to ~1e-15 relative here), so a box constant short of its target by more than that fails. The compared
    targets do not depend on the parity decision (allow's keys, R, tau_B, Gl, sblk and r_bb are computed before it is used), so the
    thin chains take their own.
    etap_scale (PLANT-TARGET only): eta+ multiplied by it, which must fail. Returns (checks, failures, largest target/box ratio)."""
    import numpy as np
    i = r['i']
    P2row = A['pieces'][N][i]
    tp = CM.tpoints(P2row['jlo'], P2row['jhi'])
    E, Ech = r['E'], r['Ech']
    EB = b_entries(E, r['SL'])
    oddc = set(j for j, s in enumerate(r['SL']) if s in A['odd'][N])
    nst = len(r['SL']) - 1
    vac, Uh, prm, leak = r['vac'], r['Uh'], r['prm'], r['leak']
    alw = r['chW']['dual'][0]['allow']
    pi = r['ch']['pi']
    K = len(pi)
    ev = [k for k in range(K) if pi[k] > 0]
    od = [k for k in range(K) if pi[k] < 0]
    etap = prm['etap'] * arb(etap_scale) if etap_scale is not None else prm['etap']
    ptW = lambda t, v, emode: CM.chain(ent_thin_bar(Ech, t, emode), A['mains'][N], A['odd'][N], v, r['C0'], tt=False)
    ptB = lambda t, v, emode: CM.chain_RB(ent_thin_bar(EB, t, emode), v, r['C0B'], oddc, nst)
    mid = lambda M: np.array([[float(x.mid()) for x in row] for row in M])
    checks, fl, worst = 0, [], 0.0

    def cmp(name, box, target):
        nonlocal checks, worst
        checks += 1
        b, tg = float(box.upper()) if isinstance(box, arb) else float(box), float(target)
        worst = max(worst, tg / b if b > 0 else float('inf'))
        if not (tg * (1 - 1e-10) <= b):
            fl.append(name)
    for t in (tp[0], tp[4], tp[8]):
        for m in END_MODES:
            vx, sg = _corner(vac, m)
            chP, h1, _w, _a = end_chain(ptW, t, vx, sg, m)
            chBP, h2, _w, _a = end_chain(ptB, t, vx, sg, m)
            if h1 != 1 or h2 != 1:
                fl.append('stand-in met %d / %d times' % (h1, h2))
            for k, a_ in chP['allow'].items():
                checks += 1
                if not (alw[k] >= a_):
                    fl.append('allowance %s' % (k,))
            lg = CM.routeb_leak(chBP, Uh)
            if lg is not None:
                cmp('tau_B', leak['tau'], float(lg['tau'].upper()))
                cmp('sblk', leak['sblk'], float(lg['sblk'].upper()))
                G = mid(lg['Gl'])
                for nm, ix, bx in (('eta+', ev, etap), ('eta-', od, prm['etam'])):
                    if ix:
                        cmp(nm, bx, math.sqrt(max(0.0, max(np.linalg.eigvalsh(G[np.ix_(ix, ix)])))))
            cmp('Rn', prm['Rn'], float(np.linalg.norm(mid(chP['R']), 2)))
            RB = mid(chBP['R'])
            if RB.shape[0] > 3:
                cmp('r_bb', leak['r_bb'], float(np.linalg.norm(RB[3:, 3:], 2)))
    return checks, fl, worst


def target_line(fails, N, i, res):
    checks, fl, worst = res
    return ('C-TARGET N=%d piece %d (the C1 check: the piece\'s box constants against their targets at thin admissible inputs, 3 t x 3 '
            'modes, in G\'s own bases and choices; allowances, tau_B, sblk, eta+-, Rn, r_bb): %d checks, largest target/box %.4f, failing '
            '%d%s -> %s' % (N, i, checks, worst, len(fl), (' (%s)' % ', '.join(sorted(set(fl))[:4])) if fl else '',
                            gate(fails, 'C-TARGET', not fl)))


def ent_thin_bar_by(E, t, modes):
    """v1_14_1: ent_thin_bar with a mode per key ({key: 1 or -1}): each key's coefficients at its spans' upper (1) or lower (-1) ends
    and its bar offset at +err_b or -err_b (C-MV-S83's gradient-sign corners)."""
    return {k: ent_thin_bar({k: E[k]}, t, mk)[k] for k, mk in modes.items()}


def s83_piece(N, A, r, plant=False):
    """v1_14_1 (the review DELTA_KT_S8_CERT_V1_13 c17ba702 (c)): at each sample t also the two gradient-sign corners of the pair, every
    entry's coefficients and bar offset at the end its sensitivity points to (G+) or away from (G-), the signs of f's gradient at the
    mode-0 point: Cov J^2 has sensitivities of mixed sign, so the all-upper and all-lower modes do not reach its extremes. They count
    as points of the check and, in the plant, are printed (the plant's gate stays modes 1 and -1). Returns (points, failing pair labels,
    {mode or 'G+', 'G-': failing pairs}).
    v1_13 C-MV-S83 (beyond the lemma's list: S8-3's strip enclosure, s8core's strip_cov_t, is a centered form in (t, the four bar offsets)
    with the coefficient spans as theta, and no check exercised it): each of the piece's N4PAIRS strip enclosures (r['s83'], the ones the
    S8-3 rows use) contains Cov J^2 = XY/Z - X Y/Z^2 at the thin points, the 9 sample t x END_MODES with ent_thin_bar's entries (every
    coefficient and bar offset at the same point), under inside_r's 2^-20 rule. The function holds no constant standing for a bound, so
    its target at thin inputs is the function itself and this is also the instance's C1 check. plant=True (PLANT-MV-S83): the same
    points against the enclosures recomputed with zero bars must fail in modes 1 and -1. Returns (points, failing pair labels, {mode:
    failing pairs})."""
    P2row = A['pieces'][N][r['i']]
    tp = CM.tpoints(P2row['jlo'], P2row['jhi'])
    E = r['E']
    f = lambda W: W['XY'] / W['Z'] - W['X'] * W['Y'] / (W['Z'] * W['Z'])
    n, bad, bym = 0, set(), {m: set() for m in END_MODES + ('G+', 'G-')}
    if len(r['s83']) != len(N4PAIRS):
        raise ValueError('C-MV-S83: %d strip enclosures for %d pairs' % (len(r['s83']), len(N4PAIRS)))
    for (lab, kind, (cx, bx), (cy, by)), (lab2, enc, cl) in zip(N4PAIRS, r['s83']):
        if lab2 != lab:
            raise ValueError('C-MV-S83: the strip enclosures are not in N4PAIRS order (%s, %s)' % (lab, lab2))
        E4 = {'Z': E['S4,Z'], 'X': E['S4,x,%d,%s' % (cx, bx)], 'Y': E['S4,x,%d,%s' % (cy, by)],
              'XY': E['S4,xy,%d,%s,%d,%s' % (cx, bx, cy, by)]}
        if plant:
            enc = CM.strip_cov_t({k: (LO, HI, Fraction(0)) for k, (LO, HI, err) in E4.items()}, r['T'])
        for t in tp:
            for m in END_MODES:
                n += 1
                if not inside_r(enc, f(ent_thin_bar(E4, t, m))):
                    bad.add(lab)
                    bym[m].add(lab)
            # v1_14_1 (the review c17ba702 (c)): the two gradient-sign corners, each entry at the end its sensitivity points to (or
            # away from), from the signs of f's gradient at the mode-0 point: d/dXY = 1/Z, d/dX = -Y/Z^2, d/dY = -X/Z^2,
            # d/dZ = -XY/Z^2 + 2 X Y/Z^3
            w0 = {k: float(v.mid()) for k, v in ent_thin_bar(E4, t, 0).items()}
            gs = {'XY': 1.0 / w0['Z'], 'X': -w0['Y'] / w0['Z'] ** 2, 'Y': -w0['X'] / w0['Z'] ** 2,
                  'Z': -w0['XY'] / w0['Z'] ** 2 + 2.0 * w0['X'] * w0['Y'] / w0['Z'] ** 3}
            for cn, sgn in (('G+', 1), ('G-', -1)):
                n += 1
                if not inside_r(enc, f(ent_thin_bar_by(E4, t, {k: (sgn if gs[k] >= 0 else -sgn) for k in E4}))):
                    bad.add(lab)
                    bym[cn].add(lab)
    return n, sorted(bad), {m: len(bym[m]) for m in bym}


def s83_line(fails, N, i, res):
    n, bad, bym = res
    return ('C-MV-S83 N=%d piece %d (S8-3\'s strip enclosures with their bars against Cov J^2 at thin points, 9 t x (3 modes, every '
            'coefficient and bar offset at its midpoint, upper or lower end, + 2 gradient-sign corners, v1_14_1)): %d points over %d pairs, '
            'failing pairs %d%s -> %s' % (
                N, i, n, len(N4PAIRS), len(bad), (' (%s)' % ', '.join(bad[:4])) if bad else '', gate(fails, 'C-MV-S83', not bad)))


SF_PICK = (3, 2)   # v1_14: C-MV-SF and C-TARGET-SF take the 3 S8-2 rows and the 2 lemma rows of smallest headroom on the piece


def sf_classes(r):
    """v1_14: the sf_pair classes that C-MV-SF and C-TARGET-SF check on an evaluated piece r: its SF_PICK[0] S8-2 rows and SF_PICK[1]
    lemma rows of smallest headroom (r['rows'], route (b)'s taken set), as [(family, class)]."""
    res = []
    for fam, n in (('S8-2', SF_PICK[0]), ('lemma', SF_PICK[1])):
        rows = sorted((x for x in r['rows'] if x[0] == fam), key=lambda x: x[2])
        res += [(fam, x[1]) for x in rows[:n]]
    return res


def sf_piece(N, A, r, mb, plant=False, c1_scale=None):
    """v1_14 C-MV-SF and C-TARGET-SF (Lemma M v2's per-instance checks for sf_pair's class-level form, which the S8-2
    and lemma rows use; the review 0226c38c sect. 5 had left it uncovered), on the classes of sf_classes(r), through s8core_v1_11's info
    record of sf_pair on r['ch'] (the W3 chain with its duals):
    - C-MV-SF (thin): with the box's own constants C1 = t1 + ddet, dz and sign sg, at each of mvbar_piece's 27 thin W3 chains
      mb['thinW'] (9 t x END_MODES: every coefficient, bar offset, wrapped allowance and delta at the same point, on the dual's allow and
      par), Num_t and Z_t = cov2 on the thin chain with R_t^k: Num_t - C1 lies in the centered ball topc and, for each dd the box
      evaluated (dz, -dz), (Num_t - C1)/(sg Z_t + dd)^2 lies in that centered ball, under the 2^-20 rule. A class whose class-level form
      is not active on the piece (Z of no certain sign) is counted, not checked.
    - C-TARGET-SF (C1): the box's C1 and dz >= sf_pair's own C1 and dz on the thin W3 chains at the 3 sample t (the box ends and the
      centre) x END_MODES, with the same prm, under C-TARGET's float allowance (box >= target (1 - 1e-10)).
    plant=True (PLANT-MV-SF): mb from mvbar_piece(..., plant=True, keep=True), so thin chains on the zero-bar run's allowance box, and the
    class-level balls from the zero-bar W3 duals (sf_pair on r['ch'] with 'dual' replaced, so C1, dz and sg stay the box's): modes 1 and
    -1 must each fail somewhere; C-TARGET-SF is skipped. c1_scale (PLANT-TARGET-SF): the box C1 multiplied by it in C-TARGET-SF, which
    must fail. Returns {'classes', 'active', 'used', 'points', 'fail': [(class, what)], 'bym': {mode: failing points}, 'tchecks',
    'tfail': [names], 'tworst'}."""
    ch = dict(r['ch'], dual=mb['cW']['dual']) if plant else r['ch']
    prm = r['prm']
    res = {'classes': 0, 'active': 0, 'used': 0, 'points': 0, 'fail': [], 'bym': {m: 0 for m in END_MODES}, 'tchecks': 0, 'tfail': [],
           'tworst': 0.0}
    RkT = {}   # (index of the thin chain, k): R_t^k
    for fam, cl in sf_classes(r):
        dL, dR, kind, m = cl
        info = {}
        CM.sf_pair(ch, prm, dL, dR, kind, m, {}, info=info)
        res['classes'] += 1
        k, C1, dz = info['k'], info['C1'], info['dz']
        if 'topc' in info:
            res['active'] += 1
            res['used'] += 1 if info['used'] else 0
            sg = info['sg']
            for j, (it, mode, cht) in enumerate(mb['thinW']):
                if (j, k) not in RkT:
                    RkT[j, k] = CM.mpow(cht['R'], k)
                numt, Zt = CM.cov2(cht, dL, dR, kind, RkT[j, k])[:2]
                res['points'] += 1
                bad = [] if inside_r(info['topc'], numt - C1) else ['Num - C1']
                for dk, dd in (('+dz', dz), ('-dz', -dz)):
                    cb = info['cen'].get(dk)
                    if cb is not None and not inside_r(cb, (numt - C1) / ((sg * Zt + dd) * (sg * Zt + dd))):
                        bad.append(dk)
                if bad:
                    res['fail'].append(('%s %s' % (fam, cl), '/'.join(bad)))
                    res['bym'][mode] += 1
        if plant:
            continue
        c1b = C1 * arb(c1_scale) if c1_scale is not None else C1
        for it, mode, cht in mb['thinW']:
            if it not in (0, 4, 8):
                continue
            itn = {}
            CM.sf_pair(cht, prm, dL, dR, kind, m, {}, info=itn)
            for nm, bx, tg in (('C1', c1b, itn['C1']), ('dz', dz, itn['dz'])):
                res['tchecks'] += 1
                b, g = float(bx.upper()), float(tg.upper())
                res['tworst'] = max(res['tworst'], g / b if b > 0 else (0.0 if g <= 0 else float('inf')))
                if not (g * (1 - 1e-10) <= b):
                    res['tfail'].append('%s %s %s' % (fam, cl, nm))
    return res


def sf_line(fails, N, i, d):
    return ('C-MV-SF N=%d piece %d (sf_pair\'s class-level form on the %d S8-2 and %d lemma rows of smallest headroom: Num - C1 and '
            '(Num - C1)/(sg Z + dd)^2 at the 27 thin W3 chains inside its centered balls, with the box\'s C1, dz and sg): %d classes, %d '
            'with the class-level form active (%d of them binding it), %d points, failing %d%s -> %s; C-TARGET-SF (the box\'s C1 and dz '
            'against sf_pair\'s own on the thin chains at 3 t x 3 modes, same prm): %d checks, largest target/box %.4f, failing %d%s -> %s' % (
                N, i, SF_PICK[0], SF_PICK[1], d['classes'], d['active'], d['used'], d['points'], len(d['fail']),
                (' (%s)' % ', '.join('%s: %s' % x for x in d['fail'][:3])) if d['fail'] else '', gate(fails, 'C-MV-SF', not d['fail']),
                d['tchecks'], d['tworst'], len(d['tfail']), (' (%s)' % ', '.join(sorted(set(d['tfail']))[:3])) if d['tfail'] else '',
                gate(fails, 'C-TARGET-SF', not d['tfail'])))


def core_plants(nofire, A, N, r):
    """v1_13 PLANT-C5-G00, PLANT-C5-T00, PLANT-C5-DSQRT, PLANT-C5-DDIV, PLANT-C6 (s8core_v1_10's gates): a W3 chain whose g00 or T00 is
    a ball through 0, a dual square root and a division by a dual whose value balls hold 0, and _cen with disjoint balls must each raise
    the core's ValueError with its own tag, C5 or C6 (counted as a refusal here; any other exception does not fire)."""
    tm = arb(r['T'].mid())
    V0 = CM.entry_points(r['Ech'], tm)

    def raises(fn, tag):
        def g():
            try:
                fn()
            except ValueError as e:
                if str(e).startswith(tag):
                    raise Refused(str(e)[:120])
                raise
        return g
    straddle = arb(0, 1)
    Vg, Vt = dict(V0), dict(V0)
    Vg[('g', 0, 0)] = straddle
    Vt[('T', 0, 0)] = straddle
    plant(nofire, 'PLANT-C5-G00', raises(lambda: CM.chain(Vg, A['mains'][N], A['odd'][N], r['vac'], r['C0'], tt=False), 'C5:'))
    plant(nofire, 'PLANT-C5-T00', raises(lambda: CM.chain(Vt, A['mains'][N], A['odd'][N], r['vac'], r['C0'], tt=False), 'C5:'))
    dd = CM.D(straddle, [arb(1)])
    plant(nofire, 'PLANT-C5-DSQRT', raises(lambda: dd.sqrt(), 'C5:'))
    plant(nofire, 'PLANT-C5-DDIV', raises(lambda: arb(1) / dd, 'C5:'))
    qd = CM.D(arb(0, 1), [arb(0)])
    plant(nofire, 'PLANT-C6', raises(lambda: CM._cen(qd, arb(5, 1) + arb(10), [arb(0)]), 'C6:'))


def fires(nofire, name, fired, detail):
    out('%s: %s -> %s' % (name, detail, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        nofire.append(name)


def hold_probe(F, in_domain=False):
    """the factor at which calib checks that f_ok still holds: F/1.1; with in_domain (v1_14_3, PLANT-U only) F/1.1 when
    F > 1.1, else sqrt(F), strictly between 1 and F."""
    return F / 1.1 if (not in_domain or F > 1.1) else math.sqrt(F)


def calib(f_ok, steps=12, in_domain=False):
    """the factor F > 1 at which f_ok turns False: a bracket by squaring from 2 (up to 2^64), then bisection in log F. Returns (F,
    f_ok(F/1.1), f_ok(1.1 F)), or None when f_ok(1) is False or f_ok still holds at 2^64. A factor at which the evaluation itself
    breaks down (a Cholesky pivot not positive, a division by a ball holding 0) counts as a failure there. v1_14_3:
    in_domain (PLANT-U only) checks the hold at hold_probe(F, True), for a factor whose domain starts at its certified value (F = 1):
    F/1.1 < 1 would leave the domain, and max(1, F/1.1) would only re-read the precondition f_ok(1)."""
    raw = f_ok

    def f_ok(F):
        try:
            return raw(F)
        except (ValueError, ArithmeticError):
            return False
    if not f_ok(1.0):
        return None
    lo_, hi_ = 1.0, 2.0
    while f_ok(hi_):
        lo_, hi_ = hi_, hi_ * hi_
        if hi_ > 2.0 ** 64:
            return None
    for _ in range(steps):
        mid = math.sqrt(lo_ * hi_)
        if f_ok(mid):
            lo_ = mid
        else:
            hi_ = mid
    F = math.sqrt(lo_ * hi_)
    return F, f_ok(hold_probe(F, in_domain)), f_ok(F * 1.1)


def row_lo(r, row):
    """the certified lower end of one row (S8-1, S8-2 or lemma) on an evaluation r (fresh caches)."""
    fam, cl = row[0], row[1]
    RkC = {}
    if fam == 'S8-1':
        return CM.s81_cert(r['ch'], r['prm'], *cl, RkC)[1]
    return CM.sf_pair(r['ch'], r['prm'], *cl, RkC)[1]


def calib_plants(nofire, A, N, r0):
    """the self-calibrating plants on the first piece of S8's range (SPEC sect. 10, P2's S1/D2; v1_12: route (b), r0's trial set and
    basis kept): PLANT-LEAK (eta+, eta- times F, the binding lemma row), PLANT-OVERLAP (the Davis-Kahan sin(theta) factor times F, the
    top-mode class with the smallest F), PLANT-BARS, PLANT-VAC, PLANT-U (every bar, the vacuum terms, U times F, the binding row: through
    U and the bars they move tau_B as well), PLANT-TAUB (v1_12: tau_B times F, the binding row). Each fires when F exists and the row
    holds at F/1.1 and fails at 1.1 F."""
    rows = [x for x in r0['rows'] if x[0] in ('S8-1', 'S8-2', 'lemma')]
    lem = min((x for x in rows if x[0] == 'lemma'), key=lambda x: x[2])
    bind = min(rows, key=lambda x: x[2])
    base = dict(T=r0['T'], C0=r0['C0'], vac=r0['vac'], Uh=r0['Uh'], rows=False, bases=(r0['basis'],), C0B=r0['C0B'])
    def f_leak(F):
        """v1_6: the leakage Gram Gl times F^2 on the piece's chain, so eta+, eta- and every Gram form of the lemma scale by F (v1_12: with
        route (b)'s block bound for s_perp, as the piece's setup)."""
        f2 = arb(F) * arb(F)
        chF = dict(r0['ch'], Gl=[[x * f2 for x in row] for row in r0['ch']['Gl']])
        return bool(row_lo({'ch': chF, 'prm': CM.setup(chF, r0['P2r'], r0['Uh'], r0['vac'], sblk=r0['leak']['sblk'])}, lem) > 0)
    res = calib(f_leak)
    fires(nofire, 'PLANT-LEAK N=%d' % N, res is not None and res[1] and not res[2],
          'the binding lemma row %s loses Cov_lo > 0 at the leakage Gram x F^2 (eta x F), F = %s (holds at F/1.1: %s, at 1.1 F: %s)' % (
              lem[1], ('%.4g' % res[0]) if res else 'none', res[1] if res else '-', res[2] if res else '-'))
    ch, prm, dkf = r0['ch'], r0['prm'], r0['dkf']
    best = None
    for key_ in sorted(r0['m0'], key=str):
        if r0['m0'][key_] is None:
            continue
        dL, kind = key_[1], key_[-1]
        dR = 'far' if key_[0] == 'S8-1' else key_[2]

        def f_ov(F, dL=dL, dR=dR, kind=kind):
            return CM.dk_class(ch, prm, dict(dkf, s1=(dkf['s1'] * arb(F)).upper()), dL, dR, kind)[0] is not None
        rr = calib(f_ov)
        if rr is not None and (best is None or rr[0] < best[1][0]):
            best = (key_, rr)
    fires(nofire, 'PLANT-OVERLAP N=%d' % N, best is not None and best[1][1] and not best[1][2],
          'the top-mode class %s loses its cover at sin(theta) x F, F = %s (holds at F/1.1: %s, at 1.1 F: %s)' % (
              best[0] if best else '-', ('%.4g' % best[1][0]) if best else 'none', best[1][1] if best else '-', best[1][2] if best else '-'))
    fU = None
    for nm, kw in (('PLANT-BARS', 'bars'), ('PLANT-VAC', 'vacf'), ('PLANT-U', 'uf')):
        def f_m(F, kw=kw):
            b = dict(base)
            if kw == 'uf':
                b['Uh'] = (r0['Uh'] * arb(F)).upper()
            else:
                b[kw] = F
            rr = piece_eval_RB(N, A, r0['i'], **b)
            return rr is not None and bool(row_lo(rr, bind) > 0)
        # v1_14_3: U's domain starts at the certified U_hi. Below the B chain's in-span trace route (b) has no bound
        # (tau_B = (U/lambda_0^2 - 1 - |R_B|_F^2)/2 <= 0), so U x F/1.1 with F < 1.1 leaves the evaluation's domain, and max(1, F/1.1)
        # would only re-read calib's precondition: PLANT-U checks the hold at F/1.1 when F > 1.1, else at sqrt(F) (calib's in_domain);
        # it still fires only if the binding row fails at 1.1 F
        res = calib(f_m, in_domain=(kw == 'uf'))
        if kw == 'uf':
            fU = res
        hp = ('%s = %.6g' % ('F/1.1' if (kw != 'uf' or res[0] > 1.1) else 'sqrt(F)', hold_probe(res[0], kw == 'uf'))) if res else 'F/1.1'
        fires(nofire, '%s N=%d' % (nm, N), res is not None and res[1] and not res[2],
              'the binding row %s %s loses Cov_lo > 0 at %s x F, F = %s (holds at %s: %s, at 1.1 F: %s)' % (
                  bind[0], bind[1], {'bars': 'every bar', 'vacf': 'the vacuum terms', 'uf': 'U'}[kw],
                  ('%.4g' % res[0]) if res else 'none', hp, res[1] if res else '-', res[2] if res else '-'))

    def f_tau(F):
        """v1_12_1: the whole piece (every row and top class) at tau_B times F, the piece's chains kept: the tau-sensitive rows decide
        (v1_12 calibrated on the binding row, which hardly depends on tau_B)."""
        return rows_at_tau(r0, (r0['leak']['tau'] * arb(F)).upper())
    res = calib(f_tau)
    fires(nofire, 'PLANT-TAUB N=%d' % N, res is not None and res[1] and not res[2],
          'the piece (every row and top class, %s) fails at tau_B x F, F = %s (passes at F/1.1: %s, at 1.1 F: %s)' % (
              r0['basis'], ('%.4g' % res[0]) if res else 'none', res[1] if res else '-', res[2] if res else '-'))
    # v1_14_3: route (b)'s tau gap at the binding piece, the break-even U factor and S4-U's R_CERT/U_hi, so a
    # re-certification of S4-U shows at once
    chB_ = r0['chB']
    uq = float(((r0['Uh'] / (chB_['lam0'] * chB_['lam0'])).upper()).mid())
    gap = 2.0 * float(r0['leak']['tau'].mid())
    rcu = float((CM.fr(A['s4u'][(N, 'R_CERT')]) / r0['Uh']).mid())
    ftau = res[0] if res else None
    slk = ((ftau - 1.0) * gap / uq) if ftau else float('nan')
    out('TAU-GAP N=%d piece %d %s (INFO): route (b)\'s gap U_hi/lambda_0^2 - 1 - |R_B|_F^2 = %.4e (U_hi/lambda_0^2 %.12f; tau_B = gap/2); '
        'the piece fails at tau_B x %s (PLANT-TAUB), i.e. at the break-even U factor 1 + %.3e; S4-U\'s R_CERT/U_hi %.3e (%.3g x that '
        'margin); the binding row %s %s alone at U_hi x %s (PLANT-U); U_hi from S4_U_CERTIFIED_v3 %s' % (
            N, r0['i'], r0['basis'], gap, uq, ('%.4g' % ftau) if ftau else 'none', slk, rcu, (rcu / slk) if (ftau and slk > 0) else float('nan'),
            bind[0], bind[1], ('%.4g' % fU[0]) if fU else 'none', PINS[S4UF][:8]))


def mirror_worst(r):
    """C-MIRROR: the largest relative difference of the central values of the S8-2 classes (dL, dR) and (dR, dL), m <= 8."""
    worst, wcl = 0.0, None
    for dL, dR, kind, m in TWO_CLS:
        if dL < dR and dL + dR + m + 3 >= 5 and m <= 8:
            a = CM.sf_pair(r['ch'], r['prm'], dL, dR, kind, m, r['RkC'])[0]
            b = CM.sf_pair(r['ch'], r['prm'], dR, dL, kind, m, r['RkC'])[0]
            q = abs(a - b) / max(abs(a), abs(b), 1e-300)
            if q > worst:
                worst, wcl = q, (dL, dR, kind, m)
    return worst, wcl


def ritz0(N, A):
    """C-RITZ0 (t = 0): bar-free entries, no vacuum terms, the parity-pure basis of t = 0; R's diagonal against the exact harmonic
    ratios (7 - 3 sqrt 5)/2, (3 - sqrt 5)(5 - sqrt 21)/4, (23 - 5 sqrt 21)/2 and against the trial file's lam0[1..3]; R's Gershgorin
    radii. Returns (largest relative difference to the exact ratios, to lam0, largest radius / ratio)."""
    Ech = w3_keys(A['EP'][N])   # v1_12: the W3 chain's keys, no TT
    Vm = CM.entry_points(Ech, arb(0))
    vac0 = {'delta': arb(0), 's': arb(0), 'sp': arb(0), 'eps_a': arb(0), 'Bp': arb(0)}
    ch0 = CM.chain(Vm, A['mains'][N], A['odd'][N], vac0, ritz_pure(Vm, A['odd'][N]), tt=False)
    s5, s21 = arb(5).sqrt(), arb(21).sqrt()
    ex = [(7 - 3 * s5) / 2, (3 - s5) * (5 - s21) / 4, (23 - 5 * s21) / 2]
    gd = CM.gersh(ch0['R'])
    de = max(float(abs(gd[k][0] - ex[k]).upper()) / float(ex[k].mid()) for k in range(3))
    dl = max(abs(float(gd[k][0].mid()) - A['lam0'][N][k + 1]) / A['lam0'][N][k + 1] for k in range(3))
    dg = max(float(gd[k][1]) / float(ex[k].mid()) for k in range(3))
    return de, dl, dg


def band_gates(A, N, i):
    """on piece i: C-BAND-LE, every certified free entry's band4(J_lo) at most its record's sum of Bp times (1 + 2^-30) (the review 7deeca77's
    sanity gate: each law term is at most 1 for J >= 300); C-BAND-J300, band4 at J = 300 reproducing the sum of Bp
    within 2^-30 relative (outward rounding only). Returns the failing keys of each."""
    J = Fraction(A['pieces'][N][i]['jlo'])
    tol = 1 + Fraction(1, 2 ** 30)
    le, j3 = [], []
    for k, (LO, HI, err) in sorted(A['EP'][N].items()):
        law = A['LAW'][N].get(k)
        if law is None or law['parity'] == 'zero' or err == 0:
            continue
        if band4(law, J) > err * tol:
            le.append(k)
        b3 = band4(law, Fraction(300))
        if not err <= b3 <= err * tol:
            j3.append(k)
    return le, j3


def pre_piece(fails, A, N, i):
    """one piece of the pre item in full: route (b)'s rows (C-KILL), C-UNIF, C-MV and C-MV-B, C-MV-DELTA and C-MV-MID (both chains) with
    the MV-ASIS INFO (v1_12_3), C-MV-BAR (-B), C-TARGET and C-MV-S83 (v1_13), C-MV-SF and C-TARGET-SF (v1_14), C-PAREXACT, the banded
    bars' gates and the break-even INFO. Returns the evaluation (None when there is no bound)."""
    STAGE[0] = 'C pre N=%d piece %d' % (N, i)
    r = piece_eval_RB(N, A, i)
    if r is None:
        out('PIECE %d %04d: no bound on the piece (the M2(b) law gives no s below 1, or no trial set has tau_B > 0) -> FAIL' % (N, i))
        fails.append('C-VAC')
        return None
    summ = piece_summary(r)
    pe = r['ch']['par_exact'] is True and r['chB']['par_exact'] is True
    out(piece_line(N, i, r['P2row'], summ, pe, r))
    gate(fails, 'C-KILL', not summ[1] and not summ[2] and pe)
    bu = unif_piece(N, A, i)
    out('C-UNIF N=%d piece %d (thin entry values with the coefficients at their spans\' midpoints, upper ends and lower ends, U and the '
        'M2(b) law at 9 points): failing %s -> %s' % (N, i, bu or 'none', gate(fails, 'C-UNIF', not bu)))
    nl, bm = mv_piece(N, A, i, r['C0'], r['vac'])
    out('C-MV N=%d piece %d (centered W3 chain with zero bars and delta = 0 against the thin point chains at 9 t on its dual run\'s allow '
        'and par, the wrapped allowances at their balls\' midpoints, upper ends and lower ends): %d leaves, failing %d%s -> %s' % (
        N, i, nl, len(bm), (' (%s)' % ', '.join(bm[:4])) if bm else '', gate(fails, 'C-MV', not bm)))
    nl, bm = mv_piece(N, A, i, r['C0'], r['vac'], SL=r['SL'], C0B=r['C0B'])
    out('C-MV-B N=%d piece %d (the same on route (b)\'s B chain, %s): %d leaves, failing %d%s -> %s' % (
        N, i, r['basis'], nl, len(bm), (' (%s)' % ', '.join(bm[:4])) if bm else '', gate(fails, 'C-MV-B', not bm)))
    for sfx, lab, kw in (('', 'W3', {}), ('-B', 'B ' + r['basis'], dict(SL=r['SL'], C0B=r['C0B']))):   # v1_12_3
        d = mvd_piece(N, A, i, r['C0'], r['vac'], **kw)
        out(mvd_line(fails, N, i, sfx, lab, d))
        out('MV-ASIS N=%d piece %d %s (INFO): the point chains with delta kept (%.3e) against the same centered chain: %d of %d leaves '
            'leave it beyond inside_r\'s slack; largest excess %.2e of the centered radius, %.2e of the point ball\'s own radius (arb\'s '
            'reduced precision on balls of relative width ~delta)' % (N, i, lab, d['u'], len(d['asis']), d['nl'], d['xo'], d['xp']))
    mb = mvbar_piece(N, A, r, keep=True)
    out(mvbar_line(fails, N, i, mb))   # v1_13: the bar slots
    out(target_line(fails, N, i, target_piece(N, A, r)))   # v1_13: the C1 check (the review lemma v2)
    out(s83_line(fails, N, i, s83_piece(N, A, r)))   # v1_13: S8-3's strip enclosures
    out(sf_line(fails, N, i, sf_piece(N, A, r, mb)))   # v1_14: sf_pair's class-level form
    parity_lines(fails, N, i, r)
    le, j3 = band_gates(A, N, i)
    out('C-BAND N=%d piece %d (J_lo %r): band4(J_lo) <= sum Bp (1 + 2^-30) for every certified free entry: failing %s -> %s; band4(300) '
        'reproduces sum Bp within 2^-30: failing %s -> %s' % (N, i, r['P2row']['jlo'], le or 'none',
                                                                               gate(fails, 'C-BAND-LE', not le), j3 or 'none',
                                                                               gate(fails, 'C-BAND-J300', not j3)))
    out(taub_info(N, r, A))
    return r


def run_pre_C(fails, nofire, A):
    """the pre item's stage C part, per N (v1_12: route (b); S8's range starts at A['RSTART'][N]): its first piece and piece 903 in full
    (pre_piece); PLANT-RIGHTEND, PLANT-LAW-JHI, PLANT-UNIF-SLACK, PLANT-MV, PLANT-MV-B, PLANT-MV-DELTA, PLANT-MV-DELTA-B (v1_12_3);
    C-MIRROR; C-RITZ0; the self-calibrating plants on the first piece; v1_13: PLANT-MV-BAR, PLANT-MV-S83, PLANT-TARGET and core_plants
    (PLANT-C5-G00, -T00, -DSQRT, -DDIV, PLANT-C6) on the first piece; v1_14: PLANT-MV-SF and PLANT-TARGET-SF on the first piece."""
    for N in (4, 3):
        i0 = A['RSTART'][N]
        r0 = pre_piece(fails, A, N, i0)
        pre_piece(fails, A, N, NPIECES - 1)
        if r0 is None:
            continue
        STAGE[0] = 'C pre plants N=%d' % N
        br = unif_piece(N, A, i0, right_end=True)
        fires(nofire, 'PLANT-RIGHTEND N=%d' % N, any(b.startswith('entry ') for b in br),
              'piece %d with its t-box replaced by its right end in J: C-UNIF fails on %d names' % (i0, len(br)))
        bl = unif_piece(N, A, i0, law_jhi=True)
        fires(nofire, 'PLANT-LAW-JHI N=%d' % N, any(b.startswith('law ') for b in bl),
              'piece %d with the M2(b) law taken at J_hi: C-UNIF fails on %s' % (i0, [b for b in bl if b.startswith('law ')] or 'nothing'))
        # v1_12_2: C-UNIF's slack must not hide a real excess: a point ball 2^-10 rad(outer) beyond each entry's enclosure on the
        # piece's box (its midpoint and radius 0) must fail unif_ok, for every entry
        Tq = CM.tball(A['pieces'][N][i0]['jlo'], A['pieces'][N][i0]['jhi'])
        encq = CM.entry_points(A['EP'][N], Tq)
        held = sorted(k for k, e in encq.items() if e.rad() > 0 and unif_ok(e, arb(e.upper()) + arb(e.rad()) / (1 << 10)))
        fires(nofire, 'PLANT-UNIF-SLACK N=%d' % N, not held, 'piece %d, every entry with a radius (%d): a point 2^-10 rad(outer) beyond the '
              'enclosure\'s upper end fails unif_ok; held %s' % (i0, sum(1 for e in encq.values() if e.rad() > 0), held or 'none'))
        nl, bm = mv_piece(N, A, i0, r0['C0'], r0['vac'], zero_tgrad=True)
        fires(nofire, 'PLANT-MV N=%d' % N, len(bm) > 0, 'piece %d with the t-gradients set to 0: C-MV fails on %d of %d leaves' % (
            i0, len(bm), nl))
        nl, bm = mv_piece(N, A, i0, r0['C0'], r0['vac'], zero_tgrad=True, SL=r0['SL'], C0B=r0['C0B'])
        fires(nofire, 'PLANT-MV-B N=%d' % N, len(bm) > 0, 'piece %d, B chain %s, with the t-gradients set to 0: C-MV-B fails on %d of %d '
              'leaves' % (i0, r0['basis'], len(bm), nl))
        for sfx, lab, kw in (('', 'W3 chain', {}), ('-B', 'B chain ' + r0['basis'], dict(SL=r0['SL'], C0B=r0['C0B']))):   # v1_12_3
            d = mvd_piece(N, A, i0, r0['C0'], r0['vac'], plant=True, **kw)
            fires(nofire, 'PLANT-MV-DELTA%s N=%d' % (sfx, N), all(d['endm'][m] for m in END_MODES) and d['hits'] == {1},
                  'piece %d, %s: the %d thin endpoint chains (lambda_0 = m-hat (1 +- %.3e) exactly, at 9 t) against the centered chain '
                  'computed with delta = 0: C-MV-DELTA%s fails on %s of %d leaves (wrapped allowances at their balls\' midpoints, upper '
                  'ends, lower ends; v1_12_4: every mode must fail)%s; the place-1 stand-in met %s' % (
                      i0, lab, d['nend'], d['u'], sfx, ', '.join(str(len(d['endm'][m])) for m in END_MODES), d['nl'],
                      (' (%s)' % ', '.join(sorted(d['end'])[:4])) if d['end'] else '',
                      'once in every chain' if d['hits'] == {1} else '%s times, not once' % sorted(d['hits'])))
        mw, mcl = mirror_worst(r0)
        out('C-MIRROR N=%d piece %d: the central values of S8-2 (dL, dR) and (dR, dL), m <= 8: largest relative difference %.1e%s '
            '(<= 1e-10) -> %s' % (N, i0, mw, (' at %s' % (mcl,)) if mcl else '', gate(fails, 'C-MIRROR', mw <= 1e-10)))
        de, dl, dg = ritz0(N, A)
        out('C-RITZ0 N=%d (t = 0, bar-free, no vacuum terms, parity-pure basis): R\'s diagonal against the exact harmonic ratios %.1e, '
            'against lam0[1..3] %.1e; Gershgorin radii / ratio %.1e (all <= 1e-9) -> %s' % (
                N, de, dl, dg, gate(fails, 'C-RITZ0', de <= 1e-9 and dl <= 1e-9 and dg <= 1e-9)))
        calib_plants(nofire, A, N, r0)
        # v1_13: PLANT-MV-BAR (the bar-corner thin points against the zero-bar centered chains must fail), PLANT-TARGET (eta+ scaled by
        # 1e-3 must fail the C1 check), and s8core_v1_10's C5 / C6 refusals
        db = mvbar_piece(N, A, r0, plant=True, keep=True)   # v1_14: keep, for PLANT-MV-SF
        fires(nofire, 'PLANT-MV-BAR N=%d' % N, all(db['bym', c][m] for c in ('W3', 'B') for m in (1, -1)) and db['hits'] == {1},
              'piece %d: the bar-corner thin points against the zero-bar centered chains (modes 1 and -1 must each fail on each chain): '
              'W3 fails on %d of %d leaves (by mode 0/1/-1: %s), B on %d of %d (%s)' % (
                  i0, len(db['W3'][1]), db['W3'][0], '/'.join(str(db['bym', 'W3'][m]) for m in END_MODES), len(db['B'][1]), db['B'][0],
                  '/'.join(str(db['bym', 'B'][m]) for m in END_MODES)))
        ps = s83_piece(N, A, r0, plant=True)
        fires(nofire, 'PLANT-MV-S83 N=%d' % N, all(ps[2][m] for m in (1, -1)),
              'piece %d: the thin points against the strip enclosures recomputed with zero bars (modes 1 and -1 must each fail): failing '
              'pairs %d of %d (by mode 0/1/-1: %s; gradient-sign corners G+/G-: %d/%d)' % (
                  i0, len(ps[1]), len(N4PAIRS), '/'.join(str(ps[2][m]) for m in END_MODES), ps[2]['G+'], ps[2]['G-']))
        tq = target_piece(N, A, r0, etap_scale=1e-3)
        fires(nofire, 'PLANT-TARGET N=%d' % N, 'eta+' in tq[1], 'piece %d with the box eta+ multiplied by 1e-3: C-TARGET fails on %s' % (
            i0, sorted(set(tq[1])) or 'nothing'))
        # v1_14: PLANT-MV-SF (the bar-corner thin W3 chains against sf_pair's class-level balls from the zero-bar duals, the box's C1, dz
        # and sg kept: modes 1 and -1 must each fail), PLANT-TARGET-SF (the box C1 times 1e-3 must fail C-TARGET-SF)
        pf = sf_piece(N, A, r0, db, plant=True)
        fires(nofire, 'PLANT-MV-SF N=%d' % N, pf['active'] > 0 and all(pf['bym'][m] for m in (1, -1)),
              'piece %d: the bar-corner thin W3 chains (zero-bar allowance box) against sf_pair\'s class-level balls from the zero-bar '
              'duals (modes 1 and -1 must each fail): %d of %d classes active, failing points %d of %d (by mode 0/1/-1: %s)' % (
                  i0, pf['active'], pf['classes'], len(pf['fail']), pf['points'], '/'.join(str(pf['bym'][m]) for m in END_MODES)))
        pt_ = sf_piece(N, A, r0, mvbar_piece(N, A, r0, keep=True), c1_scale=1e-3)
        fires(nofire, 'PLANT-TARGET-SF N=%d' % N, any(x.endswith(' C1') for x in pt_['tfail']),
              'piece %d with the box C1 multiplied by 1e-3: C-TARGET-SF fails on %d of %d checks (%s)' % (
                  i0, len(pt_['tfail']), pt_['tchecks'], ', '.join(sorted(set(pt_['tfail']))[:3]) or 'nothing'))
        core_plants(nofire, A, N, r0)


def run_chunk(fails, nofire, A, N, a, b):
    """pieces a .. b-1 of one N (v1_12: route (b); a chunk below S8's range start fails C-RANGE): per piece the kill rule on every row's
    certified lower end and every top-mode class with both chains exactly parity-pure, RISK lines, and C-UNIF, C-MV and C-MV-B on the
    sampled pieces (v1_12_3: with C-MV-DELTA and C-MV-MID on both chains); v1_13: C-MV-BAR (-B), C-TARGET and C-MV-S83 on the chunk's
    first piece; v1_14: C-MV-SF and C-TARGET-SF there too."""
    if a < A['RSTART'][N]:
        out('C-RANGE N=%d: the chunk [%d, %d) starts below S8\'s range, which starts at piece %d -> %s' % (
            N, a, b, A['RSTART'][N], gate(fails, 'C-RANGE', False)))
    kills, nrisk, nprint = [], 0, 0
    for i in range(a, b):
        STAGE[0] = 'C chunk N=%d piece %d' % (N, i)
        try:
            r = piece_eval_RB(N, A, i)
            why = None if r is not None else 'the M2(b) law gives no s below 1, or no trial set has tau_B > 0'
        except (ValueError, ArithmeticError) as e:   # the evaluation breaks down on this piece: no bound, so the piece fails
            r, why = None, 'the evaluation breaks down (%r)' % (e,)
        if r is None:
            out('PIECE %d %04d h81=nan h82=nan h83=nan hlem=nan m0=None risk=0 ok=0 | %s' % (N, i, why))
            out('KILL N=%d I=%04d: no bound on the piece (%s)' % (N, i, why))
            kills.append(i)
            continue
        summ = piece_summary(r)
        pe = r['ch']['par_exact'] is True and r['chB']['par_exact'] is True
        out(piece_line(N, i, r['P2row'], summ, pe, r))
        fm, bad, badtop, risk, m0max = summ
        for fam, cl, lo_ in bad:
            out('KILL N=%d I=%04d %s %s: certified lower end %s is not > 0 (route (b), every trial set tried: %s)' % (
                N, i, fam, cl, lo_str(lo_), ' '.join(b_ for b_, ok_, tb_ in r['tried'])))
        for k, v in badtop:
            out('KILL N=%d I=%04d top %s: m0 %s (no top-mode cover with m0 <= 8)' % (N, i, k, v))
        if not pe:   # v1_11; v1_12: both chains (the sector split of route (b)'s Gl needs the B chain's too)
            out('KILL N=%d I=%04d: a chain is not exactly parity-pure (W3 par_exact %r, B chain %r)' % (
                N, i, r['ch']['par_exact'], r['chB']['par_exact']))
        if bad or badtop or not pe:
            kills.append(i)
        nrisk += len(risk)
        for fam, cl, h in risk:
            if nprint < RISK_PRINT:
                out('RISK N=%d I=%04d %s %s: headroom %.4g < 2 (printed, not a stop: ADD1 sect. 1)' % (N, i, fam, cl, h))
                nprint += 1
        if i in (a, b - 1) or i % SAMPLE_EVERY == 0:
            bu = unif_piece(N, A, i)
            nl, bm = mv_piece(N, A, i, r['C0'], r['vac'])
            nl2, bm2 = mv_piece(N, A, i, r['C0'], r['vac'], SL=r['SL'], C0B=r['C0B'])
            out('C-UNIF N=%d piece %d: failing %s -> %s; C-MV: %d leaves, failing %d%s -> %s; C-MV-B (%s): %d leaves, failing %d%s -> %s' % (
                N, i, bu or 'none', gate(fails, 'C-UNIF', not bu), nl, len(bm), (' (%s)' % ', '.join(bm[:4])) if bm else '',
                gate(fails, 'C-MV', not bm), r['basis'], nl2, len(bm2), (' (%s)' % ', '.join(bm2[:4])) if bm2 else '',
                gate(fails, 'C-MV-B', not bm2)))
            for sfx, lab, kw in (('', 'W3', {}), ('-B', 'B ' + r['basis'], dict(SL=r['SL'], C0B=r['C0B']))):   # v1_12_3
                out(mvd_line(fails, N, i, sfx, lab, mvd_piece(N, A, i, r['C0'], r['vac'], **kw)))
            if i == a:   # v1_13: one bar-corner thin check and one C1 check per chunk (the review 8ca6c894 items 3 and 4)
                mb = mvbar_piece(N, A, r, keep=True)
                out(mvbar_line(fails, N, i, mb))
                out(target_line(fails, N, i, target_piece(N, A, r)))
                out(s83_line(fails, N, i, s83_piece(N, A, r)))
                out(sf_line(fails, N, i, sf_piece(N, A, r, mb)))   # v1_14
    out('C-KILL N=%d pieces [%d, %d): %d pieces fail the kill rule%s; RISK rows %d -> %s' % (
        N, a, b, len(kills), (' (%s)' % kills[:20]) if kills else '', nrisk, gate(fails, 'C-KILL', not kills)))


PIECE_RE = re.compile(r'^PIECE ([34]) ([0-9]{4}) h81=(\S+) h82=(\S+) h83=(\S+) hlem=(\S+) m0=(\S+) risk=([0-9]+) ok=([01]) \|')


def check_out(text, own, item, nab):
    """an output of this script (same sha256, same mode, the item, for a chunk its N, a, b), whose INPUTS digest equals this run's and
    whose VERDICT lines equal exactly ['VERDICT VALID']; a chunk's PIECE lines are exactly pieces a .. b-1 of its N once each, all ok.
    Returns the parsed PIECE rows; raises Refused otherwise."""
    lines = text.split('\n')
    m = re.match(r'^%s sha256 ([0-9a-f]{64}) MODE=(\S+) ITEM=(\S+)(?: N=([34]) A=([0-9]+) B=([0-9]+))? ' % re.escape(LABEL), lines[0])
    if m is None or m.group(1) != own or m.group(2) != MODE or m.group(3) != item:
        raise Refused('the first line does not name this script\'s sha256, mode %s and item %s' % (MODE, item))
    if item == 'chunk' and (m.group(4) is None or (int(m.group(4)), int(m.group(5)), int(m.group(6))) != nab):
        raise Refused('the first line does not name the chunk %s' % (nab,))
    if [ln for ln in lines if ln.startswith('INPUTS ')] != ['INPUTS %s' % (A_DIGEST[0] if own != ORIG_SELF else ORIG_DIGEST)]:
        raise Refused('the INPUTS digest differs from this run\'s')
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise Refused('the VERDICT lines are not exactly [\'VERDICT VALID\']')
    rows = [PIECE_RE.match(ln) for ln in lines if ln.startswith('PIECE ')]
    if item != 'chunk':
        return []
    if any(x is None for x in rows):
        raise Refused('a malformed PIECE line')
    got = [(int(x.group(1)), int(x.group(2))) for x in rows]
    N, a, b = nab
    if got != [(N, i) for i in range(a, b)] or any(x.group(9) != '1' for x in rows):
        raise Refused('the PIECE lines are not pieces %d .. %d of N = %d once each, all ok' % (a, b - 1, N))
    return [(int(x.group(1)), int(x.group(2)), float(x.group(3)), float(x.group(4)), float(x.group(5)), float(x.group(6)),
             x.group(7), int(x.group(8))) for x in rows]


def cover_check(ranges, n, start=0):
    """C-COVER: (complete, overlaps, gaps) of a list of [a, b) piece ranges against start .. n-1 (v1_12: S8's range starts at start); a
    piece below start in a range counts as an overlap."""
    cnt = [0] * n
    for a, b in ranges:
        for i in range(max(a, 0), min(b, n)):
            cnt[i] += 1
    return (all(cnt[i] == 1 for i in range(start, n)) and not any(cnt[:start]),
            [i for i in range(n) if cnt[i] > 1 or (i < start and cnt[i])], [i for i in range(start, n) if cnt[i] == 0])


def lo_not_lower(h, p):
    """a half piece's lower end not below the parent's (slack 2^-20 |lo|, v1_7); tuples (S8-3) componentwise."""
    if isinstance(p, tuple):
        return all(lo_not_lower(x, y) for x, y in zip(h, p) if x is not None and y is not None)
    s = (abs(p) * RSLACK).upper() if p > CM.NEGINF else arb(0)
    return bool(h >= (p - s).lower())


def piece_halves(N, A, i, collapse=False):
    """C-PIECE on piece i: each half of its t-box, with the parent's basis C0, M2(b) law, S4-U upper end and P2 row, lies inside the
    parent: every chain leaf (slack 1e-20 relative), every common row's certified lower end not below the parent's, and every m0 no
    larger. collapse: the parent's box replaced by its right end in J (PLANT-PIECE). Returns (leaves compared, failing leaves,
    failing rows). v1_12: route (b), the halves with the parent's trial set and B basis; the leaves of both chains (the W3 chain with
    Gl, and the B chain) are compared. v1_12_5: also returns the largest raw excess of a failing leaf other than Gl relative to the
    parent's radius; the leaves are INFO in the final's line, the rows, m0 and par_exact the gate (module docstring)."""
    par = piece_eval_RB(N, A, i)
    T = par['T']
    kw = dict(bases=(par['basis'],), C0B=par['C0B'])
    if collapse:
        par = piece_eval_RB(N, A, i, T=arb(T.lower()), C0=par['C0'], vac=par['vac'], Uh=par['Uh'], **kw)
    pl = dict(CM.leaves({'W3': par['ch'], 'B': par['chB']}))
    prow = {(f_, str(cl)): lo_ for f_, cl, h, lo_, ok in par['rows']}
    pm0 = par['m0']
    mid = arb(T.mid())
    bad_l, bad_r = set(), set()
    xl = 0.0
    for Th in (T.lower().union(mid), mid.union(T.upper())):
        hf = piece_eval_RB(N, A, i, T=Th, C0=par['C0'], vac=par['vac'], Uh=par['Uh'], **kw)
        if hf is None:
            bad_r.add('no bound on a half')
            continue
        for p, v in CM.leaves({'W3': hf['ch'], 'B': hf['chB']}):
            if p not in pl or not inside_r(pl[p], v, RSLACK, arb('1e-20')):
                bad_l.add(p)
                if p in pl and not p.startswith('/W3/Gl/'):
                    o = pl[p]
                    ex = max(float((v.upper() - o.upper()).mid()), float((o.lower() - v.lower()).mid()))
                    xl = max(xl, ex / float(o.rad()) if o.rad() > 0 else float('inf'))
        for f_, cl, h, lo_, ok in hf['rows']:
            pv = prow.get((f_, str(cl)))
            if pv is not None and not lo_not_lower(lo_, pv):
                bad_r.add('%s %s' % (f_, cl))
        if hf['ch']['par_exact'] is not True or hf['chB']['par_exact'] is not True:   # v1_11; v1_12 both chains
            bad_r.add('par_exact')
        for k, v in hf['m0'].items():
            if pm0[k] is not None and (v is None or v > pm0[k]):
                bad_r.add('m0 %s' % (k,))
    return len(pl), sorted(bad_l), sorted(bad_r), xl


def run_final(fails, nofire, A):
    """the final item: the pre output and the chunk outputs of this script (same sha256, mode and inputs), coverage, the per-N minima,
    C-PIECE at the binding pieces, the plants of this item, and the record."""
    STAGE[0] = 'final outputs'
    own = sha_file(os.path.abspath(__file__))
    names = sorted(os.listdir(OUTDIR))
    pat_pre = re.compile(r'^out_%s_%s_pre(_r[0-9]{1,2})?\.out$' % (re.escape(LABEL), MODE))
    pat_ch = re.compile(r'^out_%s_%s_c([34])_([0-9]{4})_([0-9]{4})(_r[0-9]{1,2})?\.out$' % (re.escape(LABEL), MODE))
    pres = []
    for nm in names:
        if pat_pre.match(nm):
            try:
                check_out(read_text(os.path.join(OUTDIR, nm)), ACC.expect(os.path.join(OUTDIR, nm), own, ORIG_SELF), 'pre', None)
                pres.append(nm)
            except Refused as e:
                out('PRE %s: not counted (%s)' % (nm, e))
    out('C-PRE: VALID pre outputs of this script %s -> %s' % (pres or 'none', gate(fails, 'C-PRE', len(pres) == 1)))
    chunks, kills = [], []
    for nm in names:
        mm = pat_ch.match(nm)
        if not mm:
            continue
        text = read_text(os.path.join(OUTDIR, nm))
        nab = (int(mm.group(1)), int(mm.group(2)), int(mm.group(3)))
        try:
            rows = check_out(text, ACC.expect(os.path.join(OUTDIR, nm), own, ORIG_SELF), 'chunk', nab)
            chunks.append((nab, nm, sha_file(os.path.join(OUTDIR, nm)), rows, text))
        except Refused as e:
            k = [ln for ln in text.split('\n') if ln.startswith('KILL ')]
            out('CHUNK %s: not counted (%s)%s' % (nm, e, ('; it holds %d KILL lines' % len(k)) if k else ''))
            if k:
                kills.append(nm)
    out('C-NOKILL: chunk outputs of this script holding KILL lines: %s -> %s' % (kills or 'none', gate(fails, 'C-NOKILL', not kills)))
    allrows = {4: [], 3: []}
    for N in (4, 3):
        rg = [(nab[1], nab[2]) for nab, nm, sh, rows, text in chunks if nab[0] == N]
        st = A['RSTART'][N]   # v1_12: S8's range at this N
        comp, ov, gp = cover_check(rg, NPIECES, st)
        if MODE == 'cert':
            out('C-COVER N=%d: %d VALID chunks over S8\'s range [%d, %d); complete %s, overlaps %d, gaps %d -> %s' % (
                N, len(rg), st, NPIECES, comp, len(ov), len(gp), gate(fails, 'C-COVER', comp and not ov)))
        else:
            out('C-COVER N=%d (mock dry run: disjoint VALID chunks inside S8\'s range [%d, %d); completeness is the certified run\'s gate): '
                '%d chunks, %d of %d pieces, overlaps %d -> %s' % (N, st, NPIECES, len(rg), NPIECES - st - len(gp), NPIECES - st, len(ov),
                                                                 gate(fails, 'C-COVER', not ov and len(rg) > 0)))
        for nab, nm, sh, rows, text in chunks:
            if nab[0] == N:
                allrows[N] += rows
    full = [(0, 300), (300, 600), (600, NPIECES)]
    c0 = cover_check(full, NPIECES)
    out('C-COVER-CTRL: a full disjoint cover passes: complete %s, overlaps %d, gaps %d -> %s' % (
        c0[0], len(c0[1]), len(c0[2]), gate(fails, 'C-COVER-CTRL', c0[0])))
    cg = cover_check([(0, 300), (301, NPIECES)], NPIECES)
    fires(nofire, 'PLANT-COVER-GAP', not cg[0] and cg[2] == [300], 'piece 300 missing: complete %s, gaps %s' % (cg[0], cg[2]))
    co = cover_check([(0, 301), (300, NPIECES)], NPIECES)
    fires(nofire, 'PLANT-COVER-OVERLAP', not co[0] and co[1] == [300], 'piece 300 twice: complete %s, overlaps %s' % (co[0], co[1]))
    if chunks:
        nab, nm, sh, rows, text = chunks[0]; text = text.replace(ORIG_SELF, own, 1).replace('INPUTS %s' % ORIG_DIGEST, 'INPUTS %s' % A_DIGEST[0], 1)   # option (C): the plants start from the regenerated form of a carried chunk
        for pname, bad in (('PLANT-CHUNK-SUFFIX', text.replace('VERDICT VALID', 'VERDICT VALID (planted)')),
                           ('PLANT-CHUNK-SHA', text.replace(own, own[::-1], 1)),
                           ('PLANT-CHUNK-INPUTS', text.replace('INPUTS %s' % A_DIGEST[0], 'INPUTS %s' % A_DIGEST[0][::-1], 1)),
                           ('PLANT-CHUNK-PIECE', '\n'.join(ln for ln in text.split('\n') if not ln.startswith('PIECE %d %04d ' % (nab[0], nab[1]))))):
            plant(nofire, pname, lambda bad=bad, nab=nab: check_out(bad, own, 'chunk', nab))
    STAGE[0] = 'final C-PIECE'
    mins = {}
    for N in (4, 3):
        if not allrows[N]:
            continue
        mins[N] = {f_: min(allrows[N], key=lambda x: x[2 + j]) for j, f_ in enumerate(FAMS4)}
        risk = sum(x[7] for x in allrows[N])
        m0s = [int(x[6]) for x in allrows[N] if x[6] != 'None']
        out('MINIMA N=%d over %d pieces: %s; largest m0 %s; RISK rows %d' % (
            N, len(allrows[N]), '; '.join('%s %.4g at piece %d' % (f_, mins[N][f_][2 + j], mins[N][f_][1]) for j, f_ in enumerate(FAMS4)),
            max(m0s) if m0s else None, risk))
        todo = sorted(set([mins[N][f_][1] for f_ in FAMS4] + [min(x[1] for x in allrows[N]), max(x[1] for x in allrows[N])]))
        for i in todo:
            nl, bl, br, xl = piece_halves(N, A, i)
            gl = [p for p in bl if p.startswith('/W3/Gl/')]
            out('C-PIECE N=%d piece %d (halves with the parent\'s basis, law, U and P2 row): failing rows, m0 or par_exact %d%s -> %s; leaves '
                '(INFO, v1_12_5): %d of %d outside the parent beyond inside_r\'s slack, %d of them route (b)\'s Gl (tau_B recomputed on each '
                'half), the others up to %.2e of the parent\'s radius' % (
                    N, i, len(br), (' (%s)' % ', '.join(br[:3])) if br else '', gate(fails, 'C-PIECE', not br), len(bl), nl, len(gl), xl))
            bu = unif_piece(N, A, i)   # v1_7: C-UNIF and C-MV at the binding pieces too (P2 checks its binding pieces)
            rb = piece_eval_RB(N, A, i)
            nl2, bm2 = mv_piece(N, A, i, rb['C0'], rb['vac'])
            nl3, bm3 = mv_piece(N, A, i, rb['C0'], rb['vac'], SL=rb['SL'], C0B=rb['C0B'])
            out('C-UNIF N=%d piece %d (binding): failing %s -> %s; C-MV: %d leaves, failing %d%s -> %s; C-MV-B (%s): %d leaves, failing %d%s '
                '-> %s' % (N, i, bu or 'none', gate(fails, 'C-UNIF', not bu), nl2, len(bm2), (' (%s)' % ', '.join(bm2[:4])) if bm2 else '',
                           gate(fails, 'C-MV', not bm2), rb['basis'], nl3, len(bm3), (' (%s)' % ', '.join(bm3[:4])) if bm3 else '',
                           gate(fails, 'C-MV-B', not bm3)))
            for sfx, lab, kw in (('', 'W3', {}), ('-B', 'B ' + rb['basis'], dict(SL=rb['SL'], C0B=rb['C0B']))):   # v1_12_3
                out(mvd_line(fails, N, i, sfx, lab, mvd_piece(N, A, i, rb['C0'], rb['vac'], **kw)))
            mbb = mvbar_piece(N, A, rb, keep=True)
            out(mvbar_line(fails, N, i, mbb))   # v1_13
            out(target_line(fails, N, i, target_piece(N, A, rb)))
            out(s83_line(fails, N, i, s83_piece(N, A, rb)))
            out(sf_line(fails, N, i, sf_piece(N, A, rb, mbb)))   # v1_14
            parity_lines(fails, N, i, rb)
            out(taub_info(N, rb, A))
        tu = TAUBU.get(N, [])   # v1_14_3: the smallest break-even U factor over this item's binding pieces
        if tu:
            w_ = min(tu, key=lambda x: x[1])
            out('TAUB-U MIN N=%d (INFO, over the %d binding pieces with a break-even): the smallest break-even U factor 1 + %.3e at piece '
                '%d, where S4-U\'s R_CERT/U_hi is %.3e (%.3g x that margin); U_hi from S4_U_CERTIFIED_v3 %s' % (
                    N, len(tu), w_[1] - 1.0, w_[0], w_[2], (w_[2] / (w_[1] - 1.0)) if w_[1] > 1.0 else float('nan'), PINS[S4UF][:8]))
        else:
            out('TAUB-U MIN N=%d (INFO): no binding piece with a break-even inside (1e-8, 0.1)' % N)
    if mins:
        N0 = 4 if 4 in mins else 3
        i0 = mins[N0]['S8-2'][1]
        nl, bl, br, xl = piece_halves(N0, A, i0, collapse=True)
        fires(nofire, 'PLANT-PIECE', len(br) > 0, 'N=%d piece %d with the parent\'s box collapsed to its right end in J: C-PIECE fails on %d '
              'rows (v1_12_5: the gate; and on %d leaves, INFO)' % (N0, i0, len(br), len(bl)))
    return chunks, pres, mins


def write_record_C(fails, nofire, A, chunks, pres, mins):
    """the S8 record of the final item: MOCK in mock mode; in cert mode S8_CERT_RECORD_v1, written only through kv_write with every
    input tag CERTIFIED and CERT_OK, which is set here only when no gate failed, every plant fired and both N are covered."""
    STAGE[0] = 'final record'
    rows = [('CODE', '%s:%s' % (LABEL, sha_file(os.path.abspath(__file__)))), ('CORE', '%s:%s' % (os.path.basename(CORE), PINS[CORE]))]
    for N in (4, 3):
        if N not in mins:
            continue
        for j, f_ in enumerate(FAMS4):
            key = {'S8-1': 'S8_1', 'S8-2': 'S8_2', 'S8-3': 'S8_3', 'lemma': 'LEMMA'}[f_]
            rows.append(('N%d_%s_MIN_HEADROOM' % (N, key), '%.6g' % mins[N][f_][2 + j]))
            rows.append(('N%d_%s_BINDING_PIECE' % (N, key), str(mins[N][f_][1])))
    for k, (nab, nm, sh, r_, t_) in enumerate(chunks):
        rows.append(('CHUNK_%02d' % k, '%s:%s' % (nm, sh)))
    for k, nm in enumerate(pres):
        rows.append(('PRE_%d' % k, '%s:%s' % (nm, sha_file(os.path.join(OUTDIR, nm)))))
    for k, (p, (sh, st)) in enumerate(sorted(TAGS.items())):
        rows.append(('INPUT_%02d' % k, '%s:%s:%s' % (os.path.relpath(p, CODEDIR), sh, st)))
    for k, p in enumerate(sorted(REFS)):
        rows.append(('REFERENCE_%d' % k, '%s:%s' % (os.path.relpath(p, CODEDIR), PINS[p])))
    tags = [(p, sh, st) for p, (sh, st) in TAGS.items()]
    chdr = {'FORMAT': 'S4U_KV_v1', 'RECORD': 'S8_CERT_RECORD_v1', 'EXPORT_STATUS': 'CERTIFIED', 'TAG': 'S8 certified by %s' % LABEL,
            'CLAIM': S8CLAIM}

    def certout():   # v1_8: in both modes, before CERT_OK could be set
        try:
            kv_write(REC_PATH + '.planted', 'S8_CERT_RECORD_v1', chdr, rows, True, tags)
        except ValueError as e:
            raise Refused(str(e))
    plant(nofire, 'PLANT-CERTOUT', certout)
    out('PLANT-CERTOUT file check: the refused write left no file -> %s' % gate(fails, 'C-CERTOUT-NOFILE',
                                                                                not os.path.exists(REC_PATH + '.planted')))
    okt = not cert_tags_ok([(p, sh, 'MOCK') for p, sh, st in tags]) and cert_tags_ok([(p, sh, 'CERTIFIED') for p, sh, st in tags])
    fires(nofire, 'PLANT-TAGS', okt, 'the tag check refuses this run\'s tag list relabelled MOCK and accepts it relabelled CERTIFIED')
    if MODE == 'mock':
        hdr = {'FORMAT': 'S4U_KV_v1', 'RECORD': 'S8_CERT_RECORD_v1_MOCK', 'EXPORT_STATUS': 'MOCK',
               'TAG': 'MOCK stage C of kt_s8_cert: the pieces in J on MOCK records (a dry run on the chunks listed); no claim',
               'CLAIM': 'MOCK nothing is claimed; this record tests the chunked run, the final item and the writer'}
        try:
            read_s8(kv_render(kv_note('S8_CERT_RECORD_v1_MOCK', False), 'S8_CERT_RECORD_v1_MOCK', hdr, rows), 'MOCK')
            okp = True
        except Refused:
            okp = False
        out('C-SELF-PRE: the S8 record reader accepts the MOCK record text in memory, before the write -> %s' % gate(fails, 'C-SELF-PRE', okp))
        rsha = kv_write(REC_PATH, 'S8_CERT_RECORD_v1_MOCK', hdr, rows, False, tags)
        rtext = read_text(REC_PATH)
        d = kv(rtext, 'S8 record')
        okn = all('CERTIFIED' not in d.get(k, '').upper() for k in STATUS_KEYS) and d.get('EXPORT_STATUS') == 'MOCK'
        out('C-NOCERT: %s %s, status keys MOCK, none naming CERTIFIED -> %s' % (os.path.basename(REC_PATH), rsha[:8], gate(fails, 'C-NOCERT', okn)))
        try:
            read_s8(rtext, 'MOCK')
            oks = True
        except Refused:
            oks = False
        out('C-SELF: the S8 record reader accepts the MOCK record in MOCK mode -> %s' % gate(fails, 'C-SELF', oks))
        plant(nofire, 'PLANT-SELF-CERT', lambda: read_s8(rtext, 'CERTIFIED'))
        return
    ctext = kv_render(kv_note('S8_CERT_RECORD_v1', True), 'S8_CERT_RECORD_v1', chdr, rows)
    try:   # v1_8: the certified record is checked in memory, so CERT_OK never precedes a check of the record itself
        read_s8(ctext, 'CERTIFIED')
        okp = True
    except Refused:
        okp = False
    out('C-SELF-PRE: the S8 record reader accepts the certified record text in memory, before any write -> %s' % gate(fails, 'C-SELF-PRE', okp))
    plant(nofire, 'PLANT-SELF-PRE-MOCK', lambda: read_s8(ctext.replace('EXPORT_STATUS = CERTIFIED', 'EXPORT_STATUS = MOCK', 1), 'CERTIFIED'))
    covered = all(N in mins for N in (4, 3))
    if not fails and not nofire and covered and cert_tags_ok(tags):
        CERT_OK[0] = True
    out('CERT_OK %s (gates failed %d, plants not fired %d, both N covered %s, every input CERTIFIED %s)' % (
        CERT_OK[0], len(fails), len(nofire), covered, cert_tags_ok(tags)))
    if CERT_OK[0]:
        rsha = kv_write(REC_PATH, 'S8_CERT_RECORD_v1', chdr, rows, True, tags)
        rtext = read_text(REC_PATH)
        try:
            read_s8(rtext, 'CERTIFIED')
            oks = True
        except Refused:
            oks = False
        out('RECORD %s %s' % (os.path.basename(REC_PATH), rsha))
        out('C-SELF: the S8 record reader accepts the certified record -> %s' % gate(fails, 'C-SELF', oks))


def main():
    fails, nofire = [], []
    complete = False
    try:
        if ITEM == 'pre':
            A = run_A(fails, nofire, plants=True)
            run_pre_C(fails, nofire, A)   # v1_12: no stage B (C-REPF was the W3 TT route's)
        elif ITEM == 'chunk':
            A = run_A(fails, nofire, plants=False)
            run_chunk(fails, nofire, A, CHUNK[0], CHUNK[1], CHUNK[2])
        else:
            A = run_A(fails, nofire, plants=False)
            chunks, pres, mins = run_final(fails, nofire, A)
            if not prec_ok(ctx.prec, PREC_LOG):   # v1_14_2: no record from a run whose precision moved
                raise Refused('C-PREC before the record: ctx.prec %d (the run\'s %d), module loads that changed it: %s' % (
                    ctx.prec, PREC, PREC_LOG or 'none'))
            write_record_C(fails, nofire, A, chunks, pres, mins)
        if ITEM == 'pre':   # v1_14_2: PLANT-PREC, C-PREC's predicate refuses a moved precision and a logged change
            fires(nofire, 'PLANT-PREC', not prec_ok(512, []) and not prec_ok(PREC, [('a module', PREC, 512)]),
                  'C-PREC\'s predicate on ctx.prec 512, and on %d with one logged module change' % PREC)
        complete = True
    except Refused as e:
        out('REFUSED in stage %s at cpu %.1f s: %s' % (STAGE[0], cpu(), e))
        fails.append('REFUSED')
    except Exception as e:
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        for ln in traceback.format_exc().splitlines()[-14:]:
            out('TRACE ' + ln)
        out('VERDICT INVALID (ERROR)')
        return 1
    out('C-PREC: flint ctx.prec %d at the end of the item (the run\'s %d, set at the start; module loads that changed it: %s) -> %s' % (
        ctx.prec, PREC, PREC_LOG or 'none', gate(fails, 'C-PREC', prec_ok(ctx.prec, PREC_LOG))))   # v1_14_2
    why = fails + ['%s did not fire' % x for x in nofire] + ([] if complete else ['INCOMPLETE'])
    out('ITEM %s %s cpu %.1f s, peak resident memory %.0f MiB' % (MODE, ITEM, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(sorted(set(why)))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
