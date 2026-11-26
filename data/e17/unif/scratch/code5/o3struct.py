# Exact structure of the O(3) column map for the certified interval scheme (wave 18, N = 3).  See o3sparse.py for the
# formulas.  Cut states (a, b, c): labels <= L, triangle, a + b + c even (the global inversion s -> -s acts on |abc> by
# (-1)^{a+b+c} and commutes with the transfer; the boundary state |000> is even).  Intermediate states (a, b2, c'):
# a, c' <= L, b2 <= 2L (all states reachable with vertical labels <= L), so that M = A2 A1 is the exact compression of the
# vertical-bond operator truncated at labels <= L.  Every factor entry is sign * sqrt(R) with R rational (exact 3j(000)
# and 6j symbols of integer spins); the three factors are converted to float separately (relative error <= 1.5 u each),
# so an entry has relative error <= 6.5 u.  The quadruples (s', s, p, q) carry c = sum over the intermediate b2 of
# A2[s', (a, b2, c'), p] A1[(a, b2, c'), s, q] (signed, float) and cabs = sum of |terms|; the float error of c is
# <= (cnt + 16) u cabs.  Output dict as certlib3.quad_struct plus 'cabs', cached to an .npz file if given.
import os, math
from fractions import Fraction as Fr
from functools import lru_cache
import numpy as np


def tri(a, b, c):
    return abs(a - b) <= c <= a + b


@lru_cache(maxsize=None)
def fact(n):
    return math.factorial(n)


@lru_cache(maxsize=None)
def three0_sq(a, b, c):
    """(sign, R) with (a b c; 0 0 0) = sign sqrt(R), integer spins"""
    if (a + b + c) % 2 or not tri(a, b, c):
        return 0, Fr(0)
    L = a + b + c; g = L // 2
    R = Fr(fact(L - 2 * a) * fact(L - 2 * b) * fact(L - 2 * c), fact(L + 1)) * Fr(fact(g), fact(g - a) * fact(g - b) * fact(g - c)) ** 2
    return (-1) ** g, R


@lru_cache(maxsize=None)
def gval(a, b, c):
    """g(a,b,c) = sqrt((2a+1)(2b+1)(2c+1)) (a b c; 000) as a float (relative error <= 1.5 u)"""
    s, R = three0_sq(a, b, c)
    return s * math.sqrt(float(R * (2 * a + 1) * (2 * b + 1) * (2 * c + 1))) if s else 0.0


@lru_cache(maxsize=None)
def delta_sq(a, b, c):
    return Fr(fact(a + b - c) * fact(a - b + c) * fact(-a + b + c), fact(a + b + c + 1))


def sixj_key(j1, j2, j3, j4, j5, j6):
    """canonical representative under the 24 tetrahedral symmetries (column permutations, upper/lower swaps in two
    columns): for each of the 4 swap patterns sort the columns, then take the smallest key (constant on orbits, since a
    swap pattern permutes the 4 patterns and a column permutation does not change the sorted columns)"""
    c = ((j1, j4), (j2, j5), (j3, j6))
    best = None
    for f in ((0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)):
        cols = sorted(c[i] if f[i] == 0 else (c[i][1], c[i][0]) for i in range(3))
        k = (cols[0][0], cols[1][0], cols[2][0], cols[0][1], cols[1][1], cols[2][1])
        if best is None or k < best:
            best = k
    return best


@lru_cache(maxsize=None)
def sixj_c(j1, j2, j3, j4, j5, j6):
    """{j1 j2 j3; j4 j5 j6} as a float (exact Racah sum, then sign sqrt(R) correctly rounded: relative error <= 1.5 u)"""
    if not (tri(j1, j2, j3) and tri(j1, j5, j6) and tri(j4, j2, j6) and tri(j4, j5, j3)):
        return 0.0
    al = [j1 + j2 + j3, j1 + j5 + j6, j4 + j2 + j6, j4 + j5 + j3]
    be = [j1 + j2 + j4 + j5, j2 + j3 + j5 + j6, j3 + j1 + j6 + j4]
    s = 0
    for z in range(max(al), min(be) + 1):
        den = 1
        for x in al:
            den *= fact(z - x)
        for y in be:
            den *= fact(y - z)
        s += (-1) ** z * Fr(fact(z + 1), den)
    if s == 0:
        return 0.0
    R = delta_sq(j1, j2, j3) * delta_sq(j1, j5, j6) * delta_sq(j4, j2, j6) * delta_sq(j4, j5, j3) * s * s
    return (1.0 if s > 0 else -1.0) * math.sqrt(float(R))


def sixj(j1, j2, j3, j4, j5, j6):
    return sixj_c(*sixj_key(j1, j2, j3, j4, j5, j6))


def build(L):
    n = L + 1
    st = [(a, b, c) for a in range(n) for b in range(n) for c in range(n) if tri(a, b, c) and (a + b + c) % 2 == 0]
    idx = {s: i for i, s in enumerate(st)}
    # A1 (bond rows 2-3, spectator a): (a, b, c) -> (a, b2, c') via q,
    #   A1 = W_q (-1)^{a+c+c'} g(b2,q,b) g(c',q,c) {b2 c' a; c b q}
    A1 = {}      # (a, b2, c') -> list of (s index, q, value)
    for (a, b, c) in st:
        for q in range(n):
            for c2 in range(abs(c - q), min(c + q, L) + 1, 2):
                for b2 in range(abs(b - q), b + q + 1, 2):
                    if not tri(a, b2, c2):
                        continue
                    x = (-1) ** (a + c + c2) * gval(b2, q, b) * gval(c2, q, c) * sixj(b2, c2, a, c, b, q)
                    if x != 0.0:
                        A1.setdefault((a, b2, c2), []).append((idx[(a, b, c)], q, x))
    # A2 (bond rows 1-2, spectator c'): (a, b2, c') -> (a', b', c') via p,
    #   A2 = W_p (-1)^{a+b'} g(a',p,a) g(b',p,b2) {a' b' c'; b2 a p}
    A2 = {}      # (a, b2, c') -> list of (s' index, p, value)
    for (a, b2, c2) in A1:
        for p in range(n):
            for a1 in range(abs(a - p), min(a + p, L) + 1, 2):
                for b1 in range(abs(b2 - p), min(b2 + p, L) + 1, 2):
                    if not tri(a1, b1, c2):
                        continue
                    x = (-1) ** (a + b1) * gval(a1, p, a) * gval(b1, p, b2) * sixj(a1, b1, c2, b2, a, p)
                    if x != 0.0:
                        A2.setdefault((a, b2, c2), []).append((idx[(a1, b1, c2)], p, x))
    return st, idx, A1, A2


def quad_struct(L, cache=None):
    if cache and os.path.exists(cache):
        z = np.load(cache)
        out = dict(sp=z['sp'], s=z['s'], a=z['a'], b=z['b'], c=z['c'], cabs=z['cabs'], cnt=z['cnt'], nS=int(z['nS']), L=int(z['L']))
        out['states'] = [tuple(x) for x in z['states']]
        return out
    st, idx, A1, A2 = build(L)
    nS = len(st); n_ = L + 1
    SP, S_, P_, Q_, C_, CA, CN = [], [], [], [], [], [], []
    # per intermediate, merged per block of the source label a (conserved by A1) to keep the peak memory small
    keys_by_a = {}
    for key in A1:
        keys_by_a.setdefault(key[0], []).append(key)
    for a0 in sorted(keys_by_a):
        parts = []
        for key in keys_by_a[a0]:
            l1 = A1[key]; l2 = A2.get(key)
            if not l2:
                continue
            s_i = np.array([x[0] for x in l1], dtype=np.int64); q_i = np.array([x[1] for x in l1], dtype=np.int64); v1 = np.array([x[2] for x in l1])
            sp_i = np.array([x[0] for x in l2], dtype=np.int64); p_i = np.array([x[1] for x in l2], dtype=np.int64); v2 = np.array([x[2] for x in l2])
            parts.append((np.repeat(sp_i, len(s_i)), np.tile(s_i, len(sp_i)), np.repeat(p_i, len(s_i)), np.tile(q_i, len(sp_i)), np.outer(v2, v1).ravel()))
        if not parts:
            continue
        sp = np.concatenate([x[0] for x in parts]); s = np.concatenate([x[1] for x in parts]); p = np.concatenate([x[2] for x in parts])
        q = np.concatenate([x[3] for x in parts]); t = np.concatenate([x[4] for x in parts])
        key = ((sp * nS + s) * n_ + p) * n_ + q
        uk, inv = np.unique(key, return_inverse=True)
        C_.append(np.bincount(inv, weights=t)); CA.append(np.bincount(inv, weights=np.abs(t))); CN.append(np.bincount(inv).astype(np.int32))
        Q_.append((uk % n_).astype(np.int16)); r_ = uk // n_; P_.append((r_ % n_).astype(np.int16)); r_ = r_ // n_
        S_.append((r_ % nS).astype(np.int32)); SP.append((r_ // nS).astype(np.int32))
        del parts, sp, s, p, q, t, key, uk, inv, r_
    del A1, A2, keys_by_a
    # the source label a is conserved by A1, so blocks with different a0 never share a key (no merging across blocks);
    # every merged term is nonzero, so cabs > 0 for every quadruple.  Fields are concatenated one at a time (peak memory).
    out = dict(nS=nS, L=L, states=st)
    for nm, lst in (('sp', SP), ('s', S_), ('a', P_), ('b', Q_), ('c', C_), ('cabs', CA), ('cnt', CN)):
        out[nm] = np.concatenate(lst)
        lst.clear()
    if cache:
        np.savez(cache, states=np.array(st, dtype=np.int16), **{k: v for k, v in out.items() if k != 'states'})
    return out
