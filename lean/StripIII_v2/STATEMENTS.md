# STATEMENTS.md: the Lean tree StripIII_v2

This tree formalizes five results of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI
10.5281/zenodo.24410344) about the O(N) model with N = 3 and N = 4 on the strip graphs P_3 × P_n at uniform coupling J:

- `fullStrip_thm` (module StripIIIM2.FullStripM2), Theorem 1.4 (i), the main result: for every n >= 1 and every J >= 0, every pair
  of distinct edges of P_3 × P_n has Cov >= 0;
- `fullStripM1_thm` (module StripIIIM1.FullStripM1) and `fullStripM2_thm` (module StripIIIM2.FullStripM2): the same for 1 <= n <= 11
  and for n >= 12, the two halves that `fullStrip_thm` joins; at n >= 6 and J >= jLow N (300 at N = 3, 350 at N = 4) their
  middle-row pairs are those of Theorem 6.22, whose channel classes and interior same-bond orbits rest on Propositions B.22
  and B.24;
- `stripIII_thm` (module StripIII.FinalIIIG55), Theorem 6.34 (f): for every n >= 1 and every J >= 0, every pair of distinct edges of
  P_3 × P_n in which neither edge is a middle-row horizontal edge has Cov >= 0;
- `smallN_thm` (module StripIII.Small5Final), Theorem 6.34 (e): for 1 <= n <= 5 and every J >= 0, every pair of distinct edges of
  P_3 × P_n has Cov >= 0, middle-row edges included.

Here Cov is the covariance of the two bond energies in the Gibbs measure. The tree builds on the proof tree G2Kernel_Lb_p13 of this
package, whose definitions (the model, `G2pair`, `strip`, `uniform`) and named hypotheses it uses; G2Kernel_Lb_p13's STATEMENTS.md
describes them.

## Conventions
- A claim is a `Prop` definition (`fullStrip_statementL`, `fullStripM1_statementL`, `fullStripM2_statementL`,
  `stripIII_full_statementL`, `smallN_statementL`) whose premises are named hypotheses. A named hypothesis is a `Prop` definition used
  only as an explicit premise; none is an axiom. Kinds are as in G2Kernel_Lb_p13: a *restatement* states part of a theorem's
  conclusion and names its backing, a paper proof or a certified record.
- The claims take the records' lists as parameters, and the theorems fix them to the lists made from the records. Every theorem is
  stated for every N, and N = 3 ∨ N = 4 is the first premise of each claim.
- `G2pair N (strip n) (uniform J) e f` is `0 ≤ gibbsCov N (strip n) (uniform J) (bond e) (bond f)`, so every claim is nonstrict.
  Where a record gives a lower bound L, it certifies J^2 Cov >= L > 0, i.e. Cov >= L/J^2 > 0 (the records' engines compute the
  covariance of the J-scaled bond energies).
- Edges are coded as in StripIII.Core, with 0-based columns: `hor r i` is the horizontal edge of row r between columns i and i + 1
  (row 1 is the middle row), and `ver t j` is the vertical edge of column j between rows t and t + 1.
- A step marked † in the paper is a computer calculation in rigorous arithmetic; the hypotheses that restate such steps name the
  record that certifies them.
- The orbit step: the Lean hypotheses hBoxAll5 (the n = 5 box records), hM1 (M1's assembly record) and hM2tail (M2's tail record)
  extend each certified class from its representative pair, for which the record gives the bound, to all members of the class, the
  images of the representative under the reflections of P_3 × P_n in the middle row and in the vertical midline; this rests on the
  invariance of the Gibbs measure at uniform coupling under these two graph automorphisms, which is used here but not formalized in
  Lean. For M1 and M2 the class of a pair is computed from its edge codes (`canonKey`, `classOf`), and decide checks that it is an
  orbit invariant (at n = 6..11 for M1 and n = 6..14 for M2) and that it matches the records' rows.

## A. The five results
| theorem | module | claim | named hypotheses |
|---|---|---|---|
| `fullStrip_thm N : fullStrip_statementL N box5List (o5List ++ L55) (box5AllList34 ++ box5Stage2) m1List NMAX_M1 D0_M2 M0_M2` | StripIIIM2.FullStripM2 | N = 3 or 4, every n >= 1, every J >= 0: every pair of distinct edges of P_3 × P_n has Cov >= 0 | those of `stripIII_full_statementL`, hBoxAll5, hM1 and hM2tail |
| `fullStripM1_thm N : fullStripM1_statementL N box5List (o5List ++ L55) (box5AllList34 ++ box5Stage2) m1List NMAX_M1` | StripIIIM1.FullStripM1 | the same for 1 <= n <= NMAX_M1 = 11 | those of `stripIII_full_statementL`, hBoxAll5 and hM1 |
| `fullStripM2_thm N : fullStripM2_statementL N box5List (o5List ++ L55) D0_M2 M0_M2 12` | StripIIIM2.FullStripM2 | the same for every n >= 12 | those of `stripIII_full_statementL` and hM2tail |
| `stripIII_thm N : stripIII_full_statementL N box5List (o5List ++ L55)` | StripIII.FinalIIIG55 | N = 3 or 4, every n >= 1, every J >= 0: every pair of distinct edges, neither a middle-row horizontal edge, has Cov >= 0 | the hypotheses of `stripIII_full_statementL` |
| `smallN_thm N : smallN_statementL N (box5AllList34 ++ box5Stage2)` | StripIII.Small5Final | N = 3 or 4, 1 <= n <= 5, every J >= 0: every pair of distinct edges has Cov >= 0 | the hypotheses of `smallN_statementL` |

How the proofs combine: for n <= 5, the small-n theorem; for n >= 6, a pair without a middle-row horizontal edge by `stripIII_thm`. A
pair with one: J <= 300 by G2Kernel_Lb_p13's `strip300_thm`; at N = 4 and 300 < J < 350, hShared for the two vertical edges of one column
and hRHCover350 for every other pair; at J >= jLow N (300 at N = 3, 350 at N = 4), hShared for a common vertex, hStripMirror for a
left-right mirror pair, G2Kernel_Lb_p13's corner identity `corner_step` (Lemma 6.2) with hShared for the end orbit (h_1, t_1)
(Cov >= 0 only), and every other pair, a pair of a channel class or of an interior same-bond orbit, by hM1 for n <= 11 (through the
decide checks of StripIIIM1.HCheckM1) and by hM2tail for n >= 12 (through the covering `tail_cover` of StripIIIM2.M2Core: at
n >= 2 D0 + M0 + 2 every such pair has d >= D0, d' >= D0 or m >= M0). `fullStrip_thm` takes M1's theorem for n <= 11 and M2's for n >= 12.

## B. The named hypotheses of this tree
| hypothesis | kind | paper | backing |
|---|---|---|---|
| `hRHCover350 N` | restatement | Theorem 6.19 (†) at N = 4 on [300, 350] | the union check over [300, 350]: code/pk08/out/ru2_x2.out (sha8 6ac2e171) |
| `hStripMirror N` | restatement, paper proof | Lemma 6.1 | the reflections in the middle row and in the vertical midline |
| `hVertSV N` | restatement | Theorem 6.21 (†) | the paper's proof (S0, S7 and S8 with the inputs S1-S6; at N = 4 and 300 <= J <= 350, Corollary 6.20 in place of S8) |
| `hD4 N` | restatement, paper proof | Theorem 6.34, parts (a), (c) and (d) | the paper's proofs; Theorem 6.34 (d) with the certified Proposition 6.36 |
| `hNE N` | restatement | the separated pairs near the ends (NE) | NE's certified record code/pk22/w1/rc_cert/out/ne_rc_record_cert_kt_s8h_rcc_v1_5.kv (sha8 8ff64462); StripIII.NECheck checks by decide that its list is the class |
| `hBox5 N L5` | restatement | the joint pairs of n = 5 outside S0 | the box record of run 013023Z, version v1_2 (orbits n5 G12, G13, G26, G27, G06, G21); `L5` = `box5List` |
| `hS9h N` | restatement | S9(h), with its joint kind | record A, code/pk21/p2/a/S_TB_PRIME_RECORD_v1.md (sha8 772b9968), sect. 9 |
| `hS9i N` | restatement | Proposition B.1 (†) | its certified record, records/S9i/record.kv (sha8 0c497901) |
| `hO5 N L6` | restatement | the rows that Proposition B.1 excludes at N = 4 (O5), Proposition B.15 | the box record of run 013023Z, version v1_2 (n = 6: orbits G27 and G46), and the G55 record of run 045359Z (n = 7: orbit G55) |
| `hBoxAll5 N L` | restatement | Proposition B.14 (†): the pairs of P_3 × P_5 outside S0 with at least one horizontal edge (the class `g5`: 36 orbits) | the box records of runs 013023Z (27 orbits), 114847Z (7 orbits), 154150Z (G05) and 041647Z (G33) |
| `hM1 N L nmax` | restatement | Proposition B.22 (†): the channel classes and interior same-bond orbits at 6 <= n <= 11, J >= jLow N | M1's certified assembly record code/pk24/mr_engine/MR_ASSEMBLY_cert_m1_v4b_1_n11.kv (sha8 e5d78802): one row per class, each PASS at both N on every piece; `L` = `m1List`, one representative per class; StripIIIM1.HCheckM1 checks by decide that the list holds exactly one entry per class |
| `hM2tail N D0 M0` | restatement | Proposition B.24 (†), with Lemma B.23 and Proposition B.18: the classes with an end exponent >= D0 or a gap m >= M0, at every n | M2's certified assembly record code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv (sha8 2964b12e) and its tail record code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv.tail (sha8 0a84c0b4), TAIL = D0 M0 n0 = 2 5 10, every piece PASS at both N |

## C. The records
The docstrings cite each record by its path in this package and the sha256 of the shipped file (first 8 hex digits). The list
fragments in the sources were made from the records by six converters (section E); each fragment's first comment line names its
record and the record's sha256.

| record | files |
|---|---|
| record A | code/pk21/p2/a/S_TB_PRIME_RECORD_v1.md (sha8 772b9968); manifest code/pk21/p2/a/MANIFEST_S_TB_PRIME_RECORD_v1.sha256 (sha8 39e85db3) |
| NE record v1_5 | code/pk22/w1/rc_cert/out/ne_rc_record_cert_kt_s8h_rcc_v1_5.kv (sha8 8ff64462); manifest code/pk22/w1/rc_cert/MANIFEST_NE_RC_RECORD_v1_5.sha256 (sha8 93cb0f91); engine code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (sha8 e4243548) |
| box record, run 013023Z, v1_2 | code/pk23/o5/records/O5_BOX_RECORD_run_20261118T013023Z_v1_2.md (sha8 3abdb733); table code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv (sha8 19945efd); manifest code/pk23/o5/records/MANIFEST_O5_BOX_RECORD_run_20261118T013023Z_v1_2.sha256 (sha8 ff08d9ce) |
| G55 record, run 045359Z, v1_1 | code/pk23/o5/records/O5_BOX_RECORD_run_20261118T045359Z_v1_1.md (sha8 5091f54c); table code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T045359Z_v1.tsv (sha8 a1233479); manifest code/pk23/o5/records/MANIFEST_O5_BOX_RECORD_run_20261118T045359Z_v1_1.sha256 (sha8 81c390ed) |
| kit v7 stage 1 record, run 114847Z, v1_1 | code/pk23/o5/records/O5_BOX_RECORD_run_20261118T114847Z_v1_1.md (sha8 451b2115); table code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T114847Z_v1.tsv (sha8 c317dac0); manifest code/pk23/o5/records/MANIFEST_O5_BOX_RECORD_run_20261118T114847Z_v1_1.sha256 (sha8 62e585ec) |
| stage 2 record for G05, run 154150Z | code/pk23/o5/records/O5_BOX_RECORD_run_20261118T154150Z_v1.md (sha8 6884eada); table code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T154150Z_v1.tsv (sha8 94284d6e); manifest code/pk23/o5/records/MANIFEST_O5_BOX_RECORD_run_20261118T154150Z_v1.sha256 (sha8 35cb5899) |
| stage 2 record for G33, run 041647Z | code/pk23/o5/records/O5_BOX_RECORD_run_20261119T041647Z_v1.md (sha8 e5e358d7); table code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261119T041647Z_v1.tsv (sha8 d068beac); manifest code/pk23/o5/records/MANIFEST_O5_BOX_RECORD_run_20261119T041647Z_v1.sha256 (sha8 112af271) |
| route H, union check over [300, 350] at N = 4 | code/pk08/out/ru2_x2.out (sha8 6ac2e171) |
| M1's assembly record (n = 6..11, NMAX 11) | code/pk24/mr_engine/MR_ASSEMBLY_cert_m1_v4b_1_n11.kv (sha8 e5d78802); manifest code/pk24/mr_engine/MANIFEST_CERT_M1_V4B_1.sha256 (sha8 3cc9dd95); engine code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (sha8 28a340e7) |
| M2's assembly record and tail record (TAIL 2 5 10) | code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv (sha8 2964b12e); tail code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv.tail (sha8 0a84c0b4); manifest code/pk24/mr_engine/MANIFEST_CERT_M2_1.sha256 (sha8 fe528bb4); engine as for M1 |
| the J grid of both middle-row records | code/pk25/mr/v4/MR_SPECTRAL.kv (sha8 4a609ccf), pinned by both records |

## D. Interim forms, exercises and checks: not results
Only the five theorems of section A are the results of this tree. The following declarations are steps on the way, exercises or
checks, and none of them is a result:
- interim forms: `stripIII_statement` and `stripIII_full_statement` (StripIII.Statement), `stripIII_thm_of_checks` and
  `stripIII_full_thm_of_checks` (StripIII.Proof), `stripIII_final` (StripIII.FinalIII), `smallN_statement` (StripIII.Small5Statement),
  `smallN_thm_of_checks` (StripIII.Small5Proof) and `smallN_final` (StripIII.Small5Kit7);
- trials on lists computed from the classes themselves (not certified data): `trialBox5List`, `trialO5List` and the `trial_*`
  theorems (StripIII.Core); `stripIII_trial` (StripIII.Proof); `trialM1` and `trialM1_checks` (StripIIIM1.HCore);
- trials on the candidate lists of the probe outputs (not certified data): `trialG55`, `trialG55_checks` and `stripIII_final_trial`
  (StripIII.FinalIII); `smallN_cand` (StripIII.Small5Proof); `smallN_final_trial` (StripIII.Small5Kit7);
- the candidate lists themselves and their checks: `candBox5`, `candO5` and the `cand_*` theorems (StripIII.CandCheck); `cand5All`
  and its checks (StripIII.Small5Core); `candG05G33` (StripIII.Small5Kit7);
- checks and controls of the middle-row lists: `m1Check_plant` (StripIIIM1.HCheckM1; a list without one entry fails the check),
  `count_todo`, `count_orbits` and `count_end` (the counts of an independent enumeration), `num_inj_n11`, `canonKey_invariant` and
  `classKey_invariant` (the class functions), `tail_from_n6` (no tail class at n <= 5).
The theorems `L55_eq_trial` and `box5Stage2_eq_cand` show that the certified pairs of G55, G05 and G33 equal the probe's candidates.

## E. Files, build and axioms
- Build order: MODULES.txt (35 modules: StripIII, then StripIIIM1, then StripIIIM2, one source root for the three). The modules from
  StripIII.Statement on, and the StripIIIM1 and StripIIIM2 modules from HStatement and M2Statement on, import Mathlib through
  G2Kernel_Lb_p13; they build with the Mathlib pin and the toolchain (lean v4.35.0-rc3) of G2Kernel_Lb_p13, with G2Kernel_Lb_p13's
  build products on the search path. They compiled within a 32 GiB address space on one thread.
- lean/rebuild/StripIII_v2_summary.txt gives the rebuild of every module from these sources, and lean/rebuild/StripIII_v2_axioms.log
  the `#print axioms` lines of the Ax modules: every printed theorem depends on no axioms or only on `propext`, `Classical.choice`
  and `Quot.sound`. The sources hold no `sorry`, `admit`, `native_decide` or axiom declaration.
- The six converters that made the list fragments ship with the package's programs, in code/rv83/tools/: record2lean_v1.py and
  record2lean_v1_1.py for the box record tables, orbits2lean_v1.py for the probe outputs, nerec2lean_v1_1.py for NE's record,
  mrasm2lean_v1_1.py for M1's record and mrasm2lean_m2_v1.py for M2's record with its tail. They need python3 and its standard
  library only. Run from the package root on the shipped files, a converter prints its fragment, and the fragment occurs verbatim
  in its module. For example, `m1List` of StripIIIM1.M1List comes from
  `python3 code/rv83/tools/mrasm2lean_v1_1.py CERTIFIED code/pk24/mr_engine/MR_ASSEMBLY_cert_m1_v4b_1_n11.kv code/pk25/mr/v4/MR_SPECTRAL.kv`, and `m2Rows` of StripIIIM2.M2List from
  `python3 code/rv83/tools/mrasm2lean_m2_v1.py CERTIFIED code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv.tail code/pk25/mr/v4/MR_SPECTRAL.kv`;
  both check MR_SPECTRAL's pin and J grid and the record's gates first.
- CHANGES_StripIII_v2.md describes how these sources were made from the archived ones, and SCRUBBED_FILES.tsv lists each file's
  archived and shipped sha256.
