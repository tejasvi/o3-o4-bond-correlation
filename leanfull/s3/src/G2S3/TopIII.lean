/-
G2S3.TopIII (stage S3): the top theorems T6, T7, T8 without H3, H4, H6, H7, H8, H18 (S0 already discharged H1), the
helpers M1, M2 in the same form, and the old forms of T3-T8 derived from the S3 forms (STATEMENTS_S3_v4.md, Part D).
The assembly proofs are the package's (StripIII.Small5Proof `smallN_of_list`, StripIII.Proof `stripIII_full_of_lists`,
StripIIIM1.HProof `fullStripM1_of_parts`, StripIIIM2.M2Proof `fullStripM2_of_parts`, `fullStrip_of_parts`), copied with
`strip300_thm_S3` for J ≤ 300 and the discharges `hSphereIso_holds N` (S0), `hShared_of hN`, `hStripMirror_holds N` (S3)
passed to the package lemmas that take hS, hSh, hMir; the parts for J > 300 are otherwise unchanged.
-/
import G2S3.Top

noncomputable section

namespace G2S3

open G2Kernel G2Kernel.StripIII

/-! ### T6: Theorem 6.34 (e) -/

/-- T6 with a list parameter: the package's `smallN_statementL N L` without hSphereIso, hShared, hRPGibbs, the k-triple
and hStripMirror -/
def smallN_statementL_S3 (N : ℕ) (L : List (ECode × ECode)) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hBoxAll5 N L →
    ∀ n : ℕ, 1 ≤ n → n ≤ 5 → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

/-- the package's `smallN_of_list`, with `strip300_thm_S3` and the S3 discharges of hShared and hStripMirror -/
theorem smallN_of_list_S3 (N : ℕ) (L : List (ECode × ECode)) (h : box5AllCheck L = true) :
    smallN_statementL_S3 N L := by
  intro hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hBox n hn hn5 J hJ0 e he f hf hef
  have hSh : hShared N := hShared_of hN
  have hMir : hStripMirror N := hStripMirror_holds N
  by_cases hJ300 : J ≤ 300
  · exact (strip300_thm_S3 N hN hW md hSI hSC hHub hLBu hLad hRH).1 n hn J hJ0 hJ300 e he f hf hef
  · replace hJ300 : 300 < J := not_le.mp hJ300
    by_cases hlow : jLow N ≤ J
    · by_cases hn4 : n ≤ 4
      · exact hD4' n hn hn4 J hJ0 e he f hf hef
      · -- n = 5 and J >= jLow N: the case of the code pair
        have hn5' : n = 5 := by omega
        subst hn5'
        have hFerro : Ferro (strip 5) (uniform J) := fun _ _ => hJ0
        have hvE := edgeCode_valid he
        have hvF := edgeCode_valid hf
        have hcne : edgeCode e ≠ edgeCode f := fun h' => hef (edgeCode_inj he hf h')
        have hcs := cases5 (edgeCode e) (edgeCode f) hvE hvF hcne
        simp only [Bool.or_eq_true] at hcs
        rcases hcs with (((hcv | hmir) | hlr) | hvv) | hg
        · -- a common vertex
          exact hSh (Fin 3 × Fin 5) (strip 5) (uniform J) hFerro e he f hf hef (common_of_act he hf hcv)
        · -- the mirror pair (t_i, bb_i)
          obtain ⟨i, ⟨hce, hcf⟩ | ⟨hce, hcf⟩⟩ := tbMirror_cases hmir
          · obtain ⟨r1, a1, b1, hr1, ha1, hab1, rfl⟩ := edge_of_code_hor he hce
            obtain ⟨r2, a2, b2, hr2, ha2, hab2, rfl⟩ := edge_of_code_hor hf hcf
            have e1 : r1 = 0 := Fin.ext hr1
            have e2 : r2 = 2 := Fin.ext hr2
            have e3 : a2 = a1 := Fin.ext (by omega)
            have e4 : b2 = b1 := Fin.ext (by omega)
            rw [e1, e2, e3, e4]
            exact (hMir 5 (by norm_num) J hJ0).1 a1 b1 hab1
          · obtain ⟨r1, a1, b1, hr1, ha1, hab1, rfl⟩ := edge_of_code_hor he hce
            obtain ⟨r2, a2, b2, hr2, ha2, hab2, rfl⟩ := edge_of_code_hor hf hcf
            have e1 : r1 = 2 := Fin.ext hr1
            have e2 : r2 = 0 := Fin.ext hr2
            have e3 : a2 = a1 := Fin.ext (by omega)
            have e4 : b2 = b1 := Fin.ext (by omega)
            rw [e1, e2, e3, e4]
            exact G2pair_symm_strip ((hMir 5 (by norm_num) J hJ0).1 a1 b1 hab1)
        · -- a left-right mirror pair
          simp only [lrMirror, Bool.or_eq_true, beq_iff_eq] at hlr
          obtain ⟨hmapE, hcodeE⟩ := edgeCode_stripReflV he
          obtain ⟨hmapF, hcodeF⟩ := edgeCode_stripReflV hf
          rcases hlr with hl | hl
          · have hfe : f = Sym2.map stripReflV e := edgeCode_inj hf hmapE (hl.trans hcodeE.symm)
            rw [hfe]
            exact (hMir 5 (by norm_num) J hJ0).2 e he
          · have hef' : e = Sym2.map stripReflV f := edgeCode_inj he hmapF (hl.trans hcodeF.symm)
            rw [hef']
            exact G2pair_symm_strip ((hMir 5 (by norm_num) J hJ0).2 f hf)
        · -- two vertical edges: Theorem 6.21
          rw [Bool.and_eq_true] at hvv
          obtain ⟨t1, j1, hc1⟩ := ver_of_not_isHor hvv.1
          obtain ⟨t2, j2, hc2⟩ := ver_of_not_isHor hvv.2
          obtain ⟨tt1, uu1, jj1, -, -, h1, rfl⟩ := edge_of_code_ver he hc1
          obtain ⟨tt2, uu2, jj2, -, -, h2, rfl⟩ := edge_of_code_ver hf hc2
          exact hVert 5 (by norm_num) J (le_trans (jLow_ge N) hlow) _ he _ hf hef (vertical_of_form tt1 uu1 jj1 h1)
            (vertical_of_form tt2 uu2 jj2 h2)
        · -- the class g5: the box records over L, in either order
          have hchk := List.all_eq_true.mp h _ (mem_allPairsAll hvE hvF hcne)
          simp only [hg, Bool.not_true, Bool.false_or, Bool.or_eq_true] at hchk
          rcases hchk with hc | hc
          · exact hBox J hlow e he f hf hef hc
          · exact G2pair_symm_strip (hBox J hlow f hf e he (Ne.symm hef) hc)
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
      by_cases hn4 : n ≤ 4
      · exact hD4' n hn hn4 J hJ0 e he f hf hef
      · by_cases hsc : sameColumn n e f
        · exact hSh (Fin 3 × Fin n) (strip n) (uniform J) (fun _ _ => hJ0) e he f hf hef (sameColumn_shared hsc)
        · exact le_of_lt (hRH350 hN4 n (by omega) J (le_of_lt hJ300) hJ350 e he f hf hef hsc)

theorem smallN_thmL_S3 (N : ℕ) : smallN_statementL_S3 N (box5AllList34 ++ box5Stage2) :=
  smallN_of_list_S3 N _ box5Stage2_checks.1

/-- **T6, final S3 form**: S0's `smallN_statement_S0 N` (H26 per representative) without hShared, hRPGibbs, the k-triple
and hStripMirror -/
def smallN_statement_S3 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hBoxAll5rep N StripIII.box5Reps →
    ∀ n : ℕ, 1 ≤ n → n ≤ 5 → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

theorem smallN_thm_S3 (N : ℕ) : smallN_statement_S3 N := by
  intro hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hBox
  exact smallN_thmL_S3 N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' (hBoxAll5_of_rep N hBox)

/-! ### T7: Theorem 6.34 (f) -/

/-- T7 with list parameters: the package's `stripIII_full_statementL N L5 L6` without hSphereIso, hShared, hRPGibbs, the
k-triple and hStripMirror -/
def stripIII_full_statementL_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f

/-- the package's `stripIII_full_of_lists`, with `strip300_thm_S3` and the S3 discharges -/
theorem stripIII_full_of_lists_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (h5 : box5Check L5 = true) (h6 : o5Check L6 = true) : stripIII_full_statementL_S3 N L5 L6 := by
  intro hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hBox hS9h hS9i hO5
    n hn J hJ0 e he f hf hef hme hmf
  have hSh : hShared N := hShared_of hN
  have hMir : hStripMirror N := hStripMirror_holds N
  by_cases hJ300 : J ≤ 300
  · exact (strip300_thm_S3 N hN hW md hSI hSC hHub hLBu hLad hRH).1 n hn J hJ0 hJ300 e he f hf hef
  · replace hJ300 : 300 < J := not_le.mp hJ300
    by_cases hlow : jLow N ≤ J
    · exact stripIII_of_lists N L5 L6 h5 h6 hN hSh hMir hVert hD4' hNE hBox hS9h hS9i hO5 n hn J hlow e he f hf hef hme hmf
    · have hN4 : N = 4 := by
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
      by_cases hn4 : n ≤ 4
      · exact hD4' n hn hn4 J hJ0 e he f hf hef
      · by_cases hsc : sameColumn n e f
        · exact hSh (Fin 3 × Fin n) (strip n) (uniform J) (fun _ _ => hJ0) e he f hf hef (sameColumn_shared hsc)
        · exact le_of_lt (hRH350 hN4 n (by omega) J (le_of_lt hJ300) hJ350 e he f hf hef hsc)

theorem stripIII_thmL_S3 (N : ℕ) : stripIII_full_statementL_S3 N StripIII.box5List (StripIII.o5List ++ L55) :=
  stripIII_full_of_lists_S3 N _ _ box5List_check L55_checks.1

/-- **T7, final S3 form**: S0's `stripIII_statement_S0r N` (H22, H25 per representative) without hShared, hRPGibbs, the
k-triple and hStripMirror -/
def stripIII_statement_S3r (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f

theorem stripIII_thm_S3r (N : ℕ) : stripIII_statement_S3r N := by
  intro hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hB5 hH9 hI9 hO5
  exact stripIII_thmL_S3 N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE (hBox5_of_rep N hB5) hH9 hI9
    (hO5_of_rep N hO5)

/-! ### M1's and M2's theorems (helpers of T8) -/

/-- the package's `fullStripM1_statementL` without hSphereIso, hShared, hRPGibbs, the k-triple and hStripMirror -/
def fullStripM1_statementL_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (L2 : List (ECode × ECode)) (L : List (ℕ × ECode × ECode)) (nmax : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hBoxAll5 N L2 → hM1 N L nmax →
    ∀ n : ℕ, 1 ≤ n → n ≤ nmax → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

/-- the package's `fullStripM1_of_parts`, with `strip300_thm_S3` and the S3 discharges -/
theorem fullStripM1_of_parts_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (L2 : List (ECode × ECode)) (L : List (ℕ × ECode × ECode)) (nmax : ℕ)
    (hIII : stripIII_full_statementL_S3 N L5 L6) (hSm : smallN_statementL_S3 N L2)
    (hchk : ∀ n, 6 ≤ n → n ≤ nmax → m1Check L n = true) : fullStripM1_statementL_S3 N L5 L6 L2 L nmax := by
  intro hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hBox hS9h hS9i hO5 hBoxAll hM
    n hn hnmax J hJ0 e he f hf hef
  have hS : hSphereIso N := hSphereIso_holds N
  have hSh : hShared N := hShared_of hN
  have hMir : hStripMirror N := hStripMirror_holds N
  by_cases hn5 : n ≤ 5
  · exact hSm hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hBoxAll n hn hn5 J hJ0 e he f hf hef
  · by_cases hmid : midRowEdge n e ∨ midRowEdge n f
    · by_cases hJ300 : J ≤ 300
      · exact (strip300_thm_S3 N hN hW md hSI hSC hHub hLBu hLad hRH).1 n hn J hJ0 hJ300 e he f hf hef
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
      exact hIII hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hBox hS9h hS9i hO5
        n hn J hJ0 e he f hf hef hme hmf

theorem fullStripM1_thm_S3 (N : ℕ) :
    fullStripM1_statementL_S3 N StripIII.box5List (StripIII.o5List ++ L55) (box5AllList34 ++ box5Stage2)
      StripIII.m1List StripIII.NMAX_M1 :=
  fullStripM1_of_parts_S3 N _ _ _ _ _ (stripIII_thmL_S3 N) (smallN_thmL_S3 N) m1Check_all

/-- the package's `fullStripM2_statementL` without hSphereIso, hShared, hRPGibbs, the k-triple and hStripMirror -/
def fullStripM2_statementL_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (D0 M0 nmin : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hM2tail N D0 M0 →
    ∀ n : ℕ, nmin ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

/-- the package's `fullStripM2_of_parts`, with `strip300_thm_S3` and the S3 discharges -/
theorem fullStripM2_of_parts_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (D0 M0 nmin : ℕ) (hIII : stripIII_full_statementL_S3 N L5 L6) (hnmin : 2 * D0 + M0 + 2 ≤ nmin)
    (hn4 : 4 ≤ nmin) : fullStripM2_statementL_S3 N L5 L6 D0 M0 nmin := by
  intro hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hBox hS9h hS9i hO5 hT
    n hn J hJ0 e he f hf hef
  have hS : hSphereIso N := hSphereIso_holds N
  have hSh : hShared N := hShared_of hN
  have hMir : hStripMirror N := hStripMirror_holds N
  by_cases hmid : midRowEdge n e ∨ midRowEdge n f
  · by_cases hJ300 : J ≤ 300
    · exact (strip300_thm_S3 N hN hW md hSI hSC hHub hLBu hLad hRH).1 n (by omega) J hJ0 hJ300 e he f hf hef
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
    exact hIII hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hBox hS9h hS9i hO5
      n (by omega) J hJ0 e he f hf hef hme hmf

theorem fullStripM2_thm_S3 (N : ℕ) :
    fullStripM2_statementL_S3 N StripIII.box5List (StripIII.o5List ++ L55) StripIII.D0_M2 StripIII.M0_M2 12 :=
  fullStripM2_of_parts_S3 N _ _ _ _ _ (stripIII_thmL_S3 N) M2_params.1 (by norm_num)

/-! ### T8: Theorem 1.4 (i) -/

/-- T8 with list parameters: the package's `fullStrip_statementL` without hSphereIso, hShared, hRPGibbs, the k-triple and
hStripMirror -/
def fullStrip_statementL_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (L2 : List (ECode × ECode)) (L : List (ℕ × ECode × ECode)) (nmax D0 M0 : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hBoxAll5 N L2 → hM1 N L nmax →
  hM2tail N D0 M0 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

/-- the package's `fullStrip_of_parts` in the S3 form -/
theorem fullStrip_of_parts_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (L2 : List (ECode × ECode)) (L : List (ℕ × ECode × ECode)) (nmax D0 M0 nmin : ℕ)
    (h1 : fullStripM1_statementL_S3 N L5 L6 L2 L nmax) (h2 : fullStripM2_statementL_S3 N L5 L6 D0 M0 nmin)
    (hm : nmin ≤ nmax + 1) : fullStrip_statementL_S3 N L5 L6 L2 L nmax D0 M0 := by
  intro hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hBox hS9h hS9i hO5 hBoxAll hM hT
    n hn J hJ0 e he f hf hef
  by_cases hnm : n ≤ nmax
  · exact h1 hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hBox hS9h hS9i hO5 hBoxAll hM
      n hn hnm J hJ0 e he f hf hef
  · exact h2 hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hBox hS9h hS9i hO5 hT
      n (by omega) J hJ0 e he f hf hef

theorem fullStrip_thmL_S3 (N : ℕ) :
    fullStrip_statementL_S3 N StripIII.box5List (StripIII.o5List ++ L55) (box5AllList34 ++ box5Stage2)
      StripIII.m1List StripIII.NMAX_M1 StripIII.D0_M2 StripIII.M0_M2 :=
  fullStrip_of_parts_S3 N _ _ _ _ _ _ _ _ (fullStripM1_thm_S3 N) (fullStripM2_thm_S3 N) M2_nmin

/-- **T8, final S3 form**: S0's `fullStrip_statement_S0r N` (H22, H25, H26-H28 per representative) without hShared,
hRPGibbs, the k-triple and hStripMirror -/
def fullStrip_statement_S3r (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps → hBoxAll5rep N StripIII.box5Reps → hM1rep N StripIII.m1List StripIII.NMAX_M1 →
  hM2tailRep N StripIII.D0_M2 StripIII.M0_M2 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

theorem fullStrip_thm_S3r (N : ℕ) : fullStrip_statement_S3r N := by
  intro hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hB5 hH9 hI9 hO5 hBox hM1r hM2r
  exact fullStrip_thmL_S3 N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE (hBox5_of_rep N hB5) hH9 hI9
    (hO5_of_rep N hO5) (hBoxAll5_of_rep N hBox) (hM1_of_rep N hM1r) (hM2tail_of_rep N _ _ hM2r)

/-! ### The old forms, derived from the S3 forms (each proof drops premises and applies an S3 theorem) -/

theorem stripD_factor_of_S3 (N : ℕ) : stripD_factor_statement N := by
  intro hN _hS hW md hSI hSC hSp _k _hK _hR _hCF
  exact stripD_thm_S3 N hN hW md hSI hSC hSp

theorem G2_P3P3_of_S3 (N : ℕ) : G2_P3P3_statement N := by
  intro hN _hS _hSh _hRP hW md hSI hSC hH hL
  exact G2_P3P3_thm_S3 N hN hW md hSI hSC hH hL

theorem strip300_of_S3 (N : ℕ) : strip300_statement N := by
  intro hN _hS _hSh _hRP hW md hSI hSC _k _hK _hR _hCF hHub hLBu hLad hRH
  exact strip300_thm_S3 N hN hW md hSI hSC hHub hLBu hLad hRH

theorem smallN_of_S3 (N : ℕ) : smallN_statementL N (box5AllList34 ++ box5Stage2) := by
  intro hN _hS _hSh _hRP hW md hSI hSC _k _hK _hR _hCF hHub hLBu hLad hRH hRH350 _hMir hVert hD4' hBox
  exact smallN_thmL_S3 N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hBox

theorem stripIII_of_S3 (N : ℕ) : stripIII_full_statementL N StripIII.box5List (StripIII.o5List ++ L55) := by
  intro hN _hS _hSh _hRP hW md hSI hSC _k _hK _hR _hCF hHub hLBu hLad hRH hRH350 _hMir hVert hD4' hNE hB5 hH9 hI9 hO5
  exact stripIII_thmL_S3 N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hB5 hH9 hI9 hO5

theorem fullStrip_of_S3 (N : ℕ) :
    fullStrip_statementL N StripIII.box5List (StripIII.o5List ++ L55) (box5AllList34 ++ box5Stage2) StripIII.m1List
      StripIII.NMAX_M1 StripIII.D0_M2 StripIII.M0_M2 := by
  intro hN _hS _hSh _hRP hW md hSI hSC _k _hK _hR _hCF hHub hLBu hLad hRH hRH350 _hMir hVert hD4' hNE hB5 hH9 hI9 hO5
    hBox hM hT
  exact fullStrip_thmL_S3 N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hB5 hH9 hI9 hO5 hBox hM hT

theorem stripD_factor_S0_of_S3 : type_of% @stripD_factor_thm_S0 := by
  intro N hN hW md hSI hSC hSp _k _hK _hR _hCF
  exact stripD_thm_S3 N hN hW md hSI hSC hSp

theorem G2_P3P3_S0_of_S3 : type_of% @G2_P3P3_thm_S0 := by
  intro N hN _hSh _hRP hW md hSI hSC hH hL
  exact G2_P3P3_thm_S3 N hN hW md hSI hSC hH hL

theorem strip300_S0_of_S3 : type_of% @strip300_thm_S0 := by
  intro N hN _hSh _hRP hW md hSI hSC _k _hK _hR _hCF hHub hLBu hLad hRH
  exact strip300_thm_S3 N hN hW md hSI hSC hHub hLBu hLad hRH

theorem smallN_S0_of_S3 (N : ℕ) : smallN_statement_S0 N := by
  intro hN _hSh _hRP hW md hSI hSC _k _hK _hR _hCF hHub hLBu hLad hRH hRH350 _hMir hVert hD4' hBox
  exact smallN_thm_S3 N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hBox

theorem stripIII_S0r_of_S3 (N : ℕ) : stripIII_statement_S0r N := by
  intro hN _hSh _hRP hW md hSI hSC _k _hK _hR _hCF hHub hLBu hLad hRH hRH350 _hMir hVert hD4' hNE hB5 hH9 hI9 hO5
  exact stripIII_thm_S3r N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hB5 hH9 hI9 hO5

theorem fullStrip_S0r_of_S3 (N : ℕ) : fullStrip_statement_S0r N := by
  intro hN _hSh _hRP hW md hSI hSC _k _hK _hR _hCF hHub hLBu hLad hRH hRH350 _hMir hVert hD4' hNE hB5 hH9 hI9 hO5
    hBox hM1r hM2r
  exact fullStrip_thm_S3r N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hB5 hH9 hI9 hO5 hBox hM1r hM2r

theorem fullStrip_concrete_r_of_S3 : type_of% @fullStrip_thm_concrete_r := by
  intro N hN _hSh _hRP hW md hSI hSC _hR _hCF hHub hLBu hLad hRH hRH350 _hMir hVert hD4' hNE hB5 hH9 hI9 hO5
    hBox hM1r hM2r
  exact fullStrip_thm_S3r N hN hW md hSI hSC hHub hLBu hLad hRH hRH350 hVert hD4' hNE hB5 hH9 hI9 hO5 hBox hM1r hM2r

end G2S3

#print axioms G2S3.smallN_of_list_S3
#print axioms G2S3.smallN_thmL_S3
#print axioms G2S3.smallN_thm_S3
#print axioms G2S3.stripIII_full_of_lists_S3
#print axioms G2S3.stripIII_thmL_S3
#print axioms G2S3.stripIII_thm_S3r
#print axioms G2S3.fullStripM1_of_parts_S3
#print axioms G2S3.fullStripM1_thm_S3
#print axioms G2S3.fullStripM2_of_parts_S3
#print axioms G2S3.fullStripM2_thm_S3
#print axioms G2S3.fullStrip_of_parts_S3
#print axioms G2S3.fullStrip_thmL_S3
#print axioms G2S3.fullStrip_thm_S3r
#print axioms G2S3.stripD_factor_of_S3
#print axioms G2S3.G2_P3P3_of_S3
#print axioms G2S3.strip300_of_S3
#print axioms G2S3.smallN_of_S3
#print axioms G2S3.stripIII_of_S3
#print axioms G2S3.fullStrip_of_S3
#print axioms G2S3.stripD_factor_S0_of_S3
#print axioms G2S3.G2_P3P3_S0_of_S3
#print axioms G2S3.strip300_S0_of_S3
#print axioms G2S3.smallN_S0_of_S3
#print axioms G2S3.stripIII_S0r_of_S3
#print axioms G2S3.fullStrip_S0r_of_S3
#print axioms G2S3.fullStrip_concrete_r_of_S3
