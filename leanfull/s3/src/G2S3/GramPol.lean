/-
G2S3.GramPol (stage S3, Part C1): polarization and (V1). The sphere integral of a product of D linear forms is a
nonnegative combination of Gram monomials (STATEMENTS_S3_v5.md, C1). Input from S1: `sphere_moment`,
∫ ⟪w, z⟫^n ω(dz) = |w|^n μ_n, with μ_odd = 0 and μ_even > 0.
Polarization: Σ_ε (Π ε_l) (Σ_l ε_l t_l)^D = K_D Π_l t_l with K_D > 0, since the sign sum of a list of indices is
Π_l (1 + (-1)^{count l}), which vanishes unless every index occurs an even number of times.
-/
import G2S1.Moments
import G2S3.RPCore

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

/-- the sign of a Boolean -/
def bsgn (b : Bool) : ℝ := if b then 1 else -1

/-- the sign sum of a list of indices -/
def signSum (D : ℕ) (M : List (Fin D)) : ℝ := ∑ ε : Fin D → Bool, (M.map fun i => bsgn (ε i)).prod

theorem list_prod_map_count (D : ℕ) (M : List (Fin D)) (g : Fin D → ℝ) :
    (M.map g).prod = ∏ l, g l ^ (M.count l) := by
  rw [Finset.prod_list_map_count]
  refine Finset.prod_subset (Finset.subset_univ _) (fun l _ hl => ?_)
  rw [List.mem_toFinset] at hl
  rw [List.count_eq_zero_of_not_mem hl, pow_zero]

theorem signSum_eq (D : ℕ) (M : List (Fin D)) : signSum D M = ∏ l, (1 + (-1 : ℝ) ^ (M.count l)) := by
  unfold signSum
  simp only [list_prod_map_count]
  rw [← Fintype.prod_sum (fun (l : Fin D) (b : Bool) => bsgn b ^ M.count l)]
  refine Finset.prod_congr rfl (fun l _ => ?_)
  rw [Fintype.sum_bool]
  simp [bsgn]

theorem signSum_nonneg (D : ℕ) (M : List (Fin D)) : 0 ≤ signSum D M := by
  rw [signSum_eq]
  refine Finset.prod_nonneg (fun l _ => ?_)
  rcases neg_one_pow_eq_or ℝ (M.count l) with h | h <;> rw [h] <;> norm_num

/-- the polarization constant -/
def polK (D : ℕ) : ℝ := ∑ φ : Fin D → Fin D, signSum D (List.finRange D ++ List.ofFn φ)

theorem count_finRange_append (D : ℕ) (M : List (Fin D)) (l : Fin D) :
    (List.finRange D ++ M).count l = 1 + M.count l := by
  rw [List.count_append, List.count_eq_one_of_mem (List.nodup_finRange D) (List.mem_finRange l)]

theorem polK_pos (D : ℕ) : 0 < polK D := by
  unfold polK
  have hid : signSum D (List.finRange D ++ List.ofFn id) = 2 ^ D := by
    rw [signSum_eq]
    have h2 : ∀ l : Fin D, (1 + (-1 : ℝ) ^ ((List.finRange D ++ List.ofFn id).count l)) = 2 := by
      intro l
      rw [count_finRange_append, List.ofFn_id,
        List.count_eq_one_of_mem (List.nodup_finRange D) (List.mem_finRange l)]
      norm_num
    rw [Finset.prod_congr rfl (fun l _ => h2 l), Finset.prod_const, Finset.card_univ, Fintype.card_fin]
  calc (0 : ℝ) < 2 ^ D := by positivity
    _ = signSum D (List.finRange D ++ List.ofFn id) := hid.symm
    _ ≤ ∑ φ : Fin D → Fin D, signSum D (List.finRange D ++ List.ofFn φ) :=
        Finset.single_le_sum (f := fun φ => signSum D (List.finRange D ++ List.ofFn φ))
          (fun φ _ => signSum_nonneg D _) (Finset.mem_univ id)

theorem surj_of_signSum_ne {D : ℕ} {φ : Fin D → Fin D} (h : signSum D (List.finRange D ++ List.ofFn φ) ≠ 0) :
    Function.Surjective φ := by
  intro l
  rw [signSum_eq] at h
  have hl := Finset.prod_ne_zero_iff.mp h l (Finset.mem_univ l)
  rw [count_finRange_append] at hl
  by_contra hne
  have h0 : (List.ofFn φ).count l = 0 := List.count_eq_zero_of_not_mem (fun hm => by
    obtain ⟨k, hk⟩ := List.mem_ofFn.mp hm
    exact hne ⟨k, hk⟩)
  rw [h0] at hl
  norm_num at hl

/-- **Polarization** -/
theorem polarization (D : ℕ) (t : Fin D → ℝ) :
    ∑ ε : Fin D → Bool, (∏ l, bsgn (ε l)) * (∑ l, bsgn (ε l) * t l) ^ D = polK D * ∏ l, t l := by
  have hpow : ∀ ε : Fin D → Bool, (∑ l, bsgn (ε l) * t l) ^ D
      = ∑ φ : Fin D → Fin D, (∏ k, bsgn (ε (φ k))) * ∏ k, t (φ k) := by
    intro ε
    rw [Fintype.sum_pow]
    refine Finset.sum_congr rfl (fun φ _ => ?_)
    rw [← Finset.prod_mul_distrib]
  simp only [hpow, Finset.mul_sum]
  rw [Finset.sum_comm]
  unfold polK
  rw [Finset.sum_mul]
  refine Finset.sum_congr rfl (fun φ _ => ?_)
  have hA : ∑ ε : Fin D → Bool, (∏ l, bsgn (ε l)) * ((∏ k, bsgn (ε (φ k))) * ∏ k, t (φ k))
      = signSum D (List.finRange D ++ List.ofFn φ) * ∏ k, t (φ k) := by
    unfold signSum
    rw [Finset.sum_mul]
    refine Finset.sum_congr rfl (fun ε _ => ?_)
    rw [List.map_append, List.prod_append, ← Fin.prod_univ_def, List.map_ofFn, List.prod_ofFn]
    simp only [Function.comp_apply]
    ring
  rw [hA]
  by_cases h0 : signSum D (List.finRange D ++ List.ofFn φ) = 0
  · rw [h0, zero_mul, zero_mul]
  · have hs := surj_of_signSum_ne h0
    have hb : Function.Bijective φ := ⟨Finite.injective_iff_surjective.mpr hs, hs⟩
    rw [hb.prod_comp t]

/-- the coefficients of (V1) -/
def polC (N D : ℕ) (p : Fin (D / 2) → Fin D × Fin D) : ℝ :=
  muMom N D / polK D * signSum D (List.finRange D ++ List.ofFn (fun k => (p k).1) ++ List.ofFn (fun k => (p k).2))

theorem muMom_nonneg {N : ℕ} (hN : 1 ≤ N) (D : ℕ) : 0 ≤ muMom N D := by
  rcases Nat.even_or_odd D with ⟨k, hk⟩ | ⟨k, hk⟩
  · rw [hk, ← two_mul]; exact (muMom_even_pos hN k).le
  · rw [hk, muMom_odd]

theorem polC_nonneg {N : ℕ} (hN : 1 ≤ N) (D : ℕ) (p : Fin (D / 2) → Fin D × Fin D) : 0 ≤ polC N D p :=
  mul_nonneg (div_nonneg (muMom_nonneg hN D) (polK_pos D).le) (signSum_nonneg D _)

/-- the sign sum of a pair sequence, as a sum of products -/
theorem signSum_pairs (D m : ℕ) (p : Fin m → Fin D × Fin D) :
    signSum D (List.finRange D ++ List.ofFn (fun k => (p k).1) ++ List.ofFn (fun k => (p k).2))
      = ∑ ε : Fin D → Bool, (∏ l, bsgn (ε l)) * ∏ k, (bsgn (ε (p k).1) * bsgn (ε (p k).2)) := by
  unfold signSum
  refine Finset.sum_congr rfl (fun ε _ => ?_)
  rw [List.map_append, List.map_append, List.prod_append, List.prod_append, ← Fin.prod_univ_def, List.map_ofFn,
    List.map_ofFn, List.prod_ofFn, List.prod_ofFn, Finset.prod_mul_distrib]
  simp only [Function.comp_apply]
  ring

theorem abs_inner_sph_le {N : ℕ} (w : Amb N) (z : Sph N) : |@inner ℝ (Amb N) _ w (z : Amb N)| ≤ ‖w‖ := by
  have h := abs_real_inner_le_norm w (z : Amb N)
  have hz : ‖(z : Amb N)‖ = 1 := norm_eq_of_mem_sphere z
  rw [hz, mul_one] at h
  exact h

theorem integrable_inner_pow {N : ℕ} (hN : 1 ≤ N) (w : Amb N) (n : ℕ) :
    Integrable (fun z : Sph N => @inner ℝ (Amb N) _ w (z : Amb N) ^ n) (omega N) := by
  have := omega_isProbabilityMeasure N (by omega)
  refine integrable_of_abs_le ?_ (‖w‖ ^ n) (fun z => ?_)
  · exact ((continuous_const.inner continuous_subtype_val).pow n).measurable
  · rw [abs_pow]
    exact pow_le_pow_left₀ (abs_nonneg _) (abs_inner_sph_le w z) n

/-- **(V1)**: the sphere integral of a product of linear forms is a nonnegative combination of Gram monomials -/
theorem sphere_prod_inner {N : ℕ} (hN : 1 ≤ N) (D : ℕ) (a : Fin D → Amb N) :
    ∫ z : Sph N, ∏ l, @inner ℝ (Amb N) _ (a l) (z : Amb N) ∂(omega N)
      = ∑ p : Fin (D / 2) → Fin D × Fin D, polC N D p * ∏ k, @inner ℝ (Amb N) _ (a (p k).1) (a (p k).2) := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  set v : (Fin D → Bool) → Amb N := fun ε => ∑ l, bsgn (ε l) • a l with hv
  have hK := (polK_pos D).ne'
  -- the pointwise polarization
  have hpt : ∀ z : Sph N, ∏ l, @inner ℝ (Amb N) _ (a l) (z : Amb N)
      = (1 / polK D) * ∑ ε : Fin D → Bool, (∏ l, bsgn (ε l)) * @inner ℝ (Amb N) _ (v ε) (z : Amb N) ^ D := by
    intro z
    have hP := polarization D (fun l => @inner ℝ (Amb N) _ (a l) (z : Amb N))
    have hin : ∀ ε, @inner ℝ (Amb N) _ (v ε) (z : Amb N)
        = ∑ l, bsgn (ε l) * @inner ℝ (Amb N) _ (a l) (z : Amb N) := by
      intro ε
      simp only [hv, sum_inner, real_inner_smul_left]
    simp only [hin]
    rw [hP]
    field_simp
  simp only [hpt]
  rw [integral_const_mul, integral_finsetSum _ (fun ε _ => (integrable_inner_pow hN (v ε) D).const_mul _)]
  simp only [integral_const_mul, sphere_moment hN]
  -- the parity of D
  rcases Nat.even_or_odd D with ⟨m, hm⟩ | ⟨m, hm⟩
  · -- D = 2 m: the Gram expansion of |v|^{2m}
    have hD2 : D / 2 = m := by omega
    have hnorm : ∀ ε, ‖v ε‖ ^ D = ∑ p : Fin (D / 2) → Fin D × Fin D,
        ∏ k, (bsgn (ε (p k).1) * bsgn (ε (p k).2) * @inner ℝ (Amb N) _ (a (p k).1) (a (p k).2)) := by
      intro ε
      have h1 : ‖v ε‖ ^ D = (@inner ℝ (Amb N) _ (v ε) (v ε)) ^ (D / 2) := by
        rw [real_inner_self_eq_norm_sq, ← pow_mul, hD2, show 2 * m = D by omega]
      have h2 : @inner ℝ (Amb N) _ (v ε) (v ε) = ∑ q : Fin D × Fin D,
          bsgn (ε q.1) * bsgn (ε q.2) * @inner ℝ (Amb N) _ (a q.1) (a q.2) := by
        simp only [hv, sum_inner, inner_sum, real_inner_smul_left, real_inner_smul_right]
        rw [Fintype.sum_prod_type]
        refine Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun j _ => ?_))
        rw [real_inner_comm (a i) (a j)]
        dsimp only
        ring
      rw [h1, h2, Fintype.sum_pow]
    have hterm : ∀ ε : Fin D → Bool, (∏ l, bsgn (ε l)) * (‖v ε‖ ^ D * muMom N D)
        = ∑ p : Fin (D / 2) → Fin D × Fin D, muMom N D * ((∏ l, bsgn (ε l)) *
            ∏ k, (bsgn (ε (p k).1) * bsgn (ε (p k).2))) * ∏ k, @inner ℝ (Amb N) _ (a (p k).1) (a (p k).2) := by
      intro ε
      rw [hnorm ε, Finset.sum_mul, Finset.mul_sum]
      refine Finset.sum_congr rfl (fun p _ => ?_)
      rw [Finset.prod_mul_distrib]
      ring
    simp only [hterm, Finset.mul_sum]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun p _ => ?_)
    unfold polC
    rw [signSum_pairs, Finset.mul_sum, Finset.sum_mul]
    refine Finset.sum_congr rfl (fun ε _ => ?_)
    ring
  · -- D odd: both sides vanish
    have h0 : muMom N D = 0 := by rw [hm, muMom_odd]
    simp only [h0, mul_zero, Finset.sum_const_zero, polC, zero_div, zero_mul]

end G2S3

#print axioms G2S3.signSum_eq
#print axioms G2S3.polK_pos
#print axioms G2S3.polarization
#print axioms G2S3.polC_nonneg
#print axioms G2S3.sphere_prod_inner
