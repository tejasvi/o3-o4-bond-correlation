/-
G2S1.CycleZ (stage S1): H5 (`hCycleZ`) for the paper's data: the ring formula Z_{C_n} = Σ_c d_c ∏_g k_c(J_g), n ≥ 3.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 3.1 (Cycles and cacti).
The edges of `cycleGraph (m+2)` are s(j, j+1), j : Fin (m+2), each once (m ≥ 1); by display (4) and `cycF_integral`,
W(ℓ) = [ℓ constant = c] d_c, and the label series collapses to the constant labellings.
-/
import G2S1.Cycle

noncomputable section
open Real Finset MeasureTheory

namespace G2Kernel

/-- the edge s(j, j+1) of the cycle C_{m+2} -/
def cycEdge (m : ℕ) (j : Fin (m + 2)) : Sym2 (Fin (m + 2)) := s(j, j + 1)

theorem cycEdge_mem (m : ℕ) [DecidableRel (SimpleGraph.cycleGraph (m + 2)).Adj] (j : Fin (m + 2)) :
    cycEdge m j ∈ (SimpleGraph.cycleGraph (m + 2)).edgeFinset := by
  rw [SimpleGraph.mem_edgeFinset, cycEdge, SimpleGraph.mem_edgeSet, SimpleGraph.cycleGraph_adj]
  right
  simp

theorem fin_one_add_one_ne_zero (m : ℕ) (hm : 1 ≤ m) : (1 + 1 : Fin (m + 2)) ≠ 0 := by
  intro h
  have h' := congrArg Fin.val h
  rw [Fin.val_add, Fin.val_one, Fin.val_zero, Nat.mod_eq_of_lt (by omega)] at h'
  omega

theorem cycEdge_injective (m : ℕ) (hm : 1 ≤ m) : Function.Injective (cycEdge m) := by
  intro i j h
  unfold cycEdge at h
  rcases Sym2.eq_iff.mp h with ⟨h1, _⟩ | ⟨h1, h2⟩
  · exact h1
  · exfalso
    apply fin_one_add_one_ne_zero m hm
    have h3 : i + (1 + 1) = i + 0 := by
      calc i + (1 + 1) = (i + 1) + 1 := (add_assoc _ _ _).symm
        _ = j + 1 := by rw [h2]
        _ = i := h1.symm
        _ = i + 0 := (add_zero i).symm
    exact add_left_cancel h3

theorem cycEdge_surj (m : ℕ) [DecidableRel (SimpleGraph.cycleGraph (m + 2)).Adj] (e : Sym2 (Fin (m + 2)))
    (he : e ∈ (SimpleGraph.cycleGraph (m + 2)).edgeFinset) : ∃ j, cycEdge m j = e := by
  induction e using Sym2.ind with
  | h u v =>
    rw [SimpleGraph.mem_edgeFinset, SimpleGraph.mem_edgeSet, SimpleGraph.cycleGraph_adj] at he
    rcases he with h | h
    · refine ⟨v, ?_⟩
      unfold cycEdge
      rw [sub_eq_iff_eq_add] at h
      rw [h, add_comm (1 : Fin (m + 2)) v]
      exact Sym2.eq_swap
    · refine ⟨u, ?_⟩
      unfold cycEdge
      rw [sub_eq_iff_eq_add] at h
      rw [h, add_comm (1 : Fin (m + 2)) u]

/-- the edge j as an element of the edge type -/
def toE (m : ℕ) [DecidableRel (SimpleGraph.cycleGraph (m + 2)).Adj] (j : Fin (m + 2)) :
    (SimpleGraph.cycleGraph (m + 2)).edgeFinset := ⟨cycEdge m j, cycEdge_mem m j⟩

theorem toE_bijective (m : ℕ) (hm : 1 ≤ m) [DecidableRel (SimpleGraph.cycleGraph (m + 2)).Adj] :
    Function.Bijective (toE m) := by
  constructor
  · intro i j h
    exact cycEdge_injective m hm (congrArg Subtype.val h)
  · intro e
    obtain ⟨j, hj⟩ := cycEdge_surj m e.1 e.2
    exact ⟨j, Subtype.ext hj⟩

theorem prod_cyc (N m : ℕ) (b : Fin (m + 2) → ℕ) (σ : Fin (m + 2) → Sph N) :
    ∏ j : Fin (m + 2), zonal N (b j) (σ j) (σ (j + 1)) = cycF N (m + 1) b σ := by
  rw [Fin.prod_univ_castSucc]
  unfold cycF
  congr 1
  · refine Finset.prod_congr rfl (fun i _ => ?_)
    rw [Fin.coeSucc_eq_succ]
  · rw [Fin.last_add_one]

/-- W(ℓ) on the cycle: [ℓ constant = c] d_c -/
theorem labelWeight_cycle {N : ℕ} (hN : 2 ≤ N) (m : ℕ) (hm : 1 ≤ m)
    [DecidableRel (SimpleGraph.cycleGraph (m + 2)).Adj] (ℓ : (SimpleGraph.cycleGraph (m + 2)).edgeFinset → ℕ) :
    labelWeight N (SimpleGraph.cycleGraph (m + 2)) ℓ
      = if ∀ j, ℓ (toE m j) = ℓ (toE m 0) then dConc N (ℓ (toE m 0)) else 0 := by
  unfold labelWeight
  have hprod : ∀ σ : Config N (Fin (m + 2)),
      ∏ e : (SimpleGraph.cycleGraph (m + 2)).edgeFinset, (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 (Fin (m + 2))) σ))
        = cycF N (m + 1) (fun j => ℓ (toE m j)) σ := by
    intro σ
    rw [← prod_cyc]
    symm
    exact Fintype.prod_bijective (toE m) (toE_bijective m hm) _ _ (fun j => rfl)
  simp only [hprod]
  exact cycF_integral hN (m + 1) (fun j => ℓ (toE m j))

/-- **H5 for the paper's data** (N ≥ 2): Z_{C_n} = Σ_c d_c ∏_g k_c(J_g) for every n ≥ 3 -/
theorem hCycleZ_conc (N : ℕ) (hN : 2 ≤ N) : hCycleZ N (kConc N) (dConc N) := by
  intro n inst hn J
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 2 := ⟨n - 2, by omega⟩
  have hm : 1 ≤ m := by omega
  have hL := partition_hasSum_labels hN (SimpleGraph.cycleGraph (m + 2)) J
  set cst : ℕ → ((SimpleGraph.cycleGraph (m + 2)).edgeFinset → ℕ) := fun c _ => c with hcst
  have hinj : Function.Injective cst := fun c d h => congrFun h (toE m 0)
  have hzero : ∀ ℓ ∉ Set.range cst,
      labelWeight N (SimpleGraph.cycleGraph (m + 2)) ℓ *
        ∏ e : (SimpleGraph.cycleGraph (m + 2)).edgeFinset, kConc N (ℓ e) (J e) = 0 := by
    intro ℓ hℓ
    rw [labelWeight_cycle hN m hm, if_neg, zero_mul]
    intro hconst
    apply hℓ
    refine ⟨ℓ (toE m 0), ?_⟩
    funext e
    obtain ⟨j, hj⟩ := (toE_bijective m hm).2 e
    rw [← hj, hconst j]
  have h2 := (hinj.hasSum_iff hzero).mpr hL
  refine h2.congr_fun (fun c => ?_)
  simp only [Function.comp, hcst]
  rw [labelWeight_cycle hN m hm, if_pos (fun j => rfl)]
  rw [Finset.prod_coe_sort (SimpleGraph.cycleGraph (m + 2)).edgeFinset (fun e => kConc N c (J e))]

end G2Kernel
