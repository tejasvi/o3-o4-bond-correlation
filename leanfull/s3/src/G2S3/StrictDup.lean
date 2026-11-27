/-
G2S3.StrictDup (stage S3, Part B8): the duplicated explicit term of the strict corner inequality,
  int int (s_x^k - s'_x^k)(s_y^k - s'_y^k)(s_x.s_w + s'_x.s'_w)(s_w.s_y + s'_w.s'_y) = 2 / N^3,
by four symmetries (flip of s_w, exchange of the copies, flips of s'_y and s'_x) and `single_term`.
-/
import G2S3.StrictTerm

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

theorem BddMeas.congr {Z : Type*} [MeasurableSpace Z] {f g : Z → ℝ} (hf : BddMeas f) (h : ∀ z, g z = f z) :
    BddMeas g := by
  obtain ⟨hm, C, hC⟩ := hf
  have e : g = f := funext h
  exact ⟨e ▸ hm, C, fun z => (h z) ▸ hC z⟩

section Dup

variable {N : ℕ} {W : Type*} [Fintype W] [DecidableEq W]

/-- **The duplicated term**: `= 2 / N^3`. -/
theorem dup_term (hN : 0 < N) (k : Fin N) {x y w : W} (hxy : x ≠ y) (hxw : x ≠ w) (hyw : y ≠ w) :
    ∫ p, (cf k x p.1 - cf k x p.2) * (cf k y p.1 - cf k y p.2)
        * (dot (p.1 x) (p.1 w) + dot (p.2 x) (p.2 w)) * (dot (p.1 w) (p.1 y) + dot (p.2 w) (p.2 y))
      ∂((freeMeasure N W).prod (freeMeasure N W)) = 2 / (N : ℝ) ^ 3 := by
  have hprob := omega_isProbabilityMeasure N hN
  haveI : IsProbabilityMeasure (freeMeasure N W) := by unfold freeMeasure; infer_instance
  set P := freeMeasure N W with hP
  -- the building blocks
  set fx1 : Config N W × Config N W → ℝ := fun p => cf k x p.1
  set fx2 : Config N W × Config N W → ℝ := fun p => cf k x p.2
  set fy1 : Config N W × Config N W → ℝ := fun p => cf k y p.1
  set fy2 : Config N W × Config N W → ℝ := fun p => cf k y p.2
  set a1 : Config N W × Config N W → ℝ := fun p => dot (p.1 x) (p.1 w)
  set a2 : Config N W × Config N W → ℝ := fun p => dot (p.2 x) (p.2 w)
  set b1 : Config N W × Config N W → ℝ := fun p => dot (p.1 w) (p.1 y)
  set b2 : Config N W × Config N W → ℝ := fun p => dot (p.2 w) (p.2 y)
  have Bfx1 : BddMeas fx1 := (cf_bdd (N := N) k x).comp measurable_fst
  have Bfx2 : BddMeas fx2 := (cf_bdd (N := N) k x).comp measurable_snd
  have Bfy1 : BddMeas fy1 := (cf_bdd (N := N) k y).comp measurable_fst
  have Bfy2 : BddMeas fy2 := (cf_bdd (N := N) k y).comp measurable_snd
  have Ba1 : BddMeas a1 := (dotz_bdd (N := N) x w).comp measurable_fst
  have Ba2 : BddMeas a2 := (dotz_bdd (N := N) x w).comp measurable_snd
  have Bb1 : BddMeas b1 := (dotz_bdd (N := N) w y).comp measurable_fst
  have Bb2 : BddMeas b2 := (dotz_bdd (N := N) w y).comp measurable_snd
  have Bdx : BddMeas (fun p => fx1 p - fx2 p) := (Bfx1.add (Bfx2.const_mul (-1))).congr (fun p => by ring)
  have Bdy : BddMeas (fun p => fy1 p - fy2 p) := (Bfy1.add (Bfy2.const_mul (-1))).congr (fun p => by ring)
  have hwx : w ≠ x := fun h => hxw h.symm
  have hwy : w ≠ y := fun h => hyw h.symm
  have hyx : y ≠ x := fun h => hxy h.symm
  -- step 1: flip of s_w in the first copy
  have s1 : ∫ p, (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p + a2 p) * (b1 p + b2 p) ∂(P.prod P)
      = ∫ p, (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p * b1 p + a2 p * b2 p) ∂(P.prod P) := by
    refine integral_symm ((flipAt_mp hN w).prod (MeasurePreserving.id P))
      (((Bdx.mul Bdy).mul (Ba1.add Ba2)).mul (Bb1.add Bb2))
      ((Bdx.mul Bdy).mul ((Ba1.mul Bb1).add (Ba2.mul Bb2))).integrable (fun p => ?_)
    simp only [fx1, fx2, fy1, fy2, a1, a2, b1, b2, Prod.map, id, cf_flipAt_ne k hxw, cf_flipAt_ne k hyw,
      flipAt_ne hxw, flipAt_ne hyw, flipAt_same, dot_negS_left, dot_negS_right]
    ring
  -- step 2: exchange of the copies
  have s2 : ∫ p, (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p * b1 p + a2 p * b2 p) ∂(P.prod P)
      = 2 * ∫ p, (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p * b1 p) ∂(P.prod P) := by
    have hsw := integral_prod_swap (μ := P) (ν := P)
      (fun p : Config N W × Config N W => (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p * b1 p))
    have i1 : Integrable (fun p => (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p * b1 p)) (P.prod P) :=
      ((Bdx.mul Bdy).mul (Ba1.mul Bb1)).integrable
    have i2 : Integrable (fun p : Config N W × Config N W =>
        (fx1 p.swap - fx2 p.swap) * (fy1 p.swap - fy2 p.swap) * (a1 p.swap * b1 p.swap)) (P.prod P) :=
      (((Bdx.mul Bdy).mul (Ba1.mul Bb1)).comp measurable_swap).integrable
    have e : ∀ p : Config N W × Config N W,
        (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p * b1 p + a2 p * b2 p)
          = (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p * b1 p)
            + (fx1 p.swap - fx2 p.swap) * (fy1 p.swap - fy2 p.swap) * (a1 p.swap * b1 p.swap) := by
      intro p
      simp only [fx1, fx2, fy1, fy2, a1, a2, b1, b2, Prod.fst_swap, Prod.snd_swap]
      ring
    rw [integral_congr_ae (ae_of_all _ e), integral_add i1 i2, hsw]
    ring
  -- step 3: flip of s'_y
  have s3 : ∫ p, (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p * b1 p) ∂(P.prod P)
      = ∫ p, (fx1 p - fx2 p) * fy1 p * (a1 p * b1 p) ∂(P.prod P) := by
    refine integral_symm ((MeasurePreserving.id P).prod (flipAt_mp hN y))
      ((Bdx.mul Bdy).mul (Ba1.mul Bb1)) ((Bdx.mul Bfy1).mul (Ba1.mul Bb1)).integrable (fun p => ?_)
    simp only [fx1, fx2, fy1, fy2, a1, a2, b1, b2, Prod.map, id, cf_flipAt_ne k hxy, cf_flipAt_same]
    ring
  -- step 4: flip of s'_x
  have s4 : ∫ p, (fx1 p - fx2 p) * fy1 p * (a1 p * b1 p) ∂(P.prod P)
      = ∫ p, fx1 p * fy1 p * (a1 p * b1 p) ∂(P.prod P) := by
    refine integral_symm ((MeasurePreserving.id P).prod (flipAt_mp hN x))
      ((Bdx.mul Bfy1).mul (Ba1.mul Bb1)) ((Bfx1.mul Bfy1).mul (Ba1.mul Bb1)).integrable (fun p => ?_)
    simp only [fx1, fx2, fy1, fy2, a1, a2, b1, b2, Prod.map, id, cf_flipAt_same]
    ring
  -- step 5: one copy
  have s5 : ∫ p, fx1 p * fy1 p * (a1 p * b1 p) ∂(P.prod P) = 1 / (N : ℝ) ^ 3 := by
    have h := integral_prod_mul (μ := P) (ν := P)
      (fun σ => cf k x σ * cf k y σ * dot (σ x) (σ w) * dot (σ w) (σ y)) (fun _ => (1 : ℝ))
    simp only [mul_one, integral_const, probReal_univ, one_smul] at h
    rw [single_term hN k hxy hxw hyw] at h
    rw [← h]
    refine integral_congr_ae (ae_of_all _ (fun p => ?_))
    simp only [fx1, fy1, a1, b1]
    ring
  show ∫ p, (fx1 p - fx2 p) * (fy1 p - fy2 p) * (a1 p + a2 p) * (b1 p + b2 p) ∂(P.prod P) = _
  rw [s1, s2, s3, s4, s5]
  ring

end Dup

end G2S3

#print axioms G2S3.dup_term
