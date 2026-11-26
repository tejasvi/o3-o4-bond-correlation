/-
G2Kernel.TheoremB (module M11, outline): Theorem 1.2 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344) for N = 4.
Step L-a states only the polynomial input formally (Malo's theorem, Lemma 4.5). The objects that the other
inputs need (the label weights W(ℓ) of Section 2.2, two-terminal kernels K_H, the Jacobi matrix X of μ_N,
generalized theta graphs and outerplanar strips) are not defined yet. Their statements follow after the audit
of M0–M10. Planned named hypotheses for this module:
  hSU2  — Lemma 4.1: W(ℓ) ≥ 0 for every graph and labelling at N = 4;
  hKM   — fact (K1) of Section 4.3: K ∈ 𝒦 ⟹ K(X) totally nonnegative (Karlin–McGregor);
  hLin  — nonnegative linearization coefficients of Gegenbauer polynomials (Remark 3.1).
Planned kernel statements: Lemma 4.2 via FKG on finite truncations,
Lemma 4.3, Lemmas 4.6–4.7, Lemma 4.9, Theorems 4.8 and
4.10, and the assembly of Theorem 1.2.
Skeleton (step L-a). Not compiled yet.
-/
import G2Kernel.Defs

open Polynomial

namespace G2Kernel

/-- A nonzero real polynomial has only real zeros. -/
def RealRooted (p : ℝ[X]) : Prop :=
  ∀ z : ℂ, (p.map (algebraMap ℝ ℂ)).eval z = 0 → z.im = 0

/-- The Hadamard (coefficientwise) product of two real polynomials. -/
noncomputable def hadamard (p q : ℝ[X]) : ℝ[X] :=
  ∑ i ∈ Finset.range (min p.natDegree q.natDegree + 1), monomial i (p.coeff i * q.coeff i)

/-- **hMalo** (Lemma 4.5; [Ma95], see [CC04]): if `f` has only real zeros and `g` has only
real zeros, all in `(-∞, 0]` or all in `[0, ∞)`, then the Hadamard product is zero or has only real zeros. -/
def hMalo : Prop :=
  ∀ f g : ℝ[X], f ≠ 0 → g ≠ 0 → RealRooted f → RealRooted g →
    ((∀ z : ℂ, (g.map (algebraMap ℝ ℂ)).eval z = 0 → z.re ≤ 0) ∨
     (∀ z : ℂ, (g.map (algebraMap ℝ ℂ)).eval z = 0 → 0 ≤ z.re)) →
    hadamard f g = 0 ∨ RealRooted (hadamard f g)

end G2Kernel
