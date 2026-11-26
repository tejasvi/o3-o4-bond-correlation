# release_N: re-verification package

This package holds the programs, inputs, outputs and records of the computer-assisted steps in the paper *Positive correlation of bond energies in the O(3) and O(4) models* (DOI 10.5281/zenodo.24410344). With it a reader can rerun the 130 runs of RUNS_M2_release_N.tsv and compare each of their 251 outputs with its shipped copy. The package also lets a reader rebuild the three Lean trees and check the archived records that cannot be rerun here. Section 2 lists the results of the paper with the runs that support each, and sections 3 and 4 say how to rerun them and what was checked. REVERIFICATION.md at the root describes how the package was made from the archived files, what changed from the previous release (release_M), and how the package was checked.

## 1. Working labels

- **acc2**: code/acc/acc2_v1.py, the acceptance rule of the patched gates. It accepts an item that names the released producer, or one that names the original producer and equals its own row in an item manifest (code/acc/ITEM_MANIFEST_v1.tsv, and for the NE certifier also code/acc/ITEM_MANIFEST_M_v1.tsv).
- **box runs**: the five runs of the O5 engines on a large-memory machine, each made of many box jobs.
- **c3 records**: the eight records m3_c3_*.json under code/pk22/m3/out/; the NE certifier reads six of them.
- **carried, rerun**: a rerun output was remade by this package's programs and compared with its reference. A carried output is the archived output after the changes T, G and P. It is not rerun, and the package holds its producer as well.
- **family**: a group of runs in RUNS_M2_release_N.tsv.
- **first gate**: the first check that stops a carried program when it runs on the package.
- **M1, M2**: the middle-row certificates of Propositions B.22 (6 <= n <= 11) and B.24 (every n >= 6), together with their assembly runs nM1 and nM2. The two propositions are the certificates behind Theorem 6.22, and part (i) of Theorem 1.4 uses Theorem 6.22 for the pairs with a horizontal edge of the middle row.
- **NE**: Proposition B.13 (the separated pairs near the ends) and its certificate chain in code/pk22/w1/rc_cert/. The chain runs two smokes (short test items), 20 chunks (parts of the coupling range), two finals and the record item.
- **O5**: Propositions B.14 and B.15, the whole-graph certificates for P3 × P5 and for the rows of P3 × P6 and P3 × P7 at N = 4, made by the box runs.
- **plants**: deliberately planted faults that the checks must catch (section 2.2 of REVERIFICATION.md).
- **record A**: the record of Lemma B.7 and Propositions B.8 to B.10, code/pk21/p2/a/S_TB_PRIME_RECORD_v1.md.
- **R4, R5**: the cert run of kt_p2_assembly_v1_37_1 and the C2-a sweep of kt_s9h_v1_3_2. Record A checks the exports of both runs.
- **spot regeneration**: a run of the shipped producer that remakes one of its carried items, done once for each producer whose items are read by a certified run.
- **T, G, P**: the three recorded transformations from the archived originals to the shipped files. T replaces internal names and paths. G patches the gates for the two-producer rule of acc2 and makes the few changes that T cannot express. P recomputes the checksum in every pin and manifest row that refers to a shipped file, so that the checksum matches the shipped bytes.
- **tab16c**: the folders m3/out/tab16c and pev/out/tab16c, which hold the D16 moment tables.

## 2. What the paper proves and which runs support each result

The paper asks whether the scalar products of two pairs of spins, such as the bond energies of two edges, are positively correlated in the O(N) model on a finite graph. Theorems 1.1 to 1.3 prove the inequality for all couplings on classes of graphs: cycles and cacti for every N >= 2 (Theorem 1.1), several classes at N = 4 (Theorem 1.2), and at N = 3 every graph that has no W4 minor once the two pairs are joined by edges (Theorem 1.3). Theorem 1.4 proves the inequality at uniform coupling, for N = 3 and N = 4, for every pair of edges of the strips P3 × Pn and at every value of the coupling.

The steps that rest on a computer calculation carry a dagger in the paper and appear together in its Section 7. Two of them, Proposition 5.44 and Remark 5.45, belong to Section 5, on graphs without a W4 minor. All the others belong to the proof of Theorem 1.4 in Section 6 and Appendices A and B. The table below shows the records of each step and whether this package reruns them.

| Step in the paper | Range | Records | In this package |
|---|---|---|---|
| Proposition 5.44, Remark 5.45 | fixed multiplicities; four points (Remark 5.45) | records/W4free/ | rerun (1 run) |
| Lemmas A.2, A.3 | 0 < J <= 1/100 | records/weak_coupling/ | rerun (3 runs) |
| Theorem 6.6 | 0.0099 <= J <= 20.064 (N = 4), 0.0099 <= J <= 20.070 (N = 3) | records/strip_cover/ | rerun (4 runs) |
| Theorem 6.9 | 20 <= beta <= 100.68 | records/hub_cover/ | rerun (5 runs) |
| Lemma 6.10 | J >= 80 (N = 3), J >= 100 (N = 4) | records/P3xP3_strong/ | rerun (2 runs) |
| Theorem 6.19 | 20 <= J <= 300, and 300 <= J <= 350 at N = 4 | records/route_H/ | rerun (2 runs) |
| S1 to S8 and S9(i) (results 6.24 to 6.32 and Proposition B.1) | J >= 300 (J >= 350 at N = 4 for S8 and S9(i)) | records/S1S2/, S3a/, S3bd/, S4a/, S4b/, S4d/, S5S7/, S8/, S9i/, side/ | rerun (36 runs) |
| Lemma B.3(a) and the last claim of Lemma B.4 | J >= 300 | records/A2/, records/B4/ | rerun (3 runs) |
| Proposition 6.36, the grid P3 × P4 | J >= 300 (J >= 350 at N = 4) | records/P3xP4/ | rerun (41 runs) |
| Lemma B.7 and Propositions B.8 to B.10 (record A) | J >= 300 | code/pk21/p2/a/ (family strip_a) | checks rerun (3 runs); inputs R4 and R5 carried |
| Proposition B.13 (NE) | J >= 300 (J >= 350 at N = 4) | code/pk22/w1/rc_cert/ | rerun (25 runs), on the carried c3 records |
| Propositions B.14, B.15 (O5) | J >= 300 (J >= 350 at N = 4) | code/pk23/o5/ | carried; 12 box jobs regenerated |
| Propositions B.22, B.24 (M1, M2), the middle row | J >= 300 (J >= 350 at N = 4) | code/pk24/mr_engine/ | assembly rerun (2 runs) on the carried inputs |
| evidence for Conjecture 4.11 | | records/conjecture_U/ | rerun (3 runs) |

The record, checksum, outcome and controls of every certified run are in the supplementary document of the paper, *Run protocol, records and controls of the certified computations*.

## 3. Rerunning the package

1. Place a writable copy or overlay of the package at /mnt/g2/release/root (the root under which the programs and their gates look for their inputs), and check the copy or overlay with `sha256sum -c MANIFEST_release_N.sha256`.
2. Run each family of RUNS_M2_release_N.tsv on its own fresh copy of the package, with the family's runs in level order (`python3 -I -B rerun_m2.py --runs <the family's run ids>`). The strip_ne family must run in level order on its own fresh copy: the NE certifier gives its stray outputs the tags r1, r2 and r3 in level order. The driver rerun_m2.py works through the selected runs (all 130 runs of RUNS_M2_release_N.tsv when no subset is selected) in level order, from level 0 to level 7; the runs within a level do not depend on each other. For each run it moves the shipped outputs aside, runs the command in the run's folder with one thread, compares each new output line by line with its shipped copy, keeps the new output as `<path>.rerun` and moves the shipped copy back. It prints PASS or FAIL for every output, with the first lines that differ, and exits with status 1 if any output fails. `--runs ID,ID,...` and `--levels FIRST-LAST` select a subset, and `--runs nM1,nM2` repeats the two middle-row runs alone. To repeat the 37 checked parts exactly, run each row of RERUN_PARTS_release_N.tsv as `python3 -I -B rerun_m2.py --runs <runs>` from the root of a fresh copy, except that parts 35 and 36 each continue on the copy of the part before.
3. Use the interpreter that the reruns used: Python 3.14.4 with python-flint 0.9.0 (FLINT 3.6.0), numpy 2.5.3 and mpmath 1.3.0.
4. Plan for about two hours on one core. A full rerun on one core used 6,875 s of CPU (user plus system time), about 1 h 55 min, summed over the 37 parts of RERUN_PARTS_release_N.tsv.

In the comparison, timing and memory fields are masked: time stamps, memory peaks and times in seconds (CPU, wall and elapsed). The patterns TIME_RX and the keys TIME_KEY near the top of rerun_m2.py define these fields. Two more masks cover named fields in five named files: the four hub_cover outputs in code/pk05/out/ and the final output of p212fin in code/pk12/out/p212_v1_3_6_2/. No mask covers a certified value. A differing line also passes when it is a self-checksum line (END <sha256>, the checksum of the body of its own file) or when it maps the checksum of a shipped file to the checksum of the version written by the run.

### 3.1 Running a program by hand

- The programs create their outputs with mode 'x', so they never overwrite a file. A shipped output sits at the path where its program writes it; move it aside before you run the program yourself (rerun_m2.py moves the shipped output aside for you).
- Use one thread (OMP_NUM_THREADS=1), and take the folder and command of the run from RUNS_M2_release_N.tsv. The commands call python3 -I -B, except the runs scN4hi and scN3hi, which run code8/cover_check.awk with awk, and except the run mA_n1, which runs the shell script job27_n1.sh. The NE commands wrap python3 in timeout and prlimit with the time and memory limits of the archived chain. Where a program takes an item and a CPU limit (LIM, or cap_s in the four hub cover runs), both values are on the first line of the record of that program.
- These folders must be writable in your copy:
  - data/e17/unif/scratch/tmp, the N = 4 certifier's cache, which keeps only floats of exact 6j values;
  - the tmp/ folders (the certifier caches) of the bundle packages pkg_v2, pkg_n3 and pkg_cover_n3;
  - code/pk22/w1/ne_cert/cert_out, where the NE certifier writes one stray output per item.
- Each stray output of the NE certifier takes the first tag that is free in cert_out (r1, r2, ...), and that tag is recorded in the IMPORT line of the certifier. When the levels run in order on a fresh copy, the smokes and chunks take r1, the two finals take r2 and the record item takes r3, as in the shipped outputs (step 2).
- The cover jobs of Theorem 6.6 append to ledgers, which ship read-only: first make writable out/cover6_cv.ledger, out/cover4_S<k>.ledger, out/o3cover2_V<k>.ledger and out/o3cover6_n3.ledger (in the packages pkg_cover_cv, pkg_v2, pkg_n3 and pkg_cover_n3 of the bundle code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/). To rerun the first job of the N = 4 cover, run `python3 -I -B code8/certint6.py cv_001 14 6 adapt:3.0:4:0.015:0.0216667 vec frob` from pkg_cover_cv; the job writes out/certint6_cv_001.txt and appends to out/cover6_cv.ledger. To rerun the first job of the N = 3 cover, run `python3 -I -B code8/o3cert6.py n3_001 14 6 adapt:3.0:4:0.0133333:0.02 vec frob` from pkg_cover_n3.

### 3.2 Rebuilding the Lean trees

The Lean trees ship as sources, module lists, statements and changes, without build products. The folder lean/rebuild/ holds a rebuild summary for each tree and the axiom logs of G2Kernel_Lb_p13 and StripIII_v2. The Lean trees check deductions of the paper. G2Kernel_Lb_p13 checks those behind Theorem 1.1, behind both part (ii) of Theorem 1.4 and part (a) of Theorem 6.34, and behind part (b) of Theorem 6.34 for J <= 300. StripIII_v2 checks those behind parts (e) and (f) of Theorem 6.34 and part (i) of Theorem 1.4, with the certified results stated as hypotheses. G2Kernel_La_v1_7 holds the statements of G2Kernel_Lb_p13 on their own.

The three trees build with the Lean toolchain leanprover/lean4:v4.35.0-rc3 (Lean 4.35.0-rc3, commit 470d5ce1400764999581fd26d5d72b00d990b0f4) and Mathlib at commit c55e6e786f49471c72fbddbec5415808896aec1e of leanprover-community/mathlib4. The rebuilds used these dependency commits: batteries 3b7c8101932390d60e92a3f3d917901d5b5a773b, Qq 37b0ba0b26109cf9f9c541f0f9557e50cfa1a3b9, aesop a90fbf7b02ff06a0deebf74088dff9e5fe02c9ea, proofwidgets c643bbb3c24f8a25f9c14e3a6b1ceb13d01f3de1, importGraph 7e81a29bda33a6b257bd37557a6aa6aebe175d96, LeanSearchClient 29ff470276c725ae01505d55b17148c18fc7dfd3 and plausible fb13df72ecefd8ddbf9291021d7f33a8673eb57b. A Lake project that requires Mathlib at commit c55e6e786f49471c72fbddbec5415808896aec1e provides these packages, with their build products from `lake exe cache get` or from a build.

Each module is one call of lean, in the order of the MODULES.txt of the tree, with LEAN_PATH set first to the build folders of the eight packages above (mathlib among them) and then to the build folder BUILD of the tree: `lean -R TREE/src -j 1 -o BUILD/<m>.olean -i BUILD/<m>.ilean TREE/src/<m>.lean`, where <m> is a module path from the MODULES.txt of the tree, such as G2Kernel/Defs. G2Kernel_La_v1_7 (18 modules) and G2Kernel_Lb_p13 (33 modules) need only Mathlib, and each needs a separate build folder, since both use the module names G2Kernel.*. StripIII_v2 (35 modules) builds after G2Kernel_Lb_p13, with the build folder of G2Kernel_Lb_p13 before the build folder of StripIII_v2 on LEAN_PATH and with the further options -s 262144 -DElab.async=false. The rebuilds used one thread, and each call stayed within a 32 GiB address space.

The tree lean/StripIII_v2 holds 35 sources (in src/StripIII, src/StripIIIM1 and src/StripIIIM2) together with STATEMENTS.md, CHANGES_StripIII_v2.md, MODULES.txt, SCRUBBED_FILES.tsv and MANIFEST.sha256. It cites the paper by title, DOI and printed theorem numbers. CHANGES_StripIII_v2.md says how the sources of the tree were made from the archived ones. The six converters that made the list fragments of the modules are in code/rv83/tools/. Section E of STATEMENTS.md lists them, states their check and adds example commands. The converters need only python3 and its standard library. For the four box record tables from kit v6 on (the box kits under code/pk23/o5), use record2lean_v1_1.py, since record2lean_v1.py stops on these tables with a KeyError.

The trees lean/G2Kernel_La_v1_7 and lean/G2Kernel_Lb_p13 keep their names and paths. After the paper was frozen, their comments were rewritten so that each citation of a result of the paper uses the number printed in the paper, and the paper is cited by title and DOI. The change is described in the section "Citations of the paper (this release copy)" of CHANGES_La_v1_7.md and CHANGES_Lb_p13.md, in the two trees. With every comment removed, each Lean source of the two trees equals the release_M copy of the same source. Every module of the two trees was rebuilt (lean/rebuild/G2Kernel_La_v1_7_summary.txt and lean/rebuild/G2Kernel_Lb_p13_summary.txt), and the build products equal the release_M build, as the two CHANGES files state. The axiom log lean/rebuild/G2Kernel_Lb_p13_axioms.log is the release_M log, byte for byte.

## 4. The checks at a glance

| Check | What it covers | Outcome |
|---|---|---|
| Reruns (rerun_m2.py) | the 130 runs of RUNS_M2_release_N.tsv (grouped into the 37 parts of RERUN_PARTS_release_N.tsv) and the 251 outputs of the runs | all 251 PASS with the shipped driver |
| NE chain | two smokes, 20 chunks, two finals and the record item | VERDICT VALID in all 25 |
| Spot regeneration | one carried item of each producer whose items are read by a certified run (records/spot/) | every regeneration passes |
| Box spot regeneration | 12 jobs of the O5 box runs | all 12 pass |
| Plants | the 37 planted failures of the changed gates, made again on the bytes of this package, and the two out-folder plants of the bundle certifier | 37 of 37 refused, and both out-folder plants fire |
| Pin closure (check G9) | every full or 16-hex checksum in the shipped records (.kv, .json) of the certified middle-row runs | each points to a shipped file, a producer field or a stated class of files that do not ship |
| tab16c (check G11) | the folders of the D16 moment tables | no file of these folders ships |
| Manifests | MANIFEST_release_N.sha256, the checksum lists of the bundles, and the two certificate manifests of M1 and M2 in code/pk24 | sha256sum -c passes; the certificate manifests list the shipped bytes, the rerun records included |
| Lean | the rebuild from source of StripIII_v2, G2Kernel_La_v1_7 and G2Kernel_Lb_p13 (their summaries in lean/rebuild/), and the 52 checksum cells of StripIII_v2 | every module compiles (35, 18 and 33 modules), the La and Lb build products equal the release_M builds, and each cell gives a shipped file and its checksum |

release_N was checked in 37 parts, each on a fresh copy. The larger families (P3xP4, S4a, strip_ne) were split into parts, and strip_ne's three parts ran stacked on one copy. The basis for running each of P3xP4 and S4a in full on one copy is a scan of the copies after the parts ran (section 2.1 of REVERIFICATION.md).

All 130 runs (the 25 NE certificate runs among them) and the plants were done on release_N. Check G9, check G11, the manifest checks and the check of the Lean cells took place on the pre-releases of release_N and again on the release build before it was frozen. The spot regenerations, which remake carried items of release_L and earlier releases, ran on release_E, release_F or release_G. In release_N, the producers and inputs of these items are byte-identical to release_M's files. The box spot regeneration ran on a pre-release with inputs identical to release_N's.

For the details, see REVERIFICATION.md:

- the plants (section 2.2)
- the differences between the shipped programs and the program copies that ran on release_E, release_F or release_G (Table 2)
- the Lean tree and the check for each result (section 3)
- the reason for each item that is not rerun (section 4)
- the operations T, G and P with their exceptions, and the count of each change (section 5)
- the comparison rules, the masks and the planted controls that still fail with the masks applied (section 6.2)
- the rerun outputs, one by one (Appendix A)
- the first gate of each carried program of the middle row (Table D.1)

## 5. What is rerun and what is carried

For the middle-row results, the M1 and M2 assembly runs (nM1 and nM2 in RUNS_M2_release_N.tsv) were repeated on the shipped inputs, and their outputs ship as the records: the M1 record, the M2 record with its tail, the two engine consoles and the two PINS.txt files. MIDROW_RUNS_release_N.tsv maps the records of the certified middle-row runs in 83 rows (7 rerun, 10 certificate-set copies and 66 carried), each with the record, both checksums, the producer, the folder, the command and the status.

Except for the assembly program of nM1 and nM2, every certified middle-row program ships with its records, which are carried. On the package such a program stops at its first gate. One program gets through: code/pk25/asm/kt_s9h_crudex_v1.py writes the same record rows as its carried record, and the two records differ only in the header lines CODE and SOURCE.

The following are not rerun:

- the m3 runner productions (c3h_1, c3j, c3k_2, c3l and c3n_1) and the PEV production, all of which build and read the D16 moment tables of the tab16c folders
- the nu_g record (code/pk24/nu/kt_nu_g_v1_2.py), whose tool opens a pinned review document that does not ship
- the five O5 box runs (BOX_RUNS_release_N.tsv lists every job)
- the eight c3 records and the two asm outputs, all written in code/pk22/m3/out/ by the c3_1 runner, since the runner needs the c3_1 H-prep tables
- R4 and R5
- five programs that read their own source with inspect.getsource, and ten carried-item producers, which ship with their readers

## 6. Layout

The package has 5,229 files and 285,489,789 bytes in all.

- The root: this README, REVERIFICATION.md, the run table RUNS_M2_release_N.tsv, the box table BOX_RUNS_release_N.tsv, the map MIDROW_RUNS_release_N.tsv of the middle-row records, the parts table RERUN_PARTS_release_N.tsv, CORRESPONDENCE_release_N.tsv, MANIFEST_release_N.sha256, rerun_m2.py and the two licence files.
- code/: the programs, their inputs, the carried items and the rerun outputs. The runs su14, su16 and su29c run from data/appendix_a/scratch, with their programs and outputs. Of the 794 files added for the middle-row results, 787 sit in code/pk22 to code/pk25, with the M1 and M2 records in code/pk24/mr_engine. The folder of each middle-row record is in MIDROW_RUNS_release_N.tsv.
- data/: the inputs kept outside the program folders, each at the path from which a program reads it.
- records/<family>/: byte copies of the rerun outputs.
- records/side/: byte copies of 53 further run outputs, at their code paths: 52 outputs of the 16 runs of the family S1S2 and the output code/pk07/out/cplus_sidecheck_v1.kv of the run cplus of the family S8.
- records/original_T/: the reference for the comparison, the archived originals with T applied and no P.
- records/acc2/: for each run with an acc2 gate, every accepted item with its producer.
- records/spot/: the spot regenerations, listed with their verdicts in records/spot/SPOT_LISTING.tsv, records/spot/SPOT_LISTING_M.tsv and records/spot/C5_table_v11.tsv; records/spot/MBOX/ has the box spot regenerations.
- lean/: the Lean trees, with the Lean manifest lean/MANIFEST_lean_N.sha256 and the folder lean/rebuild/ (section 3.2). lean/G2Kernel holds only the archived manifest of the proof tree G2Kernel_Lb_p13, MANIFEST.sha256 with T applied. That manifest is the archived record of the reviewed build and lists the checksums of the archived files, so the shipped files are checked against lean/MANIFEST_lean_N.sha256 instead.

## 7. Checksums and correspondence

- MANIFEST_release_N.sha256 lists the checksum of every other file of the package.
- CORRESPONDENCE_release_N.tsv has a row for every file under code/, data/ or records/ and for each of the 35 sources of lean/StripIII_v2. A row records the checksum of the archived original (where there is one), the shipped checksum, the change and the twin path (the path of a file with the same bytes elsewhere in the package, or the source path if the file of the row is a copy). The Lean sources of lean/StripIII_v2 have the change D (an edit of comments or docstrings only), and the table also lists the 21 sources of release_M's lean/StripIII_v1 (section 8).
- Provenance lines are the SOURCE lines of records and the check lines of run consoles. Where a provenance line cites a short checksum of 8 or 16 hex digits, the checksum is that of the archived bytes, and CORRESPONDENCE_release_N.tsv maps each archived checksum to the shipped file. Two check lines of code/pk23/cw/out/cw_comb_v2_2_a.out, however, cite the moment tables psixy_exact_d_v2_n4.json and psixy_exact_d_v2_n3.json, which do not ship and have no row in CORRESPONDENCE_release_N.tsv.
- Certified runs pin some review documents as inputs. release_M ships these review documents as runtime inputs under code/rv01 and code/rv03, while this package refers to them only by their package paths.
- The manifests of the middle-row results are the archived manifests with P applied: a row has the checksum of the shipped bytes when its file is in the package, and keeps the archived checksum otherwise. P also recomputes the checksum lists of the bundles of Theorem 6.6 (section 5 of REVERIFICATION.md).

## 8. What does not ship

- release_M's Lean tree lean/StripIII_v1 and its two rebuild logs, all replaced by lean/StripIII_v2 and the two rebuild files of the new tree; no shipped program or manifest needs lean/StripIII_v1 or the two rebuild logs.
- python-flint 0.9.0 as vendored in the box kits and imported by the box engines (wheel python_flint-0.9.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl, sha256 2a0d8db1fab69104afdc7a9763a690337a1cecafbf476b310f5bcd8ccc97b29b).
- The c3_1 H-prep tables: 360 files, 14,603,510,994 bytes in the archived copy. code/pk22/m3/MANIFEST_H_PREP_COPY_v1.sha256 lists their checksums, and the 24 H prep pieces of code/pk03/m3_run_v1_9_3.py made the tables in 7077.8 s of CPU.
- The D16 moment tables of the tab16c folders: 2,400 files (31,277,742,998 bytes) for m3 and 360 files for pev.
- The working specification of the middle row, replaced by MIDROW_RUNS_release_N.tsv as the map of the records.
- The other review documents that are pinned as inputs by certified runs, and the 10 files that are pinned inputs of carried middle-row producers and lie outside the record manifests (marked out:pinned-input in CORRESPONDENCE_release_N.tsv).
- Some inputs of the ten producers of carried items of section 5: 93 files pinned by sha256 in eight of them, and the five files that n5map_v1 reads by path.
- The box infrastructure scripts and the raw box logs, which BOX_RUNS_release_N.tsv summarizes.
- Archived documents superseded by later revisions; CORRESPONDENCE_release_N.tsv lists each with its archived checksum and the note "superseded".

## 9. Licences

- The code, the Lean files and the data are under the Apache License 2.0 (LICENSE).
- The texts (this README, REVERIFICATION.md and the notes) are under CC BY 4.0 (LICENSE-TEXT).

## 10. A LaTeX file among the inputs

code/pk14/paper/rh_module_v1_4/RH_MODULE_v1_4.tex is a LaTeX module written for Section 6 of an earlier working version of the paper. The repository keeps it because the program code/pk02/kt_uhat_asm_v1_8.py reads it as an input.
