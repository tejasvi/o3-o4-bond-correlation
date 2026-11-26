#!/usr/bin/env python3
# pk10 (code): riglap5b with per-group caching: series, majorants and their norms depend only on the (factor group, cov, exponent), so
# repeated groups (trial-space matrices: 10 basis polynomials per column) are computed once.  Same inequalities and numbers as riglap5b.
import math
import riglap3 as _r3
from riglap4 import lp_norm, pos_norm, group_factors, _deg
import riglap5b
from riglap5b import Prep5, series_product


def _fkey(gf):
    out = []
    for f in gf:
        if f[0] == 'xi':
            out.append(('xi', tuple(f[1]), float(f[2]), tuple(float(x) for x in f[3])))
        else:
            out.append(tuple(x if not isinstance(x, list) else tuple(x) for x in f))
    return tuple(out)


def _gdata(prep, gf):
    if not hasattr(prep, "gcache"):
        prep.gcache = {}
    k = _fkey(gf)
    if k not in prep.gcache:
        g, t = prep.g, prep.t
        ser = _r3.Model3(g, 3, gf).Fser(3).c
        d = {"ser": ser, "norm": {}}
        if prep.ok:
            mj = _r3.Majorants3(_r3.Model3(g, 4, gf), prep.a_v, t, B=riglap5b.NPOLY_B)
            d["bar"] = [mj.Fbar(j).to_dict() for j in range(5)]
            d["barp"] = _r3.Majorants3(_r3.Model3(g, 4, gf), [prep.ap] * g.V, t, B=riglap5b.NPOLY_B).Fbar(0).to_dict()
        prep.gcache[k] = d
    return prep.gcache[k]


def _gnorm(prep, d, what, i, p, cov):
    key = (what, i, p, cov)
    if key not in d["norm"]:
        g, n, W = prep.g, prep.g.n, prep.g.W
        Gm = {"u": g.G, "c": prep.Gc, "p": prep.Gp}[cov]
        tag = prep.key + "|" + cov + "%.10g" % prep.t
        if what == "ser":
            P = d["ser"][i]
            d["norm"][key] = lp_norm(P, Gm, n, W, p, tag + "|F", 64) if P else 0.0
        elif what == "bar":
            P = d["bar"][i]
            d["norm"][key] = pos_norm(P, Gm, n, W, p, tag + "|Fb") if P else 0.0
        else:
            P = d["barp"]
            d["norm"][key] = lp_norm(P, Gm, n, W, p, tag + "|p", 64) if P else 0.0
    return d["norm"][key]


def bound5c(prep, factors, verbose=False):
    g, t, J = prep.g, prep.t, prep.J
    V = g.V
    inf = float("inf")
    scal, groups = group_factors(factors)
    G_ = max(len(groups), 1)
    gds = [_gdata(prep, gf) for gf in groups]
    gser = [d["ser"] for d in gds]
    Fi = series_product(gser, scal, 3) if groups else [{tuple([0] * g.F): scal}, {}, {}, {}]
    qmax = max([sum(e[V:]) for P in Fi for e in P] + [0])
    assert qmax <= prep.qcap, (qmax, prep.qcap)
    Dn = max(_deg(Fi[i]) + _deg(prep.Ej[k - i]) for k in range(4) for i in range(k + 1) if Fi[i])
    am = prep.engine(max(Dn, 1))
    ak = [sum(am.E2(Fi[i], prep.Ej[k - i]) for i in range(k + 1) if Fi[i]) for k in range(4)]
    if not prep.ok:
        return ak, {"rem": inf, "tail": inf, "ann": inf, "far": inf}
    def comps(i):
        out = [[]]
        for _ in groups:
            out = [c + [x] for c in out for x in range(i + 1)]
        return [tuple(c) for c in out if sum(c) == i]
    def fnorm(i, p, cov):
        if not groups:
            return abs(scal) if i == 0 else 0.0
        return abs(scal) * sum(math.prod(_gnorm(prep, gds[gi], "ser", ig, p * G_, cov) for gi, ig in enumerate(c)) for c in comps(i))
    nF = [fnorm(i, 2, "u") for i in range(4)]
    nFle3 = sum(t ** i * nF[i] for i in range(4))
    nFle3c = sum(t ** i * fnorm(i, 2, "c") for i in range(4))
    EF4 = 0.0
    if groups:
        for c in comps(4):
            EF4 += math.factorial(4) / math.prod(math.factorial(x) for x in c) * math.prod(_gnorm(prep, gds[gi], "bar", jg, G_, "c") for gi, jg in enumerate(c))
        EF4 *= abs(scal)
    overflow = sum(t ** (i + j) * nF[i] * prep.nE[j] for i in range(4) for j in range(4) if i + j >= 4)
    B_rem = overflow + nFle3 * prep.rE + prep.Nc / 24 * nFle3c * prep.nC8 ** 4 + t ** 4 / 24 * prep.Nc * EF4
    nF4 = [fnorm(i, 4, "u") for i in range(4)]
    l2 = sum(t ** k * sum(nF4[i] * prep.nE4[k - i] for i in range(k + 1)) for k in range(4))
    B_tail = l2 * math.sqrt(prep.Pout)
    nF0p = abs(scal) * math.prod(_gnorm(prep, d, "barp", 0, 2 * G_, "p") for d in gds)
    B_ann = prep.Np * nF0p * math.sqrt(prep.Pout_p)
    B_far = _r3.sup_F3(factors, J) * prep.farbase
    return ak, {"rem": B_rem, "tail": B_tail, "ann": B_ann, "far": B_far}
