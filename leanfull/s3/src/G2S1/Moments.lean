/-
G2S1.Moments (stage S1, the one sphere fact): the one-point moments of ω,
∫ ⟪w, z⟫^n ω(dz) = μ_n |w|^n, with μ_0 = 1, μ_odd = 0, (n + N) μ_{n+2} = (n + 1) μ_n.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1 (ω, μ_N).
Proof: polar coordinates (`Measure.measurePreserving_homeomorphUnitSphereProd`) against the Gaussian weight e^{-|v|^2}
for homogeneous functions; the Gaussian moment of a coordinate from the product structure of `EuclideanSpace`; one
Householder reflection (`reflection_sub`) for a general direction w.
-/
import G2S1.Coord

noncomputable section
open Real Finset MeasureTheory Set

namespace G2Kernel

/-! ### Polar coordinates against the Gaussian weight -/

/-- ∫_{Ioi 0} h d(volumeIoiPow k) = ∫_{Ioi 0} r^k h(r) dr -/
theorem integral_volumeIoiPow (k : ℕ) (h : ℝ → ℝ) :
    ∫ r : Ioi (0 : ℝ), h r ∂(Measure.volumeIoiPow k) = ∫ r in Ioi (0 : ℝ), r ^ k * h r := by
  simp only [Measure.volumeIoiPow, ENNReal.ofReal]
  rw [integral_withDensity_eq_integral_smul, integral_subtype_comap measurableSet_Ioi
    (fun a => Real.toNNReal (a ^ k) • h a)]
  · refine setIntegral_congr_fun measurableSet_Ioi (fun x hx => ?_)
    rw [NNReal.smul_def, Real.coe_toNNReal _ (pow_nonneg (le_of_lt hx) _), smul_eq_mul]
  · exact (measurable_subtype_coe.pow_const _).real_toNNReal

/-- polar coordinates: for f homogeneous of degree n,
∫ e^{-|v|^2} f(v) dv = (∫_S f dσ) ∫_0^∞ r^{N-1} e^{-r^2} r^n dr, σ = volume.toSphere -/
theorem integral_gauss_homog {N : ℕ} (hN : 1 ≤ N) (f : Amb N → ℝ) (n : ℕ)
    (hf : ∀ r : ℝ, 0 < r → ∀ v, f (r • v) = r ^ n * f v) :
    ∫ v : Amb N, Real.exp (-‖v‖ ^ 2) * f v
      = (∫ z : Sph N, f z ∂(volume : Measure (Amb N)).toSphere) *
          ∫ r in Ioi (0 : ℝ), r ^ (N - 1) * (Real.exp (-r ^ 2) * r ^ n) := by
  have hdim : Module.finrank ℝ (Amb N) = N := finrank_euclideanSpace_fin
  have : Nontrivial (Amb N) := Module.nontrivial_of_finrank_pos (R := ℝ) (by omega)
  set F : Amb N → ℝ := fun v => Real.exp (-‖v‖ ^ 2) * f v with hF
  have step1 : ∫ v, F v = ∫ x : ({(0 : Amb N)}ᶜ : Set (Amb N)), F x.1 ∂((volume : Measure (Amb N)).comap (↑)) := by
    rw [integral_subtype_comap (measurableSet_singleton _).compl (fun x => F x), restrict_compl_singleton]
  have step2 : ∫ x : ({(0 : Amb N)}ᶜ : Set (Amb N)), F x.1 ∂((volume : Measure (Amb N)).comap (↑))
      = ∫ p, F ((p.2 : ℝ) • (p.1 : Amb N)) ∂((volume : Measure (Amb N)).toSphere.prod
          (Measure.volumeIoiPow (Module.finrank ℝ (Amb N) - 1))) := by
    rw [← (volume : Measure (Amb N)).measurePreserving_homeomorphUnitSphereProd.integral_comp
      (Homeomorph.measurableEmbedding _) (fun p => F ((p.2 : ℝ) • (p.1 : Amb N)))]
    refine integral_congr_ae (Filter.Eventually.of_forall (fun x => ?_))
    simp only [homeomorphUnitSphereProd_apply_snd_coe, homeomorphUnitSphereProd_apply_fst_coe]
    have hx : (x : Amb N) ≠ 0 := x.2
    rw [smul_inv_smul₀ (norm_ne_zero_iff.mpr hx)]
  have step3 : ∀ p : Sph N × Ioi (0 : ℝ), F ((p.2 : ℝ) • (p.1 : Amb N))
      = f p.1 * (Real.exp (-(p.2 : ℝ) ^ 2) * (p.2 : ℝ) ^ n) := by
    intro p
    have hr : (0 : ℝ) < p.2 := p.2.2
    have hz : ‖(p.1 : Amb N)‖ = 1 := by simp
    simp only [hF]
    rw [hf _ hr, norm_smul, hz, Real.norm_eq_abs, abs_of_pos hr, mul_one]
    ring
  rw [step1, step2, hdim]
  simp only [step3]
  have hI := integral_volumeIoiPow (N - 1) (fun r : ℝ => Real.exp (-r ^ 2) * r ^ n)
  rw [integral_prod_mul (fun z : Sph N => f z) (fun r : Ioi (0 : ℝ) => Real.exp (-(r : ℝ) ^ 2) * (r : ℝ) ^ n), hI]

/-! ### One-dimensional Gaussian moments -/

/-- g_n = ∫ x^n e^{-x^2} dx -/
def gMom (n : ℕ) : ℝ := ∫ x : ℝ, x ^ n * Real.exp (-x ^ 2)

/-- R_n = ∫_0^∞ r^{N-1} e^{-r^2} r^n dr -/
def rMom (N n : ℕ) : ℝ := ∫ r in Ioi (0 : ℝ), r ^ (N - 1) * (Real.exp (-r ^ 2) * r ^ n)

theorem integral_Ioi_pow_gauss (k : ℕ) :
    ∫ r in Ioi (0 : ℝ), r ^ k * Real.exp (-r ^ 2) = (1 / 2) * Real.Gamma (((k : ℝ) + 1) / 2) := by
  have h := integral_rpow_mul_exp_neg_rpow (p := 2) (q := (k : ℝ)) (by norm_num) (by linarith [(Nat.cast_nonneg k : (0 : ℝ) ≤ k)])
  rw [← h]
  refine setIntegral_congr_fun measurableSet_Ioi (fun x hx => ?_)
  rw [Real.rpow_natCast, show (2 : ℝ) = ((2 : ℕ) : ℝ) by norm_num, Real.rpow_natCast]

theorem rMom_eq {N : ℕ} (hN : 1 ≤ N) (n : ℕ) : rMom N n = (1 / 2) * Real.Gamma (((n : ℝ) + N) / 2) := by
  unfold rMom
  have h := integral_Ioi_pow_gauss (N - 1 + n)
  rw [show (((N - 1 + n : ℕ) : ℝ) + 1) = (n : ℝ) + N by push_cast [Nat.cast_sub hN]; ring] at h
  rw [← h]
  refine setIntegral_congr_fun measurableSet_Ioi (fun x _ => ?_)
  rw [pow_add]
  ring

theorem rMom_pos {N : ℕ} (hN : 1 ≤ N) (n : ℕ) : 0 < rMom N n := by
  rw [rMom_eq hN]
  have : (0 : ℝ) < ((n : ℝ) + N) / 2 := by
    have : (1 : ℝ) ≤ N := by exact_mod_cast hN
    positivity
  have := Real.Gamma_pos_of_pos this
  positivity

theorem rMom_succ2 {N : ℕ} (hN : 1 ≤ N) (n : ℕ) : rMom N (n + 2) = (((n : ℝ) + N) / 2) * rMom N n := by
  rw [rMom_eq hN, rMom_eq hN]
  have hpos : (0 : ℝ) < ((n : ℝ) + N) / 2 := by
    have : (1 : ℝ) ≤ N := by exact_mod_cast hN
    positivity
  rw [show (((n + 2 : ℕ) : ℝ) + N) / 2 = ((n : ℝ) + N) / 2 + 1 by push_cast; ring, Real.Gamma_add_one hpos.ne']
  ring

theorem gMom_odd (k : ℕ) : gMom (2 * k + 1) = 0 := by
  unfold gMom
  have h := integral_neg_eq_self (fun x : ℝ => x ^ (2 * k + 1) * Real.exp (-x ^ 2)) volume
  have h2 : (fun x : ℝ => (-x) ^ (2 * k + 1) * Real.exp (-(-x) ^ 2))
      = fun x => -(x ^ (2 * k + 1) * Real.exp (-x ^ 2)) := by
    funext x
    rw [Odd.neg_pow ⟨k, rfl⟩, neg_sq]
    ring
  simp only [h2, integral_neg] at h
  linarith

theorem gMom_even (k : ℕ) : gMom (2 * k) = Real.Gamma ((k : ℝ) + 1 / 2) := by
  unfold gMom
  have h := integral_comp_abs (f := fun y : ℝ => y ^ (2 * k) * Real.exp (-y ^ 2))
  have h2 : (fun x : ℝ => |x| ^ (2 * k) * Real.exp (-|x| ^ 2)) = fun x => x ^ (2 * k) * Real.exp (-x ^ 2) := by
    funext x
    rw [Even.pow_abs ⟨k, by ring⟩, sq_abs]
  simp only [h2] at h
  rw [h, integral_Ioi_pow_gauss]
  push_cast
  ring_nf

theorem gMom_zero : gMom 0 = √π := by
  have h := gMom_even 0
  simp only [mul_zero, Nat.cast_zero, zero_add] at h
  rw [h, Real.Gamma_one_half_eq]

theorem gMom_succ2 (n : ℕ) : gMom (n + 2) = (((n : ℝ) + 1) / 2) * gMom n := by
  obtain ⟨k, hk | hk⟩ := Nat.even_or_odd' n
  · subst hk
    rw [show 2 * k + 2 = 2 * (k + 1) by ring, gMom_even, gMom_even]
    have hpos : (0 : ℝ) < (k : ℝ) + 1 / 2 := by positivity
    rw [show ((k + 1 : ℕ) : ℝ) + 1 / 2 = ((k : ℝ) + 1 / 2) + 1 by push_cast; ring, Real.Gamma_add_one hpos.ne']
    push_cast
    ring
  · subst hk
    rw [show 2 * k + 1 + 2 = 2 * (k + 1) + 1 by ring, gMom_odd, gMom_odd]
    ring

theorem integral_gauss_one : ∫ x : ℝ, Real.exp (-x ^ 2) = √π := by
  have h := integral_gaussian 1
  simp only [neg_mul, one_mul, div_one] at h
  exact h

/-! ### The Gaussian moment of a coordinate and of a direction -/

theorem gauss_coord_moment (M n : ℕ) :
    ∫ v : Amb (M + 1), Real.exp (-‖v‖ ^ 2) * (v 0) ^ n = gMom n * (√π) ^ M := by
  rw [← (PiLp.volume_preserving_toLp (Fin (M + 1))).integral_comp (MeasurableEquiv.toLp 2 _).measurableEmbedding]
  set H : Fin (M + 1) → ℝ → ℝ := fun i s => if i = 0 then s ^ n * Real.exp (-s ^ 2) else Real.exp (-s ^ 2) with hH
  have hprod : ∀ x : Fin (M + 1) → ℝ,
      Real.exp (-‖(WithLp.toLp 2 x : Amb (M + 1))‖ ^ 2) * x 0 ^ n = ∏ i, H i (x i) := by
    intro x
    simp only [EuclideanSpace.norm_eq, PiLp.toLp_apply, Real.norm_eq_abs, sq_abs]
    rw [Real.sq_sqrt (Finset.sum_nonneg (fun i _ => sq_nonneg _)), ← Finset.sum_neg_distrib, Real.exp_sum,
      Fin.prod_univ_succ, Fin.prod_univ_succ]
    simp only [hH, if_true, Fin.succ_ne_zero, if_false]
    ring
  refine (integral_congr_ae (Filter.Eventually.of_forall hprod)).trans ?_
  rw [integral_fintype_prod_volume_eq_prod H, Fin.prod_univ_succ]
  simp only [hH, if_true, Fin.succ_ne_zero, if_false, integral_gauss_one, Finset.prod_const, Finset.card_univ,
    Fintype.card_fin]
  rfl

theorem inner_single_zero (M : ℕ) (v : Amb (M + 1)) :
    @inner ℝ (Amb (M + 1)) _ (EuclideanSpace.single 0 1) v = v 0 := by
  simp [PiLp.inner_apply]

theorem gauss_inner_moment (M : ℕ) (w : Amb (M + 1)) (n : ℕ) :
    ∫ v : Amb (M + 1), Real.exp (-‖v‖ ^ 2) * (@inner ℝ (Amb (M + 1)) _ w v) ^ n = ‖w‖ ^ n * (gMom n * (√π) ^ M) := by
  by_cases hw : w = 0
  · subst hw
    rcases n with _ | n
    · have h := gauss_coord_moment M 0
      simp only [pow_zero] at h ⊢
      rw [h, one_mul]
    · simp
  · set u : Amb (M + 1) := ‖w‖⁻¹ • w with hu
    set e0 : Amb (M + 1) := EuclideanSpace.single 0 1 with he0
    have hwn : ‖w‖ ≠ 0 := norm_ne_zero_iff.mpr hw
    have hun : ‖u‖ = ‖e0‖ := by
      rw [hu, he0, norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ hwn, EuclideanSpace.norm_single, norm_one]
    set Rf := (ℝ ∙ (u - e0))ᗮ.reflection with hRf
    have hRu : Rf u = e0 := Submodule.reflection_sub hun
    have hwu : w = ‖w‖ • u := by rw [hu, smul_inv_smul₀ hwn]
    have hRw : Rf w = ‖w‖ • e0 := by
      calc Rf w = Rf (‖w‖ • u) := by rw [← hwu]
        _ = ‖w‖ • Rf u := map_smul Rf ‖w‖ u
        _ = ‖w‖ • e0 := by rw [hRu]
    have hinner : ∀ v, @inner ℝ (Amb (M + 1)) _ w (Rf v) = ‖w‖ * v 0 := by
      intro v
      have h1 : @inner ℝ (Amb (M + 1)) _ w (Rf v) = @inner ℝ (Amb (M + 1)) _ (Rf w) (Rf (Rf v)) :=
        (Rf.inner_map_map w (Rf v)).symm
      rw [h1, hRf, Submodule.reflection_reflection, ← hRf, hRw, real_inner_smul_left, he0, inner_single_zero]
    have hmp := Rf.measurePreserving
    calc ∫ v, Real.exp (-‖v‖ ^ 2) * (@inner ℝ (Amb (M + 1)) _ w v) ^ n
        = ∫ v, Real.exp (-‖Rf v‖ ^ 2) * (@inner ℝ (Amb (M + 1)) _ w (Rf v)) ^ n :=
          (hmp.integral_comp Rf.toHomeomorph.measurableEmbedding
            (fun v => Real.exp (-‖v‖ ^ 2) * (@inner ℝ (Amb (M + 1)) _ w v) ^ n)).symm
      _ = ∫ v : Amb (M + 1), ‖w‖ ^ n * (Real.exp (-‖v‖ ^ 2) * (v 0) ^ n) := by
          congr 1; funext v; rw [Rf.norm_map, hinner, mul_pow]; ring
      _ = ‖w‖ ^ n * (gMom n * (√π) ^ M) := by rw [integral_const_mul, gauss_coord_moment]

/-! ### The one-point moments of ω -/

/-- μ_n = g_n R_0 / (g_0 R_n) -/
def muMom (N n : ℕ) : ℝ := gMom n * rMom N 0 / (gMom 0 * rMom N n)

theorem gMom_even_pos (k : ℕ) : 0 < gMom (2 * k) := by
  rw [gMom_even]; exact Real.Gamma_pos_of_pos (by positivity)

theorem muMom_zero {N : ℕ} (hN : 1 ≤ N) : muMom N 0 = 1 := by
  unfold muMom
  have h1 := rMom_pos hN 0
  have h2 : gMom 0 ≠ 0 := by rw [gMom_zero]; positivity
  field_simp

theorem muMom_odd (N k : ℕ) : muMom N (2 * k + 1) = 0 := by
  simp [muMom, gMom_odd]

theorem muMom_even_pos {N : ℕ} (hN : 1 ≤ N) (k : ℕ) : 0 < muMom N (2 * k) := by
  unfold muMom
  have h1 := rMom_pos hN 0
  have h2 := rMom_pos hN (2 * k)
  have h3 := gMom_even_pos k
  have h4 := gMom_even_pos 0
  simp only [mul_zero] at h4
  positivity

theorem muMom_succ2 {N : ℕ} (hN : 1 ≤ N) (n : ℕ) :
    muMom N (n + 2) * ((n : ℝ) + N) = muMom N n * ((n : ℝ) + 1) := by
  unfold muMom
  rw [gMom_succ2, rMom_succ2 hN]
  have h1 := rMom_pos hN 0
  have h2 := rMom_pos hN n
  have h3 : gMom 0 ≠ 0 := by rw [gMom_zero]; positivity
  have hN' : (1 : ℝ) ≤ N := by exact_mod_cast hN
  have h4 : ((n : ℝ) + N) ≠ 0 := by positivity
  field_simp
  all_goals ring

/-- the one-point moments of ω: ∫ ⟪w, z⟫^n ω(dz) = |w|^n μ_n -/
theorem sphere_moment {N : ℕ} (hN : 1 ≤ N) (w : Amb N) (n : ℕ) :
    ∫ z : Sph N, (@inner ℝ (Amb N) _ w (z : Amb N)) ^ n ∂(omega N) = ‖w‖ ^ n * muMom N n := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 1 := ⟨N - 1, by omega⟩
  set σ := (volume : Measure (Amb (M + 1))).toSphere with hσ
  have hpol : ∀ w' : Amb (M + 1), ∀ n',
      ‖w'‖ ^ n' * (gMom n' * (√π) ^ M) = (∫ z : Sph (M + 1), (@inner ℝ (Amb (M + 1)) _ w' (z : Amb (M + 1))) ^ n' ∂σ) *
        rMom (M + 1) n' := by
    intro w' n'
    rw [← gauss_inner_moment M w' n']
    exact integral_gauss_homog (by omega) (fun v => (@inner ℝ (Amb (M + 1)) _ w' v) ^ n') n'
      (fun r _ v => by rw [real_inner_smul_right, mul_pow])
  have h0 := hpol w 0
  simp only [pow_zero, one_mul, integral_const, smul_eq_mul, mul_one] at h0
  have hn := hpol w n
  have hR0 := rMom_pos (show 1 ≤ M + 1 by omega) 0
  have hRn := rMom_pos (show 1 ≤ M + 1 by omega) n
  have hg0 : gMom 0 ≠ 0 := by rw [gMom_zero]; positivity
  have hsq : (√π) ^ M ≠ 0 := by positivity
  have hσu : σ.real Set.univ = gMom 0 * (√π) ^ M / rMom (M + 1) 0 := by
    rw [eq_div_iff hR0.ne']; linarith
  have hint : ∫ z : Sph (M + 1), (@inner ℝ (Amb (M + 1)) _ w (z : Amb (M + 1))) ^ n ∂σ
      = ‖w‖ ^ n * (gMom n * (√π) ^ M) / rMom (M + 1) n := by
    rw [eq_div_iff hRn.ne']; linarith
  unfold omega
  rw [integral_smul_measure, ENNReal.toReal_inv, ← hσ, hint, smul_eq_mul]
  have hσr : (σ Set.univ).toReal = σ.real Set.univ := rfl
  rw [hσr, hσu]
  unfold muMom
  field_simp

end G2Kernel
