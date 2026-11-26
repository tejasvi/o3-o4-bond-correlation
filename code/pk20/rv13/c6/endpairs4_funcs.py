# pk10 (code): vertical pairs near the ends of a 3 x n strip (free boundary), by perturbation from the bulk (s19.5), uniform in J >= J1.
#   Left state at column j: T^{j-2} w (w = K^{1/2} V 1) = <u,w> lam0^{j-2} (u + eps_L), ||eps_L|| <= e_L = R_w rho1^{j-2}; right state likewise with
#   exponent n - j' - 1.  Insertions X at column j, Y at column j' = j + m (m >= 1), centred B_X = (T_xi - c T)/lam0, p_X = B_X u (= v of s19.5).
#   Cov_fin J^2 D = <Q0 a, S^{m-1} Q0 b> + <a,u><u,b>(1 - 1/D) - [<a,u><eps_L, S^m Q0 b> + <Q0 a, S^m eps_R><u,b> + <Q0 a,S^m eps_R><eps_L,S^m Q0 b>]/D,
#   a = B_X (u + eps_L), b = B_Y (u + eps_R), D = 1 + <eps_L, S^{m+1} eps_R>.
#   Flip pairs: main >= C_m - ||v+||_m (eta+_L + eta+_R) - eta+_L eta+_R - ||v-||_m (eta-_L + eta-_R) - eta-_L eta-_R,
#     ||v+||_m <= rho1^{(m-1)/2} ||v+||, ||v-||_m <= rho^{(m-1)/2} ||v-||, eta+ = rho1^{(m-1)/2} ||B+|| e, eta- = rho^{(m-1)/2} ||B-|| e,
#     C_1 >= Cov_1 (Prop. 19.3), C_m >= <v+,S v+> R+^{m-2} - <v-,S v-> rho^{m-2} (m >= 2, Jensen).
#   Same-type pairs: main >= P (P - eta_L - eta_R) - eta_L eta_R, P = ||p_X||_m >= ||v+||_m.
# Prints m0(d): the largest m such that every separation 1..m passes for all J >= J1 when both end exponents are >= d.
# Usage: endpairs.py OUTFILE M2JSON B5_JSON CLT_JSON B4_JSON ENDW_JSON TRB C_XI VACPARAMS WPAR_WT WPAR_DL TRT2 COV1LOW RATIO
import sys, json, math
import numpy as np
import scipy.linalg as sla
import mpmath as mp
from scipy.special import erfc
iv = mp.iv
iv.dps = 25
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
    def ew(nPM, D5x, R0x, J0, cw, Wg):
        sw = J0 / J
        assert sw <= 1.0 + 1e-12
        nw = nPM * sw ** 2 + (D5x + R0x) * sw ** 5 + cw * J * tails
        return (math.sqrt(nw ** 2 + (Wg * J) ** 2 * fJ) + Wg * J * g) / math.sqrt(z2)
    return eps, eps / (2 - Rtr - eps), wres, ew(nPwM, D5w, R0w, J0w, cxi, 2.0), ew(nPdM, D5d, R0d, J0d, cxi / 2, 1.0)


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
        out["Ap_" + nm] = Ap
    return out




def quantities(Jlo, Jhi):
    tI = iv.mpf([0 if Jhi is None else mp.mpf(1) / Jhi, mp.mpf(1) / Jlo]); tc = 1.0 / Jlo
    mh = 1 + mser["m1"] * tI + mser["m2"] * tI ** 2 + mser["m3"] * tI ** 3
    eps_r, s_vac, wres, eps_w, eps_d = vac(Jlo)
    er = float(eps_r); s = s_vac; c = math.sqrt(1 - s * s)
    sp = s * math.sqrt(2 / (1 + c))
    it, b5 = M2["items"], B5["items"]
    up = lambda x: float(x.b)
    lo = lambda x: float(x.a)
    g00 = item(it["g00"], tI)
    alpha = item(b5["A,0"], tI) / (mh * item(b5["g,0,0"], tI))
    eps_a = wres(cxi, 2.0)
    Bu2 = (2 * item(b5["Ia"], tI) / mh - item(b5["Na"], tI)) / item(b5["g,0,0"], tI) + iv.mpf([0, eps_a ** 2])
    vtr = iv.sqrt(iv.mpf([0, (Bu2 - alpha ** 2).b]))
    Dm = iv.mpf(TRB) - alpha
    beta = up((alpha + Dm) / 2 + iv.sqrt(((Dm - alpha) / 2) ** 2 + vtr ** 2))
    Bop = max(beta, kbar * (1 + er))
    rz = ritz(tI, tc)
    U = lead * (1 + c1 * tI + c2 * tI ** 2 + c3 * tI ** 3) + remT
    de, dse = rz["even"]; do, dso = rz["odd"]
    mu0 = max(de); muy = max(min(dse), 0.0); muz = max(do[0], 0.0)
    S2e = sum(x ** 2 for x in de)
    L1o = math.sqrt(max(up(U - S2e), 0.0))
    L1 = max(math.sqrt(up(U - mu0 ** 2 - muy ** 2 - muz ** 2)), L1o)
    mhl, mhu = lo(mh), up(mh)
    lam0 = max(mu0, mhl * (1 - er))
    rho1 = L1 / lam0; rho = L1o / lam0
    # even part: <v+, S v+> lower, ||v+|| upper, R+ lower (s19.5.4)
    HT = item(it["I3p"], tI) / (g00 * mh)
    Nw = item(it["Nw"], tI)
    Dn2 = (2 * item(it["Ip3"], tI) / mh - Nw) / g00 + iv.mpf(eps_w) ** 2
    Dn = iv.sqrt(iv.mpf([max(lo(Dn2), 0.0), up(Dn2)]))
    uh = abs(item(it["kn"], tI) - kbar * g00) / g00 + sp * iv.sqrt(Nw / g00)
    ua = abs(item(it["A0w"], tI)) / (mh * g00) + sp * Dn
    NT2 = lo(HT - 2 * eps_w * (iv.sqrt(L1 * HT / mh) + (1 + er) * uh) - (1 + er) * ua ** 2)
    num = max(math.sqrt(max(NT2, 0.0)) - s * math.sqrt(L1 / mhl) * Bop, 0.0)
    Rp = num ** 2 / ((1 + er) * (up(Dn) + s * Bop) ** 2)
    vSv_p = num ** 2 / (1 + er) ** 3
    vp_up = (up(Dn) + s * Bop) / (c * (1 - er))
    # odd part: <v-, S v-> upper, ||v-|| upper
    Hd = up(item(it["I3m"], tI) / (g00 * mh))
    rp_ = L1o / mhl
    vSv_m = (math.sqrt(Hd + 2 * eps_d * math.sqrt(rp_ * Hd) + rp_ * eps_d ** 2) + s * math.sqrt(rp_) * beta / 2) ** 2 / (c * c * (1 - er) ** 3)
    odd2 = up((2 * item({"ak": B4["I_N"]["ak"], "B": B4["I_N"]["B"]}, tI) / mh - item(b5["Ndel"], tI)) / g00) + eps_d ** 2
    vm_up = (math.sqrt(odd2) + s * beta / 2) / (c * (1 - er))
    # |E_u w~| and the insertion norms
    Ew = up((abs(item(it["A0w"], tI)) / (mh * g00) + sp * (2 * Dn + Bop * sp)) / (1 - er))
    nBp = max(beta, (kbar + Ew) * (1 + er)) / (1 - er)
    nBm = beta / 2 / (1 - er)
    # boundary vector
    q = lo(item(EW["items"]["I_mix"], tI)) * math.sqrt(EW["r_main"] / (up(g00) * up(item(EW["items"]["I_free"], tI))))
    Rw = math.sqrt(max(1.0 / (q - sp) ** 2 - 1.0, 0.0))
    return dict(rho1=rho1, rho=rho, Rp=Rp, vSv_p=vSv_p, vp=vp_up, vSv_m=vSv_m, vm=vm_up, nBp=nBp, nBm=nBm, Rw=Rw, eps_w=eps_w, eps_d=eps_d)




def mode_data(Jlo, Jhi, Q):
    """top even excited mode e_x: alpha^2 = cos^2(x', e_x) >= (q_x' - L2)/(L1 - L2) (Rayleigh quotient of x' = Q0 u_x/|Q0 u_x|, u_x = GS of e1 against psi-hat),
    c_x <= |<v+, e_x>|: alpha (|a_x| - Dlt) - sqrt(1 - alpha^2) sqrt(|v+|^2 - (|a_x| - Dlt)^2); L2 >= lambda_2^e (HS); simplicity of lambda_1^e from L2 < mu_x."""
    tI = iv.mpf([0 if Jhi is None else mp.mpf(1) / Jhi, mp.mpf(1) / Jlo]); tc = 1.0 / Jlo
    mh = 1 + mser["m1"] * tI + mser["m2"] * tI ** 2 + mser["m3"] * tI ** 3
    eps_r, s_vac, wres, eps_w, eps_d = vac(Jlo)
    er = float(eps_r); s = s_vac; c = math.sqrt(1 - s * s); sp = s * math.sqrt(2 / (1 + c))
    b5 = B5["items"]
    idx = [0, 1, 3]
    Ge = [[item(b5["g,%d,%d" % (min(a, b), max(a, b))], tI) for b in idx] for a in idx]
    Te = [[item(CT["items"]["T,%d,%d" % (min(a, b), max(a, b))], tI) for b in idx] for a in idx]
    Ae = [item(b5["A,%d" % a], tI) for a in idx]
    L = [[iv.mpf(0)] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i + 1):
            ssum = Ge[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            L[i][j] = iv.sqrt(ssum) if i == j else ssum / L[j][j]
    w = [iv.mpf(0)] * 3
    for i in range(3):
        w[i] = (Ae[i] - sum(L[i][k] * w[k] for k in range(i))) / L[i][i]
    g00 = Ge[0][0]
    ax = abs(w[1] / (mh * iv.sqrt(g00)))
    Y = [[iv.mpf(0)] * 3 for _ in range(3)]
    for j in range(3):
        for i in range(3):
            Y[i][j] = (Te[i][j] - sum(L[i][k] * Y[k][j] for k in range(i))) / L[i][i]
    Tm = [[iv.mpf(0)] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            Tm[i][j] = (Y[i][j] - sum(L[j][k] * Tm[i][k] for k in range(j))) / L[j][j]
    qx = float(Tm[1][1].a)
    # Ritz lower bounds with Gershgorin discs (disjointness checked)
    rz = ritz(tI, tc)
    de, dse = rz["even"]; do, dso = rz["odd"]
    U = lead * (1 + c1 * tI + c2 * tI ** 2 + c3 * tI ** 3) + remT
    Ap = rz["Ap_even"]
    order = sorted(range(3), key=lambda i: de[i])
    i0, ix = order[2], order[1]
    a_, c_ = float(Ap[i0][i0].a), float(Ap[ix][ix].a); b_ = float(abs(Ap[i0][ix]).b)
    mux_il = (a_ + c_) / 2 - math.sqrt(((a_ - c_) / 2) ** 2 + b_ * b_)   # 2nd eigenvalue >= smaller eigenvalue of the (vac, x) principal 2x2 (interlacing)
    mu0 = max(de); mux = mux_il; muz = max(do[0], 0.0)
    L2 = math.sqrt(max(float((U - mu0 ** 2 - mux ** 2 - muz ** 2).b), 0.0))
    # vacuum Lipschitz bound for v_a (Prop. 19.3 assembly)
    alpha_ = item(b5["A,0"], tI) / (mh * g00)
    eps_a = wres(cxi, 2.0)
    Bu2 = (2 * item(b5["Ia"], tI) / mh - item(b5["Na"], tI)) / g00 + iv.mpf([0, eps_a ** 2])
    vtr = iv.sqrt(iv.mpf([0, (Bu2 - alpha_ ** 2).b]))
    Dm = iv.mpf(TRB) - alpha_
    beta = iv.mpf(((alpha_ + Dm) / 2 + iv.sqrt(((Dm - alpha_) / 2) ** 2 + vtr ** 2)).b)
    erI = iv.mpf(er); spI = iv.mpf(sp)
    Dlt = float((spI * (beta + alpha_ + 2 * iv.sqrt(Bu2) + beta * spI) / (1 - erI) + vtr * erI / (1 - erI)).b)
    L1 = Q["rho1"] * max(mu0, float(mh.a) * (1 - er))
    qxp = qx - (1 + er) * float(mh.b) * sp * sp
    al2 = max(min((qxp - L2) / (L1 - L2), 1.0), 0.0)
    axl = float(ax.a) - Dlt
    cx = math.sqrt(al2) * axl - math.sqrt(1 - al2) * math.sqrt(max(Q["vp"] ** 2 - axl ** 2, 0.0))
    return dict(cx=cx, r2=L2 / mux, ro=Q["rho"] * max(mu0, float(mh.a) * (1 - er)) / mux, al2=al2, L2=L2, mux=mux, qx=qx, ax=float(ax.a), Dlt=Dlt,
                simple=L2 < mux, disjoint=True)


def passes_jensen(Q, d, m, kind):
    e = Q["Rw"] * Q["rho1"] ** d
    r1, r = Q["rho1"], Q["rho"]
    pX = math.sqrt(Q["vp"] ** 2 + Q["vm"] ** 2)
    nBX = Q["nBp"]
    Dm1 = r1 ** (m + 1) * e * e
    au = e * pX
    t2 = au * au * Dm1 / (1 - Dm1) + (2 * au * r1 ** m * e * (pX + nBX * e) + (r1 ** m * e * (pX + nBX * e)) ** 2) / (1 - Dm1)
    if kind == "flip":
        Cm = COV1 if m == 1 else Q["vSv_p"] * Q["Rp"] ** (m - 2) - Q["vSv_m"] * r ** (m - 2)
        ep = r1 ** ((m - 1) / 2) * Q["nBp"] * e
        em = r ** ((m - 1) / 2) * Q["nBm"] * e
        err = r1 ** ((m - 1) / 2) * Q["vp"] * 2 * ep + ep * ep + r ** ((m - 1) / 2) * Q["vm"] * 2 * em + em * em
        return Cm - err - t2 > 0
    P = math.sqrt(Q["vSv_p"] / r1) if m == 1 else math.sqrt(Q["vSv_p"] * Q["Rp"] ** (m - 2))
    et = r1 ** ((m - 1) / 2) * nBX * e
    return P >= et and P * (P - 2 * et) - et * et - t2 > 0


def passes_mode(Q, Mq, d, k, kind):
    """k = m - 1 >= 1; all terms in units of rho_x^k (rho_x = lambda_1^e/lam0 exactly; ratios bounded by r2, ro; rho_x <= rho1)."""
    e = Q["Rw"] * Q["rho1"] ** d
    X = Mq["cx"] - Q["nBp"] * e
    if X <= 0:
        return False
    pX = math.sqrt(Q["vp"] ** 2 + Q["vm"] ** 2)
    r1 = Q["rho1"]
    even_rest = Mq["r2"] ** k * (Q["vp"] + Q["nBp"] * e) ** 2
    if kind == "flip":
        odd = Mq["ro"] ** k * (Q["vm"] + Q["nBm"] * e) ** 2
    else:
        odd = Mq["ro"] ** k * (2 * Q["vm"] * Q["nBm"] * e + (Q["nBm"] * e) ** 2)
    Dm1 = r1 ** (k + 2) * e * e
    t2 = (r1 ** 2 * (e * pX) ** 2 * e * e + 2 * r1 * e * pX * e * (pX + Q["nBp"] * e) + r1 ** (k + 2) * (e * (pX + Q["nBp"] * e)) ** 2) / (1 - Dm1)
    return X * X - even_rest - odd - t2 > 0


