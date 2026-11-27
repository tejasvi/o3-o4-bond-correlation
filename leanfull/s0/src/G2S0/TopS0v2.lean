/-
G2S0.TopS0v2: version 2 of G2S0.TopS0 (sha8 c3bd44e9, unchanged): the same theorems on the v2 chain (G2S0.OrbitM2v2 in place of
G2S0.OrbitM2), and the final S0 forms after AUDIT_S0_v1 in its #print list at the end:
- T1 nonstrict `cactus_thm_blocks`, `cactus_thm_concrete`; T1 strict in the paper's form `cactus_strict_thm_blocks`,
  `cactus_strict_concrete` (G2S0.BlocksC);
- T7 `stripIII_thm_S0r` and T8 `fullStrip_thm_S0r`, `fullStrip_thm_concrete_r` with every orbit-step hypothesis (H22, H25,
  H26-H28) per representative (G2S0.OrbitB); T6 `smallN_thm_S0`;
- `hM2tailRep_iff`: H28 per representative is equivalent to H28 (G2S0.OrbitM2v2).
G2S0.TopS0 (stage S0, summary): the eight top theorems of the package with the S0 discharges.
- H1 (`hSphereIso`) is a theorem (G2S0.SphereIso), so every top theorem holds without it: T1 in the paper's form
  `cactus_thm_blocks` (G2S0.BlocksB), T6 `smallN_thm_S0` and T8 `fullStrip_thm_S0` (G2S0.OrbitM2, also with H26-H28 per
  representative), and T2, T3, T4, T5, T7 below (each statement is the package's with the premise `hSphereIso N` removed; the other
  premises verbatim).
- H3 (`hKReg`) is a theorem for the paper's coefficients `kConc N`, N ≥ 2 (G2S0.KData): `cactus_thm_concrete` (T1) and
  `fullStrip_thm_concrete` (T8) take the paper's data and drop H3 too.
-/
import G2S0.BlocksC
import G2S0.OrbitB
import G2S0.KData

noncomputable section

namespace G2Kernel

open StripIII (ECode)

/-- T2 (Theorem 1.1, strict part) without H1 -/
theorem cactus_strict_thm_S0 (N : ℕ) :
    ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d →
      (∀ c, 0 < d c) →
      ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (L : List (CactusBlock V)),
        IsCactusWith G L → ∀ J : Sym2 V → ℝ, Ferro G J →
        ∀ (n : ℕ) (φ : Fin n → V), CactusBlock.cycle n φ ∈ L →
          (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
          ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
            0 < gibbsCov N G J (bond e) (bond f) :=
  cactus_strict_thm N (hSphereIso_holds N)

/-- T3 (Theorem 1.4 (ii)) without H1 -/
theorem stripD_factor_thm_S0 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hStripSpecial N →
    ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
      ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 20 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f →
          0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f) :=
  fun hN => stripD_factor_thm N hN (hSphereIso_holds N)

/-- T4 (Theorem 6.34 (a)) without H1 -/
theorem G2_P3P3_thm_S0 (N : ℕ) :
    (N = 3 ∨ N = 4) → hShared N → hRPGibbs N → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hHub N → hLBu N →
      ∀ J : ℝ, 0 ≤ J → ∀ e ∈ grid33.edgeSet, ∀ f ∈ grid33.edgeSet, e ≠ f → G2pair N grid33 (uniform J) e f :=
  fun hN => G2_P3P3_thm N hN (hSphereIso_holds N)

/-- T5 (Theorem 6.34 (b) and Corollary 6.20 for J ≤ 300) without H1 -/
theorem strip300_thm_S0 (N : ℕ) :
    (N = 3 ∨ N = 4) → hShared N → hRPGibbs N → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
    ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
    hHub N → hLBu N → hLadder N → hRHCover N →
      (∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f) ∧
      (∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
          0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)) :=
  fun hN => strip300_thm N hN (hSphereIso_holds N)

/-- T7 (Theorem 6.34 (f)) without H1 -/
theorem stripIII_thm_S0 (N : ℕ) :
    (N = 3 ∨ N = 4) → hShared N → hRPGibbs N → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
    ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
    hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
    hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5 N StripIII.box5List → hS9h N → hS9i N →
    hO5 N (StripIII.o5List ++ L55) →
      ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
          G2pair N (strip n) (uniform J) e f :=
  fun hN => stripIII_thm N hN (hSphereIso_holds N)

/-- T1 (Theorem 1.1) for the paper's data k, d, C̃ (N ≥ 2): H1 and H3 discharged, the hypothesis on the blocks; the remaining
premises are H2, H4 and H5 for the paper's data -/
theorem cactus_thm_concrete (N : ℕ) (hN : 2 ≤ N) :
    hFH N (kConc N) (dConc N) (CConc N) → hRatio (kConc N) → hCycleZ N (kConc N) (dConc N) →
      ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
        ∀ J : Sym2 V → ℝ, Ferro G J → ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → G2pair N G J e f :=
  fun hF hR hC => cactus_thm_blocks N (kConc N) (dConc N) (CConc N) hF (hKReg_kConc N hN) hR hC

/-- T8 (Theorem 1.4 (i)) for the paper's k (N = 3, 4): H1 and H3 discharged, H26-H28 per representative -/
theorem fullStrip_thm_concrete (N : ℕ) (hN : N = 3 ∨ N = 4) :
    hShared N → hRPGibbs N → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
    hRatio (kConc N) → hCornerFactor N (kConc N) →
    hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
    hStripMirror N → hVertSV N → hD4 N → hNE N → hBox5 N StripIII.box5List → hS9h N → hS9i N →
    hO5 N (StripIII.o5List ++ L55) → hBoxAll5rep N StripIII.box5Reps → hM1rep N StripIII.m1List StripIII.NMAX_M1 →
    hM2tailRep N StripIII.D0_M2 StripIII.M0_M2 →
      ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f := by
  intro hSh hRP hW md hSI hSC hR hCF
  have h2 : 2 ≤ N := by rcases hN with rfl | rfl <;> norm_num
  exact fullStrip_thm_S0 N hN hSh hRP hW md hSI hSC (kConc N) (hKReg_kConc N h2) hR hCF

end G2Kernel

#print axioms G2Kernel.hSphereIso_holds
#print axioms G2Kernel.hKReg_kConc
#print axioms G2Kernel.hBoxAll5_of_rep
#print axioms G2Kernel.hM1_of_rep
#print axioms G2Kernel.hM2tail_of_rep
#print axioms G2Kernel.isCactus_iff_blocks
#print axioms G2Kernel.cactus_thm_blocks
#print axioms G2Kernel.cactus_strict_thm_S0
#print axioms G2Kernel.stripD_factor_thm_S0
#print axioms G2Kernel.G2_P3P3_thm_S0
#print axioms G2Kernel.strip300_thm_S0
#print axioms G2Kernel.smallN_thm_S0
#print axioms G2Kernel.stripIII_thm_S0
#print axioms G2Kernel.fullStrip_thm_S0
#print axioms G2Kernel.cactus_thm_concrete
#print axioms G2Kernel.fullStrip_thm_concrete
#print axioms G2Kernel.hM2tailRep_iff
#print axioms G2Kernel.hBox5_of_rep
#print axioms G2Kernel.hO5_of_rep
#print axioms G2Kernel.stripIII_thm_S0r
#print axioms G2Kernel.fullStrip_thm_S0r
#print axioms G2Kernel.fullStrip_thm_concrete_r
#print axioms G2Kernel.cycle_le_cycle
#print axioms G2Kernel.cycle_mem_list
#print axioms G2Kernel.cactus_strict_thm_blocks
#print axioms G2Kernel.dConc_pos
#print axioms G2Kernel.cactus_strict_concrete
