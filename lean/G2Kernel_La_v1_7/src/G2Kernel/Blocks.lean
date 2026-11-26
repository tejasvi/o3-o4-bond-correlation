/-
G2Kernel.Blocks (module M4): Lemma 2.3 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344), edge-pair form: across a cut
vertex, bond energies are independent, so their covariance vanishes.
Skeleton (step L-a). Not compiled yet.
-/
import G2Kernel.Named

namespace G2Kernel

/-- Statement M4 (Lemma 2.3, edge-pair form): if `V = A ∪ B` with `A ∩ B = {v}` and every edge lies inside
`A` or inside `B`, then an edge inside `A` and an edge inside `B` have zero covariance. Uses hSphereIso. -/
def blocks_statement (N : ℕ) : Prop :=
  hSphereIso N →
  ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (A B : Set V) (v : V), A ∪ B = Set.univ → A ∩ B = {v} →
    (∀ x y, G.Adj x y → (x ∈ A ∧ y ∈ A) ∨ (x ∈ B ∧ y ∈ B)) →
    ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, (∀ x ∈ e, x ∈ A) → (∀ y ∈ f, y ∈ B) →
      gibbsCov N G J (bond e) (bond f) = 0

end G2Kernel
