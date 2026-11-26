#!/usr/bin/env python3
# pk10 (code): Lemma 19.1b: second-order-exact Laplace bounds with a cubic remainder for small-graph O(N) integrals with insertions.
# Chart, gauge, H, xi, insertion factors, Omega, tilts: as Lemma 19.1 (riglap2/riglap3).  On Omega, with F = F0 + tF1 + t^2F2 + R_F,
# |R_F| <= (t^3/6) Fbar3, and H = tH1 + t^2H2 + R_H, |H - tH1| <= (t^2/2) hbar2, |R_H| <= (t^3/6) hbar3, H_+ <= c t X (tilt):
#   e^H = 1 + tH1 + t^2 P2 + R_E,  P2 = H2 + H1^2/2,
#   |R_E| <= (t^3/6) hbar3 + (t^3/2)|H1| hbar2 + (t^4/8) hbar2^2 + (1/6) C^3 e^{c t X},  C = t|H1| + (t^2/2) hbar2   [e^x <= 1+x+x^2/2+|x|^3 e^{x_+}/6]
#   F e^H = sum_{k<=2} t^k (F e^H)_k + Rem,
#   |Rem| <= t^3|F1 P2 + F2 H1| + t^4|F2 P2| + |F0 + tF1 + t^2F2| |R_E| + (t^3/6) Fbar3 e^{c t X}.
# Expectations of the remainder by Cauchy-Schwarz / Hoelder / Minkowski: X-only H-norms (once per graph) times per-column insertion norms.
# I/main = sum_{k<=2} a_k t^k + R,  |R| <= B_rem + B_tail + B_ann + B_far  (tail, annulus, far as Lemma 19.1, with Hoelder over columns).
import math
import numpy as np
from scipy.special import gammaln
import riglap2 as _r
import riglap3 as _r3
from riglap2 import chi_tail, tree_couplings
from pseries import padd, pscale, pmul
from amom2b import AllMom2
from scipy.special import ive

_ENG = {}


def _engine(G, n, W, idx, D, key):
    k = (key, tuple(idx), D)
    if k not in _ENG:
        _ENG[k] = AllMom2(G, n, D, W=W[:, list(idx)])
    return _ENG[k]


def _support(P):
    s = set()
    for e in P:
        for i, x in enumerate(e):
            if x:
                s.add(i)
    return sorted(s)


def _restrict(P, idx):
    out = {}
    for e, c in P.items():
        k = tuple(e[i] for i in idx)
        out[k] = out.get(k, 0.0) + c
    return out


def _deg(P):
    return max([sum(e) for e in P] + [0])


def _power(P, k):
    out = P
    for _ in range(k - 1):
        out = pmul(out, P)
    return out


def lp_norm(P, G, n, W, p, key, dmax=16):
    """(E|P|^p)^{1/p}, p even, exact Gaussian moments on the forms in P's support; None if the degree exceeds dmax."""
    if not P:
        return 0.0
    idx = _support(P)
    if not idx:
        return abs(sum(P.values()))
    Q = _restrict(P, idx)
    Pk = _power(Q, p // 2)
    D = 2 * _deg(Pk)
    if D > dmax:
        return None
    am = _engine(G, n, W, idx, D, key)
    return max(am.E2(Pk, Pk), 0.0) ** (1.0 / p)


def holder_mono(P, Gdiag, n, p):
    """Minkowski over monomials + generalized Hoelder: ||sum c prod X_v^e_v||_p <= sum |c| prod ||X_v||_{p|e|}^{e_v} (X-only monomials)."""
    tot = 0.0
    for e, c in P.items():
        k = sum(e)
        if k == 0:
            tot += abs(c); continue
        q = p * k
        val = abs(c)
        for v, ev in enumerate(e):
            if ev:
                lm = q * math.log(2 * Gdiag[v]) + gammaln(q + n / 2.0) - gammaln(n / 2.0)
                val *= math.exp(lm / q) ** ev
        tot += val
    return tot


def norm_any(P, G, n, W, p, key, dmax=16):
    v = lp_norm(P, G, n, W, p, key, dmax)
    if v is not None:
        return v
    V = G.shape[0]
    assert all(all(x == 0 for x in e[V:]) for e in P), "Hoelder fallback only for X-only polynomials"
    return holder_mono({e[:V]: c for e, c in P.items()}, np.diag(G), n, p)


def _cols(f):
    if f[0] in ('xi', 'p'):
        return tuple(sorted(f[1]))
    if f[0] == 'dot':
        return tuple(sorted((f[1], f[2])))
    return ()


def group_factors(factors):
    """groups of factors with overlapping vertex sets (consts folded into a scalar)."""
    scal = 1.0
    groups = []
    for f in factors:
        if f[0] == 'const':
            scal *= f[1]; continue
        vs = set(_cols(f))
        hit = [gi for gi, (gv, gf) in enumerate(groups) if gv & vs]
        if not hit:
            groups.append((vs, [f]))
        else:
            gv, gf = groups[hit[0]]
            gv |= vs; gf.append(f)
            for gi in sorted(hit[1:], reverse=True):
                gv |= groups[gi][0]; gf.extend(groups[gi][1]); groups.pop(gi)
    return scal, [gf for gv, gf in groups]


def bound4(g, factors, J, rho, rho_p, key="g", dmaxH=16, verbose=False):
    t = 1.0 / J
    V, n = g.V, g.n
    a_v = [r * r for r in rho]; ap = rho_p * rho_p
    inf = float("inf")
    rates = np.array([-math.log(1 - a_v[v]) / (2 * a_v[v]) * t for v in range(V)])
    ratesp = np.array([-math.log(1 - ap) / (2 * ap) * t] * V)
    Gc, Nc = g.tilted(rates)
    Gp_, Np_ = g.tilted(ratesp)
    m2 = _r3.Model3(g, 2, factors)
    coef = m2.exact()
    dk = max(_deg(P) for P in coef)
    am0 = AllMom2(g.G, n, max(dk, 1), W=g.W)
    ak = [am0.E(P) if P else 0.0 for P in coef]
    if Gc is None or Gp_ is None:
        return ak, {"rem": inf, "tail": inf, "ann": inf, "far": inf}
    Hs = m2.H(2)
    H1, H2 = Hs.c[1], Hs.c[2]
    P2 = padd(H2, pscale(pmul(H1, H1), 0.5))
    mjH = _r.Majorants(_r.Model(g, 3, []), a_v, t)
    h2 = mjH.hbar(2).to_dict(); h3 = mjH.hbar(3).to_dict()
    W = g.W
    kH, kc = key + "|H", key + "|c%.10g" % t
    # X-only H norms (untilted / tilted)
    nH1 = norm_any(H1, g.G, n, W, 2, kH, dmaxH); nP2 = norm_any(P2, g.G, n, W, 2, kH, dmaxH)
    nh3 = norm_any(h3, g.G, n, W, 2, kH, dmaxH); nH1h2 = norm_any(pmul(H1, h2), g.G, n, W, 2, kH, dmaxH)
    nh2sq = norm_any(pmul(h2, h2), g.G, n, W, 2, kH, dmaxH)
    nH1_6c = norm_any(H1, Gc, n, W, 6, kc, dmaxH); nh2_6c = norm_any(h2, Gc, n, W, 6, kc, dmaxH)
    nH1_4 = norm_any(H1, g.G, n, W, 4, kH, dmaxH); nP2_4 = norm_any(P2, g.G, n, W, 4, kH, dmaxH)
    # insertion groups
    scal, groups = group_factors(factors)
    G_ = max(len(groups), 1)
    gser, gbar, gbarp = [], [], []
    for gf in groups:
        mg = _r3.Model3(g, 2, gf)
        gser.append(mg.Fser(2).c)
        mj = _r3.Majorants3(_r3.Model3(g, 3, gf), a_v, t)
        gbar.append([mj.Fbar(j).to_dict() for j in range(4)])
        mjp = _r3.Majorants3(_r3.Model3(g, 3, gf), [ap] * V, t)
        gbarp.append(mjp.Fbar(0).to_dict())
    def comps(i):
        """compositions of i into len(groups) parts"""
        if not groups:
            return [()] if i == 0 else []
        out = [[]]
        for _ in groups:
            out = [c + [x] for c in out for x in range(i + 1)]
        return [tuple(c) for c in out if sum(c) == i]
    def fnorm(i, p, Gm, kk):
        """|| F_i ||_p <= |scal| sum_{compositions} prod_g || F^(g)_{i_g} ||_{p G}"""
        if not groups:
            return abs(scal) if i == 0 else 0.0
        tot = 0.0
        for c in comps(i):
            val = 1.0
            for gi, ig in enumerate(c):
                val *= lp_norm(gser[gi][ig], Gm, n, W, p * G_, kk, 64) if gser[gi][ig] else 0.0
            tot += val
        return abs(scal) * tot
    nF = [fnorm(i, 2, g.G, key + "|F") for i in range(3)]
    nFle2 = nF[0] + t * nF[1] + t * t * nF[2]
    nFle2c = sum(t ** i * fnorm(i, 2, Gc, kc + "|F") for i in range(3))
    nF4 = [fnorm(i, 4, g.G, key + "|F") for i in range(3)]
    # E_c[Fbar3] <= |scal| sum_{j-compositions of 3} (3!/prod j!) E_c[prod_g Fbar^(g)_{j_g}];  one group: exact E_c; G >= 2: Hoelder with
    # exponents G (Fbar >= 0 pointwise, so ||Y||_G = E[Y^G]^{1/G} for integer G)
    EF3 = 0.0
    if groups:
        for c in comps(3):
            val = math.factorial(3) / math.prod(math.factorial(x) for x in c)
            for gi, jg in enumerate(c):
                val *= pos_norm(gbar[gi][jg], Gc, n, W, G_, kc + "|Fb") if gbar[gi][jg] else 0.0
            EF3 += val
        EF3 *= abs(scal)
    # remainder on Omega
    Cn = t * nH1_6c + t * t / 2 * nh2_6c
    B_rem = (t ** 3 * (nF[1] * nP2 + nF[2] * nH1) + t ** 4 * nF[2] * nP2
             + nFle2 * (t ** 3 / 6 * nh3 + t ** 3 / 2 * nH1h2 + t ** 4 / 8 * nh2sq)
             + Nc / 6 * nFle2c * Cn ** 3 + t ** 3 / 6 * Nc * EF3)
    # tail: || sum_k t^k (F e^H)_k ||_2 P(Omega^c)^{1/2}, (F e^H)_k = sum_{i+j=k} F_i (e^H)_j, (e^H)_1 = H1, (e^H)_2 = P2
    eH4 = [1.0, nH1_4, nP2_4]
    l2 = sum(t ** k * sum(nF4[i] * eH4[k - i] for i in range(k + 1)) for k in range(3))
    Pout = sum(chi_tail(J * a_v[v] / g.G[v, v], n) for v in range(V))
    B_tail = l2 * math.sqrt(Pout)
    # annulus: N' ||Fbar0'||_{2,c'} P'(Omega^c)^{1/2}, Fbar0' = |scal| prod_g Fbar^(g)_0 (radius rho')
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
        print("  ||H1|| %.3g ||P2|| %.3g ||h3|| %.3g ||H1 h2|| %.3g ||h2^2|| %.3g ||H1||_6c %.3g ||h2||_6c %.3g N_c %.4f | ||F_i|| %s E_c Fbar3 %.3g"
              % (nH1, nP2, nh3, nH1h2, nh2sq, nH1_6c, nh2_6c, Nc, ["%.3g" % x for x in nF], EF3))
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}


def pos_norm(P, G, n, W, p, key):
    """(E[P^p])^{1/p} for a pointwise-nonnegative polynomial P and integer p >= 1 (p = 1: E[P])."""
    if not P:
        return 0.0
    idx = _support(P)
    if not idx:
        return abs(sum(P.values()))
    Q = _restrict(P, idx)
    Pk = _power(Q, p)
    am = _engine(G, n, W, idx, _deg(Pk), key)
    return max(am.E(Pk), 0.0) ** (1.0 / p)
