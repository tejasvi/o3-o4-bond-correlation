# Re-verification of the released archive

This document belongs to the archive of the computations cited in the paper "Positive correlation of bond energies in the O(3) and O(4) models". The records, checksums and controls of the certified runs are in sections 1 to 5 of the paper's supplementary document, "Run protocol, records and controls of the certified computations". Section 6 of the supplement is a summary of the present document. Here we set out what the archive lets a reader check, with the outcome of each check, and how each result of the paper is traced to its runs, records and Lean trees. Later sections describe what the checks leave open and how the released files were produced from the original files.

Files are referred to by their path in the archive and, where a checksum is quoted, by the first eight hexadecimal digits of their SHA-256 checksum. The root documents README_release_N.md, RUNS_M2_release_N.tsv, CORRESPONDENCE_release_N.tsv, BOX_RUNS_release_N.tsv, MIDROW_RUNS_release_N.tsv, RERUN_PARTS_release_N.tsv, CERT_PAIRS_release_N.tsv, P_MAP_release_N.tsv, CERT_MASKS_release_N.tsv, PLANTS_MIDROW_release_N.tsv and PREFIX_PINS_release_N.tsv are named without checksums. MANIFEST_release_N.sha256 lists the checksum of each of them and of every other file of the archive. The released files expect the archive at /mnt/g2/release/root. The root of the archive also holds the licences: LICENSE (Apache-2.0) covers the code, the Lean sources and the data. LICENSE-TEXT (CC BY 4.0) covers the texts.

## 1. What the archive lets a reader check

What the archive alone lets a reader repeat. A reader can:

- verify the archive with MANIFEST_release_N.sha256
- rerun the 130 runs with rerun_m2.py, which checks the prefix pins of PREFIX_PINS_release_N.tsv at full length before any run and compares each output with the shipped copy. Run each family of RUNS_M2_release_N.tsv on its own fresh copy of the package, with the family's runs in level order (python3 -I -B rerun_m2.py --runs <the family's run ids>). The strip_ne family must run in level order on its own fresh copy: the NE certifier gives its stray outputs the tags r1, r2 and r3 in level order.
- check the prefix pins alone, including those of the programs that no run executes, with python3 -I -B rerun_m2.py --pins
- compare each output with its certified form under records/original_T with cmp_certified.py: python3 -I -B cmp_certified.py REPORT for the shipped outputs, or the same with --rerun after rerun_m2.py for the copies that the reruns leave
- repeat the 11 planted failures of the two middle-row runs with plants_midrow.py
- rerun the six producers of section 2.1 by the commands of records/step3/STEP3_RUNS_release_N.tsv, compare their outputs with their carried forms with cmp_certified.py (section 2.1), and check rebuilt moment tables with sha256sum -c records/step3/STEP3_TABLES_release_N.sha256
- rebuild the two Lean projects lean/G2Kernel_Lb_p13 (with its statement tree lean/G2Kernel_La_v1_7) and lean/StripIII_v2, the library G2S0 under leanfull/s0, the tree of Theorem 1.1 under leanfull/s1 and the tree of the strip theorems under leanfull/s3
- inspect the certified forms of all 251 outputs under records/original_T and the spot regeneration records under records/spot/

Check A and check B need the private table of T (section 5). The spot regenerations of the programs of release_L ran on earlier issues of the archive, which are not part of the released archive, and no command to repeat them is given (only the driver of the W2M chain is archived). The 12 regenerations of box control jobs ran on a release_M pre-release. The files of that pre-release under code/pk23 include the kits and engines of these regeneration runs and are byte-identical to those of the released archive. Table 1 lists every check of this document and the section that sets it out.

**Table 1.** The checks of this document: what each covers, whether and how a reader repeats it from the archive alone, and the section that covers it in full, with its outcome.

| check | what it covers | from the archive alone | in full |
|---|---|---|---|
| the manifest | every file of the archive | yes, with MANIFEST_release_N.sha256 | section 5 |
| the reruns | the 130 runs of RUNS_M2_release_N.tsv and the 251 outputs of the runs | yes, with rerun_m2.py, family by family on fresh copies, as above | section 2.1, Table A.1 |
| the reruns of producers not rerun before | six producers, among them the pieces of the m3 runner that build and read the moment tables | yes, by the commands of records/step3/STEP3_RUNS_release_N.tsv, with cmp_certified.py and, for the tables, sha256sum -c records/step3/STEP3_TABLES_release_N.sha256 | section 2.1, Table A.2 |
| the comparison with the certified outputs | the 251 outputs | yes, with cmp_certified.py, on the shipped outputs or on the rerun copies | sections 2.1 and 6.2, Table A.1 |
| the planted failures | the plants of the changed gates, the plants of the output check of the bundle programs, and 11 plants of the two middle-row runs | for the 11 plants of the middle-row runs, yes, with plants_midrow.py; for the others, no | section 2.2 |
| the prefix pins | every token of 8 or 16 hexadecimal digits in a shipped program or run command that begins the checksum of a shipped file or of the original of a shipped file | yes, with rerun_m2.py, before the reruns or alone with --pins | sections 2.1 and 4 |
| the Lean checks | lean/G2Kernel_Lb_p13 with lean/G2Kernel_La_v1_7, and lean/StripIII_v2; the library G2S0 under leanfull/s0; the tree of Theorem 1.1 under leanfull/s1; the tree of the strip theorems under leanfull/s3 | yes, by a rebuild of each project | section 2.3 |
| the spot regeneration | one carried item of each producer of release_L, and the control jobs at $n=3$ and $n=4$ of the box runs | no: it ran on earlier issues of the archive | sections 2.4 and 6.3, Tables 2 and B.1 |
| checks A and B | the released files against the original files | no: they need the private table of T | section 5 |

## 2. The outcome of each check

### 2.1 The reruns

We reran 130 runs with the released programs: the 128 runs of release_M and the two middle-row runs. The levels, commands and inputs of these 130 runs are in the run table RUNS_M2_release_N.tsv. For the order of the runs, see README_release_N.md. The driver rerun_m2.py runs the table in level order on a writable copy of the archive and compares each output with its shipped copy. Before any run, it checks every row of PREFIX_PINS_release_N.tsv at full length and stops with exit status 2 on a difference (section 4).

Every output comes from a run on a copy of the archive in which each program and carried input read by the run is byte-identical to the released file: the outputs of release_L from runs on that release, the 62 outputs of record A and of the certificate of Proposition B.13 from runs on pre-release copies of release_M, and the outputs of the two middle-row runs from runs on a pre-release of release_N. Section 6.2 states the comparison rules of the driver and those of the comparison with the certified outputs.

release_N was checked in 37 parts, each on a fresh copy. The larger families (P3xP4, S4a, strip_ne) were split into parts, and strip_ne's three parts ran stacked on one copy. RERUN_PARTS_release_N.tsv lists the 37 parts with their families, copies, runs and CPU times (6,875 s of user and system time in all, on one core). Each part calls python3 -I -B rerun_m2.py --runs with the runs of that part from the root of a fresh copy, except parts 35 and 36, which each continue on the copy of the part before. The parts ran on a pre-release of release_N, and release_N holds the run files of that pre-release, byte-identical apart from rerun_m2.py. Every run ran once and exited 0. The parts ran with the driver of release_M: 246 outputs passed, and the other five differed only in the two fields of the added masks. The five runs of hub_cover then ran again with the shipped driver and passed, as did the runs of S9(i): p212pre then p212fin on one copy, and p212fin alone on another. Compared again under the rules of the shipped driver, all 251 outputs pass, and the two added masks change lines only in the five files that differed under the driver of release_M. The two middle-row runs also passed on a second, independent copy. After the 37 parts, a scan of the copies found three kinds of files besides the compared outputs and the .rerun copies kept by the driver: the numbered stray outputs of the NE certifier (strip_ne), the numbered stray outputs of both p212pre and p212fin, and the record folders written by the two middle-row runs (code/pk24/mr_engine/cert_*.rerun), console files included. For P3xP4 and S4a, whose parts ran on separate copies, this scan is the basis of the claim that each family can run in full on one copy: the runs of these families leave no file in the copy.

The driver of this version adds the check of the prefix pins. With this driver, the two middle-row runs nM1 and nM2 and the runs mA_a3, mA_a4 and s9h ran again, and all 11 of their outputs passed: five from the middle-row runs and six from the other three. Run with --pins alone, it found each of the 351 files of PREFIX_PINS_release_N.tsv with its full checksum, and a copy of the table with one checksum changed stopped it with exit status 2 before any run. Apart from this check, which runs before anything else and only reads files, the driver is, byte for byte, that of version 1 of the software record (10.5281/zenodo.24410346), with the same masks, comparison and run loop. The check passes on the copy from which each of the 37 parts started, so the verdicts of these parts hold for this driver as well.

With the driver of this version, the 37 parts then ran again in full. Each part except 35 and 36 started from the root of a fresh copy of release_N, checked against MANIFEST_release_N.sha256, with the driver and PREFIX_PINS_release_N.tsv of this version in place; parts 35 and 36 again continued on the copy of the part before. All 130 runs ran and all 251 outputs passed, and every part printed that the 351 files bound by a checksum prefix had been checked at full length and that none differed. The 37 parts took 7,022.8 s of CPU time in all.

Each output has one of two labels. Carried inputs (163 outputs): assembly and final steps re-executed on carried-over items. Regenerated (88 outputs): recomputed from the start with the released programs. Table 4 (section 3) shows the label of the runs behind each result of the paper, and Table A.1 lists the 251 outputs with their producers, acceptance logs and comparison results. Apart from outputs of other runs of Table A.1, the items read by the carried steps were carried over from the original runs, not recomputed. They have T and P applied, and they include:

- the job outputs of the cover of Theorem 6.19
- the interval items of the covers of Theorem 6.6
- the mode items of S1 and S2
- the node partials of S3(a) and S4
- the pieces of S3(b) and (d), together with their hand-offs
- the first-stage output and the chunks of S8
- the chunks of S9(i) and the u-hat records read by the runs of S9(i)
- the exports and the cert output of R4 as well as the export of R5, all read by the checks of record A
- six c3 records of the second item manifest (with the two assembly outputs of their runner), the t export of R4, the assembly output of the m2b runs, and the float tables and preparatory outputs pinned by the certificate of Proposition B.13
- the five input records of each middle-row run, written by the carried programs of Table D.1

These items are bound as in section 6.1 or by the full checksums pinned by the programs of the carried steps. Under records/acc2, each run with an acc2 gate logs the items accepted by its gate. The regenerated outputs also include the log written by code/pk07/kt_s9h_v1_2.py when it is run as a module by the check of (H) in code/pk07/cplus_sidecheck_v1.py, and the check of (H) pins the checksum of the log.

The outputs of the two middle-row runs ship as the records themselves: the record of Proposition B.22, the record of Proposition B.24 with its tail, the two run consoles, and the two PINS.txt files of the certificate sets. MIDROW_RUNS_release_N.tsv maps the 83 records of the certified middle-row runs: seven written by these two reruns, 10 staged as copies into the certificate sets of the runs, and 66 carried. Each row has the record, its archived checksum, its shipped checksum, its producer, the folder, the command and the status. The run command compares the two PINS.txt files with their shipped copies byte for byte.

Each output in Table A.1 was also compared line by line with its certified output, under the rules of section 6.2. Every output passed, so each reproduces its certified output up to these rules. The program cmp_certified.py repeats this comparison from the archive alone: on the shipped outputs, all 251 pass, each with the verdict of Table A.1 (section 6.2).

For this version, six producers that had not been rerun were rerun on the archive. Each output was compared by cmp_certified.py, under the map P of P_MAP_release_N.tsv, with the shipped output of the original run. The comparison of rerun_m2.py, which has no map P, fails at the lines that print a program checksum, since an output of the original run prints the checksum of the version that ran and a rerun output that of the released version; cmp_certified.py maps these lines.

- code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py, which writes the tau4 outputs for the record of S4(c) and reads its own source (section 4), with the item vsweep: VERDICT VALID, and all four outputs pass. The line of its console that prints the checksum of its export passes as a mapped rerun (section 6.2), since the export itself passes.
- R5, code/pk07/kt_s9h_v1_3_2.py, with the item sweep. Its check of the producers of its inputs compares the checksums of the original programs code/pk15/kt_sh1_v1.py and code/pk01/kt_s9b_v2.py (9a97356e and 33dda53f), which the carried outputs of these programs print in their headers, with two constants of R5, SH1_CODE (l.417) and S9B_CODE (l.426). P had set these constants to the checksums of the released programs (b7757b7e and 710ad713), so on version 1 of the software record this check failed. For this version G wrote the original checksums back into these two lines, as G wrote original constants into the changed gates of other programs (section 5); the shipped R5 differs from that of version 1 in these two lines only. R5 then gives RUN_VERDICT VALID and VERDICT VALID, and both of its outputs pass.
- code/pk11/kt_s8f1_v1_3.py, a producer whose outputs are read by the certificate of Proposition B.13 (section 4), with its four items. It pins at full length two reference outputs that version 1 did not hold, code/pk11/out/out_kt_s8f1_v1_1_n3.out and code/pk11/out/out_kt_s8f1_v1_1_n4.out; T leaves both unchanged, and this version adds them. Each item gives VERDICT VALID, and all four outputs pass.

- code/pk11/kt_s8rf_v1.py, a producer whose outputs the cert run of R4 reads, with its items n3 and n4. Of the four files that it pins at full length and that version 1 did not hold, T leaves three unchanged, and this version adds them. In the fourth, code/pk15/TABLE_P2_12_JOINT_SCREEN_SPRIME_ROUTEA_v1.tsv, T changed six header lines; this version adds its T image, and P re-pins the program to it, so the shipped kt_s8rf_v1.py differs from that of version 1 in this checksum only. Each item gives VERDICT VALID, and all four outputs pass.
- code/pk08/px08_hsd3b_export_v1_1.py, an export whose output the cert run of R4 reads and every file of which is in the archive, with the item run: VERDICT VALID, and both outputs pass.

The pieces of the m3 runner code/pk03/m3_run_v1_9_3.py, which build and read the moment tables, were rerun in four chains, H and S4 at $N=3$ and $N=4$, with 70 items in all: in each chain the prep pieces run in order until one prints that the preparation is done, and then come the entry, resume and smoke items. The last run of every item ended VALID. They are the only reruns that read the moment tables; the other five producers reran on the package alone. The rebuilt tables equal the data record: all 424 table data files byte for byte; the 296 hand-off records differ only in the kernel checksum (P map), the parameter hash that contains it, and per-unit CPU times. The item consoles do not match their carried forms line for line (the budgeted prep pieces split the work differently, 15/15/14/14 pieces against 14/10/12/13; the consoles print table hand-off checksums that follow the kernel checksum; the UNIT16 lines carry CPU times), so CERT_PAIRS lists only the chain outputs that pass, and the table check is the primary evidence for the chains. The consoles, error files and hand-off records of the prep pieces, the consoles and error files of the entry and resume items, and the memos ship as records of the reruns, not as comparison pairs. Thirty of the error files of the items hold a message of the access hook code/acc/acc2_v1.py, which opens its log with mode x and was given one log path for several items; the message is not output of the runner, and the rows of these items in STEP3_RUNS_release_N.tsv say so.

The outputs and consoles of all six reruns ship under records/step3/out at their package paths. records/step3/STEP3_RUNS_release_N.tsv lists each run with its program, folder, command, outputs and carried forms. records/step3/ also holds CERT_PAIRS_release_N.tsv for these outputs (32 rows), copies of P_MAP_release_N.tsv and CERT_MASKS_release_N.tsv, STEP3_TABLES_release_N.sha256 with the checksums of the 424 table data files, and STEP3_HANDOFFS_release_N.tsv, which lists the 296 hand-off records with both checksums and the fields that differ. Each run starts from its folder in a writable copy of the archive, after the shipped outputs of that run are renamed aside, since the programs open their outputs with mode x. Run from the root, the command `python3 -I -B cmp_certified.py --pkg records/step3/out --images . --tables records/step3 REPORT` compares the recorded outputs with their carried forms, and all 32 pass; with --pkg pointing at the root of a writable copy, it compares the outputs of a reader's own reruns in the same way. After a rerun of the chains, sha256sum -c records/step3/STEP3_TABLES_release_N.sha256 checks the rebuilt tables against the checksums of the data record.

Table A.2 lists all six reruns.

### 2.2 The planted failures

The plants of the released programs give an item a wrong producer checksum, change the bytes of a carried item or record, or offer a carried chunk of S8 under the released producer with the original input digest. The plants cover every family of changed gates. The 37 plants were made again on the bytes of release_N and run on release_N. All 37 were refused, and no run reached the time limit of 120 s. Of the 37 runs, 12 stopped at VERDICT INVALID (EXCEPTION), 14 at the refusal of a reader (with no VERDICT line), five at C-HASH naming the planted item, two at C-PRE and four at C-COVER. For 25 of these runs, the plant record of release_L has the same stop line as on release_N. The other 12 now stop at their own planted line. In release_L, whose runs stacked dry-run layers, these 12 plants had stopped earlier, at C-HASH on files of those layers and not on the planted item. The changes made by G in the certificate of Proposition B.13 add no check and so need no plant. The certificate's own plants of its format check (PLANT-C3-KEYSWAP and PLANT-C3-N) run on the path routed by these changes; each runs in 24 of the certificate's runs, and all 48 plant runs fire. The package changes of section 5 added an output check to the bundle programs. On release_N, this check was tested in the bundle program code8/certint6.py of pkg_cover_cv with two plants: an output that already exists and a copy outside the program's folder. Both plants fired.

The two middle-row runs have planted failures of their own. The assembly program takes the name of a plant as its fifth argument, PLANT, and plants_midrow.py repeats the command of each run on copies of its records whose names end in .plant_<id>, with 11 plants from the set of the program (PLANTS_MIDROW_release_N.tsv): PIN, COUNT, UNIF, SIGN, DELTA and ORIENT for the run of Proposition B.22 (nM1), and DUPKEY, XSIGN, FACTX, TAILSIGN and ENVR for the run of Proposition B.24 (nM2). All 11 fired, each within 78.1 s of CPU time. Three more plants of the set were tried on the run of Proposition B.24. PROD and CSTAT test stand-in records and do not apply to the certified runs: with either, the run did not stop and has no FAIL row. With OPN, the run fails through its margin rule, with one FAIL row, and not at G-POS, so by the rule of the program this plant does not fire. The consoles of the 14 plant runs are records/plants_midrow/P01.out to P14.out, those of PROD, CSTAT and OPN being P08, P11 and P14. plants_midrow.py runs only the rows of its table; each of the three further trials repeats by hand, with the command of the run and the name of the plant as its fifth argument.

### 2.3 The Lean checks

The three Lean trees, the library G2S0, the tree of Theorem 1.1 and the tree of the strip theorems build with the Lean toolchain leanprover/lean4:v4.35.0-rc3 (Lean 4.35.0-rc3, commit 470d5ce1400764999581fd26d5d72b00d990b0f4) and Mathlib at commit c55e6e786f49471c72fbddbec5415808896aec1e of leanprover-community/mathlib4. For the dependency commits and the build steps, see section 3.2 of README_release_N.md. Every Lean statement in the package is about finite simple graphs; Theorems 1.1 and 1.2(b) of the paper also cover graphs with parallel edges, through the reduction of Section 3.3 of the paper, which is not formalized.

The Lean project lean/G2Kernel_Lb_p13 of section 4 of the supplement was rebuilt from the copy that the archive ships: lean/rebuild/G2Kernel_Lb_p13_summary.txt records rc=0 for each of the 33 modules of the project. The axiom-check output of the project, lean/rebuild/G2Kernel_Lb_p13_axioms.log, lists the three axioms named in section 4 of the supplement and is byte-identical to that of release_M. lean/G2Kernel ships only its manifest MANIFEST.sha256, whose 36 rows name files of lean/G2Kernel_Lb_p13 by their archived checksums. The manifest is the archived record of the reviewed build, not a check of the shipped files: 11 of its rows match the shipped files and 25 do not.

lean/G2Kernel_La_v1_7 and lean/G2Kernel_Lb_p13 are copies of the release_M trees of the same names. In the copies, the comments cite the results of the paper by the numbers that the paper prints. The release_M trees cite the results by the numbers used in drafts of the paper. Both copies keep the tree names, and their files replace those of release_M at the same paths. Of the 23 files of lean/G2Kernel_La_v1_7 with its rebuild summary, 22 have new bytes and MODULES.txt is unchanged. Of the 39 files of lean/G2Kernel_Lb_p13 with its rebuild summary and axiom-check output, 27 have new bytes and 12 are unchanged (MODULES.txt, the axiom-check output and ten of the 15 files src/G2Kernel/Proofs/*.lean). Neither copy ships a list of its changed files, so the correspondence table has no rows for the files of either copy. With every comment removed, each Lean source of the two copies equals its release_M original. Both copies were rebuilt: every module compiles (lean/rebuild/G2Kernel_La_v1_7_summary.txt and lean/rebuild/G2Kernel_Lb_p13_summary.txt), and each module has the same imports and the same constants as in the build of the release_M tree, each constant with the same kind, universe parameters, type and value. CHANGES_La_v1_7.md and CHANGES_Lb_p13.md in the two copies describe the change to the comments.

lean/StripIII_v2 (the proof trees StripIII, StripIIIM1 and StripIIIM2) takes the place of the release_M tree lean/StripIII_v1, which does not ship in release_N: the tree StripIII of lean/StripIII_v2 holds the 21 sources of lean/StripIII_v1, 10 of them with changed comments or docstrings. lean/StripIII_v2 was rebuilt from the archive against lean/G2Kernel_Lb_p13: every module compiles (lean/rebuild/StripIII_v2_summary.txt), and the build product of each module equals that of the archived build. The axiom-check output in lean/rebuild/StripIII_v2_axioms.log lists the same three axioms as lean/G2Kernel_Lb_p13 and is identical to that of the archived builds. The sources of lean/StripIII_v2 differ from their originals in comments and docstrings only: with every comment removed, each source equals its original. lean/StripIII_v2/SCRUBBED_FILES.tsv lists them with the checksums of the originals and of the shipped files, and the correspondence table lists them as edits of comments only.

The six converters that made the list fragments of the modules of lean/StripIII_v2 are in code/rv83/tools/, and section E of STATEMENTS.md names them. They need only python3 and its standard library. When run from the package root on the shipped files, each converter prints a fragment that occurs verbatim in its module.

The library G2S0 of section 4 of the supplement ships under leanfull/s0: its 11 modules under src/G2S0/, with their build order in scripts/mods_S0_v2.txt; the statements of the library with their sources in the paper, STATEMENTS_S0_v3_public.md; the output of #print axioms of a clean rebuild, AXIOMS_S0_v2_public.txt; the build script scripts/build_tree_public.sh; lakefile.toml, which documents the layout (Lake is not run); and FROZEN_TO_SHIPPED_S0.tsv, which lists the files whose bytes differ from the frozen files that they come from: the statements and the axiom report differ in prose only, lakefile.toml holds a marked placeholder for the local Mathlib checkout, and the build script reads its paths from environment variables, while the 11 modules and their build list are byte-identical to the frozen ones. MANIFEST_S0_SLOT_v5.sha256 lists these 17 files with their checksums. The library builds against copies of lean/G2Kernel_Lb_p13 and lean/StripIII_v2 in its folder pkg/, with the toolchain and the Mathlib commit of the three trees, and the build sets LEAN_PATH to the build folders of the packages mathlib, batteries, Qq, aesop, proofwidgets, importGraph, LeanSearchClient and plausible of the Mathlib checkout. To rebuild it:

1. take a Mathlib checkout at commit c55e6e786f49471c72fbddbec5415808896aec1e with the builds of its packages in place, and the lean binary of leanprover/lean4:v4.35.0-rc3;
2. copy leanfull/s0 to a writable folder D, make the folders D/pkg and D/tmp, and copy lean/G2Kernel_Lb_p13 and lean/StripIII_v2 into D/pkg/;
3. set S0_DIR to D, MATHLIB_PACKAGES to the folder .lake/packages of the checkout and LEAN to the lean binary, and change to D;
4. run bash scripts/build_tree_public.sh Lb pkg/G2Kernel_Lb_p13/MODULES.txt, then bash scripts/build_tree_public.sh S3 pkg/StripIII_v2/MODULES.txt, then bash scripts/build_tree_public.sh S0 scripts/mods_S0_v2.txt; each run prints one MOD line per module and BUILD DONE, and writes only under D/build;
5. compare the 76 result lines of #print axioms in the console of the S0 run with AXIOMS_S0_v2_public.txt.

A rebuild by these steps from the shipped files passed: 33 modules for lean/G2Kernel_Lb_p13, 35 for lean/StripIII_v2 and 11 for G2S0, each run ending with BUILD DONE, and the 76 result lines of #print axioms equal to those of the axiom report, line for line. None of these lines names an axiom other than propext, Classical.choice and Quot.sound: 68 name all three, two name propext alone, and six state that the declaration depends on no axiom. Lean maps the build products of Mathlib into memory: under an address-space limit of 8 GiB the first module stops with a failure to read an .olean.private file, and the rebuild ran with a limit of 64 GiB.

The tree leanfull/s1 holds the proof of Theorem 1.1 of the paper with no hypotheses beyond those of the theorem (section 4 of the supplement): its theorems cactus_thm_full and cactus_strict_full, in src/G2S1/TopFull.lean, state both parts of the theorem for finite simple graphs and every $N\ge2$, and their proofs use only the three standard axioms of Lean.

The tree ships under leanfull/s1: the 24 modules of its build list scripts/mods_S1_final.txt, under src/, of which 18 are in src/G2S1/, one is src/G2S2/Ratio.lean, and five, SphereIso, KData, BlocksA, BlocksB and BlocksC in src/G2S0/, are byte-identical to the modules of the same names under leanfull/s0 and ship in the tree so that it builds by itself; the statements of the tree with their sources in the paper, STATEMENTS_S1_full_public.md and STATEMENTS_S1_v3_public.md; the output of #print axioms of a clean rebuild, AXIOMS_S1_public.txt, with two header lines and 101 result lines; and the build script scripts/build_s1_public.sh. The tree also ships FROZEN_TO_SHIPPED_S1.tsv, which lists the files whose bytes differ from the frozen files they come from: in the modules and the statements only comments, docstrings or prose changed, and no Lean statement or proof. MANIFEST_S1_SLOT_v4.sha256 lists these 30 files with their checksums.

The tree builds with the toolchain and the Mathlib commit of the three trees. Apart from the builds of the packages of the Mathlib checkout, the only build that it reads is that of lean/G2Kernel_Lb_p13 made for G2S0: its build script sets LEAN_PATH to the build folders of the packages mathlib, batteries, Qq, aesop, proofwidgets, importGraph, LeanSearchClient and plausible, to that build and to its own build folder. To rebuild it:

1. carry out steps 1 to 3 of the rebuild of G2S0 above and, of step 4, the run of build_tree_public.sh with Lb; this writes the build of lean/G2Kernel_Lb_p13 under D0/build/Lb, where D0 is the folder D of those steps;
2. copy leanfull/s1 to a writable folder D and make the folder D/tmp;
3. set S1_DIR to D, S0_DIR to D0, and MATHLIB_PACKAGES and LEAN as for G2S0, and change to D;
4. run bash scripts/build_s1_public.sh scripts/mods_S1_final.txt, which prints one MOD line per module and BUILD DONE;
5. compare the 101 result lines of #print axioms in its console with those of AXIOMS_S1_public.txt.

A rebuild by these steps from the shipped files passed: all 24 modules compiled and the run ended with BUILD DONE. Its 101 result lines of #print axioms are those of AXIOMS_S1_public.txt and equal, line for line, those of the final build of the tree before it was copied into the archive. Each of these lines names the three axioms propext, Classical.choice and Quot.sound and no other, among them the lines of cactus_thm_full and cactus_strict_full.

The tree leanfull/s3 proves hypotheses that the restated theorems of the library G2S0 still carry (section 4 of the supplement): Theorem 3.2 of the paper for two edges with a common vertex of a finite simple graph; Lemma 6.1 (for the diagonal reflections also without the sign condition on the couplings); at a corner of $P_3\times P_n$, the factorization over the common label that Lemma 2.4 uses and, for $0<J\le20$, the positivity of the covariance of the two corner edges; and, for $N=3$ and $N=4$, $\mathrm{Cov}(s_e,s_f)\ge0$ for any two edges of $P_3\times P_2$ at uniform coupling, the case of Theorems 1.2(a) and 1.3 that the strip theorems use. The tree derives this case from Theorem 3.2 and the corner identity of Lemma 6.2. Its forms of Theorem 1.4, of parts (a), (e) and (f) of Theorem 6.34 and, for $J\le300$, of part (b) of Theorem 6.34 and of Corollary 6.20 are those of G2S0 without these hypotheses and without the coefficient data of the corner step; every other hypothesis and every conclusion is unchanged, and their proofs use only the three standard axioms of Lean.

The tree also proves Theorem 3.7 of the paper (at $N=3$), Theorem 1.2(b) (at $N=4$) and Corollary 3.8 (at $N=3$ and $N=4$) for finite simple graphs, each with no hypotheses beyond those of the theorem; the law of the common label in Corollary 3.8 is the law under the label weight $p$ of Section 2 of the paper. For every $N\ge2$, the tree proves Theorem 3.7, the $2$-edge-cut part of Theorem 1.2(b) and the strict inequality of Corollary 3.8, again for finite simple graphs with no hypotheses beyond those of the theorems. Proposition 3.6 enters these proofs only through a factorization with weights given by Gibbs integrals, not in its form with $(2c+1)\alpha_c\beta_c$. The reduction of parallel edges in Section 3.3 of the paper is not formalized, so for graphs with parallel edges Theorem 1.2(b) rests on it, as Theorem 1.1 does.

These results are proved in six modules under src/G2S3/, CutGraph, GramSide, CutBase, CutFact, LawP and Thm37; a seventh, AxS3E, prints the axioms on which their theorems depend.

The tree ships under leanfull/s3: the 51 modules of its build list scripts/mods_S3_slot_v2.txt under src/, among them G2S1/Ladder.lean and G2S1/TopMergeH16.lean; the statements of the tree with their sources in the paper, STATEMENTS_S3_public.md and STATEMENTS_H16_public.md; the output of #print axioms of a clean rebuild, AXIOMS_S3_public.txt, with two header lines and 737 result lines; the build script scripts/build_s3_public.sh; and FROZEN_TO_SHIPPED_S3.tsv, which lists the files whose bytes differ from the frozen files that they come from. Four modules differ in comment lines only, and the other 47 are byte-identical to the frozen ones. The table also lists the closing note of STATEMENTS_S3_public.md, which has no frozen source. MANIFEST_S3_SLOT_v5.sha256 lists these 57 files with their checksums.

The tree builds with the toolchain and the Mathlib commit of the three trees, against the builds of lean/G2Kernel_Lb_p13, lean/StripIII_v2 and the library G2S0 made by the rebuild of G2S0: its build script sets LEAN_PATH to the build folders of the packages of the Mathlib checkout, to the folders build/Lb, build/S3 and build/S0 of that rebuild and to its own build folder. To rebuild it:

1. carry out steps 1 to 4 of the rebuild of G2S0 above; this writes the three builds under D0/build, where D0 is the folder D of those steps;
2. copy leanfull/s3 to a writable folder D and make the folder D/tmp;
3. set S3_DIR to D, S0_DIR to D0, and MATHLIB_PACKAGES and LEAN as for G2S0, and change to D;
4. run bash scripts/build_s3_public.sh scripts/mods_S3_slot_v2.txt, which prints one MOD line per module and BUILD DONE;
5. compare the 737 result lines of #print axioms in its console with those of AXIOMS_S3_public.txt.

A rebuild by these steps from the shipped files passed: all 51 modules compiled, with no error and no sorry. Its 737 result lines of #print axioms are those of AXIOMS_S3_public.txt. None of them names an axiom other than propext, Classical.choice and Quot.sound: 730 name all three, six name only some of them, and one states that the declaration depends on no axiom. The header comments of G2S3/AxS3.lean and G2S3/AxS3E.lean ask for all three axioms on every line; the seven lines that name fewer, those of strip_adj_iff, rev_zero_three, consEquivN_apply, fin_one_add_one_ne_zero and cycEdge_injective in AxS3 and those of reach_of_edge and sym2_exists_mk in AxS3E, are the only exceptions, and none of them names any other axiom. The first 650 are those of the tree without the seven modules above: 642 equal those of the final build of the tree before it was copied into the archive, in order, and the other eight are the lines of hLadder_holds3, hLadder_holds4, hShared_holds3 and hShared_holds4 and of the four theorems of the merged forms, strip300_thm_H16, smallN_thm_H16, stripIII_thm_H16 and fullStrip_thm_H16. The other 87 equal those of a clean build of the seven modules before they were copied into the archive, in order.

### 2.4 The spot regeneration

For each program of release_L whose carried items are read by a certified run, the spot regeneration takes one carried item, regenerates it and compares the regenerated item with its original record. The regenerations of 42 programs passed, in 42 runs. They all ran on earlier issues of the archive (release_E, release_F or release_G), while the released archive is release_N. A few programs are exempt, each for the reason given in Table B.1 or records/spot/C5_table_v11.tsv: the field arbeng_c2b_v2, which names a kernel and is not a program; the hand-made fixture mock_m2b_asm.out; the earlier version of the u-hat writer, v1_5, which is not in the archive and whose two mock outputs are read only by a control, the mock stage of code/pk12/kt_p212_cert_v1_3_6_2.py; five producers whose items are read by no certified run; and the bundle program of pkg_n3, code4/certint5.py, which has no item to regenerate. Of the producers added in release_M, only the engines of the box runs were regenerated: the 12 control jobs at $n=3$ and $n=4$ of the box runs of Propositions B.14 and B.15 all passed (section 6.3). The producers added in release_N were not regenerated either. Table D.1 shows, for each of them, the first gate at which a rerun on the package stops.

Table 2 names each class of difference between a shipped program and the version that ran, with the number of programs in each class. Table B.1 and records/spot/C5_table_v11.tsv (173d7ef7) classify each program, and records/spot/SPOT_LISTING.tsv (940f93b0) lists the files of the regeneration runs (details in section 6.3).

**Table 2.** The differences between the shipped programs and the versions that ran, by class, over the programs that produced carried items. In each class but the first, re-pinned checksums may differ too. The class of a program is the strongest found over the program and the shipped modules that it loads.

| class | how the shipped program differs from the version that ran | programs |
|---|---|---|
| identical | the same bytes | 1 |
| comments only | all the differences are in comments | 7 |
| T-v6 text only (tier a) | all the differences are in comments and docstrings | 12 |
| T-v6 text only (tier b) | all the differences are in comments, docstrings and string constants rewritten by T-v6; each of these constants is output text or is put to a use whose result cannot change | 24 |
| T-v7 text only (tier b), with G, P or both | as tier b, with T-v7 in place of T-v6, and with the changes of G or the re-pinned checksums of P where the cell names them (Table C.1 gives these classes for the programs added in release_M) | 23 |
| a file of release_L | a program of release_L listed with the producers added in release_M | 1 |
| — | no class: a producer without a version that ran in the regeneration (the reason is in its row) | 12 |
| all |  | 80 |

### 2.5 The box runs

For each job of the five box runs behind Propositions B.14 and B.15, BOX_RUNS_release_N.tsv records the command in archive paths, the limits, the exit code, the checksum of each output, the CPU time, the wall time and the peak memory. Table 3 has the total CPU time and the largest peak memory of each run. The outputs ship as T-v7 images of the outputs of the original runs. Neither the scripts that ran the box nor its raw logs are in the archive.

**Table 3.** The box runs of Propositions B.14 and B.15, summed by run from BOX_RUNS_release_N.tsv: jobs, exit codes, verdicts, total CPU time, total core-hours of the guard and the largest peak memory.

| run | jobs | exit codes | verdicts | CPU time (s) | core-h | peak memory (GiB) |
|---|---|---|---|---|---|---|
| 20261118T013023Z | 76 | none (no .rc: stopped) 1, 0 75 | VALID 75, none (no SUMMARY line) 1 | 103774.00 | 28.847 (the stopped job: last meter reading 0.250) | 150.159 |
| 20261118T045359Z | 4 | 0 4 | VALID 4 | 25441.56 | 7.072 | 497.508 |
| 20261118T114847Z | 17 | 0 17 | VALID 17 | 55326.52 | 15.375 | 90.575 |
| 20261118T154150Z | 5 | 0 5 | VALID 5 | 80670.00 | 22.414 | 382.133 |
| 20261119T041647Z | 5 | 0 5 | VALID 5 | 81007.51 | 22.508 | 382.202 |

## 3. From the results of the paper to their runs, records and Lean trees

Table 4 maps each result of the paper to the families of RUNS_M2_release_N.tsv that rerun it, to the records under which its outputs ship, and to the Lean tree and theorems that check its deduction; the statements of lean/G2Kernel_Lb_p13 are also archived on their own in lean/G2Kernel_La_v1_7. A dash in the column of runs marks a result with no rerun; a dash in the Lean column marks a result that is not proved by the Lean check but may enter it as a stated hypothesis (section 4 of the supplement lists these hypotheses). The last column contains either the label of the outputs of the runs (section 2.1) or the check that stands in for a rerun.

**Table 4.** The results of the paper, their runs, records and Lean trees.

| result of the paper | runs (family, number of runs) | records | Lean | outputs |
|---|---|---|---|---|
| Theorem 1.1, cycles and cacti, with the strict clauses | — | — | lean/G2Kernel_Lb_p13: `cycleG2_thm`, `cycleG2_strict_thm`, `cactus_thm`, `cactus_strict_thm`; leanfull/s1, with no hypotheses beyond those of the theorem: `cactus_thm_full`, `cactus_strict_full` | — |
| Proposition 2.1, the first identity, and the second for a single common label | — | — | lean/G2Kernel_Lb_p13: `covDeriv_thm`, `labelCov_thm` | — |
| Lemma 2.3, the two covariance statements | — | — | lean/G2Kernel_Lb_p13: `blocks_thm`, `blockRestrict_thm` | — |
| Lemma 6.1, the two mirror pairs of $P_3\times P_3$; Lemma 6.2 | — | — | lean/G2Kernel_Lb_p13: `rpCov_thm`, `mirror33_thm`, `corner_thm` | — |
| Proposition 6.7, the combinatorial part; Theorem 6.4, the inequality logic for one pair and the corner step through Lemma 2.4 | — | — | lean/G2Kernel_Lb_p13: `ledger_thm`, `criterion_thm`, `variance_pos_thm`, `cornerPair_thm` | — |
| Theorem 1.4(ii) and Theorem 6.34(a), the assembly | — | — | lean/G2Kernel_Lb_p13: `G2_P3P3_thm`, `strip3_thm`, `stripD_thm`, `stripD_factor_thm`, `cover_thm` | — |
| Theorem 6.34(b) for $0\le J\le300$ | — | — | lean/G2Kernel_Lb_p13: `strip300_thm` | — |
| Theorem 6.34(e) and (f) | — | — | lean/StripIII_v2, tree StripIII: `smallN_thm`, `stripIII_thm` | — |
| Theorem 1.4(i) | — (among its certified inputs: Propositions B.14, B.15, B.22 and B.24, below) | — | lean/StripIII_v2, trees StripIIIM1 and StripIIIM2: `fullStripM1_thm` ($1\le n\le11$), `fullStripM2_thm` ($n\ge12$), `fullStrip_thm` | — |
| Proposition 5.44 and Remark 5.45 | W4free, 1 | records/W4free/ | — | regenerated |
| Lemmas A.2 and A.3 | weak_coupling, 3 | records/weak_coupling/ | — | regenerated |
| Theorem 6.6 | strip_cover, 4 | records/strip_cover/ | — | carried inputs |
| Theorem 6.9 | hub_cover, 5 | records/hub_cover/ | — | regenerated |
| Lemma 6.10 | P3xP3_strong, 2 | records/P3xP3_strong/ | — | regenerated |
| Theorem 6.19 | route_H, 2 | records/route_H/ | — | carried inputs |
| S1-S2 (Propositions 6.24 and 6.25) | S1S2, 16 | records/S1S2/, records/side/ | — | carried inputs |
| S3(a) (Proposition 6.26) | S3a, 2 | records/S3a/ | — | carried inputs |
| S3(b) and (d) (Proposition 6.26) | S3bd, 1 | records/S3bd/ | — | carried inputs |
| S4(a) (Proposition 6.28) | S4a, 8 | records/S4a/ | — | carried inputs |
| S4(b) (Proposition 6.28) | S4b, 2 | records/S4b/ | — | carried inputs |
| S4(d) (Proposition 6.28) | S4d, 2 | records/S4d/ | — | carried inputs |
| S5-S7 (Propositions 6.29-6.31) | S5S7, 1 | records/S5S7/ | — | regenerated |
| S8 (Proposition 6.32), and the check of (H) after Lemma 6.27 | S8, 2 | records/S8/ | — | carried inputs |
| S9(i) (Proposition B.1) | S9i, 2 | records/S9i/ | — | carried inputs |
| Lemma B.3(a), the bound ${\rm A2}_N$ | A2, 2 | records/A2/ | — | regenerated |
| Lemma B.4 | B4, 1 | records/B4/ | — | regenerated |
| Proposition 6.36 | P3xP4, 41 | records/P3xP4/ | — | regenerated |
| Record A (Lemma B.7, Propositions B.8-B.10) | strip_a, 3 | code/pk21/p2/a/out/ | — | carried inputs (R4 not rerun, section 4; R5 rerun for this version, section 2.1) |
| Proposition B.13 | strip_ne, 25 | code/pk22/w1/rc_cert/out/ | — | carried inputs |
| Propositions B.14 and B.15 | — (the box runs, section 2.5) | BOX_RUNS_release_N.tsv | — | 12 control jobs regenerated (section 2.4) |
| Propositions B.22 and B.24 | midrow, 2 | code/pk24/mr_engine/, MIDROW_RUNS_release_N.tsv | — | carried inputs |
| Remark 4.12 | conjecture_U, 3 | records/conjecture_U/ | — | regenerated |

Every graph statement in this table is for finite simple graphs.

## 4. What these checks leave open

- Rebound code tokens. P rewrote 53 code tokens in 17 files so that the tokens name the released programs. These files are records and key-value files under code/ that were carried over from the original runs and are read by the released programs. The tokens are the values of CODE, LIB, PRODUCERS, COPIED_BLOCKS, A2_SOURCE, S8_CODE, S8_CORE and of the keys ending in _CODE. They pin program files, but they are not the producer fields that let a reader tell carried items from regenerated items. The producer fields are unchanged: the program checksums on the first lines, the engine fields and the original constants that G wrote into the changed gates. Each rebound token names one of three kinds of program:
  - (a) a program unchanged by G and therefore equal to its renamed original up to re-pinned checksums
  - (b) a program changed by G whose runs in Table A.1 passed the comparison
  - (c) a program changed by G without altering what the program produced

  The programs of kind (c) are one program with a single renamed identifier, and three versions of one certifying program. In the three versions the change is confined to an entry read by their assembly step alone, and the carried
  files name these versions only as producers of carried items. The original tokens remain in the original files, and the correspondence table lists the checksums of these files.

  The files added in release_M contain five more rebound tokens, one in each of five carried files: the CODE keys of the three exports of R4, of the C2-a export of R5 and of the tau4 export of the record of S4(c). These tokens name code/pk15/kt_p2_assembly_v1_37_1.py, code/pk07/kt_s9h_v1_3_2.py and code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py, three programs of kind (c). In each of these programs G renamed an identifier that bore a working-tree name, and in the first it also edited docstrings. The first was not rerun; the other two were rerun for this version, and their outputs passed (section 2.1). For that rerun G changed two more lines of R5, which therefore has a new checksum. The token of the C2-a export, which ships unchanged, names R5 by its checksum in version 1 of the software record, 5a877806, and P_MAP_release_N.tsv pairs this checksum with that of the shipped R5. The files added in release_N contain no rebound tokens.
- The scope of the comparison. The programs of release_L contain 301 places where a checksum rewritten by P might also be compared
  with a field of a carried item. Most of these places simply check a file. Of the 301 places, 288 lie in files read by the runs of Table A.1,
  all of which passed end to end. Each check executed by these runs at these places therefore gave the original result, while a check not executed by these runs cannot affect their outputs. The other 13 lie in code/pk03/m3_vac_v2_1.py, which no run of Table A.1 loads. The spot regeneration of m3_vac_v2_1.py in
  Table B.1 ran the program as issued in release_E and passed. The release_E copy differs from the released file in text that T-v6 rewrote. At seven of the 13 places the copy also differs in the re-pinned checksums, including the checksum of m3_reader_v5.py. The checks at these seven places have therefore run with their release_E values, not with the released values. The programs added in release_M contain 137 more such places. Of these, eight lie in code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py and in code/pk22/w1/ne_cert/kt_s8_cert_v1_14_3_ne.py, the copy of the S8 module loaded by the certificate; the 25 runs of the certificate of Proposition B.13 read both files and passed. The other 129 lie in 15 programs that no run of Table A.1 loads: the programs of R4 and R5; three earlier versions of the certificate; the three runners under code/pk22/m3/ and their hand-off module; code/pk02/kt_cert_v1_7.py, code/pk07/kt_s9h_m21.py and code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py; and three of the producers that ship without a rerun, code/pk03/m3_run_v1_8_3.py, code/pk03/m3_run_v1_10_4.py and code/pk15/m4_asm_v1.py. Two of these 15, the program of R5 and code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py, were rerun for this version, and their outputs passed (section 2.1). A check outside the runs of Table A.1 may still refuse a carried item, and no claim is made for other runs
  of the released programs. The programs added in release_N contain 404 more such places, in 40 files. Of these 404 places, two lie in code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (l.115 and l.116, the pins of mr_core_v1_3.py and g6_engine_proto_v1_2.py). The two middle-row runs load this program, and both passed. The other 402 lie in programs that no new run loads.
- Inputs bound by a prefix. PREFIX_PINS_release_N.tsv lists every token of 8 or 16 hexadecimal digits in a shipped program or run command that begins the checksum of a shipped file (991 rows) or the archived checksum of the original of a shipped file (1,298 rows): 2,289 rows from 178 programs and run commands, naming 351 files, each row with the full checksum of the shipped file. rerun_m2.py checks every row at full length before any run, and with --pins it makes this check alone, which also covers the programs that no run executes. No program and no output was changed for this: the prefix pins inside the programs stay as they are, and the table binds each of them at full length to one shipped file. The program code/pk07/kt_s9h_v1_2.py produces the outputs of S5 to S7 (records/S5S7/run.out and export.kv, Table A.1). It checks only the first eight hexadecimal digits of the checksums of 31 of the files that it reads, so for these files the link to the original files rests on the checksum prefixes, on the rows of the 31 files in the correspondence table and on check B. Among the programs added in release_M, two have runs in Table A.1 and bind inputs by such prefixes alone: code/pk21/p2/a/a3_bulk_checks_v1.py binds four of its inputs in this way, and code/pk21/p2/a/a4_units_crosscheck_v1_1.py binds three. Programs with no run in Table A.1 also bind inputs by such prefixes alone: code/pk07/kt_s9h_v1_3_2.py and code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py, which were rerun for this version (section 2.1), and code/pk07/kt_s9h_m21.py, for 31 inputs each; code/pk21/p2/a/a4_units_crosscheck_v1.py for three; code/pk15/kt_p2_assembly_v1_37_1.py for one; and eight scripts (make_*.py) under code/pk22 that write programs or entry lists, for 10 in all. For these inputs too, the link to the original files rests on the prefixes, on the correspondence table and on check B. Among the programs added in release_N, 26 bind inputs by checksum prefixes, in 105 pins, 100 of them by the prefix alone. Two of these programs run inside the two middle-row runs and write no output listed in Table A.1: code/pk24/tools/check_v4b_cols_v1.py, in the run of Proposition B.22, binds one of its inputs by the prefix alone, and code/pk24/tools/check_m2_cols_v2.py, in the run of Proposition B.24, binds two. The others were not rerun, and most of them are makers of carried programs.
- Box runs. Apart from the 12 control jobs of the spot regeneration (sections 2.4 and 2.5), the jobs of the five box runs behind Propositions B.14 and B.15 were not rerun, because of their size.
- The c3 records. The eight c3 records and the two assembly outputs of the c3_1 runner under code/pk22/m3/out/ were not rerun. The runner reads the H-prep tables, which the data record holds and which the reruns of section 2.1 rebuild, but two of the seven inputs that it pins were changed by T, so it cannot be rerun from the archive. code/pk22/m3/MANIFEST_H_PREP_COPY_v1.sha256 (5b462685) lists the 360 files of these tables, which held 14,603,510,994 bytes. The tables come from the H-prep pieces of code/pk03/m3_run_v1_9_3.py, and the 24 outputs of these pieces record 7077.8 s of CPU time in all (code/pk03/out/m3_run_v1_9_3_Hp*.out). The c3 records ship as carried items of the second item manifest and are read through the unchanged rule of acc2.
- The inputs of record A. The three exports of R4 with its cert output, and the C2-a sweep export of R5 with its sweep output, ship as carried items. Their producers, code/pk15/kt_p2_assembly_v1_37_1.py and code/pk07/kt_s9h_v1_3_2.py, ship. R4 was not rerun. R5 was rerun for this version, and both of its outputs passed (section 2.1); record A reads the carried export.
- Producers of carried outputs. The certificate of Proposition B.13 or the cert run of R4 reads the outputs of 10 programs that ship: code/pk11/kt_s8f1_v1_3.py; code/pk11/kt_s8h_mk_v1.py; code/pk24/n5/n5map_v1.py; the exports code/pk08/px08_hsd3_export_v1.py, code/pk08/px08_hsd3b_export_v1_1.py and code/pk08/px08_hsd4_export_v1.py; code/pk03/m3_run_v1_8_3.py; code/pk03/m3_run_v1_10_4.py; code/pk15/m4_asm_v1.py; and code/pk11/kt_s8rf_v1.py. Their outputs ship as carried items, and the chain of producers stops at these 10 programs. Each of these outputs keeps the archived checksum of its producer, and CORRESPONDENCE_release_N.tsv maps that checksum to the shipped program. Eight of the 10 programs pin 93 further files by checksum, 96 pins in all, and code/pk24/n5/n5map_v1.py reads five files by path. Version 1 of the software record held none of the 93 further files and none of the five files read by path. This version adds five of the 93, which T leaves unchanged: the two pinned by code/pk11/kt_s8f1_v1_3.py and three of the four pinned by code/pk11/kt_s8rf_v1.py. It adds the T image of the fourth, to which P re-pins kt_s8rf_v1.py (section 2.1). The others are not in the archive (Table B.1 counts these files for each program).
- Reruns of these producers and of code/pk02/kt_cert_v1_7.py. For this version, code/pk11/kt_s8f1_v1_3.py was rerun with the two reference outputs that it pins added to the archive, and its four outputs passed (section 2.1). The program code/pk02/kt_cert_v1_7.py, whose four items the cert run of R4 reads, cannot be rerun from the archive. It pins at full length 14 files that version 1 of the software record did not hold. This version adds the 13 that T leaves unchanged, but T changed one comment line of the fourteenth, code/pk02/out_kt_cert_v1_5_g.e1n4.out, so that a rerun stops at the check of the pinned files. With the original bytes of that file the check passes, but the four items then read the hand-offs of 16 earlier pieces of the program, which the archive does not hold. Two more of these producers were rerun for this version: code/pk11/kt_s8rf_v1.py, after P re-pinned it to the T image of the one table that it pins and that T changed, and code/pk08/px08_hsd3b_export_v1_1.py (section 2.1). The other seven cannot be rerun from the archive: code/pk11/kt_s8h_mk_v1.py, because T changed its input S8H_ENTRY_LIST_v2.json; code/pk24/n5/n5map_v1.py, because it reads five files by path, of which only three could be located; code/pk08/px08_hsd3_export_v1.py, because T changed four of the files that it pins and three could not be located; code/pk08/px08_hsd4_export_v1.py, because T changed two of them and two could not be located; code/pk03/m3_run_v1_8_3.py, because T changed both of its float references; code/pk03/m3_run_v1_10_4.py, because no copy of its 14 float references matches its pins; and code/pk15/m4_asm_v1.py, because only 2 of the 62 files that it pins could be located. R4 cannot be rerun either: its re-pin of KTCERT_SHA conflicts with the carried original efe4c40d, and a change by G would spread to four programs under code/pk25.
- Programs that read their own source. Five programs read their own source with inspect.getsource: code/pk07/kt_s9h_v1_3_2.py, which is R5; code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py, whose tau4 outputs for the record of S4(c) ship as carried items; code/pk07/kt_s9h_m21.py, a mock snapshot that runs in mock mode only, writes no shipped output and ships because R4 pins and reads it; code/pk22/m3/m3ref_px22_v1_5.py, a float reference whose outputs, twins of the certificate's inputs, the certificate reads only in development mode, not in cert mode; and code/pk23/pev/m3ref_hl_v1.py, a float reference for the PEV production on the L graph of S8. The first two were rerun for this version, and their outputs passed (section 2.1); the other three were not rerun. The outputs of code/pk23/pev/m3ref_hl_v1.py give the PEV runner the radii of its prep, and these radii are checked by the certifier of the PEV records. Apart from these five programs, the middle-row engine code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py reads program source for the C-CORE check of its two pinned modules. The two middle-row runs load it, and both were rerun and passed.
- The library python-flint. The archive does not include python-flint 0.9.0, which the programs import. The runs of Table A.1 used it under Python 3.14.4. The box runs used it under Python 3.13.5: each box kit under code/pk23/o5 carried the wheel python_flint-0.9.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (SHA-256 2a0d8db1fab69104afdc7a9763a690337a1cecafbf476b310f5bcd8ccc97b29b) together with the files installed from the wheel. The archive leaves out the wheel and the installed files, and the manifests of the kits list them by checksum. A check of each kit found that every installed file was listed in the RECORD file of the installation and was equal to its member of the wheel.
- The middle-row producers. The programs that wrote the input records of the two middle-row runs ship with their records, which are carried: the records are the archived ones with the changes of T, G and P, and they were not recomputed. For each of these programs, the first gate at which a rerun on the package stops is in Table D.1. The PEV production and the productions of the m3 runner for the middle row were not rerun: they build and read the moment tables of the tab16c folders, which do not ship, and T changed some of the inputs that they pin (Table D.1). The tab16c folder under code/pk22/m3/out held 2,400 files of 31,277,742,998 bytes, and the one under code/pk23/pev/out held 360 files. The record of the nu_g tool ships carried: the tool opens ten pinned inputs when it starts, and one of them is a review document, which does not ship.
- The carried inputs of the middle row. Table D.2 lists the 164 inputs that ship for the carried producers, each with the archived and released checksums, the change, the producer manifest if that manifest ships, and the package files that pin the input.

## 5. How the released files were made

Three operations, T, G and P, produced the released files from the original files. A few further package changes, made together with G, have an entry of their own below. Carried items are the outputs and hand-offs of the original runs, read by the released runs without being recomputed. The item manifests described below list those checked by the two-producer rule of section 6.1.

- Renaming (T) replaces each name of the original working tree by a neutral name, one to one, in paths and in the text of the files. T places the archive at /mnt/g2/release/root. Its version for release_L and release_M, T-v7, also rewrites working notes:
  - in the comments, docstrings and string literals of the programs
  - in the comments of the Lean sources
  - in the comment lines of shell and awk scripts
  - in the strings of echo, print and test statements in shell and awk scripts
  - in the text of records, outputs and notes

  T-v7 changes no number, identifier or operator in any program. On the files of the earlier issue release_L it gives the same bytes as T-v6.
- Gate changes (G) concern the checks that test the checksum of a program's own source or of the producer of one of the program's inputs. G alters most of these checks: after G, each altered check accepts an input by the two-producer rule of section 6.1. G leaves a few checks unaltered, and these require the released producer. Section 6.3 describes the regenerations of the programs that contain these unaltered checks. G also changes two kinds of check so that they accept the original checksum values only for carried items. One kind consists of the provenance checks in the readers of the S1 and S2 mode records. In the other, code/pk12/kt_p212_cert_v1_3_6_2.py binds the u-hat records read by the certified runs of S9(i). G bases the plants of S8 on the regenerated form of a carried chunk. In the certificate of Proposition B.13 (code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py), G adds the rows of the second item manifest (below) to the item rows that acc2 checks, and the certificate loads the c3 records through the certified entry point of their reader; the two-producer rule of acc2 is unchanged. For the rerun of R5 in this version, G changed two more lines of R5, which again hold the checksums of two original programs (section 2.1).
- Other package changes, made together with G, are the few code changes that T cannot express. They drop two pins of documents that no program reads, and they re-point the pin of one document to a one-line excerpt (code/pk15/HZ_PLAN_v1_1_l143.txt). The excerpt holds the line read by the program that has this pin. The archive does not contain the full document. These package changes also add an output check to the bundle programs of Theorem 6.6 that write output: each of these programs checks that its output goes into its own out/ folder. The package changes copy 10 library files into the folders of the programs that import them, and they add four empty cache folders. For the certificate of Proposition B.13 they add one more empty folder, code/pk22/w1/ne_cert/cert_out, into which the runs of the certificate write the stray output of the S8 module. Finally, they
  rename the identifiers that bear working-tree names, and T renames those names wherever they appear as text.
- Re-pinning (P) recomputes every checksum by which one released file pins another, so that the released programs and the files read by these programs pin one another. P also recomputes the checksum lists of the bundles of Theorem 6.6 and rewrites the self-checksums on the END lines of carried items. The recomputation of pins has two exceptions, both among the listed sites of check B (described below). First, a carried file keeps the original values of its pins to the original records that it was derived from. The carried files that keep these pins include the m3_s9 records and the run configurations of the u-hat writer. Second, six text pins keep their original values because recomputing them would run in a cycle through the item manifest: the pins in code/pk07/out/out_kt_s67_cert_v2_2_sweep.out, code/pk02/SCRATCH_asmdry/out_m2b_asm_v1_dry.out and the four logs of the u-hat writer under code/pk02/out/. In files carried over from the original runs, P also rebinds the code tokens that name a program (section 4).

In place of the original records, records/ contains the outputs of Table A.1 under the names used in sections 1 to 5 of the supplement. The original records are under records/original_T, with T applied but neither G nor P. The rerun outputs of record A and of the certificate of Proposition B.13 stay with their programs, under code/pk21/p2/a/out and code/pk22/w1/rc_cert/out, and the originals of nine of these outputs are under records/original_T/strip_a and records/original_T/strip_ne. The certified forms of the other 85 outputs under code/ are under records/original_T/code/, at the paths of the outputs (section 6.2). The programs and the files read by them are under code/ and data/. They have T and P applied, and the programs whose gates were changed have G applied as well. The programs behind Proposition 5.44, Remark 5.45, Lemma A.2 and Lemma A.3 also have copies under records/, byte-identical to the files that ran. The item manifest code/acc/ITEM_MANIFEST_v1.tsv (9a142db7) has one row for each of 1755 carried items checked by the two-producer rule, and the second item manifest code/acc/ITEM_MANIFEST_M_v1.tsv (dab9042d) has one row for each of the eight c3 records of the runner code/pk22/m3/m3_run_v1_9_3_px22_c3_1.py, six of which are read by the certificate of Proposition B.13. The row of an item records the item's archive path, its original checksum, its released checksum, the versions of T and P applied to it, and the checksum of its original producer.

The correspondence table CORRESPONDENCE_release_N.tsv covers every file under code/, data/ and records/, as well as the Lean sources of lean/StripIII_v2, and then lists the archived files that do not ship. The files in the table include every file named in sections 1 to 5 of the supplement, as well as the records, key-value files and data read by the runs, other than carried items. For each file the table states the file's original checksum, the path and checksum of the released file, the change, and the file's twin (the same bytes at another path), where there is one. A dash in place of the original checksum marks a file with no original: a file added by G or P, a rerun output of a regenerated family, an acceptance log, or a file written for the spot regenerations. The header of the table lists the classes of change. Among them, D is an edit of docstrings or comments only (in a program that stays the same by its syntax tree, or in a Lean source that equals its original once every comment is removed), and for an archived file that does not ship, the class says why: superseded, with the note of the file; replaced by lean/StripIII_v2, for a Lean source of the tree lean/StripIII_v1 of release_M; or not shipped, with the class of the file (out:tables, out:superseded, out:bookkeeping, out:reports or out:notes for a file of the record manifests of the middle-row runs, and out:pinned-input for a file that lies outside these manifests and is pinned by a shipped record of a carried producer).

MANIFEST_release_N.sha256 lists the checksum of every file of the archive except itself. Provenance lines are the SOURCE lines of records and the check lines of run consoles. Where a provenance line cites a short checksum of 8 or 16 hexadecimal digits, the checksum names the archived bytes. CORRESPONDENCE_release_N.tsv maps each archived checksum to the shipped file. Two check lines of code/pk23/cw/out/cw_comb_v2_2_a.out, however, cite the moment tables psixy_exact_d_v2_n4.json and psixy_exact_d_v2_n3.json, which do not ship and have no row in the correspondence table.

Two checks compared the released files with the original files. They use the private table of T, so they cannot be repeated from the archive alone. Check A rebuilt the released files byte for byte from the original files, or, for the four programs of release_M whose docstrings alone were edited, from the edited copies (which T-v7 leaves unchanged); the Lean sources of lean/StripIII_v2 are checked as section 2.3 describes. Check B located every change in every released file at a listed site of T, G or P and reported no problem. In the final archive no pin is left provisional, that is, waiting for a file that a rerun had still to make. A scan of the archive looked for machine identifiers, cloud identifiers, accounts, e-mail addresses, network addresses, absolute paths, home paths, operating-system images and affiliations. It found none apart from the archive root /mnt/g2/release/root, which the released files expect, and one chance match inside a hexadecimal checksum in code/pk22/m3/out/m3ref_px22_v1_5_P16CS4.4.p5_z9sym.out.

Against the published release_M (4,419 files with its REVERIFICATION.md), release_N holds 4,334 files unchanged, among them the root files LICENSE and LICENSE-TEXT. 57 files take the place of files of release_M: MANIFEST_release_N.sha256, README_release_N.md, CORRESPONDENCE_release_N.tsv, RUNS_M2_release_N.tsv, BOX_RUNS_release_N.tsv, this document, the driver rerun_m2.py with two added masks (section 2.1), the Lean manifest lean/MANIFEST_lean_N.sha256 in place of lean/MANIFEST_lean_M.sha256, and 49 Lean files in new versions (21 in lean/G2Kernel_La_v1_7, 26 in lean/G2Kernel_Lb_p13, and the rebuild summaries of the two trees, as section 2.3 describes). 28 files of release_M do not ship: the Lean tree lean/StripIII_v1 (26 files) and the two rebuild logs of that tree; lean/StripIII_v2 takes their place (section 2.3). release_N adds 838 files: the root tables (MIDROW_RUNS_release_N.tsv and RERUN_PARTS_release_N.tsv), 794 files for the middle-row results of the paper (Propositions B.22 and B.24), and 42 files for the Lean copy (the 40 files of lean/StripIII_v2 and two files in lean/rebuild/). The package has 5,229 files in all. The 794 additions are 437 run outputs and records, 164 inputs, 159 programs, 29 manifests and five documents. In CORRESPONDENCE_release_N.tsv the additions have these changes: identical 205, T 289, P 47, T+P 199, T+G 10, T+G+P 37 and rerun 7; the 35 Lean sources of lean/StripIII_v2 are D. The 794 additions are the files opened by the record manifests of the certified middle-row runs (without the moment tables of the tab16c folders), together with the inputs carried for the runs that are not repeated. The additions went through T, G and P like the earlier files. The latest version of T, T-v8, extends T-v7 by a folder row and by rows for names in file names, and it leaves every file of release_L and release_M byte-identical. On the additions, G changes text lines only: it removes verdict words and the names of review files but keeps the sentences. Table C.2 classifies the difference of each program added in release_N, as Table C.1 does for release_M. Certified runs pin some review documents as inputs. release_M ships them as runtime inputs under code/rv01 and code/rv03, and this document names them only by their package paths.

Against version 1 of the software record (10.5281/zenodo.24410346), this version replaces five files: CORRESPONDENCE_release_N.tsv, rerun_m2.py (section 2.1), code/pk07/kt_s9h_v1_3_2.py with its documentation manifest code/pk07/MANIFEST_kt_s9h_v1_3_2.txt (R5, section 2.1), and code/pk11/kt_s8rf_v1.py (section 2.1). It adds 464 files: ten root files (cmp_certified.py, CERT_PAIRS_release_N.tsv, CERT_MASKS_release_N.tsv, P_MAP_release_N.tsv, plants_midrow.py, PLANTS_MIDROW_release_N.tsv, PREFIX_PINS_release_N.tsv and the three slot manifests), leanfull/s0 (17 files), leanfull/s1 (30) and leanfull/s3 (57), records/original_T/code (85), records/plants_midrow (14) and records/step3 (232), the 18 pinned files of sections 2.1 and 4, and the T image of the table that code/pk11/kt_s8rf_v1.py pins. README_release_N.md, this document and MANIFEST_release_N.sha256 take the place of those of version 1.

Three further checks cover the additions. G9 checks the pin closure: in the shipped .kv and .json records of the certified middle-row runs, every full or 16-digit checksum names a shipped file, a producer field or a file that does not ship and whose class is stated. A producer field is the checksum of a program, kept in a data file as provenance. The stated classes are review documents (class out:reports of the correspondence table) and the pinned inputs of carried producers outside the record manifests (class out:pinned-input). G10: the reruns of the two middle-row runs reproduce the shipped records (section 2.1). G11: no file of a tab16c folder ships, and no Lean build product ships. All three passed.

## 6. Details of the checks

### 6.1 Acceptance of carried items

A released program that reads a carried item with two possible producers decides whether to accept it by the two-producer rule of
code/acc/acc2_v1.py (655579ea). An item remade with the released code must name the checksum of the released producer. An item carried
over must name the checksum of the original producer, and its bytes must equal its row in the item manifest. Each decision is logged, and the logs of the runs in Table A.1 are in records/acc2. Table A.1 has these counts for each output: original (a carried item accepted), cleaned (an item remade and accepted), and refused. Other counts, named carried and not-carried, tally provenance checks, which test whether a
record equals its row in the item manifest. The acc2 gates of the runs in Table A.1 accepted every input item that they checked, as original or as cleaned. The 24 decision-logging runs of the certificate of Proposition B.13 record only provenance checks, 432 in all, and each of these checks found the checked record equal to its row in the second item manifest (carried). The items refused were the programs' own controls, as in the original runs: the planted producer checksum of code/pk08/px08_trbhcert_v2.py, behind records/S4d/run_N4.out and run_N3.out, as well as the synthetic headers that code/pk04/m3_run_r0b_v1_4.py must refuse.

The runs with a dash in Table A.1 log no decision, and their inputs are bound otherwise. The cover checks of Theorem 6.6 read the interval items of their bundles by path, and these items are bound by the release manifest and by the bundle checksum lists, which P recomputes. The law certificates of S8, the first runs of S4(a) and the check of (H) pin every input by its full checksum, which P recomputes, and they stop at any mismatch. The regenerated runs log no decision, since the two-producer rule chooses between the two producers of a carried item. The inputs of the regenerated runs are bound by the checksums pinned in the programs of these runs if the programs have pins, and otherwise by the release manifest.

### 6.2 The comparison rules

The driver rerun_m2.py compares each output with its shipped copy, masking timing and memory fields. Apart from these fields, a differing line passes only if it is a self-checksum line or if it replaces the checksum in the shipped line by the checksum of a file written by the run that produced the output. The driver of release_N is that of release_M with two added masks, each limited to named fields in named files. The first mask covers the per-row timings t_in=, t_k=, t_p= and t=, which change from run to run, in the four hub_cover outputs code/pk05/out/hubcert_v1e_cover3_20_50.out, hubcert_v1e_cover3_50_100.out, hubcert_v1e_cover4_20_50.out and hubcert_v1e_cover4_50_100.out. The second mask covers the tag of the stray output on the IMPORT line of code/pk12/out/p212_v1_3_6_2/out_kt_p212_cert_v1_3_6_2_cert_final.out: the tag is r51 instead of r50 when p212pre has run first on the same copy of the archive. Planted controls still fail: a changed digit in a non-timing field of a masked hub_cover line, a changed chunk name on the IMPORT line, and a changed tag in the output of p212pre, where no mask applies. The validation of release_L had masks of its own for the fields of both added masks, and the driver of release_M did not.

The comparison with the certified outputs follows the rules below.

Each output in Table A.1 was compared line by line with its certified output after the original names had been replaced by the neutral names of T. The certified outputs of the 157 outputs under records/ are at the same paths under records/original_T. These 157 outputs include all those named in sections 1 to 5 of the supplement apart from the outputs of the two middle-row runs. The other 27 outputs, under code/, are the log code/pk07/out/out_kt_s9h_v1_2_vsweep_cplus.out and the 26 intermediate files of code/pk08/px08_a2cert_v1.py behind ${\rm A2}_N$. Their certified forms are under records/original_T/code/, at the paths of the outputs. The correspondence table lists these 27 outputs as files with no original. The 62 outputs of the record A checks and of the certificate of Proposition B.13 are under code/ as well. The original checksum of each of them is in the correspondence table; the certified forms of nine are under records/original_T/strip_a and records/original_T/strip_ne, and those of the other 53 are under records/original_T/code/, at the paths of the outputs. The five outputs of the two middle-row runs are under code/pk24/mr_engine/. Their certified forms are under records/original_T/code/ as well, and MIDROW_RUNS_release_N.tsv keeps the archived checksum of each. The 85 certified forms under records/original_T/code/, 119,586,772 bytes in all, have T applied but neither G nor P. 80 of them equal the archived checksum recorded in CORRESPONDENCE_release_N.tsv, MIDROW_RUNS_release_N.tsv or the output manifest of their producer, and five have no recorded checksum: the four manifests written by code/pk08/px08_a2cert_v1.py and the log out_kt_s9h_v1_2_vsweep_cplus.out. With the 166 certified forms of version 1 of the software record (10.5281/zenodo.24410346), records/original_T holds the certified form of each of the 251 outputs. An output and its certified output must have the same number of lines, and a pair of differing lines
passes in one of these cases:

- the lines agree once the values of CPU time, elapsed time, memory and UTC timestamps are masked (time)
- the lines agree outside hexadecimal tokens of 8 to 64 digits, and each pair of differing tokens is one of these: the original and the released checksum of one archive file (mapped P); the archived checksum of a certified output or of the file its run writes, or the checksum of the certified form under comparison, paired with the checksum of its rerun output when the rerun output has itself passed (mapped rerun); or equal-length prefixes of either kind of pair (mapped P-prefix, mapped rerun-prefix)
- the lines differ by one of the eight recorded masks:
  - two for the count of files in the C-HASH line, that is, one for each S9(i) output: the new count must be smaller than the original count by exactly two (recorded)
  - one for the time fields of the outputs of Theorem 6.9, one for the tag of the scratch chunk written by the S9(i) runs when they import S8, and one for the tag of the stray output written by the runs of the certificate of Proposition B.13 when they import the S8 module, all three masked freely and counted under time
  - three for the INPUTS digest lines, one for the final S8 output, one for both S9(i) outputs and one for the S9(i) record: in each of these lines the original value must be the original digest, and the new value is the digest of the run's own inputs (G-ORIG pair)
- the lines, or a block of consecutive lines, hold the same entries in another order, in the output of a program that sorts by a name changed by T.
  Each side is then sorted by its own names, and the entries must match one to one (resorted; Table A.1 says resorted fields when the entries lie within one line, and resorted lines when they form a block of lines).
  One block carries numbered keys: the record of the certificate of Proposition B.13 numbers the files that it pins as PIN_01 to PIN_28, in the sorted order of their paths, and T renamed these paths, so for 27 of the 28 keys the two sides name another file. In this block the values are matched as a set, one to one under the rules above, and the value under a key is not compared with the value under the same key on the other side. The comparison behind Table A.1 compared only the set of values and did not look at the keys. cmp_certified.py, in its function renumbered (l.225-234), checks in addition that the keys run from PIN_01 to PIN_28 on both sides, in the same order (l.231), and that the values of the output are in sorted order (l.234), and it matches the values one to one through match_perm (l.159-166). Table A.1 counts the 27 lines of this block as resorted lines.
- the lines differ only in the record folder of a middle-row run (run folder): the rerun writes into a record folder whose name ends in .rerun, while the certified run started one folder higher than the rerun. The paths of the certified run therefore begin with pk24/mr_engine/, whereas those of the rerun begin with mr_engine/.

A pair of differing stated file sizes passes when the two sizes are the original and the released size of a mapped file (mapped size).
JSON outputs that fail line by line are compared as parsed JSON under the same rules. Every JSON line, too, is compared as parsed JSON. To pass, an END line must be a self-checksum verified on both sides. No line of the outputs of Table A.1 fell under the JSON rule or the END-line rule. Any other difference
fails. Every output in Table A.1 passed, so each reproduces its certified output up to the rules of this section. The cases that occurred are named in the last column of Table A.1, with the number of lines in each case.
An output equal to its certified output byte for byte is marked "identical". The comparison program cmp_certified.py ships at the root with three tables: CERT_PAIRS_release_N.tsv, one row for each of the 251 outputs (the output, the file written, the certified form, and the archived checksum and size); P_MAP_release_N.tsv, the map P of checksums and sizes (5,142 rows: the archived checksum and size, and the released path, checksum and size); and CERT_MASKS_release_N.tsv, the eight recorded masks with the paths of their outputs. It needs no private table: python3 -I -B cmp_certified.py REPORT compares the shipped outputs, and with --rerun it compares the copies that rerun_m2.py leaves. On the shipped outputs all 251 pass, each with the verdict of Table A.1 (226 rows by path, and the 25 empty console files of one row; the 10 program rows of Table A.1 are not run outputs). 41 outputs are identical, and the differing lines passed under these rules: mapped P 1,409, mapped P-prefix 315, mapped rerun 137, mapped rerun-prefix 216, mapped size 26, G-ORIG pair 4, recorded 2, time 1,806, run folder 5, resorted fields 1, resorted lines 29, 27 of them one block whose keys are renumbered (the PIN lines of the record of the certificate of Proposition B.13, which cmp_certified.py reports as resorted lines with renumbered keys); no line needed the self-checksum rule. Without the raw originals, the resorted rules check only the order of the output, and the self-checksum rule only the value of the output; the docstring of the program says so. Checks A and B still need the original bytes and stay private (section 5).

### 6.3 The spot regeneration in detail

The original record of a regenerated item is a carried item unless records/spot/SPOT_LISTING.tsv marks it as archived only. The comparison of each spot regeneration uses the rules of section 6.2 with masks of its own, together with the rules for the W2M chain given below. Every
program that produced carried items appears in records/spot/C5_table_v11.tsv (173d7ef7) or, for the producers added in release_M, in Table B.1, with the result of its regeneration or the reason for its exemption. The column "gated" of the C5 table reads "yes" when a shipped program holds the full original checksum of the producer program as the constant that a changed gate uses to accept the carried items of that producer. It reads "no" when no shipped program holds that checksum. For the programs of the strip-cover bundle it reads "strip-cover": the items of these programs are bound by the checksum lists of their bundles (section 6.1). For the two plants of the output check it reads "G-v8 assert". The outputs of the spot regeneration runs and the inputs written for them are archived under records/spot/, in one folder per run, with the inputs in the runtime/ subfolder of the run's folder. records/spot/SPOT_LISTING.tsv (940f93b0) lists every file under records/spot/ apart from the two listings (itself and records/spot/SPOT_LISTING_M.tsv) and from the 12 outputs of the box control jobs under records/spot/MBOX/. The second listing, records/spot/SPOT_LISTING_M.tsv (811ff683), lists these outputs in the same columns (see the end of this section). Each row of SPOT_LISTING.tsv contains:

- the checksum of the file as shipped
- a second checksum: for a run output, the checksum of the raw output (as the run wrote it), and for any other file, the checksum of the shipped copy
- the path of the original compared with the file. The path is marked (archived only) if the archive has no file there.
- the archived checksum of that original. In the correspondence table it is the original checksum of the listed file, and of the file at that path if there is one.
- the result

A file at the path of an original is the T or T+P image of that original, so its checksum can differ from the archived value.

The difference between a shipped program and the version that ran falls into the classes of Table B.1. If a module determines the class, the cell of Table B.1 names that module. Some regenerations needed more than one run or an input written for the regeneration.

- px08_trbhcert_v1_1 and px08_trbhcert_v1_2 accept node partials only from px08_trbhcert_v1: their header check requires the
  released producer, which the carried partials do not name. The released px08_trbhcert_v1 regenerated these partials first, in nine runs at $N=4$ and nine at $N=3$. The two later versions read the regenerated partials through manifests written for the runs of these two versions.
- m2b_rep_v1_5 refuses carried inputs, so its inputs were regenerated first by the released m2b_cert_v1_1, m2b_cert_v1_4 and
  m2b_floatref_v2, in 11 runs.
- The regenerations of px08_m2bc4 and px08_m2bb4 read manifests written for them. The manifests list the carried partials that the regenerations use, each partial by its released checksum.
- The u-hat writer code/pk02/kt_uhat_asm_v1_8.py reads the W2M record of $N=4$. The program m3_run_r0m_v1_2 computes this record of the W2M mirror windows in successive work pieces, each limited in CPU time and resuming from the hand-off of the piece before. The carried W2M record names the
  original m3_run_r0m_v1_2 as its producer, while the released writer refuses records that do not name the released producer. The W2M record
  was therefore regenerated first, by the released m3_run_r0m_v1_2, and the result of that run is shown part by part in Table B.1. The regenerated W2M record and two further files agree line by line with their originals, while three other files agree with their originals outside their block of W2M pieces. Of the pieces with the same
  start and end as the archived pieces, all agree line by line except one, whose sole difference is its LIM parameter, the program's self-imposed CPU-time limit. The two pieces that were cut differently are listed by their structure, and every regenerated piece is
  valid or stopped cleanly at its limit. The writer reads only the W2M record and the assembled output of the run of m3_run_r0m_v1_2, not the pieces. A piece that stops at its limit writes no hand-off, and the next piece, with a longer limit, redoes the work of the stopped piece. The assembly checks that the pieces cover every key in order and that cutting and resuming gives the same results. The driver of the run of m3_run_r0m_v1_2 is archived with five substitutions: two in its header, one in the path of its interpreter, one in the path of its niceness wrapper and one in the name of a variable. The writer then ran on the regenerated record and on the assembled output of that run. The run configuration that it used differs from the shipped configuration only in its checksum values, each replaced by the checksum of the file that the writer reads. Both outputs of the writer passed. The archived outputs name the checksum of the original configuration, and the comparison maps this checksum to the checksum of the run configuration. The comparison also adds one mask, on line 48: on that line the writer prints the refusal message of its own planted control, cut to the first 160 characters. Because T shortened a path in the message, the cut keeps two more characters, both zeros.

The other producers added in release_M were not regenerated, each for the reason given in Table B.1. The spot regeneration reran the 12 control jobs at $n=3$ and $n=4$ of the box runs of Propositions B.14 and B.15, one run per job, with the released engines, on a release_M pre-release whose files under code/pk23 are byte-identical to those of the released archive. Each output was compared with the shipped copy of the job's output under the rules of section 6.2, with one further mask for the Python version, since the box ran Python 3.13.5 and the regenerations ran Python 3.14.4. All 12 passed. The outputs are under records/spot/MBOX/, and records/spot/SPOT_LISTING_M.tsv (811ff683) lists them in the columns of SPOT_LISTING.tsv, with the shipped output as the file compared. The control job at $n=6$ of run 20261118T045359Z and the other jobs of the box runs were not regenerated (section 4). The producers added in release_N were not regenerated (section 2.4).

## Appendix A. The rerun outputs

Table A.1 lists the outputs of the 130 runs of RUNS_M2_release_N.tsv, and Table A.2 the reruns of section 2.1 made for this version.

**Table A.1.** Outputs of the reruns with the released programs, by family. Carried inputs: assembly and final steps re-executed on carried-over items. Regenerated: recomputed from the start. Columns:

- producer: by its archive name, with the first eight digits of its checksum
- acceptance log: the acceptance decisions logged by the run (section 6.1), with a dash where the run logged none
- comparison: the result of the comparison of section 6.2, with the number of lines in each case

The checksum of each output is in MANIFEST_release_N.sha256 and, with its original, in CORRESPONDENCE_release_N.tsv.

The 25 console logs of the NE certificate runs (code/pk22/w1/rc_cert/out/console15_cert_*.txt) are empty files, as are those of the archived runs: each run sends its standard output and error to its console log, but the certifier prints only when its arguments or output folder are wrong, and the certifier writes its results to its .out file (and the record run writes results to its .kv file).

| output | label | producer | acceptance log | comparison |
|---|---|---|---|---|
| records/route_H/union_20_300.out | carried inputs | code/pk05/ru2_ledger_union.py (9d85e5d8) | original=358 | PASS mapped P=2 |
| records/route_H/union_300_350.out | carried inputs | code/pk05/ru2_ledger_union.py (9d85e5d8) | original=54 | PASS mapped P=2 |
| records/strip_cover/N4_0099_3.txt | carried inputs | code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_v2/code/checkcover.py (87e028c2) | — | PASS identical file=1 |
| records/strip_cover/N3_0099_3.txt | carried inputs | code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_n3/code4/checkcover.py (87e028c2) | — | PASS identical file=1 |
| records/strip_cover/N4_3_20.txt | carried inputs | code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_cover_cv/code8/cover_check.awk (3537d2a6) | — | PASS identical file=1 |
| records/strip_cover/N3_3_20.txt | carried inputs | code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_cover_n3/code8/cover_check.awk (3537d2a6) | — | PASS identical file=1 |
| records/S1S2/S5S7_entries_N4.out | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=8 mapped P-prefix=1 mapped rerun=10 time=3 |
| records/side/code/pk03/out/m3_m2_N4_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/side/code/pk03/out/m3_b5_N4_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/side/code/pk03/out/m3_clT_N4_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/side/code/pk03/out/m3_binding4_N4_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/side/code/pk03/out/m3_endw_N4_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/S1S2/S8_entries_1_N4.out | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=6 mapped P-prefix=1 mapped rerun=8 time=3 |
| records/side/code/pk03/out/m3_s8v3_D_N4_J300_v1_8_1.json | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=17 |
| records/side/code/pk03/out/m3_s8v3_E2_N4_J300_v1_8_1.json | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=17 |
| records/side/code/pk03/out/m3_s8v3_E3_N4_J300_v1_8_1.json | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=17 |
| records/side/code/pk03/out/m3_s8v3_FF_N4_J300_v1_8_1.json | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=17 |
| records/S1S2/S8_entries_2_N4.out | carried inputs | code/pk03/m3_run_v1_8_2.py (09a64b66) | original=21 | PASS mapped P=2 mapped P-prefix=1 mapped rerun=2 mapped size=1 time=2 |
| records/side/code/pk03/out/m3_s8v3_N_N4_J300_v1_8_2.json | carried inputs | code/pk03/m3_run_v1_8_2.py (09a64b66) | original=21 | PASS mapped P=17 |
| records/S1S2/S8_entries_3_N4.out | carried inputs | code/pk03/m3_run_v1_9_3.py (34abe374) | not-carried=10 original=100 | PASS mapped P=3 mapped P-prefix=2 mapped rerun=4 time=3 |
| records/side/code/pk03/out/m3_s8v2_H_N4_J300_v1_9_3.json | carried inputs | code/pk03/m3_run_v1_9_3.py (34abe374) | not-carried=10 original=100 | PASS mapped P=18 |
| records/side/code/pk03/out/m3_s8v2_S4_N4_J300_v1_9_3.json | carried inputs | code/pk03/m3_run_v1_9_3.py (34abe374) | not-carried=10 original=100 | PASS mapped P=18 |
| records/S1S2/S8_law_1_N4.out | carried inputs | code/pk03/m3_lawcert_v1_1.py (981f0c12) | — | PASS mapped P=1 mapped P-prefix=4 mapped rerun=1 time=2 |
| records/side/code/pk03/out/m3_lawcert_v1_1_N4.json | carried inputs | code/pk03/m3_lawcert_v1_1.py (981f0c12) | — | PASS mapped rerun=5 |
| records/S1S2/S8_law_2_N4.out | carried inputs | code/pk03/m3_lawcert_v1_2.py (79ff6ca2) | — | PASS mapped P=1 mapped P-prefix=4 mapped rerun=1 time=7 |
| records/side/code/pk03/out/m3_lawcert_v1_2_N4.json | carried inputs | code/pk03/m3_lawcert_v1_2.py (79ff6ca2) | — | PASS mapped rerun=2 |
| records/S1S2/S9i_entries_E_N4.out | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=1 mapped P-prefix=3 mapped rerun=12 mapped rerun-prefix=2 mapped size=6 time=2 |
| records/side/code/pk03/out/m3_es_D3_dL0_N4_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=24 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D3_dLm1_N4_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=24 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D4M_dL0_N4_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=24 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D4M_dLm1_N4_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=22 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D4_dL0_N4_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=24 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D4_dLm1_N4_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=22 mapped rerun=1 |
| records/S1S2/S9i_entries_R_N4.out | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=254 refused=2 | PASS mapped P=1 mapped P-prefix=123 mapped rerun=12 mapped size=6 time=3 |
| records/side/code/pk03/out/m3_r0b_D4L0_N4_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=254 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_D4ML0_N4_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=254 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_FA_N4_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=254 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_W2_N4_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=254 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_W3e_N4_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=254 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_W3f_N4_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=254 refused=2 | PASS mapped P=25 |
| records/S1S2/S5S7_entries_N3.out | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=8 mapped P-prefix=1 mapped rerun=10 time=3 |
| records/side/code/pk03/out/m3_m2_N3_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/side/code/pk03/out/m3_b5_N3_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/side/code/pk03/out/m3_clT_N3_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/side/code/pk03/out/m3_binding4_N3_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/side/code/pk03/out/m3_endw_N3_J300_v1_7.json | carried inputs | code/pk03/m3_run_v1_7.py (64533925) | original=18 | PASS mapped P=14 |
| records/S1S2/S8_entries_1_N3.out | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=5 mapped P-prefix=1 mapped rerun=8 time=3 |
| records/side/code/pk03/out/m3_s8v3_D_N3_J300_v1_8_1.json | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=17 |
| records/side/code/pk03/out/m3_s8v3_E2_N3_J300_v1_8_1.json | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=17 |
| records/side/code/pk03/out/m3_s8v3_E3_N3_J300_v1_8_1.json | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=17 |
| records/side/code/pk03/out/m3_s8v3_FF_N3_J300_v1_8_1.json | carried inputs | code/pk03/m3_run_v1_8_1.py (0d3388d2) | original=8 | PASS mapped P=17 |
| records/S1S2/S8_entries_2_N3.out | carried inputs | code/pk03/m3_run_v1_8_2.py (09a64b66) | original=24 | PASS mapped P=2 mapped P-prefix=1 mapped rerun=2 mapped size=1 time=4 |
| records/side/code/pk03/out/m3_s8v3_N_N3_J300_v1_8_2.json | carried inputs | code/pk03/m3_run_v1_8_2.py (09a64b66) | original=24 | PASS mapped P=17 |
| records/S1S2/S8_entries_3_N3.out | carried inputs | code/pk03/m3_run_v1_9_3.py (34abe374) | not-carried=10 original=112 | PASS mapped P=3 mapped P-prefix=2 mapped rerun=4 time=1 |
| records/side/code/pk03/out/m3_s8v2_H_N3_J300_v1_9_3.json | carried inputs | code/pk03/m3_run_v1_9_3.py (34abe374) | not-carried=10 original=112 | PASS mapped P=18 |
| records/side/code/pk03/out/m3_s8v2_S4_N3_J300_v1_9_3.json | carried inputs | code/pk03/m3_run_v1_9_3.py (34abe374) | not-carried=10 original=112 | PASS mapped P=18 |
| records/S1S2/S8_law_1_N3.out | carried inputs | code/pk03/m3_lawcert_v1_1.py (981f0c12) | — | PASS mapped P=1 mapped P-prefix=4 mapped rerun=1 time=2 |
| records/side/code/pk03/out/m3_lawcert_v1_1_N3.json | carried inputs | code/pk03/m3_lawcert_v1_1.py (981f0c12) | — | PASS mapped rerun=5 |
| records/S1S2/S8_law_2_N3.out | carried inputs | code/pk03/m3_lawcert_v1_2.py (79ff6ca2) | — | PASS mapped P=1 mapped P-prefix=4 mapped rerun=1 time=5 |
| records/side/code/pk03/out/m3_lawcert_v1_2_N3.json | carried inputs | code/pk03/m3_lawcert_v1_2.py (79ff6ca2) | — | PASS mapped rerun=2 |
| records/S1S2/S9i_entries_E_N3.out | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=1 mapped P-prefix=3 mapped rerun=12 mapped rerun-prefix=2 mapped size=6 time=2 |
| records/side/code/pk03/out/m3_es_D3_dL0_N3_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=24 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D3_dLm1_N3_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=24 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D4M_dL0_N3_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=24 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D4M_dLm1_N3_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=22 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D4_dL0_N3_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=24 mapped rerun=1 |
| records/side/code/pk03/out/m3_es_D4_dLm1_N3_J300_v1_3.json | carried inputs | code/pk04/m3_run_es_v1_3.py (1deb61e1) | not-carried=10 original=22 | PASS mapped P=22 mapped rerun=1 |
| records/S1S2/S9i_entries_R_N3.out | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=253 refused=2 | PASS mapped P=1 mapped P-prefix=123 mapped rerun=12 mapped size=6 time=3 |
| records/side/code/pk03/out/m3_r0b_D4L0_N3_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=253 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_D4ML0_N3_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=253 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_FA_N3_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=253 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_W2_N3_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=253 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_W3e_N3_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=253 refused=2 | PASS mapped P=25 |
| records/side/code/pk03/out/m3_r0b_W3f_N3_J300_v1.json | carried inputs | code/pk04/m3_run_r0b_v1_4.py (7a5fdf75) | cleaned=2 not-carried=10 original=253 refused=2 | PASS mapped P=25 |
| records/S3a/run_N4.out | carried inputs | code/pk08/px08_rtrcert_v1.py (28be44e1) | original=10 | PASS mapped P=1 time=1 |
| records/S3a/run_N3.out | carried inputs | code/pk08/px08_rtrcert_v1.py (28be44e1) | original=10 | PASS mapped P=1 time=1 |
| records/S3bd/run.out | carried inputs | code/pk02/m2b_asm_v1.py (27560e56) | carried=6 not-carried=6 original=22 | PASS mapped P=1 mapped P-prefix=6 mapped rerun=1 |
| records/S3bd/record.txt | carried inputs | code/pk02/m2b_asm_v1.py (27560e56) | carried=6 not-carried=6 original=22 | PASS mapped P=42 resorted fields=1 time=1 |
| records/S4a/run_1_N4.out | carried inputs | code/pk05/s4c_m2ba.py (e86784a3) | — | PASS mapped P=1 time=3 |
| records/S4a/run_1_N3.out | carried inputs | code/pk05/s4c_m2ba.py (e86784a3) | — | PASS mapped P=1 time=4 |
| records/S4a/run_3_N4.out | carried inputs | code/pk08/px08_m2bb4.py (e6a974a7) | original=14 | PASS mapped P=1 resorted lines=2 time=1 |
| records/S4a/run_2_N4.out | carried inputs | code/pk08/px08_px03_v4.py (824a3ca2) | original=7 | PASS mapped P=1 time=1 |
| records/S4a/run_3_N3.out | carried inputs | code/pk08/px08_m2bb4.py (e6a974a7) | original=14 | PASS mapped P=1 time=1 |
| records/S4a/run_2_N3.out | carried inputs | code/pk08/px08_px03_v4.py (824a3ca2) | original=8 | PASS mapped P=1 time=1 |
| records/S4a/run_4_N4.out | carried inputs | code/pk08/px08_m2bc3.py (0e8f2c20) | original=12 | PASS mapped P=1 time=1 |
| records/S4a/run_4_N3.out | carried inputs | code/pk08/px08_m2bc4.py (6527d21b) | original=12 | PASS mapped P=1 time=1 |
| records/S4b/run_N4.out | carried inputs | code/pk08/px08_trbcert_v1_1.py (6a851374) | original=10 | PASS mapped P=1 time=1 |
| records/S4b/run_N3.out | carried inputs | code/pk08/px08_trbcert_v1_1.py (6a851374) | original=10 | PASS mapped P=1 time=1 |
| records/S4d/run_N4.out | carried inputs | code/pk08/px08_trbhcert_v2.py (10662078) | original=42 refused=2 | PASS mapped P=5 time=1 |
| records/S4d/run_N3.out | carried inputs | code/pk08/px08_trbhcert_v2.py (10662078) | original=42 refused=2 | PASS mapped P=5 time=1 |
| records/side/code/pk07/out/cplus_sidecheck_v1.kv | carried inputs | code/pk07/cplus_sidecheck_v1.py (5a30003f) | — | PASS mapped P=2 mapped rerun=3 |
| records/S8/run_final.out | carried inputs | code/pk11/kt_s8_cert_v1_14_3.py (34b2e59a) | original=21 | PASS G-ORIG pair=1 mapped P=1 mapped P-prefix=6 mapped rerun=1 mapped rerun-prefix=2 time=1 |
| records/S8/record.kv | carried inputs | code/pk11/kt_s8_cert_v1_14_3.py (34b2e59a) | original=21 | PASS mapped P=62 mapped rerun=33 |
| records/S9i/run_pre.out | carried inputs | code/pk12/kt_p212_cert_v1_3_6_2.py (f353808c) | carried=2 | PASS G-ORIG pair=1 mapped P=1 mapped P-prefix=7 mapped rerun-prefix=181 recorded=1 time=1 |
| records/S9i/run_final.out | carried inputs | code/pk12/kt_p212_cert_v1_3_6_2.py (f353808c) | cleaned=2 original=4 | PASS G-ORIG pair=1 mapped P=1 mapped rerun=1 recorded=1 time=2 |
| records/S9i/record.kv | carried inputs | code/pk12/kt_p212_cert_v1_3_6_2.py (f353808c) | cleaned=2 original=4 | PASS G-ORIG pair=1 mapped P=1 |
| records/W4free/recomputation.out | regenerated | records/W4free/recomputation.py (33de0826) | — | PASS identical file=1 |
| records/weak_coupling/enclosures.out | regenerated | records/weak_coupling/enclosures.py (fb58c1f1) | — | PASS identical file=1 |
| records/weak_coupling/eval_60_digits.out | regenerated | records/weak_coupling/eval_60_digits.py (1a730c57) | — | PASS identical file=1 |
| records/weak_coupling/eval_50_digits.out | regenerated | records/weak_coupling/eval_50_digits.py (94e6d3f3) | — | PASS identical file=1 |
| records/hub_cover/run_N3_20_50.out | regenerated | code/pk05/hubcert_v1e.py (fbed2d93) | — | PASS mapped P=1 time=37 |
| records/hub_cover/run_N3_50_100.out | regenerated | code/pk05/hubcert_v1e.py (fbed2d93) | — | PASS mapped P=1 time=32 |
| records/hub_cover/run_N4_20_50.out | regenerated | code/pk05/hubcert_v1e.py (fbed2d93) | — | PASS mapped P=1 time=35 |
| records/hub_cover/run_N4_50_100.out | regenerated | code/pk05/hubcert_v1e.py (fbed2d93) | — | PASS mapped P=1 time=32 |
| records/hub_cover/union.out | regenerated | code/pk05/union_check_v1.py (8a25390d) | — | PASS mapped P=2 |
| records/P3xP3_strong/run_cert.out | regenerated | code/pk01/kt_lbu_v1_1.py (424340c0) | — | PASS time=38 |
| records/P3xP3_strong/run_controls.out | regenerated | code/pk01/kt_lbu_v1_1.py (424340c0) | — | PASS time=28 |
| records/P3xP4/run_N3_G01.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=36 |
| records/P3xP4/run_N3_G02.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=38 |
| records/P3xP4/run_N3_G03.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=37 |
| records/P3xP4/run_N3_G04.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=37 |
| records/P3xP4/run_N3_G05.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=27 |
| records/P3xP4/run_N3_G06.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=35 |
| records/P3xP4/run_N3_G07.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=32 |
| records/P3xP4/run_N3_G08.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=31 |
| records/P3xP4/run_N3_G09.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=33 |
| records/P3xP4/run_N3_G10.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=30 |
| records/P3xP4/run_N3_G11.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=38 |
| records/P3xP4/run_N3_G12.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=34 |
| records/P3xP4/run_N3_G13.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=32 |
| records/P3xP4/run_N3_G14.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=36 |
| records/P3xP4/run_N3_G15.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=37 |
| records/P3xP4/run_N3_G16.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=35 |
| records/P3xP4/run_N3_G17.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=33 |
| records/P3xP4/run_N3_G18.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=44 |
| records/P3xP4/run_N3_G19.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=37 |
| records/P3xP4/run_N4_G01.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=33 |
| records/P3xP4/run_N4_G02.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=33 |
| records/P3xP4/run_N4_G03.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=28 |
| records/P3xP4/run_N4_G04.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=41 |
| records/P3xP4/run_N4_G05.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=31 |
| records/P3xP4/run_N4_G06.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=39 |
| records/P3xP4/run_N4_G07.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=37 |
| records/P3xP4/run_N4_G08.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=37 |
| records/P3xP4/run_N4_G09.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=29 |
| records/P3xP4/run_N4_G10.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=38 |
| records/P3xP4/run_N4_G11.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=40 |
| records/P3xP4/run_N4_G12.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=29 |
| records/P3xP4/run_N4_G13.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=33 |
| records/P3xP4/run_N4_G14.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=36 |
| records/P3xP4/run_N4_G15.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=35 |
| records/P3xP4/run_N4_G16.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=32 |
| records/P3xP4/run_N4_G17.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=44 |
| records/P3xP4/run_N4_G18.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=32 |
| records/P3xP4/run_N4_G19.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=38 |
| records/P3xP4/supporting_N4_G03_J500.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=25 |
| records/P3xP4/supporting_N4_G18_J500.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=36 |
| records/P3xP4/control_run.out | regenerated | code/pk06/kt_lbu_g34_pk06_v1.py (7c437dd0) | — | PASS mapped P=1 time=56 |
| records/S5S7/run.out | regenerated | code/pk07/kt_s9h_v1_2.py (1b68e471) | — | PASS mapped P=1 mapped P-prefix=11 mapped rerun=1 mapped rerun-prefix=1 time=21 |
| records/S5S7/export.kv | regenerated | code/pk07/kt_s9h_v1_2.py (1b68e471) | — | PASS mapped P-prefix=4 mapped rerun-prefix=1 |
| records/B4/run.out | regenerated | code/pk08/px08_tau_d3b_v1_1.py (4b92f0db) | — | PASS mapped P=1 mapped rerun=1 |
| records/B4/record.kv | regenerated | code/pk08/px08_tau_d3b_v1_1.py (4b92f0db) | — | PASS mapped P=9 mapped rerun=6 |
| code/pk08/out/px08_a2cert_v1_n4_cov.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=2 |
| code/pk08/out/px08_a2cert_v1_n4_nodes0.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n4_nodes1.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/MANIFEST_nodes_n4_a2cert_v1.sha256 | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped rerun=2 |
| code/pk08/out/px08_a2cert_v1_n4_g0.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n4_g1.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n4_g2.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n4_g3.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n4_g4.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n4_g5.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n4_g6.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n4_g7.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/MANIFEST_parts_n4_a2cert_v1.sha256 | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped rerun=10 |
| records/A2/run_N4.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_cov.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_nodes0.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_nodes1.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/MANIFEST_nodes_n3_a2cert_v1.sha256 | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped rerun=2 |
| code/pk08/out/px08_a2cert_v1_n3_g0.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_g1.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_g2.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_g3.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_g4.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_g5.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_g6.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/out/px08_a2cert_v1_n3_g7.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk08/MANIFEST_parts_n3_a2cert_v1.sha256 | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped rerun=10 |
| records/A2/run_N3.out | regenerated | code/pk08/px08_a2cert_v1.py (5eb405ef) | — | PASS mapped P=1 time=1 |
| code/pk07/out/out_kt_s9h_v1_2_vsweep_cplus.out | regenerated | code/pk07/cplus_sidecheck_v1.py (5a30003f) | — | PASS mapped P=1 |
| records/conjecture_U/u4falsify_v1_A.out | regenerated | code/pk13/code/u4falsify_v1.py (4b8cd631) | — | PASS mapped P=1 |
| records/conjecture_U/u4falsify_v1_B.out | regenerated | code/pk13/code/u4falsify_v1.py (4b8cd631) | — | PASS mapped P=1 time=1 |
| records/conjecture_U/u4falsify_v1_C.out | regenerated | code/pk13/code/u4falsify_v1.py (4b8cd631) | — | PASS mapped P=1 time=1 |
| code/pk21/p2/a/out/a3_bulk_checks_v1.out | carried inputs | code/pk21/p2/a/a3_bulk_checks_v1.py (fbd21200) | — | PASS mapped P=4 mapped rerun=1 |
| code/pk21/p2/a/out/a3_rows_N4_v1.tsv | carried inputs | code/pk21/p2/a/a3_bulk_checks_v1.py (fbd21200) | — | PASS identical file=1 |
| code/pk21/p2/a/out/a3_rows_N3_v1.tsv | carried inputs | code/pk21/p2/a/a3_bulk_checks_v1.py (fbd21200) | — | PASS identical file=1 |
| code/pk21/p2/a/out/n1_export_pair_compare_v1.txt | carried inputs | code/pk21/p2/job27_n1.sh (d00b4c8b) | — | PASS mapped P=6 mapped P-prefix=3 |
| code/pk21/p2/a/out/.rows_t_v1_37.txt | carried inputs | code/pk21/p2/job27_n1.sh (d00b4c8b) | — | PASS identical file=1 |
| code/pk21/p2/a/out/.rows_t_v1_37_1.txt | carried inputs | code/pk21/p2/job27_n1.sh (d00b4c8b) | — | PASS identical file=1 |
| code/pk21/p2/a/out/.rows_14_joint_v1_37.txt | carried inputs | code/pk21/p2/job27_n1.sh (d00b4c8b) | — | PASS identical file=1 |
| code/pk21/p2/a/out/.rows_14_joint_v1_37_1.txt | carried inputs | code/pk21/p2/job27_n1.sh (d00b4c8b) | — | PASS identical file=1 |
| code/pk21/p2/a/out/.rows_14_means_v1_37.txt | carried inputs | code/pk21/p2/job27_n1.sh (d00b4c8b) | — | PASS identical file=1 |
| code/pk21/p2/a/out/.rows_14_means_v1_37_1.txt | carried inputs | code/pk21/p2/job27_n1.sh (d00b4c8b) | — | PASS identical file=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0000_0100.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/console15_cert_*.txt (25 empty files) | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 (24 logs); — (console15_cert_record.txt) | PASS identical file=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0100_0200.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0200_0300.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0300_0400.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0400_0500.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0500_0600.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0600_0700.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0700_0800.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c3_0800_0904.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0061_0141.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0141_0221.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0221_0301.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0301_0381.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0381_0461.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0461_0541.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0541_0621.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0621_0701.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0701_0781.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0781_0861.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=1 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_c4_0861_0904.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_smoke_n3.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_smoke_n4.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun-prefix=1 time=2 |
| code/pk21/p2/a/out/a4_units_crosscheck_v1_1.out | carried inputs | code/pk21/p2/a/a4_units_crosscheck_v1_1.py (dfd3cf16) | — | PASS mapped P=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_final_n3.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun=9 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_final_n4.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | carried=18 | PASS mapped P=1 mapped rerun=11 mapped rerun-prefix=1 time=2 |
| code/pk22/w1/rc_cert/out/out_kt_s8h_rcc_v1_5_cert_record.out | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | — | PASS mapped P=1 mapped rerun=1 time=2 |
| code/pk22/w1/rc_cert/out/ne_rc_record_cert_kt_s8h_rcc_v1_5.kv | carried inputs | code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py (e4243548) | — | PASS mapped P=1 mapped rerun=25 resorted lines=27 |
| code/pk24/mr_engine/MR_ASSEMBLY_cert_m1_v4b_1_n11.kv | carried inputs | code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (28a340e7) | — | PASS mapped P=2 |
| code/pk24/mr_engine/kt_mr_v1_8_4_cert_m1_v4b_1_n11.out | carried inputs | code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (28a340e7) | — | PASS mapped P=6 run folder=2 |
| code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv | carried inputs | code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (28a340e7) | — | PASS mapped P=2 |
| code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv.tail | carried inputs | code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (28a340e7) | — | PASS mapped P=2 |
| code/pk24/mr_engine/kt_mr_v1_8_4_cert_m2_m2cert_1_2_5.out | carried inputs | code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (28a340e7) | — | PASS mapped P=6 run folder=3 |

**Table A.2.** The reruns made for this version of programs that had not been rerun (section 2.1). Each output was compared by cmp_certified.py, under the map P, with the shipped output of the original run. Columns: the program, its items, the files added to the archive for the rerun, the verdict of the run, and the outputs that pass.

| program | items | files added | verdict | outputs that pass |
|---|---|---|---|---|
| code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py | vsweep | — | VALID | 4 of 4 |
| code/pk07/kt_s9h_v1_3_2.py (R5), with G lines 417 and 426 | sweep | — | VALID | 2 of 2 |
| code/pk11/kt_s8f1_v1_3.py | four items | code/pk11/out/out_kt_s8f1_v1_1_n3.out, code/pk11/out/out_kt_s8f1_v1_1_n4.out | VALID for each item | 4 of 4 |
| code/pk11/kt_s8rf_v1.py, re-pinned by P to the T image of one table that it pins | n3, n4 | code/pk15/out/out_kt_p2_14f_v1_n3.out, code/pk15/out/out_kt_p2_14f_v1_n4.out, code/rv01/out_chk_joint_reflect_v1.txt, and the T image of code/pk15/TABLE_P2_12_JOINT_SCREEN_SPRIME_ROUTEA_v1.tsv | VALID for each item | 4 of 4 |
| code/pk08/px08_hsd3b_export_v1_1.py | run | — | VALID | 2 of 2 |
| code/pk03/m3_run_v1_9_3.py, the chains H and S4 at $N=3$ and $N=4$ | 70 items | — | VALID for every item | 16 of 16 in CERT_PAIRS; the 424 table data files equal those of the data record |

For the chains of the m3 runner, CERT_PAIRS lists only the outputs that pass: the consoles and error files of the smoke items and the hand-off records of the entry and resume items. The rebuilt tables are checked against the data record (section 2.1).

## Appendix B. The spot regeneration by program

**Table B.1.** The spot regeneration of the 27 producers added in release_M, which are not listed in records/spot/C5_table_v11.tsv (173d7ef7), together with the rows of the 7 bundle programs and of the 2 plants of the output check (section 2.2). These rows also stand in the C5 table. The rows of the other producers are in the C5 table, with the same columns and the column "gated". records/spot/SPOT_LISTING.tsv (940f93b0) and records/spot/SPOT_LISTING_M.tsv (811ff683) list the files of the regeneration runs. The columns are the program, the first eight digits of the checksum of its original version, the carried items that it produced, the certified runs that read these items, the result (with the runs of a chain), the archive issue used by the regeneration run, the class of Table 2 or of Table C.1, the folder of the run under records/spot/, and notes, among them the reason for an exemption.

| program | producer | items | read by a certified run | result | issue used | program in the release | records | note |
|---|---|---|---|---|---|---|---|---|
| code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_cover_cv/code8/certint6.py | — | cv items | yes | PASS (2 outputs) | release_E | comments only | records/spot/M3E/cv_001/ | plants: OUT exists, copy outside its folder |
| code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_v2/code/certint4.py | — | certint4_S* items | yes | PASS (1 output) | release_E | comments only (module code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_v2/code/certlib.py) | records/spot/M3E/ci4v2_S3_2/ |  |
| code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_n3/code4/certint4.py (the same archived original as code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_v2/code/certint4.py; the two differ only at l.34 and l.706, where each asserts its own package's out/ folder) | — | no item | — | PASS (1 output) | release_E | comments only (module code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_n3/code4/certlib.py) | records/spot/M3D/ci4n3_S3_2/ | runs on pkg_v2 S3_2 arguments with the reconstructed certlib copies; compared with pkg_v2 item |
| code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_n3/code5/o3cert.py | — | o3cert_o3t* items | yes | PASS (1 output) | release_E | identical | records/spot/M3D/o3c_o3t1/ |  |
| code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_n3/code5/o3cert2.py | — | o3cover2 logs and ledgers | yes | PASS (1 output) | release_E | comments only | records/spot/M3E/o3c2_V3_2/ |  |
| code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_cover_n3/code8/o3cert6.py | — | o3cert6_n3 items | yes | PASS (1 output) | release_E | comments only | records/spot/M3E/o3c6_n3_001/ | code8 is the bundle runnable version; code_ran keeps the code as it ran |
| code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_n3/code4/certint5.py | — | no item | — | — | — | — | — | no item in the bundle to regenerate |
| code/pk23/o5/kit_v5/kt_lbu_g37_v1.py, code/pk23/o5/kit_v6/kt_lbu_g37_v1.py, code/pk23/o5/kt_lbu_g37_v1.py | 8677a368 | 77 | no (the record tables and the Lean list fragments) | PASS (2 outputs) | a pre-release of release_M | T-v7 text only (tier b); G; P | records/spot/MBOX/mbox_20261118T013023Z_c_G02_n4/, records/spot/MBOX/mbox_20261118T045359Z_c_G02_n4/ | control jobs of the box runs 20261118T013023Z, 20261118T045359Z |
| code/pk23/o5/kit_v6/kt_lbu_g37lzd_v1.py | a87bf335 | 5 | no (the record tables and the Lean list fragments) | PASS (1 output) | a pre-release of release_M | T-v7 text only (tier b); G; P | records/spot/MBOX/mbox_20261118T045359Z_c_G02_n4_lzd/ | control jobs of the box runs 20261118T045359Z |
| code/pk23/o5/kit_v7/kt_lbu_g37fs_v1.py | 013b521b | 20 | no (the record tables and the Lean list fragments) | PASS (3 outputs) | a pre-release of release_M | T-v7 text only (tier b); G; P | records/spot/MBOX/mbox_20261118T114847Z_c3_G02_N3K4_s1413_65536/, records/spot/MBOX/mbox_20261118T114847Z_c3_G02_N4K5_16384/, records/spot/MBOX/mbox_20261118T114847Z_c_G02_n4_fs64/ | control jobs of the box runs 20261118T114847Z |
| code/pk23/o5/kit_v7b_1/kt_lbu_g37fs_v1_1.py, code/pk23/o5/kit_v7b_2/kt_lbu_g37fs_v1_1.py | 07ef4b51 | 16 | no (the record tables and the Lean list fragments) | PASS (6 outputs) | a pre-release of release_M | T-v7 text only (tier b); G; P | records/spot/MBOX/mbox_20261118T154150Z_c3_G02_N3K4_s1413_65536/, records/spot/MBOX/mbox_20261118T154150Z_c3_G02_N4K5_16384/, records/spot/MBOX/mbox_20261118T154150Z_c_G02_n4_fs64/, records/spot/MBOX/mbox_20261119T041647Z_c3_G02_N3K4_s1413_65536/, records/spot/MBOX/mbox_20261119T041647Z_c3_G02_N4K5_16384/, records/spot/MBOX/mbox_20261119T041647Z_c_G02_n4_fs64/ | control jobs of the box runs 20261118T154150Z, 20261119T041647Z |
| code/pk23/o5/kit_v7/kt_lbu_g37fs_v1.py | 013b521b | 6 | no (the control comparisons of the box runs) | — | — | T-v7 text only (tier b); G; P | — | references for the control jobs, made with this engine |
| code/pk23/o5/kt_lbu_g36_pk23_v1.py | 58275c14 | 8 | no (the control comparisons of the box runs) | — | — | T-v7 text only (tier b); G; P | — | references for the control jobs, made with this engine |
| code/pk23/o5/kit_v6/kt_lbu_g37_v1.py | 8677a368 | 3 | no (the control comparisons of the box runs) | — | — | T-v7 text only (tier b); G; P | — | references for the control jobs, made with this engine |
| code/pk06/kt_lbu_g34_pk06_v1.py (a file of release_L) | 8b7aff00 | 5 | no (the control comparisons of the box runs) | — | — | a file of release_L | — | references for the control jobs, made with this engine |
| code/pk15/kt_p2_assembly_v1_37_1.py | f40a0d1e | 6 | yes (the checks of record A; the certificate of Proposition B.13, through the t export) | — | — | T-v7 text only (tier b); G; P | — | not rerun; its outputs ship as carried items, and it cannot be rerun from the archive (section 4) |
| code/pk07/kt_s9h_v1_3_2.py | 23a06d7d | 2 | yes (the check a4 of record A, through the C2-a export) | — | — | T-v7 text only (tier b, source-form rules); G; P | — | rerun for this version after a change by G in two lines: VERDICT VALID, both outputs pass (section 2.1); its outputs ship as carried items, and it reads its own source (section 4) |
| code/pk22/m3/m3_run_v1_9_3_px22_c3_1.py | 1c589cd5 | 25 | yes (the certificate of Proposition B.13: six c3 records and two assembly outputs) | — | — | T-v7 text only (tier b); G; P | — | not rerun: two of the seven inputs that it pins were changed by T, while the H-prep tables that it reads are in the data record and are rebuilt in section 2.1; the c3 records are carried items of code/acc/ITEM_MANIFEST_M_v1.tsv (section 4) |
| code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py | cc6f0a5f | 6 | no | — | — | T-v7 text only (tier b, source-form rules); G; P | — | rerun for this version: VERDICT VALID, all four outputs pass (section 2.1); it reads its own source (section 4) |
| code/pk22/m3/m3ref_px22_v1_5.py | 0c1c808c | 8 | no (the certificate in development mode only) | — | — | T-v7 text only (tier b); P | — | not rerun: a float reference, which reads its own source (section 4) |
| code/pk02/kt_cert_v1_7.py | efe4c40d | 4 | yes (the cert run of R4, not rerun) | — | — | T-v7 text only (tier b); P | — | not rerun; an input of R4; it cannot be rerun from the archive (section 4) |
| code/pk11/kt_s8f1_v1_3.py | 30c419d0 | 4 | yes (the certificate of Proposition B.13) | — | — | T-v7 text only (tier b); P | — | rerun for this version with the 2 reference outputs that it pins added: VERDICT VALID for each item, all four outputs pass (section 2.1); it ships with the programs that read its outputs |
| code/pk11/kt_s8h_mk_v1.py | 426ac22f | 10 | yes (the certificate of Proposition B.13) | — | — | T-v7 text only (tier b); P | — | not rerun; it ships with the programs that read its outputs; one of the files that it pins is not in the archive, and it cannot be rerun from the archive (section 4) |
| code/pk24/n5/n5map_v1.py | 05473cd1 | 1 | yes (the certificate of Proposition B.13) | — | — | T-v7 text only (tier b); G | — | not rerun; it ships with the programs that read its outputs; it reads 5 inputs by path, and none of them is in the archive; it cannot be rerun from the archive (section 4) |
| code/pk08/px08_hsd3_export_v1.py | 101646c7 | 1 | yes (the cert run of R4, not rerun) | — | — | T-v7 text only (tier b, source-form rules); G; P | — | not rerun; it ships with the programs that read its outputs; 7 of the files that it pins are not in the archive, and it cannot be rerun from the archive (section 4) |
| code/pk08/px08_hsd3b_export_v1_1.py | 737a9955 | 1 | yes (the cert run of R4, not rerun) | — | — | T-v7 text only (tier b); G; P | — | rerun for this version: VERDICT VALID, both outputs pass (section 2.1); it ships with the programs that read its outputs, and every file that it pins is in the archive |
| code/pk08/px08_hsd4_export_v1.py | efa92858 | 1 | yes (the cert run of R4, not rerun) | — | — | T-v7 text only (tier b); G; P | — | not rerun; it ships with the programs that read its outputs; 4 of the files that it pins are not in the archive, and it cannot be rerun from the archive (section 4) |
| code/pk03/m3_run_v1_8_3.py | 9660d018 | 2 | yes (the cert run of R4, not rerun) | — | — | T-v7 text only (tier b); G; P | — | not rerun; it ships with the programs that read its outputs; 2 of the files that it pins are not in the archive, and it cannot be rerun from the archive (section 4) |
| code/pk03/m3_run_v1_10_4.py | c73dda0b | 2 | yes (the cert run of R4, not rerun) | — | — | T-v7 text only (tier b); G; P | — | not rerun; it ships with the programs that read its outputs; 14 of the files that it pins are not in the archive, and it cannot be rerun from the archive (section 4) |
| code/pk15/m4_asm_v1.py | e085f35d | 2 | yes (the cert run of R4, not rerun) | — | — | T-v7 text only (tier b); G; P | — | not rerun; it ships with the programs that read its outputs; 62 of the files that it pins are not in the archive, and it cannot be rerun from the archive (section 4) |
| code/pk11/kt_s8rf_v1.py | 0912675c | 4 | yes (the cert run of R4, not rerun) | — | — | T-v7 text only (tier b); G; P | — | rerun for this version after P re-pinned it to the T image of one table that it pins: VERDICT VALID for each item, all four outputs pass (section 2.1); it ships with the programs that read its outputs |
| kt_s8hj_v1 (not in the archive) | d5daa226 | 2 | no | — | — | — | — | the producer is not in the archive; its outputs ship as carried items, pinned by their checksums where they are read |
| kt_trick_v1 (not in the archive) | 63476f37 | 4 | no | — | — | — | — | the producer is not in the archive; its outputs ship as carried items, pinned by their checksums where they are read |
| mock runs (code/pk15/mocks) | — | 20 | no (mock modes of R4, R5, the copy of the S8 module and code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py) | — | — | — | — | mock outputs, not certified; most of their producers are not in the archive |
| plant: code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_cover_cv/code8/certint6.py (bundle pkg_cover_cv) | — | — | — | FIRES | release_E | comments only | records/spot/M3D/plant_cv_out_exists/stdout.txt | PLANT-OUT-EXISTS FIRES (rc 1, AssertionError at line 52) |
| plant: code/pk09/BUNDLE_UNIFORM_0_20_v1/pkg/pkg_cover_cv/code8/certint6.py (bundle pkg_cover_cv) | — | — | — | FIRES | release_E | comments only | records/spot/M3D/plant_cv_copy_outside/stdout.txt | PLANT-COPY-OUTSIDE FIRES (rc 1, AssertionError at line 52) |

## Appendix C. The programs added in release_M, in release_N and in this version

**Table C.1.** The programs added in release_M, with the class of their difference; the checksums of the version that ran (original) and of the released file are in CORRESPONDENCE_release_N.tsv. The classes extend those of section 6.3: D, docstrings only, the same program by its syntax tree; T-v7 text only (shell), a shell script in which T-v7 rewrote the comments and strings; T-v7 text only (tier b), as in section 6.3 with T-v7 in place of T-v6; T-v7 text only (tier b, source-form rules), as tier b, except that some rules of T-v7 match a string literal as written in the source (for instance with an escaped quote), so that the comparison of constants cannot map these strings, and the class rests on check A, which shows that applying T-v7 to the original gives exactly the file before G and P; G lines, the program carries changes of G at the lines listed; P, re-pinned checksums differ too. The notes name the places where a program uses its own file or reads its own source.

| program | class | notes |
|---|---|---|
| code/pk21/p2/a/a3_bulk_checks_v1.py | T-v7 text only (tier b); P | uses __file__ (l.59) |
| code/pk21/p2/a/a4_units_crosscheck_v1.py | T-v7 text only (tier b); P | uses __file__ (l.23) |
| code/pk21/p2/a/a4_units_crosscheck_v1_1.py | T-v7 text only (tier b); P | uses __file__ (l.24) |
| code/pk21/p2/job27_n1.sh | T-v7 text only (shell) |  |
| code/pk21/p2/job28_a3.sh | T-v7 text only (shell) |  |
| code/pk21/p2/job51_a4.sh | T-v7 text only (shell) |  |
| code/pk21/p2/job52_a4b.sh | T-v7 text only (shell) |  |
| code/pk22/jobs/chain_rcc_v6.sh | T-v7 text only (shell) |  |
| code/pk22/w1/make_rcc_v1_3.py | T-v7 text only (tier b); P |  |
| code/pk22/w1/make_rcc_v1_4.py | T-v7 text only (tier b); P |  |
| code/pk22/w1/make_rcc_v1_5.py | T-v7 text only (tier b); G lines 4; P |  |
| code/pk22/w1/rc_cert/kt_s8h_rcc_v1_2.py | T-v7 text only (tier b); G lines 98,99,149,150,151,152,153,158,173,196,2729,2731; P | uses __file__ (l.2582); uses __file__ (l.2690); uses __file__ (l.178) |
| code/pk22/w1/rc_cert/kt_s8h_rcc_v1_3.py | T-v7 text only (tier b); G lines 99,100,150,151,152,153,154,159,174,197,2730,2732; P | uses __file__ (l.2583); uses __file__ (l.2691); uses __file__ (l.179) |
| code/pk22/w1/rc_cert/kt_s8h_rcc_v1_4.py | T-v7 text only (tier b); G lines 101,102,152,153,154,155,156,161,176,199,2747; P | uses __file__ (l.2585); uses __file__ (l.2697); uses __file__ (l.181) |
| code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py | T-v7 text only (tier b); G lines 104,105,155,156,157,158,159,164,179,201,202,1371,1382,2794; P | uses __file__ (l.2632); uses __file__ (l.2744); uses __file__ (l.184) |
| code/pk24/ne/kt_s8hf_rcm6.py | T-v7 text only (tier b); G lines 139,140,142,177,178; P | uses __file__ (l.188) |
| code/pk22/w1/ne_cert/kt_s8_cert_v1_14_3_ne.py | T-v7 text only (tier b); G lines 66,97,164,165,216,217,255,300,363,378,630,631,637,645,652,653,656,657,658,659,696,697,698,699,700,701,702,703,704,772,827,1055,1423,1424,1791,1894,1895,1896,2732,3489,3491; P | uses __file__ (l.3360); uses __file__ (l.639); uses __file__ (l.861); uses __file__ (l.3476) |
| code/pk23/tools/make_o5_record_table_v3.py | T-v7 text only (tier b); G lines 18,19,20,21 |  |
| code/pk23/o5/kt_lbu_g37_v1.py | T-v7 text only (tier b); G lines 111; P | uses __file__ (l.162); uses __file__ (l.163) |
| code/pk23/o5/make_g37_v1.py | T-v7 text only (tier b); P |  |
| code/pk23/o5/kit_v5/kt_lbu_g37_v1.py | T-v7 text only (tier b); G lines 111; P | uses __file__ (l.162); uses __file__ (l.163) |
| code/pk23/o5/kit_v5/o5_control_cmp_v1.sh | T-v7 text only (shell) |  |
| code/pk23/o5/kit_v6/kt_lbu_g37_v1.py | T-v7 text only (tier b); G lines 111; P | uses __file__ (l.162); uses __file__ (l.163) |
| code/pk23/o5/kit_v6/kt_lbu_g37lzd_v1.py | T-v7 text only (tier b); G lines 118; P | uses __file__ (l.169); uses __file__ (l.170) |
| code/pk23/o5/kit_v6/o5_control_cmp_v1.sh | T-v7 text only (shell) |  |
| code/pk23/o5/kit_v7/kt_lbu_g37fs_v1.py | T-v7 text only (tier b); G lines 124; P | uses __file__ (l.176); uses __file__ (l.177) |
| code/pk23/o5/kit_v7/o5_control_cmp_v2.sh | T-v7 text only (shell) |  |
| code/pk23/o5/kit_v7b_1/kt_lbu_g37fs_v1_1.py | T-v7 text only (tier b); G lines 19,124; P | uses __file__ (l.176); uses __file__ (l.177) |
| code/pk23/o5/kit_v7b_1/o5_control_cmp_v2.sh | T-v7 text only (shell) |  |
| code/pk23/o5/kit_v7b_2/kt_lbu_g37fs_v1_1.py | T-v7 text only (tier b); G lines 19,124; P | uses __file__ (l.176); uses __file__ (l.177) |
| code/pk23/o5/kit_v7b_2/o5_control_cmp_v2.sh | T-v7 text only (shell) |  |
| code/pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py | T-v7 text only (tier b, source-form rules); G lines 270,271,272,273,417,427,1969,1971,1975,1978,2123,2125,2129,2292,2296,2355,2411,2417,2421,2436,2439,2729,2733,2735,2745,2748,2752,2785,3012,3082,3089,3090,3136,3137,3245,3332,3467,3531,3533,3535,3802,3804,3806,4030,4032,4036,4570,4641,4643,4645,4844,5663,5688,5888,5911; P | reads its source with inspect.getsource (l.4340); reads its source with inspect.getsource (l.4727); reads its source with inspect.getsource (l.5094); uses __file__ (l.251); reads its source with inspect.getsource (l.3337); reads its source with inspect.getsource (l.3443); uses __file__ (l.251); uses __file__ (l.253); |
| code/pk21/p2/job22_tau4.sh | T-v7 text only (shell) |  |
| code/pk21/p2/job26_s4c_cmp.sh | T-v7 text only (shell) |  |
| code/pk22/m3/m3_run_v1_9_3_px22_c1.py | T-v7 text only (tier b); G lines 177,178,179,180,181,182,199,200; P | uses __file__ (l.299); uses __file__ (l.427) |
| code/pk22/m3/m3_handoff_v3_px22.py | T-v7 text only (tier b); P |  |
| code/pk22/m3/make_c3_v1.py | T-v7 text only (tier b); G lines 12,13,16; P |  |
| code/pk22/m3/m3_run_v1_9_3_px22_c3.py | T-v7 text only (tier b); G lines 202,203,204,205,206,207,224,225; P | uses __file__ (l.343); uses __file__ (l.471) |
| code/pk22/m3/make_c3_1_v1.py | T-v7 text only (tier b); P |  |
| code/pk22/m3/m3_run_v1_9_3_px22_c3_1.py | T-v7 text only (tier b); G lines 205,206,207,208,209,210,227,228; P | uses __file__ (l.346); uses __file__ (l.474) |
| code/pk22/tools/make_c3_list_v2.py | T-v7 text only (tier b); G lines 21,22,23,24; P | uses __file__ (l.29) |
| code/pk22/tools/check_c3_list_v1.py | T-v7 text only (tier b); G lines 7,8,9 |  |
| code/pk22/m3/make_m3ref_px22_v1.py | T-v7 text only (tier b); G lines 10,11,12; P |  |
| code/pk22/m3/make_m3ref_px22_v1_1.py | T-v7 text only (tier b); G lines 10,11,12; P |  |
| code/pk22/m3/make_m3ref_px22_v1_2.py | T-v7 text only (tier b); P |  |
| code/pk22/m3/make_m3ref_px22_v1_3.py | T-v7 text only (tier b) |  |
| code/pk22/m3/make_m3ref_px22_v1_4.py | T-v7 text only (tier b); P |  |
| code/pk22/m3/make_m3ref_px22_v1_5.py | T-v7 text only (tier b) |  |
| code/pk22/m3/m3ref_px22_v1_5.py | T-v7 text only (tier b); P | reads its source with inspect.getsource (l.433); uses __file__ (l.396) |
| code/pk22/jobs/chain_float_c3_v2.sh | T-v7 text only (shell) |  |
| code/pk22/jobs/chain_c3_v1.sh | T-v7 text only (shell) |  |
| code/pk22/jobs/chain_c3_v2.sh | T-v7 text only (shell) |  |
| code/pk23/o5/kt_lbu_g36_pk23_v1.py | T-v7 text only (tier b); G lines 110; P | uses __file__ (l.161); uses __file__ (l.162) |
| code/pk23/o5/make_g36_v1.py | T-v7 text only (tier b); P |  |
| code/pk23/jobs/run_o5_v1.sh | T-v7 text only (shell) |  |
| code/pk21/p2/kt_lbu_g35_pk21_v1.py | T-v7 text only (tier b); G lines 106; P | uses __file__ (l.157); uses __file__ (l.158) |
| code/pk23/tools/map_pk24_labels_v1.py | T-v7 text only (tier b) |  |
| code/rv83/tools/record2lean_v1.py | D: docstrings only |  |
| code/rv83/tools/record2lean_v1_1.py | D: docstrings only |  |
| code/rv83/tools/orbits2lean_v1.py | D: docstrings only |  |
| code/rv83/tools/nerec2lean_v1_1.py | D: docstrings only |  |
| code/pk15/kt_p2_assembly_v1_37_1.py | T-v7 text only (tier b); G lines 143,144,173,196,210,428,443,677,678,686,704,707,727,729,733,735,736,737,739,740,742,743,744,751,752,753,767,768,775,778,786,787,788,789,790,794,795,796,811,2316,3593,3679; P | uses __file__ (l.4209); uses __file__ (l.682); uses __file__ (l.951) |
| code/pk07/kt_s9h_v1_3_2.py | T-v7 text only (tier b, source-form rules); G lines 309,310,311,312,417,426,459,469,2193,2195,2199,2202,2347,2349,2353,2516,2520,2579,2635,2641,2645,2660,2663,2957,2961,2963,2973,2976,2980,3013,3262,3332,3339,3340,3386,3387,3496,3583,3718,3782,3784,3786,4059,4061,4063,4310,4312,4316,4857,4974,4976,4978,5223,6055,6080,6280,6303; P | reads its source with inspect.getsource (l.4620); reads its source with inspect.getsource (l.5106); reads its source with inspect.getsource (l.5473); uses __file__ (l.290); reads its source with inspect.getsource (l.3588); reads its source with inspect.getsource (l.3694); uses __file__ (l.290); uses __file__ (l.292); |
| code/pk07/kt_s9h_m21.py | T-v7 text only (tier b, source-form rules); G lines 246,247,248,249,379,387,1925,1927,1931,1934,2079,2081,2085,2248,2252,2311,2367,2373,2377,2392,2395,2642,2646,2648,2658,2661,2665,2681,2892,2962,2969,2970,3016,3017,3125,3212,3347,3410,3412,3414,3674,3676,3678,4178,4248,4250,4252,4451,5227,5252,5413,5436; P | reads its source with inspect.getsource (l.3948); reads its source with inspect.getsource (l.4334); reads its source with inspect.getsource (l.4700); uses __file__ (l.227); reads its source with inspect.getsource (l.3217); reads its source with inspect.getsource (l.3323); uses __file__ (l.227); uses __file__ (l.229); |
| code/pk07/kt_s9h_v1_3_readers.py | T-v7 text only (tier b); G lines 29,160; P |  |
| code/pk15/m4_reader_v1.py | T-v7 text only (tier b); G lines 50,409 | uses __file__ (l.495) |
| code/pk02/kt_cert_v1_7.py | T-v7 text only (tier b); P | uses __file__ (l.242) |
| code/pk11/kt_s8f1_v1_3.py | T-v7 text only (tier b); P | uses __file__ (l.60); uses __file__ (l.115) |
| code/pk11/kt_s8h_mk_v1.py | T-v7 text only (tier b); P | uses __file__ (l.52); uses __file__ (l.126); uses __file__ (l.328) |
| code/pk24/n5/n5map_v1.py | T-v7 text only (tier b); G lines 10,11,12,15 |  |
| code/pk08/px08_hsd3_export_v1.py | T-v7 text only (tier b, source-form rules); G lines 3,26,27,57,58,59,70,103,270,280,281; P | uses __file__ (l.29); uses __file__ (l.190) |
| code/pk08/px08_hsd3b_export_v1_1.py | T-v7 text only (tier b); G lines 11,22,23,86; P | uses __file__ (l.25); uses __file__ (l.221) |
| code/pk08/px08_hsd4_export_v1.py | T-v7 text only (tier b); G lines 35,36,69,72,113; P | uses __file__ (l.38); uses __file__ (l.227) |
| code/pk03/m3_run_v1_8_3.py | T-v7 text only (tier b); G lines 86,87,88,89,90,106; P | uses __file__ (l.229); uses __file__ (l.309) |
| code/pk03/m3_run_v1_10_4.py | T-v7 text only (tier b); G lines 3,4,5,7,47,48,49,50,51,66,67,441,443,444,652,660,873,891,931,933,985,1050,1077,1262,1475,1485; P | uses __file__ (l.190); uses __file__ (l.327) |
| code/pk15/m4_asm_v1.py | T-v7 text only (tier b); G lines 8,32,34,46,47,156,175,207,221,242,247,395,444,460,512,611,626,703,736,744,746,903; P | uses __file__ (l.903); uses __file__ (l.901) |
| code/pk11/kt_s8rf_v1.py | T-v7 text only (tier b); G lines 2,4,20,80,81,82,85,115,116,117,118,510,543,706; P | uses __file__ (l.86); uses __file__ (l.151) |

**Table C.2.** The programs added in release_N, with the class of their difference; the checksums of the version that ran (original) and of the released file are in CORRESPONDENCE_release_N.tsv. The classes are those of Table C.1 and section 6.3, with T-v8 in place of T-v7. One more class, T-v8 text only (template), covers a template that does not parse as a program: its T-v8 image equals the original byte for byte, and P left it unchanged. The notes name the places where a program uses its own file or reads its own source.

| program | class | notes |
|---|---|---|
| code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py | T-v8 text only (tier b); P | reads its source with inspect.getsource (l.200); reads its source with inspect.getsource (l.200); uses __file__ (l.1140); uses __file__ (l.976); uses __file__ (l.1158) |
| code/pk24/tools/stage_certset_v1.py | T-v8 text only (tier b) |  |
| code/pk24/tools/check_v4b_cols_v1.py | T-v8 text only (tier a); P |  |
| code/pk24/jobs/job_cert_m1_TEMPLATE_v2.sh | T-v8 text only (shell) |  |
| code/pk24/jobs/job232_cert_m1_v4b.sh | T-v8 text only (shell) |  |
| code/pk24/tools/check_m2_cols_v2.py | T-v8 text only (tier a); P |  |
| code/pk24/jobs/job_cert_m2_TEMPLATE_v3.sh | T-v8 text only (shell) |  |
| code/pk24/jobs/job260_cert_m2_v1.sh | T-v8 text only (shell) |  |
| code/pk24/tools/make_mrengine_v1_8_4.py | T-v8 text only (tier b) |  |
| code/pk24/mr_engine/mr_merge_v1_8_4.py | T-v8 text only (tier b); P | uses __file__ (l.231); uses __file__ (l.85); uses __file__ (l.248) |
| code/pk24/mr_engine/mr_core_v1_3.py | T-v8 text only (tier a) |  |
| code/pk24/midrow/g6_engine_proto_v1_2.py | T-v8 text only (tier b); P |  |
| code/pk24/jobs/job194_v1_8_4.sh | T-v8 text only (shell) |  |
| code/pk24/tools/check_m2_cols_v1.py | T-v8 text only (tier a); P |  |
| code/pk24/jobs/job_cert_m2_TEMPLATE_v2.sh | T-v8 text only (shell) |  |
| code/pk24/jobs/job_cert_m2_TEMPLATE_v1.sh | T-v8 text only (shell) |  |
| code/pk24/tools/make_vx_refresh_standin_v1.py | T-v8 text only (tier b) |  |
| code/pk24/jobs/job240_m2cols_v2_test.sh | T-v8 text only (shell) |  |
| code/pk25/asm/kt_s9h_asm_v1_8.py | T-v8 text only (tier b); P | uses __file__ (l.106) |
| code/pk25/asm/kt_s9h_ins_v2_2.py | T-v8 text only (tier b); G lines 2332,2363; P | uses __file__ (l.79) |
| code/pk25/jobs/job137_splice_asm_v1_8.py | T-v8 text only (tier b) |  |
| code/pk25/asm/make_kt_s9h_asm_v1_8.py | T-v8 text only (tier b); P | uses __file__ (l.147); uses __file__ (l.147) |
| code/pk25/jobs/job139_splice_ins_v2_2.py | T-v8 text only (tier b) |  |
| code/pk25/asm/make_kt_s9h_ins_v2_2.py | T-v8 text only (tier b); P | uses __file__ (l.166); uses __file__ (l.166) |
| code/pk25/asm/kt_s9h_crudex_v1.py | T-v8 text only (tier b); P | uses __file__ (l.29) |
| code/pk25/jobs/job145_crudex_cert_post.sh | T-v8 text only (shell) |  |
| code/pk25/asm/kt_s9h_ins_v2_4.py | T-v8 text only (tier b); G lines 2427,2458; P | uses __file__ (l.83) |
| code/pk25/asm/make_kt_s9h_ins_v2_4.py | T-v8 text only (tier b) | uses __file__ (l.82); uses __file__ (l.82) |
| code/pk25/jobs/job153_cmp_ins_v2_4.sh | T-v8 text only (shell) |  |
| code/pk25/jobs/job154_ins_v2_4_cert_post.sh | T-v8 text only (shell) |  |
| code/pk25/asm/kt_s9h_ins_v2_7.py | T-v8 text only (tier b); G lines 15,27,2453,2484; P | uses __file__ (l.102) |
| code/pk25/asm/make_kt_s9h_ins_v2_7.py | T-v8 text only (tier b) | uses __file__ (l.106); uses __file__ (l.106) |
| code/pk25/jobs/job164_cmp_ins_v2_5.sh | T-v8 text only (shell) |  |
| code/pk25/jobs/job173_ins_v2_7_cert.sh | T-v8 text only (shell) |  |
| code/pk25/p2/kt_p2_v2_3.py | T-v8 text only (tier b); G lines 5,7,11,15; P | uses __file__ (l.76) |
| code/pk25/p2/make_kt_p2_v2_3.py | T-v8 text only (tier b) | uses __file__ (l.88); uses __file__ (l.88) |
| code/pk25/nu/nu_reader_v1_1.py | T-v8 text only (tier b); G lines 3 |  |
| code/pk25/jobs/job172_p2_v2_3_n1.sh | T-v8 text only (shell) |  |
| code/pk25/asm/kt_s9h_p3_v7_1.py | T-v8 text only (tier b); G lines 3,23,52; P | uses __file__ (l.92) |
| code/pk25/asm/make_kt_s9h_p3_v7.py | T-v8 text only (tier b) | uses __file__ (l.156); uses __file__ (l.156) |
| code/pk25/jobs/job187_p3_v7_dry_c0.sh | T-v8 text only (shell) |  |
| code/pk25/jobs/job189_p3_v7_cert.sh | T-v8 text only (shell); G lines 3 |  |
| code/pk25/jobs/job190_p3_v7_freeze.sh | T-v8 text only (shell) |  |
| code/pk25/asm/kt_s9h_asm_v1_7.py | T-v8 text only (tier b); P | uses __file__ (l.104) |
| code/pk25/jobs/job108b_splice_asm_v1_4b.py | T-v8 text only (tier b) |  |
| code/pk25/asm/make_kt_s9h_asm_v1_3.py | T-v8 text only (tier b); P | uses __file__ (l.146); uses __file__ (l.146) |
| code/pk25/jobs/job110b_v3_vs_v2.py | T-v8 text only (tier b) |  |
| code/pk25/jobs/job107_precheck_uhat_v2.py | T-v8 text only (tier b) |  |
| code/pk22/midrow/g4/mrc/src/make_mrx_v1_9.py | T-v8 text only (tier b); G lines 6; P | uses __file__ (l.36) |
| code/pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py | T-v8 text only (tier b); P | uses __file__ (l.1118) |
| code/pk22/midrow/g4/mrc/src/mrx_combine_v1_9.py | T-v8 text only (tier b); P | uses __file__ (l.77) |
| code/pk22/jobs/job233_mrx_v1_9.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job234_mrx_v1_9_freeze.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job297_mrx_v1_10_cert.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job298_mrx_v1_10_freeze.sh | T-v8 text only (shell) |  |
| code/pk22/midrow/g4/mrc/src/make_mrx_v1_10_r2.py | T-v8 text only (tier b); P |  |
| code/pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py | T-v8 text only (tier b); P | uses __file__ (l.1470) |
| code/pk22/midrow/g4/mrc/src/make_mrx_combine_v1_10.py | T-v8 text only (tier b) |  |
| code/pk22/midrow/g4/mrc/src/mrx_combine_v1_10.py | T-v8 text only (tier b); P | uses __file__ (l.92) |
| code/pk22/jobs/job292_make_mrx_v1_10_r2.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job294_dry_mrx_v1_10.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job295_make_combine_v1_10.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job296_freeze_mrx_code_v1_10.sh | T-v8 text only (shell) |  |
| code/pk22/midrow/g4/mrc/src/mrj_cert_v1.tmpl.py | T-v8 text only (tier b) | uses __file__ (l.469) |
| code/pk22/midrow/g4/mrc/src/make_mrj_v1.py | T-v8 text only (tier b); G lines 3,11; P | uses __file__ (l.39) |
| code/pk22/midrow/g4/mrc/src/mrj_cert_v1.py | T-v8 text only (tier b); P | uses __file__ (l.469) |
| code/pk22/jobs/job236_mrj_v1.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job237_mrj_v1_freeze.sh | T-v8 text only (shell) |  |
| code/pk22/midrow/e3/src/e3_sq2_v2.tmpl.py | T-v8 text only (template, not Python: byte rule) | template with placeholders: does not parse (invalid syntax, line 43) |
| code/pk22/midrow/e3/src/make_e3_sq2_v2.py | T-v8 text only (tier b); P | uses __file__ (l.34) |
| code/pk22/midrow/e3/src/e3_sq2_v2.py | T-v8 text only (tier b); P | uses __file__ (l.282); uses __file__ (l.283) |
| code/pk22/jobs/job304_e3_sq2_v2_cert.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job305_e3_sq2_v2_freeze.sh | T-v8 text only (shell) |  |
| code/pk24/nu/kt_nu_g_v1_2.py | T-v8 text only (tier b); G lines 556; P | uses __file__ (l.56); uses __file__ (l.282) |
| code/pk24/tools/make_kt_nu_g_v1_2.py | T-v8 text only (tier b); P |  |
| code/pk24/nu/src/nu_head_v1_2.py | T-v8 text only (tier b); P | uses __file__ (l.56) |
| code/pk24/nu/src/nu_main_v1_2.py | T-v8 text only (tier b); G lines 300 | uses __file__ (l.26) |
| code/pk24/nu/arbeng_c2b_v2.py | T-v8 text only (tier a) |  |
| code/pk02/kt_cert_v1_9.py | T-v8 text only (tier b); G lines 33,34,70,95,118,129,925,927,1819,1868,1870,1873,2951; P | uses __file__ (l.427) |
| code/pk24/jobs/job244_nu_record_v1_2.sh | T-v8 text only (shell) |  |
| code/pk25/p2/kt_p2_v2_1.py | T-v8 text only (tier b); G lines 5; P | uses __file__ (l.55) |
| code/pk24/tools/assemble_nunote_v1.py | T-v8 text only (tier b) |  |
| code/pk24/jobs/job239_nunote_v1.sh | T-v8 text only (shell) |  |
| code/pk23/cw/cw_comb_v2_2.py | T-v8 text only (tier b); G lines 16; P | uses __file__ (l.491); doc-read: __doc__ (line 75) |
| code/pk23/cw/cw_comb_v2_0.py | T-v8 text only (tier b); P | uses __file__ (l.432); doc-read: __doc__ (line 55) |
| code/pk23/cw/make_cw_comb_v2_x4.py | T-v8 text only (tier b); G lines 3,78; P | doc-read: __doc__ (line 30) |
| code/pk23/cw/make_cw_comb_v2_x3.py | T-v8 text only (tier b); P | doc-read: __doc__ (line 29) |
| code/pk23/cw/cmp_cw_x11_v1.awk | T-v8 text only (shell) |  |
| code/pk23/tools/test_tball_v2_2_v1.py | T-v8 text only (tier a) | doc-read: __doc__ (line 16) |
| code/pk23/tools/test_arb_div0_v1.py | T-v8 text only (tier a) |  |
| code/pk23/tools/astcheck_v1.py | T-v8 text only (tier a) |  |
| code/pk23/pev/m3_reader_cw_v1_1.py | T-v8 text only (tier a); G lines 39,49,63,164,169,170; P |  |
| code/pk23/pev/make_m3_reader_cw_v1_1.py | T-v8 text only (tier b); P |  |
| code/pk23/pev/m3_reader_cw11_check_v1.py | T-v8 text only (tier b) |  |
| code/pk23/cw/make_cw_comb_manifest_v2_2.sh | T-v8 text only (shell) |  |
| code/pk23/cw/freeze_cw_comb_v2_2.sh | T-v8 text only (shell) |  |
| code/pk23/pev/m3_run_v1_9_3_hl_v1.py | T-v8 text only (tier b); G lines 101,168; P | uses __file__ (l.406); uses __file__ (l.534) |
| code/pk23/pev/m3_handoff_v3_hl.py | T-v8 text only (tier b); P |  |
| code/pk23/pev/m3ref_hl_v1.py | T-v8 text only (tier b); G lines 96; P | reads its source with inspect.getsource (l.458); uses __file__ (l.421) |
| code/pk23/pev/rtwin_hl_v1.py | T-v8 text only (tier b); P | uses __file__ (l.58); uses __file__ (l.223); uses __file__ (l.131) |
| code/pk23/pev/make_m3ref_hl_v1.py | T-v8 text only (tier b) |  |
| code/pk23/pev/make_rtwin_hl_v1.py | T-v8 text only (tier b); P |  |
| code/pk23/pev/make_run_hl_v1.py | T-v8 text only (tier b); P |  |
| code/pk23/pev/make_pev_summary_v1.py | T-v8 text only (tier b) | uses __file__ (l.76) |
| code/pk23/pev/make_pev_manifest_v1_1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/check_t0_closed_v1.py | T-v8 text only (tier b) |  |
| code/pk23/pev/test_rtwin_maker_ast_v1.py | T-v8 text only (tier b) |  |
| code/pk23/pev/chain_twin_hl_v1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/chain_hl_v1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/chain_hl_v1_1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/run_rtwin_hl_v1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/freeze_pev_v1_1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/make_pev_manifest_v1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/freeze_pev_v1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/m3_lawcert_cw_v1.py | T-v8 text only (tier b); G lines 52,113,114,184; P | uses __file__ (l.346) |
| code/pk23/pev/m3_lawcert_hl_v1_1.py | T-v8 text only (tier b); G lines 39,100,101,171; P | uses __file__ (l.331) |
| code/pk22/m3/m3_lawcert_c3k_v2.py | T-v8 text only (tier b); G lines 39,100,101,171; P | uses __file__ (l.336) |
| code/pk22/m3/m3_reader_c3h_v1_1.py | T-v8 text only (tier a); G lines 3,13,27,128,133,134; P |  |
| code/pk25/mu/kt_mu_hw_v1_1.py | T-v8 text only (tier a) |  |
| code/pk25/m3/m3_reader_s9h_v1.py | T-v8 text only (tier a); G lines 4,105,110,111; P |  |
| code/rv83/tools/mrasm2lean_v1_1.py | T-v8 text only (tier a) |  |
| code/rv83/tools/mrasm2lean_m2_v1.py | T-v8 text only (tier a) |  |
| code/pk23/pev/make_cw_summary_v1.py | T-v8 text only (tier b) | uses __file__ (l.104) |
| code/pk23/pev/make_cw_list_v1.py | T-v8 text only (tier b) |  |
| code/pk23/pev/m3_run_v1_9_3_cw_v1.py | T-v8 text only (tier b); G lines 107,174; P | uses __file__ (l.417); uses __file__ (l.545) |
| code/pk23/pev/make_run_cw_v1.py | T-v8 text only (tier b); P |  |
| code/pk23/pev/rtwin_cw_v1.py | T-v8 text only (tier b); P | uses __file__ (l.58); uses __file__ (l.223); uses __file__ (l.131) |
| code/pk23/pev/make_rtwin_cw_v1.py | T-v8 text only (tier b); P |  |
| code/pk23/pev/run_rtwin_cw_v1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/chain_cw_v1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/make_m3_lawcert_cw_v1.py | T-v8 text only (tier b); P | uses __file__ (l.26) |
| code/pk23/pev/make_m3_lawcert_hl_v1_1.py | T-v8 text only (tier b); G lines 6; P | uses __file__ (l.23) |
| code/pk23/pev/m3_reader_hl_v1.py | T-v8 text only (tier a); G lines 22,32,46,147,152,153; P |  |
| code/pk23/pev/make_m3_reader_hl_v1.py | T-v8 text only (tier b); P |  |
| code/pk23/pev/m3_reader_hl_check_v1.py | T-v8 text only (tier b) |  |
| code/pk23/pev/m3_reader_cw_v1.py | T-v8 text only (tier a); G lines 32,42,56,157,162,163; P |  |
| code/pk23/pev/make_m3_reader_cw_v1.py | T-v8 text only (tier b); P |  |
| code/pk23/pev/m3_reader_cw_check_v1.py | T-v8 text only (tier b) |  |
| code/pk23/pev/m3_reader_cw_check_v1_1.py | T-v8 text only (tier b) |  |
| code/pk23/pev/make_cw_manifest_v1.sh | T-v8 text only (shell) |  |
| code/pk23/pev/freeze_cw_v1.sh | T-v8 text only (shell) |  |
| code/pk25/m4h/m4h_asm_v1_1.py | T-v8 text only (tier b); G lines 54,56,177,444,509,786,796; P | uses __file__ (l.948); uses __file__ (l.946) |
| code/pk25/m4h/m4h_reader_v1_1.py | T-v8 text only (tier b); P | uses __file__ (l.512) |
| code/pk25/m3/m3_run_s9h_v1_1.py | T-v8 text only (tier b); G lines 39,42,534,753,971,989,1029,1031,1083,1148,1381,1596,1606; P | uses __file__ (l.244); uses __file__ (l.384); uses __file__ (l.412) |
| code/pk22/midrow/g4/mrx/src/joint_float_v1.py | T-v8 text only (tier b) |  |
| code/pk22/jobs/job157_joint_float.sh | T-v8 text only (shell) |  |
| code/pk22/tools/astcheck_v1.py | T-v8 text only (tier a) |  |
| code/pk22/jobs/job310_joint_float_freeze.sh | T-v8 text only (shell) |  |
| code/pk25/m4h/make_m4h_v1_1.py | T-v8 text only (tier b) |  |
| code/pk25/jobs/job72_m4h_v1_1.sh | T-v8 text only (shell) |  |
| code/pk25/jobs/c5_run_v1.sh | T-v8 text only (shell) |  |
| code/pk25/jobs/job70_freeze_m4h.sh | T-v8 text only (shell) |  |
| code/pk22/jobs/job229_lawcert_c3h_v1_1.sh | T-v8 text only (shell) |  |
| code/pk22/m3/m3_lawcert_c3h_v1_1.py | T-v8 text only (tier b); G lines 3,64,65,135; P | uses __file__ (l.299) |
| code/pk22/m3/m3_lawcert_c3h_v1_pins.py | T-v8 text only (tier b) |  |
| code/pk22/m3/m3_run_v1_9_3_px22_c3h_1.py | T-v8 text only (tier b); G lines 68,135; P | uses __file__ (l.381); uses __file__ (l.509) |
| code/pk22/jobs/job262_lawcert_c3k_v2.sh | T-v8 text only (shell) |  |
| code/pk22/m3/m3_run_v1_9_3_px22_c3k_1.py | T-v8 text only (tier b); G lines 95,162; P | uses __file__ (l.430); uses __file__ (l.558) |
| code/pk22/m3/m3_run_v1_9_3_px22_c3k_2.py | T-v8 text only (tier b); G lines 102,169; P | uses __file__ (l.450); uses __file__ (l.578) |

**Table C.3.** The programs added in this version, with their class. All three are G-new, a program written for the archive, with no original version. The notes name the places where a program uses its own file.

| program | class | notes |
|---|---|---|
| rerun_m2.py (a2965fc9) | G-new | the driver of version 1 of the software record (33d54cd7) with one addition, the full-length check of PREFIX_PINS_release_N.tsv before any run and the option --pins; everything else is byte for byte that of 33d54cd7; it does not use its own file (the archive root is fixed, /mnt/g2/release/root, as in 33d54cd7) |
| cmp_certified.py (c4fe4fd3) | G-new | written for this version; reads CERT_PAIRS_release_N.tsv, P_MAP_release_N.tsv and CERT_MASKS_release_N.tsv; uses __file__ (l.310) to find the archive root |
| plants_midrow.py (33036095) | G-new | written for this version; repeats the commands of nM1 and nM2 with the PLANT argument of the assembly program on copies of their records, and changes no certified program; reads PLANTS_MIDROW_release_N.tsv; uses __file__ (l.31) to find the archive root |

## Appendix D. The carried programs and inputs of the middle row

**Table D.1.** The carried programs of the middle row: the programs that wrote the input records of the two middle-row runs and that ship with these records. For each program, the table counts its records that ship and names the first gate at which a rerun on the package stops. The last three rows are productions that build and read the moment tables. These tables sit in the tab16c folders, which do not ship.

| program | shipped records | a rerun on the package |
|---|---|---|
| code/pk22/m3/m3_lawcert_c3h_v1_1.py | 3 | a rerun on the package stops at the acceptance check of its input table: kernel arbeng_ma_v1_4_1.py (precision 512) is not a validated layer the reader pins |
| code/pk22/m3/m3_lawcert_c3k_v2.py | 4 | a rerun on the package stops at the acceptance check of its input table: kernel arbeng_ma_v1_4_1.py (precision 512) is not a validated layer the reader pins |
| code/pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py | 8 | a rerun on the package stops where its reader checks the input table m3_c3h_CE3H_N4_J300_c3h.json: kernel arbeng_ma_v1_4_1.py (precision 512) is not a validated layer the reader pins ; a rerun on the package stops at its input checksums: code/pk22/m3/out/m3_lawcert_c3h_v1_1_3.out does not ship |
| code/pk22/midrow/g4/mrc/src/mrx_combine_v1_9.py | 3 | a rerun on the package stops at its input checksums: code/pk24/MIDROW_G6_SPEC_v1_6_2.md does not ship |
| code/pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py | 8 | a rerun on the package stops where its reader checks the input table m3_c3h_CE3H_N4_J300_c3h.json: kernel arbeng_ma_v1_4_1.py (precision 512) is not a validated layer the reader pins ; a rerun on the package stops at its input checksums: code/pk22/m3/out/m3_lawcert_c3h_v1_1_3.out does not ship |
| code/pk22/midrow/g4/mrc/src/mrx_combine_v1_10.py | 3 | a rerun on the package stops at its input checksums: code/pk24/MIDROW_G6_SPEC_v1_6_2.md does not ship |
| code/pk22/midrow/g4/mrc/src/mrj_cert_v1.py | 3 | a rerun on the package stops at an input checksum: its input record gives the archived checksum of code/pk03/out/m3_s8v3_D_N4_J300_v1_8_1.json, which the package ships as an earlier release's rerun output |
| code/pk22/midrow/e3/src/e3_sq2_v2.py | 6 | a rerun on the package stops at its input checksums: code/pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256 does not ship |
| code/pk23/pev/m3_lawcert_hl_v1_1.py | 4 | a rerun on the package stops at the acceptance check of its input table: kernel arbeng_ma_v1_4_1.py (precision 512) is not a validated layer the reader pins |
| code/pk23/pev/m3_lawcert_cw_v1.py | 4 | a rerun on the package stops at the acceptance check of its input table: kernel arbeng_ma_v1_4_1.py (precision 512) is not a validated layer the reader pins |
| code/pk23/cw/cw_comb_v2_2.py | 3 | a rerun on the package passes its input checksums (C-PINS) and then stops at an input that does not ship and that the program does not pin: code/pk24/MIDROW_G6_SPEC_v1_7.md |
| code/pk25/asm/kt_s9h_asm_v1_7.py | 3 | a rerun on the package stops at C-HASH: 1 of its 52 pinned inputs, kt_mr_assembly_v1_6.py, does not ship |
| code/pk25/asm/kt_s9h_asm_v1_8.py | 2 | a rerun on the package passes C-HASH (54 pinned files) and stops at C-CORE: 13 of its 61 copied code segments differ from the reference file or are defined twice |
| code/pk25/asm/kt_s9h_ins_v2_4.py | 2 | a rerun on the package stops at C-HASH: 14 of its 88 pinned inputs do not ship (among them kt_s9h_asm_v1_5.py, kt_mu_hw_v1.py, RHO_RECORD_v1.kv, the m3_run_s9h_v1_1 asm outputs and the NHT and NIH tables) |
| code/pk25/asm/kt_s9h_crudex_v1.py | 2 | a rerun on the package writes the same record rows (the header lines CODE and SOURCE differ) |
| code/pk25/p2/kt_p2_v2_3.py | 2 | a rerun on the package stops at its input checksums: code/pk02/out_kt_cert_v1_6_x.e1n4.out does not ship |
| code/pk25/asm/kt_s9h_ins_v2_7.py | 2 | a rerun on the package stops at C-HASH: 14 of its 91 pinned inputs do not ship (among them kt_s9h_asm_v1_5.py, kt_mu_hw_v1.py, RHO_RECORD_v1.kv, the m3_run_s9h_v1_1 asm outputs and the NHT and NIH tables) |
| code/pk25/asm/kt_s9h_p3_v7_1.py | 2 | a rerun on the package stops at its input checksums: code/pk02/out_kt_cert_v1_6_x.hn3.out does not ship |
| code/pk24/nu/kt_nu_g_v1_2.py | 2 | not rerun; its C-HASH opens its ten pinned inputs, one of them a review document, which does not ship |
| code/pk22/m3/m3_run_v1_9_3_px22_c3h_1.py | — | not rerun: T changed 10 of the 18 inputs that it pins, and its prep pieces build and its entry pieces read the D16 moment tables of m3/out/tab16c, which do not ship |
| code/pk22/m3/m3_run_v1_9_3_px22_c3k_2.py | — | not rerun: T changed 28 of the 36 inputs that it pins and 5 could not be located, and its prep pieces build and its entry pieces read the D16 moment tables of m3/out/tab16c, which do not ship |
| code/pk23/pev/m3_run_v1_9_3_hl_v1.py | — | not rerun: T changed six of its pins, and re-pinning them would spread to the pins of other programs (the lawcert programs, MANIFEST_PEV and two rows of PREFIX_PINS_release_N.tsv); the PEV production builds and reads the D16 moment tables of pev/out/tab16c, which do not ship |

**Table D.2.** The carried inputs of the middle row, with their change (their archived and released checksums are in CORRESPONDENCE_release_N.tsv), the producer manifest if it ships (a dash if it does not), and the package files that pin these inputs. These inputs ship as carried, with the changes of their change column, and none was recomputed for this release.

| input | change | producer manifest | pinned by |
|---|---|---|---|
| code/pk24/mr_engine/src/kt_mr_assembly_v1_8_4.py.in | T | code/pk24/MANIFEST_KT_MR_ASSEMBLY_v1_8_4.sha256 | 3 files, among them code/pk24/KT_MR_ASSEMBLY_v1_8_4_NOTE.md |
| code/pk24/mr_engine/src/mr_merge_v1_8_4.py.in | T | code/pk24/MANIFEST_KT_MR_ASSEMBLY_v1_8_4.sha256 | 3 files, among them code/pk24/KT_MR_ASSEMBLY_v1_8_4_NOTE.md |
| code/pk25/asm/src/kt_s9h_asm_v1_8.py.in | T | code/pk25/MANIFEST_ASM_V1_8_DRY_v8d1.sha256 | code/pk25/MANIFEST_ASM_V1_8_DRY_v8d1.sha256 |
| code/pk25/asm/src/kt_s9h_asm_v1_4b.py.in | T | code/pk25/MANIFEST_ASM_V1_8_DRY_v8d1.sha256, code/pk25/asm/MANIFEST_C6A_ASM_v1_7.sha256 | 2 files, among them code/pk25/MANIFEST_ASM_V1_8_DRY_v8d1.sha256 |
| code/pk25/asm/src/kt_s9h_ins_v2_2s.py.in | T+G | code/pk25/MANIFEST_INS_V2_2_DRY_d2.sha256 | code/pk25/MANIFEST_INS_V2_2_DRY_d2.sha256 |
| code/pk25/asm/src/kt_s9h_ins_v2_4.py.in | T+G+P | code/pk25/mr/MANIFEST_MR_V4B_CERT_v1.sha256 | code/pk25/mr/MANIFEST_MR_V4B_CERT_v1.sha256 |
| code/pk25/asm/src/kt_s9h_ins_v2_7.py.in | T+G+P | code/pk25/mr/MANIFEST_MR_V5B_CERT_v1.sha256 | code/pk25/mr/MANIFEST_MR_V5B_CERT_v1.sha256 |
| code/pk25/p2/src/kt_p2_v2_3.py.in | T+G | code/pk25/p2/MANIFEST_P2_V2_3_CERT_c1.sha256 | code/pk25/p2/MANIFEST_P2_V2_3_CERT_c1.sha256 |
| code/pk25/asm/src/kt_s9h_p3_v7.py.in | T+G | code/pk25/mr/MANIFEST_MR_V6_CRUDEX_CERT_c1.sha256 | code/pk25/mr/MANIFEST_MR_V6_CRUDEX_CERT_c1.sha256 |
| code/pk22/midrow/psixy/ts_N4_J170_D_S_z9symxyp_v1.json | T | code/pk24/MANIFEST_NU_G_NOTE_v1.sha256 | 16 files, among them code/pk22/jobs/job262_lawcert_c3k_v2.console |
| code/pk22/midrow/psixy/ts_N3_S_z9symxyp_v1.json | T | code/pk24/MANIFEST_NU_G_NOTE_v1.sha256 | 16 files, among them code/pk22/jobs/job262_lawcert_c3k_v2.console |
| code/pk22/m3/out/m3_c3h_CE3H_N4_J300_c3h.json | T+P | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 | 5 files, among them code/pk22/m3/out/m3_lawcert_c3h_v1_1_N4.json |
| code/pk22/m3/out/m3_c3h_CS4H_N4_J300_c3h.json | T+P | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 | 5 files, among them code/pk22/m3/out/m3_lawcert_c3h_v1_1_N4.json |
| code/pk22/m3/out/m3_c3j_CS4TB_N4_J300_c3j.json | T+P | — | 2 files, among them code/pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py |
| code/pk22/m3/out/m3_c3l_CS4A_N4_J300_c3l.json | T+P | — | 2 files, among them code/pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py |
| code/pk22/m3/out/m3_c3n_FFH_N4_J300_c3n.json | T+P | — | 2 files, among them code/pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py |
| code/pk22/m3/out/m3_c3h_H4TH_N4_J300_c3h.json | T+P | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 | 5 files, among them code/pk22/m3/out/m3_lawcert_c3h_v1_1_N4.json |
| code/pk22/m3/out/m3_lawcert_c3h_v1_1_N4.json | P | — | 7 files, among them code/pk22/jobs/job229_lawcert_c3h_v1_1.console |
| code/pk22/m3/out/m3_lawcert_c3h_v1_1_4.out | T+P | — | 5 files, among them code/pk22/jobs/job233_mrx_v1_9.console |
| code/pk22/m3/out/m3_run_v1_9_3_asm.4_c3h_1.out | T+P | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 | 5 files, among them code/pk22/m3/out/m3_lawcert_c3h_v1_1_N4.json |
| code/pk22/m3/out/m3_c3h_CE3H_N3_J300_c3h.json | T+P | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 | 5 files, among them code/pk22/m3/out/m3_lawcert_c3h_v1_1_N3.json |
| code/pk22/m3/out/m3_c3h_CS4H_N3_J300_c3h.json | T+P | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 | 5 files, among them code/pk22/m3/out/m3_lawcert_c3h_v1_1_N3.json |
| code/pk22/m3/out/m3_c3j_CS4TB_N3_J300_c3j.json | T+P | — | 2 files, among them code/pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py |
| code/pk22/m3/out/m3_c3l_CS4A_N3_J300_c3l.json | T+P | — | 2 files, among them code/pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py |
| code/pk22/m3/out/m3_c3n_FFH_N3_J300_c3n.json | T+P | — | 2 files, among them code/pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py |
| code/pk22/m3/out/m3_c3h_H4TH_N3_J300_c3h.json | T+P | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 | 5 files, among them code/pk22/m3/out/m3_lawcert_c3h_v1_1_N3.json |
| code/pk22/m3/out/m3_lawcert_c3h_v1_1_N3.json | P | — | 6 files, among them code/pk22/jobs/job229_lawcert_c3h_v1_1.console |
| code/pk22/m3/out/m3_run_v1_9_3_asm.3_c3h_1.out | T+P | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 | 5 files, among them code/pk22/m3/out/m3_lawcert_c3h_v1_1_N3.json |
| code/pk25/m3/out/m3_lawcert_s9h_v1_1_N4.json | P | — | 6 files, among them code/pk25/asm/kt_s9h_ins_v2_2.py |
| code/pk25/m3/out/m3_lawcert_s9h_v1_1_N3.json | P | — | 6 files, among them code/pk25/asm/kt_s9h_ins_v2_2.py |
| code/pk25/m4h/M4H_KV_v1.txt | T+P | — | 6 files, among them code/pk25/asm/kt_s9h_ins_v2_2.py |
| code/pk22/m3/out/m3_c3j_DJ_N4_J300_c3j.json | T+P | — | 8 files, among them code/pk22/jobs/job236_mrj_v1.console |
| code/pk22/m3/out/m3_c3j_DJ_N3_J300_c3j.json | T+P | — | 8 files, among them code/pk22/jobs/job236_mrj_v1.console |
| code/pk22/midrow/g4/mrx/out/joint_float_v1_n4.out | T | code/pk22/midrow/g4/mrx/MANIFEST_JOINT_FLOAT_v1.sha256 | 5 files, among them code/pk22/jobs/job236_mrj_v1.console |
| code/pk22/midrow/g4/mrx/out/joint_float_v1_n3.out | T | code/pk22/midrow/g4/mrx/MANIFEST_JOINT_FLOAT_v1.sha256 | 5 files, among them code/pk22/jobs/job236_mrj_v1.console |
| code/pk25/m3/out/m3_s9h_DH_N4_J300_v1.json | P | — | 10 files, among them code/pk22/jobs/job236_mrj_v1.console |
| code/pk25/m3/out/m3_s9h_DH_N3_J300_v1.json | P | — | 10 files, among them code/pk22/jobs/job236_mrj_v1.console |
| code/pk25/c10/C10_RECORD_v1.kv | T | — | 13 files, among them code/pk22/jobs/job292_make_mrx_v1_10_r2.console |
| code/pk25/c13/C13_RECORD_v1_1.kv | T | — | 5 files, among them code/pk22/jobs/job292_make_mrx_v1_10_r2.console |
| code/pk22/midrow/e4/out/e4_comb_v2_N4.json | T+P | — | code/pk25/asm/kt_s9h_p3_v7_1.py |
| code/pk22/midrow/e4/out/e4_comb_v2_N3.json | T+P | — | code/pk25/asm/kt_s9h_p3_v7_1.py |
| code/pk22/midrow/e6/out/e6_comb_v3_N4.json | T+P | — | code/pk25/asm/kt_s9h_p3_v7_1.py |
| code/pk22/midrow/e6/out/e6_comb_v3_N3.json | T+P | — | code/pk25/asm/kt_s9h_p3_v7_1.py |
| code/pk25/P4_LEMMA_NOTE_v1_1.md | T+G | — | code/pk25/asm/kt_s9h_ins_v2_7.py |
| code/pk24/mr_engine/v17/kt_mr_v1_5_NOF1_L3.out | T | — | 3 files, among them code/pk24/jobs/job194_v1_8_4.console |
| code/pk23/pev/out/m3_cw_LC_N4_J300_cw.json | P | — | 4 files, among them code/pk23/pev/CW_LC_RECORDS_v1.md |
| code/pk23/pev/out/m3_cw_LC_N3_J300_cw.json | P | — | 4 files, among them code/pk23/pev/CW_LC_RECORDS_v1.md |
| code/pk23/pev/CW_LC_RECORDS_v1.md | T+P | — | code/pk23/pev/out/make_cw_summary_v1.out |
| code/pk23/pev/out/make_cw_summary_v1.out | T+P | — | — |
| code/pk23/pev/HL_CW_ENTRY_LIST_v1.json | T | — | 12 files, among them code/pk23/pev/CW_LC_RECORDS_v1.md |
| code/pk23/pev/out/make_cw_list_v1.out | T+P | — | — |
| code/pk23/pev/out/make_run_cw_v1.out | T+P | — | — |
| code/pk23/pev/out/make_rtwin_cw_v1.out | T+P | — | — |
| code/pk23/pev/out/rtwin_cw_v1_LC.4_z9sym.out | T+P | — | 3 files, among them code/pk23/pev/m3_run_v1_9_3_cw_v1.py |
| code/pk23/pev/out/rtwin_cw_v1_LC.3_z9sym.out | T+P | — | 3 files, among them code/pk23/pev/m3_run_v1_9_3_cw_v1.py |
| code/pk23/pev/out/rtwin_cw_v1_LC.4.log | identical | — | — |
| code/pk23/pev/out/rtwin_cw_v1_LC.3.log | identical | — | — |
| code/pk23/pev/out/m3_run_v1_9_3_LCa.3.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCa.4.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCa.3.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCa.4.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCk1.3.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCk1.4.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCk2.3.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCk2.4.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCk1.3.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCk1.4.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCk2.3.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCk2.4.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCr1.3.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCr1.4.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCr2.3.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCr2.4.out | T | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCr1.3.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCr1.4.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCr2.3.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_LCr2.4.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_asmc.3.out | T+P | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_asmc.4.out | T+P | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_asmc.3.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/m3_run_v1_9_3_asmc.4.err | identical | — | code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/hand/m3_run_v1_9_3_LCk1.3.json | identical | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/hand/m3_run_v1_9_3_LCk1.4.json | identical | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/hand/m3_run_v1_9_3_LCk2.3.json | identical | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/hand/m3_run_v1_9_3_LCk2.4.json | identical | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/hand/m3_run_v1_9_3_LCr1.3.json | identical | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/hand/m3_run_v1_9_3_LCr1.4.json | identical | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/hand/m3_run_v1_9_3_LCr2.3.json | identical | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/hand/m3_run_v1_9_3_LCr2.4.json | identical | — | 2 files, among them code/pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 |
| code/pk23/pev/out/make_m3_lawcert_cw_v1.out | T+P | — | — |
| code/pk23/pev/out/m3_lawcert_cw_v1_N4.json | P | — | 2 files, among them code/pk23/pev/CW_LC_RECORDS_v1.md |
| code/pk23/pev/out/m3_lawcert_cw_v1_N3.json | P | — | 2 files, among them code/pk23/pev/CW_LC_RECORDS_v1.md |
| code/pk23/pev/out/m3_lawcert_cw_v1_static.out | T | — | — |
| code/pk23/pev/out/m3_lawcert_cw_v1_4.out | T+P | — | code/pk23/pev/CW_LC_RECORDS_v1.md |
| code/pk23/pev/out/m3_lawcert_cw_v1_3.out | T+P | — | code/pk23/pev/CW_LC_RECORDS_v1.md |
| code/pk23/pev/out/make_m3_lawcert_hl_v1_1.out | T+P | — | — |
| code/pk23/pev/out/m3_lawcert_hl_v1_1_N4.json | P | — | code/pk23/pev/out/m3_lawcert_hl_v1_1_4.out |
| code/pk23/pev/out/m3_lawcert_hl_v1_1_N3.json | P | — | code/pk23/pev/out/m3_lawcert_hl_v1_1_3.out |
| code/pk23/pev/out/m3_lawcert_hl_v1_1_static.out | T | — | — |
| code/pk23/pev/out/m3_lawcert_hl_v1_1_4.out | T+P | — | — |
| code/pk23/pev/out/m3_lawcert_hl_v1_1_3.out | T+P | — | — |
| code/pk23/pev/diff_m3_reader_c3h_v1_2_to_hl_v1.txt | T | — | code/pk23/pev/out/make_m3_reader_hl_v1.out |
| code/pk23/pev/out/make_m3_reader_hl_v1.out | T+P | — | — |
| code/pk23/pev/out/m3_reader_hl_check_v1.out | identical | — | — |
| code/pk23/pev/diff_m3_reader_hl_v1_to_cw_v1.txt | T | — | code/pk23/pev/out/make_m3_reader_cw_v1.out |
| code/pk23/pev/diff_m3_reader_cw_check_v1_to_v1_1.txt | T | — | — |
| code/pk23/pev/out/make_m3_reader_cw_v1.out | T+P | — | — |
| code/pk23/pev/out/m3_reader_cw_check_v1.out | identical | — | — |
| code/pk23/pev/out/m3_reader_cw_check_v1_1.out | identical | — | code/pk23/pev/CW_LC_RECORDS_v1.md |
| code/pk22/jobs/job157_joint_float.console | T | code/pk22/midrow/g4/mrx/MANIFEST_JOINT_FLOAT_v1.sha256 | code/pk22/midrow/g4/mrx/MANIFEST_JOINT_FLOAT_v1.sha256 |
| code/pk22/midrow/g4/mrx/JOINT_FLOAT_v1_FREEZE_EVIDENCE.txt | T+P | code/pk22/midrow/g4/mrx/MANIFEST_JOINT_FLOAT_v1.sha256 | code/pk22/midrow/g4/mrx/MANIFEST_JOINT_FLOAT_v1.sha256 |
| code/pk25/m4h/diff_m4h_reader_v1_to_v1_1.txt | T | code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 | 2 files, among them code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 |
| code/pk25/m4h/diff_m4h_asm_v1_to_v1_1.txt | T | code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 | 2 files, among them code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 |
| code/pk25/out/job72_make.out | P | code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 | code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 |
| code/pk25/m4h/out/out_m4h_asm_v1.out | T | code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 | code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 |
| code/pk25/m4h/out/out_m4h_asm_v1.err | identical | code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 | code/pk25/m4h/MANIFEST_C5_M4H_v1_1.sha256 |
| code/pk22/jobs/job229_lawcert_c3h_v1_1.console | T+P | — | — |
| code/pk22/m3/C3H_ENTRY_LIST_v1.json | T+P | — | 14 files, among them code/pk22/m3/m3_lawcert_c3h_v1_1.py |
| code/pk22/m3/hand/m3_run_v1_9_3_CE3Hk1.3.json | identical | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_CE3Hk1.3.out |
| code/pk22/m3/hand/m3_run_v1_9_3_CE3Hk1.4.json | identical | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_CE3Hk1.4.out |
| code/pk22/m3/hand/m3_run_v1_9_3_CS4Hk1.3.json | identical | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_CS4Hk1.3.out |
| code/pk22/m3/hand/m3_run_v1_9_3_CS4Hk1.4.json | identical | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_CS4Hk1.4.out |
| code/pk22/m3/hand/m3_run_v1_9_3_H4THk1.3.json | identical | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_H4THk1.3.out |
| code/pk22/m3/hand/m3_run_v1_9_3_H4THk1.4.json | identical | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_H4THk1.4.out |
| code/pk22/m3/out/m3_run_v1_9_3_CE3Hk1.3.out | T | — | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_CE3Hk1.4.out | T | — | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_CS4Hk1.3.out | T | — | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_CS4Hk1.4.out | T | — | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_H4THk1.3.out | T | — | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_H4THk1.4.out | T | — | code/pk22/midrow/g4/MANIFEST_G4C_C3H_v1.sha256 |
| code/pk22/jobs/job262_lawcert_c3k_v2.console | T+P | — | — |
| code/pk22/m3/C3K_ENTRY_LIST_v1_2.json | T | — | 9 files, among them code/pk22/jobs/job262_lawcert_c3k_v2.console |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Dk1.3.json | P | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Dk1.3.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Dk1.4.json | P | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Dk1.4.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Nk2.3.json | P | — | 3 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Nk2.3.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Nk2.4.json | P | — | 3 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Nk2.4.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Nk3.3.json | P | — | 3 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Nk3.3.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Nk3.4.json | P | — | 3 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Nk3.4.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Nk4.3.json | P | — | 3 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Nk4.3.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Nk4.4.json | P | — | 3 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Nk4.4.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Nk5.3.json | P | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Nk5.3.out |
| code/pk22/m3/hand/m3_run_v1_9_3_F4Nk5.4.json | P | — | 2 files, among them code/pk22/m3/out/m3_run_v1_9_3_F4Nk5.4.out |
| code/pk22/m3/out/m3_c3kp_E4D_N3_J300_c3kp.json | T+P | — | 4 files, among them code/pk22/m3/out/m3_lawcert_c3k_v2_N3.json |
| code/pk22/m3/out/m3_c3kp_E4D_N4_J300_c3kp.json | T+P | — | 4 files, among them code/pk22/m3/out/m3_lawcert_c3k_v2_N4.json |
| code/pk22/m3/out/m3_c3kp_E4N_N3_J300_c3kp.json | T+P | — | 5 files, among them code/pk22/m3/out/m3_lawcert_c3k_v2_N3.json |
| code/pk22/m3/out/m3_c3kp_E4N_N4_J300_c3kp.json | T+P | — | 5 files, among them code/pk22/m3/out/m3_lawcert_c3k_v2_N4.json |
| code/pk22/m3/out/m3_run_v1_9_3_F4Dk1.3.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Dk1.4.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk1.3.out | T | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk1.4.out | T | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk2.3.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk2.4.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk3.3.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk3.4.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk4.3.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk4.4.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk5.3.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_F4Nk5.4.out | T+P | — | code/pk22/midrow/e4/MANIFEST_E4_C3K2_v1.sha256 |
| code/pk22/m3/out/m3_run_v1_9_3_asm.3_c3k2.out | T+P | — | 3 files, among them code/pk22/m3/out/m3_lawcert_c3k_v2_N3.json |
| code/pk22/m3/out/m3_run_v1_9_3_asm.4_c3k2.out | T+P | — | 3 files, among them code/pk22/m3/out/m3_lawcert_c3k_v2_N4.json |
| code/pk22/m3/out/m3ref_px22_v1_7_P16E4D.3.p1_z9symxy.out | T | — | 3 files, among them code/pk22/m3/m3_lawcert_c3k_v2.py |
| code/pk22/m3/out/m3ref_px22_v1_7_P16E4D.4.p1_z9symxy.out | T | — | 3 files, among them code/pk22/m3/m3_lawcert_c3k_v2.py |
| code/pk22/m3/out/m3ref_px22_v1_7_P16E4N.3.p2_z9symxy.out | T | — | 3 files, among them code/pk22/m3/m3_lawcert_c3k_v2.py |
| code/pk22/m3/out/m3ref_px22_v1_7_P16E4N.4.p2_z9symxy.out | T | — | 3 files, among them code/pk22/m3/m3_lawcert_c3k_v2.py |
