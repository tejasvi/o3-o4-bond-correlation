

def wvec(colA, colB, G, Dh1, L, h):
    """end vector H^1/2 (A (x) B) 1 in sector 0: hub entries [l1, l3, 0] = colA[l1] colB[l3], then Q^T and D^1/2 (R4 (ii), (OB))"""
    n = L + 1
    A = E.tm_mul(TM([MR(c.m.reshape(n, 1), c.r.reshape(n, 1)) for c in colA.c], colA.R.reshape(n, 1), h, K_F),
                 TM([MR(c.m.reshape(1, n), c.r.reshape(1, n)) for c in colB.c], colB.R.reshape(1, n), h, K_F))
    cm, cr = [], []
    for c in A.c:
        zm, zr = np.zeros((n, n, n)), np.zeros((n, n, n))
        zm[:, :, 0], zr[:, :, 0] = c.m, c.r
        cm.append(zm)
        cr.append(zr)
    R = np.zeros((n, n, n))
    R[:, :, 0] = A.R
    Y = C.tm_blk(G, TM([MR(cm[d], cr[d]) for d in range(K_F + 1)], R, h, K_F), False)
    return C.fv_from_tm(E.tm_mul(Dh1, Y), L)


def col0(A, h):
    return TM([MR(c.m[:, 0].copy(), c.r[:, 0].copy()) for c in A.c], A.R[:, 0].copy(), h, A.k)


def centring(SP, gT):
    """centring constants (any constants are admissible): bulk means of the five insertions from the node-0 top eigenvector (floats)"""
    G, B, ST, L, h = SP['G'], SP['B'], SP['ST'], SP['L'], SP['h']
    n = L + 1
    t0 = SP['tn'][0]
    x1 = SP['vec0'][:, 0].reshape((n, n, n))
    nx = float(np.sum(x1 * x1))
    al = {e: float(np.sum(x1 * x1 * C.poly(gT[e], t0)) / nx) for e in HORIZ}
    l1 = SP['vals'][0][0]
    for e, kind in (('tv', 'X1'), ('bv', 'X3')):
        al[e] = float(np.sum(x1 * C.f_T(C.fop(G, B, ST, L, t0, kind), x1)) / (l1 * nx))
    return al


def family_base(SP, nu1up, out):
    """operators of degree K_F, the end vectors, J(0..P_MAX), centred insertions I'(e, p) for p < PE[e]. (NORM): every propagation step is
    multiplied by the positive scalar polynomial p(t) ~ 1/mu_0(t) (scal_poly; the caller checks inf p > 0)"""
    t1 = time.process_time()
    G, B, ST, L, h = SP['G'], SP['B'], SP['ST'], SP['L'], SP['h']
    tr1 = lambda A: C.tm_trunc(A, K_F)
    E1, ET1, XE1, XET1 = [tr1(A) for A in B['E']], [tr1(A) for A in B['ET']], [tr1(A) for A in B['XE']], [tr1(A) for A in B['XET']]
    Dh1 = tr1(ST['Dh'])
    OP = {'T': (G, E1, ET1, Dh1, L), 'tv': (G, XE1, ET1, Dh1, L), 'bv': (G, E1, XET1, Dh1, L), 'tb': (G, XE1, XET1, Dh1, L)}
    gT = {e: tr1(ST['g'][e]) for e in HORIZ}
    gmax = {e: float(np.max(up(gT[e].absP() + gT[e].R) * ST['mask'])) for e in HORIZ}
    pc, pmax, plo = scal_poly(SP['modes'][0]['mud'], h)
    al = centring(SP, gT)
    cE, cX = col0(E1[0], h), col0(XE1[0], h)
    F = {'J0': wvec(cE, cE, G, Dh1, L, h), 'W_tv': wvec(cX, cE, G, Dh1, L, h), 'W_bv': wvec(cE, cX, G, Dh1, L, h),
         'W_tb': wvec(cX, cX, G, Dh1, L, h)}
    step = lambda key, v: fv_pmul(C.fv_apply(OP[key], v, nu1up, L, K_F), pc, pmax, K_F)
    for p in range(P_MAX):
        F['J%d' % (p + 1)] = step('T', F['J%d' % p])
        C.guard('J')
    for e in TYPES:
        for p in range(PE[e]):
            J = F['J%d' % p]
            if e in HORIZ:
                I = C.fv_diag(gT[e], J, gmax[e], L, K_F)
            else:
                I = F['W_' + e] if p == 0 else step(e, F['J%d' % (p - 1)])
            F['I_%s_%d' % (e, p)] = C.fv_comb(1.0, I, -al[e], J)
        C.guard('I')
    out('FAMILY base: p(t) coefficients %s (sup %.6e, inf >= %.6e), centring %s, |J_p| %s (%.1f s)' % (
        ' '.join('%.6e' % c_ for c_ in pc), pmax, plo, ' '.join('%s %.9f' % (e, al[e]) for e in TYPES),
        ' '.join('%.3e' % F['J%d' % p].norm() for p in range(P_MAX + 1)), time.process_time() - t1))
    return F, dict(OP=OP, gT=gT, gmax=gmax, pc=pc, pmax=pmax, plo=plo, nu1up=nu1up, al=al, step=step)
