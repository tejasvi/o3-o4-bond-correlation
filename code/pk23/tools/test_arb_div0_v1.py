#!/usr/bin/env python3
"""test_arb_div0_v1.py (pk23): what python-flint's arb does when a ball that holds 0 is the divisor (for PLANT-FINITE in cw_comb v2_x3):
prints the quotient, its upper end as a float, and whether float() of it is finite; or the exception's name. Usage: test_arb_div0_v1.py"""
import math
import flint
arb = flint.arb
for den in (arb(0, 1), arb('0.5', 1), arb(1, '0.5')):
    try:
        q = arb(1) / den
        u = float(q.upper())
        print('1 / %s = %s; upper %r; finite %s' % (den.str(3), q.str(5), u, math.isfinite(u)))
    except Exception as exc:
        print('1 / %s raised %s: %s' % (den.str(3), type(exc).__name__, exc))
