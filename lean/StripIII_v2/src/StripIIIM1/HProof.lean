/-
StripIIIM1.HProof: the assembly of M1's interim
theorem from the named hypotheses. `fullStripM1_of_parts` proves `fullStripM1_statementL N L5 L6 L2 L nmax` from Theorem 6.34 (f) over
every J >= 0 for the lists L5, L6, the complete small-n theorem for the list L2, and the check `m1Check L n` at every n with
6 <= n <= nmax. The proof: n <= 5 by the small-n theorem; for n >= 6, a pair without a middle-row horizontal edge by Theorem 6.34 (f);
a pair with one: J <= 300 by strip300_thm, the window 300 < J < 350 at N = 4 by hShared and hRHCover350, and J >= jLow N by the case
of the code pair (`hpair_of_check`): a common vertex (hShared), a left-right mirror pair (hStripMirror), the end orbit (`endPair_G2`,
G2Kernel_Lb_p13's `corner_step` with hShared), and every other pair, a to-do pair, by hM1 through the check. It uses the lemmas of StripIII.Proof.
-/
import StripIIIM1.HStatement
import StripIII.Proof

noncomputable section

namespace G2Kernel

open StripIII

/-- the code of a middle-row horizontal edge is a middle-row code (the converse of `edgeCode_midH`) -/
theorem edgeCode_midH_true {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (hm : midRowEdge n e) : (edgeCode e).midH = true := by
  obtain ⟨i, j, hij, rfl⟩ := hm
  rw [edgeCode_hor 1 i j hij]
  show ((1 : Fin 3).val == 1) = true
  decide

/-- a corner (r, x), r = 0 or 2, is not a vertex of a middle-row edge -/
theorem corner_not_mem {n : ℕ} {r : Fin 3} (hr : r = 0 ∨ r = 2) (x a b : Fin n) :
    (r, x) ∉ s(((1 : Fin 3), a), ((1 : Fin 3), b)) := by
  intro hm
  rw [Sym2.mem_iff] at hm
  rcases hm with hm | hm <;> rcases hr with rfl | rfl <;> exact absurd (Prod.mk.inj hm).1 (by decide)

/-- the vertical edge at a corner (r, x), r = 0 or 2, is an edge of `strip n` -/
theorem corner_vert_mem {n : ℕ} {r : Fin 3} (hr : r = 0 ∨ r = 2) (x : Fin n) :
    s((r, x), ((1 : Fin 3), x)) ∈ (strip n).edgeSet := by
  rcases hr with rfl | rfl
  · exact strip_col_mem 0 1 x (by decide)
  · rw [Sym2.eq_swap]
    exact strip_col_mem 1 2 x (by decide)

/-- the vertical edge at a corner (r, x), r = 0 or 2, is not a middle-row edge -/
theorem corner_vert_ne {n : ℕ} {r : Fin 3} (hr : r = 0 ∨ r = 2) (x a b : Fin n) :
    s((r, x), ((1 : Fin 3), x)) ≠ s(((1 : Fin 3), a), ((1 : Fin 3), b)) := by
  intro h'
  apply corner_not_mem hr x a b
  rw [← h']
  exact Sym2.mem_mk_left _ _

/-- **The end orbit** (Appendix B; Cov >= 0 only): for J >= 0, a pair (h, t) of `StripIII.endPair`, h = h_1 with t = t_1 or
bb_1, or h = h_{n-1} with t = t_{n-1} or bb_{n-1} (1-based names), has nonnegative covariance. `corner_step` of G2Kernel_Lb_p13 (Lemma 6.2)
replaces t by the vertical edge at its end corner, which shares a vertex with h, and hShared (Theorem 3.2) applies. -/
theorem endPair_G2 {N n : ℕ} (hS : hSphereIso N) (hSh : hShared N) {J : ℝ} (hJ0 : 0 ≤ J)
    {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet)
    (h : endPair n (edgeCode e) (edgeCode f) = true) : G2pair N (strip n) (uniform J) e f := by
  have hFerro : Ferro (strip n) (uniform J) := fun _ _ => hJ0
  have hcode : ∃ c r : ℕ, (c = 0 ∨ c = n - 2) ∧ (r = 0 ∨ r = 2) ∧ edgeCode e = ECode.hor 1 c ∧ edgeCode f = ECode.hor r c := by
    simp only [endPair, Bool.or_eq_true, Bool.and_eq_true, beq_iff_eq] at h
    rcases h with ⟨h1, h2 | h2⟩ | ⟨h1, h2 | h2⟩
    · exact ⟨0, 0, Or.inl rfl, Or.inl rfl, h1, h2⟩
    · exact ⟨0, 2, Or.inl rfl, Or.inr rfl, h1, h2⟩
    · exact ⟨n - 2, 0, Or.inr rfl, Or.inl rfl, h1, h2⟩
    · exact ⟨n - 2, 2, Or.inr rfl, Or.inr rfl, h1, h2⟩
  obtain ⟨c, r, hc, hr, hce, hcf⟩ := hcode
  obtain ⟨r1, a1, b1, hr1, ha1, hab1, rfl⟩ := edge_of_code_hor he hce
  obtain ⟨r2, a2, b2, hr2, ha2, hab2, rfl⟩ := edge_of_code_hor hf hcf
  have e1 : r1 = 1 := Fin.ext hr1
  have ea : a2 = a1 := Fin.ext (by omega)
  have eb : b2 = b1 := Fin.ext (by omega)
  have hr2' : r2 = 0 ∨ r2 = 2 := by
    rcases hr with rfl | rfl
    · exact Or.inl (Fin.ext hr2)
    · exact Or.inr (Fin.ext hr2)
  rw [e1] at he ⊢
  rw [ea, eb]
  have hb1 := b1.isLt
  apply G2pair_symm_strip
  unfold G2pair
  rcases hc with hc | hc
  · -- the left end: the corner (r2, a1) with its row neighbour (r2, b1)
    have hstep := corner_step hS J r2 a1 b1 hr2' (Or.inl ⟨by omega, by omega⟩) s(((1 : Fin 3), a1), ((1 : Fin 3), b1))
      (corner_not_mem hr2' a1 a1 b1)
    rw [← hstep]
    exact hSh (Fin 3 × Fin n) (strip n) (uniform J) hFerro _ (corner_vert_mem hr2' a1) _ he (corner_vert_ne hr2' a1 a1 b1)
      ⟨((1 : Fin 3), a1), Sym2.mem_mk_right _ _, Sym2.mem_mk_left _ _⟩
  · -- the right end: the corner (r2, b1) with its row neighbour (r2, a1)
    have hstep := corner_step hS J r2 b1 a1 hr2' (Or.inr ⟨by omega, by omega⟩) s(((1 : Fin 3), a1), ((1 : Fin 3), b1))
      (corner_not_mem hr2' b1 a1 b1)
    rw [show s((r2, a1), (r2, b1)) = s((r2, b1), (r2, a1)) from Sym2.eq_swap, ← hstep]
    exact hSh (Fin 3 × Fin n) (strip n) (uniform J) hFerro _ (corner_vert_mem hr2' b1) _ he (corner_vert_ne hr2' b1 a1 b1)
      ⟨((1 : Fin 3), b1), Sym2.mem_mk_right _ _, Sym2.mem_mk_right _ _⟩

/-- **The pairs with a middle-row horizontal edge** at 6 <= n <= nmax and J >= jLow N: hShared (a common vertex), hStripMirror (a
left-right mirror pair), `endPair_G2` (the end orbit), and hM1 through the check at n (the other to-do pairs) -/
theorem hpair_of_check {N : ℕ} {L : List (ℕ × ECode × ECode)} {nmax : ℕ} (hS : hSphereIso N) (hSh : hShared N)
    (hMir : hStripMirror N) (hM : hM1 N L nmax) {n : ℕ} (hn6 : 6 ≤ n) (hnmax : n ≤ nmax) (hchk : m1Check L n = true)
    {J : ℝ} (hlow : jLow N ≤ J) {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet)
    (hef : e ≠ f) (hmid : midRowEdge n e ∨ midRowEdge n f) : G2pair N (strip n) (uniform J) e f := by
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
        exact (hMir n (by omega) J hJ0).2 e he
      · have hef' : e = Sym2.map stripReflV f := edgeCode_inj he hmapF (hl.trans hcodeF.symm)
        rw [hef']
        exact G2pair_symm_strip ((hMir n (by omega) J hJ0).2 f hf)
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
      · -- the classes of M1's record, through the check
        have hend' : sameBondEnd n (edgeCode e) (edgeCode f) = false := by simpa using hend
        have hc := List.all_eq_true.mp hchk _ (mem_allPairsAll hvE hvF hcne)
        dsimp only at hc
        rw [htodo, hend'] at hc
        exact hM J hlow n hn6 hnmax e he f hf hef hc

/-- **Assembly of M1's interim theorem** from Theorem 6.34 (f) over every J >= 0 for L5 and L6, the complete small-n theorem for L2 and
the check of M1's list L at every n with 6 <= n <= nmax -/
theorem fullStripM1_of_parts (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) (L2 : List (ECode × ECode))
    (L : List (ℕ × ECode × ECode)) (nmax : ℕ) (hIII : stripIII_full_statementL N L5 L6) (hSm : smallN_statementL N L2)
    (hchk : ∀ n, 6 ≤ n → n ≤ nmax → m1Check L n = true) : fullStripM1_statementL N L5 L6 L2 L nmax := by
  intro hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hNE hBox hS9h hS9i hO5 hBoxAll hM
    n hn hnmax J hJ0 e he f hf hef
  by_cases hn5 : n ≤ 5
  · exact hSm hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hBoxAll n hn hn5 J hJ0 e he f hf hef
  · by_cases hmid : midRowEdge n e ∨ midRowEdge n f
    · by_cases hJ300 : J ≤ 300
      · exact (strip300_thm N hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH).1 n hn J hJ0 hJ300 e he f hf hef
      · replace hJ300 : 300 < J := not_le.mp hJ300
        by_cases hlow : jLow N ≤ J
        · exact hpair_of_check hS hSh hMir hM (by omega) hnmax (hchk n (by omega) hnmax) hlow he hf hef hmid
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
        n hn J hJ0 e he f hf hef hme hmf

end G2Kernel
