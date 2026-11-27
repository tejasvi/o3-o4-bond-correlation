/-
G2S1.TopMergeH16 (stage B, prepared): H16 merged into S3's top forms (STATEMENTS_A2B_v1.md §B). Each form is
S3's Part D form (G2S3.Top, G2S3.TopIII, read-only copies) with the one premise `hLadder N` removed; every other premise and the
conclusion are verbatim. Each is proved by applying the S3 theorem with `hLadder_of34`, from hLadder_holds3/4 (G2S1.Ladder).
T3 and T4 have no hLadder premise. Final only after the S3 + H16 audit and the merge decision.
-/
import G2S3.TopIII
import G2S1.Ladder

namespace G2S1

open G2Kernel G2Kernel.StripIII

/-- H16 at N = 3 and N = 4 -/
theorem hLadder_of34 {N : ℕ} (hN : N = 3 ∨ N = 4) : hLadder N := by
  rcases hN with rfl | rfl
  · exact hLadder_holds3
  · exact hLadder_holds4

/-- T5 (Theorem 6.34 (b) and Corollary 6.20 for J ≤ 300): `G2S3.strip300_thm_S3` without hLadder -/
theorem strip300_thm_H16 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
    hHub N → hLBu N → hRHCover N →
      (∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f) ∧
      (∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
          0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)) := by
  intro hN hW md hId hCert hHub hLBu hRH
  exact G2S3.strip300_thm_S3 N hN hW md hId hCert hHub hLBu (hLadder_of34 hN) hRH

/-- T6 (Theorem 6.34 (e)): `G2S3.smallN_statement_S3` without hLadder -/
def smallN_statement_H16 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hBoxAll5rep N StripIII.box5Reps →
    ∀ n : ℕ, 1 ≤ n → n ≤ 5 → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

theorem smallN_thm_H16 (N : ℕ) : smallN_statement_H16 N := by
  intro hN hW md hId hCert hHub hLBu hRH hRH350 hVert hD4 hBox
  exact G2S3.smallN_thm_S3 N hN hW md hId hCert hHub hLBu (hLadder_of34 hN) hRH hRH350 hVert hD4 hBox

/-- T7 (Theorem 6.34 (f)): `G2S3.stripIII_statement_S3r` without hLadder -/
def stripIII_statement_H16 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f

theorem stripIII_thm_H16 (N : ℕ) : stripIII_statement_H16 N := by
  intro hN hW md hId hCert hHub hLBu hRH hRH350 hVert hD4 hNE hB5 hS9h hS9i hO5
  exact G2S3.stripIII_thm_S3r N hN hW md hId hCert hHub hLBu (hLadder_of34 hN) hRH hRH350 hVert hD4 hNE hB5 hS9h hS9i hO5

/-- T8 (Theorem 1.4 (i)): `G2S3.fullStrip_statement_S3r` without hLadder -/
def fullStrip_statement_H16 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps → hBoxAll5rep N StripIII.box5Reps → hM1rep N StripIII.m1List StripIII.NMAX_M1 →
  hM2tailRep N StripIII.D0_M2 StripIII.M0_M2 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

theorem fullStrip_thm_H16 (N : ℕ) : fullStrip_statement_H16 N := by
  intro hN hW md hId hCert hHub hLBu hRH hRH350 hVert hD4 hNE hB5 hS9h hS9i hO5 hBA hM1 hM2
  exact G2S3.fullStrip_thm_S3r N hN hW md hId hCert hHub hLBu (hLadder_of34 hN) hRH hRH350 hVert hD4 hNE hB5 hS9h hS9i
    hO5 hBA hM1 hM2

/-! ### Controls: each new form implies S3's form (drop the hLadder argument) -/

theorem smallN_H16_to_S3 (N : ℕ) : smallN_statement_H16 N → G2S3.smallN_statement_S3 N := by
  intro h hN hW md hId hCert hHub hLBu _ hRH hRH350 hVert hD4 hBox
  exact h hN hW md hId hCert hHub hLBu hRH hRH350 hVert hD4 hBox

theorem stripIII_H16_to_S3 (N : ℕ) : stripIII_statement_H16 N → G2S3.stripIII_statement_S3r N := by
  intro h hN hW md hId hCert hHub hLBu _ hRH hRH350 hVert hD4 hNE hB5 hS9h hS9i hO5
  exact h hN hW md hId hCert hHub hLBu hRH hRH350 hVert hD4 hNE hB5 hS9h hS9i hO5

theorem fullStrip_H16_to_S3 (N : ℕ) : fullStrip_statement_H16 N → G2S3.fullStrip_statement_S3r N := by
  intro h hN hW md hId hCert hHub hLBu _ hRH hRH350 hVert hD4 hNE hB5 hS9h hS9i hO5 hBA hM1 hM2
  exact h hN hW md hId hCert hHub hLBu hRH hRH350 hVert hD4 hNE hB5 hS9h hS9i hO5 hBA hM1 hM2

end G2S1

#print axioms G2S1.strip300_thm_H16
#print axioms G2S1.smallN_thm_H16
#print axioms G2S1.stripIII_thm_H16
#print axioms G2S1.fullStrip_thm_H16
