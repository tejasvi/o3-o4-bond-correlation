# KT_MR_ASSEMBLY_v1_8_4: engine v1_8_4 = v1_7_1 with the tail section (v1_8_1) and the bundle (X_DEFINITION, the producer orientation line and anchors, the Way B floors, route (v)), one code pass for the reviewers (pk24)

Notes on the engine (code, formulas and the tail check). The row 4359 merges the engine
reviews into one pass from v1_7_1 (pk24/KT_MR_ASSEMBLY_v1_7_1_NOTE.md, 8e50b08e) to this version, the
bundle first and the tail second; the tail section is v1_8_1's (pk24/KT_MR_ASSEMBLY_v1_8_1_NOTE.md, 6c0314cc,
sect. 2). The formulas are G6 v1_6_2's (pk24/MIDROW_G6_SPEC_v1_6_2.md, 1e570ab7, issued with this note).
Written 2026-11-21T11:21:16Z by the assembler. Paths
are relative to code/. Every number below is in the tool lines of sect. 6 and is [float] on stand-ins.

## 0. Answer first
- **Review target:** pk24/mr_engine/kt_mr_assembly_v1_8_4.py (abd48b2c) and
  pk24/mr_engine/mr_merge_v1_8_4.py (03110277). Diffs against v1_7_1: mr_engine/out/udiff_engine_tmpl_v1_7_1_v1_8_4.txt
  (6552ac82) and udiff_merge_tmpl_v1_7_1_v1_8_4.txt
  (9dcd3c7c).
- **The bundle** (the rows 4320, 4325, 4335, 4340, 4376; sect. 2): X_DEFINITION checked by G-PIN; ORIENT_CHECK on MR_SPECTRAL, MR_INSERT
  and MR_EXACT, checked with the grid's piece counts; the anchors c_y(-1) > 0 and MR_INSERT's t^0 signs; the Way B floors (G-FLOOR, G-FACTX
  with floors, the factored fallback); route (v)'s Pe_hi with the m = 1 min form; the v1_7 N-1 wording and N-2 count; five plants.
- **The tail** (sect. 3): v1_8_1's section, unchanged, with two printed lines per N for the check: C-TAILMONO OK and TAIL SUP.
- **Rows:** without Pe_hi and floors every row is v1_7_1's (five record sets); the tail rows are v1_8_1's at (3, 3) and (2, 5); with Pe_hi the
  rows equal the diagnostic engine's that the batch used; a floor behaves as G6 v1_6_2 states.
- **Superseded builds, never sent:** v1_8 (main reused the name tail), v1_8_2 (the tail's h envelope kept xc -+ s on a floor piece, so
  C-TAILMONO stopped there), v1_8_3 (C-TAILMONO had no OK line).

## 1. Files and diffs
- Makers: tools/make_mrtemplates_v1_8_2.py (the bundle, from v1_8_1's templates), make_mrtemplates_v1_8_3.py (the floor fix),
  make_mrtemplates_v1_8_4.py (the two lines), each by exact replacements with counts; tools/make_mrengine_v1_8_4.py fills the pins.
- Step diffs: udiff_engine_tmpl_v1_8_1_v1_8_2.txt (fd67c289),
  udiff_engine_tmpl_v1_8_2_v1_8_3.txt (ca76f2a5), udiff_engine_tmpl_v1_8_3_v1_8_4.txt
  (17da4a1a), and the merge's.
- tools/upgrade_set_v1.py (e1c3ddd9) copies an older record set into the v1_8_4 form (ORIENT_CHECK; in v4
  X_DEFINITION and zero floors; optionally Pe_hi from the model); the regressions run on those copies (folder mr_engine/v36).

## 2. The bundle
- **v4's final fields:** MR_INSERT = v3 + xc_lo xc_hi xf_hi; MR_EXACT = v3 + Axc_lo Axc_hi Axf_hi. MR_EXACT may end with Pe_hi (v3 or v4).
- **G-PIN:** X_DEFINITION (XDEF, exactly G6 v1_6_2 sect. 6) on v4 MR_INSERT and MR_EXACT; ORIENT_CHECK (ORIENT_RX) on MR_SPECTRAL, MR_INSERT and
  MR_EXACT, whose counts G-UNIF compares with the grid; the FIELDS check accepts MR_EXACT with a trailing Pe_hi.
- **C-ORIENT:** v1_7_1's checks plus c_y(-1) > 0 on every MR_SPECTRAL row, t and a v_x > 0 and h, t and a v_y > 0 on every MR_INSERT row.
- **G-FLOOR / G-FACTX:** a floor is >= 0 and nonzero only on the last piece and only on a power-1 row (h); t xc -+ floor inside the
  amplitude at both piece ends.
- **Factored fallback:** alpha_h gives [-1, 1] on a floor row (crude ends by MR_INSERT's xf_hi, exact h ends by Axf_hi), so the sign is
  not certified and X takes v1_6's form; the run prints FACTORED SIGN FALLBACK with the count review. In the tail, the h envelope's
  coefficient is [-1, 1] on such a piece too (the v1_8_3 fix), so C-TAILMONO passes and (c) fails there.
- **Route (v):** an exact end's |P_e a| is Pe_hi when given; the m = 1 rest then takes the least product over the ends that give |P_e a|; the
  output's ROUTE_V line says on or off and the merge requires it to agree.
- **Plants:** YORIENT, IORIENT (C-ORIENT), OCHK, XDEF (G-PIN), FLOOR (G-FLOOR), all stops.

## 3. The tail and the requests
- Unchanged from v1_8_1 except the floor fix of sect. 2. Per N the run now prints:
  - C-TAILMONO OK: the pieces, the conditions s_x, s_y, tau, rho_1, env_r < 1, and the d values the envelope was checked to enclose
    (D0..D0 + 12, D_MAX, D_MAX + 1);
  - TAIL SUP: the least and largest sup over d >= D0 of e-hat(d) over the pieces, which enters h's envelope as the coefficient xc -+ sup
    and the x amplitude v_x -+ t_hi sup (tail_piece in the engine: sup is the largest of the rows D0..D_MAX and the envelope row at
    max(D0, D_MAX + 1)).
- The (2, 5) design run's lines (envelope-class margins, the m-tail at M0, Proposition J's envelope orbits, C-TAILMONO OK, TAIL SUP) are in
  sect. 6 from job194.

## 4. Tests (job194; jobs 192 and 193 are the superseded builds' runs)
- Regressions against v1_7_1's rows on the upgraded copies: v3 factored-hull, v3 split, v4 split, a0 (1732 rows each) and v4 factored to n = 20
  (5564 rows): 0 differing.
- The tail at (3, 3) and (2, 5) on the CW + A0E set: rows and tail rows equal to v1_8_1's.
- Plants: v1_7_1's 17, the three tail plants and the five new ones, all FIRED.
- Negatives: a v4 set in v1_8_1's layout and a v3 set without ORIENT_CHECK stop at G-PIN; TAIL on a split set and NMAX below n0 stop at G-TAIL.
- Route (v): on the upgraded real-dry-input set with Pe_hi, 0 rows differ from the diagnostic engine's; on the v4 stand-ins with Pe_hi
  only m = 1 rows change, none for the worse.
- Floor: a floor of 1e-10 on the last piece passes G-FACTX, makes 276 class-piece evaluations fall back, keeps the finite rows at FAIL 0 and
  fails the tail's (c) on that piece at both N.

## 5. Review packet
- the review (code, one pass from v1_7_1): this note, the two diffs against v1_7_1, the step diffs, job194's script and console. The v1_8_1
  points the review listed (margin() and end_tuple() with rows unchanged, sb_piece(), end(env=True), tail_piece(), G-TAIL, the plant-aware
  except, OUT.tail, M-TAIL and the tail C-MERGE) are in the v1_7_1 diff.
- the review (formulas and the tail check): sect. 2's gates against G6 v1_6_2 sect. 0f, 3 and 6; sect. 3 against G6 v1_6_2 sect. 5b.

## 6. Tool lines (selected)
pk24/jobs/job194_v1_8_4.console (sha8 2ac4c792):
  l.26 UDIFF OUT 17da4a1adfaddcf88d77d6aaab7d12a75fc6b089cfa560515acc7ca38add0464 /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_engine_tmpl_v1_8_3_v1_8_4.txt: 22 lines added, 10 removed
  l.27 UDIFF OUT 33b752a1cd6d0f1e67e2cbb3d55f9ad3cbcc296e99ace6b568826239812ae86b /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_merge_tmpl_v1_8_3_v1_8_4.txt: 14 lines added, 13 removed
  l.28 UDIFF OUT 6552ac82f2730230d4712700587909863bb9f71f8ab01b4157d6d9d1b071196f /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_engine_tmpl_v1_7_1_v1_8_4.txt: 403 lines added, 90 removed
  l.29 UDIFF OUT 9dcd3c7c9d5819ffdf4a49e23023792b6cb42dae7d4350e4e1fdf8da1fedec49 /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_merge_tmpl_v1_7_1_v1_8_4.txt: 85 lines added, 15 removed
  l.32 REGRESSION v1_8_4 v3f against v1_7_1: rows 1732, rows differing 0
  l.35 REGRESSION v1_8_4 v3s against v1_7_1: rows 1732, rows differing 0
  l.38 REGRESSION v1_8_4 v4s against v1_7_1: rows 1732, rows differing 0
  l.41 REGRESSION v1_8_4 v4f against v1_7_1: rows 5564, rows differing 0
  l.44 REGRESSION v1_8_4 a0 against v1_7_1: rows 1732, rows differing 0
  l.46 TAIL N=4 D0 3 M0 3: envelope classes 45 per piece, FAIL 0, least L 7.479874e-05 at h-1-aD0+/m2 (piece 0); m-tail at M0: FAIL 0, least lower end 2.572431e-02 (pair h-a, piece 0), q_R <= 0.6347, q_T <= 0.4886; sign condition (c): FAIL on 0 pieces; Proposition J envelope orbits: FAIL 0, least L_J 6.738028e-02 (d_R 0, piece 0)
  l.47 C-TAILMONO OK N=4: 6 pieces; s_x, s_y, tau, rho_1 and env_r below 1; the envelope at D0 = 3 encloses the end at d = 3..15, 30 and 31 (A_y, A_x, N', |P_e a|, |S a|, e; for h also the coefficient and e)
  l.48 TAIL SUP N=4: sup over d >= D0 = 3 of e-hat(d) = max(rows 3..30, envelope at 31): least 2.478407e-05, largest 2.478407e-05 over the pieces; it enters h's envelope as the coefficient xc -+ sup and the x amplitude v_x -+ t_hi sup (the h end at every d >= D0)
  l.49 TAIL N=3 D0 3 M0 3: envelope classes 45 per piece, FAIL 0, least L 5.054482e-05 at h-1-aD0+/m2 (piece 0); m-tail at M0: FAIL 0, least lower end 2.081471e-02 (pair h-a, piece 0), q_R <= 0.6171, q_T <= 0.4886; sign condition (c): FAIL on 0 pieces; Proposition J envelope orbits: FAIL 0, least L_J 4.594906e-02 (d_R 0, piece 0)
  l.50 C-TAILMONO OK N=3: 6 pieces; s_x, s_y, tau, rho_1 and env_r below 1; the envelope at D0 = 3 encloses the end at d = 3..15, 30 and 31 (A_y, A_x, N', |P_e a|, |S a|, e; for h also the coefficient and e)
  l.51 TAIL SUP N=3: sup over d >= D0 = 3 of e-hat(d) = max(rows 3..30, envelope at 31): least 1.042323e-05, largest 1.042323e-05 over the pieces; it enters h's envelope as the coefficient xc -+ sup and the x amplitude v_x -+ t_hi sup (the h end at every d >= D0)
  l.54 REGRESSION v1_8_4 tail run 3:3 rows against v1_8_1: rows 534, rows differing 0
  l.55 TAIL REGRESSION v1_8_4 3:3 against v1_8_1: rows 12, rows differing 0
  l.57 TAIL N=4 D0 2 M0 5: envelope classes 77 per piece, FAIL 0, least L 1.436016e-07 at h-1-aD0+/m4 (piece 0); m-tail at M0: FAIL 0, least lower end 3.385416e-02 (pair h-a, piece 0), q_R <= 0.6347, q_T <= 0.4886; sign condition (c): FAIL on 0 pieces; Proposition J envelope orbits: FAIL 0, least L_J 6.734545e-02 (d_R 0, piece 0)
  l.58 C-TAILMONO OK N=4: 6 pieces; s_x, s_y, tau, rho_1 and env_r below 1; the envelope at D0 = 2 encloses the end at d = 2..14, 30 and 31 (A_y, A_x, N', |P_e a|, |S a|, e; for h also the coefficient and e)
  l.59 TAIL SUP N=4: sup over d >= D0 = 2 of e-hat(d) = max(rows 2..30, envelope at 31): least 1.679047e-04, largest 1.679047e-04 over the pieces; it enters h's envelope as the coefficient xc -+ sup and the x amplitude v_x -+ t_hi sup (the h end at every d >= D0)
  l.60 TAIL N=3 D0 2 M0 5: envelope classes 77 per piece, FAIL 0, least L 9.661874e-08 at h-1-aD0+/m4 (piece 0); m-tail at M0: FAIL 0, least lower end 2.439998e-02 (pair h-a, piece 0), q_R <= 0.6171, q_T <= 0.4886; sign condition (c): FAIL on 0 pieces; Proposition J envelope orbits: FAIL 0, least L_J 4.593869e-02 (d_R 0, piece 0)
  l.61 C-TAILMONO OK N=3: 6 pieces; s_x, s_y, tau, rho_1 and env_r below 1; the envelope at D0 = 2 encloses the end at d = 2..14, 30 and 31 (A_y, A_x, N', |P_e a|, |S a|, e; for h also the coefficient and e)
  l.62 TAIL SUP N=3: sup over d >= D0 = 2 of e-hat(d) = max(rows 2..30, envelope at 31): least 7.051137e-05, largest 7.051137e-05 over the pieces; it enters h's envelope as the coefficient xc -+ sup and the x amplitude v_x -+ t_hi sup (the h end at every d >= D0)
  l.65 REGRESSION v1_8_4 tail run 2:5 rows against v1_8_1: rows 534, rows differing 0
  l.66 TAIL REGRESSION v1_8_4 2:5 against v1_8_1: rows 12, rows differing 0
  l.68 PLANT OPN: FIRED on its own failure G-POS (classes failing at G-POS 75, at G-DELTA 0, on the margin alone 0; FAIL rows 75, gate lines 0)
  l.70 PLANT TAU2: FIRED on its own failure MARGIN (classes failing at G-POS 0, at G-DELTA 0, on the margin alone 174; FAIL rows 174, gate lines 0)
  l.72 PLANT SIGN: FIRED on its own failure MARGIN (classes failing at G-POS 0, at G-DELTA 0, on the margin alone 54; FAIL rows 54, gate lines 0)
  l.74 PLANT T2: FIRED on its own failure MARGIN (classes failing at G-POS 0, at G-DELTA 0, on the margin alone 2; FAIL rows 2, gate lines 0)
  l.76 PLANT DELTA: FIRED on its own failure G-DELTA (classes failing at G-POS 248, at G-DELTA 112, on the margin alone 83; FAIL rows 381, gate lines 0)
  l.78 PLANT PIN: FIRED
  l.80 PLANT COUNT: FIRED
  l.82 PLANT UNIF: FIRED
  l.84 PLANT DUPKEY: FIRED
  l.86 PLANT PROD: FIRED
  l.88 PLANT PRODOK: FIRED (the owner rule passed on 5 of 5 records with owner PRODUCER lines; FAIL rows 0, gate lines 0; a positive control)
  l.90 PLANT XSIGN: FIRED on its own failure MARGIN (classes failing at G-POS 0, at G-DELTA 0, on the margin alone 6; FAIL rows 6, gate lines 0)
  l.92 PLANT ENVR: FIRED
  l.94 PLANT FACTX: FIRED
  l.96 PLANT CSTAT: FIRED
  l.98 PLANT ORIENT: FIRED
  l.100 PLANT XORIENT: FIRED
  l.102 PLANT YORIENT: FIRED
  l.104 PLANT IORIENT: FIRED
  l.106 PLANT OCHK: FIRED
  l.108 PLANT XDEF: FIRED
  l.110 PLANT FLOOR: FIRED
  l.112 PLANT TAILQ: FIRED on its own failure TAIL-MTAIL (classes failing at G-POS 0, at G-DELTA 0, on the margin alone 0; FAIL rows 0, gate lines 0)
  l.114 PLANT TAILSIGN: FIRED on its own failure TAIL-SIGN (classes failing at G-POS 0, at G-DELTA 0, on the margin alone 0; FAIL rows 0, gate lines 0)
  l.116 PLANT TAILENV: FIRED
  l.117 negative 1 (a v4 set in v1_8_1's layout) rc=8 (8 expected)
  l.118 STOP G-PIN: MR_SPECTRAL has no valid ORIENT_CHECK line (the rows 4335, 4340): ""
  l.119 negative 2 (a v3 set without ORIENT_CHECK) rc=8 (8 expected)
  l.120 STOP G-PIN: MR_SPECTRAL has no valid ORIENT_CHECK line (the rows 4335, 4340): ""
  l.121 negative 3 (TAIL on a split set) rc=8 (8 expected)
  l.122 STOP G-TAIL: the tail section needs the factored mode (MR_INPUT_KV_v4 with a factored MR_CRUDEX)
  l.123 negative 4 (NMAX 8 below n0 10) rc=8 (8 expected)
  l.124 STOP G-TAIL: NMAX 8 is below n0 = 2 D0 + M0 + 1 = 10, so the finite check does not reach n0
  l.126 ROUTE V ON: MR_EXACT carries Pe_hi (the exact end's unwindowed flip-even |P_e a|), and the m = 1 rest takes the least of |P_e a_L| N'_R and 
  l.128 REGRESSION v1_8_4 route (v) against the diagnostic engine: rows 1732, rows differing 0
  l.131 ROUTE V ON THE V4 STAND-INS: rows 5564, H changed on 60 (m = 1: 60), H lower on 0
  l.133 G-FACTX OK: 72 x-coefficient rows inside their amplitudes with their floors (power 1) or equal to them (power 0); 2 rows with a Way B floor (last piece, h); one envelope per piece with 0 < env_r < 1
  l.134 FACTORED SIGN FALLBACK: 276 class-piece evaluations had no certified sign for the product of the two x coefficients, so X took v1_6's form there (the v1_7 N-2)
  l.135 TAIL N=4 D0 2 M0 5: envelope classes 77 per piece, FAIL 0, least L 1.055148e-07 at hD0+-a0/m4 (piece 5); m-tail at M0: FAIL 0, least lower end 2.230601e-02 (pair h-a, piece 0), q_R <= 0.6347, q_T <= 0.4886; sign condition (c): FAIL on 1 pieces; Proposition J envelope orbits: FAIL 0, least L_J 6.695998e-02 (d_R 0, piece 0)
  l.136 TAIL N=3 D0 2 M0 5: envelope classes 77 per piece, FAIL 0, least L 8.667310e-08 at hD0+-a0/m4 (piece 5); m-tail at M0: FAIL 0, least lower end 2.003058e-02 (pair h-a, piece 0), q_R <= 0.6171, q_T <= 0.4886; sign condition (c): FAIL on 1 pieces; Proposition J envelope orbits: FAIL 0, least L_J 4.571841e-02 (d_R 0, piece 0)
  l.139 FLOOR TAIL ROW N4_P0005 sign FAIL envfail 0 verdict FAIL
  l.140 FLOOR TAIL ROW N3_P0005 sign FAIL envfail 0 verdict FAIL
  l.141 REGRESSION floor set rows against the zero-floor rows of up_v4f (n <= 10): rows 534, rows differing 220

pk24/jobs/job193_v1_8_3.console (sha8 054eb57c):
  l.26 UDIFF OUT ca76f2a53a6746c856c823f3f9d2647d5ce10ad65cbaaf04da06271755fe8950 /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_engine_tmpl_v1_8_2_v1_8_3.txt: 14 lines added, 11 removed
  l.27 UDIFF OUT 4e82c0eac16c4683f6e25437aafef344011e67b9d797686a927d250d75694b7a /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_merge_tmpl_v1_8_2_v1_8_3.txt: 14 lines added, 13 removed
  l.28 UDIFF OUT 0326e10e4441500a0e72e2c4b503c3963e13fcdf0bd59df3f204666d4bb2b8f0 /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_engine_tmpl_v1_7_1_v1_8_3.txt: 391 lines added, 90 removed
  l.29 UDIFF OUT 34d622cc3fea3fad6b1c3df4889d91f420debb5b5e91482bbb013805d17e145e /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_merge_tmpl_v1_7_1_v1_8_3.txt: 84 lines added, 15 removed

pk24/jobs/job192_v1_8_2.console (sha8 f031c8ae):
  l.27 UDIFF OUT fd67c289f61d857194efb4c5b3a5a9bf971cbc70fe365abb29a8dd9285d3083e /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_engine_tmpl_v1_8_1_v1_8_2.txt: 120 lines added, 28 removed
  l.28 UDIFF OUT c049be9a35b0992bf0f4750704390e65a137e4d3bb8c9cf334f98d39b19cbd46 /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_merge_tmpl_v1_8_1_v1_8_2.txt: 16 lines added, 15 removed
  l.29 UDIFF OUT 7d4cb9d8f38a745bc87d07950da2e4a42d5a2b7aec83e8ea4d1adbcdf960a794 /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_engine_tmpl_v1_7_1_v1_8_2.txt: 388 lines added, 90 removed
  l.30 UDIFF OUT 87a2b3ff3b71952bde9944cb4e41e3ae62d090093117ba94ec2c0e7e151d750e /mnt/g2/release/root/code/pk24/mr_engine/out/udiff_merge_tmpl_v1_7_1_v1_8_2.txt: 83 lines added, 15 removed
  l.163 STOP C-TAILMONO N4 piece 5: the h envelope at D0 = 2 does not enclose the end at d = 2 (coefficient)

pk24/midrow/out/floor_effect_v1.out (sha8 6ae09299):
  l.1 FLOOR EFFECT (pk24/mr_engine/v38/MR_ASSEMBLY_floor.kv against pk24/mr_engine/v38/MR_ASSEMBLY_v4f.kv): 534 rows, FAIL 0; H changed on 45 rows, least ratio H(floor)/H(zero floor) 0.999938 at N4_n10_h3-a10

pk24/midrow/out/j195_meters.out (sha8 391bee53):
  l.1 METER MIDROW_GUARD_: 1308 logs, 7126.9 core-s
  l.2 METER hand total: 1609 logs, 10766.0 core-s = 2.9906 core-h; no meter line: none; killed: ['LEAK_GUARD_j60_w3_0.log']

## 7. Files (sha256, size, path)
4ca2e281945f1ff6e59f322d4be6779f2688ba1f366020395899fc1fdeb68b51  6959  pk24/notes_src/KT_MR_ASSEMBLY_body_v1_8_4.md
fdff041f962fc5009f50d3a1aeacea9d36c3323fb383d90ad06076aa5eff0cc6  6357  pk24/tools/assemble_mrnote_v1_8_4.py
1e570ab7476927dcd3238f347b744c223209d417084f8b756e259d97f68f8b01  189608  pk24/MIDROW_G6_SPEC_v1_6_2.md
8e50b08ea8ed9228d34f5afb466fce867592792204f0c8472cdf8dde11806d57  23990  pk24/KT_MR_ASSEMBLY_v1_7_1_NOTE.md
6c0314cce845d1313c7e8fe213f389e8946ade07c3fd7cbb09d42cd22f82b940  48580  pk24/KT_MR_ASSEMBLY_v1_8_1_NOTE.md
a015de89527cb09df74dc17ce5891d38df76f30ec1ade6e3cb082653ea783c3e  12635  pk24/MANIFEST_KT_MR_ASSEMBLY_v1_8_1.sha256
25ba5014c96581b56ffe2e3bbcd5e3c47397cb55bb618f0da8b77f3872c75f35  17166  pk24/tools/make_mrtemplates_v1_8_2.py
7e767b5ce68486570fd06134ed0c94bac62847b33ad8168fb6c47d6bd63f1dee  1413  pk24/tools/make_mrengine_v1_8_2.py
f110755e071a3c30f75e83fdbf4805e8886b9c59ca9e7ddbbdd3cd169459c169  2904  pk24/tools/make_mrtemplates_v1_8_3.py
c088845b56586a6a364e780385f96ec77945520e15860a60e7e77cd6de1b4eb1  1413  pk24/tools/make_mrengine_v1_8_3.py
dd2728c1e2d1ace94cab7e4ca68c38f619c5859f06d070534de05119a135e755  3952  pk24/tools/make_mrtemplates_v1_8_4.py
3d46bb90e9cec9c6712342ef3181013e1c3bf0bb8e908cbeac79a2d4d932952d  1413  pk24/tools/make_mrengine_v1_8_4.py
e1c3ddd9dcbbe614fa872eac838cd4849817cfee27dd430c29a42ccc59ad4233  4891  pk24/tools/upgrade_set_v1.py
4036513d147e466807b05e5f1f9c2b57288c0094fe5235322361a3bab9fa487a  1818  pk24/tools/make_mrengine_petest_v1.py
4d4f1e1df6f29596a7f0f4c45d1c72f10180b41fafd9facb9072d8ff3ea68f88  53421  pk24/mr_engine/test/kt_mr_assembly_v1_7_1_petest.py
36624a0e210ea24edb48423430532695458c780a35d172aac6678aa1d927d45d  912  pk24/tools/udiff_v1.py
b36e77a3a3742e326f10d620e1e94ccb1a1e87ccae99ec66bdfef64c8fd8f5fe  626  pk24/tools/astcheck_pk24_v1.py
a6012d273bec76c0ecf4aeed53e373d8b4bbbcf087f41c90a92b87827886b867  1374  pk24/tools/meters_v1.py
bafa8d0f1fcc3e76526f731b8253633843550cc33da076b4aaa77aff14d97796  53312  pk24/mr_engine/src/kt_mr_assembly_v1_7_1.py.in
7237c06563c136ab1081d13d6235c248fa9aaf6ccb518484d6cfcae7c922308c  11644  pk24/mr_engine/src/mr_merge_v1_7_1.py.in
21e2efabeec2ebb6b7244fa783c776f1b56714221e07b7a1b1532bcee634d2e2  53359  pk24/mr_engine/kt_mr_assembly_v1_7_1.py
ebdffc6773f00b3ed4184675c0ee3144304317893fa6687ba38c80c78779a7a7  11666  pk24/mr_engine/mr_merge_v1_7_1.py
93f9e24349fc1a4728a5a3347fb3b8358cff017eee5d8521f8c5b58b2a13d35a  68121  pk24/mr_engine/src/kt_mr_assembly_v1_8_1.py.in
6f973db12fd9dbec6d1193413b39b33242c621daca31e63922cef6fe2f66abb8  16817  pk24/mr_engine/src/mr_merge_v1_8_1.py.in
3af7c4b85211f625f674c3c596472e53881c6a201f17074a14d84f9b53e22715  68168  pk24/mr_engine/kt_mr_assembly_v1_8_1.py
f4a86ce8b02b358a3172c3f6789c0f136b02921e4f44b09000cc6816bc2eff9e  16839  pk24/mr_engine/mr_merge_v1_8_1.py
84d3449a6a196fb0165e520d273f9edf2fb800383c4a853f150c5396706f2412  75672  pk24/mr_engine/src/kt_mr_assembly_v1_8_2.py.in
59985924f141be689fed3af8ab7aebae1d7cab8ea992da15a33cb573dab1b071  17011  pk24/mr_engine/src/mr_merge_v1_8_2.py.in
cc57a95c47bf230833c73bcd5b200196b14cab6525bb8c03c057f3057310651e  75719  pk24/mr_engine/kt_mr_assembly_v1_8_2.py
e52aaea0419ffca8d90e4699e2b30ebc4c0df90df6edee567b32af5d834e8c1a  17033  pk24/mr_engine/mr_merge_v1_8_2.py
934ce7c3b13b90aebff9c7dad7c045e45dfa74ae7a1f910e5644ebe7a3ac60c2  76040  pk24/mr_engine/src/kt_mr_assembly_v1_8_3.py.in
b3d8959c7f0aff3852d10b415b35b38305b47db25115de883d4826302b75d29f  17074  pk24/mr_engine/src/mr_merge_v1_8_3.py.in
3be23b614e6810cd0ec05d6b4efcb2f0d59fe733a6246f54887bba95aa8d46bc  76087  pk24/mr_engine/kt_mr_assembly_v1_8_3.py
6da537bc65980da3915c7968e7fa7163ef70b189cdf13b8538238581a122eb0f  17096  pk24/mr_engine/mr_merge_v1_8_3.py
06a66ac4fbf75f7218f78277b688c58bcf1dc6dc4c26cac46448ebf2b14f2085  77272  pk24/mr_engine/src/kt_mr_assembly_v1_8_4.py.in
72020dd530b176a06dc3bc9539dfa49851333c922fc65728383c7a1e34058d87  17137  pk24/mr_engine/src/mr_merge_v1_8_4.py.in
abd48b2c94e0d64328ce631a21f8ab3c93c665f1de86e4abcdb190c3744df448  77319  pk24/mr_engine/kt_mr_assembly_v1_8_4.py
03110277e47b575653e573bd5135bb3c184a434b5b114a83265b53a4bbfe0138  17159  pk24/mr_engine/mr_merge_v1_8_4.py
b897451f512c69c3e08ac61d330f993634c105d42169dbd898dc91448554898a  7022  pk24/mr_engine/mr_core_v1_3.py
5e3fc430d69a445487a449fd54faefdf540ba8a3298a52c7e5fd9cadb0bd76e6  28386  pk24/midrow/g6_engine_proto_v1_2.py
6552ac82f2730230d4712700587909863bb9f71f8ab01b4157d6d9d1b071196f  52660  pk24/mr_engine/out/udiff_engine_tmpl_v1_7_1_v1_8_4.txt
fd67c289f61d857194efb4c5b3a5a9bf971cbc70fe365abb29a8dd9285d3083e  27297  pk24/mr_engine/out/udiff_engine_tmpl_v1_8_1_v1_8_2.txt
ca76f2a53a6746c856c823f3f9d2647d5ce10ad65cbaaf04da06271755fe8950  7838  pk24/mr_engine/out/udiff_engine_tmpl_v1_8_2_v1_8_3.txt
17da4a1adfaddcf88d77d6aaab7d12a75fc6b089cfa560515acc7ca38add0464  9283  pk24/mr_engine/out/udiff_engine_tmpl_v1_8_3_v1_8_4.txt
9dcd3c7c9d5819ffdf4a49e23023792b6cb42dae7d4350e4e1fdf8da1fedec49  13249  pk24/mr_engine/out/udiff_merge_tmpl_v1_7_1_v1_8_4.txt
c049be9a35b0992bf0f4750704390e65a137e4d3bb8c9cf334f98d39b19cbd46  8053  pk24/mr_engine/out/udiff_merge_tmpl_v1_8_1_v1_8_2.txt
4e82c0eac16c4683f6e25437aafef344011e67b9d797686a927d250d75694b7a  6759  pk24/mr_engine/out/udiff_merge_tmpl_v1_8_2_v1_8_3.txt
33b752a1cd6d0f1e67e2cbb3d55f9ad3cbcc296e99ace6b568826239812ae86b  6619  pk24/mr_engine/out/udiff_merge_tmpl_v1_8_3_v1_8_4.txt
0e843c9ae3d80d3004f1837c5674d2bb2cd646d194571af6a7e2c54595b04555  9258  pk24/jobs/job192_v1_8_2.sh
f031c8aedc6c2e1c9fd45c8bcf0edcce5a8a1ae0da973a7e31c51e335d61fb73  13895  pk24/jobs/job192_v1_8_2.console
8a9fcdfc7cc423e0aa398e85e1b0005003ee92193e9c56afdcc31118780e82ab  7840  pk24/jobs/job193_v1_8_3.sh
054eb57cf008eb8a48f796d58edde52d42f11e456fd9e737073d9208268643b9  9002  pk24/jobs/job193_v1_8_3.console
06e883361a084b7604d50ac3f68ffa84cebf1b4640e16edabf19a7bbd6b56250  7872  pk24/jobs/job194_v1_8_4.sh
af64bb70b343073608dac2319d63a3d8a34f55f2ec800ee733e93a126575bc47  12134  pk24/jobs/job194_v1_8_4.console
7809f44d49c637f8d5e2443d407b177dd55f25693b68b022dc0fbf3bf85c680c  4892  pk24/jobs/job195_g6spec_v1_6_2.sh
6ae0929917aeb8d276055545f12cbc0cdb3b7e926d69d890645da8bf643d22f6  207  pk24/midrow/out/floor_effect_v1.out
391bee53aab0f327636cfb2f0f0b6d7f5968d658bd7bbf720ab60a07a0f388d2  164  pk24/midrow/out/j195_meters.out
68e2b34ef41e7d34e57ce5bedbed5ca1e5307b7b6c2fa1a76e4200c80a78e1ac  4077  pk24/mr_engine/v36/up_v3f/MR_SPECTRAL.kv
fbb6b350603b9c010086b4c914d6c8efe79da2ad4763447718bdc6d809c359d7  14413  pk24/mr_engine/v36/up_v3f/MR_INSERT.kv
ed4dad3568d0a98fc1a27dab1a6ba48a47dc068442ad7ec5de8e214ca64cd8ff  6824  pk24/mr_engine/v36/up_v3f/MR_EXACT.kv
7827a7aa82d046fd66feaabb28ceb7524f3e132e5eeb8c8f734ec8bec0b846c1  3114  pk24/mr_engine/v36/up_v3f/MR_CRUDEX.kv
19bf3df0497923dc9da8f0cf1d5ccfd6ef54a6ee86199aeab2056fa1450c9571  5164  pk24/mr_engine/v36/up_v3f/MR_JOINT.kv
7e20bb8ed09ee5f2f12999d56e7ab653766fb4cfa8e97f18fcb5d4030b326b42  395  pk24/mr_engine/v36/up_v3f/PINS.txt
edc8b9855d404893e22e87f5b5ad6619c745581da8273c650cf9f0daad8e5d43  759  pk24/mr_engine/v36/up_v3f.console
cda98933237fcf01126aab745e75d86a7f74afecdec24ea69303567eda0cda85  4089  pk24/mr_engine/v36/up_v3s/MR_SPECTRAL.kv
3841c0c6325d23b4f0bc055050e21f17ed429546cec191dfe6442f3feab8ec79  14425  pk24/mr_engine/v36/up_v3s/MR_INSERT.kv
1425f9a0814035390c3d79a570f1113a580f90d831a170fad4a3c5db9fb3a211  6836  pk24/mr_engine/v36/up_v3s/MR_EXACT.kv
28183e3a41e476db2b65736160e77fe91864819511caa725fc6e62ef8e1bb5e7  3123  pk24/mr_engine/v36/up_v3s/MR_CRUDEX.kv
5146b7584c8ad11c9b2c4647c6fe57e4384ba98c4eed7dfbe6a2fdd15cac8468  5176  pk24/mr_engine/v36/up_v3s/MR_JOINT.kv
a3469fa89ff2c3d2ae8cecdedeeefff18ed4f7bdebbdea1e28cfb025fdfdc1f2  395  pk24/mr_engine/v36/up_v3s/PINS.txt
10f540093721d7a8ab43d21b18639f2815d2758499868b55166ce82e1acf954a  759  pk24/mr_engine/v36/up_v3s.console
10db2f08ac27d5742d13e134c47cd9594a7d6ebd39d2dea43347cce49d6a74fa  4091  pk24/mr_engine/v36/up_v4s/MR_SPECTRAL.kv
a01e462340079dedac03c194b953e7c0e3df3d3f4a6f51dfa56e83d20b4e5174  16094  pk24/mr_engine/v36/up_v4s/MR_INSERT.kv
33607956a7243235cd3d890ea025a75ae6e7eea5c347f6de1b24895cf3061ac5  8493  pk24/mr_engine/v36/up_v4s/MR_EXACT.kv
d234084f5e97b69517921ecc543f6301685cd5e0bffec1545e2363fbc64be92d  3125  pk24/mr_engine/v36/up_v4s/MR_CRUDEX.kv
8cb1d2a84bf8e8dda7272a55cb4ad1858405a608aeb1d982ca450703a461a002  5178  pk24/mr_engine/v36/up_v4s/MR_JOINT.kv
6a8a5c2cca3d29c2e9f18d30b994605a71e0d4eec0a6730feef6567cdd4fc9a8  395  pk24/mr_engine/v36/up_v4s/PINS.txt
d82711a251cc4e8dab806b69f437e358e2b3c8f4324702af4ed20c4f6e417124  796  pk24/mr_engine/v36/up_v4s.console
6a2ba9b6983837a83f84396f8b4a1ba4cdcd79a28be4480e185a3971e2a9ce26  4091  pk24/mr_engine/v36/up_v4f/MR_SPECTRAL.kv
41214f1b1e6ca25103dd915155785b9ba82dc35442901bb963226b290484ebec  16094  pk24/mr_engine/v36/up_v4f/MR_INSERT.kv
95600663058460309a76242e8da80d833eb96d7ab9d2735298ea0f5d4ba90e72  8493  pk24/mr_engine/v36/up_v4f/MR_EXACT.kv
0a0c131fa66ff67e0a94e12a1fb92b1d144f1ee4e6342ec578c2c65da40429b4  35542  pk24/mr_engine/v36/up_v4f/MR_CRUDEX.kv
a58fd097ac3d8512ce085b0032e8ff4fbd7b71c6c0887c3a810ec9a7df416f50  5178  pk24/mr_engine/v36/up_v4f/MR_JOINT.kv
fb14da7b88525614bf15f0392b7628d43da75aef5d26e7ad04df270ab7a60c7e  395  pk24/mr_engine/v36/up_v4f/PINS.txt
b43e188fdd7f54a5898678cf376787e079e3cf032672a461db55aa1fc0cdff67  796  pk24/mr_engine/v36/up_v4f.console
1e817b834757499cca305ddc0dbe48445aa3100b5fb294414f9448ca7dd5bf6e  4088  pk24/mr_engine/v36/up_a0/MR_SPECTRAL.kv
9bc583e2f04f09a7622271e3bfcdd20211c9d5d73d41cef68386b037ad77c3b5  14424  pk24/mr_engine/v36/up_a0/MR_INSERT.kv
bd4da62ac7d379abbcf41a21f321de803eb80e8e0d10243f0e1b1f9b2d30aa10  8689  pk24/mr_engine/v36/up_a0/MR_EXACT.kv
22f90b95d5450513886a1b8bed0b974dc1150a396d3259e7e38d08ad85d8acb8  3125  pk24/mr_engine/v36/up_a0/MR_CRUDEX.kv
e285991c1917675a3aa4fcb70ad305007112873b856bf37b2a549c66f40e5ff3  5175  pk24/mr_engine/v36/up_a0/MR_JOINT.kv
e6b575da33ad3e18af748ffc4785e32af7dd42afc4e2cf61f61f5439f1389e7e  395  pk24/mr_engine/v36/up_a0/PINS.txt
8c703e7d49ac2b39ec397902e3db34a8ab0d1da34f32accd8bcd4c09f9244f9c  753  pk24/mr_engine/v36/up_a0.console
483dec43c54d09114fb63e3e7beaf0da36de57e8d58718713741cffe3c294952  4109  pk24/mr_engine/v36/up_cwa0e/MR_SPECTRAL.kv
5a25ca1ea6b1fd07aa84c73ebfcb8202c45b88ae327e39fdc958f2f77020f511  16112  pk24/mr_engine/v36/up_cwa0e/MR_INSERT.kv
b663d9a7ce8610e1a5d167b4d8ed15b1eef99a9696c77a0791a8d37b449b64b9  10887  pk24/mr_engine/v36/up_cwa0e/MR_EXACT.kv
fc2934e183003549126166444bf81cecb6129ea3ab48fcac3f6731d8e586717d  35560  pk24/mr_engine/v36/up_cwa0e/MR_CRUDEX.kv
5045cc8cebaaf5371d16605628cff17450e89d388658dc27ee835da990a4d213  5196  pk24/mr_engine/v36/up_cwa0e/MR_JOINT.kv
75b01799e12b17558534aa7c31c93b1a58d2e3e8291e50e42f5729ed647cf050  395  pk24/mr_engine/v36/up_cwa0e/PINS.txt
6e663a2c174ca9df97bffd132cc45e00710346eec0a493d5cf00b1213fc9c030  808  pk24/mr_engine/v36/up_cwa0e.console
2138851a7343480e3ee296b061f9a67ad9463a9e74855ad80aab038e9d316250  481334  pk24/mr_engine/v36/up_routev/MR_SPECTRAL.kv
c2a6924c7ea425ca94739491c8e321606a94ea0a9a0faf0f0f4322079aa55154  2196882  pk24/mr_engine/v36/up_routev/MR_INSERT.kv
0e9f36fdb1adf768b34c6237f8e4698d7d801e31ada74889d9216eb60070ea66  1395361  pk24/mr_engine/v36/up_routev/MR_EXACT.kv
3db4eff5d130deac003e6b0a91026b133cad656c10603694863efad0cc1f76c2  384250  pk24/mr_engine/v36/up_routev/MR_CRUDEX.kv
30dfcde85ad37809703990e3f1522c2686b842d64f0e8252be279f34f79a7de7  620301  pk24/mr_engine/v36/up_routev/MR_JOINT.kv
e6e1043bca173a2bc1374d0127596ebb7abeeca0cf64877e87cfb542a584b1e0  395  pk24/mr_engine/v36/up_routev/PINS.txt
9b00f2391f48ddeace7fc4cf59a348d007acec5989c62a08696b46abad7d481c  797  pk24/mr_engine/v36/up_routev.console
6a2ba9b6983837a83f84396f8b4a1ba4cdcd79a28be4480e185a3971e2a9ce26  4091  pk24/mr_engine/v36/up_v4f_pex4/MR_SPECTRAL.kv
41214f1b1e6ca25103dd915155785b9ba82dc35442901bb963226b290484ebec  16094  pk24/mr_engine/v36/up_v4f_pex4/MR_INSERT.kv
aa14f7d1a108dc5664f9dc5d8426850879be85743b730e3add662b18b3a50e27  9207  pk24/mr_engine/v36/up_v4f_pex4/MR_EXACT.kv
0a0c131fa66ff67e0a94e12a1fb92b1d144f1ee4e6342ec578c2c65da40429b4  35542  pk24/mr_engine/v36/up_v4f_pex4/MR_CRUDEX.kv
a58fd097ac3d8512ce085b0032e8ff4fbd7b71c6c0887c3a810ec9a7df416f50  5178  pk24/mr_engine/v36/up_v4f_pex4/MR_JOINT.kv
1333c2f5c91d2914f626a719478dfbfd41e6fc54340415529e07dd45c63abd1d  395  pk24/mr_engine/v36/up_v4f_pex4/PINS.txt
d4514ca030839eefbb402b3b44a2b23c8cec7326161740376f7eb17492886ad3  832  pk24/mr_engine/v36/up_v4f_pex4.console
6a2ba9b6983837a83f84396f8b4a1ba4cdcd79a28be4480e185a3971e2a9ce26  4091  pk24/mr_engine/v36/floor_v4f/MR_SPECTRAL.kv
25efe9f011d9b644799854039f97aa558da3c98dbb8fe8be8c116d3d4adead8b  16112  pk24/mr_engine/v36/floor_v4f/MR_INSERT.kv
95600663058460309a76242e8da80d833eb96d7ab9d2735298ea0f5d4ba90e72  8493  pk24/mr_engine/v36/floor_v4f/MR_EXACT.kv
0a0c131fa66ff67e0a94e12a1fb92b1d144f1ee4e6342ec578c2c65da40429b4  35542  pk24/mr_engine/v36/floor_v4f/MR_CRUDEX.kv
a58fd097ac3d8512ce085b0032e8ff4fbd7b71c6c0887c3a810ec9a7df416f50  5178  pk24/mr_engine/v36/floor_v4f/MR_JOINT.kv
6a7328c49c139c0e15e6af6f7cd9f0700a04628593b815e900997b68cd87d13f  395  pk24/mr_engine/v36/floor_v4f/PINS.txt
354e927b503c3881669cacb0e15fea996160190b77cdc987b3af32b60dbcfe96  184717  pk24/mr_engine/v38/MR_ASSEMBLY_v3f.kv
7646cb4229ad0b65e115c6e81948c049275aa79f9f6ebd17176002463590e0f1  184702  pk24/mr_engine/v38/MR_ASSEMBLY_v3s.kv
2f688a14f307c30a84700c1e147085f6ab438bf05fd1ae87865f483b6131ddb7  184702  pk24/mr_engine/v38/MR_ASSEMBLY_v4s.kv
79d1414246d7f9f0cadaab35c6f8952db1122c1890ffe6af98ca9b01d037ffc3  594654  pk24/mr_engine/v38/MR_ASSEMBLY_v4f.kv
660289732b45bbeae92ab7189672e04f70d32937b848e4c3fab4c97030cb3257  184714  pk24/mr_engine/v38/MR_ASSEMBLY_a0.kv
d7028ae34ef2131ba37f89f7ee6074fa2c019a489c1ed5afd418ec56efc36d71  57547  pk24/mr_engine/v38/MR_ASSEMBLY_tail_D3_M3.kv
fa106a825835021f1a8be146f3ff5f684b3fff8da8b748951a0e5091d95dab1b  57547  pk24/mr_engine/v38/MR_ASSEMBLY_tail_D2_M5.kv
3f72953adc65ce0731ddf507a093a153f1d85f7cad4a75a5947b4114a79fe959  192866  pk24/mr_engine/v38/MR_ASSEMBLY_routev.kv
3aac0c378615847cba4fb2e745fcb1f652fffa6fb65375ec25e3478428271da4  594636  pk24/mr_engine/v38/MR_ASSEMBLY_v4f_pex4.kv
700a0f143257a50e644f2fbaa1d193548f753c12c075e420f4cdc87941cfa5d2  57544  pk24/mr_engine/v38/MR_ASSEMBLY_floor.kv
a2aaa75e66e8f2480e09450b16377bc4e374089bde13996a58558d13b2f390f0  6015  pk24/mr_engine/v38/MR_ASSEMBLY_tail_D3_M3.kv.tail
795b542524e15536a3e82799998f229d129d0f2bc2e6be8d04b7d521d00c3387  5991  pk24/mr_engine/v38/MR_ASSEMBLY_tail_D2_M5.kv.tail
335666847972fbff74b0f3129e8ab53541d8ca98deb71a3c0afe1de95d3ae144  5983  pk24/mr_engine/v38/MR_ASSEMBLY_floor.kv.tail
99d4863a9a5f15ba042bd589644b9d52772244680711ebeb40351f02a87a786b  10470  pk24/mr_engine/v38/kt_mr_v1_8_4_v3f.out
f0367128c847f701f0050c1119e9a3ba5bfd955fe10c543f391e9be85d7c9622  10551  pk24/mr_engine/v38/kt_mr_v1_8_4_v3s.out
e5e49fc376d751a90f4152cd4a91d80bd37f26c25198e53a6a360917f32f3a40  10707  pk24/mr_engine/v38/kt_mr_v1_8_4_v4s.out
efcbc6fac78597030be09615a498084c7f78d6732b2174b737444538ff08e0ac  13767  pk24/mr_engine/v38/kt_mr_v1_8_4_v4f.out
096b4c2992018aef28b210333b0ca8cafd603bc72e4c1da846d88ae13d19f8e2  10620  pk24/mr_engine/v38/kt_mr_v1_8_4_a0.out
dd20357f1283aaf9dc232d015375b18c42c43c00e54a70cf8ccc481503957e84  11092  pk24/mr_engine/v38/kt_mr_v1_8_4_tail_D3_M3.out
97ebec97cf2da97f31cf8a4ac05eddbc707072131c3945ed4acea3f9cfbd4fed  11092  pk24/mr_engine/v38/kt_mr_v1_8_4_tail_D2_M5.out
ca9fe22f662e289d81d7a1295cf9f6b3b0f550abeb90c7af6d0b977107ebfcae  650  pk24/mr_engine/v38/kt_mr_v1_8_4_neg1.out
6a3356f0dedc1b06f41e72fc16ab47bd591cce942140b80f696648005c48c9ff  647  pk24/mr_engine/v38/kt_mr_v1_8_4_neg2.out
d1e082269867cc2e10a70eff82ac092b66636d763640772a965d751434066485  1898  pk24/mr_engine/v38/kt_mr_v1_8_4_neg3.out
ca79bbacbca7b58f1eb6588aba8dd7bd70e568b7c275dc4f419d84ddf2dd506f  2128  pk24/mr_engine/v38/kt_mr_v1_8_4_neg4.out
4375dd9e78497c9a89c7b51b0052ba577c762e1e36f9efad70d97270d66b8cce  11740  pk24/mr_engine/v38/kt_mr_v1_8_4_routev.out
bee2074c161e27d3189cb4baba03cc498bf7332deb991470af855ea44eb4515c  13899  pk24/mr_engine/v38/kt_mr_v1_8_4_v4f_pex4.out
abef6abc6644710cf931afecfd6dfb8ba38fc4ee947c580f550ea02b066a041a  11011  pk24/mr_engine/v38/kt_mr_v1_8_4_floor.out
cb4b53db74bc69c6ee8efd910d26a41f9d9cd0418b834890a4f8d5ef5355d98b  15295  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_OPN.out
1ab67a9130a49edfe199084b245856649681407b4767fca59e49d6edbb186ec1  28222  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_TAU2.out
5f88e14cff0b240adec111ab6c8e75e79255001e11528374381d2713e03b0c49  12266  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_SIGN.out
65ec68e67a8c24deabbe36294c8a7ea9c559a76e35e920196208517a1e985127  5022  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_T2.out
c7083c849817188e258c229d00279b87229fac04f26dc6bff81b4cc6887bed3f  55441  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_DELTA.out
a98309e6337d7d1640c21d33220098198d069ff722a42d17286f999299f15691  714  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_PIN.out
c109ce7e9f43471434eae52c2c52fc5ab69546b6c82b5d79dc22e1fc9e00c961  2799  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_COUNT.out
2aa7df717c9cd3dc12b871ceb7166a1d7a29db42a718c2131b63eded4087cfd9  1187  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_UNIF.out
6b399dffeb9f4005604ad5751f15dc1df6976b7254d84dfcb8d467cb4ed454f7  713  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_DUPKEY.out
5c29e54a3cc9b863aebe41e932ec3e65a12fd97cf9af5f8fcce7604b2c70f844  609  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_PROD.out
00262ba194dc533cc104d75fdca7603bd85a544b5bd67e0748d7f7fd56d43609  4493  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_PRODOK.out
5214f9f2f23c565f977f72747f574979c47c2397515198fd9f3b59ee2df98ffe  5699  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_XSIGN.out
e5f90f1ba2ccc3d0a89139cc694f5f14efb631c5addb0431c0f5d261985cfb6d  1162  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_ENVR.out
d17a55aa980ee3cba8bf246aef318e311b2d26cfa546a2297ef223a84f210faa  1220  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_FACTX.out
b7cf17476b52368fadd1e48a62d9e739fae690374c40b1f54a85ca1030fcd0a2  604  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_CSTAT.out
5f04045f1087fd3b846b7ce0fa62019d07502f2647c9d80474950aca872fe689  1451  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_ORIENT.out
04827ff4fd09b6744f1ee560f7814390e5d131de9847d4f7207bd7f6bca8a256  1408  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_XORIENT.out
ea0f5703267cf222a5b2e2246fcefbd9928c0d069af8188076dd2767a2aa25c8  1447  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_YORIENT.out
021edd341c81398e845cdfc59f6f6c5a6e705f01bf7232c0ba7eef621a14133a  1429  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_IORIENT.out
2942118950f1370c8f408332e29118d4dee4d42042a1ec677e918e59ffe09c72  735  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_OCHK.out
bd0480e4e512324df3abb416560f7c4e3384f30d09a911880847a6321496da5f  834  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_XDEF.out
071863341a183f5e2441cc5c9b6777276c284e7e877badda31488d36da1acf18  1256  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_FLOOR.out
99990bbe6f6664d2c15f655f9f1e982b846be56ed859231bcefce73408072ec7  6334  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_TAILQ.out
4a0648286d9461ec831e5ae79f3378457f22aa27e3a87779ded1a73be2c2fbc0  6340  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_TAILSIGN.out
26955ba1d42bd2fe14aeee9b463f17d9a786b369bd8f2439c2fd263a00f03d35  3934  pk24/mr_engine/v38/kt_mr_v1_8_4_plant_TAILENV.out
a5a053c5e086fc10b4c12adcc827fbefb395541f7db312395fe6bc779646a0d8  184671  pk24/mr_engine/v22/MR_ASSEMBLY_v3f.kv
27d82599d4734abec2ff82c90afc852f07024cc961c3140732d3df9f93f44b99  184656  pk24/mr_engine/v22/MR_ASSEMBLY_v3s.kv
40e91d846a532571ad254d9e21fbe61c7a17a42188856841a613688788c5119d  184656  pk24/mr_engine/v22/MR_ASSEMBLY_v4s.kv
d76d3c078a67f02975c9368574d4c1f88b5613f75770b2ee8816467592ef19c6  594608  pk24/mr_engine/v22/MR_ASSEMBLY_v4f.kv
48687462f8d460c2bcfe44e4d04921b3fb0b513f682361c8a608b230adc6d1e1  184668  pk24/mr_engine/v22/MR_ASSEMBLY_a0.kv
0b748989246ca902e743f324e88cb66f0aa59e9e7f89b646aa045e15d58fb952  57533  pk24/mr_engine/v27/MR_ASSEMBLY_base_D3_M3.kv
babad1d96eb5b1ab3aae16768caa2db10eb9f7ba548d5e41fdd9a26e38904d0c  6015  pk24/mr_engine/v27/MR_ASSEMBLY_base_D3_M3.kv.tail
640670e41d0e12b2ac34e3b2e791c2682ae1f1ee3370ded4eca96f2a1c1d938b  57533  pk24/mr_engine/v30/MR_ASSEMBLY_base_D2_M5.kv
dcab0ffc37c538c2ce8e6bab069631cfcbe5a704a06c4995166ff5681f11a5c1  5991  pk24/mr_engine/v30/MR_ASSEMBLY_base_D2_M5.kv.tail
7a116c57274c0ab60ac5f2003d807edb7f9f32805374d34a9984de82a980d8d8  192821  pk24/mr_engine/v35/MR_ASSEMBLY_REAL_V3REC_E7_SIGNMBALL_SIGNM1_PEX4_PEV1.kv
