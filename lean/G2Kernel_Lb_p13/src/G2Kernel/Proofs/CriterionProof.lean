/-
G2Kernel.Proofs.CriterionProof: proof of `criterion_statement` (module M7, v1_6). Kernel proof, step L-b.
At separations `m ≥ m0`, `criterion_core` gives `Cov 𝒩² > 0` from (C1)–(C5). Case 1 (not top–bottom): the modes
l = 2, 3, 4 give at least (λ_4/λ_1)^m (p_2 + p_4). Case 2 (top–bottom): convexity of t ↦ t^m and (C2) give
λ_2^m + λ_4^m ≥ 2 λ_3^m, which with p_2 ≥ p_4 > 0 gives at least (λ_3/λ_1)^m (p_2 + p_4 + p_3). At separations `m < m0`,
condition (C6) is `Cov 𝒩² > 0` itself. In both cases `𝒩 > 0` gives `Cov > 0`.
-/
import G2Kernel.Criterion

namespace G2Kernel

/-- For `0 ≤ b ≤ a`, `0 ≤ c` and `2 c ≤ a + b`: `2 c^m ≤ a^m + b^m` for every `m`. -/
theorem two_pow_le_pow_add_pow (a b c : ℝ) (hb : 0 ≤ b) (hba : b ≤ a) (hc : 0 ≤ c)
    (habc : 2 * c ≤ a + b) : ∀ m : ℕ, 2 * c ^ m ≤ a ^ m + b ^ m := by
  intro m
  induction m with
  | zero => norm_num
  | succ m ih =>
    have h1 : 0 ≤ (a ^ m - b ^ m) * (a - b) :=
      mul_nonneg (sub_nonneg.mpr (pow_le_pow_left₀ hb hba m)) (sub_nonneg.mpr hba)
    have h2 : 0 ≤ c ^ m := pow_nonneg hc m
    have h3 : 2 * c ^ m * (2 * c) ≤ (a ^ m + b ^ m) * (a + b) :=
      mul_le_mul ih habc (by linarith) (by linarith)
    have key : a ^ (m + 1) + b ^ (m + 1)
        = ((a ^ m + b ^ m) * (a + b) + (a ^ m - b ^ m) * (a - b)) / 2 := by
      ring
    rw [key, pow_succ]
    nlinarith [h1, h3]

/-- The inequality logic of the proof of Theorem 6.4 at one separation: the identity of Lemma 6.3 and (C1)–(C5) give a
positive left side `Cov 𝒩²` of (6). -/
theorem criterion_core (D : ModeData) (hid : D.identity) (hcr : D.criterion) :
    0 < D.cov * D.Ncal ^ 2 := by
  unfold ModeData.identity at hid
  unfold ModeData.criterion at hcr
  obtain ⟨heq, -, hl5, hS, hR⟩ := hid
  obtain ⟨h21, h32, h43, h54, hC2, hcase⟩ := hcr
  have hl4 : 0 < D.l4 := lt_of_le_of_lt hl5 h54
  have hl3 : 0 < D.l3 := lt_trans hl4 h43
  have hl2 : 0 < D.l2 := lt_trans hl3 h32
  have hl1 : 0 < D.l1 := lt_trans hl2 h21
  have hx4 : 0 ≤ D.l4 / D.l1 := div_nonneg hl4.le hl1.le
  have hx3 : 0 ≤ D.l3 / D.l1 := div_nonneg hl3.le hl1.le
  have hx43 : D.l4 / D.l1 ≤ D.l3 / D.l1 := div_le_div_of_nonneg_right h43.le hl1.le
  have hx32 : D.l3 / D.l1 ≤ D.l2 / D.l1 := div_le_div_of_nonneg_right h32.le hl1.le
  have hx42 : D.l4 / D.l1 ≤ D.l2 / D.l1 := le_trans hx43 hx32
  have hC2' : 2 * (D.l3 / D.l1) ≤ D.l2 / D.l1 + D.l4 / D.l1 := by
    have h : 2 * D.l3 ≤ D.l2 + D.l4 := by linarith
    calc 2 * (D.l3 / D.l1) = (2 * D.l3) / D.l1 := by ring
      _ ≤ (D.l2 + D.l4) / D.l1 := div_le_div_of_nonneg_right h hl1.le
      _ = D.l2 / D.l1 + D.l4 / D.l1 := by ring
  have hS' := (abs_le.mp hS).1
  have hR' := (abs_le.mp hR).1
  simp only [ModeData.tailBound] at hcase
  rw [heq]
  rcases hcase with ⟨hp2, hp4, hp3, hB⟩ | ⟨hp2, hp4, hp42, hB⟩
  · have e1 : (D.l4 / D.l1) ^ D.m * (D.a2 * D.b2) ≤ (D.l2 / D.l1) ^ D.m * (D.a2 * D.b2) :=
      mul_le_mul_of_nonneg_right (pow_le_pow_left₀ hx4 hx42 D.m) hp2.le
    have e2 : 0 ≤ (D.l3 / D.l1) ^ D.m * (D.a3 * D.b3) := mul_nonneg (pow_nonneg hx3 D.m) hp3
    rw [mul_add] at hB
    linarith
  · have hconv := two_pow_le_pow_add_pow (D.l2 / D.l1) (D.l4 / D.l1) (D.l3 / D.l1) hx4 hx42 hx3 hC2' D.m
    have hx32m : (D.l3 / D.l1) ^ D.m ≤ (D.l2 / D.l1) ^ D.m := pow_le_pow_left₀ hx3 hx32 D.m
    have e1 : 2 * ((D.l3 / D.l1) ^ D.m * (D.a4 * D.b4)) ≤
        (D.l2 / D.l1) ^ D.m * (D.a4 * D.b4) + (D.l4 / D.l1) ^ D.m * (D.a4 * D.b4) := by
      nlinarith [mul_le_mul_of_nonneg_right hconv hp4.le]
    have e2 : (D.l3 / D.l1) ^ D.m * (D.a2 * D.b2) - (D.l3 / D.l1) ^ D.m * (D.a4 * D.b4) ≤
        (D.l2 / D.l1) ^ D.m * (D.a2 * D.b2) - (D.l2 / D.l1) ^ D.m * (D.a4 * D.b4) := by
      nlinarith [mul_le_mul_of_nonneg_right hx32m (sub_nonneg.mpr hp42)]
    rw [mul_add, mul_add] at hB
    linarith

theorem criterion_thm : criterion_statement := by
  unfold criterion_statement
  intro D m0 hid hcr hdir
  have hN : 0 < D.Ncal := by
    unfold ModeData.identity at hid
    exact hid.2.1
  have hN2 : 0 < D.Ncal ^ 2 := by positivity
  have hmain : 0 < D.cov * D.Ncal ^ 2 := by
    rcases le_or_gt m0 D.m with h | h
    · exact criterion_core D hid (hcr h)
    · exact hdir h
  by_contra hneg
  push Not at hneg
  nlinarith [hmain, hN2, hneg]

end G2Kernel
