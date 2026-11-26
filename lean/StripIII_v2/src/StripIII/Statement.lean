/-
StripIII.Statement: the statement of the large-J part of part (f) of Theorem 6.34 of the paper "Positive correlation of bond
energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344), for the pairs of edges without a middle-row horizontal edge, at J >= 300 (N = 3) and J >= 350
(N = 4), for every n >= 1, with one named hypothesis per route:
- hShared (Named.lean, Theorem 3.2): S0, the pairs with a common vertex;
- hStripMirror: S0, the mirror pairs (Lemma 6.1 with the reflection in the middle row and with the reflection in the vertical
  midline);
- hVertSV: Theorem 6.21 (†), the pairs of vertical edges for n >= 2 and J >= 300;
- hD4: Theorem 6.34, parts (a), (c) and (d), every pair for n <= 4;
- hNE: the separated pairs near the ends, n >= 5 (NE's certified RC record v1_5);
- hBox5 L5: the joint pairs of n = 5 outside S0, over the list L5 of the box records (orbits n5 G12, G13, G26, G27, G06, G21);
- hS9h: S9(h) of record A (code/pk21/p2/a/S_TB_PRIME_RECORD_v1.md) with its joint kind, n >= 6;
- hS9i: Proposition B.1 (†), n >= 6;
- hO5 L6: the pairs of the rows that Proposition B.1 excludes at N = 4, over the list L6 of the box runs (n6 G27, n6 G46,
  n7 G55).
The classes are the predicates of StripIII.Core on edge codes. `stripIII_full_statementL` covers every J >= 0 at both N: J <= 300 by
strip300_statement's hypotheses (Strip300.lean), the window 300 < J < 350 at N = 4 by hRHCover350 (Theorem 6.19 on [300, 350],
route H's further ru2 run) with hShared and hD4, and J >= jLow N by the routes above.
The Mathlib-importing modules compile within a 32 GiB address space, on one thread.
-/
import G2Kernel.Strip300
import StripIII.Core

noncomputable section

namespace G2Kernel

open StripIII (ECode)

/-- The code of an edge of `P_3 × P_n`: a horizontal edge by its row and its left column, a vertical edge by its upper row and its
column. Defined on all of `Sym2`; on the edges of `strip n` it takes valid values and is injective (StripIII.Proof). -/
def edgeCode {n : ℕ} : Sym2 (Fin 3 × Fin n) → ECode :=
  Sym2.lift ⟨fun p q => if p.1 = q.1 then ECode.hor p.1.val (min p.2.val q.2.val)
      else ECode.ver (min p.1.val q.1.val) (min p.2.val q.2.val),
    fun p q => by
      dsimp only
      by_cases h : p.1 = q.1
      · rw [ite_eq_left h, ite_eq_left h.symm, h, Nat.min_comm]
      · rw [ite_eq_right h, ite_eq_right (Ne.symm h), Nat.min_comm p.1.val, Nat.min_comm p.2.val]⟩

/-- the middle-row horizontal edges h_i -/
def midRowEdge (n : ℕ) (e : Sym2 (Fin 3 × Fin n)) : Prop :=
  ∃ i j : Fin n, i.val + 1 = j.val ∧ e = s(((1 : Fin 3), i), ((1 : Fin 3), j))

/-- the vertical edges a_j and b_j -/
def verticalEdge (n : ℕ) (e : Sym2 (Fin 3 × Fin n)) : Prop := ∃ j : Fin n, e = vUp j ∨ e = vDown j

/-- the reflection of `P_3 × P_n` in the vertical midline: column c to n - 1 - c -/
def stripReflV {n : ℕ} (p : Fin 3 × Fin n) : Fin 3 × Fin n := (p.1, p.2.rev)

/-- the lower end of the coupling range: 300 at N = 3, 350 at N = 4 -/
def jLow (N : ℕ) : ℝ := if N = 4 then 350 else 300

/-- the pairs (e, f) of distinct edges of `P_3 × P_n`, neither a middle-row horizontal edge, whose codes satisfy `c` -/
def codePair (n : ℕ) (c : ECode → ECode → Bool) (e f : Sym2 (Fin 3 × Fin n)) : Prop :=
  e ∈ (strip n).edgeSet ∧ f ∈ (strip n).edgeSet ∧ e ≠ f ∧ ¬ midRowEdge n e ∧ ¬ midRowEdge n f ∧
    c (edgeCode e) (edgeCode f) = true

/-- **hStripMirror** (S0's mirror pairs, the paper's paragraph S0; kind: restatement, backed by Lemma 6.1 with the reflection in the
middle row and with the reflection in the vertical midline, paper proofs; not formalized): for n >= 1 and J >= 0, the mirror pairs
(t_i, bb_i) and the left-right mirror pairs (e, θ(e)) have nonnegative covariance. -/
def hStripMirror (N : ℕ) : Prop :=
  ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
    (∀ i j : Fin n, i.val + 1 = j.val →
      G2pair N (strip n) (uniform J) s(((0 : Fin 3), i), ((0 : Fin 3), j)) s(((2 : Fin 3), i), ((2 : Fin 3), j))) ∧
    (∀ e ∈ (strip n).edgeSet, G2pair N (strip n) (uniform J) e (Sym2.map stripReflV e))

/-- **hVertSV** (Theorem 6.21, †; kind: restatement, backed by S0, S7 and S8 with the inputs S1-S6, and at N = 4 and
300 <= J <= 350 by Corollary 6.20 in place of S8): for n >= 2 and J >= 300, every pair of distinct vertical edges of
P_3 x P_n has nonnegative covariance. -/
def hVertSV (N : ℕ) : Prop :=
  ∀ n : ℕ, 2 ≤ n → ∀ J : ℝ, 300 ≤ J →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → verticalEdge n e → verticalEdge n f →
      G2pair N (strip n) (uniform J) e f

/-- **hD4** (Theorem 6.34, parts (a), (c) and (d); kind: restatement, backed by paper proofs, Theorem 6.34 (d) with the certified
Proposition 6.36): for n <= 4 and every J >= 0, every pair of distinct edges of P_3 x P_n has nonnegative covariance. -/
def hD4 (N : ℕ) : Prop :=
  ∀ n : ℕ, 1 ≤ n → n ≤ 4 → ∀ J : ℝ, 0 ≤ J →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

/-- **hNE** (kind: restatement, backed by NE's certified RC record code/pk22/w1/rc_cert/out/ne_rc_record_cert_kt_s8h_rcc_v1_5.kv (sha8 8ff64462);
the record's class keys cover `StripIII.cNE`, StripIII.NECheck): for n >= 5 and J >= jLow N, every pair outside S0 that is separated (k >= 0), not of two vertical edges, and
has an edge with a vertex in an end column or an end exponent below the S9(h) threshold of its kind (`StripIII.cNE`) has
nonnegative covariance. -/
def hNE (N : ℕ) : Prop :=
  ∀ n : ℕ, 5 ≤ n → ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair n (StripIII.cNE N n) e f → G2pair N (strip n) (uniform J) e f

/-- **hBox5** (kind: restatement, backed by the box record for the orbits n5 G12, G13, G26, G27, G06, G21 at N = 3 and N = 4,
code/pk23/o5/records/O5_BOX_RECORD_run_20261118T013023Z_v1_2.md (sha8 3abdb733; table O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv
sha8 19945efd; manifest MANIFEST_O5_BOX_RECORD_run_20261118T013023Z_v1_2.sha256
sha8 ff08d9ce);
the list `L` holds their pairs as code pairs, `StripIII.box5List`): for J >= jLow N, every pair of P_3 x P_5 whose code pair is in `L` has
nonnegative covariance. -/
def hBox5 (N : ℕ) (L : List (ECode × ECode)) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair 5 (fun a b => L.contains (a, b)) e f → G2pair N (strip 5) (uniform J) e f

/-- **hS9h** (kind: restatement, backed by record A, code/pk21/p2/a/S_TB_PRIME_RECORD_v1.md (sha8 772b9968; manifest sha8 39e85db3):
S9(h) with its three separated kinds and its joint kind (sect. 9,
R5; the thresholds of `StripIII.Shape.thrH`)):
for n >= 6 and J >= jLow N, every pair outside S0, not of two vertical edges, with no vertex in an end column and both end exponents
at least the threshold of its kind (`StripIII.cH9`) has nonnegative covariance. -/
def hS9h (N : ℕ) : Prop :=
  ∀ n : ℕ, 6 ≤ n → ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair n (StripIII.cH9 N n) e f → G2pair N (strip n) (uniform J) e f

/-- **hS9i** (Proposition B.1, †; kind: restatement, backed by its certified record): for n >= 6 and J >= jLow N, every
overlapping pair outside S0 with an edge with a vertex in an end column or min(d_L, d_R) below the joint threshold, other than the
rows excluded at N = 4 (`StripIII.cI9`), has nonnegative covariance (the proposition gives Cov > 0). -/
def hS9i (N : ℕ) : Prop :=
  ∀ n : ℕ, 6 ≤ n → ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair n (StripIII.cI9 N n) e f → G2pair N (strip n) (uniform J) e f

/-- **hO5** (kind: restatement, backed by the box runs n6 G27, n6 G46 and n7 G55, which exist at N = 4 only; the list `L` holds
their pairs as (n, code pair), `StripIII.o5List` with the pairs of G55 added in StripIII.FinalIIIG55; n = 6: code/pk23/o5/records/O5_BOX_RECORD_run_20261118T013023Z_v1_2.md (sha8 3abdb733; table O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv
sha8 19945efd; manifest MANIFEST_O5_BOX_RECORD_run_20261118T013023Z_v1_2.sha256
sha8 ff08d9ce);
G55: code/pk23/o5/records/O5_BOX_RECORD_run_20261118T045359Z_v1_1.md (sha8 5091f54c)): at N = 4, for J >= jLow N, every pair of P_3 x P_n whose (n, code pair) is in `L`
has nonnegative covariance (the N = 4 condition: at N = 3 the class O5 is empty, `StripIII.isO5_n3`). -/
def hO5 (N : ℕ) (L : List (ℕ × ECode × ECode)) : Prop :=
  N = 4 → ∀ n : ℕ, ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair n (fun a b => L.contains (n, a, b)) e f → G2pair N (strip n) (uniform J) e f

/-- **Part (f) of Theorem 6.34 for large J**, with the lists of the box records as parameters: for N = 3 and N = 4, every n >= 1 and J >= jLow N, every
pair of distinct edges of P_3 x P_n, neither a middle-row horizontal edge, has nonnegative covariance. -/
def stripIII_statementL (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) : Prop :=
  (N = 3 ∨ N = 4) → hShared N → hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, jLow N ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f

/-- **Part (f) of Theorem 6.34 for large J** with Core's lists alone: an interim form, not proved in this tree (`o5List` lacks the pairs of G55); the closed form is StripIII.FinalIIIG55's `stripIII_thm`. -/
def stripIII_statement (N : ℕ) : Prop := stripIII_statementL N StripIII.box5List StripIII.o5List

/-- **hRHCover350** (Theorem 6.19 of the paper at N = 4 on [300, 350], †; kind: restatement, backed by route H's further
ru2 run code/pk08/out/ru2_x2.out (sha8 6ac2e171; its record records/route_H/union_300_350.out; job manifest
code/pk08/MANIFEST_ru2_x2_jobs.sha256 sha8 f240c3aa): VALID True, VERDICT N=4 [300, 350]: COVERED, engine code/pk05/cs33h_1_rh_cert.py
(sha8 50b74eed); and the paper's proof
of Theorem 6.19. As for hRHCover, the
exterior-power form, the near and far checks and the certified spectral data are not formalized): at N = 4, for 300 <= J <= 350 and
n >= 4, every pair of distinct edges of P_3 x P_n other than the two vertical edges of one column has positive covariance. -/
def hRHCover350 (N : ℕ) : Prop :=
  N = 4 → ∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 300 ≤ J → J ≤ 350 →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
      0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)

/-- **Part (f) of Theorem 6.34 over every coupling J >= 0**, with the lists of the box records as parameters: for N = 3 and N = 4, every n >= 1
and every J >= 0, every pair of distinct edges of P_3 x P_n, neither a middle-row horizontal edge, has nonnegative covariance. It uses
strip300_statement's hypotheses for J <= 300, hRHCover350 with hShared and hD4 for the window 300 < J < 350 at N = 4, and the hypotheses
of `stripIII_statementL` for J >= jLow N. -/
def stripIII_full_statementL (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f

/-- **Part (f) of Theorem 6.34 over every coupling J >= 0** with Core's lists alone: an interim form, not proved in this tree (`o5List` lacks the pairs of G55); the closed form is StripIII.FinalIIIG55's `stripIII_thm`. -/
def stripIII_full_statement (N : ℕ) : Prop := stripIII_full_statementL N StripIII.box5List StripIII.o5List

end G2Kernel
