/-
G2S3.Spheres (stage S3, Part B4): the parametrizations of omega on S^3 and S^2 in two-plane coordinates.
- `param4`: Phi4 (r, a, b) = (rho cos a, rho sin a, tau cos b, tau sin b) is measure preserving from
  (law of r4) x Haar x Haar to omega 4, r4 = |(s_0, s_1)|.
- `param3`: Phi3 (r, e, b) = (+-rho, tau cos b, tau sin b) is measure preserving from (law of r3) x uniform x Haar to
  omega 3, r3 = |s_0|.
Both from `param_mp` with the rotation groups (rotations of the two planes, resp. sign change and rotation), which act
by linear isometries (S0's hSphereIso_holds).
-/
import G2S3.Coords
import G2S0.SphereIso

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

local instance instFactTwoPiPos' : Fact (0 < 2 * π) := ⟨Real.two_pi_pos⟩

theorem continuous_vec4 {Y : Type*} [TopologicalSpace Y] {f0 f1 f2 f3 : Y → ℝ} (h0 : Continuous f0)
    (h1 : Continuous f1) (h2 : Continuous f2) (h3 : Continuous f3) :
    Continuous (fun y => (WithLp.toLp 2 ![f0 y, f1 y, f2 y, f3 y] : Amb 4)) := by
  refine (PiLp.continuous_toLp 2 (fun _ : Fin 4 => ℝ)).comp (continuous_pi (fun i => ?_))
  fin_cases i <;> simpa

theorem continuous_vec3 {Y : Type*} [TopologicalSpace Y] {f0 f1 f2 : Y → ℝ} (h0 : Continuous f0)
    (h1 : Continuous f1) (h2 : Continuous f2) :
    Continuous (fun y => (WithLp.toLp 2 ![f0 y, f1 y, f2 y] : Amb 3)) := by
  refine (PiLp.continuous_toLp 2 (fun _ : Fin 3 => ℝ)).comp (continuous_pi (fun i => ?_))
  fin_cases i <;> simpa

theorem continuous_coordA {N : ℕ} (i : Fin N) : Continuous (fun σ : Sph N => (σ : Amb N) i) :=
  (PiLp.continuous_apply 2 (fun _ : Fin N => ℝ) i).comp continuous_subtype_val

/-! ### N = 4 -/

/-- Rotation by `g.1` in the plane of the coordinates 0, 1 and by `g.2` in the plane of 2, 3. -/
def rot4 (g : Tor × Tor) : Amb 4 ≃ₗᵢ[ℝ] Amb 4 where
  toFun x := WithLp.toLp 2 ![tcos g.1 * x 0 - tsin g.1 * x 1, tsin g.1 * x 0 + tcos g.1 * x 1,
      tcos g.2 * x 2 - tsin g.2 * x 3, tsin g.2 * x 2 + tcos g.2 * x 3]
  invFun x := WithLp.toLp 2 ![tcos g.1 * x 0 + tsin g.1 * x 1, tcos g.1 * x 1 - tsin g.1 * x 0,
      tcos g.2 * x 2 + tsin g.2 * x 3, tcos g.2 * x 3 - tsin g.2 * x 2]
  map_add' x y := by ext i; fin_cases i <;> simp <;> ring
  map_smul' c x := by ext i; fin_cases i <;> simp <;> ring
  left_inv x := by
    have h1 := tcos_sq_add_tsin_sq g.1
    have h2 := tcos_sq_add_tsin_sq g.2
    ext i
    fin_cases i
    · simp; linear_combination (x 0) * h1
    · simp; linear_combination (x 1) * h1
    · simp; linear_combination (x 2) * h2
    · simp; linear_combination (x 3) * h2
  right_inv x := by
    have h1 := tcos_sq_add_tsin_sq g.1
    have h2 := tcos_sq_add_tsin_sq g.2
    ext i
    fin_cases i
    · simp; linear_combination (x 0) * h1
    · simp; linear_combination (x 1) * h1
    · simp; linear_combination (x 2) * h2
    · simp; linear_combination (x 3) * h2
  norm_map' x := by
    have h1 := tcos_sq_add_tsin_sq g.1
    have h2 := tcos_sq_add_tsin_sq g.2
    rw [EuclideanSpace.norm_eq, EuclideanSpace.norm_eq]
    congr 1
    simp only [Fin.sum_univ_four, Real.norm_eq_abs, sq_abs]
    simp
    linear_combination (x 0 ^ 2 + x 1 ^ 2) * h1 + (x 2 ^ 2 + x 3 ^ 2) * h2

theorem rot4_apply (g : Tor × Tor) (x : Amb 4) :
    rot4 g x = WithLp.toLp 2 ![tcos g.1 * x 0 - tsin g.1 * x 1, tsin g.1 * x 0 + tcos g.1 * x 1,
      tcos g.2 * x 2 - tsin g.2 * x 3, tsin g.2 * x 2 + tcos g.2 * x 3] := rfl

/-- The coordinates of `S^3`. -/
def Phi4 (c : ℝ × (Tor × Tor)) : Sph 4 :=
  ⟨WithLp.toLp 2 ![rhoF c.1 * tcos c.2.1, rhoF c.1 * tsin c.2.1, tauF c.1 * tcos c.2.2, tauF c.1 * tsin c.2.2],
    mem_sph_of_sum _ (by
      have h1 := tcos_sq_add_tsin_sq c.2.1
      have h2 := tcos_sq_add_tsin_sq c.2.2
      have h3 := rho_sq_add_tau_sq c.1
      simp only [Fin.sum_univ_four]
      simp
      linear_combination (rhoF c.1 ^ 2) * h1 + (tauF c.1 ^ 2) * h2 + h3)⟩

theorem Phi4_coord (c : ℝ × (Tor × Tor)) :
    ((Phi4 c : Sph 4) : Amb 4) = WithLp.toLp 2 ![rhoF c.1 * tcos c.2.1, rhoF c.1 * tsin c.2.1,
      tauF c.1 * tcos c.2.2, tauF c.1 * tsin c.2.2] := rfl

theorem continuous_Phi4 : Continuous Phi4 := by
  refine Continuous.subtype_mk (continuous_vec4 ?_ ?_ ?_ ?_) _
  · exact (continuous_rhoF.comp continuous_fst).mul (continuous_tcos.comp (continuous_fst.comp continuous_snd))
  · exact (continuous_rhoF.comp continuous_fst).mul (continuous_tsin.comp (continuous_fst.comp continuous_snd))
  · exact (continuous_tauF.comp continuous_fst).mul (continuous_tcos.comp (continuous_snd.comp continuous_snd))
  · exact (continuous_tauF.comp continuous_fst).mul (continuous_tsin.comp (continuous_snd.comp continuous_snd))

def r4 (σ : Sph 4) : ℝ := Real.sqrt ((σ : Amb 4) 0 ^ 2 + (σ : Amb 4) 1 ^ 2)

def theta4 (σ : Sph 4) : Tor × Tor :=
  (((Complex.arg ⟨(σ : Amb 4) 0, (σ : Amb 4) 1⟩ : ℝ) : Tor), ((Complex.arg ⟨(σ : Amb 4) 2, (σ : Amb 4) 3⟩ : ℝ) : Tor))

theorem sph4_sum (σ : Sph 4) : (σ : Amb 4) 0 ^ 2 + (σ : Amb 4) 1 ^ 2 + (σ : Amb 4) 2 ^ 2 + (σ : Amb 4) 3 ^ 2 = 1 := by
  have h := sph_sum_sq σ
  simp only [Fin.sum_univ_four] at h
  linarith

theorem r4_le_one (σ : Sph 4) : r4 σ ≤ 1 := by
  unfold r4
  rw [Real.sqrt_le_one]
  nlinarith [sph4_sum σ, sq_nonneg ((σ : Amb 4) 2), sq_nonneg ((σ : Amb 4) 3)]

theorem rhoF_r4 (σ : Sph 4) : rhoF (r4 σ) = r4 σ :=
  rhoF_of_mem (Real.sqrt_nonneg _) (r4_le_one σ)

theorem tauF_r4 (σ : Sph 4) : tauF (r4 σ) = Real.sqrt ((σ : Amb 4) 2 ^ 2 + (σ : Amb 4) 3 ^ 2) := by
  unfold tauF
  rw [rhoF_r4, r4, Real.sq_sqrt (by positivity)]
  congr 1
  linarith [sph4_sum σ]

theorem decomp4 (g : Tor × Tor) (σ : Sph 4) : sphMap (rot4 g) σ = Phi4 (r4 σ, theta4 σ + g) := by
  have pc1 := Complex.norm_mul_cos_arg (⟨(σ : Amb 4) 0, (σ : Amb 4) 1⟩ : ℂ)
  have ps1 := Complex.norm_mul_sin_arg (⟨(σ : Amb 4) 0, (σ : Amb 4) 1⟩ : ℂ)
  have pc2 := Complex.norm_mul_cos_arg (⟨(σ : Amb 4) 2, (σ : Amb 4) 3⟩ : ℂ)
  have ps2 := Complex.norm_mul_sin_arg (⟨(σ : Amb 4) 2, (σ : Amb 4) 3⟩ : ℂ)
  rw [Complex.norm_eq_sqrt_sq_add_sq] at pc1 ps1 pc2 ps2
  simp only at pc1 ps1 pc2 ps2
  apply Subtype.ext
  rw [Phi4_coord]
  show rot4 g (σ : Amb 4) = _
  rw [rot4_apply]
  simp only [theta4, Prod.fst_add, Prod.snd_add, tcos_add, tsin_add, tcos_coe, tsin_coe, rhoF_r4, tauF_r4]
  unfold r4
  ext i
  fin_cases i
  · simp
    linear_combination (-tcos g.1) * pc1 + (tsin g.1) * ps1
  · simp
    linear_combination (-tsin g.1) * pc1 + (-tcos g.1) * ps1
  · simp
    linear_combination (-tcos g.2) * pc2 + (tsin g.2) * ps2
  · simp
    linear_combination (-tsin g.2) * pc2 + (-tcos g.2) * ps2

/-- The plane-1 radius law on `S^3`. -/
def nu4 : Measure ℝ := (omega 4).map r4

/-- **Parametrization of `ω` on `S^3`.** -/
theorem param4 :
    MeasurePreserving Phi4 (nu4.prod (AddCircle.haarAddCircle.prod AddCircle.haarAddCircle)) (omega 4) := by
  have := omega_isProbabilityMeasure 4 (by norm_num)
  have hr : Measurable r4 :=
    (Real.continuous_sqrt.comp (((continuous_coordA 0).pow 2).add ((continuous_coordA 1).pow 2))).measurable
  have hact : Measurable (fun p : (Tor × Tor) × Sph 4 => sphMap (rot4 p.1) p.2) := by
    refine Continuous.measurable (Continuous.subtype_mk ?_ _)
    show Continuous (fun p : (Tor × Tor) × Sph 4 => rot4 p.1 (p.2 : Amb 4))
    simp only [rot4_apply]
    have hs : Continuous (fun p : (Tor × Tor) × Sph 4 => p.2) := continuous_snd
    have hf1 : Continuous (fun p : (Tor × Tor) × Sph 4 => p.1.1) := continuous_fst.comp continuous_fst
    have hf2 : Continuous (fun p : (Tor × Tor) × Sph 4 => p.1.2) := continuous_snd.comp continuous_fst
    have c0 := (continuous_coordA (N := 4) 0).comp hs
    have c1 := (continuous_coordA (N := 4) 1).comp hs
    have c2 := (continuous_coordA (N := 4) 2).comp hs
    have c3 := (continuous_coordA (N := 4) 3).comp hs
    have a1 := continuous_tcos.comp hf1
    have b1 := continuous_tsin.comp hf1
    have a2 := continuous_tcos.comp hf2
    have b2 := continuous_tsin.comp hf2
    exact continuous_vec4 ((a1.mul c0).sub (b1.mul c1)) ((b1.mul c0).add (a1.mul c1))
      ((a2.mul c2).sub (b2.mul c3)) ((b2.mul c2).add (a2.mul c3))
  exact param_mp (omega 4) (AddCircle.haarAddCircle.prod AddCircle.haarAddCircle) (fun g σ => sphMap (rot4 g) σ)
    hact (fun g => hSphereIso_holds 4 (rot4 g)) Phi4 continuous_Phi4.measurable r4 hr (fun g θ => θ + g)
    (fun θ => measurePreserving_add_left _ θ) theta4 decomp4

end G2S3

#print axioms G2S3.param4
