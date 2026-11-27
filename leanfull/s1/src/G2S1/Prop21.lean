/-
G2S1.Prop21 (stage S1): Proposition 2.1 in the paper's general signed form.
For edges e ≠ f with J_e, J_f > 0: Cov(s_e, s_f) = ∂_{J_e} ∂_{J_f} log Z_{G,J} = Cov_p(r_{ℓ_e}(J_e), r_{ℓ_f}(J_f)), p the signed
label weight p(ℓ) = W(ℓ) ∏_g k_{ℓ_g}(J_g) / Z_{G,J} of display (4).
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Proposition 2.1.
- `labelCov_gen`: the second equality for a single-label series with a countable index set and signed weights (the
  package's `labelCov_thm` has weights u ≥ 0 indexed by ℕ); termwise differentiation (`hasDerivAt_tsum_of_isPreconnected`).
- `prop21`: the package's `covDeriv_thm` (first equality), display (4) for the updated couplings, and `labelCov_gen`.
-/
import G2S1.CycleZ

noncomputable section
open Real Finset MeasureTheory Filter Topology

namespace G2Kernel

/-! ### The second equality for a signed single-label series -/

theorem norm_triple_le_abs {u X Y X' Y' M : ℝ} (hX : |X| ≤ X') (hY : |Y| ≤ Y')
    (h : |u| * X' * Y' ≤ M) : ‖u * X * Y‖ ≤ M := by
  rw [Real.norm_eq_abs, abs_mul, abs_mul]
  refine le_trans ?_ h
  exact mul_le_mul (mul_le_mul_of_nonneg_left hX (abs_nonneg u)) hY (abs_nonneg _)
    (mul_nonneg (abs_nonneg u) ((abs_nonneg _).trans hX))

theorem labelCov_gen {ι : Type*} (u : ι → ℝ) (ka kb : ι → ℝ → ℝ) (a0 b0 δ : ℝ) (M : ι → ℝ)
    (hδ : 0 < δ) (hka : ∀ c, Differentiable ℝ (ka c)) (hkb : ∀ c, Differentiable ℝ (kb c)) (hM : Summable M)
    (hbd : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      |u c| * (|ka c x| + |deriv (ka c) x|) * (|kb c y| + |deriv (kb c) y|) ≤ M c)
    (hpos : ∀ a ∈ Set.Ioo (a0 - δ) (a0 + δ), 0 < ∑' c, u c * ka c a * kb c b0) :
    deriv (fun a => deriv (fun b => Real.log (∑' c, u c * ka c a * kb c b)) b0) a0
      = ((∑' c, u c * deriv (ka c) a0 * deriv (kb c) b0) * (∑' c, u c * ka c a0 * kb c b0)
          - (∑' c, u c * ka c a0 * deriv (kb c) b0) * (∑' c, u c * deriv (ka c) a0 * kb c b0))
        / (∑' c, u c * ka c a0 * kb c b0) ^ 2 := by
  have s1 : ∀ (X Y : ℝ), |X| ≤ |X| + |Y| := fun X Y => by have := abs_nonneg Y; linarith
  have s2 : ∀ (X Y : ℝ), |Y| ≤ |X| + |Y| := fun X Y => by have := abs_nonneg X; linarith
  have B00 : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      ‖u c * ka c x * kb c y‖ ≤ M c :=
    fun c x hx y hy => norm_triple_le_abs (s1 _ _) (s1 _ _) (hbd c x hx y hy)
  have B01 : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      ‖u c * ka c x * deriv (kb c) y‖ ≤ M c :=
    fun c x hx y hy => norm_triple_le_abs (s1 _ _) (s2 _ _) (hbd c x hx y hy)
  have B10 : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      ‖u c * deriv (ka c) x * kb c y‖ ≤ M c :=
    fun c x hx y hy => norm_triple_le_abs (s2 _ _) (s1 _ _) (hbd c x hx y hy)
  have B11 : ∀ c, ∀ x ∈ Set.Icc (a0 - δ) (a0 + δ), ∀ y ∈ Set.Icc (b0 - δ) (b0 + δ),
      ‖u c * deriv (ka c) x * deriv (kb c) y‖ ≤ M c :=
    fun c x hx y hy => norm_triple_le_abs (s2 _ _) (s2 _ _) (hbd c x hx y hy)
  have ha0I : a0 ∈ Set.Ioo (a0 - δ) (a0 + δ) := ⟨by linarith, by linarith⟩
  have hb0I : b0 ∈ Set.Ioo (b0 - δ) (b0 + δ) := ⟨by linarith, by linarith⟩
  have ha0C : a0 ∈ Set.Icc (a0 - δ) (a0 + δ) := Set.Ioo_subset_Icc_self ha0I
  have hb0C : b0 ∈ Set.Icc (b0 - δ) (b0 + δ) := Set.Ioo_subset_Icc_self hb0I
  have hinner : ∀ a ∈ Set.Ioo (a0 - δ) (a0 + δ),
      HasDerivAt (fun b => ∑' c, u c * ka c a * kb c b) (∑' c, u c * ka c a * deriv (kb c) b0) b0 := by
    intro a ha
    exact hasDerivAt_tsum_of_isPreconnected (u := M) (g := fun c b => u c * ka c a * kb c b)
      (g' := fun c b => u c * ka c a * deriv (kb c) b) hM isOpen_Ioo isPreconnected_Ioo
      (fun c y _ => ((hkb c y).hasDerivAt).const_mul (u c * ka c a))
      (fun c y hy => B01 c a (Set.Ioo_subset_Icc_self ha) y (Set.Ioo_subset_Icc_self hy)) hb0I
      (Summable.of_norm_bounded hM fun c => B00 c a (Set.Ioo_subset_Icc_self ha) b0 hb0C) hb0I
  have hev : (fun a => deriv (fun b => Real.log (∑' c, u c * ka c a * kb c b)) b0) =ᶠ[𝓝 a0]
      fun a => (∑' c, u c * ka c a * deriv (kb c) b0) / ∑' c, u c * ka c a * kb c b0 := by
    filter_upwards [Ioo_mem_nhds (show a0 - δ < a0 by linarith) (show a0 < a0 + δ by linarith)] with a ha
    exact ((hinner a ha).log (hpos a ha).ne').deriv
  rw [hev.deriv_eq]
  have hP : HasDerivAt (fun a => ∑' c, u c * ka c a * deriv (kb c) b0)
      (∑' c, u c * deriv (ka c) a0 * deriv (kb c) b0) a0 :=
    hasDerivAt_tsum_of_isPreconnected (u := M) (g := fun c a => u c * ka c a * deriv (kb c) b0)
      (g' := fun c a => u c * deriv (ka c) a * deriv (kb c) b0) hM isOpen_Ioo isPreconnected_Ioo
      (fun c x _ => (((hka c x).hasDerivAt).const_mul (u c)).mul_const (deriv (kb c) b0))
      (fun c x hx => B11 c x (Set.Ioo_subset_Icc_self hx) b0 hb0C) ha0I
      (Summable.of_norm_bounded hM fun c => B01 c a0 ha0C b0 hb0C) ha0I
  have hQ : HasDerivAt (fun a => ∑' c, u c * ka c a * kb c b0)
      (∑' c, u c * deriv (ka c) a0 * kb c b0) a0 :=
    hasDerivAt_tsum_of_isPreconnected (u := M) (g := fun c a => u c * ka c a * kb c b0)
      (g' := fun c a => u c * deriv (ka c) a * kb c b0) hM isOpen_Ioo isPreconnected_Ioo
      (fun c x _ => (((hka c x).hasDerivAt).const_mul (u c)).mul_const (kb c b0))
      (fun c x hx => B10 c x (Set.Ioo_subset_Icc_self hx) b0 hb0C) ha0I
      (Summable.of_norm_bounded hM fun c => B00 c a0 ha0C b0 hb0C) ha0I
  rw [(hP.fun_div hQ (hpos a0 ha0I).ne').deriv]

/-! ### The data of Proposition 2.1 -/

variable {V : Type} [Fintype V] [DecidableEq V]

/-- the signed label weight p(ℓ) = W(ℓ) ∏_e k_{ℓ_e}(J_e) / Z_{G,J} -/
def labelLaw (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (ℓ : G.edgeFinset → ℕ) : ℝ :=
  labelWeight N G ℓ * (∏ e : G.edgeFinset, kConc N (ℓ e) (J e)) / partition N G J

/-- r_ℓ(J) = ∂_J log k_ℓ(J) -/
def rRate (N l : ℕ) (J : ℝ) : ℝ := deriv (kConc N l) J / kConc N l J

/-- Cov_p(r_{ℓ_e}(J_e), r_{ℓ_f}(J_f)) -/
def covLabel (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) : ℝ :=
  (∑' ℓ, labelLaw N G J ℓ * (rRate N (ℓ e) (J e) * rRate N (ℓ f) (J f)))
    - (∑' ℓ, labelLaw N G J ℓ * rRate N (ℓ e) (J e)) * (∑' ℓ, labelLaw N G J ℓ * rRate N (ℓ f) (J f))

theorem hasSum_labelLaw {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    HasSum (labelLaw N G J) 1 := by
  have hZ := partition_pos (N := N) (by omega) G J
  have h := (partition_hasSum_labels hN G J).div_const (partition N G J)
  rw [div_self hZ.ne'] at h
  exact h

/-- ∏_g F g = F e · F f · ∏_{g ≠ e, f} F g -/
theorem prod_split_ef {E : Type*} [Fintype E] [DecidableEq E] (e f : E) (hef : e ≠ f) (F : E → ℝ) :
    ∏ g, F g = F e * F f * ∏ g ∈ (univ.erase e).erase f, F g := by
  rw [← Finset.mul_prod_erase univ F (mem_univ e),
    ← Finset.mul_prod_erase (univ.erase e) F (mem_erase.mpr ⟨hef.symm, mem_univ f⟩)]
  ring

/-- the weight of a label with the factors of e and f removed -/
def labelU (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (ℓ : G.edgeFinset → ℕ) : ℝ :=
  labelWeight N G ℓ * ∏ g ∈ (univ.erase e).erase f, kConc N (ℓ g) (J g)

theorem prod_update_split (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (hef : e ≠ f) (a b : ℝ) (k : ℕ → ℝ → ℝ) (ℓ : G.edgeFinset → ℕ) :
    ∏ g : G.edgeFinset, k (ℓ g) (Function.update (Function.update J (e : Sym2 V) a) (f : Sym2 V) b g)
      = k (ℓ e) a * k (ℓ f) b * ∏ g ∈ (univ.erase e).erase f, k (ℓ g) (J g) := by
  have hef' : (e : Sym2 V) ≠ (f : Sym2 V) := fun h => hef (Subtype.ext h)
  rw [prod_split_ef e f hef]
  congr 1
  · rw [Function.update_of_ne hef', Function.update_self, Function.update_self]
  · refine Finset.prod_congr rfl (fun g hg => ?_)
    have hgf : g ≠ f := (mem_erase.mp hg).1
    have hge : g ≠ e := (mem_erase.mp (mem_erase.mp hg).2).1
    rw [Function.update_of_ne (fun h => hgf (Subtype.ext h)), Function.update_of_ne (fun h => hge (Subtype.ext h))]

theorem partition_update_tsum {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (e f : G.edgeFinset) (hef : e ≠ f) (a b : ℝ) :
    partition N G (Function.update (Function.update J (e : Sym2 V) a) (f : Sym2 V) b)
      = ∑' ℓ, labelU N G J e f ℓ * kConc N (ℓ e) a * kConc N (ℓ f) b := by
  rw [← (partition_hasSum_labels hN G _).tsum_eq]
  congr 1
  funext ℓ
  rw [prod_update_split G J e f hef a b (kConc N) ℓ]
  unfold labelU
  ring

/-! ### Bounds on a box around (J_e, J_f) -/

theorem kConc_box_bound {N : ℕ} (hN : 2 ≤ N) {lo hi : ℝ} (hlo : 0 < lo) (hle : lo ≤ hi) :
    ∃ c, 0 < c ∧ ∀ n : ℕ, ∀ x ∈ Set.Icc lo hi,
      |kConc N n x| + |deriv (kConc N n) x| ≤ c * ((n : ℝ) + 2) * (hi / 2) ^ n / (n.factorial : ℝ) := by
  obtain ⟨c, hc, hb⟩ := (hKReg_kConc N hN).2.2 lo hi hlo hle
  refine ⟨c, hc, fun n x hx => ?_⟩
  obtain ⟨h0, h1, _⟩ := hb n x hx
  have hx0 : 0 < x := lt_of_lt_of_le hlo hx.1
  have hpow : (x / 2) ^ n ≤ (hi / 2) ^ n := pow_le_pow_left₀ (by positivity) (by linarith [hx.2]) n
  have hnf : (0 : ℝ) < (n.factorial : ℝ) := by exact_mod_cast n.factorial_pos
  have e1 : c * (x / 2) ^ n / (n.factorial : ℝ) ≤ c * (hi / 2) ^ n / (n.factorial : ℝ) := by
    apply div_le_div_of_nonneg_right _ hnf.le
    exact mul_le_mul_of_nonneg_left hpow hc.le
  have e2 : c * ((n : ℝ) + 1) * (x / 2) ^ n / (n.factorial : ℝ) ≤ c * ((n : ℝ) + 1) * (hi / 2) ^ n / (n.factorial : ℝ) := by
    apply div_le_div_of_nonneg_right _ hnf.le
    exact mul_le_mul_of_nonneg_left hpow (by positivity)
  calc |kConc N n x| + |deriv (kConc N n) x|
      ≤ c * (hi / 2) ^ n / (n.factorial : ℝ) + c * ((n : ℝ) + 1) * (hi / 2) ^ n / (n.factorial : ℝ) :=
        add_le_add (h0.trans e1) (h1.trans e2)
    _ = c * ((n : ℝ) + 2) * (hi / 2) ^ n / (n.factorial : ℝ) := by ring

theorem summable_box_bound {N : ℕ} (hN : 2 ≤ N) {c hi : ℝ} (hc : 0 ≤ c) (hhi : 0 ≤ hi) :
    Summable (fun n : ℕ => dConc N n * (c * ((n : ℝ) + 2) * (hi / 2) ^ n / (n.factorial : ℝ))) := by
  refine Summable.of_nonneg_of_le (fun n => mul_nonneg (dConc_pos_S1 hN n).le (by positivity)) (fun n => ?_)
    ((summable_poly_pow_div_factorial (N + 1) (show (0 : ℝ) ≤ hi / 2 by positivity)).mul_left (2 * c))
  have hd := dConc_le_pow hN n
  have hnf : (0 : ℝ) < (n.factorial : ℝ) := by exact_mod_cast n.factorial_pos
  have h2 : ((n : ℝ) + 2) ≤ 2 * ((n : ℝ) + 1) := by linarith [(Nat.cast_nonneg n : (0 : ℝ) ≤ n)]
  have hA : 0 ≤ c * (hi / 2) ^ n / (n.factorial : ℝ) := by positivity
  calc dConc N n * (c * ((n : ℝ) + 2) * (hi / 2) ^ n / (n.factorial : ℝ))
      = (dConc N n * ((n : ℝ) + 2)) * (c * (hi / 2) ^ n / (n.factorial : ℝ)) := by ring
    _ ≤ (((n : ℝ) + 1) ^ N * (2 * ((n : ℝ) + 1))) * (c * (hi / 2) ^ n / (n.factorial : ℝ)) := by
        apply mul_le_mul_of_nonneg_right _ hA
        exact mul_le_mul hd h2 (by positivity) (by positivity)
    _ = 2 * c * (((n : ℝ) + 1) ^ (N + 1) * (hi / 2) ^ n / (n.factorial : ℝ)) := by ring

/-- the factor bounds: e and f by the box bound, the other edges by |k| d -/
def boxB (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (c hi : ℝ)
    (g : G.edgeFinset) (n : ℕ) : ℝ :=
  if g = e ∨ g = f then dConc N n * (c * ((n : ℝ) + 2) * (hi / 2) ^ n / (n.factorial : ℝ))
  else |kConc N n (J g)| * dConc N n

theorem boxB_nonneg {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : G.edgeFinset) {c hi : ℝ} (hc : 0 ≤ c) (hhi : 0 ≤ hi) (g : G.edgeFinset) (n : ℕ) :
    0 ≤ boxB N G J e f c hi g n := by
  unfold boxB
  split_ifs
  · exact mul_nonneg (dConc_pos_S1 hN n).le (by positivity)
  · exact mul_nonneg (abs_nonneg _) (dConc_pos_S1 hN n).le

theorem summable_boxB_prod {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : G.edgeFinset) {c hi : ℝ} (hc : 0 ≤ c) (hhi : 0 ≤ hi) :
    Summable (fun ℓ : G.edgeFinset → ℕ => ∏ g, boxB N G J e f c hi g (ℓ g)) := by
  have hs : ∀ g, Summable (boxB N G J e f c hi g) := by
    intro g
    unfold boxB
    by_cases h : g = e ∨ g = f
    · simp only [if_pos h]; exact summable_box_bound hN hc hhi
    · simp only [if_neg h]; exact summable_kConc_dConc hN (J g)
  have h := (hasSum_prod_fintype (boxB N G J e f c hi) (fun g => ∑' n, boxB N G J e f c hi g n)
    (fun g => (hs g).hasSum)
    (fun g => (hs g).congr (fun n => by rw [Real.norm_eq_abs, abs_of_nonneg (boxB_nonneg hN G J e f hc hhi g n)]))).1
  exact h.summable

theorem labelU_box_bound {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : G.edgeFinset) (hef : e ≠ f) {c hi : ℝ} (hc : 0 ≤ c) (hhi : 0 ≤ hi)
    (ℓ : G.edgeFinset → ℕ) (x y : ℝ)
    (hx : |kConc N (ℓ e) x| + |deriv (kConc N (ℓ e)) x| ≤ c * ((ℓ e : ℝ) + 2) * (hi / 2) ^ (ℓ e) / ((ℓ e).factorial : ℝ))
    (hy : |kConc N (ℓ f) y| + |deriv (kConc N (ℓ f)) y| ≤ c * ((ℓ f : ℝ) + 2) * (hi / 2) ^ (ℓ f) / ((ℓ f).factorial : ℝ)) :
    |labelU N G J e f ℓ| * (|kConc N (ℓ e) x| + |deriv (kConc N (ℓ e)) x|) *
      (|kConc N (ℓ f) y| + |deriv (kConc N (ℓ f)) y|) ≤ ∏ g, boxB N G J e f c hi g (ℓ g) := by
  have hW := abs_labelWeight_le hN G ℓ
  rw [prod_split_ef e f hef (fun g => dConc N (ℓ g))] at hW
  rw [prod_split_ef e f hef (fun g => boxB N G J e f c hi g (ℓ g))]
  have hBe : boxB N G J e f c hi e (ℓ e)
      = dConc N (ℓ e) * (c * ((ℓ e : ℝ) + 2) * (hi / 2) ^ (ℓ e) / ((ℓ e).factorial : ℝ)) := by
    unfold boxB; rw [if_pos (Or.inl rfl)]
  have hBf : boxB N G J e f c hi f (ℓ f)
      = dConc N (ℓ f) * (c * ((ℓ f : ℝ) + 2) * (hi / 2) ^ (ℓ f) / ((ℓ f).factorial : ℝ)) := by
    unfold boxB; rw [if_pos (Or.inr rfl)]
  have hBr : ∏ g ∈ (univ.erase e).erase f, boxB N G J e f c hi g (ℓ g)
      = ∏ g ∈ (univ.erase e).erase f, (|kConc N (ℓ g) (J g)| * dConc N (ℓ g)) := by
    refine Finset.prod_congr rfl (fun g hg => ?_)
    have hgf : g ≠ f := (mem_erase.mp hg).1
    have hge : g ≠ e := (mem_erase.mp (mem_erase.mp hg).2).1
    unfold boxB
    rw [if_neg (fun h => h.elim hge hgf)]
  rw [hBe, hBf, hBr]
  have hU : |labelU N G J e f ℓ| ≤ dConc N (ℓ e) * dConc N (ℓ f) *
      ∏ g ∈ (univ.erase e).erase f, (|kConc N (ℓ g) (J g)| * dConc N (ℓ g)) := by
    unfold labelU
    rw [abs_mul, Finset.abs_prod, Finset.prod_mul_distrib]
    have hp1 : 0 ≤ ∏ g ∈ (univ.erase e).erase f, |kConc N (ℓ g) (J g)| := Finset.prod_nonneg (fun g _ => abs_nonneg _)
    calc |labelWeight N G ℓ| * ∏ g ∈ (univ.erase e).erase f, |kConc N (ℓ g) (J g)|
        ≤ (dConc N (ℓ e) * dConc N (ℓ f) * ∏ g ∈ (univ.erase e).erase f, dConc N (ℓ g)) *
            ∏ g ∈ (univ.erase e).erase f, |kConc N (ℓ g) (J g)| := mul_le_mul_of_nonneg_right hW hp1
      _ = _ := by ring
  have hd1 := (dConc_pos_S1 hN (ℓ e)).le
  have hd2 := (dConc_pos_S1 hN (ℓ f)).le
  have hr : 0 ≤ ∏ g ∈ (univ.erase e).erase f, (|kConc N (ℓ g) (J g)| * dConc N (ℓ g)) :=
    Finset.prod_nonneg (fun g _ => mul_nonneg (abs_nonneg _) (dConc_pos_S1 hN _).le)
  have hX : 0 ≤ |kConc N (ℓ e) x| + |deriv (kConc N (ℓ e)) x| := by positivity
  have hY : 0 ≤ |kConc N (ℓ f) y| + |deriv (kConc N (ℓ f)) y| := by positivity
  calc |labelU N G J e f ℓ| * (|kConc N (ℓ e) x| + |deriv (kConc N (ℓ e)) x|) *
        (|kConc N (ℓ f) y| + |deriv (kConc N (ℓ f)) y|)
      ≤ (dConc N (ℓ e) * dConc N (ℓ f) * ∏ g ∈ (univ.erase e).erase f, (|kConc N (ℓ g) (J g)| * dConc N (ℓ g))) *
          (c * ((ℓ e : ℝ) + 2) * (hi / 2) ^ (ℓ e) / ((ℓ e).factorial : ℝ)) *
          (c * ((ℓ f : ℝ) + 2) * (hi / 2) ^ (ℓ f) / ((ℓ f).factorial : ℝ)) := by
        have hb1 : 0 ≤ c * ((ℓ e : ℝ) + 2) * (hi / 2) ^ (ℓ e) / ((ℓ e).factorial : ℝ) := by positivity
        exact mul_le_mul (mul_le_mul hU hx hX (mul_nonneg (mul_nonneg hd1 hd2) hr)) hy hY
          (mul_nonneg (mul_nonneg (mul_nonneg hd1 hd2) hr) hb1)
    _ = _ := by ring

theorem differentiable_kConc {N : ℕ} (hN : 2 ≤ N) (l : ℕ) : Differentiable ℝ (kConc N l) :=
  ((contDiff_kConc hN l).of_le one_le_two).differentiable one_ne_zero

theorem labelLaw_eq {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (hef : e ≠ f) (ℓ : G.edgeFinset → ℕ) :
    labelLaw N G J ℓ = labelU N G J e f ℓ * kConc N (ℓ e) (J e) * kConc N (ℓ f) (J f) / partition N G J := by
  unfold labelLaw labelU
  rw [prod_split_ef e f hef (fun g => kConc N (ℓ g) (J g))]
  ring

/-- **Proposition 2.1** (general signed form): for edges e ≠ f with J_e, J_f > 0,
Cov(s_e, s_f) = ∂_{J_e} ∂_{J_f} log Z_{G,J} = Cov_p(r_{ℓ_e}(J_e), r_{ℓ_f}(J_f)) -/
theorem prop21 (N : ℕ) (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : G.edgeFinset) (hef : e ≠ f) (hJe : 0 < J e) (hJf : 0 < J f) :
    gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V))
        = deriv (fun a => deriv (fun b => Real.log (partition N G
            (Function.update (Function.update J (e : Sym2 V) a) (f : Sym2 V) b))) (J f)) (J e) ∧
    gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V)) = covLabel N G J e f := by
  have he : (e : Sym2 V) ∈ G.edgeSet := G.mem_edgeFinset.mp e.2
  have hf : (f : Sym2 V) ∈ G.edgeSet := G.mem_edgeFinset.mp f.2
  have hef' : (e : Sym2 V) ≠ (f : Sym2 V) := fun h => hef (Subtype.ext h)
  have h1 := (covDeriv_thm N V G J e f he hf hef').symm
  refine ⟨h1, h1.trans ?_⟩
  have hZ : ∀ a b, partition N G (Function.update (Function.update J (e : Sym2 V) a) (f : Sym2 V) b)
      = ∑' ℓ, labelU N G J e f ℓ * kConc N (ℓ e) a * kConc N (ℓ f) b := partition_update_tsum hN G J e f hef
  -- the box around (J_e, J_f)
  have hδ : 0 < min (J e) (J f) / 2 := by positivity
  set δ := min (J e) (J f) / 2 with hδdef
  have hmin1 : min (J e) (J f) ≤ J e := min_le_left _ _
  have hmin2 : min (J e) (J f) ≤ J f := min_le_right _ _
  have hmax1 : J e ≤ max (J e) (J f) := le_max_left _ _
  have hmax2 : J f ≤ max (J e) (J f) := le_max_right _ _
  set hi := max (J e) (J f) + δ with hhidef
  have hle : δ ≤ hi := by linarith
  have hhi : 0 ≤ hi := by linarith
  obtain ⟨c, hc, hbox⟩ := kConc_box_bound hN hδ hle
  have hA : ∀ x ∈ Set.Icc (J e - δ) (J e + δ), x ∈ Set.Icc δ hi := fun x hx => ⟨by linarith [hx.1], by linarith [hx.2]⟩
  have hB : ∀ y ∈ Set.Icc (J f - δ) (J f + δ), y ∈ Set.Icc δ hi := fun y hy => ⟨by linarith [hy.1], by linarith [hy.2]⟩
  have hL := labelCov_gen (labelU N G J e f) (fun ℓ => kConc N (ℓ e)) (fun ℓ => kConc N (ℓ f)) (J e) (J f) δ
    (fun ℓ => ∏ g, boxB N G J e f c hi g (ℓ g)) hδ
    (fun ℓ => differentiable_kConc hN (ℓ e)) (fun ℓ => differentiable_kConc hN (ℓ f))
    (summable_boxB_prod hN G J e f hc.le hhi)
    (fun ℓ x hx y hy => labelU_box_bound hN G J e f hef hc.le hhi ℓ x y (hbox _ x (hA x hx)) (hbox _ y (hB y hy)))
    (fun a _ => by
      show 0 < ∑' ℓ, labelU N G J e f ℓ * kConc N (ℓ e) a * kConc N (ℓ f) (J f)
      rw [← hZ a (J f)]
      exact partition_pos (by omega) G _)
  simp only [hZ]
  rw [hL]
  -- the algebra
  have hS : partition N G J = ∑' ℓ, labelU N G J e f ℓ * kConc N (ℓ e) (J e) * kConc N (ℓ f) (J f) := by
    rw [← hZ, Function.update_eq_self, Function.update_eq_self]
  have hSpos : 0 < ∑' ℓ, labelU N G J e f ℓ * kConc N (ℓ e) (J e) * kConc N (ℓ f) (J f) := by
    rw [← hS]; exact partition_pos (by omega) G J
  set S := ∑' ℓ, labelU N G J e f ℓ * kConc N (ℓ e) (J e) * kConc N (ℓ f) (J f) with hSdef
  have hSne : S ≠ 0 := hSpos.ne'
  have hkp : ∀ ℓ : G.edgeFinset → ℕ, kConc N (ℓ e) (J e) ≠ 0 ∧ kConc N (ℓ f) (J f) ≠ 0 :=
    fun ℓ => ⟨(kConc_pos hN (ℓ e) hJe).ne', (kConc_pos hN (ℓ f) hJf).ne'⟩
  have t1 : (∑' ℓ, labelLaw N G J ℓ * (rRate N (ℓ e) (J e) * rRate N (ℓ f) (J f)))
      = (∑' ℓ, labelU N G J e f ℓ * deriv (kConc N (ℓ e)) (J e) * deriv (kConc N (ℓ f)) (J f)) / S := by
    rw [← tsum_div_const]
    congr 1; funext ℓ
    rw [labelLaw_eq G J e f hef ℓ, hS]
    unfold rRate
    obtain ⟨hk1, hk2⟩ := hkp ℓ
    field_simp
  have t2 : (∑' ℓ, labelLaw N G J ℓ * rRate N (ℓ e) (J e))
      = (∑' ℓ, labelU N G J e f ℓ * deriv (kConc N (ℓ e)) (J e) * kConc N (ℓ f) (J f)) / S := by
    rw [← tsum_div_const]
    congr 1; funext ℓ
    rw [labelLaw_eq G J e f hef ℓ, hS]
    unfold rRate
    obtain ⟨hk1, hk2⟩ := hkp ℓ
    field_simp
  have t3 : (∑' ℓ, labelLaw N G J ℓ * rRate N (ℓ f) (J f))
      = (∑' ℓ, labelU N G J e f ℓ * kConc N (ℓ e) (J e) * deriv (kConc N (ℓ f)) (J f)) / S := by
    rw [← tsum_div_const]
    congr 1; funext ℓ
    rw [labelLaw_eq G J e f hef ℓ, hS]
    unfold rRate
    obtain ⟨hk1, hk2⟩ := hkp ℓ
    field_simp
  unfold covLabel
  rw [t1, t2, t3]
  field_simp

end G2Kernel
