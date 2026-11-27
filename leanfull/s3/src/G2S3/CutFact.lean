/-
G2S3.CutFact (stage S3, Part E4): the factorization at a 2-edge cut, Proposition 3.6 by the new route, every N ≥ 2
(STATEMENTS_S3_v8.md, E4). With the sides of the cut, the Gibbs weight with J_e = J_f = 0 never crosses them, so by vertex
elimination (`gram_exp_side`) and the four-terminal integrals (`cut_base`) the weights ∫ Π_c(σ_x, σ_y) Π_c'(σ_z, σ_w) e^{H}
vanish for c ≠ c' and are ≥ 0 for c = c'. Expanding e^{a s_e} and e^{b s_f} (display (3)) gives Z(a, b) = Σ_c u_c k_c(a) k_c(b).
-/
import G2S3.CutBase
import G2S3.CutGraph
import G2S3.CornerFact

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

section CutF

variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]

/-- the weight of the common label at a cut -/
def uCut (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (x y z w : V) (c : ℕ) : ℝ :=
  ∫ σ, zonal N c (σ x) (σ y) * zonal N c (σ z) (σ w) *
    Real.exp (energy G (Function.update (Function.update J s(x, y) 0) s(z, w) 0) σ) ∂(freeMeasure N V)

/-- expanding the weight of one edge (display (3)) under an integral -/
theorem hasSum_edge (hN : 2 ≤ N) {p q : V} {F : Config N V → ℝ} (hF : BddMeas F) (a : ℝ) :
    HasSum (fun c => kConc N c a * ∫ σ, F σ * zonal N c (σ p) (σ q) ∂(freeMeasure N V))
      (∫ σ, F σ * Real.exp (a * dot (σ p) (σ q)) ∂(freeMeasure N V)) := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  obtain ⟨hFm, C, hC⟩ := hF
  have hS := hasSum_integral_of_bound (μ := freeMeasure N V)
    (fun c σ => F σ * (kConc N c a * zonal N c (σ p) (σ q)))
    (fun σ => F σ * Real.exp (a * dot (σ p) (σ q)))
    (fun c => |C| * (|kConc N c a| * dConc N c))
    (fun c => (hFm.mul ((zonal_pair_bdd hN c p q).1.const_mul _)).aestronglyMeasurable)
    (fun c σ => by
      rw [abs_mul, abs_mul]
      exact mul_le_mul ((hC σ).trans (le_abs_self C))
        (mul_le_mul_of_nonneg_left (abs_zonal_le hN c _ _) (abs_nonneg _)) (by positivity) (abs_nonneg _))
    ((summable_kConc_dConc hN a).mul_left _)
    (fun σ => (exp_dot_hasSum hN a (σ p) (σ q)).mul_left (F σ))
  convert hS using 1
  funext c
  rw [← integral_const_mul]
  congr 1
  funext σ
  ring

/-- the couplings with J_e = J_f = 0 never cross the sides -/
theorem cutJ_side {G : SimpleGraph V} {J : Sym2 V → ℝ} {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) :
    ∀ a b, G.Adj a b → Function.update (Function.update J s(x, y) 0) s(z, w) 0 s(a, b) ≠ 0 → (a ∈ A ↔ b ∈ A) := by
  intro a b hab hJ
  refine hS.side a b hab (fun h => hJ ?_) (fun h => hJ ?_)
  · rw [h, Function.update_of_ne hS.ne, Function.update_self]
  · rw [h, Function.update_self]

theorem F4_invariant {x y z w : V} (c c' : ℕ) : ∀ v ∉ ({x, y, z, w} : Finset V), ∀ (σ : Config N V) (t : Sph N),
    zonal N c ((Function.update σ v t) x) ((Function.update σ v t) y) *
      zonal N c' ((Function.update σ v t) z) ((Function.update σ v t) w)
      = zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) := by
  intro v hv σ t
  simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hv
  obtain ⟨h1, h2, h3, h4⟩ := hv
  rw [Function.update_of_ne (Ne.symm h1), Function.update_of_ne (Ne.symm h2), Function.update_of_ne (Ne.symm h3),
    Function.update_of_ne (Ne.symm h4)]

/-- the off-diagonal weights vanish -/
theorem cut_offdiag (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) {c c' : ℕ} (hcc : c ≠ c') :
    ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) *
      Real.exp (energy G (Function.update (Function.update J s(x, y) 0) s(z, w) 0) σ) ∂(freeMeasure N V) = 0 := by
  have hef : ¬ (x = z ∧ y = w) := fun h => hS.ne (by rw [h.1, h.2])
  have hJ0 := ferro_update2 hJ s(x, y) s(z, w)
  have hF : BddMeas (fun σ : Config N V => zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w)) :=
    BddMeas.mul (zonal_pair_bdd hN c x y) (zonal_pair_bdd hN c' z w)
  have hFn : BddMeas (fun σ : Config N V => (-1) * (zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w))) :=
    hF.const_mul (-1)
  have h1 := gram_exp_side (by omega) G _ hJ0 {x, y, z, w} A hF (fun v hv σ t => F4_invariant c c' v hv σ t)
    (cutJ_side hS) (fun L hL => ((cut_base hN hS.xA hS.yA hS.zA hS.wA hef c c' L hL).1 hcc).ge)
  have h2 := gram_exp_side (by omega) G _ hJ0 {x, y, z, w} A hFn
    (fun v hv σ t => by simp only [F4_invariant c c' v hv σ t]) (cutJ_side hS)
    (fun L hL => by
      have h := (cut_base hN hS.xA hS.yA hS.zA hS.wA hef c c' L hL).1 hcc
      have e : (fun σ : Config N V => (-1) * (zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w)) * gw L σ)
          = fun σ => (-1) * (zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * gw L σ) := by
        funext σ; ring
      rw [e, integral_const_mul, h, mul_zero])
  have e2 : (fun σ : Config N V => (-1) * (zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w)) *
      Real.exp (energy G (Function.update (Function.update J s(x, y) 0) s(z, w) 0) σ))
      = fun σ => (-1) * (zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) *
        Real.exp (energy G (Function.update (Function.update J s(x, y) 0) s(z, w) 0) σ)) := by
    funext σ; ring
  rw [e2, integral_const_mul] at h2
  linarith

theorem uCut_nonneg (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (c : ℕ) : 0 ≤ uCut N G J x y z w c := by
  have hef : ¬ (x = z ∧ y = w) := fun h => hS.ne (by rw [h.1, h.2])
  have hF : BddMeas (fun σ : Config N V => zonal N c (σ x) (σ y) * zonal N c (σ z) (σ w)) :=
    BddMeas.mul (zonal_pair_bdd hN c x y) (zonal_pair_bdd hN c z w)
  exact gram_exp_side (by omega) G _ (ferro_update2 hJ s(x, y) s(z, w)) {x, y, z, w} A hF
    (fun v hv σ t => F4_invariant c c v hv σ t) (cutJ_side hS)
    (fun L hL => (cut_base hN hS.xA hS.yA hS.zA hS.wA hef c c L hL).2 rfl)

theorem uCut_zero_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (x y z w : V) :
    0 < uCut N G J x y z w 0 := by
  have e : uCut N G J x y z w 0 = partition N G (Function.update (Function.update J s(x, y) 0) s(z, w) 0) := by
    unfold uCut partition
    simp only [zonal_zero, one_mul]
  rw [e]
  exact partition_pos (by omega) G _

theorem uCut_le (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (x y z w : V) (c : ℕ) :
    |uCut N G J x y z w c| ≤ ((c : ℝ) + 1) ^ (2 * N) * uCut N G J x y z w 0 := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  obtain ⟨J0, hJ0⟩ : ∃ J0, J0 = Function.update (Function.update J s(x, y) 0) s(z, w) 0 := ⟨_, rfl⟩
  have hu0 : uCut N G J x y z w 0 = ∫ σ, Real.exp (energy G J0 σ) ∂(freeMeasure N V) := by
    unfold uCut
    rw [← hJ0]
    simp only [zonal_zero, one_mul]
  have huc : uCut N G J x y z w c
      = ∫ σ, zonal N c (σ x) (σ y) * zonal N c (σ z) (σ w) * Real.exp (energy G J0 σ) ∂(freeMeasure N V) := by
    unfold uCut
    rw [← hJ0]
  have hd := dConc_le_pow hN c
  have hd0 := (dConc_pos_S1 hN c).le
  have hint1 : Integrable (fun σ : Config N V => zonal N c (σ x) (σ y) * zonal N c (σ z) (σ w) *
      Real.exp (energy G J0 σ)) (freeMeasure N V) :=
    (BddMeas.mul (BddMeas.mul (zonal_pair_bdd hN c x y) (zonal_pair_bdd hN c z w)) (expE_bdd G J0)).integrable
  have hint2 : Integrable (fun σ : Config N V => dConc N c * dConc N c * Real.exp (energy G J0 σ))
      (freeMeasure N V) := ((expE_bdd G J0).integrable).const_mul _
  rw [huc, hu0]
  calc |∫ σ, zonal N c (σ x) (σ y) * zonal N c (σ z) (σ w) * Real.exp (energy G J0 σ) ∂(freeMeasure N V)|
      ≤ ∫ σ, |zonal N c (σ x) (σ y) * zonal N c (σ z) (σ w) * Real.exp (energy G J0 σ)| ∂(freeMeasure N V) :=
        abs_integral_le_integral_abs
    _ ≤ ∫ σ, dConc N c * dConc N c * Real.exp (energy G J0 σ) ∂(freeMeasure N V) := by
        refine integral_mono hint1.abs hint2 (fun σ => ?_)
        rw [abs_mul, abs_mul, abs_of_pos (Real.exp_pos _)]
        exact mul_le_mul_of_nonneg_right (mul_le_mul (abs_zonal_le hN c _ _) (abs_zonal_le hN c _ _)
          (abs_nonneg _) hd0) (Real.exp_pos _).le
    _ = dConc N c * dConc N c * ∫ σ, Real.exp (energy G J0 σ) ∂(freeMeasure N V) := integral_const_mul _ _
    _ ≤ ((c : ℝ) + 1) ^ (2 * N) * ∫ σ, Real.exp (energy G J0 σ) ∂(freeMeasure N V) := by
        refine mul_le_mul_of_nonneg_right ?_ (integral_nonneg (fun σ => (Real.exp_pos _).le))
        rw [two_mul, pow_add]
        exact mul_le_mul hd hd hd0 (by positivity)

/-- **Proposition 3.6 by vertex elimination**: Z(a, b) = Σ_c u_c k_c(a) k_c(b) -/
theorem cut_factor (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (a b : ℝ) :
    HasSum (fun c => uCut N G J x y z w c * kConc N c a * kConc N c b)
      (partition N G (Function.update (Function.update J s(x, y) a) s(z, w) b)) := by
  have he : s(x, y) ∈ G.edgeFinset := G.mem_edgeFinset.mpr hS.adj_e
  have hf : s(z, w) ∈ G.edgeFinset := G.mem_edgeFinset.mpr hS.adj_f
  obtain ⟨J0, hJ0⟩ : ∃ J0, J0 = Function.update (Function.update J s(x, y) 0) s(z, w) 0 := ⟨_, rfl⟩
  unfold partition
  simp only [energy_update_two G J he hf hS.ne a b]
  rw [← hJ0]
  have hE : BddMeas (fun σ : Config N V => Real.exp (energy G J0 σ)) := expE_bdd G J0
  have hEa : BddMeas (fun σ : Config N V => Real.exp (energy G J0 σ) * Real.exp (a * dot (σ x) (σ y))) := by
    refine BddMeas.mul hE ⟨?_, Real.exp |a|, fun σ => ?_⟩
    · exact ((measurable_bond (N := N) s(x, y)).const_mul a).exp
    · rw [abs_of_pos (Real.exp_pos _)]
      refine Real.exp_le_exp.mpr ?_
      have h1 := abs_dot_le (σ x) (σ y)
      calc a * dot (σ x) (σ y) ≤ |a * dot (σ x) (σ y)| := le_abs_self _
        _ = |a| * |dot (σ x) (σ y)| := abs_mul _ _
        _ ≤ |a| * 1 := mul_le_mul_of_nonneg_left h1 (abs_nonneg _)
        _ = |a| := mul_one _
  have e1 : (fun σ : Config N V => Real.exp (energy G J0 σ + a * bond s(x, y) σ + b * bond s(z, w) σ))
      = fun σ => (Real.exp (energy G J0 σ) * Real.exp (a * dot (σ x) (σ y))) * Real.exp (b * dot (σ z) (σ w)) := by
    funext σ
    rw [Real.exp_add, Real.exp_add]
    rfl
  rw [e1]
  have hinner : ∀ c', ∫ σ, (Real.exp (energy G J0 σ) * Real.exp (a * dot (σ x) (σ y))) * zonal N c' (σ z) (σ w)
      ∂(freeMeasure N V) = kConc N c' a * uCut N G J x y z w c' := by
    intro c'
    have hFc : BddMeas (fun σ : Config N V => Real.exp (energy G J0 σ) * zonal N c' (σ z) (σ w)) :=
      BddMeas.mul hE (zonal_pair_bdd hN c' z w)
    have hS2 := hasSum_edge hN (p := x) (q := y) hFc a
    have e2 : (fun σ : Config N V => (Real.exp (energy G J0 σ) * Real.exp (a * dot (σ x) (σ y))) *
        zonal N c' (σ z) (σ w))
        = fun σ => (Real.exp (energy G J0 σ) * zonal N c' (σ z) (σ w)) * Real.exp (a * dot (σ x) (σ y)) := by
      funext σ; ring
    rw [e2]
    refine hS2.unique ?_
    have hterm : ∀ c, kConc N c a * ∫ σ, Real.exp (energy G J0 σ) * zonal N c' (σ z) (σ w) * zonal N c (σ x) (σ y)
        ∂(freeMeasure N V) = if c = c' then kConc N c' a * uCut N G J x y z w c' else 0 := by
      intro c
      by_cases hcc : c = c'
      · rw [if_pos hcc, hcc]
        unfold uCut
        rw [← hJ0]
        congr 1
        congr 1
        funext σ
        ring
      · rw [if_neg hcc]
        have h0 := cut_offdiag hN G J hJ hS hcc
        rw [← hJ0] at h0
        have e3 : (fun σ : Config N V => Real.exp (energy G J0 σ) * zonal N c' (σ z) (σ w) * zonal N c (σ x) (σ y))
            = fun σ => zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * Real.exp (energy G J0 σ) := by
          funext σ; ring
        rw [e3, h0, mul_zero]
    simp only [hterm]
    exact hasSum_ite_eq c' _
  have hS1 := hasSum_edge hN (p := z) (q := w) hEa b
  simp only [hinner] at hS1
  convert hS1 using 1
  funext c
  ring

/-- u_1 > 0 from a positive path from x to y avoiding e -/
theorem uCut_one_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (hJf : 0 < J s(z, w)) (p : G.Walk x y) (hp : p.IsPath)
    (hpe : ∀ g ∈ p.edges, g ≠ s(x, y)) (hpos : ∀ g ∈ p.edges, 0 < J g) : 0 < uCut N G J x y z w 1 := by
  have he : s(x, y) ∈ G.edgeFinset := G.mem_edgeFinset.mpr hS.adj_e
  have hf : s(z, w) ∈ G.edgeFinset := G.mem_edgeFinset.mpr hS.adj_f
  have hxy : x ≠ y := hS.adj_e.ne
  have hJe : Ferro G (Function.update J s(x, y) 0) := by
    intro g hg
    by_cases hge : g = s(x, y)
    · rw [hge, Function.update_self]
    · rw [Function.update_of_ne hge]; exact hJ g hg
  have hP := gram_exp_path_pos hN G (Function.update J s(x, y) 0) hJe hxy p hp (fun g hg => by
    rw [Function.update_of_ne (hpe g hg)]; exact hpos g hg)
  obtain ⟨J0, hJ0⟩ : ∃ J0, J0 = Function.update (Function.update J s(x, y) 0) s(z, w) 0 := ⟨_, rfl⟩
  have hupd : Function.update (Function.update J s(x, y) 0) s(z, w) (J s(z, w)) = Function.update J s(x, y) 0 := by
    have h1 : Function.update J s(x, y) 0 s(z, w) = J s(z, w) := Function.update_of_ne (Ne.symm hS.ne) 0 J
    rw [← h1, Function.update_eq_self]
  have hEe : ∀ σ : Config N V, energy G (Function.update J s(x, y) 0) σ
      = energy G J0 σ + J s(z, w) * dot (σ z) (σ w) := by
    intro σ
    have h := energy_update_two G J he hf hS.ne 0 (J s(z, w)) σ
    rw [hupd, ← hJ0] at h
    rw [h]
    simp only [zero_mul, add_zero]
    rfl
  have hFc : BddMeas (fun σ : Config N V => zonal N 1 (σ x) (σ y) * Real.exp (energy G J0 σ)) :=
    BddMeas.mul (zonal_pair_bdd hN 1 x y) (expE_bdd G J0)
  have hS2 := hasSum_edge hN (p := z) (q := w) hFc (J s(z, w))
  have hval : ∫ σ, zonal N 1 (σ x) (σ y) * Real.exp (energy G J0 σ) * Real.exp (J s(z, w) * dot (σ z) (σ w))
      ∂(freeMeasure N V) = kConc N 1 (J s(z, w)) * uCut N G J x y z w 1 := by
    refine hS2.unique ?_
    have hterm : ∀ c', kConc N c' (J s(z, w)) * ∫ σ, zonal N 1 (σ x) (σ y) * Real.exp (energy G J0 σ) *
        zonal N c' (σ z) (σ w) ∂(freeMeasure N V)
          = if c' = 1 then kConc N 1 (J s(z, w)) * uCut N G J x y z w 1 else 0 := by
      intro c'
      by_cases hc : c' = 1
      · rw [if_pos hc, hc]
        unfold uCut
        rw [← hJ0]
        congr 1
        congr 1
        funext σ
        ring
      · rw [if_neg hc]
        have h0 := cut_offdiag hN G J hJ hS (c := 1) (c' := c') (Ne.symm hc)
        rw [← hJ0] at h0
        have e3 : (fun σ : Config N V => zonal N 1 (σ x) (σ y) * Real.exp (energy G J0 σ) * zonal N c' (σ z) (σ w))
            = fun σ => zonal N 1 (σ x) (σ y) * zonal N c' (σ z) (σ w) * Real.exp (energy G J0 σ) := by
          funext σ; ring
        rw [e3, h0, mul_zero]
    simp only [hterm]
    exact hasSum_ite_eq 1 _
  have e4 : ∫ σ, zonal N 1 (σ x) (σ y) * Real.exp (energy G (Function.update J s(x, y) 0) σ) ∂(freeMeasure N V)
      = ∫ σ, zonal N 1 (σ x) (σ y) * Real.exp (energy G J0 σ) * Real.exp (J s(z, w) * dot (σ z) (σ w))
          ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hEe σ, Real.exp_add]
    ring
  rw [e4, hval] at hP
  have hk1 : 0 < kConc N 1 (J s(z, w)) := (hKReg_kConc N hN).1 1 _ hJf
  exact (pos_iff_pos_of_mul_pos hP).mp hk1

end CutF

end G2S3

#print axioms G2S3.cut_offdiag
#print axioms G2S3.uCut_nonneg
#print axioms G2S3.uCut_le
#print axioms G2S3.cut_factor
#print axioms G2S3.uCut_one_pos
