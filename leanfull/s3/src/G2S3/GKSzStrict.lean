/-
G2S3.GKSzStrict (stage S3, Part B8): the strict form of the generic Ginibre-Dunlop inequality. If x and y are joined
by a path x - w - y with positive couplings that avoids v, then Cov(s_vx, s_vy) > 0. Proof: as gksz_generic, then
ConeInt.cone_strict bounds int g exp(h) below by J_xw J_wy int g D_xw D_wy, which StrictDup.dup_term evaluates to
J_xw J_wy 2/N^3 > 0 (paper, Corollary 3.8: "Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) > 0", tex l.438).
-/
import G2S3.GKSz
import G2S3.StrictDup

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

local instance instFactTwoPiPosS : Fact (0 < 2 * π) := ⟨Real.two_pi_pos⟩

/-- **Strict generic inequality**: with a vertex `w` adjacent to `x` and `y` by edges of positive coupling,
`Cov(s_vx, s_vy) > 0`. -/
theorem gksz_strict_generic {N : ℕ} (hN : 0 < N) {A1 : Type} [MeasurableSpace A1] (l1 : Measure A1)
    [IsProbabilityMeasure l1] (ν : Measure ℝ) [IsProbabilityMeasure ν] (Φ : ℝ × (A1 × Tor) → Sph N)
    (hΦ : MeasurePreserving Φ (ν.prod (l1.prod AddCircle.haarAddCircle)) (omega N)) (u : Sph N)
    (k : Fin N) (hu : ∀ s : Sph N, dot u s = (s : Amb N) k)
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
    (x y w : V) (hx : ¬ x = v) (hy : ¬ y = v) (hw : ¬ w = v) (hxy : x ≠ y) (hxw : G.Adj x w)
    (hwy : G.Adj w y) (hJxw : 0 < J s(x, w)) (hJwy : 0 < J s(w, y)) :
    0 < gibbsCov N G J (bond s(v, x)) (bond s(v, y)) := by
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
  refine div_pos ?_ (pow_pos (partition_pos hN G J) 2)
  rw [integral_cond hN v _ ((bF.mul bH).mul bw) (fun R σ => by simp only [rF, rH, rw']) u,
    integral_cond hN v _ bw (fun R σ => by simp only [rw']) u,
    integral_cond hN v _ (bF.mul bw) (fun R σ => by simp only [rF, rw']) u,
    integral_cond hN v _ (bH.mul bw) (fun R σ => by simp only [rH, rw']) u]
  have hc := cov_dup (Measure.pi fun _ : {i // ¬ i = v} => omega N) (bF.comp hjnm) (bH.comp hjnm) (bw.comp hjnm)
  simp only [hjn] at hc
  rw [hc]
  refine mul_pos (by norm_num) ?_
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
  -- the two path edges and the rest
  set exw : Sym2 V := s(x, w)
  set ewy : Sym2 V := s(w, y)
  have hexw : exw ∈ G.edgeFinset := SimpleGraph.mem_edgeFinset.mpr hxw
  have hewy : ewy ∈ G.edgeFinset := SimpleGraph.mem_edgeFinset.mpr hwy
  have hne : exw ≠ ewy := by
    intro h
    rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
    · exact hxw.ne h1
    · exact hxy h1
  have hewy' : ewy ∈ G.edgeFinset.erase exw := Finset.mem_erase.mpr ⟨Ne.symm hne, hewy⟩
  set D : Sym2 V → Om {i // ¬ i = v} ({i // ¬ i = v} → A1) ({i // ¬ i = v} → Tor) → ℝ :=
    fun e ω => bond e (jn (XiC Φ ω).1) + bond e (jn (XiC Φ ω).2) with hD
  have hA := (hedge exw hexw).const_mul (le_of_lt hJxw)
  have hB := (hedge ewy hewy).const_mul (le_of_lt hJwy)
  have hC : InC rhoF tauF c1 (ccos (V := {i // ¬ i = v})) 1
      (fun ω => ∑ e ∈ (G.edgeFinset.erase exw).erase ewy, J e * D e ω) :=
    InC.sum _ (fun e he => (hedge e (Finset.mem_of_mem_erase (Finset.mem_of_mem_erase he))).const_mul
      (hJ e (SimpleGraph.mem_edgeFinset.mp (Finset.mem_of_mem_erase (Finset.mem_of_mem_erase he)))))
  have hsplit : ∀ ω, energy G J (jn (XiC Φ ω).1) + energy G J (jn (XiC Φ ω).2)
      = J exw * D exw ω + J ewy * D ewy ω + ∑ e ∈ (G.edgeFinset.erase exw).erase ewy, J e * D e ω := by
    intro ω
    unfold energy
    rw [← Finset.sum_add_distrib, ← Finset.add_sum_erase _ _ hexw, ← Finset.add_sum_erase _ _ hewy']
    simp only [hD]
    ring
  have hg := InC.obsObs (ρ := rhoF) (τ := tauF) (c1 := c1) (c2 := ccos (V := {i // ¬ i = v})) x' y'
    (dvec x') (dvec y')
  have key := H.cone_strict hg hA hB hC
  -- the explicit term
  set w' : {i // ¬ i = v} := ⟨w, hw⟩ with hw'
  have hx'y' : x' ≠ y' := fun h => hxy (congrArg Subtype.val h)
  have hx'w' : x' ≠ w' := fun h => hxw.ne (congrArg Subtype.val h)
  have hy'w' : y' ≠ w' := fun h => hwy.ne (congrArg Subtype.val h).symm
  have hcf : ∀ (z : V) (hz : ¬ z = v) (σ : {i // ¬ i = v} → Sph N), cf k ⟨z, hz⟩ σ = bond s(v, z) (jn σ) := by
    intro z hz σ
    show ((σ ⟨z, hz⟩ : Sph N) : Amb N) k = dot (jn σ v) (jn σ z)
    simp only [hjn]
    rw [joinP_v, joinP_ne u _ hz, hu]
  have hdz : ∀ (a b : V) (ha : ¬ a = v) (hb : ¬ b = v) (σ : {i // ¬ i = v} → Sph N),
      dot (σ ⟨a, ha⟩) (σ ⟨b, hb⟩) = bond s(a, b) (jn σ) := by
    intro a b ha hb σ
    show _ = dot (jn σ a) (jn σ b)
    simp only [hjn]
    rw [joinP_ne u _ ha, joinP_ne u _ hb]
  have hΨ2m : Measurable (fun p : ({i // ¬ i = v} → Sph N) × ({i // ¬ i = v} → Sph N) =>
      (cf k x' p.1 - cf k x' p.2) * (cf k y' p.1 - cf k y' p.2)
        * (dot (p.1 x') (p.1 w') + dot (p.2 x') (p.2 w')) * (dot (p.1 w') (p.1 y') + dot (p.2 w') (p.2 y'))) := by
    have m1 := (cf_bdd (N := N) k x').1
    have m2 := (cf_bdd (N := N) k y').1
    have m3 := (dotz_bdd (N := N) x' w').1
    have m4 := (dotz_bdd (N := N) w' y').1
    exact ((((m1.comp measurable_fst).sub (m1.comp measurable_snd)).mul
      ((m2.comp measurable_fst).sub (m2.comp measurable_snd))).mul
      ((m3.comp measurable_fst).add (m3.comp measurable_snd))).mul
      ((m4.comp measurable_fst).add (m4.comp measurable_snd))
  have hX2 := integral_XiC hN Φ ν l1 AddCircle.haarAddCircle hΦ _ hΨ2m
  unfold freeMeasure at hX2
  have hdup := dup_term hN k hx'y' hx'w' hy'w'
  unfold freeMeasure at hdup
  rw [hdup] at hX2
  have hterm : ∫ ω, ((tauF (ω.1.1 x') * ccos (dvec x') ω.2.2.1 - tauF (ω.1.2 x') * ccos (dvec x') ω.2.2.2)
        * (tauF (ω.1.1 y') * ccos (dvec y') ω.2.2.1 - tauF (ω.1.2 y') * ccos (dvec y') ω.2.2.2))
        * (J exw * D exw ω * (J ewy * D ewy ω))
      ∂(POm {i // ¬ i = v} ν (Measure.pi fun _ => l1) (Measure.pi fun _ => AddCircle.haarAddCircle))
      = J exw * J ewy * (2 / (N : ℝ) ^ 3) := by
    rw [hX2, ← integral_const_mul]
    refine integral_congr_ae (ae_of_all _ (fun ω => ?_))
    simp only [hD]
    rw [hcf x hx, hcf x hx, hcf y hy, hcf y hy, hdz x w hx hw, hdz x w hx hw, hdz w y hw hy, hdz w y hw hy,
      hb1 x hx ω, hb2 x hx ω, hb1 y hy ω, hb2 y hy ω]
    ring
  have hpos : 0 < J exw * J ewy * (2 / (N : ℝ) ^ 3) := by
    have hN' : (0 : ℝ) < N := by exact_mod_cast hN
    positivity
  refine lt_of_lt_of_le (hterm ▸ hpos) (le_of_le_of_eq key (integral_congr_ae (ae_of_all _ (fun ω => ?_))))
  simp only
  rw [hb1 x hx ω, hb2 x hx ω, hb1 y hy ω, hb2 y hy ω, ← Real.exp_add, hsplit ω]
end G2S3

#print axioms G2S3.gksz_strict_generic
