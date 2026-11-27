/-
G2S3.RPInst (stage S3, Part A4): Lemma 6.1 on every box P_m x P_n (reflections in the horizontal and vertical
midlines, and in both diagonals when m = n) for theta-invariant ferromagnetic couplings and every N, and the two named
hypotheses it removes:
- H7 `hRPGibbs N` (reflection positivity for reflH and reflAnti of P_3 x P_3), `hRPGibbs_holds`;
- H18 `hStripMirror N` (middle-row and vertical-midline mirror pairs of P_3 x P_n), `hStripMirror_holds`.
Paper: Lemma 6.1 (tex l.1726-1738): "Let theta be a reflection of the box P_m x P_n in a horizontal or vertical line,
or, if m = n, in a diagonal, and let the couplings be theta-invariant. Then Cov(s_e, s_{theta e}) >= 0 for every edge
e, for every N >= 1." (Ferromagnetic couplings, J >= 0, as everywhere in the paper; only the crossing bonds of a line
between rows use the sign.)
-/
import G2S3.RPEnergy
import G2Kernel.Proofs.AssemblyProof
import StripIII.Statement

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

/-! ### Variance and the three kinds of edges -/

theorem gibbsCov_self_nonneg {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (F : Config N V → ℝ) (hFm : Measurable F) (hFb : ∀ σ, |F σ| ≤ 1) :
    0 ≤ gibbsCov N G J F F := by
  have h := gibbsExp_centered hN G J F F hFm hFm hFb hFb (gibbsExp N G J F)
  have hnn : 0 ≤ gibbsExp N G J (fun σ => (F σ - gibbsExp N G J F) * (F σ - gibbsExp N G J F)) := by
    unfold gibbsExp
    refine div_nonneg (integral_nonneg (fun σ => ?_)) (partition_pos hN G J).le
    exact mul_nonneg (mul_self_nonneg _) (Real.exp_pos _).le
  unfold gibbsCov
  linarith

theorem G2pair_self (N : ℕ) {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (e : Sym2 V) [Nonempty V] : G2pair N G J e e := by
  unfold G2pair
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · simp [gibbsCov, gibbsExp, partition, freeMeasure_zero V]
  · exact gibbsCov_self_nonneg hN G J (bond e) (measurable_bond e) (fun σ => abs_bond_le e σ)

namespace ReflData

variable {V : Type*} [DecidableEq V] (R : ReflData V)

theorem not_inS_theta {w : V} (h : ¬ R.inS (R.θ w)) : w ∈ R.P := by
  unfold inS at h
  rw [R.invol] at h
  push_neg at h
  rcases R.cover w with h1 | h1 | h1
  · exact absurd h1.symm h.1
  · exact h1
  · exact absurd h1 h.2

theorem not_inS_notP {w : V} (h : ¬ R.inS w) : w ∉ R.P := fun hw => h (Or.inr hw)

end ReflData

/-- **Lemma 6.1, every edge**: for a reflection with the crossing property, `Cov(s_e, s_{θ e}) ≥ 0` for every edge. -/
theorem G2pair_refl_edge (N : ℕ) {V : Type*} [Fintype V] [DecidableEq V] (R : ReflData V)
    (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (haut : ∀ u v, G.Adj u v ↔ G.Adj (R.θ u) (R.θ v)) (hJ : ∀ e, J (Sym2.map R.θ e) = J e)
    (hcross : R.CrossOK G) (hJc : ∀ e ∈ G.edgeFinset, R.cr e ≠ 0 → 0 ≤ J e)
    (e : Sym2 V) (he : e ∈ G.edgeSet) : G2pair N G J e (Sym2.map R.θ e) := by
  induction e using Sym2.ind with
  | h u v =>
    have hadj : G.Adj u v := he
    have hV : Nonempty V := ⟨u⟩
    by_cases hA : R.inS u ∧ R.inS v
    · refine G2pair_refl N R G J haut hJ hcross hJc s(u, v) (fun x hx => ?_)
      rcases Sym2.mem_iff.mp hx with rfl | rfl
      · exact hA.1
      · exact hA.2
    by_cases hB : R.inS (R.θ u) ∧ R.inS (R.θ v)
    · have h := G2pair_refl N R G J haut hJ hcross hJc (Sym2.map R.θ s(u, v)) (fun x hx => by
        rw [Sym2.map_mk] at hx
        rcases Sym2.mem_iff.mp hx with rfl | rfl
        · exact hB.1
        · exact hB.2)
      rw [R.map_map_invol] at h
      unfold G2pair at h ⊢
      rw [gibbsCov_comm]
      exact h
    -- a crossing edge, fixed by θ
    have hfix : Sym2.map R.θ s(u, v) = s(u, v) := by
      rw [Sym2.map_mk]
      by_cases hu : R.inS u
      · have hv : ¬ R.inS v := fun hv => hA ⟨hu, hv⟩
        have huP : u ∈ R.P := by
          by_contra huP
          have hθv : R.inS (R.θ v) := Or.inr (R.mem_of_not (fun h => hv (Or.inl h)) (R.not_inS_notP hv))
          have hθu : R.inS (R.θ u) := by
            rcases hu with h | h
            · left
              rw [h, h]
            · exact absurd h huP
          exact hB ⟨hθu, hθv⟩
        have hvu : v = R.θ u := hcross u v hadj huP hv
        rw [hvu, R.invol]
        exact Sym2.eq_swap
      · have hvP : v ∈ R.P := by
          by_contra hvP
          have hθu : R.inS (R.θ u) := Or.inr (R.mem_of_not (fun h => hu (Or.inl h)) (R.not_inS_notP hu))
          have hθv : R.inS (R.θ v) := by
            by_cases hv : R.inS v
            · rcases hv with h | h
              · left
                rw [h, h]
              · exact absurd h hvP
            · exact Or.inr (R.mem_of_not (fun h => hv (Or.inl h)) (R.not_inS_notP hv))
          exact hB ⟨hθu, hθv⟩
        have huv : u = R.θ v := hcross v u hadj.symm hvP hu
        rw [huv, R.invol]
        exact Sym2.eq_swap
    rw [hfix]
    exact G2pair_self N G J s(u, v)

/-! ### The box `P_m × P_n` and its reflections -/

/-- The box `P_m × P_n` on `Fin m × Fin n` (row, column), nearest neighbours; `strip n` is `box 3 n`. -/
def box (m n : ℕ) : SimpleGraph (Fin m × Fin n) :=
  SimpleGraph.fromRel fun p q => (p.1 = q.1 ∧ p.2.val + 1 = q.2.val) ∨ (p.2 = q.2 ∧ p.1.val + 1 = q.1.val)

instance (m n : ℕ) : DecidableRel (box m n).Adj :=
  fun p q => decidable_of_iff _ (SimpleGraph.fromRel_adj _ p q).symm

theorem box_adj {m n : ℕ} (p q : Fin m × Fin n) : (box m n).Adj p q ↔
    (p.1.val = q.1.val ∧ (p.2.val + 1 = q.2.val ∨ q.2.val + 1 = p.2.val)) ∨
    (p.2.val = q.2.val ∧ (p.1.val + 1 = q.1.val ∨ q.1.val + 1 = p.1.val)) := by
  unfold box
  rw [SimpleGraph.fromRel_adj]
  simp only [ne_eq, Prod.ext_iff, Fin.ext_iff]
  omega

theorem strip_adj_iff {n : ℕ} (p q : Fin 3 × Fin n) : (strip n).Adj p q ↔ (box 3 n).Adj p q := Iff.rfl

/-- Reflection in the horizontal midline: row `r ↦ m - 1 - r`; open half: the rows below the midline. -/
def reflHm (m n : ℕ) : ReflData (Fin m × Fin n) where
  θ := fun p => (Fin.rev p.1, p.2)
  invol := fun p => by simp
  P := Finset.univ.filter (fun p => m < 2 * p.1.val + 1)
  disj := by
    intro v hv
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Fin.val_rev] at hv ⊢
    have := v.1.isLt
    omega
  cover := by
    intro v
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Fin.val_rev, Prod.ext_iff, Fin.ext_iff, and_true]
    have := v.1.isLt
    omega

/-- Reflection in the vertical midline: column `c ↦ n - 1 - c`; open half: the columns right of the midline. -/
def reflVm (m n : ℕ) : ReflData (Fin m × Fin n) where
  θ := fun p => (p.1, Fin.rev p.2)
  invol := fun p => by simp
  P := Finset.univ.filter (fun p => n < 2 * p.2.val + 1)
  disj := by
    intro v hv
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Fin.val_rev] at hv ⊢
    have := v.2.isLt
    omega
  cover := by
    intro v
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Fin.val_rev, Prod.ext_iff, Fin.ext_iff, true_and]
    have := v.2.isLt
    omega

/-- Reflection in the diagonal `r = c`; open half: below the diagonal. -/
def reflDm (n : ℕ) : ReflData (Fin n × Fin n) where
  θ := fun p => (p.2, p.1)
  invol := fun p => rfl
  P := Finset.univ.filter (fun p => p.2.val < p.1.val)
  disj := by
    intro v hv
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hv ⊢
    omega
  cover := by
    intro v
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Prod.ext_iff, Fin.ext_iff]
    omega

/-- Reflection in the antidiagonal `r + c = n - 1`; open half: below it. -/
def reflAm (n : ℕ) : ReflData (Fin n × Fin n) where
  θ := fun p => (Fin.rev p.2, Fin.rev p.1)
  invol := fun p => by simp
  P := Finset.univ.filter (fun p => n < p.1.val + p.2.val + 1)
  disj := by
    intro v hv
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Fin.val_rev] at hv ⊢
    have := v.1.isLt
    have := v.2.isLt
    omega
  cover := by
    intro v
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Fin.val_rev, Prod.ext_iff, Fin.ext_iff]
    have := v.1.isLt
    have := v.2.isLt
    omega

theorem haut_reflHm (m n : ℕ) (u v : Fin m × Fin n) :
    (box m n).Adj u v ↔ (box m n).Adj ((reflHm m n).θ u) ((reflHm m n).θ v) := by
  rw [box_adj, box_adj]
  simp only [reflHm, Fin.val_rev]
  have := u.1.isLt
  have := v.1.isLt
  omega

theorem haut_reflVm (m n : ℕ) (u v : Fin m × Fin n) :
    (box m n).Adj u v ↔ (box m n).Adj ((reflVm m n).θ u) ((reflVm m n).θ v) := by
  rw [box_adj, box_adj]
  simp only [reflVm, Fin.val_rev]
  have := u.2.isLt
  have := v.2.isLt
  omega

theorem haut_reflDm (n : ℕ) (u v : Fin n × Fin n) :
    (box n n).Adj u v ↔ (box n n).Adj ((reflDm n).θ u) ((reflDm n).θ v) := by
  rw [box_adj, box_adj]
  simp only [reflDm]
  omega

theorem haut_reflAm (n : ℕ) (u v : Fin n × Fin n) :
    (box n n).Adj u v ↔ (box n n).Adj ((reflAm n).θ u) ((reflAm n).θ v) := by
  rw [box_adj, box_adj]
  simp only [reflAm, Fin.val_rev]
  have := u.1.isLt
  have := v.1.isLt
  have := u.2.isLt
  have := v.2.isLt
  omega

theorem cross_reflHm (m n : ℕ) : (reflHm m n).CrossOK (box m n) := by
  intro u v huv hu hv
  have huv' := (box_adj u v).mp huv
  have hu' : m < 2 * u.1.val + 1 := by
    have h : u ∈ (reflHm m n).P := hu
    simpa [reflHm] using h
  have hv1 : ¬ (m < 2 * v.1.val + 1) := by
    intro h
    exact hv (Or.inr (by simp only [reflHm, Finset.mem_filter, Finset.mem_univ, true_and]; exact h))
  have hlt1 := u.1.isLt
  have hlt2 := v.1.isLt
  have hv2 : ¬ (m = 2 * v.1.val + 1) := by
    intro h
    apply hv
    left
    show (Fin.rev v.1, v.2) = v
    refine Prod.ext (Fin.ext ?_) rfl
    simp only [Fin.val_rev]
    omega
  show v = (Fin.rev u.1, u.2)
  simp only [Prod.ext_iff, Fin.ext_iff, Fin.val_rev]
  omega

theorem cross_reflVm (m n : ℕ) : (reflVm m n).CrossOK (box m n) := by
  intro u v huv hu hv
  have huv' := (box_adj u v).mp huv
  have hu' : n < 2 * u.2.val + 1 := by
    have h : u ∈ (reflVm m n).P := hu
    simpa [reflVm] using h
  have hv1 : ¬ (n < 2 * v.2.val + 1) := by
    intro h
    exact hv (Or.inr (by simp only [reflVm, Finset.mem_filter, Finset.mem_univ, true_and]; exact h))
  have hlt1 := u.2.isLt
  have hlt2 := v.2.isLt
  have hv2 : ¬ (n = 2 * v.2.val + 1) := by
    intro h
    apply hv
    left
    show (v.1, Fin.rev v.2) = v
    refine Prod.ext rfl (Fin.ext ?_)
    simp only [Fin.val_rev]
    omega
  show v = (u.1, Fin.rev u.2)
  simp only [Prod.ext_iff, Fin.ext_iff, Fin.val_rev]
  omega

theorem cross_reflDm (n : ℕ) : (reflDm n).CrossOK (box n n) := by
  intro u v huv hu hv
  rw [box_adj] at huv
  simp only [ReflData.inS, reflDm, Finset.mem_filter, Finset.mem_univ, true_and, Prod.ext_iff, Fin.ext_iff,
    not_or, not_and] at hu hv
  exfalso
  omega

theorem cross_reflAm (n : ℕ) : (reflAm n).CrossOK (box n n) := by
  intro u v huv hu hv
  rw [box_adj] at huv
  simp only [ReflData.inS, reflAm, Finset.mem_filter, Finset.mem_univ, true_and, Prod.ext_iff, Fin.ext_iff,
    Fin.val_rev, not_or, not_and] at hu hv
  have := u.1.isLt
  have := v.1.isLt
  have := u.2.isLt
  have := v.2.isLt
  exfalso
  omega

/-! ### Lemma 6.1 -/

/-- **Lemma 6.1** (tex l.1726), horizontal line: for `θ`-invariant ferromagnetic couplings on `P_m × P_n`,
`Cov(s_e, s_{θ e}) ≥ 0` for every edge `e` and every `N`. -/
theorem lemma61_horizontal (N m n : ℕ) (J : Sym2 (Fin m × Fin n) → ℝ) (hJf : Ferro (box m n) J)
    (hJ : ∀ e, J (Sym2.map (reflHm m n).θ e) = J e) :
    ∀ e ∈ (box m n).edgeSet, G2pair N (box m n) J e (Sym2.map (reflHm m n).θ e) :=
  fun e he => G2pair_refl_edge N (reflHm m n) (box m n) J (haut_reflHm m n) hJ (cross_reflHm m n)
    (fun e' he' _ => hJf e' (SimpleGraph.mem_edgeFinset.mp he')) e he

/-- **Lemma 6.1**, vertical line. -/
theorem lemma61_vertical (N m n : ℕ) (J : Sym2 (Fin m × Fin n) → ℝ) (hJf : Ferro (box m n) J)
    (hJ : ∀ e, J (Sym2.map (reflVm m n).θ e) = J e) :
    ∀ e ∈ (box m n).edgeSet, G2pair N (box m n) J e (Sym2.map (reflVm m n).θ e) :=
  fun e he => G2pair_refl_edge N (reflVm m n) (box m n) J (haut_reflVm m n) hJ (cross_reflVm m n)
    (fun e' he' _ => hJf e' (SimpleGraph.mem_edgeFinset.mp he')) e he

/-- **Lemma 6.1**, the diagonal `r = c` of `P_n × P_n` (no sign condition is needed: no crossing bonds). -/
theorem lemma61_diagonal (N n : ℕ) (J : Sym2 (Fin n × Fin n) → ℝ)
    (hJ : ∀ e, J (Sym2.map (reflDm n).θ e) = J e) :
    ∀ e ∈ (box n n).edgeSet, G2pair N (box n n) J e (Sym2.map (reflDm n).θ e) := by
  intro e he
  refine G2pair_refl_edge N (reflDm n) (box n n) J (haut_reflDm n) hJ (cross_reflDm n) (fun e' he' hc => ?_) e he
  exfalso
  apply hc
  induction e' using Sym2.ind with
  | h u v =>
    have huv : (box n n).Adj u v := SimpleGraph.mem_edgeFinset.mp he'
    show (reflDm n).crf u v = 0
    rw [box_adj] at huv
    unfold ReflData.crf
    rw [if_neg]
    simp only [ReflData.inS, reflDm, Finset.mem_filter, Finset.mem_univ, true_and, Prod.ext_iff, Fin.ext_iff,
      not_or, not_and]
    omega

/-- **Lemma 6.1**, the antidiagonal `r + c = n - 1` of `P_n × P_n`. -/
theorem lemma61_antidiagonal (N n : ℕ) (J : Sym2 (Fin n × Fin n) → ℝ)
    (hJ : ∀ e, J (Sym2.map (reflAm n).θ e) = J e) :
    ∀ e ∈ (box n n).edgeSet, G2pair N (box n n) J e (Sym2.map (reflAm n).θ e) := by
  intro e he
  refine G2pair_refl_edge N (reflAm n) (box n n) J (haut_reflAm n) hJ (cross_reflAm n) (fun e' he' hc => ?_) e he
  exfalso
  apply hc
  induction e' using Sym2.ind with
  | h u v =>
    have huv : (box n n).Adj u v := SimpleGraph.mem_edgeFinset.mp he'
    show (reflAm n).crf u v = 0
    rw [box_adj] at huv
    unfold ReflData.crf
    rw [if_neg]
    simp only [ReflData.inS, reflAm, Finset.mem_filter, Finset.mem_univ, true_and, Prod.ext_iff, Fin.ext_iff,
      Fin.val_rev, not_or, not_and]
    have := u.1.isLt
    have := v.1.isLt
    have := u.2.isLt
    have := v.2.isLt
    omega

end G2S3

#print axioms G2S3.lemma61_horizontal
#print axioms G2S3.lemma61_vertical
#print axioms G2S3.lemma61_diagonal
#print axioms G2S3.lemma61_antidiagonal
