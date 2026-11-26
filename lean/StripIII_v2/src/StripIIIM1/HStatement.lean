/-
StripIIIM1.HStatement: the statement of
M1's interim theorem: for N = 3 and N = 4, every n with 1 <= n <= NMAX_M1 and every J >= 0, every pair of distinct edges of P_3 x P_n,
middle-row edges included, has nonnegative covariance. Nonstrict, as every statement here (the end orbit (h_1, t_1)
gives only Cov >= 0). It takes the hypotheses of StripIII.Statement's `stripIII_full_statementL` (the pairs without a middle-row
horizontal edge), StripIII.Small5Statement's hBoxAll5 (n = 5), and one new hypothesis, hM1, over the list of M1's assembly record:
- n <= 5: the hypotheses of the complete small-n theorem;
- n >= 6, no middle-row horizontal edge: the hypotheses of Theorem 6.34 (f);
- n >= 6 with a middle-row horizontal edge: J <= 300 by strip300_statement's hypotheses; N = 4 and 300 < J < 350 by hShared (the two
  vertical edges of one column) and hRHCover350 (the other pairs); J >= jLow N by hShared (a common vertex), hStripMirror (a left-right
  mirror pair), G2Kernel_Lb_p13's corner identity with hShared (the end orbit, no record), and hM1 (every other pair: the to-do pairs of Appendix B).
The modules of Theorem 6.34 (f) and of the small-n theorem stay unchanged; this module adds definitions only.
-/
import StripIII.Small5Statement
import StripIIIM1.HCore

noncomputable section

namespace G2Kernel

open StripIII (ECode)

/-- **hM1** (kind: restatement, backed by M1's certified assembly record code/pk24/mr_engine/MR_ASSEMBLY_cert_m1_v4b_1_n11.kv (sha8 e5d78802; manifest
code/pk24/mr_engine/MANIFEST_CERT_M1_V4B_1.sha256, sha8 3cc9dd95), the output of the engine code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py
(sha8 28a340e7) in CERTIFIED mode on the MR_INPUT_KV_v4 records pinned by its INPUT_PINS line (Appendix B): one row per class
of the to-do pairs outside the end orbit at 6 <= n <= NMAX, each PASS at N = 3 and N = 4 on every piece of J >= jLow N (J^2 Cov > 0 with
a certified L > 0, Proposition B.22), by Proposition B.17 for its chan-exact and chan-crude rows and Proposition B.18 for its same-bond
rows. The list `L` holds one entry (n, e, f) per row, the row's representative as a code pair (`StripIII.m1List`, made from the record
by the converter mrasm2lean_v1_1.py). The other members of a class are the images of its representative under the reflections in the
middle row and in the vertical midline, which preserve the Gibbs measure at uniform coupling (not formalized); a pair lies in the class
of an entry exactly when it has the entry's key (`StripIII.canonKey`, StripIIIM1.HCore; for M1's list by decide, StripIIIM1.HCheckM1's
`m1Orbit_n6`..`m1Orbit_n11` with HCore's `canonKey_invariant`)): for J >= jLow N and 6 <= n <= nmax, every pair of distinct edges of
P_3 x P_n whose key is the key of an entry of `L` at n has nonnegative covariance. -/
def hM1 (N : ℕ) (L : List (ℕ × ECode × ECode)) (nmax : ℕ) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ n : ℕ, 6 ≤ n → n ≤ nmax →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f →
      (StripIII.m1Keys L n).contains (StripIII.canonKey n (edgeCode e) (edgeCode f)) = true →
        G2pair N (strip n) (uniform J) e f

/-- **M1's interim theorem**, with the records' lists as parameters (L5, L6: the box records of Theorem 6.34 (f); L2: the n = 5 box records;
L: M1's assembly record) and the largest n as the parameter `nmax`: for N = 3 and N = 4, every n with 1 <= n <= nmax and every J >= 0,
every pair of distinct edges of P_3 x P_n, middle-row edges included, has nonnegative covariance. -/
def fullStripM1_statementL (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) (L2 : List (ECode × ECode))
    (L : List (ℕ × ECode × ECode)) (nmax : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hBoxAll5 N L2 → hM1 N L nmax →
    ∀ n : ℕ, 1 ≤ n → n ≤ nmax → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

end G2Kernel
