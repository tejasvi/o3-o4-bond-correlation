

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
