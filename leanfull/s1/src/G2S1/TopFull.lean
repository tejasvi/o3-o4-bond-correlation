/-
G2S1.TopFull (stages S0, S1, S2 merged): Theorem 1.1 of the paper, both parts, for the O(N) model at every N ≥ 2, in the
paper's block form, with NO hypotheses.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Theorem 1.1 (cycles and cacti):
"Let N ≥ 2 and let every block of G be a cycle or a single edge. Then Cov(s_e, s_f) ≥ 0 for every pair of edges e ≠ f
and all couplings J ≥ 0. The inequality is strict when e and f lie on a common cycle whose couplings are all positive."
The named hypotheses of the package's Theorem 1.1 are all theorems here:
- H1 `hSphereIso`: `hSphereIso_holds` (S0, G2S0.SphereIso), used inside `cactus_thm_blocks` / `cactus_strict_thm_blocks`;
- H2 `hFH`: `hFH_conc` (S1, G2S1.Expand); H5 `hCycleZ`: `hCycleZ_conc` (S1, G2S1.CycleZ);
- H3 `hKReg`: `hKReg_kConc` (S0, G2S0.KData); d > 0: `dConc_pos` (S0, G2S0.BlocksC);
- H4 `hRatio`: `hRatio_kConc` (S2, G2S2.Ratio, a copy of the module of stage S2, sha256 c7631cbb…,
  unchanged).
The graph class `BlocksCycleOrEdge G` (every block of G is a cycle or a single edge) and the strict part's "common
cycle" (an injective φ : Fin n → V, n ≥ 3, along edges of G) are S0's paper forms (G2S0.BlocksA, G2S0.BlocksC).
-/
import G2S1.TopS1
import G2S2.Ratio

noncomputable section

namespace G2Kernel

/-- **Theorem 1.1** (nonstrict part), no hypotheses: for N ≥ 2, on every finite graph whose blocks are cycles or single
edges, with couplings J_e ≥ 0, any two distinct edges have Cov(s_e, s_f) ≥ 0. -/
theorem cactus_thm_full (N : ℕ) (hN : 2 ≤ N) :
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J → ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → G2pair N G J e f :=
  cactus_thm_S1 N hN (hRatio_kConc N hN)

/-- **Theorem 1.1** (strict part), no hypotheses: for N ≥ 2, on every finite graph whose blocks are cycles or single
edges, with couplings J_e ≥ 0, two distinct edges of a common cycle whose couplings are all positive have
Cov(s_e, s_f) > 0. -/
theorem cactus_strict_full (N : ℕ) (hN : 2 ≤ N) :
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J →
      ∀ (n : ℕ) (φ : Fin n → V), 3 ≤ n → Function.Injective φ →
        (∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) →
        (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
        ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
          0 < gibbsCov N G J (bond e) (bond f) :=
  cactus_strict_S1 N hN (hRatio_kConc N hN)

end G2Kernel

#print axioms G2Kernel.hRatio_kConc
#print axioms G2Kernel.cactus_thm_full
#print axioms G2Kernel.cactus_strict_full
