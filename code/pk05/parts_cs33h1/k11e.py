

def near_checks(ips, SB, obs, DB, ps, tb, ti, negate=None, sel=None):
    """NEAR: every unordered object pair, k < K_EX (n >= 4): S = <J_X,T^k J_Y><I_X,T^k I_Y> - <J_X,T^k I_Y><I_X,T^k J_Y> (scaled T^ = p T~),
    minus F D (ps^2 nu1 nu2)^k |.| for infinity objects (INF), ps >= sup p. S is symmetric in X, Y (T~ symmetric): sel 'h' takes the pairs with a
    horizontal object, oriented so that the propagated object Y is horizontal; sel 'v' the pairs of two vertical objects; None all pairs.
    Returns (count, min value/|X||Y|, its configuration, failures, negatives)."""
    I = SB['I']
    lam = (arb(ps) ** 2 * I[0][2] * I[1][2]).upper()
    nchk, worst, wcfg, fails, negs = 0, None, None, [], []
    nrm = {ob: (arb(ips.norm(ob[2])) * arb(ips.norm(ob[3])) * (1 + arb(ips.slack))).upper() for ob in obs}   # v1_8 (Z5): true norms (TR3)
    for ix, X0 in enumerate(obs):
        for Y0 in obs[ix:]:
            hx, hy = X0[0] in HORIZ, Y0[0] in HORIZ
            if (sel == 'h' and not (hx or hy)) or (sel == 'v' and (hx or hy)):
                continue
            X, Y = (Y0, X0) if (sel == 'h' and not hy) else (X0, Y0)
            for k in range(K_EX):
                if X[1] is not None and Y[1] is not None and X[1] + Y[1] + k < 2:
                    continue
                jy, iy = (Y[2], Y[3]) if k == 0 else (Y[4], Y[5])
                S = ips.val(X[2], jy, tb, ti) * ips.val(X[3], iy, tb, ti) - ips.val(X[2], iy, tb, ti) * ips.val(X[3], jy, tb, ti)
                if negate is not None and (X[0], X[1], Y[0], Y[1], k) == negate:
                    S = -S
                err = arb(0)
                lk = lam ** k
                if X[1] is None:
                    err = err + arb(DB[X[0]][0]) * DB[X[0]][1] * lk * nrm[Y]
                if Y[1] is None:
                    err = err + arb(DB[Y[0]][0]) * DB[Y[0]][1] * lk * nrm[X]
                if X[1] is None and Y[1] is None:
                    err = err + arb(DB[X[0]][0]) * DB[X[0]][1] * arb(DB[Y[0]][0]) * DB[Y[0]][1] * lk
                err = err.upper()
                lo, hi = (S.lower() - err), (S.upper() + err)
                nchk += 1
                v = E.fdn_arb(lo / (nrm[X] * nrm[Y]))
                if worst is None or v < worst:
                    nn = nrm[X] * nrm[Y]
                    worst, wcfg = v, (X[0], X[1], Y[0], Y[1], k, float(S.mid() / nn), E.fup_arb((hi - lo) / nn))
                if not (lo > 0):
                    fails.append((X[0], X[1], Y[0], Y[1], k))
                    if hi < 0:
                        negs.append((X[0], X[1], Y[0], Y[1], k))
    return nchk, worst, wcfg, fails, negs
