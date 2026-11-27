/-
G2S0.OrbitB (S0 follow-up, AUDIT_S0_v1 item 3h): H22 `hBox5` and H25 `hO5` per representative, and the top theorems T7 and T8 with every
orbit-step hypothesis per representative.
The package lists every member of the orbits behind H22 (`StripIII.box5List`: n = 5, orbits G12, G13, G26, G27, G06, G21) and H25
(`StripIII.o5List ++ L55`: orbits n6 G27, n6 G46, n7 G55), while each box record certifies one pair per orbit. `hBox5rep` and `hO5rep`
ask for exactly the record pairs (`StripIII.box5RepsH22`, `StripIII.o5Reps`, G2S0.BoxRepsB: the tables' orbit column); the per-class
forms follow through the two reflections (`G2pair_of_orbitForms`, G2S0.Orbit), with the coverage of the lists checked by decide.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Appendix B, Propositions B.14 and B.15.
-/
import G2S0.OrbitM2v2
import G2S0.BoxRepsB
import G2S0.KData

noncomputable section

namespace G2Kernel

open StripIII (ECode)

/-! ### H22 per representative -/

/-- **hBox5rep** (H22 per representative; kind: restatement, exactly what the box record of run 013023Z certifies for the orbits n5
G12, G13, G26, G27, G06, G21): for J >= jLow N, every pair of edges of P_3 x P_5 whose code pair is a representative pair in `R` has
nonnegative covariance. The record's representatives are `StripIII.box5RepsH22`. -/
def hBox5rep (N : ℕ) (R : List (ECode × ECode)) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ q ∈ R, ∀ e ∈ (strip 5).edgeSet, ∀ f ∈ (strip 5).edgeSet,
    edgeCode e = q.1 → edgeCode f = q.2 → G2pair N (strip 5) (uniform J) e f

theorem box5RepCheck_H22 : StripIII.box5RepCheck StripIII.box5RepsH22 StripIII.box5List = true := by
  decide +kernel

/-- control: every representative is a member of `box5List` (in one order), and the 6 representatives lie in 6 distinct orbits -/
theorem box5RepsH22_controls :
    StripIII.box5RepsH22.all (fun q => StripIII.box5List.contains q || StripIII.box5List.contains (q.2, q.1)) = true ∧
    StripIII.box5RepsH22.all (fun q => (StripIII.box5RepsH22.filter fun q' =>
      (StripIII.orbitForms 5 q.1 q.2).contains q').length == 1) = true := by
  decide +kernel

/-- **H22 from its representatives** -/
theorem hBox5_of_rep (N : ℕ) : hBox5rep N StripIII.box5RepsH22 → hBox5 N StripIII.box5List := by
  intro h J hJ e f hc
  obtain ⟨he, hf, hef, -, -, hL⟩ := hc
  exact hBoxAll5_of_rep_gen N _ _ box5RepCheck_H22 h J hJ e he f hf hef hL

/-! ### H25 per representative -/

/-- **hO5rep** (H25 per representative; kind: restatement, exactly what the box records certify at N = 4: the orbits n6 G27 and
n6 G46 by run 013023Z, n7 G55 by run 045359Z): at N = 4, for J >= jLow N, for each entry (n, a, b) of `R`, every pair of edges of
P_3 x P_n with the codes (a, b) has nonnegative covariance. The records' representatives are `StripIII.o5Reps`. -/
def hO5rep (N : ℕ) (R : List (ℕ × ECode × ECode)) : Prop :=
  N = 4 → ∀ J : ℝ, jLow N ≤ J → ∀ q ∈ R, ∀ e ∈ (strip q.1).edgeSet, ∀ f ∈ (strip q.1).edgeSet,
    edgeCode e = q.2.1 → edgeCode f = q.2.2 → G2pair N (strip q.1) (uniform J) e f

/-- the check of a representative list `R` against a list `L` of entries (n, code pair): every representative is a pair of valid
codes at its n, and every entry of `L` is one of the eight images of a representative with the same n -/
def StripIII.o5RepCheck (R L : List (ℕ × ECode × ECode)) : Bool :=
  R.all (fun q => q.2.1.valid q.1 && q.2.2.valid q.1) &&
    L.all (fun p => R.any (fun q => q.1 == p.1 && (StripIII.orbitForms q.1 q.2.1 q.2.2).contains (p.2.1, p.2.2)))

theorem o5RepCheck_final : StripIII.o5RepCheck StripIII.o5Reps (StripIII.o5List ++ L55) = true := by
  decide +kernel

/-- control: every representative is an entry of `o5List ++ L55` (in one order), and the 3 representatives lie in 3 distinct
orbits -/
theorem o5Reps_controls :
    StripIII.o5Reps.all (fun q => (StripIII.o5List ++ L55).contains q ||
      (StripIII.o5List ++ L55).contains (q.1, q.2.2, q.2.1)) = true ∧
    StripIII.o5Reps.all (fun q => (StripIII.o5Reps.filter fun q' => q'.1 == q.1 &&
      (StripIII.orbitForms q.1 q.2.1 q.2.2).contains (q'.2.1, q'.2.2)).length == 1) = true := by
  decide +kernel

theorem hO5_of_rep_gen (N : ℕ) (R L : List (ℕ × ECode × ECode)) (hc : StripIII.o5RepCheck R L = true)
    (h : hO5rep N R) : hO5 N L := by
  intro hN4 n J hJ e f hcp
  obtain ⟨he, hf, _hef, -, -, hL⟩ := hcp
  simp only [StripIII.o5RepCheck, Bool.and_eq_true, List.all_eq_true, List.any_eq_true, beq_iff_eq] at hc
  obtain ⟨hv, hcov⟩ := hc
  obtain ⟨q, hq, hqn, hqp⟩ := hcov _ (List.contains_iff_mem.mp hL)
  have hqv := hv q hq
  obtain ⟨qn, qa, qb⟩ := q
  simp only at hqn hqv hqp
  subst hqn
  exact G2pair_of_orbitForms hqv.1 hqv.2 (fun e' he' f' hf' h1 h2 => h hN4 J hJ _ hq e' he' f' hf' h1 h2) he hf
    (List.contains_iff_mem.mp hqp)

/-- **H25 from its representatives** -/
theorem hO5_of_rep (N : ℕ) : hO5rep N StripIII.o5Reps → hO5 N (StripIII.o5List ++ L55) :=
  hO5_of_rep_gen N _ _ o5RepCheck_final

/-! ### T7 and T8 with every orbit-step hypothesis per representative -/

/-- Theorem 6.34 (f) (T7) with H1 discharged and H22, H25 per representative: `stripIII_full_statementL N box5List (o5List ++ L55)`
without the premise hSphereIso N and with hBox5rep N box5RepsH22, hO5rep N o5Reps in place of hBox5 N box5List, hO5 N (o5List ++ L55);
the other premises verbatim. -/
def stripIII_statement_S0r (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f

theorem stripIII_thm_S0r (N : ℕ) : stripIII_statement_S0r N := by
  intro hN hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVSV hD4 hNE hB5 hH9 hI9 hO5
  exact stripIII_thm N hN (hSphereIso_holds N) hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVSV hD4
    hNE (hBox5_of_rep N hB5) hH9 hI9 (hO5_of_rep N hO5)

/-- Theorem 1.4 (i) (T8) with H1 discharged and H22, H25, H26, H27, H28 per representative:
`fullStrip_statementL N box5List (o5List ++ L55) (box5AllList34 ++ box5Stage2) m1List NMAX_M1 D0_M2 M0_M2` without the premise
hSphereIso N and with hBox5rep, hO5rep, hBoxAll5rep, hM1rep, hM2tailRep in place of hBox5, hO5, hBoxAll5, hM1, hM2tail; the other
premises verbatim. -/
def fullStrip_statement_S0r (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps → hBoxAll5rep N StripIII.box5Reps → hM1rep N StripIII.m1List StripIII.NMAX_M1 →
  hM2tailRep N StripIII.D0_M2 StripIII.M0_M2 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

theorem fullStrip_thm_S0r (N : ℕ) : fullStrip_statement_S0r N := by
  intro hN hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVSV hD4 hNE hB5 hH9 hI9 hO5 hBox hM1r hM2r
  exact fullStrip_thm_S0 N hN hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVSV hD4 hNE
    (hBox5_of_rep N hB5) hH9 hI9 (hO5_of_rep N hO5) hBox hM1r hM2r

/-- T8 for the paper's k (N = 3, 4): H1 and H3 discharged, H22, H25 and H26-H28 per representative -/
theorem fullStrip_thm_concrete_r (N : ℕ) (hN : N = 3 ∨ N = 4) :
    hShared N → hRPGibbs N → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
    hRatio (kConc N) → hCornerFactor N (kConc N) →
    hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
    hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
    hO5rep N StripIII.o5Reps → hBoxAll5rep N StripIII.box5Reps → hM1rep N StripIII.m1List StripIII.NMAX_M1 →
    hM2tailRep N StripIII.D0_M2 StripIII.M0_M2 →
      ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f := by
  intro hSh hRP hW md hSI hSC hR hCF
  have h2 : 2 ≤ N := by rcases hN with rfl | rfl <;> norm_num
  exact fullStrip_thm_S0r N hN hSh hRP hW md hSI hSC (kConc N) (hKReg_kConc N h2) hR hCF

end G2Kernel

#print axioms G2Kernel.box5RepCheck_H22
#print axioms G2Kernel.box5RepsH22_controls
#print axioms G2Kernel.hBox5_of_rep
#print axioms G2Kernel.o5RepCheck_final
#print axioms G2Kernel.o5Reps_controls
#print axioms G2Kernel.hO5_of_rep
#print axioms G2Kernel.stripIII_thm_S0r
#print axioms G2Kernel.fullStrip_thm_S0r
#print axioms G2Kernel.fullStrip_thm_concrete_r
