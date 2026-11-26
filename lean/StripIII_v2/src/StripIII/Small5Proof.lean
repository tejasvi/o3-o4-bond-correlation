/-
StripIII.Small5Proof:
the assembly of the complete small-n theorem from the named hypotheses. `smallN_of_list` proves `smallN_statementL N L` for any list
that passes the check `box5AllCheck`; `smallN_thm_of_checks` gives `smallN_statement N` once the records' list passes it (that list holds 27
of the 36 orbits, `box5AllList_open_until_kit7`; StripIII.Small5Final closes the theorem). The proof: J <= 300 by strip300_thm; at N = 4 and 300 < J < 350, hD4 for
n <= 4, and at n = 5 hShared for the two vertical edges of one column and hRHCover350 for the other pairs; at J >= jLow N, hD4 for
n <= 4, and at n = 5 the case split `StripIII.cases5` on the code pair: a common vertex (hShared through `common_of_act`), a mirror
pair (t_i, bb_i) (hStripMirror), a left-right mirror pair (hStripMirror through `edgeCode_stripReflV`), two vertical edges (hVertSV),
or the class `StripIII.g5` (hBoxAll5 through the check, in either order). It uses the lemmas of StripIII.Proof.
-/
import StripIII.Small5Statement
import StripIII.Proof

noncomputable section

namespace G2Kernel

open StripIII

theorem ver_of_not_isHor {c : ECode} (h : (!c.isHor) = true) : ∃ t j, c = .ver t j := by
  cases c with
  | hor r i => simp [ECode.isHor] at h
  | ver t j => exact ⟨t, j, rfl⟩

/-- **Assembly of the complete small-n theorem** for any list of the n = 5 box records that passes the check. -/
theorem smallN_of_list (N : ℕ) (L : List (ECode × ECode)) (h : box5AllCheck L = true) : smallN_statementL N L := by
  intro hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hBox n hn hn5 J hJ0 e he f hf hef
  by_cases hJ300 : J ≤ 300
  · exact (strip300_thm N hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH).1 n hn J hJ0 hJ300 e he f hf hef
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
        · -- a common vertex: S0
          exact hSh (Fin 3 × Fin 5) (strip 5) (uniform J) hFerro e he f hf hef (common_of_act he hf hcv)
        · -- the mirror pair (t_i, bb_i): S0
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
        · -- a left-right mirror pair: S0
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

/-- **The complete small-n theorem** with the records' first list, once the list passes its check (`box5AllCheck`, false for that list:
`box5AllList_open_until_kit7`) and stays within the class (`box5AllInClass`, the in-class direction as for `box5List`; the
proof does not need it). -/
theorem smallN_thm_of_checks (N : ℕ) (h : box5AllCheck box5AllList = true) (_hc : box5AllInClass box5AllList = true) :
    smallN_statement N :=
  smallN_of_list N box5AllList h

/-- TRIAL (INFO): the assembly with the candidate list `cand5All`, all 36 orbits as the probe enumerates them (not certified
data; never to be cited as the result). -/
theorem smallN_cand (N : ℕ) : smallN_statementL N cand5All :=
  smallN_of_list N cand5All cand5All_check

end G2Kernel
