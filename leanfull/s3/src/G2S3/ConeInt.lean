/-
G2S3.ConeInt (stage S3, Part B3, analytic part): integrals over the duplicated coordinate space of elements of the
Ginibre cone of sign 1 are nonnegative; int F exp(G) >= 0; and the strict lower bound int F A B <= int F exp(A+B+C).
Paper: proof of Theorem 3.2 (tex l.322-354), the duplicate-variable form of [Du76, Thm 1 (2.14), Thm 2 (3.1)].
-/
import G2S3.Cone

noncomputable section
open MeasureTheory Real Filter Topology

namespace G2S3

theorem abs_list_prod_le {α : Type*} (l : List α) (f : α → ℝ) (C : ℝ) (hC : ∀ a, |f a| ≤ C) :
    |(l.map f).prod| ≤ C ^ l.length := by
  induction l with
  | nil => simp
  | cons a l ih =>
    rw [List.map_cons, List.prod_cons, abs_mul, List.length_cons, pow_succ]
    have h0 : 0 ≤ C := (abs_nonneg _).trans (hC a)
    rw [mul_comm (C ^ l.length) C]
    exact mul_le_mul (hC a) ih (abs_nonneg _) h0

theorem measurable_list_prod {α Y : Type*} [MeasurableSpace Y] (l : List α) (f : α → Y → ℝ)
    (hf : ∀ a, Measurable (f a)) : Measurable (fun y => (l.map (fun a => f a y)).prod) := by
  induction l with
  | nil => simpa using measurable_const
  | cons a l ih =>
    simp only [List.map_cons, List.prod_cons]
    exact (hf a).mul ih

theorem sgQ_cases (L : List (Bool × Bool)) : sgQ L = 1 ∨ sgQ L = -1 := by
  induction L with
  | nil => left; rfl
  | cons q L ih =>
    have e : sgQ (q :: L) = (if q.1 then sg q.2 else 1) * sgQ L := by
      simp only [sgQ, List.map_cons, List.prod_cons]
    rw [e]
    rcases ih with h | h <;> rw [h] <;> cases q.1 <;> cases q.2 <;> simp

theorem sgQ_mul_self (L : List (Bool × Bool)) : sgQ L * sgQ L = 1 := by
  rcases sgQ_cases L with h | h <;> rw [h] <;> norm_num

section Int

variable {V : Type*} [Fintype V] {X1 X2 I1 I2 : Type*} [MeasurableSpace X1] [MeasurableSpace X2]

/-- The product measure on the duplicated coordinate space. -/
def POm (V : Type*) [Fintype V] (ν : Measure ℝ) (m1 : Measure X1) (m2 : Measure X2) : Measure (Om V X1 X2) :=
  ((Measure.pi fun _ : V => ν).prod (Measure.pi fun _ : V => ν)).prod ((m1.prod m1).prod (m2.prod m2))

instance (ν : Measure ℝ) (m1 : Measure X1) (m2 : Measure X2) [IsProbabilityMeasure ν] [IsProbabilityMeasure m1]
    [IsProbabilityMeasure m2] : IsProbabilityMeasure (POm V ν m1 m2) := by
  unfold POm
  infer_instance

/-- The hypotheses of the Ginibre-Dunlop argument. -/
structure GHyp (ν : Measure ℝ) (ρ τ : ℝ → ℝ) (m1 : Measure X1) (c1 : I1 → X1 → ℝ) (m2 : Measure X2)
    (c2 : I2 → X2 → ℝ) : Prop where
  hρ : Monotone ρ
  hτ : Antitone τ
  hρ0 : ∀ r, 0 ≤ ρ r
  hτ0 : ∀ r, 0 ≤ τ r
  hρ1 : ∀ r, ρ r ≤ 1
  hτ1 : ∀ r, τ r ≤ 1
  hρm : Measurable ρ
  hτm : Measurable τ
  hc1m : ∀ i, Measurable (c1 i)
  hc2m : ∀ j, Measurable (c2 j)
  hc1b : ∀ i x, |c1 i x| ≤ 1
  hc2b : ∀ j x, |c2 j x| ≤ 1
  gin1 : ∀ L : List (I1 × Bool), 0 ≤ ∫ p, angP c1 L p ∂(m1.prod m1)
  gin2 : ∀ L : List (I2 × Bool), 0 ≤ ∫ p, angP c2 L p ∂(m2.prod m2)

variable {ν : Measure ℝ} {ρ τ : ℝ → ℝ} {m1 : Measure X1} {c1 : I1 → X1 → ℝ} {m2 : Measure X2}
  {c2 : I2 → X2 → ℝ}

theorem GHyp.radF_abs_le (H : GHyp ν ρ τ m1 c1 m2 c2) (k s : Bool) (p : ℝ × ℝ) : |radF ρ τ k s p| ≤ 2 := by
  unfold radF
  have hs := abs_sg s
  cases k <;> simp only [Bool.false_eq_true, if_false, if_true]
  · have h1 := H.hρ0 p.1
    have h2 := H.hρ0 p.2
    have h3 := H.hρ1 p.1
    have h4 := H.hρ1 p.2
    calc |ρ p.1 + sg s * ρ p.2| ≤ |ρ p.1| + |sg s * ρ p.2| := abs_add_le _ _
      _ = |ρ p.1| + |ρ p.2| := by rw [abs_mul, hs, one_mul]
      _ ≤ 2 := by rw [abs_of_nonneg h1, abs_of_nonneg h2]; linarith
  · have h1 := H.hτ0 p.1
    have h2 := H.hτ0 p.2
    have h3 := H.hτ1 p.1
    have h4 := H.hτ1 p.2
    calc |τ p.1 + sg s * τ p.2| ≤ |τ p.1| + |sg s * τ p.2| := abs_add_le _ _
      _ = |τ p.1| + |τ p.2| := by rw [abs_mul, hs, one_mul]
      _ ≤ 2 := by rw [abs_of_nonneg h1, abs_of_nonneg h2]; linarith

theorem GHyp.radF_bdd (H : GHyp ν ρ τ m1 c1 m2 c2) (k s : Bool) : BddMeas (radF ρ τ k s) := by
  refine ⟨?_, 2, H.radF_abs_le k s⟩
  unfold radF
  cases k
  · exact (H.hρm.comp measurable_fst).add (measurable_const.mul (H.hρm.comp measurable_snd))
  · exact (H.hτm.comp measurable_fst).add (measurable_const.mul (H.hτm.comp measurable_snd))

theorem angP_bdd {X I : Type*} [MeasurableSpace X] {c : I → X → ℝ} (hm : ∀ i, Measurable (c i))
    (hb : ∀ i x, |c i x| ≤ 1) (L : List (I × Bool)) : BddMeas (angP c L) := by
  refine ⟨measurable_list_prod L _ (fun q => ((hm q.1).comp measurable_fst).add
    (measurable_const.mul ((hm q.1).comp measurable_snd))), 2 ^ L.length, fun p => ?_⟩
  refine abs_list_prod_le L _ 2 (fun q => ?_)
  have h1 := hb q.1 p.1
  have h2 := hb q.1 p.2
  have hs := abs_sg q.2
  calc |c q.1 p.1 + sg q.2 * c q.1 p.2| ≤ |c q.1 p.1| + |sg q.2 * c q.1 p.2| := abs_add_le _ _
    _ = |c q.1 p.1| + |c q.1 p.2| := by rw [abs_mul, hs, one_mul]
    _ ≤ 2 := by linarith

theorem GHyp.radP_bdd (H : GHyp ν ρ τ m1 c1 m2 c2) (rad : V → List (Bool × Bool)) :
    BddMeas (radP (V := V) ρ τ rad) := by
  refine ⟨Finset.measurable_prod _ (fun x _ => measurable_list_prod (rad x) _ (fun q =>
    (H.radF_bdd q.1 q.2).1.comp ((measurable_pi_apply x).comp measurable_fst |>.prodMk
      ((measurable_pi_apply x).comp measurable_snd)))), ∏ x, (2 : ℝ) ^ (rad x).length, fun rr => ?_⟩
  unfold radP
  rw [Finset.abs_prod]
  exact Finset.prod_le_prod₀ (fun x _ => abs_nonneg _)
    (fun x _ => abs_list_prod_le (rad x) _ 2 (fun q => H.radF_abs_le q.1 q.2 _))

theorem GHyp.eval_bdd (H : GHyp ν ρ τ m1 c1 m2 c2) (t : Term V I1 I2) : BddMeas (t.eval ρ τ c1 c2) := by
  have h1 := (H.radP_bdd t.rad).comp (measurable_fst (α := (V → ℝ) × (V → ℝ)) (β := (X1 × X1) × (X2 × X2)))
  have h2 := (angP_bdd H.hc1m H.hc1b t.a1).comp
    ((measurable_fst (α := X1 × X1) (β := X2 × X2)).comp
      (measurable_snd (α := (V → ℝ) × (V → ℝ)) (β := (X1 × X1) × (X2 × X2))))
  have h3 := (angP_bdd H.hc2m H.hc2b t.a2).comp
    ((measurable_snd (α := X1 × X1) (β := X2 × X2)).comp
      (measurable_snd (α := (V → ℝ) × (V → ℝ)) (β := (X1 × X1) × (X2 × X2))))
  exact (h1.mul (h2.mul h3)).const_mul t.c

theorem radP_integral [IsProbabilityMeasure ν] (rad : V → List (Bool × Bool)) :
    ∫ rr, radP ρ τ rad rr ∂((Measure.pi fun _ : V => ν).prod (Measure.pi fun _ : V => ν))
      = ∏ x, ∫ p, ((rad x).map (fun q => radF ρ τ q.1 q.2 p)).prod ∂(ν.prod ν) := by
  have hmp := measurePreserving_arrowProdEquivProdArrow ℝ ℝ V (fun _ : V => ν) (fun _ : V => ν)
  rw [← hmp.integral_comp']
  have e : ∀ z : V → ℝ × ℝ, radP ρ τ rad (MeasurableEquiv.arrowProdEquivProdArrow ℝ ℝ V z)
      = ∏ x, ((rad x).map (fun q => radF ρ τ q.1 q.2 (z x))).prod := by
    intro z
    rfl
  simp only [e]
  exact integral_fintype_prod_eq_prod (μ := fun _ : V => ν.prod ν)
    (fun x (p : ℝ × ℝ) => ((rad x).map (fun q => radF ρ τ q.1 q.2 p)).prod)

theorem term_integral [IsProbabilityMeasure ν] [IsProbabilityMeasure m1] [IsProbabilityMeasure m2]
    (t : Term V I1 I2) :
    ∫ ω, t.eval ρ τ c1 c2 ω ∂(POm V ν m1 m2)
      = t.c * ((∫ rr, radP ρ τ t.rad rr ∂((Measure.pi fun _ : V => ν).prod (Measure.pi fun _ : V => ν)))
        * ((∫ p, angP c1 t.a1 p ∂(m1.prod m1)) * (∫ p, angP c2 t.a2 p ∂(m2.prod m2)))) := by
  unfold Term.eval POm
  rw [integral_const_mul]
  congr 1
  have h1 : ∫ ω : Om V X1 X2, radP ρ τ t.rad ω.1 * (angP c1 t.a1 ω.2.1 * angP c2 t.a2 ω.2.2)
      ∂(((Measure.pi fun _ : V => ν).prod (Measure.pi fun _ : V => ν)).prod ((m1.prod m1).prod (m2.prod m2)))
      = (∫ rr, radP ρ τ t.rad rr ∂((Measure.pi fun _ : V => ν).prod (Measure.pi fun _ : V => ν)))
        * ∫ q, angP c1 t.a1 q.1 * angP c2 t.a2 q.2 ∂((m1.prod m1).prod (m2.prod m2)) :=
    integral_prod_mul (fun rr => radP ρ τ t.rad rr) (fun q : (X1 × X1) × (X2 × X2) => angP c1 t.a1 q.1 * angP c2 t.a2 q.2)
  have h2 : ∫ q : (X1 × X1) × (X2 × X2), angP c1 t.a1 q.1 * angP c2 t.a2 q.2 ∂((m1.prod m1).prod (m2.prod m2))
      = (∫ p, angP c1 t.a1 p ∂(m1.prod m1)) * (∫ p, angP c2 t.a2 p ∂(m2.prod m2)) :=
    integral_prod_mul (fun p => angP c1 t.a1 p) (fun p => angP c2 t.a2 p)
  rw [h1, h2]

theorem angP_odd_zero {X I : Type*} [MeasurableSpace X] (m : Measure X) [IsProbabilityMeasure m]
    (c : I → X → ℝ) (L : List (I × Bool)) (hodd : sgProd L = -1) : ∫ p, angP c L p ∂(m.prod m) = 0 := by
  have h := odd_zero m (L.map (fun q => (fun p : X × X => c q.1 p.1 + sg q.2 * c q.1 p.2, q.2)))
    (fun q hq p' => by
      obtain ⟨q', -, rfl⟩ := List.mem_map.mp hq
      simp only [Prod.fst_swap, Prod.snd_swap]
      cases q'.2 <;> simp [sg] <;> ring)
    (by unfold sgProd at hodd ⊢; rw [List.map_map]; exact hodd)
  simp only [List.map_map, Function.comp_def] at h
  exact h

/-- **Every term of sign 1 has nonnegative integral.** -/
theorem GHyp.term_nonneg [IsProbabilityMeasure ν] [IsProbabilityMeasure m1] [IsProbabilityMeasure m2]
    (H : GHyp ν ρ τ m1 c1 m2 c2) (t : Term V I1 I2) (hc : 0 ≤ t.c) (hs : t.sQ = 1) :
    0 ≤ ∫ ω, t.eval ρ τ c1 c2 ω ∂(POm V ν m1 m2) := by
  rw [term_integral, radP_integral]
  rcases sgProd_cases t.a2 with h2 | h2
  · have hq : ∏ x, sgQ (t.rad x) = 1 := by
      unfold Term.sQ at hs
      rw [h2, mul_one] at hs
      exact hs
    have hrad : 0 ≤ ∏ x, ∫ p, ((t.rad x).map (fun q => radF ρ τ q.1 q.2 p)).prod ∂(ν.prod ν) := by
      have e : ∏ x, ∫ p, ((t.rad x).map (fun q => radF ρ τ q.1 q.2 p)).prod ∂(ν.prod ν)
          = ∏ x, (sgQ (t.rad x) * (sgQ (t.rad x) * ∫ p, ((t.rad x).map (fun q => radF ρ τ q.1 q.2 p)).prod
            ∂(ν.prod ν))) := by
        refine Finset.prod_congr rfl (fun x _ => ?_)
        rw [← mul_assoc, sgQ_mul_self, one_mul]
      rw [e, Finset.prod_mul_distrib, hq, one_mul]
      exact Finset.prod_nonneg (fun x _ => radial_site ν H.hρ H.hτ H.hρ0 H.hτ0 (t.rad x))
    exact mul_nonneg hc (mul_nonneg hrad (mul_nonneg (H.gin1 _) (H.gin2 _)))
  · rw [angP_odd_zero m2 c2 t.a2 h2]
    simp

theorem integral_list_sum {Y : Type*} [MeasurableSpace Y] {μ : Measure Y} {α : Type*} (L : List α)
    (f : α → Y → ℝ) (hf : ∀ a ∈ L, Integrable (f a) μ) :
    ∫ y, (L.map (fun a => f a y)).sum ∂μ = (L.map (fun a => ∫ y, f a y ∂μ)).sum := by
  induction L with
  | nil => simp
  | cons a L ih =>
    simp only [List.map_cons, List.sum_cons]
    have hL : Integrable (fun y => (L.map (fun a => f a y)).sum) μ := by
      clear ih
      induction L with
      | nil => simp
      | cons b L ih2 =>
        simp only [List.map_cons, List.sum_cons]
        exact (hf b (List.mem_cons_of_mem a List.mem_cons_self)).add
          (ih2 (fun c hc => by
            rcases List.mem_cons.mp hc with h | h
            · exact h ▸ hf a List.mem_cons_self
            · exact hf c (List.mem_cons_of_mem a (List.mem_cons_of_mem b h))))
    rw [integral_add (hf a List.mem_cons_self) hL, ih (fun b hb => hf b (List.mem_cons_of_mem a hb))]

theorem GHyp.sum_eval_bdd (H : GHyp ν ρ τ m1 c1 m2 c2) (L : List (Term V I1 I2)) :
    BddMeas (fun ω : Om V X1 X2 => (L.map (fun t => t.eval ρ τ c1 c2 ω)).sum) := by
  induction L with
  | nil => simpa using BddMeas.const (Z := Om V X1 X2) 0
  | cons t L ih =>
    simp only [List.map_cons, List.sum_cons]
    exact (H.eval_bdd t).add ih

theorem GHyp.cone_bdd (H : GHyp ν ρ τ m1 c1 m2 c2) {s : ℝ} {F : Om V X1 X2 → ℝ}
    (hF : InC ρ τ c1 c2 s F) : BddMeas F := by
  obtain ⟨L, -, hFL⟩ := hF
  obtain ⟨hm, C, hC⟩ := H.sum_eval_bdd L
  exact ⟨by simpa only [← funext hFL] using hm, C, fun ω => (hFL ω) ▸ hC ω⟩

/-- **Elements of the cone of sign 1 have nonnegative integral.** -/
theorem GHyp.cone_nonneg [IsProbabilityMeasure ν] [IsProbabilityMeasure m1] [IsProbabilityMeasure m2]
    (H : GHyp ν ρ τ m1 c1 m2 c2) {F : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 1 F) :
    0 ≤ ∫ ω, F ω ∂(POm V ν m1 m2) := by
  obtain ⟨L, hL, hFL⟩ := hF
  simp only [hFL]
  rw [integral_list_sum L (fun t ω => t.eval ρ τ c1 c2 ω) (fun t _ => (H.eval_bdd t).integrable)]
  refine List.sum_nonneg (fun y hy => ?_)
  obtain ⟨t, ht, rfl⟩ := List.mem_map.mp hy
  exact H.term_nonneg t (hL t ht).1 (hL t ht).2

/-- partial sums of the exponential series -/
def expPart (M : ℕ) (x : ℝ) : ℝ := ∑ k ∈ Finset.range M, x ^ k / (k.factorial : ℝ)

theorem InC.expPart {F : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 1 F) (M : ℕ) :
    InC ρ τ c1 c2 1 (fun ω => expPart M (F ω)) := by
  unfold G2S3.expPart
  refine InC.sum _ (fun k _ => ?_)
  have h := (hF.pow k).const_mul (a := 1 / (k.factorial : ℝ)) (by positivity)
  exact h.congr (fun ω => by ring)

/-- **`∫ F exp(G) ≥ 0`** for `F`, `G` in the cone of sign 1. -/
theorem GHyp.cone_exp [IsProbabilityMeasure ν] [IsProbabilityMeasure m1] [IsProbabilityMeasure m2]
    (H : GHyp ν ρ τ m1 c1 m2 c2) {F G : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 1 F) (hG : InC ρ τ c1 c2 1 G) :
    0 ≤ ∫ ω, F ω * Real.exp (G ω) ∂(POm V ν m1 m2) := by
  obtain ⟨hFm, CF0, hCF0⟩ := H.cone_bdd hF
  obtain ⟨hGm, CG, hCG⟩ := H.cone_bdd hG
  set CF := |CF0|
  have hCF : ∀ ω, |F ω| ≤ CF := fun ω => (hCF0 ω).trans (le_abs_self _)
  have hTm : ∀ M, Measurable (fun ω => expPart M (G ω)) := fun M =>
    Finset.measurable_sum _ (fun k _ => (hGm.pow_const k).div_const _)
  have hlim := tendsto_integral_of_dominated_convergence (μ := POm V ν m1 m2)
    (F := fun M ω => F ω * expPart M (G ω)) (f := fun ω => F ω * Real.exp (G ω))
    (fun _ => CF * Real.exp CG)
    (fun M => (hFm.mul (hTm M)).aestronglyMeasurable)
    (integrable_const _)
    (fun M => ae_of_all _ (fun ω => by
      rw [Real.norm_eq_abs, abs_mul]
      refine mul_le_mul (hCF ω) ((abs_partial_exp_le (G ω) M).trans (Real.exp_le_exp.mpr ?_)) (abs_nonneg _)
        (abs_nonneg _)
      exact hCG ω))
    (ae_of_all _ (fun ω => (tendsto_partial_exp (G ω)).const_mul (F ω)))
  refine ge_of_tendsto' hlim (fun M => ?_)
  have h := hF.mul (hG.expPart M)
  rw [one_mul] at h
  exact H.cone_nonneg h

theorem expPart_three_sub (M : ℕ) (A B C : ℝ) :
    expPart (M + 3) (A + B + C) - A * B
      = 1 + (A + B + C) + (A * A + B * B + C * C) / 2 + A * C + B * C
        + ∑ k ∈ Finset.range M, (A + B + C) ^ (k + 3) / ((k + 3).factorial : ℝ) := by
  unfold expPart
  rw [Finset.sum_range_succ', Finset.sum_range_succ', Finset.sum_range_succ']
  simp only [Nat.factorial, Nat.cast_one, pow_zero, pow_one, div_one, Nat.succ_eq_add_one, Nat.cast_mul,
    Nat.cast_ofNat, zero_add]
  ring_nf

/-- **Strict lower bound**: `∫ F A B ≤ ∫ F exp(A + B + C)` for `F, A, B, C` in the cone of sign 1. -/
theorem GHyp.cone_strict [IsProbabilityMeasure ν] [IsProbabilityMeasure m1] [IsProbabilityMeasure m2]
    (H : GHyp ν ρ τ m1 c1 m2 c2) {F A B C : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 1 F)
    (hA : InC ρ τ c1 c2 1 A) (hB : InC ρ τ c1 c2 1 B) (hC : InC ρ τ c1 c2 1 C) :
    ∫ ω, F ω * (A ω * B ω) ∂(POm V ν m1 m2) ≤ ∫ ω, F ω * Real.exp (A ω + B ω + C ω) ∂(POm V ν m1 m2) := by
  have hX : InC ρ τ c1 c2 1 (fun ω => A ω + B ω + C ω) := (hA.add hB).add hC
  obtain ⟨hFm, CF0, hCF0⟩ := H.cone_bdd hF
  obtain ⟨hXm, CX, hCX⟩ := H.cone_bdd hX
  obtain ⟨hAm, CA, hCA⟩ := H.cone_bdd hA
  obtain ⟨hBm, CB, hCB⟩ := H.cone_bdd hB
  set CF := |CF0|
  have hCF : ∀ ω, |F ω| ≤ CF := fun ω => (hCF0 ω).trans (le_abs_self _)
  have hTm : ∀ M, Measurable (fun ω => expPart M (A ω + B ω + C ω)) := fun M =>
    Finset.measurable_sum _ (fun k _ => (hXm.pow_const k).div_const _)
  -- each partial sum minus A B lies in the cone
  have hmem : ∀ M, InC ρ τ c1 c2 1 (fun ω => F ω * (expPart (M + 3) (A ω + B ω + C ω) - A ω * B ω)) := by
    intro M
    have hR : InC ρ τ c1 c2 1 (fun ω => 1 + (A ω + B ω + C ω) + (A ω * A ω + B ω * B ω + C ω * C ω) / 2
        + A ω * C ω + B ω * C ω
        + ∑ k ∈ Finset.range M, (A ω + B ω + C ω) ^ (k + 3) / ((k + 3).factorial : ℝ)) := by
      have h1 := InC.one (ρ := ρ) (τ := τ) (c1 := c1) (c2 := c2) (V := V)
      have hAA := hA.mul hA
      have hBB := hB.mul hB
      have hCC := hC.mul hC
      have hAC := hA.mul hC
      have hBC := hB.mul hC
      simp only [one_mul] at hAA hBB hCC hAC hBC
      have hsq := ((hAA.add hBB).add hCC).const_mul (a := 1 / 2) (by norm_num)
      have htail : InC ρ τ c1 c2 1 (fun ω => ∑ k ∈ Finset.range M,
          (A ω + B ω + C ω) ^ (k + 3) / ((k + 3).factorial : ℝ)) := by
        refine InC.sum _ (fun k _ => ?_)
        exact ((hX.pow (k + 3)).const_mul (a := 1 / ((k + 3).factorial : ℝ)) (by positivity)).congr
          (fun ω => by ring)
      exact (((((h1.add hX).add hsq).add hAC).add hBC).add htail).congr (fun ω => by ring)
    have h := hF.mul hR
    simp only [one_mul] at h
    exact h.congr (fun ω => by rw [expPart_three_sub])
  have hint1 : ∀ M, Integrable (fun ω => F ω * expPart (M + 3) (A ω + B ω + C ω)) (POm V ν m1 m2) := by
    intro M
    exact (H.cone_bdd (hF.mul (hX.expPart (M + 3)))).integrable
  have hint2 : Integrable (fun ω => F ω * (A ω * B ω)) (POm V ν m1 m2) :=
    (H.cone_bdd ((hF.mul (hA.mul hB)))).integrable
  have hge : ∀ M, ∫ ω, F ω * (A ω * B ω) ∂(POm V ν m1 m2)
      ≤ ∫ ω, F ω * expPart (M + 3) (A ω + B ω + C ω) ∂(POm V ν m1 m2) := by
    intro M
    have h := H.cone_nonneg (hmem M)
    have e : (fun ω => F ω * (expPart (M + 3) (A ω + B ω + C ω) - A ω * B ω))
        = fun ω => F ω * expPart (M + 3) (A ω + B ω + C ω) - F ω * (A ω * B ω) := by
      funext ω
      ring
    rw [e, integral_sub (hint1 M) hint2] at h
    linarith
  have hlim := tendsto_integral_of_dominated_convergence (μ := POm V ν m1 m2)
    (F := fun M ω => F ω * expPart (M + 3) (A ω + B ω + C ω))
    (f := fun ω => F ω * Real.exp (A ω + B ω + C ω))
    (fun _ => CF * Real.exp CX)
    (fun M => (hFm.mul (hTm (M + 3))).aestronglyMeasurable)
    (integrable_const _)
    (fun M => ae_of_all _ (fun ω => by
      rw [Real.norm_eq_abs, abs_mul]
      refine mul_le_mul (hCF ω) ((abs_partial_exp_le _ (M + 3)).trans (Real.exp_le_exp.mpr ?_))
        (abs_nonneg _) (abs_nonneg _)
      exact hCX ω))
    (ae_of_all _ (fun ω => ((tendsto_partial_exp (A ω + B ω + C ω)).comp
      (tendsto_add_atTop_nat 3)).const_mul (F ω)))
  exact ge_of_tendsto' hlim hge

end Int

end G2S3

#print axioms G2S3.GHyp.term_nonneg
#print axioms G2S3.GHyp.cone_nonneg
#print axioms G2S3.GHyp.cone_exp
#print axioms G2S3.GHyp.cone_strict
