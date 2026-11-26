

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
