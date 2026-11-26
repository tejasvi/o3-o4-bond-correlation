#!/usr/bin/env python3
"""kt_s9b_v3_2.py -- pk02 (code/pk02/). W1 of S9C_PLAN_v2 (d5c5dd4a) sect. 8, with S9C_PLAN_v2_ADD1 (6c952761): the new entries of
the double eigen trick (C9) at J = 300, on the existing riglap5s engines (2-column graph; 16-form 3-column graph; amom2b's assert holds).
FLOAT DATA: Lemma 19.1c bounds (PK10_NOTES sect. 19.3.2; riglap5s) in floating point; their certification is milestone M3.

REVISION of kt_s9b_v3_1.py (23099b09, never run) on the three asks: (a) PLANT-B5S: C-B5S's identity test applied to Dx,0 with one group
  per factor against Dx,0 must find a difference; (b) BUDGET-GX: every Gx and GxR entry's split-group remainder next to the plan's stand-in
  for it (kt_s9b_v2's r(G,g,h), the proxy of plan v2 sect. 7 line 1), with the ratio and the budget line it feeds, and BUDGET-LINE1: line 1
  recomputed as x0 (r(IhT,1) + r(Gx,0,1)) against plan v2's x0 (r(Ih,1) + r(G,0,1)) from kt_s9b_v2's printed remainders; (c) the Dx,0
  calibration (C-SPLIT's remainder ratio) stays INFO. Everything else is kt_s9b_v3_1's.
kt_s9b_v3_1 was the REVISION of kt_s9b_v3.py (6b0efb81), whose smoke (out 81a6a1d1) stopped at its CPU cap inside the first Gx entry: the three factors of a Gx
  job [p_g(left), xi(1,4), p_h(right)] all overlap, so riglap4.group_factors makes one group over all 13 forms and riglap5c's group norms
  need moments of high degree on 13 forms. Changes:
  (1) bound5s_g: a verbatim copy of riglap5s.bound5s (riglap5s.py l.37-83, spliced in by awk) whose grouping line is the only change; with
      grouping 'split' every factor is its own group. Every place where bound5s uses the groups is a Hoelder inequality over the product
      F = prod_g F_g (fnorm, nF4c, nF0p) or the Leibniz rule with Hoelder (EF4); neither needs disjoint vertex sets, so the remainder stays
      a valid bound, only looser; the a_k (series product) and the exact parts (nF0, nF0c, sup_F3) do not depend on the grouping.
      Gx and GxR entries use 'split' (3 groups); every other entry calls riglap5s.bound5s itself.
  (2) new gate C-B5S: bound5s_g with group_factors' grouping, run first on fresh caches, reproduces riglap5s.bound5s bit for bit on G,0,0
      and Dx,0 (kt_s9b_v2's job); new gate C-SPLIT: Dx,0 with 'split' has the a_k of Dx,0 (1e-12), and the remainder ratio (INFO) shows
      what the split costs; C-AKV2 now covers G,0,0 and Dx,0 against kt_s9b_v2.
  (3) LIM for n4 and n3 raised to 540 (the three IhT entries keep the standard grouping, the mirror of kt_s9b_v2's Ih, about 57 s each).
Notation as R6a sect. 1 and plan v2 sect. 2; t = 1/J; h = the M bond between two columns, xi_h = J(1 - s_M . s'_M).
  Gx,g,h   Gx_gh = <phi_g, K_xi phi_h>/main_D: the 2-column xi-Gram, xi on the pair (1,4) between the columns; (g, h) in PE (6 entries).
  IhT,g    IhT_g = <phi_g, K_xi V K phi_0>/main_N: 3-column, xi on the pair (1,4) (the left K, next to phi_g); g in {0, 1, 3}.
           kt_s9b_v2's Ih_b = <phi_b, K V K_xi phi_0>/main_N has xi on (4,7), next to phi_0. By transposition IhT_0 = Ih_0 (C-IHT0).
  Check entries: G,0,0 and Dx,0 on the new 2-column graph (C-AKV2), each also by bound5s_g with the standard grouping (G,0,0|copy,
           Dx,0|copy: C-B5S) and Dx,0 with one group per factor (Dx,0|split: C-SPLIT); GxR,h,g = Gx_gh with the two states swapped
           (C-GXSYM).
  INFO entries: Gp,g = <W P_g^+, K W P_g^+>/main_D with P_g^+ = p_g with |coefficients| (S9C_PLAN_v2_ADD1 sect. 4(b), a proposal):
           kappa_g^2 <= Gp_g/G_gg bounds ||K^{1/2}|phi_g| ||^2/||psi_g||^2 (float).
  AK4      the exact a_0..a_3 of the 4-column H_00, by kt_s9b4_smoke_v1's method (riglap5b's a_k formulas without a prep; AllMom2 on the
           19 forms at Dn <= 8, so amom2b's assert holds), for C-ET2.
Each entry: exact a_0..a_3 and the one-at-a-time J = 300 remainder parts rem, tail, ann, far (riglap5s.bound5s, or bound5s_g for the
  entries marked split or copy), with kt_s9b_v2's radii a_v = min(80 G_vv/300, 0.6) at J_REF = 300 held fixed, so each remainder bounds
  its entry for every J >= 300.
Checks (gates unless INFO); * is the product of t-series cut after t^3; m-hat = 1 + m1 t + m2 t^2 + m3 t^3 (vacres):
  C-HASH; C-GRAPH (V and F: 2-column 6/13, 3-column 9/16, 4-column 12/19); C-XIH-DX and C-XIH-NT (the xi factor on (1,4) against the
    dot series, as kt_s9b_v2's C-XIH on (4,7)); C-QCAP (Q-degree <= 6 for every job);
  C-AKV2 (G,0,0 and Dx,0 on the new 2-column graph: a_k equal kt_s9b_v2's printed entries to 1e-12 max(1, |a|));
  C-B5S (G,0,0|copy = G,0,0 and Dx,0|copy = Dx,0, a_k and the four remainder parts identical); PLANT-B5S (the same test on Dx,0|split
    against Dx,0 must find a difference); C-SPLIT (Dx,0|split a_k = Dx,0 a_k to 1e-12 max(1, |a|));
  C-GXSYM (GxR,1,0, GxR,3,0, GxR,3,1: a_k equal Gx,0,1, Gx,0,3, Gx,1,3 to 1e-12 max(1, |a|));
  C-IHT0 (IhT,0 against kt_s9b_v2's printed Ih,0: a_k to 1e-12 max(1, |a|); plan v2 asked 1e-14, printed for information);
  C-IHT1 (IhT_g = m-hat Gx_0g + <phi_g, K_xi g>/main_N with g = V K phi_0 - mu-hat phi_0 = O(t^2): the a_0, a_1 of IhT_g equal those of
    m-hat * Gx_0g to 1e-12 max(1, |a|), g in {0, 1, 3}); PLANT-IHT1 (kt_s9b_v2's Ih,1 in place of IhT,1 must fail C-IHT1);
  C-R (R = main_N^2/(main_D main_4) at J = 300 within 1e-10 of 1);
  C-ET2 (plan v2 (C9) for b = 0: H_00 = R [m-hat * (Ih_0 + IhT_0) - m-hat * m-hat * Gx_00] + O(t^4), the a_0..a_3 equal AK4 to 1e-12
    max(1, |a|)); PLANT-ET2 (m1 + 0.01 must fail C-ET2); C-AK4S (N = 4: AK4 equals kt_s9b4_smoke_v1's printed AK4 to 1e-12 max(1, |a|)).
  INFO: C-IH1 (kt_s9b_v2's Ih_b a_0 against X0 Gx_01 a_0 for b = 1 and Y0 Gx_03 a_0 for b = 3, since f_b = O(t)); the remainders of
    G,0,0 and IhT,0 against kt_s9b_v2's G,0,0 and Ih,0; kappa_g from Gp,g; BUDGET-GX and BUDGET-LINE1 (the ask (b)).
Items: smoke (N = 3, then N = 4: the 2-column prep, the check entries, Gx,0,0, AK4, C-R, C-ET2 and PLANT-ET2 with kt_s9b_v2's Ih,0 for
  both Ih_0 and IhT_0; no 3-column prep), n4 and n3 (all entries and checks). Prices [E] from kt_s9b_v2's timings (PREP-D 2.5 s, 2-column
  entries <= 2 s, PREP-N 164-172 s, first Ih entry 57 s) and the smoke's AK4 (4.3 s), with each IhT entry at up to 60 s and the split Gx
  entries at a few s: smoke <= 60 s (LIM 120, cap 125 s = 0.035 core-h); n4 and n3 300-420 s each (LIM 540, cap 545 s = 0.151 core-h each).
CPU and CAP-STOP as kt_s9b_v2: RLIMIT_CPU soft LIM, hard LIM + 5; guards before each prep and entry; SIGXCPU prints CAP-STOP, exits 3.
Run (outputs in the own folder only): D=/mnt/g2/release/root/code/pk02; OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
  MALLOC_ARENA_MAX=2 TMPDIR=$D/tmp_kt_s9b3 OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B
  $D/kt_s9b_v3_2.py <item> <LIM> > $D/out_kt_s9b_v3_2_<item>.out 2> $D/out_kt_s9b_v3_2_<item>.err
"""
import resource, sys, time, math, hashlib, signal, os, traceback, re
ITEMS = ('smoke', 'n4', 'n3')
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: kt_s9b_v3_2.py ITEM LIM   (ITEM smoke | n4 | n3; LIM = RLIMIT_CPU soft limit in s, hard LIM + 5)')
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,4}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r (need 5 <= LIM <= 540)' % sys.argv[2])
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
SRC = '/mnt/g2/release/root/code/pk01'
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
    'ts_N3_S.json': '26e20e76fbce80c205703f5ba27395ebddaeaa2713bb129b0b4e5902a2061955',
    'ts_N4_J170_D_S.json': 'd6d104ea1f2f64a82f051ce2872f1fbbd0628c9875b0743e4815bf74643fea8c',
    'vacres_K3_N3.json': 'ebcbd08ca532642188071c964039808a318038020bb1a788a7fa3a49cb357426',
    'vacres_K3_N4.json': '516b2501c37a65b21b617fba3cb1d7b02adf9966f409bc5105418822dfa0e765',
}
SRCFILES = {
    'out_kt_s9b_v2_n3.out': '3c7b2d2e6d461674b11a2e0554f8ce2294de6c644b5922ee722a159a01659cbf',
    'out_kt_s9b_v2_n4.out': 'e7ffff8b54188e7c114df47e4b44bf382877af2298092edeb018c6ecc35a27cd',
    'out_kt_s9b4_smoke_v1.out': '684bb33c1449522d846a03f87bda5398cef0f86a09ce1d35dad9111f12cd4e56',
}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('kt_s9b_v3_2 sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (sha_file(os.path.abspath(__file__)), MODE, LIM, LIM, LIM + 5))
_bad = []
for _d, _tab in ((SCR, ENGINE), (INP, INPUTS), (SRC, SRCFILES)):
    for _n in sorted(_tab):
        _got = sha_file(os.path.join(_d, _n))
        if _got != _tab[_n]:
            _bad.append('%s %s' % (_n, _got))
out('C-HASH %s (%d engine files, %d inputs, %d predecessor outputs)%s' % ('PASS' if not _bad else 'FAIL', len(ENGINE), len(INPUTS),
                                                                       len(SRCFILES), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, SCR)
import json
import numpy as np
import riglap5b
import riglap5c
import riglap5s
import riglap2 as _r
import riglap3 as _r3
from riglap2 import Graph
from riglap4 import group_factors, _deg
from riglap5b import series_product
from riglap5e import _joint
from amom2b import AllMom2
from pseries import padd, pscale, pmul
from vacmod2 import A_EX, B_EX
from lapl2 import strip_graph

S_RAD, RHO_P, J_REF, QCAP = 80.0, 0.7, 300.0, 6
NPB = {'D': 16, 'N': 12}
J = 300.0
TOL = 1e-12
EVEN = (0, 1, 3)
PE = ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3))
SWAP = ((0, 1), (0, 3), (1, 3))
X0 = (7 - 3 * math.sqrt(5)) / 2
Y0 = (23 - 5 * math.sqrt(21)) / 2
LD, RD = (0, 1, 2), (3, 4, 5)
LN, RN = (0, 1, 2), (6, 7, 8)
L4, R4 = (0, 1, 2), (9, 10, 11)
PAIRS_D = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
PAIRS_DX = PAIRS_D + [(1, 4)]
PAIRS_N = [(0, 1), (1, 2), (0, 2), (4, 7), (6, 7), (7, 8), (6, 8)]
PAIRS_NT = [(0, 1), (1, 2), (0, 2), (1, 4), (6, 7), (7, 8), (6, 8)]
PAIRS_4 = [(0, 1), (1, 2), (0, 2), (4, 7), (9, 10), (10, 11), (9, 11)]
XI_14 = ('xi', (1, 4, 2), 0.0, [1.0] + [0.0] * 8)     # riglap3 pair order (T,M), (M,B), (T,B): xi on the pair (1,4); vertex 2 sits in
#                                                       the state's column, as 8 does in kt_s9b_v2's (4, 7, 8)
H_XI = ('xi', (4, 7, 8), 0.0, [1.0] + [0.0] * 8)      # kt_s9b_v2's and kt_s9b4_smoke_v1's xi on the pair (4,7)
SFILE = {4: 'ts_N4_J170_D_S.json', 3: 'ts_N3_S.json'}
VFILE = {4: 'vacres_K3_N4.json', 3: 'vacres_K3_N3.json'}
GUARD = {'prepN': 250.0, 'prepD': 30.0, 'entry': 20.0, 'ak4': 30.0}


class CapStop(Exception):
    pass


def need(kind):
    if cpu() > LIM - GUARD[kind]:
        raise CapStop(kind)


def load_json(name):
    with open(os.path.join(INP, name)) as fh:
        return json.load(fh)


def src_text(name):
    with open(os.path.join(SRC, name)) as fh:
        return fh.read()


def graph(ncols, pairs, N):
    V, E = strip_graph(ncols, (A_EX, B_EX))
    return Graph(V, E, pairs, N=N)


def radii(g):
    return [math.sqrt(min(S_RAD * g.G[v, v] / J_REF, 0.6)) for v in range(g.V)]


def make_prep(g, key, kind):
    riglap5b.NPOLY_B = NPB[kind]
    return riglap5s.Prep5s(g, J, radii(g), RHO_P, key=key, qcap=QCAP)


def split_groups(factors):
    """one group per factor (consts folded into the scalar), for bound5s_g's grouping 'split'."""
    scal, groups = 1.0, []
    for f in factors:
        if f[0] == 'const':
            scal *= f[1]
        else:
            groups.append([f])
    return scal, groups


# ---------------------------------------------- riglap5s.bound5s (l.37-83), verbatim but for the def line and the grouping line
def bound5s_g(prep, factors, grouping):
    g, t, J = prep.g, prep.t, prep.J
    V = g.V
    inf = float("inf")
    scal, groups = group_factors(factors) if grouping == 'std' else split_groups(factors)
    G_ = max(len(groups), 1)
    gds = [riglap5c._gdata(prep, gf) for gf in groups]
    Fi = series_product([d["ser"] for d in gds], scal, 3) if groups else [{tuple([0] * g.F): scal}, {}, {}, {}]
    qmax = max([sum(e[V:]) for P in Fi for e in P] + [0])
    assert qmax <= prep.qcap, (qmax, prep.qcap)
    Dn = max(_deg(Fi[i]) + _deg(prep.Ej[k - i]) for k in range(4) for i in range(k + 1) if Fi[i])
    am = prep.engine(max(Dn, 1))
    ak = [sum(am.E2(Fi[i], prep.Ej[k - i]) for i in range(k + 1) if Fi[i]) for k in range(4)]
    if not prep.ok:
        return ak, {"rem": inf, "tail": inf, "ann": inf, "far": inf}
    d0 = 2 * _deg(Fi[0])
    nF0 = math.sqrt(max(_joint(prep, d0, "u").E2(Fi[0], Fi[0]), 0.0))
    nF0c = math.sqrt(max(_joint(prep, d0, "c").E2(Fi[0], Fi[0]), 0.0))
    def comps(i):
        out = [[]]
        for _ in groups:
            out = [c + [x] for c in out for x in range(i + 1)]
        return [tuple(c) for c in out if sum(c) == i]
    def fnorm(i, cov, p=2):
        return abs(scal) * sum(math.prod(riglap5c._gnorm(prep, gds[gi], "ser", ig, p * G_, cov) for gi, ig in enumerate(c)) for c in comps(i))
    nF = [nF0] + [fnorm(i, "u") for i in (1, 2, 3)]
    nFc = [nF0c] + [fnorm(i, "c") for i in (1, 2, 3)]
    nFle3 = sum(t ** i * nF[i] for i in range(4))
    nFle3c = sum(t ** i * nFc[i] for i in range(4))
    nF4c = fnorm(0, "c", 4) + sum(t ** i * 3.0 ** _deg(Fi[i]) * nFc[i] for i in (1, 2, 3) if Fi[i])
    EF4 = 0.0
    for c in comps(4):
        EF4 += math.factorial(4) / math.prod(math.factorial(x) for x in c) * math.prod(riglap5c._gnorm(prep, gds[gi], "bar", jg, G_, "c") for gi, jg in enumerate(c))
    EF4 *= abs(scal)
    overflow = sum(t ** (i + j) * nF[i] * prep.nE[j] for i in range(4) for j in range(4) if i + j >= 4)
    rho4 = prep.Nc / 24 * min(nFle3c * prep.nC8 ** 4, nF4c * prep.nC6 ** 4)
    B_rem = overflow + nFle3 * prep.rE + rho4 + t ** 4 / 24 * prep.Nc * EF4
    hc = lambda i: 3.0 ** _deg(Fi[i]) * nF[i] if Fi[i] else 0.0
    l2 = nF0 + sum(t ** k * sum((hc(i) if i > 0 else 3.0 ** _deg(Fi[0]) * nF0) * prep.nE4[k - i] for i in range(k + 1)) for k in range(1, 4))
    B_tail = l2 * math.sqrt(prep.Pout)
    nF0p = abs(scal) * math.prod(riglap5c._gnorm(prep, d, "barp", 0, 2 * G_, "p") for d in gds)
    B_ann = prep.Np * nF0p * math.sqrt(prep.Pout_p)
    B_far = _r3.sup_F3(factors, J) * prep.farbase
    if getattr(prep, "verbose", False):
        print("    overflow %.2e F.R_E %.2e rho4 %.2e (C8 form %.2e, C6 form %.2e) R_F %.2e"
              % (overflow, nFle3 * prep.rE, rho4, prep.Nc / 24 * nFle3c * prep.nC8 ** 4, prep.Nc / 24 * nF4c * prep.nC6 ** 4, t ** 4 / 24 * prep.Nc * EF4))
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}


def run_entry(pr, kind, facs, mode='std'):
    riglap5b.NPOLY_B = NPB[kind]
    if mode == 'std':
        ak, B = riglap5s.bound5s(pr, facs)
    else:
        ak, B = bound5s_g(pr, facs, 'std' if mode == 'copy' else 'split')
    return [float(x) for x in ak], dict((k, float(v)) for k, v in B.items())


def entry_line(N, nm, E, t0):
    ak, B = E
    return 'ENTRY N=%d J=%g %s ak=[%s] rem=%r tail=%r ann=%r far=%r r=%.6e (%.1f s, cpu %.1f s)' % (
        N, J, nm, ', '.join(repr(x) for x in ak), B['rem'], B['tail'], B['ann'], B['far'], sum(B.values()), cpu() - t0, cpu())


def qmax_of(g, facs):
    scal, groups = group_factors(facs)
    gser = [_r3.Model3(g, 3, gf).Fser(3).c for gf in groups]
    Fi = series_product(gser, scal, 3)
    return max([sum(e[g.V:]) for P in Fi for e in P] + [0])


def check_xi(g, xi, u, v):
    xs = _r3.Model3(g, 3, [xi]).Fser(3).c
    ds = _r.Model(g, 4, [('dot', u, v, 1.0)]).Fser(4).c
    worst = 0.0
    for k in range(4):
        for e in set(xs[k]) | set(ds[k + 1]):
            a, b = xs[k].get(e, 0.0), ds[k + 1].get(e, 0.0)
            worst = max(worst, abs(a + b) / max(1.0, abs(a)))
    return worst


def exact_ak(g, facs):
    """kt_s9b4_smoke_v1's exact_ak: riglap5b's a_k formulas without a prep (E_j from the H-series to order 3, F_i the factor series)."""
    scal, groups = group_factors(facs)
    gser = [_r3.Model3(g, 3, gf).Fser(3).c for gf in groups]
    Fi = series_product(gser, scal, 3)
    qmax = max([sum(e[g.V:]) for P in Fi for e in P] + [0])
    Hs = _r3.Model3(g, 3, []).H(3)
    H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
    H1sq = pmul(H1, H1)
    Ej = [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
    Dn = max(_deg(Fi[i]) + _deg(Ej[k - i]) for k in range(4) for i in range(k + 1) if Fi[i])
    return Fi, Ej, Dn, qmax


def ak4_h00(g4, facs4):
    Fi, Ej, Dn, qmax = exact_ak(g4, facs4)
    if qmax > QCAP or Dn > 8:
        raise ValueError('AK4: Q-degree %d (qcap %d), Dn %d (<= 8 for the 19 forms)' % (qmax, QCAP, Dn))
    am = AllMom2(g4.G, g4.n, max(Dn, 1), W=g4.W, groups=g4.groups, caps={1: QCAP})
    ak = [float(sum(am.E2(Fi[i], Ej[k - i]) for i in range(k + 1) if Fi[i])) for k in range(4)]
    return ak, Dn, qmax, len(am.codes[-1])


def v2_entry(N, nm):
    mt = re.search(r'ENTRY N=%d J=300 %s ak=\[([^\]]*)\] rem=(\S+) tail=(\S+) ann=(\S+) far=(\S+) r=' % (N, re.escape(nm)),
                   src_text('out_kt_s9b_v2_n%d.out' % N))
    if mt is None:
        raise ValueError('out_kt_s9b_v2_n%d.out: no ENTRY line for %s' % (N, nm))
    return ([float(x) for x in mt.group(1).split(',')],
            dict(zip(('rem', 'tail', 'ann', 'far'), (float(mt.group(i)) for i in (2, 3, 4, 5)))))


def smoke_ak4():
    mt = re.search(r'AK4 N=4 J=300 H_00: ak=\[([^\]]*)\]', src_text('out_kt_s9b4_smoke_v1.out'))
    if mt is None:
        raise ValueError('out_kt_s9b4_smoke_v1.out: no AK4 line')
    return [float(x) for x in mt.group(1).split(',')]


def conv(a, b):
    return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(4)]


def dev(a, ref, ks=(0, 1, 2, 3)):
    return max(abs(a[k] - ref[k]) / max(1.0, abs(ref[k])) for k in ks)


def mhat(R3, d1=0.0):
    return [1.0, R3['m1'] + d1, R3['m2'], R3['m3']]


def h00_c9(mh, ih0, iht0, gx00, R):
    a = conv(mh, [ih0[k] + iht0[k] for k in range(4)])
    b = conv(conv(mh, mh), gx00)
    return [R * (a[k] - b[k]) for k in range(4)]


def fmt(v):
    return ' '.join('%.13g' % x for x in v)


def pv(R3, col, absq=False):
    q = [[abs(x) for x in R3[k]] if absq else R3[k] for k in ('q1', 'q2', 'q3')]
    return ('p', col, q[0], q[1], q[2])


def cpoly(Smat, R3, b, col, absq=False):
    if b == 0:
        return pv(R3, col, absq)
    c0, c9 = float(Smat[0, b]), [float(x) for x in Smat[1:, b]]
    if absq:
        c0, c9 = abs(c0), [abs(x) for x in c9]
    return ('xi', col, c0, c9)


def xia(col):
    return ('xi', col, 0.0, [1.0] + [0.0] * 8)


def jobs_dx(Smat, R3, full):
    """(name, factors, mode); the copy entries come before their std twins, so bound5s_g starts from fresh caches."""
    g00 = [cpoly(Smat, R3, 0, LD), cpoly(Smat, R3, 0, RD)]
    dx0 = [cpoly(Smat, R3, 0, LD), xia(RD), pv(R3, RD)]
    jd = [('G,0,0|copy', g00, 'copy'), ('G,0,0', g00, 'std'), ('Dx,0|copy', dx0, 'copy'), ('Dx,0', dx0, 'std'), ('Dx,0|split', dx0, 'split')]
    jd += [('Gx,%d,%d' % (g, h), [cpoly(Smat, R3, g, LD), XI_14, cpoly(Smat, R3, h, RD)], 'split') for (g, h) in (PE if full else ((0, 0),))]
    if full:
        jd += [('GxR,%d,%d' % (h, g), [cpoly(Smat, R3, h, LD), XI_14, cpoly(Smat, R3, g, RD)], 'split') for (g, h) in SWAP]
        jd += [('Gp,%d' % g, [cpoly(Smat, R3, g, LD, True), cpoly(Smat, R3, g, RD, True)], 'std') for g in EVEN]
    return jd


def jobs_nt(Smat, R3):
    return [('IhT,%d' % g, [cpoly(Smat, R3, g, LN), XI_14, pv(R3, RN)], 'std') for g in EVEN]


def gate(fails, name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


def dx_checks(N, E, fails, nofire):
    """C-AKV2, C-B5S, PLANT-B5S and C-SPLIT, printed as soon as the five check entries exist (before the Gx entries)."""
    STAGE[0] = 'DX checks N=%d' % N
    worst, ratios = 0.0, []
    for nm in ('G,0,0', 'Dx,0'):
        akv, Bv = v2_entry(N, nm)
        worst = max(worst, dev(E[nm][0], akv))
        ratios.append('%s %.6f' % (nm, sum(E[nm][1].values()) / sum(Bv.values())))
    out('C-AKV2 N=%d: G,0,0 and Dx,0 on the 2-column xi graph against kt_s9b_v2: a_k worst %.2e -> %s; remainder ratios %s (INFO)' % (
        N, worst, gate(fails, 'C-AKV2 N=%d' % N, worst <= TOL), ', '.join(ratios)))
    same = all(E[nm + '|copy'] == E[nm] for nm in ('G,0,0', 'Dx,0'))
    out('C-B5S N=%d: bound5s_g with group_factors grouping against riglap5s.bound5s on G,0,0 and Dx,0: %s -> %s' % (
        N, 'identical' if same else 'DIFFERENT', gate(fails, 'C-B5S N=%d' % N, same)))
    fired = E['Dx,0|split'] != E['Dx,0']
    out('PLANT-B5S N=%d: the same identity test on Dx,0 with one group per factor against Dx,0: %s -> %s' % (
        N, 'different' if fired else 'identical', 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        nofire.append('PLANT-B5S N=%d' % N)
    d = dev(E['Dx,0|split'][0], E['Dx,0'][0])
    out('C-SPLIT N=%d: Dx,0 with one group per factor against the standard grouping: a_k worst %.2e -> %s; remainder ratio %.4f '
        '(INFO: the cost of the split)' % (N, d, gate(fails, 'C-SPLIT N=%d' % N, d <= TOL),
                                            sum(E['Dx,0|split'][1].values()) / sum(E['Dx,0'][1].values())))


FEEDS = {(0, 0): 'line 3 (H00) and line 1 (H10 via m_10)', (0, 1): 'line 1 (H10 via m_11)', (0, 3): 'line 4 (H30) and line 1 (H10 via m_13)',
         (1, 1): 'line 5 (h_xx)', (1, 3): 'line 5 (h_xy)', (3, 3): 'line 5 (h_xy via c_x3)'}


def budget_gx(N, E):
    """the ask (b): each split Gx/GxR remainder next to the plan's stand-in, kt_s9b_v2's r(G,g,h) (plan v2 sect. 7 line 1's proxy)."""
    STAGE[0] = 'budget N=%d' % N
    for nm in sorted(E):
        mt = re.fullmatch(r'GxR?,([0-9]),([0-9])', nm)
        if mt is None:
            continue
        g, h = sorted((int(mt.group(1)), int(mt.group(2))))
        r, rp = sum(E[nm][1].values()), sum(v2_entry(N, 'G,%d,%d' % (g, h))[1].values())
        out('BUDGET-GX N=%d %s: split remainder %.4e; plan stand-in r(G,%d,%d) %.4e (kt_s9b_v2); ratio %.3f; feeds %s' % (
            N, nm, r, g, h, rp, r / rp, FEEDS[(g, h)]))


def budget_line1(N, E):
    new = X0 * (sum(E['IhT,1'][1].values()) + sum(E['Gx,0,1'][1].values()))
    old = X0 * (sum(v2_entry(N, 'Ih,1')[1].values()) + sum(v2_entry(N, 'G,0,1')[1].values()))
    out('BUDGET-LINE1 N=%d: x0 (r(IhT,1) + r(Gx,0,1)) = %.4e against plan v2 sect. 7 / ADD1 sect. 2 line 1, x0 (r(Ih,1) + r(G,0,1)) = '
        '%.4e from kt_s9b_v2 [E]; ratio %.3f' % (N, new, old, new / old))


def run_n(N, full, fails, nofire):
    Smat, R3 = np.array(load_json(SFILE[N])['S']), load_json(VFILE[N])
    STAGE[0] = 'graphs N=%d' % N
    gDX, g4 = graph(2, PAIRS_DX, N), graph(4, PAIRS_4, N)
    gD0, gN0 = graph(2, PAIRS_D, N), graph(3, PAIRS_N, N)
    shapes = [('2-column xi', gDX, 6, 13), ('4-column', g4, 12, 19)]
    gNT = None
    if full:
        gNT = graph(3, PAIRS_NT, N)
        shapes.insert(1, ('3-column xi', gNT, 9, 16))
    ok = all((g.V, g.F) == (v, f) for _, g, v, f in shapes)
    out('C-GRAPH N=%d: %s -> %s' % (N, ', '.join('%s V %d F %d' % (nm, g.V, g.F) for nm, g, _, _ in shapes), gate(fails, 'C-GRAPH N=%d' % N, ok)))
    if not ok:
        return
    for nm, g in [('C-XIH-DX', gDX)] + ([('C-XIH-NT', gNT)] if full else []):
        w = check_xi(g, XI_14, 1, 4)
        out('%s N=%d: worst %.2e -> %s' % (nm, N, w, gate(fails, '%s N=%d' % (nm, N), w <= TOL)))
    jd = jobs_dx(Smat, R3, full)
    jn = jobs_nt(Smat, R3) if full else []
    q = max([qmax_of(gDX, f) for _, f, _ in jd] + [qmax_of(gNT, f) for _, f, _ in jn])
    ok = q <= QCAP
    out('C-QCAP N=%d: max Q-degree %d over %d jobs (qcap %d) -> %s' % (N, q, len(jd) + len(jn), QCAP, gate(fails, 'C-QCAP N=%d' % N, ok)))
    if not ok:
        return
    E = {}
    STAGE[0] = 'prepDX N=%d' % N
    need('prepD')
    t0 = cpu()
    prD = make_prep(gDX, 'KDX%d' % N, 'D')
    out('PREP-DX N=%d J=%g: %.1f s, rE %.3e, ok %s' % (N, J, cpu() - t0, getattr(prD, 'rE', float('nan')), prD.ok))
    for nm, facs, mode in jd:
        STAGE[0] = '%s N=%d' % (nm, N)
        need('entry')
        t0 = cpu()
        E[nm] = run_entry(prD, 'D', facs, mode)
        out(entry_line(N, nm, E[nm], t0))
        if nm == 'Dx,0|split':
            dx_checks(N, E, fails, nofire)
    prD = None
    budget_gx(N, E)
    STAGE[0] = 'AK4 N=%d' % N
    need('ak4')
    t0 = cpu()
    ak4, Dn, qm, nc = ak4_h00(g4, [pv(R3, L4), H_XI, pv(R3, R4)])
    out('AK4 N=%d J=300 H_00: ak=[%s] (Dn %d, Q-degree %d, %d codes at the top degree, %.1f s)' % (
        N, ', '.join(repr(x) for x in ak4), Dn, qm, nc, cpu() - t0))
    if N == 4:
        d = dev(ak4, smoke_ak4())
        out('C-AK4S N=4: AK4 against kt_s9b4_smoke_v1 AK4: worst %.2e -> %s' % (d, gate(fails, 'C-AK4S', d <= TOL)))
    if full:
        STAGE[0] = 'prepNT N=%d' % N
        need('prepN')
        t0 = cpu()
        prN = make_prep(gNT, 'KNT%d' % N, 'N')
        out('PREP-NT N=%d J=%g: %.1f s, rE %.3e, ok %s' % (N, J, cpu() - t0, getattr(prN, 'rE', float('nan')), prN.ok))
        for nm, facs, mode in jn:
            STAGE[0] = '%s N=%d' % (nm, N)
            need('entry')
            t0 = cpu()
            E[nm] = run_entry(prN, 'N', facs, mode)
            out(entry_line(N, nm, E[nm], t0))
        prN = None
    STAGE[0] = 'checks N=%d' % N
    R = math.exp(2 * gN0.logmain(J) - gD0.logmain(J) - g4.logmain(J))
    out('C-R N=%d: R = main_N^2/(main_D main_4) %.15f at J = 300 -> %s' % (N, R, gate(fails, 'C-R N=%d' % N, abs(R - 1) <= 1e-10)))
    ih0, ih0B = v2_entry(N, 'Ih,0')
    iht0, src = (E['IhT,0'][0], 'IhT,0 of this run') if full else (ih0, "kt_s9b_v2's Ih,0")
    for tag, d1 in (('C-ET2', 0.0), ('PLANT-ET2', 0.01)):
        ref = h00_c9(mhat(R3, d1), ih0, iht0, E['Gx,0,0'][0], R)
        dv = [abs(ak4[k] - ref[k]) / max(1.0, abs(ak4[k])) for k in range(4)]
        ok = max(dv) <= TOL
        if tag == 'C-ET2':
            res = gate(fails, 'C-ET2 N=%d' % N, ok)
        else:
            res = 'DOES NOT FIRE' if ok else 'FIRES'
            if ok:
                nofire.append('PLANT-ET2 N=%d' % N)
        out('%s N=%d (m1 %+.2f; IhT_0 = %s): AK4 %s vs (C9) %s; relative differences %s -> %s' % (
            tag, N, d1, src, fmt(ak4), fmt(ref), ' '.join('%.2e' % x for x in dv), res))
    if not full:
        return
    budget_line1(N, E)
    d = max(dev(E['GxR,%d,%d' % (h, g)][0], E['Gx,%d,%d' % (g, h)][0]) for (g, h) in SWAP)
    rr = max(abs(sum(E['GxR,%d,%d' % (h, g)][1].values()) / sum(E['Gx,%d,%d' % (g, h)][1].values()) - 1) for (g, h) in SWAP)
    out('C-GXSYM N=%d: GxR,h,g against Gx,g,h (3 pairs): a_k worst %.2e -> %s; remainder relative difference worst %.2e (INFO)' % (
        N, d, gate(fails, 'C-GXSYM N=%d' % N, d <= TOL), rr))
    d = dev(E['IhT,0'][0], ih0)
    out('C-IHT0 N=%d: IhT,0 (xi on (1,4)) against kt_s9b_v2 Ih,0 (xi on (4,7)): a_k worst %.2e (plan v2 asked 1e-14) -> %s; '
        'remainder ratio %.6f (INFO)' % (N, d, gate(fails, 'C-IHT0 N=%d' % N, d <= TOL), sum(E['IhT,0'][1].values()) / sum(ih0B.values())))
    mh = mhat(R3)
    worst, parts = 0.0, []
    for g in EVEN:
        ref, a = conv(mh, E['Gx,0,%d' % g][0]), E['IhT,%d' % g][0]
        d = dev(a, ref, (0, 1))
        worst = max(worst, d)
        parts.append('g=%d: a_0, a_1 %.2e (a_2 %+.4e, a_3 %+.4e)' % (g, d, a[2] - ref[2], a[3] - ref[3]))
    out('C-IHT1 N=%d: IhT_g against m-hat * Gx_0g: %s -> %s' % (N, '; '.join(parts), gate(fails, 'C-IHT1 N=%d' % N, worst <= TOL)))
    ih1 = v2_entry(N, 'Ih,1')[0]
    d = dev(ih1, conv(mh, E['Gx,0,1'][0]), (0, 1))
    out('PLANT-IHT1 N=%d: kt_s9b_v2 Ih,1 in place of IhT,1: a_0, a_1 %.2e -> %s' % (N, d, 'FIRES' if d > TOL else 'DOES NOT FIRE'))
    if d <= TOL:
        nofire.append('PLANT-IHT1 N=%d' % N)
    ih3 = v2_entry(N, 'Ih,3')[0]
    x1, x3 = X0 * E['Gx,0,1'][0][0], Y0 * E['Gx,0,3'][0][0]
    out('INFO C-IH1 N=%d: Ih,1 a_0 %r vs X0 Gx_01 a_0 %r (difference %.2e); Ih,3 a_0 %r vs Y0 Gx_03 a_0 %r (difference %.2e)' % (
        N, ih1[0], x1, ih1[0] - x1, ih3[0], x3, ih3[0] - x3))
    t, parts = 1.0 / J, []
    for g in EVEN:
        akp, Bp = E['Gp,%d' % g]
        akg, Bg = v2_entry(N, 'G,%d,%d' % (g, g))
        num = sum(akp[k] * t ** k for k in range(4)) + sum(Bp.values())
        den = sum(akg[k] * t ** k for k in range(4)) - sum(Bg.values())
        parts.append('kappa_%d <= %.6f' % (g, math.sqrt(num / den)))
    out('INFO KAPPA N=%d (S9C_PLAN_v2_ADD1 sect. 4(b), float, J = 300): %s (plan v2 used 1.5 [E])' % (N, ', '.join(parts)))


def item():
    fails, nofire = [], []
    complete = False
    try:
        for N in ((3, 4) if MODE == 'smoke' else (int(MODE[1]),)):
            run_n(N, MODE != 'smoke', fails, nofire)
        complete = True
    except CapStop as e:
        out('CAP-STOP before %s at cpu %.1f s (LIM %d)' % (e, cpu(), LIM))
    why = fails + ['%s did not fire' % x for x in nofire] + ([] if complete else ['INCOMPLETE'])
    out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (MODE, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))


def main():
    try:
        item()
    except Exception as e:
        traceback.print_exc()
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        out('VERDICT INVALID (ERROR)')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
