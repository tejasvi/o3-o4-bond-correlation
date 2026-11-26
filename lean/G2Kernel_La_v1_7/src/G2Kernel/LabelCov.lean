/-
G2Kernel.LabelCov (module M2): Proposition 2.1 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344).
(a) A bond-energy covariance is a mixed second derivative of log Z.
(b) For a single-label series Z(a, b) = ∑_c u_c k_c(a) k_c(b), that derivative is the covariance of
    r_c(a) = ∂ log k_c(a) and r_c(b) under the label weight.
Skeleton (step L-a). Not compiled yet.
-/
import G2Kernel.Defs
import G2Kernel.Chebyshev

noncomputable section
open MeasureTheory Real

namespace G2Kernel

/-- Statement M2a (Proposition 2.1, first equality): `Cov(s_e, s_f) = ∂_{J_e} ∂_{J_f} log Z`. -/
def covDeriv_statement (N : ℕ) : Prop :=
  ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : Sym2 V), e ∈ G.edgeSet → f ∈ G.edgeSet → e ≠ f →
    deriv (fun a => deriv (fun b =>
        Real.log (partition N G (Function.update (Function.update J e a) f b))) (J f)) (J e)
      = gibbsCov N G J (bond e) (bond f)

/-- Regularity of a single-label series near `(a0, b0)`: nonnegative weights, positive smooth factors, and a
summable bound on the terms and their first two derivatives on a neighbourhood. -/
def LabelRegular (u : ℕ → ℝ) (ka kb : ℕ → ℝ → ℝ) (a0 b0 : ℝ) : Prop :=
  0 < a0 ∧ 0 < b0 ∧ (∀ c, 0 ≤ u c) ∧
  (∀ c, ContDiff ℝ 2 (ka c)) ∧ (∀ c, ContDiff ℝ 2 (kb c)) ∧
  (∀ c x, 0 < x → 0 < ka c x) ∧ (∀ c x, 0 < x → 0 < kb c x) ∧
  ∃ δ : ℝ, 0 < δ ∧ δ < a0 ∧ δ < b0 ∧ ∃ M : ℕ → ℝ, Summable M ∧
    ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      u c * (|ka c x| + |deriv (ka c) x| + |iteratedDeriv 2 (ka c) x|) *
        (|kb c y| + |deriv (kb c) y| + |iteratedDeriv 2 (kb c) y|) ≤ M c

/-- Statement M2b (Proposition 2.1, second equality, single-label case). -/
def labelCov_statement : Prop :=
  ∀ (u : ℕ → ℝ) (ka kb : ℕ → ℝ → ℝ) (a0 b0 : ℝ), LabelRegular u ka kb a0 b0 →
    0 < ∑' c, u c * ka c a0 * kb c b0 →
    deriv (fun a => deriv (fun b => Real.log (∑' c, u c * ka c a * kb c b)) b0) a0
      = covW (fun c => u c * ka c a0 * kb c b0 / ∑' c', u c' * ka c' a0 * kb c' b0)
          (fun c => deriv (ka c) a0 / ka c a0) (fun c => deriv (kb c) b0 / kb c b0)

end G2Kernel
