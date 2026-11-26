# HS_TYPEB_LEMMA_NOTE_v1_1_ADD1: Lemma A, crude first-column bounds for the type-A rows (D4 and D4M at d_L = -1)

pk08, 2026-11-08T13:16:29Z (date -u). Addendum to HS_TYPEB_LEMMA_NOTE_v1_1 (6d0864e5; closed ba362538), which stands.
Context: the approval for the type-A certified rows, from my D2 answer to pk11. R6.5 needs a certified q >= ||Q0 X* a|| on the
12 type-A rows per N (D4 and D4M at d_L = -1), and q_need >= 18 on every row (pk11). These bounds replace the V12-strip route.

## 0. Answer first
- With A = (N-1)/2, tau <= N*_TAU_HI (TAU_D3B_v1) and Q0 dropped:
  - D4: q <= (A + |c_t|) (1 + tau^2)^(1/2) ((A - c_b)^2 + A^2)^(1/2), for c_b < J + A. No lambda factor.
  - D4M: q <= (A + |c_t|) (1 + tau^2)^(1/2) (A2 + c_b^2 A0)^(1/2) (lambda_h/lambda_0)^(1/2), for c_b >= 0.
- At the record's D4 boxes (bc, 30 digits):
  - D4: 5.0108394240 (N4, c_b = 0.77) and 2.1449075969 (N3, c_b = 0.50);
  - D4M: 5.5314112393 (N4, c_b = 0.89) and 2.6829148845 (N3, c_b = 0.60), each times (lambda_h/lambda_0)^(1/2).
- All are below 18. The smallest margin is 3.25x (D4M at N4), and 2.85x even with the J-uniform fallback ratio of sect. 3.
- Every input is certified and reviewed: TAU_D3B_v1, F4 (Lemma D3's first step), H-BESSEL's upper half, and Lemma D4's HS bound with A2
  and A0.

## 1. Objects (the note's sect. 1; the combined record's T_DEF, H_DEF, OPERATOR_D4 and OPERATOR_D4M)
- T = K^(1/2) V K^(1/2) on L^2((S^(N-1))^3) with normalized measures; V = e^{J(s_T.s_M - 1)} e^{J(s_M.s_B - 1)}; K = K_T (x) K_M (x) K_B with
  K_r(s, s') = e^{J(s.s' - 1)}. H is the O(N)-invariant subspace, and lambda_0 = max spec(T), attained on H.
- Z = K^(1/2) V^(1/2). Z Z* = T and Z* Z = V^(1/2) K V^(1/2) have the same top eigenvalue lambda_0 on H, so ||Z||_H = lambda_0^(1/2).
- G_t = V^(1/2) (K_t - c_t K) V^(1/2), with ||G_t||_H <= (A + |c_t|) lambda_0 (F4: Lemma D3's first step, the nonnegative kernel and
  H-BESSEL's upper half).
- M is multiplication by xi_b - c_b, with xi_b = J(1 - s_M.s_B). OPERATOR_D4: lambda_0^2 X = Z M G_t Z*. OPERATOR_D4M: lambda_0^2 X = Z G_t M Z*,
  the adjoint form.
- a = S'^-1 w/<u,w> = (lambda_0/(<u,w> v_0^(3/2))) 1, so Z* a = (lambda_0/<u,w>) V^(1/2) 1 (note sect. 1). Here v_0 = int e^{J(s.e - 1)} dsigma(s),
  ||V^(1/2) 1||^2 = int V = v_0^2, and 1 + tau^2 = lambda_0 v_0^2/<u,w>^2 (B6).
- q = ||Q0 X* a|| <= ||X* a||, with Q0 = 1 - |u><u|.
- Z, G_t and M commute with the diagonal O(N) action, and V^(1/2) 1 is O(N)-invariant, so every vector below lies in H.

## 2. Lemma A-D4 [D]
Claim. For every J > 0 (so every J >= 300), every c_t and every c_b < J + A:
q <= (A + |c_t|) (1 + tau^2)^(1/2) E_1(c_b)^(1/2) <= (A + |c_t|) (1 + tau^2)^(1/2) ((A - c_b)^2 + A^2)^(1/2), with E_1(c) as in A3.
- A1 (adjoint). G_t and M are self-adjoint, so X* = Z G_t M Z*/lambda_0^2 and X* a = (lambda_0/<u,w>) Z G_t f/lambda_0^2, where
  f = M V^(1/2) 1.
- A2 (norms). f is O(N)-invariant, so ||Z G_t f|| <= ||Z||_H ||G_t||_H ||f|| <= lambda_0^(1/2) (A + |c_t|) lambda_0 ||f||.
- A3 (one bond). ||f||^2 = int (xi_b - c_b)^2 V dsigma(s_T) dsigma(s_M) dsigma(s_B).
  - The s_T integral of e^{J(s_T.s_M - 1)} is v_0.
  - For fixed s_M, the s_B integral of (J(1 - s_M.s_B) - c_b)^2 e^{J(s_M.s_B - 1)} is v_0 E_1(c_b), where E_1(c) = E_1[(xi - c)^2]. E_1
    denotes the law of x = s_M.s_B under the density e^{J(x - 1)}/v_0 on S^(N-1), and xi = J(1 - x).
  - The s_M integral is 1. So ||f|| = v_0 E_1(c_b)^(1/2).
- A4 (assembly). ||X* a|| <= (lambda_0/<u,w>) lambda_0^(1/2) (A + |c_t|) lambda_0 v_0 E_1^(1/2)/lambda_0^2
  = (A + |c_t|) (lambda_0 v_0^2/<u,w>^2)^(1/2) E_1^(1/2) = (A + |c_t|) (1 + tau^2)^(1/2) E_1(c_b)^(1/2).
  There is no lambda factor: lambda_0 enters only through tau.
- A5 (exact single-bond identity). Put p_L(x) = A x - J (1 - x^2)/2. This is the kernel factor with
  Delta_s e^{J(s.s' - 1)} = -2J p_L(s.s') e^{J(s.s' - 1)}, because Delta f = (1 - x^2) f'' - (N - 1) x f' for f(x) = e^{J(x - 1)}. H-BESSEL
  sect. 0 writes the same factor as p_L = (N-1)/2 - xi + (xi^2 - (N-1) xi)/(2J). Pointwise in x:
    (1 + A/J) xi = A - p_L + xi^2/(2J),
  since A - p_L + xi^2/(2J) = A (1 - x) + (J/2) [(1 - x^2) + (1 - x)^2] = (A + J)(1 - x).
  The integral of a Laplacian over the sphere vanishes, so E_1[p_L] = 0. Equivalently, p_L o K_r = L^2 K_r/(2J) has no l = 0 part.
  Taking E_1 of the identity:
    E_1[xi^2] = 2 (J + A) g_0 - 2 J A, with g_0 = E_1[xi] = -J d log v_0/dJ (H-BESSEL sect. 1 at l = 0).
  Checks [D]: at N = 3, v_0 = (1 - e^{-2J})/(2J) gives g_0 = 1 - 2J/(e^{2J} - 1) and E_1[xi^2] = 2 up to O(J^2 e^{-2J}). At N = 4 for large
  J, g_0 = 3/2 - 3/(8J) + O(J^-2) and E_1[xi^2] = 15/4 + O(1/J) = A^2 + A.
- A6 (the H-BESSEL step). E_1(c) = E_1[xi^2] - 2 c g_0 + c^2 = 2 (J + A - c) g_0 - 2 J A + c^2.
  - For c < J + A the coefficient of g_0 is positive.
  - H-BESSEL's upper half gives g_0 < (N-1)/2 = A for every J > 0 (H_BESSEL_NOTE_v1 sect. 3, from Lemma 1 (L) of sect. 2 at mu = nu >= 1/2).
  - So E_1(c) < 2 (J + A - c) A - 2 J A + c^2 = (A - c)^2 + A^2.
- Remark (not used): g_0 = A - (A^2 - A)/(2J) + O(J^-2), so E_1(c) -> (A - c)^2 + A as J -> infinity. The J-uniform bound keeps A^2
  because it uses only g_0 < A. At N = 3 the two agree (A^2 = A = 1).

## 3. Lemma A-D4M [D]
Claim. For every J >= 300, every c_t and every c_b >= 0:
q <= (A + |c_t|) (1 + tau^2)^(1/2) (A2 + c_b^2 A0)^(1/2) (lambda_h/lambda_0)^(1/2).
- M1 (adjoint). X* = Z M G_t Z*/lambda_0^2, the adjoint of Z G_t M Z*/lambda_0^2. So X* a = (lambda_0/<u,w>) Z M h/lambda_0^2 with
  h = G_t V^(1/2) 1 in H and ||h|| <= (A + |c_t|) lambda_0 v_0 (F4).
- M2 (Lemma D4's factor). ||Z M h|| <= ||Z M||_H ||h||, and ||Z M||_H <= ||Z M||_HS,H, with
  ||Z M||_HS,H^2 = tr_H(Z M^2 Z*) = tr_H(K^(1/2) (xi_b - c_b)^2 V K^(1/2)) <= (A2 + c_b^2 A0) lambda_h for c_b >= 0.
  This is Lemma D4 of HS_NORMX_LEMMA_NOTE_v1 (reading A) for the same factor Z M, which also stands first in OPERATOR_D4. The cross term
  -2 c_b tr_H(K^(1/2) xi_b V K^(1/2)) is <= 0, and A2 >= tr_H(K^(1/2) V xi_b^2 K^(1/2))/lambda_h and A0 >= tr_H(T)/lambda_h are certified.
- M3 (assembly). ||X* a|| <= (lambda_0/<u,w>) (A2 + c_b^2 A0)^(1/2) lambda_h^(1/2) (A + |c_t|) lambda_0 v_0/lambda_0^2
  = (A + |c_t|) (1 + tau^2)^(1/2) (A2 + c_b^2 A0)^(1/2) (lambda_h/lambda_0)^(1/2).
- Lambda power 1/2. The reader applies the upper end of (lambda_h/lambda_0,lo)^(1/2), per piece from S8's lambda_0 lower end and
  LAMBDA_H_DEF (the rule on D4). The J-uniform fallback is lambda_h/lambda_0 <= 1/(N*_I_FREE_LO N*_RQH_LO) = 1.30766418 (N4) and
  1.19581639 (N3) from TAU_D3B_v1, by the Rayleigh quotient at V^(1/2) 1 and I_1col < 1.

## 4. Rows
- Both bounds increase in |c_t| and in tau.
  - D4's bound increases in |A - c_b|. Since c_b <= A on both boxes, its sup over a box is at the box's smallest c_b.
  - D4M's bound increases in c_b >= 0, so its sup is at the box's largest c_b.
- Over a row's box (ce = c_t, cf = c_b; the D4 boxes):
  - QA_D4 >= (A + ce_max) (1 + TAU_HI^2)^(1/2) ((A - cf_lo)^2 + A^2)^(1/2), lambda power 0;
  - QA_D4M >= (A + ce_max) (1 + TAU_HI^2)^(1/2) (A2 + cf_hi^2 A0_HI)^(1/2), lambda power 1/2.
- Values: as in sect. 0, with sqrt(1 + tau^2) = 1.1733341741 (N4) and 1.1153858587 (N3).
- Needs: q_need >= 18 on every type-A row (pk11), so every row closes.

## 5. For the review
1. A3: the s_T and s_B integrations, and that E_1 is the single-bond law of H-BESSEL sect. 1 (g_0 = w_0/v_0).
2. A5: the pointwise identity and E_1[p_L] = 0.
3. A6: the sign of the g_0 coefficient (c_b < J + A) and H-BESSEL's upper half at l = 0.
4. M2: that Lemma D4's HS bound applies to the factor Z M of X* = Z M G_t Z*/lambda_0^2 (c_b >= 0).
5. The box sups of sect. 4 and the lambda powers (0 for D4, 1/2 for D4M).

## 6. Sources (sha256sum at assembly)
- pk08/HS_TYPEB_LEMMA_NOTE_v1_1.md: 801099463aa4dff112c1bc2078c943f8aff15ecdcf9738aed1a7d9f2f03f0e53
- pk08/HS_NORMX_LEMMA_NOTE_v1.md: ffd98fc1946714e36e86359c338c38a6b89af31eb7f707306a0a59f3f281493b
- pk08/H_BESSEL_NOTE_v1.md: 3c543e3c28d67ba9f763c420c9ff3fc1d2f88b73249ed143b884078177cfb00c
- pk08/out/TAU_D3B_v1.kv: 04dfc7af4f895f14dbccd8c10a57186a3c5756210dde52749450f58a167f26aa
- pk08/out/HS_INV_NORMX_v1_d3d4b.kv: b80760c5b79f121a0c39d3302308816064a482fb47c90341938d52f9420772a3
- pk08/S4_RTR_CERTIFIED_v1.md: a2b08d873bc88b1fcdb2e64db91070ce0b204eedef725d9bf45ad15074c7a430
- pk08/out/px08_a2cert_v1_n4_asm.out: c2a7dff2b035c57e4bf9121dc11be2e8b90d5a8365b21259c2240c0f1c61ab2f
- pk08/out/px08_a2cert_v1_n3_asm.out: 82ddc3eb9004f8eb6f09208ddce6d2776ee8bad48329be04e262d0dd3ebbd87d
