

def c_probe(N, SP, out):
    """C-PROBE: cs30 (sha-checked) at beta = b0 + t_0, same L: lam_s/lam1 (s = 2..4) to 1e-8 and c_mh/c_th to 1e-4 against node 0 (T~ frame);
    cs30 reads sys.argv[1] as its CAP_S at import, so argv is set for the import only"""
    saved = sys.argv
    sys.argv = [saved[0], repr(CAP_S)]
    try:
        P = C.load(PROBE, PSHA, 'cs30_mod')
    finally:
        sys.argv = saved
    L, t0 = SP['L'], SP['tn'][0]
    r = P.analyze(N, SP['b0'] + t0, L)
    n = L + 1
    x1, x2 = (SP['vec0'][:, j].reshape((n, n, n)) for j in (0, 1))
    rm = float(np.sum(x2 * C.poly(SP['ST']['g']['mh'], t0) * x1)) / float(np.sum(x2 * C.poly(SP['ST']['g']['th'], t0) * x1))
    v0 = SP['vals'][0]
    d1 = max(abs(r['lam'][s] - v0[s] / v0[0]) / (v0[s] / v0[0]) for s in (1, 2, 3))
    d2 = abs(r['rmt'] - rm) / abs(rm)
    ok = d1 <= 1e-8 and d2 <= 1e-4
    out('C-PROBE N=%d beta=%r L=%d: lam_s/lam1 rel %.2e (gate 1e-8); c_mh/c_th cs30 %.10e here %.10e rel %.2e (gate 1e-4): %s' % (
        N, SP['b0'] + t0, L, d1, r['rmt'], rm, d2, 'PASS' if ok else 'FAIL'))
    return ok
