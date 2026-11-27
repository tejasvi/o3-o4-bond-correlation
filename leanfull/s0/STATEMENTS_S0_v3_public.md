# STATEMENTS_S0_v3: the Lean statements of stage S0, each written before its proof

Every Lean statement in this file is about finite simple graphs (Mathlib's SimpleGraph); the paper's Theorems 1.1 and
1.2(b) also cover parallel edges through its Section 3.3 reduction, which is not formalized.

This v3 replaces STATEMENTS_S0_v2.md (sha8 de8596fc, unchanged): the note on the final T6-T8 forms near its end (AUDIT_S0_v2
item (e)). Nothing else changed.

This v2 replaces STATEMENTS_S0.md (sha8 63da6e06, unchanged): the wording of H28 per representative (audit item 3f), the
form of `CConc_one` (audit minor note), and the follow-up section at the end (audit items 3h and 7). Module names: the v2 chain
uses G2S0.OrbitM2v2 and G2S0.TopS0v2 in place of G2S0.OrbitM2 and G2S0.TopS0 (same statements, plus the additions below).

Paper: "Positive correlation of bond energies in the O(3) and O(4) models", release source v4.41
(the LaTeX source `G2_PAPER_v4_41_release.tex`; "tex l.N" is a line of that file).
Package: the Lean trees `lean/G2Kernel_Lb_p13` and `lean/StripIII_v2` of this archive, copied unchanged into the build (`s0/pkg/`).
New modules: `s0/src/G2S0/*.lean`, namespace `G2Kernel` (so the package's names resolve unqualified).
Standard: kernel-only (no sorry, admit, native_decide or new axiom); `#print axioms` of each main theorem must list only
propext, Classical.choice and Quot.sound. A statement change against the brief or the plan is flagged **CHANGED**.

## (a) H1, the rotation invariance of omega (module G2S0.SphereIso)

Paper fact: omega is the rotation-invariant probability measure on S^{N-1} (Section 1.1, tex l.62-63). The package defines
`omega N` as the cone measure `volume.toSphere` divided by its total mass (G2Kernel/Defs.lean) and states the invariance as the
named hypothesis H1 `hSphereIso N` (G2Kernel/Named.lean). S0 (a) proves it for every N, so H1 is a theorem.

```lean
/-- the cone measure `volume.toSphere` on the unit sphere of `ℝ^N` is invariant under every linear isometry -/
theorem toSphere_measurePreserving_isometry (N : ℕ) (A : Amb N ≃ₗᵢ[ℝ] Amb N) :
    MeasurePreserving (fun x : Sph N => (⟨A (x : Amb N), by simp⟩ : Sph N))
      (volume : Measure (Amb N)).toSphere (volume : Measure (Amb N)).toSphere

/-- **H1 is a theorem**: `hSphereIso N` holds for every `N` -/
theorem hSphereIso_holds (N : ℕ) : hSphereIso N
```

## (c) The orbit step (modules G2S0.Box5Reps, G2S0.Orbit, G2S0.OrbitM2)

Paper facts: the proofs of Propositions B.14, B.22 and B.24 (tex l.3350, l.3529-3540, l.3579-3602) certify one pair of each orbit
or class and pass to the other pairs because "the other pairs of a class or an orbit are images of one of its pairs under the
reflections in the middle row and in the vertical midline, which preserve the Gibbs measure". The package states H26-H28 per
class with this step not formalized (StripIII.Small5Statement, StripIIIM1.HStatement, StripIIIM2.M2Statement).

Step 1, the Gibbs law and the two reflections (G2S0.Orbit).
```lean
/-- a graph automorphism preserves the Gibbs law at uniform coupling (every N; the package's gibbsExp_comp_bij is N > 0) -/
theorem gibbsExp_auto_invariant {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (J0 : ℝ)
    (g : V → V) (hbij : Function.Bijective g) (hadj : ∀ p q, G.Adj p q ↔ G.Adj (g p) (g q)) (F : Config N V → ℝ) :
    gibbsExp N G (uniform J0) (fun σ => F (σ ∘ g)) = gibbsExp N G (uniform J0) F
theorem G2pair_auto_iff {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (J0 : ℝ)
    (g : V → V) (hbij : Function.Bijective g) (hadj : ∀ p q, G.Adj p q ↔ G.Adj (g p) (g q)) (a b : Sym2 V) :
    G2pair N G (uniform J0) (Sym2.map g a) (Sym2.map g b) ↔ G2pair N G (uniform J0) a b
/-- the reflection of P_3 × P_n in the middle row (the package's `stripReflV` is the one in the vertical midline) -/
def rowFlip {n : ℕ} (p : Fin 3 × Fin n) : Fin 3 × Fin n := (p.1.rev, p.2)
theorem rowFlip_bijective {n : ℕ} : Function.Bijective (rowFlip (n := n))
theorem stripReflV_bijective {n : ℕ} : Function.Bijective (stripReflV (n := n))
theorem strip_adj_rowFlip {n : ℕ} (p q : Fin 3 × Fin n) : (strip n).Adj p q ↔ (strip n).Adj (rowFlip p) (rowFlip q)
theorem strip_adj_stripReflV {n : ℕ} (p q : Fin 3 × Fin n) :
    (strip n).Adj p q ↔ (strip n).Adj (stripReflV p) (stripReflV q)
theorem edgeCode_rowFlip {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) :
    Sym2.map rowFlip e ∈ (strip n).edgeSet ∧ edgeCode (Sym2.map rowFlip e) = (edgeCode e).flip
/-- the orbit step for one representative code pair (a, b): the eight images under the swap and the two reflections -/
theorem G2pair_of_orbitForms {N n : ℕ} {J : ℝ} {a b : ECode} (ha : a.valid n = true) (hb : b.valid n = true)
    (hrep : ∀ e' ∈ (strip n).edgeSet, ∀ f' ∈ (strip n).edgeSet, edgeCode e' = a → edgeCode f' = b →
      G2pair N (strip n) (uniform J) e' f')
    {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet)
    (hmem : (edgeCode e, edgeCode f) ∈ StripIII.orbitForms n a b) : G2pair N (strip n) (uniform J) e f
```

Step 2, the per-representative hypotheses and the derivation of the package's per-class forms. H26 and H27 per representative
ask for exactly the pairs that their records certify (the 36 box representatives, the 377 rows of M1's record), for J >= jLow N.
H28 per representative asks for one normal-form pair of every tail class at every n. It is equivalent to the package's H28
(`hM2tailRep_iff`, G2S0.OrbitM2v2), but it is not a finite list of record rows: M2's certified record gives the finite checks
(2)-(5) of the proof of Proposition B.24, and reaching every class at every n from them needs Lemma B.23 and the covering argument
of Proposition B.24 (tex l.3553-3577, l.3594), which are paper proofs.
```lean
/-- H26 per representative: the n = 5 box records, one pair per orbit (`StripIII.box5Reps`, the tables' orbit column) -/
def hBoxAll5rep (N : ℕ) (R : List (ECode × ECode)) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ q ∈ R, ∀ e ∈ (strip 5).edgeSet, ∀ f ∈ (strip 5).edgeSet,
    edgeCode e = q.1 → edgeCode f = q.2 → G2pair N (strip 5) (uniform J) e f
theorem hBoxAll5_of_rep (N : ℕ) :
    hBoxAll5rep N StripIII.box5Reps → hBoxAll5 N (box5AllList34 ++ box5Stage2)

/-- H27 per representative: M1's record rows, one pair per class (`StripIII.m1List` holds the rows' representatives) -/
def hM1rep (N : ℕ) (L : List (ℕ × ECode × ECode)) (nmax : ℕ) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ q ∈ L, 6 ≤ q.1 → q.1 ≤ nmax →
    ∀ e ∈ (strip q.1).edgeSet, ∀ f ∈ (strip q.1).edgeSet, edgeCode e = q.2.1 → edgeCode f = q.2.2 →
      G2pair N (strip q.1) (uniform J) e f
theorem hM1_of_rep (N : ℕ) : hM1rep N StripIII.m1List StripIII.NMAX_M1 → hM1 N StripIII.m1List StripIII.NMAX_M1

/-- the records' normal form of a to-do pair (the representatives of M1's and M2's rows; Appendix B, tex l.3372-3381): the
middle-row edge h = hor 1 i first; the partner hor 0 i (an interior same-bond pair, with i <= n - 2 - i), hor 2 j with j > i
(type t, by its flip image), ver 0 j with j >= i + 2 (type a), or hor 1 j with j >= i + 2 and i + j + 2 < n (type h, d < d') -/
def StripIII.recNF (n : Nat) : ECode → ECode → Bool
  | .hor 1 i, .hor 0 j => j == i && decide (i ≤ n - 2 - i)
  | .hor 1 i, .hor 2 j => decide (i < j)
  | .hor 1 i, .ver 0 j => decide (i + 2 ≤ j)
  | .hor 1 i, .hor 1 j => decide (i + 2 ≤ j) && decide (i + j + 2 < n)
  | _, _ => false
/-- H28 per representative: one normal-form pair per tail class at every n (equivalent to H28; backed by M2's record
with Lemma B.23 and the covering argument of Proposition B.24) -/
def hM2tailRep (N : ℕ) (D0 M0 : ℕ) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ n : ℕ, ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet,
    StripIII.recNF n (edgeCode e) (edgeCode f) = true →
    StripIII.todoH n (edgeCode e) (edgeCode f) = true → StripIII.sameBondEnd n (edgeCode e) (edgeCode f) = false →
    StripIII.tailClass D0 M0 (StripIII.classOf n (edgeCode e) (edgeCode f)) = true →
      G2pair N (strip n) (uniform J) e f
/-- the class argument at every n: each to-do pair outside the end orbit is an image of a normal-form pair with the same
to-do, end-orbit and tail status -/
theorem StripIII.exists_recNF {n D0 M0 : Nat} {x y : ECode} (h : StripIII.todoH n x y = true)
    (hs : StripIII.sameBondEnd n x y = false) (ht : StripIII.tailClass D0 M0 (StripIII.classOf n x y) = true) :
    ∃ a b : ECode, StripIII.recNF n a b = true ∧ StripIII.todoH n a b = true ∧ StripIII.sameBondEnd n a b = false ∧
      StripIII.tailClass D0 M0 (StripIII.classOf n a b) = true ∧ (x, y) ∈ StripIII.orbitForms n a b
theorem hM2tail_of_rep (N D0 M0 : ℕ) : hM2tailRep N D0 M0 → hM2tail N D0 M0
```

Step 3, the top theorems with H1 discharged and H26-H28 per representative (G2S0.OrbitM2): `smallN_statement_S0 N` is
`smallN_statementL N (box5AllList34 ++ box5Stage2)` with the premise hSphereIso N removed and hBoxAll5 N (...) replaced by
hBoxAll5rep N box5Reps; `fullStrip_statement_S0 N` is `fullStrip_statementL N box5List (o5List ++ L55)
(box5AllList34 ++ box5Stage2) m1List NMAX_M1 D0_M2 M0_M2` with hSphereIso N removed and hBoxAll5, hM1, hM2tail replaced by
hBoxAll5rep N box5Reps, hM1rep N m1List NMAX_M1, hM2tailRep N D0_M2 M0_M2 (the other premises verbatim).
```lean
theorem smallN_thm_S0 (N : ℕ) : smallN_statement_S0 N
theorem fullStrip_thm_S0 (N : ℕ) : fullStrip_statement_S0 N
```

Notes on (c) as built (2026-11-27):
- Name fix only: the package defines `box5AllList34` and `box5Stage2` in namespace `G2Kernel` (not `G2Kernel.StripIII`), so the
  statement of `hBoxAll5_of_rep` above names them without the `StripIII.` prefix. No statement changed in substance.
- Helpers added: `gibbsCov_auto_invariant`, `G2pair_of_orbitForms` uses `edgeCode_stripReflV` (StripIII.Proof); the general forms
  `hBoxAll5_of_rep_gen` (any representative list R passing `StripIII.box5RepCheck R L`, checked by decide for the records' lists:
  `box5RepCheck_final`) and `hM1_of_rep_gen` (any list passing `m1Orbit` and `m1InClass` at each n, which HCheckM1 checks for
  `m1List`, n = 6..11); controls `box5Reps_controls` (each representative lies in the final list; the 36 lie in 36 distinct
  orbits), `StripIII.m1List_recNF`, `StripIII.m2Rows_recNF` (every M1 row and every finite M2 row is in normal form).
- `StripIII.exists_recNF` is proved for every n by explicit witnesses (16 cases, each with arithmetic side conditions), not by
  decide. A brute-force control (scripts/check_recnf_v1.py, n = 6..14) found exactly one normal-form image in every to-do orbit
  outside the end orbit, and per-n counts equal to M1's rows (24, 36, 51, 68, 88, 110) and M2's finite rows.

## (b) The concrete data for N >= 2 and H3 for the paper's k (module G2S0.KData)

Paper facts (Section 2.1, tex l.203-219): for N >= 2 and lambda = N/2 - 1, C~_l is the Gegenbauer polynomial C^lambda_l normalized
by C~_l(1) = 1 (N = 2: C~_l(cos t) = cos(l t)); d_l = dim H_l; k_l(J) = Gamma(N/2) sum_m (J/2)^(l+2m) / (m! Gamma(l+m+N/2)); for J > 0
every k_l(J) is positive, and on every [a, b] in (0, oo) there is c with |k_l^(j)(J)| <= c (l+1)^j (J/2)^l / l! for j = 0, 1, 2.
H3 is the package's named hypothesis `hKReg k` (G2Kernel.Named). S0 (b) proves it for the paper's k.

```lean
/-- the paper's coefficient, verbatim (Section 2.1, the line after display (3)) -/
def kConc (N : ℕ) (l : ℕ) (J : ℝ) : ℝ :=
  Real.Gamma ((N : ℝ) / 2) *
    ∑' m : ℕ, (J / 2) ^ (l + 2 * m) / ((m.factorial : ℝ) * Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2))
/-- d_l = dim H_l = C(l + N - 1, l) - C(l + N - 3, l - 2) (the second term only for l >= 2) -/
def dConc (N : ℕ) (l : ℕ) : ℝ :=
  (Nat.choose (l + N - 1) l : ℝ) - (if 2 ≤ l then (Nat.choose (l + N - 3) (l - 2) : ℝ) else 0)
/-- C~_l: C~_0 = 1, C~_1(t) = t, and the normalized three-term recurrence of C^lambda_l with 2 lambda = N - 2,
C~_{n+1}(t) = ((2n + N - 2) t C~_n(t) - n C~_{n-1}(t)) / (n + N - 2) for n >= 1 (N = 2: Chebyshev T_l) -/
def CConc (N : ℕ) : ℕ → ℝ → ℝ
  | 0, _ => 1
  | 1, t => t
  | n + 2, t => ((2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * t * CConc N (n + 1) t - ((n : ℝ) + 1) * CConc N n t) /
      (((n : ℝ) + 1) + ((N : ℝ) - 2))

/-- **H3 for the paper's k** -/
theorem hKReg_kConc (N : ℕ) (hN : 2 ≤ N) : hKReg (kConc N)
/-- the normalization C~_l(1) = 1 (the second conjunct of H2 `hFH` for this C) -/
theorem CConc_one (N : ℕ) (hN : 2 ≤ N) : ∀ l : ℕ, CConc N l 1 = 1
```

## (d) Fidelity of Theorem 1.1: IsCactus G iff every block of G is a cycle or a single edge (modules G2S0.BlocksA, G2S0.BlocksB)

Paper fact: Theorem 1.1 (tex l.108-111) assumes "every block of G is a cycle or a single edge"; a block is "a maximal connected
subgraph without a cut vertex" (Section 5.1, tex l.1565, after [Die17, Section 3.1]). The package states Theorem 1.1 for
`IsCactus G` (an ordered block list, G2Kernel/Cactus.lean) and argues the equivalence on paper only (its STATEMENTS.md).
Convention: subgraphs are spanning (`H : SimpleGraph V` with `H ≤ G`), and the vertex set of `H` is the set of vertices that carry an
edge of `H`. So the blocks below are the blocks with at least one edge (the maximal 2-connected subgraphs and the bridges);
isolated vertices, which the paper's definition counts as blocks K_1, are left out, as in the package's STATEMENTS.md (they carry no
bond energy, and IsCactus allows them).
```lean
/-- the vertices that carry an edge of H -/
def vsupp (H : SimpleGraph V) : Set V := {x | ∃ y, H.Adj x y}
/-- H with the vertex v deleted -/
def delV (H : SimpleGraph V) (v : V) : SimpleGraph V   -- Adj x y := H.Adj x y ∧ x ≠ v ∧ y ≠ v
/-- connected (on its vertices) and without a cut vertex -/
def ConnNoCut (H : SimpleGraph V) : Prop :=
  (∀ x ∈ vsupp H, ∀ y ∈ vsupp H, H.Reachable x y) ∧
  (∀ v, ∀ x ∈ vsupp H, ∀ y ∈ vsupp H, x ≠ v → y ≠ v → (delV H v).Reachable x y)
/-- a block of G: a maximal subgraph with an edge that is connected and has no cut vertex -/
def IsBlock (G B : SimpleGraph V) : Prop :=
  B ≤ G ∧ (∃ x y, B.Adj x y) ∧ ConnNoCut B ∧ ∀ B' : SimpleGraph V, B ≤ B' → B' ≤ G → ConnNoCut B' → B' = B
/-- B is a cycle: the image of C_n, n ≥ 3, under an injective map -/
def IsCycleSG (B : SimpleGraph V) : Prop :=
  ∃ (n : ℕ) (φ : Fin n → V), 3 ≤ n ∧ Function.Injective φ ∧
    ∀ x y, B.Adj x y ↔ ∃ a b, (SimpleGraph.cycleGraph n).Adj a b ∧ x = φ a ∧ y = φ b
/-- B is a single edge -/
def IsEdgeSG (B : SimpleGraph V) : Prop := ∃ u w, u ≠ w ∧ ∀ x y, B.Adj x y ↔ s(x, y) = s(u, w)
/-- the hypothesis of Theorem 1.1 -/
def BlocksCycleOrEdge (G : SimpleGraph V) : Prop := ∀ B, IsBlock G B → IsCycleSG B ∨ IsEdgeSG B

theorem isCactus_imp_blocks (G : SimpleGraph V) : IsCactus G → BlocksCycleOrEdge G
theorem blocks_imp_isCactus [Finite V] (G : SimpleGraph V) : BlocksCycleOrEdge G → IsCactus G
theorem isCactus_iff_blocks [Finite V] (G : SimpleGraph V) : IsCactus G ↔ BlocksCycleOrEdge G
/-- Theorem 1.1 in the paper's form: H1 discharged, the hypothesis on the blocks -/
theorem cactus_thm_blocks (N : ℕ) :
  ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d →
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J → ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → G2pair N G J e f
```

Notes on (d) as built (2026-11-27): all statements above proved as written (G2S0.BlocksA, G2S0.BlocksB), with these helpers:
`noCross` (a connected subgraph without a cut vertex does not cross a separation at one vertex or at none), `connNoCut_cycle`
(a cycle is connected without a cut vertex), `edges_in_one_block` (its edges lie in one block of a cactus list), `exists_sep`
(a graph with an edge that is not connected without a cut vertex splits at one vertex or at none), `isBlock_of_restrict`,
`rootedCactus_exists` (lists rooted at a vertex, by induction on the number of edges). `blocks_imp_isCactus` and
`isCactus_iff_blocks` take `[Finite V]`; `isCactus_imp_blocks` holds for every V.
Not covered: the strict part of Theorem 1.1 is still the package's form (a cycle block of a cactus list, `cactus_strict_thm_S0`);
matching the paper's "e and f lie on a common cycle" also needs the lemma that every cycle of such a graph is a block of its list.

## Summary module G2S0.TopS0
The eight top theorems with the S0 discharges: T1 `cactus_thm_blocks` (paper form) and `cactus_thm_concrete` (paper's data, H1 and
H3 discharged); T2 `cactus_strict_thm_S0`; T3 `stripD_factor_thm_S0`; T4 `G2_P3P3_thm_S0`; T5 `strip300_thm_S0`; T6
`smallN_thm_S0`; T7 `stripIII_thm_S0`; T8 `fullStrip_thm_S0` and `fullStrip_thm_concrete`. Each S0 statement is the package's
statement with the premise `hSphereIso N` removed (and, where marked, H26-H28 per representative or k = kConc N without H3); every
other premise is copied verbatim, and each proof applies the package theorem, so a dropped or changed premise would not compile.
`#print axioms` of every theorem: AXIOMS_S0.txt (from logs/j25_all_clean.out).


## Follow-up after AUDIT_S0_v1 (2026-11-27): H22 and H25 per representative, the strict part, the wording of H28

### (3h) H22 `hBox5` and H25 `hO5` per representative (modules G2S0.BoxRepsB, G2S0.OrbitB)
Paper facts: Proposition B.14's box pairs at n = 5 and Proposition B.15's rows at N = 4 (tex l.3350, l.3361) are certified at one
pair per orbit; the other members follow by the two reflections, as for H26-H28. The package lists every member
(`StripIII.box5List`, 22 pairs in 6 orbits; `StripIII.o5List ++ L55`, 8 + 2 pairs in 3 orbits). The representatives are the
record tables' orbit column (G2S0.BoxRepsB, made by scripts/gen_boxrepsB_v1.py from the tables named in the package docstrings).
```lean
/-- H22 per representative: the box record of run 013023Z, one pair per orbit of `box5List` (`StripIII.box5RepsH22`) -/
def hBox5rep (N : ℕ) (R : List (ECode × ECode)) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ q ∈ R, ∀ e ∈ (strip 5).edgeSet, ∀ f ∈ (strip 5).edgeSet,
    edgeCode e = q.1 → edgeCode f = q.2 → G2pair N (strip 5) (uniform J) e f
theorem hBox5_of_rep (N : ℕ) : hBox5rep N StripIII.box5RepsH22 → hBox5 N StripIII.box5List
/-- H25 per representative: the box records of runs 013023Z (n = 6) and 045359Z (n = 7), at N = 4, one pair per orbit of
`o5List ++ L55` (`StripIII.o5Reps`, entries (n, code pair)) -/
def hO5rep (N : ℕ) (R : List (ℕ × ECode × ECode)) : Prop :=
  N = 4 → ∀ J : ℝ, jLow N ≤ J → ∀ q ∈ R, ∀ e ∈ (strip q.1).edgeSet, ∀ f ∈ (strip q.1).edgeSet,
    edgeCode e = q.2.1 → edgeCode f = q.2.2 → G2pair N (strip q.1) (uniform J) e f
theorem hO5_of_rep (N : ℕ) : hO5rep N StripIII.o5Reps → hO5 N (StripIII.o5List ++ L55)
```
The top theorems with every orbit-step hypothesis per representative: `stripIII_statement_S0r N` is T7
(`stripIII_full_statementL N box5List (o5List ++ L55)`) without `hSphereIso N` and with `hBox5rep N box5RepsH22`,
`hO5rep N o5Reps` in place of `hBox5 N box5List`, `hO5 N (o5List ++ L55)`; `fullStrip_statement_S0r N` is T8 without
`hSphereIso N` and with H22, H25, H26, H27, H28 per representative (the other premises verbatim).
```lean
theorem stripIII_thm_S0r (N : ℕ) : stripIII_statement_S0r N
theorem fullStrip_thm_S0r (N : ℕ) : fullStrip_statement_S0r N
theorem fullStrip_thm_concrete_r (N : ℕ) (hN : N = 3 ∨ N = 4) : ...   -- the same with k = kConc N and H3 dropped
```

### (7) The strict part of Theorem 1.1 in the paper's form (module G2S0.BlocksC)
Paper fact: Theorem 1.1, second sentence (tex l.110): the inequality is strict when e and f lie on a common cycle whose couplings
are all positive. A cycle of G is given by n >= 3 and an injective φ : Fin n → V whose cycle edges are edges of G; its edges are
`(CactusBlock.cycle n φ).edges`.
```lean
/-- a cycle inside a cycle is the whole cycle -/
theorem cycle_le_cycle {n m : ℕ} (hn : 3 ≤ n) (hm : 3 ≤ m) {φ : Fin n → V} {ψ : Fin m → V}
    (hφ : Function.Injective φ) (hψ : Function.Injective ψ)
    (hle : blockSG (CactusBlock.cycle n φ) ≤ blockSG (CactusBlock.cycle m ψ)) :
    blockSG (CactusBlock.cycle m ψ) ≤ blockSG (CactusBlock.cycle n φ)
/-- every cycle of G is a cycle block of any cactus list of G, with the same edges -/
theorem cycle_mem_list {G : SimpleGraph V} {L : List (CactusBlock V)} (hL : IsCactusWith G L) {n : ℕ} {φ : Fin n → V}
    (hn : 3 ≤ n) (hφ : Function.Injective φ) (hG : ∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) :
    ∃ (m : ℕ) (ψ : Fin m → V), CactusBlock.cycle m ψ ∈ L ∧ (CactusBlock.cycle m ψ).edges = (CactusBlock.cycle n φ).edges
/-- **Theorem 1.1, strict part, in the paper's form** (H1 discharged, the hypothesis on the blocks) -/
theorem cactus_strict_thm_blocks (N : ℕ) :
    ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d → (∀ c, 0 < d c) →
      ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
        ∀ J : Sym2 V → ℝ, Ferro G J →
        ∀ (n : ℕ) (φ : Fin n → V), 3 ≤ n → Function.Injective φ →
          (∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) →
          (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
          ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
            0 < gibbsCov N G J (bond e) (bond f)
/-- d_l > 0 for the paper's d, N ≥ 2 -/
theorem dConc_pos (N : ℕ) (hN : 2 ≤ N) (l : ℕ) : 0 < dConc N l
/-- the strict part for the paper's data (N ≥ 2): H1, H3 and the positivity of d discharged; H2, H4, H5 remain -/
theorem cactus_strict_concrete (N : ℕ) (hN : 2 ≤ N) :
    hFH N (kConc N) (dConc N) (CConc N) → hRatio (kConc N) → hCycleZ N (kConc N) (dConc N) →
      ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
        ∀ J : Sym2 V → ℝ, Ferro G J →
        ∀ (n : ℕ) (φ : Fin n → V), 3 ≤ n → Function.Injective φ →
          (∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) →
          (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
          ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
            0 < gibbsCov N G J (bond e) (bond f)
```

### (3f) H28 per representative, wording and equivalence (module G2S0.OrbitM2v2)
OrbitM2v2 is OrbitM2 with the docstring of `hM2tailRep` reworded as in Step 2 above, and one addition:
```lean
/-- H28 per representative is equivalent to the package's H28 -/
theorem hM2tailRep_iff (N D0 M0 : ℕ) : hM2tailRep N D0 M0 ↔ hM2tail N D0 M0
```

Notes on the follow-up as built (2026-11-27): every statement of this section is proved as written (clean rebuild of the v2 list
scripts/mods_S0_v2.txt, logs/j29_v2_clean.out, 0 error lines; AXIOMS_S0_v2.txt). Helpers: `box5RepCheck_H22` and
`o5RepCheck_final` (the coverage of `box5List` and `o5List ++ L55` by the images of the representatives, by decide),
`box5RepsH22_controls` and `o5Reps_controls` (each representative lies in its list; the representatives lie in distinct orbits),
`hO5_of_rep_gen`, `cycle_adj_at` (the two neighbours of a vertex of a cycle), `cycle_edges_ne`, `fin_succ_ne_pred`.
With these, the final forms T6 `smallN_thm_S0`, T7 `stripIII_thm_S0r` and T8 `fullStrip_thm_S0r` (and `fullStrip_thm_concrete_r`)
take every hypothesis that lists the classes of a record (H22, H25, H26, H27, H28) per representative; the v1 forms
`stripIII_thm_S0`, `fullStrip_thm_S0` and `fullStrip_thm_concrete` remain in TopS0v2. Reflection steps inside the proofs of restated
propositions (Proposition 6.36 within H20 `hD4`) are part of those hypotheses. Theorem 1.1 is stated in the
paper's form for both parts: `cactus_thm_blocks` (nonstrict) and `cactus_strict_thm_blocks` (strict, "two distinct edges of a common
cycle whose couplings are all positive"); `cactus_strict_concrete` takes the paper's data and drops H1, H3 and the positivity of d.
