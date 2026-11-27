/-
G2S3.GKSz (stage S3, Part B7, generic): for a single-site parametrization Phi of omega in two-plane coordinates
(plane-1 angular system (A1, l1, c1) satisfying Ginibre's condition, plane 2 the circle) such that
  s_p . s_q = rho_p rho_q c1_{e_p - e_q}(a) + tau_p tau_q cos(b_p - b_q)   and   u . s_q = tau_q cos(b_q),
two edges vx, vy with a common vertex v have Cov(s_vx, s_vy) >= 0 on every finite graph with ferromagnetic couplings.
Proof (paper, Theorem 3.2, tex l.322-338): condition on s_v = u by rotation invariance (integral_cond); the conditional
model has fields along u at the neighbours of v; write 2 Z^2 Cov as a duplicated integral (cov_dup); pass to the
coordinate space (integral_XiC); there the integrand is g exp(h) with g, h in the Ginibre cone of sign 1
(ConeMem), and int g exp(h) >= 0 (ConeInt.cone_exp: Ginibre's argument with Dunlop's condition (2.4)).
-/
import G2S3.Dup

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

local instance instFactTwoPiPosG : Fact (0 < 2 * π) := ⟨Real.two_pi_pos⟩

/-- `δ_p - δ_q` -/
def nvec {W : Type*} [DecidableEq W] (p q : W) : W → ℤ := fun z => (if z = p then 1 else 0) - (if z = q then 1 else 0)

/-- `δ_q` -/
def dvec {W : Type*} [DecidableEq W] (q : W) : W → ℤ := fun z => if z = q then 1 else 0

theorem dotT_nvec {W : Type*} [Fintype W] [DecidableEq W] (p q : W) (θ : W → Tor) :
    dotT (nvec p q) θ = θ p - θ q := by
  unfold dotT nvec
  simp only [sub_smul, ite_smul, one_smul, zero_smul, Finset.sum_sub_distrib, Finset.sum_ite_eq',
    Finset.mem_univ, if_true]

theorem dotT_dvec {W : Type*} [Fintype W] [DecidableEq W] (q : W) (θ : W → Tor) : dotT (dvec q) θ = θ q := by
  unfold dotT dvec
  simp only [ite_smul, one_smul, zero_smul, Finset.sum_ite_eq', Finset.mem_univ, if_true]

theorem energy_rot {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V) : energy G J (fun i => sphMap R (σ i)) = energy G J σ := by
  unfold energy
  exact Finset.sum_congr rfl (fun g _ => by rw [bond_rot])

theorem bdd_bond {N : ℕ} {V : Type*} (e : Sym2 V) : BddMeas (bond (N := N) e) :=
  ⟨measurable_bond e, 1, abs_bond_le e⟩

theorem bdd_wexp {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    BddMeas (fun σ : Config N V => Real.exp (energy G J σ)) :=
  ⟨(measurable_energy G J).exp, Real.exp (∑ g ∈ G.edgeFinset, |J g|), fun σ => abs_exp_le (abs_energy_le G J σ)⟩

theorem gibbsCov_eq_num {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (F H : Config N V → ℝ) :
    gibbsCov N G J F H
      = ((∫ σ, F σ * H σ * Real.exp (energy G J σ) ∂(freeMeasure N V)) * (∫ σ, Real.exp (energy G J σ) ∂(freeMeasure N V))
        - (∫ σ, F σ * Real.exp (energy G J σ) ∂(freeMeasure N V))
          * (∫ σ, H σ * Real.exp (energy G J σ) ∂(freeMeasure N V))) / (partition N G J) ^ 2 := by
  have hZ := (partition_pos hN G J).ne'
  have hZdef : partition N G J = ∫ σ, Real.exp (energy G J σ) ∂(freeMeasure N V) := rfl
  unfold gibbsCov gibbsExp
  rw [← hZdef]
  field_simp

theorem joinP_v {N : ℕ} {V : Type*} [DecidableEq V] {v : V} (u : Sph N) (σ : {i // ¬ i = v} → Sph N) :
    joinP (fun i => i = v) (fun _ => u) σ v = u := by
  rw [joinP_pos (p := fun i => i = v) _ _ rfl]

theorem joinP_ne {N : ℕ} {V : Type*} [DecidableEq V] {v i : V} (u : Sph N) (σ : {i // ¬ i = v} → Sph N)
    (h : ¬ i = v) : joinP (fun i => i = v) (fun _ => u) σ i = σ ⟨i, h⟩ := by
  rw [joinP_neg (p := fun i => i = v) _ _ h]

/-- **Generic Ginibre-Dunlop inequality for two edges with a common vertex.** -/
theorem gksz_generic {N : ℕ} (hN : 0 < N) {A1 : Type} [MeasurableSpace A1] (l1 : Measure A1)
    [IsProbabilityMeasure l1] (ν : Measure ℝ) [IsProbabilityMeasure ν] (Φ : ℝ × (A1 × Tor) → Sph N)
    (hΦ : MeasurePreserving Φ (ν.prod (l1.prod AddCircle.haarAddCircle)) (omega N)) (u : Sph N)
    {V : Type} [Fintype V] [DecidableEq V] (v : V)
    (c1 : ({i // ¬ i = v} → ℤ) → ({i // ¬ i = v} → A1) → ℝ) (hc1m : ∀ n, Measurable (c1 n))
    (hc1b : ∀ n a, |c1 n a| ≤ 1)
    (gin1 : ∀ L, 0 ≤ ∫ p, angP c1 L p ∂((Measure.pi fun _ : {i // ¬ i = v} => l1).prod
      (Measure.pi fun _ : {i // ¬ i = v} => l1)))
    (hdot : ∀ (r : {i // ¬ i = v} → ℝ) (a : {i // ¬ i = v} → A1) (b : {i // ¬ i = v} → Tor)
      (p q : {i // ¬ i = v}), p ≠ q →
      dot (Φ (r p, (a p, b p))) (Φ (r q, (a q, b q)))
        = rhoF (r p) * rhoF (r q) * c1 (nvec p q) a + tauF (r p) * tauF (r q) * ccos (nvec p q) b)
    (hfield : ∀ (r : {i // ¬ i = v} → ℝ) (a : {i // ¬ i = v} → A1) (b : {i // ¬ i = v} → Tor)
      (q : {i // ¬ i = v}), dot u (Φ (r q, (a q, b q))) = tauF (r q) * ccos (dvec q) b)
    (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    (x y : V) (hx : ¬ x = v) (hy : ¬ y = v) :
    0 ≤ gibbsCov N G J (bond s(v, x)) (bond s(v, y)) := by
  have hprob := omega_isProbabilityMeasure N hN
  -- the conditioned functions
  set jn : ({i // ¬ i = v} → Sph N) → Config N V := fun σ2 => joinP (fun i => i = v) (fun _ => u) σ2 with hjn
  have hjnm : Measurable jn := by
    refine Measurable.of_eval (fun i => ?_)
    by_cases hi : i = v
    · simp only [hjn, joinP, hi, dite_true]
      exact measurable_const
    · simp only [hjn, joinP, hi, dite_false]
      exact measurable_pi_apply _
  have bF := bdd_bond (N := N) s(v, x)
  have bH := bdd_bond (N := N) s(v, y)
  have bw := bdd_wexp (N := N) G J
  have rF : ∀ (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V),
      bond s(v, x) (fun i => sphMap R (σ i)) = bond s(v, x) σ := fun R σ => bond_rot R _ σ
  have rH : ∀ (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V),
      bond s(v, y) (fun i => sphMap R (σ i)) = bond s(v, y) σ := fun R σ => bond_rot R _ σ
  have rw' : ∀ (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V),
      Real.exp (energy G J (fun i => sphMap R (σ i))) = Real.exp (energy G J σ) :=
    fun R σ => by rw [energy_rot]
  rw [gibbsCov_eq_num hN]
  refine div_nonneg ?_ (sq_nonneg _)
  rw [integral_cond hN v _ ((bF.mul bH).mul bw) (fun R σ => by simp only [rF, rH, rw']) u,
    integral_cond hN v _ bw (fun R σ => by simp only [rw']) u,
    integral_cond hN v _ (bF.mul bw) (fun R σ => by simp only [rF, rw']) u,
    integral_cond hN v _ (bH.mul bw) (fun R σ => by simp only [rH, rw']) u]
  have hc := cov_dup (Measure.pi fun _ : {i // ¬ i = v} => omega N) (bF.comp hjnm) (bH.comp hjnm) (bw.comp hjnm)
  simp only [hjn] at hc
  rw [hc]
  refine mul_nonneg (by norm_num) ?_
  -- pass to the coordinate space
  have hΨm : Measurable (fun p : ({i // ¬ i = v} → Sph N) × ({i // ¬ i = v} → Sph N) =>
      (bond s(v, x) (jn p.1) - bond s(v, x) (jn p.2)) * (bond s(v, y) (jn p.1) - bond s(v, y) (jn p.2))
        * (Real.exp (energy G J (jn p.1)) * Real.exp (energy G J (jn p.2)))) := by
    have m1 := (bF.comp hjnm).1
    have m2 := (bH.comp hjnm).1
    have m3 := (bw.comp hjnm).1
    exact ((m1.comp measurable_fst).sub (m1.comp measurable_snd)).mul
      ((m2.comp measurable_fst).sub (m2.comp measurable_snd)) |>.mul
      ((m3.comp measurable_fst).mul (m3.comp measurable_snd))
  have hX := integral_XiC hN Φ ν l1 AddCircle.haarAddCircle hΦ _ hΨm
  unfold freeMeasure at hX
  simp only [hjn] at hX
  rw [hX]
  -- the cone data
  have H : GHyp ν rhoF tauF (Measure.pi fun _ : {i // ¬ i = v} => l1) c1
      (Measure.pi fun _ : {i // ¬ i = v} => (AddCircle.haarAddCircle : Measure Tor)) (ccos (V := {i // ¬ i = v})) :=
    { hρ := rhoF_mono, hτ := tauF_anti, hρ0 := rhoF_nonneg, hτ0 := tauF_nonneg, hρ1 := rhoF_le_one,
      hτ1 := tauF_le_one, hρm := continuous_rhoF.measurable, hτm := continuous_tauF.measurable,
      hc1m := hc1m, hc2m := fun n => (continuous_ccos n).measurable, hc1b := hc1b,
      hc2b := fun n θ => abs_ccos_le n θ, gin1 := gin1,
      gin2 := fun L => gin_circle (V := {i // ¬ i = v}) L }
  -- the two observables
  set x' : {i // ¬ i = v} := ⟨x, hx⟩ with hx'
  set y' : {i // ¬ i = v} := ⟨y, hy⟩ with hy'
  have hb1 : ∀ (z : V) (hz : ¬ z = v) (ω : Om {i // ¬ i = v} ({i // ¬ i = v} → A1) ({i // ¬ i = v} → Tor)),
      bond s(v, z) (jn (XiC Φ ω).1) = tauF (ω.1.1 ⟨z, hz⟩) * ccos (dvec ⟨z, hz⟩) ω.2.2.1 := by
    intro z hz ω
    show dot (jn (XiC Φ ω).1 v) (jn (XiC Φ ω).1 z) = _
    simp only [hjn]
    rw [joinP_v, joinP_ne u _ hz]
    exact hfield ω.1.1 ω.2.1.1 ω.2.2.1 ⟨z, hz⟩
  have hb2 : ∀ (z : V) (hz : ¬ z = v) (ω : Om {i // ¬ i = v} ({i // ¬ i = v} → A1) ({i // ¬ i = v} → Tor)),
      bond s(v, z) (jn (XiC Φ ω).2) = tauF (ω.1.2 ⟨z, hz⟩) * ccos (dvec ⟨z, hz⟩) ω.2.2.2 := by
    intro z hz ω
    show dot (jn (XiC Φ ω).2 v) (jn (XiC Φ ω).2 z) = _
    simp only [hjn]
    rw [joinP_v, joinP_ne u _ hz]
    exact hfield ω.1.2 ω.2.1.2 ω.2.2.2 ⟨z, hz⟩
  -- the energy term lies in the cone
  have hedge : ∀ e ∈ G.edgeFinset, InC rhoF tauF c1 (ccos (V := {i // ¬ i = v})) 1
      (fun ω : Om {i // ¬ i = v} ({i // ¬ i = v} → A1) ({i // ¬ i = v} → Tor) =>
        bond e (jn (XiC Φ ω).1) + bond e (jn (XiC Φ ω).2)) := by
    intro e he
    induction e using Sym2.ind with
    | h p q =>
      have hpq : p ≠ q := (SimpleGraph.mem_edgeFinset.mp he).ne
      by_cases hp : p = v
      · subst hp
        have hq : ¬ q = p := fun h => hpq h.symm
        refine (InC.field2 ⟨q, hq⟩ (dvec ⟨q, hq⟩)).congr (fun ω => ?_)
        rw [hb1 q hq ω, hb2 q hq ω]
      · by_cases hq : q = v
        · subst hq
          refine (InC.field2 ⟨p, hp⟩ (dvec ⟨p, hp⟩)).congr (fun ω => ?_)
          have e1 : bond s(p, q) (jn (XiC Φ ω).1) = bond s(q, p) (jn (XiC Φ ω).1) := by rw [Sym2.eq_swap]
          have e2 : bond s(p, q) (jn (XiC Φ ω).2) = bond s(q, p) (jn (XiC Φ ω).2) := by rw [Sym2.eq_swap]
          rw [e1, e2, hb1 p hp ω, hb2 p hp ω]
        · have hpq' : (⟨p, hp⟩ : {i // ¬ i = v}) ≠ ⟨q, hq⟩ := fun h => hpq (congrArg Subtype.val h)
          refine ((InC.plane1 (ρ := rhoF) (τ := tauF) (c2 := ccos (V := {i // ¬ i = v})) ⟨p, hp⟩ ⟨q, hq⟩
            (nvec ⟨p, hp⟩ ⟨q, hq⟩)).add (InC.plane2 ⟨p, hp⟩ ⟨q, hq⟩ (nvec ⟨p, hp⟩ ⟨q, hq⟩))).congr (fun ω => ?_)
          show dot (jn (XiC Φ ω).1 p) (jn (XiC Φ ω).1 q) + dot (jn (XiC Φ ω).2 p) (jn (XiC Φ ω).2 q) = _
          simp only [hjn]
          rw [joinP_ne u _ hp, joinP_ne u _ hq, joinP_ne u _ hp, joinP_ne u _ hq]
          rw [show (XiC Φ ω).1 ⟨p, hp⟩ = Φ (ω.1.1 ⟨p, hp⟩, (ω.2.1.1 ⟨p, hp⟩, ω.2.2.1 ⟨p, hp⟩)) from rfl,
            show (XiC Φ ω).1 ⟨q, hq⟩ = Φ (ω.1.1 ⟨q, hq⟩, (ω.2.1.1 ⟨q, hq⟩, ω.2.2.1 ⟨q, hq⟩)) from rfl,
            show (XiC Φ ω).2 ⟨p, hp⟩ = Φ (ω.1.2 ⟨p, hp⟩, (ω.2.1.2 ⟨p, hp⟩, ω.2.2.2 ⟨p, hp⟩)) from rfl,
            show (XiC Φ ω).2 ⟨q, hq⟩ = Φ (ω.1.2 ⟨q, hq⟩, (ω.2.1.2 ⟨q, hq⟩, ω.2.2.2 ⟨q, hq⟩)) from rfl,
            hdot ω.1.1 ω.2.1.1 ω.2.2.1 _ _ hpq', hdot ω.1.2 ω.2.1.2 ω.2.2.2 _ _ hpq']
          ring
  have hh : InC rhoF tauF c1 (ccos (V := {i // ¬ i = v})) 1
      (fun ω : Om {i // ¬ i = v} ({i // ¬ i = v} → A1) ({i // ¬ i = v} → Tor) =>
        energy G J (jn (XiC Φ ω).1) + energy G J (jn (XiC Φ ω).2)) := by
    refine (InC.sum G.edgeFinset (fun e he => (hedge e he).const_mul
      (hJ e (SimpleGraph.mem_edgeFinset.mp he)))).congr (fun ω => ?_)
    unfold energy
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl (fun e _ => by ring)
  have hg := InC.obsObs (ρ := rhoF) (τ := tauF) (c1 := c1) (c2 := ccos (V := {i // ¬ i = v})) x' y'
    (dvec x') (dvec y')
  have key := H.cone_exp hg hh
  refine le_of_le_of_eq key (integral_congr_ae (ae_of_all _ (fun ω => ?_)))
  simp only
  rw [hb1 x hx ω, hb2 x hx ω, hb1 y hy ω, hb2 y hy ω, ← Real.exp_add]

end G2S3

#print axioms G2S3.gksz_generic
