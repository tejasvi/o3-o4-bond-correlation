/-
StripIII.Small5Final: the complete small-n
theorem, closed. `smallN_final` applies with the members of G05 and G33 from the kit v7b stage 2 records, both checks by decide, and all 36
orbits of P_3 x P_5 are then in the list. G05: the box record of run 154150Z,
code/pk23/o5/records/O5_BOX_RECORD_run_20261118T154150Z_v1.md (sha8 6884eada; manifest MANIFEST_O5_BOX_RECORD_run_20261118T154150Z_v1.sha256 sha8
35cb5899; table O5_RECORD_TABLE_box_run_20261118T154150Z_v1.tsv sha8 94284d6e);
G33: the box record of run 041647Z,
code/pk23/o5/records/O5_BOX_RECORD_run_20261119T041647Z_v1.md (sha8 e5e358d7; manifest MANIFEST_O5_BOX_RECORD_run_20261119T041647Z_v1.sha256 sha8
112af271; table O5_RECORD_TABLE_box_run_20261119T041647Z_v1.tsv sha8 d068beac).
Both records certify their orbit at N = 3 (J1 300) and N = 4 (J1 350), with J^2 Cov >= L > 0, i.e. Cov >= L/J^2 > 0,
for every J >= J1 (J1, L, c2 and the outputs' sha8 in the comment lines, made from the tables by the converter record2lean_v1_1.py, which
takes an orbit only if it is certified at both N with the same members).
-/
import StripIII.Small5Kit7

noncomputable section

namespace G2Kernel

open StripIII

/-- the members of G05, certified at both N by the stage 2 record of run 154150Z -/
def box5G05 : List (ECode × ECode) := [
-- source code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T154150Z_v1.tsv sha256 94284d6e2c75a8a1c8a47c4a22073184b284107f24eac6956fbe4fbee4b887c6; labels n5_G05; N 3,4
  -- n5_G05 (4 members): N=3 J1 300 L 2.560374e-06 c2 3.293797e-06 out 986c5e8d; N=4 J1 350 L 3.775544e-06 c2 4.940695e-06 out aab9c3f7
  (.hor 0 0, .hor 1 3),
  (.hor 0 3, .hor 1 0),
  (.hor 1 0, .hor 2 3),
  (.hor 1 3, .hor 2 0)
-- total 4 pairs
]

/-- the members of G33, certified at both N by the stage 2 record of run 041647Z -/
def box5G33 : List (ECode × ECode) := [
-- source code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261119T041647Z_v1.tsv sha256 d068beacbaf923c45f338718a9f2ca001bf2b63bc5fac302aef94b50c5e41d7c; labels n5_G33; N 3,4
  -- n5_G33 (4 members): N=3 J1 300 L 2.598678e-06 c2 3.293797e-06 out 8f568334; N=4 J1 350 L 3.820294e-06 c2 4.940695e-06 out c6ac8f61
  (.hor 1 0, .ver 0 4),
  (.hor 1 0, .ver 1 4),
  (.hor 1 3, .ver 0 0),
  (.hor 1 3, .ver 1 0)
-- total 4 pairs
]

/-- the stage 2 pairs -/
def box5Stage2 : List (ECode × ECode) := box5G05 ++ box5G33

/-- the final list passes both checks: it covers the class `g5`, each pair in one order or the other, and it lies within the class -/
theorem box5Stage2_checks : box5AllCheck (box5AllList34 ++ box5Stage2) = true ∧
    box5AllInClass (box5AllList34 ++ box5Stage2) = true := by decide +kernel

/-- the certified members of G05 and G33 are the candidates of StripIII.Small5Kit7 (`candG05G33`) -/
theorem box5Stage2_eq_cand : box5Stage2 = candG05G33 := by decide +kernel

/-- the final list holds 138 ordered pairs, one for each unordered pair of the class (`count_g5`: 2 x 138 ordered pairs) -/
theorem box5Final_len : (box5AllList34 ++ box5Stage2).length = 138 := by decide +kernel

/-- **hBoxAll5** with its records, for the final list `box5AllList34 ++ box5Stage2` (kind: restatement; the 27 orbits of `box5AllList`
and the 7 of `box5Kit7S1` backed as in StripIII.Small5Kit7's `hBoxAll5_record`; G05 and G33 by the stage 2 records, as in this
module's header) -/
theorem hBoxAll5_final_record (N : ℕ) : hBoxAll5 N (box5AllList34 ++ box5Stage2) =
    (∀ J : ℝ, jLow N ≤ J → ∀ e ∈ (strip 5).edgeSet, ∀ f ∈ (strip 5).edgeSet, e ≠ f →
      (box5AllList34 ++ box5Stage2).contains (edgeCode e, edgeCode f) = true → G2pair N (strip 5) (uniform J) e f) := rfl

/-- **The complete small-n theorem, final**: for N = 3 and N = 4, every n with 1 <= n <= 5 and every J >= 0, every pair of distinct
edges of P_3 x P_n, middle-row edges included, has nonnegative covariance, under the named hypotheses of `smallN_statementL` with the
records' list `box5AllList34 ++ box5Stage2`. The records of the hypotheses: `hBoxAll5_final_record`, and StripIII.Statement and
StripIII.Small5Statement for the others. -/
theorem smallN_thm (N : ℕ) : smallN_statementL N (box5AllList34 ++ box5Stage2) :=
  smallN_final N box5Stage2 box5Stage2_checks.1 box5Stage2_checks.2

end G2Kernel
