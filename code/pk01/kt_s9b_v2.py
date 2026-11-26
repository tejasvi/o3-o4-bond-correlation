#!/usr/bin/env python3
"""kt_s9b_v2.py -- pk01 (code/pk01/). The even-block entries at J = 300 for KT-RB of SPEC_M1_CERT_v1 (ece66dc2, sect. 2).
FLOAT DATA: Lemma 19.1c bounds (PK10_NOTES sect. 19.3.2; riglap5s) evaluated in floating point; their certification is milestone M3.

REVISION of kt_s9b_v1.py (350c607a), whose objects, settings and checks it keeps (see v1's header for G, T, Ih, Dx, the Ritz pencil, the
  amplitudes, C-XIH, C-QCAP, C-AK, C-G00, C-EIG, C-HARM, C-PROP, C-KA and the plants). Changes:
  (1) one pass at J = 300 in place of the passes at J = 10^3 and 170, with the radii a_v = min(80 G_vv/300, 0.6) set at J_REF = 300 and held
      fixed in J (sect. 19.3.5), so each remainder bounds its entry for every J >= 300;
  (2) the three Dx entries are computed at J = 300 with their remainders (v1 computed Dx at J = 10^3 only, and kt_c's assembly took its
      remainder as 0);
  (3) new checks C-AKV1 (every entry's exact a_k equal kt_s9b_v1's printed a_k: J = 170 lines for G, T, Ih and the J = 10^3 lines for Dx,
      within 1e-10 max(1, |a|)) and C-J300 (each of the 15 G, T, Ih remainders at J = 300 is at most its J = 170 remainder in v1's output);
      v1's C-AKJ (two J) and its S9 kill logic are dropped; the reading R_B at J = 300 (one-at-a-time, as v1) is printed as information only.
Output: ENTRY N J=300 lines for the 18 entries G (6), T (6), Ih (3), Dx (3): exact a_0..a_3 and rem, tail, ann, far. kt_rb_v1 reads them.
Items: smoke (N = 3, J = 300: the 2-column prep with G[0,0] and the 3-column prep with T[0,0] and Ih[1], timed), n4 and n3 (all 18 entries
  at J = 300 and the checks). Prices [E] from v1's timings (PREP-N 145-168 s, PREP-D ~2 s, entries <= 55 s each, one pass): n4 and n3
  200-330 s each (LIM 540, cap 545 s = 0.151 core-h each).
CPU and CAP-STOP as v1: RLIMIT_CPU soft LIM, hard LIM + 5; guards before each prep and entry; SIGXCPU prints CAP-STOP and exits 3.
Run: D=/mnt/g2/release/root/code/pk01; env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2
  TMPDIR=$D/tmp_kt_s9b timeout 600 nice -n 10 prlimit --as=8589934592 --cpu=<LIM + 5> -- python3 -I -B $D/kt_s9b_v2.py
  <item> <LIM> > $D/out_kt_s9b_v2_<item>.out 2> $D/out_kt_s9b_v2_<item>.err
"""
import resource, sys, time, math, hashlib, signal, os, traceback, re
ITEMS = ('smoke', 'n4', 'n3')
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: kt_s9b_v2.py ITEM LIM   (ITEM smoke | n4 | n3; LIM = RLIMIT_CPU soft limit in s, hard LIM + 5)')
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2])
if not (5 <= LIM <= 540):
    print('bad LIM %d (need 5 <= LIM <= 540)' % LIM)
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
STAGE = ['start']


def cpu():
    return time.process_time()


def out(line):
    print(line, flush=True)


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)

SCR = '/mnt/g2/release/root/code/pk10/scripts'
INP = '/mnt/g2/release/root/code/pk10/scratch'
OWN = '/mnt/g2/release/root/code/pk01'
ENGINE = {
    'amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc',
    'g2sw_core_snapshot.py': 'f1b51241c54e496a8de699cc3160de3281bf98c67d019f4e92459a222d3d003a',
    'lapl2.py': 'b28ffbdb86fab237564f2db9ea8b3e904481fba31ad79e39421de7b8a9dfe116',
    'npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
    'pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
    'riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
    'riglap3.py': 'e394f81567e62222240050c7cbc70c480b0804d929a8713a7b30e70ebbf1ea69',
    'riglap4.py': 'ed8eecd6c6ed529b9471097e205b63a9c0f1435973c498d9f1920850ec3d29d7',
    'riglap5.py': 'bbfbea1f5b2680eec71eee647b2c608e08f8feacf8c21fbd67f4d0ff76f037a3',
    'riglap5b.py': '0f9dc107d8709a78e4793db0fce23d8559fa93346d593304433162c72b5b0b93',
    'riglap5c.py': 'efb2f505a2d169874e2beb358ed5179901fbd6bde0791ccd578309a2a57a054e',
    'riglap5e.py': 'cafd025a5bb46c8b4a742ca3358d299bdea8e1b382893a9c8127ec4a1da821d9',
    'riglap5r.py': '7feb47f7ce840837cf04b3156e4ed94c22ec2cb3543276c0d3892c4d6a6fe749',
    'riglap5s.py': '44bdafd38b6a77af38af0e77ea17833fa08cdde734ecce3951795984b957e839',
    'vacmod2.py': '533546b173af147a56e9531e26afa64cb3dbaccefd5fb7b1283f03baff06a000',
}
INPUTS = {
    'binding3_N4_J170.json': '8d784d1c6a9c83b661aeee466dcae96b7300150d59cf5753b413af357439c927',
    'binding_N4_J170.json': '43c7331aad10481bf51a20b1b860fa4f882f92ec1bf4b1ae18a37d96ca936316',
    'clT_N3_J170.json': '7d62c3030480a4ffb41befe931614bd790d06cf975e07963814dcac9269dc998',
    'clT_N4_J170.json': 'cfd2ab7c1be04487f8ec1b012eda42cbced4bb38310d00fcd2ac5e765b312669',
    'ts_N3_S.json': '26e20e76fbce80c205703f5ba27395ebddaeaa2713bb129b0b4e5902a2061955',
    'ts_N4_J170_D_S.json': 'd6d104ea1f2f64a82f051ce2872f1fbbd0628c9875b0743e4815bf74643fea8c',
    'vacres_K3_N3.json': 'ebcbd08ca532642188071c964039808a318038020bb1a788a7fa3a49cb357426',
    'vacres_K3_N4.json': '516b2501c37a65b21b617fba3cb1d7b02adf9966f409bc5105418822dfa0e765',
}
OWNFILES = {
    'out_kt_s9b_v1_n3.out': '1e3aa09ef3a828d5ffc3a14bebb610958ee7c5e815b933f0f8442b640ce7eebc',
    'out_kt_s9b_v1_n4.out': 'ab1273ab55f8e1d1a9160eb35c5620a706b837aefd16ed430f4126eb3d0b97f0',
}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('kt_s9b_v2 sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (sha_file(os.path.abspath(__file__)), MODE, LIM, LIM, LIM + 5))
_bad = []
for _d, _tab in ((SCR, ENGINE), (INP, INPUTS), (OWN, OWNFILES)):
    for _n in sorted(_tab):
        _got = sha_file(os.path.join(_d, _n))
        if _got != _tab[_n]:
            _bad.append('%s %s' % (_n, _got))
out('C-HASH %s (%d engine files, %d inputs, %d own outputs)%s' % ('PASS' if not _bad else 'FAIL', len(ENGINE), len(INPUTS), len(OWNFILES),
                                                  (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, SCR)
import json
import numpy as np
import scipy.linalg
from mpmath import mp
import riglap5b
import riglap5s
import riglap2 as _r
import riglap3 as _r3
from riglap2 import Graph
from riglap4 import group_factors
from riglap5b import series_product
from vacmod2 import A_EX, B_EX
from lapl2 import strip_graph
mp.dps = 40

S_RAD, RHO_P, J_REF, QCAP = 80.0, 0.7, 300.0, 6
NPB = {'D': 16, 'N': 12}
JS = (300.0,)
B_N = {3: 0.06784, 4: 0.16603}
MARGIN, TOL_KA = 0.3, 0.02
T_KA = ('1e-5', '5e-6')
EVEN = (0, 1, 3)
PE = ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3))
RNAMES = ['G,%d,%d' % p for p in PE] + ['T,%d,%d' % p for p in PE] + ['Ih,%d' % b for b in EVEN]
X0 = (7 - 3 * mp.sqrt(5)) / 2
Y0 = (23 - 5 * mp.sqrt(21)) / 2
LD, RD = (0, 1, 2), (3, 4, 5)
LN, RN = (0, 1, 2), (6, 7, 8)
PAIRS_D = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
PAIRS_N = [(0, 1), (1, 2), (0, 2), (4, 7), (6, 7), (7, 8), (6, 8)]
H_XI = ('xi', (4, 7, 8), 0.0, [1.0] + [0.0] * 8)
SFILE = {4: 'ts_N4_J170_D_S.json', 3: 'ts_N3_S.json'}
VFILE = {4: 'vacres_K3_N4.json', 3: 'vacres_K3_N3.json'}
CLT = {4: 'clT_N4_J170.json', 3: 'clT_N3_J170.json'}
G00_REF = {4: 1.006947449, 3: 1.004868248}
GUARD = {'prepN': 100.0, 'prepD': 30.0, 'entry': 20.0}


class CapStop(Exception):
    pass


def need(kind):
    if cpu() > LIM - GUARD[kind]:
        raise CapStop(kind)


def load_json(name):
    with open(os.path.join(INP, name)) as fh:
        return json.load(fh)


def make_jobs(Smat, R3, with_dx):
    def pv(col):
        return ('p', col, R3['q1'], R3['q2'], R3['q3'])

    def cpoly(b, col):
        return pv(col) if b == 0 else ('xi', col, float(Smat[0, b]), [float(x) for x in Smat[1:, b]])

    def xia(col):
        return ('xi', col, 0.0, [1.0] + [0.0] * 8)
    jd = [('G,%d,%d' % (b, c), [cpoly(b, LD), cpoly(c, RD)]) for (b, c) in PE]
    if with_dx:
        jd += [('Dx,%d' % b, [cpoly(b, LD), xia(RD), pv(RD)]) for b in EVEN]
    jn = [('T,%d,%d' % (b, c), [cpoly(b, LN), cpoly(c, RN)]) for (b, c) in PE]
    jn += [('Ih,%d' % b, [cpoly(b, LN), H_XI, pv(RN)]) for b in EVEN]
    return jd, jn


def graphs(N):
    VD, ED = strip_graph(2, (A_EX, B_EX))
    VN, EN = strip_graph(3, (A_EX, B_EX))
    return Graph(VD, ED, PAIRS_D, N=N), Graph(VN, EN, PAIRS_N, N=N)


def radii(g):
    return [math.sqrt(min(S_RAD * g.G[v, v] / J_REF, 0.6)) for v in range(g.V)]


def make_prep(g, J, key, kind):
    riglap5b.NPOLY_B = NPB[kind]
    return riglap5s.Prep5s(g, J, radii(g), RHO_P, key=key, qcap=QCAP)


def run_entry(pr, kind, facs):
    riglap5b.NPOLY_B = NPB[kind]
    ak, B = riglap5s.bound5s(pr, facs)
    return [float(x) for x in ak], dict((k, float(v)) for k, v in B.items())


def entry_line(N, J, nm, E, t0):
    ak, B = E
    return 'ENTRY N=%d J=%g %s ak=[%s] rem=%r tail=%r ann=%r far=%r r=%.6e (%.1f s, cpu %.1f s)' % (
        N, J, nm, ', '.join(repr(x) for x in ak), B['rem'], B['tail'], B['ann'], B['far'], sum(B.values()), cpu() - t0, cpu())


def qmax_of(g, facs):
    scal, groups = group_factors(facs)
    gser = [_r3.Model3(g, 3, gf).Fser(3).c for gf in groups]
    Fi = series_product(gser, scal, 3)
    return max([sum(e[g.V:]) for P in Fi for e in P] + [0])


def check_xih(gN):
    xs = _r3.Model3(gN, 3, [H_XI]).Fser(3).c
    ds = _r.Model(gN, 4, [('dot', 4, 7, 1.0)]).Fser(4).c
    worst = 0.0
    for k in range(4):
        for e in set(xs[k]) | set(ds[k + 1]):
            a, b = xs[k].get(e, 0.0), ds[k + 1].get(e, 0.0)
            worst = max(worst, abs(a + b) / max(1.0, abs(a)))
    return worst


# ---------------------------------------------- the even-block Ritz problem, in mpmath (dps 40)
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


def mhat(R3, t):
    return ev([1.0, R3['m1'], R3['m2'], R3['m3']], t)


def mats(E, t):
    G = [[ev(E['G,%d,%d' % (min(b, c), max(b, c))][0], t) for c in EVEN] for b in EVEN]
    T = [[ev(E['T,%d,%d' % (min(b, c), max(b, c))][0], t) for c in EVEN] for b in EVEN]
    Ih = [ev(E['Ih,%d' % b][0], t) for b in EVEN]
    Dx = [ev(E['Dx,%d' % b][0], t) for b in EVEN]
    return G, T, Ih, Dx


def amps(G, T, Ih, Dx, mh, pos=(0, 1, 2)):
    vals, vecs = ritz(G, T, pos)
    l0, sg0 = vals[0], mp.sqrt(G[0][0])

    def amp(cv, w, p):
        return mh * mp.fsum([cv[i] * w[a] for i, a in enumerate(pos)]) / (sg0 * l0 ** p)
    A = {'l0': l0, 'xR': vals[1] / l0, 'cx': vecs[1]}
    A['h0'], A['a0'] = amp(vecs[0], Ih, 2), amp(vecs[0], Dx, 1)
    A['hx'], A['ax'] = amp(vecs[1], Ih, 2), amp(vecs[1], Dx, 1)
    if len(pos) > 2:
        A['yR'] = vals[2] / l0
        A['hy'], A['ay'] = amp(vecs[2], Ih, 2), amp(vecs[2], Dx, 1)
    return A


def bco(t, A, power=2):
    return A['hx'] * A['ax'] / (t * A['xR'] ** power)


def perturbed(G, T, Ih, nm, d):
    G2, T2, Ih2 = [row[:] for row in G], [row[:] for row in T], Ih[:]
    kind, rest = nm.split(',', 1)
    if kind == 'Ih':
        Ih2[EVEN.index(int(rest))] += d
    else:
        b, c = [EVEN.index(int(x)) for x in rest.split(',')]
        M2 = G2 if kind == 'G' else T2
        M2[b][c] += d
        if b != c:
            M2[c][b] += d
    return G2, T2, Ih2


def remainders(E, t, mh):
    G, T, Ih, Dx = mats(E, t)
    base = amps(G, T, Ih, Dx, mh)
    b0 = bco(t, base)
    D = {}
    for nm in RNAMES:
        r = sum(E[nm][1].values())
        if not math.isfinite(r):
            D[nm] = (mp.inf, mp.inf)
            continue
        dh, dB = mp.mpf(0), mp.mpf(0)
        for s in (1, -1):
            try:
                A2 = amps(*perturbed(G, T, Ih, nm, s * mp.mpf(r)), Dx, mh)
            except ValueError:
                dh, dB = mp.inf, mp.inf
                break
            dh = max(dh, abs(A2['hx'] - base['hx']))
            dB = max(dB, abs(bco(t, A2) - b0))
        D[nm] = (dh, dB)
    return base, D


def check_eig(G, T, pos=(0, 1, 2)):
    vals, vecs = ritz(G, T, pos)
    n = len(pos)
    Gf = np.array([[float(G[a][b]) for b in pos] for a in pos])
    Tf = np.array([[float(T[a][b]) for b in pos] for a in pos])
    ref = sorted(scipy.linalg.eigh(Tf, Gf, eigvals_only=True), reverse=True)
    err = max(abs(float(vals[k]) - ref[k]) / max(1.0, abs(ref[k])) for k in range(n))
    res = mp.mpf(0)
    for k in range(n):
        c = vecs[k]
        for a in pos:
            res = max(res, abs(mp.fsum([(T[a][b] - vals[k] * G[a][b]) * c[j] for j, b in enumerate(pos)])))
        nrm = mp.fsum([c[i] * G[a][b] * c[j] for i, a in enumerate(pos) for j, b in enumerate(pos)])
        res = max(res, abs(nrm - 1))
    return err, res


def eig_line(tag, G, T, fails):
    err, res = check_eig(G, T)
    ok = err <= 1e-12 and res <= mp.mpf('1e-25')
    out('C-EIG %s: eigenvalues vs scipy %.2e, residual %s -> %s' % (tag, err, mp.nstr(res, 3), 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-EIG ' + tag)


def random_pencil():
    rng = np.random.default_rng(20261106)
    A0 = rng.standard_normal((3, 3))
    B0 = rng.standard_normal((3, 3))
    Gr = A0 @ A0.T + 3 * np.eye(3)
    Tr = (B0 + B0.T) / 2
    return [[mp.mpf(float(Gr[i, j])) for j in range(3)] for i in range(3)], [[mp.mpf(float(Tr[i, j])) for j in range(3)] for i in range(3)]


def harmonic_checks(N, E, R3, fails):
    t0 = mp.mpf(0)
    G, T, Ih, Dx = mats(E, t0)
    A = amps(G, T, Ih, Dx, mhat(R3, t0))
    s5, s21 = mp.sqrt(5), mp.sqrt(21)
    rows = [('x_R', A['xR'], X0, 'abs', 1e-9), ('y_R', A['yR'], Y0, 'abs', 1e-9), ('h_x', A['hx'], mp.mpf(0), 'abs', 1e-9),
            ('h_0', A['h0'], (N - 1) * (1 - 2 / s21) / 2, 'rel', 1e-6),
            ('a_0', A['a0'], (N - 1) * (3 / (2 * s21) + 1 / (2 * s5)) / 2, 'rel', 1e-6),
            ('a_x^2', A['ax'] ** 2, (N - 1) * X0 / 40, 'rel', 1e-6),
            ('h_y a_y', A['hy'] * A['ay'], (N - 1) * (5 + s21) * Y0 ** 2 / 28, 'rel', 1e-6)]
    for name, got, want, mode, tol in rows:
        err = abs(got - want) if mode == 'abs' else abs(got / want - 1)
        ok = err <= tol
        out('C-HARM N=%d %s: %s (exact %s) %s err %.2e -> %s' % (N, name, mp.nstr(got, 12), mp.nstr(want, 12), mode, float(err),
                                                                  'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append('C-HARM ' + name)


def b_inf(E, R3, pos=(0, 1, 2), plant=None):
    vals = []
    for ts in T_KA:
        t = mp.mpf(ts)
        G, T, Ih, Dx = mats(E, t)
        mh = mhat(R3, t)
        if plant == 'A':
            l0 = amps(G, T, Ih, Dx, mh, pos)['l0']
            Ih = [l0 * d for d in Dx]
        vals.append(bco(t, amps(G, T, Ih, Dx, mh, pos), 1 if plant == 'OFF' else 2))
    return 2 * vals[1] - vals[0], vals


def check_prop(E, R3, J):
    t = 1 / mp.mpf(J)
    mh = mhat(R3, t)
    E2 = dict((k, (v[0], {'rem': 0.0, 'tail': 0.0, 'ann': 0.0, 'far': 0.0})) for k, v in E.items())
    E2['Ih,1'] = (E['Ih,1'][0], {'rem': 1e-6, 'tail': 0.0, 'ann': 0.0, 'far': 0.0})
    base, D = remainders(E2, t, mh)
    got = mp.fsum([d[0] for d in D.values()])
    G = mats(E, t)[0]
    want = mh * abs(base['cx'][1]) * mp.mpf(1e-6) / (mp.sqrt(G[0][0]) * base['l0'] ** 2)
    return abs(got / want - 1)


def check_ak(N, E):
    refs = []
    clt = load_json(CLT[N])['items']
    refs += [(nm, clt[nm]['ak']) for nm in ['T,%d,%d' % p for p in PE] if nm in E]
    if N == 4:
        gram = load_json('binding_N4_J170.json')['gram']
        refs += [('G,%d,%d' % p, gram['%d,%d' % p]['ak']) for p in PE if ('G,%d,%d' % p) in E]
        b3 = load_json('binding3_N4_J170.json')['items']
        refs += [('Dx,%d' % b, b3['Dx,%d' % b]['ak']) for b in EVEN if ('Dx,%d' % b) in E]
    worst = 0.0
    for nm, ref in refs:
        for a, r in zip(E[nm][0], ref):
            worst = max(worst, abs(a - r) / max(1.0, abs(r)))
    return worst, [nm for nm, _ in refs]


def ak_lines(N, E, fails):
    worst, names = check_ak(N, E)
    ok = worst <= 1e-9
    out('C-AK N=%d (%s against PK10): worst %.2e -> %s' % (N, ' '.join(names), worst, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-AK')
    g00 = ev(E['G,0,0'][0], 1 / mp.mpf(170))
    err = abs(float(g00) - G00_REF[N])
    ok = err <= 1e-8
    out('C-G00 N=%d: G[0,0](170) = %s, PK10 %r, diff %.2e -> %s' % (N, mp.nstr(g00, 12), G00_REF[N], err, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append('C-G00')


def v1_compare(N, E):
    """every entry's a_k against kt_s9b_v1's n<N> output (J = 170 lines for G, T, Ih; J = 1000 lines for Dx), and the largest ratio of a
    J = 300 remainder to its J = 170 remainder over G, T, Ih."""
    ref, rem = {}, {}
    for ln in open(os.path.join(OWN, 'out_kt_s9b_v1_n%d.out' % N)).read().splitlines():
        mt = re.match(r'ENTRY N=%d J=(170|1000) (\S+) ak=\[([^\]]*)\] rem=(\S+) tail=(\S+) ann=(\S+) far=(\S+) r=' % N, ln)
        if not mt:
            continue
        jv, nm = mt.group(1), mt.group(2)
        if (jv == '170') != nm.startswith('Dx'):
            ref[nm] = [float(x) for x in mt.group(3).split(',')]
            if jv == '170':
                rem[nm] = sum(float(mt.group(k)) for k in (4, 5, 6, 7))
    assert len(ref) == 18 and len(rem) == 15, (len(ref), len(rem))
    worst = 0.0
    for nm, ak in ref.items():
        for a, b in zip(E[nm][0], ak):
            worst = max(worst, abs(a - b) / max(1.0, abs(b)))
    worst_r = max(sum(E[nm][1].values()) / rem[nm] for nm in rem)
    return worst, worst_r, len(rem)


def reading(N, J, E, R3):
    t = 1 / mp.mpf(J)
    mh = mhat(R3, t)
    base, D = remainders(E, t, mh)
    conv = abs(base['ax']) / (t * base['xR'] ** 2)
    Rhx = mp.fsum([d[0] for d in D.values()])
    RB = Rhx * conv
    ok = RB <= MARGIN * B_N[N]
    out('READ N=%d J=%g: h_x %s, a_x %s, x_R %s, B(J) %s; R_hx %s; R_B %s against 0.3 B_N = %s -> %s' % (
        N, J, mp.nstr(base['hx'], 8), mp.nstr(base['ax'], 8), mp.nstr(base['xR'], 8), mp.nstr(bco(t, base), 8), mp.nstr(Rhx, 4),
        mp.nstr(RB, 4), mp.nstr(MARGIN * B_N[N], 4), 'PASS' if ok else 'FAIL'))
    split = dict((k, mp.fsum([D[nm][0] for nm in RNAMES if nm.startswith(k + ',')]) * conv) for k in ('Ih', 'T', 'G'))
    top = sorted(RNAMES, key=lambda nm: -D[nm][0])[:3]
    out('SPLIT N=%d J=%g (B units): Ih %s, T %s, G %s; top %s' % (N, J, mp.nstr(split['Ih'], 3), mp.nstr(split['T'], 3),
                                                              mp.nstr(split['G'], 3),
                                                              ', '.join('%s %s' % (nm, mp.nstr(D[nm][0] * conv, 3)) for nm in top)))
    G = mats(E, t)[0]
    raw = sum(E['Ih,1'][1].values()) * mh * abs(base['cx'][1]) / (mp.sqrt(G[0][0]) * base['l0'] ** 2) * conv
    out('INFO N=%d J=%g: R_B from Ih[1] alone %s; full change of B %s' % (N, J, mp.nstr(raw, 3), mp.nstr(mp.fsum([d[1] for d in D.values()]), 3)))
    return RB, ok


def smoke():
    N, J = 3, 300.0
    fails, done = [], False
    Smat, R3 = np.array(load_json(SFILE[N])['S']), load_json(VFILE[N])
    gD, gN = graphs(N)
    w = check_xih(gN)
    out('C-XIH: worst %.2e -> %s' % (w, 'PASS' if w <= 1e-12 else 'FAIL'))
    if w > 1e-12:
        fails.append('C-XIH')
    jd, jn = make_jobs(Smat, R3, True)
    q = max([qmax_of(gD, f) for _, f in jd] + [qmax_of(gN, f) for _, f in jn])
    out('C-QCAP: max Q-degree %d (qcap %d) -> %s' % (q, QCAP, 'PASS' if q <= QCAP else 'FAIL'))
    if q > QCAP:
        fails.append('C-QCAP')
    eig_line('random pencil', *random_pencil(), fails)
    E = {}
    try:
        STAGE[0] = 'prepD'
        need('prepD')
        t0 = cpu()
        prD = make_prep(gD, J, 'KD%d' % N, 'D')
        out('PREP-D N=%d J=%g: %.1f s, rE %.3e, ok %s' % (N, J, cpu() - t0, getattr(prD, 'rE', float('nan')), prD.ok))
        STAGE[0] = 'G,0,0'
        need('entry')
        t0 = cpu()
        E['G,0,0'] = run_entry(prD, 'D', jd[0][1])
        out(entry_line(N, J, 'G,0,0', E['G,0,0'], t0))
        STAGE[0] = 'prepN'
        need('prepN')
        t0 = cpu()
        prN = make_prep(gN, J, 'KN%d' % N, 'N')
        out('PREP-N N=%d J=%g: %.1f s, rE %.3e, ok %s' % (N, J, cpu() - t0, getattr(prN, 'rE', float('nan')), prN.ok))
        STAGE[0] = 'T,0,0'
        need('entry')
        t0 = cpu()
        E['T,0,0'] = run_entry(prN, 'N', jn[0][1])
        out(entry_line(N, J, 'T,0,0', E['T,0,0'], t0))
        ak_lines(N, E, fails)
        STAGE[0] = 'Ih,1'
        need('entry')
        t0 = cpu()
        E['Ih,1'] = run_entry(prN, 'N', [f for nm, f in jn if nm == 'Ih,1'][0])
        out(entry_line(N, J, 'Ih,1', E['Ih,1'], t0))
        a0 = abs(E['Ih,1'][0][0])
        out('C-ZERO-RAW: |a_0(Ih[1])| %.2e -> %s' % (a0, 'PASS' if a0 <= 1e-9 else 'FAIL'))
        if a0 > 1e-9:
            fails.append('C-ZERO-RAW')
        done = True
    except CapStop as e:
        out('CAP-STOP before %s at cpu %.1f s (LIM %d); done %s' % (e, cpu(), LIM, ' '.join(sorted(E)) or '-'))
    out('SMOKE cpu %.1f s; checks %s' % (cpu(), 'PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
    out('VERDICT %s' % ('SMOKE-PASS' if (done and not fails) else ('SMOKE-FAIL' if fails else 'INCOMPLETE (CAP-STOP)')))


def item(N):
    fails, fires = [], []
    Smat, R3 = np.array(load_json(SFILE[N])['S']), load_json(VFILE[N])
    gD, gN = graphs(N)
    w = check_xih(gN)
    out('C-XIH: worst %.2e -> %s' % (w, 'PASS' if w <= 1e-12 else 'FAIL'))
    if w > 1e-12:
        fails.append('C-XIH')
    jd0, jn0 = make_jobs(Smat, R3, True)
    q = max([qmax_of(gD, f) for _, f in jd0] + [qmax_of(gN, f) for _, f in jn0])
    out('C-QCAP: max Q-degree %d (qcap %d) -> %s' % (q, QCAP, 'PASS' if q <= QCAP else 'FAIL'))
    if q > QCAP:
        fails.append('C-QCAP')
    eig_line('random pencil', *random_pencil(), fails)
    EP, RD_, missing = {}, {}, []
    try:
        for ip, J in enumerate(JS):
            E = {}
            jd, jn = make_jobs(Smat, R3, ip == 0)
            missing = [nm for nm, _ in jd + jn]
            STAGE[0] = 'prepD J=%g' % J
            need('prepD')
            t0 = cpu()
            prD = make_prep(gD, J, 'KD%d' % N, 'D')
            out('PREP-D N=%d J=%g: %.1f s, rE %.3e, ok %s' % (N, J, cpu() - t0, getattr(prD, 'rE', float('nan')), prD.ok))
            for nm, facs in jd:
                STAGE[0] = '%s J=%g' % (nm, J)
                need('entry')
                t0 = cpu()
                E[nm] = run_entry(prD, 'D', facs)
                missing.remove(nm)
                out(entry_line(N, J, nm, E[nm], t0))
            prD = None
            STAGE[0] = 'prepN J=%g' % J
            need('prepN')
            t0 = cpu()
            prN = make_prep(gN, J, 'KN%d' % N, 'N')
            out('PREP-N N=%d J=%g: %.1f s, rE %.3e, ok %s' % (N, J, cpu() - t0, getattr(prN, 'rE', float('nan')), prN.ok))
            for nm, facs in jn:
                STAGE[0] = '%s J=%g' % (nm, J)
                need('entry')
                t0 = cpu()
                E[nm] = run_entry(prN, 'N', facs)
                missing.remove(nm)
                out(entry_line(N, J, nm, E[nm], t0))
            prN = None
            if ip > 0:
                for b in EVEN:
                    E['Dx,%d' % b] = EP[0]['Dx,%d' % b]
            EP[ip] = E
            STAGE[0] = 'readings J=%g' % J
            G, T = mats(E, 1 / mp.mpf(J))[:2]
            eig_line('N=%d J=%g pencil' % (N, J), G, T, fails)
            pr_err = check_prop(E, R3, J)
            out('C-PROP N=%d J=%g: %.2e -> %s' % (N, J, float(pr_err), 'PASS' if pr_err <= 1e-9 else 'FAIL'))
            if pr_err > 1e-9:
                fails.append('C-PROP J=%g' % J)
            if ip == 0:
                ak_lines(N, E, fails)
                harmonic_checks(N, E, R3, fails)
                binf, bv = b_inf(E, R3)
                rel = abs(binf / B_N[N] - 1)
                out('C-KA N=%d: B_inf %s (B(1e-5) %s, B(5e-6) %s) against B_N %r: rel %.2e -> %s' % (
                    N, mp.nstr(binf, 8), mp.nstr(bv[0], 8), mp.nstr(bv[1], 8), B_N[N], float(rel), 'PASS' if rel <= TOL_KA else 'FAIL'))
                if rel > TOL_KA:
                    fails.append('C-KA')
                for pl in ('A', 'OFF'):
                    pb, _ = b_inf(E, R3, plant=pl)
                    prel = abs(pb / B_N[N] - 1)
                    fired = prel > TOL_KA
                    out('PLANT-%s N=%d: B_inf %s, rel %.2e -> %s' % (pl, N, mp.nstr(pb, 8), float(prel), 'FIRES' if fired else 'DOES NOT FIRE'))
                    if not fired:
                        fires.append('PLANT-' + pl)
                b2, _ = b_inf(E, R3, pos=(0, 1))
                out('PLANT-M N=%d (info): B_inf on {psi-hat, e1} %s, change %s' % (N, mp.nstr(b2, 8), mp.nstr(b2 / binf - 1, 4)))
                for Jc in (1000.0, 300.0, 170.0):
                    tc = 1 / mp.mpf(Jc)
                    Gc, Tc, Ihc, Dxc = mats(E, tc)
                    out('INFO N=%d: B(%g) = %s (central, exact a_k)' % (N, Jc, mp.nstr(bco(tc, amps(Gc, Tc, Ihc, Dxc, mhat(R3, tc))), 8)))
            RD_[J] = reading(N, J, E, R3)
        missing = []
    except CapStop as e:
        out('CAP-STOP before %s at cpu %.1f s (LIM %d); missing at that J: %s' % (e, cpu(), LIM, ' '.join(missing) or '-'))
    if len(EP) == 1:
        worst, worst_r, nr = v1_compare(N, EP[0])
        out('C-AKV1 N=%d: a_k against kt_s9b_v1 (J = 170 lines; Dx at J = 1000): worst %.2e -> %s' % (N, worst, 'PASS' if worst <= 1e-10 else 'FAIL'))
        if worst > 1e-10:
            fails.append('C-AKV1')
        out('C-J300 N=%d: largest ratio of a J = 300 remainder to its J = 170 remainder over the %d G, T, Ih entries %.4e -> %s' % (
            N, nr, worst_r, 'PASS' if worst_r <= 1.0 else 'FAIL'))
        if worst_r > 1.0:
            fails.append('C-J300')
    lim_b = MARGIN * B_N[N]
    complete = (len(EP) == 1)
    out('S9B300 N=%d (info): R_B(300) with one-at-a-time J = 300 remainders %s; 0.3 B_N = %s' % (
        N, mp.nstr(RD_[300.0][0], 4) if 300.0 in RD_ else '-', mp.nstr(lim_b, 4)))
    why = fails + ['%s did not fire' % x for x in fires] + ([] if complete else ['INCOMPLETE'])
    out('ITEM %s cpu %.1f s' % (MODE, cpu()))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))


def main():
    try:
        if MODE == 'smoke':
            smoke()
        else:
            item(int(MODE[1]))
    except Exception as e:
        traceback.print_exc()
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        out('VERDICT INVALID (ERROR)')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
