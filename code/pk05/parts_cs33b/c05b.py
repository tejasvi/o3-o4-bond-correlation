

def build(N, b0, h, L, K, out):
    """route H inputs as degree-K TMs: a~ (labels 0..2L+2), s = sqrt(a~), g = (T a~)/a~ (labels 0..2L, crude where the reciprocal is
    unusable), and per sector m: E~_m and X E~_m on degrees m..L (and their transposes)"""
    t1 = time.process_time()
    Kb, n1 = E.choose_Kb(h, K), E.choose_n1(b0)
    tail_f = E.fup_arb(E.series_tail(b0, n1))
    emb = E.arb_to_mr((-arb(b0)).exp())
    atm = E.corner_tm(N, b0, h, K, Kb, 2 * L)
    al, ga = E.t_coeffs(N, 2 * L + 2)
    nl = 2 * L + 3
    sub, sup = MR(ga.m[:nl].copy(), ga.r[:nl].copy()), MR(al.m[:nl].copy(), al.r[:nl].copy())
    sup.m[nl - 1], sup.r[nl - 1] = 0.0, 0.0
    Ta = E.tm_lin_rows(sub, sup, atm, 0.0).sub(slice(0, 2 * L + 1))
    a2 = atm.sub(slice(0, 2 * L + 1))
    s, sok = tm_sqrt(a2)
    rinv, rok = tm_recip(a2)
    g = E.tm_mul(Ta, rinv)
    lv = np.arange(2 * L + 1, dtype=np.float64)
    glo, ghi = dn(lv / up(b0 + h)), up(1.0 + up(lv / dn(b0 - h)))        # 0 < I_{nu+1}/I_nu < 1
    gm = 0.5 * glo + 0.5 * ghi
    gr = up(np.maximum(up(ghi - gm), up(gm - glo)))
    ok = rok & (g.R < gr)                                                   # v1_1: series where better than crude
    gc = [MR(np.where(ok, g.c[0].m, gm), np.where(ok, g.c[0].r, 0.0))]
    gc += [MR(np.where(ok, c.m, 0.0), np.where(ok, c.r, 0.0)) for c in g.c[1:]]
    g = TM(gc, np.where(ok, g.R, gr), h, K)
    Ek, XEk = [], []
    for m in range(L + 1):
        n = L + 1 - m
        Ef = E.kernel_tm(N, m, b0, h, K, Kb, L, n1, emb, tail_f)        # rows m..L+2, cols m..L
        x = E.x_offdiag(N, m, L + 3)
        nr = Ef.R.shape[0]
        xs = MR(np.concatenate(([0.0], x.m[:nr - 1])), np.concatenate(([0.0], x.r[:nr - 1])))
        xp = MR(np.concatenate((x.m[:nr - 1], [0.0])), np.concatenate((x.r[:nr - 1], [0.0])))
        Ek.append(Ef.sub(slice(0, n)))
        XEk.append(E.tm_lin_rows(xs, xp, Ef, 0.0).sub(slice(0, n)))
        guard('kernel')
    tr = lambda A: TM([MR(c.m.T.copy(), c.r.T.copy()) for c in A.c], A.R.T.copy(), A.h, A.k)
    out('BUILD N=%d L=%d K=%d Kb=%d n1=%d sertail=%.3e; labels 0..%d: sqrt TM on %d, g TM on %d (crude elsewhere); max rem a~ %.3e, '
        'E~ %.3e, XE~ %.3e; t=%.1f s' % (N, L, K, Kb, n1, tail_f, 2 * L, int(np.sum(sok)), int(np.sum(ok)), float(np.max(a2.R)),
                                        max(float(np.max(A.R)) for A in Ek), max(float(np.max(A.R)) for A in XEk), time.process_time() - t1))
    return dict(atm=atm, s=s, g=g, E=Ek, ET=[tr(A) for A in Ek], XE=XEk, XET=[tr(A) for A in XEk])


def trunc_consts(N, b0, h, L):
    """(eps_T, eps_e, A^3) as floats rounded up (R3 (v), R4 (iii)): A = e^h (b0/b-)^lam I_lam(b-)/I_lam(b0); eps_T = A^3 I_{L+1+lam}(b+)/
    I_lam(b+); eps_e = A^3 I_{L+lam}(b+)/I_lam(b+)"""
    lam = arb(N - 2) / 2
    b0a, bl, bh = arb(b0), arb(b0) - arb(h), arb(b0) + arb(h)
    A = arb(h).exp() * (b0a / bl) ** lam * bl.bessel_i(lam) / b0a.bessel_i(lam)
    I0 = bh.bessel_i(lam)
    return (E.fup_arb(A ** 3 * bh.bessel_i(lam + L + 1) / I0), E.fup_arb(A ** 3 * bh.bessel_i(lam + L) / I0), E.fup_arb(A ** 3))
