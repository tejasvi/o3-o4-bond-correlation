# NU_G_NOTE_v1: a certified nu_g for the delta bridge, in engine A's own identification (pk24)

Written 2026-11-21T16:56:45Z by pk24 for main (lead), the review and pk25: the rows 4635, 4639 and 4641, and the identification test as
main relayed it. Paths are relative to code/. Hand work, no run. Code is cited by content; sect. 7 gives the line numbers by tool.

## 1. Answer to the test
- My row-4635 route (geodesic normal coordinates at the middle spin) is not engine A's identification, so it would carry the extra term. It is
  withdrawn, together with its two corrections.
- Engine A's identification iota_t (pk02/kt_cert_v1_9.py, 86bcb6c7):
  - chart: the hemisphere chart sigma_v = (pi_v, s_v), s_v = (1 - |pi_v|^2)^1/2, rescaled phi_v = J^1/2 pi_v, with X_v = |phi_v|^2 and
    Q_uv = |phi_u - phi_v|^2 (PK10 sect. 12.2 and 13);
  - base point: the centre-of-mass gauge of the D graph's six vertices, n = sum_v sigma_v / |sum_v sigma_v|, so that sum_v phi_v = 0
    (BD = gauge_basis_a(6, range(6)); make_B0c's gauge_pinv on the two-column graph);
  - norm: nP's norm ||F||_t = (n1(t) E_G1(t)[F^2])^1/2, where G1, n1 = tilted_cov_a(LD, BD, [c_m t] * 6), with the Wishart on column 1. By
    F2(a) (pk02/SPEC_M1_CERT_v1_1_ADD2_v1.md sect. 6 (i)-(ii)), on the near region it dominates the Schur form of the J-space norm that
    R_e bounds.
- In this chart the test holds by construction. The base point and the rescaling are engine A's, and at each fixed chart point the states
  equal engine A's b(xi) vac (sect. 2). So no extra term enters.

## 2. The states in engine A's chart
- On the upper hemisphere, exactly: xi_p = J (1 - sigma_r . sigma_s) = Q_p/2 + t Delta_p, with
  - Delta_p = d_p w_p / 2,
  - d_p = (X_r - X_s)^2,
  - w_p = (s_r + s_s)^-2
  (PK10, "Exact chart identity"). Engine A's xi_pair = Q/2 - anh is the Taylor series of this identity, since w_coeffs expands
  w = (sqrt(1 - x) + sqrt(1 - y))^-2.
- Define B_g(t) := E0 pS_g(xi; t), with:
  - E0 = exp(-t sum_p TRI_p Delta_p);
  - pS_g = vac_poly for psi, i.e. 1 + sum_{k=1..3} t^k q_k . mu(xi);
  - pS_g = state_poly for e1, e2, e3 (linear in xi on z9sym) and for states 10 and 10' (quadratic).
- Engine A's basis series bas[g] = restrict6(E0 * pS[g]) is the Taylor series of B_g(t) to order 3, and l0_remainder bounds the rest by
  Dbar(E0 p_g). So engine A itself treats B_g(t) as the exact basis function in its chart.
- B_g(t) = phi_g / W_h, where:
  - phi_g = exp(-sum_p TRI_p xi_p) pS_g(xi; t) is a column function and does not depend on the frame;
  - W_h = exp(-sum_p TRI_p Q_p / 2) is the harmonic weight that B0 and G1 integrate against.
  The order-0 coefficient is b0_g = pS_g(Q/2; 0), and iota_t(p) = W_h p. Hence psi_g(t) - iota_t(b0_g) = iota_t(B_g(t) - b0_g), exactly,
  with no truncation and no series remainder.

## 3. The bridge, in the units of engine A's bound
- (C1) allows any coefficients. Take m*(t) = m(t) + delta at order 0, where delta = m0* - m0. By C-SPAN, r0 = sum_g delta_g b0_g as
  polynomials, so the residual's chart function becomes f* = f - sum_g delta_g B_g(t).
- Near region. f* = (P - r0) + Rem + sum_g delta_g (b0_g - B_g(t)), where Rem is what engine A bounds by nD, nR0 and the tails (with m).
  So nP is replaced by ||P - r0||_t + t sum_g |delta_g| nu_g, and ||P - r0||_t <= sum_{k=1..3} t^k M_k.
- Far region. Two facts give |f*| <= |src| + sum_g (|m_g(t)| + |delta_g|) |phi_g| there:
  - far_cert's sum is nondecreasing in each |m_g(t)|, since its X items bound integrals of |F|;
  - far_cert holds for any coefficients.
  So far_out is evaluated at |m_g(t)| + |delta_g|. I do not split it by Minkowski: the kernel restricted to the far region need not be
  positive semidefinite. gB does not read m.
- By Minkowski in R^2:
    |Q_W(t) S e_k| <= [((near with nP -> ||P - r0||_t)^2 + far_out(|m(t)| + |delta|))^1/2 + gB] + t sum_g |delta_g| nu_g.
  - This is P2 v2_1's placement: outside the square root, in
    engine A's units.
  - The one change for P2: its far term takes |m_g(t)| + |delta_g|.

## 4. nu_g in closed form
- Near region. There t X_v <= a_m at every vertex (the radius of c_m). I use a = max(a_m, a_e) >= a_m, which only enlarges the bounds. So:
  - s_v >= (1 - a)^1/2;
  - w_p <= wbar = 1/(4 (1 - a));
  - 0 <= Delta_p <= Dbar_p := wbar d_p / 2;
  - for 0 < t <= t1, Q_p/2 <= xi_p <= xibar_p := Q_p/2 + t1 Dbar_p.
- The E0 factor: |E0 - 1| <= t ebar, with ebar := sum_p TRI_p Dbar_p. Also |pS_g(xi; t)| <= Pbar_g := sum_k t1^k sum_mu |c_g,k,mu| mu(xibar).
- The polynomial part:
  - pS_g(xi; t) - pS_g(Q/2; 0) = sum_mu c_g,0,mu (mu(xi) - mu(Q/2)) + sum_{k>=1} t^k sum_mu c_g,k,mu mu(xi);
  - 0 <= xi_p - Q_p/2 <= t Dbar_p, and 0 <= xi_p xi_q - Q_p Q_q / 4 <= t (Dbar_p xibar_q + Dbar_q Q_p / 2);
  - so its modulus is at most t Dbar'_g: the same sums with |c| and these bounds.
- The majorant M_g := ebar Pbar_g + Dbar'_g:
  - M_g >= |B_g(t) - b0_g| / t on the near region, for all 0 < t <= t1;
  - it is a polynomial of degree <= 6 in column 1's six sigma variables, and M_g >= 0.
- Uniform in t: n1(t) E_G1(t)[F] = E_G1(0)[F e^(c_m t sum_v X_v)] is nondecreasing in t for F >= 0. So nu_g := (n1(t1) E_G1(t1)[M_g^2])^1/2
  bounds ||(B_g(t) - b0_g) 1_near||_t / t for all t <= t1. The choice t1 = 1/300 covers every piece.

## 5. Coverage
- psi, e1, e2 and e3 at N = 3 and 4. These make up the basis of every kt_cert kind: GK gives (psi, e1, e3), plus e2 for t, and (e2) alone for
  am. So P2 and P4 read one record.
- Item (3)'s xy kind: states 10 (z9symxy) and 10' (z9symxyp), by the same formula. This holds if item (3)'s engine keeps engine A's D graph,
  gauge, near region and tilt; a C-CORE pin on lap_a, gauge_basis_a, tilted_cov_a and ED_ checks this. Its far term follows sect. 3 with its
  own far items.

## 6. Tool and record (after the check)
- pk24/nu/kt_nu_g_v1.py runs in arb (512 bits) on an unchanged copy of arbeng_c2b_v2.py:
  - per N, G1 and n1 at t1, from verbatim copies of engine A's functions;
  - M_g from the pinned trial files;
  - nu_g = (n1 E2(M_g, M_g))^1/2.
- Gates:
  - C-HASH.
  - C-CORE: the copied source text equals kt_cert_v1_9's.
  - C-ID: engine A's bas[g], orders 0-3, built from verbatim copies of xi_pair, anh, vac_poly and state_poly, is compared with B_g(t) in
    closed form at seeded chart points; the difference must be O(t^4). PLANT-ID: B_g without E0 must fail.
  - C-MAJ: M_g >= |B_g(t) - b0_g| / t at seeded near-region points, for t in {t1, t1/10, 1e-6}. PLANT-MAJ: M_g / 100 must fail.
  - C-MONO: n1 E[M_g^2] is nondecreasing over t1/4, t1/2, t1.
- Record pk24/nu/NU_G_RECORD_v1.kv, with a manifest:
  - one line per (N, g) with nu_g's upper end, 17 digits rounded outward;
  - t1, a, wbar, c_m and the input sha256.
  pk25's NU reader pins it.
- Price [E]: 1.5-2.5 hand-h, below 0.01 core-h. pk22's export stays paused as the fallback.

## 7. Tool lines
pk02/kt_cert_v1_9.py (sha8 86bcb6c7):
  l.479 A_ = (3 + SQ21) / 6
  l.480 B_ = (3 * SQ5 - SQ21) / 12
  l.481 TRI = [A_, A_, B_]
  l.482 PAIRS = [(0, 1), (1, 2), (0, 2)]
  l.489 RHO_M, RHO_E = 0.55, 0.6                    # free radii (exact binary64)
  l.602 def xi_pair(iu, iv, iq):
  l.603     return ser([pvar(iq, NVX, arb(1) / 2)] + [{} for _ in range(KX)]) - anh(iu, iv, 1)
  l.590 def anh(iu, iv, c):
  l.621 def vac_poly(xs):
  l.632 def state_poly(xs, b):
  l.851     H0 = zero()
  l.853         H0 = H0 + anh(XS[r], XS[s], TRI[p])
  l.854     EL, E0 = HL.exp(), H0.exp()
  l.858     pS = {'psi': vac_poly(xiS), 'e1': state_poly(xiS, 1), 'e3': state_poly(xiS, 3)}
  l.861     bas = {g: restrict6(E0 * pS[g]) for g in pS}
  l.799     m = solve_mid([[B0(basis[i], basis[j]) for j in range(nb)] for i in range(nb)], [B0(basis[i], f) for i in range(nb)])
  l.766     """B0(f, h) = E_D[f(sigma) h(sigma')] for deg f <= c0 (first column) and deg h <= c1 (second column), in balls."""
  l.966 a_m, a_e = RHO_M ** 2, RHO_E ** 2
  l.967 c_m, c_e = (up_float(-(1 - arb(x)).log() / (2 * arb(x))) for x in (a_m, a_e))
  l.1427 ED_ = [((r, s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), TRI[p_]) for p_, (r, s) in enumerate(PAIRS)] + \
  l.1429 LD = lap_a(ED_, 6)
  l.1430 BD = gauge_basis_a(6, range(6))
  l.2117     G1, n1 = tilted_cov_a(LD, BD, [c_m * t] * 6)
  l.2154     G1, n1 = tilted_cov_a(LD, BD, [c_m * t] * 6)
  l.2124     nP = nsqrt(n1 * w1.E2(Pg, Pg))
  l.2168     nP = nsqrt(n1 * w1.E2(Pg, Pg))
  l.1564     """L0 side: sum_g sum_{j<=3} |m_gj| t^j t^{4-j}/(4-j)! Dbar_{4-j}(E0 p_g) (sigma variables), and the h0 majorants."""
  l.1959     """F3: P = r0 + t r1 + t^2 r2 + t^3 r3 for every kind (the free binary64 m0 leave r0 != 0, and (C1) needs the residual of the
  l.1637     mg = [abs(sum((arb(m[j][gi]) * t ** j for j in range(4)), arb(0))) for gi in range(len(G))]
  l.1552     """sup |F| of the item's source in balls (an upper bound by the triangle inequality on [0, 2J]^3)."""
  l.836 GK = {'t': ('psi', 'e1', 'e3', 'e2'), 'am': ('e2',)}                    # kt_cert_v1_7: P_4 for t, {e2} for am; (psi, e1, e3) otherwise

pk02/arbeng_c2b_v2.py (sha8 fb8cd1b5):
  l.207     """pseries.w_coeffs in exact rationals, returned as balls: w(x, y) = (sqrt(1 - x) + sqrt(1 - y))^-2 = sum w[i][j] x^i y^j, i + j <= K."""
  l.233     """condg.sigma_to_g with ball coefficients: X_r = g_rr, Q_rs = g_rr + g_ss - 2 g_rs (order (0,0),(0,1),(0,2),(1,1),(1,2),(2,2))."""
  l.604     """wishart.Wishart in balls: moments of the Gram matrix of n i.i.d. N(0, G) vectors; G an arb_mat m x m."""

pk02/SPEC_M1_CERT_v1_1_ADD2_v1.md (sha8 ddd85cfd):
  l.98 B = (near^2 + far_out)^{1/2} + gB bounds ||K^{1/2}|f| ||/(lambda_h main_D^{1/2}), not only ||K^{1/2} f||.
  l.103 - **(i) Weighted one-column norms are Schur bounds.**
  l.106   - Take h = W P and w = W. The right side is int W P^2 (K W) = <W P^2, K W>: the D-graph integral with P^2 on one column and 1 on the other.
  l.107   - Engine A evaluates exactly that quantity as n E_G[P^2], with G the tilted D-graph covariance restricted to one column (tilted_cov(LD,
  l.109   - The tilts (rates c_m t, c_e t) are upper bounds on the density of the spin measure relative to the Gaussian one, so they only enlarge
  l.114 - **(ii) Pointwise majorants.** On the near region, the Taylor remainders of L1 F and of the L0 side are bounded in absolute value by the
  l.116 - **(iii) Far and bad parts.** far_out (riglap3 majorants on the outer far region, and the truly far sup|F| times tree bounds) and gB (sup|F|
  l.124 - **(v) The m_g.** Any real m_g are allowed (C1). The |f| form uses the same m_bg as the (C9) assembly, so W2 reads them from the e1 and e3

pk10/PK10_NOTES.md (sha8 c4d89203):
  l.403 ### 12.2 The expansion (rooted hemisphere chart; G2WOLFF §6 extended to second order and to general small graphs)
  l.458 - **Centre-of-mass gauge [derived; checked].** Write σ_v = (π_v, s_v) in the frame of n = Σσ_v/|Σσ_v|, with the constraint Σπ_v = 0. The exact coarea identity is
  l.481 - **Exact chart identity on the upper hemisphere:** J Σ_e c_e(σ_u·σ_v − 1) = −(J/2)πᵀ(L⊗I)π − (J/2)Σ_e c_e(x_u − x_v)²·w(x_u, x_v), with x = |π|², w = (s_u + s_v)⁻² and s = √(1−x).

Source 1 (sha8 fba486b2):
  l.24 - Hence r0 = s0 - sum_g m0_g b0_g = sum_g (m0*_g - m0_g) b0_g lies in W(0), where m0* are the exact order-0 projection coefficients. It is
  l.31 - Since r0 lies in W(0), |Q_W(t) r0| = dist(r0, W(t)) <= sum_g |delta_g| |psi_g(t) - psi_g(0)| with delta = m0* - m0, which is O(t).

Source 2 (sha8 1b04a668):
  l.16   - (b) Add t sum_g |delta_g| nu_g to Rb[e_k]/t on the last piece. Here delta = m0* - m0, from C10's exact data against kt_cert's printed m0,

Source 3 (sha8 6abd3d0d):
  l.14 - With r0 = sum_g delta_g psi_g(0), |Q_W(t) r0| = |Q_W(t) sum_g delta_g (psi_g(0) - psi_g(t))| <= t sum_g |delta_g| nu_g.
  l.15 - The term sits outside the square root and inside the division by D, in the units of engine A's bound. This is my option (b)
  l.48 - N-2: the certified NU input (tool l.81 and l.554) must bound |psi_g(t) - psi_g(0)|/t on the whole last piece, in the norm engine A's

pk25/p2/kt_p2_v2_1.py (sha8 9e259a03):
  l.28     R_e/t <= [((300 (M1 + s M2 + s^2 M3) + 300^4 t^3 (ND + NR0) + J (tailX + tailB + ann))^2 + J^2 far)^1/2 + J gB + sum_g |delta_g| nu_g] / D,

## 8. Files (sha256, bytes, path)
86bcb6c7b3a3e9eaf2d051c2ee2266c70da81884ee8203fc78408eb80f44a25d  185747  pk02/kt_cert_v1_9.py
fb8cd1b5162930b1e9ff83c35fb652575a9f2ff1649f733c5d45bdf7f7762993  32223  pk02/arbeng_c2b_v2.py
77e488542958ddbe80499d946c75cee83782344c5a874d6a98c9558c8b9f81f4  14715  pk02/SPEC_M1_CERT_v1_1_ADD2_v1.md
dbb7ed0c958cfb5ad440606f2197a246a65240d06f167848da01a628bb1c3c9f  195003  pk10/PK10_NOTES.md
fba486b27f7f6638f7d3976355bb17b79dd3cd46e7b8809a153880528cf8e832  3184  rv02/REVIEW_KTCERT_RE_DEFINITION_rv02.md
1b04a66882a58cf7c2591385eb6b1d23ffe07d8ade13ba9e2a965a55b1dbabd2  2579  rv02/REVIEW_KTCERT_RE_DEFINITION_ADD1_rv02.md
6abd3d0d6933d1607d90516e633c6ab33085e2dc21fe8fe9c400289b504d1871  3842  rv02/REVIEW_P2_V2_1_rv02.md
9e259a033ab98f76c493beaba64487ccfd40fcd7a15455ede229d82680474866  45571  pk25/p2/kt_p2_v2_1.py
62cdc8f532a1bbe3d6ad62f95755f61882b0673dd4e014cd4b2c6c5e178391cb  105  rv02/MANIFEST_REVIEW_KTCERT_RE_DEFINITION_rv02.sha256
7107f173655f3ad809b4ae891ffdfdf998b25306c19dff857ef9362b3e8f9efa  110  rv02/MANIFEST_REVIEW_KTCERT_RE_DEFINITION_ADD1_rv02.sha256
06851e1c3bc9c74f31b0bd3f9f493c4f4953d2c803178097b3e8e59f3e515193  92  rv02/MANIFEST_REVIEW_P2_V2_1_rv02.sha256
ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d  5487  pk11/out/ts_N4_J170_D_S_z9sym_v1.json
a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6  5562  pk11/out/ts_N3_S_z9sym_v1.json
b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e  44752  pk11/out/vacres_K3_N4_sym_v1.json
e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0  44673  pk11/out/vacres_K3_N3_sym_v1.json
909b20bfa30a4b95c2a78194e032508cde161da4f66de147fc40167b6c4ee560  6006  pk22/midrow/psixy/ts_N4_J170_D_S_z9symxy_v1.json
d6b2ab93d086831e2423eed52ece6bc11abc0eeb92c31f8b8fa9368afd5f5a91  6076  pk22/midrow/psixy/ts_N3_S_z9symxy_v1.json
4f0199bc6f3b03d906c4f268d51e4aee29432cf32e6bb9a9f91cd072b983acd0  6111  pk22/midrow/psixy/ts_N4_J170_D_S_z9symxyp_v1.json
0a6109691c8626c06073e5c3e7be66026e0c3cafbb4377b1f152ced58624ecc7  6181  pk22/midrow/psixy/ts_N3_S_z9symxyp_v1.json
6ed3623cc97d872a05e486cab9fb9d9b12ba5e301c1e3a857d3970e444f6fbb4  32563  pk02/FAR_CRUDE_v1_N4.json
596c4664a6465e3aa186a1810ee0625378bbc90616245512d2f78d1e81550bc9  32584  pk02/FAR_CRUDE_v1_N3.json
a9c3492033020eed7f64ee1e9cc68446d04b2d563907dcb73a0ebd2e914a9613  7056  pk24/notes_src/NU_G_NOTE_body_v1.md
ca6a243a202583ae6270f396d6b2483e1222894a43025d565aa60705de470078  5880  pk24/tools/assemble_nunote_v1.py
399c45e2e2258c691d815935a96e64f40408467d783190afdb821497635d4848  1675  pk24/jobs/job239_nunote_v1.sh
