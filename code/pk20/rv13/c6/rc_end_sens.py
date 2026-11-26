#!/usr/bin/env python3
# the review (RV13_6): Prop. 19.6 coverage on the binding subinterval J in [170, 171.7] (and the last piece [2e4, inf)), with the author's
# quantities()/mode_data() (functions copied verbatim from endpairs4.py into endpairs4_funcs.py, inputs set here) and the reviewer's OWN
# re-implementation of the two pass tests (from the derivation in RV13_6 §3), then the distance to flipping the claimed ranges.
# Usage: rc_end_sens.py OUTFILE N
import sys, json, math
outf, NN = sys.argv[1], int(sys.argv[2])
C5 = "/mnt/g2/release/root/code/pk20/rv13/c5/scratch/"; CP = "/mnt/g2/release/root/code/pk20/rv13/copies/scratch/"
C6 = "/mnt/g2/release/root/code/pk20/rv13/c6/scratch/"
M2 = json.load(open(C5 + "m2_N%d_J170.json.b" % NN)); B5 = json.load(open(CP + "b5_N%d_J170.json" % NN)); CT = json.load(open(C5 + "clT_N%d_J170.json" % NN))
B4 = json.load(open(CP + "binding4_N%d_J170.json" % NN)); EW = json.load(open(C6 + "endw_N%d_J170.json" % NN))
mser = json.load(open(CP + "vacres_K3_N%d.json" % NN))
J1 = 170.0; kbar = M2["kbar"]
import mpmath as mp
P = {4: dict(TRB="1.312607", vac=(2.6744e-06, 1.6450e-04, 4.2950e-06, 7.4706e-06, 3.837e-10, 1.1950e-06, 7.250e-11, 1.8816e-05, 0.999993, 1.332042, 0.360),
             wt=(3.4712e-06, 5.287e-05, 7.487e-06, 170.0), dl=(2.4733e-06, 5.027e-05, 6.219e-06, 170.0), trt2=(1.0302393041, 0.846041, 0.639530, 0.498940, 6.509e-4), cov1=1.1765e-4),
     3: dict(TRB="0.942262", vac=(1.1426e-06, 5.2050e-05, 1.9050e-06, 2.5677e-06, 1.361e-10, 6.2950e-07, 5.250e-17, 1.4354e-05, 0.999998, 1.331271, 0.360),
             wt=(1.2665e-06, 1.631e-05, 3.322e-06, 170.0), dl=(9.8425e-07, 1.515e-05, 2.752e-06, 170.0), trt2=(1.0302393041, 0.742488, 0.53795, 0.43804, 1.592e-4), cov1=2.2043e-4)}[NN]
TRB = mp.mpf(P["TRB"]); cxi = 0.6594
nP, D5, R0, tX, tB, ann, far, gB, z2, Rtr, ae = P["vac"]
nPwM, D5w, R0w, J0w = P["wt"]; nPdM, D5d, R0d, J0d = P["dl"]
lead, c1, c2, c3, remT = P["trt2"]; COV1 = P["cov1"]
exec(open("/mnt/g2/release/root/code/pk20/rv13/c6/endpairs4_funcs.py").read())
# ---------------- reviewer's own pass tests ----------------
def my_jensen(Q, d, m, kind, sc):
    e = sc.get("R", 1) * Q["Rw"] * Q["rho1"] ** d
    r1, r = Q["rho1"], Q["rho"]; nBp, nBm = sc.get("B", 1) * Q["nBp"], sc.get("B", 1) * Q["nBm"]
    vp, vm = Q["vp"], Q["vm"]; pX = math.sqrt(vp * vp + vm * vm)
    Dm1 = r1 ** (m + 1) * e * e                                   # |D - 1| <= rho1^{m+1} e_L e_R
    if Dm1 >= 1:
        return False
    au = e * pX                                                   # |<a,u>|, |<u,b>| <= e |p_X|
    Sme = r1 ** m * e * (pX + nBp * e)                            # |<Q0 a, S^m eps_R>| <= rho1^m e |a|, |a| <= |p_X| + |B_X| e
    second = (au * au * Dm1 + 2 * au * Sme + Sme * Sme) / (1 - Dm1)
    if kind == "flip":
        Cm = sc.get("C", 1) * COV1 if m == 1 else Q["vSv_p"] * Q["Rp"] ** (m - 2) - Q["vSv_m"] * r ** (m - 2)
        etp = r1 ** ((m - 1) / 2) * nBp * e; etm = r ** ((m - 1) / 2) * nBm * e
        main = Cm - 2 * r1 ** ((m - 1) / 2) * vp * etp - etp ** 2 - 2 * r ** ((m - 1) / 2) * vm * etm - etm ** 2
    else:
        Pm = math.sqrt(Q["vSv_p"] / r1) if m == 1 else math.sqrt(Q["vSv_p"] * Q["Rp"] ** (m - 2))
        et = r1 ** ((m - 1) / 2) * nBp * e
        if Pm < et:
            return False
        main = Pm * Pm - 2 * Pm * et - et * et
    return main - second > 0
def my_mode(Q, Mq, d, k, kind, sc):
    e = sc.get("R", 1) * Q["Rw"] * Q["rho1"] ** d
    nBp, nBm = sc.get("B", 1) * Q["nBp"], sc.get("B", 1) * Q["nBm"]
    X = sc.get("cx", 1) * Mq["cx"] - nBp * e
    if X <= 0:
        return False
    vp, vm = Q["vp"], Q["vm"]; pX = math.sqrt(vp * vp + vm * vm); r1 = Q["rho1"]
    rest = Mq["r2"] ** k * (vp + nBp * e) ** 2
    odd = Mq["ro"] ** k * ((vm + nBm * e) ** 2 if kind == "flip" else 2 * vm * nBm * e + (nBm * e) ** 2)
    Dm1 = r1 ** (k + 2) * e * e
    second = (r1 ** 2 * e * e * (e * pX) ** 2 + 2 * r1 * e * pX * e * (pX + nBp * e) + r1 ** (k + 2) * (e * (pX + nBp * e)) ** 2) / (1 - Dm1)
    return X * X - rest - odd - second > 0
def cover(Q, Mq, d, kind, sc):
    m = 1
    while m <= 3000 and my_jensen(Q, d, m, kind, sc):
        m += 1
    mJ = m - 1
    k = 1
    while k <= 60 and not my_mode(Q, Mq, d, k, kind, sc):
        k += 1
    return mJ, k + 1, (mJ >= k) and k <= 60
lines = []
for (Jlo, Jhi, lab) in ((170.0, 170.0 * 1.01, "[170, 171.7]"), (2e4, None, "[2e4, inf)")):
    Q = quantities(Jlo, Jhi); Mq = mode_data(Jlo, Jhi, Q)
    lines.append("# N = %d, J in %s: R_w %.5f rho1 %.5f rho %.5f R+ %.5f |v+| %.5f |v-| %.5f nB+ %.4f nB- %.4f | q_x %.5f L2 %.5f mu_x %.5f alpha^2 %.4f |a_x| %.5f Dlt %.2e c_x %.5f r2 %.4f ro %.4f simple %s"
                 % (NN, lab, Q["Rw"], Q["rho1"], Q["rho"], Q["Rp"], Q["vp"], Q["vm"], Q["nBp"], Q["nBm"], Mq["qx"], Mq["L2"], Mq["mux"], Mq["al2"], Mq["ax"], Mq["Dlt"], Mq["cx"], Mq["r2"], Mq["ro"], Mq["simple"]))
    for kind, d in (("flip", 4 if NN == 4 else 3), ("flip", 8), ("same", 1), ("same", 2), ("flip", 3 if NN == 4 else 2)):
        mJ, mM, full = cover(Q, Mq, d, kind, {})
        # author's own pass functions for comparison
        ma = 1
        while ma <= 3000 and passes_jensen(Q, d, ma, kind):
            ma += 1
        ka = 1
        while ka <= 60 and not passes_mode(Q, Mq, d, ka, kind):
            ka += 1
        lines.append("  %s d=%d: own Jensen m<=%d, mode m>=%d, %s | author's tests: Jensen m<=%d, mode m>=%d" % (kind, d, mJ, mM, "FULL" if full else "not full", ma - 1, ka + 1))
    if Jhi is not None:
        Q0, Mq0 = Q, Mq
# distance to flipping the claimed ranges (binding subinterval)
claims = [("flip", 4 if NN == 4 else 3), ("same", 1)]
def full_all(sc):
    return all(cover(Q0, Mq0, d, kind, sc)[2] for kind, d in claims)
def flip_point(key, lo, hi, down=False, n=40):
    f = lambda x: full_all({key: (1 / x if down else x)})
    if f(hi):
        return None
    for _ in range(n):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) else (lo, mid)
    return (lo + hi) / 2
lines.append("# distance to losing the claimed coverage (%s) on [170, 171.7]:" % ", ".join("%s d>=%d" % c for c in claims))
for key, lab, down in (("R", "R_w x", False), ("B", "||B+||, ||B-|| x", False), ("cx", "c_x / ", True), ("C", "Cov_1 / ", True)):
    k = flip_point(key, 1.0, 1e3, down)
    lines.append("  %-20s %s" % (lab, "%.3f" % k if k else "> 1e3"))
# U raised: recompute Q, Mq with remT + delta
def full_U(delta):
    global remT
    old = remT; remT = old + delta
    Qd = quantities(170.0, 171.7); Mqd = mode_data(170.0, 171.7, Qd)
    remT = old
    return all(cover(Qd, Mqd, d, kind, {})[2] for kind, d in claims)
lo, hi = 0.0, 0.05
if not full_U(hi):
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if full_U(mid) else (lo, mid)
    lines.append("  %-20s %.3e (absolute, on tr T^2/lambda_h^2)" % ("U raised by", (lo + hi) / 2))
else:
    lines.append("  U raised by         > 0.05")
print("\n".join(lines))
open(outf, "w").write("\n".join(lines) + "\n")
