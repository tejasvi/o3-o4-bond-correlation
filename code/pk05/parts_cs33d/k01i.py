#  (NORM) Positive scalars do not change any sign. If J_X, I_X are multiplied by c_J(t), c_I(t) > 0 (and the right-hand vectors by positive
#   scalars likewise), each NEAR value S and each Lambda^2 amplitude X_ab = j_a i_b - j_b i_a (so each FAR value f(k)) is multiplied by a
#   positive product (every term has exactly one J- and one I-factor), and the eigenvalue ratios are unchanged. The code multiplies every
#   propagation step (T~, and T~_X for a vertical insertion) by p(t), the degree-K Taylor polynomial of 1/mu_0(t) with exact float
#   coefficients, after certifying inf_{|t|<=h} p > 0 (C-POS). So J(p) = p^p T~^p w; I'(e,p) = (R_e - alpha) J(p) or p (T~_X - alpha T~) J(p-1)
#   (the centring sees one common factor); propagated objects carry one more p; Y_e = p (T~_X - alpha T~) u1 for vertical e (projected).
#   Bounds that use the step norm take sup p: near checks (sup p)^2 nu1 nu2; vertical Delta bounds F_e = sup p * nu1 * |u1|^2.
#  (PAR) The row reflection rho (Psi_{l1 l2 l3} -> Psi_{l3 l2 l1}; LEMMA_STRIP_RH_v1_1 R5 (iv)) permutes the product basis, commutes with
#   T^, with R_mh (g_{l2}) and with p(t), exchanges R_th <-> R_bh and T^_{X1} <-> T^_{X3}, and fixes w = H^1/2 E~ 1 (E~1 (x) E~1 and D are
#   swap-symmetric). Hence J(p), u1 (a mode vector made exactly even by fv_sector), T~ u1 and every mh object (I(mh, p), Y_mh and their
#   propagations) are exactly rho-even. Each certified mode chi_a is a simple eigenvector inside its reflection sector (sector-wise
#   identification, R5 (iv)-(v)), so rho chi_a = +-chi_a with the sign of u_a (exactly +-rho-symmetric; C-PAR checks the node parities to
#   1e-6). For odd chi_a and even v: <chi_a, v> = <rho chi_a, rho v> = -<chi_a, v> = 0. The code uses this exact 0 for the true objects in
#   place of the enclosure <u_a, v>/|u_a| +- sqrt2 s_a |v|.
