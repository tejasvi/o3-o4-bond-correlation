/-
G2S1.Tie (stage S1): the paper's data d_ℓ, C̃_ℓ, k_ℓ tied to the paper's objects (Section 2.1).
- N = 2: C̃_ℓ(cos θ) = cos ℓθ (the paper's remark), and C̃_ℓ = T_ℓ (Mathlib's Chebyshev polynomial);
- N = 3: d_ℓ = 2ℓ + 1; N = 4: d_ℓ = (ℓ+1)^2 and (ℓ+1) C̃_ℓ = U_ℓ (Chebyshev U), as in Section 4 of the paper;
- every N ≥ 2: with μ_N the law of σ·x under ω (`muN`), ∫ C̃_a C̃_b dμ_N = δ_ab / d_ℓ, deg C̃_n = n and C̃_n(1) = 1; and
  `CConc_unique`: a family of polynomials P_n with deg P_n ≤ n, P_n(1) = 1 and ∫ P_a P_b dμ_N = 0 (a ≠ b) is C̃.
  This is the classical characterization of the Gegenbauer polynomials C^λ_n (λ = N/2 - 1) normalized at 1
  (orthogonal for the weight (1 - t^2)^{λ - 1/2}, the density of μ_N), so C̃_ℓ is the paper's normalized C^λ_ℓ, and
  d_ℓ = 1 / ∫ C̃_ℓ^2 dμ_N is the normalisation of the projection kernel Π_ℓ (display (2)).
- k_ℓ(J) = ∫ e^{Jt} C̃_ℓ(t) μ_N(dt): `kConc_eq_integral` (G2S1.Zonal), `kConc_eq_integral_muN` below.
-/
import G2S1.Zonal

noncomputable section
open Real Finset MeasureTheory Polynomial

namespace G2Kernel

/-! ### N = 2, 3, 4 -/

/-- N = 2: C̃_ℓ(cos θ) = cos ℓθ -/
theorem CConc_two_cos : ∀ (n : ℕ) (θ : ℝ), CConc 2 n (Real.cos θ) = Real.cos (n * θ)
  | 0, θ => by simp [CConc]
  | 1, θ => by simp [CConc]
  | n + 2, θ => by
    have h1 := CConc_two_cos (n + 1) θ
    have h0 := CConc_two_cos n θ
    rw [CConc, h1, h0]
    have e2 : ((n + 2 : ℕ) : ℝ) * θ = ((n + 1 : ℕ) : ℝ) * θ + θ := by push_cast; ring
    have e0 : (n : ℝ) * θ = ((n + 1 : ℕ) : ℝ) * θ - θ := by push_cast; ring
    rw [e2, e0, Real.cos_add, Real.cos_sub]
    have hn : ((n : ℝ) + 1) ≠ 0 := by positivity
    push_cast
    field_simp
    ring

/-- N = 2: C̃_ℓ is the Chebyshev polynomial T_ℓ -/
theorem CConc_two_eq_chebyshevT : ∀ (n : ℕ) (t : ℝ), CConc 2 n t = (Chebyshev.T ℝ n).eval t
  | 0, t => by simp [CConc, Chebyshev.T_zero]
  | 1, t => by simp [CConc, Chebyshev.T_one]
  | n + 2, t => by
    have h1 := CConc_two_eq_chebyshevT (n + 1) t
    have h0 := CConc_two_eq_chebyshevT n t
    rw [CConc, h1, h0]
    have hT : (Chebyshev.T ℝ ((n + 2 : ℕ) : ℤ)) = 2 * X * Chebyshev.T ℝ ((n + 1 : ℕ) : ℤ) - Chebyshev.T ℝ (n : ℤ) := by
      have := Chebyshev.T_add_two ℝ (n : ℤ)
      push_cast
      rw [this]
    rw [hT]
    simp only [eval_sub, eval_mul, eval_ofNat, eval_X]
    have hn : ((n : ℝ) + 1) ≠ 0 := by positivity
    push_cast
    field_simp
    ring

/-- N = 4: (ℓ + 1) C̃_ℓ is the Chebyshev polynomial U_ℓ -/
theorem CConc_four_eq_chebyshevU : ∀ (n : ℕ) (t : ℝ), ((n : ℝ) + 1) * CConc 4 n t = (Chebyshev.U ℝ n).eval t
  | 0, t => by simp [CConc, Chebyshev.U_zero]
  | 1, t => by
    have h : CConc 4 1 t = t := rfl
    rw [h]
    push_cast
    rw [Chebyshev.U_one]
    simp only [eval_mul, eval_ofNat, eval_X]
    ring
  | n + 2, t => by
    have h1 := CConc_four_eq_chebyshevU (n + 1) t
    have h0 := CConc_four_eq_chebyshevU n t
    rw [CConc]
    have hU : (Chebyshev.U ℝ ((n + 2 : ℕ) : ℤ)) = 2 * X * Chebyshev.U ℝ ((n + 1 : ℕ) : ℤ) - Chebyshev.U ℝ (n : ℤ) := by
      have := Chebyshev.U_add_two ℝ (n : ℤ)
      push_cast
      rw [this]
    rw [hU]
    simp only [eval_sub, eval_mul, eval_ofNat, eval_X]
    rw [← h1, ← h0]
    have hn1 : ((n : ℝ) + 1) ≠ 0 := by positivity
    have hn3 : ((n : ℝ) + 1) + (((4 : ℕ) : ℝ) - 2) ≠ 0 := by push_cast; positivity
    push_cast at hn3 ⊢
    field_simp
    ring

theorem dConc_three (l : ℕ) : dConc 3 l = 2 * (l : ℝ) + 1 := by
  rcases l with _ | a
  · rw [dConc_zero]; simp
  · have h := dConc_succ 1 a
    rw [show (1 + 2 : ℕ) = 3 from rfl] at h
    rw [h, Nat.choose_symm_add, Nat.choose_symm_add, Nat.choose_one_right, Nat.choose_one_right]
    push_cast
    ring

theorem dConc_four (l : ℕ) : dConc 4 l = ((l : ℝ) + 1) ^ 2 := by
  rcases l with _ | a
  · rw [dConc_zero]; simp
  · have h := dConc_succ 2 a
    rw [show (2 + 2 : ℕ) = 4 from rfl] at h
    rw [h, Nat.choose_symm_add, Nat.choose_symm_add, Nat.cast_choose_two, Nat.cast_choose_two]
    push_cast
    ring

/-! ### Every N ≥ 2: the normalized orthogonal polynomials of μ_N -/

/-- μ_N: the law of σ·x for σ distributed by ω -/
def muN (N : ℕ) (x : Sph N) : Measure ℝ := (omega N).map (fun z => dot x z)

theorem integral_muN {N : ℕ} (x : Sph N) (g : ℝ → ℝ) (hg : Continuous g) :
    ∫ t, g t ∂(muN N x) = ∫ z, g (dot x z) ∂(omega N) := by
  unfold muN
  rw [integral_map (continuous_dot_right x).measurable.aemeasurable hg.aestronglyMeasurable]

/-- orthogonality: ∫ C̃_a C̃_b dμ_N = δ_ab / d_a -/
theorem integral_CConc_mul {N : ℕ} (hN : 2 ≤ N) (a b : ℕ) (x : Sph N) :
    ∫ t, CConc N a t * CConc N b t ∂(muN N x) = if a = b then 1 / dConc N a else 0 := by
  have hc : ∫ t, CConc N a t * CConc N b t ∂(muN N x) = ∫ z, CConc N a (dot x z) * CConc N b (dot x z) ∂(omega N) :=
    integral_muN x (fun t => CConc N a t * CConc N b t) ((continuous_CConc N a).mul (continuous_CConc N b))
  rw [hc]
  have h := zonal_proj hN a b x x
  have hda := dConc_pos_S1 hN a
  have hdb := dConc_pos_S1 hN b
  have h2 : ∫ z, zonal N a x z * zonal N b z x ∂(omega N)
      = dConc N a * dConc N b * ∫ z, CConc N a (dot x z) * CConc N b (dot x z) ∂(omega N) := by
    rw [← integral_const_mul]
    congr 1; funext z
    unfold zonal; rw [dot_comm z x]; ring
  rw [h2] at h
  split_ifs with hab
  · subst hab
    rw [if_pos rfl, zonal_self hN] at h
    rw [eq_div_iff hda.ne']
    have h' : dConc N a * ((∫ z, CConc N a (dot x z) * CConc N a (dot x z) ∂(omega N)) * dConc N a - 1) = 0 := by
      linear_combination h
    rcases mul_eq_zero.mp h' with h'' | h''
    · exact absurd h'' hda.ne'
    · linarith
  · rw [if_neg hab] at h
    rcases mul_eq_zero.mp h with h' | h'
    · exact absurd h' (mul_pos hda hdb).ne'
    · exact h'

/-- d_ℓ is the normalisation of the projection kernel: ∫ C̃_ℓ^2 dμ_N = 1 / d_ℓ -/
theorem integral_CConc_sq_muN {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (x : Sph N) :
    ∫ t, CConc N l t ^ 2 ∂(muN N x) = 1 / dConc N l := by
  have h := integral_CConc_mul hN l l x
  rw [if_pos rfl] at h
  rw [← h]
  congr 1; funext t; ring

/-- the same on the sphere (interface form): ∫ C̃_ℓ(x · z)^2 ω(dz) = 1 / d_ℓ -/
theorem integral_CConc_sq {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (x : Sph N) :
    ∫ z, (CConc N l (dot x z)) ^ 2 ∂(omega N) = 1 / dConc N l := by
  rw [← integral_CConc_sq_muN hN l x]
  exact (integral_muN x (fun t => CConc N l t ^ 2) ((continuous_CConc N l).pow 2)).symm

/-- the paper's k_ℓ(J) = ∫ e^{Jt} C̃_ℓ(t) μ_N(dt) -/
theorem kConc_eq_integral_muN {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (J : ℝ) (x : Sph N) :
    kConc N l J = ∫ t, Real.exp (J * t) * CConc N l t ∂(muN N x) := by
  have hc : ∫ t, Real.exp (J * t) * CConc N l t ∂(muN N x) = ∫ z, Real.exp (J * dot x z) * CConc N l (dot x z) ∂(omega N) :=
    integral_muN x (fun t => Real.exp (J * t) * CConc N l t)
      ((continuous_const.mul continuous_id).rexp.mul (continuous_CConc N l))
  rw [hc]
  exact kConc_eq_integral hN l J x

/-! ### Exact degrees and uniqueness -/

theorem coeff_cPoly_top {N : ℕ} (hN : 2 ≤ N) : ∀ n : ℕ, 0 < (cPoly N n).coeff n
  | 0 => by simp [cPoly]
  | 1 => by simp [cPoly]
  | n + 2 => by
    have h1 := coeff_cPoly_top hN (n + 1)
    have h0 : (cPoly N n).coeff (n + 2) = 0 :=
      coeff_eq_zero_of_natDegree_lt (lt_of_le_of_lt (natDegree_cPoly_le N n) (by omega))
    have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
    simp only [cPoly]
    rw [coeff_C_mul, coeff_sub, coeff_C_mul, h0, mul_zero, sub_zero, mul_assoc, coeff_C_mul,
      show n + 2 = (n + 1) + 1 from rfl, coeff_X_mul]
    have hA : (0 : ℝ) < 2 * ((n : ℝ) + 1) + ((N : ℝ) - 2) := by
      have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
      linarith
    have hD : (0 : ℝ) < 1 / (((n : ℝ) + 1) + ((N : ℝ) - 2)) := by
      have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
      apply div_pos one_pos; linarith
    exact mul_pos hD (mul_pos hA h1)

/-- deg C̃_n = n -/
theorem natDegree_cPoly {N : ℕ} (hN : 2 ≤ N) (n : ℕ) : (cPoly N n).natDegree = n :=
  natDegree_eq_of_le_of_coeff_ne_zero (natDegree_cPoly_le N n) (coeff_cPoly_top hN n).ne'

theorem cPoly_eval_one {N : ℕ} (hN : 2 ≤ N) (n : ℕ) : (cPoly N n).eval 1 = 1 := by
  rw [eval_cPoly, CConc_one N hN]

/-- every polynomial of degree < n is a combination of C̃_0, …, C̃_{n-1} -/
theorem exists_cPoly_comb {N : ℕ} (hN : 2 ≤ N) : ∀ (n : ℕ) (R : Polynomial ℝ), R.degree < n →
    ∃ β : ℕ → ℝ, R = ∑ m ∈ range n, C (β m) * cPoly N m
  | 0, R, hR => by
    have : R = 0 := by
      rw [Nat.cast_zero, Nat.WithBot.lt_zero_iff, degree_eq_bot] at hR
      exact hR
    exact ⟨fun _ => 0, by simp [this]⟩
  | n + 1, R, hR => by
    set c := R.coeff n / (cPoly N n).coeff n with hc
    have hlead := (coeff_cPoly_top hN n).ne'
    have hR' : (R - C c * cPoly N n).degree < n := by
      apply degree_lt_iff_coeff_zero _ _ |>.mpr
      intro m hm
      rw [coeff_sub, coeff_C_mul]
      rcases lt_or_eq_of_le (show n ≤ m by exact_mod_cast hm) with h | h
      · have h1 : R.coeff m = 0 := coeff_eq_zero_of_degree_lt (lt_of_lt_of_le hR (by exact_mod_cast h))
        have h2 : (cPoly N n).coeff m = 0 := coeff_eq_zero_of_natDegree_lt (lt_of_le_of_lt (natDegree_cPoly_le N n) h)
        rw [h1, h2]; ring
      · subst h; rw [hc]; field_simp; ring
    obtain ⟨β, hβ⟩ := exists_cPoly_comb hN n _ hR'
    refine ⟨Function.update β n c, ?_⟩
    rw [sum_range_succ, Function.update_self]
    have hsum : ∑ m ∈ range n, C (Function.update β n c m) * cPoly N m = ∑ m ∈ range n, C (β m) * cPoly N m := by
      refine sum_congr rfl (fun m hm => ?_)
      rw [Function.update_of_ne (by simp at hm; omega)]
    rw [hsum, ← hβ]
    ring

theorem integrable_comp_dot {N : ℕ} (hN : 1 ≤ N) (g : ℝ → ℝ) (hg : Continuous g) (x : Sph N) :
    Integrable (fun z => g (dot x z)) (omega N) := by
  have := omega_isProbabilityMeasure N (by omega)
  obtain ⟨t0, -, ht0⟩ := isCompact_Icc.exists_isMaxOn (Set.nonempty_Icc.mpr (by norm_num : (-1 : ℝ) ≤ 1))
    hg.abs.continuousOn
  refine integrable_of_abs_le (hg.comp (continuous_dot_right x)).measurable (|g t0|) (fun z => ?_)
  exact isMaxOn_iff.mp ht0 _ (abs_le.mp (abs_dot_le x z))

theorem integrable_muN {N : ℕ} (hN : 1 ≤ N) (g : ℝ → ℝ) (hg : Continuous g) (x : Sph N) :
    Integrable g (muN N x) := by
  unfold muN
  exact (integrable_map_measure hg.aestronglyMeasurable (continuous_dot_right x).measurable.aemeasurable).mpr
    (integrable_comp_dot hN g hg x)

/-- uniqueness: a family of polynomials P_n with deg P_n ≤ n, P_n(1) = 1, orthogonal for μ_N, is C̃ -/
theorem CConc_unique {N : ℕ} (hN : 2 ≤ N) (x : Sph N) (P : ℕ → Polynomial ℝ)
    (hdeg : ∀ n, (P n).natDegree ≤ n) (hone : ∀ n, (P n).eval 1 = 1)
    (horth : ∀ a b, a ≠ b → ∫ t, (P a).eval t * (P b).eval t ∂(muN N x) = 0) :
    ∀ n, P n = cPoly N n := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
  have hdg : (P n).degree < ((n + 1 : ℕ) : WithBot ℕ) :=
    lt_of_le_of_lt degree_le_natDegree (by exact_mod_cast Nat.lt_succ_of_le (hdeg n))
  obtain ⟨β, hβ⟩ := exists_cPoly_comb hN (n + 1) (P n) hdg
  have hev : ∀ t, (P n).eval t = ∑ m ∈ range (n + 1), β m * CConc N m t := by
    intro t
    rw [hβ, eval_finset_sum]
    simp only [eval_mul, eval_C, eval_cPoly]
  have hβm : ∀ m < n, β m = 0 := by
    intro m hm
    have h1 := horth n m (by omega)
    rw [ih m hm] at h1
    simp only [hev, eval_cPoly, sum_mul] at h1
    rw [integral_finset_sum _ (fun m' _ => (integrable_muN (by omega) (fun t => β m' * CConc N m' t * CConc N m t)
      ((continuous_const.mul (continuous_CConc N m')).mul (continuous_CConc N m)) x))] at h1
    simp only [mul_assoc, integral_const_mul, integral_CConc_mul hN, mul_ite, mul_zero] at h1
    rw [sum_ite_eq' (range (n + 1)) m, if_pos (mem_range.mpr (by omega))] at h1
    have hd := dConc_pos_S1 hN m
    have : β m * (1 / dConc N m) = 0 := h1
    rcases mul_eq_zero.mp this with h | h
    · exact h
    · exact absurd h (by positivity)
  have hPn : P n = C (β n) * cPoly N n := by
    rw [hβ, sum_range_succ, sum_eq_zero (fun m hm => by rw [hβm m (mem_range.mp hm), C_0, zero_mul]), zero_add]
  have h1 := hone n
  rw [hPn, eval_mul, eval_C, cPoly_eval_one hN, mul_one] at h1
  rw [hPn, h1, C_1, one_mul]

end G2Kernel
