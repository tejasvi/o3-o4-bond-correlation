# Check of certlib3.bessel_derivs (Riccati / monotone hulls) against the direct Bessel formulas.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, ctx
import certlib3
ctx.prec = 128
def bd_old(Ja, nmax):
    Is = [Ja.bessel_i(n) for n in range(nmax + 7)]
    I = lambda n: Is[abs(n)]
    res = {'k': [], 'r': [], 'r1': [], 'r2': [], 'r3': []}
    for l in range(nmax + 1):
        nu = l + 1
        I0 = I(nu); I1 = (I(nu - 1) + I(nu + 1)) / 2; I2 = (I(nu - 2) + 2 * I(nu) + I(nu + 2)) / 4
        I3 = (I(nu - 3) + 3 * I(nu - 1) + 3 * I(nu + 1) + I(nu + 3)) / 8
        I4 = (I(nu - 4) + 4 * I(nu - 2) + 6 * I(nu) + 4 * I(nu + 2) + I(nu + 4)) / 16
        g1, g2, g3, g4 = I1 / I0, I2 / I0, I3 / I0, I4 / I0
        res['k'].append(2 * I0 / Ja)
        res['r'].append(g1 - 1 / Ja); res['r1'].append(g2 - g1 * g1 + 1 / (Ja * Ja))
        res['r2'].append(g3 - 3 * g1 * g2 + 2 * g1 ** 3 - 2 / Ja ** 3)
        res['r3'].append(g4 - 4 * g1 * g3 - 3 * g2 * g2 + 12 * g1 * g1 * g2 - 6 * g1 ** 4 + 6 / Ja ** 4)
    return res
worst = 0.0
for J in ('0.01', '0.05', '0.3', '1', '2.5', '3.2'):
    Ja = arb(J)
    a, b = bd_old(Ja, 16), certlib3.bessel_derivs(Ja, 16)
    for key in ('k', 'r', 'r1', 'r2', 'r3'):
        for l in range(17):
            d = abs(a[key][l] - b[key][l]) / (abs(a[key][l]) + 1e-30)
            worst = max(worst, float(d.upper()))
print('point check: max relative difference old vs new (J = 0.01 .. 3.2, l <= 16): %.2e' % worst)
for (J0, h) in ((0.03, 0.001), (0.3, 0.01), (1.0, 0.05), (2.5, 0.08)):
    B = certlib3.bessel_derivs(arb(J0, h), 16)
    Bo = bd_old(arb(J0, h), 16)
    bad = 0
    for i in range(41):
        Jp = arb(J0 - h + 2 * h * i / 40)
        P = bd_old(Jp, 16)
        for key in ('k', 'r', 'r1', 'r2', 'r3'):
            for l in range(17):
                if not B[key][l].contains(P[key][l]):
                    bad += 1
    wn = max(float(B['r3'][l].rad()) for l in range(17)); wo = max(float(Bo['r3'][l].rad()) for l in range(17))
    wn2 = max(float(B['r2'][l].rad()) for l in range(17)); wo2 = max(float(Bo['r2'][l].rad()) for l in range(17))
    print('ball J0=%g h=%g: sample points outside the new enclosures: %d; max radius r3 new %.3e old %.3e; r2 new %.3e old %.3e; r3(l=12) = %s'
          % (J0, h, bad, wn, wo, wn2, wo2, B['r3'][12].str(5)))
