/-
G2S3.Top (stage S3): the top theorems T3, T4 and T5 with the S3 discharges (and S0's H1).
- T3 (Theorem 1.4 (ii)): drops H1, H3, H4, H8 (the triple (hKReg k, hRatio k, hCornerFactor N k) was used only to derive
  hCornerPair, now `hCornerPair_holds`).
- T4 (Theorem 6.34 (a)): drops H1, H6, H7.
- T5 (Theorem 6.34 (b) and Corollary 6.20 for J <= 300): drops H1, H3, H4, H6, H7, H8; the proof is the package's
  strip300_thm with hCornerPair, hShared, hRPGibbs and hSphereIso supplied.
Every other premise is verbatim the package's.
-/
import G2S3.Corner
import G2S0.TopS0v2

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

theorem hShared_of {N : ℕ} (hN : N = 3 ∨ N = 4) : hShared N := by
  rcases hN with rfl | rfl
  · exact hShared_holds3
  · exact hShared_holds4

/-- **T3** (Theorem 1.4 (ii)) without H1, H3, H4, H8. -/
theorem stripD_thm_S3 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hStripSpecial N →
      ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 20 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f →
          0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f) :=
  fun hN hW md hSI hSC hSp =>
    stripD_thm N hN (hSphereIso_holds N) hW md hSI hSC hSp (hCornerPair_holds N hN)

/-- **T4** (Theorem 6.34 (a)) without H1, H6, H7. -/
theorem G2_P3P3_thm_S3 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hHub N → hLBu N →
      ∀ J : ℝ, 0 ≤ J → ∀ e ∈ grid33.edgeSet, ∀ f ∈ grid33.edgeSet, e ≠ f → G2pair N grid33 (uniform J) e f :=
  fun hN hW md hSI hSC hH hL =>
    G2_P3P3_thm_S0 N hN (hShared_of hN) (hRPGibbs_holds N) hW md hSI hSC hH hL

/-- **T5** (Theorem 6.34 (b) and Corollary 6.20 for `J ≤ 300`) without H1, H3, H4, H6, H7, H8. -/
theorem strip300_thm_S3 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
    hHub N → hLBu N → hLadder N → hRHCover N →
      (∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f) ∧
      (∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
          0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)) := by
  intro hN34 hW md hId hCert hH hL hLad hRH
  have hS := hSphereIso_holds N
  have hSh := hShared_of hN34
  have hRP := hRPGibbs_holds N
  have hN : 0 < N := by rcases hN34 with rfl | rfl <;> norm_num
  have hCP : hCornerPair N := hCornerPair_holds N hN34
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

end G2S3

#print axioms G2S3.stripD_thm_S3
#print axioms G2S3.G2_P3P3_thm_S3
#print axioms G2S3.strip300_thm_S3
