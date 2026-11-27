/-
G2S0.BlocksA (stage S0 (d), part 1): the blocks of a simple graph, and the direction
`IsCactus G → every block of G is a cycle or a single edge`.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Theorem 1.1 (every block of G is a cycle or a single
edge) and Section 5.1 (a block is a maximal connected subgraph without a cut vertex, after Diestel, Section 3.1).
Convention: subgraphs are spanning (`H ≤ G`), and the vertices of `H` are those that carry an edge of `H` (`vsupp`); so the blocks
here are the blocks with an edge (the maximal 2-connected subgraphs and the bridges), and isolated vertices are left out.
- `noCross`: a connected subgraph without a cut vertex does not cross a separation at one vertex (or at none).
- `connNoCut_cycle`: a cycle is connected and has no cut vertex.
- `edges_in_one_block`: the edges of such a subgraph lie in one block of a cactus list; `isCactus_imp_blocks`.
-/
import G2Kernel.Proofs.CactusProof

namespace G2Kernel

open SimpleGraph Fin.NatCast

variable {V : Type*}

/-! ### Blocks -/

/-- the vertices that carry an edge of H -/
def vsupp (H : SimpleGraph V) : Set V := {x | ∃ y, H.Adj x y}

/-- H with the vertex v deleted -/
def delV (H : SimpleGraph V) (v : V) : SimpleGraph V where
  Adj x y := H.Adj x y ∧ x ≠ v ∧ y ≠ v
  symm := ⟨fun _ _ h => ⟨h.1.symm, h.2.2, h.2.1⟩⟩
  loopless := ⟨fun _ h => H.irrefl h.1⟩

theorem delV_le (H : SimpleGraph V) (v : V) : delV H v ≤ H := fun _ _ h => h.1

/-- connected (on its vertices) and without a cut vertex -/
def ConnNoCut (H : SimpleGraph V) : Prop :=
  (∀ x ∈ vsupp H, ∀ y ∈ vsupp H, H.Reachable x y) ∧
  (∀ v, ∀ x ∈ vsupp H, ∀ y ∈ vsupp H, x ≠ v → y ≠ v → (delV H v).Reachable x y)

/-- a block of G: a maximal subgraph with an edge that is connected and has no cut vertex -/
def IsBlock (G B : SimpleGraph V) : Prop :=
  B ≤ G ∧ (∃ x y, B.Adj x y) ∧ ConnNoCut B ∧ ∀ B' : SimpleGraph V, B ≤ B' → B' ≤ G → ConnNoCut B' → B' = B

/-- B is a cycle: the image of C_n, n ≥ 3, under an injective map -/
def IsCycleSG (B : SimpleGraph V) : Prop :=
  ∃ (n : ℕ) (φ : Fin n → V), 3 ≤ n ∧ Function.Injective φ ∧
    ∀ x y, B.Adj x y ↔ ∃ a b, (SimpleGraph.cycleGraph n).Adj a b ∧ x = φ a ∧ y = φ b

/-- B is a single edge -/
def IsEdgeSG (B : SimpleGraph V) : Prop := ∃ u w, u ≠ w ∧ ∀ x y, B.Adj x y ↔ s(x, y) = s(u, w)

/-- the hypothesis of Theorem 1.1: every block of G is a cycle or a single edge -/
def BlocksCycleOrEdge (G : SimpleGraph V) : Prop := ∀ B, IsBlock G B → IsCycleSG B ∨ IsEdgeSG B

/-! ### Separations -/

theorem reach_closed {K : SimpleGraph V} {X : Set V} (hX : ∀ p q, K.Adj p q → p ∈ X → q ∈ X) {a b : V}
    (h : K.Reachable a b) : a ∈ X → b ∈ X := by
  obtain ⟨w⟩ := h
  induction w with
  | nil => exact id
  | cons hadj _ ih => exact fun ha => ih (hX _ _ hadj ha)

/-- **no crossing**: a connected subgraph without a cut vertex does not cross a separation at one vertex (or at none) -/
theorem noCross {H : SimpleGraph V} (hH : ConnNoCut H) {A B : Set V}
    (hsep : ∀ x y, H.Adj x y → (x ∈ A ∧ y ∈ A) ∨ (x ∈ B ∧ y ∈ B))
    (hAB : ∀ x y, x ∈ A → x ∈ B → y ∈ A → y ∈ B → x = y) :
    (∀ x y, H.Adj x y → x ∈ A ∧ y ∈ A) ∨ (∀ x y, H.Adj x y → x ∈ B ∧ y ∈ B) := by
  by_contra hcon
  rw [not_or] at hcon
  obtain ⟨h1, h2⟩ := hcon
  push_neg at h1 h2
  obtain ⟨x1, y1, hxy1, n1⟩ := h1
  obtain ⟨x2, y2, hxy2, n2⟩ := h2
  obtain ⟨p1, hp1s, hp1A⟩ : ∃ p, p ∈ vsupp H ∧ p ∉ A := by
    by_cases hx : x1 ∈ A
    · exact ⟨y1, ⟨x1, hxy1.symm⟩, n1 hx⟩
    · exact ⟨x1, ⟨y1, hxy1⟩, hx⟩
  obtain ⟨p2, hp2s, hp2A, hp2B⟩ : ∃ p, p ∈ vsupp H ∧ p ∈ A ∧ p ∉ B := by
    have hin : x2 ∈ A ∧ y2 ∈ A := by
      rcases hsep x2 y2 hxy2 with h | h
      · exact h
      · exact absurd h.2 (n2 h.1)
    by_cases hx : x2 ∈ B
    · exact ⟨y2, ⟨x2, hxy2.symm⟩, hin.2, n2 hx⟩
    · exact ⟨x2, ⟨y2, hxy2⟩, hin.1, hx⟩
  have hclosed : ∀ (K : SimpleGraph V), K ≤ H → (∀ p q, K.Adj p q → ¬(q ∈ A ∧ q ∈ B)) →
      ∀ p q, K.Adj p q → (p ∈ A ∧ p ∉ B) → (q ∈ A ∧ q ∉ B) := by
    intro K hK hq p q hpq hp
    rcases hsep p q (hK hpq) with h | h
    · exact ⟨h.2, fun hqB => hq p q hpq ⟨h.2, hqB⟩⟩
    · exact absurd h.1 hp.2
  by_cases hv : ∃ v, v ∈ A ∧ v ∈ B
  · obtain ⟨v, hvA, hvB⟩ := hv
    have hp1v : p1 ≠ v := fun h => hp1A (by rw [h]; exact hvA)
    have hp2v : p2 ≠ v := fun h => hp2B (by rw [h]; exact hvB)
    have hreach := hH.2 v p2 hp2s p1 hp1s hp2v hp1v
    have := reach_closed (hclosed (delV H v) (delV_le H v)
      (fun p q hpq hqAB => hpq.2.2 (hAB q v hqAB.1 hqAB.2 hvA hvB))) hreach ⟨hp2A, hp2B⟩
    exact hp1A this.1
  · have hreach := hH.1 p2 hp2s p1 hp1s
    have := reach_closed (hclosed H le_rfl (fun p q _ hqAB => hv ⟨q, hqAB⟩)) hreach ⟨hp2A, hp2B⟩
    exact hp1A this.1

/-! ### The graph of a cactus block, and cycles -/

/-- the graph of the edges of a cactus block -/
def blockSG (X : CactusBlock V) : SimpleGraph V := SimpleGraph.fromEdgeSet X.edges

theorem blockSG_adj (X : CactusBlock V) (x y : V) : (blockSG X).Adj x y ↔ s(x, y) ∈ X.edges ∧ x ≠ y :=
  SimpleGraph.fromEdgeSet_adj _

theorem cycle_edge_mem {n : ℕ} (φ : Fin n → V) {a b : Fin n} (h : (cycleGraph n).Adj a b) :
    s(φ a, φ b) ∈ (CactusBlock.cycle n φ).edges :=
  ⟨s(a, b), (SimpleGraph.mem_edgeSet _).mpr h, rfl⟩

theorem natCast_ne_zero_of_lt {m k : ℕ} (hk1 : 1 ≤ k) (hk2 : k ≤ m + 2) : ((k : ℕ) : Fin (m + 3)) ≠ 0 := by
  intro h
  have h' := congrArg Fin.val h
  rw [Fin.val_natCast, Fin.val_zero, Nat.mod_eq_of_lt (by omega)] at h'
  omega

theorem cycle_path {m : ℕ} (φ : Fin (m + 3) → V) (hφ : Function.Injective φ) (c : Fin (m + 3)) :
    ∀ k : ℕ, 1 ≤ k → k ≤ m + 2 →
      (delV (blockSG (CactusBlock.cycle (m + 3) φ)) (φ c)).Reachable (φ (c + 1)) (φ (c + (k : Fin (m + 3)))) := by
  intro k
  induction k with
  | zero => intro h; omega
  | succ k ih =>
    intro hk1 hk2
    rcases Nat.lt_or_ge k 1 with hk | hk
    · have hk0 : k = 0 := by omega
      subst hk0
      simp only [zero_add, Nat.cast_one]
      exact SimpleGraph.Reachable.refl _
    · refine (ih hk (by omega)).trans (SimpleGraph.Adj.reachable ?_)
      have hne1 : c + ((k : ℕ) : Fin (m + 3)) ≠ c := by
        intro h
        apply natCast_ne_zero_of_lt (m := m) hk (by omega)
        have := congrArg (fun x => x - c) h
        simpa using this
      have hne2 : c + ((k + 1 : ℕ) : Fin (m + 3)) ≠ c := by
        intro h
        apply natCast_ne_zero_of_lt (m := m) (k := k + 1) (by omega) hk2
        have := congrArg (fun x => x - c) h
        simpa using this
      have hadj : (cycleGraph (m + 3)).Adj (c + ((k : ℕ) : Fin (m + 3))) (c + ((k + 1 : ℕ) : Fin (m + 3))) := by
        have h1 : c + ((k + 1 : ℕ) : Fin (m + 3)) - (c + ((k : ℕ) : Fin (m + 3))) = 1 := by
          first
          | (rw [Nat.cast_succ, ← add_assoc, add_sub_cancel_left])
          | (simp only [Nat.cast_succ, ← add_assoc, add_sub_cancel_left])
          | (push_cast; abel)
          | simp
        exact (cycleGraph_adj (n := m + 1)).mpr (Or.inr h1)
      refine ⟨(blockSG_adj _ _ _).mpr ⟨cycle_edge_mem φ hadj, fun h => SimpleGraph.Adj.ne hadj (hφ h)⟩, ?_, ?_⟩
      · exact fun h => hne1 (hφ h)
      · exact fun h => hne2 (hφ h)

theorem vsupp_cycle {n : ℕ} (φ : Fin n → V) {x : V} (hx : x ∈ vsupp (blockSG (CactusBlock.cycle n φ))) :
    ∃ a, x = φ a := by
  obtain ⟨y, hxy⟩ := hx
  obtain ⟨⟨g, -, hg⟩, -⟩ := (blockSG_adj _ _ _).mp hxy
  induction g using Sym2.ind with
  | h a b =>
    rw [Sym2.map_mk, Sym2.eq_iff] at hg
    rcases hg with ⟨h1, -⟩ | ⟨-, h2⟩
    · exact ⟨a, h1.symm⟩
    · exact ⟨b, h2.symm⟩

/-- from c + 1 every other vertex of the cycle is reachable without c -/
theorem cycle_reach_from {m : ℕ} (φ : Fin (m + 3) → V) (hφ : Function.Injective φ) (c a : Fin (m + 3)) (hac : a ≠ c) :
    (delV (blockSG (CactusBlock.cycle (m + 3) φ)) (φ c)).Reachable (φ (c + 1)) (φ a) := by
  have hk1 : 1 ≤ (a - c).val := by
    rcases Nat.eq_zero_or_pos (a - c).val with h | h
    · exfalso
      apply hac
      have : a - c = 0 := Fin.ext h
      exact sub_eq_zero.mp this
    · exact h
  have hk2 : (a - c).val ≤ m + 2 := by have := (a - c).isLt; omega
  have h := cycle_path φ hφ c (a - c).val hk1 hk2
  rwa [Fin.cast_val_eq_self, add_sub_cancel] at h

/-- **a cycle is connected and has no cut vertex** -/
theorem connNoCut_cycle {n : ℕ} (hn : 3 ≤ n) {φ : Fin n → V} (hφ : Function.Injective φ) :
    ConnNoCut (blockSG (CactusBlock.cycle n φ)) := by
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 3 := ⟨n - 3, by omega⟩
  have hreach2 : ∀ c a b : Fin (m + 3), a ≠ c → b ≠ c →
      (delV (blockSG (CactusBlock.cycle (m + 3) φ)) (φ c)).Reachable (φ a) (φ b) :=
    fun c a b hac hbc => (cycle_reach_from φ hφ c a hac).symm.trans (cycle_reach_from φ hφ c b hbc)
  have hconn : ∀ a b : Fin (m + 3), (blockSG (CactusBlock.cycle (m + 3) φ)).Reachable (φ a) (φ b) := by
    intro a b
    obtain ⟨c, hca, hcb⟩ : ∃ c : Fin (m + 3), a ≠ c ∧ b ≠ c := by
      by_cases h0 : a.val ≠ 0 ∧ b.val ≠ 0
      · exact ⟨⟨0, by omega⟩, fun h => h0.1 (by rw [h]), fun h => h0.2 (by rw [h])⟩
      by_cases h1 : a.val ≠ 1 ∧ b.val ≠ 1
      · exact ⟨⟨1, by omega⟩, fun h => h1.1 (by rw [h]), fun h => h1.2 (by rw [h])⟩
      refine ⟨⟨2, by omega⟩, fun h => ?_, fun h => ?_⟩
      · have h2 := congrArg Fin.val h
        simp only at h2
        omega
      · have h2 := congrArg Fin.val h
        simp only at h2
        omega
    exact (hreach2 c a b hca hcb).mono (delV_le _ _)
  refine ⟨fun x hx y hy => ?_, fun v x hx y hy hxv hyv => ?_⟩
  · obtain ⟨a, rfl⟩ := vsupp_cycle φ hx
    obtain ⟨b, rfl⟩ := vsupp_cycle φ hy
    exact hconn a b
  · obtain ⟨a, rfl⟩ := vsupp_cycle φ hx
    obtain ⟨b, rfl⟩ := vsupp_cycle φ hy
    by_cases hv : ∃ c, v = φ c
    · obtain ⟨c, rfl⟩ := hv
      exact hreach2 c a b (fun h => hxv (by rw [h])) (fun h => hyv (by rw [h]))
    · push_neg at hv
      refine (hconn a b).mono (fun p q hpq => ⟨hpq, ?_, ?_⟩)
      · obtain ⟨c, rfl⟩ := vsupp_cycle φ ⟨q, hpq⟩
        exact (hv c).symm
      · obtain ⟨c, rfl⟩ := vsupp_cycle φ ⟨p, hpq.symm⟩
        exact (hv c).symm

/-! ### IsCactus G → every block of G is a cycle or a single edge -/

/-- the last-block condition of `IsCactusWith`, as a predicate on lists -/
def Overlap (L : List (CactusBlock V)) : Prop :=
  ∀ (L₁ L₂ : List (CactusBlock V)) (B : CactusBlock V), L = L₁ ++ B :: L₂ →
    ∀ x y, x ∈ B.verts → y ∈ B.verts → (∃ B' ∈ L₁, x ∈ B'.verts) → (∃ B' ∈ L₁, y ∈ B'.verts) → x = y

theorem overlap_init {L : List (CactusBlock V)} {X : CactusBlock V} (h : Overlap (L ++ [X])) : Overlap L := by
  intro L₁ L₂ B hL
  exact h L₁ (L₂ ++ [X]) B (by rw [hL]; simp)

theorem overlap_last {L : List (CactusBlock V)} {X : CactusBlock V} (h : Overlap (L ++ [X])) :
    ∀ x y, x ∈ X.verts → y ∈ X.verts → x ∈ listVerts L → y ∈ listVerts L → x = y :=
  fun x y hx hy hxL hyL => h L [] X rfl x y hx hy hxL hyL

/-- the edges of a connected subgraph without a cut vertex lie in one block of a cactus list -/
theorem edges_in_one_block {H : SimpleGraph V} (hH : ConnNoCut H) (hne : ∃ x y, H.Adj x y) :
    ∀ L : List (CactusBlock V), Overlap L → (∀ x y, H.Adj x y → s(x, y) ∈ listEdges L) →
      ∃ X ∈ L, ∀ x y, H.Adj x y → s(x, y) ∈ X.edges := by
  intro L
  induction L using List.reverseRecOn with
  | nil =>
    intro _ hE
    obtain ⟨x, y, hxy⟩ := hne
    obtain ⟨B, hB, -⟩ := hE x y hxy
    exact absurd hB List.not_mem_nil
  | append_singleton L X ih =>
    intro hO hE
    have hlast := overlap_last hO
    have hsep : ∀ x y, H.Adj x y → (x ∈ X.verts ∧ y ∈ X.verts) ∨ (x ∈ listVerts L ∧ y ∈ listVerts L) := by
      intro x y hxy
      rcases (mem_listEdges_append L X _).mp (hE x y hxy) with h | h
      · exact Or.inr ⟨mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_left x y),
          mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_right x y)⟩
      · exact Or.inl ⟨CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_left x y),
          CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_right x y)⟩
    have hAB : ∀ x y, x ∈ X.verts → x ∈ listVerts L → y ∈ X.verts → y ∈ listVerts L → x = y :=
      fun x y hx hxL hy hyL => hlast x y hx hy hxL hyL
    rcases noCross hH hsep hAB with hA | hB
    · refine ⟨X, List.mem_append.mpr (Or.inr (List.mem_singleton.mpr rfl)), fun x y hxy => ?_⟩
      rcases (mem_listEdges_append L X _).mp (hE x y hxy) with h | h
      · exfalso
        have hx := mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_left x y)
        have hy := mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_right x y)
        exact H.ne_of_adj hxy (hlast x y (hA x y hxy).1 (hA x y hxy).2 hx hy)
      · exact h
    · have hE' : ∀ x y, H.Adj x y → s(x, y) ∈ listEdges L := by
        intro x y hxy
        rcases (mem_listEdges_append L X _).mp (hE x y hxy) with h | h
        · exact h
        · exfalso
          exact H.ne_of_adj hxy (hlast x y (CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_left x y))
            (CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_right x y)) (hB x y hxy).1 (hB x y hxy).2)
      obtain ⟨X', hX', hX'E⟩ := ih (overlap_init hO) hE'
      exact ⟨X', List.mem_append.mpr (Or.inl hX'), hX'E⟩

theorem cycle_adj_iff {n : ℕ} {φ : Fin n → V} (hφ : Function.Injective φ) (x y : V) :
    (blockSG (CactusBlock.cycle n φ)).Adj x y ↔ ∃ a b, (cycleGraph n).Adj a b ∧ x = φ a ∧ y = φ b := by
  rw [blockSG_adj]
  constructor
  · rintro ⟨⟨g, hg, hgxy⟩, -⟩
    induction g using Sym2.ind with
    | h a b =>
      rw [SimpleGraph.mem_edgeSet] at hg
      rw [Sym2.map_mk, Sym2.eq_iff] at hgxy
      rcases hgxy with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · exact ⟨a, b, hg, h1.symm, h2.symm⟩
      · exact ⟨b, a, hg.symm, h2.symm, h1.symm⟩
  · rintro ⟨a, b, hab, rfl, rfl⟩
    exact ⟨cycle_edge_mem φ hab, fun h => SimpleGraph.Adj.ne hab (hφ h)⟩

/-- **IsCactus G → every block of G is a cycle or a single edge** -/
theorem isCactus_imp_blocks (G : SimpleGraph V) : IsCactus G → BlocksCycleOrEdge G := by
  rintro ⟨L, hval, hcov, hover⟩ B ⟨hBG, hne, hcnc, hmax⟩
  have hE : ∀ x y, B.Adj x y → s(x, y) ∈ listEdges L := fun x y hxy => hcov _ (hBG hxy)
  obtain ⟨X, hXL, hXE⟩ := edges_in_one_block hcnc hne L hover hE
  have hXG := hval X hXL
  cases X with
  | edge e =>
    right
    obtain ⟨x0, y0, h0⟩ := hne
    have he : s(x0, y0) = e := hXE x0 y0 h0
    refine ⟨x0, y0, B.ne_of_adj h0, fun x y => ⟨fun h => (hXE x y h).trans he.symm, fun h => ?_⟩⟩
    rcases Sym2.eq_iff.mp h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · exact h0
    · exact h0.symm
  | cycle n φ =>
    left
    have hn := hXG.1
    have hφ := hXG.2.1
    have hle : B ≤ blockSG (CactusBlock.cycle n φ) :=
      fun x y h => (blockSG_adj _ x y).mpr ⟨hXE x y h, B.ne_of_adj h⟩
    have hleG : blockSG (CactusBlock.cycle n φ) ≤ G := fun x y h =>
      (SimpleGraph.mem_edgeSet G).mp (CactusBlock.edges_sub_edgeSet hXG ((blockSG_adj _ x y).mp h).1)
    have hEq := hmax _ hle hleG (connNoCut_cycle hn hφ)
    refine ⟨n, φ, hn, hφ, fun x y => ?_⟩
    rw [← hEq]
    exact cycle_adj_iff hφ x y

end G2Kernel

#print axioms G2Kernel.noCross
#print axioms G2Kernel.connNoCut_cycle
#print axioms G2Kernel.edges_in_one_block
#print axioms G2Kernel.isCactus_imp_blocks
