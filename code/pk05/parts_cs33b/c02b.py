

def tm_at(A, t):
    """(centre, radius) floats of a TM at the point t; the radius covers coefficient radii, remainder and Horner rounding"""
    c, rad, aps, tp = np.zeros_like(A.R), np.zeros_like(A.R), np.zeros_like(A.R), 1.0
    for d in range(A.k + 1):
        c = c + A.c[d].m * tp
        rad = rad + A.c[d].r * abs(tp)
        aps = aps + np.abs(A.c[d].m) * abs(tp)
        tp = tp * t
    return c, up((rad + A.R + 8 * (A.k + 2) * U * aps) * (1.0 + 4 * U) + ETA)


def poly_err(A, S, mode):
    """sup over |t| <= h of |P_a - S^2| (mode 'sqrt') or |1 - P_a S| (mode 'recip'); P_a = A's polynomial (remainder not included)"""
    k, h = A.k, A.h
    z = np.zeros_like(A.R)
    tot, hp = z.copy(), 1.0
    for d in range(2 * k + 1):
        acc = None
        for i in range(max(0, d - k), min(d, k) + 1):
            t = E.mr_mul(MR(S[i]), MR(S[d - i])) if mode == 'sqrt' else E.mr_mul(A.c[i], MR(S[d - i]))
            acc = t if acc is None else E.mr_add(acc, t)
        if mode == 'sqrt':
            base = A.c[d] if d <= k else MR(z.copy())
        else:
            base = MR(np.ones_like(z) if d == 0 else z.copy())
        tot = up(tot + E.mr_add(base, acc, -1.0).absu() * hp)
        hp = up(hp * h)
    return up(tot * (1.0 + 4 * (2 * k + 3) * U))


def tm_sqrt(A):
    """entrywise sqrt of a TM with A(t) >= 0. Where a_lo > 0: S = series sqrt of P_a and |sqrt(a) - S| <= (sup|P_a - S^2| + R)/(sqrt(a_lo) + S_lo);
    the crude TM of [0, sqrt(a_hi)] (centre and remainder sqrt(a_hi)/2) is used wherever it is not worse (v1_1: per entry, no threshold).
    Returns (TM, mask of the series entries)."""
    k, h = A.k, A.h
    lo, hi = tm_bounds(A)
    pos = lo > 0
    S = [np.sqrt(np.where(pos, A.c[0].m, 1.0))]
    for d in range(1, k + 1):
        acc = np.where(pos, A.c[d].m, 0.0)
        for i in range(1, d):
            acc = acc - S[i] * S[d - i]
        S.append(acc / (2.0 * S[0]))
    err = up(poly_err(A, S, 'sqrt') + A.R)
    slo = tm_bounds(TM([MR(x) for x in S], np.zeros_like(A.R), h, k))[0]
    den = dn(dn(np.sqrt(np.where(pos, lo, 1.0))) + slo)
    okp = pos & (slo > 0) & (den > 0)
    R = up(up(err / np.where(okp, den, 1.0)) * (1.0 + 2 * U))
    hs = up(np.sqrt(np.maximum(up(hi), 0.0)))
    use = okp & (R < 0.5 * hs)
    S = [np.where(use, S[0], 0.5 * hs)] + [np.where(use, x, 0.0) for x in S[1:]]
    return TM([MR(x) for x in S], np.where(use, R, up(0.5 * hs)), h, k), use


def tm_recip(A, rel=float('inf')):
    """entrywise 1/a (cs31): |1/a - S| <= (sup|1 - P_a S| + R sup|S|)/a_lo; entries with a_lo <= 0 (or R > rel a_lo) carry 0 and must be replaced"""
    k, h = A.k, A.h
    lo, hi = tm_bounds(A)
    ok = (lo > 0) & (A.R <= rel * np.maximum(lo, 0.0))
    c = [np.where(ok, A.c[d].m, 1.0 if d == 0 else 0.0) for d in range(k + 1)]
    S = [1.0 / c[0]]
    for d in range(1, k + 1):
        acc = np.zeros_like(c[0])
        for i in range(1, d + 1):
            acc = acc + c[i] * S[d - i]
        S.append(-acc / c[0])
    sl, sh = tm_bounds(TM([MR(x) for x in S], np.zeros_like(A.R), h, k))
    num = up(poly_err(A, S, 'recip') + up(A.R * np.maximum(np.abs(sl), np.abs(sh))))
    R = up(up(num / np.where(ok, lo, 1.0)) * (1.0 + 2 * U))
    return TM([MR(np.where(ok, x, 0.0)) for x in S], np.where(ok, R, 0.0), h, k), ok
