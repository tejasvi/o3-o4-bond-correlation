#!/usr/bin/env python3
# pk10 (code): condexp with dense accumulation on precomputed supports (memory-safe) and optional degree caps on groups of forms.
#   phi2 = Mmat phi1 + zeta, zeta ~ N(0, Cmat) (x) I_n;  Q_f = |W[:,f]^T phi2|^2;  E[exp(sum s_f Q_f) | phi1]
#   = det(I - 2 S Gam)^{-n/2} exp(tr[(I - 2 S Gam)^{-1} S P g P^T]),  g = Gram of phi1.  Caps truncate s-monomials (ring quotient).
import math
import numpy as np
from amom2b import AllMom2


class CondMom:
    def __init__(self, Mmat, Cmat, W, n, Dc, groups=None, caps=None, chunk=4000000):
        Mmat, Cmat, W = (np.asarray(x, dtype=float) for x in (Mmat, Cmat, W))
        F = W.shape[1]
        n1 = Mmat.shape[1]
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
        P = W.T @ Mmat
        Gam = W.T @ Cmat @ W
        sc = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            c = np.unique((sc[-1][:, None] + self.pw[None, :F]).ravel())
            sc.append(c[self.s_ok(c)])
        self.sc = sc
        gc = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            gc.append(np.unique((gc[-1][:, None] + self.pw[None, F:]).ravel()))
        gle = [np.unique(np.concatenate(gc[:d + 1])) for d in range(Dc + 1)]      # g-codes of degree <= d
        sup = [np.sort((sc[k][:, None] + gle[k][None, :]).ravel()) for k in range(Dc + 1)]
        self.sup = sup
        # exponent Y: s-degree d part, linear in g
        Y = [None] * (Dc + 1)
        sfull = [np.zeros(1, dtype=np.int64)]
        for d in range(1, Dc + 1):
            sfull.append(np.unique((sfull[-1][:, None] + self.pw[None, :F]).ravel()))
        Sk = np.zeros((len(sfull[1]), F, F))
        for f in range(F):
            Sk[np.searchsorted(sfull[1], self.pw[f]), f, f] = 1.0
        for k in range(0, Dc):
            d = k + 1
            X = (2.0 ** k) * np.einsum('fr,mfg,gs->mrs', P, Sk, P)
            codes, vals = [], []
            for gi, (r, s) in enumerate(self.gvars):
                v = X[:, r, r] if r == s else X[:, r, s] + X[:, s, r]
                codes.append(sfull[d] + self.pw[F + gi]); vals.append(v)
            codes = np.concatenate(codes); vals = np.concatenate(vals)
            keep = (vals != 0.0) & self.s_ok(codes % BF)
            Y[d] = (codes[keep], vals[keep])
            if d < Dc:
                new = np.zeros((len(sfull[d + 1]), F, F))
                GS = np.einsum('fh,mhg->mfg', Gam, Sk)
                for f in range(F):
                    idx = np.searchsorted(sfull[d + 1], sfull[d] + self.pw[f])
                    new[idx, f, :] += GS[:, f, :]
                Sk = new
        E = [np.ones(1)]
        for k in range(1, Dc + 1):
            acc = np.zeros(len(sup[k]))
            for j in range(1, k + 1):
                cj, vj = Y[j]
                if len(cj) == 0:
                    continue
                self._acc(acc, sup[k], cj, j * vj, sup[k - j], E[k - j], chunk)
            E.append(acc / k)
        am = AllMom2(Cmat, n, Dc, W=W, groups=self.groups, caps=self.caps)
        fact = np.array([math.factorial(i) for i in range(Dc + 1)], dtype=float)
        Mser = []
        for k in range(Dc + 1):
            acc = np.zeros(len(sup[k]))
            for j in range(0, k + 1):
                cj = am.codes[j]
                vj = am.mom[j] / np.prod(fact[am.decode(am.codes[j])], axis=1)
                self._acc(acc, sup[k], cj, vj, sup[k - j], E[k - j], chunk)
            Mser.append(acc)
        self.table = {}
        for k in range(Dc + 1):
            u, v = sup[k], Mser[k]
            nz = v != 0.0
            u, v = u[nz], v[nz]
            spart, gpart = u % BF, u // BF
            order = np.argsort(spart, kind='stable')
            spart, gpart, v = spart[order], gpart[order], v[order]
            if len(spart) == 0:
                continue
            bounds = np.flatnonzero(np.diff(spart)) + 1
            starts = np.concatenate([[0], bounds]); ends = np.concatenate([bounds, [len(spart)]])
            for a0, a1 in zip(starts, ends):
                e = tuple(int(x) for x in self.decode_s(int(spart[a0])))
                ef = float(np.prod([math.factorial(x) for x in e]))
                gd = self.decode_g_arr(gpart[a0:a1])
                self.table[e] = {tuple(int(x) for x in row): ef * float(val) for row, val in zip(gd, v[a0:a1])}

    def s_ok(self, c):
        if not self.caps:
            return np.ones(len(c), dtype=bool)
        ex = np.stack([(c // self.pw[f]) % self.B for f in range(self.F)], axis=1)
        good = np.ones(len(c), dtype=bool)
        for g, cap in self.caps.items():
            good &= ex[:, self.groups == g].sum(axis=1) <= cap
        return good

    @staticmethod
    def _acc(acc, supk, ca, va, cb_sup, vb, chunk):
        nzb = vb != 0.0
        cb, vb = cb_sup[nzb], vb[nzb]
        if len(cb) == 0 or len(ca) == 0:
            return
        rows = max(1, chunk // len(cb))
        for s0 in range(0, len(ca), rows):
            cs = (ca[s0:s0 + rows, None] + cb[None, :]).ravel()
            w = (va[s0:s0 + rows, None] * vb[None, :]).ravel()
            idx = np.searchsorted(supk, cs)
            idx[idx >= len(supk)] = 0
            hit = supk[idx] == cs
            acc += np.bincount(idx[hit], weights=w[hit], minlength=len(acc))

    def decode_s(self, c):
        return [(c // self.B ** f) % self.B for f in range(self.F)]

    def decode_g_arr(self, cs):
        return np.stack([(cs // self.B ** j) % self.B for j in range(self.NG)], axis=1)

    def cond(self, e):
        e = tuple(e)
        if sum(e) == 0:
            return {tuple([0] * self.NG): 1.0}
        return self.table.get(e, {})
