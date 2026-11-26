/-
G2Kernel.Proofs.AssemblyProof: proofs of `G2_P3P3_statement` (Theorem 6.34(a)), `stripD_statement` (Theorem 1.4(ii))
and `strip3_statement` (its case n = 3). Kernel proof, step L-b.
- Theorem 6.34(a) is the orbit reduction of Proposition 6.7. At uniform coupling the covariance of two bond energies is
  invariant under graph automorphisms, so by the ledger (conjuncts 2 and 3) it suffices to treat the representatives:
  the pairs with a common vertex come from hShared, the mirror pairs from mirror33_thm, and the corner identity
  (corner_thm) moves (b_0, b_2), (b_0, b_4) to mirror pairs and (b_0, s_E) to a pair with a common vertex. The pairs
  (b_0, s_N) and (b_0, s_W) have the common covariance Cov(s_{b_0}, s_{s_N}), positive for J > 0 on the joined ranges
  (cover_thm with hWeak, the strip criterion at n = 3, hHub and hLBu) and nonnegative at J = 0 by continuity in J.
- Theorem 1.4(ii): the two edges at one corner come from hCornerPair, and on (0, 1/100] the other pairs from hWeak. On
  [0.0099, 20] a vertical edge of an end column is replaced by the horizontal edge at its corner (corner_thm, one or two
  steps), the two vertical edges of an interior column come from hStripSpecial, and the remaining pairs are regular and
  go through criterion_thm with hStripIdentity and hStripCert.
-/
import G2Kernel.Assembly
import G2Kernel.Proofs.MirrorProof
import G2Kernel.Proofs.CriterionProof
import G2Kernel.Proofs.CoverProof

noncomputable section
open MeasureTheory Real

namespace G2Kernel

/-! ### Covariances under symmetry -/

theorem gibbsCov_comm {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (F H : Config N V → ℝ) : gibbsCov N G J F H = gibbsCov N G J H F := by
  have h1 : (fun σ => F σ * H σ) = (fun σ => H σ * F σ) := funext fun σ => mul_comm _ _
  unfold gibbsCov
  rw [h1, mul_comm (gibbsExp N G J F)]

theorem energy_comp_bij {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J0 : ℝ) (g : V → V) (hbij : Function.Bijective g) (hadj : ∀ p q, G.Adj p q ↔ G.Adj (g p) (g q))
    (σ : Config N V) : energy G (uniform J0) (σ ∘ g) = energy G (uniform J0) σ := by
  let θ : V ≃ V := Equiv.ofBijective g hbij
  have hθ1 : ∀ p, g (θ.symm p) = p := fun p => θ.apply_symm_apply p
  have hθ2 : ∀ p, θ.symm (g p) = p := fun p => θ.symm_apply_apply p
  unfold energy
  simp only [bond_comp]
  have hmem : ∀ e ∈ G.edgeFinset, Sym2.map g e ∈ G.edgeFinset := by
    intro e he
    induction e using Sym2.ind with
    | h p q =>
      rw [Sym2.map_mk]
      exact SimpleGraph.mem_edgeFinset.mpr ((hadj p q).mp (SimpleGraph.mem_edgeFinset.mp he))
  have hmem' : ∀ e ∈ G.edgeFinset, Sym2.map θ.symm e ∈ G.edgeFinset := by
    intro e he
    induction e using Sym2.ind with
    | h p q =>
      rw [Sym2.map_mk]
      apply SimpleGraph.mem_edgeFinset.mpr
      apply (hadj (θ.symm p) (θ.symm q)).mpr
      rw [hθ1, hθ1]
      exact SimpleGraph.mem_edgeFinset.mp he
  have hinv1 : ∀ e : Sym2 V, Sym2.map θ.symm (Sym2.map g e) = e := by
    intro e
    induction e using Sym2.ind with
    | h p q => simp only [Sym2.map_mk, hθ2]
  have hinv2 : ∀ e : Sym2 V, Sym2.map g (Sym2.map θ.symm e) = e := by
    intro e
    induction e using Sym2.ind with
    | h p q => simp only [Sym2.map_mk, hθ1]
  exact Finset.sum_nbij' (Sym2.map g) (Sym2.map θ.symm) hmem hmem' (fun e _ => hinv1 e)
    (fun e _ => hinv2 e) (fun e _ => rfl)

theorem gibbsExp_comp_bij {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J0 : ℝ) (g : V → V) (hbij : Function.Bijective g)
    (hadj : ∀ p q, G.Adj p q ↔ G.Adj (g p) (g q)) (F : Config N V → ℝ) :
    gibbsExp N G (uniform J0) (fun σ => F (σ ∘ g)) = gibbsExp N G (uniform J0) F := by
  have := omega_isProbabilityMeasure N hN
  let eθ : V ≃ V := (Equiv.ofBijective g hbij).symm
  have hmp := measurePreserving_arrowCongr' (fun _ : V => omega N) (fun _ : V => omega N) eθ
    (MeasurableEquiv.refl (Sph N)) (fun _ => MeasurePreserving.id (omega N))
  have hcomp : ∀ σ : Config N V,
      MeasurableEquiv.arrowCongr' eθ (MeasurableEquiv.refl (Sph N)) σ = σ ∘ g := fun σ => rfl
  have h1 := hmp.integral_comp' (fun σ => F σ * Real.exp (energy G (uniform J0) σ))
  simp only [hcomp, energy_comp_bij G J0 g hbij hadj] at h1
  simp only [gibbsExp]
  congr 1

theorem gibbsCov_map_bij {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J0 : ℝ) (g : V → V) (hbij : Function.Bijective g)
    (hadj : ∀ p q, G.Adj p q ↔ G.Adj (g p) (g q)) (a b : Sym2 V) :
    gibbsCov N G (uniform J0) (bond (Sym2.map g a)) (bond (Sym2.map g b))
      = gibbsCov N G (uniform J0) (bond a) (bond b) := by
  have ha : bond (N := N) (Sym2.map g a) = fun σ => bond a (σ ∘ g) :=
    funext fun σ => (bond_comp g a σ).symm
  have hb : bond (N := N) (Sym2.map g b) = fun σ => bond b (σ ∘ g) :=
    funext fun σ => (bond_comp g b σ).symm
  have e1 : (fun σ => bond (N := N) (Sym2.map g a) σ * bond (Sym2.map g b) σ)
      = fun σ => bond a (σ ∘ g) * bond b (σ ∘ g) := funext fun σ => by simp only [bond_comp]
  have hab : gibbsExp N G (uniform J0) (fun σ => bond a (σ ∘ g) * bond b (σ ∘ g))
      = gibbsExp N G (uniform J0) (fun σ => bond a σ * bond b σ) :=
    gibbsExp_comp_bij hN G J0 g hbij hadj (fun σ => bond a σ * bond b σ)
  unfold gibbsCov
  rw [e1, hab, ha, hb, gibbsExp_comp_bij hN G J0 g hbij hadj (bond a),
    gibbsExp_comp_bij hN G J0 g hbij hadj (bond b)]

/-! ### Theorem 6.34(a) on P_3 × P_3 -/

theorem hub_pos {N : ℕ} (hN34 : N = 3 ∨ N = 4) (hW : hWeak N) (md : StripModes)
    (hId : hStripIdentity N md) (hCert : hStripCert N md) (hH : hHub N) (hL : hLBu N) (J : ℝ) (hJ : 0 < J) :
    0 < gibbsCov N grid33 (uniform J) (bond b0) (bond sN) := by
  have hb0 : b0 ∈ grid33.edgeSet := (SimpleGraph.mem_edgeSet grid33).mpr (by decide +kernel)
  have hsN : sN ∈ grid33.edgeSet := (SimpleGraph.mem_edgeSet grid33).mpr (by decide +kernel)
  have hne : b0 ≠ sN := by decide +kernel
  have hnsc : ¬ seriesCorner 3 b0 sN := by
    unfold seriesCorner isCorner
    decide +kernel
  have hreg : regularPair 3 b0 sN := by
    unfold regularPair sameColumn endVertical
    decide +kernel
  obtain ⟨c3, c4, h3, h4⟩ := cover_thm
  have htop : 20 ≤ stripTop N := by
    rcases hN34 with rfl | rfl
    · exact h3
    · exact h4
  have hcases : J ≤ 1 / 100 ∨ (99 / 10000 ≤ J ∧ J ≤ 20) ∨ (20 ≤ J ∧ J ≤ 10068 / 100) ∨
      (N = 3 ∧ 80 ≤ J) ∨ (N = 4 ∧ 100 ≤ J) := by
    rcases hN34 with rfl | rfl
    · rcases c3 J hJ with h | h | h | h
      · exact Or.inl h
      · exact Or.inr (Or.inl h)
      · exact Or.inr (Or.inr (Or.inl h))
      · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, h⟩)))
    · rcases c4 J hJ with h | h | h | h
      · exact Or.inl h
      · exact Or.inr (Or.inl h)
      · exact Or.inr (Or.inr (Or.inl h))
      · exact Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, h⟩)))
  rcases hcases with h | h | h | h | h
  · exact hW 3 le_rfl J hJ h b0 hb0 sN hsN hne hnsc
  · have hhi : J ≤ stripTop N := le_trans h.2 htop
    obtain ⟨hcv, hid⟩ := hId 3 le_rfl J h.1 hhi b0 hb0 sN hsN hne hreg
    obtain ⟨m0, hC⟩ := hCert
    have hc := hC 3 le_rfl J h.1 hhi b0 hb0 sN hsN hne hreg
    have hpos := criterion_thm (md 3 J b0 sN) (m0 J) hid hc.1 hc.2
    rw [hcv] at hpos
    exact hpos
  · exact hH J h.1 h.2
  · have hl := hL.1 h.1 J h.2
    nlinarith [sq_nonneg J]
  · have hl := hL.2 h.1 J h.2
    nlinarith [sq_nonneg J]

theorem hub_nonneg {N : ℕ} (hN34 : N = 3 ∨ N = 4) (hW : hWeak N) (md : StripModes)
    (hId : hStripIdentity N md) (hCert : hStripCert N md) (hH : hHub N) (hL : hLBu N) (J : ℝ) (hJ : 0 ≤ J) :
    0 ≤ gibbsCov N grid33 (uniform J) (bond b0) (bond sN) := by
  have hN : 0 < N := by rcases hN34 with rfl | rfl <;> norm_num
  rcases le_iff_eq_or_lt.mp hJ with h0 | hpos
  · subst h0
    apply gibbsCov_nonneg_of_shift hN grid33 (uniform 0) b0 sN
    intro ε hε
    have hfun : (fun g : Sym2 (Fin 3 × Fin 3) => (uniform 0 : Sym2 (Fin 3 × Fin 3) → ℝ) g + ε)
        = uniform ε := by
      funext g
      simp only [uniform, zero_add]
    rw [hfun]
    exact (hub_pos hN34 hW md hId hCert hH hL ε hε).le
  · exact (hub_pos hN34 hW md hId hCert hH hL J hpos).le

theorem G2_P3P3_thm (N : ℕ) : G2_P3P3_statement N := by
  unfold G2_P3P3_statement
  intro hN34 hS hSh hRP hW md hId hCert hH hL J hJ e he f hf hef
  have hN : 0 < N := by rcases hN34 with rfl | rfl <;> norm_num
  have hled := ledger_thm
  unfold ledger_statement at hled
  obtain ⟨hE, hd4, horb, -, -, h6, h7, h8a, ⟨hD1, hD2⟩, hc9⟩ := hled
  obtain ⟨hnbNE, hnbNW, hnbSE⟩ := h6
  obtain ⟨h7NE, h7NW, h7SE1, h7SE2⟩ := h7
  have hmir := mirror33_thm N hRP J hJ
  have hhub := hub_nonneg hN34 hW md hId hCert hH hL J hJ
  have hferro : Ferro grid33 (uniform J) := fun _ _ => hJ
  have hshared : ∀ a b : Sym2 (Fin 3 × Fin 3), a ∈ grid33.edgeSet → b ∈ grid33.edgeSet → a ≠ b →
      (∃ v, v ∈ a ∧ v ∈ b) → G2pair N grid33 (uniform J) a b :=
    fun a b ha hb hab hv => hSh (Fin 3 × Fin 3) grid33 (uniform J) hferro a ha b hb hab hv
  have eb0 : b0 ∈ grid33.edgeSet := (SimpleGraph.mem_edgeSet grid33).mpr (by decide +kernel)
  have eb1 : b1 ∈ grid33.edgeSet := (SimpleGraph.mem_edgeSet grid33).mpr (by decide +kernel)
  have eb7 : b7 ∈ grid33.edgeSet := (SimpleGraph.mem_edgeSet grid33).mpr (by decide +kernel)
  have esN : sN ∈ grid33.edgeSet := (SimpleGraph.mem_edgeSet grid33).mpr (by decide +kernel)
  have esE : sE ∈ grid33.edgeSet := (SimpleGraph.mem_edgeSet grid33).mpr (by decide +kernel)
  have esS : sS ∈ grid33.edgeSet := (SimpleGraph.mem_edgeSet grid33).mpr (by decide +kernel)
  -- the corner identity at NE and NW (observable s_{b_0}) and at SE (observables s_{s_E} and s_{s_N})
  have hcNE := corner_thm N hS (Fin 3 × Fin 3) grid33 (uniform J) vNE vE vN (by decide +kernel) hnbNE rfl
    (bond b0) (measurable_bond b0) ⟨1, fun σ => abs_bond_le b0 σ⟩
    (bond_dependsOnly _ b0 (fun x hx => by
      show x ≠ vNE
      rintro rfl
      exact h7NE hx))
  have hcNW := corner_thm N hS (Fin 3 × Fin 3) grid33 (uniform J) vNW vN vW (by decide +kernel) hnbNW rfl
    (bond b0) (measurable_bond b0) ⟨1, fun σ => abs_bond_le b0 σ⟩
    (bond_dependsOnly _ b0 (fun x hx => by
      show x ≠ vNW
      rintro rfl
      exact h7NW hx))
  have hcSE1 := corner_thm N hS (Fin 3 × Fin 3) grid33 (uniform J) vSE vS vE (by decide +kernel) hnbSE rfl
    (bond sE) (measurable_bond sE) ⟨1, fun σ => abs_bond_le sE σ⟩
    (bond_dependsOnly _ sE (fun x hx => by
      show x ≠ vSE
      rintro rfl
      exact h7SE1 hx))
  have hcSE2 := corner_thm N hS (Fin 3 × Fin 3) grid33 (uniform J) vSE vS vE (by decide +kernel) hnbSE rfl
    (bond sN) (measurable_bond sN) ⟨1, fun σ => abs_bond_le sN σ⟩
    (bond_dependsOnly _ sN (fun x hx => by
      show x ≠ vSE
      rintro rfl
      exact h7SE2 hx))
  have hb0s : b0 = s(vSE, vS) := Sym2.eq_swap
  have hb2s : b2 = s(vNE, vE) := Sym2.eq_swap
  have hb4s : b4 = s(vNW, vN) := Sym2.eq_swap
  -- the twelve representatives
  have p1 : G2pair N grid33 (uniform J) b0 b7 :=
    hshared b0 b7 eb0 eb7 (by decide +kernel) ⟨vS, by decide +kernel, by decide +kernel⟩
  have p2 : G2pair N grid33 (uniform J) b0 b1 :=
    hshared b0 b1 eb0 eb1 (by decide +kernel) ⟨vSE, by decide +kernel, by decide +kernel⟩
  have p3 : G2pair N grid33 (uniform J) b0 sS :=
    hshared b0 sS eb0 esS (by decide +kernel) ⟨vS, by decide +kernel, by decide +kernel⟩
  have p4 : G2pair N grid33 (uniform J) sN sS :=
    hshared sN sS esN esS (by decide +kernel) ⟨vC, by decide +kernel, by decide +kernel⟩
  have p5 : G2pair N grid33 (uniform J) sN sE :=
    hshared sN sE esN esE (by decide +kernel) ⟨vC, by decide +kernel, by decide +kernel⟩
  have p8 : G2pair N grid33 (uniform J) b0 b2 := by
    unfold G2pair
    rw [gibbsCov_comm, hb2s, hcNE, gibbsCov_comm]
    exact hmir.1
  have p9 : G2pair N grid33 (uniform J) b0 b4 := by
    unfold G2pair
    rw [gibbsCov_comm, hb4s, hcNW, gibbsCov_comm]
    exact hmir.2
  have p10 : G2pair N grid33 (uniform J) b0 sE := by
    unfold G2pair
    rw [hb0s, hcSE1]
    exact hshared b1 sE eb1 esE (by decide +kernel) ⟨vE, h8a.1, h8a.2⟩
  have p12 : G2pair N grid33 (uniform J) b0 sW := by
    have hinvD : ∀ p : Fin 3 × Fin 3, reflDiag (reflDiag p) = p := by decide +kernel
    have hbijD : Function.Bijective reflDiag :=
      Function.bijective_iff_has_inverse.mpr ⟨reflDiag, hinvD, hinvD⟩
    unfold G2pair
    rw [← hD1, ← hD2, gibbsCov_map_bij hN grid33 J reflDiag hbijD (fun p q => (hc9 p q).2.2),
      show b1 = s(vSE, vE) from rfl, ← hcSE2, ← hb0s]
    exact hhub
  have hrep : ∀ r ∈ reps, G2pair N grid33 (uniform J) r.1 r.2 := by
    intro r hr
    simp only [reps, List.mem_cons, List.not_mem_nil, or_false] at hr
    rcases hr with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    exacts [p1, p2, p3, p4, p5, hmir.1, hmir.2, p8, p9, p10, hhub, p12]
  -- transport along the orbit of (e, f)
  have he' : e ∈ edges33 := by
    rw [← hE]
    exact SimpleGraph.mem_edgeFinset.mpr he
  have hf' : f ∈ edges33 := by
    rw [← hE]
    exact SimpleGraph.mem_edgeFinset.mpr hf
  have hlen := horb e he' f hf' hef
  obtain ⟨r, hrf⟩ := List.exists_mem_of_length_pos (lt_of_lt_of_eq Nat.zero_lt_one hlen.symm)
  simp only [List.mem_filter, List.any_eq_true] at hrf
  obtain ⟨hr, g, hg, hdec⟩ := hrf
  have hsp := of_decide_eq_true hdec
  obtain ⟨hbij, hadj⟩ := hd4 g hg
  simp only [samePair, pairMap] at hsp
  rcases hsp with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · rw [← h1, ← h2]
    unfold G2pair
    rw [gibbsCov_map_bij hN grid33 J g hbij hadj]
    exact hrep r hr
  · rw [← h1, ← h2]
    unfold G2pair
    rw [gibbsCov_comm, gibbsCov_map_bij hN grid33 J g hbij hadj]
    exact hrep r hr

/-! ### Theorem 1.4(ii) on P_3 × P_n -/

theorem strip_row_mem {n : ℕ} (r : Fin 3) (j j' : Fin n) (hjj : j.val + 1 = j'.val ∨ j'.val + 1 = j.val) :
    s((r, j), (r, j')) ∈ (strip n).edgeSet := by
  rw [SimpleGraph.mem_edgeSet]
  refine ⟨fun h => ?_, ?_⟩
  · have h2 : j = j' := congrArg Prod.snd h
    omega
  · rcases hjj with h | h
    · exact Or.inl (Or.inl ⟨rfl, h⟩)
    · exact Or.inr (Or.inl ⟨rfl, h⟩)

theorem strip_corner_nbr {n : ℕ} (r : Fin 3) (j j' : Fin n) (hr : r = 0 ∨ r = 2)
    (hj : (j.val = 0 ∧ j'.val = 1) ∨ (j.val + 1 = n ∧ j'.val + 2 = n)) :
    (strip n).neighborFinset (r, j) = {((1 : Fin 3), j), (r, j')} := by
  ext ⟨a, b⟩
  rw [SimpleGraph.mem_neighborFinset, Finset.mem_insert, Finset.mem_singleton]
  simp only [strip, SimpleGraph.fromRel_adj, ne_eq, Prod.mk.injEq]
  omega

theorem row_edge_ne_vUp {n : ℕ} (r : Fin 3) (j j' k : Fin n) : s((r, j), (r, j')) ≠ vUp k := by
  intro h
  rw [vUp, Sym2.eq_iff] at h
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact absurd ((Prod.mk.inj h1).1.symm.trans (Prod.mk.inj h2).1) (by decide)
  · exact absurd ((Prod.mk.inj h1).1.symm.trans (Prod.mk.inj h2).1) (by decide)

theorem row_edge_ne_vDown {n : ℕ} (r : Fin 3) (j j' k : Fin n) : s((r, j), (r, j')) ≠ vDown k := by
  intro h
  rw [vDown, Sym2.eq_iff] at h
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact absurd ((Prod.mk.inj h1).1.symm.trans (Prod.mk.inj h2).1) (by decide)
  · exact absurd ((Prod.mk.inj h1).1.symm.trans (Prod.mk.inj h2).1) (by decide)

theorem endVertical_form {n : ℕ} (hn : 3 ≤ n) {e : Sym2 (Fin 3 × Fin n)} (hev : endVertical n e) :
    ∃ (r : Fin 3) (j j' : Fin n), (r = 0 ∨ r = 2) ∧
      ((j.val = 0 ∧ j'.val = 1) ∨ (j.val + 1 = n ∧ j'.val + 2 = n)) ∧ e = s((r, j), ((1 : Fin 3), j)) := by
  obtain ⟨j, hj, he⟩ := hev
  have hj' : ∃ j' : Fin n, (j.val = 0 ∧ j'.val = 1) ∨ (j.val + 1 = n ∧ j'.val + 2 = n) := by
    rcases hj with h | h
    · exact ⟨⟨1, by omega⟩, Or.inl ⟨h, rfl⟩⟩
    · refine ⟨⟨n - 2, by omega⟩, Or.inr ⟨h, ?_⟩⟩
      show n - 2 + 2 = n
      omega
  obtain ⟨j', hj'⟩ := hj'
  rcases he with rfl | rfl
  · exact ⟨0, j, j', Or.inl rfl, hj', rfl⟩
  · exact ⟨2, j, j', Or.inr rfl, hj', Sym2.eq_swap⟩

theorem corner_step {N : ℕ} (hS : hSphereIso N) {n : ℕ} (J : ℝ) (r : Fin 3) (j j' : Fin n)
    (hr : r = 0 ∨ r = 2) (hj : (j.val = 0 ∧ j'.val = 1) ∨ (j.val + 1 = n ∧ j'.val + 2 = n))
    (f : Sym2 (Fin 3 × Fin n)) (hcf : (r, j) ∉ f) :
    gibbsCov N (strip n) (uniform J) (bond s((r, j), ((1 : Fin 3), j))) (bond f)
      = gibbsCov N (strip n) (uniform J) (bond s((r, j), (r, j'))) (bond f) := by
  have hxy : ((1 : Fin 3), j) ≠ (r, j') := by
    intro h
    have h2 : j = j' := congrArg Prod.snd h
    omega
  exact corner_thm N hS (Fin 3 × Fin n) (strip n) (uniform J) (r, j) ((1 : Fin 3), j) (r, j') hxy
    (strip_corner_nbr r j j' hr hj) rfl (bond f) (measurable_bond f) ⟨1, fun σ => abs_bond_le f σ⟩
    (bond_dependsOnly _ f (fun w hw => by
      show w ≠ (r, j)
      rintro rfl
      exact hcf hw))

theorem replace_end {N : ℕ} (hS : hSphereIso N) {n : ℕ} (hn : 3 ≤ n) (J : ℝ) {e f : Sym2 (Fin 3 × Fin n)}
    (hev : endVertical n e) (hsc : ¬ seriesCorner n e f) :
    ∃ h : Sym2 (Fin 3 × Fin n), h ∈ (strip n).edgeSet ∧ h ≠ f ∧ ¬ endVertical n h ∧ ¬ seriesCorner n h f ∧
      (∀ g, ¬ sameColumn n h g ∧ ¬ sameColumn n g h) ∧
      gibbsCov N (strip n) (uniform J) (bond e) (bond f) = gibbsCov N (strip n) (uniform J) (bond h) (bond f) := by
  obtain ⟨r, j, j', hr, hj, rfl⟩ := endVertical_form hn hev
  have hc : isCorner n (r, j) := ⟨hr, hj.elim (fun h => Or.inl h.1) (fun h => Or.inr h.1)⟩
  have hcf : (r, j) ∉ f := fun hm => hsc ⟨(r, j), hc, Sym2.mem_mk_left _ _, hm⟩
  have hnotv : ∀ k : Fin n, s((r, j), (r, j')) ≠ vUp k ∧ s((r, j), (r, j')) ≠ vDown k :=
    fun k => ⟨row_edge_ne_vUp r j j' k, row_edge_ne_vDown r j j' k⟩
  refine ⟨s((r, j), (r, j')), strip_row_mem r j j' (by omega), ?_, ?_, ?_, ?_,
    corner_step hS J r j j' hr hj f hcf⟩
  · intro hh
    subst hh
    exact hcf (Sym2.mem_mk_left _ _)
  · rintro ⟨k, -, hk | hk⟩
    · exact (hnotv k).1 hk
    · exact (hnotv k).2 hk
  · rintro ⟨c, hc', hch, hcf'⟩
    rw [Sym2.mem_iff] at hch
    rcases hch with rfl | rfl
    · exact hcf hcf'
    · obtain ⟨-, hcol⟩ := hc'
      change j'.val = 0 ∨ j'.val + 1 = n at hcol
      omega
  · intro g
    constructor
    · rintro ⟨k, ⟨hk, -⟩ | ⟨hk, -⟩⟩
      · exact (hnotv k).1 hk
      · exact (hnotv k).2 hk
    · rintro ⟨k, ⟨-, hk⟩ | ⟨-, hk⟩⟩
      · exact (hnotv k).2 hk
      · exact (hnotv k).1 hk

theorem stripD_thm (N : ℕ) : stripD_statement N := by
  unfold stripD_statement
  intro hN34 hS hW md hId hCert hSp hCP n hn J hJ0 hJ20 e he f hf hef
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
    · by_cases hsame : sameColumn n e f
      · apply hSp n hn J hlo hhi e he f hf hef
        obtain ⟨j, hj⟩ := hsame
        have hjv : e = vUp j ∨ e = vDown j := by
          rcases hj with ⟨h1, -⟩ | ⟨h1, -⟩
          · exact Or.inl h1
          · exact Or.inr h1
        refine ⟨j, ?_, ?_, hj⟩
        · by_contra h0
          exact hev ⟨j, Or.inl (by omega), hjv⟩
        · by_contra h1
          exact hev ⟨j, Or.inr (by omega), hjv⟩
      · exact hreg e he f hf hef ⟨hsame, hev, hfv⟩

theorem strip3_thm (N : ℕ) : strip3_statement N := by
  unfold strip3_statement
  intro hN34 hS hW md hId hCert hSp hCP J hJ0 hJ20 e he f hf hef
  exact stripD_thm N hN34 hS hW md hId hCert hSp hCP 3 le_rfl J hJ0 hJ20 e he f hf hef

end G2Kernel
