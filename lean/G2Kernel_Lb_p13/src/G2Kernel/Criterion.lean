/-
G2Kernel.Criterion (module M7): the inequality logic in the proof of Theorem 6.4 of
the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344), for one pair of classes, given the identity of Lemma 6.3 (display (6)).
The premises are grouped as the paper's proof uses them: `ModeData.identity` (Lemma 6.3, a paper proof),
`ModeData.criterion` (conditions (C1)–(C5), which the certificates of Theorem 6.6 check at the separations `m ≥ m0`)
and `ModeData.direct` (condition (C6), the determinant of Section 6.3, which the certificates evaluate directly at the
separations `m < m0`). NamedStrip.lean supplies them for the strip pairs, and Assembly.lean derives positivity through
`criterion_statement`.
Skeleton (step L-a, v1_6). Not compiled yet.
-/
import G2Kernel.Defs

noncomputable section

namespace G2Kernel

/-- The numbers attached to one pair in the mode expansion (6): eigenvalues `λ_1, …, λ_5`, the mode
coefficients `â_l, b̂_l` for `l = 2, 3, 4`, the tail `S_∞`, the end correction `R_CE`, the norms used in
(C5), the normalisation `𝒩`, the covariance and the separation `m`. -/
structure ModeData where
  l1 : ℝ
  l2 : ℝ
  l3 : ℝ
  l4 : ℝ
  l5 : ℝ
  a2 : ℝ
  a3 : ℝ
  a4 : ℝ
  b2 : ℝ
  b3 : ℝ
  b4 : ℝ
  Sinf : ℝ
  RCE : ℝ
  q5u : ℝ
  q5v : ℝ
  nu : ℝ
  nv : ℝ
  eL : ℝ
  eR : ℝ
  Ncal : ℝ
  cov : ℝ
  m : ℕ

/-- The right side of (C5): the bound on `S_∞` and `R_CE`. -/
def ModeData.tailBound (D : ModeData) : ℝ :=
  (D.l5 / D.l1) ^ D.m * (D.q5u * D.q5v) + (D.l2 / D.l1) ^ (2 * D.m) * (D.nu * D.eL * D.nv * D.eR)

/-- Lemma 6.3 for one pair: the identity (6), `𝒩 > 0`, `λ_5 ≥ 0` (positivity of the transfer operator),
and the bounds on `S_∞` (Cauchy–Schwarz on the modes `l ≥ 5`) and on `R_CE`. -/
def ModeData.identity (D : ModeData) : Prop :=
  D.cov * D.Ncal ^ 2 = (D.l2 / D.l1) ^ D.m * (D.a2 * D.b2) + (D.l3 / D.l1) ^ D.m * (D.a3 * D.b3)
      + (D.l4 / D.l1) ^ D.m * (D.a4 * D.b4) + D.Sinf + D.RCE ∧
  0 < D.Ncal ∧ 0 ≤ D.l5 ∧
  |D.Sinf| ≤ (D.l5 / D.l1) ^ D.m * (D.q5u * D.q5v) ∧
  |D.RCE| ≤ (D.l2 / D.l1) ^ (2 * D.m) * (D.nu * D.eL * D.nv * D.eR)

/-- Conditions (C1)–(C5) of Theorem 6.4 for one pair: the strict order of `λ_1, …, λ_5`, (C2), and the pair's case
of (C3)–(C5), for a pair that is not top–bottom (first alternative) or top–bottom (second alternative). -/
def ModeData.criterion (D : ModeData) : Prop :=
  D.l2 < D.l1 ∧ D.l3 < D.l2 ∧ D.l4 < D.l3 ∧ D.l5 < D.l4 ∧ 0 < D.l2 + D.l4 - 2 * D.l3 ∧
  ((0 < D.a2 * D.b2 ∧ 0 < D.a4 * D.b4 ∧ 0 ≤ D.a3 * D.b3 ∧
      D.tailBound < (D.l4 / D.l1) ^ D.m * (D.a2 * D.b2 + D.a4 * D.b4)) ∨
   (0 < D.a2 * D.b2 ∧ 0 < D.a4 * D.b4 ∧ D.a4 * D.b4 ≤ D.a2 * D.b2 ∧
      D.tailBound < (D.l3 / D.l1) ^ D.m * (D.a2 * D.b2 + D.a4 * D.b4 + D.a3 * D.b3)))

/-- Condition (C6) of Theorem 6.4 for one pair: the determinant `Cov(s_e, s_f) Z²` of Section 6.3 is positive. It is
stated here in the normalisation of (6), `Cov(s_e, s_f) 𝒩²` with `𝒩 = Z / (u¹₁ v¹₁ λ_1^m)`, a positive multiple
of the determinant. The certificates of Theorem 6.6 evaluate it directly at the separations `m < m0`. -/
def ModeData.direct (D : ModeData) : Prop :=
  0 < D.cov * D.Ncal ^ 2

/-- Statement M7: for a pair with separation `m` and a threshold `m0`, the identity of Lemma 6.3, together with
(C1)–(C5) when `m ≥ m0` and with (C6) when `m < m0`, implies a positive covariance. -/
def criterion_statement : Prop :=
  ∀ (D : ModeData) (m0 : ℕ), D.identity → (m0 ≤ D.m → D.criterion) → (D.m < m0 → D.direct) → 0 < D.cov

end G2Kernel
