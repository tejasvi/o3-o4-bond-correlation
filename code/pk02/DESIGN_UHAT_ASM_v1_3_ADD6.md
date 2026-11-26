# DESIGN_UHAT_ASM_v1_3_ADD6: B''s transfer T_v, stated as computed

pk02, 2026-11-08. Sixth addendum to DESIGN_UHAT_ASM_v1_3 (faa09e23), after ADD1-ADD5. The interface review
A check asks the record's T_v_source to name the file that states the bound. v1_3 sect. 4 l.243
says "T_v is U4's T for B''s own operator"; the assembler computes the sharper bound below, so this addendum states it.

## 1. T_v (replaces v1_3 sect. 4 l.243's first sentence)
- B''s row term <eps_L, X u> is linear in u, so |alpha . C^ P X-hat (u - u-hat)| <= ||alpha||_2 beta-hat s' (the review
  l.99-101; U4's full T contains beta-hat s' and is conservative).
- So, per piece, T_v = beta-hat s', with
  - beta-hat (D4) = (1 - s^2)^-2 (A + |c_t|) ((A2/mhat_lo + c_b^2 N*_RTR)/(1 - eps_r))^(1/2), over the
    piece's D4 centre balls (ADD1 sect. 2);
  - s' = s (1 + s), s = N<N>_S_300 of M2B_KV_v1 (13cc0d9a).
- The record's bprime_hat.FA.T_v is the max over the pieces (ADD4 sect. 3), an upper end rounded up, and bprime_hat.FA.T_v_source names
  this file by path:sha256.
- R6.5 uses it as v1_3 l.243-245 say: T_FA_lo = min(x_lo, (1 - s^2)^p x_lo), x_lo = (alpha . C^ v-hat)_lo - ||alpha||_2 T_v.
