/-
G2S1.Expand (stage S1): display (3), e^{Jt} = Σ_ℓ k_ℓ(J) d_ℓ C̃_ℓ(t) on [-1, 1], the dimension bound, and H2 (`hFH`)
for the paper's data.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1, displays (2), (3) and
d_ℓ ≤ (ℓ+1)^{N-1}.
- (P_n) t^n/n! = Σ_e c'(e, n) Π_e(t) and k_e(J) = Σ_n c'(e, n) J^n give e^{Jt} = Σ_n Σ_e c'(e,n) J^n Π_e(t)
  = Σ_e k_e(J) Π_e(t): one rearrangement of an absolutely summable double series (crude bound |C̃_e| ≤ 3^e on [-1, 1]).
-/
import G2S1.TwoPoint

noncomputable section
open Real Finset MeasureTheory

namespace G2Kernel

/-! ### Elementary bounds -/

theorem abs_sub_le_add' (a b : ℝ) : |a - b| ≤ |a| + |b| := by
  have h1 := le_abs_self a
  have h2 := neg_abs_le a
  have h3 := le_abs_self b
  have h4 := neg_abs_le b
  rw [abs_le]
  constructor <;> linarith

/-- the crude bound |C̃_n(t)| ≤ 3^n on [-1, 1] -/
theorem abs_CConc_le_three_pow {N : ℕ} (hN : 2 ≤ N) {t : ℝ} (ht : |t| ≤ 1) : ∀ n, |CConc N n t| ≤ 3 ^ n
  | 0 => by simp [CConc]
  | 1 => by
    show |t| ≤ 3 ^ 1
    linarith
  | n + 2 => by
    have h1 := abs_CConc_le_three_pow hN ht (n + 1)
    have h0 := abs_CConc_le_three_pow hN ht n
    have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
    have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg n
    have hD : (0 : ℝ) < ((n : ℝ) + 1) + ((N : ℝ) - 2) := by linarith
    have hA : (0 : ℝ) ≤ 2 * ((n : ℝ) + 1) + ((N : ℝ) - 2) := by linarith
    show |((2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * t * CConc N (n + 1) t - ((n : ℝ) + 1) * CConc N n t) /
      (((n : ℝ) + 1) + ((N : ℝ) - 2))| ≤ 3 ^ (n + 2)
    rw [abs_div, abs_of_pos hD, div_le_iff₀ hD]
    have h3 : (0 : ℝ) < 3 ^ n := by positivity
    have hX : |(2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * t * CConc N (n + 1) t|
        ≤ (2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * 3 ^ (n + 1) := by
      rw [abs_mul, abs_mul, abs_of_nonneg hA]
      calc (2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * |t| * |CConc N (n + 1) t|
          ≤ (2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * 1 * 3 ^ (n + 1) := by
            apply mul_le_mul (mul_le_mul_of_nonneg_left ht hA) h1 (abs_nonneg _) (by positivity)
        _ = _ := by ring
    have hY : |((n : ℝ) + 1) * CConc N n t| ≤ ((n : ℝ) + 1) * 3 ^ n := by
      rw [abs_mul, abs_of_nonneg (by positivity)]
      exact mul_le_mul_of_nonneg_left h0 (by positivity)
    calc |(2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * t * CConc N (n + 1) t - ((n : ℝ) + 1) * CConc N n t|
        ≤ (2 * ((n : ℝ) + 1) + ((N : ℝ) - 2)) * 3 ^ (n + 1) + ((n : ℝ) + 1) * 3 ^ n :=
          (abs_sub_le_add' _ _).trans (add_le_add hX hY)
      _ ≤ 3 ^ (n + 2) * (((n : ℝ) + 1) + ((N : ℝ) - 2)) := by
          rw [pow_succ, pow_succ, pow_succ]
          nlinarith

/-- with N = M + 2, d_ℓ > 0 -/
theorem dConc_pos_S1 {N : ℕ} (hN : 2 ≤ N) (l : ℕ) : 0 < dConc N l := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  rcases l with _ | a
  · rw [dConc_zero]; norm_num
  · rw [dConc_succ]
    have h : (0 : ℝ) < (Nat.choose (a + M) a : ℝ) := by exact_mod_cast Nat.choose_pos (by omega)
    have h' : (0 : ℝ) ≤ (Nat.choose (a + 1 + M) (a + 1) : ℝ) := Nat.cast_nonneg _
    linarith

theorem choose_add_le_pow (n k : ℕ) : ((Nat.choose (n + k) k : ℕ) : ℝ) ≤ ((n : ℝ) + 1) ^ k := by
  induction k with
  | zero => simp
  | succ k ih =>
    have h := Nat.add_one_mul_choose_eq (n + k) k
    have h' : ((n + k : ℝ) + 1) * (Nat.choose (n + k) k : ℝ) = (Nat.choose (n + k + 1) (k + 1) : ℝ) * ((k : ℝ) + 1) := by
      exact_mod_cast h
    rw [show n + (k + 1) = n + k + 1 by ring]
    have hk : (0 : ℝ) < (k : ℝ) + 1 := by positivity
    have hle : (n + k : ℝ) + 1 ≤ ((n : ℝ) + 1) * ((k : ℝ) + 1) := by
      have : (0 : ℝ) ≤ (n : ℝ) * k := by positivity
      nlinarith
    have hc : (0 : ℝ) ≤ (Nat.choose (n + k) k : ℝ) := Nat.cast_nonneg _
    rw [← mul_le_mul_iff_of_pos_right hk, ← h', pow_succ]
    calc ((n + k : ℝ) + 1) * (Nat.choose (n + k) k : ℝ) ≤ (((n : ℝ) + 1) * ((k : ℝ) + 1)) * ((n : ℝ) + 1) ^ k :=
          mul_le_mul hle ih hc (by positivity)
      _ = ((n : ℝ) + 1) ^ k * ((n : ℝ) + 1) * ((k : ℝ) + 1) := by ring

/-- the dimension bound d_ℓ ≤ (ℓ + 1)^N (the paper has (ℓ+1)^{N-1}; hFH asks for (ℓ+1)^N) -/
theorem dConc_le_pow {N : ℕ} (hN : 2 ≤ N) (l : ℕ) : dConc N l ≤ ((l : ℝ) + 1) ^ N := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  rcases l with _ | a
  · rw [dConc_zero]; simp
  · rw [dConc_succ]
    have h1 : ((Nat.choose (a + 1 + M) (a + 1) : ℕ) : ℝ) ≤ ((a : ℝ) + 2) ^ M := by
      rw [Nat.choose_symm_add]
      have := choose_add_le_pow (a + 1) M
      push_cast at this
      rw [show (a : ℝ) + 1 + 1 = (a : ℝ) + 2 by ring] at this
      exact this
    have h2 : ((Nat.choose (a + M) a : ℕ) : ℝ) ≤ ((a : ℝ) + 2) ^ M := by
      rw [Nat.choose_symm_add]
      have := choose_add_le_pow a M
      calc ((Nat.choose (a + M) M : ℕ) : ℝ) ≤ ((a : ℝ) + 1) ^ M := this
        _ ≤ ((a : ℝ) + 2) ^ M := pow_le_pow_left₀ (by positivity) (by linarith) M
    have h3 : (1 : ℝ) ≤ ((a : ℝ) + 2) ^ M := one_le_pow₀ (by linarith [(Nat.cast_nonneg a : (0 : ℝ) ≤ a)])
    push_cast
    calc ((Nat.choose (a + 1 + M) (a + 1) : ℕ) : ℝ) + ((Nat.choose (a + M) a : ℕ) : ℝ)
        ≤ 2 * ((a : ℝ) + 2) ^ M := by linarith
      _ ≤ ((a : ℝ) + 2) ^ 2 * ((a : ℝ) + 2) ^ M := by
          apply mul_le_mul_of_nonneg_right _ (by positivity)
          nlinarith [(Nat.cast_nonneg a : (0 : ℝ) ≤ a)]
      _ = ((a : ℝ) + 1 + 1) ^ (M + 2) := by ring

theorem abs_zon_le_three {N : ℕ} (hN : 2 ≤ N) (e : ℕ) {t : ℝ} (ht : |t| ≤ 1) :
    |zon N e t| ≤ dConc N e * 3 ^ e := by
  unfold zon
  rw [abs_mul, abs_of_pos (dConc_pos_S1 hN e)]
  exact mul_le_mul_of_nonneg_left (abs_CConc_le_three_pow hN ht e) (dConc_pos_S1 hN e).le

/-! ### k_e as a power series in J -/

theorem cK_nonneg {N : ℕ} (hN : 2 ≤ N) (e p : ℕ) : 0 ≤ cK N e p := by
  unfold cK
  split_ifs
  · exact div_nonneg (kCoef_pos hN e _).le (by positivity)
  · exact le_rfl

theorem hasSum_cK {N : ℕ} (hN : 2 ≤ N) (e : ℕ) (J : ℝ) : HasSum (fun n => cK N e n * J ^ n) (kConc N e J) := by
  have h0 : HasSum (fun m => kCoef N e m * dpow 0 (e + 2 * m) J) (kConc N e J) := by
    rw [kConc_eq_kSer]
    exact (summable_kTerm hN e 0 J).hasSum
  have hinj : Function.Injective (fun m : ℕ => e + 2 * m) := fun a b h => by simp only at h; omega
  rw [← hinj.hasSum_iff]
  · convert h0 using 1
    funext m
    simp only [Function.comp, cK_eq, dpow, Nat.descFactorial_zero, Nat.cast_one, one_mul, Nat.sub_zero, pow_zero,
      mul_one, div_pow]
    ring
  · intro n hn
    simp only [Set.mem_range, not_exists] at hn
    rcases cases_e e n with h | ⟨m, rfl⟩ | ⟨m, rfl⟩
    · rw [cK_of_lt h, zero_mul]
    · exact absurd rfl (hn m)
    · rw [cK_odd, zero_mul]

theorem abs_kConc_le {N : ℕ} (hN : 2 ≤ N) (e : ℕ) (J : ℝ) : |kConc N e J| ≤ kConc N e |J| := by
  have h1 := hasSum_cK hN e J
  have h2 := hasSum_cK hN e |J|
  have hn : ∀ n, ‖cK N e n * J ^ n‖ = cK N e n * |J| ^ n := by
    intro n
    rw [Real.norm_eq_abs, abs_mul, abs_of_nonneg (cK_nonneg hN e n), abs_pow]
  have hs : Summable (fun n => ‖cK N e n * J ^ n‖) := by
    simp only [hn]; exact h2.summable
  rw [← h1.tsum_eq, ← h2.tsum_eq, ← Real.norm_eq_abs]
  refine (norm_tsum_le_tsum_norm hs).trans (le_of_eq ?_)
  simp only [hn]

/-- k_e(|J|) ≤ K(J) (|J|/2)^e / e! with K(J) = Σ_m ((|J|/2)^2)^m / m! -/
theorem kConc_abs_le {N : ℕ} (hN : 2 ≤ N) (e : ℕ) (J : ℝ) :
    kConc N e |J| ≤ (∑' m : ℕ, ((|J| / 2) ^ 2) ^ m / (m.factorial : ℝ)) * ((|J| / 2) ^ e / (e.factorial : ℝ)) := by
  rw [kConc_eq_kSer]
  unfold kSer
  rw [← tsum_mul_right]
  have hs2 : Summable (fun m : ℕ => ((|J| / 2) ^ 2) ^ m / (m.factorial : ℝ) * ((|J| / 2) ^ e / (e.factorial : ℝ))) :=
    (Real.summable_pow_div_factorial _).mul_right _
  refine Summable.tsum_le_tsum (fun m => ?_) (summable_kTerm hN e 0 |J|) hs2
  simp only [dpow, Nat.descFactorial_zero, Nat.cast_one, one_mul, Nat.sub_zero, pow_zero, mul_one]
  have hk := kCoef_le hN e m
  have hJ : (0 : ℝ) ≤ |J| / 2 := by positivity
  have hef : (0 : ℝ) < (e.factorial : ℝ) := by exact_mod_cast e.factorial_pos
  have hmf : (0 : ℝ) < (m.factorial : ℝ) := by exact_mod_cast m.factorial_pos
  calc kCoef N e m * (|J| / 2) ^ (e + 2 * m) ≤ 1 / ((e.factorial : ℝ) * (m.factorial : ℝ)) * (|J| / 2) ^ (e + 2 * m) :=
        mul_le_mul_of_nonneg_right hk (by positivity)
    _ = ((|J| / 2) ^ 2) ^ m / (m.factorial : ℝ) * ((|J| / 2) ^ e / (e.factorial : ℝ)) := by
        rw [pow_add, pow_mul]
        field_simp

theorem summable_dConc_three_kConc {N : ℕ} (hN : 2 ≤ N) (J : ℝ) :
    Summable (fun e => dConc N e * 3 ^ e * kConc N e |J|) := by
  set K := ∑' m : ℕ, ((|J| / 2) ^ 2) ^ m / (m.factorial : ℝ)
  have hK : 0 ≤ K := tsum_nonneg (fun m => by positivity)
  have hsum := (summable_poly_pow_div_factorial N (show (0 : ℝ) ≤ 3 * (|J| / 2) by positivity)).mul_left K
  refine Summable.of_nonneg_of_le (fun e => ?_) (fun e => ?_) hsum
  · exact mul_nonneg (mul_nonneg (dConc_pos_S1 hN e).le (by positivity)) ((abs_nonneg _).trans (abs_kConc_le hN e J))
  · have h1 := dConc_le_pow hN e
    have h2 := kConc_abs_le hN e J
    have h3 : 0 ≤ kConc N e |J| := (abs_nonneg _).trans (abs_kConc_le hN e J)
    have hef : (0 : ℝ) < (e.factorial : ℝ) := by exact_mod_cast e.factorial_pos
    calc dConc N e * 3 ^ e * kConc N e |J| ≤ ((e : ℝ) + 1) ^ N * 3 ^ e * (K * ((|J| / 2) ^ e / (e.factorial : ℝ))) :=
          mul_le_mul (mul_le_mul_of_nonneg_right h1 (by positivity)) h2 h3 (by positivity)
      _ = K * (((e : ℝ) + 1) ^ N * (3 * (|J| / 2)) ^ e / (e.factorial : ℝ)) := by
          rw [mul_pow]; ring

/-- summability of the expansion (3) in absolute value -/
theorem summable_kConc_dConc {N : ℕ} (hN : 2 ≤ N) (J : ℝ) : Summable (fun l => |kConc N l J| * dConc N l) := by
  refine Summable.of_nonneg_of_le (fun e => mul_nonneg (abs_nonneg _) (dConc_pos_S1 hN e).le) (fun e => ?_)
    (summable_dConc_three_kConc hN J)
  have h1 := abs_kConc_le hN e J
  have h2 : (1 : ℝ) ≤ 3 ^ e := one_le_pow₀ (by norm_num)
  have h3 := (dConc_pos_S1 hN e).le
  calc |kConc N e J| * dConc N e ≤ kConc N e |J| * (dConc N e * 3 ^ e) :=
        mul_le_mul h1 (le_mul_of_one_le_right h3 h2) h3 ((abs_nonneg _).trans h1)
    _ = dConc N e * 3 ^ e * kConc N e |J| := by ring

/-! ### Display (3) -/

/-- display (3) on [-1, 1]: e^{Jt} = Σ_ℓ k_ℓ(J) Π_ℓ(t) -/
theorem exp_hasSum_zon {N : ℕ} (hN : 2 ≤ N) (J t : ℝ) (ht : |t| ≤ 1) :
    HasSum (fun e => kConc N e J * zon N e t) (Real.exp (J * t)) := by
  set F : ℕ × ℕ → ℝ := fun p => cK N p.1 p.2 * J ^ p.2 * zon N p.1 t with hF
  set G : ℕ × ℕ → ℝ := fun p => cK N p.1 p.2 * |J| ^ p.2 * (dConc N p.1 * 3 ^ p.1) with hG
  have hGnn : 0 ≤ G := fun p => mul_nonneg (mul_nonneg (cK_nonneg hN _ _) (by positivity))
    (mul_nonneg (dConc_pos_S1 hN _).le (by positivity))
  have hGfib : ∀ e, HasSum (fun n => G (e, n)) (dConc N e * 3 ^ e * kConc N e |J|) := by
    intro e
    have := (hasSum_cK hN e |J|).mul_right (dConc N e * 3 ^ e)
    simp only [hG]
    convert this using 1
    ring
  have hGs : Summable G := by
    rw [summable_prod_of_nonneg hGnn]
    refine ⟨fun e => (hGfib e).summable, ?_⟩
    simp only [fun e => (hGfib e).tsum_eq]
    exact summable_dConc_three_kConc hN J
  have hFs : Summable F := by
    refine Summable.of_norm_bounded hGs (fun p => ?_)
    simp only [hF, hG, Real.norm_eq_abs]
    rw [abs_mul, abs_mul, abs_of_nonneg (cK_nonneg hN _ _), abs_pow]
    exact mul_le_mul_of_nonneg_left (abs_zon_le_three hN p.1 ht) (by positivity [cK_nonneg hN p.1 p.2])
  have hFsum := hFs.hasSum
  -- fibers over e
  have hfe : ∀ e, HasSum (fun n => F (e, n)) (kConc N e J * zon N e t) := by
    intro e
    have := (hasSum_cK hN e J).mul_right (zon N e t)
    simpa only [hF] using this
  have h1 := hFsum.prod_fiberwise hfe
  -- fibers over n
  have hswap : HasSum (F ∘ (Equiv.prodComm ℕ ℕ)) (∑' p, F p) := (Equiv.prodComm ℕ ℕ).hasSum_iff.mpr hFsum
  have hfn : ∀ n, HasSum (fun e => (F ∘ (Equiv.prodComm ℕ ℕ)) (n, e)) ((J * t) ^ n / (n.factorial : ℝ)) := by
    intro n
    have hfin : HasSum (fun e => (F ∘ (Equiv.prodComm ℕ ℕ)) (n, e))
        (∑ e ∈ range (n + 1), (F ∘ (Equiv.prodComm ℕ ℕ)) (n, e)) := by
      apply hasSum_sum_of_ne_finset_zero
      intro e he
      simp only [mem_range, not_lt] at he
      simp only [Function.comp, Equiv.prodComm_apply, Prod.swap_prod_mk, hF]
      rw [cK_of_lt (show n < e by omega)]
      ring
    convert hfin using 1
    simp only [Function.comp, Equiv.prodComm_apply, Prod.swap_prod_mk, hF]
    have hP := pow_eq_sum_zon hN n t
    have hnf : (n.factorial : ℝ) ≠ 0 := by positivity
    rw [mul_pow, hP]
    field_simp
    rw [mul_sum]
    refine sum_congr rfl (fun e _ => by ring)
  have h2 := hswap.prod_fiberwise hfn
  have hexp : HasSum (fun n => (J * t) ^ n / (n.factorial : ℝ)) (Real.exp (J * t)) := by
    rw [Real.exp_eq_exp_ℝ]
    exact NormedSpace.expSeries_div_hasSum_exp (J * t)
  rw [h2.unique hexp] at h1
  exact h1

/-- H2 for the paper's data (N ≥ 2) -/
theorem hFH_conc (N : ℕ) (hN : 2 ≤ N) : hFH N (kConc N) (dConc N) (CConc N) := by
  refine ⟨fun J t ht => ?_, CConc_one N hN, fun l => ⟨(dConc_pos_S1 hN l).le, dConc_le_pow hN l⟩,
    fun a b x y => zon_proj hN a b x y⟩
  have ht' : |t| ≤ 1 := abs_le.mpr ⟨ht.1, ht.2⟩
  exact exp_hasSum_zon hN J t ht'

end G2Kernel
