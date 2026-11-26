/-
G2Kernel.Proofs.ChebyshevProof: proofs of `chebyshev_statement` and `chebyshev_strict_statement` (module M1).
Kernel proof, step L-b. Centre `f` at its mean `μ` and `g` at its value at the first index `k` with `f k ≥ μ`;
every term of the centred series is then nonnegative.
-/
import G2Kernel.Chebyshev

namespace G2Kernel

open Classical

theorem centered_expand (p f g : ℕ → ℝ) (μ c : ℝ) :
    (fun n => p n * ((f n - μ) * (g n - c))) =
      fun n => ((p n * (f n * g n) - μ * (p n * g n)) - c * (p n * f n)) + (μ * c) * p n := by
  funext n
  ring

theorem summable_centered (p f g : ℕ → ℝ) (hp : Summable p)
    (hf : Summable (fun n => p n * f n)) (hg : Summable (fun n => p n * g n))
    (hfg : Summable (fun n => p n * (f n * g n))) (μ c : ℝ) :
    Summable (fun n => p n * ((f n - μ) * (g n - c))) := by
  rw [centered_expand p f g μ c]
  exact ((hfg.sub (hg.mul_left μ)).sub (hf.mul_left c)).add (hp.mul_left (μ * c))

theorem covW_eq_centered (p f g : ℕ → ℝ) (hp1 : HasSum p 1)
    (hf : Summable (fun n => p n * f n)) (hg : Summable (fun n => p n * g n))
    (hfg : Summable (fun n => p n * (f n * g n))) (μ c : ℝ) (hμ : μ = ∑' k, p k * f k) :
    covW p f g = ∑' n, p n * ((f n - μ) * (g n - c)) := by
  have hp : Summable p := hp1.summable
  have h1 : Summable (fun n => p n * (f n * g n) - μ * (p n * g n)) := hfg.sub (hg.mul_left μ)
  have h2 : Summable (fun n => (p n * (f n * g n) - μ * (p n * g n)) - c * (p n * f n)) :=
    h1.sub (hf.mul_left c)
  rw [centered_expand p f g μ c, h2.tsum_add (hp.mul_left (μ * c)), h1.tsum_sub (hf.mul_left c),
    hfg.tsum_sub (hg.mul_left μ), tsum_mul_left, tsum_mul_left, tsum_mul_left, hp1.tsum_eq, ← hμ]
  unfold covW
  rw [← hμ]
  ring

theorem exists_pos_weight (p : ℕ → ℝ) (hp0 : ∀ n, 0 ≤ p n) (hp1 : HasSum p 1) :
    ∃ n, 0 < p n := by
  by_contra h
  push Not at h
  have hz : p = fun _ => 0 := funext fun n => le_antisymm (h n) (hp0 n)
  have h0 : HasSum p 0 := by
    rw [hz]
    exact hasSum_zero
  have := h0.unique hp1
  norm_num at this

theorem exists_ge_mean (p f : ℕ → ℝ) (hp0 : ∀ n, 0 ≤ p n) (hp1 : HasSum p 1)
    (hf : Summable (fun n => p n * f n)) : ∃ k, (∑' n, p n * f n) ≤ f k := by
  by_contra h
  push Not at h
  obtain ⟨n0, hn0⟩ := exists_pos_weight p hp0 hp1
  have e : (fun n => p n * ((∑' k, p k * f k) - f n)) =
      fun n => (∑' k, p k * f k) * p n - p n * f n := by
    funext n
    ring
  have hs : Summable (fun n => p n * ((∑' k, p k * f k) - f n)) := by
    rw [e]
    exact (hp1.summable.mul_left _).sub hf
  have hpos : 0 < ∑' n, p n * ((∑' k, p k * f k) - f n) :=
    hs.tsum_pos (fun n => mul_nonneg (hp0 n) (by linarith [h n])) n0
      (mul_pos hn0 (by linarith [h n0]))
  have hzero : ∑' n, p n * ((∑' k, p k * f k) - f n) = 0 := by
    rw [e, (hp1.summable.mul_left _).tsum_sub hf, tsum_mul_left, hp1.tsum_eq]
    ring
  linarith

theorem chebyshev_thm : chebyshev_statement := by
  unfold chebyshev_statement
  intro p f g hp0 hp1 hfm hgm hf hg hfg
  have hex : ∃ k, (∑' n, p n * f n) ≤ f k := exists_ge_mean p f hp0 hp1 hf
  have hk : (∑' n, p n * f n) ≤ f (Nat.find hex) := Nat.find_spec hex
  have hbelow : ∀ n, n < Nat.find hex → f n < ∑' n, p n * f n :=
    fun n hn => not_le.mp (Nat.find_min hex hn)
  rw [covW_eq_centered p f g hp1 hf hg hfg (∑' n, p n * f n) (g (Nat.find hex)) rfl]
  refine tsum_nonneg fun n => mul_nonneg (hp0 n) ?_
  rcases lt_or_ge n (Nat.find hex) with hn | hn
  · exact mul_nonneg_of_nonpos_of_nonpos (by linarith [hbelow n hn]) (by linarith [hgm hn.le])
  · exact mul_nonneg (by linarith [hfm hn]) (by linarith [hgm hn])

theorem chebyshev_strict_thm : chebyshev_strict_statement := by
  unfold chebyshev_strict_statement
  intro p f g hp0 hp1 hfm hgm hf hg hfg
  have hp0' : ∀ n, 0 ≤ p n := fun n => (hp0 n).le
  have hex : ∃ k, (∑' n, p n * f n) ≤ f k := exists_ge_mean p f hp0' hp1 hf
  have hk : (∑' n, p n * f n) ≤ f (Nat.find hex) := Nat.find_spec hex
  have hbelow : ∀ n, n < Nat.find hex → f n < ∑' n, p n * f n :=
    fun n hn => not_le.mp (Nat.find_min hex hn)
  rw [covW_eq_centered p f g hp1 hf hg hfg (∑' n, p n * f n) (g (Nat.find hex)) rfl]
  have hterm : ∀ n, 0 ≤ p n * ((f n - ∑' n, p n * f n) * (g n - g (Nat.find hex))) := by
    intro n
    refine mul_nonneg (hp0' n) ?_
    rcases lt_or_ge n (Nat.find hex) with hn | hn
    · exact mul_nonneg_of_nonpos_of_nonpos (by linarith [hbelow n hn]) (by linarith [hgm hn])
    · exact mul_nonneg (by linarith [hfm.monotone hn]) (by linarith [hgm.monotone hn])
  refine (summable_centered p f g hp1.summable hf hg hfg _ _).tsum_pos hterm (Nat.find hex + 1) ?_
  refine mul_pos (hp0 _) (mul_pos ?_ ?_)
  · linarith [hfm (Nat.lt_add_one (Nat.find hex))]
  · linarith [hgm (Nat.lt_add_one (Nat.find hex))]

end G2Kernel
