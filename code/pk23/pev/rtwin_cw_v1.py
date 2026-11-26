#!/usr/bin/env python3
"""rtwin_cw_v1.py -- pk23 (code/pk23/pev/). C_w variant B (the P0_LOG row 4589; pk25's D2_DESIGN_v1_3): the FLOAT references of the
(1,1) block of |S M_c u~_x|^2 (pk23/pev/HL_CW_ENTRY_LIST_v1.json, family LC = S8's L graph with the pairs (0,2), (9,11), (1,4), (7,10)):
Cxx,1,1 = <M_h psi_1, S^2 M_h psi_1>, Cx1,1,1 and C1x,1,1 (one insertion), C11,1,1 (none), by L's RESTORED prep (the float twin m3ref_hl_v1's
P16L piece with P16-DONE), in the float twin's output format (KEYJSON a_k and bar parts B, PREPJSON, TRIAL, VERDICT); nothing here is certified.
Made by pk23's make_rtwin_cw_v1.py in the form of rtwin_hl_v1.py (512d0e61); lines 105-204 of pk22's rtwin_c3h_v1.py are copied
byte-identically (C-COPY). Checks and plants:
- C-TS-PIN: the trial file's name and sha256 equal the ones pk25/mr/v3/MR_LEMMAP.kv's TRIAL_SET line names for N; PLANT-TS-PIN (z9symxy);
- C-RESTORE: TT,0,0's a_k on the restored prep, on L's own graph (npoly base 11), against the twin piece's own TT,0,0 KEYJSON (relative
  1e-11); PLANT-RESTORE (the reference times 1 + 1e-9 must differ);
- C-RULE, C-PAIRFREE on LC's graph with PLANT-PAIRFREE (pk22's 12-vertex S4 twin P16CS4 must differ);
- C-MIRROR: Cx1,1,1 equals C1x,1,1 (a_k and bar parts, relative 1e-9) by LC's left-right reflection;
- C-T0: every key's a_0 against its exact order-0 value, relative 1e-9. At order 0, M_h psi_1 = c_h0 psi_1 + m_y u_xy + z with S z = 0, and
  S psi_1 = s_x0 psi_1, S u_xy = s_x0 s_y0 u_xy, so Cxx = s_x0^2 (c_h0^2 + m_y^2 s_y0^2), Cx1 = C1x = c_h0 s_x0^2 and C11 = s_x0^2, with the
  closed forms of the Gaussian free field of the infinite 3-row strip (N - 1 components): s_x0 = ((3 - sqrt 5)/2)^2, s_y0 = ((5 - sqrt 21)/2)^2,
  c_h0 = (N - 1) G_h / 2 with G_h = 1 - (2/3) sqrt(3/7), and m_y^2 s_y0 = (N - 1) C_h^2 / 2 with C_h = -(2/3) (1 - (5 - sqrt 21)/2)^2 / sqrt 21
  (the same forms reproduce E5's certified-twin HH,0,0 and HH,1,1 a_0, pk23/pev/out/check_t0_closed_v1.out). KC4's c_h0 (7 digits,
  relative 1e-6) and its s_x, mu_y (12 digits, relative 1e-9) are checked against the closed forms; PLANT-T0 (every prediction times 1 + 1e-6).
Each KEYJSON is followed by a KEYMEM line (the key's CPU and the peak resident memory so far).
Items: LC.<N> for N in 4, 3. Writes pk23/pev/out/rtwin_cw_v1_LC.<N>_z9sym.out (mode x).
Run (inside the core-h guard): OMP_NUM_THREADS=1 timeout <LIM + 60> nice -n 10 prlimit --as=<bytes> -- python3 -I -B
  rtwin_cw_v1.py LC.<N> <LIM>"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, time, math, hashlib, signal, traceback, re, json
import importlib.util
from fractions import Fraction

m_ = re.fullmatch(r'(LC)\.(4|3)', sys.argv[1]) if len(sys.argv) >= 3 else None
if m_ is None or not re.fullmatch(r'[0-9]{2,4}', sys.argv[2]) or not 10 <= int(sys.argv[2]) <= 3000:
    print('usage: rtwin_cw_v1.py LC.N LIM   (N = 4|3; LIM = RLIMIT_CPU soft limit in s, 10..3000)')
    sys.exit(2)
FAM, NN, LIM = m_.group(1), int(m_.group(2)), int(sys.argv[2])
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))
STAGE = ['start']
W18 = '/mnt/g2/release/root/code'
SCR = W18 + '/pk10/scripts'
INP = W18 + '/pk10/scratch'
M3D = W18 + '/pk03'
MYD = W18 + '/pk22/m3'   # read-only: rtwin_c3h_v1.py (C-COPY) and pk22's S4 twin (PLANT-PAIRFREE)
HLD = W18 + '/pk23/pev'
OUTD = HLD + '/out'   # the twin's pieces are read here, and this script writes here
TSD = W18 + '/pk11/out'
PSX = W18 + '/pk22/midrow/psixy'
MRL = W18 + '/pk25/mr/v3/MR_LEMMAP.kv'
KC4OUT = {4: W18 + '/pk22/midrow/out/out_kt_kc4_v1_2_n4.out', 3: W18 + '/pk22/midrow/out/out_kt_kc4_v1_2_n3.out'}   # C-T0's cross-checks
LISTN = 'HL_CW_ENTRY_LIST_v1.json'
SIBP = {4: 'm3ref_hl_v1_P16L.4.p5_z9sym.out', 3: 'm3ref_hl_v1_P16L.3.p5_z9sym.out'}
SIB = {'LC': ('L', 'P16L', SIBP)}
NPB = {'L': 11, 'LC': 15}   # npoly bases, the largest B with B**F < 2**63: F 18 (L, C-RESTORE), F 16 (LC)
OTHERP = {4: MYD + '/out/m3ref_px22_v1_5_P16CS4.4.p5_z9sym.out', 3: MYD + '/out/m3ref_px22_v1_5_P16CS4.3.p5_z9sym.out'}
TSFX = {4: 'ts_N4_J170_D_S_z9symxy_v1.json', 3: 'ts_N3_S_z9symxy_v1.json'}   # PLANT-TS-PIN only
RTOL = 1e-11
JREF, QCAP, DMAXH = 300.0, 6, 16
COPY_SRC = (MYD + '/rtwin_c3h_v1.py', 105, 204)
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(OUTD, '%s_%s.%d_z9sym.out' % (LABEL, FAM, NN))
if not (os.path.isdir(OUTD) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUTD)):
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
    '/mnt/g2/release/root/code/pk10/scripts/g2sw_core_snapshot.py': 'f1b51241c54e496a8de699cc3160de3281bf98c67d019f4e92459a222d3d003a',
    '/mnt/g2/release/root/code/pk10/scripts/amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc',
    '/mnt/g2/release/root/code/pk10/scripts/condexp.py': 'e0942cb478054d6be8234f6d82331ba8006bc483e4757c963db7c55581e6c91f',
    '/mnt/g2/release/root/code/pk10/scripts/lapl2.py': 'b28ffbdb86fab237564f2db9ea8b3e904481fba31ad79e39421de7b8a9dfe116',
    '/mnt/g2/release/root/code/pk10/scripts/pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
    '/mnt/g2/release/root/code/pk10/scripts/npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
    '/mnt/g2/release/root/code/pk10/scripts/riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
    '/mnt/g2/release/root/code/pk10/scripts/riglap3.py': 'e394f81567e62222240050c7cbc70c480b0804d929a8713a7b30e70ebbf1ea69',
    '/mnt/g2/release/root/code/pk10/scripts/riglap4.py': 'ed8eecd6c6ed529b9471097e205b63a9c0f1435973c498d9f1920850ec3d29d7',
    '/mnt/g2/release/root/code/pk10/scripts/riglap5.py': 'bbfbea1f5b2680eec71eee647b2c608e08f8feacf8c21fbd67f4d0ff76f037a3',
    '/mnt/g2/release/root/code/pk10/scripts/riglap5b.py': '0f9dc107d8709a78e4793db0fce23d8559fa93346d593304433162c72b5b0b93',
    '/mnt/g2/release/root/code/pk10/scripts/riglap5c.py': 'efb2f505a2d169874e2beb358ed5179901fbd6bde0791ccd578309a2a57a054e',
    '/mnt/g2/release/root/code/pk10/scripts/riglap5e.py': 'cafd025a5bb46c8b4a742ca3358d299bdea8e1b382893a9c8127ec4a1da821d9',
    '/mnt/g2/release/root/code/pk10/scripts/riglap5r.py': '7feb47f7ce840837cf04b3156e4ed94c22ec2cb3543276c0d3892c4d6a6fe749',
    '/mnt/g2/release/root/code/pk10/scripts/riglap5s.py': '44bdafd38b6a77af38af0e77ea17833fa08cdde734ecce3951795984b957e839',
    '/mnt/g2/release/root/code/pk03/m3_scal_v2.py': 'd22d3ad696074d4235f0fd31b026477e87f96f5d4b5331e29ab8d399e1e8f054',
    '/mnt/g2/release/root/code/pk03/m3_graph_v3.py': '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    '/mnt/g2/release/root/code/pk03/m3_series_v2.py': '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    '/mnt/g2/release/root/code/pk03/m3_entries_v3.py': '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    '/mnt/g2/release/root/code/pk11/out/ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    '/mnt/g2/release/root/code/pk11/out/ts_N3_S_z9sym_v1.json': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    '/mnt/g2/release/root/code/pk11/out/vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    '/mnt/g2/release/root/code/pk11/out/vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    '/mnt/g2/release/root/code/pk25/mr/v3/MR_LEMMAP.kv': '275b179f6f8e80f12101fda25989a851177c0b6003eee05f4a7095ad003fe013',
    '/mnt/g2/release/root/code/pk22/m3/rtwin_c3h_v1.py': 'cf775f629f4a51ec94a6fa0c8cb7456d0fb7115c03670ff86740f13bd39dae81',
    '/mnt/g2/release/root/code/pk22/m3/out/m3ref_px22_v1_5_P16CS4.4.p5_z9sym.out': '4a9062ac459aba26b1605d7036a738b6a7248b7a71e92b87bc46927963f18390',
    '/mnt/g2/release/root/code/pk22/m3/out/m3ref_px22_v1_5_P16CS4.3.p5_z9sym.out': 'f77f725eafa9cbbb6722ad61b978d719cfbf5a8f40bd46c5ac40ac930953b8e7',
    '/mnt/g2/release/root/code/pk23/pev/HL_CW_ENTRY_LIST_v1.json': '93b417e7d7788fbb1d229690d8f4db1460d7fc5411231e68f67254182f0de212',
    '/mnt/g2/release/root/code/pk23/pev/out/m3ref_hl_v1_P16L.4.p5_z9sym.out': '19ddb6ec632f6e5611141cc2daeb902b6ecde22bb055314d9c174a3983c994de',
    '/mnt/g2/release/root/code/pk23/pev/out/m3ref_hl_v1_P16L.3.p5_z9sym.out': 'fe622646f061c745870bd459d9423f870c70fb9ee8c5c7250f9372f4a9969668',
    '/mnt/g2/release/root/code/pk22/midrow/psixy/ts_N4_J170_D_S_z9symxy_v1.json': '909b20bfa30a4b95c2a78194e032508cde161da4f66de147fc40167b6c4ee560',
    '/mnt/g2/release/root/code/pk22/midrow/psixy/ts_N3_S_z9symxy_v1.json': 'd6b2ab93d086831e2423eed52ece6bc11abc0eeb92c31f8b8fa9368afd5f5a91',
    '/mnt/g2/release/root/code/pk22/midrow/out/out_kt_kc4_v1_2_n4.out': 'd114952faa3895db53ad97c0a5331aa337fbdf95652012cef5dc5f5ae9054985',
    '/mnt/g2/release/root/code/pk22/midrow/out/out_kt_kc4_v1_2_n3.out': 'daad669b13aaa26c4b1e07354a118704bf3bdbeff9d9d40900cdef0b1abf5f59',
# C-COPY block: rtwin_c3h_v1.py l.105-204
}
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('%s sha256 %s ITEM=%s.%d LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (LABEL, sha_file(os.path.abspath(__file__)), FAM, NN, LIM, LIM, LIM + 5))
_bad = ['%s %s' % (os.path.basename(_p), sha_file(_p)) for _p in sorted(PINS) if sha_file(_p) != PINS[_p]]
out('C-HASH %s (%d pinned files)%s' % ('PASS' if not _bad else 'FAIL', len(PINS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, SCR)
import numpy as np
import riglap5b, riglap5s, riglap4
import riglap3 as _r3
from riglap2 import Graph
from pseries import padd, pscale, pmul


def load_as(name, path):
    """a pinned pk03 module under its generic name, dependencies first (m3_run_v1_9_3's load_as)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


for _nm, _fn in (('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_entries', 'm3_entries_v3.py')):
    load_as(_nm, os.path.join(M3D, _fn))
GR, ENT = sys.modules['m3_graph'], sys.modules['m3_entries']
_pinned = set(os.path.realpath(_p) for _p in PINS)
_loaded = sorted(set(os.path.realpath(_m.__file__) for _m in list(sys.modules.values()) if getattr(_m, '__file__', None)
                     and os.path.realpath(_m.__file__).startswith((os.path.realpath(SCR) + os.sep, os.path.realpath(M3D) + os.sep))))
_unp = [os.path.basename(_p) for _p in _loaded if _p not in _pinned]
out('C-MODS %s (%d modules loaded from pk10/scripts and pk03%s)' % ('PASS' if not _unp else 'FAIL', len(_loaded),
                                                                        ', all pinned' if not _unp else '; not pinned: ' + ' '.join(_unp)))
if _unp:
    out('VERDICT INVALID (C-MODS)')
    sys.exit(2)


def gate(fails, name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


class Restored:
    """the attributes riglap5s.bound5s, riglap5c._gdata/_gnorm and riglap5e._joint read: the prep scalars from a twin PREPJSON as they
    are; Ej (riglap5b.Prep5 l.44-47) and Gc, Gp (Prep5 l.39-42, J = 300) recomputed on the graph g; ok True, so the bars are computed."""
    def __init__(self, g, pj, key):
        self.g, self.J, self.t, self.key, self.qcap, self.am0, self.ok = g, JREF, 1.0 / JREF, key, QCAP, None, True
        t = self.t
        self.a_v, self.ap = [float(a) for a in pj['a_v']], float(pj['ap'])
        if len(self.a_v) != g.V:
            raise ValueError('PREPJSON radii for %d vertices, graph has %d' % (len(self.a_v), g.V))
        rates = np.array([-math.log(1 - a) / (2 * a) * t for a in self.a_v])
        ratesp = np.array([-math.log(1 - self.ap) / (2 * self.ap) * t] * g.V)
        self.Gc, self.Nc_fresh = g.tilted(rates)
        self.Gp, self.Np_fresh = g.tilted(ratesp)
        Hs = _r3.Model3(g, 3, []).H(3)
        H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
        H1sq = pmul(H1, H1)
        self.Ej = [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
        for k in ('rE', 'nE', 'nE4', 'nC8', 'nC6', 'Nc', 'Np', 'Pout', 'Pout_p', 'farbase'):
            setattr(self, k, pj[k])
    engine = riglap5b.Prep5.engine


def fgraph(spec):
    """riglap2.Graph of a list graph: m3_graph_v3.strip of its columns (couplings by coupling_float) with the list's pairs."""
    V, E = GR.strip(spec['columns'])
    return Graph(V, dict((tuple(e), GR.coupling_float(c)) for e, c in E), [tuple(p) for p in spec['pairs']], N=NN)


def twin(fn):
    pj, kj = None, {}
    with open(os.path.join(OUTD, fn)) as fh:
        for ln in fh:
            if ln.startswith('PREPJSON '):
                pj = json.loads(ln[9:])
            elif ln.startswith('KEYJSON '):
                d = json.loads(ln[8:])
                kj[d['key']] = d
    return pj, kj


def rel_dev(ak, B, d):
    return max([abs(x - y) / max(1.0, abs(y)) for x, y in zip(ak, d['ak'])] +
               [abs(B[p] - d['B'][p]) / abs(d['B'][p]) for p in ('rem', 'tail', 'ann', 'far') if d['B'][p] > 0])


# C-COPY end


def check_copy():
    with open(os.path.abspath(__file__), 'rb') as fh:
        own = fh.read().split(b'\n')
    with open(COPY_SRC[0], 'rb') as fh:
        src = fh.read().split(b'\n')
    i0 = own.index(b'# C-COPY block: rtwin_c3h_v1.py l.105-204')
    i1 = own.index(b'# C-COPY end')
    return own[i0 + 1:i1] == src[COPY_SRC[1] - 1:COPY_SRC[2]]


def split_groups(factors):
    """m3_bar_v11.split_groups (kt_s9b_v3_2's): one group per factor, consts folded into the scalar."""
    scal = 1.0
    groups = []
    for f in factors:
        if f[0] == 'const':
            scal *= f[1]
        else:
            groups.append([f])
    return scal, groups


def bound(pr, facs, grouping):
    """riglap5s.bound5s, with riglap5s.group_factors swapped for split_groups during the call when grouping is 'split'."""
    if grouping == 'std':
        return riglap5s.bound5s(pr, facs)
    orig = riglap5s.group_factors
    riglap5s.group_factors = split_groups
    try:
        return riglap5s.bound5s(pr, facs)
    finally:
        riglap5s.group_factors = orig


def peak_mib():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024


def t0_values(n):
    """the exact order-0 values of the (1,1) block (closed forms of the infinite 3-row strip's Gaussian free field, N - 1 components)."""
    lam1, lam2 = (3 - math.sqrt(5)) / 2, (5 - math.sqrt(21)) / 2
    sx0, sy0 = lam1 * lam1, lam2 * lam2
    gh = 1 - 2 * math.sqrt(3.0 / 7) / 3
    ch0 = (n - 1) * gh / 2
    chh = -(2.0 / 3) * (1 - lam2) ** 2 / math.sqrt(21)
    my2sy0 = (n - 1) * chh * chh / 2   # m_y^2 s_y0
    return {'Cxx,1,1': sx0 * sx0 * (ch0 * ch0 + my2sy0 * sy0), 'Cx1,1,1': ch0 * sx0 * sx0, 'C1x,1,1': ch0 * sx0 * sx0, 'C11,1,1': sx0 * sx0}, \
        (sx0, sy0, ch0, my2sy0)


def run(fails, nofire):
    ok_copy = check_copy()
    out('C-COPY %s (rtwin_c3h_v1.py l.%d-%d byte-identical)' % (gate(fails, 'C-COPY', ok_copy), COPY_SRC[1], COPY_SRC[2]))
    LK = json.load(open(os.path.join(HLD, LISTN)))
    tsp = os.path.join(TSD, TSF[NN])
    TS = ENT.load_trial(tsp, os.path.join(TSD, 'vacres_K3_N%d_sym_v1.json' % NN), 0.0)
    mm = re.search(r'^TRIAL_SET = N4 (\S+):([0-9a-f]{64}), N3 (\S+):([0-9a-f]{64})', open(MRL).read(), re.M)
    want = ({4: (mm.group(1), mm.group(2)), 3: (mm.group(3), mm.group(4))}[NN]) if mm else ('-', '-')
    have = (TSF[NN], sha_file(tsp))
    out('C-TS-PIN N=%d: trial file %s sha256 %s against MR_LEMMAP.kv\'s TRIAL_SET %s:%s -> %s' % (
        NN, have[0], have[1], want[0], want[1], gate(fails, 'C-TS-PIN', have == want)))
    fx = (TSFX[NN], sha_file(os.path.join(PSX, TSFX[NN])))
    out('PLANT-TS-PIN N=%d: the z9symxy file %s (sha256 %s) against the same line -> %s' % (NN, fx[0], fx[1], 'FIRES' if fx != want else 'DOES NOT FIRE'))
    if fx == want:
        nofire.append('PLANT-TS-PIN')
    sfam, sname, sfn = SIB[FAM]
    pj, kj = twin(sfn[NN])
    out('SIBLING %s N=%d: %s (sha256 %s), PREPJSON family %s N %s J %s; %d KEYJSON lines' % (
        FAM, NN, sfn[NN], sha_file(os.path.join(OUTD, sfn[NN])), pj['family'], pj['N'], pj['J'], len(kj)))
    if not (pj['family'] == sname and pj['N'] == NN and pj['J'] == JREF):
        raise ValueError('sibling PREPJSON is not %s at N = %d, J = 300' % (sname, NN))
    STAGE[0] = 'restore on L'
    riglap5b.NPOLY_B = NPB['L']
    gL = fgraph(LK['graphs']['L'])
    prL = Restored(gL, pj, 'rkL%d' % NN)
    cols = ((0, 1, 2), (9, 10, 11))
    akr, _ = riglap5s.bound5s(prL, [TS.cp(0, cols[0]), TS.cp(0, cols[1])])
    ref = kj['TT,0,0']['ak']
    worst = max(abs(x - y) / max(1.0, abs(y)) for x, y in zip(akr, ref))
    out('C-RESTORE %s N=%d: the restored prep\'s a_k of TT,0,0 on L\'s graph against the twin piece\'s own TT,0,0 KEYJSON: largest relative '
        'difference %.2e (tolerance %.0e) -> %s' % (FAM, NN, worst, RTOL, gate(fails, 'C-RESTORE', worst <= RTOL)))
    refp = [x * (1 + 1e-9) for x in ref]
    dvp = max(abs(x - y) / max(1.0, abs(y)) for x, y in zip(akr, refp))
    out('PLANT-RESTORE %s N=%d: the reference a_k times 1 + 1e-9: largest relative difference %.2e -> %s' % (
        FAM, NN, dvp, 'FIRES' if dvp > 1e-12 else 'DOES NOT FIRE'))
    if not dvp > 1e-12:
        nofire.append('PLANT-RESTORE')
    STAGE[0] = 'family %s' % FAM
    riglap5b.NPOLY_B = NPB[FAM]
    g = fgraph(LK['graphs'][FAM])
    pr = Restored(g, pj, 'rk%s%d' % (FAM, NN))
    wantr = [min(80.0 * g.G[v, v] / JREF, 0.6) for v in range(g.V)]
    drule = max(abs(w - a) / a for w, a in zip(wantr, pj['a_v'])) if len(wantr) == len(pj['a_v']) else float('inf')
    out('C-RULE %s N=%d: the radii^2 min(80 G_vv/300, 0.6) of %s\'s graph (V %d, F %d) against the PREPJSON a_v: largest relative difference %.2e -> %s' % (
        FAM, NN, FAM, g.V, g.F, drule, gate(fails, 'C-RULE', drule <= 1e-14)))
    nE1 = riglap4.norm_any(pr.Ej[1], g.G, g.n, g.W, 2, 'pf%s%d|H' % (FAM, NN), DMAXH)
    dpf = max(abs(pr.Nc_fresh / pj['Nc'] - 1), abs(pr.Np_fresh / pj['Np'] - 1), abs(nE1 / pj['nE'][1] - 1))
    out('C-PAIRFREE %s N=%d: on %s\'s graph (pairs %s) fresh Nc %.15f, Np %.15f, nE[1] %.15f against the PREPJSON %.15f, %.15f, %.15f: largest '
        'relative difference %.2e -> %s' % (FAM, NN, FAM, [tuple(p) for p in LK['graphs'][FAM]['pairs']], pr.Nc_fresh, pr.Np_fresh, nE1, pj['Nc'],
                                           pj['Np'], pj['nE'][1], dpf, gate(fails, 'C-PAIRFREE', dpf <= 1e-12)))
    pjo, _ = twin(OTHERP[NN])
    dpo = abs(pr.Nc_fresh / pjo['Nc'] - 1)
    out('PLANT-PAIRFREE %s N=%d: fresh Nc against pk22\'s S4 twin %s PREPJSON Nc %.15f: relative difference %.2e -> %s' % (
        FAM, NN, os.path.basename(OTHERP[NN]), pjo['Nc'], dpo, 'FIRES' if dpo > 1e-12 else 'DOES NOT FIRE'))
    if not dpo > 1e-12:
        nofire.append('PLANT-PAIRFREE')
    keys, res = [], {}
    for i, e in enumerate([e for e in LK['entries'] if e['graph'] == FAM]):
        STAGE[0] = 'key %s' % e['key']
        if cpu() > LIM - 30:
            raise RuntimeError('CPU budget: %.1f s used of %d before key %s' % (cpu(), LIM, e['key']))
        facs = [ENT.factor(TS, 'N', enc) for enc in e['factors']]
        t1 = cpu()
        ak, B = bound(pr, facs, e['grouping'])
        d = {'family': 'P16' + FAM, 'N': NN, 'J': JREF, 'key': e['key'], 'index': i, 'grouping': e['grouping'], 'ak': [float(x) for x in ak],
             'B': dict((p, float(B[p])) for p in ('rem', 'tail', 'ann', 'far')), 'err': float(sum(B.values())), 'cpu': round(cpu() - t1, 2),
             'refs': [], 'restored_from': '%s:%s' % (sfn[NN], sha_file(os.path.join(OUTD, sfn[NN])))}
        res[e['key']] = d
        keys.append(e['key'])
        out('KEYJSON ' + json.dumps(d))
        out('KEYMEM %s N=%d: %d factors, cpu %.2f s, peak resident memory so far %d MiB' % (e['key'], NN, len(facs), d['cpu'], peak_mib()))
    STAGE[0] = 'mirror'
    dm = rel_dev(res['C1x,1,1']['ak'], res['C1x,1,1']['B'], res['Cx1,1,1'])
    out('C-MIRROR LC N=%d: C1x,1,1 (xi on (7,10)) against Cx1,1,1 (xi on (1,4)), a_k and bar parts: largest relative difference %.2e -> %s' % (
        NN, dm, gate(fails, 'C-MIRROR', dm <= 1e-9)))
    STAGE[0] = 't0 %s' % FAM
    pred, (sx0, sy0, ch0, my2sy0) = t0_values(NN)
    ktxt = open(KC4OUT[NN]).read()
    m1 = re.search(r'^V1 IDENT N=%d: .*?eta = v_h ([-+0-9.eE]+) ' % NN, ktxt, re.M)
    m2 = re.search(r'^KC4 V1 RITZ N=%d: s_x ([0-9.]+) \+ t [-0-9.]+; mu_y ([0-9.]+) \+ t' % NN, ktxt, re.M)
    kch0 = float(m1.group(1)) if m1 else float('nan')
    ksx, ksy = (float(m2.group(1)), float(m2.group(2))) if m2 else (float('nan'), float('nan'))
    dk = [abs(ch0 / kch0 - 1), abs(sx0 / ksx - 1), abs(sy0 / ksy - 1)]
    d0 = [(k, res[k]['ak'][0], pred[k], abs(res[k]['ak'][0] / pred[k] - 1)) for k in keys]
    ok_t0 = len(d0) == 4 and all(x[3] <= 1e-9 for x in d0) and dk[0] <= 1e-6 and dk[1] <= 1e-9 and dk[2] <= 1e-9
    out('C-T0 %s N=%d: order-0 values (s_x0 %.15f, s_y0 %.15f, c_h0 %.15f, m_y^2 s_y0 %.15e): %s (tolerance 1e-9); KC4 %s: c_h0 %.7f '
        '(relative %.2e, tolerance 1e-6), s_x %.12f (relative %.2e), mu_y %.12f (relative %.2e, tolerance 1e-9) -> %s' % (
            FAM, NN, sx0, sy0, ch0, my2sy0, '; '.join('%s a_0 %.15f against %.15f (relative %.2e)' % x for x in d0),
            os.path.basename(KC4OUT[NN]), kch0, dk[0], ksx, dk[1], ksy, dk[2], gate(fails, 'C-T0', ok_t0)))
    dq = max(abs(res[k]['ak'][0] / (pred[k] * (1 + 1e-6)) - 1) for k in keys)
    out('PLANT-T0 %s N=%d: every prediction times 1 + 1e-6: largest relative difference %.2e -> %s' % (
        FAM, NN, dq, 'FIRES' if not dq <= 1e-9 else 'DOES NOT FIRE'))
    if dq <= 1e-9:
        nofire.append('PLANT-T0')
    pjn = dict(pj)
    pjn['family'] = 'P16' + FAM
    pjn['restored_from'] = '%s:%s' % (sfn[NN], sha_file(os.path.join(OUTD, sfn[NN])))
    out('PREPJSON ' + json.dumps(pjn))
    out('KEYS %s N=%d: %d keys %s' % (FAM, NN, len(keys), ' '.join(keys)))


def main():
    fails, nofire = [], []
    try:
        run(fails, nofire)
        complete = True
    except Exception as e:
        out(traceback.format_exc().rstrip())
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        complete = False
    out('TRIAL z9sym')
    out('ITEM %s.%d cpu %.1f s, peak resident memory %d MiB' % (FAM, NN, cpu(), peak_mib()))
    why = fails + ['%s did not fire' % x for x in nofire] + ([] if complete else ['ERROR'])
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))
    return 0 if not why else 1


if __name__ == '__main__':
    sys.exit(main())
