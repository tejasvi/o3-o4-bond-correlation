/-
G2S3.LawP (stage S3, Part E5a): the law of the common label under p (Lemma 2.4, tex l.282) and its identification with the
factorization weights (STATEMENTS_S3_v8.md, E5). Fixing the labels of e and f in the label expansion (4): the series of e and
f are replaced by single terms, the others sum to e^{J_g s_g} (display (3)), and dominated convergence gives
Σ_{ℓ_e = c, ℓ_f = c'} W(ℓ) Π k = k_c(J_e) k_c'(J_f) ∫ Π_c(e) Π_c'(f) e^{H} with J_e = J_f = 0 in H. At a vertex of degree two
this is Part C's q (`qLabel_eq_commonLaw`, the fidelity link for Corollary 3.8).
-/
import G2S3.CutFact
import G2S3.Cor38

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

section LawP

variable {N : ℕ} {V : Type} [Fintype V] [DecidableEq V]

/-- the law of the common label c = ℓ_e = ℓ_f under p (Lemma 2.4, tex l.282) -/
def commonLaw (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (c : ℕ) : ℝ :=
  ∑' ℓ : G.edgeFinset → ℕ, if ℓ e = c ∧ ℓ f = c then labelLaw N G J ℓ else 0

/-- the per-edge series of the joint marginal: single terms at e and f -/
def phiJ (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (c c' : ℕ)
    (σ : Config N V) (g : G.edgeFinset) (a : ℕ) : ℝ :=
  if (g = e ∧ a ≠ c) ∨ (g = f ∧ a ≠ c') then 0 else kConc N a (J g) * zon N a (bond (g : Sym2 V) σ)

/-- its edgewise sums -/
def sJ (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (c c' : ℕ)
    (σ : Config N V) (g : G.edgeFinset) : ℝ :=
  if g = e then kConc N c (J g) * zon N c (bond (g : Sym2 V) σ)
  else if g = f then kConc N c' (J g) * zon N c' (bond (g : Sym2 V) σ)
  else Real.exp (J g * bond (g : Sym2 V) σ)

theorem phiJ_hasSum (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (hef : e ≠ f) (c c' : ℕ) (σ : Config N V) (g : G.edgeFinset) :
    HasSum (phiJ N G J e f c c' σ g) (sJ N G J e f c c' σ g) := by
  by_cases hge : g = e
  · subst hge
    have hval : sJ N G J g f c c' σ g = phiJ N G J g f c c' σ g c := by
      unfold sJ phiJ
      rw [if_pos rfl, if_neg]
      rintro (⟨-, h⟩ | ⟨h, -⟩)
      · exact h rfl
      · exact hef h
    rw [hval]
    refine hasSum_single c (fun b hb => ?_)
    unfold phiJ
    rw [if_pos (Or.inl ⟨rfl, hb⟩)]
  · by_cases hgf : g = f
    · subst hgf
      have hval : sJ N G J e g c c' σ g = phiJ N G J e g c c' σ g c' := by
        unfold sJ phiJ
        rw [if_neg hge, if_pos rfl, if_neg]
        rintro (⟨h, -⟩ | ⟨-, h⟩)
        · exact hge h
        · exact h rfl
      rw [hval]
      refine hasSum_single c' (fun b hb => ?_)
      unfold phiJ
      rw [if_pos (Or.inr ⟨rfl, hb⟩)]
    · have hfun : phiJ N G J e f c c' σ g = fun a => kConc N a (J g) * zon N a (bond (g : Sym2 V) σ) := by
        funext a
        unfold phiJ
        rw [if_neg]
        rintro (⟨h, -⟩ | ⟨h, -⟩)
        · exact hge h
        · exact hgf h
      have hval : sJ N G J e f c c' σ g = Real.exp (J g * bond (g : Sym2 V) σ) := by
        unfold sJ
        rw [if_neg hge, if_neg hgf]
      rw [hfun, hval]
      exact exp_hasSum_zon hN (J g) _ (abs_bond_le _ σ)

theorem phiJ_abs_le (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (c c' : ℕ) (σ : Config N V) (g : G.edgeFinset) (a : ℕ) :
    |phiJ N G J e f c c' σ g a| ≤ |kConc N a (J g)| * dConc N a := by
  unfold phiJ
  split_ifs
  · rw [abs_zero]; exact mul_nonneg (abs_nonneg _) (dConc_pos_S1 hN a).le
  · rw [abs_mul]; exact mul_le_mul_of_nonneg_left (abs_zon_bond_le hN a (g : Sym2 V) σ) (abs_nonneg _)

theorem sJ_prod (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (hef : e ≠ f)
    (c c' : ℕ) (σ : Config N V) :
    ∏ g, sJ N G J e f c c' σ g = kConc N c (J e) * kConc N c' (J f) *
      (zon N c (bond (e : Sym2 V) σ) * zon N c' (bond (f : Sym2 V) σ) *
        Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ)) := by
  have hsplit : ∀ g : G.edgeFinset, sJ N G J e f c c' σ g =
      ((if g = e then kConc N c (J e) * zon N c (bond (e : Sym2 V) σ) else 1) *
        (if g = f then kConc N c' (J f) * zon N c' (bond (f : Sym2 V) σ) else 1)) *
      Real.exp (Function.update (Function.update J e 0) f 0 g * bond (g : Sym2 V) σ) := by
    intro g
    unfold sJ
    by_cases hge : g = e
    · subst hge
      have hgf' : (g : Sym2 V) ≠ (f : Sym2 V) := fun h => hef (Subtype.ext h)
      rw [if_pos rfl, if_pos rfl, if_neg hef, Function.update_of_ne hgf', Function.update_self]
      simp
    · by_cases hgf : g = f
      · subst hgf
        rw [if_neg hge, if_pos rfl, if_neg hge, if_pos rfl, Function.update_self]
        simp
      · have hge' : (g : Sym2 V) ≠ (e : Sym2 V) := fun h => hge (Subtype.ext h)
        have hgf' : (g : Sym2 V) ≠ (f : Sym2 V) := fun h => hgf (Subtype.ext h)
        rw [if_neg hge, if_neg hgf, if_neg hge, if_neg hgf, Function.update_of_ne hgf', Function.update_of_ne hge']
        simp
  rw [Finset.prod_congr rfl (fun g _ => hsplit g), Finset.prod_mul_distrib, Finset.prod_mul_distrib,
    Finset.prod_ite_eq', Finset.prod_ite_eq', if_pos (Finset.mem_univ e), if_pos (Finset.mem_univ f)]
  have hE : ∏ g : G.edgeFinset, Real.exp (Function.update (Function.update J e 0) f 0 g * bond (g : Sym2 V) σ)
      = Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ) := by
    unfold energy
    rw [Real.exp_sum]
    exact Finset.prod_coe_sort G.edgeFinset
      (fun x => Real.exp (Function.update (Function.update J e 0) f 0 x * bond x σ))
  rw [hE]
  ring

theorem phiJ_prod (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (hef : e ≠ f)
    (c c' : ℕ) (σ : Config N V) (ℓ : G.edgeFinset → ℕ) :
    ∏ g, phiJ N G J e f c c' σ g (ℓ g) = if ℓ e = c ∧ ℓ f = c' then
      ∏ g, (kConc N (ℓ g) (J g) * zon N (ℓ g) (bond (g : Sym2 V) σ)) else 0 := by
  by_cases hl : ℓ e = c ∧ ℓ f = c'
  · rw [if_pos hl]
    refine Finset.prod_congr rfl (fun g _ => ?_)
    unfold phiJ
    rw [if_neg]
    rintro (⟨hge, hne⟩ | ⟨hgf, hne⟩)
    · exact hne (hge ▸ hl.1)
    · exact hne (hgf ▸ hl.2)
  · rw [if_neg hl]
    by_cases h1 : ℓ e = c
    · have h2 : ℓ f ≠ c' := fun h => hl ⟨h1, h⟩
      refine Finset.prod_eq_zero (Finset.mem_univ f) ?_
      unfold phiJ
      rw [if_pos (Or.inr ⟨rfl, h2⟩)]
    · refine Finset.prod_eq_zero (Finset.mem_univ e) ?_
      unfold phiJ
      rw [if_pos (Or.inl ⟨rfl, h1⟩)]

theorem phiJ_summable (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (c c' : ℕ) (σ : Config N V) (g : G.edgeFinset) : Summable (fun a => ‖phiJ N G J e f c c' σ g a‖) := by
  refine Summable.of_nonneg_of_le (fun a => norm_nonneg _) (fun a => ?_) (summable_kConc_dConc hN (J g))
  rw [Real.norm_eq_abs]
  exact phiJ_abs_le hN G J e f c c' σ g a

theorem phiJ_prod_hasSum (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : G.edgeFinset) (hef : e ≠ f) (c c' : ℕ) (σ : Config N V) :
    HasSum (fun ℓ : G.edgeFinset → ℕ => ∏ g, phiJ N G J e f c c' σ g (ℓ g)) (∏ g, sJ N G J e f c c' σ g) :=
  (hasSum_prod_fintype (phiJ N G J e f c c' σ) (sJ N G J e f c c' σ)
    (phiJ_hasSum hN G J e f hef c c' σ) (phiJ_summable hN G J e f c c' σ)).1

theorem phiJ_measurable (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (c c' : ℕ) (ℓ : G.edgeFinset → ℕ) (g : G.edgeFinset) :
    Measurable (fun σ : Config N V => phiJ N G J e f c c' σ g (ℓ g)) := by
  unfold phiJ
  split_ifs
  · exact measurable_const
  · exact measurable_const.mul (measurable_zon_bond _ _)

theorem phiJ_prod_measurable (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (c c' : ℕ) (ℓ : G.edgeFinset → ℕ) :
    Measurable (fun σ : Config N V => ∏ g, phiJ N G J e f c c' σ g (ℓ g)) :=
  Finset.measurable_prod Finset.univ (fun g _ => phiJ_measurable G J e f c c' ℓ g)

theorem phiJ_prod_abs_le (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : G.edgeFinset) (c c' : ℕ) (ℓ : G.edgeFinset → ℕ) (σ : Config N V) :
    |∏ g, phiJ N G J e f c c' σ g (ℓ g)| ≤ ∏ g, (|kConc N (ℓ g) (J g)| * dConc N (ℓ g)) := by
  rw [Finset.abs_prod]
  exact Finset.prod_le_prod₀ (fun g _ => abs_nonneg _) (fun g _ => phiJ_abs_le hN G J e f c c' σ g (ℓ g))

/-- the summable bound of the label expansion, in this context -/
theorem labelBound_summable (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    Summable (fun ℓ : G.edgeFinset → ℕ => ∏ g, (|kConc N (ℓ g) (J g)| * dConc N (ℓ g))) := by
  have h := (hasSum_prod_fintype (fun (g : G.edgeFinset) (a : ℕ) => |kConc N a (J g)| * dConc N a)
    (fun (g : G.edgeFinset) => ∑' a, |kConc N a (J g)| * dConc N a)
    (fun g => (summable_kConc_dConc hN (J g)).hasSum)
    (fun g => by
      refine (summable_kConc_dConc hN (J g)).congr (fun c => ?_)
      rw [Real.norm_eq_abs, abs_mul, abs_abs, abs_of_pos (dConc_pos_S1 hN c)])).1
  exact h.summable

omit [DecidableEq V] in
/-- dominated convergence for a product of coordinate series over a finite index type -/
theorem series_prod_integral (hN : 2 ≤ N) {E : Type} [Fintype E] (φ : Config N V → E → ℕ → ℝ)
    (S : Config N V → E → ℝ) (B : E → ℕ → ℝ) (hφ : ∀ σ, HasSum (fun ℓ : E → ℕ => ∏ g, φ σ g (ℓ g)) (∏ g, S σ g))
    (hmeas : ∀ ℓ : E → ℕ, Measurable (fun σ => ∏ g, φ σ g (ℓ g))) (hbound : ∀ σ g a, |φ σ g a| ≤ B g a)
    (hBs : Summable (fun ℓ : E → ℕ => ∏ g, B g (ℓ g))) :
    HasSum (fun ℓ : E → ℕ => ∫ σ, ∏ g, φ σ g (ℓ g) ∂(freeMeasure N V)) (∫ σ, ∏ g, S σ g ∂(freeMeasure N V)) := by
  have hfm := freeMeasure_isProb (N := N) (by omega) V
  have hB : ∀ (ℓ : E → ℕ) (σ : Config N V), |∏ g, φ σ g (ℓ g)| ≤ ∏ g, B g (ℓ g) := by
    intro ℓ σ
    rw [Finset.abs_prod]
    exact Finset.prod_le_prod₀ (fun g _ => abs_nonneg _) (fun g _ => hbound σ g (ℓ g))
  have hF : ∀ ℓ : E → ℕ, AEStronglyMeasurable (fun σ => ∏ g, φ σ g (ℓ g)) (freeMeasure N V) :=
    fun ℓ => (hmeas ℓ).aestronglyMeasurable
  exact hasSum_integral_of_bound _ _ _ hF hB hBs hφ

/-- the joint marginal, before identifying the terms -/
theorem joint_label_raw (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (hef : e ≠ f) (c c' : ℕ) :
    HasSum (fun ℓ : G.edgeFinset → ℕ => ∫ σ, ∏ g, phiJ N G J e f c c' σ g (ℓ g) ∂(freeMeasure N V))
      (∫ σ, ∏ g, sJ N G J e f c c' σ g ∂(freeMeasure N V)) :=
  series_prod_integral hN (phiJ N G J e f c c') (sJ N G J e f c c') (fun g a => |kConc N a (J g)| * dConc N a)
    (fun σ => phiJ_prod_hasSum hN G J e f hef c c' σ) (fun ℓ => phiJ_prod_measurable G J e f c c' ℓ)
    (fun σ g a => phiJ_abs_le hN G J e f c c' σ g a) (labelBound_summable hN G J)

/-- the joint marginal of two labels in the label expansion (4) -/
theorem joint_label (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (hef : e ≠ f) (c c' : ℕ) :
    HasSum (fun ℓ : G.edgeFinset → ℕ =>
        if ℓ e = c ∧ ℓ f = c' then labelWeight N G ℓ * ∏ g, kConc N (ℓ g) (J g) else 0)
      (kConc N c (J e) * kConc N c' (J f) * ∫ σ, zon N c (bond (e : Sym2 V) σ) * zon N c' (bond (f : Sym2 V) σ) *
        Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ) ∂(freeMeasure N V)) := by
  have h := joint_label_raw hN G J e f hef c c'
  have hval : ∫ σ, ∏ g, sJ N G J e f c c' σ g ∂(freeMeasure N V)
      = kConc N c (J e) * kConc N c' (J f) * ∫ σ, zon N c (bond (e : Sym2 V) σ) * zon N c' (bond (f : Sym2 V) σ) *
          Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ) ∂(freeMeasure N V) := by
    rw [← integral_const_mul]
    congr 1
    funext σ
    exact sJ_prod G J e f hef c c' σ
  rw [hval] at h
  refine h.congr_fun (fun ℓ => ?_)
  have hterm : ∫ σ, ∏ g, phiJ N G J e f c c' σ g (ℓ g) ∂(freeMeasure N V)
      = if ℓ e = c ∧ ℓ f = c' then labelWeight N G ℓ * ∏ g, kConc N (ℓ g) (J g) else 0 := by
    by_cases hl : ℓ e = c ∧ ℓ f = c'
    · rw [if_pos hl]
      have hfac : ∀ σ : Config N V, ∏ g, phiJ N G J e f c c' σ g (ℓ g)
          = ∏ g, (kConc N (ℓ g) (J g) * zon N (ℓ g) (bond (g : Sym2 V) σ)) := by
        intro σ
        rw [phiJ_prod G J e f hef c c' σ ℓ, if_pos hl]
      simp only [hfac]
      unfold labelWeight
      rw [← integral_mul_const]
      congr 1
      funext σ
      rw [← Finset.prod_mul_distrib]
      refine Finset.prod_congr rfl (fun g _ => ?_)
      simp only [zon]
      ring
    · rw [if_neg hl]
      have hz : ∀ σ : Config N V, ∏ g, phiJ N G J e f c c' σ g (ℓ g) = 0 := by
        intro σ
        rw [phiJ_prod G J e f hef c c' σ ℓ, if_neg hl]
      simp only [hz, integral_zero]
  exact hterm.symm

/-- the law of the common label, in closed form -/
theorem commonLaw_eq (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (hef : e ≠ f) (c : ℕ) :
    commonLaw N G J e f c = kConc N c (J e) * kConc N c (J f) * (∫ σ, zon N c (bond (e : Sym2 V) σ) *
      zon N c (bond (f : Sym2 V) σ) * Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ)
        ∂(freeMeasure N V)) / partition N G J := by
  have h := (joint_label hN G J e f hef c c).div_const (partition N G J)
  unfold commonLaw
  rw [← h.tsum_eq]
  congr 1
  funext ℓ
  unfold labelLaw
  split_ifs <;> simp

/-- **the fidelity link for Corollary 3.8**: Part C's q is the law of the common label under p -/
theorem qLabel_eq_commonLaw (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V}
    (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y) (hvx : G.Adj v x) (hvy : G.Adj v y) (c : ℕ) :
    qLabel N G J v x y c
      = commonLaw N G J ⟨s(v, x), G.mem_edgeFinset.mpr hvx⟩ ⟨s(v, y), G.mem_edgeFinset.mpr hvy⟩ c := by
  have hN0 : 0 < N := by omega
  have hfm := freeMeasure_isProb (N := N) (by omega) V
  have hne : (⟨s(v, x), G.mem_edgeFinset.mpr hvx⟩ : G.edgeFinset) ≠ ⟨s(v, y), G.mem_edgeFinset.mpr hvy⟩ := by
    intro h
    exact hxy (Sym2.congr_right.mp (congrArg Subtype.val h))
  have hxv : x ≠ v := (G.ne_of_adj hvx).symm
  have hyv : y ≠ v := (G.ne_of_adj hvy).symm
  have hb : BddMeas (fun σ : Config N V => zon N c (bond s(v, x) σ) * zon N c (bond s(v, y) σ) *
      Real.exp (energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) σ)) :=
    BddMeas.mul (BddMeas.mul (zonal_pair_bdd hN c v x) (zonal_pair_bdd hN c v y)) (expE_bdd G _)
  have hI : ∫ σ, zon N c (bond s(v, x) σ) * zon N c (bond s(v, y) σ) *
      Real.exp (energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) σ) ∂(freeMeasure N V)
      = ∫ σ, zonal N c (σ x) (σ y) *
          Real.exp (energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) σ) ∂(freeMeasure N V) := by
    rw [integral_update hN0 v _ hb]
    congr 1
    funext σ
    have h1 : ∀ z : Sph N, zon N c (bond s(v, x) (Function.update σ v z)) *
        zon N c (bond s(v, y) (Function.update σ v z)) *
        Real.exp (energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) (Function.update σ v z))
          = (zonal N c (σ x) z * zonal N c z (σ y)) *
            Real.exp (energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) σ) := by
      intro z
      rw [energy0_update_v G J hnb σ z]
      show zonal N c ((Function.update σ v z) v) ((Function.update σ v z) x) *
          zonal N c ((Function.update σ v z) v) ((Function.update σ v z) y) * _ = _
      rw [Function.update_self, Function.update_of_ne hxv, Function.update_of_ne hyv, zonal_symm N c z (σ x)]
    simp only [h1]
    rw [integral_mul_const, zonal_proj hN c c (σ x) (σ y), if_pos rfl]
  rw [commonLaw_eq hN G J _ _ hne c]
  dsimp only
  rw [hI]
  unfold qLabel uCorner
  ring

end LawP

end G2S3

#print axioms G2S3.joint_label
#print axioms G2S3.commonLaw_eq
#print axioms G2S3.qLabel_eq_commonLaw
