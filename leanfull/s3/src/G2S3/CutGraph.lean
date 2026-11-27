/-
G2S3.CutGraph (stage S3, Part E1): 2-edge cuts and cycles (STATEMENTS_S3_v8.md, E1). The definition is the paper's
equivalent form (tex l.112-114). The sides: A is the class of x in G - {e, f}; e and f are not bridges, so y ∉ A and exactly
one end of f lies in A. A cycle through s(x, y) gives a path from x to y inside the cycle that avoids s(x, y).
-/
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Combinatorics.SimpleGraph.Paths

namespace G2S3

open SimpleGraph

/-- **2-edge cut** (tex l.112-114), in the paper's equivalent form -/
def IsTwoEdgeCut {V : Type*} (G : SimpleGraph V) (e f : Sym2 V) : Prop :=
  e ∈ G.edgeSet ∧ f ∈ G.edgeSet ∧ e ≠ f ∧ (∃ a ∈ e, ∃ b ∈ f, G.Reachable a b) ∧ ¬ G.IsBridge e ∧ ¬ G.IsBridge f ∧
    ∃ u v, (∃ a ∈ e, G.Reachable a u) ∧ G.Reachable u v ∧ ¬ (G.deleteEdges {e, f}).Reachable u v

/-- the sides of a cut -/
structure CutSides {V : Type*} (G : SimpleGraph V) (x y z w : V) (A : Set V) : Prop where
  adj_e : G.Adj x y
  adj_f : G.Adj z w
  ne : s(x, y) ≠ s(z, w)
  xA : x ∈ A
  yA : y ∉ A
  zA : z ∈ A
  wA : w ∉ A
  side : ∀ a b, G.Adj a b → s(a, b) ≠ s(x, y) → s(a, b) ≠ s(z, w) → (a ∈ A ↔ b ∈ A)

section Cut

variable {V : Type*} {G : SimpleGraph V} {x y z w : V}

theorem cut_step {a b : V} (h : G.Adj a b) (he : s(a, b) ≠ s(x, y)) (hf : s(a, b) ≠ s(z, w)) :
    (G.deleteEdges {s(x, y), s(z, w)}).Reachable a b := by
  refine Adj.reachable ?_
  rw [deleteEdges_adj]
  refine ⟨h, ?_⟩
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff, not_or]
  exact ⟨he, hf⟩

theorem reach_of_edge {a b p q : V} (R : V → V → Prop) (hR : ∀ u, R u u) (hsymm : ∀ u v, R u v → R v u)
    (hpq : R p q) (h : s(a, b) = s(p, q)) : R a b := by
  rcases Sym2.eq_iff.mp h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · exact hpq
  · exact hsymm _ _ hpq

/-- with R x y, reachability in G - f lies inside reachability in G - {e, f} -/
theorem reach_sub_f (hxy : (G.deleteEdges {s(x, y), s(z, w)}).Reachable x y) {u v : V}
    (h : (G.deleteEdges {s(z, w)}).Reachable u v) : (G.deleteEdges {s(x, y), s(z, w)}).Reachable u v := by
  rw [reachable_iff_reflTransGen] at h
  induction h with
  | refl => rfl
  | @tail b c _ hbc ih =>
    rw [deleteEdges_adj] at hbc
    obtain ⟨hbc, hnf⟩ := hbc
    simp only [Set.mem_singleton_iff] at hnf
    refine ih.trans ?_
    by_cases hbe : s(b, c) = s(x, y)
    · exact reach_of_edge _ (fun _ => Reachable.refl _) (fun _ _ h => h.symm) hxy hbe
    · exact cut_step hbc hbe hnf

/-- with R z w, reachability in G - e lies inside reachability in G - {e, f} -/
theorem reach_sub_e (hzw : (G.deleteEdges {s(x, y), s(z, w)}).Reachable z w) {u v : V}
    (h : (G.deleteEdges {s(x, y)}).Reachable u v) : (G.deleteEdges {s(x, y), s(z, w)}).Reachable u v := by
  rw [reachable_iff_reflTransGen] at h
  induction h with
  | refl => rfl
  | @tail b c _ hbc ih =>
    rw [deleteEdges_adj] at hbc
    obtain ⟨hbc, hne⟩ := hbc
    simp only [Set.mem_singleton_iff] at hne
    refine ih.trans ?_
    by_cases hbf : s(b, c) = s(z, w)
    · exact reach_of_edge _ (fun _ => Reachable.refl _) (fun _ _ h => h.symm) hzw hbf
    · exact cut_step hbc hne hbf

/-- with R x y and R z w, reachability in G lies inside reachability in G - {e, f} -/
theorem reach_sub_all (hxy : (G.deleteEdges {s(x, y), s(z, w)}).Reachable x y)
    (hzw : (G.deleteEdges {s(x, y), s(z, w)}).Reachable z w) {u v : V} (h : G.Reachable u v) :
    (G.deleteEdges {s(x, y), s(z, w)}).Reachable u v := by
  rw [reachable_iff_reflTransGen] at h
  induction h with
  | refl => rfl
  | @tail b c _ hbc ih =>
    refine ih.trans ?_
    by_cases hbe : s(b, c) = s(x, y)
    · exact reach_of_edge _ (fun _ => Reachable.refl _) (fun _ _ h => h.symm) hxy hbe
    · by_cases hbf : s(b, c) = s(z, w)
      · exact reach_of_edge _ (fun _ => Reachable.refl _) (fun _ _ h => h.symm) hzw hbf
      · exact cut_step hbc hbe hbf

/-- reachability in G - f, in terms of G - {e, f} -/
theorem reach_f_cases {u v : V} (h : (G.deleteEdges {s(z, w)}).Reachable u v) :
    (G.deleteEdges {s(x, y), s(z, w)}).Reachable u v ∨
      ((G.deleteEdges {s(x, y), s(z, w)}).Reachable u x ∧ (G.deleteEdges {s(x, y), s(z, w)}).Reachable y v) ∨
      ((G.deleteEdges {s(x, y), s(z, w)}).Reachable u y ∧ (G.deleteEdges {s(x, y), s(z, w)}).Reachable x v) := by
  set R := (G.deleteEdges {s(x, y), s(z, w)}).Reachable with hRdef
  rw [reachable_iff_reflTransGen] at h
  induction h with
  | refl => exact Or.inl (Reachable.refl _)
  | @tail b c _ hbc ih =>
    rw [deleteEdges_adj] at hbc
    obtain ⟨hbc, hnf⟩ := hbc
    simp only [Set.mem_singleton_iff] at hnf
    by_cases hbe : s(b, c) = s(x, y)
    · rcases Sym2.eq_iff.mp hbe with ⟨hb, hc⟩ | ⟨hb, hc⟩
      · rw [hb] at ih
        rw [hc]
        rcases ih with h1 | ⟨h1, h2⟩ | ⟨h1, h2⟩
        · exact Or.inr (Or.inl ⟨h1, Reachable.refl _⟩)
        · exact Or.inl (h1.trans h2.symm)
        · exact Or.inl h1
      · rw [hb] at ih
        rw [hc]
        rcases ih with h1 | ⟨h1, h2⟩ | ⟨h1, h2⟩
        · exact Or.inr (Or.inr ⟨h1, Reachable.refl _⟩)
        · exact Or.inl h1
        · exact Or.inl (h1.trans h2.symm)
    · have hst : R b c := cut_step hbc hbe hnf
      rcases ih with h1 | ⟨h1, h2⟩ | ⟨h1, h2⟩
      · exact Or.inl (h1.trans hst)
      · exact Or.inr (Or.inl ⟨h1, h2.trans hst⟩)
      · exact Or.inr (Or.inr ⟨h1, h2.trans hst⟩)

theorem cut_sides (hcut : IsTwoEdgeCut G s(x, y) s(z, w)) :
    ∃ A : Set V, CutSides G x y z w A ∨ CutSides G x y w z A := by
  obtain ⟨he, hf, hef, _, hnbe, hnbf, u0, v0, _, huv, hnot⟩ := hcut
  have hbe : (G.deleteEdges {s(x, y)}).Reachable x y := by
    rw [isBridge_iff, not_not] at hnbe; exact hnbe
  have hbf : (G.deleteEdges {s(z, w)}).Reachable z w := by
    rw [isBridge_iff, not_not] at hnbf; exact hnbf
  set R := (G.deleteEdges {s(x, y), s(z, w)}).Reachable with hRdef
  have hnxy : ¬ R x y := by
    intro hxy
    exact hnot (reach_sub_all hxy (reach_sub_f hxy hbf) huv)
  have hnzw : ¬ R z w := fun hzw => hnxy (reach_sub_e hzw hbe)
  have hadj_e : G.Adj x y := he
  have hadj_f : G.Adj z w := hf
  have hside : ∀ a b, G.Adj a b → s(a, b) ≠ s(x, y) → s(a, b) ≠ s(z, w) → (R x a ↔ R x b) := by
    intro a b hab h1 h2
    have hab' := cut_step hab h1 h2
    exact ⟨fun h => h.trans hab', fun h => h.trans hab'.symm⟩
  refine ⟨{v | R x v}, ?_⟩
  rcases reach_f_cases (x := x) (y := y) hbf with h | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact absurd h hnzw
  · left
    exact ⟨hadj_e, hadj_f, hef, Reachable.refl _, hnxy, h1.symm,
      fun hw => hnxy (hw.trans h2.symm), hside⟩
  · right
    have hswap : s(w, z) = s(z, w) := Sym2.eq_swap
    refine ⟨hadj_e, hadj_f.symm, ?_, Reachable.refl _, hnxy, h2, fun hz => hnxy (hz.trans h1), ?_⟩
    · rw [hswap]; exact hef
    · intro a b hab h1' h2'
      rw [hswap] at h2'
      exact hside a b hab h1' h2'

end Cut

/-- a cycle through s(x, y) gives a path from x to y inside the cycle, avoiding s(x, y) -/
theorem cycle_path {V : Type*} [DecidableEq V] {G : SimpleGraph V} {x y u : V} (c : G.Walk u u) (hc : c.IsCycle)
    (he : s(x, y) ∈ c.edges) : ∃ p : G.Walk x y, p.IsPath ∧ ∀ g ∈ p.edges, g ∈ c.edges ∧ g ≠ s(x, y) := by
  set H : SimpleGraph V := SimpleGraph.fromEdgeSet {g | g ∈ c.edges} with hH
  have hcH : ∀ g, g ∈ c.edges → g ∈ H.edgeSet := by
    intro g hg
    rw [hH, edgeSet_fromEdgeSet]
    exact ⟨hg, G.not_isDiag_of_mem_edgeSet (c.edges_subset_edgeSet hg)⟩
  have hc' : (c.transfer H hcH).IsCycle := (Walk.isCycle_transfer hcH).mpr hc
  have he' : s(x, y) ∈ (c.transfer H hcH).edges := by rw [Walk.edges_transfer]; exact he
  obtain ⟨_, hreach⟩ := (adj_and_reachable_delete_edges_iff_exists_cycle (G := H)).mpr ⟨u, _, hc', he'⟩
  obtain ⟨q⟩ := hreach
  have hqG : ∀ g, g ∈ q.bypass.edges → g ∈ G.edgeSet := by
    intro g hg
    have h1 := q.edges_subset_edgeSet (q.edges_bypass_subset_edges hg)
    rw [edgeSet_deleteEdges] at h1
    have h2 : g ∈ H.edgeSet := h1.1
    rw [hH, edgeSet_fromEdgeSet] at h2
    exact c.edges_subset_edgeSet h2.1
  refine ⟨q.bypass.transfer G hqG, (Walk.isPath_transfer hqG).mpr (Walk.bypass_isPath q), fun g hg => ?_⟩
  rw [Walk.edges_transfer] at hg
  have h1 := q.edges_subset_edgeSet (q.edges_bypass_subset_edges hg)
  rw [edgeSet_deleteEdges] at h1
  have h2 : g ∈ H.edgeSet := h1.1
  rw [hH, edgeSet_fromEdgeSet] at h2
  exact ⟨h2.1, by simpa using h1.2⟩

end G2S3

#print axioms G2S3.cut_sides
#print axioms G2S3.cycle_path
