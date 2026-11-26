/-
G2Kernel.Proofs.CornerProof: proof of `corner_statement` (module M5, Lemma 6.2, the corner identity).
Kernel proof, step L-b. Split the configuration space at the corner v (`MeasurableEquiv.piEquivPiSubtypeProd`
and Fubini). For fixed spins off v, the reflection A in the hyperplane orthogonal to σ_x - σ_y exchanges σ_x and
σ_y and preserves ω (hSphereIso). Applied to σ_v it exchanges s_vx and s_vy, leaves the energy unchanged (v has
degree two and J_vx = J_vy) and leaves every function of the other spins unchanged. Hence
∫ s_vx Φ e^E = ∫ s_vy Φ e^E for every bounded Φ that does not depend on σ_v, which gives the identity of
covariances (take Φ = F and Φ = 1).
-/
import G2Kernel.Corner
import G2Kernel.Proofs.CycleProof

noncomputable section
open MeasureTheory Real

namespace G2Kernel

/-! ### Splitting off one site -/

/-- The configuration with spins `σ'` off `v` and `τ` at `v`. -/
def joinAt {N : ℕ} {V : Type*} [DecidableEq V] (v : V) (σ' : {i // i ≠ v} → Sph N)
    (τ : {i // ¬ i ≠ v} → Sph N) : Config N V :=
  fun i => if h : i ≠ v then σ' ⟨i, h⟩ else τ ⟨i, h⟩

theorem joinAt_of_ne {N : ℕ} {V : Type*} [DecidableEq V] {v i : V} (σ' : {i // i ≠ v} → Sph N)
    (τ : {i // ¬ i ≠ v} → Sph N) (h : i ≠ v) : joinAt v σ' τ i = σ' ⟨i, h⟩ := by
  simp [joinAt, h]

theorem joinAt_self {N : ℕ} {V : Type*} [DecidableEq V] (v : V) (σ' : {i // i ≠ v} → Sph N)
    (τ : {i // ¬ i ≠ v} → Sph N) : joinAt v σ' τ v = τ ⟨v, not_not.mpr rfl⟩ := by
  simp [joinAt]

/-- The configuration integral as an iterated integral: spins off `v` outside, the spin at `v` inside. -/
theorem integral_split_at {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] [DecidableEq V] (v : V)
    (g : Config N V → ℝ) (hgm : Measurable g) (C : ℝ) (hgb : ∀ σ, |g σ| ≤ C) :
    ∫ σ, g σ ∂(freeMeasure N V)
      = ∫ σ', ∫ τ, g (joinAt v σ' τ) ∂(Measure.pi fun _ : {i // ¬ i ≠ v} => omega N)
          ∂(Measure.pi fun _ : {i // i ≠ v} => omega N) := by
  have := omega_isProbabilityMeasure N hN
  have hmp := measurePreserving_piEquivPiSubtypeProd (fun _ : V => omega N) (fun i : V => i ≠ v)
  have hsymm := MeasurePreserving.symm _ hmp
  have h1 := hsymm.integral_comp' g
  have hjoin : ∀ p : ({i // i ≠ v} → Sph N) × ({i // ¬ i ≠ v} → Sph N),
      (MeasurableEquiv.piEquivPiSubtypeProd (fun _ : V => Sph N) (fun i : V => i ≠ v)).symm p
        = joinAt v p.1 p.2 := fun p => rfl
  simp only [hjoin] at h1
  unfold freeMeasure
  rw [← h1]
  have hm : Measurable (fun p : ({i // i ≠ v} → Sph N) × ({i // ¬ i ≠ v} → Sph N) => g (joinAt v p.1 p.2)) :=
    hgm.comp (MeasurableEquiv.piEquivPiSubtypeProd (fun _ : V => Sph N) (fun i : V => i ≠ v)).symm.measurable
  exact integral_prod (fun p => g (joinAt v p.1 p.2)) (integrable_of_abs_le hm C (fun p => hgb _))

/-- A linear isometry, restricted to the unit sphere. -/
def sphMap {N : ℕ} (A : Amb N ≃ₗᵢ[ℝ] Amb N) (z : Sph N) : Sph N :=
  ⟨A (z : Amb N), by simp⟩

/-- Applying one linear isometry to every spin of a product of copies of ω preserves the integral. -/
theorem integral_reflect_pi {N : ℕ} (hN : 0 < N) (hS : hSphereIso N) {ι : Type*} [Fintype ι]
    (A : Amb N ≃ₗᵢ[ℝ] Amb N) (H : (ι → Sph N) → ℝ) (hH : Measurable H) :
    ∫ τ, H (fun i => sphMap A (τ i)) ∂(Measure.pi fun _ : ι => omega N)
      = ∫ τ, H τ ∂(Measure.pi fun _ : ι => omega N) := by
  have := omega_isProbabilityMeasure N hN
  have hmp : MeasurePreserving (fun τ : ι → Sph N => fun i => sphMap A (τ i))
      (Measure.pi fun _ : ι => omega N) (Measure.pi fun _ : ι => omega N) :=
    measurePreserving_pi (fun _ : ι => omega N) (fun _ : ι => omega N) (fun _ => hS A)
  rw [← integral_map hmp.measurable.aemeasurable hH.aestronglyMeasurable, hmp.map_eq]

/-! ### The energy under the exchange at a corner -/

theorem energy_corner_swap {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V} (hnb : G.neighborFinset v = {x, y}) (_hxy : x ≠ y)
    (hJ : J s(v, x) = J s(v, y)) (σ σR : Config N V) (hoff : ∀ i, i ≠ v → σR i = σ i)
    (hbx : bond s(v, x) σR = bond s(v, y) σ) (hby : bond s(v, y) σR = bond s(v, x) σ) :
    energy G J σR = energy G J σ := by
  have hvx : G.Adj v x := by
    have h : x ∈ G.neighborFinset v := by
      rw [hnb]
      simp
    simpa using h
  have hvy : G.Adj v y := by
    have h : y ∈ G.neighborFinset v := by
      rw [hnb]
      simp
    simpa using h
  have ha : s(v, x) ∈ G.edgeFinset := SimpleGraph.mem_edgeFinset.mpr hvx
  have hb : s(v, y) ∈ G.edgeFinset := SimpleGraph.mem_edgeFinset.mpr hvy
  have hother : ∀ g ∈ G.edgeFinset, g ≠ s(v, x) → g ≠ s(v, y) → v ∉ g := by
    intro g hg hga hgb hvg
    obtain ⟨w, rfl⟩ := Sym2.mem_iff_exists.mp hvg
    have hadj : G.Adj v w := SimpleGraph.mem_edgeFinset.mp hg
    have hw : w ∈ G.neighborFinset v := by simpa using hadj
    rw [hnb] at hw
    rcases Finset.mem_insert.mp hw with h | h
    · exact hga (by rw [h])
    · exact hgb (by rw [Finset.mem_singleton.mp h])
  have hbond : ∀ g : Sym2 V, v ∉ g → bond g σR = bond g σ := by
    intro g hvg
    induction g using Sym2.ind with
    | h p q =>
      have hp : p ≠ v := fun h => hvg (by rw [← h]; exact Sym2.mem_mk_left p q)
      have hq : q ≠ v := fun h => hvg (by rw [← h]; exact Sym2.mem_mk_right p q)
      show dot (σR p) (σR q) = dot (σ p) (σ q)
      rw [hoff p hp, hoff q hq]
  unfold energy
  refine Finset.sum_equiv (Equiv.swap s(v, x) s(v, y)) (fun g => ?_) (fun g hg => ?_)
  · by_cases hga : g = s(v, x)
    · rw [hga, Equiv.swap_apply_left]
      exact ⟨fun _ => hb, fun _ => ha⟩
    · by_cases hgb : g = s(v, y)
      · rw [hgb, Equiv.swap_apply_right]
        exact ⟨fun _ => ha, fun _ => hb⟩
      · rw [Equiv.swap_apply_of_ne_of_ne hga hgb]
  · by_cases hga : g = s(v, x)
    · rw [hga, Equiv.swap_apply_left, hbx, hJ]
    · by_cases hgb : g = s(v, y)
      · rw [hgb, Equiv.swap_apply_right, hby, hJ]
      · rw [Equiv.swap_apply_of_ne_of_ne hga hgb, hbond g (hother g hg hga hgb)]

/-! ### Lemma 6.2 -/

/-- At a corner `v` with neighbours `x ≠ y` and equal couplings, `∫ s_vx Φ e^E = ∫ s_vy Φ e^E` for every bounded
measurable `Φ` that does not depend on `σ_v`. -/
theorem corner_key {N : ℕ} (hN : 0 < N) (hS : hSphereIso N) {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V} (hxy : x ≠ y)
    (hnb : G.neighborFinset v = {x, y}) (hJ : J s(v, x) = J s(v, y))
    (Φ : Config N V → ℝ) (hΦm : Measurable Φ) (B : ℝ) (hΦb : ∀ σ, |Φ σ| ≤ B)
    (hΦd : DependsOnly {w | w ≠ v} Φ) :
    ∫ σ, bond s(v, x) σ * Φ σ * Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, bond s(v, y) σ * Φ σ * Real.exp (energy G J σ) ∂(freeMeasure N V) := by
  have hvx : G.Adj v x := by
    have h : x ∈ G.neighborFinset v := by
      rw [hnb]
      simp
    simpa using h
  have hvy : G.Adj v y := by
    have h : y ∈ G.neighborFinset v := by
      rw [hnb]
      simp
    simpa using h
  have hxv : x ≠ v := (G.ne_of_adj hvx).symm
  have hyv : y ≠ v := (G.ne_of_adj hvy).symm
  have hmE := measurable_energy (N := N) G J
  have hgx : Measurable (fun σ : Config N V => bond s(v, x) σ * Φ σ * Real.exp (energy G J σ)) :=
    ((measurable_bond _).mul hΦm).mul hmE.exp
  have hgy : Measurable (fun σ : Config N V => bond s(v, y) σ * Φ σ * Real.exp (energy G J σ)) :=
    ((measurable_bond _).mul hΦm).mul hmE.exp
  have hΦe : ∀ σ : Config N V, |Φ σ * Real.exp (energy G J σ)| ≤ B * Real.exp (∑ g ∈ G.edgeFinset, |J g|) := by
    intro σ
    rw [abs_mul]
    exact mul_le_mul (hΦb σ) (abs_exp_le (abs_energy_le G J σ)) (abs_nonneg _) ((abs_nonneg _).trans (hΦb σ))
  have hbx : ∀ σ : Config N V,
      |bond s(v, x) σ * Φ σ * Real.exp (energy G J σ)| ≤ B * Real.exp (∑ g ∈ G.edgeFinset, |J g|) := by
    intro σ
    rw [mul_assoc]
    exact abs_one_mul_le (abs_bond_le _ σ) (hΦe σ)
  have hby : ∀ σ : Config N V,
      |bond s(v, y) σ * Φ σ * Real.exp (energy G J σ)| ≤ B * Real.exp (∑ g ∈ G.edgeFinset, |J g|) := by
    intro σ
    rw [mul_assoc]
    exact abs_one_mul_le (abs_bond_le _ σ) (hΦe σ)
  rw [integral_split_at hN v _ hgx _ hbx, integral_split_at hN v _ hgy _ hby]
  congr 1
  funext σ'
  -- the reflection exchanging the spins at x and y
  obtain ⟨u, hu⟩ : ∃ u : Amb N, u = ((σ' ⟨x, hxv⟩ : Sph N) : Amb N) := ⟨_, rfl⟩
  obtain ⟨w, hw⟩ : ∃ w : Amb N, w = ((σ' ⟨y, hyv⟩ : Sph N) : Amb N) := ⟨_, rfl⟩
  have hun : ‖u‖ = 1 := by
    rw [hu]
    exact norm_eq_of_mem_sphere _
  have hwn : ‖w‖ = 1 := by
    rw [hw]
    exact norm_eq_of_mem_sphere _
  obtain ⟨A, hA⟩ : ∃ A : Amb N ≃ₗᵢ[ℝ] Amb N, A = Submodule.reflection (ℝ ∙ (u - w))ᗮ := ⟨_, rfl⟩
  have hAA : ∀ p : Amb N, A (A p) = p := by
    intro p
    rw [hA]
    exact Submodule.reflection_reflection _ p
  have hAu : A u = w := by
    rw [hA]
    exact Submodule.reflection_sub (hun.trans hwn.symm)
  have hAw : A w = u := by
    rw [← hAu, hAA]
  have hAsymm : ∀ z p : Amb N, @inner ℝ (Amb N) _ (A z) p = @inner ℝ (Amb N) _ z (A p) := by
    intro z p
    calc @inner ℝ (Amb N) _ (A z) p = @inner ℝ (Amb N) _ (A z) (A (A p)) := by rw [hAA]
      _ = @inner ℝ (Amb N) _ z (A p) := LinearIsometryEquiv.inner_map_map A z (A p)
  have hjm : Measurable (fun τ : {i // ¬ i ≠ v} → Sph N => joinAt v σ' τ) :=
    (MeasurableEquiv.piEquivPiSubtypeProd (fun _ : V => Sph N) (fun i : V => i ≠ v)).symm.measurable.comp
      measurable_prodMk_left
  rw [← integral_reflect_pi hN hS A
    (fun τ => bond s(v, x) (joinAt v σ' τ) * Φ (joinAt v σ' τ) * Real.exp (energy G J (joinAt v σ' τ)))
    (hgx.comp hjm)]
  congr 1
  funext τ
  have hoff : ∀ i, i ≠ v → joinAt v σ' (fun j => sphMap A (τ j)) i = joinAt v σ' τ i :=
    fun i hi => by rw [joinAt_of_ne _ _ hi, joinAt_of_ne _ _ hi]
  have hvR : ((joinAt v σ' (fun j => sphMap A (τ j)) v : Sph N) : Amb N)
      = A ((joinAt v σ' τ v : Sph N) : Amb N) := by
    rw [joinAt_self, joinAt_self]
    rfl
  have hx' : ((joinAt v σ' τ x : Sph N) : Amb N) = u := by
    rw [joinAt_of_ne _ _ hxv, hu]
  have hy' : ((joinAt v σ' τ y : Sph N) : Amb N) = w := by
    rw [joinAt_of_ne _ _ hyv, hw]
  have b1 : bond s(v, x) (joinAt v σ' (fun j => sphMap A (τ j))) = bond s(v, y) (joinAt v σ' τ) := by
    simp only [bond, Sym2.lift_mk, dot]
    rw [hvR, hoff x hxv, hx', hAsymm, hAu, ← hy']
  have b2 : bond s(v, y) (joinAt v σ' (fun j => sphMap A (τ j))) = bond s(v, x) (joinAt v σ' τ) := by
    simp only [bond, Sym2.lift_mk, dot]
    rw [hvR, hoff y hyv, hy', hAsymm, hAw, ← hx']
  have hE' := energy_corner_swap G J hnb hxy hJ (joinAt v σ' τ) (joinAt v σ' (fun j => sphMap A (τ j)))
    hoff b1 b2
  have hΦ' : Φ (joinAt v σ' (fun j => sphMap A (τ j))) = Φ (joinAt v σ' τ) :=
    hΦd _ _ (fun i hi => hoff i hi)
  rw [b1, hΦ', hE']

theorem corner_thm (N : ℕ) : corner_statement N := by
  unfold corner_statement
  intro hS V _ _ G _ J v x y hxy hnb hJ F hFm hFb hFd
  obtain ⟨B, hB⟩ := hFb
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · have hV : Nonempty V := ⟨v⟩
    have h0 : freeMeasure 0 V = 0 := freeMeasure_zero V
    simp [gibbsCov, gibbsExp, partition, h0]
  have k1 := corner_key hN hS G J hxy hnb hJ F hFm B hB hFd
  have k0 := corner_key hN hS G J hxy hnb hJ (fun _ => 1) measurable_const 1 (fun _ => by simp)
    (fun _ _ _ => rfl)
  simp only [mul_one] at k0
  simp only [gibbsCov, gibbsExp]
  rw [k1, k0]

end G2Kernel
