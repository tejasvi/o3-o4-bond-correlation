# Wave 18, N = 3: consistency checks of the exact quadruple table (code5/o3struct.py) against the float engine
# (code5/o3sparse.py, independent log-space 6j symbols): the column map M = A2 A1 and its energy-inserted versions
# (r on the top or bottom vertical bond), entrywise relative to the sum of absolute values of the merged terms; the closed
# form of the boundary column b(t,h,bb) = W_t W_bb g(t,h,bb) (before K^{1/2}) against the quadruples with source |000>;
# and the size and build time of the table.
# usage: o3check.py L J
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import o3struct
from o3sparse import O3Strip
L, J = int(sys.argv[1]), float(sys.argv[2])
t0 = time.time(); Q = o3struct.quad_struct(L); t1 = time.time()
E = O3Strip(L); t2 = time.time()
assert [tuple(s) for s in Q['states']] == E.states
nS = Q['nS']; U = 2.0 ** -53
nb = sum(Q[k].nbytes for k in ('sp', 's', 'a', 'b', 'c', 'cabs', 'cnt'))
idx = Q['sp'].astype(np.int64) * nS + Q['s'].astype(np.int64)
nmax = int(np.bincount(idx, minlength=nS * nS).max())
print('L=%d: %d states, %d quadruples (%.0f MB), max merged terms %d, max quadruples per entry %d; table %.1fs, float engine %.1fs (nF %d)'
      % (L, nS, len(Q['c']), nb / 1e6, int(Q['cnt'].max()), nmax, t1 - t0, t2 - t1, E.nF), flush=True)
W = E.i(J); rW = E.r(J)
a = Q['a'].astype(np.int64); b = Q['b'].astype(np.int64)
for lab, wa, wb, B2, B1 in (('M', W, W, E.A2(W), E.A1(W)), ('M_X', W * rW, W, E.A2(W * rW), E.A1(W)), ('M_Y', W, W * rW, E.A2(W), E.A1(W * rW))):
    Mq = np.bincount(idx, weights=Q['c'] * wa[a] * wb[b], minlength=nS * nS).reshape(nS, nS)
    Ab = np.bincount(idx, weights=Q['cabs'] * wa[a] * wb[b], minlength=nS * nS).reshape(nS, nS)
    Me = (B2 @ B1).toarray()
    d = np.abs(Mq - Me)
    print('%-4s J=%g: max |table - engine| / abs-sum %.2e (in units of u: %.1f), max |table - engine| / max|M| %.2e, max |M| %.3e'
          % (lab, J, float(np.max(d / np.maximum(Ab, 1e-300))), float(np.max(d / np.maximum(Ab, 1e-300))) / U, float(d.max() / np.abs(Me).max()), float(np.abs(Me).max())), flush=True)
i0 = Q['states'].index((0, 0, 0))
sel = Q['s'] == i0
st = np.array(Q['states'])
c0 = np.zeros(nS); np.add.at(c0, Q['sp'][sel], Q['c'][sel])
ok_pq = bool(np.all(Q['a'][sel] == st[Q['sp'][sel], 0]) and np.all(Q['b'][sel] == st[Q['sp'][sel], 2]))
g = np.array([o3struct.gval(int(x[0]), int(x[1]), int(x[2])) for x in Q['states']])
print('boundary column: quadruples from |000> have p = t, q = bb: %s; one per state: %s; max |c0 - g| / |g| = %.2e'
      % (ok_pq, bool(np.bincount(Q['sp'][sel], minlength=nS).max() == 1), float(np.max(np.abs(c0 - g) / np.abs(g)))), flush=True)
# symmetry: S must be symmetric (M = A2 A1 is the compression of a symmetric operator)
Wh = np.sqrt(E.cut(W)); S = Wh[:, None] * (E.A2(W) @ E.A1(W)).toarray() * Wh[None, :]
print('engine S symmetric: max |S - S^T| / max |S| = %.2e; min eig / max eig = %.3e' % (float(np.abs(S - S.T).max() / np.abs(S).max()), float(np.linalg.eigvalsh(0.5 * (S + S.T))[0] / np.linalg.eigvalsh(0.5 * (S + S.T))[-1])), flush=True)
