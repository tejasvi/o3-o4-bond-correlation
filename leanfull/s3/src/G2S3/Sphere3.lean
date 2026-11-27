/-
G2S3.Sphere3 (stage S3, Part B4): the parametrization of omega on S^2,
  Phi3 (r, e, b) = (sign(e) rho, tau cos b, tau sin b),
measure preserving from (law of r3 = |s_0|) x uniform(Bool) x Haar to omega 3, by `param_mp` with the group generated
by the sign change of the coordinate 0 and the rotations of the plane of the coordinates 1, 2.
-/
import G2S3.Spheres

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

local instance instFactTwoPiPos3 : Fact (0 < 2 * π) := ⟨Real.two_pi_pos⟩

theorem sg_xor (a b : Bool) : sg (xor a b) = sg a * sg b := by cases a <;> cases b <;> simp [sg]

/-- Sign change of the coordinate 0 (by `g.1`) and rotation by `g.2` in the plane of the coordinates 1, 2. -/
def rot3 (g : Bool × Tor) : Amb 3 ≃ₗᵢ[ℝ] Amb 3 where
  toFun x := WithLp.toLp 2 ![sg g.1 * x 0, tcos g.2 * x 1 - tsin g.2 * x 2, tsin g.2 * x 1 + tcos g.2 * x 2]
  invFun x := WithLp.toLp 2 ![sg g.1 * x 0, tcos g.2 * x 1 + tsin g.2 * x 2, tcos g.2 * x 2 - tsin g.2 * x 1]
  map_add' x y := by ext i; fin_cases i <;> simp <;> ring
  map_smul' c x := by ext i; fin_cases i <;> simp <;> ring
  left_inv x := by
    have h1 := sg_mul_self g.1
    have h2 := tcos_sq_add_tsin_sq g.2
    ext i
    fin_cases i
    · simp; linear_combination (x 0) * h1
    · simp; linear_combination (x 1) * h2
    · simp; linear_combination (x 2) * h2
  right_inv x := by
    have h1 := sg_mul_self g.1
    have h2 := tcos_sq_add_tsin_sq g.2
    ext i
    fin_cases i
    · simp; linear_combination (x 0) * h1
    · simp; linear_combination (x 1) * h2
    · simp; linear_combination (x 2) * h2
  norm_map' x := by
    have h1 := sg_mul_self g.1
    have h2 := tcos_sq_add_tsin_sq g.2
    rw [EuclideanSpace.norm_eq, EuclideanSpace.norm_eq]
    congr 1
    simp only [Fin.sum_univ_three, Real.norm_eq_abs, sq_abs]
    simp
    linear_combination (x 0 ^ 2) * h1 + (x 1 ^ 2 + x 2 ^ 2) * h2

theorem rot3_apply (g : Bool × Tor) (x : Amb 3) :
    rot3 g x = WithLp.toLp 2 ![sg g.1 * x 0, tcos g.2 * x 1 - tsin g.2 * x 2, tsin g.2 * x 1 + tcos g.2 * x 2] := rfl

/-- The coordinates of `S^2`. -/
def Phi3 (c : ℝ × (Bool × Tor)) : Sph 3 :=
  ⟨WithLp.toLp 2 ![sg c.2.1 * rhoF c.1, tauF c.1 * tcos c.2.2, tauF c.1 * tsin c.2.2],
    mem_sph_of_sum _ (by
      have h1 := sg_mul_self c.2.1
      have h2 := tcos_sq_add_tsin_sq c.2.2
      have h3 := rho_sq_add_tau_sq c.1
      simp only [Fin.sum_univ_three]
      simp
      linear_combination (rhoF c.1 ^ 2) * h1 + (tauF c.1 ^ 2) * h2 + h3)⟩

theorem Phi3_coord (c : ℝ × (Bool × Tor)) :
    ((Phi3 c : Sph 3) : Amb 3) = WithLp.toLp 2 ![sg c.2.1 * rhoF c.1, tauF c.1 * tcos c.2.2, tauF c.1 * tsin c.2.2] :=
  rfl

theorem continuous_sg_fst {Y : Type*} [TopologicalSpace Y] {f : Y → Bool} (hf : Continuous f) :
    Continuous (fun y => sg (f y)) :=
  (continuous_of_discreteTopology (f := sg)).comp hf

theorem continuous_Phi3 : Continuous Phi3 := by
  refine Continuous.subtype_mk (continuous_vec3 ?_ ?_ ?_) _
  · exact (continuous_sg_fst (continuous_fst.comp continuous_snd)).mul (continuous_rhoF.comp continuous_fst)
  · exact (continuous_tauF.comp continuous_fst).mul (continuous_tcos.comp (continuous_snd.comp continuous_snd))
  · exact (continuous_tauF.comp continuous_fst).mul (continuous_tsin.comp (continuous_snd.comp continuous_snd))

def r3 (σ : Sph 3) : ℝ := |(σ : Amb 3) 0|

def theta3 (σ : Sph 3) : Bool × Tor :=
  (decide ((σ : Amb 3) 0 < 0), ((Complex.arg ⟨(σ : Amb 3) 1, (σ : Amb 3) 2⟩ : ℝ) : Tor))

theorem sph3_sum (σ : Sph 3) : (σ : Amb 3) 0 ^ 2 + (σ : Amb 3) 1 ^ 2 + (σ : Amb 3) 2 ^ 2 = 1 := by
  have h := sph_sum_sq σ
  simp only [Fin.sum_univ_three] at h
  linarith

theorem r3_le_one (σ : Sph 3) : r3 σ ≤ 1 := by
  unfold r3
  rw [abs_le]
  constructor <;> nlinarith [sph3_sum σ, sq_nonneg ((σ : Amb 3) 1), sq_nonneg ((σ : Amb 3) 2)]

theorem rhoF_r3 (σ : Sph 3) : rhoF (r3 σ) = r3 σ := rhoF_of_mem (abs_nonneg _) (r3_le_one σ)

theorem tauF_r3 (σ : Sph 3) : tauF (r3 σ) = Real.sqrt ((σ : Amb 3) 1 ^ 2 + (σ : Amb 3) 2 ^ 2) := by
  unfold tauF
  rw [rhoF_r3, r3, sq_abs]
  congr 1
  linarith [sph3_sum σ]

theorem sg_sign_abs (x : ℝ) : sg (decide (x < 0)) * |x| = x := by
  by_cases h : x < 0
  · simp [h, sg, abs_of_neg h]
  · simp [h, sg, abs_of_nonneg (not_lt.mp h)]

theorem decomp3 (g : Bool × Tor) (σ : Sph 3) :
    sphMap (rot3 g) σ = Phi3 (r3 σ, (xor (theta3 σ).1 g.1, (theta3 σ).2 + g.2)) := by
  have pc := Complex.norm_mul_cos_arg (⟨(σ : Amb 3) 1, (σ : Amb 3) 2⟩ : ℂ)
  have ps := Complex.norm_mul_sin_arg (⟨(σ : Amb 3) 1, (σ : Amb 3) 2⟩ : ℂ)
  rw [Complex.norm_eq_sqrt_sq_add_sq] at pc ps
  simp only at pc ps
  have h0 := sg_sign_abs ((σ : Amb 3) 0)
  apply Subtype.ext
  rw [Phi3_coord]
  show rot3 g (σ : Amb 3) = _
  rw [rot3_apply]
  simp only [theta3, sg_xor, tcos_add, tsin_add, tcos_coe, tsin_coe, rhoF_r3, tauF_r3]
  unfold r3
  ext i
  fin_cases i
  · simp
    linear_combination (-sg g.1) * h0
  · simp
    linear_combination (-tcos g.2) * pc + (tsin g.2) * ps
  · simp
    linear_combination (-tsin g.2) * pc + (-tcos g.2) * ps

/-- The plane-1 radius law on `S^2`. -/
def nu3 : Measure ℝ := (omega 3).map r3

/-- **Parametrization of `ω` on `S^2`.** -/
theorem param3 :
    MeasurePreserving Phi3 (nu3.prod (unifB.prod AddCircle.haarAddCircle)) (omega 3) := by
  have := omega_isProbabilityMeasure 3 (by norm_num)
  have hr : Measurable r3 := ((continuous_coordA 0).abs).measurable
  have hact : Measurable (fun p : (Bool × Tor) × Sph 3 => sphMap (rot3 p.1) p.2) := by
    refine Continuous.measurable (Continuous.subtype_mk ?_ _)
    show Continuous (fun p : (Bool × Tor) × Sph 3 => rot3 p.1 (p.2 : Amb 3))
    simp only [rot3_apply]
    have hs : Continuous (fun p : (Bool × Tor) × Sph 3 => p.2) := continuous_snd
    have hf1 : Continuous (fun p : (Bool × Tor) × Sph 3 => p.1.1) := continuous_fst.comp continuous_fst
    have hf2 : Continuous (fun p : (Bool × Tor) × Sph 3 => p.1.2) := continuous_snd.comp continuous_fst
    have c0 := (continuous_coordA (N := 3) 0).comp hs
    have c1 := (continuous_coordA (N := 3) 1).comp hs
    have c2 := (continuous_coordA (N := 3) 2).comp hs
    have e1 := continuous_sg_fst hf1
    have a2 := continuous_tcos.comp hf2
    have b2 := continuous_tsin.comp hf2
    exact continuous_vec3 (e1.mul c0) ((a2.mul c1).sub (b2.mul c2)) ((b2.mul c1).add (a2.mul c2))
  exact param_mp (omega 3) (unifB.prod AddCircle.haarAddCircle) (fun g σ => sphMap (rot3 g) σ)
    hact (fun g => hSphereIso_holds 3 (rot3 g)) Phi3 continuous_Phi3.measurable r3 hr
    (fun g θ => (xor θ.1 g.1, θ.2 + g.2))
    (fun θ => (xor_measurePreserving θ.1).prod (measurePreserving_add_left _ θ.2)) theta3 decomp3

end G2S3

#print axioms G2S3.param3
