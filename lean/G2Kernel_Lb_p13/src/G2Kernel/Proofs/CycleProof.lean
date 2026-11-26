/-
G2Kernel.Proofs.CycleProof: proofs of `cycleG2_statement` and `cycleG2_strict_statement` (module M3,
Theorem 1.1 on one cycle). Kernel proof, step L-b.
For couplings positive on every edge, hCycleZ writes the partition function of the updated couplings as the label
series Σ_c u_c k_c(a) k_c(b) with u_c = d_c Π_{g ≠ e, f} k_c(J_g) ≥ 0, and hKReg gives the bounds of
`LabelRegular`; covDeriv and labelCov turn the covariance into `covW`, and hRatio with Chebyshev's inequality
gives its sign (strict when every d_c > 0). For couplings ≥ 0 the covariance at J is the limit of those at
J + ε, which are continuous in ε (`hasDerivAt_expInt`). For N = 0 the covariance is 0, and the strict
hypotheses are contradictory (hCycleZ would give a positive sum equal to Z = 0).
-/
import G2Kernel.Cycle
import G2Kernel.Proofs.LabelCovProof
import G2Kernel.Proofs.ChebyshevProof

noncomputable section
open MeasureTheory Real Filter Topology

namespace G2Kernel

/-! ### Summability and coefficient bounds -/

theorem summable_poly_pow_div_factorial (K : ℕ) {y : ℝ} (hy : 0 ≤ y) :
    Summable (fun c : ℕ => ((c : ℝ) + 1) ^ K * y ^ c / (c.factorial : ℝ)) := by
  refine Summable.of_nonneg_of_le (fun c => by positivity) (fun c => ?_)
    (Real.summable_pow_div_factorial ((2 : ℝ) ^ K * y))
  have h1 : c < 2 ^ c := Nat.lt_two_pow_self
  have h1' : c + 1 ≤ 2 ^ c := h1
  have h2 : ((c : ℝ) + 1) ≤ (2 : ℝ) ^ c := by exact_mod_cast h1'
  have h3 : ((c : ℝ) + 1) ^ K ≤ ((2 : ℝ) ^ K) ^ c := by
    calc ((c : ℝ) + 1) ^ K ≤ ((2 : ℝ) ^ c) ^ K := pow_le_pow_left₀ (by positivity) h2 K
      _ = ((2 : ℝ) ^ K) ^ c := by rw [← pow_mul, ← pow_mul, mul_comm]
  have hc : (0 : ℝ) < c.factorial := by exact_mod_cast c.factorial_pos
  rw [mul_pow]
  exact div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_right h3 (pow_nonneg hy c)) hc.le

theorem abs_le_three_left (a b d : ℝ) : |a| ≤ |a| + |b| + |d| := by
  have := abs_nonneg b
  have := abs_nonneg d
  linarith

theorem abs_le_three_mid (a b d : ℝ) : |b| ≤ |a| + |b| + |d| := by
  have := abs_nonneg a
  have := abs_nonneg d
  linarith

/-- The bounds of hKReg on `[lo, hi]`, summed over the coefficient and its first two derivatives. -/
theorem kreg_sum_bound {k : ℕ → ℝ → ℝ} (hK : hKReg k) {lo hi : ℝ} (hlo : 0 < lo) (hle : lo ≤ hi) :
    ∃ c : ℝ, 0 < c ∧ ∀ ℓ : ℕ, ∀ J ∈ Set.Icc lo hi,
      |k ℓ J| + |deriv (k ℓ) J| + |iteratedDeriv 2 (k ℓ) J|
        ≤ 3 * c * (((ℓ : ℝ) + 1) ^ 2 * ((hi / 2) ^ ℓ / (ℓ.factorial : ℝ))) := by
  obtain ⟨c, hc, hb⟩ := hK.2.2 lo hi hlo hle
  refine ⟨c, hc, fun ℓ J hJ => ?_⟩
  obtain ⟨h0, h1, h2⟩ := hb ℓ J hJ
  have hJ0 : 0 ≤ J := le_trans hlo.le hJ.1
  have hF : (0 : ℝ) < ℓ.factorial := by exact_mod_cast ℓ.factorial_pos
  have hL : (1 : ℝ) ≤ (ℓ : ℝ) + 1 := by
    have := (Nat.cast_nonneg ℓ : (0 : ℝ) ≤ ℓ)
    linarith
  have hw : (J / 2) ^ ℓ / (ℓ.factorial : ℝ) ≤ (hi / 2) ^ ℓ / (ℓ.factorial : ℝ) :=
    div_le_div_of_nonneg_right (pow_le_pow_left₀ (by positivity) (by linarith [hJ.2]) ℓ) hF.le
  have hw0 : 0 ≤ (J / 2) ^ ℓ / (ℓ.factorial : ℝ) := by positivity
  rw [mul_div_assoc] at h0 h1 h2
  obtain ⟨w, hwd⟩ : ∃ w, w = (J / 2) ^ ℓ / (ℓ.factorial : ℝ) := ⟨_, rfl⟩
  obtain ⟨W, hWd⟩ : ∃ W, W = (hi / 2) ^ ℓ / (ℓ.factorial : ℝ) := ⟨_, rfl⟩
  obtain ⟨L, hLd⟩ : ∃ L, L = (ℓ : ℝ) + 1 := ⟨_, rfl⟩
  rw [← hwd] at h0 h1 h2 hw hw0
  rw [← hWd] at hw ⊢
  rw [← hLd] at h1 h2 hL ⊢
  have hW0 : 0 ≤ W := le_trans hw0 hw
  have hL2 : 1 ≤ L ^ 2 := by nlinarith
  have hLL : L ≤ L ^ 2 := by nlinarith
  have k1 : c * w ≤ c * (L ^ 2 * W) :=
    mul_le_mul_of_nonneg_left (le_trans hw (le_mul_of_one_le_left hW0 hL2)) hc.le
  have k2 : c * L * w ≤ c * (L ^ 2 * W) := by
    rw [mul_assoc]
    exact mul_le_mul_of_nonneg_left (mul_le_mul hLL hw hw0 (by positivity)) hc.le
  have k3 : c * L ^ 2 * w ≤ c * (L ^ 2 * W) := by
    rw [mul_assoc]
    exact mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hw (by positivity)) hc.le
  linarith

/-- A finite product of coefficients at positive couplings is bounded uniformly in the label. -/
theorem prod_k_bounded {k : ℕ → ℝ → ℝ} (hK : hKReg k) {ι : Type*} (s : Finset ι) (x : ι → ℝ)
    (hx : ∀ g ∈ s, 0 < x g) : ∃ U : ℝ, ∀ ℓ : ℕ, |∏ g ∈ s, k ℓ (x g)| ≤ U := by
  have hex : ∀ g, ∃ B : ℝ, 0 ≤ B ∧ ∀ ℓ : ℕ, g ∈ s → |k ℓ (x g)| ≤ B := by
    intro g
    by_cases hg : g ∈ s
    · obtain ⟨c, hc, hb⟩ := hK.2.2 (x g) (x g) (hx g hg) le_rfl
      refine ⟨c * Real.exp (x g / 2), (mul_pos hc (Real.exp_pos _)).le, fun ℓ _ => ?_⟩
      have h1 := (hb ℓ (x g) ⟨le_rfl, le_rfl⟩).1
      have h2 : (x g / 2) ^ ℓ / (ℓ.factorial : ℝ) ≤ Real.exp (x g / 2) :=
        Real.pow_div_factorial_le_exp (x g / 2) (by linarith [hx g hg]) ℓ
      rw [mul_div_assoc] at h1
      exact h1.trans (mul_le_mul_of_nonneg_left h2 hc.le)
    · exact ⟨0, le_rfl, fun ℓ h => absurd h hg⟩
  choose B _hB0 hB using hex
  refine ⟨∏ g ∈ s, B g, fun ℓ => ?_⟩
  rw [Finset.abs_prod]
  exact Finset.prod_le_prod₀ (fun g _ => abs_nonneg _) (fun g hg => hB g ℓ hg)

/-- `LabelRegular` from a polynomial bound on the weights. -/
theorem labelRegular_of_bounds {u : ℕ → ℝ} {k : ℕ → ℝ → ℝ} (hK : hKReg k) {K : ℕ} {U a0 b0 : ℝ}
    (ha0 : 0 < a0) (hb0 : 0 < b0) (hu0 : ∀ c, 0 ≤ u c) (hu : ∀ c : ℕ, u c ≤ ((c : ℝ) + 1) ^ K * U) :
    LabelRegular u k k a0 b0 := by
  have hU0 : 0 ≤ U := by
    have h := le_trans (hu0 0) (hu 0)
    simpa using h
  obtain ⟨δ, hδd⟩ : ∃ δ, δ = min a0 b0 / 2 := ⟨_, rfl⟩
  have hmin : 0 < min a0 b0 := lt_min ha0 hb0
  have hδ : 0 < δ := by
    rw [hδd]
    exact half_pos hmin
  have hδa : δ < a0 := by
    have := min_le_left a0 b0
    rw [hδd]
    linarith
  have hδb : δ < b0 := by
    have := min_le_right a0 b0
    rw [hδd]
    linarith
  obtain ⟨ca, hca, hA⟩ := kreg_sum_bound hK (lo := a0 - δ) (hi := a0 + δ) (by linarith) (by linarith)
  obtain ⟨cb, hcb, hB⟩ := kreg_sum_bound hK (lo := b0 - δ) (hi := b0 + δ) (by linarith) (by linarith)
  have hy0 : 0 ≤ (a0 + δ) * (b0 + δ) / 4 :=
    div_nonneg (mul_nonneg (by linarith) (by linarith)) (by norm_num)
  unfold LabelRegular
  refine ⟨ha0, hb0, hu0, hK.2.1, hK.2.1, hK.1, hK.1, δ, hδ, hδa, hδb,
    fun c => 9 * U * ca * cb * (((c : ℝ) + 1) ^ (K + 4) * ((a0 + δ) * (b0 + δ) / 4) ^ c / (c.factorial : ℝ)),
    (summable_poly_pow_div_factorial (K + 4) hy0).mul_left (9 * U * ca * cb), ?_⟩
  intro c x hx y hy
  show u c * (|k c x| + |deriv (k c) x| + |iteratedDeriv 2 (k c) x|) *
      (|k c y| + |deriv (k c) y| + |iteratedDeriv 2 (k c) y|)
      ≤ 9 * U * ca * cb * (((c : ℝ) + 1) ^ (K + 4) * ((a0 + δ) * (b0 + δ) / 4) ^ c / (c.factorial : ℝ))
  have hX := hA c x hx
  have hY := hB c y hy
  have hX0 : 0 ≤ |k c x| + |deriv (k c) x| + |iteratedDeriv 2 (k c) x| := by positivity
  have hY0 : 0 ≤ |k c y| + |deriv (k c) y| + |iteratedDeriv 2 (k c) y| := by positivity
  have hF1 : (1 : ℝ) ≤ (c.factorial : ℝ) := by
    exact_mod_cast Nat.one_le_iff_ne_zero.mpr (Nat.factorial_ne_zero c)
  have hF0 : (0 : ℝ) < (c.factorial : ℝ) := by linarith
  have hL0 : (0 : ℝ) ≤ (c : ℝ) + 1 := by positivity
  have hpa : (0 : ℝ) ≤ ((a0 + δ) / 2) ^ c := pow_nonneg (by linarith) c
  have hpb : (0 : ℝ) ≤ ((b0 + δ) / 2) ^ c := pow_nonneg (by linarith) c
  have hUL : 0 ≤ ((c : ℝ) + 1) ^ K * U := mul_nonneg (pow_nonneg hL0 K) hU0
  have hXb0 : 0 ≤ 3 * ca * (((c : ℝ) + 1) ^ 2 * (((a0 + δ) / 2) ^ c / (c.factorial : ℝ))) :=
    mul_nonneg (mul_nonneg (by norm_num) hca.le) (mul_nonneg (by positivity) (div_nonneg hpa hF0.le))
  have hyc : ((a0 + δ) * (b0 + δ) / 4) ^ c = ((a0 + δ) / 2) ^ c * ((b0 + δ) / 2) ^ c := by
    rw [← mul_pow]
    congr 1
    ring
  calc u c * (|k c x| + |deriv (k c) x| + |iteratedDeriv 2 (k c) x|) *
        (|k c y| + |deriv (k c) y| + |iteratedDeriv 2 (k c) y|)
      ≤ (((c : ℝ) + 1) ^ K * U) * (3 * ca * (((c : ℝ) + 1) ^ 2 * (((a0 + δ) / 2) ^ c / (c.factorial : ℝ))))
          * (3 * cb * (((c : ℝ) + 1) ^ 2 * (((b0 + δ) / 2) ^ c / (c.factorial : ℝ)))) :=
        mul_le_mul (mul_le_mul (hu c) hX hX0 hUL) hY hY0 (mul_nonneg hUL hXb0)
    _ = 9 * U * ca * cb * (((c : ℝ) + 1) ^ (K + 4) * (((a0 + δ) / 2) ^ c * ((b0 + δ) / 2) ^ c)
          / (c.factorial : ℝ)) / (c.factorial : ℝ) := by
        ring
    _ ≤ 9 * U * ca * cb * (((c : ℝ) + 1) ^ (K + 4) * (((a0 + δ) / 2) ^ c * ((b0 + δ) / 2) ^ c)
          / (c.factorial : ℝ)) := by
        apply div_le_self _ hF1
        exact mul_nonneg (mul_nonneg (mul_nonneg (mul_nonneg (by norm_num) hU0) hca.le) hcb.le)
          (div_nonneg (mul_nonneg (pow_nonneg hL0 _) (mul_nonneg hpa hpb)) hF0.le)
    _ = 9 * U * ca * cb * (((c : ℝ) + 1) ^ (K + 4) * ((a0 + δ) * (b0 + δ) / 4) ^ c
          / (c.factorial : ℝ)) := by
        rw [hyc]

/-- The four series of `LabelRegular` at the base point converge. -/
theorem labelRegular_summable {u : ℕ → ℝ} {ka kb : ℕ → ℝ → ℝ} {a0 b0 : ℝ}
    (h : LabelRegular u ka kb a0 b0) :
    Summable (fun c => u c * ka c a0 * kb c b0) ∧ Summable (fun c => u c * deriv (ka c) a0 * kb c b0) ∧
    Summable (fun c => u c * ka c a0 * deriv (kb c) b0) ∧
    Summable (fun c => u c * deriv (ka c) a0 * deriv (kb c) b0) := by
  unfold LabelRegular at h
  obtain ⟨-, -, hu, -, -, -, -, δ, hδ, -, -, M, hM, hbd⟩ := h
  have ha0C : a0 ∈ Set.Icc (a0 - δ) (a0 + δ) := ⟨by linarith, by linarith⟩
  have hb0C : b0 ∈ Set.Icc (b0 - δ) (b0 + δ) := ⟨by linarith, by linarith⟩
  refine ⟨Summable.of_norm_bounded hM fun c => ?_, Summable.of_norm_bounded hM fun c => ?_,
    Summable.of_norm_bounded hM fun c => ?_, Summable.of_norm_bounded hM fun c => ?_⟩
  · exact norm_triple_le (hu c) (abs_le_three_left _ _ _) (abs_le_three_left _ _ _) (hbd c a0 ha0C b0 hb0C)
  · exact norm_triple_le (hu c) (abs_le_three_mid _ _ _) (abs_le_three_left _ _ _) (hbd c a0 ha0C b0 hb0C)
  · exact norm_triple_le (hu c) (abs_le_three_left _ _ _) (abs_le_three_mid _ _ _) (hbd c a0 ha0C b0 hb0C)
  · exact norm_triple_le (hu c) (abs_le_three_mid _ _ _) (abs_le_three_mid _ _ _) (hbd c a0 ha0C b0 hb0C)

/-- Chebyshev's inequality for the label law: the weighted covariance is nonnegative. -/
theorem covW_label_nonneg {u : ℕ → ℝ} {k : ℕ → ℝ → ℝ} {a0 b0 : ℝ} (hreg : LabelRegular u k k a0 b0)
    (hR : hRatio k) (hS : 0 < ∑' c, u c * k c a0 * k c b0) :
    0 ≤ covW (fun c => u c * k c a0 * k c b0 / ∑' c', u c' * k c' a0 * k c' b0)
      (fun c => deriv (k c) a0 / k c a0) (fun c => deriv (k c) b0 / k c b0) := by
  obtain ⟨s00, s10, s01, s11⟩ := labelRegular_summable hreg
  have hreg' := hreg
  unfold LabelRegular at hreg'
  obtain ⟨ha0, hb0, hu, -, -, hkp, -, -⟩ := hreg'
  have hSne := hS.ne'
  apply chebyshev_thm
  · intro c
    exact div_nonneg (mul_nonneg (mul_nonneg (hu c) (hkp c a0 ha0).le) (hkp c b0 hb0).le) hS.le
  · have h1 := s00.hasSum.div_const (∑' c', u c' * k c' a0 * k c' b0)
    rwa [div_self hSne] at h1
  · exact (hR a0 ha0).monotone
  · exact (hR b0 hb0).monotone
  · refine (s10.div_const (∑' c', u c' * k c' a0 * k c' b0)).congr fun c => ?_
    have h1 := (hkp c a0 ha0).ne'
    field
  · refine (s01.div_const (∑' c', u c' * k c' a0 * k c' b0)).congr fun c => ?_
    have h2 := (hkp c b0 hb0).ne'
    field
  · refine (s11.div_const (∑' c', u c' * k c' a0 * k c' b0)).congr fun c => ?_
    have h1 := (hkp c a0 ha0).ne'
    have h2 := (hkp c b0 hb0).ne'
    field

/-- The strict form: if every weight is positive, the weighted covariance is positive. -/
theorem covW_label_pos {u : ℕ → ℝ} {k : ℕ → ℝ → ℝ} {a0 b0 : ℝ} (hreg : LabelRegular u k k a0 b0)
    (hR : hRatio k) (hS : 0 < ∑' c, u c * k c a0 * k c b0) (hupos : ∀ c, 0 < u c) :
    0 < covW (fun c => u c * k c a0 * k c b0 / ∑' c', u c' * k c' a0 * k c' b0)
      (fun c => deriv (k c) a0 / k c a0) (fun c => deriv (k c) b0 / k c b0) := by
  obtain ⟨s00, s10, s01, s11⟩ := labelRegular_summable hreg
  have hreg' := hreg
  unfold LabelRegular at hreg'
  obtain ⟨ha0, hb0, -, -, -, hkp, -, -⟩ := hreg'
  have hSne := hS.ne'
  apply chebyshev_strict_thm
  · intro c
    exact div_pos (mul_pos (mul_pos (hupos c) (hkp c a0 ha0)) (hkp c b0 hb0)) hS
  · have h1 := s00.hasSum.div_const (∑' c', u c' * k c' a0 * k c' b0)
    rwa [div_self hSne] at h1
  · exact hR a0 ha0
  · exact hR b0 hb0
  · refine (s10.div_const (∑' c', u c' * k c' a0 * k c' b0)).congr fun c => ?_
    have h1 := (hkp c a0 ha0).ne'
    field
  · refine (s01.div_const (∑' c', u c' * k c' a0 * k c' b0)).congr fun c => ?_
    have h2 := (hkp c b0 hb0).ne'
    field
  · refine (s11.div_const (∑' c', u c' * k c' a0 * k c' b0)).congr fun c => ?_
    have h1 := (hkp c a0 ha0).ne'
    have h2 := (hkp c b0 hb0).ne'
    field

/-! ### From a label series to the covariance -/

theorem partition_pos {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) : 0 < partition N G J := by
  have := omega_isProbabilityMeasure N hN
  have : IsProbabilityMeasure (freeMeasure N V) := by
    unfold freeMeasure
    infer_instance
  unfold partition
  apply integral_exp_pos
  exact integrable_of_abs_le (measurable_energy G J).exp (Real.exp (∑ g ∈ G.edgeFinset, |J g|))
    (fun σ => abs_exp_le (abs_energy_le G J σ))

/-- If the partition function of the updated couplings is a label series with `LabelRegular` data, the
covariance of the two edges is the weighted covariance of Proposition 2.1. -/
theorem gibbsCov_eq_covW {N : ℕ} (hN : 0 < N) {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V} (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet)
    (hef : e ≠ f) (u : ℕ → ℝ) (ka kb : ℕ → ℝ → ℝ)
    (hZ : ∀ a b : ℝ, partition N G (Function.update (Function.update J e a) f b) = ∑' c, u c * ka c a * kb c b)
    (hreg : LabelRegular u ka kb (J e) (J f)) :
    gibbsCov N G J (bond e) (bond f)
      = covW (fun c => u c * ka c (J e) * kb c (J f) / ∑' c', u c' * ka c' (J e) * kb c' (J f))
          (fun c => deriv (ka c) (J e) / ka c (J e)) (fun c => deriv (kb c) (J f) / kb c (J f)) := by
  rw [← covDeriv_thm N V G J e f he hf hef]
  have hfun : (fun a => deriv (fun b => Real.log (partition N G
        (Function.update (Function.update J e a) f b))) (J f))
      = fun a => deriv (fun b => Real.log (∑' c, u c * ka c a * kb c b)) (J f) := by
    funext a
    congr 1
    funext b
    rw [hZ a b]
  rw [hfun]
  apply labelCov_thm u ka kb (J e) (J f) hreg
  rw [← hZ (J e) (J f), Function.update_eq_self, Function.update_eq_self]
  exact partition_pos hN G J

/-! ### Continuity in a uniform shift of the couplings -/

/-- The sum of the bond energies over the edges. -/
def edgeSum {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (σ : Config N V) : ℝ :=
  ∑ g ∈ G.edgeFinset, bond g σ

theorem measurable_edgeSum {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] :
    Measurable (edgeSum (N := N) G) := by
  show Measurable (fun σ : Config N V => ∑ g ∈ G.edgeFinset, bond g σ)
  exact Finset.measurable_sum _ fun g _ => measurable_bond g

theorem abs_edgeSum_le {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (σ : Config N V) : |edgeSum G σ| ≤ (G.edgeFinset.card : ℝ) := by
  show |∑ g ∈ G.edgeFinset, bond g σ| ≤ (G.edgeFinset.card : ℝ)
  calc |∑ g ∈ G.edgeFinset, bond g σ| ≤ ∑ g ∈ G.edgeFinset, |bond g σ| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ g ∈ G.edgeFinset, (1 : ℝ) := Finset.sum_le_sum fun g _ => abs_bond_le g σ
    _ = (G.edgeFinset.card : ℝ) := by simp

theorem energy_shift {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (ε : ℝ) (σ : Config N V) :
    energy G (fun g => J g + ε) σ = energy G J σ + ε * edgeSum G σ := by
  unfold energy edgeSum
  rw [Finset.mul_sum, ← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl fun g _ => by ring

theorem abs_one_mul_le {a b B : ℝ} (ha : |a| ≤ 1) (hb : |b| ≤ B) : |a * b| ≤ B := by
  rw [abs_mul]
  calc |a| * |b| ≤ 1 * B := mul_le_mul ha hb (abs_nonneg _) zero_le_one
    _ = B := one_mul B

/-- If the covariance of two bond energies is nonnegative at `J + ε` for every `ε > 0`, it is nonnegative
at `J`. -/
theorem gibbsCov_nonneg_of_shift {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : Sym2 V)
    (h : ∀ ε : ℝ, 0 < ε → 0 ≤ gibbsCov N G (fun g => J g + ε) (bond e) (bond f)) :
    0 ≤ gibbsCov N G J (bond e) (bond f) := by
  have := omega_isProbabilityMeasure N hN
  have : IsProbabilityMeasure (freeMeasure N V) := by
    unfold freeMeasure
    infer_instance
  have hmE := measurable_energy (N := N) G J
  have hmZ : Measurable (fun σ : Config N V => Real.exp (energy G J σ)) := hmE.exp
  have hm1 : Measurable (fun σ : Config N V => bond e σ * Real.exp (energy G J σ)) :=
    (measurable_bond e).mul hmZ
  have hm2 : Measurable (fun σ : Config N V => bond f σ * Real.exp (energy G J σ)) :=
    (measurable_bond f).mul hmZ
  have hm12 : Measurable (fun σ : Config N V => bond e σ * bond f σ * Real.exp (energy G J σ)) :=
    ((measurable_bond e).mul (measurable_bond f)).mul hmZ
  have hmS : Measurable (edgeSum (N := N) G) := measurable_edgeSum G
  have hSb : ∀ σ : Config N V, |edgeSum G σ| ≤ (G.edgeFinset.card : ℝ) := fun σ => abs_edgeSum_le G σ
  have hbJ : ∀ σ : Config N V, |Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) :=
    fun σ => abs_exp_le (abs_energy_le G J σ)
  have hb1 : ∀ σ : Config N V,
      |bond e σ * Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) :=
    fun σ => abs_one_mul_le (abs_bond_le e σ) (hbJ σ)
  have hb2 : ∀ σ : Config N V,
      |bond f σ * Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) :=
    fun σ => abs_one_mul_le (abs_bond_le f σ) (hbJ σ)
  have hb12 : ∀ σ : Config N V,
      |bond e σ * bond f σ * Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) := by
    intro σ
    rw [mul_assoc]
    exact abs_one_mul_le (abs_bond_le e σ) (hb2 σ)
  have dZ := hasDerivAt_expInt (freeMeasure N V) hmZ hmS hbJ hSb 0
  have dA1 := hasDerivAt_expInt (freeMeasure N V) hm1 hmS hb1 hSb 0
  have dA2 := hasDerivAt_expInt (freeMeasure N V) hm2 hmS hb2 hSb 0
  have dA12 := hasDerivAt_expInt (freeMeasure N V) hm12 hmS hb12 hSb 0
  have hZ0 : expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) 0 ≠ 0 :=
    (expInt_exp_pos (freeMeasure N V) hmE hmS (fun σ => abs_energy_le G J σ) hSb 0).ne'
  have hcov : ∀ ε : ℝ, gibbsCov N G (fun g => J g + ε) (bond e) (bond f)
      = expInt (freeMeasure N V) (fun σ => bond e σ * bond f σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε
        - expInt (freeMeasure N V) (fun σ => bond e σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε
          * (expInt (freeMeasure N V) (fun σ => bond f σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε) := by
    intro ε
    simp only [gibbsCov, gibbsExp, partition, expInt, energy_shift G J ε, Real.exp_add, mul_assoc]
  have hc : ContinuousAt (fun ε : ℝ =>
      expInt (freeMeasure N V) (fun σ => bond e σ * bond f σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε
        - expInt (freeMeasure N V) (fun σ => bond e σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε
          * (expInt (freeMeasure N V) (fun σ => bond f σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε)) 0 :=
    (dA12.continuousAt.div dZ.continuousAt hZ0).sub
      ((dA1.continuousAt.div dZ.continuousAt hZ0).mul (dA2.continuousAt.div dZ.continuousAt hZ0))
  have h0eq : (fun g => J g + 0) = J := funext fun g => add_zero (J g)
  have hval := hcov 0
  rw [h0eq] at hval
  rw [hval]
  have ht := hc.tendsto.mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  refine ge_of_tendsto ht (eventually_nhdsWithin_of_forall fun ε hε => ?_)
  have h1 := h ε hε
  rw [hcov ε] at h1
  exact h1

/-! ### The cycle -/

theorem cycle_series {N : ℕ} {k : ℕ → ℝ → ℝ} {d : ℕ → ℝ} (hCZ : hCycleZ N k d) (n : ℕ)
    [DecidableRel (SimpleGraph.cycleGraph n).Adj] (h3 : 3 ≤ n) (J : Sym2 (Fin n) → ℝ) {e f : Sym2 (Fin n)}
    (he' : e ∈ (SimpleGraph.cycleGraph n).edgeFinset) (hf' : f ∈ (SimpleGraph.cycleGraph n).edgeFinset)
    (hef : e ≠ f) (a b : ℝ) :
    partition N (SimpleGraph.cycleGraph n) (Function.update (Function.update J e a) f b)
      = ∑' c, (d c * ∏ g ∈ ((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f, k c (J g))
          * k c a * k c b := by
  rw [← (hCZ n h3 (Function.update (Function.update J e a) f b)).tsum_eq]
  congr 1
  funext c
  have hfe : f ∈ (SimpleGraph.cycleGraph n).edgeFinset.erase e :=
    Finset.mem_erase.mpr ⟨fun h => hef h.symm, hf'⟩
  rw [← Finset.mul_prod_erase _ _ he', ← Finset.mul_prod_erase _ _ hfe]
  have h1 : Function.update (Function.update J e a) f b e = a := by
    rw [Function.update_of_ne hef, Function.update_self]
  have h2 : Function.update (Function.update J e a) f b f = b := Function.update_self _ _ _
  have h3' : ∏ g ∈ ((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f,
        k c (Function.update (Function.update J e a) f b g)
      = ∏ g ∈ ((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f, k c (J g) := by
    apply Finset.prod_congr rfl
    intro g hg
    have hgf : g ≠ f := (Finset.mem_erase.mp hg).1
    have hge : g ≠ e := (Finset.mem_erase.mp (Finset.mem_erase.mp hg).2).1
    rw [Function.update_of_ne hgf, Function.update_of_ne hge]
  rw [h1, h2, h3']
  ring

theorem cycle_labelRegular {N : ℕ} {k : ℕ → ℝ → ℝ} {d : ℕ → ℝ} {C : ℕ → ℝ → ℝ} (hFH : hFH N k d C)
    (hK : hKReg k) {ι : Type*} (s : Finset ι) (x : ι → ℝ) (hx : ∀ g ∈ s, 0 < x g) {a0 b0 : ℝ}
    (ha0 : 0 < a0) (hb0 : 0 < b0) :
    LabelRegular (fun c => d c * ∏ g ∈ s, k c (x g)) k k a0 b0 := by
  obtain ⟨U, hU⟩ := prod_k_bounded hK s x hx
  refine labelRegular_of_bounds hK (K := N) (U := U) ha0 hb0 (fun c => ?_) (fun c => ?_)
  · exact mul_nonneg (hFH.2.2.1 c).1 (Finset.prod_nonneg fun g hg => (hK.1 c (x g) (hx g hg)).le)
  · have hd := hFH.2.2.1 c
    calc d c * ∏ g ∈ s, k c (x g) ≤ d c * |∏ g ∈ s, k c (x g)| :=
          mul_le_mul_of_nonneg_left (le_abs_self _) hd.1
      _ ≤ ((c : ℝ) + 1) ^ N * U := mul_le_mul hd.2 (hU c) (abs_nonneg _) (by positivity)

/-- Theorem 1.1 on a cycle with couplings positive on every edge, nonstrict form. -/
theorem cycle_pos_cov {N : ℕ} (hN : 0 < N) {k : ℕ → ℝ → ℝ} {d : ℕ → ℝ} {C : ℕ → ℝ → ℝ}
    (hFH : hFH N k d C) (hK : hKReg k) (hR : hRatio k) (hCZ : hCycleZ N k d)
    (n : ℕ) [DecidableRel (SimpleGraph.cycleGraph n).Adj] (h3 : 3 ≤ n) (J : Sym2 (Fin n) → ℝ)
    (hJ : ∀ g ∈ (SimpleGraph.cycleGraph n).edgeSet, 0 < J g) {e f : Sym2 (Fin n)}
    (he : e ∈ (SimpleGraph.cycleGraph n).edgeSet) (hf : f ∈ (SimpleGraph.cycleGraph n).edgeSet) (hef : e ≠ f) :
    0 ≤ gibbsCov N (SimpleGraph.cycleGraph n) J (bond e) (bond f) := by
  have he' := SimpleGraph.mem_edgeFinset.mpr he
  have hf' := SimpleGraph.mem_edgeFinset.mpr hf
  have hx : ∀ g ∈ ((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f, 0 < J g := fun g hg =>
    hJ g (SimpleGraph.mem_edgeFinset.mp (Finset.mem_of_mem_erase (Finset.mem_of_mem_erase hg)))
  have hser := cycle_series hCZ n h3 J he' hf' hef
  have hreg := cycle_labelRegular hFH hK (((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f) J hx
    (hJ e he) (hJ f hf)
  have hS : 0 < ∑' c, (d c * ∏ g ∈ ((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f, k c (J g))
      * k c (J e) * k c (J f) := by
    rw [← hser (J e) (J f), Function.update_eq_self, Function.update_eq_self]
    exact partition_pos hN _ J
  rw [gibbsCov_eq_covW hN _ J he hf hef _ k k hser hreg]
  exact covW_label_nonneg hreg hR hS

theorem cycleG2_thm (N : ℕ) : cycleG2_statement N := by
  unfold cycleG2_statement
  intro k d C hFH hK hR hCZ n _ h3 J hJ e he f hf hef
  unfold G2pair
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · have hV : Nonempty (Fin n) := ⟨⟨0, by omega⟩⟩
    have h0 : freeMeasure 0 (Fin n) = 0 := freeMeasure_zero (Fin n)
    simp [gibbsCov, gibbsExp, partition, h0]
  apply gibbsCov_nonneg_of_shift hN _ J e f
  intro ε hε
  exact cycle_pos_cov hN hFH hK hR hCZ n h3 (fun g => J g + ε)
    (fun g hg => by
      show 0 < J g + ε
      have := hJ g hg
      linarith) he hf hef

theorem cycleG2_strict_thm (N : ℕ) : cycleG2_strict_statement N := by
  unfold cycleG2_strict_statement
  intro k d C hFH hK hR hCZ hd n _ h3 J hJ e he f hf hef
  have hxE : ∀ g ∈ (SimpleGraph.cycleGraph n).edgeFinset, 0 < J g :=
    fun g hg => hJ g (SimpleGraph.mem_edgeFinset.mp hg)
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · exfalso
    have hV : Nonempty (Fin n) := ⟨⟨0, by omega⟩⟩
    have h0 : partition 0 (SimpleGraph.cycleGraph n) J = 0 := by
      simp [partition, freeMeasure_zero (Fin n)]
    have hs := hCZ n h3 J
    rw [h0] at hs
    have hpos : ∀ c, 0 < d c * ∏ g ∈ (SimpleGraph.cycleGraph n).edgeFinset, k c (J g) :=
      fun c => mul_pos (hd c) (Finset.prod_pos fun g hg => hK.1 c (J g) (hxE g hg))
    have h1 := hs.summable.tsum_pos (fun c => (hpos c).le) 0 (hpos 0)
    rw [hs.tsum_eq] at h1
    exact lt_irrefl 0 h1
  have he' := SimpleGraph.mem_edgeFinset.mpr he
  have hf' := SimpleGraph.mem_edgeFinset.mpr hf
  have hx : ∀ g ∈ ((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f, 0 < J g := fun g hg =>
    hxE g (Finset.mem_of_mem_erase (Finset.mem_of_mem_erase hg))
  have hser := cycle_series hCZ n h3 J he' hf' hef
  have hreg := cycle_labelRegular hFH hK (((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f) J hx
    (hJ e he) (hJ f hf)
  have hS : 0 < ∑' c, (d c * ∏ g ∈ ((SimpleGraph.cycleGraph n).edgeFinset.erase e).erase f, k c (J g))
      * k c (J e) * k c (J f) := by
    rw [← hser (J e) (J f), Function.update_eq_self, Function.update_eq_self]
    exact partition_pos hN _ J
  rw [gibbsCov_eq_covW hN _ J he hf hef _ k k hser hreg]
  exact covW_label_pos hreg hR hS
    (fun c => mul_pos (hd c) (Finset.prod_pos fun g hg => hK.1 c (J g) (hx g hg)))

end G2Kernel
