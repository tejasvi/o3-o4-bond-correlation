# CHANGES_Lb_p13: proof tree G2Kernel_Lb_p13, the label-only revision of G2Kernel_Lb_p12
pk13, written 2026-11-07T11:36:17Z (date -u). The approval (logged 2026-11-07T11:26:55Z): route H is CLOSED; the backing of hRHCover moves from PENDING to the final ru2 run; no statement or proof changes; the review checks.

- Base: G2Kernel_Lb_p12 (manifest sha8 d55cd629; run pb12, summary sha8 4180fd01; the review ADD9 sha8 f2c0f1fa: 8 FAITHFUL, 0 FIX).
- Backing: pk05/out/ru2_U2.out (sha8 f6f2280c; MANIFEST_ru2_U2_out sha8 0979d81b; job manifest out/pd_U2_jobs.sha256, sha8 a9a71ab7, 358 jobs): VALID True; VERDICT N=3 [20, 300]: COVERED; VERDICT N=4 [20, 300]: COVERED; log pk05/RU2_LOG_pk05.md (sha8 e3159b02).
- Changed files (2):
  - src/G2Kernel/Strip300.lean (sha8 1f719208 -> 9fa78238): the header comment (its citations of the paper; the backing sentence), the SOURCE comment above hRHCover, and the docstring of hRHCover (the PENDING clause replaced by the run). Every line from `def hRHCover` to the end of the file, and the import and namespace lines, are byte-identical to p12.
  - STATEMENTS.md (v1_7b, sha8 75ae3faa -> v1_7c, sha8 113bc940): a new header paragraph, the paper line, the L-b bullet (the fuller wording of the ADD9 section 2, with the backing in place of "pending"), the strip300_statement row and the hRHCover row.
- Byte-identical to p12: MODULES.txt and every other file under src/, among them Proofs/Strip300Proof.lean (sha8 9ec7aa4d) and Proofs/Axioms.lean.
- Not carried: CHANGES_Lb_p12.md (it stays in G2Kernel_Lb_p12).
- Build: lb_build_v1.sh (sha8 788d13a6), run tag pb13.

## Citations of the paper (this release copy)
The paper is "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344). In this copy every
citation of one of its results gives the number that the paper prints. The earlier copy cited drafts of the paper by their own numbers,
some with LaTeX labels, and named the drafts by file name. One mechanical pass from the paper's final build changed the citations in
comments only: each draft number was mapped to its label through that draft's aux file and the label to the printed number; a cited part
was checked to read the same in the draft and in the paper; a cited section was matched by its title; the module headers, the paper line
of STATEMENTS.md and one line reference were edited by hand. Citations of other works and of the separate note keep their own numbers.
Every source's comment-stripped text equals that of the earlier copy, every module was rebuilt (lean/rebuild), and every build product
equals the earlier copy's build in its imports, constant names and, for every constant, kind, universe parameters, type and value
(Expr.equal), with a SAME and a DIFF control beside it.
