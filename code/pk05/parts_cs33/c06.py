

def states(B, L, h, K):
    """product-basis TMs on the dense cube (l1, l3, j), l2 = |l1 - l3| + 2j, j <= min(l1, l3): D^1/2 = s s s, D = a~ a~ a~, and the
    horizontal insertion multipliers g_th = g_l1, g_mh = g_l2, g_bh = g_l3; mask and the flat index of valid states"""
    n = L + 1
    l2i = np.zeros((n, n, n), dtype=np.int64)
    mask = np.zeros((n, n, n))
    for l1 in range(n):
        for l3 in range(n):
            q = min(l1, l3) + 1
            l2i[l1, l3, :q] = abs(l1 - l3) + 2 * np.arange(q)
            mask[l1, l3, :q] = 1.0

    def bc(v, ax):
        shp = [1, 1, 1]
        shp[ax] = n
        return TM([MR(c.m[:n].reshape(shp), c.r[:n].reshape(shp)) for c in v.c], v.R[:n].reshape(shp), h, K)

    def gat(v):
        return TM([MR(c.m[l2i], c.r[l2i]) for c in v.c], v.R[l2i], h, K)
    s, a, g = B['s'], B['atm'].sub(slice(0, 2 * L + 1)), B['g']
    Dh = E.tm_mul(E.tm_mul(bc(s, 0), bc(s, 1)), gat(s))
    D = E.tm_mul(E.tm_mul(bc(a, 0), bc(a, 1)), gat(a))
    return dict(mask=mask, idx=np.flatnonzero(mask.ravel()), Dh=Dh, D=D, g={'th': bc(g, 0), 'mh': gat(g), 'bh': bc(g, 1)})


def to_dense(v, L):
    """compact (valid states) -> dense cube"""
    n = L + 1
    out = np.zeros(n ** 3)
    out[STATE['idx']] = v
    return out.reshape((n, n, n))


def to_compact(A):
    return np.asarray(A).reshape(-1)[STATE['idx']]


STATE = {}


def op_apply(OP, X):
    """TM image of a TM state X (dense) under OP = (groups, side-1 kernels, side-3 kernels transposed, D^1/2 TM, L): D^1/2 Q^T G Q D^1/2 X"""
    G, KA, KBT, Dh, L = OP
    Y = tm_blk(G, E.tm_mul(Dh, X), True)
    Y = tm_blk(G, tm_G(KA, KBT, Y, L), False)
    return E.tm_mul(Dh, Y)
