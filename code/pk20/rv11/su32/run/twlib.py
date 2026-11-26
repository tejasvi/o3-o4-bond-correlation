#!/usr/bin/env python3
# pk10 (code): s19.3a library for the one-column twisted trace tr_H(T) (O(N)-invariant sector).
# Chart: root sigma_M = e_N, g = r(p) k (k in O(N-1), p = g e_N), scaled variables y = (phi_T, phi_B, zeta) in (R^n)^3, n = N - 1,
#   sigma_r = (phi_r/sqrt J, s_r), s_r = sqrt(1 - t X_r); p = (zeta/sqrt J, c), c = sqrt(1 - t Z); t = 1/J.
# Integrand e^{f2(y)} e^{H(t, y)}, f2 = -(1/2) y^T Q_k y, H = exact log integrand (5 bonds + sphere/Haar densities) - f2.
import math
import numpy as np

FORMS = ["XT", "XB", "Z", "a2T", "a3T", "a2B", "a3B", "WT", "WB"]
IX = {f: i for i, f in enumerate(FORMS)}


def Cj(j, x):
    """|d^j/dx^j sqrt(1 - x)| = (2j-3)!!/2^j (1-x)^{1/2-j}, j >= 1."""
    df = 1
    for q in range(2 * j - 3, 0, -2):
        df *= q
    return df / 2 ** j * (1 - x) ** (0.5 - j)


def cm(m):
    """sqrt(1 - x) = 1 - sum_{m >= 1} cm(m) x^m."""
    df = 1
    for q in range(2 * m - 3, 0, -2):
        df *= q
    return df / (2 ** m * math.factorial(m))


def Ej(j, x, mmax=2000):
    """sum_{m >= j+1} cm(m) (m-1)!/(m-1-j)! x^{m-1-j}  (majorant constant of the j-th t-derivative of an anharmonic bond term)."""
    return sum(cm(mm) * math.perm(mm - 1, j) * x ** (mm - 1 - j) for mm in range(j + 1, mmax))


def cfun(x):
    return -math.log(1 - x) / (2 * x)


def forms(k):
    d = k.shape[0]
    I = np.eye(d); M = I - k
    def blk(i, j, Bm):
        B = np.zeros((3 * d, 3 * d))
        B[i * d:(i + 1) * d, j * d:(j + 1) * d] += Bm
        if i != j:
            B[j * d:(j + 1) * d, i * d:(i + 1) * d] += Bm.T
        return B
    return [blk(0, 0, I), blk(1, 1, I), blk(2, 2, I), blk(0, 2, I / 2), blk(0, 2, k.T / 2), blk(1, 2, I / 2), blk(1, 2, k.T / 2),
            blk(0, 0, M.T @ M), blk(1, 1, M.T @ M)]


def Qmat(k):
    d = k.shape[0]; I = np.eye(d); M = I - k
    Q = np.zeros((3 * d, 3 * d))
    Q[:d, :d] = I + M.T @ M; Q[d:2 * d, d:2 * d] = I + M.T @ M; Q[2 * d:, 2 * d:] = 3 * I
    Q[:d, 2 * d:] = -M.T; Q[2 * d:, :d] = -M; Q[d:2 * d, 2 * d:] = -M.T; Q[2 * d:, d:2 * d] = -M
    return Q


def mono(**kw):
    e = [0] * len(FORMS)
    for f, p in kw.items():
        e[IX[f]] += p
    return tuple(e)


def padd(*Ps):
    out = {}
    for P in Ps:
        for e, c in P.items():
            out[e] = out.get(e, 0.0) + c
    return out


def pmul(P, Qp):
    out = {}
    for e1, c1 in P.items():
        for e2, c2 in Qp.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            out[e] = out.get(e, 0.0) + c1 * c2
    return out


def pscale(P, s):
    return {e: s * c for e, c in P.items()}


H1 = padd({mono(XT=1): 0.5, mono(XB=1): 0.5, mono(Z=1): 0.5},
          {mono(XT=2): -1 / 8, mono(XB=2): -1 / 8, mono(Z=2): -3 / 8},
          *[{mono(**{"X" + r: 1, "a2" + r: 1}): -0.5, mono(**{"X" + r: 1, "a3" + r: 1}): 0.5, mono(**{"a2" + r: 1, "a3" + r: 1}): -0.5,
             mono(**{"X" + r: 1, "Z": 1}): 0.5} for r in ("T", "B")])


def hbar(j, a, aZ):
    """positive majorant of sup_{t' <= t} |d^j/dt'^j H(t', y)| on Omega = {t X_T <= a, t X_B <= a, t Z <= aZ} (j >= 1)."""
    f = math.factorial(j - 1)
    P = {mono(Z=j): f / (2 * (1 - aZ) ** j), mono(Z=j + 1): 3 * Ej(j, aZ)}
    for r in ("T", "B"):
        X, W = "X" + r, "W" + r
        P = padd(P, {mono(**{X: j}): f / (2 * (1 - a) ** j), mono(**{X: j + 1}): Ej(j, a),
                     mono(**{X: j, W: 1}): Cj(j, a) / 2, mono(**{X: j, "Z": 1}): Cj(j, a) / 2,
                     mono(**{X: 1, "Z": j}): 2 * Cj(j, aZ)})
    return P


def delta_kappa(a, aZ):
    return 1 - math.sqrt(1 - a) + math.sqrt(a * aZ) / (1 + math.sqrt(1 - aZ))


def tilt(k, t, a, aZ, eps):
    """T with H(t', y) <= y^T T y on Omega for all t' <= t:  meas <= t c(a) X, anharmonic bonds <= 0,
    twisted bond r: J(B_r - 1) <= -(1/2)|M phi_r - kappa_r zeta|^2 -> excess <= eps |M phi_r - zeta|^2/2 + (1/eps - 1) delta^2 Z/2."""
    d = k.shape[0]; I = np.eye(d); M = I - k
    k2 = (1 / eps - 1) * delta_kappa(a, aZ) ** 2 / 2
    T = np.zeros((3 * d, 3 * d))
    for r in (0, 1):
        sl = slice(r * d, (r + 1) * d)
        T[sl, sl] = t * cfun(a) * I + eps / 2 * M.T @ M
        T[sl, 2 * d:] = -eps / 2 * M.T
        T[2 * d:, sl] = -eps / 2 * M
    T[2 * d:, 2 * d:] = (t * cfun(aZ) + eps + 2 * k2) * I
    return T


def chernoff(Bm, C, R, ngrid=37):
    """P(y^T B y > R) for y ~ N(0, C), B >= 0:  min_lam e^{-lam R} det(I - 2 lam B C)^{-1/2}."""
    L = np.linalg.cholesky(C)
    ev = np.linalg.eigvalsh(L.T @ Bm @ L)
    best = 1.0
    for frac in np.linspace(0.02, 0.98, ngrid):
        lam = frac / (2 * ev.max())
        val = math.exp(-lam * R - 0.5 * np.sum(np.log1p(-2 * lam * ev)))
        best = min(best, val)
    return best


def form_values(y, k):
    return np.array([y @ B @ y for B in forms(k)])


def peval(P, fv):
    return sum(c * np.prod(fv ** np.array(e)) for e, c in P.items())


def rotz(al):
    c, s = math.cos(al), math.sin(al)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def rot2(al):
    return np.array([[math.cos(al), -math.sin(al)], [math.sin(al), math.cos(al)]])


def nodes(NN, M):
    """class-function quadrature for the stabilizer O(N-1) (N = 3) / SO(3) (N = 4): list of (k, weight); periodic midpoint rule."""
    out = []
    als = [2 * math.pi * (j + 0.5) / M for j in range(M // 2)]
    if NN == 4:
        for al in als:
            out.append((rotz(al), 2 * (1 - math.cos(al)) / M))
    else:
        for al in als:
            out.append((rot2(al), 0.5 * 2.0 / M))
        out.append((np.array([[1.0, 0.0], [0.0, -1.0]]), 0.5))
    return out


def pref(NN):
    import sys
    sys.path.insert(0, "/mnt/g2/release/root/code/pk20/rv11/su32/run")
    from vacmod2 import A_EX, B_EX
    from lapl2 import strip_graph
    def detL(ncols):
        V, Ed = strip_graph(ncols, (A_EX, B_EX))
        L = np.zeros((V, V))
        for (u, v), c in Ed.items():
            L[u, u] += c; L[v, v] += c; L[u, v] -= c; L[v, u] -= c
        return np.prod(np.linalg.eigvalsh(L)[1:]), V
    n = NN - 1
    dN, VN = detL(3); dD, VD = detL(2)
    return (dN / VN) ** (n / 2) / (dD / VD) ** (n / 2)


def far_one(NN, J, a):
    """(J/2pi)^{n/2} int_{outside cap |u|^2 <= a} e^{J(sigma.e_N - 1)} dsigma (surface measure), upper bound; the full integral is <= 1 in these units."""
    e = math.exp(-J * (1 - math.sqrt(1 - a)))
    return math.sqrt(2 * J / math.pi) * e if NN == 4 else e


# second-order Taylor coefficient H2 = (1/2) d^2H/dt^2 at t = 0
H2 = padd({mono(XT=2): 0.25, mono(XB=2): 0.25, mono(Z=2): 0.25},
          {mono(XT=3): -1 / 16, mono(XB=3): -1 / 16, mono(Z=3): -3 / 16},
          *[{mono(**{"X" + r: 2, "a2" + r: 1}): -1 / 8, mono(**{"X" + r: 2, "a3" + r: 1}): 1 / 8,
             mono(**{"a2" + r: 1, "a3" + r: 1, "Z": 1}): -1 / 8, mono(**{"X" + r: 1, "Z": 2}): 1 / 8} for r in ("T", "B")])


def exact_H_mp(y, k, tp):
    """exact H(t', y) in mpmath (closed-form twisted bond, validated against explicit r(p) k matrices in twrig2_check)."""
    import mpmath as mp
    n = k.shape[0]
    tp = mp.mpf(tp)
    ph = [[mp.mpf(float(v)) for v in y[r * n:(r + 1) * n]] for r in range(3)]
    kk = [[mp.mpf(float(k[i, j])) for j in range(n)] for i in range(n)]
    dot = lambda u, v: sum(u[i] * v[i] for i in range(len(u)))
    X = [dot(ph[r], ph[r]) for r in range(2)]; Z = dot(ph[2], ph[2])
    s = [mp.sqrt(1 - tp * X[r]) for r in range(2)]; c = mp.sqrt(1 - tp * Z)
    E = sum((s[r] - 1) / tp for r in range(2)) + (c - 1) / tp
    for r in range(2):
        kph = [sum(kk[i][j] * ph[r][j] for j in range(n)) for i in range(n)]
        a1, a2, a3 = dot(ph[r], kph), dot(ph[r], ph[2]), dot(kph, ph[2])
        B = tp * a1 + s[r] * tp * (a2 - a3) - tp ** 2 * a2 * a3 / (1 + c) + c * (1 - tp * X[r])
        E += (B - 1) / tp
    meas = -sum(mp.log(1 - tp * X[r]) for r in range(2)) / 2 - mp.log(1 - tp * Z) / 2
    Q = Qmat(k)
    quad = sum(mp.mpf(float(y[i])) * mp.mpf(float(Q[i, j])) * mp.mpf(float(y[j])) for i in range(3 * n) for j in range(3 * n))
    return E + meas + quad / 2
