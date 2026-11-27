#!/usr/bin/env python3
"""kt_s8rf_v1.py -- pk11 (code/pk11/). P2-12 step 3 (inside step 3's cap): route 0's quantity for the
near-end joint classes D3 (t_i, bb_{i+1}; window of 3 columns), D4 (t_i, b_i) and D4M (t_i, b_{i+1}; 2 columns), the reflected moment
||Q0 X u||^2 = Cov(X_c, theta X_c), X_c = (xi_e - c_e)(xi_f - c_f) (the review, sects. 2.2-4: reflection
positivity in transfer-matrix form; pX^2 = E[X_c^2] - Cov^2 is only its Cauchy-Schwarz bound). FLOAT DATA, not a certificate.
Per item (n4 | n3) three parts:
H. C-JOINT-H (t = 0, the harmonic strip, numpy): the model (3 rows, unit conductance on every horizontal and on the verticals TM and
   MB, 241 columns, the window's left outer column c0 = 120; xi_b = |A_b|^2 / 2 over n = N - 1 components, g the transfer currents).
   Planes: L0 (the window's left outer column), LH (half a step out, c0 - 1/2: S8's convention, pinned below), L1 (one column out); R0,
   RH, R1 the same on the right (X^dagger u). Per class and plane:
   - the reflected formula: the Wick split (0 quanta C12 C34; 2 quanta n (g12 g23 g34 g41 + g12 g24 g43 g31); 4 quanta C13 C24 +
     C14 C23 + n g13 g32 g24 g41; C_ij = n g_ij^2 / 2) on e, f, theta e, theta f; ||Q0 X u||^2 = 2q + 4q;
   - C-WICK: the same number from my general engine (set partitions; joint cumulant of bond forms kappa(B) = (n/2) x the sum over the
     cyclic orders through B's first element of the product of g along the cycle), relative 1e-12 of 0q + 2q + 4q;
   - from the chain's harmonic vectors: S8's ten trial states s_a (ts_N*_z9sym_v1: a >= 1 the BASIS9 polynomial S[.][a] of a column,
     a = 0 the vacuum, 1 at t = 0). At a site plane on column c the vectors s_a(c) (Gram Cov(s_a(c), s_b(c))); at a half-step plane the
     chain's own vectors w_a = (T/lam_0)^1/2 s_a (Gram <Q0 w_a, Q0 w_b> = Cov(s_a(c), s_b(c+1)), S8's g entries; <w_a, Q0 X u> =
     Cov(s_a(c'), X_c), c' the column just outside). The in-span part of Q0 X u, v^T G^-1 v, over W3 (states 0..3), B4, B5, B6 (route
     (b)'s sets) and all ten. C-SPAN10: the ten-state part equals the reflected formula at every plane, relative 1e-7 (at t = 0 X u lies
     in the span: E[X_c | column] is an O(n)-invariant polynomial of degree <= 4 in the column's differences, the review, sect. 2.2 (i));
     INFO: W3's part against 2q (states 1..3 are the 2-quanta eigenvectors);
   - C-JREF: L0, L1, R0, R1 against the printed values (out_chk_joint_reflect_v1.txt 03b1d581): the total relative 1e-4, 2q and 4q
     relative 2e-3 (printed to 5 and 4 digits);
   - C-CS-H: every reflected value <= pX^2 = E[X_c^2] - Cov^2 (t = 0);
   - C-LOOP-H: theta := identity returns the window's closed form E[X_c^2] (C-LOOP's form), relative 1e-12; PLANT-THETA: that number
     must differ from the reflected L0 value (relative > 1e-3).
   Pins to the chain (S8's float reference pk03 m3ref_v1_10 V3D, the a_0 of its z9sym entries on graph D):
   - C-GRAM-H: my E[s_a(c) s_b(c+1)] against g,a,b / g,0,0 for every a <= b <= 9, |difference| <= 1e-8 max(1, |g|);
   - C-PIN-H (plane pin): the same reflected formula for S8's single vertical insertion xi_TM, Cov(xi_TM(c), xi_TM(theta c)) with theta
     the half-step reflection, against the chain's harmonic ||Q0 A_X u||^2 = pnorm2 = DYY/g00 - (DY,0/g00)^2 (s8core chain()), relative
     1e-9; PLANT-PIN: the site reflection (Var xi_TM) must miss it (relative > 1e-3);
   - C-PW-H: my W3 in-span part for that insertion against the chain's |p_W|^2 at t = 0 (s8core's Bt from DY,a and g,a,b), relative
     1e-8; C-SPAN10 also for it (the ten-state part = pnorm2).
F. FLOAT at J = 300 (amom2b, as pk15's kt_p2_14f_v1 window moments M_ij): the window doubled about its left outer column (L0, 2w - 1
   columns of the bulk strip, the single eigen trick p on both outer columns). D4: V 9, pairs both outer columns' verticals, HT(c0 - 1),
   HT(c0), MB(c0) (F 18); D4M: V 9, F 17. The L0 value bounds every plane further out, S8's LH among them (a transfer step fixes u and
   contracts u-perp). By the mirror, D4's right side is D4M's left side and D4M's right side is D4's (D3 is its own after F).
   Entries: every monomial of X_c theta X_c (D4: xi_e^a xi_te^b xi_f^k, a, b <= 1, k <= 2, theta f = f on the plane; D4M: the 16 subsets
   of e, f, theta e, theta f) at K = 2 (D 8, as pk15's M_ij, within the step's 0.05 core-h); ratios to the empty entry remove the
   trick's normalization; c_e, c_f from the same graph; Cov(X_c, theta X_c) = E[X_c theta X_c] - E[X_c]^2 as a truncated series in
   t = 1/J (a_0..a_2), evaluated at the scan pieces' J_lo (the export's grid). D3 (V 15) is probed only (graph, series degrees, packing;
   no moment): F 25, so (D+1)^25 < 9e18 allows D <= 4, the t^0 term.
   Gates: C-GRAPH (V, edges, F), C-PACK, C-H0 (a_0 against part H's L0 value, relative 1e-7), C-SAME-W (the window's own Cov_w =
   E[xi_e xi_f] - c_e c_f, a_0..a_2, against pk15's SERIES line of the class (graph DT, out_kt_p2_14f_v1_n<N>.out), relative 1e-7
   per coefficient; m_e and m_f against its M4_10 / M4_00 and M4_01 / M4_00 entries, relative 1e-7), C-SYM-F (mirror-image entries
   equal, relative 1e-10), C-POS-F and C-CS-F (0 < Cov(X_c, theta X_c) <= pX_hi^2 at every scan piece); PLANT-H0 (C-H0 against the
   L1 value must fail). INFO: the series terms, the values-first evaluation (each entry at t first: an O(t^3) indicator), rho =
   sqrt(Cov(X_c, theta X_c)) / pX_hi per piece.
S. The screen re-read from pk15's TABLE_P2_12_JOINT_SCREEN_SPRIME_ROUTEA_v1.tsv (6bc0ff4d; each class at its worst piece; terms
   a..e from my TABLE_P2_12_JOINT_SCREEN_v1 9aea4fc5, Lemma S' normX, route A): a' = a rho_L, b' = b rho_R, rho at the row's piece (D4:
   rho_L from D4-L0, rho_R from D4M-L0; D4M the reverse; D3 both from part H's exact t = 0 L0 value, flagged H: no J = 300 value exists
   on amom2b). PLAIN R = a' + b' + (c + d + e) r and ROUTE_A (d_L = 0) R_A = b' + (d + e) r + trick, r = normX_S / normX_old; headroom
   Cov/R, need (the normX at which R = Cov/2), mark and best as the table's (theta-cut targets read from its header; the trick from the
   header's formula, pk02's piece-61 estimate times 1 at N4 piece 61 and 1/0.5081 at N3 piece 0, since the table prints it to 3
   digits). C-TSV: with rho = 1 the re-read reproduces the table's R_P, R_A (relative 1e-3) and marks, and the formula's trick its
   printed one (relative 5e-3). For D3 rows the largest common rho that keeps the new best mark (INFO).
Writes pk11/out/s8hf_v1/out_kt_s8rf_v1_<item>.out and TABLE_P2_12_JOINT_SCREEN_ROUTE0_kt_s8rf_v1_<item>.tsv (new files).
Run (one job at a time; LIM 5..300 s CPU, hard LIM + 5; AS 8 GiB):
  D=/mnt/g2/release/root/code/pk11; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_s8rf_v1.py n4 LIM > $D/out/s8hf_v1/kt_s8rf_v1_n4.log 2>&1   (then n3)"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, hashlib, json, re, math, traceback
from itertools import permutations

ITEMS = {'n4': 4, 'n3': 3}
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: kt_s8rf_v1.py n4|n3 LIM   (LIM = RLIMIT_CPU soft limit in s, 5..300, hard LIM + 5)')
    sys.exit(2)
ITEM = sys.argv[1]
N = ITEMS[ITEM]
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (5 <= LIM <= 300):
    print('bad LIM %r (need 5 <= LIM <= 300)' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 2 ** 20, 10 * 2 ** 20))

CODEDIR = '/mnt/g2/release/root/code'
SCR = CODEDIR + '/pk10/scripts'
OWN = CODEDIR + '/pk11'
OUTD = OWN + '/out'
HFD = OUTD + '/s8hf_v1'
M3O = CODEDIR + '/pk03/out'
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(HFD, 'out_%s_%s.out' % (LABEL, ITEM))
TSV_PATH = os.path.join(HFD, 'TABLE_P2_12_JOINT_SCREEN_ROUTE0_%s_%s.tsv' % (LABEL, ITEM))
for p_ in (OUT_PATH, TSV_PATH):
    if not (os.path.isdir(HFD) and os.path.realpath(os.path.dirname(p_)) == os.path.realpath(HFD)
            and os.path.realpath(HFD).startswith(os.path.realpath(OUTD) + os.sep)):
        print('output directory check failed for %s' % p_)
        sys.exit(2)
FH = open(OUT_PATH, 'x')


def cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def out(line):
    FH.write(line + '\n')
    FH.flush()


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


EXPORT = CODEDIR + '/pk15/out/export_p2_14_joint_float_v1_2.kv'
TSV_IN = CODEDIR + '/pk15/TABLE_P2_12_JOINT_SCREEN_SPRIME_ROUTEA_v1.tsv'
HZOUT = {4: CODEDIR + '/pk15/out/out_kt_p2_14f_v1_n4.out', 3: CODEDIR + '/pk15/out/out_kt_p2_14f_v1_n3.out'}
RHREF = CODEDIR + '/rv01/out_chk_joint_reflect_v1.txt'
SFILE = {4: OUTD + '/ts_N4_J170_D_S_z9sym_v1.json', 3: OUTD + '/ts_N3_S_z9sym_v1.json'}
VFILE = {4: OUTD + '/vacres_K3_N4_sym_v1.json', 3: OUTD + '/vacres_K3_N3_sym_v1.json'}
V3D = {4: [M3O + '/m3ref_v1_10_V3D.4.0-32_z9sym.out', M3O + '/m3ref_v1_10_V3D.4.33-65_z9sym.out'],
       3: [M3O + '/m3ref_v1_10_V3D.3.all_z9sym.out']}
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
    EXPORT: '39d08be920a031ac33aeab936f63aa743611578e94e342e83b72a030abcbfc3e',
    TSV_IN: '32f3884037d297f154c8330bed8551aaeea4927790e04603bed31db8f8e22f2c',
    HZOUT[4]: 'c7c6f20bc9aa9f54b09855085c72102d1018896b44a2ea71c9af4a36542808cd',
    HZOUT[3]: 'ed3a37809075509a607f07feeeb5d8aa687336a4574704719e46561d7764d7f3',
    RHREF: '03b1d5816b8f4a1fd6fd6ada178d7167b5a5f0fb5bbb8fea2d453a67b6641ff5',
    SFILE[4]: 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    SFILE[3]: 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    VFILE[4]: 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    VFILE[3]: 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    V3D[4][0]: '7540647500f6c4368ad47967308b872224e08cbcaa645a1cf20acb469d9c5307',
    V3D[4][1]: '0b4c99038b245432b71e66e0ad88903b374f68b3d9b5a6521049b4c5d2098362',
    V3D[3][0]: '8a045f0bb2579e91f5a937761bacf0b54af6632b6e2a5b5307d3a652af74bc9a',
}
out('%s sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (LABEL, sha_file(os.path.abspath(__file__)), ITEM, LIM, LIM, LIM + 5))
_bad = ['%s %s' % (p, sha_file(p)) for p in sorted(PINS) if sha_file(p) != PINS[p]]
out('C-HASH %s (%d files)%s' % ('PASS' if not _bad else 'FAIL', len(PINS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
import numpy as np
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
K = 2
n = N - 1
fails = []


def gate(name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


def rel(x, y):
    return abs(x - y) / max(abs(y), 1e-300)


# ---- part H: the harmonic strip (vertex 3 c + row; row 0 T, 1 M, 2 B)
NLONG, C0 = 241, 120
WX = {'D3': 3, 'D4': 2, 'D4M': 2}
BASIS9 = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]
SETS = (('W3', [1, 2, 3]), ('B4', [1, 2, 3, 4]), ('B5', [1, 2, 3, 4, 5]), ('B6', [1, 2, 3, 4, 5, 6]), ('ALL', list(range(1, 10))))


def lap_grid(nc):
    V = 3 * nc
    Lm = np.zeros((V, V))

    def add(a, b):
        Lm[a, a] += 1.0
        Lm[b, b] += 1.0
        Lm[a, b] -= 1.0
        Lm[b, a] -= 1.0
    for c in range(nc):
        add(3 * c, 3 * c + 1)
        add(3 * c + 1, 3 * c + 2)
        if c < nc - 1:
            for r in range(3):
                add(3 * c + r, 3 * c + 3 + r)
    G = np.zeros((V, V))
    G[1:, 1:] = np.linalg.inv(Lm[1:, 1:])
    return G


def bpair(b):
    kind, c = b
    return {'HT': (3 * c, 3 * c + 3), 'HB': (3 * c + 2, 3 * c + 5), 'MB': (3 * c + 1, 3 * c + 2), 'TM': (3 * c, 3 * c + 1),
            'TB': (3 * c, 3 * c + 2)}[kind]


def Yp(p, q):
    a, b = p
    c, d = q
    return GH[a, c] - GH[a, d] - GH[b, c] + GH[b, d]


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


def kappa(block, gm):
    """the joint cumulant of the bond forms xi_i = |A_i|^2 / 2 (n components) indexed by block: (n/2) x the sum over the cyclic orders
    through block[0] of the product of g along the cycle (one element: (n/2) g_ii, the mean)."""
    b0, rest = block[0], block[1:]
    terms = []
    for perm in permutations(rest):
        cyc = (b0,) + perm
        pr = 1.0
        for i in range(len(cyc)):
            pr *= gm[cyc[i]][cyc[(i + 1) % len(cyc)]]
        terms.append(pr)
    return n / 2.0 * math.fsum(terms)


def moment(prs, centred=False):
    """E[prod xi_p] over the list of vertex pairs prs (repeats allowed); centred: E[prod (xi_p - E xi_p)] (no singleton blocks)."""
    m = len(prs)
    if m == 0:
        return 1.0
    gm = [[Yp(p, q) for q in prs] for p in prs]
    terms = []
    for part in set_partitions(list(range(m))):
        if centred and any(len(B) == 1 for B in part):
            continue
        pr = 1.0
        for B in part:
            pr *= kappa(B, gm)
        terms.append(pr)
    return math.fsum(terms)


def split(bs, cyc4=True):
    """the chk_joint_reflect_v1 split (ae15f00c l.106-114) on the bonds bs = [e, f, theta e, theta f]."""
    g = [[Yp(bpair(bs[i]), bpair(bs[j])) for j in range(4)] for i in range(4)]

    def C(i, j):
        return n * g[i][j] ** 2 / 2.0
    q0 = C(0, 1) * C(2, 3)
    q2 = n * (g[0][1] * g[1][2] * g[2][3] * g[3][0] + g[0][1] * g[1][3] * g[3][2] * g[2][0])
    q4 = C(0, 2) * C(1, 3) + C(0, 3) * C(1, 2) + (n * g[0][2] * g[2][1] * g[1][3] * g[3][0] if cyc4 else 0.0)
    return q0, q2, q4


def window_E2(e, f):
    a, b, g = Yp(bpair(e), bpair(e)), Yp(bpair(f), bpair(f)), Yp(bpair(e), bpair(f))
    return n * n * a * a * b * b / 4.0 + 2 * n * g * g * a * b + (n * n / 2.0 + n) * g ** 4


def refl(bond, plane):
    """bond (kind, column) mirrored about ('site', c), the column c, or ('half', c), the midpoint c + 1/2 (x -> 2c + 1 - x)."""
    kind, c = bond
    pk, pc = plane
    horiz = kind in ('HT', 'HB')
    if pk == 'site':
        return (kind, 2 * pc - c - 1) if horiz else (kind, 2 * pc - c)
    return (kind, 2 * pc - c) if horiz else (kind, 2 * pc + 1 - c)


def bonds_of(fam, c0):
    if fam == 'D3':
        return ('HT', c0), ('HB', c0 + 1)
    if fam == 'D4':
        return ('HT', c0), ('MB', c0)
    return ('HT', c0), ('MB', c0 + 1)


def planes(c0, cR):
    """(name, theta plane, trial column, Gram kind): site planes carry s_a on the plane's column; half-step planes the chain's w_a, whose
    components are read on the column just outside."""
    return [('L0', ('site', c0), c0, 'same'), ('LH', ('half', c0 - 1), c0 - 1, 'adj'), ('L1', ('site', c0 - 1), c0 - 1, 'same'),
            ('R0', ('site', cR), cR, 'same'), ('RH', ('half', cR), cR + 1, 'adj'), ('R1', ('site', cR + 1), cR + 1, 'same')]


def col_monos(c):
    prs = [bpair(('TM', c)), bpair(('MB', c)), bpair(('TB', c))]
    return [[]] + [[prs[i] for i in mo] for mo in BASIS9]


def covmono(ct, prs_x, cen):
    """Cov(mono_r(column ct), X) for the ten monomials, X = prod over prs_x of (xi_p - cen_p) (cen: the bulk means)."""
    res = []
    k = len(prs_x)
    subsets = [[j for j in range(k) if (m >> j) & 1] for m in range(2 ** k)]

    def ex_with(base):
        return math.fsum(moment(base + [prs_x[j] for j in sub]) * math.prod(-cen[j] for j in range(k) if j not in sub) for sub in subsets)
    EX = ex_with([])
    for mo in col_monos(ct):
        res.append(ex_with(mo) - moment(mo) * EX)
    return np.array(res)


def gram(kind):
    """the ten states' Q0 Gram, Cov(s_a(c), s_b(c)) or Cov(s_a(c), s_b(c+1)), and the raw Gram E[s_a(c) s_b(c')]; c a bulk column."""
    gc = C0 - 40
    ms, mt = col_monos(gc), col_monos(gc if kind == 'same' else gc + 1)
    raw = np.array([[moment(ms[r] + mt[s]) for s in range(10)] for r in range(10)])
    mean_s = np.array([moment(ms[r]) for r in range(10)])
    mean_t = np.array([moment(mt[s]) for s in range(10)])
    G_ = SX.T @ raw @ SX
    return G_ - np.outer(SX.T @ mean_s, SX.T @ mean_t), G_


def inspan(v, Gq, idx):
    vs = v[idx]
    return float(vs @ np.linalg.solve(Gq[np.ix_(idx, idx)], vs))


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


# ---- part F helpers (kt_s8h_mk_v1_3's entry engine)
def ej_series(g, order):
    Hs = _r3.Model3(g, 3, []).H(3)
    H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
    H1sq = pmul(H1, H1)
    full = [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
    return full[:order + 1]


def fi_series(g, facs, order):
    scal, groups = group_factors(facs)
    gser = [_r3.Model3(g, 3, gf).Fser(3).c for gf in groups]
    return series_product(gser, scal, 3)[:order + 1]


def dn(Fi, Ej, KK):
    return max(_deg(Fi[i]) + _deg(Ej[k - i]) for k in range(KK + 1) for i in range(k + 1) if Fi[i])


def salg(KS):
    def smul(a, b):
        return [math.fsum(a[i] * b[k - i] for i in range(k + 1)) for k in range(KS)]

    def sinv(a):
        b = [1.0 / a[0]]
        for k in range(1, KS):
            b.append(-math.fsum(a[i] * b[k - i] for i in range(1, k + 1)) / a[0])
        return b

    def sadd(*xs):
        return [math.fsum(x[k] for x in xs) for k in range(KS)]

    def ssc(a, c):
        return [c * x for x in a]
    return smul, sinv, sadd, ssc


def cov_d4(R, KS):
    """D4-L0 (theta f = f): E[(xi_e - c_e)(xi_te - c_e)(xi_f - c_f)^2] - E[X_c]^2 and E[X_c], from the ratios R[Eabk]."""
    smul, sinv, sadd, ssc = salg(KS)
    one = [1.0] + [0.0] * (KS - 1)
    ce, cf = R['E100'], R['E001']
    terms = []
    for a in (0, 1):
        for b in (0, 1):
            for k in (0, 1, 2):
                co = one
                for _ in range(2 - a - b):
                    co = smul(co, ssc(ce, -1.0))
                for _ in range(2 - k):
                    co = smul(co, ssc(cf, -1.0))
                terms.append(smul(ssc(co, float(math.comb(2, k))), R['E%d%d%d' % (a, b, k)]))
    exx = sadd(*terms)
    ex = sadd(R['E101'], ssc(smul(ce, cf), -1.0))
    return sadd(exx, ssc(smul(ex, ex), -1.0)), ex, ce, cf


def cov_d4m(R, KS):
    """D4M-L0: E[(xi_e - c_e)(xi_f - c_f)(xi_te - c_e)(xi_tf - c_f)] - E[X_c]^2 and E[X_c], from the subset ratios R[Sbbbb]."""
    smul, sinv, sadd, ssc = salg(KS)
    one = [1.0] + [0.0] * (KS - 1)
    ce, cf = R['S1000'], R['S0100']
    cv = (ce, cf, ce, cf)
    terms = []
    for m in range(16):
        bits = tuple((m >> i) & 1 for i in range(4))
        co = one
        for i in range(4):
            if not bits[i]:
                co = smul(co, ssc(cv[i], -1.0))
        terms.append(smul(co, R['S%d%d%d%d' % bits]))
    exx = sadd(*terms)
    ex = sadd(R['S1100'], ssc(smul(ce, cf), -1.0))
    return sadd(exx, ssc(smul(ex, ex), -1.0)), ex, ce, cf


def horner(a, t):
    return math.fsum(c * t ** k for k, c in enumerate(a))


RANK = {'pass': 3, 'theta-cut': 2, 'beyond-theta': 1, 'none': 0}


def reading(cov, free, slope, nS, target):
    """pk15's table rule: R = free + slope normX_S; pass if Cov/R >= 2; else need = (Cov/2 - free)/slope (none if <= 0; - if normX
    does not enter), theta-cut if need >= the theta-cut target, beyond-theta below it."""
    R = free + slope * nS
    h = cov / R if R > 0 else float('inf')
    if slope <= 0:
        need = '-'
    elif cov / 2.0 - free <= 0:
        need = 'none'
    else:
        need = (cov / 2.0 - free) / slope
    if h >= 2.0:
        mk = 'pass'
    elif not isinstance(need, float):
        mk = 'none'
    else:
        mk = 'theta-cut' if need >= target else 'beyond-theta'
    return R, h, need, mk


def fmt_need(x):
    return x if isinstance(x, str) else '%.4g' % x


try:
    S = json.load(open(SFILE[N]))['S']
    R3 = json.load(open(VFILE[N]))
    SX = np.array([[(1.0 if r == 0 else 0.0) if a == 0 else float(S[r][a]) for a in range(10)] for r in range(10)])
    VD = ref_ak(V3D[N])
    GH = lap_grid(NLONG)
    t0 = cpu()
    out('PART H (t = 0): harmonic strip %d columns, n = %d, window left outer column c0 = %d' % (NLONG, n, C0))
    GQ, GRAW = {}, {}
    for kind in ('same', 'adj'):
        GQ[kind], GRAW[kind] = gram(kind)
    gv = lambda a, b: VD['g,%d,%d' % (min(a, b), max(a, b))][0]
    g00 = gv(0, 0)
    worst = max(abs(GRAW['adj'][a, b] - gv(a, b) / g00) / max(1.0, abs(gv(a, b) / g00)) for a in range(10) for b in range(a, 10))
    out('C-GRAM-H: my E[s_a(c) s_b(c+1)] against S8\'s g,a,b / g,0,0 (V3D a_0, 55 entries): largest |difference| / max(1, |g|) %.2e '
        '(tolerance 1e-8) -> %s' % (worst, gate('C-GRAM-H', worst <= 1e-8)))
    # plane pin: S8's single vertical insertion xi_TM
    pv = bpair(('TM', C0))
    pn2 = VD['DYY'][0] / g00 - (VD['DY,0'][0] / g00) ** 2
    vh = moment([pv, bpair(refl(('TM', C0), ('half', C0 - 1)))], centred=True)
    vs = moment([pv, bpair(refl(('TM', C0), ('site', C0)))], centred=True)
    out('C-PIN-H: the reflected formula for xi_TM with theta the half-step reflection %.12e against the chain\'s harmonic pnorm2 = '
        'DYY/g00 - (DY,0/g00)^2 %.12e (relative %.2e, tolerance 1e-9) -> %s' % (
            vh, pn2, rel(vh, pn2), gate('C-PIN-H', rel(vh, pn2) <= 1e-9)))
    fires = rel(vs, pn2) > 1e-3
    out('PLANT-PIN: the site reflection (Var xi_TM) %.12e against pnorm2: relative %.2e -> %s' % (vs, rel(vs, pn2), 'FIRES' if fires else
                                                                                                 'DOES NOT FIRE'))
    if not fires:
        fails.append('PLANT-PIN')
    vv = SX.T @ covmono(C0 - 1, [pv], [moment([pv])])
    G2c = [[gv(a, b) / g00 - gv(a, 0) * gv(b, 0) / g00 ** 2 for b in (1, 2, 3)] for a in (1, 2, 3)]
    vc = [VD['DY,%d' % a][0] / g00 - VD['DY,0'][0] / g00 * gv(a, 0) / g00 for a in (1, 2, 3)]
    pw2 = float(np.array(vc) @ np.linalg.solve(np.array(G2c), np.array(vc)))
    mw3 = inspan(vv, GQ['adj'], [1, 2, 3])
    out('C-PW-H: my W3 in-span part for xi_TM at the half-step plane %.12e against the chain\'s |p_W|^2 at t = 0 (s8core Bt from DY,a, '
        'g,a,b) %.12e (relative %.2e, tolerance 1e-8) -> %s' % (mw3, pw2, rel(mw3, pw2), gate('C-PW-H', rel(mw3, pw2) <= 1e-8)))
    m10 = inspan(vv, GQ['adj'], list(range(1, 10)))
    out('C-SPAN10 xi_TM: the ten-state part %.12e against pnorm2 %.12e (relative %.2e, tolerance 1e-7) -> %s' % (
        m10, pn2, rel(m10, pn2), gate('C-SPAN10', rel(m10, pn2) <= 1e-7)))
    # the joint classes
    refs = {}
    for ln in open(RHREF).read().split('\n'):
        mm = re.match(r'^N(\d) (D3|D4|D4M) (L0|L1|R0|R1): \|Q0 X u\|\^2 (\S+) \(2q (\S+), 4q (\S+), 0q', ln)
        if mm and int(mm.group(1)) == N:
            refs[(mm.group(2), mm.group(3))] = tuple(float(mm.group(k)) for k in (4, 5, 6))
    if len(refs) != 12:
        raise ValueError('review reference lines for N%d: %d (want 12)' % (N, len(refs)))
    HV = {}
    for fam in ('D3', 'D4', 'D4M'):
        e, f = bonds_of(fam, C0)
        cR = C0 + WX[fam] - 1
        pe, pf = bpair(e), bpair(f)
        cov = n * Yp(pe, pf) ** 2 / 2.0
        E2 = window_E2(e, f)
        pX2 = E2 - cov * cov
        l0, l2, l4 = split([e, f, e, f])
        okl = rel(l0 + l2 + l4, E2) <= 1e-12
        out('C-LOOP-H N%d %s: theta := identity gives %.12e against the window closed form E[X_c^2] %.12e (relative %.1e) -> %s' % (
            N, fam, l0 + l2 + l4, E2, rel(l0 + l2 + l4, E2), gate('C-LOOP-H', okl)))
        cen = [moment([pe]), moment([pf])]
        for nm, pl, ct, gk in planes(C0, cR):
            te, tf = refl(e, pl), refl(f, pl)
            q0, q2, q4 = split([e, f, te, tf])
            val = q2 + q4
            cg = moment([pe, pf, bpair(te), bpair(tf)], centred=True) - (n * Yp(pe, pf) ** 2 / 2.0) ** 2
            okw = abs(cg - val) <= 1e-12 * (abs(q0) + abs(q2) + abs(q4))
            v = SX.T @ covmono(ct, [pe, pf], cen)
            isp = {nm_: inspan(v, GQ[gk], idx) for nm_, idx in SETS}
            ok10 = rel(isp['ALL'], val) <= 1e-7
            okcs = val <= pX2
            HV[(fam, nm)] = val
            out('JH N%d %s %s: ||Q0 X u||^2 %.6e (0q %.4e, 2q %.4e, 4q %.4e) | general engine relative %.1e (C-WICK %s) | in-span W3 %.4e '
                'B4 %.4e B5 %.4e B6 %.4e ALL %.6e (C-SPAN10 relative %.1e %s; W3 / 2q - 1 = %.1e) | rho = sqrt / pX(t=0) %.5f '
                '(C-CS-H %s)' % (N, fam, nm, val, q0, q2, q4, abs(cg - val) / max(val, 1e-300), gate('C-WICK', okw), isp['W3'],
                                 isp['B4'], isp['B5'], isp['B6'], isp['ALL'], rel(isp['ALL'], val), gate('C-SPAN10', ok10),
                                 isp['W3'] / q2 - 1.0 if q2 else float('nan'), math.sqrt(max(val, 0.0) / pX2), gate('C-CS-H', okcs)))
            if (fam, nm) in refs:
                rt, r2, r4 = refs[(fam, nm)]
                okr = rel(val, rt) <= 1e-4 and rel(q2, r2) <= 2e-3 and rel(q4, r4) <= 2e-3
                out('C-JREF N%d %s %s: against the review %.4e (2q %.3e, 4q %.3e): relative %.1e, %.1e, %.1e -> %s' % (
                    N, fam, nm, rt, r2, r4, rel(val, rt), rel(q2, r2), rel(q4, r4), gate('C-JREF', okr)))
        fires = rel(E2, HV[(fam, 'L0')]) > 1e-3
        out('PLANT-THETA N%d %s: theta := identity (%.6e) against the reflected L0 value (%.6e) -> %s' % (
            N, fam, E2, HV[(fam, 'L0')], 'FIRES' if fires else 'DOES NOT FIRE'))
        if not fires:
            fails.append('PLANT-THETA')
        out('INFO JH N%d %s: pX^2(t=0) %.6e; S8\'s plane (LH) against L0: ratio of ||Q0 X u|| %.4f (L1 %.4f); right side LH / R0 %.4f' % (
            N, fam, pX2, math.sqrt(HV[(fam, 'LH')] / HV[(fam, 'L0')]), math.sqrt(HV[(fam, 'L1')] / HV[(fam, 'L0')]),
            math.sqrt(HV[(fam, 'RH')] / HV[(fam, 'R0')])))
    out('PART H cpu %.1f s' % (cpu() - t0))

    # ---- part F: the doubled windows at J = 300
    t0 = cpu()

    def dwin(ncols, pairs):
        V, E = strip_graph(ncols, (A_EX, B_EX))
        return Graph(V, E, [tuple(p) for p in pairs], N=N), len(E)

    def pfac(col):
        return ('p', (3 * col, 3 * col + 1, 3 * col + 2), R3['q1'], R3['q2'], R3['q3'])

    def xfac(pr):
        return ('xi', (pr[0], pr[1], pr[1]), 0.0, [1.0] + [0.0] * 8)

    def vert(c):
        return [(3 * c, 3 * c + 1), (3 * c + 1, 3 * c + 2), (3 * c, 3 * c + 2)]

    def run_graph(name, g, ne, shape, sets):
        t1 = cpu()
        Ej = ej_series(g, K)
        Fis = {k: fi_series(g, v, K) for k, v in sets.items()}
        qmax = max([sum(e[g.V:]) for Fi in Fis.values() for P in Fi for e in P] + [0])
        D = max(max(dn(Fi, Ej, K) for Fi in Fis.values()), 1)
        okg = (g.V, ne, g.F) == shape
        okp = float(D + 1) ** g.F < 9.0e18
        out('C-GRAPH %s: V %d, edges %d, F %d (want %s) -> %s; C-PACK: K %d needs D %d, (D+1)^F = %.3g < 9e18 -> %s; Q-degree %d '
            '(series %.1f s)' % (name, g.V, ne, g.F, shape, gate('C-GRAPH', okg), K, D, float(D + 1) ** g.F, gate('C-PACK', okp), qmax,
                                 cpu() - t1))
        if not (okg and okp):
            raise ValueError('graph %s' % name)
        t1 = cpu()
        am = AllMom2(g.G, g.n, D, W=g.W, groups=g.groups, caps={1: max(QCAP, qmax)})
        ak = {k: [float(math.fsum(am.E2(Fi[i], Ej[kk - i]) for i in range(kk + 1) if Fi[i])) for kk in range(K + 1)]
              for k, Fi in Fis.items()}
        out('MOMENTS %s: D %d, Q-cap %d, %d codes at the top degree, %d entries (%.1f s)' % (
            name, D, max(QCAP, qmax), len(am.codes[-1]), len(ak), cpu() - t1))
        return ak

    # D4-L0: columns c0 - 1, c0, c0 + 1 -> 0, 1, 2; e = HT(c0), f = MB(c0) = theta f, theta e = HT(c0 - 1)
    E4, TE4, F4 = (3, 6), (0, 3), (4, 5)
    g4, ne4 = dwin(3, vert(0) + vert(2) + [TE4, E4, F4])
    sets4 = {}
    for a in (0, 1):
        for b in (0, 1):
            for k in (0, 1, 2):
                sets4['E%d%d%d' % (a, b, k)] = [pfac(0)] + [xfac(E4)] * a + [xfac(TE4)] * b + [xfac(F4)] * k + [pfac(2)]
    ak4 = run_graph('D4-L0', g4, ne4, (9, 14, 18), sets4)
    # D4M-L0: e = HT(c0), f = MB(c0 + 1), theta e = HT(c0 - 1), theta f = MB(c0 - 1)
    E5, F5, TE5, TF5 = (3, 6), (7, 8), (0, 3), (1, 2)
    g5, ne5 = dwin(3, vert(0) + vert(2) + [TE5, E5])
    sets5 = {}
    for m in range(16):
        bits = tuple((m >> i) & 1 for i in range(4))
        sets5['S%d%d%d%d' % bits] = [pfac(0)] + [xfac(pr) for pr, bb in zip((E5, F5, TE5, TF5), bits) if bb] + [pfac(2)]
    ak5 = run_graph('D4M-L0', g5, ne5, (9, 14, 17), sets5)
    # D3-L0 (probe): columns c0 - 2 .. c0 + 2 -> 0..4; e = HT(c0), f = HB(c0 + 1), theta e = HT(c0 - 1), theta f = HB(c0 - 2)
    E3, F3, TE3, TF3 = (6, 9), (11, 14), (3, 6), (2, 5)
    g3, ne3 = dwin(5, vert(0) + vert(4) + [TF3, TE3, E3, F3])
    t1 = cpu()
    Ej3 = ej_series(g3, K)
    Fi3 = fi_series(g3, [pfac(0), xfac(E3), xfac(F3), xfac(TE3), xfac(TF3), pfac(4)], K)
    need3 = [dn(Fi3, Ej3, kk) for kk in range(K + 1)]
    dmax3 = max(d for d in range(1, 40) if float(d + 1) ** g3.F < 9.0e18)
    kal = max([kk for kk in range(K + 1) if need3[kk] <= dmax3] + [-1])
    ok3 = (g3.V, ne3, g3.F) == (15, 24, 25)
    out('C-PACK D3-L0 (probe, no moment): V %d, edges %d, F %d (C-GRAPH %s); degree needed for K = 0, 1, 2: %s; (D+1)^%d < 9e18 allows '
        'D <= %d, so K <= %d (the t^0 term only, part H\'s exact harmonic value): no J = 300 FLOAT on amom2b. Top-degree codes a wider '
        'packing would hold at K = 2 (D %d): C(F - 1 + D, D) = %d, against D4-L0\'s %d (%.1f s)' % (
            g3.V, ne3, g3.F, gate('C-GRAPH', ok3), ', '.join(str(x) for x in need3), g3.F, dmax3, kal, need3[K],
            math.comb(g3.F - 1 + need3[K], need3[K]), math.comb(g4.F - 1 + 8, 8), cpu() - t1))
    KS = K + 1
    smul, sinv, sadd, ssc = salg(KS)
    R4 = {k: smul(v, sinv(ak4['E000'])) for k, v in ak4.items()}
    R5 = {k: smul(v, sinv(ak5['S0000'])) for k, v in ak5.items()}
    COV4, EX4, ce4, cf4 = cov_d4(R4, KS)
    COV5, EX5, ce5, cf5 = cov_d4m(R5, KS)
    ws = max(rel(x, y) for k in (0, 1, 2) for x, y in zip(R4['E10%d' % k], R4['E01%d' % k]))
    mir = lambda s: 'S' + s[3] + s[4] + s[1] + s[2]
    ws5 = max(rel(x, y) for s in R5 for x, y in zip(R5[s], R5[mir(s)]))
    out('C-SYM-F: D4-L0 E[xi_e xi_f^k] = E[xi_te xi_f^k] (k <= 2), largest relative %.1e; D4M-L0 mirror subsets, largest relative %.1e '
        '(tolerance 1e-10) -> %s' % (ws, ws5, gate('C-SYM-F', ws <= 1e-10 and ws5 <= 1e-10)))
    for fam, cv in (('D4', COV4), ('D4M', COV5)):
        r0 = rel(cv[0], HV[(fam, 'L0')])
        out('C-H0 %s: a_0 of Cov(X_c, theta X_c) %.12e against part H\'s L0 value %.12e (relative %.1e, tolerance 1e-7) -> %s' % (
            fam, cv[0], HV[(fam, 'L0')], r0, gate('C-H0', r0 <= 1e-7)))
    fires = rel(COV4[0], HV[('D4', 'L1')]) > 1e-3
    out('PLANT-H0: D4-L0\'s a_0 against part H\'s L1 value %.6e: relative %.2e -> %s' % (
        HV[('D4', 'L1')], rel(COV4[0], HV[('D4', 'L1')]), 'FIRES' if fires else 'DOES NOT FIRE'))
    if not fires:
        fails.append('PLANT-H0')
    hz = open(HZOUT[N]).read()
    ent = {}
    for mm in re.finditer(r'^ENTRY N=%d (M4m?_\d\d) \(graph DT[^)]*\): ak=\[([^\]]*)\]' % N, hz, re.M):
        ent[mm.group(1)] = [float(x) for x in mm.group(2).split(',')]
    for fam, hzn, ex, ce, cf, pre in (('D4', 'D4', EX4, ce4, cf4, 'M4'), ('D4M', 'D4m', EX5, ce5, cf5, 'M4m')):
        mm = re.search(r'^SERIES P2-14 N=%d %s \(t = 1/J; a_0 a_1 a_2; FLOAT\): Cov_w (\S+) (\S+) (\S+);' % (N, hzn), hz, re.M)
        if mm is None or any(('%s_%s' % (pre, s)) not in ent for s in ('00', '10', '01')):
            raise ValueError('pk15 output: no SERIES or ENTRY lines for %s' % hzn)
        cw = [float(mm.group(k)) for k in (1, 2, 3)]
        me = smul(ent[pre + '_10'], sinv(ent[pre + '_00']))
        mf = smul(ent[pre + '_01'], sinv(ent[pre + '_00']))
        wc = max(rel(x, y) for x, y in zip(ex, cw))
        wm = max(max(rel(x, y) for x, y in zip(ce, me)), max(rel(x, y) for x, y in zip(cf, mf)))
        out('C-SAME-W %s: the doubled window\'s Cov_w a_k %s against pk15\'s SERIES %s (largest relative %.1e); m_e, m_f against its '
            '%s_10, %s_01 / %s_00 (largest relative %.1e); tolerance 1e-7 -> %s' % (
                fam, ' '.join('%.12g' % x for x in ex), ' '.join('%.12g' % x for x in cw), wc, pre, pre, pre, wm,
                gate('C-SAME-W', wc <= 1e-7 and wm <= 1e-7)))
    XR = {}
    for ln in open(EXPORT).read().split('\n'):
        mm = re.match(r'^N(\d)_(D3|D4|D4M)_P(\d{4}) = (.*)$', ln)
        if mm and int(mm.group(1)) == N:
            v = mm.group(4).split()
            XR[(mm.group(2), int(mm.group(3)))] = {'jlo': float(v[0]), 'pX': float(v[3])}
    i0 = {4: 61, 3: 0}[N]
    grid = sorted(set([i0, i0 + 1, i0 + 10, i0 + 40, 150, 250, 400, 600, 800, 903]))
    COVS = {'D4': COV4, 'D4M': COV5}
    for fam in ('D4', 'D4M'):
        cv = COVS[fam]
        out('SERIES %s-L0 N%d (t = 1/J; a_0 a_1 a_2; FLOAT): Cov(X_c, theta X_c) %s; Cov_w %s' % (
            fam, N, ' '.join('%.12g' % x for x in cv), ' '.join('%.12g' % x for x in (EX4 if fam == 'D4' else EX5))))
    # values-first at the first piece (each entry at t, then the same algebra on numbers): an O(t^3) indicator
    tq = 1.0 / XR[('D4', i0)]['jlo']
    vf4 = cov_d4({k: [horner(v, tq) / horner(ak4['E000'], tq)] for k, v in ak4.items()}, 1)[0][0]
    vf5 = cov_d4m({k: [horner(v, tq) / horner(ak5['S0000'], tq)] for k, v in ak5.items()}, 1)[0][0]
    out('INFO values-first at piece %d (J_lo %.6g): D4-L0 %.6e against the series %.6e (relative %.1e); D4M-L0 %.6e against %.6e '
        '(relative %.1e)' % (i0, 1.0 / tq, vf4, horner(COV4, tq), rel(vf4, horner(COV4, tq)), vf5, horner(COV5, tq),
                             rel(vf5, horner(COV5, tq))))
    RHO = {}
    badcs = []
    for i in grid:
        jl = XR[('D4', i)]['jlo']
        if any(abs(XR[(f_, i)]['jlo'] - jl) > 1e-9 * jl for f_ in ('D3', 'D4M')):
            raise ValueError('export J_lo differs between classes at piece %d' % i)
        t = 1.0 / jl
        parts = []
        for fam in ('D4', 'D4M'):
            cv = COVS[fam]
            val = horner(cv, t)
            pX = XR[(fam, i)]['pX']
            if not (0.0 < val <= pX * pX):
                badcs.append((fam, i))
            RHO[(fam, i)] = math.sqrt(max(val, 0.0)) / pX
            parts.append('%s-L0 %.6e (a_1 t / a_0 %+.3e, a_2 t^2 / a_0 %+.3e; J_lo / t=0 %.4f) rho %.5f' % (
                fam, val, cv[1] * t / cv[0], cv[2] * t * t / cv[0], val / cv[0], RHO[(fam, i)]))
        RHO[('D3', i)] = math.sqrt(HV[('D3', 'L0')]) / XR[('D3', i)]['pX']
        out('PIECE %d J_lo %.6g: %s; D3-L0 (t = 0, H) rho %.5f' % (i, jl, '; '.join(parts), RHO[('D3', i)]))
    out('C-POS-F / C-CS-F: 0 < Cov(X_c, theta X_c) <= pX_hi^2 at every scan piece (%d pieces x 2 classes): failing %s -> %s' % (
        len(grid), badcs or 'none', gate('C-CS-F', not badcs)))
    out('PART F cpu %.1f s' % (cpu() - t0))

    # ---- part S: the screen re-read
    txt = open(TSV_IN).read()
    mt = re.search(r'theta-cut \w+ target: N4 D3 ([0-9.]+), N4 D4/D4M ([0-9.]+), N3 D3 ([0-9.]+), N3 D4/D4M ([0-9.]+)\)', txt)
    mk_ = re.search(r'D4/D4M double trick (\S+) N4, (\S+) N3; D3 CS-split single trick (\S+) N4, (\S+) N3\)', txt)
    mf_ = re.search(r'1 at N4 piece 61, 1/([0-9.]+) at N3 piece 0', txt)
    if mt is None or mk_ is None or mf_ is None:
        raise ValueError('TSV header: no theta-cut targets or trick formula')
    TH = {(4, 'D3'): float(mt.group(1)), (4, 'D4'): float(mt.group(2)), (4, 'D4M'): float(mt.group(2)),
          (3, 'D3'): float(mt.group(3)), (3, 'D4'): float(mt.group(4)), (3, 'D4M'): float(mt.group(4))}
    f3 = 1.0 / float(mf_.group(1))
    TRICK = {(4, 'D4'): float(mk_.group(1)), (4, 'D4M'): float(mk_.group(1)), (3, 'D4'): float(mk_.group(2)) * f3,
             (3, 'D4M'): float(mk_.group(2)) * f3, (4, 'D3'): float(mk_.group(3)), (3, 'D3'): float(mk_.group(4)) * f3}
    TPIECE = {4: 61, 3: 0}
    lines = [ln for ln in txt.split('\n') if ln and not ln.startswith('#')]
    hdr = lines[0].split('\t')
    want = ['N', 'family', 'd_L', 'd_R', 'Cov', 'piece', 'a', 'b', 'c', 'd', 'e', 'normX_old', 'normX_S', 'R_P', 'headroom_P', 'need_P',
            'mark_P', 'trick_A', 'R_A', 'headroom_A', 'need_A', 'mark_A', 'best']
    if hdr != want:
        raise ValueError('TSV fields %r' % hdr)
    rows = [ln.split('\t') for ln in lines[1:] if ln.split('\t')[0] == str(N)]
    badt = []
    res = []
    for r in rows:
        fam, dL, dR = r[1], int(r[2]), r[3]
        cov, piece = float(r[4]), int(r[5])
        a, b, c, d, e = (float(x) for x in r[6:11])
        nO, nS = float(r[11]), float(r[12])
        tg = TH[(N, fam)]
        trick = None
        if dL == 0:
            if piece != TPIECE[N]:
                raise ValueError('row %s (%d,%s) at piece %d: the trick formula holds at piece %d' % (fam, dL, dR, piece, TPIECE[N]))
            trick = TRICK[(N, fam)]
            if rel(float(r[17]), trick) > 5e-3:
                badt.append((fam, dL, dR, 'trick'))
        # C-TSV: rho = 1 reproduces the table
        RP1, _, _, mP1 = reading(cov, a + b, (c + d + e) / nO, nS, tg)
        if rel(RP1, float(r[13])) > 1e-3 or mP1 != r[16]:
            badt.append((fam, dL, dR, 'P'))
        if dL == 0:
            RA1, _, _, mA1 = reading(cov, b + trick, (d + e) / nO, nS, tg)
            if rel(RA1, float(r[18])) > 1e-3 or mA1 != r[21]:
                badt.append((fam, dL, dR, 'A'))
        if (fam, piece) not in RHO:
            raise ValueError('no rho at piece %d' % piece)
        if fam == 'D3':
            rL = rR = RHO[('D3', piece)]
            src = 'H'
        else:
            rL, rR = RHO[(fam, piece)], RHO[('D4M' if fam == 'D4' else 'D4', piece)]
            src = 'F'
        a0, b0 = a * rL, b * rR
        RP, hP, nP, mP = reading(cov, a0 + b0, (c + d + e) / nO, nS, tg)
        if dL == 0:
            RA, hA, nA, mA = reading(cov, b0 + trick, (d + e) / nO, nS, tg)
        else:
            RA, hA, nA, mA = None, None, '-', '-'
        best = mP if (mA == '-' or RANK[mP] >= RANK[mA]) else mA
        rmax = ''
        if fam == 'D3' and RANK[best] >= 2:
            cands = []
            if mP == best and a + b > 0:
                cands.append((cov / 2.0 - (c + d + e) / nO * (nS if best == 'pass' else tg)) / (a + b))
            if dL == 0 and mA == best and b > 0:
                cands.append((cov / 2.0 - trick - (d + e) / nO * (nS if best == 'pass' else tg)) / b)
            rmax = '%.4g' % max(cands) if cands else ''
        res.append([str(N), fam, str(dL), dR, r[4], str(piece), '%.6g' % XR[(fam, piece)]['jlo'], '%.6e' % XR[(fam, piece)]['pX'], src,
                    '%.5f' % rL, '%.5f' % rR, r[6], r[7], r[8], r[9], r[10], r[11], r[12], '%.3e' % a0, '%.3e' % b0, '%.5e' % RP,
                    '%.4g' % hP, fmt_need(nP), mP, ('%.6g' % trick) if trick is not None else '-',
                    ('%.5e' % RA) if RA is not None else '-', ('%.4g' % hA) if hA is not None else '-', fmt_need(nA), mA, best, r[22],
                    rmax])
    out('C-TSV: with rho = 1 my rule reproduces the table\'s R_P, R_A (relative 1e-3) and marks, and the trick formula its printed trick '
        '(relative 5e-3), for %d rows: differing %s -> %s' % (len(rows), badt[:6] or 'none', gate('C-TSV', not badt)))
    cols = ['N', 'family', 'd_L', 'd_R', 'Cov', 'piece', 'J_lo', 'pX_hi', 'src', 'rho_L', 'rho_R', 'a', 'b', 'c', 'd', 'e', 'normX_old',
            'normX_S', 'a_route0', 'b_route0', 'R_P', 'headroom_P', 'need_P', 'mark_P', 'trick_A', 'R_A', 'headroom_A', 'need_A',
            'mark_A', 'best', 'best_6bc0ff4d', 'rho_max_D3']
    with open(TSV_PATH, 'x') as fh:
        fh.write('# P2-12 near-end joint screen re-read with route 0 (pk11 %s, FLOAT, a necessary condition): pk15\'s '
                 'TABLE_P2_12_JOINT_SCREEN_SPRIME_ROUTEA_v1.tsv 6bc0ff4d with pX in terms a and b replaced by sqrt(Cov(X_c, theta X_c)) at '
                 'the row\'s piece: a_route0 = a rho_L, b_route0 = b rho_R, rho = sqrt(Cov(X_c, theta X_c)) / pX_hi.\n' % LABEL)
        fh.write('# src F: D4/D4M from the L0-doubled window at J = 300 (amom2b K = 2; D4: rho_L D4-L0, rho_R D4M-L0; D4M the reverse); '
                 'src H: D3 at its exact t = 0 L0 value (no J = 300 value on amom2b, F 25). Rules, r = normX_S/normX_old, need and '
                 'marks as 6bc0ff4d; trick_A from its header formula; rho_max_D3: the largest common rho keeping the new best mark.\n')
        fh.write('\t'.join(cols) + '\n')
        for x in res:
            fh.write('\t'.join(x) + '\n')
    out('WROTE %s %s (%d rows)' % (os.path.basename(TSV_PATH), sha_file(TSV_PATH), len(res)))
    cnt_old = {k: sum(1 for x in res if x[30] == k) for k in RANK}
    cnt_new = {k: sum(1 for x in res if x[29] == k) for k in RANK}
    out('REREAD N%d (%d rows), best mark old -> new: %s' % (N, len(res), ', '.join('%s %d -> %d' % (k, cnt_old[k], cnt_new[k])
                                                                               for k in ('pass', 'theta-cut', 'beyond-theta', 'none'))))
    for x in res:
        if x[29] != x[30]:
            out('MOVED %s %s (%s,%s): %s -> %s (plain h %s need %s; route A h %s need %s; rho_L %s rho_R %s %s)%s' % (
                x[0], x[1], x[2], x[3], x[30], x[29], x[21], x[22], x[26], x[27], x[9], x[10], x[8],
                ('; D3 keeps it up to rho %s' % x[31]) if x[31] else ''))
    for x in res:
        if x[29] != 'pass':
            out('REMAINING %s %s (%s,%s): best %s; plain h %s need_P %s; route A h %s need_A %s%s' % (
                x[0], x[1], x[2], x[3], x[29], x[21], x[22], x[26], x[27], ('; D3 rho_max %s' % x[31]) if x[31] else ''))
except Exception as ex:
    out('ERROR %s: %s' % (type(ex).__name__, ex))
    for ln in traceback.format_exc().splitlines()[-14:]:
        out('TRACE ' + ln)
    fails.append('ERROR')
out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (ITEM, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
out('VERDICT %s' % ('VALID' if not fails else 'INVALID (%s)' % ', '.join(sorted(set(fails)))))
