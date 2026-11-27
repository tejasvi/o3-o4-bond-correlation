/-
G2S0.OrbitM2v2: version 2 of G2S0.OrbitM2 (sha8 174212c8, unchanged). Changes: the docstring of `hM2tailRep` is reworded
(AUDIT_S0_v1 item 3f), and `hM2tailRep_iff` is added. No other statement changed.
G2S0.OrbitM2 (stage S0 (c), part 2): H28 per representative, the class argument at every n, and the top theorems T6 and T8 with
H1 discharged and H26-H28 per representative.
- `StripIII.recNF`: the records' normal form of a to-do pair (the representatives of M1's rows and of M2's rows; Appendix B,
  "Pairs with a horizontal edge of the middle row": up to the two reflections the pair is (h_i, f) with f to the right of h_i).
  Controls by decide: every entry of `m1List` and of `m2Rows` is in normal form.
- `StripIII.exists_recNF`: at every n, every to-do pair outside the end orbit is one of the eight images of a normal-form pair with
  the same to-do, end-orbit and tail status (the class argument; explicit witnesses and arithmetic, no decide).
- `hM2tailRep` and `hM2tail_of_rep`; `smallN_thm_S0` (T6) and `fullStrip_thm_S0` (T8).
-/
import G2S0.Orbit
import G2S0.SphereIso

noncomputable section

namespace G2Kernel

open StripIII (ECode)

namespace StripIII

/-- the records' normal form of a to-do pair: the middle-row edge h = hor 1 i first; the partner hor 0 i (an interior same-bond pair,
with i <= n - 2 - i), hor 2 j with j > i (type t, by its flip image), ver 0 j with j >= i + 2 (type a), or hor 1 j with j >= i + 2 and
i + j + 2 < n (type h, with the end exponents d < d') -/
def recNF (n : Nat) : ECode → ECode → Bool
  | .hor 1 i, .hor 0 j => j == i && decide (i ≤ n - 2 - i)
  | .hor 1 i, .hor 2 j => decide (i < j)
  | .hor 1 i, .ver 0 j => decide (i + 2 ≤ j)
  | .hor 1 i, .hor 1 j => decide (i + 2 ≤ j) && decide (i + j + 2 < n)
  | _, _ => false

/-- control: M1's record rows and M2's finite record rows are in normal form -/
theorem m1List_recNF : m1List.all (fun q => recNF q.1 q.2.1 q.2.2) = true := by decide +kernel
theorem m2Rows_recNF : m2Rows.all (fun q => recNF q.1 q.2.1 q.2.2.1) = true := by decide +kernel

/-- the to-do predicate with the middle-row edge hor 1 i first and a horizontal partner -/
theorem todoH_hor_hor {n i r j : Nat} (h : todoH n (.hor 1 i) (.hor r j) = true) :
    (i + 1 < n ∧ r < 3 ∧ j + 1 < n ∧ ¬(r = 1 ∧ (j = i ∨ j + 1 = i ∨ j = i + 1)) ∧ ¬(r = 1 ∧ i + j + 2 = n)) := by
  simp only [todoH, ECode.valid, ECode.midH, commonVertexAct, ECode.v1, ECode.v2, lrMirror, ECode.lr, List.any_cons,
    List.any_nil, Bool.or_false, Bool.and_eq_true, Bool.or_eq_true, Bool.not_eq_true', decide_eq_true_eq, beq_iff_eq,
    bne_iff_ne, ne_eq, ECode.hor.injEq, Bool.or_eq_false_iff, Bool.and_eq_false_iff, beq_eq_false_iff_ne] at h
  omega

/-- the to-do predicate with the middle-row edge hor 1 i first and a vertical partner -/
theorem todoH_hor_ver {n i t j : Nat} (h : todoH n (.hor 1 i) (.ver t j) = true) :
    (i + 1 < n ∧ t < 2 ∧ j < n ∧ j ≠ i ∧ j ≠ i + 1) := by
  simp only [todoH, ECode.valid, ECode.midH, commonVertexAct, ECode.v1, ECode.v2, lrMirror, ECode.lr, List.any_cons,
    List.any_nil, Bool.or_false, Bool.and_eq_true, Bool.not_eq_true', decide_eq_true_eq, beq_iff_eq,
    bne_iff_ne, ne_eq, Bool.or_eq_false_iff, Bool.and_eq_false_iff, beq_eq_false_iff_ne, reduceCtorEq] at h
  omega

theorem commonVertexAct_comm (x y : ECode) : commonVertexAct x y = commonVertexAct y x := by
  unfold commonVertexAct
  generalize x.v1 = a
  generalize x.v2 = b
  generalize y.v1 = c
  generalize y.v2 = d
  obtain ⟨a1, a2⟩ := a
  obtain ⟨b1, b2⟩ := b
  obtain ⟨c1, c2⟩ := c
  obtain ⟨d1, d2⟩ := d
  rw [Bool.eq_iff_iff]
  simp only [List.any_cons, List.any_nil, Bool.or_false, Bool.or_eq_true, Bool.and_eq_true, beq_iff_eq]
  omega

theorem todoH_swap (n : Nat) (x y : ECode) : todoH n y x = todoH n x y := by
  unfold todoH lrMirror
  rw [commonVertexAct_comm y x, Bool.eq_iff_iff]
  simp only [Bool.and_eq_true, Bool.or_eq_true, Bool.not_eq_true', bne_iff_ne, ne_eq, beq_iff_eq,
    Bool.or_eq_false_iff, beq_eq_false_iff_ne, @eq_comm _ y x]
  tauto

theorem sameBondEnd_swap (n : Nat) (x y : ECode) : sameBondEnd n y x = sameBondEnd n x y := by
  unfold sameBondEnd
  rw [Bool.or_comm]

theorem orbitForms_swap {n : Nat} {a b x y : ECode} (h : (y, x) ∈ orbitForms n a b) : (x, y) ∈ orbitForms n a b := by
  simp only [orbitForms, List.mem_cons, List.mem_nil_iff, or_false, Prod.mk.injEq] at h ⊢
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact Or.inr (Or.inl ⟨h2, h1⟩)
  · exact Or.inl ⟨h2, h1⟩
  · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨h2, h1⟩)))
  · exact Or.inr (Or.inr (Or.inl ⟨h2, h1⟩))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨h2, h1⟩)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨h2, h1⟩))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨h2, h1⟩))))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨h2, h1⟩))))))

theorem todoH_hor_hor_intro {n i r j : Nat} (h1 : i + 1 < n) (h2 : r < 3) (h3 : j + 1 < n)
    (h4 : ¬(r = 1 ∧ (j = i ∨ j + 1 = i ∨ j = i + 1))) (h5 : ¬(r = 1 ∧ i + j + 2 = n)) :
    todoH n (.hor 1 i) (.hor r j) = true := by
  simp only [todoH, ECode.valid, ECode.midH, commonVertexAct, ECode.v1, ECode.v2, lrMirror, ECode.lr, List.any_cons,
    List.any_nil, Bool.or_false, Bool.and_eq_true, Bool.or_eq_true, Bool.not_eq_true', decide_eq_true_eq, beq_iff_eq,
    bne_iff_ne, ne_eq, ECode.hor.injEq, Bool.or_eq_false_iff, Bool.and_eq_false_iff, beq_eq_false_iff_ne, true_or, or_true, true_and, and_true, false_or, or_false, false_and, and_false, not_true_eq_false, not_false_eq_true]
  omega

theorem todoH_hor_ver_intro {n i t j : Nat} (h1 : i + 1 < n) (h2 : t < 2) (h3 : j < n) (h4 : j ≠ i) (h5 : j ≠ i + 1) :
    todoH n (.hor 1 i) (.ver t j) = true := by
  simp only [todoH, ECode.valid, ECode.midH, commonVertexAct, ECode.v1, ECode.v2, lrMirror, ECode.lr, List.any_cons,
    List.any_nil, Bool.or_false, Bool.and_eq_true, Bool.or_eq_true, Bool.not_eq_true', decide_eq_true_eq, beq_iff_eq,
    bne_iff_ne, ne_eq, Bool.or_eq_false_iff, Bool.and_eq_false_iff, beq_eq_false_iff_ne, reduceCtorEq, true_or, or_true, true_and, and_true, false_or, or_false, false_and, and_false, not_true_eq_false, not_false_eq_true]
  omega

theorem sbe_hor_hor_elim {n i r j : Nat} (h : sameBondEnd n (.hor 1 i) (.hor r j) = false) :
    ¬((r = 0 ∨ r = 2) ∧ j = i ∧ (i = 0 ∨ i = n - 2)) := by
  simp only [sameBondEnd, endPair, Bool.or_eq_false_iff, Bool.and_eq_false_iff, beq_eq_false_iff_ne, ne_eq,
    ECode.hor.injEq, true_or, or_true, true_and, and_true, false_or, or_false, false_and, and_false, not_true_eq_false, not_false_eq_true] at h
  omega

theorem sbe_hor_hor_intro {n i r j : Nat} (h : ¬((r = 0 ∨ r = 2) ∧ j = i ∧ (i = 0 ∨ i = n - 2))) :
    sameBondEnd n (.hor 1 i) (.hor r j) = false := by
  simp only [sameBondEnd, endPair, Bool.or_eq_false_iff, Bool.and_eq_false_iff, beq_eq_false_iff_ne, ne_eq,
    ECode.hor.injEq, true_or, or_true, true_and, and_true, false_or, or_false, false_and, and_false, not_true_eq_false, not_false_eq_true]
  omega

theorem sbe_hor_ver {n i t j : Nat} : sameBondEnd n (.hor 1 i) (.ver t j) = false := by
  simp [sameBondEnd, endPair]

theorem classOf_hor1_side {n a r b : Nat} (hr : r ≠ 1) :
    classOf n (.hor 1 a) (.hor r b) = if a ≤ b then (a, b - a, n - b - 2) else (n - 2 - a, a - b, b) := by
  have hb : (r == 1) = false := by simp [hr]
  simp [classOf, classR, ECode.midH, ECode.pos, hb]

theorem classOf_hor1_ver (n a t b : Nat) :
    classOf n (.hor 1 a) (.ver t b) = if a ≤ b then (a, b - a - 1, n - b - 1) else (n - 2 - a, a - b, b) := by
  simp [classOf, classR, ECode.midH, ECode.pos]

theorem classOf_hor1_hor1 (n a b : Nat) :
    classOf n (.hor 1 a) (.hor 1 b) = if a ≤ b then (a, b - a, n - b - 2) else (b, a - b, n - a - 2) := by
  by_cases h : a ≤ b
  · simp [classOf, classR, ECode.midH, ECode.pos, h]
  · have h' : b ≤ a := by omega
    simp [classOf, classR, ECode.midH, ECode.pos, h, h']

theorem tailClass_iff {D0 M0 x y z : Nat} : tailClass D0 M0 (x, y, z) = true ↔ (D0 + 1 ≤ x ∨ D0 + 1 ≤ z) ∨ M0 ≤ y := by
  simp [tailClass]

/-- the eight images: membership by evaluation -/
macro "s0_mem" : tactic => `(tactic| (
  simp only [orbitForms, List.mem_cons, List.mem_nil_iff, or_false, Prod.mk.injEq, ECode.flip, ECode.lr, ECode.hor.injEq,
    ECode.ver.injEq, reduceCtorEq, true_or, or_true, true_and, and_true, false_or, or_false, false_and, and_false, not_true_eq_false, not_false_eq_true]
  <;> omega))

/-- the normal form by evaluation -/
macro "s0_nf" : tactic => `(tactic| (
  simp only [recNF, decide_eq_true_eq, Bool.and_eq_true, beq_iff_eq, true_or, or_true, true_and, and_true, false_or, or_false, false_and, and_false, not_true_eq_false, not_false_eq_true] <;> omega))

/-- the tail class: rewrite both classes, decide the branches, compare -/
macro "s0_tail" : tactic => `(tactic| (
  simp only [classOf_hor1_side (by decide : (0 : Nat) ≠ 1), classOf_hor1_side (by decide : (2 : Nat) ≠ 1),
    classOf_hor1_ver, classOf_hor1_hor1] at *
  <;> split_ifs at * <;> simp only [tailClass_iff] at * <;> omega))

/-- the conclusion of the class argument for the pair (hor 1 i, y) -/
def RecNFGoal (n D0 M0 i : Nat) (y : ECode) : Prop :=
  ∃ a b : ECode, recNF n a b = true ∧ todoH n a b = true ∧ sameBondEnd n a b = false ∧
    tailClass D0 M0 (classOf n a b) = true ∧ (ECode.hor 1 i, y) ∈ orbitForms n a b

set_option maxHeartbeats 400000 in
/-- the class argument, partner in the top row -/
theorem recNF_case_t {n D0 M0 i j : Nat} (h : todoH n (.hor 1 i) (.hor 0 j) = true)
    (hs : sameBondEnd n (.hor 1 i) (.hor 0 j) = false)
    (ht : tailClass D0 M0 (classOf n (.hor 1 i) (.hor 0 j)) = true) : RecNFGoal n D0 M0 i (.hor 0 j) := by
  obtain ⟨hn1, -, hj, -, -⟩ := todoH_hor_hor h
  have hse := sbe_hor_hor_elim hs
  clear h hs
  rcases (by omega : i < j ∨ (j = i ∧ i ≤ n - 2 - i) ∨ (j = i ∧ ¬ i ≤ n - 2 - i) ∨ j < i) with
    hc | ⟨hji, hc⟩ | ⟨hji, hc⟩ | hc
  · exact ⟨.hor 1 i, .hor 2 j, by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 i, .hor 0 i, by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 (n - 2 - i), .hor 0 (n - 2 - i), by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 (n - 2 - i), .hor 2 (n - 2 - j), by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩

set_option maxHeartbeats 400000 in
/-- the class argument, partner in the bottom row -/
theorem recNF_case_bb {n D0 M0 i j : Nat} (h : todoH n (.hor 1 i) (.hor 2 j) = true)
    (hs : sameBondEnd n (.hor 1 i) (.hor 2 j) = false)
    (ht : tailClass D0 M0 (classOf n (.hor 1 i) (.hor 2 j)) = true) : RecNFGoal n D0 M0 i (.hor 2 j) := by
  obtain ⟨hn1, -, hj, -, -⟩ := todoH_hor_hor h
  have hse := sbe_hor_hor_elim hs
  clear h hs
  rcases (by omega : i < j ∨ (j = i ∧ i ≤ n - 2 - i) ∨ (j = i ∧ ¬ i ≤ n - 2 - i) ∨ j < i) with
    hc | ⟨hji, hc⟩ | ⟨hji, hc⟩ | hc
  · exact ⟨.hor 1 i, .hor 2 j, by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 i, .hor 0 i, by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 (n - 2 - i), .hor 0 (n - 2 - i), by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 (n - 2 - i), .hor 2 (n - 2 - j), by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩

set_option maxHeartbeats 400000 in
/-- the class argument, partner in the middle row -/
theorem recNF_case_h {n D0 M0 i j : Nat} (h : todoH n (.hor 1 i) (.hor 1 j) = true)
    (hs : sameBondEnd n (.hor 1 i) (.hor 1 j) = false)
    (ht : tailClass D0 M0 (classOf n (.hor 1 i) (.hor 1 j)) = true) : RecNFGoal n D0 M0 i (.hor 1 j) := by
  obtain ⟨hn1, -, hj, hcv, hlr⟩ := todoH_hor_hor h
  clear h hs
  rcases (by omega : (i + 2 ≤ j ∧ i + j + 2 < n) ∨ (i + 2 ≤ j ∧ n < i + j + 2) ∨ (j + 2 ≤ i ∧ i + j + 2 < n) ∨
      (j + 2 ≤ i ∧ n < i + j + 2)) with hc | hc | hc | hc
  · exact ⟨.hor 1 i, .hor 1 j, by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 (n - 2 - j), .hor 1 (n - 2 - i), by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 j, .hor 1 i, by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 (n - 2 - i), .hor 1 (n - 2 - j), by s0_nf, todoH_hor_hor_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_hor_intro (by omega), by s0_tail, by s0_mem⟩

set_option maxHeartbeats 400000 in
/-- the class argument, a vertical partner of the upper half (a) -/
theorem recNF_case_a {n D0 M0 i j : Nat} (h : todoH n (.hor 1 i) (.ver 0 j) = true)
    (hs : sameBondEnd n (.hor 1 i) (.ver 0 j) = false)
    (ht : tailClass D0 M0 (classOf n (.hor 1 i) (.ver 0 j)) = true) : RecNFGoal n D0 M0 i (.ver 0 j) := by
  obtain ⟨hn1, -, hj, hji, hji1⟩ := todoH_hor_ver h
  clear h hs
  rcases (by omega : i + 2 ≤ j ∨ j < i) with hc | hc
  · exact ⟨.hor 1 i, .ver 0 j, by s0_nf, todoH_hor_ver_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_ver, by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 (n - 2 - i), .ver 0 (n - 1 - j), by s0_nf, todoH_hor_ver_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_ver, by s0_tail, by s0_mem⟩

set_option maxHeartbeats 400000 in
/-- the class argument, a vertical partner of the lower half (b) -/
theorem recNF_case_b {n D0 M0 i j : Nat} (h : todoH n (.hor 1 i) (.ver 1 j) = true)
    (hs : sameBondEnd n (.hor 1 i) (.ver 1 j) = false)
    (ht : tailClass D0 M0 (classOf n (.hor 1 i) (.ver 1 j)) = true) : RecNFGoal n D0 M0 i (.ver 1 j) := by
  obtain ⟨hn1, -, hj, hji, hji1⟩ := todoH_hor_ver h
  clear h hs
  rcases (by omega : i + 2 ≤ j ∨ j < i) with hc | hc
  · exact ⟨.hor 1 i, .ver 0 j, by s0_nf, todoH_hor_ver_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_ver, by s0_tail, by s0_mem⟩
  · exact ⟨.hor 1 (n - 2 - i), .ver 0 (n - 1 - j), by s0_nf, todoH_hor_ver_intro (by omega) (by omega) (by omega) (by omega) (by omega), sbe_hor_ver, by s0_tail, by s0_mem⟩

/-- the class argument with the middle-row edge first -/
theorem exists_recNF_mid {n D0 M0 i : Nat} {y : ECode} (h : todoH n (.hor 1 i) y = true)
    (hs : sameBondEnd n (.hor 1 i) y = false) (ht : tailClass D0 M0 (classOf n (.hor 1 i) y) = true) :
    RecNFGoal n D0 M0 i y := by
  cases y with
  | hor r j =>
    have hr3 := (todoH_hor_hor h).2.1
    interval_cases r
    · exact recNF_case_t h hs ht
    · exact recNF_case_h h hs ht
    · exact recNF_case_bb h hs ht
  | ver t j =>
    have ht2 := (todoH_hor_ver h).2.1
    interval_cases t
    · exact recNF_case_a h hs ht
    · exact recNF_case_b h hs ht

/-- **the class argument at every n**: every to-do pair outside the end orbit is one of the eight images of a normal-form pair with
the same to-do, end-orbit and tail status -/
theorem exists_recNF {n D0 M0 : Nat} {x y : ECode} (h : todoH n x y = true) (hs : sameBondEnd n x y = false)
    (ht : tailClass D0 M0 (classOf n x y) = true) :
    ∃ a b : ECode, recNF n a b = true ∧ todoH n a b = true ∧ sameBondEnd n a b = false ∧
      tailClass D0 M0 (classOf n a b) = true ∧ (x, y) ∈ orbitForms n a b := by
  have hmid : x.midH = true ∨ y.midH = true := by
    simp only [todoH, Bool.and_eq_true, Bool.or_eq_true] at h
    exact h.1.1.2
  by_cases hx : x.midH = true
  · obtain ⟨i, rfl⟩ := midH_hor hx
    exact exists_recNF_mid h hs ht
  · have hy : y.midH = true := hmid.resolve_left hx
    have hx' : x.midH = false := by simpa using hx
    obtain ⟨i, rfl⟩ := midH_hor hy
    have hcl : classOf n (.hor 1 i) x = classOf n x (.hor 1 i) := by
      have hm : (ECode.hor 1 i).midH = true := rfl
      simp only [classOf, hx', hm, Bool.false_and, Bool.true_and, Bool.not_false, Bool.true_or, Bool.false_eq_true,
        ↓reduceIte]
    obtain ⟨a, b, h1, h2, h3, h4, h5⟩ := exists_recNF_mid (y := x) (by rw [todoH_swap]; exact h)
      (by rw [sameBondEnd_swap]; exact hs) (by rw [hcl]; exact ht)
    exact ⟨a, b, h1, h2, h3, h4, orbitForms_swap h5⟩

end StripIII

/-! ### H28 per representative -/

/-- **hM2tailRep** (H28 per representative; kind: restatement, equivalent to the package's H28 (`hM2tailRep_iff`); backed by
Proposition B.24: M2's certified record gives the finite checks (2)-(5) of its proof, and reaching every tail class at every n
from them needs Lemma B.23 and the covering argument of Proposition B.24, which are paper proofs, so this hypothesis is not a
finite list of record rows): for J >= jLow N and every n, every pair of edges of P_3 x P_n whose code pair is in the records'
normal form (one pair per class), a to-do pair outside the end orbit with a tail class for (D0, M0), has nonnegative covariance. -/
def hM2tailRep (N : ℕ) (D0 M0 : ℕ) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ n : ℕ, ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet,
    StripIII.recNF n (edgeCode e) (edgeCode f) = true →
    StripIII.todoH n (edgeCode e) (edgeCode f) = true → StripIII.sameBondEnd n (edgeCode e) (edgeCode f) = false →
    StripIII.tailClass D0 M0 (StripIII.classOf n (edgeCode e) (edgeCode f)) = true →
      G2pair N (strip n) (uniform J) e f

/-- **H28 from its representatives**: the normal-form pairs give the package's per-class hypothesis `hM2tail N D0 M0` at every n -/
theorem hM2tail_of_rep (N D0 M0 : ℕ) : hM2tailRep N D0 M0 → hM2tail N D0 M0 := by
  intro h J hJ n e he f hf ht hs htail
  obtain ⟨a, b, h1, h2, h3, h4, h5⟩ := StripIII.exists_recNF ht hs htail
  have hv : a.valid n = true ∧ b.valid n = true := by
    simp only [StripIII.todoH, Bool.and_eq_true] at h2
    exact ⟨h2.1.1.1.1.1, h2.1.1.1.1.2⟩
  refine G2pair_of_orbitForms hv.1 hv.2 (fun e' he' f' hf' hc1 hc2 => ?_) he hf h5
  rw [← hc1, ← hc2] at h1 h2 h3 h4
  exact h J hJ n e' he' f' hf' h1 h2 h3 h4

/-- H28 per representative is equivalent to the package's H28: one direction is `hM2tail_of_rep`; the other drops the
normal-form premise -/
theorem hM2tailRep_iff (N D0 M0 : ℕ) : hM2tailRep N D0 M0 ↔ hM2tail N D0 M0 :=
  ⟨hM2tail_of_rep N D0 M0, fun h J hJ n e he f hf _ ht hs htail => h J hJ n e he f hf ht hs htail⟩

/-! ### The top theorems T6 and T8 with H1 discharged and H26-H28 per representative -/

/-- Theorem 6.34 (e), the complete small-n theorem (T6), with H1 discharged (G2S0.SphereIso) and H26 per representative:
`smallN_statementL N (box5AllList34 ++ box5Stage2)` without the premise hSphereIso N and with hBoxAll5rep N box5Reps in place of
hBoxAll5 N (box5AllList34 ++ box5Stage2); the other premises verbatim. -/
def smallN_statement_S0 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hBoxAll5rep N StripIII.box5Reps →
    ∀ n : ℕ, 1 ≤ n → n ≤ 5 → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

theorem smallN_thm_S0 (N : ℕ) : smallN_statement_S0 N := by
  intro hN hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVSV hD4 hBox
  exact smallN_thm N hN (hSphereIso_holds N) hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVSV hD4
    (hBoxAll5_of_rep N hBox)

/-- Theorem 1.4 (i), the strip theorem for every n (T8), with H1 discharged and H26-H28 per representative:
`fullStrip_statementL N box5List (o5List ++ L55) (box5AllList34 ++ box5Stage2) m1List NMAX_M1 D0_M2 M0_M2` without the premise
hSphereIso N and with hBoxAll5rep N box5Reps, hM1rep N m1List NMAX_M1 and hM2tailRep N D0_M2 M0_M2 in place of hBoxAll5, hM1 and
hM2tail; the other premises verbatim. -/
def fullStrip_statement_S0 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5 N StripIII.box5List → hS9h N → hS9i N →
  hO5 N (StripIII.o5List ++ L55) → hBoxAll5rep N StripIII.box5Reps → hM1rep N StripIII.m1List StripIII.NMAX_M1 →
  hM2tailRep N StripIII.D0_M2 StripIII.M0_M2 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f

theorem fullStrip_thm_S0 (N : ℕ) : fullStrip_statement_S0 N := by
  intro hN hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVSV hD4 hNE hB5 hH9 hI9 hO5 hBox hM1r hM2r
  exact fullStrip_thm N hN (hSphereIso_holds N) hSh hRP hW md hSI hSC k hK hR hCF hHub hLBu hLad hRH hRH350 hMir hVSV hD4
    hNE hB5 hH9 hI9 hO5 (hBoxAll5_of_rep N hBox) (hM1_of_rep N hM1r) (hM2tail_of_rep N _ _ hM2r)

end G2Kernel

#print axioms G2Kernel.StripIII.m1List_recNF
#print axioms G2Kernel.StripIII.m2Rows_recNF
#print axioms G2Kernel.StripIII.exists_recNF
#print axioms G2Kernel.hM2tail_of_rep
#print axioms G2Kernel.hM2tailRep_iff
#print axioms G2Kernel.smallN_thm_S0
#print axioms G2Kernel.fullStrip_thm_S0
