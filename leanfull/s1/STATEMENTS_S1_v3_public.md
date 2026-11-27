# STATEMENTS_S1_v3: the Lean statements of stage S1 (successor of STATEMENTS_S1_v2.md, sha8 dfc3d266, unchanged)

Every Lean statement in this file is about finite simple graphs (Mathlib's SimpleGraph); the paper's Theorems 1.1 and
1.2(b) also cover parallel edges through its Section 3.3 reduction, which is not formalized.

Changes against v2: the rank tie is PROVED (module G2S1.RankTie, sha8 44e30cf4), with one signature note below; the
rest is v2's text. (v2's own changes against v1: the two sections at the top, written before their proofs.)

## Theorem 1.1 with NO hypotheses (merge of S0, S1, S2), module G2S1.TopFull: PROVED
Paper, Theorem 1.1 (cycles and cacti), tex lines 108-111: "Let N ≥ 2 and let every block of G be a cycle or a single edge.
Then Cov(s_e,s_f) ≥ 0 for every pair of edges e ≠ f and all couplings J ≥ 0. The inequality is strict when e and f lie
on a common cycle whose couplings are all positive."
```lean
theorem cactus_thm_full (N : ℕ) (hN : 2 ≤ N) :
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J → ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → G2pair N G J e f
theorem cactus_strict_full (N : ℕ) (hN : 2 ≤ N) :
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], BlocksCycleOrEdge G →
      ∀ J : Sym2 V → ℝ, Ferro G J →
      ∀ (n : ℕ) (φ : Fin n → V), 3 ≤ n → Function.Injective φ →
        (∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)) →
        (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
        ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
          0 < gibbsCov N G J (bond e) (bond f)
```
- `G2pair N G J e f` is `0 ≤ gibbsCov N G J (bond e) (bond f)` (package G2Kernel.Defs): Cov(s_e, s_f) ≥ 0 under the Gibbs
  measure of the O(N) model on G with couplings J; `Ferro G J`: J_e ≥ 0 on every edge; `BlocksCycleOrEdge G`: every block
  of G is a cycle or a single edge (S0, G2S0.BlocksA); the strict part's common
  cycle is an injective φ : Fin n → V, n ≥ 3, along edges of G, with positive couplings on its edges (S0, G2S0.BlocksC).
- Proofs: `cactus_thm_S1 N hN (hRatio_kConc N hN)` and `cactus_strict_S1 N hN (hRatio_kConc N hN)`, with H4 from
  G2S2.Ratio, a copy of the module of stage S2 (sha256 c7631cbb…).
- No premise besides N ≥ 2; `#print axioms` = [propext, Classical.choice, Quot.sound] (AXIOMS_S1_public.txt).

## The rank of the projection Π_ℓ (tie of d_ℓ), module G2S1.RankTie: PROVED
Signature notes (no change of mathematical content): `finiteDimensional_zonalSpan` is proved for every N, without the
premise 2 ≤ N, as an `instance finiteDimensional_zonalSpan (N l : ℕ)` (the span lies in the span of the coordinate
monomials of degree ≤ ℓ for any N); `projOp_of_mem`, `projOp_mem`, `finrank_zonalSpan` are exactly as stated.
```lean
/-- the span of the zonal functions z ↦ Π_ℓ(x, z), x ∈ S^{N-1} -/
def zonalSpan (N l : ℕ) : Submodule ℝ (Sph N → ℝ) :=
  Submodule.span ℝ (Set.range fun x : Sph N => fun z : Sph N => zonal N l x z)
/-- the integral operator with kernel Π_ℓ -/
def projOp (N l : ℕ) (f : Sph N → ℝ) : Sph N → ℝ := fun x => ∫ z, zonal N l x z * f z ∂(omega N)
theorem projOp_of_mem (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {f : Sph N → ℝ} (hf : f ∈ zonalSpan N l) : projOp N l f = f
theorem projOp_mem (N : ℕ) (hN : 2 ≤ N) (l : ℕ) {f : Sph N → ℝ} (hf : Continuous f) : projOp N l f ∈ zonalSpan N l
theorem finiteDimensional_zonalSpan (N : ℕ) (hN : 2 ≤ N) (l : ℕ) : FiniteDimensional ℝ (zonalSpan N l)
theorem finrank_zonalSpan (N : ℕ) (hN : 2 ≤ N) (l : ℕ) : (Module.finrank ℝ (zonalSpan N l) : ℝ) = dConc N l
```
Paper fact (§2.1): "The orthogonal projection onto H_ℓ in L^2(ω) is the integral operator with kernel Π_ℓ", H_ℓ of dimension
d_ℓ. These statements say: P_ℓ = projOp N l maps continuous functions onto zonalSpan N l and is the identity there
(so P_ℓ ∘ P_ℓ = P_ℓ), and its range has dimension d_ℓ: d_ℓ is the rank of the projection with kernel Π_ℓ. (The
identification of zonalSpan with the harmonic polynomials of degree ℓ is not formalized.)


Paper: "Positive correlation of bond energies in the O(3) and O(4) models" (release source v4.42rc5,
G2_PAPER_v4_42rc5_release.tex), Section 2.1 (displays (2), (3), lines 201-219),
Section 2.2 (display (4), Proposition 2.1, lines 220-246), Section 3.1 (the ring formula, lines 302-305), Theorem 1.1.
Namespace `G2Kernel`; modules `G2S1.*` in s1/src/G2S1. Data `kConc`, `dConc`, `CConc` from G2S0.KData (S0), unchanged.
Every statement assumes `2 ≤ N` (`3 ≤ N` for the generating function). All are proved (AXIOMS_S1_public.txt).

Record of the order of work: the exported statements were fixed in an interface file (v1, sha8 a185f466) before any
proof; this file collects them with the paper references at the end of the stage. Changes against v1: none in
mathematical content. Two notes: `labelLaw`, `rRate`, `covLabel`, `prop21` take `V : Type` (not `Type*`) because the
package's `covDeriv_statement` (Proposition 2.1, first equality) quantifies over `V : Type`; `integral_CConc_sq` is
proved in the v1 form (ω) and also in a μ_N form (`integral_CConc_sq_muN`).

## H2 and H5 (the hypotheses removed)
| Lean | statement | paper |
|---|---|---|
| `hFH_conc` (Expand) | `hFH N (kConc N) (dConc N) (CConc N)` | (3) on [-1,1]; C̃_ℓ(1) = 1; 0 ≤ d_ℓ ≤ (ℓ+1)^N (paper: (ℓ+1)^{N-1}); (2) |
| `hCycleZ_conc` (CycleZ) | `hCycleZ N (kConc N) (dConc N)`: Z_{C_n} = Σ_c d_c ∏_g k_c(J_g), n ≥ 3 | §3.1, the formula for Z_C |
| `cactus_thm_S1`, `cactus_strict_S1` (TopS1) | Theorem 1.1 (nonstrict, strict) for the paper's data with the single premise `hRatio (kConc N)` (H4, stage S2) | Theorem 1.1 |

## Display (2), display (3) and the sphere
| Lean | statement | paper |
|---|---|---|
| `zonal N l x y` (Zonal, def) | Π_ℓ(σ,τ) = d_ℓ C̃_ℓ(σ·τ) | §2.1 |
| `zonal_proj` | ∫ Π_a(x,z) Π_b(z,y) ω(dz) = δ_ab Π_a(x,y) | display (2) |
| `zonal_symm`, `zonal_self`, `continuous_zonal` | Π symmetric, Π_ℓ(x,x) = d_ℓ, continuity | §2.1 |
| `abs_CConc_le_one`, `abs_zonal_le` | |C̃_ℓ| ≤ 1 on [-1,1]; |Π_ℓ| ≤ d_ℓ | used for |W(ℓ)| ≤ ∏ d (§2.2) |
| `exp_dot_hasSum`, `exp_hasSum_zon` | e^{J σ·τ} = Σ_ℓ k_ℓ(J) Π_ℓ(σ,τ) (absolutely, any J) | display (3) |
| `summable_kConc_dConc` | Σ_ℓ |k_ℓ(J)| d_ℓ < ∞ | §2.1 |
| `kConc_eq_integral`, `kConc_eq_integral_muN` | k_ℓ(J) = ∫ e^{Jt} C̃_ℓ(t) μ_N(dt) | display (3), second line |
| `zonal_posDef` | Σ_ij c_i c_j Π_ℓ(x_i,x_j) ≥ 0 | (positive-definite kernel, used in S3) |
| `exp_exp_integral_hasSum` | ∫ e^{a x·z} e^{b z·y} ω(dz) = Σ_c k_c(a) k_c(b) Π_c(x,y) | integrating out a vertex of degree 2 (§2.4, §3.1) |
| `sphere_moment` (Moments) | ∫ ⟪w,z⟫^n ω(dz) = |w|^n μ_n | the law μ_N of σ·e (§2.1) |
| `two_point_CF` (TwoPoint) | ∫ (x·z)^p (y·z)^q ω(dz) = p! q! R(p,q)(x·y) | (lemma behind (2)) |

## Display (4) and Proposition 2.1
| Lean | statement | paper |
|---|---|---|
| `labelWeight N G ℓ` (Labels, def) | W(ℓ) = ∫ ∏_{xy∈E} Π_{ℓ_xy}(σ_x,σ_y) ∏ ω(dσ_x) | §2.2 |
| `partition_hasSum_labels` | Z_{G,J} = Σ_ℓ W(ℓ) ∏_e k_{ℓ_e}(J_e), absolutely | display (4) |
| `abs_labelWeight_le` | |W(ℓ)| ≤ ∏_e d_{ℓ_e} | §2.2 |
| `labelWeight_cycle` (CycleZ) | on C_{m+2}: W(ℓ) = [ℓ constant = c] d_c | §3.1 ("the projections force all labels to be equal") |
| `labelLaw`, `rRate`, `covLabel` (Prop21, defs) | p(ℓ) = W(ℓ)∏k/Z; r_ℓ = ∂_J log k_ℓ; Cov_p(r_{ℓ_e}, r_{ℓ_f}) | §2.2 |
| `hasSum_labelLaw` | Σ_ℓ p(ℓ) = 1 | §2.2 ("total mass one") |
| `prop21` | e ≠ f, J_e, J_f > 0: Cov(s_e,s_f) = ∂_{J_e}∂_{J_f} log Z = Cov_p(r_{ℓ_e}(J_e), r_{ℓ_f}(J_f)) | Proposition 2.1 |

## The tie of d_ℓ, C̃_ℓ, k_ℓ to the paper's objects
| Lean | statement | paper |
|---|---|---|
| `CConc_two_cos`, `CConc_two_eq_chebyshevT` (Tie) | N = 2: C̃_ℓ(cos θ) = cos ℓθ = T_ℓ(cos θ) | §2.1 ("for N = 2, C̃_ℓ(cos θ) = cos ℓθ") |
| `dConc_three`, `dConc_four`, `CConc_four_eq_chebyshevU` | d_ℓ = 2ℓ+1 (N=3); d_ℓ = (ℓ+1)^2 and (ℓ+1) C̃_ℓ = U_ℓ (N=4) | §4 line 453 |
| `muN`, `integral_CConc_mul`, `integral_CConc_sq(_muN)` | μ_N = law of σ·x; ∫ C̃_a C̃_b dμ_N = δ_ab / d_a | §2.1 (μ_N; d_ℓ normalises Π_ℓ) |
| `natDegree_cPoly`, `cPoly_eval_one`, `CConc_unique` | deg C̃_n = n, C̃_n(1) = 1, and the only polynomials P_n with deg ≤ n, P_n(1) = 1, μ_N-orthogonal are C̃_n | C̃_ℓ = normalized Gegenbauer (orthogonality characterization) |
| `gegenbauer_genFun` (GenFun) | N ≥ 3, λ = N/2-1: Σ_n C(n+N-3,n) C̃_n(t) r^n = (1-2tr+r^2)^{-λ}, t ∈ [-1,1], |r| < 1 | C̃_ℓ = C^λ_ℓ / C^λ_ℓ(1) (generating-function definition, [Wa44]) |
Not proved (not planned): d_ℓ = dim of the harmonic polynomials of degree ℓ. d_ℓ is tied to the
projection Π_ℓ by (2), `zonal_self` (trace d_ℓ) and `integral_CConc_sq` (d_ℓ = 1/‖C̃_ℓ‖^2 in L^2(μ_N)).
