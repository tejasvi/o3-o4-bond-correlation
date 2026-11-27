/-
G2S1.TopS1b (stage S1, final summary): every S1 module, and the axiom report of all exported theorems.
Successor of G2S1.TopS1 (sha8 61f229c6, unchanged), adding Proposition 2.1 (G2S1.Prop21) and the tie of the data to the
paper's objects (G2S1.Tie, G2S1.GenFun).
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.1, Proposition 2.1, Section 3.1,
Theorem 1.1.
-/
import G2S1.TopS1
import G2S1.Prop21
import G2S1.GenFun

-- H2, H5 and Theorem 1.1 (only H4 left)
#print axioms G2Kernel.hFH_conc
#print axioms G2Kernel.hCycleZ_conc
#print axioms G2Kernel.cactus_thm_S1
#print axioms G2Kernel.cactus_strict_S1
-- displays (2), (3), (4) and the exports to S3
#print axioms G2Kernel.zonal_proj
#print axioms G2Kernel.zonal_symm
#print axioms G2Kernel.zonal_self
#print axioms G2Kernel.continuous_zonal
#print axioms G2Kernel.abs_CConc_le_one
#print axioms G2Kernel.abs_zonal_le
#print axioms G2Kernel.exp_dot_hasSum
#print axioms G2Kernel.summable_kConc_dConc
#print axioms G2Kernel.kConc_eq_integral
#print axioms G2Kernel.zonal_posDef
#print axioms G2Kernel.exp_exp_integral_hasSum
#print axioms G2Kernel.abs_labelWeight_le
#print axioms G2Kernel.partition_hasSum_labels
#print axioms G2Kernel.labelWeight_cycle
-- Proposition 2.1
#print axioms G2Kernel.hasSum_labelLaw
#print axioms G2Kernel.prop21
-- the tie
#print axioms G2Kernel.CConc_two_cos
#print axioms G2Kernel.CConc_two_eq_chebyshevT
#print axioms G2Kernel.CConc_four_eq_chebyshevU
#print axioms G2Kernel.dConc_three
#print axioms G2Kernel.dConc_four
#print axioms G2Kernel.integral_CConc_mul
#print axioms G2Kernel.integral_CConc_sq
#print axioms G2Kernel.integral_CConc_sq_muN
#print axioms G2Kernel.kConc_eq_integral_muN
#print axioms G2Kernel.natDegree_cPoly
#print axioms G2Kernel.CConc_unique
#print axioms G2Kernel.gegenbauer_genFun
-- the sphere fact and the algebra behind (2)
#print axioms G2Kernel.sphere_moment
#print axioms G2Kernel.two_point_CF
#print axioms G2Kernel.pow_eq_sum_zon
#print axioms G2Kernel.star_Rz
#print axioms G2Kernel.coord_zonPoly
