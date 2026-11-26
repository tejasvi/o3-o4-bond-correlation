#!/usr/bin/env python3
"""kt_s8h_mk_v1.py -- pk11 (code/pk11/). P2-12's float entries (DESIGN_P2_12_FLOAT_v1 54ba892a, step 3): the a_k of every entry
of S8H_ENTRY_LIST_v2 (kt_s8h_list_v2 7193f65c; the list pinned below by full sha256) on kt_s8f3g's entry engine, as kt_s8_mkxk_v1_1
computed TXX (riglap3's E_j and factor series, amom2b at the needed degree D, K = 3 where (D+1)^F < 9e18, else the largest K that fits;
QCAP 6). FLOAT DATA: no remainder bar. Per item N and BLOCK:
- small: E2T (eT,a), D2T (DHT,a,b), E3T (fT,a, fT2,a), with the plain checks e,a (E2T), g,a,b (D2T) and f,a (E3T);
- h4: H4T (hT,a, hT1,a) with the plain check h,a;
- n2t: N2T (N2T,a,b);
- l: L (TT,a,b);
- probe: every graph's checks, Q-degree and the degree D each K needs, with the K and D the cap allows; no moment (seconds), so
  that the other blocks are priced from their D before they run (the moments' cost grows steeply with D: kt_s8_mkxk's N graph, V 9
  F 16, took 26 s at D 10 and 86 s at D 11).
The entries come from the list (C-LIST: the block's graphs, columns, pairs and factors exactly as the list has them; the list's
factor ['cp', a, c] is the trial state a on column c, ['xi', 'HT', c] the top-row bond between columns c and c + 1, ('xi', (u, v, v),
0.0, e_1) as S8F2_ENTRY_LIST_v1). Checks (gates unless INFO):
- C-HASH; C-LIST; C-GRAPH (V, edges, F against the list's shape and the window's edge count) and C-QCAP;
- C-SAME: the plain checks against pk03's float references (pinned): e,a (m3ref_v1_10 V3E2), g,a,b (V3D), f,a (V3E3), h,a
  (m3ref_v1_14 P16H p6), largest |a_k difference| / max(1, |a_k|) <= 1e-9: an entry is unchanged by the bond's extra pair form;
- C-CS (block l): T_aa^2 <= g_aa TT_aa for a = 0..3 at t = 0 and 1/300 (Cauchy-Schwarz for T^1/2 s_a and T^3/2 s_a; T from V3N, g
  from V3D);
- INFO: K and D per graph, the a_0 of every entry, and for every bond entry its a_0 against the plain entry's a_0 on the same trial
  states (the bond's mean in that geometry).
Writes pk11/out/s8h_mk_v1/out_kt_s8h_mk_v1_<n4|n3>_<block>.out and s8h_float_v1.<N>.<block>.json (new files; the folder must exist).
Run (one job at a time; LIM 5..300 s CPU, hard LIM + 5; AS 8 GiB):
  D=/mnt/g2/release/root/code/pk11; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_s8h_mk_v1.py n4 LIM BLOCK > $D/out/s8h_mk_v1/kt_s8h_mk_v1_n4_BLOCK.log 2>&1"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, hashlib, json, re

ITEMS = {'n4': 4, 'n3': 3}
BLOCKS = {'small': ('E2T', 'D2T', 'E3T'), 'h4': ('H4T',), 'n2t': ('N2T',), 'l': ('L',),
          'probe': ('E2T', 'D2T', 'E3T', 'H4T', 'N2T', 'L')}
if len(sys.argv) < 4 or sys.argv[1] not in ITEMS or sys.argv[3] not in BLOCKS:
    print('usage: kt_s8h_mk_v1.py n4|n3 LIM small|h4|n2t|l|probe   (LIM = RLIMIT_CPU soft limit in s, 5..300, hard LIM + 5)')
    sys.exit(2)
MODE, BLOCK = sys.argv[1], sys.argv[3]
N = ITEMS[MODE]
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (5 <= LIM <= 300):
    print('bad LIM %r (need 5 <= LIM <= 300)' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))

SCR = '/mnt/g2/release/root/code/pk10/scripts'
OWN = '/mnt/g2/release/root/code/pk11'
OUTD = OWN + '/out'
M3O = '/mnt/g2/release/root/code/pk03/out'
MKD = OUTD + '/s8h_mk_v1'
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(MKD, 'out_%s_%s_%s.out' % (LABEL, MODE, BLOCK))
JSON_PATH = os.path.join(MKD, 's8h_float_v1.%d.%s.json' % (N, BLOCK))
for p_ in (OUT_PATH, JSON_PATH):
    if not (os.path.isdir(MKD) and os.path.realpath(os.path.dirname(p_)) == os.path.realpath(MKD)
            and os.path.realpath(MKD).startswith(os.path.realpath(OUTD) + os.sep)):
        print('output directory check failed for %s' % p_)
        sys.exit(2)
FH = open(OUT_PATH, 'x')


def cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def out(line):
    FH.write(line + '\n')
    FH.flush()


LIST = OUTD + '/S8H_ENTRY_LIST_v2.json'
REF = {4: {'E2': [M3O + '/m3ref_v1_10_V3E2.4.all_z9sym.out'], 'E3': [M3O + '/m3ref_v1_10_V3E3.4.all_z9sym.out'],
           'D': [M3O + '/m3ref_v1_10_V3D.4.0-32_z9sym.out', M3O + '/m3ref_v1_10_V3D.4.33-65_z9sym.out'],
           'H': [M3O + '/m3ref_v1_14_P16H.4.p6_z9sym.out'], 'N': [M3O + '/m3ref_v1_10_V3N.4.all_z9sym.out']},
       3: {'E2': [M3O + '/m3ref_v1_10_V3E2.3.all_z9sym.out'], 'E3': [M3O + '/m3ref_v1_10_V3E3.3.all_z9sym.out'],
           'D': [M3O + '/m3ref_v1_10_V3D.3.all_z9sym.out'],
           'H': [M3O + '/m3ref_v1_14_P16H.3.p6_z9sym.out'], 'N': [M3O + '/m3ref_v1_10_V3N.3.all_z9sym.out']}}
PINS = {
    SCR + '/amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc',
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
    OUTD + '/ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    OUTD + '/ts_N3_S_z9sym_v1.json': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    OUTD + '/vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    OUTD + '/vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    LIST: '46401dd1f784aaf842206b43eb5377fa6996eeb7e9dedc77fd6b6d16a4831730',
}
for _fam, _ps in REF[N].items():
    for _p in _ps:
        PINS[_p] = None   # filled below from REFPINS
REFPINS = {
    M3O + '/m3ref_v1_10_V3E2.4.all_z9sym.out': 'de30ea911622306cc88b231f9dbfd17808a9495c150e16f71b7a5f50451b9469', M3O + '/m3ref_v1_10_V3E2.3.all_z9sym.out': '6615ba0adaa496be3c1fb5658b9955b5edc7659b7aeb82ef72ef9c722edc335f',
    M3O + '/m3ref_v1_10_V3E3.4.all_z9sym.out': '5cf7ab639fbc53f3ae694e6d073276946a07d82aa71a80e5cc54219f37205cc1', M3O + '/m3ref_v1_10_V3E3.3.all_z9sym.out': '10509eb7880bab08f9012527d5e0fd5e46f75942925c3562d780996a0361946b',
    M3O + '/m3ref_v1_10_V3D.4.0-32_z9sym.out': '7540647500f6c4368ad47967308b872224e08cbcaa645a1cf20acb469d9c5307', M3O + '/m3ref_v1_10_V3D.4.33-65_z9sym.out': '0b4c99038b245432b71e66e0ad88903b374f68b3d9b5a6521049b4c5d2098362',
    M3O + '/m3ref_v1_10_V3D.3.all_z9sym.out': '8a045f0bb2579e91f5a937761bacf0b54af6632b6e2a5b5307d3a652af74bc9a',
    M3O + '/m3ref_v1_14_P16H.4.p6_z9sym.out': 'df052bb8e868d03c6ca08cbd5cd4da288e5ab2e82e92e6eee805429b3200703a', M3O + '/m3ref_v1_14_P16H.3.p6_z9sym.out': '5029d364ccc4786b5e973cf216ca11677b71169c9cf1da3289fab7bf9d945781',
    M3O + '/m3ref_v1_10_V3N.4.all_z9sym.out': '65a8145b6f2ce35aa3692ab3f89447aa52c4420220408f3c028ee67bf7fdf0c2', M3O + '/m3ref_v1_10_V3N.3.all_z9sym.out': 'd12836039cc0390feed5435486459530a781cc75865f1ecf8b95f497a0421945',
}
for _p in list(PINS):
    if PINS[_p] is None:
        PINS[_p] = REFPINS[_p]


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('%s sha256 %s ITEM=%s BLOCK=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (
    LABEL, sha_file(os.path.abspath(__file__)), MODE, BLOCK, LIM, LIM, LIM + 5))
_bad = ['%s %s' % (p, sha_file(p)) for p in sorted(PINS) if sha_file(p) != PINS[p]]
out('C-HASH %s (%d files)%s' % ('PASS' if not _bad else 'FAIL', len(PINS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, SCR)
import riglap3 as _r3
from riglap2 import Graph
from riglap4 import group_factors, _deg
from riglap5b import series_product
from amom2b import AllMom2
from pseries import padd, pscale, pmul
from vacmod2 import A_EX, B_EX
from lapl2 import strip_graph

QCAP = 6
SFILE = {4: OUTD + '/ts_N4_J170_D_S_z9sym_v1.json', 3: OUTD + '/ts_N3_S_z9sym_v1.json'}
VFILE = {4: OUTD + '/vacres_K3_N4_sym_v1.json', 3: OUTD + '/vacres_K3_N3_sym_v1.json'}


def trip(c):
    return (3 * c, 3 * c + 1, 3 * c + 2)


def window(cols, pairs):
    """the list's graph: strip_graph's columns, a 'free' column with the physical verticals (kt_s8_mkxk's window), pairs as given."""
    V, E = strip_graph(len(cols), (A_EX, B_EX))
    for c, kind in enumerate(cols):
        if kind == 'free':
            E[(3 * c, 3 * c + 1)] = 1.0
            E[(3 * c + 1, 3 * c + 2)] = 1.0
            E.pop((3 * c, 3 * c + 2), None)
        elif kind not in ('vac', 'int'):
            raise ValueError(kind)
    return Graph(V, E, [tuple(p) for p in pairs], N=N), len(E)


def ej_series(g, order):
    Hs = _r3.Model3(g, 3, []).H(3)
    H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
    H1sq = pmul(H1, H1)
    full = [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
    return full[:order + 1]


def fi_series(g, facs, order):
    if not facs:
        return [{tuple([0] * g.F): 1.0}] + [{} for _ in range(order)]
    scal, groups = group_factors(facs)
    gser = [_r3.Model3(g, 3, gf).Fser(3).c for gf in groups]
    return series_product(gser, scal, 3)[:order + 1]


def dn(Fi, Ej, K):
    return max(_deg(Fi[i]) + _deg(Ej[k - i]) for k in range(K + 1) for i in range(k + 1) if Fi[i])


def run_sets(name, g, ne, shape, sets, kmax=3, probe=False):
    """the a_k of every factor set on graph g, at the largest K <= kmax whose degree D fits (D+1)^F < 9e18. probe=True (block probe):
    the graph's checks, K and D only, no moment (the price of the other blocks); returns (None, (K, D))."""
    t0 = cpu()
    Ej = ej_series(g, kmax)
    Fis = {k: fi_series(g, v, kmax) for k, v in sets.items()}
    qmax = max([sum(e[g.V:]) for Fi in Fis.values() for P in Fi for e in P] + [0])
    K, D = None, None
    for KK in range(kmax, -1, -1):
        DD = max(max(dn(Fi, Ej, KK) for Fi in Fis.values()), 1)
        if float(DD + 1) ** g.F < 9.0e18:
            K, D = KK, DD
            break
    okg = (g.V, ne, g.F) == shape
    okq = qmax <= QCAP
    out('PREP %s N=%d: Q-degree %d, K %s, D %s, %d factor sets (%.1f s so far)' % (name, N, qmax, K, D, len(sets), cpu() - t0))
    if K is None or not okg or not okq:
        raise ValueError('graph %s: shape %s (want %s), Q-degree %d, K %s' % (name, (g.V, ne, g.F), shape, qmax, K))
    if probe:
        Kd = {}
        for KK in range(kmax, -1, -1):
            Kd[KK] = max(max(dn(Fi, Ej, KK) for Fi in Fis.values()), 1)
        out('PROBE %s N=%d: V %d, edges %d, F %d (C-GRAPH PASS), Q-degree %d (C-QCAP PASS); degree needed for K = 3, 2, 1, 0: %s; '
            'the cap (D+1)^F < 9e18 allows D <= %d; taken K %d, D %d (%.1f s)' % (
                name, N, g.V, ne, g.F, qmax, ', '.join(str(Kd[k]) for k in range(kmax, -1, -1)),
                max(d for d in range(1, 40) if float(d + 1) ** g.F < 9.0e18), K, D, cpu() - t0))
        return None, (K, D)
    am = AllMom2(g.G, g.n, D, W=g.W, groups=g.groups, caps={1: QCAP})
    ak = {k: [sum(am.E2(Fi[i], Ej[kk - i]) for i in range(kk + 1) if Fi[i]) for kk in range(K + 1)] for k, Fi in Fis.items()}
    out('GRAPH %s N=%d: V %d, edges %d, F %d (C-GRAPH PASS); Q-degree %d (C-QCAP PASS); K %d, D %d; %d factor sets (%.1f s)' % (
        name, N, g.V, ne, g.F, qmax, K, D, len(sets), cpu() - t0))
    return ak, K


def ref_ak(paths):
    E = {}
    for path in paths:
        txt = open(path).read()
        if [ln for ln in txt.split('\n') if ln.startswith('VERDICT')] != ['VERDICT VALID']:
            raise ValueError('%s: VERDICT lines' % os.path.basename(path))
        for ln in txt.split('\n'):
            if ln.startswith('KEYJSON '):
                d = json.loads(ln[8:])
                if d.get('N') != N:
                    raise ValueError('%s: a KEYJSON line with N %r' % (os.path.basename(path), d.get('N')))
                E[d['key']] = [float(x) for x in d['ak']]
    return E


EDGES = {'free': 2, 'int': 2, 'vac': 3}   # vertical edges per column kind (a vac column carries strip_graph's (0, 2) edge)
fails = []
try:
    R3 = json.load(open(VFILE[N]))
    S = json.load(open(SFILE[N]))['S']
    L2 = json.load(open(LIST))

    def fac(f):
        if f[0] == 'cp':
            a, col = f[1], f[2]
            if a == 0:
                return ('p', trip(col), R3['q1'], R3['q2'], R3['q3'])
            return ('xi', trip(col), float(S[0][a]), [float(S[r][a]) for r in range(1, 10)])
        if f[0] == 'xi' and f[1] == 'HT':
            c9 = [0.0] * 9
            c9[0] = 1.0
            u, v = 3 * f[2], 3 * (f[2] + 1)
            return ('xi', (u, v, v), 0.0, c9)
        raise ValueError('factor %r' % (f,))
    # C-LIST: the block's entries exactly as the list has them
    if L2.get('list') != 'S8H_ENTRY_LIST_v2':
        raise ValueError('the list is %r' % L2.get('list'))
    sel = [e for e in L2['entries'] if e['graph'] in BLOCKS[BLOCK]]
    want = {'small': 4 + 10 + 8, 'h4': 8, 'n2t': 10, 'l': 10, 'probe': 50}[BLOCK]
    okL = len(sel) == want and all(e['graph'] in L2['graphs'] for e in sel)
    out('C-LIST: %d entries of %s from S8H_ENTRY_LIST_v2 (expected %d) -> %s' % (len(sel), '/'.join(BLOCKS[BLOCK]), want,
                                                                                 'PASS' if okL else 'FAIL'))
    if not okL:
        raise ValueError('C-LIST')
    REFS = {fam: ref_ak(ps) for fam, ps in REF[N].items()}
    allak, Ks, worst_same = {}, {}, {}
    for gname in BLOCKS[BLOCK]:
        gd = L2['graphs'][gname]
        g, ne = window(gd['columns'], gd['pairs'])
        V = 3 * len(gd['columns'])
        shape = (V, sum(EDGES[c] for c in gd['columns']) + 3 * (len(gd['columns']) - 1), V + len(gd['pairs']))
        sets = {e['key']: [fac(f) for f in e['factors']] for e in sel if e['graph'] == gname}
        for e in sel:
            if e['graph'] == gname and tuple(e['shape_V_F']) != (shape[0], shape[2]):
                raise ValueError('%s: list shape %s, window %s' % (e['key'], e['shape_V_F'], (shape[0], shape[2])))
        checks = {}
        if gname == 'E2T':
            checks = {'e,%d' % a: [fac(['cp', a, 0])] for a in range(4)}
        elif gname == 'D2T':
            checks = {'g,%d,%d' % (a, b): [fac(['cp', a, 0]), fac(['cp', b, 1])] for a in range(4) for b in range(a, 4)}
        elif gname == 'E3T':
            checks = {'f,%d' % a: [fac(['cp', a, 0])] for a in range(4)}
        elif gname == 'H4T':
            checks = {'h,%d' % a: [fac(['cp', a, 0])] for a in range(4)}
        sets.update(checks)
        ak, K_ = run_sets(gname, g, ne, shape, sets, probe=(BLOCK == 'probe'))
        Ks[gname] = K_
        if BLOCK == 'probe':
            continue
        allak.update(ak)
        fam = {'E2T': 'E2', 'D2T': 'D', 'E3T': 'E3', 'H4T': 'H'}.get(gname)
        if fam:
            w = 0.0
            for k in checks:
                r = REFS[fam].get(k)
                if r is None:
                    raise ValueError('reference %s has no %s' % (fam, k))
                for x, y in zip(ak[k], r):
                    w = max(w, abs(x - y) / max(1.0, abs(y)))
            worst_same[gname] = w
            okS = w <= 1e-9
            out('C-SAME %s: %d plain entries against pk03 %s: largest |a_k difference| / max(1, |a_k|) %.2e (tolerance 1e-9) -> %s' % (
                gname, len(checks), fam, w, 'PASS' if okS else 'FAIL'))
            if not okS:
                fails.append('C-SAME')
    if BLOCK == 'l':
        val = lambda a_, t: sum(c * t ** i for i, c in enumerate(a_))
        for t in (0.0, 1.0 / 300):
            bad = []
            for a in range(4):
                Ta = val(REFS['N']['T,%d,%d' % (a, a)], t)
                ga = val(REFS['D']['g,%d,%d' % (a, a)], t)
                TTa = val(allak['TT,%d,%d' % (a, a)], t)
                if not (ga > 0 and TTa > 0 and Ta * Ta <= ga * TTa):
                    bad.append(a)
            out('C-CS t=%.6g: T_aa^2 <= g_aa TT_aa for a = 0..3: failing %s -> %s' % (t, bad or 'none', 'PASS' if not bad else 'FAIL'))
            if bad:
                fails.append('C-CS')
    for e in (sel if BLOCK != 'probe' else []):
        k = e['key']
        out('A0 %s (%s, %s): a_0 %.12g, K %d' % (k, e['graph'], e['role'], allak[k][0], len(allak[k]) - 1))
    # INFO: a bond entry's a_0 over the plain entry's a_0 on the same trial states and graph
    for e in (sel if BLOCK != 'probe' else []):
        k = e['key']
        base = {'eT': 'e', 'fT': 'f', 'fT2': 'f', 'hT': 'h', 'hT1': 'h'}.get(k.split(',')[0])
        if base:
            b = '%s,%s' % (base, k.split(',')[1])
            if b in allak and allak[b][0] != 0:
                out('INFO MEAN %s / %s at t = 0: %.10f' % (k, b, allak[k][0] / allak[b][0]))
    doc = {'format': 'S8H_FLOAT_v1', 'status': 'FLOAT (no remainder bar; not certified)', 'N': N, 'J_REF': 300, 'block': BLOCK,
           'source': '%s sha256 %s (kt_s8f3g entry engine)' % (LABEL, sha_file(os.path.abspath(__file__))),
           'list': 'S8H_ENTRY_LIST_v2 sha256 %s' % PINS[LIST], 'K_by_graph': Ks,
           'entries': {k: {'ak': [float(x) for x in v], 'K': len(v) - 1} for k, v in sorted(allak.items())}}
    with open(JSON_PATH, 'x') as fh:
        json.dump(doc, fh, indent=1)
        fh.write('\n')
    out('WROTE %s %s (%d entries)' % (os.path.basename(JSON_PATH), sha_file(JSON_PATH), len(doc['entries'])))
except Exception as ex:
    import traceback
    out('ERROR %s: %s' % (type(ex).__name__, ex))
    out(traceback.format_exc().replace('\n', ' | ')[-1500:])
    fails.append('ERROR')
out('ITEM %s %s cpu %.1f s' % (MODE, BLOCK, cpu()))
out('VERDICT %s' % ('VALID' if not fails else 'INVALID (%s)' % ', '.join(fails)))
