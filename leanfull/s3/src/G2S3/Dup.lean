/-
G2S3.Dup (stage S3, Part B6): the measure-theoretic plumbing of the Ginibre-Dunlop argument.
- `mp_XiC`: from a measure-preserving single-site parametrization Phi : R x (A1 x A2) -> S^{N-1}, the map from the
  duplicated coordinate space Om W (W -> A1) (W -> A2) to Config N W x Config N W is measure preserving.
- `cov_dup`: (int F H w)(int w) - (int F w)(int H w) = 1/2 int int (F - F')(H - H') w w'.
- `integral_cond`: for a rotation-invariant bounded measurable G on Config N V and any unit vector u,
  int G = int over the spins off v of G with the spin at v equal to u (paper, proof of Theorem 3.2: "Cov(F, H)
  equals the covariance under the conditional law given s_b = u, for a fixed unit vector u").
-/
import G2S3.ConeMem
import G2S3.Sphere3

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

/-! ### Rearranging products -/

theorem mp_prodAssoc {α β γ : Type*} [MeasurableSpace α] [MeasurableSpace β] [MeasurableSpace γ]
    (μ : Measure α) (ν : Measure β) (τ : Measure γ) [SFinite μ] [SFinite ν] [SFinite τ] :
    MeasurePreserving MeasurableEquiv.prodAssoc ((μ.prod ν).prod τ) (μ.prod (ν.prod τ)) :=
  ⟨MeasurableEquiv.prodAssoc.measurable, Measure.prodAssoc_prod⟩

/-- `((a, b), (c, d)) ↦ ((a, c), (b, d))` -/
def pppComm (α β γ δ : Type*) [MeasurableSpace α] [MeasurableSpace β] [MeasurableSpace γ]
    [MeasurableSpace δ] : (α × β) × (γ × δ) ≃ᵐ (α × γ) × (β × δ) :=
  MeasurableEquiv.prodAssoc.trans
    ((MeasurableEquiv.prodCongr (MeasurableEquiv.refl α)
      (MeasurableEquiv.prodAssoc.symm.trans
        ((MeasurableEquiv.prodCongr MeasurableEquiv.prodComm (MeasurableEquiv.refl δ)).trans
          MeasurableEquiv.prodAssoc))).trans MeasurableEquiv.prodAssoc.symm)

theorem pppComm_apply {α β γ δ : Type*} [MeasurableSpace α] [MeasurableSpace β] [MeasurableSpace γ]
    [MeasurableSpace δ] (p : (α × β) × (γ × δ)) :
    pppComm α β γ δ p = ((p.1.1, p.2.1), (p.1.2, p.2.2)) := rfl

theorem mp_pppComm {α β γ δ : Type*} [MeasurableSpace α] [MeasurableSpace β] [MeasurableSpace γ]
    [MeasurableSpace δ] (μa : Measure α) (μb : Measure β) (μc : Measure γ) (μd : Measure δ)
    [SFinite μa] [SFinite μb] [SFinite μc] [SFinite μd] :
    MeasurePreserving (pppComm α β γ δ) ((μa.prod μb).prod (μc.prod μd)) ((μa.prod μc).prod (μb.prod μd)) := by
  have h1 := mp_prodAssoc μa μb (μc.prod μd)
  have h2 := (mp_prodAssoc μb μc μd).symm
  have h3 : MeasurePreserving (MeasurableEquiv.prodCongr MeasurableEquiv.prodComm (MeasurableEquiv.refl δ))
      ((μb.prod μc).prod μd) ((μc.prod μb).prod μd) :=
    (Measure.measurePreserving_swap (μ := μb) (ν := μc)).prod (MeasurePreserving.id μd)
  have h4 := mp_prodAssoc μc μb μd
  have h5 := (MeasurePreserving.id μa).prod (h4.comp (h3.comp h2))
  have h6 := (mp_prodAssoc μa μc (μb.prod μd)).symm
  exact h6.comp (h5.comp h1)

/-! ### The transport to the duplicated configuration space -/

section Transport

variable {W : Type*} [Fintype W] {A1 A2 : Type*} [MeasurableSpace A1] [MeasurableSpace A2] {N : ℕ}

/-- The two spin configurations of a point of the duplicated coordinate space. -/
def XiC (Φ : ℝ × (A1 × A2) → Sph N) (ω : Om W (W → A1) (W → A2)) : Config N W × Config N W :=
  (fun x => Φ (ω.1.1 x, (ω.2.1.1 x, ω.2.2.1 x)), fun x => Φ (ω.1.2 x, (ω.2.1.2 x, ω.2.2.2 x)))

theorem mp_XiC (hN : 0 < N) (Φ : ℝ × (A1 × A2) → Sph N) (ν : Measure ℝ) (l1 : Measure A1) (l2 : Measure A2)
    [IsProbabilityMeasure ν] [IsProbabilityMeasure l1] [IsProbabilityMeasure l2]
    (hΦ : MeasurePreserving Φ (ν.prod (l1.prod l2)) (omega N)) :
    MeasurePreserving (XiC Φ) (POm W ν (Measure.pi fun _ : W => l1) (Measure.pi fun _ : W => l2))
      ((freeMeasure N W).prod (freeMeasure N W)) := by
  have := omega_isProbabilityMeasure N hN
  -- inner rearrangement ((a, a'), (b, b')) ↦ ((a, b), (a', b'))
  have hA := (MeasurePreserving.id ((Measure.pi fun _ : W => ν).prod (Measure.pi fun _ : W => ν))).prod
    (mp_pppComm (Measure.pi fun _ : W => l1) (Measure.pi fun _ : W => l1) (Measure.pi fun _ : W => l2)
      (Measure.pi fun _ : W => l2))
  -- outer rearrangement ((r, r'), (q, q')) ↦ ((r, q), (r', q'))
  have hB := mp_pppComm (Measure.pi fun _ : W => ν) (Measure.pi fun _ : W => ν)
    ((Measure.pi fun _ : W => l1).prod (Measure.pi fun _ : W => l2))
    ((Measure.pi fun _ : W => l1).prod (Measure.pi fun _ : W => l2))
  -- (r, (a, b)) ↦ (fun x => (r x, (a x, b x)))
  have hC1 := (measurePreserving_arrowProdEquivProdArrow A1 A2 W (fun _ => l1) (fun _ => l2)).symm
  have hC2 := (measurePreserving_arrowProdEquivProdArrow ℝ (A1 × A2) W (fun _ => ν)
    (fun _ => l1.prod l2)).symm
  have hC := hC2.comp ((MeasurePreserving.id (Measure.pi fun _ : W => ν)).prod hC1)
  have hD := measurePreserving_pi (fun _ : W => ν.prod (l1.prod l2)) (fun _ : W => omega N) (fun _ => hΦ)
  have hE := (hD.comp hC).prod (hD.comp hC)
  have hall := hE.comp (hB.comp hA)
  exact hall

theorem integral_XiC (hN : 0 < N) (Φ : ℝ × (A1 × A2) → Sph N) (ν : Measure ℝ) (l1 : Measure A1)
    (l2 : Measure A2) [IsProbabilityMeasure ν] [IsProbabilityMeasure l1] [IsProbabilityMeasure l2]
    (hΦ : MeasurePreserving Φ (ν.prod (l1.prod l2)) (omega N)) (Ψ : Config N W × Config N W → ℝ)
    (hΨ : Measurable Ψ) :
    ∫ p, Ψ p ∂((freeMeasure N W).prod (freeMeasure N W))
      = ∫ ω, Ψ (XiC Φ ω) ∂(POm W ν (Measure.pi fun _ : W => l1) (Measure.pi fun _ : W => l2)) := by
  have h := mp_XiC hN Φ ν l1 l2 hΦ (W := W)
  rw [← h.map_eq, integral_map h.measurable.aemeasurable hΨ.aestronglyMeasurable]

end Transport

/-! ### The duplicated covariance -/

theorem cov_dup {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ] {F H w : X → ℝ}
    (hF : BddMeas F) (hH : BddMeas H) (hw : BddMeas w) :
    (∫ x, F x * H x * w x ∂μ) * (∫ x, w x ∂μ) - (∫ x, F x * w x ∂μ) * (∫ x, H x * w x ∂μ)
      = (1 / 2) * ∫ p, (F p.1 - F p.2) * (H p.1 - H p.2) * (w p.1 * w p.2) ∂(μ.prod μ) := by
  have b1 : BddMeas (fun x => F x * H x * w x) := (hF.mul hH).mul hw
  have b2 : BddMeas (fun x => F x * w x) := hF.mul hw
  have b3 : BddMeas (fun x => H x * w x) := hH.mul hw
  have t1 : Integrable (fun p : X × X => F p.1 * H p.1 * w p.1 * w p.2) (μ.prod μ) :=
    ((b1.comp measurable_fst).mul (hw.comp measurable_snd)).integrable
  have t2 : Integrable (fun p : X × X => F p.1 * w p.1 * (H p.2 * w p.2)) (μ.prod μ) :=
    ((b2.comp measurable_fst).mul (b3.comp measurable_snd)).integrable
  have t3 : Integrable (fun p : X × X => H p.1 * w p.1 * (F p.2 * w p.2)) (μ.prod μ) :=
    ((b3.comp measurable_fst).mul (b2.comp measurable_snd)).integrable
  have t4 : Integrable (fun p : X × X => w p.1 * (F p.2 * H p.2 * w p.2)) (μ.prod μ) :=
    ((hw.comp measurable_fst).mul (b1.comp measurable_snd)).integrable
  have e : (fun p : X × X => (F p.1 - F p.2) * (H p.1 - H p.2) * (w p.1 * w p.2))
      = fun p => F p.1 * H p.1 * w p.1 * w p.2 - F p.1 * w p.1 * (H p.2 * w p.2)
          - H p.1 * w p.1 * (F p.2 * w p.2) + w p.1 * (F p.2 * H p.2 * w p.2) := by
    funext p
    ring
  have t12 : Integrable (fun p : X × X => F p.1 * H p.1 * w p.1 * w p.2 - F p.1 * w p.1 * (H p.2 * w p.2))
      (μ.prod μ) := t1.sub t2
  have t123 : Integrable (fun p : X × X => F p.1 * H p.1 * w p.1 * w p.2 - F p.1 * w p.1 * (H p.2 * w p.2)
      - H p.1 * w p.1 * (F p.2 * w p.2)) (μ.prod μ) := t12.sub t3
  rw [e, integral_add t123 t4, integral_sub t12 t3, integral_sub t1 t2]
  have i1 : ∫ p : X × X, F p.1 * H p.1 * w p.1 * w p.2 ∂(μ.prod μ)
      = (∫ x, F x * H x * w x ∂μ) * (∫ x, w x ∂μ) :=
    integral_prod_mul (fun x => F x * H x * w x) (fun x => w x)
  have i2 : ∫ p : X × X, F p.1 * w p.1 * (H p.2 * w p.2) ∂(μ.prod μ)
      = (∫ x, F x * w x ∂μ) * (∫ x, H x * w x ∂μ) :=
    integral_prod_mul (fun x => F x * w x) (fun x => H x * w x)
  have i3 : ∫ p : X × X, H p.1 * w p.1 * (F p.2 * w p.2) ∂(μ.prod μ)
      = (∫ x, H x * w x ∂μ) * (∫ x, F x * w x ∂μ) :=
    integral_prod_mul (fun x => H x * w x) (fun x => F x * w x)
  have i4 : ∫ p : X × X, w p.1 * (F p.2 * H p.2 * w p.2) ∂(μ.prod μ)
      = (∫ x, w x ∂μ) * (∫ x, F x * H x * w x ∂μ) :=
    integral_prod_mul (fun x => w x) (fun x => F x * H x * w x)
  rw [i1, i2, i3, i4]
  ring

/-! ### Conditioning on one spin -/

/-- **Conditioning on a spin by rotation invariance.** -/
theorem integral_cond {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] [DecidableEq V] (v : V)
    (G : Config N V → ℝ) (hG : BddMeas G)
    (hGr : ∀ (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V), G (fun i => sphMap R (σ i)) = G σ) (u : Sph N) :
    ∫ σ, G σ ∂(freeMeasure N V)
      = ∫ σ2, G (joinP (fun i => i = v) (fun _ => u) σ2) ∂(Measure.pi fun _ : {i // ¬ i = v} => omega N) := by
  have := omega_isProbabilityMeasure N hN
  obtain ⟨hGm, C, hC⟩ := hG
  rw [integral_split_by hN (fun i => i = v) G hGm C hC]
  set K : ({i // i = v} → Sph N) → ℝ :=
    fun σ1 => ∫ σ2, G (joinP (fun i => i = v) σ1 σ2) ∂(Measure.pi fun _ : {i // ¬ i = v} => omega N) with hK
  have hconst : ∀ σ1, K σ1 = K (fun _ => u) := by
    intro σ1
    obtain ⟨z, hz⟩ : ∃ z : Amb N, z = ((σ1 ⟨v, rfl⟩ : Sph N) : Amb N) := ⟨_, rfl⟩
    have hzn : ‖z‖ = 1 := by rw [hz]; exact norm_eq_of_mem_sphere _
    have hun : ‖(u : Amb N)‖ = 1 := norm_eq_of_mem_sphere _
    obtain ⟨R, hR⟩ : ∃ R : Amb N ≃ₗᵢ[ℝ] Amb N, R = Submodule.reflection (ℝ ∙ (z - (u : Amb N)))ᗮ := ⟨_, rfl⟩
    have hRz : R z = (u : Amb N) := by
      rw [hR]
      exact Submodule.reflection_sub (hzn.trans hun.symm)
    have hjm : Measurable (fun σ2 : {i // ¬ i = v} → Sph N => joinP (fun i => i = v) (fun _ => u) σ2) := by
      refine Measurable.of_eval (fun i => ?_)
      by_cases hi : i = v
      · simp only [joinP, hi, dite_true]
        exact measurable_const
      · simp only [joinP, hi, dite_false]
        exact measurable_pi_apply _
    simp only [hK]
    rw [← integral_reflect_pi hN (hSphereIso_holds N) R
      (fun σ2 => G (joinP (fun i => i = v) (fun _ => u) σ2)) (hGm.comp hjm)]
    congr 1
    funext σ2
    rw [← hGr R (joinP (fun i => i = v) σ1 σ2)]
    congr 1
    funext i
    by_cases hi : i = v
    · rw [joinP_pos (p := fun i => i = v) _ _ hi, joinP_pos (p := fun i => i = v) _ _ hi]
      apply Subtype.ext
      show R ((σ1 ⟨i, hi⟩ : Sph N) : Amb N) = (u : Amb N)
      have e1 : (⟨i, hi⟩ : {i // i = v}) = ⟨v, rfl⟩ := Subtype.ext hi
      rw [e1, ← hz, hRz]
    · rw [joinP_neg (p := fun i => i = v) _ _ hi, joinP_neg (p := fun i => i = v) _ _ hi]
  rw [integral_congr_ae (ae_of_all _ hconst), integral_const, probReal_univ, one_smul]

end G2S3

#print axioms G2S3.mp_XiC
#print axioms G2S3.cov_dup
#print axioms G2S3.integral_cond
