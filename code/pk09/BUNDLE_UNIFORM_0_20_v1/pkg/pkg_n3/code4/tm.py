# Scalar Taylor models on |t| <= h: f(t) = a0 + a1 t + t^2 rho(t), rho(t) in the arb ball R for all |t| <= h.
import numpy as np
from flint import arb


class TM:
    def __init__(self, a0, a1, R, h):
        self.a0, self.a1, self.R, self.h = arb(a0), arb(a1), arb(R), float(h)
        self.T = arb(0, self.h)                     # [-h, h]
        self.T2 = arb(self.h ** 2 / 2, self.h ** 2 / 2 * (1 + 1e-15))   # contains [0, h^2]

    @staticmethod
    def const(c, h):
        return TM(c, 0, 0, h)

    def _c(self, o):
        return o if isinstance(o, TM) else TM(o, 0, 0, self.h)

    def __add__(self, o):
        o = self._c(o)
        return TM(self.a0 + o.a0, self.a1 + o.a1, self.R + o.R, self.h)
    __radd__ = __add__

    def __neg__(self):
        return TM(-self.a0, -self.a1, -self.R, self.h)

    def __sub__(self, o):
        return self + (-self._c(o))

    def __rsub__(self, o):
        return self._c(o) - self

    def __mul__(self, o):
        o = self._c(o)
        R = self.a1 * o.a1 + self.R * (o.a0 + o.a1 * self.T) + o.R * (self.a0 + self.a1 * self.T) + self.T2 * self.R * o.R
        return TM(self.a0 * o.a0, self.a0 * o.a1 + self.a1 * o.a0, R, self.h)
    __rmul__ = __mul__

    def range(self):
        return self.a0 + self.a1 * self.T + self.T2 * self.R

    def inv(self):
        g = self.range()
        if g.contains(0):
            raise ZeroDivisionError('TM range contains 0')
        b0, b1 = self.a0, self.a1
        R = (b1 * b1 - self.R * (b0 - b1 * self.T)) / (g * b0 * b0)
        return TM(1 / b0, -b1 / (b0 * b0), R, self.h)

    def __truediv__(self, o):
        return self * self._c(o).inv()

    def lower(self):
        """Rigorous lower bound of f over |t| <= h."""
        m = self.R.lower()
        q = m if m < 0 else arb(0)
        x = (self.a0 - abs(self.a1) * arb(self.h) + q * arb(self.h) * arb(self.h)).lower()
        return float(np.nextafter(float(x), -np.inf))

    def upper(self):
        m = self.R.upper()
        q = m if m > 0 else arb(0)
        x = (self.a0 + abs(self.a1) * arb(self.h) + q * arb(self.h) * arb(self.h)).upper()
        return float(np.nextafter(float(x), np.inf))


def tm_apply(g, f0, f1, f2range):
    """f(g(t)) for a Taylor model g, with f0 = f(g.a0), f1 = f'(g.a0), f2range enclosing f'' over g.range()."""
    # g(t) - g0 = t (a1 + t R); f(g) = f0 + f1 (g - g0) + (1/2) f''(xi) (g - g0)^2
    s = g.a1 + g.T * g.R
    return TM(f0, f1 * g.a1, f1 * g.R + f2range * s * s * arb(0.5), g.h)


def tm_invsqrt(g):
    """1/sqrt(g) for a positive Taylor model g."""
    r = g.range()
    if not (r > 0):
        raise ValueError('invsqrt of a non-positive TM')
    a0 = g.a0
    return tm_apply(g, 1 / a0.sqrt(), arb(-0.5) / (a0 * a0.sqrt()), arb(0.75) / (r * r * r.sqrt()))


def tm_sqrt(g):
    r = g.range()
    if not (r > 0):
        raise ValueError('sqrt of a non-positive TM')
    a0 = g.a0
    return tm_apply(g, a0.sqrt(), arb(0.5) / a0.sqrt(), arb(-0.25) / (r * r.sqrt()))
