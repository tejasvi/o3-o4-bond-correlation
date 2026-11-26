#!/usr/bin/env python3
"""kt_nu_g_v1_2.py -- pk24 (code/pk24/nu/). The certified nu_g of pk24/NU_G_NOTE_v1.md (sect. 4) for the delta bridge (sect. 3) of P2 v2_1,
P4 and item (3):
    nu_g >= ||(B_g(t) - b0_g) 1_near||_t / t   for every 0 < t <= T1 = 1/300,
in engine A's near norm ||F||_t = (n1(t) E_G1(t)[F^2])^1/2, where G1, n1 = tilted_cov_a(LD, BD, [c_m t] * 6) and the Wishart is on column 1
(kt_cert_v1_9, the norm of nP). Here B_g(t) = E0 pS_g(xi; t) is the state's exact chart function, b0_g = pS_g(Q/2; 0), and the near region is
t X_v <= a_m at every vertex.
Method: the majorant M_g = ebar Pbar_g + Dbar'_g of the note's sect. 4, with a = max(a_m, a_e), wbar = 1/(4 (1 - a)) and
xibar_p = Q_p/2 + T1 wbar d_p/2. Then nu_g = (n1(T1) E_G1(T1)[M_g^2])^1/2, an exact Wishart moment in arb (WishartA of arbeng_c2b_v2).
Built by tools/make_kt_nu_g_v1_2.py from nu/src/nu_head_v1_2.py, the verbatim ast source segments of engine A's functions and statements, and
nu/src/nu_main_v1_2.py (v1_1: kt_nu_g_v1.py's dry run stopped because nn was unset before the tilt; run_N now calls setup(N, 0) first).
C-CORE re-checks every copied segment against the pinned kt_cert_v1_9.py.
v1_2 (the row 4659 approval; pk25's NU reader form), changes and nothing else:
  (1) C-TRI: |E0 - 1| <= t ebar needs TRI_p >= 0 (E0 = exp(-t sum_p TRI_p Delta_p) with Delta_p >= 0 has a nonpositive exponent only then);
      the gate requires every TRI_p certainly > 0, else the run is INVALID;
  (2) states psi, e1, e2 and e3 at N = 3 and 4 only (states 10 and 10' only if pk22 asks); the z9symxy and z9symxyp files are no longer
      read or pinned;
  (3) the record in the form of pk25's NU reader: FORMAT, RECORD, PRODUCER, CODE (path:sha256), STATUS, RUN_VERDICT, TRIAL_SET (verbatim
      from the pinned MR_LEMMAP v3, pk25/mr/v3/MR_LEMMAP.kv), J_LO_CHECK = 300 (the bound covers every t in (0, 1/300]), CLAIM, and per N
      the lines N<N>_NU = nu_psi nu_e1 nu_e3 and N<N>_NU_E2 = nu_e2 (17-digit decimals rounded up).
Model: python-flint arb at 512 bits (engine A's precision). nu/arbeng_c2b_v2.py is an unchanged copy (C-HASH: its sha256 equals pk02's).
The far part and the cutoff: by the note's sect. 3 they enter through far_out at |m_g(t)| + |delta_g| in P2's assembly. Nothing here.
Gates: C-HASH, C-CORE, C-ID with PLANT-ID, C-MAJ with PLANT-MAJ, C-MONO; the record says RUN_VERDICT = VALID only if every gate passed and
every plant fired.
Usage: kt_nu_g_v1_2.py MODE OUT   (MODE dry or record; OUT a new file under pk24/nu/). No run without its job script."""
import sys, os, math, json, hashlib, ast, time

W18 = '/mnt/g2/release/root/code'
NUDIR = W18 + '/pk24/nu'
T0 = time.process_time()


def out(line):
    print(line, flush=True)


def sha_file(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


if len(sys.argv) != 3 or sys.argv[1] not in ('dry', 'record'):
    out('usage: kt_nu_g_v1_2.py MODE OUT  (MODE dry or record)')
    sys.exit(2)
MODE, OUTP = sys.argv[1], os.path.abspath(sys.argv[2])
if not (OUTP.startswith(NUDIR + '/') and not os.path.exists(OUTP)):
    out('OUT must be a new file under %s' % NUDIR)
    sys.exit(2)
KT = 'pk02/kt_cert_v1_9.py'
PIN8 = {KT: '6305ef1b', 'pk02/arbeng_c2b_v2.py': '12c839a6', 'pk24/nu/arbeng_c2b_v2.py': '12c839a6',
        'pk11/out/ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1b', 'pk11/out/ts_N3_S_z9sym_v1.json': 'a298db65',
        'pk11/out/vacres_K3_N4_sym_v1.json': 'b40859de', 'pk11/out/vacres_K3_N3_sym_v1.json': 'e5a9b49f',
        'pk25/mr/v3/MR_LEMMAP.kv': '275b179f', 'pk24/NU_G_NOTE_v1.md': '0c05f650',
        'rv02/REVIEW_NU_G_NOTE_V1_rv02.md': '41cff4bb'}
SHAS = dict((p, sha_file(os.path.join(W18, p))) for p in PIN8)
SELF_SHA = sha_file(os.path.abspath(__file__))
out('kt_nu_g_v1_2 sha256 %s MODE=%s OUT=%s' % (SELF_SHA, MODE, OUTP.replace(W18 + '/', '')))
_bad = ['%s %s (pinned %s)' % (p, SHAS[p][:8], PIN8[p]) for p in PIN8 if not SHAS[p].startswith(PIN8[p])]
out('C-HASH %s (%d inputs; the arb layer copy equals pk02\'s: %s)%s' % ('PASS' if not _bad else 'FAIL', len(PIN8),
    'yes' if SHAS['pk24/nu/arbeng_c2b_v2.py'] == SHAS['pk02/arbeng_c2b_v2.py'] else 'NO', (': ' + '; '.join(_bad)) if _bad else ''))
if _bad or SHAS['pk24/nu/arbeng_c2b_v2.py'] != SHAS['pk02/arbeng_c2b_v2.py']:
    out('RUN_VERDICT INVALID (C-HASH)')
    sys.exit(3)
sys.path.insert(0, NUDIR)
import numpy as np
import flint
from flint import arb, arb_mat, ctx
ctx.prec = 512
import arbeng_c2b_v2 as ae
out('ENV: python-flint %s, numpy %s, python %s, ctx.prec %d' % (flint.__version__, np.__version__, sys.version.split()[0], ctx.prec))
TILT_LOG = []
nn = None                      # set per N by setup(); tilted_cov_a reads it
Smat = None                    # set per N and state source by setup()
QV = None
