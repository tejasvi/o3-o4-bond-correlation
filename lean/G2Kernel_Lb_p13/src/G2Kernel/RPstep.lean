/-
G2Kernel.RPstep (module M6): Lemma 6.1 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344).
(a) The abstract step: reflection positivity on a class closed under adding constants gives Cov(F, F∘θ) ≥ 0.
(b) Its instance on P_3 × P_3 for the two mirror pairs used in Proposition 6.7, from hRPGibbs.
Skeleton (step L-a). Not compiled yet.
-/
import G2Kernel.Named

noncomputable section
open MeasureTheory

namespace G2Kernel

/-- Statement M6a (abstract step of Lemma 6.1). -/
def rpCov_statement : Prop :=
  ∀ (Ω : Type) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ] (θ : Ω → Ω),
    MeasurePreserving θ μ μ → (∀ ω, θ (θ ω) = ω) →
    ∀ 𝒜 : Set (Ω → ℝ), (∀ F ∈ 𝒜, ∀ c : ℝ, (fun ω => F ω - c) ∈ 𝒜) →
      (∀ F ∈ 𝒜, 0 ≤ ∫ ω, F ω * F (θ ω) ∂μ) →
      ∀ F ∈ 𝒜, Measurable F → (∃ B, ∀ ω, |F ω| ≤ B) →
        0 ≤ (∫ ω, F ω * F (θ ω) ∂μ) - (∫ ω, F ω ∂μ) * (∫ ω, F (θ ω) ∂μ)

/-- Statement M6b (Lemma 6.1 for the mirror pairs `(b_0, b_3)` and `(b_0, b_5)` of `P_3 × P_3` at uniform
coupling): uses hRPGibbs. -/
def mirror33_statement (N : ℕ) : Prop :=
  hRPGibbs N → ∀ J : ℝ, 0 ≤ J → G2pair N grid33 (uniform J) b0 b3 ∧ G2pair N grid33 (uniform J) b0 b5

end G2Kernel
