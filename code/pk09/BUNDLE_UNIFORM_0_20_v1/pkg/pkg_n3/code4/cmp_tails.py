# Wave 18 (UNIF 9.21): the MINOR-2 for the certificates already in the ledgers.  certint4 / o3cert bounded the
# character-sum tails beyond label L+59 by the factor (1 + 1e-10); certint5 / o3cert2 use the rigorous geometric
# remainder term_{L+59} q/(1 - q).  Every truncation constant is an increasing function of these tail sums, and every
# bound of the certifier is increasing in the truncation constants, so a certificate of the old code is a certificate
# of the new one if, on its interval, remainder <= 1e-10 * (explicit sum) for every tail sum.  This script checks that
# (in arb) for every CERT line of the given ledgers, and also the n5 ratio bound q_r5 < 1.
# usage: cmp_tails.py MODEL ledger1 ledger2 ...      MODEL = o4 | o3
import sys
from flint import arb, ctx
ctx.prec = 128
model = sys.argv[1]
worst = 0.0; worst_q5 = 0.0; n = 0; bad = 0
for fn in sys.argv[2:]:
    for line in open(fn):
        p = line.split()
        if len(p) < 5 or p[4] != 'CERT':
            continue
        J0, h, L = float(p[0]), float(p[1]), int(p[2])
        Ja = arb(J0) + arb(h); Jl = arb(J0) - arb(h)
        AE = L + 59
        if model == 'o4':
            ks = [2 * Ja.bessel_i(l + 1) / Ja for l in range(AE + 1)]
            kr = Ja / (2 * AE + 3); m2 = arb(AE + 2) / (AE + 1)
            mult = lambda l: arb(l + 1) ** 2      # vertical tail multiplicity (l+1)^2
            sums = [([mult(a) * ks[a] for a in range(L + 1, AE + 1)], m2 * m2 * kr),
                    ([mult(a) * ks[a] * (a / Jl + 1) for a in range(L + 1, AE + 1)], m2 * m2 * kr * (AE + 1) / AE),
                    ([(l + 1) * ks[l] ** 3 for l in range(L + 1, AE + 1)], m2 * kr ** 3),
                    ([(l + 1) * ks[l] for l in range(L + 1, AE + 1)], m2 * kr)]
            rr = [(arb(l) / Jl + 1) ** 2 for l in range(AE + 1)]
            rq = (arb(AE + 1) / AE) ** 2
            sums += [([rr[l] * (l + 1) * ks[l] ** 3 for l in range(L + 1, AE + 1)], rq * m2 * kr ** 3),
                     ([rr[l] * (l + 1) * ks[l] for l in range(L + 1, AE + 1)], rq * m2 * kr)]
            q5 = ((arb(L + 2) + Ja) / (L + 1)) ** 2 * Ja / (2 * L + 5)
        else:
            pre = (arb.pi() / (2 * Ja)).sqrt()
            ks = [pre * Ja.bessel_i(arb(l) + arb(1) / 2) for l in range(AE + 1)]
            kr = Ja / (2 * AE + 2); m2 = arb(2 * AE + 3) / (2 * AE + 1)
            rr = [(arb(l) / Jl + 1) ** 2 for l in range(AE + 1)]
            rq = (arb(AE + 1) / AE) ** 2
            sums = [([(2 * a + 1) * ks[a] for a in range(L + 1, AE + 1)], m2 * kr),
                    ([(2 * a + 1) * ks[a] * (a / Jl + 1) for a in range(L + 1, AE + 1)], m2 * kr * (AE + 1) / AE),
                    ([(2 * l + 1) * ks[l] ** 3 for l in range(L + 1, AE + 1)], m2 * kr ** 3),
                    ([rr[l] * (2 * l + 1) * ks[l] ** 3 for l in range(L + 1, AE + 1)], rq * m2 * kr ** 3)]
            q5 = ((arb(L + 2) + Ja) / (L + 1)) ** 2 * Ja / (2 * L + 4)
        n += 1
        for terms, q in sums:
            assert q.upper() < 1
            S = sum(terms, arb(0)); rem = terms[-1] * q / (1 - q)
            ratio = float((rem / (S * arb(1e-10))).upper())
            worst = max(worst, ratio)
            if not (rem.upper() <= (S * arb(1e-10)).lower()):
                bad += 1
        worst_q5 = max(worst_q5, float(q5.upper()))
        if not (q5.upper() < 1):
            bad += 1
print('%s: %d certified intervals; max over tail sums of remainder / (1e-10 explicit sum) = %.3e; max n5 ratio bound q_r5 = %.4f; violations: %d'
      % (model, n, worst, worst_q5, bad), flush=True)
