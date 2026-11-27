/-
G2S3.Corner (stage S3, Part B8): the two edges at a corner of P_3 x P_n have positive covariance at N = 3 and N = 4,
for every coupling J > 0 and n >= 3; in particular the named hypothesis hCornerPair N (G2Kernel.NamedStrip) holds.
The corner c has the two neighbours x (vertical) and y (horizontal); the vertex w diagonal to c is adjacent to both,
so the path x - w - y avoids c and gksz_strict_generic applies. Paper: Corollary 3.8 (tex l.438), the conclusion
Cov(s_e, s_f) > 0, here without the label expansion (no S1, no Lemma 4.1, no Proposition 5.4).
-/
import G2S3.GKSzStrict

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

local instance instFactTwoPiPosC : Fact (0 < 2 * π) := ⟨Real.two_pi_pos⟩

theorem dot_u4 (s : Sph 4) : dot u4 s = (s : Amb 4) 2 := by
  rw [dot_eq_sum, Fin.sum_univ_four]
  simp [u4]

theorem dot_u3 (s : Sph 3) : dot u3 s = (s : Amb 3) 1 := by
  rw [dot_eq_sum, Fin.sum_univ_three]
  simp [u3]

/-- A corner of `P_3 × P_n` and two distinct neighbours have a common neighbour other than the corner. -/
theorem corner_witness {n : ℕ} (hn : 3 ≤ n) {c x y : Fin 3 × Fin n} (hc : isCorner n c) (hx : (strip n).Adj c x)
    (hy : (strip n).Adj c y) (hxy : x ≠ y) :
    ∃ w, w ≠ c ∧ (strip n).Adj x w ∧ (strip n).Adj w y := by
  rw [strip_adj_iff, box_adj] at hx hy
  obtain ⟨hc1, hc2⟩ := hc
  have hc1' : c.1.val = 0 ∨ c.1.val = 2 := by
    rcases hc1 with h | h
    · left; rw [h]; rfl
    · right; rw [h]; rfl
  have hx1 := x.1.isLt
  have hy1 := y.1.isLt
  have hc1l := c.1.isLt
  have hx2 := x.2.isLt
  have hy2 := y.2.isLt
  have hc2l := c.2.isLt
  have h1v : ((1 : Fin 3) : ℕ) = 1 := rfl
  have hxy' : ¬ (x.1.val = y.1.val ∧ x.2.val = y.2.val) := by
    intro h
    exact hxy (Prod.ext (Fin.ext h.1) (Fin.ext h.2))
  by_cases hxv : x.1.val = 1
  · -- x is the vertical neighbour, y the horizontal one
    refine ⟨((1 : Fin 3), y.2), ?_, ?_, ?_⟩
    · intro h
      have h1 : c.1.val = 1 := by rw [← h]; rfl
      omega
    · rw [strip_adj_iff, box_adj]
      dsimp only
      rw [h1v]
      omega
    · rw [strip_adj_iff, box_adj]
      dsimp only
      rw [h1v]
      omega
  · -- x is the horizontal neighbour, y the vertical one
    refine ⟨((1 : Fin 3), x.2), ?_, ?_, ?_⟩
    · intro h
      have h1 : c.1.val = 1 := by rw [← h]; rfl
      omega
    · rw [strip_adj_iff, box_adj]
      dsimp only
      rw [h1v]
      omega
    · rw [strip_adj_iff, box_adj]
      dsimp only
      rw [h1v]
      omega

/-- **The corner covariance at `N = 4`**: positive for every `J > 0`, `n ≥ 3`. -/
theorem corner_pos4 {n : ℕ} (hn : 3 ≤ n) {J : ℝ} (hJ : 0 < J) {e f : Sym2 (Fin 3 × Fin n)}
    (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet) (hef : e ≠ f) (hsc : seriesCorner n e f) :
    0 < gibbsCov 4 (strip n) (uniform J) (bond e) (bond f) := by
  obtain ⟨c, hc, hce, hcf⟩ := hsc
  obtain ⟨x, rfl⟩ := Sym2.mem_iff_exists.mp hce
  obtain ⟨y, rfl⟩ := Sym2.mem_iff_exists.mp hcf
  have hadjx : (strip n).Adj c x := he
  have hadjy : (strip n).Adj c y := hf
  have hxy : x ≠ y := fun h => hef (by rw [h])
  obtain ⟨w, hwc, hxw, hwy⟩ := corner_witness hn hc hadjx hadjy hxy
  refine gksz_strict_generic (N := 4) (by norm_num) (AddCircle.haarAddCircle : Measure Tor) nu4 Phi4 param4 u4
    2 dot_u4 c (ccos (V := {i // ¬ i = c})) (fun m => (continuous_ccos m).measurable) (fun m θ => abs_ccos_le m θ)
    (fun L => gin_circle L) ?_ ?_ (strip n) (uniform J) (fun _ _ => hJ.le) x y w
    (fun h => hadjx.ne h.symm) (fun h => hadjy.ne h.symm) hwc hxy hxw hwy hJ hJ
  · intro r a b p q hpq
    rw [dot_Phi4]
    simp only [ccos, dotT_nvec]
  · intro r a b q
    rw [dot_u4_Phi4]
    simp only [ccos, dotT_dvec]

/-- **The corner covariance at `N = 3`**: positive for every `J > 0`, `n ≥ 3`. -/
theorem corner_pos3 {n : ℕ} (hn : 3 ≤ n) {J : ℝ} (hJ : 0 < J) {e f : Sym2 (Fin 3 × Fin n)}
    (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet) (hef : e ≠ f) (hsc : seriesCorner n e f) :
    0 < gibbsCov 3 (strip n) (uniform J) (bond e) (bond f) := by
  obtain ⟨c, hc, hce, hcf⟩ := hsc
  obtain ⟨x, rfl⟩ := Sym2.mem_iff_exists.mp hce
  obtain ⟨y, rfl⟩ := Sym2.mem_iff_exists.mp hcf
  have hadjx : (strip n).Adj c x := he
  have hadjy : (strip n).Adj c y := hf
  have hxy : x ≠ y := fun h => hef (by rw [h])
  obtain ⟨w, hwc, hxw, hwy⟩ := corner_witness hn hc hadjx hadjy hxy
  refine gksz_strict_generic (N := 3) (by norm_num) unifB nu3 Phi3 param3 u3 1 dot_u3 c
    (cising (V := {i // ¬ i = c})) (fun m => measurable_of_finite _) (fun m ε => (abs_cising m ε).le)
    (fun L => gin_ising L) ?_ ?_ (strip n) (uniform J) (fun _ _ => hJ.le) x y w
    (fun h => hadjx.ne h.symm) (fun h => hadjy.ne h.symm) hwc hxy hxw hwy hJ hJ
  · intro r a b p q hpq
    rw [dot_Phi3, cising_nvec hpq]
    simp only [ccos, dotT_nvec]
  · intro r a b q
    rw [dot_u3_Phi3]
    simp only [ccos, dotT_dvec]

/-- **hCornerPair is a theorem at `N = 3, 4`.** -/
theorem hCornerPair_holds (N : ℕ) (hN : N = 3 ∨ N = 4) : hCornerPair N := by
  intro n hn J hJ0 _hJ20 e he f hf hef hsc
  rcases hN with rfl | rfl
  · exact corner_pos3 hn hJ0 he hf hef hsc
  · exact corner_pos4 hn hJ0 he hf hef hsc

end G2S3

#print axioms G2S3.corner_pos4
#print axioms G2S3.corner_pos3
#print axioms G2S3.hCornerPair_holds
