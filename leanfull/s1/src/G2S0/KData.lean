/-
G2S0.KData (stage S0 (b)): the paper's concrete data for N ≥ 2 and H3 for the paper's coefficients.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1 (display (3) and the lines after it):
k_ℓ(J) = Γ(N/2) Σ_{m ≥ 0} (J/2)^{ℓ+2m} / (m! Γ(ℓ+m+N/2)); d_ℓ = dim H_ℓ; C̃_ℓ the Gegenbauer polynomial C^{N/2-1}_ℓ normalized by
C̃_ℓ(1) = 1.
- `kConc`, `dConc`, `CConc`: the definitions; `CConc_one`: C̃_ℓ(1) = 1.
- `hKReg_kConc`: H3 (`hKReg`, G2Kernel.Named) for `kConc N`, N ≥ 2: positivity for J > 0, `ContDiff ℝ 2`, and the bounds
  c (ℓ+1)^j (J/2)^ℓ / ℓ! (j = 0, 1, 2) on every [a, b] with 0 < a.
Method: the series is differentiated termwise (`hasDerivAt_tsum_of_isPreconnected`) on intervals (-R, R); the j-th termwise
derivative of (x/2)^p is `dpow j p x`; the bounds use Γ(k + s) ≥ k! Γ(s) for s ≥ 1 and (l + m)! ≥ l! m!.
-/
import G2Kernel.Named
import G2Kernel.Proofs.CycleProof

noncomputable section
open Real Set

namespace G2Kernel

/-! ### The definitions -/

/-- the paper's coefficient, verbatim (Section 2.1, the line after display (3)):
k_ℓ(J) = Γ(N/2) Σ_{m ≥ 0} (J/2)^{ℓ+2m} / (m! Γ(ℓ+m+N/2)) -/
def kConc (N : ℕ) (l : ℕ) (J : ℝ) : ℝ :=
  Real.Gamma ((N : ℝ) / 2) *
    ∑' m : ℕ, (J / 2) ^ (l + 2 * m) / ((m.factorial : ℝ) * Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2))

/-- d_ℓ = dim H_ℓ, the dimension of the spherical harmonics of degree ℓ on S^{N-1}:
C(ℓ + N - 1, ℓ) - C(ℓ + N - 3, ℓ - 2), the second term only for ℓ ≥ 2 -/
def dConc (N : ℕ) (l : ℕ) : ℝ :=
  (Nat.choose (l + N - 1) l : ℝ) - (if 2 ≤ l then (Nat.choose (l + N - 3) (l - 2) : ℝ) else 0)

/-- C̃_ℓ: C̃_0 = 1, C̃_1(t) = t, and the normalized three-term recurrence of C^λ_ℓ with 2λ = N - 2,
C̃_{n+1}(t) = ((2n + N - 2) t C̃_n(t) - n C̃_{n-1}(t)) / (n + N - 2) for n ≥ 1 (N = 2: the Chebyshev polynomial T_ℓ) -/
def CConc (N : ℕ) : ℕ → ℝ → ℝ
  | 0, _ => 1
  | 1, t => t
  | n + 2, t => ((2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * t * CConc N (n + 1) t - ((n : ℝ) + 1) * CConc N n t) /
      (((n : ℝ) + 1) + ((N : ℝ) - 2))

/-- the normalization C̃_ℓ(1) = 1 -/
theorem CConc_one (N : ℕ) (hN : 2 ≤ N) : ∀ l : ℕ, CConc N l 1 = 1
  | 0 => rfl
  | 1 => rfl
  | n + 2 => by
    rw [CConc, CConc_one N hN (n + 1), CConc_one N hN n]
    have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
    have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg n
    have hd : ((n : ℝ) + 1) + ((N : ℝ) - 2) ≠ 0 := ne_of_gt (by linarith)
    rw [div_eq_one_iff_eq hd]
    ring

/-! ### The terms and their derivatives -/

/-- the coefficient of the m-th term: Γ(N/2) / (m! Γ(ℓ + m + N/2)) -/
def kCoef (N l m : ℕ) : ℝ := Real.Gamma ((N : ℝ) / 2) / ((m.factorial : ℝ) * Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2))

/-- the j-th derivative of x ↦ (x/2)^p -/
def dpow (j p : ℕ) (x : ℝ) : ℝ := (p.descFactorial j : ℝ) * (x / 2) ^ (p - j) * (1 / 2) ^ j

/-- the j-th termwise derivative series of k_ℓ -/
def kSer (N l j : ℕ) (x : ℝ) : ℝ := ∑' m : ℕ, kCoef N l m * dpow j (l + 2 * m) x

theorem kConc_eq_kSer (N l : ℕ) : kConc N l = kSer N l 0 := by
  funext x
  simp only [kConc, kSer, kCoef, dpow, Nat.descFactorial_zero, Nat.cast_one, one_mul, Nat.sub_zero, pow_zero, mul_one]
  rw [← tsum_mul_left]
  congr 1
  funext m
  ring

theorem hasDerivAt_dpow (j p : ℕ) (x : ℝ) : HasDerivAt (dpow j p) (dpow (j + 1) p x) x := by
  have h := ((((hasDerivAt_id x).div_const 2).pow (p - j)).const_mul (p.descFactorial j : ℝ)).mul_const
    ((1 / 2 : ℝ) ^ j)
  have hf : dpow j p = fun y => (p.descFactorial j : ℝ) * (id y / 2) ^ (p - j) * (1 / 2) ^ j := rfl
  rw [hf]
  convert h using 1
  simp only [dpow, Nat.descFactorial_succ, Nat.cast_mul, id, pow_succ, Nat.sub_sub]
  ring

/-! ### Bounds on the coefficients -/

theorem Gamma_nat_add_ge {s : ℝ} (hs : 1 ≤ s) (k : ℕ) :
    (k.factorial : ℝ) * Real.Gamma s ≤ Real.Gamma ((k : ℝ) + s) := by
  induction k with
  | zero => simp
  | succ k ih =>
    have hk0 : (0 : ℝ) ≤ k := Nat.cast_nonneg k
    have hks : 0 < (k : ℝ) + s := by linarith
    have hG : Real.Gamma (((k + 1 : ℕ) : ℝ) + s) = ((k : ℝ) + s) * Real.Gamma ((k : ℝ) + s) := by
      rw [show (((k + 1 : ℕ) : ℝ) + s) = ((k : ℝ) + s) + 1 by push_cast; ring]
      exact Real.Gamma_add_one hks.ne'
    rw [hG, Nat.factorial_succ, Nat.cast_mul]
    have hΓ : 0 ≤ Real.Gamma s := (Real.Gamma_pos_of_pos (by linarith)).le
    have h0 : 0 ≤ (k.factorial : ℝ) * Real.Gamma s := mul_nonneg (Nat.cast_nonneg _) hΓ
    have hk1 : ((k + 1 : ℕ) : ℝ) ≤ (k : ℝ) + s := by push_cast; linarith
    calc ((k + 1 : ℕ) : ℝ) * (k.factorial : ℝ) * Real.Gamma s
        = ((k + 1 : ℕ) : ℝ) * ((k.factorial : ℝ) * Real.Gamma s) := by ring
      _ ≤ ((k : ℝ) + s) * Real.Gamma ((k : ℝ) + s) := mul_le_mul hk1 ih h0 (by linarith)

theorem Gamma_arg_pos {N : ℕ} (hN : 2 ≤ N) (l m : ℕ) : 0 < Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2) := by
  apply Real.Gamma_pos_of_pos
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hl : (0 : ℝ) ≤ l := Nat.cast_nonneg l
  have hm : (0 : ℝ) ≤ m := Nat.cast_nonneg m
  linarith

theorem kCoef_pos {N : ℕ} (hN : 2 ≤ N) (l m : ℕ) : 0 < kCoef N l m := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  unfold kCoef
  apply div_pos (Real.Gamma_pos_of_pos (by linarith))
  exact mul_pos (by exact_mod_cast m.factorial_pos) (Gamma_arg_pos hN l m)

theorem kCoef_le {N : ℕ} (hN : 2 ≤ N) (l m : ℕ) : kCoef N l m ≤ 1 / ((l.factorial : ℝ) * m.factorial) := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hs1 : (1 : ℝ) ≤ (N : ℝ) / 2 := by linarith
  have hΓs := Real.Gamma_pos_of_pos (by linarith : (0 : ℝ) < (N : ℝ) / 2)
  have hG' := Gamma_arg_pos hN l m
  have hG := Gamma_nat_add_ge hs1 (l + m)
  have hcast : (((l + m : ℕ) : ℝ) + (N : ℝ) / 2) = (l : ℝ) + m + (N : ℝ) / 2 := by push_cast; ring
  rw [hcast] at hG
  have hfac : (l.factorial : ℝ) * m.factorial ≤ ((l + m).factorial : ℝ) := by
    exact_mod_cast Nat.le_of_dvd (Nat.factorial_pos _) (Nat.factorial_mul_factorial_dvd_factorial_add l m)
  have hlm : (0 : ℝ) < (l.factorial : ℝ) * m.factorial := by positivity
  have hmf : (0 : ℝ) < (m.factorial : ℝ) := by exact_mod_cast m.factorial_pos
  have hm1 : (1 : ℝ) ≤ (m.factorial : ℝ) := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr (Nat.factorial_ne_zero m)
  unfold kCoef
  rw [div_le_div_iff₀ (mul_pos hmf hG') hlm]
  have h1 : Real.Gamma ((N : ℝ) / 2) * ((l.factorial : ℝ) * m.factorial)
      ≤ Real.Gamma ((N : ℝ) / 2) * ((l + m).factorial : ℝ) := mul_le_mul_of_nonneg_left hfac hΓs.le
  have h3 : Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2) ≤ (m.factorial : ℝ) * Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2) :=
    le_mul_of_one_le_left hG'.le hm1
  nlinarith

/-! ### Summability and the termwise derivatives -/

/-- the local bound of the j-th derivative terms on |x| ≤ R -/
def kLoc (N l j : ℕ) (R : ℝ) (m : ℕ) : ℝ := kCoef N l m * ((l + 2 * m : ℕ) : ℝ) ^ j * (R / 2) ^ (l + 2 * m)

theorem summable_kLoc {N : ℕ} (hN : 2 ≤ N) (l j : ℕ) {R : ℝ} (hR : 2 ≤ R) : Summable (kLoc N l j R) := by
  have hR2 : (0 : ℝ) ≤ R / 2 := by linarith
  have hsum := (summable_poly_pow_div_factorial j (sq_nonneg (R / 2))).mul_left (((l : ℝ) + 2) ^ j * (R / 2) ^ l)
  refine Summable.of_nonneg_of_le (fun m => ?_) (fun m => ?_) hsum
  · unfold kLoc
    exact mul_nonneg (mul_nonneg (kCoef_pos hN l m).le (by positivity)) (by positivity)
  · unfold kLoc
    have hk := kCoef_le hN l m
    have hl1 : (1 : ℝ) ≤ (l.factorial : ℝ) := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr (Nat.factorial_ne_zero l)
    have hmf : (0 : ℝ) < (m.factorial : ℝ) := by exact_mod_cast m.factorial_pos
    have hk' : kCoef N l m ≤ 1 / (m.factorial : ℝ) := by
      calc kCoef N l m ≤ 1 / ((l.factorial : ℝ) * m.factorial) := hk
        _ ≤ 1 / (m.factorial : ℝ) := by
          apply one_div_le_one_div_of_le hmf
          nlinarith
    have he : ((l + 2 * m : ℕ) : ℝ) ≤ ((l : ℝ) + 2) * ((m : ℝ) + 1) := by
      push_cast
      have : (0 : ℝ) ≤ (l : ℝ) * m := by positivity
      nlinarith
    have hpow : ((l + 2 * m : ℕ) : ℝ) ^ j ≤ ((l : ℝ) + 2) ^ j * ((m : ℝ) + 1) ^ j := by
      rw [← mul_pow]
      exact pow_le_pow_left₀ (by positivity) he j
    have hRp : (R / 2) ^ (l + 2 * m) = (R / 2) ^ l * ((R / 2) ^ 2) ^ m := by
      rw [pow_add, pow_mul]
    rw [hRp]
    have hA : 0 ≤ ((l + 2 * m : ℕ) : ℝ) ^ j * ((R / 2) ^ l * ((R / 2) ^ 2) ^ m) := by positivity
    calc kCoef N l m * ((l + 2 * m : ℕ) : ℝ) ^ j * ((R / 2) ^ l * ((R / 2) ^ 2) ^ m)
        = kCoef N l m * (((l + 2 * m : ℕ) : ℝ) ^ j * ((R / 2) ^ l * ((R / 2) ^ 2) ^ m)) := by ring
      _ ≤ 1 / (m.factorial : ℝ) * (((l + 2 * m : ℕ) : ℝ) ^ j * ((R / 2) ^ l * ((R / 2) ^ 2) ^ m)) :=
          mul_le_mul_of_nonneg_right hk' hA
      _ ≤ 1 / (m.factorial : ℝ) * ((((l : ℝ) + 2) ^ j * ((m : ℝ) + 1) ^ j) * ((R / 2) ^ l * ((R / 2) ^ 2) ^ m)) := by
          apply mul_le_mul_of_nonneg_left _ (by positivity)
          exact mul_le_mul_of_nonneg_right hpow (by positivity)
      _ = ((l : ℝ) + 2) ^ j * (R / 2) ^ l * (((m : ℝ) + 1) ^ j * ((R / 2) ^ 2) ^ m / (m.factorial : ℝ)) := by
          field_simp

theorem abs_dpow_le {j p : ℕ} {x R : ℝ} (hR : 2 ≤ R) (hx : |x| ≤ R) :
    |dpow j p x| ≤ (p : ℝ) ^ j * (R / 2) ^ p := by
  unfold dpow
  have h1 : (p.descFactorial j : ℝ) ≤ (p : ℝ) ^ j := by exact_mod_cast Nat.descFactorial_le_pow p j
  have hx2 : |x / 2| ≤ R / 2 := by rw [abs_div, abs_two]; linarith
  have h2 : |x / 2| ^ (p - j) ≤ (R / 2) ^ p :=
    calc |x / 2| ^ (p - j) ≤ (R / 2) ^ (p - j) := pow_le_pow_left₀ (abs_nonneg _) hx2 _
      _ ≤ (R / 2) ^ p := pow_le_pow_right₀ (by linarith) (Nat.sub_le p j)
  have h3 : (1 / 2 : ℝ) ^ j ≤ 1 := pow_le_one₀ (by norm_num) (by norm_num)
  rw [abs_mul, abs_mul, abs_pow, abs_pow, Nat.abs_cast, abs_of_pos (by norm_num : (0 : ℝ) < 1 / 2)]
  calc (p.descFactorial j : ℝ) * |x / 2| ^ (p - j) * (1 / 2) ^ j
      ≤ (p : ℝ) ^ j * (R / 2) ^ p * 1 := by
        apply mul_le_mul _ h3 (by positivity) (by positivity)
        exact mul_le_mul h1 h2 (by positivity) (by positivity)
    _ = (p : ℝ) ^ j * (R / 2) ^ p := by ring

theorem summable_kTerm {N : ℕ} (hN : 2 ≤ N) (l j : ℕ) (x : ℝ) :
    Summable (fun m => kCoef N l m * dpow j (l + 2 * m) x) := by
  have hR : (2 : ℝ) ≤ max 2 (|x| + 1) := le_max_left _ _
  have hx : |x| ≤ max 2 (|x| + 1) := le_trans (by linarith) (le_max_right _ _)
  refine Summable.of_norm_bounded (summable_kLoc hN l j hR) (fun m => ?_)
  rw [Real.norm_eq_abs, abs_mul, abs_of_pos (kCoef_pos hN l m)]
  unfold kLoc
  rw [mul_assoc]
  exact mul_le_mul_of_nonneg_left (abs_dpow_le hR hx) (kCoef_pos hN l m).le

theorem hasDerivAt_kSer {N : ℕ} (hN : 2 ≤ N) (l j : ℕ) (x : ℝ) :
    HasDerivAt (kSer N l j) (kSer N l (j + 1) x) x := by
  set R := max 2 (|x| + 1) with hRdef
  have hR : (2 : ℝ) ≤ R := le_max_left _ _
  have hxR : |x| < R := lt_of_lt_of_le (by linarith) (le_max_right _ _)
  have hx : x ∈ Ioo (-R) R := ⟨by linarith [neg_abs_le x], by linarith [le_abs_self x]⟩
  unfold kSer
  refine hasDerivAt_tsum_of_isPreconnected (summable_kLoc hN l (j + 1) hR) isOpen_Ioo isPreconnected_Ioo
    (fun m y _ => (hasDerivAt_dpow j (l + 2 * m) y).const_mul (kCoef N l m)) (fun m y hy => ?_) hx
    (summable_kTerm hN l j x) hx
  have hy' : |y| ≤ R := abs_le.mpr ⟨hy.1.le, hy.2.le⟩
  rw [Real.norm_eq_abs, abs_mul, abs_of_pos (kCoef_pos hN l m)]
  unfold kLoc
  rw [mul_assoc]
  exact mul_le_mul_of_nonneg_left (abs_dpow_le hR hy') (kCoef_pos hN l m).le

theorem deriv_kSer {N : ℕ} (hN : 2 ≤ N) (l j : ℕ) : deriv (kSer N l j) = kSer N l (j + 1) := by
  funext x
  exact (hasDerivAt_kSer hN l j x).deriv

theorem differentiable_kSer {N : ℕ} (hN : 2 ≤ N) (l j : ℕ) : Differentiable ℝ (kSer N l j) :=
  fun x => (hasDerivAt_kSer hN l j x).differentiableAt

/-! ### H3 for the paper's k -/

theorem kConc_pos {N : ℕ} (hN : 2 ≤ N) (l : ℕ) {J : ℝ} (hJ : 0 < J) : 0 < kConc N l J := by
  rw [kConc_eq_kSer]
  unfold kSer
  have hterm : ∀ m, 0 < kCoef N l m * dpow 0 (l + 2 * m) J := by
    intro m
    apply mul_pos (kCoef_pos hN l m)
    simp only [dpow, Nat.descFactorial_zero, Nat.cast_one, one_mul, Nat.sub_zero, pow_zero, mul_one]
    positivity
  exact Summable.tsum_pos (summable_kTerm hN l 0 J) (fun m => (hterm m).le) 0 (hterm 0)

theorem contDiff_kConc {N : ℕ} (hN : 2 ≤ N) (l : ℕ) : ContDiff ℝ 2 (kConc N l) := by
  rw [kConc_eq_kSer, show (2 : WithTop ℕ∞) = 1 + 1 from rfl, contDiff_succ_iff_deriv]
  refine ⟨differentiable_kSer hN l 0, by simp, ?_⟩
  rw [deriv_kSer hN l 0, contDiff_one_iff_deriv, deriv_kSer hN l 1]
  exact ⟨differentiable_kSer hN l 1, (differentiable_kSer hN l 2).continuous⟩

/-- the constant of the bound of the j-th derivative on [a, b] -/
def kConst (a b : ℝ) (j : ℕ) : ℝ := (2 / a) ^ j * ∑' m : ℕ, ((m : ℝ) + 1) ^ j * ((b / 2) ^ 2) ^ m / (m.factorial : ℝ)

theorem kConst_nonneg {a b : ℝ} (ha : 0 < a) (j : ℕ) : 0 ≤ kConst a b j := by
  unfold kConst
  exact mul_nonneg (by positivity) (tsum_nonneg (fun m => by positivity))

/-- the term bound on [a, b] -/
theorem kTerm_le {N : ℕ} (hN : 2 ≤ N) {a b J : ℝ} (ha : 0 < a) (hJ : J ∈ Icc a b) (l j m : ℕ) :
    kCoef N l m * dpow j (l + 2 * m) J ≤
      ((l : ℝ) + 1) ^ j * (J / 2) ^ l / (l.factorial : ℝ) *
        ((2 / a) ^ j * (((m : ℝ) + 1) ^ j * ((b / 2) ^ 2) ^ m / (m.factorial : ℝ))) := by
  obtain ⟨haJ, hJb⟩ := hJ
  have hJ0 : 0 < J := lt_of_lt_of_le ha haJ
  have hJ2 : 0 < J / 2 := by linarith
  set p := l + 2 * m with hp
  -- descFactorial p j * (J/2)^(p - j) ≤ p^j * (J/2)^p * (2/a)^j
  have hD : (p.descFactorial j : ℝ) * (J / 2) ^ (p - j) ≤ (p : ℝ) ^ j * (J / 2) ^ p * (2 / a) ^ j := by
    by_cases hjp : j ≤ p
    · have hsplit : (J / 2) ^ p = (J / 2) ^ (p - j) * (J / 2) ^ j := by
        rw [← pow_add, Nat.sub_add_cancel hjp]
      have hinv : (1 : ℝ) ≤ (J / 2) ^ j * (2 / a) ^ j := by
        rw [← mul_pow]
        apply one_le_pow₀
        rw [div_mul_div_comm, le_div_iff₀ (by positivity)]
        linarith
      have h1 : (p.descFactorial j : ℝ) ≤ (p : ℝ) ^ j := by exact_mod_cast Nat.descFactorial_le_pow p j
      have hq : 0 ≤ (J / 2) ^ (p - j) := by positivity
      calc (p.descFactorial j : ℝ) * (J / 2) ^ (p - j)
          ≤ (p : ℝ) ^ j * (J / 2) ^ (p - j) := mul_le_mul_of_nonneg_right h1 hq
        _ ≤ (p : ℝ) ^ j * ((J / 2) ^ (p - j) * ((J / 2) ^ j * (2 / a) ^ j)) := by
            apply mul_le_mul_of_nonneg_left _ (by positivity)
            nlinarith
        _ = (p : ℝ) ^ j * (J / 2) ^ p * (2 / a) ^ j := by rw [hsplit]; ring
    · have h0 : p.descFactorial j = 0 := Nat.descFactorial_eq_zero_iff_lt.mpr (by omega)
      rw [h0, Nat.cast_zero, zero_mul]
      positivity
  have hpj : (p : ℝ) ^ j ≤ ((l : ℝ) + 1) ^ j * (2 ^ j * ((m : ℝ) + 1) ^ j) := by
    rw [← mul_pow, ← mul_pow]
    apply pow_le_pow_left₀ (by positivity)
    rw [hp]
    push_cast
    have : (0 : ℝ) ≤ (l : ℝ) * m := by positivity
    nlinarith
  have hJp : (J / 2) ^ p ≤ (J / 2) ^ l * ((b / 2) ^ 2) ^ m := by
    rw [hp, pow_add, pow_mul]
    apply mul_le_mul_of_nonneg_left _ (by positivity)
    apply pow_le_pow_left₀ (by positivity)
    apply pow_le_pow_left₀ hJ2.le
    linarith
  have hk := kCoef_le hN l m
  have hkp := kCoef_pos hN l m
  have hlf : (0 : ℝ) < (l.factorial : ℝ) := by exact_mod_cast l.factorial_pos
  have hmf : (0 : ℝ) < (m.factorial : ℝ) := by exact_mod_cast m.factorial_pos
  unfold dpow
  have hhalf : (0 : ℝ) ≤ (1 / 2 : ℝ) ^ j := by positivity
  have hX : 0 ≤ (p.descFactorial j : ℝ) * (J / 2) ^ (p - j) := by positivity
  calc kCoef N l m * ((p.descFactorial j : ℝ) * (J / 2) ^ (p - j) * (1 / 2) ^ j)
      ≤ 1 / ((l.factorial : ℝ) * m.factorial) * ((p : ℝ) ^ j * (J / 2) ^ p * (2 / a) ^ j * (1 / 2) ^ j) := by
        apply mul_le_mul hk _ (by positivity) (by positivity)
        exact mul_le_mul_of_nonneg_right hD hhalf
    _ ≤ 1 / ((l.factorial : ℝ) * m.factorial) *
          ((((l : ℝ) + 1) ^ j * (2 ^ j * ((m : ℝ) + 1) ^ j)) * ((J / 2) ^ l * ((b / 2) ^ 2) ^ m) * (2 / a) ^ j *
            (1 / 2) ^ j) := by
        apply mul_le_mul_of_nonneg_left _ (by positivity)
        apply mul_le_mul_of_nonneg_right _ hhalf
        apply mul_le_mul_of_nonneg_right _ (by positivity)
        exact mul_le_mul hpj hJp (by positivity) (by positivity)
    _ = ((l : ℝ) + 1) ^ j * (J / 2) ^ l / (l.factorial : ℝ) *
          ((2 / a) ^ j * (((m : ℝ) + 1) ^ j * ((b / 2) ^ 2) ^ m / (m.factorial : ℝ))) := by
        have h2 : (2 : ℝ) ^ j * (1 / 2) ^ j = 1 := by rw [← mul_pow]; norm_num
        calc 1 / ((l.factorial : ℝ) * m.factorial) *
              ((((l : ℝ) + 1) ^ j * (2 ^ j * ((m : ℝ) + 1) ^ j)) * ((J / 2) ^ l * ((b / 2) ^ 2) ^ m) * (2 / a) ^ j *
                (1 / 2) ^ j)
            = 1 / ((l.factorial : ℝ) * m.factorial) * (((l : ℝ) + 1) ^ j * ((m : ℝ) + 1) ^ j *
                ((J / 2) ^ l * ((b / 2) ^ 2) ^ m) * (2 / a) ^ j) * ((2 : ℝ) ^ j * (1 / 2) ^ j) := by ring
          _ = _ := by rw [h2]; ring

/-- the bound of the j-th derivative on [a, b] -/
theorem abs_kSer_le {N : ℕ} (hN : 2 ≤ N) {a b J : ℝ} (ha : 0 < a) (hJ : J ∈ Icc a b) (l j : ℕ) :
    |kSer N l j J| ≤ kConst a b j * ((l : ℝ) + 1) ^ j * (J / 2) ^ l / (l.factorial : ℝ) := by
  have hJ0 : 0 < J := lt_of_lt_of_le ha hJ.1
  have hnn : ∀ m, 0 ≤ kCoef N l m * dpow j (l + 2 * m) J := by
    intro m
    apply mul_nonneg (kCoef_pos hN l m).le
    unfold dpow
    positivity
  have hs1 := summable_kTerm hN l j J
  have hs2 : Summable (fun m : ℕ => ((l : ℝ) + 1) ^ j * (J / 2) ^ l / (l.factorial : ℝ) *
      ((2 / a) ^ j * (((m : ℝ) + 1) ^ j * ((b / 2) ^ 2) ^ m / (m.factorial : ℝ)))) :=
    ((summable_poly_pow_div_factorial j (sq_nonneg (b / 2))).mul_left ((2 / a) ^ j)).mul_left _
  unfold kSer
  rw [abs_of_nonneg (tsum_nonneg hnn)]
  calc ∑' m, kCoef N l m * dpow j (l + 2 * m) J
      ≤ ∑' m : ℕ, ((l : ℝ) + 1) ^ j * (J / 2) ^ l / (l.factorial : ℝ) *
          ((2 / a) ^ j * (((m : ℝ) + 1) ^ j * ((b / 2) ^ 2) ^ m / (m.factorial : ℝ))) :=
        Summable.tsum_le_tsum (fun m => kTerm_le hN ha hJ l j m) hs1 hs2
    _ = kConst a b j * ((l : ℝ) + 1) ^ j * (J / 2) ^ l / (l.factorial : ℝ) := by
        rw [tsum_mul_left, tsum_mul_left]
        unfold kConst
        ring

/-- **H3 for the paper's k**: `hKReg (kConc N)` for every N ≥ 2 -/
theorem hKReg_kConc (N : ℕ) (hN : 2 ≤ N) : hKReg (kConc N) := by
  refine ⟨fun l J hJ => kConc_pos hN l hJ, fun l => contDiff_kConc hN l, fun a b ha hab => ?_⟩
  have h0 := kConst_nonneg (b := b) ha 0
  have h1 := kConst_nonneg (b := b) ha 1
  have h2 := kConst_nonneg (b := b) ha 2
  refine ⟨1 + kConst a b 0 + kConst a b 1 + kConst a b 2, by linarith, fun l J hJ => ?_⟩
  have hJ0 : 0 < J := lt_of_lt_of_le ha hJ.1
  have hX : 0 ≤ (J / 2) ^ l / (l.factorial : ℝ) := by positivity
  have hl1 : (0 : ℝ) ≤ (l : ℝ) + 1 := by positivity
  have hc0 : kConst a b 0 ≤ 1 + kConst a b 0 + kConst a b 1 + kConst a b 2 := by linarith
  have hc1 : kConst a b 1 ≤ 1 + kConst a b 0 + kConst a b 1 + kConst a b 2 := by linarith
  have hc2 : kConst a b 2 ≤ 1 + kConst a b 0 + kConst a b 1 + kConst a b 2 := by linarith
  refine ⟨?_, ?_, ?_⟩
  · rw [kConc_eq_kSer]
    have := abs_kSer_le hN ha hJ l 0
    rw [pow_zero, mul_one] at this
    calc |kSer N l 0 J| ≤ kConst a b 0 * (J / 2) ^ l / (l.factorial : ℝ) := this
      _ ≤ (1 + kConst a b 0 + kConst a b 1 + kConst a b 2) * (J / 2) ^ l / (l.factorial : ℝ) := by
          rw [mul_div_assoc, mul_div_assoc]
          exact mul_le_mul_of_nonneg_right hc0 hX
  · rw [kConc_eq_kSer, deriv_kSer hN l 0]
    have := abs_kSer_le hN ha hJ l 1
    rw [pow_one] at this
    calc |kSer N l (0 + 1) J| ≤ kConst a b 1 * ((l : ℝ) + 1) * (J / 2) ^ l / (l.factorial : ℝ) := this
      _ ≤ (1 + kConst a b 0 + kConst a b 1 + kConst a b 2) * ((l : ℝ) + 1) * (J / 2) ^ l / (l.factorial : ℝ) := by
          rw [mul_div_assoc, mul_div_assoc, mul_assoc, mul_assoc]
          exact mul_le_mul_of_nonneg_right hc1 (mul_nonneg hl1 hX)
  · rw [kConc_eq_kSer, iteratedDeriv_succ, iteratedDeriv_one, deriv_kSer hN l 0, deriv_kSer hN l (0 + 1)]
    have := abs_kSer_le hN ha hJ l 2
    calc |kSer N l (0 + 1 + 1) J| ≤ kConst a b 2 * ((l : ℝ) + 1) ^ 2 * (J / 2) ^ l / (l.factorial : ℝ) := this
      _ ≤ (1 + kConst a b 0 + kConst a b 1 + kConst a b 2) * ((l : ℝ) + 1) ^ 2 * (J / 2) ^ l /
            (l.factorial : ℝ) := by
          rw [mul_div_assoc, mul_div_assoc, mul_assoc, mul_assoc]
          exact mul_le_mul_of_nonneg_right hc2 (mul_nonneg (by positivity) hX)

end G2Kernel

#print axioms G2Kernel.CConc_one
#print axioms G2Kernel.hasDerivAt_kSer
#print axioms G2Kernel.contDiff_kConc
#print axioms G2Kernel.kConc_pos
#print axioms G2Kernel.abs_kSer_le
#print axioms G2Kernel.hKReg_kConc
