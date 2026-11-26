#!/usr/bin/env python3
"""arbeng_v1.py -- pk01 (code/pk01/). The arb layer of SPEC_M1_CERT_v1_1_ADD2: ball-arithmetic ports of the PK10 moment engines that
engine A uses (amom2b.AllMom2, condexp2.CondMom, condg.CondG and GSpace, wishart.Wishart, npoly.NPoly) and of pseries' dict polynomials.
No compute of its own: imported by a frozen job script, which sets flint.ctx.prec (128).
Model. Index arithmetic (exponent codes, supports, searchsorted, hit masks, np.unique) is exact numpy int64, as in the float modules, with
  their code-space assertions. Values are python-flint arb balls held in Python lists; every accumulation is a ball operation, so every
  computed value is a ball that contains the exact value of the corresponding float-module quantity for exact inputs inside the input balls.
  Accumulation order differs from the float modules' (np.bincount), which does not matter for enclosures. Polynomial sums keep every term
  whose ball is not exactly zero (no ball comparison ever drops a term). No *_series function is used.
arbeng_c2b_v2.py -- pk02: arbeng_c2b_v1.py (a70d0cc4) with one addition, AllMom2A's optional W_int (the forms as integer columns over
  the underlying coordinates, Gam = W^T G W for any G): a subset A with exact integer rank(W_int[:, A]) < |A| has det(Gam_A) = 0 exactly, for
  every G, so its term is left out of the recursion (an exact zero). Each such det is still computed and must contain 0 (else ValueError:
  a check of the rank argument against the balls); zeroed and max_zero_rad record the count and the largest radius met. Reason
  (kt_cert_v1_4's smoke): arb_mat.det on an exactly singular minor can return a radius that no precision removes (row-pivoted elimination,
  then a Hadamard bound over the remaining rows), which entered the tail tables. Everything else is arbeng_c2b_v1's.
"""
import math, itertools
from fractions import Fraction
import numpy as np
from flint import arb, arb_mat


def int_rank(W_int, cols):
    """the exact rank of the integer matrix W_int[:, cols] (Fraction elimination)."""
    M = [[Fraction(int(W_int[i][c])) for c in cols] for i in range(len(W_int))]
    rk = 0
    for c in range(len(cols)):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

ZERO = arb(0)
ONE = arb(1)


def A(x):
    """an arb ball for x: arb as is; int and binary64 exactly."""
    return x if isinstance(x, arb) else arb(x)


def is_zero(x):
    return x.is_zero() if isinstance(x, arb) else (x == 0)


def mat(rows):
    """arb_mat from nested lists of numbers or balls."""
    m, n = len(rows), len(rows[0])
    M = arb_mat(m, n)
    for i in range(m):
        for j in range(n):
            M[i, j] = A(rows[i][j])
    return M


def mat_np(X):
    """arb_mat from a numpy float array (each entry exact as binary64)."""
    X = np.asarray(X, dtype=float)
    return mat(X.tolist())


def mat_mul(Am, Bm):
    return Am * Bm


def mat_T(Am):
    return Am.transpose()


def mat_entries(M):
    return [[M[i, j] for j in range(M.ncols())] for i in range(M.nrows())]


def scatter_acc(acc, supk, ca, va, cb, vb, chunk=4000000):
    """acc[i] += va[p] * vb[q] for every pair whose code sum ca[p] + cb[q] equals supk[i] (supk sorted); va, vb, acc lists of balls."""
    if len(ca) == 0 or len(cb) == 0:
        return
    nb = len(cb)
    rows = max(1, chunk // nb)
    ns = len(supk)
    for s0 in range(0, len(ca), rows):
        cs = (ca[s0:s0 + rows, None] + cb[None, :]).ravel()
        idx = np.searchsorted(supk, cs)
        idx[idx >= ns] = 0
        hit = np.flatnonzero(supk[idx] == cs)
        if len(hit) == 0:
            continue
        ii = idx[hit].tolist()
        pp = (s0 + hit // nb).tolist()
        qq = (hit % nb).tolist()
        for i, p, q in zip(ii, pp, qq):
            acc[i] += va[p] * vb[q]


def dot_pairs(ca, va, cb, vb, index_fn, mom, chunk=4000000):
    """sum over all pairs (p, q) of va[p] vb[q] mom[index_fn(ca[p] + cb[q])] (every code sum must be present: index_fn asserts)."""
    tot = arb(0)
    if len(ca) == 0 or len(cb) == 0:
        return tot
    nb = len(cb)
    rows = max(1, chunk // nb)
    for s0 in range(0, len(ca), rows):
        cs = (ca[s0:s0 + rows, None] + cb[None, :]).ravel()
        idx = index_fn(cs).tolist()
        k = 0
        for p in range(s0, min(s0 + rows, len(ca))):
            ap = va[p]
            acc = arb(0)
            for q in range(nb):
                acc += vb[q] * mom[idx[k]]
                k += 1
            tot += ap * acc
    return tot


# ------------------------------------------------------------------ dict polynomials with ball coefficients (pseries)
def padd(*Ps):
    out = {}
    for P in Ps:
        for e, c in P.items():
            out[e] = out[e] + c if e in out else A(c)
    return {e: c for e, c in out.items() if not c.is_zero()}


def pscale(P, s):
    s = A(s)
    if s.is_zero():
        return {}
    return {e: c * s for e, c in P.items()}


def pmul(P, Q):
    out = {}
    for e1, c1 in P.items():
        for e2, c2 in Q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            v = c1 * c2
            out[e] = out[e] + v if e in out else v
    return {e: c for e, c in out.items() if not c.is_zero()}


def pconst(c, nv):
    c = A(c)
    return {tuple([0] * nv): c} if not c.is_zero() else {}


def pvar(i, nv, c=1):
    e = [0] * nv
    e[i] = 1
    return {tuple(e): A(c)}


def deg(P):
    return max([sum(e) for e in P] + [0])


class Series:
    """sum_{k=0}^K t^k P_k with ball-coefficient dict polynomials (pseries.Series, same operations)."""
    def __init__(self, K, nv, coeffs=None):
        self.K, self.nv = K, nv
        self.c = [dict(p) for p in coeffs] if coeffs is not None else [{} for _ in range(K + 1)]
        while len(self.c) < K + 1:
            self.c.append({})

    def copy(self):
        return Series(self.K, self.nv, self.c)

    def __add__(self, o):
        return Series(self.K, self.nv, [padd(a, b) for a, b in zip(self.c, o.c)])

    def __sub__(self, o):
        return Series(self.K, self.nv, [padd(a, pscale(b, -1)) for a, b in zip(self.c, o.c)])

    def scale(self, s):
        return Series(self.K, self.nv, [pscale(a, s) for a in self.c])

    def __mul__(self, o):
        out = [{} for _ in range(self.K + 1)]
        for i in range(self.K + 1):
            if not self.c[i]:
                continue
            for j in range(self.K + 1 - i):
                if o.c[j]:
                    out[i + j] = padd(out[i + j], pmul(self.c[i], o.c[j]))
        return Series(self.K, self.nv, out)

    def exp(self):
        """exp of a series with zero constant term: E_0 = 1, k E_k = sum_{j=1}^k j H_j E_{k-j}."""
        assert all(c.is_zero() for c in self.c[0].values()), "exp needs H_0 = 0"
        E = [pconst(1, self.nv)] + [{} for _ in range(self.K)]
        for k in range(1, self.K + 1):
            acc = {}
            for j in range(1, k + 1):
                if self.c[j] and E[k - j]:
                    acc = padd(acc, pscale(pmul(self.c[j], E[k - j]), j))
            E[k] = pscale(acc, arb(1) / k)
        return Series(self.K, self.nv, E)


def w_coeffs(K):
    """pseries.w_coeffs in exact rationals, returned as balls: w(x, y) = (sqrt(1 - x) + sqrt(1 - y))^-2 = sum w[i][j] x^i y^j, i + j <= K."""
    from fractions import Fraction
    s = [Fraction(1)] + [Fraction(-math.comb(2 * k, k), 4 ** k * (2 * k - 1)) for k in range(1, K + 1)]
    d = {}
    for k in range(1, K + 1):
        d[(k, 0)] = d.get((k, 0), Fraction(0)) + s[k]
        d[(0, k)] = d.get((0, k), Fraction(0)) + s[k]

    def mul2(Ad, Bd):
        o = {}
        for (i1, j1), c1 in Ad.items():
            for (i2, j2), c2 in Bd.items():
                if i1 + i2 + j1 + j2 <= K:
                    o[(i1 + i2, j1 + j2)] = o.get((i1 + i2, j1 + j2), Fraction(0)) + c1 * c2
        return o
    w = {(0, 0): Fraction(1, 4)}
    pw = {(0, 0): Fraction(1)}
    hd = {k: -v / 2 for k, v in d.items()}
    for m in range(1, K + 1):
        pw = mul2(pw, hd)
        for k, v in pw.items():
            w[k] = w.get(k, Fraction(0)) + Fraction(m + 1, 4) * v
    return {k: arb(v.numerator) / v.denominator for k, v in w.items()}


def sigma_to_g(P6):
    """condg.sigma_to_g with ball coefficients: X_r = g_rr, Q_rs = g_rr + g_ss - 2 g_rs (order (0,0),(0,1),(0,2),(1,1),(1,2),(2,2))."""
    lin = {0: {(1, 0, 0, 0, 0, 0): ONE}, 1: {(0, 0, 0, 1, 0, 0): ONE}, 2: {(0, 0, 0, 0, 0, 1): ONE},
           3: {(1, 0, 0, 0, 0, 0): ONE, (0, 0, 0, 1, 0, 0): ONE, (0, 1, 0, 0, 0, 0): arb(-2)},
           4: {(0, 0, 0, 1, 0, 0): ONE, (0, 0, 0, 0, 0, 1): ONE, (0, 0, 0, 0, 1, 0): arb(-2)},
           5: {(1, 0, 0, 0, 0, 0): ONE, (0, 0, 0, 0, 0, 1): ONE, (0, 0, 1, 0, 0, 0): arb(-2)}}
    cache = {}

    def powpoly(e):
        if e not in cache:
            poly = {tuple([0] * 6): ONE}
            for i, m in enumerate(e):
                for _ in range(m):
                    poly = pmul(poly, lin[i])
            cache[e] = poly
        return cache[e]
    res = {}
    for e, c in P6.items():
        for eg, cc in powpoly(tuple(e)).items():
            v = A(c) * cc
            res[eg] = res[eg] + v if eg in res else v
    return {e: c for e, c in res.items() if not c.is_zero()}


# ------------------------------------------------------------------ AllMom2 (amom2b)
class AllMom2A:
    """amom2b.AllMom2 in balls. Gam: arb_mat F x F (W^T G W, formed by the caller in arb). codes, caps and the recursion as amom2b.
    W_int (arbeng_c2b_v2): optional integer R x F matrix with Gam = W_int^T G W_int; subsets with rank(W_int[:, A]) < |A| are exact zeros."""
    def __init__(self, Gam, n, D, groups=None, caps=None, chunk=4000000, W_int=None):
        F = Gam.nrows()
        if W_int is not None:
            assert len(W_int[0]) == F and all(float(x) == int(x) for row in W_int for x in row)
        self.zeroed, self.max_zero_rad, self.dropped = 0, 0.0, []
        self.F, self.D, self.n, self.chunk = F, D, n, chunk
        self.groups = np.zeros(F, dtype=np.int64) if groups is None else np.asarray(groups, dtype=np.int64)
        self.caps = {} if caps is None else dict(caps)
        B = D + 1
        assert float(B) ** F < 9.0e18
        self.B = B
        self.pw = np.array([B ** f for f in range(F)], dtype=np.int64)
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            c = np.unique((codes[-1][:, None] + self.pw[None, :]).ravel())
            codes.append(c[self.ok(c)])
        self.codes = codes
        Dj = [None] + [([], []) for j in range(min(F, D))]
        for j in range(1, min(F, D) + 1):
            cs, vs = [], []
            sign = arb(-2) ** j
            for Aset in itertools.combinations(range(F), j):
                c = int(sum(int(self.pw[f]) for f in Aset))
                if not self.ok(np.array([c], dtype=np.int64))[0]:
                    continue
                sub = arb_mat(j, j)
                for a_, fa in enumerate(Aset):
                    for b_, fb in enumerate(Aset):
                        sub[a_, b_] = Gam[fa, fb]
                d = sub.det()
                if W_int is not None and int_rank(W_int, Aset) < j:
                    if not d.contains(0):
                        raise ValueError('det of the singular subset %s excludes 0: %s' % (Aset, d.str(8, radius=True)))
                    self.zeroed += 1
                    self.max_zero_rad = max(self.max_zero_rad, float(d.rad()))
                    self.dropped.append((Aset, d))
                    continue
                cs.append(c)
                vs.append(sign * d)
            Dj[j] = (np.array(cs, dtype=np.int64), vs)
        self.Dj = Dj
        M = [[arb(1)]] + [None] * D
        half_n = arb(n) / 2
        for k in range(1, D + 1):
            acc = [arb(0) for _ in range(len(codes[k]))]
            for j in range(1, min(k, F) + 1):
                cj, vj = Dj[j]
                if len(cj) == 0:
                    continue
                coef = (1 - half_n) * j - k
                part = [arb(0) for _ in range(len(codes[k]))]
                scatter_acc(part, codes[k], cj, vj, codes[k - j], M[k - j], chunk)
                for i in range(len(acc)):
                    acc[i] += coef * part[i]
            M[k] = [a / k for a in acc]
        self.mom = []
        for d in range(D + 1):
            ex = self.decode(codes[d])
            row = []
            for i in range(len(codes[d])):
                f = 1
                for x in ex[i]:
                    f *= math.factorial(int(x))
                row.append(M[d][i] * f)
            self.mom.append(row)

    def ok(self, c):
        if not self.caps:
            return np.ones(len(c), dtype=bool)
        ex = self.decode(c)
        good = np.ones(len(c), dtype=bool)
        for g, cap in self.caps.items():
            good &= ex[:, self.groups == g].sum(axis=1) <= cap
        return good

    def decode(self, c):
        return np.stack([(c // self.pw[f]) % self.B for f in range(self.F)], axis=1)

    def index(self, k, cs):
        idx = np.searchsorted(self.codes[k], cs)
        assert np.all(idx < len(self.codes[k])) and np.array_equal(self.codes[k][idx], cs)
        return idx

    def arr(self, P):
        ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, self.F)
        return ex.sum(axis=1), ex @ self.pw, [A(v) for v in P.values()]

    def E(self, P):
        if not P:
            return arb(0)
        dg, cs, co = self.arr(P)
        assert dg.max() <= self.D
        tot = arb(0)
        for d in np.unique(dg):
            sel = np.flatnonzero(dg == d)
            idx = self.index(int(d), cs[sel]).tolist()
            m = self.mom[int(d)]
            for a_, i in zip(sel.tolist(), idx):
                tot += co[a_] * m[i]
        return tot

    def E2(self, P, Q):
        dP, cP, aP = self.arr(P)
        dQ, cQ, aQ = self.arr(Q)
        tot = arb(0)
        for d1 in np.unique(dP):
            s1 = np.flatnonzero(dP == d1)
            for d2 in np.unique(dQ):
                s2 = np.flatnonzero(dQ == d2)
                k = int(d1 + d2)
                assert k <= self.D
                tot += dot_pairs(cP[s1], [aP[i] for i in s1], cQ[s2], [aQ[i] for i in s2], lambda cs, k=k: self.index(k, cs),
                                 self.mom[k], self.chunk)
        return tot


# ------------------------------------------------------------------ CondMom (condexp2)
class CondMomA:
    """condexp2.CondMom in balls: phi2 = Mmat phi1 + zeta, zeta ~ N(0, Cmat) (x) I_n; Mmat, Cmat, W arb_mat (W exact).
    Same supports, caps and table format {s-exponent: {g-exponent: ball}}."""
    def __init__(self, Mmat, Cmat, W, n, Dc, groups=None, caps=None, chunk=4000000):
        F = W.ncols()
        n1 = Mmat.ncols()
        self.F, self.n1, self.Dc, self.n = F, n1, Dc, n
        self.groups = np.zeros(F, dtype=np.int64) if groups is None else np.asarray(groups, dtype=np.int64)
        self.caps = {} if caps is None else dict(caps)
        self.gvars = [(r, s) for r in range(n1) for s in range(r, n1)]
        NG = len(self.gvars)
        self.NG = NG
        nv = F + NG
        B = Dc + 1
        assert float(B) ** nv < 9.0e18
        self.B = B
        self.pw = np.array([B ** i for i in range(nv)], dtype=np.int64)
        BF = int(self.pw[F])
        self.BF = BF
        Wt = W.transpose()
        P = Wt * Mmat
        Gam = Wt * Cmat * W
        sc = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            c = np.unique((sc[-1][:, None] + self.pw[None, :F]).ravel())
            sc.append(c[self.s_ok(c)])
        gc = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            gc.append(np.unique((gc[-1][:, None] + self.pw[None, F:]).ravel()))
        gle = [np.unique(np.concatenate(gc[:d + 1])) for d in range(Dc + 1)]
        sup = [np.sort((sc[k][:, None] + gle[k][None, :]).ravel()) for k in range(Dc + 1)]
        self.sup = sup
        sfull = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            sfull.append(np.unique((sfull[-1][:, None] + self.pw[None, :F]).ravel()))
        # Sk[m] = F x F arb_mat for each s-monomial m of degree d (only nonzero matrices kept)
        Sk = {}
        for f in range(F):
            Mf = arb_mat(F, F)
            Mf[f, f] = arb(1)
            Sk[int(np.searchsorted(sfull[1], self.pw[f]))] = Mf
        Pt = P.transpose()
        Y = [None] * (Dc + 1)
        for k in range(0, Dc):
            d = k + 1
            scale = arb(2) ** k
            codes, vals = [], []
            for mi, Smm in Sk.items():
                X = Pt * Smm * P
                base = int(sfull[d][mi])
                for gi, (r, s) in enumerate(self.gvars):
                    v = X[r, r] if r == s else X[r, s] + X[s, r]
                    if v.is_zero():
                        continue
                    code = base + int(self.pw[F + gi])
                    if not self.s_ok(np.array([code % BF], dtype=np.int64))[0]:
                        continue
                    codes.append(code)
                    vals.append(scale * v)
            order = np.argsort(np.array(codes, dtype=np.int64), kind='stable') if codes else np.zeros(0, dtype=np.int64)
            Y[d] = (np.array(codes, dtype=np.int64)[order], [vals[i] for i in order.tolist()])
            if d < Dc:
                new = {}
                for mi, Smm in Sk.items():
                    GS = Gam * Smm
                    for f in range(F):
                        row = arb_mat(F, F)
                        nz = False
                        for g in range(F):
                            if not GS[f, g].is_zero():
                                row[f, g] = GS[f, g]
                                nz = True
                        if not nz:
                            continue
                        idx = int(np.searchsorted(sfull[d + 1], sfull[d][mi] + self.pw[f]))
                        new[idx] = new[idx] + row if idx in new else row
                Sk = new
        E = [[arb(1)]]
        for k in range(1, Dc + 1):
            acc = [arb(0) for _ in range(len(sup[k]))]
            for j in range(1, k + 1):
                cj, vj = Y[j]
                if len(cj) == 0:
                    continue
                vjj = [j * v for v in vj]
                nzb = [i for i, v in enumerate(E[k - j]) if not v.is_zero()]
                scatter_acc(acc, sup[k], cj, vjj, sup[k - j][nzb], [E[k - j][i] for i in nzb], chunk)
            E.append([a / k for a in acc])
        am = AllMom2A(Gam, n, Dc, groups=self.groups, caps=self.caps, chunk=chunk)
        Mser = []
        for k in range(Dc + 1):
            acc = [arb(0) for _ in range(len(sup[k]))]
            for j in range(0, k + 1):
                cj = am.codes[j]
                exj = am.decode(cj)
                vj = []
                for i in range(len(cj)):
                    f = 1
                    for x in exj[i]:
                        f *= math.factorial(int(x))
                    vj.append(am.mom[j][i] / f)
                nzb = [i for i, v in enumerate(E[k - j]) if not v.is_zero()]
                scatter_acc(acc, sup[k], cj, vj, sup[k - j][nzb], [E[k - j][i] for i in nzb], chunk)
            Mser.append(acc)
        self.table = {}
        for k in range(Dc + 1):
            u = sup[k]
            keep = [i for i in range(len(u)) if not Mser[k][i].is_zero()]
            if not keep:
                continue
            uk = u[keep]
            spart, gpart = uk % BF, uk // BF
            order = np.argsort(spart, kind='stable')
            spart, gpart = spart[order], gpart[order]
            vals = [Mser[k][keep[i]] for i in order.tolist()]
            bounds = np.flatnonzero(np.diff(spart)) + 1
            starts = np.concatenate([[0], bounds]).astype(int)
            ends = np.concatenate([bounds, [len(spart)]]).astype(int)
            for a0, a1 in zip(starts.tolist(), ends.tolist()):
                e = tuple(int(x) for x in self.decode_s(int(spart[a0])))
                ef = 1
                for x in e:
                    ef *= math.factorial(x)
                gd = self.decode_g_arr(gpart[a0:a1])
                self.table[e] = {tuple(int(x) for x in row): vals[a0 + i] * ef for i, row in enumerate(gd)}

    def s_ok(self, c):
        if not self.caps:
            return np.ones(len(c), dtype=bool)
        ex = np.stack([(c // self.pw[f]) % self.B for f in range(self.F)], axis=1)
        good = np.ones(len(c), dtype=bool)
        for g, cap in self.caps.items():
            good &= ex[:, self.groups == g].sum(axis=1) <= cap
        return good

    def decode_s(self, c):
        return [(c // self.B ** f) % self.B for f in range(self.F)]

    def decode_g_arr(self, cs):
        return np.stack([(cs // self.B ** j) % self.B for j in range(self.NG)], axis=1)

    def cond(self, e):
        e = tuple(e)
        if sum(e) == 0:
            return {tuple([0] * self.NG): arb(1)}
        return self.table.get(e, {})


# ------------------------------------------------------------------ CondG and GSpace (condg)
class GSpace:
    def __init__(self, D):
        self.D, self.B = D, D + 1
        self.pw = np.array([self.B ** i for i in range(6)], dtype=np.int64)
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            codes.append(np.unique((codes[-1][:, None] + self.pw[None, :]).ravel()))
        self.codes = np.unique(np.concatenate(codes))
        self.n = len(self.codes)
        self.deg = self.decode(self.codes).sum(axis=1)

    def decode(self, c):
        return np.stack([(c // self.pw[i]) % self.B for i in range(6)], axis=1)

    def code(self, e):
        return int(sum(int(x) * int(p) for x, p in zip(e, self.pw)))

    def index(self, cs):
        idx = np.searchsorted(self.codes, cs)
        assert np.all(idx < self.n) and np.array_equal(self.codes[idx], cs)
        return idx

    def to_dict(self, v):
        ex = self.decode(self.codes)
        return {tuple(int(x) for x in ex[i]): v[i] for i in range(self.n) if not v[i].is_zero()}

    def from_dict(self, P):
        v = [arb(0) for _ in range(self.n)]
        if P:
            ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, 6)
            idx = self.index(ex @ self.pw).tolist()
            for i, c in zip(idx, P.values()):
                v[i] += A(c)
        return v


class CondGA:
    def __init__(self, cm, Dout):
        self.cm = cm
        self.tab = GSpace(cm.Dc)
        self.out = GSpace(Dout)
        self.vec = {}
        for e2, poly in cm.table.items():
            self.vec[e2] = self.tab.from_dict(poly)
        self.vec[tuple([0] * cm.F)] = self.tab.from_dict({tuple([0] * 6): arb(1)})
        self._sh = {}

    def shift(self, eg):
        if eg not in self._sh:
            d = sum(eg)
            src = np.flatnonzero(self.tab.deg + d <= self.out.D)
            ex = self.tab.decode(self.tab.codes[src]) + np.array(eg)[None, :]
            dst = self.out.index(ex @ self.out.pw)
            self._sh[eg] = (src.tolist(), dst.tolist())
        return self._sh[eg]

    def condE(self, P12):
        """condg.CondG.condE in balls: P12 {12-tuple (sigma X 0-2, sigma Q 3-5 zero, sigma'' 6-11): ball} -> list of balls over g-monomials."""
        res = [arb(0) for _ in range(self.out.n)]
        XG = {0: 0, 1: 3, 2: 5}
        for e, c in P12.items():
            assert e[3] == e[4] == e[5] == 0, "sigma Q-forms not expected"
            eg = [0] * 6
            for r in range(3):
                eg[XG[r]] = e[r]
            src, dst = self.shift(tuple(eg))
            v = self.vec.get(tuple(e[6:]))
            if v is None:
                raise KeyError(tuple(e[6:]))
            cc = A(c)
            for s_, d_ in zip(src, dst):
                if not v[s_].is_zero():
                    res[d_] += cc * v[s_]
        return res


# ------------------------------------------------------------------ Wishart (wishart)
class WishartA:
    """wishart.Wishart in balls: moments of the Gram matrix of n i.i.d. N(0, G) vectors; G an arb_mat m x m."""
    def __init__(self, G, n, D, chunk=4000000):
        m = G.nrows()
        self.vars = [(r, s) for r in range(m) for s in range(r, m)]
        F = len(self.vars)
        self.F, self.D, self.n, self.chunk = F, D, n, chunk
        B = D + 1
        assert float(B) ** F < 9.0e18
        self.B = B
        self.pw = np.array([B ** i for i in range(F)], dtype=np.int64)

        def var(i, c):
            e = [0] * F
            e[i] = 1
            return {tuple(e): c}
        Sm = [[{} for _ in range(m)] for _ in range(m)]
        half = arb(1) / 2
        for i, (r, s) in enumerate(self.vars):
            if r == s:
                Sm[r][r] = var(i, arb(1))
            else:
                Sm[r][s] = var(i, half)
                Sm[s][r] = var(i, half)
        zero = tuple([0] * F)
        Mx = [[padd({zero: arb(1)} if r == s else {}, *[{e: -2 * c * G[k, s] for e, c in Sm[r][k].items()} for k in range(m)])
               for s in range(m)] for r in range(m)]
        det = {}
        for perm in itertools.permutations(range(m)):
            inv = sum(1 for a_ in range(m) for b_ in range(a_ + 1, m) if perm[a_] > perm[b_])
            term = {zero: arb(-1 if inv % 2 else 1)}
            for r in range(m):
                term = pmul(term, Mx[r][perm[r]])
            det = padd(det, term)
        Dj = {}
        for e, c in det.items():
            Dj.setdefault(sum(e), []).append((e, c))
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            codes.append(np.unique((codes[-1][:, None] + self.pw[None, :]).ravel()))
        self.codes = codes
        Dc = {j: (np.array([sum(int(x) * int(p) for x, p in zip(e, self.pw)) for e, c in lst], dtype=np.int64), [c for e, c in lst])
              for j, lst in Dj.items() if j > 0}
        M = [[arb(1)]] + [None] * D
        half_n = arb(n) / 2
        for k in range(1, D + 1):
            acc = [arb(0) for _ in range(len(codes[k]))]
            for j, (cj, vj) in Dc.items():
                if j > k:
                    continue
                coef = (1 - half_n) * j - k
                part = [arb(0) for _ in range(len(codes[k]))]
                scatter_acc(part, codes[k], cj, vj, codes[k - j], M[k - j], chunk)
                for i in range(len(acc)):
                    acc[i] += coef * part[i]
            M[k] = [a / k for a in acc]
        self.mom = []
        for d in range(D + 1):
            ex = self.decode(codes[d])
            row = []
            for i in range(len(codes[d])):
                f = 1
                for x in ex[i]:
                    f *= math.factorial(int(x))
                row.append(M[d][i] * f)
            self.mom.append(row)

    def decode(self, c):
        return np.stack([(c // self.pw[i]) % self.B for i in range(self.F)], axis=1)

    def index(self, k, cs):
        idx = np.searchsorted(self.codes[k], cs)
        assert np.all(idx < len(self.codes[k])) and np.array_equal(self.codes[k][idx], cs)
        return idx

    def E(self, P):
        if not P:
            return arb(0)
        ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, self.F)
        deg, cs, co = ex.sum(axis=1), ex @ self.pw, [A(v) for v in P.values()]
        assert deg.max() <= self.D
        tot = arb(0)
        for d in np.unique(deg):
            sel = np.flatnonzero(deg == d)
            idx = self.index(int(d), cs[sel]).tolist()
            m = self.mom[int(d)]
            for a_, i in zip(sel.tolist(), idx):
                tot += co[a_] * m[i]
        return tot

    def E2(self, P, Q):
        ex1 = np.array(list(P.keys()), dtype=np.int64).reshape(-1, self.F)
        c1 = [A(v) for v in P.values()]
        ex2 = np.array(list(Q.keys()), dtype=np.int64).reshape(-1, self.F)
        c2 = [A(v) for v in Q.values()]
        d1, d2 = ex1.sum(axis=1), ex2.sum(axis=1)
        k1, k2 = ex1 @ self.pw, ex2 @ self.pw
        tot = arb(0)
        for a_ in np.unique(d1):
            s1 = np.flatnonzero(d1 == a_)
            for b_ in np.unique(d2):
                s2 = np.flatnonzero(d2 == b_)
                k = int(a_ + b_)
                assert k <= self.D
                tot += dot_pairs(k1[s1], [c1[i] for i in s1], k2[s2], [c2[i] for i in s2], lambda cs, k=k: self.index(k, cs), self.mom[k],
                                 self.chunk)
        return tot


# ------------------------------------------------------------------ NPoly (npoly) with ball coefficients
class NPolyA:
    """npoly.NPoly with ball coefficients (codes in base B as npoly)."""
    def __init__(self, nv, B, codes=None, coeffs=None):
        self.nv, self.B = nv, B
        self.pw = np.array([B ** i for i in range(nv)], dtype=np.int64)
        self.codes = np.zeros(0, dtype=np.int64) if codes is None else np.asarray(codes, dtype=np.int64)
        self.coeffs = [] if coeffs is None else [A(c) for c in coeffs]

    @classmethod
    def from_dict(cls, P, nv, B):
        p = cls(nv, B)
        if P:
            ex = np.array(list(P.keys()), dtype=np.int64).reshape(-1, nv)
            assert ex.max() < B
            p.codes = ex @ p.pw
            p.coeffs = [A(v) for v in P.values()]
            p._normalize()
        return p

    def _normalize(self):
        if len(self.codes):
            u, inv = np.unique(self.codes, return_inverse=True)
            c = [arb(0) for _ in range(len(u))]
            for i, v in zip(inv.tolist(), self.coeffs):
                c[i] += v
            keep = [i for i in range(len(u)) if not c[i].is_zero()]
            self.codes, self.coeffs = u[keep], [c[i] for i in keep]

    def degrees(self):
        return np.stack([(self.codes // self.pw[i]) % self.B for i in range(self.nv)], axis=1).sum(axis=1) if len(self.codes) else np.zeros(0, dtype=np.int64)

    def exponents(self):
        return np.stack([(self.codes // self.pw[i]) % self.B for i in range(self.nv)], axis=1) if len(self.codes) else np.zeros((0, self.nv), dtype=np.int64)

    def mul(self, o):
        out = NPolyA(self.nv, self.B)
        if len(self.codes) == 0 or len(o.codes) == 0:
            return out
        assert np.all(self.exponents().max(axis=0) + o.exponents().max(axis=0) < self.B), 'NPoly exponent overflow'
        cc = (self.codes[:, None] + o.codes[None, :]).ravel()
        u, inv = np.unique(cc, return_inverse=True)
        c = [arb(0) for _ in range(len(u))]
        inv = inv.tolist()
        k = 0
        for a_ in self.coeffs:
            for b_ in o.coeffs:
                c[inv[k]] += a_ * b_
                k += 1
        out.codes = u
        out.coeffs = c
        out._normalize()
        return out

    def power(self, k):
        res = NPolyA(self.nv, self.B, np.zeros(1, dtype=np.int64), [arb(1)])
        base = self
        while k > 0:
            if k & 1:
                res = res.mul(base)
            k >>= 1
            if k:
                base = base.mul(base)
        return res

    def scale(self, s):
        s = A(s)
        return NPolyA(self.nv, self.B, self.codes.copy(), [c * s for c in self.coeffs])

    def add(self, o):
        out = NPolyA(self.nv, self.B, np.concatenate([self.codes, o.codes]), self.coeffs + o.coeffs)
        out._normalize()
        return out

    def to_dict(self):
        ex = self.exponents()
        return {tuple(int(x) for x in row): c for row, c in zip(ex, self.coeffs)}

    def project(self, idx):
        """keep only variables idx (None if another variable has a positive exponent), as npoly.NPoly.project."""
        ex = self.exponents()
        other = [i for i in range(self.nv) if i not in idx]
        if len(self.codes) and other and ex[:, other].max() > 0:
            return None
        p = NPolyA(len(idx), self.B)
        p.codes = ex[:, idx] @ p.pw if len(self.codes) else np.zeros(0, dtype=np.int64)
        p.coeffs = list(self.coeffs)
        p._normalize()
        return p
