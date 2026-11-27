/-
G2S1.GenFun (stage S1, tie): for N ≥ 3 and λ = N/2 - 1 > 0, C(n+N-3, n) C̃_n(t) are the coefficients of
(1 - 2tr + r^2)^{-λ}, the classical definition of the Gegenbauer polynomials C^λ_n (with C^λ_n(1) = C(n+N-3, n)), so
C̃_n = C^λ_n / C^λ_n(1) as the paper states.
Proof: g_n = C(n+N-3, n) C̃_n satisfies the Gegenbauer recurrence; G(r) = Σ g_n r^n solves (1-2tr+r^2) G' = 2λ(t-r) G on
(-1, 1); so G (1-2tr+r^2)^λ has derivative 0 and equals its value 1 at r = 0.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1.
-/
import G2S1.Tie

noncomputable section
open Real Finset Filter Topology

namespace G2Kernel

/-- g_n(t) = C(n + N - 3, n) C̃_n(t) -/
def gegC (N n : ℕ) (t : ℝ) : ℝ := (Nat.choose (n + N - 3) n : ℝ) * CConc N n t

theorem gegC_zero (N : ℕ) (t : ℝ) : gegC N 0 t = 1 := by
  simp [gegC, CConc]

theorem gegC_one {N : ℕ} (hN : 3 ≤ N) (t : ℝ) : gegC N 1 t = ((N : ℝ) - 2) * t := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 3 := ⟨N - 3, by omega⟩
  unfold gegC
  rw [show 1 + (M + 3) - 3 = 1 + M by omega, show (1 + M).choose 1 = 1 + M from Nat.choose_one_right _]
  have : CConc (M + 3) 1 t = t := rfl
  rw [this]
  push_cast
  ring

/-- the Gegenbauer recurrence (n+2) g_{n+2} = (2n+N) t g_{n+1} - (n+N-2) g_n -/
theorem gegC_rec {N : ℕ} (hN : 3 ≤ N) (n : ℕ) (t : ℝ) :
    ((n : ℝ) + 2) * gegC N (n + 1 + 1) t
      = (2 * (n : ℝ) + N) * t * gegC N (n + 1) t - ((n : ℝ) + N - 2) * gegC N n t := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 3 := ⟨N - 3, by omega⟩
  unfold gegC
  rw [show n + 1 + 1 + (M + 3) - 3 = n + 1 + 1 + M by omega, show n + 1 + (M + 3) - 3 = n + 1 + M by omega,
    show n + (M + 3) - 3 = n + M by omega]
  have h1 := choose_rel M (n + 1)
  have h0 := choose_rel M n
  have hC : ((n : ℝ) + M + 2) * CConc (M + 3) (n + 1 + 1) t
      = (2 * (n : ℝ) + M + 3) * t * CConc (M + 3) (n + 1) t - ((n : ℝ) + 1) * CConc (M + 3) n t := by
    rw [CConc]
    have hd : ((n : ℝ) + 1) + (((M + 3 : ℕ) : ℝ) - 2) ≠ 0 := by
      have e1 : (0 : ℝ) ≤ n := Nat.cast_nonneg n
      have e2 : (0 : ℝ) ≤ M := Nat.cast_nonneg M
      apply ne_of_gt
      push_cast
      linarith
    push_cast at hd ⊢
    field_simp
    ring
  push_cast at h1 h0 ⊢
  linear_combination (CConc (M + 3) (n + 1 + 1) t) * h1 + ((Nat.choose (n + 1 + M) (n + 1) : ℕ) : ℝ) * hC
    - (CConc (M + 3) n t) * h0

theorem abs_gegC_le {N : ℕ} (hN : 3 ≤ N) (n : ℕ) {t : ℝ} (ht : t ∈ Set.Icc (-1 : ℝ) 1) :
    |gegC N n t| ≤ ((n : ℝ) + 1) ^ (N - 3) := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 3 := ⟨N - 3, by omega⟩
  unfold gegC
  rw [show n + (M + 3) - 3 = n + M by omega, show M + 3 - 3 = M by omega, abs_mul, Nat.abs_cast]
  have h1 := abs_CConc_le_one (show 2 ≤ M + 3 by omega) n ht
  have h2 : ((Nat.choose (n + M) n : ℕ) : ℝ) ≤ ((n : ℝ) + 1) ^ M := by
    rw [Nat.choose_symm_add]; exact choose_add_le_pow n M
  calc ((Nat.choose (n + M) n : ℕ) : ℝ) * |CConc (M + 3) n t| ≤ ((n : ℝ) + 1) ^ M * 1 :=
        mul_le_mul h2 h1 (abs_nonneg _) (by positivity)
    _ = ((n : ℝ) + 1) ^ M := mul_one _

theorem summable_poly_geom (k : ℕ) {ρ : ℝ} (h0 : 0 ≤ ρ) (h1 : ρ < 1) :
    Summable (fun n : ℕ => ((n : ℝ) + 1) ^ k * ρ ^ n) := by
  have hs := summable_pow_mul_geometric_of_norm_lt_one k (show ‖ρ‖ < 1 by rw [Real.norm_eq_abs, abs_of_nonneg h0]; exact h1)
  have hs1 := (summable_nat_add_iff 1).mpr hs
  have hρ : 0 < ρ ∨ ρ = 0 := lt_or_eq_of_le h0 |>.imp id Eq.symm
  rcases hρ with hρ | hρ
  · refine (hs1.div_const ρ).congr (fun n => ?_)
    push_cast
    rw [pow_succ]
    field_simp
  · subst hρ
    refine (summable_of_ne_finset_zero (s := {0}) (fun n hn => ?_))
    have : n ≠ 0 := by simpa using hn
    simp [zero_pow this]

theorem summable_gegC_term {N : ℕ} (hN : 3 ≤ N) {t : ℝ} (ht : t ∈ Set.Icc (-1 : ℝ) 1) {r : ℝ} (hr : |r| < 1) :
    Summable (fun n => gegC N n t * r ^ n) := by
  refine Summable.of_norm_bounded (summable_poly_geom (N - 3) (abs_nonneg r) hr) (fun n => ?_)
  rw [norm_mul, norm_pow, Real.norm_eq_abs, Real.norm_eq_abs]
  exact mul_le_mul (abs_gegC_le hN n ht) le_rfl (by positivity) (by positivity)

/-- the shift X_m ↦ X_{m-1} of a power series is multiplication by r -/
theorem hasSum_shift1 {X : ℕ → ℝ} {S r : ℝ} (h : HasSum (fun m => X m * r ^ m) S) :
    HasSum (fun m => (if m = 0 then 0 else X (m - 1)) * r ^ m) (r * S) := by
  rw [← hasSum_nat_add_iff' 1]
  simp only [Finset.range_one, Finset.sum_singleton, if_pos, zero_mul, sub_zero, Nat.add_one_ne_zero, if_false,
    Nat.add_sub_cancel]
  convert h.mul_left r using 1
  funext m
  ring

/-- the shift operator on coefficient sequences -/
def shc (X : ℕ → ℝ) (m : ℕ) : ℝ := if m = 0 then 0 else X (m - 1)

/-- G' as a power series: Σ (m+1) g_{m+1} r^m -/
theorem hasDerivAt_gegG {N : ℕ} (hN : 3 ≤ N) {t : ℝ} (ht : t ∈ Set.Icc (-1 : ℝ) 1) {r : ℝ} (hr : |r| < 1) :
    HasDerivAt (fun y => ∑' n, gegC N n t * y ^ n) (∑' m : ℕ, ((m : ℝ) + 1) * gegC N (m + 1) t * r ^ m) r := by
  set ρ := (|r| + 1) / 2 with hρdef
  have hρ1 : ρ < 1 := by rw [hρdef]; linarith
  have hrρ : |r| < ρ := by rw [hρdef]; linarith
  have hρ0 : 0 < ρ := by rw [hρdef]; positivity
  have hu : Summable (fun n : ℕ => ((n : ℝ) + 1) ^ (N - 2) * ρ ^ n / ρ) :=
    (summable_poly_geom (N - 2) hρ0.le hρ1).div_const ρ
  have hrI : r ∈ Set.Ioo (-ρ) ρ := ⟨by linarith [neg_abs_le r], by linarith [le_abs_self r]⟩
  have hd := hasDerivAt_tsum_of_isPreconnected (u := fun n : ℕ => ((n : ℝ) + 1) ^ (N - 2) * ρ ^ n / ρ)
    (g := fun n y => gegC N n t * y ^ n) (g' := fun n y => gegC N n t * ((n : ℝ) * y ^ (n - 1)))
    (t := Set.Ioo (-ρ) ρ) (y₀ := r) hu isOpen_Ioo isPreconnected_Ioo
    (fun n y _ => (hasDerivAt_pow n y).const_mul _)
    (fun n y hy => by
      have hy' : |y| ≤ ρ := abs_le.mpr ⟨hy.1.le, hy.2.le⟩
      rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_pow, Nat.abs_cast]
      have hg := abs_gegC_le hN n ht
      have hp : |y| ^ (n - 1) ≤ ρ ^ (n - 1) := pow_le_pow_left₀ (abs_nonneg y) hy' _
      have key : (n : ℝ) * ρ ^ (n - 1) * ρ ≤ ((n : ℝ) + 1) * ρ ^ n := by
        rcases n with _ | m
        · simp
        · rw [show m + 1 - 1 = m by omega, pow_succ]
          push_cast
          have : (0 : ℝ) ≤ ρ ^ m * ρ := by positivity
          nlinarith
      have e1 : ((n : ℝ) + 1) ^ (N - 2) = ((n : ℝ) + 1) ^ (N - 3) * ((n : ℝ) + 1) := by
        rw [show N - 2 = (N - 3) + 1 by omega, pow_succ]
      rw [e1, le_div_iff₀ hρ0]
      calc |gegC N n t| * ((n : ℝ) * |y| ^ (n - 1)) * ρ ≤ ((n : ℝ) + 1) ^ (N - 3) * ((n : ℝ) * ρ ^ (n - 1)) * ρ := by
            apply mul_le_mul_of_nonneg_right _ hρ0.le
            exact mul_le_mul hg (mul_le_mul_of_nonneg_left hp (Nat.cast_nonneg n)) (by positivity) (by positivity)
        _ = ((n : ℝ) + 1) ^ (N - 3) * ((n : ℝ) * ρ ^ (n - 1) * ρ) := by ring
        _ ≤ ((n : ℝ) + 1) ^ (N - 3) * (((n : ℝ) + 1) * ρ ^ n) := mul_le_mul_of_nonneg_left key (by positivity)
        _ = ((n : ℝ) + 1) ^ (N - 3) * ((n : ℝ) + 1) * ρ ^ n := by ring)
    hrI (summable_gegC_term hN ht hr) hrI
  -- reindex the derivative series
  have hs : Summable (fun n => gegC N n t * ((n : ℝ) * r ^ (n - 1))) := by
    refine Summable.of_norm_bounded hu (fun n => ?_)
    have hr' : r ∈ Set.Ioo (-ρ) ρ := hrI
    have hy' : |r| ≤ ρ := hrρ.le
    rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_pow, Nat.abs_cast]
    have hg := abs_gegC_le hN n ht
    have hp : |r| ^ (n - 1) ≤ ρ ^ (n - 1) := pow_le_pow_left₀ (abs_nonneg r) hy' _
    have key : (n : ℝ) * ρ ^ (n - 1) * ρ ≤ ((n : ℝ) + 1) * ρ ^ n := by
      rcases n with _ | m
      · simp
      · rw [show m + 1 - 1 = m by omega, pow_succ]
        push_cast
        have : (0 : ℝ) ≤ ρ ^ m * ρ := by positivity
        nlinarith
    have e1 : ((n : ℝ) + 1) ^ (N - 2) = ((n : ℝ) + 1) ^ (N - 3) * ((n : ℝ) + 1) := by
      rw [show N - 2 = (N - 3) + 1 by omega, pow_succ]
    rw [e1, le_div_iff₀ hρ0]
    calc |gegC N n t| * ((n : ℝ) * |r| ^ (n - 1)) * ρ ≤ ((n : ℝ) + 1) ^ (N - 3) * ((n : ℝ) * ρ ^ (n - 1)) * ρ := by
          apply mul_le_mul_of_nonneg_right _ hρ0.le
          exact mul_le_mul hg (mul_le_mul_of_nonneg_left hp (Nat.cast_nonneg n)) (by positivity) (by positivity)
      _ = ((n : ℝ) + 1) ^ (N - 3) * ((n : ℝ) * ρ ^ (n - 1) * ρ) := by ring
      _ ≤ ((n : ℝ) + 1) ^ (N - 3) * (((n : ℝ) + 1) * ρ ^ n) := mul_le_mul_of_nonneg_left key (by positivity)
      _ = ((n : ℝ) + 1) ^ (N - 3) * ((n : ℝ) + 1) * ρ ^ n := by ring
  have hre : ∑' n, gegC N n t * ((n : ℝ) * r ^ (n - 1)) = ∑' m : ℕ, ((m : ℝ) + 1) * gegC N (m + 1) t * r ^ m := by
    rw [hs.tsum_eq_zero_add]
    simp only [Nat.cast_zero, zero_mul, mul_zero, zero_add, Nat.add_sub_cancel]
    congr 1; funext m; push_cast; ring
  rw [← hre]
  exact hd

theorem summable_gegD {N : ℕ} (hN : 3 ≤ N) {t : ℝ} (ht : t ∈ Set.Icc (-1 : ℝ) 1) {r : ℝ} (hr : |r| < 1) :
    Summable (fun m : ℕ => ((m : ℝ) + 1) * gegC N (m + 1) t * r ^ m) := by
  refine Summable.of_norm_bounded ((summable_poly_geom (N - 2) (abs_nonneg r) hr).mul_left (2 ^ (N - 3)))
    (fun m => ?_)
  rw [norm_mul, norm_mul, norm_pow, Real.norm_eq_abs, Real.norm_eq_abs, Real.norm_eq_abs,
    abs_of_nonneg (by positivity : (0 : ℝ) ≤ (m : ℝ) + 1)]
  have hg := abs_gegC_le hN (m + 1) ht
  push_cast at hg
  have h2 : ((m : ℝ) + 1 + 1) ^ (N - 3) ≤ 2 ^ (N - 3) * ((m : ℝ) + 1) ^ (N - 3) := by
    rw [← mul_pow]
    exact pow_le_pow_left₀ (by positivity) (by linarith [(Nat.cast_nonneg m : (0 : ℝ) ≤ m)]) _
  have e1 : ((m : ℝ) + 1) ^ (N - 2) = ((m : ℝ) + 1) ^ (N - 3) * ((m : ℝ) + 1) := by
    rw [show N - 2 = (N - 3) + 1 by omega, pow_succ]
  rw [e1]
  have hr0 : 0 ≤ |r| ^ m := by positivity
  calc ((m : ℝ) + 1) * |gegC N (m + 1) t| * |r| ^ m ≤ ((m : ℝ) + 1) * (2 ^ (N - 3) * ((m : ℝ) + 1) ^ (N - 3)) * |r| ^ m := by
        apply mul_le_mul_of_nonneg_right _ hr0
        exact mul_le_mul_of_nonneg_left (hg.trans h2) (by positivity)
    _ = 2 ^ (N - 3) * (((m : ℝ) + 1) ^ (N - 3) * ((m : ℝ) + 1) * |r| ^ m) := by ring

/-- the coefficient identity behind the ODE -/
theorem gegE {N : ℕ} (hN : 3 ≤ N) (t : ℝ) (m : ℕ) :
    let D : ℕ → ℝ := fun m => ((m : ℝ) + 1) * gegC N (m + 1) t
    let a : ℕ → ℝ := fun n => gegC N n t
    D m - 2 * t * shc D m + shc (shc D) m - ((N : ℝ) - 2) * t * a m + ((N : ℝ) - 2) * shc a m = 0 := by
  intro D a
  rcases m with _ | _ | k
  · simp only [D, a, shc, if_true, gegC_one hN, gegC_zero]
    push_cast; ring
  · have hr := gegC_rec hN 0 t
    simp only [D, a, shc, Nat.one_ne_zero, if_false, Nat.sub_self, if_true, zero_add, gegC_zero] at hr ⊢
    push_cast at hr ⊢
    linear_combination hr
  · have hr := gegC_rec hN (k + 1) t
    simp only [D, a, shc, Nat.add_one_ne_zero, if_false, Nat.add_sub_cancel] at hr ⊢
    push_cast at hr ⊢
    linear_combination hr

/-- the ODE (1 - 2tr + r^2) G'(r) = (N - 2)(t - r) G(r) -/
theorem gegG_ode {N : ℕ} (hN : 3 ≤ N) {t : ℝ} (ht : t ∈ Set.Icc (-1 : ℝ) 1) {r : ℝ} (hr : |r| < 1) :
    (1 - 2 * t * r + r ^ 2) * (∑' m : ℕ, ((m : ℝ) + 1) * gegC N (m + 1) t * r ^ m)
      = ((N : ℝ) - 2) * (t - r) * ∑' n, gegC N n t * r ^ n := by
  set D : ℕ → ℝ := fun m => ((m : ℝ) + 1) * gegC N (m + 1) t with hD
  set a : ℕ → ℝ := fun n => gegC N n t with ha
  have h1 : HasSum (fun m => D m * r ^ m) (∑' m : ℕ, ((m : ℝ) + 1) * gegC N (m + 1) t * r ^ m) :=
    (summable_gegD hN ht hr).hasSum
  have h4 : HasSum (fun m => a m * r ^ m) (∑' n, gegC N n t * r ^ n) := (summable_gegC_term hN ht hr).hasSum
  have h2 := hasSum_shift1 h1
  have h3 := hasSum_shift1 h2
  have h5 := hasSum_shift1 h4
  have hcomb := (((h1.sub (h2.mul_left (2 * t))).add h3).sub (h4.mul_left (((N : ℝ) - 2) * t))).add
    (h5.mul_left ((N : ℝ) - 2))
  have hz : HasSum (fun _ : ℕ => (0 : ℝ))
      ((∑' m : ℕ, ((m : ℝ) + 1) * gegC N (m + 1) t * r ^ m) - 2 * t * (r * ∑' m : ℕ, ((m : ℝ) + 1) * gegC N (m + 1) t * r ^ m)
        + r * (r * ∑' m : ℕ, ((m : ℝ) + 1) * gegC N (m + 1) t * r ^ m)
        - ((N : ℝ) - 2) * t * (∑' n, gegC N n t * r ^ n) + ((N : ℝ) - 2) * (r * ∑' n, gegC N n t * r ^ n)) := by
    refine hcomb.congr_fun (fun m => ?_)
    have hE := gegE hN t m
    simp only at hE
    have hE' : (D m - 2 * t * shc D m + shc (shc D) m - ((N : ℝ) - 2) * t * a m + ((N : ℝ) - 2) * shc a m) * r ^ m = 0 := by
      rw [hD, ha]; rw [hE, zero_mul]
    simp only [shc] at hE' ⊢
    linear_combination -hE'
  have h0 := hz.unique hasSum_zero
  linear_combination h0

theorem gegG_zero (N : ℕ) (t : ℝ) : ∑' n, gegC N n t * (0 : ℝ) ^ n = 1 := by
  rw [tsum_eq_single 0 (fun n hn => by rw [zero_pow hn, mul_zero])]
  simp [gegC_zero]

/-- **the generating function**: for N ≥ 3, λ = N/2 - 1, Σ_n C(n+N-3, n) C̃_n(t) r^n = (1 - 2tr + r^2)^{-λ} -/
theorem gegenbauer_genFun (N : ℕ) (hN : 3 ≤ N) {t r : ℝ} (ht : t ∈ Set.Icc (-1 : ℝ) 1) (hr : |r| < 1) :
    HasSum (fun n => (Nat.choose (n + N - 3) n : ℝ) * CConc N n t * r ^ n)
      ((1 - 2 * t * r + r ^ 2) ^ (-((N : ℝ) / 2 - 1))) := by
  set lam : ℝ := (N : ℝ) / 2 - 1 with hlam
  have hq : ∀ y : ℝ, |y| < 1 → 0 < 1 - 2 * t * y + y ^ 2 := by
    intro y hy
    have h1 : t * y ≤ |y| := by
      calc t * y ≤ |t * y| := le_abs_self _
        _ = |t| * |y| := abs_mul _ _
        _ ≤ 1 * |y| := mul_le_mul_of_nonneg_right (abs_le.mpr ⟨ht.1, ht.2⟩) (abs_nonneg _)
        _ = |y| := one_mul _
    have h2 : 0 < (1 - |y|) ^ 2 := by
      have h3 : 0 < 1 - |y| := by linarith
      exact pow_pos h3 2
    have e : (1 - |y|) ^ 2 = 1 - 2 * |y| + y ^ 2 := by rw [sub_sq, sq_abs]; ring
    linarith
  set G : ℝ → ℝ := fun y => ∑' n, gegC N n t * y ^ n with hG
  set H : ℝ → ℝ := fun y => G y * (1 - 2 * t * y + y ^ 2) ^ lam with hH
  have hderiv : ∀ y ∈ Set.Ioo (-1 : ℝ) 1, HasDerivAt H 0 y := by
    intro y hy
    have hy' : |y| < 1 := abs_lt.mpr ⟨hy.1, hy.2⟩
    have hqy := hq y hy'
    have hGd := hasDerivAt_gegG hN ht hy'
    have hqd : HasDerivAt (fun y => 1 - 2 * t * y + y ^ 2) (-(2 * t) + 2 * y) y := by
      have h1 : HasDerivAt (fun y => 2 * t * y) (2 * t) y := by
        simpa using (hasDerivAt_id y).const_mul (2 * t)
      have h2 : HasDerivAt (fun y => y ^ 2) (2 * y) y := by
        simpa using hasDerivAt_pow 2 y
      exact (h1.const_sub 1).add h2
    have hpd := hqd.rpow_const (p := lam) (Or.inl hqy.ne')
    have hHd := hGd.mul hpd
    convert hHd using 1
    have hode := gegG_ode hN ht hy'
    have hl : (1 : ℝ) + (lam - 1) ≠ 0 := by
      rw [hlam]
      have : (3 : ℝ) ≤ N := by exact_mod_cast hN
      intro h
      linarith
    have hsplit : (1 - 2 * t * y + y ^ 2) ^ lam = (1 - 2 * t * y + y ^ 2) * (1 - 2 * t * y + y ^ 2) ^ (lam - 1) := by
      rw [← Real.rpow_one_add' hqy.le hl]
      congr 1
      ring
    rw [hsplit]
    have e : (∑' m : ℕ, ((m : ℝ) + 1) * gegC N (m + 1) t * y ^ m) * ((1 - 2 * t * y + y ^ 2) * (1 - 2 * t * y + y ^ 2) ^ (lam - 1))
        = ((N : ℝ) - 2) * (t - y) * G y * (1 - 2 * t * y + y ^ 2) ^ (lam - 1) := by
      rw [← mul_assoc, mul_comm (∑' m : ℕ, _) (1 - 2 * t * y + y ^ 2), hode]
    rw [e, hlam]
    ring
  have hdiff : DifferentiableOn ℝ H (Set.Ioo (-1) 1) := fun y hy => (hderiv y hy).differentiableAt.differentiableWithinAt
  have heq : Set.EqOn (deriv H) 0 (Set.Ioo (-1) 1) := fun y hy => (hderiv y hy).deriv
  have h0mem : (0 : ℝ) ∈ Set.Ioo (-1 : ℝ) 1 := ⟨by norm_num, by norm_num⟩
  have hrmem : r ∈ Set.Ioo (-1 : ℝ) 1 := ⟨by linarith [neg_abs_le r], by linarith [le_abs_self r]⟩
  have hc := isOpen_Ioo.is_const_of_deriv_eq_zero isPreconnected_Ioo hdiff heq hrmem h0mem
  have hH0 : H 0 = 1 := by
    simp only [hH, hG]
    rw [gegG_zero]
    simp
  rw [hH0] at hc
  have hqr := hq r hr
  have hGr : G r = (1 - 2 * t * r + r ^ 2) ^ (-lam) := by
    rw [Real.rpow_neg hqr.le]
    have hpos : 0 < (1 - 2 * t * r + r ^ 2) ^ lam := Real.rpow_pos_of_pos hqr lam
    simp only [hH] at hc
    field_simp
    linarith
  have hs := (summable_gegC_term hN ht hr).hasSum
  rw [← hGr]
  exact hs

end G2Kernel
