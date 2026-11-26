/-
StripIII.Small5Statement:
the statement of the complete small-n theorem of P_3 x P_n: for N = 3 and N = 4, every n with 1 <= n <= 5 and every J >= 0,
every pair of distinct edges, middle-row edges included, has nonnegative covariance. It takes the hypotheses of StripIII.Statement's
`stripIII_full_statementL` without hNE, hBox5, hS9h, hS9i and hO5, and one new hypothesis, hBoxAll5, over the list of the
n = 5 box records:
- J <= 300: strip300_statement's hypotheses (Strip300.lean);
- N = 4 and 300 < J < 350: hD4 for n <= 4; at n = 5, hShared for the two vertical edges of one column and hRHCover350 (Theorem
  6.19 on [300, 350], with the scope that StripIII.Statement states) for the other pairs;
- J >= jLow N: hD4 for n <= 4; at n = 5, hShared for the pairs with a common vertex, hStripMirror for the mirror pairs, hVertSV for
  the pairs of vertical edges, and hBoxAll5 for every other pair, the class `StripIII.g5` of the 36 orbits of the whole-graph
  box runs (138 unordered pairs).
This module adds definitions only.
-/
import StripIII.Statement
import StripIII.Small5Core

noncomputable section

namespace G2Kernel

open StripIII (ECode)

/-- **hBoxAll5** (kind: restatement, backed by the box records for the 36 orbits of P_3 x P_5 at N = 3 (J1 300) and N = 4
(J1 350): the 27 orbits certified at both N in
code/pk23/o5/records/O5_BOX_RECORD_run_20261118T013023Z_v1_2.md (sha8 3abdb733; table O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv
sha8 19945efd; manifest MANIFEST_O5_BOX_RECORD_run_20261118T013023Z_v1_2.sha256 sha8 ff08d9ce);
the 7 orbits G04, G08, G11, G16, G20, G32, G36 in code/pk23/o5/records/O5_BOX_RECORD_run_20261118T114847Z_v1_1.md (sha8 451b2115), G05 in
code/pk23/o5/records/O5_BOX_RECORD_run_20261118T154150Z_v1.md (sha8 6884eada) and G33 in code/pk23/o5/records/O5_BOX_RECORD_run_20261119T041647Z_v1.md (sha8 e5e358d7); the list
`L` holds their pairs as code pairs (the final list is StripIII.Small5Final's): for J >= jLow N, every pair of distinct edges of P_3 x P_5, middle-row
edges included, whose code pair is in `L` has nonnegative covariance (the records give J^2 Cov >= L > 0, i.e. Cov >= L/J^2 > 0). The records certify each orbit at its representative pair; the bound extends to every pair of the orbit, the images of the representative under the reflections of P_3 x P_5 in the middle row and in the vertical midline, by the invariance of the Gibbs measure at uniform coupling under these two graph automorphisms (the orbit step, used here but not formalized in Lean; see STATEMENTS.md). -/
def hBoxAll5 (N : ℕ) (L : List (ECode × ECode)) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ e ∈ (strip 5).edgeSet, ∀ f ∈ (strip 5).edgeSet, e ≠ f →
    L.contains (edgeCode e, edgeCode f) = true → G2pair N (strip 5) (uniform J) e f

/-- **The complete small-n theorem**, with the list of the n = 5 box records as a parameter: for N = 3 and N = 4, every n with
1 <= n <= 5 and every J >= 0, every pair of distinct edges of P_3 x P_n, middle-row edges included, has nonnegative covariance. -/
def smallN_statementL (N : ℕ) (L : List (ECode × ECode)) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hBoxAll5 N L →
    ∀ n : ℕ, 1 ≤ n → n ≤ 5 → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

/-- **The complete small-n theorem** with the first records' list (27 of the 36 orbits; the closed form is StripIII.Small5Final's `smallN_thm`). -/
def smallN_statement (N : ℕ) : Prop := smallN_statementL N StripIII.box5AllList

end G2Kernel
