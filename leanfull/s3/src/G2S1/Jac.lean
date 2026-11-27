/-
G2S1.Jac (stage S1, algebra): the Jacobi operator of the zonal polynomials, (P_n), and the recurrence [*] for
R(p, q) = Σ_e c'(e,p) c'(e,q) Π_e(t), the zonal expansion of the two-point moments of ω.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1.
- `jacobi_sum`: t Σ_{e<M} v_e Π_e(t) = Σ_{e<M+1} (J v)_e Π_e(t) for v supported below M.
- `pow_eq_sum_zon` (P_n): t^n = n! Σ_{e ≤ n} c'(e, n) Π_e(t).
- `star_Rz`: (p+q)(p+q-2+N) R(p,q) = [p≥2] R(p-2,q) + [q≥2] R(p,q-2) + [p,q≥1] 2t R(p-1,q-1); `star_unique`.
-/
import G2S1.Alg

noncomputable section
open Real Finset

namespace G2Kernel

/-- the Jacobi operator on coefficient vectors: (J v)_e = [e ≥ 1] α_{e-1} v_{e-1} + β_{e+1} v_{e+1} -/
def jac (N : ℕ) (v : ℕ → ℝ) (e : ℕ) : ℝ :=
  (if e = 0 then 0 else alphaK N (e - 1) * v (e - 1)) + betaK N (e + 1) * v (e + 1)

theorem jacobi_sum {N : ℕ} (hN : 2 ≤ N) (v : ℕ → ℝ) (M : ℕ) (hv : ∀ e, M ≤ e → v e = 0) (t : ℝ) :
    t * ∑ e ∈ range M, v e * zon N e t = ∑ e ∈ range (M + 1), jac N v e * zon N e t := by
  have h1 : t * ∑ e ∈ range M, v e * zon N e t
      = ∑ e ∈ range M, v e * alphaK N e * zon N (e + 1) t + ∑ e ∈ range M, v e * betaK N e * zon N (e - 1) t := by
    rw [mul_sum, ← sum_add_distrib]
    refine sum_congr rfl (fun e _ => ?_)
    have := zon_rec hN e t
    calc t * (v e * zon N e t) = v e * (t * zon N e t) := by ring
      _ = _ := by rw [this]; ring
  rw [h1]
  simp only [jac, add_mul, sum_add_distrib]
  congr 1
  · rw [sum_range_succ']
    simp only [Nat.add_one_ne_zero, if_false, Nat.add_sub_cancel, if_true, zero_mul, add_zero]
    refine sum_congr rfl (fun e _ => by ring)
  · rcases M with _ | M
    · simp [hv 1 (by omega)]
    · rw [sum_range_succ' (fun e => v e * betaK N e * zon N (e - 1) t), sum_range_succ, sum_range_succ,
        hv (M + 1) le_rfl, hv (M + 1 + 1) (by omega)]
      have hb0 : betaK N 0 = 0 := rfl
      simp only [hb0, mul_zero, zero_mul, add_zero, Nat.add_sub_cancel]
      refine sum_congr rfl (fun e _ => by ring)

/-- the coefficient step of (P_n) -/
theorem Pn_term {N : ℕ} (hN : 2 ≤ N) (n e : ℕ) :
    jac N (fun e => cK N e n) e = ((n : ℝ) + 1) * cK N e (n + 1) := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have L3 := cK_L3 hN e (n + 1)
  simp only [show 1 ≤ n + 1 from by omega, if_true, Nat.add_sub_cancel] at L3
  unfold jac
  rcases e with _ | e
  · have hb : betaK N (0 + 1) = 1 := rfl
    simp only [if_true, hb, one_mul, zero_add]
    rw [L3]
    push_cast
    ring
  · have L2 := cK_L2 hN (e + 1) (n + 1)
    simp only [show 1 ≤ e + 1 from by omega, show 1 ≤ n + 1 from by omega, and_self, if_true,
      Nat.add_sub_cancel] at L2
    have hb : betaK N (e + 1 + 1) = ((e : ℝ) + N - 1) / (2 * (e : ℝ) + N) := rfl
    simp only [Nat.add_one_ne_zero, if_false, Nat.add_sub_cancel]
    rw [L2, L3, hb, alphaK]
    push_cast
    have h1 : (2 * (e : ℝ) + N) ≠ 0 := by positivity
    field_simp
    ring

/-- (P_n): t^n = n! Σ_{e ≤ n} c'(e, n) Π_e(t) -/
theorem pow_eq_sum_zon {N : ℕ} (hN : 2 ≤ N) (n : ℕ) (t : ℝ) :
    t ^ n = (n.factorial : ℝ) * ∑ e ∈ range (n + 1), cK N e n * zon N e t := by
  induction n with
  | zero => simp [cK_zero_zero hN, zon_zero]
  | succ n ih =>
    have hj := jacobi_sum hN (fun e => cK N e n) (n + 1) (fun e he => cK_of_lt (show n < e by omega)) t
    rw [pow_succ, ih, mul_assoc, mul_comm (∑ e ∈ range (n + 1), cK N e n * zon N e t) t, hj]
    simp only [Pn_term hN n]
    rw [Nat.factorial_succ, mul_sum, mul_sum]
    push_cast
    refine sum_congr rfl (fun e _ => by ring)

/-! ### The zonal expansion R(p, q) of the two-point moments and its recurrence -/

/-- R(p, q) = Σ_e c'(e,p) c'(e,q) Π_e(t) -/
def Rz (N : ℕ) (t : ℝ) (p q : ℕ) : ℝ := ∑ e ∈ range (p + 1), cK N e p * cK N e q * zon N e t

theorem Rz_eq_range (N : ℕ) (t : ℝ) (p q M : ℕ) (hM : p + 1 ≤ M) :
    Rz N t p q = ∑ e ∈ range M, cK N e p * cK N e q * zon N e t := by
  unfold Rz
  apply sum_subset (range_subset_range.mpr hM)
  intro e _ hne
  simp only [mem_range, not_lt] at hne
  rw [cK_of_lt (show p < e by omega)]
  ring

theorem Rz_zero_zero {N : ℕ} (hN : 2 ≤ N) (t : ℝ) : Rz N t 0 0 = 1 := by
  simp [Rz, cK_zero_zero hN, zon_zero]

/-- the right side of [*] -/
def starRHS (r : ℕ → ℕ → ℝ) (t : ℝ) (p q : ℕ) : ℝ :=
  (if 2 ≤ p then r (p - 2) q else 0) + (if 2 ≤ q then r p (q - 2) else 0) +
    (if 1 ≤ p ∧ 1 ≤ q then 2 * t * r (p - 1) (q - 1) else 0)

theorem ite_and_mul (A B : Prop) [Decidable A] [Decidable B] (x y : ℝ) :
    (if A ∧ B then x * y else 0) = (if A then x else 0) * (if B then y else 0) := by
  by_cases hA : A <;> by_cases hB : B <;> simp [hA, hB]

/-- the coefficient step of [*] -/
theorem star_term {N : ℕ} (hN : 2 ≤ N) (p q e : ℕ) :
    ((p : ℝ) + q) * ((p : ℝ) + q - 2 + N) * (cK N e p * cK N e q)
      = (if 2 ≤ p then cK N e (p - 2) else 0) * cK N e q + cK N e p * (if 2 ≤ q then cK N e (q - 2) else 0)
        + 2 * jac N (fun e => if 1 ≤ p ∧ 1 ≤ q then cK N e (p - 1) * cK N e (q - 1) else 0) e := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  rw [cK_L1 hN e p, cK_L1 hN e q]
  unfold jac
  rcases e with _ | e
  · have hb : betaK N (0 + 1) = 1 := rfl
    simp only [if_true, hb, one_mul, zero_add]
    rw [ite_and_mul, cK_L3 hN 0 p, cK_L3 hN 0 q]
    push_cast
    ring
  · have hb : betaK N (e + 1 + 1) = ((e : ℝ) + N - 1) / (2 * (e : ℝ) + N) := rfl
    simp only [Nat.add_one_ne_zero, if_false, Nat.add_sub_cancel]
    have L2p := cK_L2 hN (e + 1) p
    have L2q := cK_L2 hN (e + 1) q
    simp only [show 1 ≤ e + 1 from by omega, true_and, if_true, Nat.add_sub_cancel] at L2p L2q
    rw [ite_and_mul, ite_and_mul, L2p, L2q, cK_L3 hN (e + 1) p, cK_L3 hN (e + 1) q, hb, alphaK]
    push_cast
    have h1 : (2 * (e : ℝ) + N) ≠ 0 := by positivity
    field_simp
    ring

theorem star_Rz {N : ℕ} (hN : 2 ≤ N) (t : ℝ) (p q : ℕ) :
    ((p : ℝ) + q) * ((p : ℝ) + q - 2 + N) * Rz N t p q = starRHS (Rz N t) t p q := by
  have e0 : Rz N t p q = ∑ e ∈ range (p + q + 3), cK N e p * cK N e q * zon N e t :=
    Rz_eq_range N t p q _ (by omega)
  have e1 : (if 2 ≤ p then Rz N t (p - 2) q else 0)
      = ∑ e ∈ range (p + q + 3), (if 2 ≤ p then cK N e (p - 2) else 0) * cK N e q * zon N e t := by
    split_ifs with h
    · exact Rz_eq_range N t (p - 2) q _ (by omega)
    · simp
  have e2 : (if 2 ≤ q then Rz N t p (q - 2) else 0)
      = ∑ e ∈ range (p + q + 3), cK N e p * (if 2 ≤ q then cK N e (q - 2) else 0) * zon N e t := by
    split_ifs with h
    · exact Rz_eq_range N t p (q - 2) _ (by omega)
    · simp
  set w : ℕ → ℝ := fun e => if 1 ≤ p ∧ 1 ≤ q then cK N e (p - 1) * cK N e (q - 1) else 0 with hw
  have hwv : ∀ e, p + q + 2 ≤ e → w e = 0 := by
    intro e he
    simp only [hw]
    split_ifs
    · rw [cK_of_lt (show p - 1 < e by omega)]; ring
    · rfl
  have e3 : (if 1 ≤ p ∧ 1 ≤ q then 2 * t * Rz N t (p - 1) (q - 1) else 0)
      = ∑ e ∈ range (p + q + 2 + 1), 2 * jac N w e * zon N e t := by
    have hj := jacobi_sum hN w (p + q + 2) hwv t
    have hR : (if 1 ≤ p ∧ 1 ≤ q then 2 * t * Rz N t (p - 1) (q - 1) else 0)
        = 2 * (t * ∑ e ∈ range (p + q + 2), w e * zon N e t) := by
      split_ifs with h
      · rw [Rz_eq_range N t (p - 1) (q - 1) (p + q + 2) (by omega)]
        simp only [hw, if_pos h]
        ring
      · simp only [hw, if_neg h, zero_mul, sum_const_zero, mul_zero]
    rw [hR, hj, mul_sum]
    refine sum_congr rfl (fun e _ => by ring)
  unfold starRHS
  rw [e0, e1, e2, e3, mul_sum, ← sum_add_distrib, ← sum_add_distrib]
  refine sum_congr rfl (fun e _ => ?_)
  have := star_term hN p q e
  rw [← hw] at this
  linear_combination (zon N e t) * this

/-- two solutions of [*] with the same value at (0, 0) agree -/
theorem star_unique {N : ℕ} (hN : 2 ≤ N) (t : ℝ) (f g : ℕ → ℕ → ℝ)
    (hf : ∀ p q : ℕ, 1 ≤ p + q → ((p : ℝ) + q) * ((p : ℝ) + q - 2 + N) * f p q = starRHS f t p q)
    (hg : ∀ p q : ℕ, 1 ≤ p + q → ((p : ℝ) + q) * ((p : ℝ) + q - 2 + N) * g p q = starRHS g t p q)
    (h0 : f 0 0 = g 0 0) : ∀ p q, f p q = g p q := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  intro p q
  induction' hn : p + q using Nat.strong_induction_on with n ih generalizing p q
  rcases Nat.eq_zero_or_pos n with h | h
  · obtain ⟨rfl, rfl⟩ : p = 0 ∧ q = 0 := by omega
    exact h0
  · have hS : starRHS f t p q = starRHS g t p q := by
      unfold starRHS
      congr 1
      congr 1
      · split_ifs with h2
        · exact ih (p - 2 + q) (by omega) (p - 2) q rfl
        · rfl
      · split_ifs with h2
        · exact ih (p + (q - 2)) (by omega) p (q - 2) rfl
        · rfl
      · split_ifs with h2
        · rw [ih (p - 1 + (q - 1)) (by omega) (p - 1) (q - 1) rfl]
        · rfl
    have hc : ((p : ℝ) + q) * ((p : ℝ) + q - 2 + N) ≠ 0 := by
      have h1 : (1 : ℝ) ≤ (p : ℝ) + q := by exact_mod_cast (show 1 ≤ p + q by omega)
      apply mul_ne_zero <;> linarith
    have e1 := hf p q (by omega)
    have e2 := hg p q (by omega)
    rw [hS, ← e2] at e1
    exact mul_left_cancel₀ hc e1

end G2Kernel
