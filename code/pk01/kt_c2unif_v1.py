#!/usr/bin/env python3
"""kt_c2unif_v1.py -- pk01 (code/pk01/). The D(beta) float screen of PLAN_C2_UNIFORM_v1 (39323341), step 0
and the exact leading-coefficient table for every edge pair of the uniform 3x3 box (the item 4). DATA ONLY:
float64 quadrature for part A, exact rationals for part B; no proof.
Part A, the object. D(beta) := Cov(s_e, s_f) for c2's pair (e = b6 = (W, SW), f = sS) with all twelve couplings equal to beta: the box
  point (J0..J5, hE, hN, hW) = (beta,)*9 with J_e = J_b7 = beta, and the J_f tilt at J_f = beta. F(c) := E[s_e | s_f = c] and the law
  of c come from the engine; D(beta) = Cov_{P^{J_f}}(c, F) at J_f = beta on the node measure.
Engine. The kt_c2v_v1.py (4e585d9a) lines 71-538 are copied VERBATIM, as in kt_c2int_v1.py (50d3e2b8): imports, the arb reference,
  the sector engine, run_point with the closure W -e- SW -b7- S, epf, shape, g2, planted, creg, summarize. COPIED_RANGES_KT_C2UNIF_v1.txt
  gives the range sha256s. New: this header, the argument lines and the code after the copied block. One copied global is reassigned
  after the block and read at call time: M_CAP = 200 (the sector cap, for the strong points). run_point's nplus argument
  adds nodes above its clip at 160: nplus = max(0, round(56 + 10 sqrt(beta)) - 160).
  Nodes where Den underflows to 0 (far from c = 1 at large beta) get weight 0 in the node measure; their count is printed.
Part A, the grid. beta = 10^(k/4) for k = -12..8 (1e-3 .. 1e2, 21 values) and beta in (150, 200); N in (3, 4). The grid stops at 200:
  beyond it the rows near c = -1 underflow, and run_point's sector test, which reads every row, would then never converge.
Part B, the table (exact, python fractions). The 3x3 grid graph (hub C and rim S, SE, E, NE, N, NW, W, SW; 12 unit edges: b0..b7 and the
  spokes sS, sE, sN, sW). For every unordered edge pair {e, f}:
  - small beta: L_min = the length of the shortest simple cycle containing e and f, and n_cyc = the number of such cycles. The leading
    term of Cov(E_e, E_f) is n_cyc beta^(L_min - 2) N^(1 - L_min) (one cycle of L dot products integrates to N^(1-L); the graph is
    bipartite, so Cov is even in beta);
  - large beta: Delta = R_au + R_bv - R_av - R_bu (effective resistances, unit conductances, e = (a, b), f = (u, v)); the leading term
    is (N-1) Delta^2 / (8 beta^2) (E10's low-temperature expansion, a sketch; the large-beta lemma is to prove it);
  - flags: SHARED (e, f share a vertex: closed at N = 3, 4 by E10 Theorem 1), NOCYCLE (no common cycle: Cov = 0), DELTA0 (Delta = 0).
  Pairs are grouped into classes under the 8 symmetries of the square, one line per class.
Readings, fixed before any run:
  R-D      D(beta) at J_f = beta, per beta and N; a resolved negative is D < -1e-16 with correlation < -1e-6.
  R-SHAPE  the FE** class of F (kt_c2v_v1's shape() on the rows with Den > 0): MONOTONE, THRESHOLD or NEITHER (covers every J_f).
  R-SMALL  D(beta) / (beta^2 / N^3) for beta <= 0.1.
  R-LARGE  beta^2 D(beta) / ((N-1) 25/1152) for beta >= 10 (Delta_u = -5/12 for c2's pair).
  R-TAB    part B's class lines; the list of DELTA0 and NOCYCLE pairs.
  G2 ALARM any resolved negative R-D at a point whose checks pass: report at once.
Checks (must pass):
  C-REG, C-REG2  as kt_c2int_v1 (H and F(1, 1) against the arb reference at P_A, N = 3 and 4, <= 1e-9; tail <= 1e-14).
  C-T1     at beta in (1, 10, 100, 200), both N: the point again with 48 more nodes; |D1 - D2| <= 1e-6 |D1| + 1e-18, same for D at J_f = 0.
  C-MTRUNC every sector sum converged before M_CAP = 200.  C-FIN  num and Den finite, Den >= 0 at the nodes, Den > 0 at some node, and
           |F| <= 1 + 1e-9 where Den > 0.
  C-SMALL  at beta = 1e-3, |R-SMALL - 1| <= 1e-3 at both N (D = beta^2/N^3 + O(beta^4)).
  C-TAB    13 simple cycles; Foster's sum, sum over edges of R_e = 8; c2's pair (b6, sS) has L_min 4, n_cyc 1, Delta^2 = 25/144; L_min,
           n_cyc and Delta^2 constant on every symmetry class.
Must fire (a plant per reading):
  R-D      PLANT-DNEG: F = -c at the first point is a resolved negative; PLANT-DPOS: F = c is not.
  R-SHAPE  PLANT-N reads NEITHER, PLANT-T THRESHOLD, PLANT-M MONOTONE (kt_c2v_v1's planted(), first point, both N).
  C-SMALL  PLANT-SMALL: the same ratio with 1/(N+1)^3 in place of 1/N^3 fails the window.
  R-LARGE  PLANT-LARGE: the ratio with Delta = -1/2 in place of -5/12 differs from R-LARGE by the exact factor (5/6)^2 (sanity of the read).
  R-TAB    PLANT-TAB: on the bowtie (two unit squares sharing one vertex; 7 vertices, 8 edges) every cross pair reads NOCYCLE and
           DELTA0, and Foster's sum is 6.
CPU. RLIMIT_CPU soft LIM, hard LIM + 2; a guard before each beta stops at LIM - 4 s. Price [E]: 12 s at LIM 30; prlimit 32 s = 0.0089
  core-h at cap. Run: env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 TMPDIR=<own tmp> timeout 90
  nice -n 10 prlimit --as=8589934592 --cpu=32 -- python3 -I -B kt_c2unif_v1.py full 30 > <out>.
"""
import resource, sys, time, math
MODES = ('full',)
if len(sys.argv) < 3 or sys.argv[1] not in MODES:
    print('usage: kt_c2unif_v1.py full LIM   (LIM = RLIMIT_CPU soft limit in s, hard LIM + 2)')
    sys.exit(2)
MODE = sys.argv[1]
LIM = int(sys.argv[2])
if not (5 <= LIM <= 30):
    print('bad LIM %d (need 5 <= LIM <= 30)' % LIM)
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 2))
# ---------------------------------------------- copied verbatim from rv60/code/kt_c2v_v1.py (4e585d9a), lines 71-538
import numpy as np
from scipy.special import ive
from flint import arb, arb_mat, ctx
ctx.prec = 256
ctx.cap = 64
TAILTOL = 1e-60
T0 = [0.0]  # cpu() is the process CPU time, imports included, as RLIMIT_CPU counts it


def cpu():
    return time.process_time() - T0[0]


def out(line):
    print(line, flush=True)


# ---------------------------------------------- copied verbatim from pk01/k2b_nframe_v2.py (2f27e450), lines 91-189
def dsec(N, m):
    return (1 if m == 0 else 2) if N == 3 else 2 * m + 1


def dlab(N, l):
    return 2 * l + 1 if N == 3 else (l + 1) ** 2


def jac_a(N, m, n):
    lam = arb(m) + (arb(N) - 2) / 2
    return [(arb(k) * (k + 2 * lam - 1) / ((k + lam - 1) * (k + lam))).sqrt() / 2 for k in range(1, n)]


def jacobi(N, m, n):
    a = jac_a(N, m, n); X = arb_mat(n, n)
    for k in range(1, n):
        X[k - 1, k] = a[k - 1]; X[k, k - 1] = a[k - 1]
    return X


def mu_arb(N, j, J):
    J = arb(J)
    if J == 0:
        return arb(1) if j == 0 else arb(0)
    r = arb(1)
    for i in range(j):
        r = r * (arb(N) / 2 + i)
    return (J / 2) ** j / r * (J * J / 4).hypgeom_0f1(arb(N) / 2 + j)


def mus_arb(N, J, n):
    return [mu_arb(N, k, J) for k in range(n)]


def dmus_arb(N, mv):
    return [(arb(k + N - 2) * mv[k + 1] + (arb(k) * mv[k - 1] if k > 0 else arb(0))) / (2 * k + N - 2) for k in range(len(mv) - 1)]


def dmat(vals, n):
    D = arb_mat(n, n)
    for i in range(n):
        D[i, i] = vals[i]
    return D


def sel(n, ncol):
    S = arb_mat(n, ncol)
    for c in range(min(n, ncol)):
        S[c, c] = arb(1)
    return S


def rows(M, nr, nc):
    R = arb_mat(nr, nc)
    for r in range(nr):
        for c in range(nc):
            R[r, c] = M[r, c]
    return R


def tr(M, nr, nc):
    try:
        return M.transpose()
    except AttributeError:
        R = arb_mat(nc, nr)
        for r in range(nr):
            for c in range(nc):
                R[c, r] = M[r, c]
        return R


def expv(X, h, V, n, ncol):
    if h == 0:
        return V
    ha = arb(h); S = V; term = V; j = 0; ah = abs(h)
    while True:
        j += 1
        term = (X * term) * (ha / j)
        S = S + term
        tb = math.exp((j + 1) * math.log(ah) - math.lgamma(j + 2) + ah)
        if j > 2 * ah and tb < TAILTOL:
            break
    for c in range(ncol):
        nrm = math.sqrt(sum((abs(float(V[r, c].mid())) + float(V[r, c].rad())) ** 2 for r in range(n)))
        rad = tb * nrm * 1.001 + 1e-300
        for r in range(n):
            S[r, c] = S[r, c] + arb(0, rad)
    return S


def polys(N, X, B, kmax):
    out = [B * arb(dlab(N, 0))]
    A0, A1 = B, X * B
    if kmax >= 1:
        out.append(A1 * arb(dlab(N, 1)))
    for k in range(2, kmax + 1):
        A2 = (X * A1 * arb(2 * (k - 1) + N - 2) - A0 * arb(k - 1)) * (arb(1) / (k - 1 + N - 2))
        out.append(A2 * arb(dlab(N, k))); A0, A1 = A1, A2
    return out


# ---------------------------------------------- end of the copied lines; the review code below


PROBES = (-0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9)
M_CAP = 48
SECTOL = 1e-14
LMAX = 24
JES = (0.3, 3.0, 30.0)
JB7S = (1.0, math.inf)
JFS = (0.0, 1.0, 10.0, 100.0)
INF = math.inf
P_A = ('K3 uniform 1', (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0))
P_B = ('K3 lopsided hN 3', (3.0, 0.3, 0.3, 3.0, 3.0, 0.3, 0.3, 3.0, 3.0))
LABS = ('J0', 'J1', 'J2', 'J3', 'J4', 'J5', 'hE', 'hN', 'hW')
CORE = [
    ('K3 uniform 0.3', (0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.0, 0.3)),
    ('K3 uniform 1', (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0)),
    ('K3 uniform 3', (3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 3.0)),
    ('K3 rest 3', (1.0, 1.0, 3.0, 3.0, 3.0, 3.0, 1.0, 0.0, 1.0)),
    ('K3 phi 3', (3.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0)),
    ('K3 hE 3', (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 0.0, 1.0)),
    ('K3 lopsided A3', (3.0, 0.3, 0.3, 3.0, 3.0, 0.3, 3.0, 0.0, 0.3)),
    ('K3 lopsided B3', (0.3, 3.0, 3.0, 0.3, 0.3, 3.0, 0.3, 0.0, 3.0)),
    ('K3 uniform 1 hN 1', (1.0,) * 9),
    ('K3 uniform 1 hN 3', (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 1.0)),
    ('K3 uniform 3 hN 3', (3.0,) * 9),
    ('K3 lopsided hN 3', (3.0, 0.3, 0.3, 3.0, 3.0, 0.3, 0.3, 3.0, 3.0)),
    ('K2b hN~lambda 0.3', (0.3,) * 9),
    ('K6b u1 hN10', (1.0,) * 7 + (10.0, 1.0)),
    ('K6b lop3 hN0', (3.0, 0.3, 0.3, 3.0, 3.0, 0.3, 0.3, 0.0, 3.0)),
    ('K6b lop3 hN10', (3.0, 0.3, 0.3, 3.0, 3.0, 0.3, 0.3, 10.0, 3.0)),
    ('K6b s005 hN0', (0.05,) * 7 + (0.0, 0.05)),
] + [('face %s=0 at (1,)*9' % LABS[k], tuple(0.0 if i == k else 1.0 for i in range(9))) for k in range(9) if LABS[k] != 'hN']
STRONG = [
    ('K6f CB0', (0.1, 0.1, 30.0, 30.0, 30.0, 30.0, 30.0, 0.0, 30.0)),
    ('K6f CB30', (0.1, 0.1, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0)),
    ('K6f C1a', (0.1, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 0.0, 30.0)),
    ('K6f C1b', (30.0, 0.1, 30.0, 30.0, 30.0, 30.0, 30.0, 0.0, 30.0)),
    ('J0 0.1 rest 100', (0.1,) + (100.0,) * 6 + (0.0, 100.0)),
    ('J1 0.1 rest 100', (100.0, 0.1) + (100.0,) * 5 + (0.0, 100.0)),
    ('K2b uniform 30 hN 3', (30.0,) * 7 + (3.0, 30.0)),
    ('K2b uniform 30', (30.0,) * 9),
    ('K2b lopsided 30', (30.0, 0.03, 0.03, 30.0, 30.0, 0.03, 0.03, 30.0, 30.0)),
    ('uniform 100 hN 0', (100.0,) * 7 + (0.0, 100.0)),
    ('hE 100 rest 0.1', (0.1,) * 6 + (100.0, 0.0, 0.1)),
    ('K6f ST J10', (100.0,) * 6 + (10.0, 0.0, 10.0)),
    ('K6f WRSS', (0.3,) * 6 + (30.0, 30.0, 30.0)),
    ('K6f SRWS', (30.0,) * 6 + (0.03, 0.03, 0.03)),
    ('K6f WF', (30.0,) * 6 + (0.01, 30.0, 30.0)),
]
SMOKE = [P_A, ('K2b uniform 30 hN 3', (30.0,) * 7 + (3.0, 30.0))]


def tp2_face(N):
    return [('TP2 face J%g hW%g' % (J, hw), (J,) * 6 + (0.0, 0.0, hw)) for J in (1.0, 5.0, 30.0)
            for hw in ((N - 1) / 2.0 + 0.5, 3.0, 10.0)]


def atil(N, m, t):
    # A_m(t) e^{-t} on S^{N-2}: ive(m, t) at N = 3; sqrt(pi / (2t)) ive(m + 1/2, t) at N = 4, with its t -> 0 limit
    if N == 3:
        return ive(m, t)
    tt = np.where(t > 1e-12, t, 1.0)
    v = np.sqrt(np.pi / (2.0 * tt)) * ive(m + 0.5, tt)
    lim = (1.0 - t) if m == 0 else np.zeros_like(t)
    return np.where(t > 1e-12, v, lim)


def xgrid(N, n):
    # nodes (ascending) and probability weights of d nu(x) ~ (1 - x^2)^{(N-3)/2} dx
    if N == 3:
        x, w = np.polynomial.legendre.leggauss(n)
    else:
        th = np.arange(n, 0, -1) * (np.pi / (n + 1))
        x = np.cos(th)
        w = (np.pi / (n + 1)) * np.sin(th) ** 2
    return x, w / np.sum(w)


class KCache:
    # e^{-J} K_J^m on the grids 'xx' (nodes by nodes) and 'rx' (rows by nodes), for one point and one N
    def __init__(s, N, x, cr):
        s.N = N
        s.grid = {'xx': (x, x), 'rx': (cr, x)}
        s.base = {}
        s.at = {}

    def geo(s, J, g):
        key = (J, g)
        if key not in s.base:
            a, b = s.grid[g]
            sa = np.sqrt(np.clip(1.0 - a * a, 0.0, None))
            sb = np.sqrt(np.clip(1.0 - b * b, 0.0, None))
            xy = np.outer(a, b)
            ss = np.outer(sa, sb)
            s.base[key] = (xy, ss, J * ss, np.exp(J * (xy + ss - 1.0)))
        return s.base[key]

    def atm(s, J, g, m):
        key = (J, g, m)
        if key not in s.at:
            s.at[key] = atil(s.N, m, s.geo(J, g)[2])
        return s.at[key]

    def K(s, J, g, m):
        return s.geo(J, g)[3] * s.atm(J, g, m)

    def dK(s, J, g, m):
        # e^{-J} d/dJ K_J^m = x y K + s s' e^{J(x y + s s' - 1)} (A_m' e^{-t})(t)
        xy, ss, t, E = s.geo(J, g)
        N = s.N
        if N == 3 and m == 0:
            da = s.atm(J, g, 1)
        else:
            lo = s.atm(J, g, m - 1) if m > 0 else 0.0
            da = (m * lo + (m + N - 3) * s.atm(J, g, m + 1)) / (2 * m + N - 3)
        return xy * (E * s.atm(J, g, m)) + ss * E * da

    def drop(s, m):
        for key in [k for k in s.at if k[2] < m]:
            del s.at[key]


def chain(KC, m, Pt, x, w):
    # Z^m(c, x_W) without the W weight: S (rows) -b0- SE -b1- E -b2- NE -b3- N -b4- NW -b5- W
    J0, J1, J2, J3, J4, J5, hE, hN, hW = Pt
    Z = KC.K(J0, 'rx', m) * w
    Z = (Z @ KC.K(J1, 'xx', m)) * (w * np.exp(hE * (x - 1.0)))
    Z = (Z @ KC.K(J2, 'xx', m)) * w
    Z = (Z @ KC.K(J3, 'xx', m)) * (w * np.exp(hN * (x - 1.0)))
    Z = (Z @ KC.K(J4, 'xx', m)) * w
    Z = (Z @ KC.K(J5, 'xx', m)) * np.exp(hW * (x - 1.0))
    return Z


def close_terms(KC, m, Zm, w, je, jb):
    # sector-m terms of Den and Num for the closure W -e- SW -b7- S (b7 = inf: W -e- S)
    Zw = Zm * w
    if jb == INF:
        return np.sum(Zw * KC.K(je, 'rx', m), axis=1), np.sum(Zw * KC.dK(je, 'rx', m), axis=1)
    Kb = KC.K(jb, 'rx', m) * w
    return np.sum((Zw @ KC.K(je, 'xx', m)) * Kb, axis=1), np.sum((Zw @ KC.dK(je, 'xx', m)) * Kb, axis=1)


def run_point(Pt, N, jes, jb7s, nplus=0):
    jm = max(list(Pt) + list(jes) + [j for j in jb7s if j != INF])
    n = int(min(160, max(72, round(56 + 10 * math.sqrt(jm))))) + nplus
    x, w = xgrid(N, n)
    cr = np.unique(np.concatenate([x, np.array(PROBES), np.array([-1.0, 1.0])]))
    node = np.searchsorted(cr, x)
    KC = KCache(N, x, cr)
    Zs = {0: chain(KC, 0, Pt, x, w), 1: chain(KC, 1, Pt, x, w)}
    sx = np.sqrt(1.0 - x * x)
    sc = np.sqrt(np.clip(1.0 - cr * cr, 0.0, None))
    hd = Zs[0] @ w
    hn = cr * (Zs[0] @ (w * x)) + sc * (Zs[1] @ (w * sx))
    combos = [(je, jb) for je in jes for jb in jb7s] + [(0.0, 1.0), (0.0, INF)]
    den = dict((k, np.zeros(len(cr))) for k in combos)
    num = dict((k, np.zeros(len(cr))) for k in combos)
    quiet = dict((k, 0) for k in combos)
    used = {}
    live = list(combos)
    m = 0
    while live and m <= M_CAP:
        Zm = Zs[m] if m in Zs else chain(KC, m, Pt, x, w)
        dm = dsec(N, m)
        for k in list(live):
            dd, nn = close_terms(KC, m, Zm, w, k[0], k[1])
            den[k] = den[k] + dm * dd
            num[k] = num[k] + dm * nn
            if m >= 1:
                with np.errstate(divide='ignore', invalid='ignore'):
                    rel = max(float(np.max(np.abs(dm * dd) / den[k])), float(np.max(np.abs(dm * nn) / den[k])))
                quiet[k] = quiet[k] + 1 if rel < SECTOL else 0
                if quiet[k] >= 2:
                    used[k] = m
                    live.remove(k)
        KC.drop(m)
        m += 1
    return dict(n=n, x=x, w=w, cr=cr, node=node, hn=hn, hd=hd, num=num, den=den, used=used, trunc=list(live))


def epf(R, num, den):
    nd = R['node']
    return float(np.sum(R['w'] * num[nd]) / np.sum(R['w'] * den[nd]))


def shape(cr, F, ep):
    rng = float(np.max(F) - np.min(F))
    tol = max(1e-9 * rng, 1e-14)
    k = len(F) - 1
    while k > 0 and F[k - 1] <= F[k] + tol:
        k -= 1
    if k == 0:
        return 'MONOTONE', float(cr[0]), -INF, None, tol, rng
    left = F[:k] - ep
    i = int(np.argmax(left))
    ex = float(left[i])
    return ('THRESHOLD' if ex <= tol else 'NEITHER'), float(cr[k]), ex, float(cr[i]), tol, rng


def g2(R, F, den):
    nd = R['node']
    c = R['cr'][nd]
    f = F[nd]
    base = R['w'] * den[nd]
    vals = []
    for jf in JFS:
        p = base * np.exp(jf * (c - 1.0))
        p = p / np.sum(p)
        mc = float(np.sum(p * c))
        mf = float(np.sum(p * f))
        cov = float(np.sum(p * (c - mc) * (f - mf)))
        sd = math.sqrt(max(float(np.sum(p * (c - mc) ** 2)), 0.0) * max(float(np.sum(p * (f - mf) ** 2)), 0.0))
        vals.append((jf, cov, cov / sd if sd > 0.0 else 0.0))
    return vals


def planted(R):
    cr = R['cr']
    pn = 0.5 * np.exp(-((cr + 0.5) / 0.15) ** 2) - 0.5 * np.exp(-((cr - 0.2) / 0.15) ** 2) + 0.1 * cr
    pt = np.where(cr < 0.0, -0.05 * (1.0 + np.cos(2.0 * np.pi * cr)), cr * cr)
    pm = cr.copy()
    res = {}
    for name, f in (('PLANT-N', pn), ('PLANT-T', pt), ('PLANT-M', pm)):
        res[name] = shape(cr, f, epf(R, f * R['hd'], R['hd']))[0]
    return res


def rho(N, J):
    return 1.0 if J == INF else float(ive(N / 2.0, J) / ive(N / 2.0 - 1.0, J))


def probe_idx(R):
    return [int(np.searchsorted(R['cr'], p)) for p in PROBES]


def zlab(N, Pt, lcl):
    # pk01's Z_{L,l} (l <= LMAX, L <= lcl) on the direct chain, with the copied functions; arb at ctx.prec
    J0, J1, J2, J3, J4, J5, hE, hN, hW = Pt
    n0 = LMAX + lcl + 40 + int(math.ceil(12.0 * math.sqrt(max(Pt) + 1.0)))
    mu = {}
    for J in (J0, J1, J2, J3, J4, J5):
        if J not in mu:
            mu[J] = mus_arb(N, J, n0 + 1)
    Dphi = [mu[J0][k] * mu[J1][k] for k in range(n0)]
    D23 = [mu[J2][k] * mu[J3][k] for k in range(n0)]
    D45 = [mu[J4][k] * mu[J5][k] for k in range(n0)]
    L1 = lcl + 1
    Z = [[arb(0) for _ in range(L1)] for _ in range(LMAX + 1)]
    for m in range(L1):
        n = n0 - m
        nc = L1 - m
        dm = dsec(N, m)
        X = jacobi(N, m, n)
        SelL = sel(n, nc)
        u = polys(N, X, SelL, LMAX)
        dp = dmat(Dphi[m:], n)
        d23 = dmat(D23[m:], n)
        d45 = dmat(D45[m:], n)
        Wv = expv(X, hW, SelL, n, nc)
        NDW = expv(X, hN, d45 * Wv, n, nc)
        VZ = dp * expv(X, hE, d23 * NDW, n, nc)
        for l in range(LMAX + 1):
            P = tr(u[l], n, nc) * VZ
            for c in range(nc):
                Z[l][m + c] += dm * P[c, c]
    return Z, n0


def gegen(N, c):
    ca = arb(c)
    P = [arb(1), ca]
    for k in range(2, LMAX + 1):
        P.append((ca * P[k - 1] * (2 * k + N - 4) - P[k - 2] * (k - 1)) / (k + N - 3))
    return P


def ref_vals(N, Z, c, lcl, je, jb):
    P = gegen(N, c)
    rl = range(LMAX + 1)
    H = sum((Z[l][1] * P[l] for l in rl), arb(0)) / (sum((Z[l][0] * P[l] for l in rl), arb(0)) * N)
    Hw = (sum((Z[l][1] * P[l] * dlab(N, l) for l in rl), arb(0))
          / sum((Z[l][0] * P[l] * dlab(N, l) for l in rl), arb(0)))
    F = None
    if je is not None:
        mue = mus_arb(N, je, lcl + 2)
        dmue = dmus_arb(N, mue)
        mub = mus_arb(N, jb, lcl + 1)
        nf = sum((P[l] * Z[l][L] * dmue[L] * mub[L] for l in rl for L in range(lcl + 1)), arb(0))
        df = sum((P[l] * Z[l][L] * mue[L] * mub[L] for l in rl for L in range(lcl + 1)), arb(0))
        F = float((nf / df).mid())
    return float(H.mid()), float(Hw.mid()), F


def creg(N, Pt, lcl, with_f):
    R = run_point(Pt, N, (1.0,), (1.0,))
    pi = probe_idx(R)
    Hp = R['hn'] / R['hd']
    k = (1.0, 1.0)
    Fp = R['num'][k] / R['den'][k]
    Z, n0 = zlab(N, Pt, lcl)
    dh = 0.0
    dw = 0.0
    df = 0.0
    for j, c in enumerate(PROBES):
        H, Hw, F = ref_vals(N, Z, c, lcl, 1.0 if with_f else None, 1.0)
        dh = max(dh, abs(H - float(Hp[pi[j]])))
        dw = max(dw, abs(Hw - float(Hp[pi[j]])))
        if with_f:
            df = max(df, abs(F - float(Fp[pi[j]])))
    z00 = abs(float(Z[0][0].mid()))
    tail = max(abs(float(Z[LMAX][L].mid())) for L in range(lcl + 1)) / z00
    return dh, dw, df, tail, n0, R['n']


def summarize(name, N, R, jes, jb7s, recs, ck):
    cr = R['cr']
    F0 = R['hn'] / R['hd']
    for k in list(R['den'].keys()):
        d = R['den'][k]
        if not (np.all(np.isfinite(d)) and np.all(d > 0.0)):
            ck['fin'].append((name, N, k))
    if not (np.all(np.isfinite(R['hd'])) and np.all(R['hd'] > 0.0) and np.all(np.abs(F0) <= 1.0 + 1e-9)):
        ck['fin'].append((name, N, 'H'))
    for jb in (1.0, INF):
        Fc = R['num'][(0.0, jb)] / R['den'][(0.0, jb)]
        ck['id0'] = max(ck['id0'], float(np.max(np.abs(Fc - rho(N, jb) * F0))))
    for k in R['trunc']:
        ck['mtrunc'].append((name, N, k))
    parts = []
    items = [((0.0, None), F0, R['hd'], R['hn'])] + [((je, jb), R['num'][(je, jb)] / R['den'][(je, jb)], R['den'][(je, jb)],
                                                      R['num'][(je, jb)]) for je in jes for jb in jb7s]
    for (key, F, den, num) in items:
        if np.any(np.abs(F) > 1.0 + 1e-9):
            ck['fin'].append((name, N, key))
        ep = epf(R, num, den)
        kind, s0, ex, at, tol, rng = shape(cr, F, ep)
        gv = g2(R, F, den)
        gmin = min(v[1] for v in gv)
        endok = bool(F[0] <= ep + tol)
        rec = dict(name=name, N=N, je=key[0], jb=key[1], kind=kind, s0=s0, ex=ex, at=at, tol=tol, rng=rng, ep=ep,
                   fm1=float(F[0]), fp1=float(F[-1]), endok=endok, g2=gv, used=R['used'].get(key, 1))
        recs.append(rec)
        jbs = '-' if key[1] is None else ('inf' if key[1] == INF else '%g' % key[1])
        parts.append('F(%g,%s) %s s0 %.4f%s E_P %.6g F(-1) %.6g F(1) %.6g G2min %.3e sect %s' % (
            key[0], jbs, kind, s0, '' if kind == 'MONOTONE' else ' ex %.3e at %.4f' % (ex, at), ep, F[0], F[-1], gmin,
            rec['used']))
    return ' | '.join(parts)
# ---------------------------------------------- end of the lines copied from rv60/code/kt_c2v_v1.py; pk01 code below
from fractions import Fraction as Frac

M_CAP = 200  # sector cap, read by run_point at call time (raised for the strong points)
BETAS = tuple(10.0 ** (k / 4.0) for k in range(-12, 9)) + (150.0, 200.0)
T1_BETAS = (1.0, 10.0, 100.0, 200.0)
NEG_ABS = 1e-16
NEG_COR = 1e-6
LARGE_COEF = 25.0 / 1152.0  # times (N - 1): (N - 1) Delta_u^2 / 8 with Delta_u = -5/12 (c2's pair, unit box)


def nplus_for(beta):
    return max(0, int(round(56 + 10 * math.sqrt(beta))) - 160)


def node_arrays(R, key):
    nd = R['node']
    c = R['cr'][nd]
    num = R['num'][key][nd]
    den = R['den'][key][nd]
    fin = bool(np.all(np.isfinite(num)) and np.all(np.isfinite(den)) and np.all(den >= 0.0))
    ok = np.isfinite(num) & np.isfinite(den) & (den > 0.0)
    dsafe = np.where(ok, den, 1.0)
    w = np.where(ok, R['w'] * dsafe, 0.0)
    F = np.where(ok, np.where(ok, num, 0.0) / dsafe, 0.0)
    return c, F, w, ok, fin


def cov_tilt(c, F, w, jf):
    # Cov_{P^{jf}}(c, F) with P^{jf} ~ w e^{jf (c - 1)} on the nodes, and its correlation (as kt_c2v_v1's g2)
    p = w * np.exp(jf * (c - 1.0))
    s = float(np.sum(p))
    if not s > 0.0:
        return float('nan'), float('nan')
    p = p / s
    mc = float(np.sum(p * c))
    mf = float(np.sum(p * F))
    cov = float(np.sum(p * (c - mc) * (F - mf)))
    sd = math.sqrt(max(float(np.sum(p * (c - mc) ** 2)), 0.0) * max(float(np.sum(p * (F - mf) ** 2)), 0.0))
    return cov, (cov / sd if sd > 0.0 else 0.0)


def resolved_neg(d, cor):
    return (d < -NEG_ABS) and (cor < -NEG_COR)


def unif_eval(beta, N, extra=0):
    Pt = (beta,) * 9
    R = run_point(Pt, N, (beta,), (beta,), nplus=nplus_for(beta) + extra)
    key = (beta, beta)
    c, F, w, ok, fin = node_arrays(R, key)
    d, cor = cov_tilt(c, F, w, beta)
    d0, cor0 = cov_tilt(c, F, w, 0.0)
    num_r = R['num'][key]
    den_r = R['den'][key]
    okr = np.isfinite(num_r) & np.isfinite(den_r) & (den_r > 0.0)
    sw = float(np.sum(w))
    ep = float(np.sum(w * F)) / sw if sw > 0.0 else float('nan')
    kind = 'NONE'
    if int(np.sum(okr)) > 2:
        kind = shape(R['cr'][okr], num_r[okr] / den_r[okr], ep)[0]
    fmax = float(np.max(np.abs(F[ok]))) if bool(np.any(ok)) else float('inf')
    fin = fin and bool(np.any(ok)) and fmax <= 1.0 + 1e-9
    return dict(R=R, c=c, F=F, w=w, d=d, cor=cor, d0=d0, cor0=cor0, kind=kind, ep=ep, n=R['n'], used=R['used'].get(key, -1),
                trunc=bool(R['trunc']), under=int(np.sum(~ok)), fin=fin)


def part_a(checks, fires):
    recs = []
    stopped = False
    for beta in BETAS:
        for N in (3, 4):
            if cpu() > LIM - 4.0:
                out('GUARD STOP before beta %g N=%d, cpu %.2f s' % (beta, N, cpu()))
                stopped = True
                break
            t0 = cpu()
            r = unif_eval(beta, N)
            r['beta'] = beta
            r['N'] = N
            if beta == BETAS[0]:
                pl = planted(r['R'])
                for key, want in (('PLANT-N', 'NEITHER'), ('PLANT-T', 'THRESHOLD'), ('PLANT-M', 'MONOTONE')):
                    fires[key] = fires.get(key, True) and pl[key] == want
                dn, cn = cov_tilt(r['c'], -r['c'], r['w'], beta)
                dp, cp = cov_tilt(r['c'], r['c'].copy(), r['w'], beta)
                fires['PLANT-DNEG'] = fires.get('PLANT-DNEG', True) and resolved_neg(dn, cn)
                fires['PLANT-DPOS'] = fires.get('PLANT-DPOS', True) and not resolved_neg(dp, cp)
                out('PLANTED at beta %g N=%d: %s; PLANT-DNEG cov %.3e cor %.4f; PLANT-DPOS cov %.3e cor %.4f' % (
                    beta, N, ', '.join('%s %s' % (k, pl[k]) for k in sorted(pl)), dn, cn, dp, cp))
            del r['R']
            t1s = ''
            if beta in T1_BETAS:
                r2 = unif_eval(beta, N, extra=48)
                dd = abs(r['d'] - r2['d'])
                dd0 = abs(r['d0'] - r2['d0'])
                r['t1'] = bool(dd <= 1e-6 * abs(r['d']) + 1e-18 and dd0 <= 1e-6 * abs(r['d0']) + 1e-18)
                t1s = ' | C-T1 n %d vs %d: |dD| %.2e, |dD0| %.2e, %s' % (r['n'], r2['n'], dd, dd0, 'ok' if r['t1'] else 'FAIL')
            rs = r['d'] / (beta * beta / N ** 3)
            rl = beta * beta * r['d'] / ((N - 1) * LARGE_COEF)
            out('UNIF beta %.6g N=%d n %d sect %d under %d | D(J_f=beta) %.6e cor %.4f | D(J_f=0) %.6e cor %.4f | shape %s | '
                'R-SMALL %.6f | R-LARGE %.6f%s | cpu %.2f s' % (beta, N, r['n'], r['used'], r['under'], r['d'], r['cor'], r['d0'],
                                                             r['cor0'], r['kind'], rs, rl, t1s, cpu() - t0))
            recs.append(r)
        if stopped:
            break
    return recs, stopped


GV = {'C': (0, 0), 'S': (0, -1), 'SE': (1, -1), 'E': (1, 0), 'NE': (1, 1), 'N': (0, 1), 'NW': (-1, 1), 'W': (-1, 0),
      'SW': (-1, -1)}
POS2V = dict((p, v) for v, p in GV.items())
ENAMES = [('b0', 'S', 'SE'), ('b1', 'SE', 'E'), ('b2', 'E', 'NE'), ('b3', 'NE', 'N'), ('b4', 'N', 'NW'), ('b5', 'NW', 'W'),
          ('b6', 'W', 'SW'), ('b7', 'SW', 'S'), ('sS', 'C', 'S'), ('sE', 'C', 'E'), ('sN', 'C', 'N'), ('sW', 'C', 'W')]
SYMS = [lambda x, y: (x, y), lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (-x, -y),
        lambda x, y: (y, x), lambda x, y: (-y, x), lambda x, y: (y, -x), lambda x, y: (-y, -x)]


def simple_cycles(verts, edges):
    # every simple cycle once, as a frozenset of edge names; each cycle is found from its first vertex in verts
    adj = dict((v, []) for v in verts)
    for (nm, u, v) in edges:
        adj[u].append((v, nm))
        adj[v].append((u, nm))
    order = dict((v, i) for i, v in enumerate(verts))
    found = set()
    res = []

    def dfs(start, cur, visited, used):
        for (nx, nm) in adj[cur]:
            if nm in used:
                continue
            if nx == start:
                if len(used) >= 2:
                    cyc = frozenset(used | {nm})
                    if cyc not in found:
                        found.add(cyc)
                        res.append(cyc)
            elif nx not in visited and order[nx] > order[start]:
                dfs(start, nx, visited | {nx}, used | {nm})

    for s in verts:
        dfs(s, s, frozenset([s]), frozenset())
    return res


def resistances(verts, edges):
    # exact effective resistances, unit conductances; the graph must be connected; verts[0] is grounded
    idx = dict((v, i) for i, v in enumerate(verts))
    n = len(verts)
    L = [[Frac(0)] * n for _ in range(n)]
    for (nm, u, v) in edges:
        a, b = idx[u], idx[v]
        L[a][a] += 1
        L[b][b] += 1
        L[a][b] -= 1
        L[b][a] -= 1
    m = n - 1
    A = [[L[i + 1][j + 1] for j in range(m)] + [Frac(1) if k == i else Frac(0) for k in range(m)] for i in range(m)]
    for col in range(m):
        piv = [r for r in range(col, m) if A[r][col] != 0][0]
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for r in range(m):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[col])]
    G = [[Frac(0)] * n for _ in range(n)]
    for i in range(m):
        for j in range(m):
            G[i + 1][j + 1] = A[i][m + j]
    R = {}
    for u in verts:
        for v in verts:
            R[(u, v)] = G[idx[u]][idx[u]] + G[idx[v]][idx[v]] - 2 * G[idx[u]][idx[v]]
    return R


def pair_table(verts, edges):
    cyc = simple_cycles(verts, edges)
    R = resistances(verts, edges)
    ends = dict((nm, (u, v)) for (nm, u, v) in edges)
    names = [e[0] for e in edges]
    rows = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            e, f = names[i], names[j]
            a, b = ends[e]
            u, v = ends[f]
            lens = [len(cc) for cc in cyc if e in cc and f in cc]
            if lens:
                L = min(lens)
                nc = sum(1 for x in lens if x == L)
            else:
                L = 0
                nc = 0
            delta = R[(a, u)] + R[(b, v)] - R[(a, v)] - R[(b, u)]
            rows.append(dict(e=e, f=f, shared=len(set([a, b]) & set([u, v])) > 0, L=L, nc=nc, delta=delta))
    foster = sum((R[ends[nm]] for nm in names), Frac(0))
    return cyc, R, rows, foster


def edge_image(nm, sym, ends):
    u, v = ends[nm]
    a = POS2V[sym(*GV[u])]
    b = POS2V[sym(*GV[v])]
    for (n2, x, y) in ENAMES:
        if set([x, y]) == set([a, b]):
            return n2
    raise ValueError('edge image of %s' % nm)


def class_key(e, f, ends):
    best = None
    for s in SYMS:
        p = tuple(sorted((edge_image(e, s, ends), edge_image(f, s, ends))))
        if best is None or p < best:
            best = p
    return best


def part_b(checks, fires):
    verts = ['C', 'S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']
    cyc, R, rows, foster = pair_table(verts, ENAMES)
    ends = dict((nm, (u, v)) for (nm, u, v) in ENAMES)
    classes = {}
    for r in rows:
        classes.setdefault(class_key(r['e'], r['f'], ends), []).append(r)
    const_ok = True
    for k in sorted(classes):
        rs = classes[k]
        if (len(set(r['delta'] ** 2 for r in rs)) != 1 or len(set((r['L'], r['nc']) for r in rs)) != 1
                or len(set(r['shared'] for r in rs)) != 1):
            const_ok = False
        r0 = rs[0]
        d2 = r0['delta'] ** 2
        flags = [x for (x, cond) in (('SHARED', r0['shared']), ('NOCYCLE', r0['L'] == 0), ('DELTA0', d2 == 0)) if cond]
        out('TAB class %s-%s (size %d): L_min %d, n_cyc %d, small beta %d beta^%d N^%d; Delta^2 %s, large beta (N-1) Delta^2/8 '
            '= %.6f/beta^2 at N=3, %.6f/beta^2 at N=4; flags %s' % (k[0], k[1], len(rs), r0['L'], r0['nc'], r0['nc'], r0['L'] - 2,
                                                                    1 - r0['L'], d2, float(2 * d2 / 8), float(3 * d2 / 8),
                                                                    ' '.join(flags) or 'none'))
    c2 = [r for r in rows if set([r['e'], r['f']]) == set(['b6', 'sS'])]
    c2ok = len(c2) == 1 and c2[0]['L'] == 4 and c2[0]['nc'] == 1 and c2[0]['delta'] ** 2 == Frac(25, 144)
    checks['C-TAB'] = bool(len(cyc) == 13 and foster == 8 and const_ok and c2ok)
    d0 = [r for r in rows if r['delta'] == 0]
    nc0 = [r for r in rows if r['L'] == 0]
    out('READINGS R-TAB: %d pairs in %d classes; simple cycles %d; Foster sum %s; class constancy %s; c2 pair check %s; SHARED pairs '
        '%d (closed at N = 3, 4 by E10 Theorem 1); DELTA0 pairs %d: %s; NOCYCLE pairs %d' % (
            len(rows), len(classes), len(cyc), foster, const_ok, c2ok, sum(1 for r in rows if r['shared']), len(d0),
            ' '.join('%s-%s' % (r['e'], r['f']) for r in d0) or 'none', len(nc0)))
    bv = ['X', 'A1', 'A2', 'A3', 'B1', 'B2', 'B3']
    be = [('a1', 'X', 'A1'), ('a2', 'A1', 'A2'), ('a3', 'A2', 'A3'), ('a4', 'A3', 'X'),
          ('c1', 'X', 'B1'), ('c2', 'B1', 'B2'), ('c3', 'B2', 'B3'), ('c4', 'B3', 'X')]
    bcyc, bR, brows, bfoster = pair_table(bv, be)
    cross = [r for r in brows if r['e'][0] != r['f'][0]]
    fires['PLANT-TAB'] = bool(len(cross) == 16 and all(r['L'] == 0 and r['delta'] == 0 for r in cross) and bfoster == 6
                              and len(bcyc) == 2)
    out('PLANTED PLANT-TAB (bowtie): cycles %d, Foster sum %s, cross pairs %d, all NOCYCLE and DELTA0: %s' % (
        len(bcyc), bfoster, len(cross), fires['PLANT-TAB']))


def main():
    import hashlib
    with open(__file__, 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    out('kt_c2unif_v1 sha256 %s %s' % (sha, __file__))
    out('MODE=%s LIM=%d (RLIMIT_CPU soft %d, hard %d); numpy %s; flint ctx.prec %d, ctx.cap %d; M_CAP %d; betas %s' % (
        MODE, LIM, LIM, LIM + 2, np.__version__, ctx.prec, ctx.cap, M_CAP, ', '.join('%.4g' % b for b in BETAS)))
    checks = {}
    fires = {}
    part_b(checks, fires)
    dhm = 0.0
    dwm = INF
    dfm = 0.0
    tailm = 0.0
    for N in (3, 4):
        dh, dw, df, tail, n0, n = creg(N, P_A[1], 5, True)
        dhm = max(dhm, dh)
        dwm = min(dwm, dw)
        dfm = max(dfm, df)
        tailm = max(tailm, tail)
        out('C-REG %s N=%d (arb KTN %d, LMAX %d, LCL 5; quadrature n %d): max |H - H_ref| %.2e; l.104 formula miss %.2e; tail %.2e; '
            'C-REG2 F(1,1) max |F - F_ref| %.2e; cpu %.2f s' % (P_A[0], N, n0, LMAX, n, dh, dw, tail, df, cpu()))
    checks['C-REG'] = dhm <= 1e-9 and tailm <= 1e-14
    checks['C-REG2'] = dfm <= 1e-9
    fires['REG-MISS'] = dwm > 1e-3
    recs, stopped = part_a(checks, fires)
    complete = (not stopped) and len(recs) == 2 * len(BETAS)
    checks['C-FIN'] = bool(recs) and all(r['fin'] for r in recs)
    checks['C-MTRUNC'] = bool(recs) and not any(r['trunc'] for r in recs)
    t1r = [r for r in recs if 't1' in r]
    checks['C-T1'] = len(t1r) == 2 * len(T1_BETAS) and all(r['t1'] for r in t1r)
    small = [r for r in recs if r['beta'] == BETAS[0]]
    rsm = [r['d'] / (r['beta'] ** 2 / r['N'] ** 3) for r in small]
    checks['C-SMALL'] = len(small) == 2 and all(abs(x - 1.0) <= 1e-3 for x in rsm)
    rsw = [r['d'] / (r['beta'] ** 2 / (r['N'] + 1) ** 3) for r in small]
    fires['PLANT-SMALL'] = len(small) == 2 and all(abs(x - 1.0) > 1e-3 for x in rsw)
    big = [r for r in recs if r['beta'] >= 10.0]
    pl_ok = True
    for r in big:
        rl = r['beta'] ** 2 * r['d'] / ((r['N'] - 1) * LARGE_COEF)
        rlw = r['beta'] ** 2 * r['d'] / ((r['N'] - 1) / 32.0)
        pl_ok = pl_ok and abs(rlw - rl * 25.0 / 36.0) <= 1e-12 * abs(rl) + 1e-300
    fires['PLANT-LARGE'] = bool(big) and pl_ok
    negs = [r for r in recs if resolved_neg(r['d'], r['cor'])]
    out('READINGS R-D: %d points; resolved negatives (G2 ALARM) %d; smallest D(J_f=beta) %.6e at beta %.4g N=%d; smallest correlation '
        '%.4f' % (len(recs), len(negs), min(r['d'] for r in recs) if recs else float('nan'),
                  min(recs, key=lambda r: r['d'])['beta'] if recs else float('nan'), min(recs, key=lambda r: r['d'])['N'] if recs else 0,
                  min(r['cor'] for r in recs) if recs else float('nan')))
    for r in negs:
        out('  G2 ALARM beta %.6g N=%d: D %.6e, correlation %.4f' % (r['beta'], r['N'], r['d'], r['cor']))
    kinds = {}
    for r in recs:
        kinds[r['kind']] = kinds.get(r['kind'], 0) + 1
    out('READINGS R-SHAPE: %s' % ', '.join('%s %d' % (k, kinds[k]) for k in sorted(kinds)))
    out('READINGS R-SMALL (beta <= 0.1): %s' % '; '.join('beta %.4g N=%d %.6f' % (r['beta'], r['N'], r['d'] / (r['beta'] ** 2 / r['N'] ** 3))
                                                          for r in recs if r['beta'] <= 0.1 + 1e-12))
    out('READINGS R-LARGE (beta >= 10): %s' % '; '.join('beta %.4g N=%d %.6f' % (r['beta'], r['N'], r['beta'] ** 2 * r['d'] / ((r['N'] - 1) * LARGE_COEF))
                                                         for r in big))
    for key in ('PLANT-N', 'PLANT-T', 'PLANT-M', 'PLANT-DNEG', 'PLANT-DPOS', 'PLANT-SMALL', 'PLANT-LARGE', 'PLANT-TAB'):
        fires.setdefault(key, False)
    ok = all(checks.values()) and all(fires.values())
    valid = ok and complete
    why = [k for k in sorted(checks) if not checks[k]] + [k for k in sorted(fires) if not fires[k]] + ([] if complete else ['INCOMPLETE'])
    out('CHECKS %s | MUST-FIRE %s' % (checks, fires))
    out('VERDICT %s%s' % ('VALID' if valid else 'INVALID', '' if valid else ' (%s)' % ', '.join(why)))
    if valid:
        out('RESULT G2 ALARM %s' % ('none' if not negs else '%d resolved negatives: report at once' % len(negs)))
    out('SUMMARY %s: %s; points reached %d of %d%s; cpu %.2f s' % (
        MODE, 'CHECKS PASS' if ok else 'CHECK FAILED', len(recs), 2 * len(BETAS), '' if complete else ' (INCOMPLETE)', cpu()))


if __name__ == '__main__':
    main()
