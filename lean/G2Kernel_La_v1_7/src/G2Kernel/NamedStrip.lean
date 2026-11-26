/-
G2Kernel.NamedStrip: the named hypotheses for the strip part of Theorem 1.4(ii) (with Theorem 6.5, Theorem 6.4,
Lemma 6.3, Theorem 6.6, Lemma 6.2 and Lemma 2.4 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344)), split as the proof of Theorem 6.4 splits the
pairs:
- regular pairs go through the mode expansion: hStripIdentity is Lemma 6.3 (a paper proof), hStripCert is what the
  certificates of Theorem 6.6 check, namely (C1)–(C5) at the separations `m ≥ m0` and the direct evaluation (C6) at
  the separations `m < m0`, and `criterion_statement` (M7) derives positivity. Both are trusted for the mode data of
  the transfer operator of Section 6.3; in Lean the mode data `md` are abstract, so the two hypotheses are jointly
  equivalent to the positivity of the regular pairs on the certified range, and the kernel checks the inequality logic
  of Theorem 6.4 and the corner reduction;
- pairs with a vertical edge of an end column are reduced in the kernel by the corner identity (Lemma 6.2, M5), with
  one or two corner steps, except the pair of the two edges at one corner;
- the two vertical edges of an interior column ((C7), certified) are restated in hStripSpecial, and the two edges at one
  corner (Lemma 2.4) in hCornerPair, both used only for the strict Theorem 1.4(ii);
- hWeak restates Theorem 1.4(ii) on `(0, 1/100]` for every pair except the corner pairs.
Skeleton (step L-a, v1_6). Not compiled yet.
-/
import G2Kernel.Named
import G2Kernel.Criterion

noncomputable section

namespace G2Kernel

/-- The two vertical edges of column `j` of `P_3 × P_n`: top–middle and middle–bottom. -/
def vUp {n : ℕ} (j : Fin n) : Sym2 (Fin 3 × Fin n) := s(((0 : Fin 3), j), ((1 : Fin 3), j))
def vDown {n : ℕ} (j : Fin n) : Sym2 (Fin 3 × Fin n) := s(((1 : Fin 3), j), ((2 : Fin 3), j))

/-- The four corner vertices of `P_3 × P_n`, each of degree two. -/
def isCorner (n : ℕ) (c : Fin 3 × Fin n) : Prop :=
  (c.1 = 0 ∨ c.1 = 2) ∧ (c.2.val = 0 ∨ c.2.val + 1 = n)

/-- The two vertical edges of one column (condition (C7) of Theorem 6.4 for interior columns). -/
def sameColumn (n : ℕ) (e f : Sym2 (Fin 3 × Fin n)) : Prop :=
  ∃ j : Fin n, (e = vUp j ∧ f = vDown j) ∨ (e = vDown j ∧ f = vUp j)

/-- The two vertical edges of one interior column, the pairs that (C7) as written covers. -/
def sameInteriorColumn (n : ℕ) (e f : Sym2 (Fin 3 × Fin n)) : Prop :=
  ∃ j : Fin n, 0 < j.val ∧ j.val + 1 < n ∧ ((e = vUp j ∧ f = vDown j) ∨ (e = vDown j ∧ f = vUp j))

/-- A vertical edge of an end column; it contains a corner vertex. -/
def endVertical (n : ℕ) (e : Sym2 (Fin 3 × Fin n)) : Prop :=
  ∃ j : Fin n, (j.val = 0 ∨ j.val + 1 = n) ∧ (e = vUp j ∨ e = vDown j)

/-- The two edges at one corner, a vertical and a horizontal edge in series (Lemma 2.4 in the proof of Theorem 6.4). -/
def seriesCorner (n : ℕ) (e f : Sym2 (Fin 3 × Fin n)) : Prop :=
  ∃ c : Fin 3 × Fin n, isCorner n c ∧ c ∈ e ∧ c ∈ f

/-- The pairs that the proof of Theorem 6.4 treats by the mode expansion of Lemma 6.3. -/
def regularPair (n : ℕ) (e f : Sym2 (Fin 3 × Fin n)) : Prop :=
  ¬ sameColumn n e f ∧ ¬ endVertical n e ∧ ¬ endVertical n f

/-- Mode data for every strip, coupling and pair of edges; the paper's data come from the transfer operator of
Section 6.3 (eigenvalues of `T`, the coefficients of the insertion vectors of the two classes, and the separation). -/
abbrev StripModes := (n : ℕ) → ℝ → Sym2 (Fin 3 × Fin n) → Sym2 (Fin 3 × Fin n) → ModeData

/-- **hWeak** (Theorem 6.5, †; kind: restatement, backed by Appendix A, a paper proof that uses the
certified four-state data of Lemmas A.2 and A.3): for `0 < J ≤ 1/100` and `n ≥ 3`, every pair of distinct edges of
`P_3 × P_n` other than the two edges at one corner has positive covariance. -/
def hWeak (N : ℕ) : Prop :=
  ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 1 / 100 →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ seriesCorner n e f →
      0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)

/-- **hStripIdentity** (Lemma 6.3, with the transfer operator of Section 6.3; kind: paper proof, but
with `md` abstract it carries restatement strength jointly with hStripCert): for `n ≥ 3`, `J` in the certified range
and every regular pair of distinct edges, the mode data of the pair carry its covariance and satisfy the identity
(6) and the bounds of Lemma 6.3. -/
def hStripIdentity (N : ℕ) (md : StripModes) : Prop :=
  ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 99 / 10000 ≤ J → J ≤ stripTop N →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → regularPair n e f →
      (md n J e f).cov = gibbsCov N (strip n) (uniform J) (bond e) (bond f) ∧ (md n J e f).identity

/-- **hStripCert** (Theorem 6.6, †; kind: certificate, but with `md` abstract it carries
restatement strength jointly with hStripIdentity): there is a threshold `m0 J` for every coupling, fixed by the
certificates on each subinterval of the certified range (they use `m0 ∈ {0, 1}`), such that every regular pair of
distinct edges satisfies the conditions (C1)–(C5) of Theorem 6.4 if its separation is at least `m0 J`, and condition
(C6), a direct evaluation of the determinant of Section 6.3, if its separation is below `m0 J`. The certificates check
these for every pair of classes (the deep classes enclosing all larger distances), and they transfer from classes to
pairs as in Section 6.3. -/
def hStripCert (N : ℕ) (md : StripModes) : Prop :=
  ∃ m0 : ℝ → ℕ, ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 99 / 10000 ≤ J → J ≤ stripTop N →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → regularPair n e f →
      (m0 J ≤ (md n J e f).m → (md n J e f).criterion) ∧ ((md n J e f).m < m0 J → (md n J e f).direct)

/-- **hStripSpecial** (kind: restatement, backed by condition (C7) of Theorem 6.4, certified with Theorem 6.6): on the
certified range, the two vertical edges of an interior column have positive covariance. -/
def hStripSpecial (N : ℕ) : Prop :=
  ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 99 / 10000 ≤ J → J ≤ stripTop N →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → sameInteriorColumn n e f →
      0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)

/-- **hCornerPair** (kind: restatement, backed by Lemma 2.4, with a nonnegative law of the common label:
Lemma 4.1 at `N = 4`, and at `N = 3` the argument of NOTE_LEMMA24_N3_v1, confirmed with fixes by the review): for
`0 < J ≤ 20` and `n ≥ 3`, the two edges at one corner of `P_3 × P_n` have positive covariance. Used only for the
strict Theorem 1.4(ii); `cornerPair_statement` (CornerFactor.lean) derives it from hCornerFactor, hKReg and hRatio. -/
def hCornerPair (N : ℕ) : Prop :=
  ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 20 →
    ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → seriesCorner n e f →
      0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)

end G2Kernel
