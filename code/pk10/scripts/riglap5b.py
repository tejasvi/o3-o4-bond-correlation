#!/usr/bin/env python3
# pk10 (code): Lemma 19.1c bounds (riglap5) with the insertion-independent work cached per (graph, J): Prep5 holds the H-series, E_j,
# the X-only remainder norms, tilts, tails and the far factor; bound5b(prep, factors) adds the insertion parts.  Same inequalities as riglap5.
import math
import numpy as np
from scipy.special import ive
import riglap2 as _r
import riglap3 as _r3
from riglap2 import chi_tail, tree_couplings
from riglap4 import lp_norm, pos_norm, norm_any, group_factors, _deg
from riglap5 import hhat2
from pseries import padd, pscale, pmul
from amom2b import AllMom2
from npoly import NPoly

NPOLY_B = None   # base for the NPoly majorants (None: riglap2 default); set to 8 for graphs with many forms
_orig_mul = NPoly.mul


def _maxexp(p):
    return np.stack([(p.codes // p.pw[i]) % p.B for i in range(p.nv)], axis=1).max(axis=0)


def _guarded_mul(self, o, chunk=4000000):
    if len(self.codes) and len(o.codes):
        assert np.all(_maxexp(self) + _maxexp(o) < self.B), "NPoly exponent overflow"
    return _orig_mul(self, o, chunk)


NPoly.mul = _guarded_mul


class Prep5:
    def __init__(self, g, J, rho, rho_p, key="g", dmaxH=16, qcap=4, dexact=None):
        self.g, self.J, self.key = g, J, key
        t = self.t = 1.0 / J
        V, n = g.V, g.n
        self.a_v = a_v = [r * r for r in rho]; self.ap = ap = rho_p * rho_p
        rates = np.array([-math.log(1 - a_v[v]) / (2 * a_v[v]) * t for v in range(V)])
        ratesp = np.array([-math.log(1 - ap) / (2 * ap) * t] * V)
        self.Gc, self.Nc = g.tilted(rates)
        self.Gp, self.Np = g.tilted(ratesp)
        self.ok = self.Gc is not None and self.Gp is not None
        Hs = _r3.Model3(g, 3, []).H(3)
        H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
        H1sq = pmul(H1, H1)
        self.Ej = [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
        self.qcap = qcap
        self.dexact = dexact
        self.am0 = None
        if not self.ok:
            return
        mjH = _r.Majorants(_r.Model(g, 4, []), a_v, t, B=NPOLY_B)
        h2 = mjH.hbar(2).to_dict(); h3 = mjH.hbar(3).to_dict(); h4 = mjH.hbar(4).to_dict()
        hh = hhat2(g, a_v, t, h2)
        W = g.W
        kH, kc = key + "|H", key + "|c%.10g" % t
        N2 = lambda P: norm_any(P, g.G, n, W, 2, kH, dmaxH)
        self.nE = [1.0] + [N2(self.Ej[j]) for j in (1, 2, 3)]
        self.rE = (t ** 4 / 24 * N2(h4)
                   + 0.5 * (t ** 4 * N2(pmul(H2, H2)) + t ** 6 / 36 * N2(pmul(h3, h3)) + t ** 4 / 3 * N2(pmul(H1, h3)) + t ** 5 / 3 * N2(pmul(H2, h3)))
                   + (1.0 / 6) * (1.5 * t ** 4 * N2(pmul(H1sq, h2)) + 0.75 * t ** 5 * N2(pmul(H1, pmul(h2, h2))) + t ** 6 / 8 * N2(pmul(h2, pmul(h2, h2)))))
        self.nC8 = t * (norm_any(H1, self.Gc, n, W, 8, kc, dmaxH) + norm_any(hh, self.Gc, n, W, 8, kc, dmaxH))
        self.nE4 = [1.0]
        for j in (1, 2, 3):
            self.nE4.append(norm_any(self.Ej[j], g.G, n, W, 4, kH, dmaxH) if 4 * _deg(self.Ej[j]) <= dmaxH else 3.0 ** _deg(self.Ej[j]) * self.nE[j])
        self.Pout = sum(chi_tail(J * a_v[v] / g.G[v, v], n) for v in range(V))
        self.Pout_p = sum(chi_tail(J * a_v[v] / self.Gp[v, v], n) for v in range(V))
        Lp = np.diag(g.G)
        tree = tree_couplings(g)
        if g.N == 4:
            logtree = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
        else:
            logtree = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
        self.farbase = math.exp(min(math.log(sum(math.exp(-th * J * ap / (2 * Lp[v])) for v in range(V))) + logtree((1 - th) * J) - g.logmain(J)
                                    for th in np.linspace(0.01, 0.99, 197)))

    def engine(self, D):
        if self.am0 is None or self.am0.D < D:
            g = self.g
            self.am0 = AllMom2(g.G, g.n, D, W=g.W, groups=g.groups, caps={1: self.qcap})
        return self.am0


def series_product(gser, scal, kmax):
    """F_i = scal sum_{compositions} prod_g F^(g)_{i_g}, i <= kmax (dict polynomials)."""
    out = []
    for i in range(kmax + 1):
        acc = {}
        def rec(gi, rem, cur):
            nonlocal acc
            if gi == len(gser):
                if rem == 0:
                    acc = padd(acc, cur)
                return
            for ig in range(rem + 1):
                if gser[gi][ig]:
                    rec(gi + 1, rem - ig, pmul(cur, gser[gi][ig]))
        nv = next((len(next(iter(P))) for ser in gser for P in ser if P), None)
        if nv is None:
            out.append({})
            continue
        rec(0, i, {tuple([0] * nv): scal})
        out.append(acc)
    return out


def bound5b(prep, factors, verbose=False):
    g, t, J = prep.g, prep.t, prep.J
    V, n, W = g.V, g.n, g.W
    a_v, ap = prep.a_v, prep.ap
    inf = float("inf")
    scal, groups = group_factors(factors)
    G_ = max(len(groups), 1)
    gser, gbar, gbarp = [], [], []
    for gf in groups:
        gser.append(_r3.Model3(g, 3, gf).Fser(3).c)
    Fi = series_product(gser, scal, 3) if groups else [{tuple([0] * g.F): scal}, {}, {}, {}]
    qmax = max([sum(e[V:]) for P in Fi for e in P] + [0])
    assert qmax <= prep.qcap, (qmax, prep.qcap)
    Dn = max(_deg(Fi[i]) + _deg(prep.Ej[k - i]) for k in range(4) for i in range(k + 1) if Fi[i])
    am = prep.engine(max(Dn, 1))
    ak = [sum(am.E2(Fi[i], prep.Ej[k - i]) for i in range(k + 1) if Fi[i]) for k in range(4)]
    if not prep.ok:
        return ak, {"rem": inf, "tail": inf, "ann": inf, "far": inf}
    for gf in groups:
        mj = _r3.Majorants3(_r3.Model3(g, 4, gf), a_v, t)
        gbar.append([mj.Fbar(j).to_dict() for j in range(5)])
        gbarp.append(_r3.Majorants3(_r3.Model3(g, 4, gf), [ap] * V, t).Fbar(0).to_dict())
    key = prep.key
    kc = key + "|c%.10g" % t
    def comps(i):
        out = [[]]
        for _ in groups:
            out = [c + [x] for c in out for x in range(i + 1)]
        return [tuple(c) for c in out if sum(c) == i]
    def fnorm(i, p, Gm, kk):
        if not groups:
            return abs(scal) if i == 0 else 0.0
        tot = 0.0
        for c in comps(i):
            val = 1.0
            for gi, ig in enumerate(c):
                val *= lp_norm(gser[gi][ig], Gm, n, W, p * G_, kk, 64) if gser[gi][ig] else 0.0
            tot += val
        return abs(scal) * tot
    nF = [fnorm(i, 2, g.G, key + "|F") for i in range(4)]
    nFle3 = sum(t ** i * nF[i] for i in range(4))
    nFle3c = sum(t ** i * fnorm(i, 2, prep.Gc, kc + "|F") for i in range(4))
    EF4 = 0.0
    if groups:
        for c in comps(4):
            val = math.factorial(4) / math.prod(math.factorial(x) for x in c)
            for gi, jg in enumerate(c):
                val *= pos_norm(gbar[gi][jg], prep.Gc, n, W, G_, kc + "|Fb") if gbar[gi][jg] else 0.0
            EF4 += val
        EF4 *= abs(scal)
    overflow = sum(t ** (i + j) * nF[i] * prep.nE[j] for i in range(4) for j in range(4) if i + j >= 4)
    B_rem = overflow + nFle3 * prep.rE + prep.Nc / 24 * nFle3c * prep.nC8 ** 4 + t ** 4 / 24 * prep.Nc * EF4
    nF4 = [fnorm(i, 4, g.G, key + "|F") for i in range(4)]
    l2 = sum(t ** k * sum(nF4[i] * prep.nE4[k - i] for i in range(k + 1)) for k in range(4))
    B_tail = l2 * math.sqrt(prep.Pout)
    nF0p = abs(scal)
    for gi in range(len(groups)):
        nF0p *= lp_norm(gbarp[gi], prep.Gp, n, W, 2 * G_, key + "|p%.10g" % t, 64)
    B_ann = prep.Np * nF0p * math.sqrt(prep.Pout_p)
    B_far = _r3.sup_F3(factors, J) * prep.farbase
    if verbose:
        print("  ||F_i|| %s E_c Fbar4 %.3g | overflow %.2e, F.R_E %.2e, rho4 %.2e, R_F %.2e"
              % (["%.3g" % x for x in nF], EF4, overflow, nFle3 * prep.rE, prep.Nc / 24 * nFle3c * prep.nC8 ** 4, t ** 4 / 24 * prep.Nc * EF4))
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}
