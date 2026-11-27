/-
G2S1.Coord (stage S1, algebra): the zonal polynomials as polynomials, the coordinate functionals
coord_e(f) = Σ_p f_p p! c'(e, p), coord_e(Π_a) = δ_{ea}, and the algebraic form of the projection identity:
Σ_{p,q} (Π_a)_p (Π_b)_q p! q! R(p, q) = δ_{ab} Π_a(t).
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1, display (2).
-/
import G2S1.Jac

noncomputable section
open Real Finset Polynomial

namespace G2Kernel

/-! ### The polynomials -/

/-- C̃_n as a polynomial (the recurrence of `CConc`) -/
def cPoly (N : ℕ) : ℕ → Polynomial ℝ
  | 0 => 1
  | 1 => X
  | n + 2 => C (1 / (((n : ℝ) + 1) + ((N : ℝ) - 2))) *
      (C (2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * X * cPoly N (n + 1) - C ((n : ℝ) + 1) * cPoly N n)

theorem eval_cPoly (N : ℕ) : ∀ n : ℕ, ∀ t : ℝ, (cPoly N n).eval t = CConc N n t
  | 0, t => by simp [cPoly, CConc]
  | 1, t => by simp [cPoly, CConc]
  | n + 2, t => by
    have h1 := eval_cPoly N (n + 1) t
    have h0 := eval_cPoly N n t
    simp only [cPoly, eval_mul, eval_C, eval_sub, eval_X, h1, h0]
    show _ = ((2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * t * CConc N (n + 1) t - ((n : ℝ) + 1) * CConc N n t) /
      (((n : ℝ) + 1) + ((N : ℝ) - 2))
    ring

theorem natDegree_cPoly_le (N : ℕ) : ∀ n : ℕ, (cPoly N n).natDegree ≤ n
  | 0 => by simp [cPoly]
  | 1 => by simp only [cPoly]; exact natDegree_X_le
  | n + 2 => by
    have h1 := natDegree_cPoly_le N (n + 1)
    have h0 := natDegree_cPoly_le N n
    simp only [cPoly]
    refine (natDegree_C_mul_le _ _).trans ?_
    refine (natDegree_sub_le _ _).trans (max_le ?_ ?_)
    · refine (natDegree_mul_le).trans ?_
      have hx : (C (2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * X : Polynomial ℝ).natDegree ≤ 1 :=
        (natDegree_C_mul_le _ _).trans natDegree_X_le
      omega
    · exact (natDegree_C_mul_le _ _).trans (by omega)

/-- Π_e as a polynomial -/
def zonPoly (N e : ℕ) : Polynomial ℝ := C (dConc N e) * cPoly N e

theorem eval_zonPoly (N e : ℕ) (t : ℝ) : (zonPoly N e).eval t = zon N e t := by
  simp [zonPoly, zon, eval_cPoly]

theorem natDegree_zonPoly_le (N e : ℕ) : (zonPoly N e).natDegree ≤ e :=
  (natDegree_C_mul_le _ _).trans (natDegree_cPoly_le N e)

theorem alphaK_pos {N : ℕ} (hN : 2 ≤ N) (e : ℕ) : 0 < alphaK N e := by
  unfold alphaK; positivity

/-- the recurrence solved for Π_{a+1} -/
theorem zonPoly_succ {N : ℕ} (hN : 2 ≤ N) (a : ℕ) :
    zonPoly N (a + 1) = C (1 / alphaK N a) * (X * zonPoly N a - C (betaK N a) * zonPoly N (a - 1)) := by
  apply Polynomial.funext
  intro t
  simp only [eval_mul, eval_C, eval_sub, eval_X, eval_zonPoly]
  have h := zon_rec hN a t
  have ha := (alphaK_pos hN a).ne'
  rw [h]
  field_simp
  ring

/-! ### The coordinate functionals -/

/-- coord_e(f) = Σ_p f_p p! c'(e, p) -/
def coord (N e : ℕ) (f : Polynomial ℝ) : ℝ :=
  ∑ p ∈ range (f.natDegree + 1), f.coeff p * (p.factorial : ℝ) * cK N e p

theorem coord_eq_range (N e : ℕ) (f : Polynomial ℝ) (M : ℕ) (hM : f.natDegree < M) :
    coord N e f = ∑ p ∈ range M, f.coeff p * (p.factorial : ℝ) * cK N e p := by
  unfold coord
  apply sum_subset (range_subset_range.mpr (by omega))
  intro p _ hp
  simp only [mem_range, not_lt] at hp
  rw [coeff_eq_zero_of_natDegree_lt (by omega)]
  ring

theorem coord_add (N e : ℕ) (f g : Polynomial ℝ) : coord N e (f + g) = coord N e f + coord N e g := by
  set M := f.natDegree + g.natDegree + 1
  have hfg : (f + g).natDegree < M := lt_of_le_of_lt (natDegree_add_le _ _) (by omega)
  rw [coord_eq_range N e _ M hfg, coord_eq_range N e f M (by omega), coord_eq_range N e g M (by omega),
    ← sum_add_distrib]
  refine sum_congr rfl (fun p _ => ?_)
  rw [coeff_add]; ring

theorem coord_C_mul (N e : ℕ) (c : ℝ) (f : Polynomial ℝ) : coord N e (C c * f) = c * coord N e f := by
  set M := f.natDegree + 1
  have h : (C c * f).natDegree < M := lt_of_le_of_lt (natDegree_C_mul_le _ _) (by omega)
  rw [coord_eq_range N e _ M h, coord_eq_range N e f M (by omega), mul_sum]
  refine sum_congr rfl (fun p _ => ?_)
  rw [coeff_C_mul]; ring

theorem coord_sub (N e : ℕ) (f g : Polynomial ℝ) : coord N e (f - g) = coord N e f - coord N e g := by
  have h : f - g = f + C (-1) * g := by rw [C_neg, C_1]; ring
  rw [h, coord_add, coord_C_mul]; ring

theorem jac_sum (N : ℕ) {ι : Type*} (s : Finset ι) (g : ι → ℕ → ℝ) (e : ℕ) :
    jac N (fun e => ∑ i ∈ s, g i e) e = ∑ i ∈ s, jac N (g i) e := by
  unfold jac
  split_ifs
  · simp only [zero_add, mul_sum]
  · simp only [mul_sum, ← sum_add_distrib]

theorem coord_X_mul {N : ℕ} (hN : 2 ≤ N) (e : ℕ) (f : Polynomial ℝ) :
    coord N e (X * f) = jac N (fun e => coord N e f) e := by
  set D := f.natDegree
  have hX : (X * f).natDegree < D + 2 :=
    lt_of_le_of_lt natDegree_mul_le (by have := (natDegree_X_le : (X : Polynomial ℝ).natDegree ≤ 1); omega)
  rw [coord_eq_range N e _ (D + 2) hX, show D + 2 = (D + 1) + 1 from rfl, sum_range_succ']
  simp only [coeff_X_mul, coeff_X_mul_zero, zero_mul, add_zero]
  have hc : (fun e => coord N e f) = fun e => ∑ p ∈ range (D + 1), f.coeff p * (p.factorial : ℝ) * cK N e p := by
    funext e'; exact coord_eq_range N e' f (D + 1) (by omega)
  rw [hc, jac_sum]
  refine sum_congr rfl (fun p _ => ?_)
  have hj : jac N (fun e => f.coeff p * (p.factorial : ℝ) * cK N e p) e
      = f.coeff p * (p.factorial : ℝ) * jac N (fun e => cK N e p) e := by
    unfold jac; split_ifs <;> ring
  rw [hj, Pn_term hN p e, Nat.factorial_succ]
  push_cast
  ring

/-- coord_e(Π_a) = δ_{ea} -/
theorem coord_zonPoly {N : ℕ} (hN : 2 ≤ N) : ∀ a e : ℕ, coord N e (zonPoly N a) = if e = a then 1 else 0 := by
  have key : ∀ a, (∀ e, coord N e (zonPoly N a) = if e = a then 1 else 0) ∧
      (∀ e, coord N e (zonPoly N (a + 1)) = if e = a + 1 then 1 else 0) := by
    intro a
    induction a with
    | zero =>
      have h0 : ∀ e, coord N e (zonPoly N 0) = if e = 0 then 1 else 0 := by
        intro e
        have hz : zonPoly N 0 = C 1 := by simp [zonPoly, cPoly, dConc_zero]
        rw [hz, coord_eq_range N e _ 1 (by simp)]
        simp only [range_one, sum_singleton, coeff_C_zero, Nat.factorial_zero, Nat.cast_one, mul_one, one_mul]
        rcases e with _ | e
        · simp [cK_zero_zero hN]
        · simp [cK_of_lt (show 0 < e + 1 by omega)]
      refine ⟨h0, fun e => ?_⟩
      rw [zonPoly_succ hN 0, coord_C_mul, coord_sub, coord_C_mul, coord_X_mul hN]
      have hb : betaK N 0 = 0 := rfl
      rw [hb, zero_mul, sub_zero]
      unfold jac
      simp only [h0]
      have ha := (alphaK_pos hN 0).ne'
      rcases e with _ | _ | e
      · simp
      · simp; field_simp
      · simp
    | succ a ih =>
      refine ⟨ih.2, fun e => ?_⟩
      rw [zonPoly_succ hN (a + 1), coord_C_mul, coord_sub, coord_C_mul, coord_X_mul hN]
      simp only [Nat.add_sub_cancel]
      unfold jac
      simp only [ih.1, ih.2]
      have ha := (alphaK_pos hN (a + 1)).ne'
      rcases e with _ | e
      · rcases a with _ | a
        · simp
        · simp
      · simp only [Nat.add_one_ne_zero, if_false, Nat.add_sub_cancel, Nat.add_right_cancel_iff]
        by_cases h1 : e = a + 1
        · subst h1
          simp [show ¬ (a + 1 + 1 = a) from by omega]
          field_simp
        · by_cases h2 : e + 1 + 1 = a + 1
          · have h3 : e + 1 = a := by omega
            subst h3
            simp [show ¬ (e = e + 1 + 1) from by omega]
          · have h4 : e + 1 ≠ a := fun h => h2 (by omega)
            have h5 : e + 1 ≠ a + 1 + 1 := fun h => h1 (by omega)
            simp [h1, h2, h4, h5]
  intro a e
  exact (key a).1 e

/-- the algebraic projection identity: Σ_{p,q} (Π_a)_p (Π_b)_q p! q! R(p,q) = δ_{ab} Π_a(t) -/
theorem proj_alg {N : ℕ} (hN : 2 ≤ N) (t : ℝ) (a b : ℕ) :
    ∑ p ∈ range (a + 1), ∑ q ∈ range (b + 1), (zonPoly N a).coeff p * (zonPoly N b).coeff q *
      ((p.factorial : ℝ) * (q.factorial : ℝ) * Rz N t p q) = if a = b then zon N a t else 0 := by
  have hR : ∀ p ∈ range (a + 1), ∀ q, Rz N t p q = ∑ e ∈ range (a + 1), cK N e p * cK N e q * zon N e t := by
    intro p hp q
    simp only [mem_range] at hp
    exact Rz_eq_range N t p q (a + 1) (by omega)
  have step : ∑ p ∈ range (a + 1), ∑ q ∈ range (b + 1), (zonPoly N a).coeff p * (zonPoly N b).coeff q *
      ((p.factorial : ℝ) * (q.factorial : ℝ) * Rz N t p q)
      = ∑ e ∈ range (a + 1), coord N e (zonPoly N a) * coord N e (zonPoly N b) * zon N e t := by
    calc ∑ p ∈ range (a + 1), ∑ q ∈ range (b + 1), (zonPoly N a).coeff p * (zonPoly N b).coeff q *
          ((p.factorial : ℝ) * (q.factorial : ℝ) * Rz N t p q)
        = ∑ p ∈ range (a + 1), ∑ q ∈ range (b + 1), ∑ e ∈ range (a + 1),
            ((zonPoly N a).coeff p * (p.factorial : ℝ) * cK N e p) *
              ((zonPoly N b).coeff q * (q.factorial : ℝ) * cK N e q) * zon N e t := by
          refine sum_congr rfl (fun p hp => sum_congr rfl (fun q _ => ?_))
          rw [hR p hp q, mul_sum, mul_sum]
          refine sum_congr rfl (fun e _ => by ring)
      _ = ∑ p ∈ range (a + 1), ∑ e ∈ range (a + 1), ∑ q ∈ range (b + 1),
            ((zonPoly N a).coeff p * (p.factorial : ℝ) * cK N e p) *
              ((zonPoly N b).coeff q * (q.factorial : ℝ) * cK N e q) * zon N e t :=
          sum_congr rfl (fun p _ => sum_comm)
      _ = ∑ e ∈ range (a + 1), ∑ p ∈ range (a + 1), ∑ q ∈ range (b + 1),
            ((zonPoly N a).coeff p * (p.factorial : ℝ) * cK N e p) *
              ((zonPoly N b).coeff q * (q.factorial : ℝ) * cK N e q) * zon N e t := sum_comm
      _ = _ := by
          refine sum_congr rfl (fun e _ => ?_)
          rw [coord_eq_range N e (zonPoly N a) (a + 1) (by have := natDegree_zonPoly_le N a; omega),
            coord_eq_range N e (zonPoly N b) (b + 1) (by have := natDegree_zonPoly_le N b; omega),
            sum_mul_sum, sum_mul]
          refine sum_congr rfl (fun p _ => ?_)
          rw [sum_mul]
  rw [step]
  simp only [coord_zonPoly hN]
  by_cases hab : a = b
  · subst hab
    simp [sum_ite_eq']
  · rw [if_neg hab]
    apply sum_eq_zero
    intro e _
    by_cases h1 : e = a
    · subst h1; simp [hab]
    · simp [h1]

end G2Kernel
