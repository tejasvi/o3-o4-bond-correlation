# STATEMENTS_H16_public: the statements of stage H16 (G2S1.Ladder, G2S1.TopH16b) and of G2S1.TopMergeH16 (H16 merged
# into the S3 top forms), as they were written during the work: STATEMENTS_H16_v1.md, its successor STATEMENTS_H16_v2.md
# (which withdraws the two auxiliary exports of v1 section 3; their module is not in this folder) and part B of
# STATEMENTS_A2B_v1.md. Lines naming the working teams or their folders are reworded; nothing else is changed.
# Every Lean statement in this file is about finite simple graphs (Mathlib's SimpleGraph); the paper's Theorems 1.1 and
# 1.2(b) also cover parallel edges through its Section 3.3 reduction, which is not formalized.

# STATEMENTS_H16_v1: H16 (hLadder N, the ladder P_3 x P_2) at N = 3 and N = 4, with two auxiliary exports

2026-11-27. Written before the proofs, on the plan PLAN_H16_v1.md (sha8 3e5ca1d2; v2 bb808ee4 noted).
Paper: "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344).

## 1. The named hypothesis, unchanged (package G2Kernel_Lb_p13, G2Kernel/Strip300.lean l.42)
```lean
def hLadder (N : ℕ) : Prop :=
  ∀ J : ℝ, 0 ≤ J → ∀ e ∈ (strip 2).edgeSet, ∀ f ∈ (strip 2).edgeSet, e ≠ f → G2pair N (strip 2) (uniform J) e f
```
Paper fact: Theorem 1.2(a) at N = 4 and Theorem 1.3 at N = 3, restricted to the graph P_3 x P_2 at uniform coupling
J ≥ 0: every pair of distinct edges has nonnegative covariance of the bond energies (display (1)).
`strip`, `uniform`, `G2pair`, `gibbsCov`, `bond` are the package's definitions (G2Kernel/Defs.lean), used unchanged.

## 2. Main theorems (module G2S1/Ladder.lean, namespace G2Kernel)
```lean
theorem hLadder_holds3 : hLadder 3
theorem hLadder_holds4 : hLadder 4
```
Route (not the paper's proofs of Theorems 1.2(a) and 1.3): Theorem 3.2 for two edges with a common vertex (H6, S3's
`G2S3.hShared_holds3`, `G2S3.hShared_holds4`, sha256-verified unedited copies), Lemma 6.2 (the corner identity, the
package's `corner_step`, the strip form of `corner_thm`), and Section 1.1 (rotation invariance of ω, S0's
`hSphereIso_holds`). At uniform J, each of the 11 pairs of disjoint edges moves in one or two corner steps to a pair with
a common vertex with the same covariance; the 10 pairs with a common vertex are H6 directly.

## 3. Auxiliary exports (module G2S1/Deg2Swap.lean, namespace G2Kernel)
```lean
theorem partition_swap_deg2 {N : ℕ} (hN : 1 ≤ N) {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] {x y z : V} (hxy : x ≠ y) (hxz : G.Adj x z) (hzy : G.Adj z y)
    (hdeg : ∀ e ∈ G.edgeSet, z ∈ e → e = s(x, z) ∨ e = s(z, y)) (J : Sym2 V → ℝ) :
    partition N G (fun g => J (Equiv.swap s(x, z) s(z, y) g)) = partition N G J
theorem gibbsCov_swap_deg2 {N : ℕ} (hN : 1 ≤ N) {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] {x y z : V} (hxy : x ≠ y) (hxz : G.Adj x z) (hzy : G.Adj z y)
    (hdeg : ∀ e ∈ G.edgeSet, z ∈ e → e = s(x, z) ∨ e = s(z, y)) (J : Sym2 V → ℝ) (hJ : J s(x, z) = J s(z, y))
    {f : Sym2 V} (hf : f ∈ G.edgeSet) (hf1 : f ≠ s(x, z)) (hf2 : f ≠ s(z, y)) :
    gibbsCov N G J (bond s(x, z)) (bond f) = gibbsCov N G J (bond s(z, y)) (bond f)
```
Paper facts:
- `gibbsCov_swap_deg2` is Lemma 6.2 (corner identity) for F = s_f, with the degree-2 neighbourhood of z written out
  (z lies on no edge other than s(x,z), s(z,y)). Proof: the package's `corner_thm` with `hSphereIso_holds`.
- `partition_swap_deg2`: at a vertex of degree 2, exchanging the couplings of its two edges leaves Z_{G,J} unchanged,
  for every J (no equality of couplings needed). Not a numbered statement of the paper; it is the reflection argument
  of the proof of Lemma 6.2 applied to Z (integrate σ_z first; the reflection exchanging σ_x and σ_y preserves ω).
Status (2026-11-27): the ladder needs neither export; kept as planned unless
withdrawn (v2 withdraws them). Statements as in PLAN_H16_v1 §3, unchanged.

## 4. Dependencies (read-only)
- Package G2Kernel (s0/build/Lb) and StripIII (s0/build/S3, needed by S3's RPInst `import StripIII.Statement`).
- S0: G2S0/SphereIso.lean (copy in s1/src/G2S0, byte-identical to s0/src/G2S0).
- S3: the 15-module chain RPCore ... Dunlop, copied unedited into s1/src/G2S3; list with full sha256 in S3_COPIES_v1.txt.
- Not used: S1 and S2 modules (no S1/S2 import in G2S1/Ladder or G2S1/Deg2Swap).

## 5. Source hashes of the cited package statements (computed 2026-11-27T12:32:31Z)
- 6b48ad4858d32985 s0/pkg/G2Kernel_Lb_p13/src/G2Kernel/Strip300.lean
- 48ae79e3e239a163 s0/pkg/G2Kernel_Lb_p13/src/G2Kernel/Defs.lean
- 154610c7fb6b5374 s0/pkg/G2Kernel_Lb_p13/src/G2Kernel/Named.lean
- 6be7873f0adab5fa s0/pkg/G2Kernel_Lb_p13/src/G2Kernel/Corner.lean
- 7b51ccc0965d874c s0/pkg/G2Kernel_Lb_p13/src/G2Kernel/Proofs/CornerProof.lean
- 37a7f0ccc34b7ccb s0/pkg/G2Kernel_Lb_p13/src/G2Kernel/Proofs/AssemblyProof.lean
- 6521a1f03ce6340f s0/src/G2S0/SphereIso.lean
- f81d36d853646ea7 s3/src/G2S3/Dunlop.lean

---

# STATEMENTS_H16_v2 (successor of STATEMENTS_H16_v1.md, sha8 d96e7f25, unchanged)

Written 2026-11-27T12:45:35Z, on the decision "Drop both auxiliary exports".

## Change
- **Withdrawn:** the two auxiliary statements of v1 §3, `partition_swap_deg2` and `gibbsCov_swap_deg2`. The package's
  `corner_thm` (Lemma 6.2) and its strip form `corner_step` already carry the swap. They are not part of the H16
  deliverable and not in its module list. Both had been proved in src/G2S1/Deg2Swap.lean (sha8 4bbdf7ee) before the order
  arrived; that file stays on disk unused (no rm). No H16 module imports it.
- **Unchanged:** the main theorems of v1 §2, with identical statement text:
```lean
theorem hLadder_holds3 : hLadder 3
theorem hLadder_holds4 : hLadder 4
```
  Here `hLadder` is the package's definition (G2Kernel/Strip300.lean l.42), unchanged (quoted in v1 §1). Paper fact: Theorem 1.2(a)
  at N = 4 and Theorem 1.3 at N = 3, on P_3 x P_2 at uniform coupling J >= 0.
- **Route unchanged.** Ingredients:
  - H6 (S3's `G2S3.hShared_holds3/4`, copies per S3_COPIES_v1.txt);
  - the package's `corner_step` (Lemma 6.2);
  - S0's `hSphereIso_holds`;
  - the 11 reductions of disjoint pairs.
  The proof is src/G2S1/Ladder.lean (sha8 a0dcedf4 (audited as db2384c3; only comment lines differ, see FROZEN_TO_SHIPPED_S3.tsv)). It never used the exports and is unchanged.
- **Audit scope:** hLadder_holds3/4 only.

## Module list (new): scripts/mods_h16_v2.txt
G2S0/SphereIso, the 15 S3 copies (RPCore ... Dunlop), G2S1/Ladder, G2S1/TopH16b.
The 24 modules of scripts/mods_S1_final.txt (sha8 bb381e73) are frozen for the v3 release. None of them and not the list
is edited. G2S0/SphereIso, one of the 24, is compiled from its unchanged source into the H16 tree only.

---

# STATEMENTS_A2B_v1: list cuts by Lemma 6.2 (A2) and the H16 merge of the top theorems (B), stated before the proofs
(Only part B, the statements of G2S1.TopMergeH16, is given here; part A2 and its modules are not in this folder.)

## B. H16 merged into S3's top forms (module G2S1/TopMergeH16, namespace G2S1, `open G2Kernel G2Kernel.StripIII`)
Each statement is S3's Part D form (s3/src/G2S3/Top.lean, TopIII.lean; read-only copies) with the one premise `hLadder N`
removed; every other premise is verbatim, in the same order, and the conclusion is verbatim. T3 and T4 have no hLadder premise
and are unchanged. Proofs: the S3 theorem applied with `hLadder_of34 hN` (from hLadder_holds3/4).
```lean
theorem hLadder_of34 {N : ℕ} (hN : N = 3 ∨ N = 4) : hLadder N
theorem strip300_thm_H16 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
    hHub N → hLBu N → hRHCover N →
      (∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f) ∧
      (∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
          0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f))
def smallN_statement_H16 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hBoxAll5rep N StripIII.box5Reps →
    ∀ n : ℕ, 1 ≤ n → n ≤ 5 → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f
theorem smallN_thm_H16 (N : ℕ) : smallN_statement_H16 N
def stripIII_statement_H16 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f
theorem stripIII_thm_H16 (N : ℕ) : stripIII_statement_H16 N
def fullStrip_statement_H16 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps → hBoxAll5rep N StripIII.box5Reps → hM1rep N StripIII.m1List StripIII.NMAX_M1 →
  hM2tailRep N StripIII.D0_M2 StripIII.M0_M2 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f
theorem fullStrip_thm_H16 (N : ℕ) : fullStrip_statement_H16 N
```
Controls: `smallN_statement_H16 N → G2S3.smallN_statement_S3 N`, and the same for stripIII and fullStrip. These are proved by
dropping the hLadder argument, so each new form implies S3's form. The B forms become final only after the S3 + H16 audit and
the merge decision.
