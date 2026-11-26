#!/usr/bin/env python3
"""kt_s9h_asm_v1_7.py (pk25, code/pk25/asm/; G5 item C6a): the record MR_SPECTRAL (MR_INPUT_KV_v3) and the Lemma P side table MR_LEMMAP
(MR_LEMMAP_KV_v2) per piece of R4's grid, for the MIDROW M1 inputs. Made by asm/make_kt_s9h_asm_v1_3.py from asm/src/kt_s9h_asm_v1_4b.py.in (the v3 issue).
v3 (the P0_LOG row 4363; records in mr/v3, mr/v2 kept): every piece is computed twice, with the S9 records' entries (entry_piece;
v2's computation byte for byte) and with the law certificates (G and T from S8 D's g and S8 N's T, Dx from S8 D's DY, E2's e,b and
FF's z, each by entry_law_piece at the piece's J_lo through pk25's reader fork m3_reader_s9h_v1; Iht stays the S9 record's, which no
row uses), and each written field is the intersection of the two (both are certified bounds of the same quantity: the larger lower end,
the smaller upper end; single upper bounds the smaller, single lower bounds the larger). So no v3 field is wider than v2's computation.
New gates: C-LAW-READ, C-ALIAS (the law certificates' ak inside the records' coefficient balls for G, T, Dx and E2's e,b, FF's z),
C-COMBINE (no empty intersection); new plants PLANT-LAW-PIN and PLANT-ALIAS; PLANT-L3-GAP, PLANT-LK-GAP, PLANT-ORIENT and PLANT-RW run
on the law path. The v2 text follows.
The CORE block is R4's code (pk15/kt_p2_assembly_v1_37_1.py, full sha256 in R4_SHA), copied by tool def by def and constant by constant;
C-CORE re-reads the pinned R4 file at run time and compares every copied def and constant with this file's copy (ast source segments, byte
for byte).
Specification: pk24/MIDROW_G6_SPEC_v1_5.md (6505bfcd) sect. 1, 4.4 and 6; pk25/G5_PLAN_v1_ADD1_3.md (f41c45e5) sect. 1 (L3);
the addendum to the G6 v1_5 delta (2d2c0930: the side table also carries the Ritz vectors); the interface note
pk25/MR_S9H_INTERFACE_NOTE_v1_1.md (MR_LEMMAP_KV_v2).
Per piece (N = 4 from the piece that holds J = 350, N = 3 from the piece that holds J = 300; t over the piece's t-ball, so every value holds at
every J of the piece; the last piece runs to t = 0):
- the Ritz problem on W = span{psi-hat, e1, e3} (flip-even sector): R4's ritz_piece on the S9 records' 18 entries and R4's lemma_a_cbar with
  M2(b)'s eps_r and M4's R_e1, R_e3 at the piece's left end (both laws nonincreasing in J) and tau = tau4, S4(c) v1_1's claim
  ||Q_4 S Q_4|| <= tau4 (on flip-even vectors Q_4 = Q_W);
- S units (S = T/lambda_0), with s_x, mu_y the Ritz ratios to the top Ritz value and m0lo R4's lower bound of the top Ritz value over
  lambda_0: mu_0 in [m0lo, 1], mu_x in [s_x,lo m0lo, s_x,hi], mu_y in [mu_y,lo m0lo, mu_y,hi] (lambda_0 is at least the top Ritz value);
  s_x in [mu_x,lo, sxhi] and s_y in [mu_y,lo, syhi] (min-max below, R4's Kato-Temple and Weyl bounds above); rho_k = R4's residual bounds
  rho_k >= |Q_W S u~_k|;
- L3 (ADD1_3 sect. 1.1, the same proof at a = 0 with s_0 = 1) at a = 0, x, y: g_a = s_a,lo - tau4, g_ka = |mu_k - s_a| (lower ends),
  D_a = 1 - sum_(k != a) rho_k^2/(g_a g_ka) > 0, q_a = (rho_a/g_a)/D_a >= |Q_W u_a|, eps_ka = rho_k q_a/g_ka >= |<u~_k, u_a>|, with u_a
  oriented by <u~_a, u_a> > 0;
- Lemma P: L_k = rho_k/(mu_k,lo - tau4) >= |P_e u~_k|, computed from the written decimals of rho_k, mu_k,lo and tau4;
- orientation (the rule, P0_LOG line 4089: u_x along e1 = xi_TB - (N - 1)/sqrt 5 and u_y along e3, never by a stored state's sign):
  R4's ritz_piece orients by the stored states (c_kk > 0); this file then multiplies u~_x by sign(S[3][1]) and u~_y by sign(S[1][3]) of the
  pinned trial-set file (S[3][b] is stored state b's xi_TB coefficient, S[1][b] its xi_TM coefficient; at N = 4 the stored state 1 is
  -2.39 e1). C-ORIENT asks, after the flip, a positive xi_TB coefficient of u~_x and a positive xi_TM coefficient of u~_y from the
  harmonic states 1 and 3 (sum_(b in 1, 3) c_kb S[.][b]), and uhat_00 > 0 with <u~_0, psi-hat/|psi-hat|> > 0 for u~_0. v1_2 kept R4's
  stored-state orientation, which flips u_x at N = 4 (its records are withdrawn);
- the unit-basis Ritz coefficients uhat_kb = c_kb |psi_b| (u~_k = sum_b uhat_kb psi_b/|psi_b|) in that orientation;
- c_x(-1), c_y(-1): A~_k = <u~_k, w-hat> = sum_b c_kb e_b with S8's E2 entries e,b = <phi_b, K V 1>/main_mix, |w-hat|^2 = z/r_main with
  FF's z = <V 1, K V 1>/main_free and r_main = main_mix^2/(main_D main_free) = (sqrt(det L_D det L_free)/det L_mix)^(N - 1) (matrix-tree;
  pk07's r_main_iv form), all in the common unit main_mix/main_D^(1/2); |Q_W w-hat|^2 = |w-hat|^2 - sum_k A~_k^2 (Parseval); Lemma A at
  levels 0, x, y with L3's q_a and eps_ka: |<u_a, w-hat> - A~_a| <= q_a |Q_W w-hat| + sum_(k != a) eps_ka |A~_k| + (q_a^2 +
  sum_(k != a) eps_ka^2) |A~_a|; then c_a(-1) = <u_a, w-hat>/<u, w-hat>;
- rho1_hi and Rw_hi: the tokens of pk07's certified S_V export (EXPORT_KT_S67_v1), copied (C-SV-COPY).
Gates: C-HASH, C-CORE, C-PINS-R4 (stops); C-ENGINE-FIELDS, C-GRID, C-RITZ-READ, C-M2B-READ, C-M4-READ, C-SV-READ, C-TAU-TRIAL, C-E2FF-READ,
C-TAU4, C-RMAIN, C-ORIENT-SIGNS, C-CX0-SIGN; per piece C-PIECE (every piece computes: ritz_piece's and lemma_a_cbar's refusals, C-ORDER,
C-TAU-SY, C-L3-FP, C-LK-GAP,
C-ORIENT, C-QW, C-DEN, C-RW); on the last piece of each N the exact controls C-S0 (x0 and y0 inside the s and mu intervals) and CX0
(at t = 0, c_x(-1) = +x0 ((N - 1)/2)^(1/2) and c_y(-1) = +y0 ((N - 1)/2)^(1/2) in the canonical orientation, KC4's t^0 values,
x0 = (7 - 3 sqrt 5)/2, y0 = (23 - 5 sqrt 21)/2; C-CX0-SIGN also asks sign(e,1 at t^0) sign(S[3][1]) = +1 and sign(e,3 at t^0)
sign(S[1][3]) = +1); the
float twin C-F2 (scipy's generalized eigensolver on the entry midpoints at one t of the first, a middle and the last piece of each N); the
written records' C-WRITE (read back and parsed, the field checks of the M1 engine's G-UNIF, the L_k relation exactly, the tau4 token in both
records). INFO: C-L3-DOM (L3's q against the c-bar form), the c(-1) widths.
Plants (each must fire): PLANT-CORE, PLANT-PINS-R4, PLANT-RITZ-S9-PIN, PLANT-M2B-PIN, PLANT-M4-PIN, PLANT-SV-PIN, PLANT-SV-GRID,
PLANT-E2-PIN, PLANT-E2-TRIAL, PLANT-TAU4-LOW, PLANT-RMAIN, PLANT-L3-GAP, PLANT-LK-GAP, PLANT-ORIENT (u~_x negated after the flip, which is
v1_2's orientation at N = 4), PLANT-RW, PLANT-S0, PLANT-CXSWAP, PLANT-F2, PLANT-WRITE, PLANT-CX0-SIGN (N = 4's x sign reversed).
Usage: kt_s9h_asm_v1_7.py MODE TAG
  MODE dry: everything, with the records (STATUS DRY) written to asm/dry_<TAG>/ (a new folder).
  MODE cert (only under the approval naming this file's sha8): the records (EXPORT_STATUS CERTIFIED) written to mr/v3/ (MR_SPECTRAL.kv and
  MR_LEMMAP.kv; neither may exist).
  The run output is asm/out/out_<this file's name>_<MODE>_<TAG>.out (opened with 'x'). Records are written only when every gate passes and every
  plant fires (VERDICT VALID).
Interval arithmetic: python-flint arb at 256 bits (R4's ctx.prec); decimals out by R4's dec_lo and dec_hi (17 significant digits, directed)."""
import ast
import hashlib
import json
import math
import os
import re
import sys
import time
from fractions import Fraction

# ---- CORE constants: R4's module-level assignments, copied by the maker (C-CORE compares them with the pinned R4 file)
W18 = '/mnt/g2/release/root/code'
GRID = W18 + '/pk07/out/export_kt_s67_cert_v2_2_sweep.kv'
G00_CLAIM = 'for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err (Lemma U'
VACRES = dict((N, W18 + '/pk11/out/vacres_K3_N%d_sym_v1.json' % N) for N in (4, 3))
C1_CLAIM = '||K^{1/2} |g| || <= eps_r mhat ||psihat||'
M2B = (W18 + '/pk02/M2B_KV_v1.txt', W18 + '/pk02/out/out_m2b_asm_v1.out')
M2B_READER_PATH = W18 + '/pk02/m2b_reader_v1.py'
M2B_PREC = 256
M4 = (W18 + '/pk15/M4_KV_v1.txt', W18 + '/pk15/out/out_m4_asm_v1.out')
M4_READER_PATH = W18 + '/pk15/m4_reader_v1.py'
M4_PREC = 256
S67 = (W18 + '/pk07/out/export_kt_s9h_v1_2_vsweep.kv', W18 + '/pk07/out/out_kt_s9h_v1_2_vsweep.out')
S67_READER_PATH = W18 + '/pk07/kt_s67_export_reader_v2_1.py'
S67_SCRIPT = W18 + '/pk07/kt_s9h_v1_2.py'
REVEN, RPE = (0, 1, 3), ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3))
RITZ_KEYS = tuple(['G,%d,%d' % p for p in RPE] + ['T,%d,%d' % p for p in RPE] + ['Iht,%d' % b for b in REVEN] + ['Dx,%d' % b for b in REVEN])
S9_RECORDS = {4: (W18 + '/pk03/out/m3_s9_N4_J300_v1_8_3.json', W18 + '/pk03/out/m3_run_v1_8_3_asm9.4.out'), 3: (W18 + '/pk03/out/m3_s9_N3_J300_v1_8_3.json', W18 + '/pk03/out/m3_run_v1_8_3_asm9.3.out')}
TS_FILES = {4: W18 + '/pk11/out/ts_N4_J170_D_S_z9sym_v1.json', 3: W18 + '/pk11/out/ts_N3_S_z9sym_v1.json'}
M3_READER_PATH = W18 + '/pk03/m3_reader_v4_4.py'
KERNEL_SHA = '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0'
KERNEL_LINE = 'arbeng_c2b_v2.py %s ctx.prec 512' % KERNEL_SHA
M3_READER_SHA = 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0'
BADWORDS = ('PRECERT', 'STUB')

MODES = ('dry', 'cert')
if len(sys.argv) != 3 or sys.argv[1] not in MODES or not re.fullmatch(r'[A-Za-z0-9_]{1,40}', sys.argv[2]):
    print('usage: kt_s9h_asm_v1_7.py dry|cert TAG')
    sys.exit(2)
MODE, TAG = sys.argv[1], sys.argv[2]
SELF = os.path.abspath(__file__)
LABEL = os.path.splitext(os.path.basename(SELF))[0]
OWN = W18 + '/pk25'
ASM = OWN + '/asm'
OUT_DIR = ASM + '/out'
OUT_PATH = os.path.join(OUT_DIR, 'out_%s_%s_%s.out' % (LABEL, MODE, TAG))
RECDIR = OWN + '/mr/v3' if MODE == 'cert' else os.path.join(ASM, 'dry_%s' % TAG)
R4_PATH = W18 + '/pk15/kt_p2_assembly_v1_37_1.py'
R4_SHA = 'e92342b001b99e2f5a730170d2111788e8093042ad5957b6409fe96feadb6b0b'
CORE_DEFS = ('out', 'sha_file', 'Refused', 'lines_of', 'gate', 'dec_hi', 'dec_lo', 'kv_parse', 'read_kv', '_mode_checks', '_frac_ball', 'load_m3', 'read_grid', 'tball', 'grid_j', 'q2arb', 't_ends', 'check_c1', 'load_m2b', 'm2b_eps', 'm2b_call', 'load_m4', 'm4_call', 'm4_law', 'm2b_mhat_coeffs', 'check_tau_trial', 'load_ritz_mock', 'check_s9_trial', 'load_ritz', 'entry_piece', 'mhat_ball', '_min_pt', '_jacobi3', 'ritz_piece', 'lemma_a_cbar', 'pd_vectors', 'pd_dk_meet', 'plant')
CORE_CONSTS = ('CODEDIR', 'GRID', 'G00_CLAIM', 'VACRES', 'C1_CLAIM', 'M2B', 'M2B_READER_PATH', 'M2B_PREC', 'M4', 'M4_READER_PATH', 'M4_PREC', 'S67', 'S67_READER_PATH', 'S67_SCRIPT', 'REVEN,RPE', 'RITZ_KEYS', 'S9_RECORDS', 'TS_FILES', 'M3_READER_PATH', 'KERNEL_SHA', 'KERNEL_LINE', 'M3_READER_SHA', 'BADWORDS')
MR_ENGINE = W18 + '/pk24/mr_engine/kt_mr_assembly_v1_6.py'
S4C_RECORD = W18 + '/pk21/p2/s4c/S4C_TIGHT_RECORD_v1_1.md'
S4C_MANIFEST = W18 + '/pk21/p2/s4c/MANIFEST_S4C_TIGHT_RECORD_v1_1.sha256'
TAU4_TSV = dict((N, W18 + '/pk21/p2/s4c/out/tau4_kt_s9h_tau4_pk21_v1_N%d.tsv' % N) for N in (4, 3))
E2REC = dict((N, (W18 + '/pk03/out/m3_s8v3_E2_N%d_J300_v1_8_1.json' % N, W18 + '/pk03/out/m3_run_v1_8_1_asmP.%d.out' % N)) for N in (4, 3))
FFREC = dict((N, (W18 + '/pk03/out/m3_s8v3_FF_N%d_J300_v1_8_1.json' % N, W18 + '/pk03/out/m3_run_v1_8_1_asmP.%d.out' % N)) for N in (4, 3))
ENDW = dict((N, W18 + '/pk03/out/m3_endw_N%d_J300_v1_7.json' % N) for N in (4, 3))
RDR = OWN + '/m3/m3_reader_s9h_v1.py'
M3O = W18 + '/pk03/out/'
S8REC = dict((N, dict((F, (M3O + 'm3_s8v3_%s_N%d_J300_v1_8_1.json' % (F, N), M3O + 'm3_run_v1_8_1_asmP.%d.out' % N)) for F in ('D', 'E2', 'E3', 'FF')))
             for N in (4, 3))
for _N in (4, 3):
    S8REC[_N]['N'] = (M3O + 'm3_s8v3_N_N%d_J300_v1_8_2.json' % _N, M3O + 'm3_run_v1_8_2_asmN.%d.out' % _N)
S8CERT = dict((N, {'v1_1': (M3O + 'm3_lawcert_v1_1_N%d.json' % N, M3O + 'm3_lawcert_v1_1_%d.out' % N),
                   'v1_2': (M3O + 'm3_lawcert_v1_2_N%d.json' % N, M3O + 'm3_lawcert_v1_2_%d.out' % N)}) for N in (4, 3))
M_RITZ = W18 + '/pk15/mocks/mock_ritz_entries_v1.kv'
JLOW = {4: 350, 3: 300}
KNAME = ('0', 'x', 'y')
BNAME = ('p', '1', '3')
SPEC_FIELDS = 'jlo jhi sx_lo sx_hi sy_lo sy_hi tau_hi rho1_hi Rw_hi cxm1_lo cxm1_hi cym1_lo cym1_hi'
LEMMAP_FIELDS = ' '.join(['jlo jhi rho0_hi rhox_hi rhoy_hi mu0_lo mux_lo muy_lo tau_hi L0_hi Lx_hi Ly_hi']
                         + ['u%s%s_lo u%s%s_hi' % (k, b, k, b) for k in KNAME for b in BNAME]
                         + ['q0_hi qx_hi qy_hi eps_x0_hi eps_y0_hi eps_0x_hi eps_yx_hi eps_0y_hi eps_xy_hi'])
ORIENT = 'u_x along e1, u_y along e3'
J_UNIF = 'PER-PIECE: every row holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf (t = 0)'
PINS = {
    '/mnt/g2/release/root/code/pk02/M2B_KV_v1.txt': '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',
    '/mnt/g2/release/root/code/pk02/m2b_reader_v1.py': 'a9f15db48e9fa51629448181d8a83679c1b93cd2b5696c8ed1e6b41d60df8b02',
    '/mnt/g2/release/root/code/pk02/out/out_m2b_asm_v1.out': 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391',
    '/mnt/g2/release/root/code/pk15/M4_KV_v1.txt': '4bafdcc1c41cf44f6b618644d7b0fdd404422aa5ffeadcfaadae02183e9eee51',
    '/mnt/g2/release/root/code/pk15/kt_p2_assembly_v1_37_1.py': 'e92342b001b99e2f5a730170d2111788e8093042ad5957b6409fe96feadb6b0b',
    '/mnt/g2/release/root/code/pk15/m4_reader_v1.py': '5cef440ae313eddd2e6bcf49aac835f2595e61b6a3e59b23fca0c15671ec6bcd',
    '/mnt/g2/release/root/code/pk15/mocks/mock_ritz_entries_v1.kv': '568e62829e1fa07f774b48f23e11d0f677be6841be81e2b84c2382d630a8f15a',
    '/mnt/g2/release/root/code/pk15/out/out_m4_asm_v1.out': '616dd9e1919695ed9dc953c55e8c46d66dabd9700d2913722d11f94502dc858e',
    '/mnt/g2/release/root/code/pk03/m3_reader_v4_4.py': 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0',
    '/mnt/g2/release/root/code/pk03/out/m3_endw_N3_J300_v1_7.json': '5e94d11eea2e6f55e7db781e02c197649ec6f10d8ab15a8f3508805642ed7885',
    '/mnt/g2/release/root/code/pk03/out/m3_endw_N4_J300_v1_7.json': '436a143918fa2ebaa68ee3d16fab632c27bd29b822d4c7052c92dc257eaf88af',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_3.out': '2b7847dc902eed4dda6800ff2118d8c378421179ba4d77242b83dc9086c772d9',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_4.out': 'f814f9f301f8814117dfccbd6715f8ff04e6cd24dcef04e4a95ecaaeb6e37325',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_N3.json': 'ec50ab52cd88b7b0cbd717c6dc4db295e72a8faf10b378b994a4f83cc5d7cfd4',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_N4.json': '5b7cbff9443f4ff69e623caa776646b16629aa2b6436c186e1799e9f4d56ba4c',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_2_3.out': 'ec6b099bc6517e11af92cfc641592719202bbe2dd234a2f87cce0e0a54276357',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_2_4.out': '10bc81fc53d21e3a5fff08945a1e890438145bbcee2dcc73033e7c33a37e4bb5',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_2_N3.json': '819c100913e917d09bbf7788b9dba75f15584f232784b9601e9a19e266c7f70c',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_2_N4.json': '77cb4f7c05df69c5e185ecd14aeea8fb9caca8d98e306b549390d34163f190d6',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_1_asmP.3.out': 'b6e9c2dd6a6308f6dc8d72124ba37326156983ec3444625d152ab46f28e927ed',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_1_asmP.4.out': '08c8fab3f4b9080424a40c8cb61b7932f557852520e8d49c5915092a8963a127',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_2_asmN.3.out': 'c1544e32848907c28ea30bf9e6e404fa836176947ce2f6f23e22ae4895c4697e',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_2_asmN.4.out': '66a663de3924e2d8f8af1cdd65bfd88c0edc77cca9313f4dd2ef8cfb09eac3d9',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_3_asm9.3.out': 'e7f09f7381919a8aef322adfae9ada7506bda4db527faba01b8deacdf6542655',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_3_asm9.4.out': 'a41763a35f405668c748cdd1aaccfff681aacf5fb096342a791659ccb49c07a7',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_D_N3_J300_v1_8_1.json': '8707107b0ebc3dea6989d22b6284f9df368c954837c883dc36824edda63c4926',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_D_N4_J300_v1_8_1.json': '389be198d9fe919e1a097865759691847a9e4dc7553275c083d91bd753819b00',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_E2_N3_J300_v1_8_1.json': '3e7f7bf6101bc45282a202d85e3182b2340bff4d7d349bc78eb33d5d9f02f5d5',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_E2_N4_J300_v1_8_1.json': 'e900cbfed6a8a69e57f849733d4740787c978c58761ea4f0fcffbf95293ee18e',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_E3_N3_J300_v1_8_1.json': '6cd3dffbc6fac0845d05aa4b88f135c28a8091eb9623b779d874dace550a078a',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_E3_N4_J300_v1_8_1.json': 'd1df7d4fc1b8e25f266f34c32180ccb771bc1719cc0fa730f240a33179feff0d',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_FF_N3_J300_v1_8_1.json': 'dae3cfa88bf06fd97378108b9ceba0a85044f7790b38e67c0b86eb23d6443008',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_FF_N4_J300_v1_8_1.json': '042e8fc888243ac939fb9be4968f8fc9d42262a1deb7bf690993fc22a82f2a89',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_N_N3_J300_v1_8_2.json': '87f09d3ee43e44d7572e49b40f7103d2e1ef2b7409a1cb24b67d117b4145315a',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_N_N4_J300_v1_8_2.json': '4afe8f5ba75d29cbf89f0c0940c9d7790b9a215cbf1faba6f4759d1fdd7b28d6',
    '/mnt/g2/release/root/code/pk03/out/m3_s9_N3_J300_v1_8_3.json': 'd287d3dcbd4bd988aa8061fbe11b3da1609e0ab4d27ae1a619eadcee963e8fa5',
    '/mnt/g2/release/root/code/pk03/out/m3_s9_N4_J300_v1_8_3.json': 'bcc6434c6a03eecb232f10504b63f1ce10a94a489d5a2ba9cf3fe09c8018b831',
    '/mnt/g2/release/root/code/pk24/mr_engine/kt_mr_assembly_v1_6.py': 'eb8396a2a42c46e5fe39daa5e4b30ff8bed27e933ff5f1cf781fa06382bf0958',
    '/mnt/g2/release/root/code/pk07/kt_s67_export_reader_v2_1.py': '4c6949462ca8c5dda337027b7dc5bada51102a063dc5ff6f8a1c2def01eaf49d',
    '/mnt/g2/release/root/code/pk07/kt_s9h_v1_2.py': '1b68e47141dfc5e873e2660711f6430a0badc9cc948ada32eb11641fabde4ff4',
    '/mnt/g2/release/root/code/pk07/out/export_kt_s67_cert_v2_2_sweep.kv': '6fe9ab65f5207dc3658c98ff4f3696bd2db6aa784b0dec84b33881b2da579c34',
    '/mnt/g2/release/root/code/pk07/out/export_kt_s9h_v1_2_vsweep.kv': '10f3c3d9a18b9c7a596121a8dbec7d2b82afb366704845a7c00e066c8bf6d4f6',
    '/mnt/g2/release/root/code/pk07/out/out_kt_s9h_v1_2_vsweep.out': '58814f7f59dd0d8e9d16b73084b3cc5072f94fb1138300a112e0e49ff017835f',
    '/mnt/g2/release/root/code/pk25/m3/m3_reader_s9h_v1.py': '812d1395c47e1b00bcfdbf3b17c89d030db1d98655bb9c4ab62378394f9cc0c6',
    '/mnt/g2/release/root/code/pk21/p2/s4c/MANIFEST_S4C_TIGHT_RECORD_v1_1.sha256': 'dc2523dea91213a52ede2523e222fdd2c8e0dd5263036d4d5e89be6ea1012d8e',
    '/mnt/g2/release/root/code/pk21/p2/s4c/S4C_TIGHT_RECORD_v1_1.md': '9bb4751edd928a40f6e51e1806608b4c0a2c52c37f432962888f88868b1456f6',
    '/mnt/g2/release/root/code/pk21/p2/s4c/out/tau4_kt_s9h_tau4_pk21_v1_N3.tsv': '51deea98274a63ab57df087798246c13e5fd7eb999eefe98d2fe3a10b086aea7',
    '/mnt/g2/release/root/code/pk21/p2/s4c/out/tau4_kt_s9h_tau4_pk21_v1_N4.tsv': 'b6e6588412ec6e4600547f31e0ed16cdfa310d7dea1a1bd80f00ce0eab08ad81',
    '/mnt/g2/release/root/code/pk11/out/ts_N3_S_z9sym_v1.json': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    '/mnt/g2/release/root/code/pk11/out/ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    '/mnt/g2/release/root/code/pk11/out/vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    '/mnt/g2/release/root/code/pk11/out/vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
}

if not (os.path.isdir(OUT_DIR) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUT_DIR)
        and os.path.realpath(OUT_DIR).startswith(os.path.realpath(OWN) + os.sep)):
    print('output path check failed')
    sys.exit(2)
FH = open(OUT_PATH, 'x')

# ---- CORE defs: R4's functions and class, copied by the maker in R4's order (C-CORE compares them with the pinned R4 file)
def out(line):
    FH.write(line + '\n')
    FH.flush()

def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'

class Refused(Exception):
    pass

def lines_of(path):
    with open(path) as fh:
        return fh.read().split('\n')

def gate(fails, name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'

def dec_hi(x):
    """a decimal string (17 significant digits) whose value is >= every point of the ball x."""
    u = x.upper()
    f = float(u)
    for _ in range(8):
        s = '%.16e' % f
        if arb(s).lower() >= u:
            return s
        f = math.nextafter(f, math.inf)
    raise ValueError('dec_hi')

def dec_lo(x):
    """a decimal string (17 significant digits) whose value is <= every point of the ball x."""
    lo = x.lower()
    f = float(lo)
    for _ in range(8):
        s = '%.16e' % f
        if arb(s).upper() <= lo:
            return s
        f = math.nextafter(f, -math.inf)
    raise ValueError('dec_lo')

def kv_parse(L):
    d, order = {}, []
    for x in L:
        if x == '' or x.startswith('#'):
            continue
        m = re.match(r'^([A-Z][A-Z0-9_]*) = (.*)$', x)
        if m is None:
            raise Refused('non-KV line %r' % x[:40])
        if m.group(1) in d:
            raise Refused('duplicate key %s' % m.group(1))
        d[m.group(1)] = m.group(2)
        order.append(m.group(1))
    return d, order

def read_kv(L, mode, record):
    """strict KV reader; mode CERTIFIED, MOCK or GRID (pk07's FLOAT grid export, for jlo and jhi only)."""
    d, order = kv_parse(L)
    for k in ('FORMAT', 'RECORD', 'TAG', 'EXPORT_STATUS'):
        if any(w in d.get(k, '') for w in BADWORDS):
            raise Refused('PRECERT/STUB in %s' % k)
    _mode_checks(d, mode, record)
    if d.get('RUN_VERDICT') != 'VALID':
        raise Refused('RUN_VERDICT %r' % d.get('RUN_VERDICT'))
    if not order or order[-1] != 'END' or d['END'] != record or d.get('RECORD') != record:
        raise Refused('RECORD/END')
    return d

def _mode_checks(d, mode, record):
    """the FORMAT, TAG, CLAIM and KERNEL checks of read_kv (v1_1: before RECORD/END, so that a mock is refused at its FORMAT)."""
    if mode == 'GRID':
        if d.get('FORMAT') != 'S4U_KV_v1' or record != 'EXPORT_KT_S67_v1':
            raise Refused('grid FORMAT/RECORD')
    elif mode == 'CERTIFIED':
        if d.get('FORMAT') != 'S4U_KV_v1' or not d.get('TAG', '').startswith('CERTIFIED ') or 'MOCK' in d.get('TAG', '') + d.get('EXPORT_STATUS', ''):
            raise Refused('certified FORMAT/TAG')
        if d.get('KERNEL') != KERNEL_LINE:
            raise Refused('KERNEL')
    elif mode == 'MOCK':
        if d.get('FORMAT') != 'S4U_KV_v1 MOCK' or not d.get('TAG', '').startswith('MOCK') or d.get('EXPORT_STATUS') != 'MOCK':
            raise Refused('mock FORMAT/TAG')
        if not d.get('CLAIM', '').startswith('MOCK'):
            raise Refused('claim prefix')
        if 'KERNEL' in d and d['KERNEL'] != KERNEL_LINE:
            raise Refused('KERNEL')
    else:
        raise ValueError(mode)
    return d

def _frac_ball(lo, hi):
    """the arb ball containing the exact rationals lo <= hi (fractions.Fraction)."""
    a = arb(lo.numerator) / arb(lo.denominator)
    b = arb(hi.numerator) / arb(hi.denominator)
    return a.lower().union(b.upper())

def load_m3(path, N, mode, J_REF=300, asm_out=None):
    """reader (b). Entries come back as (coefficient balls a_0..a_K, a constant bar ERR over t in [0, 1/J_REF]), as entry_ball gives them."""
    if mode == 'CERTIFIED':
        if sha_file(M3_READER_PATH) != M3_READER_SHA:
            raise Refused('m3_reader_v4_4 does not match its pin')
        import importlib.util
        spec = importlib.util.spec_from_file_location('m3_reader_v4_4', M3_READER_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            rec = mod.load(path, asm_out, int(J_REF), int(N))
        except Exception as e:
            raise Refused('m3_reader_v4_4.load: %s' % e)
        E = {}
        for key in rec['balls']:
            LO, HI, err = mod.entry_ball(rec, key)
            E[key] = ([_frac_ball(a, b) for a, b in zip(LO, HI)], (arb(err.numerator) / arb(err.denominator)).upper())
        return E
    d = read_kv(lines_of(path), 'MOCK', 'MOCK_M3_ENTRIES_v1')
    E = {}
    for k, v in d.items():
        m = re.match(r'^N%d_(M(3|4|4M)_[0-2][0-2])$' % N, k)
        if m:
            f = v.split()
            K = int(f[0])
            if len(f) != K + 3:
                raise Refused('entry %s layout' % k)
            E[m.group(1)] = ([arb(x) for x in f[1:K + 2]], arb(f[K + 2]).upper())
    if len(E) != 27 or d.get('N%d_ENTRIES' % N) != '27':
        raise Refused('entry count N=%d' % N)
    return E

def read_grid():
    d = read_kv(lines_of(GRID), 'GRID', 'EXPORT_KT_S67_v1')
    P = {}
    for N in (4, 3):
        rows = []
        for i in range(10000):
            v = d.get('N%d_P%04d' % (N, i))
            if v is None:
                break
            f = v.split('|')[0].split()
            rows.append(('%04d' % i, f[0], f[1]))
        P[N] = rows
    return P, d

def tball(jlo, jhi):
    """the piece's t range [1/jhi, 1/jlo] as a ball, its midpoint (exact) and radius (an upper bound)."""
    tl, th = t_ends(jlo, jhi)   # v1_33 (1): the hull of both readings of each end
    # v1_33 (1): t_ends takes t's upper end from the smaller J reading of jlo and t's lower end from the larger reading of jhi
    tb = tl.union(th)
    return tb, arb(tb.mid()), arb(tb.rad())

def grid_j(s, low):
    """v1_33 (1), the rule: a grid end string stands for its decimal and for its binary64 value (kt_s9h's reading); the
    smaller (low) or larger of Fraction(s) and Fraction(float(s)), exactly."""
    a, b = Fraction(s), Fraction(float(s))
    return min(a, b) if low else max(a, b)

def q2arb(f):
    """an exact Fraction as an arb ball (exact when the denominator is a power of 2, else a containing ball)."""
    return arb(f.numerator) / arb(f.denominator)

def t_ends(jlo, jhi):
    """v1_33 (1): the piece's t ends as points: t_lo from the larger reading of jhi (0 for 'inf'), t_hi from the smaller reading of jlo."""
    th = (arb(1) / q2arb(grid_j(jlo, True))).upper()
    tl = arb(0) if jhi == 'inf' else (arb(1) / q2arb(grid_j(jhi, False))).lower()
    return tl, th

def check_c1(lines):
    """v1_14 (2), C-C1: the M2B record clears C1 only if exactly one of its lines starts with 'CLAIM = ' and holds C1_CLAIM, the agreed 41-byte
    string, exactly once (the same string and length check as pk07's)."""
    if len(C1_CLAIM.encode('utf-8')) != 41:
        raise Refused('C1_CLAIM is not the agreed 41-byte string')
    cl = [ln for ln in lines if ln.startswith('CLAIM = ')]
    if len(cl) != 1 or cl[0].count(C1_CLAIM) != 1:
        raise Refused('the M2B record CLAIM does not state the |g| form exactly once (C1)')
    return True

def load_m2b(pins=None):
    """v1_25 (1), (2), the M2(b) reader: pk02's certified vacuum record M2B_KV_v1 through its one sha-pinned reader m2b_reader_v1.load, which
    binds the record to m2b_asm_v1's run output (VERDICT lines exactly [VERDICT VALID], the RECORD line naming the record's sha256), runs the
    record's own checks (allow-listed keys, FORMAT, LAW, VERDICT, CLAIM, C-MONO, C-FMT) and C-PINS with this reader's pinned sha256. The record,
    its asm output and the reader must match their pins first, the flint precision is restored after the reader's import, and check_c1 must pass
    on the record's lines (C-C1, live). Returns (rec, reader module, record lines)."""
    pins = PINS if pins is None else pins
    for p in (M2B[0], M2B[1], M2B_READER_PATH):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('M2(b) file %s does not match its pin' % os.path.basename(p))
    import importlib.util
    spec = importlib.util.spec_from_file_location('m2b_reader_v1', M2B_READER_PATH)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    try:
        rec = m2b_call(mod.load, M2B[0], M2B[1], expected_sha256=pins[M2B[0]], reader_sha256=pins[M2B_READER_PATH])
    except Exception as e:
        raise Refused('m2b_reader_v1.load: %s' % e)
    L = lines_of(M2B[0])
    check_c1(L)
    return rec, mod, L

def m2b_eps(vals):
    """v1_25 (1): (eps_r, s, s-prime = s (1 + s)) as arb balls from law_v1's decimal strings, each at or above its upper end; s-prime is the
    kt_rb form that the mock key sp holds. s = inf (2 - Rtr - eps_r not certainly positive) is refused."""
    if not isinstance(vals, dict) or vals.get('eps_r') in (None, 'inf') or vals.get('s') in (None, 'inf'):
        raise Refused('M2(b) law_v1 gave no finite eps_r and s')
    er, s = arb(vals['eps_r']), arb(vals['s'])
    if not ((er > 0) and (s > 0) and (er < 1) and (s < 1)):
        raise Refused('M2(b) eps_r and s are not inside (0, 1)')
    return er, s, s * (1 + s)

def m2b_call(fn, *args, **kw):
    """(4), the note 3 on v1_26: every call into m2b_reader_v1 runs at ctx.prec = M2B_PREC, restored afterwards, so the reader's
    balls do not depend on the assembly's precision; a call that leaves ctx.prec changed is refused."""
    p0 = ctx.prec
    ctx.prec = M2B_PREC
    try:
        r = fn(*args, **kw)
        if ctx.prec != M2B_PREC:
            raise Refused('a reader call changed ctx.prec to %d' % ctx.prec)
        return r
    finally:
        ctx.prec = p0

def load_m4(pins=None):
    """v1_32 (1): the certified M4 law record M4_KV_v1 through its one sha-pinned reader m4_reader_v1.load, which binds the record to
    m4_asm_v1's run output (VERDICT lines exactly [VERDICT VALID], one RECORD line naming the record's sha256), runs the record's own checks
    (allow-list, exact fields, forms, C-MONO, C-FMT) and C-PINS with this reader's pinned sha256. The record, its run output and the reader must
    match their pins first; flint's precision is restored after the reader's import. Returns (rec, reader module)."""
    pins = PINS if pins is None else pins
    for p in (M4[0], M4[1], M4_READER_PATH):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('M4 file %s does not match its pin' % os.path.basename(p))
    import importlib.util
    spec = importlib.util.spec_from_file_location('m4_reader_v1', M4_READER_PATH)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    try:
        rec = m4_call(mod.load, M4[0], M4[1], pins[M4[0]], pins[M4_READER_PATH])
    except Exception as e:
        raise Refused('m4_reader_v1.load: %s' % e)
    return rec, mod

def m4_call(fn, *args):
    """v1_32 (1): every call into m4_reader_v1 runs at ctx.prec = M4_PREC, restored afterwards; a call that leaves it changed is refused."""
    p0 = ctx.prec
    ctx.prec = M4_PREC
    try:
        r = fn(*args)
        if ctx.prec != M4_PREC:
            raise Refused('an M4 reader call changed ctx.prec to %d' % ctx.prec)
        return r
    finally:
        ctx.prec = p0

def m4_law(rec, mod, kind, N, jlo):
    """v1_32 (1): L_k at the piece's left end as an arb ball around m4_reader_v1.law's decimal (at or above L_k(jlo)); L_k is nonincreasing in
    J, so the ball bounds the quantity on the whole piece."""
    try:
        s = m4_call(mod.law, rec, kind, N, jlo)
    except Exception as e:
        raise Refused('m4_reader_v1.law %s N=%d at %s: %s' % (kind, N, jlo, e))
    x = arb(s)
    if not (x > 0):
        raise Refused('the M4 law %s N=%d at %s is not positive' % (kind, N, jlo))
    return x

def m2b_mhat_coeffs(asm_lines, N):
    """(1), main and the review on the lt0 clause: the trial m1, m2, m3 at N as the M2(b) record's asm output lists them in its passing C-MHAT
    line (the output that m2b_reader_v1 binds to the record), parsed exactly (a Python float repr round-trips)."""
    pre = 'C-MHAT N=%d: m1..m3 = [' % N
    L = [x for x in asm_lines if x.startswith(pre)]
    if len(L) != 1 or not L[0].rstrip().endswith('-> PASS'):
        raise Refused('the M2B asm output has no single passing C-MHAT line for N=%d' % N)
    try:
        m = [float(x) for x in L[0][len(pre):].split(']', 1)[0].split(', ')]
    except ValueError:
        raise Refused('the M2B asm output C-MHAT line for N=%d does not parse' % N)
    if len(m) != 3 or not all(x >= 0 for x in m):
        raise Refused('the M2B asm output C-MHAT line for N=%d does not hold three nonnegative m' % N)
    return m

def check_tau_trial(pins):
    """v1_34 (Point 2): H2 as a machine gate (the review 5c8dd2f3 Point 2). The sweep's run output (S67[1]) names its script on line 1 by full sha256;
    that script (S67_SCRIPT, pinned) holds TRIAL_SET with the four full sha256s, which must equal this file's pinned ts and vacres files
    (basename and full sha256, per N). The output's C-TRIAL line must name the same files with the same sha8 prefixes and read PASS, and its
    C-TRIAL chain line must read PASS. Returns True or raises Refused('C-TAU-TRIAL: ...')."""
    if pins.get(S67_SCRIPT) is None or sha_file(S67_SCRIPT) != pins[S67_SCRIPT]:
        raise Refused('C-TAU-TRIAL: the S67 producer script does not match its pin')
    L = lines_of(S67[1])
    m = re.match(r'kt_s9h_v1_2 sha256 ([0-9a-f]{64}) ', L[0]) if L else None
    if m is None or m.group(1) != pins[S67_SCRIPT]:
        raise Refused('C-TAU-TRIAL: the run output line 1 does not name the pinned script by its full sha256')
    src = lines_of(S67_SCRIPT)
    k = [i for i, x in enumerate(src) if x.startswith('TRIAL_SET = {')]
    if len(k) != 1:
        raise Refused('C-TAU-TRIAL: TRIAL_SET is not defined exactly once in the producer script')
    block = ' '.join(src[k[0]:k[0] + 4])
    got = re.findall(r"(\d): dict\(ts=\('pk11/out/([^']+)', '([0-9a-f]{64})'\),\s*vacres=\('pk11/out/([^']+)', '([0-9a-f]{64})'\)\)", block)
    want = dict((N, (os.path.basename(TS_FILES[N]), pins.get(TS_FILES[N]), os.path.basename(VACRES[N]), pins.get(VACRES[N]))) for N in (4, 3))
    if sorted(int(g[0]) for g in got) != [3, 4] or any(tuple(g[1:]) != want[int(g[0])] for g in got):
        raise Refused('C-TAU-TRIAL: kt_s9h TRIAL_SET differs from the pinned ts and vacres files')
    ct = [x for x in L if x.startswith('C-TRIAL: ')]
    toks = re.findall(r'(ts_N\d\S*?\.json|vacres_K3_N\d_sym_v1\.json):([0-9a-f]{8})', ct[0]) if len(ct) == 1 else []
    exp = [(want[4][0], (want[4][1] or '')[:8]), (want[4][2], (want[4][3] or '')[:8]), (want[3][0], (want[3][1] or '')[:8]), (want[3][2], (want[3][3] or '')[:8])]
    if len(ct) != 1 or toks != exp or ' -> PASS;' not in ct[0]:
        raise Refused('C-TAU-TRIAL: the run output C-TRIAL line does not name the pinned trial set with PASS')
    ch = [x for x in L if x.startswith('C-TRIAL chain ')]
    if len(ch) != 1 or "the script's INPUTS pin the four TRIAL_SET files by the same full sha256 -> PASS" not in ch[0]:
        raise Refused('C-TAU-TRIAL: the run output C-TRIAL chain line is missing or not PASS')
    return True

def load_ritz_mock(L, N):
    """v1_27 (1): MOCK_RITZ_ENTRIES_v1 lines L at N as {key: (coefficient balls, bar)}; strict KV with the MOCK FORMAT, TAG and CLAIM; exactly
    the 18 S9 keys."""
    d = read_kv(L, 'MOCK', 'MOCK_RITZ_ENTRIES_v1')
    E = {}
    for k, v in d.items():
        m = re.match(r'^N%d_(G|T)_([013])_([013])$' % N, k)
        n = re.match(r'^N%d_(IHT|DX)_([013])$' % N, k)
        if m:
            name = '%s,%s,%s' % m.groups()
        elif n:
            name = '%s,%s' % ({'IHT': 'Iht', 'DX': 'Dx'}[n.group(1)], n.group(2))
        else:
            continue
        f = v.split()
        K = int(f[0])
        if K < 3 or len(f) != K + 3:
            raise Refused('mock Ritz entry %s layout' % k)
        E[name] = ([arb(x) for x in f[1:K + 2]], arb(f[K + 2]).upper())
    if d.get('N%d_ENTRIES' % N) != '18' or sorted(E) != sorted(RITZ_KEYS):
        raise Refused('mock Ritz entries at N=%d are not the 18 S9 keys' % N)
    return E

def check_s9_trial(r9, N, pins=None):
    """v1_27 (1): an S9 record's trial_set must name the pinned ts and vacres files in pk03's form basename:<full sha256>."""
    pins = PINS if pins is None else pins
    ts = r9.get('trial_set') if isinstance(r9, dict) else None
    for k, p in (('ts', TS_FILES[N]), ('vacres', VACRES[N])):
        want = '%s:%s' % (os.path.basename(p), pins.get(p) or '')
        if pins.get(p) is None or not isinstance(ts, dict) or ts.get(k) != want:
            raise Refused('S9 record trial_set %s is not the pinned %s' % (k, os.path.basename(p)))
    return True

def load_ritz(N, mode, path=None, asm_out=None, pins=None):
    """v1_27 (1): the 18 S9 entries of N as {key: (coefficient balls a_0..a_K, bar)} over t in [0, 1/300] (J_REF 300). CERTIFIED: pk03's
    S9 record and its asm output, both pinned by full sha256 (S9_RECORDS), through m3_reader_v4_4 (load_m3), then check_s9_trial; a KV file
    (a MOCK copy) is refused at read_kv's CERTIFIED FORMAT/TAG check before any value is read; refused while no S9 record is pinned.
    MOCK: MOCK_RITZ_ENTRIES_v1."""
    pins = PINS if pins is None else pins
    if mode == 'CERTIFIED':
        if path is None:
            if N not in S9_RECORDS:
                raise Refused('no S9 record pinned for N=%d yet' % N)
            path, asm_out = S9_RECORDS[N]
        for p in (path, asm_out):
            if p is None or pins.get(p) is None or sha_file(p) != pins[p]:
                raise Refused('S9 file %s does not match its pin' % os.path.basename(str(p)))
        if not path.endswith('.json'):
            read_kv(lines_of(path), 'CERTIFIED', 'S9_RECORD')
            raise Refused('an S9 record is an M3 json record')
        E = load_m3(path, N, 'CERTIFIED', 300, asm_out)
        with open(path) as fh:
            check_s9_trial(json.load(fh), N, pins)
    elif mode == 'MOCK':
        E = load_ritz_mock(lines_of(M_RITZ if path is None else path), N)
    else:
        raise ValueError(mode)
    miss = [k for k in RITZ_KEYS if k not in E]
    if miss:
        raise Refused('S9 entries missing at N=%d: %s' % (N, ' '.join(miss)))
    extra = sorted(k for k in E if k not in RITZ_KEYS)   # v1_30 (1), the review 4: the S9 record holds exactly the 18 keys
    if extra:
        raise Refused('S9 entries beyond the 18 keys at N=%d: %s' % (N, ' '.join(extra)))
    return dict((k, E[k]) for k in RITZ_KEYS)

def entry_piece(e, tb):
    """v1_27 (1): an entry over the piece: sum_k a_k t^k on the piece's t-ball tb plus the constant bar (the direct form, NOTE sect. 4)."""
    ak, err = e
    s = arb(0)
    for a in reversed(ak):
        s = s * tb + a
    return s + err * arb(0, 1)

def mhat_ball(m, tb):
    """v1_27 (1): mhat(t) = 1 + m1 t + m2 t^2 + m3 t^3 on the piece's t-ball tb, from exact binary64 m (the M2(b) record's m1..m3)."""
    a = [arb(x) for x in m]
    return 1 + a[0] * tb + a[1] * tb * tb + a[2] * tb * tb * tb

def _min_pt(a, b):
    return a if a < b else b

def _jacobi3(A):
    """v1_27 (1): float Jacobi on a symmetric 3 x 3 list matrix: eigenvalue and eigenvector guesses only (kt_rb_v1_5's jacobi in binary64)."""
    n = 3
    A = [row[:] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(100):
        if sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j) < 1e-30:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if A[p][q] == 0:
                    continue
                th = (A[q][q] - A[p][p]) / (2 * A[p][q])
                tt = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(tt * tt + 1)
                s = tt * c
                for k in range(n):
                    x, y = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * x - s * y, s * x + c * y
                for k in range(n):
                    x, y = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * x - s * y, s * x + c * y
                for k in range(n):
                    x, y = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * x - s * y, s * x + c * y
    return [A[i][i] for i in range(n)], V

def ritz_piece(B, mh, vecmode='PD'):
    """v1_27 (1): kt_rb_v1_5's ritz_cert (l.567-675) in arb on one piece's entry balls B (NOTE_P2_17_RITZ_PIECES_v1 sect. 4): interval Cholesky
    of the 3 x 3 Gram block (refused unless certainly positive definite), X = L^-1, C = X T X^T symmetrized by averaging (both enclose the true
    value), float Jacobi guesses on C's midpoint, residuals in arb, Weyl with rF = ||C - mid C||_F, disjoint enclosures, Davis-Kahan vector
    bars (the angle at most pi/2 times its sine), c_k = X^T v_k with c_k[k] > 0, and the amplitude balls t^_k = mhat (c_k . Iht)/(G00^(1/2)
    lambda_0^2) and a^_k = mhat (c_k . Dx)/(G00^(1/2) lambda_0) (Iht, the top-row bond, in place of kt_rb's Ih). C-GAP refusals: overlapping
    enclosures, no gap, an undetermined vector sign."""
    n = 3
    G = [[B['G,%d,%d' % (min(b, c), max(b, c))] for c in REVEN] for b in REVEN]
    T = [[B['T,%d,%d' % (min(b, c), max(b, c))] for c in REVEN] for b in REVEN]
    Iht = [B['Iht,%d' % b] for b in REVEN]
    Dx = [B['Dx,%d' % b] for b in REVEN]
    L = [[arb(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = G[i][j]
            for k in range(j):
                s = s - L[i][k] * L[j][k]
            if i == j:
                if not (s > 0):
                    raise Refused('interval Gram block not positive definite')
                L[i][i] = s.sqrt()
            else:
                L[i][j] = s / L[j][j]
    X = [[arb(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        X[i][i] = 1 / L[i][i]
        for j in range(i):
            s = arb(0)
            for k in range(j, i):
                s = s + L[i][k] * X[k][j]
            X[i][j] = -s / L[i][i]
    XT = [[sum((X[i][k] * T[k][j] for k in range(n)), arb(0)) for j in range(n)] for i in range(n)]
    C = [[sum((XT[i][k] * X[j][k] for k in range(n)), arb(0)) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i):
            C[i][j] = C[j][i] = (C[i][j] + C[j][i]) / 2
    Cm = [[float(C[i][j].mid()) for j in range(n)] for i in range(n)]
    rf2 = arb(0)
    for i in range(n):
        for j in range(n):
            d = abs(C[i][j] - arb(Cm[i][j])).upper()
            rf2 = rf2 + d * d
    rF = rf2.sqrt().upper()
    lam, Q = _jacobi3(Cm)
    order = sorted(range(n), key=lambda k: -lam[k])
    lamo, res, vec = [], [], []
    for k in order:
        v = [Q[i][k] for i in range(n)]
        r2, nv2 = arb(0), arb(0)
        for i in range(n):
            ri = sum((arb(Cm[i][j]) * arb(v[j]) for j in range(n)), arb(0)) - arb(lam[k]) * arb(v[i])
            r2 = r2 + abs(ri).upper() * abs(ri).upper()   # v1_30 (2): the upper end of |r_ki| squared
            nv2 = nv2 + arb(v[i]) * arb(v[i])
        lamo.append(lam[k])
        res.append((r2.sqrt() / nv2.sqrt()).upper())
        vec.append(v)
    one = arb(0, 1)
    encl = [arb(lamo[k]) + one * (res[k] + rF) for k in range(n)]
    cme = [arb(lamo[k]) + one * res[k] for k in range(n)]
    for k in range(n - 1):
        if not ((cme[k].lower() > cme[k + 1].upper()) and (encl[k].lower() > encl[k + 1].upper())):
            raise Refused('eigenvalue enclosures overlap (C-GAP)')
    vecs, dmin = [], None
    for k in range(n):
        g = None
        for j in range(n):
            if j != k:
                x = (abs(arb(lamo[k]) - arb(lamo[j])) - res[k] - res[j]).lower()
                g = x if g is None else _min_pt(g, x)
        d = (g - rF).lower()
        dmin = d if dmin is None else _min_pt(dmin, d)
        if not ((g > 0) and (d > 0)):
            raise Refused('no eigenvalue gap (C-GAP)')
        eps = (arb.pi() / 2 * (res[k] / g + rF / d)).upper()
        vecs.append([arb(x) + one * eps for x in vec[k]])
    if vecmode == 'PD':   # v1_28 (1): the per-direction bound (NOTE_P2_17_RITZ_PD_v1) in place of the uniform bar above
        vecs = pd_dk_meet(pd_vectors(C, vec, lamo, res, rF), vecs)   # v1_30 (3): the smaller of PD and DK per component
    elif vecmode != 'DK':
        raise ValueError(vecmode)
    cvecs = []
    for rank in range(n):
        vk = vecs[rank]
        c = [sum((X[j][i] * vk[j] for j in range(n)), arb(0)) for i in range(n)]
        if c[rank].upper() < 0:
            c = [-x for x in c]
        elif not (c[rank].lower() > 0):
            raise Refused('sign of a Ritz vector not determined (C-GAP)')
        cvecs.append(c)
    l0 = encl[0]
    sg0 = G[0][0].sqrt()

    def amp(c, w, p):
        s = sum((c[i] * w[i] for i in range(n)), arb(0))
        den = sg0
        for _ in range(p):
            den = den * l0
        return mh * s / den
    return dict(vals=encl, vecs=cvecs, C=C, vec=vec, lamo=lamo, t=[amp(cvecs[k], Iht, 2) for k in range(n)], a=[amp(cvecs[k], Dx, 1) for k in range(n)],
                rF=rF, res=res, dmin=dmin, G=G, Iht0=Iht[0], Dx0=Dx[0])

def lemma_a_cbar(RC, eps_r, Rb12, tau_r, tau_abs=None, plant=None):
    """v1_27 (1): kt_rb_v1_5's assembly_cert l.711-746 in arb on one piece: c-bar from the residual ratios Rb = (eps_r/(1 - eps_r), R_e1, R_e3),
    Weyl on the block form of S and Kato-Temple at the top (refused unless both denominators are positive: C-KT; and C-SX), then
    q = c-bar/(s_x,low - tau), eps_0 and eps_y. tau = TAU_R mu_y,high when tau_abs is None (kt_rb's form, C-LA300 only), else tau = tau_abs =
    rho_hi (the port's rows, v1_33 (3)). v1_34: eps_y = rho_y q/(s_x,low - mu_y,high) ((a)); C-KT0 gates m0lo's denominator (); plant='KT0'
    is PLANT-KT0's hook (s_x,high replaced by 1 - 1.5 c-bar in that denominator only)."""
    vals, G, V = RC['vals'], RC['G'], RC['vecs']
    s_x, mu_y = vals[1] / vals[0], vals[2] / vals[0]
    tau = arb(tau_r) * mu_y.upper() if tau_abs is None else tau_abs   # v1_33 (3): the crude certified tau (rho_hi) on the port's rows
    Rb = [eps_r / (1 - eps_r), Rb12[0], Rb12[1]]
    rho = []
    for k in range(3):
        acc = arb(0)
        for b in range(3):
            acc = acc + abs(V[k][b]).upper() * G[b][b].sqrt().upper() * Rb[b]
        rho.append(acc)
    cbar = (rho[0] * rho[0] + rho[1] * rho[1] + rho[2] * rho[2]).sqrt()
    ylev = mu_y.upper() if (tau_abs is None or mu_y.upper() > tau.upper()) else tau.upper()   # v1_33 (3): max(mu_y, tau), no r_tau < 1
    syhi = ylev + cbar
    gap_x = _min_pt((1 - s_x.upper()).lower(), (s_x.lower() - syhi).lower())
    if not (gap_x > 0):
        raise Refused('C-KT: no gap around s_x')
    s_xlo = (s_x.lower() - cbar * cbar / gap_x).lower()
    kt0 = 1 - cbar - ((s_x.upper() if plant != 'KT0' else 1 - 3 * cbar / 2) + cbar)   # v1_34: m0lo's denominator, the same arb expression
    if not (kt0 > 0):
        raise Refused('C-KT0: 1 - 2 c-bar - s_x,high (the m0lo denominator) is not certainly positive')
    m0lo = 1 - rho[0] * rho[0] / kt0
    sx_mm = s_x.lower() * m0lo
    g_below = s_xlo - syhi
    if not (g_below > 0):
        raise Refused('C-KT: s_x,low - s_y,high not positive')
    sxhi = s_x.upper() + cbar * cbar / g_below
    den0 = m0lo - sxhi
    if not (den0 > 0):
        raise Refused('C-KT: Kato-Temple denominator not positive')
    if not (s_xlo.upper() <= sx_mm.lower()):
        raise Refused('C-SX: s_x,low above the min-max bound')
    q = cbar / (s_xlo - tau)
    return dict(s_x=s_x, mu_y=mu_y, tau=tau, rho=rho, cbar=cbar, s_xlo=s_xlo, syhi=syhi, sxhi=sxhi, den0=den0, kt0=kt0, m0lo=m0lo, g_below=g_below, q=q, eps0=rho[0] * q / den0,
                epsy=rho[2] * q / (s_xlo - mu_y.upper()))

def pd_vectors(C, vec, lamo, res, rF, gap_scale=1):
    """v1_28 (1), NOTE_P2_17_RITZ_PD_v1: the per-direction Ritz vectors. For every symmetric A in the ball C and its unit eigenvectors v_k (sign
    u_k . v_k > 0): (lambda_k - lam~_j) u_j . v_k = r_j . v_k with r_j = A u_j - lam~_j u_j, so |u_j . v_k| <= R_j/g_kj for j != k, where R_j is
    the arb upper end of ||C u_j - lam~_j u_j|| (it bounds ||r_j(A)|| over the ball) and g_kj = |lam~_k - lam~_j| - res_k - rF bounds
    |lambda_k(A) - lam~_j| from below (Weyl plus the disjoint residual intervals; refused unless positive). With M = U^T U, beta = U^T v_k,
    beta^T M^-1 beta = 1 gives u_k . v_k. Returns the v_k as arb vectors in C's basis, in the order of lamo. gap_scale (PLANT-PD-GAP only)
    multiplies the gap bounds."""
    n = 3
    one = arb(0, 1)
    U = [[arb(x) for x in vec[j]] for j in range(n)]
    R = []
    for j in range(n):
        rr = arb(0)
        for i in range(n):
            ri = abs(sum((C[i][l] * U[j][l] for l in range(n)), arb(0)) - arb(lamo[j]) * U[j][i]).upper()   # v1_29: the upper end of |r_ji|
            rr = rr + ri * ri
        R.append(rr.sqrt().upper())
    Mi = arb_mat(n, n, [sum((U[i][l] * U[j][l] for l in range(n)), arb(0)) for i in range(n) for j in range(n)]).inv()
    vk_all = []
    for k in range(n):
        beta = [None] * n
        for j in range(n):
            if j != k:
                g = ((abs(arb(lamo[k]) - arb(lamo[j])) - res[k] - rF) * gap_scale).lower()
                if not (g > 0):
                    raise Refused('per-direction bound: no gap between lambda_%d and lam~_%d' % (k, j))
                beta[j] = one * (R[j] / g).upper()
        bk = one * sum((U[k][l] * U[k][l] for l in range(n)), arb(0)).sqrt().upper()
        cross = arb(0)
        for i in range(n):
            for j in range(n):
                if (i, j) != (k, k):
                    cross = cross + (bk if i == k else beta[i]) * Mi[i, j] * (bk if j == k else beta[j])
        qk = (1 - cross) / Mi[k, k]
        if not (qk > 0):
            raise Refused('per-direction bound: the u_%d component is not certainly positive' % k)
        beta[k] = qk.sqrt()
        alpha = [sum((Mi[i, j] * beta[j] for j in range(n)), arb(0)) for i in range(n)]
        vk_all.append([sum((alpha[j] * U[j][i] for j in range(n)), arb(0)) for i in range(n)])
    return vk_all

def pd_dk_meet(pd, dk):
    """v1_30 (3), the per-direction condition 3: the componentwise intersection of the per-direction and the uniform Davis-Kahan Ritz
    vectors, both of which hold v_k with u_k . v_k > 0; an empty intersection is refused."""
    out_v = []
    for k in range(3):
        row = []
        for i in range(3):
            a, b = pd[k][i], dk[k][i]
            lo = a.lower() if a.lower() > b.lower() else b.lower()
            hi = a.upper() if a.upper() < b.upper() else b.upper()
            if not (lo <= hi):
                raise Refused('the PD and DK bounds of v_%d[%d] do not meet' % (k, i))
            row.append(lo.union(hi))
        out_v.append(row)
    return out_v

def plant(nofire, name, fn):
    """a must-fire plant: fn must raise Refused (a refusal by the reader under test)."""
    try:
        fn()
    except Refused as e:
        out('%s: refused (%s) -> FIRES' % (name, e))
        return
    except Exception as e:
        out('%s: raised %r instead of a refusal -> DOES NOT FIRE' % (name, e))
        nofire.append(name)
        return
    out('%s: accepted -> DOES NOT FIRE' % name)
    nofire.append(name)

# ---- pk25's code


def segments(src):
    """the module-level function and class sources (by name) and assignment sources (by the comma-joined target names) of a Python text."""
    tree = ast.parse(src)
    segs, dup = {}, []
    for node in tree.body:
        key = None
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            key = node.name
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            t = node.targets[0]
            names = [t.id] if isinstance(t, ast.Name) else [x.id for x in t.elts] if isinstance(t, ast.Tuple) and all(isinstance(x, ast.Name) for x in t.elts) else None
            if names:
                key = '=' + ','.join(names)
        if key is not None:
            if key in segs:
                dup.append(key)
            segs[key] = ast.get_source_segment(src, node)
    return segs, dup


def check_core(tamper=None):
    """C-CORE: every name in CORE_DEFS and CORE_CONSTS is defined exactly once in R4 and in this file, with the same source text. tamper
    (PLANT-CORE) changes one character of this file's copy of the first def before the comparison."""
    if sha_file(R4_PATH) != R4_SHA:
        raise Refused('C-CORE: R4 does not match its pin')
    r4, d4 = segments(open(R4_PATH).read())
    me, dm = segments(open(SELF).read())
    if tamper:
        k0 = CORE_DEFS[0]
        me = dict(me, **{k0: me[k0].replace('(', '[', 1)})
    keys = list(CORE_DEFS) + ['=' + c for c in CORE_CONSTS]
    bad = [k for k in keys if k in d4 or k in dm or r4.get(k) is None or me.get(k) != r4.get(k)]
    if bad:
        raise Refused('C-CORE: %d of %d copies differ from R4 or are defined twice: %s' % (len(bad), len(keys), ' '.join(bad[:6])))
    return len(CORE_DEFS), len(CORE_CONSTS)


def check_pins_r4(pins):
    """C-PINS-R4: every file pinned here and in R4's PINS has the same pin in both."""
    tree = ast.parse(open(R4_PATH).read())
    r4p = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'PINS':
            r4p = ast.literal_eval(node.value)
    if not isinstance(r4p, dict):
        raise Refused('C-PINS-R4: no PINS literal in R4')
    shared = sorted(set(pins) & set(r4p))
    bad = [os.path.basename(p) for p in shared if pins[p] != r4p[p]]
    if bad or len(shared) < 20:
        raise Refused('C-PINS-R4: %d shared pins, differing: %s' % (len(shared), ' '.join(bad)))
    return len(shared)


def check_engine_fields():
    """C-ENGINE-FIELDS: the M1 engine's MR_SPECTRAL FIELDS and ORIENT, read from the pinned engine file by ast, equal this file's."""
    tree = ast.parse(open(MR_ENGINE).read())
    got = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('FIELDS', 'ORIENT'):
            got[node.targets[0].id] = ast.literal_eval(node.value)
    if got.get('ORIENT') != ORIENT or not isinstance(got.get('FIELDS'), dict) or got['FIELDS'].get('MR_SPECTRAL') != SPEC_FIELDS:
        raise Refused('C-ENGINE-FIELDS: the M1 engine\'s MR_SPECTRAL FIELDS or ORIENT differ')
    return True


def check_grid(P):
    """C-GRID: R4's grid per N runs contiguously (token equality of jhi and the next jlo) from a piece that holds J_low to inf; returns the
    index of the J_low piece."""
    first = {}
    for N in (4, 3):
        rows = P[N]
        for (i0, a0, b0), (i1, a1, b1) in zip(rows, rows[1:]):
            if int(i1) != int(i0) + 1 or b0 != a1:
                raise Refused('C-GRID: N=%d pieces %s, %s do not chain' % (N, i0, i1))
        if rows[-1][2] != 'inf':
            raise Refused('C-GRID: N=%d grid does not end at inf' % N)
        hit = [k for k, (i, a, b) in enumerate(rows) if grid_j(a, True) <= JLOW[N] and (b == 'inf' or JLOW[N] < grid_j(b, False))]
        if len(hit) != 1:
            raise Refused('C-GRID: N=%d: %d pieces hold J_low' % (N, len(hit)))
        first[N] = hit[0]
    return first


def load_sv(P, pins=None, plant=None):
    """the S_V export's rho1_hi, Rw_hi and rho_hi per piece (R4's load_tau pattern): pins, check_tau_trial, kt_s67_export_reader_v2_1.load
    (rule V2), the grid index for index with the same doubles, and each field's token on the export's own line equal to the reader's value
    (C-SV-COPY). Returns {N: {idx: {field: (Fraction, token)}}}. plant='GRID' (PLANT-SV-GRID) moves one N = 4 grid end by 1e-12."""
    pins = PINS if pins is None else pins
    for p in (S67[0], S67[1], S67_READER_PATH):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('C-SV-READ: S67 file %s does not match its pin' % os.path.basename(p))
    check_tau_trial(pins)
    import importlib.util
    spec = importlib.util.spec_from_file_location('kt_s67_export_reader_v2_1', S67_READER_PATH)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    try:
        ex = mod.load(S67[0], S67[1])
    except Exception as e:
        raise Refused('C-SV-READ: kt_s67_export_reader_v2_1.load: %s' % e)
    names = ('rho1_hi', 'Rw_hi', 'rho_hi')
    if any(f not in ex['fields'] for f in names):
        raise Refused('C-SV-READ: the S_V export lacks one of %s' % ' '.join(names))
    fi = dict((f, ex['fields'].index(f)) for f in names)
    lab = {}
    for x in lines_of(S67[0]):
        mm = re.match(r'N([34])_P([0-9]{4}) = (.*)$', x)
        if mm:
            lab[(int(mm.group(1)), int(mm.group(2)))] = mm.group(3).partition(' | ')[0].split(' ')
    res = {}
    for N in (4, 3):
        pcs = ex['pieces'].get(N, {})
        rows = P[N]
        if plant == 'GRID' and N == 4:
            rows = [r if i != 7 else (r[0], repr(float(r[1]) * (1 + 1e-12)), r[2]) for i, r in enumerate(rows)]
        if len(pcs) != len(rows):
            raise Refused('C-SV-READ: the S_V export has %d pieces at N=%d, the grid %d' % (len(pcs), N, len(rows)))
        res[N] = {}
        for i, (idx, jlo, jhi) in enumerate(rows):
            e = pcs[i]
            if e['jlo'] != float(jlo) or e['jhi'] != (math.inf if jhi == 'inf' else float(jhi)):
                raise Refused('C-SV-READ: the S_V grid differs at N=%d piece %s' % (N, idx))
            tk = lab.get((N, i))
            if tk is None or len(tk) != len(ex['fields']):
                raise Refused('C-SV-COPY: no export line N%d_P%04d of the expected length' % (N, i))
            d = {}
            for f in names:
                v, tok = e[f], tk[fi[f]]
                if not re.fullmatch(DEC_RE, tok) or Fraction(tok) != v or not (v > 0):
                    raise Refused('C-SV-COPY: N=%d piece %s field %s token %s is not the reader\'s positive value' % (N, idx, f, tok))
                d[f] = (v, tok)
            res[N][idx] = d
    return res


DEC_RE = r'-?[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?'


def read_tau4(P, SV, claim_text=None):
    """C-TAU4: tau4 per N from S4(c) v1_1's Claim line (copied by tool, exactly one match), the record and both TSVs pinned and listed in the
    record's manifest with the same sha256; the TSVs on R4's grid (float equality of the ends), no NONE row, the claim at least every row's
    tau4_hi raised by two binary64 steps (the TSV prints the 83-bit upper end rounded to nearest), and each row's rho_hi within 1e-11
    relative of the S_V export's rho_hi (the export rounds the same upper end up at 12 significant digits), so that the rows are the same
    pieces. Returns {N: token}. claim_text (PLANT-TAU4-LOW) replaces the record's text."""
    for p in (S4C_RECORD, S4C_MANIFEST, TAU4_TSV[4], TAU4_TSV[3]):
        if PINS.get(p) is None or sha_file(p) != PINS[p]:
            raise Refused('C-TAU4: %s does not match its pin' % os.path.basename(p))
    txt = open(S4C_RECORD).read() if claim_text is None else claim_text
    m = re.findall(r'tau_4\(4\) = ([0-9]+\.[0-9]+),\s+tau_4\(3\) = ([0-9]+\.[0-9]+),', txt)
    if len(m) != 1:
        raise Refused('C-TAU4: the claim line of the S4(c) record does not match exactly once')
    tok = {4: m[0][0], 3: m[0][1]}
    man = {}
    for ln in lines_of(S4C_MANIFEST):
        if ln.strip():
            h, p = ln.split(None, 1)
            man[p.strip()] = h
    if man.get('p2/s4c/S4C_TIGHT_RECORD_v1_1.md') != PINS[S4C_RECORD] or any(
            man.get('p2/s4c/out/' + os.path.basename(TAU4_TSV[N])) != PINS[TAU4_TSV[N]] for N in (4, 3)):
        raise Refused('C-TAU4: the S4(c) manifest does not list the pinned record and TSVs')
    for N in (4, 3):
        L = [x for x in lines_of(TAU4_TSV[N]) if x]
        if L[0] != 'jlo\tjhi\trho2_hi\tmuz_lo\tlam0_lo\ttau4_hi\trho_hi' or len(L) - 1 != len(P[N]):
            raise Refused('C-TAU4: N=%d TSV header or row count' % N)
        mx = Fraction(0)
        for (idx, jlo, jhi), ln in zip(P[N], L[1:]):
            r = ln.split('\t')
            if len(r) != 7 or float(r[0]) != float(jlo) or (r[1] != 'inf' if jhi == 'inf' else (r[1] == 'inf' or float(r[1]) != float(jhi))):
                raise Refused('C-TAU4: N=%d TSV row of piece %s is off the grid' % (N, idx))
            if r[5] == 'NONE':
                raise Refused('C-TAU4: N=%d piece %s has no tau4' % (N, idx))
            mx = max(mx, Fraction(math.nextafter(math.nextafter(float(r[5]), math.inf), math.inf)))
            tv, sv = Fraction(float(r[6])), SV[N][idx]['rho_hi'][0]
            if not (abs(sv - tv) <= tv / 10 ** 11):
                raise Refused('C-TAU4: N=%d piece %s: the TSV rho_hi is not the S_V export\'s (12 digits)' % (N, idx))
        if not (Fraction(tok[N]) >= mx):
            raise Refused('C-TAU4: N=%d claim %s below the TSV maximum %.17g' % (N, tok[N], float(mx)))
    return tok


def load_e2ff(N, pins=None, plant=None):
    """S8's E2 (e,0, e,1, e,3) and FF (z) records of N through R4's load_m3 (m3_reader_v4_4, bound to the asmP output pinned in R4), with
    check_s9_trial on the records' trial_set, the graphs (E2, mix) and (FF, free2), J_REF 300, N, and the claim prefix G00_CLAIM.
    plant='TRIAL' (PLANT-E2-TRIAL) changes the E2 record's ts name in memory."""
    pins = PINS if pins is None else pins
    res = {}
    for nm, (path, asm), keys, graph in (('E2', E2REC[N], ('e,0', 'e,1', 'e,3'), ('E2', 'mix')), ('FF', FFREC[N], ('z',), ('FF', 'free2'))):
        for p in (path, asm):
            if pins.get(p) is None or sha_file(p) != pins[p]:
                raise Refused('C-E2FF-READ: %s does not match its pin' % os.path.basename(p))
        with open(path) as fh:
            js = json.load(fh)
        if plant == 'TRIAL' and nm == 'E2':
            js = dict(js, trial_set=dict(js.get('trial_set', {}), ts='x' + str(js.get('trial_set', {}).get('ts'))))
        check_s9_trial(js, N, pins)
        if (js.get('graph'), js.get('graph_m3')) != graph or js.get('J_REF') != 300 or js.get('N') != N:
            raise Refused('C-E2FF-READ: %s N=%d graph, J_REF or N' % (nm, N))
        if not str(js.get('claim', '')).startswith(G00_CLAIM):
            raise Refused('C-E2FF-READ: %s N=%d claim' % (nm, N))
        E = load_m3(path, N, 'CERTIFIED', 300, asm)
        if any(k not in E for k in keys):
            raise Refused('C-E2FF-READ: %s N=%d lacks %s' % (nm, N, ' '.join(keys)))
        res[nm] = dict((k, E[k]) for k in keys)
    return res


def r_main_arb(N, swap=False):
    """r_main = (sqrt(det L_D det L_free)/det L_mix)^(N - 1) by the matrix-tree theorem in arb (pk07's r_main_iv, kt_s9h_v1_2 l.4937):
    the reduced Laplacians of the three 2-column graphs, triangle conductances A_EX = (3 + sqrt 21)/6, B_EX = (3 sqrt 5 - sqrt 21)/12, unit
    verticals and horizontals. swap exchanges the two conductances (PLANT-RMAIN)."""
    a_ = (3 + arb(21).sqrt()) / 6
    b_ = (3 * arb(5).sqrt() - arb(21).sqrt()) / 12
    if swap:
        a_, b_ = b_, a_

    def det_red(edges):
        L = [[arb(0) for _ in range(6)] for _ in range(6)]
        for (u, v), cc in edges:
            L[u][u] = L[u][u] + cc
            L[v][v] = L[v][v] + cc
            L[u][v] = L[u][v] - cc
            L[v][u] = L[v][u] - cc
        return arb_mat(5, 5, [L[i][j] for i in range(1, 6) for j in range(1, 6)]).det()
    tri = lambda o: [((o, o + 1), a_), ((o + 1, o + 2), a_), ((o, o + 2), b_)]
    ver = lambda o: [((o, o + 1), arb(1)), ((o + 1, o + 2), arb(1))]
    hor = [((r, 3 + r), arb(1)) for r in range(3)]
    tD, tmix, tfree = det_red(tri(0) + tri(3) + hor), det_red(tri(0) + ver(3) + hor), det_red(ver(0) + ver(3) + hor)
    return ((tD * tfree).sqrt() / tmix) ** (N - 1)


def check_rmain(N, swap=False):
    """C-RMAIN: r_main_arb lies inside pk03's endw record [r_main_lo, r_main_hi] (an independent computation)."""
    if PINS.get(ENDW[N]) is None or sha_file(ENDW[N]) != PINS[ENDW[N]]:
        raise Refused('C-RMAIN: the endw record does not match its pin')
    with open(ENDW[N]) as fh:
        js = json.load(fh)
    rm = r_main_arb(N, swap)
    lo, hi = Fraction(js['r_main_lo']), Fraction(js['r_main_hi'])
    if not (js.get('N') == N and q2arb(lo) <= rm.lower() and rm.upper() <= q2arb(hi)):
        raise Refused('C-RMAIN: N=%d r_main %s is not inside the endw record\'s [%r, %r]' % (N, rm.str(20), js['r_main_lo'], js['r_main_hi']))
    return rm


def cmin(x):
    """the least |y| over the ball x (0 if the ball holds 0), as an exact point."""
    if x.lower() <= 0 <= x.upper():
        return arb(0)
    return abs(x.lower()) if x.lower() > 0 else abs(x.upper())


def l3_level(a, rho, s_lo, s_hi, mu_lo, mu_hi, tau):
    """L3 at level a (0, 1, 2 for 0, x, y): (q_a, {k: eps_ka}, D_a, g_a, {k: g_ka}) or Refused('C-L3-FP: ...')."""
    ga = (s_lo[a] - tau).lower()
    if not (ga > 0):
        raise Refused('C-L3-FP: g_%s = s_%s,lo - tau4 is not positive' % (KNAME[a], KNAME[a]))
    gk = {}
    for k in range(3):
        if k != a:
            gk[k] = ((mu_lo[k] - s_hi[a]) if k < a else (s_lo[a] - mu_hi[k])).lower()
            if not (gk[k] > 0):
                raise Refused('C-L3-FP: the gap g_%s%s is not positive' % (KNAME[k], KNAME[a]))
    D = (1 - sum((rho[k] * rho[k] / (ga * gk[k]) for k in gk), arb(0))).lower()
    if not (D > 0):
        raise Refused('C-L3-FP: D_%s is not positive' % KNAME[a])
    q = (rho[a] / ga / D).upper()
    eps = dict((k, (rho[k] * q / gk[k]).upper()) for k in gk)
    return q, eps, D, ga, gk


def lemma_a(a, L3, A, Qw):
    """Lemma A at level a for w-hat: the bound on |<u_a, w-hat> - A~_a| (an exact point, rounded up)."""
    q, eps = L3[a][0], L3[a][1]
    d = q * Qw + sum((eps[k] * abs(A[k]).upper() for k in eps), arb(0)) + (q * q + sum((eps[k] * eps[k] for k in eps), arb(0))) * abs(A[a]).upper()
    return d.upper()


def orient_signs(N, pins=None):
    """the orientation (P0_LOG line 4089): the trial set's S matrix (pinned TS_FILES[N]) and the signs (sign S[3][1], sign S[1][3]) that
    turn R4's stored-state orientation into u_x along e1 = xi_TB - (N - 1)/sqrt 5 and u_y along e3 (S[3][1] is stored state 1's xi_TB
    coefficient, S[1][3] stored state 3's xi_TM coefficient); refused unless both have modulus above 1."""
    pins = PINS if pins is None else pins
    p = TS_FILES[N]
    if pins.get(p) is None or sha_file(p) != pins[p]:
        raise Refused('C-ORIENT: the trial set of N=%d does not match its pin' % N)
    with open(p) as fh:
        S = json.load(fh)['S']
    n1, n3 = Fraction(S[3][1]), Fraction(S[1][3])
    if not (abs(n1) > 1 and abs(n3) > 1):
        raise Refused('C-ORIENT: N=%d: |S[3][1]| or |S[1][3]| is not above 1' % N)
    return S, (1 if n1 > 0 else -1, 1 if n3 > 0 else -1)


def check_orient(V, G, S):
    """C-ORIENT after the flip: the xi_TB coefficient of u~_x and the xi_TM coefficient of u~_y from the harmonic states 1 and 3,
    sum_(b in 1, 3) c_kb S[3 or 1][b], certainly positive; u~_0's coefficient on psi-hat and <u~_0, psi-hat/|psi-hat|> certainly positive."""
    cx = sum((V[1][i] * arb(S[3][REVEN[i]]) for i in (1, 2)), arb(0))
    cy = sum((V[2][i] * arb(S[1][REVEN[i]]) for i in (1, 2)), arb(0))
    ip0 = sum((V[0][i] * G[i][0] for i in range(3)), arb(0)) / G[0][0].sqrt()
    if not (cx > 0 and cy > 0 and V[0][0] > 0 and ip0 > 0):
        raise Refused('C-ORIENT: after the flip u~_x is not along e1, u~_y not along e3, or u~_0 not along psi-hat')
    return True


def load_rdr(pins=None):
    """v3: pk25's reader fork m3_reader_s9h_v1 (pinned), imported once (C6b's load_rdr)."""
    pins = PINS if pins is None else pins
    if pins.get(RDR) is None or sha_file(RDR) != pins[RDR]:
        raise Refused('C-LAW-READ: the reader fork does not match its pin')
    import importlib.util
    spec = importlib.util.spec_from_file_location('m3_reader_s9h_v1', RDR)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    return mod


def load_laws_c6a(RD, N, pins=None):
    """v3: the records and law certificates the Ritz problem and c(-1) take, through the reader fork: S8's D, E2, E3, FF (certificate
    m3_lawcert_v1_1) and S8's N (v1_2); every record and job output pinned, check_s9_trial on every record. Returns {family: (record,
    certificate)} (C6b's load_laws without pk25's h records)."""
    pins = PINS if pins is None else pins
    out_ = {}
    for fams, cp, co in ((('D', 'E2', 'E3', 'FF'),) + S8CERT[N]['v1_1'], (('N',),) + S8CERT[N]['v1_2']):
        recs = {}
        for F in fams:
            rp, ap = S8REC[N][F]
            for p in (rp, ap):
                if pins.get(p) is None or sha_file(p) != pins[p]:
                    raise Refused('C-LAW-READ: %s does not match its pin' % os.path.basename(p))
            with open(rp) as fh:
                check_s9_trial(json.load(fh), N, pins)
            try:
                recs[F] = RD.load(rp, ap, 300, N)
            except Exception as e:
                raise Refused('C-LAW-READ: load %s: %s' % (os.path.basename(rp), e))
        for p in (cp, co):
            if pins.get(p) is None or sha_file(p) != pins[p]:
                raise Refused('C-LAW-READ: %s does not match its pin' % os.path.basename(p))
        try:
            cert = RD.load_lawcert(cp, co, 300, N, recs)
        except Exception as e:
            raise Refused('C-LAW-READ: load_lawcert %s: %s' % (os.path.basename(cp), e))
        for F in fams:
            out_[F] = (recs[F], cert)
    return out_


def chi2_tail(n, s):
    """Prob(chi^2_n > s) for n = 2 (e^(-s/2)) and n = 3 (erfc(sqrt(s/2)) + sqrt(2 s/pi) e^(-s/2)), as arb balls."""
    if n == 2:
        return (-s / 2).exp()
    if n == 3:
        return (s / 2).sqrt().erfc() + (2 * s / arb.pi()).sqrt() * (-s / 2).exp()
    raise Refused('chi2_tail: n = %r' % n)


def law_err(E, J):
    """LAWCERT_CLAIM's right side without the ak_rad term, at J >= 300 (an arb upper value): rem (300/J)^4 + tail (P(J)/P(300))^1/2 + ann
    (P(J)/P(300))^1/2 + far e^(-far_rate (J - 300)), the P-ratios with P(J) at its upper end over P(300) at its lower end."""
    if E.get('laws') is None:
        return arb(0)
    L, parts = E['laws'], E['parts']
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    j0 = arb(300)
    J = q2arb(J) if isinstance(J, Fraction) else (J if isinstance(J, arb) else arb(J))
    if not (J >= j0):
        raise Refused('law_err: J below J_REF')
    tot = q(parts['rem']) * (j0 / J) ** 4
    for part in ('tail', 'ann'):
        g = L[part]
        P = lambda JJ: sum((chi2_tail(g['n'], JJ * q(a) / q(G)) for a, G in g['a_G']), arb(0))
        r = P(J).upper() / P(j0).lower()
        tot = tot + q(parts[part]) * r.sqrt()
    tot = tot + q(parts['far']) * (-q(L['far_rate']) * (J - j0)).exp()
    return tot.upper()


def entry_law_piece(E, tb, t_hi, J_lo):
    """an entry over the piece by LAWCERT_CLAIM's form: sum_k ak[k] t^k on the t-ball plus [-r, r], r = sum_k ak_rad[k] t_hi^k + law_err(J_lo)."""
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    s = arb(0)
    for a in reversed(E['ak']):
        s = s * tb + q(a)
    r = law_err(E, J_lo)
    tp = arb(1)
    for ar in E['ak_rad']:
        r = r + q(ar) * tp
        tp = tp * t_hi
    return s + r.upper() * arb(0, 1)


def law_bp(IN, N, tb, t_hi, J_lo):
    """v3: the 18 RITZ_KEYS balls on the piece with law-based bars: G,b,c from S8 D's g,b,c, T,b,c from S8 N's T,b,c and Dx,b from S8 D's
    DY,b (the S9 entries' aliases, C-ALIAS) by entry_law_piece; Iht,b stays the S9 record's (entry_piece), since only ritz_piece's t
    amplitudes take it and no row uses them."""
    LW, RD = IN['LW'][N], IN['RD']
    B = {}
    for k in RITZ_KEYS:
        fam, key = k.split(',', 1)
        if fam == 'Iht':
            B[k] = entry_piece(IN['RE'][N][k], tb)
            continue
        F, kk = {'G': ('D', 'g,'), 'T': ('N', 'T,'), 'Dx': ('D', 'DY,')}[fam]
        B[k] = entry_law_piece(RD.entry_law(LW[F][1], F, kk + key), tb, t_hi, J_lo)
    return B


def law_e2ff(IN, N, tb, t_hi, J_lo):
    """v3: E2's e,b (b in REVEN) and FF's z on the piece with law-based bars (m3_lawcert_v1_1)."""
    LW, RD = IN['LW'][N], IN['RD']
    e = [entry_law_piece(RD.entry_law(LW['E2'][1], 'E2', 'e,%d' % b), tb, t_hi, J_lo) for b in REVEN]
    z = entry_law_piece(RD.entry_law(LW['FF'][1], 'FF', 'z'), tb, t_hi, J_lo)
    return e, z


def check_alias3(IN, tamper=False):
    """C-ALIAS (v3): the law certificates' midpoints ak lie in the records' coefficient balls, entry by entry: G, T and Dx against the S9
    records (load_ritz; S8 D's g and DY and S8 N's T are the S9 entries' aliases), E2's e,b and FF's z against the S8 records (load_e2ff), at
    both N. tamper (PLANT-ALIAS) moves the first ak of N = 4 by 1e-6."""
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    bad = []
    for N in (4, 3):
        cd, cn = IN['LW'][N]['D'][1], IN['LW'][N]['N'][1]
        pairs = []
        for k in RITZ_KEYS:
            fam, key = k.split(',', 1)
            if fam == 'Iht':
                continue
            F, kk = {'G': ('D', 'g,'), 'T': ('N', 'T,'), 'Dx': ('D', 'DY,')}[fam]
            pairs.append(('N%d %s' % (N, k), cn if F == 'N' else cd, F, kk + key, IN['RE'][N][k][0]))
        for b in REVEN:
            pairs.append(('N%d E2 e,%d' % (N, b), cd, 'E2', 'e,%d' % b, IN['E2'][N]['E2']['e,%d' % b][0]))
        pairs.append(('N%d FF z' % N, cd, 'FF', 'z', IN['E2'][N]['FF']['z'][0]))
        for j, (lab, cert, F, kk, mine) in enumerate(pairs):
            ent = cert['entries'].get('%s:%s' % (F, kk))
            if ent is None:
                bad.append(lab + ' (missing)')
                continue
            ak = [q(a) for a in ent['ak']]
            if tamper and N == 4 and j == 0:
                ak[0] = ak[0] + arb('1e-6')
            if len(ak) != len(mine) or any(not (a.lower() >= m.lower() - arb('1e-30') and a.upper() <= m.upper() + arb('1e-30'))
                                           for a, m in zip(ak, mine)):
                bad.append(lab)
    if bad:
        raise Refused('C-ALIAS: %d entries differ from the records: %s' % (len(bad), ' '.join(bad[:6])))
    return True


class Iv(object):
    """an exact closed interval [lo, hi] with arb points as ends, offering an arb ball's lower(), upper() and mid(): the intersected fields
    keep their exact ends, since an arb radius has a 30-bit mantissa and a ball rebuilt from the ends can be wider than either input."""

    def __init__(self, lo, hi):
        self.lo, self.hi = lo, hi

    def lower(self):
        return self.lo

    def upper(self):
        return self.hi

    def mid(self):
        return (self.lo + self.hi) / 2


def isect(a, b, what):
    """the intersection of two certified enclosures (arb balls) of one quantity, [the larger lower end, the smaller upper end], as an exact
    interval Iv; C-COMBINE refuses an empty one."""
    lo = a.lower() if a.lower() > b.lower() else b.lower()
    hi = a.upper() if a.upper() < b.upper() else b.upper()
    if not (lo <= hi):
        raise Refused('C-COMBINE: the record and law enclosures of %s do not meet' % what)
    return Iv(lo, hi)


def lmax(a, b):
    """the larger of two lower bounds (exact points)."""
    return a if a > b else b


def umin(a, b):
    """the smaller of two upper bounds (exact points)."""
    return a if a < b else b


def combine(Dr, Dl):
    """v3: a piece's written quantities from the record computation Dr (v2's, byte for byte) and the law computation Dl: the s, mu and c(-1)
    enclosures and the unit-basis coefficients intersected, rho, L_k and L3's q and eps the smaller upper bounds (both computations bound the
    same exact quantities, so each intersection is certified); RC, LA, A, Qw, Dl, sv, tau_hi, er, Rb12 from Dl (the INFO lines and the float
    twin)."""
    D = dict(Dl)
    D['s_lo'] = [arb(1)] + [lmax(Dr['s_lo'][i], Dl['s_lo'][i]) for i in (1, 2)]
    D['s_hi'] = [arb(1)] + [umin(Dr['s_hi'][i], Dl['s_hi'][i]) for i in (1, 2)]
    D['mu_lo'] = [lmax(Dr['mu_lo'][i], Dl['mu_lo'][i]) for i in range(3)]
    D['mu_hi'] = [Dl['mu_hi'][0]] + [umin(Dr['mu_hi'][i], Dl['mu_hi'][i]) for i in (1, 2)]
    D['rho'] = [umin(Dr['rho'][i], Dl['rho'][i]) for i in range(3)]
    D['Lk'] = [umin(Dr['Lk'][i], Dl['Lk'][i]) for i in range(3)]
    L3 = {}
    for a in range(3):
        qr, er_ = Dr['L3'][a][0], Dr['L3'][a][1]
        ql, el_ = Dl['L3'][a][0], Dl['L3'][a][1]
        L3[a] = (umin(qr.upper(), ql.upper()), dict((k, umin(er_[k].upper(), el_[k].upper())) for k in el_)) + tuple(Dl['L3'][a][2:])
    D['L3'] = L3
    D['uhat'] = [[isect(Dr['uhat'][k][i], Dl['uhat'][k][i], 'u%s%s' % (KNAME[k], BNAME[i])) for i in range(3)] for k in range(3)]
    D['cx'] = isect(Dr['cx'], Dl['cx'], 'c_x(-1)')
    D['cy'] = isect(Dr['cy'], Dl['cy'], 'c_y(-1)')
    for i in (1, 2):
        if not (D['s_lo'][i] < D['s_hi'][i] and D['mu_lo'][i] < D['mu_hi'][i]):
            raise Refused('C-COMBINE: the s or mu enclosures do not meet')
    wid = lambda x: (x.upper() - x.lower()).upper()
    D['wr'] = (float((wid(D['uhat'][1][2]) / wid(Dr['uhat'][1][2])).upper()), float(((D['s_hi'][2] - D['s_lo'][2]) / (Dr['s_hi'][2] - Dr['s_lo'][2])).upper()))
    return D


def piece_both(N, idx, jlo, jhi, IN, plant=None):
    """v3: piece_compute with the records' entries (v2's computation) and with the law certificates, combined field by field (combine)."""
    Dr = piece_compute(N, idx, jlo, jhi, IN, plant, 'rec')
    Dl = piece_compute(N, idx, jlo, jhi, IN, plant, 'law')
    return combine(Dr, Dl)


def piece_compute(N, idx, jlo, jhi, IN, plant=None, src='rec'):
    """one piece: the Ritz problem, S-unit bounds, L3, Lemma P, the unit-basis coefficients, c_x(-1) and c_y(-1), the S_V tokens; the
    per-piece gates raise Refused. Plants: L3GAP (tau4 raised to s_y,lo at level y), LKGAP (tau4 raised to mu_y,lo in L_y), ORIENT (u~_x
    negated), RW (R_w times 0.9). v3: src 'rec' takes the S9 records' entries and S8's E2, FF balls (v2's computation byte for byte),
    src 'law' the law certificates (law_bp, law_e2ff)."""
    tb, _tm, _r = tball(jlo, jhi)
    JL = grid_j(jlo, True)
    Rb12 = (m4_law(IN['M4REC'], IN['M4MOD'], 'e1', N, JL), m4_law(IN['M4REC'], IN['M4MOD'], 'e3', N, JL))
    Bp = law_bp(IN, N, tb, t_ends(jlo, jhi)[1], JL) if src == 'law' else dict((k, entry_piece(IN['RE'][N][k], tb)) for k in RITZ_KEYS)
    mh = mhat_ball(IN['MC'][N], tb)
    er, _s, _sp = m2b_eps(m2b_call(IN['M2MOD'].law_v1, IN['M2R'], N, JL))
    RC = ritz_piece(Bp, mh)
    tau = IN['TAU4A'][N]
    LA = lemma_a_cbar(RC, er, Rb12, None, tau)
    tau_hi = tau.upper()
    s_x, mu_y, m0lo = LA['s_x'], LA['mu_y'], LA['m0lo'].lower()
    mu_lo = [m0lo, (s_x.lower() * m0lo).lower(), (mu_y.lower() * m0lo).lower()]
    mu_hi = [arb(1), s_x.upper(), mu_y.upper()]
    s_lo = [arb(1), mu_lo[1], mu_lo[2]]
    s_hi = [arb(1), LA['sxhi'].upper(), LA['syhi'].upper()]
    rho = [r.upper() for r in LA['rho']]
    if not (s_lo[2] < s_hi[2] and s_hi[2] < s_lo[1] and s_lo[1] < s_hi[1] and s_hi[1] < mu_lo[0]):
        raise Refused('C-ORDER: s_y,lo < s_y,hi < s_x,lo < s_x,hi < mu_0,lo does not hold')
    if not (tau_hi < s_lo[2]):
        raise Refused('C-TAU-SY: tau4 is not below s_y,lo')
    L3 = {}
    for a in range(3):
        L3[a] = l3_level(a, rho, s_lo, s_hi, mu_lo, mu_hi, s_lo[2] if (plant == 'L3GAP' and a == 2) else tau_hi)
    Lk = []
    for k in range(3):
        den = (mu_lo[k] - (mu_lo[2] if (plant == 'LKGAP' and k == 2) else tau_hi)).lower()
        if not (den > 0):
            raise Refused('C-LK-GAP: mu_%s,lo - tau4 is not positive' % KNAME[k])
        Lk.append((rho[k] / den).upper())
    G = RC['G']
    sx_, sy_ = IN['SIG'][N]
    V = [RC['vecs'][0], [x if sx_ == 1 else -x for x in RC['vecs'][1]], [x if sy_ == 1 else -x for x in RC['vecs'][2]]]   # exact negation, no radius change
    if plant == 'ORIENT':
        V = [V[0], [-x for x in V[1]], V[2]]
    uhat = [[V[k][i] * G[i][i].sqrt() for i in range(3)] for k in range(3)]
    check_orient(V, G, IN['TS'][N])
    if src == 'law':
        e, z = law_e2ff(IN, N, tb, t_ends(jlo, jhi)[1], JL)
    else:
        e = [entry_piece(IN['E2'][N]['E2']['e,%d' % b], tb) for b in REVEN]
        z = entry_piece(IN['E2'][N]['FF']['z'], tb)
    A = [sum((V[k][i] * e[i] for i in range(3)), arb(0)) for k in range(3)]
    Q2 = z / IN['RMAIN'][N] - (A[0] * A[0] + A[1] * A[1] + A[2] * A[2])
    if not (Q2.upper() >= 0):
        raise Refused('C-QW: |w-hat|^2 - |Pi_W w-hat|^2 is certainly negative')
    Qw = Q2.upper().sqrt().upper() if Q2.upper() > 0 else arb(0)
    Dl = [lemma_a(a, L3, A, Qw) for a in range(3)]
    one = arb(0, 1)
    den = A[0] + Dl[0] * one
    if not (den > 0):
        raise Refused('C-DEN: <u, w-hat> is not certainly positive')
    cx = (A[1] + Dl[1] * one) / den
    cy = (A[2] + Dl[2] * one) / den
    sv = IN['SV'][N][idx]
    Rw = q2arb(sv['Rw_hi'][0]) * (arb('0.9') if plant == 'RW' else 1)
    if cmin(cx) * cmin(cx) + cmin(cy) * cmin(cy) > Rw * Rw:
        raise Refused('C-RW: c_x(-1)^2 + c_y(-1)^2 exceeds R_w^2 (Parseval)')
    return dict(RC=RC, LA=LA, s_lo=s_lo, s_hi=s_hi, mu_lo=mu_lo, mu_hi=mu_hi, rho=rho, L3=L3, Lk=Lk, uhat=uhat, A=A, Qw=Qw, Dl=Dl, cx=cx,
                cy=cy, sv=sv, tau_hi=tau_hi, er=er, Rb12=Rb12)


def rows_of(N, idx, jlo, jhi, D, tok):
    """the MR_SPECTRAL and MR_LEMMAP rows of one piece (decimal strings; L_k from the written decimals, exactly)."""
    t4 = tok[N]
    spec = [jlo, jhi, dec_lo(D['s_lo'][1]), dec_hi(D['s_hi'][1]), dec_lo(D['s_lo'][2]), dec_hi(D['s_hi'][2]), t4,
            D['sv']['rho1_hi'][1], D['sv']['Rw_hi'][1], dec_lo(D['cx']), dec_hi(D['cx']), dec_lo(D['cy']), dec_hi(D['cy'])]
    rh = [dec_hi(D['rho'][k]) for k in range(3)]
    ml = [dec_lo(D['mu_lo'][k]) for k in range(3)]
    Ls = [dec_hi(arb(rh[k]) / (arb(ml[k]) - arb(t4))) for k in range(3)]
    co = []
    for k in range(3):
        for i in range(3):
            co += [dec_lo(D['uhat'][k][i]), dec_hi(D['uhat'][k][i])]
    L3 = D['L3']
    qe = [dec_hi(L3[0][0]), dec_hi(L3[1][0]), dec_hi(L3[2][0]),
          dec_hi(L3[0][1][1]), dec_hi(L3[0][1][2]), dec_hi(L3[1][1][0]), dec_hi(L3[1][1][2]), dec_hi(L3[2][1][0]), dec_hi(L3[2][1][1])]
    return spec, [jlo, jhi] + rh + ml + [t4] + Ls + co + qe


def x0y0():
    return (7 - 3 * arb(5).sqrt()) / 2, (23 - 5 * arb(21).sqrt()) / 2


def inside(v, lo, hi):
    """v (a ball) certainly inside [lo, hi] (exact points)."""
    return lo < v and v < hi


def cx0_sign_check(IN, N):
    """C-CX0-SIGN: the E2 record's t^0 coefficients of e,1 and e,3 have certain signs, and those signs times the orientation signs of
    orient_signs are +1: at t = 0 the Ritz vectors are the harmonic trial states, so in the canonical orientation c_x(-1) and c_y(-1) are
    positive at t = 0, as KC4's t^0 values are."""
    sx_, sy_ = IN['SIG'][N]
    for k, s_ in (('e,1', sx_), ('e,3', sy_)):
        a0 = IN['E2'][N]['E2'][k][0][0]
        if not ((a0 > 0 and s_ == 1) or (a0 < 0 and s_ == -1)):
            raise Refused('C-CX0-SIGN: N=%d: the t^0 sign of %s times the orientation sign is not +1' % (N, k))
    return True


def check_exact_last(N, D, plant=None):
    """C-S0 and CX0 on the last piece (t = 0 in its t range): x0 and y0 inside the s and mu intervals; +x0 ((N - 1)/2)^(1/2) inside c_x(-1)
    and +y0 ((N - 1)/2)^(1/2) inside c_y(-1) (KC4's t^0 values, the exact harmonic values, in the canonical orientation).
    Plants: S0 (x0 times 1 + 1e-3), CXSWAP (c_x and c_y exchanged)."""
    x0, y0 = x0y0()
    if plant == 'S0':
        x0 = x0 * (1 + arb('1e-3'))
    if not (inside(x0, D['s_lo'][1], D['s_hi'][1]) and inside(y0, D['s_lo'][2], D['s_hi'][2])
            and inside(x0, D['mu_lo'][1], D['mu_hi'][1]) and inside(y0, D['mu_lo'][2], D['mu_hi'][2])):
        raise Refused('C-S0: x0 or y0 is not inside the last piece\'s s or mu interval')
    f = arb(N - 1) / 2
    cx, cy = (D['cy'], D['cx']) if plant == 'CXSWAP' else (D['cx'], D['cy'])
    if not (inside(x0 * f.sqrt(), cx.lower(), cx.upper()) and inside(y0 * f.sqrt(), cy.lower(), cy.upper())):
        raise Refused('CX0: c_x(-1) or c_y(-1) on the last piece does not hold its exact t = 0 value')
    return True


def f2_twin(N, jlo, jhi, IN, D, plant=None):
    """C-F2: a float twin at one t of the piece (the midpoint of its t range; t = 0 on the last piece): scipy.linalg.eigh(T, G) on the entry
    midpoints, the Ritz vectors G-normalised, oriented by c_kk > 0 and then by orient_signs, A~_k from the E2 midpoints. Its ratios mu_x/mu_0, mu_y/mu_0, its
    unit-basis coefficients and its Ritz-level c_x(-1) = A~_x/A~_0, c_y(-1) = A~_y/A~_0 must lie inside this piece's arb balls (R4's ratio
    balls, uhat and the c(-1) intervals). plant='F2' raises the float s_x by 1e-3 relative."""
    import numpy as np
    from scipy.linalg import eigh
    tl, th = t_ends(jlo, jhi)
    t = 0.0 if jhi == 'inf' else float(((tl + th) / 2).mid())
    f = lambda ent: sum(float(a.mid()) * t ** k for k, a in enumerate(ent[0]))
    G = np.array([[f(IN['RE'][N]['G,%d,%d' % (min(b, c), max(b, c))]) for c in REVEN] for b in REVEN])
    T = np.array([[f(IN['RE'][N]['T,%d,%d' % (min(b, c), max(b, c))]) for c in REVEN] for b in REVEN])
    w, Vv = eigh(T, G)
    order = [2, 1, 0]
    C = []
    for k, i in enumerate(order):
        c = Vv[:, i] / math.sqrt(float(Vv[:, i] @ G @ Vv[:, i]))
        C.append((c if c[k] > 0 else -c) * (1, IN['SIG'][N][0], IN['SIG'][N][1])[k])
    e = np.array([f(IN['E2'][N]['E2']['e,%d' % b]) for b in REVEN])
    A = [float(c @ e) for c in C]
    sx = w[order[1]] / w[order[0]] * (1 + (1e-3 if plant == 'F2' else 0))
    sy = w[order[2]] / w[order[0]]
    LA = D['LA']
    bad = []
    if not (LA['s_x'].lower() <= arb(sx) <= LA['s_x'].upper()):
        bad.append('s_x')
    if not (LA['mu_y'].lower() <= arb(sy) <= LA['mu_y'].upper()):
        bad.append('s_y')
    for k in range(3):
        for i in range(3):
            u = D['uhat'][k][i]
            if not (u.lower() <= arb(float(C[k][i]) * math.sqrt(G[i][i])) <= u.upper()):
                bad.append('u%s%s' % (KNAME[k], BNAME[i]))
    for nm, v, ball in (('c_x', A[1] / A[0], D['cx']), ('c_y', A[2] / A[0], D['cy'])):
        if not (ball.lower() <= arb(v) <= ball.upper()):
            bad.append(nm)
    if bad:
        raise Refused('C-F2: N=%d at t %.6e: float values outside the arb balls: %s' % (N, t, ' '.join(bad)))
    return t, sx, sy, A[1] / A[0], A[2] / A[0]


def kv_text(record, fmt, fields, rows, extra):
    """a record's text: header (FORMAT, RECORD, PRODUCER, CODE, STATUS, EXPORT_STATUS, RUN_VERDICT, SOURCE, J_UNIFORMITY, ORIENTATION, the
    extra lines), FIELDS, then one row per piece, 'N<N>_P<idx4> = values'."""
    cert = MODE == 'cert'
    head = ['# %s (pk25, %s %s): written by %s' % (record, LABEL, MODE, LABEL),
            'FORMAT = %s' % fmt, 'RECORD = %s' % record, 'PRODUCER = pk25 %s' % LABEL,
            'CODE = pk25/asm/%s.py:%s' % (LABEL, sha_file(SELF)), 'STATUS = %s' % ('CERTIFIED' if cert else 'DRY'),
            'EXPORT_STATUS = %s' % ('CERTIFIED' if cert else 'DRY'), 'RUN_VERDICT = VALID', 'SOURCE = %s' % SOURCE_LINE,
            'J_UNIFORMITY = %s' % J_UNIF, 'ORIENTATION = %s' % ORIENT,
            'TRIAL_SET = N4 %s:%s, N3 %s:%s (psi-hat and the stored states 1, 3 of the S9 records per N; u_x and u_y lie along the canonical e1, e3: '
            'the stored-state coefficients are flipped where S[3][1] or S[1][3] is negative)' % (
                os.path.basename(TS_FILES[4]), PINS[TS_FILES[4]], os.path.basename(TS_FILES[3]), PINS[TS_FILES[3]])] + extra + ['FIELDS = %s' % fields]
    return '\n'.join(head + ['%s = %s' % (k, ' '.join(v)) for k, v in rows]) + '\n'


def readback(text, fmt, record, fields, rows, tamper=False):
    """C-WRITE on a record text: the M1 engine's kv_read rules (header keys until FIELDS, no repeated keys, every line with '='), FORMAT,
    RECORD, ORIENTATION, PRODUCER's first word pk25, FIELDS, the rows equal to the in-memory rows, keys on R4's grid, finite decimals,
    *_lo <= *_hi, single *_hi >= 0, single *_lo > 0 (MR_LEMMAP's mu_k,lo). tamper (PLANT-WRITE) changes the first row's third value."""
    from decimal import Decimal as Dm
    if tamper:
        k0, v0 = rows[0]
        text = text.replace('%s = %s' % (k0, ' '.join(v0)), '%s = %s' % (k0, ' '.join(v0[:2] + ['9' + v0[2]] + v0[3:])), 1)
    head, got, flds = {}, [], None
    for ln in text.splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        if '=' not in ln:
            raise Refused('C-WRITE: a line without "="')
        k, v = [x.strip() for x in ln.split('=', 1)]
        if k == 'FIELDS':
            flds = v.split()
        elif flds is None:
            if k in head:
                raise Refused('C-WRITE: repeated header key %s' % k)
            head[k] = v
        else:
            got.append((k, v.split()))
    if (head.get('FORMAT'), head.get('RECORD'), head.get('ORIENTATION')) != (fmt, record, ORIENT) or head.get('PRODUCER', '').split()[:1] != ['pk25']:
        raise Refused('C-WRITE: %s header' % record)
    if flds != fields.split() or got != [(k, list(v)) for k, v in rows] or len(set(k for k, _ in got)) != len(got):
        raise Refused('C-WRITE: %s FIELDS or rows differ from memory' % record)
    for k, vals in got:
        row = dict(zip(flds, vals))
        for f, v in row.items():
            if f in ('jlo', 'jhi'):
                continue
            if not re.fullmatch(DEC_RE, v) or not Dm(v).is_finite():
                raise Refused('C-WRITE: %s row %s field %s = %s' % (record, k, f, v))
        for f in row:
            if f.endswith('_lo') and (f[:-3] + '_hi') in row and Dm(row[f]) > Dm(row[f[:-3] + '_hi']):
                raise Refused('C-WRITE: %s row %s has %s > %s_hi' % (record, k, f, f[:-3]))
            if f.endswith('_lo') and (f[:-3] + '_hi') not in row and not (Dm(row[f]) > 0):
                raise Refused('C-WRITE: %s row %s has the single lower bound %s <= 0' % (record, k, f))
            if f.endswith('_hi') and (f[:-3] + '_lo') not in row and Dm(row[f]) < 0:
                raise Refused('C-WRITE: %s row %s has %s < 0' % (record, k, f))
    return len(got)


def main():
    t0 = time.time()
    fails, nofire, EXEC = [], [], []

    def run_plant(name, fn):
        EXEC.append(name)
        plant(nofire, name, fn)
    out('%s sha256 %s MODE=%s TAG=%s' % (LABEL, sha_file(SELF), MODE, TAG))
    bad = ['%s %s' % (os.path.basename(p), sha_file(p)[:8]) for p in sorted(PINS) if sha_file(p) != PINS[p]]
    out('C-HASH %s (%d pinned files)%s' % ('PASS' if not bad else 'FAIL', len(PINS), (': ' + '; '.join(bad)) if bad else ''))
    if bad:
        out('VERDICT INVALID (C-HASH)')
        return 2
    try:
        nd, nc = check_core()
        out('C-CORE PASS: %d defs and %d constants equal R4 (%s) byte for byte, each defined once' % (nd, nc, R4_SHA[:8]))
    except Refused as e:
        out('C-CORE FAIL: %s' % e)
        out('VERDICT INVALID (C-CORE)')
        return 2
    run_plant('PLANT-CORE', lambda: check_core(tamper=True))
    try:
        ns = check_pins_r4(PINS)
        out('C-PINS-R4 PASS: %d files pinned here and in R4 carry the same sha256' % ns)
    except Refused as e:
        out('C-PINS-R4 FAIL: %s' % e)
        out('VERDICT INVALID (C-PINS-R4)')
        return 2
    run_plant('PLANT-PINS-R4', lambda: check_pins_r4(dict(PINS, **{M2B[0]: '0' * 64})))

    def flag(fn):
        try:
            fn()
            return True
        except Refused as e:
            out('  refused: %s' % e)
            return False
    out('C-ENGINE-FIELDS: MR_SPECTRAL FIELDS and ORIENT equal those of %s (%s) -> %s' % (
        os.path.basename(MR_ENGINE), PINS[MR_ENGINE][:8], gate(fails, 'C-ENGINE-FIELDS', flag(check_engine_fields))))
    P, _gd = read_grid()
    try:
        FIRST = check_grid(P)
        gok = True
    except Refused as e:
        out('  refused: %s' % e)
        FIRST, gok = {4: 0, 3: 0}, False
    out('C-GRID: R4\'s grid %s (%s): N=4 %d pieces, the J = 350 piece %s; N=3 %d pieces, the J = 300 piece %s; contiguous to inf -> %s' % (
        os.path.basename(GRID), PINS[GRID][:8], len(P[4]), P[4][FIRST[4]][0], len(P[3]), P[3][FIRST[3]][0], gate(fails, 'C-GRID', gok)))
    if not gok:
        out('VERDICT INVALID (C-GRID)')
        return 2
    IN = {}
    IN['RE'] = dict((N, load_ritz(N, 'CERTIFIED')) for N in (4, 3))
    out('C-RITZ-READ: the S9 records (N4 %s, N3 %s) through m3_reader_v4_4 (%s) give the 18 keys at both N, trial sets pinned -> %s' % (
        PINS[S9_RECORDS[4][0]][:8], PINS[S9_RECORDS[3][0]][:8], M3_READER_SHA[:8], gate(fails, 'C-RITZ-READ', all(sorted(IN['RE'][N]) == sorted(RITZ_KEYS) for N in (4, 3)))))
    run_plant('PLANT-RITZ-S9-PIN', lambda: load_ritz(4, 'CERTIFIED', pins=dict(PINS, **{S9_RECORDS[4][0]: '0' * 64})))
    IN['M2R'], IN['M2MOD'], _m2l = load_m2b()
    IN['MC'] = dict((N, m2b_mhat_coeffs(lines_of(M2B[1]), N)) for N in (4, 3))
    out('C-M2B-READ: %s (%s) through m2b_reader_v1 (%s), C-C1 inside; m1..m3 from its asm output N4 %s, N3 %s -> %s' % (
        os.path.basename(M2B[0]), PINS[M2B[0]][:8], PINS[M2B_READER_PATH][:8], IN['MC'][4], IN['MC'][3], gate(fails, 'C-M2B-READ', True)))
    run_plant('PLANT-M2B-PIN', lambda: load_m2b(dict(PINS, **{M2B[0]: '0' * 64})))
    IN['M4REC'], IN['M4MOD'] = load_m4()
    out('C-M4-READ: %s (%s) through m4_reader_v1 (%s) -> %s' % (os.path.basename(M4[0]), PINS[M4[0]][:8], PINS[M4_READER_PATH][:8], gate(fails, 'C-M4-READ', True)))
    run_plant('PLANT-M4-PIN', lambda: load_m4(dict(PINS, **{M4[0]: '0' * 64})))
    IN['SV'] = load_sv(P)
    out('C-SV-READ: %s (%s) through kt_s67_export_reader_v2_1 (%s): rule V2, the grid index for index, rho1_hi, Rw_hi, rho_hi tokens equal '
        'to the reader\'s values (C-SV-COPY) -> %s' % (os.path.basename(S67[0]), PINS[S67[0]][:8], PINS[S67_READER_PATH][:8], gate(fails, 'C-SV-READ', True)))
    out('C-TAU-TRIAL: the S_V run output names %s (%s) and its TRIAL_SET equals the pinned ts and vacres files -> %s' % (
        os.path.basename(S67_SCRIPT), PINS[S67_SCRIPT][:8], gate(fails, 'C-TAU-TRIAL', flag(lambda: check_tau_trial(PINS)))))
    run_plant('PLANT-SV-PIN', lambda: load_sv(P, dict(PINS, **{S67[0]: '0' * 64})))
    run_plant('PLANT-SV-GRID', lambda: load_sv(P, plant='GRID'))
    IN['E2'] = dict((N, load_e2ff(N)) for N in (4, 3))
    out('C-E2FF-READ: E2 (N4 %s, N3 %s) and FF (N4 %s, N3 %s) through m3_reader_v4_4, bound to the asmP outputs (%s, %s); trial sets, graphs '
        '(E2, mix) and (FF, free2), J_REF 300, the claim prefix -> %s' % (
            PINS[E2REC[4][0]][:8], PINS[E2REC[3][0]][:8], PINS[FFREC[4][0]][:8], PINS[FFREC[3][0]][:8], PINS[E2REC[4][1]][:8], PINS[E2REC[3][1]][:8],
            gate(fails, 'C-E2FF-READ', True)))
    run_plant('PLANT-E2-PIN', lambda: load_e2ff(4, dict(PINS, **{E2REC[4][0]: '0' * 64})))
    run_plant('PLANT-E2-TRIAL', lambda: load_e2ff(4, plant='TRIAL'))
    try:
        IN['RD'] = load_rdr()
        IN['LW'] = dict((N, load_laws_c6a(IN['RD'], N)) for N in (4, 3))
        lok = True
    except Refused as e:
        out('  refused: %s' % e)
        lok = False
    out('C-LAW-READ: S8 D, E2, E3, FF with m3_lawcert_v1_1 and S8 N with m3_lawcert_v1_2 (N4 %s %s, N3 %s %s) through m3_reader_s9h_v1 (%s), '
        'records bound to their asm outputs, trial sets as pinned -> %s' % (
            PINS[S8CERT[4]['v1_1'][0]][:8], PINS[S8CERT[4]['v1_2'][0]][:8], PINS[S8CERT[3]['v1_1'][0]][:8], PINS[S8CERT[3]['v1_2'][0]][:8],
            PINS[RDR][:8], gate(fails, 'C-LAW-READ', lok)))
    if lok:
        run_plant('PLANT-LAW-PIN', lambda: load_laws_c6a(IN['RD'], 4, dict(PINS, **{S8CERT[4]['v1_1'][0]: '0' * 64})))
        out('C-ALIAS: the law certificates\' ak lie in the records\' coefficient balls for G, T, Dx (S9 records) and E2 e,0 e,1 e,3, FF z '
            '(S8 records), both N -> %s' % gate(fails, 'C-ALIAS', flag(lambda: check_alias3(IN))))
        run_plant('PLANT-ALIAS', lambda: check_alias3(IN, tamper=True))
    try:
        TOK = read_tau4(P, IN['SV'])
        tok_ok = True
    except Refused as e:
        out('  refused: %s' % e)
        TOK, tok_ok = {4: '1', 3: '1'}, False
    out('C-TAU4: S4(c) v1_1 (%s) claims tau4 N4 %s, N3 %s; the TSVs (%s, %s) lie on R4\'s grid, each row\'s tau4_hi (raised two binary64 steps) '
        'is at most the claim, each row\'s rho_hi is the S_V export\'s; the manifest (%s) lists the same files -> %s' % (
            PINS[S4C_RECORD][:8], TOK[4], TOK[3], PINS[TAU4_TSV[4]][:8], PINS[TAU4_TSV[3]][:8], PINS[S4C_MANIFEST][:8], gate(fails, 'C-TAU4', tok_ok)))
    run_plant('PLANT-TAU4-LOW', lambda: read_tau4(P, IN['SV'], open(S4C_RECORD).read().replace('tau_4(4) = %s,' % TOK[4], 'tau_4(4) = 0.027600,')))
    IN['TAU4A'] = dict((N, arb(TOK[N])) for N in (4, 3))
    IN['RMAIN'] = {}
    for N in (4, 3):
        try:
            IN['RMAIN'][N] = check_rmain(N)
            ok = True
        except Refused as e:
            out('  refused: %s' % e)
            IN['RMAIN'][N], ok = r_main_arb(N), False
        out('C-RMAIN N=%d: r_main = %s by the matrix-tree theorem, inside the endw record (%s) interval -> %s' % (
            N, IN['RMAIN'][N].str(20), PINS[ENDW[N]][:8], gate(fails, 'C-RMAIN N=%d' % N, ok)))
    run_plant('PLANT-RMAIN', lambda: check_rmain(4, swap=True))
    IN['TS'], IN['SIG'] = {}, {}
    for N in (4, 3):
        try:
            IN['TS'][N], IN['SIG'][N] = orient_signs(N)
            ok = True
        except Refused as e:
            out('  refused: %s' % e)
            IN['TS'][N], IN['SIG'][N], ok = None, (0, 0), False
        out('C-ORIENT-SIGNS N=%d: %s S[3][1] = %r, S[1][3] = %r: u~_x times %+d, u~_y times %+d (the orientation, P0_LOG line 4089) -> %s' % (
            N, os.path.basename(TS_FILES[N]), IN['TS'][N][3][1] if ok else None, IN['TS'][N][1][3] if ok else None, IN['SIG'][N][0],
            IN['SIG'][N][1], gate(fails, 'C-ORIENT-SIGNS N=%d' % N, ok)))
        out('C-CX0-SIGN N=%d: the E2 record\'s t^0 signs of e,1 and e,3 times the orientation signs are +1 -> %s' % (
            N, gate(fails, 'C-CX0-SIGN N=%d' % N, ok and flag(lambda: cx0_sign_check(IN, N)))))
    if IN['SIG'].get(4, (0, 0))[0] in (1, -1):
        run_plant('PLANT-CX0-SIGN', lambda: cx0_sign_check(dict(IN, SIG={3: IN['SIG'][3], 4: (-IN['SIG'][4][0], IN['SIG'][4][1])}), 4))
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2

    ROWS = {'spec': [], 'lmp': []}
    perr, D1, DL, DM, cwid, l3dom, wrs = {}, {}, {}, {}, {}, {}, {}
    for N in (4, 3):
        rows = P[N][FIRST[N]:]
        mid = len(rows) // 2
        for j, (idx, jlo, jhi) in enumerate(rows):
            try:
                D = piece_both(N, idx, jlo, jhi, IN)
            except Refused as e:
                g = str(e).split(':')[0] if str(e).startswith('C-') else 'C-PIECE (%s)' % str(e)[:40]
                perr.setdefault(g, []).append('N%d_P%s' % (N, idx))
                continue
            sp, lm = rows_of(N, idx, jlo, jhi, D, TOK)
            key = 'N%d_P%s' % (N, idx)
            ROWS['spec'].append((key, sp))
            ROWS['lmp'].append((key, lm))
            wx = ((D['cx'].upper() - D['cx'].lower()) / 2 / abs(D['cx'].mid()))
            wy = ((D['cy'].upper() - D['cy'].lower()) / 2 / abs(D['cy'].mid()))
            cw = cwid.setdefault(N, [0.0, 0.0])
            cw[0], cw[1] = max(cw[0], float(wx.upper())), max(cw[1], float(wy.upper()))
            wrs.setdefault(N, []).append(D['wr'])
            r = float((D['L3'][1][0] / D['LA']['q']).upper())
            l3dom.setdefault(N, []).append(r)
            if j == 0:
                D1[N] = (idx, jlo, jhi, D)
            if j == mid:
                DM[N] = (idx, jlo, jhi, D)
            if j == len(rows) - 1:
                DL[N] = (idx, jlo, jhi, D)
        out('C-PIECE N=%d: %d of %d pieces computed (ritz_piece, lemma_a_cbar, C-ORDER, C-TAU-SY, C-L3-FP, C-LK-GAP, C-ORIENT, C-QW, C-DEN, C-RW) -> %s' % (
            N, sum(1 for k, _ in ROWS['spec'] if k.startswith('N%d_' % N)), len(rows), gate(fails, 'C-PIECE N=%d' % N,
                                                                                        not any(v for g, v in perr.items() if any(x.startswith('N%d_' % N) for x in v)))))
    for g, v in sorted(perr.items()):
        out('  C-PIECE refusals %s: %d pieces, first %s' % (g, len(v), v[0]))
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2
    for N in (4, 3):
        for lab_, (idx, jlo, jhi, D) in (('first', D1[N]), ('last', DL[N])):
            L3 = D['L3']
            out('INFO %s N=%d piece %s [%s, %s]: s_x [%s, %s], s_y [%s, %s], tau4 %s; rho %s %s %s; mu_lo %s %s %s; L %s %s %s; q (L3) %s %s %s; '
                'c_x(-1) [%s, %s], c_y(-1) [%s, %s]; |Q_W w-hat|/A~_0 %s; R_w %s, rho1 %s' % (
                    lab_, N, idx, jlo, jhi, dec_lo(D['s_lo'][1]), dec_hi(D['s_hi'][1]), dec_lo(D['s_lo'][2]), dec_hi(D['s_hi'][2]), TOK[N],
                    dec_hi(D['rho'][0]), dec_hi(D['rho'][1]), dec_hi(D['rho'][2]), dec_lo(D['mu_lo'][0]), dec_lo(D['mu_lo'][1]), dec_lo(D['mu_lo'][2]),
                    dec_hi(D['Lk'][0]), dec_hi(D['Lk'][1]), dec_hi(D['Lk'][2]), dec_hi(L3[0][0]), dec_hi(L3[1][0]), dec_hi(L3[2][0]),
                    dec_lo(D['cx']), dec_hi(D['cx']), dec_lo(D['cy']), dec_hi(D['cy']), dec_hi(D['Qw'] / D['A'][0]),
                    D['sv']['Rw_hi'][1], D['sv']['rho1_hi'][1]))
        out('INFO C(-1)-WIDTH N=%d: the largest relative half-width over the pieces: c_x(-1) %.4e, c_y(-1) %.4e' % (N, cwid[N][0], cwid[N][1]))
        out('INFO C-L3-DOM N=%d: L3\'s q_x over R4\'s c-bar q_x: %.4f .. %.4f over the pieces' % (N, min(l3dom[N]), max(l3dom[N])))
    for N in (4, 3):
        wx3 = [w[0] for w in wrs[N]]
        wsy = [w[1] for w in wrs[N]]
        out('INFO V3-WIDTH N=%d: written / record-computation width, ux3 from %.3e to %.3e, s_y from %.3e to %.3e over %d pieces' % (
            N, min(wx3), max(wx3), min(wsy), max(wsy), len(wx3)))
    for N in (4, 3):
        idx, jlo, jhi, D = DL[N]
        out('C-S0 and CX0 N=%d on the last piece %s: x0, y0 inside s_x, s_y, mu_x, mu_y; c_x(-1) holds +x0 ((N-1)/2)^(1/2), c_y(-1) holds '
            '+y0 ((N-1)/2)^(1/2) (KC4\'s t^0 values in the canonical orientation) -> %s' % (
                N, idx, gate(fails, 'C-S0/CX0 N=%d' % N, flag(lambda: check_exact_last(N, D)))))
    run_plant('PLANT-S0', lambda: check_exact_last(4, DL[4][3], 'S0'))
    run_plant('PLANT-CXSWAP', lambda: check_exact_last(4, DL[4][3], 'CXSWAP'))
    idx1, jlo1, jhi1, _d1 = D1[4]
    run_plant('PLANT-L3-GAP', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'L3GAP', 'law'))
    run_plant('PLANT-LK-GAP', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'LKGAP', 'law'))
    run_plant('PLANT-ORIENT', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'ORIENT', 'law'))
    run_plant('PLANT-RW', lambda: piece_compute(4, idx1, jlo1, jhi1, IN, 'RW', 'law'))
    for N in (4, 3):
        for lab_, (idx, jlo, jhi, D) in (('first', D1[N]), ('middle', DM[N]), ('last', DL[N])):
            try:
                t, sx, sy, cxf, cyf = f2_twin(N, jlo, jhi, IN, D)
                ok, txt = True, 'float s_x %.12f, s_y %.12f, c_x(-1) %.10f, c_y(-1) %.10f at t %.6e' % (sx, sy, cxf, cyf, t)
            except Refused as e:
                ok, txt = False, str(e)
            out('C-F2 N=%d %s piece %s: %s -> %s' % (N, lab_, idx, txt, gate(fails, 'C-F2 N=%d %s' % (N, lab_), ok)))
    run_plant('PLANT-F2', lambda: f2_twin(4, D1[4][1], D1[4][2], IN, D1[4][3], 'F2'))
    texts = {}
    for rec, fmt, flds, rws, extra in (
            ('MR_SPECTRAL', 'MR_INPUT_KV_v3', SPEC_FIELDS, ROWS['spec'], []),
            ('MR_LEMMAP', 'MR_LEMMAP_KV_v2', LEMMAP_FIELDS, ROWS['lmp'],
             ['UNITS = S units (S = T/lambda_0), W = span{psi-hat, e1, e3} in the flip-even sector',
              'BASIS = b in {p, 1, 3}: psi-hat, e1, e3 as unit vectors psi_b/|psi_b|',
              'DEFINITIONS = rhok_hi >= |Q_W S u~_k|; muk_lo <= mu_k (the Ritz values of S on W); tau_hi = tau4 >= ||Q_W S Q_W||; Lk_hi >= '
              'rhok_hi/(muk_lo - tau_hi) >= |P_e u~_k| (Lemma P); u<k><b>_lo <= uhat_kb <= u<k><b>_hi with u~_k = sum_b uhat_kb psi_b/|psi_b|, '
              'u~_0 with uhat_00 > 0, u~_x along e1 and u~_y along e3 (the P0_LOG line 4089; see TRIAL_SET); qa_hi >= |Q_W u_a| and '
              'eps_ka_hi >= |<u~_k, u_a>| for k != a (L3), u_a oriented by <u~_a, u_a> > 0',
              'ROUNDING = *_hi rounded up, *_lo rounded down, 17 significant digits; tau_hi copied from the S4(c) v1_1 claim',
              'COMPUTATION = v3: per piece each field is the intersection of the S9-record computation (v2) and the law-certificate '
              'computation (S8 D, E2, FF under m3_lawcert_v1_1, S8 N under v1_2)'])):
        txt = kv_text(rec, fmt, flds, rws, extra)
        try:
            n = readback(txt, fmt, rec, flds, rws)
            ok = True
        except Refused as e:
            out('  refused: %s' % e)
            n, ok = 0, False
        out('C-WRITE %s: %d rows read back and checked (header, FIELDS, rows, decimals, lo <= hi, single hi >= 0) -> %s' % (rec, n, gate(fails, 'C-WRITE %s' % rec, ok)))
        texts[rec] = (txt, fmt, flds, rws)
    run_plant('PLANT-WRITE', lambda: readback(texts['MR_SPECTRAL'][0], 'MR_INPUT_KV_v3', 'MR_SPECTRAL', SPEC_FIELDS, ROWS['spec'], tamper=True))
    lk_bad = 0
    t4s = {}
    for (k, sp), (k2, lm) in zip(ROWS['spec'], ROWS['lmp']):
        f = dict(zip(LEMMAP_FIELDS.split(), lm))
        if k != k2 or sp[6] != f['tau_hi']:
            lk_bad += 1
        for kk in KNAME:
            if not (Fraction(f['L%s_hi' % kk]) >= Fraction(f['rho%s_hi' % kk]) / (Fraction(f['mu%s_lo' % kk]) - Fraction(f['tau_hi']))):
                lk_bad += 1
        t4s[k[:2]] = sp[6]
    out('C-WRITE-REL: in every MR_LEMMAP row Lk_hi >= rhok_hi/(muk_lo - tau_hi) exactly (Fractions of the written decimals), and the tau_hi '
        'token equals MR_SPECTRAL\'s (%s) -> %s' % (', '.join('%s %s' % kv for kv in sorted(t4s.items())), gate(fails, 'C-WRITE-REL', lk_bad == 0)))
    unrun = [p for p in PLANT_NAMES if p not in EXEC] + [p for p in EXEC if p not in PLANT_NAMES or EXEC.count(p) != 1]
    out('PLANTS: %d of %d must-fire plants ran (not run or repeated: %s); not firing: %s' % (
        len(set(EXEC)), len(PLANT_NAMES), ' '.join(unrun) if unrun else 'none', ' '.join(nofire) if nofire else 'none'))
    if nofire or unrun:
        fails.append('PLANTS')
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2
    if MODE == 'dry':
        os.mkdir(RECDIR)
    if not os.path.isdir(RECDIR) or os.path.realpath(RECDIR) not in (os.path.realpath(OWN + '/mr/v3'), os.path.realpath(os.path.join(ASM, 'dry_%s' % TAG))):
        out('VERDICT INVALID (record folder)')
        return 2
    for rec in ('MR_SPECTRAL', 'MR_LEMMAP'):
        txt = texts[rec][0]
        path = os.path.join(RECDIR, rec + '.kv')
        with open(path, 'x') as fh:
            fh.write(txt)
        if sha_file(path) != hashlib.sha256(txt.encode()).hexdigest():
            out('VERDICT INVALID (the written %s differs from memory)' % rec)
            return 2
        out('RECORD %s sha256 %s rows %d' % (os.path.relpath(path, W18), sha_file(path), len(texts[rec][3])))
    out('RUN wall %.1f s' % (time.time() - t0))
    out('VERDICT VALID')
    return 0


PLANT_NAMES = ('PLANT-CORE', 'PLANT-PINS-R4', 'PLANT-RITZ-S9-PIN', 'PLANT-M2B-PIN', 'PLANT-M4-PIN', 'PLANT-SV-PIN', 'PLANT-SV-GRID',
               'PLANT-E2-PIN', 'PLANT-E2-TRIAL', 'PLANT-TAU4-LOW', 'PLANT-RMAIN', 'PLANT-L3-GAP', 'PLANT-LK-GAP', 'PLANT-ORIENT', 'PLANT-RW',
               'PLANT-S0', 'PLANT-CXSWAP', 'PLANT-F2', 'PLANT-WRITE', 'PLANT-CX0-SIGN', 'PLANT-ALIAS', 'PLANT-LAW-PIN')
SOURCE_LINE = ''


if __name__ == '__main__':
    from flint import arb, arb_mat, ctx
    ctx.prec = 256
    SOURCE_LINE = ('S9 records N4 %s N3 %s (pk03); M2B_KV_v1 %s; M4_KV_v1 %s; S4(c) v1_1 %s (tau4 claim); S_V export %s (pk07, rho1_hi, '
                   'Rw_hi); S8 E2 N4 %s N3 %s and FF N4 %s N3 %s (pk03); R4 %s (CORE); v3: law certificates m3_lawcert_v1_1 N4 %s N3 %s and '
                   'm3_lawcert_v1_2 N4 %s N3 %s (pk03) through m3_reader_s9h_v1 %s, each field the intersection with the record computation' % (
                       PINS[S9_RECORDS[4][0]][:8], PINS[S9_RECORDS[3][0]][:8], PINS[M2B[0]][:8], PINS[M4[0]][:8], PINS[S4C_RECORD][:8],
                       PINS[S67[0]][:8], PINS[E2REC[4][0]][:8], PINS[E2REC[3][0]][:8], PINS[FFREC[4][0]][:8], PINS[FFREC[3][0]][:8], R4_SHA[:8],
                       PINS[S8CERT[4]['v1_1'][0]][:8], PINS[S8CERT[3]['v1_1'][0]][:8], PINS[S8CERT[4]['v1_2'][0]][:8],
                       PINS[S8CERT[3]['v1_2'][0]][:8], PINS[RDR][:8]))
    try:
        rc = main()
    except Refused as e:
        out('STOP Refused: %s' % e)
        out('VERDICT INVALID (refused)')
        rc = 2
    FH.close()
    sys.exit(rc)
