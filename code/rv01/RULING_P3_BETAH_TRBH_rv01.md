# Rule: beta_H from the certified TRB_H record (pk07 P-3 for kt_s9h_v1_1)

Stamp: 2026-11-07T20:10:09Z

## Inputs
- pk15/HZ_PLAN_v1_1.md ebee9574: SH4 at l.130-151, Use at l.139-142, harmonic sizes at l.143.
- pk08/S4_TRBH_CERTIFIED_v1.md bb53005c, closed in its review.
- The review of H-BESSEL (with c_N = 2 + (N-1)(N-3)/8; P_L >= 0).
- The review of kt_s9h_v1_1 (P-3).

## 1. Answer first
(a), (b) and (d) are CONFIRMED, (b) with three conditions. (c) goes to pk15.

- **(a) Row T is the t bond and row M is the h bond. CONFIRMED.**
  - At t = 0 the diagonal <u, P_L u>/lambda_0^2 equals the harmonic (N-1)/2 - c_e (SH4 l.143): 0.4991 (t) and 0.6547 (h) at N4, 0.3327 and 0.4364 at N3.
  - A trace is at least its diagonal. TRB_H(T) at t = 0, d0 = 0.52681 (N4) and 0.35542 (N3), lies below h's diagonal at both N, so row T cannot be the h bond. With two rows and two kinds, T = t and M = h.
  - The other pairing fits: d0(M) = 0.67904 >= 0.6547 and 0.45422 >= 0.4364. The excess of each trace over its diagonal (about 0.028 and 0.024 at N4) is the size of the other modes' share, as for U.
  - The provider should print this check per row (trace >= harmonic diagonal) as a guard.
- **(b) beta_H = max((N-1)/2 - c_e, ||P_L||/lambda_0^2), with ||P_L|| <= tr_H P_L. CONFIRMED.** P_L >= 0, since L_r^2 >= 0 commutes with K >= 0, so the trace bounds the norm on H. Conditions:
  - **B-1. lambda_h is not lambda_0.**
    - TRB_H is normalized by lambda_h, the reference set by PR (strip-graph determinants), and SH4's bound needs lambda_0, the true top eigenvalue. S8 already carries their ratio: U_hi/lam0^2 in s_perp.
    - So ||P_L||/lambda_0^2 <= TRB_H x (lambda_h/lambda_0)^2, with (lambda_h/lambda_0)^2 <= 1/((1 - eps_r) mhat)^2 <= 1/(1 - eps_r)^2, using C-MHAT (mhat >= 1 for every J >= 300) and eps_r from M2(b)'s law.
    - The factor is 1 + O(1e-9), but it belongs in the bound. It makes beta_H wait on M2(b)'s certified law, which is on HOLD for F-2, as kt_s9h_v1_1 does anyway.
  - **B-2. Per piece, take the supremum over the piece's whole t-range, or use a J-uniform constant.**
    - U3_p(T) decreases in t at N4 (d1, d2, d3 < 0), so its supremum over a piece sits at the piece's largest J, not at its left end J_lo.
    - At N3 row M, d1 = +0.00795, so the cubic is not monotone.
    - The simplest sound form is the J-uniform constant d0_HI + sum_{k>=1} max(d_k_HI, 0) 300^{-k} + R_CERT:
      - N4: 0.527562 (T) and 0.679549 (M);
      - N3: 0.355588 (T) and 0.454359 (M).
      It costs at most about 1e-3 against the per-piece values (0.52668 at t = 1/300, N4 T).
  - **B-3. c_e enters twice.**
    - The max's first argument needs c_e's lower end.
    - SH4's validity condition c_e <= (N-1)/2 - eps_H, with eps_H <= c_N t, needs its upper end: c_e_hi <= (N-1)/2 - c_N/300. At N4 that is 1.4921, against harmonic c_e(t) = 1.0009.
    - Until pk15's certified c_e(J) exists, the provider can check that the TRB_H term dominates, i.e. c_e_lo >= (N-1)/2 - (that term): 0.9724 at N4 t, against harmonic 1.0009, a 2.9% margin. It can then use the TRB_H term alone. Either way, c_e must be certified.
  - The resulting beta_H(t, N4) = 0.5276 x (1 + O(1e-9)) sits below today's FLOAT 0.549.
  - SH4 l.141's block bound, lambda_max [[alpha, |b|], [|b|, tr P_L - alpha]], would bring it close to 0.50 once alpha and |b| are certified. It is optional.
- **(d) One full-norm beta_H for both parities. CONFIRMED.**
  - Row T's insertion is not F-invariant: F maps row T to row B. So B_e mixes the T <-> B sectors, and every block (++, --, +-) is bounded by ||B_e||. The full norm covers both parities.
  - It also covers the u-perp case, since ||Q0 B_e Q0|| <= ||B_e||.
  - SH4 l.142's u-perp form, with rho_1^2 in place of 1 in the first argument, is tighter but not needed.
- **(c) A certified c_e(J) for both kinds: pk15's SH4 item.** B-3 states what the provider needs from it: a lower end for the max and an upper end for the validity condition, J-uniform or per piece over the piece's whole range.
