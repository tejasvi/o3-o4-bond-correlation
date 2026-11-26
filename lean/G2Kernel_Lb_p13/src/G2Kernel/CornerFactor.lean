/-
G2Kernel.CornerFactor (modules M1v, M10c and M10d): the corner pairs of Theorem 1.4(ii) of
the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344) through the law of the common label of Lemma 2.4, on the strict-variance route.
At a corner of P_3 × P_n the two edges e, f carry the same coupling J, so Proposition 2.1 turns Cov(s_e, s_f) into
the variance of r_c(J) = ∂_J log k_c(J) under the law of the common label c. That variance is positive as soon as the
law charges two labels at which r_c(J) differs, and by Lemma 2.2 (hRatio) the labels 0 and 1 suffice. No label
needs to carry positive weight beyond these two.
Skeleton (step L-a, v1_5). Not compiled yet.
-/
import G2Kernel.NamedStrip
import G2Kernel.Chebyshev

noncomputable section

namespace G2Kernel

/-- Statement M1v (strict variance): under a probability weight on ℕ, a function with summable `p f` and `p f²`
that takes different values at two charged points has positive variance. -/
def variance_pos_statement : Prop :=
  ∀ p f : ℕ → ℝ, (∀ n, 0 ≤ p n) → HasSum p 1 →
    Summable (fun n => p n * f n) → Summable (fun n => p n * (f n * f n)) →
    (∃ m n, 0 < p m ∧ 0 < p n ∧ f m ≠ f n) → 0 < covW p f f

/-- **hCornerFactor** (kind: paper proof; Lemma 2.4 for the two edges at a corner, with a nonnegative law of the
common label). For `n ≥ 3` and uniform coupling `J > 0`, the partition function of `P_3 × P_n`, as a function of the
two couplings at one corner, is a single-label series `∑_c u_c k_c(a) k_c(b)` with nonnegative, polynomially bounded
weights `u_c` that do not depend on `(a, b)`, and the labels 0 and 1 carry positive weight.
Backing at `N = 3`: Proposition 3 and Lemma 2 of NOTE_LEMMA24_N3_v1 (sha8 611f3dbb; confirmed with fixes by the review,
sha8 08fb60e5), with `A = {v}`, `α_c = 1` and `u_c = (2c + 1) ρ_c(κ_{G - v})`; `u_0, u_1 > 0` because `G - v` joins the
two neighbours of the corner by a path with positive couplings; the bound `|ρ_c| ≤ sup κ` (note, Section 1) gives
`K = 1`. Backing at `N = 4`: the label expansion of Section 2.2 with `W ≥ 0` (Lemma 4.1); `u_0 > 0` from the zero
labelling and `u_1 > 0` from the labelling with label 1 on the 4-cycle through the corner; the bound
`|W(ℓ)| ≤ ∏_e d_{ℓ_e}` of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344) (after display (4)) gives `K = 4`. -/
def hCornerFactor (N : ℕ) (k : ℕ → ℝ → ℝ) : Prop :=
  ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 0 < J →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → seriesCorner n e f →
      ∃ (u : ℕ → ℝ) (K : ℕ) (U : ℝ), (∀ c, 0 ≤ u c) ∧ 0 < u 0 ∧ 0 < u 1 ∧
        (∀ c : ℕ, u c ≤ ((c : ℝ) + 1) ^ K * U) ∧
        ∀ a b : ℝ, partition N (strip n) (Function.update (Function.update (uniform J) e a) f b)
          = ∑' c, u c * k c a * k c b

/-- Statement M10c (the corner step of Theorem 6.4): hCornerFactor, with hKReg and hRatio for the same
coefficients `k`, gives hCornerPair. -/
def cornerPair_statement (N : ℕ) : Prop :=
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k → hCornerPair N

/-- Statement M10d (Theorem 1.4(ii) without the restatement hCornerPair): `stripD_statement` with hCornerFactor,
hKReg and hRatio in place of hCornerPair. -/
def stripD_factor_statement (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hStripSpecial N →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
    ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 20 →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f →
        0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)

end G2Kernel
