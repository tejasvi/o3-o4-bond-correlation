# Wave 18, N = 3: spot check of the float error bound of the quadruple table (code5/o3struct.py).  For a random sample of
# quadruples (s', s, p, q), c is recomputed as an arb ball (256 bits) from the exact rationals of every 3j(000) and 6j
# factor, summing over the intermediate b2; the check is |c_float - c_exact| <= (cnt + 16) u cabs, as claimed.
# usage: o3check3.py L NSAMPLE SEED
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import numpy as np
from flint import arb, fmpq, ctx
import o3struct
from o3struct import tri, three0_sq, delta_sq, fact
ctx.prec = 256
L, NS, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
Q = o3struct.quad_struct(L)
st = Q['states']; U = 2.0 ** -53
def sixj_exact(j1, j2, j3, j4, j5, j6):
    if not (tri(j1, j2, j3) and tri(j1, j5, j6) and tri(j4, j2, j6) and tri(j4, j5, j3)):
        return 0, Fr(0)
    al = [j1 + j2 + j3, j1 + j5 + j6, j4 + j2 + j6, j4 + j5 + j3]
    be = [j1 + j2 + j4 + j5, j2 + j3 + j5 + j6, j3 + j1 + j6 + j4]
    s = Fr(0)
    for z in range(max(al), min(be) + 1):
        den = 1
        for x in al:
            den *= fact(z - x)
        for y in be:
            den *= fact(y - z)
        s += (-1) ** z * Fr(fact(z + 1), den)
    if s == 0:
        return 0, Fr(0)
    return (1 if s > 0 else -1), delta_sq(j1, j2, j3) * delta_sq(j1, j5, j6) * delta_sq(j4, j2, j6) * delta_sq(j4, j5, j3) * s * s
def g_exact(a, b, c):
    s, R = three0_sq(a, b, c)
    return s, R * (2 * a + 1) * (2 * b + 1) * (2 * c + 1)
def ball(sign, R):
    return sign * arb(fmpq(R.numerator, R.denominator)).sqrt() if sign else arb(0)
rng = np.random.default_rng(seed)
pick = rng.choice(len(Q['c']), size=min(NS, len(Q['c'])), replace=False)
worst = 0.0; fails = 0
for i in pick:
    (a1, b1, c1), (a, b, c) = st[int(Q['sp'][i])], st[int(Q['s'][i])]
    p, q = int(Q['a'][i]), int(Q['b'][i])
    tot = arb(0); n = 0
    for b2 in range(abs(b - q), b + q + 1, 2):
        if not (tri(a, b2, c1) and tri(b1, p, b2) and (b1 + p + b2) % 2 == 0):
            continue
        # A1 = (-1)^{a+c+c'} g(b2,q,b) g(c',q,c) {b2 c' a; c b q};  A2 = (-1)^{a+b'} g(a',p,a) g(b',p,b2) {a' b' c'; b2 a p}
        f1 = [g_exact(b2, q, b), g_exact(c1, q, c), sixj_exact(b2, c1, a, c, b, q)]
        f2 = [g_exact(a1, p, a), g_exact(b1, p, b2), sixj_exact(a1, b1, c1, b2, a, p)]
        sg = (-1) ** (a + c + c1) * (-1) ** (a + b1)
        R = Fr(1)
        for (s_, R_) in f1 + f2:
            sg *= s_; R *= R_
        if sg:
            tot += ball(sg, R); n += 1
    err = abs(tot - float(Q['c'][i]))
    bound = (int(Q['cnt'][i]) + 16) * U * float(Q['cabs'][i])
    ratio = float(err.upper()) / bound
    worst = max(worst, ratio)
    if not (err.upper() <= bound) or n != int(Q['cnt'][i]):
        fails += 1
print('L=%d: %d sampled quadruples; |c_float - c_exact| / ((cnt + 16) u cabs) <= %.3f; violations (or term-count mismatches): %d'
      % (L, len(pick), worst, fails), flush=True)
