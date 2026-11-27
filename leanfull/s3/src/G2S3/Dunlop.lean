/-
G2S3.Dunlop (stage S3, Part B7): Theorem 3.2 for two edges with a common vertex (tex l.322) at N = 3 and N = 4, i.e. the
named hypothesis H6 `hShared N` (G2Kernel.Named) is a theorem for N = 3 and N = 4.
Site data:
- N = 4: S^3 with two rotation planes, plane-1 angular system the circle (Ginibre), Phi4, param4; the field direction
  is the coordinate 2 = tau cos b ([Du76, Thm 1 (2.14)] with the paper's Lemma 3.3).
- N = 3: S^2 with the sign of the coordinate 0 as plane-1 angular system (Griffiths) and one rotation plane, Phi3,
  param3; the field direction is the coordinate 1 = tau cos b ([Du76, Thm 2 (3.1)], a = 3, re-proved in the same frame).
-/
import G2S3.GKSz

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

local instance instFactTwoPiPosD : Fact (0 < 2 * π) := ⟨Real.two_pi_pos⟩

instance : IsProbabilityMeasure nu4 := by
  have := omega_isProbabilityMeasure 4 (by norm_num)
  have hm : Measurable r4 :=
    (Real.continuous_sqrt.comp (((continuous_coordA 0).pow 2).add ((continuous_coordA 1).pow 2))).measurable
  constructor
  unfold nu4
  rw [Measure.map_apply hm MeasurableSet.univ, Set.preimage_univ, measure_univ]

instance : IsProbabilityMeasure nu3 := by
  have := omega_isProbabilityMeasure 3 (by norm_num)
  have hm : Measurable r3 := (continuous_coordA 0).abs.measurable
  constructor
  unfold nu3
  rw [Measure.map_apply hm MeasurableSet.univ, Set.preimage_univ, measure_univ]

/-- The field direction for `N = 4`: the coordinate 2. -/
def u4 : Sph 4 := ⟨WithLp.toLp 2 ![0, 0, 1, 0], mem_sph_of_sum _ (by simp [Fin.sum_univ_four])⟩

/-- The field direction for `N = 3`: the coordinate 1. -/
def u3 : Sph 3 := ⟨WithLp.toLp 2 ![0, 1, 0], mem_sph_of_sum _ (by simp [Fin.sum_univ_three])⟩

theorem dot_Phi4 (c d : ℝ × (Tor × Tor)) :
    dot (Phi4 c) (Phi4 d) = rhoF c.1 * rhoF d.1 * tcos (c.2.1 - d.2.1) + tauF c.1 * tauF d.1 * tcos (c.2.2 - d.2.2) := by
  rw [dot_eq_sum, Fin.sum_univ_four, Phi4_coord, Phi4_coord, tcos_sub, tcos_sub]
  simp
  ring

theorem dot_u4_Phi4 (c : ℝ × (Tor × Tor)) : dot u4 (Phi4 c) = tauF c.1 * tcos c.2.2 := by
  rw [dot_eq_sum, Fin.sum_univ_four, Phi4_coord]
  simp [u4]

theorem dot_Phi3 (c d : ℝ × (Bool × Tor)) :
    dot (Phi3 c) (Phi3 d) = rhoF c.1 * rhoF d.1 * (sg c.2.1 * sg d.2.1) + tauF c.1 * tauF d.1 * tcos (c.2.2 - d.2.2) := by
  rw [dot_eq_sum, Fin.sum_univ_three, Phi3_coord, Phi3_coord, tcos_sub]
  simp
  ring

theorem dot_u3_Phi3 (c : ℝ × (Bool × Tor)) : dot u3 (Phi3 c) = tauF c.1 * tcos c.2.2 := by
  rw [dot_eq_sum, Fin.sum_univ_three, Phi3_coord]
  simp [u3]

theorem chi_one (b : Bool) : chi b 1 = sg b := by cases b <;> simp [chi, sg]
theorem chi_neg_one (b : Bool) : chi b (-1) = sg b := by cases b <;> simp [chi, sg]
theorem chi_zero (b : Bool) : chi b 0 = 1 := by cases b <;> simp [chi]

theorem cising_nvec {W : Type*} [Fintype W] [DecidableEq W] {p q : W} (hpq : p ≠ q) (ε : W → Bool) :
    cising (nvec p q) ε = sg (ε p) * sg (ε q) := by
  unfold cising
  have e : ∀ z, chi (ε z) (nvec p q z) = (if z = p then sg (ε z) else 1) * (if z = q then sg (ε z) else 1) := by
    intro z
    by_cases hp : z = p
    · rw [hp]
      have h1 : nvec p q p = 1 := by simp [nvec, hpq]
      rw [h1, chi_one, if_pos rfl, if_neg hpq, mul_one]
    · by_cases hq : z = q
      · rw [hq]
        have hqp : ¬ q = p := fun h => hp (hq.trans h)
        have h1 : nvec p q q = -1 := by simp [nvec, hqp]
        rw [h1, chi_neg_one, if_neg hqp, if_pos rfl, one_mul]
      · have h1 : nvec p q z = 0 := by simp [nvec, hp, hq]
        rw [h1, chi_zero, if_neg hp, if_neg hq, one_mul]
  rw [Finset.prod_congr rfl (fun z _ => e z), Finset.prod_mul_distrib, Finset.prod_ite_eq', Finset.prod_ite_eq']
  simp

/-- **H6 at `N = 4`** (Theorem 3.2, edge-pair case, tex l.322). -/
theorem hShared_holds4 : hShared 4 := by
  intro V _ _ G _ J hJ e he f hf _hef ⟨v, hve, hvf⟩
  obtain ⟨x, rfl⟩ := Sym2.mem_iff_exists.mp hve
  obtain ⟨y, rfl⟩ := Sym2.mem_iff_exists.mp hvf
  have hadjx : G.Adj v x := he
  have hadjy : G.Adj v y := hf
  have hx : ¬ x = v := fun h => hadjx.ne h.symm
  have hy : ¬ y = v := fun h => hadjy.ne h.symm
  unfold G2pair
  refine gksz_generic (N := 4) (by norm_num) (AddCircle.haarAddCircle : Measure Tor) nu4 Phi4 param4 u4 v
    (ccos (V := {i // ¬ i = v})) (fun n => (continuous_ccos n).measurable) (fun n θ => abs_ccos_le n θ)
    (fun L => gin_circle L) ?_ ?_ G J hJ x y hx hy
  · intro r a b p q hpq
    rw [dot_Phi4]
    simp only [ccos, dotT_nvec]
  · intro r a b q
    rw [dot_u4_Phi4]
    simp only [ccos, dotT_dvec]

/-- **H6 at `N = 3`** (Theorem 3.2, edge-pair case, tex l.322). -/
theorem hShared_holds3 : hShared 3 := by
  intro V _ _ G _ J hJ e he f hf _hef ⟨v, hve, hvf⟩
  obtain ⟨x, rfl⟩ := Sym2.mem_iff_exists.mp hve
  obtain ⟨y, rfl⟩ := Sym2.mem_iff_exists.mp hvf
  have hadjx : G.Adj v x := he
  have hadjy : G.Adj v y := hf
  have hx : ¬ x = v := fun h => hadjx.ne h.symm
  have hy : ¬ y = v := fun h => hadjy.ne h.symm
  unfold G2pair
  refine gksz_generic (N := 3) (by norm_num) unifB nu3 Phi3 param3 u3 v
    (cising (V := {i // ¬ i = v})) (fun n => measurable_of_finite _) (fun n ε => (abs_cising n ε).le)
    (fun L => gin_ising L) ?_ ?_ G J hJ x y hx hy
  · intro r a b p q hpq
    rw [dot_Phi3, cising_nvec hpq]
    simp only [ccos, dotT_nvec]
  · intro r a b q
    rw [dot_u3_Phi3]
    simp only [ccos, dotT_dvec]

end G2S3

#print axioms G2S3.hShared_holds4
#print axioms G2S3.hShared_holds3
