# SPEC_S8_CERT_v1: the certified S8 (vertical pairs near the free ends, J >= 300, N = 3 and 4)

pk11, 2026-11-07. Specification for the review, written to the approval and its rules sent after float piece 3e. Where they
differ it supersedes the route tables of PLAN_S8_CERT_v2 (28513c51). It folds in every point of the three reviews:
REVIEW_PLAN_S8_CERT_v1_rv01 8adc43f0, REVIEW_PLAN_S8_CERT_v2_rv01 6efc040d, and its ADD1 684a76a7. Section 14 maps each point.

**Float basis (all VALID; outputs N4 / N3).**
- 3a kt_s8f3a_v1 (bad405b6; 7ccf30aa / 754321c3): the m = 1 main risk.
- 3b kt_s8f3b_v1_1 (a84afc27; ff04ba0b / 3f3a8a7e): the bilinear form without cancellation; d = 1 exact.
- 3c kt_s8f3c_v1_2 (404e723c; 58390b0b / db19b5ac): R-b, T2, T4, T5 with the T1 lemma.
- 3d kt_s8f3d_v1_2 (457a4c29; ba1afc11 / 7d86384e): this SPEC's bounds under a uniform relative bar beta.
- 3e kt_s8f3e_v1 (e1d2b180; 8dbdd8ef / 7e2e59c4): uniform-beta comparison and route thresholds.
- 3e kt_s8f3e_v1_1 (e3db0160; b4db63ba / f5928ab9): per-entry bars, the requirement list, the fallbacks, and the lemma with the
  leakage Gram.

**Inputs.**
- Trial set z9sym_v1: ts ea9d6c1b / a298db65, vacres_sym b40859de / e5a9b49f. The per-state moves are in
  out/STATE_MOVES_z9sym_v1.txt (e05ada6c, jq): states 0-3, which certified entries use, moved at most 4.0e-11 / 1.5e-10.
- Entry list: S8_ENTRY_LIST_v2 (4565c6c7).
- pk03's float bars: m3ref_v1_2 z9sym N4 records (D d9e65c23, N0T 424848ea, N1 5f766307). C-M3NORM shows my a_k equal them to 2.0e-12.
- Nothing new was run for this file.

## 0. Answer first
- **Claim (S8).** For N in {3, 4}, every J >= 300 (t = 1/J in [0, 1/300]) and every 3 x n free strip, Cov(X, Y) >= 0 holds for
  every vertical pair with separation m >= 1 that S7 does not cover. Section 1 gives the classes.
- **One identity for every class** (Section 2). The left end has states (l_L, x_L = A_X l_L), the right end (l_R, y_R), and k = m - 1:
  Cov J^2 Z^2 = <A^L, S^k A^R> + det_k, with A^L = l_Lu Q0 x_L - x_Lu Q0 l_L, A^R likewise, Z = l_Lu l_Ru + z and det_k = z xy - x1 y1.
  - A right end at infinity gives 19.6.2's one-sided chain (A^R = p_Y, det_k = 0).
  - Two finite ends give its two-sided identity.
  - The n = 4 strip is the case of two end columns.
- **Bounds** (Sections 4-6).
  - Below each class's m0: the main term on the interval Ritz basis, plus the corrected lemma in its leakage-Gram form (T1'),
    and at m = 1 a parity refinement.
  - From m0 on: the top-mode form, with Weyl and Davis-Kahan bounds and the reduced form of C4.
  - In float on real bars, m0 <= 6 in all 26 classes.
- **Float status on real bars** (3e v1_1). Bulk entries carry 1.1 x pk03's float bars. S8-specific entries carry the analog
  model of Section 5.5, since none of them has a float bar yet. Headroom = Cov / (Cov - Cov_lo).

| reading (N4 / N3) | per-entry bars | uniform 1e-5 | uniform 1e-4 |
|---|---|---|---|
| S8-2 flip (0,1) m1 | 2.26 / 2.90 | 2.43 / 3.91 | 0.89 / 1.46 |
| S8-1 flip d_L 2 m1 | 5.25 / 6.02 (route B) | 2.94 / 4.1 (route A) | 1.94 / 2.52 (route A) |
| S8-3 n4 flip 1-4 | whole strip 28.4 / 22.9; chain 6.20 / 6.93 | strip 13.9 | strip 1.39 |
| one-sided flip d -1 m2 | 6.34 / 7.01 | 81.2 | 22.6 |
| global minimum, crude route | 1.73 / 2.33 | 2.43 / 3.91 | 0.89 / 1.46 |
| global minimum, AL graph route | 4.11 / 4.42 | | |

  - Uniform 1e-4 was pessimistic for the m = 1 pairs and the whole strip.
  - Uniform 1e-5 was optimistic for the lemma classes. The real leakage floor is eta+ = 1.47e-2, against 6.6e-4 in the beta model.
    It comes from the TT analog bars and the state-3 diagonal T entries (Section 5.4).
- **Decision rule** (Section 11).
  - The crude route certifies S8 if pk03's real bars for the S8-specific entries meet Section 8's requirement list. On the analog
    model, N4 needs all bars x0.67; N3 already has x1.36 of slack.
  - Otherwise the AL graph [vac a | V xi | V xi | vac b] is activated. It is a named M3 entry, on hold, and with it every row clears
    with x1.46 bar slack at N4.
  - The centered single-integrand residual entries are a minor fallback: they raise S8-2 (0,1) to 2.79 / 3.82 but leave the global
    minimum unchanged.
- **What changed from plan v2.**
  - The chain dominates the windows at every d <= 0 threshold (Section 6.7), so W3 and W4 stay only as named entries on hold.
  - No 10-state basis.
  - The S7 mode bound at d = 1, 2 is replaced by the top-mode form.
  - The fixed-coefficient |p_perp| form is dropped: 3d shows it 6x worse here (Section 5.1).
  - S8-3 is n = 4 only, by the better of the whole strip and the chain per pair; n = 2, 3 are cited.
  - The M2 safe ends are corrected for Rtr (and ae) (Section 7).
- **Price for this item:** 9-12 h and about 1 core-h (Section 12). M3's preps are its own: S4, H and L, plus AL if activated.

## 1. Claim and coverage (C6, T5, M2)
- **Pairs.** X is a T-M bond in column j, Y is in column j + m with m >= 1. The exponents are d_L = j - 2 and d_R = n - j - m - 1,
  so n = d_L + d_R + m + 3; an end column has d = -1.
  - Mirror (left-right) and T <-> B reduce every vertical pair with m >= 1 to this form (C-MIRROR).
  - m = 0 is Lemma 19.6a (flip) or a variance (same).
- **S7** (P2) covers flip pairs with min(d_L, d_R) >= 3 and same-type pairs with min(d_L, d_R) >= 1 (NOTE1_d3, e64e90cf).
- **Near and far.** Near means <= 2 (flip) or <= 0 (same). D_far = 3 (flip) and 1 (same), for both N.
- **S8-1 (n >= 5):** exactly one end near (by mirror, the left). The far exponent is >= D_far, and every bound below holds uniformly
  in it (Section 6.3).
- **S8-2 (n >= 5):** both ends near, every m >= 1.
  - At m <= 2 (T5) the list is finite: 14 flip classes and 1 same-type class, up to mirror (awk).
  - Flip: (-1,2,m1,n5) (0,1,m1,n5) (0,2,m1,n6) (1,1,m1,n6) (1,2,m1,n7) (2,2,m1,n8) (-1,1,m2,n5) (-1,2,m2,n6) (0,0,m2,n5)
    (0,1,m2,n6) (0,2,m2,n7) (1,1,m2,n7) (1,2,m2,n8) (2,2,m2,n9).
  - Same-type: (0,0,m2,n5).
  - Larger m: the chain below m0, the top mode from m0.
- **S8-3:** n = 4, every pair (Section 6.5). n <= 3 is cited, under the rule (d), to proved results of the paper.
  The citations are to pk13/paper/G2_PAPER_DRAFT_v4_13.tex (1836cd24), with numbers from its build aux.
  - n = 3, the grid P3 x P3: Theorem 1.5(i) (label thm:D, "uniform coupling on 3 x n grids"). Cov >= 0 for every pair of edges and
    every J >= 0, at N = 3 and 4.
    - Records: pk13/UNIFORM_G2_CLAIM_ASSEMBLY_v0_1.md (3892acbd) + ADD1 (872de38b) + ADD2 (9dfc0a48); the declaration
      UNIFORM_G2_DECLARATION_main_v1.txt (fd3cfad7).
    - Its deduction is checked in Lean 4: statements G2Kernel_La_v1_6 (manifest a0f5b1ab), proofs
      G2Kernel_Lb_p11 (manifest 9b37c47f), run pb11 (ee232972). The certified computations are not re-run in Lean.
  - n = 2, the grid P3 x P2 (the 2 x 3 ladder, 2-connected and outerplanar with a path weak dual), all couplings:
    - O(4): Theorem 1.3(a) (thm:B), proved as Theorem 4.10 (thm:strips). Records: e10/g2rep/G2REP_NOTES.md; review
      e10/notes/rv30_a/RV30_A_NOTES.md (d12d66de); re-derivation code/rv01/AUDIT_PAPER_v4_2_PART1_rv01.md (de554e8d), Section 4.
    - O(3): Theorem 1.4 (thm:C; the ladder has no W4 minor). Records: meta/paper/w4free/w4free.tex (53055883) Theorem 1.1 and
      k4.tex (874abe43); review code/rv03 (1cf00493).
    - The paper says so after Theorem 1.5: "The grid P3 x P2 is the 2 x 3 ladder, which Theorems 1.3 and 1.4 cover for all couplings."
    - Part A's O(3) packaging is the user's call, but the result exists either way.
  - n = 1, the path P3: it has no pair with m >= 1. Its same-column pair shares a vertex (Theorem 3.2, thm:shared).
  - The rule: list v2's conditional S2/S3 entries are dropped.
- **Completeness.** For n >= 5, both far is S7, one near is S8-1, both near is S8-2; n <= 4 is S8-3 or the cited theorems.

## 2. Exact identities
- **Notation** (19.6.2).
  - T = K^{1/2} V K^{1/2} is positive, since V > 0. lambda_0 and u are its top eigenpair; u is even.
  - Q0 = 1 - |u><u|, and S = Q0 T Q0 / lambda_0 on u-perp. S is self-adjoint and S >= 0.
  - S' = T / lambda_0 = |u><u| + S.
  - w = K^{1/2} V 1, w-hat = w / <u, w>, eps_d = S^d Q0 w-hat, with |eps_0| = R_w.
  - A_X = T_xi / lambda_0, B_X = A_X - c S' (c the bulk mean), p_X = B_X u.
  - B+- are the T <-> B parity parts of B_X; P2 exports |B+| and |B-|.
- **Chain vectors** (kt_s8f3b_v1_1's cov2).
  - Left: l(d) = S'^{d+1} w-hat and x(d) = A_X S'^d w-hat for d >= 0; l(-1) = w-hat and x(-1) = w-hat_X.
  - Right: the mirror images (A_Y = F A_X F for flip); at infinity, (u, A_Y u).
  - X sits in column d + 2; k = m - 1 transfer steps separate the ends.
  - d = -1, 0, 1 are exact: d = 1 comes from the H graph [vac a | V xi | V | free]. d >= 2 are Ritz steps with component bounds (Section 4).
- **Identity.** With Z = <l_L, S'^k l_R>, XY = <x_L, S'^k y_R>, X1 = <x_L, S'^k l_R> and Y1 = <l_L, S'^k y_R>,
  Cov J^2 = XY/Z - X1 Y1/Z^2.
  - Splitting each form into its u-part and Q0-part, the u-parts of Z XY - X1 Y1 cancel exactly (they have rank one). What remains is
    Cov J^2 Z^2 = <A^L, S^k A^R> + det_k.
  - At infinity: A^R = Q0 A_Y u = p_Y and det_k = 0. At d >= 0 with l_Lu = 1: A^L = Q0 B_X l - <eps, p_X> S eps = a_d, 19.6.2's
    one-sided form (checked in the review v1, Section 2).
  - Controls: C-HARM (t = 0, exact for d = -1, 0, 1: 6e-12 .. 1.8e-11), and C-SF0 (Section 10).
- **Flip parity.** S, Q0, W and P_perp commute with F. For flip pairs the right vectors are the F-images of the left ones.
- **S8-1's far end (T4).** For d_R >= D_far, A^R = p_Y + dA^R with |dA^R| <= sqrt(|B+|^2 + |B-|^2) e_R + |p_Y| e_R e_R+1
  (eps_R even, e_R = R_w rho1^{d_R}). Also |z| <= (r + eta)^k |Q0 l_L| e_R+1 and |det_k| <= 2 (r + eta)^{2k} |Q0 l_L| e_R+1 |Q0 x_L| |Q0 y_R|.

## 3. Ritz data on u-perp (T1 settings 1 and 2, C2)
- **Trial states.** s_0 = psi-hat (vacres p) and s_1..s_3 (z9sym; states 1, 3 even, 2 odd). Entries: g,a,b (D), T,a,b (N), TT,a,b (L).
- **Setting 1** (C2 in its v2 form). W' = Q0 W0, where W0 is the Ritz span on psi-hat-perp. With s from M2:
  - |<u, e_k>| <= s;
  - G'_kl = delta_kl - <u,e_k><u,e_l>, R'_kl = T_kl/lambda_0 - <u,e_k><u,e_l> and M2'_kl = <e_k, T^2 e_l>/lambda_0^2 - <u,e_k><u,e_l>.
    These are exact, since Q0 T^j Q0 = T^j - lambda_0^j |u><u|.
  - Components of vectors in u-perp are unchanged, and interlacing on W' bounds the eigenvalues of S itself.
- **Setting 2.** R is the interval Ritz matrix of S on W' in its orthonormal basis f_k.
  - The main term is <x_W, R^k y_W>.
  - The leakage Gram is G = M2 - R^2, with M2 = <f_k, S^2 f_l>.
  - eta+- = sqrt(lambda_max of G in each parity), upper ends; eta = max(eta+, eta-); eta_k from G's diagonal.
- **s_perp.** s_perp^2 <= |S|_HS^2 - tr(R^2), with |S|_HS^2 = U(t) (lambda_h/lambda_0)^2 - 1.
  - U(t) is S4-U v2's LEAD_HI (1 + C1_HI t + C2_HI t^2 + C3_HI t^3) + R_CERT, in P2's S4U_KV_v1 normalization.
  - The leakage blocks' HS mass is dropped, which only loosens the bound.
  - r = max(rho_1, s_perp).
- **Weyl and Davis-Kahan, per parity sector** (S = D + E, |E| = eta+-):
  - rho_x in [rho_1 - eta+, rho_1 + eta+];
  - second even eigenvalue <= max(rho_3, s_perp) + eta+;
  - top odd eigenvalue <= rho_2 + eta-; second odd <= s_perp + eta-;
  - sin(theta_1) <= eta_1 / gap_1 with gap_1 = rho_1 - max(rho_3, s_perp) - eta+, and likewise sin(theta_o) <= eta_o / gap_o.
  - When the gaps are positive, both top eigenvalues are simple (19.6.4's simplicity condition).

## 4. The truncation lemma (T1, in its leakage-Gram form T1')
- **Lemma T1'.** Take S self-adjoint on u-perp, W' with orthonormal basis f_k, R, G, eta, s_perp and r as in Section 3. For x, y in
  u-perp and n >= 1:
  |<x, S^n y> - <x_W, R^n y_W>| <= s_perp^n |x_perp||y_perp|
    + sum_{i=0}^{n-1} [ s_perp^i |x_perp| g(R^{n-1-i} y_W) + g(R^i x_W) s_perp^{n-1-i} |y_perp| ]
    + [(r + eta)^n - r^n - n r^{n-1} eta] |x||y|,
  where g(v) = |P_perp S v| = sqrt(v^T G v) for v in W. For n = 0: |<x, y> - <x_W, y_W>| <= |x_perp||y_perp|.
- **Proof.**
  - Write S = D + E with D = S_W + S_perp block-diagonal and E = P_W S P_perp + P_perp S P_W off-diagonal, |D| <= r, |E| = eta.
  - Expand (D + E)^n.
    - D^n gives <x_W, R^n y_W> + <x_perp, S_perp^n y_perp>.
    - The one-E word D^i E D^j (i + j = n - 1) gives <S_perp^i x_perp, P_perp S R^j y_W> + <P_perp S R^i x_W, S_perp^j y_perp>,
      which is bounded as stated, since |P_perp S v|^2 = v^T G v exactly.
    - Words with two or more E's total at most sum_{k>=2} C(n,k) r^{n-k} eta^k |x||y|.
  - The one-E bound is never larger than the n r^{n-1} eta (|x_W||y_perp| + |x_perp||y_W|), because g(v) <= eta |v| and s_perp <= r.
    It is much smaller when the vectors sit on low-leakage Ritz directions, which is what makes real bars workable (Section 5.4).
  - With certified G (values plus half-widths dG), g(v)^2 <= v^T G v + sum |v_a v_b| dG_ab. W-component errors e add eta rho_max^j |e|.
  - PLANT-T1: the multi-E tail is nonzero at m = 3.
- **Sector form.** The lemma holds in each parity sector with eta+-, since S, W' and P_perp commute with F.
- **m = 1 refinement with d_L = d_R** (both ends at the same exponent):
  - Flip: A^R = F A^L, so <A^L_perp, A^R_perp> >= -|P_- A^L_perp|^2. For an inserted state at d >= 1,
    |P_- A^L_perp| <= |l_u| (|p_perp| + |B-| e_d), because Q0 l is even.
  - Same-type: A^R = A^L, so the truncation is |A^L_perp|^2 >= 0.
- **Propagation.**
  - |(S v)_perp| <= s_perp |v_perp| + g(v_W).
  - The W components of S v and of A_X v, taken from v_W alone, err by at most eta |v_perp| and
    (sqrt(|B+|^2 + |B-|^2) + c eta) |v_perp|. This is the (s_perp + eta)^d correction of the review T1, now in Gram form.
- **Rational assembly.** With the truncations dz, dxy, dx1, dy1 of the four forms and t1 of <A^L, S^k A^R>:
  - Num_lo = Num - t1 - (|z| dxy + |xy| dz + dz dxy + |x1| dy1 + |y1| dx1 + dx1 dy1), and Cov_lo = Num_lo / (Z + dz)^2.
  - Every second-order product is kept (C1's rule).
  - Cov_hi (the symmetric bound) serves C-SF0.

## 5. Residual norms and floors (R-a, T2)
- **5.1 |p_perp| (R-a).**
  - Route B, on the D graph: p~ = K^{1/2} (xi_Y - c~) phi_0 / |s_0|.
    - |p~|^2 = (DYY - c~^2 g00)/g00 and <f_k, p~> come from DY,a.
    - |p~_perp|^2 = |p~|^2 - sum_k <f_k, p~>^2 is evaluated as one rational function of the entries' exact t-series. Its t^0 and t^1
      orders cancel exactly (route B is exact at t = 0; 3d: 1.3e-8 at J = inf, float level), so only remainder bars remain. That is
      R-a's request.
  - The eigen trick (19.3.3 (v)) gives |p_Y - p~| <= eps_a + Delta_vac (M2's eps_a; S5's Lipschitz form, RV13_1). So
    |p_perp| <= |p~_perp| + eps_a + Delta_vac + s |p_W|.
  - Not the fixed-coefficient form. 3d's (DYY - 2 sum G_a DY,a + sum G_a G_b g,ab)/g00, with G frozen at J = 300, equals route B at
    J = 300 (C-FIXG). But its bar is a sum of terms with large G_a: 5.4e-3 / 3.6e-3 against 8.4e-4 / 6.9e-4 (beta 1e-5). Frozen at
    300, it also leaves 4.8e-4 at t = 0.
- **5.2 d = -1, 0, exactly.**
  - |A_perp|^2 = |A|^2 - |A_W|^2, with |A|^2 = l_u^2 |Q0 x|^2 - 2 l_u x_u <Q0 x, Q0 l> + x_u^2 |Q0 l|^2.
  - The norms and cross terms are entries: FF z, wXwX and wXw at d = -1; S4 Z4, X1X2 and X1 at d = 0.
  - Real bars: |A_perp| = 0.0935 at d = -1 and 9.90e-3 at d = 0 (N4).
- **5.3 d >= 1.**
  - Plain state: Section 4's propagation.
  - Inserted state: Q0 x(d) = p_X + Q0 B_X eps_d + c S eps_d, so
    |x_perp(d)| <= |p_perp| + sqrt(|B+|^2 + |B-|^2 e_d^2 - kappa_d^2 - |W part|^2) + c |l_perp(d)|.
    - The W part of Q0 B_X eps_d is x_W(d) - p_W - c l_W(d), known.
    - e_d = min(R_w rho1^d, |Q0 l(d-1)| with floor).
  - The operator norm is the loss here. 3c's float eta_A is 0.0409 against sqrt(|B+|^2 + |B-|^2) = 1.0184, a factor of 24.9 (awk).
    eta_A times e_1 (0.0262) is 1.07e-3, against 2.8e-2 by the operator norm. The AL graph recovers this factor (Section 6.4).
- **5.4 Floors on real bars (T2).** Every residual and eta is computed from the entries' intervals.
  - 3e propagates each entry's bar linearly, entry by entry, to every quantity. On real bars, N4: eta_k = 5.2e-3 / 6.4e-3 / 1.2e-2
    (float 5.8e-5 / 1.8e-5 / 7.2e-6), and |p_perp|_c = 3.4e-3 (float 2.6e-5).
  - Shares of the half-widths:
    - eta^2: 2.15e-4, of which TT 2.1e-4, T 5.0e-6, g 1.5e-7;
    - |p_perp|^2: 1.18e-5, of which DYY 9.2e-6, DY 1.6e-6, g 9.7e-7;
    - |A_perp(0)|^2: 3.75e-5, of which fX 1.6e-5, X1X2 1.1e-5, X1 6.4e-6.
  - So the floors are set by TT, DYY, fX, X1X2 and X1, all on the analog model. The T2 estimate (about 4.6e-4 at 1e-5) holds
    only for uniform bars.
- **5.5 The analog model** (until pk03's float probe; 3e's docstring). Certified bar = 1.1 x float bar.
  - From m3ref: g,a,b; T,a,b; A,a = TX,0,a. Parity zeros of the symmetric set: 0.
  - TX,a,b: 3 x T,a,b. e,0: 3.1e-7. e,a: 2.1 x g,0,a. f,a: 2.1 x T,0,a. eX,a and fX,a: 2.1 x A,a. h and hX: 2 x f and fX.
  - z: 5.7e-7; wXw 3z; wXwX 9z; Z4 2z; X1 6z; X1X2 18z.
  - DY,a: A,a. DYY: 3 x Ia. TT,a,b: 2 x T,a,b. AA,a,b: 6 x T,a,b.

## 6. The bounds per class
- **6.1 Below m0: the lemma.** Cov_lo as in Section 4, minus the main-term bars.
  - The main-term bars come from propagating M3's bars through the cancellation-free chain. They are small at m = 1; for example
    about 1e-6 of 4.95e-4 at flip d = 1 under uniform 1e-5.
  - R-b (m = 2, 3 at d <= 0): uniform 1e-5 gives >= 77.6 / 88; real bars give one-sided flip d -1 m2 6.34 / 7.01. The leakage lemma
    replaces the alpha-bounds.
- **6.2 From m0: the top-mode form and C4.**
  Num = rho_x^k <A^L,f><f,A^R> + rho_o^k <A^L,f_o><f_o,A^R> + <A^L, S_rest^k A^R> + det_k, with f and f_o the true top even and odd
  eigenvectors and |S_rest| <= sigma_rest = max(rho_3, s_perp) + eta.
  - **Lemma C4 (S8-mono).** Put a_lo = |A^L_1| - sqrt(2) sin(theta_1) |A^L| - (component error), b_lo likewise, and P_lo = a_lo b_lo.
    Let q_o = (rho_2 + eta-)/(rho_1 - eta+), q_r = sigma_rest/(rho_1 - eta+) and q_d = (r + eta)^2/(rho_1 - eta+), all < 1. Then
    Num >= rho_x^k R(k) with R(k) = P_lo - q_o^k O - q_r^k Rr - q_d^k Dc, where:
    - O bounds the odd term;
    - Rr = sqrt(|A^L|^2 - a_lo^2) sqrt(|A^R|^2 - b_lo^2);
    - |det_k| <= (r + eta)^{2k} Dc.
    R is nondecreasing in k, so R(k0) > 0 gives Cov > 0 for every m >= k0 + 1 =: m0.
  - Every decaying term enters with its magnitude subtracted, including the odd term of same-type pairs, whose sign is unknown (v1's C4).
    The two-sided case covers S8-2 at every m >= m0.
  - Float: m0 <= 4 under uniform bars and <= 6 on real bars. R(4)/P_lo >= 0.710 / 0.755 at uniform 1e-5.
  - PLANT-OVERLAP needs a sin(theta) factor of 17.2 / 20.6 to break the binding class.
  - **F2 inputs (the rule (b)).** 3d's values are carried as the reference: sin(theta_1) <= 6.4e-3 (6.44e-3 / 6.42e-3, uniform
    1e-5) and R(M1)/P_lo >= 0.63 (0.631 / 0.692, uniform 1e-4). On real bars eta_1 is 5.2e-3 (3e v1_1), so sin(theta_1) is larger and
    m0 reaches 6. The certified run evaluates gap_1, sin(theta_1), q_o, q_r, q_d and R(k) per piece from its own intervals. 3d's values
    are the float check C-REPRO compares against.
  - This replaces 19.6.4's alpha-bound form and S7's mode bound at d = 1, 2. The review T3's second point is answered: S8 does not use
    S7's mode bound.
- **6.3 S8-1 (T4).** Per (d_L, kind, m), the better of two routes. Each holds uniformly in d_R >= D_far.
  - Route A: the one-sided bound with the crude far-end terms of Section 2 at d_R = D_far.
  - Route B: the two-sided chain for d_R = D_far, D_far + 1, D_far + 2 (Ritz steps with component bounds), and route A's terms at
    D_far + 3.
  - Real bars: flip d_L = 2, m = 1 at 5.25 / 6.02 by route B (2.94 / 4.1 by route A at uniform 1e-5).
  - The far end is S8-1's thin spot; residual entries do not help it, and route B fixes it with no new entries.
- **6.4 S8-2 (T5).** The two-sided chain for each near pair: the lemma below m0, the top mode from m0.
  - Real bars, crude route: (0,1) m=1 at 2.26 / 2.90, and the global minimum is 1.73 / 2.33.
    - The minimum is (2,1) m=1, both ends at d >= 1, where the operator-norm d >= 1 residuals multiply.
    - Every m <= 2 class clears 1.5. At N4 every row clears 2 only if all bars shrink by x0.67.
  - **Named fallbacks** (T5 asks for them now), in order:
    1. The AL graph [vac a | V xi | V xi | vac b]: V 12, F 20, the 10 entries AA,a,b. It certifies eta_A, which replaces the
       operator norm in the d >= 1 inserted residual: |x_perp(d)| <= |l_u| |p_perp| + eta_A |l_W| + (|B| + c) |l_perp|.
       - Real bars with AL: global minimum 4.11 / 4.42, all bars may grow x1.46 / x1.48, S8-2 (0,1) 6.38 / 6.44.
       - Price: K = 3 needs D about 10 at F = 20. That is past amom2b's int64 guard (K = 1 there), so it needs M3's engine and
         pk03's price. My estimate [E] is 10-50x a 4-column prep, i.e. several core-h per N.
    2. Tighter bars on the residual and leakage groups: the requirement list of Section 8. The residual groups x0.56 alone suffice at N4.
    3. The 10-state basis (+3 h, 2-4 core-h; plan v2 Section 5).
    Whole strips at n >= 5 stay out of reach.
  - **Named risks (the rule: rows between 1.2x and 2x after v1_1 are risks with a fallback, not blockers).** On the analog bars
    these are the N4 rows of S8-2 with both ends at d >= 1, at m = 1 (smallest (2,1) at 1.73). Their fallbacks are the AL graph
    (4.11) and the residual groups tightened x0.56. Nothing on real bars is below 1.2x.
  - **The two exits for the state-3 leakage floor** (the message after 3e). eta_3 is 1.18e-2 against eta_1 at 5.2e-3, and TT's share of eta^2's
    half-width is 2.1e-4 out of 2.15e-4.
    - Exit 1, tighter bars. TT (L graph, 10 entries) and T,3,3 within the factors of Section 8. With AL, TT may grow x1.47 and T x12.7;
      on the crude route T or TT alone cannot fix N4, which needs the residual set x0.56. Price: pk03's (larger radii, K or J_REF
      pieces for the L prep); asked.
    - Exit 2, structural: take state 3 out of W. W becomes span{f_1, f_2}, so the leakage Gram has no state-3 row. State 3's spectral
      mass moves into s_perp through the HS budget, which no longer subtracts rho_3^2, and gap_1 = rho_1 - s_perp - eta stays positive.
      Price: no new entries (fewer are used), plus one float reading (3e's code with W = 2 states, about 0.03 core-h) to show the margins.
    - A single-integrand leakage entry, <(T - mu)s_a, (T - mu)s_b> as one integral, is not expressible in the present format. Its three
      terms live on three graphs (L for T^2, N for T, D for 1), and the trial states sit on vacuum-type columns. It would need engine
      support for a linear combination across graphs. Not proposed.
  - **The residual-entry fallback**: a residual's Gram combination as one M3 entry.
    - The exact <x - Px, x - Px> is not one integrand either. For d = 0, x = A_X w-hat lives on the S4 strip, while P projects onto the
      trial states, which live on vacuum-type columns. So |x|^2 (S4), <s_a, x> (E3) and <s_a, s_b> (D) are three graphs.
    - The closest single-integrand form is to center within each graph, which removes the O(1) cancellation inside the norm:
      - XXc on S4: (xi - kappa_0) on both interior columns, giving |x - kappa_0 l|^2 directly;
      - fXc,a on E3: (xi - kappa_0) on the middle column, a = 0..3;
      - for d = -1, wXcwXc on FF and eXc,a on E2.
      kappa is an exact binary64 coefficient (the chain's x_u), carried in the 'xi' factor's constant.
    - If one integrand's bar scales with its own size (asked of pk03), they cut the d <= 0 floors by |A|^2/(sum of the absolute
      terms). They lift S8-2 (0,1) to 2.79 / 3.82 but leave the global minimum unchanged, so they are a minor fallback.
    - Price: 10 extra factor sets on preps that run anyway (S4: 1; E3: 4; FF: 1; E2: 4). That is seconds on the 3-column graphs and a
      small share of the S4 prep. Same F as their parent entries.
- **6.5 S8-3 (n = 4).** Per pair, the better of two routes:
  - the whole strip (S8F1's S4 set, 18 entries), with bar B_XY + 2c B_X + 3c^2 B_Z;
  - the n = 4 chain row.
  - Real bars: flip 1-4 at 28.4 / 22.9 by the strip and 6.20 / 6.93 by the chain. Every pair's better route clears 2.
  - The chain fails only at the (1,-1) pairs, which the strip covers (49x at uniform 1e-5).
- **6.6 d = 1, 2 at m = 1** (ADD1, Section 3).
  - Direct chain on real bars: d = 1 at 3.91 / 4.24 and d = 2 at 5.89 / 6.58.
  - The named alternative is bulk + delta with P2's c5. With the sharpened |x_perp| <= sqrt(|B+|^2 + |B-|^2) e_d + |kappa_d| (r + eta) e_d
    (0.0270 / 0.0158 at d = 1), it gives 16.4x / 26.2x at uniform 1e-5.
  - ADD1's budget line: the truncation stays under half the margin while |p_perp| <= (c5 + delta)/(2 x 0.0270), i.e. 6.93e-3 at N4 (awk).
    the 0.0248 used |B+| alone; 0.0270 is the valid value.
- **6.7 Windows against the chain.** The uniform beta at which the headroom falls to 2 (3e, N4):

| class | chain | window |
|---|---|---|
| flip d -1, m1 | 6.0e-4 | W3: 2.3e-4 |
| flip d 0, m1 | 4.5e-4 | W4: 8.5e-5 |
| flip d -1, m2 | 2.5e-3 | W4: 1.4e-4 |

  - Same-type is 1.3e-2 .. 2.4e-2 for the chain against 7.1e-4 .. 7.4e-3 for the windows.
  - The chain dominates everywhere. W3 and W4 stay named and on hold (the rule (a)).
  - **Triggers**, read on certified or real float bars:
    - W3 comes back if the chain's one-sided d = -1, m = 1 row (flip or same) falls below 2. On real bars it is 5.67 flip / 179.8 same
      at N4, and 5.61 / 178.6 at N3.
    - W4 comes back if the chain's d = 0, m = 1 row or d = -1, m = 2 row falls below 2. On real bars these are 14.41 / 6.34 at N4 and
      12.78 / 7.01 at N3.
    - A window can only help if its own bar headroom, Cov/(6 beta c^2) on real bars, is above the failing chain row's. The comparison
      above says it is not at any uniform beta.

## 7. Vacuum terms and M2 keys (C1, the Rtr note)
- **The five places**, each an exact identity plus an operator-norm bound, with both cross terms written out wherever both vectors move:
  1. lambda_0 in m-hat [1 -+ eps_r / sqrt(1 - s^2)] (RV13_1 N3).
  2. W' = Q0 W0, with |<u, e_k>| <= s (Section 3).
  3. c and p_Y: components from the N graph with S5's Delta (19.3.3 (vi); TRB for beta). |p_Y - p~| <= eps_a + Delta_vac.
  4. <u, w> through q - sp, as in R_w.
  5. |p_Y|^2 by the eigen trick with eps_a.
- **How each M2 key enters, and its safe end.** From P2's vac_float (kt_s67_cert_v1_2 e7e973d0, l.524-541):
  - near = nP s_^2 + (D5 + R0) s_^5 + (tX + ann) dec + tB_J, with dec = exp(-0.3 ae (J - 150)/2);
  - fJ = far (J/150)^2 e^{...}, g = gB (J/150) e^{...};
  - eps_r = (sqrt(near^2 + fJ) + g)/sqrt(z2), s = eps_r / (2 - Rtr - eps_r), and eps_a, eps_ds5 = wres(...)/sqrt(z2).
  - Safe ends:
    - UPPER for NP, D5, R0, TX, TB, ANN, FAR and GB (all enter positively);
    - UPPER for RTR, since s increases in Rtr (the correction of plan v2 l.87);
    - LOWER for Z2, which divides;
    - LOWER for AE, a decay rate: dec decreases in ae for J > 150. This is a second correction of plan v2 l.87, which listed AE among
      the upper ends.
  - sp = |u - psi-hat| increases in s.
  - S8 uses eps_r, s, sp and eps_a; eps_ds5 only if the odd norm enters.
  - S8's float scripts use none of these keys (checked: kt_s8f* contain no Rtr, Z2 or law key). The certified code reads them through
    M2's reader with these ends, and C-FMT's key-swap plant covers a swapped end.
- In 3a/3c the vacuum residual is about 2.5e-10 at J = 300, so these terms are tiny; C1 concerns their form.

## 8. Inputs, formats and the per-entry requirement
- **M3 (pk03 produces every S8 entry; S8 imports records by sha).**
  - List v2's 102 required entries. The conditional sets: W3/W4 on hold (Section 6.7); S2/S3 dropped.
  - Named fallback entries on hold: AL (AA,a,b, 10 entries); the centered entries XXc, fXc,a, wXcwXc, eXc,a.
  - Format: PLAN_M3_CODE_v1 (ffdf8446) Section 4, as in M3_ENTRY_LIST_v1_2 (3b4b6946), with pk03's sha-pinned reader (C-FMT) and a
    key-swap plant.
  - **The int64 limit (the note on the M-a layer).** The M-a layer's MomTable codes need (D + 1)^F < 9e18, and K = 3 needs D about 10. Each
    4-column form is therefore split; the layer refuses loudly if a table would exceed the limit.
    - S8's graphs list one pair list per graph (S4 F 19, H F 16, L F 18, W4 F 19; AL F 20). The split is per entry: each entry's
      table carries only the pair variables its own factors use.
      - S4: Z F 12; x,c,B F 13; xy F 14.
      - H: h,a F 15; hX,a F 16.
      - L: TT,a,b F 18.
      - W4 (on hold): Z F 15, x F 16, xy F 17.
      These fit at D = 10, since 11^18 = 5.56e18 (awk) is below the limit. The unsplit graphs would not: 11^19 = 6.12e19 for S4 or W4,
      and 11^20 = 6.73e20 for AL.
    - L and AL can be split further by expanding each 'cp' factor (trial state a on a vacuum column) into its BASIS9 monomials. Each
      monomial uses at most 2 of its column's 3 pair variables, so one product of monomials uses at most 4 pairs (L, F_eff <= 16) or 6
      (AL, F_eff <= 18). The entry is then the sum of those tables' moments; this is exact, since moments are linear.
    - So AL fits at D <= 10 only by this monomial split. Otherwise it needs the arb fallback: a big-integer or dict-keyed MomTable
      without the int64 code, slower. That is pk03's choice and price.
  - **VERDICT rule (427dccbe).** Every reader S8 uses requires a record's VERDICT lines to equal exactly
    ['VERDICT VALID']. It refuses VALID-PRECERT, VALID-STUB and any other variant by FORMAT or claim prefix, never by a substring test.
    PLANT-PRECERT: a PRECERT copy of a valid record must be refused. This applies to the M3, M2, S4-U, S4-TRB and P2 readers alike.
- **Per-entry maximum-bar table** (sent to pk03). For S8-2 flip (0,1) m=1 to clear at 2x, each group
  is scaled alone, with the rest at 1.1 x their bars. The table gives absolute bars in M3's unit normalization (3e v1_1; N3 allows
  2-6x more):

| group | largest bar per entry, N4 | factor over the analog model |
|---|---|---|
| Z4 | 3.4e-5 | x27 |
| X1 | 2.2e-5 | x5.72 |
| X1X2 | 4.1e-5 | x3.68 |
| f,0 / f,1 / f,3 (E3) | 1.4e-5 / 4.8e-5 / 1.0e-4 | x9.13 |
| fX,0 / fX,1 / fX,2 / fX,3 (E3) | 5.8e-6 / 3.8e-5 / 4.9e-5 / 8.8e-5 | x2.43 |
| h,0 / h,1 / h,3 (H) | 5.3e-5 / 1.9e-4 / 3.9e-4 | x17.7 |
| hX,0 / hX,1 / hX,2 / hX,3 (H) | 1.8e-5 / 1.2e-4 / 1.5e-4 / 2.7e-4 | x3.76 |
| DYY | 5.8e-5 | x6.29 |
| DY,0..3 | 3.6e-5 .. 5.5e-4 | x31.9 |
| TT, e, eX, z, wXw, wXwX, TX,a,b | not binding for this pair | x336 or more |

- **Global requirement** (every S8 row below its m0 at 2x, plus S8-3 by its better route; sent to pk03). The common factor on each
  set of groups, others at their bars:

| set | crude N4 | crude N3 | AL N4 | AL N3 |
|---|---|---|---|---|
| all groups | x0.671 | x1.36 | x1.46 | x1.48 |
| leakage g, T, TT | x0.0165 | x1.47 | x1.46 | x1.48 |
| residual (S4, E3, H, E2, FF, DY, DYY) | x0.558 | x1.48 | x2.67 | x2.60 |
| T alone | cannot (1.75 at x1e-3) | x17.2 | x12.7 | x18.2 |
| TT alone | cannot (1.88 at x1e-3) | x1.48 | x1.47 | x1.50 |
- **M2 (pk02).** The KV record per plan v2 Section 6, with Section 7's safe ends: certified laws at J_lo, nonincreasing on
  [300, inf), and the C-FMT values at 300.
- **S4.** S4-U v2 (b1b6b99b), via P2's S4U_KV_v1 reader; S4-TRB (91109301), one constant per N, for beta in Delta.
- **P2 export (T3).**
  - File pk07/out/export_kt_s67_cert_v2_2_sweep.kv, sha256 2520bfb9..., printed on the EXPORT line of a run whose VERDICT is VALID.
  - Code kt_s67_cert_v2_2.py (0718efcc). Reader pk07/kt_s67_export_reader_v1.py (aaaa4c97); KV layer s4u_kv_ref_v1.py (ce0ba6f4).
  - FIELDS = jlo jhi c5_lo vSv_p_lo vSv_m_hi rp_lo rho_hi rho1_hi vp2_lo vp2_hi vm2_hi Bp_hi Bm_hi cx_lo r2_hi ro_hi Rw_hi c_lo c_hi.
    P2's |B+| is the author's max(beta, c+(1 + eps_r))/(1 - eps_r).
  - S8 uses: c5_lo (bulk + delta); Bp_hi and Bm_hi (|B+-|); Rw_hi and rho1_hi (e_d, e_R); c_lo and c_hi.
  - Import rules:
    - V1: read jlo and jhi with float(token), not as exact decimals.
    - V2: pin only an export sha printed on an EXPORT line of a run whose VERDICT is VALID.
  - EXPORT_STATUS must read CERTIFIED before S8 counts anything as certified. Today it reads FLOAT-PASS, until M2 and M3 are certified.

## 9. F2 uniformity (pieces in J)
- **Entries:** sum_{k<=3} a_k t^k plus the constant bar, valid for every J >= 300 including t = 0. Each bar part is nonincreasing in J,
  with its reason stated.
- **The rest:** M2 laws at J_lo; lambda_0 as in Section 7; U as P2's F2; TRB constant.
- **Pieces:** P2's grid, with ratio <= 1.0025 on [300, 400] and <= 1.01 beyond, J_max >= 1e6, and [J_max, inf) as one piece to t = 0.
  The P2 import follows V1/V2.
- **Evaluation:** interval evaluation on each piece's t-interval and bar box. Ritz data, G, eta, s_perp, the residuals, Weyl/DK and
  R(k) are computed per piece.
- **Centered forms:** mean-value forms in t where a cancellation exceeds 10x (P2's four port conditions). C-MV, C-PIECE and C-UNIF as
  in P2.

## 10. Controls and plants (M1)
- **Gates:**
  - C-HASH;
  - C-FMT per producer's reader, with key-swap plants;
  - C-TAG allowlist (P2's F1);
  - C-MAIN; C-ENDW (against the certified e,0 and z);
  - C-RITZ0; C-PAR (exact parity zeros of z9sym, relative 1e-11 at a_0 and a_1, 3c's form);
  - C-MIRROR;
  - C-HARM (t = 0);
  - C-M3NORM (this run's entries against M3's records);
  - C-SF0 (t = 0: the exact closed form lies in [Cov_lo, Cov_hi] for the one-sided classes d = -1..2, m <= 16, and every two-sided
    pair of the strips n = 4..12 with both ends near; 3d/3e: 288 classes, largest ratio 0.998 / 0.999);
  - C-BULKSPLIT; C-REPRO (certified central values against 3e, gap reported);
  - C-MV, C-PIECE, C-UNIF.
- **Plants (each must fire):**
  - PLANT-END, PLANT-ODD, PLANT-PARITY (an explicit 1e-12).
  - PLANT-T1.
  - PLANT-SF0 (C-SF0 with every truncation set to 0 must fail; 1.5e7 / 1.1e7).
  - PLANT-M3NORM.
  - PLANT-PRECERT: every reader refuses a PRECERT (or STUB) copy of a valid record (Section 8's VERDICT rule).
  - PLANT-LEAK, self-calibrating as M1 asks: the eta factor F at which the binding lemma class loses Cov_lo > 0. It must hold at F/1.1
    and fail at 1.1 F (3d: F = 1409 / 210).
  - PLANT-OVERLAP, self-calibrating on the Davis-Kahan sin(theta) factor for the binding top-mode class (3d: F = 17.2 / 20.6).
  - Margin plants for the bars, the vacuum terms and U (P2's S1/D2).

## 11. Kill rule and the decision rule
- **Kill rule.** Stop and report if any certified margin is <= 0, or below 2x its bar, for any class and piece; or if a route's
  truncation exceeds half its margin (headroom < 2).
- **Decision rule**, once pk03's float probe replaces Section 5.5's analog bars:
  - Rerun 3e's propagation on those bars. If the crude route clears every row at 2x, S8 needs no new entries.
  - Otherwise, activate the AL graph if M3 can run it at a price main accepts, or tighten the groups the requirement list names. Both
    are checked first by the same float reading.
- **Hardest sub-case.** N4, S8-2 with both ends at d >= 1 at m = 1: (2,1) at 1.73 crude on the analog bars. With AL every row is
  >= 4.11.

## 12. Order, pieces and price (this item)
1. The review reviews this SPEC. In parallel, pk03 returns float bars for the S8-specific entries and prices AL.
2. A float re-reading on those bars: 3e's code with the new bar table, about 0.03 core-h. Piece 3 has 0.060 core-h left of its 0.2
   (0.1399 used).
3. Assembly code kt_s8_cert_v1, with readers, pieces, plants and the S8-mono evaluation: 7-9 h, < 0.5 core-h, checkpointed
   pieces under 10 min.
4. A dry run on M3's first records: 1 h, < 0.05 core-h.
5. The certified run, once M2, M3 and P2 read CERTIFIED: 1-2 h, < 0.5 core-h.
- Total for this item: 9-12 h and about 1 core-h. M3's preps (S4, H, L; AL if activated) are priced by pk03.

## 13. What this SPEC does not settle
- The real bars of the S8-specific entries. The analog model sets the global N4 reading (1.73 crude).
- AL's feasibility at K = 3 in M3's engine.
- Whether one integrand's bar scales with its size, the premise of the centered entries.

## 14. Review points, mapped
| point | where | status |
|---|---|---|
| v1 C1 vacuum terms exact | Section 7, Section 4 (rational assembly) | met |
| v1 C2 psi-hat in the pencil | Section 3, Setting 1 | met |
| v1 C3 f2 overlap with f1 leakage | no alpha bounds anywhere (Davis-Kahan, Section 6.2) | moot |
| v1 C4 S8-mono reduced form | Section 6.2, Lemma C4, one- and two-sided | met |
| v1 C5 windows certified or float | Section 6.7: chain dominates; W3/W4 named, on hold | met |
| v1 C6 coverage, D_far, S8-2 domain | Section 1 | met |
| v1 R-a budget, quadratic form, fallback | Section 5.1, Section 6.6, Section 11 | met; fixed-coefficient form shown worse |
| v1 R-b alpha-bounds too loose | Section 6.1 (lemma, no alpha) | met |
| v1 M1 PLANT-OVERLAP firing | Section 10, self-calibrating | met |
| v1 M2 S8-3 = n = 4 | Section 1 (n = 2, 3 cited), Section 6.5 | met |
| v1 M3 "five places" | Section 7 | met |
| v2 T1 lemma gap, Settings 1 and 2 | Section 3, Section 4 (T1' strengthens T1) | met |
| v2 T2 eta floor | Section 5.4 (real bars: 1.47e-2, TT-driven) | met; the floor binds |
| v2 T3 P2 export; S7 mode bound | Section 8; Section 6.2 replaces it | met |
| v2 T4 far end in every S8-1 route | Section 2, Section 6.3 (routes A, B) | met |
| v2 T5 S8-2 to n = 9, fallback named | Section 1, Section 6.4 | met |
| ADD1 W3 entries | list v2, on hold (Section 6.7) | met |
| ADD1 d = 1 budget line | Section 6.6 (0.0270; 6.93e-3) | met |
| ADD1 PLANT-LEAK firing | Section 10 | met |
| S2/S3, and rule (d) citations | Section 1: Theorems 1.5(i), 1.3(a)/4.10 and 1.4 with records | met |
| rule (a) window triggers | Section 6.7 | met |
| rule (b) F2 inputs | Section 6.2 (3d's 6.4e-3 and 0.63; recomputed per piece) | met |
| rule (c) fixed-coefficient comparison | Section 5.1 (6x) | met; the review judges against R-a |
| Rtr direction, each M2 key's safe end | Section 7 (also AE) | met |
| P2 import rules V1/V2 | Section 8 | met |
| VERDICT exact equality, PRECERT/STUB refusal | Section 8, PLANT-PRECERT | met |
| int64 MomTable limit | Section 8 (per-entry and monomial splits; arb fallback) | met |
| per-state moves | out/STATE_MOVES_z9sym_v1.txt e05ada6c | met |
| per-entry maximum-bar table | Section 8 table | met |
| global requirement per group set (T, TT) | Section 8 table | met |
| two exits for the state-3 floor | Section 6.4 (tighter TT/T,3,3; W without state 3) | met; prices partly pk03's |
| residual-entry fallback | Section 6.4 (centered entries, priced; full Gram combination not expressible) | met |
| rows between 1.2x and 2x as named risks | Section 6.4 (N4 both-ends d >= 1 at m = 1) | met |
