#!/usr/bin/env python3
"""kt_s8f1_v1_3.py -- pk11 (code/pk11/). REVISION of kt_s8f1_v1_2.py (41f0603a). v1_2's item n234.4 (out e07996e1) read VERDICT
INVALID only through two float-consistency tolerances: C-SYM (an image's Cov*J^2 a_k, relative differences up to 1.2e-9 against 1e-10,
at n = 3 and 4) and C-KEYGRAPH (Z and N_e on their own graphs against the pair graphs, up to 3.9e-12 against 1e-12). Its kill reading
was CLEAR, and C-LIST, C-HARM (70 of 70), C-C3 and C-S8F1 (18 of 18) passed. The differences are float rounding: the entries are float
sums of exact moments on different graphs (other forms, other summation orders), and Cov's a_k are differences of O(1) terms (e.g.
S4,xy,0,TM,3,MB's a_3 ~ 7.5e-4 moves by ~8e-13 against terms of order 1). A wrong image or graph would move them by O(1). Change only:
  - C-SYM compares |delta a_k| with 1e-10 max(S_k, |a_k|), S_k = |(N_ef/Z)_k| + |(N_e N_f/Z^2)_k| the two terms that cancel (the
    rounding of a difference scales with them), and prints the largest ratio;
  - C-KEYGRAPH's tolerance is 1e-10 relative (entries, no cancellation).
Everything else is v1_2's; v1_2's docstring follows.
kt_s8f1_v1_2.py -- pk11 (code/pk11/). P2-13 (C3-short; STB_PHASE2_PLAN_v1_6 row P2-13; the approval of 2026-11-08, step 1): FLOAT
items for every pair class of S8F2_ENTRY_LIST_v1 (29663a16; kt_s8f2_list_v1 7d81b613): the whole strips P3 x P_n, n = 2..5, both ends
free, every pair of distinct edges up to reflection, at N = 4 and 3. FLOAT DATA: kt_s8f1_v1_1's exact_ak route (riglap3's E_j and factor
series, amom2b at the needed degree D, K = 3 where (D+1)^F < 9e18), no remainder bar. Per class, on its own graph (pairs = its two
bonds, F = V + 2), the a_k of Z, N_e, N_f and N_ef, J^2 Cov = N_ef/Z - N_e N_f/Z^2 to order K, and:
- C-LIST: the classes recomputed in-job (the builder's rule) equal the list's keys and images exactly;
- C-GRAPH (V = 3n, edges 5n - 3, F) and C-QCAP (Q-degree <= 6);
- C-HARM: a_0 against (N - 1) T^2 / 2, T from the strip's product-mode Green's function (independent of the engine; kt_s8f2_pilot_v1's
  strip_T, C-HARM-X there), relative 1e-10;
- C-C3: a_1 against the spin-wave c3 of the same pair on the same strip (pk10's G2WOLFF coefficients), with the spin-wave c2 against
  (N - 1) T^2 / 2, relative 1e-9;
- C-KEYGRAPH: Z on its own graph (pairs []) and each edge class's N_e on its own graph (pairs [the bond]), as the list's keys have them,
  equal the values on the pair graphs (relative 1e-12): the graph's extra pair forms do not change an entry;
- C-SYM: an image of the class (another member, its own graph) has the same a_k (relative 1e-10): every class at n <= 4 with images,
  the first three such classes at n = 5;
- C-S8F1: the n = 2..4 vertical pairs that kt_s8f1_v1_1 printed (out_kt_s8f1_v1_1_n4.out 2937ce30, _n3.out c17cc777; one graph with all
  its pairs) have the same a_k (relative 1e-9);
- reading (the kill rule, FLOAT): the K-term series' minimum over t in (0, 1/300] (3000 points and both ends); any value <= 0 is a
  STOP; INFO: the values at J = 300, 600, 1200 and infinity, |c_K t^K| / Cov at J = 300, the list's flags (S0, L19.6a, THM-n<=3: for
  n <= 3 the FLOAT sign is printed beside Theorems D(i), B(a) and C as a cross-check).
Items (one job each; LIM <= 540 s CPU; AS 8 GiB): n234.N (n = 2, 3, 4), n5a.N and n5b.N (n = 5: the first 34 and the last 33 of the 67
pair classes in the list's order, each with Z, the edge classes and its own C-SYM samples), N = 4 or 3. Writes pk11/out/out_kt_s8f1_v1_2_
<item>.out (new file). Run (one job at a time):
  D=/mnt/g2/release/root/code/pk11; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_s8f1_v1_2.py ITEM LIM > $D/out/kt_s8f1_v1_2_ITEM.log 2>&1"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, time, math, hashlib, signal, traceback, json, re

m_ = re.fullmatch(r'(n234|n5a|n5b)\.([34])', sys.argv[1]) if len(sys.argv) == 3 else None
if m_ is None:
    print('usage: kt_s8f1_v1_3.py n234.N|n5a.N|n5b.N LIM   (N 4 or 3; LIM 5..540)')
    sys.exit(2)
ITEM = sys.argv[1]
NS = (2, 3, 4) if m_.group(1) == 'n234' else (5,)
HALF = {'n234': None, 'n5a': 0, 'n5b': 1}[m_.group(1)]
N = int(m_.group(2))
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r (need 5 <= LIM <= 540)' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))
STAGE = ['start']
SCR = '/mnt/g2/release/root/code/pk10/scripts'
OWN = '/mnt/g2/release/root/code/pk11'
OUTD = OWN + '/out'
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(OUTD, 'out_%s_%s.out' % (LABEL, ITEM))
if not (os.path.isdir(OUTD) and os.path.realpath(os.path.dirname(OUT_PATH)) == os.path.realpath(OUTD)
        and os.path.realpath(OUTD).startswith(os.path.realpath(OWN) + os.sep)):
    print('output directory check failed for %s' % OUT_PATH)
    sys.exit(2)
FH = open(OUT_PATH, 'x')


def cpu():
    return time.process_time()


def mem():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def out(line):
    FH.write(line + '\n')
    FH.flush()


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s (peak memory %.0f MiB)' % (cpu(), STAGE[0], mem()))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
ENGINE = {   # kt_s8f1_v1_1's pins (8933412e)
    'amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc',
    'g2sw_core_snapshot.py': 'f1b51241c54e496a8de699cc3160de3281bf98c67d019f4e92459a222d3d003a',
    'lapl2.py': 'b28ffbdb86fab237564f2db9ea8b3e904481fba31ad79e39421de7b8a9dfe116',
    'npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
    'pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
    'riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
    'riglap3.py': 'e394f81567e62222240050c7cbc70c480b0804d929a8713a7b30e70ebbf1ea69',
    'riglap4.py': 'ed8eecd6c6ed529b9471097e205b63a9c0f1435973c498d9f1920850ec3d29d7',
    'riglap5b.py': '0f9dc107d8709a78e4793db0fce23d8559fa93346d593304433162c72b5b0b93',
    'vacmod2.py': '533546b173af147a56e9531e26afa64cb3dbaccefd5fb7b1283f03baff06a000',
}
LISTF = OUTD + '/S8F2_ENTRY_LIST_v1.json'
LIST_SHA = 'adaf07438f867232310c5a9f521461a9447b148b6895ed278bba3f7ecd1b03ff'
REFS = {OUTD + '/out_kt_s8f1_v1_1_n4.out': '2937ce3057c99a4716ae2be4f4d535d876281bcfe0615c90fddca807bdb7a1dc',
        OUTD + '/out_kt_s8f1_v1_1_n3.out': 'c17cc777f25b1a4243f3717687a2153cacbee160a8a524695b24ef7fa6df8ce0'}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('%s sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (LABEL, sha_file(os.path.abspath(__file__)), ITEM, LIM, LIM, LIM + 5))
_bad = ['%s %s' % (n_, sha_file(os.path.join(SCR, n_))) for n_ in sorted(ENGINE) if sha_file(os.path.join(SCR, n_)) != ENGINE[n_]]
_bad += ['%s %s' % (os.path.basename(p), sha_file(p)) for p, h in [(LISTF, LIST_SHA)] + sorted(REFS.items()) if sha_file(p) != h]
out('C-HASH %s (%d engine files, the list, %d references)%s' % ('PASS' if not _bad else 'FAIL', len(ENGINE), len(REFS),
                                                                 (': ' + '; '.join(_bad)) if _bad else ''))
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
from g2sw_core_snapshot import coeffs

QCAP = 6
JS = (300.0, 600.0, 1200.0)
TOL_HARM, TOL_C3, TOL_KG, TOL_SYM, TOL_S8F1 = 1e-10, 1e-9, 1e-10, 1e-10, 1e-9   # v1_3: TOL_KG 1e-10; TOL_SYM on |da_k|/max(S_k, |a_k|)
BORD = {'TM': 0, 'MB': 1, 'HT': 2, 'HM': 3, 'HB': 4}
TBMAP = {'TM': 'MB', 'MB': 'TM', 'HT': 'HB', 'HB': 'HT', 'HM': 'HM'}


# ------------------------------------------------ the list's class rule (kt_s8f2_list_v1)
def edges(n):
    return [(c, b) for c in range(n) for b in ('TM', 'MB')] + [(c, b) for c in range(n - 1) for b in ('HT', 'HM', 'HB')]


def vpair(e):
    c, b = e
    return {'TM': (3 * c, 3 * c + 1), 'MB': (3 * c + 1, 3 * c + 2), 'HT': (3 * c, 3 * c + 3), 'HM': (3 * c + 1, 3 * c + 4),
            'HB': (3 * c + 2, 3 * c + 5)}[b]


def ekey(e):
    return (e[0], BORD[e[1]])


def lr(n, e):
    c, b = e
    return (n - 1 - c, b) if b in ('TM', 'MB') else (n - 2 - c, b)


def tb(e):
    return (e[0], TBMAP[e[1]])


def images_e(n, e):
    return sorted({e, lr(n, e), tb(e), tb(lr(n, e))}, key=ekey)


def canon_pair(p):
    return tuple(sorted(p, key=ekey))


def images_p(n, e1, e2):
    out_ = {canon_pair((e1, e2)), canon_pair((lr(n, e1), lr(n, e2))), canon_pair((tb(e1), tb(e2))), canon_pair((tb(lr(n, e1)), tb(lr(n, e2))))}
    return sorted(out_, key=lambda q: (ekey(q[0]), ekey(q[1])))


def kx(n, e):
    return 'S%d,x,%d,%s' % (n, e[0], e[1])


def kxy(n, p):
    return 'S%d,xy,%d,%s,%d,%s' % (n, p[0][0], p[0][1], p[1][0], p[1][1])


def classes(n):
    E = edges(n)
    ecl, pcl = {}, {}
    for e in E:
        ecl.setdefault(images_e(n, e)[0], set()).add(e)
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            im = images_p(n, E[i], E[j])
            pcl.setdefault(im[0], set()).update(im)
    return ({r: sorted(s, key=ekey) for r, s in ecl.items()},
            {r: sorted(s, key=lambda q: (ekey(q[0]), ekey(q[1]))) for r, s in pcl.items()})


def parse_key(k):
    p = k.split(',')
    if p[1] == 'x':
        return ((int(p[2]), p[3]),)
    return ((int(p[2]), p[3]), (int(p[4]), p[5]))


# ------------------------------------------------ the engine (kt_s8f1_v1_1, kt_s8f2_pilot_v1)
def xi_fac(e):
    c, b = e
    c9 = [0.0] * 9
    if b in ('TM', 'MB'):
        c9[0 if b == 'TM' else 1] = 1.0
        return ('xi', (3 * c, 3 * c + 1, 3 * c + 2), 0.0, c9)
    u, v = vpair(e)
    c9[0] = 1.0
    return ('xi', (u, v, v), 0.0, c9)


def strip(ncols, pairs):
    V, E = strip_graph(ncols, (A_EX, B_EX))
    for c in (0, ncols - 1):
        E[(3 * c, 3 * c + 1)] = 1.0
        E[(3 * c + 1, 3 * c + 2)] = 1.0
        E.pop((3 * c, 3 * c + 2), None)
    return Graph(V, E, pairs, N=N), len(E)


def ej_series(g):
    Hs = _r3.Model3(g, 3, []).H(3)
    H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
    H1sq = pmul(H1, H1)
    return [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]


def fi_series(g, facs):
    if not facs:
        return [{tuple([0] * g.F): 1.0}, {}, {}, {}]
    scal, groups = group_factors(facs)
    gser = [_r3.Model3(g, 3, gf).Fser(3).c for gf in groups]
    return series_product(gser, scal, 3)


def dn(Fi, Ej, K):
    return max(_deg(Fi[i]) + _deg(Ej[k - i]) for k in range(K + 1) for i in range(k + 1) if Fi[i])


def s_mul(a, b, K):
    return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(K + 1)]


def s_inv(z, K):
    r = [1.0 / z[0]] + [0.0] * K
    for k in range(1, K + 1):
        r[k] = -sum(z[i] * r[k - i] for i in range(1, k + 1)) / z[0]
    return r


def cov_series(z, nx, ny, nxy, K):
    iz = s_inv(z, K)
    a, b, c = s_mul(nxy, iz, K), s_mul(nx, iz, K), s_mul(ny, iz, K)
    bc = s_mul(b, c, K)
    return [a[k] - bc[k] for k in range(K + 1)]


def cov_scale(z, nx, ny, nxy, K):
    """v1_3: S_k = |(N_ef/Z)_k| + |(N_e N_f/Z^2)_k|, the two terms whose difference is Cov's a_k (its rounding scales with them)."""
    iz = s_inv(z, K)
    a, b, c = s_mul(nxy, iz, K), s_mul(nx, iz, K), s_mul(ny, iz, K)
    bc = s_mul(b, c, K)
    return [abs(a[k]) + abs(bc[k]) for k in range(K + 1)]


def strip_T(n, e, f):
    mus = [(0.0, [1 / math.sqrt(3)] * 3), (1.0, [1 / math.sqrt(2), 0.0, -1 / math.sqrt(2)]),
           (3.0, [1 / math.sqrt(6), -2 / math.sqrt(6), 1 / math.sqrt(6)])]
    lams = [(2 - 2 * math.cos(math.pi * m / n), [(math.sqrt(1.0 / n) if m == 0 else math.sqrt(2.0 / n)) * math.cos(math.pi * m * (j + 0.5) / n)
                                                  for j in range(n)]) for m in range(n)]

    def amp(b, k, m):
        u, v = vpair(b)
        ph, ps = mus[k][1], lams[m][1]
        return ph[u % 3] * ps[u // 3] - ph[v % 3] * ps[v // 3]
    return sum(amp(e, k, m) * amp(f, k, m) / (mus[k][0] + lams[m][0]) for k in range(3) for m in range(n) if (k, m) != (0, 0))


def sw_coeffs(n, eX, eY):
    E = []
    for j in range(n):
        E += [(3 * j, 3 * j + 1), (3 * j + 1, 3 * j + 2)]
        if j < n - 1:
            E += [(3 * j + r, 3 * (j + 1) + r) for r in range(3)]
    x, y = eX
    u, v = eY
    root, b = (x, y) if x not in (u, v) else (y, x)
    if root in (u, v):
        raise ValueError('pair shares both roots')
    free = [w for w in range(3 * n) if w != root]
    ix = {w: i for i, w in enumerate(free)}
    ed = {}
    for (p, q) in E:
        if p == root:
            ed[(ix[q], -1)] = 1.0
        elif q == root:
            ed[(ix[p], -1)] = 1.0
        else:
            ed[(ix[p], ix[q])] = 1.0
    c2, c3, _G = coeffs(len(free), ed, ix[b], ix[u], ix[v], N - 1)
    return c2, c3


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def series_min(c, tmax):
    ts = [tmax * i / 3000.0 for i in range(1, 3001)]
    vals = [sum(ck * t ** k for k, ck in enumerate(c)) for t in ts]
    i = min(range(len(vals)), key=lambda q: vals[q])
    return min(vals[i], c[0]), (ts[i] if vals[i] < c[0] else 0.0)


def entries_ak(n, bonds, sets):
    """the a_k of the named factor sets on the strip's graph with pairs = the bonds' vertex pairs; (ak, K, D, F, shape ok, qmax)."""
    g, ne = strip(n, [vpair(b) for b in bonds])
    okg = (g.V, ne, g.F) == (3 * n, 5 * n - 3, 3 * n + len(bonds))
    Ej = ej_series(g)
    Fis = {k: fi_series(g, v) for k, v in sets.items()}
    qmax = max([sum(x[g.V:]) for Fi in Fis.values() for P in Fi for x in P] + [0])
    K, D = None, None
    for KK in (3, 2, 1):
        DD = max(max(dn(Fi, Ej, KK) for Fi in Fis.values()), 1)
        if float(DD + 1) ** g.F < 9.0e18:
            K, D = KK, DD
            break
    if K is None:
        return None, None, None, g.F, okg, qmax
    am = AllMom2(g.G, g.n, D, W=g.W, groups=g.groups, caps={1: QCAP})
    ak = {k: [sum(am.E2(Fi[i], Ej[kk - i]) for i in range(kk + 1) if Fi[i]) for kk in range(K + 1)] for k, Fi in Fis.items()}
    return ak, K, D, g.F, okg, qmax


def pair_cov(n, e, f):
    ak, K, D, F, okg, qmax = entries_ak(n, (e, f), {'Z': [], 'X': [xi_fac(e)], 'Y': [xi_fac(f)], 'XY': [xi_fac(e), xi_fac(f)]})
    if ak is None:
        return None
    return {'ak': ak, 'K': K, 'D': D, 'F': F, 'okg': okg, 'qmax': qmax, 'c': cov_series(ak['Z'], ak['X'], ak['Y'], ak['XY'], K),
            'S': cov_scale(ak['Z'], ak['X'], ak['Y'], ak['XY'], K)}


def s8f1_refs():
    """kt_s8f1_v1_1's printed a_k of its S2-S4 vertical pairs at this N: {class key: a_k}."""
    path = OUTD + ('/out_kt_s8f1_v1_1_n4.out' if N == 4 else '/out_kt_s8f1_v1_1_n3.out')
    refs = {}
    with open(path) as fh:
        for ln in fh:
            mt = re.match(r'^PAIR n([234]) (same|flip) ([0-9])-([0-9]) N=%d \[S[234]\]: Cov\*J\^2 a_k \[([^\]]*)\]' % N, ln)
            if mt:
                n, kind, x, y = int(mt.group(1)), mt.group(2), int(mt.group(3)), int(mt.group(4))
                e, f = (x - 1, 'TM'), (y - 1, 'TM' if kind == 'same' else 'MB')
                refs.setdefault(kxy(n, images_p(n, e, f)[0]), []).append([float(v) for v in mt.group(5).split(',')])
    return refs


def main():
    fails, stops = [], []
    try:
        STAGE[0] = 'C-LIST'
        L = json.load(open(LISTF))
        byn = {}
        for ent in L['entries']:
            byn.setdefault(ent['n'], []).append(ent)
        for n in NS:
            ecl, pcl = classes(n)
            want = sorted(['S%d,Z' % n] + [kx(n, r) for r in ecl] + [kxy(n, r) for r in pcl])
            got = sorted(e['key'] for e in byn.get(n, []))
            okl = want == got and all(e.get('images', [e['key']]) == ([kx(n, x) for x in ecl[parse_key(e['key'])[0]]]
                                                                       if ',x,' in e['key'] else [kxy(n, q) for q in pcl[parse_key(e['key'])]])
                                      for e in byn.get(n, []) if ',Z' not in e['key'])
            out('C-LIST n = %d: %d keys (%d edge classes, %d pair classes), the list\'s keys and images %s -> %s' % (
                n, len(want), len(ecl), len(pcl), 'equal the in-job classes' if okl else 'DIFFER', 'PASS' if okl else 'FAIL'))
            if not okl:
                fails.append('C-LIST n%d' % n)
        refs = s8f1_refs()
        for n in NS:
            ecl, pcl = classes(n)
            flags = {e['key']: e.get('flags', []) for e in byn[n]}
            STAGE[0] = 'n %d Z and x graphs' % n
            t0 = cpu()
            zak, _K, _D, _F, okz, _q = entries_ak(n, (), {'Z': []})
            xak = {}
            for r in sorted(ecl, key=ekey):
                a_, _K, _D, _F, okx, _q = entries_ak(n, (r,), {'X': [xi_fac(r)]})
                xak[r] = a_['X']
                if not okx:
                    fails.append('C-GRAPH %s' % kx(n, r))
            if not okz:
                fails.append('C-GRAPH S%d,Z' % n)
            out('KEYGRAPHS n = %d: Z and %d edge classes on their own graphs (cpu %.1f s)' % (n, len(ecl), cpu() - t0))
            kg_worst, nsym, sym_worst = 0.0, 0, 0.0
            reps = sorted(pcl, key=lambda q: (ekey(q[0]), ekey(q[1])))
            if HALF is not None:
                reps = reps[:34] if HALF == 0 else reps[34:]
                out('n = %d, item %s: pair classes %d of %d (the list\'s order)' % (n, ITEM, len(reps), len(pcl)))
            for r in reps:
                key = kxy(n, r)
                STAGE[0] = 'pair %s' % key
                t1 = cpu()
                e, f = r
                res = pair_cov(n, e, f)
                if res is None:
                    out('PAIR %s N=%d: no K fits -> FAIL' % (key, N))
                    fails.append('no K ' + key)
                    continue
                c, K = res['c'], res['K']
                if not res['okg']:
                    fails.append('C-GRAPH ' + key)
                if res['qmax'] > QCAP:
                    fails.append('C-QCAP ' + key)
                ex, ey = images_e(n, e)[0], images_e(n, f)[0]
                kg = max(rel(res['ak']['Z'][k], zak['Z'][k]) for k in range(K + 1))
                kg = max(kg, max(rel(res['ak']['X'][k], xak[ex][k]) for k in range(K + 1)),
                         max(rel(res['ak']['Y'][k], xak[ey][k]) for k in range(K + 1)))
                kg_worst = max(kg_worst, kg)
                T = strip_T(n, e, f)
                c2 = (N - 1) * T * T / 2
                okh = rel(c[0], c2) <= TOL_HARM
                s2, s3 = sw_coeffs(n, vpair(e), vpair(f))
                ok3 = rel(c[1], s3) <= TOL_C3 and rel(s2, c2) <= TOL_C3
                vals = [sum(ck * (1.0 / J) ** k for k, ck in enumerate(c)) for J in JS]
                vmin, tmin = series_min(c, 1.0 / 300)
                last = abs(c[K] * (1.0 / 300) ** K) / vals[0] if vals[0] != 0 else float('inf')
                fl = flags.get(key, [])
                out('PAIR %s N=%d (F %d, D %d, K %d; %d images; flags %s): Cov*J^2 a_k [%s]' % (
                    key, N, res['F'], res['D'], K, len(pcl[r]), ' '.join(fl) or '-', ', '.join(repr(v) for v in c)))
                out('  C-HARM a_0 %.12e vs (N-1)T^2/2 %.12e rel %.1e -> %s; C-C3 a_1 %.9e vs spin-wave c3 %.9e (c2 rel %.1e) rel %.1e -> %s; '
                    'C-KEYGRAPH rel %.1e; J = 300 %.6e, 600 %.6e, 1200 %.6e, inf %.6e; min over (0, 1/300] %.6e (t %.3e); |c_K t^K|/Cov '
                    '%.1e%s (cpu %.1f s)' % (c[0], c2, rel(c[0], c2), 'PASS' if okh else 'FAIL', c[1], s3, rel(s2, c2), rel(c[1], s3),
                                             'PASS' if ok3 else 'FAIL', kg, vals[0], vals[1], vals[2], c[0], vmin, tmin, last,
                                             ('; THM-n<=3 cross-check: FLOAT Cov*J^2 %s 0 on (0, 1/300]' % ('>' if vmin > 0 else '<='))
                                             if 'THM-n<=3' in fl else '', cpu() - t1))
                if not okh:
                    fails.append('C-HARM ' + key)
                if not ok3:
                    fails.append('C-C3 ' + key)
                if not (vmin > 0):
                    stops.append(key)
                if len(pcl[r]) > 1 and (n <= 4 or nsym < 3):
                    STAGE[0] = 'C-SYM %s' % key
                    q = pcl[r][-1] if pcl[r][-1] != r else pcl[r][0]
                    rq = pair_cov(n, q[0], q[1])
                    w = (max(abs(rq['c'][k] - c[k]) / max(res['S'][k], abs(c[k])) for k in range(K + 1))
                         if rq is not None and rq['K'] == K else float('inf'))   # v1_3: scale-aware
                    nsym += 1
                    sym_worst = max(sym_worst, w)
                    if not (w <= TOL_SYM):
                        fails.append('C-SYM ' + key)
                        out('  C-SYM %s vs %s: largest |delta a_k| / max(S_k, |a_k|) %.1e -> FAIL' % (key, kxy(n, q), w))
                if key in refs:
                    for ref in refs[key]:
                        w8 = max(rel(c[k], ref[k]) for k in range(min(len(ref), K + 1)))
                        ok8 = w8 <= TOL_S8F1
                        out('  C-S8F1 %s: kt_s8f1_v1_1\'s printed a_k, largest relative difference %.1e -> %s' % (key, w8, 'PASS' if ok8 else 'FAIL'))
                        if not ok8:
                            fails.append('C-S8F1 ' + key)
            okkg = kg_worst <= TOL_KG
            out('C-KEYGRAPH n = %d: Z and N_e on their own graphs vs the pair graphs, largest relative difference %.1e -> %s' % (
                n, kg_worst, 'PASS' if okkg else 'FAIL'))
            if not okkg:
                fails.append('C-KEYGRAPH n%d' % n)
            out('C-SYM n = %d: %d classes checked against an image, largest |delta a_k| / max(S_k, |a_k|) %.1e (tol %.0e) -> %s' % (
                n, nsym, sym_worst, TOL_SYM, 'PASS' if sym_worst <= TOL_SYM else 'FAIL'))
        out('KILL READING N=%d, n in %s: %s' % (N, list(NS), ('STOP: Cov*J^2 <= 0 for ' + ', '.join(stops)) if stops else
                                                'CLEAR: every pair class has Cov*J^2 > 0 on (0, 1/300] (FLOAT, K-term series)'))
    except MemoryError:
        out('MEMORY-STOP in stage %s at cpu %.1f s (peak memory %.0f MiB)' % (STAGE[0], cpu(), mem()))
        out('VERDICT INCOMPLETE (MEMORY)')
        return 3
    except Exception as e:
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        for ln in traceback.format_exc().splitlines()[-12:]:
            out('TRACE ' + ln)
        out('VERDICT INVALID (ERROR)')
        return 1
    why = fails + (['KILL STOP'] if stops else [])
    out('ITEM %s cpu %.1f s, peak resident memory %.0f MiB' % (ITEM, cpu(), mem()))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why[:12])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
