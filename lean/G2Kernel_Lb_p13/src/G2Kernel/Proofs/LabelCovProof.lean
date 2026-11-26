/-
G2Kernel.Proofs.LabelCovProof: proofs of `covDeriv_statement` and `labelCov_statement` (module M2,
Proposition 2.1). Kernel proof, step L-b.
- covDeriv: for N ≥ 1 the single-site measure ω is a probability measure, hence so is the configuration
  measure. With R = E_J - J_e s_e - J_f s_f, the weight of the updated couplings is exp(R + a s_e) exp(b s_f).
  Bond energies are bounded by 1, so differentiation under the integral sign applies (`hasDerivAt_expInt`):
  the inner derivative is Z_b / Z for every a, and the outer one is (Z_ab Z - Z_b Z_a) / Z², the Gibbs
  covariance. For N = 0 the sphere is empty, ω = 0, and both sides are 0.
- labelCov: on the δ-neighbourhoods of `LabelRegular` the series and its termwise derivatives are dominated
  by `M`, so `hasDerivAt_tsum_of_isPreconnected` differentiates termwise; the quotient rule and `ka, kb > 0`
  turn the result into the weighted covariance `covW`.
-/
import G2Kernel.LabelCov

noncomputable section
open MeasureTheory Real Filter Topology

namespace G2Kernel

/-! ### Generic lemmas -/

theorem integrable_of_abs_le {X : Type*} [MeasurableSpace X] {μ : Measure X} [IsFiniteMeasure μ]
    {g : X → ℝ} (hg : Measurable g) (C : ℝ) (hC : ∀ x, |g x| ≤ C) : Integrable g μ :=
  Integrable.mono' (integrable_const C) hg.aestronglyMeasurable
    (ae_of_all _ fun x => (Real.norm_eq_abs (g x)).le.trans (hC x))

theorem abs_exp_le {x C : ℝ} (h : |x| ≤ C) : |Real.exp x| ≤ Real.exp C := by
  rw [abs_of_pos (Real.exp_pos x)]
  exact Real.exp_le_exp.mpr ((le_abs_self x).trans h)

/-- `∫ φ(x) exp(t ψ(x)) dμ`. -/
def expInt {X : Type*} [MeasurableSpace X] (μ : Measure X) (φ ψ : X → ℝ) (t : ℝ) : ℝ :=
  ∫ x, φ x * Real.exp (t * ψ x) ∂μ

/-- Differentiation under the integral sign for `expInt` with bounded measurable `φ`, `ψ`. -/
theorem hasDerivAt_expInt {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ]
    {φ ψ : X → ℝ} (hφ : Measurable φ) (hψ : Measurable ψ) {A B : ℝ} (hA : ∀ x, |φ x| ≤ A)
    (hB : ∀ x, |ψ x| ≤ B) (t₀ : ℝ) :
    HasDerivAt (expInt μ φ ψ) (expInt μ (fun x => φ x * ψ x) ψ t₀) t₀ := by
  have hB0 : ∀ x, 0 ≤ B := fun x => (abs_nonneg _).trans (hB x)
  have hA0 : ∀ x, 0 ≤ A := fun x => (abs_nonneg _).trans (hA x)
  have hexp : ∀ (t : ℝ) (x : X), |t| ≤ |t₀| + 1 → Real.exp (t * ψ x) ≤ Real.exp ((|t₀| + 1) * B) := by
    intro t x ht
    apply Real.exp_le_exp.mpr
    have h1 : t * ψ x ≤ |t| * |ψ x| := by
      rw [← abs_mul]
      exact le_abs_self _
    have h2 : |t| * |ψ x| ≤ (|t₀| + 1) * B :=
      mul_le_mul ht (hB x) (abs_nonneg _) (by positivity)
    linarith
  have hmeas : ∀ t : ℝ, Measurable (fun x => φ x * Real.exp (t * ψ x)) :=
    fun t => hφ.mul (hψ.const_mul t).exp
  have hmeas' : Measurable (fun x => φ x * ψ x * Real.exp (t₀ * ψ x)) :=
    (hφ.mul hψ).mul (hψ.const_mul t₀).exp
  have hint : Integrable (fun x => φ x * Real.exp (t₀ * ψ x)) μ := by
    refine integrable_of_abs_le (hmeas t₀) (A * Real.exp ((|t₀| + 1) * B)) fun x => ?_
    show |φ x * Real.exp (t₀ * ψ x)| ≤ A * Real.exp ((|t₀| + 1) * B)
    rw [abs_mul, abs_of_pos (Real.exp_pos _)]
    exact mul_le_mul (hA x) (hexp t₀ x (by linarith)) (Real.exp_pos _).le (hA0 x)
  have hbound : ∀ (x : X), ∀ t ∈ Metric.ball t₀ 1,
      ‖φ x * ψ x * Real.exp (t * ψ x)‖ ≤ A * (B * Real.exp ((|t₀| + 1) * B)) := by
    intro x t ht
    have ht' : |t| ≤ |t₀| + 1 := by
      rw [Metric.mem_ball, Real.dist_eq] at ht
      obtain ⟨h1, h2⟩ := abs_lt.mp ht
      obtain ⟨h3, h4⟩ := abs_le.mp (le_refl |t₀|)
      exact abs_le.mpr ⟨by linarith, by linarith⟩
    rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_of_pos (Real.exp_pos _), mul_assoc]
    exact mul_le_mul (hA x) (mul_le_mul (hB x) (hexp t x ht') (Real.exp_pos _).le (hB0 x))
      (mul_nonneg (abs_nonneg _) (Real.exp_pos _).le) (hA0 x)
  have hderiv : ∀ (x : X) (t : ℝ),
      HasDerivAt (fun t => φ x * Real.exp (t * ψ x)) (φ x * ψ x * Real.exp (t * ψ x)) t := by
    intro x t
    exact (((hasDerivAt_id' (x := t)).mul_const (ψ x)).exp.const_mul (φ x)).congr_deriv (by ring)
  obtain ⟨-, h⟩ := hasDerivAt_integral_of_dominated_loc_of_deriv_le (μ := μ)
    (F := fun t x => φ x * Real.exp (t * ψ x)) (F' := fun t x => φ x * ψ x * Real.exp (t * ψ x))
    (x₀ := t₀) (bound := fun _ => A * (B * Real.exp ((|t₀| + 1) * B))) (s := Metric.ball t₀ 1)
    (Metric.ball_mem_nhds t₀ one_pos) (Eventually.of_forall fun t => (hmeas t).aestronglyMeasurable)
    hint hmeas'.aestronglyMeasurable (ae_of_all _ fun x t ht => hbound x t ht) (integrable_const _)
    (ae_of_all _ fun x t _ => hderiv x t)
  exact h

/-- `expInt` of an exponential against a probability measure is positive. -/
theorem expInt_exp_pos {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsProbabilityMeasure μ]
    {g ψ : X → ℝ} (hg : Measurable g) (hψ : Measurable ψ) {C B : ℝ} (hC : ∀ x, |g x| ≤ C)
    (hB : ∀ x, |ψ x| ≤ B) (t : ℝ) : 0 < expInt μ (fun x => Real.exp (g x)) ψ t := by
  have e : expInt μ (fun x => Real.exp (g x)) ψ t = ∫ x, Real.exp (g x + t * ψ x) ∂μ := by
    simp only [expInt]
    congr 1
    funext x
    rw [Real.exp_add]
  rw [e]
  apply integral_exp_pos
  refine integrable_of_abs_le (hg.add (hψ.const_mul t)).exp (Real.exp (C + |t| * B)) fun x => ?_
  show |Real.exp (g x + t * ψ x)| ≤ Real.exp (C + |t| * B)
  apply abs_exp_le
  refine (abs_add_le _ _).trans (add_le_add (hC x) ?_)
  rw [abs_mul]
  exact mul_le_mul_of_nonneg_left (hB x) (abs_nonneg t)

/-! ### The single-site and configuration measures -/

theorem omega_isProbabilityMeasure (N : ℕ) (hN : 0 < N) : IsProbabilityMeasure (omega N) := by
  constructor
  have h1 : (volume : Measure (Amb N)).toSphere Set.univ ≠ 0 := by
    rw [Measure.toSphere_apply_univ, finrank_euclideanSpace_fin]
    exact mul_ne_zero (by exact_mod_cast hN.ne') (Metric.measure_ball_pos volume 0 one_pos).ne'
  have h2 : (volume : Measure (Amb N)).toSphere Set.univ ≠ ⊤ := by
    rw [Measure.toSphere_apply_univ, finrank_euclideanSpace_fin]
    exact ENNReal.mul_ne_top (ENNReal.natCast_ne_top N) measure_ball_lt_top.ne
  rw [omega, Measure.smul_apply, smul_eq_mul]
  exact ENNReal.inv_mul_cancel h1 h2

theorem omega_zero : omega 0 = 0 := by
  have h : (volume : Measure (Amb 0)).toSphere = 0 := by
    rw [Measure.toSphere_eq_zero_iff_finrank, finrank_euclideanSpace_fin]
  rw [omega, h, smul_zero]

theorem freeMeasure_zero (W : Type*) [Fintype W] [Nonempty W] : freeMeasure 0 W = 0 := by
  rw [← Measure.measure_univ_eq_zero, freeMeasure, omega_zero, Measure.pi_univ]
  obtain ⟨x⟩ := ‹Nonempty W›
  exact Finset.prod_eq_zero (Finset.mem_univ x) (by simp)

/-! ### Bond energies -/

variable {V : Type*}

theorem abs_bond_le {N : ℕ} (e : Sym2 V) (σ : Config N V) : |bond e σ| ≤ 1 := by
  refine Sym2.ind (fun x y => ?_) e
  show |dot (σ x) (σ y)| ≤ 1
  have hx : ‖((σ x : Sph N) : Amb N)‖ = 1 := norm_eq_of_mem_sphere (σ x)
  have hy : ‖((σ y : Sph N) : Amb N)‖ = 1 := norm_eq_of_mem_sphere (σ y)
  have h := abs_real_inner_le_norm ((σ x : Sph N) : Amb N) ((σ y : Sph N) : Amb N)
  rw [hx, hy, one_mul] at h
  exact h

theorem measurable_bond {N : ℕ} (e : Sym2 V) : Measurable (bond (N := N) e) := by
  refine Sym2.ind (fun x y => ?_) e
  show Measurable (fun σ : Config N V =>
    @inner ℝ (Amb N) _ ((σ x : Sph N) : Amb N) ((σ y : Sph N) : Amb N))
  exact Measurable.inner (measurable_subtype_coe.comp (measurable_pi_apply x))
    (measurable_subtype_coe.comp (measurable_pi_apply y))

variable [Fintype V]

theorem measurable_energy {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    Measurable (energy (N := N) G J) := by
  show Measurable (fun σ : Config N V => ∑ g ∈ G.edgeFinset, J g * bond g σ)
  exact Finset.measurable_sum _ fun g _ => (measurable_bond g).const_mul (J g)

theorem abs_energy_le {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (σ : Config N V) : |energy G J σ| ≤ ∑ g ∈ G.edgeFinset, |J g| := by
  show |∑ g ∈ G.edgeFinset, J g * bond g σ| ≤ ∑ g ∈ G.edgeFinset, |J g|
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun g _ => ?_)
  rw [abs_mul]
  exact mul_le_of_le_one_right (abs_nonneg _) (abs_bond_le g σ)

variable [DecidableEq V]

/-- The energy without the edges `e` and `f`: `E_J - J_e s_e - J_f s_f`. -/
def restEnergy {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : Sym2 V)
    (σ : Config N V) : ℝ :=
  energy G J σ - J e * bond e σ - J f * bond f σ

theorem energy_update {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) (a b : ℝ) (σ : Config N V) :
    energy G (Function.update (Function.update J e a) f b) σ
      = restEnergy G J e f σ + a * bond e σ + b * bond f σ := by
  have he' : e ∈ G.edgeFinset := SimpleGraph.mem_edgeFinset.mpr he
  have hf' : f ∈ G.edgeFinset := SimpleGraph.mem_edgeFinset.mpr hf
  have hfe : f ≠ e := fun h => hef h.symm
  have key : ∀ g, Function.update (Function.update J e a) f b g * bond g σ
      = J g * bond g σ + ((if g = e then a - J e else 0) + (if g = f then b - J f else 0)) * bond g σ := by
    intro g
    by_cases hgf : g = f
    · rw [hgf, Function.update_self, ite_eq_right hfe, ite_eq_left rfl]
      ring
    · by_cases hge : g = e
      · rw [Function.update_of_ne hgf, hge, Function.update_self, ite_eq_left rfl, ite_eq_right hef]
        ring
      · rw [Function.update_of_ne hgf, Function.update_of_ne hge, ite_eq_right hge, ite_eq_right hgf]
        ring
  show ∑ g ∈ G.edgeFinset, Function.update (Function.update J e a) f b g * bond g σ
      = restEnergy G J e f σ + a * bond e σ + b * bond f σ
  rw [Finset.sum_congr rfl (fun g _ => key g), Finset.sum_add_distrib]
  simp only [add_mul, Finset.sum_add_distrib, ite_mul, zero_mul, Finset.sum_ite_eq']
  rw [ite_eq_left he', ite_eq_left hf']
  unfold restEnergy energy
  ring

/-! ### Proposition 2.1, first equality -/

theorem covDeriv_thm (N : ℕ) : covDeriv_statement N := by
  unfold covDeriv_statement
  intro V _ _ G _ J e f he hf hef
  have hV : Nonempty V := by
    refine Sym2.ind (fun x _ => ?_) e
    exact ⟨x⟩
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · have h0 : freeMeasure 0 V = 0 := freeMeasure_zero V
    simp [partition, gibbsCov, gibbsExp, h0]
  have := omega_isProbabilityMeasure N hN
  have : IsProbabilityMeasure (freeMeasure N V) := by
    unfold freeMeasure
    infer_instance
  have hmE : Measurable (bond (N := N) e) := measurable_bond e
  have hmF : Measurable (bond (N := N) f) := measurable_bond f
  have hmR : Measurable (restEnergy (N := N) G J e f) := by
    show Measurable (fun σ : Config N V => energy G J σ - J e * bond e σ - J f * bond f σ)
    exact ((measurable_energy G J).sub (hmE.const_mul _)).sub (hmF.const_mul _)
  obtain ⟨K, hK⟩ : ∃ K, K = ∑ g ∈ G.edgeFinset, |J g| + |J e| + |J f| := ⟨_, rfl⟩
  have hRb : ∀ σ : Config N V, |restEnergy G J e f σ| ≤ K := by
    intro σ
    have h1 := abs_le.mp (abs_energy_le G J σ)
    have h2 : |J e * bond e σ| ≤ |J e| := by
      rw [abs_mul]
      exact mul_le_of_le_one_right (abs_nonneg _) (abs_bond_le e σ)
    have h3 : |J f * bond f σ| ≤ |J f| := by
      rw [abs_mul]
      exact mul_le_of_le_one_right (abs_nonneg _) (abs_bond_le f σ)
    have h2' := abs_le.mp h2
    have h3' := abs_le.mp h3
    rw [hK]
    unfold restEnergy
    exact abs_le.mpr ⟨by linarith [h1.1, h2'.2, h3'.2], by linarith [h1.2, h2'.1, h3'.1]⟩
  have hXb : ∀ (c : ℝ) (s : Config N V → ℝ), (∀ σ, |s σ| ≤ 1) →
      ∀ σ, |restEnergy G J e f σ + c * s σ| ≤ K + |c| := by
    intro c s hs σ
    have h2 : |c * s σ| ≤ |c| := by
      rw [abs_mul]
      exact mul_le_of_le_one_right (abs_nonneg _) (hs σ)
    exact (abs_add_le _ _).trans (add_le_add (hRb σ) h2)
  have hbE : ∀ σ : Config N V, |bond e σ| ≤ 1 := fun σ => abs_bond_le e σ
  have hbF : ∀ σ : Config N V, |bond f σ| ≤ 1 := fun σ => abs_bond_le f σ
  -- the functions of the two differentiation steps
  have hmφa : ∀ a : ℝ, Measurable (fun σ : Config N V => Real.exp (restEnergy G J e f σ + a * bond e σ)) :=
    fun a => (hmR.add (hmE.const_mul a)).exp
  have hmφQ : Measurable (fun σ : Config N V => Real.exp (restEnergy G J e f σ + J f * bond f σ)) :=
    (hmR.add (hmF.const_mul (J f))).exp
  have hmφP : Measurable
      (fun σ : Config N V => bond f σ * Real.exp (restEnergy G J e f σ + J f * bond f σ)) :=
    hmF.mul hmφQ
  have hbφa : ∀ (a : ℝ) (σ : Config N V),
      |Real.exp (restEnergy G J e f σ + a * bond e σ)| ≤ Real.exp (K + |a|) :=
    fun a σ => abs_exp_le (hXb a (bond e) hbE σ)
  have hbφQ : ∀ σ : Config N V,
      |Real.exp (restEnergy G J e f σ + J f * bond f σ)| ≤ Real.exp (K + |J f|) :=
    fun σ => abs_exp_le (hXb (J f) (bond f) hbF σ)
  have hbφP : ∀ σ : Config N V,
      |bond f σ * Real.exp (restEnergy G J e f σ + J f * bond f σ)| ≤ Real.exp (K + |J f|) := by
    intro σ
    rw [abs_mul]
    calc |bond f σ| * |Real.exp (restEnergy G J e f σ + J f * bond f σ)| ≤ 1 * Real.exp (K + |J f|) :=
          mul_le_mul (hbF σ) (hbφQ σ) (abs_nonneg _) zero_le_one
      _ = Real.exp (K + |J f|) := one_mul _
  -- the partition function of the updated couplings
  have hZ : ∀ a b : ℝ, partition N G (Function.update (Function.update J e a) f b)
      = expInt (freeMeasure N V) (fun σ => Real.exp (restEnergy G J e f σ + a * bond e σ)) (bond f) b := by
    intro a b
    simp only [partition, expInt]
    congr 1
    funext σ
    rw [energy_update G J he hf hef a b σ, ← Real.exp_add]
  have hpos : ∀ a b : ℝ,
      0 < expInt (freeMeasure N V) (fun σ => Real.exp (restEnergy G J e f σ + a * bond e σ)) (bond f) b :=
    fun a b => expInt_exp_pos (freeMeasure N V) (hmR.add (hmE.const_mul a)) hmF (hXb a (bond e) hbE) hbF b
  -- the inner derivative, for every a
  have hinner : ∀ a : ℝ,
      deriv (fun b => Real.log (partition N G (Function.update (Function.update J e a) f b))) (J f)
        = expInt (freeMeasure N V) (fun σ => Real.exp (restEnergy G J e f σ + a * bond e σ) * bond f σ)
            (bond f) (J f)
          / expInt (freeMeasure N V) (fun σ => Real.exp (restEnergy G J e f σ + a * bond e σ)) (bond f) (J f) := by
    intro a
    have hfun : (fun b => Real.log (partition N G (Function.update (Function.update J e a) f b)))
        = fun b => Real.log (expInt (freeMeasure N V)
            (fun σ => Real.exp (restEnergy G J e f σ + a * bond e σ)) (bond f) b) := by
      funext b
      rw [hZ a b]
    rw [hfun]
    exact ((hasDerivAt_expInt (freeMeasure N V) (hmφa a) hmF (hbφa a) hbF (J f)).log
      (hpos a (J f)).ne').deriv
  -- the same quotient, as functions of a
  have hPa : ∀ a : ℝ,
      expInt (freeMeasure N V) (fun σ => Real.exp (restEnergy G J e f σ + a * bond e σ) * bond f σ)
        (bond f) (J f)
      = expInt (freeMeasure N V) (fun σ => bond f σ * Real.exp (restEnergy G J e f σ + J f * bond f σ))
          (bond e) a := by
    intro a
    simp only [expInt]
    congr 1
    funext σ
    simp only [Real.exp_add]
    ring
  have hQa : ∀ a : ℝ,
      expInt (freeMeasure N V) (fun σ => Real.exp (restEnergy G J e f σ + a * bond e σ)) (bond f) (J f)
      = expInt (freeMeasure N V) (fun σ => Real.exp (restEnergy G J e f σ + J f * bond f σ)) (bond e) a := by
    intro a
    simp only [expInt]
    congr 1
    funext σ
    simp only [Real.exp_add]
    ring
  have hGfun : (fun a => deriv (fun b => Real.log (partition N G
        (Function.update (Function.update J e a) f b))) (J f))
      = fun a => expInt (freeMeasure N V)
            (fun σ => bond f σ * Real.exp (restEnergy G J e f σ + J f * bond f σ)) (bond e) a
          / expInt (freeMeasure N V) (fun σ => Real.exp (restEnergy G J e f σ + J f * bond f σ)) (bond e) a := by
    funext a
    rw [hinner a, hPa a, hQa a]
  rw [hGfun]
  have hdP := hasDerivAt_expInt (freeMeasure N V) hmφP hmE hbφP hbE (J e)
  have hdQ := hasDerivAt_expInt (freeMeasure N V) hmφQ hmE hbφQ hbE (J e)
  have hQpos : 0 < expInt (freeMeasure N V)
      (fun σ => Real.exp (restEnergy G J e f σ + J f * bond f σ)) (bond e) (J e) :=
    expInt_exp_pos (freeMeasure N V) (hmR.add (hmF.const_mul (J f))) hmE (hXb (J f) (bond f) hbF) hbE (J e)
  rw [(hdP.fun_div hdQ hQpos.ne').deriv]
  -- evaluation at a = J_e
  have hE : ∀ σ : Config N V, Real.exp (energy G J σ)
      = Real.exp (restEnergy G J e f σ + J f * bond f σ) * Real.exp (J e * bond e σ) := by
    intro σ
    rw [← Real.exp_add]
    congr 1
    unfold restEnergy
    ring
  have i1 : expInt (freeMeasure N V)
      (fun x => bond f x * Real.exp (restEnergy G J e f x + J f * bond f x) * bond e x) (bond e) (J e)
      = ∫ σ, bond e σ * bond f σ * Real.exp (energy G J σ) ∂(freeMeasure N V) := by
    simp only [expInt]
    congr 1
    funext σ
    rw [hE σ]
    ring
  have i2 : expInt (freeMeasure N V)
      (fun σ => Real.exp (restEnergy G J e f σ + J f * bond f σ)) (bond e) (J e) = partition N G J := by
    simp only [expInt, partition]
    congr 1
    funext σ
    rw [hE σ]
  have i3 : expInt (freeMeasure N V)
      (fun σ => bond f σ * Real.exp (restEnergy G J e f σ + J f * bond f σ)) (bond e) (J e)
      = ∫ σ, bond f σ * Real.exp (energy G J σ) ∂(freeMeasure N V) := by
    simp only [expInt]
    congr 1
    funext σ
    rw [hE σ]
    ring
  have i4 : expInt (freeMeasure N V)
      (fun x => Real.exp (restEnergy G J e f x + J f * bond f x) * bond e x) (bond e) (J e)
      = ∫ σ, bond e σ * Real.exp (energy G J σ) ∂(freeMeasure N V) := by
    simp only [expInt]
    congr 1
    funext σ
    rw [hE σ]
    ring
  have hZne : partition N G J ≠ 0 := by
    rw [← i2]
    exact hQpos.ne'
  rw [i1, i2, i3, i4]
  simp only [gibbsCov, gibbsExp]
  field

/-! ### Proposition 2.1, second equality -/

theorem norm_triple_le {u X Y X' Y' M : ℝ} (hu : 0 ≤ u) (hX : |X| ≤ X') (hY : |Y| ≤ Y')
    (h : u * X' * Y' ≤ M) : ‖u * X * Y‖ ≤ M := by
  rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_of_nonneg hu]
  refine le_trans ?_ h
  exact mul_le_mul (mul_le_mul_of_nonneg_left hX hu) hY (abs_nonneg _)
    (mul_nonneg hu ((abs_nonneg _).trans hX))

theorem labelCov_thm : labelCov_statement := by
  unfold labelCov_statement
  intro u ka kb a0 b0 hreg hS0
  unfold LabelRegular at hreg
  obtain ⟨ha0, hb0, hu, hka, hkb, hkapos, hkbpos, δ, hδ, hδa, hδb, M, hM, hbd⟩ := hreg
  have dka : ∀ c, Differentiable ℝ (ka c) :=
    fun c => ((hka c).of_le one_le_two).differentiable one_ne_zero
  have dkb : ∀ c, Differentiable ℝ (kb c) :=
    fun c => ((hkb c).of_le one_le_two).differentiable one_ne_zero
  have sa : ∀ c x, |ka c x| ≤ |ka c x| + |deriv (ka c) x| + |iteratedDeriv 2 (ka c) x| := by
    intro c x
    have := abs_nonneg (deriv (ka c) x)
    have := abs_nonneg (iteratedDeriv 2 (ka c) x)
    linarith
  have sa' : ∀ c x, |deriv (ka c) x| ≤ |ka c x| + |deriv (ka c) x| + |iteratedDeriv 2 (ka c) x| := by
    intro c x
    have := abs_nonneg (ka c x)
    have := abs_nonneg (iteratedDeriv 2 (ka c) x)
    linarith
  have sb : ∀ c y, |kb c y| ≤ |kb c y| + |deriv (kb c) y| + |iteratedDeriv 2 (kb c) y| := by
    intro c y
    have := abs_nonneg (deriv (kb c) y)
    have := abs_nonneg (iteratedDeriv 2 (kb c) y)
    linarith
  have sb' : ∀ c y, |deriv (kb c) y| ≤ |kb c y| + |deriv (kb c) y| + |iteratedDeriv 2 (kb c) y| := by
    intro c y
    have := abs_nonneg (kb c y)
    have := abs_nonneg (iteratedDeriv 2 (kb c) y)
    linarith
  have B00 : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      ‖u c * ka c x * kb c y‖ ≤ M c :=
    fun c x hx y hy => norm_triple_le (hu c) (sa c x) (sb c y) (hbd c x hx y hy)
  have B01 : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      ‖u c * ka c x * deriv (kb c) y‖ ≤ M c :=
    fun c x hx y hy => norm_triple_le (hu c) (sa c x) (sb' c y) (hbd c x hx y hy)
  have B10 : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      ‖u c * deriv (ka c) x * kb c y‖ ≤ M c :=
    fun c x hx y hy => norm_triple_le (hu c) (sa' c x) (sb c y) (hbd c x hx y hy)
  have B11 : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      ‖u c * deriv (ka c) x * deriv (kb c) y‖ ≤ M c :=
    fun c x hx y hy => norm_triple_le (hu c) (sa' c x) (sb' c y) (hbd c x hx y hy)
  have ha0I : a0 ∈ Set.Ioo (a0 - δ) (a0 + δ) := ⟨by linarith, by linarith⟩
  have hb0I : b0 ∈ Set.Ioo (b0 - δ) (b0 + δ) := ⟨by linarith, by linarith⟩
  have ha0C : a0 ∈ Set.Icc (a0 - δ) (a0 + δ) := Set.Ioo_subset_Icc_self ha0I
  have hb0C : b0 ∈ Set.Icc (b0 - δ) (b0 + δ) := Set.Ioo_subset_Icc_self hb0I
  -- a label with positive weight
  obtain ⟨c0, hc0⟩ : ∃ c0, 0 < u c0 := by
    by_contra h
    push Not at h
    have hz : ∀ c, u c * ka c a0 * kb c b0 = 0 := fun c => by
      rw [le_antisymm (h c) (hu c), zero_mul, zero_mul]
    have h0 : (∑' c, u c * ka c a0 * kb c b0) = 0 := by
      simp only [hz, tsum_zero]
    linarith
  have hSpos : ∀ a ∈ Set.Ioo (a0 - δ) (a0 + δ), 0 < ∑' c, u c * ka c a * kb c b0 := by
    intro a ha
    have ha' : 0 < a := by linarith [ha.1]
    refine (Summable.of_norm_bounded hM fun c =>
      B00 c a (Set.Ioo_subset_Icc_self ha) b0 hb0C).tsum_pos
      (fun c => mul_nonneg (mul_nonneg (hu c) (hkapos c a ha').le) (hkbpos c b0 hb0).le) c0 ?_
    exact mul_pos (mul_pos hc0 (hkapos c0 a ha')) (hkbpos c0 b0 hb0)
  -- the inner derivative, for a near a0
  have hinner : ∀ a ∈ Set.Ioo (a0 - δ) (a0 + δ),
      HasDerivAt (fun b => ∑' c, u c * ka c a * kb c b) (∑' c, u c * ka c a * deriv (kb c) b0) b0 := by
    intro a ha
    exact hasDerivAt_tsum_of_isPreconnected (u := M) (g := fun c b => u c * ka c a * kb c b)
      (g' := fun c b => u c * ka c a * deriv (kb c) b) hM isOpen_Ioo isPreconnected_Ioo
      (fun c y _ => ((dkb c y).hasDerivAt).const_mul (u c * ka c a))
      (fun c y hy => B01 c a (Set.Ioo_subset_Icc_self ha) y (Set.Ioo_subset_Icc_self hy)) hb0I
      (Summable.of_norm_bounded hM fun c => B00 c a (Set.Ioo_subset_Icc_self ha) b0 hb0C) hb0I
  have hev : (fun a => deriv (fun b => Real.log (∑' c, u c * ka c a * kb c b)) b0) =ᶠ[𝓝 a0]
      fun a => (∑' c, u c * ka c a * deriv (kb c) b0) / ∑' c, u c * ka c a * kb c b0 := by
    filter_upwards [Ioo_mem_nhds (show a0 - δ < a0 by linarith) (show a0 < a0 + δ by linarith)] with a ha
    exact ((hinner a ha).log (hSpos a ha).ne').deriv
  rw [hev.deriv_eq]
  -- the outer derivative
  have hP : HasDerivAt (fun a => ∑' c, u c * ka c a * deriv (kb c) b0)
      (∑' c, u c * deriv (ka c) a0 * deriv (kb c) b0) a0 :=
    hasDerivAt_tsum_of_isPreconnected (u := M) (g := fun c a => u c * ka c a * deriv (kb c) b0)
      (g' := fun c a => u c * deriv (ka c) a * deriv (kb c) b0) hM isOpen_Ioo isPreconnected_Ioo
      (fun c x _ => (((dka c x).hasDerivAt).const_mul (u c)).mul_const (deriv (kb c) b0))
      (fun c x hx => B11 c x (Set.Ioo_subset_Icc_self hx) b0 hb0C) ha0I
      (Summable.of_norm_bounded hM fun c => B01 c a0 ha0C b0 hb0C) ha0I
  have hQ : HasDerivAt (fun a => ∑' c, u c * ka c a * kb c b0)
      (∑' c, u c * deriv (ka c) a0 * kb c b0) a0 :=
    hasDerivAt_tsum_of_isPreconnected (u := M) (g := fun c a => u c * ka c a * kb c b0)
      (g' := fun c a => u c * deriv (ka c) a * kb c b0) hM isOpen_Ioo isPreconnected_Ioo
      (fun c x _ => (((dka c x).hasDerivAt).const_mul (u c)).mul_const (kb c b0))
      (fun c x hx => B10 c x (Set.Ioo_subset_Icc_self hx) b0 hb0C) ha0I
      (Summable.of_norm_bounded hM fun c => B00 c a0 ha0C b0 hb0C) ha0I
  rw [(hP.fun_div hQ (hSpos a0 ha0I).ne').deriv]
  -- the weighted covariance
  have hS0ne : (∑' c, u c * ka c a0 * kb c b0) ≠ 0 := hS0.ne'
  have t1 : (∑' c, u c * ka c a0 * kb c b0 / (∑' c', u c' * ka c' a0 * kb c' b0)
        * (deriv (ka c) a0 / ka c a0 * (deriv (kb c) b0 / kb c b0)))
      = (∑' c, u c * deriv (ka c) a0 * deriv (kb c) b0) / ∑' c, u c * ka c a0 * kb c b0 := by
    rw [← tsum_div_const]
    congr 1
    funext c
    have h1 := (hkapos c a0 ha0).ne'
    have h2 := (hkbpos c b0 hb0).ne'
    field
  have t2 : (∑' c, u c * ka c a0 * kb c b0 / (∑' c', u c' * ka c' a0 * kb c' b0)
        * (deriv (ka c) a0 / ka c a0))
      = (∑' c, u c * deriv (ka c) a0 * kb c b0) / ∑' c, u c * ka c a0 * kb c b0 := by
    rw [← tsum_div_const]
    congr 1
    funext c
    have h1 := (hkapos c a0 ha0).ne'
    field
  have t3 : (∑' c, u c * ka c a0 * kb c b0 / (∑' c', u c' * ka c' a0 * kb c' b0)
        * (deriv (kb c) b0 / kb c b0))
      = (∑' c, u c * ka c a0 * deriv (kb c) b0) / ∑' c, u c * ka c a0 * kb c b0 := by
    rw [← tsum_div_const]
    congr 1
    funext c
    have h2 := (hkbpos c b0 hb0).ne'
    field
  simp only [covW]
  rw [t1, t2, t3]
  field

end G2Kernel
