/-
G2Kernel.Corner (module M5): Lemma 6.2 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344), the corner identity.
Skeleton (step L-a). Not compiled yet.
-/
import G2Kernel.Named

namespace G2Kernel

/-- Statement M5 (Lemma 6.2): at a vertex `v` of degree two, with neighbours `x ≠ y` and equal couplings on
`vx` and `vy`, `Cov(s_{vx}, F) = Cov(s_{vy}, F)` for every bounded measurable `F` that does not depend on
`σ_v`. Uses hSphereIso (the reflection exchanging `σ_x` and `σ_y` is a linear isometry). -/
def corner_statement (N : ℕ) : Prop :=
  hSphereIso N →
  ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (v x y : V), x ≠ y → G.neighborFinset v = {x, y} → J s(v, x) = J s(v, y) →
    ∀ F : Config N V → ℝ, Measurable F → (∃ B, ∀ σ, |F σ| ≤ B) → DependsOnly {w | w ≠ v} F →
      gibbsCov N G J (bond s(v, x)) F = gibbsCov N G J (bond s(v, y)) F

end G2Kernel
