#!/usr/bin/env python3
"""make_rtwin_hl_v1.py (pk23, option B Pev entries; the P0_LOG rows 4409, 4422, 4435; pk22's handover 13d4039c): writes
pk23/pev/rtwin_hl_v1.py, the float references of the L-graph keys on L's RESTORED prep, on the pattern of pk22's rtwin_e5_v1.py
(aa996e16). The file is assembled from three parts: this maker's head (docstring, items, paths, the sibling twin pieces), a PINS dict
whose sha256 values this maker reads from the files now (with asserted prefixes for the trial files, the vacres files, pk25's
MR_LEMMAP.kv, pk22's rtwin_c3h_v1.py and the twin pieces), the C-COPY block (pk22's rtwin_c3h_v1.py l.105-204, copied
byte-identically, as rtwin_e5_v1 does), and this maker's tail (rtwin_e5_v1's check_copy, split_groups and bound, then a new run() and
main()). Usage: make_rtwin_hl_v1.py PIECE_N4 PIECE_N3 (the twin pieces with P16-DONE, file names in pk23/pev/out). Prints the shas."""
import hashlib, os, re, sys
W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
DST = HLD + '/rtwin_hl_v1.py'
C3H = W18 + '/pk22/m3/rtwin_c3h_v1.py'
E5 = W18 + '/pk22/m3/rtwin_e5_v1.py'


def sha_path(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


assert len(sys.argv) == 3, 'usage: make_rtwin_hl_v1.py PIECE_N4 PIECE_N3'
P4, P3 = sys.argv[1], sys.argv[2]
assert re.fullmatch(r'm3ref_hl_v1_P16L\.4\.p[1-9]_z9sym\.out', P4) and re.fullmatch(r'm3ref_hl_v1_P16L\.3\.p[1-9]_z9sym\.out', P3), (P4, P3)
for p in (P4, P3):
    txt = open(os.path.join(HLD, 'out', p)).read()
    n = p.split('.')[1]
    k = p.split('.')[2][1:].split('_')[0]
    assert ('P16-DONE piece %s of P16L N=%s' % (k, n)) in txt and 'VERDICT VALID' in txt and 'PREPJSON ' in txt, p
assert os.path.dirname(os.path.abspath(DST)) == HLD and not os.path.exists(DST), DST
c3h_lines = open(C3H, 'rb').read().split(b'\n')
assert sha_path(C3H).startswith('cf775f62'), sha_path(C3H)
assert sha_path(E5).startswith('aa996e16'), sha_path(E5)
block = c3h_lines[104:204]
assert block[0] == b'}' and block[1].startswith(b'TSF = {4:') and len(block) == 100, block[:2]

PIN_PATHS = [W18 + '/pk10/scripts/' + f for f in (
    'g2sw_core_snapshot.py', 'amom2b.py', 'condexp.py', 'lapl2.py', 'pseries.py', 'npoly.py', 'riglap2.py', 'riglap3.py', 'riglap4.py',
    'riglap5.py', 'riglap5b.py', 'riglap5c.py', 'riglap5e.py', 'riglap5r.py', 'riglap5s.py')]
PIN_PATHS += [W18 + '/pk03/' + f for f in ('m3_scal_v2.py', 'm3_graph_v3.py', 'm3_series_v2.py', 'm3_entries_v3.py')]
PREFIX = {
    W18 + '/pk11/out/ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1b', W18 + '/pk11/out/ts_N3_S_z9sym_v1.json': 'a298db65',
    W18 + '/pk11/out/vacres_K3_N4_sym_v1.json': 'b40859de', W18 + '/pk11/out/vacres_K3_N3_sym_v1.json': 'e5a9b49f',
    W18 + '/pk25/mr/v3/MR_LEMMAP.kv': '275b179f', C3H: 'cf775f62',
    W18 + '/pk22/m3/out/m3ref_px22_v1_5_P16CS4.4.p5_z9sym.out': '4a9062ac', W18 + '/pk22/m3/out/m3ref_px22_v1_5_P16CS4.3.p5_z9sym.out': 'f77f725e',
    HLD + '/HL_ENTRY_LIST_v1.json': '2d115b6d', HLD + '/out/' + P4: '', HLD + '/out/' + P3: '',
    W18 + '/pk22/midrow/psixy/ts_N4_J170_D_S_z9symxy_v1.json': '909b20bf', W18 + '/pk22/midrow/psixy/ts_N3_S_z9symxy_v1.json': 'd6b2ab93',
    W18 + '/pk22/midrow/out/out_kt_kc4_v1_2_n4.out': 'd114952f', W18 + '/pk22/midrow/out/out_kt_kc4_v1_2_n3.out': 'daad669b',
}
pins = []
for p in PIN_PATHS + list(PREFIX):
    h = sha_path(p)
    assert h.startswith(PREFIX.get(p, '')), (p, h)
    pins.append("    %r: %r," % (p, h))
    print('PIN %s %s' % (h, p))

HEAD = r'''#!/usr/bin/env python3
"""rtwin_hl_v1.py -- pk23 (code/pk23/pev/). Option B Pev entries (the P0_LOG rows 4409, 4422, 4435): the FLOAT references of
<psi_0, T M_e^k T psi_0> / lambda_0^2 (pk23/pev/HL_ENTRY_LIST_v1.json: family L, S8's L graph with TT,0,0; family LH, L plus h on (4,7); family LT, L plus t on
(3,6); family LB, L plus (5,8), t's top-bottom mirror, a float control only) by L's RESTORED prep (the float twin m3ref_hl_v1's P16L piece
with P16-DONE), in the float twin's output format (KEYJSON a_k and bar parts B, PREPJSON, TRIAL, VERDICT); nothing here is certified.
Made by pk23's make_rtwin_hl_v1.py on the pattern of pk22's rtwin_e5_v1.py (aa996e16); lines 105-204 of pk22's rtwin_c3h_v1.py
are copied byte-identically (C-COPY). Checks and plants:
- C-TS-PIN: the trial file's name and sha256 equal the ones pk25/mr/v3/MR_LEMMAP.kv's TRIAL_SET line names for N (the row 4435);
  PLANT-TS-PIN: the z9symxy file of the same N must not match;
- C-RESTORE: TT,0,0's a_k on the restored prep against the twin piece's own TT,0,0 KEYJSON (relative 1e-11); PLANT-RESTORE (the
  reference times 1 + 1e-9 must differ);
- C-RULE, C-PAIRFREE with PLANT-PAIRFREE (fresh Nc against pk22's 12-vertex S4 twin P16CS4, which must differ), as rtwin_e5_v1;
- C-REPEAT (LH, LT): the k = 2 key's factors hold the k = 1 key's xia factor twice, and the two keys' a_0 differ;
- C-MIRROR (LB): Mb,0,0 equals LT's Mt,0,0 (a_k and bar parts, relative 1e-9; LT's output read here) by the top-bottom reflection;
- C-T0: every key's a_0 against its exact order-0 value, relative 1e-9. At order 0 the field is the Gaussian free field of the infinite
  3-row strip with N - 1 components, so <xi_e> = (N - 1) G_e / 2 and <xi_e^2> = (N^2 - 1) G_e^2 / 4, where G_e is the effective
  resistance of the edge: G_h = 1 - (2/3) sqrt(3/7) (middle row), G_t = 1 - sqrt(1/5)/2 - sqrt(3/7)/6 (top or bottom row); TT is 1.
  The h value (N - 1) G_h / 2 is also checked against KC4's c_h0 (pk22/midrow/out/out_kt_kc4_v1_2_n<N>.out, 7 digits, relative
  1e-6), the constant rtwin_e5_v1's C-T0 reads; PLANT-T0 (every prediction times 1 + 1e-6) must fail.
Each KEYJSON is followed by a KEYMEM line (the key's CPU and the peak resident memory so far).
Items: L.<N>, LH.<N>, LT.<N>, LB.<N> for N in 4, 3 (LB after LT). Writes pk23/pev/out/rtwin_hl_v1_<FAM>.<N>_z9sym.out (mode x).
Run (inside the core-h guard): OMP_NUM_THREADS=1 timeout <LIM + 60> nice -n 10 prlimit --as=<bytes> -- python3 -I -B
  rtwin_hl_v1.py <FAM>.<N> <LIM>"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, time, math, hashlib, signal, traceback, re, json
import importlib.util
from fractions import Fraction

m_ = re.fullmatch(r'(L|LH|LT|LB)\.(4|3)', sys.argv[1]) if len(sys.argv) >= 3 else None
if m_ is None or not re.fullmatch(r'[0-9]{2,4}', sys.argv[2]) or not 10 <= int(sys.argv[2]) <= 3000:
    print('usage: rtwin_hl_v1.py L|LH|LT|LB.N LIM   (N = 4|3; LIM = RLIMIT_CPU soft limit in s, 10..3000)')
    sys.exit(2)
FAM, NN, LIM = m_.group(1), int(m_.group(2)), int(sys.argv[2])
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))
STAGE = ['start']
CODEDIR = '/mnt/g2/release/root/code'
SCR = CODEDIR + '/pk10/scripts'
INP = CODEDIR + '/pk10/scratch'
M3D = CODEDIR + '/pk03'
MYD = CODEDIR + '/pk22/m3'   # read-only: rtwin_c3h_v1.py (C-COPY) and pk22's S4 twin (PLANT-PAIRFREE)
HLD = CODEDIR + '/pk23/pev'
OUTD = HLD + '/out'   # the twin's pieces are read here, and this script writes here
TSD = CODEDIR + '/pk11/out'
PSX = CODEDIR + '/pk22/midrow/psixy'
MRL = CODEDIR + '/pk25/mr/v3/MR_LEMMAP.kv'
KC4OUT = {4: CODEDIR + '/pk22/midrow/out/out_kt_kc4_v1_2_n4.out', 3: CODEDIR + '/pk22/midrow/out/out_kt_kc4_v1_2_n3.out'}   # C-T0's c_h0
SIBP = {4: '@@P4@@', 3: '@@P3@@'}
SIB = dict((f, ('L', 'P16L', SIBP)) for f in ('L', 'LH', 'LT', 'LB'))
NPB = {'L': 11, 'LH': 9, 'LT': 9, 'LB': 9}   # npoly bases, the largest B with B**F < 2**63: F 18 (L), F 19 (L's pairs plus one)
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
'''

TAIL = r'''

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


def run(fails, nofire):
    ok_copy = check_copy()
    out('C-COPY %s (rtwin_c3h_v1.py l.%d-%d byte-identical)' % (gate(fails, 'C-COPY', ok_copy), COPY_SRC[1], COPY_SRC[2]))
    LK = json.load(open(os.path.join(HLD, 'HL_ENTRY_LIST_v1.json')))
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
    riglap5b.NPOLY_B = NPB[FAM]
    g = fgraph(LK['graphs'][FAM])
    pr = Restored(g, pj, 'rk%s%d' % (FAM, NN))
    STAGE[0] = 'restore %s' % FAM
    cols = ((0, 1, 2), (9, 10, 11))
    akr, _ = riglap5s.bound5s(pr, [TS.cp(0, cols[0]), TS.cp(0, cols[1])])
    ref = kj['TT,0,0']['ak']
    worst = max(abs(x - y) / max(1.0, abs(y)) for x, y in zip(akr, ref))
    out('C-RESTORE %s N=%d: the restored prep\'s a_k of TT,0,0 on %s\'s graph against the twin piece\'s own TT,0,0 KEYJSON: largest relative '
        'difference %.2e (tolerance %.0e) -> %s' % (FAM, NN, FAM, worst, RTOL, gate(fails, 'C-RESTORE', worst <= RTOL)))
    refp = [x * (1 + 1e-9) for x in ref]
    dvp = max(abs(x - y) / max(1.0, abs(y)) for x, y in zip(akr, refp))
    out('PLANT-RESTORE %s N=%d: the reference a_k times 1 + 1e-9: largest relative difference %.2e -> %s' % (
        FAM, NN, dvp, 'FIRES' if dvp > 1e-12 else 'DOES NOT FIRE'))
    if not dvp > 1e-12:
        nofire.append('PLANT-RESTORE')
    STAGE[0] = 'family %s' % FAM
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
    keys, res, ents = [], {}, {}
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
        ents[e['key']] = e
        keys.append(e['key'])
        out('KEYJSON ' + json.dumps(d))
        out('KEYMEM %s N=%d: %d factors, cpu %.2f s, peak resident memory so far %d MiB' % (e['key'], NN, len(facs), d['cpu'], peak_mib()))
    if FAM in ('LH', 'LT'):
        k1, k2 = {'LH': ('Mh,0,0', 'Mhh,0,0'), 'LT': ('Mt,0,0', 'Mtt,0,0')}[FAM]
        x1 = [f for f in ents[k1]['factors'] if f[0] == 'xia']
        x2 = [f for f in ents[k2]['factors'] if f[0] == 'xia']
        same = len(x1) == 1 and x2 == x1 + x1
        da0 = abs(res[k2]['ak'][0] - res[k1]['ak'][0]) / max(abs(res[k1]['ak'][0]), 1e-300)
        out('C-REPEAT %s N=%d: %s holds %s\'s xia factor %s twice: %s; a_0 %.12g against %.12g (relative difference %.2e, must exceed 1e-6) -> %s' % (
            FAM, NN, k2, k1, x1, same, res[k2]['ak'][0], res[k1]['ak'][0], da0, gate(fails, 'C-REPEAT', same and da0 > 1e-6)))
    STAGE[0] = 't0 %s' % FAM
    mm = re.search(r'^V1 IDENT N=%d: .*?eta = v_h ([-+0-9.eE]+) ' % NN, open(KC4OUT[NN]).read(), re.M)
    ch0 = float(mm.group(1)) if mm else float('nan')
    gh = 1 - 2 * math.sqrt(3.0 / 7) / 3
    gt = 1 - math.sqrt(0.2) / 2 - math.sqrt(3.0 / 7) / 6

    def t0_pred(gh_, gt_):
        ch, ct = (NN - 1) * gh_ / 2, (NN - 1) * gt_ / 2
        return {'TT,0,0': 1.0, 'TTh,0,0': 1.0, 'Mh,0,0': ch, 'Mhh,0,0': ch * ch * (NN + 1) / (NN - 1),
                'Mt,0,0': ct, 'Mtt,0,0': ct * ct * (NN + 1) / (NN - 1), 'Mb,0,0': ct}
    pred = t0_pred(gh, gt)
    d0 = [(k, res[k]['ak'][0], pred[k], abs(res[k]['ak'][0] / pred[k] - 1)) for k in keys]
    dkc = abs(pred['Mh,0,0'] / ch0 - 1)
    ok_t0 = len(d0) > 0 and all(x[3] <= 1e-9 for x in d0) and dkc <= 1e-6
    out('C-T0 %s N=%d: order-0 values (Gaussian free field of the infinite 3-row strip, N - 1 components: <xi_e> = (N - 1) G_e / 2, '
        '<xi_e^2> = (N^2 - 1) G_e^2 / 4; G_h = 1 - (2/3) sqrt(3/7) = %.15f, G_t = 1 - sqrt(1/5)/2 - sqrt(3/7)/6 = %.15f; TT 1): %s '
        '(tolerance 1e-9); (N - 1) G_h / 2 = %.12f against KC4 %s c_h0 %.7f (relative %.2e, tolerance 1e-6) -> %s' % (
            FAM, NN, gh, gt, '; '.join('%s a_0 %.12f against %.12f (relative %.2e)' % x for x in d0), pred['Mh,0,0'],
            os.path.basename(KC4OUT[NN]), ch0, dkc, gate(fails, 'C-T0', ok_t0)))
    dq = max(abs(res[k]['ak'][0] / (pred[k] * (1 + 1e-6)) - 1) for k in keys)
    out('PLANT-T0 %s N=%d: every prediction times 1 + 1e-6: largest relative difference %.2e -> %s' % (
        FAM, NN, dq, 'FIRES' if not dq <= 1e-9 else 'DOES NOT FIRE'))
    if dq <= 1e-9:
        nofire.append('PLANT-T0')
    if FAM == 'LB':
        STAGE[0] = 'mirror'
        lt = os.path.join(OUTD, '%s_LT.%d_z9sym.out' % (LABEL, NN))
        rlt = None
        with open(lt) as fh:
            for ln in fh:
                if ln.startswith('KEYJSON '):
                    dd = json.loads(ln[8:])
                    if dd['key'] == 'Mt,0,0':
                        rlt = dd
        dm = rel_dev(res['Mb,0,0']['ak'], res['Mb,0,0']['B'], rlt) if rlt else float('inf')
        out('C-MIRROR LB N=%d: Mb,0,0 (pair (5,8)) against Mt,0,0 (pair (3,6)) of %s (sha256 %s), a_k and bar parts: largest relative difference '
            '%.2e -> %s' % (NN, os.path.basename(lt), sha_file(lt), dm, gate(fails, 'C-MIRROR', dm <= 1e-9)))
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
'''
head = HEAD.replace('@@P4@@', P4).replace('@@P3@@', P3)
assert '@@' not in head
text = head.encode('utf-8') + '\n'.join(pins).encode('utf-8') + b'\n# C-COPY block: rtwin_c3h_v1.py l.105-204\n' + b'\n'.join(block) + \
    b'\n# C-COPY end\n' + TAIL.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(text)
print('COPY %s %s' % (hashlib.sha256(text).hexdigest(), DST))
