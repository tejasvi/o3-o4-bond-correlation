/-
G2S1.RankTie (stage S1, tie of d_ℓ): d_ℓ is the rank of the projection with kernel Π_ℓ.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1: "The orthogonal projection
onto H_ℓ in L²(ω) is the integral operator with kernel Π_ℓ(σ, σ') = d_ℓ C̃_ℓ(σ·σ')", H_ℓ of dimension d_ℓ.
- `zonalSpan N l` = span of the functions z ↦ Π_ℓ(x, z); `projOp N l f x` = ∫ Π_ℓ(x, z) f(z) ω(dz).
- `projOp_of_mem`: P_ℓ is the identity on zonalSpan (display (2)); `projOp_mem`: P_ℓ maps continuous functions into
  zonalSpan; so zonalSpan is the range of P_ℓ on continuous functions and P_ℓ ∘ P_ℓ = P_ℓ there.
- `finrank_zonalSpan`: dim zonalSpan = d_ℓ. Proof: zonalSpan is finite-dimensional (inside the span of the coordinate
  monomials of degree ≤ ℓ); the form ∫ f g dω is positive definite on it (reproducing property); in a basis b with Gram
  matrix A, Π_ℓ(x, ·) = Σ_j c_j(x) b_j with A c(x) = b(x), and d_ℓ = ∫ Π_ℓ(x, x) ω(dx) = tr(A⁻¹ A) = dim.
-/
import G2S1.Zonal

noncomputable section
open Real Finset MeasureTheory

namespace G2Kernel

/-- the span of the zonal functions z ↦ Π_ℓ(x, z), x ∈ S^{N-1} -/
def zonalSpan (N l : ℕ) : Submodule ℝ (Sph N → ℝ) :=
  Submodule.span ℝ (Set.range fun x : Sph N => fun z : Sph N => zonal N l x z)

/-- the integral operator with kernel Π_ℓ -/
def projOp (N l : ℕ) (f : Sph N → ℝ) : Sph N → ℝ := fun x => ∫ z, zonal N l x z * f z ∂(omega N)

theorem zfun_mem (N l : ℕ) (x : Sph N) : (fun z : Sph N => zonal N l x z) ∈ zonalSpan N l :=
  Submodule.subset_span ⟨x, rfl⟩

theorem continuous_of_mem_zonalSpan {N l : ℕ} {f : Sph N → ℝ} (hf : f ∈ zonalSpan N l) : Continuous f := by
  induction hf using Submodule.span_induction with
  | mem g hg =>
    obtain ⟨x, rfl⟩ := hg
    exact continuous_zonal_right N l x
  | zero => exact continuous_const
  | add f g _ _ hf hg => exact hf.add hg
  | smul c f _ hf => exact hf.const_smul c

theorem integrable_of_continuous_sph {N : ℕ} (hN : 2 ≤ N) {g : Sph N → ℝ} (hg : Continuous g) :
    Integrable g (omega N) := by
  have := omega_isProbabilityMeasure N (by omega)
  obtain ⟨x, -, -⟩ := exists_dot_eq hN (show (0 : ℝ) ∈ Set.Icc (-1 : ℝ) 1 from ⟨by norm_num, by norm_num⟩)
  obtain ⟨z0, -, hz0⟩ := isCompact_univ.exists_isMaxOn ⟨x, Set.mem_univ x⟩ hg.abs.continuousOn
  exact integrable_of_abs_le hg.measurable (|g z0|) (fun z => isMaxOn_iff.mp hz0 z (Set.mem_univ z))

/-! ### The reproducing property -/

theorem projOp_zfun {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (y : Sph N) :
    projOp N l (fun z => zonal N l y z) = fun z => zonal N l y z := by
  funext x
  unfold projOp
  have h := zonal_proj hN l l x y
  rw [if_pos rfl] at h
  have e : (fun z => zonal N l x z * zonal N l y z) = fun z => zonal N l x z * zonal N l z y := by
    funext z; rw [zonal_symm N l y z]
  rw [e, h, zonal_symm]

/-- P_ℓ is the identity on the span of the zonal functions -/
theorem projOp_of_mem (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {f : Sph N → ℝ} (hf : f ∈ zonalSpan N l) :
    projOp N l f = f := by
  induction hf using Submodule.span_induction with
  | mem g hg =>
    obtain ⟨y, rfl⟩ := hg
    exact projOp_zfun hN l y
  | zero =>
    funext x
    simp [projOp]
  | add f g hf hg ihf ihg =>
    funext x
    have hfc := continuous_of_mem_zonalSpan hf
    have hgc := continuous_of_mem_zonalSpan hg
    have i1 : Integrable (fun z => zonal N l x z * f z) (omega N) :=
      integrable_of_continuous_sph hN ((continuous_zonal_right N l x).mul hfc)
    have i2 : Integrable (fun z => zonal N l x z * g z) (omega N) :=
      integrable_of_continuous_sph hN ((continuous_zonal_right N l x).mul hgc)
    have e1 := congrFun ihf x
    have e2 := congrFun ihg x
    unfold projOp at e1 e2 ⊢
    simp only [Pi.add_apply, mul_add]
    rw [integral_add i1 i2, e1, e2]
  | smul c f hf ihf =>
    funext x
    have e1 := congrFun ihf x
    unfold projOp at e1 ⊢
    simp only [Pi.smul_apply, smul_eq_mul]
    have e : (fun z => zonal N l x z * (c * f z)) = fun z => c * (zonal N l x z * f z) := by
      funext z; ring
    rw [e, integral_const_mul, e1]

/-! ### Finite dimension -/

theorem dot_eq_sum {N : ℕ} (x z : Sph N) : dot x z = ∑ i, (x : Amb N) i * (z : Amb N) i := by
  unfold dot
  simp only [PiLp.inner_apply, RCLike.inner_apply, conj_trivial]
  exact Finset.sum_congr rfl (fun i _ => mul_comm _ _)

/-- the coordinate monomials z_{i_1} ⋯ z_{i_p}, p ≤ ℓ -/
def monoF (N l : ℕ) (q : Σ p : Fin (l + 1), (Fin p → Fin N)) : Sph N → ℝ :=
  fun z => ∏ k, (z : Amb N) (q.2 k)

theorem zfun_mem_monoSpan (N l : ℕ) (x : Sph N) :
    (fun z : Sph N => zonal N l x z) ∈ Submodule.span ℝ (Set.range (monoF N l)) := by
  have hexp : (fun z : Sph N => zonal N l x z)
      = ∑ p : Fin (l + 1), ∑ i : Fin p → Fin N,
          ((zonPoly N l).coeff p * ∏ k, (x : Amb N) (i k)) • monoF N l ⟨p, i⟩ := by
    funext z
    rw [zonal_eq_zon, zon_eq_sum, ← Fin.sum_univ_eq_sum_range]
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, monoF]
    refine Finset.sum_congr rfl (fun p _ => ?_)
    rw [dot_eq_sum, ← Fin.prod_const, Finset.prod_univ_sum, Finset.mul_sum]
    refine Finset.sum_congr (by simp) (fun i _ => ?_)
    rw [Finset.prod_mul_distrib]
    ring
  rw [hexp]
  refine Submodule.sum_mem _ (fun p _ => Submodule.sum_mem _ (fun i _ => Submodule.smul_mem _ _ ?_))
  exact Submodule.subset_span ⟨⟨p, i⟩, rfl⟩

/-- the span is finite-dimensional, for every N (an instance; the stated version had the premise 2 ≤ N) -/
instance finiteDimensional_zonalSpan (N l : ℕ) : FiniteDimensional ℝ (zonalSpan N l) := by
  have hW : FiniteDimensional ℝ (Submodule.span ℝ (Set.range (monoF N l))) :=
    FiniteDimensional.span_of_finite ℝ (Set.finite_range _)
  have hle : zonalSpan N l ≤ Submodule.span ℝ (Set.range (monoF N l)) := by
    rw [zonalSpan, Submodule.span_le]
    rintro _ ⟨x, rfl⟩
    exact zfun_mem_monoSpan N l x
  exact Submodule.finiteDimensional_of_le hle

/-! ### Positive definiteness of ∫ f g dω on the span -/

theorem eq_zero_of_mem_of_integral_sq {N : ℕ} (hN : 2 ≤ N) (l : ℕ) {f : Sph N → ℝ} (hf : f ∈ zonalSpan N l)
    (h0 : ∫ z, f z * f z ∂(omega N) = 0) : f = 0 := by
  have hc := continuous_of_mem_zonalSpan hf
  have hint := integrable_of_continuous_sph hN (hc.mul hc)
  have hae : (fun z => f z * f z) =ᵐ[omega N] 0 :=
    (integral_eq_zero_iff_of_nonneg (fun z => mul_self_nonneg (f z)) hint).mp h0
  have hae' : ∀ᵐ z ∂(omega N), f z = 0 := hae.mono (fun z hz => mul_self_eq_zero.mp hz)
  funext x
  rw [← projOp_of_mem N hN l hf]
  unfold projOp
  rw [integral_eq_zero_of_ae]
  · rfl
  · filter_upwards [hae'] with z hz
    rw [hz, mul_zero]
    rfl

/-! ### The Gram matrix and the trace -/

/-- the dimension of the span -/
abbrev zdim (N l : ℕ) : ℕ := Module.finrank ℝ (zonalSpan N l)

/-- a basis of the span -/
def zB (N l : ℕ) : Module.Basis (Fin (zdim N l)) ℝ (zonalSpan N l) := Module.finBasis ℝ (zonalSpan N l)

/-- the basis functions -/
def zb (N l : ℕ) (j : Fin (zdim N l)) : Sph N → ℝ := ((zB N l j : zonalSpan N l) : Sph N → ℝ)

theorem zb_mem (N l : ℕ) (j : Fin (zdim N l)) : zb N l j ∈ zonalSpan N l := (zB N l j).2

theorem continuous_zb (N l : ℕ) (j : Fin (zdim N l)) : Continuous (zb N l j) :=
  continuous_of_mem_zonalSpan (zb_mem N l j)

/-- the Gram matrix A_ij = ∫ b_i b_j dω -/
def gramZ (N l : ℕ) : Matrix (Fin (zdim N l)) (Fin (zdim N l)) ℝ :=
  fun i j => ∫ z, zb N l i z * zb N l j z ∂(omega N)

/-- the coordinates of Π_ℓ(x, ·) in the basis -/
def zc (N l : ℕ) (x : Sph N) (j : Fin (zdim N l)) : ℝ :=
  (zB N l).repr ⟨fun z => zonal N l x z, zfun_mem N l x⟩ j

theorem coe_sum_smul (N l : ℕ) (c : Fin (zdim N l) → ℝ) (z : Sph N) :
    ((∑ j, c j • zB N l j : zonalSpan N l) : Sph N → ℝ) z = ∑ j, c j * zb N l j z := by
  rw [Submodule.coe_sum]
  simp only [Finset.sum_apply, Submodule.coe_smul, Pi.smul_apply, smul_eq_mul, zb]

/-- Π_ℓ(x, z) = Σ_j c_j(x) b_j(z) -/
theorem zonal_expand (N l : ℕ) (x z : Sph N) : zonal N l x z = ∑ j, zc N l x j * zb N l j z := by
  have h := (zB N l).sum_repr ⟨fun z => zonal N l x z, zfun_mem N l x⟩
  have h2 := congrArg (fun v : zonalSpan N l => (v : Sph N → ℝ) z) h
  simp only at h2
  rw [coe_sum_smul] at h2
  exact h2.symm

theorem integrable_zb_mul {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (i j : Fin (zdim N l)) :
    Integrable (fun z => zb N l i z * zb N l j z) (omega N) :=
  integrable_of_continuous_sph hN ((continuous_zb N l i).mul (continuous_zb N l j))

/-- A c(x) = b(x) -/
theorem gram_mulVec_zc {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (x : Sph N) :
    (gramZ N l).mulVec (zc N l x) = fun k => zb N l k x := by
  funext k
  have hrep := congrFun (projOp_of_mem N hN l (zb_mem N l k)) x
  unfold projOp at hrep
  rw [← hrep]
  simp only [Matrix.mulVec, dotProduct, gramZ]
  have e : (fun z => zonal N l x z * zb N l k z) = fun z => ∑ j, zc N l x j * (zb N l j z * zb N l k z) := by
    funext z
    rw [zonal_expand N l x z, Finset.sum_mul]
    exact Finset.sum_congr rfl (fun j _ => by ring)
  rw [e, integral_finset_sum _ (fun j _ => (integrable_zb_mul hN l j k).const_mul _)]
  refine Finset.sum_congr rfl (fun j _ => ?_)
  rw [integral_const_mul]
  have : ∫ z, zb N l k z * zb N l j z ∂(omega N) = ∫ z, zb N l j z * zb N l k z ∂(omega N) := by
    congr 1; funext z; ring
  rw [this]
  ring

theorem gram_det_ne_zero {N : ℕ} (hN : 2 ≤ N) (l : ℕ) : (gramZ N l).det ≠ 0 := by
  intro hdet
  obtain ⟨v, hv0, hv⟩ := Matrix.exists_mulVec_eq_zero_iff.mpr hdet
  apply hv0
  set g : Sph N → ℝ := fun z => ∑ j, v j * zb N l j z with hg
  have hgmem : g ∈ zonalSpan N l := by
    have : g = ((∑ j, v j • zB N l j : zonalSpan N l) : Sph N → ℝ) := by
      funext z; rw [coe_sum_smul]
    rw [this]
    exact (∑ j, v j • zB N l j).2
  have hq : ∫ z, g z * g z ∂(omega N) = 0 := by
    have e : (fun z => g z * g z) = fun z => ∑ i, ∑ j, v i * v j * (zb N l i z * zb N l j z) := by
      funext z
      simp only [hg, Finset.sum_mul_sum]
      exact Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun j _ => by ring))
    rw [e, integral_finset_sum _ (fun i _ => integrable_finset_sum _
      (fun j _ => (integrable_zb_mul hN l i j).const_mul _))]
    have hz : ∀ i, ∑ j, v i * v j * gramZ N l i j = 0 := by
      intro i
      have h := congrFun hv i
      simp only [Matrix.mulVec, dotProduct, Pi.zero_apply] at h
      calc ∑ j, v i * v j * gramZ N l i j = v i * ∑ j, gramZ N l i j * v j := by
            rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun j _ => by ring)
        _ = 0 := by rw [h, mul_zero]
    calc ∑ i, ∫ z, ∑ j, v i * v j * (zb N l i z * zb N l j z) ∂(omega N)
        = ∑ i, ∑ j, v i * v j * gramZ N l i j := by
          refine Finset.sum_congr rfl (fun i _ => ?_)
          rw [integral_finset_sum _ (fun j _ => (integrable_zb_mul hN l i j).const_mul _)]
          exact Finset.sum_congr rfl (fun j _ => by rw [integral_const_mul]; rfl)
      _ = 0 := Finset.sum_eq_zero (fun i _ => hz i)
  have hg0 := eq_zero_of_mem_of_integral_sq hN l hgmem hq
  have hsum : (∑ j, v j • zB N l j : zonalSpan N l) = 0 := by
    apply Subtype.ext
    funext z
    rw [coe_sum_smul]
    exact congrFun hg0 z
  funext j
  exact Fintype.linearIndependent_iff.mp (zB N l).linearIndependent v hsum j

/-- c(x) = A⁻¹ b(x) -/
theorem zc_eq {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (x : Sph N) :
    zc N l x = (gramZ N l)⁻¹.mulVec (fun k => zb N l k x) := by
  have hu : IsUnit (gramZ N l).det := isUnit_iff_ne_zero.mpr (gram_det_ne_zero hN l)
  rw [← gram_mulVec_zc hN l x, Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ hu, Matrix.one_mulVec]

/-- **d_ℓ is the dimension of the span of the zonal functions**, the range of the projection P_ℓ -/
theorem finrank_zonalSpan (N : ℕ) (hN : 2 ≤ N) (l : ℕ) : (Module.finrank ℝ (zonalSpan N l) : ℝ) = dConc N l := by
  have := omega_isProbabilityMeasure N (by omega)
  have hu : IsUnit (gramZ N l).det := isUnit_iff_ne_zero.mpr (gram_det_ne_zero hN l)
  -- ∫ Π_ℓ(x, x) ω(dx) = d_ℓ
  have h1 : ∫ x, zonal N l x x ∂(omega N) = dConc N l := by
    simp only [zonal_self hN, integral_const, smul_eq_mul, probReal_univ, one_mul]
  -- and = tr(A⁻¹ A)
  have h2 : ∫ x, zonal N l x x ∂(omega N) = ∑ j, ∑ k, (gramZ N l)⁻¹ j k * gramZ N l k j := by
    have e : (fun x => zonal N l x x) = fun x => ∑ j, ∑ k, (gramZ N l)⁻¹ j k * (zb N l k x * zb N l j x) := by
      funext x
      rw [zonal_expand N l x x, zc_eq hN l x]
      simp only [Matrix.mulVec, dotProduct, Finset.sum_mul]
      exact Finset.sum_congr rfl (fun j _ => Finset.sum_congr rfl (fun k _ => by ring))
    have hint : ∀ j k, Integrable (fun x => (gramZ N l)⁻¹ j k * (zb N l k x * zb N l j x)) (omega N) :=
      fun j k => (integrable_zb_mul hN l k j).const_mul _
    rw [e, integral_finset_sum _ (fun j _ => integrable_finset_sum _ (fun k _ => hint j k))]
    refine Finset.sum_congr rfl (fun j _ => ?_)
    rw [integral_finset_sum _ (fun k _ => hint j k)]
    exact Finset.sum_congr rfl (fun k _ => by rw [integral_const_mul]; rfl)
  have h3 : ∑ j, ∑ k, (gramZ N l)⁻¹ j k * gramZ N l k j = Matrix.trace ((gramZ N l)⁻¹ * gramZ N l) := by
    simp only [Matrix.trace, Matrix.diag, Matrix.mul_apply]
  rw [h3, Matrix.nonsing_inv_mul _ hu, Matrix.trace_one, Fintype.card_fin] at h2
  rw [← h1, h2]

/-- P_ℓ maps continuous functions into the span of the zonal functions -/
theorem projOp_mem (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {f : Sph N → ℝ} (hf : Continuous f) :
    projOp N l f ∈ zonalSpan N l := by
  have hexp : projOp N l f = ∑ j, (∫ z, zb N l j z * f z ∂(omega N)) •
      ∑ k, (gramZ N l)⁻¹ j k • zb N l k := by
    funext x
    unfold projOp
    have e : (fun z => zonal N l x z * f z) = fun z => ∑ j, zc N l x j * (zb N l j z * f z) := by
      funext z
      rw [zonal_expand N l x z, Finset.sum_mul]
      exact Finset.sum_congr rfl (fun j _ => by ring)
    have hint : ∀ j, Integrable (fun z => zc N l x j * (zb N l j z * f z)) (omega N) := fun j =>
      (show Integrable (fun z => zb N l j z * f z) (omega N) from
        integrable_of_continuous_sph hN ((continuous_zb N l j).mul hf)).const_mul _
    rw [e, integral_finset_sum _ (fun j _ => hint j)]
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, integral_const_mul]
    rw [zc_eq hN l x]
    simp only [Matrix.mulVec, dotProduct]
    refine Finset.sum_congr rfl (fun j _ => ?_)
    rw [Finset.sum_mul, Finset.mul_sum]
    exact Finset.sum_congr rfl (fun k _ => by ring)
  rw [hexp]
  exact Submodule.sum_mem _ (fun j _ => Submodule.smul_mem _ _
    (Submodule.sum_mem _ (fun k _ => Submodule.smul_mem _ _ (zb_mem N l k))))

end G2Kernel
