#!/usr/bin/env python3
# pk10 (code): Lemma 19.1c: THIRD-order-exact Laplace bounds with a quartic remainder for small-graph O(N) integrals with insertions.
# Chart, gauge, H, xi, factors, Omega, tilts as Lemma 19.1.  On Omega (t' <= t):
#   H = tH1 + t^2H2 + t^3H3 + R4H, |R4H| <= t^4 hbar4/24;  D3 := H - tH1 - t^2H2, |D3| <= t^3 hbar3/6;  E2 := H - tH1, |E2| <= t^2 hbar2/2;
#   e^H = sum_{j<=3} t^j E_j + R_E,  E0 = 1, E1 = H1, E2 = H2 + H1^2/2, E3 = H3 + H1H2 + H1^3/6,
#   R_E = R4H + (1/2)(t^4H2^2 + D3^2 + 2tH1D3 + 2t^2H2D3) + (1/6)(3t^2H1^2E2 + 3tH1E2^2 + E2^3) + rho4(H),  |rho4(x)| <= x^4 e^{x_+}/24,
#   |H| <= t|H1| + (t^2/2)hbar2 <= t(|H1| + hhat)   (hhat: degree-2 trading of hbar2 on Omega),  H_+ <= c t X;
#   F = sum_{i<=3} t^i F_i + R_F, |R_F| <= t^4 Fbar4/24;   F e^H = sum_{k<=3} t^k (F e^H)_k + overflow + F_{<=3} R_E + R_F e^H.
# Norms: X-only H-norms exact up to degree DMAXH (Hoelder-per-monomial beyond, only in t^5, t^6 terms), insertion norms per column (Hoelder).
import math
import numpy as np
from scipy.special import ive
import riglap2 as _r
import riglap3 as _r3
from riglap2 import chi_tail, tree_couplings
from riglap4 import lp_norm, pos_norm, norm_any, group_factors, _deg
from pseries import padd, pscale, pmul
from amom2b import AllMom2


def hhat2(g, a_v, t, h2):
    """hhat >= (t/2) hbar2 on Omega with degree <= 2: degree-2 part of hbar2 times t/2, plus the degree-3 bond part with t M1 <= a_u + a_v."""
    out = {e: c * t / 2 for e, c in h2.items() if sum(e) == 2}
    NV = len(next(iter(h2)))
    for (u, v), c in g.edges.items():
        ae = max(a_v[u], a_v[v])
        K = (c / 2.0) * math.factorial(2) / (4 * (1 - ae) ** 3)
        coef = 0.5 * K * (a_v[u] + a_v[v])
        for (iu, pu, iv, pv, s) in ((u, 2, v, 0, 1.0), (u, 1, v, 1, -2.0), (u, 0, v, 2, 1.0)):
            e = [0] * NV; e[iu] += pu; e[iv] += pv
            out[tuple(e)] = out.get(tuple(e), 0.0) + coef * s
    assert all(sum(e) <= 2 for e in out)
    return out


def bound5(g, factors, J, rho, rho_p, key="g", dmaxH=16, verbose=False):
    t = 1.0 / J
    V, n = g.V, g.n
    a_v = [r * r for r in rho]; ap = rho_p * rho_p
    inf = float("inf")
    rates = np.array([-math.log(1 - a_v[v]) / (2 * a_v[v]) * t for v in range(V)])
    ratesp = np.array([-math.log(1 - ap) / (2 * ap) * t] * V)
    Gc, Nc = g.tilted(rates)
    Gp_, Np_ = g.tilted(ratesp)
    m3 = _r3.Model3(g, 3, factors)
    coef = m3.exact()
    am0 = AllMom2(g.G, n, max(max(_deg(P) for P in coef), 1), W=g.W)
    ak = [am0.E(P) if P else 0.0 for P in coef]
    if Gc is None or Gp_ is None:
        return ak, {"rem": inf, "tail": inf, "ann": inf, "far": inf}
    Hs = m3.H(3)
    H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
    H1sq = pmul(H1, H1)
    Ej = [None, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
    mjH = _r.Majorants(_r.Model(g, 4, []), a_v, t)
    h2 = mjH.hbar(2).to_dict(); h3 = mjH.hbar(3).to_dict(); h4 = mjH.hbar(4).to_dict()
    hh = hhat2(g, a_v, t, h2)
    W = g.W
    kH, kc = key + "|H", key + "|c%.10g" % t
    N2 = lambda P: norm_any(P, g.G, n, W, 2, kH, dmaxH)
    nE = [1.0] + [N2(Ej[j]) for j in (1, 2, 3)]
    # R_E pieces (untilted L2 norms of X-only polynomials)
    rE = (t ** 4 / 24 * N2(h4)
          + 0.5 * (t ** 4 * N2(pmul(H2, H2)) + t ** 6 / 36 * N2(pmul(h3, h3)) + t ** 4 / 3 * N2(pmul(H1, h3)) + t ** 5 / 3 * N2(pmul(H2, h3)))
          + (1.0 / 6) * (1.5 * t ** 4 * N2(pmul(H1sq, h2)) + 0.75 * t ** 5 * N2(pmul(H1, pmul(h2, h2))) + t ** 6 / 8 * N2(pmul(h2, pmul(h2, h2)))))
    nC8 = t * (norm_any(H1, Gc, n, W, 8, kc, dmaxH) + norm_any(hh, Gc, n, W, 8, kc, dmaxH))
    # insertion groups
    scal, groups = group_factors(factors)
    G_ = max(len(groups), 1)
    gser, gbar, gbarp = [], [], []
    for gf in groups:
        gser.append(_r3.Model3(g, 3, gf).Fser(3).c)
        mj = _r3.Majorants3(_r3.Model3(g, 4, gf), a_v, t)
        gbar.append([mj.Fbar(j).to_dict() for j in range(5)])
        gbarp.append(_r3.Majorants3(_r3.Model3(g, 4, gf), [ap] * V, t).Fbar(0).to_dict())
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
    nFle3c = sum(t ** i * fnorm(i, 2, Gc, kc + "|F") for i in range(4))
    EF4 = 0.0
    if groups:
        for c in comps(4):
            val = math.factorial(4) / math.prod(math.factorial(x) for x in c)
            for gi, jg in enumerate(c):
                val *= pos_norm(gbar[gi][jg], Gc, n, W, G_, kc + "|Fb") if gbar[gi][jg] else 0.0
            EF4 += val
        EF4 *= abs(scal)
    overflow = sum(t ** (i + j) * nF[i] * nE[j] for i in range(4) for j in range(4) if i + j >= 4)
    B_rem = overflow + nFle3 * rE + Nc / 24 * nFle3c * nC8 ** 4 + t ** 4 / 24 * Nc * EF4
    # tail: sum_k t^k sum_{i+j=k} ||F_i||_4 ||E_j||_4 * P(Omega^c)^{1/2}
    nF4 = [fnorm(i, 4, g.G, key + "|F") for i in range(4)]
    nE4 = [1.0] + [norm_any(Ej[j], g.G, n, W, 4, kH, dmaxH) if _deg(Ej[j]) * 4 <= dmaxH else None for j in (1, 2, 3)]
    for j in (1, 2, 3):
        if nE4[j] is None:   # hypercontractivity: ||P||_4 <= 3^{d/2} ||P||_2 for degree-d polynomials of the Gaussian (d = 2 deg in X)
            nE4[j] = 3.0 ** (_deg(Ej[j])) * nE[j]
    l2 = sum(t ** k * sum(nF4[i] * nE4[k - i] for i in range(k + 1)) for k in range(4))
    Pout = sum(chi_tail(J * a_v[v] / g.G[v, v], n) for v in range(V))
    B_tail = l2 * math.sqrt(Pout)
    nF0p = abs(scal)
    for gi in range(len(groups)):
        nF0p *= lp_norm(gbarp[gi], Gp_, n, W, 2 * G_, key + "|p%.10g" % t, 64)
    Pout_p = sum(chi_tail(J * a_v[v] / Gp_[v, v], n) for v in range(V))
    B_ann = Np_ * nF0p * math.sqrt(Pout_p)
    Lp = np.diag(g.G)
    tree = tree_couplings(g)
    if g.N == 4:
        logtree = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        logtree = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    best = min(math.log(sum(math.exp(-th * J * ap / (2 * Lp[v])) for v in range(V))) + logtree((1 - th) * J) - g.logmain(J)
               for th in np.linspace(0.01, 0.99, 197))
    B_far = _r3.sup_F3(factors, J) * math.exp(best)
    if verbose:
        print("  ||E_j|| %s rE %.3g ||C||_8c %.3g N_c %.4f | ||F_i|| %s E_c Fbar4 %.3g | overflow %.2e, F.R_E %.2e, rho4 %.2e, R_F %.2e"
              % (["%.3g" % x for x in nE], rE, nC8, Nc, ["%.3g" % x for x in nF], EF4, overflow, nFle3 * rE, Nc / 24 * nFle3c * nC8 ** 4, t ** 4 / 24 * Nc * EF4))
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}
