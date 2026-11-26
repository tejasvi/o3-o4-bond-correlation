# SPEC_M1_CERT_v1_1_ADD2_v1: ball arithmetic for engine A, the xi hook, and F2 (pk02)

Amends SPEC_M1_CERT_v1_1 (c81c956f) with its ADD1 (badf0f57). It supersedes pk01's unfrozen ADD2 draft (4baa4536, copied read-only as
SRC_pk01_SPEC_ADD2_draft_4baa4536.md), and carries the W3/M1 items of S9C_PLAN_v2 (d5c5dd4a) and its ADD1 (6c952761): the xi hook,
F2(a), F2(b), and C-BAD over the hook's own splits (the delta check cb89deda, l.36 and l.85-92).
- Sections 1 and 2 are the draft's, verbatim.
- Section 3 is the draft's, plus an amendment (3a).
- Sections 4 and 5 are rewritten.
- Sections 6 to 9 are new.
Written 2026-11-07 by pk02. Hand only: no script was run for this file.
Bases (read-only):
- R6a_LEMMA_C v1_1 0856e123: sect. 3.0 (positivity of K^{1/2}'s kernel), 3.1 (engine A) and 3.3 (the Lam-split);
- PK10_NOTES c4d89203, sect. 19.3.3 (v), l.1254: "the sect. 19.2 bounds control ||K^{1/2}|g| ||";
- kt_c_v2_3.py 71a224a2: engine_A l.970-1084;
- W1 results MANIFEST_W1_RESULTS_v3_1 2c0665fa: the float kappa of the |coefficient| majorant.
Marks: [D] derived here, for review; [E] estimate.

## 1. Arithmetic model (replaces M-a for engine A; M-b to M-e stand)
- Every certified quantity of engine A, the a-engine and the assembly is a python-flint arb ball (ctx.prec = 128) or an arb_mat of balls.
  arb operations are correctly rounded outward (Arb's ball arithmetic: each result ball contains the exact result for all inputs in the
  operand balls), so a computed ball contains the exact value. No *_series function is called (ctx.cap rule); arb_mat is used for inverse,
  det, products and Cholesky-type solves of small matrices.
- Inputs. Exact binary64 constants are exact balls (the json data: q1..q3, the S matrix, the radii, the m_g of the B0 projections). The
  couplings are computed in arb from their definitions (A = (3 + sqrt 21)/6, B = (3 sqrt 5 - sqrt 21)/12). Covariance matrices come from
  arb_mat Laplacians: inverses and dets in arb_mat. The gauge basis (an SVD in the float code) is replaced by an exact rational basis B of the
  orthogonal complement of the gauge vector u (u = indicator of the gauge set S; B: the differences e_s - e_s0 for s in S, and e_k for k not
  in S). For any basis B = Qb R of that complement, B (B^T L B)^-1 B^T = Qb (Qb^T L Qb)^-1 Qb^T and det(B^T L B)/det(B^T L' B) =
  det(Qb^T L Qb)/det(Qb^T L' Qb), so every covariance and normalization is unchanged.
- Integers (codes, exponents, factorials, binomials) are exact Python or numpy int64, with amom2b's code-space assertions. Index arithmetic
  (codes, searchsorted, supports, hit masks) stays in numpy int64; only values become balls.
- Transcendentals in arb: exp, log, sqrt; erfc(x), x > 0, by the bound exp(-x^2)/(x sqrt(pi)) used with nonnegative coefficients only (ADD1 b);
  chi tails as ADD1.
- Free choices stay binary64 and need no enclosure: the B0 projection coefficients m_g (Lemma C (C1) holds for any real m_g), the Chernoff
  lambda, the tilt rates, the radii. They are computed by the float code, printed, and then used as exact numbers.
- Nothing is dropped by a ball comparison: polynomial sums keep every term whose ball is not exactly zero.

## 2. The arb layer (arbeng_v1.py)
Ports, value for value, of the PK10 modules engine A uses, with numpy index arrays and Python-loop ball accumulation:
- AllMom2A (amom2b): codes and minors as amom2b, minors' dets of the arb Gram matrix, the Euler recursion by scatter accumulation;
  E and E2 by ball dot products.
- CondMomA (condexp2), with the same supports, caps and table format; CondGA (condg) shift maps; WishartA (wishart).
- Polynomial and series arithmetic on dicts with ball coefficients (pseries, sigma_to_g); majorants (npoly products of the D4, R0, pi and
  h polynomials) as dicts or code arrays with ball coefficients.

## 3. kt_cert_v1.py (items as kt_c_v2_3: e1, e3, h, a per N, then r per N)
- Explicit part: the series to order 3, condE (CondMomA at Dc = 8), the residual polynomials r1, r2, r3 with the float m_g fixed.
- Engine A: nP (WishartA), the D4 majorant, nD (CondMomA at Dc = deg2, CondGA, WishartA, det factor), the R0 majorant and nR0, the tails
  tailX, tailB, ann (AllMom2A joint moments, arb exp, the erfc bound). The a-engine: nP and nR as above.
- FLOAT inputs, marked and listed in the output: the outer far parts (outer_far3: riglap3 majorants, tree bounds) and gB (riglap2.bound on
  G4 - r), both Lemma 19.1-type bounds of milestone M3; eps_r and s (M2); Hbad, Gbad, Abad and supp0 (M4). Their float values enter as
  binary64 numbers. At J = 300 (e1, N = 4) they are far 1.2e-17, gB 1.8e-11 against a bound of 7.1e-4.
- Assembly: kt_rb_v1_5's certified KT-RB bars and Lemma A in arb, with the four engine bounds from the items.
- The xi-insertion hook: engine A takes source kinds h_b = xi_h p_b, b in {psi-hat, e1, e3}, with xi_h on the middle
  horizontal bond (M, M''); h_psi-hat is kt_c_v2_3's kind 'h' and must reproduce it (C-HOOK0). Per part, generalizing 'h':
  - explicit part: the source series is Series(xi_h) x Series(p_b) (orders 0-3), B0-projected on {psi-hat, e1, e3}; for b = e1, e3 the
    order-0 residual is not zero (xi_h p_b has harmonic components outside P(0)) and enters nP as t^0 r_0, so the K-H0-type vanishing
    check applies to h_psi-hat only;
  - D4: pis = pi_hb(j) = sum_l C(j, l) xibar_cross_l pi_state(j - l, b) (pi_h with pi_state in place of pi_vac);
  - ann: pi_hb(0) at a_pp; gB: supF = 2J sup|p_b|; outer far: (2J)^2 outer_far3 with the state factors of b (as 'h' does with p0);
  - basis side (l0_remainder, far_basis) unchanged.
  It gives ||Q K^{1/2} V K_xi phi_b|| for S9C_PLAN_v2 (C8)'s vacuum term E3 (with the f_c parts by the Lam-split).


### 3a. Amendment to sect. 3 (pk02)
- **Items per N:** e1, e3, h, a, and the hook kinds h1 = xi_h p_e1 and h3 = xi_h p_e3; then r per N.
  - h is h_psi-hat, kt_c_v2_3's kind. C-HOOK0: the ball midpoints of every part of h (nP, nD, nR0, tailX, tailB, ann, gB, far) equal kt_c_v2_3's
    printed float parts to 1e-6 relative.
  - Each item prints its m_g (lambda_h units, EXPLICIT lines as kt_c_v2_3) next to its bound, so W2 uses the same m_bg as engine A.
- **The hook's outputs** are the bounds R^xi_b >= ||Q K^{1/2} V K_xi phi_b||/(lambda_h ||psi_b||), b = psi-hat, e1, e3.
  - They give H^Q's phi-part, sum_g |m_1g| R^xi_g with the normalizations of S9C_PLAN_v2 sect. 6 and ADD1 sect. 2 line 6.
  - For the hook the signed form suffices: Q K^{1/2} phi_g = 0, so ||Q K^{1/2} V K_xi phi_b|| <= ||K^{1/2} f_hb||, with
    f_hb = V K_xi phi_b - sum_g m_g^(hb) phi_g for any real m_g^(hb).
- **H^Q's f-part,** Lam R_1^{|f|} with Lam = 60 (ADD1 sect. 1), is not an engine output. It uses F2(a) (sect. 6), and its bad part is ADD1's
  H_b, counted by W2.

## 4. Validation (each run under its own approval, <= 0.1 core-h) [rewritten]
- **kt_arbval_v1, the layer** (as the draft's sect. 4):
  - C-AF: every ported table equals the float module on engine A's own inputs at N = 4, J = 300 (CondMom at Dc 8 and 10, CondG, Wishart,
    AllMom2 joint moments, E2 values), at the ball midpoints, to 1e-10 of the table's largest entry;
  - C-RAD: every radius is below 1e-20 of that largest entry;
  - PLANT-AF (one float value perturbed by 1e-9 of the largest) must fire.
- **kt_cert_v1 smoke, the e1 item at N = 4:**
  - C-REP: kt_c_v2_3's printed float parts (nP, nD, nR0, tailX, tailB, ann) reproduced at the ball midpoints to 1e-6 relative;
  - C-RAD: relative radii below 1e-12.
- **kt_cert_v1 hook smoke, the h item at N = 4:** C-HOOK0 (sect. 3a). PLANT-HOOK0: the same item with the xi factor's coefficient scaled by
  1.01 must fail C-HOOK0.
- **Production** (every item at both N, then the r items) only under its own approval.

## 5. Price [E] [rewritten]
- Part: the layer 3-5 h and kt_cert_v1 5-9 h (the draft's), plus 2-3 h for the hook kinds and sect. 6-8.
- CPU at 128 bits, from pk01's probe (kt_arbprobe_v1: CondMom pieces 92 s and 55 s): engine A takes 250-300 s per item.
  - The 12 engine items (e1, e3, h, h1, h3, a at both N) come to about 0.9-1.0 core-h.
  - The r items take seconds.
- Validation runs <= 0.1 core-h each: kt_arbval_v1 about 0.05; the e1 smoke and the h smoke about 0.09 each.

## 6. F2(a): engine A's bound holds for |f| [D]
**Claim.** For every kind (e1, e3, and every hook and vacuum kind), engine A's output
B = (near^2 + far_out)^{1/2} + gB bounds ||K^{1/2}|f| ||/(lambda_h main_D^{1/2}), not only ||K^{1/2} f||.
So R_b^{|f|} := ||K^{1/2}|f_b| ||/(lambda_0 ||psi_b||) <= B_b/(lambda~_0 Z_b^{1/2}): the same number as R_b in (C1).

**Proof,** piece by piece (kt_c_v2_3 l.970-1084). This is PK10 19.3.3 (v)'s argument for the vacuum residual g ("all of them are bounds
for positive kernels or Cauchy-Schwarz in the near region"), written out.
- **(i) Weighted one-column norms are Schur bounds.**
  - Let K be a nonnegative symmetric kernel and w > 0. By AM-GM, |h(s)||h(s')| <= (h(s)^2 w(s')/w(s) + h(s')^2 w(s)/w(s'))/2. Integrating
    against K gives <|h|, K|h|> <= int h^2 (K w)/w.
  - Take h = W P and w = W. The right side is int W P^2 (K W) = <W P^2, K W>: the D-graph integral with P^2 on one column and 1 on the other.
  - Engine A evaluates exactly that quantity as n E_G[P^2], with G the tilted D-graph covariance restricted to one column (tilted_cov(LD,
    BD, rates), then Wishart on G[:3, :3]).
  - The tilts (rates c_m t, c_e t) are upper bounds on the density of the spin measure relative to the Gaussian one, so they only enlarge
    the integral.
  - Hence nP, nR0 and nD bound the |.|-form norms of their pieces. Here P is, respectively, the explicit residual, the L0 remainder
    majorant, and the D4 majorant times detf, each squared inside the expectation.
  - The tails tailX, tailB and ann are one-column norms of T3 and pi_hb(0) under tilted Gaussians and chi-tail factors, so the same holds.
- **(ii) Pointwise majorants.** On the near region, the Taylor remainders of L1 F and of the L0 side are bounded in absolute value by the
  majorants (D4 with detf, and R0). So |f 1_near| <= |P| + |Rem_L1| + |Rem_L0| pointwise, and each term's |.|-form norm is bounded by (i).
- **(iii) Far and bad parts.** far_out (riglap3 majorants on the outer far region, and the truly far sup|F| times tree bounds) and gB (sup|F|
  times riglap2 bounds) are sup-type or positive-kernel bounds of |f| on their regions.
- **(iv) Combination.**
  - |f|^2 = |f|^2 1_near + |f|^2 1_far pointwise. The near and far regions are disjoint in the outer column, so their weighted L2 norms add
    in quadrature, giving (near^2 + far_out)^{1/2}.
  - The bad-bond part enters by the triangle inequality: + gB.
  - No step uses the sign of f, and none uses Q. The one step that uses Q, ||Q T psi_b|| <= ||K^{1/2} f_b||, lies outside the engine and is
    not needed for |f|.
- **(v) The m_g.** Any real m_g are allowed (C1). The |f| form uses the same m_bg as the (C9) assembly, so W2 reads them from the e1 and e3
  items.

**What kt_cert_v1 prints.** For b = e1, e3: "R_b^{|f|} <= [ball]", the same ball as R_b, citing this section.
- the check C-F (R_b^{|f|} >= R_b) holds with equality, since both are the same ball.
- Use in S9(c), certified: line 2, line 5 (the cross terms) and line 6's f-part. The joint limit (certified R_1^{|f|} <= 3.72 x float at
  N = 4; the review delta 3.724x) applies to the ball's upper end.

## 7. F2(b): a certified majorant for kappa_g [D]
- **Need:** kappa_g >= ||K^{1/2}|phi_g| ||/||psi_g|| for g = psi-hat, e1, e3. It enters S9(c) line 5 (the H_bc cross terms) and nothing else.
- **Schur bound** (sect. 6 (i), with h = phi_g = W p_g and w = W):
  ||K^{1/2}|phi_g| ||^2 = <|phi_g|, K|phi_g|> <= <W p_g^2, K W> =: main_D S_gg, so kappa_g^2 <= S_gg/G_gg.
  - S_gg is a 2-column entry like G_gg, with the job [p_g(L), p_g(L)]: both factors on one column, Q-degree <= 4, one group of about 6
    forms.
  - Its a_k and its J = 300 remainder come from the entry machinery (riglap5s). kt_cert_v1 recomputes the a_k in arb with AllMom2A. The
    remainder stays FLOAT (M3), as for every Gram entry.
- **The |coefficient| majorant** G+_gg (kappa^2 <= G+_gg/G_gg) is also valid. W1's float values are 1.0013 / 6.49 / 19.9 at N = 4 and
  1.0006 / 5.33 / 16.3 at N = 3. W2 takes kappa_g = min of the two routes.
- **Expected [E].** By symmetry S_gg/G_gg = 1/corr(p_g(s), p_g(s')), the (uncentred) correlation of one polynomial on two adjacent columns
  under the D-graph measure.
  - For g = 0 it is 1.00; W1's kappa_0 = 1.0013 agrees.
  - For g = 1, 3, a correlation of 0.1-0.5 gives kappa of about 1.4-3.2, against 6.5 and 20 from G+.
  - With kappa = 3 for g = 1, 3, the N = 4 kill evaluation (KILLEVAL 7401de9f) would have line 5 at about 4.0e-7 instead of 9.6e-7, and
    the total at about 0.61 of the kill line instead of 0.700.
- **Proposal (the call):** a float follow-up job, kt_kappa_v1, on the existing 2-column prep computes S_gg for g = 0, 1, 3 at both N, at
  seconds per N. W2 could then drop the G+ values before M1's certified a_k exist.
  - Gates: C-S1 (S_gg >= G_gg, Cauchy-Schwarz) and C-S0 (S_00/G_00 within 1e-3 of 1).

## 8. C-BAD over the hook's own splits [D]
- **Scope.** the review (delta l.36): if engine A splits xi_h internally, the bad parts of those splits must be counted, so C-BAD's scope
  includes W3.
- **What engine A splits for a hook kind.** It has no Lam-split of xi_h. It splits the configuration space:
  - On the near region, xi_h enters the D4 majorant through Q_MM'' <= 2 X_M + 2 X''_M.
  - On the outer far region and the bad bonds it is bounded by 0 <= xi_h <= 2J. These far-side pieces are the hook's bad parts.
- **kt_cert_v1 prints,** for each hook kind h_b (b = psi-hat, e1, e3), as separate balls:
  - gB_hb = 2J sup|p_b| x gB_base;
  - the outer far part, (2J)^2 outer_far3 with b's factors, plus far_basis;
  - the tails tailX, tailB and ann.
- **W2's sum.** W2 adds X sum_g |m_1g| (gB_hg + far_hg)/(lambda~_0 Z_g^{1/2}) to C-BAD. The weight is line 6's: H^Q multiplies X, about
  1.1e-5 at N = 4.
- **Scale [E].** From kt_c_v2_3 (e1, N = 4: gB 1.8e-11, far 1.2e-17), with the hook's factors 2J and (2J)^2, this is at most about 1e-8 x
  1.1e-5, negligible against C-BAD's 1e-9. It is printed and counted all the same.
- The f-part split (Lam = 60, ADD1 sect. 1, H_b) belongs to W2, not to the engine.

## 9. Open questions
1. Sect. 6: is the piece-by-piece argument that engine A's bound holds for |f| complete? In particular (i): are the tilted one-column norms
   Schur bounds with w = W?
2. Sect. 7: kappa by Schur, kappa_g^2 <= S_gg/G_gg, and taking the min with W1's G+ route.
3. Sect. 8: is the list of the hook's own splits complete for C-BAD?
