/-
G2S1.TopS1c (stage S1, final summary after the S0-S2 merge and the rank tie): imports every module of the S1 tree and
reports the axioms of Theorem 1.1 with no hypotheses and of the rank tie. Successor of G2S1.TopS1b (sha8 a51410d2,
unchanged), whose report covers the other exports.
-/
import G2S1.TopS1b
import G2S1.TopFull
import G2S1.RankTie

-- Theorem 1.1, both parts, every N ≥ 2, no hypotheses (with S2's H4)
#print axioms G2Kernel.hRatio_kConc
#print axioms G2Kernel.cactus_thm_full
#print axioms G2Kernel.cactus_strict_full
-- d_ℓ = rank of the projection with kernel Π_ℓ
#print axioms G2Kernel.finiteDimensional_zonalSpan
#print axioms G2Kernel.projOp_of_mem
#print axioms G2Kernel.projOp_mem
#print axioms G2Kernel.finrank_zonalSpan
