/-
G2Kernel.Assembly (module M10): Theorem 1.4(ii) of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344) for every n ≥ 3,
its case n = 3, and Theorem 6.34(a), the 3 × 3 grid at every J ≥ 0 for N = 3, 4, assembled from the kernel modules
and the named hypotheses.
- Theorem 1.4(ii), strict: on (0, 1/100] hWeak (all pairs but the corner pairs); on [0.0099, 20] the regular pairs go through
  criterion_statement (M7) with hStripIdentity and hStripCert, a vertical edge of an end column is replaced by the
  horizontal edge at its corner through corner_statement (M5), the two vertical edges of an interior column come from
  hStripSpecial; the two edges at one corner come from hCornerPair on (0, 20].
- Theorem 6.34(a), Cov ≥ 0: as Theorem 1.4(ii), except that every pair with a common vertex is taken from hShared; so Theorem 6.34(a)
  uses neither hStripSpecial nor hCornerPair.
For the regular strip pairs, hStripIdentity and hStripCert are trusted for the mode data of Section 6.3; with `md`
abstract they are jointly equivalent to the positivity of those pairs on the certified range, and the kernel checks
the inequality logic of Theorem 6.4 and the corner reduction.
Skeleton (step L-a, v1_2). Not compiled yet.
-/
import G2Kernel.Ledger
import G2Kernel.Corner
import G2Kernel.RPstep
import G2Kernel.Cover
import G2Kernel.NamedStrip

namespace G2Kernel

/-- Statement M10a (Theorem 1.4(ii) at `n = 3`): positive covariance for `0 < J ≤ 20`. Uses hSphereIso, hWeak,
hStripIdentity, hStripCert, hStripSpecial and hCornerPair. -/
def strip3_statement (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hStripSpecial N → hCornerPair N →
    ∀ J : ℝ, 0 < J → J ≤ 20 →
      ∀ e ∈ grid33.edgeSet, ∀ f ∈ grid33.edgeSet, e ≠ f →
        0 < gibbsCov N grid33 (uniform J) (bond e) (bond f)

/-- Statement M10b (Theorem 1.4(ii)): for `N = 3, 4`, every `n ≥ 3` and `0 < J ≤ 20`, every pair of distinct edges of
`P_3 × P_n` has positive covariance. Uses hSphereIso, hWeak, hStripIdentity, hStripCert, hStripSpecial and hCornerPair,
with the kernel statements of M5, M7 and M9. -/
def stripD_statement (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hStripSpecial N → hCornerPair N →
    ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 20 →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f →
        0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)

/-- Statement M10 (Theorem 6.34(a)): every pair of distinct edges of `P_3 × P_3` has `Cov ≥ 0` at every `J ≥ 0`, for
`N = 3, 4`. Uses hSphereIso, hShared, hRPGibbs, hWeak, hStripIdentity, hStripCert, hHub and hLBu, with the kernel
statements of M5, M6, M7, M8 and M9; pairs with a common vertex come from hShared at every `J`. -/
def G2_P3P3_statement (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hSphereIso N → hShared N → hRPGibbs N → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hHub N → hLBu N →
    ∀ J : ℝ, 0 ≤ J → ∀ e ∈ grid33.edgeSet, ∀ f ∈ grid33.edgeSet, e ≠ f → G2pair N grid33 (uniform J) e f

end G2Kernel
