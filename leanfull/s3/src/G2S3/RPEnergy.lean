/-
G2S3.RPEnergy (stage S3, Part A3): for a reflection theta of a graph (an involutive automorphism with theta-invariant
couplings) whose only edges between the open half P and theta P are of the form {x, theta x}, the energy splits as
A(s) + A(s o theta) + crossing, with A depending only on the closed half and the crossing term a nonnegative
combination of products u_k(s|P) u_k((s o theta)|P) (edges on the line are split into two halves, as in the paper).
Consequences: reflection positivity of the Gibbs measure, and Cov(s_e, s_{theta e}) >= 0 for every edge e in the
closed half. Paper: Lemma 6.1 (tex l.1726-1738).
-/
import G2S3.RPGraph

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

theorem dot_eq_sum {N : ℕ} (x y : Sph N) :
    dot x y = ∑ i, (x : Amb N) i * (y : Amb N) i := by
  unfold dot
  rw [PiLp.inner_apply]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rw [RCLike.inner_apply, conj_trivial, mul_comm]

theorem abs_coord_le {N : ℕ} (x : Sph N) (i : Fin N) : |(x : Amb N) i| ≤ 1 := by
  have h := PiLp.norm_apply_le (x : Amb N) i
  rw [Real.norm_eq_abs, norm_eq_of_mem_sphere] at h
  exact h

theorem measurable_coord {N : ℕ} {Y : Type*} [MeasurableSpace Y] {f : Y → Sph N} (hf : Measurable f)
    (i : Fin N) : Measurable (fun y => ((f y : Sph N) : Amb N) i) := by
  have hc : Continuous (fun x : Sph N => (x : Amb N) i) :=
    (PiLp.continuous_apply 2 (fun _ : Fin N => ℝ) i).comp continuous_subtype_val
  exact hc.measurable.comp hf

namespace ReflData

variable {V : Type*} [DecidableEq V] (R : ReflData V)

/-- Membership in the closed half, as a decidable proposition. -/
def inS (v : V) : Prop := R.θ v = v ∨ v ∈ R.P

instance (v : V) : Decidable (R.inS v) := by unfold inS; infer_instance

/-- The weight of an edge in the half energy `A`: 1 inside the closed half, 1/2 on the line, 0 otherwise. -/
def wtf (u v : V) : ℝ := if R.inS u ∧ R.inS v then (if R.θ u = u ∧ R.θ v = v then 1 / 2 else 1) else 0

theorem wtf_comm (u v : V) : R.wtf u v = R.wtf v u := by
  unfold wtf
  by_cases h1 : R.inS u ∧ R.inS v
  · have h1' : R.inS v ∧ R.inS u := ⟨h1.2, h1.1⟩
    by_cases h2 : R.θ u = u ∧ R.θ v = v
    · have h2' : R.θ v = v ∧ R.θ u = u := ⟨h2.2, h2.1⟩
      simp [h1, h1', h2, h2']
    · have h2' : ¬ (R.θ v = v ∧ R.θ u = u) := fun h => h2 ⟨h.2, h.1⟩
      simp only [h1, h1', h2, h2', and_self, if_true, if_false]
  · have h1' : ¬ (R.inS v ∧ R.inS u) := fun h => h1 ⟨h.2, h.1⟩
    simp only [h1, h1', if_false]

def wt : Sym2 V → ℝ := Sym2.lift ⟨R.wtf, R.wtf_comm⟩

/-- The crossing indicator: one end in `P`, the other outside the closed half. -/
def crf (u v : V) : ℝ := if (u ∈ R.P ∧ ¬ R.inS v) ∨ (v ∈ R.P ∧ ¬ R.inS u) then 1 else 0

theorem crf_comm (u v : V) : R.crf u v = R.crf v u := by
  unfold crf
  by_cases h : (u ∈ R.P ∧ ¬ R.inS v) ∨ (v ∈ R.P ∧ ¬ R.inS u)
  · have h' : (v ∈ R.P ∧ ¬ R.inS u) ∨ (u ∈ R.P ∧ ¬ R.inS v) := h.symm
    simp only [h, h', if_true]
  · have h' : ¬ ((v ∈ R.P ∧ ¬ R.inS u) ∨ (u ∈ R.P ∧ ¬ R.inS v)) := fun h'' => h h''.symm
    simp only [h, h', if_false]

def cr : Sym2 V → ℝ := Sym2.lift ⟨R.crf, R.crf_comm⟩

/-- The coordinate `i` of the spin at the `P`-end of a crossing edge (0 for other edges). -/
def ccf {N : ℕ} (i : Fin N) (y : R.Pt → Sph N) (u v : V) : ℝ :=
  if hu : u ∈ R.P ∧ ¬ R.inS v then ((y ⟨u, hu.1⟩ : Sph N) : Amb N) i
  else if hv : v ∈ R.P ∧ ¬ R.inS u then ((y ⟨v, hv.1⟩ : Sph N) : Amb N) i else 0

theorem not_both {u v : V} (hu : u ∈ R.P ∧ ¬ R.inS v) (hv : v ∈ R.P ∧ ¬ R.inS u) : False :=
  hv.2 (Or.inr hu.1)

theorem ccf_comm {N : ℕ} (i : Fin N) (y : R.Pt → Sph N) (u v : V) : R.ccf i y u v = R.ccf i y v u := by
  unfold ccf
  by_cases hu : u ∈ R.P ∧ ¬ R.inS v
  · have hv : ¬ (v ∈ R.P ∧ ¬ R.inS u) := fun hv => R.not_both hu hv
    simp only [hu, hv, dite_true, dite_false, and_self, not_false_eq_true]
  · by_cases hv : v ∈ R.P ∧ ¬ R.inS u
    · simp only [hu, hv, dite_true, dite_false, and_self, not_false_eq_true]
    · simp only [hu, hv, dite_false]

def cc {N : ℕ} (i : Fin N) (e : Sym2 V) (y : R.Pt → Sph N) : ℝ :=
  Sym2.lift ⟨R.ccf i y, R.ccf_comm i y⟩ e

theorem cc_bdd {N : ℕ} (i : Fin N) (e : Sym2 V) : BddMeas (R.cc i e) := by
  induction e using Sym2.ind with
  | h u v =>
    refine ⟨?_, 1, fun y => ?_⟩
    · show Measurable (fun y => R.ccf i y u v)
      by_cases hu : u ∈ R.P ∧ ¬ R.inS v
      · simp only [ccf, dif_pos hu]
        exact measurable_coord (measurable_pi_apply (⟨u, hu.1⟩ : R.Pt)) i
      · by_cases hv : v ∈ R.P ∧ ¬ R.inS u
        · simp only [ccf, dif_neg hu, dif_pos hv]
          exact measurable_coord (measurable_pi_apply (⟨v, hv.1⟩ : R.Pt)) i
        · simp only [ccf, dif_neg hu, dif_neg hv]
          exact measurable_const
    · show |R.ccf i y u v| ≤ 1
      by_cases hu : u ∈ R.P ∧ ¬ R.inS v
      · simp only [ccf, dif_pos hu]
        exact abs_coord_le _ i
      · by_cases hv : v ∈ R.P ∧ ¬ R.inS u
        · simp only [ccf, dif_neg hu, dif_pos hv]
          exact abs_coord_le _ i
        · simp only [ccf, dif_neg hu, dif_neg hv, abs_zero, zero_le_one]


/-- The three classes of a vertex: fixed, in `P`, in `θ P`. -/
theorem cls (w : V) : (R.θ w = w ∧ w ∉ R.P ∧ True ∧ True) ∨
    (w ∈ R.P ∧ R.θ w ≠ w ∧ w ≠ R.θ w ∧ R.θ w ∉ R.P) ∨
    (w ∉ R.P ∧ R.θ w ≠ w ∧ w ≠ R.θ w ∧ R.θ w ∈ R.P) := by
  by_cases h1 : R.θ w = w
  · by_cases h2 : w ∈ R.P
    · exact absurd h1 (R.ne_of_mem h2)
    · exact Or.inl ⟨h1, h2, trivial, trivial⟩
  · have h1' : w ≠ R.θ w := fun h => h1 h.symm
    by_cases h2 : w ∈ R.P
    · exact Or.inr (Or.inl ⟨h2, h1, h1', R.disj w h2⟩)
    · exact Or.inr (Or.inr ⟨h2, h1, h1', R.mem_of_not h1 h2⟩)

/-- Every edge is counted once: in `A`, in `A ∘ θ`, half in each, or as a crossing edge. -/
theorem key_sum (u v : V) : R.wtf u v + R.wtf (R.θ u) (R.θ v) + R.crf u v = 1 := by
  have hθθ : ∀ w, R.θ (R.θ w) = w := R.invol
  unfold wtf crf inS
  rcases R.cls u with ⟨hu1, hu2, hu3, hu4⟩ | ⟨hu1, hu2, hu3, hu4⟩ | ⟨hu1, hu2, hu3, hu4⟩ <;>
  rcases R.cls v with ⟨hv1, hv2, hv3, hv4⟩ | ⟨hv1, hv2, hv3, hv4⟩ | ⟨hv1, hv2, hv3, hv4⟩ <;>
  simp [hθθ, hu1, hu2, hu3, hu4, hv1, hv2, hv3, hv4] <;> norm_num

theorem key_sum_sym2 (e : Sym2 V) : R.wt e + R.wt (Sym2.map R.θ e) + R.cr e = 1 := by
  induction e using Sym2.ind with
  | h u v => exact R.key_sum u v

theorem cr_nonneg (e : Sym2 V) : 0 ≤ R.cr e := by
  induction e using Sym2.ind with
  | h u v =>
    show 0 ≤ R.crf u v
    unfold crf
    split_ifs <;> norm_num

theorem wt_ne_zero_inS {e : Sym2 V} (h : R.wt e ≠ 0) : ∀ x ∈ e, R.inS x := by
  induction e using Sym2.ind with
  | h u v =>
    have h' : R.wtf u v ≠ 0 := h
    unfold wtf at h'
    by_cases hc : R.inS u ∧ R.inS v
    · intro x hx
      rcases Sym2.mem_iff.mp hx with rfl | rfl
      · exact hc.1
      · exact hc.2
    · simp [hc] at h'

variable [Fintype V]

/-- The half energy `A`. -/
def halfE {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (σ : Config N V) : ℝ :=
  ∑ e ∈ G.edgeFinset, R.wt e * J e * bond e σ

theorem halfE_dependsOnly {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    DependsOnly R.S (R.halfE (N := N) G J) := by
  intro σ σ' hσ
  unfold halfE
  refine Finset.sum_congr rfl (fun e _ => ?_)
  by_cases h : R.wt e = 0
  · simp [h]
  · rw [bond_dependsOnly R.S e (fun x hx => R.wt_ne_zero_inS h x hx) σ σ' hσ]

theorem halfE_bdd {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    BddMeas (R.halfE (N := N) G J) := by
  refine BddMeas.sum G.edgeFinset (fun e _ => ?_)
  exact ⟨(measurable_bond e).const_mul _, |R.wt e * J e|, fun σ => by
    rw [abs_mul]
    exact mul_le_of_le_one_right (abs_nonneg _) (abs_bond_le e σ)⟩

/-- The weights of the crossing kernel. -/
def crossW (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {N : ℕ} (k : Sym2 V × Fin N) : ℝ :=
  if k.1 ∈ G.edgeFinset then R.cr k.1 * J k.1 else 0

/-- The functions of the crossing kernel. -/
def crossU {N : ℕ} (k : Sym2 V × Fin N) (y : R.Pt → Sph N) : ℝ := R.cc k.2 k.1 y

theorem crossW_nonneg (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJc : ∀ e ∈ G.edgeFinset, R.cr e ≠ 0 → 0 ≤ J e) {N : ℕ} (k : Sym2 V × Fin N) :
    0 ≤ R.crossW G J k := by
  unfold crossW
  split_ifs with h
  · by_cases hc : R.cr k.1 = 0
    · rw [hc, zero_mul]
    · exact mul_nonneg (R.cr_nonneg _) (hJc _ h hc)
  · exact le_refl 0

theorem crossU_bdd {N : ℕ} (k : Sym2 V × Fin N) : BddMeas (R.crossU k) := R.cc_bdd k.2 k.1

/-- Hypothesis on a graph and a reflection: the only edges between `P` and the outside of the closed half are
`{x, θ x}` with `x ∈ P`. -/
def CrossOK (G : SimpleGraph V) : Prop := ∀ u v, G.Adj u v → u ∈ R.P → ¬ R.inS v → v = R.θ u

theorem cross_eq {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hcross : R.CrossOK G)
    (σ : Config N V) :
    rankSum (G.edgeFinset ×ˢ Finset.univ) (R.crossW G J) R.crossU (R.restrP σ, R.restrP (σ ∘ R.θ))
      = ∑ e ∈ G.edgeFinset, R.cr e * J e * bond e σ := by
  unfold rankSum
  rw [Finset.sum_product]
  refine Finset.sum_congr rfl (fun e he => ?_)
  have hw : ∀ i : Fin N, R.crossW G J (e, i) = R.cr e * J e := fun i => by simp [crossW, he]
  simp only [hw, ← Finset.mul_sum]
  by_cases hc : R.cr e = 0
  · rw [hc]
    ring
  congr 1
  induction e using Sym2.ind with
  | h u v =>
    have hadj : G.Adj u v := SimpleGraph.mem_edgeFinset.mp he
    have hc' : R.crf u v ≠ 0 := hc
    unfold crf at hc'
    have hcases : (u ∈ R.P ∧ ¬ R.inS v) ∨ (v ∈ R.P ∧ ¬ R.inS u) := by
      by_contra hn
      simp [hn] at hc'
    show ∑ i, R.ccf i (R.restrP σ) u v * R.ccf i (R.restrP (σ ∘ R.θ)) u v = dot (σ u) (σ v)
    rcases hcases with hu | hv
    · have hvu : v = R.θ u := hcross u v hadj hu.1 hu.2
      simp only [ccf, dif_pos hu]
      subst hvu
      rw [dot_eq_sum]
      rfl
    · have huv : u = R.θ v := hcross v u hadj.symm hv.1 hv.2
      have hu : ¬ (u ∈ R.P ∧ ¬ R.inS v) := fun hu => R.not_both hu hv
      simp only [ccf, dif_neg hu, dif_pos hv]
      subst huv
      rw [dot_eq_sum]
      exact Finset.sum_congr rfl (fun i _ => mul_comm _ _)

theorem map_map_invol (e : Sym2 V) : Sym2.map R.θ (Sym2.map R.θ e) = e := by
  induction e using Sym2.ind with
  | h p q => simp only [Sym2.map_mk, R.invol]

theorem map_mem_edgeFinset (G : SimpleGraph V) [DecidableRel G.Adj]
    (haut : ∀ u v, G.Adj u v ↔ G.Adj (R.θ u) (R.θ v)) {e : Sym2 V} (he : e ∈ G.edgeFinset) :
    Sym2.map R.θ e ∈ G.edgeFinset := by
  induction e using Sym2.ind with
  | h p q =>
    rw [Sym2.map_mk]
    exact SimpleGraph.mem_edgeFinset.mpr ((haut p q).mp (SimpleGraph.mem_edgeFinset.mp he))

/-- **Energy decomposition** `E(σ) = A(σ) + A(σ ∘ θ) + crossing`. -/
theorem energy_decomp {N : ℕ} (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (haut : ∀ u v, G.Adj u v ↔ G.Adj (R.θ u) (R.θ v)) (hJ : ∀ e, J (Sym2.map R.θ e) = J e)
    (hcross : R.CrossOK G) (σ : Config N V) :
    energy G J σ = R.halfE G J σ + R.halfE G J (σ ∘ R.θ)
      + rankSum (G.edgeFinset ×ˢ Finset.univ) (R.crossW G J) R.crossU (R.restrP σ, R.restrP (σ ∘ R.θ)) := by
  rw [R.cross_eq G J hcross σ]
  have h2 : R.halfE G J (σ ∘ R.θ) = ∑ e ∈ G.edgeFinset, R.wt (Sym2.map R.θ e) * J e * bond e σ := by
    unfold halfE
    simp only [bond_comp]
    refine Finset.sum_nbij' (Sym2.map R.θ) (Sym2.map R.θ) (fun e he => R.map_mem_edgeFinset G haut he)
      (fun e he => R.map_mem_edgeFinset G haut he) (fun e _ => R.map_map_invol e)
      (fun e _ => R.map_map_invol e) (fun e _ => ?_)
    rw [R.map_map_invol, hJ]
  rw [h2]
  unfold energy halfE
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun e _ => ?_)
  have hk := R.key_sum_sym2 e
  calc J e * bond e σ = (R.wt e + R.wt (Sym2.map R.θ e) + R.cr e) * J e * bond e σ := by rw [hk, one_mul]
    _ = _ := by ring

/-- **Reflection positivity of the Gibbs measure.** -/
theorem rp_gibbs {N : ℕ} (hN : 0 < N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (haut : ∀ u v, G.Adj u v ↔ G.Adj (R.θ u) (R.θ v)) (hJ : ∀ e, J (Sym2.map R.θ e) = J e)
    (hcross : R.CrossOK G) (hJc : ∀ e ∈ G.edgeFinset, R.cr e ≠ 0 → 0 ≤ J e)
    {F : Config N V → ℝ} (hF : BddMeas F) (hFd : DependsOnly R.S F) :
    0 ≤ gibbsExp N G J (fun σ => F σ * F (σ ∘ R.θ)) := by
  unfold gibbsExp
  refine div_nonneg ?_ (partition_pos hN G J).le
  simp_rw [R.energy_decomp G J haut hJ hcross]
  exact rp_config hN R (R.halfE_bdd G J) (R.halfE_dependsOnly G J) hF hFd _ (R.crossW_nonneg G J hJc)
    (fun k => R.crossU_bdd k)

end ReflData

open ReflData

theorem energy_comp_inv {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (θ : V → V) (hinv : ∀ p, θ (θ p) = p) (hadj : ∀ p q, G.Adj p q ↔ G.Adj (θ p) (θ q))
    (hJ : ∀ e, J (Sym2.map θ e) = J e) (σ : Config N V) : energy G J (σ ∘ θ) = energy G J σ := by
  unfold energy
  simp only [bond_comp]
  have hmem : ∀ g ∈ G.edgeFinset, Sym2.map θ g ∈ G.edgeFinset := by
    intro g hg
    induction g using Sym2.ind with
    | h p q =>
      rw [Sym2.map_mk]
      exact SimpleGraph.mem_edgeFinset.mpr ((hadj p q).mp (SimpleGraph.mem_edgeFinset.mp hg))
  have hinv2 : ∀ g : Sym2 V, Sym2.map θ (Sym2.map θ g) = g := by
    intro g
    induction g using Sym2.ind with
    | h p q => simp only [Sym2.map_mk, hinv]
  refine Finset.sum_nbij' (Sym2.map θ) (Sym2.map θ) hmem hmem (fun g _ => hinv2 g) (fun g _ => hinv2 g)
    (fun g _ => ?_)
  rw [hJ]

theorem gibbsExp_comp_inv {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (θ : V → V) (hinv : ∀ p, θ (θ p) = p)
    (hadj : ∀ p q, G.Adj p q ↔ G.Adj (θ p) (θ q)) (hJ : ∀ e, J (Sym2.map θ e) = J e) (F : Config N V → ℝ) :
    gibbsExp N G J (fun σ => F (σ ∘ θ)) = gibbsExp N G J F := by
  have := omega_isProbabilityMeasure N hN
  let eθ : V ≃ V := ⟨θ, θ, hinv, hinv⟩
  have hmp := measurePreserving_arrowCongr' (fun _ : V => omega N) (fun _ : V => omega N) eθ
    (MeasurableEquiv.refl (Sph N)) (fun _ => MeasurePreserving.id (omega N))
  have hcomp : ∀ σ : Config N V,
      MeasurableEquiv.arrowCongr' eθ (MeasurableEquiv.refl (Sph N)) σ = σ ∘ θ := fun σ => rfl
  have h1 := hmp.integral_comp' (fun σ => F σ * Real.exp (energy G J σ))
  simp only [hcomp, energy_comp_inv G J θ hinv hadj hJ] at h1
  simp only [gibbsExp]
  congr 1

/-- **Lemma 6.1, covariance form**: `Cov(F, F ∘ θ) ≥ 0` for `|F| ≤ 1` depending only on the closed half. -/
theorem cov_refl {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] [DecidableEq V] (R : ReflData V)
    (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (haut : ∀ u v, G.Adj u v ↔ G.Adj (R.θ u) (R.θ v)) (hJ : ∀ e, J (Sym2.map R.θ e) = J e)
    (hcross : R.CrossOK G) (hJc : ∀ e ∈ G.edgeFinset, R.cr e ≠ 0 → 0 ≤ J e)
    (F : Config N V → ℝ) (hFm : Measurable F) (hFb : ∀ σ, |F σ| ≤ 1) (hFd : DependsOnly R.S F) :
    0 ≤ gibbsCov N G J F (fun σ => F (σ ∘ R.θ)) := by
  have hsym := gibbsExp_comp_inv hN G J R.θ R.invol haut hJ F
  have hθm : Measurable (fun σ : Config N V => σ ∘ R.θ) :=
    Measurable.of_eval (fun i => measurable_pi_apply (R.θ i))
  have hFθm : Measurable (fun σ : Config N V => F (σ ∘ R.θ)) := hFm.comp hθm
  have hc := R.rp_gibbs hN G J haut hJ hcross hJc (F := fun σ => F σ - gibbsExp N G J F)
    ⟨hFm.sub measurable_const, 1 + |gibbsExp N G J F|, fun σ => by
      have h1 := hFb σ
      have h2 := abs_sub (F σ) (gibbsExp N G J F)
      linarith⟩
    (fun σ σ' h => by
      show F σ - gibbsExp N G J F = F σ' - gibbsExp N G J F
      rw [hFd σ σ' h])
  rw [gibbsExp_centered hN G J F (fun σ => F (σ ∘ R.θ)) hFm hFθm hFb (fun σ => hFb _), hsym] at hc
  simp only [gibbsCov]
  rw [hsym]
  linarith

/-- **Lemma 6.1 for an edge**: `Cov(s_e, s_{θ e}) ≥ 0` for every edge `e` in the closed half, every `N`. -/
theorem G2pair_refl (N : ℕ) {V : Type*} [Fintype V] [DecidableEq V] (R : ReflData V)
    (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (haut : ∀ u v, G.Adj u v ↔ G.Adj (R.θ u) (R.θ v)) (hJ : ∀ e, J (Sym2.map R.θ e) = J e)
    (hcross : R.CrossOK G) (hJc : ∀ e ∈ G.edgeFinset, R.cr e ≠ 0 → 0 ≤ J e)
    (e : Sym2 V) (he : ∀ x ∈ e, R.inS x) : G2pair N G J e (Sym2.map R.θ e) := by
  unfold G2pair
  have hb : (fun σ : Config N V => bond e (σ ∘ R.θ)) = bond (Sym2.map R.θ e) := by
    funext σ
    rw [bond_comp]
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · obtain ⟨x, -⟩ : ∃ x, x ∈ e := by
      induction e using Sym2.ind with
      | h p q => exact ⟨p, Sym2.mem_mk_left p q⟩
    have hV : Nonempty V := ⟨x⟩
    have h0 : freeMeasure 0 V = 0 := freeMeasure_zero V
    simp [gibbsCov, gibbsExp, partition, h0]
  rw [← hb]
  exact cov_refl hN R G J haut hJ hcross hJc (bond e) (measurable_bond e) (fun σ => abs_bond_le e σ)
    (bond_dependsOnly R.S e (fun x hx => he x hx))

end G2S3

#print axioms G2S3.rp_config
#print axioms G2S3.ReflData.rp_gibbs
#print axioms G2S3.cov_refl
#print axioms G2S3.G2pair_refl
