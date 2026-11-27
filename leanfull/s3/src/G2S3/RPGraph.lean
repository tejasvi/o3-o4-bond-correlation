/-
G2S3.RPGraph (stage S3, Part A2): reflection positivity for the free measure on Config N V, for a reflection theta
of the vertex set with open half P (V = Fix theta + P + theta P), a weight exp(A(s) + A(s o theta) + crossing) with A
depending only on the closed half Fix + P, and a crossing term that is a nonnegative combination of products
u_k(s|P) u_k((s o theta)|P). Paper: Lemma 6.1 (tex l.1726-1738), both cases (line through vertices: no crossing
term; line between rows: crossing bonds J s_x . s_{theta x}).
-/
import G2S3.RPCore

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

/-- A reflection of a finite vertex set: an involution `θ` and an open half `P` with `P ∩ θ P = ∅`, such that every
vertex is fixed, in `P`, or in `θ P`. -/
structure ReflData (V : Type*) [DecidableEq V] where
  θ : V → V
  invol : ∀ v, θ (θ v) = v
  P : Finset V
  disj : ∀ v ∈ P, θ v ∉ P
  cover : ∀ v, θ v = v ∨ v ∈ P ∨ θ v ∈ P

namespace ReflData

variable {V : Type*} [DecidableEq V] (R : ReflData V)

/-- The closed half: the fixed points and `P`. -/
def S : Set V := {v | R.θ v = v ∨ v ∈ R.P}

/-- The fixed points and the open half as types. -/
abbrev Fx := {v : V // R.θ v = v}
abbrev Pt := {v : V // v ∈ R.P}

theorem ne_of_mem {v : V} (hv : v ∈ R.P) : R.θ v ≠ v := fun h => R.disj v hv (h.symm ▸ hv)

theorem mem_of_not {v : V} (h1 : R.θ v ≠ v) (h2 : v ∉ R.P) : R.θ v ∈ R.P := by
  rcases R.cover v with h | h | h
  · exact absurd h h1
  · exact absurd h h2
  · exact h

/-- `V = Fix ⊕ P ⊕ θ P`. -/
def split : R.Fx ⊕ (R.Pt ⊕ R.Pt) → V
  | .inl a => a.1
  | .inr (.inl p) => p.1
  | .inr (.inr p) => R.θ p.1

theorem split_bij : Function.Bijective R.split := by
  constructor
  · rintro (a | p | p) (b | q | q) h
    · exact congrArg _ (Subtype.ext h)
    · exact absurd (show R.θ q.1 = q.1 from (show q.1 = a.1 from h.symm) ▸ a.2) (R.ne_of_mem q.2)
    · exfalso
      have h' : a.1 = R.θ q.1 := h
      have : R.θ q.1 = q.1 := by
        have h2 := a.2
        rw [h'] at h2
        rw [R.invol] at h2
        exact h2.symm
      exact R.ne_of_mem q.2 this
    · exact absurd (show R.θ p.1 = p.1 from (show p.1 = b.1 from h) ▸ b.2) (R.ne_of_mem p.2)
    · exact congrArg _ (congrArg _ (Subtype.ext h))
    · exfalso
      have h' : p.1 = R.θ q.1 := h
      exact R.disj q.1 q.2 (h' ▸ p.2)
    · exfalso
      have h' : R.θ p.1 = b.1 := h
      have : R.θ p.1 = p.1 := by
        have h2 := b.2
        rw [← h'] at h2
        rw [R.invol] at h2
        exact h2.symm
      exact R.ne_of_mem p.2 this
    · exfalso
      have h' : R.θ p.1 = q.1 := h
      exact R.disj p.1 p.2 (h' ▸ q.2)
    · have h' : R.θ p.1 = R.θ q.1 := h
      have : p.1 = q.1 := by
        have := congrArg R.θ h'
        rwa [R.invol, R.invol] at this
      exact congrArg _ (congrArg _ (Subtype.ext this))
  · intro v
    rcases R.cover v with h | h | h
    · exact ⟨.inl ⟨v, h⟩, rfl⟩
    · exact ⟨.inr (.inl ⟨v, h⟩), rfl⟩
    · exact ⟨.inr (.inr ⟨R.θ v, h⟩), R.invol v⟩

/-- The equivalence `Fix ⊕ (P ⊕ P) ≃ V` (the second copy of `P` mapped by `θ`). -/
def splitEquiv : R.Fx ⊕ (R.Pt ⊕ R.Pt) ≃ V := Equiv.ofBijective R.split R.split_bij

variable (N : ℕ)

/-- `σ ↦ (σ|Fix, (σ|P, (σ ∘ θ)|P))` as a measurable equivalence. -/
def Xi : Config N V ≃ᵐ (R.Fx → Sph N) × ((R.Pt → Sph N) × (R.Pt → Sph N)) :=
  (MeasurableEquiv.piCongrLeft (fun _ : V => Sph N) R.splitEquiv).symm.trans
    ((MeasurableEquiv.sumPiEquivProdPi (fun _ : R.Fx ⊕ (R.Pt ⊕ R.Pt) => Sph N)).trans
      (MeasurableEquiv.prodCongr (MeasurableEquiv.refl _)
        (MeasurableEquiv.sumPiEquivProdPi (fun _ : R.Pt ⊕ R.Pt => Sph N))))

theorem Xi_apply (σ : Config N V) :
    R.Xi N σ = (fun a => σ a.1, (fun p => σ p.1, fun p => σ (R.θ p.1))) := rfl

theorem measurePreserving_Xi [Fintype V] (hN : 0 < N) :
    MeasurePreserving (R.Xi N) (freeMeasure N V)
      ((Measure.pi fun _ : R.Fx => omega N).prod
        ((Measure.pi fun _ : R.Pt => omega N).prod (Measure.pi fun _ : R.Pt => omega N))) := by
  have := omega_isProbabilityMeasure N hN
  have h1 := (measurePreserving_piCongrLeft (fun _ : V => omega N) R.splitEquiv).symm
  have h2 := measurePreserving_sumPiEquivProdPi (fun _ : R.Fx ⊕ (R.Pt ⊕ R.Pt) => omega N)
  have h3 := (MeasurePreserving.id (Measure.pi fun _ : R.Fx => omega N)).prod
    (measurePreserving_sumPiEquivProdPi (fun _ : R.Pt ⊕ R.Pt => omega N))
  exact (h3.comp h2).comp h1

/-- Rebuild a configuration from its values on `Fix` and on `P` (and the same values on `θ P`). -/
def recon {N : ℕ} (x : R.Fx → Sph N) (y : R.Pt → Sph N) : Config N V := fun v =>
  if h : R.θ v = v then x ⟨v, h⟩ else if hp : v ∈ R.P then y ⟨v, hp⟩ else y ⟨R.θ v, R.mem_of_not h hp⟩

theorem measurable_recon : Measurable (fun q : (R.Fx → Sph N) × (R.Pt → Sph N) => R.recon q.1 q.2) := by
  refine Measurable.of_eval (fun v => ?_)
  unfold recon
  by_cases h : R.θ v = v
  · simp only [h, dite_true]
    exact (measurable_pi_apply _).comp measurable_fst
  · by_cases hp : v ∈ R.P
    · simp only [h, hp, dite_false, dite_true]
      exact (measurable_pi_apply _).comp measurable_snd
    · simp only [h, hp, dite_false]
      exact (measurable_pi_apply _).comp measurable_snd

/-- the restriction to `P` -/
def restrP {N : ℕ} (σ : Config N V) : R.Pt → Sph N := fun p => σ p.1

theorem recon_agree {N : ℕ} (σ : Config N V) :
    ∀ v ∈ R.S, R.recon (fun a => σ a.1) (R.restrP σ) v = σ v := by
  intro v hv
  unfold recon
  by_cases h : R.θ v = v
  · simp [h]
  · have hp : v ∈ R.P := hv.resolve_left h
    simp [h, hp, restrP]

theorem recon_agree_refl {N : ℕ} (σ : Config N V) :
    ∀ v ∈ R.S, R.recon (fun a => σ a.1) (R.restrP (σ ∘ R.θ)) v = (σ ∘ R.θ) v := by
  intro v hv
  unfold recon
  by_cases h : R.θ v = v
  · simp [h, Function.comp]
  · have hp : v ∈ R.P := hv.resolve_left h
    simp [h, hp, restrP]

end ReflData

/-- **Reflection positivity on `Config N V`.** -/
theorem rp_config {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] [DecidableEq V] (R : ReflData V)
    {A F : Config N V → ℝ} (hA : BddMeas A) (hAd : DependsOnly R.S A) (hF : BddMeas F) (hFd : DependsOnly R.S F)
    {ι : Type*} (s : Finset ι) {w : ι → ℝ} (hw : ∀ k, 0 ≤ w k) {u : ι → (R.Pt → Sph N) → ℝ}
    (hu : ∀ k, BddMeas (u k)) :
    0 ≤ ∫ σ, F σ * F (σ ∘ R.θ) *
      Real.exp (A σ + A (σ ∘ R.θ) + rankSum s w u (R.restrP σ, R.restrP (σ ∘ R.θ))) ∂(freeMeasure N V) := by
  have := omega_isProbabilityMeasure N hN
  obtain ⟨g, hg⟩ : ∃ g : (R.Fx → Sph N) × (R.Pt → Sph N) → ℝ,
      g = fun q => F (R.recon q.1 q.2) * Real.exp (A (R.recon q.1 q.2)) := ⟨_, rfl⟩
  obtain ⟨K, hK⟩ : ∃ K : (R.Pt → Sph N) × (R.Pt → Sph N) → ℝ,
      K = fun p => Real.exp (1 * rankSum s w u p) := ⟨_, rfl⟩
  have key : ∀ σ : Config N V, F σ * F (σ ∘ R.θ) *
      Real.exp (A σ + A (σ ∘ R.θ) + rankSum s w u (R.restrP σ, R.restrP (σ ∘ R.θ)))
      = g ((R.Xi N σ).1, (R.Xi N σ).2.1) * g ((R.Xi N σ).1, (R.Xi N σ).2.2) * K (R.Xi N σ).2 := by
    intro σ
    rw [R.Xi_apply, hg, hK]
    dsimp only
    have e1 : F (R.recon (fun a => σ a.1) (fun p => σ p.1)) = F σ :=
      hFd _ _ (fun v hv => R.recon_agree σ v hv)
    have e2 : A (R.recon (fun a => σ a.1) (fun p => σ p.1)) = A σ :=
      hAd _ _ (fun v hv => R.recon_agree σ v hv)
    have e3 : F (R.recon (fun a => σ a.1) (fun p => σ (R.θ p.1))) = F (σ ∘ R.θ) :=
      hFd _ _ (fun v hv => R.recon_agree_refl σ v hv)
    have e4 : A (R.recon (fun a => σ a.1) (fun p => σ (R.θ p.1))) = A (σ ∘ R.θ) :=
      hAd _ _ (fun v hv => R.recon_agree_refl σ v hv)
    have e5 : R.restrP σ = (fun p => σ p.1) := rfl
    have e6 : R.restrP (σ ∘ R.θ) = (fun p => σ (R.θ p.1)) := rfl
    rw [e1, e2, e3, e4, e5, e6, Real.exp_add, Real.exp_add, one_mul]
    ring
  rw [integral_congr_ae (ae_of_all _ key)]
  have h : ∫ σ, g ((R.Xi N σ).1, (R.Xi N σ).2.1) * g ((R.Xi N σ).1, (R.Xi N σ).2.2) * K (R.Xi N σ).2
        ∂(freeMeasure N V)
      = ∫ q, g (q.1, q.2.1) * g (q.1, q.2.2) * K q.2
        ∂((Measure.pi fun _ : R.Fx => omega N).prod
          ((Measure.pi fun _ : R.Pt => omega N).prod (Measure.pi fun _ : R.Pt => omega N))) :=
    (R.measurePreserving_Xi N hN).integral_comp' (fun q => g (q.1, q.2.1) * g (q.1, q.2.2) * K q.2)
  rw [h]
  have hgb : BddMeas g := by
    rw [hg]
    obtain ⟨hFm, CF, hCF⟩ := hF
    obtain ⟨hAm, CA, hCA⟩ := hA
    refine ⟨(hFm.comp (R.measurable_recon N)).mul (hAm.comp (R.measurable_recon N)).exp, CF * Real.exp CA,
      fun q => ?_⟩
    rw [abs_mul]
    have hC0 : 0 ≤ CF := (abs_nonneg _).trans (hCF (R.recon q.1 q.2))
    exact mul_le_mul (hCF _) (abs_exp_le (hCA _)) (abs_nonneg _) hC0
  have hKb : BddMeas K := by
    rw [hK]
    obtain ⟨hSm, CS, hCS⟩ := rankSum_bdd s w hu
    refine ⟨(measurable_const.mul hSm).exp, Real.exp (1 * CS), fun p => ?_⟩
    refine abs_exp_le ?_
    rw [abs_mul, abs_one, one_mul, one_mul]
    exact hCS p
  have hKpd : PDKernel (Measure.pi fun _ : R.Pt => omega N) K := by
    rw [hK]
    exact pd_exp_rankSum _ s hw hu zero_le_one
  exact rp_prod _ _ hKpd hKb hgb

end G2S3

#print axioms G2S3.rp_config
