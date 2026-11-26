# Wave 18 item (4), scoping only (float, NOT a certificate): the §9.13 criterion quantities on 3 x n grids at uniform
# J >= 3 with the sparse engine (labels <= L, matrix-free transfer S = C^{1/2} A2 A1 C^{1/2}).  Reports per J: eigenvalue
# ratios and parities, (C2), (C3) signs, (C4) min p2 - p4 and F(0), (C5) safety at m = 0 and the per-pair threshold m0,
# (C7) same-column minimum, |eps(0)|, |Q5 u~|, and the deep decay (lam2/lam1).  Run at two cutoffs to see truncation.
# usage: scope40.py TAG L I J1,J2,...
import os, sys, time, math
import numpy as np
import scipy.sparse.linalg as sla
sys.path.insert(0, '/mnt/g2/release/root/data/e17/unif/scratch/code')
from strip_sparse import SparseStrip
tag, L, I = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
Js = [float(x) for x in sys.argv[4].split(',')]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out', 'scope40_%s.txt' % tag)
assert '/pkg_v2/out/' in OUT and not os.path.exists(OUT)
lines = []
def say(s):
    print(s, flush=True); lines.append(s)
    open(OUT, 'w').write('\n'.join(lines) + '\n')
t0 = time.time()
SS = SparseStrip(L)
n = L + 1
lab = np.arange(n)
t_ = np.repeat(lab, n * n); h_ = np.tile(np.repeat(lab, n), n); b_ = np.tile(lab, n * n)
flip = (b_ * n + h_) * n + t_
say('scope40 %s: L=%d I=%d; %d states, nnz %d + %d; build %.1fs' % (tag, L, I, SS.nS, SS.nnz1, SS.nnz2, time.time() - t0))
for J in Js:
    t1 = time.time()
    k = SS.k(J); r = SS.r(J); W = (lab + 1.0) * k
    c = SS.cutw((W, W, W)) * SS.adm3; sq = np.sqrt(c)
    A1, A2 = SS.A1(W), SS.A2(W); A1r, A2r = SS.A1(W * r), SS.A2(W * r)
    Sv = lambda v: sq * (A2 @ (A1 @ (sq * v)))
    TX = lambda v: sq * (A2 @ (A1r @ (sq * v)))
    TY = lambda v: sq * (A2r @ (A1 @ (sq * v)))
    TXY = lambda v: sq * (A2r @ (A1r @ (sq * v)))
    rng = np.random.default_rng(1); u = rng.standard_normal(SS.nS) * SS.adm3; w = rng.standard_normal(SS.nS) * SS.adm3
    asym = abs(u @ Sv(w) - w @ Sv(u)) / (abs(u @ Sv(w)) + 1e-300)
    op = sla.LinearOperator((SS.nS, SS.nS), matvec=Sv, dtype=float)
    lam, V = sla.eigsh(op, k=7, which='LA', tol=1e-13, maxiter=20000)
    o = np.argsort(-lam); lam = lam[o]; V = V[:, o]
    if V[:, 0].sum() < 0:
        V[:, 0] = -V[:, 0]
    par = [float(V[flip, j] @ V[:, j]) for j in range(5)]
    res = max(float(np.linalg.norm(Sv(V[:, j]) - lam[j] * V[:, j])) for j in range(5)) / lam[0]
    R = {'t': r[t_] * SS.adm3, 'h': r[h_] * SS.adm3, 'bb': r[b_] * SS.adm3}
    b = sq * k[t_] * k[b_]
    xs = [b / (V[:, 0] @ b)]
    for i in range(I + 1):
        y = Sv(xs[-1]); xs.append(y / (V[:, 0] @ y))
    cls = {}
    for tau in ('t', 'h', 'bb'):
        for i in range(I + 2):
            cls['%s@%d' % (tau, i)] = (tau, i, xs[i], R[tau] * xs[i])
    for vt, T in (('a', TX), ('b', TY)):
        for j in range(1, I + 2):
            y = Sv(xs[j - 1]); nj = V[:, 0] @ y
            cls['%s@%d' % (vt, j)] = (vt, j, xs[j], T(xs[j - 1]) / nj)
    data = {}
    for nm, (typ, pos, L1, LE) in cls.items():
        u0 = V[:, 0] @ L1; ce = (V[:, 0] @ LE) / u0
        ut = (LE - ce * L1) / u0
        al = [float(V[:, l] @ ut) for l in (1, 2, 3)]
        q5v = ut - V[:, :4] @ (V[:, :4].T @ ut)
        eps = L1 / u0 - V[:, 0]
        data[nm] = dict(typ=typ, pos=pos, al=al, nut=float(np.linalg.norm(ut)), neps=float(np.linalg.norm(eps)), q5=float(np.linalg.norm(q5v)), L1=L1 / u0, LE=LE / u0)
    side = {'t': 1, 'a': 1, 'bb': -1, 'b': -1, 'h': 0}
    s2 = np.sign(data['t@0']['al'][0]); s4 = np.sign(data['t@0']['al'][2]); s3 = np.sign(data['t@%d' % (I + 1)]['al'][1])
    ok2 = all(d['al'][0] * s2 > 0 for d in data.values()); ok4 = all(d['al'][2] * s4 > 0 for d in data.values())
    ok3 = all(d['al'][1] * s3 * side[d['typ']] > 0 for d in data.values() if side[d['typ']] != 0)
    l1, l2, l3, l4, l5 = lam[:5]
    worst = dict(F0=(9, None), pp=(9, None), same=(9, None), sf=(1e300, None))
    need = {}
    m0max = 0; m0pairs = 0
    for X, dX in data.items():
        for Y, dY in data.items():
            p2 = dX['al'][0] * dY['al'][0]; p4 = dX['al'][2] * dY['al'][2]
            p3 = 0.0 if (dX['typ'] == 'h' or dY['typ'] == 'h') else dX['al'][1] * dY['al'][1]
            opp = side[dX['typ']] * side[dY['typ']] < 0
            q55 = dX['q5'] * dY['q5']; AA = dX['nut'] * dX['neps'] * dY['nut'] * dY['neps']
            if opp:
                base = p2 + p3 + p4; ra, rb = l5 / l3, l2 * l2 / (l1 * l3)
                worst['F0'] = min(worst['F0'], (base, (X, Y))); worst['pp'] = min(worst['pp'], (p2 - p4, (X, Y)))
            else:
                base = p2 + p4; ra, rb = l5 / l4, l2 * l2 / (l1 * l4)
                worst['same'] = min(worst['same'], (base, (X, Y)))
            m = 0
            while base <= 0 or q55 * ra ** m + AA * rb ** m >= base:
                m += 1
                if m > 60:
                    break
            if m > 0:
                need[(X, Y)] = m
                m0pairs += 1
            m0max = max(m0max, m)
            worst['sf'] = min(worst['sf'], (base / max(q55 + AA, 1e-300), (X, Y)))
    # (C6) direct m-step covariance minors A D - B C for the pairs below their dominance threshold
    c6 = None
    for (X, Y), mXY in need.items():
        if mXY > 6:
            c6 = (-1.0, X, Y, -1); continue
        cl1, clE = data[X]['L1'], data[X]['LE']; r1, rE = data[Y]['L1'], data[Y]['LE']
        for m in range(mXY):
            if not (m == 0 and data[X]['typ'] == data[Y]['typ'] and data[X]['typ'] in ('t', 'h', 'bb')):
                A_ = clE @ rE; B_ = clE @ r1; C_ = cl1 @ rE; D_ = cl1 @ r1
                v = (A_ * D_ - B_ * C_) / D_ ** 2
                if c6 is None or v < c6[0]:
                    c6 = (v, X, Y, m)
            r1 = Sv(r1); rE = Sv(rE); nn = V[:, 0] @ r1; r1 = r1 / nn; rE = rE / nn
    # (C7) same-column pairs
    c7 = None
    for iL in range(I + 2):
        for iR in range(I + 2):
            l_, r_ = xs[iL], xs[iR]
            a_ = l_ @ TXY(r_); s_ = l_ @ Sv(r_); x_ = l_ @ TX(r_); y_ = l_ @ TY(r_)
            v = (a_ * s_ - x_ * y_) / s_ ** 2
            if c7 is None or v < c7[0]:
                c7 = (v, iL, iR)
    say('J=%g: lam_k/lam_1 %s; parities %s; residual %.1e; asym %.1e; conv %.5f lam1; signs a2 %s a4 %s a3 %s; min F(0) %.4e at %s; min p2-p4 %.4e at %s; same-side %.4e; '
        'safety(m=0) %.3g at %s; m0 %d (%d pairs); C6 min %s; C7 min %.4e at %s; |eps(0)| %.3e; max |Q5 u~| %.3e (%.1fs)'
        % (J, ' '.join('%.5f' % (x / l1) for x in lam[1:6]), ' '.join('%+.0f' % p for p in par), res, asym, (l2 + l4 - 2 * l3) / l1, ok2, ok4, ok3,
           worst['F0'][0], worst['F0'][1], worst['pp'][0], worst['pp'][1], worst['same'][0], worst['sf'][0], worst['sf'][1], m0max, m0pairs, ('%.4e at %s' % (c6[0], c6[1:])) if c6 else '-',
           c7[0], c7[1:], data['t@0']['neps'], max(d['q5'] for d in data.values()), time.time() - t1))
say('done %.1fs' % (time.time() - t0))
