#!/usr/bin/env python3
# cs30_ks1_probe.py (pk05): kill test K-S1 of SCOPE_P0_STRIP_COVER_v1 (d21ebce9) section 3(b). Float DATA, not a certificate.
# Singlet column transfer of the uniform 3 x n strip (rows top/mid/bottom), N in {3, 4}, in the hub-frame basis |l1, l3, m> (each column's
# middle spin is the axis): T = V^{1/2} H V^{1/2}, V^{1/2} = (+)_m exp(beta X^(m)/2) (x) exp(beta X^(m)/2) on (l1, l3); H = Q diag(a_l1 a_l3
# a_l2) Q^T, Q = eigenvectors of the diagonal O(N) Casimir C on each (l1, l3) block (tridiagonal in m), eigenvalues l2(l2+N-2),
# l1 + l2 + l3 even. Edge insertions: vertical = X^(m) on l1 (tv) or l3 (bv); horizontal = a_l -> a_l g_l on l1 (th), l2 (mh), l3 (bh),
# g_l = I_{l+lam+1}/I_{l+lam} + l/beta. Bulk (infinite strip): Omega_v = X, Omega_h = V^{1/2} H_e V^{1/2}/lam1;
# Cov(e, f; k) = <Omega_e psi1, (P T/lam1)^k P Omega_f psi1>, P = 1 - |psi1><psi1| (no cancellation).
# READINGS (fixed before any run):
#  R1 per (N, beta): lam_s/lam1 and top-bottom parity (l1 <-> l3) for s = 2..6.
#  R2 per (N, beta): for the leading reflection-even mode s* (largest lam_s, even parity): c_e = <psi_s*, Omega_e psi1> for e = th, mh,
#     tv; c_mh/c_th, beta c_mh/c_th, sign(c_mh c_th), sign(c_mh c_tv). Also lam and c_th for the leading odd mode.
#  R3 per (N, beta): Cov(e, f; k), k = 3..12, for (mh, th), (mh, tv), (th, bh), (tv, bv).
#  KILL-CAND if sign(c_mh c_th) < 0 or sign(c_mh c_tv) < 0 at any (N, beta), or any R3 value < -tol_k with
#     tol_k = 1e-9 |P Omega_e psi1| |P Omega_f psi1| (lam2/lam1)^k. Else PASS. DATA: the trend of beta c_mh/c_th over beta.
#  Grid: beta in (20, 40, 80) first, then (30, 60, 120); L = ceil(sqrt(56 beta)); both N.
# CONTROLS (any failure: VOID): CAS (every block's eigenvalues equal l2(l2+N-2) to 1e-9 relative), MF-CAS (a planted 1% error in one
#  off-diagonal must fail CAS: must fire), ONECOL (n = 1: <sigma1.sigma2> = I_{lam+1}/I_lam to 1e-12), BOX (n = 3: <th>, <mh>, <tv> agree
#  with route H's hub trace sum_m D_m tr(E W E W E W E W) to 1e-8 relative at beta = 20), LCONV (beta = 40 at L + 8: lam2/lam1 and c_mh/c_th
#  change < 1e-6 relative).
# Usage: cs30_ks1_probe.py CAP_S
import sys
import time
import hashlib
import numpy as np
from scipy.special import ive
from scipy.linalg import eigh_tridiagonal
from scipy.sparse.linalg import LinearOperator, eigsh

T0 = time.process_time()
CAP_S = float(sys.argv[1])
PAD = 24


def guard():
    if time.process_time() > CAP_S - 4.0:
        print('CAP-STOP at %.1f s' % time.process_time(), flush=True)
        sys.exit(3)


def xoff(N, m, ls):
    # off-diagonal of X^(m) between l and l+1, l in ls (l >= m): sqrt((l-m+1)(l+m+N-2)/((2l+N-2)(2l+N)))
    ls = np.asarray(ls, dtype=np.float64)
    return np.sqrt((ls - m + 1.0) * (ls + m + N - 2.0) / ((2.0 * ls + N - 2.0) * (2.0 * ls + N)))


def bessel(N, beta, lmax):
    lam = (N - 2) / 2.0
    ls = np.arange(lmax + 2, dtype=np.float64)
    iv = ive(ls + lam, beta)
    a = iv[:lmax + 1] / iv[0]
    g = iv[1:lmax + 2] / iv[:lmax + 1] + ls[:lmax + 1] / beta
    return a, g


def cas_block(N, l1, l3, plant=False):
    s = min(l1, l3) + 1
    m = np.arange(s, dtype=np.float64)
    if N == 3:
        d = l1 * (l1 + 1.0) + l3 * (l3 + 1.0) - 2.0 * m * m
        mm = m[:-1]
        e = np.sqrt((l1 - mm) * (l1 + mm + 1.0) * (l3 - mm) * (l3 + mm + 1.0))
        if s > 1:
            e[0] *= np.sqrt(2.0)
    else:
        d = l1 * (l1 + 2.0) + l3 * (l3 + 2.0) - 2.0 * m * (m + 1.0)
        mm = m[:-1]
        e = 2.0 * (mm + 1.0) * np.sqrt(((l1 + 1.0) ** 2 - (mm + 1.0) ** 2) * ((l3 + 1.0) ** 2 - (mm + 1.0) ** 2)) / np.sqrt((2.0 * mm + 1.0) * (2.0 * mm + 3.0))
    if plant and s > 1:
        e = e.copy()
        e[-1] *= 1.01
    return d, e


class Strip:
    def __init__(self, N, beta, L):
        self.N, self.beta, self.L = N, beta, L
        self.a, self.g = bessel(N, beta, 2 * L + 2)
        self.Eh, self.X = [], []
        for m in range(L + 1):
            n = L + PAD + 1 - m
            off = xoff(N, m, np.arange(m, m + n - 1))
            w, U = eigh_tridiagonal(np.zeros(n), off)
            E = (U * np.exp(0.5 * beta * (w - 1.0))) @ U.T
            k = L + 1 - m
            self.Eh.append(E[:k, :k].copy())
            self.X.append(np.diag(off[:k - 1], 1) + np.diag(off[:k - 1], -1))
        self.groups = []
        self.casmax = 0.0
        for s in range(1, L + 2):
            pairs = [(l1, l3) for l1 in range(L + 1) for l3 in range(L + 1) if min(l1, l3) == s - 1]
            Qs, l2s = [], []
            for (l1, l3) in pairs:
                d, e = cas_block(N, l1, l3)
                w, U = eigh_tridiagonal(d, e) if s > 1 else (d.copy(), np.ones((1, 1)))
                l2 = abs(l1 - l3) + 2 * np.arange(s)
                want = l2 * (l2 + N - 2.0)
                self.casmax = max(self.casmax, float(np.max(np.abs(w - want) / np.maximum(want, 1.0))))
                Qs.append(U)
                l2s.append(l2)
            i1 = np.array([p[0] for p in pairs])
            i3 = np.array([p[1] for p in pairs])
            self.groups.append((s, i1, i3, np.array(Qs), np.array(l2s)))
        self.mask = np.zeros((L + 1,) * 3)
        for l1 in range(L + 1):
            for l3 in range(L + 1):
                self.mask[l1, l3, :min(l1, l3) + 1] = 1.0

    def vhalf(self, A):
        B = np.zeros_like(A)
        for m in range(self.L + 1):
            E = self.Eh[m]
            B[m:, m:, m] = E @ A[m:, m:, m] @ E.T
        return B

    def xop(self, A, side):
        B = np.zeros_like(A)
        for m in range(self.L + 1):
            X = self.X[m]
            B[m:, m:, m] = X @ A[m:, m:, m] if side == 1 else A[m:, m:, m] @ X.T
        return B

    def hop(self, A, ins=None):
        B = np.zeros_like(A)
        a, g = self.a, self.g
        for (s, i1, i3, Q, l2) in self.groups:
            x = A[i1, i3, :s]
            y = np.einsum('pij,pi->pj', Q, x)
            dd = a[i1][:, None] * a[i3][:, None] * a[l2]
            if ins == 'th':
                dd = dd * g[i1][:, None]
            elif ins == 'bh':
                dd = dd * g[i3][:, None]
            elif ins == 'mh':
                dd = dd * g[l2]
            B[i1, i3, :s] = np.einsum('pij,pj->pi', Q, y * dd)
        return B

    def tmat(self, A, ins=None):
        return self.vhalf(self.hop(self.vhalf(A), ins))

    def omega(self, A, e, lam1):
        if e == 'tv':
            return self.xop(A, 1)
        if e == 'bv':
            return self.xop(A, 3)
        return self.tmat(A, e) / lam1

    def parity(self, A):
        return float(np.sum(A * np.transpose(A, (1, 0, 2))) / np.sum(A * A))


def hubtrace_box(N, beta, L):
    # route H's 3x3 box: Z = sum_m D_m tr(E_N W E_E W E_S W E_W W); <th> = ring edge NW-N, <mh> = spoke W, <tv> = spoke N
    a, g = bessel(N, beta, L + PAD + 2)
    z = np.zeros(4)
    for m in range(L + 1):
        n = L + PAD + 1 - m
        off = xoff(N, m, np.arange(m, m + n - 1))
        w, U = eigh_tridiagonal(np.zeros(n), off)
        E = (U * np.exp(beta * (w - 1.0))) @ U.T
        X = np.diag(off, 1) + np.diag(off, -1)
        ls = np.arange(m, m + n)
        W, Wg = np.diag(a[ls] ** 2), np.diag(a[ls] ** 2 * g[ls])
        Dm = (1.0 if m == 0 else 2.0) if N == 3 else 2.0 * m + 1.0
        EW = E @ W
        R = EW @ EW @ EW
        z += Dm * np.array([np.trace(R @ EW), np.trace(R @ E @ Wg), np.trace(R @ X @ E @ W), np.trace(X @ E @ W @ R)])
    return z[1] / z[0], z[2] / z[0], z[3] / z[0]


def e0vec(S):
    A = np.zeros((S.L + 1,) * 3)
    A[0, 0, 0] = 1.0
    return S.vhalf(A)


def spectrum(S, k=6):
    shp = (S.L + 1,) * 3
    n = (S.L + 1) ** 3
    op = LinearOperator((n, n), matvec=lambda x: S.tmat(x.reshape(shp)).ravel(), dtype=np.float64)
    vals, vecs = eigsh(op, k=k, which='LA', v0=e0vec(S).ravel(), tol=1e-10, ncv=32)
    o = np.argsort(vals)[::-1]
    psi = [vecs[:, i].reshape(shp) for i in o]
    if psi[0][0, 0, 0] < 0:
        psi[0] = -psi[0]
    return vals[o], psi


def analyze(N, beta, L):
    t1 = time.process_time()
    S = Strip(N, beta, L)
    lam, psi = spectrum(S)
    p1 = psi[0]
    par = [S.parity(p) for p in psi]
    ev = [s for s in range(1, len(psi)) if par[s] > 0.5]
    od = [s for s in range(1, len(psi)) if par[s] < -0.5]
    om = {e: S.omega(p1, e, lam[0]) for e in ('th', 'mh', 'bh', 'tv', 'bv')}
    out = {'N': N, 'beta': beta, 'L': L, 'lam': lam / lam[0], 'par': par, 'cas': S.casmax}
    if ev:
        se = ev[0]
        c = {e: float(np.sum(psi[se] * om[e])) for e in om}
        out.update(se=se, c=c, rmt=c['mh'] / c['th'], kill=(c['mh'] * c['th'] < 0) or (c['mh'] * c['tv'] < 0))
    if od:
        out.update(so=od[0], cth_odd=float(np.sum(psi[od[0]] * om['th'])))
    covs, negs = {}, []
    rho = lam[1] / lam[0]
    for (e, f) in (('mh', 'th'), ('mh', 'tv'), ('th', 'bh'), ('tv', 'bv')):
        we = om[e] - np.sum(om[e] * p1) * p1
        w = om[f] - np.sum(om[f] * p1) * p1
        ne, nf = np.sqrt(np.sum(we * we)), np.sqrt(np.sum(w * w))
        vals = []
        for k in range(1, 13):
            w = S.tmat(w) / lam[0]
            w = w - np.sum(w * p1) * p1
            if k >= 3:
                cv = float(np.sum(we * w))
                vals.append(cv)
                if cv < -1e-9 * ne * nf * rho ** k:
                    negs.append((e, f, k, cv))
        covs[(e, f)] = vals
    out.update(covs=covs, negs=negs, sec=time.process_time() - t1)
    return out


def main():
    with open(__file__, 'rb') as fh:
        print('SELF sha256 %s' % hashlib.sha256(fh.read()).hexdigest())
    print('cs30_ks1_probe CAP_S %.0f PAD %d' % (CAP_S, PAD), flush=True)
    ok = True
    for N in (3, 4):
        d, e = cas_block(N, 12, 9, plant=True)
        w = eigh_tridiagonal(d, e)[0]
        l2 = 3 + 2 * np.arange(10)
        dev = float(np.max(np.abs(w - l2 * (l2 + N - 2.0)) / np.maximum(l2 * (l2 + N - 2.0), 1.0)))
        print('CONTROL MF-CAS N=%d: planted 1%% off-diagonal error gives deviation %.3e (must exceed 1e-6): %s' % (N, dev, 'FIRED' if dev > 1e-6 else 'NOT FIRED'))
        ok = ok and dev > 1e-6
        S = Strip(N, 20.0, 34)
        v = e0vec(S)
        one = float(np.sum(v * S.xop(v, 1)) / np.sum(v * v))
        lam = (N - 2) / 2.0
        ref = ive(lam + 1.0, 20.0) / ive(lam, 20.0)
        print('CONTROL ONECOL N=%d beta=20: <s1.s2> %.15f vs I ratio %.15f, rel %.2e (gate 1e-12): %s' % (N, one, ref, abs(one / ref - 1), 'PASS' if abs(one / ref - 1) < 1e-12 else 'FAIL'))
        ok = ok and abs(one / ref - 1) < 1e-12
        Tv = S.tmat(v)
        z = np.sum(v * S.tmat(Tv))
        st = (np.sum(v * S.tmat(Tv, 'th')) / z, np.sum(v * S.tmat(Tv, 'mh')) / z, np.sum(v * S.tmat(S.xop(Tv, 1))) / z)
        hb = hubtrace_box(N, 20.0, 34)
        rel = max(abs(st[i] / hb[i] - 1) for i in range(3))
        print('CONTROL BOX N=%d beta=20: strip n=3 (th, mh, tv) = (%.12f, %.12f, %.12f), hub trace (%.12f, %.12f, %.12f), max rel %.2e (gate 1e-8): %s' % (
            N, st[0], st[1], st[2], hb[0], hb[1], hb[2], rel, 'PASS' if rel < 1e-8 else 'FAIL'), flush=True)
        ok = ok and rel < 1e-8
    res, kills = [], []
    for beta in (20.0, 40.0, 80.0, 30.0, 60.0, 120.0):
        for N in (3, 4):
            guard()
            L = int(np.ceil(np.sqrt(56.0 * beta)))
            r = analyze(N, beta, L)
            res.append(r)
            ok = ok and r['cas'] < 1e-9
            print('RUN N=%d beta=%g L=%d (%.1f s): CAS %.1e | lam_s/lam1 s=2..6: %s | parity: %s' % (N, beta, L, r['sec'], r['cas'],
                  ' '.join('%.5f' % x for x in r['lam'][1:]), ' '.join('%+.2f' % x for x in r['par'][1:])))
            if 'c' in r:
                c = r['c']
                print('  even mode s*=%d: c_th %+.6e c_mh %+.6e c_bh %+.6e c_tv %+.6e c_bv %+.6e | c_mh/c_th %+.6e beta*c_mh/c_th %+.5f | %s' % (
                    r['se'] + 1, c['th'], c['mh'], c['bh'], c['tv'], c['bv'], r['rmt'], beta * r['rmt'], 'KILL-CAND' if r['kill'] else 'same sign'))
                if r['kill']:
                    kills.append((N, beta, 'coefficient sign'))
            if 'so' in r:
                print('  odd mode s=%d: lam/lam1 %.5f c_th %+.6e' % (r['so'] + 1, r['lam'][r['so']], r['cth_odd']))
            for (pr, vals) in r['covs'].items():
                print('  Cov%s k=3..12: %s' % (str(pr), ' '.join('%.3e' % x for x in vals)))
            for ng in r['negs']:
                print('  NEGATIVE Cov%s at k=%d: %.3e  KILL-CAND' % ((ng[0], ng[1]), ng[2], ng[3]))
                kills.append((N, beta, 'Cov %s-%s k=%d' % (ng[0], ng[1], ng[2])))
            sys.stdout.flush()
    for N in (3, 4):
        guard()
        L = int(np.ceil(np.sqrt(56.0 * 40.0)))
        r1 = [r for r in res if r['N'] == N and r['beta'] == 40.0][0]
        r2 = analyze(N, 40.0, L + 8)
        d1 = abs(r2['lam'][1] / r1['lam'][1] - 1)
        d2 = abs(r2['rmt'] / r1['rmt'] - 1) if ('rmt' in r1 and 'rmt' in r2) else 1.0
        print('CONTROL LCONV N=%d beta=40: L %d -> %d: lam2/lam1 rel %.2e, c_mh/c_th rel %.2e (gate 1e-6): %s' % (
            N, L, L + 8, d1, d2, 'PASS' if max(d1, d2) < 1e-6 else 'FAIL'))
        ok = ok and max(d1, d2) < 1e-6
    print('TREND beta*c_mh/c_th: %s' % ' '.join('N%d/b%g:%+.4f' % (r['N'], r['beta'], r['beta'] * r['rmt']) for r in res if 'rmt' in r))
    print('KILL-CAND %d: %s' % (len(kills), kills))
    print('READING %s' % ('KILL-CAND' if kills else 'PASS'))
    print('VERDICT %s' % ('VALID' if ok else 'VOID'))
    print('CPU %.2f' % (time.process_time() - T0))


if __name__ == '__main__':
    main()
