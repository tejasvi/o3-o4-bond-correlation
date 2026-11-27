/-
G2S3.Moments (stage S3, Part B8): first and second moments of omega and the flips of one spin.
- `int_coord_zero`: int s_i d omega = 0; `int_coord_mul`: int s_i s_j d omega = (if i = j then 1/N else 0), from the
  coordinate reflections and transpositions (linear isometries, S0's hSphereIso_holds) and sum_i s_i^2 = 1.
- `flipAt`: changing the sign of one spin preserves the free measure.
These give the explicit positive term of the strict corner inequality (Corollary 3.8, Cov > 0).
-/
import G2S3.Dunlop

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

/-- The reflection changing the sign of the coordinate `i`. -/
def reflC {N : ℕ} (i : Fin N) : Amb N ≃ₗᵢ[ℝ] Amb N where
  toFun x := WithLp.toLp 2 (fun j => if j = i then -x j else x j)
  invFun x := WithLp.toLp 2 (fun j => if j = i then -x j else x j)
  map_add' x y := by
    ext j
    by_cases h : j = i <;> simp [h] <;> ring
  map_smul' c x := by
    ext j
    by_cases h : j = i <;> simp [h]
  left_inv x := by
    ext j
    by_cases h : j = i <;> simp [h]
  right_inv x := by
    ext j
    by_cases h : j = i <;> simp [h]
  norm_map' x := by
    rw [EuclideanSpace.norm_eq, EuclideanSpace.norm_eq]
    congr 1
    refine Finset.sum_congr rfl (fun j _ => ?_)
    by_cases h : j = i <;> simp [h]

theorem reflC_apply {N : ℕ} (i j : Fin N) (x : Amb N) : (reflC i x) j = if j = i then -x j else x j := rfl

/-- The transposition of the coordinates `i` and `j`. -/
def swapC {N : ℕ} (i j : Fin N) : Amb N ≃ₗᵢ[ℝ] Amb N where
  toFun x := WithLp.toLp 2 (fun k => x (Equiv.swap i j k))
  invFun x := WithLp.toLp 2 (fun k => x (Equiv.swap i j k))
  map_add' x y := by ext k; simp
  map_smul' c x := by ext k; simp
  left_inv x := by ext k; simp
  right_inv x := by ext k; simp
  norm_map' x := by
    rw [EuclideanSpace.norm_eq, EuclideanSpace.norm_eq]
    congr 1
    exact Equiv.sum_comp (Equiv.swap i j) (fun k => ‖x k‖ ^ 2)

theorem swapC_apply {N : ℕ} (i j k : Fin N) (x : Amb N) : (swapC i j x) k = x (Equiv.swap i j k) := rfl

theorem integral_sphMap {N : ℕ} (hN : 0 < N) (R : Amb N ≃ₗᵢ[ℝ] Amb N) (f : Sph N → ℝ) (hf : Measurable f) :
    ∫ s, f (sphMap R s) ∂(omega N) = ∫ s, f s ∂(omega N) := by
  have := omega_isProbabilityMeasure N hN
  have hmp : MeasurePreserving (sphMap R) (omega N) (omega N) := hSphereIso_holds N R
  rw [← integral_map hmp.measurable.aemeasurable hf.aestronglyMeasurable, hmp.map_eq]

theorem int_coord_zero {N : ℕ} (hN : 0 < N) (i : Fin N) : ∫ s, (s : Amb N) i ∂(omega N) = 0 := by
  have h := integral_sphMap hN (reflC i) (fun s => (s : Amb N) i) (continuous_coordA i).measurable
  have e : ∀ s : Sph N, ((sphMap (reflC i) s : Sph N) : Amb N) i = -(s : Amb N) i := by
    intro s
    show (reflC i (s : Amb N)) i = _
    rw [reflC_apply, if_pos rfl]
  simp only [e, integral_neg] at h
  linarith

theorem int_coord_mul_ne {N : ℕ} (hN : 0 < N) {i j : Fin N} (hij : i ≠ j) :
    ∫ s, (s : Amb N) i * (s : Amb N) j ∂(omega N) = 0 := by
  have h := integral_sphMap hN (reflC i) (fun s => (s : Amb N) i * (s : Amb N) j)
    ((continuous_coordA i).mul (continuous_coordA j)).measurable
  have e : ∀ s : Sph N, ((sphMap (reflC i) s : Sph N) : Amb N) i * ((sphMap (reflC i) s : Sph N) : Amb N) j
      = -((s : Amb N) i * (s : Amb N) j) := by
    intro s
    show (reflC i (s : Amb N)) i * (reflC i (s : Amb N)) j = _
    rw [reflC_apply, reflC_apply, if_pos rfl, if_neg (Ne.symm hij)]
    ring
  simp only [e, integral_neg] at h
  linarith

theorem int_coord_sq {N : ℕ} (hN : 0 < N) (i : Fin N) :
    ∫ s, (s : Amb N) i * (s : Amb N) i ∂(omega N) = 1 / (N : ℝ) := by
  have := omega_isProbabilityMeasure N hN
  have hsame : ∀ j : Fin N, ∫ s, (s : Amb N) j * (s : Amb N) j ∂(omega N)
      = ∫ s, (s : Amb N) i * (s : Amb N) i ∂(omega N) := by
    intro j
    have h := integral_sphMap hN (swapC i j) (fun s => (s : Amb N) j * (s : Amb N) j)
      ((continuous_coordA j).mul (continuous_coordA j)).measurable
    have e : ∀ s : Sph N, ((sphMap (swapC i j) s : Sph N) : Amb N) j * ((sphMap (swapC i j) s : Sph N) : Amb N) j
        = (s : Amb N) i * (s : Amb N) i := by
      intro s
      show (swapC i j (s : Amb N)) j * (swapC i j (s : Amb N)) j = _
      rw [swapC_apply, Equiv.swap_apply_right]
    simp only [e] at h
    exact h.symm
  have hsum : ∑ j : Fin N, ∫ s, (s : Amb N) j * (s : Amb N) j ∂(omega N) = 1 := by
    rw [← integral_finset_sum _ (fun j _ => (BddMeas.integrable (ν := omega N)
      (f := fun s : Sph N => (s : Amb N) j * (s : Amb N) j)
      ⟨((continuous_coordA j).mul (continuous_coordA j)).measurable, 1, fun s => by
        rw [abs_mul]
        exact mul_le_one₀ (abs_coord_le s j) (abs_nonneg _) (abs_coord_le s j)⟩))]
    have e : ∀ s : Sph N, ∑ j : Fin N, (s : Amb N) j * (s : Amb N) j = 1 := by
      intro s
      have := sph_sum_sq s
      simpa [sq] using this
    simp only [e, integral_const, probReal_univ, one_smul]
  simp only [hsame, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hsum
  have hN' : (N : ℝ) ≠ 0 := by exact_mod_cast hN.ne'
  rw [eq_div_iff hN']
  linarith

theorem int_coord_mul {N : ℕ} (hN : 0 < N) (i j : Fin N) :
    ∫ s, (s : Amb N) i * (s : Amb N) j ∂(omega N) = if i = j then 1 / (N : ℝ) else 0 := by
  by_cases h : i = j
  · subst h
    rw [if_pos rfl, int_coord_sq hN]
  · rw [if_neg h, int_coord_mul_ne hN h]

/-! ### Flipping one spin -/

/-- The sign change of one coordinate vector: `s ↦ -s` on the sphere. -/
def negS {N : ℕ} (s : Sph N) : Sph N := sphMap (LinearIsometryEquiv.neg ℝ) s

theorem negS_coe {N : ℕ} (s : Sph N) : ((negS s : Sph N) : Amb N) = -(s : Amb N) := rfl

/-- Change the sign of the spin at `z`. -/
def flipAt {N : ℕ} {W : Type*} [DecidableEq W] (z : W) (σ : Config N W) : Config N W :=
  fun k => if k = z then negS (σ k) else σ k

theorem flipAt_mp {N : ℕ} (hN : 0 < N) {W : Type*} [Fintype W] [DecidableEq W] (z : W) :
    MeasurePreserving (flipAt (N := N) z) (freeMeasure N W) (freeMeasure N W) := by
  have := omega_isProbabilityMeasure N hN
  have h : ∀ k : W, MeasurePreserving (fun s : Sph N => if k = z then negS s else s) (omega N) (omega N) := by
    intro k
    by_cases hk : k = z
    · simp only [hk, if_true]
      exact hSphereIso_holds N (LinearIsometryEquiv.neg ℝ)
    · simp only [hk, if_false]
      exact MeasurePreserving.id _
  exact measurePreserving_pi (fun _ : W => omega N) (fun _ : W => omega N) h

theorem dot_negS_left {N : ℕ} (s t : Sph N) : dot (negS s) t = -dot s t := by
  unfold dot
  rw [negS_coe, inner_neg_left]

theorem dot_negS_right {N : ℕ} (s t : Sph N) : dot s (negS t) = -dot s t := by
  unfold dot
  rw [negS_coe, inner_neg_right]

end G2S3

#print axioms G2S3.int_coord_mul
#print axioms G2S3.flipAt_mp
