/-
G2Kernel.Proofs.MirrorProof: proof of `mirror33_statement` (module M6b, Lemma 6.1 for the mirror pairs
(b_0, b_3) and (b_0, b_5) of P_3 × P_3). Kernel proof, step L-b. The reflections reflH and reflAnti are involutive
graph automorphisms, so σ ↦ σ ∘ θ preserves the free measure (`measurePreserving_arrowCongr'`) and, at uniform
coupling, the energy; hence the Gibbs expectation of F(σ ∘ θ) equals that of F. Reflection positivity
(hRPGibbs) for F - c, with c = ⟨s_{b_0}⟩ and F = s_{b_0}, which depends only on the half containing b_0, gives
0 ≤ ⟨(F - c)(F∘θ - c)⟩ = Cov(F, F∘θ), and F∘θ is the bond energy of the mirror edge (ledger, conjunct 5).
-/
import G2Kernel.RPstep
import G2Kernel.Proofs.LedgerProof
import G2Kernel.Proofs.BlocksProof

noncomputable section
open MeasureTheory Real

namespace G2Kernel

theorem bond_comp {N : ℕ} {V : Type*} (θ : V → V) (g : Sym2 V) (σ : Config N V) :
    bond g (σ ∘ θ) = bond (Sym2.map θ g) σ := by
  induction g using Sym2.ind with
  | h p q => rfl

theorem energy_comp_auto {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J0 : ℝ) (θ : V → V) (hinv : ∀ p, θ (θ p) = p) (hadj : ∀ p q, G.Adj p q ↔ G.Adj (θ p) (θ q))
    (σ : Config N V) : energy G (uniform J0) (σ ∘ θ) = energy G (uniform J0) σ := by
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
  exact Finset.sum_nbij' (Sym2.map θ) (Sym2.map θ) hmem hmem (fun g _ => hinv2 g) (fun g _ => hinv2 g)
    (fun g _ => rfl)

theorem gibbsExp_comp_auto {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J0 : ℝ) (θ : V → V) (hinv : ∀ p, θ (θ p) = p)
    (hadj : ∀ p q, G.Adj p q ↔ G.Adj (θ p) (θ q)) (F : Config N V → ℝ) :
    gibbsExp N G (uniform J0) (fun σ => F (σ ∘ θ)) = gibbsExp N G (uniform J0) F := by
  have := omega_isProbabilityMeasure N hN
  let eθ : V ≃ V := ⟨θ, θ, hinv, hinv⟩
  have hmp := measurePreserving_arrowCongr' (fun _ : V => omega N) (fun _ : V => omega N) eθ
    (MeasurableEquiv.refl (Sph N)) (fun _ => MeasurePreserving.id (omega N))
  have hcomp : ∀ σ : Config N V,
      MeasurableEquiv.arrowCongr' eθ (MeasurableEquiv.refl (Sph N)) σ = σ ∘ θ := fun σ => rfl
  have h1 := hmp.integral_comp' (fun σ => F σ * Real.exp (energy G (uniform J0) σ))
  simp only [hcomp, energy_comp_auto G J0 θ hinv hadj] at h1
  simp only [gibbsExp]
  congr 1

theorem gibbsExp_centered {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (F H : Config N V → ℝ) (hF : Measurable F) (hH : Measurable H)
    (hFb : ∀ σ, |F σ| ≤ 1) (hHb : ∀ σ, |H σ| ≤ 1) (c : ℝ) :
    gibbsExp N G J (fun σ => (F σ - c) * (H σ - c))
      = gibbsExp N G J (fun σ => F σ * H σ) - c * gibbsExp N G J H - c * gibbsExp N G J F + c * c := by
  have := omega_isProbabilityMeasure N hN
  have : IsProbabilityMeasure (freeMeasure N V) := by
    unfold freeMeasure
    infer_instance
  have hZne := (partition_pos hN G J).ne'
  have hmw : Measurable (fun σ : Config N V => Real.exp (energy G J σ)) := (measurable_energy G J).exp
  have hbw : ∀ σ : Config N V, |Real.exp (energy G J σ)| ≤ Real.exp (∑ g ∈ G.edgeFinset, |J g|) :=
    fun σ => abs_exp_le (abs_energy_le G J σ)
  have iFH : Integrable (fun σ => F σ * H σ * Real.exp (energy G J σ)) (freeMeasure N V) :=
    integrable_of_abs_le ((hF.mul hH).mul hmw) _ (fun σ => by
      rw [mul_assoc]
      exact abs_one_mul_le (hFb σ) (abs_one_mul_le (hHb σ) (hbw σ)))
  have iH : Integrable (fun σ => H σ * Real.exp (energy G J σ)) (freeMeasure N V) :=
    integrable_of_abs_le (hH.mul hmw) _ (fun σ => abs_one_mul_le (hHb σ) (hbw σ))
  have iF : Integrable (fun σ => F σ * Real.exp (energy G J σ)) (freeMeasure N V) :=
    integrable_of_abs_le (hF.mul hmw) _ (fun σ => abs_one_mul_le (hFb σ) (hbw σ))
  have iw : Integrable (fun σ => Real.exp (energy G J σ)) (freeMeasure N V) := integrable_of_abs_le hmw _ hbw
  have i1 : Integrable (fun σ => F σ * H σ * Real.exp (energy G J σ) - c * (H σ * Real.exp (energy G J σ)))
      (freeMeasure N V) := iFH.sub (iH.const_mul c)
  have i2 : Integrable (fun σ => F σ * H σ * Real.exp (energy G J σ) - c * (H σ * Real.exp (energy G J σ))
      - c * (F σ * Real.exp (energy G J σ))) (freeMeasure N V) := i1.sub (iF.const_mul c)
  have e : (fun σ => (F σ - c) * (H σ - c) * Real.exp (energy G J σ))
      = fun σ => F σ * H σ * Real.exp (energy G J σ) - c * (H σ * Real.exp (energy G J σ))
          - c * (F σ * Real.exp (energy G J σ)) + c * c * Real.exp (energy G J σ) := by
    funext σ
    ring
  have hZ' : partition N G J = ∫ σ, Real.exp (energy G J σ) ∂(freeMeasure N V) := rfl
  simp only [gibbsExp]
  rw [e, integral_add i2 (iw.const_mul (c * c)), integral_sub i1 (iF.const_mul c),
    integral_sub iFH (iH.const_mul c), integral_const_mul, integral_const_mul, integral_const_mul, ← hZ']
  field

theorem cov_nonneg_of_rp {N : ℕ} (hN : 0 < N) {V : Type*} [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (J0 : ℝ) (θ : V → V) (hinv : ∀ p, θ (θ p) = p)
    (hadj : ∀ p q, G.Adj p q ↔ G.Adj (θ p) (θ q)) (F : Config N V → ℝ) (hFm : Measurable F)
    (hFb : ∀ σ, |F σ| ≤ 1)
    (hrp : ∀ c : ℝ, 0 ≤ gibbsExp N G (uniform J0) (fun σ => (F σ - c) * (F (σ ∘ θ) - c))) :
    0 ≤ gibbsCov N G (uniform J0) F (fun σ => F (σ ∘ θ)) := by
  have hsym := gibbsExp_comp_auto hN G J0 θ hinv hadj F
  have hθm : Measurable (fun σ : Config N V => σ ∘ θ) :=
    Measurable.of_eval (fun i => measurable_pi_apply (θ i))
  have hFθm : Measurable (fun σ : Config N V => F (σ ∘ θ)) := hFm.comp hθm
  have hc := hrp (gibbsExp N G (uniform J0) F)
  rw [gibbsExp_centered hN G (uniform J0) F (fun σ => F (σ ∘ θ)) hFm hFθm hFb (fun σ => hFb _), hsym] at hc
  simp only [gibbsCov]
  rw [hsym]
  linarith

theorem abs_sub_const_le {x c : ℝ} (hx : |x| ≤ 1) : |x - c| ≤ 1 + |c| := by
  obtain ⟨h1, h2⟩ := abs_le.mp hx
  obtain ⟨h3, h4⟩ := abs_le.mp (le_refl |c|)
  exact abs_le.mpr ⟨by linarith, by linarith⟩

theorem mirror33_thm (N : ℕ) : mirror33_statement N := by
  unfold mirror33_statement
  intro hRP J hJ
  unfold G2pair
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · have hV : Nonempty (Fin 3 × Fin 3) := ⟨(0, 0)⟩
    have h0 : freeMeasure 0 (Fin 3 × Fin 3) = 0 := freeMeasure_zero _
    constructor <;> simp [gibbsCov, gibbsExp, partition, h0]
  have hled := ledger_thm
  unfold ledger_statement at hled
  obtain ⟨-, -, -, -, ⟨h5H, h5A⟩, -, -, -, -, hc9⟩ := hled
  have hinvH : ∀ p : Fin 3 × Fin 3, reflH (reflH p) = p := by decide +kernel
  have hinvA : ∀ p : Fin 3 × Fin 3, reflAnti (reflAnti p) = p := by decide +kernel
  have hhalfH : ∀ x : Fin 3 × Fin 3, x ∈ b0 → 1 ≤ x.1.val := by decide +kernel
  have hhalfA : ∀ x : Fin 3 × Fin 3, x ∈ b0 → 2 ≤ x.1.val + x.2.val := by decide +kernel
  have hdH : DependsOnly halfH (bond (N := N) b0) := bond_dependsOnly halfH b0 (fun x hx => hhalfH x hx)
  have hdA : DependsOnly halfAnti (bond (N := N) b0) := bond_dependsOnly halfAnti b0 (fun x hx => hhalfA x hx)
  have hbnd : ∀ c : ℝ, ∃ B, ∀ σ : Config N (Fin 3 × Fin 3), |bond b0 σ - c| ≤ B :=
    fun c => ⟨1 + |c|, fun σ => abs_sub_const_le (abs_bond_le b0 σ)⟩
  have hmc : ∀ c : ℝ, Measurable (fun σ : Config N (Fin 3 × Fin 3) => bond b0 σ - c) :=
    fun c => (measurable_bond b0).sub measurable_const
  refine ⟨?_, ?_⟩
  · have h3 : (fun σ : Config N (Fin 3 × Fin 3) => bond b0 (σ ∘ reflH)) = bond b3 := by
      funext σ
      rw [bond_comp, h5H]
    have hcov := cov_nonneg_of_rp hN grid33 J reflH hinvH (fun p q => (hc9 p q).1) (bond b0)
      (measurable_bond b0) (fun σ => abs_bond_le b0 σ)
      (fun c => (hRP J hJ (fun σ => bond b0 σ - c) (hmc c) (hbnd c)).1
        (fun σ σ' h => by
          show bond b0 σ - c = bond b0 σ' - c
          rw [hdH σ σ' h]))
    rw [h3] at hcov
    exact hcov
  · have h5 : (fun σ : Config N (Fin 3 × Fin 3) => bond b0 (σ ∘ reflAnti)) = bond b5 := by
      funext σ
      rw [bond_comp, h5A]
    have hcov := cov_nonneg_of_rp hN grid33 J reflAnti hinvA (fun p q => (hc9 p q).2.1) (bond b0)
      (measurable_bond b0) (fun σ => abs_bond_le b0 σ)
      (fun c => (hRP J hJ (fun σ => bond b0 σ - c) (hmc c) (hbnd c)).2
        (fun σ σ' h => by
          show bond b0 σ - c = bond b0 σ' - c
          rw [hdA σ σ' h]))
    rw [h5] at hcov
    exact hcov

end G2Kernel
