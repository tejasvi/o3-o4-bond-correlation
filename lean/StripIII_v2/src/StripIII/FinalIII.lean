/-
StripIII.FinalIII: the final form of
part (f) of Theorem 6.34 over every coupling J >= 0, `stripIII_full_of_lists` with the records' final lists passed as parameters, and the records
behind its hypotheses. Core, Statement and Proof cite the same records; in the release copy their comments were updated by a recorded
transformation of comments only (CHANGES_StripIII_v2.md). The hypotheses of
`stripIII_full_statementL` and their backing:
- strip300_statement's hypotheses, hShared, hRHCover350, hStripMirror, hVertSV, hD4 and hS9i: as StripIII.Statement states them;
- hS9h: record A (`hS9h_record`);
- hNE: NE's certified RC record v1_5 (`hNE_record`), whose class keys cover the class `StripIII.cNE` (StripIII.NECheck, `neRec_all`);
- hBox5 over `box5List` and the n = 6 part of hO5 over `o5List`: the box record v1_2 of run 013023Z (`hBox5_record`,
  `hO5_record`);
- the n = 7 part of hO5, the two pairs of orbit G55: the G55 record of run 045359Z (StripIII.FinalIIIG55); the pairs enter as the parameter `L55` of
  `stripIII_final`.
-/
import StripIII.Proof
import StripIII.NECheck
import StripIII.CandCheck

noncomputable section

namespace G2Kernel

open StripIII

/-- **hS9h** with its record (kind: restatement, backed by record A, code/pk21/p2/a/S_TB_PRIME_RECORD_v1.md (sha8 772b9968; manifest
code/pk21/p2/a/MANIFEST_S_TB_PRIME_RECORD_v1.sha256 sha8 39e85db3): S9(h) with
its three separated kinds and its joint kind, at the thresholds of `StripIII.Shape.thrH`). -/
theorem hS9h_record (N : ℕ) : hS9h N =
    (∀ n : ℕ, 6 ≤ n → ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair n (StripIII.cH9 N n) e f → G2pair N (strip n) (uniform J) e f) := rfl

/-- **hNE** with its record (kind: restatement, backed by NE's certified RC record
code/pk22/w1/rc_cert/out/ne_rc_record_cert_kt_s8h_rcc_v1_5.kv (sha8 8ff64462; manifest code/pk22/w1/rc_cert/MANIFEST_NE_RC_RECORD_v1_5.sha256
sha8 93cb0f91; engine code/pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py, sha8 e4243548), whose CLAIM gives Cov > 0 at N = 4 for every J >= 350 and at N = 3 for every J >= 300
on NE's FLIP/SAME and MIXED classes (every two-sided class with n >= 5, the 58 separated pairs of P_3 x P_5 among them, and every class
at infinity and far)).
The record's class keys cover `StripIII.cNE`:
StripIII.NECheck, `neRec_all`, with the convention
checked on the 58 pairs of n = 5
(`pairMap4_keys`, `pairMap3_keys`, `pairMap4_cNE`, `pairMap3_cNE`,
`cNE5_pairMap4`, `cNE5_pairMap3`). -/
theorem hNE_record (N : ℕ) : hNE N =
    (∀ n : ℕ, 5 ≤ n → ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair n (StripIII.cNE N n) e f → G2pair N (strip n) (uniform J) e f) := rfl

/-- **hBox5** with its record, for the list `StripIII.box5List` (kind: restatement, backed by the box record v1_2 of run
013023Z, the final record of the run, code/pk23/o5/records/O5_BOX_RECORD_run_20261118T013023Z_v1_2.md (sha8 3abdb733; manifest
MANIFEST_O5_BOX_RECORD_run_20261118T013023Z_v1_2.sha256 sha8 ff08d9ce; table O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv sha8 19945efd, from
which `box5List` and `o5List` were made):
the orbits n5 G12, G13, G26, G27, G06, G21 at N = 3
(J1 300) and N = 4 (J1 350), with J^2 Cov >= L > 0, i.e. Cov >= L/J^2 > 0,
for every J >= J1). -/
theorem hBox5_record (N : ℕ) (L : List (ECode × ECode)) : hBox5 N L =
    (∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair 5 (fun a b => L.contains (a, b)) e f → G2pair N (strip 5) (uniform J) e f) := rfl

/-- **hO5** with its records, for the list `StripIII.o5List ++ L55` (kind: restatement; the n = 6 part, the orbits n6 G27 and G46 at
N = 4, backed by the box record v1_2 of run 013023Z as in `hBox5_record`; the n = 7 part, the two pairs of orbit G55 in `L55`, by the
G55 record of run 045359Z (StripIII.FinalIIIG55)). -/
theorem hO5_record (N : ℕ) (L : List (ℕ × ECode × ECode)) : hO5 N L =
    (N = 4 → ∀ n : ℕ, ∀ J : ℝ, jLow N ≤ J → ∀ e f, codePair n (fun a b => L.contains (n, a, b)) e f →
      G2pair N (strip n) (uniform J) e f) := rfl

/-- **Part (f) of Theorem 6.34 over every coupling J >= 0, final form**: `stripIII_full_statementL` with the list `box5List` for hBox5 and
`o5List ++ L55` for hO5, where `L55` holds the pairs of orbit G55 from their record (StripIII.FinalIIIG55). It needs `o5List ++ L55` to pass the check
`o5Check`; the second premise, the in-class direction, keeps the final list free of extra pairs, and the proof does not
use it. `box5List` passes both checks already (`finalLists_now`). The records of the hypotheses: `hS9h_record`, `hNE_record`,
`hBox5_record` and `hO5_record`, and StripIII.Statement for the others. -/
theorem stripIII_final (N : ℕ) (L55 : List (ℕ × ECode × ECode)) (h55 : o5Check (o5List ++ L55) = true)
    (_h55c : o5InClass (o5List ++ L55) = true) : stripIII_full_statementL N box5List (o5List ++ L55) :=
  stripIII_full_of_lists N box5List (o5List ++ L55) box5List_check h55

/-- the lists now: `box5List` covers its class and lies within it; `o5List` lies within O5 and still lacks the pairs of G55 -/
theorem finalLists_now : box5Check box5List = true ∧ box5InClass box5List = true ∧ o5InClass o5List = true ∧
    o5Check o5List = false :=
  ⟨box5List_check, box5List_inClass, o5List_inClass, o5List_open_until_G55⟩

/-- TRIAL (INFO): the two pairs of G55 as the n = 7 probe enumerates them, the n = 7 entries of StripIII.CandCheck's `candO5`
(not certified data; never to be cited as the result) -/
def trialG55 : List (ℕ × ECode × ECode) := candO5.filter fun q => q.1 == 7

theorem trialG55_checks : trialG55.length = 2 ∧ o5Check (o5List ++ trialG55) = true ∧ o5InClass (o5List ++ trialG55) = true := by
  decide +kernel

theorem stripIII_final_trial (N : ℕ) : stripIII_full_statementL N box5List (o5List ++ trialG55) :=
  stripIII_final N trialG55 trialG55_checks.2.1 trialG55_checks.2.2

end G2Kernel
