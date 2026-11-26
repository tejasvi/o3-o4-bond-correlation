/-
G2Kernel.Cover (module M9): the joins of the coupling ranges in the proofs of Theorems 6.34(a) and 1.4(ii)
(with Theorems 6.5, 6.6 and 6.9 and Lemma 6.10) of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344).
Skeleton (step L-a). Not compiled yet.
-/
import G2Kernel.Named

namespace G2Kernel

/-- Statement M9: every `J > 0` lies in one of the certified ranges, at `N = 3` (large-coupling threshold
`80`) and at `N = 4` (threshold `100`); and both strip tops exceed `20`. -/
def cover_statement : Prop :=
  (∀ J : ℝ, 0 < J →
     J ≤ 1 / 100 ∨ (99 / 10000 ≤ J ∧ J ≤ 20) ∨ (20 ≤ J ∧ J ≤ 10068 / 100) ∨ 80 ≤ J) ∧
  (∀ J : ℝ, 0 < J →
     J ≤ 1 / 100 ∨ (99 / 10000 ≤ J ∧ J ≤ 20) ∨ (20 ≤ J ∧ J ≤ 10068 / 100) ∨ 100 ≤ J) ∧
  (20 ≤ stripTop 3 ∧ 20 ≤ stripTop 4)

end G2Kernel
