/-
G2Kernel.Proofs.BlocksProof: proof of `blocks_statement` (module M4, Lemma 2.3, edge-pair form).
Kernel proof, step L-b. Split the energy as E = E_A + E_B over the edges inside A and the other edges, which lie
inside B. Under the free product measure, a function of the A-spins and a rotation-invariant function of the
B-spins are uncorrelated: split the configuration at A (Fubini); for fixed A-spins the inner integral of the
B-function depends on them only through σ_v, and a reflection mapping σ_v to any other unit vector (hSphereIso)
shows that it is constant. Hence the four Gibbs integrals factor and Cov(s_e, s_f) = 0.
-/
import G2Kernel.Blocks
import G2Kernel.Proofs.CornerProof

noncomputable section
open MeasureTheory Real

namespace G2Kernel

/-! ### Splitting along a predicate -/

/-- The configuration with spins `σ1` where `p` holds and `σ2` elsewhere. -/
def joinP {N : ℕ} {V : Type*} (p : V → Prop) [DecidablePred p] (σ1 : {i // p i} → Sph N)
    (σ2 : {i // ¬ p i} → Sph N) : Config N V :=
  fun i => if h : p i then σ1 ⟨i, h⟩ else σ2 ⟨i, h⟩

theorem joinP_pos {N : ℕ} {V : Type*} {p : V → Prop} [DecidablePred p] (σ1 : {i // p i} → Sph N)
    (σ2 : {i // ¬ p i} → Sph N) {i : V} (h : p i) : joinP p σ1 σ2 i = σ1 ⟨i, h⟩ := by
  simp [joinP, h]

theorem joinP_neg {N : ℕ} {V : Type*} {p : V → Prop} [DecidablePred p] (σ1 : {i // p i} → Sph N)
    (σ2 : {i // ¬ p i} → Sph N) {i : V} (h : ¬ p i) : joinP p σ1 σ2 i = σ2 ⟨i, h⟩ := by
  simp [joinP, h]

theorem integral_split_by {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (p : V → Prop) [DecidablePred p]
    (g : Config N V → ℝ) (hgm : Measurable g) (C : ℝ) (hgb : ∀ σ, |g σ| ≤ C) :
    ∫ σ, g σ ∂(freeMeasure N V)
      = ∫ σ1, ∫ σ2, g (joinP p σ1 σ2) ∂(Measure.pi fun _ : {i // ¬ p i} => omega N)
          ∂(Measure.pi fun _ : {i // p i} => omega N) := by
  have := omega_isProbabilityMeasure N hN
  have hmp := measurePreserving_piEquivPiSubtypeProd (fun _ : V => omega N) p
  have hsymm := MeasurePreserving.symm _ hmp
  have h1 := hsymm.integral_comp' g
  have hjoin : ∀ q : ({i // p i} → Sph N) × ({i // ¬ p i} → Sph N),
      (MeasurableEquiv.piEquivPiSubtypeProd (fun _ : V => Sph N) p).symm q = joinP p q.1 q.2 :=
    fun q => rfl
  simp only [hjoin] at h1
  unfold freeMeasure
  rw [← h1]
  have hm : Measurable (fun q : ({i // p i} → Sph N) × ({i // ¬ p i} → Sph N) => g (joinP p q.1 q.2)) :=
    hgm.comp (MeasurableEquiv.piEquivPiSubtypeProd (fun _ : V => Sph N) p).symm.measurable
  exact integral_prod (fun q => g (joinP p q.1 q.2)) (integrable_of_abs_le hm C (fun q => hgb _))

/-! ### Locality and rotation invariance -/

theorem DependsOnly.mul {N : ℕ} {V : Type*} {H : Set V} {F1 F2 : Config N V → ℝ}
    (h1 : DependsOnly H F1) (h2 : DependsOnly H F2) : DependsOnly H (fun σ => F1 σ * F2 σ) :=
  fun σ σ' h => by
    show F1 σ * F2 σ = F1 σ' * F2 σ'
    rw [h1 σ σ' h, h2 σ σ' h]

theorem DependsOnly.exp {N : ℕ} {V : Type*} {H : Set V} {F : Config N V → ℝ} (h : DependsOnly H F) :
    DependsOnly H (fun σ => Real.exp (F σ)) :=
  fun σ σ' hσ => by
    show Real.exp (F σ) = Real.exp (F σ')
    rw [h σ σ' hσ]

theorem bond_dependsOnly {N : ℕ} {V : Type*} (H : Set V) (g : Sym2 V) (hg : ∀ x ∈ g, x ∈ H) :
    DependsOnly H (bond (N := N) g) := by
  intro σ σ' hσ
  induction g using Sym2.ind with
  | h p q =>
    show dot (σ p) (σ q) = dot (σ' p) (σ' q)
    rw [hσ p (hg p (Sym2.mem_mk_left p q)), hσ q (hg q (Sym2.mem_mk_right p q))]

theorem bond_rot {N : ℕ} {V : Type*} (R : Amb N ≃ₗᵢ[ℝ] Amb N) (g : Sym2 V) (σ : Config N V) :
    bond g (fun i => sphMap R (σ i)) = bond g σ := by
  induction g using Sym2.ind with
  | h p q =>
    show @inner ℝ (Amb N) _ (R ((σ p : Sph N) : Amb N)) (R ((σ q : Sph N) : Amb N))
      = @inner ℝ (Amb N) _ ((σ p : Sph N) : Amb N) ((σ q : Sph N) : Amb N)
    exact LinearIsometryEquiv.inner_map_map R _ _

/-- The energy of the edges satisfying `P`. -/
def energyIn {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (P : Sym2 V → Prop) [DecidablePred P] (σ : Config N V) : ℝ :=
  ∑ g ∈ G.edgeFinset.filter P, J g * bond g σ

theorem energy_eq_energyIn_add {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (P : Sym2 V → Prop) [DecidablePred P] (σ : Config N V) :
    energy G J σ = energyIn G J P σ + energyIn G J (fun g => ¬ P g) σ := by
  unfold energy energyIn
  exact (Finset.sum_filter_add_sum_filter_not _ _ _).symm

theorem energyIn_dependsOnly {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (P : Sym2 V → Prop) [DecidablePred P] (H : Set V)
    (hP : ∀ g ∈ G.edgeFinset, P g → ∀ x ∈ g, x ∈ H) : DependsOnly H (energyIn (N := N) G J P) := by
  intro σ σ' h
  unfold energyIn
  apply Finset.sum_congr rfl
  intro g hg
  obtain ⟨hgE, hgP⟩ := Finset.mem_filter.mp hg
  rw [bond_dependsOnly H g (hP g hgE hgP) σ σ' h]

theorem energyIn_rot {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (P : Sym2 V → Prop) [DecidablePred P] (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V) :
    energyIn G J P (fun i => sphMap R (σ i)) = energyIn G J P σ := by
  unfold energyIn
  apply Finset.sum_congr rfl
  intro g _
  rw [bond_rot]

theorem measurable_energyIn {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (P : Sym2 V → Prop) [DecidablePred P] : Measurable (energyIn (N := N) G J P) := by
  show Measurable (fun σ : Config N V => ∑ g ∈ G.edgeFinset.filter P, J g * bond g σ)
  exact Finset.measurable_sum _ fun g _ => (measurable_bond g).const_mul (J g)

theorem abs_energyIn_le {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (P : Sym2 V → Prop) [DecidablePred P] (σ : Config N V) :
    |energyIn G J P σ| ≤ ∑ g ∈ G.edgeFinset.filter P, |J g| := by
  unfold energyIn
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun g _ => ?_)
  rw [abs_mul]
  exact mul_le_of_le_one_right (abs_nonneg _) (abs_bond_le g σ)

/-! ### Uncorrelated across a cut vertex -/

/-- A bounded function of the A-spins and a bounded rotation-invariant function of the B-spins are
uncorrelated under the free product measure when A and B meet only at v. -/
theorem integral_mul_of_cut {N : ℕ} (hN : 0 < N) (hS : hSphereIso N) {V : Type*} [Fintype V]
    (A B : Set V) [DecidablePred (· ∈ A)] (v : V) (hvA : v ∈ A)
    (hAB' : ∀ i, i ∈ A → i ∈ B → i = v)
    (φ ψ : Config N V → ℝ) (hφm : Measurable φ) (hψm : Measurable ψ) {Cφ Cψ : ℝ}
    (hφb : ∀ σ, |φ σ| ≤ Cφ) (hψb : ∀ σ, |ψ σ| ≤ Cψ) (hφd : DependsOnly A φ) (hψd : DependsOnly B ψ)
    (hψr : ∀ (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V), ψ (fun i => sphMap R (σ i)) = ψ σ) :
    ∫ σ, φ σ * ψ σ ∂(freeMeasure N V)
      = (∫ σ, φ σ ∂(freeMeasure N V)) * ∫ σ, ψ σ ∂(freeMeasure N V) := by
  have := omega_isProbabilityMeasure N hN
  have hφψm : Measurable (fun σ => φ σ * ψ σ) := hφm.mul hψm
  have hφψb : ∀ σ, |φ σ * ψ σ| ≤ Cφ * Cψ := fun σ => by
    rw [abs_mul]
    exact mul_le_mul (hφb σ) (hψb σ) (abs_nonneg _) ((abs_nonneg _).trans (hφb σ))
  rw [integral_split_by hN (fun i => i ∈ A) _ hφψm _ hφψb, integral_split_by hN (fun i => i ∈ A) _ hφm _ hφb,
    integral_split_by hN (fun i => i ∈ A) _ hψm _ hψb]
  obtain ⟨φt, hφt⟩ : ∃ φt : ({i // i ∈ A} → Sph N) → ℝ,
      φt = fun σ1 => φ (joinP (fun i => i ∈ A) σ1 (fun _ => σ1 ⟨v, hvA⟩)) := ⟨_, rfl⟩
  obtain ⟨K, hK⟩ : ∃ K : ({i // i ∈ A} → Sph N) → ℝ,
      K = fun σ1 => ∫ σ2, ψ (joinP (fun i => i ∈ A) σ1 σ2) ∂(Measure.pi fun _ : {i // ¬ i ∈ A} => omega N) :=
    ⟨_, rfl⟩
  have F1 : ∀ σ1 σ2, φ (joinP (fun i => i ∈ A) σ1 σ2) = φt σ1 := by
    intro σ1 σ2
    rw [hφt]
    apply hφd
    intro i hi
    rw [joinP_pos _ _ hi, joinP_pos _ _ hi]
  have F2 : ∀ σ1 σ1', K σ1 = K σ1' := by
    intro σ1 σ1'
    obtain ⟨z, hz⟩ : ∃ z : Amb N, z = ((σ1 ⟨v, hvA⟩ : Sph N) : Amb N) := ⟨_, rfl⟩
    obtain ⟨z', hz'⟩ : ∃ z' : Amb N, z' = ((σ1' ⟨v, hvA⟩ : Sph N) : Amb N) := ⟨_, rfl⟩
    have hzn : ‖z‖ = 1 := by
      rw [hz]
      exact norm_eq_of_mem_sphere _
    have hzn' : ‖z'‖ = 1 := by
      rw [hz']
      exact norm_eq_of_mem_sphere _
    obtain ⟨R, hR⟩ : ∃ R : Amb N ≃ₗᵢ[ℝ] Amb N, R = Submodule.reflection (ℝ ∙ (z - z'))ᗮ := ⟨_, rfl⟩
    have hRz : R z = z' := by
      rw [hR]
      exact Submodule.reflection_sub (hzn.trans hzn'.symm)
    have hjm : Measurable (fun σ2 : {i // ¬ i ∈ A} → Sph N => joinP (fun i => i ∈ A) σ1' σ2) :=
      (MeasurableEquiv.piEquivPiSubtypeProd (fun _ : V => Sph N) (fun i => i ∈ A)).symm.measurable.comp
        measurable_prodMk_left
    rw [hK]
    show ∫ σ2, ψ (joinP (fun i => i ∈ A) σ1 σ2) ∂(Measure.pi fun _ : {i // ¬ i ∈ A} => omega N)
      = ∫ σ2, ψ (joinP (fun i => i ∈ A) σ1' σ2) ∂(Measure.pi fun _ : {i // ¬ i ∈ A} => omega N)
    rw [← integral_reflect_pi hN hS R (fun σ2 => ψ (joinP (fun i => i ∈ A) σ1' σ2)) (hψm.comp hjm)]
    congr 1
    funext σ2
    rw [← hψr R (joinP (fun i => i ∈ A) σ1 σ2)]
    apply hψd
    intro i hi
    by_cases hiA : i ∈ A
    · have hiv : i = v := hAB' i hiA hi
      rw [joinP_pos _ _ hiA, joinP_pos _ _ hiA]
      apply Subtype.ext
      show R ((σ1 ⟨i, hiA⟩ : Sph N) : Amb N) = ((σ1' ⟨i, hiA⟩ : Sph N) : Amb N)
      have e1 : (⟨i, hiA⟩ : {i // i ∈ A}) = ⟨v, hvA⟩ := Subtype.ext hiv
      rw [e1, ← hz, ← hz', hRz]
    · rw [joinP_neg _ _ hiA, joinP_neg _ _ hiA]
  have F3 : ∀ σ1, K σ1 = ∫ σ1', K σ1' ∂(Measure.pi fun _ : {i // i ∈ A} => omega N) := by
    intro σ1
    rw [integral_congr_ae (ae_of_all _ (fun σ1' => (F2 σ1 σ1').symm)), integral_const, probReal_univ,
      one_smul]
  have e1 : (fun σ1 => ∫ σ2, φ (joinP (fun i => i ∈ A) σ1 σ2) * ψ (joinP (fun i => i ∈ A) σ1 σ2)
      ∂(Measure.pi fun _ : {i // ¬ i ∈ A} => omega N))
      = fun σ1 => φt σ1 * ∫ σ1', K σ1' ∂(Measure.pi fun _ : {i // i ∈ A} => omega N) := by
    funext σ1
    simp only [F1 σ1]
    rw [integral_const_mul, ← F3 σ1, hK]
  have e2 : (fun σ1 => ∫ σ2, φ (joinP (fun i => i ∈ A) σ1 σ2) ∂(Measure.pi fun _ : {i // ¬ i ∈ A} => omega N))
      = φt := by
    funext σ1
    simp only [F1 σ1]
    rw [integral_const, probReal_univ, one_smul]
  have e3 : (fun σ1 => ∫ σ2, ψ (joinP (fun i => i ∈ A) σ1 σ2) ∂(Measure.pi fun _ : {i // ¬ i ∈ A} => omega N))
      = K := hK.symm
  rw [e1, e2, e3, integral_mul_const]

/-! ### Lemma 2.3 -/

theorem blocks_thm (N : ℕ) : blocks_statement N := by
  unfold blocks_statement
  intro hS V _ _ G _ J A B v _hAB hAB' hedge e _he f _hf heA hfB
  classical
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · have hV : Nonempty V := ⟨v⟩
    have h0 : freeMeasure 0 V = 0 := freeMeasure_zero V
    simp [gibbsCov, gibbsExp, partition, h0]
  have := omega_isProbabilityMeasure N hN
  have : IsProbabilityMeasure (freeMeasure N V) := by
    unfold freeMeasure
    infer_instance
  have hvA : v ∈ A := by
    have h : v ∈ A ∩ B := by
      rw [hAB']
      exact Set.mem_singleton v
    exact h.1
  have hcut : ∀ i, i ∈ A → i ∈ B → i = v := fun i hiA hiB => by
    have h : i ∈ A ∩ B := ⟨hiA, hiB⟩
    rw [hAB'] at h
    exact Set.mem_singleton_iff.mp h
  -- the split of the energy
  have hPA : ∀ g ∈ G.edgeFinset, (∀ x ∈ g, x ∈ A) → ∀ x ∈ g, x ∈ A := fun _ _ h => h
  have hPB : ∀ g ∈ G.edgeFinset, (¬ ∀ x ∈ g, x ∈ A) → ∀ x ∈ g, x ∈ B := by
    intro g hg hnA
    induction g using Sym2.ind with
    | h p q =>
      have hadj : G.Adj p q := SimpleGraph.mem_edgeFinset.mp hg
      rcases hedge p q hadj with ⟨hp, hq⟩ | ⟨hp, hq⟩
      · exfalso
        apply hnA
        intro x hx
        rcases Sym2.mem_iff.mp hx with rfl | rfl
        · exact hp
        · exact hq
      · intro x hx
        rcases Sym2.mem_iff.mp hx with rfl | rfl
        · exact hp
        · exact hq
  set P : Sym2 V → Prop := fun g => ∀ x ∈ g, x ∈ A
  have hEAd : DependsOnly A (energyIn (N := N) G J P) := energyIn_dependsOnly G J P A hPA
  have hEBd : DependsOnly B (energyIn (N := N) G J (fun g => ¬ P g)) :=
    energyIn_dependsOnly G J (fun g => ¬ P g) B hPB
  have hmA := measurable_energyIn (N := N) G J P
  have hmB := measurable_energyIn (N := N) G J (fun g => ¬ P g)
  have hbA : ∀ σ : Config N V, |Real.exp (energyIn G J P σ)|
      ≤ Real.exp (∑ g ∈ G.edgeFinset.filter P, |J g|) := fun σ => abs_exp_le (abs_energyIn_le G J P σ)
  have hbB : ∀ σ : Config N V, |Real.exp (energyIn G J (fun g => ¬ P g) σ)|
      ≤ Real.exp (∑ g ∈ G.edgeFinset.filter (fun g => ¬ P g), |J g|) :=
    fun σ => abs_exp_le (abs_energyIn_le G J (fun g => ¬ P g) σ)
  have hde : DependsOnly A (bond (N := N) e) := bond_dependsOnly A e heA
  have hdf : DependsOnly B (bond (N := N) f) := bond_dependsOnly B f hfB
  -- the four factorizations
  have hrot1 : ∀ (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V),
      Real.exp (energyIn G J (fun g => ¬ P g) (fun i => sphMap R (σ i)))
        = Real.exp (energyIn G J (fun g => ¬ P g) σ) := fun R σ => by rw [energyIn_rot]
  have hrotf : ∀ (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V),
      bond f (fun i => sphMap R (σ i)) * Real.exp (energyIn G J (fun g => ¬ P g) (fun i => sphMap R (σ i)))
        = bond f σ * Real.exp (energyIn G J (fun g => ¬ P g) σ) := fun R σ => by
    rw [bond_rot, energyIn_rot]
  have f11 := integral_mul_of_cut hN hS A B v hvA hcut
    (fun σ => bond e σ * Real.exp (energyIn G J P σ))
    (fun σ => bond f σ * Real.exp (energyIn G J (fun g => ¬ P g) σ))
    ((measurable_bond e).mul hmA.exp) ((measurable_bond f).mul hmB.exp)
    (fun σ => abs_one_mul_le (abs_bond_le e σ) (hbA σ)) (fun σ => abs_one_mul_le (abs_bond_le f σ) (hbB σ))
    (hde.mul hEAd.exp) (hdf.mul hEBd.exp) hrotf
  have f00 := integral_mul_of_cut hN hS A B v hvA hcut
    (fun σ => Real.exp (energyIn G J P σ)) (fun σ => Real.exp (energyIn G J (fun g => ¬ P g) σ))
    hmA.exp hmB.exp hbA hbB hEAd.exp hEBd.exp hrot1
  have f10 := integral_mul_of_cut hN hS A B v hvA hcut
    (fun σ => bond e σ * Real.exp (energyIn G J P σ)) (fun σ => Real.exp (energyIn G J (fun g => ¬ P g) σ))
    ((measurable_bond e).mul hmA.exp) hmB.exp
    (fun σ => abs_one_mul_le (abs_bond_le e σ) (hbA σ)) hbB (hde.mul hEAd.exp) hEBd.exp hrot1
  have f01 := integral_mul_of_cut hN hS A B v hvA hcut
    (fun σ => Real.exp (energyIn G J P σ))
    (fun σ => bond f σ * Real.exp (energyIn G J (fun g => ¬ P g) σ))
    hmA.exp ((measurable_bond f).mul hmB.exp) hbA (fun σ => abs_one_mul_le (abs_bond_le f σ) (hbB σ))
    hEAd.exp (hdf.mul hEBd.exp) hrotf
  -- the Gibbs integrals in factored form
  have hexp : ∀ σ : Config N V, Real.exp (energy G J σ)
      = Real.exp (energyIn G J P σ) * Real.exp (energyIn G J (fun g => ¬ P g) σ) := by
    intro σ
    rw [energy_eq_energyIn_add G J P σ, Real.exp_add]
  have i11 : ∫ σ, bond e σ * bond f σ * Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, bond e σ * Real.exp (energyIn G J P σ)
          * (bond f σ * Real.exp (energyIn G J (fun g => ¬ P g) σ)) ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hexp σ]
    ring
  have i00 : ∫ σ, Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, Real.exp (energyIn G J P σ) * Real.exp (energyIn G J (fun g => ¬ P g) σ) ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hexp σ]
  have i10 : ∫ σ, bond e σ * Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, bond e σ * Real.exp (energyIn G J P σ)
          * Real.exp (energyIn G J (fun g => ¬ P g) σ) ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hexp σ]
    ring
  have i01 : ∫ σ, bond f σ * Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, Real.exp (energyIn G J P σ)
          * (bond f σ * Real.exp (energyIn G J (fun g => ¬ P g) σ)) ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hexp σ]
    ring
  have hKA : 0 < ∫ σ, Real.exp (energyIn G J P σ) ∂(freeMeasure N V) :=
    integral_exp_pos (integrable_of_abs_le hmA.exp _ hbA)
  have hKB : 0 < ∫ σ, Real.exp (energyIn G J (fun g => ¬ P g) σ) ∂(freeMeasure N V) :=
    integral_exp_pos (integrable_of_abs_le hmB.exp _ hbB)
  have hKA' := hKA.ne'
  have hKB' := hKB.ne'
  simp only [gibbsCov, gibbsExp, partition]
  rw [i11, i00, i10, i01, f11, f00, f10, f01]
  field

end G2Kernel
