/-
G2S3.Gin (stage S3, Part B1-B2): the single-system positivity lemmas of the Ginibre duplicate-variable argument.
- `odd_zero`: a product of factors that change sign under the exchange of the two copies integrates to 0 when the
  number of sign changes is odd.
- `radial_site`: Dunlop's hypothesis of negative correlation [Du76, (2.4)] for any law of the radius, with plane-1
  radius rho (increasing) and plane-2 radius tau (decreasing): the exchange argument of the paper's Lemma 3.3
  (tex l.340-354), stated with the sign of the tau-factors made explicit.
- `gin_circle`: Ginibre's condition for the torus (AddCircle (2 pi))^V with Haar measure and the functions
  cos(n . theta), via the surjective homomorphism (alpha, beta) -> (alpha + beta, alpha - beta) and
  cos(A + B) +- cos(A - B) = 2 cos A cos B or -2 sin A sin B.
- `gin_ising`: Griffiths' condition for {+-1}^V with the uniform measure and the characters, via
  (eps, eta) -> (eps, eps * eta).
-/
import G2S3.RPNamed

noncomputable section
open MeasureTheory Real

namespace G2S3

/-! ### Signs -/

/-- The sign of a flag: `false ↦ 1`, `true ↦ -1`. -/
def sg (b : Bool) : ℝ := if b then -1 else 1

@[simp] theorem sg_false : sg false = 1 := rfl
@[simp] theorem sg_true : sg true = -1 := rfl

theorem sg_mul_self (b : Bool) : sg b * sg b = 1 := by cases b <;> simp [sg]

theorem abs_sg (b : Bool) : |sg b| = 1 := by cases b <;> simp [sg]

/-- The product of the signs of a list of flagged items. -/
def sgProd {α : Type*} (L : List (α × Bool)) : ℝ := (L.map (fun q => sg q.2)).prod

theorem sgProd_cases {α : Type*} (L : List (α × Bool)) : sgProd L = 1 ∨ sgProd L = -1 := by
  induction L with
  | nil => left; rfl
  | cons q L ih =>
    have e : sgProd (q :: L) = sg q.2 * sgProd L := by
      simp only [sgProd, List.map_cons, List.prod_cons]
    rw [e]
    rcases ih with h | h <;> rw [h] <;> cases q.2 <;> simp

/-! ### Odd exchange sign gives zero -/

theorem prod_swap_sign {X : Type*} (L : List ((X × X → ℝ) × Bool))
    (hswap : ∀ q ∈ L, ∀ p, q.1 p.swap = sg q.2 * q.1 p) (p : X × X) :
    (L.map (fun q => q.1 p.swap)).prod = sgProd L * (L.map (fun q => q.1 p)).prod := by
  induction L with
  | nil => simp [sgProd]
  | cons q L ih =>
    have h1 := hswap q List.mem_cons_self p
    have h2 := ih (fun q' hq' => hswap q' (List.mem_cons_of_mem q hq'))
    simp only [List.map_cons, List.prod_cons, sgProd] at h2 ⊢
    rw [h1, h2]
    ring

theorem odd_zero {X : Type*} [MeasurableSpace X] (μ : Measure X) [SFinite μ] (L : List ((X × X → ℝ) × Bool))
    (hswap : ∀ q ∈ L, ∀ p, q.1 p.swap = sg q.2 * q.1 p) (hodd : sgProd L = -1) :
    ∫ p, (L.map (fun q => q.1 p)).prod ∂(μ.prod μ) = 0 := by
  have h := integral_prod_swap (μ := μ) (ν := μ) (fun p => (L.map (fun q => q.1 p)).prod)
  simp only [prod_swap_sign L hswap, hodd, neg_one_mul, integral_neg] at h
  linarith

/-! ### The radial lemma (Dunlop's hypothesis (2.4)) -/

/-- A radial factor of the duplicated system: `ρ(r) ± ρ(r')` (`k = false`) or `τ(r) ± τ(r')` (`k = true`). -/
def radF (ρ τ : ℝ → ℝ) (k s : Bool) (p : ℝ × ℝ) : ℝ :=
  if k then τ p.1 + sg s * τ p.2 else ρ p.1 + sg s * ρ p.2

/-- The sign carried by the `τ`-factors with a minus sign. -/
def sgQ (L : List (Bool × Bool)) : ℝ := (L.map (fun q => if q.1 then sg q.2 else 1)).prod

theorem radF_swap (ρ τ : ℝ → ℝ) (k s : Bool) (p : ℝ × ℝ) :
    radF ρ τ k s p.swap = sg s * radF ρ τ k s p := by
  unfold radF
  cases k <;> cases s <;> simp [sg] <;> ring

/-- **Dunlop's condition (2.4), one site**: `sgQ(L) · ∫∫ ∏ (radial factors) dν dν ≥ 0`, for every law `ν`. -/
theorem radial_site (ν : Measure ℝ) [IsProbabilityMeasure ν] {ρ τ : ℝ → ℝ} (hρ : Monotone ρ) (hτ : Antitone τ)
    (hρ0 : ∀ r, 0 ≤ ρ r) (hτ0 : ∀ r, 0 ≤ τ r) (L : List (Bool × Bool)) :
    0 ≤ sgQ L * ∫ p, (L.map (fun q => radF ρ τ q.1 q.2 p)).prod ∂(ν.prod ν) := by
  rcases sgProd_cases L with hev | hodd
  · rw [← integral_const_mul]
    refine integral_nonneg (fun p => ?_)
    -- the adjusted factors are nonnegative when `p.2 ≤ p.1`
    have hadj : ∀ p : ℝ × ℝ, p.2 ≤ p.1 →
        0 ≤ sgQ L * (L.map (fun q => radF ρ τ q.1 q.2 p)).prod := by
      intro p hp
      have e : sgQ L * (L.map (fun q => radF ρ τ q.1 q.2 p)).prod
          = (L.map (fun q => (if q.1 then sg q.2 else 1) * radF ρ τ q.1 q.2 p)).prod := by
        unfold sgQ
        rw [← List.prod_map_mul]
      rw [e]
      refine List.prod_nonneg (fun x hx => ?_)
      obtain ⟨q, -, rfl⟩ := List.mem_map.mp hx
      obtain ⟨k, s⟩ := q
      unfold radF
      cases k <;> cases s <;> simp only [sg, if_true, if_false, Bool.false_eq_true, one_mul]
      · linarith [hρ0 p.1, hρ0 p.2]
      · linarith [hρ hp]
      · linarith [hτ0 p.1, hτ0 p.2]
      · linarith [hτ hp]
    by_cases hp : p.2 ≤ p.1
    · exact hadj p hp
    · have hp' : p.swap.2 ≤ p.swap.1 := by
        simp only [Prod.snd_swap, Prod.fst_swap]
        linarith
      have h := hadj p.swap hp'
      have hsw := prod_swap_sign (L.map (fun q => (radF ρ τ q.1 q.2, q.2)))
        (fun q hq p' => by
          obtain ⟨q', -, rfl⟩ := List.mem_map.mp hq
          exact radF_swap ρ τ q'.1 q'.2 p') p
      simp only [List.map_map, Function.comp_def] at hsw
      have hs : sgProd (L.map (fun q => (radF ρ τ q.1 q.2, q.2))) = 1 := by
        unfold sgProd at hev ⊢
        rw [List.map_map]
        exact hev
      rw [hsw, hs, one_mul] at h
      exact h
  · have h := odd_zero ν (L.map (fun q => (radF ρ τ q.1 q.2, q.2)))
      (fun q hq p' => by
        obtain ⟨q', -, rfl⟩ := List.mem_map.mp hq
        exact radF_swap ρ τ q'.1 q'.2 p')
      (by unfold sgProd at hodd ⊢; rw [List.map_map]; exact hodd)
    simp only [List.map_map, Function.comp_def] at h
    rw [h, mul_zero]

/-! ### The circle -/

local instance instFactTwoPiPos : Fact (0 < 2 * π) := ⟨Real.two_pi_pos⟩

/-- The circle `ℝ / 2πℤ`. -/
abbrev Tor := AddCircle (2 * π)

/-- cosine and sine on the circle -/
def tcos : Tor → ℝ := Real.cos_periodic.lift
def tsin : Tor → ℝ := Real.sin_periodic.lift

@[simp] theorem tcos_coe (x : ℝ) : tcos (x : Tor) = Real.cos x := rfl
@[simp] theorem tsin_coe (x : ℝ) : tsin (x : Tor) = Real.sin x := rfl

theorem continuous_tcos : Continuous tcos := Real.continuous_cos.quotient_liftOn' _
theorem continuous_tsin : Continuous tsin := Real.continuous_sin.quotient_liftOn' _

theorem tcos_add_add_sub (A B : Tor) : tcos (A + B) + tcos (A - B) = 2 * tcos A * tcos B := by
  induction A using QuotientAddGroup.induction_on with
  | H a =>
    induction B using QuotientAddGroup.induction_on with
    | H b =>
      rw [← AddCircle.coe_add, ← AddCircle.coe_sub, tcos_coe, tcos_coe, tcos_coe, tcos_coe, Real.cos_add,
        Real.cos_sub]
      ring

theorem tcos_add_sub_sub (A B : Tor) : tcos (A + B) - tcos (A - B) = -2 * tsin A * tsin B := by
  induction A using QuotientAddGroup.induction_on with
  | H a =>
    induction B using QuotientAddGroup.induction_on with
    | H b =>
      rw [← AddCircle.coe_add, ← AddCircle.coe_sub, tcos_coe, tcos_coe, tsin_coe, tsin_coe, Real.cos_add,
        Real.cos_sub]
      ring

theorem abs_tcos_le (A : Tor) : |tcos A| ≤ 1 := by
  induction A using QuotientAddGroup.induction_on with
  | H a => exact Real.abs_cos_le_one a

variable {V : Type*} [Fintype V]

/-- `n · θ = ∑_x n_x θ_x` on the torus. -/
def dotT (n : V → ℤ) (θ : V → Tor) : Tor := ∑ x, n x • θ x

theorem dotT_add (n : V → ℤ) (α β : V → Tor) : dotT n (α + β) = dotT n α + dotT n β := by
  unfold dotT
  rw [← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl (fun x _ => by simp [smul_add])

theorem dotT_sub (n : V → ℤ) (α β : V → Tor) : dotT n (α - β) = dotT n α - dotT n β := by
  unfold dotT
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl (fun x _ => by simp [smul_sub])

theorem continuous_dotT (n : V → ℤ) : Continuous (dotT n) :=
  continuous_finset_sum _ (fun x _ => (continuous_zsmul (n x)).comp (continuous_apply x))

/-- The functions `cos(n · θ)` of Ginibre's argument. -/
def ccos (n : V → ℤ) (θ : V → Tor) : ℝ := tcos (dotT n θ)

theorem continuous_ccos (n : V → ℤ) : Continuous (ccos n) := continuous_tcos.comp (continuous_dotT n)

theorem abs_ccos_le (n : V → ℤ) (θ : V → Tor) : |ccos n θ| ≤ 1 := abs_tcos_le _

/-- The Haar probability measure on the torus `Tor^V`. -/
def torMeas (V : Type*) [Fintype V] : Measure (V → Tor) := Measure.pi fun _ => AddCircle.haarAddCircle

instance : IsProbabilityMeasure (torMeas V) := by unfold torMeas; infer_instance

instance : (torMeas V).IsAddHaarMeasure := by unfold torMeas; infer_instance

instance instSCTor : SecondCountableTopology (V → Tor) := inferInstance

/-- `(α, β) ↦ (α + β, α - β)` as a homomorphism. -/
def psiHom (G : Type*) [AddCommGroup G] : G × G →+ G × G where
  toFun := fun p => (p.1 + p.2, p.1 - p.2)
  map_zero' := by simp
  map_add' := by
    intro p q
    ext <;> simp <;> abel

theorem psiHom_surj : Function.Surjective (psiHom (V → Tor)) := by
  intro q
  have h : ∀ x : Tor, ∃ y : Tor, y + y = x := by
    intro x
    induction x using QuotientAddGroup.induction_on with
    | H a => exact ⟨((a / 2 : ℝ) : Tor), by rw [← AddCircle.coe_add]; congr 1; ring⟩
  choose half hhalf using h
  refine ⟨(fun x => half (q.1 x + q.2 x), fun x => half (q.1 x + q.2 x) - q.2 x), ?_⟩
  ext x
  · show half (q.1 x + q.2 x) + (half (q.1 x + q.2 x) - q.2 x) = q.1 x
    have := hhalf (q.1 x + q.2 x)
    rw [← add_sub_assoc, this]
    abel
  · show half (q.1 x + q.2 x) - (half (q.1 x + q.2 x) - q.2 x) = q.2 x
    abel

theorem psi_measurePreserving :
    MeasurePreserving (psiHom (V → Tor)) ((torMeas V).prod (torMeas V)) ((torMeas V).prod (torMeas V)) := by
  haveI : ((torMeas V).prod (torMeas V)).IsAddHaarMeasure :=
    MeasureTheory.Measure.prod.instIsAddHaarMeasure (torMeas V) (torMeas V)
  exact AddMonoidHom.measurePreserving
    ((continuous_fst.add continuous_snd).prodMk (continuous_fst.sub continuous_snd)) psiHom_surj rfl

/-- **Ginibre's condition on the torus.** -/
theorem gin_circle (L : List ((V → ℤ) × Bool)) :
    0 ≤ ∫ p, (L.map (fun q => ccos q.1 p.1 + sg q.2 * ccos q.1 p.2)).prod
      ∂((torMeas V).prod (torMeas V)) := by
  rcases sgProd_cases L with hev | hodd
  · set F : (V → Tor) × (V → Tor) → ℝ := fun p => (L.map (fun q => ccos q.1 p.1 + sg q.2 * ccos q.1 p.2)).prod
      with hF
    have hFc : Continuous F := by
      rw [hF]
      refine continuous_list_prod _ (fun q _ => ?_)
      exact ((continuous_ccos q.1).comp continuous_fst).add
        (continuous_const.mul ((continuous_ccos q.1).comp continuous_snd))
    have hmp := psi_measurePreserving (V := V)
    rw [← hmp.map_eq, integral_map hmp.measurable.aemeasurable hFc.aestronglyMeasurable]
    -- the factorization
    set g : ((V → ℤ) × Bool) → (V → Tor) → ℝ :=
      fun q θ => if q.2 then tsin (dotT q.1 θ) else tcos (dotT q.1 θ) with hg
    have hfac : ∀ p : (V → Tor) × (V → Tor), F (psiHom (V → Tor) p)
        = (2 : ℝ) ^ L.length * ((L.map (fun q => g q p.1)).prod * (L.map (fun q => g q p.2)).prod) := by
      intro p
      have hq : ∀ q : (V → ℤ) × Bool, ccos q.1 (p.1 + p.2) + sg q.2 * ccos q.1 (p.1 - p.2)
          = sg q.2 * (2 * (g q p.1 * g q p.2)) := by
        intro q
        simp only [ccos, dotT_add, dotT_sub, hg]
        cases q.2
        · simp only [sg_false, one_mul, if_false, Bool.false_eq_true]
          rw [tcos_add_add_sub]
          ring
        · simp only [sg_true, if_true]
          have := tcos_add_sub_sub (dotT q.1 p.1) (dotT q.1 p.2)
          linarith
      show (L.map (fun q => ccos q.1 (p.1 + p.2) + sg q.2 * ccos q.1 (p.1 - p.2))).prod = _
      simp only [hq]
      rw [List.prod_map_mul, List.prod_map_mul, List.prod_map_mul]
      have h1 : (L.map (fun q => sg q.2)).prod = 1 := hev
      rw [h1, one_mul, List.map_const', List.prod_replicate]
    simp only [hfac]
    rw [integral_const_mul]
    have hpm : ∫ a, (L.map (fun q => g q a.1)).prod * (L.map (fun q => g q a.2)).prod
        ∂((torMeas V).prod (torMeas V))
        = (∫ θ, (L.map (fun q => g q θ)).prod ∂(torMeas V)) * (∫ θ, (L.map (fun q => g q θ)).prod ∂(torMeas V)) :=
      integral_prod_mul (fun θ => (L.map (fun q => g q θ)).prod) (fun θ => (L.map (fun q => g q θ)).prod)
    rw [hpm]
    exact mul_nonneg (pow_nonneg (by norm_num) _) (mul_self_nonneg _)
  · have h := odd_zero (torMeas V) (L.map (fun q => (fun p : (V → Tor) × (V → Tor) =>
        ccos q.1 p.1 + sg q.2 * ccos q.1 p.2, q.2)))
      (fun q hq p' => by
        obtain ⟨q', -, rfl⟩ := List.mem_map.mp hq
        simp only [Prod.fst_swap, Prod.snd_swap]
        cases q'.2 <;> simp [sg] <;> ring)
      (by unfold sgProd at hodd ⊢; rw [List.map_map]; exact hodd)
    simp only [List.map_map, Function.comp_def] at h
    rw [h]

/-! ### Ising signs -/

/-- the character value of a sign flag (`true` = `-1`) at an integer exponent -/
def chi (b : Bool) (k : ℤ) : ℝ := if b then (-1) ^ k.natAbs else 1

theorem abs_chi (b : Bool) (k : ℤ) : |chi b k| = 1 := by
  unfold chi
  cases b <;> simp

theorem chi_xor (a b : Bool) (k : ℤ) : chi (xor a b) k = chi a k * chi b k := by
  unfold chi
  cases a <;> cases b <;> simp [← pow_add, ← two_mul, pow_mul]

/-- The characters `∏_x ε_x^{n_x}` of Griffiths' argument. -/
def cising (n : V → ℤ) (ε : V → Bool) : ℝ := ∏ x, chi (ε x) (n x)

theorem abs_cising (n : V → ℤ) (ε : V → Bool) : |cising n ε| = 1 := by
  unfold cising
  rw [Finset.abs_prod]
  exact Finset.prod_eq_one (fun x _ => abs_chi _ _)

theorem cising_xor (n : V → ℤ) (ε η : V → Bool) :
    cising n (fun x => xor (ε x) (η x)) = cising n ε * cising n η := by
  unfold cising
  rw [← Finset.prod_mul_distrib]
  exact Finset.prod_congr rfl (fun x _ => chi_xor _ _ _)

/-- The uniform probability measure on `Bool`. -/
def unifB : Measure Bool := (2 : ENNReal)⁻¹ • (Measure.dirac false + Measure.dirac true)

instance : IsProbabilityMeasure unifB := by
  constructor
  simp only [unifB, Measure.smul_apply, Measure.add_apply, Measure.dirac_apply_of_mem (Set.mem_univ _),
    smul_eq_mul]
  rw [one_add_one_eq_two]
  exact ENNReal.inv_mul_cancel (by norm_num) (by norm_num)

theorem integral_unifB (f : Bool → ℝ) : ∫ b, f b ∂unifB = (f false + f true) / 2 := by
  unfold unifB
  rw [integral_smul_measure, integral_add_measure (integrable_dirac (by simp)) (integrable_dirac (by simp)),
    integral_dirac, integral_dirac]
  simp only [ENNReal.toReal_inv, ENNReal.toReal_ofNat, smul_eq_mul]
  ring

theorem unifB_singleton (b : Bool) : unifB {b} = 2⁻¹ := by
  cases b <;> simp [unifB, Measure.dirac_apply']

theorem xor_measurePreserving (c : Bool) : MeasurePreserving (fun b => xor c b) unifB unifB := by
  refine ⟨measurable_of_finite _, Measure.ext_iff_singleton.mpr (fun a => ?_)⟩
  rw [Measure.map_apply (measurable_of_finite _) (measurableSet_singleton a)]
  have h : (fun b => xor c b) ⁻¹' {a} = {xor c a} := by
    ext b
    cases b <;> cases c <;> cases a <;> simp
  rw [h, unifB_singleton, unifB_singleton]

/-- The uniform probability measure on `Bool^V`. -/
def isMeas (V : Type*) [Fintype V] : Measure (V → Bool) := Measure.pi fun _ => unifB

instance : IsProbabilityMeasure (isMeas V) := by unfold isMeas; infer_instance

theorem shear_measurePreserving :
    MeasurePreserving (fun p : (V → Bool) × (V → Bool) => (p.1, fun x => xor (p.1 x) (p.2 x)))
      ((isMeas V).prod (isMeas V)) ((isMeas V).prod (isMeas V)) := by
  refine MeasurePreserving.skew_product (g := fun (ε η : V → Bool) => fun x => xor (ε x) (η x)) (MeasurePreserving.id _)
    (measurable_of_finite _) ?_
  refine ae_of_all _ (fun ε => ?_)
  exact (measurePreserving_pi (fun _ => unifB) (fun _ => unifB) (fun x => xor_measurePreserving (ε x))).map_eq

theorem integral_isMeas_prod (f : V → Bool → ℝ) :
    ∫ ε, ∏ x, f x (ε x) ∂(isMeas V) = ∏ x, (f x false + f x true) / 2 := by
  unfold isMeas
  rw [integral_fintype_prod_eq_prod]
  exact Finset.prod_congr rfl (fun x _ => integral_unifB _)

theorem abs_list_prod_eq_one (l : List ℝ) (h : ∀ x ∈ l, |x| = 1) : |l.prod| = 1 := by
  induction l with
  | nil => simp
  | cons a l ih =>
    rw [List.prod_cons, abs_mul, h a List.mem_cons_self,
      ih (fun x hx => h x (List.mem_cons_of_mem a hx)), one_mul]

theorem prod_cising_eq (L : List ((V → ℤ) × Bool)) (ε : V → Bool) :
    (L.map (fun q => cising q.1 ε)).prod = ∏ x, (L.map (fun q => chi (ε x) (q.1 x))).prod := by
  induction L with
  | nil => simp
  | cons q L ih =>
    rw [List.map_cons, List.prod_cons, ih]
    simp only [List.map_cons, List.prod_cons]
    rw [Finset.prod_mul_distrib]
    rfl

/-- **Griffiths' condition on `{±1}^V`.** -/
theorem gin_ising (L : List ((V → ℤ) × Bool)) :
    0 ≤ ∫ p, (L.map (fun q => cising q.1 p.1 + sg q.2 * cising q.1 p.2)).prod
      ∂((isMeas V).prod (isMeas V)) := by
  have hmp := shear_measurePreserving (V := V)
  rw [← hmp.map_eq, integral_map hmp.measurable.aemeasurable (measurable_of_finite _).aestronglyMeasurable]
  have hfac : ∀ p : (V → Bool) × (V → Bool),
      (L.map (fun q => cising q.1 p.1 + sg q.2 * cising q.1 (fun x => xor (p.1 x) (p.2 x)))).prod
        = (L.map (fun q => cising q.1 p.1)).prod * (L.map (fun q => 1 + sg q.2 * cising q.1 p.2)).prod := by
    intro p
    rw [← List.prod_map_mul]
    congr 1
    refine List.map_congr_left (fun q _ => ?_)
    rw [cising_xor]
    ring
  simp only [hfac]
  have hpm : ∫ a, (L.map (fun q => cising q.1 a.1)).prod * (L.map (fun q => 1 + sg q.2 * cising q.1 a.2)).prod
      ∂((isMeas V).prod (isMeas V))
      = (∫ ε, (L.map (fun q => cising q.1 ε)).prod ∂(isMeas V))
        * (∫ η, (L.map (fun q => 1 + sg q.2 * cising q.1 η)).prod ∂(isMeas V)) :=
    integral_prod_mul (fun ε => (L.map (fun q => cising q.1 ε)).prod)
      (fun η => (L.map (fun q => 1 + sg q.2 * cising q.1 η)).prod)
  rw [hpm]
  refine mul_nonneg ?_ (integral_nonneg (fun η => List.prod_nonneg (fun y hy => ?_)))
  · simp only [prod_cising_eq L]
    rw [integral_isMeas_prod (fun x b => (L.map (fun q => chi b (q.1 x))).prod)]
    refine Finset.prod_nonneg (fun x _ => div_nonneg ?_ (by norm_num))
    have h1 : (L.map (fun q => chi false (q.1 x))).prod = 1 := by
      simp [chi]
    have h2 : |(L.map (fun q => chi true (q.1 x))).prod| = 1 := by
      refine abs_list_prod_eq_one _ (fun y hy => ?_)
      obtain ⟨q, -, rfl⟩ := List.mem_map.mp hy
      exact abs_chi _ _
    rw [h1]
    linarith [neg_abs_le ((L.map (fun q => chi true (q.1 x))).prod)]
  · obtain ⟨q, -, rfl⟩ := List.mem_map.mp hy
    have h := abs_cising q.1 η
    have hs := abs_sg q.2
    have : |sg q.2 * cising q.1 η| = 1 := by rw [abs_mul, h, hs, mul_one]
    linarith [neg_abs_le (sg q.2 * cising q.1 η)]

end G2S3

#print axioms G2S3.odd_zero
#print axioms G2S3.radial_site
#print axioms G2S3.gin_circle
#print axioms G2S3.gin_ising
