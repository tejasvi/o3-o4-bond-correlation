#!/usr/bin/env python3
"""m3_lawcert_c3k_v2.py -- pk22 (code/pk22/m3/). m3_lawcert_c3k_v1.py (sha256 8b96d81a; the review 6797a258 clear)
retargeted to runner c3k_2's records E4D and E4N on state 10' (the P0_LOG rows 4578 and 4582; pk25/D2_DESIGN_v1_2.md sect. (a)-(b)),
made by pk22/m3/make_m3_lawcert_c3k_v2.py. What changes, and nothing else:
- RUNF = c3k_2 (d027f2d4), the list C3K_ENTRY_LIST_v1_2.json, the trial set z9symxyp (state 10' = s1 s3', S33' = -S13/2 exactly), the run
  manifest midrow/e4/MANIFEST_E4_C3K2_v1.sha256 (e7a1cd17), the records m3_c3kp_<F>_N<N>_J300_c3kp.json against m3_run_v1_9_3_asm.<N>_c3k2.out,
  the certificate out/m3_lawcert_c3k_v2_N<N>.json and the banner m3_lawcert_c3k_v2.
- The preps are c3k_1's (c76745bc), reused by c3k_2: PRODF names c3k_1 for E4D and E4N, so C-PRODUCER compares each record's prep16
  prep_script with c3k_1's pin, C-PINS asks the runner's INPUTS for the list and c3k_1, and C-PREP16 (c) reads both runners (RUN_PRODUCERS);
  the PREP16 plants act on c3k_1's text (PRUN).
- C-NO-RESUME reads the runner's own items F4Da, F4Na1..F4Na4, F4Dk<k>, F4Nk<k>, F4Nr1, F4Nr2 (EPFX: F4D for E4D, F4N for E4N; ITEM_RE_WANT the
  runner's); the PIECE-START line may end '; hand-off <name> sha256 <hex>' (the review's optional note in 40abbd62), and a piece that resumes
  from an earlier valid piece must name exactly that piece's hand-off and its sha256, a row of the run manifest; a piece with no earlier valid
  piece names none (check 'start-hand'); PLANT-NO-RESUME gains a sixth plant, a PIECE-START naming a wrong sha256.
The other gates, plants, pins texts and the claim are v1's.
---- m3_lawcert_c3k_v1.py's docstring:
m3_lawcert_c3k_v1.py -- pk22 (code/pk22/m3/). m3_lawcert_c3h_v1_1.py (sha256 554fa9d3; the v1_9 delta check d7074f53:
clear) retargeted to pk22's c3k_1 records E4D and E4N (H-CONN E4: Gxh,10,b on [vac, vac], IhL,10,b and IhR,10,b on [vac, int, vac], with the
mirror controls; runner m3_run_v1_9_3_px22_c3k_1 c76745bc, asm.N; the P0_LOG row 4535: E4 in the factored c(0) + t c_1 form for pk25's C13),
made by pk22/m3/make_m3_lawcert_c3k_v1.py. What changes, and nothing else:
- FAMS = (E4D, E4N), RUNF = c3k_1, the list C3K_ENTRY_LIST_v1_1.json, the run manifest midrow/e4/MANIFEST_E4_C3K_v1.sha256 (fe67843b), the
  records m3_c3k_<F>_N<N>_J300_c3k.json against m3_run_v1_9_3_asm.<N>_c3k.out. Each family ran on its own prep, made by the runner itself
  (PREPOF E4D, E4N; PRODF the runner, so C-PINS asks the runner's INPUTS for the list only and C-PREP16 (c) reads the runner alone); FAMREF
  P16E4D, P16E4N; PREPREF the twin pieces m3ref_px22_v1_7_P16E4D.<N>.p1 and P16E4N.<N>.p2 on z9symxy.
- The trial set is z9symxy (pk22/midrow/psixy: states 0..9 z9sym's, state 10 psi_xy): C-LAWFIELDS loads it from PSX, INPUTS pins it, and
  PIN_NAMES gains PSX (the runner's INPUTS keys use it). Every pin is the runner's own.
- C-NO-RESUME review, adapted to multi-piece chains: the runner's only resume items are E4Nr1 and E4Nr2 (ITEM_RE and RESUME_FAMS
  exactly the runner's), C-RESUME's checks, whose hand-offs hold no entry; the records' entries come from entry pieces only (walk_reads, as v1);
  and per family the chain k1..k_last is whole: the asm's piece lines cover entries 0..m-1 contiguously in k order with the cover line; every
  piece output names the runner's sha256, starts where the previous non-capped piece stopped, with exactly the units it carried and the count
  of capped pieces just before; a capped piece ends VERDICT INCOMPLETE (CAP-STOP) with a CAP-STOP line and has no hand-off; every other piece
  ends VERDICT VALID, its C-PIECE line equals the asm's, and it names its hand-off by sha256; outputs and hand-offs are rows of the run
  manifest; no piece output follows the last. Plants: a resume read in walk_pieces, a second resume family, a store into res in run_asm, a gap in
  the asm's piece lines, restored units that differ from the previous piece's carry.
- The certificate is out/m3_lawcert_c3k_v1_N<N>.json and the banner names m3_lawcert_c3k_v1 (the consumers' reader fork v1_2 adds this
  producer, with the records E4D and E4N). The other gates, plants, the pins texts and the claim are v1_1's.
---- m3_lawcert_c3h_v1_1.py's docstring:
m3_lawcert_c3h_v1_1.py -- pk22 (code/pk22/m3/). m3_lawcert_c3h_v1.py (sha256 89725eca
) with c3h's third record H4TH added (the P0_LOG row 4485: MR_EXACT's h0 rows need H4TH's certified J-laws), made by
pk22/m3/make_m3_lawcert_c3h_v1_1.py with exact replacements of asserted counts. What changes, and nothing else:
- FAMS = (CE3H, CS4H, H4TH). H4TH's nine entries (hH,b, hH1,b, h0,b; b = 0, 1, 3) ran in the same runner c3h_1, as the one piece H4THk1 of
  each N, on the shared H prep that pk03's runner m3_run_v1_9_3.py (57991eb0) produced (c3h_1's PREPOF H4TH: H), whose radii came from
  pk03's float twin P16H (m3ref_v1_14_P16H.<N>.p6_z9sym.out): PREPOF, FAMREF and PREPREF gain those entries, as the runner's own.
- PRODF holds (folder, file) pairs, since H4TH's prep producer lives in pk03's folder: C-PRODUCER compares each record's prep16
  prep_script with the pin of its pair; C-PINS asks the runner's INPUTS for all three producers (pk03's runner sits there in c3h_1, not
  in OWNMOD, so the OWNMOD comparison leaves the producers out); C-PREP16 (c) reads the runner and all three producers (RUN_PRODUCERS as
  pairs). PINS_STATIC pins m3_run_v1_9_3.py, and INPUTS the two P16H outputs, with the runner's full sha256s.
- The certificate is out/m3_lawcert_c3h_v1_1_N<N>.json and the banner names m3_lawcert_c3h_v1_1 (the consumers' reader fork v1_1 adds this
  producer, with the records CE3H, CS4H and H4TH). The gates, plants, pins texts and claim are v1's.
---- m3_lawcert_c3h_v1.py's docstring:
m3_lawcert_c3h_v1.py -- pk22 (code/pk22/m3/). A PORT of pk25/m3/m3_lawcert_s9h_v1_1.py (sha256 c43084befcb99ccfc5db3f875f3ece99fc6c00b7fcf941ec9c61c692b7bae7fc) to pk22's c3h
records CE3H and CS4H (runner m3_run_v1_9_3_px22_c3h_1, asm.N; bar m3_bar_v11; the P0_LOG row 4376: one combined m3_lawcert fork), made by
pk22/m3/make_m3_lawcert_c3h_v1.py with exact replacements of asserted counts (pk22/m3/diff_m3_lawcert_s9h_v1_1_to_c3h_v1.txt). The
gates are pk25's, retargeted; what differs in substance is where the records' prep stages come from. The entry pieces ran Prep.bound on a
class Prep restored from the scalars of a shared D16 prep: CE3H on c3_1's CE3 prep, CS4H on c1's S4 prep, both computed by m3_bar_v11's
Prep16.stage_u16 and stage_c16 in their prep pieces. So pk25's C-PREP-CLASS (no Prep16 anywhere) cannot hold, and C-PREP16 takes its place.
- C-HASH: PINS_STATIC (the pk03 modules with m3_bar_v11 and m3_reader_v6_3, the runner c3h_1, the prep producers c1 and c3_1, this
  port's pins module m3_lawcert_c3h_v1_pins, the C3-h list and the run manifest MANIFEST_G4C_C3H_v1) and INPUTS (trial sets, vacres, m2, the
  PREPJSON references P16CE3 and P16S4 whose radii the preps took).
- C-PINS: the runner's own pin tables (OWNMOD, and INPUTS evaluated from its module-level assignments) hold every pin of this script that
  the run read (the modules, the inputs, the list and both producers) with the same full sha256; the asm output's first line names the
  runner's full sha256. Plants: the asm line against a changed sha256; the runner's bar pin changed.
- C-BIND: the records m3_c3h_<F>_N<N>_J300_c3h.json (F in CE3H, CS4H) through m3_reader_v6_3.load bound to m3_run_v1_9_3_asm.<N>_c3h_1.out;
  the run manifest lists the asm output and the records with these sha256s; each record holds exactly the C3-h list's keys of its graph,
  every one free. C-PRODUCER: each record's engine names the runner (key m3_run_v1_9_3) and m3_bar_v11, and its prep16 names the prep
  family (CE3, S4) and the producer's sha256 (c3_1, c1).
- C-LAW-REM: pk25's interpreter over m3_bar_v11's Prep.bound, stage_u and stage_c (self_assigns on class Prep, as pk25's).
- C-PREP16 (new): (a) the rewrite R (class R16) of Prep16.stage_u16 and stage_c16 into Prep's terms (norm16(lab, which, p, thunk) ->
  norm_any(body, which, p, lab); N2(lab, thunk) -> N2(body, lab); self.h(k) -> hk; self.h2sq() -> h2sq; self.hh16() -> hh) gives exactly
  Prep.stage_u's and Prep.stage_c's statements, in order, once the pinned setup, N2 and cleanup statements are left out; so every stage
  result Prep16 hands off is the arithmetic of Prep's stage text, which C-LAW-REM audits; (b) every stage result (Prep.UK, Prep.CK and the
  tree) is assigned in exactly Prep.stage_x and Prep16.stage_x16 over every class and module function of the bar, and self.h2, self.hh and
  self.t only in Prep.__init__; (c) in the runner and both producers, BAR.Prep16 and BAR.Prep are called once each, in make_prep, with
  stages=(), no other attribute named Prep or Prep16 is used, stage_u16 and stage_c16 are called once each and scalars_out only in
  run_prep16, nothing calls stage_u or stage_c, and the only stores into the bar module are BAR.ARB['kern'] and BAR.FALLBACKS[:] (the review
  N-2 on C-PREP-CLASS). Prep16.lazy, h, hh16, h2sq and norm16 are pinned texts in C-LAW-SHAPE. Plants: R(stage_u16) with T(3) in 't4|H4|';
  stage_c16's nC8 without t; 'hh p8' at p 6; self.rE assigned in Prep16.h2sq; a producer's Prep16 call with stages ('u', 'c'); a store
  BAR.Prep16.stage_c16 = BAR.Prep.stage_c; a call of pr.stage_u.
- C-PREP-BAR: pk25's gate hardened by the N-1, for class Prep (no bases)
  and class Prep16 (base Prep): no attribute named Prep or Prep16 and no star import; the names used only as a class base or as the function
  of a call <name>.<method>(...); DUNDER adds __code__, __defaults__, __kwdefaults__, __func__, __globals__ and __wrapped__; setattr and
  delattr only inside a method of the two classes, on that method's first parameter. pk25's six plants and six more: a self-import
  rebinding, a star import, a method's code replaced, setattr on self outside the classes, Prep16 rebound, a second base of Prep16.
- C-LAW-SHAPE: pk25's shapes on the pins of m3_lawcert_c3h_v1_pins (v1_1's 45 texts, unchanged, at m3_bar_v11's and c3h_1's lines) and the
  new texts: Prep16.lazy, h, hh16, h2sq, norm16 and the setup, N2 and cleanup statements C-PREP16 leaves out.
- C-NO-RESUME (adapted): the runner has the resume items CS4Hr1 and CS4Hr2 (RESUME_FAMS ('CS4H',)), C-RESUME's checks, whose
  hand-offs hold no entry. The gate takes ITEM_RE and RESUME_FAMS as exactly those, and adds that the records' entries come from entry
  pieces only: walk_pieces reads only '<f>k<piece>' hand-offs, and run_asm fills res only through walk_pieces (no store, method or other
  call on res in run_asm and rep_checks). Then, per family, pk25's checks: the one piece <f>k1 from entry 0 after 0 capped pieces with no
  unit restored, VALID, its hand-off by sha256, no later piece, and the output and hand-off rows of the run manifest. Plants: a resume read in
  walk_pieces, a second resume family, a store into res in run_asm, a second asm piece line, a piece start with restored units.
- C-LAWFIELDS: the C3-h list's graphs (columns and pairs), the runner's factors (m3_entries_v3.factor on the column names 'N', as its
  EDGES), the PREPJSON whose radii each prep took (PREPREF); C-MONO-FAR and C-BAND as pk25's.
- C-LAWCERT-RT: the certificate m3_lawcert_c3h_v1_N<N>.json through m3_reader_v6_3's _bound and _parse_lawcert against the two records,
  pk25's plants on CS4H; the producer pin is the consumers' reader fork's (m3_reader_c3h_v1, made after this file is frozen).
- Items: 4, 3 and static (C-HASH on the static pins, C-LAW-REM, C-PREP16, C-PREP-BAR, C-LAW-SHAPE; no records, no certificate).
Run (under the core-h guard): D=/mnt/g2/release/root/code/pk22; OMP_NUM_THREADS=1 TMPDIR=$D/m3/tmp timeout 580 nice -n 10
  prlimit --as=8589934592 -- python3 -I -B $D/m3/m3_lawcert_c3h_v1.py ITEM LIM > $D/m3/out/m3_lawcert_c3h_v1_ITEM.out
m3_lawcert_s9h_v1_1's docstring follows.
m3_lawcert_s9h_v1_1.py -- pk25 (code/pk25/m3/). REVISION of m3_lawcert_s9h_v1.py (sha256 87e5032a26c629b2b0c08503b5d368e79fa26ee157781d94eb4c682b751649e8) for the review's
port review, made by
pk25/m3/make_m3_lawcert_s9h_v1_1.py with exact replacements of asserted counts. What changes, and nothing else
(pk25/m3/diff_m3_lawcert_s9h_v1_to_v1_1.txt):
- C-PREP-BAR (N-1; every item, static included): C-PREP-CLASS's bar-side premises as a gate on m3_bar_v16_1's text. Class Prep is defined
  once, at module level, with no bases, keywords or decorators; nothing else binds or deletes the name Prep; every use of the name reads one
  of its attributes or is a class's base; no attribute of Prep is assigned or deleted; every setattr or delattr call acts on the plain name
  self; and the text uses no other reflection. Plants (PLANT-PREP-BAR, each must be refused): Prep = Prep16 at module level, an attribute of
  Prep assigned, setattr on Prep, a base for class Prep, globals() rebinding Prep, an alias of Prep.
- C-NO-RESUME (N-2; items 4 and 3): no checkpoint state seeded the group cache of the records. The runner admits no resume item (its ITEM_RE
  is the grammar of smoke, entry-piece and asm items, and RESUME_FAMS is empty), and each family of the N ran as the one piece <f>k1, which
  started at entry 0 after 0 capped pieces with no unit restored, ended VALID with its hand-off, and had no later piece. The piece outputs and
  hand-offs are the frozen production files listed in pk25/MANIFEST_S9H_PROD_v1.sha256 (53 rows, pinned by its sha256). Plants
  (PLANT-NO-RESUME, each must be refused): a resume alternative in ITEM_RE, a non-empty RESUME_FAMS, a second piece among the asm's piece
  lines, a piece start with restored units.
- names: the header line, the usage line and the certificate m3_lawcert_s9h_v1_1_N<N>.json.
N-3 (the consumers' reader fork runs loads_lawcert's full checks, the producer pin included, and gets its own review) belongs to the reader fork.
Run (under the core-h guard): D=/mnt/g2/release/root/code/pk25; OMP_NUM_THREADS=1 TMPDIR=$D/tmp timeout 580 nice -n 10
  prlimit --as=8589934592 -- python3 -I -B $D/m3/m3_lawcert_s9h_v1_1.py ITEM LIM > $D/m3/out/m3_lawcert_s9h_v1_1_ITEM.out
m3_lawcert_s9h_v1's docstring follows.
m3_lawcert_s9h_v1.py -- pk25 (code/pk25/m3/). A PORT of pk03/m3_lawcert_v1_2.py (sha256 79ff6ca2e350cf8b033427633b29e907a64e8d7b04599b5b44299afde3d6d63a) to the S9H records
(pk25's m3_run_s9h_v1_1 on m3_bar_v16_1; G5_PLAN_v1_ADD1_1 sect. 8 C3; the row 4146), made by pk25/m3/make_m3_lawcert_s9h_v1.py with exact
replacements of asserted counts. The gates are v1_2's, retargeted:
- C-HASH: PINS_STATIC (the pk03 modules, m3_bar_v16_1, m3_reader_v6_3, the prep producer m3_run_v1_10_4, the S9H runner, this port's pins
  module m3_lawcert_s9h_v1_pins, the S9H list and the run manifest) and INPUTS (trial set, vacres, m2, the V3N/V3D references).
- C-PINS: pk25/m3/MANIFEST_m3_run_s9h_v1_1.sha256 lists every pin of the run with this script's sha256; the asm output's first line names
  m3_run_s9h_v1_1's sha256.
- C-BIND: the three records m3_s9h_<G>_N<N>_J300_v1.json (G in NIH, NHT, DH) through m3_reader_v6_3.load bound to the asm output; the side
  manifest MANIFEST_m3_run_s9h_v1_1_asm.N.sha256 names exactly the asm output and the records; each record holds exactly the S9H list's keys
  of its graph, every one free. C-PRODUCER: each record's engine names m3_run_s9h_v1_1, its parent m3_run_v1_10_4 and m3_bar_v16_1.
- C-LAW-REM: the t-valuation interpreter over m3_bar_v16_1's Prep.bound, stage_u and stage_c; self_assigns looks at class Prep only, since
  m3_bar_v16_1's subclass Prep16 assigns the same stage results. C-PREP-CLASS (new) backs that: the S9H runner and its prep producer build
  BAR.Prep in make_prep and never name Prep16 (PLANT-PREP-CLASS: make_prep calling BAR.Prep16 must be refused).
- C-LAW-SHAPE: the pinned texts of m3_lawcert_s9h_v1_pins (43 of v1_1's texts unchanged, the new group-norm closure gn and the runner's law
  statements) as ASTs in their places; the alpha_lo plant changes the text inside Prep.stage_c only (Prep16.stage_c16 holds a copy).
- C-LAWFIELDS: the S9H list's graphs (columns and pairs, as the runner's family_graph), the runner's own enc_of (executed from its source),
  the PREPJSON of the record's prep family (V3N for NIH and NHT, V3D for DH); C-MONO-FAR and C-BAND as v1_2.
- C-LAWCERT-RT: the certificate m3_lawcert_s9h_v1_N<N>.json through m3_reader_v6_3's _bound and _parse_lawcert against the three loaded
  records, with v1_2's plants (on DH); the producer pin is the consumers' reader fork's, made after this file is frozen.
- Items: 4, 3 (everything, after the S9H production and asm) and static (C-HASH on PINS_STATIC, C-LAW-REM, C-PREP-CLASS, C-LAW-SHAPE; no
  records, no certificate), so that the bar port is checked before production.
Run (under the core-h guard): D=/mnt/g2/release/root/code/pk25; OMP_NUM_THREADS=1 TMPDIR=$D/tmp timeout 580 nice -n 10
  prlimit --as=8589934592 -- python3 -I -B $D/m3/m3_lawcert_s9h_v1.py ITEM LIM > $D/m3/out/m3_lawcert_s9h_v1_ITEM.out
v1_2's docstring follows.
m3_lawcert_v1_2.py -- pk03 (code/pk03/). REVISION of m3_lawcert_v1_1.py (acdff41a) for the N record on
route B's scope (m3_run_v1_8_2, item asmN; option 3): the same gates over the one family N. What changes:
- The record is m3_s8v3_N_N<N>_J300_v1_8_2.json, bound to out/m3_run_v1_8_2_asmN.N.out (m3_reader_v6.load) and to
  MANIFEST_m3_run_v1_8_2_asmN.N; C-PINS reads MANIFEST_m3_run_v1_8_2 and requires the asmN output's first line to name
  m3_run_v1_8_2's full sha256; C-PRODUCER requires the record's engine to name m3_run_v1_8_2 (entries_by m3_run_v1_8, bar v10).
- C-BIND compares the record's entries with route B's scope, not the full N family: every T,a,b of S8_ENTRY_LIST_v3's N graph and
  the TX,a,b with max(a, b) <= 3, with the list's parity, and the record's extra scope_keys must equal that scope, sorted.
- C-LAWFIELDS builds the N graph from all the list's N entries (as the run did) and recomputes the laws of the record's entries
  only.
- The certificate is out/m3_lawcert_v1_2_N<N>.json; m3_reader_v6_2 adds this producer to the allow-list. C-LAWCERT-RT's
  changed-record-sha and added-entry plants use N, and the records-map plant drops the N record, the only one.
Everything else is m3_lawcert_v1_1's (pins m3_lawcert_v1_1_pins b469dd2e). Its docstring follows.
m3_lawcert_v1_1: REVISION of m3_lawcert_v1.py (3c75316a) for the partial
asm's records (m3_run_v1_8_1 32bed253, item asmP): the same gates over the four families D, E2, E3 and FF.
What changes:
- The records are m3_s8v3_<D|E2|E3|FF>_N<N>_J300_v1_8_1.json, bound to out/m3_run_v1_8_1_asmP.N.out (m3_reader_v6.load) and to
  MANIFEST_m3_run_v1_8_1_asmP.N. C-PINS reads MANIFEST_m3_run_v1_8_1 (25f24fed), which lists m3_run_v1_8_1, m3_run_v1_8 and the
  modules, and requires the asmP output's first line to name m3_run_v1_8_1's full sha256.
- C-PRODUCER (new): every record's engine names m3_run_v1_8_1, entries_by m3_run_v1_8 and m3_bar_v10, each with its full sha256,
  so the entries come from the bar that C-LAW-REM and C-LAW-SHAPE audit.
- The pins module is m3_lawcert_v1_1_pins (b469dd2e): v1's 43 texts plus bar v10 l.249-250 (t and the tilt rates,
  The review 7327a692), which C-LAW-SHAPE checks beside l.251-253 as before.
- TVal's docstring states the basis of the fixed J_REF values in the words (03674489 l.40-41).
- The certificate is out/m3_lawcert_v1_1_N<N>.json (FORMAT M3_LAWCERT_v1, the same claim); m3_reader_v6_1 tells the producers
  apart by the job output's first line. C-LAWCERT-RT's changed-record-sha and added-entry plants use D, since there is no N record.
Everything else is m3_lawcert_v1's. Its docstring follows.
m3_lawcert_v1: Certified J-laws for M3's S8 records without a rerun (PLAN_M3_LAWCERT_v1 255a9d70;
the AST gate's conditions 1-5 with two additions, banded
<= uniform err as a sanity gate and arb chi-square tails rounded outward). One item per N. It reads the five m3_run_v1_8 records of that
N, checks their binding and the producer's pins, checks the bar's term structure on the exact pinned files, recomputes every law
parameter, and after every gate and plant writes out/m3_lawcert_v1_N<N>.json (FORMAT M3_LAWCERT_v1, read by m3_reader_v6.load_lawcert)
with a per-entry LAW_CLAIM, named on a RECORD line. No entry is recomputed.
  C-HASH        every pinned file has its full sha256: this folder's modules, m3_run_v1_8 and its manifest, m3_reader_v6, the pins
                module m3_lawcert_v1_pins (exact source texts) and the run's inputs (PLANT-HASH).
  C-PINS        MANIFEST_m3_run_v1_8 (5b5b7861) lists the run, bar, scal, graph, series, major, entries and record modules and the
                run's inputs with this script's full sha256s; the asm output's first line names m3_run_v1_8's full sha256 (PLANT-PINS).
  C-BIND        each record through m3_reader_v6.load (asm VERDICT exactly VALID, its RECORD line and sha; laws parsed and checked on
                every free entry); MANIFEST_m3_run_v1_8_asm.N names exactly the asm output and the five records with their sha256s;
                each record's entries are the list's keys of its graph, with the list's parity.
  C-LAW-REM     the item 3, structural: a t-valuation interpreter over the AST of m3_bar_v10's Prep.bound, stage_u and stage_c
                (TVal below). It refuses by default; every name in B_rem's four terms resolves to exactly one binding, a direct
                statement with a value; allow-listed atoms (nonnegative, fixed at J_REF by Lemma U) are pinned by their exact source
                texts (m3_lawcert_v1_pins), each binding of the atom in its function is one of them, and none mentions t, T or J;
                the stage results self.rE, self.nC8, self.nC6 and self.nE have one assignment in the module (the restore from
                hand-offs takes the same names, Prep.UK/CK, pinned in C-LAW-SHAPE). Each term must be a polynomial in t with
                nonnegative fixed coefficients and valuation >= 4, and l2 (the tail factor) one of valuation >= 0. Positive
                control, then nine plants that must each refuse: six of the plan, a second binding (condition 2), and two
                allow-list plants (a pin that is not the name's definition; a t-dependent name with its own definition, condition 4).
  C-LAW-SHAPE   the tail, ann and far statements, sup_F, norm_any, chi_tail_up, ive1, logtree, logmain, far_base, the bound's
                return, Prep.UK/CK, __init__'s t, rates, tilts and restore, laws_of, the entry lines that write laws, and the record
                writer equal their pinned source texts as ASTs, each in its named place (three plants).
  C-LAWFIELDS   each free entry's laws equal an independent recompute from the pinned inputs: rem_tpow 4; tail = {n: g.n,
                J_REF: 300, a_G: [[a_v, up(G_vv)]]} with the graph's G_vv and m3ref_v1_10's a_v (the run's manifest l.17-27); ann the
                same with tilt_p's G_vv (rates from ap); far_cF = m_F + n(V-1)/2 with m_F from the pinned sup_F, which must be >= this
                script's own exponent max(d - i) over the nonzero coefficients (negative values allowed, with the constant term's 0;
                ); far_rate = down(alpha_lo - c_F/300).
  C-MONO-FAR    every recomputed far rate has its lower end > 0.
  C-BAND        sanity: LAWCERT_CLAIM's right side in arb (prec 128; P2(s) = e^(-s/2), P3(s) = erfc(sqrt(s/2)) + sqrt(2s/pi) e^(-s/2),
                ratio upper ends) at J = 300, 600, 1000 and 3000: <= err (1 + 2^-30) at 300, <= err beyond, and non-increasing.
  C-LAWCERT-RT  the certificate parses through m3_reader_v6.loads_lawcert against the loaded records; twelve plants each refused
                (the plan's nine, the records map without one loaded record, a non-canonical exact string, and a writing
                job whose VERDICT line is VERDICT VALID-PRECERT).
Arguments: N LIM (N = 3 or 4; LIM = RLIMIT_CPU soft limit in s, 5..540).
Run: D=/mnt/g2/release/root/code/pk03; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/m3_lawcert_v1.py N LIM > $D/out/m3_lawcert_v1_N.out 2> $D/out/m3_lawcert_v1_N.err
"""
import resource, sys, time, hashlib, signal, os, json, re, copy, ast, textwrap

if len(sys.argv) != 3 or sys.argv[1] not in ('3', '4', 'static'):
    print('usage: m3_lawcert_c3k_v2.py ITEM LIM   (ITEM = 3, 4 or static; LIM = RLIMIT_CPU soft limit in s, 5..540)')
    sys.exit(2)
STATIC = sys.argv[1] == 'static'   # m3_lawcert_s9h_v1: the static item checks the bar port before production
NN = 4 if STATIC else int(sys.argv[1])
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r' % sys.argv[2])
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
    sys.stdout.flush()
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
W18 = '/mnt/g2/release/root/code'
OWN = W18 + '/pk03'
MYD = W18 + '/pk22/m3'   # m3_lawcert_c3h_v1: the c3h runner's folder (its records, asm outputs, hand-offs; this certificate)
OUTD = MYD + '/out'
HANDD = MYD + '/hand'   # m3_lawcert_c3h_v1: the c3h hand-offs (C-NO-RESUME)
OUTD_IN = OWN + '/out'   # m3_lawcert_s9h_v1: pk03's float references (here P16S4)
G4 = W18 + '/pk22/midrow/g4'   # m3_lawcert_c3h_v1: the c3h run manifest
INP = W18 + '/pk10/scratch'
W4 = W18 + '/pk11/out'
J_REF = 300
PSX = W18 + '/pk22/midrow/psixy'   # m3_lawcert_c3k_v2: the z9symxyp trial files (the runner's PSX)
E4M = W18 + '/pk22/midrow/e4'   # m3_lawcert_c3k_v1: the c3k run manifest
FAMS = ('E4D', 'E4N')   # m3_lawcert_c3k_v1: the two c3k_1 records (H-CONN E4; the row 4535)
RUNF = 'm3_run_v1_9_3_px22_c3k_2.py'   # m3_lawcert_c3k_v2: the runner whose entry pieces and asm wrote the records
C3K1F = 'm3_run_v1_9_3_px22_c3k_1.py'   # m3_lawcert_c3k_v2: c3k_1, whose prep pieces c3k_2 reused
EPFX = {'E4D': 'F4D', 'E4N': 'F4N'}   # m3_lawcert_c3k_v2: the runner's own item prefixes (its EPFX)
PREPOF = {'E4D': 'E4D', 'E4N': 'E4N'}   # m3_lawcert_c3k_v1: each family's own prep (the runner's PREPOF)
PRODF = {'E4D': (MYD, C3K1F), 'E4N': (MYD, C3K1F)}   # m3_lawcert_c3k_v2: c3k_1 produced the preps c3k_2 reused
FAMREF = {'E4D': 'P16E4D', 'E4N': 'P16E4N'}   # m3_lawcert_c3k_v1: the float family of the PREPJSON whose radii each prep took
PREPREF = {'E4D': (OUTD, 'm3ref_px22_v1_7_P16E4D.%d.p1_z9symxy.out'), 'E4N': (OUTD, 'm3ref_px22_v1_7_P16E4N.%d.p2_z9symxy.out')}   # the runner's PREPREF
LISTF = 'C3K_ENTRY_LIST_v1_2.json'   # m3_lawcert_c3k_v2: the c3k_2 list
SIDEF = (E4M, 'MANIFEST_E4_C3K2_v1.sha256')   # m3_lawcert_c3k_v2: the c3k_2 run manifest (absolute paths)
PINS_STATIC = {   # m3_lawcert_s9h_v1: (folder, file) -> sha256, read by every item
    (OWN, 'm3_scal_v2.py'): 'd22d3ad696074d4235f0fd31b026477e87f96f5d4b5331e29ab8d399e1e8f054',
    (OWN, 'm3_graph_v3.py'): '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    (OWN, 'm3_series_v2.py'): '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    (OWN, 'm3_major_v2.py'): '89dd5a2184a511d4dea39fb3c558501e9738af118be9d41f2ac4b2d4b8d7b016',
    (OWN, 'm3_bar_v11.py'): 'a11438d0b7d555e3f53aae65e57588df0a2a8a88a79fd0dc47300feeed4f59e3',
    (OWN, 'm3_entries_v3.py'): '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    (OWN, 'm3_record_v4.py'): '2c8a53efb5170d6c6e320bd814c824e69d2ccdd73c57cf87a9130b796109e30f',
    (OWN, 'm3_reader_v6_3.py'): '539b613f6a9c07a9bef3d0cbb408c1d41de276a6a59aede8b03149204ce28661',
    (MYD, RUNF): '7d41512363828e06584c468180bbfee8bd4d78203e336e5f46612975418ab64b',   # m3_lawcert_c3k_v2: the runner c3k_2
    (MYD, C3K1F): '8876ba2883a37f2946ea9d40a2afda6c6ee4d1738f3c332303da69e0194d2c46',   # m3_lawcert_c3k_v2: c3k_1, the producer of the reused preps
    (MYD, 'm3_lawcert_c3h_v1_pins.py'): 'f22f8b9ddba117e65e5d4bcb17cc4292cf85bc1ac7ee5202107025fd9b433f0a',
    (MYD, LISTF): 'e82f042cf2f8f97ee0ce60adea76209ea577937f1ccd16c4484bb66e9a7efe73',
    SIDEF: '50003fbf8ea549481778bbc788f4650e505ea85deb9457c4c0d9fcb932a0799f',
}
INPUTS = {   # m3_lawcert_s9h_v1: read by the items 4 and 3 (C-LAWFIELDS); m3_lawcert_c3k_v1: z9symxy and the E4 twins
    (PSX, 'ts_N4_J170_D_S_z9symxyp_v1.json'): '4f0199bc6f3b03d906c4f268d51e4aee29432cf32e6bb9a9f91cd072b983acd0',   # m3_lawcert_c3k_v2: state 10'
    (PSX, 'ts_N3_S_z9symxyp_v1.json'): '0a6109691c8626c06073e5c3e7be66026e0c3cafbb4377b1f152ced58624ecc7',   # m3_lawcert_c3k_v2: state 10'
    (W4, 'vacres_K3_N4_sym_v1.json'): 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    (W4, 'vacres_K3_N3_sym_v1.json'): 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    (INP, 'm2_N4_J170.json.b'): '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    (INP, 'm2_N3_J170.json.b'): '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    (OUTD, 'm3ref_px22_v1_7_P16E4D.4.p1_z9symxy.out'): '0d2610017e2f84763f81e5b46a027ed68cd636fa3b5b197ac667a42de5c6cc68',
    (OUTD, 'm3ref_px22_v1_7_P16E4D.3.p1_z9symxy.out'): 'e861177831cee9b7f9ed0d8a31cb2f9bfedf592e8843c99af3452ee1cc461b04',
    (OUTD, 'm3ref_px22_v1_7_P16E4N.4.p2_z9symxy.out'): 'b5169c8ead6fc0b7092505a39cb1ec42bb03effaf765f0b4dfc230e9f8242174',
    (OUTD, 'm3ref_px22_v1_7_P16E4N.3.p2_z9symxy.out'): 'd4a9fcb3f174eb7d899201556453ff6aa12457c16ad32d951b1ce34e86cc9fbd',
}
FORMAT = 'M3_LAWCERT_v1'
CLAIM = ('for every J >= J_REF, t = 1/J: |I(J)/main(J) - sum_k ak[k] t^k| <= rem (J_REF/J)^4 + tail (P(J; tail)/P(J_REF; tail))^(1/2) '
         '+ ann (P(J; ann)/P(J_REF; ann))^(1/2) + far exp(-far_rate (J - J_REF)) + sum_k ak_rad[k] t^k, where rem, tail, ann, far are '
         'the entry\'s B parts, P(J; x) = sum over the pairs [a, G] of laws.x.a_G of Prob(chi^2_n > J a / G) with n = laws.x.n, and '
         'far_rate = laws.far_rate (Lemma U, U3: PLAN_M3_CODE_v1_2 sect. C; PLAN_M3_LAWCERT_v1 sect. 3)')
FAILS, NOFIRE = [], []


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def finish():
    out('STAGE-CPU total %.2f s' % cpu())
    if FAILS or NOFIRE:
        out('VERDICT INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE]))
    else:
        out('VERDICT VALID')


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tsha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def flip(h):
    return h[:-1] + ('0' if h[-1] != '0' else '1')


def stage(name):
    STAGE[0] = name
    out('STAGE-CPU %s start %.2f s' % (name, cpu()))


SELF_SHA = sha(os.path.abspath(__file__))
out('m3_lawcert_c3k_v2 N %s LIM %d; script sha256 %s; python %s' % (sys.argv[1], LIM, SELF_SHA, sys.version.split()[0]))
stage('C-HASH')
bad = [f for (d, f), h in PINS_STATIC.items() if not os.path.exists(os.path.join(d, f)) or sha(os.path.join(d, f)) != h]
if not STATIC:
    bad += [f for (d, f), h in INPUTS.items() if not os.path.exists(os.path.join(d, f)) or sha(os.path.join(d, f)) != h]
gate('C-HASH', not bad, '(%d pinned files%s)%s' % (len(PINS_STATIC), '' if STATIC else ', %d inputs' % len(INPUTS),
                                                    (': changed or missing ' + ', '.join(bad)) if bad else ''))
plant('PLANT-HASH', sha(os.path.join(OWN, 'm3_bar_v11.py')) != flip(PINS_STATIC[(OWN, 'm3_bar_v11.py')]),
      '(m3_bar_v11 against its sha256 with the last digit changed)')
if FAILS:
    finish()
    sys.exit(1)

if not STATIC:   # m3_lawcert_s9h_v1: C-PINS needs the run's asm output
    stage('C-PINS')
    RUNSHA = PINS_STATIC[(MYD, RUNF)]
    PIN_NAMES = ('CODEDIR', 'OWN', 'C2B', 'INP', 'W4', 'MYD', 'OUTD', 'OUTD_IN', 'HANDD', 'PSX', 'OWNMOD', 'INPUTS')   # m3_lawcert_c3k_v1: + PSX


    def runner_pins(src):
        """m3_lawcert_c3h_v1: the runner's pin tables OWNMOD and INPUTS, evaluated without builtins from its module-level assignments of
        them and of the folder names they use. Each name must be bound exactly once in the module's own scope (its top-level statements,
        compound ones walked whole), by a plain top-level assignment, and never declared global or nonlocal. Raises ValueError."""
        tree = ast.parse(src)
        glob = set(x for n in ast.walk(tree) if isinstance(n, (ast.Global, ast.Nonlocal)) for x in n.names)
        ns_ = {'__builtins__': {}}
        for nm in PIN_NAMES:
            nb = 0
            for st in tree.body:
                if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    nb += st.name == nm
                    continue
                nb += sum(1 for x in ast.walk(st) if isinstance(x, ast.Name) and x.id == nm and not isinstance(x.ctx, ast.Load))
                nb += sum(1 for x in ast.walk(st) if isinstance(x, ast.alias) and (x.asname or x.name).split('.')[0] == nm)
            top = [st for st in tree.body if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name)
                   and st.targets[0].id == nm]
            if nb != 1 or len(top) != 1 or nm in glob:
                raise ValueError('%s: %d bindings in the module scope, %d top-level assignments%s' % (
                    nm, nb, len(top), ', declared global' if nm in glob else ''))
            exec(compile(ast.Module(body=[top[0]], type_ignores=[]), '%s:%s' % (RUNF, nm), 'exec'), ns_)
        return ns_['OWNMOD'], ns_['INPUTS']


    def pins_missing(src):
        """m3_lawcert_c3h_v1: this script's pins that the run read and the runner's tables lack or pin with another sha256 (the pk03
        modules in OWNMOD; the inputs, the list and both producers in INPUTS), and how many were compared."""
        r_own, r_inp = runner_pins(src)
        miss_ = [f for (d, f), h in PINS_STATIC.items() if d == OWN and (d, f) not in PRODF.values() and r_own.get(f) != h]
        want_inp = dict(INPUTS)
        want_inp.update({k: PINS_STATIC[k] for k in ((MYD, LISTF), (MYD, C3K1F))})   # m3_lawcert_c3k_v2: the list and c3k_1 (the prep producer)
        miss_ += [f for (d, f), h in want_inp.items() if r_inp.get((d, f)) != h]
        return miss_, len(want_inp) + sum(1 for (d, f) in PINS_STATIC if d == OWN and (d, f) not in PRODF.values())


    with open(os.path.join(MYD, RUNF)) as fh:
        RUNSRC = fh.read()
    try:
        miss, npin = pins_missing(RUNSRC)
    except ValueError as ex:
        miss, npin = ['refused: %s' % ex], 0
    ASM = os.path.join(OUTD, 'm3_run_v1_9_3_asm.%d_c3k2.out' % NN)
    with open(ASM) as fh:
        ASM_FIRST = fh.readline().rstrip('\n')
    asm_ok = ASM_FIRST.startswith('m3_run_v1_9_3 item asm.%d LIM ' % NN) and ('; script sha256 %s;' % RUNSHA) in ASM_FIRST
    gate('C-PINS', not miss and asm_ok, '(the runner %s pins %d of this script\'s pins in its own OWNMOD and INPUTS (the modules, the inputs, '
         'the list) with the same full sha256s; the asm output\'s first line names the runner %s)%s' % (
             RUNF, npin, RUNSHA[:8], (': not pinned alike ' + ', '.join(miss)) if miss else ''))
    plant('PLANT-PINS', ('; script sha256 %s;' % flip(RUNSHA)) not in ASM_FIRST,
          '(the asm output\'s first line against the runner\'s sha256 with the last digit changed)')
    BARPIN = "'m3_bar_v11.py': '%s'" % PINS_STATIC[(OWN, 'm3_bar_v11.py')]
    rmut = RUNSRC.replace(BARPIN, "'m3_bar_v11.py': '%s'" % flip(PINS_STATIC[(OWN, 'm3_bar_v11.py')]), 1) if RUNSRC.count(BARPIN) == 1 else None
    try:
        fired = rmut is not None and 'm3_bar_v11.py' in pins_missing(rmut)[0]
    except ValueError:
        fired = False
    plant('PLANT-PINS', fired, '(the runner text with its bar pin\'s last digit changed must leave m3_bar_v11 not pinned alike)')

from fractions import Fraction
import importlib.util


def load_as(name, path):
    """m3_lawcert_s9h_v1: a pinned file loaded under the given module name from its full path (dependencies first)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


GENERIC = [('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_major', 'm3_major_v2.py'),
           ('m3_bar', 'm3_bar_v11.py'), ('m3_entries', 'm3_entries_v3.py')]
MODS = {name: load_as(name, os.path.join(OWN, fname)) for name, fname in GENERIC}
S, SER, BAR, ENT = (MODS[k] for k in ('m3_scal', 'm3_series', 'm3_bar', 'm3_entries'))
GR = MODS['m3_graph']
RDR = load_as('m3_reader_v6_3', os.path.join(OWN, 'm3_reader_v6_3.py'))
PINS = load_as('m3_lawcert_c3h_v1_pins', os.path.join(MYD, 'm3_lawcert_c3h_v1_pins.py')).PINS
from mpmath import iv
import flint
S.setup()
out('PRECISION iv.prec %d (m3_scal_v2.setup, as the run)' % iv.prec)

if not STATIC:   # m3_lawcert_s9h_v1: C-BIND and C-PRODUCER need the records
    stage('C-BIND')
    with open(os.path.join(MYD, LISTF)) as fh:
        LIST = json.load(fh)
    RECS = {}
    for f in FAMS:
        RECS[f] = RDR.load(os.path.join(OUTD, 'm3_c3kp_%s_N%d_J300_c3kp.json' % (f, NN)), ASM, J_REF, NN)
    SIDE = os.path.join(*SIDEF)   # m3_lawcert_c3k_v1: the c3k run manifest (absolute paths), pinned in PINS_STATIC
    side = {}
    with open(SIDE) as fh:
        for ln in fh:
            h_, p_ = ln.rstrip('\n').split('  ', 1)
            side[p_] = h_
    want_side = {ASM: sha(ASM)}
    want_side.update({os.path.join(OUTD, RECS[f]['name']): RECS[f]['sha256'] for f in FAMS})
    side_bad = [os.path.basename(p) for p, h in want_side.items() if side.get(p) != h]
    LKEYS = {f: set(e['key'] for e in LIST['entries'] if e['graph'] == f) for f in FAMS}
    scope = [f for f in FAMS if set(RECS[f]['laws']) != LKEYS[f] or any(d['parity'] != 'free' for d in RECS[f]['laws'].values())]
    nfree = sum(1 for f in FAMS for d in RECS[f]['laws'].values() if d['parity'] == 'free')
    gate('C-BIND', not side_bad and not scope, '(the c3k records through m3_reader_v6_3.load against %s; the run manifest %s lists the asm '
         'output and the records with these sha256s; each record holds exactly the C3-h list\'s keys of its graph, every one free: %s; %d '
         'free)%s%s' % (os.path.basename(ASM), os.path.basename(SIDE), ', '.join('%s %d' % (f, len(RECS[f]['laws'])) for f in FAMS), nfree,
                        (': not listed alike ' + ', '.join(side_bad)) if side_bad else '', (': scope differs for ' + ', '.join(scope)) if scope else ''))
    eng_bad = [f for f in FAMS if not isinstance(RECS[f]['top'].get('engine'), dict)
               or RECS[f]['top']['engine'].get('m3_run_v1_9_3') != RUNSHA
               or (RECS[f]['top']['engine'].get('modules') or {}).get('m3_bar_v11.py') != PINS_STATIC[(OWN, 'm3_bar_v11.py')]
               or not isinstance(RECS[f]['top'].get('prep16'), dict)
               or RECS[f]['top']['prep16'].get('prep_family') != PREPOF[f]
               or RECS[f]['top']['prep16'].get('prep_script') != PINS_STATIC[PRODF[f]]]
    gate('C-PRODUCER', not eng_bad, '(each record\'s engine names the runner %s and m3_bar_v11 %s, the bar that C-LAW-REM, C-PREP16 and '
         'C-LAW-SHAPE audit; its prep16 names the prep family and its producer: %s)%s' % (
             RUNSHA[:8], PINS_STATIC[(OWN, 'm3_bar_v11.py')][:8],
             ', '.join('%s %s %s' % (f, PREPOF[f], PINS_STATIC[PRODF[f]][:8]) for f in FAMS), (': differ ' + ', '.join(eng_bad)) if eng_bad else ''))
    if FAILS:
        finish()
        sys.exit(1)


# ------------------------------------------------------------------ C-LAW-REM and C-LAW-SHAPE: the AST checks
class Refuse(Exception):
    pass


def find_node(tree, path):
    """the FunctionDef or ClassDef at path ('name' or 'Class.name') of a parsed module, defined exactly once."""
    body, node = tree.body, None
    for p in path.split('.'):
        hits = [n for n in body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == p]
        if len(hits) != 1:
            raise Refuse('%s: %d definitions of %s' % (path, len(hits), p))
        node = hits[0]
        body = node.body
    return node


def stmts_in(node):
    """every statement under node, nested blocks included, nested function and class bodies excluded."""
    acc = []

    def visit(stmts):
        for st in stmts:
            acc.append(st)
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            for fld in ('body', 'orelse', 'finalbody'):
                sub = getattr(st, fld, None)
                if isinstance(sub, list):
                    visit([s for s in sub if isinstance(s, ast.stmt)])
            for h in getattr(st, 'handlers', None) or []:
                visit(h.body)
    visit(node.body)
    return acc


def bindings(fn):
    """name -> [(value or None, top)] for every binding of a plain name in fn's own scope; top: a direct statement of fn's body."""
    acc = {}
    tops = set(id(s) for s in fn.body)

    def add(nm, val, top):
        acc.setdefault(nm, []).append((val, top))

    def bind(tg, val, top):
        if isinstance(tg, ast.Name):
            add(tg.id, val, top)
        elif isinstance(tg, (ast.Tuple, ast.List)):
            if isinstance(val, (ast.Tuple, ast.List)) and len(val.elts) == len(tg.elts):
                for a, b in zip(tg.elts, val.elts):
                    bind(a, b, top)
            else:
                for nd in ast.walk(tg):
                    if isinstance(nd, ast.Name):
                        add(nd.id, None, top)
        elif isinstance(tg, ast.Starred):
            bind(tg.value, None, top)
    for st in stmts_in(fn):
        top = id(st) in tops
        if isinstance(st, ast.Assign):
            for tg in st.targets:
                bind(tg, st.value, top)
        elif isinstance(st, (ast.AugAssign, ast.AnnAssign)):
            bind(st.target, None, top)
        elif isinstance(st, (ast.For, ast.AsyncFor)):
            bind(st.target, None, False)
        elif isinstance(st, (ast.With, ast.AsyncWith)):
            for it in st.items:
                if it.optional_vars is not None:
                    bind(it.optional_vars, None, False)
        elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            add(st.name, st, top)
        elif isinstance(st, (ast.Import, ast.ImportFrom)):
            for a in st.names:
                add((a.asname or a.name).split('.')[0], None, top)
        elif isinstance(st, ast.Try):
            for h in st.handlers:
                if h.name:
                    add(h.name, None, False)
    for nd in ast.walk(fn):
        if isinstance(nd, ast.NamedExpr):
            add(nd.target.id, None, False)
    return acc


def pin_stmts(key):
    return ast.parse(textwrap.dedent(PINS[key])).body


def is_attr(e, base, attr):
    return isinstance(e, ast.Attribute) and isinstance(e.value, ast.Name) and e.value.id == base and e.attr == attr


def mentions_t(nodes):
    """an allow-listed definition may not mention t, T or J (plain or as self.t / self.J)."""
    for st in nodes:
        for nd in ast.walk(st):
            if isinstance(nd, ast.Name) and nd.id in ('t', 'T', 'J'):
                return nd.id
            if isinstance(nd, ast.Attribute) and isinstance(nd.value, ast.Name) and nd.value.id == 'self' and nd.attr in ('t', 'J'):
                return 'self.' + nd.attr
    return None


def self_assigns(tree, attr):
    """the methods of class Prep that assign self.<attr>, one entry per assignment, anywhere in the module (m3_lawcert_s9h_v1: class Prep
    alone; m3_lawcert_c3h_v1: Prep16's stage methods, which computed the c3h preps, are R-equal to Prep's, C-PREP16)."""
    acc = []
    for cls in [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Prep']:   # m3_lawcert_s9h_v1: class Prep only (C-PREP-CLASS)
        for fn in [n for n in cls.body if isinstance(n, ast.FunctionDef)]:
            for nd in ast.walk(fn):
                tgs = nd.targets if isinstance(nd, ast.Assign) else ([nd.target] if isinstance(nd, (ast.AugAssign, ast.AnnAssign)) else [])
                for tg in tgs:
                    for x in ast.walk(tg):
                        if is_attr(x, 'self', attr) and isinstance(x.ctx, ast.Store):
                            acc.append('%s.%s' % (cls.name, fn.name))
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        for nd in ast.walk(fn):
            if isinstance(nd, ast.Assign):
                for tg in nd.targets:
                    for x in ast.walk(tg):
                        if is_attr(x, 'self', attr) and isinstance(x.ctx, ast.Store):
                            acc.append(fn.name)
    return acc


class TVal:
    """t-valuation of the expressions of one Prep method. An accepted expression is a polynomial in t with
    nonnegative coefficients fixed at J_REF, and v(e) is a lower bound of its t-adic valuation:
      a + b -> min; a * b -> sum; a / (positive literal) -> v(a); T(k) and S.ipow(t, k) -> k; S.ipow(x, k), k a literal -> k v(x);
      t -> 1; the form iv.mpf([iv.mpf(0), X.b if X.b < Y.b else Y.b]) -> min(v(X), v(Y)); S.isum over a comprehension -> the minimum over
      its enumerated indices (arithmetic filters evaluated, the fixed filter 'not is_zero(Fi[...])' kept as a superset); S.isum over the
      values of a dict built by one literal and single-key stores -> the minimum over them; an index-only branch -> its branch;
      allow-listed atoms, atom calls, self.norm_any calls, subscripts of atom lists, iv.mpf of a positive literal,
      S.ipow(atom, data-dependent power) and abs(S.I(scal)) -> 0.
    Anything else refuses: subtraction, negation, an unknown name or call, division by anything but a positive literal, a name with
    more than one binding or bound under a branch.
    Atoms and norm_any values are evaluated once, at J_REF, and enter with valuation 0. They bound the quantities the bar needs at every
    t <= t_REF by Lemma U: the radii and tilt rates are fixed at J_REF and admissible for every smaller t
    (H_+ <= c t X <= c t_REF X on Omega), and the only t-carrying argument, hh, is pointwise nonnegative and nondecreasing in t (U2),
    so its J_REF norm, exact or by the Hoelder fallback, bounds the true norm at every t <= t_REF. The computed values themselves need
    not be monotone in t (the review 03674489 l.41)."""

    def __init__(self, tree, path, atoms, attr_atoms, attrs):
        self.tree, self.path = tree, path
        self.fn = find_node(tree, path)
        self.b = bindings(self.fn)
        self.stm = set(ast.dump(s) for s in stmts_in(self.fn))
        self.atoms, self.attr_atoms, self.attrs = atoms, attr_atoms, attrs
        self.memo, self.okatoms = {}, set()

    def fail(self, why):
        raise Refuse('%s: %s' % (self.path, why))

    def one(self, name):
        bs = self.b.get(name, [])
        if len(bs) != 1 or not bs[0][1] or bs[0][0] is None:
            self.fail('%s must have exactly one binding, a direct statement with a value (bindings %d)' % (name, len(bs)))
        return bs[0][0]

    def atom(self, name):
        """an allow-listed atom: each pinned statement is a statement of this function, the atom has exactly as many bindings here as
        in its pinned statements, and no pinned statement mentions t, T or J."""
        if name in self.okatoms:
            return 0
        nodes = [s for key in self.atoms[name] for s in pin_stmts(key)]
        bad = mentions_t(nodes)
        if bad:
            self.fail('allow-listed %s mentions %s' % (name, bad))
        if any(ast.dump(s) not in self.stm for s in nodes):
            self.fail('a pinned definition of %s is not a statement of this function' % name)
        fake = ast.parse('def _pinned():\n    pass\n').body[0]
        fake.body = nodes
        if len(bindings(fake).get(name, [])) != len(self.b.get(name, [])):
            self.fail('%s has bindings outside its pinned definition' % name)
        self.okatoms.add(name)
        return 0

    def attr_atom(self, attr):
        key, where = self.attr_atoms[attr]
        nodes = pin_stmts(key)
        bad = mentions_t(nodes)
        if bad:
            self.fail('allow-listed self.%s mentions %s' % (attr, bad))
        fnw = find_node(self.tree, where)
        if any(ast.dump(s) not in set(ast.dump(x) for x in stmts_in(fnw)) for s in nodes):
            self.fail('the pinned definition of self.%s is not a statement of %s' % (attr, where))
        if self_assigns(self.tree, attr) != [where]:
            self.fail('self.%s is assigned in %s, expected once in %s' % (attr, self_assigns(self.tree, attr), where))
        return 0

    def is_tref(self, x):
        if is_attr(x, 'self', 't'):
            return True
        if isinstance(x, ast.Name) and x.id == 't':
            return is_attr(self.one('t'), 'self', 't')
        return False

    def check_T(self):
        lam = self.one('T')
        ok = (isinstance(lam, ast.Lambda) and len(lam.args.args) == 1 and not lam.args.vararg and not lam.args.kwarg and not lam.args.defaults
              and isinstance(lam.body, ast.Call) and is_attr(lam.body.func, 'S', 'ipow') and len(lam.body.args) == 2 and not lam.body.keywords
              and self.is_tref(lam.body.args[0]) and isinstance(lam.body.args[1], ast.Name) and lam.body.args[1].id == lam.args.args[0].arg)
        if not ok:
            self.fail('T is not lambda k: S.ipow(t, k) with t = self.t')

    def ival(self, e, env):
        """an exact int: literals, comprehension indices and +, -, * of them."""
        if isinstance(e, ast.Constant) and type(e.value) is int:
            return e.value
        if isinstance(e, ast.Name) and e.id in env:
            return env[e.id]
        if isinstance(e, ast.BinOp) and isinstance(e.op, (ast.Add, ast.Sub, ast.Mult)):
            a, b = self.ival(e.left, env), self.ival(e.right, env)
            return a + b if isinstance(e.op, ast.Add) else (a - b if isinstance(e.op, ast.Sub) else a * b)
        self.fail('not an exact int: %s' % ast.dump(e)[:80])

    def itest(self, e, env):
        if isinstance(e, ast.Compare) and len(e.ops) == 1:
            a, b = self.ival(e.left, env), self.ival(e.comparators[0], env)
            op = type(e.ops[0])
            table = {ast.GtE: a >= b, ast.Gt: a > b, ast.LtE: a <= b, ast.Lt: a < b, ast.Eq: a == b, ast.NotEq: a != b}
            if op in table:
                return table[op]
        self.fail('not an index test: %s' % ast.dump(e)[:80])

    @staticmethod
    def fixed_filter(e):
        """'not is_zero(Fi[...])': a filter fixed at J_REF; keeping every index is a superset, so the minimum stays a lower bound."""
        return (isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.Not) and isinstance(e.operand, ast.Call)
                and isinstance(e.operand.func, ast.Name) and e.operand.func.id == 'is_zero' and len(e.operand.args) == 1
                and isinstance(e.operand.args[0], ast.Subscript) and isinstance(e.operand.args[0].value, ast.Name)
                and e.operand.args[0].value.id == 'Fi')

    def enum(self, gens, env):
        envs = [dict(env)]
        for g in gens:
            if not isinstance(g.target, ast.Name) or g.is_async:
                self.fail('comprehension target')
            nxt = []
            for en in envs:
                it = g.iter
                if isinstance(it, ast.Call) and isinstance(it.func, ast.Name) and it.func.id == 'range' and 1 <= len(it.args) <= 2 and not it.keywords:
                    lo, hi = (0, self.ival(it.args[0], en)) if len(it.args) == 1 else (self.ival(it.args[0], en), self.ival(it.args[1], en))
                    vals = list(range(lo, hi))
                elif isinstance(it, (ast.Tuple, ast.List)):
                    vals = [self.ival(x, en) for x in it.elts]
                else:
                    self.fail('comprehension over %s' % ast.dump(it)[:80])
                for v_ in vals:
                    e2 = dict(en)
                    e2[g.target.id] = v_
                    if all(self.fixed_filter(c) or self.itest(c, e2) for c in g.ifs):
                        nxt.append(e2)
            envs = nxt
        return envs

    def dict_values(self, name):
        lit = self.one(name)
        if not isinstance(lit, ast.Dict) or any(k is None or not isinstance(k, ast.Constant) or not isinstance(k.value, str) for k in lit.keys):
            self.fail('%s is not one dict literal with string keys' % name)
        keys = [k.value for k in lit.keys]
        vals = list(lit.values)
        for nd in ast.walk(self.fn):
            if isinstance(nd, ast.Subscript) and isinstance(nd.value, ast.Name) and nd.value.id == name and not isinstance(nd.ctx, ast.Load):
                self.fail('%s[...] is stored or deleted outside a single-key assignment' % name) if not isinstance(nd.ctx, ast.Store) else None
            if isinstance(nd, ast.Attribute) and isinstance(nd.value, ast.Name) and nd.value.id == name and nd.attr != 'values':
                self.fail('%s.%s may change the dict' % (name, nd.attr))
            if isinstance(nd, ast.AugAssign) and isinstance(nd.target, ast.Subscript) and isinstance(nd.target.value, ast.Name) and nd.target.value.id == name:
                self.fail('%s[...] is updated in place' % name)
        for st in stmts_in(self.fn):
            if isinstance(st, ast.Assign) and any(isinstance(tg, ast.Subscript) and isinstance(tg.value, ast.Name) and tg.value.id == name for tg in st.targets):
                tg = st.targets[0]
                if len(st.targets) != 1 or id(st) not in set(id(s) for s in self.fn.body) or not isinstance(tg.slice, ast.Constant) or not isinstance(tg.slice.value, str):
                    self.fail('%s[...] must be stored by direct single-key statements' % name)
                keys.append(tg.slice.value)
                vals.append(st.value)
        if len(set(keys)) != len(keys):
            self.fail('%s has a key stored twice' % name)
        return vals

    @staticmethod
    def zero_min(e):
        """iv.mpf([iv.mpf(0), X.b if X.b < Y.b else Y.b]) -> (X, Y), else None."""
        if not (isinstance(e, ast.Call) and is_attr(e.func, 'iv', 'mpf') and len(e.args) == 1 and not e.keywords
                and isinstance(e.args[0], ast.List) and len(e.args[0].elts) == 2):
            return None
        z, m = e.args[0].elts
        if not (isinstance(z, ast.Call) and is_attr(z.func, 'iv', 'mpf') and len(z.args) == 1 and isinstance(z.args[0], ast.Constant)
                and z.args[0].value == 0 and isinstance(m, ast.IfExp) and isinstance(m.test, ast.Compare) and len(m.test.ops) == 1
                and isinstance(m.test.ops[0], ast.Lt)):
            return None
        a, b, x, y = m.test.left, m.test.comparators[0], m.body, m.orelse
        if all(isinstance(q, ast.Attribute) and q.attr == 'b' for q in (a, b, x, y)) and ast.dump(a) == ast.dump(x) and ast.dump(b) == ast.dump(y):
            return a.value, b.value
        return None

    def v(self, e, env):
        if isinstance(e, ast.Constant) and type(e.value) in (int, float) and e.value > 0:
            return 0
        if isinstance(e, ast.Name):
            n = e.id
            if n in env:
                self.fail('the index %s used as a value' % n)
            if n in self.atoms:
                return self.atom(n)
            if n == 't':
                if not self.is_tref(e):
                    self.fail('t is not self.t')
                return 1
            if n not in self.memo:
                self.memo[n] = None
                self.memo[n] = self.v(self.one(n), {})
            if self.memo[n] is None:
                self.fail('%s is defined through itself' % n)
            return self.memo[n]
        if is_attr(e, 'self', 't'):
            return 1
        if isinstance(e, ast.Attribute) and isinstance(e.value, ast.Name) and e.value.id == 'self' and e.attr in self.attrs:
            return self.attrs[e.attr]()
        if isinstance(e, ast.BinOp):
            if isinstance(e.op, ast.Add):
                return min(self.v(e.left, env), self.v(e.right, env))
            if isinstance(e.op, ast.Mult):
                return self.v(e.left, env) + self.v(e.right, env)
            if isinstance(e.op, ast.Div) and isinstance(e.right, ast.Constant) and type(e.right.value) in (int, float) and e.right.value > 0:
                return self.v(e.left, env)
            self.fail('operator %s refused' % type(e.op).__name__)
        if isinstance(e, ast.IfExp):
            return self.v(e.body if self.itest(e.test, env) else e.orelse, env)
        if isinstance(e, ast.Subscript):
            base = e.value
            if isinstance(base, ast.Name) and base.id in self.atoms:
                self.ival(e.slice, env)
                return self.atom(base.id)
            if isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name) and base.value.id == 'self' and base.attr in self.attr_atoms:
                self.ival(e.slice, env)
                return self.attr_atom(base.attr)
            self.fail('subscript of %s refused' % ast.dump(base)[:60])
        if isinstance(e, ast.Call):
            f = e.func
            zm = self.zero_min(e)
            if zm is not None:
                return min(self.v(zm[0], env), self.v(zm[1], env))
            if e.keywords:
                self.fail('call with keywords refused')
            if isinstance(f, ast.Name) and f.id == 'T' and len(e.args) == 1:
                self.check_T()
                k = self.ival(e.args[0], env)
                if k < 0:
                    self.fail('negative t power')
                return k
            if is_attr(f, 'S', 'ipow') and len(e.args) == 2:
                x, k = e.args
                if self.is_tref(x):
                    kk = self.ival(k, env)
                    if kk < 0:
                        self.fail('negative t power')
                    return kk
                if isinstance(k, ast.Constant) and type(k.value) is int and k.value >= 0:
                    return k.value * self.v(x, env)
                if isinstance(x, ast.Name) and x.id in self.atoms:
                    return self.atom(x.id)
                self.fail('S.ipow form refused')
            if is_attr(f, 'S', 'isum') and len(e.args) == 1:
                a = e.args[0]
                if isinstance(a, ast.GeneratorExp):
                    vals = [self.v(a.elt, en) for en in self.enum(a.generators, env)]
                    if not vals:
                        self.fail('empty sum')
                    return min(vals)
                if (isinstance(a, ast.Call) and not a.args and isinstance(a.func, ast.Attribute) and a.func.attr == 'values'
                        and isinstance(a.func.value, ast.Name)):
                    return min(self.v(x, {}) for x in self.dict_values(a.func.value.id))
                self.fail('S.isum form refused')
            if isinstance(f, ast.Name) and f.id in self.atoms:
                return self.atom(f.id)
            if is_attr(f, 'self', 'norm_any'):
                return 0
            if is_attr(f, 'iv', 'mpf') and len(e.args) == 1 and isinstance(e.args[0], ast.Constant) and type(e.args[0].value) is int and e.args[0].value > 0:
                return 0
            if (isinstance(f, ast.Name) and f.id == 'abs' and len(e.args) == 1 and isinstance(e.args[0], ast.Call)
                    and is_attr(e.args[0].func, 'S', 'I') and len(e.args[0].args) == 1 and isinstance(e.args[0].args[0], ast.Name)
                    and e.args[0].args[0].id == 'scal'):
                return 0
            self.fail('call %s refused' % ast.dump(f)[:80])
        self.fail('%s refused' % type(e).__name__)


def terms(e):
    """the operands of a chain of + (left-nested)."""
    if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add):
        return terms(e.left) + terms(e.right)
    return [e]


BOUND_ATOMS = {'nF0': ['bar:Prep.bound:nF0'], 'nF0c': ['bar:Prep.bound:nF0c'], 'nF': ['bar:Prep.bound:nF'], 'nFc': ['bar:Prep.bound:nFc'],
               'three': ['bar:Prep.bound:three'], 'EF4': ['bar:Prep.bound:EF4'], 'Nc': ['bar:Prep.bound:Nc'], 'fnorm': ['bar:Prep.bound:fnorm'],
               'gn': ['bar:Prep.bound:gn'], 'hc': ['bar:Prep.bound:hc']}
U_ATOMS = {'N2': ['bar:Prep.stage_u:N2']}
C_ATOMS = {'nh2_6': ['bar:Prep.stage_c:nh2_6']}
ATTR_ATOMS = {'nE': ('bar:Prep.stage_u:nE', 'Prep.stage_u'), 'nE4': ('bar:Prep.stage_u:nE4', 'Prep.stage_u')}


def stage_attr(tv, tree, where, attr):
    """the valuation of the stage result self.<attr>: its one assignment, in the method where."""
    if self_assigns(tree, attr) != [where]:
        raise Refuse('self.%s is assigned in %s, expected once in %s' % (attr, self_assigns(tree, attr), where))
    hits = [st for st in tv.fn.body if isinstance(st, ast.Assign) and len(st.targets) == 1 and is_attr(st.targets[0], 'self', attr)]
    if len(hits) != 1:
        raise Refuse('self.%s is not assigned by one direct statement of %s' % (attr, where))
    return tv.v(hits[0].value, {})


def law_rem(src, bound_atoms=None):
    """C-LAW-REM on a bar source text: the valuations of B_rem's terms (Refuse on any refusal)."""
    tree = ast.parse(src)
    tu = TVal(tree, 'Prep.stage_u', U_ATOMS, {}, {})
    tc = TVal(tree, 'Prep.stage_c', C_ATOMS, {}, {})
    attrs = {'rE': lambda: stage_attr(tu, tree, 'Prep.stage_u', 'rE'), 'nC8': lambda: stage_attr(tc, tree, 'Prep.stage_c', 'nC8'),
             'nC6': lambda: stage_attr(tc, tree, 'Prep.stage_c', 'nC6')}
    tb = TVal(tree, 'Prep.bound', bound_atoms or BOUND_ATOMS, ATTR_ATOMS, attrs)
    if self_assigns(tree, 't') != ['Prep.__init__']:
        raise Refuse('self.t is assigned in %s, expected once in Prep.__init__' % self_assigns(tree, 't'))
    vs = [tb.v(x, {}) for x in terms(tb.one('B_rem'))]
    l2 = tb.v(tb.one('l2'), {})
    return vs, l2


stage('C-LAW-REM')
with open(os.path.join(OWN, 'm3_bar_v11.py')) as fh:   # m3_lawcert_c3h_v1: the c3h records' bar
    BARSRC = fh.read()
try:
    VS, L2V = law_rem(BARSRC)
    rem_ok, rem_why = len(VS) == 4 and min(VS) >= 4 and L2V >= 0, 'term valuations %s, l2 valuation %d' % (VS, L2V)
except Refuse as ex:
    rem_ok, rem_why = False, 'refused: %s' % ex
gate('C-LAW-REM', rem_ok, '(m3_bar_v11 Prep.bound: B_rem = overflow + nFle3 rE + rho4 + t^4 Nc EF4/24, each term a polynomial in t with '
     'nonnegative coefficients fixed at J_REF and valuation >= 4; l2 a polynomial of valuation >= 0; %s)' % rem_why)
REM_PLANTS = [
    ('T(4) -> T(3) in the EF4 term', 'B_rem = overflow + nFle3 * self.rE + rho4 + T(4) / 24 * Nc * EF4',
     'B_rem = overflow + nFle3 * self.rE + rho4 + T(3) / 24 * Nc * EF4'),
    ('the overflow filter >= 3', 'for i in range(4) for j in range(4) if i + j >= 4)', 'for i in range(4) for j in range(4) if i + j >= 3)'),
    ('nC8 without its factor t', 'self.nC8 = t * (self.norm_any(H1', 'self.nC8 = (self.norm_any(H1'),
    ("rE's 't4|H4|' part with T(3)", "'t4|H4|': T(4) * N2(H4", "'t4|H4|': T(3) * N2(H4"),
    ("a '- nF0' term in B_rem", 'B_rem = overflow + nFle3', 'B_rem = overflow - nF0 + nFle3'),
    ('an unknown name in rho4', 'rho4 = Nc / 24 * iv.mpf(', 'rho4 = Nc / 24 * zeta * iv.mpf('),
    ('a second binding of overflow (condition 2)', '        overflow = S.isum(', '        overflow = nF0\n        overflow = S.isum('),
]
for lab, old, new in REM_PLANTS:
    if BARSRC.count(old) != 1:
        plant('PLANT-LAW-REM', False, '(%s: the text to change occurs %d times, expected once)' % (lab, BARSRC.count(old)))
        continue
    try:
        vs_, l2_ = law_rem(BARSRC.replace(old, new))
        fired, why = not (len(vs_) == 4 and min(vs_) >= 4 and l2_ >= 0), 'valuations %s' % vs_
    except Refuse as ex:
        fired, why = True, 'refused: %s' % str(ex)[:120]
    plant('PLANT-LAW-REM', fired, '(%s: %s)' % (lab, why))
try:
    law_rem(BARSRC, dict(BOUND_ATOMS, nFle3=['bar:Prep.bound:nF0']))
    fired, why = False, 'accepted'
except Refuse as ex:
    fired, why = True, 'refused: %s' % str(ex)[:120]
plant('PLANT-LAW-REM', fired, '(nFle3 allow-listed with a pinned text that is not its definition: %s)' % why)
PINS['plant:nFle3'] = '        nFle3 = S.isum(T(i) * nF[i] for i in range(4))\n'
try:
    law_rem(BARSRC, dict(BOUND_ATOMS, nFle3=['plant:nFle3']))
    fired, why = False, 'accepted'
except Refuse as ex:
    fired, why = True, 'refused: %s' % str(ex)[:120]
plant('PLANT-LAW-REM', fired, '(a t-dependent name allow-listed with its own definition: %s)' % why)
del PINS['plant:nFle3']

stage('C-PREP16')


def in_place(src, place, old, new):
    """m3_lawcert_s9h_v1: src with old replaced by new inside the named place only (the class or method path, find_node), when old occurs
    there exactly once; else None."""
    node = find_node(ast.parse(src), place)
    lines = src.split('\n')
    a, z = node.lineno - 1, node.end_lineno
    seg = '\n'.join(lines[a:z])
    if seg.count(old) != 1:
        return None
    return '\n'.join(lines[:a] + seg.replace(old, new).split('\n') + lines[z:])


def thunk_body(fn):
    """m3_lawcert_c3h_v1: the body X of a thunk 'lambda: X' or 'lambda j=j: X' (one parameter whose default is the same name); else None."""
    if not isinstance(fn, ast.Lambda):
        return None
    a = fn.args
    if a.vararg or a.kwarg or a.kwonlyargs or a.posonlyargs:
        return None
    if not a.args:
        return fn.body
    if len(a.args) == 1 and len(a.defaults) == 1 and isinstance(a.defaults[0], ast.Name) and a.defaults[0].id == a.args[0].arg:
        return fn.body
    return None


class R16(ast.NodeTransformer):
    """m3_lawcert_c3h_v1, the rewrite R of Prep16's stage text into Prep's terms (C-PREP16): self.norm16(lab, which, p, thunk) ->
    self.norm_any(X, which, p, lab) and N2(lab, thunk) -> N2(X, lab), X the thunk's body (Prep16.norm16 returns norm_any(fn(), which, p),
    or the value an earlier piece of the same prep chain recorded for that step; Prep16's N2 is norm16 at 'u', 2 and Prep's N2 norm_any at
    'u', 2, both pinned); self.h(k) -> hk for k = 2, 3, 5, self.h2sq() -> h2sq and self.hh16() -> hh (Prep16.h, h2sq and hh16, pinned in
    C-LAW-SHAPE, build mj.hbar(k), h(2).mul(h(2)) and hhat2(kern, g, a_v, t, h(2)) on Prep's majorants mj, which Prep.__init__ and
    stage_u bind to h2, hh, h3, h5 and h2sq). Any other form of those names is left as it is, so it cannot match Prep's text."""

    def visit_Call(self, node):
        self.generic_visit(node)
        f = node.func
        if is_attr(f, 'self', 'norm16') and len(node.args) == 4 and not node.keywords:
            x = thunk_body(node.args[3])
            if x is not None:
                return ast.Call(func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='norm_any', ctx=ast.Load()),
                                args=[x, node.args[1], node.args[2], node.args[0]], keywords=[])
        if isinstance(f, ast.Name) and f.id == 'N2' and len(node.args) == 2 and not node.keywords:
            x = thunk_body(node.args[1])
            if x is not None:
                return ast.Call(func=f, args=[x, node.args[0]], keywords=[])
        if (is_attr(f, 'self', 'h') and len(node.args) == 1 and not node.keywords and isinstance(node.args[0], ast.Constant)
                and type(node.args[0].value) is int and node.args[0].value in (2, 3, 5)):
            return ast.Name(id='h%d' % node.args[0].value, ctx=ast.Load())
        if is_attr(f, 'self', 'h2sq') and not node.args and not node.keywords:
            return ast.Name(id='h2sq', ctx=ast.Load())
        if is_attr(f, 'self', 'hh16') and not node.args and not node.keywords:
            return ast.Name(id='hh', ctx=ast.Load())
        return node


def stage_seq(tree, path, drop_keys, rewrite):
    """m3_lawcert_c3h_v1: the statements of the method at path as AST dumps, in order: its docstring and the pinned statements of drop_keys
    (each exactly once in the method's body) left out, the rest rewritten by R when rewrite. Raises Refuse."""
    fn = find_node(tree, path)
    body = list(fn.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    dumps0 = [ast.dump(s) for s in body]
    drops = [ast.dump(s) for k in drop_keys for s in pin_stmts(k)]
    for d in drops:
        if dumps0.count(d) != 1:
            raise Refuse('%s: a pinned statement of %s is not once in its body' % (path, ', '.join(drop_keys)))
    return [ast.dump(R16().visit(copy.deepcopy(s)) if rewrite else s) for s, d in zip(body, dumps0) if d not in drops]


def all_assigns(tree, attr):
    """m3_lawcert_c3h_v1: v1_2's self_assigns over every class and module-level function, augmented and annotated assignments included."""
    acc = []
    owners = [(cls.name + '.', fn) for cls in tree.body if isinstance(cls, ast.ClassDef) for fn in cls.body if isinstance(fn, ast.FunctionDef)]
    owners += [('', fn) for fn in tree.body if isinstance(fn, ast.FunctionDef)]
    for pre, fn in owners:
        for nd in ast.walk(fn):
            tgs = nd.targets if isinstance(nd, ast.Assign) else ([nd.target] if isinstance(nd, (ast.AugAssign, ast.AnnAssign)) else [])
            for tg in tgs:
                for x in ast.walk(tg):
                    if is_attr(x, 'self', attr) and isinstance(x.ctx, ast.Store):
                        acc.append(pre + fn.name)
    return acc


STAGE16 = [('Prep.stage_u', 'Prep16.stage_u16', ['bar:Prep.stage_u:setup', 'bar:Prep.stage_u:N2'], ['bar:Prep16.stage_u16:N2', 'bar:Prep16.stage_u16:cleanup']),
           ('Prep.stage_c', 'Prep16.stage_c16', ['bar:Prep.stage_c:setup'], ['bar:Prep16.stage_c16:setup', 'bar:Prep16.stage_c16:cleanup'])]
STAGE_ATTRS = {'Prep.stage_u': ('nE', 'nE4', 'rE_parts', 'rE'), 'Prep.stage_c': ('nC8', 'nC6', 'Pout', 'Pout_p', 'farbase', 'alpha_lo', 'tree')}


def prep16_bar_check(src):
    """m3_lawcert_c3h_v1, C-PREP16 (a) and (b) on a bar text: R(Prep16.stage_x16) has exactly Prep.stage_x's statements in order, once the
    pinned statements are left out; each stage result is assigned in exactly Prep.stage_x and Prep16.stage_x16, and self.h2, self.hh and
    self.t only in Prep.__init__. Returns (ok, why)."""
    tree = ast.parse(src)
    why = []
    for a, b, da, db in STAGE16:
        try:
            if stage_seq(tree, a, da, False) != stage_seq(tree, b, db, True):
                why.append('R(%s) differs from %s' % (b, a))
        except Refuse as ex:
            why.append(str(ex))
        for at in STAGE_ATTRS[a]:
            if sorted(all_assigns(tree, at)) != sorted([a, b]):
                why.append('self.%s assigned in %s' % (at, all_assigns(tree, at)))
    for at in ('h2', 'hh', 't'):
        if all_assigns(tree, at) != ['Prep.__init__']:
            why.append('self.%s assigned in %s' % (at, all_assigns(tree, at)))
    return not why, why


RUN_PRODUCERS = ((MYD, RUNF), (MYD, C3K1F))   # m3_lawcert_c3k_v2: the runner and c3k_1, the producer of the preps it reused
BAR_STORES_OK = ["BAR.ARB['kern']", 'BAR.FALLBACKS[:]']   # m3_lawcert_c3h_v1: the runners' only stores into the bar module


def root_name(e):
    while isinstance(e, (ast.Attribute, ast.Subscript, ast.Starred)):
        e = e.value
    return e.id if isinstance(e, ast.Name) else None


def runner_prep_check(src):
    """m3_lawcert_c3h_v1, C-PREP16 (c) on a runner text: BAR.Prep16(...) and BAR.Prep(...) are each called exactly once, in make_prep, with
    the keyword stages=(); no other use of an attribute named Prep or Prep16; .stage_u16() and .stage_c16() are each called once, in
    run_prep16, and .scalars_out twice, there only; no call of .stage_u or .stage_c; the stores and deletes rooted at the name BAR are
    exactly BAR_STORES_OK; no setattr or delattr on anything rooted at BAR. Returns (ok, why)."""
    tree = ast.parse(src)
    par_ = {}
    for p in ast.walk(tree):
        for c in ast.iter_child_nodes(p):
            par_[id(c)] = p
    spans = [(n.lineno, n.end_lineno, n.name) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    def where(ln):
        hit = [nm for a, z, nm in spans if a <= ln <= z]
        return hit[0] if hit else '<module>'
    why, calls, stores = [], {}, []
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute) and n.attr in ('Prep', 'Prep16'):
            p = par_.get(id(n))
            if not (isinstance(n.value, ast.Name) and n.value.id == 'BAR' and isinstance(n.ctx, ast.Load) and isinstance(p, ast.Call) and p.func is n):
                why.append('l.%d uses %s other than as a call' % (n.lineno, ast.unparse(n)))
                continue
            st = [k for k in p.keywords if k.arg == 'stages']
            calls.setdefault(n.attr, []).append((where(n.lineno), len(st) == 1 and isinstance(st[0].value, ast.Tuple) and not st[0].value.elts))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ('stage_u', 'stage_c', 'stage_u16', 'stage_c16', 'scalars_out'):
            if n.func.attr in ('stage_u', 'stage_c'):
                why.append('l.%d calls .%s' % (n.lineno, n.func.attr))
            else:
                calls.setdefault(n.func.attr, []).append((where(n.lineno), True))
        elif isinstance(n, (ast.Attribute, ast.Subscript)) and not isinstance(n.ctx, ast.Load) and root_name(n) == 'BAR':
            stores.append(ast.unparse(n))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ('setattr', 'delattr') and n.args and root_name(n.args[0]) == 'BAR':
            why.append('l.%d %s on %s' % (n.lineno, n.func.id, ast.unparse(n.args[0])))
    want = {'Prep16': [('make_prep', True)], 'Prep': [('make_prep', True)], 'stage_u16': [('run_prep16', True)],
            'stage_c16': [('run_prep16', True)], 'scalars_out': [('run_prep16', True), ('run_prep16', True)]}
    if calls != want:
        why.append('calls %s' % sorted(calls.items()))
    if sorted(stores) != sorted(BAR_STORES_OK):
        why.append('stores rooted at BAR %s' % stores)
    return not why, why


B16_OK, B16_WHY = prep16_bar_check(BARSRC)
RSRC16 = {}
for f_ in RUN_PRODUCERS:
    with open(os.path.join(*f_)) as fh:   # m3_lawcert_c3h_v1_1: pairs
        RSRC16[f_] = fh.read()
rpc = {f_: runner_prep_check(s_) for f_, s_ in RSRC16.items()}
gate('C-PREP16', B16_OK and all(r[0] for r in rpc.values()), '(m3_bar_v11: R(Prep16.stage_u16) and R(Prep16.stage_c16) equal Prep.stage_u '
     'and Prep.stage_c statement by statement once the pinned setup, N2 and cleanup statements are left out, and every stage result is '
     'assigned in exactly those two methods%s; the runner (%s), which made its own preps, builds BAR.Prep16 and BAR.Prep only in make_prep with '
     'stages=(), run stage_u16, stage_c16 and scalars_out only in run_prep16, never stage_u or stage_c, and store into the bar module only %s%s)' % (
         '' if B16_OK else ': ' + '; '.join(B16_WHY[:4]), ', '.join(f_[1] for f_ in RUN_PRODUCERS), ' and '.join(BAR_STORES_OK),
         ''.join('; %s: %s' % (f_[1], '; '.join(r[1][:3])) for f_, r in rpc.items() if not r[0])))
P16_PLANTS = [("R(stage_u16) with T(3) in the 't4|H4|' part", in_place(BARSRC, 'Prep16.stage_u16', "'t4|H4|': T(4) * N2('t4|H4|', lambda: H4)",
                                                                       "'t4|H4|': T(3) * N2('t4|H4|', lambda: H4)")),
              ("stage_c16's nC8 without its factor t", in_place(BARSRC, 'Prep16.stage_c16', "self.nC8 = t * (self.norm16('H1 p8'",
                                                                "self.nC8 = (self.norm16('H1 p8'")),
              ("stage_c16's 'hh p8' at p 6", in_place(BARSRC, 'Prep16.stage_c16', "self.norm16('hh p8', 'c', 8,", "self.norm16('hh p8', 'c', 6,")),
              ('self.rE assigned in Prep16.h2sq', in_place(BARSRC, 'Prep16.h2sq', "        return self.lazy('h2sq',",
                                                           "        self.rE = 0\n        return self.lazy('h2sq',"))]
for lab, mod_ in P16_PLANTS:
    if mod_ is None:
        plant('PLANT-PREP16', False, '(%s: the text to change is not once in its place)' % lab)
        continue
    ok_, why_ = prep16_bar_check(mod_)
    plant('PLANT-PREP16', not ok_, '(%s must be refused: %s)' % (lab, '; '.join(why_)[:120]))
PRUN = RSRC16[(MYD, C3K1F)]   # m3_lawcert_c3k_v2: c3k_1 made the preps
P16CALL = 'd16, log=out, stages=(), scalars=scalars)'
RUN_PLANTS = [("c1's make_prep calling BAR.Prep16 with stages ('u', 'c')",
               PRUN.replace(P16CALL, "d16, log=out, stages=('u', 'c'), scalars=scalars)", 1) if PRUN.count(P16CALL) == 1 else None),
              ('a store BAR.Prep16.stage_c16 = BAR.Prep.stage_c in c1', PRUN + '\nBAR.Prep16.stage_c16 = BAR.Prep.stage_c\n'),
              ("a call of pr.stage_u in c1's run_prep16", PRUN.replace('        pr.stage_u16()\n', '        pr.stage_u(None)\n        pr.stage_u16()\n', 1)
               if PRUN.count('        pr.stage_u16()\n') == 1 else None)]
for lab, mod_ in RUN_PLANTS:
    if mod_ is None:
        plant('PLANT-PREP16', False, '(%s: the text to change is not once in the producer)' % lab)
        continue
    ok_, why_ = runner_prep_check(mod_)
    plant('PLANT-PREP16', not ok_, '(%s must be refused: %s)' % (lab, '; '.join(why_)[:120]))

stage('C-PREP-BAR')
REFLECT = ('setattr', 'delattr', 'vars', 'globals', 'locals', 'exec', 'eval', 'compile', '__import__', 'type')   # m3_lawcert_s9h_v1_1
DUNDER = ('__dict__', '__class__', '__bases__', '__mro__', '__setattr__', '__delattr__', '__init_subclass__', '__subclasses__',
          '__code__', '__defaults__', '__kwdefaults__', '__func__', '__globals__', '__wrapped__')   # m3_lawcert_c3h_v1: + the review N-1's six
PREP_CLASSES = {'Prep': [], 'Prep16': ['Prep']}   # m3_lawcert_c3h_v1: the classes whose methods the gates read, with their allowed bases


def prep_bar_check(src):
    """m3_lawcert_s9h_v1_1's C-PREP-BAR, hardened by the N-1 (3edf8ca2) and extended to Prep16 (m3_lawcert_c3h_v1). In the bar text,
    each class of PREP_CLASSES is defined once, at module level, with exactly its allowed bases and no keywords or decorators; nothing else
    binds or deletes its name (assignment, def, class, argument, import, loop, with, except, global, nonlocal, match or walrus target); its
    name is used only as a class base or as the function of a call <name>.<method>(...), so nothing is stored through it; no attribute
    anywhere is named Prep or Prep16 and nothing is star-imported; every setattr or delattr call is inside a method of one of the classes and
    acts on that method's first parameter; and the text calls none of vars, globals, locals, exec, eval, compile, __import__, type and uses
    none of the attributes in DUNDER. Then each class's methods are the ones in its body."""
    tree = ast.parse(src)
    why = []
    parent = {}
    for p in ast.walk(tree):
        for c in ast.iter_child_nodes(p):
            parent[id(c)] = p
    meth = {}
    for cn, bases in PREP_CLASSES.items():
        defs = [n for n in ast.walk(tree) if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == cn]
        top = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cn]
        if len(defs) != 1 or len(top) != 1:
            why.append('%d definitions of %s, %d at module level' % (len(defs), cn, len(top)))
            continue
        if [ast.unparse(b) for b in top[0].bases] != bases or top[0].keywords or top[0].decorator_list:
            why.append('class %s has bases %s, keywords or decorators' % (cn, [ast.unparse(b) for b in top[0].bases]))
        for m in top[0].body:
            if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and m.args.args:
                meth[id(m)] = m.args.args[0].arg

    def method_of(n):
        p = parent.get(id(n))
        while p is not None and not isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            p = parent.get(id(p))
        return p
    uses, sets = 0, 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id in PREP_CLASSES:
            uses += 1
            p = parent.get(id(n))
            gp = parent.get(id(p)) if p is not None else None
            if not isinstance(n.ctx, ast.Load):
                why.append('l.%d binds or deletes %s' % (n.lineno, n.id))
            elif not ((isinstance(p, ast.ClassDef) and any(b is n for b in p.bases))
                      or (isinstance(p, ast.Attribute) and p.value is n and isinstance(p.ctx, ast.Load) and isinstance(gp, ast.Call) and gp.func is p)):
                why.append('l.%d uses %s other than as a class base or in a call %s.<method>(...)' % (n.lineno, n.id, n.id))
        elif isinstance(n, ast.Attribute) and n.attr in PREP_CLASSES:
            why.append('l.%d an attribute named %s' % (n.lineno, n.attr))
        elif isinstance(n, ast.arg) and n.arg in PREP_CLASSES:
            why.append('l.%d an argument named %s' % (n.lineno, n.arg))
        elif isinstance(n, ast.alias) and (n.name == '*' or (n.asname or n.name).split('.')[0] in PREP_CLASSES):
            why.append('a star import' if n.name == '*' else 'an import binds %s' % (n.asname or n.name))
        elif isinstance(n, ast.ExceptHandler) and n.name in PREP_CLASSES:
            why.append('l.%d an except clause binds %s' % (n.lineno, n.name))
        elif isinstance(n, (ast.Global, ast.Nonlocal)) and set(n.names) & set(PREP_CLASSES):
            why.append('l.%d declares %s global or nonlocal' % (n.lineno, sorted(set(n.names) & set(PREP_CLASSES))))
        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name in PREP_CLASSES:
            why.append('l.%d a match pattern binds %s' % (n.lineno, n.name))
        elif isinstance(n, ast.MatchMapping) and n.rest in PREP_CLASSES:
            why.append('l.%d a match pattern binds %s' % (n.lineno, n.rest))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in REFLECT:
            if n.func.id in ('setattr', 'delattr'):
                sets += 1
                fm = method_of(n)
                if not (fm is not None and id(fm) in meth and n.args and isinstance(n.args[0], ast.Name) and n.args[0].id == meth[id(fm)]):
                    why.append('l.%d %s outside a method of %s or not on its first parameter' % (n.lineno, n.func.id, '/'.join(PREP_CLASSES)))
            else:
                why.append('l.%d calls %s' % (n.lineno, n.func.id))
        elif isinstance(n, ast.Attribute) and n.attr in DUNDER:
            why.append('l.%d uses %s' % (n.lineno, n.attr))
    if why:
        return False, '; '.join(why[:4])
    return True, ('classes %s at module level with bases %s; %d uses of their names, each a class base or a call <name>.<method>(...); no '
                  'attribute named Prep or Prep16, no star import; %d setattr/delattr calls, each in a method of theirs on its first '
                  'parameter; no other binding and no other reflection' % (
                      ', '.join(PREP_CLASSES), ', '.join('%s %s' % kv for kv in PREP_CLASSES.items()), uses, sets))


pb_ok, pb_why = prep_bar_check(BARSRC)
gate('C-PREP-BAR', pb_ok, '(m3_bar_v11, the premises of C-LAW-REM\'s and C-PREP16\'s reading of classes Prep and Prep16, with the %s)' % pb_why)
BAR_PLANTS = [('Prep = Prep16 at module level', BARSRC + '\nPrep = Prep16\n'),
              ('an attribute of Prep assigned', BARSRC + '\nPrep.stage_c = None\n'),
              ('setattr on Prep', BARSRC + "\nsetattr(Prep, 'bound', None)\n"),
              ('a base for class Prep', BARSRC.replace('\nclass Prep:\n', '\nclass Prep(object):\n') if BARSRC.count('\nclass Prep:\n') == 1 else None),
              ('globals() rebinding Prep', BARSRC + "\nglobals()['Prep'] = Prep16\n"),
              ('an alias of Prep', BARSRC + '\n_P = Prep\n'),
              ('the module attribute Prep rebound through a self-import (N-1)', BARSRC + '\nimport m3_bar as _mb\n_mb.Prep = Prep16\n'),
              ('a star import (N-1)', BARSRC + '\nfrom m3_scal import *\n'),
              ("a method's code replaced through Prep.<method> (N-1)", BARSRC + '\nPrep.stage_c.__code__ = Prep16.stage_c16.__code__\n'),
              ('setattr on a parameter named self outside the classes (N-1)', BARSRC + "\n\ndef _f(self):\n    setattr(self, 'rE', 0)\n"),
              ('Prep16 = Prep at module level', BARSRC + '\nPrep16 = Prep\n'),
              ('a second base for class Prep16', BARSRC.replace('\nclass Prep16(Prep):\n', '\nclass Prep16(Prep, object):\n')
               if BARSRC.count('\nclass Prep16(Prep):\n') == 1 else None)]
for lab, mod_ in BAR_PLANTS:
    if mod_ is None:
        plant('PLANT-PREP-BAR', False, '(%s: the text to change is not once in the bar)' % lab)
        continue
    ok_, why_ = prep_bar_check(mod_)
    plant('PLANT-PREP-BAR', not ok_, '(%s must be refused: %s)' % (lab, why_[:120]))

stage('C-LAW-SHAPE')
SRC = {'bar': BARSRC}
for k_, p_ in (('scal', os.path.join(OWN, 'm3_scal_v2.py')), ('run', os.path.join(MYD, RUNF)), ('rec', os.path.join(OWN, 'm3_record_v4.py'))):
    with open(p_) as fh:   # m3_lawcert_c3h_v1: the c3h runner's law texts
        SRC[k_] = fh.read()
SHAPES = [('bar:sup_F', 'bar', 'sup_F', 'fn'), ('bar:Prep.norm_any', 'bar', 'Prep.norm_any', 'fn'),
          ('scal:chi_tail_up', 'scal', 'chi_tail_up', 'fn'), ('scal:ive1', 'scal', 'ive1', 'fn'), ('scal:logtree', 'scal', 'logtree', 'fn'),
          ('scal:logmain', 'scal', 'logmain', 'fn'), ('scal:far_base', 'scal', 'far_base', 'fn'), ('run:laws_of', 'run', 'laws_of', 'fn'),
          ('rec:entry_record', 'rec', 'entry_record', 'fn'), ('bar:Prep.UK', 'bar', 'Prep', 'cls'), ('bar:Prep.CK', 'bar', 'Prep', 'cls'),
          ('run:compute_entry:laws', 'run', 'compute_entry', 'st')]
SHAPES += [(k, 'bar', 'Prep.__init__', 'st') for k in ('bar:Prep.__init__:t', 'bar:Prep.__init__:tloc', 'bar:Prep.__init__:rates', 'bar:Prep.__init__:ratesp', 'bar:Prep.__init__:tilt_c',
                                                        'bar:Prep.__init__:tilt_p', 'bar:Prep.__init__:restore')]
SHAPES += [(k, 'bar', 'Prep.stage_c', 'st') for k in ('bar:Prep.stage_c:n_', 'bar:Prep.stage_c:Pout', 'bar:Prep.stage_c:Pout_p',
                                                       'bar:Prep.stage_c:farbase', 'bar:Prep.stage_c:alpha_lo')]
SHAPES += [(k, 'bar', 'Prep.bound', 'st') for k in ('bar:Prep.bound:l2', 'bar:Prep.bound:B_tail', 'bar:Prep.bound:nF0p', 'bar:Prep.bound:B_ann',
                                                     'bar:Prep.bound:supF', 'bar:Prep.bound:B_far', 'bar:Prep.bound:return')]
SHAPES += [('bar:' + p, 'bar', p, 'fn') for p in ('Prep16.lazy', 'Prep16.h', 'Prep16.hh16', 'Prep16.h2sq', 'Prep16.norm16')]   # m3_lawcert_c3h_v1
SHAPES += [('bar:Prep.stage_u:setup', 'bar', 'Prep.stage_u', 'st'), ('bar:Prep.stage_c:setup', 'bar', 'Prep.stage_c', 'st'),
           ('bar:Prep16.stage_u16:N2', 'bar', 'Prep16.stage_u16', 'st'), ('bar:Prep16.stage_u16:cleanup', 'bar', 'Prep16.stage_u16', 'st'),
           ('bar:Prep16.stage_c16:setup', 'bar', 'Prep16.stage_c16', 'st'),
           ('bar:Prep16.stage_c16:cleanup', 'bar', 'Prep16.stage_c16', 'st')]   # m3_lawcert_c3h_v1: the statements C-PREP16 leaves out


def shape_misses(srcs):
    """the pins of SHAPES that are not, as ASTs, in their named places of the given source texts."""
    trees = {k: ast.parse(v) for k, v in srcs.items()}
    miss_ = []
    for key, fk, place, kind in SHAPES:
        try:
            node = find_node(trees[fk], place)
        except Refuse:
            miss_.append(key)
            continue
        pins_ = pin_stmts(key)
        if kind == 'fn':
            ok_ = len(pins_) == 1 and ast.dump(pins_[0]) == ast.dump(node)
        else:
            have = set(ast.dump(s) for s in (node.body if kind == 'cls' else stmts_in(node)))
            ok_ = all(ast.dump(s) in have for s in pins_)
        if not ok_:
            miss_.append(key)
    return miss_


sm = shape_misses(SRC)
gate('C-LAW-SHAPE', not sm, '(%d pinned texts of m3_lawcert_c3h_v1_pins, as ASTs, in their places: the tail, ann and far statements, sup_F, '
     'norm_any, chi_tail_up, ive1, logtree, logmain, far_base, the bound\'s return, Prep.UK/CK, __init__\'s t, rates, tilts and restore, '
     'laws_of, compute_entry\'s law lines, entry_record, Prep16\'s lazy, h, hh16, h2sq and norm16, and the statements C-PREP16 leaves out)%s' % (len(SHAPES), (': missing ' + ', '.join(sm)) if sm else ''))
for lab, fk, old, new in (('B_tail without sqrt_nn', 'bar', 'B_tail = l2 * S.sqrt_nn(self.Pout)', 'B_tail = l2 * self.Pout'),
                          ('alpha_lo taking .b', 'bar', '/ (2 * gv)).a for gv in g.Gvv)', '/ (2 * gv)).b for gv in g.Gvv)'),
                          ("sup_F's m_F without '- i'", 'bar', 'mx = max(mx, len(mono) - i)', 'mx = max(mx, len(mono))')):
    mod_ = in_place(SRC[fk], 'Prep.stage_c', old, new) if lab == 'alpha_lo taking .b' else (SRC[fk].replace(old, new) if SRC[fk].count(old) == 1 else None)
    if mod_ is None:   # m3_lawcert_s9h_v1: the alpha_lo text has a second copy in Prep16.stage_c16, so it changes inside Prep.stage_c only
        plant('PLANT-LAW-SHAPE', False, '(%s: the text to change is not once in its place)' % lab)
        continue
    plant('PLANT-LAW-SHAPE', bool(shape_misses(dict(SRC, **{fk: mod_}))), '(%s must be missed)' % lab)
if STATIC:   # m3_lawcert_s9h_v1: the static item ends here (no records, no certificate)
    out('STATIC item: C-HASH on the static pins, C-LAW-REM, C-PREP16, C-PREP-BAR and C-LAW-SHAPE; no records, no certificate')
    finish()
    sys.exit(0 if not (FAILS or NOFIRE) else 1)

# ------------------------------------------------------------------ C-LAWFIELDS and C-MONO-FAR: the independent recompute
# ------------------------------------------------------------------ C-NO-RESUME (m3_lawcert_s9h_v1_1)
stage('C-NO-RESUME')
ITEM_RE_WANT = r'(F4Da|F4Na[1-4]|(F4D|F4N)k[1-9]|F4Nr[12]|asm)\.(4|3)'   # m3_lawcert_c3k_v2: the runner's item grammar
RESUME_WANT = ('E4N',)   # m3_lawcert_c3k_v1: the resume items E4Nr1 and E4Nr2 (C-RESUME's checks; their hand-offs hold no entry)
PS_RE = re.compile(r'PIECE-START (\S+) piece ([0-9]+) resumes at entry ([0-9]+)(?: with ([0-9]+) units of (\S+) restored)? after ([0-9]+) capped '
                   r'piece\(s\); stop factor [0-9]+\.[0-9]+(?:; hand-off (\S+) sha256 ([0-9a-f]{64}))?')   # m3_lawcert_c3k_v2: the hand-off read
CP_RE = re.compile(r'C-PIECE \((\S+) piece ([0-9]+): entries ([0-9]+)\.\.(-?[0-9]+) of ([0-9]+) done, next ([0-9]+); [0-9]+ units computed'
                   r'(?:, ([0-9]+) units of (\S+) carried)?\) -> PASS')
AP_RE = re.compile(r'C-PIECES \((\S+)k([0-9]+)\.([34]): entries ([0-9]+)\.\.(-?[0-9]+) complete(?:, ([0-9]+) units of (\S+) carried)?\) -> PASS')


def module_const(src, name):
    """the literal value of a name that a text binds exactly once, by a module-level assignment; None otherwise."""
    tree = ast.parse(src)
    stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == name and not isinstance(n.ctx, ast.Load)]
    top = [n for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
           and n.targets[0].id == name]
    if len(stores) != 1 or len(top) != 1:
        return None
    try:
        return ast.literal_eval(top[0].value)
    except ValueError:
        return None


def walk_reads(runsrc):
    """m3_lawcert_c3h_v1: the failed checks of 'the records' entries come from entry pieces only' on a runner text: every read_handoff call
    in walk_pieces reads an entry piece ('%sk%d.%d' % ...); run_asm binds res once, to an empty dict, by a direct statement; and in run_asm
    and rep_checks the name res is never stored through, never the object of an attribute and passed to no call but walk_pieces and
    rep_checks."""
    tree = ast.parse(runsrc)
    bad = []
    rh = [n for n in ast.walk(find_node(tree, 'walk_pieces')) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'read_handoff']
    if not rh or any(not (n.args and isinstance(n.args[0], ast.BinOp) and isinstance(n.args[0].op, ast.Mod) and isinstance(n.args[0].left, ast.Constant)
                          and n.args[0].left.value == '%sk%d.%d') for n in rh):
        bad.append('runner:walk-reads')
    br = bindings(find_node(tree, 'run_asm')).get('res', [])
    if len(br) != 1 or not br[0][1] or not (isinstance(br[0][0], ast.Dict) and not br[0][0].keys):
        bad.append('runner:asm-res-binding')
    for fname in ('run_asm', 'rep_checks'):
        fn = find_node(tree, fname)
        par_ = {}
        for p in ast.walk(fn):
            for c in ast.iter_child_nodes(p):
                par_[id(c)] = p
        for n in ast.walk(fn):
            if not (isinstance(n, ast.Name) and n.id == 'res'):
                continue
            p = par_.get(id(n))
            if isinstance(p, ast.Subscript) and p.value is n and not isinstance(p.ctx, ast.Load):
                bad.append('runner:%s-res-store' % fname)
            elif isinstance(p, ast.Attribute) and p.value is n:
                bad.append('runner:%s-res-method' % fname)
            elif isinstance(p, ast.keyword) or (isinstance(p, ast.Call) and any(a is n for a in p.args)
                                                and not (isinstance(p.func, ast.Name) and p.func.id in ('walk_pieces', 'rep_checks'))):
                bad.append('runner:%s-res-passed' % fname)
    return sorted(set(bad))


def no_resume_check(runsrc, asm_lines, pieces, man):
    """m3_lawcert_c3h_v1's C-NO-RESUME review, adapted to multi-piece chains (m3_lawcert_c3k_v1): no checkpoint state seeded the group
    cache of a record of this N. The runner's only resume items are E4Nr1 and E4Nr2 (ITEM_RE and RESUME_FAMS exactly as above), C-RESUME's
    checks, whose hand-offs hold no entry; the records' entries come from entry pieces only (walk_reads); and per family the chain k1..k_last is
    whole: the asm's piece lines cover entries 0..m-1 contiguously in k order, with the cover line once; every piece output names the runner's
    sha256 and starts at the entry where the previous non-capped piece stopped, with exactly the units that piece carried, after the count of
    capped pieces just before it; a capped piece (absent from the asm's piece lines) ends VERDICT INCOMPLETE (CAP-STOP) with a CAP-STOP line and
    has no hand-off; every other piece ends VERDICT VALID, its C-PIECE line equals the asm's line, and it names its hand-off by sha256; outputs and
    hand-offs are rows of the pinned run manifest; no piece output follows the last. Returns (ok, the failed checks as 'family:check')."""
    bad = []
    if module_const(runsrc, 'ITEM_RE') != ITEM_RE_WANT:
        bad.append('runner:ITEM_RE')
    if module_const(runsrc, 'RESUME_FAMS') != RESUME_WANT:
        bad.append('runner:RESUME_FAMS')
    try:
        bad += walk_reads(runsrc)
    except Refuse as ex:
        bad.append('runner:walk-reads (%s)' % ex)
    for f in FAMS:
        m_f = len(LKEYS[f])
        apl = [AP_RE.fullmatch(ln) for ln in asm_lines if ln.startswith('C-PIECES (%sk' % EPFX[f])]   # m3_lawcert_c3k_v2: EPFX
        if not apl or any(m is None or m.group(1) != EPFX[f] or int(m.group(3)) != NN for m in apl):
            bad.append('%s:asm-pieces' % f)
            continue
        if asm_lines.count('C-PIECES (the %s pieces cover all %d %s entries, in order, none left in progress) -> PASS' % (f, m_f, f)) != 1:
            bad.append('%s:asm-cover' % f)
        ak = [int(m.group(2)) for m in apl]
        if ak != sorted(set(ak)):
            bad.append('%s:asm-order' % f)
        nxt = 0
        for m in apl:
            s, e = int(m.group(4)), int(m.group(5))
            if s != nxt:
                bad.append('%s:asm-gap' % f)
            nxt = e + 1 if e >= s else nxt
        if nxt != m_f:
            bad.append('%s:asm-end' % f)
        klast = ak[-1]
        if sorted(pieces[f]) != list(range(1, klast + 1)):
            bad.append('%s:piece-set' % f)
        asm_by_k = dict((int(m.group(2)), m) for m in apl)
        capped, nxt, carry, prevj = 0, 0, None, None   # m3_lawcert_c3k_v2: prevj, the last valid piece
        for k in range(1, klast + 1):
            lines = pieces[f].get(k, b'').decode().split('\n')
            hand = 'm3_run_v1_9_3_%sk%d.%d.json' % (EPFX[f], k, NN)
            hpath = os.path.join(HANDD, hand)
            opath = os.path.join(OUTD, 'm3_run_v1_9_3_%sk%d.%d.out' % (EPFX[f], k, NN))
            if not (lines[0].startswith('m3_run_v1_9_3 item %sk%d.%d LIM ' % (EPFX[f], k, NN)) and ('; script sha256 %s;' % RUNSHA) in lines[0]):
                bad.append('%s:k%d:header' % (f, k))
            ps = [PS_RE.fullmatch(ln) for ln in lines if ln.startswith('PIECE-START')]
            p0 = ps[0] if len(ps) == 1 else None
            rest = None if p0 is None or p0.group(4) is None else (int(p0.group(4)), p0.group(5))
            if not (p0 is not None and p0.group(1) == f and int(p0.group(2)) == k and int(p0.group(3)) == nxt and int(p0.group(6)) == capped
                    and rest == carry):
                bad.append('%s:k%d:start' % (f, k))
            ph = None if prevj is None else 'm3_run_v1_9_3_%sk%d.%d.json' % (EPFX[f], prevj, NN)   # m3_lawcert_c3k_v2: the note
            phs = None if ph is None or not os.path.exists(os.path.join(HANDD, ph)) else sha(os.path.join(HANDD, ph))
            if not (p0 is not None and (p0.group(7), p0.group(8)) == (ph, phs) and (ph is None or man.get(os.path.join(HANDD, ph)) == phs)):
                bad.append('%s:k%d:start-hand' % (f, k))
            if man.get(opath) != hashlib.sha256(pieces[f].get(k, b'')).hexdigest():
                bad.append('%s:k%d:man-out' % (f, k))
            verd = [ln for ln in lines if ln.startswith('VERDICT')]
            hands = [ln for ln in lines if ln.startswith('HANDOFF ')]
            if k not in asm_by_k:
                if verd != ['VERDICT INCOMPLETE (CAP-STOP)'] or hands or os.path.exists(hpath) or not any(ln.startswith('CAP-STOP ') for ln in lines):
                    bad.append('%s:k%d:capped' % (f, k))
                capped += 1
                continue
            m = asm_by_k[k]
            cps = [CP_RE.fullmatch(ln) for ln in lines if ln.startswith('C-PIECE (')]
            c0 = cps[0] if len(cps) == 1 else None
            if not (c0 is not None and c0.group(1) == f and int(c0.group(2)) == k and c0.group(3) == m.group(4) and c0.group(4) == m.group(5)
                    and int(c0.group(5)) == m_f and (c0.group(7), c0.group(8)) == (m.group(6), m.group(7))):
                bad.append('%s:k%d:piece-line' % (f, k))
            if verd != ['VERDICT VALID']:
                bad.append('%s:k%d:verdict' % (f, k))
            if not (os.path.exists(hpath) and hands == ['HANDOFF %s %s' % (hand, sha(hpath))] and man.get(hpath) == sha(hpath)):
                bad.append('%s:k%d:handoff' % (f, k))
            prevj = k   # m3_lawcert_c3k_v2: the hand-off the next piece must name
            if c0 is not None:
                nxt = int(c0.group(6))
                carry = (int(c0.group(7)), c0.group(8)) if c0.group(7) else None
            capped = 0
        if any(os.path.exists(os.path.join(OUTD, 'm3_run_v1_9_3_%sk%d.%d.out' % (EPFX[f], k, NN))) for k in range(klast + 1, 10)):
            bad.append('%s:later' % f)
    return not bad, bad


with open(ASM) as fh:
    ASM_LINES = fh.read().split('\n')
PIECES = {}
for f in FAMS:
    PIECES[f] = {}
    for k in range(1, 10):
        p_ = os.path.join(OUTD, 'm3_run_v1_9_3_%sk%d.%d.out' % (EPFX[f], k, NN))
        if os.path.exists(p_):
            with open(p_, 'rb') as fh:
                PIECES[f][k] = fh.read()
nr_ok, nr_bad = no_resume_check(RUNSRC, ASM_LINES, PIECES, side)
gate('C-NO-RESUME', nr_ok, '(adapted to multi-piece chains: the runner\'s only resume items are F4Nr1 and F4Nr2 (ITEM_RE; RESUME_FAMS '
     '(\'E4N\',)), whose hand-offs hold no entry, and the records\' entries come from entry pieces only; each family\'s chain k1..k_last is whole '
     '(contiguous entries, units carried exactly into the next piece, capped pieces without hand-offs, the asm\'s lines equal the pieces\' lines, '
     'hand-offs by sha256, no later piece; each PIECE-START names the hand-off it read by sha256); outputs and hand-offs are rows of %s %s: %s, '
     'pieces %s)%s' % (
         os.path.basename(SIDE), PINS_STATIC[SIDEF][:8], ', '.join(FAMS), ', '.join('%s %s' % (f, sorted(PIECES[f])) for f in FAMS),
         (': failed ' + ', '.join(nr_bad)) if nr_bad else ''))
WP_OLD = "        body = read_handoff('%sk%d.%d' % (EPFX[graph], piece, NN), graph)\n"
RS_OLD = "    resume_chain()\n    refs, fins = {}, {}\n"
mid = [ln for ln in ASM_LINES if ln.startswith('C-PIECES (F4Nk')]
gap_lines = [ln for ln in ASM_LINES if ln != mid[len(mid) // 2]]
kr = [k for k in sorted(PIECES['E4N']) if any(ln.startswith(b'PIECE-START') and b' restored after ' in ln for ln in PIECES['E4N'][k].split(b'\n'))]
k_r = kr[0] if kr else None


kh = [k for k in sorted(PIECES['E4N']) if any(ln.startswith(b'PIECE-START') and b'; hand-off ' in ln for ln in PIECES['E4N'][k].split(b'\n'))]
k_h = kh[0] if kh else None   # m3_lawcert_c3k_v2: a piece that names its hand-off


def flip_hand(b):
    """m3_lawcert_c3k_v2: the PIECE-START line's hand-off sha256 with its last digit changed."""
    out_ = []
    for ln in b.split(b'\n'):
        if ln.startswith(b'PIECE-START') and b'; hand-off ' in ln:
            ln = ln[:-1] + (b'0' if ln[-1:] != b'0' else b'1')
        out_.append(ln)
    return b'\n'.join(out_)


def bump_restore(b):
    out_ = []
    done = False
    for ln in b.split(b'\n'):
        if not done and ln.startswith(b'PIECE-START') and b' units of ' in ln:
            pre, post = ln.split(b' with ', 1)
            u, tail = post.split(b' units of ', 1)
            ln = pre + b' with ' + str(int(u) + 1).encode() + b' units of ' + tail
            done = True
        out_.append(ln)
    return b'\n'.join(out_)


NR_PLANTS = [('a resume read in walk_pieces', 'runner:walk-reads',
              (RUNSRC.replace(WP_OLD, "        body = read_handoff('%sr1.%d' % (EPFX[graph], NN), graph)\n", 1) if RUNSRC.count(WP_OLD) == 1 else None,
               ASM_LINES, PIECES)),
             ('a second resume family', 'runner:RESUME_FAMS', (RUNSRC.replace("RESUME_FAMS = ('E4N',)", "RESUME_FAMS = ('E4N', 'E4D')", 1)
                                                               if RUNSRC.count("RESUME_FAMS = ('E4N',)") == 1 else None, ASM_LINES, PIECES)),
             ('a store into res in run_asm', 'runner:run_asm-res-store',
              (RUNSRC.replace(RS_OLD, "    resume_chain()\n    res[('E4N', 'IhR,10,0')] = None\n    refs, fins = {}, {}\n", 1) if RUNSRC.count(RS_OLD) == 1 else None,
               ASM_LINES, PIECES)),
             ('a gap in the asm\'s E4N piece lines', 'E4N:asm-gap', (RUNSRC, gap_lines, PIECES)),
             ('restored units that differ from the previous piece\'s carry', 'E4N:k%s:start' % k_r,
              (RUNSRC, ASM_LINES, dict(PIECES, E4N={**PIECES['E4N'], k_r: bump_restore(PIECES['E4N'][k_r])}) if k_r is not None else None)),
             ('a PIECE-START naming a wrong hand-off sha256', 'E4N:k%s:start-hand' % k_h,   # m3_lawcert_c3k_v2
              (RUNSRC, ASM_LINES, dict(PIECES, E4N={**PIECES['E4N'], k_h: flip_hand(PIECES['E4N'][k_h])}) if k_h is not None else None))]
for lab, want, (rs_, al_, pc_) in NR_PLANTS:
    if rs_ is None or pc_ is None:
        plant('PLANT-NO-RESUME', False, '(%s: the text to change is not once in its place)' % lab)
        continue
    ok_, bad_ = no_resume_check(rs_, al_, pc_, side)
    plant('PLANT-NO-RESUME', not ok_ and want in bad_, '(%s must be refused as %s: failed %s)' % (lab, want, ', '.join(bad_[:6])))

stage('C-LAWFIELDS')
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9symxyp_v1.json', 3: 'ts_N3_S_z9symxyp_v1.json'}[NN]   # m3_lawcert_c3k_v2: z9symxyp, the runner's trial set
TS = ENT.load_trial(os.path.join(PSX, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)


def prepjson(f):
    """m3_lawcert_c3h_v1: the PREPJSON line of the float reference whose radii the record's shared prep took (PREPREF, as the runner's)."""
    fn = PREPREF[f][1] % NN
    with open(os.path.join(PREPREF[f][0], fn)) as fh:
        hits = [json.loads(ln[len('PREPJSON '):]) for ln in fh if ln.startswith('PREPJSON ')]
    if len(hits) != 1:
        raise ValueError('%s: %d PREPJSON lines' % (fn, len(hits)))
    return hits[0]


def own_mF(facs):
    """this script's own J-exponent of sup_F: per factor the largest exponent over its terms, the constant term counting 0 ('p' and a
    nonzero xi constant) and a coefficient of degree d at t^i counting d - i, negative values allowed."""
    m = 0
    for f in facs:
        if f[0] == 'const':
            continue
        if f[0] == 'p':
            ex = [0] + [len(mono) - i for i, coef in ((1, f[2]), (2, f[3]), (3, f[4])) for cb, mono in zip(coef, SER.BASIS9) if cb != 0.0]
        elif f[0] == 'xi':
            ex = ([0] if f[2] != 0.0 else []) + [len(mono) for cb, mono in zip(f[3], SER.BASIS9) if cb != 0.0]
            ex = ex or [0]
        else:
            raise ValueError('factor kind %r' % (f[0],))
        m += max(ex)
    return m


T300 = 1 / S.I(J_REF)
fld_bad, rates, nchk = [], [], 0
for f in FAMS:
    spec = LIST['graphs'][f]
    V_, E_ = GR.strip(spec['columns'])
    g = GR.GraphIV(V_, E_, sorted(tuple(sorted(p)) for p in spec['pairs']), NN)   # m3_lawcert_s9h_v1: as the runner's family_graph
    ents = [e for e in LIST['entries'] if e['graph'] == f]
    fls = [[ENT.factor(TS, 'N', enc) for enc in e['factors']] for e in ents]   # m3_lawcert_c3h_v1: the runner's factors (EDGES 'N', no enc_of)
    rp = prepjson(f)
    if rp['family'] != FAMREF[f] or rp['N'] != NN or rp['J'] != J_REF:
        fld_bad.append('%s: PREPJSON family %r N %r J %r' % (f, rp['family'], rp['N'], rp['J']))
        continue
    ratesp = [S.up(-iv.log(1 - S.I(rp['ap'])) / (2 * S.I(rp['ap'])) * T300)] * g.V
    tp = g.tilted(ratesp)
    if tp is None:
        fld_bad.append('%s: tilt_p not certainly positive definite' % f)
        continue
    tail = [(Fraction(a), Fraction(S.up(gv))) for a, gv in zip(rp['a_v'], g.Gvv)]
    ann = [(Fraction(a), Fraction(S.up(gv))) for a, gv in zip(rp['a_v'], tp['Gvv'])]
    alpha_lo = min((S.I(rp['theta0']) * S.I(rp['ap']) / (2 * gv)).a for gv in g.Gvv)
    for e, facs in zip(ents, fls):
        if e['key'] not in RECS[f]['laws'] or RECS[f]['laws'][e['key']]['parity'] != 'free':
            continue
        nchk += 1
        _, mF = BAR.sup_F(facs, J_REF)
        mo = own_mF(facs)
        cF = mF + Fraction(g.n * (g.V - 1), 2)
        rate = alpha_lo - S.I(cF) / J_REF
        rates.append((S.down(rate), rate.a > 0, '%s:%s' % (f, e['key'])))
        want = {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': J_REF, 'a_G': tail}, 'ann': {'n': g.n, 'J_REF': J_REF, 'a_G': ann},
                'far_rate': Fraction(S.down(rate)), 'far_cF': cF}
        if RECS[f]['laws'][e['key']]['laws'] != want or not mo <= mF:
            fld_bad.append('%s:%s%s' % (f, e['key'], '' if mo <= mF else ' (own m_F %d > %d)' % (mo, mF)))
gate('C-LAWFIELDS', not fld_bad and nchk == nfree, '(%d free entries: rem_tpow 4; tail and ann n, J_REF and a_G from the C3-h list\'s graphs\' G_vv, '
     'tilt_p\'s G_vv and the a_v of the PREPJSON each prep took; far_cF from the pinned sup_F\'s m_F of the runner\'s factors, never below this script\'s own '
     'exponent; far_rate = down(alpha_lo - c_F/300); all exactly equal)%s' % (nchk, (': differ ' + ', '.join(fld_bad[:12])) if fld_bad else ''))
rmin = min(rates) if rates else (0.0, False, '-')
gate('C-MONO-FAR', bool(rates) and all(r[1] for r in rates), '(every recomputed far rate certainly > 0; smallest %.4e at %s)' % (rmin[0], rmin[2]))

# ------------------------------------------------------------------ C-BAND: the banded bound against the uniform err, in arb
stage('C-BAND')
flint.ctx.prec = 128
A = flint.arb


def fa(x):
    x = Fraction(x)
    return A(x.numerator) / A(x.denominator)


def ptail(n, s):
    if n == 2:
        return (-s / 2).exp()
    if n == 3:
        return (s / 2).sqrt().erfc() + (2 * s / A.pi()).sqrt() * (-s / 2).exp()
    raise ValueError('n %r' % n)


def psum(J, part):
    return sum((ptail(part['n'], A(J) * fa(a) / fa(G)) for a, G in part['a_G']), A(0))


def banded(d, J):
    L, P = d['laws'], d['parts']
    q = A(J_REF) / A(J)
    t = A(1) / A(J)
    out_ = fa(P['rem']) * q * q * q * q
    out_ += fa(P['tail']) * (psum(J, L['tail']) / psum(J_REF, L['tail'])).sqrt()
    out_ += fa(P['ann']) * (psum(J, L['ann']) / psum(J_REF, L['ann'])).sqrt()
    out_ += fa(P['far']) * (-fa(L['far_rate']) * (J - J_REF)).exp()
    tk = A(1)
    for r in d['ak_rad']:
        out_ += fa(r) * tk
        tk = tk * t
    return out_.upper()


JS = (300, 600, 1000, 3000)
band_bad, worst = [], {J: 0.0 for J in JS}
for f in FAMS:
    for k, d in RECS[f]['laws'].items():
        if d['parity'] != 'free':
            continue
        bs = [banded(d, J) for J in JS]
        err = fa(d['err'])
        okb = bool(bs[0] <= err * (1 + A(1) / A(2 ** 30))) and all(bool(b <= err) for b in bs[1:]) and all(bool(bs[i + 1] <= bs[i]) for i in range(len(bs) - 1))
        if not okb:
            band_bad.append('%s:%s' % (f, k))
        for J, b in zip(JS, bs):
            worst[J] = max(worst[J], float(b / err))
gate('C-BAND', not band_bad, '(sanity, %d free entries: the banded bound in arb at J = %s is <= err (1 + 2^-30) at 300, <= err beyond and '
     'non-increasing; largest banded/err: %s)%s' % (nfree, ', '.join(map(str, JS)), ', '.join('J %d %.4f' % (J, worst[J]) for J in JS),
                                                   (': ' + ', '.join(band_bad[:12])) if band_bad else ''))
for f in FAMS:
    fr_ = [d for d in RECS[f]['laws'].values() if d['parity'] == 'free']
    if fr_:
        out('BAND-INFO %s: %d free entries; largest banded/err at J = 600 %.4f, at J = 1000 %.4f' % (
            f, len(fr_), max(float(banded(d, 600) / fa(d['err'])) for d in fr_), max(float(banded(d, 1000) / fa(d['err'])) for d in fr_)))

# ------------------------------------------------------------------ the certificate, C-LAWCERT-RT and its plants
stage('C-LAWCERT-RT')
NAME = 'm3_lawcert_c3k_v2_N%d.json' % NN


def exact_laws(L):
    return {'rem_tpow': 4, 'tail': {'n': L['tail']['n'], 'J_REF': J_REF, 'a_G': [[str(a), str(G)] for a, G in L['tail']['a_G']]},
            'ann': {'n': L['ann']['n'], 'J_REF': J_REF, 'a_G': [[str(a), str(G)] for a, G in L['ann']['a_G']]},
            'far_rate': str(L['far_rate']), 'far_cF': str(L['far_cF'])}


CERT = {'format': FORMAT, 'claim': CLAIM, 'J_REF': J_REF, 'N': NN,
        'records': {f: {'file': RECS[f]['name'], 'sha256': RECS[f]['sha256']} for f in FAMS},
        'asm': {'file': os.path.basename(ASM), 'sha256': sha(ASM)}, 'entries': {}}
for f in FAMS:
    for k, d in RECS[f]['laws'].items():
        CERT['entries']['%s:%s' % (f, k)] = ({'parity': 'zero', 'law_claim': None, 'laws': None} if d['parity'] == 'zero' else
                                            {'parity': 'free', 'law_claim': CLAIM, 'laws': exact_laws(d['laws'])})


def dumps(c):
    return json.dumps(c, sort_keys=True, indent=1) + '\n'


def sim_out(text, verdict='VERDICT VALID'):
    return '%s\nRECORD %s %s\n' % (verdict, NAME, tsha(text))


TEXT = dumps(CERT)
try:
    RDR._bound(NAME, TEXT.encode(), sim_out(TEXT))   # m3_lawcert_s9h_v1: m3_reader_v6_3's checks without the producer pin
    back = RDR._parse_lawcert(json.loads(TEXT), NAME, J_REF, NN, RECS)
    rt_ok = len(back['entries']) == len(CERT['entries']) and all(back['entries']['%s:%s' % (f, k)]['laws'] == d['laws']
                                                                for f in FAMS for k, d in RECS[f]['laws'].items())
    rt_why = '%d entries back with the records\' laws' % len(back['entries'])
except ValueError as ex:
    rt_ok, rt_why = False, 'refused: %s' % str(ex)[:200]
gate('C-LAWCERT-RT', rt_ok and CLAIM == RDR.LAWCERT_CLAIM and FORMAT == RDR.LAWCERT_FORMAT,
     '(the certificate through m3_reader_v6_3\'s _bound and _parse_lawcert against the two loaded records: %s; claim and format equal the '
     'reader\'s)' % rt_why)
F0 = [eid for eid in sorted(CERT['entries']) if CERT['entries'][eid]['parity'] == 'free'][0]


def refused(mut, verdict='VERDICT VALID'):
    c2 = copy.deepcopy(CERT)
    mut(c2)
    t2 = dumps(c2)
    try:
        RDR._bound(NAME, t2.encode(), sim_out(t2, verdict))   # m3_lawcert_s9h_v1
        RDR._parse_lawcert(json.loads(t2), NAME, J_REF, NN, RECS)
        return False
    except ValueError:
        return True


def setl(path, val):
    def mut(c):
        node = c['entries'][F0]['laws']
        for p in path[:-1]:
            node = node[p]
        node[path[-1]] = val
    return mut


CERT_PLANTS = [('rem_tpow 3', setl(['rem_tpow'], 3)), ('far_rate 0', setl(['far_rate'], '0')),
               ('an a_G entry 0', lambda c: c['entries'][F0]['laws']['tail']['a_G'][0].__setitem__(0, '0')),
               ('J_REF 299', lambda c: c.__setitem__('J_REF', 299)), ('n 4', setl(['tail', 'n'], 4)),
               ('a record sha changed', lambda c: c['records']['E4N'].__setitem__('sha256', flip(c['records']['E4N']['sha256']))),
               ('an entry dropped', lambda c: c['entries'].pop(F0)),
               ('an entry added', lambda c: c['entries'].__setitem__('E4N:ZZZ', copy.deepcopy(c['entries'][F0]))),
               ("law_claim + ' '", lambda c: c['entries'][F0].__setitem__('law_claim', CLAIM + ' ')),
               ('a records map without one loaded record', lambda c: c['records'].pop('E4N')),
               ('a non-canonical exact string', setl(['far_rate'], str(Fraction(CERT['entries'][F0]['laws']['far_rate'])) + '0/10'))]
for lab, mut in CERT_PLANTS:
    plant('PLANT-LAWCERT', refused(mut), '(%s must be refused)' % lab)
plant('PLANT-LAWCERT', refused(lambda c: None, 'VERDICT VALID-PRECERT'), '(a writing job whose VERDICT line is VERDICT VALID-PRECERT must be refused)')

# ------------------------------------------------------------------ the write, after every gate and plant
if FAILS or NOFIRE:
    out('NO-WRITE %s: a gate failed or a plant did not fire' % NAME)
else:
    path = os.path.join(OUTD, NAME)
    with open(path, 'x') as fh:
        fh.write(TEXT)
    with open(path, 'rb') as fh:
        gate('C-WRITE', fh.read() == TEXT.encode(), '(%s re-read byte for byte)' % NAME)
    out('RECORD %s %s' % (NAME, tsha(TEXT)))
finish()
