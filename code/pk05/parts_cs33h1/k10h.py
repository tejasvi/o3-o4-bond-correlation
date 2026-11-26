

def xc_vectors(SP, F, A):
    """XC_e_a = XU_e_a - alpha_e mu_a(0) u_a (truncated) ~ (T~_X - alpha T~) u_a, vertical e, a = 0..NCERT-1 (XU is unscaled)"""
    for e in VERT:
        for a in range(NCERT):
            m = SP['modes'][a]
            F['XC_%s_%d' % (e, a)] = C.fv_comb(1.0, F['XU_%s_%d' % (e, a)], -A['al'][e] * m['mud'][0], C.fv_trunc(m['u'], K_F))
    return F


def delta_bounds(ips, SB, SP, A, tb, ti, scale=1.0):
    """per type e: (F_e, D_e) for the infinity object, uniform in p >= PE[e] (INF): S(Xi_true(e,p), Y) F_e / c_p^2 = S(X_comp, Y) + error,
    |error| <= F_e D_e |(Lambda^2 T~)^k Y|. Also '_eta1' = eta(P_EX) + sqrt2 s1' bounds |chi1 + J'(q) - u1/|u1|| for q >= P_EX.
    scale multiplies every D_e (plant P-DELTA)."""
    I, ur, s, modes = SB['I'], SB['urem'], SB['s'], SP['modes']
    n0lo, n0hi = I[0][1], I[0][2]
    beta = modecoef(ips, SB, 'J0', tb, ti)
    b0 = abs(beta[0]).lower()
    wp = amax(arb(0), (ips.val('J0', 'J0', tb, ti).upper() - sum(((x * x).lower() for x in beta), arb(0))).upper()).sqrt()
    rat = lambda a, pp: ((I[a][2] / n0lo) ** pp).upper()
    tail = lambda pp: ((ur / n0lo) ** pp * wp / b0).upper()
    etaf = lambda pp: (sum((rat(a, pp) * abs(beta[a]).upper() / b0 for a in range(1, NCERT)), arb(0)) + tail(pp)).upper()
    eta = etaf(P_EX)
    nu = [ips.val('U%d' % a, 'U%d' % a, tb, ti).sqrt() for a in range(NCERT)]
    s0p = (s[0] + arb(ips.fvs['u1'].rho) / nu[0].lower()).upper()
    uu = ips.val('u1', 'u1', tb, ti).upper()
    out = {'_eta1': (eta + SQ2 * s0p).upper()}
    for e in TYPES:
        p = PE[e]
        eta_e = etaf(p)
        if e in HORIZ:
            Rop = arb(float(up(max(A['gmax'][e] - A['al'][e], A['al'][e]))))   # v1_8 (Z3): rounded up, as in tr_slack
            ne = [(ips.norm('RU_%s_%d' % (e, a)) / nu[a].lower() + Rop * SQ2 * s[a] + (arb(A['epsW']) / I[a][1]).sqrt()).upper()
                  for a in range(NCERT)]                                  # v1_5 (R9 TR7): + |R' P_tail chi_a|
            RTn = (n0hi * (Rop ** 2 * n0hi + arb(A['epsW']))).sqrt()          # v1_5 (R9 TR7): |R' T~| in place of |R'|
            m = sum((rat(a, p) * abs(beta[a]).upper() / b0 * ne[a] for a in range(1, NCERT)), arb(0)) + RTn / n0lo * tail(p - 1)
            Fe = uu
        else:
            Rop = arb(float(up(1.0 + abs(A['al'][e]))))   # v1_8 (Z3): rounded up
            ne = []
            for a in range(NCERT):
                mm = modes[a]
                dmu = arb(float(up(sum(abs(c_) * SP['h'] ** d for d, c_ in enumerate(mm['mud']) if d > 0) * (1.0 + 1e-12))))
                cxc = arb(abs(A['al'][e] * mm['mud'][0])) * arb(2.0 ** -52) * nu[a].upper()   # v1_7 (rule (b)): float coefficient of XC
                num = (arb(ips.norm('XC_%s_%d' % (e, a))) + arb(abs(A['al'][e])) * (dmu * nu[a].upper() + arb(mm['rb']))
                       + n0hi * Rop * arb(A['trho'][a]) + cxc)
                ne.append(((num / nu[a].lower() + n0hi * Rop * SQ2 * s[a] + Rop * (arb(A['eT']) * I[a][2]).sqrt()) / n0lo).upper())
            m = sum((rat(a, p - 1) * abs(beta[a]).upper() / b0 * ne[a] for a in range(1, NCERT)), arb(0)) + Rop * tail(p - 1)
            Fe = (arb(A['pmax']) * n0hi * uu).upper()
        D = (m + eta_e * ne[0] + eta_e * m + SQ2 * s0p * (ne[0] + Rop)).upper()
        out[e] = (Fe, (D * scale).upper())
    return out
