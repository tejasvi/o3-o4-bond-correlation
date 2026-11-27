# STATEMENTS_S3_public: the statements of stage S3 for the modules of this folder (the 39 modules of the S3 freeze,
# G2S2.Ratio, G2S3.Cor38Pos and the 7 modules of Part E), as they were written during the work: STATEMENTS_S3.md and its
# successors _v2 to _v9, in order, each under its own title (v8: Part E, Theorems 3.7 and 1.2(b); v9: a correction and a
# proviso), and a closing note (v10) written for this release. Lines naming the working teams or their folders are
# reworded; nothing else is changed.
# Every Lean statement in this file is about finite simple graphs (Mathlib's SimpleGraph); the paper's Theorems 1.1 and
# 1.2(b) also cover parallel edges through its Section 3.3 reduction, which is not formalized.

# STATEMENTS_S3 (v1, 2026-11-27): statements of stage S3, with the paper facts (release source
G2_PAPER_v4_42rc5_release.tex, "tex l.N")

Conventions: the package definitions (G2Kernel.Defs: Config, omega, freeMeasure, bond, energy, partition, gibbsExp,
gibbsCov, Ferro, G2pair, uniform, strip, grid33) are used verbatim. `box m n` (G2S3.RPInst) is P_m x P_n on
Fin m x Fin n with the relation of `strip` (so `strip n` is `box 3 n` by definition).

## Part A: reflection positivity (Lemma 6.1, tex l.1726-1738)

NOTE (process): A1-A4 below were proved before this file existed (rule slip, reported at M1); the statements are
recorded exactly as compiled. A5, A6 were written here before their proofs.

- A1 `G2S3.rp_config` (RPGraph): for a reflection R of V (ReflData: involution theta, open half P, P and theta P
  disjoint, V = Fix + P + theta P), bounded measurable A, F depending only on the closed half S = Fix + P, and a crossing
  term rankSum s w u with w >= 0 and bounded measurable u:
  0 <= int F(s) F(s o theta) exp(A(s) + A(s o theta) + rankSum s w u (s|P, (s o theta)|P)) d(freeMeasure N V), N > 0.
  Paper: the factorization e^{H+} theta(e^{H+}) and "the standard expansion of e^{J s_x . s_theta x} into products of
  components [FILS78]" (tex l.1733-1737).
- A2 `G2S3.ReflData.rp_gibbs` (RPEnergy): for a graph G with R.theta an automorphism, J theta-invariant, the crossing
  property CrossOK (every edge from P to outside S is {x, theta x}) and J >= 0 on crossing edges:
  0 <= gibbsExp N G J (fun s => F s * F (s o theta)) for bounded measurable F depending only on S (reflection
  positivity of the Gibbs measure; Lemma 6.1, proof).
- A3 `G2S3.cov_refl`, `G2S3.G2pair_refl` (RPEnergy), `G2S3.G2pair_refl_edge` (RPInst): under the hypotheses of A2,
  Cov(F, F o theta) >= 0 (|F| <= 1, F depends only on S), and Cov(s_e, s_{theta e}) >= 0 for EVERY edge e of G, every N.
- A4 Lemma 6.1 (tex l.1726), four theorems (RPInst), every N, every m n:
  `lemma61_horizontal N m n J (Ferro (box m n) J) (J o map theta = J)`: forall e in edges, G2pair N (box m n) J e (theta e),
  theta (r, c) = (rev r, c);
  `lemma61_vertical`: theta (r, c) = (r, rev c);
  `lemma61_diagonal N n J (J o map theta = J)`: theta (r, c) = (c, r) on P_n x P_n (no sign condition needed);
  `lemma61_antidiagonal`: theta (r, c) = (rev c, rev r).
  Fidelity: the paper's "theta-invariant couplings" are ferromagnetic (the paper's standing assumption J_e >= 0); the
  sign is used only for the crossing bonds of a line between rows (horizontal/vertical with m resp. n even).
- A5 `G2S3.hRPGibbs_holds (N : ℕ) : hRPGibbs N` (RPNamed): H7 is a theorem for every N (Lemma 6.1, first part, for
  reflH and reflAnti of P_3 x P_3, uniform J >= 0, bounded measurable F on the closed halves halfH, halfAnti).
- A6 `G2S3.hStripMirror_holds (N : ℕ) : hStripMirror N` (RPNamed): H18 is a theorem for every N (Lemma 6.1 on P_3 x P_n
  for the middle-row reflection, pairs (t_i, bb_i), and for the vertical midline stripReflV, pairs (e, theta e)).

## Part B (planned): Dunlop / Ginibre
- B1 `hShared_holds3 : hShared 3`, `hShared_holds4 : hShared 4` (H6; Theorem 3.2, edge-pair case, tex l.322).
- B2 `hCornerPair_holds (N) (hN : N = 3 ∨ N = 4) : hCornerPair N` (strict corner covariance; the consequence of H8 that
  T3, T5-T8 use; Corollary 3.8's Cov > 0, tex l.438).

---

# STATEMENTS_S3_v2 (2026-11-27): successor of STATEMENTS_S3.md (sha8 9e4c4052, unchanged). Part A text unchanged;
Part B statements added (B1 was listed before its proof; the intermediate lemmas B0.* were recorded after their proofs).

## Part A: see STATEMENTS_S3.md (A1-A6: rp_config, rp_gibbs, cov_refl/G2pair_refl/G2pair_refl_edge, lemma61_*,
hRPGibbs_holds, hStripMirror_holds).

## Part B: Theorem 3.2, edge-pair case (tex l.322-354), via Ginibre's duplicate variables and Dunlop's condition
- B0.1 `G2S3.radial_site` (Gin): for every probability law nu on R, rho increasing, tau decreasing, both >= 0, and every
  list L of radial factors rho(r) +- rho(r'), tau(r) +- tau(r'):  0 <= sgQ(L) * int int prod(L) d nu d nu.
  Paper: Lemma 3.3 (tex l.340-354), Dunlop's hypothesis (2.4), for any radial law.
- B0.2 `G2S3.gin_circle`, `G2S3.gin_ising` (Gin): Ginibre's condition 0 <= int int prod (c_n(a) +- c_n(a')) on the torus
  (cos(n . theta), Haar) and on {+-1}^V (characters, uniform).
- B0.3 `G2S3.GHyp.cone_nonneg`, `cone_exp`, `cone_strict` (ConeInt): integrals of the Ginibre cone of sign 1 are >= 0;
  int F exp(G) >= 0; int F A B <= int F exp(A + B + C).
- B0.4 `G2S3.param4`, `G2S3.param3` (Spheres, Sphere3): omega on S^3 (resp. S^2) is the image of
  (law of the plane-1 radius) x Haar x Haar (resp. x uniform(Bool) x Haar) under the two-plane coordinates Phi4 (Phi3).
- B0.5 `G2S3.integral_cond` (Dup): int G = int G(s_v = u, rest) for rotation-invariant bounded measurable G (the
  conditioning step of the proof of Theorem 3.2); `G2S3.cov_dup`: the duplicated form of the covariance numerator.
- B0.6 `G2S3.gksz_generic` (GKSz): from site data (Phi measure preserving, Ginibre plane-1 system, the two dot-product
  identities), 0 <= gibbsCov N G J (bond s(v, x)) (bond s(v, y)) for every finite graph, Ferro J, x, y /= v.
- B1 `G2S3.hShared_holds4 : hShared 4`, `G2S3.hShared_holds3 : hShared 3` (Dunlop): H6 is a theorem at N = 3, 4.
  Paper: Theorem 3.2, edge-pair case ("In particular Cov(s_e, s_f) >= 0 for every two edges e, f with a common vertex").
- B2 (next) `hCornerPair_holds (N) (hN : N = 3 ∨ N = 4) : hCornerPair N` (strict corner covariance, Corollary 3.8's
  Cov > 0, tex l.438), via `cone_strict` and the explicit term 2 J^2 / N^3 of the path x - w - y around the corner.

---

# STATEMENTS_S3_v3 (2026-11-27): successor of STATEMENTS_S3_v2.md (sha8 b4e3f1ae, unchanged), which itself extends
STATEMENTS_S3.md (sha8 9e4c4052). Added: Part B8 (strict corner inequality).

## Part B8: Corollary 3.8, Cov > 0 at a corner (tex l.438), and hCornerPair
- B8.1 `G2S3.int_coord_mul (hN : 0 < N) (i j : Fin N) : int s_i s_j d omega = if i = j then 1/N else 0`
  and `int_coord_zero` (Moments): moments of omega from coordinate reflections and transpositions.
- B8.2 `G2S3.dup_term` (StrictDup): for distinct x, y, w and a coordinate k,
  int int (s_x^k - s'_x^k)(s_y^k - s'_y^k)(s_x.s_w + s'_x.s'_w)(s_w.s_y + s'_w.s'_y) = 2 / N^3.
- B8.3 `G2S3.gksz_strict_generic` (GKSzStrict): with the site data of gksz_generic, u . s = s_k, and a vertex
  w /= v with G.Adj x w, G.Adj w y, J s(x,w) > 0, J s(w,y) > 0, x /= y:  0 < gibbsCov N G J (bond s(v,x)) (bond s(v,y)).
  Fidelity note: this is the covariance conclusion of Corollary 3.8 for a positive path of length 2 from x to y
  avoiding v (the paper allows any positive path; v of degree two is not needed here).
- B8.4 `G2S3.corner_pos4`, `G2S3.corner_pos3` (Corner): for n >= 3 and EVERY J > 0, the two edges at a corner of
  P_3 x P_n have positive covariance at N = 4, resp. N = 3.
- B2 `G2S3.hCornerPair_holds (N : ℕ) (hN : N = 3 ∨ N = 4) : hCornerPair N` (Corner).

## Not proved (Part C, needs S1)
- H8 `hCornerFactor N (kConc N)` as stated (single-label series with nonnegative weights u_c) and Corollary 3.8's
  "the law of the common label is nonnegative and charges the labels 0 and 1". No top theorem needs them once
  hCornerPair is proved: T3, T5-T8 use (hKReg k, hRatio k, hCornerFactor N k) only to derive hCornerPair.

---

# STATEMENTS_S3_v4 (2026-11-27): successor of STATEMENTS_S3_v3.md (sha8 3812dbab, unchanged). Added: Part D, the top
theorems T3-T8 without H3, H4, H6, H7, H8, H18 (after M3), with the old forms derived from them.

## Part D: the top theorems T3-T8 restated

Numbering of SCOPE_LEAN_FULL_v1.md: T3 Theorem 1.4 (ii); T4 Theorem 6.34 (a); T5 Theorem 6.34 (b) and Corollary 6.20 for
J <= 300; T6 Theorem 6.34 (e); T7 Theorem 6.34 (f); T8 Theorem 1.4 (i).

Rule of the restatement. Each S3 form is S0's final form of the theorem (s0/STATEMENTS_S0_v3.md: H1 `hSphereIso N`
discharged; H22, H25, H26-H28 per representative where S0 has them) with exactly these premises removed; every other premise
is verbatim and in the same order, and the conclusion is verbatim:
- `hShared N` (H6; discharged by `G2S3.hShared_of hN`, from hShared_holds3, hShared_holds4, Part B1);
- `hRPGibbs N` (H7; `G2S3.hRPGibbs_holds N`, Part A5);
- `hStripMirror N` (H18; `G2S3.hStripMirror_holds N`, Part A6);
- the triple `∀ k : ℕ → ℝ → ℝ, hKReg k → hRatio k → hCornerFactor N k` (H3, H4, H8). The package uses the triple only to
  derive `hCornerPair N` (Strip300Proof l.158, CornerFactorProof l.75); S3 proves `G2S3.hCornerPair_holds N hN` (Part B8).
  The S3 forms therefore carry no coefficient data k, and they need nothing from S1 or S2.
Proofs of T6-T8: the package's assembly proofs (StripIII.Small5Proof `smallN_of_list`, StripIII.Proof
`stripIII_full_of_lists`, StripIIIM1.HProof `fullStripM1_of_parts`, StripIIIM2.M2Proof `fullStripM2_of_parts`,
`fullStrip_of_parts`) copied, with `strip300_thm_S3` in place of `strip300_thm (... k hK hR hCF ...)` for J <= 300 and the
discharges `hSphereIso_holds N`, `hShared_of hN`, `hStripMirror_holds N` passed to the package lemmas that take hS, hSh, hMir
(`stripIII_of_lists`, `hpair_of_check`, `hpair_tail`); the parts for J > 300 are otherwise unchanged. The per-representative
forms use S0's `hBoxAll5_of_rep`, `hBox5_of_rep`, `hO5_of_rep`, `hM1_of_rep`, `hM2tail_of_rep`.
Namespace G2S3, with `open G2Kernel G2Kernel.StripIII`.

### D1-D3: T3, T4, T5 (module G2S3.Top, sha8 64e31638)
NOTE (process): these three were compiled at 12:05Z (logs/j59_final.out) before being recorded in a STATEMENTS file, a slip
against "write each statement into STATEMENTS before proving it"; they are recorded here exactly as compiled.
```lean
/-- T3 (Theorem 1.4 (ii)) without H1, H3, H4, H8 -/
theorem stripD_thm_S3 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hStripSpecial N →
      ∀ n : ℕ, 3 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 20 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f →
          0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f)
/-- T4 (Theorem 6.34 (a)) without H1, H6, H7 -/
theorem G2_P3P3_thm_S3 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md → hHub N → hLBu N →
      ∀ J : ℝ, 0 ≤ J → ∀ e ∈ grid33.edgeSet, ∀ f ∈ grid33.edgeSet, e ≠ f → G2pair N grid33 (uniform J) e f
/-- T5 (Theorem 6.34 (b) and Corollary 6.20 for J ≤ 300) without H1, H3, H4, H6, H7, H8 -/
theorem strip300_thm_S3 (N : ℕ) :
    (N = 3 ∨ N = 4) → hWeak N →
    ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
    hHub N → hLBu N → hLadder N → hRHCover N →
      (∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f) ∧
      (∀ n : ℕ, 4 ≤ n → ∀ J : ℝ, 0 < J → J ≤ 300 →
        ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ sameColumn n e f →
          0 < gibbsCov N (strip n) (uniform J) (bond e) (bond f))
```

### D4: T6, Theorem 6.34 (e), the complete small-n theorem (module G2S3.TopIII; written before its proof)
```lean
/-- T6 with a list parameter: the package's `smallN_statementL N L` without hSphereIso, hShared, hRPGibbs, the k-triple
and hStripMirror -/
def smallN_statementL_S3 (N : ℕ) (L : List (ECode × ECode)) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hBoxAll5 N L →
    ∀ n : ℕ, 1 ≤ n → n ≤ 5 → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f
theorem smallN_of_list_S3 (N : ℕ) (L : List (ECode × ECode)) (h : box5AllCheck L = true) : smallN_statementL_S3 N L
theorem smallN_thmL_S3 (N : ℕ) : smallN_statementL_S3 N (box5AllList34 ++ box5Stage2)
/-- **T6, final S3 form**: S0's `smallN_statement_S0 N` (H26 per representative) without hShared, hRPGibbs, the k-triple
and hStripMirror -/
def smallN_statement_S3 (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hBoxAll5rep N StripIII.box5Reps →
    ∀ n : ℕ, 1 ≤ n → n ≤ 5 → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f
theorem smallN_thm_S3 (N : ℕ) : smallN_statement_S3 N
```

### D5: T7, Theorem 6.34 (f) (module G2S3.TopIII; written before its proof)
```lean
/-- T7 with list parameters: the package's `stripIII_full_statementL N L5 L6` without hSphereIso, hShared, hRPGibbs, the
k-triple and hStripMirror -/
def stripIII_full_statementL_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode)) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f
theorem stripIII_full_of_lists_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (h5 : box5Check L5 = true) (h6 : o5Check L6 = true) : stripIII_full_statementL_S3 N L5 L6
theorem stripIII_thmL_S3 (N : ℕ) : stripIII_full_statementL_S3 N StripIII.box5List (StripIII.o5List ++ L55)
/-- **T7, final S3 form**: S0's `stripIII_statement_S0r N` (H22, H25 per representative) without hShared, hRPGibbs, the
k-triple and hStripMirror -/
def stripIII_statement_S3r (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → ¬ midRowEdge n e → ¬ midRowEdge n f →
        G2pair N (strip n) (uniform J) e f
theorem stripIII_thm_S3r (N : ℕ) : stripIII_statement_S3r N
```

### D6: M1's and M2's theorems, helpers of T8 (Propositions B.22, B.24 assembly; module G2S3.TopIII)
```lean
/-- the package's `fullStripM1_statementL` without hSphereIso, hShared, hRPGibbs, the k-triple and hStripMirror -/
def fullStripM1_statementL_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (L2 : List (ECode × ECode)) (L : List (ℕ × ECode × ECode)) (nmax : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hBoxAll5 N L2 → hM1 N L nmax →
    ∀ n : ℕ, 1 ≤ n → n ≤ nmax → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f
theorem fullStripM1_of_parts_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (L2 : List (ECode × ECode)) (L : List (ℕ × ECode × ECode)) (nmax : ℕ)
    (hIII : stripIII_full_statementL_S3 N L5 L6) (hSm : smallN_statementL_S3 N L2)
    (hchk : ∀ n, 6 ≤ n → n ≤ nmax → m1Check L n = true) : fullStripM1_statementL_S3 N L5 L6 L2 L nmax
theorem fullStripM1_thm_S3 (N : ℕ) :
    fullStripM1_statementL_S3 N StripIII.box5List (StripIII.o5List ++ L55) (box5AllList34 ++ box5Stage2)
      StripIII.m1List StripIII.NMAX_M1
/-- the package's `fullStripM2_statementL` without hSphereIso, hShared, hRPGibbs, the k-triple and hStripMirror -/
def fullStripM2_statementL_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (D0 M0 nmin : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hM2tail N D0 M0 →
    ∀ n : ℕ, nmin ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f
theorem fullStripM2_of_parts_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (D0 M0 nmin : ℕ) (hIII : stripIII_full_statementL_S3 N L5 L6) (hnmin : 2 * D0 + M0 + 2 ≤ nmin)
    (hn4 : 4 ≤ nmin) : fullStripM2_statementL_S3 N L5 L6 D0 M0 nmin
theorem fullStripM2_thm_S3 (N : ℕ) :
    fullStripM2_statementL_S3 N StripIII.box5List (StripIII.o5List ++ L55) StripIII.D0_M2 StripIII.M0_M2 12
```

### D7: T8, Theorem 1.4 (i), the strip theorem for every n (module G2S3.TopIII; written before its proof)
```lean
/-- T8 with list parameters: the package's `fullStrip_statementL` without hSphereIso, hShared, hRPGibbs, the k-triple and
hStripMirror -/
def fullStrip_statementL_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (L2 : List (ECode × ECode)) (L : List (ℕ × ECode × ECode)) (nmax D0 M0 : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5 N L5 → hS9h N → hS9i N → hO5 N L6 → hBoxAll5 N L2 → hM1 N L nmax →
  hM2tail N D0 M0 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f
theorem fullStrip_of_parts_S3 (N : ℕ) (L5 : List (ECode × ECode)) (L6 : List (ℕ × ECode × ECode))
    (L2 : List (ECode × ECode)) (L : List (ℕ × ECode × ECode)) (nmax D0 M0 nmin : ℕ)
    (h1 : fullStripM1_statementL_S3 N L5 L6 L2 L nmax) (h2 : fullStripM2_statementL_S3 N L5 L6 D0 M0 nmin)
    (hm : nmin ≤ nmax + 1) : fullStrip_statementL_S3 N L5 L6 L2 L nmax D0 M0
theorem fullStrip_thmL_S3 (N : ℕ) :
    fullStrip_statementL_S3 N StripIII.box5List (StripIII.o5List ++ L55) (box5AllList34 ++ box5Stage2)
      StripIII.m1List StripIII.NMAX_M1 StripIII.D0_M2 StripIII.M0_M2
/-- **T8, final S3 form**: S0's `fullStrip_statement_S0r N` (H22, H25, H26-H28 per representative) without hShared,
hRPGibbs, the k-triple and hStripMirror -/
def fullStrip_statement_S3r (N : ℕ) : Prop :=
  (N = 3 ∨ N = 4) → hWeak N →
  ∀ md : StripModes, hStripIdentity N md → hStripCert N md →
  hHub N → hLBu N → hLadder N → hRHCover N → hRHCover350 N →
  hVertSV N → hD4 N → hNE N → hBox5rep N StripIII.box5RepsH22 → hS9h N → hS9i N →
  hO5rep N StripIII.o5Reps → hBoxAll5rep N StripIII.box5Reps → hM1rep N StripIII.m1List StripIII.NMAX_M1 →
  hM2tailRep N StripIII.D0_M2 StripIII.M0_M2 →
    ∀ n : ℕ, 1 ≤ n → ∀ J : ℝ, 0 ≤ J →
      ∀ e ∈ (strip n).edgeSet, ∀ f ∈ (strip n).edgeSet, e ≠ f → G2pair N (strip n) (uniform J) e f
theorem fullStrip_thm_S3r (N : ℕ) : fullStrip_statement_S3r N
```

### D8: the old forms, derived from the S3 forms (module G2S3.TopIII; written before the proofs)
Each proof takes the old premises, drops the removed ones and applies the S3 theorem; none of them calls a package or S0
top theorem. The S0 forms of T3, T4, T5 and S0's concrete T8 are stated inline in S0 (TopS0v2, OrbitB), so their types are
taken from the S0 theorems themselves with `type_of%`, which makes the match exact by construction.
```lean
-- the package's forms (G2Kernel_Lb_p13, StripIII_v2)
theorem stripD_factor_of_S3 (N : ℕ) : stripD_factor_statement N
theorem G2_P3P3_of_S3 (N : ℕ) : G2_P3P3_statement N
theorem strip300_of_S3 (N : ℕ) : strip300_statement N
theorem smallN_of_S3 (N : ℕ) : smallN_statementL N (box5AllList34 ++ box5Stage2)
theorem stripIII_of_S3 (N : ℕ) : stripIII_full_statementL N StripIII.box5List (StripIII.o5List ++ L55)
theorem fullStrip_of_S3 (N : ℕ) :
    fullStrip_statementL N StripIII.box5List (StripIII.o5List ++ L55) (box5AllList34 ++ box5Stage2) StripIII.m1List
      StripIII.NMAX_M1 StripIII.D0_M2 StripIII.M0_M2
-- S0's final forms
theorem stripD_factor_S0_of_S3 : type_of% @stripD_factor_thm_S0
theorem G2_P3P3_S0_of_S3 : type_of% @G2_P3P3_thm_S0
theorem strip300_S0_of_S3 : type_of% @strip300_thm_S0
theorem smallN_S0_of_S3 (N : ℕ) : smallN_statement_S0 N
theorem stripIII_S0r_of_S3 (N : ℕ) : stripIII_statement_S0r N
theorem fullStrip_S0r_of_S3 (N : ℕ) : fullStrip_statement_S0r N
theorem fullStrip_concrete_r_of_S3 : type_of% @fullStrip_thm_concrete_r
```

---

# STATEMENTS_S3_v5 (2026-11-27): successor of STATEMENTS_S3_v4.md (sha8 04d2319d, unchanged). Added: Part C, H8 for the
paper's coefficients and Corollary 3.8's label law at a vertex of degree two with a positive path of any length. Written
before the proofs.

## Part C: the corner factor and the law of the common label

Paper facts. Lemma 2.4 / Corollary 3.8 (tex l.438-460): v a vertex of degree two with edges e = vx, f = vy; integrating
out sigma_v gives Z = sum_c u_c k_c(J_e) k_c(J_f) (display (3) twice and display (2)); the law of the common label is
q_c = u_c k_c(J_e) k_c(J_f) / Z. Corollary 3.8: at N = 3, 4, q >= 0, q charges 0 and 1, and
Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) > 0. H8 `hCornerFactor N k` (package G2Kernel.CornerFactor) is this
factorization at the corners of P_3 x P_n with weights u_c >= 0, u_0, u_1 > 0, u_c <= (c+1)^K U.

Route (a structural optimization; the paper uses SU(2) for N = 4 and spinors for N = 3): u_c = int Pi_c(s_x, s_y) e^{H}
with H the energy without e, f. (V1) the sphere integral of a product of D linear forms is a nonnegative combination of
Gram monomials (polarization from S1's `sphere_moment`); eliminating the vertices other than x, y one at a time turns
every Gram monomial into a nonnegative combination of powers (s_x.s_y)^k; and int int Pi_c(s,t) (s.t)^k >= 0 because
Pi_c is a projection kernel (S1's `zonal_proj`). So u_c >= 0 for EVERY N >= 2, and the paper's N = 3, 4 are special
cases. u_1 > 0 from the term of a positive path x - ... - y (its integral is N^(1 - r) for r edges).

S1 inputs, compiled from unchanged copies (S1_COPIES_v1.sha256; G2S1.Alg ... G2S1.Prop21): `sphere_moment`, `muMom`,
`muMom_odd`, `muMom_even_pos`, `zonal`, `zonal_proj`, `zonal_symm`, `abs_zonal_le`, `continuous_zonal`,
`exp_exp_integral_hasSum`, `hasSum_integral_of_bound`, `summable_kConc_dConc`, `dConc_le_pow`, `labelCov_gen`, `rRate`.

Namespace G2S3, `open G2Kernel`. Notation: ⟪a, z⟫ = `@inner ℝ (Amb N) _ a (z : Amb N)`.

### C1 (module G2S3.GramPol): polarization and (V1)
```lean
/-- the sign of a Boolean -/
def bsgn (b : Bool) : ℝ := if b then 1 else -1
/-- the sign sum of a list of indices -/
def signSum (D : ℕ) (M : List (Fin D)) : ℝ := ∑ ε : Fin D → Bool, (M.map fun i => bsgn (ε i)).prod
theorem signSum_eq (D : ℕ) (M : List (Fin D)) : signSum D M = ∏ l, (1 + (-1 : ℝ) ^ (M.count l))
theorem signSum_nonneg (D : ℕ) (M : List (Fin D)) : 0 ≤ signSum D M
/-- the polarization constant -/
def polK (D : ℕ) : ℝ := ∑ φ : Fin D → Fin D, signSum D (List.finRange D ++ List.ofFn φ)
theorem polK_pos (D : ℕ) : 0 < polK D
/-- polarization -/
theorem polarization (D : ℕ) (t : Fin D → ℝ) :
    ∑ ε : Fin D → Bool, (∏ l, bsgn (ε l)) * (∑ l, bsgn (ε l) * t l) ^ D = polK D * ∏ l, t l
/-- the coefficients of (V1) -/
def polC (N D : ℕ) (p : Fin (D / 2) → Fin D × Fin D) : ℝ :=
  muMom N D / polK D * signSum D (List.finRange D ++ List.ofFn (fun k => (p k).1) ++ List.ofFn (fun k => (p k).2))
theorem polC_nonneg {N : ℕ} (hN : 1 ≤ N) (D : ℕ) (p : Fin (D / 2) → Fin D × Fin D) : 0 ≤ polC N D p
-- helpers
theorem list_prod_map_count (D : ℕ) (M : List (Fin D)) (g : Fin D → ℝ) :
    (M.map g).prod = ∏ l, g l ^ (M.count l)
theorem count_finRange_append (D : ℕ) (M : List (Fin D)) (l : Fin D) :
    (List.finRange D ++ M).count l = 1 + M.count l
theorem surj_of_signSum_ne {D : ℕ} {φ : Fin D → Fin D} (h : signSum D (List.finRange D ++ List.ofFn φ) ≠ 0) :
    Function.Surjective φ
theorem muMom_nonneg {N : ℕ} (hN : 1 ≤ N) (D : ℕ) : 0 ≤ muMom N D
theorem signSum_pairs (D m : ℕ) (p : Fin m → Fin D × Fin D) :
    signSum D (List.finRange D ++ List.ofFn (fun k => (p k).1) ++ List.ofFn (fun k => (p k).2))
      = ∑ ε : Fin D → Bool, (∏ l, bsgn (ε l)) * ∏ k, (bsgn (ε (p k).1) * bsgn (ε (p k).2))
theorem abs_inner_sph_le {N : ℕ} (w : Amb N) (z : Sph N) : |@inner ℝ (Amb N) _ w (z : Amb N)| ≤ ‖w‖
theorem integrable_inner_pow {N : ℕ} (hN : 1 ≤ N) (w : Amb N) (n : ℕ) :
    Integrable (fun z : Sph N => @inner ℝ (Amb N) _ w (z : Amb N) ^ n) (omega N)
/-- **(V1)**: the sphere integral of a product of linear forms is a nonnegative combination of Gram monomials -/
theorem sphere_prod_inner {N : ℕ} (hN : 1 ≤ N) (D : ℕ) (a : Fin D → Amb N) :
    ∫ z : Sph N, ∏ l, @inner ℝ (Amb N) _ (a l) (z : Amb N) ∂(omega N)
      = ∑ p : Fin (D / 2) → Fin D × Fin D, polC N D p * ∏ k, @inner ℝ (Amb N) _ (a (p k).1) (a (p k).2)
```

### C2 (module G2S3.GramElim): vertex elimination
```lean
variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]
/-- Fubini at one vertex -/
theorem integral_update (hN : 0 < N) (v : V) (g : Config N V → ℝ) (hg : BddMeas g) :
    ∫ σ, g σ ∂(freeMeasure N V) = ∫ σ, (∫ z, g (Function.update σ v z) ∂(omega N)) ∂(freeMeasure N V)
/-- the law of two spins -/
theorem integral_two (hN : 0 < N) {x y : V} (hxy : x ≠ y) (φ : Sph N → Sph N → ℝ)
    (hφ : BddMeas (fun p : Sph N × Sph N => φ p.1 p.2)) :
    ∫ σ, φ (σ x) (σ y) ∂(freeMeasure N V) = ∫ s, ∫ t, φ s t ∂(omega N) ∂(omega N)
/-- a Gram word: the product of the scalar products of the listed pairs -/
def gw (L : List (V × V)) (σ : Config N V) : ℝ := (L.map fun q => dot (σ q.1) (σ q.2)).prod
theorem gw_append (L L' : List (V × V)) (σ : Config N V) : gw (L ++ L') σ = gw L σ * gw L' σ
theorem gw_bdd (L : List (V × V)) : BddMeas (gw (N := N) L)
/-- the pairs of L away from v, and the partners of v in L -/
def restW (v : V) (L : List (V × V)) : List (V × V) := L.filter fun q => !(q.1 == v) && !(q.2 == v)
def partW (v : V) (L : List (V × V)) : List V :=
  L.filterMap fun q => if q.1 = v then (if q.2 = v then none else some q.2) else if q.2 = v then some q.1 else none
theorem gw_update (v : V) (L : List (V × V)) (σ : Config N V) (z : Sph N) :
    gw L (Function.update σ v z) = gw (restW v L) σ * ((partW v L).map fun u => dot (σ u) z).prod
/-- a kernel of positive type -/
def PosType (F : Sph N → Sph N → ℝ) : Prop :=
  ∀ k : ℕ, 0 ≤ ∫ s, ∫ t, F s t * dot s t ^ k ∂(omega N) ∂(omega N)
/-- **Vertex elimination** -/
theorem gram_pos (hN : 1 ≤ N) {x y : V} (hxy : x ≠ y) {F : Sph N → Sph N → ℝ}
    (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2)) (hpos : PosType F) (L : List (V × V)) :
    0 ≤ ∫ σ, F (σ x) (σ y) * gw L σ ∂(freeMeasure N V)
/-- Π_c is of positive type -/
theorem zonal_posType {N : ℕ} (hN : 2 ≤ N) (c : ℕ) : PosType (zonal N c)
-- helpers
instance uniqueNotNe (v : V) : Unique {i : V // ¬ i ≠ v}
theorem joinAt_update (v : V) (σ' : {i // i ≠ v} → Sph N) (τ : {i // ¬ i ≠ v} → Sph N) (z : Sph N) :
    Function.update (joinAt v σ' τ) v z = joinAt v σ' (fun _ => z)
theorem gw_cons (q : V × V) (L : List (V × V)) (σ : Config N V) : gw (q :: L) σ = dot (σ q.1) (σ q.2) * gw L σ
theorem gw_ofFn {m : ℕ} (f : Fin m → V × V) (σ : Config N V) : gw (List.ofFn f) σ = ∏ k, dot (σ (f k).1) (σ (f k).2)
theorem abs_gw_le (L : List (V × V)) (σ : Config N V) : |gw L σ| ≤ 1
theorem measurable_gw (L : List (V × V)) : Measurable (gw (N := N) L)
theorem mem_restW {v : V} {L : List (V × V)} {q : V × V} (h : q ∈ restW v L) : q ∈ L ∧ q.1 ≠ v ∧ q.2 ≠ v
theorem mem_partW {v : V} {L : List (V × V)} {u : V} (h : u ∈ partW v L) : u ≠ v ∧ ∃ q ∈ L, u = q.1 ∨ u = q.2
theorem gw_two {x y : V} (L : List (V × V)) (hL : ∀ q ∈ L, (q.1 = x ∨ q.1 = y) ∧ (q.2 = x ∨ q.2 = y)) :
    ∃ k : ℕ, ∀ σ : Config N V, gw L σ = dot (σ x) (σ y) ^ k
```

### C3 (module G2S3.GramExp): the Gibbs weight, and the strict path term
```lean
theorem gram_exp_pos (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y : V} (hxy : x ≠ y) {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2))
    (hpos : PosType F) : 0 ≤ ∫ σ, F (σ x) (σ y) * Real.exp (energy G J σ) ∂(freeMeasure N V)
/-- the second moment: ∫ ⟪a, z⟫ ⟪b, z⟫ = ⟪a, b⟫ / N -/
theorem sphere_inner_inner {N : ℕ} (hN : 0 < N) (a b : Amb N) :
    ∫ z : Sph N, @inner ℝ (Amb N) _ a (z : Amb N) * @inner ℝ (Amb N) _ b (z : Amb N) ∂(omega N)
      = @inner ℝ (Amb N) _ a b / N
/-- the consecutive pairs of a list of vertices -/
def pathW : List V → List (V × V)
  | a :: b :: l => (a, b) :: pathW (b :: l)
  | _ => []
/-- the integral of a path word: a list x :: l of distinct vertices ending at y ≠ x, with r = l.length edges -/
theorem path_integral (hN : 0 < N) : ∀ (l : List V) (x y : V), (x :: l).Nodup → (x :: l).getLast? = some y →
    x ≠ y → ∫ σ, dot (σ x) (σ y) * gw (pathW (x :: l)) σ ∂(freeMeasure N V) = (1 / (N : ℝ)) ^ l.length
/-- **strict form**: a path from x to y with positive couplings -/
theorem gram_exp_path_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y : V} (hxy : x ≠ y) (p : G.Walk x y) (hp : p.IsPath) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    0 < ∫ σ, zonal N 1 (σ x) (σ y) * Real.exp (energy G J σ) ∂(freeMeasure N V)
-- helpers
def ePair (g : Sym2 V) : V × V := Quot.out g
theorem bond_ePair (g : Sym2 V) (σ : Config N V) : bond g σ = dot (σ (ePair g).1) (σ (ePair g).2)
theorem bddF_gw {x y : V} {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2))
    (L : List (V × V)) : BddMeas (fun σ : Config N V => F (σ x) (σ y) * gw L σ)
theorem energy_pow (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (σ : Config N V) (n : ℕ) :
    energy G J σ ^ n = ∑ s : Fin n → G.edgeFinset,
      (∏ k, J (s k)) * gw (List.ofFn fun k => ePair ((s k : G.edgeFinset) : Sym2 V)) σ
theorem integral_F_energy_pow (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {x y : V}
    {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2)) (n : ℕ) :
    ∫ σ, F (σ x) (σ y) * energy G J σ ^ n ∂(freeMeasure N V)
      = ∑ s : Fin n → G.edgeFinset, (∏ k, J (s k)) *
          ∫ σ, F (σ x) (σ y) * gw (List.ofFn fun k => ePair ((s k : G.edgeFinset) : Sym2 V)) σ ∂(freeMeasure N V)
theorem hasSum_integral_exp (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {x y : V}
    {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2)) :
    HasSum (fun n => ∫ σ, F (σ x) (σ y) * (energy G J σ ^ n / (n.factorial : ℝ)) ∂(freeMeasure N V))
      (∫ σ, F (σ x) (σ y) * Real.exp (energy G J σ) ∂(freeMeasure N V))
theorem exp_term_nonneg (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y : V} (hxy : x ≠ y) {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2))
    (hpos : PosType F) (n : ℕ) :
    0 ≤ ∫ σ, F (σ x) (σ y) * (energy G J σ ^ n / (n.factorial : ℝ)) ∂(freeMeasure N V)
theorem gram_exp_term_le (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y : V} (hxy : x ≠ y) {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2))
    (hpos : PosType F) {r : ℕ} (s0 : Fin r → G.edgeFinset) :
    (∏ k, J (s0 k)) * (∫ σ, F (σ x) (σ y) * gw (List.ofFn fun k => ePair ((s0 k : G.edgeFinset) : Sym2 V)) σ
        ∂(freeMeasure N V)) / (r.factorial : ℝ)
      ≤ ∫ σ, F (σ x) (σ y) * Real.exp (energy G J σ) ∂(freeMeasure N V)
theorem mem_pathW : ∀ (l : List V) (q : V × V), q ∈ pathW l → q.1 ∈ l ∧ q.2 ∈ l
theorem gw_update_of_notMem {u : V} (L : List (V × V)) (hL : ∀ q ∈ L, q.1 ≠ u ∧ q.2 ≠ u) (σ : Config N V)
    (z : Sph N) : gw L (Function.update σ u z) = gw L σ
theorem walk_gw (G : SimpleGraph V) {u w : V} (p : G.Walk u w) (σ : Config N V) :
    (p.edges.map fun g => bond g σ).prod = gw (pathW p.support) σ
```

### C4 (module G2S3.CornerFact): the factorization at a vertex of degree two, and H8
```lean
/-- the weight of the common label: u_c = ∫ Π_c(σ_x, σ_y) e^{H}, H the energy with J_e = J_f = 0 -/
def uCorner (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : Sym2 V) (x y : V) (c : ℕ) : ℝ :=
  ∫ σ, zonal N c (σ x) (σ y) * Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ) ∂(freeMeasure N V)
/-- Lemma 2.4 at a vertex of degree two: Z = Σ_c u_c k_c(a) k_c(b) for all real a, b -/
theorem corner_factor (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V}
    (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y) (a b : ℝ) :
    HasSum (fun c => uCorner N G J s(v, x) s(v, y) x y c * kConc N c a * kConc N c b)
      (partition N G (Function.update (Function.update J s(v, x) a) s(v, y) b))
theorem uCorner_nonneg (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {v x y : V} (hxy : x ≠ y) (c : ℕ) : 0 ≤ uCorner N G J s(v, x) s(v, y) x y c
theorem uCorner_zero_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V} :
    0 < uCorner N G J s(v, x) s(v, y) x y 0
theorem uCorner_le (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V} (c : ℕ) :
    uCorner N G J s(v, x) s(v, y) x y c ≤ ((c : ℝ) + 1) ^ N * uCorner N G J s(v, x) s(v, y) x y 0
theorem uCorner_one_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {v x y : V} (hxy : x ≠ y) (p : G.Walk x y) (hp : p.IsPath) (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    0 < uCorner N G J s(v, x) s(v, y) x y 1
/-- **H8 for the paper's coefficients**, every N ≥ 2 (the top theorems use N = 3, 4) -/
theorem hCornerFactor_kConc (N : ℕ) (hN : 2 ≤ N) : hCornerFactor N (kConc N)
-- helpers
theorem ferro_update2 {G : SimpleGraph V} [DecidableRel G.Adj] {J : Sym2 V → ℝ} (hJ : Ferro G J) (e f : Sym2 V) :
    Ferro G (Function.update (Function.update J e 0) f 0)
theorem bond_update_of_notMem {g : Sym2 V} {v : V} (hv : v ∉ g) (σ : Config N V) (z : Sph N) :
    bond g (Function.update σ v z) = bond g σ
theorem energy_update_two (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeFinset) (hf : f ∈ G.edgeFinset) (hef : e ≠ f) (a b : ℝ) (σ : Config N V) :
    energy G (Function.update (Function.update J e a) f b) σ
      = energy G (Function.update (Function.update J e 0) f 0) σ + a * bond e σ + b * bond f σ
theorem nbr_edge {G : SimpleGraph V} [DecidableRel G.Adj] {v x y : V} (hnb : G.neighborFinset v = {x, y})
    {g : Sym2 V} (hg : g ∈ G.edgeFinset) (hv : v ∈ g) : g = s(v, x) ∨ g = s(v, y)
theorem energy0_update_v (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V}
    (hnb : G.neighborFinset v = {x, y}) (σ : Config N V) (z : Sph N) :
    energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) (Function.update σ v z)
      = energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) σ
theorem abs_kConc_le_series (hN : 2 ≤ N) (c : ℕ) (a : ℝ) :
    |kConc N c a| ≤ (∑' m : ℕ, ((|a| / 2) ^ 2) ^ m / (m.factorial : ℝ)) * ((|a| / 2) ^ c / (c.factorial : ℝ))
theorem zonal_bdd (hN : 2 ≤ N) (c : ℕ) : BddMeas (fun q : Sph N × Sph N => zonal N c q.1 q.2)
theorem expE_bdd (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    BddMeas (fun σ : Config N V => Real.exp (energy G J σ))
theorem zonal_zero (N : ℕ) (s t : Sph N) : zonal N 0 s t = 1
theorem uCorner_zero_eq (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (v x y : V) :
    uCorner N G J s(v, x) s(v, y) x y 0
      = partition N G (Function.update (Function.update J s(v, x) 0) s(v, y) 0)
/-- the neighbours of a corner of P_3 × P_n -/
theorem strip_corner_nbr' {n : ℕ} (hn : 3 ≤ n) {c x y : Fin 3 × Fin n} (hc : isCorner n c)
    (hx : (strip n).Adj c x) (hy : (strip n).Adj c y) (hxy : x ≠ y) : (strip n).neighborFinset c = {x, y}
```

### C5 (module G2S3.Cor38): Corollary 3.8 at a vertex of degree two, any positive path
```lean
/-- the law of the common label of e = vx and f = vy -/
def qLabel (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (v x y : V) (c : ℕ) : ℝ :=
  uCorner N G J s(v, x) s(v, y) x y c * kConc N c (J s(v, x)) * kConc N c (J s(v, y)) / partition N G J
/-- **Corollary 3.8, the law of the common label** (every N ≥ 2): q is a probability law on ℕ, nonnegative, and it
charges the labels 0 and 1 -/
theorem cor38_law (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {v x y : V} (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y))
    (p : G.Walk x y) (hp : p.IsPath) (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    (∀ c, 0 ≤ qLabel N G J v x y c) ∧ HasSum (qLabel N G J v x y) 1 ∧
      0 < qLabel N G J v x y 0 ∧ 0 < qLabel N G J v x y 1
/-- **Corollary 3.8, the covariance identity** (V : Type, as in the package's covDeriv_statement) -/
theorem cor38_cov {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y)
    (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y)) :
    gibbsCov N G J (bond s(v, x)) (bond s(v, y))
      = covW (qLabel N G J v x y) (fun c => rRate N c (J s(v, x))) (fun c => rRate N c (J s(v, y)))
/-- Corollary 3.8 in the paper's form: N = 3 or N = 4 -/
theorem cor38_paper {V : Type} [Fintype V] [DecidableEq V] (hN : N = 3 ∨ N = 4) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hnb : G.neighborFinset v = {x, y})
    (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y)) (p : G.Walk x y) (hp : p.IsPath)
    (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    (∀ c, 0 ≤ qLabel N G J v x y c) ∧ HasSum (qLabel N G J v x y) 1 ∧
      0 < qLabel N G J v x y 0 ∧ 0 < qLabel N G J v x y 1 ∧
      gibbsCov N G J (bond s(v, x)) (bond s(v, y))
        = covW (qLabel N G J v x y) (fun c => rRate N c (J s(v, x))) (fun c => rRate N c (J s(v, y)))
-- helpers
theorem update_self_self (J : Sym2 V → ℝ) (e f : Sym2 V) : Function.update (Function.update J e (J e)) f (J f) = J
theorem corner_hasSum_Z (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V}
    (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y) :
    HasSum (fun c => uCorner N G J s(v, x) s(v, y) x y c * kConc N c (J s(v, x)) * kConc N c (J s(v, y)))
      (partition N G J)
theorem kConc_pos' (hN : 2 ≤ N) (c : ℕ) {a : ℝ} (ha : 0 < a) : 0 < kConc N c a
```
Not in this plan: the strict sign Cov_q(r_c(J_e), r_c(J_f)) > 0 for paths of any length. It follows from cor38_law with
Lemma 2.2 (`hRatio_kConc`, stage S2) and a strict Chebyshev step; at the corners of P_3 x P_n it is already proved
(`hCornerPair_holds`, Part B8).

## Notes as built (2026-11-27 13:12Z)
- Every statement of Part C above is proved as written: clean rebuild logs/j76_v2clean.out (scripts/mods_S3_v2.txt,
  38 modules: Parts A, B, Top, TopIII, the 11 unchanged S1 copies, Part C), AXIOMS_S3_v2.txt (92 theorems, all
  [propext, Classical.choice, Quot.sound]).
- Edits made to this file before the proofs they concern: the index list in `polC` (two `List.ofFn` of the first and the
  second components, in place of a `flatMap`; the same multiset of indices), the argument order of `path_integral`
  (`∀ l x y, ...`, for the structural recursion), and the helper statements, each appended before its module was compiled.
- No statement differs in content from the paper. H8 and Corollary 3.8 are proved for every N ≥ 2; the paper's N = 3, 4
  are special cases, and `cor38_paper` states the paper's form.

---

# STATEMENTS_S3_v6 (2026-11-27): successor of STATEMENTS_S3_v5.md (sha8 473b20d5, unchanged). Adds the freeze record, the
list of paper results that the Part C route replaces, and the planned statements for Corollary 3.8's strict covariance on
paths of any length (written before their proofs, outside the frozen set).

## Freeze record (after M4)
- Frozen modules: the 38 modules of scripts/mods_S3_v2.txt.
  - Part A: RPCore, RPGraph, RPEnergy, RPInst, RPNamed.
  - Part B: Gin, Cone, ConeInt, Coords, Spheres, Sphere3, ConeMem, Dup, GKSz, Dunlop.
  - The corner part (B8): Moments, StrictTerm, StrictDup, GKSzStrict, Corner.
  - Part D: Top, TopIII.
  - The 11 unchanged S1 copies G2S1.Alg ... G2S1.Prop21 (S1_COPIES_v1.sha256).
  - Part C: GramPol, GramElim, GramExp, CornerFact, Cor38.
  - The record module G2S3.AxS3 prints `#print axioms` for every theorem of these modules (532 theorems; generated by
    scripts/gen_axs3_v1.py).
- sha256 of every file: FREEZE_S3_v1.sha256. Fresh clean build: logs/j78_freeze.out (scripts/mods_S3_freeze_v1.txt,
  39 modules, 0 errors). AXIOMS_S3_v3.txt: 624 lines, each a subset of [propext, Classical.choice, Quot.sound].
- After the freeze these files are not edited; new work goes in new modules.
- The statements of the frozen modules are those of STATEMENTS_S3.md (9e4c4052), _v2 (b4e3f1ae), _v3 (3812dbab),
  _v4 (04d2319d) and _v5 (473b20d5). This file adds no statement for them.
- For the H16 proof: `hShared_holds3`, `hShared_holds4` (G2S3.Dunlop, sha8 f81d36d8) and the chain RPCore ... Dunlop
  are unchanged since M2.
- H16 `hLadder N` stays a named premise of T5-T8 in their S3 forms (Top, TopIII).

## Part C: the paper results that the route replaces
This record was asked for after M5, so it is recorded here, after the proofs; the
Part C statements themselves were written in v5 before their proofs.
- The route proves u_c >= 0 directly, for every N >= 2, by vertex elimination (`sphere_prod_inner`, `gram_pos`,
  `zonal_posType`, `gram_exp_pos`), and u_1 > 0 by the term of a positive path (`gram_exp_path_pos`).
- For H8 and for Corollary 3.8 at a vertex of degree two it replaces:
  - at N = 3: Lemmas 3.4 and 3.5, Proposition 5.4 (used by Lemma 3.5: the kernel of a graph lies in the class P),
    Proposition 3.6 (tex l.396) and Corollary 3.8 (tex l.438);
  - at N = 4: Lemma 4.1 (tex l.457, W >= 0 via SU(2)) with the label expansion (4).
- These paper results are not formalized, and H8 and Corollary 3.8 do not depend on them here. The replacement covers the
  case these two results use (A = {v}, a vertex of degree two). Proposition 3.6 and Theorem 3.7 for general 2-edge cuts,
  and Lemma 4.1 for general labellings, are not covered.

## Planned, outside the frozen set: Corollary 3.8, strict covariance on positive paths of any length
Route: the paper's proof of Corollary 3.8 ("Lemma 2.2 with Chebyshev's inequality gives a positive covariance"):
`cor38_cov` (Part C), Lemma 2.2 = `hRatio_kConc` (stage S2, compiled from an unchanged copy of G2S2.Ratio, sha8 c7631cbb,
which imports only G2S0.KData), and a strict Chebyshev step. Modules: G2S2/Ratio (copy), G2S3/Cor38Pos. Namespace G2S3.
```lean
/-- strict Chebyshev: under a probability law q on ℕ that charges 0 and 1, two strictly increasing sequences with
summable q f, q g, q f g are positively correlated -/
theorem covW_pos (q f g : ℕ → ℝ) (hq : ∀ c, 0 ≤ q c) (hq1 : HasSum q 1) (hf : StrictMono f) (hg : StrictMono g)
    (hsf : Summable (fun c => q c * f c)) (hsg : Summable (fun c => q c * g c))
    (hsfg : Summable (fun c => q c * (f c * g c))) (h0 : 0 < q 0) (h1 : 0 < q 1) : 0 < covW q f g
/-- the weights and the coefficients with their first derivatives at two positive couplings -/
theorem summable_corner_box {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hxy : x ≠ y) {a b : ℝ} (ha : 0 < a)
    (hb : 0 < b) :
    Summable (fun c => |uCorner N G J s(v, x) s(v, y) x y c| * (|kConc N c a| + |deriv (kConc N c) a|)
      * (|kConc N c b| + |deriv (kConc N c) b|))
/-- **Corollary 3.8, the strict covariance** (every N ≥ 2) -/
theorem cor38_cov_pos {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hnb : G.neighborFinset v = {x, y})
    (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y)) (p : G.Walk x y) (hp : p.IsPath)
    (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    0 < gibbsCov N G J (bond s(v, x)) (bond s(v, y))
/-- **Corollary 3.8 in the paper's form, complete** (N = 3 or N = 4): the law of the common label is nonnegative and
charges 0 and 1, and Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) > 0 -/
theorem cor38_full {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : N = 3 ∨ N = 4) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hnb : G.neighborFinset v = {x, y})
    (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y)) (p : G.Walk x y) (hp : p.IsPath)
    (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    (∀ c, 0 ≤ qLabel N G J v x y c) ∧ HasSum (qLabel N G J v x y) 1 ∧
      0 < qLabel N G J v x y 0 ∧ 0 < qLabel N G J v x y 1 ∧
      gibbsCov N G J (bond s(v, x)) (bond s(v, y))
        = covW (qLabel N G J v x y) (fun c => rRate N c (J s(v, x))) (fun c => rRate N c (J s(v, y))) ∧
      0 < gibbsCov N G J (bond s(v, x)) (bond s(v, y))
```

---

# STATEMENTS_S3_v7 (2026-11-27): successor of STATEMENTS_S3_v6.md (sha8 fb5e860c, unchanged). As-built note only.

## Corollary 3.8, strict covariance on positive paths of any length (planned in v6, now proved)
- `covW_pos`, `summable_corner_box`, `cor38_cov_pos` and `cor38_full` are proved exactly as stated in v6, in the new
  module G2S3.Cor38Pos (outside the frozen set). Lemma 2.2 enters as `hRatio_kConc` from G2S2.Ratio, compiled from an
  unchanged copy (S2_COPIES_v1.sha256, sha8 c7631cbb).
- Fresh clean build: logs/j82_post.out (scripts/mods_S3_post_v1.txt = the 39 modules of the freeze list, then
  G2S2/Ratio, then G2S3/Cor38Pos), 0 errors; AXIOMS_S3_v4.txt.
- With `cor38_full`, Corollary 3.8 (tex l.438) is formalized in full at N = 3 and N = 4: the law of the common label is
  nonnegative and charges 0 and 1, and Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) > 0, for every finite graph, every vertex
  of degree two and every positive path of any length in G - v. `cor38_cov_pos` holds for every N >= 2.

---

# STATEMENTS_S3_v8 (2026-11-27): successor of STATEMENTS_S3_v7.md (sha8 598d24e1, unchanged). Part E: Theorem 3.7 and
Theorem 1.2(b) by the Part C route (plan PLAN_NEXT_S3_v1, f4582de4). Written before the proofs. Each module's
helper statements are appended before that module's first compile. New modules only (list scripts/mods_S3_E_v1.txt);
the frozen set and Cor38Pos are not touched.

Paper (release source v4.42rc5):
- Theorem 1.2 (tex l.118-124) and the definition of a 2-edge cut before it (tex l.112-114);
- Lemma 2.4 (tex l.282-286): the law of the common label, and continuity at zero couplings;
- Proposition 2.1 (tex l.235): the package's `covDeriv_thm` with S1's `labelCov_gen`;
- Lemma 2.2 (tex l.247): `hRatio_kConc` (S2 copy);
- Theorem 3.2, edge case (tex l.322): `hShared_holds4` (S3 Part B);
- Proposition 3.6 (tex l.396): the factorization at a cut, here by vertex elimination, for every N;
- Theorem 3.7 (tex l.419).

Namespace G2S3, `open G2Kernel`.

## E1 (module G2S3.CutGraph): 2-edge cuts and cycles
```lean
/-- **2-edge cut** (tex l.112-114), in the paper's equivalent form: "e and f lie in the same component, neither is a
bridge, and removing both disconnects that component" -/
def IsTwoEdgeCut {V : Type*} (G : SimpleGraph V) (e f : Sym2 V) : Prop :=
  e ∈ G.edgeSet ∧ f ∈ G.edgeSet ∧ e ≠ f ∧ (∃ a ∈ e, ∃ b ∈ f, G.Reachable a b) ∧ ¬ G.IsBridge e ∧ ¬ G.IsBridge f ∧
    ∃ u v, (∃ a ∈ e, G.Reachable a u) ∧ G.Reachable u v ∧ ¬ (G.deleteEdges {e, f}).Reachable u v
/-- the sides of a cut: e = s(x, y), f = s(z, w), x, z ∈ A, y, w ∉ A, and no other edge crosses -/
structure CutSides {V : Type*} (G : SimpleGraph V) (x y z w : V) (A : Set V) : Prop where
  adj_e : G.Adj x y
  adj_f : G.Adj z w
  ne : s(x, y) ≠ s(z, w)
  xA : x ∈ A
  yA : y ∉ A
  zA : z ∈ A
  wA : w ∉ A
  side : ∀ a b, G.Adj a b → s(a, b) ≠ s(x, y) → s(a, b) ≠ s(z, w) → (a ∈ A ↔ b ∈ A)
theorem cut_sides {V : Type*} {G : SimpleGraph V} {x y z w : V} (hcut : IsTwoEdgeCut G s(x, y) s(z, w)) :
    ∃ A : Set V, CutSides G x y z w A ∨ CutSides G x y w z A
/-- a cycle through the edge s(x, y) gives a path from x to y inside the cycle, avoiding s(x, y) -/
theorem cycle_path {V : Type*} [DecidableEq V] {G : SimpleGraph V} {x y u : V} (c : G.Walk u u) (hc : c.IsCycle)
    (he : s(x, y) ∈ c.edges) : ∃ p : G.Walk x y, p.IsPath ∧ ∀ g ∈ p.edges, g ∈ c.edges ∧ g ≠ s(x, y)
```
Note: the first form of the definition (G - {e, f} has more components than G, while G - e and G - f do not) is not
formalized. The paper states the equivalence in the same sentence.

## E2 (module G2S3.GramSide): vertex elimination respecting a cut
```lean
variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]
/-- words whose pairs never cross the cut stay so under elimination -/
theorem gram_pos_side (hN : 1 ≤ N) (T : Finset V) (A : Set V) {F : Config N V → ℝ} (hF : BddMeas F)
    (hFT : ∀ v ∉ T, ∀ (σ : Config N V) (z : Sph N), F (Function.update σ v z) = F σ)
    (hbase : ∀ L : List (V × V), (∀ q ∈ L, q.1 ∈ T ∧ q.2 ∈ T ∧ (q.1 ∈ A ↔ q.2 ∈ A)) →
      0 ≤ ∫ σ, F σ * gw L σ ∂(freeMeasure N V))
    (L : List (V × V)) (hL : ∀ q ∈ L, (q.1 ∈ A ↔ q.2 ∈ A)) : 0 ≤ ∫ σ, F σ * gw L σ ∂(freeMeasure N V)
theorem gram_exp_side (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    (T : Finset V) (A : Set V) {F : Config N V → ℝ} (hF : BddMeas F)
    (hFT : ∀ v ∉ T, ∀ (σ : Config N V) (z : Sph N), F (Function.update σ v z) = F σ)
    (hJA : ∀ a b, G.Adj a b → J s(a, b) ≠ 0 → (a ∈ A ↔ b ∈ A))
    (hbase : ∀ L : List (V × V), (∀ q ∈ L, q.1 ∈ T ∧ q.2 ∈ T ∧ (q.1 ∈ A ↔ q.2 ∈ A)) →
      0 ≤ ∫ σ, F σ * gw L σ ∂(freeMeasure N V)) :
    0 ≤ ∫ σ, F σ * Real.exp (energy G J σ) ∂(freeMeasure N V)
```

## E3 (module G2S3.CutBase): the four-terminal integrals
```lean
/-- for words on {x, y, z, w} that never cross the cut: zero off the diagonal, nonnegative on it -/
theorem cut_base (hN : 2 ≤ N) {x y z w : V} {A : Set V} (hxA : x ∈ A) (hyA : y ∉ A) (hzA : z ∈ A) (hwA : w ∉ A)
    (hef : ¬ (x = z ∧ y = w)) (c c' : ℕ) (L : List (V × V))
    (hL : ∀ q ∈ L, q.1 ∈ ({x, y, z, w} : Finset V) ∧ q.2 ∈ ({x, y, z, w} : Finset V) ∧ (q.1 ∈ A ↔ q.2 ∈ A)) :
    (c ≠ c' → ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * gw L σ ∂(freeMeasure N V) = 0) ∧
    (c = c' → 0 ≤ ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * gw L σ ∂(freeMeasure N V))
```

## E4 (module G2S3.CutFact): the factorization at a cut (Proposition 3.6 by the new route, every N)
```lean
/-- the weight of the common label at a cut -/
def uCut (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (x y z w : V) (c : ℕ) : ℝ :=
  ∫ σ, zonal N c (σ x) (σ y) * zonal N c (σ z) (σ w) *
    Real.exp (energy G (Function.update (Function.update J s(x, y) 0) s(z, w) 0) σ) ∂(freeMeasure N V)
theorem cut_offdiag (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) {c c' : ℕ} (hcc : c ≠ c') :
    ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) *
      Real.exp (energy G (Function.update (Function.update J s(x, y) 0) s(z, w) 0) σ) ∂(freeMeasure N V) = 0
theorem uCut_nonneg (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (c : ℕ) : 0 ≤ uCut N G J x y z w c
theorem cut_factor (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (a b : ℝ) :
    HasSum (fun c => uCut N G J x y z w c * kConc N c a * kConc N c b)
      (partition N G (Function.update (Function.update J s(x, y) a) s(z, w) b))
theorem uCut_zero_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (x y z w : V) :
    0 < uCut N G J x y z w 0
theorem uCut_le (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (x y z w : V) (c : ℕ) :
    |uCut N G J x y z w c| ≤ ((c : ℝ) + 1) ^ (2 * N) * uCut N G J x y z w 0
/-- u_1 > 0 when a positive path joins x to y avoiding e (and J_f > 0) -/
theorem uCut_one_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (hJf : 0 < J s(z, w)) (p : G.Walk x y) (hp : p.IsPath)
    (hpe : ∀ g ∈ p.edges, g ≠ s(x, y)) (hpos : ∀ g ∈ p.edges, 0 < J g) : 0 < uCut N G J x y z w 1
```

## E5 (module G2S3.Thm37): the law under p, the covariance, Theorems 3.7 and 1.2(b)
```lean
/-- the law of the common label c = ℓ_e = ℓ_f under p (Lemma 2.4, tex l.282) -/
def commonLaw {V : Type} [Fintype V] [DecidableEq V] (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (e f : G.edgeFinset) (c : ℕ) : ℝ :=
  ∑' ℓ : G.edgeFinset → ℕ, if ℓ e = c ∧ ℓ f = c then labelLaw N G J ℓ else 0
/-- the joint marginal of two labels under the label expansion (4) -/
theorem joint_label {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (e f : G.edgeFinset) (hef : e ≠ f) (c c' : ℕ) :
    HasSum (fun ℓ : G.edgeFinset → ℕ =>
        if ℓ e = c ∧ ℓ f = c' then labelWeight N G ℓ * ∏ g, kConc N (ℓ g) (J g) else 0)
      (kConc N c (J e) * kConc N c' (J f) * ∫ σ, zon N c (bond (e : Sym2 V) σ) * zon N c' (bond (f : Sym2 V) σ) *
        Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ) ∂(freeMeasure N V))
/-- **the fidelity link for Corollary 3.8**: Part C's q (factorization weights) is the law of the common label under p -/
theorem qLabel_eq_commonLaw {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V} (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y)
    (hvx : G.Adj v x) (hvy : G.Adj v y) (c : ℕ) :
    qLabel N G J v x y c = commonLaw N G J ⟨s(v, x), G.mem_edgeFinset.mpr hvx⟩ ⟨s(v, y), G.mem_edgeFinset.mpr hvy⟩ c
/-- nonstrict Chebyshev -/
theorem covW_nonneg (q f g : ℕ → ℝ) (hq : ∀ c, 0 ≤ q c) (hq1 : HasSum q 1) (hf : Monotone f) (hg : Monotone g)
    (hsf : Summable (fun c => q c * f c)) (hsg : Summable (fun c => q c * g c))
    (hsfg : Summable (fun c => q c * (f c * g c))) : 0 ≤ covW q f g
/-- **Theorem 3.7, every N ≥ 2** -/
theorem thm37_all {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) (e f : G.edgeFinset)
    (hcut : IsTwoEdgeCut G (e : Sym2 V) (f : Sym2 V)) :
    (∀ c, 0 ≤ commonLaw N G J e f c) ∧ 0 ≤ gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V)) ∧
      (0 < J e → 0 < J f → (∃ (u : V) (c : G.Walk u u), c.IsCycle ∧ (e : Sym2 V) ∈ c.edges ∧ (f : Sym2 V) ∈ c.edges ∧
          ∀ g ∈ c.edges, 0 < J g) → 0 < gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V)))
/-- **Theorem 3.7** (tex l.419): N = 3 -/
theorem thm37 {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJ : Ferro G J) (e f : G.edgeFinset) (hcut : IsTwoEdgeCut G (e : Sym2 V) (f : Sym2 V)) :
    (∀ c, 0 ≤ commonLaw 3 G J e f c) ∧ 0 ≤ gibbsCov 3 G J (bond (e : Sym2 V)) (bond (f : Sym2 V)) ∧
      (0 < J e → 0 < J f → (∃ (u : V) (c : G.Walk u u), c.IsCycle ∧ (e : Sym2 V) ∈ c.edges ∧ (f : Sym2 V) ∈ c.edges ∧
          ∀ g ∈ c.edges, 0 < J g) → 0 < gibbsCov 3 G J (bond (e : Sym2 V)) (bond (f : Sym2 V)))
/-- the cut part of Theorem 1.2(b), every N ≥ 2 -/
theorem cut_cov_nonneg {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) (e f : Sym2 V) (hcut : IsTwoEdgeCut G e f) :
    0 ≤ gibbsCov N G J (bond e) (bond f)
/-- **Theorem 1.2(b)** (tex l.122): N = 4, every finite graph -/
theorem thm12b {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJ : Ferro G J) (e f : Sym2 V) (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) :
    ((∃ v, v ∈ e ∧ v ∈ f) ∨ IsTwoEdgeCut G e f) → 0 ≤ gibbsCov 4 G J (bond e) (bond f)
```

## Helper statements
NOTE (process): the helpers of E1-E3 below were added to their modules and compiled before being recorded here; the main
statements above were written before any proof. The E4 helpers are recorded here before E4's first compile.
```lean
-- E1 (CutGraph); R = (G.deleteEdges {s(x, y), s(z, w)}).Reachable
theorem cut_step {a b : V} (h : G.Adj a b) (he : s(a, b) ≠ s(x, y)) (hf : s(a, b) ≠ s(z, w)) :
    (G.deleteEdges {s(x, y), s(z, w)}).Reachable a b
theorem reach_of_edge {a b p q : V} (R : V → V → Prop) (hR : ∀ u, R u u) (hsymm : ∀ u v, R u v → R v u)
    (hpq : R p q) (h : s(a, b) = s(p, q)) : R a b
theorem reach_sub_f (hxy : (G.deleteEdges {s(x, y), s(z, w)}).Reachable x y) {u v : V}
    (h : (G.deleteEdges {s(z, w)}).Reachable u v) : (G.deleteEdges {s(x, y), s(z, w)}).Reachable u v
theorem reach_sub_e (hzw : (G.deleteEdges {s(x, y), s(z, w)}).Reachable z w) {u v : V}
    (h : (G.deleteEdges {s(x, y)}).Reachable u v) : (G.deleteEdges {s(x, y), s(z, w)}).Reachable u v
theorem reach_sub_all (hxy : (G.deleteEdges {s(x, y), s(z, w)}).Reachable x y)
    (hzw : (G.deleteEdges {s(x, y), s(z, w)}).Reachable z w) {u v : V} (h : G.Reachable u v) :
    (G.deleteEdges {s(x, y), s(z, w)}).Reachable u v
theorem reach_f_cases {u v : V} (h : (G.deleteEdges {s(z, w)}).Reachable u v) :
    (G.deleteEdges {s(x, y), s(z, w)}).Reachable u v ∨
      ((G.deleteEdges {s(x, y), s(z, w)}).Reachable u x ∧ (G.deleteEdges {s(x, y), s(z, w)}).Reachable y v) ∨
      ((G.deleteEdges {s(x, y), s(z, w)}).Reachable u y ∧ (G.deleteEdges {s(x, y), s(z, w)}).Reachable x v)
-- E2 (GramSide)
theorem mem_partW' {v : V} {L : List (V × V)} {u : V} (h : u ∈ partW v L) :
    ∃ q ∈ L, (q.1 = v ∧ q.2 = u) ∨ (q.2 = v ∧ q.1 = u)
theorem ePair_eq (g : Sym2 V) : s((ePair g).1, (ePair g).2) = g
theorem integral_G_energy_pow (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    {F : Config N V → ℝ} (hF : BddMeas F) (n : ℕ) :
    ∫ σ, F σ * energy G J σ ^ n ∂(freeMeasure N V) = ∑ s : Fin n → G.edgeFinset, (∏ k, J (s k)) *
      ∫ σ, F σ * gw (List.ofFn fun k => ePair ((s k : G.edgeFinset) : Sym2 V)) σ ∂(freeMeasure N V)
theorem hasSum_integral_expG (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    {F : Config N V → ℝ} (hF : BddMeas F) :
    HasSum (fun n => ∫ σ, F σ * (energy G J σ ^ n / (n.factorial : ℝ)) ∂(freeMeasure N V))
      (∫ σ, F σ * Real.exp (energy G J σ) ∂(freeMeasure N V))
-- E3 (CutBase)
theorem zonal_pair_bdd (hN : 2 ≤ N) (c : ℕ) (a b : V) : BddMeas (fun σ : Config N V => zonal N c (σ a) (σ b))
theorem dot_pow_bdd (a b : V) (p : ℕ) : BddMeas (fun σ : Config N V => dot (σ a) (σ b) ^ p)
theorem int_out_pair (hN : 2 ≤ N) {u a b : V} (hau : a ≠ u) (hbu : b ≠ u) (c e : ℕ) {R : Config N V → ℝ}
    (hR : BddMeas R) (hRu : ∀ (σ : Config N V) (z : Sph N), R (Function.update σ u z) = R σ) :
    ∫ σ, zonal N c (σ a) (σ u) * zonal N e (σ u) (σ b) * R σ ∂(freeMeasure N V)
      = if c = e then ∫ σ, zonal N c (σ a) (σ b) * R σ ∂(freeMeasure N V) else 0
theorem pos_int (hN : 2 ≤ N) {x z : V} (hxz : x ≠ z) (c p : ℕ) :
    0 ≤ ∫ σ, zonal N c (σ x) (σ z) * dot (σ x) (σ z) ^ p ∂(freeMeasure N V)
theorem dot_two {x z a b : V} (ha : a = x ∨ a = z) (hb : b = x ∨ b = z) :
    ∃ i : ℕ, ∀ σ : Config N V, dot (σ a) (σ b) = dot (σ x) (σ z) ^ i
theorem gw_side4 {x y z w : V} {A : Set V} (hxA : x ∈ A) (hyA : y ∉ A) (hzA : z ∈ A) (hwA : w ∉ A)
    (L : List (V × V)) (hL : ∀ q ∈ L, q.1 ∈ ({x, y, z, w} : Finset V) ∧ q.2 ∈ ({x, y, z, w} : Finset V) ∧
      (q.1 ∈ A ↔ q.2 ∈ A)) :
    ∃ p q : ℕ, ∀ σ : Config N V, gw L σ = dot (σ x) (σ z) ^ p * dot (σ y) (σ w) ^ q
theorem base_gen (hN : 2 ≤ N) {x y z w : V} (hxy : x ≠ y) (hxw : x ≠ w) (hzy : z ≠ y) (hzw : z ≠ w) (hxz : x ≠ z)
    (hyw : y ≠ w) (c c' p q : ℕ) :
    (c ≠ c' → ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) * (dot (σ x) (σ z) ^ p * dot (σ y) (σ w) ^ q)
      ∂(freeMeasure N V) = 0) ∧
    (c = c' → 0 ≤ ∫ σ, zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w) *
      (dot (σ x) (σ z) ^ p * dot (σ y) (σ w) ^ q) ∂(freeMeasure N V))
-- E4 (CutFact), recorded before compiling
theorem hasSum_edge (hN : 2 ≤ N) {p q : V} {F : Config N V → ℝ} (hF : BddMeas F) (a : ℝ) :
    HasSum (fun c => kConc N c a * ∫ σ, F σ * zonal N c (σ p) (σ q) ∂(freeMeasure N V))
      (∫ σ, F σ * Real.exp (a * dot (σ p) (σ q)) ∂(freeMeasure N V))
theorem cutJ_side {G : SimpleGraph V} {J : Sym2 V → ℝ} {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) :
    ∀ a b, G.Adj a b → Function.update (Function.update J s(x, y) 0) s(z, w) 0 s(a, b) ≠ 0 → (a ∈ A ↔ b ∈ A)
theorem F4_invariant {x y z w : V} (c c' : ℕ) : ∀ v ∉ ({x, y, z, w} : Finset V), ∀ (σ : Config N V) (t : Sph N),
    zonal N c ((Function.update σ v t) x) ((Function.update σ v t) y) *
      zonal N c' ((Function.update σ v t) z) ((Function.update σ v t) w)
      = zonal N c (σ x) (σ y) * zonal N c' (σ z) (σ w)
```
```lean
-- E5a (LawP), recorded before compiling: commonLaw, joint_label, qLabel_eq_commonLaw as in section E5, and
theorem commonLaw_eq {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj]
    (J : Sym2 V → ℝ) (e f : G.edgeFinset) (hef : e ≠ f) (c : ℕ) :
    commonLaw N G J e f c = kConc N c (J e) * kConc N c (J f) * (∫ σ, zon N c (bond (e : Sym2 V) σ) *
      zon N c (bond (f : Sym2 V) σ) * Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ)
        ∂(freeMeasure N V)) / partition N G J
```
```lean
-- E5a (LawP) helpers. NOTE (process): phiJ, sJ, the helpers phiJ_hasSum to labelBound_summable and joint_label_raw
-- were compiled in the LawP drafts (jobs j90-j97) before being recorded here; series_prod_integral is recorded here
-- before its first compile. Context: {N : ℕ} {V : Type} [Fintype V] [DecidableEq V].
/-- the per-edge series of the joint marginal: single terms at e and f -/
def phiJ (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (c c' : ℕ)
    (σ : Config N V) (g : G.edgeFinset) (a : ℕ) : ℝ :=
  if (g = e ∧ a ≠ c) ∨ (g = f ∧ a ≠ c') then 0 else kConc N a (J g) * zon N a (bond (g : Sym2 V) σ)
/-- its edgewise sums -/
def sJ (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (c c' : ℕ)
    (σ : Config N V) (g : G.edgeFinset) : ℝ :=
  if g = e then kConc N c (J g) * zon N c (bond (g : Sym2 V) σ)
  else if g = f then kConc N c' (J g) * zon N c' (bond (g : Sym2 V) σ)
  else Real.exp (J g * bond (g : Sym2 V) σ)
theorem phiJ_hasSum (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (hef : e ≠ f) (c c' : ℕ) (σ : Config N V) (g : G.edgeFinset) :
    HasSum (phiJ N G J e f c c' σ g) (sJ N G J e f c c' σ g)
theorem phiJ_abs_le (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (c c' : ℕ) (σ : Config N V) (g : G.edgeFinset) (a : ℕ) :
    |phiJ N G J e f c c' σ g a| ≤ |kConc N a (J g)| * dConc N a
theorem sJ_prod (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (hef : e ≠ f)
    (c c' : ℕ) (σ : Config N V) :
    ∏ g, sJ N G J e f c c' σ g = kConc N c (J e) * kConc N c' (J f) *
      (zon N c (bond (e : Sym2 V) σ) * zon N c' (bond (f : Sym2 V) σ) *
        Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ))
theorem phiJ_prod (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset) (hef : e ≠ f)
    (c c' : ℕ) (σ : Config N V) (ℓ : G.edgeFinset → ℕ) :
    ∏ g, phiJ N G J e f c c' σ g (ℓ g) = if ℓ e = c ∧ ℓ f = c' then
      ∏ g, (kConc N (ℓ g) (J g) * zon N (ℓ g) (bond (g : Sym2 V) σ)) else 0
theorem phiJ_summable (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (c c' : ℕ) (σ : Config N V) (g : G.edgeFinset) : Summable (fun a => ‖phiJ N G J e f c c' σ g a‖)
theorem phiJ_prod_hasSum (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : G.edgeFinset) (hef : e ≠ f) (c c' : ℕ) (σ : Config N V) :
    HasSum (fun ℓ : G.edgeFinset → ℕ => ∏ g, phiJ N G J e f c c' σ g (ℓ g)) (∏ g, sJ N G J e f c c' σ g)
theorem phiJ_measurable (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (c c' : ℕ) (ℓ : G.edgeFinset → ℕ) (g : G.edgeFinset) :
    Measurable (fun σ : Config N V => phiJ N G J e f c c' σ g (ℓ g))
theorem phiJ_prod_measurable (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (c c' : ℕ) (ℓ : G.edgeFinset → ℕ) :
    Measurable (fun σ : Config N V => ∏ g, phiJ N G J e f c c' σ g (ℓ g))
theorem phiJ_prod_abs_le (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (e f : G.edgeFinset) (c c' : ℕ) (ℓ : G.edgeFinset → ℕ) (σ : Config N V) :
    |∏ g, phiJ N G J e f c c' σ g (ℓ g)| ≤ ∏ g, (|kConc N (ℓ g) (J g)| * dConc N (ℓ g))
theorem labelBound_summable (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    Summable (fun ℓ : G.edgeFinset → ℕ => ∏ g, (|kConc N (ℓ g) (J g)| * dConc N (ℓ g)))
/-- dominated convergence for a product of coordinate series over a finite index type -/
theorem series_prod_integral (hN : 2 ≤ N) {E : Type} [Fintype E] (φ : Config N V → E → ℕ → ℝ)
    (S : Config N V → E → ℝ) (B : E → ℕ → ℝ) (hφ : ∀ σ, HasSum (fun ℓ : E → ℕ => ∏ g, φ σ g (ℓ g)) (∏ g, S σ g))
    (hmeas : ∀ ℓ : E → ℕ, Measurable (fun σ => ∏ g, φ σ g (ℓ g))) (hbound : ∀ σ g a, |φ σ g a| ≤ B g a)
    (hBs : Summable (fun ℓ : E → ℕ => ∏ g, B g (ℓ g))) :
    HasSum (fun ℓ : E → ℕ => ∫ σ, ∏ g, φ σ g (ℓ g) ∂(freeMeasure N V)) (∫ σ, ∏ g, S σ g ∂(freeMeasure N V))
/-- the joint marginal, before identifying the terms -/
theorem joint_label_raw (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    (hef : e ≠ f) (c c' : ℕ) :
    HasSum (fun ℓ : G.edgeFinset → ℕ => ∫ σ, ∏ g, phiJ N G J e f c c' σ g (ℓ g) ∂(freeMeasure N V))
      (∫ σ, ∏ g, sJ N G J e f c c' σ g ∂(freeMeasure N V))
```

## E5 addition (main statement, recorded before compiling G2S3.Thm37)
```lean
/-- the law of the common label at a 2-edge cut is a probability law (Lemma 2.4, tex l.282: "the law of the common
label c = ℓ_e = ℓ_f under p") -/
theorem commonLaw_hasSum {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) (e f : G.edgeFinset)
    (hcut : IsTwoEdgeCut G (e : Sym2 V) (f : Sym2 V)) : HasSum (commonLaw N G J e f) 1
```
Note: Lemma 2.4's first sentence (W(ℓ) = 0 for each labelling with ℓ_e ≠ ℓ_f) is not formalized and not used: the route
groups the labellings by (ℓ_e, ℓ_f) (`joint_label`).

## E5b (G2S3.Thm37) helpers, recorded before the first compile
```lean
theorem sym2_exists_mk {W : Type*} (e : Sym2 W) : ∃ x y : W, e = s(x, y)
theorem kConc_nonneg {N : ℕ} (hN : 2 ≤ N) (c : ℕ) {a : ℝ} (ha : 0 ≤ a) : 0 ≤ kConc N c a
theorem summable_box {N : ℕ} (hN : 2 ≤ N) (u : ℕ → ℝ) (K : ℕ) (U : ℝ) (hu : ∀ c, |u c| ≤ ((c : ℝ) + 1) ^ K * U)
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Summable (fun c => |u c| * (|kConc N c a| + |deriv (kConc N c) a|) * (|kConc N c b| + |deriv (kConc N c) b|))
theorem summable_q_box {N : ℕ} (hN : 2 ≤ N) (u : ℕ → ℝ) (K : ℕ) (U : ℝ)
    (hu : ∀ c, |u c| ≤ ((c : ℝ) + 1) ^ K * U) {a b : ℝ} (ha : 0 < a) (hb : 0 < b) (Z : ℝ) (A B : ℕ → ℝ)
    (hA : ∀ c, |A c| ≤ |kConc N c a| + |deriv (kConc N c) a|)
    (hB : ∀ c, |B c| ≤ |kConc N c b| + |deriv (kConc N c) b|) : Summable (fun c => u c * A c * B c / Z)
-- context {N : ℕ} {V : Type} [Fintype V] [DecidableEq V]
/-- Proposition 2.1 for a single-label factorization -/
theorem cov_factor_eq (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) (u : ℕ → ℝ) (K : ℕ) (U : ℝ)
    (hu : ∀ c, |u c| ≤ ((c : ℝ) + 1) ^ K * U)
    (hZ : ∀ a b, HasSum (fun c => u c * kConc N c a * kConc N c b)
      (partition N G (Function.update (Function.update J e a) f b)))
    (hJe : 0 < J e) (hJf : 0 < J f) :
    gibbsCov N G J (bond e) (bond f) = covW (fun c => u c * kConc N c (J e) * kConc N c (J f) / partition N G J)
      (fun c => rRate N c (J e)) (fun c => rRate N c (J f))
def qCut (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (x y z w : V) (c : ℕ) : ℝ :=
  uCut N G J x y z w c * kConc N c (J s(x, y)) * kConc N c (J s(z, w)) / partition N G J
theorem cut_law_data (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (hJe : 0 < J s(x, y)) (hJf : 0 < J s(z, w)) :
    (∀ c, 0 ≤ qCut N G J x y z w c) ∧ HasSum (qCut N G J x y z w) 1 ∧
      Summable (fun c => qCut N G J x y z w c * rRate N c (J s(x, y))) ∧
      Summable (fun c => qCut N G J x y z w c * rRate N c (J s(z, w))) ∧
      Summable (fun c => qCut N G J x y z w c * (rRate N c (J s(x, y)) * rRate N c (J s(z, w)))) ∧
      gibbsCov N G J (bond s(x, y)) (bond s(z, w))
        = covW (qCut N G J x y z w) (fun c => rRate N c (J s(x, y))) (fun c => rRate N c (J s(z, w)))
theorem cut_cov_nonneg_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (hJe : 0 < J s(x, y)) (hJf : 0 < J s(z, w)) :
    0 ≤ gibbsCov N G J (bond s(x, y)) (bond s(z, w))
theorem cut_cov_strict (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (hJe : 0 < J s(x, y)) (hJf : 0 < J s(z, w))
    (p : G.Walk x y) (hp : p.IsPath) (hpe : ∀ g ∈ p.edges, g ≠ s(x, y)) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    0 < gibbsCov N G J (bond s(x, y)) (bond s(z, w))
def shiftJ (J : Sym2 V → ℝ) (e f : Sym2 V) (t : ℝ) : Sym2 V → ℝ :=
  Function.update (Function.update J e (J e + t)) f (J f + t)
theorem contAt_int_shift (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) {F : Config N V → ℝ} (hF : BddMeas F) :
    ContinuousAt (fun t : ℝ => ∫ σ, F σ * Real.exp (energy G (shiftJ J e f t) σ) ∂(freeMeasure N V)) 0
theorem contAt_cov_shift (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) :
    ContinuousAt (fun t : ℝ => gibbsCov N G (shiftJ J e f t) (bond e) (bond f)) 0
/-- zero couplings, by continuity (Lemma 2.4, last sentence) -/
theorem cut_cov_nonneg_ferro (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJ : Ferro G J) {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) :
    0 ≤ gibbsCov N G J (bond s(x, y)) (bond s(z, w))
theorem commonLaw_cut (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    {x y z w : V} (he : (e : Sym2 V) = s(x, y)) (hf : (f : Sym2 V) = s(z, w)) (hef : e ≠ f) (c : ℕ) :
    commonLaw N G J e f c
      = uCut N G J x y z w c * kConc N c (J s(x, y)) * kConc N c (J s(z, w)) / partition N G J
theorem commonLaw_hasSum_core (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJ : Ferro G J) (e f : G.edgeFinset) {x y z w : V} {A : Set V} (he : (e : Sym2 V) = s(x, y))
    (hf : (f : Sym2 V) = s(z, w)) (hS : CutSides G x y z w A) : HasSum (commonLaw N G J e f) 1
theorem thm37_core (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    (e f : G.edgeFinset) {x y z w : V} {A : Set V} (he : (e : Sym2 V) = s(x, y)) (hf : (f : Sym2 V) = s(z, w))
    (hS : CutSides G x y z w A) :
    (∀ c, 0 ≤ commonLaw N G J e f c) ∧ 0 ≤ gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V)) ∧
      (0 < J e → 0 < J f → (∃ (u : V) (c : G.Walk u u), c.IsCycle ∧ (e : Sym2 V) ∈ c.edges ∧ (f : Sym2 V) ∈ c.edges ∧
          ∀ g ∈ c.edges, 0 < J g) → 0 < gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V)))
```

## As built (2026-11-27)
- List scripts/mods_S3_E_v1.txt (sha8 137fe8ae), 6 new modules, 1,778 lines: G2S3/CutGraph 189 (039a197c), GramSide 224
  (caeb1247), CutBase 263 (4c9181fc), CutFact 289 (2a210a73), LawP 311 (13b8d8c1), Thm37 502 (a234d78c). Axioms record
  G2S3/AxS3E (73 lines, 422a2aec, generated by scripts/gen_axs3_v2.py): `#print axioms` for all 66 theorems of the list.
- Clean build: scripts/mods_S3_E_build_v1.txt (0983d2da, the list plus AxS3E), job j105, log logs/j105_Eclean.out,
  Lean 4.35.0-rc3, BUILD DONE, 26 s, 0.008 core-h. Every theorem shows a subset of [propext, Classical.choice,
  Quot.sound] (64 the full set, `reach_of_edge` [propext, Quot.sound], `sym2_exists_mk` none). No sorry, no new axiom.
  The frozen set (FREEZE_S3_v1.sha256, 52 files), Cor38Pos (feef8aba) and the S1/S2 copies are byte-stable.
- Statement check: scripts/check_stmts_E_v2.py (04fcbfad), logs/j103_stmts.out and, on this file with the as-built
  section, logs/j106_stmts.out (same result; the code blocks are unchanged since): 69 MATCH, 5 BINDERS (the
  declaration uses section variables for {V : Type} [Fintype V] [DecidableEq V], resp. {V} {G} {x y z w} in CutGraph:
  cut_sides, commonLaw, joint_label, qLabel_eq_commonLaw, commonLaw_eq), 0 DIFF, 0 MISSING, 0 unrecorded theorems.
- Presentation edits before this file was cited: in E4 the shorthand binders (G), (J) are written out, and in four E1
  helpers the abbreviation R is written out. No statement changed.
- Paper results from this route: Theorem 3.7 (`thm37`, N = 3; `thm37_all`, every N ≥ 2); Theorem 1.2(b) (`thm12b`,
  N = 4; the cut part `cut_cov_nonneg` for every N ≥ 2); the law of the common label of Lemma 2.4 under p
  (`commonLaw`, `joint_label`, `commonLaw_hasSum`), its continuity step at zero couplings (`cut_cov_nonneg_ferro`), and
  the fidelity link for Corollary 3.8 (`qLabel_eq_commonLaw`). Proposition 3.6 enters as `cut_factor`: Z(a, b) =
  Σ_c u_c k_c(a) k_c(b) with u_c ≥ 0 defined by a Gibbs integral (`uCut`); the paper's form (2c+1) α_c β_c is not stated.
  Lemma 4.1 (SU(2)) and Schur's lemma are not used.

---

# STATEMENTS_S3_v9 (2026-11-27): successor of STATEMENTS_S3_v8.md (a7edb250, unchanged; frozen in FREEZE_S3E_v1.sha256,
71e6488b, and under audit). It corrects one claim about the frozen S3 set (audit finding F1) and states the proviso of the
delta audit. No Lean statement is added or changed, and no module is edited.

Paper line numbers: v4.42rc5 / v4.41 release source, and in brackets the v4.43p8 release source used by the audit.
Corollary 3.8 = tex l.438-442 [l.453-457]; the label weight p = tex l.230 [l.245]; W(ℓ) = tex l.223 [l.238];
Π_ℓ(σ, σ') = d_ℓ C̃_ℓ(σ·σ') = tex l.206 [l.221].

## F1 (AUDIT_S3H16_v1.md, 9d8d8829): `cor38_paper` is weaker than Corollary 3.8
- STATEMENTS_S3_v5.md l.257-258 reads: "No statement differs in content from the paper. H8 and Corollary 3.8 are proved
  for every N ≥ 2; the paper's N = 3, 4 are special cases, and `cor38_paper` states the paper's form." This overclaims.
- Corollary 3.8 also asserts Cov(s_e, s_f) > 0. `cor38_paper` (G2S3/Cor38.lean:178, frozen) has the nonnegative law, the
  charge at the labels 0 and 1 and the identity Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)), but not Cov > 0. So
  `cor38_paper` is WEAKER than Corollary 3.8.
- Corrected reading of v5 l.257-258: "H8 and the law and identity clauses of Corollary 3.8 are proved for every N ≥ 2.
  `cor38_paper` states those clauses at N = 3, 4, without the strict Cov > 0. The full corollary is `cor38_full`."
- The full corollary is `cor38_full` (G2S3/Cor38Pos.lean, feef8aba; statements in STATEMENTS_S3_v6.md, as built in v7).
  It has every hypothesis and clause of Corollary 3.8, the strict Cov > 0 included; the delta audit (AUDIT_S3H16_v2.md,
  f0d5aef5) rates its hypotheses and Cov > 0 EXACT.

## Proviso (AUDIT_S3H16_v2.md, f0d5aef5), attached to STATEMENTS_S3_v7.md l.9-11
- v7 l.9-11 reads: "With `cor38_full`, Corollary 3.8 (tex l.438) is formalized in full at N = 3 and N = 4: the law of the
  common label is nonnegative and charges 0 and 1, and Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) > 0, ..."
- Proviso: the law and identity clauses of `cor38_full` (and of `cor38_law`, `cor38_cov`, `cor38_paper`) are about
  `qLabel`, the law defined by the factorization weights u_c of Part C:
  qLabel N G J v x y c = u_c k_c(J_e) k_c(J_f) / Z. They match the corollary's "law of the common label" exactly once
  qLabel equals the marginal of the paper's label weight p(ℓ) = W(ℓ) Π_e k_{ℓ_e}(J_e) / Z_{G,J}.
- That equality is the theorem `G2S3.qLabel_eq_commonLaw` (G2S3/LawP.lean, 13b8d8c1; Part E, now under audit):
  qLabel N G J v x y c = commonLaw N G J e f c for e = vx, f = vy, every N ≥ 2, every c, where
  `commonLaw N G J e f c = Σ'_ℓ (if ℓ e = c ∧ ℓ f = c then labelLaw N G J ℓ else 0)` (LawP.lean l.23-24) is the law of the
  common label c = ℓ_e = ℓ_f under p. Here `labelLaw` (S1 copy G2S1/Prop21.lean l.87) is
  labelWeight N G ℓ · Π_e kConc N (ℓ e) (J e) / partition N G J, and `labelWeight` (S1 copy G2S1/Labels.lean l.92) is
  ∫ Π_{e ∈ E} dConc N (ℓ e) · CConc N (ℓ e) (s_e) d(Π_x ω): the paper's W(ℓ) with Π_ℓ = d_ℓ C̃_ℓ(σ·σ'). The series
  defining commonLaw converges absolutely (`joint_label`), and its sum is given by `commonLaw_eq`.
- So, given `qLabel_eq_commonLaw`, the law and identity clauses of `cor38_full` hold with the paper's law of the common
  label in place of `qLabel`. Until that theorem is audited, the v7 claim "formalized in full" carries this proviso.

---

# STATEMENTS_S3_v10 (closing note, written for this release)

The proviso of v9 no longer applies: `qLabel_eq_commonLaw` (LawP.lean) proves that the factorization law `qLabel` equals the
law of the common label under the paper's label weight p (`commonLaw`). So, for finite simple graphs, the law clauses of `cor38_law` and `cor38_full` are
those of Corollary 3.8, and `cor38_full` states Corollary 3.8 exactly.
