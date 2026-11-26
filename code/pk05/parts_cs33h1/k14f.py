

def checks_all(ips, SP, A, SBs, obs, NS, h, part, near_neg=None, far_neg=None, dscale=1.0, sub=None):
    """the checks of a part on the subballs (all, or the indices in sub): part A runs FAR, part B runs NEAR (Bh, Bv: its two halves,
    see near_checks); v1_2: no same-column checks (coverage table)"""
    tot = dict(near=[0, None, None], far=[0, 0, None, None], fails=[], negs=[])
    nrm = {ob: (arb(ips.norm(ob[2])) * arb(ips.norm(ob[3])) * (1 + arb(ips.slack))).upper() for ob in obs}   # v1_8 (Z5): true norms (TR3)
    for ti, tb in enumerate(E.subballs(h, NSUB)):
        if sub is not None and ti not in sub:
            continue
        sb = SBs[ti]
        DB = delta_bounds(ips, sb, SP, A, tb, ti, dscale)
        if 'A' in part:
            OD = {ob: objdata(ips, sb, ob, tb, ti, A.get('ext')) for ob in obs}
            n2, k2, w2, c2, f2, g2 = far_checks(sb, OD, obs, DB, nrm, far_neg)
            tot['far'][0] += n2
            tot['far'][1] = max(tot['far'][1], k2 or 0)
            if w2 is not None and (tot['far'][2] is None or w2 < tot['far'][2]):
                tot['far'][2], tot['far'][3] = w2, (ti,) + c2
            tot['fails'] += [('far', ti) + f for f in f2]
            tot['negs'] += [('far', ti) + f for f in g2]
        if 'B' in part:
            sel = 'h' if part == 'Bh' else ('v' if part == 'Bv' else None)
            n1, w1, c1, f1, g1 = near_checks(ips, sb, obs, DB, A['pmax'], tb, ti, near_neg, sel)
            tot['near'][0] += n1
            if w1 is not None and (tot['near'][1] is None or w1 < tot['near'][1]):
                tot['near'][1], tot['near'][2] = w1, (ti,) + c1
            tot['fails'] += [('near', ti) + f for f in f1]
            tot['negs'] += [('near', ti) + f for f in g1]
        C.guard('checks')
    return tot


def vec_plant_ext(ips, SP, SBs, A):
    """P-VEC: mode 1 replaced by u1' = u_1 + 0.03 u_3 (same sector); eps' from stored residual bounds (linearity); returns ext(v, tb, ti)"""
    m1, m3 = SP['modes'][1], SP['modes'][3]
    h = SP['h']
    dmu = float(up(sum(abs(a - b) * h ** d for d, (a, b) in enumerate(zip(m1['mud'], m3['mud']))) * (1.0 + 1e-12)))
    n3 = ips.norm('U3')
    rb = float(up(m1['rb'] + 0.03 * (m3['rb'] + dmu * n3)))
    nlo = float(dn(m1['nlo'] - 0.03 * n3))

    def ext(v, tb, ti):
        g = SBs[ti]['gam'].get(1)
        ip = ips.val('U1', v, tb, ti) + 0.03 * ips.val('U3', v, tb, ti)
        nu = (ips.val('U1', 'U1', tb, ti) + 0.06 * ips.val('U1', 'U3', tb, ti) + 0.0009 * ips.val('U3', 'U3', tb, ti)).sqrt()
        s = (arb(rb) / arb(nlo) / g).upper() if (g is not None and nlo > 0) else arb(10)
        return ip, nu, s
    return ext
