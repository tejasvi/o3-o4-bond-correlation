/-
G2Kernel.Cycle (module M3): Theorem 1.1 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344) on a single cycle, every N ≥ 2,
all couplings J ≥ 0, with the strict form. The cactus form, with the block decomposition, is in Cactus.lean
(module M3c).
Skeleton (step L-a). Not compiled yet.
-/
import G2Kernel.Named
import G2Kernel.LabelCov

namespace G2Kernel

/-- Statement M3 (Theorem 1.1 on one cycle): uses hFH, hKReg, hRatio, hCycleZ. -/
def cycleG2_statement (N : ℕ) : Prop :=
  ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d →
    ∀ (n : ℕ) [DecidableRel (SimpleGraph.cycleGraph n).Adj], 3 ≤ n → ∀ J : Sym2 (Fin n) → ℝ,
      Ferro (SimpleGraph.cycleGraph n) J →
      ∀ e ∈ (SimpleGraph.cycleGraph n).edgeSet, ∀ f ∈ (SimpleGraph.cycleGraph n).edgeSet, e ≠ f →
        G2pair N (SimpleGraph.cycleGraph n) J e f

/-- Statement M3' (Theorem 1.1, strict part): if all couplings of the cycle are positive, the covariance
of two distinct edges is positive. -/
def cycleG2_strict_statement (N : ℕ) : Prop :=
  ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d →
    (∀ c, 0 < d c) →
    ∀ (n : ℕ) [DecidableRel (SimpleGraph.cycleGraph n).Adj], 3 ≤ n → ∀ J : Sym2 (Fin n) → ℝ,
      (∀ e ∈ (SimpleGraph.cycleGraph n).edgeSet, 0 < J e) →
      ∀ e ∈ (SimpleGraph.cycleGraph n).edgeSet, ∀ f ∈ (SimpleGraph.cycleGraph n).edgeSet, e ≠ f →
        0 < gibbsCov N (SimpleGraph.cycleGraph n) J (bond e) (bond f)

end G2Kernel
