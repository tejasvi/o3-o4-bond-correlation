import sys
import time
import math
import hashlib
import resource
import importlib.util
import numpy as np

DIR = '/mnt/g2/release/root/code/pk05/'
CORE, CSHA = DIR + 'cs33b_rh_core.py', '82b7cfdd3d1eaf0a095b46231a0a0e1851ade2b0e3796d04be24ba4642163436'
PROBE, PSHA = DIR + 'cs30_ks1_probe.py', '2dbd9a3e7a2820055450ec90228c93830d3cc390bda03134dc6706914bb5288c'
T0 = time.process_time()
ITEM, CAP_S = sys.argv[1], float(sys.argv[2])
KDEG = int(sys.argv[3]) if len(sys.argv) > 3 else 3
if KDEG not in (3, 4):
    raise SystemExit('K must be 3 or 4')


def _load(path, sha, name):
    with open(path, 'rb') as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != sha:
        print('SHA MISMATCH %s %s' % (path, got), flush=True)
        sys.exit(2)
    spec_ = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)
    return mod


C = _load(CORE, CSHA, 'cs33b_rh_core_mod')
E, MR, TM, arb, U, ETA, up, gam, SQ2, FV = C.E, C.MR, C.TM, C.arb, C.U, C.ETA, C.up, C.gam, C.SQ2, C.FV
dn, amin, amax = C.dn, C.amin, C.amax
NMODE, NCERT, K_S, K_F, P_EX, K_EX, NSUB, K_MAX = 8, 6, KDEG, KDEG, 6, 2, 16, 60
PE = {'th': P_EX, 'mh': P_EX + 3, 'bh': P_EX, 'tv': P_EX, 'bv': P_EX}       # v1_4: mh objects to p < 9, INF mh from p = 9
P_MAX = max(PE.values())
TYPES, HORIZ, VERT = ('th', 'mh', 'bh', 'tv', 'bv'), ('th', 'mh', 'bh'), ('tv', 'bv')
QGATE, NODEGATE = 1e-9, 1e-12
