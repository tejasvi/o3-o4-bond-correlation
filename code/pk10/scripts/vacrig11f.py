#!/usr/bin/env python3
# pk10 (code): s19.2 vacuum residual bound, v10.  Usage: vacrig10.py OUTFILE VACRES3N_JSON N RHO_M RHO_E DELTA_DEG J1,...
# Decomposition g = g_G + g_B, g_B = V(sigma) int K(sigma,sigma'') phi(sigma'') 1_bad (bad: some horizontal bond sigma_r--sigma''_r at angle > delta).
#   ||K^{1/2} g_B||^2 / main4 <= sup|p|^2 sum_r e^{-th J (1 - cos delta)} Z_{G4 - r}/main4     (single-bond theta-split, riglap2 for G4 - r)
#   g_G: for (sigma, sigma') in Omega_out (|pi_v| <= rho_m on the middle columns), in the chart:
#     g_G / norm = sum_{k=2}^4 t^k r_k + delta1,
#     |delta1| <= E[|T4 L1| (1_{Omega''^c} + 1_bad) | s] + t^5/120 E[e^{r'' t sum X''} Dt5 | s] e^{r_s t sum X_s} + E[pi0'' e^{c'' t sum X''} 1_{X''_v > J a_e} | s] + R0(s)
#     (Dt5: order-5 derivative majorant with every (1 - tau x)^{-j} replaced by exp(j tau x/(1-a)); j <= 12 per vertex)
#   outer far (some middle vertex beyond rho_m): S-gauge per-vertex energy + theta-split + tree bounds.
import sys, json, math, time
import numpy as np
from scipy.special import ive, erfc
sys.path.insert(0, "/mnt/g2/release/root/code/pk10/scripts")
from vacmod2 import Builder, ltri, XS, QS, XD, QD, PAIRS, BASIS, A_EX, B_EX
from pseries import padd, pscale, pmul, pconst
from condexp2 import CondMom
from condpoly3 import SigmaPolys, CondSigma
from condg import CondG, GSpace, sigma_to_g
from wishart import Wishart
from amom2b import AllMom2
from npoly import NPoly
import riglap2

outf, resf, NN = sys.argv[1], sys.argv[2], int(sys.argv[3])
rho_m, rho_e, delta = float(sys.argv[4]), float(sys.argv[5]), math.radians(float(sys.argv[6]))
Js = [float(x) for x in sys.argv[7].split(",")]
nn = NN - 1
R3 = json.load(open(resf))
q = [None, R3["q1"], R3["q2"], R3["q3"]]
a_m, a_e = rho_m ** 2, rho_e ** 2
c_m, c_e = (-math.log(1 - x) / (2 * x) for x in (a_m, a_e))
ang2 = math.asin(rho_m) + delta
assert ang2 < math.pi / 2
rho_pp = math.sin(ang2); a_pp = rho_pp ** 2; c_pp = -math.log(1 - a_pp) / (2 * a_pp)
JMAX = 12
a, b = A_EX, B_EX
NV, BB = 12, 26
AVt = [a_m] * 3 + [None] * 3 + [a_e] * 3 + [None] * 3        # for trading explicit t's
t0 = time.time()
A = np.eye(3) + ltri()
Ainv = np.linalg.inv(A)
W2 = np.zeros((3, 6))
for r in range(3):
    W2[r, r] = 1.0
for p_, (r, s) in enumerate(PAIRS):
    W2[r, 3 + p_] = 1.0; W2[s, 3 + p_] = -1.0
bd = Builder(4)
L1 = bd.L1(q[1], q[2], q[3])
L0 = bd.L0(q[1], q[2], q[3])
mser = [1.0, R3["m1"], R3["m2"], R3["m3"]]
cm8 = CondMom(Ainv, Ainv, W2, nn, 8, groups=[0, 0, 0, 1, 1, 1], caps={1: 2})
sp8 = SigmaPolys(8)
cs8 = CondSigma(cm8, sp8)
mL04 = {}
for e, c in padd(*[pscale(L0.c[4 - j], mser[j]) for j in range(4)]).items():
    mL04[e[:6]] = mL04.get(e[:6], 0.0) + c
r4 = sp8.to_dict(cs8.condE(L1.c[4]) - sp8.from_dict(mL04))
rk = {2: {tuple(int(x) for x in k.split(",")): v for k, v in R3["r2"].items()},
      3: {tuple(int(x) for x in k.split(",")): v for k, v in R3["r3"].items()}, 4: r4}
rkg = {k: sigma_to_g(v) for k, v in rk.items()}
print("explicit part built (%.1f s)" % (time.time() - t0)); sys.stdout.flush()
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


def far_rel(edges, V, S, J, aa):
    L = lap(edges, V)
    Bm_ = gauge_basis(V, S)
    GS = Bm_ @ np.linalg.inv(Bm_.T @ L @ Bm_) @ Bm_.T
    g_ = riglap2.Graph(V, dict(edges), [], N=NN)
    tree = riglap2.tree_couplings(g_)
    if NN == 4:
        lt = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        lt = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    return math.exp(min(math.log(sum(math.exp(-th * J * aa / (2 * GS[v, v])) for v in S)) + lt((1 - th) * J) - g_.logmain(J)
                        for th in np.linspace(0.01, 0.99, 197)))


E4 = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + [((9 + r, 9 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((r, 3 + r), 1.0) for r in range(3)] + [((3 + r, 6 + r), 1.0) for r in range(3)] + [((6 + r, 9 + r), 1.0) for r in range(3)] + \
     [((3, 4), 1.0), ((4, 5), 1.0), ((6, 7), 1.0), ((7, 8), 1.0)]
E3 = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + [((6 + r, 6 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((r, 3 + r), 1.0) for r in range(3)] + [((3 + r, 6 + r), 1.0) for r in range(3)] + [((3, 4), 1.0), ((4, 5), 1.0)]
RHO_P = 0.9
A_P = RHO_P ** 2
C_P = -math.log(1 - A_P) / (2 * A_P)


def outer_far(edges, V, S, pcols, J):
    """bound, relative to the graph's main term, of the integral with |p| on pcols over {some v in S with |pi_v| > rho_m (S-gauge pole)}:
    chart part (all |pi| <= rho'): E_{S-gauge}[e^{c' t sum X} pbar pbar' e^{lam (X_v - J a_m)}] summed over v in S (Chernoff);
    truly far part (some |pi_v| > rho' or lower hemisphere): sup|p|^2 x per-vertex energy (S-gauge variances), theta-split, tree bound."""
    t = 1.0 / J
    L = lap(edges, V)
    Bm_ = gauge_basis(V, S)
    pairs = []
    for c_ in pcols:
        pairs += [(c_[0], c_[1]), (c_[1], c_[2]), (c_[0], c_[2])]
    g_ = riglap2.Graph(V, dict(edges), pairs, N=NN)
    m_ = riglap2.Model(g_, 3, [('p', c_, q[1], q[2], q[3]) for c_ in pcols])
    mj_ = riglap2.Majorants(m_, [A_P] * V, t, B=10)
    P0 = mj_.Fbar(0)
    degP = int(P0.degrees().max())
    qP = int(np.stack([(P0.codes // P0.pw[i]) % P0.B for i in range(P0.nv)], axis=1)[:, V:].sum(axis=1).max())
    best = float("inf")
    for lam in (0.5, 1.0, 1.5):
        acc = 0.0; ok = True
        for v in S:
            rates = np.full(V, C_P * t); rates[v] += lam
            G_, N_ = tilted_cov(L, Bm_, rates)
            if G_ is None:
                ok = False; break
            am_ = AllMom2(G_, nn, max(degP, 1), W=g_.W, groups=g_.groups, caps={1: max(qP, 1)})
            acc += math.exp(-lam * J * a_m) * N_ * riglap2.expect_np(am_, P0)
        if ok:
            best = min(best, acc)
    GS = Bm_ @ np.linalg.inv(Bm_.T @ L @ Bm_) @ Bm_.T
    tree = riglap2.tree_couplings(g_)
    if NN == 4:
        lt = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        lt = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    farp = math.exp(min(math.log(sum(math.exp(-th * J * A_P / (2 * GS[v, v])) for v in range(V))) + lt((1 - th) * J) - g_.logmain(J)
                        for th in np.linspace(0.01, 0.99, 197)))
    supp_ = 1.0 + sum(t ** i * abs(cb) * (2.0 * J) ** len(mono_) for i, coef in ((1, q[1]), (2, q[2]), (3, q[3])) for cb, mono_ in zip(coef, BASIS))
    return best + supp_ ** len(pcols) * farp


lines = ["# vacrig11: N = %d; rho_m %g rho_e %g delta %.1f deg (rho'' %.4f); eps_r for the trial vacuum (%s)" % (NN, rho_m, rho_e, math.degrees(delta), rho_pp, resf)]
for J in Js:
    t = 1.0 / J
    supp = 1.0 + sum(t ** i * abs(cb) * (2.0 * J) ** len(mono_) for i, coef in ((1, q[1]), (2, q[2]), (3, q[3])) for cb, mono_ in zip(coef, BASIS))
    mhat = 1.0 + mser[1] * t + mser[2] * t ** 2 + mser[3] * t ** 3
    # ---- D5 (radius-constant form) ----
    h = {k: hk(k, [(v, a_e) for v in XD], bondsL, cf_rad) for k in range(1, 6)}
    pis = [pi_j(j, XD, QD, a_e, t, cf_rad) for j in range(6)]
    D5 = Dbar(5, h, pis)
    ex5 = np.stack([(D5.codes // D5.pw[i]) % D5.B for i in range(NV)], axis=1)
    deg2 = int(ex5[:, 6:].sum(axis=1).max()); qdeg = int(ex5[:, 9:].sum(axis=1).max()); tot = int(ex5.sum(axis=1).max())
    r_e = c_e; r_s = 0.0
    At = A - 2 * r_e * t * np.eye(3)
    assert np.linalg.eigvalsh(At).min() > 0
    Ati = np.linalg.inv(At)
    detf = (np.linalg.det(A) / np.linalg.det(At)) ** (0.5 * nn)
    Delta = Ati - Ainv
    cmT = CondMom(Ati, Ati, W2, nn, deg2, groups=[0, 0, 0, 1, 1, 1], caps={1: max(qdeg, 1)})
    cgT = CondG(cmT, tot)
    ED = cgT.out.to_dict(cgT.condE(D5.to_dict()))
    print("  D5: %d terms, deg'' %d, total %d; conditional expectation done (%.1f s)" % (len(D5.codes), deg2, tot, time.time() - t0)); sys.stdout.flush()
    # outer weight for the D5 term: exp(c_m t sum_S X + 2 r_s t sum_sigma X + <phi_s, Delta phi_s>)
    rates = np.full(6, c_m * t); rates[:3] += 2 * r_s * t
    ext = np.zeros((6, 6)); ext[:3, :3] = Delta
    G2, n2 = tilted_cov(LD, BD, rates, extra=ext)
    w2 = Wishart(G2[:3, :3], nn, 2 * max(sum(e) for e in ED))
    nD = (t ** 5 / 120.0) * detf * math.sqrt(n2 * max(w2.E2(ED, ED), 0.0))
    # ---- explicit part and L0 remainder (outer weight exp(c_m t sum_S X)) ----
    h0 = {k: hk(k, [], bonds0, cf_rad) for k in range(1, 6)}
    mfull = mser + [0.0]
    R0 = NPoly(NV, BB)
    for j in range(5):
        n_ = 4 - j
        pis0 = [pi_j(i, XS, QS, a_m, t, cf_rad) for i in range(n_ + 2)]
        R0 = R0.add(Dbar(n_ + 1, h0, pis0).scale(abs(mfull[j]) * t ** j * t ** (n_ + 1) / math.factorial(n_ + 1)))
    R0g = sigma_to_g({e[:6]: c for e, c in R0.to_dict().items()})
    G1, n1 = tilted_cov(LD, BD, np.full(6, c_m * t))
    Pv = {}
    for k in (2, 3, 4):
        Pv = padd(Pv, pscale(rkg[k], t ** k))
    w1 = Wishart(G1[:3, :3], nn, 2 * max([sum(e) for e in Pv] + [sum(e) for e in R0g]))
    nP = math.sqrt(n1 * max(w1.E2(Pv, Pv), 0.0))
    nR0 = math.sqrt(n1 * max(w1.E2(R0g, R0g), 0.0))
    # ---- inner polynomial tails (Omega''^c by Chernoff on X''_v; bad bonds by Cauchy-Schwarz with Gaussian tails) ----
    T4_9 = to9(padd(*[pscale(L1.c[k], t ** k) for k in range(5)]))
    dT = max(sum(e) for e in T4_9)
    lams = [0.3, 0.45, 0.6]
    am0, N0, G90 = joint_moments(np.array([c_m * t] * 6 + [0.0] * 3), 2 * dT)
    normT = math.sqrt(N0 * max(am0.E2(T4_9, T4_9), 0.0))
    tailX = float("inf")
    for lam in lams:
        acc = 0.0; ok = True
        for v in range(3):
            rates9 = np.array([c_m * t] * 6 + [0.0] * 3); rates9[6 + v] += lam
            am9, N9, _ = joint_moments(rates9, 2 * dT)
            if am9 is None:
                ok = False; break
            acc += math.exp(-lam * J * a_e) * N9 * max(am9.E2(T4_9, T4_9), 0.0)
        if ok:
            tailX = min(tailX, math.sqrt(acc))
    # bad_r on Omega'': 1 - s.s'' > 1 - cos delta and (s - s'')^2 <= a^2/(4(1-a)) (a = max radius^2) => Q_rr'' > J kappa
    amax = max(a_m, a_e)
    kappa = 2 * (1 - math.cos(delta)) - amax ** 2 / (4 * (1 - amax))
    assert kappa > 0
    sbad = 0.0
    for r in range(3):
        vq = G90[r, r] + G90[6 + r, 6 + r] - 2 * G90[r, 6 + r]
        sbad += math.sqrt(chi_tail(J * kappa / vq))
    tailB = normT * sbad
    # ---- inner annulus: good minus Omega'' (chart valid, |pi''| <= rho''): |L1| <= pi0'' e^{c'' t sum X''}; Chernoff on X''_v ----
    pi0pp = pi_j(0, XD, QD, a_pp, t, cf_rad)
    P0d = to9(pi0pp.to_dict())
    dA = max(sum(e) for e in P0d)
    ann = float("inf")
    for lam in lams:
        acc = 0.0; ok = True
        for v in range(3):
            rates9 = np.array([c_m * t] * 6 + [2 * c_pp * t] * 3); rates9[6 + v] += lam
            am9, N9, _ = joint_moments(rates9, 2 * dA)
            if am9 is None:
                ok = False; break
            acc += math.exp(-lam * J * a_e) * N9 * max(am9.E2(P0d, P0d), 0.0)
        if ok:
            ann = min(ann, math.sqrt(acc))
    near = nP + nD + nR0 + tailX + tailB + ann
    # ---- bad bonds: ||K^{1/2} g_B||^2 / main4 <= supp^2 sum_r e^{-th J(1 - cos delta)} Z_{G4 - r}/main4 ----
    gB_sq = 0.0
    th = 0.95
    for r in range(3):
        edges_r = [(e_, c_) for (e_, c_) in E4 if e_ != (r, 3 + r)]
        Lfull = lap(E4, 12); Lr_ = lap(edges_r, 12)
        Q12 = np.linalg.svd(np.eye(12) - np.ones((12, 12)) / 12)[0][:, :11]
        ratio_main = (np.linalg.det(Q12.T @ Lfull @ Q12) / np.linalg.det(Q12.T @ Lr_ @ Q12)) ** (0.5 * nn)
        gR = riglap2.Graph(12, dict(edges_r), [], N=NN)
        akR, BR = riglap2.bound(gR, [], 1, (1.0) * J, [math.sqrt(min(60.0 * gR.G[v, v] / J, 0.5)) for v in range(12)], 0.9)
        zR = sum(x * t ** k for k, x in enumerate(akR)) + sum(BR.values())
        gB_sq += math.exp(-th * J * (1 - math.cos(delta))) * ratio_main * zR
    gB = supp * math.sqrt(gB_sq)
    # ---- outer far ----
    far_out = (outer_far(E4, 12, list(range(3, 9)), [(0, 1, 2), (9, 10, 11)], J) + 2 * mhat * outer_far(E3, 9, list(range(3, 9)), [(0, 1, 2), (6, 7, 8)], J)
               + mhat ** 2 * outer_far(ED_, 6, list(range(6)), [(0, 1, 2), (3, 4, 5)], J))
    # ---- normalization ----
    gD = riglap2.Graph(6, dict(ED_), [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)], N=NN)
    rho_v = [math.sqrt(min(70.0 * gD.G[v, v] / J, 0.6)) for v in range(6)]
    akD, BDb = riglap2.bound(gD, [('p', (0, 1, 2), q[1], q[2], q[3]), ('p', (3, 4, 5), q[1], q[2], q[3])], 3, J, rho_v, 0.9)
    Z2low = sum(x * t ** k for k, x in enumerate(akD)) - sum(BDb.values())
    eps = (math.sqrt(near ** 2 + far_out) + gB) / (mhat * math.sqrt(Z2low))
    lines.append("J = %6.1f: eps_r <= %.3e | near %.3e [P %.2e D5 %.2e R0 %.2e tailX %.2e tailB %.2e ann %.2e] gB %.1e far_out %.1e Z2/main2 >= %.6f"
                 % (J, eps, near, nP, nD, nR0, tailX, tailB, ann, gB, far_out, Z2low))
    print(lines[-1], "(%.1f s)" % (time.time() - t0)); sys.stdout.flush()
open(outf, "w").write("\n".join(lines) + "\n")
