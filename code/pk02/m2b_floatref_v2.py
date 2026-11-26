#!/usr/bin/env python3
"""m2b_floatref_v2.py -- pk02 (code/pk02/). REVISION of m2b_floatref_v1.py (06fa61bc) for the two trade fixes: the FLOAT references
for m2b_cert_v1_3's pieces, with the majorants of the shared fix majfix_v1.py (its binary64 mode, the algorithm m2b_cert_v1_3 runs in balls).
Changes, and nothing else (DIFF_m2b_floatref_v1_to_v2.txt):
  - D5 and D5W (fix_pis_d5): pi_vac built untraded (M3's form) and capped at TOT - maxdeg(Y[5 - j]), TOT the total degree of today's D5
    (vacrig11f's pi_j with its trade, which stays verbatim above for that degree only); radii a_m, a_e (radv_for).
  - R0 and R0W: pi_vac untraded (no cap; Wishart only).
  - ANN (fix_pi0pp): pi_vac(0) at a_pp untraded, capped at today's pi0'' degree, radii a_pp on sigma''.
  - majfix_v1.py pinned (C-HASH) and imported from this folder (C-IMPORT); the header line and usage name this file. The FIX line prints
    the budgets and the cap's step counts. Every other quantity (NP, R1, NPM_*, R1_*, TX_*, TB) is v1's, unchanged.
Run as v1 below with this file's name and a NEW output path (out_m2b_floatref_v2_n<N>.out).
m2b_floatref_v1 was: pk02 (code/pk02/). The FLOAT references for m2b_cert_v1's port items (SPEC_M2B_CERT_v1 sect. 5, C-REP):
the same quantities in the same forms, in float64, with pk10's float engines (vacmod2, condexp2, condpoly3, condg, wishart, amom2b, npoly,
sha256 pinned). vacrig11f's builders are copied verbatim below (its l.62-163 and l.166-224, checked by C-VERBATIM); the Minkowski forms are
vacmono's (l.84-115), the weights vacrig11w's (l.276-301), and tailB is kt_cert's F1 per-bond form, in float. Not FLOAT inputs of any record:
m2b_rep_v1 compares m2b_cert_v1's balls with these values.
On the trial vacuum vacres_K3_N<N>_sym_v1.json (pk11/out), N = argv[1] in {3, 4}; J1 = 150, J0 = 170; rho_m 0.55, rho_e 0.6, delta 40 deg.
Prints one line 'FREF N=<N> <key> <value %.12e>' per quantity:
  NP, R1 (J1; nP = sum_{k=2..4} t1^k ||r_k||, R1 = t1 ||r1||), NPM_wt, R1_wt, NPM_dl, R1_dl (J0; per order, ||lin_w P|| + ||B_w P||),
  D5 (J1), D5W_wt, D5W_dl (J0), R0 (J1), R0W_wt, R0W_dl (J0), TX_<lam> (J1, lam in 0.3, 0.45, 0.6: the root of the sum over the three
  tables), TB (J1, F1 form, lambda 0.45), ANN_<lam> (J1).
Run (own folder): D=/mnt/g2/release/root/code/pk02; o=$D/out/out_m2b_floatref_v1_n<N>.out; [ ! -e "$o" ] &&
  OMP_NUM_THREADS=1 timeout 580 nice -n 10 /usr/bin/time -v prlimit --as=8589934592 -- python3 -I -B $D/m2b_floatref_v1.py <N>
  > "$o" 2> "${o%.out}.err"

"""
import sys, os, math, time, json, hashlib, resource

OWN = '/mnt/g2/release/root/code/pk02'
SCR = '/mnt/g2/release/root/code/pk10/scripts'
WOUT = '/mnt/g2/release/root/code/pk11/out'
SCRATCH = '/mnt/g2/release/root/code/pk10/scratch'
ENGINE = {
    'pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
    'condexp2.py': 'c38c284e1ee764d064c9d946d98fef1976fdf2821c98767a3085c6f31d4f25af',
    'condpoly3.py': 'f36c21c15138699f030f0d76a6e380e225b886a4e16bacc4df940a20a810a0c0',
    'condg.py': '0c669ea7cd193ce58d74d515dd8036f7af08f14564da599a86ea79f296106236',
    'wishart.py': 'b79933910a0e82909fa1d3a1a069ac937ad5a0c696a0dfd28200b5a79b0f7c06',
    'amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc',
    'npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
    'vacmod2.py': '533546b173af147a56e9531e26afa64cb3dbaccefd5fb7b1283f03baff06a000',
    'vacrig11f.py': 'c2d6c059adaee674e5bc9cdc2fe96f97a73ac9042eda620c1e259f734e870eff',
    'vacrig11w.py': 'bf2a9de15d3c17c6c6302157509b784c65b1030fab3851a0565abc0b8ef2eee6',
    'vacmono.py': 'd930f997afc01e1cd26714e38b095447f3fe2bd5d18ed0937c63f20fa4511c47',
}
TRIAL = {
    'vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    'vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
}
KBARF = {
    'm2_N3_J170.json.b': '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    'm2_N4_J170.json.b': '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
}
NN = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] in ('3', '4') else 0
if NN == 0:
    print('usage: m2b_floatref_v2.py 3|4')
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (540, 545))


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


print('m2b_floatref_v2 sha256 %s N=%d' % (sha(os.path.abspath(__file__)), NN), flush=True)
MAJFIX = {'majfix_v1.py': '742b8b8bf7c0f6d9ab797e2f45a02855eac6ac4520040d49fe97cdd205d43c40'}                       # m2b_floatref_v2: the shared trade fix (OWN), binary64 mode
bad = ['%s' % n for d, tab in ((SCR, ENGINE), (WOUT, TRIAL), (SCRATCH, KBARF), (OWN, MAJFIX)) for n, h in sorted(tab.items()) if sha(os.path.join(d, n)) != h]
print('C-HASH %s%s' % ('PASS' if not bad else 'FAIL', (': ' + ', '.join(bad)) if bad else ''), flush=True)
if bad:
    print('VERDICT INVALID (C-HASH)')
    sys.exit(2)
sys.path.insert(0, SCR)
import numpy as np
from scipy.special import erfc
from vacmod2 import Builder, ltri, XS, QS, XD, QD, PAIRS, BASIS, A_EX, B_EX
from pseries import padd, pscale, pmul
from condexp2 import CondMom
from condpoly3 import SigmaPolys, CondSigma
from condg import CondG, sigma_to_g
from wishart import Wishart
from amom2b import AllMom2
from npoly import NPoly
sys.path.insert(0, OWN)
import majfix_v1 as mf
if os.path.realpath(mf.__file__) != os.path.realpath(os.path.join(OWN, 'majfix_v1.py')):
    print('C-IMPORT FAIL: majfix_v1 from %s' % mf.__file__)
    sys.exit(2)

t0c = time.process_time()
nn = NN - 1
with open(os.path.join(WOUT, {4: 'vacres_K3_N4_sym_v1.json', 3: 'vacres_K3_N3_sym_v1.json'}[NN])) as fh:
    R3 = json.load(fh)
with open(os.path.join(SCRATCH, {4: 'm2_N4_J170.json.b', 3: 'm2_N3_J170.json.b'}[NN])) as fh:
    KBAR = json.load(fh)['kbar']
q = [None, R3['q1'], R3['q2'], R3['q3']]
mser = [1.0, R3['m1'], R3['m2'], R3['m3']]
rho_m, rho_e, delta = 0.55, 0.6, math.radians(40.0)
a_m, a_e = rho_m ** 2, rho_e ** 2
c_m, c_e = (-math.log(1 - x) / (2 * x) for x in (a_m, a_e))
ang2 = math.asin(rho_m) + delta
rho_pp = math.sin(ang2); a_pp = rho_pp ** 2; c_pp = -math.log(1 - a_pp) / (2 * a_pp)
a, b = A_EX, B_EX
NV, BB = 12, 26
AVt = [a_m] * 3 + [None] * 3 + [a_e] * 3 + [None] * 3
A = np.eye(3) + ltri()
Ainv = np.linalg.inv(A)
W2 = np.zeros((3, 6))
for r in range(3):
    W2[r, r] = 1.0
for p_, (r, s) in enumerate(PAIRS):
    W2[r, 3 + p_] = 1.0; W2[s, 3 + p_] = -1.0
# ---------------------------------------------------------------- vacrig11f.py (9d57f823) l.62-163, verbatim
ONE = NPoly(NV, BB, np.zeros(1, dtype=np.int64), np.ones(1))


def mono(e, c=1.0):
    return NPoly(NV, BB, np.array([int(sum(int(x) * BB ** i for i, x in enumerate(e)))], dtype=np.int64), np.array([c]))


def xv(i, k=1, c=1.0):
    e = [0] * NV; e[i] = k
    return mono(e, c)


def D2(i, j):
    return xv(i, 2).add(xv(i, 1).mul(xv(j, 1)).scale(-2.0)).add(xv(j, 2))


def Mk(i, j, k):
    return ONE if k == 0 else xv(i, k).add(xv(j, k))


def trade(p, t, nt):
    ex = np.stack([(p.codes // p.pw[i]) % p.B for i in range(NV)], axis=1)
    out_e, out_c = [], []
    qa = {3: 4 * a_m, 4: 4 * a_m, 5: 4 * a_m, 9: 4 * a_e, 10: 4 * a_e, 11: 4 * a_e}
    for row, c in zip(ex, p.coeffs):
        row = row.copy(); fac = c
        for _ in range(nt):
            cand = [(row[i], i) for i in range(NV) if row[i] > 0]
            if not cand:
                fac *= t; continue
            _, i = max(cand)
            row[i] -= 1
            fac *= AVt[i] if AVt[i] is not None else qa[i]
        out_e.append(row); out_c.append(fac)
    res = NPoly(NV, BB, np.array(out_e, dtype=np.int64) @ p.pw, np.array(out_c))
    res._normalize()
    return res


def hk(k, meas_vertices, bonds, cfac):
    """derivative majorant; cfac(x) supplies the radius factors (1-a)^{-x} (or 1 when they are moved into a tilt)."""
    out = NPoly(NV, BB)
    for (v, av) in meas_vertices:
        out = out.add(xv(v, k, math.factorial(k - 1) / 2.0 * cfac(av, k)))
    for (iu, iv, c, aa) in bonds:
        out = out.add(D2(iu, iv).mul(Mk(iu, iv, k - 1)).scale((c / 2.0) * math.factorial(k) / 4.0 * cfac(aa, k + 1)))
    return out


def xibar(Xi, Qi, aa, t, nmax, cfac):
    res = []
    for p_, (r, s) in enumerate(PAIRS):
        Dx = D2(Xi[r], Xi[s])
        lst = [xv(Qi[p_], 1, 0.5).add(trade(Dx.scale(cfac(aa, 1) / 8.0), t, 1))]
        for l in range(1, nmax + 1):
            lst.append(Dx.mul(Mk(Xi[r], Xi[s], l - 1)).scale(math.factorial(l) / 8.0 * cfac(aa, l + 1)))
        res.append(lst)
    return res


def fbd(xd, mono_, n):
    if len(mono_) == 1:
        return xd[mono_[0]][n]
    e1, e2 = mono_
    out = NPoly(NV, BB)
    for l in range(n + 1):
        out = out.add(xd[e1][l].mul(xd[e2][n - l]).scale(float(math.comb(n, l))))
    return out


def pi_j(j, Xi, Qi, aa, t, cfac):
    xd = xibar(Xi, Qi, aa, t, j, cfac)
    out = ONE if j == 0 else NPoly(NV, BB)
    for i in (1, 2, 3):
        for cb, mono_ in zip(q[i], BASIS):
            if cb == 0.0:
                continue
            for l in range(0, min(i, j) + 1):
                coef = math.comb(j, l) * (math.factorial(i) / math.factorial(i - l)) * abs(cb)
                term = fbd(xd, mono_, j - l).scale(coef)
                out = out.add(trade(term, t, i - l) if i - l > 0 else term)
    return out


def Dbar(n, h, pis):
    Y = [ONE]
    for mm in range(n):
        acc = NPoly(NV, BB)
        for i in range(mm + 1):
            acc = acc.add(h[i + 1].mul(Y[mm - i]).scale(float(math.comb(mm, i))))
        Y.append(acc)
    out = NPoly(NV, BB)
    for j in range(n + 1):
        out = out.add(pis[j].mul(Y[n - j]).scale(float(math.comb(n, j))))
    return out


cf_one = lambda aa, k: 1.0
cf_rad = lambda aa, k: (1.0 - aa) ** (-k)
bondsL = [(XD[r], XD[s], [a, a, b][p_], a_e) for p_, (r, s) in enumerate(PAIRS)] + \
         [(XS[r], XD[r], 1.0, max(a_m, a_e)) for r in range(3)] + [(XS[0], XS[1], 1.0, a_m), (XS[1], XS[2], 1.0, a_m)]
bonds0 = [(XS[r], XS[s], [a, a, b][p_], a_m) for p_, (r, s) in enumerate(PAIRS)]
# ---------------------------------------------------------------- vacrig11f.py (9d57f823) l.166-224, verbatim
def lap(edges, V):
    L = np.zeros((V, V))
    for (u, v), c in edges:
        L[u, u] += c; L[v, v] += c; L[u, v] -= c; L[v, u] -= c
    return L


def gauge_basis(V, S):
    u = np.zeros(V); u[list(S)] = 1.0
    return np.linalg.svd(np.eye(V) - np.outer(u, u) / u.dot(u))[0][:, :V - 1]


def tilted_cov(L, Bm, rates, extra=None):
    Lr = Bm.T @ L @ Bm
    Lx = L - 2 * np.diag(rates)
    if extra is not None:
        Lx = Lx - 2 * extra
    Lt = Bm.T @ Lx @ Bm
    if np.linalg.eigvalsh(Lt).min() <= 0:
        return None, float("inf")
    return Bm @ np.linalg.inv(Lt) @ Bm.T, (np.linalg.det(Lr) / np.linalg.det(Lt)) ** (0.5 * nn)


def chi_tail(s):
    return math.exp(-s / 2) if nn == 2 else erfc(math.sqrt(s / 2)) + math.sqrt(2 * s / math.pi) * math.exp(-s / 2)


E9 = [((6 + r, 6 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((6 + r, r), 1.0) for r in range(3)] + [((r, 3 + r), 1.0) for r in range(3)] + [((0, 1), 1.0), ((1, 2), 1.0)]
L9 = lap(E9, 9); B9 = gauge_basis(9, range(6))
ED_ = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \
      [((r, 3 + r), 1.0) for r in range(3)]
LD = lap(ED_, 6); BD = gauge_basis(6, range(6))
W12 = np.zeros((6, 12))
for blk in range(2):
    for r in range(3):
        W12[3 * blk + r, 6 * blk + r] = 1.0
    for p_, (r, s) in enumerate(PAIRS):
        W12[3 * blk + r, 6 * blk + 3 + p_] = 1.0; W12[3 * blk + s, 6 * blk + 3 + p_] = -1.0
IDX9F = [0, 1, 2, 6, 7, 8, 9, 10, 11]


def joint_moments(rates9, Dmax):
    G9, N9 = tilted_cov(L9, B9, rates9)
    if G9 is None:
        return None, float("inf"), None
    idx = [0, 1, 2, 6, 7, 8]
    G6 = G9[np.ix_(idx, idx)]
    return AllMom2(G6, nn, Dmax, W=W12[:, IDX9F], groups=[0] * 6 + [1] * 3, caps={1: 4}), N9, G9


def to9(P):
    out = {}
    for e, c in P.items():
        assert e[3] == e[4] == e[5] == 0
        e9 = tuple(e[i] for i in IDX9F)
        out[e9] = out.get(e9, 0.0) + c
    return out

# ---------------------------------------------------------------- the references
FAILS = []
with open(os.path.abspath(__file__)) as fh:
    own = fh.read().split('\n')
with open(os.path.join(SCR, 'vacrig11f.py')) as fh:
    src = fh.read().split('\n')
i1 = own.index('# ---------------------------------------------------------------- vacrig11f.py (9d57f823) l.62-163, verbatim')
i2 = own.index('# ---------------------------------------------------------------- vacrig11f.py (9d57f823) l.166-224, verbatim')
okv = own[i1 + 1:i1 + 103] == src[61:163] and own[i2 + 1:i2 + 60] == src[165:224]
print('C-VERBATIM: the copied blocks equal vacrig11f.py l.62-163 and l.166-224 -> %s' % ('PASS' if okv else 'FAIL'))
if not okv:
    FAILS.append('C-VERBATIM')
# ---------------------------------------------------------------- m2b_floatref_v2: the trade fix (majfix_v1, binary64 mode)
FB = mf.FormBasis(NV, list(XS) + list(XD), list(QS) + list(QD), num=float)
RADV_MAIN = mf.radv_for(a_e, a_m, a_e, num=float)
RADV_ANN = mf.radv_for(a_pp, a_m, a_e, num=float)
FIXSTAT = {}


def fix_pis_d5(t, h):
    """D5's pis: majfix_v1's untraded pi_vac (inner, a_e), capped at TOT - maxdeg(Y[5 - j]) with TOT the total degree of today's D5
    (vacrig11f's pi_j with its trade, verbatim above), so the CondMom table keeps its size."""
    D5old = Dbar(5, h, [pi_j(j, XD, QD, a_e, t, cf_rad) for j in range(6)])
    tot = int(D5old.degrees().max())
    yd = mf.ydegs(h, 5, ONE, NPoly, BB, NV)
    budgets = [tot - yd[5 - j] for j in range(6)]
    FIXSTAT['d5'] = (tot, budgets)
    return [FB.evaluate(FB.cap(FB.pi_vac(j, XD, QD, PAIRS, a_e, q, BASIS), budgets[j], RADV_MAIN, FIXSTAT), t, NPoly, BB, D2) for j in range(6)]


def fix_pi0pp(t):
    """ann's pi0'': majfix_v1's untraded pi_vac(0) at a_pp, capped at today's degree (vacrig11f's pi_j(0) at a_pp), radii a_pp on sigma''."""
    dA = int(pi_j(0, XD, QD, a_pp, t, cf_rad).degrees().max())
    FIXSTAT['ann'] = dA
    return FB.evaluate(FB.cap(FB.pi_vac(0, XD, QD, PAIRS, a_pp, q, BASIS), dA, RADV_ANN, FIXSTAT), t, NPoly, BB, D2)


LAMS = (0.3, 0.45, 0.6)
J1, J0 = 150.0, 170.0


def emit(key, v):
    print('FREF N=%d %s %.12e' % (NN, key, v), flush=True)


def joint_moments_x(rates9, Dmax, extra):
    """vacrig11f.joint_moments with an optional 9 x 9 quadratic tilt (kt_cert's F1 form)."""
    G9, N9 = tilted_cov(L9, B9, rates9, extra=extra)
    if G9 is None:
        return None, float("inf"), None
    idx = [0, 1, 2, 6, 7, 8]
    G6 = G9[np.ix_(idx, idx)]
    return AllMom2(G6, nn, Dmax, W=W12[:, IDX9F], groups=[0] * 6 + [1] * 3, caps={1: 4}), N9, G9


def lin_w(w):
    """vacrig11w's lin (l.284-289), in the g variables."""
    d = {(0, 0, 0, 1, 0, 0): 0.25, (0, 0, 0, 0, 1, 0): 0.25 if w == 'wt' else -0.25}
    if w == 'wt':
        d[(0, 0, 0, 0, 0, 0)] = -KBAR
    return sigma_to_g(d)


def b_w(t):
    """vacrig11w's B_g (l.297-298)."""
    cB = t / (16 * (1 - a_m))
    return sigma_to_g({(2, 0, 0, 0, 0, 0): cB, (1, 1, 0, 0, 0, 0): -2 * cB, (0, 2, 0, 0, 0, 0): 2 * cB, (0, 1, 1, 0, 0, 0): -2 * cB,
                       (0, 0, 2, 0, 0, 0): cB})


def wnorm(w2, P, nfac, lg, bg):
    """vacrig11w's wnorm (l.299-301), summed."""
    PL, PB = pmul(lg, P), pmul(bg, P)
    return math.sqrt(nfac * max(w2.E2(PL, PL), 0.0)) + math.sqrt(nfac * max(w2.E2(PB, PB), 0.0))


# explicit part: r_1..r_4 by the conditional expectation (vacrig11f l.47-57 for every k, as m2b_cert_v1)
bd = Builder(4)
L1 = bd.L1(q[1], q[2], q[3])
L0 = bd.L0(q[1], q[2], q[3])
cm8 = CondMom(Ainv, Ainv, W2, nn, 8, groups=[0, 0, 0, 1, 1, 1], caps={1: 2})
sp8 = SigmaPolys(8)
cs8 = CondSigma(cm8, sp8)
rk = {}
for k in range(1, 5):
    mL0 = {}
    for e, c in padd(*[pscale(L0.c[k - j], mser[j]) for j in range(min(k, 3) + 1)]).items():
        mL0[e[:6]] = mL0.get(e[:6], 0.0) + c
    rk[k] = sp8.to_dict(cs8.condE(L1.c[k]) - sp8.from_dict(mL0))
rkg = {k: sigma_to_g(v) for k, v in rk.items()}
dmax = max(sum(e) for v in rkg.values() for e in v)
t1, t0 = 1.0 / J1, 1.0 / J0
G1, n1 = tilted_cov(LD, BD, np.full(6, c_m * t1))
w1 = Wishart(G1[:3, :3], nn, 2 * dmax)
nk = {k: math.sqrt(n1 * max(w1.E2(rkg[k], rkg[k]), 0.0)) for k in rkg}
emit('NP', sum(t1 ** k * nk[k] for k in (2, 3, 4)))
emit('R1', t1 * nk[1])
G0, n0 = tilted_cov(LD, BD, np.full(6, c_m * t0))
w0 = Wishart(G0[:3, :3], nn, 2 * dmax + 4)
bg0 = b_w(t0)
for w in ('wt', 'dl'):
    wn = {k: wnorm(w0, rkg[k], n0, lin_w(w), bg0) for k in rkg}
    emit('NPM_' + w, sum(t0 ** k * wn[k] for k in (2, 3, 4)))
    emit('R1_' + w, t0 * wn[1])
print('explicit part done (%.1f s)' % (time.process_time() - t0c), flush=True)


def d5(t, weighted):
    """vacrig11f l.294-313 (and vacrig11w l.317-326 for the weights)."""
    h = {k: hk(k, [(v, a_e) for v in XD], bondsL, cf_rad) for k in range(1, 6)}
    pis = fix_pis_d5(t, h)                    # m2b_floatref_v2: the trade fix (majfix_v1, budgets from today's D5)
    D5 = Dbar(5, h, pis)
    ex5 = np.stack([(D5.codes // D5.pw[i]) % D5.B for i in range(NV)], axis=1)
    deg2 = int(ex5[:, 6:].sum(axis=1).max()); qdeg = int(ex5[:, 9:].sum(axis=1).max()); tot = int(ex5.sum(axis=1).max())
    At = A - 2 * c_e * t * np.eye(3)
    Ati = np.linalg.inv(At)
    detf = (np.linalg.det(A) / np.linalg.det(At)) ** (0.5 * nn)
    Delta = Ati - Ainv
    cmT = CondMom(Ati, Ati, W2, nn, deg2, groups=[0, 0, 0, 1, 1, 1], caps={1: max(qdeg, 1)})
    cgT = CondG(cmT, tot)
    ED = cgT.out.to_dict(cgT.condE(D5.to_dict()))
    ext = np.zeros((6, 6)); ext[:3, :3] = Delta
    G2, n2 = tilted_cov(LD, BD, np.full(6, c_m * t), extra=ext)
    dED = max(sum(e) for e in ED)
    w2 = Wishart(G2[:3, :3], nn, 2 * dED + (4 if weighted else 0))
    if not weighted:
        return (t ** 5 / 120.0) * detf * math.sqrt(n2 * max(w2.E2(ED, ED), 0.0))
    return {w: (t ** 5 / 120.0) * detf * wnorm(w2, ED, n2, lin_w(w), b_w(t)) for w in ('wt', 'dl')}


emit('D5', d5(t1, False))
for w, v in d5(t0, True).items():
    emit('D5W_' + w, v)
print('D5 done (%.1f s)' % (time.process_time() - t0c), flush=True)


def r0g(t):
    """vacrig11f l.316-327."""
    h0 = {k: hk(k, [], bonds0, cf_rad) for k in range(1, 6)}
    mfull = mser + [0.0]
    R0 = NPoly(NV, BB)
    for j in range(5):
        n_ = 4 - j
        pis0 = [FB.evaluate(FB.pi_vac(i, XS, QS, PAIRS, a_m, q, BASIS), t, NPoly, BB, D2) for i in range(n_ + 2)]   # v2: untraded
        R0 = R0.add(Dbar(n_ + 1, h0, pis0).scale(abs(mfull[j]) * t ** j * t ** (n_ + 1) / math.factorial(n_ + 1)))
    return sigma_to_g({e[:6]: c for e, c in R0.to_dict().items()})


R01 = r0g(t1)
w1r = Wishart(G1[:3, :3], nn, 2 * max(sum(e) for e in R01))
emit('R0', math.sqrt(n1 * max(w1r.E2(R01, R01), 0.0)))
R00 = r0g(t0)
w0r = Wishart(G0[:3, :3], nn, 2 * max(sum(e) for e in R00) + 4)
for w in ('wt', 'dl'):
    emit('R0W_' + w, wnorm(w0r, R00, n0, lin_w(w), bg0))
Lk = [to9(L1.c[k]) for k in range(5)]
dT = max(sum(e) for P in Lk for e in P)
for lam in LAMS:
    acc = 0.0
    for v in range(3):
        rates9 = np.array([c_m * t1] * 6 + [0.0] * 3); rates9[6 + v] += lam
        am9, N9, _ = joint_moments(rates9, 2 * dT)
        s = sum(t1 ** k * math.sqrt(max(am9.E2(P, P), 0.0)) for k, P in enumerate(Lk) if P)
        acc += math.exp(-lam * J1 * a_e) * N9 * s * s
    emit('TX_%g' % lam, math.sqrt(acc))
amax = max(a_m, a_e)
kappa = 2 * (1 - math.cos(delta)) - amax ** 2 / (4 * (1 - amax))
acc = 0.0
for r in range(3):
    extra = np.zeros((9, 9)); extra[r, r] = extra[6 + r, 6 + r] = 0.45; extra[r, 6 + r] = extra[6 + r, r] = -0.45
    am9, N9, _ = joint_moments_x(np.array([c_m * t1] * 6 + [0.0] * 3), 2 * dT, extra)
    s = sum(t1 ** k * math.sqrt(max(am9.E2(P, P), 0.0)) for k, P in enumerate(Lk) if P)
    acc += math.exp(-0.45 * J1 * kappa) * N9 * s * s
emit('TB', math.sqrt(acc))
P0d = to9(fix_pi0pp(t1).to_dict())             # m2b_floatref_v2: capped at today's degree, radii a_pp on sigma''
dA = max(sum(e) for e in P0d)
for lam in LAMS:
    acc = 0.0
    for v in range(3):
        rates9 = np.array([c_m * t1] * 6 + [2 * c_pp * t1] * 3); rates9[6 + v] += lam
        am9, N9, _ = joint_moments(rates9, 2 * dA)
        acc += math.exp(-lam * J1 * a_e) * N9 * max(am9.E2(P0d, P0d), 0.0)
    emit('ANN_%g' % lam, math.sqrt(acc))
print('FIX N=%d: D5 budgets %s (today\'s total degree %d), ann budget %d; cap calls %d, steps %d, atom splits %d' % (
    NN, ','.join(str(b) for b in FIXSTAT['d5'][1]), FIXSTAT['d5'][0], FIXSTAT['ann'], FIXSTAT.get('calls', 0), FIXSTAT.get('steps', 0),
    FIXSTAT.get('splits', 0)), flush=True)
print('FLOATREF N=%d cpu %.1f s, peak rss %.0f MiB' % (NN, time.process_time() - t0c, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
print('VERDICT %s' % ('VALID' if not FAILS else 'INVALID (%s)' % ', '.join(FAILS)))
