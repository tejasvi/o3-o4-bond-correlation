#!/usr/bin/env python3
# pk10 (code): bulk flip-related vertical pairs (T-M in column j, M-B in column j + m) at every separation m >= 2, uniform in J >= J1.
#   Cov_m J^2 = <v+, S^{m-1} v+> - <v-, S^{m-1} v->,  S = T/lam0,  v+- = Q0 T_{xi+-} Omega0/lam0,  xi+- = (xi_TM +- xi_MB)/2.
#   Jensen (spectral measure of v+ on the even part of Omega0-perp) and ||S|_odd|| = rho_odd give
#   Cov_m J^2 >= |v+|^2 R+^{m-1} - |v-|^2 rho_odd^{m-1} >= Cov_1 J^2 rho^{m-1} > 0  whenever R+ >= rho >= rho_odd  (Cov_1 > 0: Prop. 19.3).
# This script checks R+_low(J) >= rho_up(J) on log-spaced J subintervals (interval t), with (mu-hat units; lam_h = 1):
#   R+ >= [sqrt(NT2) - s sqrt(L1e/mh) Bop]_+^2 / ((1 + eps_r) [Dn + s Bop]^2),
#   NT2 = H_T - 2 eps_w [sqrt(L1e H_T/mh) + (1 + eps_r) uh] - (1 + eps_r) ua^2,   H_T = I3p/(g00 mh),   Dn^2 = (2 Ip3/mh - Nw)/g00 + eps_w^2,
#   uh = |kn - kbar g00|/g00 + sp sqrt(Nw/g00),   ua = |A0w|/(mh g00) + sp Dn,   Bop = max(beta, kbar (1 + eps_r))  (-kbar T <= T_w <= T_xi+),
#   L1e^2 <= U - mu0^2 - mu_y^2 - mu_z^2 (top even excited, Hilbert-Schmidt with Ritz lower bounds),
#   rho^2 <= (U - S2_even)/lam0_low^2 (top odd, Hilbert-Schmidt with the even Ritz block), U >= tr T^2/lam_h^2 (Lemma 19.4).
# Usage: m2_unif.py OUTFILE M2JSON B5_JSON CLT_JSON TRB C_XI VACPARAMS WPARAMS(nPwM,D5w,R0w,J0w) TRT2(lead,c1,c2,c3,rem) RATIO
import sys, json, math
import numpy as np
import scipy.linalg as sla
import mpmath as mp
from scipy.special import erfc
iv = mp.iv
iv.dps = 25
outf, m2f, b5f, ctf = sys.argv[1:5]
TRB, cxi = mp.mpf(sys.argv[5]), float(sys.argv[6])
nP, D5, R0, tX, tB, ann, far, gB, z2, Rtr, ae = (float(x) for x in sys.argv[7].split(","))
nPwM, D5w, R0w, J0w = (float(x) for x in sys.argv[8].split(","))
lead, c1, c2, c3, remT = (float(x) for x in sys.argv[9].split(","))
RATIO = float(sys.argv[10])
M2 = json.load(open(m2f)); B5 = json.load(open(b5f)); CT = json.load(open(ctf))
NN = B5["N"]; J1 = B5["J"]
assert M2["N"] == NN and CT["N"] == NN if "N" in CT else True
kbar = M2["kbar"]
mser = json.load(open("/mnt/g2/release/root/code/pk10/scratch/vacres_K3_N%d.json" % NN))
VQ = [0.66767, 0.56373]
KAPPA = 0.41729
chi3 = lambda s: math.exp(-s / 2) if NN == 3 else erfc(math.sqrt(s / 2)) + math.sqrt(2 * s / math.pi) * math.exp(-s / 2)


def vac(J):
    s_ = 150.0 / J
    dec = math.exp(-0.3 * ae * (J - 150) / 2)
    tBJ = tB * max(math.sqrt(chi3(J * KAPPA / v) / chi3(150 * KAPPA / v)) for v in VQ)
    tails = (tX + ann) * dec + tBJ
    near = nP * s_ ** 2 + (D5 + R0) * s_ ** 5 + tails
    fJ = far * (J / 150.0) ** 2 * math.exp(-0.5 * 0.3025 * (J - 150))
    g = gB * (J / 150.0) * math.exp(-0.95 * (1 - math.cos(math.radians(40))) * (J - 150) / 2)
    eps = (math.sqrt(near ** 2 + fJ) + g) / math.sqrt(z2)
    wres = lambda cw, Wg: (math.sqrt((cw * J * near) ** 2 + (Wg * J) ** 2 * fJ) + Wg * J * g) / math.sqrt(z2)
    sw = J0w / J
    assert sw <= 1.0 + 1e-12
    near_w = nPwM * sw ** 2 + (D5w + R0w) * sw ** 5 + cxi * J * tails          # w~ = xi+ - kbar: |w~| <= c_xi J on Omega_out
    eps_w = (math.sqrt(near_w ** 2 + (2 * J) ** 2 * fJ) + 2 * J * g) / math.sqrt(z2)  # |w~| <= 2J globally
    return eps, eps / (2 - Rtr - eps), wres, eps_w


def item(d, tI):
    e = d["err"] if "err" in d else sum(d["B"].values())
    return sum(iv.mpf(a) * tI ** k for k, a in enumerate(d["ak"])) + iv.mpf([-e, e])


def central(d, t):
    return sum(a * t ** k for k, a in enumerate(d["ak"]))


def ritz(tI, tc):
    out = {}
    for idx, nm in (([0, 1, 3], "even"), ([2], "odd")):
        m = len(idx)
        Gc = np.array([[central(B5["items"]["g,%d,%d" % (min(a, b), max(a, b))], tc) for b in idx] for a in idx])
        Tc = np.array([[central(CT["items"]["T,%d,%d" % (min(a, b), max(a, b))], tc) for b in idx] for a in idx])
        nu, Uv = sla.eigh(Tc, Gc)
        GI = [[item(B5["items"]["g,%d,%d" % (min(idx[a], idx[b]), max(idx[a], idx[b]))], tI) for b in range(m)] for a in range(m)]
        TI = [[item(CT["items"]["T,%d,%d" % (min(idx[a], idx[b]), max(idx[a], idx[b]))], tI) for b in range(m)] for a in range(m)]
        Ui = [[iv.mpf(float(Uv[i, j])) for j in range(m)] for i in range(m)]
        cg = lambda X: [[sum(Ui[a][i] * X[a][b] * Ui[b][j] for a in range(m) for b in range(m)) for j in range(m)] for i in range(m)]
        Mm, Am = cg(GI), cg(TI)
        L = [[iv.mpf(0)] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1):
                s = Mm[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
                L[i][j] = iv.sqrt(s) if i == j else s / L[j][j]
        Y = [[iv.mpf(0)] * m for _ in range(m)]
        for j in range(m):
            for i in range(m):
                Y[i][j] = (Am[i][j] - sum(L[i][k] * Y[k][j] for k in range(i))) / L[i][i]
        Ap = [[iv.mpf(0)] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                Ap[i][j] = (Y[i][j] - sum(L[j][k] * Ap[i][k] for k in range(j))) / L[j][j]
        diag = [max(float(Ap[i][i].a), 0.0) for i in range(m)]
        discs = [float(Ap[i][i].a) - (sum(float(abs(Ap[i][j]).b) for j in range(m) if j != i) if m > 1 else 0.0) for i in range(m)]
        out[nm] = (diag, discs)
    return out


def check(Jlo, Jhi):
    tI = iv.mpf([0 if Jhi is None else mp.mpf(1) / Jhi, mp.mpf(1) / Jlo]); tc = 1.0 / Jlo
    mh = 1 + mser["m1"] * tI + mser["m2"] * tI ** 2 + mser["m3"] * tI ** 3
    eps_r, s_vac, wres, eps_w = vac(Jlo)            # each scaled vacuum quantity is nonincreasing in J: values at J_lo bound the subinterval
    er = iv.mpf(eps_r); ew = iv.mpf(eps_w)
    sp = iv.mpf(s_vac * math.sqrt(2 / (1 + math.sqrt(1 - s_vac ** 2)))); sI = iv.mpf(s_vac)
    it, b5 = M2["items"], B5["items"]
    g00 = item(it["g00"], tI)
    # beta = ||T_xi_a||/mu-hat (2x2 block bound, as in Prop. 19.3); ||T_xi+|| <= beta
    alpha = item(b5["A,0"], tI) / (mh * item(b5["g,0,0"], tI))
    eps_a = wres(cxi, 2.0)
    Bu2 = (2 * item(b5["Ia"], tI) / mh - item(b5["Na"], tI)) / item(b5["g,0,0"], tI) + iv.mpf([0, eps_a ** 2])
    vtr = iv.sqrt(iv.mpf([0, (Bu2 - alpha ** 2).b]))
    Dm = iv.mpf(TRB) - alpha
    beta = iv.mpf(((alpha + Dm) / 2 + iv.sqrt(((Dm - alpha) / 2) ** 2 + vtr ** 2)).b)
    Bop = iv.mpf(max(float(beta.b), float((kbar * (1 + er)).b)))
    # Ritz data and Hilbert-Schmidt bounds
    rz = ritz(tI, tc)
    U = lead * (1 + c1 * tI + c2 * tI ** 2 + c3 * tI ** 3) + remT
    de, dse = rz["even"]; do, dso = rz["odd"]
    mu0 = max(de); muy = max(min(dse), 0.0); muz = max(do[0], 0.0)
    L1e2 = U - mu0 ** 2 - muy ** 2 - muz ** 2
    S2e_ = sum(x ** 2 for x in de)
    L1e = iv.mpf(max(math.sqrt(float(L1e2.b)), math.sqrt(max(float((U - S2e_).b), 0.0))))   # top of T on u-perp, both parities
    S2e = sum(x ** 2 for x in de)
    lam0 = iv.mpf(max(mu0, float((mh * (1 - er)).a)))
    rho = iv.mpf(math.sqrt(max(float((U - S2e).b), 0.0)) / float(lam0.a))
    # R+ lower bound
    HT = item(it["I3p"], tI) / (g00 * mh)
    Nw = item(it["Nw"], tI)
    Dn2 = (2 * item(it["Ip3"], tI) / mh - Nw) / g00 + ew ** 2
    Dn = iv.sqrt(iv.mpf([max(float(Dn2.a), 0.0), float(Dn2.b)]))
    uh = abs(item(it["kn"], tI) - kbar * g00) / g00 + sp * iv.sqrt(Nw / g00)
    ua = abs(item(it["A0w"], tI)) / (mh * g00) + sp * Dn
    NT2 = HT - 2 * ew * (iv.sqrt(L1e * HT / mh) + (1 + er) * uh) - (1 + er) * ua ** 2
    num = iv.sqrt(iv.mpf(max(float(NT2.a), 0.0))) - sI * iv.sqrt(L1e / mh) * Bop
    Rp = iv.mpf(max(float(num.a), 0.0)) ** 2 / ((1 + er) * (Dn + sI * Bop) ** 2)
    return float(Rp.a), float(rho.b), eps_r, eps_w, float(L1e.b), float(beta.b), float((HT - NT2).b) / float(HT.a)


lines = ["# m2_unif: N = %d, J >= %g; R+_low vs rho_up (flip-related vertical pairs, separations m >= 2); kbar %.9f, TRB %s, ratio %g" % (NN, J1, kbar, TRB, RATIO)]
Jlo = J1; worst = None; n = 0
while True:
    Jhi = Jlo * RATIO if Jlo < 2e4 else None
    Rp, rho, er, ew, L1e, be, crossrel = check(Jlo, Jhi)
    n += 1
    if worst is None or Rp / rho < worst[0]:
        worst = (Rp / rho, Jlo, Jhi, Rp, rho)
    if n % 40 == 1 or Jhi is None:
        lines.append("J in [%.1f, %s]: R+ >= %.5f, rho_odd <= %.5f (ratio %.4f) | eps_r %.2e eps_w %.3e L1e %.5f beta %.4f cross/H_T %.4f"
                     % (Jlo, "%.1f" % Jhi if Jhi else "inf", Rp, rho, Rp / rho, er, ew, L1e, be, crossrel))
        print(lines[-1]); sys.stdout.flush()
    if Jhi is None:
        break
    Jlo = Jhi
lines.append("%d subintervals; minimum R+_low/rho_up = %.4f on J in [%.1f, %s] (R+ >= %.5f, rho <= %.5f)%s"
             % (n, worst[0], worst[1], "%.1f" % worst[2] if worst[2] else "inf", worst[3], worst[4], "  => Cov_m > 0 for all m >= 2" if worst[0] > 1 else "  NOT CLOSED"))
print(lines[-1])
open(outf, "w").write("\n".join(lines) + "\n")
