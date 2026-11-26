#!/usr/bin/env python3
# pk10 (code): s19.2 uniformity in J >= J1 for the vacuum residual bound (vacrig11f): Minkowski forms of the polynomial norms
# (nP, normT -> tailX, tailB), signs of the exact normalization coefficients a_k of Z2 = <phi, K phi>/main2, and of the G4 - r coefficients.
# Usage: vacmono.py OUTFILE VACRES3N_JSON N RHO_M RHO_E DELTA_DEG J1
import sys, json, math, time
import numpy as np
from scipy.special import erfc
sys.path.insert(0, "/mnt/g2/release/root/code/pk10/scripts")
from vacmod2 import Builder, ltri, XS, QS, XD, QD, PAIRS, BASIS, A_EX, B_EX
from pseries import padd, pscale
from condexp2 import CondMom
from condpoly3 import SigmaPolys, CondSigma
from condg import sigma_to_g
from wishart import Wishart
from amom2b import AllMom2
import riglap2

outf, resf, NN = sys.argv[1], sys.argv[2], int(sys.argv[3])
rho_m, rho_e, delta = float(sys.argv[4]), float(sys.argv[5]), math.radians(float(sys.argv[6]))
J = float(sys.argv[7]); t = 1.0 / J
nn = NN - 1
R3 = json.load(open(resf))
q = [None, R3["q1"], R3["q2"], R3["q3"]]
a_m, a_e = rho_m ** 2, rho_e ** 2
c_m = -math.log(1 - a_m) / (2 * a_m)
a, b = A_EX, B_EX
t0 = time.time()
A = np.eye(3) + ltri(); Ainv = np.linalg.inv(A)
W2 = np.zeros((3, 6))
for r in range(3):
    W2[r, r] = 1.0
for p_, (r, s) in enumerate(PAIRS):
    W2[r, 3 + p_] = 1.0; W2[s, 3 + p_] = -1.0
bd = Builder(4)
L1 = bd.L1(q[1], q[2], q[3]); L0 = bd.L0(q[1], q[2], q[3])
mser = [1.0, R3["m1"], R3["m2"], R3["m3"]]
cm8 = CondMom(Ainv, Ainv, W2, nn, 8, groups=[0, 0, 0, 1, 1, 1], caps={1: 2})
sp8 = SigmaPolys(8); cs8 = CondSigma(cm8, sp8)
mL04 = {}
for e, c in padd(*[pscale(L0.c[4 - j], mser[j]) for j in range(4)]).items():
    mL04[e[:6]] = mL04.get(e[:6], 0.0) + c
r4 = sp8.to_dict(cs8.condE(L1.c[4]) - sp8.from_dict(mL04))
rk = {2: {tuple(int(x) for x in k.split(",")): v for k, v in R3["r2"].items()},
      3: {tuple(int(x) for x in k.split(",")): v for k, v in R3["r3"].items()}, 4: r4}
rkg = {k: sigma_to_g(v) for k, v in rk.items()}


def lap(edges, V):
    L = np.zeros((V, V))
    for (u, v), c in edges:
        L[u, u] += c; L[v, v] += c; L[u, v] -= c; L[v, u] -= c
    return L


def gauge_basis(V, S):
    u = np.zeros(V); u[list(S)] = 1.0
    return np.linalg.svd(np.eye(V) - np.outer(u, u) / u.dot(u))[0][:, :V - 1]


def tilted_cov(L, Bm, rates):
    Lr = Bm.T @ L @ Bm
    Lt = Bm.T @ (L - 2 * np.diag(rates)) @ Bm
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
    idx = [0, 1, 2, 6, 7, 8]
    return AllMom2(G9[np.ix_(idx, idx)], nn, Dmax, W=W12[:, IDX9F], groups=[0] * 6 + [1] * 3, caps={1: 4}), N9, G9


def to9(P):
    out = {}
    for e, c in P.items():
        assert e[3] == e[4] == e[5] == 0
        e9 = tuple(e[i] for i in IDX9F)
        out[e9] = out.get(e9, 0.0) + c
    return out


lines = ["# vacmono: N = %d, J1 = %g (rho_m %g, rho_e %g, delta %g deg)" % (NN, J, rho_m, rho_e, math.degrees(delta))]
# (1) nP: joint vs Minkowski
G1, n1 = tilted_cov(LD, BD, np.full(6, c_m * t))
Pv = {}
for k in (2, 3, 4):
    Pv = padd(Pv, pscale(rkg[k], t ** k))
w1 = Wishart(G1[:3, :3], nn, 2 * max(sum(e) for k in (2, 3, 4) for e in rkg[k]))
nP = math.sqrt(n1 * max(w1.E2(Pv, Pv), 0.0))
nPm = sum(t ** k * math.sqrt(n1 * max(w1.E2(rkg[k], rkg[k]), 0.0)) for k in (2, 3, 4))
lines.append("nP: joint %.4e, Minkowski %.4e" % (nP, nPm))
# (2) normT, tailX, tailB with Minkowski
Lk = [to9(L1.c[k]) for k in range(5)]
T4_9 = to9(padd(*[pscale(L1.c[k], t ** k) for k in range(5)]))
dT = max(sum(e) for e in T4_9)
am0, N0, G90 = joint_moments(np.array([c_m * t] * 6 + [0.0] * 3), 2 * dT)
normT = math.sqrt(N0 * max(am0.E2(T4_9, T4_9), 0.0))
normTm = sum(t ** k * math.sqrt(N0 * max(am0.E2(Lk[k], Lk[k]), 0.0)) for k in range(5))
lines.append("normT: joint %.6f, Minkowski %.6f; per-order norms %s" % (normT, normTm, " ".join("%.4g" % math.sqrt(N0 * max(am0.E2(Lk[k], Lk[k]), 0.0)) for k in range(5))))
tX = tXm = float("inf")
for lam in (0.3, 0.45, 0.6):
    acc = accm = 0.0
    for v in range(3):
        rates9 = np.array([c_m * t] * 6 + [0.0] * 3); rates9[6 + v] += lam
        am9, N9, _ = joint_moments(rates9, 2 * dT)
        acc += math.exp(-lam * J * a_e) * N9 * max(am9.E2(T4_9, T4_9), 0.0)
        accm += math.exp(-lam * J * a_e) * N9 * sum(t ** k * math.sqrt(max(am9.E2(Lk[k], Lk[k]), 0.0)) for k in range(5)) ** 2
    tX, tXm = min(tX, math.sqrt(acc)), min(tXm, math.sqrt(accm))
lines.append("tailX: joint %.4e, Minkowski %.4e" % (tX, tXm))
amax = max(a_m, a_e)
kappa = 2 * (1 - math.cos(delta)) - amax ** 2 / (4 * (1 - amax))
sbad = sum(math.sqrt(chi_tail(J * kappa / (G90[r, r] + G90[6 + r, 6 + r] - 2 * G90[r, 6 + r]))) for r in range(3))
lines.append("tailB: joint %.4e, Minkowski %.4e" % (normT * sbad, normTm * sbad))
# (3) exact coefficients of Z2 and of Z_{G4 - r}
gD = riglap2.Graph(6, dict(ED_), [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)], N=NN)
rho_v = [math.sqrt(min(70.0 * gD.G[v, v] / J, 0.6)) for v in range(6)]
akD, BDb = riglap2.bound(gD, [('p', (0, 1, 2), q[1], q[2], q[3]), ('p', (3, 4, 5), q[1], q[2], q[3])], 3, J, rho_v, 0.9)
lines.append("Z2/main2: a_k = %s; remainders %s; Z2low(J1) = %.6f; 1 - sum B = %.6f"
             % (" ".join("%.6f" % x for x in akD), " ".join("%s %.2e" % (k_, v_) for k_, v_ in BDb.items()),
                sum(x * t ** k for k, x in enumerate(akD)) - sum(BDb.values()), 1 - sum(BDb.values())))
E4 = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + [((9 + r, 9 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((r, 3 + r), 1.0) for r in range(3)] + [((3 + r, 6 + r), 1.0) for r in range(3)] + [((6 + r, 9 + r), 1.0) for r in range(3)] + \
     [((3, 4), 1.0), ((4, 5), 1.0), ((6, 7), 1.0), ((7, 8), 1.0)]
for r in range(3):
    edges_r = [(e_, c_) for (e_, c_) in E4 if e_ != (r, 3 + r)]
    gR = riglap2.Graph(12, dict(edges_r), [], N=NN)
    akR, BR = riglap2.bound(gR, [], 1, J, [math.sqrt(min(60.0 * gR.G[v, v] / J, 0.5)) for v in range(12)], 0.9)
    lines.append("G4 - (%d, %d): a_k = %s; sum B = %.3e" % (r, 3 + r, " ".join("%.6f" % x for x in akR), sum(BR.values())))
lines.append("m-hat series: %s" % " ".join("%.10f" % x for x in mser))
print("\n".join(lines))
open(outf, "w").write("\n".join(lines) + "\n")
