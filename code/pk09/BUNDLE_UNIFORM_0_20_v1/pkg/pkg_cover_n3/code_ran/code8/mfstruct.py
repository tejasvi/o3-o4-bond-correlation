# Wave 18, matrix-free certifier (UNIF 9.24-): exact structure of the N = 4 three-row column map as two sparse factors.
#   A1: state (t, h, bb) -> hub (bb, g, tp), coefficient {bb g tp; a t h}^2 (g + 1) W_a     (vertical label a: rows 1-2)
#   A2: hub (bb, g, tp) -> state (tp, hp, bbp), coefficient {tp hp bbp; b bb g}^2 W_b       (vertical label b: rows 2-3)
# (the conventions of code/strip_sparse.py, which the dense certint5 tables reproduce).  Squared 6j symbols are evaluated
# EXACTLY (su2lib.sixj_sq, rationals) once per tetrahedral-symmetry class and rounded to float (relative error <= 2^-53);
# the canonical class key is the smallest of the sorted column triples over the 4 upper/lower swap patterns.
# For each factor the structure stores the merged CSR pattern (entries with equal (row, col) over the vertical label are
# summed per weight vector) and, per tuple, its position in the CSR data array, its vertical label and its exact-rounded
# coefficient, so that A(w) for any weight vector w is one bincount.
import sys, time
import numpy as np
import scipy.sparse as sp
sys.path.insert(0, '/mnt/g2/release/root/data/e15/dy4/scratch/code')
from su2lib import sixj_sq


def _adm(x, y, z):
    return ((x + y + z) % 2 == 0) & (np.abs(x - y) <= z) & (z <= x + y)


def sixj_tuples(r123, r456):
    """index tuples (x1..x6) of the admissible {x1 x2 x3; x4 x5 x6} with x1..x3 in the box r123, x4..x6 in r456
    (triangles (x1,x2,x3), (x1,x5,x6), (x4,x2,x6), (x4,x5,x3)); int16 array [6, n]"""
    n1, n2, n3 = r123
    n4, n5, n6 = r456
    D, E, F = np.meshgrid(np.arange(n4), np.arange(n5), np.arange(n6), indexing='ij')
    out = []
    for a in range(n1):
        for b in range(n2):
            for c in range(abs(a - b), min(a + b, n3 - 1) + 1, 2):
                m = _adm(a, E, F) & _adm(D, b, F) & _adm(D, E, c)
                if not m.any():
                    continue
                cnt = int(m.sum())
                out.append(np.stack([np.full(cnt, a), np.full(cnt, b), np.full(cnt, c), D[m], E[m], F[m]]).astype(np.int16))
    return np.concatenate(out, axis=1)


def canon_keys(T, B):
    """canonical int64 key per 6j tuple (columns (x1,x4), (x2,x5), (x3,x6)); B > every label"""
    a, b, c, d, e, f = [T[i].astype(np.int64) for i in range(6)]
    best = None
    for (u0, l0, u1, l1, u2, l2) in ((a, d, b, e, c, f), (d, a, e, b, c, f), (d, a, b, e, f, c), (a, d, e, b, f, c)):
        cols = np.sort(np.stack([u0 * B + l0, u1 * B + l1, u2 * B + l2]), axis=0)
        k = (cols[0] * B * B + cols[1]) * B * B + cols[2]
        best = k if best is None else np.minimum(best, k)
    return best


def exact_values(keys, B):
    """float(exact {6j}^2) for canonical keys (columns decoded in sorted order)"""
    raw = sixj_sq.__wrapped__ if hasattr(sixj_sq, '__wrapped__') else sixj_sq
    BB = B * B
    out = np.empty(len(keys))
    for i, k in enumerate(keys.tolist()):
        c2 = k % BB; k //= BB; c1 = k % BB; c0 = k // BB
        out[i] = float(raw(c0 // B, c1 // B, c2 // B, c0 % B, c1 % B, c2 % B))
    return out


class Factor:
    """one sparse factor: CSR pattern of shape (nr, nc), per-tuple position, vertical label and coefficient"""
    def __init__(self, rows, cols, vlab, coef, nr, nc):
        key = rows.astype(np.int64) * nc + cols.astype(np.int64)
        uk, pos = np.unique(key, return_inverse=True)
        r = (uk // nc).astype(np.int64); c = (uk % nc).astype(np.int32)
        self.indptr = np.searchsorted(r, np.arange(nr + 1)).astype(np.int64)
        self.indices = c
        self.pos = pos.astype(np.int64); self.vlab = vlab.astype(np.int64); self.coef = coef
        self.nr, self.nc, self.nnz = nr, nc, len(uk)
        self.rowcount = int(np.max(np.diff(self.indptr))) if nr > 0 else 0
        self.terms = int(np.max(np.bincount(self.pos))) if len(pos) else 0      # max tuples merged into one entry

    def data(self, w):
        """CSR data for the vertical weight vector w (float array over labels)"""
        return np.bincount(self.pos, weights=self.coef * w[self.vlab], minlength=self.nnz)

    def matrix(self, data):
        return sp.csr_matrix((data, self.indices, self.indptr), shape=(self.nr, self.nc))


def build(L, verbose=True, vmax=None):
    """vmax: largest vertical label (default L); vmax = 2L keeps every vertical label of a cut state (a <= t + tp, b <= bb + bbp),
    so the restriction of the full transfer to the cut states is exact (no vertical tail)"""
    t0 = time.time()
    Lv = L if vmax is None else vmax
    n = L + 1; ng = 2 * L + 1; nv = Lv + 1; B = max(2 * L, Lv) + 3
    T1 = sixj_tuples((n, ng, n), (nv, n, n))         # (bb, g, tp, a, t, h)
    T2 = sixj_tuples((n, n, n), (nv, n, ng))         # (tp, hp, bbp, b, bb, g)
    t1 = time.time()
    k1 = canon_keys(T1, B); k2 = canon_keys(T2, B)
    uk, inv = np.unique(np.concatenate([k1, k2]), return_inverse=True)
    t2 = time.time()
    vals = exact_values(uk, B)
    t3 = time.time()
    v1 = vals[inv[:len(k1)]]; v2 = vals[inv[len(k1):]]
    keep1 = v1 != 0; keep2 = v2 != 0
    bb, g, tp, a, t, h = [T1[i][keep1].astype(np.int64) for i in range(6)]
    nS = n ** 3; nF = n * ng * n
    A1 = Factor((bb * ng + g) * n + tp, (t * n + h) * n + bb, a, v1[keep1] * (g + 1.0), nF, nS)
    tp2, hp, bbp, b, bb2, g2 = [T2[i][keep2].astype(np.int64) for i in range(6)]
    A2 = Factor((tp2 * n + hp) * n + bbp, (bb2 * ng + g2) * n + tp2, b, v2[keep2], nS, nF)
    lab = np.arange(n)
    tt = np.repeat(lab, n * n); hh = np.tile(np.repeat(lab, n), n); bbs = np.tile(lab, n * n)
    adm3 = _adm(tt, hh, bbs)
    st = dict(L=L, Lv=Lv, n=n, ng=ng, nS=nS, nF=nF, A1=A1, A2=A2, adm=adm3, t=tt, h=hh, bb=bbs,
              ntup=(int(keep1.sum()), int(keep2.sum())), nclass=len(uk),
              times=(t1 - t0, t2 - t1, t3 - t2, time.time() - t3))
    if verbose:
        print('mfstruct L=%d Lv=%d: tuples %d + %d, 6j classes %d, CSR nnz %d + %d (max merged %d, %d); enumerate %.1fs, keys %.1fs, exact %.1fs, CSR %.1fs'
              % ((L, Lv) + st['ntup'] + (len(uk), A1.nnz, A2.nnz, A1.terms, A2.terms) + st['times']), flush=True)
    return st


if __name__ == '__main__':
    for L in [int(x) for x in sys.argv[1].split(',')]:
        build(L)
