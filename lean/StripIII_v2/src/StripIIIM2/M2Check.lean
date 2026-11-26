/-
StripIIIM2.M2Check: the checks of M2's
parameters and control list by decide. `m2Rows_class`: every finite row of M2's record has the class (d + 1, m, d' + 1) that `classOf`
computes from its codes, in both orders. `m2Rows_todo`: every row is a to-do pair outside the end orbit. `M2_params`: 2 D0 + M0 + 2 <= 12,
so the covering holds at every n >= 12, and n0 = 2 D0 + M0 + 1 <= NMAX_M1, so the classes with n <= n0 are M1's (Proposition B.22). `M2_nmin`:
12 <= NMAX_M1 + 1, so M1's and M2's ranges meet. `tail_from_n6`: with the record's (D0, M0), no to-do pair outside the end orbit has a
tail class at n <= 5, so hM2tail claims nothing below Proposition B.24's n >= 6. No Mathlib.
-/
import StripIIIM2.M2List
import StripIIIM1.M1List

namespace G2Kernel.StripIII

theorem m2Rows_class : m2Rows.all (fun q => classOf q.1 q.2.1 q.2.2.1 == q.2.2.2 && classOf q.1 q.2.2.1 q.2.1 == q.2.2.2) = true := by
  decide +kernel

theorem m2Rows_todo : m2Rows.all (fun q => todoH q.1 q.2.1 q.2.2.1 && !sameBondEnd q.1 q.2.1 q.2.2.1) = true := by
  decide +kernel

theorem M2_params : 2 * D0_M2 + M0_M2 + 2 ≤ 12 ∧ 2 * D0_M2 + M0_M2 + 1 ≤ NMAX_M1 := by decide

theorem M2_nmin : 12 ≤ NMAX_M1 + 1 := by decide

/-- with the record's (D0, M0), no to-do pair outside the end orbit has a tail class at n <= 5 (at n >= 6 the claim is Proposition B.24's) -/
theorem tail_from_n6 : [1, 2, 3, 4, 5].all (fun n => (allPairsAll n).all fun p =>
    !(todoH n p.1 p.2 && !sameBondEnd n p.1 p.2) || !tailClass D0_M2 M0_M2 (classOf n p.1 p.2)) = true := by
  decide +kernel

end G2Kernel.StripIII
