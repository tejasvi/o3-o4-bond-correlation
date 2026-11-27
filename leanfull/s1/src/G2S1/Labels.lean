/-
G2S1.Labels (stage S1): display (4), the label expansion Z_{G,J} = Σ_ℓ W(ℓ) ∏_e k_{ℓ_e}(J_e) on every finite graph,
absolutely convergent, with |W(ℓ)| ≤ ∏_e d_{ℓ_e}.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 2.2, display (4).
- `hasSum_prod_fintype`: the product over a finite index set of absolutely summable series is the sum over labellings.
-/
import G2S1.Zonal

noncomputable section
open Real Finset MeasureTheory

namespace G2Kernel

/-! ### Products of series over a finite index set -/

/-- (Fin (n+1) → ℕ) ≃ ℕ × (Fin n → ℕ) -/
def consEquivN (n : ℕ) : (Fin (n + 1) → ℕ) ≃ ℕ × (Fin n → ℕ) where
  toFun ℓ := (ℓ 0, Fin.tail ℓ)
  invFun p := Fin.cons p.1 p.2
  left_inv ℓ := Fin.cons_self_tail ℓ
  right_inv p := by
    rcases p with ⟨a, t⟩
    simp only [Fin.cons_zero, Fin.tail_cons]

theorem consEquivN_apply (n : ℕ) (ℓ : Fin (n + 1) → ℕ) : consEquivN n ℓ = (ℓ 0, Fin.tail ℓ) := rfl

theorem hasSum_prod_fin (n : ℕ) : ∀ (f : Fin n → ℕ → ℝ) (s : Fin n → ℝ), (∀ i, HasSum (f i) (s i)) →
    (∀ i, Summable (fun k => ‖f i k‖)) →
    HasSum (fun ℓ : Fin n → ℕ => ∏ i, f i (ℓ i)) (∏ i, s i) ∧
      Summable (fun ℓ : Fin n → ℕ => ‖∏ i, f i (ℓ i)‖) := by
  induction n with
  | zero =>
    intro f s _ _
    refine ⟨?_, (hasSum_unique (fun ℓ : Fin 0 → ℕ => ‖∏ i, f i (ℓ i)‖)).summable⟩
    simp
  | succ n ih =>
    intro f s hf hfa
    have ih' : HasSum (fun ℓ : Fin n → ℕ => ∏ i : Fin n, f i.succ (ℓ i)) (∏ i : Fin n, s i.succ) ∧
        Summable (fun ℓ : Fin n → ℕ => ‖∏ i : Fin n, f i.succ (ℓ i)‖) :=
      ih (fun i => f i.succ) (fun i => s i.succ) (fun i => hf i.succ) (fun i => hfa i.succ)
    obtain ⟨ih1, ih2⟩ := ih'
    have hg : HasSum (fun p : ℕ × (Fin n → ℕ) => f 0 p.1 * ∏ i : Fin n, f i.succ (p.2 i))
        (s 0 * ∏ i : Fin n, s i.succ) :=
      HasSum.mul (f := f 0) (g := fun ℓ : Fin n → ℕ => ∏ i : Fin n, f i.succ (ℓ i)) (hf 0) ih1
        (summable_mul_of_summable_norm (f := f 0) (g := fun ℓ : Fin n → ℕ => ∏ i : Fin n, f i.succ (ℓ i))
          (hfa 0) ih2)
    have hgn : Summable (fun p : ℕ × (Fin n → ℕ) => ‖f 0 p.1 * ∏ i : Fin n, f i.succ (p.2 i)‖) := by
      have h := Summable.mul_of_nonneg (f := fun k => ‖f 0 k‖)
        (g := fun ℓ : Fin n → ℕ => ‖∏ i : Fin n, f i.succ (ℓ i)‖) (hfa 0) ih2
        (fun _ => norm_nonneg _) (fun _ => norm_nonneg _)
      refine h.congr (fun p => ?_)
      rw [norm_mul]
    have hcomp : ∀ ℓ : Fin (n + 1) → ℕ,
        ∏ i, f i (ℓ i) = f 0 (consEquivN n ℓ).1 * ∏ i : Fin n, f i.succ ((consEquivN n ℓ).2 i) := by
      intro ℓ
      rw [Fin.prod_univ_succ, consEquivN_apply]
      simp only [Fin.tail]
    have hs : ∏ i, s i = s 0 * ∏ i : Fin n, s i.succ := Fin.prod_univ_succ s
    constructor
    · rw [hs]
      exact ((consEquivN n).hasSum_iff.mpr hg).congr_fun hcomp
    · refine ((consEquivN n).summable_iff.mpr hgn).congr (fun ℓ => ?_)
      simp only [Function.comp]
      rw [hcomp ℓ]

theorem hasSum_prod_fintype {ι : Type*} [Fintype ι] (f : ι → ℕ → ℝ) (s : ι → ℝ) (hf : ∀ i, HasSum (f i) (s i))
    (hfa : ∀ i, Summable (fun k => ‖f i k‖)) :
    HasSum (fun ℓ : ι → ℕ => ∏ i, f i (ℓ i)) (∏ i, s i) ∧ Summable (fun ℓ : ι → ℕ => ‖∏ i, f i (ℓ i)‖) := by
  set e := Fintype.equivFin ι
  obtain ⟨h1, h2⟩ := hasSum_prod_fin (Fintype.card ι) (fun j => f (e.symm j)) (fun j => s (e.symm j))
    (fun j => hf (e.symm j)) (fun j => hfa (e.symm j))
  set E : (ι → ℕ) ≃ (Fin (Fintype.card ι) → ℕ) := e.arrowCongr (Equiv.refl ℕ)
  have hcomp : ∀ ℓ : ι → ℕ, ∏ i, f i (ℓ i) = ∏ j, f (e.symm j) (E ℓ j) := by
    intro ℓ
    simp only [E, Equiv.arrowCongr_apply, Equiv.coe_refl, Function.comp, id]
    exact (Fintype.prod_equiv e.symm _ _ (fun j => rfl)).symm
  have hs : ∏ i, s i = ∏ j, s (e.symm j) := (Fintype.prod_equiv e.symm _ _ (fun j => rfl)).symm
  constructor
  · rw [hs]
    exact (E.hasSum_iff.mpr h1).congr_fun hcomp
  · refine (E.summable_iff.mpr h2).congr (fun ℓ => ?_)
    simp only [Function.comp]
    rw [hcomp ℓ]

/-! ### The label weights -/

variable {V : Type*} [Fintype V] [DecidableEq V]

omit [Fintype V] [DecidableEq V] in

/-- W(ℓ) = ∫ ∏_{xy ∈ E} Π_{ℓ_xy}(σ_x, σ_y) ∏_x ω(dσ_x) -/
def labelWeight (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (ℓ : G.edgeFinset → ℕ) : ℝ :=
  ∫ σ, ∏ e : G.edgeFinset, (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 V) σ)) ∂(freeMeasure N V)

theorem abs_bond_le' {N : ℕ} (e : Sym2 V) (σ : Config N V) : |bond e σ| ≤ 1 := abs_bond_le e σ

omit [Fintype V] [DecidableEq V] in
theorem abs_zon_bond_le {N : ℕ} (hN : 2 ≤ N) (l : ℕ) (e : Sym2 V) (σ : Config N V) :
    |dConc N l * CConc N l (bond e σ)| ≤ dConc N l := by
  rw [abs_mul, abs_of_pos (dConc_pos_S1 hN l)]
  have h := abs_CConc_le_one hN l (abs_le.mp (abs_bond_le e σ))
  have hd := dConc_pos_S1 hN l
  calc dConc N l * |CConc N l (bond e σ)| ≤ dConc N l * 1 := mul_le_mul_of_nonneg_left h hd.le
    _ = dConc N l := mul_one _

omit [Fintype V] [DecidableEq V] in
theorem measurable_zon_bond {N : ℕ} (l : ℕ) (e : Sym2 V) :
    Measurable (fun σ : Config N V => dConc N l * CConc N l (bond e σ)) :=
  measurable_const.mul ((continuous_CConc N l).measurable.comp (measurable_bond e))

theorem freeMeasure_isProb {N : ℕ} (hN : 1 ≤ N) (W : Type*) [Fintype W] :
    IsProbabilityMeasure (freeMeasure N W) := by
  have := omega_isProbabilityMeasure N (by omega)
  unfold freeMeasure
  infer_instance

theorem abs_labelWeight_le {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj]
    (ℓ : G.edgeFinset → ℕ) : |labelWeight N G ℓ| ≤ ∏ e : G.edgeFinset, dConc N (ℓ e) := by
  have := freeMeasure_isProb (N := N) (by omega) V
  have hb : ∀ σ : Config N V, ‖∏ e : G.edgeFinset, (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 V) σ))‖
      ≤ ∏ e : G.edgeFinset, dConc N (ℓ e) := by
    intro σ
    rw [Real.norm_eq_abs, Finset.abs_prod]
    exact Finset.prod_le_prod₀ (fun e _ => abs_nonneg _) (fun e _ => abs_zon_bond_le hN (ℓ e) e σ)
  have h := norm_integral_le_of_norm_le_const (μ := freeMeasure N V) (Filter.Eventually.of_forall hb)
  rw [Real.norm_eq_abs] at h
  unfold labelWeight
  have hu : (freeMeasure N V).real Set.univ = 1 := by simp
  rw [hu, mul_one] at h
  exact h

/-- the pointwise expansion of the Gibbs weight over labellings -/
theorem gibbs_hasSum_labels {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (σ : Config N V) :
    HasSum (fun ℓ : G.edgeFinset → ℕ =>
      ∏ e : G.edgeFinset, (kConc N (ℓ e) (J e) * (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 V) σ))))
      (Real.exp (energy G J σ)) := by
  have h := (hasSum_prod_fintype (fun (e : G.edgeFinset) (a : ℕ) => kConc N a (J e) * zon N a (bond (e : Sym2 V) σ))
    (fun (e : G.edgeFinset) => Real.exp (J e * bond (e : Sym2 V) σ))
    (fun e => exp_hasSum_zon hN (J e) _ (abs_bond_le _ σ))
    (fun e => by
      refine Summable.of_nonneg_of_le (fun c => norm_nonneg _) (fun c => ?_) (summable_kConc_dConc hN (J e))
      rw [Real.norm_eq_abs, abs_mul]
      exact mul_le_mul_of_nonneg_left (abs_zon_bond_le hN c _ σ) (abs_nonneg _))).1
  have he : ∏ e : G.edgeFinset, Real.exp (J e * bond (e : Sym2 V) σ) = Real.exp (energy G J σ) := by
    unfold energy
    rw [Real.exp_sum]
    exact Finset.prod_coe_sort G.edgeFinset (fun x => Real.exp (J x * bond x σ))
  rw [he] at h
  exact h

theorem summable_labelBound {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    Summable (fun ℓ : G.edgeFinset → ℕ => ∏ e : G.edgeFinset, (|kConc N (ℓ e) (J e)| * dConc N (ℓ e))) := by
  have h := (hasSum_prod_fintype (fun (e : G.edgeFinset) (a : ℕ) => |kConc N a (J e)| * dConc N a)
    (fun (e : G.edgeFinset) => ∑' a, |kConc N a (J e)| * dConc N a)
    (fun e => (summable_kConc_dConc hN (J e)).hasSum)
    (fun e => by
      refine (summable_kConc_dConc hN (J e)).congr (fun c => ?_)
      rw [Real.norm_eq_abs, abs_mul, abs_abs, abs_of_pos (dConc_pos_S1 hN c)])).1
  exact h.summable

theorem labelTerm_abs_le {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (ℓ : G.edgeFinset → ℕ) (σ : Config N V) :
    |∏ e : G.edgeFinset, (kConc N (ℓ e) (J e) * (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 V) σ)))|
      ≤ ∏ e : G.edgeFinset, (|kConc N (ℓ e) (J e)| * dConc N (ℓ e)) := by
  rw [Finset.abs_prod]
  refine Finset.prod_le_prod₀ (fun e _ => abs_nonneg _) (fun e _ => ?_)
  rw [abs_mul]
  exact mul_le_mul_of_nonneg_left (abs_zon_bond_le hN (ℓ e) e σ) (abs_nonneg _)

theorem measurable_labelTerm {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (ℓ : G.edgeFinset → ℕ) :
    Measurable (fun σ : Config N V =>
      ∏ e : G.edgeFinset, (kConc N (ℓ e) (J e) * (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 V) σ)))) :=
  Finset.measurable_fun_prod _ (fun e _ => measurable_const.mul (measurable_zon_bond (ℓ e) (e : Sym2 V)))

theorem labelTerm_hasSum_integral {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) :
    HasSum (fun ℓ : G.edgeFinset → ℕ => ∫ σ, ∏ e : G.edgeFinset,
        (kConc N (ℓ e) (J e) * (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 V) σ))) ∂(freeMeasure N V))
      (∫ σ, Real.exp (energy G J σ) ∂(freeMeasure N V)) := by
  have hfm := freeMeasure_isProb (N := N) (by omega) V
  have h3 := summable_labelBound hN G J
  have h4 := gibbs_hasSum_labels hN G J
  have h5 : ∀ ℓ : G.edgeFinset → ℕ, AEStronglyMeasurable (fun σ : Config N V => ∏ e : G.edgeFinset,
      (kConc N (ℓ e) (J e) * (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 V) σ)))) (freeMeasure N V) :=
    fun ℓ => (measurable_labelTerm G J ℓ).aestronglyMeasurable
  have h6 : ∀ (ℓ : G.edgeFinset → ℕ) (σ : Config N V), |∏ e : G.edgeFinset,
      (kConc N (ℓ e) (J e) * (dConc N (ℓ e) * CConc N (ℓ e) (bond (e : Sym2 V) σ)))|
        ≤ ∏ e : G.edgeFinset, (|kConc N (ℓ e) (J e)| * dConc N (ℓ e)) :=
    fun ℓ σ => labelTerm_abs_le hN G J ℓ σ
  exact hasSum_integral_of_bound _ _ _ h5 h6 h3 h4

/-- display (4): Z_{G,J} = Σ_ℓ W(ℓ) ∏_e k_{ℓ_e}(J_e), absolutely convergent -/
theorem partition_hasSum_labels {N : ℕ} (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) :
    HasSum (fun ℓ : G.edgeFinset → ℕ => labelWeight N G ℓ * ∏ e : G.edgeFinset, kConc N (ℓ e) (J e))
      (partition N G J) := by
  have hS := labelTerm_hasSum_integral hN G J
  unfold partition
  refine hS.congr_fun (fun ℓ => ?_)
  unfold labelWeight
  rw [← integral_mul_const]
  congr 1
  funext σ
  rw [← Finset.prod_mul_distrib]
  exact Finset.prod_congr rfl (fun e _ => by ring)

end G2Kernel
