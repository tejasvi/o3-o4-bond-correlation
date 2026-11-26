/-
G2Kernel.Proofs.RPstepProof: proof of `rpCov_statement` (module M6a, the last step of Lemma 6.1). Kernel proof,
step L-b. Put m = ∫ F dμ. Since θ preserves μ, ∫ F∘θ dμ = m. The class is closed under F ↦ F - m, so reflection
positivity for F - m gives 0 ≤ ∫ (F - m)(F∘θ - m) dμ = ∫ F·(F∘θ) dμ - m². Bounded measurable functions are
integrable for the probability measure μ. This step does not use that θ is an involution.
-/
import G2Kernel.RPstep

noncomputable section
open MeasureTheory

namespace G2Kernel

theorem rpCov_thm : rpCov_statement := by
  unfold rpCov_statement
  intro Ω _ μ _ θ hθ _ A hshift hRP F hF hFm hbd
  obtain ⟨B, hB⟩ := hbd
  have hθm : Measurable θ := hθ.measurable
  have mFθ : Measurable (fun ω => F (θ ω)) := hFm.comp hθm
  have mFF : Measurable (fun ω => F ω * F (θ ω)) := hFm.mul mFθ
  have iF : Integrable F μ :=
    Integrable.mono' (integrable_const B) hFm.aestronglyMeasurable
      (ae_of_all _ fun ω => (Real.norm_eq_abs _).le.trans (hB ω))
  have iFθ : Integrable (fun ω => F (θ ω)) μ :=
    Integrable.mono' (integrable_const B) mFθ.aestronglyMeasurable
      (ae_of_all _ fun ω => (Real.norm_eq_abs _).le.trans (hB (θ ω)))
  have iFF : Integrable (fun ω => F ω * F (θ ω)) μ :=
    Integrable.mono' (integrable_const (B * B)) mFF.aestronglyMeasurable
      (ae_of_all _ fun ω => (Real.norm_eq_abs _).le.trans ((abs_mul _ _).le.trans
        (mul_le_mul (hB ω) (hB (θ ω)) (abs_nonneg _) ((abs_nonneg _).trans (hB ω)))))
  have hmθ : ∫ ω, F (θ ω) ∂μ = ∫ ω, F ω ∂μ := by
    rw [← integral_map hθm.aemeasurable hFm.aestronglyMeasurable, hθ.map_eq]
  obtain ⟨m, hm⟩ : ∃ m, ∫ ω, F ω ∂μ = m := ⟨_, rfl⟩
  have hG : 0 ≤ ∫ ω, (F ω - m) * (F (θ ω) - m) ∂μ := hRP (fun ω => F ω - m) (hshift F hF m)
  have i1 : Integrable (fun ω => F ω * F (θ ω) - m * F (θ ω)) μ := iFF.sub (iFθ.const_mul m)
  have i2 : Integrable (fun ω => F ω * F (θ ω) - m * F (θ ω) - m * F ω) μ := i1.sub (iF.const_mul m)
  have hc : ∫ _ω, m * m ∂μ = m * m := by
    rw [integral_const, probReal_univ, one_smul]
  have e : (fun ω => (F ω - m) * (F (θ ω) - m)) =
      fun ω => F ω * F (θ ω) - m * F (θ ω) - m * F ω + m * m := by
    funext ω
    ring
  have hexp : ∫ ω, (F ω - m) * (F (θ ω) - m) ∂μ = ∫ ω, F ω * F (θ ω) ∂μ - m * m := by
    rw [e, integral_add i2 (integrable_const (m * m)), hc, integral_sub i1 (iF.const_mul m),
      integral_sub iFF (iFθ.const_mul m), integral_const_mul, integral_const_mul, hmθ, hm]
    ring
  rw [hmθ, hm]
  linarith

end G2Kernel
