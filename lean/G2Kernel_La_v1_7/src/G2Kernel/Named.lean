/-
G2Kernel.Named: the named hypotheses of the kernel track. Each is a `Prop` that states one claim of
the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344) (each docstring gives the number of the result). None is an axiom. A top-level statement lists
the named hypotheses it uses as explicit premises. STATEMENTS.md cross-references every one of them.
The hypotheses for the strip part of Theorem 1.4(ii), including hWeak, are in NamedStrip.lean.
Skeleton (step L-a, v1_2). Not compiled yet.
-/
import G2Kernel.Defs
import G2Kernel.Ledger

noncomputable section
open MeasureTheory Real

namespace G2Kernel

/-! ### Analytic inputs (cited in the paper) -/

/-- **hFH** (Section 2.1, display (3) and display (2)). Abstract data: `k ℓ J` are the coefficients
`k_ℓ(J)`, `d ℓ = dim H_ℓ`, and `C ℓ` is the normalized Gegenbauer polynomial `C̃_ℓ`, with
`Π_ℓ(σ, σ') = d ℓ * C ℓ (σ · σ')`. The conjuncts: the expansion of `e^{Jt}`; `C̃_ℓ(1) = 1`; the dimensions
are nonnegative and grow at most like `(ℓ+1)^N`; and the projection identity (2). -/
def hFH (N : ℕ) (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ) : Prop :=
  (∀ J t : ℝ, t ∈ Set.Icc (-1 : ℝ) 1 → HasSum (fun ℓ => k ℓ J * (d ℓ * C ℓ t)) (Real.exp (J * t))) ∧
  (∀ ℓ, C ℓ 1 = 1) ∧
  (∀ ℓ, 0 ≤ d ℓ ∧ d ℓ ≤ ((ℓ : ℝ) + 1) ^ N) ∧
  (∀ (a b : ℕ) (x y : Sph N),
     ∫ z, (d a * C a (dot x z)) * (d b * C b (dot z y)) ∂(omega N)
       = if a = b then d a * C a (dot x y) else 0)

/-- **hKReg** (Section 2.1, after (3)): for `J > 0` every `k_ℓ(J)` is positive; each `k_ℓ` is twice
continuously differentiable; and on each compact subinterval of `(0, ∞)` the coefficient and its first two
derivatives are bounded by `c (ℓ+1)^j (J/2)^ℓ / ℓ!`. -/
def hKReg (k : ℕ → ℝ → ℝ) : Prop :=
  (∀ ℓ J, 0 < J → 0 < k ℓ J) ∧
  (∀ ℓ, ContDiff ℝ 2 (k ℓ)) ∧
  (∀ a b : ℝ, 0 < a → a ≤ b → ∃ c : ℝ, 0 < c ∧ ∀ ℓ : ℕ, ∀ J ∈ Set.Icc a b,
     |k ℓ J| ≤ c * (J / 2) ^ ℓ / (ℓ.factorial : ℝ) ∧
     |deriv (k ℓ) J| ≤ c * ((ℓ : ℝ) + 1) * (J / 2) ^ ℓ / (ℓ.factorial : ℝ) ∧
     |iteratedDeriv 2 (k ℓ) J| ≤ c * ((ℓ : ℝ) + 1) ^ 2 * (J / 2) ^ ℓ / (ℓ.factorial : ℝ))

/-- **hRatio** (Lemma 2.2, which the paper derives from [Am74, (16)] and [RS16, Thm 2]):
for every `J > 0`, `ℓ ↦ r_ℓ(J) = ∂_J log k_ℓ(J)` is strictly increasing. -/
def hRatio (k : ℕ → ℝ → ℝ) : Prop :=
  ∀ J : ℝ, 0 < J → StrictMono (fun ℓ : ℕ => deriv (k ℓ) J / k ℓ J)

/-- **hCycleZ** (Section 3.1, the formula for `Z_C`, the classical solution of the ring [St69]): on the
cycle `C_n`, `Z = ∑_c d_c ∏_{g} k_c(J_g)`. For the paper's data it follows from (3) and (2) by integrating
the projections around the cycle; for abstract data this needs, besides hFH, the bound `|C ℓ t| ≤ 1` on `[-1, 1]`
and a locally uniform bound on `|k ℓ J|`, so it is kept as a named hypothesis. -/
def hCycleZ (N : ℕ) (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) : Prop :=
  ∀ (n : ℕ) [DecidableRel (SimpleGraph.cycleGraph n).Adj], 3 ≤ n → ∀ J : Sym2 (Fin n) → ℝ,
    HasSum (fun c => d c * ∏ e ∈ (SimpleGraph.cycleGraph n).edgeFinset, k c (J e))
      (partition N (SimpleGraph.cycleGraph n) J)

/-- **hShared** (Theorem 3.2, edge-pair case; from [Du76, Thm 2, (3.1)] at `N = 3` and
[Du76, Thm 1, (2.14)] with Lemma 3.3 at `N = 4`): on every finite graph with ferromagnetic
couplings, two edges with a common vertex have nonnegative covariance. -/
def hShared (N : ℕ) : Prop :=
  ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ),
    Ferro G J → ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → (∃ v, v ∈ e ∧ v ∈ f) → G2pair N G J e f

/-- One-sided observables: `F` depends only on the spins in `H`. -/
def DependsOnly {N : ℕ} {V : Type*} (H : Set V) (F : Config N V → ℝ) : Prop :=
  ∀ σ σ' : Config N V, (∀ v ∈ H, σ v = σ' v) → F σ = F σ'

/-- The closed halves of `P_3 × P_3` that contain `b_0`: rows 1–2 for the reflection in the horizontal
middle line through `W, C, E` (`reflH`), and the side `i + j ≥ 2` of the diagonal through `NE, C, SW`
(`reflAnti`), which contains `S` and `SE`. These are the side reflection and the diagonal reflection of
the proof of Proposition 6.7, to which Lemma 6.1 is applied. -/
def halfH : Set (Fin 3 × Fin 3) := {p | 1 ≤ p.1.val}
def halfAnti : Set (Fin 3 × Fin 3) := {p | 2 ≤ p.1.val + p.2.val}

/-- **hRPGibbs** (Lemma 6.1, first part: reflection positivity [FILS78]) for the two
reflections of `P_3 × P_3` that the proof of Proposition 6.7 uses, at uniform coupling `J ≥ 0`. -/
def hRPGibbs (N : ℕ) : Prop :=
  ∀ J : ℝ, 0 ≤ J → ∀ F : Config N (Fin 3 × Fin 3) → ℝ, Measurable F → (∃ B, ∀ σ, |F σ| ≤ B) →
    (DependsOnly halfH F → 0 ≤ gibbsExp N grid33 (uniform J) (fun σ => F σ * F (σ ∘ reflH))) ∧
    (DependsOnly halfAnti F → 0 ≤ gibbsExp N grid33 (uniform J) (fun σ => F σ * F (σ ∘ reflAnti)))

/-- **hSphereIso** (Section 1.1: `ω` is the rotation-invariant probability measure): every linear isometry
of `ℝ^N` preserves `ω`. The kernel uses it for Lemma 2.3, Lemma 6.2 and the case `J = 0` of Theorem 6.34(a).
It is expected to follow from Mathlib (`Measure.toSphere` and the isometry invariance of `volume`); it is
used as a named hypothesis only if that proof is not completed. -/
def hSphereIso (N : ℕ) : Prop :=
  ∀ A : Amb N ≃ₗᵢ[ℝ] Amb N,
    MeasurePreserving (fun x : Sph N => (⟨A (x : Amb N), by simp⟩ : Sph N))
      (omega N) (omega N)

/-! ### Certified computations (steps marked † in the paper) -/

/-- Upper ends of the certified strip covers (Theorem 6.6): `20.064` at `N = 4`, `20.070` at `N = 3`. -/
def stripTop (N : ℕ) : ℝ := if N = 4 then 20064 / 1000 else 20070 / 1000

/-- **hHub** (Theorem 6.9, †; kind: certificate plus paper proof, namely Lemma 6.8
and the equivalence of `Cov > 0` with `N_τ > 0`): on `P_3 × P_3`, `Cov(s_{b_0}, s_{s_N}) > 0` for every
`J ∈ [20, 100.68]`. -/
def hHub (N : ℕ) : Prop :=
  ∀ J : ℝ, 20 ≤ J → J ≤ 10068 / 100 → 0 < gibbsCov N grid33 (uniform J) (bond b0) (bond sN)

/-- **hLBu** (Lemma 6.10, †; kind: certificate plus paper proof, namely the remainder bounds of
Lemma 6.10): `J^2 Cov(s_{b_0}, s_{s_N}) ≥ 2.24·10^{-4}` for `J ≥ 80` at `N = 3`, and `≥ 4.63·10^{-4}` for `J ≥ 100`
at `N = 4`. -/
def hLBu (N : ℕ) : Prop :=
  (N = 3 → ∀ J : ℝ, 80 ≤ J → 224 / 1000000 ≤ J ^ 2 * gibbsCov N grid33 (uniform J) (bond b0) (bond sN)) ∧
  (N = 4 → ∀ J : ℝ, 100 ≤ J → 463 / 1000000 ≤ J ^ 2 * gibbsCov N grid33 (uniform J) (bond b0) (bond sN))

end G2Kernel
