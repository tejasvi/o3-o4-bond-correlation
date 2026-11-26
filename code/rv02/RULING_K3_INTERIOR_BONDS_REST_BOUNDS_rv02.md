# RULING_K3_INTERIOR_BONDS_REST_BOUNDS_rv02: bonds inside k = 3 chains, and the k = 3 rest factor by operator bounds

2026-11-08T19:09:29Z. Two questions. The first, with priority: which interior-bond bound is sound (pk08's draft 04dc9e2d) and
what v1_3 must change. The second (cap 0.2 h): (a) can J-uniform operator bounds replace the four-column mirror windows of the k = 3
rests, and (b) if not, is Lemma U order-generic?

Sources (sha256, first 8 hex; paths under code/):
- pk08/NOTE_I6_COLUMN2_OPERATOR_BOUND_v1.md 04dc9e2d (frozen draft, cited on the word);
- pk08/HS_NORMX_LEMMA_NOTE_v1.md 1340a52c (sect. 1 notation, F2, F3, F4, F6), pk08/S4_TRB_CERTIFIED_v1.md 91109301,
  pk08/S4_A2_DESIGN_v1.md 0eca31ca, pk08/out/px08_a2cert_v1_n4_asm.out c2a7dff2 and px08_a2cert_v1_n3_asm.out 82ddc3eb;
- pk02/DESIGN_UHAT_ASM_v1_3.md faa09e23, pk02/M2B_KV_v1.txt 13cc0d9a;
- rv02/CHECK_DESIGN_UHAT_ASM_V1_3_DELTA_rv02.md bce56382, REVIEW_DESIGN_UHAT_ASM_V1_2_DELTA_rv02.md c8c39134,
  chk_bond_in_chain_toy_v1.py 1cdbb181.

Notation (normX note sect. 1): Z = K^(1/2) V^(1/2), T = Z Z*, T_f = Z f Z*, lambda_0 = ||T||; G(c) = V^(1/2) (xi o K - c K) V^(1/2)
for a bond on a link between two V columns; H is the subspace invariant under global rotations, and every vector below lies in H.

## Answers
- Interior bonds. v1_3's l.211 factor is not sound inside a chain. pk08's sects. 2.2, 2.3 and 2.4 are sound, with two repairs: 2.3's
  last line misses the |c| part, and 2.4's J-law gate must be C-K3-MONO.
- (a) Yes. The k = 3 rest factor may be bounded by operator norms, provided each link takes the factor valid in its own normalization:
  F4 for a bond between two V columns, never the L-FH / sup_l form. With true rests at both ends no four-column window is needed.
- (b) Not needed for soundness once (a) is taken. Sect. 4 lists what a review of Lemma U at order K + 1 would check.

## 1. Interior bonds (pk08 04dc9e2d)
- **Not sound: v1_3 l.211.** sup_l |a_l - c| c_l/c_0 = ||xi o K - c K||/||K|| bounds the bond against K. Inside a K^(1/2)-normed chain
  the bond acts as b = a(Lambda) - c next to the middle column's T_M, and ||b T_M|| <= (sup_l |b_l| c_l/c_0) ||T_M|| fails near c = A
  (pk08 sect. 2.5; toy 1cdbb181: 1.46 to 2.24 times at c = A). This withdraws item (5) of c8c39134, as bce56382 said.
- **Sound: sect. 2.3** (one bond on the link into column 2 away from the modelled junction).
  - Split Theta = Theta~ + (Theta - Theta~) inside the form. The model part reads the engine's model mirror exactly. The difference is
    <a', (xi_w o K) h> with a' = V f_2 K (f_1 Delta) and h = f_3 g, bounded by R2 and E-R at that link, plus the |c| part:
    (2A + |A - c| + |c|) beta_2 eps(f_1) eps(f_3), which is J-uniform.
  - Steps checked: the transpose identity; |X| <= P_c (R1) and R2; E-R on each factor; |a'| <= V |f_2| K |f_1 Delta| pointwise,
    because K's kernel is >= 0; the |c| part by Lemma T.
  - Repair: at a bonded junction with no interior bond, the second-order term is (2A + |A - c| + |c|) beta_2 eps eps, not
    (2A + |A - c|) beta_2 eps eps as the section's last line says. The |c| part of v1_3 l.186 carries the rest's difference too.
- **Sound: sect. 2.4** (a junction bond by route R and an interior bond).
  - The bound 0 <= xi_w <= 2J holds pointwise on nonnegative kernels, which gives (2A + |A - c| + |c|) (2J) beta_2 eps(f_1) eps(f_3).
  - Repair: the J-law gate must be v1_3's C-K3-MONO, the n + 1 rate conditions per law. C-K3-JLAW reads only the sig^k structure.
    That covers the polynomial pieces, but the tail, far and g terms grow with the sup weights' J^n, so "they fall exponentially" needs
    (n + 1)/J_W < rate. With only the J_W keys, the value at J_W serves every piece.
- **Sound: sect. 2.2** (D4L0's column-2 multiplication).
  - Bounds: beta(xi45) <= N*_TRB/(1 - eps_r) and beta(xi45^2) <= N*_A2/(1 - eps_r), both J-uniform.
  - Steps checked: T_f >= 0 preserves H, so ||T_f||_H <= tr_H T_f. F6 gives the trace as int dg int W K(sigma, g sigma). The CLAIMs hold
    for every J >= 300 (TRB l.12; A2 READING lines, VERDICT VALID). The mirror (s_T, s_M, s_B) -> (s_B, s_M, s_T) preserves V, K and
    P_H, so xi_MB's traces are xi_TM's (A2 design l.13). Finally lambda_h <= mu-hat, since mhat >= 1, and mu_R >= (1 - eps_r) mu-hat.
  - Condition: the int column's V must be the records' column V; C-K3-SRC checks its couplings.
  - This replaces (I6')'s sup form (2J)^k, and it closes the E112 item of bce56382. E112 then carries
    3A (2J) N*_A2/(1 - eps_r) eps eps, bounded under C-K3-MONO.

## 2. What v1_3 must change
- (I6) and (I6'): column 2's beta by source: 1/(1 - s^2) (U2), N*_TRB/(1 - eps_r) for xi(4,5), N*_A2/(1 - eps_r) for xi(4,5)^2, read
  from the pinned records. Drop the (2J)^k sup form and l.98's polynomial line.
- l.211: delete it. A bond on a link into column 2 goes by sect. 2.3 (one) or 2.4 (two). This holds in the rest's model part and in
  T2's Delta-Delta term alike (l.155, l.192-197, l.210), or by sect. 3 below if the rest is bounded by operators.
- Gates, each with its plant:
  - C-K3-OP: beta source by k, and the bond route (none, 2.3 or 2.4);
  - C-K3-SRC: pinned reads, and the int column's V;
  - C-K3-MONO with n + 1 for every term with a factor 2J, in place of C-K3-JLAW;
  - C-K3-COUNT: 10, 1, 3, 4 per N.
- The rest of that review stands.

## 3. The k = 3 rest factor by operator bounds (ask (a))
- **Bound the true rest directly.** For the end at column 1 the rest is Theta' = f_2 V K_23 (f_3 F) with F = V K phi_0, so
  K^(1/2) Theta' = Z f_2 G_23 f_3 Z* psi-hat, where G_23 = V^(1/2) K_23 V^(1/2) and psi-hat = K^(1/2) phi_0. Hence
    ||K^(1/2) Theta'|| <= ||T_{f_2^2}||^(1/2) ||G_23|| <psi-hat, T_{f_3^2} psi-hat>^(1/2),
  and with no bond on link 2-3 also ||K^(1/2) Theta'|| <= ||T_{f_2}|| ||T_{f_3} psi-hat||.
- **Factors, each J-uniform.**
  - Empty column: lambda_0 <= mu_R/(1 - s^2) (U2).
  - Column multiplication: ||T_f||_H <= tr_H T_f (F6, TRB, A2).
  - Bond between two V columns: F4 gives ||G(c)|| <= (A + |c|) lambda_0, and A lambda_0 for the raw xi of the window. F3 bounds every
    eigenvalue of the positive kernel V^(1/2) (xi o K) V^(1/2) by its top, so the high harmonics cost nothing. This is the interior-bond
    factor for rests. The L-FH / sup_l form in the list is not a chain bound (sect. 1) and must not be used. Condition: both
    columns carry the records' V.
  - Far end: <psi-hat, T_{f_3^2} psi-hat> = W[f_3^2] = W_0 mu_R G_33 (the k = 1 model's G_bb), or a trace bound (A2 for D4ML0's
    xi(7,8)).
  - Bond at the modelled junction: route R's end factor, with the rest factor by E-R, (2A + |A - c|) ||K^(1/2) |Theta'| ||^2. That is
    the same chain with |f_2|, |f_3| and the raw bond.
- **T2 with true rests at both ends.** The identity W - W~ = <Delta_1, R F_3> + <F_1, R Delta_3> - <Delta_1, R Delta_3> is exact.
  - Both first-order terms have rests that end in V columns, so F4 serves every bond inside them.
  - The Delta-Delta term goes by sect. 2.3 or 2.4.
  - No four-column window and no extra model term are needed.
  - A decomposition that leaves a bond next to a non-V end (the model end F~, or a residual) cannot use F4 there. The two-term
    identity's F~ term does that whenever its junction is bonded; the three-term form avoids it.
- **The one weak spot.** xi(4,5)^2 next to a bond inside a rest (D4L0 E012, E102, E112) needs ||T_{xi45^4}||, which no record
  certifies.
  - Pointwise xi45^4 <= (2J)^2 xi45^2 gives ||Z xi45^2|| <= 2J (N*_A2 lambda_h)^(1/2). That puts a factor 2J in a first-order term,
    which stays bounded under C-K3-MONO's n + 1 conditions: about 2 J_W eps_r times the J-uniform factors, with 2 J_W eps_r = 3.1e-03 at
    N4 (nearest, INFO only).
  - A certified xi^4 trace, made like A2, would remove the factor.
- **Scope.** W3e, W3f, D4L0 and D4ML0. FA's rest ends in the cp state, not in F, so its factor needs <cp, K cp>-type data. FA is
  outside this rule until pk02 states FA's rest.

## 4. Lemma U at order K + 1 (ask (b))
- Not needed for soundness if sect. 3 is taken. pk02's float side decides whether its bars are tight enough.
- If main still wants the K 1 / K 0 path, the review of PLAN_M3_CODE_v1 sect. 5 with U1-U4 must check:
  - (i) the order-(K + 1) split moves every term of total order >= K + 1 into rem, including the overflow F_i E_j with i + j >= K + 1,
    with nothing dropped or counted twice;
  - (ii) the order-2 Hoelder pair has conjugate exponents, and its moments are certified;
  - (iii) every rem term carries t^(K+1) with a coefficient nondecreasing in t, so that B_rem(t) <= (t/t_REF)^(K+1) B_rem(t_REF);
  - (iv) U2's hhat bound does not depend on K.
- I have not read sect. 5. The review would take about 0.5 h.
