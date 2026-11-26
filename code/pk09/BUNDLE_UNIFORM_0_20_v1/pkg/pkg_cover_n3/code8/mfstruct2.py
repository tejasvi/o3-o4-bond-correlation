# Wave 18, checkpoint 2: blocked, memory-lean build of the N = 4 three-row column factors (same factors as mfstruct.py):
#   A1: state (t, h, bb) -> hub (bb, g, tp), coefficient {bb g tp; a t h}^2 (g + 1) W_a     (vertical label a: rows 1-2)
#   A2: hub (bb, g, tp) -> state (tp, hp, bbp), coefficient {tp hp bbp; b bb g}^2 W_b       (vertical label b: rows 2-3)
# Changes from mfstruct.py (results identical):
#  - canonical 6j keys computed in chunks (the full-array int64 copies made the build peak at 6.7 GB at L = 29);
#  - classes made unique per factor, then united; exact squared 6j values (su2lib.sixj_sq, rationals -> float) are
#    taken from a disk cache keyed by an L-independent code (base 128, labels <= 125) and only missing classes are
#    evaluated (the cache stores the float of the exact value, so it changes no number);
#  - each factor keeps its merged CSR pattern plus the weight map C (one row per CSR entry, one column per vertical
#    label, the exact-rounded coefficients), so A(w) has CSR data C @ w: 12 bytes per tuple, no temporaries.
import os, sys, time
import numpy as np
import scipy.sparse as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_dep = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'code_dep')     # package copy of su2lib, else the part source
sys.path.insert(0, _dep if os.path.isfile(os.path.join(_dep, 'su2lib.py')) else '/mnt/g2/release/root/data/e15/dy4/scratch/code')
from su2lib import sixj_sq
import mfstruct                                   # sixj_tuples, _adm (unchanged)

BC = 128                                          # cache key base (labels <= 125)
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tmp', 'sixj_sq_cache_b128.npz')     # ../tmp (N = 4 squared 6j cache)
CHUNK = 1 << 21


def canon_keys_chunked(T, B=BC):
    """canonical int64 key per 6j tuple (min over the 4 swap patterns of the sorted column codes), in chunks"""
    n = T.shape[1]
    out = np.empty(n, dtype=np.int64)
    for c0 in range(0, n, CHUNK):
        out[c0:c0 + CHUNK] = mfstruct.canon_keys(T[:, c0:c0 + CHUNK], B)
    return out


def exact_values_cached(keys, verbose=False):
    """float(exact {6j}^2) for sorted unique base-128 keys, through the disk cache"""
    ck = np.zeros(0, dtype=np.int64); cv = np.zeros(0)
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        ck, cv = z['k'], z['v']
    miss = np.setdiff1d(keys, ck, assume_unique=True)
    if len(miss):
        mv = mfstruct.exact_values(miss, BC)
        k2 = np.concatenate([ck, miss]); v2 = np.concatenate([cv, mv])
        o = np.argsort(k2, kind='stable'); ck, cv = k2[o], v2[o]
        assert os.path.isdir(os.path.dirname(CACHE))
        tmpf = CACHE + '.part.npz'
        np.savez(tmpf, k=ck, v=cv)
        os.replace(tmpf, CACHE)
    idx = np.searchsorted(ck, keys)
    assert np.all(ck[idx] == keys)
    if verbose:
        print('   6j cache: %d classes, %d evaluated now, cache size %d' % (len(keys), len(miss), len(ck)), flush=True)
    return cv[idx]


class Factor:
    """merged CSR pattern (nr x nc) and the weight map C (nnz x nlab): CSR data for weights w is C @ w"""
    def __init__(self, rows, cols, vlab, coef, nr, nc, nlab, coef_ulps=0):
        key = rows.astype(np.int64) * nc + cols.astype(np.int64)
        uk, pos = np.unique(key, return_inverse=True)
        del key
        r = (uk // nc).astype(np.int64); c = (uk % nc).astype(np.int32)
        self.indptr = np.searchsorted(r, np.arange(nr + 1)).astype(np.int64)
        self.indices = c
        self.nr, self.nc, self.nnz = nr, nc, len(uk)
        del uk, r
        self.rowcount = int(np.max(np.diff(self.indptr))) if nr > 0 else 0
        cnt = np.bincount(pos, minlength=self.nnz)
        self.terms = int(cnt.max()) if len(cnt) else 0                 # max tuples merged into one entry
        o = np.argsort(pos, kind='stable')
        cptr = np.zeros(self.nnz + 1, dtype=np.int64); np.cumsum(cnt, out=cptr[1:])
        self.C = sp.csr_matrix((coef[o], vlab[o].astype(np.int32), cptr), shape=(self.nnz, nlab))
        # signed coefficients (N = 3): the radius terms need sum |coef| |w|; nonnegative ones (N = 4) reuse C
        self.Cabs = None if bool(np.all(coef >= 0)) else sp.csr_matrix((np.abs(coef[o]), self.C.indices, cptr), shape=(self.nnz, nlab))
        self.coef_ulps = coef_ulps                                     # relative error of a coefficient beyond 1 u, in u
        self.ntup = len(pos)

    def data(self, w):
        """CSR data for the vertical weight vector w (float array over labels)"""
        return self.C @ np.asarray(w, dtype=float)

    def data_abs(self, w):
        """CSR data of the absolute coefficients for the nonnegative weights w"""
        return (self.C if self.Cabs is None else self.Cabs) @ np.asarray(w, dtype=float)

    def matrix(self, data):
        return sp.csr_matrix((data, self.indices, self.indptr), shape=(self.nr, self.nc))


def build(L, verbose=True, vmax=None):
    """vmax: largest vertical label (default L); vmax = 2L keeps every vertical label of a cut state"""
    t0 = time.time()
    Lv = L if vmax is None else vmax
    assert max(2 * L, Lv) <= BC - 3
    n = L + 1; ng = 2 * L + 1; nv = Lv + 1; nlab = Lv + 1
    nS = n ** 3; nF = n * ng * n
    facs = {}; ntup = {}; times = []
    for name, (r123, r456) in (('A1', ((n, ng, n), (nv, n, n))), ('A2', ((n, n, n), (nv, n, ng)))):
        T = mfstruct.sixj_tuples(r123, r456)
        k = canon_keys_chunked(T)
        uk, inv = np.unique(k, return_inverse=True)
        del k
        vals = exact_values_cached(uk, verbose)[inv]
        del uk, inv
        keep = vals != 0
        if name == 'A1':                              # T = (bb, g, tp, a, t, h)
            bb, g, tp, a, t, h = [T[i][keep].astype(np.int32) for i in range(6)]
            del T
            facs[name] = Factor((bb * ng + g) * n + tp, (t * n + h) * n + bb, a, vals[keep] * (g + 1.0), nF, nS, nlab)
        else:                                         # T = (tp, hp, bbp, b, bb, g)
            tp, hp, bbp, b, bb, g = [T[i][keep].astype(np.int32) for i in range(6)]
            del T
            facs[name] = Factor((tp * n + hp) * n + bbp, (bb * ng + g) * n + tp, b, vals[keep], nS, nF, nlab)
        ntup[name] = facs[name].ntup
        times.append(time.time() - t0)
    lab = np.arange(n)
    tt = np.repeat(lab, n * n); hh = np.tile(np.repeat(lab, n), n); bbs = np.tile(lab, n * n)
    adm3 = mfstruct._adm(tt, hh, bbs)
    st = dict(L=L, Lv=Lv, n=n, ng=ng, nS=nS, nF=nF, A1=facs['A1'], A2=facs['A2'], adm=adm3, t=tt, h=hh, bb=bbs, model=4, A1bond='X',
              ntup=(ntup['A1'], ntup['A2']), times=tuple(times))
    if verbose:
        print('mfstruct2 L=%d Lv=%d: tuples %d + %d, CSR nnz %d + %d (max merged %d, %d); A1 %.1fs, A2 %.1fs'
              % (L, Lv, ntup['A1'], ntup['A2'], facs['A1'].nnz, facs['A2'].nnz, facs['A1'].terms, facs['A2'].terms, times[0], times[1] - times[0]), flush=True)
    return st


if __name__ == '__main__':
    for L in [int(x) for x in sys.argv[1].split(',')]:
        build(L, vmax=2 * L)
