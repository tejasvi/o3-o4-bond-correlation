# FACTS USED [S] (beyond R1-R6):
#  (L2) For edges e (left) and f (right) with left vectors J_L (plain), I_L (e inserted) and right vectors J_R, I_R at the boundaries next
#   to them and k factors T~ between: Cov(s_e, s_f) Z^2 = <J_L ^ I_L, (Lambda^2 T~)^k (J_R ^ I_R)> (Cauchy-Binet; Z = <J_L, T~^k J_R> > 0).
#   Lambda^2 T~ >= 0 has the eigenvalues nu_a nu_b (a < b), top nu1 nu2; I -> I' = I - alpha J leaves J ^ I unchanged.
#  (OB) Objects: J(p) = T~^p w, w = H^1/2 E~ 1 (free end); I(e,p) = R_e J(p) (horizontal e at junction p+1), T~_X J(p-1) (vertical e at
#   column p+1 >= 2), w_X (vertical at column 1), for p < P_e = PE[e] (9 for mh, 6 otherwise). The right end is the mirror image (the same
#   objects); n = p + k + q + 2.
#  (INF) For p >= P_e: J(p) = c_p (chi1 + J'(p)), |J'(p)| <= eta(P_e) (certified even modes decay like (nu_a/nu1)^p, the rest like
#   (u_+/nu1)^p |w_perp|), so J(p) ^ I'(e,p) = c_p^2 (chi1 ^ y_e + Delta) with |Delta| <= D_e uniform in p >= P_e (y_e: bulk insertion).
#  (NEAR) k < K_EX: exact values from family vectors (meet in the middle) and from the bulk seeds T~^k u1, T~^k y_e (infinity objects).
#  (FAR) k >= K_EX: S(k) = sum_{a<b certified} (nu_a nu_b)^k X_ab Y_ab + E, |E| <= (nu1 u_rem)^k |X^perp||Y^perp|, plus Delta terms
#   <= (nu1 nu2)^k (...). Divided by (nu1 nu2)^k, the absolute-value lower bound increases with k (every ratio < 1), so evaluation up to the
#   first k* where that bound is positive settles every k >= K_EX.
#  (R9) Family vectors carry exact float polynomial coefficients and a 2-norm remainder; an operator step adds its folded TM error and
#   multiplies the old remainder by its norm bound (|T^| = nu1 = |T^_X| bound (S_L X S_L^*), |R_e| <= max |g|).
#  (TR) Truncation (LEMMA_STRIP_R9_v1): spectral data widened by eps_T (Weyl in each reflection sector); Davis-Kahan in the T frame, so
#   the sine of a mode in the T~ frame carries sqrt(nu0/nu_a) (TR4); every inner product gets slack_f |a||b| with
#   slack_f = (eps_*/nu0)(2 p_max c kappa rho + (c kappa rho)^2)(1 + 1e-6), eps_* = max(eps_T, eps_e, eps_W), kappa = |v| sqrt(nu0)/|beta_0|,
#   rho = max over objects of (insertion factor x parent norm)/(lower norm), c = ((nu0+/nu0-)(1 + eps_T/nu0-))^p_max (TR1-TR5).
#  (IP) Coefficient inner products of the family vectors come from one chunked BLAS Gram product M M^T (any summation order):
#   |fl(<x, y>) - <x, y>| <= gam(n + 2) |x|_2 |y|_2 + (n + 2) ETA for n states (Cauchy-Schwarz on sum |x_i y_i|); norms cached per vector.
