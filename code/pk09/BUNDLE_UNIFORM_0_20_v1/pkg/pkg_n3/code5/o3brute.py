# Validation of code5/o3sparse.py: the same truncated O(3) strip transfer built in the explicit m-basis
# e_{l1 m1}(s_t) e_{l2 m2}(s_h) e_{l3 m3}(s_bb) with Gaunt coefficients from sympy (no recoupling theory):
#   O_12 = sum_{p <= Lb} i_p sum_mu e_{p mu}(s_t) e_{p mu}(s_h)^*,  O_23 likewise,  M = P O_12 O_23 P  (P: labels <= Lb;
#   the middle spin's intermediate labels run up to 2 Lb, the outer spins' intermediates are cut at Lb exactly, since
#   O_12 does not act on s_bb and O_23 not on s_t),  S = K^{1/2} M K^{1/2}, b = K^{1/2} M |000>,  Z(P3 x Pn) = <b, S^{n-2} b>.
# Also the first-column energy insertions (i_p -> i_p r_p on the top or bottom vertical bond).
# usage: o3brute.py Lb J1,J2,.. n1,n2,..
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sympy.physics.wigner import gaunt
from o3sparse import O3Strip
Lb = int(sys.argv[1]); Js = [float(x) for x in sys.argv[2].split(',')]; ns = [int(x) for x in sys.argv[3].split(',')]
lmB = [(l, m) for l in range(2 * Lb + 1) for m in range(-l, l + 1)]
dB = len(lmB); dA = (Lb + 1) ** 2
pos = {x: i for i, x in enumerate(lmB)}
# G[p, mu][(l', m'), (l, m)] = int e*_{l'm'} e_{p mu} e_{lm} dsigma = sqrt(4 pi) (-1)^{m'} gaunt(l', p, l, -m', mu, m);
# only entries with at least one index in the l <= Lb block are needed
G = {}
for p in range(Lb + 1):
    for mu in range(-p, p + 1):
        M = np.zeros((dB, dB))
        for (l1, m1) in lmB:
            for (l, m) in lmB:
                if -m1 + mu + m != 0 or (pos[(l1, m1)] >= dA and pos[(l, m)] >= dA) or (l1 + p + l) % 2:
                    continue
                v = gaunt(l1, p, l, -m1, mu, m)
                if v != 0:
                    M[pos[(l1, m1)], pos[(l, m)]] = (-1) ** m1 * math.sqrt(4 * math.pi) * float(v)
        G[(p, mu)] = M
E = O3Strip(Lb)
for J in Js:
    il = E.i(J); rl = E.r(J)
    def O23(x, w):          # x[t, h, bb] (all <= Lb) -> y[t, h2, bb2], h2 <= 2 Lb, bb2 <= Lb
        y = np.zeros((dA, dB, dA))
        for p in range(Lb + 1):
            for mu in range(-p, p + 1):
                y += w[p] * (-1) ** mu * np.einsum('Hh,Bb,thb->tHB', G[(p, mu)][:, :dA], G[(p, -mu)][:dA, :dA], x)
        return y
    def O12(y, w):          # y[t, h2, bb] (h2 <= 2 Lb) -> z[t2, h3, bb], all <= Lb
        z = np.zeros((dA, dA, dA))
        for p in range(Lb + 1):
            for mu in range(-p, p + 1):
                z += w[p] * (-1) ** mu * np.einsum('Tt,Hh,thb->THb', G[(p, mu)][:dA, :dA], G[(p, -mu)][:dA, :], y)
        return z
    kd = np.array([il[l] for (l, m) in lmB[:dA]])
    sq = np.sqrt(np.einsum('i,j,k->ijk', kd, kd, kd))
    vac = np.zeros((dA, dA, dA)); vac[0, 0, 0] = 1.0
    b = sq * O12(O23(vac, il), il)
    bX = sq * O12(O23(vac, il), il * rl)
    bY = sq * O12(O23(vac, il * rl), il)
    for n in ns:
        x = b.copy()
        for _ in range(n - 2):
            x = sq * O12(O23(sq * x, il), il)
        for lab, bb_, ins in (('Z', b, None), ('Z_X', bX, 'X'), ('Z_Y', bY, 'Y')):
            zb = float(np.sum(bb_ * x))
            ze = E.Z(J, n, ins)
            print('Lb=%d J=%g n=%d %-4s m-basis %.15e engine %.15e rel diff %.2e' % (Lb, J, n, lab, zb, ze, abs(zb - ze) / abs(ze)), flush=True)
