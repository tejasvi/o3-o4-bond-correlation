/-
G2S3.GramElim (stage S3, Part C2): vertex elimination (STATEMENTS_S3_v5.md, C2). For a kernel F of positive type
(∫∫ F(s,t) (s.t)^k ≥ 0 for every k) and every Gram word L, ∫ F(σ_x, σ_y) gw_L(σ) ≥ 0: integrate out the vertices other than
x, y one at a time; at a vertex v the word splits into a part away from v and a product of linear forms in σ_v, whose sphere
integral (V1) is a nonnegative combination of Gram words in the partners of v. At the end the word is (σ_x.σ_y)^k.
Π_c is of positive type: t^k = k! Σ_e c'(e,k) Π_e(t) with c' ≥ 0 (S1's `pow_eq_sum_zon`, `cK_nonneg`) and display (2).
-/
import G2S3.GramPol
import G2S3.RPEnergy
import G2S1.Zonal

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

section Elim

variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]

instance uniqueNotNe (v : V) : Unique {i : V // ¬ i ≠ v} where
  default := ⟨v, not_not.mpr rfl⟩
  uniq := fun ⟨_, h⟩ => Subtype.ext (not_not.mp h)

theorem joinAt_update (v : V) (σ' : {i // i ≠ v} → Sph N) (τ : {i // ¬ i ≠ v} → Sph N) (z : Sph N) :
    Function.update (joinAt v σ' τ) v z = joinAt v σ' (fun _ => z) := by
  funext i
  by_cases h : i = v
  · subst h
    rw [Function.update_self, joinAt_self]
  · rw [Function.update_of_ne h, joinAt_of_ne σ' τ h, joinAt_of_ne σ' _ h]

/-- **Fubini at one vertex** -/
theorem integral_update (hN : 0 < N) (v : V) (g : Config N V → ℝ) (hg : BddMeas g) :
    ∫ σ, g σ ∂(freeMeasure N V) = ∫ σ, (∫ z, g (Function.update σ v z) ∂(omega N)) ∂(freeMeasure N V) := by
  have hprob := omega_isProbabilityMeasure N hN
  obtain ⟨hgm, C, hC⟩ := hg
  have hm2 : Measurable (fun p : Config N V × Sph N => g (Function.update p.1 v p.2)) :=
    hgm.comp measurable_update'
  set ψ : Config N V → ℝ := fun σ => ∫ z, g (Function.update σ v z) ∂(omega N) with hψ
  have hψm : Measurable ψ := (hm2.stronglyMeasurable.integral_prod_right' (ν := omega N)).measurable
  have hψC : ∀ σ, |ψ σ| ≤ C := by
    intro σ
    have h := norm_integral_le_of_norm_le_const (μ := omega N) (C := C)
      (f := fun z => g (Function.update σ v z))
      (Filter.Eventually.of_forall (fun z => by rw [Real.norm_eq_abs]; exact hC _))
    rw [Real.norm_eq_abs] at h
    simpa using h
  rw [integral_split_at hN v g hgm C hC, integral_split_at hN v ψ hψm C hψC]
  congr 1
  funext σ'
  have hR : ∀ τ : {i // ¬ i ≠ v} → Sph N, ψ (joinAt v σ' τ) = ∫ z, g (joinAt v σ' (fun _ => z)) ∂(omega N) := by
    intro τ
    simp only [hψ, joinAt_update]
  simp only [hR]
  rw [integral_const]
  simp only [probReal_univ, one_smul]
  have hmp := measurePreserving_funUnique (omega N) {i : V // ¬ i ≠ v}
  have hsymm : ∀ z : Sph N, (MeasurableEquiv.funUnique {i : V // ¬ i ≠ v} (Sph N)).symm z = fun _ => z := by
    intro z
    funext i
    rw [Subsingleton.elim i default]
    exact (MeasurableEquiv.funUnique {i : V // ¬ i ≠ v} (Sph N)).apply_symm_apply z
  have h := hmp.symm.integral_comp' (g := fun τ => g (joinAt v σ' τ))
  simp only [hsymm] at h
  convert h.symm

/-- **The law of two spins** -/
theorem integral_two (hN : 0 < N) {x y : V} (hxy : x ≠ y) (φ : Sph N → Sph N → ℝ)
    (hφ : BddMeas (fun p : Sph N × Sph N => φ p.1 p.2)) :
    ∫ σ, φ (σ x) (σ y) ∂(freeMeasure N V) = ∫ s, ∫ t, φ s t ∂(omega N) ∂(omega N) := by
  have hprob := omega_isProbabilityMeasure N hN
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  obtain ⟨hφm, C, hC⟩ := hφ
  have hm1 := hφm.comp ((measurable_pi_apply (X := fun _ : V => Sph N) x).prodMk (measurable_pi_apply y))
  have hg1 : BddMeas (fun σ : Config N V => φ (σ x) (σ y)) := ⟨hm1, C, fun σ => hC (σ x, σ y)⟩
  rw [integral_update hN y _ hg1]
  have e1 : ∀ σ : Config N V, ∫ t, φ ((Function.update σ y t) x) ((Function.update σ y t) y) ∂(omega N)
      = ∫ t, φ (σ x) t ∂(omega N) := by
    intro σ
    congr 1
    funext t
    rw [Function.update_of_ne hxy, Function.update_self]
  simp only [e1]
  set ψ : Sph N → ℝ := fun s => ∫ t, φ s t ∂(omega N) with hψ
  have hψm : Measurable ψ := (hφm.stronglyMeasurable.integral_prod_right' (ν := omega N)).measurable
  have hψC : ∀ s, |ψ s| ≤ C := by
    intro s
    have h := norm_integral_le_of_norm_le_const (μ := omega N) (C := C) (f := fun t => φ s t)
      (Filter.Eventually.of_forall (fun t => by rw [Real.norm_eq_abs]; exact hC (s, t)))
    rw [Real.norm_eq_abs] at h
    simpa using h
  have hg2 : BddMeas (fun σ : Config N V => ψ (σ x)) := ⟨hψm.comp (measurable_pi_apply x), C, fun σ => hψC _⟩
  show ∫ σ, ψ (σ x) ∂(freeMeasure N V) = ∫ s, ψ s ∂(omega N)
  rw [integral_update hN x _ hg2]
  simp only [Function.update_self]
  rw [integral_const]
  simp only [probReal_univ, one_smul]

/-- a Gram word: the product of the scalar products of the listed pairs -/
def gw (L : List (V × V)) (σ : Config N V) : ℝ := (L.map fun q => dot (σ q.1) (σ q.2)).prod

theorem gw_cons (q : V × V) (L : List (V × V)) (σ : Config N V) :
    gw (q :: L) σ = dot (σ q.1) (σ q.2) * gw L σ := by
  simp [gw]

theorem gw_append (L L' : List (V × V)) (σ : Config N V) : gw (L ++ L') σ = gw L σ * gw L' σ := by
  simp [gw, List.map_append, List.prod_append]

theorem gw_ofFn {m : ℕ} (f : Fin m → V × V) (σ : Config N V) :
    gw (List.ofFn f) σ = ∏ k, dot (σ (f k).1) (σ (f k).2) := by
  unfold gw
  rw [List.map_ofFn, List.prod_ofFn]
  rfl

theorem abs_gw_le (L : List (V × V)) (σ : Config N V) : |gw L σ| ≤ 1 := by
  induction L with
  | nil => simp [gw]
  | cons q L ih =>
    rw [gw_cons, abs_mul]
    exact mul_le_one₀ (abs_dot_le _ _) (abs_nonneg _) ih

theorem measurable_gw (L : List (V × V)) : Measurable (gw (N := N) L) := by
  induction L with
  | nil => exact measurable_const
  | cons q L ih =>
    have e : gw (N := N) (q :: L) = fun σ => dot (σ q.1) (σ q.2) * gw L σ := funext (gw_cons q L)
    rw [e]
    exact (measurable_bond (N := N) s(q.1, q.2)).mul ih

theorem gw_bdd (L : List (V × V)) : BddMeas (gw (N := N) L) := ⟨measurable_gw L, 1, abs_gw_le L⟩

/-- the pairs of L away from v -/
def restW (v : V) (L : List (V × V)) : List (V × V) := L.filter fun q => !(q.1 == v) && !(q.2 == v)

/-- the partners of v in L -/
def partW (v : V) (L : List (V × V)) : List V :=
  L.filterMap fun q => if q.1 = v then (if q.2 = v then none else some q.2) else if q.2 = v then some q.1 else none

theorem gw_update (v : V) (L : List (V × V)) (σ : Config N V) (z : Sph N) :
    gw L (Function.update σ v z) = gw (restW v L) σ * ((partW v L).map fun u => dot (σ u) z).prod := by
  induction L with
  | nil => simp [gw, restW, partW]
  | cons q L ih =>
    obtain ⟨a, b⟩ := q
    rw [gw_cons]
    by_cases ha : a = v
    · by_cases hb : b = v
      · have hrest : restW v ((a, b) :: L) = restW v L := by simp [restW, ha]
        have hpart : partW v ((a, b) :: L) = partW v L := by simp [partW, ha, hb]
        rw [hrest, hpart, ← ih]
        simp only [ha, hb, Function.update_self]
        rw [dot_self, one_mul]
      · have hrest : restW v ((a, b) :: L) = restW v L := by simp [restW, ha]
        have hpart : partW v ((a, b) :: L) = b :: partW v L := by simp [partW, ha, hb]
        rw [hrest, hpart, List.map_cons, List.prod_cons, ih]
        simp only [ha, Function.update_self, Function.update_of_ne hb]
        rw [dot_comm z (σ b)]
        ring
    · by_cases hb : b = v
      · have hrest : restW v ((a, b) :: L) = restW v L := by simp [restW, hb]
        have hpart : partW v ((a, b) :: L) = a :: partW v L := by simp [partW, ha, hb]
        rw [hrest, hpart, List.map_cons, List.prod_cons, ih]
        simp only [hb, Function.update_self, Function.update_of_ne ha]
        ring
      · have hrest : restW v ((a, b) :: L) = (a, b) :: restW v L := by simp [restW, ha, hb]
        have hpart : partW v ((a, b) :: L) = partW v L := by simp [partW, ha, hb]
        rw [hrest, hpart, gw_cons, ih]
        simp only [Function.update_of_ne ha, Function.update_of_ne hb]
        ring

theorem mem_restW {v : V} {L : List (V × V)} {q : V × V} (h : q ∈ restW v L) : q ∈ L ∧ q.1 ≠ v ∧ q.2 ≠ v := by
  unfold restW at h
  rw [List.mem_filter] at h
  obtain ⟨h1, h2⟩ := h
  simp only [Bool.and_eq_true, Bool.not_eq_true', beq_eq_false_iff_ne] at h2
  exact ⟨h1, h2.1, h2.2⟩

theorem mem_partW {v : V} {L : List (V × V)} {u : V} (h : u ∈ partW v L) :
    u ≠ v ∧ ∃ q ∈ L, u = q.1 ∨ u = q.2 := by
  unfold partW at h
  rw [List.mem_filterMap] at h
  obtain ⟨⟨a, b⟩, hq, hf⟩ := h
  simp only at hf
  by_cases ha : a = v
  · by_cases hb : b = v
    · simp [ha, hb] at hf
    · simp only [ha, hb, if_true, if_false, Option.some.injEq] at hf
      exact ⟨hf ▸ hb, ⟨(a, b), hq, Or.inr hf.symm⟩⟩
  · by_cases hb : b = v
    · simp only [ha, hb, if_true, if_false, Option.some.injEq] at hf
      exact ⟨hf ▸ ha, ⟨(a, b), hq, Or.inl hf.symm⟩⟩
    · simp [ha, hb] at hf

/-- a word on {x, y} is a power of σ_x . σ_y -/
theorem gw_two {x y : V} (L : List (V × V)) (hL : ∀ q ∈ L, (q.1 = x ∨ q.1 = y) ∧ (q.2 = x ∨ q.2 = y)) :
    ∃ k : ℕ, ∀ σ : Config N V, gw L σ = dot (σ x) (σ y) ^ k := by
  induction L with
  | nil => exact ⟨0, fun σ => by simp [gw]⟩
  | cons q L ih =>
    obtain ⟨k, hk⟩ := ih (fun q' hq' => hL q' (List.mem_cons_of_mem _ hq'))
    obtain ⟨h1, h2⟩ := hL q List.mem_cons_self
    obtain ⟨a, b⟩ := q
    simp only at h1 h2
    rcases h1 with h1 | h1 <;> rcases h2 with h2 | h2
    · exact ⟨k, fun σ => by rw [gw_cons, hk]; simp only [h1, h2, dot_self, one_mul]⟩
    · exact ⟨k + 1, fun σ => by rw [gw_cons, hk]; simp only [h1, h2]; ring⟩
    · exact ⟨k + 1, fun σ => by rw [gw_cons, hk]; simp only [h1, h2]; rw [dot_comm (σ y) (σ x)]; ring⟩
    · exact ⟨k, fun σ => by rw [gw_cons, hk]; simp only [h1, h2, dot_self, one_mul]⟩

/-- a kernel of positive type -/
def PosType (F : Sph N → Sph N → ℝ) : Prop :=
  ∀ k : ℕ, 0 ≤ ∫ s, ∫ t, F s t * dot s t ^ k ∂(omega N) ∂(omega N)

/-- **Vertex elimination** -/
theorem gram_pos (hN : 1 ≤ N) {x y : V} (hxy : x ≠ y) {F : Sph N → Sph N → ℝ}
    (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2)) (hpos : PosType F) (L : List (V × V)) :
    0 ≤ ∫ σ, F (σ x) (σ y) * gw L σ ∂(freeMeasure N V) := by
  have hN0 : 0 < N := by omega
  have hprob := omega_isProbabilityMeasure N hN0
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  obtain ⟨hFm, C, hC⟩ := hF
  have hFxy0 := hFm.comp ((measurable_pi_apply (X := fun _ : V => Sph N) x).prodMk (measurable_pi_apply y))
  have hFxy : Measurable (fun σ : Config N V => F (σ x) (σ y)) := hFxy0
  have hbdd : ∀ L' : List (V × V), BddMeas (fun σ : Config N V => F (σ x) (σ y) * gw L' σ) := fun L' =>
    BddMeas.mul ⟨hFxy, C, fun σ => hC (σ x, σ y)⟩ (gw_bdd L')
  suffices H : ∀ S : Finset V, ∀ L : List (V × V),
      (∀ q ∈ L, (q.1 = x ∨ q.1 = y ∨ q.1 ∈ S) ∧ (q.2 = x ∨ q.2 = y ∨ q.2 ∈ S)) →
      0 ≤ ∫ σ, F (σ x) (σ y) * gw L σ ∂(freeMeasure N V) by
    exact H Finset.univ L (fun q _ => ⟨Or.inr (Or.inr (Finset.mem_univ _)), Or.inr (Or.inr (Finset.mem_univ _))⟩)
  intro S
  induction S using Finset.induction_on with
  | empty =>
    intro L hL
    obtain ⟨k, hk⟩ := gw_two (N := N) (x := x) (y := y) L (fun q hq => by
      obtain ⟨h1, h2⟩ := hL q hq
      simp only [Finset.notMem_empty, or_false] at h1 h2
      exact ⟨h1, h2⟩)
    simp only [hk]
    have hdm : Measurable (fun p : Sph N × Sph N => dot p.1 p.2) :=
      ((continuous_subtype_val.comp continuous_fst).inner (continuous_subtype_val.comp continuous_snd)).measurable
    have hb2 : BddMeas (fun p : Sph N × Sph N => F p.1 p.2 * dot p.1 p.2 ^ k) :=
      BddMeas.mul ⟨hFm, C, hC⟩ ⟨hdm.pow_const k, 1, fun p => by
        rw [abs_pow]; exact pow_le_one₀ (abs_nonneg _) (abs_dot_le _ _)⟩
    rw [integral_two hN0 hxy (fun s t => F s t * dot s t ^ k) hb2]
    exact hpos k
  | insert v S hvS ih =>
    intro L hL
    by_cases hvx : v = x
    · refine ih L (fun q hq => ?_)
      obtain ⟨h1, h2⟩ := hL q hq
      simp only [Finset.mem_insert] at h1 h2
      constructor
      · rcases h1 with h | h | h | h
        · exact Or.inl h
        · exact Or.inr (Or.inl h)
        · exact Or.inl (h.trans hvx)
        · exact Or.inr (Or.inr h)
      · rcases h2 with h | h | h | h
        · exact Or.inl h
        · exact Or.inr (Or.inl h)
        · exact Or.inl (h.trans hvx)
        · exact Or.inr (Or.inr h)
    by_cases hvy : v = y
    · refine ih L (fun q hq => ?_)
      obtain ⟨h1, h2⟩ := hL q hq
      simp only [Finset.mem_insert] at h1 h2
      constructor
      · rcases h1 with h | h | h | h
        · exact Or.inl h
        · exact Or.inr (Or.inl h)
        · exact Or.inr (Or.inl (h.trans hvy))
        · exact Or.inr (Or.inr h)
      · rcases h2 with h | h | h | h
        · exact Or.inl h
        · exact Or.inr (Or.inl h)
        · exact Or.inr (Or.inl (h.trans hvy))
        · exact Or.inr (Or.inr h)
    -- eliminate the spin at v
    have hxv : x ≠ v := fun h => hvx h.symm
    have hyv : y ≠ v := fun h => hvy h.symm
    set U := partW v L with hU
    set D := U.length with hD
    set W : (Fin (D / 2) → Fin D × Fin D) → List (V × V) :=
      fun p => List.ofFn (fun k => (U[((p k).1 : ℕ)], U[((p k).2 : ℕ)])) with hW
    have step : ∀ σ : Config N V, ∫ z, F ((Function.update σ v z) x) ((Function.update σ v z) y) *
        gw L (Function.update σ v z) ∂(omega N)
          = ∑ p : Fin (D / 2) → Fin D × Fin D, polC N D p * (F (σ x) (σ y) * gw (restW v L ++ W p) σ) := by
      intro σ
      simp only [Function.update_of_ne hxv, Function.update_of_ne hyv, gw_update]
      have e1 : (fun z : Sph N => F (σ x) (σ y) * (gw (restW v L) σ * (U.map fun u => dot (σ u) z).prod))
          = fun z : Sph N => (F (σ x) (σ y) * gw (restW v L) σ) *
              ∏ l : Fin D, @inner ℝ (Amb N) _ ((σ U[(l : ℕ)] : Sph N) : Amb N) (z : Amb N) := by
        funext z
        rw [← Fin.prod_univ_fun_getElem U (fun u => dot (σ u) z), ← mul_assoc]
        rfl
      rw [e1, integral_const_mul, sphere_prod_inner hN D, Finset.mul_sum]
      refine Finset.sum_congr rfl (fun p _ => ?_)
      rw [gw_append, hW, gw_ofFn]
      simp only [dot]
      ring
    rw [integral_update hN0 v _ (hbdd L)]
    simp only [step]
    rw [integral_finsetSum _ (fun p _ => ((hbdd _).integrable).const_mul _)]
    refine Finset.sum_nonneg (fun p _ => ?_)
    rw [integral_const_mul]
    refine mul_nonneg (polC_nonneg hN D p) (ih _ (fun q hq => ?_))
    rcases List.mem_append.mp hq with hq | hq
    · obtain ⟨hqL, hq1, hq2⟩ := mem_restW hq
      obtain ⟨h1, h2⟩ := hL q hqL
      simp only [Finset.mem_insert] at h1 h2
      constructor
      · rcases h1 with h | h | h | h
        · exact Or.inl h
        · exact Or.inr (Or.inl h)
        · exact absurd h hq1
        · exact Or.inr (Or.inr h)
      · rcases h2 with h | h | h | h
        · exact Or.inl h
        · exact Or.inr (Or.inl h)
        · exact absurd h hq2
        · exact Or.inr (Or.inr h)
    · rw [hW, List.mem_ofFn] at hq
      obtain ⟨k, hk⟩ := hq
      have hmemU : ∀ i : Fin D, U[(i : ℕ)] = x ∨ U[(i : ℕ)] = y ∨ U[(i : ℕ)] ∈ S := by
        intro i
        have hm : U[(i : ℕ)] ∈ partW v L := List.getElem_mem _
        obtain ⟨hne, q', hq', hu⟩ := mem_partW hm
        obtain ⟨h1, h2⟩ := hL q' hq'
        simp only [Finset.mem_insert] at h1 h2
        rcases hu with hu | hu
        · rw [hu]
          rcases h1 with h | h | h | h
          · exact Or.inl h
          · exact Or.inr (Or.inl h)
          · exact absurd (hu.trans h) hne
          · exact Or.inr (Or.inr h)
        · rw [hu]
          rcases h2 with h | h | h | h
          · exact Or.inl h
          · exact Or.inr (Or.inl h)
          · exact absurd (hu.trans h) hne
          · exact Or.inr (Or.inr h)
      rw [← hk]
      exact ⟨hmemU (p k).1, hmemU (p k).2⟩

end Elim

/-- **Π_c is of positive type** -/
theorem zonal_posType {N : ℕ} (hN : 2 ≤ N) (c : ℕ) : PosType (zonal N c) := by
  intro k
  have hprob := omega_isProbabilityMeasure N (by omega)
  have hin : ∀ s : Sph N, ∫ t, zonal N c s t * dot s t ^ k ∂(omega N)
      = (k.factorial : ℝ) * ∑ e ∈ Finset.range (k + 1), cK N e k * (if c = e then dConc N c else 0) := by
    intro s
    have hexp : ∀ t : Sph N, zonal N c s t * dot s t ^ k
        = (k.factorial : ℝ) * ∑ e ∈ Finset.range (k + 1), cK N e k * (zonal N c s t * zonal N e t s) := by
      intro t
      rw [pow_eq_sum_zon hN k (dot s t), Finset.mul_sum, Finset.mul_sum, Finset.mul_sum]
      refine Finset.sum_congr rfl (fun e _ => ?_)
      rw [zonal_symm N e t s, zonal_eq_zon N e s t]
      ring
    simp only [hexp]
    rw [integral_const_mul, integral_finsetSum (Finset.range (k + 1))
      (f := fun e z => cK N e k * (zonal N c s z * zonal N e z s)) (fun e _ =>
      (integrable_zonal_mul hN c e id id continuous_id continuous_id s s).const_mul (cK N e k))]
    congr 1
    refine Finset.sum_congr rfl (fun e _ => ?_)
    rw [integral_const_mul]
    rw [zonal_proj hN c e s s]
    split_ifs with hce
    · rw [zonal_self hN c s]
    · rfl
  simp only [hin]
  rw [integral_const]
  simp only [probReal_univ, one_smul]
  refine mul_nonneg (by positivity) (Finset.sum_nonneg (fun e _ => mul_nonneg (cK_nonneg hN e k) ?_))
  split_ifs
  · exact (dConc_pos_S1 hN c).le
  · exact le_refl 0

end G2S3

#print axioms G2S3.integral_update
#print axioms G2S3.integral_two
#print axioms G2S3.gw_update
#print axioms G2S3.gram_pos
#print axioms G2S3.zonal_posType
