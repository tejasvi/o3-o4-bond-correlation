#!/usr/bin/env python3
"""kt_sh1_v1.py -- pk15 (code/pk15/). Phase 1 FLOAT slice of S_TB' under the cost-check decision (2026-11-07 12:34Z: floats
only, no certified work; slice cap 12 h and 0.5 core-h); HZ_PLAN_v1_1 (ebee9574) sect. 2.0-2.3 and 2.7, HZ_PLAN_v1_ADD1_1 (eff30fb9).
SH1 (the t-amplitude entries), SH2's float odd norms, and the J = 300 float readings of C7 (S9(g)), KT-C8 (proposed S9(j)), C5 (S9(d))
and C6 (S9(e)), for N = 4 and N = 3. FLOAT DATA: exact Taylor coefficients a_k of riglap entries (kt_s9b_v3_2's exact_ak: no prep, no
Lemma 19.1c remainder), assembled in mpmath (dps 40) with S9(b)'s float Lemma A constants. No certificate. No run without the approval
naming this file's sha8.
Notation as HZ_PLAN_v1_1 sect. 1 and KT-S9B (kt_s9b_v1's header). t = 1/J; column c holds the vertices (T, M, B) = (3c, 3c+1, 3c+2);
  phi_0 is the vacuum polynomial (vacres_K3), phi_1 = e1 and phi_3 = e3 (ts_*_S.json); EVEN = (0, 1, 3). The Ritz pencil (T, G) on
  P = {psi-hat, e1, e3} comes from kt_s9b_v2's printed G and T entries (a_0..a_3 summed at t), with Ritz pairs (mu_k, c_k), k = 0, x, y,
  by kt_s9b_v2's ritz; mhat = 1 + m1 t + m2 t^2 + m3 t^3; s_x = mu_x/mu_0, s_y = mu_y/mu_0.
New entries (each divided by the main term main(G) of its graph; "xi on (u,v)" is riglap3's xi factor with c9 = (1, 0, ..)):
  Gxt,g,h    <phi_g, K_xi phi_h>/main_D, xi on the top bond (0,3), (g,h) in PE: 2 columns, pairs PAIRS_D + (0,3), F 13
  Gxbb,0,0   the same with xi on the bottom bond (2,5) (C-PARITY, PLANT-ODD)
  G00|DT     <phi_0, K phi_0>/main_D on Gxt's graph (C-AKV2)
  IhTt,g     <phi_g, K_xi V K phi_0>/main_N, xi on (0,3) next to phi_g, g in EVEN: 3 columns, F 16
  Iht,b      <phi_b, K V K_xi phi_0>/main_N, xi on (3,6) next to phi_0, b in EVEN: 3 columns, F 16
  Ihh,b      kt_s9b_v2's Ih,b recomputed, xi on (4,7) (C-H)
  XTT, XTB, XBT  <phi_0, K_xi V K V K_xi'' phi_0>/main_4, xi on (0,3) (T) or (2,5) (B) in gap 0-1 and xi'' on (6,9) (T) or (8,11) (B) in
             gap 2-3: 4 columns, F 20, a_0..a_2 only (amom2b holds for 20 forms at D <= 7, not at the D 8 that a_3 needs)
  Geps       <eps phi_0, K eps phi_0>/main_D, eps = (xi_TM - xi_MB)/2 on both columns: 2 columns, PAIRS_D, F 12
Amplitudes, single eigen trick (kt_s9b_v1's form; exact through O(t), errors O(t^2) from the residual g and psi-hat for Omega_0):
  e_k = mhat (c_k . I^e)/(G_00^{1/2} mu_0^w), w = 2 for t (I = Iht) and h (I = kt_s9b_v2's Ih), w = 1 for a (I = kt_s9b_v2's Dx).
  Centering c_t: single trick mhat Iht_0/(G_00 mu_0^2); double trick (C9 at b = 0) [mhat (Iht_0 + IhTt_0) - mhat^2 Gxt_00]/(G_00 mu_0^2).
  O_t := ||v_t^-||^2 = mhat^2 (XTT - XTB)/(2 G_00 mu_0^4), with v_t^- = H_delta Omega_0/lambda_0^2, delta = (xi_t - xi_bb)/2 and the flip
  (XBB = XTT, XBT = XTB); Va := ||v_a^-||^2 = mhat^2 Geps/(G_00 mu_0^2); R = main_N^2/(main_D main_4) is 1 to 1e-10 (C-R).
External float inputs (pinned by sha256): kt_rb_v1_5's OAT300 lines (pk01/out_kt_rb_v1_5_r<N>.out): eps_r, s, the s_x and mu_y
  intervals, tau, c-bar, rho_k, q, eps_0, eps_y, ||Q v_h|| and its parts, ||Q v_a||, dh_x, da_x, R_c and the |h|, |a| bounds; pk07's
  S5-S7 export, piece J in [300, 300.75]: rho_hi (S6's odd radius rho) and vm2_hi (S5's ||v_a^-||^2).
Stand-in, no engine yet: ||Q v_t^+|| := QSI = 3 (A_h part) + (Lam eps_r part) + (Lam + |t_0| + Hbad) s (1 + s) + Gbad, i.e. kt_rb's
  ||Q v_h|| formula with t_0 for h_0 and three times h's engine-A part [E]. In the certified phase engine A on the flip-even insertion
  (xi_t + xi_bb)/2 replaces it. C7 prints the QSI tolerance; every reading is repeated with 10 QSI (SENS lines, INFO).
Readings at J = 300 (floats; kill rules of HZ_PLAN_v1_1 sect. 5 and the 12:34Z decision):
  C7    dt_x = q QSI + eps_0 |t_0| + eps_y |t_y| + (q^2 + eps_0^2 + eps_y^2) |t_x|, A_t = |t_x| - dt_x. PASS iff A_t^2 > O_t, else KILL.
        Printed: O_t/A_t^2 (harmonic 0.29137), the QSI tolerance for A_t^2 >= 1.05 O_t, and C7.3's rho/s_x,lo.
  KT-C8 X_ta = t_x a_x and R_c^ta = |dt_x||a_x| + |t_x||da_x| + |dt_x||da_x|: PASS iff X_ta > 0 and R_c^ta <= 0.5 X_ta. C8.2: the (h, t)
        signal J h_x t_x/s_x^2 is > 0 and R_c^ht = J (|dh_x||t_x| + |h_x||dt_x| + |dh_x||dt_x|)/s_x,lo^2 <= 0.25 B_N e^{-kappa_1} (KR-C's
        budget times the harmonic t_x/a_x).
  C5    for (h, t) (= (h, bb)), (h, a) (= (h, b)) and (t, a) (the even part of (t, a), (t, b), (bb, a), (bb, b)):
        (i) Lemma A_y diagnostic: q_y = c-bar/(s_y,lo - tau); VOID if q_y >= 1, else Y = e_y f_y - |Qv_e||Qv_f| - dY (plan C5.1);
        (ii) crossover: X_lo = |e_x f_x| - (|de_x||f_x| + |e_x||df_x| + |de_x||df_x|) with Lemma A's de_x; k1 = min k with
             X_lo s_x,lo^k > |v_e^+| |v_f^+| s_yU^k, where s_yU = max(mu_y,hi, tau) + c-bar bounds S beyond Omega_0 and u_x and
             |v^+| = (e_x^2 + e_y^2 + |Qv|^2)^{1/2};
        (iii) block route for k < k1 (Lemma D of HCONN_FEAS_v1_1 with |Qv| factors; no true eigenvectors, no S4(c)): Pi = span(u~_x, u~_y),
             Q its even complement, A = Pi S Pi + Q S Q, B = S - A with |B| <= c-bar; Duhamel to second order gives <v_e, S^k v_f> >=
             sig(k) - E0(k) - H1(k) - H2(k) with sig = e_x f_x s_x^k + e_y f_y s_y^k, E0 = |Qv_e||Qv_f| tau^k,
             H1 = c-bar sum_{i+j=k-1} [n_e(i) tau^j |Qv_f| + tau^i |Qv_e| n_f(j)], n_e(i) = (e_x^2 s_x^{2i} + e_y^2 s_y^{2i})^{1/2},
             H2 = C(k,2) c-bar^2 s_xU^{k-2} |v_e^+||v_f^+|, s_xU = s_x,hi + c-bar^2/(s_x,lo - tau). The O(s) terms between psi-hat and
             Omega_0 are left out of this float.
        PASS iff k1 <= 8 and the block lower bound is > 0 at every k < k1; KILL only if (i) is void or negative and (iii) fails.
  C6    for the odd sector of (t, a), (t, b), (bb, a), (bb, b): O_ef = (O_t max(Va, vm2_hi))^{1/2}; Cov_lo(k) = EL(k) - rho^k O_ef, EL the
        larger of (ii) and (iii) for (t, a); k1_C6 = min k >= 1 with O_ef (rho/s_x,lo)^k <= 0.5 X_lo (the plan's half margin). PASS iff
        Cov_lo(k) > 0 for k = 1..8 and k1_C6 <= 3; the k = 0 pairs are C4's D5, D6.
Checks (gates unless INFO):
  C-HASH; C-CORE (the blocks copied from kt_s9b_v3_2.py and kt_s9b_v2.py are byte-identical); C-GRAPH (V/F 6/12, 6/13, 9/16, 12/20);
  C-XIT (each new xi factor against riglap2's dot series, as kt_s9b_v3_2's C-XIH); C-QCAP (every entry's Q-degree within its moment cap);
  C-K2 (exact_ak_k at order 2 equals exact_ak's a_0..a_2 on IhTt,0); C-AKV2 (G00|DT = kt_s9b_v2's G,0,0); C-H (Ihh,b = kt_s9b_v2's
  Ih,b); C-IHT0T (Iht,0 = IhTt,0, by reflection); C-IHT1T (the a_0, a_1 of IhTt,g equal those of mhat * Gxt,0,g); C-PARITY
  (Gxt,0,0 = Gxbb,0,0); C-SYM4 (XTB = XBT): every a_k to 1e-12 max(1, |a|);
  C-R (|R - 1| <= 1e-10 at J = 300); C-READ (h_x, a_x, x_R at J = 300 equal kt_s9b_v2's READ line to 1e-7 relative); C-RC (kt_rb's R_c from
  its printed |h|, |a| bounds, to 2e-3 relative);
  C-HARM at t = 0, relative 1e-6: kt_s9b_v2's x_R, y_R, h_0, a_0, a_x^2, h_y a_y, and t_0 = (N-1)(1 - 1/(2 sqrt5) - 1/(2 sqrt21))/2,
  t_x^2 = (N-1) x0^2/40, t_y^2 = (N-1) y0^2/168, t_x a_x = (N-1) x0^{3/2}/40, t_y a_y = (N-1) y0^{3/2}/56, h_y t_y = (N-1) y0^2/42,
  O_t = (N-1) x0 y0/(4 sqrt105), Va = 3 (N-1) e^{-kappa_1-kappa_2}/(4 sqrt105), and both centerings c_t = t_0.
  INFO: C-ODD0 (O_ef over the harmonic odd channel of (t, a) at t = 0; 1 for a rank-one z sector), C-VAX (Va against vm2_hi), and at
  t = 0 the ratios O_t/t_x^2 (0.29137) and O_ef/X_ta (0.6827).
Plants (must fire): PLANT-ODD ((Gxt,0,0 + Gxbb,0,0)/2 in place of the parity difference is not 0); PLANT-PAIR (C7 with h's x amplitude
  for t's fails); PLANT-SIGN (KT-C8 with -t_x for t_x alone fails); PLANT-SIGNY (C5's block route on (h, a) with -a_y fails at k = 0);
  PLANT-RHO (C6 with rho = s_x,lo finds no k1_C6).
Items: smoke (N = 4: C-HASH, C-CORE, C-GRAPH, C-XIT, C-K2 and one entry of each graph kind, timed); n4 and n3 (everything at that N).
CPU and CAP-STOP: RLIMIT_CPU soft LIM, hard LIM + 5; a guard before each moment build; SIGXCPU prints CAP-STOP and exits 3.
Prices [E], from kt_s9b_v3_2's AK4 (19 forms at D 7: 4.5 s) and the D of these entries: smoke 30-90 s (LIM 150, cap 155 s = 0.043
  core-h); n4 and n3 100-250 s each (LIM 300, cap 305 s = 0.085 core-h each), re-priced from the smoke.
Writes only pk15/out/out_kt_sh1_v1_<item>.out. Run (one job at a time):
  D=/mnt/g2/release/root/code/pk15; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_sh1_v1.py <item> <LIM> > $D/out/kt_sh1_v1_<item>.log 2>&1
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, time, math, hashlib, signal, traceback, re

ITEMS = ('smoke', 'n4', 'n3')
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: kt_sh1_v1.py ITEM LIM   (ITEM smoke | n4 | n3; LIM = RLIMIT_CPU soft limit in s, 10..400; hard LIM + 5)')
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (10 <= LIM <= 400):
    print('bad LIM %r (need 10 <= LIM <= 400)' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))
STAGE = ['start']

CODEDIR = '/mnt/g2/release/root/code'
SCR = CODEDIR + '/pk10/scripts'
INP = CODEDIR + '/pk10/scratch'
OWN = CODEDIR + '/pk15'
OUTD = OWN + '/out'
SRC_V2 = CODEDIR + '/pk01/kt_s9b_v2.py'
SRC_V32 = CODEDIR + '/pk02/kt_s9b_v3_2.py'
V2OUT = {3: CODEDIR + '/pk01/out_kt_s9b_v2_n3.out', 4: CODEDIR + '/pk01/out_kt_s9b_v2_n4.out'}
RBOUT = {3: CODEDIR + '/pk01/out_kt_rb_v1_5_r3.out', 4: CODEDIR + '/pk01/out_kt_rb_v1_5_r4.out'}
EXPORT = CODEDIR + '/pk07/out/export_kt_s67_cert_v2_2_sweep.kv'
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(OUTD, 'out_%s_%s.out' % (LABEL, MODE))
if not (os.path.isdir(OUTD) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUTD)
        and os.path.realpath(OUTD).startswith(os.path.realpath(OWN) + os.sep)):
    print('output directory check failed for %s' % OUT_PATH)
    sys.exit(2)
FH = open(OUT_PATH, 'x')


def cpu():
    return time.process_time()


def out(line):
    FH.write(line + '\n')
    FH.flush()


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)

PINS = {
    SCR + '/amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc',
    SCR + '/g2sw_core_snapshot.py': 'f1b51241c54e496a8de699cc3160de3281bf98c67d019f4e92459a222d3d003a',
    SCR + '/lapl2.py': 'b28ffbdb86fab237564f2db9ea8b3e904481fba31ad79e39421de7b8a9dfe116',
    SCR + '/npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
    SCR + '/pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
    SCR + '/riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
    SCR + '/riglap3.py': 'e394f81567e62222240050c7cbc70c480b0804d929a8713a7b30e70ebbf1ea69',
    SCR + '/riglap4.py': 'ed8eecd6c6ed529b9471097e205b63a9c0f1435973c498d9f1920850ec3d29d7',
    SCR + '/riglap5.py': 'bbfbea1f5b2680eec71eee647b2c608e08f8feacf8c21fbd67f4d0ff76f037a3',
    SCR + '/riglap5b.py': '0f9dc107d8709a78e4793db0fce23d8559fa93346d593304433162c72b5b0b93',
    SCR + '/riglap5c.py': 'efb2f505a2d169874e2beb358ed5179901fbd6bde0791ccd578309a2a57a054e',
    SCR + '/riglap5e.py': 'cafd025a5bb46c8b4a742ca3358d299bdea8e1b382893a9c8127ec4a1da821d9',
    SCR + '/riglap5r.py': '7feb47f7ce840837cf04b3156e4ed94c22ec2cb3543276c0d3892c4d6a6fe749',
    SCR + '/riglap5s.py': '44bdafd38b6a77af38af0e77ea17833fa08cdde734ecce3951795984b957e839',
    SCR + '/vacmod2.py': '533546b173af147a56e9531e26afa64cb3dbaccefd5fb7b1283f03baff06a000',
    INP + '/ts_N3_S.json': '26e20e76fbce80c205703f5ba27395ebddaeaa2713bb129b0b4e5902a2061955',
    INP + '/ts_N4_J170_D_S.json': 'd6d104ea1f2f64a82f051ce2872f1fbbd0628c9875b0743e4815bf74643fea8c',
    INP + '/vacres_K3_N3.json': 'ebcbd08ca532642188071c964039808a318038020bb1a788a7fa3a49cb357426',
    INP + '/vacres_K3_N4.json': '516b2501c37a65b21b617fba3cb1d7b02adf9966f409bc5105418822dfa0e765',
    V2OUT[3]: '3c7b2d2e6d461674b11a2e0554f8ce2294de6c644b5922ee722a159a01659cbf',
    V2OUT[4]: 'e7ffff8b54188e7c114df47e4b44bf382877af2298092edeb018c6ecc35a27cd',
    RBOUT[3]: '3e79a6c072ad730235944064b5f1980252d28336e35b1af1a1ad4e0cc35e54cc',
    RBOUT[4]: '842edc202150668838ce24b1fc54f0adbebadc8f0df984480a44c84fed6ecf5a',
    SRC_V2: '710ad713289dd232f2ea51414e99bcb75f8493ba76d664793f256e0b9bcfcbc7',
    SRC_V32: '0743aba2679e5f9694be5e14856df5dffa98d3eb1c11f776f215c34cc8df19fa',
    EXPORT: '6fe9ab65f5207dc3658c98ff4f3696bd2db6aa784b0dec84b33881b2da579c34',
}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('%s sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (LABEL, sha_file(os.path.abspath(__file__)), MODE, LIM, LIM, LIM + 5))
_bad = ['%s %s' % (os.path.basename(_p), sha_file(_p)) for _p in sorted(PINS) if sha_file(_p) != PINS[_p]]
out('C-HASH %s (%d pinned files)%s' % ('PASS' if not _bad else 'FAIL', len(PINS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, SCR)
import json
import numpy as np
from mpmath import mp
import riglap2 as _r
import riglap3 as _r3
from riglap2 import Graph
from riglap4 import group_factors, _deg
from riglap5b import series_product
from amom2b import AllMom2
from pseries import padd, pscale, pmul
from vacmod2 import A_EX, B_EX
from lapl2 import strip_graph
mp.dps = 40

J = 300.0
TOL = 1e-12
QCAP = 6
KB = 8
EVEN = (0, 1, 3)
PE = ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3))
LD, RD = (0, 1, 2), (3, 4, 5)
LN, RN = (0, 1, 2), (6, 7, 8)
L4, R4 = (0, 1, 2), (9, 10, 11)
PAIRS_D = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
GSPEC = {   # graph key: (columns, pairs, expected V, expected F)
    'D': (2, PAIRS_D, 6, 12),
    'DT': (2, PAIRS_D + [(0, 3)], 6, 13),
    'DB': (2, PAIRS_D + [(2, 5)], 6, 13),
    'NTT': (3, [(0, 1), (1, 2), (0, 2), (0, 3), (6, 7), (7, 8), (6, 8)], 9, 16),
    'NIT': (3, [(0, 1), (1, 2), (0, 2), (3, 6), (6, 7), (7, 8), (6, 8)], 9, 16),
    'NIH': (3, [(0, 1), (1, 2), (0, 2), (4, 7), (6, 7), (7, 8), (6, 8)], 9, 16),
    '4TT': (4, [(0, 1), (1, 2), (0, 2), (0, 3), (6, 9), (9, 10), (10, 11), (9, 11)], 12, 20),
    '4TB': (4, [(0, 1), (1, 2), (0, 2), (0, 3), (8, 11), (9, 10), (10, 11), (9, 11)], 12, 20),
    '4BT': (4, [(0, 1), (1, 2), (0, 2), (2, 5), (6, 9), (9, 10), (10, 11), (9, 11)], 12, 20),
}


def XI(u, v, w):
    """riglap3 xi factor on the pair (u, v); w is a third vertex that only fills riglap3's (T, M, B) slot (c9 uses xi_TM alone)."""
    return ('xi', (u, v, w), 0.0, [1.0] + [0.0] * 8)


XT01, XB01, XT12, XH12, XT23, XB23 = XI(0, 3, 1), XI(2, 5, 1), XI(3, 6, 7), XI(4, 7, 8), XI(6, 9, 10), XI(8, 11, 10)
EPS0 = ('xi', (0, 1, 2), 0.0, [0.5, -0.5] + [0.0] * 7)    # (xi_TM - xi_MB)/2 on column 0
EPS1 = ('xi', (3, 4, 5), 0.0, [0.5, -0.5] + [0.0] * 7)    # the same on column 1
XIT_CHECKS = (('DT', XT01, 0, 3), ('DB', XB01, 2, 5), ('NIT', XT12, 3, 6), ('4TT', XT23, 6, 9), ('4TB', XB23, 8, 11))
SFILE = {4: 'ts_N4_J170_D_S.json', 3: 'ts_N3_S.json'}
VFILE = {4: 'vacres_K3_N4.json', 3: 'vacres_K3_N3.json'}
B_N = {3: 0.06784, 4: 0.16603}
GUARD = 40.0
CORE = ((SRC_V32, 'kt_s9b_v3_2.py', 302, 310), (SRC_V32, 'kt_s9b_v3_2.py', 313, 324), (SRC_V32, 'kt_s9b_v3_2.py', 352, 367),
        (SRC_V32, 'kt_s9b_v3_2.py', 374, 385), (SRC_V2, 'kt_s9b_v2.py', 225, 303))


class CapStop(Exception):
    pass


def need(what):
    if cpu() > LIM - GUARD:
        raise CapStop(what)


# C-CORE block 1: kt_s9b_v3_2.py l.302-310
def check_xi(g, xi, u, v):
    xs = _r3.Model3(g, 3, [xi]).Fser(3).c
    ds = _r.Model(g, 4, [('dot', u, v, 1.0)]).Fser(4).c
    worst = 0.0
    for k in range(4):
        for e in set(xs[k]) | set(ds[k + 1]):
            a, b = xs[k].get(e, 0.0), ds[k + 1].get(e, 0.0)
            worst = max(worst, abs(a + b) / max(1.0, abs(a)))
    return worst
# C-CORE end 1


# C-CORE block 2: kt_s9b_v3_2.py l.313-324
def exact_ak(g, facs):
    """kt_s9b4_smoke_v1's exact_ak: riglap5b's a_k formulas without a prep (E_j from the H-series to order 3, F_i the factor series)."""
    scal, groups = group_factors(facs)
    gser = [_r3.Model3(g, 3, gf).Fser(3).c for gf in groups]
    Fi = series_product(gser, scal, 3)
    qmax = max([sum(e[g.V:]) for P in Fi for e in P] + [0])
    Hs = _r3.Model3(g, 3, []).H(3)
    H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
    H1sq = pmul(H1, H1)
    Ej = [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
    Dn = max(_deg(Fi[i]) + _deg(Ej[k - i]) for k in range(4) for i in range(k + 1) if Fi[i])
    return Fi, Ej, Dn, qmax
# C-CORE end 2


# C-CORE block 3: kt_s9b_v3_2.py l.352-367
def conv(a, b):
    return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(4)]


def dev(a, ref, ks=(0, 1, 2, 3)):
    return max(abs(a[k] - ref[k]) / max(1.0, abs(ref[k])) for k in ks)


def mhat(R3, d1=0.0):
    return [1.0, R3['m1'] + d1, R3['m2'], R3['m3']]


def h00_c9(mh, ih0, iht0, gx00, R):
    a = conv(mh, [ih0[k] + iht0[k] for k in range(4)])
    b = conv(conv(mh, mh), gx00)
    return [R * (a[k] - b[k]) for k in range(4)]
# C-CORE end 3


# C-CORE block 4: kt_s9b_v3_2.py l.374-385
def pv(R3, col, absq=False):
    q = [[abs(x) for x in R3[k]] if absq else R3[k] for k in ('q1', 'q2', 'q3')]
    return ('p', col, q[0], q[1], q[2])


def cpoly(Smat, R3, b, col, absq=False):
    if b == 0:
        return pv(R3, col, absq)
    c0, c9 = float(Smat[0, b]), [float(x) for x in Smat[1:, b]]
    if absq:
        c0, c9 = abs(c0), [abs(x) for x in c9]
    return ('xi', col, c0, c9)
# C-CORE end 4


# C-CORE block 5: kt_s9b_v2.py l.225-303
def chol(A):
    n = A.rows
    Lm = mp.zeros(n, n)
    for i in range(n):
        for j in range(i + 1):
            s = A[i, j] - mp.fsum([Lm[i, k] * Lm[j, k] for k in range(j)])
            if i == j:
                if s <= 0:
                    raise ValueError('Gram block not positive definite')
                Lm[i, i] = mp.sqrt(s)
            else:
                Lm[i, j] = s / Lm[j, j]
    return Lm


def lower_inv(Lm):
    n = Lm.rows
    X = mp.zeros(n, n)
    for i in range(n):
        X[i, i] = 1 / Lm[i, i]
        for j in range(i):
            X[i, j] = -mp.fsum([Lm[i, k] * X[k, j] for k in range(j, i)]) / Lm[i, i]
    return X


def jacobi(A):
    n = A.rows
    A = A.copy()
    V = mp.eye(n)
    tol = mp.mpf(10) ** (10 - 2 * mp.dps)
    for _ in range(100):
        if mp.fsum([A[i, j] ** 2 for i in range(n) for j in range(n) if i != j]) < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if A[p, q] == 0:
                    continue
                th = (A[q, q] - A[p, p]) / (2 * A[p, q])
                tt = (1 if th >= 0 else -1) / (abs(th) + mp.sqrt(th * th + 1))
                c = 1 / mp.sqrt(tt * tt + 1)
                s = tt * c
                for k in range(n):
                    x, y = A[k, p], A[k, q]
                    A[k, p], A[k, q] = c * x - s * y, s * x + c * y
                for k in range(n):
                    x, y = A[p, k], A[q, k]
                    A[p, k], A[q, k] = c * x - s * y, s * x + c * y
                for k in range(n):
                    x, y = V[k, p], V[k, q]
                    V[k, p], V[k, q] = c * x - s * y, s * x + c * y
    return [A[i, i] for i in range(n)], V


def ritz(G, T, pos):
    """Ritz pairs of the pencil (T, G) on the positions pos of (psi-hat, e1, e3): eigenvalues decreasing, coefficient vectors with
    c^T G c = 1, each with a positive entry at its own rank."""
    n = len(pos)
    Gs, Ts = mp.matrix(n, n), mp.matrix(n, n)
    for i, a in enumerate(pos):
        for j, b in enumerate(pos):
            Gs[i, j], Ts[i, j] = G[a][b], T[a][b]
    Li = lower_inv(chol(Gs))
    C = Li * Ts * Li.T
    for i in range(n):
        for j in range(i):
            C[i, j] = C[j, i] = (C[i, j] + C[j, i]) / 2
    lam, V = jacobi(C)
    order = sorted(range(n), key=lambda k: -lam[k])
    vals, vecs = [], []
    for rank, k in enumerate(order):
        cv = Li.T * mp.matrix([V[i, k] for i in range(n)])
        sg = 1 if cv[rank] >= 0 else -1
        vals.append(lam[k])
        vecs.append([sg * cv[i] for i in range(n)])
    return vals, vecs


def ev(ak, t):
    return mp.fsum([mp.mpf(a) * t ** k for k, a in enumerate(ak)])
# C-CORE end 5


NUM = r'([-+0-9.eE]+)'


def check_core():
    with open(os.path.abspath(__file__), 'rb') as fh:
        own = fh.read().split(b'\n')
    res = []
    for k, (path, name, a, b) in enumerate(CORE, 1):
        with open(path, 'rb') as fh:
            src = fh.read().split(b'\n')
        try:
            i0 = own.index(('# C-CORE block %d: %s l.%d-%d' % (k, name, a, b)).encode())
            i1 = own.index(('# C-CORE end %d' % k).encode())
        except ValueError:
            res.append(False)
            continue
        res.append(own[i0 + 1:i1] == src[a - 1:b])
    return res


def gate(fails, name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


def src_text(path):
    with open(path) as fh:
        return fh.read()


def load_json(name):
    with open(os.path.join(INP, name)) as fh:
        return json.load(fh)


def graph(key, N):
    nc, pairs = GSPEC[key][0], GSPEC[key][1]
    V, E = strip_graph(nc, (A_EX, B_EX))
    return Graph(V, E, pairs, N=N)


EJC = {}


def ejs(g, gk):
    """exact_ak's E_j, j <= 3 (the exponential of the H-series to order 3), computed once per graph."""
    if gk not in EJC:
        Hs = _r3.Model3(g, 3, []).H(3)
        H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
        H1sq = pmul(H1, H1)
        EJC[gk] = [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
    return EJC[gk]


def exact_ak_k(g, gk, facs, K):
    """exact_ak with the orders cut at K <= 3: Dn and the Q-degree over k <= K only (K = 2 for the 4-column entries)."""
    scal, groups = group_factors(facs)
    gser = [_r3.Model3(g, 3, gf).Fser(3).c for gf in groups]
    Fi = series_product(gser, scal, 3)
    qmax = max([sum(e[g.V:]) for P in Fi[:K + 1] for e in P] + [0])
    Ej = ejs(g, gk)
    Dn = max(_deg(Fi[i]) + _deg(Ej[k - i]) for k in range(K + 1) for i in range(k + 1) if Fi[i])
    return Fi, Ej, Dn, qmax


def specs_for(Smat, R3, smoke):
    """(name, graph key, factors, K) for every entry of the item."""
    def cp(b, col):
        return cpoly(Smat, R3, b, col)
    if smoke:
        return [('Gxt,0,0', 'DT', [cp(0, LD), XT01, cp(0, RD)], 3), ('IhTt,0', 'NTT', [cp(0, LN), XT01, pv(R3, RN)], 3),
                ('XTT', '4TT', [pv(R3, L4), XT01, XT23, pv(R3, R4)], 2)]
    S = [('G00|DT', 'DT', [cp(0, LD), cp(0, RD)], 3)]
    S += [('Gxt,%d,%d' % (g, h), 'DT', [cp(g, LD), XT01, cp(h, RD)], 3) for (g, h) in PE]
    S += [('Gxbb,0,0', 'DB', [cp(0, LD), XB01, cp(0, RD)], 3)]
    S += [('IhTt,%d' % g, 'NTT', [cp(g, LN), XT01, pv(R3, RN)], 3) for g in EVEN]
    S += [('Iht,%d' % b, 'NIT', [cp(b, LN), XT12, pv(R3, RN)], 3) for b in EVEN]
    S += [('Ihh,%d' % b, 'NIH', [cp(b, LN), XH12, pv(R3, RN)], 3) for b in EVEN]
    S += [('XTT', '4TT', [pv(R3, L4), XT01, XT23, pv(R3, R4)], 2), ('XTB', '4TB', [pv(R3, L4), XT01, XB23, pv(R3, R4)], 2),
          ('XBT', '4BT', [pv(R3, L4), XB01, XT23, pv(R3, R4)], 2)]
    S += [('Geps', 'D', [pv(R3, LD), EPS0, EPS1, pv(R3, RD)], 3)]
    return S


def compute_entries(N, specs, G_):
    """exact a_0..a_K of every entry; one AllMom2 per graph, at the largest Dn and Q-degree of its entries."""
    pre = {}
    for nm, gk, facs, K in specs:
        need('series ' + nm)
        STAGE[0] = 'series %s N=%d' % (nm, N)
        t0 = cpu()
        pre[nm] = (gk, K) + exact_ak_k(G_[gk], '%s/N%d' % (gk, N), facs, K) + (cpu() - t0,)
    E = {}
    for gk in sorted(set(v[0] for v in pre.values())):
        names = [nm for nm, gk2, _, _ in specs if gk2 == gk]
        g = G_[gk]
        D = max(max(pre[nm][4] for nm in names), 1)
        cap = max([QCAP] + [pre[nm][5] for nm in names])
        if not float(D + 1) ** g.F < 9.0e18:
            raise ValueError('amom2b cap: graph %s, F %d at D %d' % (gk, g.F, D))
        need('moments ' + gk)
        STAGE[0] = 'moments %s N=%d' % (gk, N)
        t0 = cpu()
        am = AllMom2(g.G, g.n, D, W=g.W, groups=g.groups, caps={1: cap})
        out('MOMENTS N=%d graph %s: F %d, D %d, Q-cap %d, %d codes at the top degree, %.1f s (cpu %.1f s)' % (
            N, gk, g.F, D, cap, len(am.codes[-1]), cpu() - t0, cpu()))
        for nm in names:
            _, K, Fi, Ej, Dn, qmax, ts = pre[nm]
            STAGE[0] = 'entry %s N=%d' % (nm, N)
            t0 = cpu()
            E[nm] = [float(sum(am.E2(Fi[i], Ej[k - i]) for i in range(k + 1) if Fi[i])) for k in range(K + 1)]
            out('ENTRY N=%d %s (graph %s, Dn %d, Q-degree %d; series %.1f s, sums %.1f s): ak=[%s]' % (
                N, nm, gk, Dn, qmax, ts, cpu() - t0, ', '.join(repr(x) for x in E[nm])))
        am = None
    return E, pre


def ck2(N, G_, Smat, R3, E, fails):
    g = G_['NTT']
    facs = [cpoly(Smat, R3, 0, LN), XT01, pv(R3, RN)]
    STAGE[0] = 'C-K2 N=%d' % N
    Fi, Ej, Dn3, q3 = exact_ak(g, facs)
    Dn2, q2 = exact_ak_k(g, 'NTT/N%d' % N, facs, 2)[2:]
    need('C-K2 moments')
    am = AllMom2(g.G, g.n, max(Dn2, 1), W=g.W, groups=g.groups, caps={1: max(QCAP, q2)})
    a2 = [float(sum(am.E2(Fi[i], Ej[k - i]) for i in range(k + 1) if Fi[i])) for k in range(3)]
    d = dev(a2, E['IhTt,0'], (0, 1, 2))
    out('C-K2 N=%d: IhTt,0 a_0..a_2 from moments at D %d (order-2 cut; exact_ak Dn %d, Q-degree %d) against the entry run: worst %.2e -> %s'
        % (N, Dn2, Dn3, q3, d, gate(fails, 'C-K2 N=%d' % N, d <= TOL)))


def v2_entries(N):
    txt = src_text(V2OUT[N])
    E = {}
    for mt in re.finditer(r'^ENTRY N=%d J=300 (\S+) ak=\[([^\]]*)\]' % N, txt, re.M):
        E[mt.group(1)] = [float(x) for x in mt.group(2).split(',')]
    want = ['G,%d,%d' % p for p in PE] + ['T,%d,%d' % p for p in PE] + ['Ih,%d' % b for b in EVEN] + ['Dx,%d' % b for b in EVEN]
    miss = [x for x in want if x not in E]
    if miss:
        raise ValueError('out_kt_s9b_v2_n%d.out lacks %s' % (N, ' '.join(miss)))
    return E


def parse_rb(N):
    txt = src_text(RBOUT[N])
    pat = {
        'VAC': r'OAT300 VAC N=%d J=300: eps_r %s, s %s \(vacscale formula\); mhat %s, lambda~_0 >= %s' % ((N,) + (NUM,) * 4),
        'RITZ': r'OAT300 RITZ N=%d J=300: mu %s %s %s \(bars %s %s %s\); s_x in \[%s, %s\], mu_y in \[%s, %s\], tau <= %s' % ((N,) + (NUM,) * 11),
        'AMP': r'OAT300 RITZ N=%d J=300: \|h\| <= %s %s %s \(0, x, y\), \|a\| <= %s %s %s' % ((N,) + (NUM,) * 6),
        'CBAR': r'OAT300 CBAR N=%d J=300: R_psi %s R_e1 %s R_e3 %s; rho %s %s %s; c-bar %s; q %s; eps_0 %s, eps_y %s' % ((N,) + (NUM,) * 10),
        'QVH': r'OAT300 QVH N=%d J=300: \|\|Q v_h\|\| <= %s \[A_h part %s, Lam eps_r %s \(Lam %s\), s-part %s, Hbad %s, Gbad %s\]' % (
            (N,) + (NUM,) * 7),
        'QVA': r'OAT300 QVA N=%d J=300: \|\|Q v_a\|\| <= %s \[' % (N, NUM),
        'RC': r'OAT300 RC N=%d J=300: dh_x %s, da_x %s; R_c %s ' % ((N,) + (NUM,) * 3),
    }
    R = {}
    for k in sorted(pat):
        mt = re.search(pat[k], txt)
        if mt is None:
            raise ValueError('%s: no OAT300 %s line for N=%d' % (os.path.basename(RBOUT[N]), k, N))
        R[k] = [float(x) for x in mt.groups()]
    return R


def parse_export(N):
    txt = src_text(EXPORT)
    mf = re.search(r'^FIELDS = (.+)$', txt, re.M)
    mv = re.search(r'^N%d_P0000 = ([^|]+)\|' % N, txt, re.M)
    st = [re.search(r'^%s = (\S+)' % k, txt, re.M) for k in ('RUN_VERDICT', 'EXPORT_STATUS')]
    if mf is None or mv is None or None in st:
        raise ValueError('export: FIELDS, N%d_P0000, RUN_VERDICT or EXPORT_STATUS missing' % N)
    d = dict(zip(mf.group(1).split(), [float(x) for x in mv.group(1).split()]))
    if not (d.get('jlo') == 300.0 and 300.0 < d.get('jhi', 0.0) <= 301.0):
        raise ValueError('export piece N%d_P0000 is not J in [300, 301]: %r %r' % (N, d.get('jlo'), d.get('jhi')))
    d['status'] = '%s %s' % (st[0].group(1), st[1].group(1))
    return d


def ritz_at(t, V2, E, R3):
    """Ritz pencil of kt_s9b_v2's G, T at t; single-trick amplitudes of h, a, t; the centering c_t (both tricks); O_t; Va."""
    G = [[ev(V2['G,%d,%d' % (min(b, c), max(b, c))], t) for c in EVEN] for b in EVEN]
    T = [[ev(V2['T,%d,%d' % (min(b, c), max(b, c))], t) for c in EVEN] for b in EVEN]
    vals, vecs = ritz(G, T, (0, 1, 2))
    mh = ev(mhat(R3), t)
    l0, sg0 = vals[0], mp.sqrt(G[0][0])

    def amp(cv, w, p):
        return mh * mp.fsum([cv[i] * w[i] for i in range(3)]) / (sg0 * l0 ** p)
    I = {'h': [ev(V2['Ih,%d' % b], t) for b in EVEN], 'a': [ev(V2['Dx,%d' % b], t) for b in EVEN],
         't': [ev(E['Iht,%d' % b], t) for b in EVEN]}
    A = {'l0': l0, 'sx': vals[1] / l0, 'sy': vals[2] / l0, 'mh': mh, 'G00': G[0][0]}
    for e, p in (('h', 2), ('a', 1), ('t', 2)):
        A[e] = [amp(vecs[k], I[e], p) for k in range(3)]
    A['ct1'] = mh * I['t'][0] / (G[0][0] * l0 ** 2)
    A['ct2'] = (mh * (I['t'][0] + ev(E['IhTt,0'], t)) - mh ** 2 * ev(E['Gxt,0,0'], t)) / (G[0][0] * l0 ** 2)
    A['Ot'] = mh ** 2 * (ev(E['XTT'], t) - ev(E['XTB'], t)) / (2 * G[0][0] * l0 ** 4)
    A['Va'] = mh ** 2 * ev(E['Geps'], t) / (G[0][0] * l0 ** 2)
    return A


def harm(N):
    s5, s21, s105 = mp.sqrt(5), mp.sqrt(21), mp.sqrt(105)
    x0, y0, e1, e2, k = (7 - 3 * s5) / 2, (23 - 5 * s21) / 2, (3 - s5) / 2, (5 - s21) / 2, N - 1
    return {'x_R': x0, 'y_R': y0, 'e1': e1, 'e2': e2, 'h_0': k * (1 - 2 / s21) / 2, 'a_0': k * (3 / (2 * s21) + 1 / (2 * s5)) / 2,
            'a_x^2': k * x0 / 40, 'h_y a_y': k * (5 + s21) * y0 ** 2 / 28, 't_0': k * (1 - 1 / (2 * s5) - 1 / (2 * s21)) / 2,
            't_x^2': k * x0 ** 2 / 40, 't_y^2': k * y0 ** 2 / 168, 't_x a_x': k * x0 * e1 / 40, 't_y a_y': k * y0 * e2 / 56,
            'h_y t_y': k * y0 ** 2 / 42, 'O_t': k * x0 * y0 / (4 * s105), 'Va': 3 * k * e1 * e2 / (4 * s105),
            'odd_ta': k * e1 * e2 * (1 - e1) * (1 - e2) / (4 * s105)}


def harmonic_checks(N, A0, H, fails):
    rows = [('x_R', A0['sx'], H['x_R'], 'abs', 1e-9), ('y_R', A0['sy'], H['y_R'], 'abs', 1e-9), ('h_x', A0['h'][1], mp.mpf(0), 'abs', 1e-9),
            ('h_0', A0['h'][0], H['h_0'], 'rel', 1e-6), ('a_0', A0['a'][0], H['a_0'], 'rel', 1e-6),
            ('a_x^2', A0['a'][1] ** 2, H['a_x^2'], 'rel', 1e-6), ('h_y a_y', A0['h'][2] * A0['a'][2], H['h_y a_y'], 'rel', 1e-6),
            ('t_0', A0['t'][0], H['t_0'], 'rel', 1e-6), ('t_x^2', A0['t'][1] ** 2, H['t_x^2'], 'rel', 1e-6),
            ('t_y^2', A0['t'][2] ** 2, H['t_y^2'], 'rel', 1e-6), ('t_x a_x', A0['t'][1] * A0['a'][1], H['t_x a_x'], 'rel', 1e-6),
            ('t_y a_y', A0['t'][2] * A0['a'][2], H['t_y a_y'], 'rel', 1e-6), ('h_y t_y', A0['h'][2] * A0['t'][2], H['h_y t_y'], 'rel', 1e-6),
            ('O_t', A0['Ot'], H['O_t'], 'rel', 1e-6), ('Va', A0['Va'], H['Va'], 'rel', 1e-6),
            ('c_t single trick', A0['ct1'], H['t_0'], 'rel', 1e-6), ('c_t double trick', A0['ct2'], H['t_0'], 'rel', 1e-6)]
    for name, got, want, mode, tol in rows:
        err = abs(got - want) if mode == 'abs' else abs(got / want - 1)
        out('C-HARM N=%d %s: %s (exact %s) %s err %.2e -> %s' % (N, name, mp.nstr(got, 12), mp.nstr(want, 12), mode, float(err),
                                                                  gate(fails, 'C-HARM N=%d %s' % (N, name), err <= tol)))
    oef = mp.sqrt(A0['Ot'] * A0['Va'])
    out('INFO C-ODD0 N=%d (t = 0): O_ef = (O_t Va)^{1/2} %s over the odd channel of (t_i, a_{i+2}) %s: ratio %s (1 for a rank-one z sector); '
        'O_t/t_x^2 %s (0.29137); O_ef/(t_x a_x) %s (0.6827)' % (N, mp.nstr(oef, 10), mp.nstr(H['odd_ta'], 10), mp.nstr(oef / H['odd_ta'], 10),
                                                                mp.nstr(A0['Ot'] / A0['t'][1] ** 2, 6), mp.nstr(oef / (A0['t'][1] * A0['a'][1]), 6)))


def readings(N, A, RB, EX, H, qf, tag, nofire):
    """the J = 300 float readings with ||Q v_t^+|| = qf QSI; nofire is None for the SENS pass (no plants). Returns {class: bool}."""
    res = {}
    eps_r, s = RB['VAC'][0], RB['VAC'][1]
    sxlo_rb, sxhi_rb, muylo, muyhi, tau = RB['RITZ'][6:11]
    rho0, rhox, rhoy, cbar, q, eps0, epsy = RB['CBAR'][3:10]
    Qvh, Ahp, LamEps, Lam, _sph, Hbad, Gbad = RB['QVH']
    Qva = RB['QVA'][0]
    dhx, dax = RB['RC'][0], RB['RC'][1]
    gapx = min(1 - sxhi_rb, sxlo_rb - muyhi)
    sxlo = sxlo_rb - cbar ** 2 / gapx
    sxU = sxhi_rb + cbar ** 2 / (sxlo - tau)
    syU = max(muyhi, tau) + cbar
    sx, sy = float(A['sx']), float(A['sy'])
    am = dict((e, [float(v) for v in A[e]]) for e in ('h', 'a', 't'))
    t0, tx, ty = abs(am['t'][0]), abs(am['t'][1]), abs(am['t'][2])
    QSI = qf * (3 * Ahp + LamEps + (Lam + t0 + Hbad) * s * (1 + s) + Gbad)
    dtx = q * QSI + eps0 * t0 + epsy * ty + (q ** 2 + eps0 ** 2 + epsy ** 2) * tx
    Ot, Va = float(A['Ot']), float(A['Va'])
    rho, vm2 = EX['rho_hi'], EX['vm2_hi']
    out('%s INPUTS N=%d J=300: Ritz s_x %.8f s_y %.8f; s_x,lo %.8f s_xU %.8f s_yU %.6f tau %.6f; c-bar %.4e q %.4e eps_0 %.3e eps_y %.3e; '
        '|Qv_h| %.4e |Qv_a| %.4e |Qv_t+| = %g QSI %.4e; dh_x %.4e da_x %.4e dt_x %.4e; rho %.6f vm2_hi %.6e' % (
            tag, N, sx, sy, sxlo, sxU, syU, tau, cbar, q, eps0, epsy, Qvh, Qva, qf, QSI, dhx, dax, dtx, rho, vm2))
    # C7
    At = tx - dtx
    ok7 = At > 0 and At * At > Ot and rho < sxlo
    qtol = (tx * (1 - q ** 2 - eps0 ** 2 - epsy ** 2) - eps0 * t0 - epsy * ty - math.sqrt(1.05 * Ot)) / q
    out('%s C7 N=%d J=300: |t_x| %.6e, dt_x %.3e, A_t %.6e; O_t %.6e; O_t/A_t^2 %.5f (harmonic 0.29137), A_t^2/O_t %.4f, margin '
        '1 - O_t/A_t^2 %.4f; QSI tolerance for A_t^2 >= 1.05 O_t %.3e (%.0f QSI); C7.3 rho/s_x,lo %.4f -> %s' % (
            tag, N, tx, dtx, At, Ot, Ot / At ** 2, At ** 2 / Ot, 1 - Ot / At ** 2, qtol, qtol / QSI, rho / sxlo, 'PASS' if ok7 else 'KILL'))
    res['C7'] = ok7
    if nofire is not None:
        Ah = abs(am['h'][1]) - dhx
        fired = not (Ah > 0 and Ah * Ah > Ot)
        out('PLANT-PAIR N=%d: C7 with h_x %.4e for t_x: A^2 %.3e against O_t %.3e -> %s' % (
            N, am['h'][1], max(Ah, 0.0) ** 2, Ot, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            nofire.append('PLANT-PAIR N=%d' % N)
    # KT-C8
    ax = abs(am['a'][1])
    Xta = am['t'][1] * am['a'][1]
    Rcta = dtx * ax + tx * dax + dtx * dax
    ok8 = Xta > 0 and Rcta <= 0.5 * Xta
    hx = am['h'][1]
    Bht = J * hx * am['t'][1] / sx ** 2
    Rcht = J * (dhx * tx + abs(hx) * dtx + dhx * dtx) / sxlo ** 2
    bud = 0.25 * B_N[N] * float(H['e1'])
    ok82 = Bht > 0 and Rcht <= bud
    out('%s KT-C8 N=%d J=300: X_ta = t_x a_x %.6e (t = 0: %.6e), R_c^ta %.3e, R_c^ta/X_ta %.3e (kill above 0.5) -> %s; C8.2: B^ht = J h_x t_x/s_x^2 '
        '%.6f (J -> inf: B_N e^-kappa1 = %.6f), R_c^ht %.4e against 0.25 B_N e^-kappa1 = %.4e, ratio %.4f -> %s' % (
            tag, N, Xta, float(H['t_x a_x']), Rcta, Rcta / abs(Xta), 'PASS' if ok8 else 'KILL', Bht, B_N[N] * float(H['e1']), Rcht, bud,
            Rcht / bud, 'PASS' if ok82 else 'KILL'))
    res['C8'], res['C8.2'] = ok8, ok82
    if nofire is not None:
        fired = not ((-am['t'][1]) * am['a'][1] > 0)
        out('PLANT-SIGN N=%d: KT-C8 with -t_x for t_x alone: X_ta %.4e -> %s' % (N, -Xta, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            nofire.append('PLANT-SIGN N=%d' % N)
    # C5
    Qn = {'h': Qvh, 'a': Qva, 't': QSI}
    dx = {'h': dhx, 'a': dax, 't': dtx}

    def vplus(e):
        return math.sqrt(am[e][1] ** 2 + am[e][2] ** 2 + Qn[e] ** 2)

    def nrm(e, i):
        return math.sqrt((am[e][1] * sx ** i) ** 2 + (am[e][2] * sy ** i) ** 2)

    def block(e, f, k, ysg=1.0):
        sig = am[e][1] * am[f][1] * sx ** k + ysg * am[e][2] * am[f][2] * sy ** k
        e0 = Qn[e] * Qn[f] * tau ** k
        h1 = cbar * sum(nrm(e, i) * tau ** (k - 1 - i) * Qn[f] + tau ** i * Qn[e] * nrm(f, k - 1 - i) for i in range(k))
        h2 = math.comb(k, 2) * cbar ** 2 * sxU ** (k - 2) * vplus(e) * vplus(f) if k >= 2 else 0.0
        return sig, sig - e0 - h1 - h2

    def xlo(e, f):
        if not am[e][1] * am[f][1] > 0:
            return None
        ex, fx = abs(am[e][1]), abs(am[f][1])
        return ex * fx - (dx[e] * fx + ex * dx[f] + dx[e] * dx[f])

    def k1_of(e, f):
        X = xlo(e, f)
        if X is None or not X > 0:
            return None
        return next((k for k in range(KB + 1) if X * sxlo ** k > vplus(e) * vplus(f) * syU ** k), None)
    qy = cbar / (muylo - tau) if muylo > tau else float('inf')
    for e, f in (('h', 't'), ('h', 'a'), ('t', 'a')):
        if qy < 1:
            e0y, exy = rho0 * qy / (1 - muylo), rhox * qy / (sxlo - muyhi)

            def dy(v):
                return qy * Qn[v] + e0y * abs(am[v][0]) + exy * abs(am[v][1]) + (qy ** 2 + e0y ** 2 + exy ** 2) * abs(am[v][2])
            Y = am[e][2] * am[f][2] - Qn[e] * Qn[f] - (dy(e) * abs(am[f][2]) + abs(am[e][2]) * dy(f) + dy(e) * dy(f))
            ly = 'Lemma A_y q_y %.4f: Y %.4e (Y/(e_y f_y) %.4f)' % (qy, Y, Y / (am[e][2] * am[f][2]))
        else:
            ly = 'Lemma A_y VOID (q_y = c-bar/(s_y,lo - tau) = %.3f >= 1)' % qy
        k1 = k1_of(e, f)
        X = xlo(e, f)
        bl = [block(e, f, k) for k in range(KB + 1)]
        upto = KB + 1 if k1 is None else k1
        okb = k1 is not None and all(bl[k][1] > 0 for k in range(upto))
        mm = min([bl[k][1] / bl[k][0] for k in range(upto)] + [1.0])
        out('%s C5 N=%d J=300 (%s, %s): e_y f_y %.6e, |Qv_e||Qv_f| %.3e; %s; crossover X_lo %s, |v_e+||v_f+| %.4e, k1 %s; block route '
            'lower/signal at k = 0..%d: %s; min over k < k1 %.4f -> %s' % (
                tag, N, e, f, am[e][2] * am[f][2], Qn[e] * Qn[f], ly, 'none' if X is None else '%.4e' % X, vplus(e) * vplus(f), k1, KB,
                ' '.join('%.4f' % (b[1] / b[0]) for b in bl), mm, 'PASS' if okb else 'KILL'))
        res['C5 (%s,%s)' % (e, f)] = okb
    if nofire is not None:
        sig, low = block('h', 'a', 0, -1.0)
        fired = not low > 0
        out('PLANT-SIGNY N=%d: block route on (h, a) with -a_y at k = 0: signal %.4e, lower %.4e -> %s' % (
            N, sig, low, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            nofire.append('PLANT-SIGNY N=%d' % N)
    # C6
    Vu = max(Va, vm2)
    Oef = math.sqrt(Ot * Vu)
    Xlo = xlo('t', 'a')

    def cov6(k, r):
        cross = Xlo * sxlo ** k - vplus('t') * vplus('a') * syU ** k
        return max(block('t', 'a', k)[1], cross) - r ** k * Oef

    def k1c6(r):
        return next((k for k in range(1, KB + 1) if Oef * (r / sxlo) ** k <= 0.5 * Xlo), None)
    k6 = k1c6(rho) if Xlo is not None and Xlo > 0 else None
    covs = [cov6(k, rho) for k in range(KB + 1)] if Xlo is not None else [float('nan')] * (KB + 1)
    ok6 = k6 is not None and k6 <= 3 and all(c > 0 for c in covs[1:])
    out('%s C6 N=%d J=300: O_t %.6e, Va %.6e (vm2_hi %.6e; used %.6e), O_ef %.6e, X_lo(t,a) %s, O_ef/X_lo %.4f, rho/s_x,lo %.4f; '
        'k1_C6 %s; Cov_lo(k)/(t_x a_x s_x^k) at k = 0..%d: %s -> %s' % (
            tag, N, Ot, Va, vm2, Vu, Oef, 'none' if Xlo is None else '%.6e' % Xlo, Oef / Xlo if Xlo else float('nan'), rho / sxlo, k6, KB,
            ' '.join('%.4f' % (c / (Xta * sx ** k)) for k, c in enumerate(covs)), 'PASS' if ok6 else 'KILL'))
    res['C6'] = ok6
    if nofire is not None:
        kp = k1c6(sxlo) if Xlo is not None and Xlo > 0 else None
        fired = kp is None
        out('PLANT-RHO N=%d: rho = s_x,lo: k1_C6 %s -> %s' % (N, kp, 'FIRES' if fired else 'DOES NOT FIRE'))
        if not fired:
            nofire.append('PLANT-RHO N=%d' % N)
    return res


def run_n(N, smoke, fails, nofire):
    Smat, R3 = np.array(load_json(SFILE[N])['S']), load_json(VFILE[N])
    STAGE[0] = 'graphs N=%d' % N
    keys = ('DT', 'NTT', '4TT') if smoke else tuple(sorted(GSPEC))
    G_ = dict((k, graph(k, N)) for k in keys)
    ok = all((G_[k].V, G_[k].F) == GSPEC[k][2:] for k in keys)
    out('C-GRAPH N=%d: %s -> %s' % (N, ', '.join('%s V %d F %d' % (k, G_[k].V, G_[k].F) for k in keys), gate(fails, 'C-GRAPH N=%d' % N, ok)))
    if not ok:
        return None
    for gk, xi, u, v in XIT_CHECKS:
        if gk in G_:
            STAGE[0] = 'C-XIT (%d,%d) N=%d' % (u, v, N)
            w = check_xi(G_[gk], xi, u, v)
            out('C-XIT N=%d xi on (%d,%d) (graph %s): worst %.2e -> %s' % (N, u, v, gk, w, gate(fails, 'C-XIT N=%d (%d,%d)' % (N, u, v), w <= TOL)))
    E, pre = compute_entries(N, specs_for(Smat, R3, smoke), G_)
    out('C-QCAP N=%d: largest Q-degree %d over %d entries; every moment cap is at least its entries\' Q-degree (%d where none exceeds %d) -> PASS'
        % (N, max(v[5] for v in pre.values()), len(pre), QCAP, QCAP))
    ck2(N, G_, Smat, R3, E, fails)
    if smoke:
        return None
    STAGE[0] = 'entry checks N=%d' % N
    V2 = v2_entries(N)
    mh = mhat(R3)
    rows = [('C-AKV2', 'G00|DT against kt_s9b_v2 G,0,0', dev(E['G00|DT'], V2['G,0,0'])),
            ('C-H', 'Ihh,b against kt_s9b_v2 Ih,b, b in EVEN', max(dev(E['Ihh,%d' % b], V2['Ih,%d' % b]) for b in EVEN)),
            ('C-IHT0T', 'Iht,0 (xi on (3,6)) against IhTt,0 (xi on (0,3))', dev(E['Iht,0'], E['IhTt,0'])),
            ('C-IHT1T', 'IhTt,g a_0, a_1 against mhat * Gxt,0,g, g in EVEN',
             max(dev(E['IhTt,%d' % g], conv(mh, E['Gxt,0,%d' % g]), (0, 1)) for g in EVEN)),
            ('C-PARITY', 'Gxt,0,0 against Gxbb,0,0', dev(E['Gxt,0,0'], E['Gxbb,0,0'])),
            ('C-SYM4', 'XTB against XBT (a_0..a_2)', dev(E['XTB'], E['XBT'], (0, 1, 2)))]
    for nm, what, d in rows:
        out('%s N=%d: %s: worst %.2e -> %s' % (nm, N, what, d, gate(fails, '%s N=%d' % (nm, N), d <= TOL)))
    pl = (E['Gxt,0,0'][0] + E['Gxbb,0,0'][0]) / 2
    out('PLANT-ODD N=%d: (Gxt,0,0 + Gxbb,0,0)/2 a_0 = %.6f in place of the parity difference -> %s' % (
        N, pl, 'FIRES' if abs(pl) > 1e-3 else 'DOES NOT FIRE'))
    if not abs(pl) > 1e-3:
        nofire.append('PLANT-ODD N=%d' % N)
    R = math.exp(2 * G_['NIH'].logmain(J) - G_['D'].logmain(J) - G_['4TT'].logmain(J))
    out('C-R N=%d: R = main_N^2/(main_D main_4) %.15f at J = 300 -> %s' % (N, R, gate(fails, 'C-R N=%d' % N, abs(R - 1) <= 1e-10)))
    STAGE[0] = 'Ritz N=%d' % N
    H = harm(N)
    A0 = ritz_at(mp.mpf(0), V2, E, R3)
    harmonic_checks(N, A0, H, fails)
    A = ritz_at(mp.mpf(1) / 300, V2, E, R3)
    mt = re.search(r'READ N=%d J=300: h_x %s, a_x %s, x_R %s, B\(J\)' % ((N,) + (NUM,) * 3), src_text(V2OUT[N]))
    if mt is None:
        raise ValueError('out_kt_s9b_v2_n%d.out: no READ line' % N)
    ref = [float(x) for x in mt.groups()]
    got = [float(A['h'][1]), float(A['a'][1]), float(A['sx'])]
    d = max(abs(g_ / r_ - 1) for g_, r_ in zip(got, ref))
    out('C-READ N=%d: h_x %.11g, a_x %.11g, x_R %.11g against kt_s9b_v2 READ %r: worst relative %.2e -> %s' % (
        N, got[0], got[1], got[2], ref, d, gate(fails, 'C-READ N=%d' % N, d <= 1e-7)))
    RB = parse_rb(N)
    sxlo_rb, sxhi_rb, muyhi = RB['RITZ'][6], RB['RITZ'][7], RB['RITZ'][9]
    cbar = RB['CBAR'][6]
    sxlo = sxlo_rb - cbar ** 2 / min(1 - sxhi_rb, sxlo_rb - muyhi)
    hbx, abx = RB['AMP'][1], RB['AMP'][4]
    dhx, dax, Rc = RB['RC']
    Rc2 = J * (dhx * abx + hbx * dax + dhx * dax) / sxlo ** 2
    out('C-RC N=%d: kt_rb R_c from its printed |h_x| %.4e, |a_x| %.4e, dh_x, da_x and s_x,lo %.8f: %.5e against its R_c %.4e: relative %.2e -> %s' % (
        N, hbx, abx, sxlo, Rc2, Rc, abs(Rc2 / Rc - 1), gate(fails, 'C-RC N=%d' % N, abs(Rc2 / Rc - 1) <= 2e-3)))
    EX = parse_export(N)
    out('INPUT N=%d: pk07 export piece N%d_P0000 (J %.2f-%.4f, %s): rho_hi %.10e, vm2_hi %.10e, ro_hi %.6f' % (
        N, N, EX['jlo'], EX['jhi'], EX['status'], EX['rho_hi'], EX['vm2_hi'], EX['ro_hi']))
    out('INFO C-VAX N=%d: Va(300) %.8e against vm2_hi %.8e: ratio %.6f' % (N, float(A['Va']), EX['vm2_hi'], float(A['Va']) / EX['vm2_hi']))
    out('SH1 N=%d J=300: t-amplitudes (u~_0, u~_x, u~_y) %s; c_t single trick %s, double trick %s (difference %.2e); s_x %s, s_y %s; '
        'h %s; a %s; O_t %s; Va %s' % (N, ' '.join(mp.nstr(v, 12) for v in A['t']), mp.nstr(A['ct1'], 12), mp.nstr(A['ct2'], 12),
                                      float(A['ct1'] - A['ct2']), mp.nstr(A['sx'], 12), mp.nstr(A['sy'], 12),
                                      ' '.join(mp.nstr(v, 10) for v in A['h']), ' '.join(mp.nstr(v, 10) for v in A['a']),
                                      mp.nstr(A['Ot'], 12), mp.nstr(A['Va'], 12)))
    STAGE[0] = 'readings N=%d' % N
    res = readings(N, A, RB, EX, H, 1.0, 'READ', nofire)
    sens = readings(N, A, RB, EX, H, 10.0, 'SENS', None)
    out('READING N=%d J=300 (float): %s' % (N, '; '.join('%s %s' % (k, 'PASS' if res[k] else 'KILL') for k in sorted(res))))
    out('SENS N=%d J=300 (|Qv_t+| = 10 QSI, INFO): %s' % (N, '; '.join('%s %s' % (k, 'PASS' if sens[k] else 'KILL') for k in sorted(sens))))
    return res


def item():
    fails, nofire = [], []
    core = check_core()
    out('C-CORE %s (%d blocks: %s)' % (gate(fails, 'C-CORE', all(core)), len(core), ' '.join('same' if c else 'DIFF' for c in core)))
    complete = False
    try:
        for N in ((4,) if MODE == 'smoke' else (int(MODE[1]),)):
            run_n(N, MODE == 'smoke', fails, nofire)
        complete = True
    except CapStop as e:
        out('CAP-STOP before %s at cpu %.1f s (LIM %d)' % (e, cpu(), LIM))
    why = fails + ['%s did not fire' % x for x in nofire] + ([] if complete else ['INCOMPLETE'])
    out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (MODE, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))


def main():
    try:
        item()
    except Exception as e:
        out(traceback.format_exc().rstrip())
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        out('VERDICT INVALID (ERROR)')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
