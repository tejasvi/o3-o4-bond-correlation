/-
G2Kernel.Proofs.CoverProof: proof of `cover_statement` (module M9). Kernel proof, step L-b.
-/
import G2Kernel.Cover

namespace G2Kernel

theorem cover_thm : cover_statement := by
  unfold cover_statement
  refine ⟨fun J _ => ?_, fun J _ => ?_, ?_, ?_⟩
  · by_cases h1 : J ≤ 1 / 100
    · exact Or.inl h1
    · push Not at h1
      by_cases h2 : J ≤ 20
      · exact Or.inr (Or.inl ⟨by linarith, h2⟩)
      · push Not at h2
        by_cases h3 : J ≤ 10068 / 100
        · exact Or.inr (Or.inr (Or.inl ⟨h2.le, h3⟩))
        · push Not at h3
          exact Or.inr (Or.inr (Or.inr (by linarith)))
  · by_cases h1 : J ≤ 1 / 100
    · exact Or.inl h1
    · push Not at h1
      by_cases h2 : J ≤ 20
      · exact Or.inr (Or.inl ⟨by linarith, h2⟩)
      · push Not at h2
        by_cases h3 : J ≤ 10068 / 100
        · exact Or.inr (Or.inr (Or.inl ⟨h2.le, h3⟩))
        · push Not at h3
          exact Or.inr (Or.inr (Or.inr (by linarith)))
  · norm_num [stripTop]
  · norm_num [stripTop]

end G2Kernel
