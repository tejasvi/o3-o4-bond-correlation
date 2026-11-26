#!/usr/bin/env python3
"""mr_core_v1_3.py (pk24): the frozen core of kt_mr_assembly v1_7, made by tools/make_core_proto_v1_3.py from mr_core_v1_2.py
(c6e5db3a) with EXPECT extended by tools/count_todo_bf_v1.py's independent count; mr_core_v1_2.py was the core of kt_mr_assembly
v1_4 to v1_6, made by tools/make_mrcore_v1_2.py from mr_core_v1_1.py (ec0587ab):
negation and modulus exact through copy_negate() and copy_abs() (unary minus and abs() would round in the current context).
mr_core_v1_1.py was made by tools/make_mrcore_v1_1.py (mr_core_v1.py with a directed square root). Do not edit: the engine pins this file's sha256, and its C-CORE gate compares the class-map blocks below with the M1
prototype's (midrow/g6_engine_proto_v1_2.py).
- Interval core: Iv holds decimal endpoints; every lower end comes from the ROUND_FLOOR context CF and every upper end from the
  ROUND_CEILING context CC (prec 50), through the contexts' own methods. Decimal.sqrt rounds half-even in any context, so sqrt_lo and
  sqrt_hi correct its result by one-ulp steps until r^2 <= x <= R^2, with the squares computed exactly at 4 x 50 digits. Inputs are decimal
  strings, read exactly. Products take the least and the greatest of the four endpoint products; division is only by positive intervals.
- Class map: byte copies of the prototype's blocks (the to-do list of P_3 x P_n, the pair position (type, d, k, d'), corner twins)."""
import re
from decimal import Decimal as Dm, Context, ROUND_FLOOR, ROUND_CEILING

PREC = 50
CF = Context(prec=PREC, rounding=ROUND_FLOOR)
CC = Context(prec=PREC, rounding=ROUND_CEILING)
CX = Context(prec=4 * PREC)
ONE = Dm(1)
ZERO = Dm(0)


def sqrt_lo(x):
    """the largest prec-digit r found from the half-even root by downward steps, with r^2 <= x (x >= 0)"""
    r = CF.sqrt(x)
    while CX.multiply(r, r) > x:
        r = CF.next_minus(r)
    return r


def sqrt_hi(x):
    """a prec-digit R found from the half-even root by upward steps, with R^2 >= x (x >= 0)"""
    r = CC.sqrt(x)
    while CX.multiply(r, r) < x:
        r = CC.next_plus(r)
    return r


class Iv:
    __slots__ = ('lo', 'hi')

    def __init__(s, lo, hi=None):
        s.lo, s.hi = lo, (lo if hi is None else hi)
        if not (s.lo <= s.hi):
            raise ValueError('interval with lo > hi: %r %r' % (s.lo, s.hi))

    def __add__(s, o):
        o = cv(o)
        return Iv(CF.add(s.lo, o.lo), CC.add(s.hi, o.hi))

    def __sub__(s, o):
        o = cv(o)
        return Iv(CF.subtract(s.lo, o.hi), CC.subtract(s.hi, o.lo))

    def __neg__(s):
        return Iv(s.hi.copy_negate(), s.lo.copy_negate())

    def __mul__(s, o):
        o = cv(o)
        a, b, c, d = s.lo, s.hi, o.lo, o.hi
        return Iv(min(CF.multiply(a, c), CF.multiply(a, d), CF.multiply(b, c), CF.multiply(b, d)),
                  max(CC.multiply(a, c), CC.multiply(a, d), CC.multiply(b, c), CC.multiply(b, d)))

    def inv(s):
        if not s.lo > 0:
            raise ValueError('inverse of a non-positive interval')
        return Iv(CF.divide(ONE, s.hi), CC.divide(ONE, s.lo))

    def __truediv__(s, o):
        return s * cv(o).inv()

    def __pow__(s, k):
        if not (isinstance(k, int) and k >= 0):
            raise ValueError('power needs an integer >= 0')
        r = Iv(ONE)
        for _ in range(k):
            r = r * s
        return r

    def amax(s):
        return max(s.lo.copy_abs(), s.hi.copy_abs())

    def sqrt(s):
        if s.lo < 0:
            raise ValueError('square root of an interval with a negative lower end')
        return Iv(sqrt_lo(s.lo), sqrt_hi(s.hi))

    def hull(s, o):
        o = cv(o)
        return Iv(min(s.lo, o.lo), max(s.hi, o.hi))

    def __repr__(s):
        return 'Iv(%s, %s)' % (s.lo, s.hi)


def cv(x):
    """an Iv as is; an int or a decimal string as a point interval (floats are refused: inputs are decimal strings)"""
    if isinstance(x, Iv):
        return x
    if isinstance(x, float):
        raise TypeError('float input to the interval core')
    return Iv(Dm(x) if isinstance(x, (str, int, Dm)) else Dm(str(x)))


def iv2(lo, hi):
    return Iv(Dm(lo), Dm(hi))


def up(x):
    """an upper bound read as the point interval [x, x]"""
    return Iv(Dm(x))


# ---------------------------------------------------------------- class map: byte copies of the prototype's blocks
RX = re.compile(r'^(t|h|bb|a|b)(\d+)$')
ROW = {'t': 0, 'h': 1, 'bb': 2}
EXPECT = {6: 25, 7: 37, 8: 52, 9: 69, 10: 89, 11: 111, 12: 136, 13: 163, 14: 193, 15: 225, 16: 260, 17: 297, 18: 337, 19: 379, 20: 424, 21: 471, 22: 521, 23: 573, 24: 628, 25: 685, 26: 745, 27: 807, 28: 872, 29: 939, 30: 1009}
def span(name):
    m = RX.match(name)
    ty, i = m.group(1), int(m.group(2))
    return (i, i + 1) if ty in ROW else (i, i)


def image(name, n, flip, refl):
    m = RX.match(name)
    ty, i = m.group(1), int(m.group(2))
    if flip:
        ty = {'t': 'bb', 'bb': 't', 'a': 'b', 'b': 'a'}.get(ty, ty)
    if refl:
        i = (n - i) if ty in ROW else (n + 1 - i)
    return '%s%d' % (ty, i)


def canon(e, f, n):
    return min(tuple(sorted((image(e, n, fl, rf), image(f, n, fl, rf)))) for fl in (0, 1) for rf in (0, 1))


def position(e, f, n):
    for rf in (0, 1):
        a, b = image(e, n, 0, rf), image(f, n, 0, rf)
        for x, y in ((a, b), (b, a)):
            if RX.match(x).group(1) != 'h':
                continue
            sx, sy = span(x), span(y)
            if sy[0] < sx[0] or (sy[0] == sx[0] and RX.match(y).group(1) == 'h' and int(RX.match(y).group(2)) < int(RX.match(x).group(2))):
                continue
            ty = {'bb': 't', 'b': 'a'}.get(RX.match(y).group(1), RX.match(y).group(1))
            i, j = int(RX.match(x).group(2)), int(RX.match(y).group(2))
            return ty, i - 2, sy[0] - sx[1] - 1, (n - j - 2) if RX.match(y).group(1) in ROW else (n - j - 1), (x, y)
    return None


def edges(n):
    E = {}
    for r, nm in ((0, 't'), (1, 'h'), (2, 'bb')):
        for i in range(1, n):
            E['%s%d' % (nm, i)] = ((r, i), (r, i + 1))
    for nm, r in (('a', 0), ('b', 1)):
        for j in range(1, n + 1):
            E['%s%d' % (nm, j)] = ((r, j), (r + 1, j))
    return E


def todo(n):
    E = edges(n)
    names = sorted(E)
    out = set()
    for ia in range(len(names)):
        for ib in range(ia + 1, len(names)):
            e, f = names[ia], names[ib]
            if 'h' not in (RX.match(e).group(1), RX.match(f).group(1)):
                continue
            if set(E[e]) & set(E[f]) or image(e, n, 0, 1) == f:
                continue
            out.add(canon(e, f, n))
    return sorted(out)


def corner_twin(e, f, n):
    tw = {'t1': 'a1', 'a1': 't1', 't%d' % (n - 1): 'a%d' % n, 'a%d' % n: 't%d' % (n - 1),
          'bb1': 'b1', 'b1': 'bb1', 'bb%d' % (n - 1): 'b%d' % n, 'b%d' % n: 'bb%d' % (n - 1)}
    E = edges(n)
    out = []
    for x, y in ((e, f), (f, e)):
        if y in tw and x != y and not (set(E[y]) & set(E[tw[y]]) & set(E[x])):
            out.append(canon(x, tw[y], n))
    return out
