/-
StripIII.Core: the combinatorial core of the Lean coverage module for the pairs without a middle-row
horizontal edge in part (f) of Theorem 6.34 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344), at J >= 300 (N = 3) and J >= 350 (N = 4). No Mathlib.
Edge codes of P_3 x P_n, the shape of a pair, the classes of the routes as Boolean predicates, and `coverage`: for N = 3 and N = 4,
every admissible pair of every P_3 x P_n lies in one of the classes.
Conventions (the paper's, with 1-based columns there and 0-based here): t_i, h_i, bb_i are the horizontal edges of rows 0, 1, 2 that
join columns i and i + 1 (code `hor r i`); a_j (top-middle) and b_j (middle-bottom) are the vertical edges of column j (codes
`ver 0 j`, `ver 1 j`). For a pair whose columns lie in {j..j'} with 2 <= j <= j' <= n - 1 (1-based), d_L = j - 2 and d_R = n - 1 - j';
with 0-based columns cmin..cmax, d_L = cmin - 1 and d_R = n - 2 - cmax, read only when no edge has a vertex in an end column.
k = m - w_e: the left edge e at position p (a horizontal edge at its left column, a vertical edge at its column),
the other edge at p + m, w_e = 2 for a horizontal and 1 for a vertical edge; separated if k >= 0, overlapping if k < 0.
The shape of a pair: the types of its left and right edge (smaller position first, ties by type rank), the offset m of their
positions, and the end gaps cmin and n - 1 - cmax, all uncapped. The classes read a pair only through its shape and, for S0, the
left-right mirror flag. `Shape.cap` caps the offset at 4 and the end gaps at 5, and every class predicate is invariant under it (the
`*_cap` lemmas, proved for every shape), so the coverage for n >= 6 is one decide over the 2880 capped shapes. n = 5 is a decide over
its 153 admissible pairs; n <= 4 is Theorem 6.34, parts (a), (c) and (d).
The records' lists `box5List` and `o5List` hold the pairs of the box records; `box5Check` and `o5Check` compare a list with its class
(o5List gains the two pairs of G55 in StripIII.FinalIIIG55), and the trial lists only exercise the checks.
-/

namespace G2Kernel.StripIII

/-- Edge codes, 0-based columns: `hor r i` joins (r, i) and (r, i + 1); `ver t j` joins (t, j) and (t + 1, j). -/
inductive ECode where
  | hor (r i : Nat)
  | ver (t j : Nat)
  deriving DecidableEq, Repr

namespace ECode

def valid (n : Nat) : ECode → Bool
  | hor r i => decide (r < 3) && decide (i + 1 < n)
  | ver t j => decide (t < 2) && decide (j < n)

/-- a middle-row horizontal edge h_i -/
def midH : ECode → Bool
  | hor r _ => r == 1
  | ver _ _ => false

/-- the two vertices of an edge as (row, column) -/
def v1 : ECode → Nat × Nat
  | hor r i => (r, i)
  | ver t j => (t, j)

def v2 : ECode → Nat × Nat
  | hor r i => (r, i + 1)
  | ver t j => (t + 1, j)

/-- the position of an edge (a horizontal edge at its left column) -/
def pos : ECode → Nat
  | hor _ i => i
  | ver _ j => j

/-- the rightmost column of an edge -/
def cmax : ECode → Nat
  | hor _ i => i + 1
  | ver _ j => j

/-- w_e: 2 for a horizontal, 1 for a vertical edge -/
def w : ECode → Nat
  | hor _ _ => 2
  | ver _ _ => 1

/-- the left-right mirror of `P_3 × P_n` (column c to n - 1 - c) -/
def lr (n : Nat) : ECode → ECode
  | hor r i => hor r (n - 2 - i)
  | ver t j => ver t (n - 1 - j)

end ECode

/-- The four edge types without a middle-row horizontal edge: t (top row), bb (bottom row), a, b (vertical). -/
inductive EType where
  | T | BB | A | B
  deriving DecidableEq, Repr

def allTypes : List EType := [.T, .BB, .A, .B]

theorem mem_allTypes (t : EType) : t ∈ allTypes := by cases t <;> decide

def etypeOf : ECode → EType
  | .hor 0 _ => .T
  | .hor _ _ => .BB
  | .ver 0 _ => .A
  | .ver _ _ => .B

def EType.rank : EType → Nat
  | .T => 0 | .BB => 1 | .A => 2 | .B => 3

def EType.isVer : EType → Bool
  | .A => true | .B => true | _ => false

def EType.w : EType → Nat
  | .T => 2 | .BB => 2 | .A => 1 | .B => 1

theorem EType.w_le (t : EType) : t.w ≤ 2 := by cases t <;> decide

/-- The shape of a pair. -/
structure Shape where
  ta : EType
  tb : EType
  off : Nat
  gl : Nat
  gr : Nat
  deriving DecidableEq, Repr

/-- the left edge of a pair: smaller position, ties by type rank -/
def leftFirst (e f : ECode) : Bool :=
  decide (e.pos < f.pos) || (decide (e.pos = f.pos) && decide ((etypeOf e).rank ≤ (etypeOf f).rank))

/-- the shape of a pair with left edge `l` and right edge `r` -/
def mkShape (n : Nat) (l r : ECode) : Shape :=
  { ta := etypeOf l, tb := etypeOf r, off := r.pos - l.pos, gl := l.pos, gr := n - 1 - max l.cmax r.cmax }

/-- the shape of the pair (e, f) in `P_3 × P_n` -/
def shapeOf (n : Nat) (e f : ECode) : Shape := if leftFirst e f then mkShape n e f else mkShape n f e

/-- the capped shape: the offset capped at 4, the end gaps at 5 -/
def Shape.cap (s : Shape) : Shape :=
  { ta := s.ta, tb := s.tb, off := min s.off 4, gl := min s.gl 5, gr := min s.gr 5 }

/-- the vertices of an edge of type `t` at position `p` -/
def typeVerts : EType → Nat → List (Nat × Nat)
  | .T, p => [(0, p), (0, p + 1)]
  | .BB, p => [(2, p), (2, p + 1)]
  | .A, q => [(0, q), (1, q)]
  | .B, q => [(1, q), (2, q)]

namespace Shape

/-- a common vertex, with the left edge at 0 and the right edge at the offset -/
def commonVertex (s : Shape) : Bool :=
  (typeVerts s.ta 0).any fun x => (typeVerts s.tb s.off).any fun y => x.1 == y.1 && x.2 == y.2

/-- the mirror pair (t_i, bb_i) of the reflection in the middle row -/
def mirrorTB (s : Shape) : Bool :=
  ((s.ta == .T && s.tb == .BB) || (s.ta == .BB && s.tb == .T)) && s.off == 0

/-- two vertical edges -/
def vv (s : Shape) : Bool := s.ta.isVer && s.tb.isVer

/-- overlapping: k = m - w_e < 0 -/
def ovl (s : Shape) : Bool := decide (s.off < s.ta.w)

/-- an edge with a vertex in an end column -/
def endTouch (s : Shape) : Bool := s.gl == 0 || s.gr == 0

/-- the end exponents d_L = cmin - 1 and d_R = n - 2 - cmax (read only when `endTouch` is false) -/
def dL (s : Shape) : Nat := s.gl - 1
def dR (s : Shape) : Nat := s.gr - 1

/-- The kinds of a pair: separated pairs of two top-row or bottom-row edges of the same type (same) or of different types (flip),
separated pairs of a horizontal and a vertical edge (mixed), overlapping pairs (joint), and two vertical edges (vert). -/
inductive Kind where
  | same | flip | mixed | joint | vert
  deriving DecidableEq, Repr

def kind (s : Shape) : Kind :=
  if s.vv then .vert
  else if s.ovl then .joint
  else if !s.ta.isVer && !s.tb.isVer then (if s.ta == s.tb then .same else .flip)
  else .mixed

/-- The threshold of the joint kind on min(d_L, d_R) (Proposition B.1): 3 at N = 3, 4 at N = 4. -/
def thrI (N : Nat) : Nat := if N == 4 then 4 else 3

/-- The thresholds of S9(h) on both end exponents, as record A gives them (code/pk21/p2/a/S_TB_PRIME_RECORD_v1.md, sha8 772b9968;
sect. 9: R5, all eight tags certified): flip 2, same 1, mixed 3 at N = 4 and 2 at N = 3, and the
joint kinds D3, D4, D4M 3 at both N. Proposition B.1's joint threshold `thrI` is 3 at N = 3 and 4 at N = 4, so at N = 4 the
classes S9(h) and S9(i) overlap on min(d_L, d_R) = 3, which the coverage allows. -/
def thrH (N : Nat) : Kind → Nat
  | .flip => 2
  | .same => 1
  | .mixed => if N == 4 then 3 else 2
  | .joint => 3
  | .vert => 0

inductive Fam where
  | D3 | D4 | D4M | none
  deriving DecidableEq, Repr

/-- the overlapping families, as the paper defines them before Proposition B.1: D3 (t_i, bb_(i+-1)), D4 (t_i, b_i), D4M (t_i, b_(i+1)), each with its flip image -/
def fam (s : Shape) : Fam :=
  if s.off == 0 then
    (match s.ta, s.tb with
     | .T, .B => .D4
     | .BB, .A => .D4
     | _, _ => .none)
  else if s.off == 1 then
    (match s.ta, s.tb with
     | .T, .BB => .D3
     | .BB, .T => .D3
     | .T, .B => .D4M
     | .BB, .A => .D4M
     | _, _ => .none)
  else .none

/-- the rows that Proposition B.1 excludes at N = 4: D3 with (d_L, d_R) in {(0,1), (1,0), (1,1)}, D4 and D4M with (1,1),
mirror images included -/
def excl (N : Nat) (s : Shape) : Bool :=
  N == 4 && !s.endTouch &&
    ((s.fam == .D3 && ((s.dL == 0 && s.dR == 1) || (s.dL == 1 && s.dR == 0) || (s.dL == 1 && s.dR == 1))) ||
     ((s.fam == .D4 || s.fam == .D4M) && s.dL == 1 && s.dR == 1))

/-- the part of S0 that the shape sees: a common vertex or a mirror pair (t_i, bb_i) -/
def s0loc (s : Shape) : Bool := s.commonVertex || s.mirrorTB

/-- NE: separated, an edge with a vertex in an end column or an end exponent below the threshold of its kind -/
def isNE (N : Nat) (s : Shape) : Bool :=
  !s.s0loc && !s.vv && !s.ovl && (s.endTouch || decide (s.dL < thrH N s.kind) || decide (s.dR < thrH N s.kind))

/-- S9(h): no end-column vertex and both end exponents at least the threshold of its kind (separated kinds and the joint kind) -/
def isH9 (N : Nat) (s : Shape) : Bool :=
  !s.s0loc && !s.vv && !s.endTouch && decide (thrH N s.kind ≤ s.dL) && decide (thrH N s.kind ≤ s.dR)

/-- S9(i) (Proposition B.1): overlapping, an end-column vertex or min(d_L, d_R) below the joint threshold, not an excluded row -/
def isI9 (N : Nat) (s : Shape) : Bool :=
  !s.s0loc && !s.vv && s.ovl && (s.endTouch || decide (s.dL < thrI N) || decide (s.dR < thrI N)) && !s.excl N

/-- O5: the overlapping pairs of the excluded rows (the box runs n6 G27, n6 G46, n7 G55) -/
def isO5 (N : Nat) (s : Shape) : Bool := !s.s0loc && !s.vv && s.ovl && s.excl N

/-- the coverage of a shape for n >= 6 (the left-right mirror pairs, also in S0, are taken apart) -/
def cover6 (N : Nat) (s : Shape) : Bool := s.s0loc || s.vv || s.isNE N || s.isH9 N || s.isI9 N || s.isO5 N

-- ------------------------------------------------------------------ the cap changes no class
theorem thrI_le (N : Nat) : thrI N ≤ 4 := by
  unfold thrI; split <;> omega

theorem thrH_le (N : Nat) (k : Kind) : thrH N k ≤ 4 := by
  cases k <;> simp only [thrH] <;> (try split) <;> omega

theorem commonVertex_two_le (s : Shape) (h : 2 ≤ s.off) : s.commonVertex = false := by
  obtain ⟨ta, tb, off, gl, gr⟩ := s
  simp only at h
  cases ta <;> cases tb <;> simp [commonVertex, typeVerts] <;> omega

theorem commonVertex_cap (s : Shape) : s.cap.commonVertex = s.commonVertex := by
  obtain ⟨ta, tb, off, gl, gr⟩ := s
  by_cases h : off < 4
  · simp only [cap, commonVertex, Nat.min_eq_left (Nat.le_of_lt h)]
  · rw [commonVertex_two_le (cap ⟨ta, tb, off, gl, gr⟩) (by simp only [cap]; omega),
      commonVertex_two_le ⟨ta, tb, off, gl, gr⟩ (by simp only; omega)]

theorem off_beq0_cap (s : Shape) : (s.cap.off == 0) = (s.off == 0) := by
  simp only [cap]; rw [Bool.eq_iff_iff, beq_iff_eq, beq_iff_eq]; omega

theorem off_beq1_cap (s : Shape) : (s.cap.off == 1) = (s.off == 1) := by
  simp only [cap]; rw [Bool.eq_iff_iff, beq_iff_eq, beq_iff_eq]; omega

theorem mirrorTB_cap (s : Shape) : s.cap.mirrorTB = s.mirrorTB := by
  obtain ⟨ta, tb, off, gl, gr⟩ := s
  simp only [mirrorTB]
  rw [off_beq0_cap ⟨ta, tb, off, gl, gr⟩]
  rfl

theorem vv_cap (s : Shape) : s.cap.vv = s.vv := rfl

theorem ovl_cap (s : Shape) : s.cap.ovl = s.ovl := by
  have := s.ta.w_le
  simp only [ovl]; rw [Bool.eq_iff_iff, decide_eq_true_eq, decide_eq_true_eq]; simp only [cap]; omega

theorem endTouch_cap (s : Shape) : s.cap.endTouch = s.endTouch := by
  simp only [endTouch, cap]
  rw [Bool.eq_iff_iff]; simp only [Bool.or_eq_true, beq_iff_eq]; omega

theorem kind_cap (s : Shape) : s.cap.kind = s.kind := by
  simp only [kind, vv_cap, ovl_cap]; rfl

theorem fam_cap (s : Shape) : s.cap.fam = s.fam := by
  obtain ⟨ta, tb, off, gl, gr⟩ := s
  simp only [fam]
  rw [off_beq0_cap ⟨ta, tb, off, gl, gr⟩, off_beq1_cap ⟨ta, tb, off, gl, gr⟩]
  rfl

theorem dL_lt_cap (s : Shape) (c : Nat) (hc : c ≤ 4) : decide (s.cap.dL < c) = decide (s.dL < c) := by
  rw [Bool.eq_iff_iff, decide_eq_true_eq, decide_eq_true_eq]; simp only [dL, cap]; omega

theorem dR_lt_cap (s : Shape) (c : Nat) (hc : c ≤ 4) : decide (s.cap.dR < c) = decide (s.dR < c) := by
  rw [Bool.eq_iff_iff, decide_eq_true_eq, decide_eq_true_eq]; simp only [dR, cap]; omega

theorem dL_ge_cap (s : Shape) (c : Nat) (hc : c ≤ 4) : decide (c ≤ s.cap.dL) = decide (c ≤ s.dL) := by
  rw [Bool.eq_iff_iff, decide_eq_true_eq, decide_eq_true_eq]; simp only [dL, cap]; omega

theorem dR_ge_cap (s : Shape) (c : Nat) (hc : c ≤ 4) : decide (c ≤ s.cap.dR) = decide (c ≤ s.dR) := by
  rw [Bool.eq_iff_iff, decide_eq_true_eq, decide_eq_true_eq]; simp only [dR, cap]; omega

theorem dL_beq_cap (s : Shape) (c : Nat) (hc : c ≤ 3) : (s.cap.dL == c) = (s.dL == c) := by
  simp only [dL, cap]; rw [Bool.eq_iff_iff, beq_iff_eq, beq_iff_eq]; omega

theorem dR_beq_cap (s : Shape) (c : Nat) (hc : c ≤ 3) : (s.cap.dR == c) = (s.dR == c) := by
  simp only [dR, cap]; rw [Bool.eq_iff_iff, beq_iff_eq, beq_iff_eq]; omega

theorem excl_cap (N : Nat) (s : Shape) : s.cap.excl N = s.excl N := by
  simp only [excl, endTouch_cap, fam_cap, dL_beq_cap s 0 (by omega), dL_beq_cap s 1 (by omega),
    dR_beq_cap s 0 (by omega), dR_beq_cap s 1 (by omega)]

theorem s0loc_cap (s : Shape) : s.cap.s0loc = s.s0loc := by
  simp only [s0loc, commonVertex_cap, mirrorTB_cap]

theorem isNE_cap (N : Nat) (s : Shape) : s.cap.isNE N = s.isNE N := by
  simp only [isNE, s0loc_cap, vv_cap, ovl_cap, endTouch_cap, kind_cap,
    dL_lt_cap s _ (thrH_le N s.kind), dR_lt_cap s _ (thrH_le N s.kind)]

theorem isH9_cap (N : Nat) (s : Shape) : s.cap.isH9 N = s.isH9 N := by
  simp only [isH9, s0loc_cap, vv_cap, endTouch_cap, kind_cap,
    dL_ge_cap s _ (thrH_le N s.kind), dR_ge_cap s _ (thrH_le N s.kind)]

theorem isI9_cap (N : Nat) (s : Shape) : s.cap.isI9 N = s.isI9 N := by
  simp only [isI9, s0loc_cap, vv_cap, ovl_cap, endTouch_cap, excl_cap,
    dL_lt_cap s _ (thrI_le N), dR_lt_cap s _ (thrI_le N)]

theorem isO5_cap (N : Nat) (s : Shape) : s.cap.isO5 N = s.isO5 N := by
  simp only [isO5, s0loc_cap, vv_cap, ovl_cap, excl_cap]

theorem cover6_cap (N : Nat) (s : Shape) : s.cap.cover6 N = s.cover6 N := by
  simp only [cover6, s0loc_cap, vv_cap, isNE_cap, isH9_cap, isI9_cap, isO5_cap]

theorem cap_bounds (s : Shape) : s.cap.off < 5 ∧ s.cap.gl < 6 ∧ s.cap.gr < 6 := by
  simp only [cap]; omega

end Shape

/-- COVERAGE OF EVERY CAPPED SHAPE, BY DECIDE, at N = 3 and N = 4. -/
theorem cover6_bounded3 : ∀ ta ∈ allTypes, ∀ tb ∈ allTypes, ∀ off, off < 5 → ∀ gl, gl < 6 → ∀ gr, gr < 6 →
    Shape.cover6 3 ⟨ta, tb, off, gl, gr⟩ = true := by decide +kernel

theorem cover6_bounded4 : ∀ ta ∈ allTypes, ∀ tb ∈ allTypes, ∀ off, off < 5 → ∀ gl, gl < 6 → ∀ gr, gr < 6 →
    Shape.cover6 4 ⟨ta, tb, off, gl, gr⟩ = true := by decide +kernel

/-- every shape is covered (n >= 6), at N = 3 and N = 4 -/
theorem cover6_all (N : Nat) (hN : N = 3 ∨ N = 4) (s : Shape) : s.cover6 N = true := by
  rw [← Shape.cover6_cap]
  obtain ⟨h1, h2, h3⟩ := Shape.cap_bounds s
  rcases hN with rfl | rfl
  · exact cover6_bounded3 _ (mem_allTypes _) _ (mem_allTypes _) _ h1 _ h2 _ h3
  · exact cover6_bounded4 _ (mem_allTypes _) _ (mem_allTypes _) _ h1 _ h2 _ h3

theorem cmax_le (c : ECode) : c.cmax ≤ c.pos + 1 := by
  cases c <;> simp only [ECode.cmax, ECode.pos] <;> omega

/-- the left edge comes first: at offset 0 its type has the smaller rank -/
theorem shapeOf_rank (n : Nat) (e f : ECode) (h : (shapeOf n e f).off = 0) :
    (shapeOf n e f).ta.rank ≤ (shapeOf n e f).tb.rank := by
  unfold shapeOf at h ⊢
  by_cases hlf : leftFirst e f = true
  · rw [ite_eq_left hlf] at h ⊢
    simp only [leftFirst, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at hlf
    simp only [mkShape] at h ⊢
    omega
  · rw [ite_eq_right hlf] at h ⊢
    simp only [leftFirst, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at hlf
    simp only [mkShape] at h ⊢
    omega

/-- n is at most the end gaps plus the offset plus 2 -/
theorem shapeOf_n_le (n : Nat) (e f : ECode) :
    n ≤ (shapeOf n e f).gl + (shapeOf n e f).off + (shapeOf n e f).gr + 2 := by
  have h1 := cmax_le e
  have h2 := cmax_le f
  unfold shapeOf
  by_cases hlf : leftFirst e f = true
  · rw [ite_eq_left hlf]
    simp only [leftFirst, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at hlf
    simp only [mkShape]
    omega
  · rw [ite_eq_right hlf]
    simp only [leftFirst, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at hlf
    simp only [mkShape]
    omega

/-- outside S0 and two vertical edges, a pair is overlapping exactly when it lies in D3, D4 or D4M (the paper's families), for every pair -/
theorem ovl_iff_fam_bounded : ∀ ta ∈ allTypes, ∀ tb ∈ allTypes, ∀ off, off < 5 → ∀ gl, gl < 6 → ∀ gr, gr < 6 →
    (off != 0 || decide (ta.rank ≤ tb.rank)) = true →
    (Shape.s0loc ⟨ta, tb, off, gl, gr⟩ || Shape.vv ⟨ta, tb, off, gl, gr⟩ ||
      (Shape.ovl ⟨ta, tb, off, gl, gr⟩ == (Shape.fam ⟨ta, tb, off, gl, gr⟩ != .none))) = true := by decide +kernel

theorem ovl_iff_fam (n : Nat) (e f : ECode) (h0 : (shapeOf n e f).s0loc = false) (hv : (shapeOf n e f).vv = false) :
    (shapeOf n e f).ovl = ((shapeOf n e f).fam != .none) := by
  have hr := shapeOf_rank n e f
  have hb := Shape.cap_bounds (shapeOf n e f)
  have key := ovl_iff_fam_bounded _ (mem_allTypes (shapeOf n e f).ta) _ (mem_allTypes (shapeOf n e f).tb) _ hb.1 _ hb.2.1 _
    hb.2.2
  have e1 : (⟨(shapeOf n e f).ta, (shapeOf n e f).tb, (shapeOf n e f).cap.off, (shapeOf n e f).cap.gl,
      (shapeOf n e f).cap.gr⟩ : Shape) = (shapeOf n e f).cap := rfl
  rw [e1, Shape.s0loc_cap, Shape.vv_cap, Shape.ovl_cap, Shape.fam_cap, h0, hv] at key
  have hpre : ((shapeOf n e f).cap.off != 0 || decide ((shapeOf n e f).ta.rank ≤ (shapeOf n e f).tb.rank)) = true := by
    simp only [bne, Shape.off_beq0_cap, Bool.or_eq_true, Bool.not_eq_true', beq_eq_false_iff_ne, decide_eq_true_eq]
    by_cases h : (shapeOf n e f).off = 0
    · exact Or.inr (hr h)
    · exact Or.inl h
  have := key hpre
  simp only [Bool.false_or, beq_iff_eq] at this
  exact this

/-- the admissible pairs: two distinct valid edges, neither a middle-row horizontal edge -/
def admissible (n : Nat) (e f : ECode) : Bool :=
  e.valid n && f.valid n && e != f && !e.midH && !f.midH

/-- the left-right mirror pairs (S0) -/
def lrMirror (n : Nat) (e f : ECode) : Bool := f == e.lr n || e == f.lr n

/-- the union of the classes, read through the shape `s` and the left-right mirror flag `lr` (see `covered_eq`) -/
def coveredS (N n : Nat) (s : Shape) (lr : Bool) : Bool :=
  decide (n ≤ 4) || (s.s0loc || lr) || (decide (2 ≤ n) && s.vv) || (decide (5 ≤ n) && !(s.s0loc || lr) && s.isNE N) ||
    ((n == 5) && !(s.s0loc || lr) && !s.vv && s.ovl) || (decide (6 ≤ n) && !(s.s0loc || lr) && s.isH9 N) ||
    (decide (6 ≤ n) && !(s.s0loc || lr) && s.isI9 N) || (decide (6 ≤ n) && !(s.s0loc || lr) && s.isO5 N)

/-- S0 (the paper's paragraph S0): a common vertex, a mirror pair (t_i, bb_i), or a left-right mirror pair -/
def s0 (n : Nat) (e f : ECode) : Bool := (shapeOf n e f).s0loc || lrMirror n e f

/-- two vertical edges, n >= 2 (Theorem 6.21) -/
def cVV (n : Nat) (e f : ECode) : Bool := decide (2 ≤ n) && (shapeOf n e f).vv

/-- NE, n >= 5, outside S0 -/
def cNE (N n : Nat) (e f : ECode) : Bool := decide (5 ≤ n) && !s0 n e f && (shapeOf n e f).isNE N

/-- the joint pairs of n = 5 outside S0 (the box orbits n5 G12, G13, G26, G27, G06, G21) -/
def cBox5 (n : Nat) (e f : ECode) : Bool :=
  (n == 5) && !s0 n e f && !(shapeOf n e f).vv && (shapeOf n e f).ovl

/-- S9(h), n >= 6, outside S0 -/
def cH9 (N n : Nat) (e f : ECode) : Bool := decide (6 ≤ n) && !s0 n e f && (shapeOf n e f).isH9 N

/-- S9(i), n >= 6, outside S0 -/
def cI9 (N n : Nat) (e f : ECode) : Bool := decide (6 ≤ n) && !s0 n e f && (shapeOf n e f).isI9 N

/-- O5, n >= 6, outside S0 -/
def cO5 (N n : Nat) (e f : ECode) : Bool := decide (6 ≤ n) && !s0 n e f && (shapeOf n e f).isO5 N

def covered (N n : Nat) (e f : ECode) : Bool := coveredS N n (shapeOf n e f) (lrMirror n e f)

/-- the classes of `covered`: n <= 4 (Theorem 6.34, parts (a), (c) and (d)) | S0 | two vertical edges | NE | the box orbits of n = 5 | S9(h) | S9(i) | O5 -/
theorem covered_eq (N n : Nat) (e f : ECode) : covered N n e f =
    (decide (n ≤ 4) || s0 n e f || cVV n e f || cNE N n e f || cBox5 n e f || cH9 N n e f || cI9 N n e f || cO5 N n e f) := rfl

theorem coveredS_ge6 (N n : Nat) (hn : 6 ≤ n) (s : Shape) (lr : Bool) (hs : s.cover6 N = true) :
    coveredS N n s lr = true := by
  have h4 : decide (n ≤ 4) = false := by simp only [decide_eq_false_iff_not]; omega
  have h2 : decide (2 ≤ n) = true := by simp only [decide_eq_true_eq]; omega
  have h5 : decide (5 ≤ n) = true := by simp only [decide_eq_true_eq]; omega
  have h6 : decide (6 ≤ n) = true := by simp only [decide_eq_true_eq]; omega
  have h55 : (n == 5) = false := by simp only [beq_eq_false_iff_ne]; omega
  simp only [coveredS, h4, h2, h5, h6, h55, Bool.false_or, Bool.true_and, Bool.false_and, Bool.or_false]
  simp only [Shape.cover6] at hs
  cases h0 : s.s0loc <;> cases hlr : lr <;> simp_all

/-- every valid edge code of `P_3 × P_n` -/
def allCodes (n : Nat) : List ECode :=
  ((List.range 3).flatMap fun r => (List.range (n - 1)).map fun i => ECode.hor r i) ++
  ((List.range 2).flatMap fun t => (List.range n).map fun j => ECode.ver t j)

theorem mem_allCodes {n : Nat} {e : ECode} (h : e.valid n = true) : e ∈ allCodes n := by
  cases e with
  | hor r i =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at h
    simp only [allCodes, List.mem_append, List.mem_flatMap, List.mem_range, List.mem_map]
    exact Or.inl ⟨r, h.1, i, by omega, rfl⟩
  | ver t j =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at h
    simp only [allCodes, List.mem_append, List.mem_flatMap, List.mem_range, List.mem_map]
    exact Or.inr ⟨t, h.1, j, h.2, rfl⟩

/-- the admissible pairs of `P_3 × P_n`, both orders -/
def allPairs (n : Nat) : List (ECode × ECode) :=
  (allCodes n).flatMap fun e => ((allCodes n).filter fun f => admissible n e f).map fun f => (e, f)

theorem mem_allPairs {n : Nat} {e f : ECode} (h : admissible n e f = true) : (e, f) ∈ allPairs n := by
  have hv : e.valid n = true ∧ f.valid n = true := by
    simp only [admissible, Bool.and_eq_true] at h
    exact ⟨h.1.1.1.1, h.1.1.1.2⟩
  simp only [allPairs, List.mem_flatMap, List.mem_map, List.mem_filter]
  exact ⟨e, mem_allCodes hv.1, f, ⟨mem_allCodes hv.2, h⟩, rfl⟩

/-- COVERAGE FOR n = 5, BY DECIDE over its admissible pairs (both orders), at N = 3 and N = 4. -/
theorem allPairs5_cover3 : (allPairs 5).all (fun p => covered 3 5 p.1 p.2) = true := by decide +kernel
theorem allPairs5_cover4 : (allPairs 5).all (fun p => covered 4 5 p.1 p.2) = true := by decide +kernel

/-- **coverage**: for N = 3 and N = 4, every admissible pair of every `P_3 × P_n` lies in one of the classes. -/
theorem coverage (N n : Nat) (hN : N = 3 ∨ N = 4) (e f : ECode) (h : admissible n e f = true) : covered N n e f = true := by
  by_cases h4 : n ≤ 4
  · have : decide (n ≤ 4) = true := by simp only [decide_eq_true_eq]; exact h4
    simp only [covered, coveredS, this, Bool.true_or]
  · by_cases h5 : n = 5
    · subst h5
      rcases hN with rfl | rfl
      · exact List.all_eq_true.mp allPairs5_cover3 (e, f) (mem_allPairs h)
      · exact List.all_eq_true.mp allPairs5_cover4 (e, f) (mem_allPairs h)
    · exact coveredS_ge6 N n (by omega) _ _ (cover6_all N hN _)

-- ------------------------------------------------------------------ the shape against the edges (for the assembly)
/-- an actual common vertex of two codes -/
def commonVertexAct (e f : ECode) : Bool :=
  [e.v1, e.v2].any fun x => [f.v1, f.v2].any fun y => x.1 == y.1 && x.2 == y.2

/-- the four kinds of valid codes without a middle-row horizontal edge -/
theorem code_cases {n : Nat} {c : ECode} (hv : c.valid n = true) (hm : c.midH = false) :
    (∃ i, c = .hor 0 i ∧ i + 1 < n) ∨ (∃ i, c = .hor 2 i ∧ i + 1 < n) ∨ (∃ j, c = .ver 0 j ∧ j < n) ∨
      (∃ j, c = .ver 1 j ∧ j < n) := by
  cases c with
  | hor r i =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at hv
    simp only [ECode.midH, beq_eq_false_iff_ne] at hm
    have : r = 0 ∨ r = 2 := by omega
    rcases this with rfl | rfl
    · exact Or.inl ⟨i, rfl, hv.2⟩
    · exact Or.inr (Or.inl ⟨i, rfl, hv.2⟩)
  | ver t j =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at hv
    have : t = 0 ∨ t = 1 := by omega
    rcases this with rfl | rfl
    · exact Or.inr (Or.inr (Or.inl ⟨j, rfl, hv.2⟩))
    · exact Or.inr (Or.inr (Or.inr ⟨j, rfl, hv.2⟩))

/-- the shape sees a common vertex exactly when the two edges share one -/
theorem commonVertex_act {n : Nat} {e f : ECode} (he : e.valid n = true) (hf : f.valid n = true)
    (hme : e.midH = false) (hmf : f.midH = false) : (shapeOf n e f).commonVertex = commonVertexAct e f := by
  rcases code_cases he hme with ⟨i, rfl, -⟩ | ⟨i, rfl, -⟩ | ⟨i, rfl, -⟩ | ⟨i, rfl, -⟩ <;>
  rcases code_cases hf hmf with ⟨i', rfl, -⟩ | ⟨i', rfl, -⟩ | ⟨i', rfl, -⟩ | ⟨i', rfl, -⟩ <;>
  unfold shapeOf <;> split <;> rename_i hlf <;>
  simp only [leftFirst, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at hlf <;>
  simp only [ECode.pos, etypeOf, EType.rank] at hlf <;>
  simp only [mkShape, Shape.commonVertex, commonVertexAct, typeVerts, etypeOf, ECode.v1, ECode.v2, ECode.pos,
    List.any_cons, List.any_nil, Bool.or_false] <;>
  rw [Bool.eq_iff_iff] <;> simp [Bool.or_eq_true, beq_iff_eq] <;> omega

/-- a mirror pair seen by the shape is a pair (t_i, bb_i) -/
theorem mirror_of_shape {n : Nat} {e f : ECode} (he : e.valid n = true) (hf : f.valid n = true)
    (hme : e.midH = false) (hmf : f.midH = false) (h : (shapeOf n e f).mirrorTB = true) :
    ∃ i, (e = .hor 0 i ∧ f = .hor 2 i) ∨ (e = .hor 2 i ∧ f = .hor 0 i) := by
  rcases code_cases he hme with ⟨i, rfl, -⟩ | ⟨i, rfl, -⟩ | ⟨i, rfl, -⟩ | ⟨i, rfl, -⟩ <;>
  rcases code_cases hf hmf with ⟨i', rfl, -⟩ | ⟨i', rfl, -⟩ | ⟨i', rfl, -⟩ | ⟨i', rfl, -⟩ <;>
  unfold shapeOf at h <;> split at h <;> rename_i hlf <;>
  simp only [leftFirst, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at hlf <;>
  simp only [ECode.pos, etypeOf, EType.rank] at hlf <;>
  simp only [mkShape, Shape.mirrorTB, etypeOf, ECode.pos, Bool.and_eq_true, Bool.or_eq_true, beq_iff_eq] at h <;>
  first
    | exact ⟨i, Or.inl ⟨rfl, by rw [ECode.hor.injEq]; exact ⟨rfl, by omega⟩⟩⟩
    | exact ⟨i, Or.inr ⟨rfl, by rw [ECode.hor.injEq]; exact ⟨rfl, by omega⟩⟩⟩
    | simp_all

theorem isVer_etypeOf {c : ECode} (h : (etypeOf c).isVer = true) : ∃ t j, c = .ver t j := by
  cases c with
  | hor r i => cases r <;> simp [etypeOf, EType.isVer] at h
  | ver t j => exact ⟨t, j, rfl⟩

/-- two vertical edges seen by the shape are two vertical codes -/
theorem vv_of_shape {n : Nat} {e f : ECode} (h : (shapeOf n e f).vv = true) :
    (∃ t j, e = .ver t j) ∧ (∃ t j, f = .ver t j) := by
  unfold shapeOf at h
  split at h
  · simp only [mkShape, Shape.vv, Bool.and_eq_true] at h
    exact ⟨isVer_etypeOf h.1, isVer_etypeOf h.2⟩
  · simp only [mkShape, Shape.vv, Bool.and_eq_true] at h
    exact ⟨isVer_etypeOf h.2, isVer_etypeOf h.1⟩

-- ------------------------------------------------------------------ the records' lists
/-- The joint pairs of P_3 x P_5 outside S0 that the box record certifies at N = 3 (J1 300) and at N = 4 (J1 350): every member
of the orbits n5 G12, G13, G26, G27, G06, G21, as code pairs. Record code/pk23/o5/records/O5_BOX_RECORD_run_20261118T013023Z_v1_2.md (sha8 3abdb733; table O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv
sha8 19945efd; manifest MANIFEST_O5_BOX_RECORD_run_20261118T013023Z_v1_2.sha256 sha8 ff08d9ce);
there "certified" means J^2 Cov >= L > 0, i.e. Cov >= L/J^2 > 0, for every J >= J1, the members as images of the
representative under the grid automorphisms.
Made from the table by the converter record2lean_v1.py, which requires certified True, VALID, DONE, rc 0
and the same members at both N. -/
def box5List : List (ECode × ECode) := [
-- source code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv sha256 19945efdec713105192a164fff21914a1da8341c1e8a2513178ea784fccf1b21; labels n5_G12,n5_G13,n5_G26,n5_G27,n5_G06,n5_G21; N 3,4
  -- n5_G12 (4 members): N=3 J1 300 L 7.361430e-03 c2 7.491487e-03 out 7a00b77f; N=4 J1 350 L 1.095971e-02 c2 1.123723e-02 out e2d9ea61
  (.hor 0 0, .ver 1 0),
  (.hor 0 3, .ver 1 4),
  (.hor 2 0, .ver 0 0),
  (.hor 2 3, .ver 0 4),
  -- n5_G13 (4 members): N=3 J1 300 L 1.168191e-03 c2 1.267694e-03 out 9bd41151; N=4 J1 350 L 1.688173e-03 c2 1.901540e-03 out 904da0ad
  (.hor 0 0, .ver 1 1),
  (.hor 0 3, .ver 1 3),
  (.hor 2 0, .ver 0 1),
  (.hor 2 3, .ver 0 3),
  -- n5_G26 (4 members): N=3 J1 300 L 3.311583e-03 c2 3.403580e-03 out 8190a414; N=4 J1 350 L 4.909004e-03 c2 5.105370e-03 out f98330c9
  (.hor 0 1, .ver 1 1),
  (.hor 0 2, .ver 1 3),
  (.hor 2 1, .ver 0 1),
  (.hor 2 2, .ver 0 3),
  -- n5_G27 (4 members): N=3 J1 300 L 2.426746e-03 c2 2.515699e-03 out 815f6a81; N=4 J1 350 L 3.583683e-03 c2 3.773548e-03 out 63f1c615
  (.hor 0 1, .ver 1 2),
  (.hor 0 2, .ver 1 2),
  (.hor 2 1, .ver 0 2),
  (.hor 2 2, .ver 0 2),
  -- n5_G06 (4 members): N=3 J1 300 L 2.474672e-03 c2 2.595769e-03 out 8d17c86e; N=4 J1 350 L 3.635425e-03 c2 3.893653e-03 out bf072a5e
  (.hor 0 0, .hor 2 1),
  (.hor 0 1, .hor 2 0),
  (.hor 0 2, .hor 2 3),
  (.hor 0 3, .hor 2 2),
  -- n5_G21 (2 members): N=3 J1 300 L 3.384966e-03 c2 3.496612e-03 out 98c93d0a; N=4 J1 350 L 5.007833e-03 c2 5.244918e-03 out 70841f60
  (.hor 0 1, .hor 2 2),
  (.hor 0 2, .hor 2 1)
-- total 22 pairs
]

/-- The O5 pairs that the box runs certify at N = 4 (J1 350), as (n, code pair): every member of the n = 6 orbits G27 and
G46, from the record of `box5List`; the two pairs of the n = 7 orbit G55 come from their own record (StripIII.FinalIIIG55, `L55`), so `o5Check o5List` is
false alone (`o5List_open_until_G55`). Made from the table by the converter record2lean_v1.py. -/
def o5List : List (Nat × ECode × ECode) := [
-- source code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv sha256 19945efdec713105192a164fff21914a1da8341c1e8a2513178ea784fccf1b21; labels n6_G27,n6_G46; N 4
  -- n6_G27 (4 members): N=4 J1 350 L 5.005397e-03 c2 5.509642e-03 out 003ede79
  (6, .hor 0 1, .hor 2 2),
  (6, .hor 0 2, .hor 2 1),
  (6, .hor 0 2, .hor 2 3),
  (6, .hor 0 3, .hor 2 2),
  -- n6_G46 (4 members): N=4 J1 350 L 3.749486e-03 c2 4.138353e-03 out d84b0faf
  (6, .hor 0 2, .ver 1 2),
  (6, .hor 0 2, .ver 1 3),
  (6, .hor 2 2, .ver 0 2),
  (6, .hor 2 2, .ver 0 3)
-- total 8 pairs
]

/-- the list check for the box orbits at n = 5: every pair of the class (either order) is in the list -/
def box5Check (L : List (ECode × ECode)) : Bool :=
  (allPairs 5).all fun p => !cBox5 5 p.1 p.2 || L.contains p || L.contains (p.2, p.1)

/-- the list check for O5 at N = 4 over n = 6, 7 (the class is empty for n >= 8 and at N = 3, `o5_empty`) -/
def o5Check (L : List (Nat × ECode × ECode)) : Bool :=
  [6, 7].all fun n => (allPairs n).all fun p => !cO5 4 n p.1 p.2 || L.contains (n, p.1, p.2) || L.contains (n, p.2, p.1)

/-- O5 is empty at N = 3, and at N = 4 for n >= 8 (the excluded rows need d_L + d_R <= 2), for every shape -/
theorem isO5_n3 (s : Shape) : s.isO5 3 = false := by
  simp [Shape.isO5, Shape.excl]

theorem isO5_small : ∀ ta ∈ allTypes, ∀ tb ∈ allTypes, ∀ off, off < 5 → ∀ gl, gl < 6 → ∀ gr, gr < 6 →
    (!Shape.isO5 4 ⟨ta, tb, off, gl, gr⟩ || (decide (gl ≤ 2) && decide (off ≤ 1) && decide (gr ≤ 2))) = true := by decide +kernel

theorem isO5_ge8 (n : Nat) (hn : 8 ≤ n) (e f : ECode) : (shapeOf n e f).isO5 4 = false := by
  cases h : (shapeOf n e f).isO5 4
  · rfl
  · exfalso
    have hb := Shape.cap_bounds (shapeOf n e f)
    have key := isO5_small _ (mem_allTypes (shapeOf n e f).ta) _ (mem_allTypes (shapeOf n e f).tb) _ hb.1 _ hb.2.1 _ hb.2.2
    have e1 : (⟨(shapeOf n e f).ta, (shapeOf n e f).tb, (shapeOf n e f).cap.off, (shapeOf n e f).cap.gl,
        (shapeOf n e f).cap.gr⟩ : Shape) = (shapeOf n e f).cap := rfl
    rw [e1, Shape.isO5_cap, h] at key
    simp only [Bool.not_true, Bool.false_or, Bool.and_eq_true, decide_eq_true_eq] at key
    have := shapeOf_n_le n e f
    simp only [Shape.cap] at key
    omega

/-- TRIAL lists computed from the classes themselves, only to exercise the checks (not certified data). -/
def trialBox5List : List (ECode × ECode) := (allPairs 5).filter fun p => cBox5 5 p.1 p.2
def trialO5List : List (Nat × ECode × ECode) :=
  [6, 7].flatMap fun n => ((allPairs n).filter fun p => cO5 4 n p.1 p.2).map fun p => (n, p.1, p.2)

theorem trial_box5Check : box5Check trialBox5List = true := by decide +kernel
theorem trial_o5Check : o5Check trialO5List = true := by decide +kernel

/-- the converse checks: every listed pair lies in its class, so a final list carries no extra pair -/
def box5InClass (L : List (ECode × ECode)) : Bool := L.all fun p => cBox5 5 p.1 p.2

def o5InClass (L : List (Nat × ECode × ECode)) : Bool := L.all fun q => cO5 4 q.1 q.2.1 q.2.2

theorem trial_box5InClass : box5InClass trialBox5List = true := by decide +kernel
theorem trial_o5InClass : o5InClass trialO5List = true := by decide +kernel
/-- the records' lists against the classes: box5List is exactly the class of the box orbits at n = 5; o5List lies
within O5 and covers its n = 6 part; o5List does not cover O5 alone (the pairs of G55 at n = 7 are in StripIII.FinalIIIG55) -/
theorem box5List_check : box5Check box5List = true := by decide +kernel
theorem box5List_inClass : box5InClass box5List = true := by decide +kernel
theorem o5List_inClass : o5InClass o5List = true := by decide +kernel
theorem o5List_n6 : (allPairs 6).all (fun p => !cO5 4 6 p.1 p.2 || o5List.contains (6, p.1, p.2) || o5List.contains (6, p.2, p.1))
    = true := by decide +kernel
theorem o5List_open_until_G55 : o5Check o5List = false := by decide +kernel

/-- COUNTS (INFO, by decide), each unordered pair in both orders: 153 admissible pairs at n = 5, of which 58 separated pairs outside S0
and two vertical edges (NE) and 22 joint pairs outside S0 (box orbits); 10 O5 pairs (n = 6, 7) at N = 4. -/
theorem count_pairs5 : (allPairs 5).length = 2 * 153 := by decide +kernel
theorem count_ne5_3 : ((allPairs 5).filter fun p => cNE 3 5 p.1 p.2).length = 2 * 58 := by decide +kernel
theorem count_ne5_4 : ((allPairs 5).filter fun p => cNE 4 5 p.1 p.2).length = 2 * 58 := by decide +kernel
theorem count_box5 : trialBox5List.length = 2 * 22 := by decide +kernel
theorem count_o5 : trialO5List.length = 2 * 10 := by decide +kernel

-- ------------------------------------------------------------------ INFO: k of the paper against the shape, n = 2..9
/-- k = m - w_e with the left edge as in `leftFirst` -/
def kAct (e f : ECode) : Int :=
  if leftFirst e f then (f.pos : Int) - e.pos - e.w else (e.pos : Int) - f.pos - f.w

def sanity (n : Nat) : Bool := (allPairs n).all fun p => (shapeOf n p.1 p.2).ovl == decide (kAct p.1 p.2 < 0)

theorem sanity_k : [2, 3, 4, 5, 6, 7, 8, 9].all sanity = true := by decide +kernel

end G2Kernel.StripIII
