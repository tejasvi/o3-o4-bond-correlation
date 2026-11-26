/-
G2Kernel.Proofs.Strip300Proof: proof of `strip300_statement` (module M12). Kernel proof, step L-b.
- On `(0, 20]`, for `n ≥ 3` and pairs not in one column, `strip_route_nsc` runs the route of `stripD_thm` without
  hStripSpecial: corner pairs from hCornerPair (derived by `cornerPair_thm`), `(0, 1/100]` from hWeak, a vertical edge
  of an end column replaced by the horizontal edge at its corner (`replace_end`; a corner step never produces a pair in
  one column), and regular pairs through `criterion_thm` with hStripIdentity and hStripCert.
- On `[20, 300]`, for `n ≥ 4` and pairs not in one column, hRHCover. The two ranges meet at `J = 20`; the proof splits
  at `J ≤ 20` against `20 < J`.
- The two vertical edges of one column share the middle vertex, so hShared gives `Cov ≥ 0` at every `J ≥ 0`.
- `J = 0`, `n ≥ 4`, pairs not in one column: continuity from the right, with the shifts `0 < ε ≤ 20` only
  (`gibbsCov_nonneg_of_small_shift`, the proof of `gibbsCov_nonneg_of_shift` with the limit along `(0, δ]`).
- `n = 3` from `G2_P3P3_thm`, `n = 2` from hLadder, `n = 1` from hShared (both edges contain the middle vertex).
-/
import G2Kernel.Strip300
import G2Kernel.Proofs.CornerFactorProof

noncomputable section
open MeasureTheory Real Filter Topology

namespace G2Kernel

/-- In `P_3 × P_1` every edge contains the middle vertex. -/
theorem strip1_adj_mid : ∀ p q : Fin 3 × Fin 1, (strip 1).Adj p q →
    p = ((1 : Fin 3), (0 : Fin 1)) ∨ q = ((1 : Fin 3), (0 : Fin 1)) := by
  decide +kernel

theorem strip1_mem_mid {e : Sym2 (Fin 3 × Fin 1)} (he : e ∈ (strip 1).edgeSet) :
    ((1 : Fin 3), (0 : Fin 1)) ∈ e := by
  induction e using Sym2.ind with
  | h p q =>
    rcases strip1_adj_mid p q ((SimpleGraph.mem_edgeSet (strip 1)).mp he) with h | h
    · rw [h]
      exact Sym2.mem_mk_left _ _
    · rw [h]
      exact Sym2.mem_mk_right _ _

/-- The two vertical edges of one column share the middle vertex of the column. -/
theorem sameColumn_shared {n : ℕ} {e f : Sym2 (Fin 3 × Fin n)} (h : sameColumn n e f) :
    ∃ v, v ∈ e ∧ v ∈ f := by
  obtain ⟨j, ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩⟩ := h
  · exact ⟨((1 : Fin 3), j), by simp [vUp], by simp [vDown]⟩
  · exact ⟨((1 : Fin 3), j), by simp [vDown], by simp [vUp]⟩

/-- If the covariance of two bond energies is nonnegative at `J + ε` for every `0 < ε ≤ δ`, it is nonnegative at `J`:
the proof of `gibbsCov_nonneg_of_shift`, with the limit taken along `(0, δ]` only. -/
theorem gibbsCov_nonneg_of_small_shift {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : Sym2 V) (δ : ℝ) (hδ : 0 < δ)
    (h : ∀ ε : ℝ, 0 < ε → ε ≤ δ → 0 ≤ gibbsCov N G (fun g => J g + ε) (bond e) (bond f)) :
    0 ≤ gibbsCov N G J (bond e) (bond f) := by
  have := omega_isProbabilityMeasure N hN
  have : IsProbabilityMeasure (freeMeasure N V) := by
    unfold freeMeasure
    infer_instance
  have hmE := measurable_energy (N := N) G J
  have hmZ : Measurable (fun σ : Config N V => Real.exp (energy G J σ)) := hmE.exp
  have hm1 : Measurable (fun σ : Config N V => bond e σ * Real.exp (energy G J σ)) :=
    (measurable_bond e).mul hmZ
  have hm2 : Measurable (fun σ : Config N V => bond f σ * Real.exp (energy G J σ)) :=
    (measurable_bond f).mul hmZ
  have hm12 : Measurable (fun σ : Config N V => bond e σ * bond f σ * Real.exp (energy G J σ)) :=
    ((measurable_bond e).mul (measurable_bond f)).mul hmZ
  have hmS : Measurable (edgeSum (N := N) G) := measurable_edgeSum G
  have hSb : ∀ σ : Config N V, |edgeSum G σ| ≤ (G.edgeFinset.card : ℝ) := fun σ => abs_edgeSum_le G σ
  have hbJ : ∀ σ : Config N V, |Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) :=
    fun σ => abs_exp_le (abs_energy_le G J σ)
  have hb1 : ∀ σ : Config N V,
      |bond e σ * Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) :=
    fun σ => abs_one_mul_le (abs_bond_le e σ) (hbJ σ)
  have hb2 : ∀ σ : Config N V,
      |bond f σ * Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) :=
    fun σ => abs_one_mul_le (abs_bond_le f σ) (hbJ σ)
  have hb12 : ∀ σ : Config N V,
      |bond e σ * bond f σ * Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) := by
    intro σ
    rw [mul_assoc]
    exact abs_one_mul_le (abs_bond_le e σ) (hb2 σ)
  have dZ := hasDerivAt_expInt (freeMeasure N V) hmZ hmS hbJ hSb 0
  have dA1 := hasDerivAt_expInt (freeMeasure N V) hm1 hmS hb1 hSb 0
  have dA2 := hasDerivAt_expInt (freeMeasure N V) hm2 hmS hb2 hSb 0
  have dA12 := hasDerivAt_expInt (freeMeasure N V) hm12 hmS hb12 hSb 0
  have hZ0 : expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) 0 ≠ 0 :=
    (expInt_exp_pos (freeMeasure N V) hmE hmS (fun σ => abs_energy_le G J σ) hSb 0).ne'
  have hcov : ∀ ε : ℝ, gibbsCov N G (fun g => J g + ε) (bond e) (bond f)
      = expInt (freeMeasure N V) (fun σ => bond e σ * bond f σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε
        - expInt (freeMeasure N V) (fun σ => bond e σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε
          * (expInt (freeMeasure N V) (fun σ => bond f σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε) := by
    intro ε
    simp only [gibbsCov, gibbsExp, partition, expInt, energy_shift G J ε, Real.exp_add, mul_assoc]
  have hc : ContinuousAt (fun ε : ℝ =>
      expInt (freeMeasure N V) (fun σ => bond e σ * bond f σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε
        - expInt (freeMeasure N V) (fun σ => bond e σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε
          * (expInt (freeMeasure N V) (fun σ => bond f σ * Real.exp (energy G J σ)) (edgeSum G) ε
          / expInt (freeMeasure N V) (fun σ => Real.exp (energy G J σ)) (edgeSum G) ε)) 0 :=
    (dA12.continuousAt.div dZ.continuousAt hZ0).sub
      ((dA1.continuousAt.div dZ.continuousAt hZ0).mul (dA2.continuousAt.div dZ.continuousAt hZ0))
  have h0eq : (fun g => J g + 0) = J := funext fun g => add_zero (J g)
  have hval := hcov 0
  rw [h0eq] at hval
  rw [hval]
  have ht := hc.tendsto.mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  refine ge_of_tendsto ht ?_
  filter_upwards [Ioc_mem_nhdsGT hδ] with ε hε
  have h1 := h ε hε.1 hε.2
  rw [hcov ε] at h1
  exact h1

/-- The route of `stripD_thm` on `(0, 20]` for the pairs not in one column, without hStripSpecial. -/
theorem strip_route_nsc {N : ℕ} (hN34 : N = 3 ∨ N = 4) (hS : hSphereIso N) (hW : hWeak N) (md : StripModes)
    (hId : hStripIdentity N md) (hCert : hStripCert N md) (hCP : hCornerPair N) {n : ℕ} (hn : 3 ≤ n) {J : ℝ}
    (hJ0 : 0 < J) (hJ20 : J ≤ 20) {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet)
    (hf : f ∈ (strip n).edgeSet) (hef : e ≠ f) (hnsc : ¬ sameColumn n e f) :
    0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f) := by
  have htop : 20 ≤ stripTop N := by
    obtain ⟨-, -, h3, h4⟩ := cover_thm
    rcases hN34 with rfl | rfl
    · exact h3
    · exact h4
  by_cases hsc : seriesCorner n e f
  · exact hCP n hn J hJ0 hJ20 e he f hf hef hsc
  rcases le_or_gt J (1 / 100) with hJs | hJl
  · exact hW n hn J hJ0 hJs e he f hf hef hsc
  have hlo : 99 / 10000 ≤ J := by linarith
  have hhi : J ≤ stripTop N := le_trans hJ20 htop
  have hreg : ∀ e' ∈ (strip n).edgeSet, ∀ f' ∈ (strip n).edgeSet, e' ≠ f' → regularPair n e' f' →
      0 < gibbsCov N (strip n) (uniform J) (bond e') (bond f') := by
    intro e' he' f' hf' hne hr
    obtain ⟨hcv, hid⟩ := hId n hn J hlo hhi e' he' f' hf' hne hr
    obtain ⟨m0, hC⟩ := hCert
    have hc := hC n hn J hlo hhi e' he' f' hf' hne hr
    have hpos := criterion_thm (md n J e' f') (m0 J) hid hc.1 hc.2
    rw [hcv] at hpos
    exact hpos
  by_cases hev : endVertical n e
  · obtain ⟨h, hh, hhf, hhv, hhsc, hhcol, hcov⟩ := replace_end hS hn J hev hsc
    rw [hcov]
    by_cases hfv : endVertical n f
    · have hsc' : ¬ seriesCorner n f h := fun ⟨c, hc, h1, h2⟩ => hhsc ⟨c, hc, h2, h1⟩
      obtain ⟨h', hh', hh'h, hh'v, -, -, hcov'⟩ := replace_end hS hn J hfv hsc'
      rw [gibbsCov_comm, hcov', gibbsCov_comm]
      exact hreg h hh h' hh' (Ne.symm hh'h) ⟨(hhcol h').1, hhv, hh'v⟩
    · exact hreg h hh f hf hhf ⟨(hhcol f).1, hhv, hfv⟩
  · by_cases hfv : endVertical n f
    · have hsc' : ¬ seriesCorner n f e := fun ⟨c, hc, h1, h2⟩ => hsc ⟨c, hc, h2, h1⟩
      obtain ⟨h, hh, hhe, hhv, -, hhcol, hcov⟩ := replace_end hS hn J hfv hsc'
      rw [gibbsCov_comm, hcov, gibbsCov_comm]
      exact hreg e he h hh (Ne.symm hhe) ⟨(hhcol e).2, hev, hhv⟩
    · exact hreg e he f hf hef ⟨hnsc, hev, hfv⟩

theorem strip300_thm (N : ℕ) : strip300_statement N := by
  unfold strip300_statement
  intro hN34 hS hSh hRP hW md hId hCert k hK hR hCF hH hL hLad hRH
  have hN : 0 < N := by rcases hN34 with rfl | rfl <;> norm_num
  have hCP : hCornerPair N := cornerPair_thm N k hK hR hCF
  have hstrict : ∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 300 →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
        0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f) := by
    intro n hn J hJ0 hJ300 e he f hf hef hnsc
    rcases le_or_gt J 20 with hJ20 | hJ20
    · exact strip_route_nsc hN34 hS hW md hId hCert hCP (by omega) hJ0 hJ20 he hf hef hnsc
    · exact hRH n hn J hJ20.le hJ300 e he f hf hef hnsc
  refine ⟨?_, hstrict⟩
  intro n hn J hJ0 hJ300 e he f hf hef
  have hferro : ∀ m : ℕ, Ferro (strip m) (uniform J) := fun _ _ _ => hJ0
  rcases Nat.lt_or_ge n 4 with h4 | h4
  · interval_cases n
    · exact hSh (Fin 3 × Fin 1) (strip 1) (uniform J) (hferro 1) e he f hf hef
        ⟨((1 : Fin 3), (0 : Fin 1)), strip1_mem_mid he, strip1_mem_mid hf⟩
    · exact hLad J hJ0 e he f hf hef
    · exact G2_P3P3_thm N hN34 hS hSh hRP hW md hId hCert hH hL J hJ0 e he f hf hef
  · by_cases hsc : sameColumn n e f
    · exact hSh (Fin 3 × Fin n) (strip n) (uniform J) (hferro n) e he f hf hef (sameColumn_shared hsc)
    · rcases lt_or_eq_of_le hJ0 with hJpos | hJz
      · exact (hstrict n h4 J hJpos hJ300 e he f hf hef hsc).le
      · subst hJz
        show 0 ≤ gibbsCov N (strip n) (uniform 0) (bond e) (bond f)
        apply gibbsCov_nonneg_of_small_shift hN (strip n) (uniform 0) e f 20 (by norm_num)
        intro ε hε0 hε20
        have hfun : (fun g : Sym2 (Fin 3 × Fin n) => (uniform 0 : Sym2 (Fin 3 × Fin n) → ℝ) g + ε)
            = uniform ε := by
          funext g
          simp only [uniform, zero_add]
        rw [hfun]
        exact (hstrict n h4 ε hε0 (by linarith) e he f hf hef hsc).le

end G2Kernel
