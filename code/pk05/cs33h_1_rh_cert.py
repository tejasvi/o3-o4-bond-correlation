#!/usr/bin/env python3
# cs33h_1_rh_cert.py (pk05, P-RH Stage B v1_8 of cs33h_rh_cert 4120f9ee): certified cover of GKS-II on
# the uniform 3 x n strip, N = 3, 4, J in [20, 300], for every pair of edges of every strip with n >= 4 columns, by the coverage table below.
# v1_1 (cs33b): family Taylor models of degree K_F, each interval certified in two items (part A far pairs, part B near pairs, or B as
# Bh + Bv), each recomputing the spectral part; inner products from one BLAS Gram product. v1_2 (cs33c): same-column pairs left to the
# shared-vertex theorem (scope change after the cs33b smoke, out/cs33b_smoke.out feab303a). V1_3 (cs33d), after
# the cs33c pilot at J = 300 (out/cs33c_pilotA.out 78127b83: FAR balls containing 0, no negatives) and the diagnostic dg2 (d12f5641,
# out/dg2_far_budget.out a94471d4: the error is degree truncation growing with p, amplified by centring; not the a~ remainder):
# (NORM) every propagation step is multiplied by a positive scalar polynomial p(t) ~ 1/mu_0(t) (inf p > 0 certified per interval, C-POS);
# (PAR) odd-mode coefficients of rho-even objects are set to exactly 0; the TM degree K (kernels, modes, family) is an item parameter,
# K in {3, 4}; P-NODE scales every E~_m by (1 + 1e-6). Facts (NORM) and (PAR) are proved below; LEMMA_STRIP_RH_v1_2 will carry them.
# v1_4 (cs33e), after the cs33d pilots at J = 300 (out/cs33d_pilotA_K4.out ecd5d38e: 112 FAR failures, exactly the pairs (mh, p),
# (mh, inf), where the mh lead (c_mh)^2 ~ 2e-6 lies below the mh INF Delta tail 8.75e-6 at depth 6): (DEPTH) the mh objects run to
# p < 9 and the INF mh object starts at p = 9 (PE[mh] = 9; 6 for the other types), so its Delta bound shrinks by about 0.146^3.
# v1_5 (cs33f): the truncation is accounted by the proved bound of LEMMA_STRIP_R9_v1 (TR1-TR7), replacing cs33e's unproved inner-product
# slack (all cs33e certificates superseded, LEDGER_NOTES_pk05 31fd26f3): slack_f per interval from eps_T, eps_e, eps_W, kappa, rho, c
# (TRUNC line, control C-SLACK); Davis-Kahan sines carry sqrt(nu0/nu_a); delta_bounds uses |R' T~| for the remainder and the
# tail norms of R' chi_a, T' chi_a. v1_6 (cs33g): the TRUNC line also prints rho per object type; the insertion factor of every
# horizontal object is max(Rop_e, 1) (R9 v1_1), which cs33f's code already used. v1_7 (cs33h): the vertical enclosure
# num in delta_bounds adds 2^-52 |alpha_e mu_a(0)| |u_a| for the float coefficient fl(alpha_e mu_a(0)) of XC (R9 TR7);
# v1_8 (this file), the review of R10 (f0c81dbc): Z1 the Davis-Kahan gap of R4 (iii) is g - eps_j (sb_spectral); Z3 Rop rounded up
# in delta_bounds; Z4 the gap minimum takes the lower ends (lmin); Z5 the INF error multipliers |J_Y||I_Y| carry (1 + slack_f); Z7
# comments (J >= 0 below; Wc_* unused). No other change.
# COVERAGE TABLE (pairs of distinct edges e, f of the 3 x n strip, J in [20, 300], N = 3, 4):
#  n = 1: a tree (Cov = 0). n = 2: the 3 x 2 grid, a ladder: LAD (RV21_55, RV22_47). n = 3: the 3 x 3 box (done).
#  n >= 4, e and f the two vertical edges of one column: they share the middle vertex; the shared-vertex theorem (the E10 adjacent-pair
#   reduction via Dunlop; the paper's sections 2-3) covers every graph, every coupling J >= 0 and N = 3, 4.
#  n >= 4, every other pair: e precedes f with k >= 0 complete factors T~ between their insertions; NEAR checks (k < K_EX, part B or
#   Bh + Bv) and FAR checks (k >= K_EX, part A) below. In particular the three same-gap horizontal pairs (th_x, mh_x), (th_x, bh_x),
#   (mh_x, bh_x) share no vertex and stay in the verdict: they are the NEAR checks at k = 0 with both objects horizontal (part B or Bh;
#   n = p + q + 2, the two insertions multiply one kernel).
# Math: LEMMA_STRIP_RH_v1_1 (2d0e7bea) R1-R6 and the facts below [S] (R7-R9 notes follow). Core: cs33b_rh_core.py (929ab8a0, unchanged,
# sha-checked), which loads route H's hubcert_v1e (c08d33c1).
# FACTS USED [S] (beyond R1-R6):
#  (L2) For edges e (left) and f (right) with left vectors J_L (plain), I_L (e inserted) and right vectors J_R, I_R at the boundaries next
#   to them and k factors T~ between: Cov(s_e, s_f) Z^2 = <J_L ^ I_L, (Lambda^2 T~)^k (J_R ^ I_R)> (Cauchy-Binet; Z = <J_L, T~^k J_R> > 0).
#   Lambda^2 T~ >= 0 has the eigenvalues nu_a nu_b (a < b), top nu1 nu2; I -> I' = I - alpha J leaves J ^ I unchanged.
#  (OB) Objects: J(p) = T~^p w, w = H^1/2 E~ 1 (free end); I(e,p) = R_e J(p) (horizontal e at junction p+1), T~_X J(p-1) (vertical e at
#   column p+1 >= 2), w_X (vertical at column 1), for p < P_e = PE[e] (9 for mh, 6 otherwise). The right end is the mirror image (the same
#   objects); n = p + k + q + 2.
#  (INF) For p >= P_e: J(p) = c_p (chi1 + J'(p)), |J'(p)| <= eta(P_e) (certified even modes decay like (nu_a/nu1)^p, the rest like
#   (u_+/nu1)^p |w_perp|), so J(p) ^ I'(e,p) = c_p^2 (chi1 ^ y_e + Delta) with |Delta| <= D_e uniform in p >= P_e (y_e: bulk insertion).
#  (NEAR) k < K_EX: exact values from family vectors (meet in the middle) and from the bulk seeds T~^k u1, T~^k y_e (infinity objects).
#  (FAR) k >= K_EX: S(k) = sum_{a<b certified} (nu_a nu_b)^k X_ab Y_ab + E, |E| <= (nu1 u_rem)^k |X^perp||Y^perp|, plus Delta terms
#   <= (nu1 nu2)^k (...). Divided by (nu1 nu2)^k, the absolute-value lower bound increases with k (every ratio < 1), so evaluation up to the
#   first k* where that bound is positive settles every k >= K_EX.
#  (R9) Family vectors carry exact float polynomial coefficients and a 2-norm remainder; an operator step adds its folded TM error and
#   multiplies the old remainder by its norm bound (|T^| = nu1 = |T^_X| bound (S_L X S_L^*), |R_e| <= max |g|).
#  (TR) Truncation (LEMMA_STRIP_R9_v1): spectral data widened by eps_T (Weyl in each reflection sector); Davis-Kahan in the T frame, so
#   the sine of a mode in the T~ frame carries sqrt(nu0/nu_a) (TR4); every inner product gets slack_f |a||b| with
#   slack_f = (eps_*/nu0)(2 p_max c kappa rho + (c kappa rho)^2)(1 + 1e-6), eps_* = max(eps_T, eps_e, eps_W), kappa = |v| sqrt(nu0)/|beta_0|,
#   rho = max over objects of (insertion factor x parent norm)/(lower norm), c = ((nu0+/nu0-)(1 + eps_T/nu0-))^p_max (TR1-TR5).
#  (IP) Coefficient inner products of the family vectors come from one chunked BLAS Gram product M M^T (any summation order):
#   |fl(<x, y>) - <x, y>| <= gam(n + 2) |x|_2 |y|_2 + (n + 2) ETA for n states (Cauchy-Schwarz on sum |x_i y_i|); norms cached per vector.
#  (NORM) Positive scalars do not change any sign. If J_X, I_X are multiplied by c_J(t), c_I(t) > 0 (and the right-hand vectors by positive
#   scalars likewise), each NEAR value S and each Lambda^2 amplitude X_ab = j_a i_b - j_b i_a (so each FAR value f(k)) is multiplied by a
#   positive product (every term has exactly one J- and one I-factor), and the eigenvalue ratios are unchanged. The code multiplies every
#   propagation step (T~, and T~_X for a vertical insertion) by p(t), the degree-K Taylor polynomial of 1/mu_0(t) with exact float
#   coefficients, after certifying inf_{|t|<=h} p > 0 (C-POS). So J(p) = p^p T~^p w; I'(e,p) = (R_e - alpha) J(p) or p (T~_X - alpha T~) J(p-1)
#   (the centring sees one common factor); propagated objects carry one more p; Y_e = p (T~_X - alpha T~) u1 for vertical e (projected).
#   Bounds that use the step norm take sup p: near checks (sup p)^2 nu1 nu2; vertical Delta bounds F_e = sup p * nu1 * |u1|^2.
#  (PAR) The row reflection rho (Psi_{l1 l2 l3} -> Psi_{l3 l2 l1}; LEMMA_STRIP_RH_v1_1 R5 (iv)) permutes the product basis, commutes with
#   T^, with R_mh (g_{l2}) and with p(t), exchanges R_th <-> R_bh and T^_{X1} <-> T^_{X3}, and fixes w = H^1/2 E~ 1 (E~1 (x) E~1 and D are
#   swap-symmetric). Hence J(p), u1 (a mode vector made exactly even by fv_sector), T~ u1 and every mh object (I(mh, p), Y_mh and their
#   propagations) are exactly rho-even. Each certified mode chi_a is a simple eigenvector inside its reflection sector (sector-wise
#   identification, R5 (iv)-(v)), so rho chi_a = +-chi_a with the sign of u_a (exactly +-rho-symmetric; C-PAR checks the node parities to
#   1e-6). For odd chi_a and even v: <chi_a, v> = <rho chi_a, rho v> = -<chi_a, v> = 0. The code uses this exact 0 for the true objects in
#   place of the enclosure <u_a, v>/|u_a| +- sqrt2 s_a |v|.
# READINGS (fixed before any run), per interval [b0 - h, b0 + h], N and part:
#  Part A CERTIFIED iff (a) controls pass: C-CAS (every Casimir block's Davis-Kahan radius <= 1e-9), C-NODE (the float operator at the
#   K + 1 nodes lies in the TM enclosure, excess <= 1e-12 relative), C-PAR (the 8 node-0 eigenvectors have parity +-1 to 1e-6), C-FIN (every
#   bound finite), C-POS (inf p > 0 on the interval, NORM, rigorous enclosure), C-SLACK (the proved truncation slack slack_f of R9 TR5 is
#   finite); (b) on every subball: 8 KW intervals, sector trace bounds (+ eps_T), modes 1..6
#   certified (Davis-Kahan gap > 2 eps_T inside their
#   sector), nu1 nu2 isolated as the top of Lambda^2 (u_rem < nu2); (c) every FAR check (all pairs of objects {(e, p): p < P_e} u {(e, inf)},
#   every k >= K_EX) is positive on every subball. (v1_2: no same-column check; see the coverage table.)
#  Part B CERTIFIED iff (a) and (b) hold and every NEAR check (all pairs of objects, k < K_EX, n >= 4) is positive on every subball.
#   Parts Bh and Bv split part B: Bh takes the pairs with at least one horizontal object, Bv the pairs of two vertical objects; Bh and Bv
#   together certify exactly what B certifies.
#  An interval is CERTIFIED iff part A and part B (or both Bh and Bv) certify it (LEDGER lines tagged by part; the union check uses the
#   intervals tagged A and B, or A, Bh and Bv). FAILED otherwise. CONFLICT if some check value is certified negative (a counterexample
#   candidate; reported first, nothing else done).
#  Job: the first interval of every job runs the plants of its part and C-PROBE (cs30, same L, node 0: lam_s/lam1, s = 2..4, to 1e-8, and
#   c_mh/c_th to 1e-4). VALID iff every plant FIRES and C-PROBE passes. COVERED [a, b] (one part) iff VALID, every ledger interval of the
#   job is CERTIFIED for that part and their union contains [a, b] (exact endpoints, b0hex/hhex, rechecked by an independent union script).
#   VOID otherwise.
# PLANTS (first interval of a job; each must FIRE): every part: P6 (flint zero-centred ball), P-CAS (1% error in one Casimir off-diagonal:
#  radius > 1e-9), P-NODE (every float E~_m x (1 + 1e-6): C-NODE fails), P-TR (mode 2 left out of the trace bound: the identification
#  fails), P-L (eps_T at L/4: the identification fails), P-DELTA (every Delta bound x 1e8: a FAR (A) or NEAR (B) check fails); part A:
#  P-VEC (mode 2 replaced by mode 2 + 0.03 mode 4, residual by linearity: a FAR check fails), P-FAR (the leading amplitudes X_12 of (mh, inf)
#  negated: a FAR check fails); parts B, Bh: P-NEAR (the exact near value of the objects (th, 1), (mh, 1) at k = 0 (n = 4) negated: a NEAR
#  check fails); part Bv: P-NEAR on (tv, 1), (bv, 1).
# Usage: cs33h_1_rh_cert.py <item> <CAP_S> [K]. K = 3 (default) or 4 is the TM degree. Items: smoke (J = 20.2, N = 3, one interval of
#  relative width 1%, parts A and B in one process),
#  pilotA / pilotB / pilotBh / pilotBv (KT-P1: N = 4, one interval containing [300/1.01, 300]), coverP:N:a:b:q for P in A, B, Bh, Bv
#  (consecutive intervals of relative width q from a until b is covered, or the time cap; the next item resumes from the last LEDGER line).
import sys
import time
import math
import hashlib
import resource
import importlib.util
import numpy as np

DIR = '/mnt/g2/release/root/code/pk05/'
CORE, CSHA = DIR + 'cs33b_rh_core.py', '82b7cfdd3d1eaf0a095b46231a0a0e1851ade2b0e3796d04be24ba4642163436'
PROBE, PSHA = DIR + 'cs30_ks1_probe.py', '2dbd9a3e7a2820055450ec90228c93830d3cc390bda03134dc6706914bb5288c'
T0 = time.process_time()
ITEM, CAP_S = sys.argv[1], float(sys.argv[2])
KDEG = int(sys.argv[3]) if len(sys.argv) > 3 else 3
if KDEG not in (3, 4):
    raise SystemExit('K must be 3 or 4')


def _load(path, sha, name):
    with open(path, 'rb') as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != sha:
        print('SHA MISMATCH %s %s' % (path, got), flush=True)
        sys.exit(2)
    spec_ = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)
    return mod


C = _load(CORE, CSHA, 'cs33b_rh_core_mod')
E, MR, TM, arb, U, ETA, up, gam, SQ2, FV = C.E, C.MR, C.TM, C.arb, C.U, C.ETA, C.up, C.gam, C.SQ2, C.FV
dn, amin, amax = C.dn, C.amin, C.amax
NMODE, NCERT, K_S, K_F, P_EX, K_EX, NSUB, K_MAX = 8, 6, KDEG, KDEG, 6, 2, 16, 60
PE = {'th': P_EX, 'mh': P_EX + 3, 'bh': P_EX, 'tv': P_EX, 'bv': P_EX}       # v1_4: mh objects to p < 9, INF mh from p = 9
P_MAX = max(PE.values())
TYPES, HORIZ, VERT = ('th', 'mh', 'bh', 'tv', 'bv'), ('th', 'mh', 'bh'), ('tv', 'bv')
QGATE, NODEGATE = 1e-9, 1e-12


def fv_scale(v, c):
    """multiply by an exact power of two"""
    return FV([x * c for x in v.c], v.rho * c, v.h)


def make_perm(L):
    """compact permutation of the side swap rho: (l1, l3, j) -> (l3, l1, j) (R5 (iv))"""
    n = L + 1
    idx = C.STATE['idx']
    l1, rest = np.divmod(idx, n * n)
    l3, j = np.divmod(rest, n)
    pos = np.full(n ** 3, -1, dtype=np.int64)
    pos[idx] = np.arange(idx.size)
    return pos[(l3 * n + l1) * n + j]


def fv_rho(v):
    return FV([x[PERM[0]] for x in v.c], v.rho, v.h)


def fv_sector(v, sg):
    """(v + sg rho v)/2: the sector part (sg = +1 even, -1 odd)"""
    return C.fv_comb(0.5, v, 0.5 * sg, fv_rho(v))


PERM = [None]


class IPS:
    """inner products <a, b> of named family vectors as (arb polynomial, error); per-subball values with the truncation slack"""

    def __init__(self, fvs, slack):
        self.fvs, self.slack, self.cache, self.vals = fvs, slack, {}, {}

    def poly(self, a, b):
        key = (a, b) if a <= b else (b, a)
        if key not in self.cache:
            P, e = C.fv_inner(self.fvs[key[0]], self.fvs[key[1]])
            e = float(up(e + self.slack * self.fvs[key[0]].norm() * self.fvs[key[1]].norm()))
            self.cache[key] = (P, e)
        return self.cache[key]

    def val(self, a, b, tb, ti):
        key = (a, b, ti) if a <= b else (b, a, ti)
        if key not in self.vals:
            P, e = self.poly(a, b)
            self.vals[key] = E.ev(P, arb(0, e), tb)
        return self.vals[key]

    def norm(self, a):
        return self.fvs[a].norm()


def ival(lo, hi):
    """arb ball containing the exact points lo <= hi"""
    return lo.union(hi)


class GIPS(IPS):
    """IPS whose coefficient inner products come from one chunked Gram product M M^T over the listed names (BLAS, any summation order;
    v1_1), other pairs from per-pair dots: |fl(<x, y>) - <x, y>| <= gam(n + 2) sum |x_i y_i| + (n + 2) ETA <= gam(n + 2) |x|_2 |y|_2
    + (n + 2) ETA (n states; Cauchy-Schwarz). pnorm and norm are cached per name."""

    def __init__(self, fvs, slack, names, chunk=32768):
        IPS.__init__(self, fvs, slack)
        self.pn, self.nm, self.nub = {}, {}, {}
        names = [a for a in dict.fromkeys(names) if a in fvs]
        rows = [(a, d) for a in names for d in range(len(fvs[a].c))]
        self.row = {r: i for i, r in enumerate(rows)}
        n = fvs[names[0]].c[0].size
        G = np.zeros((len(rows), len(rows)))
        M = np.empty((len(rows), chunk))
        for s in range(0, n, chunk):
            w = min(chunk, n - s)
            for i, (a, d) in enumerate(rows):
                M[i, :w] = fvs[a].c[d][s:s + w]
            Mw = M[:, :w]
            G += Mw @ Mw.T
            C.guard('gram')
        self.G, self.nst, self.nfall = G, n, 0
        self.gn = gam(n + 2)
        self.en = float(up((n + 2) * ETA))

    def cnorm(self, a, d):
        """>= |c_d|_2 of the named vector"""
        if (a, d) not in self.nub:
            self.nub[(a, d)] = C.vec_norm_ub(np.abs(self.fvs[a].c[d]))
        return self.nub[(a, d)]

    def pnorm(self, a):
        if a not in self.pn:
            self.pn[a] = self.fvs[a].pnorm()
        return self.pn[a]

    def norm(self, a):
        if a not in self.nm:
            self.nm[a] = float(up(up(self.pnorm(a) + self.fvs[a].rho) * (1.0 + 4 * U)))
        return self.nm[a]

    def poly(self, a, b):
        key = (a, b) if a <= b else (b, a)
        if key not in self.cache:
            v, w = self.fvs[key[0]], self.fvs[key[1]]
            gram = (key[0], 0) in self.row and (key[1], 0) in self.row
            self.nfall += 0 if gram else 1
            P = [arb(0) for _ in range(len(v.c) + len(w.c) - 1)]
            for d in range(len(v.c)):
                for e in range(len(w.c)):
                    g = self.G[self.row[(key[0], d)], self.row[(key[1], e)]] if gram else np.dot(v.c[d], w.c[e])
                    rad = float(up(up(self.gn * self.cnorm(key[0], d) * self.cnorm(key[1], e)) * (1.0 + 4 * self.gn) + self.en))
                    P[d + e] = P[d + e] + arb(float(g)) + arb(0, rad)
            pv, pw = self.pnorm(key[0]), self.pnorm(key[1])
            err = float(up((pv * w.rho + v.rho * pw + v.rho * w.rho) * (1.0 + 8 * U)))
            err = float(up((err + self.slack * self.norm(key[0]) * self.norm(key[1])) * (1.0 + 8 * U)))
            self.cache[key] = (P, err)
        return self.cache[key]


def scal_poly(mud, h):
    """(NORM) exact float coefficients of p(t), the degree-K_F Taylor polynomial at t = 0 of 1/mu_0(t) (mu_0 the fitted top eigenvalue;
    any positive polynomial would do), with sup_{|t|<=h} |p| <= pmax and inf_{|t|<=h} p >= plo (arb, rounded outward)"""
    m = [float(x) for x in mud]
    pc = [1.0 / m[0]]
    for d in range(1, K_F + 1):
        acc = 0.0
        for i in range(1, min(d, len(m) - 1) + 1):
            acc += m[i] * pc[d - i]
        pc.append(-acc / m[0])
    H = arb(h)
    rest = sum((abs(arb(c_)) * H ** d for d, c_ in enumerate(pc) if d > 0), arb(0))
    return pc, E.fup_arb(abs(arb(pc[0])) + rest), E.fdn_arb(arb(pc[0]) - rest)


def fv_pmul(v, pc, pmax, k):
    """(NORM) the family vector p(t) v(t) for the exact float polynomial p (|p| <= pmax on [-h, h]): products with their rounding radii;
    degrees above k and all radii go to the 2-norm remainder, and the old remainder is multiplied by pmax"""
    nd = len(v.c) + len(pc) - 1
    cs, rad, hp = [], 0.0, 1.0
    for d in range(nd):
        acc = None
        for i in range(max(0, d - len(v.c) + 1), min(d, len(pc) - 1) + 1):
            t_ = E.mr_scale(MR(v.c[d - i]), pc[i])
            acc = t_ if acc is None else E.mr_add(acc, t_)
        if d <= k:
            cs.append(acc.m)
            rad = float(up(rad + C.vec_norm_ub(acc.r) * hp))
        else:
            rad = float(up(rad + C.vec_norm_ub(acc.absu()) * hp))
        hp = float(up(hp * v.h))
    return FV(cs, float(up(up(pmax * v.rho) * (1.0 + 2 * U) + rad)), v.h)


MODEPAR = [None]


def rho_even(name):
    """(PAR) the objects that are exactly even under the row reflection rho: J(p), the bulk seeds u1 and T~ u1, and every mh object"""
    return ((name[0] == 'J' and name[1:].isdigit()) or name in ('u1', 'Tu1', 'Y_mh', 'TY_mh') or name.startswith('I_mh_')
            or name.startswith('P_mh_'))


def fv_lower(v):
    """a lower bound of inf_{|t|<=h} |v(t)|_2: |c_0| (rounded down) minus sum_{d>=1} |c_d| h^d and the remainder (rounded up)"""
    n = v.c[0].size
    s0 = float(np.dot(v.c[0], v.c[0]))
    lo0 = float(dn(math.sqrt(max(0.0, float(dn(s0 * (1.0 - 4 * gam(n + 2))))))))
    rest = sum(C.vec_norm_ub(np.abs(x)) * float(up(v.h ** d * (1.0 + 1e-12))) for d, x in enumerate(v.c) if d > 0)
    return float(dn(lo0 - float(up((rest + v.rho) * (1.0 + 1e-12)))))


def tr_slack(N, b0, h, L, SP, SBs, F, A, names, tc):
    """(R9 TR1, TR5) eps_W, kappa, rho, c and the proved inner-product slack slack_f for one interval; inf when a lower bound fails"""
    eT, ee, A3 = tc
    lam = arb(N - 2) / 2
    b0a, bm, bp = arb(b0), arb(b0) - arb(h), arb(b0) + arb(h)
    Amax = arb(A3) ** (arb(1) / 3)
    a0lo = ((-arb(h)).exp() * (b0a / bp) ** lam * bp.bessel_i(lam) / b0a.bessel_i(lam)).lower()
    epsW = max(E.fup_arb(2 * Amax * arb(eT) / a0lo), E.fup_arb((1 + arb(L + 1) / bm) * arb(ee)))
    epss = max(eT, ee, epsW)
    n0lo = min(E.fdn_arb(sb['I'][0][1]) for sb in SBs)
    n0hi = max(E.fup_arb(sb['I'][0][2]) for sb in SBs)
    vnorm = float(np.max(C.tm_bounds(SP['B']['E'][0])[1][0, 0]))
    P, e = C.fv_inner(F['U0'], F['J0'])
    bt = E.ev(P, arb(0, e), arb(0, h))
    s0 = max(E.fup_arb(sb['s'][0]) for sb in SBs)
    b0lo = E.fdn_arb(abs(bt).lower() / arb(F['U0'].norm()) - SQ2 * arb(s0) * arb(F['J0'].norm()))
    if not (b0lo > 0 and n0lo > 0):
        return float('inf'), dict(epsW=epsW, kappa=float('inf'), rho=float('inf'), arg='-', c=float('inf'), rt={})
    kappa = E.fup_arb(arb(vnorm) * arb(n0hi).sqrt() / arb(b0lo))
    pmx = P_MAX + 1
    c = E.fup_arb(((arb(n0hi) / arb(n0lo)) * (1 + arb(eT) / arb(n0lo))) ** pmx)
    # insertion factors (R9 v1_1): max(Rop_e, 1) for every horizontal object (as in cs33f), 1 + |alpha_e| for vertical ones
    f = {e_: (max(float(up(max(A['gmax'][e_] - A['al'][e_], A['al'][e_]))), 1.0) if e_ in HORIZ else float(up(1.0 + abs(A['al'][e_]))))
         for e_ in TYPES}
    rho, arg = 1.0, '-'
    rt = {}                                                                  # v1_6: rho per object type, printed
    for x in dict.fromkeys(names):
        if x not in F:
            continue
        lo = fv_lower(F[x])
        if x[0] == 'U' and x[1:].isdigit():
            a = int(x[1:])
            r = E.fup_arb((arb(n0hi) / arb(min(E.fdn_arb(sb['I'][a][1]) for sb in SBs))).sqrt()) if a < NCERT else 1.0
        else:
            parts = x.split('_')
            if x[0] == 'J' or x in ('u1', 'Tu1'):
                sig = F[x].norm()
            elif parts[0] == 'I':
                sig = f[parts[1]] * F['J%s' % parts[2]].norm()
            elif parts[0] == 'P':
                sig = f[parts[1]] * F['J%d' % (int(parts[2]) + 1)].norm()
            elif parts[0] == 'Y':
                sig = f[parts[1]] * (F['u1'] if parts[1] in HORIZ else F['Tu1']).norm()
            elif parts[0] == 'TY':
                sig = f[parts[1]] * F['Tu1'].norm() * (1.0 if parts[1] in HORIZ else float(up(A['pmax'] * n0hi)))
            else:
                sig = F[x].norm()
            r = float(up(sig / lo)) if lo > 0 else float('inf')
        if x[0] == 'U' and x[1:].isdigit():
            tk = 'U'
        elif x[0] == 'J' or x in ('u1', 'Tu1'):
            tk = 'J' if x[0] == 'J' else 'seed'
        else:
            tk = '_'.join(x.split('_')[:2])
        rt[tk] = max(rt.get(tk, 0.0), r) if r == r else float('inf')
        if not (r < float('inf')):                                        # nan or inf: no finite slack
            r = float('inf')
        if r > rho:
            rho, arg = r, x
    slack = E.fup_arb(arb(epss) / arb(n0lo) * (2 * pmx * arb(c) * arb(kappa) * arb(rho) + (arb(c) * arb(kappa) * arb(rho)) ** 2)
                      * (1 + arb(1e-6)))
    if not (pmx ** 2 * epss / n0lo <= 1e-6):
        slack = float('inf')
    return slack, dict(epsW=epsW, kappa=kappa, rho=rho, arg=arg, c=c, rt=rt)


def spectral(N, b0, h, L, out):
    """Q, inputs, node eigenpairs, 8 mode fits with sector projection u_j = (x_j + sg rho x_j)/2, their TM residuals (KW), C-NODE, and
    the sector traces minus the exact mode polynomials (R5 (iii), (iv))"""
    t1 = time.process_time()
    G, qmax, nb = C.build_Q(N, L)
    out('Q N=%d L=%d: %d blocks, max Davis-Kahan radius %.3e (gate %.0e) (%.1f s)' % (N, L, nb, qmax, QGATE, time.process_time() - t1))
    B = C.build(N, b0, h, L, K_S, out)
    ST = C.states(B, L, h, K_S)
    C.STATE['idx'] = ST['idx']
    PERM[0] = make_perm(L)
    OPS = (G, B['E'], B['ET'], ST['Dh'], L)
    tn, vals, vecs, xs, mus, ops, pars = C.nodes_eig(G, B, ST, L, h, K_S, NMODE, out)
    vec0 = vecs[0]
    del vecs
    trT, trR = C.traces(G, B, ST, L, h, K_S)
    opn = E.fup_arb(E.ev(*E.tm_arb(trT), arb(0, h)))          # |T^| <= tr T^ (T^ >= 0)
    mask, cnode, modes = ST['mask'], -np.inf, []
    for j in range(NMODE):
        sg = 1.0 if pars[j] > 0 else -1.0
        X, TX, r = C.residual(OPS, xs[j], mus[j], h, K_S)
        for i, t in enumerate(tn):
            xt = sum(xs[j][d] * t ** d for d in range(K_S + 1))
            f = C.f_T(ops[i], xt)
            c, rr = C.tm_at(TX, t)
            cnode = max(cnode, float(np.max((np.abs(c - f) - rr) * mask)) / float(np.max(np.abs(f))))
        del TX
        u = fv_sector(FV([C.to_compact(x).copy() for x in xs[j]], 0.0, h), sg)
        P = C.fv_inner(u, u)
        n2 = min(E.fdn_arb(E.ev(P[0], arb(0, P[1]), tb)) for tb in E.subballs(h, NSUB))
        nlo = float(dn(math.sqrt(n2))) if n2 > 0 else 0.0
        mumax = float(up(sum(abs(c_) * h ** d for d, c_ in enumerate(mus[j])) * (1.0 + 1e-12)))
        rb = float(up(C.tm_norm_ub(r, mask) + (opn + mumax) * u.rho * (1.0 + 4 * U)))     # |P_sg r| <= |r|, plus u's rounding
        eps = float(up(rb / nlo * (1.0 + 2 * U))) if nlo > 0 else float('inf')
        modes.append(dict(u=u, sg=sg, par=pars[j], eps=eps, rb=rb, nlo=nlo, mu=[arb(c_) for c_ in mus[j]], mud=mus[j]))
        del X, r
        xs[j] = None
        C.guard('residual')
    del ops
    trs = {}
    for sg in (1.0, -1.0):
        D = E.tm_scale(E.tm_add(trT, trR, sg), 0.5)
        for m in modes:
            if m['sg'] == sg:
                D = E.tm_add(D, TM([MR(np.float64(c_)) for c_ in m['mud']], np.float64(0.0), h, K_S), -1.0)
        trs[sg] = E.tm_arb(D)
    out('SPECTRAL N=%d: eps/mu0 %s; parities %s; C-NODE excess %.2e; |T^| <= %.6e (%.1f s)' % (N, ' '.join(
        '%.1e' % (m['eps'] / m['mud'][0]) for m in modes), ' '.join('%+.9f' % m['par'] for m in modes), cnode, opn,
        time.process_time() - t1))
    return dict(N=N, G=G, qmax=qmax, B=B, ST=ST, tn=tn, vals=vals, vec0=vec0, modes=modes, trs=trs, cnode=cnode, opn=opn,
                L=L, h=h, b0=b0)


def lmin(a, b):
    """v1_8: a safe lower bound of min(a, b) for balls: the smaller of the two lower ends, as an exact ball"""
    la, lb = a.lower(), b.lower()
    return la if la < lb else lb


def sb_spectral(SP, tb, eT, drop=None):
    """one subball: KW intervals (widened by eps_T); per sector a maximal set of pairwise disjoint intervals is subtracted in the trace
    bound tau (an interval overlapping an earlier one may hold the same eigenvalue: not subtracted, never certified); certified modes need a
    positive Davis-Kahan gap inside their sector; sines s_j (KW part plus the T-frame Davis-Kahan part times sqrt(nu0/nu_j), R9 TR4), u_rem;
    drop: a mode left out of the trace bound (plant P-TR)."""
    modes = SP['modes']
    I = []
    for m in modes:
        mu = E.ev(m['mu'], arb(0), tb)
        w = arb(m['eps']) + arb(eT)
        I.append((mu, (mu - w).lower(), (mu + w).upper()))
    disj = lambda a, b: I[a][1] > I[b][2] or I[b][1] > I[a][2]
    ok, why, tau, subt = True, [], {}, set()
    for sg in (1.0, -1.0):
        ids = [j for j, m in enumerate(modes) if m['sg'] == sg]
        for j in ids:
            if j != drop and all(disj(j, i) for i in subt if modes[i]['sg'] == sg):
                subt.add(j)
        t = E.ev(SP['trs'][sg][0], SP['trs'][sg][1], tb).upper()
        for j in ids:
            t = t + (arb(modes[j]['eps']) if j in subt else I[j][0].upper())
        tau[sg] = (t + arb(eT)).upper()
    cert, gam_, s = [], {}, {}
    for j, m in enumerate(modes):
        sg = m['sg']
        g = I[j][0].lower() - tau[sg]
        for i, mi in enumerate(modes):
            if i != j and mi['sg'] == sg:
                if I[j][0].lower() > I[i][2]:
                    d = I[j][0].lower() - I[i][2]
                elif I[i][1] > I[j][0].upper():
                    d = I[i][1] - I[j][0].upper()
                else:
                    d = arb(-1)
                g = lmin(g, d)                                         # v1_8 (Z4): lower ends, never the undecided side
        gD = g - arb(m['eps'])                                   # v1_8 (Z1): R4 (iii)'s gap around the eigenvalue is >= g - eps_j
        if j in subt and gD > 2 * arb(eT):
            cert.append(j)
            gam_[j] = g
            fr = (I[0][2] / I[j][1]).sqrt()                         # v1_5 (R9 TR4): the T-frame Davis-Kahan term carries sqrt(nu0/nu_j)
            s[j] = (arb(m['eps']) / g + fr * (SQ2 * arb(eT) / (gD - arb(eT)) + arb(eT) / (2 * I[j][1]))).upper()
    if not all(j in cert for j in range(NCERT)):
        ok = False
        why.append('certified %s' % cert)
    cert = [j for j in cert if j < NCERT]
    urem = {sg: tau[sg] for sg in (1.0, -1.0)}
    for j, m in enumerate(modes):
        if j not in cert:
            urem[m['sg']] = amax(urem[m['sg']], I[j][2])
    ur = amax(urem[1.0], urem[-1.0])
    top1 = ur
    for j in range(1, NMODE):
        top1 = amax(top1, I[j][2])
    if not (I[0][1] > top1):
        ok = False
        why.append('nu1 not top')
    top2 = ur
    for j in range(2, NMODE):
        top2 = amax(top2, I[j][2])
    if not (I[1][1] > top2) or modes[1]['sg'] < 0:
        ok = False
        why.append('nu2 not isolated')
    return dict(I=I, tau=tau, cert=cert, gam=gam_, s=s, urem=ur, ok=ok, why=why, subt=sorted(subt))


def wvec(colA, colB, G, Dh1, L, h):
    """end vector H^1/2 (A (x) B) 1 in sector 0: hub entries [l1, l3, 0] = colA[l1] colB[l3], then Q^T and D^1/2 (R4 (ii), (OB))"""
    n = L + 1
    A = E.tm_mul(TM([MR(c.m.reshape(n, 1), c.r.reshape(n, 1)) for c in colA.c], colA.R.reshape(n, 1), h, K_F),
                 TM([MR(c.m.reshape(1, n), c.r.reshape(1, n)) for c in colB.c], colB.R.reshape(1, n), h, K_F))
    cm, cr = [], []
    for c in A.c:
        zm, zr = np.zeros((n, n, n)), np.zeros((n, n, n))
        zm[:, :, 0], zr[:, :, 0] = c.m, c.r
        cm.append(zm)
        cr.append(zr)
    R = np.zeros((n, n, n))
    R[:, :, 0] = A.R
    Y = C.tm_blk(G, TM([MR(cm[d], cr[d]) for d in range(K_F + 1)], R, h, K_F), False)
    return C.fv_from_tm(E.tm_mul(Dh1, Y), L)


def col0(A, h):
    return TM([MR(c.m[:, 0].copy(), c.r[:, 0].copy()) for c in A.c], A.R[:, 0].copy(), h, A.k)


def centring(SP, gT):
    """centring constants (any constants are admissible): bulk means of the five insertions from the node-0 top eigenvector (floats)"""
    G, B, ST, L, h = SP['G'], SP['B'], SP['ST'], SP['L'], SP['h']
    n = L + 1
    t0 = SP['tn'][0]
    x1 = SP['vec0'][:, 0].reshape((n, n, n))
    nx = float(np.sum(x1 * x1))
    al = {e: float(np.sum(x1 * x1 * C.poly(gT[e], t0)) / nx) for e in HORIZ}
    l1 = SP['vals'][0][0]
    for e, kind in (('tv', 'X1'), ('bv', 'X3')):
        al[e] = float(np.sum(x1 * C.f_T(C.fop(G, B, ST, L, t0, kind), x1)) / (l1 * nx))
    return al


def family_base(SP, nu1up, out):
    """operators of degree K_F, the end vectors, J(0..P_MAX), centred insertions I'(e, p) for p < PE[e]. (NORM): every propagation step is
    multiplied by the positive scalar polynomial p(t) ~ 1/mu_0(t) (scal_poly; the caller checks inf p > 0)"""
    t1 = time.process_time()
    G, B, ST, L, h = SP['G'], SP['B'], SP['ST'], SP['L'], SP['h']
    tr1 = lambda A: C.tm_trunc(A, K_F)
    E1, ET1, XE1, XET1 = [tr1(A) for A in B['E']], [tr1(A) for A in B['ET']], [tr1(A) for A in B['XE']], [tr1(A) for A in B['XET']]
    Dh1 = tr1(ST['Dh'])
    OP = {'T': (G, E1, ET1, Dh1, L), 'tv': (G, XE1, ET1, Dh1, L), 'bv': (G, E1, XET1, Dh1, L), 'tb': (G, XE1, XET1, Dh1, L)}
    gT = {e: tr1(ST['g'][e]) for e in HORIZ}
    gmax = {e: float(np.max(up(gT[e].absP() + gT[e].R) * ST['mask'])) for e in HORIZ}
    pc, pmax, plo = scal_poly(SP['modes'][0]['mud'], h)
    al = centring(SP, gT)
    cE, cX = col0(E1[0], h), col0(XE1[0], h)
    F = {'J0': wvec(cE, cE, G, Dh1, L, h), 'W_tv': wvec(cX, cE, G, Dh1, L, h), 'W_bv': wvec(cE, cX, G, Dh1, L, h),
         'W_tb': wvec(cX, cX, G, Dh1, L, h)}
    step = lambda key, v: fv_pmul(C.fv_apply(OP[key], v, nu1up, L, K_F), pc, pmax, K_F)
    for p in range(P_MAX):
        F['J%d' % (p + 1)] = step('T', F['J%d' % p])
        C.guard('J')
    for e in TYPES:
        for p in range(PE[e]):
            J = F['J%d' % p]
            if e in HORIZ:
                I = C.fv_diag(gT[e], J, gmax[e], L, K_F)
            else:
                I = F['W_' + e] if p == 0 else step(e, F['J%d' % (p - 1)])
            F['I_%s_%d' % (e, p)] = C.fv_comb(1.0, I, -al[e], J)
        C.guard('I')
    out('FAMILY base: p(t) coefficients %s (sup %.6e, inf >= %.6e), centring %s, |J_p| %s (%.1f s)' % (
        ' '.join('%.6e' % c_ for c_ in pc), pmax, plo, ' '.join('%s %.9f' % (e, al[e]) for e in TYPES),
        ' '.join('%.3e' % F['J%d' % p].norm() for p in range(P_MAX + 1)), time.process_time() - t1))
    return F, dict(OP=OP, gT=gT, gmax=gmax, pc=pc, pmax=pmax, plo=plo, nu1up=nu1up, al=al, step=step)


def family_common(SP, F, A, out):
    """both parts: the modes, the bulk seeds (u1, T~ u1, projected y_e; scaled by p(t) like the family) and the vertical mode products
    XU_e_a = T~_X u_a (unscaled; Delta bounds)"""
    t1 = time.process_time()
    step, gT, gmax, al = A['step'], A['gT'], A['gmax'], A['al']
    L = SP['L']
    for a, m in enumerate(SP['modes']):
        F['U%d' % a] = m['u']
    u1 = C.fv_trunc(SP['modes'][0]['u'], K_F)
    F['u1'] = u1
    F['Tu1'] = step('T', u1)
    for e in TYPES:
        if e in HORIZ:
            y = C.fv_comb(1.0, C.fv_diag(gT[e], u1, gmax[e], L, K_F), -al[e], u1)
        else:
            y = C.fv_comb(1.0, step(e, u1), -al[e], F['Tu1'])
        c = float(np.dot(u1.c[0], y.c[0]) / np.dot(u1.c[0], u1.c[0]))
        F['Y_' + e] = C.fv_comb(1.0, y, -c, u1)
        C.guard('Y')
    for e in VERT:
        for a in range(NCERT):
            F['XU_%s_%d' % (e, a)] = C.fv_apply(A['OP'][e], C.fv_trunc(SP['modes'][a]['u'], K_F), A['nu1up'], L, K_F)
        C.guard('XU')
    out('FAMILY common: %d vectors (%.1f s)' % (len(F), time.process_time() - t1))
    return F


def family_part(SP, F, A, part, out):
    """part B: depth-1 propagation of the centred insertions (P_e_p) and of the bulk seeds (TY_e) for every type (Bh: horizontal types,
    Bv: vertical types); part A needs no further vectors (v1_2: no same-column images)"""
    t1 = time.process_time()
    step = A['step']
    if 'B' in part:
        for e in (HORIZ if part == 'Bh' else (VERT if part == 'Bv' else TYPES)):
            for p in range(PE[e]):
                F['P_%s_%d' % (e, p)] = step('T', F['I_%s_%d' % (e, p)])
            F['TY_' + e] = step('T', F['Y_' + e])
            C.guard('P')
    out('FAMILY part %s: %d vectors, max rho/norm %.2e (%.1f s)' % (part, len(F), max(v.rho / max(v.norm(), 1e-300) for v in F.values()),
        time.process_time() - t1))
    return F


def family_extra(SP, F, A):
    """vectors for the Delta bounds: RU_e_a = (R_e - alpha_e) u_a (horizontal) (the vertical products XU are in family_common),
    and the centred end vectors W'_A for the same-column end column"""
    gT, gmax, al, step = A['gT'], A['gmax'], A['al'], A['step']
    L = SP['L']
    for a in range(NCERT):
        ua = C.fv_trunc(SP['modes'][a]['u'], K_F)
        for e in HORIZ:
            F['RU_%s_%d' % (e, a)] = C.fv_comb(1.0, C.fv_diag(gT[e], ua, gmax[e], L, K_F), -al[e], ua)
    a1, a3 = al['tv'], al['bv']
    # Wc_* below are left over from the earlier same-column scope: computed, never read (not in names, no effect on rho)
    F['Wc_tv'] = C.fv_comb(1.0, F['W_tv'], -a1, F['J0'])
    F['Wc_bv'] = C.fv_comb(1.0, F['W_bv'], -a3, F['J0'])
    t = C.fv_comb(1.0, F['W_tb'], -a1, F['W_bv'])
    t = C.fv_comb(1.0, t, -a3, F['W_tv'])
    F['Wc_tb'] = C.fv_comb(1.0, t, a1 * a3, F['J0'])
    return F


def objects():
    """(e, p, J name, I' name, T~J name, T~I' name); p = None is the infinity object (p >= PE[e])"""
    obs = []
    for e in TYPES:
        for p in range(PE[e]):
            obs.append((e, p, 'J%d' % p, 'I_%s_%d' % (e, p), 'J%d' % (p + 1), 'P_%s_%d' % (e, p)))
        obs.append((e, None, 'u1', 'Y_' + e, 'Tu1', 'TY_' + e))
    return obs


def modecoef(ips, SB, v, tb, ti, ext=None):
    """<chi_a, v> for the certified a: <u_a, v>/|u_a| +- sqrt2 s_a |v|; ext: plant data replacing mode 1 (P-VEC). (PAR): exactly 0 for an
    odd mode a and a rho-even object v (chi_a is rho-odd, v is rho-even)"""
    res = []
    for a in SB['cert']:
        if MODEPAR[0][a] < 0 and rho_even(v):
            res.append(arb(0))
            continue
        if ext is not None and a == 1:
            ip, nu, s = ext(v, tb, ti)
        else:
            ua = 'U%d' % a
            ip, nu, s = ips.val(ua, v, tb, ti), ips.val(ua, ua, tb, ti).sqrt(), SB['s'][a]
        res.append(ip / nu + arb(0, E.fup_arb(SQ2 * s * ips.norm(v))))
    return res


def objdata(ips, SB, ob, tb, ti, ext=None):
    """Lambda^2 data of an object: X_ab = j_a i_b - j_b i_a (certified a < b), |X^perp| <= |J_C||I_perp| + |J_perp||I|, |X| <= |J||I|"""
    e, p, Jn, In = ob[:4]
    j, i = modecoef(ips, SB, Jn, tb, ti, ext), modecoef(ips, SB, In, tb, ti, ext)
    nc = len(j)
    X = {(a, b): j[a] * i[b] - j[b] * i[a] for a in range(nc) for b in range(a + 1, nc)}
    nJ2, nI2 = ips.val(Jn, Jn, tb, ti).upper(), ips.val(In, In, tb, ti).upper()
    jp2 = amax(arb(0), (nJ2 - sum(((x * x).lower() for x in j), arb(0))).upper())
    ip2 = amax(arb(0), (nI2 - sum(((x * x).lower() for x in i), arb(0))).upper())
    perp = (nJ2.sqrt() * ip2.sqrt() + jp2.sqrt() * nI2.sqrt()).upper()
    return dict(X=X, perp=perp, nl=(nJ2 * nI2).sqrt().upper(), j=j, i=i)


def xc_vectors(SP, F, A):
    """XC_e_a = XU_e_a - alpha_e mu_a(0) u_a (truncated) ~ (T~_X - alpha T~) u_a, vertical e, a = 0..NCERT-1 (XU is unscaled)"""
    for e in VERT:
        for a in range(NCERT):
            m = SP['modes'][a]
            F['XC_%s_%d' % (e, a)] = C.fv_comb(1.0, F['XU_%s_%d' % (e, a)], -A['al'][e] * m['mud'][0], C.fv_trunc(m['u'], K_F))
    return F


def delta_bounds(ips, SB, SP, A, tb, ti, scale=1.0):
    """per type e: (F_e, D_e) for the infinity object, uniform in p >= PE[e] (INF): S(Xi_true(e,p), Y) F_e / c_p^2 = S(X_comp, Y) + error,
    |error| <= F_e D_e |(Lambda^2 T~)^k Y|. Also '_eta1' = eta(P_EX) + sqrt2 s1' bounds |chi1 + J'(q) - u1/|u1|| for q >= P_EX.
    scale multiplies every D_e (plant P-DELTA)."""
    I, ur, s, modes = SB['I'], SB['urem'], SB['s'], SP['modes']
    n0lo, n0hi = I[0][1], I[0][2]
    beta = modecoef(ips, SB, 'J0', tb, ti)
    b0 = abs(beta[0]).lower()
    wp = amax(arb(0), (ips.val('J0', 'J0', tb, ti).upper() - sum(((x * x).lower() for x in beta), arb(0))).upper()).sqrt()
    rat = lambda a, pp: ((I[a][2] / n0lo) ** pp).upper()
    tail = lambda pp: ((ur / n0lo) ** pp * wp / b0).upper()
    etaf = lambda pp: (sum((rat(a, pp) * abs(beta[a]).upper() / b0 for a in range(1, NCERT)), arb(0)) + tail(pp)).upper()
    eta = etaf(P_EX)
    nu = [ips.val('U%d' % a, 'U%d' % a, tb, ti).sqrt() for a in range(NCERT)]
    s0p = (s[0] + arb(ips.fvs['u1'].rho) / nu[0].lower()).upper()
    uu = ips.val('u1', 'u1', tb, ti).upper()
    out = {'_eta1': (eta + SQ2 * s0p).upper()}
    for e in TYPES:
        p = PE[e]
        eta_e = etaf(p)
        if e in HORIZ:
            Rop = arb(float(up(max(A['gmax'][e] - A['al'][e], A['al'][e]))))   # v1_8 (Z3): rounded up, as in tr_slack
            ne = [(ips.norm('RU_%s_%d' % (e, a)) / nu[a].lower() + Rop * SQ2 * s[a] + (arb(A['epsW']) / I[a][1]).sqrt()).upper()
                  for a in range(NCERT)]                                  # v1_5 (R9 TR7): + |R' P_tail chi_a|
            RTn = (n0hi * (Rop ** 2 * n0hi + arb(A['epsW']))).sqrt()          # v1_5 (R9 TR7): |R' T~| in place of |R'|
            m = sum((rat(a, p) * abs(beta[a]).upper() / b0 * ne[a] for a in range(1, NCERT)), arb(0)) + RTn / n0lo * tail(p - 1)
            Fe = uu
        else:
            Rop = arb(float(up(1.0 + abs(A['al'][e]))))   # v1_8 (Z3): rounded up
            ne = []
            for a in range(NCERT):
                mm = modes[a]
                dmu = arb(float(up(sum(abs(c_) * SP['h'] ** d for d, c_ in enumerate(mm['mud']) if d > 0) * (1.0 + 1e-12))))
                cxc = arb(abs(A['al'][e] * mm['mud'][0])) * arb(2.0 ** -52) * nu[a].upper()   # v1_7 (rule (b)): float coefficient of XC
                num = (arb(ips.norm('XC_%s_%d' % (e, a))) + arb(abs(A['al'][e])) * (dmu * nu[a].upper() + arb(mm['rb']))
                       + n0hi * Rop * arb(A['trho'][a]) + cxc)
                ne.append(((num / nu[a].lower() + n0hi * Rop * SQ2 * s[a] + Rop * (arb(A['eT']) * I[a][2]).sqrt()) / n0lo).upper())
            m = sum((rat(a, p - 1) * abs(beta[a]).upper() / b0 * ne[a] for a in range(1, NCERT)), arb(0)) + Rop * tail(p - 1)
            Fe = (arb(A['pmax']) * n0hi * uu).upper()
        D = (m + eta_e * ne[0] + eta_e * m + SQ2 * s0p * (ne[0] + Rop)).upper()
        out[e] = (Fe, (D * scale).upper())
    return out


def near_checks(ips, SB, obs, DB, ps, tb, ti, negate=None, sel=None):
    """NEAR: every unordered object pair, k < K_EX (n >= 4): S = <J_X,T^k J_Y><I_X,T^k I_Y> - <J_X,T^k I_Y><I_X,T^k J_Y> (scaled T^ = p T~),
    minus F D (ps^2 nu1 nu2)^k |.| for infinity objects (INF), ps >= sup p. S is symmetric in X, Y (T~ symmetric): sel 'h' takes the pairs with a
    horizontal object, oriented so that the propagated object Y is horizontal; sel 'v' the pairs of two vertical objects; None all pairs.
    Returns (count, min value/|X||Y|, its configuration, failures, negatives)."""
    I = SB['I']
    lam = (arb(ps) ** 2 * I[0][2] * I[1][2]).upper()
    nchk, worst, wcfg, fails, negs = 0, None, None, [], []
    nrm = {ob: (arb(ips.norm(ob[2])) * arb(ips.norm(ob[3])) * (1 + arb(ips.slack))).upper() for ob in obs}   # v1_8 (Z5): true norms (TR3)
    for ix, X0 in enumerate(obs):
        for Y0 in obs[ix:]:
            hx, hy = X0[0] in HORIZ, Y0[0] in HORIZ
            if (sel == 'h' and not (hx or hy)) or (sel == 'v' and (hx or hy)):
                continue
            X, Y = (Y0, X0) if (sel == 'h' and not hy) else (X0, Y0)
            for k in range(K_EX):
                if X[1] is not None and Y[1] is not None and X[1] + Y[1] + k < 2:
                    continue
                jy, iy = (Y[2], Y[3]) if k == 0 else (Y[4], Y[5])
                S = ips.val(X[2], jy, tb, ti) * ips.val(X[3], iy, tb, ti) - ips.val(X[2], iy, tb, ti) * ips.val(X[3], jy, tb, ti)
                if negate is not None and (X[0], X[1], Y[0], Y[1], k) == negate:
                    S = -S
                err = arb(0)
                lk = lam ** k
                if X[1] is None:
                    err = err + arb(DB[X[0]][0]) * DB[X[0]][1] * lk * nrm[Y]
                if Y[1] is None:
                    err = err + arb(DB[Y[0]][0]) * DB[Y[0]][1] * lk * nrm[X]
                if X[1] is None and Y[1] is None:
                    err = err + arb(DB[X[0]][0]) * DB[X[0]][1] * arb(DB[Y[0]][0]) * DB[Y[0]][1] * lk
                err = err.upper()
                lo, hi = (S.lower() - err), (S.upper() + err)
                nchk += 1
                v = E.fdn_arb(lo / (nrm[X] * nrm[Y]))
                if worst is None or v < worst:
                    nn = nrm[X] * nrm[Y]
                    worst, wcfg = v, (X[0], X[1], Y[0], Y[1], k, float(S.mid() / nn), E.fup_arb((hi - lo) / nn))
                if not (lo > 0):
                    fails.append((X[0], X[1], Y[0], Y[1], k))
                    if hi < 0:
                        negs.append((X[0], X[1], Y[0], Y[1], k))
    return nchk, worst, wcfg, fails, negs


def far_checks(SB, OD, obs, DB, nrm, negate=None):
    """FAR: every unordered object pair, all k >= K_EX. f(k) = S(k)/(nu1 nu2)^k = X_01 Y_01 + sum_{ab != 01} r_ab^k X_ab Y_ab
    +- (u_rem/nu2)^k |X^perp||Y^perp| +- Delta, r_ab = nu_a nu_b/(nu1 nu2). f(k) > 0 is checked for K_EX <= k < k*, where k* is the first k
    with the monotone lower bound g(k) (absolute values for ab != 01) > 0. Returns (count, max k*, min f/|X||Y|, failures, negatives)."""
    I, nc = SB['I'], len(SB['cert'])
    nuI = [ival(I[a][1], I[a][2]) for a in range(nc)]
    pairs = [(a, b) for a in range(nc) for b in range(a + 1, nc) if (a, b) != (0, 1)]
    r = {ab: (nuI[ab[1]] / nuI[1]) if ab[0] == 0 else (nuI[ab[0]] * nuI[ab[1]] / (nuI[0] * nuI[1])) for ab in pairs}
    rhi = {ab: r[ab].upper() for ab in pairs}
    q = (SB['urem'] / I[1][1]).upper()
    if not (q < 1 and all(rhi[ab] < 1 for ab in pairs)):
        return 0, None, None, None, [('ratios', None)], []
    nchk, kmax, worst, wcfg, fails, negs = 0, 0, None, None, [], []
    for ix, X in enumerate(obs):
        for Y in obs[ix:]:
            dX, dY = OD[X], OD[Y]
            lead = dX['X'][(0, 1)] * dY['X'][(0, 1)]
            if negate is not None and (X[0], X[1]) == negate:
                lead = -lead
            cst = arb(0)
            if X[1] is None:
                cst = cst + arb(DB[X[0]][0]) * DB[X[0]][1] * nrm[Y]
            if Y[1] is None:
                cst = cst + arb(DB[Y[0]][0]) * DB[Y[0]][1] * nrm[X]
            if X[1] is None and Y[1] is None:
                cst = cst + arb(DB[X[0]][0]) * DB[X[0]][1] * arb(DB[Y[0]][0]) * DB[Y[0]][1]
            cst = cst.upper()
            PP = {ab: dX['X'][ab] * dY['X'][ab] for ab in pairs}
            Pa = {ab: abs(PP[ab]).upper() for ab in pairs}
            pp = (dX['perp'] * dY['perp']).upper()
            rk = {ab: r[ab] ** K_EX for ab in pairs}
            rkh = {ab: rhi[ab] ** K_EX for ab in pairs}
            qk = q ** K_EX
            ok, k = False, K_EX
            while k <= K_MAX:
                f = lead + sum((rk[ab] * PP[ab] for ab in pairs), arb(0))
                lo, hi = f.lower() - qk * pp - cst, f.upper() + qk * pp + cst
                nchk += 1
                v = E.fdn_arb(lo / (nrm[X] * nrm[Y]))
                if worst is None or v < worst:
                    nn = nrm[X] * nrm[Y]
                    worst, wcfg = v, (X[0], X[1], Y[0], Y[1], k, float(lead.mid() / nn), E.fup_arb((qk * pp + cst) / nn))
                if not (lo > 0):
                    if hi < 0:
                        negs.append((X[0], X[1], Y[0], Y[1], k))
                    break
                g = lead.lower() - sum((rkh[ab] * Pa[ab] for ab in pairs), arb(0)) - qk * pp - cst
                if g > 0:
                    ok = True
                    break
                rk = {ab: rk[ab] * r[ab] for ab in pairs}
                rkh = {ab: (rkh[ab] * rhi[ab]).upper() for ab in pairs}
                qk = (qk * q).upper()
                k += 1
            kmax = max(kmax, k)
            if not ok:
                fails.append((X[0], X[1], Y[0], Y[1], k))
    return nchk, kmax, worst, wcfg, fails, negs


def checks_all(ips, SP, A, SBs, obs, NS, h, part, near_neg=None, far_neg=None, dscale=1.0, sub=None):
    """the checks of a part on the subballs (all, or the indices in sub): part A runs FAR, part B runs NEAR (Bh, Bv: its two halves,
    see near_checks); v1_2: no same-column checks (coverage table)"""
    tot = dict(near=[0, None, None], far=[0, 0, None, None], fails=[], negs=[])
    nrm = {ob: (arb(ips.norm(ob[2])) * arb(ips.norm(ob[3])) * (1 + arb(ips.slack))).upper() for ob in obs}   # v1_8 (Z5): true norms (TR3)
    for ti, tb in enumerate(E.subballs(h, NSUB)):
        if sub is not None and ti not in sub:
            continue
        sb = SBs[ti]
        DB = delta_bounds(ips, sb, SP, A, tb, ti, dscale)
        if 'A' in part:
            OD = {ob: objdata(ips, sb, ob, tb, ti, A.get('ext')) for ob in obs}
            n2, k2, w2, c2, f2, g2 = far_checks(sb, OD, obs, DB, nrm, far_neg)
            tot['far'][0] += n2
            tot['far'][1] = max(tot['far'][1], k2 or 0)
            if w2 is not None and (tot['far'][2] is None or w2 < tot['far'][2]):
                tot['far'][2], tot['far'][3] = w2, (ti,) + c2
            tot['fails'] += [('far', ti) + f for f in f2]
            tot['negs'] += [('far', ti) + f for f in g2]
        if 'B' in part:
            sel = 'h' if part == 'Bh' else ('v' if part == 'Bv' else None)
            n1, w1, c1, f1, g1 = near_checks(ips, sb, obs, DB, A['pmax'], tb, ti, near_neg, sel)
            tot['near'][0] += n1
            if w1 is not None and (tot['near'][1] is None or w1 < tot['near'][1]):
                tot['near'][1], tot['near'][2] = w1, (ti,) + c1
            tot['fails'] += [('near', ti) + f for f in f1]
            tot['negs'] += [('near', ti) + f for f in g1]
        C.guard('checks')
    return tot


def vec_plant_ext(ips, SP, SBs, A):
    """P-VEC: mode 1 replaced by u1' = u_1 + 0.03 u_3 (same sector); eps' from stored residual bounds (linearity); returns ext(v, tb, ti)"""
    m1, m3 = SP['modes'][1], SP['modes'][3]
    h = SP['h']
    dmu = float(up(sum(abs(a - b) * h ** d for d, (a, b) in enumerate(zip(m1['mud'], m3['mud']))) * (1.0 + 1e-12)))
    n3 = ips.norm('U3')
    rb = float(up(m1['rb'] + 0.03 * (m3['rb'] + dmu * n3)))
    nlo = float(dn(m1['nlo'] - 0.03 * n3))

    def ext(v, tb, ti):
        g = SBs[ti]['gam'].get(1)
        ip = ips.val('U1', v, tb, ti) + 0.03 * ips.val('U3', v, tb, ti)
        nu = (ips.val('U1', 'U1', tb, ti) + 0.06 * ips.val('U1', 'U3', tb, ti) + 0.0009 * ips.val('U3', 'U3', tb, ti)).sqrt()
        s = (arb(rb) / arb(nlo) / g).upper() if (g is not None and nlo > 0) else arb(10)
        return ip, nu, s
    return ext


def _fe(v):
    return '-' if v is None else '%.3e' % v


def _fc(c):
    return '-' if c is None else '(' + ','.join(('%.3e' % x) if isinstance(x, float) else str(x) for x in c) + ')'


def interval(N, b0, h, part, out):
    """one interval, one part ('A', 'B', 'Bh', 'Bv' or 'AB'): returns (status, info, SP, SBs, pack); status CERTIFIED / FAILED / CONFLICT"""
    t1 = time.process_time()
    L = int(math.ceil(math.sqrt(60.0 * (b0 + h)))) + 8
    tc = C.trunc_consts(N, b0, h, L)
    eT = tc[0]
    SP = spectral(N, b0, h, L, out)
    MODEPAR[0] = [1 if m['par'] > 0 else -1 for m in SP['modes']]
    SBs = [sb_spectral(SP, tb, eT) for tb in E.subballs(h, NSUB)]
    par_ok = all(abs(abs(m['par']) - 1.0) <= 1e-6 for m in SP['modes'])
    ctl = dict(cas=SP['qmax'] <= QGATE, node=SP['cnode'] <= NODEGATE, par=par_ok)
    spec_ok = all(sb['ok'] for sb in SBs)
    gaps = []
    for j in range(NCERT):
        gaps.append('%.3e' % min(E.fdn_arb(sb['gam'][j] / sb['I'][0][2]) for sb in SBs) if all(j in sb['gam'] for sb in SBs) else '-')
    out('SPEC N=%d b0=%r part %s: identification %s%s; eps_T %.3e eps_e %.3e; min gap/nu1 %s; u_rem/nu2 <= %.6f; mode sha8 (diagnostic) %s' % (
        N, b0, part, spec_ok, '' if spec_ok else ' ' + str([sb['why'] for sb in SBs if not sb['ok']][:2]), tc[0], tc[1], ' '.join(gaps),
        max(E.fup_arb(sb['urem'] / sb['I'][1][1]) for sb in SBs),
        ' '.join(hashlib.sha256(b''.join(np.ascontiguousarray(x).tobytes() for x in m['u'].c)).hexdigest()[:8] for m in SP['modes'])))
    res = dict(L=L, ctl=ctl, spec=spec_ok, tc=tc)
    if not spec_ok:
        return ('FAILED', res, SP, SBs, None)
    nu1up = max(E.fup_arb(sb['I'][0][2]) for sb in SBs)
    F, A = family_base(SP, nu1up, out)
    ctl['pos'] = A['plo'] > 0
    F = family_common(SP, F, A, out)
    F = family_part(SP, F, A, part, out)
    F = family_extra(SP, F, A)
    A['trho'] = [C.fv_trunc(SP['modes'][a]['u'], K_F).rho for a in range(NCERT)]
    F = xc_vectors(SP, F, A)
    NS = None
    obs = objects()
    names = ['J0'] + ['U%d' % a for a in range(NCERT)]
    for ob in obs:
        names += [ob[2], ob[3]] + ([ob[4], ob[5]] if 'B' in part else [])
    slack, trd = tr_slack(N, b0, h, L, SP, SBs, F, A, names, tc)               # v1_5: the proved slack (R9 TR5)
    A['epsW'], A['eT'] = trd['epsW'], tc[0]
    ctl['slack'] = slack < float('inf')
    out('TRUNC N=%d b0=%r part %s: eps_T %.3e eps_e %.3e eps_W %.3e kappa %.4g rho %.4g (%s) c %.6g slack_f %.3e | rho by type %s' % (
        N, b0, part, tc[0], tc[1], trd['epsW'], trd['kappa'], trd['rho'], trd['arg'], trd['c'], slack,
        ' '.join('%s %.4g' % kv for kv in sorted(trd['rt'].items()))))
    tg = time.process_time()
    ips = GIPS(F, slack, names)
    tgram = time.process_time() - tg
    tot = checks_all(ips, SP, A, SBs, obs, NS, h, part)
    ctl['fin'] = all(math.isfinite(v.rho) for v in F.values()) and all(math.isfinite(m['eps']) for m in SP['modes'])
    ok = all(ctl.values()) and not tot['fails']
    status = 'CERTIFIED' if ok else ('CONFLICT' if tot['negs'] else 'FAILED')
    out('CHECKS N=%d b0=%r part %s: NEAR %d min %s at %s | FAR %d k* <= %d min %s at %s | fails %d %s | negatives %d %s | slack %.2e | '
        'controls %s | gram rows %d, per-pair %d, inner products %d (gram %.1f s, checks %.1f s)' % (
            N, b0, part, tot['near'][0], _fe(tot['near'][1]), _fc(tot['near'][2]), tot['far'][0], tot['far'][1], _fe(tot['far'][2]),
            _fc(tot['far'][3]), len(tot['fails']), tot['fails'][:3], len(tot['negs']), tot['negs'][:3], slack, ctl, len(ips.row), ips.nfall,
            len(ips.cache), tgram, time.process_time() - tg - tgram))
    res.update(tot=tot, status=status, sec=time.process_time() - t1)
    return (status, res, SP, SBs, (F, A, ips, obs, NS))


def plants(N, b0, h, SP, SBs, pack, part, out):
    """the plants of the first interval of a job for its part (each must FIRE); P-NEAR negates a pair with n = 4 (p + q + k = 2)"""
    F, A, ips, obs, NS = pack
    G, B, ST, L = SP['G'], SP['B'], SP['ST'], SP['L']
    tb0 = E.subballs(h, NSUB)[0]
    tc = C.trunc_consts(N, b0, h, L)
    fired = {'P6': E.plant_P6(out)}
    fired['P-CAS'] = float(np.max(C.cert_block(N, 12, 9, plant=True)[1])) > QGATE
    u0, t0 = SP['modes'][0]['u'], SP['tn'][0]
    TX = C.op_apply((G, B['E'], B['ET'], ST['Dh'], L), C.fv_tm(u0, L, K_S))
    op = C.fop(G, B, ST, L, t0)
    Ef = [x * (1.0 + 1e-6) for x in op[1]]                     # v1_3: every E~_m scaled (fires at every J)
    xt = C.to_dense(sum(c_ * t0 ** d for d, c_ in enumerate(u0.c)), L)
    f = C.f_T((op[0], Ef, op[2], op[3], op[4]), xt)
    c, rr = C.tm_at(TX, t0)
    exc = float(np.max((np.abs(c - f) - rr) * ST['mask'])) / float(np.max(np.abs(f)))
    fired['P-NODE'] = exc > NODEGATE
    del TX
    if 'A' in part:
        A['ext'] = vec_plant_ext(ips, SP, SBs, A)
        fired['P-VEC'] = bool(checks_all(ips, SP, A, SBs, obs, NS, h, 'A', sub=[0])['fails'])
        del A['ext']
        fired['P-FAR'] = bool(checks_all(ips, SP, A, SBs, obs, NS, h, 'A', far_neg=('mh', None), sub=[0])['fails'])
    if 'B' in part:
        bp = part if part in ('Bh', 'Bv') else 'B'
        cfg = ('tv', 1, 'bv', 1, 0) if bp == 'Bv' else ('th', 1, 'mh', 1, 0)
        fired['P-NEAR'] = bool(checks_all(ips, SP, A, SBs, obs, NS, h, bp, near_neg=cfg, sub=[0])['fails'])
    fired['P-TR'] = not sb_spectral(SP, tb0, tc[0], drop=1)['ok']
    fired['P-DELTA'] = bool(checks_all(ips, SP, A, SBs, obs, NS, h, part, dscale=1e8, sub=[0])['fails'])
    fired['P-L'] = not sb_spectral(SP, tb0, C.trunc_consts(N, b0, h, max(4, L // 4))[0])['ok']
    out('PLANTS N=%d b0=%r part %s: %s (P-NODE excess %.2e)' % (N, b0, part, ' '.join('%s:%s' % (k, 'FIRED' if v else 'DID-NOT-FIRE')
        for k, v in fired.items()), exc))
    return fired


def c_probe(N, SP, out):
    """C-PROBE: cs30 (sha-checked) at beta = b0 + t_0, same L: lam_s/lam1 (s = 2..4) to 1e-8 and c_mh/c_th to 1e-4 against node 0 (T~ frame);
    cs30 reads sys.argv[1] as its CAP_S at import, so argv is set for the import only"""
    saved = sys.argv
    sys.argv = [saved[0], repr(CAP_S)]
    try:
        P = C.load(PROBE, PSHA, 'cs30_mod')
    finally:
        sys.argv = saved
    L, t0 = SP['L'], SP['tn'][0]
    r = P.analyze(N, SP['b0'] + t0, L)
    n = L + 1
    x1, x2 = (SP['vec0'][:, j].reshape((n, n, n)) for j in (0, 1))
    rm = float(np.sum(x2 * C.poly(SP['ST']['g']['mh'], t0) * x1)) / float(np.sum(x2 * C.poly(SP['ST']['g']['th'], t0) * x1))
    v0 = SP['vals'][0]
    d1 = max(abs(r['lam'][s] - v0[s] / v0[0]) / (v0[s] / v0[0]) for s in (1, 2, 3))
    d2 = abs(r['rmt'] - rm) / abs(rm)
    ok = d1 <= 1e-8 and d2 <= 1e-4
    out('C-PROBE N=%d beta=%r L=%d: lam_s/lam1 rel %.2e (gate 1e-8); c_mh/c_th cs30 %.10e here %.10e rel %.2e (gate 1e-4): %s' % (
        N, SP['b0'] + t0, L, d1, r['rmt'], rm, d2, 'PASS' if ok else 'FAIL'))
    return ok


def make_iv(ell, q):
    """floats (b0, h): [b0 - h, b0 + h] starts at ell (exactly contained) and has relative width about q"""
    b0 = ell / (1.0 - 0.5 * q)
    h = b0 - ell
    while not (arb(b0) - arb(h) <= arb(ell)):
        h = float(np.nextafter(h, np.inf))
    return b0, h


def top_iv(J, f):
    """floats (b0, h) with [b0 - h, b0 + h] containing [J/f, J] exactly"""
    lo = arb(J) / arb(f)
    b0, h = 0.5 * (J / f + J), 0.5 * (J - J / f)
    while not ((arb(b0) - arb(h) <= lo.lower()) and (arb(b0) + arb(h) >= arb(J))):
        h = float(np.nextafter(h, np.inf))
    return b0, h


def ledger(out, N, b0, h, st, part):
    lo, hi = arb(b0) - arb(h), arb(b0) + arb(h)
    out('IV N=%d part %s K=%d b0=%r h=%r L=%d status %s (%.1f s)' % (N, part, KDEG, b0, h, st['L'], st.get('status', 'FAILED'),
                                                                   st.get('sec', 0.0)))
    if st.get('status') == 'CERTIFIED':
        out('LEDGER %s N=%d lo=%s hi=%s b0hex=%s hhex=%s K=%d' % (part, N, lo.str(25, radius=False), hi.str(25, radius=False), b0.hex(),
                                                                   h.hex(), KDEG))
    return hi


def run_item(item, out):
    if item == 'smoke':
        plan, part = [(3, make_iv(20.2, 0.01))], 'AB'
        N, a, b, q = 3, None, None, None
    elif item in ('pilotA', 'pilotB', 'pilotBh', 'pilotBv'):
        plan, part = [(4, top_iv(300.0, 1.01))], item[5:]
        N, a, b, q = 4, None, None, None
    else:
        kind, Ns, As, Bs, Qs = item.split(':')
        if kind not in ('coverA', 'coverB', 'coverBh', 'coverBv'):
            raise SystemExit('unknown item %s' % item)
        part = kind[5:]
        N, a, b, q = int(Ns), float(As), float(Bs), float(Qs)
        plan = None
    valid, allcert, ell, idx, last, hi, stopped = True, True, a, 0, 0.0, None, False
    while True:
        if plan is not None:
            if idx >= len(plan):
                break
            N, (b0, h) = plan[idx]
        else:
            if hi is not None and not (hi < arb(b)):
                break
            if time.process_time() - T0 + 1.5 * last > 0.9 * CAP_S:
                out('COVER_STOP N=%d part %s next_left=%r (time)' % (N, part, ell))
                stopped = True
                break
            b0, h = make_iv(ell, q)
        t1 = time.process_time()
        status, st, SP, SBs, pack = interval(N, b0, h, part, out)
        if idx == 0:
            if pack is None:
                valid = False
                out('PLANTS not run: the first interval failed before the checks')
            else:
                fired = plants(N, b0, h, SP, SBs, pack, part, out)
                cp = c_probe(N, SP, out)
                valid = valid and all(fired.values()) and cp
        hi = ledger(out, N, b0, h, st, part)
        allcert = allcert and status == 'CERTIFIED'
        if status == 'CONFLICT':
            out('CONFLICT at N=%d b0=%r part %s: report first; stopping' % (N, b0, part))
            break
        del SP, SBs, pack
        last = time.process_time() - t1
        idx += 1
        if plan is None:
            ell = float(np.nextafter(float(hi.lower()), -np.inf))
    return valid, allcert, a, hi, stopped, part


def main():
    C.CAP[0] = CAP_S
    with open(__file__, 'rb') as fh:
        me = hashlib.sha256(fh.read()).hexdigest()

    def out(s):
        print(s, flush=True)
    out('SELF sha256 %s' % me)
    out('cs33h_1_rh_cert core %s engine %s probe %s item %s CAP_S %.0f NMODE %d NCERT %d K_S %d K_F %d PE %s K_EX %d NSUB %d K_MAX %d' % (
        CSHA[:8], C.ESHA[:8], PSHA[:8], ITEM, CAP_S, NMODE, NCERT, K_S, K_F, PE, K_EX, NSUB, K_MAX))
    valid, allcert, a, hi, stopped, part = run_item(ITEM, out)
    if not valid:
        verdict = 'VOID'
    elif not allcert:
        verdict = 'FAILED'
    elif ITEM == 'smoke' or ITEM.startswith('pilot'):
        verdict = 'CERTIFIED part %s' % part
    else:
        verdict = ('PARTIAL %s [%r, %s]' if stopped else 'COVERED %s [%r, %s]') % (part, a, hi.str(25, radius=False) if hi is not None else '-')
    out('VALID %s' % valid)
    out('VERDICT %s' % verdict)
    out('CPU %.1f s maxrss_kb %d' % (time.process_time() - T0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    main()
