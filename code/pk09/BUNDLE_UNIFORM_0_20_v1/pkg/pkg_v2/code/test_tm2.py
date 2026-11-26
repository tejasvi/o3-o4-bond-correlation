# Containment tests of the order-2 Taylor-model arithmetic (tm2.TM2) and of the vector models of certint3 (VT, vt_mv,
# vt_dm, vt_smul, vt_dot): exact polynomial inputs, values at sample points must lie in the model evaluated there.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from flint import arb, ctx
from tm2 import TM2
ctx.prec = 128
rng = np.random.default_rng(7)
bad = 0; tests = 0
def tm_at(f, t):
    """enclosure of the model f at the point t (|t| <= h)"""
    T = arb(t)
    return f.a0 + f.a1 * T + f.a2 * T * T + f.R * T * T * T
def poly(c, t):
    return sum(arb(x) * arb(t) ** k for k, x in enumerate(c))
for trial in range(200):
    h = float(10 ** rng.uniform(-4, -1))
    c = [float(rng.uniform(0.5, 2.0))] + [float(x) for x in rng.normal(0, 1, 3)]
    d = [float(rng.uniform(0.5, 2.0))] + [float(x) for x in rng.normal(0, 1, 3)]
    f = TM2(c[0], c[1], c[2], c[3], h); g = TM2(d[0], d[1], d[2], d[3], h)
    ops = [('mul', f * g, lambda t: poly(c, t) * poly(d, t)), ('inv', f.inv(), lambda t: 1 / poly(c, t)),
           ('sqrt', f.sqrt(), lambda t: poly(c, t).sqrt()), ('invsqrt', f.invsqrt(), lambda t: 1 / poly(c, t).sqrt()),
           ('sub', f - g * 2, lambda t: poly(c, t) - 2 * poly(d, t))]
    for name, m, ex in ops:
        for t in np.linspace(-h, h, 9):
            tests += 1
            if not tm_at(m, float(t)).overlaps(ex(float(t))):
                bad += 1
                if bad <= 5:
                    print('FAIL', name, h, t)
        lo, up = m.lower(), m.upper()
        for t in np.linspace(-h, h, 9):
            v = float(ex(float(t)).mid())
            tests += 1
            if not (lo <= v <= up):
                bad += 1
                if bad <= 5:
                    print('FAIL bounds', name, h, t, lo, v, up)
print('TM2: %d checks, %d failures' % (tests, bad))
# vector models: import the helpers of certint3 without running it (copy of the needed definitions)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certint3.py')).read()
start = src.index('class MR:'); stop = src.index('# ---------------- point part')
ns = {'np': np, 'arb': arb, 'math': math, 'TM2': TM2, 'U64': 2.0 ** -53, 'INF': 1 + 1e-12}
from tm2 import fdn, fup
ns['fdn'] = fdn; ns['fup'] = fup; ns['nS'] = 6
exec(src[start:stop], ns)
MR, VT = ns['MR'], ns['VT']
bad2 = 0; tests2 = 0
for trial in range(100):
    h = float(10 ** rng.uniform(-3, -1)); n = 6
    vc = [rng.normal(0, 1, n) for _ in range(3)]; vr = rng.normal(0, 1, n)
    v = VT(MR(vc[0], np.zeros(n)), MR(vc[1], np.zeros(n)), MR(vc[2], np.zeros(n)), MR(vr, np.zeros(n)))   # remainder = constant vector
    Mc = [rng.normal(0, 1, (n, n)) for _ in range(4)]
    Mt = tuple(MR(M, np.zeros((n, n))) for M in Mc)
    Mt = Mt + (ns['mtm_prange'](Mt[0], Mt[1], Mt[2], h),)
    dc = [rng.normal(0, 1, n) for _ in range(4)]
    Dt = tuple(MR(x, np.zeros(n)) for x in dc); Dt = Dt + (ns['mtm_prange'](Dt[0], Dt[1], Dt[2], h),)
    s = TM2(1.3, -0.4, 0.7, 0.2, h)
    mvv = ns['vt_mv'](Mt, v, h); dmv = ns['vt_dm'](Dt, v, h); smv = ns['vt_smul'](s, v, h)
    dt = ns['vt_dot'](v, mvv, h)
    for t in np.linspace(-h, h, 7):
        vt = vc[0] + vc[1] * t + vc[2] * t * t + vr * t ** 3
        Mtv = (Mc[0] + Mc[1] * t + Mc[2] * t * t + Mc[3] * t ** 3) @ vt
        Dtv = (dc[0] + dc[1] * t + dc[2] * t * t + dc[3] * t ** 3) * vt
        stv = (1.3 - 0.4 * t + 0.7 * t * t + 0.2 * t ** 3) * vt
        for name, model, exact in (('mv', mvv, Mtv), ('dm', dmv, Dtv), ('smul', smv, stv)):
            enc_c = model.c0.c + model.c1.c * t + model.c2.c * t * t + model.R.c * t ** 3
            enc_r = model.c0.r + model.c1.r * abs(t) + model.c2.r * t * t + model.R.r * abs(t) ** 3
            tests2 += 1
            if not np.all(np.abs(exact - enc_c) <= enc_r * (1 + 1e-9) + 1e-13 * (1 + np.abs(exact))):
                bad2 += 1
                if bad2 <= 5:
                    print('FAIL', name, h, t, float(np.max(np.abs(exact - enc_c) - enc_r)))
        tests2 += 1
        if not tm_at(dt, float(t)).overlaps(arb(float(vt @ Mtv), 1e-12 * (1 + abs(float(vt @ Mtv))))):
            bad2 += 1
            if bad2 <= 5:
                print('FAIL dot', h, t)
print('vector models: %d checks, %d failures' % (tests2, bad2))
