# HS_TYPEB_LEMMA_NOTE_v1_1: the first-column lemma for ||Q0 X* a|| at d_L = -1 (D3 type-B rows), split and crude forms (revises v1)
pk08, written 2026-11-08T11:03:56Z (date -u).

Note: no code, no run. Brief: the approval of 2026-11-08 for the type-B first-column lemma (D3 at d_L = -1: pk11's DESIGN_P2_12_v1_5,
sect. 3, option (b)). It asks for the lemma in its split and crude forms with every step, as for D3, for the review. It builds on
Lemma D3's operator bounds (HS_NORMX_D3_LEMMA_v1, S1-S6).
v1_1: the REVIEW_HS_TYPEB_LEMMA_NOTE_V1 (3684b492) found Lemma B SOUND in both forms and asked for one fix, which is made here: a is in
L^2, so v1's extension paragraph in sect. 1 is withdrawn and replaced. Nothing else changes.
Marks: [D] derived here; [D, awk] a float hand number from awk; [E] estimate. path:sha8 tokens are in sect. 7.

## 0. Answer first
- **Lemma B** [D]. Let a = S'^-1 w-hat, which is S8's l(-1) carried to d_L = -1. Let X = X_c(D3) as in v1_2, with the true lambda_0, and
  q = ||Q0 X* a||. Then for every J > 0 and real c_t, c_bb:
  - split form: q <= ||Q0 X* u|| + (A + |c_t|)(A + |c_bb|) tau;
  - crude form: q <= (A + |c_t|)(A + |c_bb|) (1 + tau^2)^(1/2);
  - with A = (N-1)/2 and tau = tan of the angle between V^(1/2) and psi = Z* u/lambda_0^(1/2) (the top eigenvector of Z* Z), so
    tau^2 = lambda_0 v_0^2/<u,w>^2 - 1.
- **Inputs.**
  - The two G bounds of Lemma D3 (S4).
  - ||Z|| = lambda_0^(1/2).
  - int V = v_0^2 exactly.
  - A certified upper end of tau over the J grid, from lambda_0's upper end and <u,w>'s lower end. Its source is open with pk11
    (S8 spec sect. 7 item 4).
  - For the split form, a certified ||Q0 X* u||.
- **Sizes** [E: R_w certified (S9 export), RQ at t = 0] at pk15's box ends:
  - tau is about 0.595 (N4) and 0.473 (N3).
  - Crude: 7.63 (N4), 3.27 (N3).
  - Split slope (A + |c_t|)(A + |c_bb|) tau: 3.90 (N4), 1.40 (N3).
- **Rows** (DESIGN_P2_12_v1_5 sect. 3, q_need at the first piece, N4 / N3):

  | d_R | q_need | crude (N4 / N3) | result |
  |---|---|---|---|
  | 2 | 5.89 / 5.29 | 7.63 / 3.27 | N3 closes; N4 only by the split form (needs ||Q0 X* u|| <= 1.99) |
  | 3 | 41.3 / 38.3 | 7.63 / 3.27 | both close |
  | 4, 5, 6, far, inf | 193-509 / 180-473 | 7.63 / 3.27 | all close |

  - So 13 of 14 close by the crude form once tau_hi is certified near its estimate. N4 (-1,2) closes by the split form with a certified
    ||Q0 X* u|| <= 1.99, or stays open.

## 1. Objects
- As in HS_NORMX_D3_LEMMA_v1 sect. 1:
  - L, H, P_H; K = K_T (x) K_M (x) K_B; V; Z = K^(1/2) V^(1/2);
  - T = Z Z*, Th = Z* Z, and lambda_0 = max spec(T), attained on H;
  - G_t = V^(1/2) (K_t - c_t K) V^(1/2) and G_bb likewise, both self-adjoint with real symmetric kernels;
  - X = Z G_t G_bb Z*/lambda_0^3, which is v1_2's OPERATOR_D3 with the true lambda_0.
- u is T's top eigenvector in H, with norm 1. psi = Z* u/lambda_0^(1/2) has norm 1 (||Z* u||^2 = <u, T u> = lambda_0), and
  Th psi = Z* (Z Z* u)/lambda_0^(1/2) = lambda_0 psi.
  - Th has a strictly positive continuous kernel, so by Jentzsch psi is its positive top eigenfunction. Fix u's sign so that psi > 0.
- w = K^(1/2) V 1 = Z V^(1/2), where V^(1/2) is the function sigma -> V(sigma)^(1/2), which lies in H.
  - w-hat = w/<u,w> (S8 spec l.106), with <u,w> = <Z* u, V^(1/2)> = lambda_0^(1/2) <psi, V^(1/2)> > 0.
- S' = T/lambda_0, and a = S'^-1 w-hat (DESIGN_P2_12_v1_5 sect. 3; S8's l(-1) = w-hat). Q0 = 1 - |u><u|.
- **a is in L^2** (the fix to v1).
  - 1 is the l = 0 eigenvector of each K_r, with eigenvalue v_0, so K^(1/2) 1 = v_0^(3/2) 1.
  - Hence T (v_0^(-3/2) 1) = K^(1/2) V K^(1/2) v_0^(-3/2) 1 = K^(1/2) V 1 = w. T = Z Z* is injective, because Z* = V^(1/2) K^(1/2) is.
    So T^-1 w = v_0^(-3/2) 1.
  - a = lambda_0 T^-1 w-hat = (lambda_0/(<u,w> v_0^(3/2))) 1, a constant function in H.
  - Z* a = V^(1/2) K^(1/2) a = (lambda_0/(<u,w> v_0^(3/2))) v_0^(3/2) V^(1/2) = (lambda_0/<u,w>) V^(1/2). This is the design's "Z* a is
    proportional to V^(1/2)", with no extension needed.
  - X* a = Z G_bb G_t (Z* a)/lambda_0^3, since X* = Z G_bb G_t Z*/lambda_0^3 (the G are self-adjoint).

## 2. The steps [D]
- **B1 (split along psi).** Write V^(1/2) = alpha psi + beta y, with y a unit vector orthogonal to psi in H, alpha = <psi, V^(1/2)> > 0 and
  beta real.
  - Then alpha = <u,w>/lambda_0^(1/2), so lambda_0 alpha/<u,w> = lambda_0^(1/2).
  - Hence Z* a = lambda_0^(1/2) psi + (lambda_0 beta/<u,w>) y = Z* u + (lambda_0 beta/<u,w>) y.
- **B2 (the psi part is X* u).** X* a = Z G_bb G_t Z* u/lambda_0^3 + (lambda_0 beta/<u,w>) Z G_bb G_t y/lambda_0^3
  = X* u + (lambda_0 beta/<u,w>) Z G_bb G_t y/lambda_0^3.
- **B3 (operator bounds; Lemma D3's S4 and ||Z||).** On H, ||G_t|| <= (A + |c_t|) lambda_0, ||G_bb|| <= (A + |c_bb|) lambda_0, and
  ||Z|| = ||Z Z*||^(1/2) = lambda_0^(1/2).
  - So ||Z G_bb G_t y|| <= (A + |c_t|)(A + |c_bb|) lambda_0^(5/2).
- **B4 (split form).** ||Q0 X* a|| <= ||Q0 X* u|| + (lambda_0 |beta|/<u,w>) (A + |c_t|)(A + |c_bb|) lambda_0^(5/2)/lambda_0^3
  = ||Q0 X* u|| + (A + |c_t|)(A + |c_bb|) |beta|/alpha, because lambda_0^(1/2)/<u,w> = 1/alpha. Put tau = |beta|/alpha.
- **B5 (crude form).** ||Q0 X* a|| <= ||X* a|| <= ||Z G_bb G_t|| ||Z* a||/lambda_0^3 <= (A + |c_t|)(A + |c_bb|) lambda_0^(5/2)
  (lambda_0/<u,w>) ||V^(1/2)||/lambda_0^3 = (A + |c_t|)(A + |c_bb|) ||V^(1/2)||/alpha = (A + |c_t|)(A + |c_bb|) (1 + tau^2)^(1/2).
- **B6 (tau and v_0).** tau^2 = (||V^(1/2)||^2 - alpha^2)/alpha^2 = lambda_0 ||V^(1/2)||^2/<u,w>^2 - 1.
  - ||V^(1/2)||^2 = int V dsigma = v_0^2: integrate s_T and s_B given s_M, each a zonal integral equal to
    v_0 = int_{S^(N-1)} e^{J(s.e - 1)} ds, the l = 0 Funk-Hecke value. So v_0 = (1 - e^{-2J})/(2J) at N = 3 and 2 e^{-J} I_1(J)/J at N = 4.
  - With R_w = ||Q0 w-hat|| (S8), <u,w>^2 = ||w||^2/(1 + R_w^2), so tau^2 = (1 + R_w^2)/RQ - 1 with RQ = ||w||^2/(lambda_0 v_0^2) in (0, 1].
    RQ is the Rayleigh quotient of Th/lambda_0 at V^(1/2).
- **Certified form.** tau^2 <= lambda_0,hi v_0^2/<u,w>_lo^2 - 1, with lambda_0's upper end and <u,w>'s lower end over the J grid, in one
  unit. Both bounds increase in |c_t|, |c_bb| and tau, so the sup over a c box is at |c| largest.

## 3. Sizes [D, awk; E for RQ]
- RQ at t = 0, from the strip Laplacians (riglap2's main terms, the normalized-measure area and 2 pi/J factors cancelling):
  - RQ_h = ||w||^2_h/(lambda_h v_0^2_h) = (d3/(15 d2))^((N-1)/2).
  - d3/d2 = PR^(2/(N-1)) = 12.5437544346, from S4's PR in the TRB record. 15 is the 2 x 3 grid's spanning-tree count, which is
    det_red of the open 2-column strip ||w||^2; det_red of the 1-column strip is 1.
  - RQ_h = 0.764723 (N4) and 0.836250 (N3).
- R_w,hi from the S9 export: 0.188825 (N4) and 0.153893 (N3). tau^2 is about 0.354287 (N4) and 0.224135 (N3); tau is about 0.59522 and
  0.47343.
- At pk15's box ends (c_t, c_bb <= 1.06 at N4, 0.72 at N3):
  - crude 6.5536 x 1.163741 = 7.6267 (N4) and 2.9584 x 1.106406 = 3.2732 (N3);
  - slope 3.9008 (N4) and 1.4006 (N3);
  - N4 (-1,2) closes by the split form iff ||Q0 X* u||_hi <= 5.89 - 3.9008 = 1.9892.
- RQ at J >= 300 differs from RQ_h by O(1/J). The certified tau_hi must come from certified ends over the grid, not from RQ_h.

## 4. What remains for the rows
- The certified tau_hi over the J grid, from existing records if S8's chain exports <u,w>'s lower end ("through q - sp") together with
  lambda_0's upper end; otherwise the open 2-column strip ||w||^2 is a new certified integral, priced before any build.
- For N4 (-1,2): a certified ||Q0 X* u|| (route 0's L0 value from R6.4), else the row stays open.
- The export: the combined lemma-form record (ADD1 shape) with type-B keys, as proposed to pk15 (crude and slope per N).

## 5. For the review
1. Sect. 1: a = (lambda_0/(<u,w> v_0^(3/2))) 1, from K^(1/2) 1 = v_0^(3/2) 1. This is the fix to v1, and v1's extension paragraph is
   withdrawn.
2. B1-B2: alpha = <u,w>/lambda_0^(1/2), and the psi part of Z* a is exactly Z* u.
3. B3-B5: Lemma D3's G bounds on H, ||Z|| = lambda_0^(1/2), and the two forms.
4. B6: int V = v_0^2, and tau^2 = (1 + R_w^2)/RQ - 1.
5. The sign convention: psi > 0, so alpha > 0.

## 7. Sources (sha256sum at assembly)
- pk08/HS_TYPEB_LEMMA_NOTE_v1.md:822bb71a
- rv01/REVIEW_HS_TYPEB_LEMMA_NOTE_V1_rv01.md:3684b492
- pk08/HS_NORMX_D3_LEMMA_v1.md:19530995
- rv01/REVIEW_HS_NORMX_D3_LEMMA_V1_rv01.md:7e7af25e
- pk08/HS_NORMX_LEMMA_NOTE_v1.md:1340a52c
- pk11/DESIGN_P2_12_v1_5.md:1713cce3
- pk11/SPEC_S8_CERT_v1.md:c0f95398
- pk07/out/export_kt_s9h_v1_2_vsweep.kv:761084be
- pk08/S4_TRB_CERTIFIED_v1.md:91109301
- pk15/SPEC_HS_INV_NORMX_v1_2.md:84f6a3e0
- pk15/SPEC_HS_INV_NORMX_v1_2_ADD1.md:f2ad58c9
