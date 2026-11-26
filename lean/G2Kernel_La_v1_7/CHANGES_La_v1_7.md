# CHANGES_La_v1_7: what L-a v1_7 changes against v1_6
pk13. Written 2026-11-07T04:03:31Z (date -u). Base: lean/G2Kernel_La_v1_6 (manifest sha8 a0f5b1ab), which stays frozen, with the labelling of STATEMENTS.md v1_6b (in lean/G2Kernel_Lb_p11, sha8 00132340). Purpose: the Lean side of Corollary 6.20 for `J ≤ 300` (Section 6.5 of the paper), statements only.

| file | change |
|---|---|
| `src/G2Kernel/Strip300.lean` | new module M12: hRHCover (restatement of Theorem 6.19 for `J ≤ 300`, backed by the route H certificate), hLadder (cited: Theorem 1.2(a) at `N = 4`, Theorem 1.3 at `N = 3`, for `P_3 × P_2`), and `strip300_statement` (nonstrict for every `n ≥ 1`, `0 ≤ J ≤ 300`; strict for `n ≥ 4`, `0 < J ≤ 300`, pairs not in one column) |
| `src/G2Kernel.lean` | imports G2Kernel.Strip300; header v1_7 |
| `MODULES.txt` | G2Kernel/Strip300 after G2Kernel/CornerFactor |
| `STATEMENTS.md` | v1_7: the five v1_6 statements marked proved (pb11); row M12; the proof plan of M12; hRHCover and hLadder in B; five questions in D |

All other statement files are byte-identical to La_v1_6 and to the proof tree `G2Kernel_Lb_p11`.

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
