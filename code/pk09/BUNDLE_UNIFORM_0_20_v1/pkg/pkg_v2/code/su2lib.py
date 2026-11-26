# SU(2) recoupling: exact squared 6j symbols for labels l = 2j (integers); K4-type label kernels with general edge spectra.
from fractions import Fraction as Fr
from math import factorial
from functools import lru_cache


def adm(a, b, c):
    return (a + b + c) % 2 == 0 and abs(a - b) <= c <= a + b


@lru_cache(maxsize=None)
def fact(n):
    return factorial(n)


@lru_cache(maxsize=None)
def delta2(a, b, c):
    # Delta(j1 j2 j3)^2 with labels a=2j1 etc.: (j1+j2-j3)!(j1-j2+j3)!(-j1+j2+j3)!/(j1+j2+j3+1)!
    return Fr(fact((a + b - c) // 2) * fact((a - b + c) // 2) * fact((-a + b + c) // 2), fact((a + b + c) // 2 + 1))


@lru_cache(maxsize=None)
def sixj_sq(a, b, c, d, e, f):
    """{j1 j2 j3; j4 j5 j6}^2 with (a,b,c,d,e,f) = 2*(j1..j6). Triangles: (a,b,c),(a,e,f),(d,b,f),(d,e,c)."""
    if not (adm(a, b, c) and adm(a, e, f) and adm(d, b, f) and adm(d, e, c)):
        return Fr(0)
    al = [(a + b + c) // 2, (a + e + f) // 2, (d + b + f) // 2, (d + e + c) // 2]
    be = [(a + b + d + e) // 2, (b + c + e + f) // 2, (c + a + f + d) // 2]
    s = 0
    for z in range(max(al), min(be) + 1):
        term = fact(z + 1)
        den = 1
        for x in al:
            den *= fact(z - x)
        for y in be:
            den *= fact(y - z)
        s += (-1) ** z * Fr(term, den)
    return delta2(a, b, c) * delta2(a, e, f) * delta2(d, b, f) * delta2(d, e, c) * s * s
