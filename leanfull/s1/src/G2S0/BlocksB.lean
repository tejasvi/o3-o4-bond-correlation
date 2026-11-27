/-
G2S0.BlocksB (stage S0 (d), part 2): the direction `every block of G is a cycle or a single edge → IsCactus G` for finite G,
the equivalence `isCactus_iff_blocks`, and Theorem 1.1 in the paper's form (`cactus_thm_blocks`, H1 discharged).
Method: induction on the number of edges. If G is connected without a cut vertex, G is its own block, hence a cycle or an edge. Otherwise
G splits at one vertex (or at none) into two parts with fewer edges (`exists_sep`); the blocks of each part are blocks of G (`noCross`);
the lists of the parts are joined, the part that holds the root first, the other part rooted at the shared vertex (`rootedCactus_append`).
-/
import G2S0.BlocksA
import G2S0.SphereIso

namespace G2Kernel

open SimpleGraph

variable {V : Type*}

/-! ### Separations of a graph that is not connected without a cut vertex -/

theorem delV_reach_self {G : SimpleGraph V} {v x : V} (h : (delV G v).Reachable x v) : x = v := by
  have hcl : ∀ p q, (delV G v).Adj p q → p ∈ ({v} : Set V) → q ∈ ({v} : Set V) := by
    intro p q hpq hp
    exact absurd hp hpq.2.1
  exact reach_closed hcl h.symm rfl

/-- a graph with an edge that is not connected without a cut vertex splits at one vertex (or at none) into two parts with edges -/
theorem exists_sep {G : SimpleGraph V} (hne : ∃ x y, G.Adj x y) (hnc : ¬ ConnNoCut G) :
    ∃ A B : Set V, (∀ x, x ∈ A ∨ x ∈ B) ∧ (∀ x y, x ∈ A → x ∈ B → y ∈ A → y ∈ B → x = y) ∧
      (∀ x y, G.Adj x y → (x ∈ A ∧ y ∈ A) ∨ (x ∈ B ∧ y ∈ B)) ∧
      (∃ x y, G.Adj x y ∧ x ∈ A ∧ y ∈ A) ∧ (∃ x y, G.Adj x y ∧ x ∈ B ∧ y ∈ B) := by
  unfold ConnNoCut at hnc
  by_cases hP : ∀ x ∈ vsupp G, ∀ y ∈ vsupp G, G.Reachable x y
  · have hQ : ¬ ∀ v, ∀ x ∈ vsupp G, ∀ y ∈ vsupp G, x ≠ v → y ≠ v → (delV G v).Reachable x y :=
      fun hQ => hnc ⟨hP, hQ⟩
    push_neg at hQ
    obtain ⟨v, x, ⟨wx, hxw⟩, y, ⟨wy, hyw⟩, hxv, hyv, hxy⟩ := hQ
    refine ⟨{z | z = v ∨ (delV G v).Reachable x z}, {z | ¬ (delV G v).Reachable x z},
      fun z => ?_, fun p q hpA hpB hqA hqB => ?_, fun p q hpq => ?_, ?_, ?_⟩
    · by_cases hz : (delV G v).Reachable x z
      · exact Or.inl (Or.inr hz)
      · exact Or.inr hz
    · have hp : p = v := hpA.resolve_right hpB
      have hq : q = v := hqA.resolve_right hqB
      rw [hp, hq]
    · by_cases hpv : p = v
      · by_cases hq : (delV G v).Reachable x q
        · exact Or.inl ⟨Or.inl hpv, Or.inr hq⟩
        · refine Or.inr ⟨fun h => ?_, hq⟩
          rw [hpv] at h
          exact hxv (delV_reach_self h)
      by_cases hqv : q = v
      · by_cases hp : (delV G v).Reachable x p
        · exact Or.inl ⟨Or.inr hp, Or.inl hqv⟩
        · refine Or.inr ⟨hp, fun h => ?_⟩
          rw [hqv] at h
          exact hxv (delV_reach_self h)
      have hadj : (delV G v).Adj p q := ⟨hpq, hpv, hqv⟩
      by_cases hp : (delV G v).Reachable x p
      · exact Or.inl ⟨Or.inr hp, Or.inr (hp.trans hadj.reachable)⟩
      · exact Or.inr ⟨hp, fun h => hp (h.trans hadj.symm.reachable)⟩
    · refine ⟨x, wx, hxw, Or.inr (SimpleGraph.Reachable.refl _), ?_⟩
      by_cases hwv : wx = v
      · exact Or.inl hwv
      · exact Or.inr (SimpleGraph.Adj.reachable ⟨hxw, hxv, hwv⟩)
    · refine ⟨y, wy, hyw, hxy, fun h => ?_⟩
      by_cases hwv : wy = v
      · rw [hwv] at h
        exact hxv (delV_reach_self h)
      · exact hxy (h.trans (SimpleGraph.Adj.reachable ⟨hyw.symm, hwv, hyv⟩))
  · push_neg at hP
    obtain ⟨x, ⟨wx, hxw⟩, y, ⟨wy, hyw⟩, hxy⟩ := hP
    refine ⟨{z | G.Reachable x z}, {z | ¬ G.Reachable x z}, fun z => em _, fun p q hpA hpB _ _ => absurd hpA hpB,
      fun p q hpq => ?_, ⟨x, wx, hxw, SimpleGraph.Reachable.refl _, hxw.reachable⟩, ⟨y, wy, hyw, hxy, fun h => hxy
        (h.trans hyw.symm.reachable)⟩⟩
    by_cases hp : G.Reachable x p
    · exact Or.inl ⟨hp, hp.trans hpq.reachable⟩
    · exact Or.inr ⟨hp, fun h => hp (h.trans hpq.symm.reachable)⟩

/-- the blocks of a part of a separation are blocks of the graph -/
theorem isBlock_of_restrict {G : SimpleGraph V} {A B : Set V}
    (hsep : ∀ x y, G.Adj x y → (x ∈ A ∧ y ∈ A) ∨ (x ∈ B ∧ y ∈ B))
    (hAB : ∀ x y, x ∈ A → x ∈ B → y ∈ A → y ∈ B → x = y) {K : SimpleGraph V} (hK : IsBlock (restrictTo G A) K) :
    IsBlock G K := by
  obtain ⟨hKA, ⟨x0, y0, h0⟩, hKc, hKmax⟩ := hK
  refine ⟨fun x y h => (hKA h).1, ⟨x0, y0, h0⟩, hKc, fun B' hKB' hB'G hB'c => ?_⟩
  have h0A : x0 ∈ A ∧ y0 ∈ A := ⟨(hKA h0).2.1, (hKA h0).2.2⟩
  rcases noCross hB'c (fun x y h => hsep x y (hB'G h)) hAB with hA | hB
  · exact hKmax B' hKB' (fun x y h => ⟨hB'G h, (hA x y h).1, (hA x y h).2⟩) hB'c
  · exfalso
    have hB0 := hB x0 y0 (hKB' h0)
    exact K.ne_of_adj h0 (hAB x0 y0 h0A.1 hB0.1 h0A.2 hB0.2)

/-! ### Rooted cactus lists -/

/-- the last-block condition with a root: each block meets the earlier blocks and the set `S` in at most one vertex -/
def OverlapR (L : List (CactusBlock V)) (S : Set V) : Prop :=
  ∀ (L₁ L₂ : List (CactusBlock V)) (X : CactusBlock V), L = L₁ ++ X :: L₂ →
    ∀ x y, x ∈ X.verts → y ∈ X.verts → (x ∈ S ∨ ∃ B' ∈ L₁, x ∈ B'.verts) → (y ∈ S ∨ ∃ B' ∈ L₁, y ∈ B'.verts) → x = y

theorem overlap_of_overlapR {L : List (CactusBlock V)} {S : Set V} (h : OverlapR L S) : Overlap L :=
  fun L₁ L₂ X hL x y hx hy hx1 hy1 => h L₁ L₂ X hL x y hx hy (Or.inr hx1) (Or.inr hy1)

theorem overlapR_append {L1 L2 : List (CactusBlock V)} {S1 S2 W2 : Set V}
    (h1 : OverlapR L1 S1) (h2 : OverlapR L2 S2) (hW : ∀ X ∈ L2, X.verts ⊆ W2)
    (hS : ∀ x ∈ W2, (x ∈ S1 ∨ ∃ B' ∈ L1, x ∈ B'.verts) → x ∈ S2) : OverlapR (L1 ++ L2) S1 := by
  intro M₁ M₂ X hM x y hx hy hx1 hy1
  have hsecond : ∀ a' : List (CactusBlock V), M₁ = L1 ++ a' → L2 = a' ++ X :: M₂ → x = y := by
    intro a' hM1 hL2
    have hXL2 : X ∈ L2 := by rw [hL2]; simp
    have conv : ∀ z, z ∈ X.verts → (z ∈ S1 ∨ ∃ B' ∈ M₁, z ∈ B'.verts) → (z ∈ S2 ∨ ∃ B' ∈ a', z ∈ B'.verts) := by
      intro z hz hz1
      rcases hz1 with hzS | ⟨B', hB'M, hzB'⟩
      · exact Or.inl (hS z (hW X hXL2 hz) (Or.inl hzS))
      · rw [hM1] at hB'M
        rcases List.mem_append.mp hB'M with hB'1 | hB'2
        · exact Or.inl (hS z (hW X hXL2 hz) (Or.inr ⟨B', hB'1, hzB'⟩))
        · exact Or.inr ⟨B', hB'2, hzB'⟩
    exact h2 a' M₂ X hL2 x y hx hy (conv x hx hx1) (conv y hy hy1)
  rcases List.append_eq_append_iff.mp hM with ⟨a', hM1, hL2⟩ | ⟨c', hL1, hXM⟩
  · exact hsecond a' hM1 hL2
  · cases c' with
    | nil =>
      simp only [List.append_nil, List.nil_append] at hL1 hXM
      exact hsecond [] (by rw [hL1, List.append_nil]) (by rw [← hXM, List.nil_append])
    | cons Y c'' =>
      simp only [List.cons_append, List.cons.injEq] at hXM
      obtain ⟨hXY, -⟩ := hXM
      subst hXY
      exact h1 M₁ c'' X hL1 x y hx hy hx1 hy1

/-- a rooted cactus list of G: blocks of G covering every edge, each meeting the earlier blocks and the root in at most one vertex,
on the vertices of G that carry an edge -/
def RootedCactus (G : SimpleGraph V) (r : V) (L : List (CactusBlock V)) : Prop :=
  (∀ X ∈ L, X.IsBlockOf G) ∧ (∀ e ∈ G.edgeSet, ∃ X ∈ L, e ∈ X.edges) ∧ OverlapR L {r} ∧ (∀ X ∈ L, X.verts ⊆ vsupp G)

theorem isBlockOf_mono {G G' : SimpleGraph V} (h : G ≤ G') {X : CactusBlock V} (hX : X.IsBlockOf G) :
    X.IsBlockOf G' := by
  cases X with
  | edge e => exact SimpleGraph.edgeSet_mono h hX
  | cycle n φ => exact ⟨hX.1, hX.2.1, fun a b hab => h (hX.2.2 a b hab)⟩

theorem vsupp_mono {H K : SimpleGraph V} (h : H ≤ K) : vsupp H ⊆ vsupp K := fun _ ⟨y, hxy⟩ => ⟨y, h hxy⟩

theorem vsupp_restrictTo (G : SimpleGraph V) (A : Set V) : vsupp (restrictTo G A) ⊆ A := fun _ ⟨_, hxy⟩ => hxy.2.1

theorem restrictTo_le (G : SimpleGraph V) (A : Set V) : restrictTo G A ≤ G := fun _ _ h => h.1

theorem rootedCactus_append {G : SimpleGraph V} {A1 A2 : Set V} {r c : V}
    (hsep : ∀ x y, G.Adj x y → (x ∈ A1 ∧ y ∈ A1) ∨ (x ∈ A2 ∧ y ∈ A2))
    (hroot : ∀ x, x ∈ A2 → (x = r ∨ x ∈ A1) → x = c)
    {L1 L2 : List (CactusBlock V)} (h1 : RootedCactus (restrictTo G A1) r L1)
    (h2 : RootedCactus (restrictTo G A2) c L2) : RootedCactus G r (L1 ++ L2) := by
  obtain ⟨v1, c1, o1, s1⟩ := h1
  obtain ⟨v2, c2, o2, s2⟩ := h2
  refine ⟨fun X hX => ?_, fun e he => ?_, ?_, fun X hX => ?_⟩
  · rcases List.mem_append.mp hX with h | h
    · exact isBlockOf_mono (restrictTo_le G A1) (v1 X h)
    · exact isBlockOf_mono (restrictTo_le G A2) (v2 X h)
  · induction e using Sym2.ind with
    | h x y =>
      rcases hsep x y he with hA | hA
      · obtain ⟨X, hX, hXe⟩ := c1 s(x, y) ⟨he, hA.1, hA.2⟩
        exact ⟨X, List.mem_append.mpr (Or.inl hX), hXe⟩
      · obtain ⟨X, hX, hXe⟩ := c2 s(x, y) ⟨he, hA.1, hA.2⟩
        exact ⟨X, List.mem_append.mpr (Or.inr hX), hXe⟩
  · refine overlapR_append o1 o2 (W2 := A2) (fun X hX z hz => vsupp_restrictTo G A2 (s2 X hX hz)) ?_
    intro x hx hx1
    show x = c
    rcases hx1 with hxr | ⟨B', hB', hxB'⟩
    · exact hroot x hx (Or.inl hxr)
    · exact hroot x hx (Or.inr (vsupp_restrictTo G A1 (s1 B' hB' hxB')))
  · rcases List.mem_append.mp hX with h | h
    · exact fun z hz => vsupp_mono (restrictTo_le G A1) (s1 X h hz)
    · exact fun z hz => vsupp_mono (restrictTo_le G A2) (s2 X h hz)

theorem overlapR_single (X : CactusBlock V) (r : V) : OverlapR [X] {r} := by
  intro L₁ L₂ Y hL x y _ _ hx1 hy1
  cases L₁ with
  | nil =>
    have hx : x = r := by
      rcases hx1 with h | ⟨B', hB', -⟩
      · exact h
      · exact absurd hB' List.not_mem_nil
    have hy : y = r := by
      rcases hy1 with h | ⟨B', hB', -⟩
      · exact h
      · exact absurd hB' List.not_mem_nil
    rw [hx, hy]
  | cons Z L₁' =>
    simp only [List.cons_append, List.cons.injEq] at hL
    exact absurd hL.2.symm (by simp)

theorem finite_edgeSet [Finite V] (G : SimpleGraph V) : G.edgeSet.Finite := by
  have : Finite (Sym2 V) := Finite.of_surjective (fun p : V × V => s(p.1, p.2)) (fun z => by
    induction z using Sym2.ind with
    | h a b => exact ⟨(a, b), rfl⟩)
  exact Set.toFinite _

theorem cycle_adj_add_one {m : ℕ} (a : Fin (m + 3)) : (cycleGraph (m + 3)).Adj a (a + 1) := by
  have h1 : a + 1 - a = 1 := by
    first
    | (rw [add_sub_cancel_left])
    | simp
  exact (cycleGraph_adj (n := m + 1)).mpr (Or.inr h1)

/-- **the rooted cactus lists exist** when every block is a cycle or a single edge (induction on the number of edges) -/
theorem rootedCactus_exists [Finite V] :
    ∀ (n : ℕ) (G : SimpleGraph V), G.edgeSet.ncard = n → BlocksCycleOrEdge G → ∀ r, ∃ L, RootedCactus G r L := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro G hn hB r
    by_cases hne : ∃ x y, G.Adj x y
    · by_cases hc : ConnNoCut G
      · have hGB : IsBlock G G := ⟨le_rfl, hne, hc, fun B' h1 h2 _ => le_antisymm h2 h1⟩
        rcases hB G hGB with ⟨m, φ, hm, hφ, hadj⟩ | ⟨u, w, huw, hadj⟩
        · refine ⟨[CactusBlock.cycle m φ], fun X hX => ?_, fun e he => ?_, overlapR_single _ r, fun X hX => ?_⟩
          · rw [List.mem_singleton] at hX
            subst hX
            exact ⟨hm, hφ, fun a b hab => (hadj (φ a) (φ b)).mpr ⟨a, b, hab, rfl, rfl⟩⟩
          · refine ⟨CactusBlock.cycle m φ, List.mem_singleton.mpr rfl, ?_⟩
            induction e using Sym2.ind with
            | h x y =>
              obtain ⟨a, b, hab, rfl, rfl⟩ := (hadj x y).mp he
              exact cycle_edge_mem φ hab
          · rw [List.mem_singleton] at hX
            subst hX
            rintro z ⟨a, rfl⟩
            obtain ⟨m', rfl⟩ : ∃ m', m = m' + 3 := ⟨m - 3, by omega⟩
            exact ⟨φ (a + 1), (hadj _ _).mpr ⟨a, a + 1, cycle_adj_add_one a, rfl, rfl⟩⟩
        · refine ⟨[CactusBlock.edge s(u, w)], fun X hX => ?_, fun e he => ?_, overlapR_single _ r, fun X hX => ?_⟩
          · rw [List.mem_singleton] at hX
            subst hX
            exact (hadj u w).mpr rfl
          · refine ⟨CactusBlock.edge s(u, w), List.mem_singleton.mpr rfl, ?_⟩
            induction e using Sym2.ind with
            | h x y => exact (hadj x y).mp he
          · rw [List.mem_singleton] at hX
            subst hX
            intro z hz
            rcases Sym2.mem_iff.mp hz with rfl | rfl
            · exact ⟨w, (hadj z w).mpr rfl⟩
            · exact ⟨u, (hadj z u).mpr Sym2.eq_swap⟩
      · obtain ⟨A, B, hcov, hAB, hsep, ⟨xa, ya, ha, hxa, hya⟩, ⟨xb, yb, hb, hxb, hyb⟩⟩ := exists_sep hne hc
        have hsep' : ∀ x y, G.Adj x y → (x ∈ B ∧ y ∈ B) ∨ (x ∈ A ∧ y ∈ A) := fun x y h => (hsep x y h).symm
        have hBA : ∀ x y, x ∈ B → x ∈ A → y ∈ B → y ∈ A → x = y :=
          fun x y hxB hxA hyB hyA => hAB x y hxA hxB hyA hyB
        have hfin := finite_edgeSet G
        have hltA : (restrictTo G A).edgeSet.ncard < n := by
          rw [← hn]
          refine Set.ncard_lt_ncard ⟨SimpleGraph.edgeSet_mono (restrictTo_le G A), fun hsub => ?_⟩ hfin
          have hmem : s(xb, yb) ∈ (restrictTo G A).edgeSet := hsub hb
          exact G.ne_of_adj hb (hAB xb yb hmem.2.1 hxb hmem.2.2 hyb)
        have hltB : (restrictTo G B).edgeSet.ncard < n := by
          rw [← hn]
          refine Set.ncard_lt_ncard ⟨SimpleGraph.edgeSet_mono (restrictTo_le G B), fun hsub => ?_⟩ hfin
          have hmem : s(xa, ya) ∈ (restrictTo G B).edgeSet := hsub ha
          exact G.ne_of_adj ha (hAB xa ya hxa hmem.2.1 hya hmem.2.2)
        have hBA' : BlocksCycleOrEdge (restrictTo G A) := fun K hK => hB K (isBlock_of_restrict hsep hAB hK)
        have hBB' : BlocksCycleOrEdge (restrictTo G B) := fun K hK => hB K (isBlock_of_restrict hsep' hBA hK)
        have IA := fun r' => ih _ hltA (restrictTo G A) rfl hBA' r'
        have IB := fun r' => ih _ hltB (restrictTo G B) rfl hBB' r'
        by_cases hv : ∃ v, v ∈ A ∧ v ∈ B
        · obtain ⟨v, hvA, hvB⟩ := hv
          by_cases hrA : r ∈ A
          · obtain ⟨L1, h1⟩ := IA r
            obtain ⟨L2, h2⟩ := IB v
            refine ⟨L1 ++ L2, rootedCactus_append hsep (fun x hxB hx => ?_) h1 h2⟩
            rcases hx with rfl | hxA
            · exact hAB x v hrA hxB hvA hvB
            · exact hAB x v hxA hxB hvA hvB
          · obtain ⟨L1, h1⟩ := IB r
            obtain ⟨L2, h2⟩ := IA v
            refine ⟨L1 ++ L2, rootedCactus_append hsep' (fun x hxA hx => ?_) h1 h2⟩
            rcases hx with rfl | hxB
            · exact absurd hxA hrA
            · exact hAB x v hxA hxB hvA hvB
        · by_cases hrA : r ∈ A
          · obtain ⟨L1, h1⟩ := IA r
            obtain ⟨L2, h2⟩ := IB r
            refine ⟨L1 ++ L2, rootedCactus_append hsep (fun x hxB hx => ?_) h1 h2⟩
            rcases hx with rfl | hxA
            · rfl
            · exact absurd ⟨x, hxA, hxB⟩ hv
          · obtain ⟨L1, h1⟩ := IB r
            obtain ⟨L2, h2⟩ := IA r
            refine ⟨L1 ++ L2, rootedCactus_append hsep' (fun x hxA hx => ?_) h1 h2⟩
            rcases hx with rfl | hxB
            · rfl
            · exact absurd ⟨x, hxA, hxB⟩ hv
    · refine ⟨[], fun X hX => absurd hX List.not_mem_nil, fun e he => ?_, fun L₁ L₂ X hL => ?_,
        fun X hX => absurd hX List.not_mem_nil⟩
      · exfalso
        induction e using Sym2.ind with
        | h x y => exact hne ⟨x, y, he⟩
      · exact absurd hL.symm (by simp)

/-- **every block of G is a cycle or a single edge → IsCactus G**, for finite G -/
theorem blocks_imp_isCactus [Finite V] (G : SimpleGraph V) (hB : BlocksCycleOrEdge G) : IsCactus G := by
  rcases isEmpty_or_nonempty V with hV | hV
  · refine ⟨[], fun X hX => absurd hX List.not_mem_nil, fun e _ => ?_, fun L₁ L₂ X hL => ?_⟩
    · exfalso
      induction e using Sym2.ind with
      | h x y => exact isEmptyElim x
    · exact absurd hL.symm (by simp)
  · obtain ⟨r⟩ := hV
    obtain ⟨L, hval, hcov, hover, -⟩ := rootedCactus_exists _ G rfl hB r
    exact ⟨L, hval, hcov, overlap_of_overlapR hover⟩

/-- **the fidelity of Theorem 1.1**: for a finite graph, the package's `IsCactus G` (an ordered block list) holds exactly when every
block of G is a cycle or a single edge -/
theorem isCactus_iff_blocks [Finite V] (G : SimpleGraph V) : IsCactus G ↔ BlocksCycleOrEdge G :=
  ⟨isCactus_imp_blocks G, blocks_imp_isCactus G⟩

/-- **Theorem 1.1 in the paper's form**: H1 discharged (G2S0.SphereIso), the hypothesis on the blocks -/
theorem cactus_thm_blocks (N : ℕ) :
    ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d →
      ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
        ∀ J : Sym2 V → ℝ, Ferro G J → ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → G2pair N G J e f := by
  intro k d C hFH hK hR hCZ V _ _ G _ hB
  exact cactus_thm N (hSphereIso_holds N) k d C hFH hK hR hCZ V G (blocks_imp_isCactus G hB)

end G2Kernel

#print axioms G2Kernel.exists_sep
#print axioms G2Kernel.isBlock_of_restrict
#print axioms G2Kernel.rootedCactus_exists
#print axioms G2Kernel.blocks_imp_isCactus
#print axioms G2Kernel.isCactus_iff_blocks
#print axioms G2Kernel.cactus_thm_blocks
