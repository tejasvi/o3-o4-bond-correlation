/-
StripIIIM2.M2Core: the combinatorial part of M2's
statement, the pairs with a middle-row horizontal edge at every n >= 12. No Mathlib; it uses StripIIIM1.HCore's to-do predicate `todoH`
and end orbit `sameBondEnd`.
- `classOf n e f`: the class (d + 1, m, d' + 1) of a to-do pair (Appendix B: (T, d, m, d'), d >= -1 h's end exponent, d' >= -1 the
  partner's, m the gap), from the codes: h = hor 1 i is the middle-row edge (the left one of two), and a partner to h's left is read in
  the left-right mirror. Vertical partner ver t j: (i, j - i - 1, n - j - 1) for j >= i, (n - 2 - i, i - j, j) for j < i; row partner
  hor r j: (i, j - i, n - j - 2) for j >= i, (n - 2 - i, i - j, j) for j < i.
- `class_sum`: for every n and every to-do pair, (d + 1) + m + (d' + 1) + 2 = n, so n = d + m + d' + 4 (Appendix B).
- `tailClass D0 M0`: d >= D0, d' >= D0 or m >= M0: the classes of Lemma B.23 (a) and (b) and of Proposition B.18's envelope orbits.
- `tail_cover`: for n >= 2 D0 + M0 + 2 every to-do pair has a tail class (a class with d, d' < D0 and m < M0 has n <= n0 = 2 D0 + M0 + 1).
- Controls by decide: `classKey` (the two end exponents as a set, and m) is invariant under the swap and both reflections, n = 6..14;
  the record rows' (d + 1, m, d' + 1) are checked against `classOf` in StripIIIM2.M2Check.
-/
import StripIIIM1.HCore

namespace G2Kernel.StripIII

/-- the class of a pair (h, p) with h = hor 1 i: (d + 1, m, d' + 1) -/
def classR (n : Nat) (h p : ECode) : Nat × Nat × Nat :=
  match h, p with
  | .hor _ i, .ver _ j => if i ≤ j then (i, j - i - 1, n - j - 1) else (n - 2 - i, i - j, j)
  | .hor _ i, .hor _ j => if i ≤ j then (i, j - i, n - j - 2) else (n - 2 - i, i - j, j)
  | _, _ => (0, 0, 0)

/-- the class (d + 1, m, d' + 1) of a to-do pair: h is its middle-row edge, the left one of two -/
def classOf (n : Nat) (e f : ECode) : Nat × Nat × Nat :=
  if e.midH && (!f.midH || decide (e.pos ≤ f.pos)) then classR n e f else classR n f e

/-- the tail classes for (D0, M0): d >= D0, d' >= D0 or m >= M0 -/
def tailClass (D0 M0 : Nat) (c : Nat × Nat × Nat) : Bool :=
  decide (D0 + 1 ≤ c.1) || decide (D0 + 1 ≤ c.2.2) || decide (M0 ≤ c.2.1)

/-- the two end exponents as a set, and m: what a class's tail condition reads -/
def classKey (c : Nat × Nat × Nat) : Nat × Nat × Nat := (min c.1 c.2.2, max c.1 c.2.2, c.2.1)

theorem midH_hor {c : ECode} (h : c.midH = true) : ∃ i, c = .hor 1 i := by
  cases c with
  | hor r i =>
    simp only [ECode.midH, beq_iff_eq] at h
    exact ⟨i, by rw [h]⟩
  | ver t j => simp [ECode.midH] at h

theorem cv_hor_ver {i t j : Nat} (ht : t < 2) (h : commonVertexAct (.hor 1 i) (.ver t j) = false) : j ≠ i := by
  simp only [commonVertexAct, ECode.v1, ECode.v2, List.any_cons, List.any_nil, Bool.or_false, Bool.or_eq_false_iff,
    Bool.and_eq_false_iff, beq_eq_false_iff_ne, ne_eq] at h
  omega

theorem cv_ver_hor {i t j : Nat} (ht : t < 2) (h : commonVertexAct (.ver t j) (.hor 1 i) = false) : j ≠ i := by
  simp only [commonVertexAct, ECode.v1, ECode.v2, List.any_cons, List.any_nil, Bool.or_false, Bool.or_eq_false_iff,
    Bool.and_eq_false_iff, beq_eq_false_iff_ne, ne_eq] at h
  omega

/-- the class sum for h = hor 1 i and a valid partner with no common vertex (either order of the vertex test) -/
theorem classR_sum {n i : Nat} {p : ECode} (hi : i + 1 < n) (hp : p.valid n = true)
    (hcv : commonVertexAct (.hor 1 i) p = false ∨ commonVertexAct p (.hor 1 i) = false) :
    (classR n (.hor 1 i) p).1 + (classR n (.hor 1 i) p).2.1 + (classR n (.hor 1 i) p).2.2 + 2 = n := by
  cases p with
  | hor r j =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at hp
    simp only [classR]
    split <;> (try dsimp only) <;> omega
  | ver t j =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at hp
    have hj : j ≠ i := hcv.elim (cv_hor_ver hp.1) (cv_ver_hor hp.1)
    simp only [classR]
    split <;> (try dsimp only) <;> omega

/-- **n = d + m + d' + 4** for every to-do pair, at every n -/
theorem class_sum {n : Nat} {e f : ECode} (h : todoH n e f = true) :
    (classOf n e f).1 + (classOf n e f).2.1 + (classOf n e f).2.2 + 2 = n := by
  simp only [todoH, Bool.and_eq_true, Bool.not_eq_true'] at h
  obtain ⟨⟨⟨⟨⟨hve, hvf⟩, -⟩, hmid⟩, hcv⟩, -⟩ := h
  unfold classOf
  split
  · rename_i hsel
    have hem : e.midH = true := by
      cases hem' : e.midH <;> simp_all
    obtain ⟨i, rfl⟩ := midH_hor hem
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at hve
    exact classR_sum hve.2 hvf (Or.inl hcv)
  · rename_i hsel
    have hfm : f.midH = true := by
      cases hem : e.midH <;> cases hfm' : f.midH <;> simp_all
    obtain ⟨i, rfl⟩ := midH_hor hfm
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at hvf
    exact classR_sum hvf.2 hve (Or.inr hcv)

/-- **the covering**: for n >= 2 D0 + M0 + 2 every to-do pair has a tail class -/
theorem tail_cover {n D0 M0 : Nat} {e f : ECode} (h : todoH n e f = true) (hn : 2 * D0 + M0 + 2 ≤ n) :
    tailClass D0 M0 (classOf n e f) = true := by
  have hs := class_sum h
  simp only [tailClass, Bool.or_eq_true, decide_eq_true_eq]
  omega

/-- control: the class key is invariant under the swap and both reflections on every to-do pair, n = 6..14 -/
theorem classKey_invariant : [6, 7, 8, 9, 10, 11, 12, 13, 14].all (fun n => (allPairsAll n).all fun p =>
    !todoH n p.1 p.2 || (classKey (classOf n p.2 p.1) == classKey (classOf n p.1 p.2) &&
      classKey (classOf n p.1.flip p.2.flip) == classKey (classOf n p.1 p.2) &&
      classKey (classOf n (p.1.lr n) (p.2.lr n)) == classKey (classOf n p.1 p.2))) = true := by
  decide +kernel

end G2Kernel.StripIII
