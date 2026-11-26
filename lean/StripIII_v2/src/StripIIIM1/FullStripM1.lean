/-
StripIIIM1.FullStripM1: M1's interim theorem,
closed: `fullStripM1_of_parts` with the final theorem `stripIII_thm` of Theorem 6.34 (f) (lists box5List and o5List ++ L55), the final
small-n theorem `smallN_thm` (list box5AllList34 ++ box5Stage2) and the checks of M1's list `m1List` (StripIIIM1.HCheckM1's
`m1Check_all`), for nmax = NMAX_M1.
-/
import StripIIIM1.HProof
import StripIIIM1.HCheckM1
import StripIII.FinalIIIG55
import StripIII.Small5Final

noncomputable section

namespace G2Kernel

open StripIII

/-- **hM1** with its record, for the list `m1List` and nmax = NMAX_M1 (kind: restatement; the record as in StripIIIM1.HStatement's
`hM1` and StripIIIM1.M1List's header) -/
theorem hM1_record (N : ℕ) : hM1 N m1List NMAX_M1 =
    (∀ J : ℝ, jLow N ≤ J → ∀ n : ℕ, 6 ≤ n → n ≤ NMAX_M1 →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f →
        (m1Keys m1List n).contains (canonKey n (edgeCode e) (edgeCode f)) = true → G2pair N (strip n) (uniform J) e f) := rfl

/-- **M1's interim theorem, final**: for N = 3 and N = 4, every n with 1 <= n <= NMAX_M1 and every J >= 0, every pair of distinct
edges of P_3 x P_n, middle-row edges included, has nonnegative covariance, under the named hypotheses of `fullStripM1_statementL`
with the records' lists `box5List`, `o5List ++ L55`, `box5AllList34 ++ box5Stage2` and `m1List`. The records of the hypotheses:
`hM1_record`, StripIII.FinalIIIG55's and StripIII.Small5Final's, and StripIII.Statement and StripIII.Small5Statement for the others. -/
theorem fullStripM1_thm (N : ℕ) :
    fullStripM1_statementL N box5List (o5List ++ L55) (box5AllList34 ++ box5Stage2) m1List NMAX_M1 :=
  fullStripM1_of_parts N _ _ _ _ _ (stripIII_thm N) (smallN_thm N) m1Check_all

end G2Kernel
