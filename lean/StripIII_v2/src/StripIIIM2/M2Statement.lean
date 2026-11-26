/-
StripIIIM2.M2Statement: the statements of
M2's theorem and of the strip theorem for every n. Nonstrict, as every statement here.
- hM2tail N D0 M0: the tail classes of Proposition B.24, at every n.
- fullStripM2_statementL: for N = 3 and N = 4, every n >= nmin, every J >= 0 and every pair of distinct edges of P_3 x P_n, middle-row
  edges included, nonnegative covariance, under the hypotheses of Theorem 6.34 (f) (StripIII.Statement's stripIII_full_statementL) and
  hM2tail.
- fullStrip_statementL, Theorem 1.4 (i): the same for every n >= 1, under the hypotheses of M1's interim theorem
  (StripIIIM1.HStatement's fullStripM1_statementL) and hM2tail.
The modules of Theorem 6.34 (f), of the small-n theorem and of M1 stay unchanged; this module adds definitions only.
-/
import StripIIIM1.HStatement
import StripIIIM2.M2Core

noncomputable section

namespace G2Kernel

open StripIII (ECode)

/-- **hM2tail** (kind: restatement, backed by Proposition B.24, checks (2)-(5) of its proof, through M2's certified assembly record
code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv (sha8 2964b12e) and its tail record code/pk24/mr_engine/MR_ASSEMBLY_cert_m2_m2cert_1_2_5.kv.tail (sha8 0a84c0b4;
manifest code/pk24/mr_engine/MANIFEST_CERT_M2_1.sha256, sha8 fe528bb4), the output of the engine
code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (sha8 28a340e7) in CERTIFIED mode, XMODE factored, with TAIL = D0 M0 n0 and TAIL_VERDICT PASS on every piece of
J >= jLow N at N = 3 and N = 4: the sign condition; Lemma B.23 (a)'s envelope classes (an end at d >= D0) with positive margins;
Lemma B.23 (b)'s inequality at M0 (every m >= M0); and Proposition B.18's envelope orbits (an interior same-bond orbit with an end at
d >= D0). The record gives J^2 Cov > 0 with a certified L > 0 on these classes. The class of a pair is
`StripIII.classOf` (StripIIIM2.M2Core), equal to the record's d, m, dp on its finite rows (StripIIIM2.M2Check); a class is an orbit of
the reflections in the middle row and in the vertical midline, which preserve the Gibbs measure at uniform coupling (not formalized), as
for hM1 and hBoxAll5): for J >= jLow N and every n, every pair of edges of P_3 x P_n that is a to-do pair outside the end orbit and whose
class has d >= D0, d' >= D0 or m >= M0 has nonnegative covariance. With the record's (D0, M0) = (2, 5), such pairs exist only at
n >= 6 (StripIIIM2.M2Check's `tail_from_n6`, by decide for n <= 5), so the claim is no wider than Proposition B.24's n >= 6. -/
def hM2tail (N : ℕ) (D0 M0 : ℕ) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ n : ℕ, ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet,
    StripIII.todoH n (edgeCode e) (edgeCode f) = true → StripIII.sameBondEnd n (edgeCode e) (edgeCode f) = false →
    StripIII.tailClass D0 M0 (StripIII.classOf n (edgeCode e) (edgeCode f)) = true →
      G2pair N (strip n) (uniform J) e f

/-- **M2's theorem**, with the lists of the box records of Theorem 6.34 (f) as parameters, the tail's (D0, M0) and the least n `nmin`: for
N = 3 and N = 4, every n >= nmin and every J >= 0, every pair of distinct edges of P_3 x P_n, middle-row edges included, has nonnegative
covariance. -/
def fullStripM2_statementL (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) (D0 M0 nmin : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hM2tail N D0 M0 →
    ∀ n : ℕ, nmin ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

/-- **The strip theorem for every n**, Theorem 1.4 (i), with the records' lists as parameters (L5, L6: the box records of Theorem 6.34 (f); L2: the n = 5 box
records; L: M1's assembly record), M1's largest n `nmax` and M2's (D0, M0): for N = 3 and N = 4, every n >= 1 and every J >= 0, every
pair of distinct edges of P_3 x P_n, middle-row edges included, has nonnegative covariance. -/
def fullStrip_statementL (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) (L2 : List (ECode × ECode))
    (L : List (ℕ × ECode × ECode)) (nmax D0 M0 : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hBoxAll5 N L2 → hM1 N L nmax →
  hM2tail N D0 M0 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

end G2Kernel
