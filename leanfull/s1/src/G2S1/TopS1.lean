/-
G2S1.TopS1 (stage S1, summary): Theorem 1.1 with H2 and H5 discharged, and the axiom report of the S1 exports.
- `cactus_thm_S1` (T1) and `cactus_strict_S1` (T2, strict part) take the paper's data k, d, C̃ and N ≥ 2; H1 (S0), H2
  (`hFH_conc`), H3 (S0), H5 (`hCycleZ_conc`) are theorems; the one premise left is H4 = `hRatio (kConc N)` (stage S2).
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Theorem 1.1.
-/
import G2S0.BlocksC
import G2S1.CycleZ

noncomputable section

namespace G2Kernel

/-- T1 (Theorem 1.1) for the paper's data: H1, H2, H3, H5 discharged; the premise left is H4 (stage S2) -/
theorem cactus_thm_S1 (N : ℕ) (hN : 2 ≤ N) : hRatio (kConc N) →
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J → ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → G2pair N G J e f :=
  fun hR => cactus_thm_blocks N (kConc N) (dConc N) (CConc N) (hFH_conc N hN) (hKReg_kConc N hN) hR
    (hCycleZ_conc N hN)

/-- T2 (Theorem 1.1, strict part) for the paper's data: H1, H2, H3, H5 and d > 0 discharged; H4 left -/
theorem cactus_strict_S1 (N : ℕ) (hN : 2 ≤ N) : hRatio (kConc N) →
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J →
      ∀ (n : ℕ) (φ : Fin n → V), 3 ≤ n → Function.Injective φ →
        (∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) →
        (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
        ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
          0 < gibbsCov N G J (bond e) (bond f) :=
  fun hR => cactus_strict_concrete N hN (hFH_conc N hN) hR (hCycleZ_conc N hN)

end G2Kernel

#print axioms G2Kernel.hFH_conc
#print axioms G2Kernel.hCycleZ_conc
#print axioms G2Kernel.cactus_thm_S1
#print axioms G2Kernel.cactus_strict_S1
#print axioms G2Kernel.zonal_proj
#print axioms G2Kernel.abs_CConc_le_one
#print axioms G2Kernel.abs_zonal_le
#print axioms G2Kernel.exp_dot_hasSum
#print axioms G2Kernel.summable_kConc_dConc
#print axioms G2Kernel.kConc_eq_integral
#print axioms G2Kernel.zonal_posDef
#print axioms G2Kernel.exp_exp_integral_hasSum
#print axioms G2Kernel.partition_hasSum_labels
#print axioms G2Kernel.abs_labelWeight_le
#print axioms G2Kernel.labelWeight_cycle
#print axioms G2Kernel.sphere_moment
#print axioms G2Kernel.two_point_CF
