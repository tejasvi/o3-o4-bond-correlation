

def spectral(N, b0, h, L, out):
    """Q, inputs, node eigenpairs, 8 mode fits with sector projection u_j = (x_j + sg rho x_j)/2, their TM residuals (KW), C-NODE, and
    the sector traces minus the exact mode polynomials (R5 (iii), (iv))"""
    t1 = time.process_time()
    G, qmax, nb = C.build_Q(N, L)
    out('Q N=%d L=%d: %d blocks, max Davis-Kahan radius %.3e (gate %.0e) (%.1f s)' % (N, L, nb, qmax, QGATE, time.process_time() - t1))
    B = C.build(N, b0, h, L, K_S, out)
    ST = C.states(B, L, h, K_S)
    C.STATE['idx'] = ST['idx']
    PERM[0] = make_perm(L)
    OPS = (G, B['E'], B['ET'], ST['Dh'], L)
    tn, vals, vecs, xs, mus, ops, pars = C.nodes_eig(G, B, ST, L, h, K_S, NMODE, out)
    vec0 = vecs[0]
    del vecs
    trT, trR = C.traces(G, B, ST, L, h, K_S)
    opn = E.fup_arb(E.ev(*E.tm_arb(trT), arb(0, h)))          # |T^| <= tr T^ (T^ >= 0)
    mask, cnode, modes = ST['mask'], -np.inf, []
    for j in range(NMODE):
        sg = 1.0 if pars[j] > 0 else -1.0
        X, TX, r = C.residual(OPS, xs[j], mus[j], h, K_S)
        for i, t in enumerate(tn):
            xt = sum(xs[j][d] * t ** d for d in range(K_S + 1))
            f = C.f_T(ops[i], xt)
            c, rr = C.tm_at(TX, t)
            cnode = max(cnode, float(np.max((np.abs(c - f) - rr) * mask)) / float(np.max(np.abs(f))))
        del TX
        u = fv_sector(FV([C.to_compact(x).copy() for x in xs[j]], 0.0, h), sg)
        P = C.fv_inner(u, u)
        n2 = min(E.fdn_arb(E.ev(P[0], arb(0, P[1]), tb)) for tb in E.subballs(h, NSUB))
        nlo = float(dn(math.sqrt(n2))) if n2 > 0 else 0.0
        mumax = float(up(sum(abs(c_) * h ** d for d, c_ in enumerate(mus[j])) * (1.0 + 1e-12)))
        rb = float(up(C.tm_norm_ub(r, mask) + (opn + mumax) * u.rho * (1.0 + 4 * U)))     # |P_sg r| <= |r|, plus u's rounding
        eps = float(up(rb / nlo * (1.0 + 2 * U))) if nlo > 0 else float('inf')
        modes.append(dict(u=u, sg=sg, par=pars[j], eps=eps, rb=rb, nlo=nlo, mu=[arb(c_) for c_ in mus[j]], mud=mus[j]))
        del X, r
        xs[j] = None
        C.guard('residual')
    del ops
    trs = {}
    for sg in (1.0, -1.0):
        D = E.tm_scale(E.tm_add(trT, trR, sg), 0.5)
        for m in modes:
            if m['sg'] == sg:
                D = E.tm_add(D, TM([MR(np.float64(c_)) for c_ in m['mud']], np.float64(0.0), h, K_S), -1.0)
        trs[sg] = E.tm_arb(D)
    out('SPECTRAL N=%d: eps/mu0 %s; parities %s; C-NODE excess %.2e; |T^| <= %.6e (%.1f s)' % (N, ' '.join(
        '%.1e' % (m['eps'] / m['mud'][0]) for m in modes), ' '.join('%+.9f' % m['par'] for m in modes), cnode, opn,
        time.process_time() - t1))
    return dict(N=N, G=G, qmax=qmax, B=B, ST=ST, tn=tn, vals=vals, vec0=vec0, modes=modes, trs=trs, cnode=cnode, opn=opn,
                L=L, h=h, b0=b0)
