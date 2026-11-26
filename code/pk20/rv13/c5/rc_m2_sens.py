#!/usr/bin/env python3
# the review (RV13_5): own arb re-implementation of the Prop. 19.5b check R+_low >= rho_up on the binding subinterval J in [170, 171.7]
# (formulas of 19.5.3-19.5.4 re-derived by the reviewer), and the distance to flipping for every float input.
# Usage: rc_m2_sens.py OUTFILE N
import sys, json, math
import numpy as np
import scipy.linalg as sla
from flint import arb, ctx
ctx.prec = 120
outf, NN = sys.argv[1], int(sys.argv[2])
D = "/mnt/g2/release/root/code/pk20/rv13/c5/scratch/"
M2 = json.load(open(D + "m2_N%d_J170.json.b" % NN)); CT = json.load(open(D + "clT_N%d_J170.json" % NN))
B5 = json.load(open("/mnt/g2/release/root/code/pk20/rv13/copies/scratch/b5_N%d_J170.json" % NN))
VR = json.load(open("/mnt/g2/release/root/code/pk20/rv13/copies/scratch/vacres_K3_N%d.json" % NN))
kbar = arb(M2["kbar"])
P0 = {4: dict(nP=2.6744e-06, D5=1.6450e-04, R0=4.2950e-06, tX=7.4706e-06, tB=3.837e-10, ann=1.1950e-06, far=7.250e-11, gB=1.8816e-05, z2=0.999993, Rtr=1.332042, ae=0.360,
              nPw=3.4712e-06, D5w=5.287e-05, R0w=7.487e-06, TRB=1.312607, lead=1.0302393041, c1=0.846041, c2=0.639530, c3=0.498940, rem=6.509e-4),
      3: dict(nP=1.1426e-06, D5=5.2050e-05, R0=1.9050e-06, tX=2.5677e-06, tB=1.361e-10, ann=6.2950e-07, far=5.250e-17, gB=1.4354e-05, z2=0.999998, Rtr=1.331271, ae=0.360,
              nPw=1.2665e-06, D5w=1.631e-05, R0w=3.322e-06, TRB=0.942262, lead=1.0302393041, c1=0.742488, c2=0.53795, c3=0.43804, rem=1.592e-4)}[NN]
CXI = 4 * (1 - (1 - arb("0.55") ** 2).sqrt())
VQ = [arb("0.66767"), arb("0.56373")]; KAPPA = arb("0.41729")
def chi(s):
    return (-s / 2).exp() if NN == 3 else (s / 2).sqrt().erfc() + (2 * s / arb.pi()).sqrt() * (-s / 2).exp()
def ub(x):
    u = x.upper(); return arb(u)
def evaluate(kn):
    P = {k: arb(v) for k, v in P0.items()}
    for k in ("D5", "gB", "tX", "nP", "R0", "ann", "far", "D5w", "nPw", "R0w"):
        P[k] = P[k] * arb(kn.get(k, 1.0))
    J = arb(170); tI = (arb(1) / 170).union(arb(1) / (arb(170) * arb("1.01")))
    s_ = arb(150) / J
    dec = (-arb("0.3") * P["ae"] * (J - 150) / 2).exp()
    rat = max([(chi(J * KAPPA / v) / chi(150 * KAPPA / v)).sqrt() for v in VQ], key=lambda x: x.upper())
    tails = (P["tX"] + P["ann"]) * dec + P["tB"] * rat
    near = P["nP"] * s_ ** 2 + (P["D5"] + P["R0"]) * s_ ** 5 + tails
    fJ = P["far"] * (J / 150) ** 2 * (-arb("0.5") * arb("0.3025") * (J - 150)).exp()
    g = P["gB"] * (J / 150) * (-arb("0.95") * (1 - (arb.pi() * 40 / 180).cos()) * (J - 150) / 2).exp()
    er = ((near ** 2 + fJ).sqrt() + g) / P["z2"].sqrt()
    s = er / (2 - P["Rtr"] - er)
    wres = lambda cw, Wg: (((cw * J * near) ** 2 + (Wg * J) ** 2 * fJ).sqrt() + Wg * J * g) / P["z2"].sqrt()
    near_w = P["nPw"] + P["D5w"] + P["R0w"] + CXI * J * tails
    ew = (((near_w ** 2 + (2 * J) ** 2 * fJ).sqrt() + 2 * J * g) / P["z2"].sqrt()) * arb(kn.get("ew", 1.0))
    sp = s * (2 / (1 + (1 - s ** 2).sqrt())).sqrt()
    def item(d, name=None):
        e = sum(arb(x) for x in d["B"].values()) * arb(kn.get("B", 1.0)) * arb(kn.get("B:" + str(name), 1.0))
        c = sum(arb(a) * tI ** k for k, a in enumerate(d["ak"])) * (1 + arb(kn.get("rel:" + str(name), 0.0)))
        return c + arb(0, e.upper())
    mh = 1 + arb(VR["m1"]) * tI + arb(VR["m2"]) * tI ** 2 + arb(VR["m3"]) * tI ** 3
    it, b5 = M2["items"], B5["items"]
    g00 = item(it["g00"], "g00")
    alpha = item(b5["A,0"]) / (mh * item(b5["g,0,0"]))
    eps_a = wres(CXI, arb(2))
    Bu2 = (2 * item(b5["Ia"]) / mh - item(b5["Na"])) / item(b5["g,0,0"]) + arb((eps_a ** 2).upper() / 2, (eps_a ** 2).upper() / 2)
    vtr = arb((arb(0).union(Bu2 - alpha ** 2)).upper()).sqrt()
    TRB = P["TRB"] * arb(kn.get("TRB", 1.0))
    Dm = TRB - alpha
    beta = ub((alpha + Dm) / 2 + (((Dm - alpha) / 2) ** 2 + vtr ** 2).sqrt())
    Bop = beta if beta.upper() > (kbar * (1 + er)).upper() else ub(kbar * (1 + er))
    # Ritz data: central eigenvectors (any basis is legitimate), interval congruence, interval Cholesky, A' = L^-1 A L^-T
    tc = 1 / 170.0
    def cen(d):
        return sum(a * tc ** k for k, a in enumerate(d["ak"]))
    out = {}
    for idx, nm in (([0, 1, 3], "even"), ([2], "odd")):
        m = len(idx)
        gkey = lambda a, b: "g,%d,%d" % (min(a, b), max(a, b)); tkey = lambda a, b: "T,%d,%d" % (min(a, b), max(a, b))
        Gc = np.array([[cen(b5[gkey(a, b)]) for b in idx] for a in idx]); Tc = np.array([[cen(CT["items"][tkey(a, b)]) for b in idx] for a in idx])
        nu, Uv = sla.eigh(Tc, Gc)
        GI = [[item(b5[gkey(idx[a], idx[b])], "Ritz") for b in range(m)] for a in range(m)]
        TI = [[item(CT["items"][tkey(idx[a], idx[b])], "Ritz") for b in range(m)] for a in range(m)]
        Ui = [[arb(float(Uv[i, j])) for j in range(m)] for i in range(m)]
        cg = lambda X: [[sum((Ui[a][i] * X[a][b] * Ui[b][j] for a in range(m) for b in range(m)), arb(0)) for j in range(m)] for i in range(m)]
        Mm, Am = cg(GI), cg(TI)
        L = [[arb(0)] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1):
                s2 = Mm[i][j] - sum((L[i][k] * L[j][k] for k in range(j)), arb(0))
                L[i][j] = s2.sqrt() if i == j else s2 / L[j][j]
        Y = [[arb(0)] * m for _ in range(m)]
        for j in range(m):
            for i in range(m):
                Y[i][j] = (Am[i][j] - sum((L[i][k] * Y[k][j] for k in range(i)), arb(0))) / L[i][i]
        Ap = [[arb(0)] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                Ap[i][j] = (Y[i][j] - sum((L[j][k] * Ap[i][k] for k in range(j)), arb(0))) / L[j][j]
        diag = [max(float(Ap[i][i].lower()), 0.0) for i in range(m)]
        discs = [float(Ap[i][i].lower()) - (sum(float(abs(Ap[i][j]).upper()) for j in range(m) if j != i) if m > 1 else 0.0) for i in range(m)]
        out[nm] = (diag, discs)
    de, dse = out["even"]; do, dso = out["odd"]
    U = P["lead"] * (1 + arb(P0["c1"]) * tI + arb(P0["c2"]) * tI ** 2 + arb(P0["c3"]) * tI ** 3) + P["rem"] * arb(kn.get("rem", 1.0)) + arb(kn.get("U+", 0.0))
    mu0 = max(de); muy = max(min(dse), 0.0); muz = max(do[0], 0.0)
    L1e2 = U - mu0 ** 2 - muy ** 2 - muz ** 2
    S2e = sum(x ** 2 for x in de)
    L1e = arb(max(math.sqrt(max(float(L1e2.upper()), 0.0)), math.sqrt(max(float((U - S2e).upper()), 0.0))))
    lam0 = max(mu0, float((mh * (1 - er)).lower()))
    rho = math.sqrt(max(float((U - S2e).upper()), 0.0)) / lam0
    HT = item(it["I3p"], "I3p") / (g00 * mh)
    Nw = item(it["Nw"], "Nw")
    Dn2 = (2 * item(it["Ip3"], "Ip3") / mh - Nw) / g00 + ew ** 2
    Dn = arb((max(float(Dn2.lower()), 0.0) + float(Dn2.upper())) / 2, (float(Dn2.upper()) - max(float(Dn2.lower()), 0.0)) / 2).sqrt()
    uh = abs(item(it["kn"], "kn") - kbar * g00) / g00 + sp * (Nw / g00).sqrt()
    ua = abs(item(it["A0w"], "A0w")) / (mh * g00) + sp * Dn
    NT2 = HT - 2 * ew * ((L1e * HT / mh).sqrt() + (1 + er) * uh) - (1 + er) * ua ** 2
    num = arb(max(float(NT2.lower()), 0.0)).sqrt() - s * (L1e / mh).sqrt() * Bop
    Rp = arb(max(float(num.lower()), 0.0)) ** 2 / ((1 + er) * (Dn + s * Bop) ** 2)
    return float(Rp.lower()), rho, float(ew.upper()), float(er.upper()), float(L1e.upper())
Rp, rho, ew, er, L1 = evaluate({})
lines = ["# rc_m2_sens N = %d on J in [170, 171.7]: R+ >= %.5f, rho <= %.5f, ratio %.4f (eps_w %.3e, eps_r %.3e, L1 %.5f)" % (NN, Rp, rho, Rp / rho, ew, er, L1)]
def flip(f, lo, hi, n=50):
    if f(hi) > 1:
        return None
    for _ in range(n):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > 1 else (lo, mid)
    return (lo + hi) / 2
def ratio(kn):
    a, b, *_ = evaluate(kn)
    return a / b if b > 0 else float("inf")
for key, lo, hi, lab in (("ew", 1, 100, "eps_w x"), ("D5", 1, 1e3, "D5 (eps_r, s) x"), ("gB", 1, 1e3, "gB (eps_r and eps_w bad-bond part) x"),
                         ("B", 1, 100, "all Lemma 19.1c error bars (M2, B5, CT) x"), ("B:Ritz", 1, 100, "Ritz error bars (B5 Gram + CT T) x"),
                         ("B:I3p", 1, 1e3, "I3p error bar x"), ("B:Ip3", 1, 1e3, "Ip3 error bar x"), ("B:Nw", 1, 1e3, "Nw error bar x"),
                         ("rem", 1, 1e3, "Lemma 19.4 remainder rem x"), ("TRB", 1, 100, "TRB x")):
    k = flip(lambda x: ratio({key: x}), lo, hi)
    lines.append("%-45s flips at %s" % (lab, "%.4g" % k if k else "> %g" % hi))
for key, lab in (("U+", "U raised by (absolute)"), ("rel:I3p", "I3p central lowered by (relative)"), ("rel:Ip3", "Ip3 central raised by (relative)"), ("rel:Nw", "Nw central lowered by (relative)")):
    sgn = -1 if ("lowered" in lab) else 1
    k = flip(lambda x: ratio({key: sgn * x}), 0.0, 0.9)
    lines.append("%-45s flips at %s" % (lab, "%.4g" % k if k else "> 0.9"))
print("\n".join(lines))
open(outf, "w").write("\n".join(lines) + "\n")
