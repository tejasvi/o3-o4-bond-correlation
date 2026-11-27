/-
G2S3.Coords (stage S3, Part B4): the two-plane coordinates of the spheres S^2 and S^3 used in the Ginibre-Dunlop
argument, and the parametrization of omega.
- `param_mp`: if a group of measure-preserving maps acts on (S, omega) and every point is Phi(r(s), theta(s)) with the
  action moving only theta by a measure-preserving translation, then Phi is measure preserving from
  (law of r) x lambda to omega. Proof by Tonelli and averaging over the group (rotation invariance of omega from S0's
  hSphereIso_holds).
- N = 4: s = (rho cos a, rho sin a, tau cos b, tau sin b), a, b on the circle (two rotation planes).
- N = 3: s = (eps rho, tau cos b, tau sin b), eps = +-1 (the plane-1 "rotations" are the sign changes).
Here rho = clamp(r) in [0, 1] and tau = sqrt(1 - rho^2). The laws of the radii are never computed (Dunlop's condition
holds for every law, G2S3.radial_site).
-/
import G2S3.ConeInt

noncomputable section
open MeasureTheory Real
open scoped ENNReal

namespace G2S3

open G2Kernel

/-! ### The averaging lemma -/

theorem param_mp {S Gr : Type*} [MeasurableSpace S] [MeasurableSpace Gr] (ω : Measure S) [IsProbabilityMeasure ω]
    (lam : Measure Gr) [IsProbabilityMeasure lam] (act : Gr → S → S)
    (hact : Measurable (fun p : Gr × S => act p.1 p.2)) (hmp : ∀ g, MeasurePreserving (act g) ω ω)
    (Φ : ℝ × Gr → S) (hΦ : Measurable Φ) (r : S → ℝ) (hr : Measurable r) (T : Gr → Gr → Gr)
    (hT : ∀ θ, MeasurePreserving (fun g => T g θ) lam lam) (θ : S → Gr)
    (hdec : ∀ g σ, act g σ = Φ (r σ, T g (θ σ))) :
    MeasurePreserving Φ ((ω.map r).prod lam) ω := by
  refine ⟨hΦ, Measure.ext (fun A hA => ?_)⟩
  rw [Measure.map_apply hΦ hA]
  have hind : Measurable (A.indicator (fun _ => (1 : ℝ≥0∞))) := measurable_const.indicator hA
  have h1 : ((ω.map r).prod lam) (Φ ⁻¹' A)
      = ∫⁻ z, A.indicator (fun _ => (1 : ℝ≥0∞)) (Φ z) ∂((ω.map r).prod lam) := by
    rw [← lintegral_indicator_one (hΦ hA)]
    rfl
  have hj : Measurable (fun z : ℝ × Gr => A.indicator (fun _ => (1 : ℝ≥0∞)) (Φ z)) := hind.comp hΦ
  rw [h1, lintegral_prod _ hj.aemeasurable,
    lintegral_map (hj.lintegral_prod_right' (ν := lam)) hr]
  have h2 : ∀ σ, ∫⁻ g, A.indicator (fun _ => (1 : ℝ≥0∞)) (Φ (r σ, g)) ∂lam
      = ∫⁻ g, A.indicator (fun _ => (1 : ℝ≥0∞)) (act g σ) ∂lam := by
    intro σ
    have hm : Measurable (fun g => A.indicator (fun _ => (1 : ℝ≥0∞)) (Φ (r σ, g))) :=
      hind.comp (hΦ.comp (measurable_const.prodMk measurable_id))
    rw [← (hT (θ σ)).lintegral_comp hm]
    simp only [hdec]
  simp only [h2]
  have hjm : Measurable (fun p : S × Gr => A.indicator (fun _ => (1 : ℝ≥0∞)) (act p.2 p.1)) :=
    hind.comp (hact.comp measurable_swap)
  rw [lintegral_lintegral_swap hjm.aemeasurable]
  have h3 : ∀ g, ∫⁻ σ, A.indicator (fun _ => (1 : ℝ≥0∞)) (act g σ) ∂ω = ω A := by
    intro g
    rw [(hmp g).lintegral_comp hind]
    exact lintegral_indicator_one hA
  simp only [h3, lintegral_const, measure_univ, mul_one]

/-! ### Radii -/

def rhoF (r : ℝ) : ℝ := max 0 (min r 1)
def tauF (r : ℝ) : ℝ := Real.sqrt (1 - rhoF r ^ 2)

theorem rhoF_mono : Monotone rhoF := fun a b h => max_le_max le_rfl (min_le_min h le_rfl)
theorem rhoF_nonneg (r : ℝ) : 0 ≤ rhoF r := le_max_left _ _
theorem rhoF_le_one (r : ℝ) : rhoF r ≤ 1 := max_le zero_le_one (min_le_right _ _)
theorem rhoF_of_mem {r : ℝ} (h0 : 0 ≤ r) (h1 : r ≤ 1) : rhoF r = r := by
  unfold rhoF
  rw [min_eq_left h1, max_eq_right h0]
theorem continuous_rhoF : Continuous rhoF := continuous_const.max (continuous_id.min continuous_const)
theorem tauF_nonneg (r : ℝ) : 0 ≤ tauF r := Real.sqrt_nonneg _
theorem tauF_le_one (r : ℝ) : tauF r ≤ 1 := by
  unfold tauF
  rw [Real.sqrt_le_one]
  nlinarith [rhoF_nonneg r]
theorem tauF_anti : Antitone tauF := by
  intro a b h
  unfold tauF
  apply Real.sqrt_le_sqrt
  have := rhoF_mono h
  nlinarith [rhoF_nonneg a, rhoF_nonneg b]
theorem continuous_tauF : Continuous tauF :=
  Real.continuous_sqrt.comp (continuous_const.sub (continuous_rhoF.pow 2))
theorem rho_sq_add_tau_sq (r : ℝ) : rhoF r ^ 2 + tauF r ^ 2 = 1 := by
  unfold tauF
  rw [Real.sq_sqrt]
  · ring
  · nlinarith [rhoF_nonneg r, rhoF_le_one r]

/-! ### Circle identities -/

theorem tcos_sq_add_tsin_sq (A : Tor) : tcos A ^ 2 + tsin A ^ 2 = 1 := by
  induction A using QuotientAddGroup.induction_on with
  | H a => exact Real.cos_sq_add_sin_sq a

theorem tcos_add (A B : Tor) : tcos (A + B) = tcos A * tcos B - tsin A * tsin B := by
  induction A using QuotientAddGroup.induction_on with
  | H a =>
    induction B using QuotientAddGroup.induction_on with
    | H b => rw [← AddCircle.coe_add, tcos_coe, tcos_coe, tcos_coe, tsin_coe, tsin_coe, Real.cos_add]

theorem tsin_add (A B : Tor) : tsin (A + B) = tsin A * tcos B + tcos A * tsin B := by
  induction A using QuotientAddGroup.induction_on with
  | H a =>
    induction B using QuotientAddGroup.induction_on with
    | H b => rw [← AddCircle.coe_add, tsin_coe, tsin_coe, tcos_coe, tcos_coe, tsin_coe, Real.sin_add]

theorem tcos_sub (A B : Tor) : tcos (A - B) = tcos A * tcos B + tsin A * tsin B := by
  induction A using QuotientAddGroup.induction_on with
  | H a =>
    induction B using QuotientAddGroup.induction_on with
    | H b => rw [← AddCircle.coe_sub, tcos_coe, tcos_coe, tcos_coe, tsin_coe, tsin_coe, Real.cos_sub]

/-- polar form of a point of the plane: `(x, y) = |z| (cos arg z, sin arg z)` -/
theorem polar_cos (x y : ℝ) : Real.sqrt (x ^ 2 + y ^ 2) * tcos ((Complex.arg ⟨x, y⟩ : ℝ) : Tor) = x := by
  rw [tcos_coe]
  have h := Complex.norm_mul_cos_arg (⟨x, y⟩ : ℂ)
  rw [Complex.norm_eq_sqrt_sq_add_sq] at h
  exact h

theorem polar_sin (x y : ℝ) : Real.sqrt (x ^ 2 + y ^ 2) * tsin ((Complex.arg ⟨x, y⟩ : ℝ) : Tor) = y := by
  rw [tsin_coe]
  have h := Complex.norm_mul_sin_arg (⟨x, y⟩ : ℂ)
  rw [Complex.norm_eq_sqrt_sq_add_sq] at h
  exact h

/-! ### Coordinates of the sphere -/

theorem sph_sum_sq {N : ℕ} (σ : Sph N) : ∑ i, (σ : Amb N) i ^ 2 = 1 := by
  have h := norm_eq_of_mem_sphere σ
  rw [EuclideanSpace.norm_eq] at h
  have h2 : ∑ i, ‖(σ : Amb N) i‖ ^ 2 = 1 := by
    have := Real.sqrt_eq_one.mp h
    exact this
  simpa [Real.norm_eq_abs, sq_abs] using h2

theorem mem_sph_of_sum {N : ℕ} (x : Amb N) (h : ∑ i, x i ^ 2 = 1) : x ∈ Metric.sphere (0 : Amb N) 1 := by
  rw [mem_sphere_zero_iff_norm, EuclideanSpace.norm_eq]
  simp only [Real.norm_eq_abs, sq_abs, h, Real.sqrt_one]

end G2S3

#print axioms G2S3.param_mp
