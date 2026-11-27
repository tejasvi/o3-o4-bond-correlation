/-
G2S3.RPNamed (stage S3, Part A5-A6): the named hypotheses H7 `hRPGibbs N` (G2Kernel.Named) and H18 `hStripMirror N`
(StripIII.Statement) are theorems for every N, from Lemma 6.1 (G2S3.RPInst).
Paper: Lemma 6.1 (tex l.1726-1738); H7 is its first part (reflection positivity) for the side reflection reflH and the
diagonal reflection reflAnti of P_3 x P_3 used in Proposition 6.7; H18 is its covariance form on P_3 x P_n for the
reflection in the middle row (pairs t_i, bb_i) and in the vertical midline (pairs e, theta e).
-/
import G2S3.RPInst

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

theorem dependsOnly_mono {N : ℕ} {V : Type*} {H H' : Set V} (hsub : H ⊆ H') {F : Config N V → ℝ}
    (hF : DependsOnly H F) : DependsOnly H' F :=
  fun σ σ' h => hF σ σ' (fun v hv => h v (hsub hv))

theorem halfH_sub : halfH ⊆ (reflHm 3 3).S := by
  have key : ∀ p : Fin 3 × Fin 3, 1 ≤ p.1.val → (reflHm 3 3).inS p := by decide
  intro p hp
  exact key p hp

theorem halfAnti_sub : halfAnti ⊆ (reflAm 3).S := by
  have key : ∀ p : Fin 3 × Fin 3, 2 ≤ p.1.val + p.2.val → (reflAm 3).inS p := by decide
  intro p hp
  exact key p hp

theorem gibbsExp_zero_N {V : Type*} [Fintype V] [Nonempty V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (F : Config 0 V → ℝ) : gibbsExp 0 G J F = 0 := by
  simp [gibbsExp, freeMeasure_zero V]

/-- **H7 is a theorem**: `hRPGibbs N` for every `N` (Lemma 6.1, first part, tex l.1726). -/
theorem hRPGibbs_holds (N : ℕ) : hRPGibbs N := by
  intro J hJ F hFm hFb
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · have : Nonempty (Fin 3 × Fin 3) := ⟨(0, 0)⟩
    exact ⟨fun _ => (gibbsExp_zero_N _ _ _).ge, fun _ => (gibbsExp_zero_N _ _ _).ge⟩
  have hFB : BddMeas F := ⟨hFm, hFb⟩
  constructor
  · intro hFd
    exact (reflHm 3 3).rp_gibbs hN grid33 (uniform J) (haut_reflHm 3 3) (fun _ => rfl) (cross_reflHm 3 3)
      (fun _ _ _ => hJ) hFB (dependsOnly_mono halfH_sub hFd)
  · intro hFd
    exact (reflAm 3).rp_gibbs hN grid33 (uniform J) (haut_reflAm 3) (fun _ => rfl) (cross_reflAm 3)
      (fun _ _ _ => hJ) hFB (dependsOnly_mono halfAnti_sub hFd)

theorem rev_zero_three : Fin.rev (0 : Fin 3) = 2 := rfl

/-- **H18 is a theorem**: `hStripMirror N` for every `N` (Lemma 6.1 on `P_3 × P_n`, tex l.1726). -/
theorem hStripMirror_holds (N : ℕ) : hStripMirror N := by
  intro n _hn J hJ
  have hJf : Ferro (box 3 n) (uniform J) := fun _ _ => hJ
  constructor
  · intro i j hij
    have he : s(((0 : Fin 3), i), ((0 : Fin 3), j)) ∈ (box 3 n).edgeSet := by
      show (box 3 n).Adj ((0 : Fin 3), i) ((0 : Fin 3), j)
      rw [box_adj]
      left
      exact ⟨rfl, Or.inl hij⟩
    have h := lemma61_horizontal N 3 n (uniform J) hJf (fun _ => rfl) _ he
    simp only [Sym2.map_mk, reflHm, rev_zero_three] at h
    exact h
  · intro e he
    exact lemma61_vertical N 3 n (uniform J) hJf (fun _ => rfl) e he

end G2S3

#print axioms G2S3.hRPGibbs_holds
#print axioms G2S3.hStripMirror_holds
