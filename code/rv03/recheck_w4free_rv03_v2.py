#!/usr/bin/env python3
"""the review exact re-check for the paper draft w4free.tex (sha256 prefix 53055883).

Stdlib only, exact rational arithmetic. Prints to stdout; writes no files.
CPU is capped inside the script at 170 s (RLIMIT_CPU).

Moment arrays U_G(N) and transfer densities are computed from the latitude formula of
w4free Lemma 2.6 (freeze a vertex o, sum over integer circulations on G-o, integrate the
latitudes by Beta integrals), coded from the statement of that lemma in two ways: U()
enumerates circulations through fundamental cycles, U_dp() eliminates vertices one at a
time with the flow balance kept in the state. U() is validated against methods that do
not use that lemma: the product formula for trees, the Legendre formula of w4free
Remark 4.3 for cycles, and the Gaussian representation
E prod (g_x.g_y)^k = prod k! [J^k] det(I-J)^(-3/2) on K4 and W4. U_dp() is validated
against U().

Parts:
  V  validation of the moment code
  A  w4free Proposition 7.1 (spokes 01,03 of W4)
  B  w4free Remark 7.2 (rim edges 12,41 of W4)
  C  w4free Remark 7.3 (minor of tau_g)
  D  local inequalities of (T3) for U_G on W4-free graphs: K4+K4 glued along an edge
     (edge kept), K4+C4 glued along an edge (edge kept), a chain of three K4
"""
import itertools
import random
import resource
import time
from fractions import Fraction as Fr
from math import comb, factorial

resource.setrlimit(resource.RLIMIT_CPU, (170, 175))
T0 = time.process_time()


def stamp(label):
    print("[cpu %7.2fs] %s" % (time.process_time() - T0, label), flush=True)


def prod_fr(it):
    r = Fr(1)
    for x in it:
        r *= x
    return r


def beta(dv, b):
    return Fr(factorial(dv - b) * factorial(b), factorial(dv + 1))


def degrees(V, E, N, o):
    d = {p: 0 for p in V if p != o}
    for (p, q), n in zip(E, N):
        if p != o:
            d[p] += n
        if q != o:
            d[q] += n
    return d


def circulations(nodes, edges, mult):
    """Integer circulations f on (nodes, edges), edges oriented p->q, |f_e| <= mult[e].
    Each circulation is produced exactly once (coordinates on the non-tree edges)."""
    parent = {v: v for v in nodes}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    tree, nontree = [], []
    for i, (p, q) in enumerate(edges):
        rp, rq = find(p), find(q)
        if rp != rq:
            parent[rp] = rq
            tree.append(i)
        else:
            nontree.append(i)
    adj = {v: [] for v in nodes}
    for i in tree:
        p, q = edges[i]
        adj[p].append((q, i, 1))
        adj[q].append((p, i, -1))

    def tree_path(s, t):
        prev = {s: None}
        stack = [s]
        while stack:
            v = stack.pop()
            for w, i, sg in adj[v]:
                if w not in prev:
                    prev[w] = (v, i, sg)
                    stack.append(w)
        path = []
        v = t
        while v != s:
            u, i, sg = prev[v]
            path.append((i, sg))
            v = u
        return path

    cycles = []
    for i in nontree:
        p, q = edges[i]
        vec = {i: 1}
        for j, sg in tree_path(q, p):
            vec[j] = vec.get(j, 0) + sg
        cycles.append(vec)
    m = len(edges)
    ranges = [range(-mult[i], mult[i] + 1) for i in nontree]
    for coeffs in itertools.product(*ranges):
        f = [0] * m
        for c, vec in zip(coeffs, cycles):
            if c:
                for j, x in vec.items():
                    f[j] += c * x
        if all(abs(f[j]) <= mult[j] for j in range(m)):
            yield f


def latitude(V, E, N, o, keep=()):
    """Latitude formula. Returns (dens, d, kept): dens maps (b_p for p in kept) to the
    weight after integrating the latitudes u_op of all other p != o."""
    others = [p for p in V if p != o]
    pos = {p: i for i, p in enumerate(others)}
    d = degrees(V, E, N, o)
    inner = [i for i, (p, q) in enumerate(E) if p != o and q != o]
    iE = [E[i] for i in inner]
    iN = [N[i] for i in inner]
    kept = [p for p in others if p in keep]
    dens = {}
    zero = tuple([0] * len(others))
    for f in circulations(others, iE, iN):
        poly = {zero: 1}
        for (p, q), n, fe in zip(iE, iN, f):
            terms = {}
            for k in range(n + 1):
                l = k - fe
                if 0 <= l <= n:
                    terms[k + l] = terms.get(k + l, 0) + comb(n, k) * comb(n, l)
            ip, iq = pos[p], pos[q]
            new = {}
            for ex, c in poly.items():
                for mm, t in terms.items():
                    e2 = list(ex)
                    e2[ip] += mm
                    e2[iq] += mm
                    e2 = tuple(e2)
                    new[e2] = new.get(e2, 0) + c * t
            poly = new
        for ex, c in poly.items():
            val = Fr(c)
            key = []
            for p in others:
                twob = ex[pos[p]]
                if twob % 2 or twob > 2 * d[p]:
                    raise AssertionError("exponent parity or range")
                b = twob // 2
                if p in keep:
                    key.append(b)
                else:
                    val *= beta(d[p], b)
            key = tuple(key)
            dens[key] = dens.get(key, 0) + val
    return dens, d, kept


def U(V, E, N, o):
    dens = latitude(V, E, N, o)[0]
    return sum(dens.values(), Fr(0))


def U_dp(V, E, N, o):
    """Same formula, vertex elimination with (flow, 2b) of open vertices in the state.
    Integer weights; the Beta denominators prod (d_p+1)! are divided out at the end."""
    d = degrees(V, E, N, o)
    inner = [(E[i], N[i]) for i in range(len(E)) if o not in E[i]]
    last = {}
    for t, ((p, q), n) in enumerate(inner):
        last[p] = t
        last[q] = t
    num = 1
    den = 1
    for p in d:
        den *= factorial(d[p] + 1)
        if p not in last:
            num *= factorial(d[p])
    fv = []
    states = {(): 1}
    for t, ((p, q), n) in enumerate(inner):
        for v in (p, q):
            if v not in fv:
                fv.append(v)
                states = {st + (0, 0): w for st, w in states.items()}
        ip, iq = 2 * fv.index(p), 2 * fv.index(q)
        cl = [(v, 2 * fv.index(v)) for v in (p, q) if last[v] == t]
        cpos = sorted((j for _, j in cl), reverse=True)
        bet = {v: [factorial(d[v] - b) * factorial(b) for b in range(d[v] + 1)] for v, _ in cl}
        trans = [(k - l, k + l, comb(n, k) * comb(n, l))
                 for k in range(n + 1) for l in range(n + 1)]
        new = {}
        for st, w in states.items():
            for f, mm, c in trans:
                s2 = list(st)
                s2[ip] += f
                s2[ip + 1] += mm
                s2[iq] -= f
                s2[iq + 1] += mm
                wt = w * c
                ok = True
                for v, j in cl:
                    if s2[j] != 0:
                        ok = False
                        break
                    tb = s2[j + 1]
                    if tb % 2:
                        raise AssertionError("parity")
                    wt *= bet[v][tb // 2]
                if not ok:
                    continue
                for j in cpos:
                    del s2[j:j + 2]
                key = tuple(s2)
                new[key] = new.get(key, 0) + wt
        for v, _ in cl:
            fv.remove(v)
        states = new
    if fv or set(states) - {()}:
        raise AssertionError("open frontier")
    return Fr(num * states.get((), 0), den)


def perm_sign(perm):
    s = 1
    seen = [False] * len(perm)
    for i in range(len(perm)):
        if not seen[i]:
            j, length = i, 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                length += 1
            if length % 2 == 0:
                s = -s
    return s


def pmul(a, b, maxdeg):
    out = {}
    for ea, ca in a.items():
        da = sum(ea)
        for eb, cb in b.items():
            if da + sum(eb) > maxdeg:
                continue
            e = tuple(x + y for x, y in zip(ea, eb))
            out[e] = out.get(e, 0) + ca * cb
    return {e: c for e, c in out.items() if c != 0}


def gauss_series(nvert, E, maxdeg):
    """Coefficients of det(I-J)^(-3/2) up to total degree maxdeg in the edge variables."""
    m = len(E)
    unit = tuple([0] * m)
    M = [[{} for _ in range(nvert)] for _ in range(nvert)]
    for x in range(nvert):
        M[x][x] = {unit: Fr(1)}
    for i, (p, q) in enumerate(E):
        k = tuple(1 if j == i else 0 for j in range(m))
        for x, y in ((p, q), (q, p)):
            M[x][y][k] = M[x][y].get(k, 0) - 1
    det = {}
    for perm in itertools.permutations(range(nvert)):
        term = {unit: Fr(perm_sign(perm))}
        for x in range(nvert):
            term = pmul(term, M[x][perm[x]], maxdeg)
            if not term:
                break
        for e, c in term.items():
            det[e] = det.get(e, 0) + c
    if det.get(unit, 0) != 1:
        raise AssertionError("det constant term")
    P = {e: -c for e, c in det.items() if e != unit and c != 0}
    res = {unit: Fr(1)}
    Pn = {unit: Fr(1)}
    cn = Fr(1)
    for n in range(1, maxdeg + 1):
        Pn = pmul(Pn, P, maxdeg)
        cn = cn * (Fr(3, 2) + n - 1) / n
        for e, c in Pn.items():
            res[e] = res.get(e, 0) + cn * c
    return res


def dfact_odd(n):
    r = 1
    while n > 1:
        r *= n
        n -= 2
    return r


def U_gauss(nvert, E, N, series):
    total = Fr(0)
    for k in itertools.product(*[range(n + 1) for n in N]):
        deg = [0] * nvert
        for (p, q), ke in zip(E, k):
            deg[p] += ke
            deg[q] += ke
        if any(x % 2 for x in deg):
            continue
        g = series.get(tuple(k), 0)
        if g == 0:
            continue
        g = g * prod_fr(Fr(factorial(ke)) for ke in k)
        norm = prod_fr(Fr(dfact_odd(x + 1)) for x in deg)
        total += prod_fr(Fr(comb(n, ke)) for n, ke in zip(N, k)) * g / norm
    return total / 2 ** sum(N)


def expand2(dens, d1, d2):
    poly = {}
    for (b1, b2), c in dens.items():
        a1, a2 = d1 - b1, d2 - b2
        for r in range(b1 + 1):
            cr = comb(b1, r) * (-1) ** r
            for s in range(b2 + 1):
                key = (a1 + r, a2 + s)
                poly[key] = poly.get(key, 0) + c * cr * comb(b2, s) * (-1) ** s
    return {k: v for k, v in poly.items() if v != 0}


def ev(poly, x, y):
    x, y = Fr(x), Fr(y)
    return sum((c * x ** i * y ** j for (i, j), c in poly.items()), Fr(0))


def dx(poly):
    return {(i - 1, j): c * i for (i, j), c in poly.items() if i > 0}


def dy(poly):
    return {(i, j - 1): c * j for (i, j), c in poly.items() if j > 0}


def mom(poly, n, k):
    return sum((c * Fr(1, i + n + 1) * Fr(1, j + k + 1) for (i, j), c in poly.items()), Fr(0))


def gam(n, l):
    if l > n:
        return Fr(0)
    return Fr(factorial(n) ** 2, factorial(n - l) * factorial(n + l + 1))


def local_check(V, E, o, bases, pairs):
    cache = {}

    def Uc(Nt):
        if Nt not in cache:
            cache[Nt] = U_dp(V, E, list(Nt), o)
        return cache[Nt]

    cnt = viol = 0
    worst = None
    for Nb in bases:
        b0 = tuple(Nb)
        for i, j in pairs:
            Ni = list(Nb)
            Ni[i] += 1
            Nj = list(Nb)
            Nj[j] += 1
            Nij = list(Ni)
            Nij[j] += 1
            lhs = Uc(tuple(Nij)) * Uc(b0)
            rhs = Uc(tuple(Ni)) * Uc(tuple(Nj))
            cnt += 1
            if lhs < rhs:
                viol += 1
            rel = lhs / rhs - 1
            if worst is None or rel < worst:
                worst = rel
    return cnt, viol, worst


def allpairs(m):
    return [(i, j) for i in range(m) for j in range(i + 1, m)]


K4V = [0, 1, 2, 3]
K4E = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
W4V = [0, 1, 2, 3, 4]
W4E = [(1, 2), (2, 3), (3, 4), (4, 1), (0, 1), (0, 2), (0, 3), (0, 4)]
#      12      23      34      41      01      02      03      04
GKK = (list(range(6)), [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                        (0, 4), (0, 5), (1, 4), (1, 5), (4, 5)])
GKC = (list(range(6)), [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                        (1, 4), (4, 5), (5, 0)])
GCH = (list(range(8)), [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                        (2, 4), (2, 5), (3, 4), (3, 5), (4, 5),
                        (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)])

stamp("start")
rng = random.Random(20261106)

# ---------------- V: validation
cmp_n = mism_n = 0
for _ in range(8):
    Ns = [rng.randint(0, 4) for _ in range(3)]
    for Et in ([(0, 1), (1, 2), (2, 3)], [(0, 1), (0, 2), (0, 3)]):
        expect = prod_fr(Fr(1, n + 1) for n in Ns)
        for o in range(4):
            cmp_n += 1
            mism_n += U(list(range(4)), Et, Ns, o) != expect
print("V1 trees vs product formula: comparisons %d, mismatches %d" % (cmp_n, mism_n))

cmp_n = mism_n = 0
for mc in range(3, 7):
    Vc = list(range(mc))
    Ec = [(i, (i + 1) % mc) for i in range(mc)]
    for _ in range(6):
        Ns = [rng.randint(0, 3) for _ in range(mc)]
        expect = sum(((2 * l + 1) * prod_fr(gam(n, l) for n in Ns)
                      for l in range(min(Ns) + 1)), Fr(0))
        for o in (0, mc // 2):
            cmp_n += 1
            mism_n += U(Vc, Ec, Ns, o) != expect
print("V2 cycles C3..C6 vs Legendre formula (Rem 4.3): comparisons %d, mismatches %d" % (cmp_n, mism_n))
stamp("V2 done")

serK4 = gauss_series(4, K4E, 6)
testN = [list(t) for t in itertools.product((0, 1), repeat=6)]
while len(testN) < 74:
    t = [rng.randint(0, 2) for _ in range(6)]
    if sum(t) <= 6:
        testN.append(t)
cmp_n = mism_n = 0
for Ns in testN:
    ug = U_gauss(4, K4E, Ns, serK4)
    for o in K4V:
        cmp_n += 1
        mism_n += U(K4V, K4E, Ns, o) != ug
print("V3 K4 latitude (each frozen vertex) vs Gaussian method: comparisons %d, mismatches %d" % (cmp_n, mism_n))
stamp("V3 done")

serW4 = gauss_series(5, W4E, 6)
cmp_n = mism_n = 0
reps = 0
while reps < 12:
    t = [rng.randint(0, 2) for _ in range(8)]
    if sum(t) > 6:
        continue
    reps += 1
    ug = U_gauss(5, W4E, t, serW4)
    for o in W4V:
        cmp_n += 1
        mism_n += U(W4V, W4E, t, o) != ug
print("V4 W4 latitude (each frozen vertex) vs Gaussian method: comparisons %d, mismatches %d" % (cmp_n, mism_n))
stamp("V4 done")

cmp_n = mism_n = 0
cases = (("K4", K4V, K4E, 0, (0, 1, 2, 3), 3, 4),
         ("W4", W4V, W4E, 0, (0, 1, 2), 2, 4),
         ("K4+K4", GKK[0], GKK[1], 0, (0, 2, 5), 2, 4),
         ("K4+C4", GKC[0], GKC[1], 0, (0, 2, 4), 2, 4),
         ("chain3K4", GCH[0], GCH[1], 2, (2, 0, 6), 1, 2))
for name, Vg, Eg, oref, olist, top, nrep in cases:
    for _ in range(nrep):
        t = [rng.randint(0, top) for _ in range(len(Eg))]
        ref = U(Vg, Eg, t, oref)
        for o in olist:
            cmp_n += 1
            mism_n += U_dp(Vg, Eg, t, o) != ref
print("V5 U_dp (several frozen vertices) vs U on K4, W4, K4+K4, K4+C4, chain3K4: comparisons %d, mismatches %d"
      % (cmp_n, mism_n))
stamp("V5 done")

# ---------------- A: Proposition 7.1
NA = [2, 3, 2, 3, 0, 0, 0, 1]
dens, d, kept = latitude(W4V, W4E, NA, 0, keep=(1, 3))
assert kept == [1, 3]
rho = expand2(dens, d[1], d[3])
degx = max(i for i, j in rho)
degy = max(j for i, j in rho)
row0 = {j: c for (i, j), c in rho.items() if i == 0}
row1 = {j: c for (i, j), c in rho.items() if i == 1}
exp0 = {0: Fr(1, 252), 1: Fr(-2, 315), 2: Fr(1, 525), 3: Fr(1, 1050), 4: Fr(-1, 2800)}
exp1 = {0: Fr(-1, 420), 1: Fr(29, 525), 2: Fr(-59, 700), 3: Fr(13, 350), 4: Fr(-11, 2800)}
print("A degrees of rho in (x, y): (%d, %d); paper: (5, 4)" % (degx, degy))
print("A rho(0,y) coefficients:", [str(row0.get(j, 0)) for j in range(degy + 1)], "equal to paper:", row0 == exp0)
print("A d_x rho(0,y) coefficients:", [str(row1.get(j, 0)) for j in range(degy + 1)], "equal to paper:", row1 == exp1)
r = ev(rho, 0, 1)
rx = ev(dx(rho), 0, 1)
ry = ev(dy(rho), 0, 1)
rxy = ev(dx(dy(rho)), 0, 1)
print("A rho(0,1) = %s, d_y = %s, d_x = %s, d_xy = %s (paper: 1/8400, -1/900, 1/560, -37/2100)" % (r, ry, rx, rxy))
print("A d_x d_y log rho at (0,1) = %s (paper: -8)" % ((r * rxy - rx * ry) / r ** 2))
h = Fr(1, 100)
mnr = ev(rho, 0, 1 - h) * ev(rho, h, 1) - ev(rho, 0, 1) * ev(rho, h, 1 - h)
print("A displayed minor = %s; equal to paper value: %s"
      % (mnr, mnr == Fr(-10524303486251, 30240000000000000000000000)))
mism = 0
for n in range(6):
    for k in range(6):
        N2 = list(NA)
        N2[4] = n
        N2[6] = k
        mism += mom(rho, n, k) != U(W4V, W4E, N2, 1)
print("A moments of rho vs U_W4 with rim vertex 1 frozen (n,k <= 5): comparisons 36, mismatches %d" % mism)
stamp("A done")

# ---------------- B: Remark 7.2
NB = [0, 1, 4, 0, 4, 4, 0, 2]
dens, d, kept = latitude(W4V, W4E, NB, 1, keep=(2, 4))
assert kept == [2, 4]
rhoB = expand2(dens, d[2], d[4])
for px, py in ((0, 1), (1, 0)):
    r = ev(rhoB, px, py)
    rx = ev(dx(rhoB), px, py)
    ry = ev(dy(rhoB), px, py)
    rxy = ev(dx(dy(rhoB)), px, py)
    L = (r * rxy - rx * ry) / r ** 2 if r != 0 else None
    print("B at (x,y) = (%d,%d), x = u_12, y = u_41: rho' = %s, d_x d_y log rho' = %s" % (px, py, r, L))
print("B paper: rho'(0,1) = 1/69300, d_x d_y log rho'(0,1) = -32/3")
mism = cnt = 0
for n in range(d[2] + 1):
    for k in range(d[4] + 1):
        N2 = list(NB)
        N2[0] = n
        N2[3] = k
        cnt += 1
        mism += mom(rhoB, n, k) != U(W4V, W4E, N2, 0)
print("B moments of rho' vs U_W4 with hub 0 frozen: comparisons %d, mismatches %d" % (cnt, mism))
stamp("B done")

# ---------------- C: Remark 7.3


def tauM(M, v, w):
    return sum((comb(M, k) ** 2 * (v * w) ** (M - k) * ((1 - v) * (1 - w)) ** k
                for k in range(M + 1)), Fr(0))


gM = [Fr(4 ** n, factorial(n)) for n in range(41)]
v1, v2, w1, w2 = Fr(97, 100), Fr(99, 100), Fr(1, 100), Fr(3, 100)
TT = {}
for v in (v1, v2):
    for w in (w1, w2):
        TT[(v, w)] = [tauM(M, v, w) for M in range(41)]
tg = {key: sum((gM[M] * vals[M] for M in range(41)), Fr(0)) for key, vals in TT.items()}
Dm = tg[(v1, w1)] * tg[(v2, w2)] - tg[(v1, w2)] * tg[(v2, w1)]
print("C minor of tau_g at (97/100,99/100)x(1/100,3/100): %s; relative to tau_g(v1,w1)tau_g(v2,w2): %.4e; "
      "relative to tau_g(v1,w2)tau_g(v2,w1): %.4e"
      % ("negative" if Dm < 0 else "nonnegative", float(Dm / (tg[(v1, w1)] * tg[(v2, w2)])),
         float(Dm / (tg[(v1, w2)] * tg[(v2, w1)]))))
negM = [M for M in range(41)
        if TT[(v1, w1)][M] * TT[(v2, w2)][M] - TT[(v1, w2)][M] * TT[(v2, w1)][M] < 0]
print("C tau_M minors negative for M in:", negM, "(paper: none for M <= 40); paper relative size: -2.66e-3")
stamp("C done")

# ---------------- D: local inequalities (T3) on W4-free graphs
m = len(GKK[1])
bases = [[0] * m, [1] * m] + [[rng.randint(0, 2) for _ in range(m)] for _ in range(8)]
cnt, viol, worst = local_check(GKK[0], GKK[1], 0, bases, allpairs(m))
print("D1 K4+K4 (glued edge kept), all 55 pairs, %d base points in {0,1,2}^11 incl. 0 and 1: "
      "inequalities %d, violations %d, min relative margin %.3e" % (len(bases), cnt, viol, float(worst)))
cross = [(i, j) for i in range(1, 6) for j in range(6, 11)]
bases = [[rng.randint(0, 4) for _ in range(m)] for _ in range(6)]
cnt, viol, worst = local_check(GKK[0], GKK[1], 0, bases, cross)
print("D2 K4+K4 cross pairs (25, one edge in each K4, glued edge excluded), %d base points in {0..4}^11: "
      "inequalities %d, violations %d, min relative margin %.3e" % (len(bases), cnt, viol, float(worst)))
stamp("D2 done")
m = len(GKC[1])
bases = [[0] * m, [1] * m] + [[rng.randint(0, 3) for _ in range(m)] for _ in range(8)]
cnt, viol, worst = local_check(GKC[0], GKC[1], 0, bases, allpairs(m))
print("D3 K4+C4 (glued edge kept), all 36 pairs, %d base points in {0..3}^9 incl. 0 and 1: "
      "inequalities %d, violations %d, min relative margin %.3e" % (len(bases), cnt, viol, float(worst)))
stamp("D3 done")
m = len(GCH[1])
cross = [(i, j) for i in range(0, 5) for j in range(11, 16)]
bases = [[0] * m, [1] * m] + [[rng.randint(0, 1) for _ in range(m)] for _ in range(3)]
cnt, viol, worst = local_check(GCH[0], GCH[1], 2, bases, cross)
print("D4 chain of three K4 (glue edges 23 and 45), end-to-end pairs (25), %d base points: "
      "inequalities %d, violations %d, min relative margin %.3e" % (len(bases), cnt, viol, float(worst)))
stamp("D4 done")
print("END")
