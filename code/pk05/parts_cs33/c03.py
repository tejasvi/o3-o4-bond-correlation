

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
