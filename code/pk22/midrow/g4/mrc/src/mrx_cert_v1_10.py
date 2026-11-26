#!/usr/bin/env python3
"""mrx_cert_v1_10.py (pk22; item (4), the P0_LOG rows 4558 and 4738): mrx_cert_v1_9.py (sha256 3725a2d01666e195a08d50e19c25700ef2cb0be538f6d132cef1b47e6eb2874b) with Way A for h-1 and h0
on the last piece, variant C (made by make_mrx_v1_10_r2.py; diff_mrx_cert_v1_9_to_v1_10.txt). v1_9 wrote the last piece of h-1 and h0 by Way B
(Axc 0 0 and a J-free floor Axf); G6's M2 needs Way A there (v1_6_9 sect. 0f item 3, sect. 6: Axf_hi = 0 and Axc enclosing A_x/t at every J of the
piece, t -> 0 included). On the pattern of pk25's P4 (kt_s9h_ins_v2_7, waya_last):
- The x amplitude of each exact end is A_x = F / (P0 s_x) with F = <u_x, w1 - r* w2>, r* = <u, w1>/<u, w2> and P0 = <u, w2>: h-1 with w1, w2 the
  CE3H fH,b and E3 f,b vectors (amps' r and P0 enclose r* and P0 on the piece); h0 with the H4TH hH,b and h0,b vectors (r* in r0 +- Dr, P0 in
  [P0_lo, P0_hi], h0_end's balls).
- F(0) = 0: at t^0 the end vector w1 - r* w2 has no x amplitude (X_POWER 'h-1 1, h0 1'; the order-0 states and the free end factor over the mode
  coordinates, C13's C-GAMMA, and M_c u_x^(0) = h_y^(0) u_xy^(0), C13's C-BH0, with u_x^(0) orthogonal to u^(0) and u_xy^(0), P1's C-SPAN). Lemma A's
  errors vanish at t^0, so F(0) = X1(0) - r*(0) X2(0) with X_i = A~_x(w_i) = sum_b c_xb v_b and r*(0) = N0/D0, N0 = A~_0(w1)(0), D0 = A~_0(w2)(0);
  C-WAYA-T0 checks that the coefficient balls hold T0 = X1(0) D0 - N0 X2(0) = 0. The separate X_i(0) are not 0 (try 1 of this file showed it).
- Hence F/t = X1d - r* X2d - rd X2(0) +- (dx(w1) + |r*| dx(w2))/t, X_id = (X_i(t) - X_i(0))/t, rd = (r*(t) - r*(0))/t = (Nd D0 - N0 Dd)/(P0 D0)
  with Nd and Dd the level-0 differences over t, each +- Lemma A's level-0 error over t; and A_x/t = (F/t)/(P0 s_x).
- Each difference over t at level k: (sum_b c_kb v_b(t) - sum_b c0_kb v_b(0))/t = sum_b dc_kb v_b(t) + sum_b c0_kb (v_b(t) - v_b(0))/t, with
  c_kb = uhat_kb / G_bb^1/2, c0_kb = uhat_kb(0) / G0_bb^1/2 exact (C10's UHAT0 and GT0_W; uhat_0(0) = (1, 0, 0)), dc_kb = du_kb/g_b - u0_kb G1_bb /
  (g_b g0_b (g_b + g0_b)), du_kb P2's (uhat_kb - uhat_kb(0))/t, g_b = G_bb^1/2 on the piece, g0_b = G0_bb^1/2, G1_bb and (v_b(t) - v_b(0))/t from
  the reader's coefficient balls, sum_(k=1..3) [LO_k, HI_k] t^(k-1) + [-R/t, R/t], R the law's four parts without the ak_rad term (entry_law's
  N-1), R/t <= rem 300^4 t_hi^3 + J_lo (tail + ann + far)(J_lo) (C-MONO-TAIL, C-MONO-FAR); C-A0: C10's exact G0_bb lies in G_bb's t^0 ball.
- Lemma A's error at level a over t, from P2's /t fields: qat |Q_W w| + sum_(k != a) eps_kat |A~_k(w)| + (q_a qat + sum_(k != a) eps_ka eps_kat)
  |A~_a(w)|, with |Q_W w_i| for h-1 amps' qw1, qw2 (the norm entries) and for h0 |Q_W w2| <= P0_hi qq, |Q_W w1| <= P0_hi (X + (|r0| + Dr) qq)
  (w1 = P0 (w + r l_3), |Q_W l_3| <= qq, h0_end's fixed point X >= |Q_W w|).
- The written row: Axc = A_x/t rounded outward, Axf 0, and the Ax columns the hull of v1_9's direct Ax ball, 0 and t_1 Axc (t_1 = 1/jlo), so
  G-FACTX holds by construction and C-ROUND still covers the direct ball. Variant U keeps Way B (no J-law there); mrx_combine writes variant C.
New inputs (C-WAYA-IN): P2's MR_LEMMAP_V3F (CERTIFIED; SOURCE naming this run's MR_LEMMAP v3 and C10), P1's C10 record and C13's record, each a
row of its pk25 manifest. New gates: C-WAYA-IN, C-WAYA-RUN (no refusal: C-A0, C-MONO-TAIL, C-MONO-FAR), C-WAYA-T0 (both ends' T0 hold 0),
C-WAYA-CONT (a control of the formula: on the piece before the last, Way A's A_x/t overlaps v1_9's direct Ax/T), C-WAYA-JOIN (the continuity
control: the last piece's Way A Axc overlaps the direct Ax/T of the piece before it), C-WAYA (the last piece's h-1 and h0 rows carry Axf 0 and a
finite Axc); plants PLANT-WAYA-ZERO (u_y(0) in place of u_x(0): h-1's T0 must leave 0) and PLANT-WAYA-PIN (a wrong P2 pin must
be refused). Parts MR_EXACT_PART_v1_10_<V>_N<N>.kv. Usage: mrx_cert_v1_10.py cert N
---- mrx_cert_v1_9.py's docstring:
mrx_cert_v1_9.py (pk22): mrx_cert_v1_8.py with H4TH's certified J-laws (the P0_LOG row 4485). v1_8's h0 rows took the uniform claims
of c3h's H4TH entries, which have no law certificate in m3_lawcert_c3h_v1, so h0's x sign held only to J 484 (N4) and 854 (N3). Now variant C
reads the c3h certificates of m3_lawcert_c3h_v1_1 (2178e7ff, 5f085edb; frozen in MANIFEST_C3H_LAWCERT_v1_1 bce72571), which certify CE3H, CS4H
and H4TH, through the reader fork m3_reader_c3h_v1_1 (73ca0690; frozen in MANIFEST_m3_reader_c3h_v1_1 5202b515): CERTDEF's c3h row names that
producer with the three families, cert_law gives H4TH's entries their certified laws, and C-CERT-SAME now covers them too. Nothing else changes.
Usage: mrx_cert_v1_9.py cert N
---- mrx_cert_v1_8.py's docstring:
mrx_cert_v1_8.py (pk22): the certified v4 MR_EXACT writer (the P0_LOG rows 4430, 4446, 4453): mrx_cert_v1_7.py with the h0 rows
and pk25's certified mr/v4 records (MR_SPECTRAL 0e4d8177, rows equal to mr/v3's; MR_INSERT 21e88843; MANIFEST_MR_V4_CERT_v1 6ac308d7), with
MR_LEMMAP kept at mr/v3 (3164b778). Mode 'cert' only: every input is certified, and the parts go to out/cert for mrx_combine_v1_8.
- h0, the h end at d = 0 (G6 v1_6_2 sect. 4.1 with sect. 0d item 2; no d = 0 norm entry): w1 = S M_h l_2 and w2 = S l_2 = S^2 w-hat are
  c3h's H4TH entries hH,b and h0,b (N4 4119b0e1, N3 9c7cdb4a), in one graph's units. With P0 = <u, w2>, l_3 = w2/P0 = u + eps(1) and
  r = <u, w1>/P0, the windowed end vector w = S a(0) = (w1 - r w2)/P0 is flip-even and orthogonal to u.
  - P0 by Lemma A at level 0 on w2 with |Q_W w2| <= P0 qq, qq = q_0 + R_w rho_1^2 (|Q_W u| <= q_0 by L3 at level 0, |eps(1)| <= R_w rho_1^2):
    |P0 - A~_0(w2)| <= E_2 + q_0 qq P0, so P0 lies in [(A~_0,lo - E_2)/(1 + q_0 qq), (A~_0,hi + E_2)/(1 - q_0 qq)], E_2 Lemma A's eps terms.
  - r: r0 = mid(A~_0(w1)/A~_0(w2)) (an exact point), z = w1 - r0 w2 entry by entry, D >= |r - r0| = |<u, z>|/P0. Lemma A at level 0 on z,
    with |Q_W z| <= P0 X + D P0 qq (z = P0 w + (r - r0) P0 l_3), gives D <= (|A~_0(z)| + E_z)/P0_lo + q_0 X + q_0 qq D.
  - A~_k(w) = (A~_k(z) - (r - r0) A~_k(w2))/P0, so |A~_k(w)| <= al_k + be_k D with al_k = |A~_k(z)|/P0_lo and be_k = |A~_k(w2)|/P0_lo.
  - X >= |Q_W w| by the fixed point: |Q_W w| <= |P_e w| + sum_(k = x, y) |<u_k, w>| q_k (the k = 0 term drops: <u, w> = 0), |P_e w| <= r_W,
    and Lemma A's |<u_k, w>| <= |A~_k(w)| + q_k X + c_k, so X <= (r_W + sum_k q_k (|A~_k(w)| + c_k)) / (1 - q_x^2 - q_y^2). Both bounds are
    linear in (X, D): X <= A + B D and D <= C + q_0 X + q_0 qq D, solved exactly in Fractions, D = (C + q_0 A) / (1 - q_0 qq - q_0 B) and
    X = A + B D (C-H0-FP: every denominator positive, P0_lo > 0, both inequalities re-checked on the solution).
  - r_W = |P_e S v_h| + |c_x(-1)| |P_e B^w u_x| + |c_y(-1)| |P_e B^w u_y| + |P_e B^w P_e| |P_e eps(-1)| + |v+| |eps(0)| tau |P_e eps(0)| from
    MR_INSERT's h row (Pevw_hi, PeBwux_hi, PeBwuy_hi, win_hi, vp_hi) and MR_SPECTRAL (cxm1, cym1, Rw_hi, rho1_hi, tau_hi), with |P_e eps(-1)| <=
    (R_w^2 - c_x,mig^2 - c_y,mig^2)^1/2, |eps(0)| <= R_w rho_1 and |P_e eps(0)| <= tau |P_e eps(-1)|: the engine's crude windowed N' at d = 0,
    with |c_a(-1)| in place of |c_a(0)| / s_a. win_hi bounds B^w between vectors in P_e's range only, which is how it enters here.
  - The row: A^a = <u_a, w> in A~_a(w) +- (q_a X + c_a), Ay, Ax = A^a / s_a; Np_hi = r_W (G6: N' = r_W; Lemma P from X is larger); Axc and
    Way B as for h-1 (power 1). Pe_hi by G6 sect. 4.3's m = 1 form at d = 0 from MR_INSERT, min(Pev + |c_x(-1)| C s_x^1/2 + |c_y(-1)| C s_y^1/2
    + C tau^1/2 |P_e eps(-1)| + |v+| |eps(0)| |P_e eps(0)|, Pev + C s_x^1/2 R_w + |v+| |eps(0)| |P_e eps(0)|): with Pev_hi = C it is a valid
    filler that keeps FIELDS uniform (the row 4438 built no h0 Pe_hi entry); the engine's m = 1 rest takes the least form.
  - The H4TH entries have no law certificate, so variant C takes their uniform claims.
New gates: C-INSERT (MR_INSERT's header, FIELDS, LEMMAP_SHA256 and TRIAL_SET; keys, jlo and jhi equal to MR_SPECTRAL's; h and t windowed),
C-SPECTRAL's rows-equal check against mr/v3, C-H0-FP with PLANT-H0-FP (X = r_W alone must fail the fixed-point re-check), C-RW-FLOAT (r_W in
floats from the same decimals) with PLANT-RW (win_hi doubled), and C-BULKSIGN (engine v1_8_4's C-ORIENT anchor on every written row: the exact
end's x coefficient sign against its bulk x sign in MR_INSERT where both are strict). C-FLOAT now covers h0 (mrx_err_v1_2's float a_x, a_y).
C-FACTX, C-ROUND and x_cols treat h0 as h-1 (power 1). Usage: mrx_cert_v1_8.py cert N
---- mrx_cert_v1_7.py's docstring:
mrx_cert_v1_7.py (pk22): mrx_cert_v1_6.py with G6 v1_6_2's optional Pe_hi (sect. 6; engine v1_8_4's route (v); the P0_LOG row
4438, pk24's answer): Pe_hi >= |P_e a| of each exact end, written after Axf_hi on every row.
- h-1 and t-1: the trivial bound |P_e a_even| <= |a| (for t-1 |a_even| <= |a_t| by T <-> B), with a = (M - r) x_w / <u_0, x_w> for the free
  end x_w = K^1/2 1, M = M_h (h-1) or M_t (t-1), r the end's ball as the amplitudes use it, and <u_0, x_w> = <u_0, S x_w> = P0 since S u_0 = u_0.
  The numerator |(M - r) x_w|^2 = W2 - 2 r W1 + r^2 Z0 from runner c3n_1's record (FFH: Z0, WH1, WH2, WT1, WT2 on [free, free]), centred in
  r (R(r0) + 2 rr |W1 - r0 Z0| + rr^2 Z0). The denominator by Lemma A at level 0 on x_w: A~_k(x_w) = sum_b uhat_kb e_b / |psi_b| from S8's
  E2 overlaps e,b = <psi_b, x_w>, delta_0 = q_0 |Q_W x_w| + sum_(k != 0) eps_k0 |A~_k| + (q_0^2 + sum eps_k0^2) |A~_0|, |Q_W x_w|^2 =
  Z0 - rho_E2 e' G^-1 e, all in FF units: <u_0, x_w> / main_FF^1/2 = rho_E2^1/2 A~_0 +- delta_0 with rho_E2 = main_E2^2 / (main_D main_FF) =
  (tau_D tau_FF / tau_E2^2)^((N-1)/2) (matrix-tree theorem in arb; the vertex counts balance, so no lambda_0 enters); Pe_hi = R_hi^1/2 /
  (rho_E2^1/2 lo A~_0 - delta_0), rounded up.
- a0: Lemma P on a itself, Pe_hi = Np_hi / tau4 (a0's record vector is a, so Np_hi = tau4 times Lemma P).
- Variant C takes S8's certified laws for E2 and FF as for E3 (m3_lawcert_v1_1); the FFH record has no law certificate (uniform claim).
New gates: C-RHO-E2 (arb against the float eigenvalue form) with PLANT-RHO-E2; C-Z0 (FFH's Z0 a_k against S8's FF z, relative 1e-12) with
PLANT-Z0; C-PE (every Pe_hi finite: the Lemma A denominator positive on every piece); C-PE-FLOAT (at the J_low piece the h-1 Pe_hi lies in
[1, 3] times a float |a| from midpoints) with PLANT-PE-FLOAT (4 times the float must fail); C-ROUND also checks Pe_hi. Parts
MR_EXACT_PART_v1_7_<V>_N<N>.kv; mrx_combine_v1_7.py joins them. Usage: mrx_cert_v1_7.py dry N
---- mrx_cert_v1_6.py's docstring:
mrx_cert_v1_6.py (pk22): mrx_cert_v1_5.py with G6 v1_6_2's final MR_EXACT x columns (pk24/MIDROW_G6_SPEC_v1_6_2.md 1e570ab7
sect. 6; engine v1_8_4 abd48b2c). FIELDS gain Axf_hi. h-1 off the last piece writes Axc = Ax/T rounded outward and its Ax columns as the hull
of t Axc at the piece's ends (t = 1/jlo, 1/jhi), so the engine's G-FACTX holds by construction and X_DEFINITION's floor is 0. h-1 on the last
piece takes Way B (the row 4325): Axc 0 0 and the floor Axf = max(|lo Ax|, |hi Ax|) rounded up, Ax written [-Axf, Axf]. t-1 and a0
(power 0) write Axc = Ax and Axf 0. New gate C-FACTX (the engine's G-FACTX and G-FLOOR on every written row, exactly, no slack) with
PLANT-FACTX (an h-1 row's Axc_hi doubled); C-ROUND also checks Axc against the Ax/T ball. The records are PARTS, one per N and variant
(MR_EXACT_PART_v1_6_<V>_N<N>.kv); mrx_combine_v1_6.py joins the two N into the one MR_EXACT record the engine reads, with ORIENT_CHECK and
X_DEFINITION copied by tool from the spec. Pe_hi (optional) is not written. Usage: mrx_cert_v1_6.py dry N
---- mrx_cert_v1_5.py's docstring:
mrx_cert_v1_5.py (pk22): mrx_cert_v1_4.py with variant C in place of variant L (main rows 4354, 4376: the MR_EXACT certified path's
pieces that do not wait on G6 v1_6_2). Variant C takes, for each entry, min(uniform claim, its CERTIFIED J-law at the piece's jlo) where a
law certificate covers the entry, and the uniform claim elsewhere. The certified laws are read through pk22's reader fork
m3_reader_c3h_v1 (d7e39d07; frozen in midrow/g4/MANIFEST_m3_reader_c3h_v1.sha256): each certificate's records through load bound to their asm
output, the certificate through load_lawcert bound to its job's output (producer pin), the law through entry_law (exact rationals), and
LAWCERT_CLAIM's right side evaluated in arb with outward rounding at jlo (every term non-increasing in J). Certificates: m3_lawcert_c3h_v1
(CE3H, CS4H; pk22, MANIFEST_C3H_LAWCERT_v1) and pk03's m3_lawcert_v1_1 (S8's D, E2, E3, FF v1_8_1); S9's G entries are byte-identical
aliases of the S8 D items, so they take D's certified laws when the alias names the D record that certificate binds (file and sha256). So h-1
(fH,b; f,b; xxH, xH, Z; G) is certified throughout; t-1 and a0 take certified laws for their E3 and G entries and the uniform claim for the c3,
c3j and c3l entries (no certificate). New gates: C-LAWCERT (both certificates load, producers as pinned), C-CERT-SAME (for every entry with a
certified law, the record item the balls use has exactly the certified entry's ak and err), with PLANT-LAWCERT (the c3h certificate offered
with the S8 job's output must be refused) and PLANT-CERT-SAME (an entry offered another entry's law must fail C-CERT-SAME). Records:
MR_EXACT_DRY_v1_5_<V>_N<N>.kv for V in U and C. Usage: mrx_cert_v1_5.py dry N
---- mrx_cert_v1_4.py's docstring:
mrx_cert_v1_4.py (pk22): mrx_cert_v1_3.py pinned to pk25's certified mr/v3 side tables (main rows 4363, 4376 item 3): MR_LEMMAP.kv and
MR_SPECTRAL.kv through pk25/mr/MANIFEST_C6A_CERT_v3.sha256 (each field the per-piece intersection of v2's record computation and the
law-certificate computation, so u~_x's e3 coefficient no longer has v2's J-independent floor). Nothing else changes. Records:
MR_EXACT_DRY_v1_4_<V>_N<N>.kv. Usage: mrx_cert_v1_4.py dry N
---- mrx_cert_v1_3.py's docstring:
mrx_cert_v1_3.py (pk22): mrx_cert_v1_2.py with the centred vector's residual in centred form. v1_1 and v1_2 evaluated
R(r) = |Q_W (w1 - r w2)|^2 = rho4 (N11 - 2 r N12 + r^2 N22) - (v1 - r v2)' G^-1 (v1 - r v2) with r a ball in each occurrence, so r's width
entered through -2 r N12 and r^2 N22 separately. Now, with r0 = mid(r) (an exact point), rr = rad(r) and r = r0 + D:
R(r) = R(r0) - 2 D [rho4 (N12 - r0 N22) - v2' G^-1 (v1 - r0 v2)] + D^2 (rho4 N22 - v2' G^-1 v2), bounded by R(r0) + 2 rr |slope| + rr^2 |c2|.
Records: MR_EXACT_DRY_v1_3_<V>_N<N>.kv. Usage: mrx_cert_v1_3.py dry N
---- mrx_cert_v1_2.py's docstring:
mrx_cert_v1_2.py (pk22): mrx_cert_v1_1.py with diagnostics only: the PARTS of h-1's Ax at the first piece where its sign is open
(per variant), with the parts of delta_x and the error each entry takes there (uniform or law), and per-row values unchanged. Records:
MR_EXACT_DRY_v1_2_<V>_N<N>.kv. Usage: mrx_cert_v1_2.py dry N
---- mrx_cert_v1_1.py's docstring:
mrx_cert_v1_1.py (pk22): mrx_cert_v1.py (b3a0a892) with Lemma A applied once, to the centred vector w = w1 - r w2, in place of v1's
two applications (to w1 and to w2) whose errors added without the cancellation in w1 - r w2. Now: r = <u_0, w1>/<u_0, w2> with u~_0's
psi-hat coefficient divided out of both (B_i = a_i,p + (uhat_01/uhat_0p) a_i,1 + (uhat_03/uhat_0p) a_i,3, level-0 Lemma A errors over
uhat_0p,lo); the centred overlaps v1_b - r v2_b; |Q_W w|^2 = rho4 (N11 - 2 r N12 + r^2 N22) - (v1 - r v2)' G^-1 (v1 - r v2) in one form;
<u_a, w> in A~_a(w) +- delta_a(w); A^a = <u_a, w>/P0. Records: MR_EXACT_DRY_v1_1_<V>_N<N>.kv. Usage: mrx_cert_v1_1.py dry N
---- mrx_cert_v1.py's docstring:
mrx_cert_v1.py (pk22, G4: the exact ends of MR_EXACT in MR_INPUT_KV_v4; main rows 4307, 4312, 4321, 4329, 4334). DRY builder: it
writes DRY records only, because the h0 rows wait for pk25's MR_INSERT and the header lines X_DEFINITION and the producer orientation
check wait for G6 v1_6_2's texts (rows 4320, 4335). Usage: mrx_cert_v1.py dry N

Inputs, pinned by full sha256 here:
- pk25's certified side tables pk25/mr/v2/MR_LEMMAP.kv (MR_LEMMAP_KV_v2) and MR_SPECTRAL.kv (MR_INPUT_KV_v3), through
  pk25/mr/MANIFEST_C6A_CERT_v2.sha256 (main row 4329: the certified issue; TRIAL_SET copied from it by tool);
- the certified records: S9 (pk03 m3_s9_N<N>_J300_v1_8_3, its G entries alias S8's D), S8's E3 (f,b and fX,b), c3's CE3 (fT,b) and
  CS4 (xx, x, Z, A.yy, A.yl), c3h's CE3H (fH,b) and CS4H (xxH, xH, Z), c3j's CS4TB (xTB), c3l's CS4A (xAB).
Per piece of R4's grid (the side tables' keys, with their jlo, jhi tokens copied) and per end X in {h-1, t-1, a0}:
- each entry E(t) is enclosed over the piece through its record's uniform claim |E - sum_k ak t^k| <= err (t a ball over [1/jhi, 1/jlo],
  t = 0 on the last piece). Variant L (INFO here, uncertified for the c3 family) takes min(err, the entry's J-law at jlo) per
  PLAN_M3_LAWCERT_v1 sect. 2;
- W = span{psi-hat, e1, e3} = the S9 trial states 0, 1, 3, G their Gram (S9 G,a,b), |psi_b| = G_bb^1/2;
- w1 = Lambda_X and w2 = Lambda, with W overlaps v1_b, v2_b, and N11 = |w1|^2 (of the flip-even part for t and a), N12 = <w1, w2>,
  N22 = |w2|^2: h-1 (fH,b; f,b; xxH, xH, Z), t-1 (fT,b; f,b; (xx + xTB)/2, x, Z), a0 (fX,b; f,b; (A.yy + xAB)/2, A.yl, Z);
- |Q_W (w1 - r w2)|^2 = c0 - 2 r c1 + r^2 c2 with c0 = rho4 N11 - v1' G^-1 v1, c1 = rho4 N12 - v1' G^-1 v2, c2 = rho4 N22 - v2' G^-1 v2;
  rho4 = main_CS4 main_D / main_E3^2 = (tau_E3^2 / (tau_CS4 tau_D))^((N-1)/2), tau the weighted spanning-tree counts (matrix-tree
  theorem, in arb), the vertex graphs of riglap2.logmain;
- A~_k(w) = sum_b uhat_kb v_b / |psi_b| (MR_LEMMAP's enclosures), and Lemma A: <u_a, w> in A~_a(w) +- delta_a(w), delta_a(w) = q_a |Q_W w|
  + sum_(k != a) eps_ka |A~_k(w)| + (q_a^2 + sum_(k != a) eps_ka^2) |A~_a(w)|;
- r = <u_0, w1>/<u_0, w2>, A^a = <u_a, w1>/P0 - r <u_a, w2>/P0 with P0 = <u_0, w2> (a = x, y); the engine's Ay, Ax = A^a / s_a for the
  horizontal ends (s_a from MR_SPECTRAL), A^a for the vertical a0;
- Np >= |S P_e a| by Lemma P: |Q_W S a| + sum_k |A~_k(S a)| L_k with S a = (w1 - r w2)/P0 (h-1, t-1); for a0, whose vector is a itself,
  tau4 (|Q_W a| + sum_k |A~_k(a)| L_k);
- Axc = A_x / t: Ax-ball / t-ball on every piece with t_lo > 0 (h-1, power 1), Ax (t-1, a0, power 0). The h-1 row of the last piece writes
  nan nan (Way B pending, pk24).
Gates: C-SRC, C-MANIFEST, C-LEMMAP (header, FIELDS, rows), C-SPECTRAL, C-KEYS (same keys and jlo, jhi strings), C-RHO4 (arb against an
independent float), C-ORIENT (on every piece: the xi_TB coefficient of u~_x and the xi_TM coefficient of u~_y certainly positive, from the
stored states' coefficients), C-QW (c0, c2 not certainly negative), C-FINITE, C-ROUND (each written lo <= the exact lower end, hi >= the
upper end, as Fractions), C-FLOAT (mrx_err_v1_2's and mrx_a0_err_v1's float engine values, x flipped by sign(S[3][1]), inside the J_low
piece's intervals). Plants: PLANT-ORIENT (u~_x negated), PLANT-RHO4 (rho4 times 1 + 1e-6 against the float), PLANT-ROUND (a lo written
one unit up), PLANT-KEY (one key dropped from MR_SPECTRAL), PLANT-FLOAT (a float value moved by ten half-widths).
Outputs (mode 'x'): midrow/g4/mrc/out/dry/MR_EXACT_DRY_<V>_N<N>.kv for V in U (uniform) and L (laws, INFO) and the listing on stdout."""
import hashlib
import json
import math
import os
import re
import sys
from fractions import Fraction as Fr
import flint

flint.ctx.prec = 256
arb, fmpq, arb_mat = flint.arb, flint.fmpq, flint.arb_mat
if len(sys.argv) != 3 or sys.argv[1] != 'cert' or sys.argv[2] not in ('4', '3'):
    print('usage: mrx_cert_v1_10.py cert N   (N = 4 or 3; certified parts for mrx_combine_v1_10)')
    sys.exit(2)
N = int(sys.argv[2])
W = '/mnt/g2/release/root/code'
M3O, MYO = W + '/pk03/out', W + '/pk22/m3/out'
OUTD = W + '/pk22/midrow/g4/mrc/out/cert'   # mrx_cert_v1_8: the certified parts
MAN = W + '/pk25/mr/MANIFEST_C6A_CERT_v3.sha256'
MAN_SHA = '6c8641197635798069221101e4bec2fbc07f9462fd390b6d21a9a8b43466eb50'
MAN4 = W + '/pk25/mr/MANIFEST_MR_V4_CERT_v1.sha256'   # mrx_cert_v1_8: mr/v4 MR_SPECTRAL and MR_INSERT
MAN4_SHA = '9cf8e6d238d89eb2bb67964f1ed206a4b9b1e4fd1461b69c02d568d013817615'
REC = {4: {'S9': ('m3_s9_N4_J300_v1_8_3.json', 'bcc6434c6a03eecb232f10504b63f1ce10a94a489d5a2ba9cf3fe09c8018b831'),
           'E3': ('m3_s8v3_E3_N4_J300_v1_8_1.json', 'd1df7d4fc1b8e25f266f34c32180ccb771bc1719cc0fa730f240a33179feff0d'),
           'CE3': ('m3_c3_CE3_N4_J300_c3.json', 'ab64935d7ba4857f089d91bac27a36f76fe1d35ae228af2bc20003a8e5e3eb18'),
           'CS4': ('m3_c3_CS4_N4_J300_c3.json', 'c0614f924bedd3a68bd11cd5976e479b31a86a0e85b5ec91133f70e02ee78230'),
           'CE3H': ('m3_c3h_CE3H_N4_J300_c3h.json', '5ae505c08e3400e2a27c72038921925718f4b92622a3e95a51846dd487b59eaa'),
           'CS4H': ('m3_c3h_CS4H_N4_J300_c3h.json', '08af1a02db5b63763c244964608370a83c0d053141eafa4cb625497db2778626'),
           'CS4TB': ('m3_c3j_CS4TB_N4_J300_c3j.json', '2465c595fc04429e25c49028555d522f9f18da24cb84a53fcb5ff8c23537d555'),
           'CS4A': ('m3_c3l_CS4A_N4_J300_c3l.json', '7bdd94ca3487ee382a43d4a1a797fcb4b432acc19b2dc9b6edfef9bab43fef44'),
           'E2': ('m3_s8v3_E2_N4_J300_v1_8_1.json', 'e900cbfed6a8a69e57f849733d4740787c978c58761ea4f0fcffbf95293ee18e'),
           'FF': ('m3_s8v3_FF_N4_J300_v1_8_1.json', '042e8fc888243ac939fb9be4968f8fc9d42262a1deb7bf690993fc22a82f2a89'),
           'FFH': ('m3_c3n_FFH_N4_J300_c3n.json', 'c6ff04d12c06b5cad2ed55152313ef687a6a8a8a964ac7226936070da3d9fac3'),
           'H4TH': ('m3_c3h_H4TH_N4_J300_c3h.json', 'e46eb15b5c5618ffdf899c370bce49ff9c325bd16c5597027328e324cdb75a5d')},   # mrx_cert_v1_8: + H4TH
       3: {'S9': ('m3_s9_N3_J300_v1_8_3.json', 'd287d3dcbd4bd988aa8061fbe11b3da1609e0ab4d27ae1a619eadcee963e8fa5'),
           'E3': ('m3_s8v3_E3_N3_J300_v1_8_1.json', '6cd3dffbc6fac0845d05aa4b88f135c28a8091eb9623b779d874dace550a078a'),
           'CE3': ('m3_c3_CE3_N3_J300_c3.json', '3bedff291ef056d4664217752da3bf668fd74f8bea6a6d1696102b24aea90fa8'),
           'CS4': ('m3_c3_CS4_N3_J300_c3.json', '95f54466e52a79d8540041da90385f6683d79d5363ee2728877ba92065e88d01'),
           'CE3H': ('m3_c3h_CE3H_N3_J300_c3h.json', 'b4eab7d94ba069fa3162cb8639160d51a76e2d75f3621cf3dd2f39b1417c24dd'),
           'CS4H': ('m3_c3h_CS4H_N3_J300_c3h.json', '4481012865c8cbe275d2c3ae795aeb7b136ea588fb4ac3d38a7277c2db4733ef'),
           'CS4TB': ('m3_c3j_CS4TB_N3_J300_c3j.json', '70dd21c0f2c1971829de243c3531b09696a224852c73357474098414fc370561'),
           'CS4A': ('m3_c3l_CS4A_N3_J300_c3l.json', 'b0adfcc1b763bd532aecd7fa1bda3a54ed20265e014517996cbcff60b3f3c6be'),
           'E2': ('m3_s8v3_E2_N3_J300_v1_8_1.json', '3e7f7bf6101bc45282a202d85e3182b2340bff4d7d349bc78eb33d5d9f02f5d5'),
           'FF': ('m3_s8v3_FF_N3_J300_v1_8_1.json', 'dae3cfa88bf06fd97378108b9ceba0a85044f7790b38e67c0b86eb23d6443008'),
           'FFH': ('m3_c3n_FFH_N3_J300_c3n.json', '642d3df737dbed3f02e6677bd59aaacbc70d74ba6f893704e46d7e22489b3507'),
           'H4TH': ('m3_c3h_H4TH_N3_J300_c3h.json', '8721aa431947a15a5ba570c1974b6023b1de192fc7ef8f0743e591d476b3aeb5')}}[N]   # mrx_cert_v1_8: + H4TH
TSF = {4: W + '/pk11/out/ts_N4_J170_D_S_z9sym_v1.json', 3: W + '/pk11/out/ts_N3_S_z9sym_v1.json'}[N]
TSF_SHA = {4: 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d', 3: 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6'}[N]
MRXERR = (W + '/pk22/midrow/g4/mrx/out/mrx_err_v1_2_n%d.out' % N, {4: '03e6fb9d', 3: 'eb94f546'}[N])
MRXA0 = (W + '/pk22/midrow/g4/mrx/out/mrx_a0_err_v1_n%d.out' % N, {4: 'bb096e93', 3: '043aa549'}[N])
CERTSRC = {   # mrx_cert_v1_5: the reader fork, the two law certificates with their jobs' outputs, and the S8 records and asm outputs
    'READER': ({4: '/mnt/g2/release/root/code/pk22/m3/m3_reader_c3h_v1_1.py', 3: '/mnt/g2/release/root/code/pk22/m3/m3_reader_c3h_v1_1.py'}[N], {4: 'febfafab27d4f5d5e4b603128159c411db2f84f9af2a5facf12be316571e6d9e', 3: 'febfafab27d4f5d5e4b603128159c411db2f84f9af2a5facf12be316571e6d9e'}[N]),   # mrx_cert_v1_9: the reader fork v1_1
    'C_c3h': ({4: '/mnt/g2/release/root/code/pk22/m3/out/m3_lawcert_c3h_v1_1_N4.json', 3: '/mnt/g2/release/root/code/pk22/m3/out/m3_lawcert_c3h_v1_1_N3.json'}[N], {4: '75eb63eb28efd31875cc7a9b2e8596b9e1096abbbeaa1fec674e5265310f7b5f', 3: '05ee268c4dae3be99361652f07ee95d7b744dfead75dc994ca79399bbff2887d'}[N]),   # mrx_cert_v1_9: m3_lawcert_c3h_v1_1's certificates
    'O_c3h': ({4: '/mnt/g2/release/root/code/pk22/m3/out/m3_lawcert_c3h_v1_1_4.out', 3: '/mnt/g2/release/root/code/pk22/m3/out/m3_lawcert_c3h_v1_1_3.out'}[N], {4: '3ef6e59b6df1a40f6d95bd00a6b65387cd19926f1a57372506f6b2195f1fd234', 3: '054734389a93a9a272ce2ccec75e2d24808acd0edfc8824daa6b8ce4e18d8841'}[N]),   # mrx_cert_v1_9: their jobs' outputs
    'A_c3h': ({4: '/mnt/g2/release/root/code/pk22/m3/out/m3_run_v1_9_3_asm.4_c3h_1.out', 3: '/mnt/g2/release/root/code/pk22/m3/out/m3_run_v1_9_3_asm.3_c3h_1.out'}[N], {4: '5b03e7f3d54ec403c6d7e10768ad006f38c1b1b527a6f0715fa6971f767c50aa', 3: '96e1fd949ef18bdf88e234f8d535a30bae4516a24f1a33505936e42e87ad58f8'}[N]),
    'C_s8': ({4: '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_N4.json', 3: '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_N3.json'}[N], {4: '5b7cbff9443f4ff69e623caa776646b16629aa2b6436c186e1799e9f4d56ba4c', 3: 'ec50ab52cd88b7b0cbd717c6dc4db295e72a8faf10b378b994a4f83cc5d7cfd4'}[N]),
    'O_s8': ({4: '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_4.out', 3: '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_3.out'}[N], {4: 'f814f9f301f8814117dfccbd6715f8ff04e6cd24dcef04e4a95ecaaeb6e37325', 3: '2b7847dc902eed4dda6800ff2118d8c378421179ba4d77242b83dc9086c772d9'}[N]),
    'A_s8': ({4: '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_1_asmP.4.out', 3: '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_1_asmP.3.out'}[N], {4: '08c8fab3f4b9080424a40c8cb61b7932f557852520e8d49c5915092a8963a127', 3: 'b6e9c2dd6a6308f6dc8d72124ba37326156983ec3444625d152ab46f28e927ed'}[N]),
    'R_s8_D': ({4: '/mnt/g2/release/root/code/pk03/out/m3_s8v3_D_N4_J300_v1_8_1.json', 3: '/mnt/g2/release/root/code/pk03/out/m3_s8v3_D_N3_J300_v1_8_1.json'}[N], {4: '389be198d9fe919e1a097865759691847a9e4dc7553275c083d91bd753819b00', 3: '8707107b0ebc3dea6989d22b6284f9df368c954837c883dc36824edda63c4926'}[N]),
    'R_s8_E2': ({4: '/mnt/g2/release/root/code/pk03/out/m3_s8v3_E2_N4_J300_v1_8_1.json', 3: '/mnt/g2/release/root/code/pk03/out/m3_s8v3_E2_N3_J300_v1_8_1.json'}[N], {4: 'e900cbfed6a8a69e57f849733d4740787c978c58761ea4f0fcffbf95293ee18e', 3: '3e7f7bf6101bc45282a202d85e3182b2340bff4d7d349bc78eb33d5d9f02f5d5'}[N]),
    'R_s8_FF': ({4: '/mnt/g2/release/root/code/pk03/out/m3_s8v3_FF_N4_J300_v1_8_1.json', 3: '/mnt/g2/release/root/code/pk03/out/m3_s8v3_FF_N3_J300_v1_8_1.json'}[N], {4: '042e8fc888243ac939fb9be4968f8fc9d42262a1deb7bf690993fc22a82f2a89', 3: 'dae3cfa88bf06fd97378108b9ceba0a85044f7790b38e67c0b86eb23d6443008'}[N]),
}
CERTDEF = {'c3h': ('m3_lawcert_c3h_v1_1.py', ('CE3H', 'CS4H', 'H4TH'), MYO + '/m3_c3h_%%s_N%d_J300_c3h.json' % N, 'A_c3h', 'C_c3h', 'O_c3h'),   # v1_9
           's8': ('m3_lawcert_v1_1.py', ('D', 'E2', 'E3', 'FF'), M3O + '/m3_s8v3_%%s_N%d_J300_v1_8_1.json' % N, 'A_s8', 'C_s8', 'O_s8')}   # mrx_cert_v1_5
LEMMAP_FIELDS = ('jlo jhi rho0_hi rhox_hi rhoy_hi mu0_lo mux_lo muy_lo tau_hi L0_hi Lx_hi Ly_hi u0p_lo u0p_hi u01_lo u01_hi u03_lo u03_hi '
                 'uxp_lo uxp_hi ux1_lo ux1_hi ux3_lo ux3_hi uyp_lo uyp_hi uy1_lo uy1_hi uy3_lo uy3_hi q0_hi qx_hi qy_hi eps_x0_hi eps_y0_hi '
                 'eps_0x_hi eps_yx_hi eps_0y_hi eps_xy_hi').split()
SPECTRAL_FIELDS = 'jlo jhi sx_lo sx_hi sy_lo sy_hi tau_hi rho1_hi Rw_hi cxm1_lo cxm1_hi cym1_lo cym1_hi'.split()
OUT_FIELDS = 'jlo jhi Ay_lo Ay_hi Ax_lo Ax_hi Np_hi Ay_mid Axc_lo Axc_hi Axf_hi Pe_hi'   # mrx_cert_v1_7: + Pe_hi (G6 v1_6_2 sect. 6)
X_POWER = 'h-1 1, h0 1, t-1 0, a0 0'
ENDS = ('h-1', 'h0', 't-1', 'a0')   # mrx_cert_v1_8: + h0
ENDS3 = ('h-1', 't-1', 'a0')   # the ends with a norm entry (EV, NE)
LV = ('0', 'x', 'y')        # Ritz levels
BV = ('p', '1', '3')        # W's basis labels: psi-hat (state 0), e1 (state 1), e3 (state 3)
ST = (0, 1, 3)
FAILS, NOFIRE = [], []


def out(line):
    print(line, flush=True)


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def fr_of(x):
    """an exact arb endpoint (or an exact arb) as a Fraction."""
    m, e = x.man_exp()
    m, e = int(m), int(e)
    return Fr(m) * (Fr(2) ** e) if e >= 0 else Fr(m, 2 ** (-e))


def ab(q):
    """a ball holding the exact rational q."""
    q = Fr(q)
    return arb(fmpq(q.numerator, q.denominator))


def hull(lo, hi):
    return ab(lo).union(ab(hi))


def lo_of(x):
    return fr_of(x.lower())


def hi_of(x):
    return fr_of(x.upper())


def absup(x):
    return max(abs(lo_of(x)), abs(hi_of(x)))


def dec(q, up):
    """the 17-significant-digit decimal string nearest q in the given direction (up: >= q; down: <= q), from exact integers."""
    q = Fr(q)
    if q == 0:
        return '0'
    neg = q < 0
    m = -q if neg else q
    e = len(str(m.numerator)) - len(str(m.denominator))
    while Fr(10) ** e > m:
        e -= 1
    while Fr(10) ** (e + 1) <= m:
        e += 1
    scale = Fr(10) ** (16 - e)
    v = m * scale
    away = (up and not neg) or (neg and not up)
    n = (v.numerator + v.denominator - 1) // v.denominator if away else v.numerator // v.denominator
    if n >= 10 ** 17:
        n //= 10
        e += 1
        n = n + 1 if away and Fr(n) * Fr(10) ** (e - 16) < m else n
    s = str(n)
    txt = '%s%s.%se%s%02d' % ('-' if neg else '', s[0], s[1:], '-' if e < 0 else '+', abs(e))
    assert (Fr(txt) >= q) if up else (Fr(txt) <= q), (txt, q, up)
    return txt


# ---- inputs and pins
srcs = {'MANIFEST': (MAN, MAN_SHA), 'MANIFEST4': (MAN4, MAN4_SHA), 'TS': (TSF, TSF_SHA)}
srcs.update(('R_' + k, (os.path.join(M3O if k in ('S9', 'E3', 'E2', 'FF') else MYO, f), h)) for k, (f, h) in REC.items())   # mrx_cert_v1_7: E2, FF
srcs.update(CERTSRC)   # mrx_cert_v1_5
shas = dict((k, sha(p)) for k, (p, h) in srcs.items())
gate('C-SRC', all(shas[k] == h for k, (p, h) in srcs.items()), '(%s)' % ', '.join('%s %s' % (os.path.basename(p), shas[k][:8]) for k, (p, h) in srcs.items()))
man = {}
for ln in open(MAN):
    h, name = ln.split()
    man[name] = h
LEMF, SPEF3 = W + '/pk25/mr/v3/MR_LEMMAP.kv', W + '/pk25/mr/v3/MR_SPECTRAL.kv'
SPEF, INSF = W + '/pk25/mr/v4/MR_SPECTRAL.kv', W + '/pk25/mr/v4/MR_INSERT.kv'   # mrx_cert_v1_8: the certified mr/v4 records
lem_sha, spe3_sha, spe_sha, ins_sha = sha(LEMF), sha(SPEF3), sha(SPEF), sha(INSF)
man4 = dict((ln.split()[1], ln.split()[0]) for ln in open(MAN4) if ln.strip())
gate('C-MANIFEST', man.get('mr/v3/MR_LEMMAP.kv') == lem_sha and man.get('mr/v3/MR_SPECTRAL.kv') == spe3_sha
     and man4.get('mr/v4/MR_SPECTRAL.kv') == spe_sha and man4.get('mr/v4/MR_INSERT.kv') == ins_sha,
     '(mr/v3: MR_LEMMAP.kv %s and MR_SPECTRAL.kv %s as MANIFEST_C6A_CERT_v3 lists them; mr/v4: MR_SPECTRAL.kv %s and MR_INSERT.kv %s as '
     'MANIFEST_MR_V4_CERT_v1 lists them)' % (lem_sha[:16], spe3_sha[:16], spe_sha[:16], ins_sha[:16]))


def read_kv(path):
    head, rows = {}, {}
    for ln in open(path):
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#'):
            continue
        k, sep, v = ln.partition(' = ')
        assert sep, ln[:80]
        if re.fullmatch(r'N[34]_P[0-9]{4}', k):
            assert k not in rows, k
            rows[k] = v.split()
        else:
            assert k not in head, k
            head[k] = v
    return head, rows


LH, LR = read_kv(LEMF)
SH, SR = read_kv(SPEF)
SH3, SR3 = read_kv(SPEF3)   # mrx_cert_v1_8: mr/v3, for the rows-equal check
okl = (LH.get('FORMAT') == 'MR_LEMMAP_KV_v2' and LH.get('RECORD') == 'MR_LEMMAP' and LH.get('PRODUCER', '').split()[:1] == ['pk25']
       and LH.get('STATUS') == 'CERTIFIED' and LH.get('EXPORT_STATUS') == 'CERTIFIED' and LH.get('RUN_VERDICT') == 'VALID'
       and LH.get('ORIENTATION') == 'u_x along e1, u_y along e3' and LH.get('FIELDS', '').split() == LEMMAP_FIELDS
       and all(len(v) == len(LEMMAP_FIELDS) for v in LR.values()))
gate('C-LEMMAP', okl, '(FORMAT %s, PRODUCER %s, STATUS %s, %d rows of %d fields)' % (LH.get('FORMAT'), LH.get('PRODUCER'), LH.get('STATUS'),
                                                                                  len(LR), len(LEMMAP_FIELDS)))
oks = (SH.get('FORMAT') == 'MR_INPUT_KV_v4' and SH.get('RECORD') == 'MR_SPECTRAL' and SH.get('PRODUCER', '').split()[:1] == ['pk25'] and SR == SR3
       and SH.get('EXPORT_STATUS') == 'CERTIFIED' and SH.get('RUN_VERDICT') == 'VALID' and SH.get('ORIENTATION') == 'u_x along e1, u_y along e3'
       and SH.get('FIELDS', '').split() == SPECTRAL_FIELDS and all(len(v) == len(SPECTRAL_FIELDS) for v in SR.values())
       and SH.get('TRIAL_SET') == LH.get('TRIAL_SET'))
gate('C-SPECTRAL', oks, '(mr/v4: FORMAT %s, RECORD %s, %d rows, every row equal to mr/v3\'s: %s; TRIAL_SET equal to MR_LEMMAP\'s: %s)' % (
    SH.get('FORMAT'), SH.get('RECORD'), len(SR), SR == SR3, SH.get('TRIAL_SET') == LH.get('TRIAL_SET')))
# ---- mrx_cert_v1_8: pk25's certified MR_INSERT (mr/v4), whose h row feeds h0's r_W and Pe_hi
INSERT_FIELDS = ('jlo jhi vx_lo vx_hi vy_lo vy_hi Pevw_hi Pev_hi vp_hi mxx_lo mxx_hi mxy_lo mxy_hi myy_lo myy_hi PeBwux_hi PeBwuy_hi win_hi C_hi '
                 'windowed xc_lo xc_hi xf_hi').split()


def read_ins(path):
    head, rows = {}, {}
    for ln in open(path):
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#'):
            continue
        k, sep, v = ln.partition(' = ')
        assert sep, ln[:80]
        if re.fullmatch(r'N[34]_P[0-9]{4}_[hta]', k):
            assert k not in rows, k
            rows[k] = v.split()
        else:
            assert k not in head, k
            head[k] = v
    return head, rows


IH, IR = read_ins(INSF)
WIN_I = INSERT_FIELDS.index('windowed')
oki = (IH.get('FORMAT') == 'MR_INPUT_KV_v4' and IH.get('RECORD') == 'MR_INSERT' and IH.get('PRODUCER', '').split()[:1] == ['pk25']
       and IH.get('STATUS') == 'CERTIFIED' and IH.get('EXPORT_STATUS') == 'CERTIFIED' and IH.get('RUN_VERDICT') == 'VALID'
       and IH.get('ORIENTATION') == 'u_x along e1, u_y along e3' and IH.get('TRIAL_SET') == LH.get('TRIAL_SET')
       and IH.get('LEMMAP_SHA256') == lem_sha and IH.get('FIELDS', '').split() == INSERT_FIELDS
       and all(len(v) == len(INSERT_FIELDS) for v in IR.values()) and sorted(IR) == sorted(k + s for k in SR for s in ('_h', '_t', '_a'))
       and all(IR[k + s][:2] == SR[k][:2] for k in SR for s in ('_h', '_t', '_a'))
       and all(IR[k + '_h'][WIN_I] == '1' and IR[k + '_t'][WIN_I] == '1' and IR[k + '_a'][WIN_I] == '0' for k in SR))
gate('C-INSERT', oki, '(mr/v4 MR_INSERT: FORMAT %s, PRODUCER %s, STATUS %s, EXPORT_STATUS %s, RUN_VERDICT %s; FIELDS as G6 v1_6_2 sect. 6; '
     'LEMMAP_SHA256 is MR_LEMMAP\'s; TRIAL_SET equal; %d rows: h, t and a on every MR_SPECTRAL key with its jlo, jhi; h and t windowed, a not)' % (
         IH.get('FORMAT'), IH.get('PRODUCER'), IH.get('STATUS'), IH.get('EXPORT_STATUS'), IH.get('RUN_VERDICT'), len(IR)))
TRIAL_SET = LH.get('TRIAL_SET', '')
gate('C-TRIALSET', ('ts_N%d' % N) in TRIAL_SET and TSF_SHA in TRIAL_SET, '(the side tables\' TRIAL_SET names %s with its full sha256)' % os.path.basename(TSF))
keysN = sorted(k for k in LR if k.startswith('N%d_' % N))


def keys_ok(lr, sr):
    kl = sorted(k for k in lr if k.startswith('N%d_' % N))
    ks = sorted(k for k in sr if k.startswith('N%d_' % N))
    return kl == ks and all(lr[k][0] == sr[k][0] and lr[k][1] == sr[k][1] for k in kl)


gate('C-KEYS', keys_ok(LR, SR) and len(keysN) > 0, '(N = %d: %d keys, the same in both tables, jlo and jhi strings equal; first %s [%s, %s], last %s [%s, %s])' % (
    N, len(keysN), keysN[0], LR[keysN[0]][0], LR[keysN[0]][1], keysN[-1], LR[keysN[-1]][0], LR[keysN[-1]][1]))
SR2 = dict(SR)
SR2.pop(keysN[len(keysN) // 2])
plant('PLANT-KEY', not keys_ok(LR, SR2), '(MR_SPECTRAL without %s)' % keysN[len(keysN) // 2])
RJ = dict((k, json.load(open(srcs['R_' + k][0]))) for k in REC)
ALIAS = {}


def item_of(rk, key):
    rec, it, hops = RJ[rk], RJ[rk]['items'][key], 0
    while it.get('alias_of'):
        fn, k2, h = it['alias_of'].split()
        p = os.path.join(M3O, os.path.basename(fn))
        if p not in ALIAS:
            assert sha(p) == h, p
            ALIAS[p] = json.load(open(p))
        rec, it, hops = ALIAS[p], ALIAS[p]['items'][k2], hops + 1
        assert hops <= 4
    assert it['kind'] == 'entry' and it['parity'] == 'free', (rk, key)
    assert rec.get('J_REF') == 300 and rec.get('N') == N and rec.get('claim', '').startswith('for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err'), (rk, key)
    return it


def chi2_tail(n, x):
    """Prob(chi^2_n > x) for n = 2, 3 (x an arb, x >= 0)."""
    if n == 2:
        return (-x / 2).exp()
    assert n == 3
    return (x / 2).sqrt().erfc() + (2 * x / arb.pi()).sqrt() * (-x / 2).exp()


def p_law(g, J):
    return sum((chi2_tail(int(g['n']), ab(J) * arb(a) / arb(G)) for a, G in g['a_G']), arb(0))


# ---- mrx_cert_v1_5: the certified J-laws through the reader fork (load bound to the asm outputs, load_lawcert to the certificate jobs' outputs)
import importlib.util


def load_as(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


RDR = load_as('m3_reader_c3h_v1_1', CERTSRC['READER'][0])   # mrx_cert_v1_9
CERTS, CERT_RECS = {}, {}
for cn, (prod, fams, rfmt, ak_, ck_, ok_k) in CERTDEF.items():
    asm_, cfile, cout = CERTSRC[ak_][0], CERTSRC[ck_][0], CERTSRC[ok_k][0]
    recs = dict((f, RDR.load(rfmt % f, asm_, 300, N)) for f in fams)
    try:
        cobj = RDR.load_lawcert(cfile, cout, 300, N, recs)
        okc, why = cobj['producer'] == prod, 'producer %s, %d entries' % (cobj['producer'], len(cobj['entries']))
    except ValueError as ex:
        cobj, okc, why = None, False, 'refused: %s' % str(ex)[:160]
    CERTS[cn], CERT_RECS[cn] = cobj, recs
    gate('C-LAWCERT', okc, '(%s: %s through m3_reader_c3h_v1_1.load_lawcert bound to %s; its records %s through load bound to %s: %s)' % (
        cn, os.path.basename(cfile), os.path.basename(cout), ', '.join(recs[f]['name'] for f in fams), os.path.basename(asm_), why))
try:
    RDR.load_lawcert(CERTSRC['C_c3h'][0], CERTSRC['O_s8'][0], 300, N, CERT_RECS['c3h'])
    fired = False
except ValueError:
    fired = True
plant('PLANT-LAWCERT', fired, '(the c3h certificate offered with m3_lawcert_v1_1\'s job output must be refused)')


def cert_law(rk, key):
    """mrx_cert_v1_5: the certified law of record rk's entry key (m3_reader_c3h_v1.entry_law), or None: c3h's for CE3H and CS4H, m3_lawcert_v1_1's
    for S8's E3 and for S9's G entries whose alias is an item of the S8 D record that certificate binds (file name and sha256)."""
    if rk in ('CE3H', 'CS4H', 'H4TH') and CERTS.get('c3h') is not None:   # mrx_cert_v1_9: + H4TH (m3_lawcert_c3h_v1_1)
        return RDR.entry_law(CERTS['c3h'], rk, key)
    if rk == 'E3' and CERTS.get('s8') is not None:
        return RDR.entry_law(CERTS['s8'], 'E3', key)
    if rk in ('E2', 'FF') and CERTS.get('s8') is not None:   # mrx_cert_v1_7: S8's E2 and FF, certified by m3_lawcert_v1_1 too
        return RDR.entry_law(CERTS['s8'], rk, key)
    if rk == 'S9' and CERTS.get('s8') is not None:
        al = RJ['S9']['items'][key].get('alias_of')
        if al:
            fn, k2, h = al.split()
            d = CERT_RECS['s8']['D']
            if os.path.basename(fn) == d['name'] and h == d['sha256']:
                return RDR.entry_law(CERTS['s8'], 'D', k2)
    return None


def p_lawq(g, J):
    """P(J; x) of LAWCERT_CLAIM from a certified law part (exact rationals): sum over [a, G] of Prob(chi^2_n > J a / G)."""
    return sum((chi2_tail(int(g['n']), ab(J) * ab(a) / ab(G)) for a, G in g['a_G']), arb(0))


class Ent:
    def __init__(self, rk, key):
        it = item_of(rk, key)
        self.name = '%s:%s' % (rk, key)
        self.ak = [arb(float(c)) for c in it['ak']]
        self.err = Fr(float(it['err']))
        self.it = it
        self.claw = cert_law(rk, key)   # mrx_cert_v1_5: the certified law, or None

    def cert_err(self, jlo):
        """mrx_cert_v1_5: LAWCERT_CLAIM's right side at jlo from the certified law (exact rationals; arb, outward rounding): rem (300/J)^4 +
        tail (P(J)/P(300))^(1/2) + ann (P(J)/P(300))^(1/2) + far exp(-far_rate (J - 300)) + sum_k ak_rad[k] J^-k; every term is
        non-increasing in J, so its value at jlo bounds the piece."""
        cl, J = self.claw, Fr(jlo)
        lw, bp = cl['laws'], cl['parts']
        e = ab(bp['rem']) * (ab(Fr(300) / J) ** 4)
        for part in ('tail', 'ann'):
            e = e + ab(bp[part]) * (p_lawq(lw[part], J) / p_lawq(lw[part], Fr(300))).sqrt()
        e = e + ab(bp['far']) * (-ab(lw['far_rate']) * ab(J - 300)).exp()
        e = e + sum((ab(r) * ab(Fr(1) / J) ** k for k, r in enumerate(cl['ak_rad'])), arb(0))
        return hi_of(e)

    def err_at(self, jlo, laws):
        """mrx_cert_v1_5: the error the entry takes on a piece starting at jlo: the uniform claim (laws False), min with the certified J-law
        where a certificate covers the entry, else the uniform claim (laws 'C')."""
        if laws == 'C':
            return min(self.err, self.cert_err(jlo)) if self.claw is not None else self.err
        return min(self.err, self.law_err(jlo)) if laws else self.err

    def law_err(self, jlo):
        """the entry's J-law at jlo (PLAN_M3_LAWCERT_v1 sect. 2), an upper bound over the piece (every term non-increasing in J)."""
        it, J = self.it, Fr(jlo)
        if not it.get('laws') or 'Bp' not in it:
            return self.err
        lw, bp = it['laws'], it['Bp']
        e = arb(float(bp['rem'])) * (ab(Fr(300) / J) ** 4)
        for part in ('tail', 'ann'):
            e = e + arb(float(bp[part])) * (p_law(lw[part], J) / p_law(lw[part], Fr(300))).sqrt()
        e = e + arb(float(bp['far'])) * (-arb(float(lw['far_rate'])) * ab(J - 300)).exp()
        e = e + sum((arb(float(r)) * ab(Fr(1) / J) ** k for k, r in enumerate(it.get('ak_rad', []))), arb(0))
        return hi_of(e)

    def ball(self, T, jlo, laws):
        v = arb(0)
        for c in reversed(self.ak):
            v = v * T + c
        return v + arb(0, ab(self.err_at(jlo, laws)).upper())   # mrx_cert_v1_5


S9G = dict(((a, b), Ent('S9', 'G,%d,%d' % (min(a, b), max(a, b)))) for a in ST for b in ST)
EV = {'h-1': ([Ent('CE3H', 'fH,%d' % b) for b in ST], [Ent('E3', 'f,%d' % b) for b in ST], ('CS4H', 'xxH', None), ('CS4H', 'xH'), ('CS4H', 'Z')),
      't-1': ([Ent('CE3', 'fT,%d' % b) for b in ST], [Ent('E3', 'f,%d' % b) for b in ST], ('CS4', 'xx', ('CS4TB', 'xTB')), ('CS4', 'x'), ('CS4', 'Z')),
      'a0': ([Ent('E3', 'fX,%d' % b) for b in ST], [Ent('E3', 'f,%d' % b) for b in ST], ('CS4', 'A.yy', ('CS4A', 'xAB')), ('CS4', 'A.yl'), ('CS4', 'Z'))}
NE = {}
for end, (v1, v2, n11, n12, n22) in EV.items():
    NE[end] = (Ent(n11[0], n11[1]), Ent(n11[2][0], n11[2][1]) if n11[2] else None, Ent(*n12), Ent(*n22))

PE_E2 = [Ent('E2', 'e,%d' % b) for b in ST]   # mrx_cert_v1_7: <psi_b, x_w> (S8's E2, [vac, free])
PE_Z = Ent('FFH', 'Z0')   # mrx_cert_v1_7: <x_w, x_w> (runner c3n_1)
PE_W = {'h-1': (Ent('FFH', 'WH1'), Ent('FFH', 'WH2')), 't-1': (Ent('FFH', 'WT1'), Ent('FFH', 'WT2'))}   # mrx_cert_v1_7: <x_w, M^k x_w>
S8Z = Ent('FF', 'z')   # mrx_cert_v1_7: S8's FF z, C-Z0's control for Z0
H0V = ([Ent('H4TH', 'hH,%d' % b) for b in ST], [Ent('H4TH', 'h0,%d' % b) for b in ST])   # mrx_cert_v1_8: w1 = S M_h l_2, w2 = S l_2 (c3h's H4TH)


# ---- mrx_cert_v1_10: Way A on the last piece for h-1 and h0 (see the docstring)
WAYA_SRC = {'P2': (W + '/pk25/p2/v3f2/MR_LEMMAP_V3F.kv', '9ef6abafdf450eff317545dd95aff519051352db3c01c752f739466a616d48c4'), 'P2MAN': (W + '/pk25/p2/MANIFEST_P2_V2_3_CERT_c1.sha256', 'a0dd069903fbfa6e69fba33b21e6f8d9d33f256a45097f7273bab7432ae66c29'),
            'C10': (W + '/pk25/c10/C10_RECORD_v1.kv', '29a4f3c67afc2b3e2611e37e3026def71d6ae819bcc2ee5ed34f678734bebb98'), 'C10MAN': (W + '/pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256', 'bf8df39779ec0d3a797f13a67d73fd83a01ff27b437add8f84d7ab0c9884c183'),
            'C13': (W + '/pk25/c13/C13_RECORD_v1_1.kv', '1ff7fcef9c8841269037df9eef478d58c8373b22bea5b27ede3b18b288f6a567'), 'C13MAN': (W + '/pk25/c13/MANIFEST_C13_V1_1_CERT_c2.sha256', '14aeb7415e8e5efb5d14434fd31e2d6a514d8467b1c564907723d732861e695b')}
WAYA_KEYS = (keysN[-1], keysN[-2])          # the last piece (Way A) and the piece before it (C-WAYA-CONT's control)
WAYA_BAD, WAYA_LOG = [], {}


class WayaRefused(ValueError):
    pass


def waya_arb(e):
    """an exact sympy number (rationals, square roots, sums, products, integer powers) as an arb ball (pk25's waya_arb, kt_s9h_ins_v2_7)."""
    import sympy as sp
    if e.is_Rational:
        return arb(int(e.p)) / arb(int(e.q))
    if e.is_Add:
        s = arb(0)
        for x in e.args:
            s += waya_arb(x)
        return s
    if e.is_Mul:
        s = arb(1)
        for x in e.args:
            s *= waya_arb(x)
        return s
    if e.is_Pow:
        b, x = e.args
        if x == sp.Rational(1, 2):
            return waya_arb(b).sqrt()
        if x == -sp.Rational(1, 2):
            return 1 / waya_arb(b).sqrt()
        if x.is_Integer:
            return waya_arb(b) ** int(x)
    raise WayaRefused('C-WAYA-IN: waya_arb cannot convert %s' % e)


def waya_kv(path):
    head, rows, ix = {}, {}, None
    for ln in open(path).read().splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        if ' = ' not in ln:
            raise WayaRefused('C-WAYA-IN: a line without " = " in %s' % os.path.basename(path))
        k, v = ln.split(' = ', 1)
        if k == 'FIELDS':
            ix = dict((f, i) for i, f in enumerate(v.split()))
        elif re.fullmatch(r'N[34]_P[0-9]+', k):
            rows[k] = v.split()
        elif k in head:
            raise WayaRefused('C-WAYA-IN: the header key %s twice in %s' % (k, os.path.basename(path)))
        else:
            head[k] = v
    return head, rows, ix


def waya_load(src=None):
    """C-WAYA-IN: P2's MR_LEMMAP_V3F (the /t table), P1's C10 record (exact uhat(0), the t^0 Gram G0 on W) and C13's record (C-BH0), each
    pinned and a row of its pk25 manifest (paths relative to pk25/). P2: FORMAT MR_LEMMAP_KV_v3F, RECORD MR_LEMMAP_F, STATUS CERTIFIED,
    RUN_VERDICT VALID, SOURCE naming this run's MR_LEMMAP v3 and the pinned C10, ORIENTATION as MR_LEMMAP v3; C10: certified, valid, N<N>_UHAT0
    equal to P2's, uhat_0(0) = (1, 0, 0), G0_00 = 1; C13: a certified C13_KV_v1 whose CLAIM states C-BH0 exactly."""
    import sympy as sp
    src = WAYA_SRC if src is None else src
    for k, (p, h) in src.items():
        if sha(p) != h:
            raise WayaRefused('C-WAYA-IN: %s does not match its pin' % os.path.basename(p))
    for f, m in (('P2', 'P2MAN'), ('C10', 'C10MAN'), ('C13', 'C13MAN')):
        mrows = dict((ln.split()[1], ln.split()[0]) for ln in open(src[m][0]).read().splitlines() if len(ln.split()) == 2)
        if mrows.get(os.path.relpath(src[f][0], W + '/pk25')) != src[f][1]:
            raise WayaRefused('C-WAYA-IN: %s is not a row of %s' % (os.path.basename(src[f][0]), os.path.basename(src[m][0])))
    h2, rows2, ix2 = waya_kv(src['P2'][0])
    hc = waya_kv(src['C10'][0])[0]
    h13 = waya_kv(src['C13'][0])[0]
    if (h2.get('FORMAT'), h2.get('RECORD'), h2.get('STATUS'), h2.get('RUN_VERDICT')) != ('MR_LEMMAP_KV_v3F', 'MR_LEMMAP_F', 'CERTIFIED', 'VALID') or ix2 is None:
        raise WayaRefused('C-WAYA-IN: the P2 record is not a certified valid MR_LEMMAP_KV_v3F record')
    if ('MR_LEMMAP v3 %s;' % lem_sha[:8]) not in h2.get('SOURCE', '') or ('C10 %s;' % src['C10'][1][:8]) not in h2.get('SOURCE', ''):
        raise WayaRefused('C-WAYA-IN: the P2 record SOURCE does not name this run\'s MR_LEMMAP v3 and the pinned C10 record')
    if not h2.get('ORIENTATION', '').startswith('u_x along e1, u_y along e3'):
        raise WayaRefused('C-WAYA-IN: the P2 record ORIENTATION is not MR_LEMMAP v3\'s')
    if (hc.get('FORMAT'), hc.get('STATUS'), hc.get('RUN_VERDICT')) != ('C10_KV_v1', 'CERTIFIED', 'VALID'):
        raise WayaRefused('C-WAYA-IN: the C10 record is not a certified valid C10_KV_v1')
    if (h13.get('FORMAT'), h13.get('STATUS')) != ('C13_KV_v1', 'CERTIFIED') or 'C-BH0 holds exactly' not in h13.get('CLAIM', ''):
        raise WayaRefused('C-WAYA-IN: the C13 record is not a certified C13_KV_v1 stating C-BH0 exactly')
    raw = hc.get('N%d_UHAT0' % N)
    if raw is None or h2.get('N%d_UHAT0' % N) != raw:
        raise WayaRefused('C-WAYA-IN: N%d_UHAT0 differs between the P2 and C10 records' % N)
    u = {}
    for part in raw.split('; '):
        nm, ex = part.split(' ', 1)
        mt = re.fullmatch(r'u([0xy])([p13])', nm)
        if mt is None or (mt.group(1), mt.group(2)) in u:
            raise WayaRefused('C-WAYA-IN: N%d uhat name %r' % (N, nm))
        u[(mt.group(1), mt.group(2))] = sp.sympify(ex)
    if len(u) != 9 or [u[('0', b)] for b in 'p13'] != [1, 0, 0]:
        raise WayaRefused('C-WAYA-IN: N%d_UHAT0 is not nine values with uhat_0(0) = (1, 0, 0)' % N)
    mg = re.fullmatch(r'G \[(.+)\]; T \[(.+)\] \(psi-hat, s1, s3 unnormalised, t\^0\)', hc.get('N%d_GT0_W' % N, ''))
    if mg is None:
        raise WayaRefused('C-WAYA-IN: N%d_GT0_W does not parse' % N)
    G0 = [sp.sympify(e) for e in mg.group(1).split(', ')]
    if len(G0) != 9 or G0[0] != 1:
        raise WayaRefused('C-WAYA-IN: N%d G0 is not 3 x 3 with G0_00 = 1' % N)
    return dict(rows=rows2, ix=ix2, ux0=[waya_arb(u[('x', b)]) for b in 'p13'], uy0=[waya_arb(u[('y', b)]) for b in 'p13'],
                G0d=[waya_arb(G0[0]), waya_arb(G0[4]), waya_arb(G0[8])])


def waya_ent(e):
    """(record, certificate, family, key) of Ent e for the reader's entry_ball and entry_law: CE3H and H4TH from c3h's records and certificate,
    E3 from S8's, S9's G entries through their alias in S8's D record (file name and sha256 checked), as cert_law takes them."""
    rk, key = e.name.split(':', 1)
    if rk in ('CE3H', 'H4TH') and CERTS.get('c3h') is not None:
        return CERT_RECS['c3h'][rk], CERTS['c3h'], rk, key
    if rk == 'E3' and CERTS.get('s8') is not None:
        return CERT_RECS['s8']['E3'], CERTS['s8'], 'E3', key
    if rk == 'S9' and CERTS.get('s8') is not None:
        fn, k2, h = RJ['S9']['items'][key]['alias_of'].split()
        d = CERT_RECS['s8']['D']
        if os.path.basename(fn) == d['name'] and h == d['sha256']:
            return d, CERTS['s8'], 'D', k2
    raise WayaRefused('C-WAYA-IN: no certified law for %s' % e.name)


def waya_rt(law, J_lo, t_hi):
    """R/t over a piece starting at J_lo (t <= t_hi): rem 300^4 t_hi^3 + J_lo (tail (P(J_lo)/P(300))^1/2 + ann (P(J_lo)/P(300))^1/2 +
    far e^(-far_rate (J_lo - 300))), the law's four parts without the ak_rad term (entry_law's N-1), with C-MONO-TAIL (J_lo a/G > 5 for every
    chi-square pair, so J^2 P(J) decreases) and C-MONO-FAR (J_lo far_rate > 1, so J e^(-far_rate J) decreases); pk25's waya_rt."""
    L, parts = law['laws'], law['parts']
    if L is None:
        return arb(0)
    J = ab(Fr(J_lo))
    tot = ab(parts['rem']) * arb(300) ** 4 * t_hi ** 3
    for part in ('tail', 'ann'):
        g = L[part]
        for a, G in g['a_G']:
            if not (J * ab(a) / ab(G) > 5):
                raise WayaRefused('C-MONO-TAIL: J_lo a/G is not above 5 for a %s pair' % part)
        tot = tot + J * ab(parts[part]) * (p_lawq(g, Fr(J_lo)).upper() / p_lawq(g, Fr(300)).lower()).sqrt()
    fr = ab(L['far_rate'])
    if not (J * fr > 1):
        raise WayaRefused('C-MONO-FAR: J_lo far_rate is not above 1')
    tot = tot + J * ab(parts['far']) * (-fr * (J - 300)).exp()
    return tot.upper()


def waya_x1(e, x0, J_lo, t_hi, tb):
    """(X(t) - X(0))/t over the piece in the reader's coefficient-ball form (pk25's waya_x1): the true a_k lie in [LO_k, HI_k] (entry_ball) and
    the rest of the law is at most R(J), so X1 lies in sum_(k=1..3) [LO_k, HI_k] t^(k-1) + [-R/t, R/t] with X(0) = a_0 in [LO_0, HI_0]. x0 (an
    exact arb value, or None) must lie in [LO_0, HI_0] (C-A0). Returns (X1, [LO_0, HI_0])."""
    rec, cert, fam, key = waya_ent(e)
    LO, HI, _eb = RDR.entry_ball(rec, key)
    if len(LO) != 4 or len(HI) != 4:
        raise WayaRefused('C-A0: %s has %d coefficient balls, expected 4' % (e.name, len(LO)))
    ball = lambda k: ab(Fr(LO[k])).union(ab(Fr(HI[k])))
    if x0 is not None and not (ab(Fr(LO[0])) <= x0 and x0 <= ab(Fr(HI[0]))):
        raise WayaRefused('C-A0: P1\'s exact %s(0) is outside [LO_0, HI_0]' % e.name)
    s = arb(0)
    for k in (3, 2, 1):
        s = s * tb + ball(k)
    return s + arb(0, 1) * waya_rt(RDR.entry_law(cert, fam, key), J_lo, t_hi), ball(0)


def waya_piece(key, W0):
    """P2's row of the piece (the same jlo and jhi as LR's), its J_lo and t_hi = 1/J_lo."""
    pr = W0['rows'].get(key)
    if pr is None or pr[W0['ix']['jlo']] != LR[key][0] or pr[W0['ix']['jhi']] != LR[key][1]:
        raise WayaRefused('C-WAYA-IN: P2 has no row %s with jlo %s and jhi %s' % (key, LR[key][0], LR[key][1]))
    return pr, Fr(LR[key][0]), (1 / ab(Fr(LR[key][0]))).upper()


def waya_coefs(pr, nrm, W0, J_lo, t_hi, tb):
    """the Ritz coefficients c_kb = uhat_kb / G_bb^1/2 (amps' U[k][b] / nrm[b]) and their parts on the piece: c0[k]_b = uhat_kb(0) / G0_bb^1/2
    exact (C10; uhat_0(0) = (1, 0, 0)) for k = 0, x, y, and dc[k]_b = (c_kb - c0[k]_b)/t = du_kb/g_b - u0_kb G1_bb/(g_b g0_b (g_b + g0_b)) for
    k = 0, x, with du_kb P2's (uhat_kb - uhat_kb(0))/t, g_b = nrm[b], g0_b = G0_bb^1/2, G1_bb by waya_x1 on S9's G,b,b (C-A0). Returns (c0, dc)."""
    hv = lambda f: ab(Fr(pr[W0['ix'][f + '_lo']])).union(ab(Fr(pr[W0['ix'][f + '_hi']])))
    G1 = [waya_x1(S9G[(b, b)], W0['G0d'][i], J_lo, t_hi, tb)[0] for i, b in enumerate(ST)]
    g0 = [W0['G0d'][i].sqrt() for i in range(3)]
    u0 = {'0': [arb(1), arb(0), arb(0)], 'x': W0['ux0'], 'y': W0['uy0']}
    c0 = dict((k, [u0[k][i] / g0[i] for i in range(3)]) for k in ('0', 'x', 'y'))
    dc = dict((k, [hv('u%s%st' % (k, BV[i])) / nrm[i] - u0[k][i] * G1[i] / (nrm[i] * g0[i] * (nrm[i] + g0[i])) for i in range(3)]) for k in ('0', 'x'))
    return c0, dc


def waya_xt(ents, c0, dc, T, jlo, laws, J_lo, t_hi):
    """(X(t) - X(0))/t for X = sum_b c_kb v_b(t) at one level: sum_b dc_b v_b(t) + sum_b c0_b (v_b(t) - v_b(0))/t, and X(0)'s ball
    sum_b c0_b [LO_0, HI_0]."""
    xt, z0 = arb(0), arb(0)
    for i in range(3):
        x1, a0 = waya_x1(ents[i], None, J_lo, t_hi, T)
        xt = xt + dc[i] * ents[i].ball(T, jlo, laws) + c0[i] * x1
        z0 = z0 + c0[i] * a0
    return xt, z0


def waya_t0(ents, c, J_lo, t_hi, T):
    """X(0)'s ball sum_b c_b [LO_0, HI_0] alone (PLANT-WAYA-ZERO's level y)."""
    return sum((c[i] * waya_x1(ents[i], None, J_lo, t_hi, T)[1] for i in range(3)), arb(0))


def waya_dt(pr, W0, a, q, eps, qw, A):
    """Lemma A's error at level a over t, from P2's /t fields: qat qw + sum_(k != a) eps_kat |A_k| + (q_a qat + sum_(k != a) eps_ka eps_kat) |A_a|,
    for a vector w with |Q_W w| <= qw and Ritz amplitude balls A (levels 0, x, y), q_a and eps_ka MR_LEMMAP v3's."""
    fv = lambda f: ab(Fr(pr[W0['ix'][f]]))
    qat = fv('q%st_hi' % a)
    oth = [k for k in LV if k != a]
    et = dict((k, fv('eps_%s%st_hi' % (k, a))) for k in oth)
    qwb = qw if isinstance(qw, arb) else ab(qw)
    return (qat * qwb + sum((et[k] * ab(absup(A[k])) for k in oth), arb(0)) +
            (ab(q[a]) * qat + sum((ab(eps[(k, a)]) * et[k] for k in oth), arb(0))) * ab(absup(A[a]))).upper()


def waya_end(key, w1e, w2e, T, jlo, laws, nrm, q, eps, S, rb, Dt, qw1, qw2, A1, A2, W0):
    """Way A for an exact end, A_x = F / (Dt s_x) with F = <u_x, w1 - r* w2>, r* = <u, w1>/<u, w2> in the ball rb and Dt = <u, w2> on the piece (h-1:
    amps' r and P0; h0: r0 +- Dr and P0's interval). F(0) = X1(0) - r*(0) X2(0) = 0 (X_i = A~_x(w_i), r*(0) = N0/D0, N0 = A~_0(w1)(0), D0 = A~_0(w2)(0);
    Lemma A's errors vanish at t^0), so F/t = X1d - r* X2d - rd X2(0) +- (dx(w1) + |r*| dx(w2))/t with X_id = (X_i(t) - X_i(0))/t and
    rd = (r*(t) - r*(0))/t = (Nd D0 - N0 Dd)/(Dt D0), Nd, Dd the level-0 differences over t, each +- Lemma A's level-0 error over t. Returns the
    A_x/t ball with its parts, T0 = X1(0) D0 - N0 X2(0) (C-WAYA-T0) and T0y, the same with u_y(0) in place of u_x(0) (PLANT-WAYA-ZERO)."""
    pr, J_lo, t_hi = waya_piece(key, W0)
    c0, dc = waya_coefs(pr, nrm, W0, J_lo, t_hi, T)
    X1d, X10 = waya_xt(w1e, c0['x'], dc['x'], T, jlo, laws, J_lo, t_hi)
    X2d, X20 = waya_xt(w2e, c0['x'], dc['x'], T, jlo, laws, J_lo, t_hi)
    N1d, N0 = waya_xt(w1e, c0['0'], dc['0'], T, jlo, laws, J_lo, t_hi)
    D1d, D0 = waya_xt(w2e, c0['0'], dc['0'], T, jlo, laws, J_lo, t_hi)
    X1y0, X2y0 = waya_t0(w1e, c0['y'], J_lo, t_hi, T), waya_t0(w2e, c0['y'], J_lo, t_hi, T)
    d01, d02 = waya_dt(pr, W0, '0', q, eps, qw1, A1), waya_dt(pr, W0, '0', q, eps, qw2, A2)
    dx1, dx2 = waya_dt(pr, W0, 'x', q, eps, qw1, A1), waya_dt(pr, W0, 'x', q, eps, qw2, A2)
    rd = ((N1d + arb(0, d01)) * D0 - N0 * (D1d + arb(0, d02))) / (Dt * D0)
    Ft = X1d - rb * X2d - rd * X20 + arb(0, (dx1 + ab(absup(rb)) * dx2).upper())
    return dict(Axc=Ft / (Dt * S['x']), T0=X10 * D0 - N0 * X20, T0y=X1y0 * D0 - N0 * X2y0, Ft=Ft, rd=rd, X10=X10, X20=X20, N0=N0, D0=D0,
                err=(dx1 + ab(absup(rb)) * dx2).upper())


try:
    WAYA = waya_load()
    okw, whyw = True, 'loaded'
except WayaRefused as ex:
    WAYA, okw, whyw = None, False, str(ex)[:200]
gate('C-WAYA-IN', okw, '(P2\'s MR_LEMMAP_V3F %s, C10 %s, C13 %s, each a row of its pk25 manifest; P2 CERTIFIED, its SOURCE naming MR_LEMMAP v3 %s and C10; '
     'UHAT0 equal; C13 states C-BH0 exactly: %s)' % (WAYA_SRC['P2'][1][:8], WAYA_SRC['C10'][1][:8], WAYA_SRC['C13'][1][:8], lem_sha[:8], whyw))
try:
    waya_load(dict(WAYA_SRC, P2=(WAYA_SRC['P2'][0], '0' * 64)))
    fired = False
except WayaRefused:
    fired = True
plant('PLANT-WAYA-PIN', fired, '(a wrong pin for P2\'s record must be refused)')

# ---- mrx_cert_v1_5: C-CERT-SAME (the record items the balls use carry exactly the certified entries' ak and err) and the certified counts
ALL_ENTS = list(S9G.values())
for end in ENDS3:
    ALL_ENTS += EV[end][0] + EV[end][1] + [x for x in NE[end] if x is not None]
ALL_ENTS += H0V[0] + H0V[1]   # mrx_cert_v1_8
ALL_ENTS += PE_E2 + [S8Z]   # mrx_cert_v1_7: the Pe_hi entries with certified laws (S8's E2 and FF)


def cert_same(e, cl):
    return cl is not None and [Fr(float(a)) for a in e.it['ak']] == list(cl['ak']) and Fr(float(e.it['err'])) == cl['err']


same_bad = sorted(set(e.name for e in ALL_ENTS if e.claw is not None and not cert_same(e, e.claw)))
ncert = sorted(set(e.name for e in ALL_ENTS if e.claw is not None))
gate('C-CERT-SAME', not same_bad and len(ncert) > 0, '(%d distinct entries take a certified law; each record item has exactly the certified ak and err; '
     'failures %s)' % (len(ncert), same_bad[:4]))
plant('PLANT-CERT-SAME', not cert_same(S9G[(1, 1)], S9G[(3, 3)].claw), '(S9 G,1,1 offered G,3,3\'s certified law must fail C-CERT-SAME)')
for end in ENDS3:
    ents = EV[end][0] + EV[end][1] + [x for x in NE[end] if x is not None]
    out('CERT-COUNT N=%d %s: %d of %d entries take a certified law (%s); the S9 Gram entries: %d of 9' % (
        N, end, sum(1 for e in ents if e.claw is not None), len(ents), ', '.join(e.name for e in ents if e.claw is not None),
        sum(1 for k, e in S9G.items() if e.claw is not None)))
out('CERT-COUNT N=%d h0: %d of %d entries take a certified law (H4TH through m3_lawcert_c3h_v1_1); the S9 Gram entries: %d of 9' % (
    N, sum(1 for e in H0V[0] + H0V[1] if e.claw is not None), len(H0V[0] + H0V[1]), sum(1 for k, e in S9G.items() if e.claw is not None)))   # mrx_cert_v1_8

# ---- rho4 by the matrix-tree theorem (riglap2.logmain: main ~ tau^(-(N-1)/2) times factors that cancel in rho4)
A_F = (3 + arb(21).sqrt()) / 6
B_F = (3 * arb(5).sqrt() - arb(21).sqrt()) / 12


def strip_edges(cols, AF, BF):
    E = {}
    for j, ty in enumerate(cols):
        T, M, B = 3 * j, 3 * j + 1, 3 * j + 2
        if ty == 'vac':
            E[(T, M)] = AF
            E[(M, B)] = AF
            E[(T, B)] = BF
        else:
            E[(T, M)] = 1
            E[(M, B)] = 1
        if j < len(cols) - 1:
            for r in range(3):
                E[(3 * j + r, 3 * (j + 1) + r)] = 1
    return 3 * len(cols), E


def tau_arb(cols):
    V, E = strip_edges(cols, A_F, B_F)
    L = [[arb(0) for _ in range(V)] for _ in range(V)]
    for (u, v), c in E.items():
        c = arb(c)
        L[u][u] += c
        L[v][v] += c
        L[u][v] -= c
        L[v][u] -= c
    return arb_mat([row[:-1] for row in L[:-1]]).det()


def rho4_float(cols3):
    import numpy as np
    af, bf = (3 + math.sqrt(21)) / 6, (3 * math.sqrt(5) - math.sqrt(21)) / 12
    lg = []
    for cols in cols3:
        V, E = strip_edges(cols, af, bf)
        L = np.zeros((V, V))
        for (u, v), c in E.items():
            L[u, u] += c
            L[v, v] += c
            L[u, v] -= c
            L[v, u] -= c
        ev = np.linalg.eigvalsh(L)
        lg.append(sum(math.log(x) for x in ev[1:]) - math.log(V))
    return math.exp(-0.5 * (N - 1) * (lg[0] + lg[1] - 2 * lg[2]))


GCS4, GD, GE3 = ['free', 'int', 'int', 'free'], ['vac', 'vac'], ['vac', 'int', 'free']
ratio = tau_arb(GE3) ** 2 / (tau_arb(GCS4) * tau_arb(GD))
RHO4 = ratio * ratio.sqrt() if N == 4 else ratio
r4f = rho4_float((GCS4, GD, GE3))
gate('C-RHO4', abs(float(RHO4.mid()) - r4f) <= 1e-9 * r4f and float(RHO4.rad()) < 1e-30,
     '(arb %s against the float eigenvalue form %.15f; radius %.1e)' % (RHO4.mid().str(20), r4f, float(RHO4.rad())))
plant('PLANT-RHO4', not abs(float(RHO4.mid()) * (1 + 1e-6) - r4f) <= 1e-9 * r4f, '(rho4 times 1 + 1e-6)')
# ---- mrx_cert_v1_7: rho_E2 = main_E2^2 / (main_D main_FF) = (tau_D tau_FF / tau_E2^2)^((N-1)/2), the FF units of Pe_hi's denominator
GFF, GE2 = ['free', 'free'], ['vac', 'free']
ratio_e2 = tau_arb(GD) * tau_arb(GFF) / tau_arb(GE2) ** 2
RHO_E2 = ratio_e2 * ratio_e2.sqrt() if N == 4 else ratio_e2


def lt_float(cols):
    """log tau by the eigenvalues of the weighted Laplacian (matrix-tree: tau = prod of the nonzero eigenvalues / V), as rho4_float."""
    import numpy as np
    af, bf = (3 + math.sqrt(21)) / 6, (3 * math.sqrt(5) - math.sqrt(21)) / 12
    V, E = strip_edges(cols, af, bf)
    L = np.zeros((V, V))
    for (u, v), c in E.items():
        L[u, u] += c
        L[v, v] += c
        L[u, v] -= c
        L[v, u] -= c
    ev = np.linalg.eigvalsh(L)
    return sum(math.log(x) for x in ev[1:]) - math.log(V)


re2f = math.exp(0.5 * (N - 1) * (lt_float(GD) + lt_float(GFF) - 2 * lt_float(GE2)))
gate('C-RHO-E2', abs(float(RHO_E2.mid()) - re2f) <= 1e-9 * re2f and float(RHO_E2.rad()) < 1e-30,
     '(rho_E2 = main_E2^2/(main_D main_FF) by the matrix-tree theorem in arb %s against the float eigenvalue form %.15f; radius %.1e)' % (
         RHO_E2.mid().str(20), re2f, float(RHO_E2.rad())))
plant('PLANT-RHO-E2', not abs(float(RHO_E2.mid()) * (1 + 1e-6) - re2f) <= 1e-9 * re2f, '(rho_E2 times 1 + 1e-6)')

# ---- orientation data: the stored states' xi_TB (row 3) and xi_TM (row 1) coefficients
TSJ = json.load(open(TSF))
SM = TSJ['S']
SGN_X = 1 if SM[3][1] > 0 else -1


def lem(key, f):
    return Fr(LR[key][LEMMAP_FIELDS.index(f)])


def spe(key, f):
    return Fr(SR[key][SPECTRAL_FIELDS.index(f)])


def orient_ok(key, nrm, flip=1):
    """C-ORIENT on one piece: u~_x's xi_TB and u~_y's xi_TM coefficients from the stored states' coefficients, certainly positive."""
    cx = sum((flip * hull(lem(key, 'ux%s_lo' % b), lem(key, 'ux%s_hi' % b)) * SM[3][s] / nrm[i] for i, (b, s) in enumerate(zip(BV, ST))), arb(0))
    cy = sum((hull(lem(key, 'uy%s_lo' % b), lem(key, 'uy%s_hi' % b)) * SM[1][s] / nrm[i] for i, (b, s) in enumerate(zip(BV, ST))), arb(0))
    return lo_of(cx) > 0 and lo_of(cy) > 0, cx, cy


# ---- per piece
def piece_t(key):
    jlo, jhi = LR[key][0], LR[key][1]
    tlo = Fr(0) if jhi == 'inf' else 1 / Fr(jhi)
    thi = 1 / Fr(jlo)
    return Fr(jlo), tlo, thi, hull(tlo, thi)


# ---- mrx_cert_v1_8: the h0 row (the h end at d = 0) with G6 v1_6_2's r_W and the fixed point (see the docstring)
H0BAD, RWF, H0PL = [], [], {}


def ins(key, f):
    return Fr(IR[key + '_h'][INSERT_FIELDS.index(f)])


def rw_parts(key):
    """r_W (G6 v1_6_2 sect. 4.1) and h0's Pe_hi (G6 sect. 4.3's m = 1 form at d = 0) from MR_INSERT's h row and MR_SPECTRAL, in arb from the
    written decimals (upper ends as Fractions); appends r_W's relative difference from a float recomputation of the same decimals to RWF."""
    cxa = max(abs(spe(key, 'cxm1_lo')), abs(spe(key, 'cxm1_hi')))
    cya = max(abs(spe(key, 'cym1_lo')), abs(spe(key, 'cym1_hi')))

    def mig(f):
        lo, hi = spe(key, f + '_lo'), spe(key, f + '_hi')
        return min(abs(lo), abs(hi)) if (lo > 0 or hi < 0) else Fr(0)
    Rw, rho1, tau = ab(spe(key, 'Rw_hi')), ab(spe(key, 'rho1_hi')), ab(spe(key, 'tau_hi'))
    p2 = Rw * Rw - ab(mig('cxm1')) ** 2 - ab(mig('cym1')) ** 2
    pem1 = ab(max(hi_of(p2), Fr(0))).sqrt().upper()
    e0, pen0 = Rw * rho1, tau * pem1
    vp, C = ab(ins(key, 'vp_hi')), ab(ins(key, 'C_hi'))
    terms = [ab(ins(key, 'Pevw_hi')), ab(cxa) * ab(ins(key, 'PeBwux_hi')), ab(cya) * ab(ins(key, 'PeBwuy_hi')), ab(ins(key, 'win_hi')) * pem1,
             vp * e0 * tau * pen0]
    rW = hi_of(sum(terms, arb(0)).upper())
    rsx, rsy = ab(spe(key, 'sx_hi')).sqrt(), ab(spe(key, 'sy_hi')).sqrt()
    tail = vp * e0 * pen0
    pe1 = ab(ins(key, 'Pev_hi')) + ab(cxa) * C * rsx + ab(cya) * C * rsy + C * tau.sqrt() * pem1 + tail
    pe2 = ab(ins(key, 'Pev_hi')) + C * rsx * Rw + tail
    pe = min(hi_of(pe1.upper()), hi_of(pe2.upper()))
    fs = lambda f: float(SR[key][SPECTRAL_FIELDS.index(f)])
    fi = lambda f: float(IR[key + '_h'][INSERT_FIELDS.index(f)])

    def rwf(winf):
        mg = lambda f: min(abs(fs(f + '_lo')), abs(fs(f + '_hi'))) if (fs(f + '_lo') > 0 or fs(f + '_hi') < 0) else 0.0
        pm = math.sqrt(max(fs('Rw_hi') ** 2 - mg('cxm1') ** 2 - mg('cym1') ** 2, 0.0))
        return (fi('Pevw_hi') + max(abs(fs('cxm1_lo')), abs(fs('cxm1_hi'))) * fi('PeBwux_hi') + max(abs(fs('cym1_lo')), abs(fs('cym1_hi'))) * fi('PeBwuy_hi')
                + winf * fi('win_hi') * pm + fi('vp_hi') * fs('Rw_hi') * fs('rho1_hi') * fs('tau_hi') ** 2 * pm)
    f0 = rwf(1.0)
    RWF.append(abs(float(rW) - f0) / f0)
    if 'rw' not in H0PL:
        H0PL['rw'] = (key, float(rW), f0, rwf(2.0))
    parts = {'rW_Pevw': float(terms[0].mid()), 'rW_cxPeBx': float(terms[1].mid()), 'rW_cyPeBy': float(terms[2].mid()), 'rW_win': float(terms[3].mid()),
             'rW_tail': float(terms[4].mid()), 'pem1': float(pem1)}
    return rW, pe, parts


def h0_end(key, T, jlo, tlo, laws, nrm, U, q, eps, S):
    """the h0 row as a dict like amps' rows (Np = r_W, Pe the m = 1 form), or None with the reason in H0BAD."""
    w1 = [e.ball(T, jlo, laws) for e in H0V[0]]
    w2 = [e.ball(T, jlo, laws) for e in H0V[1]]
    A2 = dict((k, sum((U[k][i] * w2[i] / nrm[i] for i in range(3)), arb(0))) for k in LV)
    A10 = sum((U['0'][i] * w1[i] / nrm[i] for i in range(3)), arb(0))
    qq = q['0'] + spe(key, 'Rw_hi') * spe(key, 'rho1_hi') ** 2
    sq0 = q['0'] ** 2 + sum(eps[(k, '0')] ** 2 for k in ('x', 'y'))
    E2 = sum(eps[(k, '0')] * absup(A2[k]) for k in ('x', 'y')) + sq0 * absup(A2['0'])
    rW, pe, rwp = rw_parts(key)
    den = 1 - q['x'] ** 2 - q['y'] ** 2
    bad = [w for w, ok in (('q_0 qq >= 1', q['0'] * qq < 1), ('1 - q_x^2 - q_y^2 <= 0', den > 0)) if not ok]
    P0lo = (lo_of(A2['0']) - E2) / (1 + q['0'] * qq)
    if not P0lo > 0:
        bad.append('P0_lo <= 0')
    if bad:
        H0BAD.append((key, laws, bad))
        return None
    P0hi = (hi_of(A2['0']) + E2) / (1 - q['0'] * qq)
    r0 = (A10 / A2['0']).mid()
    az = [(w1[i] - r0 * w2[i]) / nrm[i] for i in range(3)]
    Az = dict((k, sum((U[k][i] * az[i] for i in range(3)), arb(0))) for k in LV)
    al = dict((k, absup(Az[k]) / P0lo) for k in LV)
    be = dict((k, absup(A2[k]) / P0lo) for k in LV)
    c0, c1 = {}, {}
    for a_ in ('x', 'y'):
        oth = [k for k in LV if k != a_]
        sqa = q[a_] ** 2 + sum(eps[(k, a_)] ** 2 for k in oth)
        c0[a_] = sum(eps[(k, a_)] * al[k] for k in oth) + sqa * al[a_]
        c1[a_] = sum(eps[(k, a_)] * be[k] for k in oth) + sqa * be[a_]
    A_ = (rW + sum(q[a_] * (al[a_] + c0[a_]) for a_ in ('x', 'y'))) / den
    B_ = sum(q[a_] * (be[a_] + c1[a_]) for a_ in ('x', 'y')) / den
    Ez = sum(eps[(k, '0')] * absup(Az[k]) for k in ('x', 'y')) + sq0 * absup(Az['0'])
    C_ = (absup(Az['0']) + Ez) / P0lo
    dd = 1 - q['0'] * qq - q['0'] * B_
    if not dd > 0:
        H0BAD.append((key, laws, ['1 - q_0 qq - q_0 B <= 0']))
        return None
    Dr = (C_ + q['0'] * A_) / dd
    X = A_ + B_ * Dr
    if not (X >= A_ + B_ * Dr and Dr >= C_ + q['0'] * X + q['0'] * qq * Dr):
        H0BAD.append((key, laws, ['the solved (X, D) fails a fixed-point inequality']))
        return None
    if 'fp' not in H0PL:
        H0PL['fp'] = (key, rW, A_, B_, Dr)
    P0b = hull(P0lo, P0hi)
    Aw = dict((a_, (Az[a_] + arb(0, ab(Dr).upper()) * A2[a_]) / P0b) for a_ in ('x', 'y'))
    bar = dict((a_, q[a_] * X + c0[a_] + c1[a_] * Dr) for a_ in ('x', 'y'))
    amp = dict((a_, (Aw[a_] + arb(0, ab(bar[a_]).upper())) / S[a_]) for a_ in ('x', 'y'))
    parts = dict(rwp, P0lo=float(P0lo), P0hi=float(P0hi), D=float(Dr), X=float(X), rW=float(rW), qq=float(qq), Az0=float(absup(Az['0'])),
                 al_x=float(al['x']), al_y=float(al['y']), be_x=float(be['x']), be_y=float(be['y']), bar_x=float(bar['x']), bar_y=float(bar['y']),
                 Aw_x=' %.6e+-%.2e' % (flo(Aw['x']), float(Aw['x'].rad())), Aw_y=' %.6e+-%.2e' % (flo(Aw['y']), float(Aw['y'].rad())), r0=float(r0),
                 pe=float(pe), err_w1=' '.join('%.2e' % float(e.err_at(jlo, laws)) for e in H0V[0]),
                 err_w2=' '.join('%.2e' % float(e.err_at(jlo, laws)) for e in H0V[1]))
    wy = None
    if laws == 'C' and key in WAYA_KEYS and WAYA is not None:   # mrx_cert_v1_10: Way A for h0 (last piece) and its control
        try:
            A1w = dict((k, sum((U[k][i] * w1[i] / nrm[i] for i in range(3)), arb(0))) for k in LV)
            wy = waya_end(key, H0V[0], H0V[1], T, jlo, laws, nrm, q, eps, S, r0 + arb(0, ab(Dr).upper()), P0b,
                          P0hi * (X + (absup(r0) + Dr) * qq), P0hi * qq, A1w, A2, WAYA)
        except WayaRefused as ex:
            WAYA_BAD.append((key, 'h0', str(ex)[:160]))
    d0 = {'Ay': amp['y'], 'Ax': amp['x'], 'Np': rW, 'Axc': (amp['x'] / T) if tlo > 0 else (wy['Axc'] if wy is not None else None), 'P0': P0b,
          'qw1': float('nan'), 'qw2': float(qq), 'qwsa': float(X), 'parts': parts, 'Pe': pe, 'pe_float': float(pe), 'X': X, 'Dr': Dr, 'waya': wy}
    if laws == 'C' and key in WAYA_KEYS:
        WAYA_LOG[(key, 'h0')] = d0
    return d0


def amps(key, laws, orient_flip=1):
    jlo, tlo, thi, T = piece_t(key)
    G = arb_mat([[S9G[(a, b)].ball(T, jlo, laws) for b in ST] for a in ST])
    Gi = G.inv()
    nrm = [G[i, i].sqrt() for i in range(3)]
    U = dict((k, [hull(lem(key, 'u%s%s_lo' % (k, b)), lem(key, 'u%s%s_hi' % (k, b))) * (orient_flip if k == 'x' else 1) for b in BV]) for k in LV)
    q = dict((k, lem(key, 'q%s_hi' % k)) for k in LV)
    eps = dict(((k, a), lem(key, 'eps_%s%s_hi' % (k, a))) for k in LV for a in LV if k != a)
    L = dict((k, lem(key, 'L%s_hi' % k)) for k in LV)
    tau4 = lem(key, 'tau_hi')
    S = {'x': hull(spe(key, 'sx_lo'), spe(key, 'sx_hi')), 'y': hull(spe(key, 'sy_lo'), spe(key, 'sy_hi'))}
    res = {}
    for end in ENDS3:
        v1e, v2e = EV[end][0], EV[end][1]
        e11, e11b, e12, e22 = NE[end]
        v1 = [e.ball(T, jlo, laws) for e in v1e]
        v2 = [e.ball(T, jlo, laws) for e in v2e]
        n11 = e11.ball(T, jlo, laws) if e11b is None else (e11.ball(T, jlo, laws) + e11b.ball(T, jlo, laws)) / 2
        n12, n22 = e12.ball(T, jlo, laws), e22.ball(T, jlo, laws)

        def quad(x, y):
            return sum((x[i] * Gi[i, j] * y[j] for i in range(3) for j in range(3)), arb(0))
        a1 = [v1[i] / nrm[i] for i in range(3)]
        a2 = [v2[i] / nrm[i] for i in range(3)]
        c0 = RHO4 * n11 - quad(v1, v1)
        c2 = RHO4 * n22 - quad(v2, v2)
        qw1 = ab(max(hi_of(c0), Fr(0))).sqrt().upper()
        qw2 = ab(max(hi_of(c2), Fr(0))).sqrt().upper()
        A1 = dict((k, sum((U[k][i] * a1[i] for i in range(3)), arb(0))) for k in LV)
        A2 = dict((k, sum((U[k][i] * a2[i] for i in range(3)), arb(0))) for k in LV)

        def dlt(a, qw, A):
            """Lemma A's bound at level a for a vector with Ritz amplitudes A and |Q_W w| <= qw."""
            d = (ab(q[a]) * qw + sum((ab(eps[(k, a)]) * ab(absup(A[k])) for k in LV if k != a), arb(0))
                 + (ab(q[a]) ** 2 + sum((ab(eps[(k, a)]) ** 2 for k in LV if k != a), arb(0))) * ab(absup(A[a])))
            return d.upper()
        u0p = U['0'][0]
        if not lo_of(u0p) > 0:
            raise ValueError('%s: uhat_0p not certainly positive' % key)
        rho = [U['0'][1] / u0p, U['0'][2] / u0p]
        B1 = a1[0] + rho[0] * a1[1] + rho[1] * a1[2]
        B2 = a2[0] + rho[0] * a2[1] + rho[1] * a2[2]
        d01, d02 = dlt('0', qw1, A1), dlt('0', qw2, A2)
        r = (B1 + arb(0, (d01 / ab(lo_of(u0p))).upper())) / (B2 + arb(0, (d02 / ab(lo_of(u0p))).upper()))
        P0 = A2['0'] + arb(0, d02)
        vd = [v1[i] - r * v2[i] for i in range(3)]
        ad = [vd[i] / nrm[i] for i in range(3)]
        r0 = r.mid()
        rr = r.rad()
        d0 = [v1[i] - r0 * v2[i] for i in range(3)]
        R0 = RHO4 * (n11 - 2 * r0 * n12 + r0 * r0 * n22) - quad(d0, d0)
        slope = RHO4 * (n12 - r0 * n22) - quad(v2, d0)
        qd2 = R0 + arb(0, (2 * rr * ab(absup(slope)) + rr * rr * ab(absup(c2))).upper())
        qwd = ab(max(hi_of(qd2), Fr(0))).sqrt().upper()
        Ad = dict((k, sum((U[k][i] * ad[i] for i in range(3)), arb(0))) for k in LV)
        dd = dict((a, dlt(a, qwd, Ad)) for a in ('x', 'y'))
        Ahat = dict((a, (Ad[a] + arb(0, dd[a])) / P0) for a in ('x', 'y'))
        if end == 'a0':
            amp = Ahat
        else:
            amp = dict((a, Ahat[a] / S[a]) for a in ('x', 'y'))
        p0mig = min(abs(lo_of(P0)), abs(hi_of(P0))) if (lo_of(P0) > 0 or hi_of(P0) < 0) else Fr(0)
        if p0mig == 0:
            raise ValueError('%s %s: <u_0, w2> not bounded away from 0' % (key, end))
        qwsa = qwd / ab(p0mig).lower()
        lp = qwsa + sum((ab(absup(Ad[k])) / ab(p0mig).lower() * ab(L[k]) for k in LV), arb(0))
        Np = lp * ab(tau4) if end == 'a0' else lp
        if end == 'h-1':
            axc = amp['x'] / T if tlo > 0 else None
        else:
            axc = amp['x']
        parts = {'Ad_x_rad': float(Ad['x'].rad()), 'Ad_y_rad': float(Ad['y'].rad()), 'dx': float(dd['x']), 'dy': float(dd['y']),
                 'qx_qwd': float(q['x'] * hi_of(qwd)), 'qy_qwd': float(q['y'] * hi_of(qwd)), 'r_rad': float(r.rad()), 'P0': flo(P0),
                 'Ad_x_mid': flo(Ad['x']), 'Ad_0': float(absup(Ad['0'])), 'Ad_y': float(absup(Ad['y'])), 'qwd': float(qwd), 'qx': float(q['x']),
                 'eps_0x': float(eps[('0', 'x')]), 'eps_yx': float(eps[('y', 'x')]),
                 'ux_rad': ' '.join('%.2e' % float(U['x'][i].rad()) for i in range(3)), 'ad': ' '.join('%.3e+-%.1e' % (flo(ad[i]), float(ad[i].rad())) for i in range(3)),
                 'err_v1': ' '.join('%.2e' % float(e.err_at(jlo, laws)) for e in v1e),
                 'err_v2': ' '.join('%.2e' % float(e.err_at(jlo, laws)) for e in v2e),
                 'err_n': ' '.join('%.2e' % float(e.err_at(jlo, laws)) for e in (e11, e12, e22)),
                 'err_G33': '%.2e' % float(S9G[(3, 3)].err_at(jlo, laws))}
        res[end] = {'Ay': amp['y'], 'Ax': amp['x'], 'Np': hi_of(Np.upper()), 'Axc': axc, 'c0': c0, 'c2': c2, 'q2': qd2, 'P0': P0,
                    'qw1': qw1, 'qw2': qw2, 'qwsa': qwsa, 'parts': parts, 'r': r, 'lp': lp}   # mrx_cert_v1_7: r and Lemma P's bound kept
        if end == 'h-1' and laws == 'C' and key in WAYA_KEYS and WAYA is not None:   # mrx_cert_v1_10: Way A (last piece) and its control
            try:
                res[end]['waya'] = waya_end(key, v1e, v2e, T, jlo, laws, nrm, q, eps, S, r, P0, qw1, qw2, A1, A2, WAYA)
            except WayaRefused as ex:
                WAYA_BAD.append((key, end, str(ex)[:160]))
                res[end]['waya'] = None
            WAYA_LOG[(key, end)] = res[end]
            if tlo == 0 and res[end]['waya'] is not None:
                res[end]['Axc'] = res[end]['waya']['Axc']
    res['h0'] = h0_end(key, T, jlo, tlo, laws, nrm, U, q, eps, S)   # mrx_cert_v1_8
    # mrx_cert_v1_7: Pe_hi >= |P_e a| (h-1, t-1: |a| by the free end; a0: Lemma P on a)
    e2 = [e.ball(T, jlo, laws) for e in PE_E2]
    zb = PE_Z.ball(T, jlo, laws)
    At = dict((k, sum((U[k][i] * e2[i] / nrm[i] for i in range(3)), arb(0))) for k in LV)
    qe = sum((e2[i] * Gi[i, j] * e2[j] for i in range(3) for j in range(3)), arb(0))
    qwx = ab(max(hi_of(zb - RHO_E2 * qe), Fr(0))).sqrt().upper()
    srho = RHO_E2.sqrt()
    d0x = (ab(q['0']) * qwx + srho * (sum((ab(eps[(k, '0')]) * ab(absup(At[k])) for k in LV if k != '0'), arb(0))
                                      + (ab(q['0']) ** 2 + sum((ab(eps[(k, '0')]) ** 2 for k in LV if k != '0'), arb(0))) * ab(absup(At['0'])))).upper()
    m0 = srho * At['0']
    mlo = (lo_of(m0) - hi_of(d0x)) if lo_of(m0) > 0 else Fr(0)
    for end in ('h-1', 't-1'):
        b1, b2 = PE_W[end][0].ball(T, jlo, laws), PE_W[end][1].ball(T, jlo, laws)
        rb = res[end]['r']
        r0_, rr_ = rb.mid(), rb.rad()
        R0 = b2 - 2 * r0_ * b1 + r0_ * r0_ * zb
        Rhi = hi_of((R0 + arb(0, (2 * rr_ * ab(absup(b1 - r0_ * zb)) + rr_ * rr_ * ab(absup(zb))).upper())).upper())
        res[end]['Pe'] = hi_of((ab(max(Rhi, Fr(0))).sqrt() / ab(mlo)).upper()) if mlo > 0 else None
        nf = flo(b2) - 2 * flo(rb) * flo(b1) + flo(rb) ** 2 * flo(zb)
        res[end]['pe_float'] = math.sqrt(max(nf, 0.0)) / flo(m0) if flo(m0) > 0 else float('nan')
        res[end]['pe_parts'] = {'R_hi': float(Rhi), 'den_lo': float(mlo), 'A0': flo(m0), 'delta0': float(hi_of(d0x)), 'QWx': float(hi_of(qwx))}
    res['a0']['Pe'] = res['a0']['lp'] if isinstance(res['a0']['lp'], Fr) else hi_of(res['a0']['lp'].upper())
    res['a0']['pe_float'] = float(res['a0']['Pe'])
    return res, nrm, (jlo, tlo, thi)


def flo(x):
    return float(x.mid())


def pfmt(dp):
    return ', '.join('%s %s' % (k, ('%.3e' % v) if isinstance(v, float) else v) for k, v in sorted(dp.items()))


def x_cols(key, end, d):
    """mrx_cert_v1_6: (Ax_lo, Ax_hi, Axc_lo, Axc_hi, Axf_hi) as written, in G6 v1_6_2's form (sect. 6; engine v1_8_4's G-FACTX and G-FLOOR).
    t-1 and a0 (power 0): Axc = Ax, the same strings, Axf 0. h-1 (power 1) on a piece with t_lo > 0: Axc = Ax/T rounded outward and Ax written
    as the hull of t Axc at the piece's ends t = 1/jlo, 1/jhi (exact rationals of the written strings) rounded outward: every A_x(t) of the
    piece lies in t (Ax/T), inside the hull, and t Axc stays inside it. h-1 on the last piece (Way B, the row 4325): Axc 0 0, Axf =
    max(|lo Ax|, |hi Ax|) rounded up, Ax written [-Axf, Axf]. In each case Axc_lo t - Axf <= A_x <= Axc_hi t + Axf on the piece."""
    if end not in ('h-1', 'h0'):   # mrx_cert_v1_8: h0 has power 1, as h-1
        a_lo, a_hi = dec(lo_of(d['Ax']), False), dec(hi_of(d['Ax']), True)
        return a_lo, a_hi, a_lo, a_hi, '0'
    jlo_s, jhi_s = LR[key][0], LR[key][1]
    if jhi_s == 'inf' and d.get('waya') is not None:   # mrx_cert_v1_10: Way A, Axf 0, Ax the hull of the direct ball, 0 and t_1 Axc
        c_lo, c_hi = dec(lo_of(d['waya']['Axc']), False), dec(hi_of(d['waya']['Axc']), True)
        t1 = 1 / Fr(jlo_s)
        return (dec(min(lo_of(d['Ax']), Fr(0), t1 * Fr(c_lo)), False), dec(max(hi_of(d['Ax']), Fr(0), t1 * Fr(c_hi)), True), c_lo, c_hi, '0')
    if jhi_s == 'inf':
        f = dec(max(abs(lo_of(d['Ax'])), abs(hi_of(d['Ax']))), True)
        return ('-' + f) if f != '0' else '0', f, '0', '0', f
    c_lo, c_hi = dec(lo_of(d['Axc']), False), dec(hi_of(d['Axc']), True)
    ts = (1 / Fr(jlo_s), 1 / Fr(jhi_s))
    return dec(min(t * Fr(c_lo) for t in ts), False), dec(max(t * Fr(c_hi) for t in ts), True), c_lo, c_hi, '0'


# ---- run both error variants
fin_bad, qw_bad, orient_bad, orient_plant = [], [], [], 0
pe_bad = []   # mrx_cert_v1_7
bulk_bad, bulk_n = [], 0   # mrx_cert_v1_8: C-BULKSIGN
rows = {'U': [], 'C': []}
signs = {'U': {}, 'C': {}}
first = {}
for V, laws in (('U', False), ('C', 'C')):
    for key in keysN:
        res, nrm, (jlo, tlo, thi) = amps(key, laws)
        if V == 'U':
            ok, cx, cy = orient_ok(key, nrm)
            if not ok:
                orient_bad.append(key)
            okp, _, _ = orient_ok(key, nrm, flip=-1)
            orient_plant += 0 if okp else 1
        for end in ENDS:
            d = res[end]
            if d is None:   # mrx_cert_v1_8: an h0 row that C-H0-FP refused
                fin_bad.append((V, key, end))
                continue
            vals = [d['Ay'], d['Ax']] + ([d['Axc']] if d['Axc'] is not None else [])
            if not all(x.is_finite() for x in vals):
                fin_bad.append((V, key, end))
                continue
            if end != 'h0' and (hi_of(d['c0']) < 0 or hi_of(d['c2']) < 0):   # mrx_cert_v1_8: h0 has no norm entry
                qw_bad.append((V, key, end))
            xl = x_cols(key, end, d)   # mrx_cert_v1_6: G6 v1_6_2's x columns
            xi = IR['%s_%s' % (key, {'h-1': 'h', 'h0': 'h', 't-1': 't', 'a0': 'a'}[end])]   # mrx_cert_v1_8: the engine's C-ORIENT anchor
            se = 1 if Fr(xl[2]) > 0 else (-1 if Fr(xl[3]) < 0 else 0)
            si = 1 if Fr(xi[INSERT_FIELDS.index('xc_lo')]) > 0 else (-1 if Fr(xi[INSERT_FIELDS.index('xc_hi')]) < 0 else 0)
            bulk_n += 1
            if se and si and se != si:
                bulk_bad.append((V, key, end))
            if d['Pe'] is None:   # mrx_cert_v1_7: C-PE
                pe_bad.append((V, key, end))
            line = '%s_%s = %s %s %s %s %s %s %s %s %s %s %s %s' % (key, end, LR[key][0], LR[key][1], dec(lo_of(d['Ay']), False), dec(hi_of(d['Ay']), True),
                                                                    xl[0], xl[1], dec(d['Np'], True), repr(flo(d['Ay'])), xl[2], xl[3], xl[4],
                                                                    dec(d['Pe'], True) if d['Pe'] is not None else 'nan')
            rows[V].append((line, d))
            signs[V].setdefault(end, []).append((float(jlo), Fr(xl[0]) > 0, Fr(xl[1]) < 0))
            if key == keysN[0]:
                first[(V, end)] = d
            if end == 'h-1' and (V, 'open') not in first and not (Fr(xl[0]) > 0 or Fr(xl[1]) < 0):
                first[(V, 'open')] = (key, d)
            if end == 'h0' and (V, 'open0') not in first and not (Fr(xl[0]) > 0 or Fr(xl[1]) < 0):   # mrx_cert_v1_8
                first[(V, 'open0')] = (key, d)
gate('C-FINITE', not fin_bad, '(every Ay, Ax and Axc ball finite on every piece and end; failures %d, first %s)' % (len(fin_bad), fin_bad[:3]))
gate('C-QW', not qw_bad, '(c0 = |Q_W w1|^2 and c2 = |Q_W w2|^2 not certainly negative; failures %d, first %s)' % (len(qw_bad), qw_bad[:3]))
gate('C-ORIENT', not orient_bad, '(on all %d pieces: the xi_TB coefficient of u~_x and the xi_TM coefficient of u~_y certainly positive; failures %s)' % (
    len(keysN), orient_bad[:3]))
plant('PLANT-ORIENT', orient_plant == len(keysN), '(u~_x negated: C-ORIENT fails on %d of %d pieces)' % (orient_plant, len(keysN)))
# ---- mrx_cert_v1_8: the h0 gates and the bulk-sign anchor
gate('C-H0-FP', not H0BAD and 'fp' in H0PL, '(h0 on every piece in both variants: q_0 qq < 1, 1 - q_x^2 - q_y^2 > 0, P0_lo > 0, 1 - q_0 qq - q_0 B > 0, '
     'and the solved (X, D) re-checked exactly against both inequalities; failures %d, first %s)' % (len(H0BAD), H0BAD[:2]))
if 'fp' in H0PL:
    kf, rWf, Af, Bf, Df = H0PL['fp']
    plant('PLANT-H0-FP', not (rWf >= Af + Bf * Df), '(%s: X = r_W alone, %.6e, without the reverse term must fail the re-check X >= A + B D = %.6e)' % (
        kf, float(rWf), float(Af + Bf * Df)))
gate('C-RW-FLOAT', bool(RWF) and max(RWF) <= 1e-12, '(r_W in arb against a float recomputation from the same decimals, every piece and variant: '
     'largest relative difference %.2e over %d evaluations)' % (max(RWF) if RWF else float('nan'), len(RWF)))
if 'rw' in H0PL:
    kr, ra, f0r, f2r = H0PL['rw']
    plant('PLANT-RW', not abs(ra - f2r) / f2r <= 1e-12, '(%s: the float r_W with win_hi doubled, %.6e, against the arb value %.6e must leave the band)' % (
        kr, f2r, ra))
gate('C-BULKSIGN', not bulk_bad and bulk_n > 0, '(engine v1_8_4\'s C-ORIENT anchor on all %d written rows: the exact end\'s Axc sign against MR_INSERT\'s '
     'xc sign of its bulk (h for h-1 and h0, t for t-1, a for a0) where both are strict; failures %d, first %s)' % (bulk_n, len(bulk_bad), bulk_bad[:3]))

# ---- C-ROUND on every written number, with its plant
bad_round = 0
for V in rows:
    for line, d in rows[V]:
        f = line.split(' = ')[1].split()
        ok_r = (Fr(f[2]) <= lo_of(d['Ay']) and Fr(f[3]) >= hi_of(d['Ay']) and Fr(f[4]) <= lo_of(d['Ax']) and Fr(f[5]) >= hi_of(d['Ax'])
                and Fr(f[6]) >= d['Np'] and (d['Pe'] is None or Fr(f[11]) >= d['Pe']))   # mrx_cert_v1_7: Pe_hi too
        if d['Axc'] is not None and line.split(' = ')[0].endswith(('_h-1', '_h0')):   # mrx_cert_v1_6 (v1_8: h0 too): Axc against the Ax/T ball
            ok_r = ok_r and Fr(f[8]) <= lo_of(d['Axc']) and Fr(f[9]) >= hi_of(d['Axc'])
        if not ok_r:
            bad_round += 1
gate('C-ROUND', bad_round == 0, '(every written Ay_lo, Ax_lo and h-1 Axc_lo off the last piece <= the exact lower ends; Ay_hi, Ax_hi, Axc_hi, Np_hi '
     '>= the upper ends; failures %d)' % bad_round)

# ---- mrx_cert_v1_10: the Way A gates (variant C)
gate('C-WAYA-RUN', WAYA is not None and not WAYA_BAD, '(Way A on %s and %s for h-1 and h0: no refusal (C-WAYA-IN at use, C-A0, C-MONO-TAIL, C-MONO-FAR); '
     'failures %s)' % (keysN[-1], keysN[-2], WAYA_BAD[:3]))
t0_lines, t0_ok = [], WAYA is not None and not WAYA_BAD
for end in ('h-1', 'h0'):
    dW = WAYA_LOG.get((keysN[-1], end), {}).get('waya')
    if dW is None:
        t0_ok = False
        continue
    t0_ok = t0_ok and dW['T0'].overlaps(arb(0))
    t0_lines.append('%s: T0 %s (X1(0) %s, X2(0) %s, N0 %s, D0 %s)' % (end, dW['T0'].str(6, radius=True), dW['X10'].str(6, radius=True),
                                                                  dW['X20'].str(6, radius=True), dW['N0'].str(6, radius=True), dW['D0'].str(6, radius=True)))
gate('C-WAYA-T0', t0_ok, '(T0 = X1(0) D0 - N0 X2(0) holds 0 for both ends; F(0) = 0 exactly by C13\'s C-GAMMA and C-BH0 with P1\'s C-SPAN: %s)' % (
    '; '.join(t0_lines)))
dZ = WAYA_LOG.get((keysN[-1], 'h-1'), {}).get('waya')
plant('PLANT-WAYA-ZERO', dZ is not None and not dZ['T0y'].overlaps(arb(0)), '(u_y(0) in place of u_x(0) in h-1\'s T0: %s must leave 0)' % (
    dZ['T0y'].str(6, radius=True) if dZ is not None else 'not computed'))
ct_lines, ct_ok = [], WAYA is not None and not WAYA_BAD
for end in ('h-1', 'h0'):
    dC = WAYA_LOG.get((keysN[-2], end))
    if dC is None or dC.get('waya') is None or dC.get('Axc') is None:
        ct_ok = False
        continue
    ok1 = dC['waya']['Axc'].overlaps(dC['Axc'])
    ct_ok = ct_ok and ok1
    ct_lines.append('%s: Way A %s, direct Ax/T %s%s' % (end, dC['waya']['Axc'].str(8, radius=True), dC['Axc'].str(8, radius=True), '' if ok1 else ' (NO OVERLAP)'))
gate('C-WAYA-CONT', ct_ok, '(the control on %s [%s, %s], a piece with t_lo > 0: Way A\'s A_x/t overlaps v1_9\'s direct Ax/T (P2\'s /t fields are '
     'crude there, X_hi jhi): %s)' % (keysN[-2], LR[keysN[-2]][0], LR[keysN[-2]][1], '; '.join(ct_lines)))
jn_lines, jn_ok = [], WAYA is not None and not WAYA_BAD
for end in ('h-1', 'h0'):
    dL, dC = WAYA_LOG.get((keysN[-1], end)), WAYA_LOG.get((keysN[-2], end))
    if dL is None or dL.get('waya') is None or dC is None or dC.get('Axc') is None:
        jn_ok = False
        continue
    ok1 = dL['waya']['Axc'].overlaps(dC['Axc'])
    jn_ok = jn_ok and ok1
    jn_lines.append('%s: last piece Way A [%.6f, %.6f], the piece before, direct Ax/T [%.6f, %.6f]%s' % (
        end, float(lo_of(dL['waya']['Axc'])), float(hi_of(dL['waya']['Axc'])), float(lo_of(dC['Axc'])), float(hi_of(dC['Axc'])), '' if ok1 else ' (NO OVERLAP)'))
gate('C-WAYA-JOIN', jn_ok, '(A_x/t is continuous at J = %s: the last piece\'s Way A Axc overlaps the direct Ax/T of the piece before it: %s)' % (
    LR[keysN[-1]][0], '; '.join(jn_lines)))
wl_lines, wl_ok = [], True
for ln, d in rows['C']:
    k_, e_ = ln.split(' = ')[0].rsplit('_', 1)
    if k_ == keysN[-1] and e_ in ('h-1', 'h0'):
        f = ln.split(' = ')[1].split()
        okr = f[10] == '0' and d.get('waya') is not None and d['waya']['Axc'].is_finite()
        wl_ok = wl_ok and okr
        sg = 'positive' if Fr(f[8]) > 0 else ('negative' if Fr(f[9]) < 0 else 'open')
        wl_lines.append('%s: Axc [%s, %s] (%s), Axf %s, Ax [%s, %s]' % (e_, f[8], f[9], sg, f[10], f[4], f[5]))
gate('C-WAYA', wl_ok and len(wl_lines) == 2, '(the last piece %s of variant C: h-1 and h0 rows with Axf 0 and a finite Way A Axc: %s)' % (
    keysN[-1], '; '.join(wl_lines)))


def factx_bad(line):
    """mrx_cert_v1_6: engine v1_8_4's G-FLOOR and G-FACTX on one written row, exactly (no slack). Power 1 (h-1): at t = 1/jlo and at t = 1/jhi
    (0 on the last piece) t Axc_lo - Axf >= Ax_lo and t Axc_hi + Axf <= Ax_hi; a floor only on the last piece of h-1. Power 0: Axc = Ax as
    strings and Axf 0. Returns the reason, or None."""
    k, f = line.split(' = ')[0], line.split(' = ')[1].split()
    lo, hi, clo, chi, ff = (Fr(x) for x in (f[4], f[5], f[8], f[9], f[10]))
    if ff < 0 or (ff > 0 and (f[1] != 'inf' or not k.endswith(('_h-1', '_h0')))):   # mrx_cert_v1_8: h0 as h-1
        return 'floor %s off the last h-1 piece' % f[10]
    if not k.endswith(('_h-1', '_h0')):
        return None if (f[8], f[9], f[10]) == (f[4], f[5], '0') else 'power-0 coefficient differs from the amplitude'
    ts = [1 / Fr(f[0])] + ([Fr(0)] if f[1] == 'inf' else [1 / Fr(f[1])])
    return None if all(t * clo - ff >= lo and t * chi + ff <= hi for t in ts) else 't Axc with the floor leaves the amplitude'


fx = [(ln.split(' = ')[0], factx_bad(ln)) for V in rows for ln, d in rows[V]]
fx_bad = [x for x in fx if x[1]]
nfloor = sum(1 for V in rows for ln, d in rows[V] if Fr(ln.split(' = ')[1].split()[10]) > 0)
gate('C-FACTX', not fx_bad, '(engine v1_8_4\'s G-FACTX and G-FLOOR on all %d written rows, exactly: t Axc -+ Axf inside the amplitude at both '
     'ends of each h-1 and h0 piece, Axc = Ax and Axf 0 for t-1 and a0; %d rows with a Way B floor, each on the last piece of h-1 or h0; failures %s)' % (
         len(fx), nfloor, fx_bad[:3]))
lh_ = [ln for ln, d in rows['U'] if ln.split(' = ')[0].endswith('_h-1') and ln.split(' = ')[1].split()[1] != 'inf'][0]
fh_ = lh_.split(' = ')[1].split()
fh_[9] = dec(2 * Fr(fh_[9]), True)
plant('PLANT-FACTX', factx_bad(lh_.split(' = ')[0] + ' = ' + ' '.join(fh_)) is not None, '(%s with Axc_hi doubled must fail C-FACTX)' % lh_.split(' = ')[0])
lnp, dp = rows['U'][0]
q_lo = lo_of(dp['Ay'])
wrong = Fr(dec(q_lo, False)) + abs(q_lo) * Fr(1, 10 ** 15)
plant('PLANT-ROUND', not (wrong <= q_lo), '(Ay_lo of %s written one part in 1e15 above its rounded-down value: %.17e against %.17e)' % (
    lnp.split(' = ')[0], float(wrong), float(q_lo)))

# ---- mrx_cert_v1_7: C-PE, C-PE-FLOAT and C-Z0
gate('C-PE', not pe_bad, '(Pe_hi finite on every row: the Lemma A denominator rho_E2^1/2 lo A~_0 - delta_0 positive on every piece; failures %d, first %s)' % (
    len(pe_bad), pe_bad[:3]))
pf_lines, pf_ok, pf_plant = [], True, True
for V in ('U', 'C'):
    d0_ = first[(V, 'h-1')]
    pe_, pf_ = d0_['Pe'], d0_['pe_float']
    okv = pe_ is not None and pf_ == pf_ and pf_ > 0 and Fr(pf_) <= pe_ <= 3 * Fr(pf_)
    pf_ok = pf_ok and okv
    pf_plant = pf_plant and not (pe_ is not None and pf_ > 0 and Fr(4 * pf_) <= pe_ <= 3 * Fr(4 * pf_))
    pf_lines.append('%s: Pe_hi %.6e, float |a| %.6e (ratio %.4f)' % (V, float(pe_) if pe_ is not None else float('nan'), pf_, (float(pe_) / pf_) if (pe_ is not None and pf_ > 0) else float('nan')))
gate('C-PE-FLOAT', pf_ok, '(h-1 at %s, the J_low piece: Pe_hi in [1, 3] times the float |a| from midpoints: %s)' % (keysN[0], '; '.join(pf_lines)))
plant('PLANT-PE-FLOAT', pf_plant, '(4 times the float |a| must leave the [1, 3] band)')
dz = max(abs(float(a.mid()) - float(b.mid())) / max(1.0, abs(float(b.mid()))) for a, b in zip(PE_Z.ak, S8Z.ak))
gate('C-Z0', dz <= 1e-12, '(runner c3n_1\'s Z0 a_k against S8\'s FF z (the same integral): largest relative difference %.2e)' % dz)
zp = [b * (1 + 1e-9) if i == 1 else b for i, b in enumerate(S8Z.ak)]
dzp = max(abs(float(a.mid()) - float(b.mid())) / max(1.0, abs(float(b.mid()))) for a, b in zip(PE_Z.ak, zp))
plant('PLANT-Z0', not dzp <= 1e-12, '(S8\'s z with a_1 times 1 + 1e-9: relative difference %.2e)' % dzp)

# ---- C-FLOAT against the float tools at the J_low piece (x flipped by sign(S[3][1]))
ftxt, atxt = open(MRXERR[0]).read(), open(MRXA0[0]).read()
gate('C-FLOAT-SRC', sha(MRXERR[0]).startswith(MRXERR[1]) and sha(MRXA0[0]).startswith(MRXA0[1]), '(%s %s, %s %s)' % (
    os.path.basename(MRXERR[0]), sha(MRXERR[0])[:8], os.path.basename(MRXA0[0]), sha(MRXA0[0])[:8]))
JL = {4: 350, 3: 300}[N]
fl = {}
for end in ('h-1', 'h0', 't-1'):   # mrx_cert_v1_8: + h0
    m = re.search(r'^END N=%d J=%d %s: .*?engine a_x = A_x/s_x ([-+0-9.eE]+) a_y = A_y/s_y ([-+0-9.eE]+)' % (N, JL, end), ftxt, re.M)
    fl[end] = (SGN_X * float(m.group(1)), float(m.group(2)))
m = re.search(r'^A0 EVEN N=%d J=%d: A_x ([-+0-9.eE]+) A_y ([-+0-9.eE]+)' % (N, JL), atxt, re.M)
fl['a0'] = (SGN_X * float(m.group(1)), float(m.group(2)))
jkey = [k for k in keysN if Fr(LR[k][0]) <= JL and (LR[k][1] == 'inf' or JL <= Fr(LR[k][1]))][0]
resJ, _, _ = amps(jkey, False)
okf, lines = True, []
for end in ENDS:
    ax, ay = fl[end]
    d = resJ[end]
    inx = float(lo_of(d['Ax'])) <= ax <= float(hi_of(d['Ax']))
    iny = float(lo_of(d['Ay'])) <= ay <= float(hi_of(d['Ay']))
    okf = okf and inx and iny
    lines.append('%s: a_x %.6e in [%.6e, %.6e] %s, a_y %.6f in [%.6f, %.6f] %s' % (end, ax, float(lo_of(d['Ax'])), float(hi_of(d['Ax'])), inx, ay,
                                                                                   float(lo_of(d['Ay'])), float(hi_of(d['Ay'])), iny))
gate('C-FLOAT', okf, '(piece %s [%s, %s] holds J = %d; %s)' % (jkey, LR[jkey][0], LR[jkey][1], JL, '; '.join(lines)))
d = resJ['h-1']
hw = float(hi_of(d['Ay']) - lo_of(d['Ay'])) / 2
plant('PLANT-FLOAT', not (float(lo_of(d['Ay'])) <= fl['h-1'][1] + 10 * hw <= float(hi_of(d['Ay']))), '(h-1 a_y moved by ten half-widths)')

# ---- summaries
for V in ('U', 'C'):
    for end in ENDS:
        d = first[(V, end)]
        out('JLOW %s N=%d %s %s: Ay [%.9f, %.9f] (half-width/|mid| %.3e); Ax [%+.6e, %+.6e] (half-width/|mid| %.3e); Np_hi %.4e; |Q_W w1| %.3e |Q_W w2| %.3e '
            '|Q_W S a| %.3e' % (V, N, keysN[0], end, float(lo_of(d['Ay'])), float(hi_of(d['Ay'])), float(d['Ay'].rad()) / abs(flo(d['Ay'])),
                                float(lo_of(d['Ax'])), float(hi_of(d['Ax'])), float(d['Ax'].rad()) / max(abs(flo(d['Ax'])), 1e-300), float(d['Np']),
                                float(d['qw1']), float(d['qw2']), float(d['qwsa'])))
        out('PARTS %s N=%d %s %s: %s' % (V, N, keysN[0], end, pfmt(d['parts'])))
    if (V, 'open') in first:
        ko, do = first[(V, 'open')]
        out('PARTS-OPEN %s N=%d %s [%s, %s] h-1 (the first piece where Ax\'s sign is open): Ax [%+.4e, %+.4e]; %s' % (
            V, N, ko, LR[ko][0], LR[ko][1], float(lo_of(do['Ax'])), float(hi_of(do['Ax'])), pfmt(do['parts'])))
    if (V, 'open0') in first:   # mrx_cert_v1_8
        ko, do = first[(V, 'open0')]
        out('PARTS-OPEN %s N=%d %s [%s, %s] h0 (the first piece where Ax\'s sign is open): Ax [%+.4e, %+.4e]; %s' % (
            V, N, ko, LR[ko][0], LR[ko][1], float(lo_of(do['Ax'])), float(hi_of(do['Ax'])), pfmt(do['parts'])))
    for end in ENDS:
        sg = signs[V][end]
        pos = [j for j, p, n_ in sg if p]
        lost = [j for j, p, n_ in sg if not p and not n_]
        neg = [j for j, p, n_ in sg if n_]
        out('XSIGN %s N=%d %s: Ax certainly positive on %d pieces, negative on %d, open on %d; the first open piece starts at J = %s; the last positive '
            'piece starts at J = %s' % (V, N, end, len(pos), len(neg), len(lost), ('%.6g' % min(lost)) if lost else 'none', ('%.6g' % max(pos)) if pos else 'none'))
    for end in ENDS:   # mrx_cert_v1_7: Pe_hi
        pes = [(float(d['Pe']), ln.split(' = ')[0]) for ln, d in rows[V] if ln.split(' = ')[0].endswith('_' + end) and d['Pe'] is not None]
        if pes:
            d0_ = first[(V, end)]
            out('PE %s N=%d %s: Pe_hi at J_low %.4e (float %.4e; %s); largest %.4e at %s; smallest %.4e at %s' % (
                V, N, end, float(d0_['Pe']) if d0_['Pe'] is not None else float('nan'), d0_['pe_float'], pfmt(d0_.get('pe_parts', {})),
                max(pes)[0], max(pes)[1], min(pes)[0], min(pes)[1]))
    widest = max(((float(d['Ay'].rad()) / abs(flo(d['Ay'])), ln.split(' = ')[0]) for ln, d in rows[V]))
    out('WIDTH %s N=%d: the largest relative half-width of Ay %.3e at %s' % (V, N, widest[0], widest[1]))

# ---- the DRY records
if FAILS or NOFIRE:
    out('VERDICT INVALID (fails %s, plants not firing %s); no record written' % (FAILS, NOFIRE))
    sys.exit(3)
os.makedirs(OUTD, exist_ok=True)
code_sha = sha(os.path.abspath(__file__))
for V in ('U', 'C'):
    path = os.path.join(OUTD, 'MR_EXACT_PART_v1_10_%s_N%d.kv' % (V, N))
    assert os.path.dirname(path) == OUTD
    head = ['# MR_EXACT PART (N = %d) of pk22 mrx_cert_v1_10 on mr/v4 MR_SPECTRAL and MR_INSERT with mr/v3 MR_LEMMAP (mrx_combine_v1_10 joins '
            'N = 4 and 3 into the certified MR_EXACT record with ORIENT_CHECK and X_DEFINITION; h-1, h0, t-1 and a0; errors: %s)' % (N, 'each record\'s uniform claim' if V == 'U' else 'min of the uniform claim and the '
                                                                'certified J-law where m3_lawcert_c3h_v1_1 or m3_lawcert_v1_1 covers the entry (all of h-1 and h0; '
                                                                'E3 and S9 G entries of t-1 and a0), else the uniform claim (the c3, c3j, c3l and c3n entries)'),
            'FORMAT = MR_INPUT_KV_v4', 'RECORD = MR_EXACT_PART', 'PRODUCER = pk22 mrx_cert_v1_10 CERT_%s' % V,
            'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py:%s' % code_sha[:8], 'STATUS = CERTIFIED', 'EXPORT_STATUS = PART', 'RUN_VERDICT = VALID',
            'SOURCE = %s' % ' '.join('%s:%s' % (os.path.basename(p), shas[k][:8]) for k, (p, h) in srcs.items()) + ' MR_LEMMAP.kv:%s MR_SPECTRAL.kv:%s MR_INSERT.kv:%s MR_LEMMAP_V3F.kv:%s C10_RECORD_v1.kv:%s C13_RECORD_v1_1.kv:%s' % (
                lem_sha[:8], spe_sha[:8], ins_sha[:8], WAYA_SRC['P2'][1][:8], WAYA_SRC['C10'][1][:8], WAYA_SRC['C13'][1][:8]),
            'J_UNIFORMITY = PER-PIECE: every row holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf (t = 0)',
            'ORIENTATION = u_x along e1, u_y along e3', 'TRIAL_SET = %s' % TRIAL_SET, 'LEMMAP_SHA256 = %s' % lem_sha, 'X_POWER = %s' % X_POWER,
            'FIELDS = %s' % OUT_FIELDS]
    with open(path, 'x') as fh:
        fh.write('\n'.join(head + [ln for ln, d in rows[V]]) + '\n')
    out('RECORD %s sha256 %s rows %d' % (path, sha(path), len(rows[V])))
out('VERDICT VALID')
