

def family_common(SP, F, A, out):
    """both parts: the modes, the bulk seeds (u1, T~ u1, projected y_e; scaled by p(t) like the family) and the vertical mode products
    XU_e_a = T~_X u_a (unscaled; Delta bounds)"""
    t1 = time.process_time()
    step, gT, gmax, al = A['step'], A['gT'], A['gmax'], A['al']
    L = SP['L']
    for a, m in enumerate(SP['modes']):
        F['U%d' % a] = m['u']
    u1 = C.fv_trunc(SP['modes'][0]['u'], K_F)
    F['u1'] = u1
    F['Tu1'] = step('T', u1)
    for e in TYPES:
        if e in HORIZ:
            y = C.fv_comb(1.0, C.fv_diag(gT[e], u1, gmax[e], L, K_F), -al[e], u1)
        else:
            y = C.fv_comb(1.0, step(e, u1), -al[e], F['Tu1'])
        c = float(np.dot(u1.c[0], y.c[0]) / np.dot(u1.c[0], u1.c[0]))
        F['Y_' + e] = C.fv_comb(1.0, y, -c, u1)
        C.guard('Y')
    for e in VERT:
        for a in range(NCERT):
            F['XU_%s_%d' % (e, a)] = C.fv_apply(A['OP'][e], C.fv_trunc(SP['modes'][a]['u'], K_F), A['nu1up'], L, K_F)
        C.guard('XU')
    out('FAMILY common: %d vectors (%.1f s)' % (len(F), time.process_time() - t1))
    return F


def family_part(SP, F, A, part, out):
    """part B: depth-1 propagation of the centred insertions (P_e_p) and of the bulk seeds (TY_e) for every type (Bh: horizontal types,
    Bv: vertical types); part A needs no further vectors (v1_2: no same-column images)"""
    t1 = time.process_time()
    step = A['step']
    if 'B' in part:
        for e in (HORIZ if part == 'Bh' else (VERT if part == 'Bv' else TYPES)):
            for p in range(PE[e]):
                F['P_%s_%d' % (e, p)] = step('T', F['I_%s_%d' % (e, p)])
            F['TY_' + e] = step('T', F['Y_' + e])
            C.guard('P')
    out('FAMILY part %s: %d vectors, max rho/norm %.2e (%.1f s)' % (part, len(F), max(v.rho / max(v.norm(), 1e-300) for v in F.values()),
        time.process_time() - t1))
    return F
