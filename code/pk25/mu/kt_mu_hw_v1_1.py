#!/usr/bin/env python3
"""kt_mu_hw_v1_1.py -- pk25 (code/pk25/mu/). v1_1 (the P0_LOG row 4370): MU-3 now states c_hi >= 0,
which gives K = c_N t - (A - c_hi) >= -A >= -3/2 at N = 3, 4, the bound the u > 1 branch of MU-3's proof takes; tail_ok checks K >= -3/2 and
one_row checks c_hi >= 0, both certainly. Nothing else changes, so every value equals v1's wherever v1's hypotheses held with c_hi >= 0.
v1: kt_mu_hw_v1.py -- pk25 (code/pk25/mu/). The mu tool of G5 (G5_PLAN_v1_ADD1_1 sect. 3, item C8; ADD1_2: it also exports the one-row
|M_c K^1/2|), as a module of certified upper bounds in python-flint arb, in pk24's normalisation (a_0 = 1, |V| = 1; g6_hwn1_v1):
    OR(J; c)          = sup_{l >= 0} |m(l) - c| a_l^{1/2}                                    (one row: |M_c K^1/2| <= OR),
    TRX(J; c_t, c_h)  = sup_{l1, l2 >= 0} |m(l1) m(l2) - c_t m(l2) - c_h m(l1)| (a_l1 a_l2)^{1/2}   (Xi_c = M_t M_h - c_t M_h - c_h M_t),
    TRP(J; c_t, c_h)  = OR(J; c_t) OR(J; c_h)                                                (the product form (M_t - c_t)(M_h - c_h)),
with a_l = I_{l+nu}(J)/I_nu(J), m(l) = J (1 - I_{l+nu+1}(J)/I_{l+nu}(J)) - l, nu = (N - 2)/2, t = 1/J. m(l) is g6_hwn1_v1's beta (1 - g_l)
and H_BESSEL_NOTE_v1's w_l/v_l. The engine forms C = OR lambda_0'^{-1/2} and C_J = TR lambda_0'^{-1/2} with its own lambda_0' lower end.
Why TRP serves Proposition J: w_J = Q0 Xi_c u and Xi_c = (M_t - c_t)(M_h - c_h) - c_t c_h, so w_J = Q0 (M_t - c_t)(M_h - c_h) u (Q0 u = 0);
the N-1 bound with Pi = |u><u| then gives |w_J| <= |(M_t - c_t)(M_h - c_h) K^1/2| lambda_0^{-1/2} <= TRP lambda_0'^{-1/2} (a_l3 <= a_0 = 1).

Lemma MU-1. For N in {3, 4}, every J > 0 and every l >= 0, with y = y_l = l (l + N - 2) t / 2, A = (N - 1)/2, c_N = 2 + (N - 1)(N - 3)/8:
  (a) A - c_N t - y < m(l) < A (H-BESSEL: pk08/H_BESSEL_NOTE_v1.md sect. 3);
  (b) a_l <= exp(-y + E(y, t)) with E(y, t) = t y^2 / 6 + t^2 nu^2 y / 6.
  Proof of (b). a_l = prod_{k < l} r_{nu+k}(J) with r_mu = I_{mu+1}/I_mu. By (U) of H_BESSEL_NOTE_v1 sect. 2, r_mu(J) < J/(a + (J^2 + a^2 +
  a)^{1/2}) <= exp(-asinh(a t)) with a = mu + 1/2, here a_k = k + (N - 1)/2. asinh z >= z - z^3/6 for z >= 0 (the derivative of the
  difference is (1 + z^2)^{-1/2} - 1 + z^2/2 >= 0). sum_{k<l} a_k t = y. Since x^3 is convex on x >= 0 and a_k - 1/2 = k + nu >= 0, the
  midpoint rule gives sum_{k<l} a_k^3 <= ((l + nu)^4 - nu^4)/4, and (l + nu)^2 = 2 y / t + nu^2. Hence sum_k asinh(a_k t) >= y - (t^3/24)
  ((2 y/t + nu^2)^2 - nu^4) = y - E(y, t). QED
Corollary MU-2. Put g(y) = -y/2 + E(y, t)/2 (convex in y), M0 = max_c |A - c| and K = c_N t - (A - c_hi) over c in [c_lo, c_hi]. Then
  |m(l) - c| a_l^{1/2} <= Phi(y_l) := max(M0, y_l + K) exp(g(y_l)). For TRX, m1 m2 - c_t m2 - c_h m1 is multilinear in (m1, m2, c_t, c_h), so
  on the box m_i in [A - c_N t - y_i, A] (closed hull of (a)) its modulus is at most its largest modulus over the 16 vertices, V(y1, y2);
  then the TRX term is at most Psi(y1, y2) := V(y1, y2) exp(g(y1) + g(y2)). Phi and Psi are nondecreasing in t (t enters K, E and the box
  with nonnegative signs; the box only grows), so a piece's largest t bounds the piece, and t = 1/300 every J >= 300.
Lemma MU-3 (the tail). Let t <= 1/299, c_hi >= 0 (v1_1: then K >= -3/2) and Y_max with Y_max + K >= max(3, M0). Let l0 be the first l
  with y_l >= Y_max. Then for l >= l0,
  |m(l) - c| a_l^{1/2} <= b(l) := (y_l + K) exp(-(1/2) sum_{k<l} asinh(a_k t)), and b is nonincreasing on l >= l0, so the sup over l >= l0
  is at most b(l0) <= Phi(y_l0), with y_l0 < Y_cut := Y_max + t ((2 Y_max/t + nu^2)^{1/2} + 1/2).
  Proof. b(l+1)/b(l) = (1 + u/Y) exp(-asinh(u)/2) with u = a_l t = y_{l+1} - y_l and Y = y_l + K >= 3. If u <= 1, asinh u >= 5u/6, so the
  log of the ratio is at most u (1/Y - 5/12) < 0. If u > 1, then a_l > J >= 299 and y_l = t ((a_l - 1/2)^2 - nu^2)/2 >= u (a_l - 3/2)/2
  (as a_l >= 2 nu^2 - 1/2), so Y = y_l + K >= 148 u - 3/2 (by K >= -3/2) >= 146 u and u/Y <= 1/146 < asinh(1)/2. The step bound: (l0 - 1 + nu)^2 = 2 y_{l0-1}/t +
  nu^2 < 2 Y_max/t + nu^2. The check uses t <= 1/299 so that a piece starting at J = 300 passes with its t ball. QED
  So OR <= sup over y in [0, Y_cut] of Phi. For TRX, with l1 >= l1_0 and l2 fixed, |P| <= alpha (y1 + A + c_N t) + beta (alpha = max |m2 - c_h|,
  beta = max |c_t| max |m2|), whose b-sequence is nonincreasing by the same ratio argument (y1 + A + c_N t >= 3), and at l1 = l1_0 it is
  nonincreasing in l2 >= l2_0 too (slope form gamma (y2 + delta/gamma) with delta/gamma >= -max(|K_h|, A), checked >= 3 - Y_max); the
  symmetric strip likewise. So TRX <= max(sup of Psi over [0, Y_cut]^2, the two strip bounds on [Y_max, Y_cut] x [0, Y_cut]).
Every sup is taken by branch and bound in arb on boxes, using that the first factors are nondecreasing in y (evaluated at the box's upper
end) and g is convex (its box maximum is at an end). The returned values are arb upper ends; lower ends of the sup (box midpoints) are
returned for information. Inputs: N, t (fmpq or arb ball), the c enclosures (arb balls or fmpq). No float enters a bound.
Checks of MU-1 against arb Bessel values, C-PROTO against pk24's g6_hwn1_v1 and g6_cj_v1_1 outputs, and the plants are in the check job
pk25/mu/kt_mu_hw_check_v1.py."""
from flint import arb, fmpq, ctx

PREC = 128


def setup():
    ctx.prec = PREC


def A_(x):
    """an arb from an arb, fmpq, int or decimal string (exact or enclosing)."""
    if isinstance(x, arb):
        return x
    if isinstance(x, (fmpq, int)):
        return arb(x)
    if isinstance(x, str):
        return arb(x)
    raise TypeError('kt_mu_hw_v1 takes arb, fmpq, int or str, not %s' % type(x).__name__)


class Consts:
    def __init__(self, N):
        if N not in (3, 4):
            raise ValueError('N must be 3 or 4')
        self.N = N
        self.A = arb(fmpq(N - 1, 2))
        self.nu2 = arb(fmpq((N - 2) ** 2, 4))
        self.cN = arb(2) + arb(fmpq((N - 1) * (N - 3), 8))


def gexp(y, t, K):
    """g(y) = -y/2 + E(y, t)/2, E(y, t) = t y^2/6 + t^2 nu^2 y/6 (Lemma MU-1 (b))."""
    return -y / 2 + (t * y * y + t * t * K.nu2 * y) / 12


def y_cut(t, Ymax, K):
    """Y_cut = Y_max + t ((2 Y_max/t + nu^2)^{1/2} + 1/2) (Lemma MU-3)."""
    return Ymax + t * ((2 * Ymax / t + K.nu2).sqrt() + arb(1) / 2)


def certainly_le(a, b):
    return bool(a <= b)


def tail_ok(t, Ymax, Kc, M0):
    """Lemma MU-3's hypotheses: 0 < t <= 1/299 certainly, Y_max + K >= 3 and >= M0 certainly, and (v1_1) K >= -3/2 certainly."""
    return bool(t <= arb(fmpq(1, 299))) and bool(t > 0) and bool(Ymax + Kc >= 3) and bool(Ymax + Kc >= M0) and bool(Kc >= arb(-3) / 2)


def _bb1(f_box, f_pt, lo, hi, n0, tol, maxbox):
    """branch and bound for sup over [lo, hi] of a function with box upper bounds f_box(a, b) and point values f_pt(y) (arb balls):
    returns (upper end ball, lower end ball, boxes evaluated)."""
    boxes = [(lo + (hi - lo) * k / n0, lo + (hi - lo) * (k + 1) / n0) for k in range(n0)]
    best = None
    for a, b in boxes:
        v = f_pt((a + b) / 2)
        best = v if best is None else best.max(v)
    best_lo = best.lower()
    done, nbox = None, 0
    while boxes:
        nxt = []
        for a, b in boxes:
            nbox += 1
            if nbox > maxbox:
                raise RuntimeError('branch and bound exceeded %d boxes' % maxbox)
            u = f_box(a, b).upper()
            if bool(u < best_lo):
                continue
            m = (a + b) / 2
            best_lo = best_lo.max(f_pt(m).lower())
            if bool(u - best_lo < tol) or bool(b - a < arb(fmpq(1, 10 ** 12))):
                done = u if done is None else done.max(u)
                continue
            nxt += [(a, m), (m, b)]
        boxes = nxt
    return done.upper(), best_lo, nbox


def one_row(N, t, c_lo, c_hi, Ymax=20, tol=fmpq(1, 10 ** 6), maxbox=200000):
    """OR's upper end on every J with 1/J <= t: (upper, lower end of sup Phi, info dict). Raises ValueError if MU-3's hypotheses fail."""
    K = Consts(N)
    t, c_lo, c_hi, Ymax = A_(t), A_(c_lo), A_(c_hi), A_(Ymax)
    if bool(c_lo > c_hi):   # balls are allowed: only a certain inversion is refused
        raise ValueError('c_lo above c_hi')
    if not bool(c_hi >= 0):   # v1_1: MU-3's hypothesis c_hi >= 0 (it gives K >= -3/2)
        raise ValueError('MU-3 needs c_hi >= 0 certainly (c_hi %s)' % c_hi)
    M0 = (K.A - c_lo).abs_upper().max((K.A - c_hi).abs_upper())
    Kc = (K.cN * t - (K.A - c_hi)).upper()
    if not tail_ok(t, Ymax, (K.cN * t - (K.A - c_hi)).lower(), M0):
        raise ValueError('MU-3 hypotheses fail (t %s, Y_max %s, K %s, M0 %s)' % (t, Ymax, Kc, M0))
    Yc = y_cut(t, Ymax, K).upper()

    def f_box(a, b):
        return M0.max(b + Kc) * gexp(a, t, K).max(gexp(b, t, K)).exp()

    def f_pt(y):
        return M0.max(y + Kc) * gexp(y, t, K).exp()
    up, lo, nb = _bb1(f_box, f_pt, arb(0), Yc, 64, A_(tol), maxbox)
    return up, lo, {'Y_cut': Yc, 'M0': M0, 'K': Kc, 'boxes': nb}


def _vertex_max(m1lo, m2lo, A, ct, ch, form):
    """largest |P| over the vertices m_i in {m_ilo, A}, c_t in {ct_lo, ct_hi}, c_h in {ch_lo, ch_hi}; P = m1 m2 - c_t m2 - c_h m1 (xi)
    or (m1 - c_t)(m2 - c_h) (prod)."""
    best = None
    for m1 in (m1lo, A):
        for m2 in (m2lo, A):
            for c1 in ct:
                for c2 in ch:
                    p = (m1 * m2 - c1 * m2 - c2 * m1) if form == 'xi' else ((m1 - c1) * (m2 - c2))
                    v = p.abs_upper()
                    best = v if best is None else best.max(v)
    return best


def two_row_xi(N, t, ct_lo, ct_hi, ch_lo, ch_hi, Ymax=20, tol=fmpq(1, 10 ** 6), n0=24, maxbox=400000):
    """TRX's upper end on every J with 1/J <= t: (upper, lower end of sup Psi, info). Branch and bound on [0, Y_cut]^2 plus the two strips."""
    K = Consts(N)
    t, Ymax = A_(t), A_(Ymax)
    ct = (A_(ct_lo), A_(ct_hi))
    ch = (A_(ch_lo), A_(ch_hi))
    if bool(ct[0] > ct[1]) or bool(ch[0] > ch[1]):   # balls are allowed: only a certain inversion is refused
        raise ValueError('c_lo above c_hi')
    M0t = (K.A - ct[0]).abs_upper().max((K.A - ct[1]).abs_upper())
    M0h = (K.A - ch[0]).abs_upper().max((K.A - ch[1]).abs_upper())
    Kt = (K.cN * t - (K.A - ct[1])).upper()
    Kh = (K.cN * t - (K.A - ch[1])).upper()
    Kmin = (K.cN * t - (K.A - ct[1])).lower().min((K.cN * t - (K.A - ch[1])).lower())
    if not (tail_ok(t, Ymax, Kmin, M0t.max(M0h)) and bool(Ymax - Kt.abs_upper().max(Kh.abs_upper()).max(K.A) >= 3)):
        raise ValueError('MU-3 hypotheses fail for the two-row bound')
    Yc = y_cut(t, Ymax, K).upper()
    ctab = ct[0].abs_upper().max(ct[1].abs_upper())
    chab = ch[0].abs_upper().max(ch[1].abs_upper())

    def gmax(a, b):
        return gexp(a, t, K).max(gexp(b, t, K))

    def psi_box(b1, b2):
        a1, e1, a2, e2 = b1[0], b1[1], b2[0], b2[1]
        V = _vertex_max(K.A - K.cN * t - e1, K.A - K.cN * t - e2, K.A, ct, ch, 'xi')
        return V * (gmax(a1, e1) + gmax(a2, e2)).exp()

    def psi_pt(y1, y2):
        V = _vertex_max(K.A - K.cN * t - y1, K.A - K.cN * t - y2, K.A, ct, ch, 'xi')
        return V * (gexp(y1, t, K) + gexp(y2, t, K)).exp()
    # 2-D branch and bound
    h = Yc / n0
    boxes = [((h * i, h * (i + 1)), (h * j, h * (j + 1))) for i in range(n0) for j in range(n0)]
    best_lo = None
    for b1, b2 in boxes:
        v = psi_pt((b1[0] + b1[1]) / 2, (b2[0] + b2[1]) / 2).lower()
        best_lo = v if best_lo is None else best_lo.max(v)
    done, nbox, tl = None, 0, A_(tol)
    while boxes:
        nxt = []
        for b1, b2 in boxes:
            nbox += 1
            if nbox > maxbox:
                raise RuntimeError('branch and bound exceeded %d boxes' % maxbox)
            u = psi_box(b1, b2).upper()
            if bool(u < best_lo):
                continue
            m1, m2 = (b1[0] + b1[1]) / 2, (b2[0] + b2[1]) / 2
            best_lo = best_lo.max(psi_pt(m1, m2).lower())
            if bool(u - best_lo < tl) or bool(b1[1] - b1[0] < arb(fmpq(1, 10 ** 9))):
                done = u if done is None else done.max(u)
                continue
            nxt += [((b1[0], m1), (b2[0], m2)), ((b1[0], m1), (m2, b2[1])), ((m1, b1[1]), (b2[0], m2)), ((m1, b1[1]), (m2, b2[1]))]
        boxes = nxt
    # the strips (Lemma MU-3 for TRX): y1 in [Y_max, Y_cut], y2 in [0, Y_cut] with the alpha-beta form, and the symmetric strip
    strip = None
    ns = 400
    hs = Yc / ns
    g1 = gmax(Ymax, Yc)
    for j in range(ns):
        a2, e2 = hs * j, hs * (j + 1)
        fh = M0h.max(e2 + Kh)
        m2ab = K.A.max(e2 + K.cN * t - K.A)
        ft = M0t.max(e2 + Kt)
        for v in ((fh * (Yc + K.A + K.cN * t) + ctab * m2ab) * (g1 + gmax(a2, e2)).exp(),
                  (ft * (Yc + K.A + K.cN * t) + chab * m2ab) * (g1 + gmax(a2, e2)).exp()):
            strip = v.upper() if strip is None else strip.max(v.upper())
    up = done.max(strip).upper()
    return up, best_lo, {'Y_cut': Yc, 'boxes': nbox, 'strip': strip, 'core': done}


def two_row_prod(N, t, ct_lo, ct_hi, ch_lo, ch_hi, **kw):
    """TRP = OR(c_t) OR(c_h): (upper, lower, info)."""
    ut, lt, it = one_row(N, t, ct_lo, ct_hi, **kw)
    uh, lh, ih = one_row(N, t, ch_lo, ch_hi, **kw)
    return (ut * uh).upper(), lt * lh, {'t': (ut, it), 'h': (uh, ih)}


def bessel_parts(N, J, L):
    """arb values of a_l and m(l) for l = 0..L at J (an arb), from scaled I (the scale cancels in the ratios): (a list, m list, r list)."""
    nu = arb(fmpq(N - 2, 2))
    I = [J.bessel_i(nu + k, scaled=True) for k in range(L + 2)]
    r = [I[k + 1] / I[k] for k in range(L + 1)]
    a = [I[k] / I[0] for k in range(L + 1)]
    m = [J * (1 - r[k]) - k for k in range(L + 1)]
    return a, m, r
