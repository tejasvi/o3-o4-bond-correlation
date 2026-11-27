/-
G2S0.SphereIso (stage S0 (a)): the measure `omega N` of G2Kernel.Defs is invariant under every linear isometry of `ℝ^N`,
so the named hypothesis H1 `hSphereIso N` (G2Kernel.Named) is a theorem for every `N`.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Section 1.1: omega is the rotation-invariant
probability measure on S^{N-1}.
Proof: `Measure.toSphere_apply'` writes `volume.toSphere s` as `N * volume (Ioo 0 1 • s)`; a linear isometry `A` maps the cone
`Ioo 0 1 • s` onto the cone over `A s` and preserves `volume` (`LinearIsometryEquiv.measurePreserving`). `omega N` is a constant
multiple of `volume.toSphere`.
-/
import G2Kernel.Named

noncomputable section
open MeasureTheory Set Metric
open scoped Pointwise

namespace G2Kernel

/-- the action of a linear isometry of `ℝ^N` on the unit sphere (the map of `hSphereIso`) -/
def sphAct {N : ℕ} (A : Amb N ≃ₗᵢ[ℝ] Amb N) (x : Sph N) : Sph N := ⟨A (x : Amb N), by simp⟩

theorem measurable_sphAct {N : ℕ} (A : Amb N ≃ₗᵢ[ℝ] Amb N) : Measurable (sphAct A) :=
  Measurable.subtype_mk (A.continuous.measurable.comp measurable_subtype_coe)

/-- the cone over the preimage of `s` is the preimage of the cone over `s` -/
theorem cone_preimage_sphAct {N : ℕ} (A : Amb N ≃ₗᵢ[ℝ] Amb N) (s : Set (Sph N)) :
    (Ioo (0 : ℝ) 1 • (((↑) : Sph N → Amb N) '' (sphAct A ⁻¹' s)) : Set (Amb N))
      = A ⁻¹' (Ioo (0 : ℝ) 1 • (((↑) : Sph N → Amb N) '' s)) := by
  ext y
  simp only [Set.mem_smul, Set.mem_image, Set.mem_preimage]
  constructor
  · rintro ⟨r, hr, _, ⟨x, hx, rfl⟩, rfl⟩
    exact ⟨r, hr, A (x : Amb N), ⟨sphAct A x, hx, rfl⟩, by rw [map_smul]⟩
  · rintro ⟨r, hr, _, ⟨z, hz, rfl⟩, hy⟩
    have hz' : A.symm (z : Amb N) ∈ sphere (0 : Amb N) 1 := by simp
    refine ⟨r, hr, A.symm (z : Amb N), ⟨⟨A.symm (z : Amb N), hz'⟩, ?_, rfl⟩, ?_⟩
    · have hx : sphAct A ⟨A.symm (z : Amb N), hz'⟩ = z := by
        apply Subtype.ext
        simp [sphAct]
      rw [hx]
      exact hz
    · apply A.injective
      rw [map_smul, LinearIsometryEquiv.apply_symm_apply, hy]

/-- the cone measure `volume.toSphere` on the unit sphere of `ℝ^N` is invariant under every linear isometry -/
theorem toSphere_measurePreserving_isometry (N : ℕ) (A : Amb N ≃ₗᵢ[ℝ] Amb N) :
    MeasurePreserving (fun x : Sph N => (⟨A (x : Amb N), by simp⟩ : Sph N))
      (volume : Measure (Amb N)).toSphere (volume : Measure (Amb N)).toSphere := by
  show MeasurePreserving (sphAct A) _ _
  refine ⟨measurable_sphAct A, ?_⟩
  ext s hs
  rw [Measure.map_apply (measurable_sphAct A) hs, Measure.toSphere_apply' _ hs,
    Measure.toSphere_apply' _ (measurable_sphAct A hs), cone_preimage_sphAct]
  congr 1
  have hA : MeasurePreserving (A.toHomeomorph.toMeasurableEquiv) (volume : Measure (Amb N))
      (volume : Measure (Amb N)) := A.measurePreserving
  exact hA.measure_preimage_equiv _

/-- **H1 is a theorem**: `hSphereIso N` holds for every `N` -/
theorem hSphereIso_holds (N : ℕ) : hSphereIso N := by
  intro A
  have h := toSphere_measurePreserving_isometry N A
  refine ⟨h.measurable, ?_⟩
  unfold omega
  rw [Measure.map_smul, h.map_eq]
  exact h.measurable.aemeasurable

end G2Kernel

#print axioms G2Kernel.toSphere_measurePreserving_isometry
#print axioms G2Kernel.hSphereIso_holds
