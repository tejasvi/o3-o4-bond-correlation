/-
G2S1.Ladder (stage H16): the named hypothesis H16, `hLadder N` (G2Kernel/Strip300.lean), is a theorem for
N = 3 and N = 4 (STATEMENTS_H16_v1.md §2).
The ladder P_3 × P_2 is `strip 2`, with vertex (r, j) in row r and column j. It has 7 edges: top a1 = s((0,0),(1,0)),
a2 = s((0,0),(0,1)), a3 = s((0,1),(1,1)); middle rung m = s((1,0),(1,1)); bottom b1 = s((2,0),(1,0)),
b2 = s((2,0),(2,1)), b3 = s((2,1),(1,1)). The four corners (0,0), (0,1), (2,0), (2,1) have degree 2.
- The 10 pairs of distinct edges with a common vertex: Theorem 3.2 (H6, S3's `G2S3.hShared_holds3/4`).
- The 11 pairs of disjoint edges: at uniform coupling, Lemma 6.2 (the corner identity: the package's `corner_step` with
  S0's `hSphereIso_holds`) exchanges the two edges at a corner in the covariance with any edge that avoids the corner.
  One or two such steps reach a pair with a common vertex.
-/
import G2S3.Dunlop
import G2Kernel.Proofs.AssemblyProof
import G2S0.SphereIso

noncomputable section

namespace G2Kernel

/-! ### The seven edges of `strip 2` -/

abbrev ladA1 : Sym2 (Fin 3 × Fin 2) := s(((0 : Fin 3), (0 : Fin 2)), ((1 : Fin 3), (0 : Fin 2)))
abbrev ladA2 : Sym2 (Fin 3 × Fin 2) := s(((0 : Fin 3), (0 : Fin 2)), ((0 : Fin 3), (1 : Fin 2)))
abbrev ladA3 : Sym2 (Fin 3 × Fin 2) := s(((0 : Fin 3), (1 : Fin 2)), ((1 : Fin 3), (1 : Fin 2)))
abbrev ladM : Sym2 (Fin 3 × Fin 2) := s(((1 : Fin 3), (0 : Fin 2)), ((1 : Fin 3), (1 : Fin 2)))
abbrev ladB1 : Sym2 (Fin 3 × Fin 2) := s(((2 : Fin 3), (0 : Fin 2)), ((1 : Fin 3), (0 : Fin 2)))
abbrev ladB2 : Sym2 (Fin 3 × Fin 2) := s(((2 : Fin 3), (0 : Fin 2)), ((2 : Fin 3), (1 : Fin 2)))
abbrev ladB3 : Sym2 (Fin 3 × Fin 2) := s(((2 : Fin 3), (1 : Fin 2)), ((1 : Fin 3), (1 : Fin 2)))

/-- Every edge of `strip 2` is one of the seven. -/
theorem ladder_edge_cases {e : Sym2 (Fin 3 × Fin 2)} (he : e ∈ (strip 2).edgeSet) :
    e = ladA1 ∨ e = ladA2 ∨ e = ladA3 ∨ e = ladM ∨ e = ladB1 ∨ e = ladB2 ∨ e = ladB3 := by
  induction e using Sym2.ind with
  | h p q =>
    have key : ∀ p q : Fin 3 × Fin 2, s(p, q) ∈ (strip 2).edgeSet →
        s(p, q) = ladA1 ∨ s(p, q) = ladA2 ∨ s(p, q) = ladA3 ∨ s(p, q) = ladM ∨ s(p, q) = ladB1 ∨
          s(p, q) = ladB2 ∨ s(p, q) = ladB3 := by
      decide
    exact key p q he

/-- A covariance identity in the first slot moves the predicate of display (1). -/
theorem ladder_tr {N : ℕ} {J : ℝ} {e e' f : Sym2 (Fin 3 × Fin 2)}
    (h : gibbsCov N (strip 2) (uniform J) (bond e) (bond f) = gibbsCov N (strip 2) (uniform J) (bond e') (bond f))
    (h' : G2pair N (strip 2) (uniform J) e' f) : G2pair N (strip 2) (uniform J) e f := by
  unfold G2pair at h' ⊢
  rw [h]
  exact h'

/-- The two orders of a pair. -/
theorem ladder_swap {N : ℕ} {J : ℝ} {e f : Sym2 (Fin 3 × Fin 2)}
    (h : G2pair N (strip 2) (uniform J) f e) : G2pair N (strip 2) (uniform J) e f := by
  unfold G2pair at h ⊢
  rw [gibbsCov_comm]
  exact h

/-- H16 from H6 (Theorem 3.2 for edge pairs with a common vertex) and Lemma 6.2 (with `hSphereIso`). -/
theorem ladder_of_shared {N : ℕ} (hS : hSphereIso N) (h6 : hShared N) : hLadder N := by
  intro J hJ e he f hf hef
  have hF : Ferro (strip 2) (uniform J) := fun _ _ => hJ
  have H : ∀ a ∈ (strip 2).edgeSet, ∀ b ∈ (strip 2).edgeSet, a ≠ b → (∃ v, v ∈ a ∧ v ∈ b) →
      G2pair N (strip 2) (uniform J) a b :=
    fun a ha b hb hab hv => h6 (Fin 3 × Fin 2) (strip 2) (uniform J) hF a ha b hb hab hv
  -- Lemma 6.2 at the four corners
  have t00 : ∀ g, ((0 : Fin 3), (0 : Fin 2)) ∉ g →
      gibbsCov N (strip 2) (uniform J) (bond ladA1) (bond g)
        = gibbsCov N (strip 2) (uniform J) (bond ladA2) (bond g) :=
    fun g hg => corner_step hS J 0 (0 : Fin 2) 1 (by decide) (by decide) g hg
  have t01 : ∀ g, ((0 : Fin 3), (1 : Fin 2)) ∉ g →
      gibbsCov N (strip 2) (uniform J) (bond ladA3) (bond g)
        = gibbsCov N (strip 2) (uniform J) (bond ladA2) (bond g) :=
    fun g hg => (corner_step hS J 0 (1 : Fin 2) 0 (by decide) (by decide) g hg).trans (by rw [Sym2.eq_swap])
  have t20 : ∀ g, ((2 : Fin 3), (0 : Fin 2)) ∉ g →
      gibbsCov N (strip 2) (uniform J) (bond ladB1) (bond g)
        = gibbsCov N (strip 2) (uniform J) (bond ladB2) (bond g) :=
    fun g hg => corner_step hS J 2 (0 : Fin 2) 1 (by decide) (by decide) g hg
  have t21 : ∀ g, ((2 : Fin 3), (1 : Fin 2)) ∉ g →
      gibbsCov N (strip 2) (uniform J) (bond ladB3) (bond g)
        = gibbsCov N (strip 2) (uniform J) (bond ladB2) (bond g) :=
    fun g hg => (corner_step hS J 2 (1 : Fin 2) 0 (by decide) (by decide) g hg).trans (by rw [Sym2.eq_swap])
  -- the pairs of disjoint edges, one or two corner steps each
  have c1 : G2pair N (strip 2) (uniform J) ladA1 ladA3 :=
    ladder_tr (t00 ladA3 (by decide)) (H ladA2 (by decide) ladA3 (by decide) (by decide) (by decide))
  have c2 : G2pair N (strip 2) (uniform J) ladA1 ladB2 :=
    ladder_swap (ladder_tr (t20 ladA1 (by decide)).symm
      (H ladB1 (by decide) ladA1 (by decide) (by decide) (by decide)))
  have c7 : G2pair N (strip 2) (uniform J) ladA2 ladB3 :=
    ladder_tr (t01 ladB3 (by decide)).symm (H ladA3 (by decide) ladB3 (by decide) (by decide) (by decide))
  have c3 : G2pair N (strip 2) (uniform J) ladA1 ladB3 := ladder_tr (t00 ladB3 (by decide)) c7
  have c4 : G2pair N (strip 2) (uniform J) ladA2 ladM :=
    ladder_tr (t00 ladM (by decide)).symm (H ladA1 (by decide) ladM (by decide) (by decide) (by decide))
  have c5 : G2pair N (strip 2) (uniform J) ladA2 ladB1 :=
    ladder_tr (t00 ladB1 (by decide)).symm (H ladA1 (by decide) ladB1 (by decide) (by decide) (by decide))
  have c6 : G2pair N (strip 2) (uniform J) ladA2 ladB2 := ladder_tr (t00 ladB2 (by decide)).symm c2
  have c8 : G2pair N (strip 2) (uniform J) ladA3 ladA1 :=
    ladder_tr (t01 ladA1 (by decide)) (H ladA2 (by decide) ladA1 (by decide) (by decide) (by decide))
  have c9 : G2pair N (strip 2) (uniform J) ladA3 ladB1 := ladder_tr (t01 ladB1 (by decide)) c5
  have c10 : G2pair N (strip 2) (uniform J) ladA3 ladB2 :=
    ladder_swap (ladder_tr (t21 ladA3 (by decide)).symm
      (H ladB3 (by decide) ladA3 (by decide) (by decide) (by decide)))
  have c12 : G2pair N (strip 2) (uniform J) ladM ladB2 :=
    ladder_swap (ladder_tr (t20 ladM (by decide)).symm
      (H ladB1 (by decide) ladM (by decide) (by decide) (by decide)))
  have c15 : G2pair N (strip 2) (uniform J) ladB1 ladB3 :=
    ladder_tr (t20 ladB3 (by decide)) (H ladB2 (by decide) ladB3 (by decide) (by decide) (by decide))
  have c22 : G2pair N (strip 2) (uniform J) ladB3 ladB1 :=
    ladder_tr (t21 ladB1 (by decide)) (H ladB2 (by decide) ladB1 (by decide) (by decide) (by decide))
  by_cases hv : ∃ v, v ∈ e ∧ v ∈ f
  · exact H e he f hf hef hv
  rcases ladder_edge_cases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    rcases ladder_edge_cases hf with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    first
    | exact absurd rfl hef
    | exact absurd (by decide) hv
    | skip
  -- the 22 ordered pairs of disjoint edges, in the order of the case split
  · exact c1                -- a1 a3
  · exact c2                -- a1 b2
  · exact c3                -- a1 b3
  · exact c4                -- a2 m
  · exact c5                -- a2 b1
  · exact c6                -- a2 b2
  · exact c7                -- a2 b3
  · exact c8                -- a3 a1
  · exact c9                -- a3 b1
  · exact c10               -- a3 b2
  · exact ladder_swap c4    -- m a2
  · exact c12               -- m b2
  · exact ladder_swap c5    -- b1 a2
  · exact ladder_swap c9    -- b1 a3
  · exact c15               -- b1 b3
  · exact ladder_swap c2    -- b2 a1
  · exact ladder_swap c6    -- b2 a2
  · exact ladder_swap c10   -- b2 a3
  · exact ladder_swap c12   -- b2 m
  · exact ladder_swap c3    -- b3 a1
  · exact ladder_swap c7    -- b3 a2
  · exact c22               -- b3 b1

/-- **H16 at `N = 3`** (Theorem 1.3 on `P_3 × P_2`, uniform `J ≥ 0`). -/
theorem hLadder_holds3 : hLadder 3 := ladder_of_shared (hSphereIso_holds 3) G2S3.hShared_holds3

/-- **H16 at `N = 4`** (Theorem 1.2(a) on `P_3 × P_2`, uniform `J ≥ 0`). -/
theorem hLadder_holds4 : hLadder 4 := ladder_of_shared (hSphereIso_holds 4) G2S3.hShared_holds4

end G2Kernel
