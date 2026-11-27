/-
G2S2.Ratio (stage S2): H4 (`hRatio`, the paper's Lemma 2.2) for the paper's coefficients `kConc N`, N ≥ 2.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.2, Lemma 2.2 (tex l.247).
The paper derives Lemma 2.2 from the Bessel ratio bound of [Am74, (16)] and [RS16, Thm 2]. This module uses a Wronskian ODE
instead, which needs no Bessel theory:
- D1 `kConc_deriv_mul`: x k_ℓ' = ℓ k_ℓ + x k_{ℓ+1}; D2 `kConc_succ_deriv_mul`: x k_{ℓ+1}' + (ℓ + N - 1) k_{ℓ+1} = x k_ℓ
  (termwise from S0's series `kSer`; the only Gamma fact used is Γ(s + 1) = s Γ(s)).
- F(x) = x^(N-1) (k_ℓ² - k_{ℓ+1}²) - (2ℓ + N - 1) x^(N-2) k_ℓ k_{ℓ+1} satisfies x F'(x) = (2ℓ + N - 1) x^(N-2) k_ℓ k_{ℓ+1} > 0
  and F(0) = 0, so F > 0 on (0, ∞) (`strictMonoOn_of_deriv_pos`).
- x^(N-1) (k_{ℓ+1}' k_ℓ - k_ℓ' k_{ℓ+1}) = F, so the Wronskian is positive, which is `hRatio (kConc N)`.
- F > 0 says 1 - R² - (2ν + 1) R / x > 0 for R = k_{ℓ+1}/k_ℓ = R_ν, ν = ℓ + N/2 - 1. Solving the quadratic gives the cited
  bound R_ν(x) < x / (ν + 1/2 + √((ν + 1/2)² + x²)) itself, and from it R_ν(x) < x / (ν + 1/2 + x) and k_{ℓ+1} < k_ℓ.
- Further facts the paper uses later "from the proof of Lemma 2.2": r_ℓ = ℓ/J + R_{ℓ+λ} (tex l.252), r_ℓ < 1 + ℓ/J and
  k_{ℓ+1}' < k_ℓ (tex l.2254), and R_ν and k_{ℓ+1}/k_0 = I_{ℓ+1+λ}/I_λ strictly increasing in J (tex l.2225).
-/
import G2S0.KData

noncomputable section
open Real Set

namespace G2Kernel

/-! ### Termwise facts -/

/-- x · (d/dx)(x/2)^p = p (x/2)^p -/
theorem mul_dpow_one (p : ℕ) (x : ℝ) : x * dpow 1 p x = (p : ℝ) * dpow 0 p x := by
  unfold dpow
  rcases Nat.eq_zero_or_pos p with rfl | hp
  · simp
  · obtain ⟨q, rfl⟩ : ∃ q, p = q + 1 := ⟨p - 1, by omega⟩
    simp only [Nat.descFactorial_one, Nat.descFactorial_zero, Nat.cast_one, one_mul, Nat.sub_zero,
      pow_zero, mul_one, pow_one, Nat.add_sub_cancel]
    ring

/-- (x/2)^(p+1) = (x/2)^p · (x/2) -/
theorem dpow_zero_succ (p : ℕ) (x : ℝ) : dpow 0 (p + 1) x = dpow 0 p x * (x / 2) := by
  simp only [dpow, Nat.descFactorial_zero, Nat.cast_one, one_mul, Nat.sub_zero, pow_zero, mul_one]
  ring

/-- Γ(s + 1) = s Γ(s) in the coefficients, at ℓ + 1 -/
theorem kCoef_succ_left {N : ℕ} (hN : 2 ≤ N) (l m : ℕ) :
    kCoef N (l + 1) m * (2 * (l : ℝ) + 2 * (m : ℝ) + (N : ℝ)) = 2 * kCoef N l m := by
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hl : (0 : ℝ) ≤ l := Nat.cast_nonneg l
  have hm : (0 : ℝ) ≤ m := Nat.cast_nonneg m
  have hs : 0 < (l : ℝ) + m + (N : ℝ) / 2 := by linarith
  have hcast : ((l + 1 : ℕ) : ℝ) + m + (N : ℝ) / 2 = ((l : ℝ) + m + (N : ℝ) / 2) + 1 := by push_cast; ring
  have hG : Real.Gamma ((l : ℝ) + m + (N : ℝ) / 2) ≠ 0 := (Real.Gamma_pos_of_pos hs).ne'
  have hmf : (m.factorial : ℝ) ≠ 0 := by exact_mod_cast m.factorial_ne_zero
  have hs' : (l : ℝ) + m + (N : ℝ) / 2 ≠ 0 := hs.ne'
  have key : ∀ (A F G s : ℝ), F ≠ 0 → G ≠ 0 → s ≠ 0 → A / (F * (s * G)) * (2 * s) = 2 * (A / (F * G)) := by
    intro A F G s hF hG hs
    field_simp
    try ring
  have h2s : 2 * (l : ℝ) + 2 * (m : ℝ) + (N : ℝ) = 2 * ((l : ℝ) + m + (N : ℝ) / 2) := by ring
  unfold kCoef
  rw [hcast, Real.Gamma_add_one hs', h2s]
  exact key _ _ _ _ hmf hG hs'

/-- the coefficient at m + 1 against the one at ℓ + 1 -/
theorem kCoef_succ_right (N l j : ℕ) : kCoef N l (j + 1) * ((j : ℝ) + 1) = kCoef N (l + 1) j := by
  have hl : (0 : ℝ) ≤ l := Nat.cast_nonneg l
  have hj0 : (0 : ℝ) ≤ j := Nat.cast_nonneg j
  have hN0 : (0 : ℝ) ≤ N := Nat.cast_nonneg N
  have hcast : (l : ℝ) + ((j + 1 : ℕ) : ℝ) + (N : ℝ) / 2 = ((l + 1 : ℕ) : ℝ) + (j : ℝ) + (N : ℝ) / 2 := by
    push_cast; ring
  have hpos : 0 < (l : ℝ) + 1 + (j : ℝ) + (N : ℝ) / 2 := by linarith
  have hG : Real.Gamma ((l : ℝ) + 1 + (j : ℝ) + (N : ℝ) / 2) ≠ 0 := (Real.Gamma_pos_of_pos hpos).ne'
  have hj : ((j : ℝ) + 1) ≠ 0 := by positivity
  have hjf : (j.factorial : ℝ) ≠ 0 := by exact_mod_cast j.factorial_ne_zero
  have key : ∀ (A F G t : ℝ), t ≠ 0 → F ≠ 0 → G ≠ 0 → A / (t * F * G) * t = A / (F * G) := by
    intro A F G t ht hF hG
    field_simp
    try ring
  unfold kCoef
  rw [hcast, Nat.factorial_succ, Nat.cast_mul]
  push_cast
  exact key _ _ _ _ hj hjf hG

/-- k_{ℓ+1}(0) = 0 -/
theorem kConc_succ_zero (N l : ℕ) : kConc N (l + 1) 0 = 0 := by
  have hterm : ∀ m : ℕ, (0 : ℝ) ^ (l + 1 + 2 * m) = 0 := fun m => zero_pow (by omega)
  simp only [kConc, hterm, zero_div, tsum_zero, mul_zero]

/-- the derivative of k_ℓ is the first termwise derivative series -/
theorem deriv_kConc {N : ℕ} (hN : 2 ≤ N) (l : ℕ) : deriv (kConc N l) = kSer N l 1 := by
  rw [kConc_eq_kSer]; exact deriv_kSer hN l 0

/-- a series whose first term vanishes, shifted by one -/
theorem tsum_eq_tsum_of_shift {f g : ℕ → ℝ} (hf : Summable f) (h0 : f 0 = 0) (hs : ∀ j, f (j + 1) = g j) :
    ∑' m, f m = ∑' j, g j := by
  rw [hf.tsum_eq_zero_add, h0, zero_add]
  exact tsum_congr hs

/-! ### The derivative identities -/

/-- **D1**: x k_ℓ'(x) = ℓ k_ℓ(x) + x k_{ℓ+1}(x) (the paper's I_ν' = I_{ν+1} + (ν/x) I_ν, proof of Lemma 2.2) -/
theorem kConc_deriv_mul (N : ℕ) (hN : 2 ≤ N) (l : ℕ) (x : ℝ) :
    x * deriv (kConc N l) x = (l : ℝ) * kConc N l x + x * kConc N (l + 1) x := by
  rw [deriv_kConc hN l, kConc_eq_kSer N l, kConc_eq_kSer N (l + 1)]
  suffices h : x * kSer N l 1 x - (l : ℝ) * kSer N l 0 x = x * kSer N (l + 1) 0 x by linarith
  have hs1 := (summable_kTerm hN l 1 x).mul_left x
  have hs0 := (summable_kTerm hN l 0 x).mul_left (l : ℝ)
  unfold kSer
  rw [← tsum_mul_left, ← tsum_mul_left, ← tsum_mul_left, ← Summable.tsum_sub hs1 hs0]
  refine tsum_eq_tsum_of_shift (hs1.sub hs0) ?_ (fun j => ?_)
  · show x * (kCoef N l 0 * dpow 1 l x) - (l : ℝ) * (kCoef N l 0 * dpow 0 l x) = 0
    linear_combination (kCoef N l 0) * mul_dpow_one l x
  · show x * (kCoef N l (j + 1) * dpow 1 (l + 2 * (j + 1)) x) -
        (l : ℝ) * (kCoef N l (j + 1) * dpow 0 (l + 2 * (j + 1)) x) =
      x * (kCoef N (l + 1) j * dpow 0 (l + 1 + 2 * j) x)
    have h1 := mul_dpow_one (l + 2 * (j + 1)) x
    have h2 := kCoef_succ_right N l j
    have h3 : dpow 0 (l + 2 * (j + 1)) x = dpow 0 (l + 1 + 2 * j) x * (x / 2) := by
      rw [show l + 2 * (j + 1) = (l + 1 + 2 * j) + 1 by ring]
      exact dpow_zero_succ (l + 1 + 2 * j) x
    push_cast at h1
    linear_combination (kCoef N l (j + 1)) * h1 + (2 * dpow 0 (l + 2 * (j + 1)) x) * h2 +
      (2 * kCoef N (l + 1) j) * h3

/-- **D2**: x k_{ℓ+1}'(x) + (ℓ + N - 1) k_{ℓ+1}(x) = x k_ℓ(x) (the paper's I_{ν+1}' = I_ν - ((ν+1)/x) I_{ν+1}) -/
theorem kConc_succ_deriv_mul (N : ℕ) (hN : 2 ≤ N) (l : ℕ) (x : ℝ) :
    x * deriv (kConc N (l + 1)) x + ((l : ℝ) + (N : ℝ) - 1) * kConc N (l + 1) x = x * kConc N l x := by
  rw [deriv_kConc hN (l + 1), kConc_eq_kSer N (l + 1), kConc_eq_kSer N l]
  have hs1 := (summable_kTerm hN (l + 1) 1 x).mul_left x
  have hs0 := (summable_kTerm hN (l + 1) 0 x).mul_left ((l : ℝ) + (N : ℝ) - 1)
  unfold kSer
  rw [← tsum_mul_left, ← tsum_mul_left, ← tsum_mul_left, ← Summable.tsum_add hs1 hs0]
  refine tsum_congr (fun m => ?_)
  show x * (kCoef N (l + 1) m * dpow 1 (l + 1 + 2 * m) x) +
      ((l : ℝ) + (N : ℝ) - 1) * (kCoef N (l + 1) m * dpow 0 (l + 1 + 2 * m) x) =
    x * (kCoef N l m * dpow 0 (l + 2 * m) x)
  have h1 := mul_dpow_one (l + 1 + 2 * m) x
  have h2 := kCoef_succ_left hN l m
  have h3 : dpow 0 (l + 1 + 2 * m) x = dpow 0 (l + 2 * m) x * (x / 2) := by
    rw [show l + 1 + 2 * m = (l + 2 * m) + 1 by ring]
    exact dpow_zero_succ (l + 2 * m) x
  push_cast at h1
  linear_combination (kCoef N (l + 1) m) * h1 + (dpow 0 (l + 1 + 2 * m) x) * h2 + (2 * kCoef N l m) * h3

/-- the three-term recurrence x (k_ℓ - k_{ℓ+2}) = (2ℓ + N) k_{ℓ+1} (I_{ν-1} - I_{ν+1} = (2ν/x) I_ν) -/
theorem kConc_three_term (N : ℕ) (hN : 2 ≤ N) (l : ℕ) (x : ℝ) :
    x * (kConc N l x - kConc N (l + 2) x) = (2 * (l : ℝ) + (N : ℝ)) * kConc N (l + 1) x := by
  have h1 : x * deriv (kConc N (l + 1)) x = ((l : ℝ) + 1) * kConc N (l + 1) x + x * kConc N (l + 2) x := by
    have h := kConc_deriv_mul N hN (l + 1) x
    push_cast at h
    exact h
  have h2 := kConc_succ_deriv_mul N hN l x
  linear_combination h1 - h2

/-! ### The Wronskian ODE -/

/-- the auxiliary function F of the Wronskian ODE: y^(M+1) (u² - v²) - a y^M u v -/
def wronskF (u v : ℝ → ℝ) (M : ℕ) (a : ℝ) (y : ℝ) : ℝ :=
  y ^ (M + 1) * (u y * u y - v y * v y) - a * y ^ M * u y * v y

theorem mul_natCast_mul_pow_pred (M : ℕ) (y : ℝ) : y * ((M : ℝ) * y ^ (M - 1)) = (M : ℝ) * y ^ M := by
  cases M with
  | zero => simp
  | succ n =>
    rw [Nat.add_sub_cancel]
    push_cast
    ring

/-- the Wronskian ODE argument for any u, v with the two derivative identities (c = b + M + 1, a = 2b + M + 1):
x F'(x) = a x^M u v > 0 and F(0) = 0 give F(x) > 0 for x > 0 -/
theorem wronskF_pos_of_ode {u v u' v' : ℝ → ℝ} (M : ℕ) {b : ℝ} (hb : 0 ≤ b)
    (hu : ∀ y, HasDerivAt u (u' y) y) (hv : ∀ y, HasDerivAt v (v' y) y)
    (h1 : ∀ y, y * u' y = b * u y + y * v y)
    (h2 : ∀ y, y * v' y + (b + (M : ℝ) + 1) * v y = y * u y)
    (hupos : ∀ y, 0 < y → 0 < u y) (hvpos : ∀ y, 0 < y → 0 < v y) (hv0 : v 0 = 0)
    {x : ℝ} (hx : 0 < x) :
    0 < wronskF u v M (2 * b + (M : ℝ) + 1) x := by
  have ha : 0 < 2 * b + (M : ℝ) + 1 := by positivity
  have hp1 : ∀ y : ℝ, HasDerivAt (fun y : ℝ => y ^ (M + 1)) (((M : ℝ) + 1) * y ^ M) y := fun y => by
    simpa using hasDerivAt_pow (M + 1) y
  have key : ∀ y, ∃ D, HasDerivAt (wronskF u v M (2 * b + (M : ℝ) + 1)) D y ∧
      y * D = (2 * b + (M : ℝ) + 1) * y ^ M * u y * v y := by
    intro y
    refine ⟨_, ((hp1 y).mul (((hu y).mul (hu y)).sub ((hv y).mul (hv y)))).sub
      ((((hasDerivAt_pow M y).const_mul (2 * b + (M : ℝ) + 1)).mul (hu y)).mul (hv y)), ?_⟩
    simp only [Pi.mul_apply, Pi.sub_apply]
    have e1 := h1 y
    have e2 := h2 y
    have e3 := mul_natCast_mul_pow_pred M y
    linear_combination (2 * u y * y ^ (M + 1) - (2 * b + (M : ℝ) + 1) * y ^ M * v y) * e1 +
      (-2 * v y * y ^ (M + 1) - (2 * b + (M : ℝ) + 1) * y ^ M * u y) * e2 +
      (-(2 * b + (M : ℝ) + 1) * u y * v y) * e3
  have hcont : ContinuousOn (wronskF u v M (2 * b + (M : ℝ) + 1)) (Ici 0) := fun y _ => by
    obtain ⟨D, hD, _⟩ := key y
    exact hD.continuousAt.continuousWithinAt
  have hmono : StrictMonoOn (wronskF u v M (2 * b + (M : ℝ) + 1)) (Ici 0) := by
    apply strictMonoOn_of_deriv_pos (convex_Ici 0) hcont
    intro y hy
    rw [interior_Ici, mem_Ioi] at hy
    obtain ⟨D, hD, hyD⟩ := key y
    rw [hD.deriv]
    have hpos : 0 < y * D := by
      rw [hyD]
      exact mul_pos (mul_pos (mul_pos ha (pow_pos hy M)) (hupos y hy)) (hvpos y hy)
    exact pos_of_mul_pos_right hpos hy.le
  have hF0 : wronskF u v M (2 * b + (M : ℝ) + 1) 0 = 0 := by
    rw [wronskF, hv0, pow_succ]
    ring
  have h := hmono (mem_Ici.mpr le_rfl) (mem_Ici.mpr hx.le) hx
  rw [hF0] at h
  exact h

/-- F > 0 on (0, ∞) for the paper's k (N = M + 2) -/
theorem wronskF_pos (M l : ℕ) {x : ℝ} (hx : 0 < x) :
    0 < x ^ (M + 1) * (kConc (M + 2) l x * kConc (M + 2) l x - kConc (M + 2) (l + 1) x * kConc (M + 2) (l + 1) x) -
      (2 * (l : ℝ) + (M : ℝ) + 1) * x ^ M * kConc (M + 2) l x * kConc (M + 2) (l + 1) x := by
  have hN : 2 ≤ M + 2 := by omega
  have hu : ∀ y, HasDerivAt (kConc (M + 2) l) (deriv (kConc (M + 2) l) y) y := fun y => by
    rw [kConc_eq_kSer]; exact (differentiable_kSer hN l 0 y).hasDerivAt
  have hv : ∀ y, HasDerivAt (kConc (M + 2) (l + 1)) (deriv (kConc (M + 2) (l + 1)) y) y := fun y => by
    rw [kConc_eq_kSer]; exact (differentiable_kSer hN (l + 1) 0 y).hasDerivAt
  have h2 : ∀ y, y * deriv (kConc (M + 2) (l + 1)) y + ((l : ℝ) + (M : ℝ) + 1) * kConc (M + 2) (l + 1) y =
      y * kConc (M + 2) l y := fun y => by
    have h := kConc_succ_deriv_mul (M + 2) hN l y
    push_cast at h
    linear_combination h
  exact wronskF_pos_of_ode M (Nat.cast_nonneg l) hu hv (kConc_deriv_mul (M + 2) hN l) h2
    (fun y hy => kConc_pos hN l hy) (fun y hy => kConc_pos hN (l + 1) hy) (kConc_succ_zero (M + 2) l) hx

/-- **The Wronskian is positive**: k_{ℓ+1}' k_ℓ - k_ℓ' k_{ℓ+1} > 0 for x > 0 (k is TP2 in (ℓ, J), the remark after
Lemma 2.2) -/
theorem kConc_wronskian_pos (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {x : ℝ} (hx : 0 < x) :
    0 < deriv (kConc N (l + 1)) x * kConc N l x - deriv (kConc N l) x * kConc N (l + 1) x := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  have hF := wronskF_pos M l hx
  have h1 := kConc_deriv_mul (M + 2) hN l x
  have h2 := kConc_succ_deriv_mul (M + 2) hN l x
  push_cast at h2
  have hxM : 0 < x ^ (M + 1) := pow_pos hx _
  have key : x ^ (M + 1) * (deriv (kConc (M + 2) (l + 1)) x * kConc (M + 2) l x -
      deriv (kConc (M + 2) l) x * kConc (M + 2) (l + 1) x) =
      x ^ (M + 1) * (kConc (M + 2) l x * kConc (M + 2) l x - kConc (M + 2) (l + 1) x * kConc (M + 2) (l + 1) x) -
        (2 * (l : ℝ) + (M : ℝ) + 1) * x ^ M * kConc (M + 2) l x * kConc (M + 2) (l + 1) x := by
    linear_combination (x ^ M * kConc (M + 2) l x) * h2 - (x ^ M * kConc (M + 2) (l + 1) x) * h1
  rw [← key] at hF
  exact pos_of_mul_pos_right hF hxM.le

/-! ### H4 -/

/-- **H4 for the paper's k** (Lemma 2.2): `hRatio (kConc N)` for every N ≥ 2 -/
theorem hRatio_kConc (N : ℕ) (hN : 2 ≤ N) : hRatio (kConc N) := by
  intro J hJ
  apply strictMono_nat_of_lt_succ
  intro l
  have hu := kConc_pos hN l hJ
  have hv := kConc_pos hN (l + 1) hJ
  have hW := kConc_wronskian_pos N hN l hJ
  show deriv (kConc N l) J / kConc N l J < deriv (kConc N (l + 1)) J / kConc N (l + 1) J
  rw [div_lt_div_iff₀ hu hv]
  linarith

/-! ### The Bessel ratio bound and its consequences -/

/-- the Bessel ratio bound the paper cites ([Am74, (16)], [RS16, Thm 2]) for R_ν = k_{ℓ+1}/k_ℓ, ν = ℓ + N/2 - 1:
R_ν(x) < x / (ν + 1/2 + √((ν + 1/2)² + x²)) -/
theorem kConc_ratio_lt (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {x : ℝ} (hx : 0 < x) :
    kConc N (l + 1) x / kConc N l x <
      x / (((l : ℝ) + (N : ℝ) / 2 - 1 / 2) + Real.sqrt (((l : ℝ) + (N : ℝ) / 2 - 1 / 2) ^ 2 + x ^ 2)) := by
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  have hF := wronskF_pos M l hx
  have hu := kConc_pos hN l hx
  have hv := kConc_pos hN (l + 1) hx
  have hl : (0 : ℝ) ≤ l := Nat.cast_nonneg l
  have hM : (0 : ℝ) ≤ M := Nat.cast_nonneg M
  have hc : ((l : ℝ) + ((M + 2 : ℕ) : ℝ) / 2 - 1 / 2) = (2 * (l : ℝ) + (M : ℝ) + 1) / 2 := by push_cast; ring
  rw [hc]
  have hc0 : 0 < (2 * (l : ℝ) + (M : ℝ) + 1) / 2 := by positivity
  have hxM : 0 < x ^ M := pow_pos hx M
  -- F > 0 gives x (u² - v²) - (2ℓ + M + 1) u v > 0
  have hq : 0 < x * (kConc (M + 2) l x * kConc (M + 2) l x - kConc (M + 2) (l + 1) x * kConc (M + 2) (l + 1) x) -
      (2 * (l : ℝ) + (M : ℝ) + 1) * (kConc (M + 2) l x * kConc (M + 2) (l + 1) x) := by
    have e : x ^ (M + 1) * (kConc (M + 2) l x * kConc (M + 2) l x -
        kConc (M + 2) (l + 1) x * kConc (M + 2) (l + 1) x) -
        (2 * (l : ℝ) + (M : ℝ) + 1) * x ^ M * kConc (M + 2) l x * kConc (M + 2) (l + 1) x =
        x ^ M * (x * (kConc (M + 2) l x * kConc (M + 2) l x - kConc (M + 2) (l + 1) x * kConc (M + 2) (l + 1) x) -
          (2 * (l : ℝ) + (M : ℝ) + 1) * (kConc (M + 2) l x * kConc (M + 2) (l + 1) x)) := by ring
    rw [e] at hF
    exact pos_of_mul_pos_right hF hxM.le
  -- in terms of R = v / u: x (1 - R²) - (2ℓ + M + 1) R > 0
  set R := kConc (M + 2) (l + 1) x / kConc (M + 2) l x with hR_def
  have hR0 : 0 < R := div_pos hv hu
  have hvR : kConc (M + 2) (l + 1) x = R * kConc (M + 2) l x := by
    rw [hR_def]; exact (div_mul_cancel₀ _ hu.ne').symm
  have hq' : 0 < x * (1 - R * R) - (2 * (l : ℝ) + (M : ℝ) + 1) * R := by
    have e : (kConc (M + 2) l x * kConc (M + 2) l x) * (x * (1 - R * R) - (2 * (l : ℝ) + (M : ℝ) + 1) * R) =
        x * (kConc (M + 2) l x * kConc (M + 2) l x - kConc (M + 2) (l + 1) x * kConc (M + 2) (l + 1) x) -
        (2 * (l : ℝ) + (M : ℝ) + 1) * (kConc (M + 2) l x * kConc (M + 2) (l + 1) x) := by
      rw [hvR]; ring
    rw [← e] at hq
    exact pos_of_mul_pos_right hq (mul_pos hu hu).le
  -- (x R + c)² < c² + x², so x R + c < √(c² + x²)
  set c := (2 * (l : ℝ) + (M : ℝ) + 1) / 2 with hc_def
  have hlt : x * R + c < Real.sqrt (c ^ 2 + x ^ 2) := by
    rw [Real.lt_sqrt (add_pos (mul_pos hx hR0) hc0).le]
    have e : 2 * (l : ℝ) + (M : ℝ) + 1 = 2 * c := by rw [hc_def]; ring
    rw [e] at hq'
    nlinarith [mul_pos hx hq']
  set s := Real.sqrt (c ^ 2 + x ^ 2) with hs_def
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hs2 : s ^ 2 = c ^ 2 + x ^ 2 := Real.sq_sqrt (by positivity)
  have hcs : 0 < c + s := by linarith
  rw [lt_div_iff₀ hcs]
  have h1 : x * (R * (c + s)) < x * x := by nlinarith [mul_lt_mul_of_pos_right hlt hcs, hs2]
  exact lt_of_mul_lt_mul_left h1 hx.le

/-- the weaker form R_ν(x) < x / (ν + 1/2 + x) (tex l.2255) -/
theorem kConc_ratio_lt_simple (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {x : ℝ} (hx : 0 < x) :
    kConc N (l + 1) x / kConc N l x < x / (((l : ℝ) + (N : ℝ) / 2 - 1 / 2) + x) := by
  have h := kConc_ratio_lt N hN l hx
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hl : (0 : ℝ) ≤ l := Nat.cast_nonneg l
  have hc0 : 0 < (l : ℝ) + (N : ℝ) / 2 - 1 / 2 := by linarith
  have hsx : x ≤ Real.sqrt (((l : ℝ) + (N : ℝ) / 2 - 1 / 2) ^ 2 + x ^ 2) :=
    (Real.le_sqrt hx.le (by positivity)).mpr (le_add_of_nonneg_left (sq_nonneg _))
  have hle : x / (((l : ℝ) + (N : ℝ) / 2 - 1 / 2) + Real.sqrt (((l : ℝ) + (N : ℝ) / 2 - 1 / 2) ^ 2 + x ^ 2)) ≤
      x / (((l : ℝ) + (N : ℝ) / 2 - 1 / 2) + x) :=
    div_le_div_of_nonneg_left hx.le (by linarith) (by linarith)
  exact lt_of_lt_of_le h hle

/-- k_{ℓ+1}(x) < k_ℓ(x) for x > 0 (tex l.2063) -/
theorem kConc_succ_lt (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {x : ℝ} (hx : 0 < x) :
    kConc N (l + 1) x < kConc N l x := by
  have h := kConc_ratio_lt_simple N hN l hx
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hl : (0 : ℝ) ≤ l := Nat.cast_nonneg l
  have hc0 : 0 < (l : ℝ) + (N : ℝ) / 2 - 1 / 2 := by linarith
  have h1 : x / (((l : ℝ) + (N : ℝ) / 2 - 1 / 2) + x) < 1 := by
    rw [div_lt_one (by linarith)]; linarith
  exact (div_lt_one (kConc_pos hN l hx)).mp (lt_trans h h1)

/-! ### Further consequences used later in the paper -/

/-- r_ℓ(J) = ℓ/J + R_{ℓ+λ}(J) with R_{ℓ+λ} = k_{ℓ+1}/k_ℓ (tex l.252) -/
theorem kConc_logDeriv_eq (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {x : ℝ} (hx : 0 < x) :
    deriv (kConc N l) x / kConc N l x = (l : ℝ) / x + kConc N (l + 1) x / kConc N l x := by
  have hu := kConc_pos hN l hx
  have h := kConc_deriv_mul N hN l x
  rw [div_add_div _ _ hx.ne' hu.ne', div_eq_div_iff hu.ne' (mul_ne_zero hx.ne' hu.ne')]
  linear_combination (kConc N l x) * h

/-- r_ℓ(J) < 1 + ℓ/J (tex l.2254) -/
theorem kConc_logDeriv_lt (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {x : ℝ} (hx : 0 < x) :
    deriv (kConc N l) x / kConc N l x < 1 + (l : ℝ) / x := by
  rw [kConc_logDeriv_eq N hN l hx]
  have h1 : kConc N (l + 1) x / kConc N l x < 1 := (div_lt_one (kConc_pos hN l hx)).mpr (kConc_succ_lt N hN l hx)
  linarith

/-- k_{ℓ+1}'(x) < k_ℓ(x) for x > 0, i.e. r_{ℓ+1} k_{ℓ+1} < k_ℓ (tex l.2254) -/
theorem kConc_succ_deriv_lt (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {x : ℝ} (hx : 0 < x) :
    deriv (kConc N (l + 1)) x < kConc N l x := by
  have h := kConc_succ_deriv_mul N hN l x
  have hN' : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hl : (0 : ℝ) ≤ l := Nat.cast_nonneg l
  have hpos : 0 < ((l : ℝ) + (N : ℝ) - 1) * kConc N (l + 1) x := mul_pos (by linarith) (kConc_pos hN (l + 1) hx)
  have h2 : x * deriv (kConc N (l + 1)) x < x * kConc N l x := by linarith
  exact lt_of_mul_lt_mul_left h2 hx.le

/-- R_ν = k_{ℓ+1}/k_ℓ is strictly increasing in J on (0, ∞) (tex l.2225, "proof of Lemma 2.2") -/
theorem kConc_ratio_strictMonoOn (N : ℕ) (hN : 2 ≤ N) (l : ℕ) :
    StrictMonoOn (fun x => kConc N (l + 1) x / kConc N l x) (Ioi 0) := by
  have hd : ∀ x, 0 < x → HasDerivAt (fun x => kConc N (l + 1) x / kConc N l x)
      ((deriv (kConc N (l + 1)) x * kConc N l x - kConc N (l + 1) x * deriv (kConc N l) x) / kConc N l x ^ 2) x := by
    intro x hx
    have hu : HasDerivAt (kConc N l) (deriv (kConc N l) x) x := by
      rw [kConc_eq_kSer]; exact (differentiable_kSer hN l 0 x).hasDerivAt
    have hv : HasDerivAt (kConc N (l + 1)) (deriv (kConc N (l + 1)) x) x := by
      rw [kConc_eq_kSer]; exact (differentiable_kSer hN (l + 1) 0 x).hasDerivAt
    exact hv.fun_div hu (kConc_pos hN l hx).ne'
  apply strictMonoOn_of_deriv_pos (convex_Ioi 0)
  · intro x hx
    exact (hd x (mem_Ioi.mp hx)).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ioi, mem_Ioi] at hx
    rw [(hd x hx).deriv]
    have hW := kConc_wronskian_pos N hN l hx
    refine div_pos ?_ (pow_pos (kConc_pos hN l hx) 2)
    linarith [mul_comm (kConc N (l + 1) x) (deriv (kConc N l) x)]

/-- k_{ℓ+1}/k_0 = I_{ℓ+1+λ}/I_λ is strictly increasing in J on (0, ∞) (tex l.2225: a product of the ratios R_ν) -/
theorem kConc_div_zero_strictMonoOn (N : ℕ) (hN : 2 ≤ N) (l : ℕ) :
    StrictMonoOn (fun x => kConc N (l + 1) x / kConc N 0 x) (Ioi 0) := by
  induction l with
  | zero => exact kConc_ratio_strictMonoOn N hN 0
  | succ n ih =>
    intro a ha b hb hab
    have hR := kConc_ratio_strictMonoOn N hN (n + 1) ha hb hab
    have hI := ih ha hb hab
    have ha0 : 0 < a := ha
    have hb0 : 0 < b := hb
    beta_reduce at hR hI ⊢
    have key : ∀ y, 0 < y → kConc N (n + 1 + 1) y / kConc N (n + 1) y * (kConc N (n + 1) y / kConc N 0 y) =
        kConc N (n + 1 + 1) y / kConc N 0 y := fun y hy => div_mul_div_cancel₀ (kConc_pos hN (n + 1) hy).ne'
    rw [← key a ha0, ← key b hb0]
    have p1 : 0 < kConc N (n + 1 + 1) a / kConc N (n + 1) a := div_pos (kConc_pos hN _ ha0) (kConc_pos hN _ ha0)
    have p2 : 0 < kConc N (n + 1) a / kConc N 0 a := div_pos (kConc_pos hN _ ha0) (kConc_pos hN _ ha0)
    calc kConc N (n + 1 + 1) a / kConc N (n + 1) a * (kConc N (n + 1) a / kConc N 0 a)
        < kConc N (n + 1 + 1) b / kConc N (n + 1) b * (kConc N (n + 1) a / kConc N 0 a) :=
          mul_lt_mul_of_pos_right hR p2
      _ < kConc N (n + 1 + 1) b / kConc N (n + 1) b * (kConc N (n + 1) b / kConc N 0 b) :=
          mul_lt_mul_of_pos_left hI (lt_trans p1 hR)

end G2Kernel

#print axioms G2Kernel.kConc_deriv_mul
#print axioms G2Kernel.kConc_succ_deriv_mul
#print axioms G2Kernel.kConc_three_term
#print axioms G2Kernel.wronskF_pos
#print axioms G2Kernel.kConc_wronskian_pos
#print axioms G2Kernel.hRatio_kConc
#print axioms G2Kernel.kConc_ratio_lt
#print axioms G2Kernel.kConc_ratio_lt_simple
#print axioms G2Kernel.kConc_succ_lt
#print axioms G2Kernel.kConc_logDeriv_eq
#print axioms G2Kernel.kConc_logDeriv_lt
#print axioms G2Kernel.kConc_succ_deriv_lt
#print axioms G2Kernel.kConc_ratio_strictMonoOn
#print axioms G2Kernel.kConc_div_zero_strictMonoOn
