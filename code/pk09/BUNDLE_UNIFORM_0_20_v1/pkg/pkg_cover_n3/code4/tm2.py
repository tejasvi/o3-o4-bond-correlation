# Scalar Taylor models of order 2 on |t| <= h: f(t) = a0 + a1 t + a2 t^2 + t^3 rho(t), with rho(t) in the arb ball R
# for every |t| <= h.  Arithmetic: +, -, *, composition with a smooth function (inv, invsqrt, sqrt); rigorous float
# lower/upper bounds over |t| <= h.
import numpy as np
from flint import arb


def fdn(x):
    """float <= every point of the arb ball x"""
    return float(np.nextafter(float(x.lower()), -np.inf))


def fup(x):
    return float(np.nextafter(float(x.upper()), np.inf))


class TM2:
    __slots__ = ('a0', 'a1', 'a2', 'R', 'h', 'H', 'H2', 'H3', 'T', 'T2', 'T3')

    def __init__(self, a0, a1, a2, R, h):
        self.a0, self.a1, self.a2, self.R = arb(a0), arb(a1), arb(a2), arb(R)
        self.h = float(h)
        self.H = arb(self.h); self.H2 = self.H * self.H; self.H3 = self.H2 * self.H
        u = arb(0, 1)
        self.T = self.H * u                      # [-h, h]
        self.T2 = self.H2 / 2 * (1 + u)          # [0, h^2]
        self.T3 = self.H3 * u                    # [-h^3, h^3]

    def _c(self, o):
        return o if isinstance(o, TM2) else TM2(o, 0, 0, 0, self.h)

    def __add__(self, o):
        o = self._c(o)
        return TM2(self.a0 + o.a0, self.a1 + o.a1, self.a2 + o.a2, self.R + o.R, self.h)
    __radd__ = __add__

    def __neg__(self):
        return TM2(-self.a0, -self.a1, -self.a2, -self.R, self.h)

    def __sub__(self, o):
        return self + (-self._c(o))

    def __rsub__(self, o):
        return self._c(o) - self

    def prange(self):
        """enclosure of the polynomial part over |t| <= h"""
        return self.a0 + self.a1 * self.T + self.a2 * self.T2

    def range(self):
        return self.prange() + self.R * self.T3

    def __mul__(self, o):
        o = self._c(o)
        a0 = self.a0 * o.a0
        a1 = self.a0 * o.a1 + self.a1 * o.a0
        a2 = self.a0 * o.a2 + self.a1 * o.a1 + self.a2 * o.a0
        # f g = P_f P_g + t^3 (rho_f g + P_f rho_g); the t^3, t^4 terms of P_f P_g go to the remainder
        R = self.a1 * o.a2 + self.a2 * o.a1 + self.T * self.a2 * o.a2 + self.R * o.range() + o.R * self.prange()
        return TM2(a0, a1, a2, R, self.h)
    __rmul__ = __mul__

    def addball(self, r):
        """f + e(t) with |e(t)| <= r (float) for all t"""
        return TM2(self.a0 + arb(0, float(r)), self.a1, self.a2, self.R, self.h)

    def compose(self, f0, f1, f2, f3range):
        """F(f(t)) for smooth F with F(a0) = f0, F'(a0) = f1, F''(a0) = f2 and F''' in f3range over range(f)."""
        # f - a0 = t s(t), s = a1 + a2 t + rho t^2;  t^2 s^2 = a1^2 t^2 + t^3 (a2 + rho t)(s + a1)
        S = self.a1 + self.a2 * self.T + self.R * self.T2
        a1 = f1 * self.a1
        a2 = f1 * self.a2 + f2 * self.a1 * self.a1 / 2
        R = f1 * self.R + f2 / 2 * (self.a2 + self.R * self.T) * (S + self.a1) + f3range / 6 * S * S * S
        return TM2(f0, a1, a2, R, self.h)

    def inv(self):
        g = self.range()
        if g.contains(0):
            raise ZeroDivisionError('TM2 range contains 0')
        a0 = self.a0
        return self.compose(1 / a0, -1 / (a0 * a0), 2 / (a0 * a0 * a0), -6 / (g * g * g * g))

    def invsqrt(self):
        g = self.range()
        if not (g > 0):
            raise ValueError('invsqrt of a non-positive TM2')
        a0 = self.a0; s0 = a0.sqrt()
        return self.compose(1 / s0, arb(-0.5) / (a0 * s0), arb(0.75) / (a0 * a0 * s0), arb(-1.875) / (g * g * g * g.sqrt()))

    def sqrt(self):
        g = self.range()
        if not (g > 0):
            raise ValueError('sqrt of a non-positive TM2')
        a0 = self.a0; s0 = a0.sqrt()
        return self.compose(s0, arb(0.5) / s0, arb(-0.25) / (a0 * s0), arb(0.375) / (g * g * g.sqrt()))

    def lower(self):
        """rigorous float lower bound of f over |t| <= h"""
        m = self.a2.lower()
        q = m if m < 0 else arb(0)
        return fdn(self.a0 - abs(self.a1) * self.H + q * self.H2 - abs(self.R) * self.H3)

    def upper(self):
        m = self.a2.upper()
        q = m if m > 0 else arb(0)
        return fup(self.a0 + abs(self.a1) * self.H + q * self.H2 + abs(self.R) * self.H3)
