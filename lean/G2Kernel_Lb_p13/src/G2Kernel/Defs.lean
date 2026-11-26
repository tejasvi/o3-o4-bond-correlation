/-
G2Kernel.Defs (module M0): the O(N) model on a finite graph, bond energies, Gibbs expectations,
covariances and the predicate of display (1) of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344).
Skeleton (step L-a, v1_1). Not compiled yet. Statements of later modules are Prop-valued
definitions named `*_statement`. Step L-b proves them as theorems.
-/
import Mathlib

noncomputable section
open MeasureTheory Real

namespace G2Kernel

/-- The ambient space `ℝ^N`. -/
abbrev Amb (N : ℕ) := EuclideanSpace ℝ (Fin N)

/-- The unit sphere `S^{N-1} ⊂ ℝ^N`. -/
abbrev Sph (N : ℕ) := Metric.sphere (0 : Amb N) 1

/-- The rotation-invariant probability measure `ω` on `S^{N-1}`: the cone measure of Lebesgue
measure, divided by its total mass (paper, Section 1.1). -/
def omega (N : ℕ) : Measure (Sph N) :=
  (((volume : Measure (Amb N)).toSphere) Set.univ)⁻¹ • (volume : Measure (Amb N)).toSphere

/-- The scalar product `σ · τ` of two spins. -/
def dot {N : ℕ} (x y : Sph N) : ℝ := @inner ℝ (Amb N) _ (x : Amb N) (y : Amb N)

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Spin configurations `σ : V → S^{N-1}`. -/
abbrev Config (N : ℕ) (V : Type*) := V → Sph N

/-- The product measure `∏_x ω(dσ_x)`. -/
def freeMeasure (N : ℕ) (V : Type*) [Fintype V] : Measure (Config N V) :=
  Measure.pi (fun _ : V => omega N)

/-- The scalar product of the spins at two vertices, `σ_a · σ_b`. -/
def pairDot {N : ℕ} (a b : V) (σ : Config N V) : ℝ := dot (σ a) (σ b)

/-- The bond energy `s_e = σ_x · σ_y` of an edge `e = s(x, y)`. -/
def bond {N : ℕ} (e : Sym2 V) (σ : Config N V) : ℝ :=
  Sym2.lift ⟨fun x y => dot (σ x) (σ y), fun x y => by simp only [dot, real_inner_comm]⟩ e

/-- The exponent `∑_{e ∈ E} J_e s_e` of the Gibbs weight. -/
def energy {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (σ : Config N V) : ℝ :=
  ∑ e ∈ G.edgeFinset, J e * bond e σ

/-- The partition function `Z_{G,J}`. -/
def partition (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) : ℝ :=
  ∫ σ, Real.exp (energy G J σ) ∂(freeMeasure N V)

/-- The Gibbs expectation of an observable. -/
def gibbsExp (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (F : Config N V → ℝ) : ℝ :=
  (∫ σ, F σ * Real.exp (energy G J σ) ∂(freeMeasure N V)) / partition N G J

/-- The Gibbs covariance `Cov_{G,J}(F, H)`. -/
def gibbsCov (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (F H : Config N V → ℝ) : ℝ :=
  gibbsExp N G J (fun σ => F σ * H σ) - gibbsExp N G J F * gibbsExp N G J H

/-- Ferromagnetic couplings: `J_e ≥ 0` on every edge. -/
def Ferro (G : SimpleGraph V) (J : Sym2 V → ℝ) : Prop := ∀ e ∈ G.edgeSet, 0 ≤ J e

/-- The predicate of display (1) for a pair of edges. -/
def G2pair (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : Sym2 V) : Prop :=
  0 ≤ gibbsCov N G J (bond e) (bond f)

/-- The predicate of display (1) for two pairs of vertices. -/
def G2vertices (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (a b c d : V) : Prop :=
  0 ≤ gibbsCov N G J (pairDot a b) (pairDot c d)

/-- Uniform coupling `J` on every edge. -/
def uniform (J : ℝ) : Sym2 V → ℝ := fun _ => J

/-- The grid `P_3 × P_n` on `Fin 3 × Fin n` (row, column): nearest neighbours. -/
def strip (n : ℕ) : SimpleGraph (Fin 3 × Fin n) :=
  SimpleGraph.fromRel fun p q =>
    (p.1 = q.1 ∧ p.2.val + 1 = q.2.val) ∨ (p.2 = q.2 ∧ p.1.val + 1 = q.1.val)

instance (n : ℕ) : DecidableRel (strip n).Adj :=
  fun p q => decidable_of_iff _ (SimpleGraph.fromRel_adj _ p q).symm

/-- The `3 × 3` grid `P_3 × P_3`. -/
abbrev grid33 : SimpleGraph (Fin 3 × Fin 3) := strip 3

end G2Kernel
