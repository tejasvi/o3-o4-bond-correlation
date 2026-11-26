#!/usr/bin/env python3
# u4falsify_v1.py (pk13, CODEDIR P0, bounded Conjecture U attempt, falsification step; the approval of 2026-11-06).
# Exact test of W10's Conjecture U (e10/g2rep/G2REP_NOTES.md section 6.4) and of its Gegenbauer versions
# U_2 (Malo's theorem) and U_3 (paper realroot, Corollary zstar), in exact rational arithmetic, no CAS.
# A zonal kernel on S^(N-1) is K = sum_c rho_c Pi_c, with Pi_c = d_c C~_c the reproducing kernel of the
# degree-c harmonics: N = 2: Pi_0 = 1, Pi_c = 2 T_c; N = 3: Pi_c = (2c+1) P_c; N = 4: Pi_c = (c+1) U_c.
# Series composition on S^(N-1) multiplies the rho's. KK = nonzero real polynomials with positive leading
# coefficient whose zeros are all real and <= -1. U_N: K1, K2 in KK implies K1 *_N K2 in KK.
# Membership is exact: Q = K / gcd(K, K') is squarefree, and Sturm counts of the distinct real zeros of Q on
# (-inf, +inf) and on (-inf, -1] must both equal deg Q.
# Reading, fixed before any run:
#   VOID if a control fails: detector must-flag / must-pass lists; closed forms from sphere Wick moments;
#   recurrence-route vs moment-route basis changes and round trips; must-pass families (N = 2 and N = 3 on
#   every family that runs them; N = 4 on F2, whose factors lie in W10's proved class D, Lemma L2); the
#   must-fail set (one factor with a zero in (-1, 1)) must flag at least one N = 4 composite.
#   U4-VIOLATION if some N = 4 composite of two KK kernels outside F2 fails; every such pair is printed and
#   re-tested through the moment route.  Otherwise NO-U4-VIOLATION with the exact counts.
# Usage: u4falsify_v1.py A|B|C  (three parts with separate seeds; each stops starting new pairs after
# CPU_STOP seconds of CPU and reports what it ran; the hard CPU limit is set outside by prlimit).
import sys
import time
import random
import hashlib
from fractions import Fraction as Fr
from math import comb

T0 = time.process_time()
CPU_STOP = 50.0
DMAX = 16
SEED = 20261106


class Stop(Exception):
    pass


def guard():
    if time.process_time() - T0 > CPU_STOP:
        raise Stop


def ptrim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def padd(a, b):
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def psub(a, b):
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0) for i in range(n)])


def pscale(a, s):
    return ptrim([x * s for x in a])


def pmul(a, b):
    out = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return ptrim(out)


def pshift(a):
    return [Fr(0)] + list(a)


def pdeg(a):
    a = ptrim(a)
    if len(a) == 1 and a[0] == 0:
        return -1
    return len(a) - 1


def pderiv(a):
    if len(a) == 1:
        return [Fr(0)]
    return ptrim([a[i] * i for i in range(1, len(a))])


def pdivmod(a, b):
    a = [Fr(x) for x in ptrim(a)]
    b = ptrim(b)
    db = pdeg(b)
    if db < 0:
        raise ZeroDivisionError('division by the zero polynomial')
    da = pdeg(a)
    if da < db:
        return [Fr(0)], ptrim(a)
    q = [Fr(0)] * (da - db + 1)
    lb = b[db]
    for k in range(da - db, -1, -1):
        c = a[k + db] / lb
        q[k] = c
        if c:
            for i in range(db + 1):
                a[k + i] -= c * b[i]
    r = ptrim(a[:db]) if db > 0 else [Fr(0)]
    return ptrim(q), r


def pmonic(a):
    a = ptrim(a)
    return [x / a[-1] for x in a]


def pgcd(a, b):
    a, b = ptrim(a), ptrim(b)
    while pdeg(b) >= 0:
        _, r = pdivmod(a, b)
        a, b = b, r
    return pmonic(a)


def peval(p, x):
    s = Fr(0)
    for c in reversed(p):
        s = s * x + c
    return s


def sgn(x):
    return (x > 0) - (x < 0)


def variations(vals):
    s = [sgn(v) for v in vals if v != 0]
    return sum(1 for i in range(1, len(s)) if s[i] != s[i - 1])


def sturm_chain(q):
    chain = [ptrim(q), pderiv(q)]
    while True:
        _, r = pdivmod(chain[-2], chain[-1])
        if pdeg(r) < 0:
            break
        chain.append(pscale(r, Fr(-1) / abs(r[-1])))
    return chain


def in_KK(K):
    K = ptrim(K)
    d = pdeg(K)
    if d < 0:
        return False, 'zero polynomial'
    if K[-1] <= 0:
        return False, 'leading coefficient <= 0'
    if d == 0:
        return True, 'positive constant'
    g = pgcd(K, pderiv(K))
    Q, rem = pdivmod(K, g)
    if pdeg(rem) >= 0:
        raise RuntimeError('gcd quotient not exact')
    q = pdeg(Q)
    ch = sturm_chain(Q)
    vm = variations([c[-1] * (-1) ** pdeg(c) for c in ch])
    vp = variations([c[-1] for c in ch])
    v1 = variations([peval(c, Fr(-1)) for c in ch])
    n_all, n_le = vm - vp, vm - v1
    return (n_all == q and n_le == q), 'deg %d squarefree %d real %d at-most-minus-one %d' % (d, q, n_all, n_le)


def basis(N, D):
    if N == 2:
        T = [[Fr(1)], [Fr(0), Fr(1)]]
        for c in range(2, D + 1):
            T.append(psub(pscale(pshift(T[c - 1]), 2), T[c - 2]))
        return [T[0]] + [pscale(T[c], 2) for c in range(1, D + 1)]
    if N == 3:
        P = [[Fr(1)], [Fr(0), Fr(1)]]
        for n in range(1, D):
            P.append(pscale(psub(pscale(pshift(P[n]), 2 * n + 1), pscale(P[n - 1], n)), Fr(1, n + 1)))
        return [pscale(P[c], 2 * c + 1) for c in range(D + 1)]
    if N == 4:
        U = [[Fr(1)], [Fr(0), Fr(2)]]
        for c in range(2, D + 1):
            U.append(psub(pscale(pshift(U[c - 1]), 2), U[c - 2]))
        return [pscale(U[c], c + 1) for c in range(D + 1)]
    raise ValueError('N must be 2, 3 or 4')


def moments(N, K):
    # moments of t = s.e for s uniform on S^(N-1): arcsine (N = 2), uniform (N = 3), semicircle (N = 4)
    m = []
    for k in range(K + 1):
        if k % 2:
            m.append(Fr(0))
        elif N == 2:
            m.append(Fr(comb(k, k // 2), 2 ** k))
        elif N == 3:
            m.append(Fr(1, k + 1))
        else:
            j = k // 2
            m.append(Fr(comb(2 * j, j), (j + 1) * 4 ** j))
    return m


BASIS = {N: basis(N, DMAX) for N in (2, 3, 4)}
MOM = {N: moments(N, 2 * DMAX) for N in (2, 3, 4)}


def inner(N, f, g):
    m = MOM[N]
    s = Fr(0)
    for i, x in enumerate(f):
        if x:
            for j, y in enumerate(g):
                if y:
                    s += x * y * m[i + j]
    return s


NORM = {N: [inner(N, BASIS[N][c], BASIS[N][c]) for c in range(DMAX + 1)] for N in (2, 3, 4)}


def to_rho_A(N, K):
    B = BASIS[N]
    K = [Fr(x) for x in ptrim(K)]
    d = pdeg(K)
    rho = [Fr(0)] * (d + 1)
    for c in range(d, -1, -1):
        r = K[c] / B[c][c]
        rho[c] = r
        if r:
            for i in range(c + 1):
                K[i] -= r * B[c][i]
    if any(K):
        raise RuntimeError('basis conversion residue')
    return rho


def to_rho_B(N, K):
    return [inner(N, K, BASIS[N][c]) / NORM[N][c] for c in range(pdeg(K) + 1)]


def from_rho(N, rho):
    B = BASIS[N]
    out = [Fr(0)] * len(rho)
    for c, r in enumerate(rho):
        if r:
            for i in range(c + 1):
                out[i] += r * B[c][i]
    return ptrim(out)


def compose(N, K1, K2, route='A'):
    f = to_rho_A if route == 'A' else to_rho_B
    r1, r2 = f(N, K1), f(N, K2)
    n = min(len(r1), len(r2))
    return from_rho(N, [r1[c] * r2[c] for c in range(n)])


def kern(roots):
    K = [Fr(1)]
    for r in roots:
        K = pmul(K, [Fr(r), Fr(1)])
    return K


STATS = {}
VIOL = []
ANOMALY = []
ROUTE_MISMATCH = [0]
MF = [0, 0]


def check_pair(fam, roots1, roots2, Ns=(4,), route_check=False, must_pass=False):
    K1, K2 = kern(roots1), kern(roots2)
    if route_check:
        for K in (K1, K2):
            if not in_KK(K)[0]:
                ANOMALY.append((fam, 0, roots1, roots2, 'input not in KK', None, None, None))
    for N in Ns:
        C = compose(N, K1, K2, 'A')
        ok, info = in_KK(C)
        st = STATS.setdefault((fam, N), [0, 0])
        st[0] += 1
        if route_check and compose(N, K1, K2, 'B') != C:
            ROUTE_MISMATCH[0] += 1
        if not ok:
            st[1] += 1
            CB = compose(N, K1, K2, 'B')
            okB, infoB = in_KK(CB)
            rec = (fam, N, roots1, roots2, info, okB, infoB, CB == C)
            if N == 4 and not must_pass:
                VIOL.append(rec)
            else:
                ANOMALY.append(rec)


def make_rng(part):
    return random.Random(SEED + {'A': 0, 'B': 1, 'C': 2}[part])


def rand_root(rng):
    u = rng.random()
    if u < 0.15:
        return Fr(1)
    if u < 0.30:
        return 1 + Fr(1, rng.choice((10, 100, 1000)))
    return 1 + Fr(rng.randint(0, 600), 100)


def controls_detector():
    must_flag = [kern([Fr(9, 10), Fr(2)]), [Fr(1), Fr(1), Fr(1)], kern([Fr(-2), Fr(3)]),
                 kern([Fr(1), Fr(1), Fr(999, 1000)]), pscale(kern([Fr(2)]), -1), kern([Fr(1, 2)]), [Fr(0)],
                 pmul([Fr(5), Fr(4), Fr(1)], kern([Fr(2)]))]
    must_pass = [kern([Fr(1)] * 5), kern([Fr(1), Fr(1000001, 1000000), Fr(5)]), kern([Fr(2)] * 3 + [Fr(3)]),
                 [Fr(3)], kern([Fr(1), Fr(1)])]
    nf = sum(1 for K in must_flag if not in_KK(K)[0])
    npass = sum(1 for K in must_pass if in_KK(K)[0])
    return nf, len(must_flag), npass, len(must_pass)


def controls_closed():
    ok = tot = 0
    quads = [(Fr(1), Fr(1), Fr(1), Fr(1)), (Fr(2), Fr(7, 3), Fr(1), Fr(5)), (Fr(13, 10), Fr(4), Fr(11, 7), Fr(9))]
    for N in (2, 3, 4):
        for (a, b, c, d) in quads:
            got = compose(N, kern([a, b]), kern([c, d]))
            want = ptrim([a * b * c * d + (a * b + c * d) / N + Fr(1, N * (N + 2)), (a + b) * (c + d) / N,
                          Fr(2, N * (N + 2))])
            tot += 1
            ok += (got == want)
            got1 = compose(N, kern([a]), kern([c]))
            tot += 1
            ok += (got1 == ptrim([a * c, Fr(1, N)]))
    return ok, tot


def controls_route(rng, n):
    bad = 0
    for _ in range(n):
        d = rng.randint(0, DMAX)
        K = [Fr(rng.randint(-20, 20), rng.randint(1, 9)) for _ in range(d + 1)]
        K[-1] = K[-1] or Fr(1)
        K = ptrim(K)
        for N in (2, 3, 4):
            rA, rB = to_rho_A(N, K), to_rho_B(N, K)
            if rA != rB or from_rho(N, rA) != K:
                bad += 1
    return bad


def fam_mustfail(rng, n):
    for _ in range(n):
        guard()
        r1 = [rand_root(rng) for _ in range(rng.randint(3, 7))]
        r2 = [rand_root(rng) for _ in range(rng.randint(2, 6))] + [rng.choice((Fr(0), Fr(1, 2), Fr(-1, 2)))]
        ok, _ = in_KK(compose(4, kern(r1), kern(r2)))
        MF[0] += 1
        MF[1] += (not ok)


def fam_binomial(rng, nmax):
    for n in range(1, nmax + 1):
        for m in range(1, nmax + 1):
            guard()
            check_pair('F2-binomial', [Fr(1)] * n, [Fr(1)] * m, Ns=(4, 3, 2), route_check=((n + m) % 7 == 0),
                       must_pass=True)


def cluster_kernel(rng):
    roots = []
    for _ in range(rng.randint(1, 3)):
        centre = 1 + rng.choice((Fr(0), Fr(1, 10), Fr(1), Fr(2), Fr(5), Fr(rng.randint(0, 400), 100)))
        eps = rng.choice((Fr(1, 10), Fr(1, 100), Fr(1, 1000)))
        roots += [centre + j * eps for j in range(rng.randint(1, 3))]
    return roots[:8]


W10EX = [Fr(1), Fr(3), Fr(31, 10)]


def fam_cluster(rng, n):
    for i in range(n):
        guard()
        r1 = W10EX if i % 6 == 0 else cluster_kernel(rng)
        check_pair('F3-cluster', r1, cluster_kernel(rng), Ns=(4, 3), route_check=(i % 10 == 0))


def fam_random(rng, n):
    for i in range(n):
        guard()
        r1 = [rand_root(rng) for _ in range(rng.randint(1, 9))]
        r2 = [rand_root(rng) for _ in range(rng.randint(1, 9))]
        check_pair('F1-random', r1, r2, Ns=((4, 3, 2) if i % 3 == 0 else (4,)), route_check=(i % 10 == 0))


def fam_boundary(rng, n):
    betas = (Fr(11, 10), Fr(2), Fr(3), Fr(10))
    for i in range(n):
        guard()
        r1 = [Fr(1)] * rng.randint(0, 6) + [rng.choice(betas)] * rng.randint(1, 6)
        r2 = [Fr(1)] * rng.randint(0, 6) + [rng.choice(betas)] * rng.randint(1, 6)
        check_pair('F4-boundary', r1, r2, Ns=(4,), route_check=(i % 10 == 0))


def spread_root(rng):
    return 1 + Fr(10) ** rng.randint(-3, 4)


def fam_spread(rng, n):
    for i in range(n):
        guard()
        if i % 3 == 2:
            M = rng.randint(2, 10)
            s1 = Fr(rng.randint(1, 10 * M), 10)
            M2 = rng.randint(2, 10)
            s2 = Fr(rng.randint(1, 10 * M2), 10)
            r1, r2 = [Fr(M) / s1] * M, [Fr(M2) / s2] * M2
        else:
            da, db = rng.randint(1, 3), rng.randint(7, 12)
            if i % 2:
                da, db = db, da
            r1 = [spread_root(rng) for _ in range(da)]
            r2 = [spread_root(rng) for _ in range(db)]
        check_pair('F5-spread', r1, r2, Ns=(4, 3), route_check=(i % 10 == 0))


def float_score(C):
    import numpy as np
    c = [float(x) for x in reversed(C)]
    if len(c) < 2:
        return -1e9
    return max((z.real + 1.0) + 5.0 * abs(z.imag) for z in np.roots(c))


def fam_search(rng, starts, steps):
    for _ in range(starts):
        guard()
        r1 = [rand_root(rng) for _ in range(rng.randint(3, 8))]
        r2 = [rand_root(rng) for _ in range(rng.randint(3, 8))]
        best = float_score(compose(4, kern(r1), kern(r2)))
        check_pair('F6-search', r1, r2, Ns=(4,))
        for _ in range(steps):
            guard()
            t1, t2 = list(r1), list(r2)
            tgt = t1 if rng.random() < 0.5 else t2
            k = rng.randrange(len(tgt))
            tgt[k] = max(Fr(1), tgt[k] + Fr(rng.randint(-50, 50), rng.choice((10, 100, 1000))))
            sc = float_score(compose(4, kern(t1), kern(t2)))
            if sc > best:
                best, r1, r2 = sc, t1, t2
                check_pair('F6-search', r1, r2, Ns=(4,))


def main():
    part = sys.argv[1] if len(sys.argv) > 1 else ''
    if part not in ('A', 'B', 'C'):
        print('usage: u4falsify_v1.py A|B|C')
        sys.exit(2)
    with open(__file__, 'rb') as fh:
        me = hashlib.sha256(fh.read()).hexdigest()
    print('u4falsify_v1 sha256 %s part %s python %s seed %d cpu_stop %.0f s' % (
        me, part, sys.version.split()[0], SEED, CPU_STOP), flush=True)
    rng = make_rng(part)
    nf, tf, npass, tp = controls_detector()
    print('CONTROL detector: must-flag flagged %d of %d; must-pass passed %d of %d' % (nf, tf, npass, tp), flush=True)
    cf_ok, cf_tot = controls_closed()
    print('CONTROL closed forms from sphere Wick moments (N = 2, 3, 4): %d of %d match' % (cf_ok, cf_tot), flush=True)
    rb = controls_route(rng, 40)
    print('CONTROL basis routes (recurrence vs moments, round trip; N = 2, 3, 4): %d mismatches in 40 random polynomials'
          % rb, flush=True)
    truncated = None
    try:
        fam_mustfail(rng, 100)
        if part == 'A':
            fam_binomial(rng, 14)
            fam_cluster(rng, 450)
        elif part == 'B':
            fam_random(rng, 900)
            fam_boundary(rng, 250)
        else:
            fam_spread(rng, 160)
            fam_search(rng, 30, 25)
    except Stop:
        truncated = 'CPU stop reached at %.1f s; later families or pairs not run' % (time.process_time() - T0)
    print('CONTROL must-fail (N = 4, second factor has a zero in (-1, 1)): flagged %d of %d' % (MF[1], MF[0]))
    for key in sorted(STATS):
        print('FAMILY %s N=%d composites %d not-in-KK %d' % (key[0], key[1], STATS[key][0], STATS[key][1]))
    print('ROUTE-CHECKS on sampled pairs: %d mismatches' % ROUTE_MISMATCH[0])
    for rec in VIOL[:8]:
        print('U4-VIOLATION fam %s roots1 %s roots2 %s | %s | moment route in KK %s (%s) same composite %s' % (
            rec[0], [str(x) for x in rec[2]], [str(x) for x in rec[3]], rec[4], rec[5], rec[6], rec[7]))
    for rec in ANOMALY[:8]:
        print('ANOMALY fam %s N=%d roots1 %s roots2 %s | %s | moment route in KK %s (%s) same composite %s' % (
            rec[0], rec[1], [str(x) for x in rec[2]], [str(x) for x in rec[3]], rec[4], rec[5], rec[6], rec[7]))
    void = []
    if nf != tf or npass != tp:
        void.append('detector controls')
    if cf_ok != cf_tot:
        void.append('closed forms')
    if rb:
        void.append('basis routes')
    if ROUTE_MISMATCH[0]:
        void.append('route checks')
    if MF[0] == 0 or MF[1] == 0:
        void.append('must-fail set flagged nothing')
    if ANOMALY:
        void.append('must-pass anomaly (%d)' % len(ANOMALY))
    n4 = sum(v[0] for k, v in STATS.items() if k[1] == 4 and k[0] != 'F2-binomial')
    print('ELAPSED cpu %.2f s' % (time.process_time() - T0))
    if truncated:
        print('TRUNCATED %s' % truncated)
    if void:
        print('VERDICT VOID (%s)' % '; '.join(void))
    elif VIOL:
        print('VERDICT U4-VIOLATION (%d of %d tested N = 4 composites outside F2 fail)' % (len(VIOL), n4))
    else:
        print('VERDICT NO-U4-VIOLATION in %d exact N = 4 composites outside F2' % n4)


if __name__ == '__main__':
    main()
