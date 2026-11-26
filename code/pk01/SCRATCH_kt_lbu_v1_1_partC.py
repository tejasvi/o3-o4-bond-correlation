
# ---------------------------------------------------------------- the J1-independent part for one graph, N, K and partner list
FNAMES = ('1', 'e', 'f', 'ef')
DF = {'1': 0, 'e': 1, 'f': 1, 'ef': 2}


class Build:
    def __init__(s, g, n, K, epair, fpairs, Jmin, kappa, rho2, label, need_tilts=True):
        t0 = cpu()
        s.g, s.n, s.K, s.label, s.Jmin, s.kappa, s.rho2 = g, n, K, label, Jmin, kappa, rho2
        V = g.V
        nb = len(fpairs)
        R = PR(V, nb)
        s.R = R
        wd = w_exact(max(K, 1) + 1)
        H = H_series(R, g, n, K, wd)
        E = sexp(R, H, K)
        s.ep = (epair[0], epair[1], (1, 0))
        s.fps = [(f[0], f[1], (0, b + 1)) for b, f in enumerate(fpairs)]
        xe = xi_series(R, wd, epair[0], epair[1], (1, 0), K)
        xfs = [xi_series(R, wd, f[0], f[1], (0, b + 1), K) for b, f in enumerate(fpairs)]
        one = szero(K)
        one[0] = {(0, 0): R.one}
        s.PS = {('1', 0): smul(R, one, E, K), ('e', 0): smul(R, xe, E, K)}
        for b in range(1, nb + 1):
            s.PS[('f', b)] = smul(R, xfs[b - 1], E, K)
            s.PS[('ef', b)] = smul(R, smul(R, xe, xfs[b - 1], K), E, K)
        s.keys = list(s.PS.keys())
        out('SERIES %s: K %d, terms per key %s, cpu %.2f s' % (label, K, {k: [pnterms(p) for p in v] for k, v in s.PS.items() if k[1] <= 1},
                                                             cpu() - t0))
        s.evec = evec_of(V, epair)
        s.fvecs = [evec_of(V, f) for f in fpairs]
        guard('T0 ' + label)
        s.T0 = Moments(R, g, g.Lp, fmpq(1), n, s.evec, s.fvecs, {0: 2 * K, 1: 2 * K, 2: 2 * K}, label + ' T0')
        out('RSS %s T0: peak %.0f MB' % (label, rss_mb()))
        s.a = {key: [s.T0.E(s.PS[key][k]) for k in range(K + 1)] for key in s.keys}
        if not need_tilts:
            return
        rng = random.Random(7)
        # T1: the common B_rem tilt exp(C35 t_max sum X), valid for every radius (a_v <= 3/5) and every J1 >= Jmin
        s.tau_c = C35 / Jmin
        C1, r1, ok1 = g.tilt([s.tau_c] * V)
        check('C-H %s T1' % label, ok1, 'tilt %s' % s.tau_c)
        if not ok1:
            raise ValueError('T1 tilt violates (H)')
        guard('T1 ' + label)
        s.T1 = Moments(R, g, C1, r1, n, s.evec, s.fvecs, {0: 2 * K + 6, 1: 2 * K + 4, 2: 2 * K + 2}, label + ' T1')
        out('RSS %s T1: peak %.0f MB' % (label, rss_mb()))
        bad, done = c_exact(s.T1, V, rng, 10, 6)
        check('C-EXACT %s T1' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
        s.Nc = s.T1.Narb()
        # T2_v: the Chernoff tilts lambda_v = kappa / (2 L+_vv); tail expectations of |(F e^H)_k|
        s.lam = [kappa / (2 * g.Lpd[v]) for v in range(V)]
        s.N2, s.TL = [], {key: [[None] * V for _ in range(K + 1)] for key in s.keys}
        pab = {key: [pabs(R, s.PS[key][k]) for k in range(K + 1)] for key in s.keys}
        for v in range(V):
            rates = [fmpq(0)] * V
            rates[v] = s.lam[v]
            C2, r2, ok2 = g.tilt(rates)
            check('C-H %s T2 v%d' % (label, v), ok2, 'lambda %s' % s.lam[v])
            if not ok2:
                raise ValueError('T2 tilt violates (H)')
            guard('T2 %s v%d' % (label, v))
            T2 = Moments(R, g, C2, r2, n, s.evec, s.fvecs, {0: 2 * K, 1: 2 * K, 2: 2 * K}, '%s T2 v%d' % (label, v))
            if v == 0:
                bad, done = c_exact(T2, V, rng, 10, 6)
                check('C-EXACT %s T2 v0' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
            s.N2.append(T2.Narb())
            for key in s.keys:
                for k in range(K + 1):
                    s.TL[key][k][v] = T2.E(pab[key][k])
            del T2
        out('RSS %s T2: peak %.0f MB' % (label, rss_mb()))
        # T3_v: the annulus tilts; expectations of the annulus majorant (t-polynomial parts)
        cp = -(arb(1 - rho2).log()) / (2 * arb(rho2))
        s.cprime = q_ceil(up_q(cp), 64)
        s.tau_a = s.cprime / Jmin
        s.N3, s.lam_a, s.AN = [], [], {key: [None] * V for key in s.keys}
        f0 = {}
        for key in s.keys:
            F, b = key
            f0[key] = F0p(R, F, s.ep, s.fps[b - 1] if b else None, rho2)
        for v in range(V):
            C3, r3, lam_a, ka = ann_rates(g, s.tau_a, v)
            check('C-H %s T3 v%d' % (label, v), C3 is not None, 'tilt %s + kappa_a %s' % (s.tau_a, ka))
            if C3 is None:
                raise ValueError('no annulus tilt satisfies (H)')
            guard('T3 %s v%d' % (label, v))
            T3 = Moments(R, g, C3, r3, n, s.evec, s.fvecs, {0: 4, 1: 2, 2: 0}, '%s T3 v%d' % (label, v))
            if v == 0:
                bad, done = c_exact(T3, V, rng, 10, 6)
                check('C-EXACT %s T3 v0' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
            s.N3.append(T3.Narb())
            s.lam_a.append(lam_a)
            for key in s.keys:
                s.AN[key][v] = [T3.E(part) for part in f0[key]]
            del T3
        s.sig = {}
        out('BUILD %s done, cpu %.2f s, peak RSS %.0f MB' % (label, cpu() - t0, rss_mb()))

    def add_sigma(s, sigma):
        """radii for sigma and the expectations E_T1[Dbar_{K+1}] (t-parts) per key."""
        t0 = cpu()
        g, R = s.g, s.R
        avec, rvec = radii(g, sigma)
        assert s.rho2 > max(avec)
        cmax = max(up_q(cslope(avec[v], rvec[v])) for v in range(g.V))
        assert cmax <= C35
        mj = Maj(R, g, s.n, avec, rvec, s.K)
        ED, nt = {}, {}
        for key in s.keys:
            guard('Dbar %s sigma %s %s' % (s.label, sigma, key))
            F, b = key
            parts = mj.Dbar(F, s.ep, s.fps[b - 1] if b else None)
            nt[key] = sum(pnterms(p) for p in parts)
            vals = [s.T1.E(p) for p in parts]
            for x in vals:
                assert x >= 0
            ED[key] = vals + [fmpq(0)] * (3 - len(vals))
        s.sig[sigma] = (avec, rvec, ED)
        out('SIGMA %s %s: radii %s, max slope %s, Dbar terms %s, cpu %.2f s, peak RSS %.0f MB' % (s.label, sigma, [f6(x) for x in avec],
            f6(cmax), {k: nt[k] for k in s.keys if k[1] <= 1}, cpu() - t0, rss_mb()))

    def errors(s, sigma, J1, key, drop_rem=False):
        """(B_rem, B_tail, B_ann, B_far) for key at J1 (arb upper bounds), radii of sigma."""
        avec, rvec, ED = s.sig[sigma]
        K, V, n = s.K, s.g.V, s.n
        t1 = fmpq(1, J1)
        assert t1 <= fmpq(1, s.Jmin)
        F = key[0]
        e = ED[key]
        brem = arb(0) if drop_rem else arb(t1 ** (K + 1) / FACT[K + 1]) * s.Nc * arb(e[0] + e[1] * t1 + e[2] * t1 * t1)
        ch = [(-(arb(s.lam[v] * J1 * avec[v]))).exp() for v in range(V)]
        cha = [(-(arb(s.lam_a[v] * J1 * avec[v]))).exp() for v in range(V)]
        btail = arb(0)
        for k in range(K + 1):
            for v in range(V):
                btail += arb(t1 ** k) * ch[v] * s.N2[v] * arb(s.TL[key][k][v])
        bann = arb(0)
        for v in range(V):
            val = fmpq(0)
            for i, x in enumerate(s.AN[key][v]):
                val += x * t1 ** i
            bann += cha[v] * s.N3[v] * arb(val)
        bfar, th = far_bound(s.g, n, J1, DF[F], s.rho2)
        return [arb(up_q(x)) for x in (brem, btail, bann, bfar)], th

