/-
G2Kernel.Chebyshev (module M1): Chebyshev's sum inequality for a probability weight on ℕ, the step used in
the proofs of Lemma 2.4 and Theorem 1.1 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344).
Skeleton (step L-a, v1_1). Not compiled yet.
-/
import G2Kernel.Defs

namespace G2Kernel

/-- Covariance of `f` and `g` under the weight `p` on ℕ. -/
noncomputable def covW (p f g : ℕ → ℝ) : ℝ :=
  (∑' n, p n * (f n * g n)) - (∑' n, p n * f n) * (∑' n, p n * g n)

/-- Statement M1: under a probability weight, two nondecreasing functions with summable `p f`, `p g` and
`p f g` are nonnegatively correlated. -/
def chebyshev_statement : Prop :=
  ∀ p f g : ℕ → ℝ, (∀ n, 0 ≤ p n) → HasSum p 1 → Monotone f → Monotone g →
    Summable (fun n => p n * f n) → Summable (fun n => p n * g n) → Summable (fun n => p n * (f n * g n)) →
    0 ≤ covW p f g

/-- Statement M1': strictly increasing functions under a weight that charges every point are strictly
positively correlated (the strict part of Theorem 1.1). -/
def chebyshev_strict_statement : Prop :=
  ∀ p f g : ℕ → ℝ, (∀ n, 0 < p n) → HasSum p 1 → StrictMono f → StrictMono g →
    Summable (fun n => p n * f n) → Summable (fun n => p n * g n) → Summable (fun n => p n * (f n * g n)) →
    0 < covW p f g

end G2Kernel
