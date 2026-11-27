/-
G2S0.BlocksC (S0 follow-up, AUDIT_S0_v1 item 7): the strict part of Theorem 1.1 in the paper's form.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Theorem 1.1, second sentence: the inequality is strict
when e and f lie on a common cycle whose couplings are all positive.
- `cycle_le_cycle`: a cycle inside a cycle is the whole cycle (each vertex of the inner cycle has its two neighbours of the outer
  one, so the inner vertex set is closed under the outer adjacency, and the outer cycle is connected).
- `cycle_mem_list`: every cycle of G is a cycle block of any cactus list of G, with the same edges (its edges lie in one block of the
  list, `edges_in_one_block`; that block is a cycle containing it).
- `cactus_strict_thm_blocks`: the strict part with the hypothesis on the blocks and "a common cycle" (H1 discharged).
- `dConc_pos` and `cactus_strict_concrete`: the paper's data, with H1, H3 and the positivity of d discharged.
A cycle of G is given by n ≥ 3 and an injective φ : Fin n → V whose cycle edges are edges of G; its edges are
`(CactusBlock.cycle n φ).edges`.
-/
import G2S0.BlocksB
import G2S0.KData

noncomputable section

namespace G2Kernel

open SimpleGraph

variable {V : Type*}

/-! ### Cycles -/

theorem fin_succ_ne_pred {k : ℕ} (a : Fin (k + 3)) : a + 1 ≠ a - 1 := by
  intro h
  have h2 : a + (1 + 1) = a + 0 := by
    calc a + (1 + 1) = (a + 1) + 1 := by rw [add_assoc]
      _ = (a - 1) + 1 := by rw [h]
      _ = a + 0 := by rw [sub_add_cancel, add_zero]
  have h3 : (1 + 1 : Fin (k + 3)) = 0 := add_left_cancel h2
  have h4 := congrArg Fin.val h3
  rw [Fin.val_add] at h4
  have h1 : (1 : Fin (k + 3)).val = 1 := rfl
  rw [h1, Fin.val_zero] at h4
  have h5 : (1 + 1) % (k + 3) = 2 := Nat.mod_eq_of_lt (by omega)
  omega

/-- the two neighbours of a vertex of a cycle -/
theorem cycle_adj_at {m : ℕ} {ψ : Fin (m + 3) → V} (hψ : Function.Injective ψ) (b : Fin (m + 3)) (w : V) :
    (blockSG (CactusBlock.cycle (m + 3) ψ)).Adj (ψ b) w ↔ w = ψ (b + 1) ∨ w = ψ (b - 1) := by
  rw [cycle_adj_iff hψ]
  constructor
  · rintro ⟨a, c, hac, hab, rfl⟩
    have hab' : a = b := (hψ hab).symm
    subst hab'
    rcases (cycleGraph_adj (n := m + 1)).mp hac with h | h
    · have h' : a - c = (1 : Fin (m + 3)) := h
      right
      congr 1
      rw [← h', sub_sub_cancel]
    · have h' : c - a = (1 : Fin (m + 3)) := h
      left
      congr 1
      rw [← h', add_comm a (c - a), sub_add_cancel]
  · rintro (rfl | rfl)
    · exact ⟨b, b + 1, cycle_adj_add_one b, rfl, rfl⟩
    · refine ⟨b, b - 1, ?_, rfl, rfl⟩
      have h := cycle_adj_add_one (b - 1)
      rw [sub_add_cancel] at h
      exact h.symm

theorem two_set_cover {α : Type*} {x1 x2 u1 u2 w : α} (hne : x1 ≠ x2) (h1 : x1 = u1 ∨ x1 = u2)
    (h2 : x2 = u1 ∨ x2 = u2) (hw : w = u1 ∨ w = u2) : w = x1 ∨ w = x2 := by
  rcases h1 with rfl | rfl <;> rcases h2 with rfl | rfl <;> rcases hw with rfl | rfl <;> simp_all

/-- **a cycle inside a cycle is the whole cycle** -/
theorem cycle_le_cycle {n m : ℕ} (hn : 3 ≤ n) (hm : 3 ≤ m) {φ : Fin n → V} {ψ : Fin m → V}
    (hφ : Function.Injective φ) (hψ : Function.Injective ψ)
    (hle : blockSG (CactusBlock.cycle n φ) ≤ blockSG (CactusBlock.cycle m ψ)) :
    blockSG (CactusBlock.cycle m ψ) ≤ blockSG (CactusBlock.cycle n φ) := by
  obtain ⟨n', rfl⟩ : ∃ n', n = n' + 3 := ⟨n - 3, by omega⟩
  obtain ⟨m', rfl⟩ : ∃ m', m = m' + 3 := ⟨m - 3, by omega⟩
  have hA : ∀ a w, (blockSG (CactusBlock.cycle (m' + 3) ψ)).Adj (φ a) w →
      (blockSG (CactusBlock.cycle (n' + 3) φ)).Adj (φ a) w := by
    intro a w hw
    have hD1 : (blockSG (CactusBlock.cycle (n' + 3) φ)).Adj (φ a) (φ (a + 1)) :=
      (cycle_adj_at hφ a _).mpr (Or.inl rfl)
    have hD2 : (blockSG (CactusBlock.cycle (n' + 3) φ)).Adj (φ a) (φ (a - 1)) :=
      (cycle_adj_at hφ a _).mpr (Or.inr rfl)
    obtain ⟨b, hb⟩ := vsupp_cycle ψ ⟨φ (a + 1), hle hD1⟩
    have hE1 : (blockSG (CactusBlock.cycle (m' + 3) ψ)).Adj (ψ b) (φ (a + 1)) := by
      rw [← hb]
      exact hle hD1
    have hE2 : (blockSG (CactusBlock.cycle (m' + 3) ψ)).Adj (ψ b) (φ (a - 1)) := by
      rw [← hb]
      exact hle hD2
    rw [hb] at hw
    have h1 := (cycle_adj_at hψ b (φ (a + 1))).mp hE1
    have h2 := (cycle_adj_at hψ b (φ (a - 1))).mp hE2
    have hw' := (cycle_adj_at hψ b w).mp hw
    have hne : φ (a + 1) ≠ φ (a - 1) := fun h => fin_succ_ne_pred a (hφ h)
    rcases two_set_cover hne h1 h2 hw' with rfl | rfl
    · exact hD1
    · exact hD2
  have hB : ∀ p q, (blockSG (CactusBlock.cycle (m' + 3) ψ)).Adj p q → p ∈ Set.range φ → q ∈ Set.range φ := by
    rintro p q hpq ⟨a, rfl⟩
    obtain ⟨c, hc⟩ := vsupp_cycle φ ⟨φ a, (hA a q hpq).symm⟩
    exact ⟨c, hc.symm⟩
  intro x y hxy
  have hEc := connNoCut_cycle hm hψ
  have h0 : φ 0 ∈ vsupp (blockSG (CactusBlock.cycle (m' + 3) ψ)) :=
    ⟨φ (0 + 1), hle ((cycle_adj_at hφ 0 _).mpr (Or.inl rfl))⟩
  have hx : x ∈ vsupp (blockSG (CactusBlock.cycle (m' + 3) ψ)) := ⟨y, hxy⟩
  obtain ⟨a, rfl⟩ := reach_closed hB (hEc.1 _ h0 _ hx) ⟨0, rfl⟩
  exact hA a y hxy

theorem cycle_edges_ne {m : ℕ} {ψ : Fin m → V} (hψ : Function.Injective ψ) {x y : V}
    (h : s(x, y) ∈ (CactusBlock.cycle m ψ).edges) : x ≠ y := by
  obtain ⟨g, hg, hgxy⟩ := h
  induction g using Sym2.ind with
  | h a c =>
    rw [SimpleGraph.mem_edgeSet] at hg
    rw [Sym2.map_mk, Sym2.eq_iff] at hgxy
    intro hxy
    subst hxy
    rcases hgxy with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact hg.ne (hψ (h1.trans h2.symm))
    · exact hg.ne (hψ (h1.trans h2.symm))

/-- **every cycle of G is a cycle block of any cactus list of G**, with the same edges -/
theorem cycle_mem_list {G : SimpleGraph V} {L : List (CactusBlock V)} (hL : IsCactusWith G L) {n : ℕ} {φ : Fin n → V}
    (hn : 3 ≤ n) (hφ : Function.Injective φ) (hG : ∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) :
    ∃ (m : ℕ) (ψ : Fin m → V), CactusBlock.cycle m ψ ∈ L ∧ (CactusBlock.cycle m ψ).edges = (CactusBlock.cycle n φ).edges := by
  obtain ⟨hval, hcov, hover⟩ := hL
  have hDc := connNoCut_cycle hn hφ
  obtain ⟨n', rfl⟩ : ∃ n', n = n' + 3 := ⟨n - 3, by omega⟩
  have hD0 : (blockSG (CactusBlock.cycle (n' + 3) φ)).Adj (φ 0) (φ (0 + 1)) := (cycle_adj_at hφ 0 _).mpr (Or.inl rfl)
  have hD0' : (blockSG (CactusBlock.cycle (n' + 3) φ)).Adj (φ 0) (φ (0 - 1)) := (cycle_adj_at hφ 0 _).mpr (Or.inr rfl)
  have hE : ∀ x y, (blockSG (CactusBlock.cycle (n' + 3) φ)).Adj x y → s(x, y) ∈ listEdges L := by
    intro x y hxy
    apply hcov
    obtain ⟨a, c, hac, rfl, rfl⟩ := (cycle_adj_iff hφ x y).mp hxy
    exact hG a c hac
  obtain ⟨X, hXL, hXE⟩ := edges_in_one_block hDc ⟨_, _, hD0⟩ L hover hE
  cases X with
  | edge e =>
    exfalso
    have h1 : s(φ 0, φ (0 + 1)) = e := hXE _ _ hD0
    have h2 : s(φ 0, φ (0 - 1)) = e := hXE _ _ hD0'
    have h3 : φ (0 + 1) = φ (0 - 1) := Sym2.congr_right.mp (h1.trans h2.symm)
    exact fin_succ_ne_pred 0 (hφ h3)
  | cycle m ψ =>
    have hXG := hval _ hXL
    refine ⟨m, ψ, hXL, ?_⟩
    have hle : blockSG (CactusBlock.cycle (n' + 3) φ) ≤ blockSG (CactusBlock.cycle m ψ) :=
      fun x y h => (blockSG_adj _ x y).mpr ⟨hXE x y h, SimpleGraph.Adj.ne h⟩
    have hge := cycle_le_cycle hn hXG.1 hφ hXG.2.1 hle
    ext g
    induction g using Sym2.ind with
    | h x y =>
      constructor
      · intro hg
        have hxy : x ≠ y := cycle_edges_ne hXG.2.1 hg
        exact ((blockSG_adj _ x y).mp (hge ((blockSG_adj _ x y).mpr ⟨hg, hxy⟩))).1
      · intro hg
        have hxy : x ≠ y := cycle_edges_ne hφ hg
        exact hXE x y ((blockSG_adj _ x y).mpr ⟨hg, hxy⟩)

/-! ### The strict part of Theorem 1.1 -/

/-- **Theorem 1.1, strict part, in the paper's form**: on a finite graph whose blocks are cycles or single edges, two distinct
edges of a common cycle whose couplings are all positive have positive covariance (H1 discharged) -/
theorem cactus_strict_thm_blocks (N : ℕ) :
    ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d → (∀ c, 0 < d c) →
      ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
        ∀ J : Sym2 V → ℝ, Ferro G J →
        ∀ (n : ℕ) (φ : Fin n → V), 3 ≤ n → Function.Injective φ →
          (∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) →
          (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
          ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
            0 < gibbsCov N G J (bond e) (bond f) := by
  intro k d C hFH hK hR hCZ hd V _ _ G _ hB J hJ n φ hn hφ hG hpos e he f hf hef
  obtain ⟨L, hL⟩ := blocks_imp_isCactus G hB
  obtain ⟨m, ψ, hmem, hedges⟩ := cycle_mem_list hL hn hφ hG
  rw [← hedges] at hpos he hf
  exact cactus_strict_thm N (hSphereIso_holds N) k d C hFH hK hR hCZ hd V G L hL J hJ m ψ hmem hpos e he f hf hef

/-- d_ℓ > 0 for the paper's d, N ≥ 2 -/
theorem dConc_pos (N : ℕ) (hN : 2 ≤ N) (l : ℕ) : 0 < dConc N l := by
  unfold dConc
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 2 := ⟨N - 2, by omega⟩
  rcases Nat.lt_or_ge l 2 with hl | hl
  · rw [if_neg (by omega), sub_zero]
    exact_mod_cast Nat.choose_pos (by omega)
  · rw [if_pos hl]
    obtain ⟨j, rfl⟩ : ∃ j, l = j + 2 := ⟨l - 2, by omega⟩
    have e1 : j + 2 + (M + 2) - 1 = j + M + 3 := by omega
    have e2 : j + 2 + (M + 2) - 3 = j + M + 1 := by omega
    have e3 : j + 2 - 2 = j := by omega
    rw [e1, e2, e3]
    have p1 : Nat.choose (j + M + 3) (j + 2) = Nat.choose (j + M + 2) (j + 1) + Nat.choose (j + M + 2) (j + 2) :=
      Nat.choose_succ_succ _ _
    have p2 : Nat.choose (j + M + 2) (j + 1) = Nat.choose (j + M + 1) j + Nat.choose (j + M + 1) (j + 1) :=
      Nat.choose_succ_succ _ _
    have p3 : 0 < Nat.choose (j + M + 2) (j + 2) := Nat.choose_pos (by omega)
    have hlt : Nat.choose (j + M + 1) j < Nat.choose (j + M + 3) (j + 2) := by omega
    have hlt' : (Nat.choose (j + M + 1) j : ℝ) < (Nat.choose (j + M + 3) (j + 2) : ℝ) := by exact_mod_cast hlt
    linarith

/-- the strict part for the paper's data (N ≥ 2): H1, H3 and the positivity of d discharged; H2, H4 and H5 remain -/
theorem cactus_strict_concrete (N : ℕ) (hN : 2 ≤ N) :
    hFH N (kConc N) (dConc N) (CConc N) → hRatio (kConc N) → hCycleZ N (kConc N) (dConc N) →
      ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
        ∀ J : Sym2 V → ℝ, Ferro G J →
        ∀ (n : ℕ) (φ : Fin n → V), 3 ≤ n → Function.Injective φ →
          (∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) →
          (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
          ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
            0 < gibbsCov N G J (bond e) (bond f) :=
  fun hF hR hC => cactus_strict_thm_blocks N (kConc N) (dConc N) (CConc N) hF (hKReg_kConc N hN) hR hC (dConc_pos N hN)

end G2Kernel

#print axioms G2Kernel.cycle_le_cycle
#print axioms G2Kernel.cycle_mem_list
#print axioms G2Kernel.cactus_strict_thm_blocks
#print axioms G2Kernel.dConc_pos
#print axioms G2Kernel.cactus_strict_concrete
