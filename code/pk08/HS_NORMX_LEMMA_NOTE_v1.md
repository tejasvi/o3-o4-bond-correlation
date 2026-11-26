# HS_NORMX_LEMMA_NOTE_v1: a certified HS bound on H for the D3, D4 and D4m class operators (route A, stage (a))
pk08, written 2026-11-08T07:59:29Z (date -u).

Note: no code, no run. Brief: the approval of 2026-11-08 (route A, stage (a): the derivation note, frozen, to the review before any code).
Spec: pk15/SPEC_HS_INV_NORMX_v1_1.md (operators in sect. 1 and 6). Marks: [D] derived here; [D, awk] a hand number from awk (float);
[E] estimate. Every path:sha8 is listed in sect. 8, computed by sha256sum when this note was assembled.

## 0. Answer first
- **Lemma D3** [D]. For every J > 0, N >= 3 and real c_t, c_bb, with a = (N-1)/2:
  tr_H(X_c* X_c) <= (a + |c_t|)^2 (a + |c_bb|)^2 tr_H(T^2)/lambda_0^2.
  For J >= 300 this gives HS2(D3) <= COEF_D3 (lambda_h/lambda_0)^2, with COEF_D3 = (a + |c_t|)^2 (a + |c_bb|)^2 U_N.
- **Lemma D4** [D]. For every J > 0, real c_t and c_b >= 0:
  tr_H(X_c* X_c) <= (a + |c_t|)^2 tr_H(K^(1/2) V (xi_b - c_b)^2 K^(1/2))/lambda_0 <= (a + |c_t|)^2 (A2 + c_b^2 A0) lambda_h/lambda_0,
  with A2 = tr_H(K^(1/2) V xi_b^2 K^(1/2))/lambda_h (new: stage (b)) and A0 = tr_H(T)/lambda_h <= N*_RTR mhat(t). D4m has the same bound.
- **Inputs used:** the upper half of H-BESSEL (w_l < a v_l), U_N, Rtr, the new A2, and the consumer's lambda_0 lower end through
  (lambda_h/lambda_0)^p, p = 2 (D3) or 1 (D4, D4m). Not used: TRB_H's P_L, the lower half of H-BESSEL, any cutoff in l.
- **Sizes** at pk15's box upper ends (v1_1 sect. 6), against the needs as HS^2:

  | class | COEF | p | need |
  |---|---|---|---|
  | N4 D3 | 44.38 [D, awk] | 2 | 240 |
  | N3 D3 | 9.04 [D, awk] | 2 | 225 |
  | N4 D4, D4m | about 21 [E] (A2 about 2.1) | 1 | 86 |
  | N3 D4, D4m | about 5 [E] (A2 about 1.3) | 1 | 86 |

- **Change from my first price (07:22Z).** Its factorization ||T^a S T^b||_HS <= lambda_0^a ||S|| ||T^b||_HS, with S = K^(-1/2) K_e K^(-1/2),
  fails because ||S|| is infinite (sect. 5). The positive-kernel step F3-F4 replaces it and covers the high harmonics where K_e is not
  PSD. The spectral step tr(T^(2b))/lambda_0^(2b) <= tr(T^2)/lambda_0^2 is not needed either: F5 yields tr_H(T^2) for any ring length.

## 1. Setup
- L = L^2((S^(N-1))^3) with normalized measures, sigma = (s_T, s_M, s_B). H = {f : U_g f = f} and P_H = int U_g dg.
- K_r(s, s') = e^{J(s.s' - 1)} on S^(N-1), and K = K_T (x) K_M (x) K_B. By Funk-Hecke, K_r = sum_l v_l Pi_l with v_l > 0, so K >= 0.
- V(sigma) = e^{J(s_T.s_M - 1)} e^{J(s_M.s_B - 1)}, in (0, 1], acting as a multiplication operator.
- The bond variables all lie in [0, 2J], so every operator below is bounded:
  - horizontal on row r, between two columns: xi_r(sigma, tau) = J(1 - s_r.t_r), and K_r^xi = xi_r o K (kernel times xi_r)
    = (xi o K_r) (x) (the other two rows' K);
  - the MB vertical of a column: xi_b(sigma) = J(1 - s_M.s_B), a multiplication operator.
- Z = K^(1/2) V^(1/2). Then T = Z Z*, and Th := Z* Z = V^(1/2) K V^(1/2).
- lambda_0 = max spec(T) on L.
  - T and Th have the same nonzero spectrum, so lambda_0 = max spec(Th).
  - Th has a continuous, strictly positive kernel. By Jentzsch, lambda_0 is simple with a positive eigenfunction. U_g maps that
    eigenfunction to a positive eigenfunction with the same eigenvalue, so it is invariant, and lambda_0 = max spec(T on H).
  - This is the spec's lambda_0 (sect. 1).
- Every operator here commutes with U_g, hence with P_H: K_r is zonal; V and xi_b depend only on dot products within the column;
  xi_r is invariant under simultaneous rotation.
- Trace class: tr T = int V(sigma) K(sigma, sigma) dsigma = int V <= 1. So T and Th are trace class on L and on H, and Z is
  Hilbert-Schmidt.
- G_r(c) = V^(1/2) (K_r^xi - c K) V^(1/2) for real c.
- The spec's operators (v1_1 sect. 6 strings), with equal column potentials:
  - D3: lambda_0^3 X_c = K^(1/2) V (K_t - c_t K) V (K_bb - c_bb K) V K^(1/2) = Z G_T(c_t) G_B(c_bb) Z*.
  - D4: lambda_0^2 X_c = K^(1/2) V (xi_b - c_b) (K_t - c_t K) V K^(1/2) = Z M G_T(c_t) Z*, where M multiplies by xi_b - c_b on
    column 0 (M and V^(1/2) commute).
  - D4m: lambda_0^2 X_c = K^(1/2) V (K_t - c_t K) V (xi_b - c_b) K^(1/2). This is the adjoint of D4's, because K_t and K have
    symmetric kernels and M commutes with V.
- **Reading of HS2** (to confirm in v1_2): HS2 = tr_H(X_c* X_c) with X_c as in sect. 1, normalized once by lambda_0^w. v1_1 sect. 6
  l.84 writes "tr_H(X_c* X_c)/lambda_0^(2w)" for that same quantity.

## 2. Facts
- **F1** (upper half of H-BESSEL: H_BESSEL_NOTE_v1 sect. 2 Lemma 1, sect. 3 "Upper") [D]. For N >= 3, J > 0 and l >= 0, w_l < a v_l,
  where xi o K_r = sum_l w_l Pi_l.
  - w_l = -J dv_l/dJ gives w_l/v_l = J(1 - r_mu(J)) - l, with mu = l + (N-2)/2 >= 1/2 and r_mu = I_{mu+1}/I_mu.
  - r_mu solves r' = 1 - 2 alpha r/x - r^2 with alpha = mu + 1/2 >= 1.
  - phi = 1 - alpha/x gives phi' - F(x, phi) = alpha (1 - alpha)/x^2 <= 0, and phi < 0 < r near 0.
  - Riccati comparison then gives r_mu > phi on (0, inf). So J(1 - r_mu(J)) < alpha, and w_l/v_l < alpha - l = a.
- **F2** (operator order) [D]. On L, K_r^xi <= a K, and hence V^(1/2) K_r^xi V^(1/2) <= a Th.
  - F1 gives xi o K_r <= a K_r on L^2(S^(N-1)): both are diagonal in Pi_l.
  - Tensoring with the positive K of the other two rows keeps the order, and so does conjugation by V^(1/2).
- **F3** (positive kernels) [D]. A bounded self-adjoint A with a pointwise nonnegative kernel has ||A|| = max spec(A).
  - Proof: |<f, A f>| <= <|f|, A |f|> <= max spec(A) ||f||^2.
- **F4** (the class factor) [D]. ||G_r(c)|| <= (a + |c|) lambda_0, on L and therefore on H.
  - V^(1/2) K_r^xi V^(1/2) has the symmetric nonnegative kernel V(sigma)^(1/2) xi_r(sigma, tau) K(sigma, tau) V(tau)^(1/2).
  - By F3 and F2, its norm is at most a max spec(Th) = a lambda_0. Also ||c Th|| = |c| lambda_0.
  - **This step covers the high harmonics.** xi o K_r has negative eigenvalues for large l (g_l -> -inf). F3 still bounds every
    eigenvalue of V^(1/2) K_r^xi V^(1/2) in absolute value by the top one. No inverse of K and no cutoff in l is used.
- **F5** (HS sandwich on H) [D]. For bounded A commuting with U_g: ||Z A Z*||_HS(H)^2 <= ||A||^2 tr_H(T^2).
  - Proof (everything on H): ||Z A Z*||_HS^2 = tr(Z A* Z* Z A Z*) = tr(A* Th A Th). Cyclicity holds because Z is HS.
  - That equals <Th A, A Th>_HS <= ||Th A||_HS ||A Th||_HS <= ||A||^2 ||Th||_HS^2.
  - Finally tr_H(Th^2) = tr(P_H Z* T Z) = tr(P_H T^2).
- **F6** (twisted one-column traces) [D]. For a bounded multiplication W >= 0 that commutes with U_g:
  tr_H(K^(1/2) W K^(1/2)) = int dg int dsigma W(sigma) K(sigma, g sigma) >= 0, and it is monotone in W pointwise.
  - Proof: tr(P_H K^(1/2) W K^(1/2)) = tr(W^(1/2) K P_H W^(1/2)), and K P_H has the kernel int dg K(sigma, g tau) >= 0.
  - This is the spec's tr_H formula (sect. 2).

## 3. Lemma D3 [D]
- **Statement.** For every J > 0 and real c_t, c_bb: tr_H(X_c* X_c) <= (a + |c_t|)^2 (a + |c_bb|)^2 tr_H(T^2)/lambda_0^2.
- **Proof.** lambda_0^3 X_c = Z A Z* with A = G_T(c_t) G_B(c_bb). F4 gives ||A|| <= (a + |c_t|)(a + |c_bb|) lambda_0^2, and F5 gives
  tr_H(X_c* X_c) <= ||A||^2 tr_H(T^2)/lambda_0^6.
- **Certified form (J >= 300).** tr_H(T^2) <= U_N lambda_h^2 (S4_U_CERTIFIED_v3 CLAIM), so
  HS2(D3) <= (a + |c_t|)^2 (a + |c_bb|)^2 U_N (lambda_h/lambda_0)^2.
  - The bound is monotone in |c_t| and |c_bb|. For pk15's positive boxes, the sup is at the upper ends.
- **Remarks.**
  - The bound holds for every c, so it does not use the centring's cancellation.
  - At c = 0 it bounds the uncentred ring by a^4 tr_H(T^2)/lambda_0^2.

## 4. Lemma D4 and D4m [D]
- **Statement.** For every J > 0, real c_t and c_b >= 0:
  tr_H(X_c* X_c) <= (a + |c_t|)^2 tr_H(K^(1/2) V (xi_b - c_b)^2 K^(1/2))/lambda_0 <= (a + |c_t|)^2 (A2 + c_b^2 A0) lambda_h/lambda_0.
- **Proof.**
  - lambda_0^2 X_c = (Z M) G_T(c_t) Z*, so ||X_c||_HS(H) <= ||Z M||_HS(H) ||G_T(c_t)|| ||Z*||/lambda_0^2.
  - ||Z*||^2 = ||Z Z*|| = lambda_0, and F4 bounds the middle factor by (a + |c_t|) lambda_0.
  - ||Z M||_HS(H)^2 = tr_H(Z M^2 Z*) = tr_H(K^(1/2) V (xi_b - c_b)^2 K^(1/2)), by F6 with W = V (xi_b - c_b)^2.
  - For xi_b >= 0 and c_b >= 0, (xi_b - c_b)^2 <= xi_b^2 + c_b^2, so F6's monotonicity gives the last step.
- **Inputs.**
  - A0 = tr_H(T)/lambda_h <= N*_RTR mhat(t) <= N*_RTR mhat(1/300). This is S4_RTR_CERTIFIED_v1:
    tr_H(T)/mu-hat <= N*_RTR, with mu-hat = lambda_h mhat and m1..m3 > 0.
  - A2 is new (stage (b)): TRB's chain (px08_trbcert_v1_1) with F -> F^2.
  - Mirror: (s_T, s_M, s_B) -> (s_B, s_M, s_T) preserves V, K and P_H. So A2 for xi_MB equals A2 for xi_TM, which is TRB's insertion
    (X_T/2 at leading order).
- **D4m.** X_c(D4m) = X_c(D4)* (sect. 1). Both commute with P_H, so tr_H(X X*) = tr_H(X* X), and the bound is the same row for row
  (C-HS-MIRROR).
- **Dropped term.** -2 c_b A1, with A1 = tr_H(K^(1/2) V xi_b K^(1/2))/lambda_h >= 0 (TRB). Keeping it would need a lower end of A1.
  It would shrink COEF by about 3-4x at N4 [E], which is not needed.

## 5. Why the first price's factorization is replaced
- On row r, S = K^(-1/2) K_r^xi K^(-1/2) acts as g_l = w_l/v_l on Pi_l.
  - H-BESSEL's lower half allows g_l as low as (N-1)/2 - c_N/J - l(l+N-2)/(2J).
  - The true g_l does go to -inf: r_mu(J) -> 0 as l -> inf at fixed J, so g_l is about J - l.
  - So ||S|| is infinite, and ||T^a S T^b||_HS <= lambda_0^a ||S|| ||T^b||_HS gives nothing.
- Splitting off L_r^2/(2J) (TRB_H's P_L) leaves |S| of size L_r^2/(2J) on the high harmonics.
  - The HS norm is quadratic in the insertion, so that split needs a second moment of L_r^2, a degree-4 insertion, which no record
    has.
- F3-F4 avoid S. They bound the norm of V^(1/2) K_r^xi V^(1/2) through its nonnegative kernel, using only w_l < a v_l.

## 6. Sizes, interface, remaining stages
- **COEF at pk15's box upper ends** (N4: c_t, c_bb <= 1.06 and c_b <= 0.89; N3: 0.72 and 0.60):
  - D3 [D, awk]: N4 (1.5 + 1.06)^4 x 1.033200684443 = 44.376; N3 (1 + 0.72)^4 x 1.032809143879 = 9.039.
  - D4 and D4m [E]: N4 6.5536 (A2 + 0.7921 A0); N3 2.9584 (A2 + 0.36 A0).
    - A0 <= 1.33104 x mhat(1/300) = 1.3329 at N4 [D, awk].
    - The A2 estimates assume a chi-square shape with N - 1 degrees of freedom for xi under the trace weight, with mean TRB/Rtr
      (0.983 at N4, 0.706 at N3): A2 about 2.1 and 1.3.
- **The (lambda_h/lambda_0)^p factor.**
  - lambda_0's certified lower end is the consumer's (S9 pieces).
  - Since mu-hat = lambda_h mhat with mhat >= 1, the factor is about 1/mhat(t)^p <= 1, up to the Ritz width [E].
  - Asked of pk15 for v1_2: a LAMBDA_POWER field, or a J-uniform pin.
- **J.** The lemmas hold for every J > 0. U_N, N*_RTR and A2 hold for every J >= 300 by their REASON keys. Proposed METHOD:
  UNIFORM_LEMMA.
- **Remaining stages** (prices, 2026-11-08 about 07:56Z):
  - (b) A2;
  - (c) the export script: KV record plus a run output with the VERDICT and RECORD lines;
  - the C-HS-OP t = 0 ring controls, if kept.
- **Tightness** [E].
  - the review expects the true HS^2 at about 1e-4 (D3) to 1e-2 (D4).
  - The bound gives up the centring (F4 bounds |G|, not G near Omega_0) and every eigenvalue of T beyond tr_H(T^2).
  - A sharper F4 would need a lower end of V^(1/2) K_r^xi V^(1/2) above -a lambda_0. It is not needed for these needs.

## 7. For the review
1. The operator identities of sect. 1, against v1_1 sect. 6's OPERATOR strings: equal column potentials, D4's M on column 0, and
   D4m = D4*. Also the HS2 reading in sect. 1.
2. F3 and its use in F4: the kernel of V^(1/2) K_r^xi V^(1/2) is symmetric and nonnegative, and the bound holds on L and hence on H.
3. F5: Z is Hilbert-Schmidt on H (tr_H Th = tr_H T <= 1); the cyclicity step; tr_H(Th^2) = tr_H(T^2).
4. F1 as restated. It is H_BESSEL_NOTE_v1's Lemma 1, and only this half is used.
5. lambda_0: the max of spec(T) on L, attained on H (Jentzsch for Th), equal to the spec's normalization.
6. Lemma D4: (xi_b - c_b)^2 <= xi_b^2 + c_b^2 needs c_b >= 0, which holds for the positive boxes. Also check the mirror step for A2.
7. A0 from Rtr: tr_H(T)/lambda_h <= N*_RTR mhat(t), with mhat increasing on (0, 1/300] because m1..m3 > 0.

## 8. Sources (sha256sum at assembly)
- pk15/SPEC_HS_INV_NORMX_v1_1.md:8043f94a
- rv01/CHECK_SPEC_HS_INV_NORMX_V1_rv01.md:f912ebb0
- pk15/SPEC_HS_INV_NORMX_v1.md:d73b1f53
- pk08/H_BESSEL_NOTE_v1.md:3c543e3c
- pk08/S4_U_CERTIFIED_v3.md:e870cbe5
- pk08/S4_RTR_CERTIFIED_v1.md:417cb603
- pk08/S4_TRB_CERTIFIED_v1.md:91109301
- pk08/S4_TRBH_CERTIFIED_v1.md:bb53005c
- pk08/px08_trbcert_v1_1.py:6baa4535
