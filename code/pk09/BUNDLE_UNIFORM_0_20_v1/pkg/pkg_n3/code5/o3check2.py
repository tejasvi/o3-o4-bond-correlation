# Wave 18, N = 3: the interval assembly of code5/o3lib3.py against the float engine code5/o3sparse.py at a point J:
# S, T_X, T_Y, T_XY and b (engine weights are e^{-J} i_l, so S carries e^{-5J}, b e^{-7J/2}), and the first and second
# J-derivatives against central finite differences of the engine (step 1e-3: truncation error ~1e-7 relative).
# Also checks that every engine value lies in the assembled interval (orders 0) up to float noise of the engine.
# usage: o3check2.py L J
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from flint import arb, ctx
import o3struct, o3lib3
from o3sparse import O3Strip
ctx.prec = 128
L, J = int(sys.argv[1]), float(sys.argv[2])
Q = o3struct.quad_struct(L); E = O3Strip(L); nS = Q['nS']
A = o3lib3.assemble_derivs(Q, Q['states'], arb(J), 2)
def eng(Jx):
    W = E.i(Jx); Wr = W * E.r(Jx); sq = np.sqrt(E.cut(W))
    out = {}
    for nm, (w2, w1) in (('S', (W, W)), ('TX', (Wr, W)), ('TY', (W, Wr)), ('TXY', (Wr, Wr))):
        out[nm] = (sq[:, None] * (E.A2(w2) @ E.A1(w1)).toarray() * sq[None, :]) * math.exp(5 * Jx)
    out['b'] = sq * (E.A2(W) @ (E.A1(W) @ E.vac())) * math.exp(3.5 * Jx)
    return out
e0 = eng(J); hd = 1e-3; ep = eng(J + hd); em = eng(J - hd)
for nm in ('S', 'TX', 'TY', 'TXY', 'b'):
    iv = A[nm]; lo = iv.lo.reshape(e0[nm].shape); hi = iv.hi.reshape(e0[nm].shape)
    mid = 0.5 * (lo + hi); scale = np.abs(e0[nm]).max()
    d0 = np.abs(mid - e0[nm]).max() / scale
    out_ = np.maximum(lo - e0[nm], e0[nm] - hi).max() / scale
    fd1 = (ep[nm] - em[nm]) / (2 * hd); fd2 = (ep[nm] - 2 * e0[nm] + em[nm]) / hd ** 2
    m1 = 0.5 * (A[nm + '1'].lo + A[nm + '1'].hi).reshape(fd1.shape); m2 = 0.5 * (A[nm + '2'].lo + A[nm + '2'].hi).reshape(fd2.shape)
    print('%-4s L=%d J=%g: |mid - engine|/max %.2e; engine outside interval by <= %.2e (rel); radius/max %.2e; d1 vs FD %.2e; d2 vs FD %.2e'
          % (nm, L, J, d0, out_, float((0.5 * (hi - lo)).max() / scale), float(np.abs(m1 - fd1).max() / np.abs(fd1).max()), float(np.abs(m2 - fd2).max() / np.abs(fd2).max())), flush=True)
