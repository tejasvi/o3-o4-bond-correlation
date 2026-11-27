# STATEMENTS_S1_full: Theorem 1.1 of the paper with NO hypotheses (merge of stages S0, S1, S2)

Every Lean statement in this file is about finite simple graphs (Mathlib's SimpleGraph); the paper's Theorems 1.1 and
1.2(b) also cover parallel edges through its Section 3.3 reduction, which is not formalized.

Module G2S1.TopFull (src/G2S1/TopFull.lean, sha8 259a19a9 (audited as 4b8a08d0; only comment lines differ, see FROZEN_TO_SHIPPED_S1.tsv)). Axioms: AXIOMS_S1_public.txt (standard three only).
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Theorem 1.1 (cycles and cacti), tex lines
108-111: "Let N ≥ 2 and let every block of G be a cycle or a single edge. Then Cov(s_e,s_f) ≥ 0 for every pair of edges
e ≠ f and all couplings J ≥ 0. The inequality is strict when e and f lie on a common cycle whose couplings are all
positive."

```lean
theorem cactus_thm_full (N : ℕ) (hN : 2 ≤ N) :
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J → ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → G2pair N G J e f
theorem cactus_strict_full (N : ℕ) (hN : 2 ≤ N) :
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J →
      ∀ (n : ℕ) (φ : Fin n → V), 3 ≤ n → Function.Injective φ →
        (∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) →
        (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
        ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
          0 < gibbsCov N G J (bond e) (bond f)
```
- Objects (package G2Kernel.Defs, unchanged): finite simple graph G on V; ω the normalized rotation-invariant measure on
  S^{N-1}; `gibbsCov N G J (bond e) (bond f)` = Cov(s_e, s_f) for the O(N) Gibbs measure with couplings J;
  `G2pair N G J e f` = 0 ≤ that covariance; `Ferro G J` = J_e ≥ 0 on every edge.
- `BlocksCycleOrEdge G`: every block (maximal 2-connected subgraph or bridge) of G is a cycle or a single edge (S0,
  G2S0.BlocksA). The strict part's "common cycle": an injective φ : Fin n → V, n ≥ 3,
  along edges of G, with J > 0 on its edges (S0, G2S0.BlocksC, in the form of the paper).
- The only premise is N ≥ 2. The named hypotheses H1-H5 of the package are all theorems: H1 `hSphereIso_holds` (S0),
  H2 `hFH_conc` and H5 `hCycleZ_conc` (S1), H3 `hKReg_kConc` (S0), H4 `hRatio_kConc` (S2, G2S2.Ratio: a copy of the module of
  stage S2, sha256 c7631cbb…), and d > 0
  `dConc_pos` (S0).
- Proofs: `cactus_thm_S1 N hN (hRatio_kConc N hN)`, `cactus_strict_S1 N hN (hRatio_kConc N hN)` (G2S1.TopS1).

Also done: d_ℓ = rank of the projection with kernel Π_ℓ, G2S1.RankTie (sha8 44e30cf4, 301 lines):
`projOp_of_mem`, `projOp_mem`, `finrank_zonalSpan` (= d_ℓ); see STATEMENTS_S1_v3_public.md.
