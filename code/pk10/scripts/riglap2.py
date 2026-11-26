#!/usr/bin/env python3
# pk10 (code): rigorous Laplace bounds for small-graph O(4) integrals with insertions (floating point; s19.1).
#   I(J) = int prod_v dsigma_v F(sigma) exp(J sum_e c_e (sigma_u.sigma_v - 1)),  normalized measures, F = product of insertion factors.
#   Centre-of-mass gauge (all vertices); scaled chart phi = sqrt(J) pi; Gaussian gamma with covariance L^+ (x) I_3 on {sum phi = 0}.
#   I/main = E_gamma[F e^H 1_chart] + far/main,  H = sum_v meas_v + FP + sum_e anh_e  (meas >= 0, FP <= 0, anh <= 0).
#   Result: I/main = sum_{k<=K} a_k t^k + R,  |R| <= B_rem + B_tail + B_ann + B_far  (t = 1/J), where
#     B_rem  = t^{K+1}/(K+1)! N_c E_c[Dbar_{K+1}]            (integral-form Taylor remainder on Omega; Dbar positive majorant)
#     B_tail = sum_{k<=K} t^k ||(F e^H)_k||_2 P(Omega^c)^{1/2}  (Gaussian tail of the explicit polynomial)
#     B_ann  = N_a ||F||_{2,a} P_a(Omega^c)^{1/2}              (annulus rho_v < |pi_v| <= rho', true integrand <= |F| e^{meas})
#     B_far  = sup|F| sum_v e^{-th J rho'^2/(2 L+_vv)} Z((1-th)J)/main  (some |pi_v| > rho' or lower hemisphere; tree bound for Z)
#   Omega = {|pi_v|^2 = t X_v <= a_v}.  Tilts: e^{meas(t)} <= exp(sum_v c_v t X_v), c_v = -log(1-a_v)/(2 a_v) on Omega.
import math, itertools
import numpy as np
from scipy.special import ive, erfc
from pseries import Series, padd, pscale, pmul, pconst, pvar, w_coeffs
from npoly import NPoly
from amom2b import AllMom2


def chi_tail(s, n):
    if n == 2:
        return math.exp(-s / 2)
    return erfc(math.sqrt(s / 2)) + math.sqrt(2 * s / math.pi) * math.exp(-s / 2)


class Graph:
    def __init__(self, V, edges, pairs, N=4):
        """edges: dict (u, v) -> c; pairs: list of vertex pairs (u, v) whose edge forms Q_uv = |phi_u - phi_v|^2 are used by insertions."""
        self.V, self.edges, self.pairs = V, dict(edges), list(pairs)
        self.N, self.n = N, N - 1
        self.F = V + len(pairs)
        L = np.zeros((V, V))
        for (u, v), c in edges.items():
            L[u, u] += c; L[v, v] += c; L[u, v] -= c; L[v, u] -= c
        self.L = L
        ev, evec = np.linalg.eigh(L)
        self.Qb = evec[:, 1:]
        self.Lsub = self.Qb.T @ L @ self.Qb
        self.G = self.Qb @ np.linalg.inv(self.Lsub) @ self.Qb.T
        self.W = np.zeros((V, self.F))
        self.W[:, :V] = np.eye(V)
        for i, (u, v) in enumerate(pairs):
            self.W[u, V + i] = 1.0; self.W[v, V + i] = -1.0
        self.groups = [0] * V + [1] * len(pairs)

    def qidx(self, u, v):
        for i, p in enumerate(self.pairs):
            if p == (u, v) or p == (v, u):
                return self.V + i
        raise KeyError((u, v))

    def logmain(self, J):
        V = self.V
        area = 2 * math.pi ** 2 if self.N == 4 else 4 * math.pi
        return (-(V - 1) * math.log(area) + 0.5 * self.n * (V - 1) * math.log(2 * math.pi / J)
                - 0.5 * self.n * math.log(np.linalg.det(self.Lsub) / V))

    def tilted(self, rates):
        """covariance and normalization of gamma tilted by exp(sum_v rates_v X_v) (X = |phi|^2, 3 components)."""
        Lt = self.Qb.T @ (self.L - 2 * np.diag(rates)) @ self.Qb
        ev = np.linalg.eigvalsh(Lt)
        if ev.min() <= 0:
            return None, float("inf")
        return self.Qb @ np.linalg.inv(Lt) @ self.Qb.T, (np.linalg.det(self.Lsub) / np.linalg.det(Lt)) ** (0.5 * self.n)


class Model:
    """series of H and of the insertion product F, exact coefficients and positive derivative majorants."""
    def __init__(self, g, K, factors):
        """factors: list of ('dot', u, v, c) [sigma_u.sigma_v - c] or ('p', (r1, r2, r3), q1, q2, q3) [trial polynomial of the column
        with vertices r1 (T), r2 (M), r3 (B): 1 + t q1(xi) + t^2 q2(xi) + t^3 q3(xi), xi = (xi_TM, xi_MB, xi_TB)] or ('const', c)."""
        self.g, self.K, self.factors = g, K, factors
        self.NV = g.F
        self.w = w_coeffs(K + 2)

    def S(self, coeffs, K=None):
        return Series(self.K if K is None else K, self.NV, coeffs)

    def xv(self, i, k=1, c=1.0):
        e = [0] * self.NV; e[i] = k
        return {tuple(e): c}

    def anh(self, iu, iv, c, K):
        out = [{} for _ in range(K + 1)]
        d2 = padd(self.xv(iu, 2), pscale(pmul(self.xv(iu), self.xv(iv)), -2.0), self.xv(iv, 2))
        for (i, j), cw in self.w.items():
            k = 1 + i + j
            if k > K:
                continue
            mono = {tuple((i if q == iu else 0) + (j if q == iv else 0) for q in range(self.NV)): 1.0}
            out[k] = padd(out[k], pscale(pmul(d2, mono), -0.5 * c * cw))
        return Series(K, self.NV, out)

    def xi(self, u, v, K):
        base = Series(K, self.NV, [self.xv(self.g.qidx(u, v), 1, 0.5)] + [{} for _ in range(K)])
        return base - self.anh(u, v, 1.0, K)

    def H(self, K):
        V = self.g.V
        Hs = Series(K, self.NV)
        for v in range(V):
            Hs = Hs + Series(K, self.NV, [{}] + [self.xv(v, k, 1.0 / (2 * k)) for k in range(1, K + 1)])
        # FP = 3 log(1 - y), y = (1/V) sum_v (1 - sqrt(1 - t X_v))
        b = [0.0] + [math.comb(2 * k, k) / (4 ** k * (2 * k - 1)) for k in range(1, K + 1)]
        y = Series(K, self.NV)
        for v in range(V):
            y = y + Series(K, self.NV, [{}] + [self.xv(v, k, b[k] / V) for k in range(1, K + 1)])
        y_m = y
        FP = Series(K, self.NV)
        for m in range(1, K + 1):
            FP = FP + y_m.scale(-float(self.g.n) / m)
            y_m = y_m * y
        Hs = Hs + FP
        for (u, v), c in self.g.edges.items():
            Hs = Hs + self.anh(u, v, c, K)
        return Hs

    def Fser(self, K):
        Fs = Series(K, self.NV, [pconst(1.0, self.NV)] + [{} for _ in range(K)])
        for f in self.factors:
            if f[0] == 'const':
                Fs = Fs.scale(f[1])
            elif f[0] == 'dot':
                _, u, v, c = f
                x = self.xi(u, v, K)
                fs = Series(K, self.NV, [pconst(1.0 - c, self.NV)] + [{} for _ in range(K)]) - Series(K, self.NV, [{}] + x.c[:K])
                Fs = Fs * fs
            elif f[0] == 'p':
                _, col, q1, q2, q3 = f
                T, M, B = col
                xs = [self.xi(T, M, K), self.xi(M, B, K), self.xi(T, B, K)]
                BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]
                P = Series(K, self.NV, [pconst(1.0, self.NV)] + [{} for _ in range(K)])
                for coef, sh in ((q1, 1), (q2, 2), (q3, 3)):
                    for cb, mono in zip(coef, BASIS):
                        if cb == 0.0 or sh > K:
                            continue
                        fbs = Series(K, self.NV, [pconst(1.0, self.NV)] + [{} for _ in range(K)])
                        for p_ in mono:
                            fbs = fbs * xs[p_]
                        P = P + Series(K, self.NV, [{} for _ in range(sh)] + [pscale(c_, cb) for c_ in fbs.c[:K + 1 - sh]])
                Fs = Fs * P
        return Fs

    def exact(self):
        """coefficients (F e^H)_k, k = 0..K, as dict polynomials."""
        H = self.H(self.K)
        return (self.Fser(self.K) * H.exp()).c


BASIS9 = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]


class Majorants:
    """positive NPoly majorants (as functions of X >= 0, Q >= 0) of sup_{tau <= t} |H^(k)(tau)| and |F^(j)(tau)| on Omega(a_v)."""
    def __init__(self, model, avec, t, B=None):
        self.m, self.g, self.a, self.t = model, model.g, list(avec), t
        self.NV = model.NV
        self.B = B if B is not None else 2 * (model.K + 2) + 8
        self.ONE = NPoly(self.NV, self.B, np.zeros(1, dtype=np.int64), np.ones(1))

    def mono(self, e, c=1.0):
        return NPoly(self.NV, self.B, np.array([int(sum(int(x) * self.B ** i for i, x in enumerate(e)))], dtype=np.int64), np.array([c]))

    def xv(self, i, k=1, c=1.0):
        e = [0] * self.NV; e[i] = k
        return self.mono(e, c)

    def D2(self, i, j):
        return self.xv(i, 2).add(self.xv(i, 1).mul(self.xv(j, 1)).scale(-2.0)).add(self.xv(j, 2))

    def Mk(self, i, j, k):
        return self.ONE if k == 0 else self.xv(i, k).add(self.xv(j, k))

    @staticmethod
    def partial_bell(k, m, xs, ONE, ZERO):
        """B_{k,m}(xs[1], xs[2], ...) with NPoly arguments (positive), by B_{k,m} = sum_i C(k-1, i-1) x_i B_{k-i, m-1}."""
        memo = {}
        def rec(kk, mm):
            if (kk, mm) in memo:
                return memo[(kk, mm)]
            if kk == 0 and mm == 0:
                r = ONE
            elif kk == 0 or mm == 0:
                r = ZERO
            else:
                r = ZERO
                for i in range(1, kk - mm + 2):
                    r = r.add(xs[i].mul(rec(kk - i, mm - 1)).scale(float(math.comb(kk - 1, i - 1))))
            memo[(kk, mm)] = r
            return r
        return rec(k, m)

    def hbar(self, k):
        V, a = self.g.V, self.a
        ZERO = NPoly(self.NV, self.B)
        out = ZERO
        for v in range(V):
            out = out.add(self.xv(v, k, math.factorial(k - 1) / (2 * (1 - a[v]) ** k)))
        for (u, v), c in self.g.edges.items():
            ae = max(a[u], a[v])
            out = out.add(self.D2(u, v).mul(self.Mk(u, v, k - 1)).scale((c / 2.0) * math.factorial(k) / (4 * (1 - ae) ** (k + 1))))
        # Faddeev-Popov: 3 sum_m (m-1)! (1 - ybar)^{-m} B_{k,m}(ybar_1, ...), ybar_j = (1/V) sum_v c_j X_v^j (1 - a_v)^{1/2 - j}
        ymax = sum(a[v] / (2 - a[v]) for v in range(V)) / V
        def cj(j):
            df = 1
            for q in range(2 * j - 3, 0, -2):
                df *= q
            return df / 2 ** j
        ys = [None] + [ZERO.add(ZERO)]
        ys = [None]
        for j in range(1, k + 1):
            yj = ZERO
            for v in range(V):
                yj = yj.add(self.xv(v, j, cj(j) * (1 - a[v]) ** (0.5 - j) / V))
            ys.append(yj)
        fp = ZERO
        for mm in range(1, k + 1):
            fp = fp.add(self.partial_bell(k, mm, ys, self.ONE, ZERO).scale(float(self.g.n) * math.factorial(mm - 1) / (1 - ymax) ** mm))
        return out.add(fp)

    def xibar(self, u, v, l, aa):
        """majorant of xi_uv^(l)(tau), tau <= t (xi = Q/2 + (1/2) D W(tau))."""
        D = self.D2(u, v)
        if l == 0:
            return self.xv(self.g.qidx(u, v), 1, 0.5).add(D.scale(self.t / (8 * (1 - aa))))
        return D.mul(self.Mk(u, v, l - 1)).scale(math.factorial(l) / (8 * (1 - aa) ** (l + 1)))

    def factor_bar(self, f, j):
        a, t = self.a, self.t
        if f[0] == 'const':
            return self.ONE.scale(abs(f[1])) if j == 0 else NPoly(self.NV, self.B)
        if f[0] == 'dot':
            _, u, v, c = f
            aa = max(a[u], a[v])
            if j == 0:
                return self.ONE.scale(abs(1 - c)).add(self.xibar(u, v, 0, aa).scale(t))
            return self.xibar(u, v, j - 1, aa).scale(float(j)).add(self.xibar(u, v, j, aa).scale(t))
        if f[0] == 'p':
            _, col, q1, q2, q3 = f
            T, M, Bv = col
            prs = [(T, M), (M, Bv), (T, Bv)]
            def fbd(mono, n):
                if len(mono) == 1:
                    u, v = prs[mono[0]]
                    return self.xibar(u, v, n, max(a[u], a[v]))
                (u1, v1), (u2, v2) = prs[mono[0]], prs[mono[1]]
                out = NPoly(self.NV, self.B)
                for l in range(n + 1):
                    out = out.add(self.xibar(u1, v1, l, max(a[u1], a[v1])).mul(self.xibar(u2, v2, n - l, max(a[u2], a[v2]))).scale(float(math.comb(n, l))))
                return out
            out = self.ONE if j == 0 else NPoly(self.NV, self.B)
            for i, coef in ((1, q1), (2, q2), (3, q3)):
                for cb, mono in zip(coef, BASIS9):
                    if cb == 0.0:
                        continue
                    for l in range(0, min(i, j) + 1):
                        cf = math.comb(j, l) * (math.factorial(i) / math.factorial(i - l)) * t ** (i - l) * abs(cb)
                        out = out.add(fbd(mono, j - l).scale(cf))
            return out
        raise ValueError(f)

    def Fbar(self, j):
        """Leibniz over the factors."""
        facs = self.m.factors
        if not facs:
            return self.ONE if j == 0 else NPoly(self.NV, self.B)
        cache = {}
        def fb(i, jj):
            if (i, jj) not in cache:
                cache[(i, jj)] = self.factor_bar(facs[i], jj)
            return cache[(i, jj)]
        out = NPoly(self.NV, self.B)
        for js in itertools.product(range(j + 1), repeat=len(facs)):
            if sum(js) != j:
                continue
            term = self.ONE.scale(float(math.factorial(j)) / math.prod(math.factorial(x) for x in js))
            for i, ji in enumerate(js):
                term = term.mul(fb(i, ji))
            out = out.add(term)
        return out

    def Dbar(self, n):
        h = {k: self.hbar(k) for k in range(1, n + 1)}
        Y = [self.ONE]
        for mm in range(n):
            acc = NPoly(self.NV, self.B)
            for i in range(mm + 1):
                acc = acc.add(h[i + 1].mul(Y[mm - i]).scale(float(math.comb(mm, i))))
            Y.append(acc)
        out = NPoly(self.NV, self.B)
        for j in range(n + 1):
            out = out.add(self.Fbar(j).mul(Y[n - j]).scale(float(math.comb(n, j))))
        return out


def expect_np(am, p):
    """E[P] for an NPoly in the forms of am (recoded)."""
    if len(p.codes) == 0:
        return 0.0
    ex = np.stack([(p.codes // p.pw[i]) % p.B for i in range(p.nv)], axis=1)
    deg = ex.sum(axis=1)
    assert deg.max() <= am.D, (deg.max(), am.D)
    cs = ex @ am.pw
    return float(sum(np.dot(p.coeffs[deg == d], am.mom[d][am.index(int(d), cs[deg == d])]) for d in np.unique(deg)))


def tree_couplings(g):
    par = list(range(g.V))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    tree = []
    for (u, v), c in sorted(g.edges.items(), key=lambda kv: -kv[1]):
        ru, rv = find(u), find(v)
        if ru != rv:
            par[ru] = rv; tree.append(c)
    return tree


def sup_F(factors, J):
    s = 1.0
    t = 1.0 / J
    for f in factors:
        if f[0] == 'const':
            s *= abs(f[1])
        elif f[0] == 'dot':
            s *= 1.0 + abs(f[3])
        elif f[0] == 'p':
            _, col, q1, q2, q3 = f
            val = 1.0
            for i, coef in ((1, q1), (2, q2), (3, q3)):
                for cb, mono in zip(coef, BASIS9):
                    val += t ** i * abs(cb) * (2.0 * J) ** len(mono)
            s *= val
    return s


def bound(g, factors, K, J, rho, rho_p, verbose=False):
    """rigorous bound for I(J)/main(J) = sum_{k<=K} a_k t^k + R.  rho: list of near-region radii per vertex; rho_p: outer radius."""
    t = 1.0 / J
    V = g.V
    m = Model(g, K, factors)
    coef = m.exact()
    qcap = max([sum(e[V:]) for P in coef for e in P] + [0])
    degs = [max([sum(e) for e in P] + [0]) for P in coef]
    a_v = [r * r for r in rho]
    ap = rho_p * rho_p
    # untilted engine for a_k and tails
    D0 = max(2 * max(degs), 2)
    am0 = AllMom2(g.G, g.n, D0, W=g.W, groups=g.groups, caps={1: 2 * qcap})
    ak = [am0.E(P) if P else 0.0 for P in coef]
    norms = [math.sqrt(max(am0.E2(P, P), 0.0)) if P else 0.0 for P in coef]
    Pout = sum(chi_tail(J * a_v[v] / g.G[v, v], g.n) for v in range(V))
    B_tail = sum(t ** k * norms[k] for k in range(K + 1)) * math.sqrt(Pout)
    # remainder majorant
    mj = Majorants(m, a_v, t)
    Db = mj.Dbar(K + 1)
    dD = int(Db.degrees().max())
    qD = int(np.stack([(Db.codes // Db.pw[i]) % Db.B for i in range(Db.nv)], axis=1)[:, V:].sum(axis=1).max()) if g.F > V else 0
    rates = np.array([-math.log(1 - a_v[v]) / (2 * a_v[v]) * t for v in range(V)])
    Gc, Nc = g.tilted(rates)
    amc = AllMom2(Gc, g.n, dD, W=g.W, groups=g.groups, caps={1: max(qD, 1)})
    ED = expect_np(amc, Db)
    B_rem = t ** (K + 1) / math.factorial(K + 1) * Nc * ED
    # annulus: |F| e^{meas} with meas <= c' t X (radius rho_p)
    mjp = Majorants(m, [ap] * V, t)
    F0 = mjp.Fbar(0)
    ratesp = np.array([-math.log(1 - ap) / (2 * ap) * t] * V)
    Gp_, Np_ = g.tilted(ratesp)
    dF = int(F0.degrees().max()) if len(F0.codes) else 0
    qF = int(np.stack([(F0.codes // F0.pw[i]) % F0.B for i in range(F0.nv)], axis=1)[:, V:].sum(axis=1).max()) if g.F > V and len(F0.codes) else 0
    amp = AllMom2(Gp_, g.n, max(2 * dF, 2), W=g.W, groups=g.groups, caps={1: max(2 * qF, 1)})
    F0d = F0.to_dict()
    nF0 = math.sqrt(max(amp.E2(F0d, F0d), 0.0))
    Pout_p = sum(chi_tail(J * a_v[v] / Gp_[v, v], g.n) for v in range(V))
    B_ann = Np_ * nF0 * math.sqrt(Pout_p)
    # far
    Lp = np.diag(g.G)
    tree = tree_couplings(g)
    if g.N == 4:
        logtree = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        logtree = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    best = min(math.log(sum(math.exp(-th * J * ap / (2 * Lp[v])) for v in range(V))) + logtree((1 - th) * J) - g.logmain(J)
               for th in np.linspace(0.01, 0.99, 197))
    B_far = sup_F(factors, J) * math.exp(best)
    if verbose:
        print("  degrees %s, qcap %d, Dbar deg %d (Q %d), N_c %.4f, E_c[Dbar] %.4e, P(out) %.2e" % (degs, qcap, dD, qD, Nc, ED, Pout))
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}
