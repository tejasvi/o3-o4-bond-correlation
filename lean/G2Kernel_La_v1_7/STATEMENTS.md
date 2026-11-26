# STATEMENTS.md (v1_7): the G2 kernel track, step L-a (statements) with the L-b status
pk13. Written 2026-11-07T04:03:19Z (date -u). v1_7 adds module M12 (`Strip300.lean`): the named hypotheses hRHCover and hLadder and the statement `strip300_statement`, the Lean side of Corollary 6.20 for `J ≤ 300` (Section 6.5 of the paper) together with Theorem 1.4(ii). Statements only; no proof of M12 yet. Base: v1_6b (in the proof tree `G2Kernel_Lb_p11`, STATEMENTS.md sha8 00132340) and the statement tree La_v1_6 (manifest sha8 a0f5b1ab), whose statements the review found faithful (AUDIT_G2KERNEL_LA_v1_1_DELTA_rv05_ADD7, sha8 eaa95a3d) and run pb11 proved (manifest sha8 9b37c47f, summary sha8 ee232972). The statement files of v1_6 are unchanged; CHANGES_La_v1_7.md lists the changes.
Paper: the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344). Every theorem, lemma, proposition, corollary, section and display number in these files is the number that the paper prints.

## Conventions
- Every claim is a `Prop` definition named `*_statement`; step L-b proves each one as `theorem *_thm : *_statement` in modules under `G2Kernel/Proofs/`.
- Named hypotheses are `Prop` definitions in `Named.lean`, `NamedStrip.lean`, `CornerFactor.lean` and `Strip300.lean` (`hMalo` in `TheoremB.lean`), used only as explicit premises; none is an axiom. Kinds: *cited*, *paper proof*, *certificate*, *restatement* (a hypothesis that states part of a theorem's conclusion, with its backing named), and combinations.
- **Strip pairs (audit D1).** hStripIdentity and hStripCert are trusted for the mode data of the transfer operator of Section 6.3. hStripCert carries a threshold `m0` for every coupling: (C1)–(C5) at the separations `m ≥ m0`, and (C6), the determinant of Section 6.3, at `m < m0`. For the pairs with `m < m0`, (C6) is a direct certified evaluation of the sign of `Cov · Z²`, so for those pairs hStripCert with hStripIdentity is a restatement of their positivity. In Lean the mode data `md` are abstract, so the two hypotheses are jointly equivalent to the positivity of the regular pairs on the certified range. The kernel checks the inequality logic of Theorem 6.4 (`criterion_statement`) and the corner reduction. Defining `md` from the transfer operator is out of scope.
- **Strips for `20 ≤ J ≤ 300` (v1_7).** hRHCover is a restatement of Theorem 6.19 for `J ≤ 300`, backed by the route H certificate; nothing of the route H method is formalized. For these couplings the kernel checks only the combination of ranges and cases in `strip300_statement`.
- L-b counts as done only when every top theorem's `#print axioms` lists only `propext`, `Classical.choice`, `Quot.sound` (checked by the build script on every run), and the source gate finds no `sorry`, `admit`, `native_decide` or axiom declaration.
- Model (M0, `Defs.lean`) and the names of `Ledger.lean` are unchanged from v1_1 (Section 1.1; start of Section 6, row 0 on top). `grid33` is `strip 3`.

## A. Kernel statements
Every statement below except `strip300_statement` is proved in `G2Kernel_Lb_p11` (manifest sha8 9b37c47f; run pb11, summary sha8 ee232972), and each top theorem there depends only on `[propext, Classical.choice, Quot.sound]`. The L-b column names the run in which the proof of the current form first passed.

| statement | module | paper claim (label, number) | named hypotheses used | L-b |
|---|---|---|---|---|
| `ledger_statement` | M8 | Prop. 6.7, combinatorial part (nine conjuncts, as in v1_1) | none (decidable) | proved (pb2b) |
| `chebyshev_statement` | M1 | Chebyshev's sum inequality (Lemma 2.4, Theorem 1.1) | none | proved (pb1) |
| `chebyshev_strict_statement` | M1 | strict form (Theorem 1.1) | none | proved (pb1) |
| `variance_pos_statement` | M1v | strict variance: a function that differs at two charged labels has positive variance (Lemma 2.4 at a corner) | none | proved (pb10) |
| `covDeriv_statement N` | M2 | Prop. 2.1, first equality | none | proved (pb3b) |
| `labelCov_statement` | M2 | Prop. 2.1, second equality, single-label form | none | proved (pb3b) |
| `cycleG2_statement N` | M3 | Theorem 1.1 on one cycle | hFH, hKReg, hRatio, hCycleZ | proved (pb4b) |
| `cycleG2_strict_statement N` | M3 | Theorem 1.1, strict part, one cycle | hFH, hKReg, hRatio, hCycleZ | proved (pb4b) |
| `cactus_statement N` | M3c | Theorem 1.1 on cacti, all `J ≥ 0` | hSphereIso, hFH, hKReg, hRatio, hCycleZ | proved (pb9) |
| `cactus_strict_statement N` | M3c | Theorem 1.1, strict part: two edges of one cycle block with positive couplings | hSphereIso, hFH, hKReg, hRatio, hCycleZ | proved (pb9) |
| `blocks_statement N` | M4 | Lemma 2.3, first part, edge-pair form | hSphereIso | proved (pb6) |
| `blockRestrict_statement N` | M4b | Lemma 2.3, second part | hSphereIso | proved (pb9) |
| `corner_statement N` | M5 | Lemma 6.2 | hSphereIso | proved (pb5) |
| `rpCov_statement` | M6 | Lemma 6.1, last step | none | proved (pb2b) |
| `mirror33_statement N` | M6 | Lemma 6.1 for `(b0, b3)`, `(b0, b5)` | hRPGibbs | proved (pb7b) |
| `criterion_statement` | M7 | Theorem 6.4, inequality logic for one pair: Lemma 6.3 with (C1)–(C5) at `m ≥ m0` and (C6) at `m < m0` | none | proved (pb11) |
| `cover_statement` | M9 | joins of coupling ranges in Theorems 6.34(a) and 1.4(ii) | none | proved (pb1) |
| `strip3_statement N` | M10 | Theorem 1.4(ii) at `n = 3`, strict | hSphereIso, hWeak, hStripIdentity, hStripCert, hStripSpecial, hCornerPair | proved (pb11) |
| `stripD_statement N` | M10 | Theorem 1.4(ii), strict, every `n ≥ 3`, `0 < J ≤ 20` | hSphereIso, hWeak, hStripIdentity, hStripCert, hStripSpecial, hCornerPair | proved (pb11) |
| `G2_P3P3_statement N` | M10 | Theorem 6.34(a), `Cov ≥ 0` on `P_3 × P_3`, every `J ≥ 0` | hSphereIso, hShared, hRPGibbs, hWeak, hStripIdentity, hStripCert, hHub, hLBu | proved (pb11) |
| `cornerPair_statement N` | M10c | the corner step of Theorem 6.4: Lemma 2.4 at a corner gives `Cov > 0` | hKReg, hRatio, hCornerFactor (concludes hCornerPair) | proved (pb10) |
| `stripD_factor_statement N` | M10d | Theorem 1.4(ii) as `stripD_statement`, with no restatement for the corner pairs | hSphereIso, hWeak, hStripIdentity, hStripCert, hStripSpecial, hKReg, hRatio, hCornerFactor | proved (pb11) |
| `strip300_statement N` | M12 | Corollary 6.20 with Theorem 1.4(ii): `Cov ≥ 0` for every pair, every `n ≥ 1`, `0 ≤ J ≤ 300`; `Cov > 0` for `n ≥ 4`, `0 < J ≤ 300`, every pair other than the two vertical edges of one column | hSphereIso, hShared, hRPGibbs, hWeak, hStripIdentity, hStripCert, hKReg, hRatio, hCornerFactor, hHub, hLBu, hLadder, hRHCover | statement only (v1_7) |

**What the kernel proves of Theorem 6.34(a) and Theorem 1.4(ii) (wording for every L-b report).**
- Theorem 1.4(ii) (`stripD_factor_thm`; also `stripD_thm` and `strip3_thm` with hCornerPair as a premise). On `[0.0099, 20]`:
  - the regular pairs follow from `criterion_statement` with hStripIdentity and hStripCert (restatement strength, as above): (C1)–(C5) at the separations `m ≥ m0`; at `m < m0` the direct evaluation (C6) restates their positivity;
  - a vertical edge of an end column is replaced by the horizontal edge at its corner through `corner_statement`, with two steps when both edges are such verticals;
  - the two vertical edges of an interior column come from hStripSpecial ((C7));
  - the two edges at one corner come from hCornerFactor (paper proof) through Prop. 2.1 and `variance_pos_statement`; hCornerPair is derived (`cornerPair_thm`), no longer assumed.
  - On `(0, 1/100]`, hWeak gives every pair except the corner pairs.
- Theorem 6.34(a) (`G2_P3P3_thm`, `Cov ≥ 0`): at every `J ≥ 0`, Prop. 6.7 (ledger, invariance under the automorphisms in `d4`, mirror pairs, corner identity, and hShared for the pairs with a common vertex) reduces every pair to `Cov(s_{b0}, s_{sN})`. That covariance is positive for `J > 0` (hWeak on `(0, 1/100]`, the criterion route at `n = 3` on `[0.0099, 20]`, hHub on `[20, 100.68]`, hLBu beyond) and nonnegative at `J = 0` by continuity in `J`. So Theorem 6.34(a) uses neither hStripSpecial nor hCornerPair.
- What remains assumed for the strict Theorem 1.4(ii): hWeak and hStripSpecial (labelled restatements) and, for the regular pairs, hStripIdentity with hStripCert (restatement strength jointly).

**The strips for `0 ≤ J ≤ 300` (M12, v1_7; plan of the proof).** `strip300_statement` has two conjuncts.
- Nonstrict, every `n ≥ 1` and `0 ≤ J ≤ 300`, every pair of distinct edges:
  - `n ≥ 4` and `0 < J ≤ 20`: the route of Theorem 1.4(ii) (stripD) for the pairs not in one column; the two vertical edges of one column from hShared (they share the middle vertex);
  - `n ≥ 4` and `20 ≤ J ≤ 300`: hRHCover for the pairs not in one column, hShared for the two vertical edges of one column; at `J = 20` either range applies, and the proof splits by `J ≤ 20` or `20 < J`;
  - `n ≥ 4` and `J = 0`: continuity in `J` from the right, with the shift form of `gibbsCov_nonneg_of_shift` restricted to small shifts (the proof needs `Cov ≥ 0` only at `J = ε` for `0 < ε ≤ 20`, since nothing is assumed beyond `J = 300`);
  - `n = 3`: `G2_P3P3_thm` (every `J ≥ 0`); `n = 2`: hLadder; `n = 1`: the only pair is the two vertical edges of the single column, from hShared (or `blocks_thm`, which gives `Cov = 0`).
- Strict, `n ≥ 4`, `0 < J ≤ 300`, every pair of distinct edges other than the two vertical edges of one column: on `(0, 20]` the route of Theorem 1.4(ii); on `[20, 300]` hRHCover itself.
- hStripSpecial and hCornerPair are not premises. In `stripD_thm`, hStripSpecial enters only for the two vertical edges of an interior column, which the strict conjunct excludes and the nonstrict conjunct takes from hShared; the proof will use a form of `stripD_thm` restricted to the pairs not in one column. The corner pairs come from `cornerPair_thm` (hCornerFactor, hKReg, hRatio), as in `stripD_factor_thm`.
- Strictness as in the paper: `n ≥ 4` on `(0, 300]` for every pair not in one column; `n = 3` at `J > 20` and `n ≤ 2` are nonstrict, as in Corollary 6.20.

**Theorem 1.1 (`cactus_thm`, `cactus_strict_thm`).** Proved for every graph with a cactus decomposition, from hSphereIso and the analytic inputs of M3. The proof applies the second part of Lemma 2.3 once per block, peeling the last block of the list, and carries a cycle block to the cycle graph `C_n` by dropping the vertices off the cycle (their spins integrate to 1) and relabelling along `φ`.

**Corner pairs on the strict-variance route (M10c).** At a corner both edges carry the coupling `J`, so by Prop. 2.1 (`covDeriv_statement`, `labelCov_statement`) the covariance is `covW q r r`, the variance of `r_c(J) = k_c'(J)/k_c(J)` under the law `q_c ∝ u_c k_c(J)^2` of the common label. hCornerFactor gives `u_0, u_1 > 0`, so `q_0, q_1 > 0`, and hRatio gives `r_0(J) < r_1(J)`; `variance_pos_statement` then gives `Cov > 0`. At `N = 0` the premises cannot hold, since the partition function vanishes while the series is positive.

**Cactus decomposition (M3c).** `IsCactusWith G L` lists blocks, each `CactusBlock.edge e` with `e` an edge of `G`, or `CactusBlock.cycle n φ` with `n ≥ 3`, `φ : Fin n → V` injective and the edges of `C_n` mapped to edges of `G`. Every edge of `G` lies in a listed block, and every block meets the union of the earlier blocks in at most one vertex. For a finite graph, `IsCactus G` holds exactly when every block of `G` (maximal 2-connected subgraph or bridge) is a cycle or a single edge (ADD2, Q1). To build the list, take the blocks of each component in an order in which every block follows the block that contains its attaching cut vertex, for example breadth-first from any block; a leaf-first order can fail (on the path a-b-c-d, the list ab, cd, bc does).

**The threshold `m0` (v1_6).** `criterion_statement` reads: for mode data `D` and `m0 : ℕ`, `D.identity`, `m0 ≤ D.m → D.criterion` and `D.m < m0 → D.direct` give `0 < D.cov`. Here `D.direct` is `0 < D.cov * D.Ncal ^ 2`, the left side of (6): condition (C6) in the normalisation of Lemma 6.3, a positive multiple of the determinant `Cov · Z²` of Section 6.3. hStripCert gives a function `m0 : ℝ → ℕ` with, for every `n ≥ 3`, every `J` in the certified range and every regular pair of distinct edges, `(m0 J ≤ m → criterion) ∧ (m < m0 J → direct)`. The certificates fix `m0 ∈ {0, 1}` on each subinterval; where two subintervals overlap, either value serves at the common couplings. For the pairs with `m < m0` this is a restatement of positivity, labelled as such in the conventions above and in table B.

## B. Named hypotheses
| name | kind | paper claim | backing | Lean form |
|---|---|---|---|---|
| all of v1_2 except hCornerPair, hStripCert and hStripSpecial | as in v1_2 | as in v1_2 | as in v1_2 | unchanged |
| `hStripCert N md` | certificate for `m ≥ m0`; restatement backed by a direct certified evaluation for `m < m0`; restatement strength jointly with hStripIdentity | Theorem 6.6 for the hypotheses of Theorem 6.4 on the regular pairs | the certificates of Theorem 6.6: on each subinterval a threshold `m0 ∈ {0, 1}`, (C1)–(C5) at `m ≥ m0` and the direct evaluation (C6) at `m < m0`, for every pair of classes | `∃ m0 : ℝ → ℕ`, and for every `n ≥ 3`, `J ∈ [0.0099, stripTop N]` and regular pair of distinct edges, `(m0 J ≤ m → criterion) ∧ (m < m0 J → direct)` |
| `hStripSpecial N` | restatement | the two vertical edges of an interior column | condition (C7) of Theorem 6.4, certified with Theorem 6.6 | unchanged; not a premise of `strip300_statement` |
| `hCornerPair N` | derived | Theorem 6.4 and App. A, the two edges at one corner | `cornerPair_thm` proves it from hCornerFactor, hKReg and hRatio | unchanged; a premise only of `stripD_statement` and `strip3_statement` |
| `hCornerFactor N k` | paper proof | Lemma 2.4 at a corner of `P_3 × P_n`, with Prop. 3 of the note at `N = 3` and the label expansion with `W ≥ 0` (Lemma 4.1) at `N = 4` | as in v1_5 (note Prop. 3 and Lemma 2 at `N = 3`, `K = 1`; Lemma 4.1 at `N = 4`, `K = 4`) | unchanged |
| `hRHCover N` (new) | restatement | Theorem 6.19 (†) for `J ≤ 300` | the route H certificate: engine cs33h_1 with the ledger of its five batches and the independent union check ru2 over `[20, 300]` at `N = 3, 4` (notes LEMMA_STRIP_RH_v1_3, R7R8_v1_1, R9_v1_4, R10_v1_4, R11_v1_4, reviewed by the review and, for R2) | for every `n ≥ 4`, `20 ≤ J ≤ 300` and pair of distinct edges of `strip n` that are not `sameColumn n e f`: `0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)` |
| `hLadder N` (new) | cited (not formalized) | Theorem 1.2(a) at `N = 4` and Theorem 1.3 at `N = 3`, for `P_3 × P_2` | `P_3 × P_2` is a 2-connected outerplanar graph whose weak dual is a path (Theorem 1.2(a)), and an outerplanar graph has no `W_4` minor (Theorem 1.3) | for every `J ≥ 0` and pair of distinct edges of `strip 2`: `G2pair N (strip 2) (uniform J) e f` |

## C. Not in L-a, and plans
- Prop. 2.1 in its signed general form; M11 beyond `hMalo`; the paper's data in Lean; Theorem 1.3; Theorem 1.2 (so hLadder stays cited).
- **Strips beyond `J = 300`.** When Theorem S exists (now Section 6.6 of the paper), a hypothesis of the form of hRHCover for `J ≥ 300` (its certificate as backing) extends `strip300_statement` in the same pattern, with hShared again for the two vertical edges of one column. The corner route of M10c works for every `J > 0`.

## D. Questions for the check of v1_7
1. hRHCover: one hypothesis per `N`, for `n ≥ 4`, the closed range `20 ≤ J ≤ 300`, and every pair of distinct edges except `sameColumn n e f`. Is this faithful to Theorem 6.19 for `J ≤ 300` (whose scope also includes pairs with a common vertex, as there) and honestly labelled as a restatement?
2. hLadder is cited rather than derived in the kernel. A kernel derivation for `P_3 × P_2` would need reflection positivity for that graph (a further named hypothesis) and a ledger of its pairs as in Prop. 6.7. Is the cited form acceptable?
3. hStripSpecial and hCornerPair are not premises of `strip300_statement`; the proof will restrict `stripD_thm` to the pairs not in one column and take the corner pairs from `cornerPair_thm`. Any objection?
4. `J = 0` (for `n ≥ 4`) by continuity from the right using only shifts `0 < ε ≤ 20`. Acceptable, or should the nonstrict conjunct start at `J > 0`?
5. The strict conjunct on `[20, 300]` is hRHCover itself; it is kept so that the statement records the strictness of Corollary 6.20 for `J ≤ 300` together with the derived strictness on `(0, 20]`. Acceptable?

## E. Files, build order, L-b status
- Build order: Defs, Ledger, Named, Chebyshev, LabelCov, Cycle, Blocks, Cactus, Corner, RPstep, Criterion, NamedStrip, Cover, Assembly, CornerFactor, Strip300, TheoremB, root (`MODULES.txt`).
- Changed against La_v1_6: new `Strip300.lean` (M12); root `G2Kernel.lean` imports it (header v1_7); `MODULES.txt` lists it. All other statement files are byte-identical to La_v1_6, and so to `G2Kernel_Lb_p11`.
- L-b: as in section A. The next proof tree adds a proof module for M12 (with a form of `stripD_thm` for the pairs not in one column and the short-range continuity step), after the check of these statements.

## F. Paper items
- When `strip300_thm` is proved, the Formal verification paragraph can name hRHCover (restatement of Theorem 6.19 for `J ≤ 300`) and hLadder (Theorems 1.2(a), 1.3) among the stated hypotheses, and Corollary 6.20 for `J ≤ 300` among the checked deductions.
