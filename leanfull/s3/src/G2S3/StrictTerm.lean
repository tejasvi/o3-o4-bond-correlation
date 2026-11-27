/-
G2S3.StrictTerm (stage S3, Part B8): the explicit positive term of the strict corner inequality. For distinct sites
x, y, w and the coordinate k,
  int int (s_x^k - s'_x^k)(s_y^k - s'_y^k)(s_x.s_w + s'_x.s'_w)(s_w.s_y + s'_w.s'_y) = 2 / N^3
under the duplicated free measure: four symmetries (sign flips of single spins, exchange of the copies) reduce it to
2 int s_x^k s_y^k (s_x.s_w)(s_w.s_y) = 2 sum_{i,j} (d_ki/N)(d_ij/N)(d_jk/N).
-/
import G2S3.Moments

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

theorem integral_symm {X : Type*} [MeasurableSpace X] {μ : Measure X} [IsFiniteMeasure μ] {φ : X → X}
    (hφ : MeasurePreserving φ μ μ) {F G : X → ℝ} (hF : BddMeas F) (hG : Integrable G μ)
    (h : ∀ x, F x + F (φ x) = 2 * G x) : ∫ x, F x ∂μ = ∫ x, G x ∂μ := by
  have h1 : ∫ x, F (φ x) ∂μ = ∫ x, F x ∂μ := by
    rw [← integral_map hφ.measurable.aemeasurable hF.1.aestronglyMeasurable, hφ.map_eq]
  have h2 : ∫ x, (F x + F (φ x)) ∂μ = ∫ x, 2 * G x ∂μ := integral_congr_ae (ae_of_all _ h)
  rw [integral_add hF.integrable (hF.comp hφ.measurable).integrable, h1, integral_const_mul] at h2
  linarith

section Strict

variable {N : ℕ} {W : Type*} [Fintype W] [DecidableEq W]

/-- the coordinate `k` of the spin at `z` -/
def cf (k : Fin N) (z : W) (σ : Config N W) : ℝ := ((σ z : Sph N) : Amb N) k

theorem cf_bdd (k : Fin N) (z : W) : BddMeas (cf (N := N) k z) :=
  ⟨measurable_coord (measurable_pi_apply z) k, 1, fun σ => abs_coord_le _ k⟩

theorem dotz_bdd (a b : W) : BddMeas (fun σ : Config N W => dot (σ a) (σ b)) :=
  ⟨measurable_bond s(a, b), 1, fun σ => abs_bond_le s(a, b) σ⟩

theorem cf_flipAt_same (k : Fin N) (z : W) (σ : Config N W) : cf k z (flipAt z σ) = -cf k z σ := by
  unfold cf flipAt
  rw [if_pos rfl, negS_coe]
  rfl

theorem cf_flipAt_ne (k : Fin N) {z a : W} (h : a ≠ z) (σ : Config N W) : cf k a (flipAt z σ) = cf k a σ := by
  unfold cf flipAt
  rw [if_neg h]

theorem flipAt_ne {z a : W} (h : a ≠ z) (σ : Config N W) : flipAt z σ a = σ a := by
  unfold flipAt
  rw [if_neg h]

theorem flipAt_same (z : W) (σ : Config N W) : flipAt z σ z = negS (σ z) := by
  unfold flipAt
  rw [if_pos rfl]

/-- **The single-copy term**: `∫ s_x^k s_y^k (s_x.s_w)(s_w.s_y) = 1/N^3`. -/
theorem single_term (hN : 0 < N) (k : Fin N) {x y w : W} (hxy : x ≠ y) (hxw : x ≠ w) (hyw : y ≠ w) :
    ∫ σ, cf k x σ * cf k y σ * dot (σ x) (σ w) * dot (σ w) (σ y) ∂(freeMeasure N W) = 1 / (N : ℝ) ^ 3 := by
  have hprob := omega_isProbabilityMeasure N hN
  haveI : IsProbabilityMeasure (freeMeasure N W) := by unfold freeMeasure; infer_instance
  -- the product form of each summand
  set ψ : Fin N → Fin N → W → Sph N → ℝ := fun i j z s =>
    (if z = x then (s : Amb N) k * (s : Amb N) i else 1) * (if z = w then (s : Amb N) i * (s : Amb N) j else 1)
      * (if z = y then (s : Amb N) j * (s : Amb N) k else 1) with hψ
  have hexp : ∀ σ : Config N W, cf k x σ * cf k y σ * dot (σ x) (σ w) * dot (σ w) (σ y)
      = ∑ i, ∑ j, ∏ z, ψ i j z (σ z) := by
    intro σ
    rw [dot_eq_sum, dot_eq_sum, mul_assoc, Finset.sum_mul_sum, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl (fun j _ => ?_)
    simp only [hψ, Finset.prod_mul_distrib, Finset.prod_ite_eq', Finset.mem_univ, if_true, cf]
    ring
  have hψm : ∀ i j z, Measurable (ψ i j z) := by
    intro i j z
    simp only [hψ]
    refine Measurable.mul (Measurable.mul ?_ ?_) ?_ <;> split_ifs <;>
      first
      | exact measurable_const
      | exact ((continuous_coordA _).mul (continuous_coordA _)).measurable
  have hψb : ∀ i j z s, |ψ i j z s| ≤ 1 := by
    intro i j z s
    have h1 := abs_coord_le s k
    have h2 := abs_coord_le s i
    have h3 := abs_coord_le s j
    simp only [hψ, abs_mul]
    refine mul_le_one₀ (mul_le_one₀ ?_ (abs_nonneg _) ?_) (abs_nonneg _) ?_ <;> split_ifs <;>
      simp only [abs_mul, abs_one, le_refl] <;>
      first
      | exact mul_le_one₀ h1 (abs_nonneg _) h2
      | exact mul_le_one₀ h2 (abs_nonneg _) h3
      | exact mul_le_one₀ h3 (abs_nonneg _) h1
  have hint : ∀ i j, Integrable (fun σ : Config N W => ∏ z, ψ i j z (σ z)) (freeMeasure N W) := by
    intro i j
    refine BddMeas.integrable ⟨Finset.measurable_prod _ (fun z _ => (hψm i j z).comp (measurable_pi_apply z)),
      1, fun σ => ?_⟩
    rw [Finset.abs_prod]
    exact Finset.prod_le_one₀ (fun z _ => abs_nonneg _) (fun z _ => hψb i j z (σ z))
  simp only [hexp]
  rw [integral_finset_sum _ (fun i _ => integrable_finset_sum _ (fun j _ => hint i j))]
  simp_rw [integral_finset_sum _ (fun j _ => hint _ j)]
  -- each summand factorizes over the sites
  have hfac : ∀ i j, ∫ σ, ∏ z, ψ i j z (σ z) ∂(freeMeasure N W)
      = (if k = i then 1 / (N : ℝ) else 0) * (if i = j then 1 / (N : ℝ) else 0)
        * (if j = k then 1 / (N : ℝ) else 0) := by
    intro i j
    unfold freeMeasure
    rw [integral_fintype_prod_eq_prod (fun z s => ψ i j z s)]
    have hz : ∀ z, ∫ s, ψ i j z s ∂(omega N)
        = (if z = x then (if k = i then 1 / (N : ℝ) else 0) else 1)
          * (if z = w then (if i = j then 1 / (N : ℝ) else 0) else 1)
          * (if z = y then (if j = k then 1 / (N : ℝ) else 0) else 1) := by
      intro z
      simp only [hψ]
      by_cases hzx : z = x
      · rw [hzx]
        simp [hxw, hxy, int_coord_mul hN]
      · by_cases hzw : z = w
        · rw [hzw]
          have hwx : w ≠ x := fun h => hxw h.symm
          have hwy : w ≠ y := fun h => hyw h.symm
          simp [hwx, hwy, int_coord_mul hN]
        · by_cases hzy : z = y
          · rw [hzy]
            have hyx : y ≠ x := fun h => hxy h.symm
            simp [hyx, hyw, int_coord_mul hN]
          · simp [hzx, hzw, hzy]
    simp only [hz, Finset.prod_mul_distrib, Finset.prod_ite_eq', Finset.mem_univ, if_true]
  simp only [hfac]
  rw [Finset.sum_eq_single k (fun i _ hi => by simp [Ne.symm hi]) (fun h => absurd (Finset.mem_univ k) h)]
  rw [Finset.sum_eq_single k (fun j _ hj => by simp [hj]) (fun h => absurd (Finset.mem_univ k) h)]
  simp only [if_true]
  ring

end Strict

end G2S3

#print axioms G2S3.single_term
