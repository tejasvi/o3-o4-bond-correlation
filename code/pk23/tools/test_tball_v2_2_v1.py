#!/usr/bin/env python3
"""test_tball_v2_2_v1.py (pk23, C_w): checks cw_comb_v2_2's t-ball on every piece of MR_LEMMAP v3. T = ab((1/jlo + tlo)/2) +
arb(0, ab((1/jlo - tlo)/2).upper()), tlo = 1/jhi (0 on the last piece), from the exact Fractions of the jlo and jhi tokens, must contain
1/jlo and tlo, hence the piece's whole t-interval (a ball is convex). First checks that COMB holds the ab helper and the T line used here,
verbatim and once each. Prints the counts, the largest relative excess of T's radius over the exact half-width (INFO, float) and VERDICT.
Usage: test_tball_v2_2_v1.py COMB LEMMAP"""
import sys
from fractions import Fraction as Fr
import flint

flint.ctx.prec = 256
arb, fmpq = flint.arb, flint.fmpq
LINES = ['def ab(q):', '    q = Fr(q)', '    return arb(fmpq(q.numerator, q.denominator))',
         '        T = ab((1 / jq + tlo_q) / 2) + arb(0, ab((1 / jq - tlo_q) / 2).upper())   # v2_2: [1/jhi, 1/jlo] ([0, 1/jlo]) '
         'from exact endpoints']
assert len(sys.argv) == 3, __doc__.split('Usage: ')[1]
comb, lem = sys.argv[1], sys.argv[2]
with open(comb) as fh:
    code = fh.read().splitlines()
miss = [ln for ln in LINES if code.count(ln) != 1]
print('CODE %s: the ab helper and the T line occur once each: %s' % (comb.rsplit('/', 1)[-1], 'yes' if not miss else 'NO %r' % miss))


def ab(q):
    q = Fr(q)
    return arb(fmpq(q.numerator, q.denominator))


n = bad = nlast = 0
worst = 0.0
with open(lem) as fh:
    for ln in fh:
        if not (ln.startswith('N4_P') or ln.startswith('N3_P')):
            continue
        tok = ln.split(' = ', 1)[1].split()
        jq = Fr(tok[0])
        last = tok[1] == 'inf'
        tlo_q = Fr(0) if last else 1 / Fr(tok[1])
        T = ab((1 / jq + tlo_q) / 2) + arb(0, ab((1 / jq - tlo_q) / 2).upper())
        ok = T.contains(ab(1 / jq)) and T.contains(ab(tlo_q))
        n += 1
        nlast += last
        bad += not ok
        worst = max(worst, float(T.rad()) / float((1 / jq - tlo_q) / 2) - 1)
print('PIECES %d (%d last pieces to t = 0): T contains 1/jlo and tlo on %d of them; largest relative radius excess %.2e (INFO, float)' % (
    n, nlast, n - bad, worst))
print('VERDICT %s' % ('PASS' if not miss and not bad and n == 1747 and nlast == 2 else 'FAIL'))
sys.exit(0 if not miss and not bad and n == 1747 and nlast == 2 else 1)
