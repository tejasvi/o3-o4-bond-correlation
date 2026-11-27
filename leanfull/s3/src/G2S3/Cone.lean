/-
G2S3.Cone (stage S3, Part B3): the Ginibre cone on the duplicated coordinate space
  Om = (R^V x R^V) x ((X1 x X1) x (X2 x X2))
with the product of a radial law nu (per site, both copies) and two "angular systems" (X1, m1, c1), (X2, m2, c2), each
satisfying Ginibre's condition. A term is a nonnegative coefficient times products of
  rho(r_x) +- rho(r'_x), tau(r_x) +- tau(r'_x), c1_i(a) +- c1_i(a'), c2_j(b) +- c2_j(b').
Only the sign sQ of the plane-2 factors (tau and c2 factors with a minus sign) is tracked: plane-1 integrals are >= 0
for every list (Ginibre), the per-site radial integral has sign sgQ (Dunlop (2.4), G2S3.radial_site), and a plane-2
angular product with an odd number of minus signs integrates to 0. So every term with sQ = 1 has nonnegative integral.
Consequences: int F exp(H) >= 0 for F, H in the cone of sign 1 (partial sums, dominated convergence), and the strict
lower bound int F exp(A + B + C) >= int F A B.
Paper: the proof of Theorem 3.2 via [Du76, Thm 1 (2.14)] / [Du76, Thm 2 (3.1)] and Lemma 3.3 (tex l.322-354).
-/
import G2S3.Gin

noncomputable section
open MeasureTheory Real Filter Topology

namespace G2S3

/-- A term of the cone. -/
structure Term (V I1 I2 : Type*) where
  c : ℝ
  rad : V → List (Bool × Bool)
  a1 : List (I1 × Bool)
  a2 : List (I2 × Bool)

/-- The duplicated coordinate space. -/
abbrev Om (V X1 X2 : Type*) := ((V → ℝ) × (V → ℝ)) × ((X1 × X1) × (X2 × X2))

/-- An angular product `∏ (c_i(a) ± c_i(a'))`. -/
def angP {X I : Type*} (c : I → X → ℝ) (L : List (I × Bool)) (p : X × X) : ℝ :=
  (L.map (fun q => c q.1 p.1 + sg q.2 * c q.1 p.2)).prod

/-- The radial product `∏_x ∏ (radial factors at x)`. -/
def radP {V : Type*} [Fintype V] (ρ τ : ℝ → ℝ) (rad : V → List (Bool × Bool)) (rr : (V → ℝ) × (V → ℝ)) : ℝ :=
  ∏ x, ((rad x).map (fun q => radF ρ τ q.1 q.2 (rr.1 x, rr.2 x))).prod

namespace Term

variable {V I1 I2 : Type*} [Fintype V]

def eval {X1 X2 : Type*} (ρ τ : ℝ → ℝ) (c1 : I1 → X1 → ℝ) (c2 : I2 → X2 → ℝ) (t : Term V I1 I2)
    (ω : Om V X1 X2) : ℝ :=
  t.c * (radP ρ τ t.rad ω.1 * (angP c1 t.a1 ω.2.1 * angP c2 t.a2 ω.2.2))

/-- The plane-2 sign of a term. -/
def sQ (t : Term V I1 I2) : ℝ := (∏ x, sgQ (t.rad x)) * sgProd t.a2

def mul (t u : Term V I1 I2) : Term V I1 I2 :=
  ⟨t.c * u.c, fun x => t.rad x ++ u.rad x, t.a1 ++ u.a1, t.a2 ++ u.a2⟩

theorem eval_mul {X1 X2 : Type*} (ρ τ : ℝ → ℝ) (c1 : I1 → X1 → ℝ) (c2 : I2 → X2 → ℝ) (t u : Term V I1 I2)
    (ω : Om V X1 X2) : (t.mul u).eval ρ τ c1 c2 ω = t.eval ρ τ c1 c2 ω * u.eval ρ τ c1 c2 ω := by
  simp only [eval, mul, radP, angP, List.map_append, List.prod_append, Finset.prod_mul_distrib]
  ring

theorem sQ_mul (t u : Term V I1 I2) : (t.mul u).sQ = t.sQ * u.sQ := by
  simp only [sQ, mul, sgQ, sgProd, List.map_append, List.prod_append, Finset.prod_mul_distrib]
  ring

end Term

theorem list_sum_mul {α : Type*} (L : List α) (f : α → ℝ) (a : ℝ) :
    (L.map f).sum * a = (L.map (fun x => f x * a)).sum := by
  induction L with
  | nil => simp
  | cons x L ih => simp [ih, add_mul]

theorem list_mul_sum {α : Type*} (L : List α) (f : α → ℝ) (a : ℝ) :
    a * (L.map f).sum = (L.map (fun x => a * f x)).sum := by
  induction L with
  | nil => simp
  | cons x L ih => simp [ih, mul_add]

theorem list_sum_flatMap {α β : Type*} (L : List α) (g : α → List β) (f : β → ℝ) :
    ((L.flatMap g).map f).sum = (L.map (fun x => ((g x).map f).sum)).sum := by
  induction L with
  | nil => simp
  | cons x L ih => simp [ih, List.flatMap_cons]

section Cone

variable {V : Type*} [Fintype V] {X1 X2 I1 I2 : Type*}
variable (ρ τ : ℝ → ℝ) (c1 : I1 → X1 → ℝ) (c2 : I2 → X2 → ℝ)

/-- The cone of sign `s`: finite sums of terms with nonnegative coefficients and plane-2 sign `s`. -/
def InC (s : ℝ) (F : Om V X1 X2 → ℝ) : Prop :=
  ∃ L : List (Term V I1 I2), (∀ t ∈ L, 0 ≤ t.c ∧ t.sQ = s) ∧ ∀ ω, F ω = (L.map (fun t => t.eval ρ τ c1 c2 ω)).sum

variable {ρ τ c1 c2}

theorem InC.add {s : ℝ} {F G : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 s F) (hG : InC ρ τ c1 c2 s G) :
    InC ρ τ c1 c2 s (fun ω => F ω + G ω) := by
  obtain ⟨L, hL, hFL⟩ := hF
  obtain ⟨M, hM, hGM⟩ := hG
  refine ⟨L ++ M, fun t ht => ?_, fun ω => ?_⟩
  · rcases List.mem_append.mp ht with h | h
    · exact hL t h
    · exact hM t h
  · beta_reduce
    rw [List.map_append, List.sum_append, hFL, hGM]

theorem InC.zero (s : ℝ) : InC ρ τ c1 c2 s (fun _ : Om V X1 X2 => 0) :=
  ⟨[], fun t ht => absurd ht List.not_mem_nil, fun _ => rfl⟩

theorem InC.one : InC ρ τ c1 c2 1 (fun _ : Om V X1 X2 => 1) := by
  refine ⟨[⟨1, fun _ => [], [], []⟩], fun t ht => ?_, fun ω => ?_⟩
  · rw [List.mem_singleton] at ht
    subst ht
    simp [Term.sQ, sgQ, sgProd]
  · simp [Term.eval, radP, angP]

theorem InC.const_mul {s : ℝ} {F : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 s F) {a : ℝ} (ha : 0 ≤ a) :
    InC ρ τ c1 c2 s (fun ω => a * F ω) := by
  obtain ⟨L, hL, hFL⟩ := hF
  refine ⟨L.map (fun t => ⟨a * t.c, t.rad, t.a1, t.a2⟩), fun t ht => ?_, fun ω => ?_⟩
  · obtain ⟨u, hu, rfl⟩ := List.mem_map.mp ht
    exact ⟨mul_nonneg ha (hL u hu).1, (hL u hu).2⟩
  · beta_reduce
    rw [hFL, List.map_map, list_mul_sum]
    congr 1
    refine List.map_congr_left (fun t _ => ?_)
    simp only [Function.comp, Term.eval]
    ring

theorem InC.mul {s s' : ℝ} {F G : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 s F) (hG : InC ρ τ c1 c2 s' G) :
    InC ρ τ c1 c2 (s * s') (fun ω => F ω * G ω) := by
  obtain ⟨L, hL, hFL⟩ := hF
  obtain ⟨M, hM, hGM⟩ := hG
  refine ⟨L.flatMap (fun t => M.map (fun u => t.mul u)), fun t ht => ?_, fun ω => ?_⟩
  · obtain ⟨t1, ht1, ht⟩ := List.mem_flatMap.mp ht
    obtain ⟨u, hu, rfl⟩ := List.mem_map.mp ht
    refine ⟨mul_nonneg (hL t1 ht1).1 (hM u hu).1, ?_⟩
    rw [Term.sQ_mul, (hL t1 ht1).2, (hM u hu).2]
  · beta_reduce
    rw [hFL, hGM, list_sum_flatMap, list_sum_mul]
    congr 1
    refine List.map_congr_left (fun t _ => ?_)
    rw [List.map_map, list_mul_sum]
    congr 1
    refine List.map_congr_left (fun u _ => ?_)
    simp only [Function.comp, Term.eval_mul]

theorem InC.pow {F : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 1 F) (n : ℕ) :
    InC ρ τ c1 c2 1 (fun ω => F ω ^ n) := by
  induction n with
  | zero => simpa using (InC.one (ρ := ρ) (τ := τ) (c1 := c1) (c2 := c2) (V := V))
  | succ n ih =>
    have h := ih.mul hF
    simp only [one_mul] at h
    simpa [pow_succ] using h

theorem InC.sum {s : ℝ} {ι : Type*} (S : Finset ι) {F : ι → Om V X1 X2 → ℝ}
    (hF : ∀ i ∈ S, InC ρ τ c1 c2 s (F i)) : InC ρ τ c1 c2 s (fun ω => ∑ i ∈ S, F i ω) := by
  classical
  induction S using Finset.induction_on with
  | empty => simpa using InC.zero (ρ := ρ) (τ := τ) (c1 := c1) (c2 := c2) (V := V) s
  | insert a S ha ih =>
    have h1 := hF a (Finset.mem_insert_self a S)
    have h2 := ih (fun i hi => hF i (Finset.mem_insert_of_mem hi))
    have h := h1.add h2
    simpa [Finset.sum_insert ha] using h

theorem InC.congr {s : ℝ} {F G : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 s F) (h : ∀ ω, G ω = F ω) :
    InC ρ τ c1 c2 s G := by
  obtain ⟨L, hL, hFL⟩ := hF
  exact ⟨L, hL, fun ω => (h ω).trans (hFL ω)⟩

/-! ### Generators -/

theorem InC.radRho (x : V) (b : Bool) :
    InC ρ τ c1 c2 1 (fun ω : Om V X1 X2 => ρ (ω.1.1 x) + sg b * ρ (ω.1.2 x)) := by
  classical
  refine ⟨[⟨1, fun y => if y = x then [(false, b)] else [], [], []⟩], fun t ht => ?_, fun ω => ?_⟩
  · rw [List.mem_singleton] at ht
    subst ht
    refine ⟨zero_le_one, ?_⟩
    simp only [Term.sQ, sgProd, List.map_nil, List.prod_nil, mul_one]
    refine Finset.prod_eq_one (fun y _ => ?_)
    by_cases hy : y = x <;> simp [hy, sgQ]
  · simp only [Term.eval, radP, angP, List.map_nil, List.prod_nil, mul_one, one_mul, List.map_cons,
      List.sum_cons, List.sum_nil, add_zero]
    rw [Finset.prod_eq_single x (fun y _ hy => by simp [hy]) (fun h => absurd (Finset.mem_univ x) h)]
    simp [radF]

theorem InC.radTau (x : V) (b : Bool) :
    InC ρ τ c1 c2 (sg b) (fun ω : Om V X1 X2 => τ (ω.1.1 x) + sg b * τ (ω.1.2 x)) := by
  classical
  refine ⟨[⟨1, fun y => if y = x then [(true, b)] else [], [], []⟩], fun t ht => ?_, fun ω => ?_⟩
  · rw [List.mem_singleton] at ht
    subst ht
    refine ⟨zero_le_one, ?_⟩
    simp only [Term.sQ, sgProd, List.map_nil, List.prod_nil, mul_one]
    rw [Finset.prod_eq_single x (fun y _ hy => by simp [hy, sgQ]) (fun h => absurd (Finset.mem_univ x) h)]
    simp [sgQ]
  · simp only [Term.eval, radP, angP, List.map_nil, List.prod_nil, mul_one, one_mul, List.map_cons,
      List.sum_cons, List.sum_nil, add_zero]
    rw [Finset.prod_eq_single x (fun y _ hy => by simp [hy]) (fun h => absurd (Finset.mem_univ x) h)]
    simp [radF]

theorem InC.ang1 (i : I1) (b : Bool) :
    InC ρ τ c1 c2 1 (fun ω : Om V X1 X2 => c1 i ω.2.1.1 + sg b * c1 i ω.2.1.2) := by
  refine ⟨[⟨1, fun _ => [], [(i, b)], []⟩], fun t ht => ?_, fun ω => ?_⟩
  · rw [List.mem_singleton] at ht
    subst ht
    simp [Term.sQ, sgQ, sgProd]
  · simp [Term.eval, radP, angP]

theorem InC.ang2 (j : I2) (b : Bool) :
    InC ρ τ c1 c2 (sg b) (fun ω : Om V X1 X2 => c2 j ω.2.2.1 + sg b * c2 j ω.2.2.2) := by
  refine ⟨[⟨1, fun _ => [], [], [(j, b)]⟩], fun t ht => ?_, fun ω => ?_⟩
  · rw [List.mem_singleton] at ht
    subst ht
    simp [Term.sQ, sgQ, sgProd]
  · simp [Term.eval, radP, angP]

end Cone

end G2S3
