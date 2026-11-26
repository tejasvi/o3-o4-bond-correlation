

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
