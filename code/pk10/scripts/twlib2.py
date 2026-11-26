#!/usr/bin/env python3
# pk10 (code): library for the TWO-column twisted trace tr_H(T^2) = int dg dsigma1 dsigma2 V(1) K(1,2) V(2) K(2, g 1) (O(N)-invariant sector).
# Chart rooted at sigma1_M = e_N; g = r(p) k; scaled variables y = (phi1 = col1 T, phi2 = col1 B, phi3 = col2 T, phi4 = col2 M, phi5 = col2 B, zeta) in (R^n)^6.
# Bonds: col-1 verticals root-1, root-2; horizontals 1-3, root-4, 2-5; col-2 verticals 3-4, 4-5; twisted 3-(g 1), 4-p, 5-(g 2).
# Forms: X1..X5, Z, aT = phi3.zeta, bT = k phi1.zeta, aB = phi5.zeta, bB = k phi2.zeta.
import math
import numpy as np
from twlib import Cj, cm, Ej, cfun, padd, pmul, pscale

FORMS2 = ["X1", "X2", "X3", "X4", "X5", "Z", "aT", "bT", "aB", "bB"]
IX2 = {f: i for i, f in enumerate(FORMS2)}
NF = len(FORMS2)
ROOT_BONDS = ["X1", "X2", "X4"]
PAIR_BONDS = [("X1", "X3"), ("X2", "X5"), ("X3", "X4"), ("X4", "X5"), ("X4", "Z")]
TWISTED = [("X1", "X3", "aT", "bT"), ("X2", "X5", "aB", "bB")]   # (rotated col-1 var, col-2 var, a' = phi'.zeta, b = k phi.zeta)


def m2(**kw):
    e = [0] * NF
    for f, p in kw.items():
        e[IX2[f]] += p
    return tuple(e)


ONE = {tuple([0] * NF): 1.0}


def s_add(a, b):
    return [padd(x, y) for x, y in zip(a, b)]


def s_scale(a, c):
    return [pscale(x, c) for x in a]


def s_mul(a, b, K):
    out = [{} for _ in range(K + 1)]
    for i in range(K + 1):
        for j in range(K + 1 - i):
            if a[i] and b[j]:
                out[i + j] = padd(out[i + j], pmul(a[i], b[j]))
    return out


def s_sqrt1m(var, K):
    """sqrt(1 - t X_var) as a series in t (order K)."""
    out = [dict(ONE)] + [{} for _ in range(K)]
    for m_ in range(1, K + 1):
        out[m_] = {m2(**{var: m_}): -cm(m_)}
    return out


def s_const(P, K):
    return [dict(P)] + [{} for _ in range(K)]


def s_inv1pc(K):
    """1/(1 + c), c = sqrt(1 - t Z):  (1/2) sum_k (w/2)^k with w = 1 - c = sum_{m>=1} cm(m) t^m Z^m."""
    w = [{}] + [{m2(Z=m_): cm(m_)} for m_ in range(1, K + 1)]
    out = s_const({tuple([0] * NF): 0.5}, K)
    pw = s_const(ONE, K)
    for k in range(1, K + 1):
        pw = s_mul(pw, s_scale(w, 0.5), K)
        out = s_add(out, s_scale(pw, 0.5))
    return out


def H_series(K):
    """H = sum_{k=1}^K t^k H_k (list index k), exact series of (exact log-integrand) - f2."""
    KK = K + 1
    H = [{} for _ in range(K + 1)]
    def add_shift(S, extra=None):
        # S = series (order KK) of (bond scalar - 1); contributes S/t + extra (extra = the harmonic X/2 terms, order 0)
        for k in range(1, KK + 1):
            if k - 1 <= K and S[k]:
                H[k - 1] = padd(H[k - 1], S[k])
        if extra:
            H[0] = padd(H[0], extra)
    for v in FORMS2[:6]:                                       # measures: -1/2 log(1 - t X) = sum_m t^m X^m/(2m)
        for m_ in range(1, K + 1):
            H[m_] = padd(H[m_], {m2(**{v: m_}): 1.0 / (2 * m_)})
    for v in ROOT_BONDS:
        S = s_sqrt1m(v, KK); S[0] = {}
        add_shift(S, {m2(**{v: 1}): 0.5})
    for (u, v) in PAIR_BONDS:
        S = s_mul(s_sqrt1m(u, KK), s_sqrt1m(v, KK), KK); S[0] = padd(S[0], pscale(ONE, -1.0))
        add_shift(S, {m2(**{u: 1}): 0.5, m2(**{v: 1}): 0.5})
    for (x, xp, a, b) in TWISTED:
        S = s_mul(s_mul(s_sqrt1m("Z", KK), s_sqrt1m(x, KK), KK), s_sqrt1m(xp, KK), KK); S[0] = padd(S[0], pscale(ONE, -1.0))
        add_shift(S, {m2(**{x: 1}): 0.5, m2(**{xp: 1}): 0.5, m2(Z=1): 0.5})
        ab = {m2(**{a: 1, b: 1}): 1.0}
        inv = s_inv1pc(K)
        for k in range(K):                                    # -t b a' / (1 + c)
            if inv[k]:
                H[k + 1] = padd(H[k + 1], pscale(pmul(ab, inv[k]), -1.0))
        sx = s_sqrt1m(x, K); sxp = s_sqrt1m(xp, K)
        for k in range(1, K + 1):                             # (s - 1) a' - (s' - 1) b
            H[k] = padd(H[k], pmul(sx[k], {m2(**{a: 1}): 1.0}))
            H[k] = padd(H[k], pscale(pmul(sxp[k], {m2(**{b: 1}): 1.0}), -1.0))
    clean = []
    for P in H:
        clean.append({e: c for e, c in P.items() if abs(c) > 1e-15})
    assert not clean[0], clean[0]
    return clean


def mats(k):
    """(Q_k, list of form matrices B_f, Q_nt), y in R^{6n}."""
    n = k.shape[0]; I = np.eye(n); d = 6 * n
    def sel(v):
        S = np.zeros((n, d)); S[:, v * n:(v + 1) * n] = I; return S
    def term(*parts):
        M = sum(c @ sel(v) for v, c in parts)
        return M.T @ M
    Q = (term((0, I)) + term((1, I)) + term((0, I), (2, -I)) + term((3, I)) + term((1, I), (4, -I)) + term((2, I), (3, -I)) + term((3, I), (4, -I))
         + term((2, I), (0, -k), (5, -I)) + term((3, I), (5, -I)) + term((4, I), (1, -k), (5, -I)))
    Qnt = (term((0, I)) + term((1, I)) + term((0, I), (2, -I)) + term((3, I)) + term((1, I), (4, -I)) + term((2, I), (3, -I)) + term((3, I), (4, -I))
           + term((3, I), (5, -I)))
    def blk(i, j, Bm):
        B = np.zeros((d, d)); B[i * n:(i + 1) * n, j * n:(j + 1) * n] += Bm
        if i != j:
            B[j * n:(j + 1) * n, i * n:(i + 1) * n] += Bm.T
        return B
    Bs = [blk(v, v, I) for v in range(6)] + [blk(2, 5, I / 2), blk(0, 5, k.T / 2), blk(4, 5, I / 2), blk(1, 5, k.T / 2)]
    return Q, Bs, Qnt


def tilt2(k, t, av, eps):
    """y^T T y with H(t') <= y^T T y on Omega(av) for t' <= t (av: radii for X1..X5, Z)."""
    n = k.shape[0]; I = np.eye(n); d = 6 * n
    T = np.zeros((d, d))
    for v in range(6):
        T[v * n:(v + 1) * n, v * n:(v + 1) * n] += t * cfun(av[v]) * I
    def sel(v):
        S = np.zeros((n, d)); S[:, v * n:(v + 1) * n] = I; return S
    for (vr, vp) in ((0, 2), (1, 4)):                        # twisted T (rotated phi1, phi3), B (phi2, phi5)
        M = sel(vp) - k @ sel(vr) - sel(5)
        T += eps / 2 * M.T @ M
        a, aZ = av[vr], av[5]
        dk = 1 - math.sqrt(1 - a) + math.sqrt(a * aZ) / (1 + math.sqrt(1 - aZ))
        T[5 * n:, 5 * n:] += (1 / eps - 1) * dk ** 2 / 2 * I
    return T


def hbar2(j, av, t):
    """positive majorant (polynomial in X1..X5, Z) of sup_{t' <= t} |d^j H/dt'^j| on Omega(av), j >= 1."""
    V = FORMS2[:6]
    A = dict(zip(V, av))
    f = math.factorial
    P = {}
    for v in V:                                               # measures
        P = padd(P, {m2(**{v: j}): f(j - 1) / (2 * (1 - A[v]) ** j)})
    for v in ROOT_BONDS:
        P = padd(P, {m2(**{v: j + 1}): Ej(j, A[v])})
    def D2(u, v):
        return padd({m2(**{u: 2}): 1.0}, {m2(**{u: 1, v: 1}): -2.0}, {m2(**{v: 2}): 1.0})
    def Mk(u, v, kk):
        return dict(ONE) if kk == 0 else padd({m2(**{u: kk}): 1.0}, {m2(**{v: kk}): 1.0})
    def Abar(u, v, i):                                        # majorant of |d^i A(X_u, X_v)| (i = 0: |A| <= (t/2) D^2 /(4(1 - a)))
        ae = max(A[u], A[v])
        if i == 0:
            return pscale(D2(u, v), t / 2 / (4 * (1 - ae)))
        return pscale(pmul(D2(u, v), Mk(u, v, i - 1)), 0.5 * f(i) / (4 * (1 - ae) ** (i + 1)))
    def Zbar(i):                                              # majorant of |d^i Zanh|, Zanh = J(c - 1) + Z/2
        if i == 0:
            return {m2(Z=2): t * sum(cm(m_) * A["Z"] ** (m_ - 2) for m_ in range(2, 400))}
        return {m2(Z=i + 1): Ej(i, A["Z"])}
    for (u, v) in PAIR_BONDS:
        P = padd(P, Abar(u, v, j))
    for (x, xp, a, b) in TWISTED:
        # A3 = A(x, xp) + Zanh + t(x + xp)Z/4 - t(x + xp)Zanh/2 - t Z A/2 + t A Zanh
        P = padd(P, Abar(x, xp, j), Zbar(j))
        if j == 1:
            P = padd(P, {m2(**{x: 1, "Z": 1}): 0.25, m2(**{xp: 1, "Z": 1}): 0.25})
        sx = padd({m2(**{x: 1}): 0.5}, {m2(**{xp: 1}): 0.5})
        G1 = lambda i: pmul(sx, Zbar(i))                      # (x + xp) Zanh/2
        G2 = lambda i: pmul({m2(Z=1): 0.5}, Abar(x, xp, i))   # Z A/2
        G3 = lambda i: (lambda acc: acc)(padd(*[pscale(pmul(Abar(x, xp, l), Zbar(i - l)), math.comb(i, l)) for l in range(i + 1)]))
        for G in (G1, G2, G3):
            P = padd(P, pscale(G(j), t), pscale(G(j - 1), j))
        # (s - 1) a': C_j(a_x) X^j (X' + Z)/2 ; -(s' - 1) b: C_j(a_xp) X'^j (X + Z)/2 ; -t b a'/(1+c) = -b a'(1 - c)/Z: (X + X')/2 Z^j C_j(aZ)
        P = padd(P, {m2(**{x: j, xp: 1}): Cj(j, A[x]) / 2, m2(**{x: j, "Z": 1}): Cj(j, A[x]) / 2})
        P = padd(P, {m2(**{xp: j, x: 1}): Cj(j, A[xp]) / 2, m2(**{xp: j, "Z": 1}): Cj(j, A[xp]) / 2})
        P = padd(P, {m2(**{x: 1, "Z": j}): Cj(j, A["Z"]) / 2, m2(**{xp: 1, "Z": j}): Cj(j, A["Z"]) / 2})
    return {e: c for e, c in P.items() if c != 0.0}


def form_values2(y, k):
    Q, Bs, _ = mats(k)
    return np.array([y @ B @ y for B in Bs])


def peval2(P, fv):
    return sum(c * np.prod(fv ** np.array(e)) for e, c in P.items())


def exact_H2_mp(y, k, tp):
    """exact H(t', y) in mpmath from explicit vectors and rotation matrices (independent of the series code)."""
    import mpmath as mp
    n = k.shape[0]; N = n + 1
    tp = mp.mpf(tp)
    ph = [[mp.mpf(float(v)) for v in y[r * n:(r + 1) * n]] for r in range(6)]
    def sph(phv):
        X = sum(x * x for x in phv)
        return [mp.sqrt(tp) * x for x in phv] + [mp.sqrt(1 - tp * X)], X
    sig = [sph(ph[r]) for r in range(5)]
    vv = [mp.sqrt(tp) * x for x in ph[5]]; Z = sum(x * x for x in ph[5]); c = mp.sqrt(1 - tp * Z)
    p = vv + [c]
    eN = [mp.mpf(0)] * n + [mp.mpf(1)]
    dot = lambda u, w: sum(a * b for a, b in zip(u, w))
    vn = mp.sqrt(dot(vv, vv)); vh = [x / vn for x in vv] + [mp.mpf(0)]
    R = mp.eye(N)
    for i in range(N):
        for j_ in range(N):
            R[i, j_] += (c - 1) * (vh[i] * vh[j_] + eN[i] * eN[j_]) + vn * (vh[i] * eN[j_] - eN[i] * vh[j_])
    Kf = mp.eye(N)
    for i in range(n):
        for j_ in range(n):
            Kf[i, j_] = mp.mpf(float(k[i, j_]))
    G = R * Kf
    gv = lambda s: [sum(G[i, j_] * s[j_] for j_ in range(N)) for i in range(N)]
    s1, s2, s3, s4, s5 = [sig[r][0] for r in range(5)]
    bonds = [dot(s1, eN), dot(s2, eN), dot(s1, s3), dot(eN, s4), dot(s2, s5), dot(s3, s4), dot(s4, s5), dot(s3, gv(s1)), dot(s4, p), dot(s5, gv(s2))]
    E = sum((b_ - 1) / tp for b_ in bonds)
    meas = -sum(mp.log(1 - tp * sig[r][1]) for r in range(5)) / 2 - mp.log(1 - tp * Z) / 2
    Q, _, _ = mats(k)
    quad = sum(mp.mpf(float(y[i])) * mp.mpf(float(Q[i, j_])) * mp.mpf(float(y[j_])) for i in range(6 * n) for j_ in range(6 * n))
    return E + meas + quad / 2
