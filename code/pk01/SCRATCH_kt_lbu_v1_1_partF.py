
# ---------------------------------------------------------------- v2 and cert
def run_v2():
    n = 3
    e, f = EDGES['b0'], EDGES['sN']
    for K in (3, 4):
        t0 = cpu()
        bd = Build(G9, n, K, e, [f], JGRID[0], KAPPA, RHO2, 'O4 N=4 K=%d' % K)
        for sigma in SIGMAS:
            bd.add_sigma(sigma)
        best = certify(bd, 1, SIGMAS, JGRID, 'O4 N=4 K=%d' % K)
        if best is None:
            out('R-J1 O4 N=4 K=%d: none on the grid' % K)
        else:
            out('R-J1 O4 N=4 K=%d: J1 %d, sigma %s, L %s; E %s; theta %s' % (K, best['J1'], best['sigma'], f6(best['L']),
                {F: f6(best['Eu'][F]) for F in FNAMES}, best['ths']))
        out('CPU O4 N=4 K=%d: %.2f s; peak RSS %.0f MB' % (K, cpu() - t0, rss_mb()))
        del bd


def run_cert():
    K = KCERT
    orbs = [o for o in ORBITS if SET == 'all' or o[0] == 'O4']
    fpairs = [EDGES[o[2]] for o in orbs]
    res = {}
    for n in (2, 3):
        t0 = cpu()
        bd = Build(G9, n, K, EDGES['b0'], fpairs, JGRID[0], KAPPA, RHO2, 'cert %s N=%d K=%d' % (SET, n + 1, K))
        for sigma in SIGMAS:
            bd.add_sigma(sigma)
        for b, (nm, e, f, d2, _) in enumerate(orbs, start=1):
            best = certify(bd, b, SIGMAS, JGRID, '%s N=%d K=%d' % (nm, n + 1, K))
            res[(nm, n + 1)] = best
            if best is None:
                out('R-J1 %s N=%d K=%d: none on the grid' % (nm, n + 1, K))
                continue
            out('R-J1 %s N=%d K=%d: J1 %d, sigma %s, L %s (c2 %s); E %s; theta %s' % (nm, n + 1, K, best['J1'], best['sigma'],
                f6(best['L']), f6(fmpq(n, 8) * d2), {F: f6(best['Eu'][F]) for F in FNAMES}, best['ths']))
            if nm == 'O3':
                Acoef = {F: bd.a[(F, 0) if F in ('1', 'e') else (F, b)] for F in FNAMES}
                cs = cov_series(Acoef['1'], Acoef['e'], Acoef['f'], Acoef['ef'], K)
                for J in (100, 150, 200):
                    if J < best['J1']:
                        continue
                    t = fmpq(1, J)
                    Lj, mono, nneg = phi_scan(Acoef, best['Eu'], t, ncell=1)
                    cen = sum((cs[k] * t ** k for k in range(K + 1)), fmpq(0))
                    data = CDATA[(n + 1, J)] * J * J
                    ok = float(Lj) <= data * (1 + 1e-5) and (J != 200 or abs(float(cen) - data) <= 1e-3 * data)
                    check('C-DATA O3 N=%d J=%d' % (n + 1, J), ok, 'certified %s <= data %.6e; central %s' % (f6(Lj), data, f6(cen)))
        out('CPU cert N=%d: %.2f s; peak RSS %.0f MB' % (n + 1, cpu() - t0, rss_mb()))
        del bd
    js = [v['J1'] for v in res.values() if v is not None]
    allc = all(v is not None for v in res.values())
    out('READINGS R-J1: ' + '; '.join('%s N=%d %s' % (k[0], k[1], v['J1'] if v else 'none') for k, v in sorted(res.items())))
    out('READINGS LB_u J1 (SET %s) = %s (all certified on the grid: %s)' % (SET, max(js) if js and allc else 'none', allc))


# ---------------------------------------------------------------- main
def main():
    out('kt_lbu_v1_1 mode %s LIM %d K %d SET %s | python %s | python-flint %s | prec %d' % (MODE, LIM, KCERT, SET,
        sys.version.split()[0], flint.__version__, FLINT.prec))
    status = 'DONE'
    try:
        if MODE == 'v1':
            run_v1()
        elif MODE == 'v2':
            run_v2()
        else:
            run_cert()
    except GuardStop as ex:
        status = 'INCOMPLETE (guard stop at %s)' % ex
    allc = all(CHECKS.values()) if CHECKS else False
    allp = all(PLANTS.values()) if PLANTS else (MODE != 'v1')
    out('CHECKS %s' % CHECKS)
    out('PLANTS %s' % PLANTS)
    if status != 'DONE':
        verdict = 'INCOMPLETE'
    else:
        verdict = 'VALID' if allc and allp else 'INVALID'
    out('SUMMARY mode %s: status %s; checks %d/%d; plants %d/%d; VERDICT %s; cpu %.2f s; wall %.2f s; peak RSS %.0f MB' % (
        MODE, status, sum(CHECKS.values()), len(CHECKS), sum(PLANTS.values()), len(PLANTS), verdict, cpu(), time.time() - T_START,
        rss_mb()))


T_START = time.time()
main()
