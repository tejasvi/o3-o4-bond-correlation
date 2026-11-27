/-
G2S1.Alg (stage S1, algebra): the power-series coefficients of k_ℓ, the three-term recurrence of the zonal polynomials
Π_e(t) = d_e C̃_e(t), the shift identity of the Jacobi operator, and (P_n): t^n = n! Σ_e c'(e, n) Π_e(t).
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1 (displays (2), (3)).
- `cK N e p` = c'(e, p): the coefficient of J^p in k_e(J) = Σ_m kCoef N e m (J/2)^(e+2m) (zero unless p = e + 2m).
- `zon N e t` = d_e C̃_e(t); `zon_rec`: t Π_e = α_e Π_{e+1} + β_e Π_{e-1} (β_0 = 0, β_1 = 1).
- `jacobi_sum`: t Σ_{e<M} v_e Π_e = Σ_{e<M+1} (J v)_e Π_e; `pow_eq_sum_zon`: (P_n).
-/
import G2S0.KData

noncomputable section
open Real Finset

namespace G2Kernel

/-! ### Ratios of the coefficients `kCoef` -/

theorem kCoef_succ_m {N : ℕ} (hN : 2 ≤ N) (l m : ℕ) :
    kCoef N l (m + 1) * (((m : ℝ) + 1) * ((l : ℝ) + m + (N : ℝ) / 2)) = kCoef N l m := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hs : (0 : ℝ) < (l : ℝ) + m + (N : ℝ) / 2 := by positivity
  unfold kCoef
  have hG : Real.Gamma ((l : ℝ) + ((m + 1 : ℕ) : ℝ) + (N : ℝ) / 2)
      = ((l : ℝ) + m + (N : ℝ) / 2) * Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2) := by
    rw [show (l : ℝ) + ((m + 1 : ℕ) : ℝ) + (N : ℝ) / 2 = ((l : ℝ) + m + (N : ℝ) / 2) + 1 by push_cast; ring]
    exact Real.Gamma_add_one hs.ne'
  rw [hG, Nat.factorial_succ]
  have hΓ := Gamma_arg_pos hN l m
  have hmf : (0 : ℝ) < (m.factorial : ℝ) := by exact_mod_cast m.factorial_pos
  push_cast
  rw [div_mul_eq_mul_div, div_eq_div_iff (by positivity) (by positivity)]
  ring

theorem kCoef_succ_l {N : ℕ} (hN : 2 ≤ N) (l m : ℕ) :
    kCoef N (l + 1) m * ((l : ℝ) + m + (N : ℝ) / 2) = kCoef N l m := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hs : (0 : ℝ) < (l : ℝ) + m + (N : ℝ) / 2 := by positivity
  unfold kCoef
  have hG : Real.Gamma (((l + 1 : ℕ) : ℝ) + (m : ℝ) + (N : ℝ) / 2)
      = ((l : ℝ) + m + (N : ℝ) / 2) * Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2) := by
    rw [show ((l + 1 : ℕ) : ℝ) + (m : ℝ) + (N : ℝ) / 2 = ((l : ℝ) + m + (N : ℝ) / 2) + 1 by push_cast; ring]
    exact Real.Gamma_add_one hs.ne'
  rw [hG]
  have hΓ := Gamma_arg_pos hN l m
  have hmf : (0 : ℝ) < (m.factorial : ℝ) := by exact_mod_cast m.factorial_pos
  rw [div_mul_eq_mul_div, div_eq_div_iff (by positivity) (by positivity)]
  ring

theorem kCoef_zero_zero {N : ℕ} (hN : 2 ≤ N) : kCoef N 0 0 = 1 := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  unfold kCoef
  have h := Real.Gamma_pos_of_pos (by linarith : (0 : ℝ) < (N : ℝ) / 2)
  simp only [Nat.factorial_zero, Nat.cast_one, one_mul, Nat.cast_zero, zero_add]
  exact div_self h.ne'

/-! ### The coefficient c'(e, p) of J^p in k_e(J) -/

/-- c'(e, p): the coefficient of J^p in k_e(J); `kCoef N e m / 2^p` when p = e + 2m, otherwise 0 -/
def cK (N e p : ℕ) : ℝ := if e ≤ p ∧ (p - e) % 2 = 0 then kCoef N e ((p - e) / 2) / 2 ^ p else 0

theorem cK_eq (N e m : ℕ) : cK N e (e + 2 * m) = kCoef N e m / 2 ^ (e + 2 * m) := by
  unfold cK
  rw [if_pos ⟨by omega, by omega⟩, show (e + 2 * m - e) / 2 = m by omega]

theorem cK_of_lt {N e p : ℕ} (h : p < e) : cK N e p = 0 := by
  unfold cK
  rw [if_neg (by omega)]

theorem cK_odd (N e m : ℕ) : cK N e (e + 2 * m + 1) = 0 := by
  unfold cK
  rw [if_neg (by omega)]

theorem cK_zero_zero {N : ℕ} (hN : 2 ≤ N) : cK N 0 0 = 1 := by
  have h := cK_eq N 0 0
  simp only [mul_zero, add_zero, pow_zero, div_one] at h
  rw [h, kCoef_zero_zero hN]

/-- every `p` is below `e`, or `e + 2m`, or `e + 2m + 1` -/
theorem cases_e (e p : ℕ) : p < e ∨ (∃ m, p = e + 2 * m) ∨ (∃ m, p = e + 2 * m + 1) := by
  rcases Nat.lt_or_ge p e with h | h
  · exact Or.inl h
  · obtain ⟨m, hm⟩ := Nat.even_or_odd' (p - e)
    rcases hm with hm | hm
    · exact Or.inr (Or.inl ⟨m, by omega⟩)
    · exact Or.inr (Or.inr ⟨m, by omega⟩)

theorem kCoef_pos' {N : ℕ} (hN : 2 ≤ N) (l m : ℕ) : 0 < kCoef N l m := kCoef_pos hN l m

/-- (L1) the guarded two-step ratio -/
theorem cK_L1 {N : ℕ} (hN : 2 ≤ N) (e p : ℕ) :
    (if 2 ≤ p then cK N e (p - 2) else 0) = cK N e p * ((p : ℝ) - e) * ((p : ℝ) + e - 2 + N) := by
  rcases cases_e e p with h | ⟨m, rfl⟩ | ⟨m, rfl⟩
  · rw [cK_of_lt h]
    split_ifs
    · rw [cK_of_lt (by omega)]; ring
    · ring
  · rcases m with _ | m
    · simp only [mul_zero, add_zero, sub_self, mul_zero, zero_mul]
      split_ifs with h2
      · apply cK_of_lt; omega
      · rfl
    · rw [if_pos (by omega), show e + 2 * (m + 1) - 2 = e + 2 * m by omega, cK_eq, cK_eq]
      have h1 := kCoef_succ_m hN e m
      have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
      rw [← h1]
      push_cast
      field_simp
      ring
  · rw [cK_odd, zero_mul, zero_mul]
    split_ifs with h2
    · rcases m with _ | m
      · apply cK_of_lt; omega
      · rw [show e + 2 * (m + 1) + 1 - 2 = e + 2 * m + 1 by omega, cK_odd]
    · rfl

/-- (L2) the guarded diagonal ratio -/
theorem cK_L2 {N : ℕ} (hN : 2 ≤ N) (e p : ℕ) :
    (if 1 ≤ e ∧ 1 ≤ p then cK N (e - 1) (p - 1) else 0)
      = (if 1 ≤ e then cK N e p * ((p : ℝ) + e - 2 + N) else 0) := by
  rcases e with _ | e
  · simp
  · simp only [show (1 : ℕ) ≤ e + 1 from by omega, true_and, if_true, Nat.add_sub_cancel]
    rcases cases_e (e + 1) p with h | ⟨m, rfl⟩ | ⟨m, rfl⟩
    · rw [cK_of_lt h]
      split_ifs
      · rw [cK_of_lt (by omega)]; ring
      · ring
    · rw [if_pos (by omega), show e + 1 + 2 * m - 1 = e + 2 * m by omega, cK_eq, cK_eq]
      have h1 := kCoef_succ_l hN e m
      have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
      rw [← h1]
      push_cast
      field_simp
      ring
    · rw [if_pos (by omega), show e + 1 + 2 * m + 1 - 1 = e + 2 * m + 1 by omega, cK_odd, cK_odd]; ring

/-- (L3) the guarded anti-diagonal ratio -/
theorem cK_L3 {N : ℕ} (hN : 2 ≤ N) (e p : ℕ) :
    (if 1 ≤ p then cK N (e + 1) (p - 1) else 0) = cK N e p * ((p : ℝ) - e) := by
  rcases cases_e e p with h | ⟨m, rfl⟩ | ⟨m, rfl⟩
  · rw [cK_of_lt h]
    split_ifs
    · rw [cK_of_lt (by omega)]; ring
    · ring
  · rcases m with _ | m
    · simp only [mul_zero, add_zero, sub_self, mul_zero]
      split_ifs with h2
      · apply cK_of_lt; omega
      · rfl
    · rw [if_pos (by omega), show e + 2 * (m + 1) - 1 = (e + 1) + 2 * m by omega, cK_eq, cK_eq]
      have h1 := kCoef_succ_m hN e m
      have h2 := kCoef_succ_l hN e m
      have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
      have hs : (0 : ℝ) < (e : ℝ) + m + (N : ℝ) / 2 := by positivity
      have hk := kCoef_pos hN e (m + 1)
      have hk2 := kCoef_pos hN (e + 1) m
      -- both sides equal kCoef N e m / ((e + m + N/2) 2^(e+2m+1))
      have e1 : kCoef N (e + 1) m = kCoef N e m / ((e : ℝ) + m + (N : ℝ) / 2) := by
        rw [← h2]; field_simp
      have e2 : kCoef N e (m + 1) = kCoef N e m / (((m : ℝ) + 1) * ((e : ℝ) + m + (N : ℝ) / 2)) := by
        rw [← h1]; field_simp
      rw [e1, e2]
      push_cast
      field_simp
      ring
  · rw [cK_odd, if_pos (by omega)]
    rcases m with _ | m
    · rw [cK_of_lt (by omega)]; ring
    · rw [show e + 2 * (m + 1) + 1 - 1 = (e + 1) + 2 * m + 1 by omega, cK_odd]; ring

/-! ### The dimensions d_ℓ -/

theorem dConc_zero (N : ℕ) : dConc N 0 = 1 := by
  simp [dConc]

/-- with N = M + 2 and b_a = C(a + M, a): d_{a+1} = b_{a+1} + b_a -/
theorem dConc_succ (M a : ℕ) :
    dConc (M + 2) (a + 1) = (Nat.choose (a + 1 + M) (a + 1) : ℝ) + (Nat.choose (a + M) a : ℝ) := by
  unfold dConc
  rw [show a + 1 + (M + 2) - 1 = (a + 1 + M) + 1 by omega]
  rw [Nat.choose_succ_succ' (a + 1 + M) a]
  rcases a with _ | a
  · simp only [zero_add, Nat.choose_zero_right, Nat.choose_one_right, show ¬ (2 ≤ 0 + 1) from by omega, if_false]
    push_cast
    ring
  · rw [if_pos (by omega), show a + 1 + 1 + (M + 2) - 3 = a + M + 1 by omega, show a + 1 + 1 - 2 = a by omega,
      show a + 1 + 1 + M = (a + M + 1) + 1 by omega, show a + 1 + M = a + M + 1 by omega,
      Nat.choose_succ_succ' (a + M + 1) a]
    push_cast
    ring

theorem choose_rel (M a : ℕ) :
    ((a : ℝ) + 1) * (Nat.choose (a + 1 + M) (a + 1) : ℝ) = ((a : ℝ) + 1 + M) * (Nat.choose (a + M) a : ℝ) := by
  have h := Nat.add_one_mul_choose_eq (a + M) a
  rw [show a + M + 1 = a + 1 + M by omega] at h
  have h' : (((a + 1 + M) * Nat.choose (a + M) a : ℕ) : ℝ) = ((Nat.choose (a + 1 + M) (a + 1) * (a + 1) : ℕ) : ℝ) := by
    rw [h]
  push_cast at h'
  linarith

/-- (R1) (2a + N)(a + N - 2) d_a = (a + 1)(2a + N - 2) d_{a+1} -/
theorem dConc_R1 {N : ℕ} (hN : 2 ≤ N) (a : ℕ) :
    (2 * (a : ℝ) + N) * ((a : ℝ) + N - 2) * dConc N a = ((a : ℝ) + 1) * (2 * (a : ℝ) + N - 2) * dConc N (a + 1) := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  rcases a with _ | a
  · rw [dConc_zero, dConc_succ]
    simp only [zero_add, Nat.choose_one_right, Nat.choose_zero_right]
    push_cast
    ring
  · rw [dConc_succ, dConc_succ]
    have h1 := choose_rel M a
    have h2 := choose_rel M (a + 1)
    push_cast at h1 h2 ⊢
    linear_combination (-(2 * (a : ℝ) + M + 4)) * h1 + (-(2 * (a : ℝ) + M + 2)) * h2

theorem dConc_one {N : ℕ} (hN : 2 ≤ N) : dConc N 1 = N := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  have h := dConc_succ M 0
  simp only [zero_add, Nat.choose_one_right, Nat.choose_zero_right] at h
  rw [h]
  push_cast
  ring

/-! ### The zonal polynomials and their three-term recurrence -/

/-- Π_e(t) = d_e C̃_e(t) -/
def zon (N e : ℕ) (t : ℝ) : ℝ := dConc N e * CConc N e t

/-- α_e = (e + 1) / (2e + N) -/
def alphaK (N e : ℕ) : ℝ := ((e : ℝ) + 1) / (2 * (e : ℝ) + N)

/-- β_0 = 0, β_1 = 1, β_{e+2} = (e + N - 1) / (2e + N) -/
def betaK (N : ℕ) : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | e + 2 => ((e : ℝ) + N - 1) / (2 * (e : ℝ) + N)

theorem zon_zero (N : ℕ) (t : ℝ) : zon N 0 t = 1 := by
  simp [zon, dConc_zero, CConc]

theorem zon_one {N : ℕ} (hN : 2 ≤ N) (t : ℝ) : zon N 1 t = N * t := by
  have h1 : CConc N 1 t = t := rfl
  rw [zon, dConc_one hN, h1]

theorem dConc_two {N : ℕ} (hN : 2 ≤ N) : dConc N 2 = ((N : ℝ) + 2) * ((N : ℝ) - 1) / 2 := by
  have hR := dConc_R1 hN 1
  rw [dConc_one hN] at hR
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  rw [eq_div_iff (by norm_num)]
  push_cast at hR
  have hNpos : (0 : ℝ) < N := by linarith
  have h2 : (2 : ℝ) * N * dConc N 2 = ((N : ℝ) + 2) * ((N : ℝ) - 1) * N := by linarith
  have h3 : (N : ℝ) * (dConc N 2 * 2 - ((N : ℝ) + 2) * ((N : ℝ) - 1)) = 0 := by linarith
  rcases mul_eq_zero.mp h3 with h | h
  · linarith
  · linarith

theorem zon_two {N : ℕ} (hN : 2 ≤ N) (t : ℝ) :
    zon N 2 t = ((N : ℝ) + 2) / 2 * ((N : ℝ) * t ^ 2 - 1) := by
  have hC2 : CConc N 2 t = ((2 * (((0 : ℕ) : ℝ) + 1) + ((N : ℝ) - 2)) * t * CConc N 1 t - (((0 : ℕ) : ℝ) + 1) * CConc N 0 t) /
      ((((0 : ℕ) : ℝ) + 1) + ((N : ℝ) - 2)) := rfl
  have h1 : CConc N 1 t = t := rfl
  have h0 : CConc N 0 t = 1 := rfl
  rw [zon, dConc_two hN, hC2, h1, h0]
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  push_cast
  rw [show (M : ℝ) + 2 - 2 = M by ring, show (M : ℝ) + 2 - 1 = M + 1 by ring]
  field_simp
  ring

/-- the step of the recurrence for e = n + 2, in clean real variables -/
theorem zon_rec_aux (x M t D1 D2 D3 C1 C2 : ℝ) (hx : 0 ≤ x) (hM : 0 ≤ M)
    (hR2 : (2 * (x + 2) + (M + 2)) * (x + 2 + M) * D2 = (x + 3) * (2 * (x + 2) + M) * D3)
    (hR1 : (2 * (x + 1) + (M + 2)) * (x + 1 + M) * D1 = (x + 2) * (2 * (x + 1) + M) * D2) :
    t * (D2 * C2) = (x + 3) / (2 * (x + 2) + (M + 2)) * (D3 * (((2 * (x + 2) + M) * t * C2 - (x + 2) * C1) / (x + 2 + M)))
      + (x + M + 1) / (2 * x + (M + 2)) * (D1 * C1) := by
  have e3 : D3 = (2 * (x + 2) + (M + 2)) * (x + 2 + M) * D2 / ((x + 3) * (2 * (x + 2) + M)) := by
    rw [eq_div_iff (by positivity)]; linarith
  have e1 : D1 = (x + 2) * (2 * (x + 1) + M) * D2 / ((2 * (x + 1) + (M + 2)) * (x + 1 + M)) := by
    rw [eq_div_iff (by positivity)]; linarith
  rw [e3, e1]
  field_simp
  ring

/-- the three-term recurrence t Π_e = α_e Π_{e+1} + β_e Π_{e-1} -/
theorem zon_rec {N : ℕ} (hN : 2 ≤ N) (e : ℕ) (t : ℝ) :
    t * zon N e t = alphaK N e * zon N (e + 1) t + betaK N e * zon N (e - 1) t := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hN0 : (N : ℝ) ≠ 0 := by positivity
  rcases e with _ | _ | n
  · have hb : betaK N 0 = 0 := rfl
    rw [zon_zero, zon_one hN, hb, alphaK]
    push_cast
    field_simp
    ring
  · have hb : betaK N 1 = 1 := rfl
    rw [zon_one hN, show 0 + 1 + 1 = 2 from rfl, zon_two hN, hb, show 0 + 1 - 1 = 0 from rfl, zon_zero, alphaK]
    push_cast
    field_simp
    ring
  · have hR2 := dConc_R1 hN (n + 1 + 1)
    have hR1 := dConc_R1 hN (n + 1)
    have hb : betaK N (n + 1 + 1) = ((n : ℝ) + N - 1) / (2 * (n : ℝ) + N) := rfl
    have hC : CConc N (n + 1 + 1 + 1) t = ((2 * (((n + 1 : ℕ) : ℝ) + 1) + ((N : ℝ) - 2)) * t * CConc N (n + 1 + 1) t -
        (((n + 1 : ℕ) : ℝ) + 1) * CConc N (n + 1) t) / ((((n + 1 : ℕ) : ℝ) + 1) + ((N : ℝ) - 2)) := rfl
    simp only [zon, alphaK]
    rw [show n + 1 + 1 - 1 = n + 1 from rfl, hb, hC]
    obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
    push_cast at hR2 hR1 ⊢
    have A := zon_rec_aux (n : ℝ) (M : ℝ) t (dConc (M + 2) (n + 1)) (dConc (M + 2) (n + 1 + 1))
      (dConc (M + 2) (n + 1 + 1 + 1)) (CConc (M + 2) (n + 1) t) (CConc (M + 2) (n + 1 + 1) t)
      (Nat.cast_nonneg n) (Nat.cast_nonneg M) (by linear_combination hR2) (by linear_combination hR1)
    linear_combination A

end G2Kernel
