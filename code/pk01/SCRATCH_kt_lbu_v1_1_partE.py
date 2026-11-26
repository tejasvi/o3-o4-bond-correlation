
def run_v1():
    rng = random.Random(20261102)
    # C-SER
    wd = w_exact(8)
    rows = all(sum((c for (i, j), c in wd.items() if i + j == m), fmpq(0)) == fmpq(1, 4) for m in range(9))
    sym = all(wd.get((j, i), fmpq(0)) == c for (i, j), c in wd.items())
    check('C-SER', rows and sym, 'w row sums 1/4 to degree 8: %s; symmetric: %s' % (rows, sym))
    # C-GRAPH
    g = G9
    want = [fmpq(13, 36), fmpq(13, 24)] * 4 + [fmpq(2, 9)]
    okL = all(g.Lpd[v] == want[v] for v in range(9))
    foster = sum((g.R(*EDGES[x]) for x in ELIST), fmpq(0))
    okD = True
    for (nm, e, f, d2, _) in ORBITS:
        dd = delta_of(g, EDGES[e], EDGES[f])
        okD = okD and dd * dd == d2
        out('ORBIT %s (%s, %s): Delta %s, Delta^2 %s (table %s)' % (nm, e, f, dd, dd * dd, d2))
    check('C-GRAPH', okL and g.tau == 192 and foster == 8 and okD,
          'L+ diag %s; tau %s; Foster %s; Delta^2 match %s' % (okL, g.tau, foster, okD))
    # C-TREE (+ PLANT-FP): P3, K = 5
    gt = Graph(3, [(0, 1), (1, 2)])
    KT = 5
    for n in (2, 3):
        exp_ = tree_expect(n, KT)
        for fpc, isplant in ((n, False), (n + 1, True)):
            Rt = PR(3, 1)
            wdt = w_exact(KT + 1)
            H = H_series(Rt, gt, n, KT, wdt, fpc=fpc)
            E = sexp(Rt, H, KT)
            xe = xi_series(Rt, wdt, 0, 1, (1, 0), KT)
            xf = xi_series(Rt, wdt, 1, 2, (0, 1), KT)
            one = szero(KT)
            one[0] = {(0, 0): Rt.one}
            T0 = Moments(Rt, gt, gt.Lp, fmpq(1), n, evec_of(3, (0, 1)), [evec_of(3, (1, 2))], {0: 2 * KT, 1: 2 * KT, 2: 2 * KT},
                         'tree N=%d fpc=%d' % (n + 1, fpc))
            got = {'1': [T0.E(p) for p in smul(Rt, one, E, KT)], 'e': [T0.E(p) for p in smul(Rt, xe, E, KT)],
                   'ef': [T0.E(p) for p in smul(Rt, smul(Rt, xe, xf, KT), E, KT)]}
            okT = all(got[F] == exp_[F] for F in got)
            if isplant:
                plant('PLANT-FP N=%d' % (n + 1), not okT, 'FP coefficient n + 1 breaks the exact tree series')
            else:
                check('C-TREE N=%d' % (n + 1), okT, ' | '.join('%s: %s' % (F, [str(x) for x in got[F]]) for F in got))
    # the untilted P3 x P3 tables at K = 4, both N, partners PARTNERS_V1: C-EXACT (+ PLANT-MOM), C-GAUSS, C-ROW0, C-ECON, C-R1,
    # R-SERIES; C-SYM (+ PLANT-SYM) at K = 2
    K = 4
    fpairs = [EDGES[x] for x in PARTNERS_V1]
    series = {}
    for n in (2, 3):
        guard('v1 main N=%d' % (n + 1))
        bd = Build(G9, n, K, EDGES['b0'], fpairs, JGRID[0], KAPPA, RHO2, 'P3xP3 N=%d' % (n + 1), need_tilts=False)
        bad, done = c_exact(bd.T0, 9, rng, 40, 6)
        check('C-EXACT N=%d T0' % (n + 1), bad == 0 and done > 0, '%d of %d monomials match the alpha-permanent' % (done - bad, done))
        wx = aperm(bd.T0.Gl, [0, 0], fmpq(n, 2)) * 4
        hx = bd.T0.mom[(0, 0)][2][tuple([2] + [0] * 8)]
        check('C-EXACT N=%d X0^2' % (n + 1), hx == wx, 'E[X_0^2] %s, 4 per_{n/2} %s' % (hx, wx))
        plant('PLANT-MOM N=%d' % (n + 1), hx + fmpq(1, 10 ** 20) != wx, 'E[X_0^2] + 1e-20 against the same alpha-permanent')
        A1, Ae = bd.a[('1', 0)], bd.a[('e', 0)]
        cs_of = {}
        for b, x in enumerate(PARTNERS_V1, start=1):
            cs_of[x] = cov_series(A1, Ae, bd.a[('f', b)], bd.a[('ef', b)], K)
        for b, (nm, e, f, d2, _) in enumerate(ORBITS, start=1):
            Af, Aef = bd.a[('f', b)], bd.a[('ef', b)]
            cs = cs_of[f]
            series[(nm, n + 1)] = cs
            okG = (A1[0] == 1 and Ae[0] == fmpq(n, 2) * G9.R(*EDGES[e]) and Af[0] == fmpq(n, 2) * G9.R(*EDGES[f])
                   and cs[0] == fmpq(n, 8) * d2)
            check('C-GAUSS %s N=%d' % (nm, n + 1), okG, 'c2 = %s = (N-1) Delta^2 / 8: %s' % (cs[0], cs[0] == fmpq(n, 8) * d2))
            r0 = ROW0[nm][n - 2]
            okR = (Aef[0] == r0[0] and cs[0] == r0[1] and cs[1] == r0[2])
            check('C-ROW0 %s N=%d' % (nm, n + 1), okR, 'A_ef(0) %s (reference %s), c2 %s (%s), c3 %s (%s)' % (
                Aef[0], r0[0], cs[0], r0[1], cs[1], r0[2]))
            out('R-SERIES %s N=%d: c2 %s (%s), c3 %s (%s), c4 %s (%s); a_k(1) %s' % (nm, n + 1, cs[0], f6(cs[0]), cs[1], f6(cs[1]),
                cs[2], f6(cs[2]), [f6(x) for x in A1]))
        for nm, x in (('M1', 'b3'), ('M2', 'b5')):
            cs = cs_of[x]
            series[(nm, n + 1)] = cs
            out('R-SERIES %s N=%d: c2 %s (%s), c3 %s (%s), c4 %s (%s)' % (nm, n + 1, cs[0], f6(cs[0]), cs[1], f6(cs[1]), cs[2], f6(cs[2])))
        okA = (A1[1] == A1ROW0[n] and Ae[0] == fmpq(17 * n, 48)
               and all(bd.a[('f', b)][0] == (fmpq(17 * n, 48) if x[0] == 'b' else fmpq(7 * n, 24)) for b, x in enumerate(PARTNERS_V1, start=1)))
        check('C-ROW0 N=%d a_1, A_b(0), A_s(0)' % (n + 1), okA, 'a_1(F = 1) %s (reference %s); A_b0(0) %s (17n/48 = %s); spokes 7n/24' % (
            A1[1], A1ROW0[n], Ae[0], fmpq(17 * n, 48)))
        rims = [b for b, x in enumerate(PARTNERS_V1, start=1) if x[0] == 'b']
        spk = [b for b, x in enumerate(PARTNERS_V1, start=1) if x[0] == 's']
        okE = all(bd.a[('f', b)] == Ae for b in rims) and all(bd.a[('f', b)] == bd.a[('f', spk[0])] for b in spk)
        check('C-ECON N=%d' % (n + 1), okE, 'a_k (k <= %d) of xi_x equal for b0 and %s, and for %s' % (
            K, [PARTNERS_V1[b - 1] for b in rims], [PARTNERS_V1[b - 1] for b in spk]))
        b1se = Build(G9, n, K, EDGES['b1'], [EDGES['sE']], JGRID[0], KAPPA, RHO2, 'R1 (b1, sE) N=%d' % (n + 1), need_tilts=False)
        cs13 = cov_series(b1se.a[('1', 0)], b1se.a[('e', 0)], b1se.a[('f', 1)], b1se.a[('ef', 1)], K)
        r1s = (cs_of['sN'] == cs_of['sW'], cs_of['b2'] == cs_of['b3'], cs_of['b4'] == cs_of['b5'], cs_of['sE'] == cs13)
        check('C-R1 N=%d' % (n + 1), all(r1s), 'O4 = O5 %s; O1 = M1 %s; O2 = M2 %s; O3 = (b1, sE) %s (series to order %d)' % (r1s + (K,)))
        for b, (nm, e, f, d2, (e2, f2)) in enumerate(ORBITS, start=1):
            bs = Build(G9, n, 2, EDGES[e2], [EDGES[f2]], JGRID[0], KAPPA, RHO2, 'sym %s (%s, %s) N=%d' % (nm, e2, f2, n + 1),
                       need_tilts=False)
            okS = all(bs.a[(F, 0 if F in ('1', 'e') else 1)][k] == bd.a[(F, 0 if F in ('1', 'e') else b)][k] for F in FNAMES for k in range(3))
            check('C-SYM %s N=%d' % (nm, n + 1), okS, 'second member (%s, %s): a_k (k <= 2) equal' % (e2, f2))
        okP = all(bd.a[('ef', 2)][k] == bd.a[('ef', 1)][k] for k in range(3))
        plant('PLANT-SYM N=%d' % (n + 1), not okP, 'O2 against O1 (different orbits) differ')
        del bd, b1se
    # C-H (+ PLANT-H, PLANT-H-ANN) for the tilts of v2/cert
    okc = G9.tilt([C35 / JGRID[0]] * 9)[2]
    okl = all(G9.tilt([KAPPA / (2 * G9.Lpd[v]) if u == v else fmpq(0) for u in range(9)])[2] for v in range(9))
    cpr = q_ceil(up_q(-(arb(1 - RHO2).log()) / (2 * arb(RHO2))), 64)
    oka = all(ann_rates(G9, cpr / JGRID[0], v)[0] is not None for v in range(9))
    check('C-H P3xP3', okc and okl and oka, 'T1 %s, T2 %s, T3 %s' % (okc, okl, oka))
    plant('PLANT-H', not G9.tilt([1 / G9.Lpd[1] if u == 1 else fmpq(0) for u in range(9)])[2], 'kappa = 2 violates (H)')
    plant('PLANT-H-ANN', not G9.tilt([cpr / JGRID[0] + (1 / G9.Lpd[1] if u == 1 else 0) for u in range(9)])[2],
          'annulus tilt with kappa_a = 2 at v1 violates (H)')
    # C-LIT
    c_lit()
    # C-BOUND on P3 (+ PLANT-BOUND)
    c_bound()
    # PLANT-NEG
    t1 = fmpq(1, 100)
    c2 = fmpq(1, 1000)
    Asyn = {'1': [fmpq(1)], 'e': [fmpq(1)], 'f': [fmpq(1)], 'ef': [1 + c2, -8 * c2 / t1, 8 * c2 / (t1 * t1)]}
    L, mono, nneg = phi_scan(Asyn, {F: arb(0) for F in FNAMES}, t1)
    plant('PLANT-NEG', nneg > 0, 'planted dip: %d negative cells, min %s' % (nneg, f6(L)))
    out('READINGS R-SERIES: ' + '; '.join('%s N=%d c2 %s c3 %s c4 %s' % (k[0], k[1], f6(v[0]), f6(v[1]), f6(v[2]))
                                         for k, v in sorted(series.items())))

