#!/usr/bin/env python3
# cs33b_rh_core.py (pk05, P-RH Stage B, v1_1 of cs33_rh_core cfa3c2da): shared arithmetic and operators of route H on the uniform 3 x n strip,
# N = 3, 4. v1_1 changes: tm_sqrt and the insertion multiplier g use the series enclosure per entry wherever it beats the crude one (c02b, c05b).
# Math: LEMMA_STRIP_RH_v1 (05964cd1) R1-R6; Lambda^2 identity, objects, near/far regimes and Taylor-model propagation in the header of
# cs33b_rh_cert.py. Route H's MR/TM arithmetic, corner_tm, kernel_tm, tm_lin_rows come from hubcert_v1e.py (c08d33c1), loaded read-only after
# its sha256 check. Imported by cs33b_rh_cert.py (sha-checked); never run alone.
import sys
import time
import math
import hashlib
import importlib.util
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.sparse.linalg import LinearOperator, eigsh

DIR = '/mnt/g2/release/root/code/pk05/'
ENGINE, ESHA = DIR + 'hubcert_v1e.py', 'fbed2d93a84a738207d59b3bd451e6c7572a293c2d356167c0a57a2ddac1ad30'
CAP = [1e9]


def guard(tag):
    if time.process_time() > CAP[0] - 5.0:
        print('CAP-STOP at %.1f s (%s)' % (time.process_time(), tag), flush=True)
        sys.exit(3)


def load(path, sha, name):
    with open(path, 'rb') as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != sha:
        print('SHA MISMATCH %s %s' % (path, got), flush=True)
        sys.exit(2)
    spec_ = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)
    return mod


E = load(ENGINE, ESHA, 'hubcert_v1e_mod')
MR, TM, arb, U, ETA, up, gam = E.MR, E.TM, E.arb, E.U, E.ETA, E.up, E.gam
SQ2 = arb(2).sqrt()


def dn(x):
    return np.nextafter(x, -np.inf)


def amin(a, b):
    return a if a < b else b


def amax(a, b):
    return a if a > b else b


def tm_bounds(A):
    """entrywise floats lo <= A(t) <= hi for every |t| <= h"""
    rest, hp = np.zeros_like(A.R), 1.0
    for d in range(1, A.k + 1):
        hp = up(hp * A.h)
        rest = up(rest + A.c[d].absu() * hp)
    rest = up((rest + A.R + A.c[0].r) * (1.0 + 4 * (A.k + 3) * U))
    m = A.c[0].m
    return dn(m - rest), up(m + rest)


def tm_const(v, like, h, k):
    """degree-k TM of an exact float (array or scalar) broadcast to the shape of like"""
    z = np.zeros_like(np.asarray(like, dtype=np.float64))
    return TM([MR(np.asarray(v, dtype=np.float64) + z)] + [MR(z.copy()) for _ in range(k)], z.copy(), h, k)


def tm_trunc(A, k):
    """the same function as a degree-k TM (k <= A.k): coefficients above k move to the remainder"""
    if k >= A.k:
        return A
    extra, hp = np.zeros_like(A.R), _hp(A.h, k + 1)
    for d in range(k + 1, A.k + 1):
        extra = up(extra + A.c[d].absu() * hp)
        hp = up(hp * A.h)
    return TM([A.c[d] for d in range(k + 1)], up((A.R + extra) * (1.0 + 4 * U)), A.h, k)


def _hp(h, d):
    v = 1.0
    for _ in range(d):
        v = up(v * h)
    return v


def poly(A, t):
    """float value of A's polynomial part at t (Horner); remainders ignored (float operator only)"""
    v = A.c[A.k].m.copy()
    for d in range(A.k - 1, -1, -1):
        v = v * t + A.c[d].m
    return v


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


def mr_sum(A):
    n = A.m.size
    g = gam(n + 2)
    r = float(np.sum(A.r)) + g * float(np.sum(np.abs(A.m)))
    return MR(np.float64(float(np.sum(A.m))), np.float64(up(r * (1.0 + 4 * g) + n * ETA)))


def tm_sum(A):
    """scalar TM of the sum of all entries"""
    n = A.R.size
    g = gam(n + 2)
    return TM([mr_sum(c) for c in A.c], np.float64(up(float(np.sum(A.R)) * (1.0 + 4 * g) + n * ETA)), A.h, A.k)


def vec_norm_ub(v):
    """float >= the 2-norm of a nonnegative float array"""
    return float(up(math.sqrt(up(float(np.sum(up(v * v))) * (1.0 + 4 * gam(v.size + 2))))))


def tm_norm_ub(A, mask=None):
    """float >= sup over |t| <= h of the 2-norm of A(t) (restricted to the mask)"""
    v = up(A.absP() + A.R)
    return vec_norm_ub(v * mask if mask is not None else v)


def cas_mr(N, l1, l3, plant=False):
    """Casimir block (R2) on m = 0..s-1: diagonal exact; off-diagonal as MR. N = 3: sqrt of an exact integer (x 2 at m = 0 inside);
    N = 4: 2(m+1) sqrt(p/q), p, q exact integers (three roundings, enclosed with 4u)."""
    s = min(l1, l3) + 1
    m = np.arange(s, dtype=np.float64)
    mm = m[:-1]
    if N == 3:
        d = l1 * (l1 + 1.0) + l3 * (l3 + 1.0) - 2.0 * m * m
        p = (l1 - mm) * (l1 + mm + 1.0) * (l3 - mm) * (l3 + mm + 1.0)
        if s > 1:
            p[0] *= 2.0
        e = np.sqrt(p)
        r = 2 * U * e
    else:
        d = l1 * (l1 + 2.0) + l3 * (l3 + 2.0) - 2.0 * m * (m + 1.0)
        p = ((l1 + 1.0) ** 2 - (mm + 1.0) ** 2) * ((l3 + 1.0) ** 2 - (mm + 1.0) ** 2)
        q = (2.0 * mm + 1.0) * (2.0 * mm + 3.0)
        e = 2.0 * (mm + 1.0) * np.sqrt(p / q)
        r = 4 * U * e
    if plant and s > 1:
        e = e.copy()
        e[-1] *= 1.01
    return d, MR(e, up(r))


def cert_block(N, l1, l3, plant=False):
    """(U, delta): float eigenvectors of the block and radii delta_j >= max_i |Q_ij - U_ij| (R2, Davis-Kahan against l2(l2+N-2))"""
    s = min(l1, l3) + 1
    if s == 1:
        return np.ones((1, 1)), np.zeros(1)
    l2 = abs(l1 - l3) + 2 * np.arange(s)
    mu = (l2 * (l2 + N - 2)).astype(np.float64)
    d, e = cas_mr(N, l1, l3, plant)
    Uf = eigh_tridiagonal(d, e.m)[1]
    Um = MR(Uf)
    sub = MR(np.concatenate(([0.0], e.m)), np.concatenate(([0.0], e.r)))
    sup = MR(np.concatenate((e.m, [0.0])), np.concatenate((e.r, [0.0])))
    CU = E.mr_add(E.tri_rows(sub, sup, Um, 0.0), E.mr_mul(MR(d[:, None]), Um))
    res = E.mr_add(CU, E.mr_mul(Um, MR(mu[None, :])), -1.0)
    g = gam(s + 2)
    rn = up(np.sqrt(up(np.sum(up(res.absu() ** 2), axis=0) * (1.0 + 4 * g))))
    nn = np.sum(Uf * Uf, axis=0)
    nlo, nhi = dn(np.sqrt(dn(nn * (1.0 - 4 * g)))), up(np.sqrt(up(nn * (1.0 + 4 * g))))
    gap = np.full(s, np.inf)
    gap[1:] = mu[1:] - mu[:-1]
    gap[:-1] = np.minimum(gap[:-1], mu[1:] - mu[:-1])
    dev = np.maximum(up(nhi - 1.0), up(1.0 - nlo))
    return Uf, up(up(1.4142135623730954 * rn / (gap * nlo)) * (1.0 + 4 * U) + dev)


def build_Q(N, L):
    """groups as cs30/cs31: for s = 1..L+1 the pairs (l1, l3) with min = s-1 (blocks (l1, l3) and (l3, l1) share Q, R1 (c));
    returns (groups, max radius, number of certified blocks)"""
    groups, qmax, nb = [], 0.0, 0
    for s in range(1, L + 2):
        base = [cert_block(N, s - 1, l3) for l3 in range(s - 1, L + 1)]
        nb += len(base)
        pairs = [(s - 1, l3) for l3 in range(s - 1, L + 1)] + [(l1, s - 1) for l1 in range(s, L + 1)]
        bl = base + base[1:]
        Qm, Qr = np.array([b[0] for b in bl]), np.array([b[1] for b in bl])
        qmax = max(qmax, float(np.max(Qr)))
        i1, i3 = np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs])
        groups.append((s, i1, i3, Qm, Qr))
        guard('Q')
    return groups, qmax, nb


def mr_blk(Qm, Qr, X, fwd):
    """one group: Q x (fwd: product -> hub, 'pij,pj->pi') or Q^T x ('pij,pi->pj'); true Q = Qm + Delta, |Delta_pij| <= Qr_pj"""
    s = Qm.shape[1]
    g = gam(s + 2)
    aQ, ax = np.abs(Qm), np.abs(X.m)
    if fwd:
        m = np.einsum('pij,pj->pi', Qm, X.m)
        R = np.einsum('pij,pj->pi', aQ, X.r + g * ax) + np.sum(Qr * (ax + X.r), axis=1)[:, None]
    else:
        m = np.einsum('pij,pi->pj', Qm, X.m)
        R = np.einsum('pij,pi->pj', aQ, X.r + g * ax) + Qr * np.sum(ax + X.r, axis=1)[:, None]
    return MR(m, up(R * (1.0 + 4 * g) + s * ETA))


def tm_blk(G, A, fwd):
    """TM of Q A (fwd) or Q^T A on the dense (L+1)^3 state arrays, group by group (Q is t-independent)"""
    k = A.k
    cm = [np.zeros_like(A.R) for _ in range(k + 1)]
    cr = [np.zeros_like(A.R) for _ in range(k + 1)]
    R = np.zeros_like(A.R)
    for (s, i1, i3, Qm, Qr) in G:
        for d in range(k + 1):
            y = mr_blk(Qm, Qr, MR(A.c[d].m[i1, i3, :s], A.c[d].r[i1, i3, :s]), fwd)
            cm[d][i1, i3, :s] = y.m
            cr[d][i1, i3, :s] = y.r
        aQ = np.abs(Qm) + Qr[:, None, :]
        e = A.R[i1, i3, :s]
        Ro = np.einsum('pij,pj->pi', aQ, e) if fwd else np.einsum('pij,pi->pj', aQ, e)
        R[i1, i3, :s] = up(Ro * (1.0 + 4 * gam(s + 2)) + s * ETA)
    return TM([MR(cm[d], cr[d]) for d in range(k + 1)], R, A.h, k)


def tm_G(KA, KBT, A, L):
    """TM of G A on hub states: in sector m, W = KA[m] V KBT[m] (side-1 kernel times V times the transposed side-3 kernel)"""
    k = A.k
    cm = [np.zeros_like(A.R) for _ in range(k + 1)]
    cr = [np.zeros_like(A.R) for _ in range(k + 1)]
    R = np.zeros_like(A.R)
    for m in range(L + 1):
        V = TM([MR(np.ascontiguousarray(c.m[m:, m:, m]), np.ascontiguousarray(c.r[m:, m:, m])) for c in A.c],
               np.ascontiguousarray(A.R[m:, m:, m]), A.h, k)
        W = E.tm_matmul(E.tm_matmul(KA[m], V), KBT[m])
        for d in range(k + 1):
            cm[d][m:, m:, m] = W.c[d].m
            cr[d][m:, m:, m] = W.c[d].r
        R[m:, m:, m] = W.R
        guard('tmG')
    return TM([MR(cm[d], cr[d]) for d in range(k + 1)], R, A.h, k)


def f_blk(G, X, fwd):
    Y = np.zeros_like(X)
    for (s, i1, i3, Qm, Qr) in G:
        x = X[i1, i3, :s]
        Y[i1, i3, :s] = np.einsum('pij,pj->pi', Qm, x) if fwd else np.einsum('pij,pi->pj', Qm, x)
    return Y


def f_T(op, X):
    """float operator: op = (groups, [side-1 kernels], [side-3 kernels], D^1/2, L) from TM polynomial parts at one t"""
    G, Ea, Eb, Dh, L = op
    Y = f_blk(G, Dh * X, True)
    Z = np.zeros_like(Y)
    for m in range(L + 1):
        Z[m:, m:, m] = Ea[m] @ Y[m:, m:, m] @ Eb[m].T
    return Dh * f_blk(G, Z, False)


def build(N, b0, h, L, K, out):
    """route H inputs as degree-K TMs: a~ (labels 0..2L+2), s = sqrt(a~), g = (T a~)/a~ (labels 0..2L, crude where the reciprocal is
    unusable), and per sector m: E~_m and X E~_m on degrees m..L (and their transposes)"""
    t1 = time.process_time()
    Kb, n1 = E.choose_Kb(h, K), E.choose_n1(b0)
    tail_f = E.fup_arb(E.series_tail(b0, n1))
    emb = E.arb_to_mr((-arb(b0)).exp())
    atm = E.corner_tm(N, b0, h, K, Kb, 2 * L)
    al, ga = E.t_coeffs(N, 2 * L + 2)
    nl = 2 * L + 3
    sub, sup = MR(ga.m[:nl].copy(), ga.r[:nl].copy()), MR(al.m[:nl].copy(), al.r[:nl].copy())
    sup.m[nl - 1], sup.r[nl - 1] = 0.0, 0.0
    Ta = E.tm_lin_rows(sub, sup, atm, 0.0).sub(slice(0, 2 * L + 1))
    a2 = atm.sub(slice(0, 2 * L + 1))
    s, sok = tm_sqrt(a2)
    rinv, rok = tm_recip(a2)
    g = E.tm_mul(Ta, rinv)
    lv = np.arange(2 * L + 1, dtype=np.float64)
    glo, ghi = dn(lv / up(b0 + h)), up(1.0 + up(lv / dn(b0 - h)))        # 0 < I_{nu+1}/I_nu < 1
    gm = 0.5 * glo + 0.5 * ghi
    gr = up(np.maximum(up(ghi - gm), up(gm - glo)))
    ok = rok & (g.R < gr)                                                   # v1_1: series where better than crude
    gc = [MR(np.where(ok, g.c[0].m, gm), np.where(ok, g.c[0].r, 0.0))]
    gc += [MR(np.where(ok, c.m, 0.0), np.where(ok, c.r, 0.0)) for c in g.c[1:]]
    g = TM(gc, np.where(ok, g.R, gr), h, K)
    Ek, XEk = [], []
    for m in range(L + 1):
        n = L + 1 - m
        Ef = E.kernel_tm(N, m, b0, h, K, Kb, L, n1, emb, tail_f)        # rows m..L+2, cols m..L
        x = E.x_offdiag(N, m, L + 3)
        nr = Ef.R.shape[0]
        xs = MR(np.concatenate(([0.0], x.m[:nr - 1])), np.concatenate(([0.0], x.r[:nr - 1])))
        xp = MR(np.concatenate((x.m[:nr - 1], [0.0])), np.concatenate((x.r[:nr - 1], [0.0])))
        Ek.append(Ef.sub(slice(0, n)))
        XEk.append(E.tm_lin_rows(xs, xp, Ef, 0.0).sub(slice(0, n)))
        guard('kernel')
    tr = lambda A: TM([MR(c.m.T.copy(), c.r.T.copy()) for c in A.c], A.R.T.copy(), A.h, A.k)
    out('BUILD N=%d L=%d K=%d Kb=%d n1=%d sertail=%.3e; labels 0..%d: sqrt TM on %d, g TM on %d (crude elsewhere); max rem a~ %.3e, '
        'E~ %.3e, XE~ %.3e; t=%.1f s' % (N, L, K, Kb, n1, tail_f, 2 * L, int(np.sum(sok)), int(np.sum(ok)), float(np.max(a2.R)),
                                        max(float(np.max(A.R)) for A in Ek), max(float(np.max(A.R)) for A in XEk), time.process_time() - t1))
    return dict(atm=atm, s=s, g=g, E=Ek, ET=[tr(A) for A in Ek], XE=XEk, XET=[tr(A) for A in XEk])


def trunc_consts(N, b0, h, L):
    """(eps_T, eps_e, A^3) as floats rounded up (R3 (v), R4 (iii)): A = e^h (b0/b-)^lam I_lam(b-)/I_lam(b0); eps_T = A^3 I_{L+1+lam}(b+)/
    I_lam(b+); eps_e = A^3 I_{L+lam}(b+)/I_lam(b+)"""
    lam = arb(N - 2) / 2
    b0a, bl, bh = arb(b0), arb(b0) - arb(h), arb(b0) + arb(h)
    A = arb(h).exp() * (b0a / bl) ** lam * bl.bessel_i(lam) / b0a.bessel_i(lam)
    I0 = bh.bessel_i(lam)
    return (E.fup_arb(A ** 3 * bh.bessel_i(lam + L + 1) / I0), E.fup_arb(A ** 3 * bh.bessel_i(lam + L) / I0), E.fup_arb(A ** 3))


def states(B, L, h, K):
    """product-basis TMs on the dense cube (l1, l3, j), l2 = |l1 - l3| + 2j, j <= min(l1, l3): D^1/2 = s s s, D = a~ a~ a~, and the
    horizontal insertion multipliers g_th = g_l1, g_mh = g_l2, g_bh = g_l3; mask and the flat index of valid states"""
    n = L + 1
    l2i = np.zeros((n, n, n), dtype=np.int64)
    mask = np.zeros((n, n, n))
    for l1 in range(n):
        for l3 in range(n):
            q = min(l1, l3) + 1
            l2i[l1, l3, :q] = abs(l1 - l3) + 2 * np.arange(q)
            mask[l1, l3, :q] = 1.0

    def bc(v, ax):
        shp = [1, 1, 1]
        shp[ax] = n
        return TM([MR(c.m[:n].reshape(shp), c.r[:n].reshape(shp)) for c in v.c], v.R[:n].reshape(shp), h, K)

    def gat(v):
        return TM([MR(c.m[l2i], c.r[l2i]) for c in v.c], v.R[l2i], h, K)
    s, a, g = B['s'], B['atm'].sub(slice(0, 2 * L + 1)), B['g']
    Dh = E.tm_mul(E.tm_mul(bc(s, 0), bc(s, 1)), gat(s))
    D = E.tm_mul(E.tm_mul(bc(a, 0), bc(a, 1)), gat(a))
    return dict(mask=mask, idx=np.flatnonzero(mask.ravel()), Dh=Dh, D=D, g={'th': bc(g, 0), 'mh': gat(g), 'bh': bc(g, 1)})


def to_dense(v, L):
    """compact (valid states) -> dense cube"""
    n = L + 1
    out = np.zeros(n ** 3)
    out[STATE['idx']] = v
    return out.reshape((n, n, n))


def to_compact(A):
    return np.asarray(A).reshape(-1)[STATE['idx']]


STATE = {}


def op_apply(OP, X):
    """TM image of a TM state X (dense) under OP = (groups, side-1 kernels, side-3 kernels transposed, D^1/2 TM, L): D^1/2 Q^T G Q D^1/2 X"""
    G, KA, KBT, Dh, L = OP
    Y = tm_blk(G, E.tm_mul(Dh, X), True)
    Y = tm_blk(G, tm_G(KA, KBT, Y, L), False)
    return E.tm_mul(Dh, Y)


def fop(G, B, ST, L, t, kind='T'):
    """float operator at t: kind 'T' (E~, E~), 'X1' (XE~, E~), 'X3' (E~, XE~), 'X13' (XE~, XE~)"""
    Ef = [poly(A, t) for A in B['E']]
    Xf = [poly(A, t) for A in B['XE']] if kind != 'T' else None
    ka = Xf if kind in ('X1', 'X13') else Ef
    kb = Xf if kind in ('X3', 'X13') else Ef
    return (G, ka, kb, poly(ST['Dh'], t) * ST['mask'], L)


def parity(A):
    return float(np.sum(A * np.transpose(A, (1, 0, 2))) / np.sum(A * A))


def nodes_eig(G, B, ST, L, h, K, nmode, out):
    """float eigsh (top nmode + 2) of T^ at K+1 Chebyshev nodes; degree-K fits x_j(t), mu_j(t) of the top nmode pairs (any polynomials are
    admissible: the TM residuals decide). Returns nodes, eigenvalues, node vectors, x coefficient arrays (dense), mu coefficients, ops."""
    t1 = time.process_time()
    tn = [h * math.cos((2 * i + 1) * math.pi / (2 * (K + 1))) for i in range(K + 1)]
    n = L + 1
    shp, size = (n, n, n), n ** 3
    v0 = (poly(ST['Dh'], 0.0) * ST['mask']).ravel()
    vals, vecs, ops, prev = [], [], [], None
    ke = nmode + 2
    for t in tn:
        op = fop(G, B, ST, L, t)
        A = LinearOperator((size, size), matvec=lambda x, op=op: f_T(op, x.reshape(shp)).ravel(), dtype=np.float64)
        w, V = eigsh(A, k=ke, which='LA', v0=v0, tol=1e-12, ncv=max(32, 3 * ke))
        o = np.argsort(w)[::-1]
        w, V = w[o], V[:, o]
        for j in range(ke):
            ref = prev[:, j] if prev is not None else (np.ones(size) if j == 0 else V[:, j])
            if float(np.dot(V[:, j], ref)) < 0:
                V[:, j] = -V[:, j]
        prev = V
        vals.append(w)
        vecs.append(V[:, :nmode].copy())
        ops.append(op)
        v0 = V[:, 0].copy()
        out('NODE t=%+.6f lam1=%.12e lam_s/lam1 s=2..%d: %s parity %s (%.1f s)' % (t, w[0], ke, ' '.join('%.7f' % (x / w[0]) for x in w[1:]),
            ' '.join('%+.0f' % parity(V[:, j].reshape(shp)) for j in range(ke)), time.process_time() - t1))
        guard('eigsh')
    Vi = np.linalg.inv(np.array([[t ** d for d in range(K + 1)] for t in tn]))
    xs = [[sum(Vi[d, i] * vecs[i][:, j] for i in range(K + 1)).reshape(shp) * ST['mask'] for d in range(K + 1)] for j in range(nmode)]
    mus = [[float(sum(Vi[d, i] * vals[i][j] for i in range(K + 1))) for d in range(K + 1)] for j in range(nmode)]
    pars = [parity(vecs[0][:, j].reshape(shp)) for j in range(nmode)]
    return tn, vals, vecs, xs, mus, ops, pars


def residual(OP, x, mu, h, K):
    """TMs X = x(t) (exact degree-K polynomial), TX = T^(t) X, r = TX - mu(t) X"""
    X = TM([MR(c) for c in x], np.zeros_like(x[0]), h, K)
    TX = op_apply(OP, X)
    MU = TM([MR(np.float64(c)) for c in mu], np.float64(0.0), h, K)
    return X, TX, E.tm_add(TX, E.tm_mul(MU, X), -1.0)


def gram(X, Y):
    """arb coefficients (degrees 0..kx+ky) of <P_X(t), P_Y(t)> for the polynomial parts (MR coefficients) of two TMs"""
    P = [arb(0) for _ in range(X.k + Y.k + 1)]
    for d, x in enumerate(X.c):
        for e, y in enumerate(Y.c):
            nn = x.m.size
            g = gam(nn + 2)
            v = float(np.sum(x.m * y.m))
            r = g * float(np.sum(np.abs(x.m * y.m))) + float(np.sum(np.abs(x.m) * y.r + x.r * (np.abs(y.m) + y.r)))
            P[d + e] = P[d + e] + arb(v) + arb(0, float(up(r * (1.0 + 4 * g) + nn * ETA)))
    return P


def vdata(X, r, mu, mask, h, nsub):
    """eigenvector data (cs31): Gram polynomial P = |P_X|^2, Rn >= |remainder of X|, nlo <= inf |X(t)|, rb >= sup |r(t)|, eps = rb/nlo"""
    P = gram(X, X)
    Rn = vec_norm_ub(X.R * mask)
    n2 = min(E.fdn_arb(E.ev(P, arb(0), tb)) for tb in E.subballs(h, nsub))
    nlo = float(dn(dn(math.sqrt(n2)) - Rn)) if n2 > 0 else 0.0
    rb = tm_norm_ub(r, mask)
    eps = float(up(rb / nlo * (1.0 + 2 * U))) if nlo > 0 else float('inf')
    return dict(X=X, P=P, Rn=Rn, nlo=nlo, rb=rb, eps=eps, mu=[arb(c) for c in mu])


def traces(G, B, ST, L, h, K):
    """scalar TMs of tr T^ and tr T^ rho (R5 (iii), (iv)): sum_(l1,l3) sum_j D sum_m Q_mj^2 w_m with w_m = E~_m(l1,l1) E~_m(l3,l3), resp.
    E~_m(l1,l3)^2"""
    n = L + 1
    cm = [np.zeros((n, n, n)) for _ in range(K + 1)]
    cr = [np.zeros((n, n, n)) for _ in range(K + 1)]
    R = np.zeros((n, n, n))
    for m in range(n):
        A = B['E'][m]
        for d in range(K + 1):
            cm[d][m:, m:, m] = A.c[d].m
            cr[d][m:, m:, m] = A.c[d].r
        R[m:, m:, m] = A.R
    Ecube = TM([MR(cm[d], cr[d]) for d in range(K + 1)], R, h, K)       # Ecube[l1, l3, m] = E~_m(l1, l3)
    D, out = ST['D'], [None, None]
    for (s, i1, i3, Qm, Qr) in G:
        ed1 = TM([MR(c.m[i1, i1, :s], c.r[i1, i1, :s]) for c in Ecube.c], Ecube.R[i1, i1, :s], h, K)
        ed3 = TM([MR(c.m[i3, i3, :s], c.r[i3, i3, :s]) for c in Ecube.c], Ecube.R[i3, i3, :s], h, K)
        eo = TM([MR(c.m[i1, i3, :s], c.r[i1, i3, :s]) for c in Ecube.c], Ecube.R[i1, i3, :s], h, K)
        qlo, qhi = np.maximum(dn(np.abs(Qm) - Qr[:, None, :]), 0.0), up(np.abs(Qm) + Qr[:, None, :])
        lo2, hi2 = dn(qlo * qlo), up(qhi * qhi)
        q2m = 0.5 * lo2 + 0.5 * hi2
        q2r = up(np.maximum(up(hi2 - q2m), up(q2m - lo2)))
        g = gam(s + 2)
        Dg = TM([MR(c.m[i1, i3, :s], c.r[i1, i3, :s]) for c in D.c], D.R[i1, i3, :s], h, K)
        for w_i, P in enumerate((E.tm_mul(ed1, ed3), E.tm_mul(eo, eo))):
            cs = []
            for c in P.c:
                mm = np.einsum('pij,pi->pj', q2m, c.m)
                rr = np.einsum('pij,pi->pj', q2m, c.r + g * np.abs(c.m)) + np.einsum('pij,pi->pj', q2r, np.abs(c.m) + c.r)
                cs.append(MR(mm, up(rr * (1.0 + 4 * g) + s * ETA)))
            Hd = TM(cs, up(np.einsum('pij,pi->pj', up(q2m + q2r), P.R) * (1.0 + 4 * g) + s * ETA), h, K)
            term = tm_sum(E.tm_mul(Dg, Hd))
            out[w_i] = term if out[w_i] is None else E.tm_add(out[w_i], term)
    return out[0], out[1]


class FV:
    """family vector (R9): v(t) = sum_d c_d t^d + r(t), c_d exact float arrays on the valid states, sup_{|t|<=h} |r(t)|_2 <= rho"""
    __slots__ = ('c', 'rho', 'h')

    def __init__(self, c, rho, h):
        self.c, self.rho, self.h = c, float(rho), h

    def pnorm(self):
        """>= sup_t |sum_d c_d t^d|_2"""
        acc, hp = 0.0, 1.0
        for x in self.c:
            acc = float(up(acc + vec_norm_ub(np.abs(x)) * hp))
            hp = float(up(hp * self.h))
        return float(up(acc * (1.0 + 4 * U)))

    def norm(self):
        return float(up(self.pnorm() + self.rho))


def fv_from_tm(T, L):
    """exact centres kept, coefficient radii and the remainder folded into a 2-norm"""
    rad, hp = np.zeros_like(T.R), 1.0
    for d in range(T.k + 1):
        rad = up(rad + T.c[d].r * hp)
        hp = up(hp * T.h)
    rad = up((rad + T.R) * (1.0 + 4 * U))
    return FV([to_compact(c.m).copy() for c in T.c], vec_norm_ub(to_compact(rad)), T.h)


def fv_tm(v, L, k):
    """dense TM of the polynomial part (remainder 0), degree k >= len(v.c) - 1"""
    cs = [MR(to_dense(x, L)) for x in v.c]
    z = np.zeros_like(cs[0].m)
    while len(cs) < k + 1:
        cs.append(MR(z.copy()))
    return TM(cs, z.copy(), v.h, k)


def fv_trunc(v, k):
    """drop the coefficients above k into rho"""
    if len(v.c) <= k + 1:
        return v
    extra, hp = 0.0, _hp(v.h, k + 1)
    for x in v.c[k + 1:]:
        extra = float(up(extra + vec_norm_ub(np.abs(x)) * hp))
        hp = float(up(hp * v.h))
    return FV(v.c[:k + 1], up(v.rho + extra), v.h)


def fv_apply(OP, v, opnorm, L, k):
    """the operator OP (TM inputs of degree k) applied: rho' = (folded TM error) + opnorm rho"""
    w = fv_from_tm(op_apply(OP, fv_tm(v, L, k)), L)
    w.rho = float(up(w.rho + opnorm * v.rho * (1.0 + 2 * U)))
    return w


def fv_diag(gT, v, gmax, L, k):
    """a diagonal TM multiplier gT (dense, degree k, entrywise |g| <= gmax) applied"""
    w = fv_from_tm(E.tm_mul(gT, fv_tm(v, L, k)), L)
    w.rho = float(up(w.rho + gmax * v.rho * (1.0 + 2 * U)))
    return w


def fv_comb(a, v, b, w):
    """a v + b w for exact floats a, b (rounding folded into rho)"""
    k = max(len(v.c), len(w.c))
    z = np.zeros_like(v.c[0])
    cs, rad, hp = [], 0.0, 1.0
    for d in range(k):
        x = v.c[d] if d < len(v.c) else z
        y = w.c[d] if d < len(w.c) else z
        mm = E.mr_add(E.mr_scale(MR(x), a), E.mr_scale(MR(y), b))
        cs.append(mm.m)
        rad = float(up(rad + vec_norm_ub(mm.r) * hp))
        hp = float(up(hp * v.h))
    return FV(cs, up(abs(a) * v.rho + abs(b) * w.rho + rad), v.h)


def fv_inner(v, w):
    """(arb coefficients of <P_v(t), P_w(t)>, error radius) with <v, w> in sum_d P_d t^d + [-e, e] for every |t| <= h"""
    P = [arb(0) for _ in range(len(v.c) + len(w.c) - 1)]
    for d, x in enumerate(v.c):
        for e, y in enumerate(w.c):
            g = gam(x.size + 2)
            P[d + e] = P[d + e] + arb(float(np.dot(x, y))) + arb(0, float(up(g * float(np.dot(np.abs(x), np.abs(y))) * (1.0 + 4 * g) + ETA)))
    nv, nw = v.pnorm(), w.pnorm()
    return P, float(up(nv * w.rho + v.rho * nw + v.rho * w.rho))
