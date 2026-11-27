/-
G2S1.Cycle (stage S1): H5 (`hCycleZ`) for the paper's data, the ring formula Z_{C_n} = Σ_c d_c ∏_g k_c(J_g).
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 3.1 (the formula for Z_C).
- `cycF_integral`: ∫ Π_{a_0}(σ_0,σ_1) ⋯ Π_{a_{m-1}}(σ_{m-1},σ_m) Π_{a_m}(σ_m,σ_0) ∏ ω(dσ_i) = [a constant = c] d_c, by
  integrating out the last vertex with (2) (Fubini through `measurePreserving_piFinSuccAbove` at `Fin.last`).
- the edges of `cycleGraph (m+2)` are s(j, j+1), j : Fin (m+2), each once (m ≥ 1); with display (4) this gives
  W(ℓ) = [ℓ constant = c] d_c and `hCycleZ_conc`.
-/
import G2S1.Labels

noncomputable section
open Real Finset MeasureTheory

namespace G2Kernel

/-! ### The cycle integral -/

/-- the cycle integrand on Fin (m+1): ∏_{i<m} Π_{a i}(σ_i, σ_{i+1}) · Π_{a m}(σ_m, σ_0) -/
def cycF (N m : ℕ) (a : Fin (m + 1) → ℕ) (σ : Fin (m + 1) → Sph N) : ℝ :=
  (∏ i : Fin m, zonal N (a i.castSucc) (σ i.castSucc) (σ i.succ)) * zonal N (a (Fin.last m)) (σ (Fin.last m)) (σ 0)

theorem continuous_zonal_coord (N l : ℕ) {ι : Type*} (i j : ι) :
    Continuous (fun σ : ι → Sph N => zonal N l (σ i) (σ j)) := by
  have h1 : Continuous (fun σ : ι → Sph N => σ i) := continuous_apply i
  have h2 : Continuous (fun σ : ι → Sph N => σ j) := continuous_apply j
  exact (continuous_zonal N l).comp (h1.prodMk h2)

theorem continuous_cycF (N m : ℕ) (a : Fin (m + 1) → ℕ) : Continuous (cycF N m a) := by
  unfold cycF
  refine (continuous_finset_prod _ (fun i _ => ?_)).mul ?_
  · exact continuous_zonal_coord N (a i.castSucc) i.castSucc i.succ
  · exact continuous_zonal_coord N (a (Fin.last m)) (Fin.last m) 0

theorem abs_cycF_le {N : ℕ} (hN : 2 ≤ N) (m : ℕ) (a : Fin (m + 1) → ℕ) (σ : Fin (m + 1) → Sph N) :
    |cycF N m a σ| ≤ (∏ i : Fin m, dConc N (a i.castSucc)) * dConc N (a (Fin.last m)) := by
  unfold cycF
  rw [abs_mul, Finset.abs_prod]
  exact mul_le_mul (Finset.prod_le_prod₀ (fun i _ => abs_nonneg _) (fun i _ => abs_zonal_le hN _ _ _))
    (abs_zonal_le hN _ _ _) (abs_nonneg _) (Finset.prod_nonneg (fun i _ => (dConc_pos_S1 hN _).le))

/-- the integrand at a configuration with a last vertex appended -/
theorem cycF_snoc (N m : ℕ) (a : Fin (m + 2) → ℕ) (τ : Fin (m + 1) → Sph N) (v : Sph N) :
    cycF N (m + 1) a (Fin.snoc τ v)
      = (∏ j : Fin m, zonal N (a j.castSucc.castSucc) (τ j.castSucc) (τ j.succ)) *
          (zonal N (a (Fin.last m).castSucc) (τ (Fin.last m)) v * zonal N (a (Fin.last (m + 1))) v (τ 0)) := by
  unfold cycF
  rw [Fin.prod_univ_castSucc]
  have h1 : ∀ j : Fin m, (Fin.snoc τ v : Fin (m + 2) → Sph N) j.castSucc.castSucc = τ j.castSucc := fun j =>
    Fin.snoc_castSucc (α := fun _ => Sph N) _ _ _
  have h2 : ∀ j : Fin m, (Fin.snoc τ v : Fin (m + 2) → Sph N) j.castSucc.succ = τ j.succ := by
    intro j
    rw [Fin.succ_castSucc]
    exact Fin.snoc_castSucc (α := fun _ => Sph N) _ _ _
  have h3 : (Fin.snoc τ v : Fin (m + 2) → Sph N) (Fin.last m).castSucc = τ (Fin.last m) :=
    Fin.snoc_castSucc (α := fun _ => Sph N) _ _ _
  have h4 : (Fin.snoc τ v : Fin (m + 2) → Sph N) (Fin.last m).succ = v := by
    rw [Fin.succ_last]
    exact Fin.snoc_last (α := fun _ => Sph N) _ _
  have h5 : (Fin.snoc τ v : Fin (m + 2) → Sph N) (Fin.last (m + 1)) = v := Fin.snoc_last (α := fun _ => Sph N) _ _
  have h6 : (Fin.snoc τ v : Fin (m + 2) → Sph N) 0 = τ 0 := by
    rw [show (0 : Fin (m + 2)) = (0 : Fin (m + 1)).castSucc from rfl]
    exact Fin.snoc_castSucc (α := fun _ => Sph N) _ _ _
  simp only [h1, h2, h3, h4, h5, h6]
  ring

/-- the ring integral: [a constant = c] d_c -/
theorem cycF_integral {N : ℕ} (hN : 2 ≤ N) : ∀ (m : ℕ) (a : Fin (m + 1) → ℕ),
    ∫ σ, cycF N m a σ ∂(Measure.pi fun _ : Fin (m + 1) => omega N)
      = if ∀ i, a i = a 0 then dConc N (a 0) else 0 := by
  have hω := omega_isProbabilityMeasure N (by omega)
  intro m
  induction m with
  | zero =>
    intro a
    have hc : ∀ σ : Fin 1 → Sph N, cycF N 0 a σ = dConc N (a 0) := by
      intro σ
      unfold cycF
      simp only [Finset.univ_eq_empty, Finset.prod_empty, one_mul]
      rw [show Fin.last 0 = 0 from rfl, zonal_self hN]
    simp only [hc, integral_const, smul_eq_mul]
    rw [if_pos (fun i => by rw [Fin.fin_one_eq_zero i])]
    simp
  | succ m ih =>
    intro a
    set a' : Fin (m + 1) → ℕ := fun i => a i.castSucc with ha'
    -- Fubini at the last coordinate
    have hmp := measurePreserving_piFinSuccAbove (fun _ : Fin (m + 2) => omega N) (Fin.last (m + 1))
    set e := MeasurableEquiv.piFinSuccAbove (fun _ : Fin (m + 2) => Sph N) (Fin.last (m + 1)) with he_def
    have hesymm : ∀ p : Sph N × (Fin (m + 1) → Sph N), e.symm p = Fin.snoc p.2 p.1 := by
      intro p
      simp [e, MeasurableEquiv.piFinSuccAbove_symm_apply, Fin.insertNth_last']
      all_goals rfl
    have he : ∀ σ : Fin (m + 2) → Sph N, Fin.snoc (e σ).2 (e σ).1 = σ := by
      intro σ
      rw [← hesymm, MeasurableEquiv.symm_apply_apply]
    have hint : Integrable (fun p : Sph N × (Fin (m + 1) → Sph N) => cycF N (m + 1) a (Fin.snoc p.2 p.1))
        ((omega N).prod (Measure.pi fun _ : Fin (m + 1) => omega N)) := by
      refine integrable_of_abs_le ((continuous_cycF N (m + 1) a).measurable.comp ?_) _
        (fun p => abs_cycF_le hN (m + 1) a _)
      have : (fun p : Sph N × (Fin (m + 1) → Sph N) => (Fin.snoc p.2 p.1 : Fin (m + 2) → Sph N))
          = fun p => e.symm p := by
        funext p; rw [hesymm]
      rw [this]
      exact MeasurableEquiv.measurable _
    have step1 : ∫ σ, cycF N (m + 1) a σ ∂(Measure.pi fun _ : Fin (m + 2) => omega N)
        = ∫ p, cycF N (m + 1) a (Fin.snoc p.2 p.1) ∂((omega N).prod (Measure.pi fun _ : Fin (m + 1) => omega N)) := by
      rw [← hmp.integral_comp' (fun p => cycF N (m + 1) a (Fin.snoc p.2 p.1))]
      congr 1
      funext σ
      rw [he]
    rw [step1, integral_prod_symm _ hint]
    have step2 : ∀ τ : Fin (m + 1) → Sph N, ∫ v, cycF N (m + 1) a (Fin.snoc τ v) ∂(omega N)
        = (if a (Fin.last m).castSucc = a (Fin.last (m + 1)) then 1 else 0) * cycF N m a' τ := by
      intro τ
      simp only [cycF_snoc]
      rw [integral_const_mul, zonal_proj hN]
      unfold cycF
      simp only [ha']
      split_ifs with h
      · rw [h]; ring
      · ring
    simp only [step2]
    rw [integral_const_mul, ih a']
    simp only [ha']
    have hiff : (∀ i : Fin (m + 2), a i = a 0) ↔
        (a (Fin.last m).castSucc = a (Fin.last (m + 1)) ∧ ∀ i : Fin (m + 1), a i.castSucc = a (0 : Fin (m + 1)).castSucc) := by
      constructor
      · intro h
        exact ⟨by rw [h, h (Fin.last (m + 1))], fun i => by rw [h, h (0 : Fin (m + 1)).castSucc]⟩
      · rintro ⟨h1, h2⟩ i
        rw [show (0 : Fin (m + 2)) = (0 : Fin (m + 1)).castSucc from rfl]
        rcases Fin.eq_castSucc_or_eq_last i with ⟨j, rfl⟩ | rfl
        · exact h2 j
        · rw [← h1, h2 (Fin.last m)]
    by_cases h1 : a (Fin.last m).castSucc = a (Fin.last (m + 1))
    · by_cases h2 : ∀ i : Fin (m + 1), a i.castSucc = a (0 : Fin (m + 1)).castSucc
      · rw [if_pos h1, if_pos h2, if_pos (hiff.mpr ⟨h1, h2⟩), one_mul]
        rfl
      · rw [if_pos h1, if_neg h2, if_neg (fun h => h2 (hiff.mp h).2), mul_zero]
    · rw [if_neg h1, zero_mul, if_neg (fun h => h1 (hiff.mp h).1)]

end G2Kernel
