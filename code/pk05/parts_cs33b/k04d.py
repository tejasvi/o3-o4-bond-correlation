

class GIPS(IPS):
    """IPS whose coefficient inner products come from one chunked Gram product M M^T over the listed names (BLAS, any summation order;
    v1_1), other pairs from per-pair dots: |fl(<x, y>) - <x, y>| <= gam(n + 2) sum |x_i y_i| + (n + 2) ETA <= gam(n + 2) |x|_2 |y|_2
    + (n + 2) ETA (n states; Cauchy-Schwarz). pnorm and norm are cached per name."""

    def __init__(self, fvs, slack, names, chunk=32768):
        IPS.__init__(self, fvs, slack)
        self.pn, self.nm, self.nub = {}, {}, {}
        names = [a for a in dict.fromkeys(names) if a in fvs]
        rows = [(a, d) for a in names for d in range(len(fvs[a].c))]
        self.row = {r: i for i, r in enumerate(rows)}
        n = fvs[names[0]].c[0].size
        G = np.zeros((len(rows), len(rows)))
        M = np.empty((len(rows), chunk))
        for s in range(0, n, chunk):
            w = min(chunk, n - s)
            for i, (a, d) in enumerate(rows):
                M[i, :w] = fvs[a].c[d][s:s + w]
            Mw = M[:, :w]
            G += Mw @ Mw.T
            C.guard('gram')
        self.G, self.nst, self.nfall = G, n, 0
        self.gn = gam(n + 2)
        self.en = float(up((n + 2) * ETA))

    def cnorm(self, a, d):
        """>= |c_d|_2 of the named vector"""
        if (a, d) not in self.nub:
            self.nub[(a, d)] = C.vec_norm_ub(np.abs(self.fvs[a].c[d]))
        return self.nub[(a, d)]

    def pnorm(self, a):
        if a not in self.pn:
            self.pn[a] = self.fvs[a].pnorm()
        return self.pn[a]

    def norm(self, a):
        if a not in self.nm:
            self.nm[a] = float(up(up(self.pnorm(a) + self.fvs[a].rho) * (1.0 + 4 * U)))
        return self.nm[a]

    def poly(self, a, b):
        key = (a, b) if a <= b else (b, a)
        if key not in self.cache:
            v, w = self.fvs[key[0]], self.fvs[key[1]]
            gram = (key[0], 0) in self.row and (key[1], 0) in self.row
            self.nfall += 0 if gram else 1
            P = [arb(0) for _ in range(len(v.c) + len(w.c) - 1)]
            for d in range(len(v.c)):
                for e in range(len(w.c)):
                    g = self.G[self.row[(key[0], d)], self.row[(key[1], e)]] if gram else np.dot(v.c[d], w.c[e])
                    rad = float(up(up(self.gn * self.cnorm(key[0], d) * self.cnorm(key[1], e)) * (1.0 + 4 * self.gn) + self.en))
                    P[d + e] = P[d + e] + arb(float(g)) + arb(0, rad)
            pv, pw = self.pnorm(key[0]), self.pnorm(key[1])
            err = float(up((pv * w.rho + v.rho * pw + v.rho * w.rho) * (1.0 + 8 * U)))
            err = float(up((err + self.slack * self.norm(key[0]) * self.norm(key[1])) * (1.0 + 8 * U)))
            self.cache[key] = (P, err)
        return self.cache[key]
