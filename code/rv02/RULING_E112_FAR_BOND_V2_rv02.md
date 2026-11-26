# RULING_E112_FAR_BOND_V2_rv02: pk08's column-2 traces (sect. 2.2), E111 and E112, and the far bond of the k = 3 rests

The review, 2026-11-08T19:27:38Z. Two lead asks. The first: pk08 04dc9e2d sect. 2.2 and E112, three questions, and the status of the 18:41Z ask.
The second, sharper: is there a J-uniform bound for the far bond of the 18 both-bond entries inside the rest's norm?

Sources (sha256, first 8 hex; paths under code/):
- pk08/NOTE_I6_COLUMN2_OPERATOR_BOUND_v1.md 04dc9e2d; pk08/HS_NORMX_LEMMA_NOTE_v1.md 1340a52c (sect. 1 notation; F2, F3, F4; F6);
- pk02/out/uhat_opr_v1_2.out 40981aed (SCRATCH_uhat_opr_v1_2.py cb1199fd); pk02/DESIGN_UHAT_ASM_v1_3_ADD1.md 03f73445 and _ADD2.md 60de6595;
- rv02/RULING_K3_INTERIOR_BONDS_REST_BOUNDS_rv02.md 965f72f0, CHECK_DESIGN_UHAT_ASM_V1_3_DELTA_rv02.md bce56382.

Notation as in 965f72f0: Z = K^(1/2) V^(1/2), T_f = Z f Z*, lambda_0 = ||T|| <= mu_R/(1 - s^2) (U2), and G = V^(1/2) (xi o K) V^(1/2)
for a raw bond on a link between two V columns.

## Answers
- (1) Yes. Sect. 2.2 bounds the factor that the chain itself carries, and every vector of the chain lies in H.
- (2) It closes E112's second-order term, and E111 uses N*_TRB/(1 - eps_r) in the same way. Under the operator route, one first-order
  rest of E012, E102 and E112 each still needs a xi(4,5)^4 trace (sect. 2).
- (3) Four gates beyond pk08's sect. 4 list are needed (sect. 3).
- The far bond of the 18 both-bond entries: yes. F4 bounds it J-uniformly by A lambda_0 inside a true rest. That is the factor A of
  pk02's original OPR column, now on a valid proof. Neither the pointwise 2J (OPR2J) nor the L-FH Gamma route is needed there.
- The 18:41Z ask was answered by 965f72f0 at 19:09Z, and main has since taken (a).

## 1. Sect. 2.2 inside the chain (question 1)
- In the second-order term (pk08 sects. 2.3 and 2.4), column 2 enters only through |a'| <= V |f_2| K |f_1 Delta|. So
  ||K^(1/2) |a'| || <= ||T_{|f_2|}|| ||K^(1/2) |f_1 Delta| ||: the chain's factor is ||T_{|f_2|}|| in the chain's own normalization.
- Sect. 2.2 bounds exactly that norm: ||T_f||_H <= tr_H T_f for T_f >= 0, together with F6 and the records' CLAIMs. All vectors involved
  (phi_0, F, g, the st weights, the xi's) are invariant under global rotations, so the H-norm is the norm that matters.
- l.211's bond factor failed because it compared the bond with K, not with T_M. Sect. 2.2 has no such mismatch.

## 2. E111 and E112 (question 2)
- Second-order term (sect. 2.4): 3A (2J) beta_2 eps(f_1) eps(f_3), with beta_2 = N*_TRB/(1 - eps_r) for E111 and N*_A2/(1 - eps_r) for
  E112. One power of J remains, so the term is bounded under C-K3-MONO's n + 1 conditions. E111 and E112 both close there.
- First-order terms under the operator route (sect. 4 below):
  - a rest whose far link carries a bond takes the chain Z f_2 G f_3 Z* psi-hat and needs ||Z f_2|| = ||T_{f_2^2}||^(1/2);
  - for xi(4,5) that is ||T_{xi45^2}|| <= N*_A2 lambda_h (certified), so E111, E011 and E101 close;
  - for xi(4,5)^2 it is ||T_{xi45^4}||, and no record certifies a xi^4 trace. That affects E112 (both ends), E012 (the end at column 3)
    and E102 (the end at column 1).
  - A rest without a far bond splits as T_{f_2} T_{f_3} psi-hat and needs only ||T_{f_2}|| (N*_A2 for k = 2). So E002 is not affected.
- For those three keys: either a certified xi^4 trace (A4, made as A2 on pk08's TRB chart), or the pointwise xi45^4 <= (2J)^2 xi45^2.
  The pointwise route puts 2J into a first-order term. pk02's OPRsup line (D4L0 N4, binding at E112) suggests that this does not
  fit D4L0's tolerance. Until A4 is certified and reviewed, C-K3-OP should refuse the three keys.

## 3. Gates beyond pk08's sect. 4 (question 3)
- C-K3-JLAW must be C-K3-MONO: the n + 1 rate conditions per law, for every term carrying a factor 2J (965f72f0 sect. 1).
- C-K3-SRC also checks that the int column's V is the records' column V, since sect. 2.2's traces and F4 both assume it.
- C-K3-DECOMP: every first-order term's rest must end in a true V column (sect. 4's three-term identity). A rest with a bond next to the
  model end F~ is refused. PLANT: decomposition (B)'s F~ term on a key with a bond on that junction must be refused.
- C-K3-A4: E012, E102 and E112 are refused unless a pinned, reviewed xi^4 trace is read. PLANT: N*_A2 in its place must be refused.
- On pk02's point (ADD1 sect. 4): for route none with a junction bond the factor is (2A + |A - c| + |c|). The P_c part and the |c| part
  of v1_3 l.186 both carry the rest's difference. ADD1 is right, and pk08 2.3's last line is short by |c| (965f72f0, repair 1).

## 4. The far bond inside a true rest (the sharper ask)
- Take the end at column 1, with route R on its junction. E-R gives <Theta', P_c Theta'> <= (2A + |A - c|) ||K^(1/2) |Theta'| ||^2.
  For the true rest Theta' = f_2 V K_xi (f_3 F), with F = V K phi_0 > 0, the raw far bond and K's nonnegative kernels give
    |Theta'| <= |f_2| V (xi o K) |f_3| V K phi_0 = V^(1/2) |f_2| G |f_3| Z* psi-hat,
  so that
    ||K^(1/2) |Theta'| || <= ||T_{f_2^2}||^(1/2) ||G|| <psi-hat, T_{f_3^2} psi-hat>^(1/2).
- F4 (normX 1340a52c l.70-74): G has a nonnegative symmetric kernel, so ||G|| is its top eigenvalue (F3). That eigenvalue is at most
  A lambda_0, since G <= A V^(1/2) K V^(1/2) by F2 (B3: xi o K <= A K on the row). The bound is J-uniform, and nothing new is needed.
- Inputs: A = (N - 1)/2; lambda_0 <= mu_R/(1 - s^2) with s = N*_S_300; ||T_{f_2^2}|| (lambda_0 for f_2 = 1, N*_A2 lambda_h for xi(4,5));
  <psi-hat, T_{f_3^2} psi-hat> = W_0 mu_R G_33 (the k = 1 model's G_bb) or N*_A2 lambda_h W_0 for an xi_MB end; and E-R's
  (2A + |A - c|) with the |c| part.
- Condition: the rest's far end must be a true V column. So T2 takes
    W - W~ = <Delta_1, R F_3> + <F_1, R Delta_3> - <Delta_1, R Delta_3>,
  with both first-order terms on true rests. The Delta-Delta term keeps sect. 2.4's 2J: its far side is a residual, but the term is
  second order. ADD1's decomposition (B) leaves one term with F~ at the far end, and with a bond on that junction F4 cannot serve.
- OPR2J put 2J on every raw rest bond, following bce56382, which gave only the pointwise factor. Inside a true rest, F4's A is
  the right factor. So pk02's original OPR column (factor A for raw rest bonds, 40981aed) is the right float for every
  bond-carrying rest that has no xi(4,5)^2 next to its bond.
