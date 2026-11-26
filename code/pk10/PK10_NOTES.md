# PK10_NOTES: G2 on uniform 3 × n grids at strong coupling (wave 18, part pk10, reference)

Status: INTERIM v6 (§10–§12 appended in round 3, §13 in round 4, §14–§15 in round 5; §1–§9 as in v3), 2026-10-30. Directory /mnt/g2/release/root/code/pk10/ (scripts/, scratch/, log scratch/PROGRESS.md).
Labels: [proved], [proved | X], [sketch], [heuristic], [numerical], [lit.].

**Setup.** O(N) model, N = 3 or 4, on G = P₃ × P_n with every coupling equal to J. Edges are named as in the engine: t_j, h_j, bb_j are the top, middle and bottom horizontals between columns j and j+1, and a_j, b_j are the top–middle and middle–bottom verticals of column j. For an edge pair, m is the column offset. G2 means Cov(E_e, E_f) ≥ 0 with E_e = q_x·q_y.

## 0. Answer first

1. **Harmonic leading order, every pair type [proved | G2WOLFF §6 expansion; computed exactly].**
   - J²·Cov(E_e, E_f) = c₂ + c₃/J + O(J⁻²), with c₂ = (N−1)·T(e,f)²/2. Here T(e,f) is the transfer current, the current through f for a unit current across e on the unit-conductance grid; equivalently c₂ = (N−1)Δ²/8 with G2WOLFF's Δ. In UST terms, T² = P(e∈UST)P(f∈UST) − P(e,f∈UST).
   - T is a sum over the transverse modes of P₃ (Laplacian eigenvalues 0, 1, 3; vectors (1,1,1), (1,0,−1), (1,−2,1)). Mode k decays along the strip like e^{−κ_k m}, with cosh κ_k = 1 + λ_k/2, so κ₁ = 0.9624 and κ₂ = 1.5668. The zero mode carries no current between distinct cuts.
   - So c₂ decays like e^{−2κ₁m} (ratio 0.146 per column) for pairs where both edges see mode 1, i.e. all pairs not involving the middle row. It decays like e^{−2κ₂m} (ratio 0.0436) when one edge is a middle-row horizontal h_j, because mode 1 vanishes on the middle row. Tables in §2.
2. **Check against the exact O(4) model [numerical].** I computed every pair on P₃ × P₄ at J = 10 and 20 and on P₃ × P₇ at J = 10, with the dense strip engine (snapshot). Labels ≤ 18/16 at J = 10 and ≤ 22/20 at J = 20 agree to all printed digits.
   - The ratio exact/(c₂ + c₃/J) lies between 1.001 and 1.10 at J = 10, and between 1.0003 and 1.031 at J = 20 (P₃ × P₄). The deviation shrinks about 3–4× per doubling of J, i.e. O(J⁻²).
   - Every exact covariance is positive (all pairs on P₃ × P₄ and P₃ × P₇). The review has been asked for the corresponding numbers from the UNIF §9.4 runs.
3. **Near-zeros and the next order (kill tests) [numerical].**
   - There is no exact zero of T at integer offsets, in the bulk or at the ends. The only dip is the "diagonal verticals" pair (a_j, b_{j+1}). There the mode-1 and mode-2 terms cancel near m ≈ 0.86, leaving |T| = 0.0171 at m = 1, smaller than at m = 2 (0.0184).
     - There c₂ = 4.4·10⁻⁴ but c₃ = +6.45·10⁻³ (N = 4) and +2.68·10⁻³ (N = 3), both positive. The exact J²Cov at J = 10 is 1.45·10⁻³ (P₃ × P₇) and 1.78·10⁻³ (P₃ × P₄). No kill.
   - c₃ > 0 in every non-adjacent pair computed: 120/124 at N = 4 and 62/62 at N = 3, over n = 8, 12, 16. The coefficients converge in n, to 3–4 digits between n = 12 and 16, so no growth from the zero mode.
     - The 4 negatives are the adjacent middle-row pairs (h_j, h_{j+1}), which share a vertex. There J* = |c₃|/c₂ = 0.11–0.15, far outside the expansion, and adjacent pairs are covered by G2WOLFF's shared-vertex theorem.
   - **Non-uniformity in distance.** For pairs involving the middle row, c₂ decays at rate 2κ₂ while c₃ decays at rate 2κ₁ (ratio 0.147 per column for (t_j, h_{j+m})). So at fixed J the "leading" term is overtaken at m ≳ log J/(2(κ₂ − κ₁)).
     - The overtaking terms are positive. On P₃ × P₇ at J = 10 the exact covariance exceeds c₂ + c₃/J by 1.18–1.34× for (t₀, h_{3…5}) and up to 2.3× for (h₀, h₅).
4. **The heuristic is confirmed [heuristic, consistent with all data].**
   - Invariant functions of a column depend only on the Gram entries q_i·q_j, which are quadratic in the relative deviations (modes 1, 2). So SO(N)-invariant one-phonon states do not exist for N ≥ 3 (SO(N−1) fixes no vector).
   - The lowest invariant excitation is the two-phonon singlet (1,1), at energy 2κ₁ = 1.925 per column ("≈ 2"), top–bottom even. Next come (1,2) at κ₁ + κ₂ = 2.53 (odd) and (2,2) at 2κ₂ = 3.13. The zero mode drops out of the invariant sector.
   - The exact covariance of (t₀, h_m) on P₃ × P₇ at J = 10 decays with ratio 0.148 per column, against e^{−2κ₁} = 0.146.
   - Middle-row edges have zero (1,1) amplitude at harmonic order. Their O(1/J) amplitude has the same sign as the others, because c₃(t, h_m) > 0 at large m. **So all (1,1) amplitudes are one-signed, and that channel gives a positive contribution to every pair.** This is the strong-coupling counterpart of the "one-signed top cluster mode".
5. **Plan for a rigorous strong-coupling theorem (J ≥ J₁, uniform in n)** (§5): the invariant-sector transfer operator T = K^{1/2}VK^{1/2} of STRIPW §1, made semiclassical; a harmonic block (vacuum, (1,1), (1,2), (2,2)) with Schur-complement bounds; one-signed (1,1) amplitudes; short distances from the explicit c₂ + c₃/J expansion with Laplace-method remainders; end columns through the boundary vector b.

6. **One 4-state block for all couplings [numerical, §7].** The top of the SO(4)-invariant transfer spectrum has the same structure at every J from 0.5 to 16: vacuum, then three states with flip parities even, odd, even, then a gap (s4/s3 ≤ 0.55, maximum near J ≈ 3.5). At weak J these are STRIPW's three level-1 bond states; at strong J the harmonic singlets (1,1), (1,2), (2,2).
   - Channel products: (1,1) and (2,2) are positive for all 25 edge-class pairs, h included (A_h/A_t ≈ 1/J). The odd channel (1,2) vanishes on h, is positive for same-side pairs and negative only for opposite-side pairs (t–bb, t–b, a–bb, a–b).
   - For those, at harmonic order the three channels add up to the square (N−1)(T₁+T₂)²/2. Geometric convexity and amplitude AM–GM, the strong-coupling analogues of STRIPW's top–bottom criterion, hold from J ≈ 3 with margins ≈ 0.15/J. Below J ≈ 2.5 they fail and only arithmetic convexity (the Bernoulli form) survives.
7. **What the theorem must control [plan, §8].** (i) The block location to O(1/J). (ii) One-signed (1,1) and (2,2) amplitudes, with A_h(1,1) at its leading order 1/J. (iii) The exact 1/J coefficients of the two opposite-side margins. (iv) The complement. (v) Short offsets via c₂ + c₃/J, the diagonal verticals being binding.
   - The adjacent h–h pairs (c₃ < 0) are covered by G2WOLFF Theorem 1 (shared vertex, proved). Their exact J²Cov is positive at J = 0.01–20.
   - Middle-row large-distance pairs are channel-wise positive and need only (ii) and (iv).
8. **Round 2 (§9): the hard step becomes scalar integrals.**
   - **Lemma 9.2 [proved by the author, standard pinching inequality; independent review pending]:** for any trial block, ‖QTQ‖^p ≤ tr_ℋT^p − tr(PTP)^p, and ‖QTP‖²_HS = tr PT²P − tr(PTP)². So STRIPW §4.3–§6 run on explicit integrals (traces of (KV)^p, matrix elements of K^{1/2}φ trial functions), and no uniform operator bound on T − T_harm is needed.
   - Numerically the complement stays ≤ 0.71λ₃ at every J tested.
   - The convexity margins are not needed. The only inputs that must be sharp at order 1/J are κ_h = +0.8456 (the middle-row (1,1) amplitude, exact) and three short-offset opposite-side configurations, binding (a_j, b_{j+1}) with cancellation ρ = 0.0123.
   - Exact first-order energies: J·δE = −0.3456, −0.4406, −0.7095, and J·δ_λ → 0.1740.
   - J₁ ≈ 20–40 is realistic if the Laplace remainders are within 10–30× of their true sizes.
   - the long-strip data close item (2) and show item (3)'s crossover at the predicted offsets.

## 1. Formulas [proved | G2WOLFF §6; elementary]
- **Expansion (G2WOLFF Prop. 6.1, rooted at an endpoint of e):** Cov(q_a·q_b, q_u·q_v) = (n/2)(G_bu − G_bv)²/J² + c₃/J³ + O(J⁻⁴), with n = N − 1 and G the Dirichlet Green function rooted at a.
  - With unit conductances, G_bu − G_bv = −T(e,f), the transfer current. T(e,f) = L⁺[u,x] − L⁺[u,y] − L⁺[v,x] + L⁺[v,y] for e = xy, f = uv.
  - So c₂ = (N−1)T²/2. T is symmetric, and equal for edges in series (the corner verticals a₀, b₀ and their horizontals), consistent with the shared labels of the strip engine.
- **Mode form (bulk).** A dipole across e splits into transverse modes k with weights from the P₃ eigenvectors. Each mode propagates as a 1D massive chain, e^{−κ_k|m|}/(2 sinh κ_k), with cosh κ_k = 1 + λ_k/2.
  - Mode 1 is antisymmetric (1, 0, −1)/√2: zero on the middle row, odd under the top–bottom flip.
  - Mode 2, (1, −2, 1)/√6, is even. The zero mode carries no current between distinct cuts.
- c₃: G2WOLFF's cumulant formula (Gaussian moments of quadratic and quartic forms), coded in their g2sw.py. I use a snapshot of its core (b5d82cfe), applied to the rooted P₃ × P_n.

## 2. Harmonic tables [computed exactly] (scripts/harmonic.py; scratch/harmonic_n41.txt; P₃ × P₄₁, e at column 16)
Values of T(e,f) at offset m (horizontals: cut index; verticals: column index); c₂ = (N−1)T²/2.

| e \ f | m = 0 | 1 | 2 | 3 | 4 | asymptotic ratio |
|---|---|---|---|---|---|---|
| t, t | — | −0.1082 | −0.0374 | −0.0135 | −0.0050 | 0.38 (κ₁) |
| t, h | +0.2182 | +0.0455 | +0.0095 | +0.0020 | +0.00041 | 0.2087 (κ₂) |
| t, bb | +0.1145 | +0.0626 | +0.0279 | +0.0115 | +0.0046 | 0.38 |
| t, a | +0.2245 | −0.2245 | −0.0708 | −0.0239 | −0.0085 | 0.38 |
| t, b | +0.0519 | −0.0519 | −0.0348 | −0.0164 | −0.0069 | 0.38 |
| h, h | — | −0.0911 | −0.0190 | −0.0040 | −0.00083 | 0.2087 |
| h, a | −0.1727 | +0.1727 | +0.0360 | +0.0075 | +0.0016 | 0.2087 |
| a, a | — | +0.1537 | +0.0469 | +0.0154 | +0.0054 | 0.38 |
| **a, b** | −0.1037 | **+0.0171** | +0.0184 | +0.0095 | +0.0041 | 0.38 |

- End columns change the amplitudes but not the rates (e.g. T(t₀, t_m) = −0.0947, −0.0324, −0.0116 for m = 1, 2, 3). No dips beyond (a, b).
- Sum rule check: Σ_e T(e,e) = V − 1 = 122 to 10⁻⁶; T(e,e) = R_e = P(e ∈ UST).

## 3. The next order and the kill tests [numerical] (scripts/sw3.py; scratch/sw3_N4.txt, sw3_N4_n12_16.txt, sw3_N3_n12.txt)

| pair (bulk, n = 16) | c₂ (N = 4) | c₃ (N = 4) | c₃/c₂ |
|---|---|---|---|
| (a₆, b₇) diagonal verticals | 4.38·10⁻⁴ | +6.45·10⁻³ | +14.7 |
| (t₆, t₇) | 1.756·10⁻² | +1.92·10⁻³ | +0.11 |
| (t₆, t₁₀), m = 4 | 3.70·10⁻⁵ | +4.30·10⁻⁵ | +1.16 |
| (t₆, h₇) | 3.11·10⁻³ | +9.67·10⁻³ | +3.1 |
| (t₆, h₁₀), m = 4 | 2.57·10⁻⁷ | +2.93·10⁻⁵ | +114 |
| (h₆, h₇), adjacent | 1.245·10⁻² | −1.36·10⁻³ | −0.11 |
| (h₆, h₁₀), m = 4 | 1.03·10⁻⁶ | +2.08·10⁻⁶ | +2.0 |

- N = 3, n = 12: all 62 coefficients c₃ are positive; (a₄, b₅) has c₂ = 2.93·10⁻⁴ and c₃ = +2.68·10⁻³.
- The growth of c₃/c₂ with m for middle-row pairs is the rate mismatch: 2κ₁ for c₃ against 2κ₂ for c₂.

## 4. Exact O(4) check at J = 10, 20 [numerical] (scripts/exact_vs_sw.py; scratch/exact_vs_sw_n4_J10.txt, exact_vs_sw_n4_J20.txt, exact_vs_sw_n7_J10.txt)
- Method: Cov(E_e,E_f) = Cov_p(r(ℓ_e), r(ℓ_f)) from the bivariate label laws of the strip engine (snapshots 0f8b36da, a63dbc27), for pinned e in the classes t₀, t₁, h₀, h₁, a₁ and all f.
- P₃ × P₄, ratio exact/(c₂ + c₃/J): at J = 10, 1.0010 (t₁, bb₁) to 1.0987 (t₀, h₂); at J = 20, 1.0003 to 1.0306 (the same pairs). Examples at J = 20, as J²Cov exact against c₂ + c₃/J: (t₀, a₁) 0.062558 vs 0.062502; (t₀, h₂) 1.7814·10⁻⁴ vs 1.7285·10⁻⁴; (a₁, b₂) 1.3567·10⁻³ vs 1.3312·10⁻³.
- P₃ × P₇ at J = 10: 135 pairs, all positive. The (1,1) channel takes over at larger offsets: J²Cov(t₀, h_m) = 2.46·10⁻⁵, 3.08·10⁻⁶, 4.56·10⁻⁷ (m = 3, 4, 5), ratio 0.125 and then 0.148, against c₂ = 5.4·10⁻⁶, 2.3·10⁻⁷, 9.4·10⁻⁹.

## 5. Plan for a rigorous strong-coupling theorem (J ≥ J₁, every n) [plan]
- **(a) Frame.** STRIPW §1 verbatim: the SO(N)-invariant column space ℋ, T = K^{1/2}VK^{1/2} positive and trace class, Z = ⟨b, T^{n−2}b⟩, and Cov·Z² as a 2×2 minor. This frame does not depend on J.
- **(b) Semiclassical block.** In the invariant sector use the relative coordinates (Gram entries). At large J, T is close to the harmonic transfer operator e^{−H}, where H is the Hamiltonian of two (N−1)-dimensional oscillators (modes 1, 2) restricted to SO(N−1)-singlets.
  - The block is P = span{vacuum, (1,1), (2,2), (1,2)}, with eigenvalue ratios e^{−2κ₁}, e^{−2κ₂}, e^{−(κ₁+κ₂)}. The complement starts at four phonons, e^{−min(4κ₁, …)} ≤ e^{−3.85}.
  - The needed input is ‖T − T_harm‖ = O(J^{−1/2}) in a weighted norm on the relevant sector, or O(J⁻¹) after symmetrization. This is a Laplace-method bound for a kernel integral over (S^{N−1})⁶ near the diagonal, with explicit constants. It replaces the §4 scalar and level bounds.
- **(c) Schur complement and inertia** exactly as STRIPW §4.3: locate the top invariant eigenvalues within O(J^{−1/2}) of their harmonic values, uniformly in n.
- **(d) One-signed (1,1) amplitudes.** A_e = ⟨0|Ê_e|(1,1)⟩ is −(1/2)(mode-1 gradient component of e)² < 0 for t, bb, a, b, and O(1/J) for h, with a sign that must be computed. The c₃ data say it is negative. Then the (1,1) channel contributes A_eA_f·e^{−E₁₁m} > 0 to every pair.
- **(e) Short and medium distances (m ≤ m₀(J)).** Use the explicit expansion J²Cov = c₂ + c₃/J + R with a rigorous bound on R. Only finitely many pair types and offsets occur, by translation invariance and the end-column classes. All c₂ + c₃/J values are positive and computable in closed form from L⁺.
  - The binding case is the diagonal-vertical pair (c₂ = 4.4·10⁻⁴, c₃ = 6.45·10⁻³).
- **(f) End columns** through the boundary vector b, as in STRIPW. The end tables of §2 show no new zeros.
- **Main difficulty:** explicit semiclassical remainder bounds (b) uniform in the column state, including the frame rotation between columns (zero mode). In the invariant sector it enters only through O(1/J) couplings of relative modes to the inter-column twist. Expected J₁: O(10–100), to be matched against a certified middle range.
- **Alternative route for (b)–(c): a massive-mode cluster expansion** [plan]. In spin-wave variables the relative modes 1 and 2 have a J-independent gap (κ₁ ≥ 0.96 per column), and the anharmonic terms are O(1/J).
  - Integrating out the massive modes is then a convergent cluster (polymer) expansion in 1/J, with exponentially decaying clusters, uniform in n by translation invariance and locality.
  - What remains is the zero mode, the column frame doing a random walk on S^{N−1}. That walk is exactly solvable, and invariant observables couple to it only at O(1/J).
  - This is the standard large-β spin-wave technology on a quasi-one-dimensional strip, and it would give the expansion c₂ + c₃/J + … with remainders uniform in n and m, including the (1,1)-dominated large-m regime.
- **Consistency with the label picture (WIRE §4.7).** At strong coupling the label law approaches the norms of a Gaussian divergence-free ℝ³-flow, whose cross-covariance on e ≠ f is −s²T(e,f), with T the transfer current (the projection onto the cut space). Wick then gives Cov(|L_e|², |L_f|²) ∝ T², the same c₂. The label-space PQD at strong coupling is the Gaussian correlation inequality for that flow.


## 7. The invariant transfer operator across J: one 4-state block for all couplings [numerical] (scripts/spec.py, amps.py, amps2.py; scratch/spec_J*.txt, amps_J*.txt, amps2_J*.txt)
- **Method.** Take the interior column step of the engine (snapshot), F → half2(half1(legw(F, w), W_a), W_b), on admissible cut states F(t, h, bb). Its spectrum is that of the symmetric invariant T (STRIPW §1.1).
  - Top eigenvalues come from ARPACK on the black-box step. Amplitudes come from dense left and right eigenvectors (dimension 616–932) and the five insertion operators (leg weight × r(ℓ)).
  - Labels L against L − 2 agree to all printed digits at J = 8 (16/18) and J = 16 (20/22).
- **Spectrum** (ratios λ_s/λ₀; parity under the top–bottom flip):

| J | s=1 (e) | s=2 (o) | s=3 (e) | s=4 (e) | s4/s3 | δ_λ = 1 − z²/(xy) | (x+y)/2 − z |
|---|---|---|---|---|---|---|---|
| 0.5 | 0.01764 | 0.01482 | 0.01244 | 0.00017 | 0.014 | −0.0002 | +0.0002 |
| 1 | 0.0698 | 0.0501 | 0.0358 | 0.0026 | 0.073 | −0.0034 | +0.0027 |
| 2 | 0.1646 | 0.0990 | 0.0587 | 0.0212 | 0.360 | −0.0135 | +0.0127 |
| 3 | 0.1678 | 0.0965 | 0.0559 | 0.0301 | 0.539 | +0.0076 | +0.0154 |
| 4 | 0.1613 | 0.0911 | 0.0525 | 0.0285 | 0.543 | +0.0186 | +0.0157 |
| 8 | 0.1528 | 0.0846 | 0.0477 | 0.0245 | 0.514 | +0.0169 | +0.0156 |
| 16 | 0.1492 | 0.0820 | 0.0456 | 0.0228 | 0.501 | +0.0098 | +0.0153 |
| ∞ (harmonic) | 0.1459 | 0.0797 | 0.0436 | 0.0213 | 0.488 | 0 | +0.0151 |

  Here x, z, y are the s = 1, 2, 3 ratios.
  - **The same three states run through all J.** At weak J they are the level-1 bond states (⟨t+h+bb⟩ ≈ 2); at strong J they are the harmonic singlets (1,1), (1,2), (2,2). STRIPW's 4-state block and the harmonic block are the same spectral subspace.
  - The gap to the rest never closes: s4/s3 ≤ 0.55 at every J tested (maximum near J ≈ 3.5).
  - Deviation from harmonic: s1/0.1459 − 1 ≈ 0.38/J for J ≥ 4.
- **Channel products P_ef(s) = A_e(s)A_f(s)** (the coefficient of (λ_s/λ₀)^m in Cov for a bulk pair at offset m):
  - (1,1), even: positive for all 25 edge-class pairs (t, h, bb, a, b × same) at J = 0.5, 1, 2, 4, 8. So the amplitudes are one-signed, h included. A_h/A_t = 0.81, 0.30, 0.12 at J = 2, 4, 8, i.e. ≈ 1/J.
  - (2,2), even: positive for all class pairs.
  - (1,2), odd: zero for any pair containing h (h is flip-even); positive for same-side pairs (t–t, t–a, a–a, and the bottom images); negative for **opposite-side pairs** (t–bb, t–b, a–bb, a–b).
- **Opposite-side pairs: the harmonic square and its O(1/J) margins.**
  - At harmonic order the three channels add up to the perfect square (N−1)(T₁ + T₂)²/2. In channel form, P₁₁x^m + P₁₂z^m + P₂₂y^m ≥ 0 for every m follows from geometric convexity (z ≤ √(xy)) together with amplitude AM–GM (P₁₂² ≤ 4P₁₁P₂₂); both are equalities at J = ∞.
  - Numerically both margins are positive from J ≈ 3: δ_λ above, and δ_A = 1 − P₁₂²/(4P₁₁P₂₂) = 0.013, 0.054, 0.071, 0.110 for (t,bb), (t,b), (a,bb), (a,b) at J = 4. Both margins decay like 1/J (δ_λ ≈ 0.16/J at J = 16).
  - Both margins fail at J ≤ 2.5 (e.g. δ_A(t,bb) = −0.16 at J = 2). Only arithmetic convexity, (x+y)/2 ≥ z, holds at every J; that is the form the weak-coupling Bernoulli argument uses.
- **The 1/J coefficients, and their exact (Gaussian) origin [numerical].** With E_s = −ln(λ_s/λ₀) against the harmonic values 2κ₁, κ₁ + κ₂, 2κ₂:

| J | J·δE₁₁ | J·δE₁₂ | J·δE₂₂ | J·δ_λ |
|---|---|---|---|---|
| 12 | −0.359 | −0.464 | −0.722 | 0.150 |
| 16 | −0.355 | −0.459 | −0.718 | 0.157 |
| 24 | −0.352 | −0.452 | −0.716 | 0.162 |
| 32 | −0.351 | −0.449 | −0.714 | 0.166 |

  (J = 24: labels 22 and 24 agree to all digits.)
  - Limits: δE₁₁ ≈ −0.35/J, δE₁₂ ≈ −0.445/J, δE₂₂ ≈ −0.71/J, and J·δ_λ → about 0.17–0.18.
  - **Additive one-phonon shifts cancel in δ_λ ≈ 2δE₁₂ − δE₁₁ − δE₂₂**, so δ_λ > 0 is a genuine phonon–phonon interaction effect: the mixed pair (1,2) is less bound than the mean of (1,1) and (2,2).
  - These coefficients are already contained in G2WOLFF's cumulant expansion (§3). At large m, c₃/c₂ grows linearly in m with slope −J·δE.
    - The slope for (t_j, t_{j+m}) on P₃ × P₁₆ is 0.367, 0.346, 0.340 per column, against −J·δE₁₁ = 0.35.
    - The slope for (h_j, h_{j+m}) is 0.709, 0.710, against −J·δE₂₂ = 0.71.
  - So the first-order quantities the theorem needs (§8 (i)–(iii)) are explicit Gaussian cumulant expressions, traces of products of lattice Green functions of P₃ × ℤ, computable exactly.
- **Amplitude AM–GM at J = 8** (labels 16): δ_A = 0.026 (t,bb), 0.037 (t,b), 0.053 (a,bb), 0.063 (a,b), all positive. The J = 16 dense run exceeded the 10-minute job limit; a Krylov version is needed there.

## 8. What the strong-coupling theorem must control (answers to the items 1–3) [plan, with the numerical facts above]
- **(1) The harmonic block closes structurally from J ≈ 3.** From J ≈ 3 upward the ordering, the parities, the gap to the complement (factor ≥ 1.8) and both opposite-side margins (δ_λ, δ_A > 0) all hold. A rigorous J₁ is set by the constants of the semiclassical remainder:
  - (i) **block location:** the top four invariant eigenvalues to O(1/J), with an explicit constant. The numerics give s1 = e^{−2κ₁}(1 + 0.38/J + …).
  - (ii) **one-signed amplitudes:** A_e(1,1), A_e(2,2) of every edge type have one sign, with A_h(1,1) = κ_h A_t(1,1)/J + O(J⁻²) and κ_h > 0 (numerically κ_h ≈ 0.9–1.2).
  - (iii) **opposite-side margins:** the 1/J coefficients of δ_λ and δ_A must be computed exactly and the O(J⁻²) remainders bounded. These are the strong-coupling analogues of STRIPW's λ₂ + λ₄ ≥ 2λ₃ and p₂ ≥ p₄. Numerically J·δ_λ → about 0.17 (a two-phonon interaction energy, §7); they are Gaussian cumulant expressions.
  - (iv) **the complement:** contributions bounded by C·(λ₄/λ₀)^m, with complement amplitudes O(1/J) relative to the block.
  - (v) **short offsets** m ≤ m₀ through the explicit expansion c₂ + c₃/J. The binding case is the diagonal-vertical pair, where c₂ = 4.4·10⁻⁴ is small and c₃ > 0 must be used exactly.
  - All of (i)–(iii) are second-order perturbation theory of two (N−1)-dimensional oscillators by the quartic terms of G2WOLFF §6 (V and the observables), plus tail bounds of order e^{−cJ}.
  - Estimate: if the remainder constant is C, the margins ≈ 0.15/J beat C/J² once J ≳ 7C. With C ≈ 10 this gives J₁ of order 10², to be matched by a certified middle range.
- **(2) Adjacent middle-row pairs (h_j, h_{j+1}), the four c₃ < 0 cases: positive at every J [proved + numerical].**
  - They share a vertex, so G2WOLFF Theorem 1 (pairs sharing a vertex, N = 3, 4, any graph, any J ≥ 0) covers them; it is proved there.
  - Exact check (scripts/adj_hh.py, P₃ × P₆, bulk and end, labels L and L − 2 identical): J²Cov > 0 at J = 0.01, 0.1, 0.3, 1, 2, 4, 8, and at J = 10, 20 from §4.
  - c₂ + c₃/J is negative only for J ≲ 0.15, where the true value is weak-coupling small and positive; from J = 2 it is accurate to 1–5%. The long-strip data have not arrived yet.
- **(3) The middle-row large-distance regime.** For any pair containing a middle-row edge h, the odd channel is absent (P(1,2) = 0 by the flip), so
  Cov(e, h at offset m) = P(1,1)(λ₁₁/λ₀)^m + P(2,2)(λ₂₂/λ₀)^m + R(m),
  with both block terms ≥ 0 by one-signedness.
  - At harmonic order P(1,1) = 0 (mode 1 vanishes on the middle row). P(1,1) = A_eA_h is O(J⁻¹) relative for (t, h) and O(J⁻²) for (h, h), while P(2,2) is O(1).
  - The (1,1) term takes over at m ≳ log(J)/(2(κ₂ − κ₁)) for (t, h), and at twice that for (h, h). That is the "1/J³ term dominates" regime of §0.
  - **What the theorem must control there:**
    - (a) the sign of A_h(1,1) at its leading order 1/J, the one-signedness in (ii);
    - (b) |R(m)| ≤ P(1,1)(λ₁₁/λ₀)^m + P(2,2)(λ₂₂/λ₀)^m. The complement decays faster (ratio ≤ 0.55 against the block), and its amplitudes on E_h are O(1/J²).
  - No cancellation is involved: middle-row pairs, like same-side pairs, are channel-wise positive. Only opposite-side pairs need the convexity margins (iii).

## 9. The hard step reduced to scalar integrals; exact first-order data; J₁ (interim v3: the round-2 items 1–3)

### 9.1 Answer first
- **No uniform operator bound on T − T_harm is needed.** Lemma 9.2 (two-line proof by the author; standard; review pending) controls the complement of any trial block by traces. Then every input of STRIPW §4.3–§6 is a finite list of explicit scalar integrals:
  - μ_k, the eigenvalues of the compression PTP;
  - τ_∞, the norm of the complement, bounded by tr_ℋ(T^p) − tr(PTP)^p;
  - c, the off-diagonal coupling, bounded by its Hilbert–Schmidt norm;
  - the amplitudes and ‖Q₅ũ‖.
  - So "explicit semiclassical bounds" means explicit Laplace bounds, to second order, for tr_ℋ(T^p) (p = 2 or 3) and for Gram, T- and T²-matrix elements of explicit trial functions and insertion vectors (§9.2, list (I1)–(I3)).
- **The trace bound has room at every J tested.** With the exact top-4 eigenvectors as trial space, (Σ_{j≥4}λ_j²)^{1/2}/λ₃ = 0.12, 0.51, 0.71, 0.65, 0.635, 0.628 at J = 1, 2, 4, 8, 12, 16, and 0.61 in the harmonic limit. With p = 3 the ratios are 0.095, 0.42, 0.60, 0.555, 0.543, 0.538 (§9.3). So the complement sits below the block with at least 29% to spare for trial-state errors.
- **The convexity margins δ_λ, δ_A of §7–§8 are not needed** (§9.5).
  - For opposite-side pairs the harmonic channel sum is a perfect square. Its cancellation against the sum of absolute channel terms is small only at four short-offset configurations; the binding one is the diagonal-vertical pair (a_j, b_{j+1}), with ρ = 0.0123.
  - From time-offset 2 on, (1,1) dominance holds with O(1) room, so O(1/J)-accurate block data suffice there.
  - **Only two inputs must be sharp at order 1/J:** the sign of A_h(1,1), and the finitely many short-offset configurations, through c₂ + c₃/J with a second-order remainder.
- **Exact first-order data** (G2WOLFF cumulant expansion, symmetry-reduced fits; §9.4):
  - J·δE₁₁ → −0.34556, J·δE₁₂ → −0.44055, J·δE₂₂ → −0.7095, so J·δ_λ → +0.1740;
  - **κ_h = lim J·A_h(1,1)/A_t(1,1) = +0.8456**, so the middle-row (1,1) amplitude has the same sign as all the others at leading order.
- **J₁ [estimate].** With the first-order terms exact, the binding pair needs 0.0123J² + 0.181J ≥ K. Here K is the rigorous second-order remainder constant, in units of the absolute channel sum.
  - The true size is K ≈ 1 (exact J = 10 data), which gives J ≈ 4.3. K = 10 gives J₁ ≈ 22, and K = 100 gives J₁ ≈ 83.
  - The trace budget is not binding for J ≳ 10 (§9.6).
  - **Realistic target: J₁ ≈ 20–40**, to be met by the certified middle range. Lemma 9.2 serves that range as well: with label-truncated trial spaces the only analytic input is a tail bound on Σ T(s,s′)².
- **Item (2) is closed with the long-strip data, and item (3)'s crossover is visible in it at the predicted offsets** (§9.7).

### 9.2 Lemma 9.2 (trace control of the complement) [proved by the author: the pinching inequality plus convexity of tr A^p, standard; independent review pending]
Let P project onto any finite-dimensional subspace of ℋ, Q = 1 − P, T_d = PTP, T_∞ = QTQ, C = QTP. Then for every p ≥ 1:
- (a) ‖T_∞‖^p ≤ tr_ℋ(T^p) − tr(T_d^p);
- (b) ‖C‖² ≤ ‖C‖²_HS = tr(PT²P) − tr(T_d²).

*Proof.*
- (a) U = P − Q is unitary, and T_d + T_∞ = (T + UTU*)/2. A ↦ tr(A^p) is convex on positive trace-class operators for p ≥ 1, so tr(T_d^p) + tr(T_∞^p) = tr((T_d+T_∞)^p) ≤ tr(T^p). Finally ‖T_∞‖^p ≤ tr(T_∞^p), since T_∞ ≥ 0.
- (b) tr(PT²P) = tr(PTPTP) + tr(PTQTP) = tr(T_d²) + ‖C‖²_HS. ∎

**Use.** STRIPW Lemmas 4.3–4.4 then apply verbatim, with τ_∞ := (tr_ℋT^p − tr T_d^p)^{1/p} and c := ‖C‖_HS (and c_k := ‖CP_k‖_HS).

**The inputs are explicit integrals once trial functions are taken of the form ψ = K^{1/2}φ, with φ explicit** (as STRIPW's b = K^{1/2}V1):
- (I1) tr_ℋ(T^p) = tr_ℋ((KV)^p) = ∫_{SO(4)}dg ∫Π_{i≤p}dσ⁽ⁱ⁾ V(σ⁽ⁱ⁾)K(σ⁽ⁱ⁾,σ⁽ⁱ⁺¹⁾), with σ⁽ᵖ⁺¹⁾ = gσ⁽¹⁾ and K the product of von Mises kernels. No square root of K occurs.
- (I2) ⟨ψ_i,ψ_j⟩ = ⟨φ_i,Kφ_j⟩, ⟨ψ_i,Tψ_j⟩ = ⟨Kφ_i,VKφ_j⟩, ⟨ψ_i,T²ψ_j⟩ = ⟨Kφ_i,VKVKφ_j⟩.
- (I3) Insertions: R_τK is the kernel ∂_J e^{Jσ_τ·σ′_τ} on row τ (R_τ commutes with K), and T_X = K^{1/2}XVK^{1/2}. So every amplitude and every ‖Q₅ũ‖-type quantity is of type (I2).
- Natural trial functions: φ = harmonic two-phonon singlets in the relative coordinates (modes 1, 2), with their first-order corrections. Laplace expansion of (I1)–(I3) around the aligned set, with the SO(4) orbit integrated exactly, is the remaining analytic work; it is finite and mechanical, but long.

### 9.3 Numbers for Lemma 9.2 on the exact operator [numerical] (scripts/trace_sep.py; scratch/trace_sep_a.txt)
Trial space = exact top-4 eigenvectors (best case); S_p = Σ_{j≥4}(λ_j/λ₀)^p.

| J | labels | λ₁…λ₄ / λ₀ | tr T²/λ₀² | S₂^{1/2}/(λ₃/λ₀) | S₃^{1/3}/(λ₃/λ₀) |
|---|---|---|---|---|---|
| 1 | 10 | 0.06975, 0.05007, 0.03582, 0.00263 | 1.00867 | 0.121 | 0.095 |
| 2 | 12 | 0.16456, 0.09895, 0.05871, 0.02116 | 1.04121 | 0.508 | 0.419 |
| 4 | 12 (= 10) | 0.16125, 0.09112, 0.05246, 0.02847 | 1.03845 | 0.711 | 0.597 |
| 8 | 14 | 0.15277, 0.08465, 0.04771, 0.02452 | 1.03374 | 0.651 | 0.555 |
| 12 | 16 | 0.15034, 0.08287, 0.04626, 0.02336 | 1.03247 | 0.635 | 0.543 |
| 16 | 16 | 0.14918, 0.08204, 0.04556, 0.02282 | 1.03188 | 0.628 | 0.538 |
| ∞ | harmonic | 0.14590, 0.07966, 0.04356, 0.02129 | 1.03025 | 0.61 | — |

(J = 12, 16: scratch/trace_sep_b.txt. At J = 16 the 16-label spectrum agrees with §7's 20/22-label values to the printed digits.)

- **Harmonic limit, exact.** The SO(N−1)-invariants of the two relative modes are generated freely by |π₁|², π₁·π₂, |π₂|² (N = 3, 4). Hence Σ_s(λ_s/λ₀)^p = 1/((1−x^p)(1−z^p)(1−y^p)), with x = e^{−2κ₁}, z = e^{−κ₁−κ₂}, y = e^{−2κ₂}.
- **Trace budget.** τ_∞ < μ₃ requires errors in tr T² (from above) and in Σ_{k<4}μ_k² (from below) totalling less than μ₃² − S₂. That is 1.36·10⁻³λ₀² at J = 4, 1.32·10⁻³ at J = 8, 1.28·10⁻³ at J = 12, 1.26·10⁻³ at J = 16 and 1.2·10⁻³ at J = ∞.
- **The trace is smooth in 1/J.** J(tr T²/λ₀² − 1.03025) = 0.033, 0.028, 0.0267, 0.0261 at J = 4, 8, 12, 16, so the first-order coefficient is ≈ 0.024 and the second-order one ≈ 0.03–0.04.

### 9.4 Exact first-order data [numerical: exact cumulant coefficients, fitted] (scripts/fit_eps2.py; scratch/fit_eps2_n30_m2_7.txt, P₃ × P₃₀, offsets 2–7)
- **Form.** In the bulk, c₂(m) = Σ_s p_s e^{−E_s m} and c₃(m) = Σ_s (q_s − p_s ε_s m)e^{−E_s m}, with ε_s = lim J·δE_s.
- **Symmetry reduction, so each ε_s is a 2-parameter fit:**
  - (h,h) carries only (2,2) at orders J⁻², J⁻³ (mode 1 vanishes on the middle row, and (1,2) is flip-odd);
  - (t,t) − (t,bb) and (a,a) − (a,b) carry only the odd channel (1,2).
  - (A first unreduced 6-parameter fit, scratch/fit_eps_n30.txt, was ill-conditioned for ε₁₂, ε₂₂ and is superseded.)
- **Results:**
  - ε₁₁ = −0.345557: (t,t)+(t,bb) and (a,a)+(a,b) agree to 6 digits;
  - ε₁₂ = −0.44055: −0.440554 and −0.440544;
  - ε₂₂ = −0.7095 ± 0.0002: five combinations;
  - **J·δ_λ → 2ε₁₂ − ε₁₁ − ε₂₂ = +0.1740.**
  - The spectrum at J = 32 (§7) gives −0.351, −0.449, −0.714 and 0.166; the differences are O(J⁻²).
- **Middle-row amplitude.** P_th(1,1) = q₁₁(t,h)/J³ + …, so **κ_h = q₁₁(t,h)/p₁₁(t,t) = +0.8456**.
  - Consistency: (a,h) gives 0.3230 = κ_h·e^{−κ₁}, because a vertical edge sits half a column from a horizontal one.
  - Against §7: A_h/A_t = 0.81, 0.30, 0.12 at J = 2, 4, 8, versus κ_h/J = 0.42, 0.21, 0.106. The second-order term is positive, ≈ +1·A_t/J².
- **Closed forms (harmonic).**
  - Top row: T(t_j, t_{j+m}) = ±(α₁e^{−κ₁m} + α₂e^{−κ₂m}), with α₁ = 1/(4 sinh κ₁) = 1/(2√5) and α₂ = 1/(4 sinh κ₂) = 1/(2√21).
  - Middle row: T(h_j, h_{j+m}) = ±(2/√21)e^{−κ₂m}.
  - Hence p₁₁ = 3/40, p₂₂(t,t) = 1/56, p₂₂(h,h) = 2/7.
  - General rule: mode k contributes ψ_k(row)²λ_k e^{−κ_k m}/(2 sinh κ_k), because the second difference of e^{−κ|m|}/(2 sinh κ) is λ_k times itself for m ≥ 1.

### 9.5 Which inputs must be sharp at order 1/J (the offset split) [sketch: the reduction is STRIPW §4.4 plus the exact harmonic channel data; the error budget is not yet written]
- Channel form (STRIPW §4.4): Cov·N² = Σ_{l≥2}(λ_l/λ₁)^m â_lb̂_l + R_CE.
- **Same-side and middle-row pairs.** Every block channel is ≥ 0 by one-signedness. So O(1)-accurate block data, plus the complement bound of Lemma 9.2, suffice at every offset.
  - The exception is the sign of A_h(1,1), which vanishes at harmonic order: κ_h = +0.8456 must be certified together with its O(J⁻²) remainder.
- **Opposite-side pairs.** The harmonic channel sum is 1.5α₁²x^m(1 − u)², with u = r·s^m and s = e^{−(κ₂−κ₁)} = 0.5464. Its cancellation against the absolute channel sum is ρ = ((1−u)/(1+u))².
  - Configurations are counted by time-offset (vertical edges sit at integer times, horizontal ones at half-integers). Mirror and flip reduce them to the following list:

| configuration | u | ρ |
|---|---|---|
| (a_j, b_{j+1}) (diagonal verticals) | 0.800 | 0.0123 |
| (t_j, b_{j+1}) ≅ (a_j, bb_j) | 0.625 | 0.054 |
| (t_j, bb_j) (same cut) | 0.488 | 0.118 |
| (a_j, b_{j+2}) | 0.437 | 0.153 |
| all others | ≤ 0.34 | ≥ 0.24 |

  - (a_j, b_j) shares a vertex (G2WOLFF Theorem 1).
  - With ρ ≥ 0.15, relative errors of a few percent in the block data are harmless. The geometric-convexity route (δ_λ, δ_A > 0) is a sufficient alternative, but it is not needed.
- **Hence the sharp inputs are:**
  - (a) κ_h with its remainder;
  - (b) the first three configurations of the table, plus STRIPW §7's same-position pairs, through the exact c₂ + c₃/J.
  - c₃ for the infinite strip is a lattice sum of Green-function products with exponential decay, so it is rigorously computable.

### 9.6 J₁ [estimate]
- **Binding pair (a_j, b_{j+1}):** c₂ = 4.39·10⁻⁴, c₃/c₂ = 14.7, ρ = 0.0123, absolute channel sum 0.0355.
  - The exact J²Cov at J = 10 (1.45·10⁻³, §4) gives c₄ ≈ +0.036 ≈ 1.0 × the absolute sum.
  - With a rigorous remainder |R| ≤ K·(absolute sum)/J², positivity needs 0.0123J² + 0.181J ≥ K. K = 1 gives J ≥ 4.3, K = 10 gives J ≥ 22, K = 100 gives J ≥ 83.
- **κ_h:** the true second-order coefficient is ≈ +1 (in units of A_t), so a rigorous constant K_h needs J > K_h/0.8456.
- **Trace budget (§9.3):** about 5·10⁻⁴λ₀² each for tr T² and for the Ritz sum. The true second-order coefficient of tr T²/λ₀² is ≈ 0.04, and with first-order-corrected trial functions the Ritz deficit is O(J⁻⁴). So this is not binding for J ≳ 10.
- **Conclusion: J₁ ≈ 20–40 if the Laplace remainders are within a factor 10–30 of their true sizes.** A plain harmonic trial space, with no first-order corrections, would give J₁ ≈ 80K′ with K′ = O(1). So the first-order corrections should be built into the trial functions.

### 9.7 Items (2) and (3) against the long-strip data [numerical] (UNIF ca0547bb §9.11; files /mnt/g2/release/root/data/e17/unif/scratch/out/g2long_P3n*_pairs.txt, read-only)
- **(2) Adjacent middle-row pairs (h_j, h_{j+1}), the only c₃ < 0 cases.**
  - Positive at J = 5, 10, 20 for n = 6, 8, 12 and every position, with Cov/rounding bound ≥ 4·10¹³.
  - Bulk J²Cov = 0.012391, 0.012349, 0.012386 at J = 5, 10, 20, against c₂ + c₃/J = 0.012173, 0.012310, 0.012378 (c₂ = 0.012446, c₃ = −0.001365). The ratios are 1.018, 1.003, 1.0007, so the next term is positive, c₄ ≈ +3–5·10⁻³.
  - End pair (h₀,h₁): 0.011360, 0.011276, 0.011315, against 0.011053, 0.011219, 0.011302.
  - With G2WOLFF Theorem 1 (every J, proved) this closes item (2).
- **(3) Middle-row large distance.** Cov(h_j, h_{j+m}) ≈ P_hh(1,1)x^m + P_hh(2,2)y^m, with P_hh(1,1) = κ_h²p₁₁/J⁴ = 0.0536/J⁴ and P_hh(2,2) = (2/7)/J².
  - The crossover is at m* = ln(5.33J²)/(2(κ₂−κ₁)) = 4.1, 5.2, 6.3 for J = 5, 10, 20.
  - In the data the decay ratio of (h₀, h_m) moves from ≈ 0.045–0.056 (e^{−2κ₂} = 0.0436, shifted by O(1/J)) to 0.15–0.16 (e^{−2κ₁} = 0.146). It passes the midpoint 0.08 at m ≈ 4, 5.3, 7.
  - For (t,h): P_th(1,1) = 0.0634/J³ against P_th(2,2) = (1/14)/J², so m* = ln(1.126J)/1.2088 (2.6 at J = 20).
  - The smallest covariance in all of the runs (≈ 2·10⁻¹⁵, (h₀,h₁₀), n = 12, J = 20) is of the predicted bulk size 1.5·10⁻¹⁵.
  - **What the theorem must control there:**
    - the sign of κ_h, certified;
    - the complement, whose amplitudes on E_h are O(J⁻²) and whose decay is at most 0.71λ₃ < λ₁₁ by Lemma 9.2. It is then ≤ O(J⁻²)·0.49^m relative to the (2,2) term, and ≤ x^m-suppressed relative to the (1,1) term.

## 6. Files
- scripts/harmonic.py (transfer currents, all pair types, bulk and ends); scripts/sw3.py (c₂, c₃ on P₃ × P_n); scripts/g2sw_core_snapshot.py (G2WOLFF g2sw.py core, source sha8 b5d82cfe); scripts/exact_vs_sw.py with unif_strip_engine2_snapshot.py (0f8b36da) and unif_pairs2_snapshot.py (a63dbc27).
- scripts/spec.py (invariant transfer spectrum, ARPACK on the engine step), amps.py and amps2.py (dense eigenvectors, channel products, convexity margins), adj_hh.py (adjacent middle-row pairs over J).
- scripts/fit_eps.py (first, unreduced fit; superseded), fit_eps2.py (symmetry-reduced exact 1/J coefficients and κ_h), trace_sep.py (Lemma 9.2 numbers on the exact operator).
- scratch/: harmonic_n41.txt; sw3_N4.txt, sw3_N4_n12_16.txt, sw3_N3_n12.txt; exact_vs_sw_n4_J10.txt, exact_vs_sw_n4_J20.txt, exact_vs_sw_n7_J10.txt; fit_eps_n30.txt, fit_eps2_n30_m2_7.txt; trace_sep_a.txt, trace_sep_b.txt; PROGRESS.md.

## 10. Appended after review: corrections, a cross-link, and the plan for the second-order bounds (round 3)

### 10.1 Lemma 9.2 is REVIEWED; corrections from RV11_2 (/mnt/g2/release/root/code/pk20/rv11/RV11_2_NOTES.md, 4c460948)
- **Status.** RV11_2 confirms Lemma 9.2 and its use in §9. The hypotheses, all necessary: for (a), T ≥ 0 trace class, P an orthogonal projection, p ≥ 1; for (b), T = T* with PT²P trace class.
- **MINOR-1 (N = 3 only).** ℋ must be the O(3)-invariant, parity-even sector.
  - The SO(3)-invariant sector contains the triple product q_T·(q_M × q_B). Its top state sits at e^{−κ₁−κ₂} ≈ 0.080 > μ₃ ≈ 0.044, which would make τ_∞ < μ₃ impossible.
  - So at N = 3, (I1) uses the O(3) average, as the SG₃ does.
  - §9.3's "generated freely by |π₁|², π₁·π₂, |π₂|² (N = 3, 4)" holds for the stabilizers O(2) (N = 3, parity-even sector) and SO(3) (N = 4); it fails for SO(2).
  - At N = 4 there is no pseudoscalar on three spins in ℝ⁴ (a determinant needs four vectors), so the SO(4) and O(4) sectors coincide here.
- **Nit, §9.1.** Read "τ_∞ ≤ (tr_ℋ(T^p) − tr(PTP)^p)^{1/p}"; the 1/p power was missing.
- **Nit, §9.7 (3).** The factor 0.49^m is the harmonic λ₄/λ₃. What Lemma 9.2 certifies (numerically, §9.3) is τ_∞/λ₃ ≤ 0.71, so the certified suppression relative to the (2,2) term is 0.71^m.
- **Improvement at p = 2 (RV11_2).** ‖T_∞‖² ≤ tr T_∞² = tr T² − 2 tr PT²P + tr T_d². This gains 2‖C‖²_HS over (a): tr T² = tr T_d² + 2‖C‖²_HS + tr T_∞², and ‖C‖²_HS = tr PT²P − tr T_d².
  - C = 0 for the exact-eigenvector trial spaces of §9.3, so those numbers are unchanged. The gain matters for explicit trial functions.

### 10.2 Cross-link with the review (conjecture LM): c₃ at exactly balanced pairs, any graph [G2WOLFF Prop. 6.1, sketch + validation; my evaluation]
- At T(e,f) = 0, G2WOLFF §6 gives c₃ = (n/4)Σ_{xy∈E} c_xy(g_x−g_y)²[(d_x−d_y)² + (n−1)(d_x²+d_y²)] ≥ 0, with g = Ge_b, d = G(e_u−e_v), G rooted at a, and d_b = 0. It vanishes only in degenerate cases (e.g. a cut vertex, where Cov ≡ 0).
  - So the sign of c₃ at T = 0 is settled on every graph, at the level of G2WOLFF's sketch with its numerical validation (75 random balanced shapes, and a scan of ≈ 20,000 shapes).
- **Wheatstone/K₄** (e = 12, f = 34, N = 4; scripts/wheat.py, scratch/wheat.txt; the SOS formula and the cumulant core agree to all digits). Weights are (w₁₃, w₁₄, w₂₃, w₂₄, w₁₂, w₃₄):
  - uniform K₄: c₃ = 9/256;
  - without the edge 12: 9/64;
  - (1, 10, 0.1, 1, 1, 1): 0.011622;
  - (2, 1, 6, 3, 1, 1): 0.0079221;
  - (5, 0.2, 25, 1, 1, 1): 0.0027326;
  - (1, 1000, 0.001, 1, 1, 1): 1.40·10⁻⁴;
  - (1, 1, 1, 1, 1000, 1): 1.40·10⁻⁷.
  - In the normalization (K = J·C_eff(e)), q = 2C_eff³c₃/(N−1): 0.1875 for uniform K₄, and 0.09375 without the edge 12. The hexagon has q ≈ 0.32–0.33.

### 10.3 Second-order bounds: every input is a small-graph O(4) integral [derivation; plan]
- **Harmonic trial states in the frame ψ = K^{1/2}φ** (the frame of §9.2).
  - For T = K^{1/2}VK^{1/2}, the top eigenvector is K^{1/2}φ₀ with VKφ₀ = λ₀φ₀.
  - For one Gaussian mode with vertical stiffness λ_m, φ₀ = exp(−(J/2)s|π̃|²) with s² = λ_m(1+s), i.e. s = e^{κ}−1: 1.6180 (mode 1, the golden ratio) and 3.7913 (mode 2).
  - In Gram variables (|π̃₁|² ≈ 1−Z and |π̃₂|² ≈ [4(1−X) + 4(1−Y) − 2(1−Z)]/6) this reads **φ₀ ∝ e^{J(aX + aY + bZ)}**, with a = (e^{κ₂}−1)/3 = 1.2638 and b = (e^{κ₁}−1)/2 − (e^{κ₂}−1)/6 = 0.1771.
  - The excited states of VK are polynomial × φ₀. The two-phonon singlets are linear in X, Y, Z: (1,1) ∝ (1−Z) − c, (1,2) ∝ X − Y (flip-odd), (2,2) ∝ (2−X−Y) − c′.
  - **So the strong-coupling block is, to leading order, e^{J(aX+aY+bZ)}·span{1, X, Y, Z}: STRIPW's weak-coupling block span{e₀, e₁₁₀, e₁₀₁, e₀₁₁} times a Gaussian weight.** With a(J), b(J) free, this one family interpolates between the two ends. It is a candidate uniform trial space, for the certified middle range too.
- **Consequence.** With φ_i = e^{J(aX+aY+bZ)}P_i(X, Y, Z), every input of §9.2 is an O(4) partition function, with polynomial insertions of dot products, on a graph with 6–12 vertices:
  - ⟨φ_i, Kφ_j⟩: two columns;
  - ⟨Kφ_i, VKφ_j⟩: three columns;
  - ⟨Kφ_i, VKVKφ_j⟩: four columns;
  - insertions: R_τ on a horizontal bond, X or Y on a vertical bond;
  - tr_ℋ T²: the two-column cylinder with the SO(4) twist averaged.
  - The end columns carry couplings aJ (T–M, M–B) and bJ (T–B).
  - So the Laplace bounds are finite-dimensional (≤ 33 dimensions after rooting), with bounded rooted variances (no growth along a long window). G2WOLFF's cumulant machinery gives the 1/J expansions of these integrals.
- **Amplitudes lose no factor J.** Write â_l = ⟨φ_l, Oφ₀⟩ with φ_k = ψ_k + e_k (trial plus error, ψ_l ⊥ ψ₀). Then
  â_l = ⟨ψ_l, Oψ₀⟩ + ⟨(O−c)ψ_l, e₀⟩ + ⟨e_l, (O−c)ψ₀⟩ + ⟨e_l, (O−c)e₀⟩
  for any constant c, using ⟨ψ_l, e₀⟩ + ⟨e_l, ψ₀⟩ = −⟨e_l, e₀⟩.
  - ‖(O−c)ψ_k‖ = O(1/J) is an explicit integral, and ‖O−c‖ ≤ 2 enters only the doubly small last term. So with ‖e_k‖ ≤ C/J² the relative amplitude error is O(C/J²), not O(C/J). This is the strong-coupling counterpart of STRIPW §6.1's bookkeeping.
- **Where the constants can grow.** In Lemma 4.4, the (2,2) state's distance to the complement bound is only ≈ 0.013λ₀ for a 4-dimensional trial space (τ_∞ ≈ 0.7λ₃). That inflates its eigenvector constant about 75×.
  - Remedy: add the six four-phonon singlets, φ₀ × quadratic polynomials in X, Y, Z, giving dimension 10. Then τ_∞ drops to the six-phonon level (≈ 0.003λ₀), and the Ritz step absorbs the first-order mixings exactly.
- **J₁ outlook (unchanged).** Nothing so far forces J₁ above 40. The trace budget is quadratic in trial errors; κ_h and long range tolerate O(1/J²) amplitude errors; the binding pair needs relative amplitude errors ≲ 0.5%, i.e. J ≳ 22√C with C the O(J⁻²) constant of the 10-state trial space.

## 11. One explicit trial space for every J: exact Ritz tests (round 3) [numerical: exact finite-J computations with the engine]

### 11.1 Answer first
- **Trial space.** In the frame ψ = K^{1/2}φ, take φ = e^{J(aX + aY + bZ)}·P(X, Y, Z), with the harmonic constants a = 1.26376, b = 0.17713 held fixed for all J (§10.3), and P running over the monomials of degree ≤ d:
  - d = 1: 4 states, STRIPW's block times the Gaussian weight;
  - d = 2: 10 states;
  - d = 3: 20 states.
- **Exactness.** Each trial state is an exact engine Y-kernel: a triangle end column F_tri[t,h,bb] = Σ_{b,w,a} W_bW_wW_a{t h bb; b w a}², with monomials realized as J-derivatives on the triangle's bonds. The inner product is ⟨F,G⟩_w = Σ F·w_tw_hw_bb·G, for which the column step is self-adjoint and ⟨F_φ,F_φ′⟩_w = ⟨K^{1/2}φ, K^{1/2}φ′⟩.
  - Normalization checks: switching off the T–B bond gives the engine's series end; all external labels 0 give the exact triangle integral; the gluing reproduces the K₄ tetrahedral network.
- **Results, J = 0.5–16** (scripts/ritz.py, ritz2.py; scratch/ritz_J*.txt, ritz2_J*.txt). Every Ritz value is a rigorous lower bound in exact arithmetic (min–max).

| J | d = 1: τ/μ₃ | d = 1: ‖φ_k − ψ_k‖, vacuum / block | d = 2: τ/μ₃ | d = 2: vacuum / block | d = 3: vacuum / block |
|---|---|---|---|---|---|
| 0.5 | 0.026 | 7.6·10⁻⁵ / 0.77–1.1·10⁻² | ≈ 0 | 2.3·10⁻⁷ / 2.9–5.0·10⁻⁵ | 4·10⁻¹⁰ / ≤ 1.3·10⁻⁷ |
| 1 | 0.124 | 8.6·10⁻⁴ / 3.2–4.0·10⁻² | 0.003 | 8.3·10⁻⁶ / 4.6–6.6·10⁻⁴ | 4.8·10⁻⁸ / 3.8–6.0·10⁻⁶ |
| 2 | 0.537 | — | 0.054 | — | — |
| 4 | 0.719 | — | 0.146 | — | — |
| 8 | 0.652 | 1.4·10⁻³ / 1.3–2.1·10⁻² | 0.113 | 5.5·10⁻⁵ / 2.0–3.3·10⁻³ | 3.4·10⁻⁶ / 1.0–2.1·10⁻⁴ |
| 16 | 0.628 | 6.8·10⁻⁴ / 0.57–1.05·10⁻² | 0.100 | 1.2·10⁻⁵ / 0.84–1.72·10⁻³ | 1.05·10⁻⁶ / 2.3–4.6·10⁻⁵ |

  - τ/μ₃ is the improved p = 2 bound of §10.1 for the complement of the trial space, relative to the (2,2) Ritz value; block Ritz values agree with the exact ones to 10⁻⁵ (d = 2) or 10⁻⁸ (d = 3) at J = 8. Ritz test at J = 2, 4 for d ≤ 2 only (scratch/ritz_J2.txt, ritz_J4.txt).
  - "—": not run with eigenvector errors at that J.
- **Scaling with J.** For d = 1 and d = 2 the block errors fall like 1/J (≈ 0.15/J and ≈ 0.027/J): d = 2 misses the six-phonon admixture, a first-order effect. For d = 3 they fall like 1/J² (≈ 0.01/J²). At weak coupling the space contains STRIPW's block, and the errors vanish as J → 0.
- **Consequences.**
  - (i) **Block isolation holds with a large margin at every J tested.** With 10 explicit states, Lemma 9.2 puts the complement at ≤ 0.15μ₃ from J = 0.5 to 16.
  - (ii) **The binding cancellation is affordable.** (a_j, b_{j+1}) needs block eigenvectors to about 0.1–0.2% (§9.6). The 20-state space gives ≤ 0.02% for every J tested, and the 10-state space for J ≳ 27.
  - (iii) **For the certified middle range** no eigen-decomposition is needed. It suffices to have certified Gram, T- and T²-matrices of 10–20 explicit vectors, tr M² with a truncation tail bound, and J-continuity between grid points.
  - (iv) **For the analytic range J ≥ J₁** the inputs are the same matrix elements (small-graph O(4) integrals, §10.3), plus the residual functions (T − μ_k)ψ_k.
- **Numerical caveat.** The monomial basis is ill-conditioned at large J (scaled cond(B) ≈ 10¹⁴ for d = 3 at J = 16). There the trace bound and the residuals, computed by subtraction, lose precision; the eigenvector errors computed directly are unaffected. A certified version should use polynomials orthogonalized in ⟨·,·⟩_w (e.g. in the centred variables J(1−X), J(1−Y), J(1−Z)), and bound residuals as norms of the residual functions rather than by subtraction.

## 12. Second-order Laplace expansions: the vacuum Ritz value and tr_ℋ(T²), validated against the exact operator (round 3) [formal expansion, derived; numerical validation]

### 12.1 Answer first
- **Second-order expansions of the two inputs it was asked for are derived and validated.** The residuals against the exact engine values fall like J⁻³ with small coefficients.
  - The vacuum-sector integrals D = ⟨φ₀,Kφ₀⟩, N = ⟨Kφ₀,VKφ₀⟩ and N₂ = ⟨Kφ₀,VKVKφ₀⟩, with φ₀ = e^{J(aX+aY+bZ)} (scripts/lapl2.py, exact_vac.py).
  - The twisted cylinder tr_ℋ(T²) (scripts/trace2.py).
- **Vacuum Ritz value.** μ₀ = N/D satisfies 1 − μ₀/λ₀ = 4.5·10⁻⁴, 8.1·10⁻⁵, 1.8·10⁻⁵ at J = 4, 8, 16, i.e. ≈ 4.5·10⁻³/J², as second-order perturbation theory predicts for the exact harmonic ground state.
- **Trace.** tr_ℋ(T²)/μ₀² = 1.030242 + 0.0247/J + 0.031/J² + O(J⁻³).
  - The constant is exactly the harmonic Σ_s(λ_s/λ₀)² = 1/((1−x²)(1−z²)(1−y²)), reproduced to 10⁻⁶.
  - The exact values, 1.039375, 1.033911, 1.031915 at J = 4, 8, 16, differ from the second-order prediction by 1.0·10⁻³, 1.0·10⁻⁴, 8·10⁻⁶.
- **So the trace budget of §9.3 (≈ 5·10⁻⁴λ₀² for each input) is met by the second-order expansions with a J⁻³ remainder of the observed size from J ≈ 6 on.** A rigorous version needs explicit remainder constants (§12.4).

### 12.2 The expansion (rooted hemisphere chart; G2WOLFF §6 extended to second order and to general small graphs)
- **Setting.** I(J) = ∫Π_v dσ_v Π_{i∈ins}(σ_u·σ_v)·exp(JΣ_e c_eσ_u·σ_v), with normalized uniform measures on S³ and n = N − 1. Root one vertex (exact, by global invariance). Chart σ = (π, √(1−|π|²)) with φ = √J π.
- **Bond.** J(σ_u·σ_v − 1) = −|φ_u−φ_v|²/2 − D_e²/(8J) − (|φ_u|²+|φ_v|²)D_e²/(16J²) + O(J⁻³), with D_e = |φ_u|² − |φ_v|².
- **Measure.** −½Σ log(1−x) = Σ|φ|²/(2J) + Σ|φ|⁴/(4J²) + ….
- **Result.**
  log I = JΣc − m log|S³| + (nm/2)log(2π/J) − (n/2)log det L + log(1 + A₁/J + A₂/J²),
  with m the number of non-root vertices and
  - A₁ = E[P₁ + U₁], A₂ = E[P₂ + P₁U₁ + U₂ + U₁²/2];
  - U₁ = Σ|φ_v|²/2 − Σc_eD_e²/8;
  - U₂ = Σ|φ_v|⁴/4 − Σc_e(|φ_u|²+|φ_v|²)D_e²/16;
  - P₁, P₂ from the insertions.
  The Gaussian moments of products of quadratic forms come from G2WOLFF's cumulant core.
- **Vacuum-trial graphs** (a = 1.26376, b = 0.17713; triangle end columns (a, a, b); horizontals and interior verticals 1):

| graph | Σc | log pref | nm/2 | A₁ | A₂ |
|---|---|---|---|---|---|
| D (2 columns) | 8.409312 | −6.7653289 | 7.5 | 0.1695784 | −0.0094356 |
| N (3 columns) | 13.409312 | −11.2365373 | 12 | 0.5806129 | 0.2706650 |
| N₂ (4 columns) | 18.409312 | −15.7077457 | 16.5 | 0.9916471 | 0.7231742 |

  Residuals of log I after second order, against the engine (scratch/exact_vac_a.txt), at J = 4, 8, 16:
  - D: −1.4·10⁻³, −1.4·10⁻⁴, −1.6·10⁻⁵;
  - N: 9.5·10⁻⁴, 1.6·10⁻⁴, 2.2·10⁻⁵;
  - N₂: 6.1·10⁻³, 8.4·10⁻⁴, 1.1·10⁻⁴.
  These are J⁻³ with coefficients 0.07, 0.09 and 0.45.
- **Twisted cylinder.** tr_ℋ(KVKV) = ∫dg∫dσdσ′ V(σ)V(σ′)Π_r e^{J(σ_r·σ′_r + σ′_r·gσ_r)}. Write g = r(p)k, with p = ge₄ uniform on S³ (chart η) and k ∈ SO(3) = Stab(e₄) (Weyl angle α, density (1−cos α)/π); then dg = dp dk.
  - Twisted bond, exactly: σ′·gσ = a₁ + βa₂ + s′(sc − a₃), with a₁ = π′·kπ, a₂ = π′·η, a₃ = (kπ)·η, s = √(1−|π|²), s′ = √(1−|π′|²), c = √(1−|η|²), β = s − a₃/(1+c).
  - Its expansion f₂ + f₄ + f₆ in these quadratic forms is checked against the exact function to O(ε⁸).
  - With 18 Gaussian dimensions and n = 1 moments, converged in the α-quadrature (8 = 16 nodes):
    **log tr_ℋ(T²) = 10J − 8.9126256678 − 9 log J + log(1 + 0.84604137/J + 0.63952636/J²).**
  - Hence log(tr_ℋT²/μ₀²) = 0.0297911 + 0.0239725/J + 0.02976/J² + O(J⁻³) (scratch/trace2_n16.txt).

### 12.3 What this gives the theorem
- The trace bound (Lemma 9.2 with the p = 2 improvement) at large J, with the 4- or 10-state trial space, uses only:
  - tr_ℋT² (above);
  - tr PT²P and tr(PTP)², which are four-, three- and two-column integrals of the same type with polynomial insertions, so lapl2.py covers them.
- **Second-order coefficients are small** (0.03–0.7 in the logs), and so are the observed third-order ones (0.03–0.45). So J₁ is set by how sharp the rigorous remainder constants are, not by the expansions.

### 12.4 Rigorous remainders: the plan [plan]
- **Near region** (every vertex within angle Θ of a central root): Taylor bounds for √(1−x), (1−x)^{−1/2} and the twisted bond, with explicit sixth- and eighth-order majorants. Their Gaussian moments are positive combinations of moments of products of quadratic forms, computed exactly with the same code.
  - Since g(x,y) = √(1−x)√(1−y) − 1 + (x+y)/2 ≤ 0 (AM–GM), the exponent is bounded above by its Gaussian part. This gives one-sided bounds without cancellation.
- **Far region:** the chordal energy Σc_e|σ_u−σ_v|²/2 ≥ |σ_v−σ_r|²/(2R_eff(r,v)), integrated against the normalized Gaussian of the chart (no J^{nm/2} loss).
  - With a central root, R_eff ≤ 0.7–0.8 on these graphs, giving e^{−J(1−cos Θ)/R_eff}. That is ≲ e^{−20} at J = 30 for Θ ≈ 1.1.
- **Expected outcome:** explicit |log I − second order| ≤ K/J³ with K ≲ 10× the observed coefficients, for J ≥ 20–30. That suffices for the trace budget and for the Ritz values.
  - Residual norms for the eigenvector bounds must be bounded as norms of the explicit residual functions, not by subtraction (§11.1).

### 12.5 Files for §10–§12
- scripts/wheat.py (balanced K₄ c₃, sum-of-squares formula against cumulants); scripts/ritz.py, ritz2.py (exact Ritz tests of the explicit trial spaces; residuals and eigenvector errors); scripts/lapl2.py (second-order Laplace for small graphs); scripts/exact_vac.py (engine values of the vacuum-trial integrals and λ₀); scripts/trace2.py (twisted-cylinder expansion of tr_ℋ(T²), with a self-test of the twisted-bond series).
- scratch/: wheat.txt; ritz_J2.txt, ritz_J4.txt, ritz_J8.txt; ritz2_J0.5.txt, ritz2_J1.txt, ritz2_J8.txt, ritz2_J16.txt; lapl2_vac.txt; exact_vac_a.txt; trace2_n4.txt, trace2_n8.txt, trace2_n16.txt.

## 13. Rigorous remainders: first attempt, the gauge problem, the centre-of-mass gauge, and third order (round 4)

### 13.1 Answer first
- **A first rigorous remainder bound** (rooted chart, absolute-value majorants; scripts/rig.py) is correct in structure but 10³–10⁴ times too crude. For the two-column Gram integral D it gives J³·B ≈ 4000 at J = 100, against a true third-order coefficient ≈ 0.06.
  - Cause: a gauge artifact. In the rooted chart the measure and bond parts of U₁ are each large and nearly cancel: for D, E[U₁] = 4.81 − 4.64 = 0.17 and Var(U₁) = 10.4. Every |·| majorant pays that factor.
- **Centre-of-mass gauge [derived; checked].** Write σ_v = (π_v, s_v) in the frame of n = Σσ_v/|Σσ_v|, with the constraint Σπ_v = 0. The exact coarea identity is
  Π_v dσ_v = dn·(Σ_v s_v)³·δ³(Σ_v π_v)·Π_v s_v⁻¹dπ_v,
  valid on configurations inside n's upper hemisphere.
  - The covariance becomes L⁺. The anharmonic terms shrink: Var(U₁) = 1.22, 3.81, 8.43 for 2, 3, 4 columns, against 10.4, 18.0, 37.3 rooted.
  - The coefficients A₁, A₂, A₃ are identical in the two gauges to all printed digits. This checks the Faddeev–Popov factor and the expansion (scripts/gauge_cmp.py, lapl3.py; scratch/gauge_cmp.txt, lapl3.txt).
- **Third-order expansion [formal; validated].** I/main = 1 + A₁/J + A₂/J² + A₃/J³ + O(J⁻⁴).

| graph | A₃ | log-coefficient of J⁻³ | residual after 3rd order at J = 4, 8, 16 |
|---|---|---|---|
| D (2 columns) | −0.06057775 | −0.057352 | −5.3·10⁻⁴, −2.6·10⁻⁵, −1.5·10⁻⁶ |
| N (3 columns) | 0.09417728 | 0.002269 | −3.2·10⁻⁴, −1.1·10⁻⁵, −5·10⁻⁷ |
| N₂ (4 columns) | 0.46061082 | 0.068527 | 5.7·10⁻⁴, 4.9·10⁻⁵, 3.3·10⁻⁶ |

  The residuals fall like J⁻⁴, with fourth-order coefficients ≈ −0.10, −0.03 and +0.22.
- **J₁ outlook, revised [estimate].**
  - The binding pair (a_j, b_{j+1}) needs block amplitudes, which are O(1/J), to ≈ 0.3% relative.
  - With second-order expansions and K/J³ remainders, that needs K/(cJ²) ≤ 3·10⁻³ (c ≈ 0.3): J ≳ 100–300 for K = 10–100.
  - With exact third-order terms and crude fourth-order remainders in the CM gauge, it needs K₄/(cJ³) ≤ 3·10⁻³: J ≳ 50–100 for K₄ = 10²–10³.
  - **So the analytic regime realistically starts at J₁ ≈ 50–100.** A nearly sharp J₁ ≈ 20, which the true constants would allow, needs a better remainder technology: cumulant or cluster bounds that respect extensivity, or a Helffer–Sjöstrand representation.
  - The certified middle range should therefore be planned up to J ≈ 60–100. With the explicit trial space of §11 a J-value costs ≈ 40 column steps, and the trace can come from §12's expansion at that J, since it needs only 5·10⁻⁴. At labels ≈ 45 the 6j tables must be computed on the fly.
- **Residual norms** for the eigenvector bounds must be expanded as norms of the residual functions g = VKφ − μφ, where the leading terms cancel analytically. They cannot be obtained by subtracting separately bounded four-column integrals.

### 13.2 The remainder lemma (structure) [plan; the pieces below are proved or elementary]
- **Exact chart identity on the upper hemisphere:** J Σ_e c_e(σ_u·σ_v − 1) = −(J/2)πᵀ(L⊗I)π − (J/2)Σ_e c_e(x_u − x_v)²·w(x_u, x_v), with x = |π|², w = (s_u + s_v)⁻² and s = √(1−x).
  - w is a power series with nonnegative coefficients, so on [0, a]² the part beyond second order, w₂, satisfies 0 ≤ w₂ ≤ (x² + y²)/(4(1−a)).
  - The measure term satisfies 0 ≤ −½log(1−x) − x/2 − x²/4 ≤ x³/(6(1−a)).
- **e^H expansion:** |e^H − Σ_{k≤K}H^k/k!| ≤ |H|^{K+1}e^{H₊}/(K+1)!. The factor e^{H₊} is absorbed by tilting the Gaussian: E[F·e^{tΣ|φ|²}] = (det L/det(L−2t))^{3/2}·E_t[F].
- **Far regions:**
  - Annulus and lower hemisphere: harmonic decomposition E = |σ_v − n|²/(2R_eff) + E(δ), with the product bound M(β) = sup_t e^{−β(1−t)²/2}e^{−βt}k₀(βt) for the remaining vertices. This gives e^{−J(1−√(1−ρ²))/R_eff}·M^{m−1}·(main term)⁻¹.
  - The sup-density bound first used for the annulus is useless and is replaced by this.
- **Fast moments:** scripts/gmom.py computes Gaussian moments of products of diagonal quadratic forms by subset recursion. It agrees with G2WOLFF's core to 10⁻¹⁵.
- **Next:** exact third-order terms for the needed integrals; CM-gauge fourth-order remainder majorants; the binding pair's amplitudes first.

### 13.3 Files for §13
- scripts/gmom.py (fast diagonal-form Gaussian moments), gmom_test.py (check against G2WOLFF's core; root independence of A₁, A₂), rig.py (first rigorous remainder bound, rooted chart), gauge_cmp.py (rooted against CM gauge), lapl3.py (third-order expansion in both gauges against the engine).
- scratch/: rig_D_r1_rho06.txt, gauge_cmp.txt, lapl3.txt.

## 14. The remainder lemma, evaluated: analytic J₁ ≈ 120–150 with present technology (round 5) [explicit bound, floating-point evaluation; not yet interval-certified]

### 14.1 Answer first
- **Bound.** For a small-graph integral I(J), with the second- to fourth-order coefficients computed exactly,
  |I/main − (1 + A₁/J + A₂/J² + A₃/J³)| ≤ B(J).
  B is a sum of explicit terms: Taylor majorants on a near region, a tilted-Gaussian bound for the e^{H₊} factor, Hölder bookkeeping for the products, Gaussian tails, and far-region energy bounds (§14.2).
- **Numbers** (centre-of-mass gauge, near radius ρ = 0.6, outer radius ρ₂ = 0.85; scripts/rig3c.py; scratch/rig3c_*.txt):

| J | D (2 columns) | N (3 columns) |
|---|---|---|
| 40 | 5.5·10⁻⁴ | — |
| 50 | 8.1·10⁻⁵ | 1.2·10⁻² (far region) |
| 75 | 6.8·10⁻⁶ | 9.6·10⁻⁵ |
| 100 | 1.8·10⁻⁶ | 1.4·10⁻⁵ |
| 150 | — | 1.8·10⁻⁶ |

  - Asymptotically J⁴B ≈ 180 (D) and ≈ 900–1400 (N), against true fourth-order coefficients ≈ 0.1. The far-region terms are negligible from J ≈ 50 (D) and J ≈ 75 (N).
- **What sets J₁.** The binding pair needs block amplitudes, which are O(1/J), to ≈ 0.3%. That needs the 3-column integrals with insertions to ≈ 10⁻³/J relative, i.e. about 10⁻⁵ at J = 100. The table meets this from J ≈ 120–150.
  - A direct expansion of the binding covariance gives the same scale: positivity needs K/J⁵ ≤ c₂/J² with c₂ = 4.4·10⁻⁴ and K ~ 10³, i.e. J ≳ 130.
  - **So, with present technology, the analytic regime is J ≥ J₁ ≈ 120–150.**
- **Why higher orders do not help** (scripts/rig4.py; lapl4.py, which validates A₄):
  - Exact fourth order checks against the engine: A₄ = −0.08957 (D) and −0.02381 (N), with residuals J⁻⁵ (1.3·10⁻⁷ at J = 16).
  - But the norms of the exact signed terms grow ≈ 4–5× per order: ‖U_k‖₂ = 1.1, 2.9, 10.9, 54.6 for D. The fourth-order majorant (E Ū₄ = 108) is only 2× the exact ‖U₄‖₂.
  - So better majorants cannot help much. A sharper J₁ needs coordinates in which the anharmonic terms are smaller (the CM gauge already gained 13–50× over the rooted chart), or a non-perturbative remainder (cumulant/cluster or Helffer–Sjöstrand).

### 14.2 The bound (centre-of-mass gauge)
- **Representation.** I/main = E_γ[Φ·1_chart] + far/main.
  - γ is the Gaussian on {Σπ_v = 0} with covariance L⁺⊗I₃/J.
  - Φ = (Σs/V)³Π_v s_v⁻¹·exp(−(J/2)Σ_e c_e(x_u − x_v)²w(x_u, x_v)).
  - log Φ = H₁ + H₂ + H₃ + H₄ with H_k = U_k/J^k exact for k ≤ 3.
- **Majorant of H₄ on Ω = {all |π_v| ≤ ρ}, a = ρ²:**
  - measure: 0 ≤ M₄ ≤ x⁴/(8(1−a));
  - bonds: 0 ≤ w₃ ≤ (x³ + y³)/(4(1−a)), because w has nonnegative coefficients and its degree-k part at (a, a) is a^k/4;
  - Faddeev–Popov factor: F∘y has nonpositive coefficients, so |R_FP| ≤ (max x/a)⁴·(3/2)Σ_{k≥4}a^k/k.
- **Terms of B:**
  - B1 = (1+ε)³·dr·E_t[U₁⁴]/(24J⁴) + (1+1/ε)³·dr·‖R‖⁴_{4,t}/24 (the tilt t = 1/(2(1−a)J) absorbs e^{H₊});
  - B2 = E[U₂²]/(2J⁴), B3 = √(E U₁²·E U₃²)/J⁴, B4 = √(E U₁⁴·E U₂²)/(2J⁴), B5 = E[Ū₄]/J⁴;
  - B6: higher products, by Hölder;
  - B7: Gaussian tail of the main polynomial, via χ²₃ tails with L⁺_vv;
  - Ba: chart valid, all |π| ≤ ρ₂, some |π_v| > ρ. Here Φ ≤ (1−ρ₂²)^{−V/2}, giving (1−ρ₂²)^{−V/2}·P_γ(some |π_v| > ρ);
  - Bb: some vertex at angle ≥ arcsin ρ₂ from n, chart valid or not. The per-vertex energy bound E ≥ |σ_v − σ̄|²/(2L⁺_vv) ≥ ρ₂²/(2L⁺_vv) (minimal Dirichlet energy with a fixed deviation from the mean; better than Poincaré by the factor 1/(λ₂L⁺_vv) ≈ 2.2) is combined with a θ-split and the rigorous a priori bound I(J′) ≤ Π_{spanning tree}e^{−J′c}k₀(J′c).
- **Moments.** Exact, with scripts/gmom3.py: Gaussian moments of products of diagonal quadratic forms on multisets, with cumulants by a DP over count vectors. It agrees with G2WOLFF's core to 10⁻¹⁵ and handles 20-form moments in seconds.
- **Remaining for a certified version:**
  - interval arithmetic for the constants;
  - the insertion integrals (amplitudes) and the twisted trace in the same format;
  - residuals as norms of residual functions (§13.1).

## 15. G2WOLFF Prop. 6.1 made a theorem: strong-coupling G2 on every finite graph at leading nonvanishing order (round 5) [proved by the author; independent review needed]

### 15.1 Statement
**Theorem 15.1.** Setting:
- G is a finite connected graph with couplings J·c_xy (c_xy > 0 fixed).
- The O(N) model has N ≥ 2, and n := N − 1.
- a, b, u, v are vertices with {a,b} ≠ {u,v} (typically e = ab and f = uv are edges).
- Root at a. G_Dir is the Dirichlet Green function of the c-weighted Laplacian L on V∖{a}, g := G_Dir e_b, d := G_Dir(e_u − e_v), with g_a = d_a = 0.

Then, as J → ∞,
  Cov(q_a·q_b, q_u·q_v) = c₂J⁻² + c₃J⁻³ + O(J⁻⁴), with c₂ = (n/2)d_b².
Here d_b = g_u − g_v is the transfer current T(e,f) up to sign; it equals Δ/2 in G2WOLFF's notation.
If d_b = 0 (a balanced pair), then
  **c₃ = (n/4)Σ_{xy∈E} c_xy(g_x − g_y)²[(d_x − d_y)² + (n − 1)(d_x² + d_y²)] ≥ 0.**

**Corollary 15.2 (strong-coupling G2 on every finite graph).** For every finite graph, every coupling profile c > 0 and every pair, Cov(q_a·q_b, q_u·q_v) > 0 for all J ≥ J₀(G, c, pair), unless d_b = 0 and c₃ = 0.
- For N ≥ 3, c₃ = 0 at a balanced pair iff d vanishes at both endpoints of every edge with g_x ≠ g_y. That is, d is zero on the support of the e-current; this happens e.g. across a cut vertex, where Cov ≡ 0.
- J₀ is not uniform in G or c. An explicit J₀ for a given graph follows from the remainder lemma of §14, extended to integrals with insertions.

### 15.2 Proof
**(a) Asymptotic expansion [lit. + elementary].**
- After rooting (exact, by global O(N) invariance), each of the four integrals I, I_ab, I_uv, I_ab,uv (with the indicated dot-product insertions) is ∫_{(S^{N−1})^m}F e^{−JE}, with m = |V| − 1.
  - E = Σc_xy(1 − q_x·q_y) ≥ 0 vanishes only at the aligned configuration, by connectivity.
  - Its Hessian there is L_Dir ⊗ I_n, positive definite.
  - F is a polynomial in dot products.
- The classical Laplace theorem for a unique nondegenerate interior minimum gives full asymptotic expansions in J⁻¹ times J^{−nm/2} (e.g. Wong, *Asymptotic Approximations of Integrals*, ch. IX).
- So Cov = I_ab,uv/I − I_abI_uv/I² has an expansion in J⁻¹, and its coefficients are those of the formal Gaussian expansion.
- In the hemisphere chart q_x = (π_x, √(1−|π_x|²)), with φ = √J π and covariance G_Dir ⊗ I_n:
  - X := q_a·q_b = 1 − A/(2J) − A²/(8J²) + O(J⁻³), with A = |φ_b|²;
  - Y := q_u·q_v = 1 − |D|²/(2J) − P²/(8J²) + O(J⁻³), with D = φ_u − φ_v and P = |φ_u|² − |φ_v|² = D·S, S = φ_u + φ_v (from q_u·q_v − 1 = −|q_u − q_v|²/2);
  - the density is Gaussian × exp(U₁/J + O(J⁻²)), with U₁ = Σ_x|φ_x|²/2 − Σ_xy c_xy(|φ_x|² − |φ_y|²)²/8.
- Hence c₂ = ¼Cov_γ(A, |D|²) and c₃ = (1/16)[Cov_γ(A, P²) + Cov_γ(A², |D|²)] + ¼κ₃(A, |D|², U₁) (G2WOLFF §6).
- Wick: Cov_γ(A, |D|²) = 2n(e_bᵀG_Dir(e_u − e_v))² = 2n d_b², so c₂ = (n/2)d_b².

**(b) Balance.**
- E[φ_b,k D_l] = δ_kl d_b. So d_b = 0 makes the jointly Gaussian φ_b and D uncorrelated, hence independent.
- Write γ := g_u = g_v and R := E[D_l²] = d_u − d_v = D(d,d). Here D(f,h) = Σ_xy c_xy(f_x − f_y)(h_x − h_y) = fᵀLh for f_a = h_a = 0.
- Cov_γ(A², |D|²) = 0 by independence.
- Cov_γ(A, (D·S)²): both legs of φ_b must contract with S-legs (E[φ_b,k S_i] = 2γδ_ki) and both D-legs with each other. This gives Cov = 8nγ²R.

**(c) The cumulant term.**
- Quadratic part of U₁. For quadratic forms, κ₃(Q_A, Q_D, Q_x) = 4n[tr(B_A G B_D G B_x G) + tr(B_A G B_x G B_D G)]. Each trace contains the factor e_bᵀG_Dir(e_u − e_v) = d_b = 0.
- Quartic part. Write W_xy = (Δ·Σ)² with Δ = φ_x − φ_y and Σ = φ_x + φ_y. In κ₃(A, |D|², W_xy), A and |D|² cannot link directly, so all four legs of W_xy are used, two by A and two by |D|².
  - Use E[φ_b,kΔ_i] = δ_ki g_Δ, E[φ_b,kΣ_i] = δ_ki g_Σ, E[D_lΔ_i] = δ_li d_Δ, E[D_lΣ_i] = δ_li d_Σ, with g_Δ = g_x − g_y, g_Σ = g_x + g_y, and likewise for d.
  - Summing over the six splittings of W's legs:
    κ₃(A, |D|², W_xy) = 8n(n+1)g_Δg_Σd_Δd_Σ + 4n(g_Δ²d_Σ² + g_Σ²d_Δ²).
  - With g_Δ²d_Σ² + g_Σ²d_Δ² = 4((gd)_x − (gd)_y)² − 2(g_x² − g_y²)(d_x² − d_y²), this becomes 8n²(g_x² − g_y²)(d_x² − d_y²) + 16n((gd)_x − (gd)_y)².
  - Hence κ₃(A, |D|², U₁) = −n²D(g², d²) − 2nD(gd, gd).
- Altogether: c₃ = (n/2)[γ²D(d,d) − D(gd,gd)] − (n²/4)D(g², d²).

**(d) Summation by parts.**
- Use Lg = e_b, Ld = e_u − e_v, and the discrete Leibniz rule L(fh)_x = f_x(Lh)_x + h_x(Lf)_x − Σ_{y∼x}c_xy(f_x − f_y)(h_x − h_y).
- First term:
  - D(gd, gd) = γ²R + g_bd_b² − Σ_xy c_xy(g_x−g_y)(d_x−d_y)(g_xd_x + g_yd_y), and the middle term vanishes.
  - Write g_xd_x + g_yd_y = ½(g_x+g_y)(d_x+d_y) + ½(g_x−g_y)(d_x−d_y).
  - This gives γ²D(d,d) − D(gd,gd) = ½D(g², d²) + ½Σc_xy(g_x−g_y)²(d_x−d_y)².
- Second term: D(g², d²) = ⟨d², L g²⟩ = 2g_bd_b² − Σ_x d_x²Σ_{y∼x}c_xy(g_x−g_y)² = −Σ_xy c_xy(g_x−g_y)²(d_x² + d_y²).
- Substituting,
  c₃ = (n/4)Σc(g_x−g_y)²(d_x−d_y)² − (n(n−1)/4)D(g², d²) = (n/4)Σ_xy c_xy(g_x−g_y)²[(d_x−d_y)² + (n−1)(d_x² + d_y²)]. ∎

### 15.3 Checks and remarks
- **Numerical checks:**
  - The sum-of-squares form equals the general cumulant code to all printed digits on 11 balanced K₄/Wheatstone shapes, including lopsided ones (§10.2; scripts/wheat.py).
  - G2WOLFF reports 10⁻⁹ agreement on 75 random balanced shapes, and a scan of ≈ 20,000 shapes without a negative value.
  - the independent label-series and quadrature values on five balanced hexagon families agree with q = 2C_eff³c₃/(N−1) to 3–4 digits.
- **n = 1 (XY)** gives c₃ = ¼Σc(g_x−g_y)²(d_x−d_y)², consistent with Ginibre's G2.
- **What this gives the team:**
  - Leading-order strong-coupling G2 on every finite graph: the leading nonvanishing term is c₂ = (n/2)T² > 0, or c₃ ≥ 0 when T = 0.
  - Together with c₂ = (N−1)T²/2, this is the general-graph form of the strip picture, and it closes the k ≈ 0 corner at the level of asymptotics.
  - The remaining gap for a uniform statement is non-uniformity in the graph. J₀ grows as c₂ (or c₃ at balance) becomes small, and on ℤ² boxes T can be small for distant pairs. That is the strip problem of §9–§14.
- **Explicit J₀:** for a given graph and pair, the §14 lemma (exact terms through c₃, a J⁻⁴ remainder bound for the four integrals with insertions) gives J₀ = (remainder constant)/c₃ at balance. To do: extend rig3c.py to insertions.
- **Step-by-step numerical check of the proof** (scripts/prop61_check.py, prop61_check2.py; scratch/prop61_check*.txt). On random balanced graphs (7 vertices, log-normal couplings, balance by bisection on one coupling), each of the following agrees to all 10 printed digits:
  - Cov_γ(A, P²) = 8nγ²R;
  - κ₃(A, |D|², U₁) = −n²D(g²,d²) − 2nD(gd,gd), computed by G2WOLFF's general cumulant core;
  - the Leibniz identity of (d);
  - c₃ (cumulant core) = intermediate form = sum of squares.

### 15.4 Files for §14–§15
- scripts/gmom2.py, gmom2_test.py (DP cumulant engine), gmom3.py, gmom3_test.py (multiset engine), rig2.py (rooted-gauge bound with third order exact; superseded), rig3.py, rig3b.py, rig3c.py (CM-gauge bound; rig3c has the per-vertex far-region bound), lapl4.py (fourth-order expansion, validated), rig4.py (fourth-order bound; not better), prop61_check.py, prop61_check2.py (checks of Theorem 15.1's proof).
- scratch/: rig2_D_r1_rho09.txt, rig3_D.txt, rig3_N.txt, rig3_N_r*_r2*.txt, rig3c_N.txt, rig3c_N_r*_r2085.txt, rig3c_D_r06_r2085.txt, lapl4.txt, rig4_D.txt, prop61_check.txt, prop61_check2.txt.

### 15.5 The Laplace step, precisely (for RV11_10)
- **Reference.** L. Hörmander, *The Analysis of Linear Partial Differential Operators I*, 2nd ed., Springer 1990, Theorem 7.7.5 (stationary phase with complex phase).
  - Statement. Let K ⊂ ℝ^d be compact, X ⊃ K open, k ≥ 1. Assume u ∈ C₀^{2k}(K), f ∈ C^{3k+1}(X), Im f ≥ 0 in X, Im f(x₀) = 0, f′(x₀) = 0, det f″(x₀) ≠ 0, and f′ ≠ 0 on K∖{x₀}. Then
    |∫u e^{iωf}dx − e^{iωf(x₀)}det(ωf″(x₀)/2πi)^{−1/2}Σ_{j<k}ω^{−j}L_ju| ≤ Cω^{−k}Σ_{|α|≤2k}sup|D^αu| for ω > 0,
    with L_j differential operators of order 2j at x₀.
  - We take f = iE, so e^{iωf} = e^{−ωE} and Im f = E ≥ 0, with ω = J.
- **Hypotheses, checked for each of I, I_ab, I_uv, I_ab,uv:**
  - (H1) **Rooting is exact.** The integrand is invariant under the diagonal O(N) action, so integrating out σ_a (normalized measure) leaves the same integral with σ_a = e_N.
  - (H2) **Unique minimum.** After rooting, E = Σ_xy c_xy(1 − σ_x·σ_y) ≥ 0 on (S^{N−1})^m vanishes only at σ ≡ e_N, because G is connected and c > 0.
  - (H3) **Non-degeneracy.** In the hemisphere chart σ_x = (π_x, √(1−|π_x|²)), E is real-analytic near π = 0 with E′(0) = 0 and E″(0) = L_Dir ⊗ I_n. This is positive definite, since L_Dir (root removed, G connected) is invertible.
    - Hence x₀ = 0 is an isolated critical point, and a chart neighbourhood K contains no other.
  - (H4) **Smooth amplitudes.** With a cutoff χ ∈ C₀^∞(K), χ = 1 near 0, the amplitude u = χ·(insertion polynomial)·Π_x(1−|π_x|²)^{−1/2} is C^∞.
    - On the support of 1 − χ, E ≥ δ > 0 by (H2) and compactness, so that part is O(e^{−δJ}) relative to J^{−nm/2}.
- **Conclusion.** For every k, each of the four integrals equals e^{JΣc}J^{−nm/2}(a₀ + a₁J⁻¹ + … + a_{k−1}J^{−k+1} + O(J^{−k})), with a₀ > 0 and the a_j given by the formal Gaussian (Wick) expansion.
  - k = 4 gives Cov = c₂J⁻² + c₃J⁻³ + O(J⁻⁴), with constants that depend on (G, c, pair).
  - Nothing here is uniform in the graph.

### 15.6 The exceptional class on ℤ² boxes [proved: 15.6.1–15.6.2; computer-assisted: 15.6.3; open: all rectangles]
**15.6.1 Lemma (N ≥ 3).** Let S be the set of vertices incident to an edge carrying e-current, i.e. g_x ≠ g_y.
- (i) N[a] ∪ N[b] ⊆ S.
  - Proof: by the strict maximum principle, g_y < g_b for every y ≠ b. A second maximum point y ≠ b would propagate along neighbours to a, where g_a = 0. Symmetrically g_y > 0 for every y ≠ a.
- (ii) If (e, f) is exceptional (d_b = 0 and c₃ = 0), then d = 0 on S, from the sum of squares with n ≥ 2.
- (iii) Hence, for each endpoint w ∈ {u, v}∖{a} of f, some vertex of N[w] lies outside S.
  - Proof: otherwise d = 0 on N[w], so (Ld)_w = 0, contradicting (Ld)_w = ±1.
- In particular, **if no vertex is current-free (S = V), the class is empty.**

**15.6.2 The class is not empty on 2-connected planar graphs, even at uniform couplings [proved, explicit].**
- Construction:
  - Start from the ladder P₂ × P₃ with e = the middle rung. By the left–right symmetry, the corner vertices w₁ = (0,0) and w₂ = (0,2) are equipotential.
  - Add vertices y₁, y₂, the edge f = y₁y₂, and the edges w_iy_j (all couplings 1).
- Then:
  - no e-current enters the gadget, since it is attached only at equal potentials;
  - d = (1/4)(e_{y₁} − e_{y₂}) is supported on the gadget, since the flux into w₁ and w₂ cancels by the equal couplings;
  - so d_b = 0 and d = 0 on S, giving c₂ = c₃ = 0.
- The graph is planar and 2-connected (8 vertices).
- Check (scripts/exc_class.py, scratch/exc_class.txt): c₂ = 0, c₃ (cumulant core) = 1.8·10⁻¹⁵, c₃ (sum of squares) = 10⁻³³.
- So "2-connected planar" does not suffice. Whether Cov ≥ 0 there at strong coupling is decided at order J⁻⁴ (not computed).

**15.6.3 Uniform rectangles [computer-assisted for k, ℓ ≤ 12].**
- For all 66 rectangles P_k × P_ℓ with 2 ≤ k ≤ ℓ ≤ 12 at uniform couplings, and every edge e: every vertex carries e-current.
  - The minimum over (e, vertex) of the largest incident |current| is 3.1·10⁻⁸ (at 3 × 12, a far corner of a thin strip), against rounding ≈ 10⁻¹³.
  - The pseudo-inverse is computed as inv(L + 11ᵀ/V) − 11ᵀ/V.
  - (np.linalg.pinv loses precision here and produced spurious zeros. An exact rational solve confirms, e.g., a current of 1/290376 at the far corner of 3 × 9.)
- So by 15.6.1 the exceptional class is empty, and a direct test of all disjoint pairs agrees (scripts/exc_class3b.py, exc_class4.py; scratch/exc_class3.txt, exc_class4.txt).
- **Corollary on boxes.** For uniform couplings, every rectangle P_k × P_ℓ with k, ℓ ≤ 12 and every pair of distinct edges satisfies G2 for J ≥ J₀(box).
  - Pairs sharing a vertex are covered at every J by G2WOLFF Theorem 1.
- **Open for all rectangles:** "a unit dipole on an edge of a uniform rectangle leaves no current-free vertex". For thin strips this should follow from the explicit transverse-mode formulas; I have no general proof.
- For general couplings, couplings can be tuned to create equipotential sets, so exceptional pairs on rectangles cannot be excluded this way.

### 15.7 How J₀ depends on the graph [estimate, from the structure of the §14 bounds]
- With exact terms through J⁻³ and a J⁻⁴ remainder bound K_G for each of the four integrals, |Cov − c₂J⁻² − c₃J⁻³| ≤ ≈ 4K_G·J⁻⁴. Hence
  - J₀ ≈ (4K_G/c₂)^{1/2} for T ≠ 0;
  - J₀ ≈ 4K_G/c₃ at balance;
  - in either case, also J₀ ≳ C·L⁺_max·log|V| for the far-region terms.
- **Dependence of K_G on the graph.** The dominant terms are E[U₁⁴]/24 ∝ Var(U₁)² ∝ |V|² and E[Ū₄] ∝ |V|·(L⁺_max)⁴, so K_G ∝ |V|²·(L⁺_max)^{O(1)}.
  - Observed: K ≈ 180 for 6 vertices and ≈ 1000 for 9 (§14).
  - The |V|² comes from bounding the integrals rather than the connected covariance; a cumulant (connected) remainder would remove it.
- **Dependence on the pair.** c₂ = (n/2)T² with T(e,f) ~ r⁻² at distance r on ℤ² (dipole–dipole).
- **On an ℓ × ℓ box: J₀ ≲ C·ℓ²(log ℓ)²·r².** With a connected remainder this would improve to ~ r²(log ℓ)^{O(1)}.
- **So Theorem 15.1 is a fixed-graph theorem, not a family theorem on boxes.** The r² growth is intrinsic to fixed-order asymptotics: distant pairs have tiny c₂. Uniformity needs structure beyond the expansion, as in the strip analysis (one-signed (1,1) channel).

## 16. Tighter remainders (round 6): chart test, full-Φ cancellation, and a fourth-order-exact bound [numerical: exploratory Monte Carlo for the chart test; floating-point evaluation of an explicit bound]

### 16.1 Answer first
- **Chart test** (the item: stereographic/Cayley chart vs the hemisphere chart with centre-of-mass gauge; 2-column Gram integral D; Monte Carlo, 4·10⁵ samples; scripts/chart_test.py; scratch/chart_test_D.txt).
  - Two kinds of order-k coefficient matter: U_k, of the exponent log Φ, and P_k = [ε^{2k}]exp(ΣU_kε^{2k}), of the full integrand Φ. RMS sizes (the means of P_k reproduce A₁…A₄):

| chart (centre gauge) | ‖U₁‖ | ‖U₂‖ | ‖U₃‖ | ‖U₄‖ | ‖P₂‖ | ‖P₃‖ | ‖P₄‖ |
|---|---|---|---|---|---|---|---|
| hemisphere, CM | 1.12 | 2.93 | 11.1 | 54.3 | 2.07 | 3.65 | 10.3 |
| stereographic (= Cayley for SU(2)), Σπ = 0 | 2.03 | 3.89 | 4.85 | 7.37 | 7.08 | 31.0 | 116 |

  - The stereographic chart shrinks the higher log coefficients, since its singularities sit at radius 4 rather than 1. But it doubles ‖U₁‖, which makes the full-Φ coefficients worse. **The hemisphere chart with the CM gauge stays the best.**
- **The key finding: the full-Φ coefficients are 5× smaller than the log coefficients at order 4** (‖P₄‖ = 10.3 against ‖U₄‖ = 54.3). The order-4 terms cancel pointwise, not just in expectation. A sign-preserving remainder for Φ itself is therefore the main lever; it is not yet built, see 16.3.
- **A fourth-order-exact bound** (scripts/rig5a.py, rig5b.py, cmseries.py; scratch/rig5_D.txt):
  - The expansion is exact through J⁻⁴ (A₄ = −0.0895712).
  - The order-5 remainder of log Φ is bounded by the exact degree-5 and degree-6 pieces, each one-signed (measure +, Faddeev–Popov −, bonds −, with the bonds' Bd² factored out exactly via s_u − s_v = −Bd·Σ_k b_k h_{k−1}). The Faddeev–Popov pieces keep their 1/V weights. A crude majorant is used only from degree 7.
  - E|H₁|⁵ ≤ √(E U₁⁴·E U₁⁶), with E U₁⁶ = 20109 exact.
  - Results for D, relative error bounds (ρ = 0.6, ρ₂ = 0.85):

| J | 50 | 60 | 75 | 100 |
|---|---|---|---|---|
| §14 bound (rig3c) | 8.1·10⁻⁵ | — | 6.8·10⁻⁶ | 1.8·10⁻⁶ |
| §16 bound (rig5) | 1.25·10⁻⁴ | 1.66·10⁻⁵ | 1.9·10⁻⁶ | 2.4·10⁻⁷ |

  - So the new bound is better by 3.5× at J = 75 and 7.5× at J = 100.
  - Up to J ≈ 60 it is limited by the Hölder (single-form) L⁶ norms of U₂…U₄ inside the e^H remainder. At J = 100 it is limited by ½‖U₁‖₂‖U₂‖₄² with a term-Minkowski ‖U₂‖₄ = 50.7.
  - The exact E[U₂⁴] (1.1·10⁵ moments of ≤ 12 forms) did not finish within the 10-minute job limit; it needs an algorithmic speed-up.

### 16.2 What the numbers mean for J₁
- For D-type integrals the analytic regime now starts at J ≈ 60–75. The 3-column integrals need the same exact order-4 moments, which cost about 10× more (E U₁⁶ alone has 3.8·10⁵ multisets). Speed-ups: symmetry reduction, and closed Wick-graph formulas for E[U₁^p].
- The binding pair should not go through amplitudes (the item 3). Plan: write its covariance in the two-replica form Cov = ½E_{μ⊗μ}[(X−X′)(Y−Y′)], which is STRIPW §1.3's exterior-square minor. Then expand that integrand as one function. It is O(J⁻²) pointwise, so the remainder is relative to the covariance scale; no subtraction of separately bounded integrals is needed.

### 16.3 What would buy more [plan]
- **Sign-preserving remainder for Φ** (the 5× of 16.1 at order 4, presumably more at higher order):
  - Write Φ = A·B·e^C with A = (Σs/V)³ (decreasing), B = Πs⁻¹ (increasing), C ≤ 0.
  - Bound the Taylor remainder of the product using monotonicity in t, rather than coefficientwise majorants. Coefficientwise majorants flip the signs of A and C and destroy the cancellation.
- **Optimal truncation (Borel-type):** with norms growing ≈ 2–3× per order for P_k, truncation at k ≈ J/3 is optimal. At J = 50 that would need exact P_k far beyond what is computable, so fixed order 4–5 with good majorants is the practical choice.
- **Cumulant, cluster or Helffer–Sjöstrand bounds** (short note, as requested). They would remove the |V|² extensivity of K_G (§15.7) and give remainders relative to connected quantities. That matters for 3-column integrals and for the binding covariance. Not pursued until the explicit-J₁ version exists.

### 16.4 Update: exact norms by an X-basis engine; the bound for D improves 30–50× over §14 [floating-point evaluation of an explicit bound]
- **Speed-up.** Every polynomial here is a polynomial in the V variables X_v = |φ_v|², because Bd_e = X_u − X_v. Expanding in that basis merges terms, and Gaussian moments are then needed only over vertex multisets (scripts/xpoly.py).
  - E U₁⁶ takes 20 s instead of 246 s; E U₂⁴ = 20538 takes 0.1 s, giving ‖U₂‖₄ = 11.97 against the earlier term-Minkowski 50.7; E U₃⁴ takes 311 s, giving ‖U₃‖₄ = 79.0 against 328.
- **Refined bound** (scripts/rig5ax2.py, rig5c3.py, rig5b3.py; scratch/rig5x_moments_D.json, rig5x3_D_r2*.txt):
  - exact norms where available;
  - hypercontractive L⁴→L⁶ bounds ‖P‖₆ ≤ (5/3)^{d/2}‖P‖₄, with d the Gaussian degree;
  - the split exponent in the e^H remainder optimized for each J;
  - the Gaussian tail of the main polynomial bounded by Hölder with q = 4 instead of Cauchy–Schwarz.

| J | 40 | 50 | 60 | 75 | 100 |
|---|---|---|---|---|---|
| §14 (rig3c) | 5.5·10⁻⁴ | 8.1·10⁻⁵ | — | 6.8·10⁻⁶ | 1.8·10⁻⁶ |
| §16.4 (rig5b3) | 1.08·10⁻⁵ | 2.10·10⁻⁶ | 7.2·10⁻⁷ | 2.1·10⁻⁷ | 4.6·10⁻⁸ |

- Asymptotically J⁵B ≈ 460. The order-5 products dominate, bounded by Cauchy–Schwarz (≈ 280); then the e^H remainder and the exact one-signed order-5 pieces.
- **Next lever:** exact order 5 (A₅ = E P₅ needs moments of degree ≤ 10 only, now cheap). That moves the remainder to J⁻⁶, a further ≈ 10× at J ≈ 50.
- **Then:** the same scheme for the 3-column integrals (V = 9; degree-12 moments are feasible, degree-16 ones are not, so Minkowski/Hölder fallbacks there); and the binding pair in its two-replica form.

### 16.5 Exact fifth order (D) [floating-point evaluation of an explicit bound]
- A₅ = −0.12521164 is exact (moments of degree ≤ 10 in the X-basis; scripts/rig6a.py). The remainder is now order 6:
  - the exact one-signed degree-6 and degree-7 pieces of log Φ, plus a crude degree ≥ 8 majorant;
  - the order-6 products, each bounded with the best norm available (E[U₁²U₂²] exactly, since it is nonnegative);
  - the e^H remainder |H|⁶e^{h_max}/720, with E U₁⁶ exact;
  - generic Hölder for order ≥ 7 (scripts/rig6b3.py; scratch/rig6_D.txt; ρ = 0.7, ρ₂ = 0.95).
- **Best of the two schemes** (both bounds are valid, so the smaller one applies at each J):

| J | 40 | 50 | 60 | 75 | 100 |
|---|---|---|---|---|---|
| relative error bound for D | 1.08·10⁻⁵ (order-4 scheme) | 7.4·10⁻⁷ | 1.3·10⁻⁷ | 2.6·10⁻⁸ | 3.9·10⁻⁹ |

- For J ≤ 40 the order-5 scheme is limited by order-≥ 7 Hölder terms that involve the single-form Hölder norms of U₄ and U₅ (‖U₄‖₄ ≤ 6268, ‖U₅‖₄ ≤ 9·10⁴). Exact L⁴ norms of U₄ and U₅ need degree-20 and degree-24 moments, which are too slow at present.
- **Roadmap to the explicit-J₁ theorem** (the items, in order):
  - (i) Insertions. The trial-space matrix elements carry insertions of end-column dot products, and these contain non-diagonal forms |φ_u − φ_v|². The X-basis must be extended by these few edge variables (6 for two triangle end columns). The engine already supports general forms.
  - (ii) 3-column integrals with insertions (Ritz matrices), then 4-column ones (residual functions as single integrands).
  - (iii) The binding pair as a two-replica integrand.
  - (iv) The twisted trace, with non-isotropic forms.
  - (v) Assembly: STRIPW Lemmas 4.3–4.4 with Lemma 9.2, the §9.5 offset split, and the far/short-offset bookkeeping, with every constant explicit.

## 17. All moments at once; exact-moment bounds for the 2- and 3-column integrals; a route to the binding pair that avoids subtraction (round 7) [engine validated; bounds: floating-point evaluation of explicit bounds; the route: plan with the error budget]

### 17.1 Answer first
- **A new moment engine removes the moment bottleneck** (scripts/amom2.py; amom.py is an independent second implementation; tests amom_test.py, amom2_test.py, amom2_test2.py).
  - It computes every Gaussian moment of rank-one quadratic forms Q_f = |Σ_v W_vf φ_v|² up to total degree D in one pass. It uses M(s) = E exp(Σ s_f Q_f) = det(I − 2SΓ)^{−n/2} with Γ = WᵀGW. The determinant is multilinear in s (principal minors of Γ), so the Euler identity gives the recursion k·M_k = Σ_{j≥1} ((1 − n/2)j − k)·D_j·M_{k−j}.
  - Checks:
    - every moment agrees with the per-monomial DP engine (gmom3) to 10⁻¹⁵;
    - every moment agrees with an independent log-MGF implementation (amom.py: log M = (n/2)Σ(2^k/k)tr((SΓ)^k), then exp) to 5·10⁻¹⁴;
    - general (non-diagonal) rank-one forms reproduce the closed-form cumulant moments to 10⁻¹⁶;
    - degree caps on groups of forms are exact ring quotients.
  - Cost: degree 24 on 6 vertices in under 1 s; degree 16 on 9 vertices in 7 s. The old engine timed out at degree 12 on 9 vertices.
  - Edge forms |φ_u − φ_v|² enter as extra rank-one forms with a degree cap, so insertions of dot products are covered.
- **Exact norms replace the Hölder and Minkowski fallbacks** (scripts/rig6a_am.py; scratch/rig6am_moments_D_r7.json, rig6am_moments_N_r6.json):

| quantity | D (2 columns): exact | D: earlier bound | N (3 columns): exact | N: earlier bound |
|---|---|---|---|---|
| ‖U₂‖₄ | 11.97 | — | 25.7 | 137 (term-Minkowski) |
| ‖U₃‖₄ | 79.0 | — | 221 | 1114 |
| ‖U₄‖₄ | 733 | 6268 (Hölder) | — (degree 20) | 27257 |
| ‖U₅‖₄ | 8793 | 89532 | — (degree 24) | 4.9·10⁵ |
| E U₁⁶ | 20109 | — | 2.93·10⁵ | 3.36·10⁶ (hypercontractive) |
| A₅ | −0.12521164 | — | −0.13581057 (new) | — |

- **Bounds with exact fifth order** (scripts/rig6b4.py; scratch/rig6b4_D_r7_0.95.txt, rig6b4_N_r6_*.txt). These are relative error bounds for I/main after the exact A₁…A₅:

| J | 40 | 50 | 60 | 75 | 100 | 150 |
|---|---|---|---|---|---|---|
| D (ρ = 0.7, ρ₂ = 0.95) | 1.28·10⁻⁵ | 5.4·10⁻⁷ | 1.0·10⁻⁷ | 2.1·10⁻⁸ | 3.4·10⁻⁹ | — |
| N (ρ = 0.6, ρ₂ = 0.9) | 0.16 | 4.1·10⁻⁴ | 6.7·10⁻⁶ | 4.5·10⁻⁷ | 5.2·10⁻⁸ | 3.7·10⁻⁹ |

  - For N at J ≤ 50 the far-region θ-split (Bb) and the generic order-≥ 7 Hölder terms dominate. The order-≥ 7 terms use single-form Hölder norms of U₄ and U₅, because degree-20 and degree-24 moments on 9 vertices are out of reach. From J = 75 on, the order-6 products dominate.
  - With the light moment set (term-Minkowski L⁴ norms, §16) N had 6.6·10⁻⁵ at J = 75. So exact moments gain 150× there.
- **The binding pair without excited eigenvectors and without subtraction** (17.2).
  - For adjacent columns the bulk covariance involves only the vacuum. Expanding it in the 10-state trial space puts the cancellation (ρ = 0.0123) into an explicit finite sum of 3-column integrals, which needs only relative precision ≈ 10⁻³.
  - The vacuum error and the out-of-space part are norms of residual functions, expanded as whole functions. Their Laplace remainders enter linearly, so precision ≈ 10⁻⁵ suffices. Forming ⟨ψ,T²ψ⟩ − μ²‖ψ‖² from separately bounded integrals would need ≈ 10⁻⁹.
  - Expected J₁ for this pair ≈ 40–50, set by D-type inner remainders and the 3-column integrals.
- **Correction of a constant.** The harmonic constants used so far, a = 1.263763 and b = 0.177130, are rounded. The exact values are a = (3 + √21)/6 = 1.26376262 and b = (3√5 − √21)/12 = 0.17713569, from e^{κ₁} = φ² and e^{κ₂} = (5 + √21)/2.
  - With the exact values, I − (I + L_tri(a,a,b))⁻¹ = L_tri(a−1, a−1, b) holds (checked numerically, scripts/fixpt.py). This is the harmonic fixed point of the column step V·K.
  - Single-integral bounds are valid for any a, b, so nothing above changes. The residual functions need the exact values.

### 17.2 The binding pair through the vacuum alone [plan; the identities are exact, the error budget is an estimate]
- **Identity (bulk, adjacent columns).** With T_X = K^{1/2}XVK^{1/2}, A = T_a − c_aT, B = T_b − c_bT and Q₀ = 1 − |Ω₀⟩⟨Ω₀|:
  Cov(a_j, b_{j+1}) = ⟨Ω₀, T_aQ₀T_bΩ₀⟩/λ₀² = ⟨v_a, v_b⟩, where v_X = Q₀(T_X − c_XT)Ω₀/λ₀ for any constants c_X.
  - No excited eigenvector enters. The only gap needed is the vacuum gap λ₀ − λ₁ ≈ 0.85λ₀.
- **Trial vacuum.** ψ̂₀ is the Ritz vacuum of the 10-state space P = {K^{1/2}e^{J(aX+aY+bZ)}p : deg p ≤ 2}. Its true error is ≈ 3.5·10⁻³/J² (§11). The constants c_X are chosen so that ⟨ψ̂₀, (T_X − c_XT)ψ̂₀⟩ = 0, and v_X^tr = (T_X − c_XT)ψ̂₀/μ₀.
- **Exact decomposition.** Let e_i be any orthonormal basis of P and Q_P = 1 − P. Then
  ⟨v_a^tr, v_b^tr⟩ = Σ_i ⟨v_a^tr, e_i⟩⟨e_i, v_b^tr⟩ + ⟨Q_Pv_a^tr, Q_Pv_b^tr⟩.
  - Each amplitude ⟨e_i, v_X^tr⟩ is a 3-column integral with insertions: an end polynomial and X − c_X in the middle column. No near-cancellation occurs inside one amplitude, so the Laplace remainder is small relative to the amplitude.
  - The cancellation between channels sits in the finite sum. Its error is ≤ (relative amplitude error) × Σ|a_ib_i|, so relative precision 10⁻³ is ample.
  - |⟨Q_Pv_a, Q_Pv_b⟩| ≤ ‖Q_Pv_a‖‖Q_Pv_b‖. At harmonic order v_X is a two-phonon state; the four-phonon part is O(1/J) and lies in P (quadratic p). So ‖Q_Pv_X‖/‖v_X‖ = O(J⁻²), while ≤ 7% suffices.
- **Residual functions, expanded as whole functions.** Q_Pv_X and the vacuum residual (T − μ₀)ψ̂₀ have the form K^{1/2}g with g = (X − c)VKφ − Σα_iφ_i, resp. VKφ − μφ.
  - Expand the inner integral Kφ(σ) = ∫K(σ,σ″)φ(σ″)dσ″ conditionally, in one chart for everything. The gauge is the centre of mass of the two middle columns (σ, σ′) of ⟨g, Kg⟩. Given σ, the variable σ″ is Gaussian with mean (I + L_tri)⁻¹φ_σ.
  - With the exact (a, b) the harmonic factors of VKφ and μφ coincide (fixed point above). So g = φ_harm·[explicit polynomial in t and the chart variables] + δg, where δg is the conditional Taylor remainder.
  - Then ‖K^{1/2}g‖ ≤ ⟨g̃, Kg̃⟩^{1/2} + ⟨|δg|, K|δg|⟩^{1/2}.
    - The first term is a 2-column integral of an explicitly small integrand. All its pieces are expectations under one 4-column Gaussian (the conditional laws of σ″ and σ‴ given the middle columns are independent), so its leading orders cancel exactly in the coefficients.
    - The second term is bounded by Cauchy–Schwarz by the L² norm of the inner Taylor remainder under the 4-column measure. That is a 6-vertex marginal moment problem: ≈ B_inner·λ₀‖ψ‖, linear in B_inner.
- **Vacuum error.** ‖Ω₀ − ψ̂₀‖ ≤ ‖(T − μ₀)ψ̂₀‖/(μ₀ − λ₁). It enters Cov through 2‖e₀‖·‖A v_b^tr‖ plus O(‖e₀‖²) terms.
  - ‖A v_b^tr‖ ≤ Σ_i|β_i|‖Ae_i‖ + 2λ₀‖Q_Pv_b^tr‖ is O(J⁻²)λ₀. Each ‖Ae_i‖² is a positive 4-column integral with two insertions, computed directly without subtraction.
  - So ‖e₀‖ ≲ 2·10⁻⁵ suffices. At J = 40 the true error is ≈ 2·10⁻⁶ and the inner remainder adds ≈ B_inner ≈ 10⁻⁵.
- **Finite strips.** Near an end the left state is the explicit boundary state T^{j−1}b, with a free P₃ end column (no T–B bond), instead of Ω₀. The same decomposition applies with an oblique projection in the 2×2 minor and explicit end columns. From j ≈ 6 the bulk form applies, since the correction is ≲ 0.146^{j−1}·O(J⁻²).
- **Order of work:**
  - (1) the inner conditional expansion and the residual norm of the vacuum;
  - (2) the amplitudes ⟨e_i, v_X^tr⟩ and ‖Ae_i‖;
  - (3) ‖Q_Pv_X‖;
  - (4) assembly for (a_j, b_{j+1}), then the three other short-offset configurations of §9.5 and the end positions;
  - (5) the remaining pair types through the block decomposition, which needs only O(1/J)-accurate data, and the theorem.

## 18. The vacuum residual as a whole function: conditional expansion, exact orders 2–4, and where the remainder stands (round 7, continued) [machinery validated; bound: floating-point evaluation of an explicit near-region bound; tails and far regions not yet included]

### 18.1 Answer first
- **The residual function of the trial vacuum can now be expanded exactly, order by order.** With the gauge at the centre of mass of the two middle columns (σ, σ′) of ⟨g, Kg⟩, we have
  ‖(T − mλ_h)ψ‖² = main₂·λ_h²·E_{γ₄}[M(L₁ − mL₀)(R₁ − mR₀)].
  - γ₄ is the 4-column Gaussian. M carries the Faddeev–Popov factor and the middle measure and bonds. L₁ is the σ″-side factor (measure of σ″, triangle of σ″, horizontals σ″–σ, verticals of σ, trial polynomial p(σ″)). L₀ is the triangle and p of σ.
  - Given σ, σ″ is Gaussian with mean (I + L_tri)⁻¹φ_σ and covariance (I + L_tri)⁻¹. So the residual function is r(σ) = E[L₁|σ] − mL₀(σ) = Σ_k t^k r_k(σ).
- **New engines** (all validated):
  - condexp.py / condexp2.py: conditional moments of rank-one forms as polynomials in the Gram matrix of the conditioning field, from E[exp(Σs_fQ_f)|φ₁] = det(I − 2SΓ)^{−n/2}·exp(tr[(I − 2SΓ)⁻¹S·P g Pᵀ]).
    - Averaging over φ₁ reproduces the joint moments to 4·10⁻¹⁵, and Monte Carlo at fixed φ₁ agrees within 1.6σ.
    - condexp2 uses dense supports and degree caps: degree 10 with ≤ 2 edge forms takes 30 s.
  - wishart.py: moments of Gram entries g_rs (Wishart), from det(I − 2SG)^{−n/2} and the Euler recursion. Diagonal moments agree with amom2 to 4·10⁻¹⁶, second moments are exact, and Monte Carlo agrees within 1.8σ.
  - condg.py: conditional expectations kept in the Gram variables (total degree is preserved).
  - npoly.py, moment_np.py: numpy polynomial algebra.
- **Exact orders** (scripts/vacres.py, vacres3.py; scratch/vacres_K2.json, vacres_K3.json). The trial vacuum is φ = e^{J(aX+aY+bZ)}(1 + tq₁(ξ) + t²q₂(ξ) + t³q₃(ξ)), with ξ = J(1 − Gram) and q_i in the 9 non-constant monomials of degree ≤ 2.
  - **Invariance checks pass.** r₁ has no X-terms for any q₁, and r₂ has none once r₁ = 0 (3·10⁻¹⁵), as the SO(4)-invariance of the true residual requires.
  - **Order 1:** r₁ ≡ 0 is solvable exactly (residual coefficients 9·10⁻¹⁵), with m₁ = 0.4110342096 = A₁(N) − A₁(D). q₁ = (0.232850, 0.232850, 0.226700; −0.024871, −0.024871, −0.013863; −0.022998, −0.026099, −0.026099) in the basis ξ_TM, ξ_MB, ξ_TB, squares, products (TM·MB, MB·TB, TM·TB). It is flip-symmetric.
  - **Orders 2 and 3:** minimizing over q₂, m₂ and then q₃, m₃ gives m₂ = 0.2143944522 and m₃ = 0.1325074. B₀(r₂, r₂) = 6.96·10⁻⁶ and B₀(r₃, r₃) = 7.78·10⁻⁶.
    - So the exact leading residual is ‖(T − μ̂)ψ‖/(λ‖ψ‖) = 2.64·10⁻³/J² + O(J⁻³): 1.05·10⁻⁶ at J = 50 and 2.6·10⁻⁷ at J = 100.
    - This matches the true error of the 10-state vacuum (3.1–3.5·10⁻³/J², §11) times the gap.
  - **Order 4:** the conditional expectation (condexp, degree 8) gives ‖r₄‖ = 0.80 in the Cauchy–Schwarz norm, so t⁴‖r₄‖ = 1.3·10⁻⁷ at J = 50.
- **What the binding pair needs from it.** ‖e₀‖ ≤ ‖(T − μ̂)ψ̂‖/(μ̂ − λ₁). It enters the covariance as 2‖e₀‖·‖A v_b‖ ≈ 0.25‖e₀‖/J², against a margin (c₂ + c₃/J)/J² ≈ 5·10⁻⁴/J². So ε_r := ‖(T − μ̂)ψ̂‖/(μ̂‖ψ̂‖) ≤ 3·10⁻⁴ suffices.
- **The remainder is the obstacle** (scripts/vacrig*.py). The rigorous bound needs the inner Taylor remainder of E[L₁|σ] beyond the explicit orders, and that remainder is large in every norm I tried:
  - **Joint L² norms** of the inner coefficients (L₁)_k are 2.52, 13.3, 125.5, 1707 (k = 1…4). They grow 10–15× per order, against ≈ 2–4× for the 2-column integral D in its own centre-of-mass gauge.
    - Cause: given σ, the end column σ″ has conditional variance ≈ 0.52 per vertex, of which 1/3 is its rotation relative to σ. With the outer pole that becomes ≈ 0.7. The measure and bond anharmonicities are polynomials in |φ″|², whose high moments grow like χ²₃ moments.
    - The conditional expectations themselves are small (‖E[F₄|σ]‖ = 5.6, nearly cancelled by (mL₀)₄). Only the fluctuations are large.
  - **Coefficientwise majorants** are useless (‖E[F̄₄|σ]‖ = 1.5·10⁵), because of the (X_u − X_v)² cancellations.
  - **The τ-polynomial route** (sup over τ of the polynomial D_{K+1}(τ)) blows up for the same reason.
  - **What works:** explicit r₂, r₃, r₄, then an order-5 remainder in the integral form with closed-form derivative majorants valid on the near region. These are |meas^{(k)}| ≤ (k−1)!X^k/(2(1−a)^k) and |bond^{(k)}| ≤ (c/2)(X_u−X_v)²k!m^{k−1}/(4(1−a)^{k+1}) (w(z,z) = 1/(4(1−z)) dominates w coefficientwise), plus ξ̄-majorants for p. The remainder is evaluated in the mixed norm (conditional L¹ in σ″, L² in σ), with the e^{meas} factors absorbed by Gaussian tilts.
    - Near-region result at J = 100 (radii 0.4 middle, 0.45 end): ε_near ≤ 2.07·10⁻⁴, of which 1.94·10⁻⁴ is the order-5 remainder (scratch/vacrig8_r45.txt).
    - At radius 0.45 the end-column tail is not negligible at J = 100 (P(|π″| > 0.45) ≈ 10⁻⁵). Radius ≈ 0.6 is needed, and the (1−a)^{−k} constants then cost ≈ 4×.
- **Estimate:** with this technology the vacuum residual closes (ε_r ≤ 3·10⁻⁴ including tails) at J ≈ 120–150, not at 50–100.

### 18.2 Options [plan]
- **(A) Complete the binding-pair theorem at J₁ ≈ 120–150.**
  - The other pieces need much less precision: trial-space amplitudes ≈ 10⁻³ relative, ‖Q_Pv_X‖/‖v_X‖ ≤ 7%, ‖A e_i‖ to 10%, and λ₁ ≤ 0.2λ₀ from the twisted trace to 0.5%. So the vacuum residual sets J₁.
  - Cost: the certified middle range would have to reach J ≈ 150.
- **(B) Sharpen the inner remainder to reach J₁ ≈ 70–90.** Estimated gains:
  - replace the worst-case (1−a)^{−k} by per-term Gaussian tilts (typical factor 1.2 instead of 4–10);
  - make order 5 explicit (condexp at degree 10 is feasible) and bound the order-6 remainder.
  - Both are mechanical but heavy; the gain is uncertain (2–5×).
- **(C) Treat the end column's rotation exactly** (SO(4) group integral), or use the cumulant/cluster route.
  - The 10–15× growth per order comes from the soft rotation mode of σ″ relative to σ. A connected expansion would not see it.
  - This is research-level and was deferred.

### 15.8 After review: RV22_24 confirms Theorem 15.1; two corrections; the 8-vertex example settled by the review; a closed form on C₄ (appended)
- **Review.** the RV22_24 FINAL (sha8 5d7d407c) confirms Theorem 15.1 and Corollary 15.2. The review moved from the review to the review.
- **MINOR 1 (§15.5).** Hörmander's Theorem 7.7.5 bounds the remainder in absolute terms, by Cω^{−k}Σsup|D^αu|, while the leading term is of size ω^{−nm/2}.
  - To obtain I/(leading term) to relative order J^{−k}, apply the theorem with k + ⌈nm/2⌉ terms, not with k.
  - So "k = 4 gives Cov = c₂J⁻² + c₃J⁻³ + O(J⁻⁴)" should read "k = 4 + ⌈nm/2⌉". The conclusion is unchanged.
- **MINOR 2 (§15.6.1).** Part (i), N[a] ∪ N[b] ⊆ S, is false when a or b is a cut vertex with a pendant block: the pendant block sits at one potential and carries no e-current. An exact counterexample exists.
  - (i) is withdrawn. It is not used: the emptiness criterion "S = V ⇒ the exceptional class is empty" rests on (ii)–(iii) only.
- **The 8-vertex example of §15.6.2 is positive at strong coupling** (the review, RV22_32 FINAL; parts .head 51594c15, .methods 6ea581f6, .validation 3dd6ae02, .errors 90fa7634 in /mnt/g2/release/root/data/e14/pk20/rv22/).
  - Graph: the ladder P₂ × P₃, e = the middle rung, and the gadget y₁, y₂ with f = y₁y₂ attached at the equipotential corners. All couplings are J.
  - Cov(e, f) > 0 at N = 3 and 4 for all J computed (10 to 320).
  - c₄ ≈ +8.2·10⁻⁴ (N = 3) and +3.0·10⁻³ (N = 4), from exact interpolation and Richardson extrapolation of arb values (400 bits, 30 digits).
  - Two independent methods: an exact sector/transfer reduction in arb, and a direct 3D quadrature reduction in double precision. They agree to ≈ 10⁻¹⁷ absolute at J = 10 and 20.
  - So on this graph G2 holds at strong coupling, decided at order J⁻⁴. The counterexample question for "all planar graphs" stays open only in the sense that no negative case is known.
- **Open lemma (recorded at the request).** "For every uniform rectangle P_k × P_ℓ and every edge e, every vertex carries e-current."
  - It is verified for k, ℓ ≤ 12 (§15.6.3). A proof would make the box form of Corollary 15.2 unconditional for all rectangles at uniform couplings.
- **Closed form on the 4-cycle (cross-link with the RV23_14 §24).**
  - Setting: C₄ = 1–3–2–4–1 with couplings K₁₃ = α, K₂₃ = β, K₁₄ = λα, K₂₄ = λβ. This is the general balanced bridge, K₁₃K₂₄ = K₁₄K₂₃. Take the diagonal pair (a, b) = (1, 2), (u, v) = (3, 4).
  - Theorem 15.1 gives c₃ = n²/(4e₃(K)), with e₃ = λαβ(1+λ)(α+β) the spanning-tree polynomial. So Cov·e₃(JK) → (N−1)²/4, which is the Gibbs-level value.
  - Proof:
    - g₃ = g₄ = 1/(α(1+λ)) and g₂ − g₃ = g₂ − g₄ = 1/(β(1+λ)).
    - The d-problem (unit current 3 → 4, vertex 1 grounded) has V₂ = 0, V₃ = 1/(α+β) and V₄ = −1/(λ(α+β)).
    - So d_xd_y = 0 on every edge, and each bracket in the sum of squares collapses to n(d_x² + d_y²).
    - The four edge terms sum to n²/(4αβλ(1+λ)(α+β)).
  - Numerical check: 6 random balanced shapes, including K-ratios up to 2500, give c₃·e₃ = 1.0000000000 (N = 3) and 2.2500000000 (N = 4) (scripts/c4_c3.py).

## 19. The strong-coupling theorem for 3 × n grids at an explicit J₁ (round 8; the decision (A)) [in progress; pieces frozen for review as completed]

### 19.0 Plan (structure mirrors STRIPW §1–§8)
- **Target.** Theorem S: for N ∈ {3, 4}, every n ≥ 2, every pair of distinct edges of the 3 × n grid with all couplings J, and every J ≥ J₁ (explicit, ≈ 120–150), Cov(σ_e, σ_f) > 0.
- **Frame.** STRIPW §1, unchanged: T = K^{1/2}VK^{1/2} on the invariant sector, Cov·Z² as a 2×2 minor, and the reduction Cov·N² = S_cl + S_∞ + R_CE (STRIPW §4.4).
  - The roles of STRIPW's 4-state block are taken by the vacuum Ω₀ and the strong-coupling cluster Ω₁, Ω₂, Ω₃ = (1,1), (1,2), (2,2).
  - The complement starts at the four-phonon level.
- **Inputs, each a frozen piece:**
  - 19.1 Laplace bounds for small-graph integrals with insertions (general lemma; riglap.py).
  - 19.2 The vacuum residual lemma: ‖(T − μ̂)ψ̂₀‖ ≤ ε_r μ̂‖ψ̂₀‖, so ‖Ω₀ − ψ̂₀‖ ≤ ε_r/(1 − λ₁/μ̂ − ε_r) (inner conditional expansion, §18).
  - 19.3 The 10-state trial space: Gram and T-matrices with insertions, Ritz data, and the twisted trace, giving τ_∞ by Lemma 9.2 (precision ≈ 10⁻⁴ suffices). Also λ₁ ≤ 0.2λ₀.
  - 19.4 Coupling c = ‖Q_PTP‖ through residual functions of the basis states, and cluster eigenvectors by STRIPW Lemmas 4.3–4.4.
  - 19.5 Amplitudes â_l for every edge type, bulk and near the ends, and ‖Q_Pũ‖.
  - 19.6 Assembly.
    - W1 analogue (pairs that are not top–bottom): every cluster channel is positive. The sign of A_h(1,1) is controlled through the product ⟨χ₂, Q_Pũ_h⟩ of two small quantities.
    - W2 analogue (top–bottom pairs): Bernoulli convexity F(m) ≥ F(0). At strong coupling this needs only x + y − 2z ≥ 0.03λ₀ and p₂ ≥ 0.55p₄; the true ratio is ≈ 4. F(0) > 0 comes from route V′ (§17.2) at m = 0.
    - Same-position pairs, the ends, and short strips.

### 19.1 Lemma 19.1: Laplace bounds with insertions on small graphs [proved by the author, modulo floating-point evaluation of finite sums; independent review needed] (scripts/riglap.py; checks riglap_test*.py, riglap_majtest.py)
**Setting.**
- G = (V, E) is finite and connected, with couplings Jc_e (c_e > 0). The O(N) model has n = N − 1, and normalized uniform measures on S^{N−1}.
- I(J) = ∫Π_v dσ_v F(σ) exp(JΣ_e c_e(σ_u·σ_v − 1)).
- F is a product of factors of three types:
  - 'dot': σ_u·σ_v − c;
  - 'p': the trial polynomial of a column (T, M, B), 1 + Σ_{i≤3} t^i q_i(ξ), with ξ = J(1 − σ_T·σ_M, 1 − σ_M·σ_B, 1 − σ_T·σ_B) and q_i in the 9 monomials of degree 1–2;
  - 'const'.
- t = 1/J. main(J) = |S^{N−1}|^{−(V−1)}(2π/J)^{n(V−1)/2}(det L|_{1⊥}/V)^{−n/2}.

**Chart.** Centre-of-mass gauge over all vertices, with scaled variables φ_v = √J π_v and Σφ_v = 0. γ is the Gaussian with covariance L⁺ ⊗ I_n.
- Then I/main = E_γ[F e^H 1_chart] + far/main, where H = Σ_v meas_v + FP + Σ_e anh_e.
- In terms of X_v = |φ_v|² (so tX_v = |π_v|²):
  - meas_v = −½log(1 − tX_v) ≥ 0;
  - FP = n·log(1 − y) ≤ 0, with y = V⁻¹Σ_v(1 − √(1 − tX_v));
  - anh_e = −(c_e/2)·t(X_u − X_v)²·w(tX_u, tX_v) ≤ 0, with w(x, y) = (√(1−x) + √(1−y))⁻² (§13.2).
- The insertions are polynomials in ξ_uv = Q_uv/2 + ½(X_u − X_v)²·t·w(tX_u, tX_v), with Q_uv = |φ_u − φ_v|², because J(1 − σ_u·σ_v) = ξ_uv exactly.

**Statement.** Fix K ≥ 0, radii ρ_v ∈ (0,1) (a_v = ρ_v²), an outer radius ρ′ ∈ (max ρ_v, 1), and Ω = {tX_v ≤ a_v for all v}. Then
  I/main = Σ_{k≤K} a_k t^k + R,  with a_k = E_γ[(F e^H)_k] (exact Gaussian moments) and |R| ≤ B_rem + B_tail + B_ann + B_far, where:
- **B_rem** = t^{K+1}/(K+1)!·N_c·E_c[D̄_{K+1}]. Here:
  - E_c and N_c are the Gaussian tilted by exp(Σ_v c_v tX_v) and its normalization (det ratio)^{n/2}, with c_v = −log(1 − a_v)/(2a_v);
  - D̄_{K+1} = Σ_j C(K+1, j) F̄_j·Ȳ_{K+1−j}(h̄₁, …, h̄_{K+1−j});
  - Ȳ is the complete Bell polynomial;
  - h̄_k and F̄_j are the derivative majorants below.
- **B_tail** = Σ_{k≤K} t^k‖(F e^H)_k‖_{L²(γ)}·P_γ(Ω^c)^{1/2}, with P_γ(Ω^c) ≤ Σ_v P(χ²_n > Ja_v/L⁺_vv).
- **B_ann** = N_{c′}·‖F̄₀′‖_{L²(c′)}·P_{c′}(Ω^c)^{1/2}. This is the annulus "all |π_v| ≤ ρ′, some |π_v| > ρ_v", using F̄₀′ (the majorant of |F| with all radii ρ′) and the tilt c′ = −log(1 − ρ′²)/(2ρ′²).
- **B_far** = sup|F|·min_θ exp[log Σ_v e^{−θJρ′²/(2L⁺_vv)} + Σ_{tree} log(2I₁((1−θ)Jc)e^{−(1−θ)Jc}/((1−θ)Jc)) − log main(J)]. This covers "some |π_v| > ρ′, or some σ_v in the lower hemisphere".
- sup|F| uses |σ·σ − c| ≤ 1 + |c| and ξ ≤ 2J.

**Derivative majorants.** Valid for 0 ≤ τ ≤ t and X ∈ Ω (with Q ≥ 0). Write D_e = (X_u − X_v)², m_e = max(X_u, X_v), M_{k−1} = X_u^{k−1} + X_v^{k−1} (M₀ = 1), and a_e = max(a_u, a_v).
- **Measure:** meas_v^{(k)}(τ) = (k−1)!X_v^k/(2(1 − τX_v)^k) ≤ (k−1)!X_v^k/(2(1−a_v)^k).
- **Bonds:** anh_e = −(c_e/2)D_e·W_e(τ), with W_e(τ) = τw(τX_u, τX_v).
  - w has nonnegative Taylor coefficients, and Σ_{i+j=k} w_ij = [z^k]w(z, z) = [z^k](4(1−z))⁻¹ = 1/4.
  - So W_e is dominated coefficientwise by τ/(4(1 − τm_e)), whose k-th derivative is k!m_e^{k−1}/(4(1 − τm_e)^{k+1}).
  - Hence |anh_e^{(k)}| ≤ (c_e/2)D_e·k!·M_{k−1}/(4(1 − a_e)^{k+1}).
- **Faddeev–Popov:** −FP = n·g(y) with g(y) = −log(1 − y). Both g and τ ↦ y(τ) have nonnegative coefficients. By Faà di Bruno,
  |FP^{(k)}| ≤ n·Σ_{m≤k}(m−1)!(1 − ȳ_max)^{−m}·B_{k,m}(ȳ₁, ȳ₂, …),
  - with ȳ_j = V⁻¹Σ_v c_j X_v^j (1 − a_v)^{1/2−j} and c_j = (2j−3)!!/2^j, from (1 − √(1−x))^{(j)} = c_j(1−x)^{1/2−j};
  - and ȳ_max = V⁻¹Σ_v a_v/(2 − a_v), since 1 − √(1−x) = x/(1 + √(1−x)) ≤ x/(2 − x).
- h̄_k is the sum of these three bounds.
- **Insertions:** ξ_uv^{(l)} ≤ (D_uv/8)·l!·M_{l−1}/(1 − a_uv)^{l+1} for l ≥ 1, and ξ_uv ≤ Q_uv/2 + tD_uv/(8(1 − a_uv)).
  - 'dot': |(τξ)^{(j)}| ≤ jξ̄_{j−1} + tξ̄_j.
  - 'p': Leibniz on τ^i q_i(ξ(τ)), with |c_ib| on each monomial of ξ̄'s.
  - Products: Leibniz over the factors.

**Proof.**
- (i) The chart identity and the sign structure of H are §13.2–§14. The factor n·log(1 − y) is the coarea factor (Σs/V)^n.
- (ii) Taylor's theorem in integral form, in τ at fixed (X, Q), applied to τ ↦ F(τ)e^{H(τ)} on Ω, where H(τ) and F(τ) are the true functions with t replaced by τ:
  |Fe^H − Σ_{k≤K} t^k(Fe^H)_k| ≤ t^{K+1}/(K+1)!·sup_{τ≤t}|(Fe^H)^{(K+1)}(τ)|.
  - (Fe^H)^{(K+1)} = e^H·Σ_j C(K+1, j)F^{(j)}Y_{K+1−j}(H′, H″, …).
  - |Y_k(H′, …)| ≤ Ȳ_k(h̄) because Bell polynomials have nonnegative coefficients.
  - e^{H(τ)} ≤ e^{meas(τ)} ≤ e^{meas(t)} ≤ exp(Σc_v tX_v) on Ω, because FP ≤ 0, anh ≤ 0 and −½log(1−x) ≤ c_v x for x ≤ a_v.
  - Extending to all of space (the integrand is ≥ 0) gives B_rem.
- (iii) E_γ[(Fe^H)_k 1_Ω] = a_k − E_γ[(Fe^H)_k 1_{Ω^c}]. Cauchy–Schwarz gives B_tail.
- (iv) On the annulus the chart is valid, s ≥ √(1−ρ′²), and |Fe^H| ≤ |F|e^{meas} ≤ F̄₀′·exp(Σc′tX). Cauchy–Schwarz under the tilt gives B_ann.
- (v) Outside "all |π_v| ≤ ρ′": some σ_v has |σ_v − σ̄| ≥ ρ′ (for the lower hemisphere, ≥ 1).
  - The energy satisfies E ≥ |σ_v − σ̄|²/(2L⁺_vv) (minimal Dirichlet energy for a fixed deviation from the mean, §14.2).
  - The θ-split E ≥ θE_min + (1−θ)E, with Z((1−θ)J) bounded by its spanning-tree product, gives B_far.
  - The tree bound is exact for trees and an upper bound in general, since dropping edges only increases e^{−JE}. ∎

**Checks.**
- a_k agrees with rig6a_am for D and N without insertions (A₁…A₄ to all digits, riglap_test.py).
- With 'dot' insertions, a₁ and a₂ agree with lapl2 (rooted chart, an independent code using G2WOLFF's core) to 8 digits for four insertion sets (riglap_test3.py).
- 'p' factors equal the equivalent 'dot' combinations, 1 + tξ_e = 2 − σ·σ and 1 + t²ξ_eξ_f = 1 + (1 − σ·σ)(1 − σ′·σ′), to 2·10⁻¹⁴ through order 4 (riglap_test4.py).
- **The majorants hold:** at 25 random near-region points and random τ ≤ t (J = 60, a = 0.3, a random trial polynomial and a shifted dot), max|H^{(k)}|/h̄_k = 0.49 and max|F^{(j)}|/F̄_j = 0.66 for k, j ≤ 5. The exact derivatives come from mpmath at 40 digits (riglap_majtest.py).

**Numbers (N = 4, exact harmonic a, b, no insertions; relative error bounds for I/main).** Radii a_v = s*·L⁺_vv/J (a common tail exponent), ρ′ = 0.9 (riglap_test5.py):

| integral | K | s* | J = 120 | J = 150 |
|---|---|---|---|---|
| D (2 columns) | 5 | 70 | 4.9·10⁻⁷ | 3.7·10⁻⁷ |
| N (3 columns) | 4 | 70 | 1.9·10⁻⁵ | 4.1·10⁻⁶ |

- For D the tail terms dominate at this s*. The remainder alone is 2.3·10⁻⁸ at J = 150, so a Chernoff-tilted tail bound (full exponent instead of ½) would gain ≈ 10×.
- For N the order-5 majorant dominates. It is ≈ 10³–10⁴ above the signed-norm bounds of §17 (rig6b4), because absolute majorants lose the cancellations between measure, Faddeev–Popov and bond terms. It is simpler and fully pointwise, which is what the insertion integrals need.
- **Caveat:** the moments and sums are evaluated in double precision. The moment engines are exact recursions with nonnegative weights, so an interval version is mechanical. N = 3 needs n = 2 in place of 3 throughout and has not been run yet.
- **N = 3 (added).** scripts/riglap2.py is riglap.py with n = N − 1 as a parameter. It changes the Faddeev–Popov coefficient to n, the Gaussian components to n, the normalization exponents to n/2, |S^{N−1}| = 4π, the χ²_n tails, and the S² tree factor (1 − e^{−2x})/(2x).
  - At N = 4 it reproduces riglap.py exactly.
  - At N = 3, a₁ and a₂ agree with lapl2(N = 3) to 8 digits, both with dot insertions and without (D: A₁ = 0.43476529, A₂ = 0.22289272) (riglap2_test.py).
  - N = 3 bounds, same choices as the table above:

| integral | K | J = 120 | J = 150 |
|---|---|---|---|
| D | 5 | 1.7·10⁻⁷ | 1.4·10⁻⁷ |
| N | 4 | 5.4·10⁻⁶ | 1.2·10⁻⁶ |

### 19.2 Lemma 19.2: the vacuum for all J ≥ 150 — residual, trace, gap and vacuum error [proved by the author, modulo floating-point evaluation of finite sums and an α-quadrature checked by node doubling; independent review needed] (scripts/twlib.py, twrig3.py, vacrig11f.py, vacmono.py, vacgap.py)

**Answer first.**
- The vacuum is now controlled for every J ≥ 150, at N = 3 and N = 4. The new piece is a rigorous upper bound on the one-column twisted trace tr_ℋT, good to 4·10⁻⁴ relative at J = 150. It gives the vacuum gap λ₁ ≤ 0.3323·λ₀ and, together with the residual bound of §18, the vacuum error ‖ψ̂ − Ω₀‖ ≤ 2.98·10⁻⁴‖ψ̂‖ (N = 4) and 1.09·10⁻⁴‖ψ̂‖ (N = 3).
- The binding pair needs ‖e₀‖ ≲ 3·10⁻⁴ (§18.1: the vacuum enters Cov as ≈ 0.25‖e₀‖/J² against a margin ≈ 5·10⁻⁴/J²). So J₁ = 150 holds for the vacuum at both N, with a factor ≈ 6.7 to spare in the covariance (N = 4).

**Setting.**
- ℋ is the O(N)-invariant subspace of L²((S^{N−1})³) with normalized measures. T = K^{1/2}VK^{1/2} is the one-column transfer operator of the 3 × n grid: K carries the three horizontal bonds, V the two vertical bonds T–M and M–B. Its eigenvalues on ℋ are λ₀ > λ₁ ≥ ….
- λ_h = main_N/main_D is the Gaussian main term of the Rayleigh quotient ⟨φ, KVKφ⟩/⟨φ, Kφ⟩, with the graphs N (3 columns) and D (2 columns) of §17–§18 and the exact couplings (a, a, b) = ((3+√21)/6, (3+√21)/6, (3√5−√21)/12).
- The trial vacuum is ψ̂ = K^{1/2}φ with φ = e^{J(aX+aY+bZ)}(1 + tq₁(ξ) + t²q₂(ξ) + t³q₃(ξ)) (§18.1; q_i in scratch/vacres_K3_N{3,4}.json). μ̂ = m̂λ_h with m̂ = 1 + m₁t + m₂t² + m₃t³:

| N | m₁ | m₂ | m₃ |
|---|---|---|---|
| 4 | 0.4110342096 | 0.2143944522 | 0.1325073767 |
| 3 | 0.3639110189 | 0.1902087354 | 0.1312176314 |

**Lemma 19.2.** For N ∈ {3, 4} and every J ≥ 150 (t = 1/J):
- (a) **Trace.** tr_ℋT ≤ λ_h·[S_h(1 + c₁t + c₂t²) + E_tr], where S_h = 1/((1−x)(1−z)(1−y)) = 1.3301890167, and
  - N = 4: c₁ = 0.569629, c₂ = 0.425288, E_tr = 4.38·10⁻⁴;
  - N = 3: c₁ = 0.472683, c₂ = 0.339318, E_tr = 1.11·10⁻⁴.
  - At J = 150: tr_ℋT ≤ 1.335702λ_h (N = 4) and 1.334511λ_h (N = 3).
- (b) **Residual.** ‖(T − μ̂)ψ̂‖ ≤ ε_r·μ̂‖ψ̂‖ with ε_r = 1.9904·10⁻⁴ (N = 4) and 7.261·10⁻⁵ (N = 3). At J = 150 itself the bounds are 1.945·10⁻⁴ and 7.10·10⁻⁵.
- (c) **Gap.** λ₀ ≥ (1 − ε_r)μ̂ and λ₁ ≤ 0.332241μ̂ (N = 4), 0.331344μ̂ (N = 3). In particular λ₀ is simple and λ₁/λ₀ ≤ 0.3323.
- (d) **Vacuum error.** Let Ω₀ be the orthogonal projection of ψ̂ onto the λ₀-eigenline. Then ‖ψ̂ − Ω₀‖ ≤ 2.981·10⁻⁴‖ψ̂‖ (N = 4) and 1.086·10⁻⁴‖ψ̂‖ (N = 3).

**Proof of (c) and (d) from (a) and (b).**
- λ₀ ≥ ⟨ψ̂, Tψ̂⟩/‖ψ̂‖² = μ̂ + ⟨ψ̂, (T − μ̂)ψ̂⟩/‖ψ̂‖² ≥ (1 − ε_r)μ̂.
- T ≥ 0 is trace class on ℋ, so λ₁ ≤ Σ_{s≥1}λ_s = tr_ℋT − λ₀ ≤ tr_ℋT − (1 − ε_r)μ̂. Hence λ₁/μ̂ ≤ R_tr − 1 + ε_r with R_tr := sup_{J≥150} tr_ℋT/μ̂.
  - By (a) and m̂ ≥ 1, tr_ℋT/μ̂ ≤ S_h(1 + c₁t + c₂t²)/m̂(t) + E_tr. The first term increases in t on (0, 1/150], since c₁ > m₁ (checked on a 2001-point grid), so its supremum is attained at J = 150.
  - R_tr ≤ 1.332042 (N = 4) and 1.331271 (N = 3).
- Write ψ̂ = Ω₀ + e with e ⊥ Ω₀. Then (T − μ̂)ψ̂ = (λ₀ − μ̂)Ω₀ + (T − μ̂)e, and the two summands are orthogonal. On Ω₀^⊥ ∩ ℋ the spectrum of T lies in [0, λ₁], so (μ̂ − λ₁)‖e‖ ≤ ‖(T − μ̂)e‖ ≤ ε_rμ̂‖ψ̂‖.
- Therefore ‖e‖/‖ψ̂‖ ≤ ε_r/(1 − λ₁/μ̂) ≤ ε_r/(2 − R_tr − ε_r). ∎

**Proof of (a): the twisted one-column trace.**
- **Formula.** tr_ℋT = tr(P_ℋVK) = ∫dg∫dσ V(σ)K(σ, gσ), with g Haar on O(N).
  - Fix σ_M = e_N by invariance. Write g = r(p)k, where p = ge_N is uniform on S^{N−1}, r(p) is the rotation in span(e_N, p) taking e_N to p, and k is Haar on the stabilizer O(N−1).
  - The integrand is a class function of k.
  - N = 4: the SO(4)- and O(4)-invariant sectors coincide for three vectors in ℝ⁴. By Weyl's formula on SO(3), k is a rotation by α with weight (1 − cos α)/π on [0, π].
  - N = 3: the O(3) sector is the right one; the SO(3) sector also contains the pseudoscalar det(σ_T, σ_M, σ_B), and its trace is 1.436 instead of 1.330 at leading order. So k ∈ O(2): half rotations (α uniform) and half reflections (all conjugate).
- **Chart.** σ_r = (φ_r/√J, s_r) with s_r = √(1 − tX_r) (r = T, B), and p = (ζ/√J, c) with c = √(1 − tZ). The variables are y = (φ_T, φ_B, ζ) ∈ (ℝⁿ)³, n = N − 1.
  - Five bonds enter: the verticals J(s_r − 1), the middle horizontal J(c − 1), and two twisted bonds. For the twisted bonds the exact identity is
    σ_r·r(p)kσ_r = t·a₁ + s_r·t(a₂ − a₃) − t²a₂a₃/(1 + c) + c(1 − tX_r), with a₁ = φ_r·kφ_r, a₂ = φ_r·ζ, a₃ = kφ_r·ζ.
    It agrees with explicit rotation matrices to 10⁻⁴¹ (twrig2_check).
  - Each sphere variable carries the density (1 − tX)^{−1/2} (surface measure; Haar = uniform p × Haar k).
- **Harmonic part.** f₂ = −½yᵀQ_ky = −½[X_T + X_B + Z + |Mφ_T − ζ|² + |Mφ_B − ζ|²], with M = I − k. Put H(t, y) := (exact log-integrand) − f₂. Then
  tr_ℋT/λ_h = pref·∫dμ(k) det(Q_k)^{−1/2} E_k[e^H 1_Ω] + pref·(J/2π)^{3n/2}·∫_{Ω^c}(integrand, surface measures),
  - pref = (det_N/9)^{n/2}(det_D/6)^{−n/2}, the ratio of reduced Laplacian determinants of N and D;
  - Ω = {tX_T ≤ a, tX_B ≤ a, tZ ≤ a_Z}, with a = a_Z = 0.2.
  - Check of the normalization chain: pref·∫dμ det(Q_k)^{−1/2} = 1.3301890167 = S_h to 10 digits (32-point rule). S_h is the harmonic Σ_sλ_s/λ₀ in the invariant sector, Π_{i≤j}(1 − e^{−κ_i−κ_j})^{−1}; the invariants of two n-vectors of modes, n ≥ 2, are the three Gram entries.
- **Exact orders.** H = tH₁ + t²H₂ + O(t³), with
  - H₁ = ½(X_T + X_B + Z) − ⅛(X_T² + X_B²) − ⅜Z² + Σ_r[−½X_r(a₂r − a₃r) − ½a₂ra₃r + ½X_rZ];
  - H₂ = ¼(X_T² + X_B² + Z²) − (1/16)(X_T³ + X_B³) − (3/16)Z³ + Σ_r[−⅛X_r²(a₂r − a₃r) − ⅛a₂ra₃rZ + ⅛X_rZ²].
  - Check: (H − tH₁ − t²H₂)/t³ converges as t → 0 in 50-digit arithmetic (twrig3_check).
- **Majorants.** On Ω and uniformly in t′ ≤ t, |d^jH/dt′^j| ≤ h̄_j for j = 1, 2, 3, where
  h̄_j = Σ_r[(j−1)!X_r^j/(2(1−a)^j) + E_j(a)X_r^{j+1} + ½C_j(a)X_r^j(W_r + Z) + 2C_j(a_Z)X_rZ^j] + (j−1)!Z^j/(2(1−a_Z)^j) + 3E_j(a_Z)Z^{j+1}.
  - Notation: W_r = |Mφ_r|², C_j(x) = (2j−3)!!·2^{−j}(1−x)^{1/2−j} = |d^j/dx^j √(1−x)|, and E_j(x) = Σ_{m>j}c_m(m−1)!/(m−1−j)!·x^{m−1−j}, where √(1−x) = 1 − Σc_mx^m.
  - Sources of the terms:
    - the measure;
    - the vertical Z-anharmonics and three horizontal ones: the middle bond, plus the Z-part J(c − 1) + Z/2 of each twisted bond;
    - (s_r − 1)(a₂ − a₃), using |a₂ − a₃| = |ζ·Mφ_r| ≤ (Z + W_r)/2;
    - −t′a₂a₃/(1 + c) = −a₂a₃(1 − c)/Z and X_r(1 − c), using |a₂a₃| ≤ X_rZ.
  - Check: at 36 points × 3 values of t′ the ratios are ≤ 0.75 (twrig2_check, twrig3_check).
- **Tilt.** On Ω and for t′ ≤ t, H(t′) ≤ yᵀT_εy for every ε ∈ (0, 1), where
  yᵀT_εy = tc(a)(X_T + X_B) + tc(a_Z)Z + Σ_r[ε|Mφ_r − ζ|²/2 + (1/ε − 1)δ_κ²Z/2],
  with c(x) = −log(1−x)/(2x) and δ_κ = 1 − √(1−a) + √(aa_Z)/(1 + √(1−a_Z)).
  - Proof. J(B_r − 1) = −J|σ_r − gσ_r|²/2 ≤ −J|Π(σ_r − gσ_r)|²/2, where Π is the projection on e_N^⊥.
  - √J·Π(σ_r − gσ_r) = Mφ_r − κ_rζ with κ_r = s_r − t′a₃/(1 + c), and |1 − κ_r| ≤ δ_κ on Ω.
  - Then ½(|A|² − |A + B|²) ≤ ε|A|²/2 + (1/ε − 1)|B|²/2 with A = Mφ_r − ζ and B = (1 − κ_r)ζ.
  - The verticals and the middle bond are ≤ their harmonic parts, and the measure is ≤ tc(a)X. ∎
  - Properness. Q_k − 2T_ε = diag(1 − 2tc(a), 1 − 2tc(a), 1 − 2tc(a_Z) − 2(1/ε − 1)δ_κ²) + (1 − ε)·(twisted part). It is positive definite whenever 1 − 2tc(a_Z) − 2(1/ε − 1)δ_κ² > 0, which holds for ε ≥ 0.1 at a = 0.2. The code checks positive definiteness at every node.
  - The soft rotation mode of Q_k at α ≈ π is a null vector of the twisted part, so ε does not touch it. The first attempt, a region-constant tilt, failed exactly there.
  - Check: H(t′) − yᵀT_εy < 0 at every test point.
- **Bound on Ω.** Use e^x ≤ 1 + x + x²/2 + (x₊³/6)e^{x₊}, |H − tH₁| ≤ (t²/2)h̄₂, |H − tH₁ − t²H₂| ≤ (t³/6)h̄₃, and H₊ ≤ yᵀT_εy. On Ω this gives
  e^H ≤ 1 + tH₁ + t²P₂ + (t³/6)h̄₃ + (t³/2)|H₁|h̄₂ + (t⁴/8)h̄₂² + (1/6)(t|H₁| + (t²/2)h̄₂)³e^{yᵀT_εy}, where P₂ = H₂ + H₁²/2.
  - Polynomial part. E[(1 + tH₁ + t²P₂)1_Ω] ≤ 1 + tE H₁ + t²E P₂ + ‖tH₁ + t²P₂‖₂·P(Ω^c)^{1/2}, using −P(Ω^c) ≤ 0 and Chernoff for P(Ω^c).
  - The remaining terms are nonnegative, so they are bounded by their full expectations:
    - E|H₁|h̄₂ ≤ (E H₁²·E h̄₂²)^{1/2};
    - E[(…)³e^{yᵀT_εy}] = N_εE_ε[(…)³] ≤ N_ε(t(E_εH₁²·E_εH₁⁴)^{1/6} + (t²/2)(E_εh̄₂³)^{1/3})³, by Minkowski and Cauchy–Schwarz, with N_ε = (det Q_k/det(Q_k − 2T_ε))^{1/2}.
  - All moments are exact Gaussian moments of polynomials in the 9 quadratic forms. They come from gfmom.py (log-trace expansion plus the exponential recursion), which agrees with Monte Carlo and, on diagonal forms, with amom2 to 1.4·10⁻¹⁴.
  - ε is chosen per node from {0.1, 0.2, 0.3, 0.45, 0.6}; the optimum is 0.2–0.3.
- **Off Ω.** Drop both twisted bonds (each factor is ≤ 1). The integrand becomes a product of three one-variable weights e^{J(σ·e_N − 1)}.
  - (J/2π)^{n/2}∫_{S^{N−1}}e^{J(σ·e_N − 1)}dσ ≤ 1: at N = 4 because e^{−J}I₁(J) < (2πJ)^{−1/2}; at N = 3 it is exact.
  - The part outside the cap tX ≤ a is ≤ f(a) := √(2J/π)·e^{−J(1−√(1−a))} at N = 4 (using sin²θ ≤ sin θ), and ≤ e^{−J(1−√(1−a))} at N = 3.
  - So the off-Ω term is ≤ pref·[2f(a) + f(a_Z)].
- **Quadrature.** Periodic midpoint rule in α with 16 and 32 points. The two agree to 1.2·10⁻⁶ in the leading term and to 10⁻⁶ in the bound; the integrand is analytic and periodic, so the error decays geometrically. [Not interval-certified.]
- **Numbers at J = 150** (scratch/twrig3_N4_a20_M32.txt, twrig3_N3_a20_M32.txt):

| N | second-order value | tail | signed cubic | tilted cubic | off-Ω | bound |
|---|---|---|---|---|---|---|
| 4 | 1.335266 | 7.8·10⁻⁵ | 1.23·10⁻⁴ | 6.3·10⁻⁵ | 1.73·10⁻⁴ | 1.335702 |
| 3 | 1.334401 | 3.5·10⁻⁵ | 5.2·10⁻⁵ | 1.8·10⁻⁵ | 5·10⁻⁶ | 1.334511 |

- **Uniformity in J.** The second-order part S_h(1 + c₁t + c₂t²) is explicit; the moments do not depend on J. Each error term is nonincreasing in J:
  - the moment terms are t^k times unnormalized tilted expectations E[(positive polynomial)·e^{yᵀTy}], and the tilt depends on t only through tc(a)X ≥ 0;
  - the Chernoff terms are e^{−λJa}·E[e^{λX}];
  - the off-Ω term is √J·e^{−0.106J}, decreasing for J ≥ 5.
  - So E_tr(J) ≤ E_tr(150).

**Proof of (b): the vacuum residual** (scripts/vacrig11f.py; machinery of §18). All quantities below are in units of λ_h·main_D^{1/2}, so that ε_r = (√(near² + far_out) + gB)/(m̂√Z₂) with Z₂ = ⟨φ, Kφ⟩/main_D.
- **Setup.** (T − μ̂)ψ̂ = K^{1/2}g with g = VKφ − μ̂φ, so ‖(T − μ̂)ψ̂‖² = ⟨g, Kg⟩. This is a 4-column integral on G₄: the end columns carry the φ-couplings (a, a, b), there are three horizontal K's, and the two middle columns carry verticals.
- **Bad bonds.** Split g = g_G + g_B, where g_B(σ) = V(σ)∫K(σ, σ″)φ(σ″)1_bad dσ″, and "bad" means some horizontal bond σ_r–σ″_r makes an angle > δ = 40°.
  - ‖K^{1/2}g_B‖² ≤ sup|p|²·Σ_r e^{−θJ(1−cos δ)}Z_{G₄−r}, with θ = 0.95.
  - Z_{G₄−r}/main_{G₄−r} is bounded by Lemma 19.1 (K = 1). main_{G₄−r}/main_{G₄} is a determinant ratio. sup|p| ≤ 1 + Σ_i t^iΣ_β|q_{i,β}|(2J)^{deg β}.
  - gB = 1.88·10⁻⁵ (N = 4) and 1.44·10⁻⁵ (N = 3).
- **Good part.** Work on Ω_out = {all six middle vertices have |π_v| ≤ ρ_m = 0.55}, in the gauge S = centre of mass of the two middle columns.
  - Given σ, the end column σ″ is Gaussian with mean A⁻¹φ_σ and covariance A⁻¹, where A = I + L_tri.
  - E[L₁|σ] − m̂L₀(σ) = Σ_{k=2}^4 t^k r_k(σ) + δ₁(σ). Here r₁ ≡ 0 by the choice of q₁ and m₁; r₂ and r₃ come from vacres3N; r₄ comes from condexp2 at degree 8.
  - On the good set and Ω_out the end column stays in the chart: |π″| ≤ ρ″ = sin(arcsin ρ_m + δ) = 0.958.
  - |δ₁| ≤ (i) + (ii) + (iii) + (iv) + (v):
    - (i) Order-5 remainder: (t⁵/120)·E[D̄₅e^{c_e tΣX″}|σ] on Ω″ = {|π″_v| ≤ ρ_e = 0.6}. D̄₅ is the positive derivative majorant: measure, bond and p-factor majorants with radius constants (1−a_e)^{−k}, composed through Bell polynomials as in Lemma 19.1. The conditional law is tilted (A → A − 2c_e tI).
    - (ii) The L₀-side remainder: Σ_j|m_j|t^j·t^{5−j}/(5−j)!·D̄_{5−j}(L₀) at radius ρ_m.
    - (iii) The tail of the explicit polynomial T₄L₁ outside Ω″: Cauchy–Schwarz, then Chernoff on X″_v with λ ∈ {0.3, 0.45, 0.6}.
    - (iv) T₄L₁ on bad ∩ Ω″ ⊂ ∪_r{Q_rr″ > Jκ}, where κ = 2(1 − cos δ) − a²/(4(1 − a)) and a is the largest radius²: the Gaussian tail of Q_rr″.
    - (v) The annulus good \ Ω″: |L₁| ≤ π̄₀″·e^{c″tΣX″} at radius ρ″, then Chernoff on X″_v.
  - Each term is bounded in the outer weighted norm E[e^{c_m tΣ_SX}(·)²]^{1/2}, computed from Wishart moments of the Gram variables of σ.
    - This norm dominates the M-weighted norm: the Faddeev–Popov factor and the middle-bond anharmonics are ≤ 0, and the middle measure is ≤ e^{c_m tX}.
    - The form ⟨·, K·⟩ on Ω_out is then bounded by Cauchy–Schwarz for the positive weight M.
- **Outer far region** (some middle vertex beyond ρ_m). |g_G| ≤ VK|φ| + μ̂|φ| gives the 4-, 3- and 2-column integrals E4 + 2m̂·E3 + m̂²·ED with |p| majorants.
  - The chart part uses Chernoff in the S-gauge (λ ∈ {0.5, 1, 1.5}, p-majorants at radius ρ′ = 0.9).
  - Beyond ρ′ it uses the per-vertex energy, a θ-split and the tree bound.
- **Normalization.** Z₂ ≥ Σ_{k≤3}a_kt^k − B, by Lemma 19.1 with p at both ends:
  - N = 4: a_k = (1, 1.171955, 1.537725, 1.898528);
  - N = 3: a_k = (1, 0.823007, 0.776584, 0.780152).
- **Numbers at J = 150** (scratch/vacrig11_N4.txt, vacrig11_N3.txt):

| N | P | (i) D5 | (ii) R0 | (iii) tailX | (iv) tailB | (v) ann | gB | far_out | Z₂ ≥ | ε_r |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 2.64·10⁻⁶ | 1.64·10⁻⁴ | 4.3·10⁻⁶ | 4.2·10⁻⁶ | 3.8·10⁻¹⁰ | 1.2·10⁻⁶ | 1.88·10⁻⁵ | 7.2·10⁻¹¹ | 1.007875 | 1.945·10⁻⁴ |
| 3 | 1.13·10⁻⁶ | 5.20·10⁻⁵ | 1.9·10⁻⁶ | 1.3·10⁻⁶ | 1.3·10⁻¹⁰ | 6.3·10⁻⁷ | 1.44·10⁻⁵ | 5.2·10⁻¹⁷ | 1.005519 | 7.10·10⁻⁵ |

- **Uniformity in J ≥ 150** (scripts/vacmono.py, vacgap.py). Fix all radii at their J = 150 values. Then every term is one of:
  - t^k times an unnormalized tilted expectation of a positive polynomial, whose coefficients are polynomials in t with nonnegative coefficients (the degree trading tX ≤ a keeps an explicit t only where no variable is left);
  - a Chernoff factor e^{−λJa};
  - e^{−θJA}·(a polynomial in J of degree ≤ 1)·(a ratio of Bessel-type normalizations).
  - All of these are nonincreasing in J for J ≥ 150.
  - Norms of sums Σt^kX_k are replaced by Σt^k‖X_k‖ (Minkowski):
    - N = 4: nP 2.636 → 2.674·10⁻⁶ and tailX 4.24 → 7.47·10⁻⁶;
    - N = 3: nP 1.131 → 1.143·10⁻⁶ and tailX 1.34 → 2.57·10⁻⁶.
  - Denominators: m̂ ≥ 1, and Z₂ ≥ 1 − B(150) because all a_k > 0. This gives Z₂ ≥ 0.999993 (N = 4) and 0.999998 (N = 3).
  - Result: ε_r ≤ 1.9904·10⁻⁴ (N = 4) and 7.261·10⁻⁵ (N = 3) for all J ≥ 150. The inputs are upper roundings of the printed values, and gB is recomputed in vacgap.py.

**Flags for the reviewer.**
1. The normalization chain: pref and λ_h = main_N/main_D. The 10-digit identity with S_h is the check.
2. The α-quadrature is not interval-certified.
3. All evaluation is in floating point: moments from gfmom, amom2, wishart and condexp2.
4. The uniformity argument rests on the structure of each term, and on Minkowski where needed.
5. Pieces (i)–(v) of (b) use the majorant constructions of Lemma 19.1 (frozen, 8689b705), applied to the conditional problem.

**Files (sha8).**

| file | sha8 | file | sha8 |
|---|---|---|---|
| twlib.py | e5fd303c | twrig3_N4_a20_M32.txt | 8cdbec61 |
| twrig3.py | 5124f785 | twrig3_N3_a20_M32.txt | 7e2cda57 |
| twrig2_check.py | c7d3cb72 | twrig3_N4_a20_M16.txt | 5addc02a |
| twrig3_check.py | d98ac310 | twrig3_N3_a20_M16.txt | 0dea007b |
| gfmom.py | aafae8ce | twrig2_check_N4.txt / _N3.txt | e920e643 / 561d772a |
| gfmom_test.py | ed8a3171 | twrig3_check_N4.txt / _N3.txt | 3d71425c / 1202ec5f |
| vacrig11f.py | 9d57f823 | vacrig11_N4.txt / _N3.txt | 3c9d992f / 1e3e545a |
| vacmono.py | 67cb2324 | vacmono_N4.txt / _N3.txt | dba25ee6 / 4e31722f |
| vacgap.py | 09746c72 | vacgap_N4.txt / _N3.txt | 2a98ef95 / 2f157dc9 |
| vacres3N.py | 0aa22e03 | vacres_K3_N4.json / _N3.json | 516b2501 / ebcbd08c |
| condexp2.py | 36b2ea7d | condg.py | cad76714 |
| condpoly3.py | f6bd4b05 | wishart.py | 1efab7b4 |
| amom2b.py | cdc4d168 | riglap2.py | 0f9407a1 |
| npoly.py | 7c448ace | vacmod2.py | b323e7c6 |
| lapl2.py | aabd7c9f | pseries.py | e978732a |

**Next (§19.3).** The 10-state trial space: Gram and T matrices with insertions via Lemma 19.1, Ritz values, and τ_∞ ≤ tr_ℋT − Σ_{k≤9}μ_k (STRIPW Lemma 9.2 with p = 1; the trace bound above is the input). Harmonically τ_∞ ≈ 0.0098λ₀, against the cluster bottom 0.0436λ₀.

### 19.1a After review: RV12_3 confirms Lemma 19.1 (analytic part, with nits); the nits fixed; coverage stated (appended)
- **Review.** the RV12_3 FINAL (/mnt/g2/release/root/code/pk20/rv12/RV12_3_NOTES.md, 02e24777) confirms the analytic bounds of Lemma 19.1 with nits. It checked them line by line and found 0 violations in 118 tests against exact integrals. The numbers are double precision; RV12_3 §5 lists the 9 groups to redo in interval or exact arithmetic at assembly, and I adopt that list as the assembly checklist.
- **L1, the tilt hypothesis.** Add to the Statement of Lemma 19.1: *(H) L − 2t·diag(c_v) and L − 2t·c′I are positive definite on 1⊥.* B_rem needs the first and B_ann the second; without them the bound is void (+∞).
  - Code: scripts/riglap2b.py returns the exact a_k with +∞ remainders when (H) fails, where riglap2.bound crashed. riglap2.py stays unchanged (0f9407a1) because the frozen results use it, and (H) holds in all of them.
- **L2, wording.** The §19.1 caveat "exact recursions with nonnegative weights" is wrong. The amom2b recursion (D_j = (−2)^j det Γ_A) and the D_e = (X_u − X_v)² terms of D̄ are signed, so E_c[D̄], a_k and the norms are cancelling sums. Corrected caveat: the interval version is mechanical, but its widths must be checked. At assembly, D_e may be majorized by 2(X_u² + X_v²) to make D̄ all-positive, at most a factor 2 on B_rem.
- **L3, radii.** The tables use a_v = min(s*·L⁺_vv/J, 0.6), not s*·L⁺_vv/J. The cap matters: uncapped radii near 1 give valid but useless bounds (B_rem ≈ 10⁷ in RV12_3's test).
- **L4, coarea identity (now part of the Lemma).** In the centre-of-mass gauge with n̂ = Σσ/|Σσ|, the derivative of P_n̂^⊥Σσ along δn̂ ⊥ n̂ is −(Σ_v s_v)δn̂. So the Faddeev–Popov Jacobian is (Σ_v s_v)^{N−1}, giving FP = n·log(Σs_v/V) = n·log(1 − y) after normalization, and dσ_v = dπ_v/s_v in the hemisphere chart. Checks: a₀ = 1, and on trees a_k agrees with the exact asymptotic series to ≤ 10⁻¹³ (RV12_3).
- **Plan risk (RV12_3 L5).** The 3-column N = 4 bound without insertions is 1.9·10⁻⁵ at J = 120 and 4.1·10⁻⁶ at J = 150, and each dot insertion raises B_rem by 1.6–2.1×. So J₁ = 120 is not supported at N = 4. The vacuum (§19.2) closes at J = 150, and with a 2× margin at J = 170 (§19.2a). The realistic J₁ is 150–170, to be fixed in §19.3 once the trial-space integrals with insertions are priced.
- **Coverage, restated for the plan (§19.0).** Theorem S covers J ≥ J₁ only. The 3 × n middle range is certified only up to J = 3 (N = 4; N = 3 under review), so **[3, J₁] is uncovered**. That gap needs a separate certified computation, which §19 does not schedule. The statement "G2 for every pair on every 3 × n grid for J ≥ J₁, uniform in n" is complete in its own right, but it is not G2 for all J.

### 19.2a The N = 4 vacuum margin: what the 3·10⁻⁴ means, and the slack available (appended)
- **What 3·10⁻⁴ is.** It is a budget allocation, not a threshold. In the binding pair the vacuum error enters Cov as ≈ 0.25‖e₀‖/J², against a margin ≈ 5·10⁻⁴/J² (§18.1; both are estimates, to be fixed at assembly). So ‖e₀‖ = 2.98·10⁻⁴ uses ≈ 15% of the margin. The theorem depends on the total of all error terms at assembly (§19.6), not on the fourth digit of ‖e₀‖.
- **Slack by a slightly larger J₁** (scripts/vacscale.py, scratch/vacscale_N4.txt, vacscale_N3.txt). This is rigorous, from the J = 150 components and the monotone structure of each term at fixed radii:
  - nP (Minkowski) ≤ nP(150)·(150/J)²;
  - D5 and R0 ≤ (150/J)⁵ × their values (t⁵ times coefficients nondecreasing in t);
  - tailX and ann ≤ value × e^{−0.3a_e(J−150)/2} (Chernoff parameter λ ≥ 0.3);
  - gB ≤ gB(150)·(J/150)·e^{−0.95(1−cos 40°)(J−150)/2};
  - m̂ ≥ 1, Z₂ ≥ 1 − B(150), and tr/μ̂ nonincreasing.

| J | 150 | 160 | 170 | 175 | 200 |
|---|---|---|---|---|---|
| N = 4: ε_r ≤ | 1.99·10⁻⁴ | 1.37·10⁻⁴ | 9.80·10⁻⁵ | 8.41·10⁻⁵ | 4.31·10⁻⁵ |
| N = 4: ‖e₀‖/‖ψ̂‖ ≤ | 2.98·10⁻⁴ | 2.04·10⁻⁴ | 1.47·10⁻⁴ | 1.26·10⁻⁴ | 6.45·10⁻⁵ |
| N = 3: ‖e₀‖/‖ψ̂‖ ≤ | 1.09·10⁻⁴ | 7.03·10⁻⁵ | — | 4.14·10⁻⁵ | — |

  - So J₁ = 170 gives a 2× margin on the allocation at N = 4, with no new work. N = 3 has 2.8× at J = 150.
- **Slack by a better λ₁ (after §19.3).** The gap bound λ₁ ≤ Σ_{s≥1}λ_s = tr T − λ₀ is crude: it gives 0.332, while the true value is x ≈ 0.146. With the Ritz values of the 10-state space (μ_k ≤ λ_k), λ₁ ≤ tr T − μ₀ − Σ_{k=2}^{9}μ_k ≈ (0.146 + 0.010 + O(t))λ₀. With a cap of 0.17 this gives ‖e₀‖ ≤ 2.40·10⁻⁴ at J = 150, 1.64·10⁻⁴ at 160 and 1.18·10⁻⁴ at 170 (scratch/vacscale_N4_lam16.txt).
- **Not a lever: the trace remainder.** The trace bound is within 4.4·10⁻⁴ of its exact second-order value, so tightening it changes λ₁/μ̂ in the fourth digit only.
- **Recommendation.** Plan J₁ = 170 at N = 4 (J₁ = 150 at N = 3), and use the Ritz λ₁ once §19.3 is done; that leaves margin for the interval pass. The rest of §19 is priced at J = 170 unless the integrals with insertions in §19.3 force more.

### 19.3 The binding pair in the bulk for all J ≥ 170, N = 3 and 4 [proved by the author, modulo floating-point evaluation (moments, quadrature) and review of the new Lemma 19.1c; independent review needed] (scripts/riglap5s.py, binding4.py, binding5.py, twrig4.py, assemble_binding_unif4.py)

**Answer first.**
- **Proposition 19.3.** In the bulk of the 3 × ∞ strip (infinite-volume Gibbs state, both sides carried by the vacuum), for every J ≥ 170, with a = top–middle vertical of column j and b = middle–bottom vertical of column j+1:
  - Cov(σ_a, σ_b)·J² ≥ 1.177·10⁻⁴ at N = 4 (the true value is ≈ c₂ + c₃/J ≈ 4.77·10⁻⁴);
  - Cov(σ_a, σ_b)·J² ≥ 2.204·10⁻⁴ at N = 3 (the true value is ≈ 3.05·10⁻⁴ at J = 170).
  - This is the binding pair of the whole strong-coupling theorem, with channel cancellation ρ = 0.0123 (§9).
- **Three new ingredients:**
  - an exact identity that removes the residual norm ‖Q_Pv‖ altogether (flip symmetry plus Bessel);
  - the eigen trick, which turns the odd norm into 2-column integrals;
  - Lemma 19.1c, a third-order-exact Laplace bound that is 20–50× sharper than Lemma 19.1 for these integrals.
- **Not covered here:** positions near the ends of finite strips (left/right states other than Ω₀), and all other pair types. The plan for both is in 19.3.7.

#### 19.3.1 Why the 10-state space was dropped (finding)
- The harmonic trial basis reproduces the invariant-sector spectrum exactly: Ritz ratios 1, x, z, y, x², xz, z² = xy (degenerate), zy, y² (scratch/ts_N4_J170_D_S.json).
- The six 4-phonon states cannot be resolved by Laplace bounds. Their K-normalized polynomials are rough: the L² norm per column is ≈ 20–30, with coefficients up to 64. Every remainder bound scales with the product of the L² norms, while the entry itself is O(1).
  - Example: the Gram bound for entry (9,9) is 0.33 at J = 170 (scratch/ts_radii_D_N4.txt).
  - This is intrinsic to the approach, not a tuning issue.
- **Consequence:** route V′ is run with P = {ψ̂, the three cluster states}. τ_∞ (needed only for separated pairs) will come from a Hilbert–Schmidt bound with P = 4 states: ‖QTQ‖² ≤ tr T² − Σ_{k≤3}μ_k² = 0.0264²λ₀² at harmonic order, below y² = 0.0436².

#### 19.3.2 Lemma 19.1c: third-order-exact Laplace bounds with a refined quartic remainder [proved by the author; review needed]
- **Setting.** As Lemma 19.1, for insertions given as products of column factors (column polynomials p(ξ) in ξ_uv = J(1 − σ_u·σ_v), trial polynomials, dot products).
- **Statement.** I/main = Σ_{k≤3}a_kt^k + R, where a_k = Σ_{i+j=k}E_γ[F_iE_j] exactly, and |R| ≤ B_rem + B_tail + B_ann + B_far.
  - Notation: E₀ = 1, E₁ = H₁, E₂ = H₂ + H₁²/2, E₃ = H₃ + H₁H₂ + H₁³/6; F_i are the Taylor coefficients of the insertion F(τ).
- **Proof of the bound on Ω**, uniformly in t′ ≤ t:
  - (a) e^H = Σ_{m≤3}H^m/m! + ρ₄(H), with |ρ₄(x)| ≤ x⁴e^{x₊}/24 and H₊ ≤ Σ_v c_vtX_v (Lemma 19.1's tilt).
  - (b) Write H = Σ_{k≤4}t^kH_k + R₅ with |R₅| ≤ t⁵h̄₅/120, D₃ := H − tH₁ − t²H₂ with |D₃| ≤ t³h̄₃/6, and E₂′ := H − tH₁ with |E₂′| ≤ t²h̄₂/2 (h̄_k are Lemma 19.1's derivative majorants). Then
    R_E := e^H − Σ_{j≤3}t^jE_j = R₄H + ½(t⁴H₂² + D₃² + 2tH₁D₃ + 2t²H₂D₃) + (1/6)(3t²H₁²E₂′ + 3tH₁E₂′² + E₂′³) + ρ₄(H),
    where R₄H = t⁴H₄ + R₅, 2tH₁D₃ = 2t⁴H₁H₃ + 2tH₁R₄H, and 3t²H₁²E₂′ = 3t⁴H₁²H₂ + 3t²H₁²D₃.
  - (c) So the O(t⁴) part of |R_E| is bounded by exact signed polynomials (|H₄|, H₂², |H₁H₃|, H₁²|H₂|). Majorants enter only at O(t⁵): h̄₅, |H₁H₄|, |H₂|h̄₃, H₁²h̄₃, |H₁|h̄₂², h̄₂³, h̄₃², |H₁|h̄₅.
  - (d) F e^H = Σ_{k≤3}t^k(Fe^H)_k + Σ_{i+j≥4}t^{i+j}F_iE_j + F_{≤3}R_E + R_Fe^H, with |R_F| ≤ t⁴F̄₄/24 (Lemma 19.1's insertion majorants).
  - (e) Expectations:
    - E|F_{≤3}R_E| ≤ ‖F_{≤3}‖₂·Σ(L² norms of the R_E pieces). The pieces are X-only polynomials; norms are exact up to degree 18 in the vertex forms (amom2b), with Hölder per monomial beyond that (only O(t⁶) terms).
    - The ρ₄ term: N_cE_c[|F|C⁴] ≤ N_c·min(‖F‖_{2,c}‖C‖_{8,c}⁴, ‖F‖_{4,c}‖C‖_{6,c}⁴), with C = t|H₁| + (t²/2)h̄₂ and degree trading (t²/2)h̄₂ ≤ tĥ on Ω where needed.
    - ‖F₀‖₂ is computed exactly from joint moments. ‖F_i‖ for i ≥ 1 and the norms of F̄₄ use Hölder over the column groups.
  - (f) Tail, annulus and far terms are as in Lemma 19.1, with Hölder over groups. In the tail, hypercontractivity is used for the t^{≥1} terms.
- **Checks.** Exact integrals (edge with dot insertions; path P₃ with column polynomials including the non-edge pair, at couplings (1,1) and the lopsided (1, 0.3)), J = 40–170: 26 cases at N = 4 and 26 at N = 3, 0 violations (scratch/riglap5s_test_N{4,3}.txt).
- **Sharpness at J = 170** (graph N, s = 80): rE drops from 1.97·10⁻⁴ (Lemma 19.1-type majorants) to 8.5·10⁻⁶. Amplitude integrals carry relative errors 0.12–0.3% on the 3-column graph and 10⁻⁵–10⁻⁴ on the 2-column graph.

#### 19.3.3 The exact structure of the binding covariance
- **(i) Route V′.** In the bulk, Cov(σ_a, σ_b) = ⟨v_a, v_b⟩ with v_X = Q₀T_XΩ₀/λ₀ (§17.2), where T_X = K^{1/2}XVK^{1/2} and X = σ_u·σ_v of the edge.
  - Write X = 1 − tξ_X. Since Q₀TΩ₀ = 0, v_X = −tQ₀T_ξΩ₀/λ₀ with T_ξ = K^{1/2}ξ_XVK^{1/2}. This is the choice c̄ = 1, which removes every residual term from the amplitudes.
- **(ii) Flip symmetry.** b is the top–bottom flip F of a, and FΩ₀ = Ω₀, so v_b = Fv_a. Hence
  Cov = ⟨v_a, Fv_a⟩ = ‖v⁺‖² − ‖v⁻‖², with v^± the flip-even and flip-odd parts of v_a.
- **(iii) Bessel.** For any orthonormal flip-even u_x, u_y: ‖v⁺‖² ≥ |⟨u_x, v_a⟩|² + |⟨u_y, v_a⟩|². No residual norm ‖Q_Pv‖ is needed.
- **(iv) The odd part, exactly.** v⁻ = −tQ₀K^{1/2}δVK^{1/2}Ω₀/λ₀, with δ = (ξ_TM − ξ_MB)/2 on the middle column. It is automatically orthogonal to Ω₀.
- **(v) Eigen trick.** With ψ̂ = K^{1/2}φ and the residual function g = VKφ − μ̂φ (§19.2): K^{1/2}wVK^{1/2}ψ̂ = μ̂K^{1/2}wφ + K^{1/2}wg for any multiplier w. Hence
  ‖K^{1/2}δVK^{1/2}ψ̂‖² = 2μ̂⟨δφ, KδVKφ⟩ − μ̂²⟨δφ, Kδφ⟩ + ⟨δg, Kδg⟩.
  - So ‖v^{tr,−}‖²/t² = (2I_N/m̂ − N_δ)/g₀₀ + ε_δ², with:
    - I_N = ⟨δφ, KδVKφ⟩/main_N (3 columns) and N_δ = ⟨δφ, Kδφ⟩/main_D (2 columns);
    - ε_δ = ‖K^{1/2}δg‖/(μ̂‖ψ̂‖) ≤ [√((c_ξJ/2·near)² + J²far) + J·gB]/√Z₂, where c_ξ = 4(1 − √(1 − ρ_m²)) = 0.6594.
  - The ε_δ bound holds because |δ| ≤ c_ξJ/2 on the near region of §19.2 and |δ| ≤ J everywhere, and the §19.2 bounds control ‖K^{1/2}|g|‖ (all of them are bounds for positive kernels or Cauchy–Schwarz in the near region).
  - The same identity with w = ξ_a gives ‖v^tr‖.
- **(vi) Vacuum error.** Write û = cΩ₀ + sw with s ≤ ε_r/(2 − R_tr − ε_r) (Lemma 19.2) and f(Ω) = Q_ΩBΩ with B = T_ξ, β = ‖B‖_op. Then
  ‖f(Ω₀) − f(û)‖ ≤ ‖Ω₀ − û‖(β + ⟨û,Bû⟩ + 2‖Bû‖ + β‖Ω₀ − û‖), and |Cov(Ω₀) − Cov(û)| ≤ ‖Δ‖(2‖v^tr‖ + ‖Δ‖).
  - β is bounded by the 2×2 block bound λ_max[[α, ‖b‖], [‖b‖, tr B − α]] in the decomposition (û, û^⊥), with α = ⟨û,Bû⟩, b = Q_ûBû, and ‖Q_ûBQ_û‖ ≤ tr(B) − α since B ≥ 0.
  - tr_ℋT_ξ comes from twrig4, the twisted trace with the positive insertion ξ_a = X_T/(1 + s_T) (scheme of §19.2, all moments of degree ≤ 8): tr T_ξ ≤ 1.312607λ_h at N = 4 and 0.942262λ_h at N = 3 (J = 170). This gives β ≤ 0.912μ̂ (N = 4) and 0.645μ̂ (N = 3).

#### 19.3.4 The computed inputs (J = 170, radii a_v = min(80G_vv/J, 0.6), ρ′ = 0.7)
- **Gram** (graph D) g_αβ for α, β ∈ {ψ̂, e₁, e₂, e₃}. Off-diagonal entries between odd e₂ and the even states vanish by symmetry. Errors 10⁻⁵–1.7·10⁻⁴.
- **Raw amplitudes** A_α = ⟨φ_α, Kξ_aVKφ⟩/main_N (graph N, three insertion groups). Relative errors:
  - N = 4: 1.8·10⁻⁵, 1.2·10⁻³, 1.2·10⁻³, 3.0·10⁻³;
  - N = 3: 1.0·10⁻⁵, 5.9·10⁻⁴, 6.1·10⁻⁴, 1.6·10⁻³.
  - The b-amplitudes equal the a-amplitudes for even states and their negatives for e₂, which checks the flip symmetry.
- **Eigen-trick 2-column integrals** reproduce A_α/m̂ to 10⁻⁶ (scratch/binding3_N4_J170.json), a check of (v).
- **Central values at J = 170, N = 4:** a_x/t = +0.1049, a₂/t = −0.1325, a_y/t = −0.0838. Then Cov·J² = a_x² − a₂² + a_y² = 4.768·10⁻⁴, which matches c₂ + c₃/J = 4.77·10⁻⁴ from the data (§9). This checks the whole set-up.

#### 19.3.5 Uniformity in J ≥ 170
- Fix all radii at their J = 170 values. Every Lemma 19.1c remainder is then nonincreasing in J (t^k times unnormalized tilted expectations with coefficients nondecreasing in t; Chernoff factors; far terms of the form (polynomial in J)·e^{−cJ}). The central values are explicit polynomials in t.
- ε_r(J) and s(J) come from the monotone scaling of the §19.2 components (vacscale). Two decays are added to it:
  - the bad-bond tail tailB(J) decays as √chi_tail(Jκ/vq_r) (scripts/vq_tailB.py);
  - the far term decays as (J/150)²e^{−0.151(J−150)}.
- J·ε_r(J) is nonincreasing for J ≥ 150, which controls ε_δ and ε_a.
- The assembly is evaluated with t as an interval on 481 log-spaced subintervals (ratio 1.01) up to J = 2·10⁴, plus [2·10⁴, ∞).
- **Result:** the lower bound is positive on every subinterval. The minimum is at J ∈ [170, 171.7]:
  - N = 4: Cov·J² ≥ 1.1765·10⁻⁴;
  - N = 3: Cov·J² ≥ 2.2043·10⁻⁴.
  - (scratch/assemble_unif4_N{4,3}.txt)
- **Error budget at J = 170, N = 4** (t² units; margin 4.77·10⁻⁴):

| item | size |
|---|---|
| even and odd amplitude errors | ≈ 1.4·10⁻⁴ |
| odd-norm residual ε_δ² | ≈ 3·10⁻⁵ |
| vacuum term | 1.98·10⁻⁴ (s = 1.46·10⁻⁴) |

  - The vacuum term falls below 3·10⁻⁵ by J = 250. So J₁ is set by the vacuum residual, as in §19.2.

#### 19.3.6 Flags for the reviewer
1. Lemma 19.1c is new. Check (a)–(f), the degree trading in the ρ₄ term, and the Hölder exponents over groups.
2. The weighted-residual bound ε_δ (19.3.3 (v)): the §19.2 near-region bound applies to |g| (Cauchy–Schwarz with the positive weight M), and c_ξ is the geometric sup of ξ_uv/J on the near region.
3. The vacuum Lipschitz bound and the 2×2 block bound for β.
4. All arithmetic is floating point, apart from the final interval assembly, which is done in mpmath interval arithmetic on floating-point inputs.
5. Scope: bulk only. Finite strips need the boundary states; other pair types need W1/W2 and τ_∞.

#### 19.3.7 Next
- **(a) Ends.** Near an end the left state is T^{j−1}b (free end column), not Ω₀. Expected route: the same flip/Bessel structure with the oblique (2×2-minor) form of §17.2, with explicit end-column integrals. Positions j ≥ j₀ reduce to the bulk with corrections ≲ 0.146^{j−1}.
- **(b) The other pair types** need only O(1/J)-accurate data (§9). This requires the cluster eigen-data (P = 4 Ritz problem), τ_∞ through tr T² (a 2-column twisted trace), and W1/W2.
- **(c) Interval versions of everything** at assembly (RV12_3 §5 list).

**Files (sha8).**

| file | sha8 | file | sha8 |
|---|---|---|---|
| riglap3.py | a9c049f1 | riglap5_test.py | be42ca28 |
| riglap4.py | f451e2d2 | riglap5s_test.py | 97f5545f |
| riglap5.py | c6d2a4d9 | riglap4_test_N4.txt | 7c62e3b7 |
| riglap5b.py | 99b20f19 | riglap5_test_N4.txt | 89d80c52 |
| riglap5c.py | 6b647d85 | riglap5s_test_N4.txt / _N3.txt | b41f8b36 / 2d0a29b8 |
| riglap5e.py | 1039532e | twrig4.py | 585e655b |
| riglap5r.py | 05a5a601 | twrig4_N4_a25.txt / _N3_a25.txt | bad58875 / bf8608b2 |
| riglap5s.py | fd62f8ca | binding5.py | f09c0427 |
| binding4.py | 3309733d | b5_N4_J170.json / b5_N3_J170.json | f19d1e08 / 567f5543 |
| order0_basis.py | 2a53a12b | binding4_N4_J170.json / _N3_J170.json | 46a47036 / f5e90b08 |
| assemble_binding.py | 1fa84e2b | assemble_N4_J170.txt | 74c734e4 |
| assemble_binding_unif4.py | 8e25c204 | assemble_unif4_N4.txt / _N3.txt | c1a0fc55 / 600ee8bf |
| vq_tailB.py | dfb86121 | ts_N4_J170_D_S.json / ts_N3_S.json | d6d104ea / 26e20e76 |
| trial_space.py | f22c6818 | ts_N4_J170_D.json / ts_radii_D_N4.txt | ef601e0e / 2d7793dd |

### 19.2b After review: RV12_7 confirms Lemma 19.2 (analytic part, with nits); answers (appended)
- **Review.** the RV12_7 FINAL (/mnt/g2/release/root/code/pk20/rv12/RV12_7_NOTES.md, 92d7a23f) confirms the analytic part of Lemma 19.2 with nits. The numbers are not certified; RV12_7 §5 lists them for the interval pass.
- **N1, the 3·10⁻⁴.** Agreed. The "≲ 3·10⁻⁴" in §19.2 misquotes §18.1, where 3·10⁻⁴ was a budget share for ε_r. The covariance itself needs only ‖e₀‖ ≲ 2·10⁻³. §19.3 does not use any allocation: it feeds the actual vacuum term (1.98·10⁻⁴·t² at J = 170, N = 4) into the interval assembly.
- **N2, D5 first.** At J₁ = 170 the D5 term is (150/170)⁵ ≈ 0.53 of its J = 150 value. The vacuum term takes ≈ 40% of the binding margin in §19.3, so D5's signed float moments must be right to ≈ 1%. They are first on the interval list.
- **Minor items:**
  - **sup|p|² is of degree 2 in J.** This is consistent with §19.2's uniformity step: gB is linear in sup|p| ≤ (J/150)·sup|p|(150), so gB² carries (J/150)², and both are killed by e^{−0.111(J−150)}.
  - **Monotonicity, one line.** f(t) = (1 + c₁t + c₂t²)/m̂(t) has f′ = num/m̂² with
    num = (c₁ − m₁) + 2(c₂ − m₂)t − 0.3448t² − 0.1510t³ − 0.0564t⁴ (N = 4), and (c₁ − m₁) = 0.1586, 2(c₂ − m₂) = 0.4218.
    So num ≥ 0.1586 − 0.56t² > 0 for t ≤ 1/150. For N = 3: num ≥ 0.1088 − 0.53t² > 0. (scratch/tmp/fcheck.py)
  - **The Bessel citation is no longer needed.** With u = 1 − cos θ, ∫₀^π e^{−J(1−cos θ)}sin²θ dθ = ∫₀² e^{−Ju}√(u(2−u))du ≤ ∫₀^∞ e^{−Ju}√(2u)du = √(π/2)·J^{−3/2}. Hence (J/2π)^{3/2}·4π·(that integral) ≤ 1 exactly. Numerically the ratio is 0.9975 at J = 150.
  - **α-quadrature.** For the interval pass, the periodic trapezoid error is bounded by 4πM_β/(e^{Mβ} − 1) on a strip |Im α| < β where det Q_k(α) stays away from 0. The soft mode at α ≈ π fixes β, which will be read off the closed form of det Q_k(α) (blocks with m = 2(1 − cos α)). Recorded as an open certification item.

### 19.4 The two-column twisted trace and the spectral separation τ_∞ < λ_y for J ≥ 170 [proved by the author, modulo floating-point evaluation (moments, quadrature); independent review needed] (scripts/twlib2.py, twrig6.py/twrig6z.py, cluster_T.py, tau_inf3.py, tau_inf_unif.py)

**Answer first.**
- Let P₄ = span{ψ̂, e₁, e₂, e₃} (vacuum and the three cluster states), Q₄ = 1 − P₄, and τ_∞ := ‖Q₄TQ₄‖.
- **Corollary 19.4.** For every J ≥ 170: τ_∞ < μ_y ≤ λ_y, where μ_y is the lowest cluster Ritz value of P₄ and λ_y the corresponding eigenvalue. The ratios are:

| N | at J = 170 | worst ratio for J ≥ 170 |
|---|---|---|
| 4 | τ_∞ ≤ 0.0396λ_h, μ_y ≥ 0.0425λ_h (ratio 0.933) | ≤ 0.983 |
| 3 | τ_∞ ≤ 0.0312λ_h, μ_y ≥ 0.0431λ_h (ratio 0.725) | ≤ 0.769 |

- So the complement starts strictly below the cluster, as STRIPW Lemma 4.3 needs. The N = 4 margin is thin. It is enough for the eigenvector bounds if the coupling c = ‖Q₄TP₄‖ is O(10⁻³)λ₀, which is the size the cluster residuals should have (19.4.4).
- The one-column trace bound fails in the flip-even sector (0.043 against y = 0.0436). The input that makes the difference is the new **Lemma 19.4**, a rigorous bound for tr_ℋT² from a two-column twisted trace.

#### 19.4.1 Lemma 19.4 (two-column twisted trace) [proved by the author; review needed]
- **Formula.** tr_ℋT² = tr(P_ℋVKVK) = ∫dg∫dσ¹dσ² V(σ¹)K(σ¹,σ²)V(σ²)K(σ², gσ¹).
  - Fix σ¹_M = e_N and write g = r(p)k (k a class-function variable on the stabilizer: SO(3) with weight (1 − cos α)/π at N = 4; O(2), half rotations and half reflections, at N = 3).
  - Chart variables y = (φ₁, φ₂, φ₃, φ₄, φ₅, ζ) for col-1 T and B, col-2 T, M and B, and p.
  - Ten bonds: col-1 verticals (root–1, root–2); horizontals 1–3, root–4, 2–5; col-2 verticals 3–4, 4–5; twisted 3–g1, 4–p, 5–g2.
- **Exact twisted bond.** σ′·r(p)kσ = t[φ′·kφ − t(kφ·ζ)(φ′·ζ)/(1 + c) + s(φ′·ζ) − s′(kφ·ζ)] + css′. All bonds that do not involve k have anharmonic parts depending only on the X's: A(X_u, X_v) = −(t/2)(X_u − X_v)²w(tX_u, tX_v).
- **Forms:** X₁, …, X₅, Z, a_T = φ₃·ζ, b_T = kφ₁·ζ, a_B = φ₅·ζ, b_B = kφ₂·ζ.
- **The series** H = Σ_k t^kH_k is built programmatically from the bond formulas. Check: (H − tH₁ − t²H₂ − t³H₃)/t⁴ converges in 50-digit arithmetic against explicit rotation matrices (twlib2_check, N = 4 and N = 3).
- **Normalization.** tr T²/λ_h² = pref²·∫dμ(k)det(Q_k)^{−1/2}E_k[e^H 1_Ω] + (off-Ω terms). Check: pref²·∫dμ det(Q_k)^{−1/2} = 1.0302393041 = Π_{i≤j}(1 − e^{−2(κ_i+κ_j)})^{−1} = 1/((1−x²)(1−z²)(1−y²)) to 10 digits, at both N.
- **Bound on Ω** (scheme of Lemma 19.1c without insertion): third order exact,
  E[e^H1_Ω] ≤ 1 + Σ_{k≤3}t^kE[E_k] + (tail) + E|R_E|.
  - R_E = R₄H + ½(t⁴H₂² + D₃² + 2tH₁D₃ + 2t²H₂D₃) + (1/6)(3t²H₁²E₂′ + 3tH₁E₂′² + E₂′³) + ρ₄(H).
  - Majorants h̄_j (polynomials in the X's and Z) come from the bond-wise derivative bounds: Lemma 19.1's for the pair bonds; E_j for root bonds and Zanh. The three-variable part J(css′ − 1) + (X + X′ + Z)/2 is decomposed as A(X, X′) + Zanh + t(X + X′)Z/4 − t(X + X′)Zanh/2 − tZA/2 + tA·Zanh, with C_j-bounds for the cross terms.
  - Majorant ratios ≤ 0.60 at 48 test points (j = 1, 2, 3; N = 3, 4).
  - Tilt for ρ₄: the projected-distance bound for the twisted bonds 3–g1 and 5–g2 (κ = s − tb/(1 + c)); every other bond is bounded by its harmonic part.
- **Off Ω:**
  - A graded annulus: shells Ω_{i−1} ⊂ Ω_i up to radius a′, each shell bounded by the tilt valid at its outer radius, with Chernoff in the tilted law.
  - A far region beyond a′: the twisted bonds 3–g1 and 5–g2 are dropped (≤ 1). The global projection bound J(σ_u·σ_v − 1) ≤ −½|φ_u − φ_v|² holds for all other bonds, including 4–p. Add the density tilt on {tX ≤ 0.96} and a factor 2⁶ for the hemispheres.
  - An equatorial piece (some tX_v > 0.96) by the tree-path energy.
- **Numbers at J = 170** (radii² 0.2 for col-1, 0.3 for col-2 and Z; annulus to (0.45, 0.55) in 3 shells; 16-point α-rule):

| N | bound on tr T²/λ_h² | third-order value | R_E | ρ₄ | annulus | tail | far |
|---|---|---|---|---|---|---|---|
| 4 | 1.0360403 | 1.0353894 | 1.3·10⁻⁴ | 4.5·10⁻⁴ | 5.8·10⁻⁵ | 8·10⁻⁶ | 6·10⁻⁷ |
| 3 | 1.0349174 | 1.0347582 | 5.1·10⁻⁵ | 9.5·10⁻⁵ | 1.1·10⁻⁵ | 3·10⁻⁶ | 4·10⁻⁸ |

  - ρ₄ carries the tilt's normalization N_ε ≈ 3–7. That is the floor of this scheme at J = 170 for N = 4: a radius scan found nothing better than 6.5·10⁻⁴.

#### 19.4.2 τ_∞ by Hilbert–Schmidt
- ‖Q₄TQ₄‖² ≤ tr((Q₄TQ₄)²) = tr T² − 2‖Q₄TP₄‖²_HS − Σ_kμ_k² ≤ tr T² − Σ_kμ_k², where μ_k are the Ritz values of P₄.
- Σμ_k² is bounded below in interval arithmetic. Take the central G_c-orthonormal Ritz vectors U, form M = UᵀGU and A = UᵀTU as interval matrices (Gram from graph D, T from graph N, Lemma 19.1c), apply an interval Cholesky M = LLᵀ, and set A′ = L⁻¹AL⁻ᵀ. Then Σμ_k² = ‖A′‖_F² ≥ Σ_i(A′_ii)²_low.
  - A global Weyl bound was too crude: the y-state's T-error leaks into μ₀.
- **Ritz enclosures at J = 170** (Gershgorin discs of A′):
  - N = 4: μ₀ ∈ [1.002310, 1.002541], μ_x ∈ [0.14595, 0.14715], μ_z ∈ [0.07982, 0.08042], μ_y ∈ [0.04246, 0.04524].
  - N = 3: [1.00209, 1.00220], [0.14608, 0.14669], [0.07988, 0.08018], [0.04305, 0.04449].
- **Uniformity in J ≥ 170.** Radii are fixed at J = 170, so the remainders of tr T² and of the matrix entries are nonincreasing in J. The central values are polynomials in t. The interval evaluation runs over 2400 subintervals (ratio 1.002) up to J = 2·10⁴, plus [2·10⁴, ∞) (scratch/tau_unif3_N{4,3}.txt).

#### 19.4.3 For (C): what J₁ the present tools allow
- **Vacuum residual (§19.2, Lemma 19.1-type majorants).** J₁ ≈ 150–170 at N = 4. A Lemma 19.1c-type refinement of its order-5 conditional remainder (expected ≈ 10–20×, as for the integrals) would move the vacuum to J ≈ 100.
- **Binding amplitudes (Lemma 19.1c, graph N).** Errors scale like t⁴: about 1.4·10⁻⁴·t² of the 4.77·10⁻⁴ margin at J = 170, but 8.4× more at J = 100, which exceeds the margin. Fourth-order exactness (≈ 5× sharper) would be needed for J ≈ 100–120.
- **τ_∞ (Lemma 19.4).** The tr T² excess scales like t⁴; at J = 100 it is ≈ 5·10⁻³ at N = 4, which fails. Fourth order or a cheaper tilt would be needed. N = 3 has 3× more room.
- **Summary.**
  - With the present tools, J₁ ≈ 150–170.
  - With fourth-order versions everywhere plus a refined vacuum residual, J₁ ≈ 100–120.
  - J₁ ≈ 50–75 is out of reach of term-by-term Laplace bounds: the remainder constants grow ≈ 10× per order while t gains only ≈ 1/50 per order at J = 50, so higher orders stop helping. It needs (C), the collective coordinate for the rotation mode, or a different expansion.

#### 19.4.4 Next
- **c = ‖Q₄TP₄‖ from the cluster Ritz residuals.**
  - The vacuum part is ε_r (known).
  - For each cluster state, the residual g_i = VKφ_i − μ_iφ_i is O(t). It splits into t·r_{1,i}·φ_harm (explicit, via the conditional expansion of §18, order 1 only) plus an order-2 remainder (crude majorants are enough: c is needed only to a factor ≈ 2).
  - ‖K^{1/2}(r_{1,i}φ)‖² is a 2-column integral.
  - Then STRIPW Lemmas 4.3–4.4 give eigenvalues and eigenvectors of the cluster.
- **Then the ends** (the boundary state's overlaps with the cluster, plus complement decay τ_∞^{j−1}), **then W1/W2.**

**Files (sha8):** twlib2.py 32a4e216, twlib2_check.py 3567b818 (outputs N4 04706d5f, N3 bee5c675), twrig6.py eb816b61, twrig6z.py 27145c31 (twrig6_N4_J170.txt 1eba1e14, twrig6z_N3.txt d5052d81), twrig5.py 936a849c, twrig5b.py 521d9b4c (second-order versions, superseded), cluster_T.py 112622a4 (clT_N4_J170.json cfd2ab7c, clT_N3_J170.json 7d62c303), tau_inf3.py 09d69789 (tau_inf3_N4_J170.txt c7b06f60, _N3 3d5aca25), tau_inf_unif.py 6d43a587 (tau_unif3_N4.txt 742779b6, _N3 33265ef5).

### 19.4a Can a collective-coordinate (spin-wave) treatment bring J₁ to ≤ 35? (the question; assessment, no new computation)
- **Answer: doubtful by this route.** Low confidence for J₁ ≤ 35 by a collective coordinate added to the present Laplace/majorant scheme. A credible attempt is weeks of work, not days. A realistic reach is J₁ ≈ 80–120: medium confidence, ≈ 1–2 weeks.
- **Method (what (C) would be).** Introduce, for each column, its rigid rotation relative to the neighbouring column as a collective coordinate g ∈ SO(N), and integrate it exactly with Haar measure; the twisted traces of §19.2–§19.4 already do this for the trace. Expand only the "shape" fluctuations (relative angles inside a column) in t = 1/J. Keep the third- or fourth-order-exact remainder scheme (Lemma 19.1c), the graded tilt shells, and the eigen trick.
- **Main obstacle: the remainder constants grow faster than t shrinks.**
  - All present remainders scale like t⁴–t⁵ times fixed majorant moments. At J = 170 they already use 25–70% of the binding margin: the amplitude errors are 0.12–0.3%; the vacuum term takes ≈ 40% of the margin; τ_∞/μ_y = 0.93.
  - Going to J = 35 multiplies them by (170/35)⁴⁻⁵ ≈ 550–2800. The exact series are tame, for example ⟨E₁⟩, ⟨E₂⟩, ⟨E₃⟩ = 0.85, 0.64, 0.50 for tr T², so the true remainders at J = 35 are tiny (≈ t⁴·O(1) ≈ 10⁻⁶). The loss is entirely in the rigorous majorants, which exceed the true coefficients by 10³–10⁵.
- **What the collective coordinate buys.** The relative rotation is ≈ 1/3 of the end column's conditional variance (§18.1), the source of the 10–15× growth per order of the inner Taylor coefficients. Removing it should cut the growth to ≈ 6–8× per order, a gain of ≈ 10–50× at order 4–5. That is far short of the 10³ needed.
- **Two further walls at J = 35:**
  - (i) Tails. Chernoff tails ≲ 10⁻⁶ at J = 35 need chart radii a ≈ 0.8, where the majorant region constants (1 − a)^{−k} ≈ 5.9^k explode. The graded shells help only while the tilted Gaussians stay narrow.
  - (ii) More exact orders. Recovering 10³ by order count needs K ≈ 8, since each order gains only Ct ≈ 12/35 ≈ 0.3. That means exact Gaussian moments of degree ≈ 22 in 15–17 forms, beyond the engines (degree ≤ 10 in 16 forms, ≤ 18 in 9 X-forms).
- **What could reach J ≈ 35:** a rigorous cluster (polymer) expansion around the spin-wave Gaussian with a large-field/small-field split and explicit constants. The strip helps here: the gap is O(1) (λ₁/λ₀ ≈ 0.146 uniformly in J), and the per-bond anharmonicity t·X² ≈ 0.03–0.15 at J = 35 is small. But this is a new framework in the style of constructive field theory: several weeks, low-to-medium confidence.
- **N = 3 vs N = 4.** N = 3 is 2–3× easier in every remainder (twrig6: 1.6·10⁻⁴ against 6.5·10⁻⁴), which does not change the picture.
- **Consequence for the 3 × n route.** With the strong-coupling side at J₁ ≈ 80–120 and the review at ≈ 35, the gap [35, 80–120] stays open unless the cover can be extended. The memory grows like L⁵ with L ≈ √(44J), about 10× from 35 to 100, so a large-memory machine could do it. That is the call, not a recommendation to create one.

### 19.5 All vertical pairs in the bulk for J ≥ 170, N = 3 and 4 [proved by the author, modulo floating-point evaluation (moments, quadrature) and review of Lemma 19.1c and of the new Lemma 19.5w; independent review needed] (scripts/pairs_m2.py, pairs_m2b.py, pairs_m0b.py, vacrig11w.py, vacw_mink.py, m2_unif3.py, m0_unif.py)

**Answer first.**
- Every pair of vertical bonds in the bulk of the 3 × ∞ strip has Cov ≥ 0 for all J ≥ 170, at N = 3 and N = 4. With the binding pair (Prop. 19.3) this finishes item (1) of the plan.
- **Same-type pairs** (T–M with T–M, M–B with M–B, any separation): Cov = ⟨v, S^{m−1}v⟩ ≥ 0 because T ≥ 0. This holds for every J.
- **Flip pairs** (T–M in column j, M–B in column j + m):

| m | result (J ≥ 170) | where |
|---|---|---|
| 0 | Cov·J² ≥ 1.563·10⁻² (N = 4), 1.069·10⁻² (N = 3) | Prop. 19.5a |
| 1 | Cov·J² ≥ 1.177·10⁻⁴ (N = 4), 2.204·10⁻⁴ (N = 3) | Prop. 19.3 |
| ≥ 2 | Cov_m·J² ≥ Cov₁·J²·ρ^{m−1} > 0 | Prop. 19.5b |

- Prop. 19.5b rests on one inequality, R⁺ ≥ ρ, between a Rayleigh quotient of the even part and a bound on the top odd eigenvalue. It holds with ratio ≥ 1.133 (N = 4) and ≥ 1.203 (N = 3), worst at J = 170.
- No cluster residual c is needed.
- **New ingredient: weighted vacuum residuals** (Lemma 19.5w). At J = 170, N = 4:
  - ε_w̃ ≤ 8.87·10⁻⁴ and ε_δ ≤ 4.70·10⁻⁴;
  - the sup-weight bounds of §19.3 give 1.10·10⁻² and 5.49·10⁻³, about 12 times larger.

#### 19.5.1 Setting
- Notation as in §19.2–§19.4: u = Ω₀ is the normalized top eigenvector of T on ℋ, λ₀ its eigenvalue, and S = T/λ₀.
  - û = ψ̂/‖ψ̂‖ = cu + s·y, with y ⊥ u a unit vector, c > 0, s ≤ s_vac (Lemma 19.2(d)), and sp := ‖u − û‖ = s·√(2/(1 + c)).
  - T_f = K^{1/2}fVK^{1/2} for a multiplier f on one column.
  - ξ_rs = J(1 − σ_r·σ_s), ξ^± = (ξ_TM ± ξ_MB)/2, δ := ξ⁻. The flip F (T ↔ B) commutes with T, and Fu = u.
- **Covariance.** As in §19.3.3(i), with v^± = Q₀T_{ξ^±}u/λ₀:
  Cov(T–M at j, M–B at j + m)·J² = ⟨v⁺, S^{m−1}v⁺⟩ − ⟨v⁻, S^{m−1}v⁻⟩ for m ≥ 1.
  - v⁺ is flip-even and v⁻ is flip-odd. Both are orthogonal to u.
  - For every constant k̄, v⁺ = Q₀T_{w̃}u/λ₀ with w̃ = ξ⁺ − k̄, since Q₀Tu = 0. We take k̄ = ⟨ξ⁺φ, Kφ⟩/⟨φ, Kφ⟩ at J = 170, which makes ⟨û, K^{1/2}w̃φ̂⟩ = 0 at the central value.
- **Parity of the trial objects.** The trial vacuum and the cluster states are used in their flip-symmetrized form.
  - The stored coefficients (vacres_K3_N{3,4}.json, order0_basis) agree with their symmetrizations to 10⁻¹².
  - The computed cross-parity Gram entries are ≤ 10⁻¹¹.
  - Both are far below the error bars, which are ≥ 10⁻⁶.

#### 19.5.2 Lemma 19.5r (reduction for m ≥ 2) [proved]
- Let λ₁^o be the top of T on the odd sector, ρ_odd = λ₁^o/λ₀, and R⁺ = ⟨v⁺, Sv⁺⟩/‖v⁺‖².
- If R⁺ ≥ ρ ≥ ρ_odd, then for every m ≥ 2:
  Cov_m·J² ≥ ‖v⁺‖²(R⁺)^{m−1} − ‖v⁻‖²ρ_odd^{m−1} ≥ (‖v⁺‖² − ‖v⁻‖²)ρ^{m−1} = Cov₁·J²·ρ^{m−1}.
- **Proof.**
  - Even part: Jensen for the spectral measure ν of v⁺ under S, since x ↦ x^{m−1} is convex on [0, ∞): ∫x^{m−1}dν ≥ ν(1)(∫x dν/ν(1))^{m−1}.
  - Odd part: 0 ≤ S ≤ ρ_odd on the odd sector.
  - Cov₁ = ‖v⁺‖² − ‖v⁻‖² is the binding pair (§19.3.3(ii)), which is positive by Prop. 19.3. ∎
- **Why it works.**
  - v⁻ lives almost entirely on the odd 2-phonon mode z, with λ_z ≈ 0.080λ₀.
  - v⁺ splits between x (≈ 0.146λ₀) and y (≈ 0.044λ₀). The binding amplitudes of §19.3.4 give weights ≈ 0.61 and 0.39, so R⁺ ≈ 0.106.
  - The trial value I3p/(N_w m̂) = 0.10633 agrees with this.

#### 19.5.3 The odd radius by Hilbert–Schmidt [proved]
- Let U ≥ tr_ℋT²/λ_h² be the bound of Lemma 19.4.
- Let μ₀ ≥ μ_x ≥ μ_y be the Ritz values of the even cluster block {ψ̂, e₁, e₃} (pencil of §19.4.2, interval Cholesky), and μ_z the odd 1 × 1 block {e₂}.
- Interlacing in each parity sector gives λ₀ ≥ μ₀, λ₁^e ≥ μ_x, λ₂^e ≥ μ_y and λ₁^o ≥ μ_z. Since tr T² ≥ λ₀² + (λ₁^e)² + (λ₂^e)² + (λ₁^o)²:
  - (λ₁^o)² ≤ U − S2_even, where S2_even = Σ_{i∈even}(A′_ii)₋² ≤ Σ_even μ_k² (diagonal of the orthonormalized Ritz matrix A′, lower ends);
  - (λ₁^e)² ≤ U − μ₀² − μ_y² − μ_z², with lower ends: μ₀ ≥ max_i A′_ii, μ_y ≥ the lowest Gershgorin end of the even block, μ_z = A′_zz.
- **Bounds used.**
  - The top of T on u^⊥, of either parity, is λ₁ ≤ L₁ := max of the two square roots. Numerically L₁ is the even one, ≈ 0.152λ_h.
  - ρ := √(U − S2_even)/λ₀,low with λ₀,low = max(μ₀, m̂(1 − ε_r)). At J = 170, ρ ≤ 0.0900 (N = 4) and 0.0864 (N = 3); harmonically λ_z = 0.0797.

#### 19.5.4 The lower bound on R⁺ [proved]
- **Eigen trick in the T-norm.** T_{w̃}û = μ̂h + e with h = K^{1/2}w̃φ̂, e = K^{1/2}w̃ĝ, φ̂ = φ/‖ψ̂‖ and ĝ = g/‖ψ̂‖ (§19.3.3(v)). Write x = T_{w̃}u = (T_{w̃}û − sT_{w̃}y)/c, so that v⁺ = Q₀x/λ₀ and R⁺ = ‖Q₀x‖_T²/(λ₀‖Q₀x‖²), with ‖z‖_T² := ⟨z, Tz⟩.
- **Numerator.**
  - ‖Q₀z‖_T² = ‖z‖_T² − λ₀⟨u,z⟩².
  - ‖μ̂h + e‖_T² ≥ μ̂²⟨h,Th⟩ − 2μ̂|⟨e,Th⟩|, dropping ⟨e,Te⟩ ≥ 0.
  - |⟨e,Th⟩| ≤ ‖e‖(λ₁^{1/2}‖h‖_T + λ₀|⟨u,h⟩|). Split h along u, use Cauchy–Schwarz for the form of T on u^⊥, and ‖Q₀e‖_T ≤ λ₁^{1/2}‖e‖.
  - The vacuum part: s‖Q₀T_{w̃}y‖_T ≤ sλ₁^{1/2}‖T_{w̃}‖.
- **Denominator.** ‖Q₀x‖ ≤ (‖T_{w̃}û‖ + s‖T_{w̃}‖)/c, with the odd-norm identity of §19.3.3(v) for w = w̃:
  ‖T_{w̃}û‖²/μ̂² = (2I_p3/m̂ − N_w)/g₀₀ + ε_w̃².
  The factors c cancel in the ratio.
- **Operator norm.** −k̄T ≤ T_{w̃} ≤ T_{ξ⁺}, and ‖T_{ξ⁺}‖ ≤ β (the 2 × 2 block bound of §19.3.3(vi), twrig4). So ‖T_{w̃}‖/μ̂ ≤ B_op := max(β, k̄(1 + ε_r)).
- **Result** (μ̂ units, λ_h = 1):
  R⁺ ≥ [√NT2 − s√(L₁/m̂)·B_op]₊² / ((1 + ε_r)(D_n + s·B_op)²), where
  - NT2 = H_T − 2ε_w̃[√(L₁H_T/m̂) + (1 + ε_r)u_h] − (1 + ε_r)u_a²;
  - H_T = I3p/(g₀₀m̂) and D_n² = (2I_p3/m̂ − N_w)/g₀₀ + ε_w̃²;
  - u_h = |k_n − k̄g₀₀|/g₀₀ + sp√(N_w/g₀₀);
  - u_a = |A_0w|/(m̂g₀₀) + sp·D_n.
- **The integrals.**
  - D graph: g₀₀ = ⟨φ, Kφ⟩, k_n = ⟨ξ⁺φ, Kφ⟩, N_w = ⟨w̃φ, Kw̃φ⟩.
  - N graph: I3p = ⟨w̃φ, KVKw̃φ⟩, I_p3 = ⟨w̃φ, Kw̃VKφ⟩, A_0w = ⟨φ, Kw̃VKφ⟩.
  - All are normalized by main_D or main_N and bounded by Lemma 19.1c (riglap5s; radii a_v = min(80G_vv/J, 0.6), ρ′ = 0.7).
  - Checks: I_p3 = m̂N_w to 7 digits (N = 4: 0.018210185 against 0.018210178). A_0w and ⟨φ, KVKw̃φ⟩ vanish at the central value, which checks the eigen trick and k̄.

#### 19.5.5 Lemma 19.5w: weighted residuals [proved by the author; review needed] (scripts/vacrig11w.py)
- **Statement.** Let w be a multiplier on the residual column. Suppose that on Ω_out (§19.2(b)) |w| ≤ |ℓ| + B, where ℓ and B ≥ 0 are polynomials in the Gram variables of σ; that |w| ≤ c_wJ on Ω_out; and that |w| ≤ W_wJ everywhere. Then
  ε_w := ‖K^{1/2}wg‖/(μ̂‖ψ̂‖) ≤ (√(near_w² + (W_wJ)²far_out) + W_wJ·gB)/(m̂√Z₂),
  near_w = Σ_P(‖ℓP‖ + ‖BP‖) + c_wJ(tailX + tailB + ann).
  - The sum runs over the three polynomial pieces P of §19.2(b): the explicit part Σ_{k=2}^4t^kr_k, the order-5 term (i) after the conditional expectation, and the L₀-side remainder (ii).
  - The norms are the outer weighted norm of §19.2(b), evaluated exactly by Wishart moments. tailX, tailB, ann, gB and far_out are the unweighted pieces of §19.2(b).
- **Proof.**
  - Use the decomposition g = g_G + g_B of §19.2(b). The K-seminorm satisfies Minkowski.
  - On Ω_out, Cauchy–Schwarz for the positive weight M gives ⟨wg_G, Kwg_G⟩ ≤ E_M[w²R²] ≤ E_outer[w²R²], where R is the normalized residual function. Then |R| ≤ Σ|pieces| and |w| ≤ |ℓ| + B, and Minkowski applies.
  - The inner tails and the annulus use sup_{Ω_out}|w|.
  - The bad-bond part and the outer far region use sup|w|, by positivity of the kernel. ∎
- **The weights.** The chart identity
  ξ_rs = Q_rs/2 + J·f(tX_r, tX_s), with f(u, v) = (√(1−u) − √(1−v))²/2 = (u − v)²/(2(√(1−u) + √(1−v))²) ∈ [0, (u − v)²/(8(1 − a_m))] on Ω_out,
  gives:
  - for w̃: ℓ = (Q_TM + Q_MB)/4 − k̄, B = t[(X_T − X_M)² + (X_M − X_B)²]/(16(1 − a_m)), c_w = c_ξ, W_w = 2;
  - for δ: ℓ = (Q_TM − Q_MB)/4, the same B, c_w = c_ξ/2, W_w = 1.
- **Numbers at J = 170** (scratch/vacrig11w_N{4,3}_J170.txt; the run also recomputes ε_r at J = 170 directly: 9.33·10⁻⁵ at N = 4, 3.12·10⁻⁵ at N = 3):

| N | w | ε_w | sup-weight form | near_w | bad-bond part W_wJ·gB |
|---|---|---|---|---|---|
| 4 | w̃ | 8.87·10⁻⁴ | 1.10·10⁻² | 1.11·10⁻⁴ | 7.78·10⁻⁴ |
| 4 | δ | 4.70·10⁻⁴ | 5.49·10⁻³ | 8.27·10⁻⁵ | 3.89·10⁻⁴ |
| 3 | w̃ | 6.32·10⁻⁴ | 3.89·10⁻³ | 3.96·10⁻⁵ | 5.96·10⁻⁴ |
| 3 | δ | 3.25·10⁻⁴ | 1.95·10⁻³ | 2.82·10⁻⁵ | 2.98·10⁻⁴ |

  - The bad-bond part, with the sup weight, now dominates. A weighted version (w² inserted into Z_{G₄−r}) would remove most of it; this is not needed here.
- **Uniformity.** For J ≥ J₀ = 170:
  near_w(J) ≤ nPw_M(J₀)(J₀/J)² + (D5w + R0w)(J₀)(J₀/J)⁵ + c_wJ·tails(J).
  - nPw_M is the per-order (Minkowski) form, from vacw_mink.py: 3.47·10⁻⁶ (N = 4) and 1.27·10⁻⁶ (N = 3).
  - tails(J) is the scaled unweighted tail of §19.3.5, and the far and bad-bond terms carry (W_wJ)² and W_wJ.
  - Each term is nonincreasing for J ≥ 170: the polynomial weights are J-independent up to B ∝ t; J·e^{−0.054(J−150)}, J⁴e^{−0.151J} and J²e^{−0.111J} all decrease there.

#### 19.5.6 Prop. 19.5b (flip pairs, m ≥ 2) [proved by the author; review needed] (scripts/m2_unif3.py)
- For N ∈ {3, 4} and every J ≥ 170: R⁺_low(J) ≥ ρ(J). By Lemma 19.5r, Cov_m·J² ≥ Cov₁·J²·ρ^{m−1} > 0 for every m ≥ 2.
- Evaluation: mpmath intervals in t on 481 log-spaced subintervals (ratio 1.01) up to J = 2·10⁴, plus [2·10⁴, ∞).
  - Central values are polynomials in t, with the Lemma 19.1c remainders fixed at J = 170.
  - ε_r, s and ε_w̃ come from the scalings of §19.3.5 and §19.5.5, evaluated at the left end of each subinterval.
  - U is from Lemma 19.4, and the Ritz data are recomputed on each subinterval as in tau_inf_unif.

| N | worst R⁺_low/ρ | where | R⁺ ≥ | ρ ≤ | J → ∞ |
|---|---|---|---|---|---|
| 4 | 1.1329 | J ∈ [170, 171.7] | 0.10191 | 0.08995 | 1.173 (0.10508 vs 0.08956) |
| 3 | 1.2026 | J ∈ [170, 171.7] | 0.10391 | 0.08640 | 1.226 |

- Budget at J = 170, N = 4: the cross term costs 3.95% of H_T (with the scaled ε_w̃ = 1.61·10⁻³; the direct value at J = 170 would give 2.2%). Vacuum terms with s cost < 0.1%, and the trial-integral error bars ≈ 1.3%.

#### 19.5.7 Prop. 19.5a (same-column flip pair) [proved by the author; review needed] (scripts/pairs_m0b.py, m0_unif.py)
- **Formula.** Cov(X_TM, X_MB)·J² = Cov(ξ_TM, ξ_MB) = E_u[f₂] − E_u[w̃]², where:
  - f₂ = (ξ_TM − k̄)(ξ_MB − k̄) = w̃² − δ²;
  - E_u[f] = ⟨u, T_fu⟩/λ₀;
  - E[ξ_TM] = E[ξ_MB] by flip symmetry.
- **Bound.**
  - ⟨u, Fu⟩ ≥ ⟨û, Fû⟩ − sp(2‖Fû‖ + ‖F‖·sp), with F = T_{f₂}.
  - ⟨û, Fû⟩ = μ̂A_f/(m̂g₀₀) (N graph, middle insertion).
  - ‖Fû‖/μ̂ ≤ √(N_f/g₀₀) + ε_f, by the eigen trick and the triangle inequality, with the sup weights (c_ξJ)² and (2J)² in ε_f (crude is enough).
  - ‖F‖ ≤ 2Jβμ̂ + k̄²λ₀, because −T_{δ²} ≤ F ≤ T_{w̃²}, w̃² ≤ 2Jξ⁺ + k̄², δ² ≤ Jξ⁺ and ‖T_{ξ⁺}‖ ≤ βμ̂.
  - |E_u[w̃]| is controlled by A_0w and B_op as in §19.5.4.
- **Inputs at J = 170:**

| N | A_f | N_f |
|---|---|---|
| 4 | 0.016264487 ± 2.5·10⁻⁵ | 0.002340576 ± 1.7·10⁻⁵ |
| 3 | 0.010836912 ± 8.9·10⁻⁶ | 0.001214830 ± 3.0·10⁻⁶ |

- **Result** (same uniform scheme as §19.5.6): Cov₀·J² ≥ 1.5629·10⁻² (N = 4) and 1.0690·10⁻² (N = 3) for all J ≥ 170, worst at J = 170. The vacuum terms are ≤ 4.6·10⁻⁴ there, against a trial value of 0.0157.

#### 19.5.8 Inputs at J = 170 (scratch/m2_N{4,3}_J170.json.b, .b.m0)

| item | N = 4 | N = 3 |
|---|---|---|
| g₀₀ | 1.006947449 ± 1.6·10⁻⁶ | 1.004868248 ± 7.3·10⁻⁷ |
| k_n (k̄ = k_n/g₀₀) | 0.832885937 ± 2.0·10⁻⁶ (0.827139427) | 0.554110405 ± 7.1·10⁻⁷ (0.551425927) |
| N_w | 0.018166127 ± 2.3·10⁻⁶ | 0.012067991 ± 6.7·10⁻⁷ |
| N_δ | 0.017686280 ± 1.5·10⁻⁶ | 0.011758430 ± 4.4·10⁻⁷ |
| I3p = ⟨w̃φ, KVKw̃φ⟩ | 0.001936303 ± 9.8·10⁻⁶ | 0.001284278 ± 3.0·10⁻⁶ |
| I3m = ⟨δφ, KVKδφ⟩ | 0.001417067 ± 6.6·10⁻⁶ | 0.000941057 ± 2.1·10⁻⁶ |
| I_p3 | 0.018210185 ± 2.5·10⁻⁵ | 0.012093904 ± 8.6·10⁻⁶ |
| A_0w | 0 ± 8.9·10⁻⁶ | 0 ± 3.6·10⁻⁶ |
| ⟨φ, KVKφ⟩ | 1.009389591 ± 9.6·10⁻⁶ | 1.007025962 ± 4.6·10⁻⁶ |

- I3m is not used by the proof. It gives the direct m = 2 check: ⟨v⁺,Sv⁺⟩ ≈ 1.92·10⁻³ against ⟨v⁻,Sv⁻⟩ ≈ 1.41·10⁻³ at N = 4.

#### 19.5.9 Flags for the reviewer
1. Lemma 19.5w is new: the chart identity for ξ_rs, the Minkowski split |w| ≤ |ℓ| + B inside the outer norm, and the sup weights for the remaining pieces.
2. Lemma 19.5r: Jensen, and the use of the same v^± as in Prop. 19.3.
3. §19.5.3: interlacing per parity sector needs exactly flip-even and flip-odd trial spaces. We use the symmetrized coefficients, which differ from the stored ones by 10⁻¹².
4. §19.5.4: the T-norm Cauchy–Schwarz on u^⊥ with λ₁ ≤ L₁ (both parities), and the operator sandwich for T_{w̃}.
5. Uniformity: the left-end evaluation relies on each scaled term being nonincreasing in J. For ‖F‖ in Prop. 19.5a the factor J is taken at the right end; on the last interval we use that J·sp(J)² is nonincreasing.
6. All arithmetic is floating point, except the final interval assembly (mpmath intervals on floating-point inputs).

#### 19.5.10 Next
- (2) Ends with j ≥ 8, then (3) the residual engine for c and small j, then (4) horizontal edges (the order).
- Open from RV12_7: the α-strip bound for the quadratures.
- For (C): at J = 170 the m ≥ 2 margin is 13%, and m = 0 has a factor ≈ 30 to spare. The binding pair (m = 1) still sets J₁.

**Files (sha8).**

| file | sha8 | file | sha8 |
|---|---|---|---|
| pairs_m2.py | c9c18669 | m2_N4_J170.json.b / _N3 | 7c0d4316 / 55da99fd |
| pairs_m2b.py | ad303222 | m2_N4_J170.json.b.m0 / _N3 | 3d296279 / 68b2821a |
| pairs_m0b.py | c82b4fe2 | vacrig11w_N4_J170.txt / _N3 | d6038475 / 9baf04a4 |
| vacrig11w.py | aad478e7 | vacw_mink_N4_J170.txt / _N3 | 9a6e5f24 / c1d500be |
| vacw_mink.py | 0ded3db6 | m2_unif3_N4.txt / _N3 | 91f6f1a4 / 643b702d |
| m2_unif3.py | af526dd3 | m0_unif_N4.txt / _N3 | ba792e17 / 98181781 |
| m0_unif.py | d8cc5f60 | | |

### 19.6 Vertical pairs near the ends (finite 3 × n strips, free boundary) for J ≥ 170 [proved by the author, modulo floating-point evaluation; independent review needed] (scripts/endw.py, endpairs4.py)

**Answer first.**
- **The same-column flip pair is positive everywhere, for every J and every n**, by site reflection positivity through the middle row (Lemma 19.6a). This is elementary. It supersedes the computation in Prop. 19.5a, which remains as a check.
- **All other vertical pairs with both bonds away from the ends** have Cov ≥ 0 for J ≥ 170, at every separation m ≥ 1, in every strip (Prop. 19.6). "Away" means:

| pairs | N = 4 | N = 3 |
|---|---|---|
| flip pairs (T–M at j, M–B at j′) | 6 ≤ j and j′ ≤ n − 5 | 5 ≤ j and j′ ≤ n − 4 |
| same-type pairs | 3 ≤ j and j′ ≤ n − 2 | 3 ≤ j and j′ ≤ n − 2 |

  - Here j < j′ are the columns, and column 1 and column n are the end columns.
  - This covers the plan's item (2) (ends with j ≥ 8) with room to spare.
- **Two mechanisms.**
  - For short separations the bulk bound (Jensen, §19.5) absorbs the end corrections.
  - For long separations a top-mode decomposition is used: the overlap of v⁺ with the exact top even excited eigenvector e_x is bounded below through Hilbert–Schmidt alone, with no cluster residual. Every term then decays at the same exact rate λ₁^e/λ₀.
- **Remaining for (3):** vertical pairs with a bond within 5 columns of an end at N = 4 (4 at N = 3) for flip pairs, or within 2 columns for same-type pairs.

#### 19.6.1 Lemma 19.6a (site reflection positivity through the middle row) [proved; elementary]
- Let θ exchange the T and B rows and fix the M row. Write H = H₊ + θH₊, where H₊ collects the T-row horizontals, the T–M verticals and half of each M-row horizontal.
- For f depending on the T and M rows, ⟨f·θf⟩ = Z⁻¹∫dσ_M F_f(σ_M)², with F_f(σ_M) = ∫dσ_T e^{H₊}f. This is ≥ 0.
- With f = Σ_j c_j(X_TM(j) − ⟨X_TM(j)⟩), the matrix C_jj′ = Cov(X_TM(j), X_MB(j′)) is positive semidefinite, using ⟨X_MB(j)⟩ = ⟨X_TM(j)⟩.
- In particular C_jj ≥ 0 for every J > 0, every n, every N, and also for any flip-symmetric column-dependent couplings. ∎

#### 19.6.2 The finite-strip covariance
- Z = ⟨w, T^{n−2}w⟩ with the boundary vector w = K^{1/2}V·1 (§19.4.4).
- For bonds at columns 2 ≤ j < j′ ≤ n − 1 with m = j′ − j:
  - the left state is T^{j−2}w = ⟨u,w⟩λ₀^{j−2}(u + ε_L);
  - the right state is T^{n−j′−1}w = ⟨u,w⟩λ₀^{n−j′−1}(u + ε_R);
  - ‖ε_L‖ ≤ e_L := R_wρ₁^{d_L}, with d_L = j − 2, d_R = n − j′ − 1, R_w = ‖Q₀w‖/|⟨u,w⟩| and ρ₁ = λ₁/λ₀ (w is even, so ε_L ∈ even ∩ u^⊥).
- With centred insertions B_X = (T_ξ − cT)/λ₀ (c the bulk mean), p_X = B_Xu (the vector v of §19.5), a = B_X(u + ε_L), b = B_Y(u + ε_R) and D = 1 + ⟨ε_L, S^{m+1}ε_R⟩, the exact identity is
  Cov_fin·J²·D = ⟨Q₀a, S^{m−1}Q₀b⟩ + ⟨a,u⟩⟨u,b⟩(1 − 1/D) − [⟨a,u⟩⟨ε_L, S^mQ₀b⟩ + ⟨Q₀a, S^mε_R⟩⟨u,b⟩ + ⟨Q₀a, S^mε_R⟩⟨ε_L, S^mQ₀b⟩]/D,
  with ⟨a,u⟩ = ⟨ε_L, p_X⟩ and ⟨u,b⟩ = ⟨p_Y, ε_R⟩.
- **Flip pairs:** B_Y = FB_XF. Parity splits the main term:
  ⟨Q₀a, S^{m−1}Q₀b⟩ = ⟨a⁺, S^{m−1}b⁺⟩ − ⟨a⁻, S^{m−1}b⁻⟩, with a^± = v^± + (B^±ε_L) (projected on u^⊥), and B⁺ is the same for X and Y.
- **R_w** (endw.py; 2-column integrals with the free end column, verticals (1, 1)):
  - q = |⟨û,w⟩|/‖w‖ satisfies q² = I_mix²·r_main/(g₀₀I_free), and R_w² ≤ 1/(q − sp)² − 1.
  - J = 170: q² = 0.965685 (N = 4) and 0.976901 (N = 3), so R_w ≤ 0.1896 and 0.1544.

#### 19.6.3 Short separations: Jensen perturbation [proved]
- **Flip pairs.**
  - main ≥ C_m − ‖v⁺‖_m(η⁺_L + η⁺_R) − η⁺_Lη⁺_R − ‖v⁻‖_m(η⁻_L + η⁻_R) − η⁻_Lη⁻_R.
  - Here ‖z‖_m² = ⟨z, S^{m−1}z⟩, ‖v⁺‖_m ≤ ρ₁^{(m−1)/2}‖v⁺‖, ‖v⁻‖_m ≤ ρ^{(m−1)/2}‖v⁻‖, η⁺ = ρ₁^{(m−1)/2}‖B⁺‖e and η⁻ = ρ^{(m−1)/2}‖B⁻‖e.
  - C₁ ≥ Cov₁ (Prop. 19.3), and C_m ≥ ⟨v⁺,Sv⁺⟩R₊^{m−2} − ⟨v⁻,Sv⁻⟩ρ^{m−2} for m ≥ 2.
- **Same-type pairs.** main ≥ P(P − 2η) − η², with P ≤ ‖p_X‖_m from ‖p_X‖_m ≥ ‖v⁺‖_m.
- **Inputs.**
  - ⟨v⁻,Sv⁻⟩ ≤ (μ̂³/c²λ₀³)[√(H_δ + 2ε_δ√(ρ′H_δ) + ρ′ε_δ²) + s√ρ′·β/2]², with H_δ = I3m/(g₀₀m̂) and ρ′ = √(U − S2_even)/m̂.
  - ‖B⁺‖ ≤ max(β, c⁺(1 + ε_r))/(1 − ε_r) and ‖B⁻‖ ≤ β/(2(1 − ε_r)).
- The second-order terms are bounded as written, with ‖S^mε‖ ≤ ρ₁^m‖ε‖.

#### 19.6.4 Long separations: the top even mode [proved by the author; review needed]
- **Simplicity.** λ₁^e (the top of T on even ∩ u^⊥) is simple: λ₂^e ≤ L₂ < μ_x.
  - L₂² = U − μ₀² − μ_x² − μ_z², by Hilbert–Schmidt with tr T² ≥ λ₀² + (λ₁^e)² + (λ₂^e)² + (λ₁^o)².
  - μ_x is bounded below by the smaller eigenvalue of the (vac, x) principal 2 × 2 of the even Ritz matrix (interlacing).
- **Overlap with e_x.** Let u_x be the cluster state e₁ orthonormalized against ψ̂ (the basis of Prop. 19.3), and x′ = Q₀u_x/‖Q₀u_x‖.
  - Its Rayleigh quotient satisfies q_x′ ≥ ⟨u_x, Tu_x⟩ − λ₀sp², and q_x′ ≤ α²λ₁^e + (1 − α²)λ₂^e, so α² := ⟨x′, e_x⟩² ≥ (q_x′ − L₂)/(L₁ − L₂).
  - Hence |⟨v⁺, e_x⟩| ≥ c_x := α(|a_x| − Δ) − √(1 − α²)·√(‖v⁺‖² − (|a_x| − Δ)²), where a_x is the Prop. 19.3 amplitude and Δ its vacuum Lipschitz bound.
- **Decomposition.** With k = m − 1 and everything in units of ρ_x^k (ρ_x = λ₁^e/λ₀ exactly):
  ⟨a⁺, S^kb⁺⟩ − λ₀-part ≥ ρ_x^k[X_LX_R − (λ₂^e/λ₁^e)^k(‖v⁺‖ + ‖B⁺‖e_L)(‖v⁺‖ + ‖B⁺‖e_R)], with X = c_x − ‖B⁺‖e > 0.
  - The odd part is ≤ (λ₁^o/λ₁^e)^k(‖v⁻‖ + ‖B⁻‖e)², with λ₂^e/λ₁^e ≤ L₂/μ_x and λ₁^o/λ₁^e ≤ √(U − S2_even)/μ_x.
  - The second-order terms carry an extra ρ_x e², since ‖S^mε_L‖ ≤ ρ_x^m‖ε_L‖ exactly.
  - All terms decay at the same rate, so once the bracket is positive at some k it stays positive for every larger k.
- **J = 170 values.**

| N | q_x′ ≥ | L₂ ≤ | α² ≥ | \|a_x\| ≥ | c_x ≥ | ‖v⁺‖ ≤ | λ₂^e/λ₁^e ≤ | λ₁^o/λ₁^e ≤ |
|---|---|---|---|---|---|---|---|---|
| 4 | 0.14636 | 0.0600 | 0.9347 | 0.10479 | 0.07901 | 0.13468 | 0.410 | 0.616 |
| 3 | 0.14628 | 0.0547 | 0.9597 | 0.08555 | 0.06986 | 0.10972 | 0.374 | 0.592 |

#### 19.6.5 Prop. 19.6 [proved by the author; review needed]
- For N ∈ {3, 4}, J ≥ 170, and pairs with both end exponents ≥ d, every separation m ≥ 1 is covered, by Jensen for m ≤ m_J(d) and by the top mode for m ≥ m_M(d). The worst case over 481 log-spaced J subintervals plus [2·10⁴, ∞) is (scratch/endpairs4_N{4,3}.txt):

| N | pairs | d | m_J(d) | m_M(d) |
|---|---|---|---|---|
| 4 | flip | 4 | 17 | 4 |
| 4 | flip | 8 | 36 | 4 |
| 4 | same-type | 1 | 4 | 4 |
| 4 | same-type | 2 | 14 | 3 |
| 3 | flip | 3 | 14 | 4 |
| 3 | same-type | 1 | 7 | 3 |

  - So both ranges overlap for flip pairs at d ≥ 4 (N = 4) and d ≥ 3 (N = 3), and for same-type pairs at d ≥ 1.
  - At smaller d the m = 1 flip pair (the binding pair, relative margin 0.65%) fails first. Its end correction at d = 3 is ≈ 2.4·10⁻⁴ against Cov₁·J² ≥ 1.18·10⁻⁴.
- Same-type pairs at m = 0 are variances. Flip pairs at m = 0 are covered by Lemma 19.6a.

#### 19.6.6 What remains, and a route for (3)
- **What remains.**
  - (i) Pairs with a bond in columns 1–5 (N = 4) or 1–4 (N = 3), or their mirror images, for flip pairs; columns 1–2 for same-type pairs.
  - (ii) Horizontal edges.
- **Route for (i).** The top-mode technique also handles long separations from a bond near the end, if the end-modified amplitude ⟨u_x, B⁺T^{d}ŵ⟩ is computed. This is a 3-column integral for d = 0 (cluster | insertion·V | free end), and for d ≥ 1 it follows from the 2-column ⟨u_x, ŵ⟩ via the same decomposition.
- **Cost.** Short separations near the end need norms such as ‖B_Xŵ‖² (4 columns) or the cluster residual c. This is item (3).

**Files (sha8).** endw.py bcddbe81; endpairs4.py 6a366d45; endw_N4_J170.json / _N3 e8b1fe30 / 0db59cc3; endpairs4_N4.txt / _N3 6b2702ef / 540b079f.

### 19.7 After review (RV13_1 + §6, RV13_2 §6, RV11_32), and the pause point (the redirect, round 12) (appended)

**Checks.**
- **RV13_1** (f1b60d65; addendum §6 1cd72965): Prop. 19.3 and Lemma 19.1c hold in floating point (not certified).
  - the arb re-assembly gives Cov·J² ≥ 1.1735·10⁻⁴ (N = 4) and 2.2036·10⁻⁴ (N = 3).
  - Lemma 19.1c was tested exactly on graphs with cycles: 174 cases, 0 violations.
- **RV13_2 §6** (92b5e31e): Lemma 19.2 holds in floating point.
- **RV11_32** (e2019ebb): Lemma 19.4 and Cor. 19.4 hold in floating point.
  - the exact MC gives tr T²/λ_h² = 1.0353916(36) (N = 4) and 1.0347575(45) (N = 3).
- §19.5 is with the review as RV13_5. §19.6 is frozen (c4d17a01).

**Answers.**
- **M1 (RV13_1, now a nit): TRB(J) ≤ TRB(170) for J ≥ 170.** Add to 19.3.5.
  - twrig4's bound has the structure of Lemma 19.2(a): second-order part S_ξ(1 + s₁t + s₂t²), with s₁ = 1.074, s₂ = 1.065 (N = 4) and 0.682, 0.672 (N = 3), all positive, so this part increases in t.
  - Every error term is nonincreasing in J: t^k times unnormalized tilted expectations with the tilt fixed at J = 170; Chernoff factors; off-Ω terms √J·e^{−cJ}.
  - Hence tr T_ξ/λ_h ≤ TRB(170) on J ≥ 170, and tr T_ξ/μ̂ ≤ TRB(170) because m̂ ≥ 1.
- **D5 tolerance** (corrects ADD1's "about 1%"):
  - For Prop. 19.3, D5 may be underestimated by up to ×1.455 (N = 4) or ×5.1 (N = 3) before the bound flips.
  - At N = 4 on [170, 171.7] the other distances to flip are: all 19.1c error bars together ×2.08, TRB ×2.9, everything else ≥ ×11.
  - D5 is the first term to certify.
- **Nits (RV13_1).**
  - t endpoints were rounded to nearest; they will be rounded outward in the certified version (a 10⁻¹⁶ relative effect).
  - The stored trial polynomials are flip-even only to 10⁻¹¹; the symmetrized coefficients are used (§19.5.1).
  - |λ₀ − μ̂| carries a factor 1/√(1 − s²) ≤ 1 + 1.1·10⁻⁸; immaterial.
  - The N = 3 true value of Cov·J² at J = 170 is 3.08·10⁻⁴.
  - c₃ comes from sw3 (G2WOLFF), not from the data.
  - Scope: at N = 3 the pieces 19.3, 19.5 and 19.6 are claimed from J = 170 only, so [150, 170) is open there.
- **α-strip correction (RV13_2 §6).** In the one-column trace, det Q_k(α) = 3[(1+m)(3+m)]² vanishes only at Re α = 0, |Im α| = κ₁ = 0.962 (and 1.567). The strip is limited near α = 0 by κ₁, not by the soft mode at α = π.
  - In the two-column trace det Q_k vanishes at 1.925i (RV11_32 m2).
  - The per-node bounds take a min over ε, so they are only piecewise analytic. ε must be fixed per node interval before the quadrature error is estimated.
- **Withdrawn (RV13_2 nit).** The "better λ₁" slack in §19.2a relied on 10-state Ritz values, which §19.3.1 found unresolvable.
- **m1 (RV11_32): the J ≥ 170 argument for Lemma 19.4.**
  - The third-order part lead·(1 + c₁t + c₂t² + c₃t³) has c_k > 0, so it increases in t.
  - Each remainder (R_E, ρ₄, tail, annulus, far) is nonincreasing in J once the radii, the tilts, the per-node ε and the Chernoff λ are all frozen at their J = 170 grid values. That is the λ-grid technicality: re-optimizing per J could only lower the bound.
  - the numbers: the N = 4 remainder is 6.51·10⁻⁴ at J = 170, 3.79·10⁻⁴ at J = 185 and 1.5·10⁻⁵ at J = 340. Piecewise freezing would raise the J → ∞ ratio margin (0.944, 0.726, 0.774); the bottleneck is J ≈ 170.

**Pause point.** On the redirect to IM_√, resume here in this order:
1. α-strip bounds for the quadratures of 19.2 (κ₁ = 0.962) and 19.4 (1.925), with ε fixed per node interval (RV11_32 m2).
2. Certify D5 first, then the 19.1c error bars. This needs interval versions of amom2b, CondMom and Wishart; send main a price before starting.
3. RV11_32 m3 (add twlib2_check checks for exactly what twrig6 uses, l.27, 40, 44) and m4 (the hemisphere factor 2⁶ against the far-region Chernoff; a sentence on the equatorial set).
4. Deferred by the decision: (3) small j (route in §19.6.6), (4) horizontal edges, and the [35, 80–120] gap (parked).
5. N = 3 on [150, 170).
