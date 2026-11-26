

def plants(N, b0, h, SP, SBs, pack, part, out):
    """the plants of the first interval of a job for its part (each must FIRE); P-NEAR negates a pair with n = 4 (p + q + k = 2)"""
    F, A, ips, obs, NS = pack
    G, B, ST, L = SP['G'], SP['B'], SP['ST'], SP['L']
    tb0 = E.subballs(h, NSUB)[0]
    tc = C.trunc_consts(N, b0, h, L)
    fired = {'P6': E.plant_P6(out)}
    fired['P-CAS'] = float(np.max(C.cert_block(N, 12, 9, plant=True)[1])) > QGATE
    u0, t0 = SP['modes'][0]['u'], SP['tn'][0]
    TX = C.op_apply((G, B['E'], B['ET'], ST['Dh'], L), C.fv_tm(u0, L, K_S))
    op = C.fop(G, B, ST, L, t0)
    Ef = [x * (1.0 + 1e-6) for x in op[1]]                     # v1_3: every E~_m scaled (fires at every J)
    xt = C.to_dense(sum(c_ * t0 ** d for d, c_ in enumerate(u0.c)), L)
    f = C.f_T((op[0], Ef, op[2], op[3], op[4]), xt)
    c, rr = C.tm_at(TX, t0)
    exc = float(np.max((np.abs(c - f) - rr) * ST['mask'])) / float(np.max(np.abs(f)))
    fired['P-NODE'] = exc > NODEGATE
    del TX
    if 'A' in part:
        A['ext'] = vec_plant_ext(ips, SP, SBs, A)
        fired['P-VEC'] = bool(checks_all(ips, SP, A, SBs, obs, NS, h, 'A', sub=[0])['fails'])
        del A['ext']
        fired['P-FAR'] = bool(checks_all(ips, SP, A, SBs, obs, NS, h, 'A', far_neg=('mh', None), sub=[0])['fails'])
    if 'B' in part:
        bp = part if part in ('Bh', 'Bv') else 'B'
        cfg = ('tv', 1, 'bv', 1, 0) if bp == 'Bv' else ('th', 1, 'mh', 1, 0)
        fired['P-NEAR'] = bool(checks_all(ips, SP, A, SBs, obs, NS, h, bp, near_neg=cfg, sub=[0])['fails'])
    fired['P-TR'] = not sb_spectral(SP, tb0, tc[0], drop=1)['ok']
    fired['P-DELTA'] = bool(checks_all(ips, SP, A, SBs, obs, NS, h, part, dscale=1e8, sub=[0])['fails'])
    fired['P-L'] = not sb_spectral(SP, tb0, C.trunc_consts(N, b0, h, max(4, L // 4))[0])['ok']
    out('PLANTS N=%d b0=%r part %s: %s (P-NODE excess %.2e)' % (N, b0, part, ' '.join('%s:%s' % (k, 'FIRED' if v else 'DID-NOT-FIRE')
        for k, v in fired.items()), exc))
    return fired
