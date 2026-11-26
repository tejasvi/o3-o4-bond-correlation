#!/usr/bin/env python3
# pk10 (code): Lemma 19.1c bounds, refined remainder (riglap5r) + degree-18 X-only norms:
#   (1/6)|E2|^3 <= (t^6/48) hbar2^3 with the exact ||hbar2^3||_2 (min with the traded t^5 form);
#   rho4: E_c[|F| C^4] <= ||F||_{3,c} ||C||_{6,c}^4 <= ||F||_{4,c} (t||H1||_{6,c} + (t^2/2)||hbar2||_{6,c})^4   (Hoelder 1/3 + 4/6 = 1),
#   taken as the minimum with the riglap5 form ||F||_{2,c} (t(||H1||_{8,c} + ||hhat||_{8,c}))^4;
#   ||F_{<=3}||_{4,c} <= prod_g ||F0^(g)||_{4G,c} + sum_{i>=1} t^i 3^{deg F_i} ||F_i||_{2,c}  (Hoelder over groups; hypercontractivity).
import math
import numpy as np
import riglap2 as _r
import riglap3 as _r3
import riglap5b, riglap5c
from riglap5r import Prep5r
from riglap4 import norm_any, lp_norm, group_factors, _deg
from riglap5b import series_product
from riglap5e import _joint
from pseries import pmul


class Prep5s(Prep5r):
    def __init__(self, g, J, rho, rho_p, key="g", qcap=4):
        super().__init__(g, J, rho, rho_p, key=key, dmaxH=18, qcap=qcap)
        if not self.ok:
            return
        t, n, W = self.t, g.n, g.W
        mjH = _r.Majorants(_r.Model(g, 3, []), self.a_v, t, B=riglap5b.NPOLY_B)
        h2 = mjH.hbar(2).to_dict()
        H1 = self.Ej[1]
        kH, kc = key + "|H", key + "|c%.10g" % t
        ex = t ** 6 / 48 * norm_any(pmul(h2, pmul(h2, h2)), g.G, n, W, 2, kH, 18)
        tr = self.rE_parts["t5 h2^2 hhat/24"]
        self.rE_parts["E2^3 term"] = min(ex, tr)
        del self.rE_parts["t5 h2^2 hhat/24"]
        self.rE = sum(self.rE_parts.values())
        self.nC6 = t * norm_any(H1, self.Gc, n, W, 6, kc, 18) + t * t / 2 * norm_any(h2, self.Gc, n, W, 6, kc, 18)


def bound5s(prep, factors):
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
    def fnorm(i, cov, p=2):
        return abs(scal) * sum(math.prod(riglap5c._gnorm(prep, gds[gi], "ser", ig, p * G_, cov) for gi, ig in enumerate(c)) for c in comps(i))
    nF = [nF0] + [fnorm(i, "u") for i in (1, 2, 3)]
    nFc = [nF0c] + [fnorm(i, "c") for i in (1, 2, 3)]
    nFle3 = sum(t ** i * nF[i] for i in range(4))
    nFle3c = sum(t ** i * nFc[i] for i in range(4))
    nF4c = fnorm(0, "c", 4) + sum(t ** i * 3.0 ** _deg(Fi[i]) * nFc[i] for i in (1, 2, 3) if Fi[i])
    EF4 = 0.0
    for c in comps(4):
        EF4 += math.factorial(4) / math.prod(math.factorial(x) for x in c) * math.prod(riglap5c._gnorm(prep, gds[gi], "bar", jg, G_, "c") for gi, jg in enumerate(c))
    EF4 *= abs(scal)
    overflow = sum(t ** (i + j) * nF[i] * prep.nE[j] for i in range(4) for j in range(4) if i + j >= 4)
    rho4 = prep.Nc / 24 * min(nFle3c * prep.nC8 ** 4, nF4c * prep.nC6 ** 4)
    B_rem = overflow + nFle3 * prep.rE + rho4 + t ** 4 / 24 * prep.Nc * EF4
    hc = lambda i: 3.0 ** _deg(Fi[i]) * nF[i] if Fi[i] else 0.0
    l2 = nF0 + sum(t ** k * sum((hc(i) if i > 0 else 3.0 ** _deg(Fi[0]) * nF0) * prep.nE4[k - i] for i in range(k + 1)) for k in range(1, 4))
    B_tail = l2 * math.sqrt(prep.Pout)
    nF0p = abs(scal) * math.prod(riglap5c._gnorm(prep, d, "barp", 0, 2 * G_, "p") for d in gds)
    B_ann = prep.Np * nF0p * math.sqrt(prep.Pout_p)
    B_far = _r3.sup_F3(factors, J) * prep.farbase
    if getattr(prep, "verbose", False):
        print("    overflow %.2e F.R_E %.2e rho4 %.2e (C8 form %.2e, C6 form %.2e) R_F %.2e"
              % (overflow, nFle3 * prep.rE, rho4, prep.Nc / 24 * nFle3c * prep.nC8 ** 4, prep.Nc / 24 * nF4c * prep.nC6 ** 4, t ** 4 / 24 * prep.Nc * EF4))
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}
