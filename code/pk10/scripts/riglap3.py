#!/usr/bin/env python3
# pk10 (code): Lemma 19.1 bounds (riglap2) extended by a general column-polynomial insertion factor
#   ('xi', (T, M, B), c0, c9):  F = c0 + sum_beta c9[beta] xi^beta,  beta over BASIS9 (xi_TM, xi_MB, xi_TB, squares, products),
# with no explicit t-powers (so its tau-derivatives act on xi(tau) only), plus the RV12_3 L1 fix (+inf when a tilt does not exist).
# Majorant of the j-th tau-derivative: |c0| [j = 0] + sum_beta |c9[beta]| fbd(beta, j) (xi-bar majorants of riglap2).  sup|F| <= |c0| + sum |c9| (2J)^deg.
import math, itertools
import numpy as np
from scipy.special import ive
import riglap2 as _r
from riglap2 import Graph, expect_np, tree_couplings, chi_tail, BASIS9
from pseries import Series, pconst, pscale
from npoly import NPoly
from amom2b import AllMom2


class Model3(_r.Model):
    def Fser(self, K):
        base = [f for f in self.factors if f[0] != 'xi']
        saved = self.factors
        self.factors = base
        Fs = _r.Model.Fser(self, K)
        self.factors = saved
        for f in saved:
            if f[0] != 'xi':
                continue
            _, col, c0, c9 = f
            T, M, B = col
            prs = [(T, M), (M, B), (T, B)]
            need = sorted({p_ for cb, mono in zip(c9, BASIS9) if cb != 0.0 for p_ in mono})
            xs = {p_: self.xi(prs[p_][0], prs[p_][1], K) for p_ in need}   # only the pair series actually used
            P = Series(K, self.NV, [pconst(c0, self.NV)] + [{} for _ in range(K)])
            for cb, mono in zip(c9, BASIS9):
                if cb == 0.0:
                    continue
                fbs = Series(K, self.NV, [pconst(1.0, self.NV)] + [{} for _ in range(K)])
                for p_ in mono:
                    fbs = fbs * xs[p_]
                P = P + fbs.scale(cb)
            Fs = Fs * P
        return Fs


class Majorants3(_r.Majorants):
    def factor_bar(self, f, j):
        if f[0] != 'xi':
            return _r.Majorants.factor_bar(self, f, j)
        a = self.a
        _, col, c0, c9 = f
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
        out = self.ONE.scale(abs(c0)) if j == 0 else NPoly(self.NV, self.B)
        for cb, mono in zip(c9, BASIS9):
            if cb != 0.0:
                out = out.add(fbd(mono, j).scale(abs(cb)))
        return out


def sup_F3(factors, J):
    s = _r.sup_F([f for f in factors if f[0] != 'xi'], J)
    for f in factors:
        if f[0] == 'xi':
            _, col, c0, c9 = f
            s *= abs(c0) + sum(abs(cb) * (2.0 * J) ** len(mono) for cb, mono in zip(c9, BASIS9))
    return s


def bound(g, factors, K, J, rho, rho_p, verbose=False, exact_only=False):
    """as riglap2.bound, with 'xi' factors; +inf remainders when a tilt does not exist (RV12_3 L1)."""
    t = 1.0 / J
    V = g.V
    m = Model3(g, K, factors)
    coef = m.exact()
    qcap = max([sum(e[V:]) for P in coef for e in P] + [0])
    degs = [max([sum(e) for e in P] + [0]) for P in coef]
    a_v = [r * r for r in rho] if rho is not None else None
    ap = rho_p * rho_p if rho_p is not None else None
    D0 = max(degs) if exact_only else max(2 * max(degs), 2)
    am0 = AllMom2(g.G, g.n, D0, W=g.W, groups=g.groups, caps={1: 2 * qcap})
    ak = [am0.E(P) if P else 0.0 for P in coef]
    inf = float("inf")
    if exact_only:
        return ak, {}
    rates = np.array([-math.log(1 - a_v[v]) / (2 * a_v[v]) * t for v in range(V)])
    ratesp = np.array([-math.log(1 - ap) / (2 * ap) * t] * V)
    Gc, Nc = g.tilted(rates)
    Gp_, Np_ = g.tilted(ratesp)
    if Gc is None or Gp_ is None:
        return ak, {"rem": inf, "tail": inf, "ann": inf, "far": inf}
    norms = [math.sqrt(max(am0.E2(P, P), 0.0)) if P else 0.0 for P in coef]
    Pout = sum(chi_tail(J * a_v[v] / g.G[v, v], g.n) for v in range(V))
    B_tail = sum(t ** k * norms[k] for k in range(K + 1)) * math.sqrt(Pout)
    mj = Majorants3(m, a_v, t)
    Db = mj.Dbar(K + 1)
    dD = int(Db.degrees().max())
    qD = int(np.stack([(Db.codes // Db.pw[i]) % Db.B for i in range(Db.nv)], axis=1)[:, V:].sum(axis=1).max()) if g.F > V else 0
    amc = AllMom2(Gc, g.n, dD, W=g.W, groups=g.groups, caps={1: max(qD, 1)})
    ED = expect_np(amc, Db)
    B_rem = t ** (K + 1) / math.factorial(K + 1) * Nc * ED
    mjp = Majorants3(m, [ap] * V, t)
    F0 = mjp.Fbar(0)
    dF = int(F0.degrees().max()) if len(F0.codes) else 0
    qF = int(np.stack([(F0.codes // F0.pw[i]) % F0.B for i in range(F0.nv)], axis=1)[:, V:].sum(axis=1).max()) if g.F > V and len(F0.codes) else 0
    amp = AllMom2(Gp_, g.n, max(2 * dF, 2), W=g.W, groups=g.groups, caps={1: max(2 * qF, 1)})
    F0d = F0.to_dict()
    nF0 = math.sqrt(max(amp.E2(F0d, F0d), 0.0))
    Pout_p = sum(chi_tail(J * a_v[v] / Gp_[v, v], g.n) for v in range(V))
    B_ann = Np_ * nF0 * math.sqrt(Pout_p)
    Lp = np.diag(g.G)
    tree = tree_couplings(g)
    if g.N == 4:
        logtree = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        logtree = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    best = min(math.log(sum(math.exp(-th * J * ap / (2 * Lp[v])) for v in range(V))) + logtree((1 - th) * J) - g.logmain(J)
               for th in np.linspace(0.01, 0.99, 197))
    B_far = sup_F3(factors, J) * math.exp(best)
    if verbose:
        print("  degrees %s, qcap %d, Dbar deg %d (Q %d), N_c %.4f, E_c[Dbar] %.4e, P(out) %.2e" % (degs, qcap, dD, qD, Nc, ED, Pout))
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}
