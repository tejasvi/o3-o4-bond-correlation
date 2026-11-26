/-
G2Kernel.Strip300 (module M12): the strips `P_3 × P_n` for `0 ≤ J ≤ 300`, the Lean side of Corollary 6.20 for `J ≤ 300`
(in Section 6.5) together with Theorem 1.4(ii), both of
the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344). Two named hypotheses and one statement:
- hRHCover restates Theorem 6.19 (†) of the paper for `J ≤ 300`: for `20 ≤ J ≤ 300` and `n ≥ 4`, every pair of distinct
  edges other than the two vertical edges of one column has positive covariance. Its backing is the route H certificate,
  the strip engine with its ledger and the independent union check over `[20, 300]`. The exterior-power form, the near
  and far checks and the certified spectral data are not formalized.
- hLadder cites Theorem 1.2(a) at `N = 4` and Theorem 1.3 at `N = 3` for `P_3 × P_2`; neither
  is formalized.
- `strip300_statement` combines Theorem 1.4(ii) on `(0, 20]` (hWeak, hStripIdentity, hStripCert with its threshold `m0`,
  and the corner route of M10c), hRHCover on `[20, 300]`, hShared for the two vertical edges of one column, Theorem 6.34(a)
  for `n = 3`, hLadder for `n = 2` and hShared for `n = 1`; `J = 0` follows by continuity in `J`. Both ranges contain
  `J = 20`.
Skeleton (step L-a, v1_7). Not compiled yet.
-/
import G2Kernel.CornerFactor

namespace G2Kernel

/-- **hRHCover** (Theorem 6.19 of the paper for `J ≤ 300`, †; kind: restatement, backed by the route H certificate:
the strip engine cs33h_1 with the ledger of its five batches and the independent union check ru2 over `[20, 300]` at
`N = 3` and `N = 4`; the exterior-power form of the covariance, the near and far checks and the certified spectral data
are not formalized): for `20 ≤ J ≤ 300` and `n ≥ 4`, every pair of distinct edges of `P_3 × P_n` other than the two
vertical edges of one column has positive covariance. -/
def hRHCover (N : ℕ) : Prop :=
  ∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 20 ≤ J → J ≤ 300 →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
      0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)

/-- **hLadder** (kind: cited, not formalized; Theorem 1.2(a), at `N = 4`, since `P_3 × P_2`, the ladder with
three rungs, is a 2-connected outerplanar graph whose weak dual is a path; Theorem 1.3, at `N = 3`, since an
outerplanar graph has no `W_4` minor): at every uniform coupling `J ≥ 0`, every pair of distinct edges of `P_3 × P_2` has
nonnegative covariance. -/
def hLadder (N : ℕ) : Prop :=
  ∀ J : ℝ, 0 ≤ J → ∀ e ∈ (strip 2).edgeSet, ∀ f ∈ (strip 2).edgeSet, e ≠ f → G2pair N (strip 2) (uniform J) e f

/-- Statement M12 (Corollary 6.20 with Theorem 1.4(ii)): for `N = 3, 4`, every `n ≥ 1` and `0 ≤ J ≤ 300`, every
pair of distinct edges of `P_3 × P_n` has nonnegative covariance; for `n ≥ 4` and `0 < J ≤ 300` the covariance is
positive for every pair of distinct edges other than the two vertical edges of one column. Uses hSphereIso, hShared,
hRPGibbs, hWeak, hStripIdentity, hStripCert, hKReg, hRatio, hCornerFactor, hHub, hLBu, hLadder and hRHCover. -/
def strip300_statement (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  ∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k →
  hHub N → hLBu N → hLadder N → hRHCover N →
    (∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J → J ≤ 300 →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f) ∧
    (∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 300 →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
        0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f))

end G2Kernel
