/-
G2S1.Zonal (stage S1): the zonal kernel Π_ℓ(σ, τ) = d_ℓ C̃_ℓ(σ · τ) on the sphere and the facts exported to the other
stages (the interface of stage S1): display (2), display (3) on the sphere, |C̃_ℓ| ≤ 1 on [-1, 1] (from (2) by
Cauchy-Schwarz), the paper's integral formula for k_ℓ, positive definiteness of Π_ℓ, and the identity for
integrating out a vertex of degree two.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1.
-/
import G2S1.Expand

noncomputable section
open Real Finset MeasureTheory

namespace G2Kernel

/-- Π_ℓ(σ, τ) = d_ℓ C̃_ℓ(σ · τ) -/
def zonal (N l : ℕ) (x y : Sph N) : ℝ := dConc N l * CConc N l (dot x y)

theorem zonal_eq_zon (N l : ℕ) (x y : Sph N) : zonal N l x y = zon N l (dot x y) := rfl

theorem zonal_symm (N l : ℕ) (x y : Sph N) : zonal N l x y = zonal N l y x := by
  unfold zonal; rw [dot_comm]

theorem zonal_self {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (x : Sph N) : zonal N l x x = dConc N l := by
  unfold zonal; rw [dot_self, CConc_one N hN, mul_one]

theorem continuous_CConc (N n : ℕ) : Continuous (CConc N n) := by
  have h : CConc N n = fun t => (cPoly N n).eval t := by funext t; rw [eval_cPoly]
  rw [h]; exact (cPoly N n).continuous

theorem continuous_zonal (N l : ℕ) : Continuous (fun p : Sph N × Sph N => zonal N l p.1 p.2) := by
  unfold zonal dot
  exact continuous_const.mul ((continuous_CConc N l).comp
    ((continuous_subtype_val.comp continuous_fst).inner (continuous_subtype_val.comp continuous_snd)))

theorem continuous_zonal_right (N l : ℕ) (x : Sph N) : Continuous (fun z : Sph N => zonal N l x z) :=
  (continuous_zonal N l).comp (continuous_const.prodMk continuous_id)

theorem continuous_zonal_left (N l : ℕ) (y : Sph N) : Continuous (fun z : Sph N => zonal N l z y) :=
  (continuous_zonal N l).comp (continuous_id.prodMk continuous_const)

/-- display (2) -/
theorem zonal_proj {N : ℕ} (hN : 2 ≤ N) (a b : ℕ) (x y : Sph N) :
    ∫ z, zonal N a x z * zonal N b z y ∂(omega N) = if a = b then zonal N a x y else 0 :=
  zon_proj hN a b x y

theorem abs_zonal_le_three {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (x y : Sph N) : |zonal N l x y| ≤ dConc N l * 3 ^ l :=
  abs_zon_le_three hN l (abs_dot_le x y)

theorem integrable_zonal_mul {N : ℕ} (hN : 2 ≤ N) (a b : ℕ) (f g : Sph N → Sph N)
    (hf : Continuous f) (hg : Continuous g) (x y : Sph N) :
    Integrable (fun z => zonal N a x (f z) * zonal N b (g z) y) (omega N) := by
  have := omega_isProbabilityMeasure N (by omega)
  refine integrable_of_abs_le (((continuous_zonal_right N a x).comp hf).mul
    ((continuous_zonal_left N b y).comp hg)).measurable ((dConc N a * 3 ^ a) * (dConc N b * 3 ^ b)) (fun z => ?_)
  rw [abs_mul]
  exact mul_le_mul (abs_zonal_le_three hN a x (f z)) (abs_zonal_le_three hN b (g z) y) (abs_nonneg _)
    (mul_nonneg (dConc_pos_S1 hN a).le (by positivity))

/-- |Π_ℓ(x, y)| ≤ d_ℓ, from (2) by Cauchy-Schwarz -/
theorem abs_zonal_le {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (x y : Sph N) : |zonal N l x y| ≤ dConc N l := by
  have hsq : ∀ u : Sph N, ∫ z, zonal N l u z * zonal N l u z ∂(omega N) = dConc N l := by
    intro u
    have h := zonal_proj hN l l u u
    rw [if_pos rfl, zonal_self hN] at h
    rw [← h]
    congr 1; funext z; rw [zonal_symm N l z u]
  have hxy := zonal_proj hN l l x y
  rw [if_pos rfl] at hxy
  have i1 : Integrable (fun z => zonal N l x z * zonal N l x z) (omega N) := by
    have := integrable_zonal_mul hN l l id id continuous_id continuous_id x x
    refine this.congr (Filter.Eventually.of_forall (fun z => ?_))
    simp only [id]; rw [zonal_symm N l z x]
  have i3 := integrable_zonal_mul hN l l id id continuous_id continuous_id x y
  simp only [id] at i3
  have hyy : ∫ z, zonal N l z y * zonal N l z y ∂(omega N) = dConc N l := by
    rw [← hsq y]; congr 1; funext z; rw [zonal_symm N l z y]
  have i2' : Integrable (fun z => zonal N l z y * zonal N l z y) (omega N) := by
    have := integrable_zonal_mul hN l l id id continuous_id continuous_id y y
    refine this.congr (Filter.Eventually.of_forall (fun z => ?_))
    simp only [id]; rw [zonal_symm N l y z, zonal_symm N l z y]
  have hup : ∫ z, zonal N l x z * zonal N l z y ∂(omega N)
      ≤ (∫ z, zonal N l x z * zonal N l x z ∂(omega N) + ∫ z, zonal N l z y * zonal N l z y ∂(omega N)) / 2 := by
    rw [← integral_add i1 i2', ← integral_div]
    refine integral_mono i3 ((i1.add i2').div_const 2) (fun z => ?_)
    simp only [Pi.add_apply]
    nlinarith [sq_nonneg (zonal N l x z - zonal N l z y)]
  have hlo : -(∫ z, zonal N l x z * zonal N l z y ∂(omega N))
      ≤ (∫ z, zonal N l x z * zonal N l x z ∂(omega N) + ∫ z, zonal N l z y * zonal N l z y ∂(omega N)) / 2 := by
    rw [← integral_neg, ← integral_add i1 i2', ← integral_div]
    refine integral_mono i3.neg ((i1.add i2').div_const 2) (fun z => ?_)
    simp only [Pi.add_apply, Pi.neg_apply]
    nlinarith [sq_nonneg (zonal N l x z + zonal N l z y)]
  rw [hxy, hsq x, hyy] at hup hlo
  rw [abs_le]
  constructor <;> linarith

theorem exists_dot_eq {N : ℕ} (hN : 2 ≤ N) {t : ℝ} (ht : t ∈ Set.Icc (-1 : ℝ) 1) : ∃ x y : Sph N, dot x y = t := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  set b := EuclideanSpace.basisFun (Fin (M + 2)) ℝ
  have hon := b.orthonormal
  have h01 : (0 : Fin (M + 2)) ≠ 1 := fun h => by
    have := congrArg Fin.val h
    simp at this
  have n0 : ‖b 0‖ = 1 := hon.1 0
  have n1 : ‖b 1‖ = 1 := hon.1 1
  have i01 : @inner ℝ (Amb (M + 2)) _ (b 0) (b 1) = 0 := hon.2 h01
  have i00 : @inner ℝ (Amb (M + 2)) _ (b 0) (b 0) = 1 := by rw [real_inner_self_eq_norm_sq, n0, one_pow]
  set s := Real.sqrt (1 - t ^ 2)
  have hs : s ^ 2 = 1 - t ^ 2 := Real.sq_sqrt (by nlinarith [ht.1, ht.2])
  set v : Amb (M + 2) := t • b 0 + s • b 1
  have hv2 : ‖v‖ ^ 2 = 1 := by
    rw [norm_add_sq_real, norm_smul, norm_smul, real_inner_smul_left, real_inner_smul_right, i01, n0, n1,
      Real.norm_eq_abs, Real.norm_eq_abs, mul_one, mul_one, sq_abs, sq_abs, hs]
    ring
  have hv : ‖v‖ = 1 := by
    have h0 : 0 ≤ ‖v‖ := norm_nonneg _
    nlinarith [hv2]
  refine ⟨⟨b 0, by simp [n0]⟩, ⟨v, by simp [hv]⟩, ?_⟩
  unfold dot
  simp only [v, inner_add_right, real_inner_smul_right, i00, i01]
  ring

/-- |C̃_ℓ(t)| ≤ 1 on [-1, 1] -/
theorem abs_CConc_le_one {N : ℕ} (hN : 2 ≤ N) (l : ℕ) {t : ℝ} (ht : t ∈ Set.Icc (-1 : ℝ) 1) : |CConc N l t| ≤ 1 := by
  obtain ⟨x, y, hxy⟩ := exists_dot_eq hN ht
  have h := abs_zonal_le hN l x y
  unfold zonal at h
  rw [hxy, abs_mul, abs_of_pos (dConc_pos_S1 hN l)] at h
  have hd := dConc_pos_S1 hN l
  nlinarith [abs_nonneg (CConc N l t)]

/-- display (3) on the sphere -/
theorem exp_dot_hasSum {N : ℕ} (hN : 2 ≤ N) (J : ℝ) (x y : Sph N) :
    HasSum (fun l => kConc N l J * zonal N l x y) (Real.exp (J * dot x y)) :=
  exp_hasSum_zon hN J (dot x y) (abs_dot_le x y)

/-! ### Exchange of sums and integrals -/

theorem hasSum_integral_of_bound {α : Type*} [MeasurableSpace α] {μ : Measure α} [IsFiniteMeasure μ]
    {ι : Type*} [Countable ι] (F : ι → α → ℝ) (f : α → ℝ) (B : ι → ℝ)
    (hF : ∀ i, AEStronglyMeasurable (F i) μ) (hB : ∀ i a, |F i a| ≤ B i) (hBs : Summable B)
    (hlim : ∀ a, HasSum (fun i => F i a) (f a)) :
    HasSum (fun i => ∫ a, F i a ∂μ) (∫ a, f a ∂μ) :=
  hasSum_integral_of_dominated_convergence (fun i _ => B i) hF
    (fun i => Filter.Eventually.of_forall (fun a => by rw [Real.norm_eq_abs]; exact hB i a))
    (Filter.Eventually.of_forall (fun _ => hBs)) (integrable_const _) (Filter.Eventually.of_forall hlim)

theorem summable_kConc_dConc_nonneg {N : ℕ} (hN : 2 ≤ N) (J : ℝ) (l : ℕ) : 0 ≤ |kConc N l J| * dConc N l :=
  mul_nonneg (abs_nonneg _) (dConc_pos_S1 hN l).le

/-- the paper's integral formula k_ℓ(J) = ∫ e^{Jt} C̃_ℓ(t) μ_N(dt), in sphere form -/
theorem kConc_eq_integral {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (J : ℝ) (x : Sph N) :
    kConc N l J = ∫ z, Real.exp (J * dot x z) * CConc N l (dot x z) ∂(omega N) := by
  have := omega_isProbabilityMeasure N (by omega)
  have hS := hasSum_integral_of_bound (μ := omega N)
    (fun c z => kConc N c J * zonal N c x z * zonal N l z x)
    (fun z => Real.exp (J * dot x z) * zonal N l z x)
    (fun c => |kConc N c J| * dConc N c * dConc N l)
    (fun c => ((continuous_const.mul (continuous_zonal_right N c x)).mul
      (continuous_zonal_left N l x)).aestronglyMeasurable)
    (fun c z => by
      rw [abs_mul, abs_mul]
      exact mul_le_mul (mul_le_mul_of_nonneg_left (abs_zonal_le hN c x z) (abs_nonneg _)) (abs_zonal_le hN l z x)
        (abs_nonneg _) (mul_nonneg (abs_nonneg _) (dConc_pos_S1 hN c).le))
    ((summable_kConc_dConc hN J).mul_right _)
    (fun z => (exp_dot_hasSum hN J x z).mul_right _)
  have hval : ∀ c, ∫ z, kConc N c J * zonal N c x z * zonal N l z x ∂(omega N)
      = if c = l then kConc N l J * dConc N l else 0 := by
    intro c
    simp only [mul_assoc]
    rw [integral_const_mul, zonal_proj hN c l x x]
    split_ifs with h
    · rw [h, zonal_self hN]
    · rw [mul_zero]
  simp only [hval] at hS
  have h2 := hS.unique (hasSum_ite_eq l (kConc N l J * dConc N l))
  have hd := dConc_pos_S1 hN l
  have h3 : ∫ z, Real.exp (J * dot x z) * zonal N l z x ∂(omega N)
      = dConc N l * ∫ z, Real.exp (J * dot x z) * CConc N l (dot x z) ∂(omega N) := by
    rw [← integral_const_mul]
    congr 1; funext z
    unfold zonal; rw [dot_comm z x]; ring
  rw [h3] at h2
  field_simp at h2
  linarith

/-- Π_ℓ is a positive-definite kernel -/
theorem zonal_posDef {N : ℕ} (hN : 2 ≤ N) (l : ℕ) {ι : Type*} (s : Finset ι) (c : ι → ℝ) (x : ι → Sph N) :
    0 ≤ ∑ i ∈ s, ∑ j ∈ s, c i * c j * zonal N l (x i) (x j) := by
  have hrep : ∀ i j, zonal N l (x i) (x j) = ∫ z, zonal N l (x i) z * zonal N l (x j) z ∂(omega N) := by
    intro i j
    have h := zonal_proj hN l l (x i) (x j)
    rw [if_pos rfl] at h
    rw [← h]
    congr 1; funext z; rw [zonal_symm N l z (x j)]
  have hint2 : ∀ i j, Integrable (fun z => c i * zonal N l (x i) z * (c j * zonal N l (x j) z)) (omega N) := by
    intro i j
    have h := integrable_zonal_mul hN l l id id continuous_id continuous_id (x i) (x j)
    refine (h.const_mul (c i * c j)).congr (Filter.Eventually.of_forall (fun z => ?_))
    simp only [id]; rw [zonal_symm N l z (x j)]; ring
  have key : ∑ i ∈ s, ∑ j ∈ s, c i * c j * zonal N l (x i) (x j)
      = ∫ z, (∑ i ∈ s, c i * zonal N l (x i) z) ^ 2 ∂(omega N) := by
    calc ∑ i ∈ s, ∑ j ∈ s, c i * c j * zonal N l (x i) (x j)
        = ∑ i ∈ s, ∑ j ∈ s, ∫ z, c i * zonal N l (x i) z * (c j * zonal N l (x j) z) ∂(omega N) := by
          refine sum_congr rfl (fun i _ => sum_congr rfl (fun j _ => ?_))
          rw [hrep i j, ← integral_const_mul]
          congr 1; funext z; ring
      _ = ∫ z, ∑ i ∈ s, ∑ j ∈ s, c i * zonal N l (x i) z * (c j * zonal N l (x j) z) ∂(omega N) := by
          rw [integral_finset_sum _ (fun i _ => integrable_finset_sum _ (fun j _ => hint2 i j))]
          refine sum_congr rfl (fun i _ => ?_)
          rw [integral_finset_sum _ (fun j _ => hint2 i j)]
      _ = ∫ z, (∑ i ∈ s, c i * zonal N l (x i) z) ^ 2 ∂(omega N) := by
          congr 1; funext z; rw [sq, sum_mul_sum]
  rw [key]
  exact integral_nonneg (fun z => sq_nonneg _)

theorem zonal_term_abs_le {N : ℕ} (hN : 2 ≤ N) (J : ℝ) (c : ℕ) (u v : Sph N) :
    |kConc N c J * zonal N c u v| ≤ |kConc N c J| * dConc N c := by
  rw [abs_mul]
  exact mul_le_mul_of_nonneg_left (abs_zonal_le hN c u v) (abs_nonneg _)

theorem summable_norm_zonal_term {N : ℕ} (hN : 2 ≤ N) (J : ℝ) (u v : Sph N) :
    Summable (fun c => ‖kConc N c J * zonal N c u v‖) := by
  refine Summable.of_nonneg_of_le (fun c => norm_nonneg _) (fun c => ?_) (summable_kConc_dConc hN J)
  rw [Real.norm_eq_abs]
  exact zonal_term_abs_le hN J c u v

theorem exp_exp_pointwise {N : ℕ} (hN : 2 ≤ N) (a b : ℝ) (x y z : Sph N) :
    HasSum (fun p : ℕ × ℕ => (kConc N p.1 a * zonal N p.1 x z) * (kConc N p.2 b * zonal N p.2 z y))
      (Real.exp (a * dot x z) * Real.exp (b * dot z y)) :=
  (exp_dot_hasSum hN a x z).mul (exp_dot_hasSum hN b z y)
    (summable_mul_of_summable_norm (summable_norm_zonal_term hN a x z) (summable_norm_zonal_term hN b z y))

theorem continuous_exp_exp_term (N : ℕ) (a b : ℝ) (p : ℕ × ℕ) (x y : Sph N) :
    Continuous (fun z : Sph N => (kConc N p.1 a * zonal N p.1 x z) * (kConc N p.2 b * zonal N p.2 z y)) :=
  (continuous_const.mul (continuous_zonal_right N p.1 x)).mul (continuous_const.mul (continuous_zonal_left N p.2 y))

theorem exp_exp_term_abs_le {N : ℕ} (hN : 2 ≤ N) (a b : ℝ) (p : ℕ × ℕ) (x y z : Sph N) :
    |(kConc N p.1 a * zonal N p.1 x z) * (kConc N p.2 b * zonal N p.2 z y)|
      ≤ (|kConc N p.1 a| * dConc N p.1) * (|kConc N p.2 b| * dConc N p.2) := by
  rw [abs_mul]
  exact mul_le_mul (zonal_term_abs_le hN a p.1 x z) (zonal_term_abs_le hN b p.2 z y) (abs_nonneg _)
    (summable_kConc_dConc_nonneg hN a p.1)

theorem exp_exp_term_integral {N : ℕ} (hN : 2 ≤ N) (a b : ℝ) (p : ℕ × ℕ) (x y : Sph N) :
    ∫ z, (kConc N p.1 a * zonal N p.1 x z) * (kConc N p.2 b * zonal N p.2 z y) ∂(omega N)
      = if p.1 = p.2 then kConc N p.1 a * kConc N p.1 b * zonal N p.1 x y else 0 := by
  have h : ∀ z, (kConc N p.1 a * zonal N p.1 x z) * (kConc N p.2 b * zonal N p.2 z y)
      = (kConc N p.1 a * kConc N p.2 b) * (zonal N p.1 x z * zonal N p.2 z y) := fun z => by ring
  simp only [h]
  rw [integral_const_mul, zonal_proj hN]
  split_ifs with h1
  · rw [h1]
  · rw [mul_zero]

/-- integrating out a vertex of degree two:
∫ e^{a x·z} e^{b z·y} ω(dz) = Σ_c k_c(a) k_c(b) Π_c(x, y) -/
theorem exp_exp_integral_hasSum {N : ℕ} (hN : 2 ≤ N) (a b : ℝ) (x y : Sph N) :
    HasSum (fun c => kConc N c a * kConc N c b * zonal N c x y)
      (∫ z, Real.exp (a * dot x z) * Real.exp (b * dot z y) ∂(omega N)) := by
  have := omega_isProbabilityMeasure N (by omega)
  have hS := hasSum_integral_of_bound (μ := omega N)
    (fun p : ℕ × ℕ => fun z => (kConc N p.1 a * zonal N p.1 x z) * (kConc N p.2 b * zonal N p.2 z y))
    (fun z => Real.exp (a * dot x z) * Real.exp (b * dot z y))
    (fun p => (|kConc N p.1 a| * dConc N p.1) * (|kConc N p.2 b| * dConc N p.2))
    (fun p => (continuous_exp_exp_term N a b p x y).aestronglyMeasurable)
    (fun p z => exp_exp_term_abs_le hN a b p x y z)
    ((summable_kConc_dConc hN a).mul_of_nonneg (summable_kConc_dConc hN b)
      (summable_kConc_dConc_nonneg hN a) (summable_kConc_dConc_nonneg hN b))
    (fun z => exp_exp_pointwise hN a b x y z)
  have hS' : HasSum (fun p : ℕ × ℕ => if p.1 = p.2 then kConc N p.1 a * kConc N p.1 b * zonal N p.1 x y else 0)
      (∫ z, Real.exp (a * dot x z) * Real.exp (b * dot z y) ∂(omega N)) := by
    refine hS.congr_fun ?_
    intro p
    exact (exp_exp_term_integral hN a b p x y).symm
  have hinj : Function.Injective (fun c : ℕ => (c, c)) := fun c d h => by simpa using h
  have hzero : ∀ p ∉ Set.range (fun c : ℕ => (c, c)),
      (if p.1 = p.2 then kConc N p.1 a * kConc N p.1 b * zonal N p.1 x y else 0) = 0 := by
    intro p hp
    rw [if_neg]
    intro h
    exact hp ⟨p.1, by ext <;> simp [h]⟩
  have h2 := (hinj.hasSum_iff hzero).mpr hS'
  refine h2.congr_fun ?_
  intro c
  simp

end G2Kernel
