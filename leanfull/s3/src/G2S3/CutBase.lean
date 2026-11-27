/-
G2S3.CutBase (stage S3, Part E3): the four-terminal integrals (STATEMENTS_S3_v8.md, E3). For a word on {x, y, z, w} whose pairs
never cross the cut (x, z ∈ A; y, w ∉ A), gw = (σ_x.σ_z)^p (σ_y.σ_w)^q. Expanding (σ_y.σ_w)^q in zonal functions
(S1's `pow_eq_sum_zon`) and integrating out σ_y and then σ_w with display (2) (`zonal_proj`) leaves zero unless the two labels
agree, and otherwise a nonnegative multiple of ∫ Π_c(σ_x, σ_z) (σ_x.σ_z)^p ≥ 0 (`zonal_posType`). The cases x = z and y = w
are similar.
-/
import G2S3.GramSide

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

section Base

variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]

theorem zonal_pair_bdd (hN : 2 ≤ N) (c : ℕ) (a b : V) : BddMeas (fun σ : Config N V => zonal N c (σ a) (σ b)) := by
  have h0 := ((continuous_zonal N c).measurable).comp
    ((measurable_pi_apply (X := fun _ : V => Sph N) a).prodMk (measurable_pi_apply b))
  exact ⟨h0, dConc N c, fun σ => abs_zonal_le hN c _ _⟩

theorem dot_pow_bdd (a b : V) (p : ℕ) : BddMeas (fun σ : Config N V => dot (σ a) (σ b) ^ p) :=
  BddMeas.pow ⟨measurable_bond (N := N) s(a, b), 1, fun σ => abs_bond_le s(a, b) σ⟩ p

/-- integrating out the middle vertex of two zonal factors (display (2)) -/
theorem int_out_pair (hN : 2 ≤ N) {u a b : V} (hau : a ≠ u) (hbu : b ≠ u) (c e : ℕ) {R : Config N V → ℝ}
    (hR : BddMeas R) (hRu : ∀ (σ : Config N V) (z : Sph N), R (Function.update σ u z) = R σ) :
    ∫ σ, zonal N c (σ a) (σ u) * zonal N e (σ u) (σ b) * R σ ∂(freeMeasure N V)
      = if c = e then ∫ σ, zonal N c (σ a) (σ b) * R σ ∂(freeMeasure N V) else 0 := by
  have hN0 : 0 < N := by omega
  have hprob := omega_isProbabilityMeasure N hN0
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  have hb : BddMeas (fun σ : Config N V => zonal N c (σ a) (σ u) * zonal N e (σ u) (σ b) * R σ) :=
    BddMeas.mul (BddMeas.mul (zonal_pair_bdd hN c a u) (zonal_pair_bdd hN e u b)) hR
  rw [integral_update hN0 u _ hb]
  have hin : ∀ σ : Config N V, ∫ z, zonal N c ((Function.update σ u z) a) ((Function.update σ u z) u) *
      zonal N e ((Function.update σ u z) u) ((Function.update σ u z) b) * R (Function.update σ u z) ∂(omega N)
        = (if c = e then zonal N c (σ a) (σ b) else 0) * R σ := by
    intro σ
    simp only [Function.update_of_ne hau, Function.update_of_ne hbu, Function.update_self, hRu]
    rw [integral_mul_const, zonal_proj hN c e (σ a) (σ b)]
  simp only [hin]
  by_cases hce : c = e
  · simp only [hce, if_true]
  · simp only [hce, if_false, zero_mul, integral_zero]

/-- the positive-type integral on two distinct spins -/
theorem pos_int (hN : 2 ≤ N) {x z : V} (hxz : x ≠ z) (c p : ℕ) :
    0 ≤ ∫ σ, zonal N c (σ x) (σ z) * dot (σ x) (σ z) ^ p ∂(freeMeasure N V) := by
  have hdm : Measurable (fun q : Sph N × Sph N => dot q.1 q.2) :=
    ((continuous_subtype_val.comp continuous_fst).inner (continuous_subtype_val.comp continuous_snd)).measurable
  have hb : BddMeas (fun q : Sph N × Sph N => zonal N c q.1 q.2 * dot q.1 q.2 ^ p) :=
    BddMeas.mul ⟨(continuous_zonal N c).measurable, dConc N c, fun q => abs_zonal_le hN c q.1 q.2⟩
      ⟨hdm.pow_const p, 1, fun q => by rw [abs_pow]; exact pow_le_one₀ (abs_nonneg _) (abs_dot_le _ _)⟩
  rw [integral_two (by omega) hxz (fun s t => zonal N c s t * dot s t ^ p) hb]
  exact zonal_posType hN c p

theorem dot_two {x z a b : V} (ha : a = x ∨ a = z) (hb : b = x ∨ b = z) :
    ∃ i : ℕ, ∀ σ : Config N V, dot (σ a) (σ b) = dot (σ x) (σ z) ^ i := by
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl
  · exact ⟨0, fun σ => by rw [dot_self, pow_zero]⟩
  · exact ⟨1, fun σ => by rw [pow_one]⟩
  · exact ⟨1, fun σ => by rw [pow_one, dot_comm]⟩
  · exact ⟨0, fun σ => by rw [dot_self, pow_zero]⟩

theorem gw_side4 {x y z w : V} {A : Set V} (hxA : x ∈ A) (hyA : y ∉ A) (hzA : z ∈ A) (hwA : w ∉ A)
    (L : List (V × V))
    (hL : ∀ q ∈ L, q.1 ∈ ({x, y, z, w} : Finset V) ∧ q.2 ∈ ({x, y, z, w} : Finset V) ∧ (q.1 ∈ A ↔ q.2 ∈ A)) :
    ∃ p q : ℕ, ∀ σ : Config N V, gw L σ = dot (σ x) (σ z) ^ p * dot (σ y) (σ w) ^ q := by
  induction L with
  | nil => exact ⟨0, 0, fun σ => by simp [gw]⟩
  | cons r L ih =>
    obtain ⟨p, q, hpq⟩ := ih (fun r' hr' => hL r' (List.mem_cons_of_mem _ hr'))
    obtain ⟨h1, h2, h3⟩ := hL r List.mem_cons_self
    simp only [Finset.mem_insert, Finset.mem_singleton] at h1 h2
    by_cases hr1 : r.1 ∈ A
    · have hr2 : r.2 ∈ A := h3.mp hr1
      have ha : r.1 = x ∨ r.1 = z := by
        rcases h1 with h | h | h | h
        · exact Or.inl h
        · rw [h] at hr1; exact absurd hr1 hyA
        · exact Or.inr h
        · rw [h] at hr1; exact absurd hr1 hwA
      have hb : r.2 = x ∨ r.2 = z := by
        rcases h2 with h | h | h | h
        · exact Or.inl h
        · rw [h] at hr2; exact absurd hr2 hyA
        · exact Or.inr h
        · rw [h] at hr2; exact absurd hr2 hwA
      obtain ⟨i, hi⟩ := dot_two (N := N) ha hb
      exact ⟨p + i, q, fun σ => by rw [gw_cons, hi, hpq]; ring⟩
    · have hr2 : r.2 ∉ A := fun h => hr1 (h3.mpr h)
      have ha : r.1 = y ∨ r.1 = w := by
        rcases h1 with h | h | h | h
        · rw [h] at hr1; exact absurd hxA hr1
        · exact Or.inl h
        · rw [h] at hr1; exact absurd hzA hr1
        · exact Or.inr h
      have hb : r.2 = y ∨ r.2 = w := by
        rcases h2 with h | h | h | h
        · rw [h] at hr2; exact absurd hxA hr2
        · exact Or.inl h
        · rw [h] at hr2; exact absurd hzA hr2
        · exact Or.inr h
      obtain ⟨i, hi⟩ := dot_two (N := N) ha hb
      exact ⟨p, q + i, fun σ => by rw [gw_cons, hi, hpq]; ring⟩

/-- the general case x ≠ z, y ≠ w -/
theorem base_gen (hN : 2 ≤ N) {x y z w : V} (hxy : x ≠ y) (hxw : x ≠ w) (hzy : z ≠ y) (hzw : z ≠ w) (hxz : x ≠ z)
    (hyw : y ≠ w) (c c' p q : ℕ) :
    (c ≠ c' → ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * (dot (σ x) (σ z) ^ p * dot (σ y) (σ w) ^ q)
      ∂(freeMeasure N V) = 0) ∧
    (c = c' → 0 ≤ ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * (dot (σ x) (σ z) ^ p * dot (σ y) (σ w) ^ q)
      ∂(freeMeasure N V)) := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  set R : Config N V → ℝ := fun σ => zonal N c' (σ z) (σ w) * dot (σ x) (σ z) ^ p with hR
  have hRb : BddMeas R := BddMeas.mul (zonal_pair_bdd hN c' z w) (dot_pow_bdd x z p)
  have hRy : ∀ (σ : Config N V) (t : Sph N), R (Function.update σ y t) = R σ := by
    intro σ t
    simp only [hR, Function.update_of_ne hzy, Function.update_of_ne hxy, Function.update_of_ne (Ne.symm hyw)]
  have hexp : ∀ σ : Config N V, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) *
      (dot (σ x) (σ z) ^ p * dot (σ y) (σ w) ^ q)
        = ∑ e ∈ Finset.range (q + 1), ((q.factorial : ℝ) * cK N e q) *
            (zonal N c (σ x) (σ y) * zonal N e (σ y) (σ w) * R σ) := by
    intro σ
    rw [pow_eq_sum_zon hN q (dot (σ y) (σ w)), Finset.mul_sum, Finset.mul_sum, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun e _ => ?_)
    rw [← zonal_eq_zon N e (σ y) (σ w)]
    simp only [hR]
    ring
  have hterm : ∀ e, ∫ σ, zonal N c (σ x) (σ y) * zonal N e (σ y) (σ w) * R σ ∂(freeMeasure N V)
      = if c = e then (if c = c' then ∫ σ, zonal N c (σ x) (σ z) * dot (σ x) (σ z) ^ p ∂(freeMeasure N V) else 0)
        else 0 := by
    intro e
    rw [int_out_pair hN hxy (Ne.symm hyw) c e hRb hRy]
    by_cases hce : c = e
    · rw [if_pos hce, if_pos hce]
      have e2 : (fun σ : Config N V => zonal N c (σ x) (σ w) * R σ)
          = fun σ => zonal N c (σ x) (σ w) * zonal N c' (σ w) (σ z) * dot (σ x) (σ z) ^ p := by
        funext σ
        simp only [hR]
        rw [zonal_symm N c' (σ z) (σ w)]
        ring
      rw [e2, int_out_pair hN hxw hzw c c' (dot_pow_bdd x z p) (fun σ t => by
        simp only [Function.update_of_ne hxw, Function.update_of_ne hzw])]
    · rw [if_neg hce, if_neg hce]
  have hint : ∀ e ∈ Finset.range (q + 1), Integrable (fun σ : Config N V => ((q.factorial : ℝ) * cK N e q) *
      (zonal N c (σ x) (σ y) * zonal N e (σ y) (σ w) * R σ)) (freeMeasure N V) := fun e _ =>
    ((BddMeas.mul (BddMeas.mul (zonal_pair_bdd hN c x y) (zonal_pair_bdd hN e y w)) hRb).integrable).const_mul _
  simp only [hexp]
  rw [integral_finsetSum _ hint]
  simp only [integral_const_mul, hterm]
  constructor
  · intro hcc
    refine Finset.sum_eq_zero (fun e _ => ?_)
    by_cases hce : c = e
    · rw [if_pos hce, if_neg hcc, mul_zero]
    · rw [if_neg hce, mul_zero]
  · intro hcc
    refine Finset.sum_nonneg (fun e _ => ?_)
    have hP := pos_int hN hxz c p
    have hq0 : (0 : ℝ) ≤ (q.factorial : ℝ) * cK N e q := mul_nonneg (by positivity) (cK_nonneg hN e q)
    by_cases hce : c = e
    · rw [if_pos hce, if_pos hcc]
      exact mul_nonneg hq0 hP
    · rw [if_neg hce, mul_zero]

/-- **the four-terminal integrals** -/
theorem cut_base (hN : 2 ≤ N) {x y z w : V} {A : Set V} (hxA : x ∈ A) (hyA : y ∉ A) (hzA : z ∈ A) (hwA : w ∉ A)
    (hef : ¬ (x = z ∧ y = w)) (c c' : ℕ) (L : List (V × V))
    (hL : ∀ q ∈ L, q.1 ∈ ({x, y, z, w} : Finset V) ∧ q.2 ∈ ({x, y, z, w} : Finset V) ∧ (q.1 ∈ A ↔ q.2 ∈ A)) :
    (c ≠ c' → ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * gw L σ ∂(freeMeasure N V) = 0) ∧
    (c = c' → 0 ≤ ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * gw L σ ∂(freeMeasure N V)) := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  obtain ⟨p, q, hpq⟩ := gw_side4 (N := N) hxA hyA hzA hwA L hL
  simp only [hpq]
  have hxy : x ≠ y := fun h => hyA (h ▸ hxA)
  have hxw : x ≠ w := fun h => hwA (h ▸ hxA)
  have hzy : z ≠ y := fun h => hyA (h ▸ hzA)
  have hzw : z ≠ w := fun h => hwA (h ▸ hzA)
  by_cases hxz : x = z
  · -- x = z, so y ≠ w
    have hyw : y ≠ w := fun h => hef ⟨hxz, h⟩
    rw [← hxz]
    have e1 : ∀ σ : Config N V, zonal N c (σ x) (σ y) * zonal N c' (σ x) (σ w) *
        (dot (σ x) (σ x) ^ p * dot (σ y) (σ w) ^ q)
          = ∑ e ∈ Finset.range (q + 1), ((q.factorial : ℝ) * cK N e q) *
              (zonal N c (σ x) (σ y) * zonal N e (σ y) (σ w) * zonal N c' (σ x) (σ w)) := by
      intro σ
      rw [dot_self, one_pow, one_mul, pow_eq_sum_zon hN q (dot (σ y) (σ w)), Finset.mul_sum, Finset.mul_sum]
      refine Finset.sum_congr rfl (fun e _ => ?_)
      rw [← zonal_eq_zon N e (σ y) (σ w)]
      ring
    have hterm : ∀ e, ∫ σ, zonal N c (σ x) (σ y) * zonal N e (σ y) (σ w) * zonal N c' (σ x) (σ w) ∂(freeMeasure N V)
        = if c = e then (if c = c' then dConc N c else 0) else 0 := by
      intro e
      rw [int_out_pair hN hxy (Ne.symm hyw) c e (zonal_pair_bdd hN c' x w) (fun σ t => by
        simp only [Function.update_of_ne hxy, Function.update_of_ne (Ne.symm hyw)])]
      by_cases hce : c = e
      · rw [if_pos hce, if_pos hce]
        have e2 : (fun σ : Config N V => zonal N c (σ x) (σ w) * zonal N c' (σ x) (σ w))
            = fun σ => zonal N c (σ x) (σ w) * zonal N c' (σ w) (σ x) * (fun _ : Config N V => (1 : ℝ)) σ := by
          funext σ
          rw [zonal_symm N c' (σ x) (σ w)]
          ring
        rw [e2, int_out_pair hN hxw hxw c c' (BddMeas.const 1) (fun σ t => rfl)]
        by_cases hcc : c = c'
        · rw [if_pos hcc, if_pos hcc]
          simp only [mul_one, zonal_self hN c, integral_const, probReal_univ, one_smul]
        · rw [if_neg hcc, if_neg hcc]
      · rw [if_neg hce, if_neg hce]
    have hint : ∀ e ∈ Finset.range (q + 1), Integrable (fun σ : Config N V => ((q.factorial : ℝ) * cK N e q) *
        (zonal N c (σ x) (σ y) * zonal N e (σ y) (σ w) * zonal N c' (σ x) (σ w))) (freeMeasure N V) := fun e _ =>
      ((BddMeas.mul (BddMeas.mul (zonal_pair_bdd hN c x y) (zonal_pair_bdd hN e y w))
        (zonal_pair_bdd hN c' x w)).integrable).const_mul _
    simp only [e1]
    rw [integral_finsetSum _ hint]
    simp only [integral_const_mul, hterm]
    constructor
    · intro hcc
      refine Finset.sum_eq_zero (fun e _ => ?_)
      by_cases hce : c = e
      · rw [if_pos hce, if_neg hcc, mul_zero]
      · rw [if_neg hce, mul_zero]
    · intro hcc
      refine Finset.sum_nonneg (fun e _ => ?_)
      have hq0 : (0 : ℝ) ≤ (q.factorial : ℝ) * cK N e q := mul_nonneg (by positivity) (cK_nonneg hN e q)
      by_cases hce : c = e
      · rw [if_pos hce, if_pos hcc]
        exact mul_nonneg hq0 (dConc_pos_S1 hN c).le
      · rw [if_neg hce, mul_zero]
  · by_cases hyw : y = w
    · -- y = w
      rw [← hyw]
      have e1 : ∀ σ : Config N V, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ y) *
          (dot (σ x) (σ z) ^ p * dot (σ y) (σ y) ^ q)
            = zonal N c (σ x) (σ y) * zonal N c' (σ y) (σ z) * dot (σ x) (σ z) ^ p := by
        intro σ
        rw [dot_self, one_pow, mul_one, zonal_symm N c' (σ z) (σ y)]
      simp only [e1]
      rw [int_out_pair hN hxy hzy c c' (dot_pow_bdd x z p) (fun σ t => by
        simp only [Function.update_of_ne hxy, Function.update_of_ne hzy])]
      constructor
      · intro hcc
        rw [if_neg hcc]
      · intro hcc
        rw [if_pos hcc]
        exact pos_int hN hxz c p
    · exact base_gen hN hxy hxw hzy hzw hxz hyw c c' p q

end Base

end G2S3

#print axioms G2S3.int_out_pair
#print axioms G2S3.gw_side4
#print axioms G2S3.cut_base
