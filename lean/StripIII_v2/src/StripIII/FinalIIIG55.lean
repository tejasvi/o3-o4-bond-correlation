/-
StripIII.FinalIIIG55: part (f) of Theorem 6.34 over every
coupling J >= 0, closed. `stripIII_final` applies with the pairs of orbit G55 from their record, both checks by decide. The record is
the box record of run 045359Z, code/pk23/o5/records/O5_BOX_RECORD_run_20261118T045359Z_v1_1.md (sha8 5091f54c; manifest
MANIFEST_O5_BOX_RECORD_run_20261118T045359Z_v1_1.sha256 sha8 81c390ed; table O5_RECORD_TABLE_box_run_20261118T045359Z_v1.tsv sha8 a1233479).
It certifies G55 of P_3 x P_7 at N = 4 for both members, with J^2 Cov >= L > 0, i.e. Cov >= L/J^2 > 0, for every J >= J1
(J1, L, c2 and the output's sha8 in the comment line of `L55`,
made from the table by the converter record2lean_v1_1.py).
-/
import StripIII.FinalIII

noncomputable section

namespace G2Kernel

open StripIII

/-- the pairs of orbit G55 that their record certifies at N = 4, as (n, code pair) -/
def L55 : List (ℕ × ECode × ECode) := [
-- source code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T045359Z_v1.tsv sha256 a1233479612e660f697e3d0e88be0a0bb878a7421ac71a4190db1e8df5b0472b; labels n7_G55; N 4
  -- n7_G55 (2 members): N=4 J1 350 L 4.643864e-03 c2 5.786858e-03 out 54b1f9f1
  (7, .hor 0 2, .hor 2 3),
  (7, .hor 0 3, .hor 2 2)
-- total 2 pairs
]

/-- the final list passes both checks: it covers the class O5 at N = 4 (n = 6 and 7), and it lies within the class -/
theorem L55_checks : o5Check (o5List ++ L55) = true ∧ o5InClass (o5List ++ L55) = true := by decide +kernel

/-- the certified pairs are the two pairs that the n = 7 probe enumerates (StripIII.FinalIII's `trialG55`) -/
theorem L55_eq_trial : L55 = trialG55 := by decide +kernel

/-- **hO5** with its records, for the final list `o5List ++ L55` (kind: restatement; the n = 6 part, the orbits n6 G27 and G46, backed
by the box record v1_2 of run 013023Z, as in `hO5_record`; the n = 7 part, the two pairs of G55, by the G55 record of run 045359Z, as
in this module's header) -/
theorem hO5_final_record (N : ℕ) : hO5 N (o5List ++ L55) =
    (N = 4 → ∀ n : ℕ, ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair n (fun a b => (o5List ++ L55).contains (n, a, b)) e f →
      G2pair N (strip n) (uniform J) e f) := rfl

/-- **Part (f) of Theorem 6.34, final**: for N = 3 and N = 4, every n >= 1 and every J >= 0, every pair of distinct
edges of P_3 x P_n, neither a middle-row horizontal edge, has nonnegative covariance, under the named hypotheses of
`stripIII_full_statementL` with the records' lists `box5List` and `o5List ++ L55`. The records of the hypotheses: `hS9h_record`,
`hNE_record`, `hBox5_record`, `hO5_final_record`, and StripIII.Statement for the others. -/
theorem stripIII_thm (N : ℕ) : stripIII_full_statementL N box5List (o5List ++ L55) :=
  stripIII_final N L55 L55_checks.1 L55_checks.2

end G2Kernel
