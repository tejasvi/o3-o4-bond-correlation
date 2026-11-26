

def scal_poly(mud, h):
    """(NORM) exact float coefficients of p(t), the degree-K_F Taylor polynomial at t = 0 of 1/mu_0(t) (mu_0 the fitted top eigenvalue;
    any positive polynomial would do), with sup_{|t|<=h} |p| <= pmax and inf_{|t|<=h} p >= plo (arb, rounded outward)"""
    m = [float(x) for x in mud]
    pc = [1.0 / m[0]]
    for d in range(1, K_F + 1):
        acc = 0.0
        for i in range(1, min(d, len(m) - 1) + 1):
            acc += m[i] * pc[d - i]
        pc.append(-acc / m[0])
    H = arb(h)
    rest = sum((abs(arb(c_)) * H ** d for d, c_ in enumerate(pc) if d > 0), arb(0))
    return pc, E.fup_arb(abs(arb(pc[0])) + rest), E.fdn_arb(arb(pc[0]) - rest)


def fv_pmul(v, pc, pmax, k):
    """(NORM) the family vector p(t) v(t) for the exact float polynomial p (|p| <= pmax on [-h, h]): products with their rounding radii;
    degrees above k and all radii go to the 2-norm remainder, and the old remainder is multiplied by pmax"""
    nd = len(v.c) + len(pc) - 1
    cs, rad, hp = [], 0.0, 1.0
    for d in range(nd):
        acc = None
        for i in range(max(0, d - len(v.c) + 1), min(d, len(pc) - 1) + 1):
            t_ = E.mr_scale(MR(v.c[d - i]), pc[i])
            acc = t_ if acc is None else E.mr_add(acc, t_)
        if d <= k:
            cs.append(acc.m)
            rad = float(up(rad + C.vec_norm_ub(acc.r) * hp))
        else:
            rad = float(up(rad + C.vec_norm_ub(acc.absu()) * hp))
        hp = float(up(hp * v.h))
    return FV(cs, float(up(up(pmax * v.rho) * (1.0 + 2 * U) + rad)), v.h)


MODEPAR = [None]


def rho_even(name):
    """(PAR) the objects that are exactly even under the row reflection rho: J(p), the bulk seeds u1 and T~ u1, and every mh object"""
    return ((name[0] == 'J' and name[1:].isdigit()) or name in ('u1', 'Tu1', 'Y_mh', 'TY_mh') or name.startswith('I_mh_')
            or name.startswith('P_mh_'))
