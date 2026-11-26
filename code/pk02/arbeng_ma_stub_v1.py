#!/usr/bin/env python3
"""arbeng_ma_stub_v1.py -- pk02 (code/pk02/). Build target for the M-a layer's kernel interface: SPEC_MA_LAYER_v1_2 (d8b05870)
sect. 6 plus pk03's requests (PLAN_M3_CODE_v1 ffdf8446 sect. 2a): the polynomial type SPoly, AllMom2 with mp.iv in and out,
lp_moment and pos_moment, the M-e probes. Every value is computed in arb through arbeng_c2b_v2 (fb8cd1b5): correct enclosures, arb speed,
no M-a. SPoly's shadow fields (codes, mid, sa, sr, k) are filled from its arb coefficients (sa = |mid|, sr >= |mid| + rad, k = 0); in
arbeng_ma_v1 they are the true M-a shadows. Importers pin this file's sha256 and re-pin to arbeng_ma_v1 once it passes its validation;
the API is the same. No compute of its own.
API:
  env_probes() -> str
  SPoly(nv) | SPoly.from_dict(P, nv)    P: {exponent tuple: v}, v = (mid, rad) floats | mp.iv interval | arb | Fraction | int | float
    .to_dict() -> {exp: mp.iv};  .to_arb_dict() -> {exp: arb};  .codes, .mid, .sa, .sr, .k (arrays);  .nv
    .add/__add__, .sub/__sub__, .scale(c), .div_int(n), .mul(Q, keep=None), .power(k, keep=None)
    keep(exponent array (m x nv) int64) -> bool array: truncation (a ring quotient). A coefficient is dropped only when it is exactly 0
    (value and both shadows 0).
  AllMom2(Gam, n, D, groups=None, caps=None, W_int=None)   Gam: F x F list of mp.iv or arb_mat; minors formed inside (exact zeros by W_int)
    .E(P) -> mp.iv;  .E2(P, Q) -> mp.iv;  .zeroed;  .shadow_max()          P, Q: SPoly or {exp: value}
  lp_moment(table, P, p) -> mp.iv  (E[P^(p/2) P^(p/2)], p even);  pos_moment(table, P, p) -> mp.iv  (E[P^p])
  For pk02's own items (arb in and out): MomTable/allmom2 (.E, .E2 -> arb), CondTable/condmom (.condE), npoly_mul, npoly_pow,
  lp_norm, pos_norm, budget, MAFallback.
"""
import math, os, sys
from fractions import Fraction
import numpy as np
from flint import arb, arb_mat
from mpmath import iv, libmp

_OWN = os.path.dirname(os.path.abspath(__file__))
if _OWN not in sys.path:
    sys.path.insert(0, _OWN)
import arbeng_c2b_v2 as _ae

VERSION = 'arbeng_ma_stub_v1'


class MAFallback(ArithmeticError):
    """as arbeng_ma_v1 (never raised by the stub)."""


def env_probes():
    a = math.ldexp(3, -54)
    ok = (1.0 + a) == 1.0 + 2.0 ** -52 and (-1.0 - a) == -(1.0 + 2.0 ** -52) and math.ldexp(1, -1074) > 0
    ok = ok and math.ldexp(1, -1022) / 2 != 0 and bool((np.array([math.ldexp(1, -1022)]) / 2.0)[0] != 0.0)
    if not ok:
        raise RuntimeError('M-e probe failed')
    return 'M-e probes PASS; %s (arb-backed stub)' % VERSION


def budget(err, bar):
    return float(err) <= 0.1 * float(bar)


def mpi_to_arb(x):
    """an mp.iv interval as an arb ball containing it (exact endpoints)."""
    a, b = x._mpi_
    ma, ea = libmp.to_man_exp(a)
    mb, eb = libmp.to_man_exp(b)
    lo = arb(int(ma)) * arb(2) ** int(ea)
    hi = arb(int(mb)) * arb(2) ** int(eb)
    return lo.union(hi)


def arb_to_mpi(x):
    """an arb ball as an mp.iv interval containing it (exact midpoint and radius, then mid + rad [-1, 1] in mp.iv)."""
    mm, me = x.mid().man_exp()
    rm, re = x.rad().man_exp()
    m = iv.mpf(int(mm)) * iv.mpf(2) ** int(me)
    r = iv.mpf(int(rm)) * iv.mpf(2) ** int(re)
    return m + r * iv.mpf([-1, 1])


def to_arb(v):
    """a coefficient as an arb ball: (mid, rad) floats, mp.iv, arb, Fraction, int or float (exact)."""
    if isinstance(v, arb):
        return v
    if isinstance(v, tuple):
        return arb(float(v[0])) + arb(0, float(v[1]))
    if isinstance(v, Fraction):
        return arb(v.numerator) / v.denominator
    if isinstance(v, (int, np.integer)):
        return arb(int(v))
    if isinstance(v, float):
        return arb(float(v))
    if hasattr(v, '_mpi_'):
        return mpi_to_arb(v)
    raise TypeError('coefficient type %r' % type(v))


def _up(x):
    u = x.upper()
    f = float(u)
    if not (arb(f) >= u):
        f = math.nextafter(f, math.inf)
    return f


class SPoly:
    """the kernel polynomial type (arb-backed in the stub)."""
    def __init__(self, nv, d=None):
        self.nv = nv
        self._d = {} if d is None else {e: c for e, c in d.items() if not c.is_zero()}

    @classmethod
    def from_dict(cls, P, nv=None):
        if nv is None:
            nv = len(next(iter(P))) if P else 0
        d = {}
        for e, v in P.items():
            e = tuple(int(x) for x in e)
            assert len(e) == nv
            c = to_arb(v)
            d[e] = d[e] + c if e in d else c
        return cls(nv, d)

    def to_dict(self):
        return {e: arb_to_mpi(c) for e, c in self._d.items()}

    def to_arb_dict(self):
        return dict(self._d)

    def _arrays(self):
        if not self._d:
            z = np.zeros(0)
            return np.zeros(0, dtype=np.int64), z, z, z, np.zeros(0, dtype=np.int64)
        ex = np.array(list(self._d.keys()), dtype=np.int64)
        B = int(ex.max()) + 1
        assert float(B) ** self.nv < 9.0e18
        codes = ex @ np.array([B ** i for i in range(self.nv)], dtype=np.int64)
        mid = np.array([float(c.mid()) for c in self._d.values()])
        sa = np.abs(mid)
        sr = np.array([math.nextafter(abs(float(c.mid())) + _up(c.rad() + abs(c.mid() - arb(float(c.mid())))), math.inf)
                       for c in self._d.values()])
        return codes, mid, sa, sr, np.zeros(len(mid), dtype=np.int64)

    codes = property(lambda self: self._arrays()[0])
    mid = property(lambda self: self._arrays()[1])
    sa = property(lambda self: self._arrays()[2])
    sr = property(lambda self: self._arrays()[3])
    k = property(lambda self: self._arrays()[4])

    def add(self, Q):
        assert Q.nv == self.nv
        d = dict(self._d)
        for e, c in Q._d.items():
            d[e] = d[e] + c if e in d else c
        return SPoly(self.nv, d)

    def sub(self, Q):
        return self.add(Q.scale(-1))

    __add__, __sub__ = add, sub

    def scale(self, c):
        ca = to_arb(c)
        return SPoly(self.nv, {e: v * ca for e, v in self._d.items()})

    def div_int(self, n):
        assert isinstance(n, int) and n != 0
        return SPoly(self.nv, {e: v / n for e, v in self._d.items()})

    def mul(self, Q, keep=None):
        assert Q.nv == self.nv
        d = {}
        items_q = list(Q._d.items())
        for e1, c1 in self._d.items():
            exs = np.array([[x + y for x, y in zip(e1, e2)] for e2, _ in items_q], dtype=np.int64).reshape(-1, self.nv)
            ok = keep(exs) if keep is not None else np.ones(len(items_q), dtype=bool)
            for (e2, c2), row, k_ in zip(items_q, exs, ok):
                if not k_:
                    continue
                e = tuple(int(x) for x in row)
                v = c1 * c2
                d[e] = d[e] + v if e in d else v
        return SPoly(self.nv, d)

    def power(self, k, keep=None):
        assert k >= 1
        out = self
        for _ in range(k - 1):
            out = out.mul(self, keep)
        return out


class MomTable:
    """arb in, arb out (pk02's items); over arbeng_c2b_v2.AllMom2A with W_int's exact zeros."""
    def __init__(self, Gam, n, D, groups=None, caps=None, W_int=None, chunk=4000000):
        if not isinstance(Gam, arb_mat):
            F = len(Gam)
            G = arb_mat(F, F)
            for i in range(F):
                for j in range(F):
                    G[i, j] = to_arb(Gam[i][j])
            Gam = G
        self._am = _ae.AllMom2A(Gam, n, D, groups=groups, caps=caps, chunk=chunk, W_int=W_int)
        self.F, self.D, self.n = self._am.F, self._am.D, n
        self.zeroed = self._am.zeroed

    def shadow_max(self):
        return 0.0

    @staticmethod
    def _dict(P):
        return P.to_arb_dict() if isinstance(P, SPoly) else {tuple(e): to_arb(v) for e, v in P.items()}

    def E(self, P, fallback=True):
        d = self._dict(P)
        return self._am.E(d) if d else arb(0)

    def E2(self, P, Q, fallback=True):
        d1, d2 = self._dict(P), self._dict(Q)
        return self._am.E2(d1, d2) if d1 and d2 else arb(0)


class AllMom2(MomTable):
    """pk03's interface: Gam in mp.iv (or arb), E and E2 out as mp.iv enclosures."""
    def E(self, P, fallback=True):
        return arb_to_mpi(MomTable.E(self, P))

    def E2(self, P, Q, fallback=True):
        return arb_to_mpi(MomTable.E2(self, P, Q))


def allmom2(Gam, n, D, groups=None, caps=None, W_int=None, chunk=4000000):
    return MomTable(Gam, n, D, groups=groups, caps=caps, W_int=W_int, chunk=chunk)


def lp_moment(table, P, p):
    assert p % 2 == 0 and p >= 2
    Pk = P.power(p // 2) if isinstance(P, SPoly) else SPoly.from_dict(P).power(p // 2)
    return table.E2(Pk, Pk)


def pos_moment(table, P, p):
    assert p >= 1
    Pk = P.power(p) if isinstance(P, SPoly) else SPoly.from_dict(P).power(p)
    return table.E(Pk)


class CondTable:
    """arb in, arb out; over arbeng_c2b_v2.CondMomA and CondGA."""
    def __init__(self, Mmat, Cmat, W, W_int, n, Dc, groups=None, caps=None, chunk=4000000):
        self._cm = _ae.CondMomA(Mmat, Cmat, W, n, Dc, groups=groups, caps=caps, chunk=chunk)
        self.entries = sum(len(v) for v in self._cm.table.values())

    def shadow_max(self):
        return 0.0

    def condE(self, P12, Dout, batch=4000000):
        cg = _ae.CondGA(self._cm, Dout)
        return cg.out.to_dict(cg.condE(P12)), 0


def condmom(Mmat, Cmat, W, W_int, n, Dc, groups=None, caps=None, chunk=4000000):
    return CondTable(Mmat, Cmat, W, W_int, n, Dc, groups=groups, caps=caps, chunk=chunk)


def npoly_mul(P, Q, keep=None):
    nv = len(next(iter(P))) if P else 0
    return SPoly.from_dict(P, nv).mul(SPoly.from_dict(Q, nv), keep).to_arb_dict() if P and Q else {}


def npoly_pow(P, k, keep=None):
    return SPoly.from_dict(P).power(k, keep).to_arb_dict() if P else {}


def _root_ball(x, p):
    if not (x.upper() > 0):
        return arb(0)
    if x.lower() > 0:
        return x ** (arb(1) / p)
    hu = math.nextafter(float((arb(x.upper()) ** (arb(1) / p)).upper()), math.inf)
    return arb(hu / 2, hu / 2)


def lp_norm(table, P, p):
    assert p % 2 == 0 and p >= 2
    if not P:
        return arb(0)
    Pk = npoly_pow(P, p // 2)
    return _root_ball(table.E2(Pk, Pk), p)


def pos_norm(table, P, p):
    assert p >= 1
    if not P:
        return arb(0)
    return _root_ball(table.E(npoly_pow(P, p)), p)
