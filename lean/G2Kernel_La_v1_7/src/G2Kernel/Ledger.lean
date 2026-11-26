/-
G2Kernel.Ledger (module M8): the combinatorics of Proposition 6.7 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344):
vertex and edge names of P_3 × P_3, the dihedral group, the 12 orbits of pairs of edges, and the facts the
reduction uses (shared vertices, mirror images, degree-two corners). Every statement here is decidable.
Skeleton (step L-a, v1_1). Not compiled yet.
-/
import G2Kernel.Defs

namespace G2Kernel

/-- Vertices of `P_3 × P_3` as (row, column), row 0 on top. -/
def vN  : Fin 3 × Fin 3 := (0, 1)
def vS  : Fin 3 × Fin 3 := (2, 1)
def vE  : Fin 3 × Fin 3 := (1, 2)
def vW  : Fin 3 × Fin 3 := (1, 0)
def vC  : Fin 3 × Fin 3 := (1, 1)
def vNE : Fin 3 × Fin 3 := (0, 2)
def vSE : Fin 3 × Fin 3 := (2, 2)
def vSW : Fin 3 × Fin 3 := (2, 0)
def vNW : Fin 3 × Fin 3 := (0, 0)

/-- Rim edges `b_0, …, b_7` and spokes `s_N, s_E, s_S, s_W` (paper, Section 6). -/
def b0 : Sym2 (Fin 3 × Fin 3) := s(vS, vSE)
def b1 : Sym2 (Fin 3 × Fin 3) := s(vSE, vE)
def b2 : Sym2 (Fin 3 × Fin 3) := s(vE, vNE)
def b3 : Sym2 (Fin 3 × Fin 3) := s(vNE, vN)
def b4 : Sym2 (Fin 3 × Fin 3) := s(vN, vNW)
def b5 : Sym2 (Fin 3 × Fin 3) := s(vNW, vW)
def b6 : Sym2 (Fin 3 × Fin 3) := s(vW, vSW)
def b7 : Sym2 (Fin 3 × Fin 3) := s(vSW, vS)
def sN : Sym2 (Fin 3 × Fin 3) := s(vC, vN)
def sE : Sym2 (Fin 3 × Fin 3) := s(vC, vE)
def sS : Sym2 (Fin 3 × Fin 3) := s(vC, vS)
def sW : Sym2 (Fin 3 × Fin 3) := s(vC, vW)

/-- The twelve edges. -/
def edges33 : Finset (Sym2 (Fin 3 × Fin 3)) := {b0, b1, b2, b3, b4, b5, b6, b7, sN, sE, sS, sW}

/-- The reflections used in the proof of Proposition 6.7: in the horizontal middle line through `W, C, E`
(`reflH`), in the diagonal through `NE, C, SW` (`reflAnti`), and in the diagonal through `NW, C, SE`
(`reflDiag`). -/
def reflH (p : Fin 3 × Fin 3) : Fin 3 × Fin 3 := (Fin.rev p.1, p.2)
def reflAnti (p : Fin 3 × Fin 3) : Fin 3 × Fin 3 := (Fin.rev p.2, Fin.rev p.1)
def reflDiag (p : Fin 3 × Fin 3) : Fin 3 × Fin 3 := (p.2, p.1)

/-- The rotation by a quarter turn and the eight elements of the dihedral group. -/
def rot (p : Fin 3 × Fin 3) : Fin 3 × Fin 3 := (p.2, Fin.rev p.1)
def reflV (p : Fin 3 × Fin 3) : Fin 3 × Fin 3 := (p.1, Fin.rev p.2)
def d4 : List (Fin 3 × Fin 3 → Fin 3 × Fin 3) :=
  [id, rot, rot ∘ rot, rot ∘ rot ∘ rot, reflV, reflV ∘ rot, reflV ∘ rot ∘ rot, reflV ∘ rot ∘ rot ∘ rot]

/-- Orbit representatives in the order of the paper's proof of Proposition 6.7: five pairs sharing a vertex,
the two mirror pairs, the three pairs moved by the corner identity (at `NE`, `NW`, `SE`), and the two pairs
whose common covariance is `Cov(s_{b_0}, s_{s_N})`. -/
def reps : List (Sym2 (Fin 3 × Fin 3) × Sym2 (Fin 3 × Fin 3)) :=
  [(b0, b7), (b0, b1), (b0, sS), (sN, sS), (sN, sE), (b0, b3), (b0, b5), (b0, b2), (b0, b4), (b0, sE),
   (b0, sN), (b0, sW)]

/-- Image of an unordered pair of edges under a vertex map. -/
def pairMap (g : Fin 3 × Fin 3 → Fin 3 × Fin 3) (ef : Sym2 (Fin 3 × Fin 3) × Sym2 (Fin 3 × Fin 3)) :
    Sym2 (Fin 3 × Fin 3) × Sym2 (Fin 3 × Fin 3) :=
  (Sym2.map g ef.1, Sym2.map g ef.2)

/-- Two ordered pairs of edges are the same unordered pair. -/
def samePair (x y : Sym2 (Fin 3 × Fin 3) × Sym2 (Fin 3 × Fin 3)) : Prop :=
  (x.1 = y.1 ∧ x.2 = y.2) ∨ (x.1 = y.2 ∧ x.2 = y.1)

instance : DecidableRel samePair := fun _ _ => by unfold samePair; infer_instance

/-- Statement M8 (combinatorial part of Proposition 6.7). All conjuncts are decidable. -/
def ledger_statement : Prop :=
  -- (1) the edges of the grid are exactly the twelve named ones
  grid33.edgeFinset = edges33 ∧
  -- (2) every element of `d4` is a bijection of the vertices and a graph automorphism
  (∀ g ∈ d4, Function.Bijective g ∧ ∀ p q : Fin 3 × Fin 3, grid33.Adj p q ↔ grid33.Adj (g p) (g q)) ∧
  -- (3) every pair of distinct edges lies in the orbit of exactly one representative
  (∀ e ∈ edges33, ∀ f ∈ edges33, e ≠ f →
     (reps.filter (fun r => d4.any (fun g => decide (samePair (pairMap g r) (e, f))))).length = 1) ∧
  -- (4) the first five representatives share a vertex
  (∀ r ∈ reps.take 5, ∃ v : Fin 3 × Fin 3, v ∈ r.1 ∧ v ∈ r.2) ∧
  -- (5) mirror pairs: reflH maps b0 to b3, and reflAnti maps b0 to b5
  (Sym2.map reflH b0 = b3 ∧ Sym2.map reflAnti b0 = b5) ∧
  -- (6) the corners NE, NW, SE have degree two, with the stated neighbours
  (grid33.neighborFinset vNE = {vE, vN} ∧ grid33.neighborFinset vNW = {vN, vW} ∧
     grid33.neighborFinset vSE = {vS, vE}) ∧
  -- (7) the observables used with the corner identity do not involve the corner
  (vNE ∉ b0 ∧ vNW ∉ b0 ∧ vSE ∉ sE ∧ vSE ∉ sN) ∧
  -- (8) (b1, sE) share a vertex, and reflDiag maps the pair (b1, sN) to (b0, sW)
  (vE ∈ b1 ∧ vE ∈ sE) ∧ (Sym2.map reflDiag b1 = b0 ∧ Sym2.map reflDiag sN = sW) ∧
  -- (9) the reflections are graph automorphisms
  (∀ p q : Fin 3 × Fin 3, (grid33.Adj p q ↔ grid33.Adj (reflH p) (reflH q)) ∧
     (grid33.Adj p q ↔ grid33.Adj (reflAnti p) (reflAnti q)) ∧
     (grid33.Adj p q ↔ grid33.Adj (reflDiag p) (reflDiag q)))

end G2Kernel
