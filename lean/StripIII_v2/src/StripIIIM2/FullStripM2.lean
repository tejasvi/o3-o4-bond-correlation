/-
StripIIIM2.FullStripM2: M2's theorem and the
strip theorem for every n, closed. `fullStripM2_thm`: `fullStripM2_of_parts` with the final theorem `stripIII_thm` of Theorem 6.34 (f) (lists
box5List and o5List ++ L55), the tail's (D0, M0) from M2's record and nmin = 12 (`M2_params`: 2 D0 + M0 + 2 <= 12). `fullStrip_thm`:
`fullStrip_of_parts` with M1's final theorem `fullStripM1_thm` (n <= NMAX_M1) and `fullStripM2_thm` (`M2_nmin`: 12 <= NMAX_M1 + 1).
The record above is M2's certified record (Proposition B.24).
-/
import StripIIIM2.M2Proof
import StripIIIM2.M2Check
import StripIIIM1.FullStripM1

noncomputable section

namespace G2Kernel

open StripIII

/-- **hM2tail** with its record, for (D0, M0) = (D0_M2, M0_M2) (kind: restatement; the record as in StripIIIM2.M2Statement's `hM2tail`
and StripIIIM2.M2List's header) -/
theorem hM2tail_record (N : ℕ) : hM2tail N D0_M2 M0_M2 =
    (∀ J : ℝ, jLow N ≤ J → ∀ n : ℕ, ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet,
      todoH n (edgeCode e) (edgeCode f) = true → sameBondEnd n (edgeCode e) (edgeCode f) = false →
      tailClass D0_M2 M0_M2 (classOf n (edgeCode e) (edgeCode f)) = true → G2pair N (strip n) (uniform J) e f) := rfl

/-- **M2's theorem, final**: for N = 3 and N = 4, every n >= 12 and every J >= 0, every pair of distinct edges of P_3 x P_n, middle-row
edges included, has nonnegative covariance, under the named hypotheses of `fullStripM2_statementL` with the records' lists `box5List`
and `o5List ++ L55` and M2's tail (D0_M2, M0_M2). -/
theorem fullStripM2_thm (N : ℕ) : fullStripM2_statementL N box5List (o5List ++ L55) D0_M2 M0_M2 12 :=
  fullStripM2_of_parts N _ _ _ _ _ (stripIII_thm N) M2_params.1 (by norm_num)

/-- **The strip theorem for every n, final**, Theorem 1.4 (i): for N = 3 and N = 4, every n >= 1 and every J >= 0, every pair of distinct edges of
P_3 x P_n, middle-row edges included, has nonnegative covariance, under the named hypotheses of `fullStrip_statementL` with the records'
lists `box5List`, `o5List ++ L55`, `box5AllList34 ++ box5Stage2` and `m1List`, M1's NMAX_M1 and M2's tail (D0_M2, M0_M2). The records of
the hypotheses: `hM2tail_record`, StripIIIM1.FullStripM1's `hM1_record`, and those of Theorem 6.34 (f) and of the small-n theorem. -/
theorem fullStrip_thm (N : ℕ) :
    fullStrip_statementL N box5List (o5List ++ L55) (box5AllList34 ++ box5Stage2) m1List NMAX_M1 D0_M2 M0_M2 :=
  fullStrip_of_parts N _ _ _ _ _ _ _ _ (fullStripM1_thm N) (fullStripM2_thm N) M2_nmin

end G2Kernel
