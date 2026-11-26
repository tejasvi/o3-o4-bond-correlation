#!/usr/bin/env python3
# pk10 (code): binding pair, uniform in J >= J1 (refines assemble_binding_unif.py):
#   log-spaced J subintervals (ratio RATIO) to control interval dependency in t, plus [0, t_min];
#   eps_r(J), s(J) by the monotone scaling of the J = 150 components (vacscale), with far_out(J) <= far_out(150) e^{-0.5 a_m (J - 150)}
#   (Chernoff lambda >= 0.5 at radius a_m = 0.3025) and tailB(J) <= tailB(150) e^{-J kappa/(4 vq_max) + 150 kappa/(4 vq_max)} dropped to its value (tiny).
# Usage: assemble_binding_unif2.py OUTFILE B5_JSON B4_JSON TRB C_XI VACPARAMS(nP,D5,R0,tailX,tailB,ann,far,gB,Z2min,Rtr,a_e) RATIO
import sys, json, math
import mpmath as mp
iv = mp.iv
iv.dps = 25
outf, b5f, b4f, TRB, cxi = sys.argv[1], sys.argv[2], sys.argv[3], mp.mpf(sys.argv[4]), mp.mpf(sys.argv[5])
nP, D5, R0, tX, tB, ann, far, gB, z2, Rtr, ae = (float(x) for x in sys.argv[6].split(","))
RATIO = float(sys.argv[7])
B5 = json.load(open(b5f)); B4 = json.load(open(b4f))
J1 = B5["J"]
mser = json.load(open("/mnt/g2/release/root/code/pk10/scratch/vacres_K3_N%d.json" % B5["N"]))


from scipy.special import erfc
VQ = [float(x) for x in sys.argv[8].split(",")] if len(sys.argv) > 8 else [0.66767, 0.56373]
KAPPA = 0.41729
chi3 = lambda s: math.exp(-s / 2) if B5["N"] == 3 else erfc(math.sqrt(s / 2)) + math.sqrt(2 * s / math.pi) * math.exp(-s / 2)


def vac(J):
    s_ = 150.0 / J
    dec = math.exp(-0.3 * ae * (J - 150) / 2)
    tBJ = tB * max(math.sqrt(chi3(J * KAPPA / v) / chi3(150 * KAPPA / v)) for v in VQ)   # bad-bond tail decays (vq_tailB.py)
    near = nP * s_ ** 2 + (D5 + R0) * s_ ** 5 + (tX + ann) * dec + tBJ
    fJ = far * (J / 150.0) ** 2 * math.exp(-0.5 * 0.3025 * (J - 150))      # supp^2 growth of the truly-far part included
    g = gB * (J / 150.0) * math.exp(-0.95 * (1 - math.cos(math.radians(40))) * (J - 150) / 2)
    eps = (math.sqrt(near ** 2 + fJ) + g) / math.sqrt(z2)
    # weighted residuals: |w| <= c_w J on Omega_out (near part), |w| <= W J globally (bad-bond and far parts); returned as functions of (c_w, W)
    wres = lambda cw, Wg: (math.sqrt((cw * J * near) ** 2 + (Wg * J) ** 2 * fJ) + Wg * J * g) / math.sqrt(z2)
    return eps, eps / (2 - Rtr - eps), wres


def item(name, src, tI):
    d = src[name]
    e = d["err"] if "err" in d else sum(d["B"].values())
    return sum(iv.mpf(a) * tI ** k for k, a in enumerate(d["ak"])) + iv.mpf([-e, e])


def cov_lower(Jlo, Jhi):
    tI = iv.mpf([0 if Jhi is None else mp.mpf(1) / Jhi, mp.mpf(1) / Jlo])
    mh = 1 + mser["m1"] * tI + mser["m2"] * tI ** 2 + mser["m3"] * tI ** 3
    it = B5["items"]
    g = lambda a, b: item("g,%d,%d" % (min(a, b), max(a, b)), it, tI)
    idx = [0, 1, 3]
    Ge = [[g(a, b) for b in idx] for a in idx]
    Ae = [item("A,%d" % a, it, tI) for a in idx]
    L = [[iv.mpf(0)] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i + 1):
            ssum = Ge[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            L[i][j] = iv.sqrt(ssum) if i == j else ssum / L[j][j]
    w = [iv.mpf(0)] * 3
    for i in range(3):
        w[i] = (Ae[i] - sum(L[i][k] * w[k] for k in range(i))) / L[i][i]
    g00 = Ge[0][0]
    ax = w[1] / (mh * iv.sqrt(g00)); ay = w[2] / (mh * iv.sqrt(g00))
    eps_r, s_vac, wres = vac(Jlo)
    eps_d = wres(float(cxi) / 2, 1.0); eps_a = wres(float(cxi), 2.0)   # delta = (xi_TM - xi_MB)/2: |delta| <= c_xi J/2 near, <= J globally; xi_a <= c_xi J near, <= 2J
    # J * (each scaled vacuum term) is nonincreasing for J >= 150, so the values at J_lo bound the subinterval
    odd = (2 * item("I_N", {"I_N": B4["I_N"]}, tI) / mh - item("Ndel", it, tI)) / g00 + iv.mpf(eps_d) ** 2
    even = ax ** 2 + ay ** 2
    Bu2 = (2 * item("Ia", it, tI) / mh - item("Na", it, tI)) / g00 + iv.mpf([0, eps_a ** 2])
    alpha = item("A,0", it, tI) / (mh * g00)
    QBu2 = Bu2 - alpha ** 2
    vtr = iv.sqrt(iv.mpf([0, QBu2.b]))
    Dm = iv.mpf(TRB) - alpha
    beta = iv.mpf(((alpha + Dm) / 2 + iv.sqrt(((Dm - alpha) / 2) ** 2 + vtr ** 2)).b)
    sp = iv.mpf(s_vac * math.sqrt(2 / (1 + math.sqrt(1 - s_vac ** 2))))
    erI = iv.mpf(eps_r)
    Bu = iv.sqrt(Bu2)
    Dlt = sp * (beta + alpha + 2 * Bu + beta * sp) / (1 - erI) + vtr * erI / (1 - erI)
    vacT = Dlt * (2 * vtr + Dlt)
    return (even - odd - vacT), even, odd, vacT, eps_r, s_vac, beta


lines = ["# assemble_binding_unif2: N = %d, J1 = %g, TRB %s, c_xi %s, ratio %g" % (B5["N"], J1, TRB, cxi, RATIO)]
Jlo = J1; worst = None; n = 0
while True:
    Jhi = Jlo * RATIO if Jlo < 2e4 else None
    c, ev, od, vt, er, sv, be = cov_lower(Jlo, Jhi)
    n += 1
    if worst is None or c.a < worst[0]:
        worst = (c.a, Jlo, Jhi, ev, od, vt, er, sv, be)
    if n % 40 == 1 or Jhi is None:
        lines.append("J in [%.1f, %s]: Cov J^2 >= %.4e (even >= %.6f, odd <= %.6f, vac <= %.2e, eps_r %.2e, s %.2e, beta <= %.4f)"
                     % (Jlo, "%.1f" % Jhi if Jhi else "inf", float(c.a), float(ev.a), float(od.b), float(vt.b), er, sv, float(be.b)))
        print(lines[-1]); sys.stdout.flush()
    if Jhi is None:
        break
    Jlo = Jhi
lines.append("%d subintervals; minimum lower bound Cov J^2 >= %.4e on J in [%.1f, %s]" % (n, float(worst[0]), worst[1], worst[2]))
print(lines[-1])
open(outf, "w").write("\n".join(lines) + "\n")
