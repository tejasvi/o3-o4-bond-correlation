/-
G2S3.ConeMem (stage S3, Part B5): the duplicated interactions, fields and observables lie in the Ginibre cone.
With r = s.1.1, r' = s.1.2 (radii of the two copies), a, a' (plane-1 angles), b, b' (plane-2 angles):
- plane 1: rho_x rho_y c1(a) + rho'_x rho'_y c1(a') has sign 1;
- plane 2: tau_x tau_y c2(b) + tau'_x tau'_y c2(b') has sign 1;
- field: tau_x c2(b) + tau'_x c2(b') has sign 1;
- observable: tau_x c2(b) - tau'_x c2(b') has sign -1 (so a product of two has sign 1).
These are the identities ab + a'b' = ((a + a')(b + b') + (a - a')(b - b'))/2 and
ab - a'b' = ((a - a')(b + b') + (a + a')(b - b'))/2 of Ginibre's argument (tex l.330-336, [Du76]).
-/
import G2S3.ConeInt

noncomputable section
open MeasureTheory Real

namespace G2S3

section Mem

variable {V : Type*} [Fintype V] {X1 X2 I1 I2 : Type*}
variable {ρ τ : ℝ → ℝ} {c1 : I1 → X1 → ℝ} {c2 : I2 → X2 → ℝ}

theorem InC.cast {s s' : ℝ} (h : s = s') {F : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 s F) :
    InC ρ τ c1 c2 s' F := h ▸ hF

theorem InC.half {s : ℝ} {F : Om V X1 X2 → ℝ} (hF : InC ρ τ c1 c2 s F) :
    InC ρ τ c1 c2 s (fun ω => F ω / 2) :=
  (hF.const_mul (a := 1 / 2) (by norm_num)).congr (fun ω => by ring)

/-- `a b + a' b'` from the four combinations. -/
theorem InC.dupSum {s t : ℝ} {A A' C C' : Om V X1 X2 → ℝ}
    (h1 : InC ρ τ c1 c2 s (fun ω => A ω + A' ω)) (h2 : InC ρ τ c1 c2 t (fun ω => A ω - A' ω))
    (h3 : InC ρ τ c1 c2 s (fun ω => C ω + C' ω)) (h4 : InC ρ τ c1 c2 t (fun ω => C ω - C' ω))
    (hst : s * s = t * t) :
    InC ρ τ c1 c2 (s * s) (fun ω => A ω * C ω + A' ω * C' ω) := by
  have hp := h1.mul h3
  have hm := (h2.mul h4).cast hst.symm
  exact (hp.add hm).half.congr (fun ω => by ring)

/-- `a b - a' b'` from the four combinations. -/
theorem InC.dupDiff {s t : ℝ} {A A' C C' : Om V X1 X2 → ℝ}
    (h1 : InC ρ τ c1 c2 s (fun ω => A ω + A' ω)) (h2 : InC ρ τ c1 c2 t (fun ω => A ω - A' ω))
    (h3 : InC ρ τ c1 c2 s (fun ω => C ω + C' ω)) (h4 : InC ρ τ c1 c2 t (fun ω => C ω - C' ω))
    (hst : t * s = s * t) :
    InC ρ τ c1 c2 (t * s) (fun ω => A ω * C ω - A' ω * C' ω) := by
  have hp := h2.mul h3
  have hm := (h1.mul h4).cast hst.symm
  exact (hp.add hm).half.congr (fun ω => by ring)

theorem InC.rhoP (x : V) : InC ρ τ c1 c2 1 (fun ω : Om V X1 X2 => ρ (ω.1.1 x) + ρ (ω.1.2 x)) :=
  (InC.radRho x false).congr (fun ω => by simp)

theorem InC.rhoM (x : V) : InC ρ τ c1 c2 1 (fun ω : Om V X1 X2 => ρ (ω.1.1 x) - ρ (ω.1.2 x)) :=
  (InC.radRho x true).congr (fun ω => by simp; ring)

theorem InC.tauP (x : V) : InC ρ τ c1 c2 1 (fun ω : Om V X1 X2 => τ (ω.1.1 x) + τ (ω.1.2 x)) :=
  ((InC.radTau x false).cast (by simp)).congr (fun ω => by simp)

theorem InC.tauM (x : V) : InC ρ τ c1 c2 (-1) (fun ω : Om V X1 X2 => τ (ω.1.1 x) - τ (ω.1.2 x)) :=
  ((InC.radTau x true).cast (by simp)).congr (fun ω => by simp; ring)

theorem InC.c1P (i : I1) : InC ρ τ c1 c2 1 (fun ω : Om V X1 X2 => c1 i ω.2.1.1 + c1 i ω.2.1.2) :=
  (InC.ang1 i false).congr (fun ω => by simp)

theorem InC.c1M (i : I1) : InC ρ τ c1 c2 1 (fun ω : Om V X1 X2 => c1 i ω.2.1.1 - c1 i ω.2.1.2) :=
  (InC.ang1 i true).congr (fun ω => by simp; ring)

theorem InC.c2P (j : I2) : InC ρ τ c1 c2 1 (fun ω : Om V X1 X2 => c2 j ω.2.2.1 + c2 j ω.2.2.2) :=
  ((InC.ang2 j false).cast (by simp)).congr (fun ω => by simp)

theorem InC.c2M (j : I2) : InC ρ τ c1 c2 (-1) (fun ω : Om V X1 X2 => c2 j ω.2.2.1 - c2 j ω.2.2.2) :=
  ((InC.ang2 j true).cast (by simp)).congr (fun ω => by simp; ring)

/-- radial products `ρ_x ρ_y ± ρ'_x ρ'_y` -/
theorem InC.rhoRhoP (x y : V) : InC ρ τ c1 c2 1
    (fun ω : Om V X1 X2 => ρ (ω.1.1 x) * ρ (ω.1.1 y) + ρ (ω.1.2 x) * ρ (ω.1.2 y)) :=
  ((InC.dupSum (InC.rhoP x) (InC.rhoM x) (InC.rhoP y) (InC.rhoM y) rfl).cast (by norm_num))

theorem InC.rhoRhoM (x y : V) : InC ρ τ c1 c2 1
    (fun ω : Om V X1 X2 => ρ (ω.1.1 x) * ρ (ω.1.1 y) - ρ (ω.1.2 x) * ρ (ω.1.2 y)) :=
  ((InC.dupDiff (InC.rhoP x) (InC.rhoM x) (InC.rhoP y) (InC.rhoM y) rfl).cast (by norm_num))

theorem InC.tauTauP (x y : V) : InC ρ τ c1 c2 1
    (fun ω : Om V X1 X2 => τ (ω.1.1 x) * τ (ω.1.1 y) + τ (ω.1.2 x) * τ (ω.1.2 y)) :=
  ((InC.dupSum (InC.tauP x) (InC.tauM x) (InC.tauP y) (InC.tauM y) (by norm_num)).cast (by norm_num))

theorem InC.tauTauM (x y : V) : InC ρ τ c1 c2 (-1)
    (fun ω : Om V X1 X2 => τ (ω.1.1 x) * τ (ω.1.1 y) - τ (ω.1.2 x) * τ (ω.1.2 y)) :=
  ((InC.dupDiff (InC.tauP x) (InC.tauM x) (InC.tauP y) (InC.tauM y) (by norm_num)).cast (by norm_num))

/-- **Plane 1, duplicated**: `ρ_x ρ_y c1_i(a) + ρ'_x ρ'_y c1_i(a')` has sign 1. -/
theorem InC.plane1 (x y : V) (i : I1) : InC ρ τ c1 c2 1
    (fun ω : Om V X1 X2 => ρ (ω.1.1 x) * ρ (ω.1.1 y) * c1 i ω.2.1.1 + ρ (ω.1.2 x) * ρ (ω.1.2 y) * c1 i ω.2.1.2) :=
  ((InC.dupSum (InC.rhoRhoP x y) (InC.rhoRhoM x y) (InC.c1P i) (InC.c1M i) rfl).cast (by norm_num))

/-- **Plane 2, duplicated**: `τ_x τ_y c2_j(b) + τ'_x τ'_y c2_j(b')` has sign 1. -/
theorem InC.plane2 (x y : V) (j : I2) : InC ρ τ c1 c2 1
    (fun ω : Om V X1 X2 => τ (ω.1.1 x) * τ (ω.1.1 y) * c2 j ω.2.2.1 + τ (ω.1.2 x) * τ (ω.1.2 y) * c2 j ω.2.2.2) :=
  ((InC.dupSum (InC.tauTauP x y) (InC.tauTauM x y) (InC.c2P j) (InC.c2M j) (by norm_num)).cast (by norm_num))

/-- **Field, duplicated**: `τ_x c2_j(b) + τ'_x c2_j(b')` has sign 1. -/
theorem InC.field2 (x : V) (j : I2) : InC ρ τ c1 c2 1
    (fun ω : Om V X1 X2 => τ (ω.1.1 x) * c2 j ω.2.2.1 + τ (ω.1.2 x) * c2 j ω.2.2.2) :=
  ((InC.dupSum (InC.tauP x) (InC.tauM x) (InC.c2P j) (InC.c2M j) (by norm_num)).cast (by norm_num))

/-- **Observable, duplicated**: `τ_x c2_j(b) - τ'_x c2_j(b')` has sign -1. -/
theorem InC.obs2 (x : V) (j : I2) : InC ρ τ c1 c2 (-1)
    (fun ω : Om V X1 X2 => τ (ω.1.1 x) * c2 j ω.2.2.1 - τ (ω.1.2 x) * c2 j ω.2.2.2) :=
  ((InC.dupDiff (InC.tauP x) (InC.tauM x) (InC.c2P j) (InC.c2M j) (by norm_num)).cast (by norm_num))

/-- The product of two observable differences has sign 1. -/
theorem InC.obsObs (x y : V) (j k : I2) : InC ρ τ c1 c2 1
    (fun ω : Om V X1 X2 => (τ (ω.1.1 x) * c2 j ω.2.2.1 - τ (ω.1.2 x) * c2 j ω.2.2.2)
      * (τ (ω.1.1 y) * c2 k ω.2.2.1 - τ (ω.1.2 y) * c2 k ω.2.2.2)) :=
  ((InC.obs2 x j).mul (InC.obs2 y k)).cast (by norm_num)

end Mem

end G2S3
