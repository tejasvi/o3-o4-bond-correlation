#!/usr/bin/env python3
"""kt_s9h_ins_v2_7.py (pk25, code/pk25/asm/; G5 C12 step 1, the rows 4380, 4401, 4407, 4418): the MR_INSERT v4 producer, MODE dry or
cert (cert only under the approval naming this file's sha8; the record to mr/v4b/MR_INSERT.kv, a dry run's to asm/dry_<TAG>/). h rows:
S9(c)-h (the code of the S9C engine kt_s9c_h_v1_7, pk25/S9C_LINES_v1.md with S9C_LINES_v1_1.md), xc enclosing v_x/t by the centred
form of M_R^c/t with the lines and Lemma A over t_lo, vx joined with t xc at both ends, way B on the last piece (xc = [g_lo, g_hi],
xf = f); t and a rows as kt_s9h_ins_v1_5 (power 0: xc = vx, xf = 0); Pev = C for h and t (the row 4376); the header of
pk24/MIDROW_G6_SPEC_v1_6_2.md sect. 6 with FIELDS, X_POWER, X_DEFINITION and the ORIENT_CHECK pattern read by ast from the
pinned M1 engine, TRIAL_SET copied from mr/v3 MR_SPECTRAL, LEMMAP_SHA256 of mr/v3 MR_LEMMAP; gates C-SIGN-S9C, C-BAD-W, C-ANCHOR,
C-FACTX, C-FLOOR, C-ORIENT-LINE, C-WRITE; the C8 notes N1 (c_t ends by exact comparison), N2 (PLANT-MU-T, PLANT-MU-C), N4
(mu tool v1_1). v2_2: L7's |h_00| bounds (C8)'s vacuum amplitude, + (2 W + W^2) N_H (the row 4441).
v2_4 (the rows 4422, 4426, 4491, 4520): option (B)'s Pev for h and t per piece, Pev_hi = min(C, V) (the rho note's sect. 4 form) with
V = |u00| ((c - e1)^2 + e2 - e1^2 - 2 e1 + (N - 1)/2 + rho)_+^1/2 + C (|u01| + |u03|) + C delta_0 >= |v|, e_k = E_k/E_0 from pk23's records
(TT,0,0 of family L; Mh,0,0, Mhh,0,0 of LH; Mt,0,0, Mtt,0,0 of LT) and rho = RHO_HI of pk25/rho/RHO_RECORD_v1.kv (Lemma RHO: the xi^2
entry's multiplier is m_l^2 + m_l - J m_l', pk25/rho/RHO_LEMMA_v1.md); Pevw and vp follow as before; the cert record to mr/v4b.
v2_5 (P4, the rows 4636, 4640, 4644; pk25/P4_LEMMA_NOTE_v1_1.md): MR_INSERT v5 = v4b with
the last h row by route (B), Way A (waya_last): s_x v_x = <u_x, B^w u> = h~ + R_1 - c_h R_2 + E_A with h~ = <u~_x, S M_h psi-hat_n>, ONE S
(the NIH entry next to psi-hat is <psi_b, S M_h psi-hat>), R_1 = <u~_x, S M_h (u - psi-hat_n)>, R_2 = <u~_x, u>, E_A Lemma
A's error at level x. h~ = sum_b c_xb Ih_b / (G_00^1/2 Lambda) with the true top eigenvalue Lambda in the records' units, enclosed by
[mu_0, mu_0/m0lo] (the Ritz value and Kato-Temple's m0lo, as S9(c)'s lambda_0 term), and P2's oriented Ritz coefficients (so v2_4's sigma_x
flip is not applied again); the t^0 value of the combination is exactly 0 (C13's C-BH0, P1's C-T0-EXACT and C-HARM; C-WAYA-T0 checks the
coefficient balls hold 0), so xc = v_x/t is finite at t = 0 with xf_hi = 0, and vx_lo, vx_hi are refreshed to [min(0, t_1 xc_lo),
max(0, t_1 xc_hi)]. Inputs added: P2's MR_LEMMAP_V3F record (the factored /t table; a cert run needs its CERTIFIED record) and P1's C10
record (exact uhat(0) and G0). Every other row and field is v4b's computation, unchanged (vp_hi of the last h row keeps the way B bound,
which stays valid); way B still runs and prints as INFO. Gates C-WAYA-IN, C-WAYA-T0, C-A0, C-MONO-TAIL, C-MONO-FAR, C-WAYA; plants
PLANT-WAYA-PIN, PLANT-WAYA-ZERO (u_y(0) in place of u_x(0): a nonzero t^0 combination), PLANT-WAYA-ORIENT (c_x flipped); the cert record to
mr/v5b/MR_INSERT.kv.
v2_6 = v2_5 for P4's cert (the rows 4670, 4672):
Lambda is the eigenvalue that mu_0 and m0lo bound only because the Ritz problem's T entries and the NIH entries share one main, main_N (the
three-column vertex graph N; were the mains to differ, F would need main_T/main_N). C-MAIN-N gates it from the pinned records at both N:
S8 N's record has graph N, the NIH record's prep names the vertex graph VN, and the two families carry equal prep parameters (a_v, ap,
theta0). PLANT-MAIN-N (S8 D's two-column record in the T slot) must be refused. R_1's factor reads the upper end of |c_h|.
v2_7 = v2_6 with the cert record to mr/v5b/MR_INSERT.kv (the row 4691): P2's N1 fix gives a new P2 table (p2/v3f2/MR_LEMMAP_V3F.kv)
whose last rows equal the cited one's, so the rows reproduce MR_INSERT v5 (91f80105); mr/v5 stays as cited. No other change.
The C6b base template text follows. C6b base: h's bulk amplitudes per piece of R4's grid (S9(b)-h).
Made by asm/make_kt_s9h_ins_v1.py from asm/src/kt_s9h_ins_v1.py.in. CORE blocks copied by tool: R4's code (pk15/kt_p2_assembly_v1_37_1.py,
R4_SHA) and pk25's C6a code (asm/kt_s9h_asm_v1_5.py, C6A_SHA); C-CORE compares every copy with its pinned source at run time.
Design: pk25/C6B_DESIGN_NOTE_v1.md sect. 1-2. Per piece (N = 4 from the J = 350 piece, N = 3 from the J = 300 piece):
- the Ritz problem on W = span{psi-hat, e1, e3} from S8's D (g) and N (T) records with their law certificates (pk03's m3_lawcert_v1_1 and
  v1_2) at err(J_lo) (LAWCERT_CLAIM's right side, nonincreasing in J, evaluated here with outward rounding: rem (300/J)^4 + tail and ann by the
  chi-square P-ratios + far e^(-far_rate (J - 300)) + sum_k ak_rad[k] t^k over the piece's t range), with pk25's Ih,b (NIH record and its
  certificate m3_lawcert_s9h_v1_1) in R4's Iht slot, so ritz_piece's t amplitudes are h^_k = mhat (c_k . Ih)/(G00^1/2 lambda~0^2), and S8 D's
  DY,b in the Dx slot (the S9 record's Dx alias); all read through pk25's reader fork m3_reader_s9h_v1 (load, load_lawcert, entry_law);
- lemma_a_cbar with tau4 (S4(c) v1_1's claim), the S-unit bounds and L3 as C6a; lemma_a_amp (R4) for Delta_k with Lam = 40, Hbad' =
  tail_h kappa^2, Gbad', NA-prime and Abad' (Lemma G and B constants; C-R4-LG checks them against R4's certified run output); qv4 with
  A_h from M4H_KV_v1 (pk25's m4h_reader_v1_1); Lemma A (L3) at x and y: dh_a = q_a Q + eps_0a h0t + eps_ba |h~_b| + (q_a^2 + eps_0a^2 +
  eps_ba^2) |h~_a|;
- the orientation (P0_LOG line 4089): the x amplitude times sign(S[3][1]) and the y amplitude times sign(S[1][3]) of the pinned trial
  sets (C-ORIENT-SIGNS), C-ORIENT on the flipped Ritz vectors;
- v_x = sigma_x h~_x + [-dh_x, dh_x], v_y likewise; xc = v_x/[t_lo, t_hi] on pieces with t_lo > 0; Pev = Q + h0t L_0 + |h~_x| L_x +
  |h~_y| L_y with MR_LEMMAP v2's L_k; vp = (h0t^2 + h~_x^2 + h~_y^2 + Q^2)^1/2.
Output: the run log asm/out/out_<name>_dry_<TAG>.out and a TSV asm/out/ins_h_<name>_<TAG>.tsv (per piece: vx, vy, xc, the error parts).
Usage: kt_s9h_ins_v2_7.py dry|cert TAG"""
import ast
import hashlib
import json
import math
import os
import re
import sys
import time
from fractions import Fraction

# ---- CORE constants (R4)
W18 = '/mnt/g2/release/root/code'
GRID = W18 + '/pk07/out/export_kt_s67_cert_v2_2_sweep.kv'
EPS_G, THETA_G = '0.25', '0.7'
G00_MOCK = '1'
G00_CLAIM = 'for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err (Lemma U'
S7G00 = dict((N, (W18 + '/pk03/out/m3_b5_N%d_J300_v1_7.json' % N, W18 + '/pk03/out/m3_run_v1_7_asm.%d.out' % N)) for N in (4, 3))
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
LAM_T, LAM_A = '40', '20'
M3_READER_PATH = W18 + '/pk03/m3_reader_v4_4.py'
KERNEL_SHA = '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0'
KERNEL_LINE = 'arbeng_c2b_v2.py %s ctx.prec 512' % KERNEL_SHA
M3_READER_SHA = 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0'
BADWORDS = ('PRECERT', 'STUB')
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]

# ---- CORE constants (pk25's C6a engine kt_s9h_asm_v1_5)
JLOW = {4: 350, 3: 300}
KNAME = ('0', 'x', 'y')

MODES = ('dry', 'cert')   # v2_1: cert only under the approval naming this file's sha8
if len(sys.argv) != 3 or sys.argv[1] not in MODES or not re.fullmatch(r'[A-Za-z0-9_]{1,40}', sys.argv[2]):
    print('usage: kt_s9h_ins_v2_7.py dry|cert TAG')
    sys.exit(2)
MODE, TAG = sys.argv[1], sys.argv[2]
SELF = os.path.abspath(__file__)
LABEL = os.path.splitext(os.path.basename(SELF))[0]
OWN = W18 + '/pk25'
ASM = OWN + '/asm'
OUT_DIR = ASM + '/out'
OUT_PATH = os.path.join(OUT_DIR, 'out_%s_%s_%s.out' % (LABEL, MODE, TAG))
TSV_PATH = os.path.join(OUT_DIR, 'ins_h_%s_%s.tsv' % (LABEL, TAG))
R4_PATH = W18 + '/pk15/kt_p2_assembly_v1_37_1.py'
R4_SHA = 'e92342b001b99e2f5a730170d2111788e8093042ad5957b6409fe96feadb6b0b'
C6A_PATH = ASM + '/kt_s9h_asm_v1_5.py'
C6A_SHA = '1704af081b8766c30cbdb4ad0ae0b245353b5d2f50f53a11d271d16c00f83692'
CORE_DEFS = ('out', 'sha_file', 'Refused', 'lines_of', 'gate', 'dec_hi', 'dec_lo', 'kv_parse', 'read_kv', '_mode_checks', '_frac_ball', 'load_m3', 'read_grid', 'qv4', 'tball', 'grid_j', 'q2arb', 't_ends', 'lam_h', 'kappa_bound', 'trial_ab', 'load_trial_q', 's_eps', 'tau_strip', 'lg_weights', 'gbad_p', 'abad_p', 'load_g00', 'g00_s7', 'check_g00', 'check_g00_entry', 'g00_lower', 'phi_T', 'check_c1', 'check_trial_set', 'load_m2b', 'm2b_eps', 'm2b_call', 'load_m4', 'm4_call', 'm4_law', 'm2b_mhat_coeffs', 'check_tau_trial', 'load_ritz_mock', 'check_s9_trial', 'load_ritz', 'entry_piece', 'mhat_ball', '_min_pt', '_jacobi3', 'ritz_piece', 'lemma_a_cbar', 'lemma_a_amp', 'na_prime', 'pd_vectors', 'pd_dk_meet', '_gam_up', 'tail_h', 'plant')
CORE_CONSTS = ('CODEDIR', 'GRID', 'EPS_G,THETA_G', 'G00_MOCK', 'G00_CLAIM', 'S7G00', 'VACRES', 'C1_CLAIM', 'M2B', 'M2B_READER_PATH', 'M2B_PREC', 'M4', 'M4_READER_PATH', 'M4_PREC', 'S67', 'S67_READER_PATH', 'S67_SCRIPT', 'REVEN,RPE', 'RITZ_KEYS', 'S9_RECORDS', 'TS_FILES', 'LAM_T,LAM_A', 'M3_READER_PATH', 'KERNEL_SHA', 'KERNEL_LINE', 'M3_READER_SHA', 'BADWORDS', 'BASIS')
C6A_DEFS = ('segments', 'check_grid', 'l3_level', 'orient_signs', 'check_orient')
C6A_CONSTS_N = ('JLOW', 'KNAME')
R4_CERT_OUT = W18 + '/pk15/out/out_kt_p2_assembly_v1_37_1_cert.out'
RDR = OWN + '/m3/m3_reader_s9h_v1.py'
M3O = W18 + '/pk03/out/'
S8REC = dict((N, dict((F, (M3O + 'm3_s8v3_%s_N%d_J300_v1_8_1.json' % (F, N), M3O + 'm3_run_v1_8_1_asmP.%d.out' % N)) for F in ('D', 'E2', 'E3', 'FF')))
             for N in (4, 3))
for _N in (4, 3):
    S8REC[_N]['N'] = (M3O + 'm3_s8v3_N_N%d_J300_v1_8_2.json' % _N, M3O + 'm3_run_v1_8_2_asmN.%d.out' % _N)
S8CERT = dict((N, {'v1_1': (M3O + 'm3_lawcert_v1_1_N%d.json' % N, M3O + 'm3_lawcert_v1_1_%d.out' % N),
                   'v1_2': (M3O + 'm3_lawcert_v1_2_N%d.json' % N, M3O + 'm3_lawcert_v1_2_%d.out' % N)}) for N in (4, 3))
HREC = dict((N, dict((F, (OWN + '/m3/out/m3_s9h_%s_N%d_J300_v1.json' % (F, N), OWN + '/m3/out/m3_run_s9h_v1_1_asm.%d.out' % N)) for F in ('NIH', 'NHT', 'DH')))
            for N in (4, 3))
HCERT = dict((N, (OWN + '/m3/out/m3_lawcert_s9h_v1_1_N%d.json' % N, OWN + '/m3/out/m3_lawcert_s9h_v1_1_%d.out' % N)) for N in (4, 3))
M4H = (OWN + '/m4h/M4H_KV_v1.txt', OWN + '/m4h/out/out_m4h_asm_v1_1.out')
M4H_READER_PATH = OWN + '/m4h/m4h_reader_v1_1.py'
MU = OWN + '/mu/kt_mu_hw_v1_1.py'   # the mu tool v1_1 (the row 4386 N4)
CI_MARGIN = '0.01'   # the margin around c~_h's hull for the mu tool's interval (C-CH-HULL checks c_h inside)
MEANS = W18 + '/pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37_1.kv'   # R4's certified means export (c_t, c_b)
DJREC = dict((N, (W18 + '/pk22/m3/out/m3_c3j_DJ_N%d_J300_c3j.json' % N, W18 + '/pk22/m3/out/m3_run_v1_9_3_asm.%d_c3j.out' % N)) for N in (4, 3))   # pk22's c3j DJ records (DHT)
PEVB = {4: {'L': ('/mnt/g2/release/root/code/pk23/pev/out/m3_hl_L_N4_J300_hl.json', '/mnt/g2/release/root/code/pk23/pev/out/m3_run_v1_9_3_asm.4.out'), 'LH': ('/mnt/g2/release/root/code/pk23/pev/out/m3_hl_LH_N4_J300_hl.json', '/mnt/g2/release/root/code/pk23/pev/out/m3_run_v1_9_3_asm.4.out'), 'LT': ('/mnt/g2/release/root/code/pk23/pev/out/m3_hl_LT_N4_J300_hl.json', '/mnt/g2/release/root/code/pk23/pev/out/m3_run_v1_9_3_asm.4.out')}, 3: {'L': ('/mnt/g2/release/root/code/pk23/pev/out/m3_hl_L_N3_J300_hl.json', '/mnt/g2/release/root/code/pk23/pev/out/m3_run_v1_9_3_asm.3.out'), 'LH': ('/mnt/g2/release/root/code/pk23/pev/out/m3_hl_LH_N3_J300_hl.json', '/mnt/g2/release/root/code/pk23/pev/out/m3_run_v1_9_3_asm.3.out'), 'LT': ('/mnt/g2/release/root/code/pk23/pev/out/m3_hl_LT_N3_J300_hl.json', '/mnt/g2/release/root/code/pk23/pev/out/m3_run_v1_9_3_asm.3.out')}}   # v2_3: pk23's option (B) records {N: {family: (record, asm output)}} (maker-filled)
RHOREC = OWN + '/rho/RHO_RECORD_v1.kv'   # v2_3: Lemma RHO's certified record (RHO_HI for every finite J >= J0)
PEVB_KEYS = {'L': ('TT,0,0',), 'LH': ('TTh,0,0', 'Mh,0,0', 'Mhh,0,0'), 'LT': ('Mt,0,0', 'Mtt,0,0')}   # v2_3: pk23's HL_ENTRY_LIST_v1
LAM9C = 60   # the S9(c) Lam-split level (pk02/S9C_PLAN_v2_ADD1.md sect. 1; the row 4328)
BAD_TOL = '1e-10'   # C-BAD-SMALL and C-BAD-W (S9C_BADPART_LEMMA_v1 sect. 4)
ENGA = dict((N, W18 + '/pk01/out_kt_c_v2_3_e1n%d.out' % N) for N in (4, 3))   # engine A's EXPLICIT lines (m_bg, INFO)
M1ENG = W18 + '/pk24/mr_engine/kt_mr_assembly_v1_8_4.py'   # the M1 engine: MR_INSERT v4 FIELDS, X_POWER, X_DEFINITION, ORIENT_RX
SPEC_V3 = OWN + '/mr/v3/MR_SPECTRAL.kv'   # the certified MR_SPECTRAL: TRIAL_SET is copied from it (the row 4321)
LEMMAP = OWN + '/mr/v3/MR_LEMMAP.kv'   # v2_1: the certified C6a v3 side table (the review 087868a8 CLEAR; the row 4401)
S4C_RECORD = W18 + '/pk21/p2/s4c/S4C_TIGHT_RECORD_v1_1.md'
M_RITZ = W18 + '/pk15/mocks/mock_ritz_entries_v1.kv'
KC4_A1 = {4: '3.3786416397e-02', 3: '1.6907850836e-02'}   # KC4's a_1 h_x in u_x's orientation (G5_PLAN_v1 sect. 4, C-HARM), for INFO only here
P2REC = W18 + '/pk25/p2/v3f2/MR_LEMMAP_V3F.kv'   # v2_5: P2's MR_LEMMAP_V3F record (maker-filled; a cert run needs STATUS CERTIFIED)
C10REC = OWN + '/c10/C10_RECORD_v1.kv'   # v2_5: P1's certified exact t^0 data (UHAT0, GT0_W)
P4NOTE = OWN + '/P4_LEMMA_NOTE_v1_1.md'   # v2_5: route (B)'s lemma
PINS = {
    '/mnt/g2/release/root/code/pk01/out_kt_c_v2_3_e1n3.out': 'cee0e054ab2b800d8a6bcd6cbb7e88bbb0c3b34d81c0e5748c8e2dc0494fc1e5',
    '/mnt/g2/release/root/code/pk01/out_kt_c_v2_3_e1n4.out': 'f38d2d62c50bdb136aeb7399a6c04dc9112137cba199e17a622adcd6f4e2e3c9',
    '/mnt/g2/release/root/code/pk02/M2B_KV_v1.txt': '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',
    '/mnt/g2/release/root/code/pk02/m2b_reader_v1.py': 'a9f15db48e9fa51629448181d8a83679c1b93cd2b5696c8ed1e6b41d60df8b02',
    '/mnt/g2/release/root/code/pk02/out/out_m2b_asm_v1.out': 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391',
    '/mnt/g2/release/root/code/pk15/M4_KV_v1.txt': '4bafdcc1c41cf44f6b618644d7b0fdd404422aa5ffeadcfaadae02183e9eee51',
    '/mnt/g2/release/root/code/pk15/kt_p2_assembly_v1_37_1.py': 'e92342b001b99e2f5a730170d2111788e8093042ad5957b6409fe96feadb6b0b',
    '/mnt/g2/release/root/code/pk15/m4_reader_v1.py': '5cef440ae313eddd2e6bcf49aac835f2595e61b6a3e59b23fca0c15671ec6bcd',
    '/mnt/g2/release/root/code/pk15/mocks/mock_ritz_entries_v1.kv': '568e62829e1fa07f774b48f23e11d0f677be6841be81e2b84c2382d630a8f15a',
    '/mnt/g2/release/root/code/pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37_1.kv': '0fed18c6f3a832b6455ae08632ed9a4cd91480ac2a89c85c9cec411e31ff6768',
    '/mnt/g2/release/root/code/pk15/out/out_kt_p2_assembly_v1_37_1_cert.out': 'b4a1dea6e7dddaad535c92bc491e0b8c2ffb23851c6b2f7fc2901605f9a45a12',
    '/mnt/g2/release/root/code/pk15/out/out_m4_asm_v1.out': '616dd9e1919695ed9dc953c55e8c46d66dabd9700d2913722d11f94502dc858e',
    '/mnt/g2/release/root/code/pk03/m3_reader_v4_4.py': 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0',
    '/mnt/g2/release/root/code/pk03/out/m3_b5_N3_J300_v1_7.json': '411913043ce7c90970f8fc35918e6c221af2eb025b728dde6f55b755646ab8d3',
    '/mnt/g2/release/root/code/pk03/out/m3_b5_N4_J300_v1_7.json': '77f83bc79060bae4c34de47884f00d48e6403fee995e3e54dab6781e4c527b3a',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_3.out': '2b7847dc902eed4dda6800ff2118d8c378421179ba4d77242b83dc9086c772d9',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_4.out': 'f814f9f301f8814117dfccbd6715f8ff04e6cd24dcef04e4a95ecaaeb6e37325',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_N3.json': 'ec50ab52cd88b7b0cbd717c6dc4db295e72a8faf10b378b994a4f83cc5d7cfd4',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_1_N4.json': '5b7cbff9443f4ff69e623caa776646b16629aa2b6436c186e1799e9f4d56ba4c',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_2_3.out': 'ec6b099bc6517e11af92cfc641592719202bbe2dd234a2f87cce0e0a54276357',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_2_4.out': '10bc81fc53d21e3a5fff08945a1e890438145bbcee2dcc73033e7c33a37e4bb5',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_2_N3.json': '819c100913e917d09bbf7788b9dba75f15584f232784b9601e9a19e266c7f70c',
    '/mnt/g2/release/root/code/pk03/out/m3_lawcert_v1_2_N4.json': '77cb4f7c05df69c5e185ecd14aeea8fb9caca8d98e306b549390d34163f190d6',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_7_asm.3.out': '18964e97c320395f44b5923d132b1ac65c95b935cc8708a50e197076cc24e0dc',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_7_asm.4.out': 'a5b294f364f9399b9d12f89af6ce1a1e598b8b424bc6e60d35e122ebd1391b97',
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
    '/mnt/g2/release/root/code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py': '28a340e7b38b0f37a40b4eb2df4c0f03b58dedf0b80755a659c0157c1094a56c',
    '/mnt/g2/release/root/code/pk07/kt_s67_export_reader_v2_1.py': '4c6949462ca8c5dda337027b7dc5bada51102a063dc5ff6f8a1c2def01eaf49d',
    '/mnt/g2/release/root/code/pk07/kt_s9h_v1_2.py': '1b68e47141dfc5e873e2660711f6430a0badc9cc948ada32eb11641fabde4ff4',
    '/mnt/g2/release/root/code/pk07/out/export_kt_s67_cert_v2_2_sweep.kv': '6fe9ab65f5207dc3658c98ff4f3696bd2db6aa784b0dec84b33881b2da579c34',
    '/mnt/g2/release/root/code/pk07/out/export_kt_s9h_v1_2_vsweep.kv': '10f3c3d9a18b9c7a596121a8dbec7d2b82afb366704845a7c00e066c8bf6d4f6',
    '/mnt/g2/release/root/code/pk07/out/out_kt_s9h_v1_2_vsweep.out': '58814f7f59dd0d8e9d16b73084b3cc5072f94fb1138300a112e0e49ff017835f',
    '/mnt/g2/release/root/code/pk25/asm/kt_s9h_asm_v1_5.py': '1704af081b8766c30cbdb4ad0ae0b245353b5d2f50f53a11d271d16c00f83692',
    '/mnt/g2/release/root/code/pk25/m3/m3_reader_s9h_v1.py': '812d1395c47e1b00bcfdbf3b17c89d030db1d98655bb9c4ab62378394f9cc0c6',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_lawcert_s9h_v1_1_3.out': '0df499fe6a0c0017463ec0479c1ed5402f959bf766ce24367fbf81f527d95470',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_lawcert_s9h_v1_1_4.out': '805e6f6f1a46a2cdc5b0e316369c5a36ec0fe569c970a1f9f388866273a3a1b6',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_lawcert_s9h_v1_1_N3.json': 'cedffc03309fb7f7ee97206b21f158d0aff00a47350e09f0d0cdd8392cd0e040',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_lawcert_s9h_v1_1_N4.json': 'e45b28c9fc52c637400395e7501b08da5aba4b9a18fe32469b457c58c0ca5ddc',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_run_s9h_v1_1_asm.3.out': '654c3d44d682d60a2a5c9fc9b784db27847753f76e0c90e8b334cdbcc7b1218b',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_run_s9h_v1_1_asm.4.out': 'e8e529dd8323bf730ba6ed41639f69282f4d82c671c1e75821ea360c5e5cfb5e',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_s9h_DH_N3_J300_v1.json': '9248b1183f8ebb5c7f8dcba4a9293e5081bf35e96c43a659b69a19f2203a0f3b',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_s9h_DH_N4_J300_v1.json': 'e02852c2159663318d3a20a5369f5c5585b029faed3a48f4c576d47317d889f8',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_s9h_NHT_N3_J300_v1.json': '86f0c48d40a10b83d9e6f2200117b37f4efb72daf763e58bf7a9d0ad5c7607fc',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_s9h_NHT_N4_J300_v1.json': 'bb4dd91c93eaf8c1e95ee477557553a402621e135acc224ca18e073e28b6fbad',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_s9h_NIH_N3_J300_v1.json': '4b385abfc2d3172bcd338dbbe6837287c36aaec2a1319d42d3bc565c107bd616',
    '/mnt/g2/release/root/code/pk25/m3/out/m3_s9h_NIH_N4_J300_v1.json': '343f7abebd57b015b538e50f310b397ea83dca6f9718d225119e9a8cf808f942',
    '/mnt/g2/release/root/code/pk25/m4h/M4H_KV_v1.txt': '2338cde9c97098abdcddf4d05f159b43dfe55d7869a3eadc899850ee29582995',
    '/mnt/g2/release/root/code/pk25/m4h/m4h_reader_v1_1.py': 'f6cb5da4373a0cfdd2bd888c61088279a5ec6c860279f77ad37df558245736a7',
    '/mnt/g2/release/root/code/pk25/m4h/out/out_m4h_asm_v1_1.out': 'a6ce379e337fd2b4483f3298848485c086ba5e4a0d0bd205ee92cf1a8e5d05b0',
    '/mnt/g2/release/root/code/pk25/mr/v3/MR_LEMMAP.kv': '275b179f6f8e80f12101fda25989a851177c0b6003eee05f4a7095ad003fe013',
    '/mnt/g2/release/root/code/pk25/mr/v3/MR_SPECTRAL.kv': 'af3ba5e36180cfdbf028f8a12c3b28414cf48cccdefc9173579712648aa14b5a',
    '/mnt/g2/release/root/code/pk25/mu/kt_mu_hw_v1.py': '6790050877ac5a3f649f6c995d500a89d0ee4102e207b5e95189bea4cc58c998',
    '/mnt/g2/release/root/code/pk25/mu/kt_mu_hw_v1_1.py': '71a447cc82975f95372d487af6e22b448687d35bbeb80d5579795619e034f95c',
    '/mnt/g2/release/root/code/pk21/p2/s4c/S4C_TIGHT_RECORD_v1_1.md': '9bb4751edd928a40f6e51e1806608b4c0a2c52c37f432962888f88868b1456f6',
    '/mnt/g2/release/root/code/pk22/m3/out/m3_c3j_DJ_N3_J300_c3j.json': 'ac33223fee938157db58c64616e475a42aad7b0b626eb244fcc3b3526e012c22',
    '/mnt/g2/release/root/code/pk22/m3/out/m3_c3j_DJ_N4_J300_c3j.json': '290d2142a532ab23b509e6da294b864941185612f74298afc84041d98f799db3',
    '/mnt/g2/release/root/code/pk22/m3/out/m3_run_v1_9_3_asm.3_c3j.out': 'a8d33d8646f036ce059f21a9430d3d8bddd67fed6ff97e232874d0dc86e773cd',
    '/mnt/g2/release/root/code/pk22/m3/out/m3_run_v1_9_3_asm.4_c3j.out': 'ad7a1177d6d0c8ecb4819e3c50115b65a68022fc7ecd1a938fccd28ea1b72463',
    '/mnt/g2/release/root/code/pk11/out/ts_N3_S_z9sym_v1.json': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    '/mnt/g2/release/root/code/pk11/out/ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    '/mnt/g2/release/root/code/pk11/out/vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    '/mnt/g2/release/root/code/pk11/out/vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    '/mnt/g2/release/root/code/pk23/pev/out/m3_hl_L_N4_J300_hl.json': 'c4bee75a7b224a4893b33138a9d7d6de5c76fa3ae18ac1ba5cdd09d03d700a7d',
    '/mnt/g2/release/root/code/pk23/pev/out/m3_run_v1_9_3_asm.4.out': 'b69fe47c4adf84598285d8d0c71d1d49fa2e4c5ba9ba978c03142734b33dad39',
    '/mnt/g2/release/root/code/pk23/pev/out/m3_hl_LH_N4_J300_hl.json': 'cb539044caeacfcb72aa70cddcf332a026d1f388cb6e51be72e8bee72b0b9bbb',
    '/mnt/g2/release/root/code/pk23/pev/out/m3_hl_LT_N4_J300_hl.json': 'a14b76056962fc35cae228064863c0297faed269a12e0030b11279bc3c7f6ead',
    '/mnt/g2/release/root/code/pk23/pev/out/m3_hl_L_N3_J300_hl.json': '2926e9fe24a6ce8b3b9a7b6021b9c3f5a049b5142b2c52ac23377f5b5e1218e6',
    '/mnt/g2/release/root/code/pk23/pev/out/m3_run_v1_9_3_asm.3.out': '0956bc3d12795a133d5bb359cba90631937fe41479ce488c6f4dcdf3c72435dc',
    '/mnt/g2/release/root/code/pk23/pev/out/m3_hl_LH_N3_J300_hl.json': 'b7d03024fdda4c5e522b01621ee377b87a6fe5ff02ca5f33d5908531b313742f',
    '/mnt/g2/release/root/code/pk23/pev/out/m3_hl_LT_N3_J300_hl.json': '4137b0548286aae88384cb2a8594704264bcca7dfdca385831b256ce63ce3cb2',
    '/mnt/g2/release/root/code/pk25/rho/RHO_RECORD_v1.kv': '252e0cc459daff8ccac044169f00fbfca221f66e7162feb32427ef1a1d369e8f',
    '/mnt/g2/release/root/code/pk25/p2/v3f2/MR_LEMMAP_V3F.kv': '9ef6abafdf450eff317545dd95aff519051352db3c01c752f739466a616d48c4',
    '/mnt/g2/release/root/code/pk25/c10/C10_RECORD_v1.kv': '29a4f3c67afc2b3e2611e37e3026def71d6ae819bcc2ee5ed34f678734bebb98',
    '/mnt/g2/release/root/code/pk25/P4_LEMMA_NOTE_v1_1.md': '48de79f66b17768f363572408fc2b442eea421c6cb585f1b82e4d2e15d84ec74',
}
if not (os.path.isdir(OUT_DIR) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUT_DIR)):
    print('output path check failed')
    sys.exit(2)
FH = open(OUT_PATH, 'x')

# ---- CORE defs (R4)
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

def qv4(A_hi, I):
    """||Q_4 v_t|| (kt_rb_v1_5's form with A_t, t_0 in place of A_h, h_0)."""
    mh, lt0 = I['mhat'], I['lt0']
    hb = I.get('HbadP', I['Hbad'])   # v1_9 (2): Hbad' = tau~0(Lam) kappa^2 when computed
    return (mh / (lt0 * lt0)) * A_hi + I['Lam'] * (mh / lt0) * I['eps_r'] + (I['Lam'] + I['t0'] + hb) * I['sp'] + I.get('GbadP', I['Gbad'])

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

def lam_h(N, J):
    """lambda_h(J) = exp(logmain_N - logmain_D) by riglap2's logmain (pk10/scripts/riglap2.py l.52-56), with det(L_sub)/V = tau(G), the weighted
    spanning-tree count (Kirchhoff), on lapl2.strip_graph(3) and (2): end triangles (A, A, B), interior verticals 1, horizontals 1 (v1_9 (1))."""
    A = ((arb(3) + arb(21).sqrt()) / 6).union(arb((3 + 21 ** 0.5) / 6))
    B = ((3 * arb(5).sqrt() - arb(21).sqrt()) / 12).union(arb((3 * 5 ** 0.5 - 21 ** 0.5) / 12))

    def tau(ncols):
        V = 3 * ncols
        L = arb_mat(V, V)
        E = []
        for j in range(ncols):
            T, M, Bv = 3 * j, 3 * j + 1, 3 * j + 2
            if j == 0 or j == ncols - 1:
                E += [(T, M, A), (M, Bv, A), (T, Bv, B)]
            else:
                E += [(T, M, arb(1)), (M, Bv, arb(1))]
            if j < ncols - 1:
                E += [(3 * j + r, 3 * (j + 1) + r, arb(1)) for r in range(3)]
        for u, v, c in E:
            L[u, u] += c
            L[v, v] += c
            L[u, v] -= c
            L[v, u] -= c
        Lr = arb_mat(V - 1, V - 1, [L[i, k] for i in range(1, V) for k in range(1, V)])
        return Lr.det()
    n = N - 1
    area = 2 * arb.pi() * arb.pi() if N == 4 else 4 * arb.pi()
    logl = -3 * area.log() + arb(3 * n) / 2 * (2 * arb.pi() / J).log() - arb(n) / 2 * (tau(3) / tau(2)).log()
    return logl.exp()

def kappa_bound(N, eps_r_max):
    """kappa_max = k1_hi(300)^3/((1 - eps_r_max) lambda_h(300)), valid for every J >= 300: lambda_h(J) J^(3(N-1)/2) and k1_hi(J) J^((N-1)/2) are
    constant, mhat >= 1 and lambda_0 >= (1 - eps_r) mhat lambda_h (NOTE_M4_SCOPE_v1 sect. 2; the review 606b1fe4 claim 1). v1_25 (1): eps_r_max is the certified eps_r of M2B_KV_v1 at J = 300 (LAW v1 is nonincreasing in J)."""
    j0 = arb(300)
    k1h = 1 / (2 * j0) if N == 3 else (2 / arb.pi()).sqrt() / (j0 * j0 * j0).sqrt()
    return k1h * k1h * k1h / ((1 - eps_r_max) * lam_h(N, j0))

def trial_ab():
    """the trial weights A = (3 + sqrt 21)/6 and B = (3 sqrt 5 - sqrt 21)/12 as hulls of the algebraic values and their binary64 roundings
    (kt_rb v1_2's convention, as in lam_h)."""
    A = ((arb(3) + arb(21).sqrt()) / 6).union(arb((3 + 21 ** 0.5) / 6))
    B = ((3 * arb(5).sqrt() - arb(21).sqrt()) / 12).union(arb((3 * 5 ** 0.5 - 21 ** 0.5) / 12))
    return A, B

def load_trial_q(path, N):
    """reader (f): the z9sym trial coefficients q1, q2, q3 (9 each, on BASIS) of pk11's vacres json (pinned), taken exactly: they define p0."""
    with open(path) as fh:
        d = json.load(fh)
    q = []
    for key in ('q1', 'q2', 'q3'):
        v = d.get(key)
        if not isinstance(v, list) or len(v) != 9 or not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v):
            raise Refused('vacres %s: %s is not 9 numbers' % (os.path.basename(path), key))
        q.append([arb(x) for x in v])
    return q

def s_eps(q, eps, t):
    """(G3): S_eps = sup |p0| W^eps <= 1 + sum_i t^i sum_m |q_i[m]| prod_j (d_j/(eps w_j e))^d_j, w = (A, A, B): each monomial's sup over
    xi >= 0 against e^(-eps w . xi). Nonincreasing in J, so t = 1/300 bounds every J >= 300. Refuses eps outside (0, 1)."""
    if not (eps > 0 and eps < 1):
        raise Refused('Lemma G eps outside (0, 1)')
    A, B = trial_ab()
    w, e = (A, A, B), arb(1).exp()
    S, ti = arb(1), arb(1)
    for i in range(3):
        ti = ti * t
        for c, mono in zip(q[i], BASIS):
            f = arb(1)
            for j in range(3):
                d = mono.count(j)
                for _ in range(d):
                    f = f * d / (eps * w[j] * e)
            S = S + ti * abs(c) * f
    return S

def tau_strip(ncols):
    """tau of lapl2.strip_graph(ncols), end triangles (A, A, B), interior verticals 1, horizontals 1: lam_h's graph, here for main_D (ncols 2)."""
    A, B = trial_ab()
    V = 3 * ncols
    L = arb_mat(V, V)
    E = []
    for j in range(ncols):
        T, M, Bv = 3 * j, 3 * j + 1, 3 * j + 2
        if j == 0 or j == ncols - 1:
            E += [(T, M, A), (M, Bv, A), (T, Bv, B)]
        else:
            E += [(T, M, arb(1)), (M, Bv, arb(1))]
        if j < ncols - 1:
            E += [(3 * j + r, 3 * (j + 1) + r, arb(1)) for r in range(3)]
    for a, b, c in E:
        L[a, a] += c
        L[b, b] += c
        L[a, b] -= c
        L[b, a] -= c
    return arb_mat(V - 1, V - 1, [L[i, k] for i in range(1, V) for k in range(1, V)]).det()

def lg_weights(eps, theta):
    """(G4): the triangle edge weights (TM, MB, TB) of ||W||^2 (kt_rb's phi ratio), ||W^(1-eps)||^2 and ||W_theta||^2."""
    A, B = trial_ab()
    w0 = (2 * A, 2 * A, 2 * B)
    we = (2 * (1 - eps) * A, 2 * (1 - eps) * A, 2 * (1 - eps) * B)
    wt = (2 * (1 - theta) * (1 - eps) * A, 2 * (1 - theta) * (1 - eps) * A, 2 * (1 - eps) * B)
    return w0, we, wt

def gbad_p(N, Lam, kap, u, phi_e):
    """(G1): Gbad'(Lam) = tau~0(Lam) kappa (kappa + u) sqrt(Phi_eps), for Lam >= 1."""
    if not (Lam >= 1):
        raise Refused('Lemma G level Lam below 1')
    return tail_h(N, 1, Lam, arb(0)) * kap * (kap + u) * phi_e.sqrt()

def abad_p(Lam_a, kap, u, phi_e, phi_t, eps, theta):
    """(G2): Abad'(Lam_a) = Lam_a e^(-2 Lam_a) kappa sqrt(Phi_eps) + u Lam_a e^(-2 theta (1 - eps) A Lam_a) sqrt(Phi_eps,theta), for theta in
    (0, 1), Lam_a >= 1/2 and Lam_a >= 1/(2 theta (1 - eps) A)."""
    A, _b = trial_ab()
    c = 2 * theta * (1 - eps) * A
    if not (theta > 0 and theta < 1 and Lam_a >= arb(1) / 2 and Lam_a * c >= 1):
        raise Refused('Lemma G level Lam_a below max(1/2, 1/(2 theta (1 - eps) A)), or theta outside (0, 1)')
    return Lam_a * (-2 * Lam_a).exp() * kap * phi_e.sqrt() + u * Lam_a * (-c * Lam_a).exp() * phi_t.sqrt()

def load_g00(mode, pins=None):
    """v1_17 (1), v1_20 (1): G_00's lower end per N over every J >= 300, Lemma T-prime's only J-dependent input. CERTIFIED: S7's certified g,0,0
    (g00_s7; refused only on a pin failure of a record or its asm output, or on the normalization pin). MOCK: G00_MOCK, for tests only."""
    if mode == 'CERTIFIED':
        return dict((N, g00_s7(N, pins)[0]) for N in (4, 3))
    return dict((N, arb(G00_MOCK)) for N in (4, 3))

def g00_s7(N, pins=None):
    """v1_20 (1): S7's certified g,0,0 at N (pk03: the same object as S9's G,0,0). The record and its asm output must match their pins (PINS,
    or pins for a plant), the entry must pass check_g00_entry, and its lower end over every J >= 300 is g00_lower's. Returns (lower end, value
    at J = 300, err, record)."""
    pins = PINS if pins is None else pins
    rp, ap = S7G00[N]
    for p in (rp, ap):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('S7 g,0,0 file %s does not match its pin' % os.path.basename(p))
    cf7, er7 = load_m3(rp, N, 'CERTIFIED', 300, ap)['g,0,0']
    with open(rp) as fh:
        r7 = json.load(fh)
    check_g00_entry(r7['claim'], r7['items']['g,0,0']['a0_exact'], cf7[0].lower(), cf7[0].upper())
    check_trial_set(r7, N, pins)   # v1_25 (3): main, on the note 1
    t300 = 1 / arb(300)
    v300 = arb(0)
    for a in reversed(cf7):
        v300 = v300 * t300 + a
    return check_g00(g00_lower(cf7, er7, t300)), v300, er7, r7

def check_g00(g):
    """v1_17 (1), a piece whose G_00 lower end is not certainly positive is refused."""
    if not (g > 0):
        raise Refused('G_00 lower end not certainly positive')
    return g

def check_g00_entry(claim, a0_exact, lo0, hi0):
    """v1_19 (1), the pin: an M3 G,0,0 entry (S7's g,0,0) stands for <phi_0, K phi_0>/main_D only if its record's claim starts with G00_CLAIM,
    its a0_exact is '1' and its a_0 ball is exactly 1 (the t = 0 value; a wrong main term or area factor would move it)."""
    if not (isinstance(claim, str) and claim.startswith(G00_CLAIM) and a0_exact == '1' and lo0 == 1 and hi0 == 1):
        raise Refused('G,0,0 normalization does not match the pin (claim, a0_exact or a_0)')
    return True

def g00_lower(coef, err, t_hi):
    """v1_19 (2): the lower end of sum_k a_k t^k - err over t in [0, t_hi], the cubic as a ball over the t-interval (pk03's rule)."""
    t = arb(0).union(t_hi)
    s = arb(0)
    for a in reversed(coef):
        s = s * t + a
    return (s - err).lower()

def phi_T(N, S, wT, g00):
    """v1_17 (1), Lemma T-prime (NOTE_P2_17_TRIANGLE_v1): c_K S^2 ||W'||^2/||psi-hat||^2 <= S^2 (tau_D/(w_1 w_2))^(n/2)/G_00,
    with the TB edge (the smallest weight) in the trace and (w_1, w_2) the TM and MB weights; every power of J, area and 2 pi cancels."""
    r = tau_strip(2) / (wT[0] * wT[1])
    f = r * r.sqrt() if N == 4 else r
    return S * S * f / check_g00(g00)

def check_c1(lines):
    """v1_14 (2), C-C1: the M2B record clears C1 only if exactly one of its lines starts with 'CLAIM = ' and holds C1_CLAIM, the agreed 41-byte
    string, exactly once (the same string and length check as pk07's)."""
    if len(C1_CLAIM.encode('utf-8')) != 41:
        raise Refused('C1_CLAIM is not the agreed 41-byte string')
    cl = [ln for ln in lines if ln.startswith('CLAIM = ')]
    if len(cl) != 1 or cl[0].count(C1_CLAIM) != 1:
        raise Refused('the M2B record CLAIM does not state the |g| form exactly once (C1)')
    return True

def check_trial_set(r7, N, pins=None):
    """v1_25 (3), the addition on the note 1: S7's g,0,0 serves as G_00 only if its record's trial_set names the vacres file the
    assembly pins for S_eps, VACRES[N], with its pinned sha prefix (the record writes basename:sha8). a_0 = 1 does not depend on the trial, so
    check_g00_entry cannot see a mismatch."""
    pins = PINS if pins is None else pins
    want = '%s:%s' % (os.path.basename(VACRES[N]), (pins.get(VACRES[N]) or '')[:8])
    ts = r7.get('trial_set') if isinstance(r7, dict) else None
    got = ts.get('vacres') if isinstance(ts, dict) else None
    if pins.get(VACRES[N]) is None or got != want:
        raise Refused('S7 record trial_set vacres %r is not the pinned %s' % (got, want))
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

def lemma_a_amp(RC, LA, eps_r, s, mh, NAp, HbP, GbP, AbP, Aa_hi):
    """v1_27 (1): kt_rb_v1_5's assembly_cert l.747-792 in arb on one piece, at the levels (LAM_T, LAM_A), with Iht in place of Ih (the t side),
    Lemma B's NA-prime in place of BETA_R mhat/lambda~0, and Lemma G's Hbad-prime, Gbad-prime, Abad-prime: sigma_k (C-SIGN0), the vacuum
    values |t_00| and |a_00|, the corrections Delta, the amplitude balls t~_x = t^_x + [-Delta_x, Delta_x], t~_y, a~_x, and da_x (with A_am at
    J = 300). dt_x is tprov's (it needs A_t). Returns tprov's inputs for the piece plus av0 (the vacuum bar |a^_00|) for C-NA."""
    vals, G, V = RC['vals'], RC['G'], RC['vecs']
    if not (mh > 0):   # v1_35 (4): C-MHAT, where lt0 is formed
        raise Refused('C-MHAT: mhat is not certainly positive')
    lt0 = (1 - eps_r) * mh
    sp = s * (1 + s)
    if not ((mh - vals[1].upper()) > 0):   # v1_34 (grep): C-DK0, sigma_0's Davis-Kahan denominator
        raise Refused('C-DK0: mhat - mu_x,high is not certainly positive')
    sig0 = eps_r * mh / (mh - vals[1].upper())
    ip = []
    for k in range(3):
        acc = arb(0)
        for b in range(3):
            acc = acc + G[0][b] * V[k][b]
        ip.append(acc / G[0][0].sqrt())
    if not (ip[0] > 0):
        raise Refused('C-SIGN0: <u~_0, u-hat> not certainly positive')
    s0 = sig0.upper()
    sgk = [None, _min_pt(s0, abs(ip[1]).upper()), _min_pt(s0, abs(ip[2]).upper())]
    d0 = sig0 * (1 + sig0) + sp
    tv0 = abs(mh * RC['Iht0'] / (G[0][0] * vals[0] * vals[0])).upper()
    av0 = abs(mh * RC['Dx0'] / (G[0][0] * vals[0])).upper()
    axb, ayb = abs(RC['a'][1]).upper(), abs(RC['a'][2]).upper()
    Lam, Lam_a = arb(LAM_T), arb(LAM_A)
    NH = Lam + HbP
    GP = Lam * (mh / lt0) * eps_r + GbP
    GA = Lam_a * (mh / lt0) * eps_r + AbP
    t00 = tv0 + 2 * NH * sp + GP
    dlx = NH * sp + (sp + sgk[1]) * t00 + GP
    dly = NH * sp + (sp + sgk[2]) * t00 + GP
    a00 = av0 + 2 * NAp * sp + GA
    dlax = NAp * sp + (sp + sgk[1]) * a00 + GA
    dlay = NAp * sp + (sp + sgk[2]) * a00 + GA
    q, eps0, epsy = LA['q'], LA['eps0'], LA['epsy']
    Qva = (mh / lt0) * Aa_hi + Lam_a * (mh / lt0) * eps_r + (NAp + a00) * sp + AbP
    dax = q * Qva + eps0 * (d0 * NAp) + epsy * (ayb + dlay) + (q * q + eps0 * eps0 + epsy * epsy) * (axb + dlax)
    one = arb(0, 1)
    Gr = arb_mat(3, 3, [sum((V[k][i] * G[i][j] * V[l][j] for i in range(3) for j in range(3)), arb(0)) for k in range(3) for l in range(3)])
    return dict(mhat=mh, lt0=lt0, eps_r=eps_r, sp=sp, Lam=Lam, Hbad=HbP, HbadP=HbP, Gbad=GbP, GbadP=GbP, Lam_a=Lam_a, Abad=AbP, AbadP=AbP, q=q,
                eps0=eps0, epsy=epsy,
                t0=t00, t0t=d0 * NH, tx=RC['t'][1] + one * dlx.upper(), ty=RC['t'][2] + one * dly.upper(), ax=RC['a'][1] + one * dlax.upper(), dax=dax, G=Gr,
                av0=av0, a00=a00)

def na_prime(kap):
    """v1_27 (1), Lemma B (a) (NOTE_P2_17_BETA_v1): ||T_xi_TM||/lambda_0 <= L + L e^(-L) kappa for every L >= 1, so
    NA-prime is the minimum over the grid L = 1, 9/8, ..., 20 at kappa = kappa_max, J-uniform for J >= 300 (any L >= 1 is valid, so the grid
    needs no certification). Returns (NA-prime as an upper end, its L)."""
    best = None
    for k in range(8, 161):
        L = arb(k) / 8
        v = (L + L * (-L).exp() * kap).upper()
        if best is None or v < best[0]:
            best = (v, L)
    return best

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

def _gam_up(N, s2, L):
    """Gamma(s2/2, L) for s2 in {3, 5, 7}, closed forms through erfc (C-GAMMA checks Gamma(3/2, 5) against flint)."""
    sq = L.sqrt()
    g = sq * (-L).exp() + arb.const_sqrt_pi() / 2 * sq.erfc()
    if s2 >= 5:
        g = L * sq * (-L).exp() + arb(3) / 2 * g
    if s2 >= 7:
        g = L * L * sq * (-L).exp() + arb(5) / 2 * g
    return g

def tail_h(N, m, L, cl):
    """the horizontal Schur slot int_{xi > L} (xi - cl)^m e^-xi dmu / k1 (m = 1 with cl = 0, or m = 2), at J = 300, hence for every J >= 300."""
    if N == 3:
        x = L - cl
        poly = (x + 1) if m == 1 else (x * x + 2 * x + 2)
        return poly * (-L).exp() / (1 - arb(-600).exp())
    j0 = arb(300)
    low = arb.const_sqrt_pi() / 2 * j0.sqrt().erf() - j0.sqrt() * (-j0).exp()
    if m == 1:
        num = _gam_up(N, 5, L) - cl * _gam_up(N, 3, L)
    else:
        num = _gam_up(N, 7, L) - 2 * cl * _gam_up(N, 5, L) + cl * cl * _gam_up(N, 3, L)
    return arb(2).sqrt() * num / low

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

# ---- CORE defs (pk25's C6a engine)
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

# ---- pk25's C6b code


def check_core2(tamper=None):
    """C-CORE: every copied R4 def and constant equals R4's (pinned) source text, and every copied C6a def and constant equals
    kt_s9h_asm_v1_5's (pinned), each defined exactly once in both files. tamper (PLANT-CORE) changes one character of one copy."""
    if sha_file(R4_PATH) != R4_SHA or sha_file(C6A_PATH) != C6A_SHA:
        raise Refused('C-CORE: R4 or the C6a engine does not match its pin')
    me, dm = segments(open(SELF).read())
    if tamper:
        k0 = C6A_DEFS[0]
        me = dict(me, **{k0: me[k0].replace('(', '[', 1)})
    bad, n = [], 0
    for path, defs, consts in ((R4_PATH, CORE_DEFS, CORE_CONSTS), (C6A_PATH, C6A_DEFS, C6A_CONSTS_N)):
        src, ds = segments(open(path).read())
        for k in list(defs) + ['=' + c for c in consts]:
            n += 1
            if k in ds or k in dm or src.get(k) is None or me.get(k) != src.get(k):
                bad.append(k)
    if bad:
        raise Refused('C-CORE: %d of %d copies differ or are defined twice: %s' % (len(bad), n, ' '.join(bad[:6])))
    return n


def load_rdr(pins=None):
    """pk25's reader fork m3_reader_s9h_v1 (pinned), imported once."""
    pins = PINS if pins is None else pins
    if pins.get(RDR) is None or sha_file(RDR) != pins[RDR]:
        raise Refused('C-RDR: the reader fork does not match its pin')
    import importlib.util
    spec = importlib.util.spec_from_file_location('m3_reader_s9h_v1', RDR)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    return mod


def load_laws(RD, N, pins=None):
    """the records and law certificates of N through the reader fork: S8's D, E2, E3, FF (certificate m3_lawcert_v1_1), S8's N (v1_2) and
    pk25's NIH, NHT, DH (m3_lawcert_s9h_v1_1); every record and job output pinned, check_s9_trial on every record. Returns
    {family: (record, certificate)}."""
    pins = PINS if pins is None else pins
    out_ = {}
    groups = ((('D', 'E2', 'E3', 'FF'), S8REC[N], S8CERT[N]['v1_1']), (('N',), S8REC[N], S8CERT[N]['v1_2']), (('NIH', 'NHT', 'DH'), HREC[N], HCERT[N]))
    for fams, recmap, (cp, co) in groups:
        recs = {}
        for F in fams:
            rp, ap = recmap[F]
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


def ritz_entries(RD, LW, tb, t_hi, J_lo):
    """the 18 RITZ_KEYS balls on the piece: G,b,c from S8 D's g,b,c, T,b,c from S8 N's T,b,c, Iht,b from pk25's Ih,b (NIH) and Dx,b from S8 D's
    DY,b (the S9 record's aliases), each by entry_law_piece."""
    B = {}
    for k in RITZ_KEYS:
        fam, key = k.split(',', 1)
        if fam == 'G':
            F, kk = 'D', 'g,' + key
        elif fam == 'T':
            F, kk = 'N', 'T,' + key
        elif fam == 'Iht':
            F, kk = 'NIH', 'Ih,' + key
        else:
            F, kk = 'D', 'DY,' + key
        rec, cert = LW[F]
        B[k] = entry_law_piece(RD.entry_law(cert, F, kk), tb, t_hi, J_lo)
    return B


def check_alias(LW, RE):
    """C-ALIAS: the S8 entries used for G, T and Dx carry the same ak as the S9 record's entries (load_ritz), so the Ritz problem is the S9
    records' (C6a's) with law-based bars."""
    bad = []
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    for k in RITZ_KEYS:
        fam, key = k.split(',', 1)
        if fam == 'Iht':
            continue
        F, kk = {'G': ('D', 'g,'), 'T': ('N', 'T,'), 'Dx': ('D', 'DY,')}[fam]
        ak = LW[F][1]['entries']['%s:%s%s' % (F, kk, key)]['ak']
        mine = RE[k][0]
        if len(ak) != len(mine) or any(not (q(a).lower() >= m.lower() - arb('1e-30') and q(a).upper() <= m.upper() + arb('1e-30')) for a, m in zip(ak, mine)):
            bad.append(k)
    if bad:
        raise Refused('C-ALIAS: %s differ from the S9 record' % ' '.join(bad))
    return True


def load_m4h(pins=None):
    """M4H_KV_v1 through pk25's m4h_reader_v1_1 (load binds the record to its asm output; law returns L_k at J)."""
    pins = PINS if pins is None else pins
    for p in (M4H[0], M4H[1], M4H_READER_PATH):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('C-M4H-READ: %s does not match its pin' % os.path.basename(p))
    import importlib.util
    spec = importlib.util.spec_from_file_location('m4h_reader_v1_1', M4H_READER_PATH)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    try:
        rec = m4_call(mod.load, M4H[0], M4H[1], pins[M4H[0]], pins[M4H_READER_PATH])
    except Exception as e:
        raise Refused('C-M4H-READ: m4h_reader_v1_1.load: %s' % e)
    return rec, mod


def lg_constants(M2MOD, M2R):
    """Lemma G and B constants per N, as R4 forms them: eps_r at J = 300, kappa_max, S_eps, G_00, Phi_eps, Phi_eps,theta, Hbad', Gbad', Abad',
    NA-prime. Returns {N: dict}."""
    epsg, thg = arb(EPS_G), arb(THETA_G)
    w0, we, wt = lg_weights(epsg, thg)
    G00 = load_g00('CERTIFIED')
    C = {}
    for N in (4, 3):
        er300 = m2b_eps(m2b_call(M2MOD.law_v1, M2R, N, 300))
        kap = kappa_bound(N, er300[0])
        S = s_eps(load_trial_q(VACRES[N], N), epsg, 1 / arb(300))
        g00 = check_g00(G00[N])
        pe, pt = phi_T(N, S, we, g00), phi_T(N, S, wt, g00)
        uC = 1 / (1 - er300[0])
        C[N] = dict(er300=er300, kap=kap, S=S, g00=g00, pe=pe, pt=pt, uC=uC,
                    HBP=tail_h(N, 1, arb(LAM_T), arb(0)) * kap * kap, GBP=gbad_p(N, arb(LAM_T), kap, uC, pe),
                    ABP=abad_p(arb(LAM_A), kap, uC, pe, pt, epsg, thg), NAP=na_prime(kap))
    return C


def check_r4_lg(C):
    """C-R4-LG: the constants equal R4's certified run output (PHI-EPS lines: S_eps, G_00, Phi_eps, Phi_eps,theta; C-NA lines: NA-prime and
    kappa_max), as the same decimal strings by dec_hi / dec_lo."""
    if PINS.get(R4_CERT_OUT) is None or sha_file(R4_CERT_OUT) != PINS[R4_CERT_OUT]:
        raise Refused('C-R4-LG: R4\'s certified run output does not match its pin')
    L = lines_of(R4_CERT_OUT)
    bad = []
    for N in (4, 3):
        c = C[N]
        ph = [x for x in L if x.startswith('PHI-EPS N=%d ' % N)]
        na = [x for x in L if x.startswith('C-NA N=%d: ' % N)]
        want_ph = 'S_eps <= %s, G_00 >= %s, Phi_eps <= %s, Phi_eps,theta <= %s' % (dec_hi(c['S']), dec_lo(c['g00']), dec_hi(c['pe']), dec_hi(c['pt']))
        want_na = 'NA-prime (Lemma B) = %s at L = %s with kappa_max %s;' % (dec_hi(c['NAP'][0]), c['NAP'][1].str(5, radius=False), dec_hi(c['kap']))
        if len(ph) != 1 or want_ph not in ph[0]:
            bad.append('PHI-EPS N=%d' % N)
        if len(na) != 1 or want_na not in na[0]:
            bad.append('C-NA N=%d' % N)
    if bad:
        raise Refused('C-R4-LG: %s differ from R4\'s certified run output' % ' '.join(bad))
    return True


def load_lemmap():
    """MR_LEMMAP v2 (pinned): {key: {field: Fraction or token}}, with its header's FORMAT checked."""
    if PINS.get(LEMMAP) is None or sha_file(LEMMAP) != PINS[LEMMAP]:
        raise Refused('C-LEMMAP: MR_LEMMAP.kv does not match its pin')
    head, flds, rows = {}, None, {}
    for ln in lines_of(LEMMAP):
        if not ln.strip() or ln.startswith('#'):
            continue
        k, v = [x.strip() for x in ln.split('=', 1)]
        if k == 'FIELDS':
            flds = v.split()
        elif flds is None:
            head[k] = v
        else:
            rows[k] = dict(zip(flds, v.split()))
    if head.get('FORMAT') != 'MR_LEMMAP_KV_v2' or head.get('EXPORT_STATUS') != 'CERTIFIED' or head.get('RUN_VERDICT') != 'VALID':
        raise Refused('C-LEMMAP: MR_LEMMAP.kv is not a certified MR_LEMMAP_KV_v2 record')
    return rows


def load_mu(pins=None):
    """pk25's mu tool (C8, pinned; S9C v1_6: kt_mu_hw_v1_1, the K >= -3/2 condition of the review's N-1, equal to v1 on every set): one_row(N, t,
    c_lo, c_hi) bounds OR = sup_l |m(l) - c| a_l^1/2 = |M_c K^1/2| (a_0 = 1) on every J with 1/J <= t (nondecreasing in t)."""
    pins = PINS if pins is None else pins
    if pins.get(MU) is None or sha_file(MU) != pins[MU]:
        raise Refused('C-MU: the mu tool does not match its pin')
    import importlib.util
    spec = importlib.util.spec_from_file_location('kt_mu_hw_v1', MU)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    return mod


def piece_t(jlo, jhi):
    """a grid piece's t ends (exact arb points, t_ends's readings) and its J lower end for the laws (grid_j's smaller reading)."""
    tl, th = t_ends(jlo, jhi)
    return tl, th, grid_j(jlo, True)


def h_piece(N, tl, th, JL, key, IN, mode='full', plant=None, s9c=None):
    """h's quantities on the t range [tl, th] (exact arb points; JL the J lower end, a Fraction or int, for the laws and the lawcerts).
    mode 'c0' returns only c~_h = <u~_0, M_h u~_0> (the Ritz-level mean); 'full' returns every MR_INSERT(h) quantity. key names the
    MR_LEMMAP row (the grid piece) whose L_k serve. Per-piece gates raise Refused. v1_3: vx, vy are MR_INSERT's unwindowed amplitudes
    <u_a, v> (the windowed <u_a, S v> of R4's frame divided by the piece's s_a enclosure; vxw, vyw keep the windowed ones); Pevw bounds
    |P_e S v|, Pev and vp the unwindowed |P_e v| and |v+|. v1_4: win = C tau4^3/2 >= |P_e B^w P_e| (beta_perp). v1_5: uhat, the
    unit-basis Ritz coefficients uhat_kb = c_kb |psi_b| of the law-based Ritz problem (MR_LEMMAP's u_kb form), for the width comparison.
    S9C v1_6: s9c (None, or s9c_htx) gives S9(c)-h's Ritz-level x amplitude h~_x in the orientation from this piece's quantities (H^Q, X
    and the Lemma A inputs below); Lemma A at level x with |h~_x| as its own amplitude (the k = 0, y amplitudes stay S9(b)'s), the
    windowed and unwindowed S9(c) v_x are returned under 'S9' next to S9(b)'s vx, vxw (unchanged)."""
    tb = tl.union(th)
    B = ritz_entries(IN['RD'], IN['LW'][N], tb, th, JL)
    mh = mhat_ball(IN['MC'][N], tb)
    er, s_, sp = m2b_eps(m2b_call(IN['M2MOD'].law_v1, IN['M2R'], N, JL))
    Rb12 = (m4_law(IN['M4REC'], IN['M4MOD'], 'e1', N, JL), m4_law(IN['M4REC'], IN['M4MOD'], 'e3', N, JL))
    RC = ritz_piece(B, mh)
    sx_, sy_ = IN['SIG'][N]
    G = RC['G']
    V = [RC['vecs'][0], [x if sx_ == 1 else -x for x in RC['vecs'][1]], [x if sy_ == 1 else -x for x in RC['vecs'][2]]]   # exact negation
    if plant == 'ORIENT':
        V = [V[0], [-x for x in V[1]], V[2]]
    check_orient(V, G, IN['TS'][N])
    uhat = [[V[k][i] * G[i][i].sqrt() for i in range(3)] for k in range(3)]   # v1_5: MR_LEMMAP's unit-basis coefficients (C6a's form), law-based
    GX = [[entry_law_piece(IN['RD'].entry_law(IN['LW'][N]['DH'][1], 'DH', 'Gxh,%d,%d' % (min(b, c), max(b, c))), tb, th, JL) for c in REVEN] for b in REVEN]
    quad = lambda a, b: sum((V[a][i] * V[b][j] * GX[i][j] for i in range(3) for j in range(3)), arb(0))
    ch0 = quad(0, 0)
    if mode == 'c0':
        return dict(ch0=ch0)
    Aa = m4_law(IN['M4REC'], IN['M4MOD'], 'am', N, JL)
    Ah = m4_law(IN['M4HREC'], IN['M4HMOD'], 'h', N, JL)
    tau = IN['TAU4A'][N]
    LA = lemma_a_cbar(RC, er, Rb12, None, tau)
    tau_hi = tau.upper()
    s_x, mu_y, m0lo = LA['s_x'], LA['mu_y'], LA['m0lo'].lower()
    mu_lo = [m0lo, (s_x.lower() * m0lo).lower(), (mu_y.lower() * m0lo).lower()]
    mu_hi = [arb(1), s_x.upper(), mu_y.upper()]
    s_lo = [arb(1), mu_lo[1], mu_lo[2]]
    s_hi = [arb(1), LA['sxhi'].upper(), LA['syhi'].upper()]
    rho = [r.upper() for r in LA['rho']]
    if not (tau_hi < s_lo[2] and s_hi[2] < s_lo[1] and s_hi[1] < mu_lo[0]):
        raise Refused('C-ORDER: tau4 < s_y,lo, s_y,hi < s_x,lo < s_x,hi < mu_0,lo does not hold')
    L3 = dict((a, l3_level(a, rho, s_lo, s_hi, mu_lo, mu_hi, tau_hi)) for a in range(3))
    delta = [(2 * (L3[a][0] * L3[a][0] + sum((L3[a][1][k] * L3[a][1][k] for k in L3[a][1]), arb(0)))).sqrt().upper() for a in range(3)]
    C = IN['LG'][N]
    IP = lemma_a_amp(RC, LA, er, s_, mh, C['NAP'][0], C['HBP'], C['GBP'], C['ABP'], Aa)
    Q = qv4(Ah, IP)
    hx, hy, h0t = IP['tx'], IP['ty'], IP['t0t']
    ax, ay, a0t = abs(hx).upper(), abs(hy).upper(), abs(h0t).upper()
    dh = []
    for a, own, others in ((1, ax, {0: a0t, 2: ay}), (2, ay, {0: a0t, 1: ax})):
        q, eps = L3[a][0], L3[a][1]
        d = q * Q + sum((eps[k] * others[k] for k in eps), arb(0)) + (q * q + sum((eps[k] * eps[k] for k in eps), arb(0))) * own
        dh.append(d.upper())
    one = arb(0, 1)
    vxw = (hx if sx_ == 1 else -hx) + dh[0] * one   # <u_x, S v>: R4's paper frame, v_e = S v for a horizontal insertion
    vyw = (hy if sy_ == 1 else -hy) + dh[1] * one
    sxb, syb = s_lo[1].union(s_hi[1]), s_lo[2].union(s_hi[2])
    vx, vy = vxw / sxb, vyw / syb   # v1_3: MR_INSERT's unwindowed <u_a, v> = <u_a, S v> / s_a (G6 v1_6_1 sect. 1, Frames)
    lm = IN['LM'][key]
    Lk = [arb(lm['L%s_hi' % k]) for k in KNAME]
    if lm['tau_hi'] != IN['TOK'][N]:
        raise Refused('C-LEMMAP-ROW: MR_LEMMAP row %s carries another tau_hi' % key)
    PevwL = (Q + a0t * Lk[0] + ax * Lk[1] + ay * Lk[2]).upper()   # v1_3: Lemma P on the windowed vector S v (Q = |Q_W S v|)
    SH = [entry_law_piece(IN['RD'].entry_law(IN['LW'][N]['DH'][1], 'DH', 'Sh,%d' % b), tb, th, JL) for b in REVEN]
    if not all(x > 0 for x in SH):
        raise Refused('C-SH-POS: an Sh entry is not certainly positive')
    kap = [sum((abs(V[a][i]).upper() * SH[i].upper().sqrt().upper() for i in range(3)), arb(0)).upper() for a in range(3)]
    Cc, OR = IN['CC'][N], IN['OR'][N]
    dc = (delta[0] * (Cc + OR * kap[0])).upper()
    ch = ch0 + dc * one
    Pev = pev_route(N, tb, IN, uhat[0], Cc, delta[0], ch, vx, vy, ('Mh,0,0', 'Mhh,0,0'), 'LH')   # v2_3: option (B) with Lemma RHO (v1_3: C)
    Pevw = PevwL if PevwL < (tau_hi * Pev).upper() else (tau_hi * Pev).upper()   # |P_e S v|: Lemma P on S v, or tau4 |P_e v|
    vpa = (abs(vx).upper() * abs(vx).upper() + abs(vy).upper() * abs(vy).upper() + Pev * Pev).sqrt().upper()
    vp = Cc if Cc < vpa else vpa   # |v+|^2 = v_x^2 + v_y^2 + |P_e v|^2, and |v+| <= |v| <= C
    if not (IN['CI'][N][0] < ch and ch < IN['CI'][N][1]):
        raise Refused('C-CH-HULL: c_h is not inside the interval the mu tool used')
    m = {}
    for a, b in ((1, 1), (1, 2), (2, 2)):
        mt = quad(a, b) - (ch if a == b else 0)
        e1 = delta[a] * Cc / s_lo[b].sqrt() + OR * kap[a] * delta[b]
        e2 = delta[b] * Cc / s_lo[a].sqrt() + OR * kap[b] * delta[a]
        e = (e1.upper() if e1.upper() < e2.upper() else e2.upper())
        m[(a, b)] = mt + e * one
    pebw = []
    for a in (1, 2):
        f1 = (tau_hi * Cc * s_hi[a].sqrt()).upper()
        f2 = (s_hi[a] * (tau_hi * OR * kap[a] + Cc * delta[a])).upper()
        pebw.append(f1 if f1 < f2 else f2)
    win = (Cc * tau_hi * tau_hi.sqrt()).upper()   # v1_4: beta_perp >= |P_e B^w P_e| = |P_e S M_c S P_e| <= |S P_e| |M_c S P_e| <= tau4 C tau4^1/2
    if not (win < (Cc * s_hi[1] * s_hi[1].sqrt()).upper()):
        raise Refused('C-WIN: C tau4^3/2 is not below C s_x^3/2')
    T_, A_ = ta_rows(N, RC, LA, L3, delta, kap, er, s_, sp, mh, tb, th, JL, key, IN, V, s_lo, s_hi, tau_hi, Lk) if mode == 'full' else (None, None)
    S9 = None
    if s9c is not None:   # S9C v1_6: S9(c)-h's h~_x, then Lemma A at level x as above with its own amplitude
        S9 = s9c(N, tl, th, JL, IN, dict(RC=RC, LA=LA, L3=L3, delta=delta, Q=Q, Cc=Cc, OR=OR, ch=ch, m=m, pebw=pebw, s_hi=s_hi, mu_hi=mu_hi,
                                         rho=rho, tau_hi=tau_hi, vx=vx, er=er, Rb12=Rb12, m0lo=m0lo, SH=SH, mh=mh))
        hc = S9['htx']
        q, eps = L3[1][0], L3[1][1]
        others = {0: a0t, 2: ay}
        dhc = (q * Q + sum((eps[k] * others[k] for k in eps), arb(0)) + (q * q + sum((eps[k] * eps[k] for k in eps), arb(0))) * abs(hc).upper()).upper()
        S9['dhx'] = dhc
        S9['vxw'] = hc + dhc * one
        S9['vx'] = S9['vxw'] / sxb
    return dict(vx=vx, vy=vy, vxw=vxw, vyw=vyw, uhat=uhat, Pev=Pev, Pevw=Pevw, PevwL=PevwL, vp=vp, Q=Q, dlx=IP['tx'].rad(), dhx=dh[0], dhy=dh[1], ch=ch, ch0=ch0, dc=dc, kap=kap, t=T_, a=A_,
                delta=delta, m=m, pebw=pebw, win=win, s_lo=s_lo, s_hi=s_hi, Ah=Ah, q=[L3[a][0] for a in range(3)], S9=S9,
                RC=RC, B=B, m0lo=m0lo, a0t=a0t, ax=ax, ay=ay)   # v2_5: the piece's Ritz data and Lemma A's O(1) amplitude bounds for waya_last


def agg(Ds):
    """one piece's quantities from its sub-pieces: hulls of the intervals, maxima of the upper bounds."""
    mx = lambda a, b: a.upper() if a.upper() >= b.upper() else b.upper()
    D = dict(Ds[0])
    for E in Ds[1:]:
        for k in ('vx', 'vy', 'vxw', 'vyw', 'ch', 'ch0'):
            D[k] = D[k].union(E[k])
        for k in ('Pev', 'Pevw', 'PevwL', 'vp', 'Q', 'dhx', 'dhy', 'dc', 'win', 'Ah'):
            D[k] = mx(D[k], E[k])
        D['m'] = dict((ab, D['m'][ab].union(E['m'][ab])) for ab in D['m'])
        D['uhat'] = [[D['uhat'][k][i].union(E['uhat'][k][i]) for i in range(3)] for k in range(3)]
        D['pebw'] = [mx(D['pebw'][i], E['pebw'][i]) for i in range(2)]
        D['kap'] = [mx(D['kap'][i], E['kap'][i]) for i in range(3)]
        D['delta'] = [mx(D['delta'][i], E['delta'][i]) for i in range(3)]
    return D


def last_piece_floor(N, tl, th, key, IN, ratio=Fraction(101, 100), t_min=Fraction(1, 10 ** 13), s9c=None):
    """Way B on the piece whose t range starts at 0 (the row 4325), on the unwindowed v_x (v1_3): sub-pieces [t_(k+1), t_k] with
    t_0 = th, t_(k+1) = t_k/ratio down to t_min, and [0, t_min]; v_x on each by h_piece. f = F0 + t_min max(|g_lo|, |g_hi|) with F0 >= |v_x| on [0, t_min]; g_lo, g_hi such that
    t g_lo - f <= v_x(t) <= t g_hi + f on every sub-piece (the end of the sub-piece chosen by the sign of v_x -+ f). Returns
    (g_lo, g_hi, f, F0, number of sub-pieces, the hull of v_x and v_y over the piece). S9C v1_6: with s9c, v_x is S9(c)'s (h_piece's
    'S9' entry) on every sub-piece; any ratio > 1 is valid."""
    vxof = (lambda D: D['S9']['vx']) if s9c is not None else (lambda D: D['vx'])
    if not (tl == 0):
        raise Refused('last_piece_floor: the piece does not start at t = 0')
    ts = [th]
    tk = th
    while True:
        nxt = (tk / q2arb(ratio)).upper()
        if not (nxt > q2arb(t_min)):
            break
        ts.append(nxt)
        tk = nxt
    tz = q2arb(t_min)
    ts.append(tz)
    subs = []
    for k in range(len(ts) - 1):
        hi_, lo_ = ts[k], ts[k + 1]
        JL = Fraction(int((1 / hi_).lower().floor().unique_fmpz()))
        D = h_piece(N, lo_, hi_, JL, key, IN, mode='hx', s9c=s9c)
        subs.append((lo_, hi_, D))
    J0 = Fraction(int((1 / tz).lower().floor().unique_fmpz()))
    D0 = h_piece(N, arb(0), tz, J0, key, IN, mode='hx', s9c=s9c)
    F0 = max(abs(vxof(D0).lower()), abs(vxof(D0).upper())).upper()
    f = F0
    for _it in range(3):
        glo = ghi = None
        for lo_, hi_, D in subs:
            a = vxof(D).lower() + f
            g1 = (a / (hi_ if a >= 0 else lo_)).lower()
            b = vxof(D).upper() - f
            g2 = (b / (lo_ if b >= 0 else hi_)).upper()
            glo = g1 if glo is None or g1 < glo else glo
            ghi = g2 if ghi is None or g2 > ghi else ghi
        fn = (F0 + tz * (abs(glo) if abs(glo) > abs(ghi) else abs(ghi))).upper()
        if fn <= f:
            break
        f = fn
    if not (f >= (F0 + tz * (abs(glo) if abs(glo) > abs(ghi) else abs(ghi))).upper()):
        raise Refused('C-FLOOR: the floor does not cover [0, t_min] after three passes')
    vxh = vxof(D0)
    vyh = D0['vy']
    for _lo, _hi, D in subs:
        vxh, vyh = vxh.union(vxof(D)), vyh.union(D['vy'])
    return glo, ghi, f, F0, len(subs) + 1, vxh, vyh, subs, D0


def load_sv2(P, pins=None):
    """the S_V export's Bp_hi and vp2_hi per piece (C6a's load_sv pattern: pins, check_tau_trial, kt_s67_export_reader_v2_1.load with rule V2,
    the grid index for index with the same doubles, each token on the export's own line equal to the reader's positive value).
    Returns {N: {idx: {field: (Fraction, token)}}}."""
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
    names = ('Bp_hi', 'vp2_hi')
    if any(f not in ex['fields'] for f in names):
        raise Refused('C-SV-READ: the S_V export lacks Bp_hi or vp2_hi')
    fi = dict((f, ex['fields'].index(f)) for f in names)
    lab = {}
    for x in lines_of(S67[0]):
        mm = re.match(r'N([34])_P([0-9]{4}) = (.*)$', x)
        if mm:
            lab[(int(mm.group(1)), int(mm.group(2)))] = mm.group(3).partition(' | ')[0].split(' ')
    res = {}
    for N in (4, 3):
        pcs = ex['pieces'].get(N, {})
        if len(pcs) != len(P[N]):
            raise Refused('C-SV-READ: piece count at N=%d' % N)
        res[N] = {}
        for i, (idx, jlo, jhi) in enumerate(P[N]):
            e = pcs[i]
            if e['jlo'] != float(jlo) or e['jhi'] != (math.inf if jhi == 'inf' else float(jhi)):
                raise Refused('C-SV-READ: the S_V grid differs at N=%d piece %s' % (N, idx))
            tk = lab.get((N, i))
            d = {}
            for f in names:
                v, tok = e[f], tk[fi[f]]
                if Fraction(tok) != v or not (v > 0):
                    raise Refused('C-SV-COPY: N=%d piece %s field %s' % (N, idx, f))
                d[f] = (v, tok)
            res[N][idx] = d
    return res


def load_means(P, pins=None):
    """R4's certified means export EXPORT_P2_14_MEANS_v1 (pinned): {N: {idx: (ce_lo, ce_hi, cf_lo, cf_hi)}} with ce = c_t from the D3 rows and
    cf = c_b, the vertical edge's mean, from the D4 rows (c_a = c_b by the flip); FORMAT, RECORD, EXPORT_STATUS, RUN_VERDICT and the grid tokens
    of every row checked against R4's grid. Means only: no sign is read from it (the row 4326)."""
    pins = PINS if pins is None else pins
    if pins.get(MEANS) is None or sha_file(MEANS) != pins[MEANS]:
        raise Refused('C-MEANS: the means export does not match its pin')
    head, rows = {}, {}
    for ln in lines_of(MEANS):
        if not ln.strip() or ln.startswith('#'):
            continue
        k, v = ln.split(' = ', 1)
        if re.match(r'^N[34]_D(3|4|4M)_P[0-9]{4}$', k):
            rows[k] = v.split()
        else:
            head[k] = v
    if head.get('RECORD') != 'EXPORT_P2_14_MEANS_v1' or head.get('EXPORT_STATUS') != 'CERTIFIED' or head.get('RUN_VERDICT') != 'VALID' or \
            head.get('FIELDS') != 'jlo jhi ce_lo ce_hi cf_lo cf_hi Cov_inf_lo Cov_inf_hi':
        raise Refused('C-MEANS: the means export header is not the certified EXPORT_P2_14_MEANS_v1')
    out_ = {}
    for N in (4, 3):
        out_[N] = {}
        for idx, jlo, jhi in P[N]:
            r3, r4 = rows.get('N%d_D3_P%s' % (N, idx)), rows.get('N%d_D4_P%s' % (N, idx))
            if r3 is None or r4 is None or (r3[0], r3[1]) != (jlo, jhi) or (r4[0], r4[1]) != (jlo, jhi):
                raise Refused('C-MEANS: no D3/D4 row on the grid for N=%d piece %s' % (N, idx))
            out_[N][idx] = (arb(r3[2]), arb(r3[3]), arb(r4[4]), arb(r4[5]))
    return out_


def load_dj(RD, pins=None):
    """pk22's c3j DJ records (DJREC, pinned) through the reader fork's certified load with their asm outputs, check_s9_trial on each:
    DHT,a,b = <psi_a, M_t psi_b> with t on the top-row bond (0,3) of the D vertex graph, D-normalised, in the stored basis {0, 1, 3}
    (pk22's message; the records carry no law certificate, so their uniform bars serve). Returns {N: record}."""
    pins = PINS if pins is None else pins
    res = {}
    for N in (4, 3):
        rp, ap = DJREC[N]
        for p in (rp, ap):
            if pins.get(p) is None or sha_file(p) != pins[p]:
                raise Refused('C-DJ-READ: %s does not match its pin' % os.path.basename(p))
        with open(rp) as fh:
            check_s9_trial(json.load(fh), N, pins)
        try:
            res[N] = RD.load(rp, ap, 300, N)
        except Exception as e:
            raise Refused('C-DJ-READ: load %s: %s' % (os.path.basename(rp), e))
        miss = [b for b in REVEN for c in REVEN if 'DHT,%d,%d' % (min(b, c), max(b, c)) not in res[N]['balls']]
        if miss:
            raise Refused('C-DJ-READ: a DHT entry is missing at N=%d' % N)
    return res


def dj_piece(RD, rec, key, tb):
    """a DJ entry over the piece: sum_k [LO_k, HI_k] t^k on the t-ball plus the record's constant bar err_b (entry_ball's form, t <= 1/300)."""
    LO, HI, eb = RD.entry_ball(rec, key)
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    s = arb(0)
    for lo, hi in reversed(list(zip(LO, HI))):
        s = s * tb + q(lo).union(q(hi))
    return s + q(eb).upper() * arb(0, 1)


def load_pevb(RD, pins=None):
    """v2_3: pk23's option (B) records (PEVB, pinned) through the reader fork's certified load with their asm outputs, check_s9_trial on
    each, every key of PEVB_KEYS present. Returns {N: {family: record}}."""
    pins = PINS if pins is None else pins
    res = {}
    for N in (4, 3):
        res[N] = {}
        for fam in ('L', 'LH', 'LT'):
            rp, ap = PEVB[N][fam]
            for p in (rp, ap):
                if pins.get(p) is None or sha_file(p) != pins[p]:
                    raise Refused('C-PEVB-READ: %s does not match its pin' % os.path.basename(p))
            with open(rp) as fh:
                check_s9_trial(json.load(fh), N, pins)
            try:
                rec = RD.load(rp, ap, 300, N)
            except Exception as e:
                raise Refused('C-PEVB-READ: load %s: %s' % (os.path.basename(rp), e))
            miss = [k for k in PEVB_KEYS[fam] if k not in rec['balls']]
            if miss:
                raise Refused('C-PEVB-READ: %s lacks %s at N=%d' % (os.path.basename(rp), ', '.join(miss), N))
            res[N][fam] = rec
    return res


def load_rho(path=None, pins=None):
    """v2_3: Lemma RHO's certified record (pinned): (RHO_HI, J0) as exact Fractions; FORMAT RHO_KV_v1, STATUS CERTIFIED, RUN_VERDICT VALID."""
    path = RHOREC if path is None else path
    pins = PINS if pins is None else pins
    if pins.get(path) is None or sha_file(path) != pins[path]:
        raise Refused('C-RHO: %s does not match its pin' % os.path.basename(path))
    d = {}
    for ln in lines_of(path):
        if ln.startswith('#') or ' = ' not in ln:
            continue
        k, v = ln.split(' = ', 1)
        d[k] = v
    if d.get('FORMAT') != 'RHO_KV_v1' or d.get('STATUS') != 'CERTIFIED' or d.get('RUN_VERDICT') != 'VALID':
        raise Refused('C-RHO: %s is not a certified VALID RHO_KV_v1 record' % os.path.basename(path))
    return Fraction(d['RHO_HI']), Fraction(d['J0'])


def pev_route(N, tb, IN, uh0, Cc, d0, c, vx, vy, keys, fam):
    """v2_3: option (B)'s |P_e v| bound on one piece (the rows 4422, 4426; pk25/rho/RHO_LEMMA_v1.md sect. 4). e_k = E_k / E_0 with E_0 =
    TT,0,0 (family L) and E_1, E_2 the family's k = 1, 2 entries (the xi and xi^2 insertions) over the piece's t-ball; since |S| <= 1,
    |M_c S psi-hat|^2 <= |M_c S psi-hat|^2 / |S psi-hat|^2 <= (c - e_1)^2 + e_2 - e_1^2 - 2 e_1 + (N - 1)/2 + rho (Lemma RHO's corollary, c
    over its ball); V = |u00| (that)_+^1/2 + C (|u01| + |u03|) + C delta_0 >= |M_c S u~_0| + C delta_0 >= |v| >= |P_e v| (v2_4: the rho
    note's sect. 4 form, the row 4520; the positive part over c's ball); returns min(C, V). vx, vy are unused."""
    RD, PB = IN['RD'], IN['PB'][N]
    E0 = dj_piece(RD, PB['L'], 'TT,0,0', tb)
    E1 = dj_piece(RD, PB[fam], keys[0], tb)
    E2 = dj_piece(RD, PB[fam], keys[1], tb)
    if not (E0 > 0):
        raise Refused('C-PEVB-POS: TT,0,0 is not certainly positive at N=%d' % N)
    e1, e2 = E1 / E0, E2 / E0
    rho = arb(IN['RHO'][0].numerator) / arb(IN['RHO'][0].denominator)
    rad = ((c - e1) * (c - e1) + e2 - e1 * e1 - 2 * e1 + arb(N - 1) / 2 + rho).upper()
    if rad < 0:
        raise Refused('C-PEVB-POS: the second-moment bound is certainly negative at N=%d (inconsistent inputs)' % N)
    rad = rad if rad > 0 else arb(0)   # v2_4: the positive part over c's ball before the square root
    V = (abs(uh0[0]).upper() * rad.sqrt() + Cc * (abs(uh0[1]).upper() + abs(uh0[2]).upper()) + Cc * d0).upper()
    return V if V < Cc else Cc   # v2_4: |P_e v| <= |v| <= V, no subtraction (the row 4520)


def rows_val(rows, key, i):
    """v2_4: the decimal string of field i on the row key."""
    return [v for k, v in rows if k == key][0][i]


def t048(rows, ipev, thr):
    """v2_4: gate C-PEVB-T048 (the row 4520): every t row's Pev_hi <= thr, exactly."""
    hi = [(Fraction(v[ipev]), k) for k, v in rows if k.endswith('_t') and Fraction(v[ipev]) > thr]
    if hi:
        raise Refused('C-PEVB-T048: %d t rows have Pev_hi above %s (largest %s on %s)' % (len(hi), thr, float(max(hi)[0]), max(hi)[1]))


def ta_rows(N, RC, LA, L3, delta, kap, er, s_, sp, mh, tb, th, JL, key, IN, V, s_lo, s_hi, tau_hi, Lk):
    """the t and a quantities on one t range, in the orientation (V already flipped; t~ and a~ come in R4's stored-state frame from
    lemma_a_amp and are flipped here by the same signs). Returns ({t fields}, {a fields}). v1_3: t is horizontal, so its amplitudes are
    divided by the s_a enclosures (MR_INSERT's unwindowed frame) and Pevw, Pev, vp are formed as h_piece's; a is vertical (w_e = 1) and
    its paper-frame vector is already unwindowed. v1_5: m_ab(t) from the DHT entries (load_dj, dj_piece)."""
    sx_, sy_ = IN['SIG'][N]
    one = arb(0, 1)
    C = IN['LG'][N]
    vals, Gm, Vs = RC['vals'], RC['G'], RC['vecs']
    tS = [entry_piece(IN['RE'][N]['Iht,%d' % b], tb) for b in REVEN]
    sg0, l0 = Gm[0][0].sqrt(), vals[0]
    that = [mh * sum((Vs[k][i] * tS[i] for i in range(3)), arb(0)) / (sg0 * l0 * l0) for k in range(3)]
    Aa = m4_law(IN['M4REC'], IN['M4MOD'], 'am', N, JL)
    At = m4_law(IN['M4REC'], IN['M4MOD'], 't', N, JL)
    IPt = lemma_a_amp(dict(RC, t=that, Iht0=tS[0]), LA, er, s_, mh, C['NAP'][0], C['HBP'], C['GBP'], C['ABP'], Aa)
    Qt = qv4(At, IPt)
    tx, ty, t0t = IPt['tx'], IPt['ty'], IPt['t0t']
    bx, by, b0 = abs(tx).upper(), abs(ty).upper(), abs(t0t).upper()

    def lemA(Qv, own_x, own_y, z0):
        res = []
        for a, own, others in ((1, own_x, {0: z0, 2: own_y}), (2, own_y, {0: z0, 1: own_x})):
            q, eps = L3[a][0], L3[a][1]
            d = q * Qv + sum((eps[k] * others[k] for k in eps), arb(0)) + (q * q + sum((eps[k] * eps[k] for k in eps), arb(0))) * own
            res.append(d.upper())
        return res
    dtx, dty = lemA(Qt, bx, by, b0)
    vxtw = (tx if sx_ == 1 else -tx) + dtx * one   # <u_x, S v_t>: R4's paper frame
    vytw = (ty if sy_ == 1 else -ty) + dty * one
    vxt, vyt = vxtw / s_lo[1].union(s_hi[1]), vytw / s_lo[2].union(s_hi[2])   # v1_3: MR_INSERT's unwindowed <u_a, v_t>
    PtL = (Qt + b0 * Lk[0] + bx * Lk[1] + by * Lk[2]).upper()   # v1_3: Lemma P on S v_t
    ce = IN['MEANS'][N][key[4:]] if key[4:] in IN['MEANS'][N] else None
    Ct, ORt = IN['CCT'][N], IN['ORT'][N]
    if ce is None:
        raise Refused('C-MEANS-ROW: no c_t for %s' % key)
    uh0 = [V[0][i] * Gm[i][i].sqrt() for i in range(3)]   # v2_3: the vacuum's unit-basis coefficients (h_piece's uhat[0])
    Pt = pev_route(N, tb, IN, uh0, Ct, delta[0], ce[0].union(ce[1]), vxt, vyt, ('Mt,0,0', 'Mtt,0,0'), 'LT')   # v2_3: option (B) with Lemma RHO (v1_3: C_t)
    Ptw = PtL if PtL < (tau_hi * Pt).upper() else (tau_hi * Pt).upper()
    vpa = (abs(vxt).upper() * abs(vxt).upper() + abs(vyt).upper() * abs(vyt).upper() + Pt * Pt).sqrt().upper()
    pebt = []
    for a in (1, 2):
        f1 = (tau_hi * Ct * s_hi[a].sqrt()).upper()
        f2 = (s_hi[a] * (tau_hi * ORt * kap[a] + Ct * delta[a])).upper()
        pebt.append(f1 if f1 < f2 else f2)
    # v1_5: m_ab(t) from pk22's DHT,a,b = <psi_a, M_t psi_b> (c3j DJ records), h's trial route with C_t and OR_t; c_t is the means export's,
    # and C-CT-MEANS checks it against <u, M_t u> = <u~_0, M_t u~_0> +- delta_0 (C_t + OR_t kappa_0) from the same entries
    DT = [[dj_piece(IN['RD'], IN['DJ'][N], 'DHT,%d,%d' % (min(b, c), max(b, c)), tb) for c in REVEN] for b in REVEN]
    qt = lambda a, b: sum((V[a][i] * V[b][j] * DT[i][j] for i in range(3) for j in range(3)), arb(0))
    ctr = qt(0, 0) + (delta[0] * (Ct + ORt * kap[0])).upper() * one
    if ce is None:
        raise Refused('C-MEANS-ROW: no c_t for %s' % key)
    cem = ce[0].union(ce[1])
    if not ctr.overlaps(cem):
        raise Refused('C-CT-MEANS: <u, M_t u> from the DHT entries misses the means export c_t on %s' % key)
    mtab = {}
    for a, b in ((1, 1), (1, 2), (2, 2)):
        e1 = delta[a] * Ct / s_lo[b].sqrt() + ORt * kap[a] * delta[b]
        e2 = delta[b] * Ct / s_lo[a].sqrt() + ORt * kap[b] * delta[a]
        e = e1.upper() if e1.upper() < e2.upper() else e2.upper()
        mtab[(a, b)] = qt(a, b) - (cem if a == b else 0) + e * one
    T_ = dict(vx=vxt, vy=vyt, vxw=vxtw, vyw=vytw, Pev=Pt, Pevw=Ptw, PevwL=PtL, vp=(Ct if Ct < vpa else vpa), Q=Qt,
              pebw=pebt, win=(Ct * tau_hi * tau_hi.sqrt()).upper(), C=Ct, thx=that[1], m=mtab, ctr=ctr)   # v1_4: beta_perp <= C_t tau4^3/2
    # a: lemma_a_amp's a~_x, and a~_y's Delta by its formulas (replicated; C-A-DELTA compares the x radius)
    lt0 = (1 - er) * mh
    sig0 = er * mh / (mh - vals[1].upper())
    s0 = sig0.upper()
    ip = [sum((Gm[0][b] * Vs[k][b] for b in range(3)), arb(0)) / Gm[0][0].sqrt() for k in range(3)]
    sgk = [None, s0 if s0 < abs(ip[1]).upper() else abs(ip[1]).upper(), s0 if s0 < abs(ip[2]).upper() else abs(ip[2]).upper()]
    NAp, AbP, Lam_a = C['NAP'][0], C['ABP'], arb(LAM_A)
    GA = Lam_a * (mh / lt0) * er + AbP
    a00 = IPt['a00']
    dlax = NAp * sp + (sp + sgk[1]) * a00 + GA
    dlay = NAp * sp + (sp + sgk[2]) * a00 + GA
    if not (abs(IPt['ax'].rad() - RC['a'][1].rad() - dlax.upper()) < arb('1e-30') + RC['a'][1].rad() * arb('1e-6') + dlax.upper() * arb('1e-12')):
        raise Refused('C-A-DELTA: the replicated Delta_x of a differs from lemma_a_amp\'s')
    ax = IPt['ax']
    ay = RC['a'][2] + dlay.upper() * one
    d0 = sig0 * (1 + sig0) + sp
    z0 = (d0 * NAp).upper()
    Qva = ((mh / lt0) * Aa + Lam_a * (mh / lt0) * er + (NAp + a00) * sp + AbP).upper()
    cx_, cy_ = abs(ax).upper(), abs(ay).upper()
    dax, day = lemA(Qva, cx_, cy_, z0)
    vxa = (ax if sx_ == 1 else -ax) + dax * one
    vya = (ay if sy_ == 1 else -ay) + day * one
    Pa = (Qva + z0 * Lk[0] + cx_ * Lk[1] + cy_ * Lk[2]).upper()
    sv = IN['SV'][N][key[4:]]
    Bp = q2arb(sv['Bp_hi'][0])
    vp2 = q2arb(sv['vp2_hi'][0])
    ca_lo, ca_hi = (ce[2], ce[3]) if ce is not None else (None, None)
    if ce is None or not (ca_lo > 0):
        raise Refused('C-MEANS-ROW: no positive c_a for %s' % key)
    Lam = (Bp + ca_hi).upper()
    TX = [[entry_law_piece(IN['RD'].entry_law(IN['LW'][N]['N'][1], 'N', 'TX,%d,%d' % (min(b, c), max(b, c))), tb, th, JL) for c in REVEN] for b in REVEN]
    lam0 = l0.lower().union((l0 / LA['m0lo']).upper())
    mut = lambda a, b: sum((V[a][i] * V[b][j] * TX[i][j] for i in range(3) for j in range(3)), arb(0)) / lam0
    mud = {a: mut(a, a) for a in (1, 2)}
    muhi = {}
    for a in (1, 2):
        mh_ = mud[a].upper() if mud[a].upper() > 0 else arb(0)
        r = (delta[a] * Lam.sqrt() + (delta[a] * delta[a] * Lam + 4 * (mh_ + delta[a] * (Lam * mh_).sqrt())).sqrt()) / 2
        muhi[a] = (r * r).upper()
    mab = {}
    for a, b in ((1, 1), (1, 2), (2, 2)):
        if a == b:
            mh_ = mud[a].upper() if mud[a].upper() > 0 else arb(0)
            err = (Lam.sqrt() * delta[a] * (muhi[a].sqrt() + mh_.sqrt())).upper()
            mu_lo = (mud[a] - err).lower()
            mu_up = muhi[a] if muhi[a] < (mud[a] + err).upper() else (mud[a] + err).upper()
            mab[(a, b)] = arb(mu_lo).union(mu_up) - arb(ca_lo).union(ca_hi) * arb(s_lo[a]).union(s_hi[a])
        else:
            m1 = mud[a].upper() if mud[a].upper() > 0 else arb(0)
            m2 = mud[b].upper() if mud[b].upper() > 0 else arb(0)
            e1 = Lam.sqrt() * (delta[a] * muhi[b].sqrt() + delta[b] * m1.sqrt())
            e2 = Lam.sqrt() * (delta[b] * muhi[a].sqrt() + delta[a] * m2.sqrt())
            e = e1.upper() if e1.upper() < e2.upper() else e2.upper()
            mab[(a, b)] = mut(a, b) + e * one
    peba = []
    mlo = lambda z: arb(0) if (z.lower() <= 0 <= z.upper()) else (abs(z.lower()) if z.lower() > 0 else abs(z.upper()))
    for a, va in ((1, vxa), (2, vya)):
        mu = muhi[a]
        first = (Lam * Lam / 4) if mu > Lam / 2 else (Lam * mu - mu * mu)
        rad = first - mlo(va) * mlo(va) - mlo(mab[(1, 2)]) * mlo(mab[(1, 2)])
        ru = rad.upper()
        peba.append(ru.sqrt().upper() if ru > 0 else arb(0))
    A_ = dict(vx=vxa, vy=vya, Pev=Pa, Pevw=(tau_hi * Pa).upper(), vp=vp2.upper().sqrt().upper(), Q=Qva, m=mab, pebw=peba, win=Bp.upper(),
              C=arb(0), Lam=Lam, muhi=muhi)
    return T_, A_


def s_eps_lin(S, b, eps):
    """(G3) for a stored state: S_eps,b = sup over xi >= 0 of |p_b| W^eps <= sum_m |S[m][b]| prod_j (d_j/(eps w_j e))^d_j, with p_b = S[0][b] +
    sum_m S[m+1][b] BASIS[m] (column b of the pinned trial set's S matrix: row 0 the constant, rows 1..9 the BASIS monomials in xi_TM, xi_MB,
    xi_TB) and w = (A, A, B); each monomial's sup against e^(-eps w . xi) factorizes. J-free (the trial polynomials of the stored states carry
    no t)."""
    if not (eps > 0 and eps < 1):
        raise Refused('Lemma G eps outside (0, 1)')
    A, B = trial_ab()
    w, e = (A, A, B), arb(1).exp()
    tot = abs(arb(S[0][b]))
    for m, mono in enumerate(BASIS):
        c = S[m + 1][b]
        if c == 0:
            continue
        f = arb(1)
        for j in range(3):
            d = mono.count(j)
            for _ in range(d):
                f = f * d / (eps * w[j] * e)
        tot = tot + abs(arb(c)) * f
    return tot


def load_enga_m(N, pins=None):
    """engine A's coefficients m_bg(t) = m0 + m1 t + m2 t^2 + m3 t^3 (lambda_h units; b in e1, e3 rows, g in psi, e1, e3 columns) from its
    EXPLICIT lines (kt_c_v2_3's pinned output ENGA[N]), as exact decimals: the free choices that define f_b = V K phi_b - sum_g lambda_h m_bg
    phi_g. Returns {b: {g: [Fraction m0..m3]}} with b, g in (1, 3) and (0, 1, 3)."""
    pins = PINS if pins is None else pins
    p = ENGA[N]
    if pins.get(p) is None or sha_file(p) != pins[p]:
        raise Refused('C-ENGA: engine A output %s does not match its pin' % os.path.basename(p))
    res = {}
    rx = re.compile(r'^EXPLICIT N=%d (e1|e3) +: m0 (\S+) (\S+) (\S+) \| m1 (\S+) (\S+) (\S+) \| m2 (\S+) (\S+) (\S+) \| m3 (\S+) (\S+) (\S+);' % N)
    for ln in lines_of(p):
        mm = rx.match(ln)
        if mm:
            b = 1 if mm.group(1) == 'e1' else 3
            v = [Fraction(x) for x in mm.groups()[1:]]
            res[b] = dict((g, [v[3 * k + i] for k in range(4)]) for i, g in enumerate((0, 1, 3)))
    if sorted(res) != [1, 3]:
        raise Refused('C-ENGA: N=%d: the e1 and e3 EXPLICIT lines are not found once each' % N)
    return res


def load_m4_mg(N, pins=None):
    """v1_1: M4_KV_v1's coefficients m_bg(t) = m0 + m1 t + m2 t^2 + m3 t^3 for b = e1, e3 (the lines N<N>_E1_MG and N<N>_E3_MG, items g:k:value
    with g in psi, e1, e3 and k = 0..3), as exact decimals: the free choices that R_e1 and R_e3 belong to (kt_cert's), so f_b of the S9(c)
    assembly is the f_b of M4's residual laws. Returns {b: {g: [m0..m3]}} with b in (1, 3), g in (0, 1, 3)."""
    pins = PINS if pins is None else pins
    p = M4[0]
    if pins.get(p) is None or sha_file(p) != pins[p]:
        raise Refused('C-MBG: M4_KV_v1 does not match its pin')
    res = {}
    for b, nm in ((1, 'E1'), (3, 'E3')):
        ln = [x for x in lines_of(p) if x.startswith('N%d_%s_MG = ' % (N, nm))]
        if len(ln) != 1:
            raise Refused('C-MBG: N%d_%s_MG found %d times' % (N, nm, len(ln)))
        d = {}
        for it in ln[0].split(' = ', 1)[1].split(';'):
            g, k, v = [x.strip() for x in it.split(':')]
            d.setdefault({'psi': 0, 'e1': 1, 'e3': 3}[g], {})[int(k)] = Fraction(v)
        if sorted(d) != [0, 1, 3] or any(sorted(d[g]) != [0, 1, 2, 3] for g in d):
            raise Refused('C-MBG: N%d_%s_MG does not hold g in psi, e1, e3 with k = 0..3' % (N, nm))
        res[b] = dict((g, [d[g][k] for k in range(4)]) for g in d)
    return res


def piece_t(jlo, jhi):
    """a grid piece's t ends (exact arb points, t_ends's readings) and its J lower end for the laws (grid_j's smaller reading)."""
    tl, th = t_ends(jlo, jhi)
    return tl, th, grid_j(jlo, True)


def poly_ball(mc, tb):
    """sum_k m_k t^k on the t-ball tb (exact decimal coefficients)."""
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    s = arb(0)
    for c in reversed(mc):
        s = s * tb + q(c)
    return s


def s9c_main_piece(N, tl, th, JL, IN, plant=None, keep=None, tpt=None):
    """v1_1, S9C stage 2a: the (C9) main term on the t range [tl, th] (pk01/S9C_PLAN_v2 sect. 1-2; pk02/kt_s9c_v1 option_a), every entry
    by its law certificate at J_lo: H_b0 = mhat Ih_b + sum_g m_bg (IhT_g - mhat Gx_g0) (b = 1, 3), H_00 = 2 mhat Ih_0 - mhat^2 Gx_00,
    n_h = 1/(G_00^1/2 mu_0^2), M_U = n_h sum_(b = 1, 3) c_xb (H_b0 - G_b0 H_00/G_00), hhat = H_00/(G_00 mu_0^2), alpha_k = (G c_k)_0/G_00^1/2,
    M_R^c = (M_U + alpha_x hhat)/alpha_0, with u~_x in the orientation; also S9(b)-h's eigen-trick h^_x (ritz_piece's t amplitude with Ih
    in the Iht slot) in the same orientation, and IhT_0 against Ih_0 (C-IHT0). v1_2: plant='IHT0' shifts IhT_0 by twice the two radii plus
    1e-6 (beyond any overlap); keep (diagnostics only, never in a record) is None or a predicate keep(group, key): an input ball whose
    predicate is False is replaced by its midpoint, groups 'B' (the 18 Ritz entries, key RITZ_KEYS), 'MH' (mhat, key None), 'Ih' and 'IhT'
    (key g), 'Gx' (key (g, h)) and 'M' (m_bg, key (b, g)). v1_3: C-IHT0 reads the full balls, before keep. v1_5: tpt (a t point in
    [tl, th]) evaluates every law polynomial, mhat and m_bg at tpt alone while each law box keeps its size on the range (ak_rad at th, law_err
    at J_lo): the centre term of the centred form (s9c_main_cf)."""
    kp = lambda grp, key, x: x if (keep is None or keep(grp, key)) else arb(x.mid())
    if tpt is not None and not (tpt >= tl and tpt <= th):
        raise Refused('s9c_main_piece: tpt is not inside [tl, th]')
    tb = tl.union(th) if tpt is None else tpt
    B = ritz_entries(IN['RD'], IN['LW'][N], tb, th, JL)
    B = dict((k, kp('B', k, v)) for k, v in B.items())
    mh = kp('MH', None, mhat_ball(IN['MC'][N], tb))
    RC = ritz_piece(B, mh)
    sx_, sy_ = IN['SIG'][N]
    G, vals = RC['G'], RC['vals']
    V = [RC['vecs'][0], [x if sx_ == 1 else -x for x in RC['vecs'][1]], [x if sy_ == 1 else -x for x in RC['vecs'][2]]]
    check_orient(V, G, IN['TS'][N])
    LW, RD = IN['LW'][N], IN['RD']
    ent = lambda F, key: entry_law_piece(RD.entry_law(LW[F][1], F, key), tb, th, JL)
    Ih = dict((b, ent('NIH', 'Ih,%d' % b)) for b in REVEN)
    IhT = dict((g, ent('NHT', 'IhTh,%d' % g)) for g in REVEN)
    if plant == 'IHT0':
        IhT[0] = IhT[0] + 2 * (IhT[0].rad() + Ih[0].rad()) + arb('1e-6')
    if not IhT[0].overlaps(Ih[0]):
        raise Refused('C-IHT0: IhT_0 and Ih_0 do not meet (the reflection IhT_0 = Ih_0)')
    Ih = dict((b, kp('Ih', b, x)) for b, x in Ih.items())
    IhT = dict((g, kp('IhT', g, x)) for g, x in IhT.items())
    Gx = dict(((g, h), kp('Gx', (g, h), ent('DH', 'Gxh,%d,%d' % (min(g, h), max(g, h))))) for g in REVEN for h in REVEN)
    M = IN['MG'][N]
    m = dict(((b, g), kp('M', (b, g), poly_ball(M[b][g], tb))) for b in (1, 3) for g in (0, 1, 3))
    iht = {0: Ih[0], 1: IhT[1], 3: IhT[3]}
    H = dict((b, mh * Ih[b] + sum((m[(b, g)] * (iht[g] - mh * Gx[(g, 0)]) for g in (0, 1, 3)), arb(0))) for b in (1, 3))
    H00 = 2 * mh * Ih[0] - mh * mh * Gx[(0, 0)]
    pos = {0: 0, 1: 1, 3: 2}
    g00, mu0 = G[0][0], vals[0]
    nh = 1 / (g00.sqrt() * mu0 * mu0)
    MU = nh * sum((V[1][pos[b]] * (H[b] - G[pos[b]][0] * H00 / g00) for b in (1, 3)), arb(0))
    hhat = H00 / (g00 * mu0 * mu0)
    alpha = [sum((G[0][j] * V[k][j] for j in range(3)), arb(0)) / g00.sqrt() for k in range(3)]
    if not (alpha[0] > 0):
        raise Refused('C-ALPHA0: alpha_0 is not certainly positive')
    MR = (MU + alpha[1] * hhat) / alpha[0]
    hS = RC['t'][1] if sx_ == 1 else -RC['t'][1]
    return dict(MR=MR, hS=hS, MU=MU, hhat=hhat, alpha=alpha, H=H, H00=H00, Ih=Ih, IhT=IhT, Gx=Gx, m=m, nh=nh, RC=RC, V=V, G=G, mh=mh,
                tb=tb, B=B)


def entry_of(N, IN, grp, key):
    """v1_2 diagnostics: the law entry behind one input of s9c_main_piece, as (name, E); (None, None) for mhat and m_bg, whose balls are the
    t range only (exact coefficients)."""
    LW, RD = IN['LW'][N], IN['RD']
    if grp == 'B':
        fam, kk = key.split(',', 1)
        F, kk = {'G': ('D', 'g,' + kk), 'T': ('N', 'T,' + kk), 'Iht': ('NIH', 'Ih,' + kk)}.get(fam, ('D', 'DY,' + kk))
    elif grp == 'Ih':
        F, kk = 'NIH', 'Ih,%d' % key
    elif grp == 'IhT':
        F, kk = 'NHT', 'IhTh,%d' % key
    elif grp == 'Gx':
        F, kk = 'DH', 'Gxh,%d,%d' % (min(key), max(key))
    else:
        return None, None
    return '%s:%s' % (F, kk), RD.entry_law(LW[F][1], F, kk)


def law_parts(E, tb, t_hi, J_lo):
    """v1_2 diagnostics: an entry over the piece split as entry_law_piece adds it up: the law polynomial on the t-ball (midpoint, radius = the
    t range), the ak_rad term at t_hi, and law_err's four parts at J_lo (rem, tail, ann, far). Floats."""
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    s = arb(0)
    for a in reversed(E['ak']):
        s = s * tb + q(a)
    akr, tp = arb(0), arb(1)
    for ar in E['ak_rad']:
        akr = akr + q(ar) * tp
        tp = tp * t_hi
    res = dict(mid=float(s.mid()), trad=float(s.rad()), akr=float(akr.upper()), rem=0.0, tail=0.0, ann=0.0, far=0.0)
    if E.get('laws') is None:
        return res
    L, parts = E['laws'], E['parts']
    j0 = arb(300)
    J = q2arb(J_lo) if isinstance(J_lo, Fraction) else (J_lo if isinstance(J_lo, arb) else arb(J_lo))
    res['rem'] = float((q(parts['rem']) * (j0 / J) ** 4).upper())
    for part in ('tail', 'ann'):
        g = L[part]
        P = lambda JJ: sum((chi2_tail(g['n'], JJ * q(a) / q(G)) for a, G in g['a_G']), arb(0))
        res[part] = float((q(parts[part]) * (P(J).upper() / P(j0).lower()).sqrt()).upper())
    res['far'] = float((q(parts['far']) * (-q(L['far_rate']) * (J - j0)).exp()).upper())
    return res


def mr_solo(N, tl, th, JL, IN):
    """v1_2 diagnostics: on one piece, the radius of M_R^c with every input ball (full), with none (every input at its midpoint), with one
    group only and with one input only (first-order shares of the width; the shares add up to about the full radius). Returns (full, none,
    {group: radius}, [(radius, group, key)] largest first)."""
    run = lambda kf: float(s9c_main_piece(N, tl, th, JL, IN, keep=kf)['MR'].rad())
    full, none = run(None), run(lambda g, k: False)
    gr = dict((g0, run(lambda g, k, g0=g0: g == g0)) for g0 in ('B', 'MH', 'Ih', 'IhT', 'Gx', 'M'))
    keys = ([('B', k) for k in RITZ_KEYS] + [('MH', None)] + [('Ih', b) for b in REVEN] + [('IhT', g) for g in (1, 3)] +
            [('Gx', (g, 0)) for g in REVEN] + [('M', (b, g)) for b in (1, 3) for g in (0, 1, 3)])
    er = sorted(((run(lambda g, k, g0=g0, k0=k0: g == g0 and k == k0), g0, k0) for g0, k0 in keys), key=lambda x: -x[0])
    return full, none, gr, er


def s9c_main_sub(N, tl, th, JL, IN, K):
    """v1_3: s9c_main_piece on K equal t sub-ranges of [tl, th] (K a power of 2), each with its own t-ball and ak_rad top, law_err at the
    piece's J_lo (law_err falls with J); returns the union of the K M_R^c balls. The sub-ranges cut the dependency blow-up of evaluating
    each entry's law separately on one t-ball. v1_4: the cut points x_i = tl + (th - tl) i / K are balls (the sum rounds at ctx.prec), so
    sub-range i runs from the lower end of x_i to the upper end of x_(i+1), x_0 = tl and x_K = th exact: the sub-ranges overlap by the
    rounding and their union covers [tl, th]."""
    if K < 1 or K & (K - 1):
        raise Refused('s9c_main_sub: K = %r is not a power of 2' % K)
    if tl.rad() != 0 or th.rad() != 0:
        raise Refused('s9c_main_sub: the piece ends are not exact points')
    xs = [tl] + [tl + (th - tl) * i / K for i in range(1, K)] + [th]
    res = None
    for i in range(K):
        a, b = xs[i].lower(), xs[i + 1].upper()
        if not (a <= b):
            raise Refused('s9c_main_sub: sub-range %d is empty' % i)
        x = s9c_main_piece(N, a, b, JL, IN)['MR']
        res = x if res is None else res.union(x)
    return res


class Du(object):
    """v1_5: a first-order dual number (value ball v, t-derivative ball d) for the derivative of the (C9) main term along a path in t."""
    __slots__ = ('v', 'd')

    def __init__(self, v, d):
        self.v, self.d = v, d

    def __add__(self, o):
        o = du(o)
        return Du(self.v + o.v, self.d + o.d)

    __radd__ = __add__

    def __sub__(self, o):
        o = du(o)
        return Du(self.v - o.v, self.d - o.d)

    def __rsub__(self, o):
        return du(o) - self

    def __mul__(self, o):
        o = du(o)
        return Du(self.v * o.v, self.d * o.v + self.v * o.d)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = du(o)
        if not (o.v > 0 or o.v < 0):
            raise Refused('Du: a divisor may vanish')
        q = self.v / o.v
        return Du(q, (self.d - q * o.d) / o.v)

    def __rtruediv__(self, o):
        return du(o) / self

    def __neg__(self):
        return Du(-self.v, -self.d)

    def sqrt(self):
        if not (self.v > 0):
            raise Refused('Du: a square root of a value not certainly positive')
        s = self.v.sqrt()
        return Du(s, self.d / (2 * s))


def du(x):
    """v1_5: an int or arb constant as a Du with derivative 0."""
    if isinstance(x, Du):
        return x
    return Du(x if isinstance(x, arb) else arb(x), arb(0))


def du_sum(xs):
    s = Du(arb(0), arb(0))
    for x in xs:
        s = s + x
    return s


def law_der(E, tb):
    """v1_5: d/dt of an entry law's polynomial sum_k ak[k] t^k on the t-ball tb (Horner on k ak[k]). The law box is held fixed along the
    centred form's path, so it carries no derivative."""
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    ak = E['ak']
    s = arb(0)
    for k in range(len(ak) - 1, 0, -1):
        s = s * tb + k * q(ak[k])
    return s


def poly_der(mc, tb):
    """v1_5: d/dt of sum_k m_k t^k (exact decimal coefficients) on the t-ball tb."""
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    s = arb(0)
    for k in range(len(mc) - 1, 0, -1):
        s = s * tb + k * q(mc[k])
    return s


def mhat_der(m, tb):
    """v1_5: d/dt of mhat_ball's 1 + m1 t + m2 t^2 + m3 t^3 (exact binary64 m) on the t-ball tb."""
    a = [arb(x) for x in m]
    return a[0] + 2 * a[1] * tb + 3 * a[2] * tb * tb


def eig_der(Gd, Td, lam, cv):
    """v1_5: the t-derivatives of the generalized eigenpairs T c_k = lambda_k G c_k, c_j^T G c_k = delta_jk (ritz_piece's c_k = X^T v_k are
    G-orthonormal), from enclosures of lambda_k, c_k and of G', T': lambda_k' = c_k^T (T' - lambda_k G') c_k and c_k' = sum_(j != k)
    [c_j^T (T' - lambda_k G') c_k / (lambda_k - lambda_j)] c_j - (1/2) (c_k^T G' c_k) c_k (the gaps are ritz_piece's disjoint enclosures)."""
    n = 3
    qf = lambda a, M, b: sum((a[i] * M[i][j] * b[j] for i in range(n) for j in range(n)), arb(0))
    lamd, cvd = [], []
    for k in range(n):
        E = [[Td[i][j] - lam[k] * Gd[i][j] for j in range(n)] for i in range(n)]
        lamd.append(qf(cv[k], E, cv[k]))
        h = qf(cv[k], Gd, cv[k]) / 2
        d = [-h * cv[k][i] for i in range(n)]
        for j in range(n):
            if j == k:
                continue
            gap = lam[k] - lam[j]
            if not (gap > 0 or gap < 0):
                raise Refused('eig_der: eigenvalue enclosures %d and %d meet' % (k, j))
            a = qf(cv[j], E, cv[k]) / gap
            d = [d[i] + a * cv[j][i] for i in range(n)]
        cvd.append(d)
    return lamd, cvd


def mr_der(N, tb, Df, IN, plant=None):
    """v1_5: an enclosure of d/dtau M_R^c(p(tau) + delta) over tau in the t-ball tb and every law error delta in its box: the (C9) formula of
    s9c_main_piece in Du arithmetic, values = the full balls Df of s9c_main_piece on the same range (its eigenpair enclosures hold at every
    point of the box), derivatives = law_der of each entry (S8 D g, S8 N T, NIH Ih, NHT IhTh, DH Gxh), mhat_der, poly_der of m_bg, and
    eig_der for lambda_0 and the oriented c_k. Returns the Du of M_R^c. plant='DER' negates every input derivative (PLANT-DER)."""
    LW, RD = IN['LW'][N], IN['RD']
    sgn = -1 if plant == 'DER' else 1
    dl = lambda F, key: sgn * law_der(RD.entry_law(LW[F][1], F, key), tb)
    Gd = [[dl('D', 'g,%d,%d' % (min(b, c), max(b, c))) for c in REVEN] for b in REVEN]
    Td = [[dl('N', 'T,%d,%d' % (min(b, c), max(b, c))) for c in REVEN] for b in REVEN]
    lam, cv = Df['RC']['vals'], Df['RC']['vecs']
    lamd, cvd = eig_der(Gd, Td, lam, cv)
    sx_, sy_ = IN['SIG'][N]
    sg = (1, sx_, sy_)
    G = [[Du(Df['G'][i][j], Gd[i][j]) for j in range(3)] for i in range(3)]
    V = [[Du(Df['V'][k][j], sg[k] * cvd[k][j]) for j in range(3)] for k in range(3)]
    Ih = dict((b, Du(Df['Ih'][b], dl('NIH', 'Ih,%d' % b))) for b in REVEN)
    IhT = dict((g, Du(Df['IhT'][g], dl('NHT', 'IhTh,%d' % g))) for g in (1, 3))
    Gx = dict((g, Du(Df['Gx'][(g, 0)], dl('DH', 'Gxh,%d,%d' % (min(g, 0), max(g, 0))))) for g in REVEN)
    mh = Du(Df['mh'], sgn * mhat_der(IN['MC'][N], tb))
    M = IN['MG'][N]
    m = dict(((b, g), Du(Df['m'][(b, g)], sgn * poly_der(M[b][g], tb))) for b in (1, 3) for g in (0, 1, 3))
    iht = {0: Ih[0], 1: IhT[1], 3: IhT[3]}
    H = dict((b, mh * Ih[b] + du_sum(m[(b, g)] * (iht[g] - mh * Gx[g]) for g in (0, 1, 3))) for b in (1, 3))
    H00 = 2 * mh * Ih[0] - mh * mh * Gx[0]
    pos = {0: 0, 1: 1, 3: 2}
    g00, mu0 = G[0][0], Du(lam[0], lamd[0])
    nh = 1 / (g00.sqrt() * mu0 * mu0)
    MU = nh * du_sum(V[1][pos[b]] * (H[b] - G[pos[b]][0] * H00 / g00) for b in (1, 3))
    hhat = H00 / (g00 * mu0 * mu0)
    alpha = [du_sum(G[0][j] * V[k][j] for j in range(3)) / g00.sqrt() for k in range(2)]
    return (MU + alpha[1] * hhat) / alpha[0]


def s9c_main_cf(N, tl, th, JL, IN, K=1, plant=None):
    """v1_5: the centred form of M_R^c on [tl, th]. An entry is e(t) = p(t) + delta(t), p the law polynomial, delta(t) in the law box of the
    range (ak_rad at the range top, law_err at J_lo). For t in a sub-range [a, b] with centre c, the path tau -> M_R^c(p(tau) + delta(t))
    from c to t is differentiable (the eigenpair enclosures and gaps of the range hold at every point of the box) and the mean value theorem
    gives M_R^c(t) in M_R^c(p(c) + box) + (t - c) D, D = mr_der over [a, b] and the box. K equal sub-ranges (K a power of 2, outward-rounded
    cut points as s9c_main_sub). Returns the union and the per-sub-range parts (a, b, c, centre ball, D, full-range result)."""
    if K < 1 or K & (K - 1):
        raise Refused('s9c_main_cf: K = %r is not a power of 2' % K)
    tl, th = tl.lower(), th.upper()   # v1_6: ends given as balls (way B's t_min) are widened outward to exact points
    xs = [tl] + [tl + (th - tl) * i / K for i in range(1, K)] + [th]
    res, parts = None, []
    for i in range(K):
        a, b = xs[i].lower(), xs[i + 1].upper()
        Df = s9c_main_piece(N, a, b, JL, IN)
        Dd = mr_der(N, a.union(b), Df, IN, plant)
        c = arb(((a + b) / 2).mid())
        Dc = s9c_main_piece(N, a, b, JL, IN, tpt=c)
        u1, u2 = (b - c).upper(), (c - a).upper()
        hw = u1 if u1 > u2 else u2
        x = Dc['MR'] + Dd.d * hw * arb(0, 1)
        parts.append(dict(a=a, b=b, c=c, MRc=Dc['MR'], D=Dd.d, Df=Df))
        res = x if res is None else res.union(x)
    return res, parts


def der_fd_check(N, tl, th, JL, IN, plant=None):
    """v1_5 C-DER-FD, a sanity check of mr_der's formula (not part of any bound): the central difference (m(c + h) - m(c - h)) / (2 h) of the
    M_R^c midpoints at the t points c +- h (c the centre, h = (th - tl) / 2^12) meets the derivative enclosure of [tl, th]. Returns the
    difference quotient, the enclosure and its position (fd - mid D) / rad D; refuses when they do not meet."""
    Df = s9c_main_piece(N, tl, th, JL, IN)
    D = mr_der(N, tl.union(th), Df, IN, plant).d
    c = arb(((tl + th) / 2).mid())
    h = arb(((th - tl) / 4096).mid())
    mp = arb(s9c_main_piece(N, tl, th, JL, IN, tpt=c + h)['MR'].mid())
    mm = arb(s9c_main_piece(N, tl, th, JL, IN, tpt=c - h)['MR'].mid())
    fd = (mp - mm) / (2 * h)
    pos = float((fd - D.mid()).mid()) / float(D.rad()) if float(D.rad()) > 0 else float('inf')
    if not D.overlaps(fd):
        raise Refused('C-DER-FD: the difference quotient %s is outside the derivative enclosure %s' % (fd.str(6), D.str(6, radius=True)))
    return fd, D, pos


def m_abs_up(mc, t_hi):
    """|m(t)| <= sum_k |m_k| t^k on 0 <= t <= t_hi (an arb upper value)."""
    q = lambda x: arb(x.numerator) / arb(x.denominator)
    s, tp = arb(0), arb(1)
    for c in mc:
        s = s + abs(q(c)) * tp
        tp = tp * t_hi
    return s.upper()


def badpart_constants(N, IN, Lam, plant=None):
    """the bad-part lemma's constants at level Lam for N (S9C_BADPART_LEMMA_v1 sect. 2): J-uniform for J >= 300. Returns a dict of arb upper
    values. plant='GBB' halves G_bb's lower end for b = 1 (PLANT-GBB must move Phi_1)."""
    C = IN['LG'][N]
    kap, uC, pe, S0, g00 = C['kap'], C['uC'], C['pe'], C['S'], C['g00']
    eps, th = arb(EPS_G), arb(THETA_G)
    _w0, we, _wt = lg_weights(eps, th)
    r = tau_strip(2) / (we[0] * we[1])
    fT = r * r.sqrt() if N == 4 else r
    if not (abs(S0 * S0 * fT / g00 - pe) < arb('1e-30') * pe + (S0 * S0 * fT / g00).rad() + pe.rad()):
        raise Refused('C-FT: Phi_eps does not equal S_eps^2 f_T / G_00 (Lemma T prime at R4 weights)')
    t_hi = 1 / arb(300)
    tb = arb(0).union(t_hi)
    LW, RD = IN['LW'][N], IN['RD']
    G = {}
    for b in REVEN:
        x = entry_law_piece(RD.entry_law(LW['D'][1], 'D', 'g,%d,%d' % (b, b)), tb, t_hi, 300)
        G[b] = (x.lower() * (arb('0.5') if (plant == 'GBB' and b == 1) else 1), x.upper())
        if not (G[b][0] > 0):
            raise Refused('C-GBB: G_%d%d is not certainly positive over J >= 300' % (b, b))
    Sb = {0: S0, 1: s_eps_lin(IN['TS'][N], 1, eps), 3: s_eps_lin(IN['TS'][N], 3, eps)}
    Phi = {0: pe, 1: (Sb[1] * Sb[1] * fT / G[1][0]).upper(), 3: (Sb[3] * Sb[3] * fT / G[3][0]).upper()}
    M = IN['MG'][N]   # v1_1: M4's MG coefficients (the ones R_e1, R_e3 belong to)
    mab = dict(((b, g), m_abs_up(M[b][g], t_hi)) for b in (1, 3) for g in (0, 1, 3))
    Psi = {}
    for b in (1, 3):
        s = Phi[b].sqrt()
        for g in (0, 1, 3):
            s = s + uC * mab[(b, g)] * Phi[g].sqrt() * (G[g][1] / G[b][0]).sqrt()
        Psi[b] = s.upper()
    tau0 = tail_h(N, 1, arb(Lam), arb(0)).upper()
    Gb = gbad_p(N, arb(Lam), kap, uC, pe).upper()
    out_ = dict(kap=kap, uC=uC, fT=fT.upper(), S=Sb, G=G, Phi=Phi, mab=mab, Psi=Psi, tau0=tau0, Gb=Gb)
    out_['P0'] = (tau0 * (kap + uC) * (kap + uC) * pe).upper()
    for b in (1, 3):
        out_['P%d' % b] = (Gb * Psi[b]).upper()
        out_['H%d' % b] = (tau0 * kap * kap * Psi[b]).upper()
    out_['H0'] = Gb
    for b in (1, 3):
        for c in (1, 3):
            cross = arb(0)
            for g in (0, 1, 3):
                cross = cross + tau0 * kap * uC * mab[(b, g)] * Phi[g].sqrt() * Psi[c] * (G[g][1] / G[b][0]).sqrt()
            out_['X%d%d' % (b, c)] = cross.upper()
            out_['F%d%d' % (b, c)] = (tau0 * kap * kap * Psi[b] * Psi[c]).upper()
    return out_


def bad_bc(D):
    """v1_7: the bad parts of H_bc's double (C9) expansion for b, c in {1, 3}, normalised by lambda_0^2 ||psi_b|| ||psi_c||, J-uniform for
    J >= 300: X_bc + X_cb + F_bc of S9C_BADPART_LEMMA_v1 (both cross terms and the f-f term), read from
    badpart_constants's dict D for one N."""
    return dict(((b, c), (D['X%d%d' % (b, c)] + D['X%d%d' % (c, b)] + D['F%d%d' % (b, c)]).upper()) for b in (1, 3) for c in (1, 3))


def hb_bound(ca, cb, Q9):
    """v1_7: |<u~_a, H_xi u~_b>| / lambda_0^2 for Ritz coefficient vectors with |c_ab| <= ca[b], |c_bc| <= cb[c] (b, c in 0, 1, 3), the pairs
    split as the N-1. For b, c in {1, 3}: the double (C9) expansion H_bc = sum_(g,h) m_bg m_ch Gx_gh
    (lambda_0 >= mu_0) + the cross terms m_bg <phi_g, K_xi f_c> + m_ch <f_b, K_xi phi_h> + <f_b, K_xi f_c>, split at Lam: good parts by
    positivity with ||K^1/2 |phi_g| || <= Sh_g^1/2 and ||K^1/2 |f_b| || <= R_b lambda_0 ||psi_b|| (M4's R_e1, R_e3 in the |f| form
    a9e77bd7), bad parts X_bc + X_cb + F_bc (bad_bc). For the pairs with 0: the single (C9) identities H_b0 = mhat Ih_b + sum_g m_bg (IhT_g - mhat
    Gx_g0) + P_b and H_00 = 2 mhat Ih_0 - mhat^2 Gx_00 + P_0 (H_0b = H_b0), the law-certified values |H_b0^(C9)| and |P_b| <= lambda_0^2 G_00^1/2
    G_bb^1/2 pb_b, |P_0| <= lambda_0^2 G_00 p0 (good part with R_0 = eps_r mhat / lambda_0 by Lemma 19.2, bad part (P_b), (P_0)). Returns a dict
    of uppers: main, cross, ff, bad (the b, c in {1, 3} pairs), zero (the pairs with 0, all of it) and zbad (the (P_b), (P_0) share of zero)."""
    E1, E = (1, 3), (0, 1, 3)
    mabs, gx, sSh, sG, R, l0, Lam, B = Q9['mabs'], Q9['gx'], Q9['sSh'], Q9['sG'], Q9['R'], Q9['l0lo'], Q9['Lam'], Q9['Bbc']
    main_ = sum((ca[b] * cb[c] * mabs[(b, g)] * mabs[(c, h)] * gx[(g, h)] for b in E1 for c in E1 for g in E for h in E), arb(0)) / (l0 * l0)
    ms = dict((b, sum((mabs[(b, g)] * sSh[g] for g in E), arb(0))) for b in E1)
    cross = sum((ca[b] * cb[c] * (ms[b] * R[c] * sG[c] + ms[c] * R[b] * sG[b]) for b in E1 for c in E1), arb(0)) * Lam / l0
    ff = sum((ca[b] * cb[c] * R[b] * R[c] * sG[b] * sG[c] for b in E1 for c in E1), arb(0)) * Lam
    bad = sum((ca[b] * cb[c] * B[(b, c)] * sG[b] * sG[c] for b in E1 for c in E1), arb(0))
    w = dict((b, ca[b] * cb[0] + ca[0] * cb[b]) for b in E1)
    zero = (sum((w[b] * (Q9['Hb0'][b] / (l0 * l0) + sG[0] * sG[b] * Q9['pb'][b]) for b in E1), arb(0)) +
            ca[0] * cb[0] * (Q9['Hb0'][0] / (l0 * l0) + sG[0] * sG[0] * Q9['p0']))
    zbad = sum((w[b] * sG[0] * sG[b] * Q9['pbad'][b] for b in E1), arb(0)) + ca[0] * cb[0] * sG[0] * sG[0] * Q9['pbad'][0]
    return dict(main=main_.upper(), cross=cross.upper(), ff=ff.upper(), bad=bad.upper(), zero=zero.upper(), zbad=zbad.upper())


def s9c_htx(N, tl, th, JL, IN, H, plant=None):
    """v1_6, S9C stage 2b: S9(c)-h's Ritz-level x amplitude on [tl, th] in the orientation (S9C_LINES_v1): h~_x = M_R^c +- (E_R + L6 + L7),
    M_R^c the centred form of the (C9) main term (s9c_main_cf). E_R = (1 - m0lo^2) |M_R^c| + (L2 + L3 + L3b + L4 + L5 + bad2 + bad4) / alpha_0,lo
    bounds M_R - M_R^c ((C8): alpha_0 M_R = M_U + alpha_x (h-hat - h_xx) - alpha_y h_xy with lambda_0 in place of the Ritz value, mu_0 / lambda_0
    in [m0lo, 1]; the products <f_b, K_xi g> (L2, L4; bad2, bad4 by (P_b)) and <g, K_xi g> (L3 through G_b0 / G_00, L3b through alpha_x h-hat;
    (P_0) inside) split at Lam; L5 = |alpha_x| |h_xx| + |alpha_y| |h_xy| by hb_bound). L6 = H^Q X: X = rho_0 / (1 - tau4 - sum_k rho_k^2 /
    (1 - mu_k)) and H^Q <= PeBwu_x + C delta_x + sum_k beta_k q_k + |c_h| (1 + mu_x) rho_x (S9C_ENGINE_DESIGN_v1 sect. 3; no Lam split, so no bad
    part). L7 = <u~_k, Omega_0> h_kx (k = x, y) + |h_00| <u~_x, Omega_0> + (1 - <u~_0, Omega_0>) |M_R|. H holds h_piece's quantities on the
    same piece (beta_0 takes S9(b)'s |v_x| bound). plant: 'HQ' (H^Q times 1e4), 'RB' (R_e1 times 1e3), 'BAD' (the bad parts at Lam = 10).
    v1_7: hb_bound with the pair split (the pairs with 0 by the single (C9) identities and (P_b), (P_0); X_bc + X_cb + F_bc for b, c in
    {1, 3}); H^Q's P_e term tau4 C delta_x in place of C delta_x (the bound ||P_e B^w (u~_x - u_x)|| <= ||S P_e||
    ||M_c S|| delta_x with ||S P_e|| <= tau4)."""
    CF, parts = s9c_main_cf(N, tl, th, JL, IN)
    Df = parts[0]['Df']
    BP = IN['BP10'][N] if plant == 'BAD' else IN['BP'][N]
    BBC = bad_bc(BP)
    E = (0, 1, 3)
    pos = {0: 0, 1: 1, 3: 2}
    G, V, al = Df['G'], Df['V'], Df['alpha']
    l0lo = Df['RC']['vals'][0].lower()
    a0lo = al[0].lower()
    if not (l0lo > 0 and a0lo > 0):
        raise Refused('C-S9C-POS: mu_0 or alpha_0 is not certainly positive')
    mh = abs(Df['mh']).upper()
    er = H['er'].upper()
    R = {0: (er * mh / l0lo).upper(), 1: (H['Rb12'][0].upper() * (1000 if plant == 'RB' else 1)).upper(), 3: H['Rb12'][1].upper()}
    sG = dict((g, G[pos[g]][pos[g]].upper().sqrt().upper()) for g in E)
    sSh = dict((g, H['SH'][pos[g]].upper().sqrt().upper()) for g in E)
    cv = lambda k: dict((g, abs(V[k][pos[g]]).upper()) for g in E)
    c0, cx, cy = cv(0), cv(1), cv(2)
    mabs = dict(((b, g), abs(Df['m'][(b, g)]).upper()) for b in (1, 3) for g in E)
    mabs.update({(0, 0): mh, (0, 1): arb(0), (0, 3): arb(0)})
    gx = dict(((g, h), abs(Df['Gx'][(g, h)]).upper()) for g in E for h in E)
    Lam = arb(LAM9C)
    mhl = (mh / l0lo).upper()
    pbad = {0: BP['P0'], 1: BP['P1'], 3: BP['P3']}
    pb = dict((b, (Lam * R[b] * er * mhl + pbad[b]).upper()) for b in (1, 3))   # |P_b| / (lambda_0^2 ||psi_0|| ||psi_b||): good part and (P_b)
    Hb0 = {0: abs(Df['H00']).upper(), 1: abs(Df['H'][1]).upper(), 3: abs(Df['H'][3]).upper()}   # the (C9) values on the range, law bars inside
    Q9 = dict(mabs=mabs, gx=gx, sSh=sSh, sG=sG, R=R, l0lo=l0lo, Lam=Lam, Bbc=BBC, Hb0=Hb0, pb=pb, pbad=pbad,
              p0=(Lam * er * er * mhl * mhl + BP['P0']).upper())
    hxx, hxy, h00 = hb_bound(cx, cx, Q9), hb_bound(cx, cy, Q9), hb_bound(c0, c0, Q9)
    HXX, HXY, H00 = [(x['main'] + x['cross'] + x['ff'] + x['bad'] + x['zero']).upper() for x in (hxx, hxy, h00)]
    hbad = dict((k, (x['bad'] + x['zbad']).upper()) for k, x in (('xx', hxx), ('xy', hxy), ('00', h00)))
    g10, g30 = (abs(G[1][0]) / G[0][0]).upper(), (abs(G[2][0]) / G[0][0]).upper()
    axa, aya = abs(al[1]).upper(), abs(al[2]).upper()
    L2 = (cx[1] * Lam * R[1] * er * mhl * sG[1]).upper()
    L4 = (cx[3] * Lam * R[3] * er * mhl * sG[3]).upper()
    p0 = Q9['p0']   # |<g, K_xi g>| / (lambda_0^2 ||psi_0||^2): the good part and (P_0)
    L3 = ((cx[1] * g10 + cx[3] * g30) * sG[0] * p0).upper()
    L3b = (axa * p0).upper()
    L5 = (axa * HXX + aya * HXY).upper()
    bad2 = (cx[1] * sG[1] * BP['P1']).upper()
    bad4 = (cx[3] * sG[3] * BP['P3']).upper()
    MRhi = abs(CF).upper()
    lamterm = ((1 - H['m0lo'] * H['m0lo']) * MRhi).upper()
    ER = (lamterm + (L2 + L3 + L3b + L4 + L5 + bad2 + bad4) / a0lo).upper()
    rho, mu_hi, tau_hi = H['rho'], H['mu_hi'], H['tau_hi']
    den = 1 - tau_hi - sum((rho[k] * rho[k] / (1 - mu_hi[k]) for k in (1, 2)), arb(0))
    if not (den > 0):
        raise Refused('C-X: 1 - tau4 - sum_k rho_k^2 / (1 - mu_k) is not certainly positive')
    X = (rho[0] / den).upper()
    ukO = dict((k, (X * rho[k] / (1 - mu_hi[k])).upper()) for k in (1, 2))
    rad = 1 - X * X - ukO[1] * ukO[1] - ukO[2] * ukO[2]
    if not (rad > 0):
        raise Refused('C-X: 1 - X^2 - sum_k <u~_k, Omega_0>^2 is not certainly positive')
    uO0 = (1 - rad.sqrt()).upper()
    s_hi, Cc, dx = H['s_hi'], H['Cc'], H['delta'][1]
    qk = [H['L3'][a][0].upper() for a in range(3)]
    b0 = s_hi[1] * abs(H['vx']).upper() + Cc * dx
    bx = s_hi[1] * s_hi[1] * abs(H['m'][(1, 1)]).upper() + Cc * s_hi[1].sqrt() * dx
    by = s_hi[1] * s_hi[2] * abs(H['m'][(1, 2)]).upper() + Cc * s_hi[2].sqrt() * dx
    HQ = (H['pebw'][0] + tau_hi * Cc * dx + b0 * qk[0] + bx * qk[1] + by * qk[2] + abs(H['ch']).upper() * (1 + mu_hi[1]) * rho[1]).upper()
    if plant == 'HQ':
        HQ = (HQ * 10000).upper()
    L6 = (HQ * X).upper()
    MRabs = (MRhi + ER).upper()
    # (C8)'s h_00 is the vacuum amplitude <Omega_0, H_xi Omega_0>/lambda_0^2. With Omega_0 = beta u~_0 + w,
    # ||w||^2 <= W^2 = 1 - rad, and ||H_xi||/lambda_0^2 <= N_H = Lam + tau~0 kappa^2 for every J >= 300 (positivity below Lam, the lemma's
    # Schur step above), |h_00| <= hb_bound(c_0, c_0) + (2 W + W^2) N_H
    W2 = (1 - rad).upper()
    H00 = (H00 + (2 * W2.sqrt() + W2) * (Lam + BP['tau0'] * BP['kap'] * BP['kap'])).upper()
    L7 = (ukO[1] * HXX + ukO[2] * HXY + H00 * ukO[1] + uO0 * MRabs).upper()
    tot = (ER + L6 + L7).upper()
    badw = ((bad2 + bad4 + ((cx[1] * g10 + cx[3] * g30) * sG[0] + axa) * BP['P0'] + axa * hbad['xx'] + aya * hbad['xy']) / a0lo +
            ukO[1] * hbad['xx'] + ukO[2] * hbad['xy'] + ukO[1] * hbad['00']).upper()
    return dict(htx=CF + tot * arb(0, 1), MRc=CF, ER=ER, L2=L2, L3=L3, L3b=L3b, L4=L4, L5=L5, L6=L6, L7=L7, lamterm=lamterm, bad2=bad2,
                bad4=bad4, badw=badw, X=X, HQ=HQ, HXX=HXX, HXY=HXY, H00=H00, hxx=hxx, hxy=hxy, uO0=uO0, ukO=ukO, tot=tot, D=parts[0]['D'],
                R=R, er=er, mhl=mhl)


def m1_texts(pins=None):
    """v2_1: MR_INSERT's MR_INPUT_KV_v4 texts read by ast from the pinned M1 engine (pk24's kt_mr_assembly_v1_8_4, G6 v1_6_2 sect. 6 as
    built): the v4 FIELDS (FIELDS['MR_INSERT'] plus FIELDS4's MR_INSERT suffix), X_POWER and X_DEFINITION for MR_INSERT, ORIENTATION and the
    ORIENT_CHECK pattern ORIENT_RX. The writer copies them; nothing here is typed."""
    pins = PINS if pins is None else pins
    if pins.get(M1ENG) is None or sha_file(M1ENG) != pins[M1ENG]:
        raise Refused('C-M1-TEXTS: the M1 engine does not match its pin')
    tree = ast.parse(open(M1ENG).read())
    got, suffix = {}, None
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
            continue
        nm = node.targets[0].id
        if nm in ('FIELDS', 'XPOW', 'XDEF', 'ORIENT', 'ORIENT_RX'):
            if nm in got:
                raise Refused('C-M1-TEXTS: %s is assigned twice in the M1 engine' % nm)
            got[nm] = ast.literal_eval(node.value)
        elif nm == 'FIELDS4':
            for kw in getattr(node.value, 'keywords', []):
                if kw.arg == 'MR_INSERT' and isinstance(kw.value, ast.BinOp) and isinstance(kw.value.right, ast.Constant):
                    suffix = kw.value.right.value
    if sorted(got) != ['FIELDS', 'ORIENT', 'ORIENT_RX', 'XDEF', 'XPOW'] or suffix is None:
        raise Refused('C-M1-TEXTS: the M1 engine does not define FIELDS, FIELDS4, XPOW, XDEF, ORIENT and ORIENT_RX as expected')
    return dict(fields=(got['FIELDS']['MR_INSERT'] + suffix), xpow=got['XPOW']['MR_INSERT'], xdef=got['XDEF']['MR_INSERT'],
                orient=got['ORIENT'], orient_rx=got['ORIENT_RX'])


def trial_set_line(pins=None):
    """v2_1: the TRIAL_SET header value copied by tool from pk25's certified MR_SPECTRAL (mr/v3, pinned; the row 4321)."""
    pins = PINS if pins is None else pins
    if pins.get(SPEC_V3) is None or sha_file(SPEC_V3) != pins[SPEC_V3]:
        raise Refused('C-TRIAL-SET: mr/v3 MR_SPECTRAL.kv does not match its pin')
    v = [ln.split('=', 1)[1].strip() for ln in lines_of(SPEC_V3) if ln.startswith('TRIAL_SET = ')]
    if len(v) != 1 or not v[0]:
        raise Refused('C-TRIAL-SET: mr/v3 MR_SPECTRAL.kv has %d TRIAL_SET lines' % len(v))
    return v[0]


def s9c_main_cf_q(N, tl, th, JL, IN):
    """v2_1: the centred form of M_R^c(t) / t on [tl, th] with tl > 0, as s9c_main_cf with one range: F(p(c) + B)/c + [a - c, b - c] D_q,
    D_q an enclosure of d/dtau [F(p(tau) + delta)/tau] = (F' - F/tau)/tau, mr_der's dual number divided by the dual (tau, 1) on the t-ball
    (the mean value theorem on tau -> F(p(tau) + delta)/tau, C^1 on [a, b] since a > 0 and s9c_main_cf's conditions hold)."""
    tl, th = tl.lower(), th.upper()
    if not (tl > 0):
        raise Refused('s9c_main_cf_q: the range reaches t = 0')
    Df = s9c_main_piece(N, tl, th, JL, IN)
    tb = tl.union(th)
    Dq = mr_der(N, tb, Df, IN) / Du(tb, arb(1))
    c = arb(((tl + th) / 2).mid())
    Dc = s9c_main_piece(N, tl, th, JL, IN, tpt=c)
    u1, u2 = (th - c).upper(), (c - tl).upper()
    hw = u1 if u1 > u2 else u2
    return Dc['MR'] / c + Dq.d * hw * arb(0, 1)


def ins_fields(jlo, jhi, vx, vy, Pevw, Pev, vp, m, pebw, win, C, windowed, xc, xf):
    """v2_1: one MR_INSERT v4 row as decimal strings in FIELDS order (jlo jhi vx vy Pevw Pev vp m_xx m_xy m_yy PeBwux PeBwuy win C windowed
    xc xf): *_lo rounded down, *_hi rounded up (dec_lo, dec_hi); xc given as strings when it must equal vx exactly (power 0)."""
    if m is None:
        raise Refused('C-INS-M: a row has no m_ab')
    xs = list(xc) if isinstance(xc, tuple) else [dec_lo(xc), dec_hi(xc)]
    return [jlo, jhi, dec_lo(vx), dec_hi(vx), dec_lo(vy), dec_hi(vy), dec_hi(Pevw), dec_hi(Pev), dec_hi(vp), dec_lo(m[(1, 1)]), dec_hi(m[(1, 1)]),
            dec_lo(m[(1, 2)]), dec_hi(m[(1, 2)]), dec_lo(m[(2, 2)]), dec_hi(m[(2, 2)]), dec_hi(pebw[0]), dec_hi(pebw[1]), dec_hi(win), dec_hi(C),
            windowed] + xs + [xf]


def h_row_v4(N, jlo, jhi, tl, th, JL, D, IN, plant=None):
    """v2_1: MR_INSERT's h row on a piece with t_lo > 0, from h_piece's output D with S9(c) (D['S9']). xc encloses v_x(t)/t on the piece:
    (M_R^c(t)/t by s9c_main_cf_q + [-1, 1] (tot + dhx)/t_lo) / s_x, because h~_x(t) lies in M_R^c(t) +- tot (s9c_htx) and Lemma A adds dhx, and
    v_x = h_x/s_x with s_x in the piece's enclosure. vx is S9(c)'s unwindowed v_x joined with t xc at both ends, so t xc lies inside the
    amplitude at both ends (the M1 engine's G-FACTX); xf = 0. vp = min(C, (v_x^2 + v_y^2 + Pev^2)^1/2) with S9(c)'s vx. The other fields are
    h_piece's. plant='FACTX' doubles xc's upper end after the join (C-FACTX must stop it)."""
    S9 = D['S9']
    sxb = D['s_lo'][1].union(D['s_hi'][1])
    tlo, thi = tl.lower(), th.upper()
    xc = (s9c_main_cf_q(N, tl, th, JL, IN) + ((S9['tot'] + S9['dhx']) / tlo).upper() * arb(0, 1)) / sxb
    vx = S9['vx'].union(xc * tlo).union(xc * thi)
    if plant == 'FACTX':
        xc = xc + abs(xc).upper() * arb(1)
    Cc = IN['CC'][N]
    vpa = (abs(vx).upper() * abs(vx).upper() + abs(D['vy']).upper() * abs(D['vy']).upper() + D['Pev'] * D['Pev']).sqrt().upper()
    vp = Cc if Cc < vpa else vpa
    return ins_fields(jlo, jhi, vx, D['vy'], D['Pevw'], D['Pev'], vp, D['m'], D['pebw'], D['win'], Cc, '1', xc, '0'), dict(xc=xc, vx=vx)


def h_last_row_v4(N, jlo, jhi, th, L, Dagg, IN):
    """v2_1: MR_INSERT's h row on the last piece by way B on S9(c)'s v_x (the row 4325, G6 v1_6_2 sect. 6): xc = [g_lo, g_hi], xf = f and
    the amplitude columns min(0, t_1 g_lo) - f and t_1 g_hi + f with t_1 the piece's top t; the other fields the sub-pieces' aggregate."""
    t1 = th.upper()
    glo, ghi, f = L['glo'], L['ghi'], L['f']
    lo = ((t1 * glo).lower() if (t1 * glo).lower() < 0 else arb(0)) - f
    vx = lo.lower().union((t1 * ghi + f).upper())
    Cc = IN['CC'][N]
    vpa = (abs(vx).upper() * abs(vx).upper() + abs(Dagg['vy']).upper() * abs(Dagg['vy']).upper() + Dagg['Pev'] * Dagg['Pev']).sqrt().upper()
    vp = Cc if Cc < vpa else vpa
    return ins_fields(jlo, jhi, vx, Dagg['vy'], Dagg['Pevw'], Dagg['Pev'], vp, Dagg['m'], Dagg['pebw'], Dagg['win'], Cc, '1',
                      glo.lower().union(ghi.upper()), dec_hi(f))


def waya_arb(e):
    """v2_5: an exact sympy number (rationals, square roots, sums, products, integer powers) as an arb ball (C13's and P2's to_arb)."""
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
    raise Refused('C-WAYA-IN: waya_arb cannot convert %s' % e)


def waya_load(mode, pins=None):
    """v2_5 C-WAYA-IN: P2's MR_LEMMAP_V3F record and P1's C10 record, both pinned. The P2 record: FORMAT MR_LEMMAP_KV_v3F, RECORD
    MR_LEMMAP_F, RUN_VERDICT VALID, STATUS CERTIFIED (a dry run also takes DRY), SOURCE naming the pinned MR_LEMMAP v3 and C10 record,
    ORIENTATION as MR_LEMMAP v3, N<N>_UHAT0 equal to the C10 record's line. The C10 record: a certified valid C10_KV_v1 with uhat_0(0) =
    (1, 0, 0) and G0_00 = 1. Returns {head, rows, ix, N: {N: ux0, uy0 (exact uhat_x(0), uhat_y(0)), G0d (exact G0_bb)}} as sympy numbers."""
    import sympy as sp
    pins = PINS if pins is None else pins
    for p in (P2REC, C10REC):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('C-WAYA-IN: %s does not match its pin' % os.path.basename(p))

    def kv(path):
        head, rows, ix = {}, {}, None
        for ln in lines_of(path):
            if ln.startswith('#') or not ln.strip():
                continue
            if ' = ' not in ln:
                raise Refused('C-WAYA-IN: a line without " = " in %s' % os.path.basename(path))
            k, v = ln.split(' = ', 1)
            if k == 'FIELDS':
                ix = dict((f, i) for i, f in enumerate(v.split()))
            elif re.fullmatch(r'N[34]_P[0-9]+', k):
                rows[k] = v.split()
            elif k in head:
                raise Refused('C-WAYA-IN: the header key %s twice in %s' % (k, os.path.basename(path)))
            else:
                head[k] = v
        return head, rows, ix
    h2, rows2, ix2 = kv(P2REC)
    hc, _rc, _ic = kv(C10REC)
    if (h2.get('FORMAT'), h2.get('RECORD'), h2.get('RUN_VERDICT')) != ('MR_LEMMAP_KV_v3F', 'MR_LEMMAP_F', 'VALID') or ix2 is None:
        raise Refused('C-WAYA-IN: the P2 record is not a valid MR_LEMMAP_KV_v3F record')
    st = h2.get('STATUS')
    if not (st == 'CERTIFIED' or (mode == 'dry' and st == 'DRY')):
        raise Refused('C-WAYA-IN: the P2 record has STATUS %s in %s mode' % (st, mode))
    src = h2.get('SOURCE', '')
    if ('MR_LEMMAP v3 %s;' % pins[LEMMAP][:8]) not in src or ('C10 %s;' % pins[C10REC][:8]) not in src:
        raise Refused('C-WAYA-IN: the P2 record SOURCE does not name the pinned MR_LEMMAP v3 and C10 record')
    if not h2.get('ORIENTATION', '').startswith('u_x along e1, u_y along e3'):
        raise Refused('C-WAYA-IN: the P2 record ORIENTATION is not MR_LEMMAP v3\'s')
    if (hc.get('FORMAT'), hc.get('STATUS'), hc.get('RUN_VERDICT')) != ('C10_KV_v1', 'CERTIFIED', 'VALID'):
        raise Refused('C-WAYA-IN: the C10 record is not a certified valid C10_KV_v1')
    res = {}
    for N in (4, 3):
        raw = hc.get('N%d_UHAT0' % N)
        if raw is None or h2.get('N%d_UHAT0' % N) != raw:
            raise Refused('C-WAYA-IN: N%d_UHAT0 differs between the P2 and C10 records' % N)
        u = {}
        for part in raw.split('; '):
            nm, ex = part.split(' ', 1)
            m = re.fullmatch(r'u([0xy])([p13])', nm)
            if m is None or (m.group(1), m.group(2)) in u:
                raise Refused('C-WAYA-IN: N%d uhat name %r' % (N, nm))
            u[(m.group(1), m.group(2))] = sp.sympify(ex)
        if len(u) != 9 or [u[('0', b)] for b in 'p13'] != [1, 0, 0]:
            raise Refused('C-WAYA-IN: N%d_UHAT0 is not nine values with uhat_0(0) = (1, 0, 0)' % N)
        mg = re.fullmatch(r'G \[(.+)\]; T \[(.+)\] \(psi-hat, s1, s3 unnormalised, t\^0\)', hc.get('N%d_GT0_W' % N, ''))
        if mg is None:
            raise Refused('C-WAYA-IN: N%d_GT0_W does not parse' % N)
        G0 = [sp.sympify(e) for e in mg.group(1).split(', ')]
        if len(G0) != 9 or G0[0] != 1:
            raise Refused('C-WAYA-IN: N%d G0 is not 3 x 3 with G0_00 = 1' % N)
        res[N] = dict(ux0=[u[('x', b)] for b in 'p13'], uy0=[u[('y', b)] for b in 'p13'], G0d=[G0[0], G0[4], G0[8]])
    return dict(head=h2, rows=rows2, ix=ix2, N=res)


def waya_rt(E, J_lo, t_hi, jtest=None):
    """v2_5 (P2's r_over_t): R/t over the last piece, rem 300^4 t_hi^3 + J_lo (tail + ann + far)(J_lo), with C-MONO-TAIL (J_lo a/G > 5 for
    every chi-square pair, so J^2 P(J) decreases) and C-MONO-FAR (J_lo far_rate > 1, so J e^(-far_rate J) decreases); jtest replaces J_lo
    in the two tests only."""
    if E.get('laws') is None:
        return arb(0)
    q = lambda x: arb(Fraction(x).numerator) / arb(Fraction(x).denominator)
    L, parts = E['laws'], E['parts']
    j0, J = arb(300), q2arb(Fraction(J_lo))
    Jt = J if jtest is None else q2arb(Fraction(jtest))
    tot = q(parts['rem']) * arb(300) ** 4 * t_hi ** 3
    for part in ('tail', 'ann'):
        g = L[part]
        for a, G in g['a_G']:
            if not (Jt * q(a) / q(G) > 5):
                raise Refused('C-MONO-TAIL: J_lo a/G is not above 5 for a %s pair' % part)
        P = lambda JJ: sum((chi2_tail(g['n'], JJ * q(a) / q(G)) for a, G in g['a_G']), arb(0))
        tot = tot + J * q(parts[part]) * (P(J).upper() / P(j0).lower()).sqrt()
    fr = q(L['far_rate'])
    if not (Jt * fr > 1):
        raise Refused('C-MONO-FAR: J_lo far_rate is not above 1')
    tot = tot + J * q(parts['far']) * (-fr * (J - j0)).exp()
    return tot.upper()


def waya_x1(RD, LWN, F, key, x0, J_lo, t_hi, tb, jtest=None):
    """v2_5 (P2's entry_x1): (X(t) - X(0))/t over the last piece in the reader's coefficient-ball form: the true a_k lie in [LO_k, HI_k]
    (entry_ball) and the rest of the law is at most R(J) (entry_law's parts with no ak_rad term, the reader's N-1), so X1 lies in
    sum_(k=1..3) [LO_k, HI_k] t^(k-1) + [-R/t, R/t] with X(0) = a_0. x0 (an exact arb value, or None) must lie in [LO_0, HI_0] (C-A0).
    Returns (X1, [LO_0, HI_0])."""
    rec, cert = LWN[F]
    LO, HI, _eb = RD.entry_ball(rec, key)
    if len(LO) != 4 or len(HI) != 4:
        raise Refused('C-A0: %s:%s has %d coefficient balls, expected 4' % (F, key, len(LO)))
    ball = lambda k: q2arb(Fraction(LO[k])).union(q2arb(Fraction(HI[k])))
    if x0 is not None and not (q2arb(Fraction(LO[0])) <= x0 and x0 <= q2arb(Fraction(HI[0]))):
        raise Refused('C-A0: P1\'s exact %s:%s(0) is outside [LO_0, HI_0]' % (F, key))
    E = RD.entry_law(cert, F, key)
    s = arb(0)
    for k in (3, 2, 1):
        s = s * tb + ball(k)
    return s + arb(0, 1) * waya_rt(E, J_lo, t_hi, jtest), ball(0)


def waya_last(N, jlo, th, JL, key, IN, D, plant=None):
    """v2_5, route (B) Way A on the last h row (P4_LEMMA_NOTE_v1_1; the rows 4640, 4644): for t in [0, t_1],
    t_1 = th, s_x v_x = <u_x, B^w u> = h~ + R_1 - c_h R_2 + E_A, where h~ = <u~_x, S M_h psi-hat_n> with ONE S (the NIH entry next to psi-hat,
    [cp b 0] [xh M 1 8] [cp 0 2], is lambda_0 <chi_b, S M_h chi_0> over its main), R_1 = <u~_x, S M_h (u - psi-hat_n)>, R_2 = <u~_x, u> and E_A
    Lemma A's error at level x for w = B^w u. In the records' units h~ = sum_b c_xb Ih_b / (G_00^1/2 Lambda) with Lambda the true top eigenvalue,
    Lambda in [mu_0, mu_0/m0lo] (the piece's Ritz value; m0lo <= mu_0/Lambda by Kato-Temple, lemma_a_cbar), and c_x = uhat_x/G_bb^1/2 from
    P2's oriented table (the orientation, so no sigma_x flip). The t^0 value sum_b c_x0,b Ih_b(0) is exactly 0 (C13's C-BH0 with P1's
    C-T0-EXACT and C-HARM; C-WAYA-T0 checks that the coefficient balls [LO_0, HI_0] hold 0), so
      h~/t = [sum_b dc_b Ih_b(t) + sum_b c_x0,b Ih1_b(t)] / (G_00^1/2 Lambda),
      dc_b = (c_xb - c_x0,b)/t = du_b/g_b - u0_b G1_bb/(g_b g0_b (g_b + g0_b)),
    with du_b P2's (uhat_xb - uhat_xb(0))/t, u0_b = uhat_xb(0) exact (C10), g_b = G_bb^1/2 on the piece, g0_b = G0_bb^1/2 exact, and G1_bb,
    Ih1_b = (X(t) - X(0))/t by waya_x1. Remainders over t, from P2's last row: R_1/t <= (C + |c_h|)(delta_0/t + sum_b |uhat_0b - uhat_0b(0)|/t)
    (|S M_h| <= C + |c_h|), |c_h| R_2/t <= |c_h| delta_0/t, delta_0/t <= (2 (q0t^2 + eps_x0t^2 + eps_y0t^2))^1/2, and dh_x/t <= qxt Q +
    eps_0xt a0t + eps_yxt ay + t_1 (qxt^2 + eps_0xt^2 + eps_yxt^2) ax (Q, a0t, ay, ax h_piece's O(1) bounds on the piece). Then
    xc = (h~/t +- the remainders)/[s_x,lo, s_x,hi], C-WAYA: xc certainly positive. plant 'ZERO': u_y(0) in place of u_x(0) in C-WAYA-T0;
    'ORIENT': c_x flipped."""
    W = IN['WA']['N'][N]
    ix, row = IN['WA']['ix'], IN['WA']['rows'].get(key)
    if row is None or row[ix['jlo']] != jlo or row[ix['jhi']] != 'inf':
        raise Refused('C-WAYA-IN: the P2 record has no last row %s with jlo %s and jhi inf' % (key, jlo))
    fv = lambda f: q2arb(Fraction(row[ix[f]]))
    hv = lambda f: fv(f + '_lo').union(fv(f + '_hi'))
    t1 = th.upper()
    tb = arb(0).union(t1)
    RD, LWN = IN['RD'], IN['LW'][N]
    RC, B = D['RC'], D['B']
    G, mu0, m0lo = RC['G'], RC['vals'][0], D['m0lo']
    if not (mu0 > 0 and m0lo > 0 and G[0][0] > 0):
        raise Refused('C-WAYA: mu_0, m0lo or G_00 is not certainly positive')
    Lam = mu0.lower().union((mu0.upper() / m0lo).upper())
    F = 1 / (G[0][0].sqrt() * Lam)
    sgn = -1 if plant == 'ORIENT' else 1
    u0 = [sgn * waya_arb(x) for x in W['ux0']]
    du = [sgn * hv('ux%st' % b) for b in 'p13']
    g0 = [waya_arb(x).sqrt() for x in W['G0d']]
    g = [G[i][i].sqrt() for i in range(3)]
    c0 = [u0[i] / g0[i] for i in range(3)]
    dc, Ih1, a0 = [], [], []
    for i, b in enumerate(REVEN):
        G1, _g0b = waya_x1(RD, LWN, 'D', 'g,%d,%d' % (b, b), waya_arb(W['G0d'][i]), JL, t1, tb)
        dc.append(du[i] / g[i] - u0[i] * G1 / (g[i] * g0[i] * (g[i] + g0[i])))
        x1, ab = waya_x1(RD, LWN, 'NIH', 'Ih,%d' % b, None, JL, t1, tb)
        Ih1.append(x1)
        a0.append(ab)
    cz = [waya_arb(W['uy0'][i]) / g0[i] for i in range(3)] if plant == 'ZERO' else c0
    z0 = sum((cz[i] * a0[i] for i in range(3)), arb(0))
    if not z0.overlaps(arb(0)):
        raise Refused('C-WAYA-T0: sum_b c_x0,b [LO_0, HI_0] of the NIH entries does not hold 0 (%s): the t^0 combination is not O(t)' % z0.str(6))
    Ih = [B['Iht,%d' % b] for b in REVEN]
    ht = F * (sum((dc[i] * Ih[i] for i in range(3)), arb(0)) + sum((c0[i] * Ih1[i] for i in range(3)), arb(0)))
    sq = lambda x: x * x
    d0t = (2 * (sq(fv('q0t_hi')) + sq(fv('eps_x0t_hi')) + sq(fv('eps_y0t_hi')))).sqrt().upper()
    U0t = sum((abs(hv('u0%st' % b)).upper() for b in 'p13'), arb(0)).upper()
    Cc, ch = IN['CC'][N], abs(D['ch']).upper()
    R1t = ((Cc + ch) * (d0t + U0t)).upper()
    R2t = (ch * d0t).upper()
    qxt, e0xt, eyxt = fv('qxt_hi'), fv('eps_0xt_hi'), fv('eps_yxt_hi')
    dht = (qxt * D['Q'].upper() + e0xt * D['a0t'] + eyxt * D['ay'] + t1 * (sq(qxt) + sq(e0xt) + sq(eyxt)) * D['ax']).upper()
    rem = (R1t + R2t + dht).upper()
    sxb = D['s_lo'][1].union(D['s_hi'][1])
    xc = (ht + rem * arb(0, 1)) / sxb
    if not (xc > 0):
        raise Refused('C-WAYA: xc = v_x/t is not certainly positive on the last piece (%s)' % xc.str(6))
    return dict(xc=xc, ht=ht, rem=rem, R1t=R1t, R2t=R2t, dht=dht, z0=z0, F=F, Lam=Lam, d0t=d0t, U0t=U0t, t1=t1)


def main_n_check(N, t_path, i_path, pins=None):
    """v2_6 C-MAIN-N (the row 4672): the Ritz problem's T entries (t_path, S8 N's record) and the NIH entries
    (i_path) share one main, main_N, so that Lambda = lambda_0 main_D/main_N is the eigenvalue mu_0 and m0lo bound: the T record's graph is N,
    the NIH record's prep names the vertex graph VN, and the two records' family prep parameters (radii a_v, rho'^2 ap, theta0) are equal.
    Both files must match their pins."""
    pins = PINS if pins is None else pins
    for p in (t_path, i_path):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('C-MAIN-N: %s does not match its pin' % os.path.basename(p))
    with open(t_path) as fh:
        rt = json.load(fh)
    with open(i_path) as fh:
        ri = json.load(fh)
    if rt.get('graph') != 'N' or not isinstance(rt.get('families'), dict) or 'N' not in rt['families']:
        raise Refused('C-MAIN-N: %s is not a graph N record (graph %r)' % (os.path.basename(t_path), rt.get('graph')))
    prep = ri.get('prep') if isinstance(ri.get('prep'), dict) else {}
    if prep.get('vgraph') != 'VN' or not isinstance(ri.get('families'), dict) or 'NIH' not in ri['families']:
        raise Refused('C-MAIN-N: %s does not name the vertex graph VN' % os.path.basename(i_path))
    ft, fi = rt['families']['N'], ri['families']['NIH']
    keys = ('a_v', 'ap', 'theta0')
    if any(ft.get(k) is None or ft.get(k) != fi.get(k) for k in keys):
        raise Refused('C-MAIN-N: the T and NIH families carry different prep parameters at N = %d' % N)
    return True


def waya_row(rh, WA, fields):
    """v2_5: the last h row with way A: vx_lo, vx_hi = min(0, t_1 xc_lo), max(0, t_1 xc_hi); xc_lo, xc_hi from waya_last; xf_hi = 0; every other
    field is way B's row (vp_hi keeps way B's bound, which stays valid)."""
    ix = dict((f, i) for i, f in enumerate(fields))
    xc, t1 = WA['xc'], WA['t1']
    lo = (t1 * xc).lower()
    lo = lo if lo < 0 else arb(0)
    hi = (t1 * xc).upper()
    hi = hi if hi > 0 else arb(0)
    r = list(rh)
    r[ix['vx_lo']], r[ix['vx_hi']] = dec_lo(lo), dec_hi(hi)   # the two ends apart: a ball's hull of [0, hi] would read below 0
    r[ix['xc_lo']], r[ix['xc_hi']], r[ix['xf_hi']] = dec_lo(xc), dec_hi(xc), '0'
    return r


def ta_row_v4(jlo, jhi, E, windowed):
    """v2_1: MR_INSERT's t or a row from ta_rows' dict E: power 0, so xc is the amplitude's own two strings and xf = 0."""
    s = [dec_lo(E['vx']), dec_hi(E['vx'])]
    return ins_fields(jlo, jhi, E['vx'], E['vy'], E['Pevw'], E['Pev'], E['vp'], E.get('m'), E['pebw'], E['win'], E['C'], windowed, tuple(s), '0')


def factx_check(rows, fields, tamper=None):
    """v2_1 C-FACTX and C-FLOOR on the written decimals (the M1 engine's G-FACTX and G-FLOOR, exact Fractions): an h row's t xc -+ xf lies
    inside [vx_lo, vx_hi] at both ends of its piece (t = 1/jlo and 1/jhi, or 0 on the last piece; relative slack 1e-14 as the engine), a t or a
    row has xc equal to vx string for string and xf = 0, and xf > 0 only on the last piece's h row. Returns the number of rows checked."""
    from decimal import Decimal as Dm
    ix = dict((f, i) for i, f in enumerate(fields))
    n = 0
    for k, v in rows:
        it = k.rsplit('_', 1)[1]
        jlo, jhi = v[ix['jlo']], v[ix['jhi']]
        lo, hi, clo, chi, ff = (Fraction(Dm(v[ix[f]])) for f in ('vx_lo', 'vx_hi', 'xc_lo', 'xc_hi', 'xf_hi'))
        if ff < 0 or (ff > 0 and (jhi != 'inf' or it != 'h')):
            raise Refused('C-FLOOR: row %s has the floor %s off the last piece or on a power-0 row' % (k, v[ix['xf_hi']]))
        n += 1
        if it in ('t', 'a'):
            if (v[ix['xc_lo']], v[ix['xc_hi']]) != (v[ix['vx_lo']], v[ix['vx_hi']]):
                raise Refused('C-FACTX: row %s: with power 0 xc must equal vx' % k)
            continue
        slack = Fraction(1, 10 ** 14) * max(abs(lo), abs(hi))
        for t in [Fraction(1) / Fraction(Dm(jlo))] + ([Fraction(0)] if jhi == 'inf' else [Fraction(1) / Fraction(Dm(jhi))]):
            if t * clo - ff < lo - slack or t * chi + ff > hi + slack:
                raise Refused('C-FACTX: row %s: t xc with the floor leaves the amplitude at t = %.6e' % (k, float(t)))
    return n


def anchor_check(rows, fields):
    """v2_1 C-ANCHOR, the M1 engine's anchors on MR_INSERT (G6 v1_6_2 sect. 6): t and a v_x > 0 and h, t and a v_y > 0 on every row, and h's
    v_x lower end > 0 on every piece with t_lo > 0 (the orientation)."""
    from decimal import Decimal as Dm
    ix = dict((f, i) for i, f in enumerate(fields))
    for k, v in rows:
        it = k.rsplit('_', 1)[1]
        if not Dm(v[ix['vy_lo']]) > 0:
            raise Refused('C-ANCHOR: row %s has vy_lo <= 0' % k)
        if (it in ('t', 'a') or v[ix['jhi']] != 'inf') and not Dm(v[ix['vx_lo']]) > 0:
            raise Refused('C-ANCHOR: row %s has vx_lo <= 0' % k)
    return len(rows)


def rec_text_v4(fields, rows, extra, source):
    """v2_1: the MR_INSERT v4 record text: header (FORMAT, RECORD, PRODUCER, CODE, STATUS, EXPORT_STATUS, RUN_VERDICT, SOURCE, J_UNIFORMITY,
    then the extra lines: ORIENTATION, ORIENT_CHECK, TRIAL_SET, X_POWER, X_DEFINITION, LEMMAP_SHA256, PEV_ROUTE), FIELDS, then one row per
    piece and item, 'N<N>_P<idx4>_<h|t|a> = values'."""
    cert = MODE == 'cert'
    head = ['# MR_INSERT (pk25, %s %s): written by %s' % (LABEL, MODE, LABEL),
            'FORMAT = MR_INPUT_KV_v4', 'RECORD = MR_INSERT', 'PRODUCER = pk25 %s' % LABEL,
            'CODE = pk25/asm/%s.py:%s' % (LABEL, sha_file(SELF)), 'STATUS = %s' % ('CERTIFIED' if cert else 'DRY'),
            'EXPORT_STATUS = %s' % ('CERTIFIED' if cert else 'DRY'), 'RUN_VERDICT = VALID', 'SOURCE = %s' % source,
            'J_UNIFORMITY = PER-PIECE: every row holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf (t = 0)'] + extra
    return '\n'.join(head + ['FIELDS = %s' % fields] + ['%s = %s' % (k, ' '.join(v)) for k, v in rows]) + '\n'


def readback_v4(text, TX, rows, counts, tamper=None):
    """v2_1 C-WRITE on the MR_INSERT v4 text: the M1 engine's kv_read rules (header keys until FIELDS, no repeated key, '=' on every line),
    FORMAT MR_INPUT_KV_v4, RECORD, ORIENTATION, PRODUCER's first word pk25, X_POWER and X_DEFINITION equal to the engine's, ORIENT_CHECK
    matching ORIENT_RX with this record's piece counts, TRIAL_SET equal to mr/v3 MR_SPECTRAL's, FIELDS, the rows equal to memory with unique
    keys, finite decimals, *_lo <= *_hi, single *_hi >= 0. tamper: 'ROW' changes the first row's third value, 'OCHK' drops ORIENT_CHECK."""
    from decimal import Decimal as Dm
    if tamper == 'ROW':
        k0, v0 = rows[0]
        text = text.replace('%s = %s' % (k0, ' '.join(v0)), '%s = %s' % (k0, ' '.join(v0[:2] + ['9' + v0[2]] + v0[3:])), 1)
    if tamper == 'OCHK':
        text = '\n'.join(ln for ln in text.split('\n') if not ln.startswith('ORIENT_CHECK = ')) + '\n'
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
    if (head.get('FORMAT'), head.get('RECORD'), head.get('ORIENTATION')) != ('MR_INPUT_KV_v4', 'MR_INSERT', TX['orient']):
        raise Refused('C-WRITE: FORMAT, RECORD or ORIENTATION')
    if head.get('PRODUCER', '').split()[:1] != ['pk25'] or head.get('X_POWER') != TX['xpow'] or head.get('X_DEFINITION') != TX['xdef']:
        raise Refused('C-WRITE: PRODUCER, X_POWER or X_DEFINITION')
    mo = re.match(TX['orient_rx'], head.get('ORIENT_CHECK', ''))
    if not mo or (int(mo.group(1)), int(mo.group(2))) != (counts[4], counts[3]):
        raise Refused('C-WRITE: ORIENT_CHECK missing or with other piece counts')
    if head.get('TRIAL_SET') != trial_set_line():
        raise Refused('C-WRITE: TRIAL_SET differs from mr/v3 MR_SPECTRAL')
    if flds != TX['fields'].split() or got != [(k, list(v)) for k, v in rows] or len(set(k for k, _ in got)) != len(got):
        raise Refused('C-WRITE: FIELDS or rows differ from memory')
    for k, vals in got:
        row = dict(zip(flds, vals))
        for f, v in row.items():
            if f in ('jlo', 'jhi', 'windowed'):
                continue
            if not re.fullmatch(r'-?[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?', v) or not Dm(v).is_finite():
                raise Refused('C-WRITE: row %s field %s = %s' % (k, f, v))
        for f in row:
            if f.endswith('_lo') and (f[:-3] + '_hi') in row and Dm(row[f]) > Dm(row[f[:-3] + '_hi']):
                raise Refused('C-WRITE: row %s has %s > %s_hi' % (k, f, f[:-3]))
            if f.endswith('_hi') and (f[:-3] + '_lo') not in row and Dm(row[f]) < 0:
                raise Refused('C-WRITE: row %s has %s < 0' % (k, f))
    return len(got)


def mu_refuses(fn):
    """v2_1, for the C8 note N2: the mu tool's refusal (ValueError) of an input outside its domain, turned into a Refused for plant()."""
    try:
        fn()
    except ValueError as e:
        raise Refused('C-MU-DOMAIN: the mu tool refused: %s' % e)


def main():
    t0 = time.time()
    fails, nofire, EXEC = [], [], []

    def run_plant(name, fn):
        EXEC.append(name)
        plant(nofire, name, fn)

    def flag(fn):
        try:
            fn()
            return True
        except Refused as e:
            out('  refused: %s' % e)
            return False
    out('%s sha256 %s MODE=%s TAG=%s (MR_INSERT v5 producer, v4 FIELDS: h rows from S9(c)-h, the last h rows by route (B) way A, t and a rows, the G6 v1_6_2 sect. 6 header; %s)' % (
        LABEL, sha_file(SELF), MODE, TAG, 'CERTIFIED record to mr/v5b' if MODE == 'cert' else 'DRY record to asm/dry_%s' % TAG))
    bad = ['%s %s' % (os.path.basename(p), sha_file(p)[:8]) for p in sorted(PINS) if sha_file(p) != PINS[p]]
    out('C-HASH %s (%d pinned files)%s' % ('PASS' if not bad else 'FAIL', len(PINS), (': ' + '; '.join(bad)) if bad else ''))
    if bad:
        out('VERDICT INVALID (C-HASH)')
        return 2
    try:
        n = check_core2()
        out('C-CORE PASS: %d copies equal R4 (%s) and the C6a engine (%s), each defined once' % (n, R4_SHA[:8], C6A_SHA[:8]))
    except Refused as e:
        out('C-CORE FAIL: %s' % e)
        out('VERDICT INVALID (C-CORE)')
        return 2
    run_plant('PLANT-CORE', lambda: check_core2(tamper=True))
    P, _gd = read_grid()
    FIRST = check_grid(P)
    IN = {}
    IN['RD'] = load_rdr()
    IN['LW'] = dict((N, load_laws(IN['RD'], N)) for N in (4, 3))
    out('C-LAW-READ: S8 D, E2, E3, FF with m3_lawcert_v1_1, S8 N with m3_lawcert_v1_2, pk25 NIH, NHT, DH with m3_lawcert_s9h_v1_1, through '
        'm3_reader_s9h_v1 (%s), both N -> %s' % (PINS[RDR][:8], gate(fails, 'C-LAW-READ', True)))
    RE = dict((N, load_ritz(N, 'CERTIFIED')) for N in (4, 3))
    out('C-ALIAS: the S8 entries for G, T and Dx carry the S9 records\' ak (both N) -> %s' % gate(
        fails, 'C-ALIAS', all(flag(lambda N=N: check_alias(IN['LW'][N], RE[N])) for N in (4, 3))))
    IN['RE'] = RE
    IN['M2R'], IN['M2MOD'], _m2l = load_m2b()
    IN['MC'] = dict((N, m2b_mhat_coeffs(lines_of(M2B[1]), N)) for N in (4, 3))
    IN['M4REC'], IN['M4MOD'] = load_m4()
    IN['M4HREC'], IN['M4HMOD'] = load_m4h()
    IN['MU'] = load_mu()
    out('C-READ: M2B (%s), M4 (%s), M4H (%s), the mu tool %s (%s) through their pinned files -> %s' % (
        PINS[M2B[0]][:8], PINS[M4[0]][:8], PINS[M4H[0]][:8], os.path.basename(MU), PINS[MU][:8], gate(fails, 'C-READ', True)))
    m = re.findall(r'tau_4\(4\) = ([0-9]+\.[0-9]+),\s+tau_4\(3\) = ([0-9]+\.[0-9]+),', open(S4C_RECORD).read())
    if len(m) != 1:
        out('VERDICT INVALID (the S4(c) claim line)')
        return 2
    IN['TOK'] = {4: m[0][0], 3: m[0][1]}
    IN['TAU4A'] = dict((N, arb(IN['TOK'][N])) for N in (4, 3))
    IN['LG'] = lg_constants(IN['M2MOD'], IN['M2R'])
    out('C-R4-LG: S_eps, G_00, Phi_eps, Phi_eps,theta, NA-prime and kappa_max equal R4\'s certified run output (%s) -> %s' % (
        PINS[R4_CERT_OUT][:8], gate(fails, 'C-R4-LG', flag(lambda: check_r4_lg(IN['LG'])))))
    IN['TS'], IN['SIG'], IN['MG'], IN['ENGA'] = {}, {}, {}, {}
    for N in (4, 3):
        IN['TS'][N], IN['SIG'][N] = orient_signs(N)
        IN['MG'][N] = load_m4_mg(N)
        IN['ENGA'][N] = load_enga_m(N)
    out('C-ORIENT-SIGNS: u~_x times %+d (N4), %+d (N3); u~_y times %+d, %+d -> %s' % (
        IN['SIG'][4][0], IN['SIG'][3][0], IN['SIG'][4][1], IN['SIG'][3][1], gate(fails, 'C-ORIENT-SIGNS', True)))
    out('C-MBG: M4_KV_v1\'s N<N>_E1_MG and E3_MG coefficients m_bg(t) (kt_cert\'s own m_g) from %s (%s) -> %s' % (
        os.path.basename(M4[0]), PINS[M4[0]][:8], gate(fails, 'C-MBG', True)))
    run_plant('PLANT-MBG-PIN', lambda: load_m4_mg(4, dict(PINS, **{M4[0]: '0' * 64})))
    IN['LM'] = load_lemmap()
    out('C-LEMMAP: MR_LEMMAP v3 %s (%s) read, %d rows (cleared by the review 087868a8, main row 4401) -> %s' % (
        os.path.relpath(LEMMAP, W18), PINS[LEMMAP][:8], len(IN['LM']), gate(fails, 'C-LEMMAP', True)))
    IN['MEANS'] = load_means(P)
    IN['SV'] = load_sv2(P)
    out('C-MEANS-SV: R4\'s means export (%s; c_t from D3, c_a = c_b from D4) and the S_V export (%s; Bp_hi, vp2_hi) on R4\'s grid -> %s' % (
        PINS[MEANS][:8], PINS[S67[0]][:8], gate(fails, 'C-MEANS-SV', True)))
    try:
        IN['DJ'] = load_dj(IN['RD'])
        dj_ok = True
    except Refused as e:
        out('  refused: %s' % e)
        dj_ok = False
    out('C-DJ-READ: pk22\'s c3j DJ records (N4 %s, N3 %s) through m3_reader_s9h_v1 -> %s' % (
        PINS[DJREC[4][0]][:8], PINS[DJREC[3][0]][:8], gate(fails, 'C-DJ-READ', dj_ok)))
    try:   # v2_3: pk23's option (B) records and Lemma RHO's record
        IN['PB'] = load_pevb(IN['RD'])
        IN['RHO'] = load_rho()
        low = [N for N in (4, 3) if not all(Fraction(a) >= IN['RHO'][1] for (_i, a, _b) in P[N][FIRST[N]:])]
        if low:
            raise Refused('C-RHO: a piece at N = %s starts below the record\'s J0' % low)
        tw = arb(0).union(arb(1) / 300)
        tt = [N for N in (4, 3) if not dj_piece(IN['RD'], IN['PB'][N]['L'], 'TT,0,0', tw).overlaps(dj_piece(IN['RD'], IN['PB'][N]['LH'], 'TTh,0,0', tw))]
        if tt:
            raise Refused('C-PEVB-TT: TTh,0,0 (family LH) misses TT,0,0 (family L) at N = %s' % tt)
        pb_ok = True
    except Refused as e:
        out('  refused: %s' % e)
        pb_ok = False
    out('C-PEVB-READ: pk23\'s option (B) records (%s) through m3_reader_s9h_v1; Lemma RHO\'s record %s (%s): RHO_HI = %s for J >= %s, every piece '
        'from J_low on; TTh,0,0 overlaps TT,0,0 -> %s' % (
            ', '.join('N%d %s %s' % (N, f, PINS[PEVB[N][f][0]][:8]) for N in (4, 3) for f in ('L', 'LH', 'LT')), os.path.relpath(RHOREC, W18),
            PINS[RHOREC][:8], IN['RHO'][0] if pb_ok else '-', IN['RHO'][1] if pb_ok else '-', gate(fails, 'C-PEVB-READ', pb_ok)))
    run_plant('PLANT-PEVB-PIN', lambda: load_pevb(IN['RD'], dict(PINS, **{PEVB[4]['LH'][0]: '0' * 64})))
    run_plant('PLANT-RHO-PIN', lambda: load_rho(pins=dict(PINS, **{RHOREC: '0' * 64})))
    try:
        TX = m1_texts()
        TSL = trial_set_line()
        ok = True
    except Refused as e:
        out('  refused: %s' % e)
        ok = False
    out('C-M1-TEXTS: MR_INSERT v4 FIELDS, X_POWER, X_DEFINITION, ORIENTATION and the ORIENT_CHECK pattern from %s (%s); TRIAL_SET from %s (%s) -> %s' % (
        os.path.relpath(M1ENG, W18), PINS[M1ENG][:8], os.path.relpath(SPEC_V3, W18), PINS[SPEC_V3][:8], gate(fails, 'C-M1-TEXTS', ok)))
    try:   # v2_5: P2's factored table and P1's exact t^0 data for way A
        IN['WA'] = waya_load(MODE)
        ok = True
    except Refused as e:
        out('  refused: %s' % e)
        ok = False
    out('C-WAYA-IN: P2\'s %s (%s, STATUS %s) and P1\'s %s (%s): SOURCE names MR_LEMMAP v3 and C10, UHAT0 lines equal, uhat_0(0) = (1, 0, 0), '
        'G0_00 = 1 -> %s' % (os.path.relpath(P2REC, W18), PINS[P2REC][:8], IN['WA']['head']['STATUS'] if ok else '-', os.path.relpath(C10REC, W18),
                             PINS[C10REC][:8], gate(fails, 'C-WAYA-IN', ok)))
    run_plant('PLANT-WAYA-PIN', lambda: waya_load(MODE, dict(PINS, **{P2REC: '0' * 64})))
    try:   # v2_6: the shared main_N of the T and NIH entries
        ok = all(main_n_check(N, S8REC[N]['N'][0], HREC[N]['NIH'][0]) for N in (4, 3))
    except Refused as e:
        out('  refused: %s' % e)
        ok = False
    out('C-MAIN-N: S8 N\'s records (N4 %s, N3 %s) have graph N, the NIH records (N4 %s, N3 %s) name the vertex graph VN, and the families carry '
        'equal prep parameters (a_v, ap, theta0): the T and NIH entries share main_N -> %s' % (
            PINS[S8REC[4]['N'][0]][:8], PINS[S8REC[3]['N'][0]][:8], PINS[HREC[4]['NIH'][0]][:8], PINS[HREC[3]['NIH'][0]][:8],
            gate(fails, 'C-MAIN-N', ok)))
    run_plant('PLANT-MAIN-N', lambda: main_n_check(4, S8REC[4]['D'][0], HREC[4]['NIH'][0]))
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2
    # S9C stage 1: the bad-part constants (S9C_BADPART_LEMMA_v1) at Lam = LAM9C and, for PLANT-BAD, at Lam = 10
    IN['BP'], IN['BP10'] = {}, {}
    for N in (4, 3):
        try:
            IN['BP'][N] = badpart_constants(N, IN, LAM9C)
            IN['BP10'][N] = badpart_constants(N, IN, 10)
            ok = True
        except Refused as e:
            out('  refused: %s' % e)
            ok = False
        if not gate(fails, 'C-BADPART N=%d' % N, ok) == 'PASS':
            continue
        D = IN['BP'][N]
        B = bad_bc(D)
        mx = max([float(D[k]) for k in ('P0', 'P1', 'P3')] + [float(x) for x in B.values()])
        out('BADPART N=%d Lam %s: normalised P_0 %s, P_1 %s, P_3 %s; B_bc = X_bc + X_cb + F_bc (b, c in 1, 3): B_11 %s, B_13 %s, B_33 %s -> '
            'C-BAD-SMALL %s' % (N, LAM9C, dec_hi(D['P0']), dec_hi(D['P1']), dec_hi(D['P3']), dec_hi(B[(1, 1)]), dec_hi(B[(1, 3)]),
                                dec_hi(B[(3, 3)]), gate(fails, 'C-BAD-SMALL N=%d' % N, mx <= float(BAD_TOL))))
    if 4 in IN['BP']:
        def gbb_plant():
            D = badpart_constants(4, IN, LAM9C, plant='GBB')
            if D['Phi'][1] > IN['BP'][4]['Phi'][1]:
                raise Refused('C-GBB: halving G_11 raised Phi_1 (the bound reads G_bb)')
        run_plant('PLANT-GBB', gbb_plant)
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2
    # the mu tool for t (C_t, OR_t): c_t's interval ends by exact comparison
    IN['ORT'], IN['CCT'] = {}, {}
    for N in (4, 3):
        prs = P[N][FIRST[N]:]
        clo = chi = None
        for idx, _a, _b in prs:
            lo_, hi_ = IN['MEANS'][N][idx][0].lower(), IN['MEANS'][N][idx][1].upper()
            clo = lo_ if clo is None or lo_ < clo else clo
            chi = hi_ if chi is None or hi_ > chi else chi
        tmax = t_ends(prs[0][1], prs[0][2])[1]
        try:
            up_, lw_, inf_ = IN['MU'].one_row(N, tmax, clo, chi)
        except ValueError as e:
            out('VERDICT INVALID (the mu tool refused for t: %s)' % e)
            return 2
        IN['ORT'][N] = up_.upper()
        IN['CCT'][N] = (up_ * (IN['LG'][N]['kap']).sqrt()).upper()
        out('MU-T N=%d: c_t over the pieces in [%s, %s] (exact ends); OR_t <= %s at t <= %s (%d boxes); C_t = OR_t kappa_max^1/2 <= %s' % (
            N, dec_lo(clo), dec_hi(chi), dec_hi(IN['ORT'][N]), dec_hi(tmax), inf_['boxes'], dec_hi(IN['CCT'][N])))
    # pass 1: the Ritz-level mean c~_h on every piece; the mu tool's interval; OR and C per N
    IN['CI'], IN['OR'], IN['CC'] = {}, {}, {}
    for N in (4, 3):
        prs = P[N][FIRST[N]:]
        lo_ = hi_ = None
        for idx, jlo, jhi in prs:
            tl, th, JL = piece_t(jlo, jhi)
            c0 = h_piece(N, tl, th, JL, 'N%d_P%s' % (N, idx), IN, mode='c0')['ch0']
            lo_ = c0.lower() if lo_ is None or c0.lower() < lo_ else lo_
            hi_ = c0.upper() if hi_ is None or c0.upper() > hi_ else hi_
        IN['CI'][N] = ((lo_ - arb(CI_MARGIN)).lower(), (hi_ + arb(CI_MARGIN)).upper())
        tmax = t_ends(prs[0][1], prs[0][2])[1]
        try:
            up_, lw_, inf_ = IN['MU'].one_row(N, tmax, IN['CI'][N][0], IN['CI'][N][1])
        except ValueError as e:
            out('VERDICT INVALID (the mu tool refused: %s)' % e)
            return 2
        IN['OR'][N] = up_.upper()
        IN['CC'][N] = (up_ * (IN['LG'][N]['kap']).sqrt()).upper()
        out('MU N=%d: c~_h over the pieces in [%s, %s]; the interval [%s, %s]; OR <= %s at t <= %s (%d boxes); C = OR kappa_max^1/2 <= %s' % (
            N, dec_lo(lo_), dec_hi(hi_), dec_lo(IN['CI'][N][0]), dec_hi(IN['CI'][N][1]), dec_hi(IN['OR'][N]), dec_hi(tmax), inf_['boxes'],
            dec_hi(IN['CC'][N])))
    t4max = t_ends(P[4][FIRST[4]][1], P[4][FIRST[4]][2])[1]
    run_plant('PLANT-MU-T', lambda: mu_refuses(lambda: IN['MU'].one_row(4, arb(1) / 298, IN['CI'][4][0], IN['CI'][4][1])))
    run_plant('PLANT-MU-C', lambda: mu_refuses(lambda: IN['MU'].one_row(4, t4max, IN['CI'][4][1], IN['CI'][4][0])))
    for N in (4, 3):
        idx0, jlo0, jhi0 = P[N][FIRST[N]]
        tl0, th0, JL0 = piece_t(jlo0, jhi0)
        run_plant('PLANT-ORIENT N=%d' % N, lambda N=N, a=(tl0, th0, JL0, idx0): h_piece(N, a[0], a[1], a[2], 'N%d_P%s' % (N, a[3]), IN, mode='c0',
                                                                                          plant='ORIENT'))
    # pass 2: h (S9(c)), t and a on every piece; the last piece by way B on S9(c)'s v_x
    rows, perr, hst, last = [], {}, {}, {}
    for N in (4, 3):
        prs = P[N][FIRST[N]:]
        hst[N] = []
        for j, (idx, jlo, jhi) in enumerate(prs):
            tl, th, JL = piece_t(jlo, jhi)
            key = 'N%d_P%s' % (N, idx)
            try:
                if jhi == 'inf':
                    glo, ghi, f, F0, nsub, vxh, vyh, subs, D0 = last_piece_floor(N, tl, th, key, IN, ratio=Fraction(11, 10), s9c=s9c_htx)
                    L = dict(glo=glo, ghi=ghi, f=f, F0=F0, nsub=nsub, vxh=vxh, idx=idx)
                    Dagg = agg([s[2] for s in subs] + [D0])
                    Dta = h_piece(N, arb(0), th, JL, key, IN, mode='full')
                    rh = h_last_row_v4(N, jlo, jhi, th, L, Dagg, IN)
                    WA = waya_last(N, jlo, th, JL, key, IN, Dta)   # v2_5: route (B) way A replaces way B's xc, xf and vx
                    rh = waya_row(rh, WA, TX['fields'].split())
                    L.update(WA=WA, Dta=Dta, key=key, jlo=jlo, th=th, JL=JL)
                    rt, ra = ta_row_v4(jlo, jhi, Dta['t'], '1'), ta_row_v4(jlo, jhi, Dta['a'], '0')
                    last[N] = L
                else:
                    D = h_piece(N, tl, th, JL, key, IN, mode='full', s9c=s9c_htx)
                    rh, hx = h_row_v4(N, jlo, jhi, tl, th, JL, D, IN)
                    rt, ra = ta_row_v4(jlo, jhi, D['t'], '1'), ta_row_v4(jlo, jhi, D['a'], '0')
                    hst[N].append((idx, jlo, D['S9'], hx))
            except Refused as e:
                g = str(e).split(':')[0] if str(e).startswith('C-') else 'C-PIECE (%s)' % str(e)[:50]
                perr.setdefault(g, []).append(key)
                continue
            rows += [(key + '_h', rh), (key + '_t', rt), (key + '_a', ra)]
        nN = sum(1 for k, _v in rows if k.startswith('N%d_' % N) and k.endswith('_h'))
        out('C-PIECE N=%d: %d of %d pieces carry h (S9(c), the last by route (B) way A), t and a rows (C-ORIENT on every piece) -> %s' % (
            N, nN, len(prs), gate(fails, 'C-PIECE N=%d' % N, nN == len(prs))))
    for g, v in sorted(perr.items()):
        out('  refusals %s: %d pieces, first %s' % (g, len(v), v[0]))
    rw = lambda x: float(x.rad()) / abs(float(x.mid())) if float(x.mid()) != 0 else float('inf')
    for N in (4, 3):
        H = hst.get(N, [])
        if not H:
            continue
        n9 = sum(1 for h in H if bool(h[2]['vx'] > 0 or h[2]['vx'] < 0))
        out('C-SIGN-S9C N=%d: S9(c)\'s v_x certainly signed on %d of %d pieces with t_lo > 0 -> %s' % (
            N, n9, len(H), gate(fails, 'C-SIGN-S9C N=%d' % N, n9 == len(H))))
        bmax = max(H, key=lambda h: float(h[2]['badw']))
        out('C-BAD-W N=%d: the weighted bad parts at most %s (piece %s) <= %s -> %s' % (
            N, dec_hi(bmax[2]['badw']), bmax[0], BAD_TOL, gate(fails, 'C-BAD-W N=%d' % N, bmax[2]['badw'] <= arb(BAD_TOL))))
        wv = max((rw(h[3]['vx']), h[0]) for h in H)
        wx = max((rw(h[3]['xc']), h[0]) for h in H)
        out('INFO WIDTH N=%d: h row relative half-widths, largest: vx %.3e (piece %s), xc %.3e (piece %s); S9(c) v_x alone %.3e' % (
            N, wv[0], wv[1], wx[0], wx[1], max(rw(h[2]['vx']) for h in H)))
        L = last.get(N)
        if L:
            out('INFO WAYB-S9C N=%d last piece %s (v4b\'s way B, replaced by way A below): xc = [%s, %s], xf = %s (F0 %s, %d sub-pieces, ratio 11/10); the sign holds for J < %s' % (
                N, L['idx'], dec_lo(L['glo']), dec_hi(L['ghi']), dec_hi(L['f']), dec_hi(L['F0']), L['nsub'],
                dec_lo((L['glo'] / L['f']).lower()) if L['glo'] > 0 else 'none'))
            A = L['WA']
            out('C-WAYA-T0, C-WAYA N=%d last piece %s: the t^0 combination sum_b c_x0,b [LO_0, HI_0] = %s holds 0; h~/t = %s with '
                '1/(G_00^1/2 Lambda) = %s (Lambda in %s); remainders over t: R_1 %s, |c_h| R_2 %s, dh_x %s (delta_0/t %s, sum |uhat_0b - uhat_0b(0)|/t %s); '
                'xc = [%s, %s] certainly positive, xf = 0; vx refreshed to [0, %s] -> PASS' % (
                    N, L['idx'], A['z0'].str(4), A['ht'].str(10), A['F'].str(10), A['Lam'].str(10), dec_hi(A['R1t']), dec_hi(A['R2t']),
                    dec_hi(A['dht']), dec_hi(A['d0t']), dec_hi(A['U0t']), dec_lo(A['xc']), dec_hi(A['xc']), dec_hi((A['t1'] * A['xc']).upper())))
    fields = TX['fields']
    nf = len(fields.split())
    out('C-ROW-LEN: every row carries the %d v4 fields -> %s' % (nf, gate(fails, 'C-ROW-LEN', all(len(v) == nf for _k, v in rows))))
    out('C-ANCHOR: t and a v_x > 0, h, t and a v_y > 0, h v_x > 0 off the last piece, on all %d rows -> %s' % (
        len(rows), gate(fails, 'C-ANCHOR', flag(lambda: anchor_check(rows, fields.split())))))
    out('C-FACTX: h rows t xc -+ xf inside the amplitude at both ends, t and a rows xc = vx, floors only on the last h rows -> %s' % (
        gate(fails, 'C-FACTX', flag(lambda: factx_check(rows, fields.split())))))
    idx0, jlo0, jhi0 = P[4][FIRST[4]]
    tl0, th0, JL0 = piece_t(jlo0, jhi0)
    key0 = 'N4_P%s' % idx0

    def factx_plant():
        D = h_piece(4, tl0, th0, JL0, key0, IN, mode='hx', s9c=s9c_htx)
        r, _x = h_row_v4(4, jlo0, jhi0, tl0, th0, JL0, D, IN, plant='FACTX')
        factx_check([(key0 + '_h', r)], fields.split())
    run_plant('PLANT-FACTX', factx_plant)

    def waya_plant(pl):   # v2_5: way A on N = 4's last piece with a planted fault
        L4 = last[4]
        waya_last(4, L4['jlo'], L4['th'], L4['JL'], L4['key'], IN, L4['Dta'], plant=pl)
    run_plant('PLANT-WAYA-ZERO', lambda: waya_plant('ZERO'))
    run_plant('PLANT-WAYA-ORIENT', lambda: waya_plant('ORIENT'))

    def anchor_plant():
        k, v = [(k, v) for k, v in rows if k.endswith('_t')][0]
        anchor_check([(k, v[:2] + ['-' + v[2]] + v[3:])], fields.split())
    run_plant('PLANT-ANCHOR', anchor_plant)
    try:
        fd, Dd, pos = der_fd_check(4, tl0, th0, JL0, IN)
        ok = True
    except Refused as e:
        out('  refused: %s' % e)
        ok = False
    out('C-DER-FD N=4 piece %s: the difference quotient %s against dM_R^c/dt %s -> %s' % (
        idx0, fd.str(8) if ok else '-', Dd.str(8, radius=True) if ok else '-', gate(fails, 'C-DER-FD', ok)))
    run_plant('PLANT-DER', lambda: der_fd_check(4, tl0, th0, JL0, IN, plant='DER'))
    run_plant('PLANT-IHT0', lambda: s9c_main_piece(4, tl0, th0, JL0, IN, plant='IHT0'))

    def sign_plant(pl):
        D = h_piece(4, tl0, th0, JL0, key0, IN, mode='hx', s9c=lambda a, b, c, d, e, f: s9c_htx(a, b, c, d, e, f, plant=pl))
        if not bool(D['S9']['vx'] > 0 or D['S9']['vx'] < 0):
            raise Refused('C-SIGN-S9C: v_x is not certainly signed with plant %s' % pl)
    run_plant('PLANT-HQ', lambda: sign_plant('HQ'))
    run_plant('PLANT-RB', lambda: sign_plant('RB'))

    def bad_plant():
        D = h_piece(4, tl0, th0, JL0, key0, IN, mode='hx', s9c=lambda a, b, c, d, e, f: s9c_htx(a, b, c, d, e, f, plant='BAD'))
        if D['S9']['badw'] > arb(BAD_TOL):
            raise Refused('C-BAD-W: the weighted bad parts at Lam = 10 exceed %s' % BAD_TOL)
    run_plant('PLANT-BAD', bad_plant)
    counts = dict((N, sum(1 for k, _v in rows if k.startswith('N%d_' % N) and k.endswith('_h'))) for N in (4, 3))
    ipev = fields.split().index('Pev_hi')   # v2_3: the option (B) Pev per N and item, for pk24's runs
    for N in (4, 3):
        for kind in ('h', 't'):
            pv = [(Fraction(v[ipev]), k) for k, v in rows if k.startswith('N%d_' % N) and k.endswith('_' + kind)]
            out('INFO PEV N=%d %s: Pev_hi from %.4g to %.4g over %d pieces; first piece %s %.4g; last piece %s %.4g' % (
                N, kind, float(min(pv)[0]), float(max(pv)[0]), len(pv), pv[0][1], float(pv[0][0]), pv[-1][1], float(pv[-1][0])))
            out('INFO PEV MAX N=%d %s: the largest certified Pev_hi is %s on %s (the row 4520)' % (N, kind, rows_val(rows, max(pv)[1], ipev), max(pv)[1]))
    out('C-PEVB-T048: every t row\'s Pev_hi <= 0.48 (the row 4520; above it the subtraction route of RHO_LEMMA_v1_ADD1 is used) -> %s' % gate(
        fails, 'C-PEVB-T048', flag(lambda: t048(rows, ipev, Fraction(48, 100)))))
    run_plant('PLANT-T048', lambda: t048(rows, ipev, Fraction(3, 10)))
    ochk = ('C-ORIENT PASS on every piece (N4 %d, N3 %d): u~_x has a positive coefficient on the canonical e1 and u~_y on the canonical e3; '
            'plant PLANT-ORIENT fired' % (counts[4], counts[3]))
    oriented = ('C-PIECE N=4' not in fails and 'C-PIECE N=3' not in fails and 'PLANT-ORIENT N=4' in EXEC and 'PLANT-ORIENT N=3' in EXEC and
                'PLANT-ORIENT N=4' not in nofire and 'PLANT-ORIENT N=3' not in nofire and re.match(TX['orient_rx'], ochk) is not None)
    out('C-ORIENT-LINE: C-ORIENT passed on every piece of the record (N4 %d, N3 %d), PLANT-ORIENT fired at both N, the line matches the M1 '
        'engine\'s ORIENT_RX -> %s' % (counts[4], counts[3], gate(fails, 'C-ORIENT-LINE', oriented)))
    source = ('S8 law certificates m3_lawcert_v1_1 N4 %s N3 %s, m3_lawcert_v1_2 N4 %s N3 %s (pk03); pk25 m3_lawcert_s9h_v1_1 N4 %s N3 %s; '
              'M2B_KV_v1 %s; M4_KV_v1 %s (R_e1, R_e3 and the E1_MG, E3_MG lines; A_am); M4H_KV_v1 %s (A_h); S4(c) v1_1 %s (tau4 claim); R4 %s '
              '(CORE); mu tool %s; MR_LEMMAP v3 %s; R4 means export %s; S_V export %s; pk22 c3j DJ N4 %s N3 %s; S9C bad-part lemma '
              'S9C_BADPART_LEMMA_v1; pk23 option (B) records N4 %s, N3 %s; Lemma RHO record %s' % (
                  PINS[S8CERT[4]['v1_1'][0]][:8], PINS[S8CERT[3]['v1_1'][0]][:8], PINS[S8CERT[4]['v1_2'][0]][:8], PINS[S8CERT[3]['v1_2'][0]][:8],
                  PINS[HCERT[4][0]][:8], PINS[HCERT[3][0]][:8], PINS[M2B[0]][:8], PINS[M4[0]][:8], PINS[M4H[0]][:8], PINS[S4C_RECORD][:8],
                  R4_SHA[:8], PINS[MU][:8], PINS[LEMMAP][:8], PINS[MEANS][:8], PINS[S67[0]][:8], PINS[DJREC[4][0]][:8], PINS[DJREC[3][0]][:8],
                  '+'.join(PINS[PEVB[4][f][0]][:8] for f in ('L', 'LH', 'LT')), '+'.join(PINS[PEVB[3][f][0]][:8] for f in ('L', 'LH', 'LT')),
                  PINS[RHOREC][:8]))
    source += ('; v2_5 the last h rows by route (B) way A (P4_LEMMA_NOTE_v1_1 %s): P2 MR_LEMMAP_V3F %s %s (STATUS %s), C10 %s' % (
        PINS[P4NOTE][:8], os.path.relpath(P2REC, W18), PINS[P2REC][:8], IN['WA']['head']['STATUS'], PINS[C10REC][:8]))
    extra =['ORIENTATION = %s' % TX['orient'], 'ORIENT_CHECK = %s' % ochk, 'TRIAL_SET = %s' % TSL, 'X_POWER = %s' % TX['xpow'],
             'X_DEFINITION = %s' % TX['xdef'], 'LEMMAP_SHA256 = %s' % PINS[LEMMAP],
             'PEV_ROUTE = Pev_hi = min(C, V) for h and t, V = |u00| ((c - e1)^2 + e2 - e1^2 - 2 e1 + (N - 1)/2 + rho)_+^1/2 + C (|u01| + |u03|) + C delta_0 >= |v| >= |P_e v|, e_k = E_k/E_0 from pk23\'s option (B) records, rho = RHO_HI of pk25/rho/RHO_RECORD_v1.kv:%s (Lemma RHO, pk25/rho/RHO_LEMMA_v1.md sect. 4; the rows 4422, 4426, 4491, 4520)' % PINS[RHOREC]]
    text = rec_text_v4(fields, rows, extra, source)
    out('C-WRITE: the MR_INSERT v4 text read back by the M1 engine\'s rules (%d rows) -> %s' % (
        len(rows), gate(fails, 'C-WRITE', flag(lambda: readback_v4(text, TX, rows, counts)))))
    run_plant('PLANT-WRITE', lambda: readback_v4(text, TX, rows, counts, tamper='ROW'))
    run_plant('PLANT-OCHK', lambda: readback_v4(text, TX, rows, counts, tamper='OCHK'))
    unrun = [p for p in PLANT_NAMES if p not in EXEC] + [p for p in EXEC if p not in PLANT_NAMES or EXEC.count(p) != 1]
    out('PLANTS: %d of %d must-fire plants ran (not run or repeated: %s); not firing: %s' % (
        len(set(EXEC)), len(PLANT_NAMES), ' '.join(unrun) if unrun else 'none', ' '.join(nofire) if nofire else 'none'))
    if nofire or unrun:
        fails.append('PLANTS')
    if fails:
        out('VERDICT INVALID (%s)' % ' '.join(fails))
        return 2
    recdir = OWN + '/mr/v5b' if MODE == 'cert' else os.path.join(ASM, 'dry_%s' % TAG)   # v2_5: MR_INSERT v5 (way A on the last h rows)
    if MODE == 'dry':
        os.mkdir(recdir)
    if not os.path.isdir(recdir) or os.path.realpath(recdir) not in (os.path.realpath(OWN + '/mr/v5b'), os.path.realpath(os.path.join(ASM, 'dry_%s' % TAG))):
        out('VERDICT INVALID (record folder)')
        return 2
    path = os.path.join(recdir, 'MR_INSERT.kv')
    with open(path, 'x') as fh:
        fh.write(text)
    if sha_file(path) != hashlib.sha256(text.encode()).hexdigest():
        out('VERDICT INVALID (the written MR_INSERT differs from memory)')
        return 2
    out('RECORD %s sha256 %s rows %d' % (os.path.relpath(path, W18), sha_file(path), len(rows)))
    out('RUN wall %.1f s' % (time.time() - t0))
    out('VERDICT VALID')
    return 0


PLANT_NAMES = ('PLANT-CORE', 'PLANT-PEVB-PIN', 'PLANT-RHO-PIN', 'PLANT-T048', 'PLANT-MBG-PIN', 'PLANT-GBB', 'PLANT-MU-T', 'PLANT-MU-C', 'PLANT-ORIENT N=4', 'PLANT-ORIENT N=3', 'PLANT-FACTX',
               'PLANT-ANCHOR', 'PLANT-DER', 'PLANT-IHT0', 'PLANT-HQ', 'PLANT-RB', 'PLANT-BAD', 'PLANT-WRITE', 'PLANT-OCHK',
               'PLANT-WAYA-PIN', 'PLANT-WAYA-ZERO', 'PLANT-WAYA-ORIENT',   # v2_5: way A's three
               'PLANT-MAIN-N')   # v2_6


if __name__ == '__main__':
    from flint import arb, arb_mat, ctx
    ctx.prec = 256
    try:
        rc = main()
    except Refused as e:
        out('STOP Refused: %s' % e)
        out('VERDICT INVALID (refused)')
        rc = 2
    FH.close()
    sys.exit(rc)
