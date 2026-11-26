

def fv_scale(v, c):
    """multiply by an exact power of two"""
    return FV([x * c for x in v.c], v.rho * c, v.h)


def make_perm(L):
    """compact permutation of the side swap rho: (l1, l3, j) -> (l3, l1, j) (R5 (iv))"""
    n = L + 1
    idx = C.STATE['idx']
    l1, rest = np.divmod(idx, n * n)
    l3, j = np.divmod(rest, n)
    pos = np.full(n ** 3, -1, dtype=np.int64)
    pos[idx] = np.arange(idx.size)
    return pos[(l3 * n + l1) * n + j]


def fv_rho(v):
    return FV([x[PERM[0]] for x in v.c], v.rho, v.h)


def fv_sector(v, sg):
    """(v + sg rho v)/2: the sector part (sg = +1 even, -1 odd)"""
    return C.fv_comb(0.5, v, 0.5 * sg, fv_rho(v))


PERM = [None]


class IPS:
    """inner products <a, b> of named family vectors as (arb polynomial, error); per-subball values with the truncation slack"""

    def __init__(self, fvs, slack):
        self.fvs, self.slack, self.cache, self.vals = fvs, slack, {}, {}

    def poly(self, a, b):
        key = (a, b) if a <= b else (b, a)
        if key not in self.cache:
            P, e = C.fv_inner(self.fvs[key[0]], self.fvs[key[1]])
            e = float(up(e + self.slack * self.fvs[key[0]].norm() * self.fvs[key[1]].norm()))
            self.cache[key] = (P, e)
        return self.cache[key]

    def val(self, a, b, tb, ti):
        key = (a, b, ti) if a <= b else (b, a, ti)
        if key not in self.vals:
            P, e = self.poly(a, b)
            self.vals[key] = E.ev(P, arb(0, e), tb)
        return self.vals[key]

    def norm(self, a):
        return self.fvs[a].norm()


def ival(lo, hi):
    """arb ball containing the exact points lo <= hi"""
    return lo.union(hi)
