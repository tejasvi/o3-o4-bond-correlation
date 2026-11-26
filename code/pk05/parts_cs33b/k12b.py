

def far_checks(SB, OD, obs, DB, nrm, negate=None):
    """FAR: every unordered object pair, all k >= K_EX. f(k) = S(k)/(nu1 nu2)^k = X_01 Y_01 + sum_{ab != 01} r_ab^k X_ab Y_ab
    +- (u_rem/nu2)^k |X^perp||Y^perp| +- Delta, r_ab = nu_a nu_b/(nu1 nu2). f(k) > 0 is checked for K_EX <= k < k*, where k* is the first k
    with the monotone lower bound g(k) (absolute values for ab != 01) > 0. Returns (count, max k*, min f/|X||Y|, failures, negatives)."""
    I, nc = SB['I'], len(SB['cert'])
    nuI = [ival(I[a][1], I[a][2]) for a in range(nc)]
    pairs = [(a, b) for a in range(nc) for b in range(a + 1, nc) if (a, b) != (0, 1)]
    r = {ab: (nuI[ab[1]] / nuI[1]) if ab[0] == 0 else (nuI[ab[0]] * nuI[ab[1]] / (nuI[0] * nuI[1])) for ab in pairs}
    rhi = {ab: r[ab].upper() for ab in pairs}
    q = (SB['urem'] / I[1][1]).upper()
    if not (q < 1 and all(rhi[ab] < 1 for ab in pairs)):
        return 0, None, None, None, [('ratios', None)], []
    nchk, kmax, worst, wcfg, fails, negs = 0, 0, None, None, [], []
    for ix, X in enumerate(obs):
        for Y in obs[ix:]:
            dX, dY = OD[X], OD[Y]
            lead = dX['X'][(0, 1)] * dY['X'][(0, 1)]
            if negate is not None and (X[0], X[1]) == negate:
                lead = -lead
            cst = arb(0)
            if X[1] is None:
                cst = cst + arb(DB[X[0]][0]) * DB[X[0]][1] * nrm[Y]
            if Y[1] is None:
                cst = cst + arb(DB[Y[0]][0]) * DB[Y[0]][1] * nrm[X]
            if X[1] is None and Y[1] is None:
                cst = cst + arb(DB[X[0]][0]) * DB[X[0]][1] * arb(DB[Y[0]][0]) * DB[Y[0]][1]
            cst = cst.upper()
            PP = {ab: dX['X'][ab] * dY['X'][ab] for ab in pairs}
            Pa = {ab: abs(PP[ab]).upper() for ab in pairs}
            pp = (dX['perp'] * dY['perp']).upper()
            rk = {ab: r[ab] ** K_EX for ab in pairs}
            rkh = {ab: rhi[ab] ** K_EX for ab in pairs}
            qk = q ** K_EX
            ok, k = False, K_EX
            while k <= K_MAX:
                f = lead + sum((rk[ab] * PP[ab] for ab in pairs), arb(0))
                lo, hi = f.lower() - qk * pp - cst, f.upper() + qk * pp + cst
                nchk += 1
                v = E.fdn_arb(lo / (nrm[X] * nrm[Y]))
                if worst is None or v < worst:
                    nn = nrm[X] * nrm[Y]
                    worst, wcfg = v, (X[0], X[1], Y[0], Y[1], k, float(lead.mid() / nn), E.fup_arb((qk * pp + cst) / nn))
                if not (lo > 0):
                    if hi < 0:
                        negs.append((X[0], X[1], Y[0], Y[1], k))
                    break
                g = lead.lower() - sum((rkh[ab] * Pa[ab] for ab in pairs), arb(0)) - qk * pp - cst
                if g > 0:
                    ok = True
                    break
                rk = {ab: rk[ab] * r[ab] for ab in pairs}
                rkh = {ab: (rkh[ab] * rhi[ab]).upper() for ab in pairs}
                qk = (qk * q).upper()
                k += 1
            kmax = max(kmax, k)
            if not ok:
                fails.append((X[0], X[1], Y[0], Y[1], k))
    return nchk, kmax, worst, wcfg, fails, negs
