#!/usr/bin/env python3
"""kt_lbu_v1.py -- pk01 (code/pk01/). The engine of LBU_SPEC_v1 (44974154; manifest 09ff07ae): the large-beta lemma LB_u for the
disjoint edge pairs of the uniform P3 x P3, N = 3 and 4, orbits O1..O5 with representatives (b0, f), f in (b2, b4, sE, sN, sW).

Object. J^2 Cov(E_e, E_f) = Cov(xi_e, xi_f), xi_x = J (1 - sigma_a.sigma_b), from the four integrals I_F / main, F in {1, xi_e, xi_f,
  xi_e xi_f}, each bounded by PK10 Lemma 19.1 (sec. 19.1; analytic part REVIEWED in RV12_3, its nits L1-L4 adopted) with the three
  changes of the spec: (C1) fixed rational radii a_v = 1 - r_v^2; (C2) per-vertex Chernoff tails in B_tail and B_ann; (C3) the J-free far
  constant tau(G)^{n/2} (1 - theta)^{-n(V-1)/2}. The error terms are evaluated once at J1 and are nonincreasing in J (spec sec. 3); the
  lower bound Phi(t) (spec sec. 2, vertex form) is evaluated on 64 t-cells covering [0, 1/J1].
Arithmetic. Exact rationals (python-flint fmpq, fmpq_mat, fmpq_mpoly): L+, the Gram matrices (untilted and tilted), principal minors,
  the Gaussian moment recursion k M_k = sum_j ((1 - n/2) j - k) D_j M_{k-j} (amom2b's recursion, exact, in the quotient ring with
  Q_e-degree <= 1, partner degree <= 1 and X-degree caps per Q-pattern that do not increase with the Q-degree), every series, majorant
  and expectation. python-flint arb (prec 256) only for scalars: N^{1/2} at n = 3, the tilt slopes (log), the Chernoff and far
  exponentials, and Phi on t-cells; every final scalar is an arb upper or lower endpoint, in the direction that keeps the bound valid.
  No *_series type of python-flint is used.
Tables per (graph, N, K): T0 untilted, X-degree <= 2K; T1 the common B_rem tilt exp(C35 / Jmin sum X) (C35 >= c(3/5) >= every slope
  c_v, since every radius is capped at 3/5), caps 2K+6 / 2K+4 / 2K+2; T2_v the Chernoff tilt lambda_v = KAPPA / (2 L+_vv), caps 2K;
  T3_v the annulus tilt c'_up / Jmin on every vertex plus lambda'_v = kappa_a / (2 L+_vv) at v (kappa_a = 1/2, halved until (H) holds),
  caps 4 / 2 / 0. The tables do not depend on J1 >= Jmin or on the radii, so the (sigma, J1) grid costs scalar and polynomial work only.
Parameters. JGRID = 50, 55, 60, 65, 70, 75, 80, 90, 100, 110, 120, 135, 150, 175, 200 (Jmin = 50); radii a_v <= min(sigma L+_vv, 3/5)
  with sigma in SIGMAS = 1/4, 1/3, 2/5, 1/2, 3/5; KAPPA = 4/5; rho'^2 = 9801/10000; theta for B_far on the grid k/400.
Modes.
  v1    validation 1: C-SER, C-GRAPH, C-TREE (+ PLANT-FP), C-EXACT (+ PLANT-MOM), C-GAUSS, C-SYM (+ PLANT-SYM), C-H (+ PLANT-H), C-LIT
        (the riglap2/pseries/npoly/amom2b, verbatim copies in lbu_lit_v1/ with sha256 checks), C-BOUND on P3 (+ PLANT-BOUND),
        PLANT-NEG; reading R-SERIES: the exact c2, c3, c4 of J^2 Cov = c2 + c3 t + c4 t^2 + ... for all five orbits at N = 3, 4.
  v2    validation 2 (sizing): orbit O2 = (b0, b4) at N = 4, K = 3 and 4: every table, the four bound terms per F on the (sigma, J1)
        grid, Phi, the smallest certified J1, CPU per step.
  cert  all five orbits at N = 3 and 4 at order K (third argument, 3..5): R-J1 per orbit and N (the smallest certified J1 on JGRID,
        the lower bound L, the bound terms and parameters), C-DATA on O3.
Readings, checks and plants as in LBU_SPEC_v1 sec. 5; every line says PASS/FAIL or FIRED/SILENT; VERDICT VALID needs every check PASS
  and every plant FIRED.
Deviations from LBU_SPEC_v1 sec. 5 (stated here so the review sees them):
  - C-LIT compares polynomials, not only numbers: the series (F e^H)_k for F = 1 (k <= 3) and F = xi_e xi_f (k <= 2; riglap2 with two
    'dot' factors c = 1, shifted by t^2), the majorants h_k (k <= 4), Dbar_4 (F = 1) and xibar_l of b0 (l <= 4) at sigma = 1/2,
    t = 1/120, and the moments a_k (F = 1, k <= 3) through amom2b in floats; relative tolerance 1e-12 (moments 1e-10). The spec's
    K = 4, J = 120, s* = 70 comparison of a_k and B_rem is replaced because riglap2's series are pure Python and the B_rem tilts differ
    by design (common tilt here).
  - PLANT-BOUND runs at J = 40, not 10: at J = 10 the far term on P3 (about 0.15 for F = 1) would hide the planted miss.
  - C-EXACT: 40 random monomials per untilted P3 x P3 table (v1) and 10 per tilted table type (T1, T2_v0, T3_v0) in every Build.
  - C-SYM compares a_k for k <= 2 (central coefficients do not depend on K).
  - The annulus Chernoff rate kappa_a is separate from KAPPA (see Tables).
CPU. RLIMIT_CPU soft LIM, hard LIM + 2; guard() before each heavy step stops at LIM - 4 s with VERDICT INCOMPLETE.
Run (in code/pk01): env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=<own tmp> timeout <LIM+60>
  nice -n 10 prlimit --as=8589934592 --cpu=<LIM+2> -- python3 -I -B kt_lbu_v1.py MODE LIM [K] > <out>
"""
import resource, sys, time, math, os, hashlib, random, itertools

MODES = {'v1': (20, 300), 'v2': (60, 900), 'cert': (60, 3000)}
if len(sys.argv) < 3 or sys.argv[1] not in MODES:
    print('usage: kt_lbu_v1.py MODE LIM [K]   (MODE v1 | v2 | cert; LIM = RLIMIT_CPU soft limit in s, hard LIM + 2; K for cert, 3..5)')
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2])
if not (MODES[MODE][0] <= LIM <= MODES[MODE][1]):
    print('bad LIM %d for mode %s (need %d..%d)' % (LIM, MODE, MODES[MODE][0], MODES[MODE][1]))
    sys.exit(2)
KCERT = int(sys.argv[3]) if len(sys.argv) > 3 else 4
if not (3 <= KCERT <= 5):
    print('bad K %d (need 3..5)' % KCERT)
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 2))

import flint
from flint import fmpq, fmpq_mat, fmpq_mpoly_ctx, arb
from flint import ctx as FLINT
FLINT.prec = 256

HERE = os.path.dirname(os.path.abspath(__file__))
LIT = os.path.join(HERE, 'lbu_lit_v1')
LIT_SHA = {'riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
           'pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
           'npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
           'amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc'}


# ---------------------------------------------------------------- bookkeeping
def cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def out(s=''):
    print(s, flush=True)


class GuardStop(Exception):
    pass


def guard(tag):
    if cpu() > LIM - 4:
        raise GuardStop(tag)


CHECKS = {}
PLANTS = {}


def check(name, ok, detail=''):
    ok = bool(ok)
    CHECKS[name] = CHECKS.get(name, True) and ok
    out('CHECK %s %s %s' % (name, 'PASS' if ok else 'FAIL', detail))


def plant(name, fired, detail=''):
    fired = bool(fired)
    PLANTS[name] = PLANTS.get(name, True) and fired
    out('PLANT %s %s %s' % (name, 'FIRED' if fired else 'SILENT', detail))


FACT = [1]
for _i in range(1, 80):
    FACT.append(FACT[-1] * _i)


def mfact(m):
    r = 1
    for e in m:
        r *= FACT[e]
    return r


def dfact(m):
    r = 1
    while m > 1:
        r *= m
        m -= 2
    return r


def q_ceil(x, den):
    """the smallest k/den >= x (x an fmpq)."""
    return fmpq(int((x * den).ceil()), den)


def up_q(x):
    """an exact rational upper bound of the arb x."""
    return x.upper().fmpq()


def f6(x):
    return '%.6e' % float(x)


# ---------------------------------------------------------------- univariate exact series (lists of fmpq)
def us_mul(a, b, K):
    res = [fmpq(0)] * (K + 1)
    for i in range(min(K + 1, len(a))):
        if a[i] == 0:
            continue
        for j in range(min(K + 1 - i, len(b))):
            res[i + j] += a[i] * b[j]
    return res


def us_inv(a, K):
    res = [fmpq(0)] * (K + 1)
    res[0] = 1 / a[0]
    for k in range(1, K + 1):
        acc = fmpq(0)
        for j in range(1, min(k, len(a) - 1) + 1):
            acc += a[j] * res[k - j]
        res[k] = -acc / a[0]
    return res


def cov_series(A1, Ae, Af, Aef, K):
    i1 = us_inv(A1, K)
    x = us_mul(Aef, i1, K)
    y = us_mul(us_mul(Ae, Af, K), us_mul(i1, i1, K), K)
    return [p - q for p, q in zip(x, y)]


# ---------------------------------------------------------------- graphs (exact)
class Graph:
    def __init__(s, V, edges):
        s.V, s.edges = V, list(edges)
        L = fmpq_mat(V, V)
        for (a, b) in s.edges:
            L[a, a] = L[a, a] + 1
            L[b, b] = L[b, b] + 1
            L[a, b] = L[a, b] - 1
            L[b, a] = L[b, a] - 1
        s.L = L
        B = fmpq_mat(V, V - 1)
        for i in range(V - 1):
            B[i, i] = 1
            B[V - 1, i] = -1
        s.B, s.Bt = B, B.transpose()
        s.A0 = s.Bt * L * B
        s.detA0 = s.A0.det()
        s.Lp = s.B * s.A0.inv() * s.Bt
        red = fmpq_mat(V - 1, V - 1)
        for i in range(V - 1):
            for j in range(V - 1):
                red[i, j] = L[i, j]
        s.tau = red.det()
        s.Lpd = [s.Lp[v, v] for v in range(V)]

    def R(s, a, b):
        return s.Lp[a, a] + s.Lp[b, b] - 2 * s.Lp[a, b]

    def tilt(s, rates):
        """gamma tilted by exp(sum_v rates_v X_v): (C, ratio, ok). C = B A^{-1} B^T with A = B^T (L - 2 diag(rates)) B on the basis B of
        1-perp; ratio = det A0 / det A, so E_gamma[exp(sum rates X)] = ratio^{n/2}; ok = hypothesis (H) (RV12_3 L1) by Sylvester."""
        V = s.V
        Dm = fmpq_mat(V, V)
        for v in range(V):
            Dm[v, v] = rates[v]
        A_ = s.Bt * (s.L - 2 * Dm) * s.B
        for k in range(1, V):
            sub = fmpq_mat(k, k)
            for i in range(k):
                for j in range(k):
                    sub[i, j] = A_[i, j]
            if not (sub.det() > 0):
                return None, None, False
        return s.B * A_.inv() * s.Bt, s.detA0 / A_.det(), True


def evec_of(V, pair):
    e = [0] * V
    e[pair[0]] = 1
    e[pair[1]] = -1
    return e


KAPPA_A = fmpq(1, 2)


def ann_rates(g, tau_a, v):
    """the annulus tilt: tau_a on every vertex plus lambda'_v = kappa_a / (2 L+_vv) at v, kappa_a = 1/2 halved until (H) holds."""
    ka = KAPPA_A
    for _ in range(8):
        lam = ka / (2 * g.Lpd[v])
        rates = [tau_a] * g.V
        rates[v] = tau_a + lam
        C, r, ok = g.tilt(rates)
        if ok:
            return C, r, lam, ka
        ka = ka / 2
    return None, None, None, None


# ---------------------------------------------------------------- the pattern ring: X polynomials times Q_e^a Q_{f_b}^[b > 0]
class PR:
    def __init__(s, V, nb):
        s.V, s.nb = V, nb
        s.ctx = fmpq_mpoly_ctx.get(('x', V))
        s.zero = s.ctx.from_dict({})
        s.one = s.ctx.constant(1)
        s.pats = [(a, b) for a in (0, 1) for b in range(nb + 1)]

    @staticmethod
    def q(P):
        return P[0] + (1 if P[1] else 0)

    @staticmethod
    def pmul(P1, P2):
        a = P1[0] + P2[0]
        if a > 1 or (P1[1] and P2[1]):
            return None
        return (a, P1[1] or P2[1])

    @staticmethod
    def splits(P3):
        a3, b3 = P3
        res = []
        for a1 in range(a3 + 1):
            if b3 == 0:
                res.append(((a1, 0), (a3 - a1, 0)))
            else:
                res.append(((a1, b3), (a3 - a1, 0)))
                res.append(((a1, 0), (a3 - a1, b3)))
        return res

    def X(s, v, k=1, c=1):
        e = [0] * s.V
        e[v] = k
        return s.ctx.from_dict({tuple(e): c})

    def D2(s, u, v):
        return s.X(u, 2) - s.X(u, 1) * s.X(v, 1) * 2 + s.X(v, 2)

    def Mk(s, u, v, k):
        return s.one if k == 0 else s.X(u, k) + s.X(v, k)


def padd(*Ps):
    res = {}
    for P in Ps:
        for k, v in P.items():
            res[k] = res[k] + v if k in res else v
    return {k: v for k, v in res.items() if not v.is_zero()}


def pscale(P, c):
    if c == 0:
        return {}
    return {k: v * c for k, v in P.items()}


def pmulp(R, P1, P2):
    res = {}
    for k1, v1 in P1.items():
        for k2, v2 in P2.items():
            k = R.pmul(k1, k2)
            if k is None:
                raise ValueError('forbidden Q product %s * %s' % (k1, k2))
            pr = v1 * v2
            res[k] = res[k] + pr if k in res else pr
    return {k: v for k, v in res.items() if not v.is_zero()}


def pabs(R, P):
    return {k: R.ctx.from_dict({m: abs(c) for m, c in zip(v.monoms(), v.coeffs())}) for k, v in P.items()}


def pnterms(P):
    return sum(len(v) for v in P.values())


def szero(K):
    return [dict() for _ in range(K + 1)]


def sadd(A_, B_):
    return [padd(a, b) for a, b in zip(A_, B_)]


def sscale(A_, c):
    return [pscale(a, c) for a in A_]


def smul(R, A_, B_, K):
    res = szero(K)
    for i in range(K + 1):
        if not A_[i]:
            continue
        for j in range(K + 1 - i):
            if B_[j]:
                res[i + j] = padd(res[i + j], pmulp(R, A_[i], B_[j]))
    return res


def sexp(R, H, K):
    assert not H[0]
    E = [{(0, 0): R.one}] + [dict() for _ in range(K)]
    for k in range(1, K + 1):
        acc = {}
        for j in range(1, k + 1):
            if H[j] and E[k - j]:
                acc = padd(acc, pscale(pmulp(R, H[j], E[k - j]), j))
        E[k] = pscale(acc, fmpq(1, k))
    return E


def tp_add(A_, B_):
    m = max(len(A_), len(B_))
    return [padd(A_[i] if i < len(A_) else {}, B_[i] if i < len(B_) else {}) for i in range(m)]


def tp_mul(R, A_, B_):
    res = [dict() for _ in range(len(A_) + len(B_) - 1)]
    for i, x in enumerate(A_):
        for j, y in enumerate(B_):
            if x and y:
                res[i + j] = padd(res[i + j], pmulp(R, x, y))
    return res


def tp_scale(A_, c):
    return [pscale(x, c) for x in A_]


# ---------------------------------------------------------------- exact series of the chart (PK10 sec. 19.1)
def w_exact(Kw):
    """w(x, y) = (sqrt(1 - x) + sqrt(1 - y))^{-2} to total degree Kw, exact: w = (1/4) sum_m (m + 1) (-d/2)^m, d = s(x) + s(y) - 2."""
    s_ = [fmpq(1)] + [fmpq(-math.comb(2 * k, k), 4 ** k * (2 * k - 1)) for k in range(1, Kw + 1)]
    hd = {}
    for k in range(1, Kw + 1):
        hd[(k, 0)] = hd.get((k, 0), fmpq(0)) - s_[k] / 2
        hd[(0, k)] = hd.get((0, k), fmpq(0)) - s_[k] / 2

    def mul2(P1, P2):
        res = {}
        for (i1, j1), c1 in P1.items():
            for (i2, j2), c2 in P2.items():
                if i1 + i2 + j1 + j2 <= Kw:
                    key = (i1 + i2, j1 + j2)
                    res[key] = res.get(key, fmpq(0)) + c1 * c2
        return res
    w = {(0, 0): fmpq(1, 4)}
    pw = {(0, 0): fmpq(1)}
    for m in range(1, Kw + 1):
        pw = mul2(pw, hd)
        for key, v in pw.items():
            w[key] = w.get(key, fmpq(0)) + fmpq(m + 1, 4) * v
    return w


def wpoly(R, wd, a, b, m):
    d = {}
    for (i, j), c in wd.items():
        if i + j == m and c != 0:
            e = [0] * R.V
            e[a] += i
            e[b] += j
            d[tuple(e)] = d.get(tuple(e), fmpq(0)) + c
    return R.ctx.from_dict(d)


def H_series(R, g, n, K, wd, fpc=None):
    """H = sum_v meas_v + FP + sum_x anh_x to order K: meas_v = -1/2 log(1 - t X_v), FP = fpc log(1 - y) (fpc = n; PLANT-FP: n + 1),
    y = (1/V) sum_v (1 - sqrt(1 - t X_v)), anh_x = -(1/2) t D_x w(t X_a, t X_b), D_x = (X_a - X_b)^2."""
    fpc = n if fpc is None else fpc
    V = g.V
    H = szero(K)
    for k in range(1, K + 1):
        p = R.zero
        for v in range(V):
            p = p + R.X(v, k, fmpq(1, 2 * k))
        H[k] = padd(H[k], {(0, 0): p})
    y = szero(K)
    for k in range(1, K + 1):
        bk = fmpq(math.comb(2 * k, k), 4 ** k * (2 * k - 1) * V)
        p = R.zero
        for v in range(V):
            p = p + R.X(v, k, bk)
        y[k] = {(0, 0): p}
    y_m = y
    for m in range(1, K + 1):
        H = sadd(H, sscale(y_m, fmpq(-fpc, m)))
        y_m = smul(R, y_m, y, K)
    for (a, b) in g.edges:
        D = R.D2(a, b)
        for k in range(1, K + 1):
            H[k] = padd(H[k], {(0, 0): D * wpoly(R, wd, a, b, k - 1) * fmpq(-1, 2)})
    return H


def xi_series(R, wd, a, b, P, K):
    """xi_x = Q_x / 2 + (1/2) D_x t w(t X_a, t X_b); Q_x is the pattern P."""
    S = szero(K)
    S[0] = {P: R.ctx.constant(fmpq(1, 2))}
    D = R.D2(a, b)
    for k in range(1, K + 1):
        S[k] = {(0, 0): D * wpoly(R, wd, a, b, k - 1) * fmpq(1, 2)}
    return S


# ---------------------------------------------------------------- exact Gaussian moments (amom2b's recursion, exact, quotient ring)
def det_sub(Gl, S):
    k = len(S)
    M = fmpq_mat(k, k)
    for i in range(k):
        for j in range(k):
            M[i, j] = Gl[S[i]][S[j]]
    return M.det()


class Moments:
    """E_C[X^alpha Q_e^a Q_f^b] for the Gaussian with covariance C (x) I_n on 1-perp; forms X_v = |phi_v|^2, Q_e, Q_{f_b} = |phi_u - phi_w|^2.
    M(s) = det(I - 2 S Gamma)^{-n/2}; k M_k = sum_j ((1 - n/2) j - k) D_j M_{k-j}; moments = alpha! [s^alpha] M."""
    def __init__(s, R, g, C, ratio, n, evec, fvecs, caps, tag):
        t0 = cpu()
        V = g.V
        s.R, s.n, s.ratio, s.caps, s.tag = R, n, ratio, dict(caps), tag
        assert caps[0] >= caps[1] >= caps[2]
        vecs = [[1 if u == v else 0 for u in range(V)] for v in range(V)] + [evec] + list(fvecs)
        m = len(vecs)
        U = fmpq_mat(V, m)
        for i, vec in enumerate(vecs):
            for u in range(V):
                U[u, i] = vec[u]
        Gm = U.transpose() * C * U
        s.Gl = [[Gm[i, j] for j in range(m)] for i in range(m)]
        s.D = {}
        for P in R.pats:
            extra = ([V] if P[0] else []) + ([V + P[1]] if P[1] else [])
            lst = []
            for j in range(V + 1):
                d = {}
                for Asub in itertools.combinations(range(V), j):
                    S_ = list(Asub) + extra
                    if not S_:
                        continue
                    dt = det_sub(s.Gl, S_)
                    if dt != 0:
                        e = [0] * V
                        for i in Asub:
                            e[i] = 1
                        d[tuple(e)] = dt * (-2) ** (j + len(extra))
                lst.append(R.ctx.from_dict(d))
            s.D[P] = lst
        cap = {P: caps[R.q(P)] for P in R.pats}
        M = {P: [None] * (cap[P] + 1) for P in R.pats}
        M[(0, 0)][0] = R.one
        kmax = max(cap[P] + R.q(P) for P in R.pats)
        for k in range(1, kmax + 1):
            guard('moments %s k=%d' % (tag, k))
            for P3 in R.pats:
                d3 = k - R.q(P3)
                if d3 < 0 or d3 > cap[P3]:
                    continue
                acc = R.zero
                for j in range(1, k + 1):
                    part = R.zero
                    for (P1, P2) in R.splits(P3):
                        dj1 = j - R.q(P1)
                        if dj1 < 0 or dj1 > V:
                            continue
                        d2 = d3 - dj1
                        if d2 < 0:
                            continue
                        Dp = s.D[P1][dj1]
                        if Dp.is_zero():
                            continue
                        part = part + Dp * M[P2][d2]
                    if not part.is_zero():
                        acc = acc + part * fmpq((2 - n) * j - 2 * k, 2)
                M[P3][d3] = acc * fmpq(1, k)
        s.mom = {}
        s.nterms = 0
        for P in R.pats:
            s.mom[P] = []
            for d in range(cap[P] + 1):
                p = M[P][d]
                s.mom[P].append(R.ctx.from_dict({mm: c * mfact(mm) for mm, c in zip(p.monoms(), p.coeffs())}))
                s.nterms += len(p)
            M[P] = None
        s.cpu = cpu() - t0
        out('TABLE %s: n %d, caps %s, %d moments, cpu %.2f s' % (tag, n, caps, s.nterms, s.cpu))

    def E(s, PP):
        tot = fmpq(0)
        for P, p in PP.items():
            if p.is_zero():
                continue
            tab = s.mom[P]
            for mm, c in zip(p.monoms(), p.coeffs()):
                d = sum(mm)
                if d >= len(tab):
                    raise ValueError('%s: degree %d beyond cap %d in pattern %s' % (s.tag, d, len(tab) - 1, P))
                tot += c * tab[d][mm]
        return tot

    def Narb(s):
        r = arb(s.ratio)
        return r if s.n == 2 else r * r.sqrt()


def aperm(Gl, idx, alpha):
    """the alpha-permanent sum_pi alpha^{cyc(pi)} prod_i Gl[idx_i][idx_pi(i)] (exact)."""
    k = len(idx)
    tot = fmpq(0)
    for perm in itertools.permutations(range(k)):
        pr = fmpq(1)
        for i in range(k):
            pr *= Gl[idx[i]][idx[perm[i]]]
        if pr == 0:
            continue
        seen = [False] * k
        cyc = 0
        for i in range(k):
            if not seen[i]:
                cyc += 1
                j = i
                while not seen[j]:
                    seen[j] = True
                    j = perm[j]
        tot += pr * alpha ** cyc
    return tot


def c_exact(mo, V, rng, nmono, maxdeg, perturb=False):
    """C-EXACT: E[prod of forms] = 2^k per_{n/2}(Gamma) for random monomials of total degree <= maxdeg (independent formula)."""
    alpha = fmpq(mo.n, 2)
    bad = done = 0
    for _ in range(nmono):
        P = mo.R.pats[rng.randrange(len(mo.R.pats))]
        qd = mo.R.q(P)
        dmax = min(mo.caps[qd], maxdeg - qd)
        if dmax < 0:
            continue
        d = rng.randint(0, dmax)
        e = [0] * V
        for _r in range(d):
            e[rng.randrange(V)] += 1
        idx = [v for v in range(V) for _r in range(e[v])] + ([V] if P[0] else []) + ([V + P[1]] if P[1] else [])
        want = aperm(mo.Gl, idx, alpha) * 2 ** len(idx)
        have = mo.mom[P][d][tuple(e)]
        if perturb and done == 0:
            have = have + fmpq(1, 10 ** 20)
        done += 1
        if have != want:
            bad += 1
    return bad, done


# ---------------------------------------------------------------- Lemma 19.1's majorants (exact, given rational radii)
def partial_bell(R, k, m, xs):
    memo = {}

    def rec(kk, mm):
        if (kk, mm) in memo:
            return memo[(kk, mm)]
        if kk == 0 and mm == 0:
            res = R.one
        elif kk == 0 or mm == 0:
            res = R.zero
        else:
            res = R.zero
            for i in range(1, kk - mm + 2):
                res = res + xs[i] * rec(kk - i, mm - 1) * math.comb(kk - 1, i - 1)
        memo[(kk, mm)] = res
        return res
    return rec(k, m)


class Maj:
    """h_k (k <= K + 1), complete Bell Y_m (m <= K + 1), xi majorants as t-polynomials, Fbar_j, Dbar_{K+1} (PK10 sec. 19.1)."""
    def __init__(s, R, g, n, avec, rvec, K):
        s.R, s.g, s.n, s.a, s.r, s.K = R, g, n, list(avec), list(rvec), K
        s.h = {k: s.hbar(k) for k in range(1, K + 2)}
        Y = [{(0, 0): R.one}]
        for m in range(K + 1):
            acc = {}
            for i in range(m + 1):
                acc = padd(acc, pscale(pmulp(R, s.h[i + 1], Y[m - i]), math.comb(m, i)))
            Y.append(acc)
        s.Y = Y

    def hbar(s, k):
        R, g, a, r, V = s.R, s.g, s.a, s.r, s.g.V
        p = R.zero
        for v in range(V):
            p = p + R.X(v, k, fmpq(FACT[k - 1]) / (2 * (1 - a[v]) ** k))
        for (u, v) in g.edges:
            ae = max(a[u], a[v])
            p = p + R.D2(u, v) * R.Mk(u, v, k - 1) * (fmpq(FACT[k], 8) / (1 - ae) ** (k + 1))
        ymax = sum((a[v] / (2 - a[v]) for v in range(V)), fmpq(0)) / V
        ys = [None]
        for j in range(1, k + 1):
            cj = fmpq(dfact(2 * j - 3), 2 ** j)
            yj = R.zero
            for v in range(V):
                yj = yj + R.X(v, j, cj / (r[v] ** (2 * j - 1) * V))
            ys.append(yj)
        fp = R.zero
        for mm in range(1, k + 1):
            fp = fp + partial_bell(R, k, mm, ys) * (fmpq(s.n * FACT[mm - 1]) / (1 - ymax) ** mm)
        return {(0, 0): p + fp}

    def xibar(s, a_, b_, P, l):
        R = s.R
        ax = max(s.a[a_], s.a[b_])
        D = R.D2(a_, b_)
        if l == 0:
            return [{P: R.ctx.constant(fmpq(1, 2))}, {(0, 0): D * (fmpq(1, 8) / (1 - ax))}]
        return [{(0, 0): D * R.Mk(a_, b_, l - 1) * (fmpq(FACT[l], 8) / (1 - ax) ** (l + 1))}]

    def Fbar(s, F, j, ep, fp):
        if F == '1':
            return [{(0, 0): s.R.one}] if j == 0 else [dict()]
        if F == 'e':
            return s.xibar(ep[0], ep[1], ep[2], j)
        if F == 'f':
            return s.xibar(fp[0], fp[1], fp[2], j)
        res = [dict()]
        for i in range(j + 1):
            res = tp_add(res, tp_scale(tp_mul(s.R, s.xibar(ep[0], ep[1], ep[2], i), s.xibar(fp[0], fp[1], fp[2], j - i)), math.comb(j, i)))
        return res

    def Dbar(s, F, ep, fp):
        K1 = s.K + 1
        res = [dict()]
        for j in range(K1 + 1):
            fb = s.Fbar(F, j, ep, fp)
            term = [pmulp(s.R, x, s.Y[K1 - j]) if x else {} for x in fb]
            res = tp_add(res, tp_scale(term, math.comb(K1, j)))
        return res


def F0p(R, F, ep, fp, rho2):
    """the annulus majorant of |F| (all radii rho'^2) as a t-polynomial."""
    def xb(a_, b_, P):
        return [{P: R.ctx.constant(fmpq(1, 2))}, {(0, 0): R.D2(a_, b_) * (fmpq(1, 8) / (1 - rho2))}]
    if F == '1':
        return [{(0, 0): R.one}]
    if F == 'e':
        return xb(*ep)
    if F == 'f':
        return xb(*fp)
    return tp_mul(R, xb(*ep), xb(*fp))


def radii(g, sigma):
    """(C1): a_v = 1 - r_v^2 <= min(sigma L+_vv, 3/5), r_v = m/256 the smallest with r_v^2 >= max(1 - sigma L+_vv, 2/5)."""
    avec, rvec = [], []
    for v in range(g.V):
        x = max(1 - sigma * g.Lpd[v], fmpq(2, 5))
        m = math.isqrt(int((x * 65536).floor()))
        while fmpq(m * m, 65536) < x:
            m += 1
        r = fmpq(m, 256)
        assert 0 < r < 1
        avec.append(1 - r * r)
        rvec.append(r)
    return avec, rvec


def cslope(a, r):
    """c = -log(1 - a)/(2a) = -log(r)/a (arb)."""
    return -(arb(r).log()) / arb(a)


C35 = q_ceil(up_q(-(arb(fmpq(2, 5)).log()) / arb(fmpq(6, 5))), 64)     # >= c(3/5): every radius is capped at 3/5


# ---------------------------------------------------------------- the J1-independent part for one graph, N, K and partner list
FNAMES = ('1', 'e', 'f', 'ef')
DF = {'1': 0, 'e': 1, 'f': 1, 'ef': 2}


class Build:
    def __init__(s, g, n, K, epair, fpairs, Jmin, kappa, rho2, label, need_tilts=True):
        t0 = cpu()
        s.g, s.n, s.K, s.label, s.Jmin, s.kappa, s.rho2 = g, n, K, label, Jmin, kappa, rho2
        V = g.V
        nb = len(fpairs)
        R = PR(V, nb)
        s.R = R
        wd = w_exact(max(K, 1) + 1)
        H = H_series(R, g, n, K, wd)
        E = sexp(R, H, K)
        s.ep = (epair[0], epair[1], (1, 0))
        s.fps = [(f[0], f[1], (0, b + 1)) for b, f in enumerate(fpairs)]
        xe = xi_series(R, wd, epair[0], epair[1], (1, 0), K)
        xfs = [xi_series(R, wd, f[0], f[1], (0, b + 1), K) for b, f in enumerate(fpairs)]
        one = szero(K)
        one[0] = {(0, 0): R.one}
        s.PS = {('1', 0): smul(R, one, E, K), ('e', 0): smul(R, xe, E, K)}
        for b in range(1, nb + 1):
            s.PS[('f', b)] = smul(R, xfs[b - 1], E, K)
            s.PS[('ef', b)] = smul(R, smul(R, xe, xfs[b - 1], K), E, K)
        s.keys = list(s.PS.keys())
        out('SERIES %s: K %d, terms per key %s, cpu %.2f s' % (label, K, {k: [pnterms(p) for p in v] for k, v in s.PS.items() if k[1] <= 1},
                                                             cpu() - t0))
        s.evec = evec_of(V, epair)
        s.fvecs = [evec_of(V, f) for f in fpairs]
        guard('T0 ' + label)
        s.T0 = Moments(R, g, g.Lp, fmpq(1), n, s.evec, s.fvecs, {0: 2 * K, 1: 2 * K, 2: 2 * K}, label + ' T0')
        s.a = {key: [s.T0.E(s.PS[key][k]) for k in range(K + 1)] for key in s.keys}
        if not need_tilts:
            return
        rng = random.Random(7)
        # T1: the common B_rem tilt exp(C35 t_max sum X), valid for every radius (a_v <= 3/5) and every J1 >= Jmin
        s.tau_c = C35 / Jmin
        C1, r1, ok1 = g.tilt([s.tau_c] * V)
        check('C-H %s T1' % label, ok1, 'tilt %s' % s.tau_c)
        if not ok1:
            raise ValueError('T1 tilt violates (H)')
        guard('T1 ' + label)
        s.T1 = Moments(R, g, C1, r1, n, s.evec, s.fvecs, {0: 2 * K + 6, 1: 2 * K + 4, 2: 2 * K + 2}, label + ' T1')
        bad, done = c_exact(s.T1, V, rng, 10, 6)
        check('C-EXACT %s T1' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
        s.Nc = s.T1.Narb()
        # T2_v: the Chernoff tilts lambda_v = kappa / (2 L+_vv); tail expectations of |(F e^H)_k|
        s.lam = [kappa / (2 * g.Lpd[v]) for v in range(V)]
        s.N2, s.TL = [], {key: [[None] * V for _ in range(K + 1)] for key in s.keys}
        pab = {key: [pabs(R, s.PS[key][k]) for k in range(K + 1)] for key in s.keys}
        for v in range(V):
            rates = [fmpq(0)] * V
            rates[v] = s.lam[v]
            C2, r2, ok2 = g.tilt(rates)
            check('C-H %s T2 v%d' % (label, v), ok2, 'lambda %s' % s.lam[v])
            if not ok2:
                raise ValueError('T2 tilt violates (H)')
            guard('T2 %s v%d' % (label, v))
            T2 = Moments(R, g, C2, r2, n, s.evec, s.fvecs, {0: 2 * K, 1: 2 * K, 2: 2 * K}, '%s T2 v%d' % (label, v))
            if v == 0:
                bad, done = c_exact(T2, V, rng, 10, 6)
                check('C-EXACT %s T2 v0' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
            s.N2.append(T2.Narb())
            for key in s.keys:
                for k in range(K + 1):
                    s.TL[key][k][v] = T2.E(pab[key][k])
            del T2
        # T3_v: the annulus tilts; expectations of the annulus majorant (t-polynomial parts)
        cp = -(arb(1 - rho2).log()) / (2 * arb(rho2))
        s.cprime = q_ceil(up_q(cp), 64)
        s.tau_a = s.cprime / Jmin
        s.N3, s.lam_a, s.AN = [], [], {key: [None] * V for key in s.keys}
        f0 = {}
        for key in s.keys:
            F, b = key
            f0[key] = F0p(R, F, s.ep, s.fps[b - 1] if b else None, rho2)
        for v in range(V):
            C3, r3, lam_a, ka = ann_rates(g, s.tau_a, v)
            check('C-H %s T3 v%d' % (label, v), C3 is not None, 'tilt %s + kappa_a %s' % (s.tau_a, ka))
            if C3 is None:
                raise ValueError('no annulus tilt satisfies (H)')
            guard('T3 %s v%d' % (label, v))
            T3 = Moments(R, g, C3, r3, n, s.evec, s.fvecs, {0: 4, 1: 2, 2: 0}, '%s T3 v%d' % (label, v))
            if v == 0:
                bad, done = c_exact(T3, V, rng, 10, 6)
                check('C-EXACT %s T3 v0' % label, bad == 0 and done > 0, '%d of %d' % (done - bad, done))
            s.N3.append(T3.Narb())
            s.lam_a.append(lam_a)
            for key in s.keys:
                s.AN[key][v] = [T3.E(part) for part in f0[key]]
            del T3
        s.sig = {}
        out('BUILD %s done, cpu %.2f s' % (label, cpu() - t0))

    def add_sigma(s, sigma):
        """radii for sigma and the expectations E_T1[Dbar_{K+1}] (t-parts) per key."""
        t0 = cpu()
        g, R = s.g, s.R
        avec, rvec = radii(g, sigma)
        cmax = max(up_q(cslope(avec[v], rvec[v])) for v in range(g.V))
        assert cmax <= C35
        mj = Maj(R, g, s.n, avec, rvec, s.K)
        ED, nt = {}, {}
        for key in s.keys:
            guard('Dbar %s sigma %s %s' % (s.label, sigma, key))
            F, b = key
            parts = mj.Dbar(F, s.ep, s.fps[b - 1] if b else None)
            nt[key] = sum(pnterms(p) for p in parts)
            vals = [s.T1.E(p) for p in parts]
            for x in vals:
                assert x >= 0
            ED[key] = vals + [fmpq(0)] * (3 - len(vals))
        s.sig[sigma] = (avec, rvec, ED)
        out('SIGMA %s %s: radii %s, max slope %s, Dbar terms %s, cpu %.2f s' % (s.label, sigma, [f6(x) for x in avec], f6(cmax),
            {k: nt[k] for k in s.keys if k[1] <= 1}, cpu() - t0))

    def errors(s, sigma, J1, key, drop_rem=False):
        """(B_rem, B_tail, B_ann, B_far) for key at J1 (arb upper bounds), radii of sigma."""
        avec, rvec, ED = s.sig[sigma]
        K, V, n = s.K, s.g.V, s.n
        t1 = fmpq(1, J1)
        assert t1 <= fmpq(1, s.Jmin)
        F = key[0]
        e = ED[key]
        brem = arb(0) if drop_rem else arb(t1 ** (K + 1) / FACT[K + 1]) * s.Nc * arb(e[0] + e[1] * t1 + e[2] * t1 * t1)
        ch = [(-(arb(s.lam[v] * J1 * avec[v]))).exp() for v in range(V)]
        cha = [(-(arb(s.lam_a[v] * J1 * avec[v]))).exp() for v in range(V)]
        btail = arb(0)
        for k in range(K + 1):
            for v in range(V):
                btail += arb(t1 ** k) * ch[v] * s.N2[v] * arb(s.TL[key][k][v])
        bann = arb(0)
        for v in range(V):
            val = fmpq(0)
            for i, x in enumerate(s.AN[key][v]):
                val += x * t1 ** i
            bann += cha[v] * s.N3[v] * arb(val)
        bfar, th = far_bound(s.g, n, J1, DF[F], s.rho2)
        return [arb(up_q(x)) for x in (brem, btail, bann, bfar)], th


def far_bound(g, n, J1, dF, rho2):
    """(C3): B_far <= (2 J1)^dF tau^{n/2} (1 - th)^{-n(V-1)/2} sum_v exp(-th J1 rho'^2 / (2 L+_vv)); th chosen on k/400 in floats, the
    bound evaluated in arb at that rational th; B_far is decreasing in J for J > 2 max L+ dF / (th rho'^2) (asserted)."""
    V = g.V
    best = None
    for k in range(1, 400):
        th = k / 400.0
        xs = [-th * J1 * float(rho2) / (2 * float(g.Lpd[v])) for v in range(V)]
        mx = max(xs)
        val = (dF * math.log(2 * J1) + 0.5 * n * math.log(float(g.tau)) - 0.5 * n * (V - 1) * math.log(1 - th)
               + mx + math.log(sum(math.exp(x - mx) for x in xs)))
        if best is None or val < best[0]:
            best = (val, k)
    th = fmpq(best[1], 400)
    assert J1 > 2 * max(g.Lpd) * dF / (th * rho2)
    sm = arb(0)
    for v in range(V):
        sm += (-(arb(th * J1 * rho2 / (2 * g.Lpd[v])))).exp()
    tauN = arb(g.tau) if n == 2 else arb(g.tau) * arb(g.tau).sqrt()
    ex = n * (V - 1)
    om = arb(1 - th)
    fac = om ** (ex // 2)
    if ex % 2:
        fac = fac * om.sqrt()
    return arb(2 * J1) ** dF * tauN * sm / fac, th


def horner(coefs, x):
    r = arb(0)
    for c in reversed(coefs):
        r = r * x + arb(c)
    return r


def phi_scan(Acoef, Eu, t1, ncell=64):
    """min over t-cells of [0, t1] of the vertex lower bound of Cov = i_ef/i_1 - i_e i_f / i_1^2, i_F in A_F(t) +- E_F, with the
    monotonicity in i_1 (2 i_e i_f > i_ef i_1) checked on every box. Returns (min lower bound (arb), monotone ok, negative cells)."""
    worst = None
    mono = True
    nneg = 0
    for i in range(ncell):
        lo_t = t1 * i / ncell
        hi_t = t1 * (i + 1) / ncell
        tb = arb((lo_t + hi_t) / 2) + arb(0, (hi_t - lo_t) / 2)
        val = {F: horner(Acoef[F], tb) for F in FNAMES}
        i1l = (val['1'] - Eu['1']).lower()
        i1h = (val['1'] + Eu['1']).upper()
        iel = (val['e'] - Eu['e']).lower()
        ieh = (val['e'] + Eu['e']).upper()
        ifl = (val['f'] - Eu['f']).lower()
        ifh = (val['f'] + Eu['f']).upper()
        iefl = (val['ef'] - Eu['ef']).lower()
        iefh = (val['ef'] + Eu['ef']).upper()
        if not (i1l > 0 and iel > 0 and ifl > 0 and iefl > 0):
            mono = False
            ph = arb(-1)
        else:
            if not (2 * iel * ifl - iefh * i1h > 0):
                mono = False
            ph = (iefl / i1l - ieh * ifh / (i1l * i1l)).lower()
        if worst is None or ph < worst:
            worst = ph
        if not (ph > 0):
            nneg += 1
    return worst, mono, nneg


# ---------------------------------------------------------------- the 3 x 3 grid
NAMES = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW', 'C']
EDGES = {'b0': (0, 1), 'b1': (1, 2), 'b2': (2, 3), 'b3': (3, 4), 'b4': (4, 5), 'b5': (5, 6), 'b6': (6, 7), 'b7': (7, 0),
         'sS': (8, 0), 'sE': (8, 2), 'sN': (8, 4), 'sW': (8, 6)}
ELIST = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'sS', 'sE', 'sN', 'sW']
# (name, e, f, Delta^2 from out_kt_c2unif_v1_full.out 438317a3 l.4-12, second member (sigma e, sigma f) for C-SYM)
ORBITS = [('O1', 'b0', 'b2', fmpq(1, 36), ('b2', 'b4')), ('O2', 'b0', 'b4', fmpq(1, 144), ('b1', 'b5')),
          ('O3', 'b0', 'sE', fmpq(25, 144), ('b6', 'sS')), ('O4', 'b0', 'sN', fmpq(1, 144), ('b2', 'sW')),
          ('O5', 'b0', 'sW', fmpq(1, 144), ('b2', 'sS'))]
G9 = Graph(9, [EDGES[x] for x in ELIST])
JGRID = [50, 55, 60, 65, 70, 75, 80, 90, 100, 110, 120, 135, 150, 175, 200]
SIGMAS = [fmpq(1, 4), fmpq(1, 3), fmpq(2, 5), fmpq(1, 2), fmpq(3, 5)]
KAPPA = fmpq(4, 5)
RHO2 = fmpq(9801, 10000)
# out_kt_c2unif_v1_full.out (438317a3) l.61-66: D(J_f = beta) for c2's pair (b6, sS) in O3, float quadrature
CDATA = {(3, 100): 4.361620e-06, (3, 150): 1.935314e-06, (3, 200): 1.087723e-06,
         (4, 100): 6.541862e-06, (4, 150): 2.902814e-06, (4, 200): 1.631521e-06}


def delta_of(g, e, f):
    (a, b), (u, w) = e, f
    return g.R(a, u) + g.R(b, w) - g.R(a, w) - g.R(b, u)


def certify(bd, b, sigmas, jgrid, tagline):
    """for partner b: the smallest J1 in jgrid with min Phi > 0 (over sigmas); prints every evaluated point. Returns a dict or None."""
    best = None
    for J1 in jgrid:
        t1 = fmpq(1, J1)
        Acoef = {F: bd.a[(F, 0) if F in ('1', 'e') else (F, b)] for F in FNAMES}
        for sigma in sigmas:
            guard('certify %s J1 %d' % (tagline, J1))
            Eu, terms, ths = {}, {}, {}
            for F in FNAMES:
                key = (F, 0) if F in ('1', 'e') else (F, b)
                tt, th = bd.errors(sigma, J1, key)
                terms[F] = tt
                ths[F] = str(th)
                Eu[F] = arb(up_q(tt[0] + tt[1] + tt[2] + tt[3]))
            L, mono, nneg = phi_scan(Acoef, Eu, t1)
            ok = mono and nneg == 0 and L > 0
            out('POINT %s J1 %d sigma %s: L %s mono %s neg %d | %s' % (tagline, J1, sigma, f6(L), mono, nneg,
                '; '.join('%s rem %s tail %s ann %s far %s (th %s)' % (F, f6(terms[F][0]), f6(terms[F][1]), f6(terms[F][2]),
                                                                       f6(terms[F][3]), ths[F]) for F in FNAMES)))
            if ok and (best is None or J1 < best['J1'] or (J1 == best['J1'] and L > best['L'])):
                best = dict(J1=J1, sigma=sigma, L=L, terms=terms, ths=ths, Eu=Eu)
        if best is not None and best['J1'] == J1:
            break
    return best


# ---------------------------------------------------------------- v1: validation 1
def tree_expect(n, K):
    """P3 with e = (0, 1), f = (1, 2): the exact asymptotic series of I/main = r^2, I_xi_e/main = <xi> r^2, I_xi_e xi_f/main = <xi>^2 r^2,
    r = 1 (N = 3: 1 - e^{-2J}) or sqrt(2 pi J) e^{-J} I_1(J) ~ sum_k (-1)^k a_k(1) t^k (N = 4); <xi> = n/2 + t d/dt log r."""
    r = [fmpq(1)]
    for k in range(1, K + 1):
        if n == 2:
            r.append(fmpq(0))
        else:
            num = 1
            for i in range(1, k + 1):
                num *= (4 - (2 * i - 1) ** 2)
            r.append(fmpq((-1) ** k * num, FACT[k] * 8 ** k))
    u = [fmpq(0)] + r[1:]
    lg = [fmpq(0)] * (K + 1)
    um = u[:]
    for m in range(1, K + 1):
        lg = [x + y * fmpq((-1) ** (m + 1), m) for x, y in zip(lg, um)]
        um = us_mul(um, u, K)
    xi = [fmpq(n, 2)] + [k * lg[k] for k in range(1, K + 1)]
    r2 = us_mul(r, r, K)
    return {'1': r2, 'e': us_mul(xi, r2, K), 'ef': us_mul(us_mul(xi, xi, K), r2, K)}


def tree_truth(n, J):
    Ja = arb(J)
    if n == 2:
        r = 1 - (-2 * Ja).exp()
        xi = 1 - 2 * Ja * (-2 * Ja).exp() / r
    else:
        i1 = Ja.bessel_i(1, scaled=True)
        i0 = Ja.bessel_i(0, scaled=True)
        r = (2 * arb.pi() * Ja).sqrt() * i1
        xi = Ja + 2 - Ja * i0 / i1
    return {'1': r * r, 'e': xi * r * r, 'ef': xi * xi * r * r}


def run_v1():
    rng = random.Random(20261102)
    # C-SER
    wd = w_exact(8)
    rows = all(sum((c for (i, j), c in wd.items() if i + j == m), fmpq(0)) == fmpq(1, 4) for m in range(9))
    sym = all(wd.get((j, i), fmpq(0)) == c for (i, j), c in wd.items())
    check('C-SER', rows and sym, 'w row sums 1/4 to degree 8: %s; symmetric: %s' % (rows, sym))
    # C-GRAPH
    g = G9
    want = [fmpq(13, 36), fmpq(13, 24)] * 4 + [fmpq(2, 9)]
    okL = all(g.Lpd[v] == want[v] for v in range(9))
    foster = sum((g.R(*EDGES[x]) for x in ELIST), fmpq(0))
    okD = True
    for (nm, e, f, d2, _) in ORBITS:
        dd = delta_of(g, EDGES[e], EDGES[f])
        okD = okD and dd * dd == d2
        out('ORBIT %s (%s, %s): Delta %s, Delta^2 %s (table %s)' % (nm, e, f, dd, dd * dd, d2))
    check('C-GRAPH', okL and g.tau == 192 and foster == 8 and okD,
          'L+ diag %s; tau %s; Foster %s; Delta^2 match %s' % (okL, g.tau, foster, okD))
    # C-TREE (+ PLANT-FP): P3, K = 5
    gt = Graph(3, [(0, 1), (1, 2)])
    KT = 5
    for n in (2, 3):
        exp_ = tree_expect(n, KT)
        for fpc, isplant in ((n, False), (n + 1, True)):
            Rt = PR(3, 1)
            wdt = w_exact(KT + 1)
            H = H_series(Rt, gt, n, KT, wdt, fpc=fpc)
            E = sexp(Rt, H, KT)
            xe = xi_series(Rt, wdt, 0, 1, (1, 0), KT)
            xf = xi_series(Rt, wdt, 1, 2, (0, 1), KT)
            one = szero(KT)
            one[0] = {(0, 0): Rt.one}
            T0 = Moments(Rt, gt, gt.Lp, fmpq(1), n, evec_of(3, (0, 1)), [evec_of(3, (1, 2))], {0: 2 * KT, 1: 2 * KT, 2: 2 * KT},
                         'tree N=%d fpc=%d' % (n + 1, fpc))
            got = {'1': [T0.E(p) for p in smul(Rt, one, E, KT)], 'e': [T0.E(p) for p in smul(Rt, xe, E, KT)],
                   'ef': [T0.E(p) for p in smul(Rt, smul(Rt, xe, xf, KT), E, KT)]}
            okT = all(got[F] == exp_[F] for F in got)
            if isplant:
                plant('PLANT-FP N=%d' % (n + 1), not okT, 'FP coefficient n + 1 breaks the exact tree series')
            else:
                check('C-TREE N=%d' % (n + 1), okT, ' | '.join('%s: %s' % (F, [str(x) for x in got[F]]) for F in got))
    # main T0 tables at K = 4, both N, all five partners: C-EXACT (+ PLANT-MOM), C-GAUSS, R-SERIES; C-SYM (+ PLANT-SYM) at K = 2
    K = 4
    fpairs = [EDGES[o[2]] for o in ORBITS]
    series = {}
    for n in (2, 3):
        guard('v1 main N=%d' % (n + 1))
        bd = Build(G9, n, K, EDGES['b0'], fpairs, JGRID[0], KAPPA, RHO2, 'P3xP3 N=%d' % (n + 1), need_tilts=False)
        bad, done = c_exact(bd.T0, 9, rng, 40, 6)
        check('C-EXACT N=%d T0' % (n + 1), bad == 0 and done > 0, '%d of %d monomials match the alpha-permanent' % (done - bad, done))
        badp, donep = c_exact(bd.T0, 9, rng, 3, 6, perturb=True)
        plant('PLANT-MOM N=%d' % (n + 1), badp > 0, 'one moment + 1e-20 is caught (%d of %d)' % (badp, donep))
        for b, (nm, e, f, d2, _) in enumerate(ORBITS, start=1):
            A1, Ae, Af, Aef = bd.a[('1', 0)], bd.a[('e', 0)], bd.a[('f', b)], bd.a[('ef', b)]
            cs = cov_series(A1, Ae, Af, Aef, K)
            series[(nm, n + 1)] = cs
            okG = (A1[0] == 1 and Ae[0] == fmpq(n, 2) * G9.R(*EDGES[e]) and Af[0] == fmpq(n, 2) * G9.R(*EDGES[f])
                   and cs[0] == fmpq(n, 8) * d2)
            check('C-GAUSS %s N=%d' % (nm, n + 1), okG, 'c2 = %s = (N-1) Delta^2 / 8: %s' % (cs[0], cs[0] == fmpq(n, 8) * d2))
            out('R-SERIES %s N=%d: c2 %s (%s), c3 %s (%s), c4 %s (%s); a_k(1) %s' % (nm, n + 1, cs[0], f6(cs[0]), cs[1], f6(cs[1]),
                cs[2], f6(cs[2]), [f6(x) for x in A1]))
        for b, (nm, e, f, d2, (e2, f2)) in enumerate(ORBITS, start=1):
            bs = Build(G9, n, 2, EDGES[e2], [EDGES[f2]], JGRID[0], KAPPA, RHO2, 'sym %s (%s, %s) N=%d' % (nm, e2, f2, n + 1),
                       need_tilts=False)
            okS = all(bs.a[(F, 0 if F in ('1', 'e') else 1)][k] == bd.a[(F, 0 if F in ('1', 'e') else b)][k] for F in FNAMES for k in range(3))
            check('C-SYM %s N=%d' % (nm, n + 1), okS, 'second member (%s, %s): a_k (k <= 2) equal' % (e2, f2))
        okP = all(bd.a[('ef', 2)][k] == bd.a[('ef', 1)][k] for k in range(3))
        plant('PLANT-SYM N=%d' % (n + 1), not okP, 'O2 against O1 (different orbits) differ')
    # C-H (+ PLANT-H) for the tilts of v2/cert
    okc = G9.tilt([C35 / JGRID[0]] * 9)[2]
    okl = all(G9.tilt([KAPPA / (2 * G9.Lpd[v]) if u == v else fmpq(0) for u in range(9)])[2] for v in range(9))
    cpr = q_ceil(up_q(-(arb(1 - RHO2).log()) / (2 * arb(RHO2))), 64)
    oka = all(ann_rates(G9, cpr / JGRID[0], v)[0] is not None for v in range(9))
    check('C-H P3xP3', okc and okl and oka, 'T1 %s, T2 %s, T3 %s' % (okc, okl, oka))
    plant('PLANT-H', not G9.tilt([1 / G9.Lpd[1] if u == 1 else fmpq(0) for u in range(9)])[2], 'kappa = 2 violates (H)')
    # C-LIT
    c_lit()
    # C-BOUND on P3 (+ PLANT-BOUND)
    c_bound()
    # PLANT-NEG
    t1 = fmpq(1, 100)
    c2 = fmpq(1, 1000)
    Asyn = {'1': [fmpq(1)], 'e': [fmpq(1)], 'f': [fmpq(1)], 'ef': [1 + c2, -8 * c2 / t1, 8 * c2 / (t1 * t1)]}
    L, mono, nneg = phi_scan(Asyn, {F: arb(0) for F in FNAMES}, t1)
    plant('PLANT-NEG', nneg > 0, 'planted dip: %d negative cells, min %s' % (nneg, f6(L)))
    out('READINGS R-SERIES: ' + '; '.join('%s N=%d c2 %s c3 %s c4 %s' % (k[0], k[1], f6(v[0]), f6(v[1]), f6(v[2]))
                                         for k, v in sorted(series.items())))


def c_lit():
    """C-LIT: the riglap2 (RV12_3: matches Lemma 19.1 term by term), float, against this engine on P3 x P3 with pairs (b0, b4)."""
    okc = True
    for fn, want in LIT_SHA.items():
        with open(os.path.join(LIT, fn), 'rb') as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        okc = okc and h == want
    check('C-LIT-COPY', okc, 'lbu_lit_v1 sha256 match: %s' % okc)
    if not okc:
        return
    sys.path.insert(0, LIT)
    import riglap2
    import pseries
    from amom2b import AllMom2
    wf = pseries.w_coeffs(6)
    wd = w_exact(6)
    dw = max(abs(float(wd.get(k, fmpq(0))) - wf.get(k, 0.0)) for k in set(wd) | set(wf))
    check('C-LIT w', dw <= 1e-14, 'max |w exact - w reference| %.2e' % dw)
    KL, n, N = 3, 3, 4
    e, f = EDGES['b0'], EDGES['b4']
    gr = riglap2.Graph(9, {EDGES[x]: 1.0 for x in ELIST}, [e, f], N)
    bd = Build(G9, n, KL, e, [f], JGRID[0], KAPPA, RHO2, 'lit N=4', need_tilts=False)
    R = bd.R

    def to_rig(P, sg):
        d = {}
        for (a, b), p in P.items():
            for m, c in zip(p.monoms(), p.coeffs()):
                d[tuple(m) + (a, 1 if b else 0)] = sg * float(c)
        return d

    def cmp(dr, dm):
        keys = set(dr) | set(dm)
        scale = max([abs(v) for v in dr.values()] + [1e-300])
        return max([abs(dr.get(k, 0.0) - dm.get(k, 0.0)) for k in keys] + [0.0]) / scale
    worst = 0.0
    for F, factors, sh, kmax in (('1', [], 0, KL), ('ef', [('dot', e[0], e[1], 1.0), ('dot', f[0], f[1], 1.0)], 2, 2)):
        guard('C-LIT series ' + F)
        coef = riglap2.Model(gr, kmax + sh, factors).exact()
        key = ('1', 0) if F == '1' else ('ef', 1)
        for k in range(kmax + 1):
            worst = max(worst, cmp(coef[k + sh], to_rig(bd.PS[key][k], 1.0)))
    check('C-LIT series', worst <= 1e-12, 'max relative difference of (F e^H)_k (F = 1, k <= %d; xi_e xi_f, k <= 2): %.2e' % (KL, worst))
    avec, rvec = radii(G9, fmpq(1, 2))
    t = fmpq(1, 120)
    mj = Maj(R, G9, n, avec, rvec, KL)
    mr = riglap2.Majorants(riglap2.Model(gr, KL, []), [float(x) for x in avec], float(t))
    wm = 0.0
    for k in range(1, KL + 2):
        wm = max(wm, cmp(mr.hbar(k).to_dict(), to_rig(mj.h[k], 1.0)))
    db = mj.Dbar('1', bd.ep, None)
    wm = max(wm, cmp(mr.Dbar(KL + 1).to_dict(), to_rig(db[0], 1.0)))
    aa = float(max(avec[e[0]], avec[e[1]]))
    for l in range(0, KL + 2):
        xb = mj.xibar(e[0], e[1], (1, 0), l)
        mine = padd(xb[0], pscale(xb[1], t)) if len(xb) > 1 else xb[0]
        wm = max(wm, cmp(mr.xibar(e[0], e[1], l, aa).to_dict(), to_rig(mine, 1.0)))
    check('C-LIT majorants', wm <= 1e-12, 'max relative difference of h_k, Dbar_%d (F = 1), xibar_l (b0): %.2e' % (KL + 1, wm))
    am = AllMom2(gr.G, gr.n, 2 * KL)
    wa = 0.0
    for k in range(KL + 1):
        P = bd.PS[('1', 0)][k]
        d = {}
        for m, c in zip(P[(0, 0)].monoms(), P[(0, 0)].coeffs()):
            d[tuple(m)] = float(c)
        x = am.E(d) if d else 0.0
        y = float(bd.a[('1', 0)][k])
        wa = max(wa, abs(x - y) / max(abs(y), 1e-300))
    check('C-LIT moments', wa <= 1e-10, 'a_k (F = 1, k <= %d): max relative difference %.2e' % (KL, wa))


def c_bound():
    """C-BOUND: on P3 (exact closed forms) the certified enclosure A_F(t) +- E_F contains the truth (J = 10, 20, 40; N = 3, 4; K = 4);
    PLANT-BOUND: K = 0 without B_rem at N = 4, J = 40 must miss."""
    gt = Graph(3, [(0, 1), (1, 2)])
    sigma = fmpq(2)
    viol = 0
    tot = 0
    for n in (2, 3):
        for K, plantcase in ((4, False), (0, True)):
            if plantcase and n == 2:
                continue
            guard('C-BOUND N=%d K=%d' % (n + 1, K))
            bd = Build(gt, n, K, (0, 1), [(1, 2)], 10, KAPPA, RHO2, 'P3 N=%d K=%d' % (n + 1, K))
            bd.add_sigma(sigma)
            for J in ((40,) if plantcase else (10, 20, 40)):
                tr = tree_truth(n, J)
                t = fmpq(1, J)
                miss = 0
                for F in ('1', 'e', 'ef'):
                    key = (F, 0) if F in ('1', 'e') else (F, 1)
                    tt, th = bd.errors(sigma, J, key, drop_rem=plantcase)
                    Et = tt[0] + tt[1] + tt[2] + tt[3]
                    A = horner(bd.a[key], arb(t))
                    inside = ((A - Et).lower() <= tr[F].lower()) and (tr[F].upper() <= (A + Et).upper())
                    out('BOUND P3 N=%d K=%d J=%d F=%s: A %s, E %s (rem %s tail %s ann %s far %s), truth %s, inside %s' % (
                        n + 1, K, J, F, f6(A), f6(Et), f6(tt[0]), f6(tt[1]), f6(tt[2]), f6(tt[3]), f6(tr[F]), inside))
                    if not inside:
                        miss += 1
                if plantcase:
                    plant('PLANT-BOUND', miss > 0, 'K = 0 without B_rem at J = 40 misses %d of 3' % miss)
                else:
                    viol += miss
                    tot += 3
    check('C-BOUND', viol == 0 and tot > 0, '%d violations in %d enclosures' % (viol, tot))


# ---------------------------------------------------------------- v2 and cert
def run_v2():
    n = 3
    e, f = EDGES['b0'], EDGES['b4']
    for K in (3, 4):
        t0 = cpu()
        bd = Build(G9, n, K, e, [f], JGRID[0], KAPPA, RHO2, 'O2 N=4 K=%d' % K)
        for sigma in SIGMAS:
            bd.add_sigma(sigma)
        best = certify(bd, 1, SIGMAS, JGRID, 'O2 N=4 K=%d' % K)
        if best is None:
            out('R-J1 O2 N=4 K=%d: none on the grid' % K)
        else:
            out('R-J1 O2 N=4 K=%d: J1 %d, sigma %s, L %s; E %s' % (K, best['J1'], best['sigma'], f6(best['L']),
                {F: f6(best['Eu'][F]) for F in FNAMES}))
        out('CPU O2 N=4 K=%d: %.2f s' % (K, cpu() - t0))


def run_cert():
    K = KCERT
    fpairs = [EDGES[o[2]] for o in ORBITS]
    res = {}
    for n in (2, 3):
        t0 = cpu()
        bd = Build(G9, n, K, EDGES['b0'], fpairs, JGRID[0], KAPPA, RHO2, 'cert N=%d K=%d' % (n + 1, K))
        for sigma in SIGMAS:
            bd.add_sigma(sigma)
        for b, (nm, e, f, d2, _) in enumerate(ORBITS, start=1):
            best = certify(bd, b, SIGMAS, JGRID, '%s N=%d K=%d' % (nm, n + 1, K))
            res[(nm, n + 1)] = best
            if best is None:
                out('R-J1 %s N=%d K=%d: none on the grid' % (nm, n + 1, K))
                continue
            out('R-J1 %s N=%d K=%d: J1 %d, sigma %s, L %s (c2 %s); E %s; theta %s' % (nm, n + 1, K, best['J1'], best['sigma'],
                f6(best['L']), f6(fmpq(n, 8) * d2), {F: f6(best['Eu'][F]) for F in FNAMES}, best['ths']))
            if nm == 'O3':
                Acoef = {F: bd.a[(F, 0) if F in ('1', 'e') else (F, b)] for F in FNAMES}
                cs = cov_series(Acoef['1'], Acoef['e'], Acoef['f'], Acoef['ef'], K)
                for J in (100, 150, 200):
                    if J < best['J1']:
                        continue
                    t = fmpq(1, J)
                    Lj, mono, nneg = phi_scan(Acoef, best['Eu'], t, ncell=1)
                    cen = sum((cs[k] * t ** k for k in range(K + 1)), fmpq(0))
                    data = CDATA[(n + 1, J)] * J * J
                    ok = float(Lj) <= data * (1 + 1e-5) and (J != 200 or abs(float(cen) - data) <= 1e-3 * data)
                    check('C-DATA O3 N=%d J=%d' % (n + 1, J), ok, 'certified %s <= data %.6e; central %s' % (f6(Lj), data, f6(cen)))
        out('CPU cert N=%d: %.2f s' % (n + 1, cpu() - t0))
    js = [v['J1'] for v in res.values() if v is not None]
    allc = all(v is not None for v in res.values())
    out('READINGS R-J1: ' + '; '.join('%s N=%d %s' % (k[0], k[1], v['J1'] if v else 'none') for k, v in sorted(res.items())))
    out('READINGS LB_u J1 = %s (all orbits certified on the grid: %s)' % (max(js) if js and allc else 'none', allc))


# ---------------------------------------------------------------- main
def main():
    out('kt_lbu_v1 mode %s LIM %d K %d | python %s | python-flint %s | prec %d' % (MODE, LIM, KCERT, sys.version.split()[0],
        flint.__version__, FLINT.prec))
    status = 'DONE'
    try:
        if MODE == 'v1':
            run_v1()
        elif MODE == 'v2':
            run_v2()
        else:
            run_cert()
    except GuardStop as ex:
        status = 'INCOMPLETE (guard stop at %s)' % ex
    allc = all(CHECKS.values()) if CHECKS else False
    allp = all(PLANTS.values()) if PLANTS else (MODE != 'v1')
    out('CHECKS %s' % CHECKS)
    out('PLANTS %s' % PLANTS)
    if status != 'DONE':
        verdict = 'INCOMPLETE'
    else:
        verdict = 'VALID' if allc and allp else 'INVALID'
    out('SUMMARY mode %s: status %s; checks %d/%d; plants %d/%d; VERDICT %s; cpu %.2f s; wall %.2f s' % (
        MODE, status, sum(CHECKS.values()), len(CHECKS), sum(PLANTS.values()), len(PLANTS), verdict, cpu(), time.time() - T_START))


T_START = time.time()
main()
