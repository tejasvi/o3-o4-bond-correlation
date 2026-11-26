/-
StripIIIM2.M2Proof: the assembly of M2's
theorem and of the strip theorem for every n from the named hypotheses. `fullStripM2_of_parts` proves `fullStripM2_statementL N L5 L6 D0
M0 nmin` from Theorem 6.34 (f) over every J >= 0 for every nmin >= 2 D0 + M0 + 2: a pair without a middle-row horizontal edge by Theorem
6.34 (f); one with: J <= 300 by strip300_thm, the window 300 < J < 350 at N = 4 by hShared and hRHCover350, and J >= jLow N by
`hpair_of_todo` (a common vertex: hShared; a left-right mirror pair: hStripMirror; the end orbit: StripIIIM1.HProof's `endPair_G2`) with
hM2tail for the other to-do pairs through the covering `tail_cover`. `fullStrip_of_parts` joins M1's theorem (n <= nmax) and M2's
(n >= nmin, nmin <= nmax + 1). It uses the lemmas of StripIII.Proof and StripIIIM1.HProof.
-/
import StripIIIM2.M2Statement
import StripIIIM1.HProof

noncomputable section

namespace G2Kernel

open StripIII

/-- the pairs with a middle-row horizontal edge at J >= jLow N: hShared (a common vertex), hStripMirror (a left-right mirror pair),
`endPair_G2` (the end orbit), and the hypothesis `hT` for the other to-do pairs -/
theorem hpair_of_todo {N n : ℕ} (hS : hSphereIso N) (hSh : hShared N) (hMir : hStripMirror N) (hn : 1 ≤ n) {J : ℝ}
    (hlow : jLow N ≤ J) {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet) (hef : e ≠ f)
    (hmid : midRowEdge n e ∨ midRowEdge n f)
    (hT : todoH n (edgeCode e) (edgeCode f) = true → sameBondEnd n (edgeCode e) (edgeCode f) = false →
      G2pair N (strip n) (uniform J) e f) :
    G2pair N (strip n) (uniform J) e f := by
  have hJ0 : 0 ≤ J := le_trans (by norm_num) (le_trans (jLow_ge N) hlow)
  have hFerro : Ferro (strip n) (uniform J) := fun _ _ => hJ0
  have hvE := edgeCode_valid he
  have hvF := edgeCode_valid hf
  have hcne : edgeCode e ≠ edgeCode f := fun h' => hef (edgeCode_inj he hf h')
  by_cases hcv : commonVertexAct (edgeCode e) (edgeCode f) = true
  · -- a common vertex: S0
    exact hSh (Fin 3 × Fin n) (strip n) (uniform J) hFerro e he f hf hef (common_of_act he hf hcv)
  · by_cases hlr : lrMirror n (edgeCode e) (edgeCode f) = true
    · -- a left-right mirror pair: S0
      simp only [lrMirror, Bool.or_eq_true, beq_iff_eq] at hlr
      obtain ⟨hmapE, hcodeE⟩ := edgeCode_stripReflV he
      obtain ⟨hmapF, hcodeF⟩ := edgeCode_stripReflV hf
      rcases hlr with hl | hl
      · have hfe : f = Sym2.map stripReflV e := edgeCode_inj hf hmapE (hl.trans hcodeE.symm)
        rw [hfe]
        exact (hMir n hn J hJ0).2 e he
      · have hef' : e = Sym2.map stripReflV f := edgeCode_inj he hmapF (hl.trans hcodeF.symm)
        rw [hef']
        exact G2pair_symm_strip ((hMir n hn J hJ0).2 f hf)
    · -- a to-do pair
      have hcv' : commonVertexAct (edgeCode e) (edgeCode f) = false := by simpa using hcv
      have hlr' : lrMirror n (edgeCode e) (edgeCode f) = false := by simpa using hlr
      have hmidc : ((edgeCode e).midH || (edgeCode f).midH) = true := by
        rcases hmid with hm | hm
        · rw [edgeCode_midH_true hm, Bool.true_or]
        · rw [edgeCode_midH_true hm, Bool.or_true]
      have hne' : (edgeCode e != edgeCode f) = true := bne_iff_ne.mpr hcne
      have htodo : todoH n (edgeCode e) (edgeCode f) = true := by
        unfold todoH
        rw [hvE, hvF, hne', hmidc, hcv', hlr']
        rfl
      by_cases hend : sameBondEnd n (edgeCode e) (edgeCode f) = true
      · -- the end orbit: G2Kernel_Lb_p13's corner identity with hShared
        simp only [sameBondEnd, Bool.or_eq_true] at hend
        rcases hend with h1 | h1
        · exact endPair_G2 hS hSh hJ0 he hf h1
        · exact G2pair_symm_strip (endPair_G2 hS hSh hJ0 hf he h1)
      · exact hT htodo (by simpa using hend)

/-- **The tail pairs**: for n >= 2 D0 + M0 + 2 and J >= jLow N, every pair with a middle-row horizontal edge has nonnegative covariance,
by `hpair_of_todo` with hM2tail through the covering `tail_cover` -/
theorem hpair_tail {N : ℕ} {D0 M0 : ℕ} (hS : hSphereIso N) (hSh : hShared N) (hMir : hStripMirror N) (hT : hM2tail N D0 M0)
    {n : ℕ} (hn : 2 * D0 + M0 + 2 ≤ n) {J : ℝ} (hlow : jLow N ≤ J) {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet)
    (hf : f ∈ (strip n).edgeSet) (hef : e ≠ f) (hmid : midRowEdge n e ∨ midRowEdge n f) : G2pair N (strip n) (uniform J) e f :=
  hpair_of_todo hS hSh hMir (by omega) hlow he hf hef hmid fun htodo hend =>
    hT J hlow n e he f hf htodo hend (tail_cover htodo hn)

/-- **Assembly of M2's theorem** from Theorem 6.34 (f) over every J >= 0 for L5 and L6, for every nmin >= 2 D0 + M0 + 2 with nmin >= 4 -/
theorem fullStripM2_of_parts (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) (D0 M0 nmin : ℕ)
    (hIII : stripIII_full_statementL N L5 L6) (hnmin : 2 * D0 + M0 + 2 ≤ nmin) (hn4 : 4 ≤ nmin) :
    fullStripM2_statementL N L5 L6 D0 M0 nmin := by
  intro hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hNE hBox hS9h hS9i hO5 hT
    n hn J hJ0 e he f hf hef
  by_cases hmid : midRowEdge n e ∨ midRowEdge n f
  · by_cases hJ300 : J ≤ 300
    · exact (strip300_thm N hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH).1 n (by omega) J hJ0 hJ300 e he f hf hef
    · replace hJ300 : 300 < J := not_le.mp hJ300
      by_cases hlow : jLow N ≤ J
      · exact hpair_tail hS hSh hMir hT (by omega) hlow he hf hef hmid
      · -- the window 300 < J < 350 at N = 4
        have hN4 : N = 4 := by
          rcases hN with rfl | rfl
          · exfalso
            apply hlow
            unfold jLow
            norm_num
            linarith
          · rfl
        have hJ350 : J ≤ 350 := by
          rw [hN4] at hlow
          unfold jLow at hlow
          norm_num at hlow
          linarith
        by_cases hsc : sameColumn n e f
        · exact hSh (Fin 3 × Fin n) (strip n) (uniform J) (fun _ _ => hJ0) e he f hf hef (sameColumn_shared hsc)
        · exact le_of_lt (hRH350 hN4 n (by omega) J (le_of_lt hJ300) hJ350 e he f hf hef hsc)
  · have hme : ¬ midRowEdge n e := fun h' => hmid (Or.inl h')
    have hmf : ¬ midRowEdge n f := fun h' => hmid (Or.inr h')
    exact hIII hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hNE hBox hS9h hS9i hO5
      n (by omega) J hJ0 e he f hf hef hme hmf

/-- **Assembly of the strip theorem for every n** from M1's theorem (n <= nmax) and M2's (n >= nmin), with nmin <= nmax + 1 -/
theorem fullStrip_of_parts (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) (L2 : List (ECode × ECode))
    (L : List (ℕ × ECode × ECode)) (nmax D0 M0 nmin : ℕ) (h1 : fullStripM1_statementL N L5 L6 L2 L nmax)
    (h2 : fullStripM2_statementL N L5 L6 D0 M0 nmin) (hm : nmin ≤ nmax + 1) : fullStrip_statementL N L5 L6 L2 L nmax D0 M0 := by
  intro hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hNE hBox hS9h hS9i hO5 hBoxAll hM hT
    n hn J hJ0 e he f hf hef
  by_cases hnm : n ≤ nmax
  · exact h1 hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hNE hBox hS9h hS9i hO5 hBoxAll hM
      n hn hnm J hJ0 e he f hf hef
  · exact h2 hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hNE hBox hS9h hS9i hO5 hT
      n (by omega) J hJ0 e he f hf hef

end G2Kernel
