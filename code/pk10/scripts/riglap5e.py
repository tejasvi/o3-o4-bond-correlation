#!/usr/bin/env python3
# pk10 (code): Lemma 19.1c bounds (same inequalities as riglap5/5b/5c) organized for 3 insertion groups:
#   ||F0||_2 and ||F0||_{2,c} exactly (joint moments of degree 2 deg F0);  ||F_i||_2, i >= 1, by Hoelder over groups (L^{2G});
#   tail: k = 0 term exact, k >= 1 terms via hypercontractivity ||P||_4 <= 3^{deg P} ||P||_2 (Gaussian polynomial of degree 2 deg P);
#   annulus and Fbar4 by Hoelder over groups with cached per-group norms.
import math
import numpy as np
import riglap3 as _r3
from riglap4 import lp_norm, pos_norm, group_factors, _deg
from riglap5b import series_product
import riglap5b, riglap5c
from amom2b import AllMom2


def _joint(prep, D, cov):
    key = ("joint", D, cov)
    if not hasattr(prep, "jcache"):
        prep.jcache = {}
    if key not in prep.jcache:
        g = prep.g
        Gm = g.G if cov == "u" else prep.Gc
        prep.jcache[key] = AllMom2(Gm, g.n, D, W=g.W, groups=g.groups, caps={1: 2 * prep.qcap})
    return prep.jcache[key]


def bound5e(prep, factors):
    g, t, J = prep.g, prep.t, prep.J
    V = g.V
    inf = float("inf")
    scal, groups = group_factors(factors)
    G_ = max(len(groups), 1)
    gds = [riglap5c._gdata(prep, gf) for gf in groups]
    Fi = series_product([d["ser"] for d in gds], scal, 3) if groups else [{tuple([0] * g.F): scal}, {}, {}, {}]
    qmax = max([sum(e[V:]) for P in Fi for e in P] + [0])
    assert qmax <= prep.qcap, (qmax, prep.qcap)
    Dn = max(_deg(Fi[i]) + _deg(prep.Ej[k - i]) for k in range(4) for i in range(k + 1) if Fi[i])
    am = prep.engine(max(Dn, 1))
    ak = [sum(am.E2(Fi[i], prep.Ej[k - i]) for i in range(k + 1) if Fi[i]) for k in range(4)]
    if not prep.ok:
        return ak, {"rem": inf, "tail": inf, "ann": inf, "far": inf}
    d0 = 2 * _deg(Fi[0])
    nF0 = math.sqrt(max(_joint(prep, d0, "u").E2(Fi[0], Fi[0]), 0.0))
    nF0c = math.sqrt(max(_joint(prep, d0, "c").E2(Fi[0], Fi[0]), 0.0))
    def comps(i):
        out = [[]]
        for _ in groups:
            out = [c + [x] for c in out for x in range(i + 1)]
        return [tuple(c) for c in out if sum(c) == i]
    def fnorm(i, cov):
        return abs(scal) * sum(math.prod(riglap5c._gnorm(prep, gds[gi], "ser", ig, 2 * G_, cov) for gi, ig in enumerate(c)) for c in comps(i))
    nF = [nF0] + [fnorm(i, "u") for i in (1, 2, 3)]
    nFc = [nF0c] + [fnorm(i, "c") for i in (1, 2, 3)]
    nFle3 = sum(t ** i * nF[i] for i in range(4))
    nFle3c = sum(t ** i * nFc[i] for i in range(4))
    EF4 = 0.0
    for c in comps(4):
        EF4 += math.factorial(4) / math.prod(math.factorial(x) for x in c) * math.prod(riglap5c._gnorm(prep, gds[gi], "bar", jg, G_, "c") for gi, jg in enumerate(c))
    EF4 *= abs(scal)
    overflow = sum(t ** (i + j) * nF[i] * prep.nE[j] for i in range(4) for j in range(4) if i + j >= 4)
    B_rem = overflow + nFle3 * prep.rE + prep.Nc / 24 * nFle3c * prep.nC8 ** 4 + t ** 4 / 24 * prep.Nc * EF4
    hc = lambda i: 3.0 ** _deg(Fi[i]) * nF[i] if Fi[i] else 0.0
    l2 = nF0 + sum(t ** k * sum((hc(i) if i > 0 else 3.0 ** _deg(Fi[0]) * nF0) * prep.nE4[k - i] for i in range(k + 1)) for k in range(1, 4))
    B_tail = l2 * math.sqrt(prep.Pout)
    nF0p = abs(scal) * math.prod(riglap5c._gnorm(prep, d, "barp", 0, 2 * G_, "p") for d in gds)
    B_ann = prep.Np * nF0p * math.sqrt(prep.Pout_p)
    B_far = _r3.sup_F3(factors, J) * prep.farbase
    if getattr(prep, "verbose", False):
        print("    ||F_i|| %s ||F||_c %s E_c Fbar4 %.3g | overflow %.2e F.R_E %.2e rho4 %.2e R_F %.2e" % (["%.3g" % x for x in nF], ["%.3g" % x for x in nFc], EF4,
              overflow, nFle3 * prep.rE, prep.Nc / 24 * nFle3c * prep.nC8 ** 4, t ** 4 / 24 * prep.Nc * EF4))
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}
