/-
StripIIIM1.HCore: the combinatorial part of M1's
statement, the pairs of edges of P_3 x P_n with a middle-row horizontal edge at 6 <= n <= NMAX_M1. No Mathlib; it uses StripIII.Core's
edge codes, `commonVertexAct` and `lrMirror`, and StripIII.Small5Core's `allPairsAll`.
- `todoH`: the to-do pairs of Appendix B (two distinct valid codes, at least one a middle-row horizontal edge, no common vertex,
  not a left-right mirror pair). The other pairs with a middle-row horizontal edge are S0 (hShared, hStripMirror).
- `sameBondEnd`: the end orbit (h_1, t_1) of Appendix B (1-based names; 0-based codes (hor 1 0, hor 0 0), (hor 1 0, hor 2 0) and
  their images at the right end, either order), closed by G2Kernel_Lb_p13's corner identity with hShared, with no record.
- `canonKey`: the least number of the four images of an unordered code pair under the reflections in the middle row (`ECode.flip`) and in
  the vertical midline (`ECode.lr`). The edge number `ECode.num` is injective on the valid codes of P_3 x P_n and below 1000 for
  n <= 11 (`num_inj_n11`), so two pairs of valid codes have one key exactly when they lie in one orbit of the group of the two
  reflections and the swap; the key is invariant under that group (`canonKey_invariant`).
- `m1Check L n`: every ordered to-do pair of P_3 x P_n outside the end orbit has its key among the keys of the entries of `L` at n;
  `m1InClass L n`: every entry of `L` at n is a to-do pair outside the end orbit; `m1Orbit L n`: every ordered pair of distinct valid
  codes with the key of an entry at n is one of the entry's eight images (`orbitForms`), the key argument above checked for `L`.
-/
import StripIII.Small5Core

namespace G2Kernel.StripIII

namespace ECode

/-- the reflection of P_3 x P_n in the middle row: row r to row 2 - r -/
def flip : ECode → ECode
  | hor r i => hor (2 - r) i
  | ver t j => ver (1 - t) j

/-- the edge number: 5 i + r for `hor r i`, 5 j + 3 + t for `ver t j` -/
def num : ECode → Nat
  | hor r i => 5 * i + r
  | ver t j => 5 * j + 3 + t

end ECode

/-- the number of an unordered pair of codes -/
def pairNum (a b : ECode) : Nat := min a.num b.num * 1000 + max a.num b.num

/-- the canonical key of a code pair of P_3 x P_n: the least number of its images under the two reflections -/
def canonKey (n : Nat) (e f : ECode) : Nat :=
  min (min (pairNum e f) (pairNum e.flip f.flip)) (min (pairNum (e.lr n) (f.lr n)) (pairNum (e.flip.lr n) (f.flip.lr n)))

/-- the to-do pairs of Appendix B: two distinct valid codes, at least one a middle-row horizontal edge, no common vertex, not a
left-right mirror pair -/
def todoH (n : Nat) (e f : ECode) : Bool :=
  e.valid n && f.valid n && e != f && (e.midH || f.midH) && !commonVertexAct e f && !lrMirror n e f

/-- the pairs (h, t) of the end orbit with the middle-row edge first: h = h_1 with t = t_1 or bb_1, or h = h_{n-1} with t = t_{n-1} or
bb_{n-1} (1-based names, 0-based codes) -/
def endPair (n : Nat) (h t : ECode) : Bool :=
  (h == .hor 1 0 && (t == .hor 0 0 || t == .hor 2 0)) ||
    (h == .hor 1 (n - 2) && (t == .hor 0 (n - 2) || t == .hor 2 (n - 2)))

/-- the end orbit of the same-bond pairs, either order -/
def sameBondEnd (n : Nat) (e f : ECode) : Bool := endPair n e f || endPair n f e

/-- the keys of the entries of `L` at n -/
def m1Keys (L : List (Nat × ECode × ECode)) (n : Nat) : List Nat :=
  (L.filter fun q => q.1 == n).map fun q => canonKey n q.2.1 q.2.2

/-- the check at n: every ordered to-do pair of P_3 x P_n outside the end orbit has its key among the keys of `L` at n -/
def m1Check (L : List (Nat × ECode × ECode)) (n : Nat) : Bool :=
  (allPairsAll n).all fun p => !(todoH n p.1 p.2 && !sameBondEnd n p.1 p.2) || (m1Keys L n).contains (canonKey n p.1 p.2)

/-- the converse at n: every entry of `L` at n is a to-do pair outside the end orbit -/
def m1InClass (L : List (Nat × ECode × ECode)) (n : Nat) : Bool :=
  (L.filter fun q => q.1 == n).all fun q => todoH n q.2.1 q.2.2 && !sameBondEnd n q.2.1 q.2.2

/-- the eight images of an ordered code pair of P_3 x P_n under the swap and the two reflections -/
def orbitForms (n : Nat) (e f : ECode) : List (ECode × ECode) :=
  [(e, f), (f, e), (e.flip, f.flip), (f.flip, e.flip), (e.lr n, f.lr n), (f.lr n, e.lr n), (e.flip.lr n, f.flip.lr n),
    (f.flip.lr n, e.flip.lr n)]

/-- the key check at n: every ordered pair of distinct valid codes that has the key of an entry of `L` at n is an image of that entry,
so the pairs with the key of an entry are exactly the members of its orbit (with `canonKey_invariant`) -/
def m1Orbit (L : List (Nat × ECode × ECode)) (n : Nat) : Bool :=
  (allPairsAll n).all fun p => (L.filter fun q => q.1 == n).all fun q =>
    canonKey n q.2.1 q.2.2 != canonKey n p.1 p.2 || (orbitForms n q.2.1 q.2.2).contains p

/-- the number of orbits of to-do pairs at n: the ordered to-do pairs (a, b) with a.num < b.num whose number is their key, one per
orbit (the key of an orbit is the least number of its members) -/
def orbitCount (n : Nat) : Nat :=
  ((allPairsAll n).filter fun p => todoH n p.1 p.2 && decide (p.1.num < p.2.num) && pairNum p.1 p.2 == canonKey n p.1 p.2).length

/-- the edge number is injective on the valid codes of P_3 x P_11 and below 1000 (so also for every n <= 11) -/
theorem num_inj_n11 : (allCodes 11).all (fun a => decide (a.num < 1000) && (allCodes 11).all fun b => a == b || a.num != b.num) = true := by
  decide +kernel

/-- the key is invariant under the swap and the two reflections, on every ordered pair of distinct valid codes, n = 6..11 -/
theorem canonKey_invariant : [6, 7, 8, 9, 10, 11].all (fun n => (allPairsAll n).all fun p =>
    canonKey n p.2 p.1 == canonKey n p.1 p.2 && canonKey n p.1.flip p.2.flip == canonKey n p.1 p.2 &&
      canonKey n (p.1.lr n) (p.2.lr n) == canonKey n p.1 p.2) = true := by
  decide +kernel

/-- TRIAL (INFO): the list of every ordered to-do pair outside the end orbit at n, which the class itself generates (not record data;
never to be cited as a result); it exercises the two checks -/
def trialM1 (n : Nat) : List (Nat × ECode × ECode) :=
  ((allPairsAll n).filter fun p => todoH n p.1 p.2 && !sameBondEnd n p.1 p.2).map fun p => (n, p.1, p.2)

theorem trialM1_checks : m1Check (trialM1 6) 6 = true ∧ m1InClass (trialM1 6) 6 = true ∧ m1Check (trialM1 6) 7 = false := by
  decide +kernel

end G2Kernel.StripIII
