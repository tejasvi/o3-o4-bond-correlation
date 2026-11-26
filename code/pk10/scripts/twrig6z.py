#!/usr/bin/env python3
# pk10 (code): rigorous upper bound for tr_H(T^2)/lambda_h^2, THIRD order exact, quartic remainder (two-column twisted trace).
# On Omega (t' <= t), with E1 = H1, E2 = H2 + H1^2/2, E3 = H3 + H1 H2 + H1^3/6, D3 := H - tH1 - t^2H2 (|D3| <= t^3 hbar3/6), E2' := H - tH1 (|E2'| <= t^2 hbar2/2),
#   R4H := H - sum_{k<=3} t^k H_k (|R4H| <= t^4 hbar4/24):
#   e^H - sum_{k<=3} t^k E_k = R4H + (1/2)(t^4 H2^2 + D3^2 + 2t H1 D3 + 2 t^2 H2 D3) + (1/6)(3t^2 H1^2 E2' + 3t H1 E2'^2 + E2'^3) + rho4(H),
#   |rho4(x)| <= x^4 e^{x_+}/24, |H| <= t|H1| + (t^2/2) hbar2, H_+ <= y^T T_eps y.
#   E|R_E| <= t^4 E hbar4/24 + (1/2)[t^4 E H2^2 + t^6 E hbar3^2/36 + (t^4/3)(E H1^2 E hbar3^2)^{1/2} + (t^5/3)(E H2^2 E hbar3^2)^{1/2}]
#            + (1/6)[(3/2) t^4 (E H1^4 E hbar2^2)^{1/2} + (3/4) t^5 (E H1^2 E hbar2^4)^{1/2} + (t^6/8) E hbar2^3]
#            + N_eps (t ||H1||_{4,eps} + (t^2/2)||hbar2||_{4,eps})^4/24.
# Tail, graded annulus, far and equator as twrig5 (tail norms by Minkowski/hypercontractivity).  Usage: twrig6.py OUTFILE N A1 A2 AP1 AP2 M NSH J1,...
import sys, math
import numpy as np
sys.path.insert(0, "/mnt/g2/release/root/code/pk10/scripts")
import twlib as tl
import twlib2 as t2
from gfmom import GFMom

outf, NN = sys.argv[1], int(sys.argv[2])
A1, A2, AP1, AP2, M, NSH = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
AZ = float(sys.argv[10]) if len(sys.argv) > 10 else A2
APZ = float(sys.argv[11]) if len(sys.argv) > 11 else AP2
Js = [float(x) for x in sys.argv[9].split(",")]
n = NN - 1
av = [A1, A1, A2, A2, A2, AZ]; avp = [AP1, AP1, AP2, AP2, AP2, APZ]
SHELLS = [[av[v] + (avp[v] - av[v]) * (i + 1) / NSH for v in range(6)] for i in range(NSH)]
PR = tl.pref(NN)
EPS = [0.2, 0.35, 0.5, 0.65]
Hs = t2.H_series(3)
H1, H2, H3 = Hs[1], Hs[2], Hs[3]
pm, pa, ps = t2.pmul, t2.padd, t2.pscale
H1sq = pm(H1, H1)
E2 = pa(H2, ps(H1sq, 0.5)); E3 = pa(H3, pm(H1, H2), ps(pm(H1sq, H1), 1.0 / 6))
H1q = pm(H1sq, H1sq)
POS = list(range(6))
restrict = lambda P: {tuple(e[i] for i in POS): c for e, c in P.items()}
deg = lambda P: max(sum(e) for e in P)


def chern(B, C, R, ngrid=29):
    L = np.linalg.cholesky(C)
    ev = np.linalg.eigvalsh(L.T @ B @ L)
    best = 1.0
    for fr in np.linspace(0.02, 0.98, ngrid):
        lam = fr / (2 * ev.max())
        best = min(best, math.exp(-lam * R - 0.5 * np.sum(np.log1p(-2 * lam * ev))))
    return best


nd = tl.nodes(NN, M)
pre = []
for k, w in nd:
    Q, Bs, Qnt = t2.mats(k)
    C = np.linalg.inv(Q)
    g8 = GFMom(Bs, C, 8)
    pre.append(dict(k=k, w=w, Q=Q, C=C, Bs=Bs, dq=np.linalg.det(Q) ** -0.5,
                    EE=[g8.E(H1), g8.E(E2), g8.E(E3)], EH1sq=g8.E(H1sq), EH2sq=g8.E(pm(H2, H2)), EH1q=g8.E(H1q), EH3sq=g8.E(pm(H3, H3)), EE2sq=g8.E(pm(E2, E2))))
lead = PR ** 2 * sum(p["w"] * p["dq"] for p in pre)
cc = [PR ** 2 * sum(p["w"] * p["dq"] * p["EE"][i] for p in pre) / lead for i in range(3)]
lines = ["# twrig6: tr_H(T^2)/lambda_h^2, N = %d, Omega radii^2 (%g, %g), annulus (%g, %g) in %d shells, %d-point rule; lead %.10f; <E1> %.6f <E2> %.5f <E3> %.5f"
         % (NN, A1, A2, AP1, AP2, NSH, M, lead, cc[0], cc[1], cc[2])]
print(lines[0]); sys.stdout.flush()
Qnt0 = t2.mats(nd[0][0])[2]; Bs0 = t2.mats(nd[0][0])[1]
for J in Js:
    t = 1.0 / J
    h2b, h3b, h4b = (t2.hbar2(j, av, t) for j in (2, 3, 4))
    h2r, h3r, h4r = restrict(h2b), restrict(h3b), restrict(h4b)
    h2sq = pm(h2r, h2r)
    sm = sR = srho = stail = sann = 0.0
    for p in pre:
        dmax6 = max(4 * deg(h2r), 2 * deg(h3r), deg(h4r))
        g6 = GFMom([p["Bs"][i] for i in POS], p["C"], dmax6)
        Eh4 = g6.E(h4r); Eh3sq = g6.E(pm(h3r, h3r)); Eh2sq = g6.E(h2sq); Eh2q = g6.E(pm(h2sq, h2sq)); Eh2cu = g6.E(pm(h2sq, h2r))
        RE = (t ** 4 / 24 * Eh4
              + 0.5 * (t ** 4 * p["EH2sq"] + t ** 6 / 36 * Eh3sq + t ** 4 / 3 * math.sqrt(p["EH1sq"] * Eh3sq) + t ** 5 / 3 * math.sqrt(p["EH2sq"] * Eh3sq))
              + (1.0 / 6) * (1.5 * t ** 4 * math.sqrt(p["EH1q"] * Eh2sq) + 0.75 * t ** 5 * math.sqrt(p["EH1sq"] * Eh2q) + t ** 6 / 8 * Eh2cu))
        best = float("inf")
        for eps in EPS:
            Qt = p["Q"] - 2 * t2.tilt2(p["k"], t, av, eps)
            if np.linalg.eigvalsh(Qt).min() <= 0:
                continue
            Ct = np.linalg.inv(Qt); Nt = math.sqrt(np.linalg.det(p["Q"]) / np.linalg.det(Qt))
            gt = GFMom(p["Bs"], Ct, 8)
            gt6 = GFMom([p["Bs"][i] for i in POS], Ct, 4 * deg(h2r))
            nC = t * gt.E(H1q) ** 0.25 + t * t / 2 * gt6.E(pm(h2sq, h2sq)) ** 0.25
            best = min(best, Nt * nC ** 4 / 24)
        Pout = min(1.0, sum(chern(p["Bs"][v], p["C"], J * av[v]) for v in range(6)))
        hc = lambda q, d: (q - 1) ** (d / 2)              # hypercontractivity ||P||_q <= (q-1)^{d/2} ||P||_2, d = Gaussian degree
        nE3 = math.sqrt(p["EH3sq"]) + (p["EH1q"] ** 0.25) * hc(4, 6) * math.sqrt(p["EH2sq"]) + hc(6, 4) ** 3 * p["EH1sq"] ** 1.5 / 6
        l2 = t * math.sqrt(p["EH1sq"]) + t * t * math.sqrt(p["EE2sq"]) + t ** 3 * nE3
        ann = 0.0; prev = av
        for sh in SHELLS:
            bs = float("inf")
            for eps in EPS:
                Qp = p["Q"] - 2 * t2.tilt2(p["k"], t, sh, eps)
                if np.linalg.eigvalsh(Qp).min() <= 0:
                    continue
                Cp = np.linalg.inv(Qp); Np_ = math.sqrt(np.linalg.det(p["Q"]) / np.linalg.det(Qp))
                bs = min(bs, Np_ * min(1.0, sum(chern(p["Bs"][v], Cp, J * prev[v]) for v in range(6))))
            ann += bs; prev = sh
        wq = p["w"] * p["dq"]
        sm += wq * (1 + sum(t ** (i + 1) * p["EE"][i] for i in range(3))); sR += wq * RE; srho += wq * best
        stail += wq * l2 * math.sqrt(Pout); sann += wq * ann
    Qf = Qnt0 - 2 * tl.cfun(0.96) * t * np.eye(Qnt0.shape[0]); Cf = np.linalg.inv(Qf)
    far = PR ** 2 * 64 * np.linalg.det(Qf) ** -0.5 * sum(chern(Bs0[v], Cf, J * avp[v]) for v in range(6))
    equ = PR ** 2 * 12 * math.sqrt(2 * J / math.pi) * math.exp(-J * (1 - math.cos(0.685)))
    up = PR ** 2 * (sm + sR + srho + stail + sann) + far + equ
    lines.append("J = %6.1f: tr(T^2)/lam_h^2 <= %.7f  [third-order %.7f; R_E %.2e; rho4 %.2e; tail %.2e; annulus %.2e; far %.2e; equator %.1e]"
                 % (J, up, PR ** 2 * sm, PR ** 2 * sR, PR ** 2 * srho, PR ** 2 * stail, PR ** 2 * sann, far, equ))
    print(lines[-1]); sys.stdout.flush()
open(outf, "w").write("\n".join(lines) + "\n")
