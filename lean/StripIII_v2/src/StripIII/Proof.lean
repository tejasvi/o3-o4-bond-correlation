/-
StripIII.Proof: the assembly of part (f) of Theorem 6.34 from the named
hypotheses. `stripIII_of_lists` proves `stripIII_statementL N L5 L6` for any lists that pass the checks `box5Check` and `o5Check`;
`stripIII_thm_of_checks` gives `stripIII_statement N` once the records' lists pass them (StripIII.FinalIII and StripIII.FinalIIIG55 give the final form).
The proof: an edge of `strip n` has a valid code, the code is injective on edges and sees middle-row horizontal edges
(`edgeCode_valid`, `edgeCode_inj`, `edgeCode_midH`); `StripIII.coverage` puts the pair in a class; each class goes to its hypothesis,
S0 through `commonVertex_act`, `mirror_of_shape` and the reflection lemma `edgeCode_stripReflV`, two vertical edges through `vv_of_shape`.
`stripIII_full_of_lists` adds J <= 300 (strip300_thm) and the window 300 < J < 350 at N = 4 (hRHCover350, hShared, hD4).
-/
import StripIII.Statement
import G2Kernel.Proofs.AssemblyProof
import G2Kernel.Proofs.Strip300Proof

noncomputable section

namespace G2Kernel

open StripIII

/-! ### Edges of `P_3 × P_n` and their codes -/

theorem strip_edge_forms {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) :
    (∃ (r : Fin 3) (i j : Fin n), i.val + 1 = j.val ∧ e = s((r, i), (r, j))) ∨
    (∃ (t u : Fin 3) (j : Fin n), t.val + 1 = u.val ∧ e = s((t, j), (u, j))) := by
  induction e using Sym2.ind with
  | h p q =>
    obtain ⟨p1, p2⟩ := p
    obtain ⟨q1, q2⟩ := q
    rw [SimpleGraph.mem_edgeSet, strip, SimpleGraph.fromRel_adj] at he
    obtain ⟨-, (⟨h1, h2⟩ | ⟨h1, h2⟩) | (⟨h1, h2⟩ | ⟨h1, h2⟩)⟩ := he
    · have e1 : p1 = q1 := h1
      have e2 : p2.val + 1 = q2.val := h2
      exact Or.inl ⟨p1, p2, q2, e2, by rw [e1]⟩
    · have e1 : p2 = q2 := h1
      have e2 : p1.val + 1 = q1.val := h2
      exact Or.inr ⟨p1, q1, p2, e2, by rw [e1]⟩
    · have e1 : q1 = p1 := h1
      have e2 : q2.val + 1 = p2.val := h2
      exact Or.inl ⟨q1, q2, p2, e2, by rw [e1, Sym2.eq_swap]⟩
    · have e1 : q2 = p2 := h1
      have e2 : q1.val + 1 = p1.val := h2
      exact Or.inr ⟨q1, p1, q2, e2, by rw [e1, Sym2.eq_swap]⟩

theorem edgeCode_hor {n : ℕ} (r : Fin 3) (i j : Fin n) (h : i.val + 1 = j.val) :
    edgeCode s((r, i), (r, j)) = ECode.hor r.val i.val := by
  have hm : min i.val j.val = i.val := Nat.min_eq_left (by omega)
  simp only [edgeCode, Sym2.lift_mk, ↓reduceIte, hm]

theorem edgeCode_ver {n : ℕ} (t u : Fin 3) (j : Fin n) (h : t.val + 1 = u.val) :
    edgeCode s((t, j), (u, j)) = ECode.ver t.val j.val := by
  have hne : t ≠ u := fun h' => by rw [h'] at h; omega
  simp only [edgeCode, Sym2.lift_mk]
  rw [ite_eq_right hne, Nat.min_eq_left (by omega), Nat.min_self]

theorem edgeCode_v {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) :
    ∃ a b : Fin 3 × Fin n, e = s(a, b) ∧ (edgeCode e).v1 = (a.1.val, a.2.val) ∧ (edgeCode e).v2 = (b.1.val, b.2.val) := by
  rcases strip_edge_forms he with ⟨r, i, j, hij, rfl⟩ | ⟨t, u, j, htu, rfl⟩
  · exact ⟨(r, i), (r, j), rfl, (congrArg ECode.v1 (edgeCode_hor r i j hij)).trans rfl,
      (congrArg ECode.v2 (edgeCode_hor r i j hij)).trans (by show (r.val, i.val + 1) = (r.val, j.val); rw [hij])⟩
  · exact ⟨(t, j), (u, j), rfl, (congrArg ECode.v1 (edgeCode_ver t u j htu)).trans rfl,
      (congrArg ECode.v2 (edgeCode_ver t u j htu)).trans (by show (t.val + 1, j.val) = (u.val, j.val); rw [htu])⟩

theorem edgeCode_valid {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) : (edgeCode e).valid n = true := by
  rcases strip_edge_forms he with ⟨r, i, j, hij, rfl⟩ | ⟨t, u, j, htu, rfl⟩
  · rw [edgeCode_hor r i j hij]
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq]
    exact ⟨r.isLt, by have := j.isLt; omega⟩
  · rw [edgeCode_ver t u j htu]
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq]
    exact ⟨by have := u.isLt; omega, j.isLt⟩

theorem edgeCode_midH {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) (hm : ¬ midRowEdge n e) :
    (edgeCode e).midH = false := by
  rcases strip_edge_forms he with ⟨r, i, j, hij, rfl⟩ | ⟨t, u, j, htu, rfl⟩
  · rw [edgeCode_hor r i j hij]
    simp only [ECode.midH, beq_eq_false_iff_ne, ne_eq]
    intro hr
    exact hm ⟨i, j, hij, by rw [show r = 1 from Fin.ext hr]⟩
  · rw [edgeCode_ver t u j htu]
    rfl

theorem edgeCode_inj {n : ℕ} {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet)
    (h : edgeCode e = edgeCode f) : e = f := by
  obtain ⟨a, b, rfl, ha, hb⟩ := edgeCode_v he
  obtain ⟨c, d, rfl, hc, hd⟩ := edgeCode_v hf
  rw [h, hc, Prod.mk.injEq] at ha
  rw [h, hd, Prod.mk.injEq] at hb
  have hac : a = c := Prod.ext (Fin.ext ha.1.symm) (Fin.ext ha.2.symm)
  have hbd : b = d := Prod.ext (Fin.ext hb.1.symm) (Fin.ext hb.2.symm)
  rw [hac, hbd]

theorem common_of_act {n : ℕ} {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet)
    (h : commonVertexAct (edgeCode e) (edgeCode f) = true) : ∃ v, v ∈ e ∧ v ∈ f := by
  obtain ⟨a, b, rfl, ha, hb⟩ := edgeCode_v he
  obtain ⟨c, d, rfl, hc, hd⟩ := edgeCode_v hf
  simp only [commonVertexAct, ha, hb, hc, hd, List.any_cons, List.any_nil, Bool.or_false, Bool.or_eq_true,
    Bool.and_eq_true, beq_iff_eq] at h
  have key : ∀ x y : Fin 3 × Fin n, x.1.val = y.1.val → x.2.val = y.2.val → x = y :=
    fun x y h1 h2 => Prod.ext (Fin.ext h1) (Fin.ext h2)
  rcases h with (⟨h1, h2⟩ | ⟨h1, h2⟩) | (⟨h1, h2⟩ | ⟨h1, h2⟩)
  · exact ⟨a, Sym2.mem_mk_left a b, by rw [key a c h1 h2]; exact Sym2.mem_mk_left c d⟩
  · exact ⟨a, Sym2.mem_mk_left a b, by rw [key a d h1 h2]; exact Sym2.mem_mk_right c d⟩
  · exact ⟨b, Sym2.mem_mk_right a b, by rw [key b c h1 h2]; exact Sym2.mem_mk_left c d⟩
  · exact ⟨b, Sym2.mem_mk_right a b, by rw [key b d h1 h2]; exact Sym2.mem_mk_right c d⟩

theorem edge_of_code_hor {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) {r i : ℕ}
    (hc : edgeCode e = ECode.hor r i) :
    ∃ (rr : Fin 3) (a b : Fin n), rr.val = r ∧ a.val = i ∧ a.val + 1 = b.val ∧ e = s((rr, a), (rr, b)) := by
  rcases strip_edge_forms he with ⟨rr, a, b, hab, rfl⟩ | ⟨t, u, j, htu, rfl⟩
  · rw [edgeCode_hor rr a b hab, ECode.hor.injEq] at hc
    exact ⟨rr, a, b, hc.1, hc.2, hab, rfl⟩
  · rw [edgeCode_ver t u j htu] at hc
    cases hc

theorem edge_of_code_ver {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) {t j : ℕ}
    (hc : edgeCode e = ECode.ver t j) :
    ∃ (tt uu : Fin 3) (jj : Fin n), tt.val = t ∧ jj.val = j ∧ tt.val + 1 = uu.val ∧ e = s((tt, jj), (uu, jj)) := by
  rcases strip_edge_forms he with ⟨rr, a, b, hab, rfl⟩ | ⟨tt, uu, jj, htu, rfl⟩
  · rw [edgeCode_hor rr a b hab] at hc
    cases hc
  · rw [edgeCode_ver tt uu jj htu, ECode.ver.injEq] at hc
    exact ⟨tt, uu, jj, hc.1, hc.2, htu, rfl⟩

theorem vertical_of_form {n : ℕ} (t u : Fin 3) (j : Fin n) (h : t.val + 1 = u.val) : verticalEdge n s((t, j), (u, j)) := by
  have : (t = 0 ∧ u = 1) ∨ (t = 1 ∧ u = 2) := by omega
  rcases this with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · exact ⟨j, Or.inl rfl⟩
  · exact ⟨j, Or.inr rfl⟩

theorem strip_col_mem {n : ℕ} (t u : Fin 3) (j : Fin n) (h : t.val + 1 = u.val) : s((t, j), (u, j)) ∈ (strip n).edgeSet := by
  rw [SimpleGraph.mem_edgeSet]
  refine ⟨fun h' => ?_, Or.inl (Or.inr ⟨rfl, h⟩)⟩
  have : t.val = u.val := congrArg (fun x : Fin 3 × Fin n => x.1.val) h'
  omega

theorem map_stripReflV_hor {n : ℕ} (r : Fin 3) (i j : Fin n) :
    Sym2.map stripReflV s((r, i), (r, j)) = s((r, j.rev), (r, i.rev)) := by
  rw [Sym2.map_mk]
  exact Sym2.eq_swap

/-- the reflection in the vertical midline maps an edge to an edge, and its code to the mirrored code -/
theorem edgeCode_stripReflV {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) :
    Sym2.map stripReflV e ∈ (strip n).edgeSet ∧ edgeCode (Sym2.map stripReflV e) = (edgeCode e).lr n := by
  rcases strip_edge_forms he with ⟨r, i, j, hij, rfl⟩ | ⟨t, u, j, htu, rfl⟩
  · have hj := j.isLt
    have h' : j.rev.val + 1 = i.rev.val := by rw [Fin.val_rev, Fin.val_rev]; omega
    rw [map_stripReflV_hor r i j]
    refine ⟨strip_row_mem r j.rev i.rev (Or.inl h'), ?_⟩
    rw [edgeCode_hor r j.rev i.rev h', edgeCode_hor r i j hij]
    show ECode.hor r.val j.rev.val = ECode.hor r.val (n - 2 - i.val)
    rw [Fin.val_rev]
    congr 1
    omega
  · have hj := j.isLt
    rw [Sym2.map_mk]
    show s((t, j.rev), (u, j.rev)) ∈ (strip n).edgeSet ∧
      edgeCode s((t, j.rev), (u, j.rev)) = (edgeCode s((t, j), (u, j))).lr n
    refine ⟨strip_col_mem t u j.rev htu, ?_⟩
    rw [edgeCode_ver t u j.rev htu, edgeCode_ver t u j htu]
    show ECode.ver t.val j.rev.val = ECode.ver t.val (n - 1 - j.val)
    rw [Fin.val_rev]
    congr 1
    omega

theorem G2pair_symm_strip {N n : ℕ} {J : ℝ} {e f : Sym2 (Fin 3 × Fin n)} (h : G2pair N (strip n) (uniform J) f e) :
    G2pair N (strip n) (uniform J) e f := by
  unfold G2pair at h ⊢
  rwa [gibbsCov_comm] at h

theorem jLow_ge (N : ℕ) : (300 : ℝ) ≤ jLow N := by
  unfold jLow; split <;> norm_num

/-! ### The assembly -/

/-- **Assembly of part (f) of Theorem 6.34 for large J** for any lists of the box records that pass their checks. -/
theorem stripIII_of_lists (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (h5 : box5Check L5 = true) (h6 : o5Check L6 = true) : stripIII_statementL N L5 L6 := by
  intro hN hSh hMir hVert hD4 hNE hBox hS9h hS9i hO5 n hn J hJ e he f hf hef hme hmf
  have hJ300 : (300 : ℝ) ≤ J := le_trans (jLow_ge N) hJ
  have hJ0 : (0 : ℝ) ≤ J := le_trans (by norm_num) hJ300
  have hFerro : Ferro (strip n) (uniform J) := fun _ _ => hJ0
  have hvE := edgeCode_valid he
  have hvF := edgeCode_valid hf
  have hmE := edgeCode_midH he hme
  have hmF := edgeCode_midH hf hmf
  have hcne : edgeCode e ≠ edgeCode f := fun h => hef (edgeCode_inj he hf h)
  have hadm : admissible n (edgeCode e) (edgeCode f) = true := by
    simp only [admissible, hvE, hvF, hmE, hmF, Bool.true_and, Bool.not_false, Bool.and_true, bne_iff_ne, ne_eq]
    exact hcne
  have hcov := coverage N n hN (edgeCode e) (edgeCode f) hadm
  rw [covered_eq] at hcov
  simp only [Bool.or_eq_true] at hcov
  rcases hcov with ((((((h4 | hs0) | hvv) | hne5) | hb5) | hh9) | hi9) | ho5
  · -- n ≤ 4: Theorem 6.34, parts (a), (c) and (d)
    exact hD4 n hn (of_decide_eq_true h4) J hJ0 e he f hf hef
  · -- S0
    simp only [s0, Shape.s0loc, Bool.or_eq_true] at hs0
    rcases hs0 with (hcv | hmir) | hlr
    · rw [commonVertex_act hvE hvF hmE hmF] at hcv
      exact hSh (Fin 3 × Fin n) (strip n) (uniform J) hFerro e he f hf hef (common_of_act he hf hcv)
    · obtain ⟨i, ⟨hce, hcf⟩ | ⟨hce, hcf⟩⟩ := mirror_of_shape hvE hvF hmE hmF hmir
      · obtain ⟨r1, a1, b1, hr1, ha1, hab1, rfl⟩ := edge_of_code_hor he hce
        obtain ⟨r2, a2, b2, hr2, ha2, hab2, rfl⟩ := edge_of_code_hor hf hcf
        have e1 : r1 = 0 := Fin.ext hr1
        have e2 : r2 = 2 := Fin.ext hr2
        have e3 : a2 = a1 := Fin.ext (by omega)
        have e4 : b2 = b1 := Fin.ext (by omega)
        rw [e1, e2, e3, e4]
        exact (hMir n hn J hJ0).1 a1 b1 hab1
      · obtain ⟨r1, a1, b1, hr1, ha1, hab1, rfl⟩ := edge_of_code_hor he hce
        obtain ⟨r2, a2, b2, hr2, ha2, hab2, rfl⟩ := edge_of_code_hor hf hcf
        have e1 : r1 = 2 := Fin.ext hr1
        have e2 : r2 = 0 := Fin.ext hr2
        have e3 : a2 = a1 := Fin.ext (by omega)
        have e4 : b2 = b1 := Fin.ext (by omega)
        rw [e1, e2, e3, e4]
        exact G2pair_symm_strip ((hMir n hn J hJ0).1 a1 b1 hab1)
    · simp only [lrMirror, Bool.or_eq_true, beq_iff_eq] at hlr
      obtain ⟨hmapE, hcodeE⟩ := edgeCode_stripReflV he
      obtain ⟨hmapF, hcodeF⟩ := edgeCode_stripReflV hf
      rcases hlr with h | h
      · have hfe : f = Sym2.map stripReflV e := edgeCode_inj hf hmapE (h.trans hcodeE.symm)
        rw [hfe]
        exact (hMir n hn J hJ0).2 e he
      · have hef' : e = Sym2.map stripReflV f := edgeCode_inj he hmapF (h.trans hcodeF.symm)
        rw [hef']
        exact G2pair_symm_strip ((hMir n hn J hJ0).2 f hf)
  · -- two vertical edges: Theorem 6.21
    simp only [cVV, Bool.and_eq_true, decide_eq_true_eq] at hvv
    obtain ⟨⟨t1, j1, hc1⟩, ⟨t2, j2, hc2⟩⟩ := vv_of_shape hvv.2
    obtain ⟨tt1, uu1, jj1, -, -, h1, rfl⟩ := edge_of_code_ver he hc1
    obtain ⟨tt2, uu2, jj2, -, -, h2, rfl⟩ := edge_of_code_ver hf hc2
    exact hVert n hvv.1 J hJ300 _ he _ hf hef (vertical_of_form tt1 uu1 jj1 h1) (vertical_of_form tt2 uu2 jj2 h2)
  · -- NE
    have h5n : 5 ≤ n := by
      simp only [cNE, Bool.and_eq_true, decide_eq_true_eq] at hne5
      exact hne5.1.1
    exact hNE n h5n J hJ e f ⟨he, hf, hef, hme, hmf, hne5⟩
  · -- the joint pairs of n = 5: the box records over L5
    have hn5 : n = 5 := by
      simp only [cBox5, Bool.and_eq_true, beq_iff_eq] at hb5
      exact hb5.1.1.1
    subst hn5
    have hchk := List.all_eq_true.mp h5 _ (mem_allPairs hadm)
    simp only [hb5, Bool.not_true, Bool.false_or, Bool.or_eq_true] at hchk
    rcases hchk with hc | hc
    · exact hBox J hJ e f ⟨he, hf, hef, hme, hmf, hc⟩
    · exact G2pair_symm_strip (hBox J hJ f e ⟨hf, he, Ne.symm hef, hmf, hme, hc⟩)
  · -- S9(h)
    have h6n : 6 ≤ n := by
      simp only [cH9, Bool.and_eq_true, decide_eq_true_eq] at hh9
      exact hh9.1.1
    exact hS9h n h6n J hJ e f ⟨he, hf, hef, hme, hmf, hh9⟩
  · -- S9(i)
    have h6n : 6 ≤ n := by
      simp only [cI9, Bool.and_eq_true, decide_eq_true_eq] at hi9
      exact hi9.1.1
    exact hS9i n h6n J hJ e f ⟨he, hf, hef, hme, hmf, hi9⟩
  · -- O5: N = 4 and n ∈ {6, 7}, the box runs over L6
    have ho := ho5
    simp only [cO5, Bool.and_eq_true, decide_eq_true_eq] at ho
    obtain ⟨⟨h6n, -⟩, hiso⟩ := ho
    have hN4 : N = 4 := by
      rcases hN with rfl | rfl
      · rw [isO5_n3] at hiso
        exact absurd hiso (by decide)
      · rfl
    subst hN4
    have hn7 : n ≤ 7 := by
      by_contra hlt
      rw [isO5_ge8 n (by omega)] at hiso
      exact absurd hiso (by decide)
    have hmemN : n ∈ [6, 7] := by
      simp only [List.mem_cons]
      omega
    have hchk := List.all_eq_true.mp (List.all_eq_true.mp h6 n hmemN) _ (mem_allPairs hadm)
    simp only [ho5, Bool.not_true, Bool.false_or, Bool.or_eq_true] at hchk
    rcases hchk with hc | hc
    · exact hO5 rfl n J hJ e f ⟨he, hf, hef, hme, hmf, hc⟩
    · exact G2pair_symm_strip (hO5 rfl n J hJ f e ⟨hf, he, Ne.symm hef, hmf, hme, hc⟩)

/-- **Part (f) of Theorem 6.34 for large J** with the records' lists, once both lists pass their checks (the final lists are those of StripIII.FinalIIIG55;
there the premises hold by `decide +kernel`): each list covers its class (`box5Check`, `o5Check`) and stays within it
(`box5InClass`, `o5InClass`: a final list carries no extra pair; the proof does not need these two). -/
theorem stripIII_thm_of_checks (N : ℕ) (h5 : box5Check box5List = true) (h6 : o5Check o5List = true)
    (_h5c : box5InClass box5List = true) (_h6c : o5InClass o5List = true) : stripIII_statement N :=
  stripIII_of_lists N box5List o5List h5 h6

/-- TRIAL (INFO): the assembly with the trial lists, which the classes themselves generate (not certified data; never to be cited as
the result). -/
theorem stripIII_trial (N : ℕ) : stripIII_statementL N trialBox5List trialO5List :=
  stripIII_of_lists N trialBox5List trialO5List trial_box5Check trial_o5Check

/-- **Assembly over every coupling J >= 0** for any lists of the box records that pass their checks: J <= 300 from strip300_thm; the
window 300 < J < 350 at N = 4 from hD4 (n <= 4), hShared (the two vertical edges of one column) and hRHCover350 (the other pairs,
n >= 5); J >= jLow N from `stripIII_of_lists`. -/
theorem stripIII_full_of_lists (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (h5 : box5Check L5 = true) (h6 : o5Check L6 = true) : stripIII_full_statementL N L5 L6 := by
  intro hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVert hD4' hNE hBox hS9h hS9i hO5
    n hn J hJ0 e he f hf hef hme hmf
  by_cases hJ300 : J ≤ 300
  · exact (strip300_thm N hN hS hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH).1 n hn J hJ0 hJ300 e he f hf hef
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

/-- **Part (f) of Theorem 6.34 over every coupling J >= 0** with the records' lists, once both lists pass their four checks (as for
`stripIII_thm_of_checks`; the converse checks keep a final list free of extra pairs). -/
theorem stripIII_full_thm_of_checks (N : ℕ) (h5 : box5Check box5List = true) (h6 : o5Check o5List = true)
    (_h5c : box5InClass box5List = true) (_h6c : o5InClass o5List = true) : stripIII_full_statement N :=
  stripIII_full_of_lists N box5List o5List h5 h6

end G2Kernel
