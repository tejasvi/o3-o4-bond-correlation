/-
G2Kernel.Proofs.CactusProof: proofs of `blockRestrict_statement` (M4b, Lemma 2.3, second part), `cactus_statement`
(M3c, Theorem 1.1 on cacti) and `cactus_strict_statement` (M3c'). Kernel proof, step L-b.
- M4b: across the cut vertex the integral over the spins of B factors off (`integral_mul_of_cut`), so the Gibbs law
  of the spins in A is the law of the graph of the edges inside A.
- Two transfer lemmas: dropping the vertices outside a set (their spins integrate to 1, since ω is a probability
  measure), and transport along an injective map φ : Fin n → V. Together they carry a cycle block to the cycle graph
  C_n with the couplings J ∘ Sym2.map φ.
- M3c and M3c': induction along the block list, peeling the last block. That block meets the earlier ones in at most
  one vertex v; with A the complement of its vertices together with v, M4b keeps the covariances of the earlier
  blocks and those of the last block, and Lemma 2.3 (`blocks_thm`) makes the mixed covariances vanish. On a cycle
  block the covariance is that of C_n (`cycleG2_thm`, `cycleG2_strict_thm`); a single-edge block has no pair of
  distinct edges.
-/
import G2Kernel.Cactus
import G2Kernel.Proofs.AssemblyProof

noncomputable section
open MeasureTheory Real

namespace G2Kernel

/-! ### Graphs with the same edges -/

theorem restrictTo_adj {V : Type*} (G : SimpleGraph V) (A : Set V) (x y : V) :
    (restrictTo G A).Adj x y ↔ G.Adj x y ∧ x ∈ A ∧ y ∈ A := Iff.rfl

/-- The graph of the edges of `G` that lie in `S`. -/
def edgeRestrict {V : Type*} (G : SimpleGraph V) (S : Set (Sym2 V)) : SimpleGraph V where
  Adj x y := G.Adj x y ∧ s(x, y) ∈ S
  symm := ⟨fun x y h => ⟨h.1.symm, by rw [Sym2.eq_swap]; exact h.2⟩⟩
  loopless := ⟨fun _ h => G.irrefl h.1⟩

instance {V : Type*} (G : SimpleGraph V) (S : Set (Sym2 V)) : DecidableRel (edgeRestrict G S).Adj :=
  Classical.decRel _

theorem edgeRestrict_adj {V : Type*} (G : SimpleGraph V) (S : Set (Sym2 V)) (x y : V) :
    (edgeRestrict G S).Adj x y ↔ G.Adj x y ∧ s(x, y) ∈ S := Iff.rfl

theorem mem_edgeRestrict_edgeSet {V : Type*} (G : SimpleGraph V) (S : Set (Sym2 V)) (e : Sym2 V) :
    e ∈ (edgeRestrict G S).edgeSet ↔ e ∈ G.edgeSet ∧ e ∈ S := by
  induction e using Sym2.ind with
  | h x y => exact Iff.rfl

theorem energy_congr_edges {N : ℕ} {V : Type*} [Fintype V] (G H : SimpleGraph V) [DecidableRel G.Adj]
    [DecidableRel H.Adj] (h : G.edgeSet = H.edgeSet) (J : Sym2 V → ℝ) (σ : Config N V) :
    energy G J σ = energy H J σ := by
  have hE : G.edgeFinset = H.edgeFinset := by
    ext g
    rw [SimpleGraph.mem_edgeFinset, SimpleGraph.mem_edgeFinset, h]
  unfold energy
  rw [hE]

theorem gibbsCov_congr_edges {N : ℕ} {V : Type*} [Fintype V] (G H : SimpleGraph V) [DecidableRel G.Adj]
    [DecidableRel H.Adj] (h : G.edgeSet = H.edgeSet) (J : Sym2 V → ℝ) (F F' : Config N V → ℝ) :
    gibbsCov N G J F F' = gibbsCov N H J F F' := by
  simp only [gibbsCov, gibbsExp, partition, energy_congr_edges G H h J]

/-! ### Lemma 2.3, second part (M4b) -/

theorem energy_restrictTo {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (A : Set V)
    [DecidablePred (· ∈ A)] [DecidablePred (fun g : Sym2 V => ∀ x ∈ g, x ∈ A)] (J : Sym2 V → ℝ)
    (σ : Config N V) :
    energy (restrictTo G A) J σ = energyIn G J (fun g => ∀ x ∈ g, x ∈ A) σ := by
  unfold energy energyIn
  apply Finset.sum_congr _ (fun _ _ => rfl)
  ext g
  induction g using Sym2.ind with
  | h p q =>
    rw [Finset.mem_filter, SimpleGraph.mem_edgeFinset, SimpleGraph.mem_edgeFinset, SimpleGraph.mem_edgeSet,
      SimpleGraph.mem_edgeSet, restrictTo_adj]
    constructor
    · rintro ⟨h, hp, hq⟩
      refine ⟨h, fun x hx => ?_⟩
      rcases Sym2.mem_iff.mp hx with rfl | rfl
      · exact hp
      · exact hq
    · rintro ⟨h, hx⟩
      exact ⟨h, hx p (Sym2.mem_mk_left _ _), hx q (Sym2.mem_mk_right _ _)⟩

theorem blockRestrict_thm (N : ℕ) : blockRestrict_statement N := by
  unfold blockRestrict_statement
  intro hS V _ _ G _ J A B _ v _hAB hAB' hedge e f heA hfA
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
  have hdf : DependsOnly A (bond (N := N) f) := bond_dependsOnly A f hfA
  have hrot1 : ∀ (R : Amb N ≃ₗᵢ[ℝ] Amb N) (σ : Config N V),
      Real.exp (energyIn G J (fun g => ¬ P g) (fun i => sphMap R (σ i)))
        = Real.exp (energyIn G J (fun g => ¬ P g) σ) := fun R σ => by rw [energyIn_rot]
  -- the four factorizations: a function of the spins in A against the weight of the edges not inside A
  have f11 := integral_mul_of_cut hN hS A B v hvA hcut
    (fun σ => bond e σ * bond f σ * Real.exp (energyIn G J P σ))
    (fun σ => Real.exp (energyIn G J (fun g => ¬ P g) σ))
    (((measurable_bond e).mul (measurable_bond f)).mul hmA.exp) hmB.exp
    (fun σ => by
      rw [mul_assoc]
      exact abs_one_mul_le (abs_bond_le e σ) (abs_one_mul_le (abs_bond_le f σ) (hbA σ)))
    hbB ((hde.mul hdf).mul hEAd.exp) hEBd.exp hrot1
  have f10 := integral_mul_of_cut hN hS A B v hvA hcut
    (fun σ => bond e σ * Real.exp (energyIn G J P σ)) (fun σ => Real.exp (energyIn G J (fun g => ¬ P g) σ))
    ((measurable_bond e).mul hmA.exp) hmB.exp
    (fun σ => abs_one_mul_le (abs_bond_le e σ) (hbA σ)) hbB (hde.mul hEAd.exp) hEBd.exp hrot1
  have f01 := integral_mul_of_cut hN hS A B v hvA hcut
    (fun σ => bond f σ * Real.exp (energyIn G J P σ)) (fun σ => Real.exp (energyIn G J (fun g => ¬ P g) σ))
    ((measurable_bond f).mul hmA.exp) hmB.exp
    (fun σ => abs_one_mul_le (abs_bond_le f σ) (hbA σ)) hbB (hdf.mul hEAd.exp) hEBd.exp hrot1
  have f00 := integral_mul_of_cut hN hS A B v hvA hcut
    (fun σ => Real.exp (energyIn G J P σ)) (fun σ => Real.exp (energyIn G J (fun g => ¬ P g) σ))
    hmA.exp hmB.exp hbA hbB hEAd.exp hEBd.exp hrot1
  have hexp : ∀ σ : Config N V, Real.exp (energy G J σ)
      = Real.exp (energyIn G J P σ) * Real.exp (energyIn G J (fun g => ¬ P g) σ) := by
    intro σ
    rw [energy_eq_energyIn_add G J P σ, Real.exp_add]
  have i11 : ∫ σ, bond e σ * bond f σ * Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, bond e σ * bond f σ * Real.exp (energyIn G J P σ)
          * Real.exp (energyIn G J (fun g => ¬ P g) σ) ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hexp σ]
    ring
  have i10 : ∫ σ, bond e σ * Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, bond e σ * Real.exp (energyIn G J P σ)
          * Real.exp (energyIn G J (fun g => ¬ P g) σ) ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hexp σ]
    ring
  have i01 : ∫ σ, bond f σ * Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, bond f σ * Real.exp (energyIn G J P σ)
          * Real.exp (energyIn G J (fun g => ¬ P g) σ) ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hexp σ]
    ring
  have i00 : ∫ σ, Real.exp (energy G J σ) ∂(freeMeasure N V)
      = ∫ σ, Real.exp (energyIn G J P σ) * Real.exp (energyIn G J (fun g => ¬ P g) σ) ∂(freeMeasure N V) := by
    congr 1
    funext σ
    rw [hexp σ]
  have hR : ∀ σ : Config N V, energy (restrictTo G A) J σ = energyIn G J P σ :=
    fun σ => energy_restrictTo G A J σ
  have hKA : 0 < ∫ σ, Real.exp (energyIn G J P σ) ∂(freeMeasure N V) :=
    integral_exp_pos (integrable_of_abs_le hmA.exp _ hbA)
  have hKB : 0 < ∫ σ, Real.exp (energyIn G J (fun g => ¬ P g) σ) ∂(freeMeasure N V) :=
    integral_exp_pos (integrable_of_abs_le hmB.exp _ hbB)
  have hKA' := hKA.ne'
  have hKB' := hKB.ne'
  simp only [gibbsCov, gibbsExp, partition, hR]
  rw [i11, i00, i10, i01, f11, f00, f10, f01]
  field

/-! ### Dropping isolated vertices and transport along an injective map -/

theorem bond_map {N : ℕ} {V W : Type*} (φ : W → V) (g : Sym2 W) (σ : Config N V) :
    bond g (σ ∘ φ) = bond (Sym2.map φ g) σ := by
  induction g using Sym2.ind with
  | h p q => rfl

/-- The spins off the set `p` integrate to 1: restricting a configuration to `{i // p i}` carries the free measure
to the free measure of the subtype. -/
theorem measurePreserving_restrict_sub {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (p : V → Prop)
    [DecidablePred p] :
    MeasurePreserving (fun σ : Config N V => fun i : {i // p i} => σ i) (freeMeasure N V)
      (Measure.pi fun _ : {i // p i} => omega N) := by
  have := omega_isProbabilityMeasure N hN
  have h1 := measurePreserving_piEquivPiSubtypeProd (fun _ : V => omega N) p
  have h2 : MeasurePreserving
      (Prod.fst : ({i // p i} → Sph N) × ({i // ¬ p i} → Sph N) → ({i // p i} → Sph N))
      ((Measure.pi fun _ : {i // p i} => omega N).prod (Measure.pi fun _ : {i // ¬ p i} => omega N))
      (Measure.pi fun _ : {i // p i} => omega N) := measurePreserving_fst
  exact h2.comp h1

/-- Transport along an equivalence of index types. -/
theorem measurePreserving_relabel {N : ℕ} (hN : 0 < N) {W U : Type*} [Fintype W] [Fintype U] (e : W ≃ U) :
    MeasurePreserving (fun τ : U → Sph N => fun w => τ (e w)) (Measure.pi fun _ : U => omega N)
      (freeMeasure N W) := by
  have := omega_isProbabilityMeasure N hN
  exact measurePreserving_arrowCongr' (fun _ : U => omega N) (fun _ : W => omega N) e.symm
    (MeasurableEquiv.refl (Sph N)) (fun _ => MeasurePreserving.id (omega N))

theorem measurePreserving_comp_inj {N : ℕ} (hN : 0 < N) {V W : Type*} [Fintype V] [Fintype W]
    (φ : W → V) (hφ : Function.Injective φ) :
    MeasurePreserving (fun σ : Config N V => σ ∘ φ) (freeMeasure N V) (freeMeasure N W) := by
  classical
  let p : V → Prop := fun i => ∃ w, φ w = i
  let e : W ≃ {i // p i} := Equiv.ofBijective (fun w => ⟨φ w, w, rfl⟩)
    ⟨fun w w' h => hφ (congrArg Subtype.val h), fun i => ⟨i.2.choose, Subtype.ext i.2.choose_spec⟩⟩
  exact (measurePreserving_relabel hN e).comp (measurePreserving_restrict_sub hN p)

theorem integral_comp_inj {N : ℕ} (hN : 0 < N) {V W : Type*} [Fintype V] [Fintype W] (φ : W → V)
    (hφ : Function.Injective φ) (F : Config N W → ℝ) (hF : Measurable F) :
    ∫ σ, F (σ ∘ φ) ∂(freeMeasure N V) = ∫ τ, F τ ∂(freeMeasure N W) := by
  have hmp := measurePreserving_comp_inj hN φ hφ
  rw [← hmp.map_eq, integral_map hmp.measurable.aemeasurable hF.aestronglyMeasurable]

theorem energy_transport {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V] {n : ℕ}
    [DecidableRel (SimpleGraph.cycleGraph n).Adj] (φ : Fin n → V) (hφ : Function.Injective φ)
    (H : SimpleGraph V) [DecidableRel H.Adj]
    (hH : H.edgeSet = Sym2.map φ '' (SimpleGraph.cycleGraph n).edgeSet) (J : Sym2 V → ℝ) (σ : Config N V) :
    energy H J σ = energy (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) (σ ∘ φ) := by
  have hE : H.edgeFinset = (SimpleGraph.cycleGraph n).edgeFinset.image (Sym2.map φ) := by
    ext g
    rw [SimpleGraph.mem_edgeFinset, hH, Finset.mem_image]
    constructor
    · rintro ⟨a, ha, rfl⟩
      exact ⟨a, SimpleGraph.mem_edgeFinset.mpr ha, rfl⟩
    · rintro ⟨a, ha, rfl⟩
      exact ⟨a, SimpleGraph.mem_edgeFinset.mp ha, rfl⟩
  unfold energy
  rw [hE, Finset.sum_image (Set.injOn_of_injective (Sym2.map.injective hφ))]
  apply Finset.sum_congr rfl
  intro g _
  exact congrArg (fun x => J (Sym2.map φ g) * x) (bond_map φ g σ).symm

theorem gibbsExp_transport {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] [DecidableEq V] {n : ℕ}
    [DecidableRel (SimpleGraph.cycleGraph n).Adj] (φ : Fin n → V) (hφ : Function.Injective φ)
    (H : SimpleGraph V) [DecidableRel H.Adj]
    (hH : H.edgeSet = Sym2.map φ '' (SimpleGraph.cycleGraph n).edgeSet) (J : Sym2 V → ℝ)
    (F : Config N (Fin n) → ℝ) (hF : Measurable F) :
    gibbsExp N H J (fun σ => F (σ ∘ φ)) = gibbsExp N (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) F := by
  have hm : Measurable (fun τ : Config N (Fin n) =>
      Real.exp (energy (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) τ)) := (measurable_energy _ _).exp
  have h1 : ∫ σ, F (σ ∘ φ) * Real.exp (energy (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) (σ ∘ φ))
        ∂(freeMeasure N V)
      = ∫ τ, F τ * Real.exp (energy (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) τ) ∂(freeMeasure N (Fin n)) :=
    integral_comp_inj hN φ hφ (fun τ => F τ * Real.exp (energy (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) τ))
      (hF.mul hm)
  have h2 : ∫ σ, Real.exp (energy (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) (σ ∘ φ)) ∂(freeMeasure N V)
      = ∫ τ, Real.exp (energy (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) τ) ∂(freeMeasure N (Fin n)) :=
    integral_comp_inj hN φ hφ (fun τ => Real.exp (energy (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) τ)) hm
  simp only [gibbsExp, partition, energy_transport φ hφ H hH J]
  rw [h1, h2]

theorem gibbsCov_transport {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] [DecidableEq V] {n : ℕ}
    [DecidableRel (SimpleGraph.cycleGraph n).Adj] (φ : Fin n → V) (hφ : Function.Injective φ)
    (H : SimpleGraph V) [DecidableRel H.Adj]
    (hH : H.edgeSet = Sym2.map φ '' (SimpleGraph.cycleGraph n).edgeSet) (J : Sym2 V → ℝ) (a b : Sym2 (Fin n)) :
    gibbsCov N H J (bond (Sym2.map φ a)) (bond (Sym2.map φ b))
      = gibbsCov N (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) (bond a) (bond b) := by
  have ha : bond (N := N) (Sym2.map φ a) = fun σ => bond a (σ ∘ φ) :=
    funext fun σ => (bond_map φ a σ).symm
  have hb : bond (N := N) (Sym2.map φ b) = fun σ => bond b (σ ∘ φ) :=
    funext fun σ => (bond_map φ b σ).symm
  have e1 : (fun σ => bond (N := N) (Sym2.map φ a) σ * bond (Sym2.map φ b) σ)
      = fun σ => bond a (σ ∘ φ) * bond b (σ ∘ φ) := funext fun σ => by simp only [bond_map]
  have hab : gibbsExp N H J (fun σ => bond a (σ ∘ φ) * bond b (σ ∘ φ))
      = gibbsExp N (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) (fun τ => bond a τ * bond b τ) :=
    gibbsExp_transport hN φ hφ H hH J (fun τ => bond a τ * bond b τ) ((measurable_bond a).mul (measurable_bond b))
  unfold gibbsCov
  rw [e1, hab, ha, hb, gibbsExp_transport hN φ hφ H hH J (bond a) (measurable_bond a),
    gibbsExp_transport hN φ hφ H hH J (bond b) (measurable_bond b)]

/-! ### Blocks and block lists -/

namespace CactusBlock

theorem mem_verts_of_mem_edges {V : Type*} {B : CactusBlock V} {e : Sym2 V} (he : e ∈ B.edges) {x : V}
    (hx : x ∈ e) : x ∈ B.verts := by
  cases B with
  | edge e₀ =>
    have h : e = e₀ := he
    rw [h] at hx
    exact hx
  | cycle n φ =>
    obtain ⟨g, -, rfl⟩ := he
    obtain ⟨y, -, rfl⟩ := Sym2.mem_map.mp hx
    exact ⟨y, rfl⟩

theorem edges_sub_edgeSet {V : Type*} {G : SimpleGraph V} {B : CactusBlock V} (hB : B.IsBlockOf G) {e : Sym2 V}
    (he : e ∈ B.edges) : e ∈ G.edgeSet := by
  cases B with
  | edge e₀ =>
    have h : e = e₀ := he
    rw [h]
    exact hB
  | cycle n φ =>
    obtain ⟨-, -, hadj⟩ := hB
    obtain ⟨g, hg, rfl⟩ := he
    induction g using Sym2.ind with
    | h a b => exact hadj a b hg

theorem exists_mem_verts {V : Type*} {G : SimpleGraph V} {B : CactusBlock V} (hB : B.IsBlockOf G) :
    ∃ x, x ∈ B.verts := by
  cases B with
  | edge e₀ =>
    induction e₀ using Sym2.ind with
    | h a b => exact ⟨a, Sym2.mem_mk_left a b⟩
  | cycle n φ =>
    obtain ⟨hn, -, -⟩ := hB
    exact ⟨φ ⟨0, by omega⟩, ⟨_, rfl⟩⟩

end CactusBlock

/-- The edges, and the vertices, of the blocks of a list. -/
def listEdges {V : Type*} (L : List (CactusBlock V)) : Set (Sym2 V) := {e | ∃ B ∈ L, e ∈ B.edges}
def listVerts {V : Type*} (L : List (CactusBlock V)) : Set V := {x | ∃ B ∈ L, x ∈ B.verts}

theorem mem_listEdges_append {V : Type*} (L : List (CactusBlock V)) (B : CactusBlock V) (e : Sym2 V) :
    e ∈ listEdges (L ++ [B]) ↔ e ∈ listEdges L ∨ e ∈ B.edges := by
  constructor
  · rintro ⟨B', hB', he⟩
    rcases List.mem_append.mp hB' with h | h
    · exact Or.inl ⟨B', h, he⟩
    · rw [List.mem_singleton] at h
      rw [h] at he
      exact Or.inr he
  · rintro (⟨B', hB', he⟩ | he)
    · exact ⟨B', List.mem_append.mpr (Or.inl hB'), he⟩
    · exact ⟨B, List.mem_append.mpr (Or.inr (List.mem_singleton.mpr rfl)), he⟩

theorem mem_listVerts_of_mem_listEdges {V : Type*} {L : List (CactusBlock V)} {e : Sym2 V}
    (he : e ∈ listEdges L) {x : V} (hx : x ∈ e) : x ∈ listVerts L := by
  obtain ⟨B, hB, heB⟩ := he
  exact ⟨B, hB, CactusBlock.mem_verts_of_mem_edges heB hx⟩

theorem listEdges_sub {V : Type*} {G : SimpleGraph V} {L : List (CactusBlock V)}
    (hval : ∀ B ∈ L, B.IsBlockOf G) {e : Sym2 V} (he : e ∈ listEdges L) : e ∈ G.edgeSet := by
  obtain ⟨B, hB, heB⟩ := he
  exact CactusBlock.edges_sub_edgeSet (hval B hB) heB

/-! ### One step: the last block of the list -/

theorem peel_step {N : ℕ} (hS : hSphereIso N) {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    (J : Sym2 V → ℝ) (L' : List (CactusBlock V)) (B : CactusBlock V) (hval' : ∀ B'' ∈ L', B''.IsBlockOf G)
    (hB : B.IsBlockOf G)
    (hlast : ∀ x y, x ∈ B.verts → y ∈ B.verts → x ∈ listVerts L' → y ∈ listVerts L' → x = y) :
    (∀ e ∈ listEdges L', ∀ f ∈ listEdges L',
      gibbsCov N (edgeRestrict G (listEdges (L' ++ [B]))) J (bond e) (bond f)
        = gibbsCov N (edgeRestrict G (listEdges L')) J (bond e) (bond f)) ∧
    (∀ e ∈ B.edges, ∀ f ∈ B.edges,
      gibbsCov N (edgeRestrict G (listEdges (L' ++ [B]))) J (bond e) (bond f)
        = gibbsCov N (edgeRestrict G B.edges) J (bond e) (bond f)) ∧
    (∀ e ∈ listEdges L', ∀ f ∈ B.edges,
      gibbsCov N (edgeRestrict G (listEdges (L' ++ [B]))) J (bond e) (bond f) = 0) := by
  classical
  -- the vertex at which the last block is attached (any vertex of it if it meets nothing earlier)
  obtain ⟨v, hvB, hv⟩ : ∃ v, v ∈ B.verts ∧ ∀ x, x ∈ B.verts → x ∈ listVerts L' → x = v := by
    by_cases h : ∃ x, x ∈ B.verts ∧ x ∈ listVerts L'
    · obtain ⟨x, hxB, hxL⟩ := h
      exact ⟨x, hxB, fun y hyB hyL => hlast y x hyB hxB hyL hxL⟩
    · obtain ⟨x, hx⟩ := CactusBlock.exists_mem_verts hB
      exact ⟨x, hx, fun y hyB hyL => (h ⟨y, hyB, hyL⟩).elim⟩
  obtain ⟨A, hA⟩ : ∃ A : Set V, ∀ x, x ∈ A ↔ (x ∉ B.verts ∨ x = v) :=
    ⟨{x | x ∉ B.verts ∨ x = v}, fun x => Iff.rfl⟩
  have hLA : ∀ x, x ∈ listVerts L' → x ∈ A := by
    intro x hx
    by_cases hxB : x ∈ B.verts
    · exact (hA x).mpr (Or.inr (hv x hxB hx))
    · exact (hA x).mpr (Or.inl hxB)
  have hAB : A ∪ B.verts = Set.univ := by
    apply Set.eq_univ_of_forall
    intro x
    by_cases hxB : x ∈ B.verts
    · exact Or.inr hxB
    · exact Or.inl ((hA x).mpr (Or.inl hxB))
  have hAB' : A ∩ B.verts = {v} := by
    ext x
    constructor
    · rintro ⟨hxA, hxB⟩
      exact ((hA x).mp hxA).resolve_left (not_not.mpr hxB)
    · intro hx
      rw [Set.mem_singleton_iff] at hx
      rw [hx]
      exact ⟨(hA v).mpr (Or.inr rfl), hvB⟩
  have hedge : ∀ x y, (edgeRestrict G (listEdges (L' ++ [B]))).Adj x y →
      (x ∈ A ∧ y ∈ A) ∨ (x ∈ B.verts ∧ y ∈ B.verts) := by
    intro x y hxy
    rcases (mem_listEdges_append L' B s(x, y)).mp hxy.2 with h | h
    · exact Or.inl ⟨hLA x (mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_left x y)),
        hLA y (mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_right x y))⟩
    · exact Or.inr ⟨CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_left x y),
        CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_right x y)⟩
  have hset1 : (restrictTo (edgeRestrict G (listEdges (L' ++ [B]))) A).edgeSet
      = (edgeRestrict G (listEdges L')).edgeSet := by
    ext g
    induction g using Sym2.ind with
    | h x y =>
      rw [SimpleGraph.mem_edgeSet, SimpleGraph.mem_edgeSet, restrictTo_adj, edgeRestrict_adj, edgeRestrict_adj,
        mem_listEdges_append]
      constructor
      · rintro ⟨⟨hadj, h | h⟩, hxA, hyA⟩
        · exact ⟨hadj, h⟩
        · exfalso
          have hx := CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_left x y)
          have hy := CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_right x y)
          have hxv : x = v := ((hA x).mp hxA).resolve_left (not_not.mpr hx)
          have hyv : y = v := ((hA y).mp hyA).resolve_left (not_not.mpr hy)
          rw [hxv, hyv] at hadj
          exact G.irrefl hadj
      · rintro ⟨hadj, h⟩
        exact ⟨⟨hadj, Or.inl h⟩, hLA x (mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_left x y)),
          hLA y (mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_right x y))⟩
  have hset2 : (restrictTo (edgeRestrict G (listEdges (L' ++ [B]))) B.verts).edgeSet
      = (edgeRestrict G B.edges).edgeSet := by
    ext g
    induction g using Sym2.ind with
    | h x y =>
      rw [SimpleGraph.mem_edgeSet, SimpleGraph.mem_edgeSet, restrictTo_adj, edgeRestrict_adj, edgeRestrict_adj,
        mem_listEdges_append]
      constructor
      · rintro ⟨⟨hadj, h | h⟩, hxB, hyB⟩
        · exfalso
          have hxv := hv x hxB (mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_left x y))
          have hyv := hv y hyB (mem_listVerts_of_mem_listEdges h (Sym2.mem_mk_right x y))
          rw [hxv, hyv] at hadj
          exact G.irrefl hadj
        · exact ⟨hadj, h⟩
      · rintro ⟨hadj, h⟩
        exact ⟨⟨hadj, Or.inr h⟩, CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_left x y),
          CactusBlock.mem_verts_of_mem_edges h (Sym2.mem_mk_right x y)⟩
  refine ⟨fun e he f hf => ?_, fun e he f hf => ?_, fun e he f hf => ?_⟩
  · have heA : ∀ x ∈ e, x ∈ A := fun x hx => hLA x (mem_listVerts_of_mem_listEdges he hx)
    have hfA : ∀ x ∈ f, x ∈ A := fun x hx => hLA x (mem_listVerts_of_mem_listEdges hf hx)
    rw [blockRestrict_thm N hS V _ J A B.verts v hAB hAB' hedge e f heA hfA]
    exact gibbsCov_congr_edges _ _ hset1 J _ _
  · have heB : ∀ x ∈ e, x ∈ B.verts := fun x hx => CactusBlock.mem_verts_of_mem_edges he hx
    have hfB : ∀ x ∈ f, x ∈ B.verts := fun x hx => CactusBlock.mem_verts_of_mem_edges hf hx
    have hBA : B.verts ∪ A = Set.univ := by
      rw [Set.union_comm]
      exact hAB
    have hBA' : B.verts ∩ A = {v} := by
      rw [Set.inter_comm]
      exact hAB'
    rw [blockRestrict_thm N hS V _ J B.verts A v hBA hBA' (fun x y h => (hedge x y h).symm) e f heB hfB]
    exact gibbsCov_congr_edges _ _ hset2 J _ _
  · have heA : ∀ x ∈ e, x ∈ A := fun x hx => hLA x (mem_listVerts_of_mem_listEdges he hx)
    have hfB : ∀ x ∈ f, x ∈ B.verts := fun x hx => CactusBlock.mem_verts_of_mem_edges hf hx
    have heG : e ∈ (edgeRestrict G (listEdges (L' ++ [B]))).edgeSet :=
      (mem_edgeRestrict_edgeSet _ _ e).mpr ⟨listEdges_sub hval' he, (mem_listEdges_append L' B e).mpr (Or.inl he)⟩
    have hfG : f ∈ (edgeRestrict G (listEdges (L' ++ [B]))).edgeSet :=
      (mem_edgeRestrict_edgeSet _ _ f).mpr
        ⟨CactusBlock.edges_sub_edgeSet hB hf, (mem_listEdges_append L' B f).mpr (Or.inr hf)⟩
    exact blocks_thm N hS V _ J A B.verts v hAB hAB' hedge e heG f hfG heA hfB

/-! ### The induction along the list -/

theorem cactus_invariant {N : ℕ} (hS : hSphereIso N) {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    (J : Sym2 V → ℝ) (L : List (CactusBlock V)) :
    (∀ B ∈ L, B.IsBlockOf G) →
    (∀ (L₁ L₂ : List (CactusBlock V)) (B : CactusBlock V), L = L₁ ++ B :: L₂ →
      ∀ x y, x ∈ B.verts → y ∈ B.verts → (∃ B' ∈ L₁, x ∈ B'.verts) → (∃ B' ∈ L₁, y ∈ B'.verts) → x = y) →
    (∀ B₀ ∈ L, ∀ e ∈ B₀.edges, ∀ f ∈ B₀.edges,
      gibbsCov N (edgeRestrict G (listEdges L)) J (bond e) (bond f)
        = gibbsCov N (edgeRestrict G B₀.edges) J (bond e) (bond f)) ∧
    (∀ e ∈ listEdges L, ∀ f ∈ listEdges L, (¬ ∃ B₀ ∈ L, e ∈ B₀.edges ∧ f ∈ B₀.edges) →
      gibbsCov N (edgeRestrict G (listEdges L)) J (bond e) (bond f) = 0) := by
  induction L using List.reverseRecOn with
  | nil =>
    intro _ _
    refine ⟨fun B₀ hB₀ => ?_, fun e he => ?_⟩
    · simp at hB₀
    · obtain ⟨B₀, hB₀, -⟩ := he
      simp at hB₀
  | append_singleton L' B ih =>
    intro hval hatt
    have hval' : ∀ B'' ∈ L', B''.IsBlockOf G := fun B'' h => hval B'' (List.mem_append.mpr (Or.inl h))
    have hB : B.IsBlockOf G := hval B (List.mem_append.mpr (Or.inr (List.mem_singleton.mpr rfl)))
    have hatt' : ∀ (L₁ L₂ : List (CactusBlock V)) (B' : CactusBlock V), L' = L₁ ++ B' :: L₂ →
        ∀ x y, x ∈ B'.verts → y ∈ B'.verts → (∃ B'' ∈ L₁, x ∈ B''.verts) → (∃ B'' ∈ L₁, y ∈ B''.verts) →
          x = y := by
      intro L₁ L₂ B' h
      exact hatt L₁ (L₂ ++ [B]) B' (by rw [h]; simp)
    have hlast : ∀ x y, x ∈ B.verts → y ∈ B.verts → x ∈ listVerts L' → y ∈ listVerts L' → x = y :=
      fun x y hx hy hxL hyL => hatt L' [] B rfl x y hx hy hxL hyL
    obtain ⟨ihA, ihB⟩ := ih hval' hatt'
    obtain ⟨s1, s2, s3⟩ := peel_step hS G J L' B hval' hB hlast
    refine ⟨?_, ?_⟩
    · intro B₀ hB₀ e he f hf
      by_cases hB₀L : B₀ ∈ L'
      · rw [s1 e ⟨B₀, hB₀L, he⟩ f ⟨B₀, hB₀L, hf⟩]
        exact ihA B₀ hB₀L e he f hf
      · have hBB : B₀ = B := by
          rcases List.mem_append.mp hB₀ with h | h
          · exact absurd h hB₀L
          · exact List.mem_singleton.mp h
        rw [hBB] at he hf ⊢
        exact s2 e he f hf
    · intro e he f hf hnot
      by_cases heL : e ∈ listEdges L'
      · by_cases hfL : f ∈ listEdges L'
        · rw [s1 e heL f hfL]
          apply ihB e heL f hfL
          rintro ⟨B₀, hB₀, he₀, hf₀⟩
          exact hnot ⟨B₀, List.mem_append.mpr (Or.inl hB₀), he₀, hf₀⟩
        · have hfB : f ∈ B.edges := ((mem_listEdges_append L' B f).mp hf).resolve_left hfL
          exact s3 e heL f hfB
      · have heB : e ∈ B.edges := ((mem_listEdges_append L' B e).mp he).resolve_left heL
        by_cases hfL : f ∈ listEdges L'
        · rw [gibbsCov_comm]
          exact s3 f hfL e heB
        · have hfB : f ∈ B.edges := ((mem_listEdges_append L' B f).mp hf).resolve_left hfL
          exact absurd ⟨B, List.mem_append.mpr (Or.inr (List.mem_singleton.mpr rfl)), heB, hfB⟩ hnot

/-! ### Theorem 1.1 on cacti -/

theorem cactus_cov_eq_list {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (L : List (CactusBlock V)) (hcov : ∀ e ∈ G.edgeSet, ∃ B ∈ L, e ∈ B.edges)
    (J : Sym2 V → ℝ) (F F' : Config N V → ℝ) :
    gibbsCov N G J F F' = gibbsCov N (edgeRestrict G (listEdges L)) J F F' := by
  apply gibbsCov_congr_edges
  ext g
  induction g using Sym2.ind with
  | h x y =>
    rw [SimpleGraph.mem_edgeSet, SimpleGraph.mem_edgeSet, edgeRestrict_adj]
    constructor
    · intro h
      exact ⟨h, hcov s(x, y) h⟩
    · intro h
      exact h.1

theorem cycleBlock_edgeSet {V : Type} (G : SimpleGraph V) {n : ℕ} (φ : Fin n → V)
    (hB : (CactusBlock.cycle n φ).IsBlockOf G) :
    (edgeRestrict G (CactusBlock.cycle n φ).edges).edgeSet = Sym2.map φ '' (SimpleGraph.cycleGraph n).edgeSet := by
  ext g
  rw [mem_edgeRestrict_edgeSet]
  constructor
  · rintro ⟨-, h⟩
    exact h
  · intro h
    exact ⟨CactusBlock.edges_sub_edgeSet hB h, h⟩

theorem block_cov_nonneg {N : ℕ} (hN : 0 < N) {k : ℕ → ℝ → ℝ} {d : ℕ → ℝ} {C : ℕ → ℝ → ℝ}
    (hFH : hFH N k d C) (hK : hKReg k) (hR : hRatio k) (hCZ : hCycleZ N k d) {V : Type} [Fintype V]
    [DecidableEq V] (G : SimpleGraph V) (J : Sym2 V → ℝ) (hJ : ∀ e ∈ G.edgeSet, 0 ≤ J e) (B : CactusBlock V)
    (hB : B.IsBlockOf G) {e f : Sym2 V} (he : e ∈ B.edges) (hf : f ∈ B.edges) (hef : e ≠ f) :
    0 ≤ gibbsCov N (edgeRestrict G B.edges) J (bond e) (bond f) := by
  cases B with
  | edge e₀ =>
    have h1 : e = e₀ := he
    have h2 : f = e₀ := hf
    exact absurd (h1.trans h2.symm) hef
  | cycle n φ =>
    classical
    have hB' := hB
    obtain ⟨hn, hφ, -⟩ := hB'
    obtain ⟨a, ha, rfl⟩ := he
    obtain ⟨b, hb, rfl⟩ := hf
    have hab : a ≠ b := fun h => hef (by rw [h])
    rw [gibbsCov_transport hN φ hφ _ (cycleBlock_edgeSet G φ hB) J a b]
    have hferro : Ferro (SimpleGraph.cycleGraph n) (J ∘ Sym2.map φ) := fun g hg =>
      hJ _ (CactusBlock.edges_sub_edgeSet hB ⟨g, hg, rfl⟩)
    exact cycleG2_thm N k d C hFH hK hR hCZ n hn (J ∘ Sym2.map φ) hferro a ha b hb hab

theorem block_cov_pos {N : ℕ} (hN : 0 < N) {k : ℕ → ℝ → ℝ} {d : ℕ → ℝ} {C : ℕ → ℝ → ℝ}
    (hFH : hFH N k d C) (hK : hKReg k) (hR : hRatio k) (hCZ : hCycleZ N k d) (hd : ∀ c, 0 < d c)
    {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V) (J : Sym2 V → ℝ) {n : ℕ} (φ : Fin n → V)
    (hB : (CactusBlock.cycle n φ).IsBlockOf G) (hJpos : ∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g)
    {e f : Sym2 V} (he : e ∈ (CactusBlock.cycle n φ).edges) (hf : f ∈ (CactusBlock.cycle n φ).edges)
    (hef : e ≠ f) :
    0 < gibbsCov N (edgeRestrict G (CactusBlock.cycle n φ).edges) J (bond e) (bond f) := by
  classical
  have hB' := hB
  obtain ⟨hn, hφ, -⟩ := hB'
  obtain ⟨a, ha, rfl⟩ := he
  obtain ⟨b, hb, rfl⟩ := hf
  have hab : a ≠ b := fun h => hef (by rw [h])
  rw [gibbsCov_transport hN φ hφ _ (cycleBlock_edgeSet G φ hB) J a b]
  exact cycleG2_strict_thm N k d C hFH hK hR hCZ hd n hn (J ∘ Sym2.map φ) (fun g hg => hJpos _ ⟨g, hg, rfl⟩)
    a ha b hb hab

theorem cactus_thm (N : ℕ) : cactus_statement N := by
  unfold cactus_statement
  intro hS k d C hFH hK hR hCZ V _ _ G _ hcac J hJ e he f hf hef
  obtain ⟨L, hval, hcov, hatt⟩ := hcac
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · have hV : Nonempty V := by
      induction e using Sym2.ind with
      | h x y => exact ⟨x⟩
    have h0 : freeMeasure 0 V = 0 := freeMeasure_zero V
    simp [G2pair, gibbsCov, gibbsExp, partition, h0]
  unfold G2pair
  rw [cactus_cov_eq_list G L hcov J]
  obtain ⟨hA, hB⟩ := cactus_invariant hS G J L hval hatt
  by_cases hcom : ∃ B₀ ∈ L, e ∈ B₀.edges ∧ f ∈ B₀.edges
  · obtain ⟨B₀, hB₀, he₀, hf₀⟩ := hcom
    rw [hA B₀ hB₀ e he₀ f hf₀]
    exact block_cov_nonneg hN hFH hK hR hCZ G J hJ B₀ (hval B₀ hB₀) he₀ hf₀ hef
  · exact le_of_eq (hB e (hcov e he) f (hcov f hf) hcom).symm

theorem cactus_strict_thm (N : ℕ) : cactus_strict_statement N := by
  unfold cactus_strict_statement
  intro hS k d C hFH hK hR hCZ hd V _ _ G _ L hcac J _hJ n φ hmem hJpos e he f hf hef
  obtain ⟨hval, hcov, hatt⟩ := hcac
  have hB := hval _ hmem
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · exfalso
    classical
    obtain ⟨hn, -, -⟩ := hB
    obtain ⟨a, ha, rfl⟩ := he
    obtain ⟨b, hb, rfl⟩ := hf
    have hab : a ≠ b := fun h => hef (by rw [h])
    have hpos := cycleG2_strict_thm 0 k d C hFH hK hR hCZ hd n hn (J ∘ Sym2.map φ)
      (fun g hg => hJpos _ ⟨g, hg, rfl⟩) a ha b hb hab
    have hV : Nonempty (Fin n) := ⟨⟨0, by omega⟩⟩
    have h0 : freeMeasure 0 (Fin n) = 0 := freeMeasure_zero (Fin n)
    simp [gibbsCov, gibbsExp, partition, h0] at hpos
  rw [cactus_cov_eq_list G L hcov J]
  obtain ⟨hA, -⟩ := cactus_invariant hS G J L hval hatt
  rw [hA _ hmem e he f hf]
  exact block_cov_pos hN hFH hK hR hCZ hd G J φ hB hJpos he hf hef

end G2Kernel
