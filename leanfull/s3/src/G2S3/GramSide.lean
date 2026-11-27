/-
G2S3.GramSide (stage S3, Part E2): vertex elimination respecting a cut (STATEMENTS_S3_v8.md, E2). Words whose pairs never
cross the side set A keep that property when a vertex v outside the terminal set T is integrated out: the partners of v lie on
v's side. So for F depending only on the spins in T, nonnegativity on such words over T gives nonnegativity on all of them, and
on the Gibbs weight of couplings that never cross A.
-/
import G2S3.GramExp

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

section Side

variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]

theorem mem_partW' {v : V} {L : List (V × V)} {u : V} (h : u ∈ partW v L) :
    ∃ q ∈ L, (q.1 = v ∧ q.2 = u) ∨ (q.2 = v ∧ q.1 = u) := by
  unfold partW at h
  rw [List.mem_filterMap] at h
  obtain ⟨⟨a, b⟩, hq, hf⟩ := h
  simp only at hf
  by_cases ha : a = v
  · by_cases hb : b = v
    · simp [ha, hb] at hf
    · simp only [ha, hb, if_true, if_false, Option.some.injEq] at hf
      exact ⟨(a, b), hq, Or.inl ⟨ha, hf⟩⟩
  · by_cases hb : b = v
    · simp only [ha, hb, if_true, if_false, Option.some.injEq] at hf
      exact ⟨(a, b), hq, Or.inr ⟨hb, hf⟩⟩
    · simp [ha, hb] at hf

/-- **Vertex elimination respecting a cut** -/
theorem gram_pos_side (hN : 1 ≤ N) (T : Finset V) (A : Set V) {F : Config N V → ℝ} (hF : BddMeas F)
    (hFT : ∀ v ∉ T, ∀ (σ : Config N V) (z : Sph N), F (Function.update σ v z) = F σ)
    (hbase : ∀ L : List (V × V), (∀ q ∈ L, q.1 ∈ T ∧ q.2 ∈ T ∧ (q.1 ∈ A ↔ q.2 ∈ A)) →
      0 ≤ ∫ σ, F σ * gw L σ ∂(freeMeasure N V))
    (L : List (V × V)) (hL : ∀ q ∈ L, (q.1 ∈ A ↔ q.2 ∈ A)) : 0 ≤ ∫ σ, F σ * gw L σ ∂(freeMeasure N V) := by
  have hN0 : 0 < N := by omega
  have hprob := omega_isProbabilityMeasure N hN0
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  have hbdd : ∀ L' : List (V × V), BddMeas (fun σ : Config N V => F σ * gw L' σ) :=
    fun L' => BddMeas.mul hF (gw_bdd L')
  suffices H : ∀ S : Finset V, ∀ L : List (V × V),
      (∀ q ∈ L, (q.1 ∈ T ∨ q.1 ∈ S) ∧ (q.2 ∈ T ∨ q.2 ∈ S) ∧ (q.1 ∈ A ↔ q.2 ∈ A)) →
      0 ≤ ∫ σ, F σ * gw L σ ∂(freeMeasure N V) by
    exact H Finset.univ L (fun q hq => ⟨Or.inr (Finset.mem_univ _), Or.inr (Finset.mem_univ _), hL q hq⟩)
  intro S
  induction S using Finset.induction_on with
  | empty =>
    intro L hL'
    refine hbase L (fun q hq => ?_)
    obtain ⟨h1, h2, h3⟩ := hL' q hq
    simp only [Finset.notMem_empty, or_false] at h1 h2
    exact ⟨h1, h2, h3⟩
  | insert v S hvS ih =>
    intro L hL'
    by_cases hvT : v ∈ T
    · refine ih L (fun q hq => ?_)
      obtain ⟨h1, h2, h3⟩ := hL' q hq
      simp only [Finset.mem_insert] at h1 h2
      refine ⟨?_, ?_, h3⟩
      · rcases h1 with h | h | h
        · exact Or.inl h
        · exact Or.inl (h ▸ hvT)
        · exact Or.inr h
      · rcases h2 with h | h | h
        · exact Or.inl h
        · exact Or.inl (h ▸ hvT)
        · exact Or.inr h
    set U := partW v L with hU
    set D := U.length with hD
    set W : (Fin (D / 2) → Fin D × Fin D) → List (V × V) :=
      fun p => List.ofFn (fun k => (U[((p k).1 : ℕ)], U[((p k).2 : ℕ)])) with hW
    have step : ∀ σ : Config N V, ∫ z, F (Function.update σ v z) * gw L (Function.update σ v z) ∂(omega N)
        = ∑ p : Fin (D / 2) → Fin D × Fin D, polC N D p * (F σ * gw (restW v L ++ W p) σ) := by
      intro σ
      simp only [hFT v hvT, gw_update]
      have e1 : (fun z : Sph N => F σ * (gw (restW v L) σ * (U.map fun u => dot (σ u) z).prod))
          = fun z : Sph N => (F σ * gw (restW v L) σ) *
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
      obtain ⟨h1, h2, h3⟩ := hL' q hqL
      simp only [Finset.mem_insert] at h1 h2
      refine ⟨?_, ?_, h3⟩
      · rcases h1 with h | h | h
        · exact Or.inl h
        · exact absurd h hq1
        · exact Or.inr h
      · rcases h2 with h | h | h
        · exact Or.inl h
        · exact absurd h hq2
        · exact Or.inr h
    · rw [hW, List.mem_ofFn] at hq
      obtain ⟨k, hk⟩ := hq
      have hmemU : ∀ i : Fin D, (U[(i : ℕ)] ∈ T ∨ U[(i : ℕ)] ∈ S) ∧ (U[(i : ℕ)] ∈ A ↔ v ∈ A) := by
        intro i
        have hm : U[(i : ℕ)] ∈ partW v L := List.getElem_mem _
        obtain ⟨hne, -⟩ := mem_partW hm
        obtain ⟨q', hq', hqv⟩ := mem_partW' hm
        obtain ⟨h1, h2, h3⟩ := hL' q' hq'
        simp only [Finset.mem_insert] at h1 h2
        rcases hqv with ⟨hv1, hu2⟩ | ⟨hv2, hu1⟩
        · rw [← hu2]
          refine ⟨?_, ?_⟩
          · rcases h2 with h | h | h
            · exact Or.inl h
            · exact absurd (hu2.symm.trans h) hne
            · exact Or.inr h
          · rw [← hv1]; exact h3.symm
        · rw [← hu1]
          refine ⟨?_, ?_⟩
          · rcases h1 with h | h | h
            · exact Or.inl h
            · exact absurd (hu1.symm.trans h) hne
            · exact Or.inr h
          · rw [← hv2]; exact h3
      rw [← hk]
      obtain ⟨a1, a2⟩ := hmemU (p k).1
      obtain ⟨b1, b2⟩ := hmemU (p k).2
      exact ⟨a1, b1, a2.trans b2.symm⟩

theorem ePair_eq (g : Sym2 V) : s((ePair g).1, (ePair g).2) = g := by
  unfold ePair
  exact Quot.out_eq g

theorem integral_G_energy_pow (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    {F : Config N V → ℝ} (hF : BddMeas F) (n : ℕ) :
    ∫ σ, F σ * energy G J σ ^ n ∂(freeMeasure N V)
      = ∑ s : Fin n → G.edgeFinset, (∏ k, J (s k)) *
          ∫ σ, F σ * gw (List.ofFn fun k => ePair ((s k : G.edgeFinset) : Sym2 V)) σ ∂(freeMeasure N V) := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  simp only [energy_pow, Finset.mul_sum]
  rw [integral_finsetSum _ (fun s _ => ((BddMeas.mul hF (gw_bdd _)).integrable).const_mul (∏ k, J (s k)) |>.congr
    (Filter.Eventually.of_forall (fun σ => by ring)))]
  refine Finset.sum_congr rfl (fun s _ => ?_)
  rw [← integral_const_mul]
  congr 1
  funext σ
  ring

theorem hasSum_integral_expG (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    {F : Config N V → ℝ} (hF : BddMeas F) :
    HasSum (fun n => ∫ σ, F σ * (energy G J σ ^ n / (n.factorial : ℝ)) ∂(freeMeasure N V))
      (∫ σ, F σ * Real.exp (energy G J σ) ∂(freeMeasure N V)) := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  obtain ⟨hFm, C, hC⟩ := hF
  obtain ⟨M, hMb⟩ : ∃ M : ℝ, ∀ σ : Config N V, |energy G J σ| ≤ M := ⟨_, fun σ => abs_energy_le G J σ⟩
  have hB : ∀ (n : ℕ) (σ : Config N V),
      |F σ * (energy G J σ ^ n / (n.factorial : ℝ))| ≤ |C| * (M ^ n / (n.factorial : ℝ)) := by
    intro n σ
    have h1 : |F σ| ≤ |C| := (hC σ).trans (le_abs_self C)
    have h2 : |energy G J σ ^ n / (n.factorial : ℝ)| ≤ M ^ n / (n.factorial : ℝ) := by
      rw [abs_div, abs_pow, Nat.abs_cast]
      exact div_le_div_of_nonneg_right (pow_le_pow_left₀ (abs_nonneg _) (hMb σ) n) (Nat.cast_nonneg _)
    rw [abs_mul]
    exact mul_le_mul h1 h2 (abs_nonneg _) (abs_nonneg _)
  have hsum : Summable (fun n : ℕ => |C| * (M ^ n / (n.factorial : ℝ))) :=
    (Real.summable_pow_div_factorial M).mul_left _
  have hmeas : ∀ n : ℕ, AEStronglyMeasurable
      (fun σ : Config N V => F σ * (energy G J σ ^ n / (n.factorial : ℝ))) (freeMeasure N V) :=
    fun n => (hFm.mul (((measurable_energy (N := N) G J).pow_const n).div_const _)).aestronglyMeasurable
  have hlim : ∀ σ : Config N V, HasSum (fun n => F σ * (energy G J σ ^ n / (n.factorial : ℝ)))
      (F σ * Real.exp (energy G J σ)) := by
    intro σ
    have h := NormedSpace.expSeries_div_hasSum_exp (𝔸 := ℝ) (energy G J σ)
    rw [← Real.exp_eq_exp_ℝ] at h
    exact h.mul_left (F σ)
  exact hasSum_integral_of_bound _ _ _ hmeas hB hsum hlim

/-- **the Gibbs weight respecting a cut** -/
theorem gram_exp_side (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    (T : Finset V) (A : Set V) {F : Config N V → ℝ} (hF : BddMeas F)
    (hFT : ∀ v ∉ T, ∀ (σ : Config N V) (z : Sph N), F (Function.update σ v z) = F σ)
    (hJA : ∀ a b, G.Adj a b → J s(a, b) ≠ 0 → (a ∈ A ↔ b ∈ A))
    (hbase : ∀ L : List (V × V), (∀ q ∈ L, q.1 ∈ T ∧ q.2 ∈ T ∧ (q.1 ∈ A ↔ q.2 ∈ A)) →
      0 ≤ ∫ σ, F σ * gw L σ ∂(freeMeasure N V)) :
    0 ≤ ∫ σ, F σ * Real.exp (energy G J σ) ∂(freeMeasure N V) := by
  refine (hasSum_integral_expG hN G J hF).nonneg (fun n => ?_)
  have e : (fun σ : Config N V => F σ * (energy G J σ ^ n / (n.factorial : ℝ)))
      = fun σ => (1 / (n.factorial : ℝ)) * (F σ * energy G J σ ^ n) := by
    funext σ; ring
  rw [e, integral_const_mul, integral_G_energy_pow hN G J hF n]
  refine mul_nonneg (by positivity) (Finset.sum_nonneg (fun s _ => ?_))
  by_cases hz : ∃ k, J (s k) = 0
  · obtain ⟨k, hk⟩ := hz
    rw [Finset.prod_eq_zero (Finset.mem_univ k) hk, zero_mul]
  · push_neg at hz
    refine mul_nonneg (Finset.prod_nonneg (fun k _ => hJ _ (G.mem_edgeFinset.mp (s k).2))) ?_
    refine gram_pos_side hN T A hF hFT hbase _ (fun q hq => ?_)
    rw [List.mem_ofFn] at hq
    obtain ⟨k, rfl⟩ := hq
    have hg := G.mem_edgeFinset.mp (s k).2
    rw [← ePair_eq ((s k : G.edgeFinset) : Sym2 V)] at hg
    have hJk := hz k
    rw [← ePair_eq ((s k : G.edgeFinset) : Sym2 V)] at hJk
    exact hJA _ _ hg hJk

end Side

end G2S3

#print axioms G2S3.gram_pos_side
#print axioms G2S3.gram_exp_side
