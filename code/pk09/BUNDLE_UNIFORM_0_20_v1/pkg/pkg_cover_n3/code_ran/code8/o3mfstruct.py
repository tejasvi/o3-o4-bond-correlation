# Wave 18, N = 3 matrix-free certifier: exact structure of the O(3) three-row column map (the formulas of
# code5/o3struct.py, reviewed in RV21_43) as two sparse factors with SIGNED coefficients, built like mfstruct2.py:
#   A1 (bond rows 2-3, vertical label q, spectator a): state (a, b, c) -> hub (a, b2, c'),
#        coefficient (-1)^{a+c+c'} g(b2,q,b) g(c',q,c) {b2 c' a; c b q} W_q
#   A2 (bond rows 1-2, vertical label p, spectator c'): hub (a, b2, c') -> state (a', b', c'),
#        coefficient (-1)^{a+b'} g(a',p,a) g(b',p,b2) {a' b' c'; b2 a p} W_p
# with g(x,y,z) = sqrt((2x+1)(2y+1)(2z+1)) (x y z; 0 0 0) and W_l = i_l(J).  Cut states: labels <= L, triangle, even sum.
# All four triads of both 6j symbols have even sums (cut state, hub, and the two 3j(000) triads), so the admissible tuples
# are those of mfstruct.sixj_tuples.  vmax = 2L keeps every vertical label of a cut state (q <= c + c' <= 2L,
# p <= a + a' <= 2L): the factors then give P T P exactly (9.25 (T1) for N = 3).
# g and the 6j symbols are exact rationals rounded once (sign sqrt(R), relative error <= 1.5 u each); a coefficient
# (two g, one 6j, two products) has relative error <= 5.5 u, so Factor.coef_ulps = 6.  The signed 6j values are cached
# on disk by canonical base-128 key (float of the exact value only).  T_X inserts on the top bond (p, in A2), T_Y on the
# bottom bond (q, in A1): A1bond = 'Y'.
import os, sys, time, math
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mfstruct, mfstruct2
sys.path.insert(1, '/mnt/g2/release/root/data/e17/unif/scratch/code5')
import o3struct                                   # three0_sq, delta_sq, fact (exact rationals)

BC = 128
CACHE6 = '/mnt/g2/release/root/data/e17/unif/scratch/tmp/sixj_signed_cache_b128.npz'


def sixj_signed(j1, j2, j3, j4, j5, j6):
    """{j1 j2 j3; j4 j5 j6} for integer spins as a float: exact Racah sum, then sign sqrt(R) rounded once"""
    tri = o3struct.tri
    if not (tri(j1, j2, j3) and tri(j1, j5, j6) and tri(j4, j2, j6) and tri(j4, j5, j3)):
        return 0.0
    fact = o3struct.fact
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
    ds = o3struct.delta_sq
    R = ds(j1, j2, j3) * ds(j1, j5, j6) * ds(j4, j2, j6) * ds(j4, j5, j3) * s * s
    return (1.0 if s > 0 else -1.0) * math.sqrt(float(R))


def signed_values_cached(keys, verbose=False):
    """signed 6j floats for sorted unique base-128 canonical keys, through the disk cache"""
    ck = np.zeros(0, dtype=np.int64); cv = np.zeros(0)
    if os.path.exists(CACHE6):
        z = np.load(CACHE6)
        ck, cv = z['k'], z['v']
    miss = np.setdiff1d(keys, ck, assume_unique=True)
    if len(miss):
        BB = BC * BC
        mv = np.empty(len(miss))
        for i, k in enumerate(miss.tolist()):
            c2 = k % BB; k //= BB; c1 = k % BB; c0 = k // BB
            mv[i] = sixj_signed(c0 // BC, c1 // BC, c2 // BC, c0 % BC, c1 % BC, c2 % BC)
        k2 = np.concatenate([ck, miss]); v2 = np.concatenate([cv, mv])
        o = np.argsort(k2, kind='stable'); ck, cv = k2[o], v2[o]
        assert '/data/e17/unif/scratch/tmp/' in CACHE6
        tmpf = CACHE6 + '.part.npz'
        np.savez(tmpf, k=ck, v=cv)
        os.replace(tmpf, CACHE6)
    idx = np.searchsorted(ck, keys)
    assert np.all(ck[idx] == keys)
    if verbose:
        print('   signed 6j cache: %d classes, %d evaluated now, cache size %d' % (len(keys), len(miss), len(ck)), flush=True)
    return cv[idx]


def gtable(m):
    """G[x, y, z] = g(x, y, z) for labels 0..m-1 (symmetric; zero unless triangle and even sum)"""
    G = np.zeros((m, m, m))
    for x in range(m):
        for y in range(x, m):
            for z in range(y, min(x + y, m - 1) + 1):
                if (x + y + z) % 2:
                    continue
                v = o3struct.gval(x, y, z)
                for (p, q, r) in ((x, y, z), (x, z, y), (y, x, z), (y, z, x), (z, x, y), (z, y, x)):
                    G[p, q, r] = v
    return G


def build(L, verbose=True, vmax=None):
    t0 = time.time()
    Lv = L if vmax is None else vmax
    assert max(2 * L, Lv) <= BC - 3
    n = L + 1; ng = 2 * L + 1; nv = Lv + 1; nlab = Lv + 1
    nS = n ** 3; nF = n * ng * n
    G = gtable(max(ng, nv))
    facs = {}; ntup = {}; times = []
    for name, (r123, r456) in (('A1', ((ng, n, n), (n, n, nv))), ('A2', ((n, n, n), (ng, n, nv)))):
        T = mfstruct.sixj_tuples(r123, r456)
        k = mfstruct2.canon_keys_chunked(T)
        uk, inv = np.unique(k, return_inverse=True)
        del k
        six = signed_values_cached(uk, verbose)[inv]
        del uk, inv
        if name == 'A1':                              # T = (b2, c', a, c, b, q)
            b2, c2, a, c, b, q = [T[i].astype(np.int32) for i in range(6)]       # int32 labels (peak memory); indices < 2^31
            del T
            sign = np.where((a + c + c2) % 2 == 0, 1.0, -1.0)
            coef = sign * G[b2, q, b] * G[c2, q, c] * six
            keep = coef != 0
            facs[name] = mfstruct2.Factor(((a * ng + b2) * n + c2)[keep], ((a * n + b) * n + c)[keep], q[keep], coef[keep], nF, nS, nlab, coef_ulps=6)
        else:                                         # T = (a', b', c', b2, a, p)
            a1, b1, c2, b2, a, p = [T[i].astype(np.int32) for i in range(6)]
            del T
            sign = np.where((a + b1) % 2 == 0, 1.0, -1.0)
            coef = sign * G[a1, p, a] * G[b1, p, b2] * six
            keep = coef != 0
            facs[name] = mfstruct2.Factor(((a1 * n + b1) * n + c2)[keep], ((a * ng + b2) * n + c2)[keep], p[keep], coef[keep], nS, nF, nlab, coef_ulps=6)
        ntup[name] = facs[name].ntup
        times.append(time.time() - t0)
    lab = np.arange(n)
    tt = np.repeat(lab, n * n); hh = np.tile(np.repeat(lab, n), n); bbs = np.tile(lab, n * n)
    adm3 = mfstruct._adm(tt, hh, bbs)
    st = dict(L=L, Lv=Lv, n=n, ng=ng, nS=nS, nF=nF, A1=facs['A1'], A2=facs['A2'], adm=adm3, t=tt, h=hh, bb=bbs, model=3, A1bond='Y',
              ntup=(ntup['A1'], ntup['A2']), times=tuple(times), G=G)
    if verbose:
        print('o3mfstruct L=%d Lv=%d: tuples %d + %d, CSR nnz %d + %d (max merged %d, %d); A1 %.1fs, A2 %.1fs'
              % (L, Lv, ntup['A1'], ntup['A2'], facs['A1'].nnz, facs['A2'].nnz, facs['A1'].terms, facs['A2'].terms, times[0], times[1] - times[0]), flush=True)
    return st


if __name__ == '__main__':
    for L in [int(x) for x in sys.argv[1].split(',')]:
        build(L, vmax=2 * L)
