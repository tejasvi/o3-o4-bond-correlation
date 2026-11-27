/-
G2S1.TwoPoint (stage S1): the two-point moments of ω and the projection identity (2).
- `rmom x y p q` = ∫ (x·z)^p (y·z)^q ω(dz) / (p! q!) satisfies the recurrence [*] of G2S1.Jac (from the one-point moments
  by polarization: the polynomial identity in J for ∫ (J x·z + y·z)^n ω(dz)), hence `rmom = Rz` (`two_point_CF`).
- `zon_proj`: ∫ Π_a(x·z) Π_b(z·y) ω(dz) = δ_ab Π_a(x·y), display (2) of the paper.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1, display (2).
-/
import G2S1.Moments

noncomputable section
open Real Finset MeasureTheory Polynomial

namespace G2Kernel

/-! ### Elementary facts on `dot` -/

theorem dot_comm {N : ℕ} (x y : Sph N) : dot x y = dot y x := by
  unfold dot; exact real_inner_comm _ _

theorem norm_sph {N : ℕ} (x : Sph N) : ‖(x : Amb N)‖ = 1 := norm_eq_of_mem_sphere x

theorem abs_dot_le {N : ℕ} (x y : Sph N) : |dot x y| ≤ 1 := by
  have h := abs_real_inner_le_norm (x : Amb N) (y : Amb N)
  rw [norm_sph, norm_sph, one_mul] at h
  exact h

theorem dot_self {N : ℕ} (x : Sph N) : dot x x = 1 := by
  unfold dot
  rw [real_inner_self_eq_norm_sq, norm_sph, one_pow]

theorem continuous_dot_right {N : ℕ} (x : Sph N) : Continuous (fun z : Sph N => dot x z) := by
  unfold dot; exact continuous_const.inner continuous_subtype_val

theorem continuous_dot_left {N : ℕ} (y : Sph N) : Continuous (fun z : Sph N => dot z y) := by
  unfold dot; exact continuous_subtype_val.inner continuous_const

theorem lin_dot {N : ℕ} (x y z : Sph N) (J : ℝ) :
    J * dot x z + dot y z = @inner ℝ (Amb N) _ (J • (x : Amb N) + (y : Amb N)) (z : Amb N) := by
  unfold dot; rw [inner_add_left, real_inner_smul_left]

theorem norm_lin_sq {N : ℕ} (x y : Sph N) (J : ℝ) :
    ‖J • (x : Amb N) + (y : Amb N)‖ ^ 2 = J ^ 2 + 2 * J * dot x y + 1 := by
  rw [norm_add_sq_real, norm_smul, real_inner_smul_left, Real.norm_eq_abs, norm_sph, norm_sph, mul_one, sq_abs]
  unfold dot; ring

theorem two_point_even {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) (J : ℝ) (k : ℕ) :
    ∫ z : Sph N, (J * dot x z + dot y z) ^ (2 * k) ∂(omega N)
      = muMom N (2 * k) * (J ^ 2 + 2 * J * dot x y + 1) ^ k := by
  simp only [lin_dot]
  rw [sphere_moment hN, pow_mul, norm_lin_sq]
  ring

theorem two_point_odd {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) (J : ℝ) (k : ℕ) :
    ∫ z : Sph N, (J * dot x z + dot y z) ^ (2 * k + 1) ∂(omega N) = 0 := by
  simp only [lin_dot]
  rw [sphere_moment hN, muMom_odd, mul_zero]

/-! ### The two-point moments -/

/-- m(p, q) = ∫ (x·z)^p (y·z)^q ω(dz) -/
def mom2 {N : ℕ} (x y : Sph N) (p q : ℕ) : ℝ := ∫ z : Sph N, dot x z ^ p * dot y z ^ q ∂(omega N)

/-- r(p, q) = m(p, q) / (p! q!) -/
def rmom {N : ℕ} (x y : Sph N) (p q : ℕ) : ℝ := mom2 x y p q / ((p.factorial : ℝ) * (q.factorial : ℝ))

theorem integrable_dot_pow {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) (p q : ℕ) (c : ℝ) :
    Integrable (fun z : Sph N => c * (dot x z ^ p * dot y z ^ q)) (omega N) := by
  have := omega_isProbabilityMeasure N (by omega)
  refine integrable_of_abs_le (((continuous_dot_right x).pow p).mul ((continuous_dot_right y).pow q)
    |>.const_smul c |>.measurable) (|c|) (fun z => ?_)
  rw [abs_mul, abs_mul, abs_pow, abs_pow]
  have h1 := abs_dot_le x z
  have h2 := abs_dot_le y z
  have h3 : |dot x z| ^ p ≤ 1 := pow_le_one₀ (abs_nonneg _) h1
  have h4 : |dot y z| ^ q ≤ 1 := pow_le_one₀ (abs_nonneg _) h2
  have h5 : |dot x z| ^ p * |dot y z| ^ q ≤ 1 := by
    calc |dot x z| ^ p * |dot y z| ^ q ≤ 1 * 1 := mul_le_mul h3 h4 (by positivity) zero_le_one
      _ = 1 := one_mul 1
  calc |c| * (|dot x z| ^ p * |dot y z| ^ q) ≤ |c| * 1 := mul_le_mul_of_nonneg_left h5 (abs_nonneg c)
    _ = |c| := mul_one _

/-- the generating polynomial Q_n(X) = Σ_p r(p, n - p) X^p -/
def Qp {N : ℕ} (x y : Sph N) (n : ℕ) : Polynomial ℝ := ∑ p ∈ range (n + 1), C (rmom x y p (n - p)) * X ^ p

theorem eval_Qp {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) (n : ℕ) (J : ℝ) :
    (n.factorial : ℝ) * (Qp x y n).eval J = ∫ z : Sph N, (J * dot x z + dot y z) ^ n ∂(omega N) := by
  have hexp : ∀ z : Sph N, (J * dot x z + dot y z) ^ n
      = ∑ p ∈ range (n + 1), ((n.choose p : ℝ) * J ^ p) * (dot x z ^ p * dot y z ^ (n - p)) := by
    intro z
    rw [add_pow]
    refine sum_congr rfl (fun p _ => by ring)
  simp only [hexp]
  rw [integral_finset_sum _ (fun p _ => integrable_dot_pow hN x y p (n - p) _)]
  unfold Qp
  rw [eval_finset_sum, mul_sum]
  refine sum_congr rfl (fun p hp => ?_)
  simp only [eval_mul, eval_C, eval_pow, eval_X]
  rw [integral_const_mul]
  unfold rmom mom2
  have hpn : p ≤ n := Nat.lt_succ_iff.mp (mem_range.mp hp)
  have hc : ((n.choose p : ℕ) : ℝ) * (p.factorial : ℝ) * ((n - p).factorial : ℝ) = (n.factorial : ℝ) := by
    exact_mod_cast Nat.choose_mul_factorial_mul_factorial hpn
  have h1 : (p.factorial : ℝ) ≠ 0 := by positivity
  have h2 : ((n - p).factorial : ℝ) ≠ 0 := by positivity
  rw [← hc]
  field_simp

theorem coeff_Qp {N : ℕ} (x y : Sph N) (n p : ℕ) :
    (Qp x y n).coeff p = if p ≤ n then rmom x y p (n - p) else 0 := by
  unfold Qp
  rw [finset_sum_coeff]
  simp only [coeff_C_mul_X_pow]
  rw [sum_ite_eq]
  simp only [mem_range, Nat.lt_succ_iff]

theorem Qp_odd {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) (k : ℕ) : Qp x y (2 * k + 1) = 0 := by
  apply Polynomial.funext
  intro J
  have h := eval_Qp hN x y (2 * k + 1) J
  rw [two_point_odd hN] at h
  have hf : ((2 * k + 1).factorial : ℝ) ≠ 0 := by positivity
  rw [eval_zero]
  exact (mul_eq_zero.mp h).resolve_left hf

theorem Qp_succ2 {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) (k : ℕ) :
    Qp x y (2 * k + 2) = C (1 / ((2 * (k : ℝ) + 2) * (2 * (k : ℝ) + N))) *
      ((X ^ 2 + C (2 * dot x y) * X + 1) * Qp x y (2 * k)) := by
  apply Polynomial.funext
  intro J
  have h2 := eval_Qp hN x y (2 * k + 2) J
  have h0 := eval_Qp hN x y (2 * k) J
  rw [show 2 * k + 2 = 2 * (k + 1) by ring, two_point_even hN] at h2
  rw [two_point_even hN] at h0
  have hm := muMom_succ2 hN (2 * k)
  rw [show 2 * k + 2 = 2 * (k + 1) by ring] at hm
  simp only [eval_mul, eval_C, eval_add, eval_pow, eval_X, eval_one]
  have hN' : (1 : ℝ) ≤ N := by exact_mod_cast hN
  have hf0 : ((2 * k).factorial : ℝ) ≠ 0 := by positivity
  have hfac : ((2 * (k + 1)).factorial : ℝ) = (2 * (k : ℝ) + 2) * (2 * (k : ℝ) + 1) * ((2 * k).factorial : ℝ) := by
    rw [show 2 * (k + 1) = (2 * k + 1) + 1 by ring, Nat.factorial_succ, Nat.factorial_succ]
    push_cast; ring
  rw [hfac] at h2
  have hA : (Qp x y (2 * k)).eval J = muMom N (2 * k) * (J ^ 2 + 2 * J * dot x y + 1) ^ k / ((2 * k).factorial : ℝ) := by
    rw [eq_div_iff hf0]; linarith
  have hd1 : (2 * (k : ℝ) + 2) ≠ 0 := by positivity
  have hd2 : (2 * (k : ℝ) + 1) ≠ 0 := by positivity
  have hd3 : (2 * (k : ℝ) + N) ≠ 0 := by positivity
  have hB : (Qp x y (2 * (k + 1))).eval J = muMom N (2 * (k + 1)) * (J ^ 2 + 2 * J * dot x y + 1) ^ (k + 1) /
      ((2 * (k : ℝ) + 2) * (2 * (k : ℝ) + 1) * ((2 * k).factorial : ℝ)) := by
    rw [eq_div_iff (by positivity)]; linarith
  rw [show 2 * k + 2 = 2 * (k + 1) by ring, hB, hA]
  push_cast at hm
  have hm' : muMom N (2 * (k + 1)) = muMom N (2 * k) * (2 * (k : ℝ) + 1) / (2 * (k : ℝ) + N) := by
    rw [eq_div_iff hd3]; linarith
  rw [hm']
  field_simp
  ring

theorem coeff_quad_mul (c : ℝ) (Q : Polynomial ℝ) (p : ℕ) :
    ((X ^ 2 + C c * X + 1) * Q).coeff p
      = (if 2 ≤ p then Q.coeff (p - 2) else 0) + c * (if 1 ≤ p then Q.coeff (p - 1) else 0) + Q.coeff p := by
  rw [add_mul, add_mul, coeff_add, coeff_add, one_mul, coeff_X_pow_mul', mul_assoc, coeff_C_mul,
    show (X : Polynomial ℝ) * Q = X ^ 1 * Q by rw [pow_one], coeff_X_pow_mul']

theorem rmom_odd {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) (p q k : ℕ) (h : p + q = 2 * k + 1) : rmom x y p q = 0 := by
  have hc := coeff_Qp x y (2 * k + 1) p
  rw [Qp_odd hN, coeff_zero, if_pos (by omega), show 2 * k + 1 - p = q by omega] at hc
  exact hc.symm

theorem rmom_zero_zero {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) : rmom x y 0 0 = 1 := by
  have := omega_isProbabilityMeasure N (by omega)
  simp [rmom, mom2]

/-- the recurrence [*] for the two-point moments -/
theorem star_rmom {N : ℕ} (hN : 1 ≤ N) (x y : Sph N) (p q : ℕ) (hpq : 1 ≤ p + q) :
    ((p : ℝ) + q) * ((p : ℝ) + q - 2 + N) * rmom x y p q = starRHS (rmom x y) (dot x y) p q := by
  obtain ⟨k, hk | hk⟩ := Nat.even_or_odd' (p + q)
  · -- p + q = 2k, k ≥ 1
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    have hc := coeff_Qp x y (2 * k + 2) p
    rw [Qp_succ2 hN, coeff_C_mul, coeff_quad_mul, coeff_Qp, coeff_Qp, coeff_Qp,
      if_pos (show p ≤ 2 * k + 2 by omega), show 2 * k + 2 - p = q by omega] at hc
    have hq : (q : ℝ) = 2 * (k : ℝ) + 2 - p := by
      have : (p : ℝ) + q = 2 * (k : ℝ) + 2 := by exact_mod_cast (show p + q = 2 * k + 2 by omega)
      linarith
    have hN' : (1 : ℝ) ≤ N := by exact_mod_cast hN
    have hd : ((2 * (k : ℝ) + 2) * (2 * (k : ℝ) + N)) ≠ 0 := by positivity
    rw [← hc]
    unfold starRHS
    have e1 : (if 2 ≤ p then (if p - 2 ≤ 2 * k then rmom x y (p - 2) (2 * k - (p - 2)) else 0) else 0)
        = (if 2 ≤ p then rmom x y (p - 2) q else 0) := by
      split_ifs with h1 h2
      · rw [show 2 * k - (p - 2) = q by omega]
      · omega
      · rfl
    have e2 : (if 1 ≤ p then (if p - 1 ≤ 2 * k then rmom x y (p - 1) (2 * k - (p - 1)) else 0) else 0)
        = (if 1 ≤ p ∧ 1 ≤ q then rmom x y (p - 1) (q - 1) else 0) := by
      split_ifs with h1 h2 h3 h3
      · rw [show 2 * k - (p - 1) = q - 1 by omega]
      · omega
      · omega
      · rfl
      · omega
      · rfl
    have e3 : (if p ≤ 2 * k then rmom x y p (2 * k - p) else 0) = (if 2 ≤ q then rmom x y p (q - 2) else 0) := by
      split_ifs with h1 h2 h2
      · rw [show 2 * k - p = q - 2 by omega]
      · omega
      · omega
      · rfl
    rw [e1, e2, e3, hq]
    have e4 : (if 1 ≤ p ∧ 1 ≤ q then 2 * dot x y * rmom x y (p - 1) (q - 1) else 0)
        = 2 * dot x y * (if 1 ≤ p ∧ 1 ≤ q then rmom x y (p - 1) (q - 1) else 0) := by
      split_ifs <;> ring
    rw [e4]
    field_simp
    ring
  · -- p + q odd: both sides vanish
    rw [rmom_odd hN x y p q k hk, mul_zero]
    unfold starRHS
    have z1 : (if 2 ≤ p then rmom x y (p - 2) q else 0) = 0 := by
      split_ifs with h
      · exact rmom_odd hN x y _ _ (k - 1) (by omega)
      · rfl
    have z2 : (if 2 ≤ q then rmom x y p (q - 2) else 0) = 0 := by
      split_ifs with h
      · exact rmom_odd hN x y _ _ (k - 1) (by omega)
      · rfl
    have z3 : (if 1 ≤ p ∧ 1 ≤ q then 2 * dot x y * rmom x y (p - 1) (q - 1) else 0) = 0 := by
      split_ifs with h
      · rw [rmom_odd hN x y _ _ (k - 1) (by omega), mul_zero]
      · rfl
    rw [z1, z2, z3]
    ring

/-- (CF): the two-point moments in the zonal basis, ∫ (x·z)^p (y·z)^q ω(dz) = p! q! R(p, q)(x·y) -/
theorem two_point_CF {N : ℕ} (hN : 2 ≤ N) (x y : Sph N) (p q : ℕ) :
    ∫ z : Sph N, dot x z ^ p * dot y z ^ q ∂(omega N)
      = (p.factorial : ℝ) * (q.factorial : ℝ) * Rz N (dot x y) p q := by
  have h := star_unique hN (dot x y) (rmom x y) (Rz N (dot x y))
    (fun p q hpq => star_rmom (by omega) x y p q hpq) (fun p q _ => star_Rz hN (dot x y) p q)
    (by rw [rmom_zero_zero (by omega), Rz_zero_zero hN]) p q
  unfold rmom mom2 at h
  have h1 : (p.factorial : ℝ) ≠ 0 := by positivity
  have h2 : (q.factorial : ℝ) ≠ 0 := by positivity
  rw [div_eq_iff (by positivity)] at h
  rw [h]
  ring

/-! ### The projection identity -/

theorem zon_eq_sum {N : ℕ} (a : ℕ) (t : ℝ) :
    zon N a t = ∑ p ∈ range (a + 1), (zonPoly N a).coeff p * t ^ p := by
  rw [← eval_zonPoly, eval_eq_sum_range' (n := a + 1) (by have := natDegree_zonPoly_le N a; omega)]

/-- display (2): ∫ Π_a(x·z) Π_b(z·y) ω(dz) = δ_ab Π_a(x·y) -/
theorem zon_proj {N : ℕ} (hN : 2 ≤ N) (a b : ℕ) (x y : Sph N) :
    ∫ z : Sph N, zon N a (dot x z) * zon N b (dot z y) ∂(omega N) = if a = b then zon N a (dot x y) else 0 := by
  have hexp : ∀ z : Sph N, zon N a (dot x z) * zon N b (dot z y)
      = ∑ p ∈ range (a + 1), ∑ q ∈ range (b + 1),
          ((zonPoly N a).coeff p * (zonPoly N b).coeff q) * (dot x z ^ p * dot y z ^ q) := by
    intro z
    rw [zon_eq_sum, zon_eq_sum, dot_comm z y, sum_mul_sum]
    refine sum_congr rfl (fun p _ => sum_congr rfl (fun q _ => by ring))
  simp only [hexp]
  rw [integral_finset_sum _ (fun p _ => integrable_finset_sum _ (fun q _ => integrable_dot_pow (by omega) x y p q _))]
  rw [← proj_alg hN (dot x y) a b]
  refine sum_congr rfl (fun p _ => ?_)
  rw [integral_finset_sum _ (fun q _ => integrable_dot_pow (by omega) x y p q _)]
  refine sum_congr rfl (fun q _ => ?_)
  rw [integral_const_mul, two_point_CF hN]

end G2Kernel
