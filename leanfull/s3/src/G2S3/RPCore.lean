/-
G2S3.RPCore (stage S3, Part A1): positive-definite kernels on a finite measure space, the kernel
exp(J * sum_k w_k u_k(y) u_k(y')) with w_k >= 0 and J >= 0, and the abstract reflection-positivity step on a product
X x Y x Y (Fubini over X, positive definiteness for each fixed x).
Paper: Lemma 6.1 (tex l.1726-1738). For a reflection line between two rows the crossing bonds are
J s_x . s_{theta x}, "and reflection positivity holds by the standard expansion of e^{J s_x . s_{theta x}} into
products of components [FILS78]": this module is that expansion (power series, each power a nonnegative
combination of products u(y) u(y')). No harmonic analysis (S1) is used.
-/
import G2Kernel.Proofs.MirrorProof

noncomputable section
open MeasureTheory Real Filter Topology

namespace G2S3

open G2Kernel

/-- Bounded measurable real functions. -/
def BddMeas {Z : Type*} [MeasurableSpace Z] (K : Z → ℝ) : Prop := Measurable K ∧ ∃ C, ∀ z, |K z| ≤ C

/-- A kernel `K` on `Y × Y` is positive definite for `μ` if `∫∫ G(y) G(y') K(y, y') ≥ 0` for every bounded
measurable `G`. -/
def PDKernel {Y : Type*} [MeasurableSpace Y] (μ : Measure Y) (K : Y × Y → ℝ) : Prop :=
  ∀ G : Y → ℝ, Measurable G → (∃ C, ∀ y, |G y| ≤ C) →
    0 ≤ ∫ p, G p.1 * G p.2 * K p ∂(μ.prod μ)

section PD

variable {Y : Type*} [MeasurableSpace Y] (μ : Measure Y) [IsFiniteMeasure μ]

theorem BddMeas.mul {Z : Type*} [MeasurableSpace Z] {f g : Z → ℝ} (hf : BddMeas f) (hg : BddMeas g) :
    BddMeas (fun z => f z * g z) := by
  obtain ⟨hfm, Cf, hCf⟩ := hf
  obtain ⟨hgm, Cg, hCg⟩ := hg
  refine ⟨hfm.mul hgm, Cf * Cg, fun z => ?_⟩
  rw [abs_mul]
  exact mul_le_mul (hCf z) (hCg z) (abs_nonneg _) ((abs_nonneg _).trans (hCf z))

theorem BddMeas.add {Z : Type*} [MeasurableSpace Z] {f g : Z → ℝ} (hf : BddMeas f) (hg : BddMeas g) :
    BddMeas (fun z => f z + g z) := by
  obtain ⟨hfm, Cf, hCf⟩ := hf
  obtain ⟨hgm, Cg, hCg⟩ := hg
  exact ⟨hfm.add hgm, Cf + Cg, fun z => (abs_add_le _ _).trans (add_le_add (hCf z) (hCg z))⟩

theorem BddMeas.const_mul {Z : Type*} [MeasurableSpace Z] {f : Z → ℝ} (hf : BddMeas f) (c : ℝ) :
    BddMeas (fun z => c * f z) :=
  BddMeas.mul ⟨measurable_const, |c|, fun _ => le_refl _⟩ hf

theorem BddMeas.const {Z : Type*} [MeasurableSpace Z] (c : ℝ) : BddMeas (fun _ : Z => c) :=
  ⟨measurable_const, |c|, fun _ => le_refl _⟩

theorem BddMeas.pow {Z : Type*} [MeasurableSpace Z] {f : Z → ℝ} (hf : BddMeas f) (m : ℕ) :
    BddMeas (fun z => f z ^ m) := by
  induction m with
  | zero => simpa using BddMeas.const (Z := Z) 1
  | succ m ih =>
    have h := ih.mul hf
    simpa [pow_succ] using h

theorem BddMeas.sum {Z ι : Type*} [MeasurableSpace Z] (s : Finset ι) {f : ι → Z → ℝ}
    (hf : ∀ i ∈ s, BddMeas (f i)) : BddMeas (fun z => ∑ i ∈ s, f i z) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using BddMeas.const (Z := Z) 0
  | insert a s ha ih =>
    have h1 := hf a (Finset.mem_insert_self a s)
    have h2 := ih (fun i hi => hf i (Finset.mem_insert_of_mem hi))
    have h := h1.add h2
    simpa [Finset.sum_insert ha] using h

theorem BddMeas.integrable {Z : Type*} [MeasurableSpace Z] {ν : Measure Z} [IsFiniteMeasure ν] {f : Z → ℝ}
    (hf : BddMeas f) : Integrable f ν := by
  obtain ⟨hfm, C, hC⟩ := hf
  exact integrable_of_abs_le hfm C hC

theorem BddMeas.comp {Z W : Type*} [MeasurableSpace Z] [MeasurableSpace W] {f : Z → ℝ} (hf : BddMeas f)
    {φ : W → Z} (hφ : Measurable φ) : BddMeas (fun w => f (φ w)) := by
  obtain ⟨hfm, C, hC⟩ := hf
  exact ⟨hfm.comp hφ, C, fun w => hC (φ w)⟩

theorem pd_one : PDKernel μ (fun _ => 1) := by
  intro G _ _
  simp only [mul_one]
  rw [integral_prod_mul (μ := μ) (ν := μ) G G]
  exact mul_self_nonneg _

theorem pd_mul_rank1 {K : Y × Y → ℝ} (hK : PDKernel μ K) {u : Y → ℝ} (hu : BddMeas u) :
    PDKernel μ (fun p => K p * (u p.1 * u p.2)) := by
  intro G hG hGb
  obtain ⟨CG, hCG⟩ := hGb
  obtain ⟨hum, Cu, hCu⟩ := hu
  have h := hK (fun y => G y * u y) (hG.mul hum) ⟨CG * Cu, fun y => by
    rw [abs_mul]
    exact mul_le_mul (hCG y) (hCu y) (abs_nonneg _) ((abs_nonneg _).trans (hCG y))⟩
  have e : (fun p : Y × Y => G p.1 * G p.2 * (K p * (u p.1 * u p.2)))
      = fun p => G p.1 * u p.1 * (G p.2 * u p.2) * K p := by
    funext p
    ring
  rw [e]
  exact h

theorem pd_add {K1 K2 : Y × Y → ℝ} (h1 : PDKernel μ K1) (h2 : PDKernel μ K2) (b1 : BddMeas K1)
    (b2 : BddMeas K2) : PDKernel μ (fun p => K1 p + K2 p) := by
  intro G hG hGb
  have hGG : BddMeas (fun p : Y × Y => G p.1 * G p.2) :=
    BddMeas.mul (⟨hG.comp measurable_fst, hGb.elim fun C hC => ⟨C, fun p => hC p.1⟩⟩)
      (⟨hG.comp measurable_snd, hGb.elim fun C hC => ⟨C, fun p => hC p.2⟩⟩)
  have i1 : Integrable (fun p : Y × Y => G p.1 * G p.2 * K1 p) (μ.prod μ) := (hGG.mul b1).integrable
  have i2 : Integrable (fun p : Y × Y => G p.1 * G p.2 * K2 p) (μ.prod μ) := (hGG.mul b2).integrable
  have e : (fun p : Y × Y => G p.1 * G p.2 * (K1 p + K2 p))
      = fun p => G p.1 * G p.2 * K1 p + G p.1 * G p.2 * K2 p := by
    funext p
    ring
  rw [e, integral_add i1 i2]
  exact add_nonneg (h1 G hG hGb) (h2 G hG hGb)

theorem pd_const_mul {K : Y × Y → ℝ} (hK : PDKernel μ K) {c : ℝ} (hc : 0 ≤ c) :
    PDKernel μ (fun p => c * K p) := by
  intro G hG hGb
  have e : (fun p : Y × Y => G p.1 * G p.2 * (c * K p)) = fun p => c * (G p.1 * G p.2 * K p) := by
    funext p
    ring
  rw [e, integral_const_mul]
  exact mul_nonneg hc (hK G hG hGb)

theorem pd_zero : PDKernel μ (fun _ => 0) := by
  intro G _ _
  simp

theorem pd_sum {ι : Type*} (s : Finset ι) {K : ι → Y × Y → ℝ} (hK : ∀ i ∈ s, PDKernel μ (K i))
    (hb : ∀ i ∈ s, BddMeas (K i)) : PDKernel μ (fun p => ∑ i ∈ s, K i p) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using pd_zero μ
  | insert a s ha ih =>
    have h1 := hK a (Finset.mem_insert_self a s)
    have h2 := ih (fun i hi => hK i (Finset.mem_insert_of_mem hi)) (fun i hi => hb i (Finset.mem_insert_of_mem hi))
    have hb2 : BddMeas (fun p => ∑ i ∈ s, K i p) := BddMeas.sum s (fun i hi => hb i (Finset.mem_insert_of_mem hi))
    have h := pd_add μ h1 h2 (hb a (Finset.mem_insert_self a s)) hb2
    simpa [Finset.sum_insert ha] using h

/-- A nonnegative combination of rank-one kernels `u_k(y) u_k(y')`. -/
def rankSum {ι : Type*} (s : Finset ι) (w : ι → ℝ) (u : ι → Y → ℝ) (p : Y × Y) : ℝ :=
  ∑ k ∈ s, w k * (u k p.1 * u k p.2)

theorem rankSum_bdd {ι : Type*} (s : Finset ι) (w : ι → ℝ) {u : ι → Y → ℝ} (hu : ∀ k, BddMeas (u k)) :
    BddMeas (rankSum s w u) :=
  BddMeas.sum s (fun k _ => (BddMeas.mul ((hu k).comp measurable_fst) ((hu k).comp measurable_snd)).const_mul (w k))

theorem pd_rankSum_pow {ι : Type*} (s : Finset ι) {w : ι → ℝ} (hw : ∀ k, 0 ≤ w k) {u : ι → Y → ℝ}
    (hu : ∀ k, BddMeas (u k)) (m : ℕ) : PDKernel μ (fun p => rankSum s w u p ^ m) := by
  induction m with
  | zero => simpa using pd_one μ
  | succ m ih =>
    have hb : BddMeas (fun p => rankSum s w u p ^ m) := (rankSum_bdd s w hu).pow m
    have e : (fun p => rankSum s w u p ^ (m + 1))
        = fun p => ∑ k ∈ s, w k * (rankSum s w u p ^ m * (u k p.1 * u k p.2)) := by
      funext p
      rw [pow_succ, rankSum, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro k _
      ring
    rw [e]
    refine pd_sum μ s (fun k _ => pd_const_mul μ (pd_mul_rank1 μ ih (hu k)) (hw k)) (fun k _ => ?_)
    exact (hb.mul (BddMeas.mul ((hu k).comp measurable_fst) ((hu k).comp measurable_snd))).const_mul (w k)

theorem abs_partial_exp_le (x : ℝ) (M : ℕ) :
    |∑ m ∈ Finset.range M, x ^ m / (m.factorial : ℝ)| ≤ Real.exp |x| := by
  refine (Finset.abs_sum_le_sum_abs _ _).trans ?_
  have e : ∀ m ∈ Finset.range M, |x ^ m / (m.factorial : ℝ)| = |x| ^ m / (m.factorial : ℝ) := by
    intro m _
    rw [abs_div, abs_pow, Nat.abs_cast]
  rw [Finset.sum_congr rfl e]
  exact Real.sum_le_exp_of_nonneg (abs_nonneg x) M

theorem tendsto_partial_exp (x : ℝ) :
    Tendsto (fun M => ∑ m ∈ Finset.range M, x ^ m / (m.factorial : ℝ)) atTop (𝓝 (Real.exp x)) := by
  have h := NormedSpace.expSeries_div_hasSum_exp (𝔸 := ℝ) x
  rw [← Real.exp_eq_exp_ℝ] at h
  exact h.tendsto_sum_nat

/-- **The crossing kernel is positive definite**: `exp(J * sum_k w_k u_k(y) u_k(y'))` with `J ≥ 0`, `w_k ≥ 0`. -/
theorem pd_exp_rankSum {ι : Type*} (s : Finset ι) {w : ι → ℝ} (hw : ∀ k, 0 ≤ w k) {u : ι → Y → ℝ}
    (hu : ∀ k, BddMeas (u k)) {J : ℝ} (hJ : 0 ≤ J) :
    PDKernel μ (fun p => Real.exp (J * rankSum s w u p)) := by
  intro G hG hGb
  obtain ⟨CG0, hCG0⟩ := hGb
  set CG := |CG0| with hCGdef
  have hCG : ∀ y, |G y| ≤ CG := fun y => (hCG0 y).trans (le_abs_self CG0)
  have hC0 : 0 ≤ CG := abs_nonneg _
  obtain ⟨hSm, CS, hCS⟩ := rankSum_bdd s w hu
  set S := rankSum s w u with hSdef
  let T : ℕ → Y × Y → ℝ := fun M p => ∑ m ∈ Finset.range M, (J * S p) ^ m / (m.factorial : ℝ)
  have hTpd : ∀ M, PDKernel μ (T M) := by
    intro M
    have e : T M = fun p => ∑ m ∈ Finset.range M, (J ^ m / (m.factorial : ℝ)) * S p ^ m := by
      funext p
      apply Finset.sum_congr rfl
      intro m _
      rw [mul_pow]
      ring
    rw [e]
    refine pd_sum μ _ (fun m _ => pd_const_mul μ (pd_rankSum_pow μ s hw hu m)
      (div_nonneg (pow_nonneg hJ m) (Nat.cast_nonneg _))) (fun m _ => ?_)
    exact ((rankSum_bdd s w hu).pow m).const_mul _
  have hGm1 : Measurable (fun p : Y × Y => G p.1) := hG.comp measurable_fst
  have hGm2 : Measurable (fun p : Y × Y => G p.2) := hG.comp measurable_snd
  have hTm : ∀ M, Measurable (T M) := fun M =>
    Finset.measurable_sum _ (fun m _ => ((measurable_const.mul hSm).pow_const m).div_const _)
  have hbound : ∀ M p, ‖G p.1 * G p.2 * T M p‖ ≤ CG * CG * Real.exp (J * CS) := by
    intro M p
    rw [Real.norm_eq_abs, abs_mul, abs_mul]
    have hT : |T M p| ≤ Real.exp (J * CS) := by
      refine (abs_partial_exp_le (J * S p) M).trans (Real.exp_le_exp.mpr ?_)
      rw [abs_mul, abs_of_nonneg hJ]
      exact mul_le_mul_of_nonneg_left (hCS p) hJ
    exact mul_le_mul (mul_le_mul (hCG p.1) (hCG p.2) (abs_nonneg _) hC0) hT (abs_nonneg _)
      (mul_nonneg hC0 hC0)
  have hlim := tendsto_integral_of_dominated_convergence (μ := μ.prod μ)
    (F := fun M p => G p.1 * G p.2 * T M p) (f := fun p => G p.1 * G p.2 * Real.exp (J * S p))
    (fun _ => CG * CG * Real.exp (J * CS))
    (fun M => ((hGm1.mul hGm2).mul (hTm M)).aestronglyMeasurable)
    (integrable_const _)
    (fun M => ae_of_all _ (hbound M))
    (ae_of_all _ (fun p => (tendsto_partial_exp (J * S p)).const_mul (G p.1 * G p.2)))
  exact ge_of_tendsto' hlim (fun M => hTpd M G hG ⟨CG, hCG⟩)

end PD

/-- **Abstract reflection-positivity step.** For a positive definite bounded measurable kernel `K` on `Y × Y` and
bounded measurable `g` on `X × Y`, `∫ g(x, y) g(x, y') K(y, y') d(μX ⊗ μ ⊗ μ) ≥ 0`. -/
theorem rp_prod {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y] (μX : Measure X) [IsFiniteMeasure μX]
    (μ : Measure Y) [IsFiniteMeasure μ] {K : Y × Y → ℝ} (hK : PDKernel μ K) (hKb : BddMeas K)
    {g : X × Y → ℝ} (hg : BddMeas g) :
    0 ≤ ∫ q, g (q.1, q.2.1) * g (q.1, q.2.2) * K q.2 ∂(μX.prod (μ.prod μ)) := by
  have hint : Integrable (fun q : X × (Y × Y) => g (q.1, q.2.1) * g (q.1, q.2.2) * K q.2) (μX.prod (μ.prod μ)) :=
    (((hg.comp (measurable_fst.prodMk (measurable_fst.comp measurable_snd))).mul
      (hg.comp (measurable_fst.prodMk (measurable_snd.comp measurable_snd)))).mul
      (hKb.comp measurable_snd)).integrable
  rw [integral_prod _ hint]
  refine integral_nonneg (fun x => ?_)
  obtain ⟨hgm, C, hC⟩ := hg
  exact hK (fun y => g (x, y)) (hgm.comp measurable_prodMk_left) ⟨C, fun y => hC (x, y)⟩

end G2S3

#print axioms G2S3.pd_exp_rankSum
#print axioms G2S3.rp_prod
