

class FV:
    """family vector (R9): v(t) = sum_d c_d t^d + r(t), c_d exact float arrays on the valid states, sup_{|t|<=h} |r(t)|_2 <= rho"""
    __slots__ = ('c', 'rho', 'h')

    def __init__(self, c, rho, h):
        self.c, self.rho, self.h = c, float(rho), h

    def pnorm(self):
        """>= sup_t |sum_d c_d t^d|_2"""
        acc, hp = 0.0, 1.0
        for x in self.c:
            acc = float(up(acc + vec_norm_ub(np.abs(x)) * hp))
            hp = float(up(hp * self.h))
        return float(up(acc * (1.0 + 4 * U)))

    def norm(self):
        return float(up(self.pnorm() + self.rho))


def fv_from_tm(T, L):
    """exact centres kept, coefficient radii and the remainder folded into a 2-norm"""
    rad, hp = np.zeros_like(T.R), 1.0
    for d in range(T.k + 1):
        rad = up(rad + T.c[d].r * hp)
        hp = up(hp * T.h)
    rad = up((rad + T.R) * (1.0 + 4 * U))
    return FV([to_compact(c.m).copy() for c in T.c], vec_norm_ub(to_compact(rad)), T.h)


def fv_tm(v, L, k):
    """dense TM of the polynomial part (remainder 0), degree k >= len(v.c) - 1"""
    cs = [MR(to_dense(x, L)) for x in v.c]
    z = np.zeros_like(cs[0].m)
    while len(cs) < k + 1:
        cs.append(MR(z.copy()))
    return TM(cs, z.copy(), v.h, k)


def fv_trunc(v, k):
    """drop the coefficients above k into rho"""
    if len(v.c) <= k + 1:
        return v
    extra, hp = 0.0, _hp(v.h, k + 1)
    for x in v.c[k + 1:]:
        extra = float(up(extra + vec_norm_ub(np.abs(x)) * hp))
        hp = float(up(hp * v.h))
    return FV(v.c[:k + 1], up(v.rho + extra), v.h)


def fv_apply(OP, v, opnorm, L, k):
    """the operator OP (TM inputs of degree k) applied: rho' = (folded TM error) + opnorm rho"""
    w = fv_from_tm(op_apply(OP, fv_tm(v, L, k)), L)
    w.rho = float(up(w.rho + opnorm * v.rho * (1.0 + 2 * U)))
    return w


def fv_diag(gT, v, gmax, L, k):
    """a diagonal TM multiplier gT (dense, degree k, entrywise |g| <= gmax) applied"""
    w = fv_from_tm(E.tm_mul(gT, fv_tm(v, L, k)), L)
    w.rho = float(up(w.rho + gmax * v.rho * (1.0 + 2 * U)))
    return w


def fv_comb(a, v, b, w):
    """a v + b w for exact floats a, b (rounding folded into rho)"""
    k = max(len(v.c), len(w.c))
    z = np.zeros_like(v.c[0])
    cs, rad, hp = [], 0.0, 1.0
    for d in range(k):
        x = v.c[d] if d < len(v.c) else z
        y = w.c[d] if d < len(w.c) else z
        mm = E.mr_add(E.mr_scale(MR(x), a), E.mr_scale(MR(y), b))
        cs.append(mm.m)
        rad = float(up(rad + vec_norm_ub(mm.r) * hp))
        hp = float(up(hp * v.h))
    return FV(cs, up(abs(a) * v.rho + abs(b) * w.rho + rad), v.h)


def fv_inner(v, w):
    """(arb coefficients of <P_v(t), P_w(t)>, error radius) with <v, w> in sum_d P_d t^d + [-e, e] for every |t| <= h"""
    P = [arb(0) for _ in range(len(v.c) + len(w.c) - 1)]
    for d, x in enumerate(v.c):
        for e, y in enumerate(w.c):
            g = gam(x.size + 2)
            P[d + e] = P[d + e] + arb(float(np.dot(x, y))) + arb(0, float(up(g * float(np.dot(np.abs(x), np.abs(y))) * (1.0 + 4 * g) + ETA)))
    nv, nw = v.pnorm(), w.pnorm()
    return P, float(up(nv * w.rho + v.rho * nw + v.rho * w.rho))
