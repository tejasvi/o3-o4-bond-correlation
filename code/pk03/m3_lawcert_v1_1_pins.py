"""m3_lawcert_v1_1_pins.py -- pk03 (code/pk03/). The source texts that m3_lawcert_v1_1's C-LAW-SHAPE and C-LAW-REM allow-list pin,
copied byte for byte by tmp/r16/build_lawcert_pins_v1_1.awk from the files m3_run_v1_8's manifest (5b5b7861) pins: m3_bar_v10.py
(b80f4e3b), m3_scal_v2.py (f9ebafef), m3_run_v1_8.py (7d72fc7f) and m3_record_v4.py (b2671d5a); each entry names its file and
line range. A reviewer reads the reviewed formulas here; m3_lawcert_v1_1 compares each, as an AST, with the statement or function
in the named place of the pinned file. No code."""
PINS = {}
# m3_bar_v10.py lines 199-225
PINS['bar:sup_F'] = r'''
def sup_F(factors, J):
    """riglap2.sup_F and riglap3.sup_F3 with every coefficient in absolute value; also the J-degree m_F of Lemma U."""
    J, t = S.I(J), 1 / S.I(J)
    s, mF = iv.mpf(1), 0
    for f in factors:
        if f[0] == 'const':
            s = s * abs(S.I(f[1]))
        elif f[0] == 'p':
            _, col, q1, q2, q3 = f
            val, mx = iv.mpf(1), 0
            for i, coef in ((1, q1), (2, q2), (3, q3)):
                for cb, mono in zip(coef, BASIS9):
                    val = val + S.ipow(t, i) * S.I(abs(cb)) * S.ipow(2 * J, len(mono))
                    if cb != 0.0:
                        mx = max(mx, len(mono) - i)
            s, mF = s * val, mF + mx
        elif f[0] == 'xi':
            _, col, c0, c9 = f
            val, mx = S.I(abs(c0)), 0
            for cb, mono in zip(c9, BASIS9):
                val = val + S.I(abs(cb)) * S.ipow(2 * J, len(mono))
                if cb != 0.0:
                    mx = max(mx, len(mono))
            s, mF = s * val, mF + mx
        else:
            raise ValueError('factor kind %r is not supported' % (f[0],))
    return S.finite(s), mF
'''
# m3_bar_v10.py lines 237-237
PINS['bar:Prep.UK'] = r'''
    UK = ('nE', 'nE4', 'rE_parts', 'rE')
'''
# m3_bar_v10.py lines 238-238
PINS['bar:Prep.CK'] = r'''
    CK = ('nC8', 'nC6', 'Pout', 'Pout_p', 'farbase', 'alpha_lo')
'''
# m3_bar_v10.py lines 242-242
PINS['bar:Prep.__init__:t'] = r'''
        self.t = 1 / S.I(J)
'''
# m3_bar_v10.py lines 249-249
PINS['bar:Prep.__init__:tloc'] = r'''
        t = self.t
'''
# m3_bar_v10.py lines 250-250
PINS['bar:Prep.__init__:rates'] = r'''
        self.rates = [S.up(-iv.log(1 - S.I(a)) / (2 * S.I(a)) * t) for a in self.a_v]
'''
# m3_bar_v10.py lines 251-251
PINS['bar:Prep.__init__:ratesp'] = r'''
        self.ratesp = [S.up(-iv.log(1 - S.I(ap)) / (2 * S.I(ap)) * t)] * V
'''
# m3_bar_v10.py lines 252-252
PINS['bar:Prep.__init__:tilt_c'] = r'''
        self.tilt_c = g.tilted(self.rates)
'''
# m3_bar_v10.py lines 253-253
PINS['bar:Prep.__init__:tilt_p'] = r'''
        self.tilt_p = g.tilted(self.ratesp)
'''
# m3_bar_v10.py lines 264-266
PINS['bar:Prep.__init__:restore'] = r'''
        if scalars:
            for k, v in scalars.items():
                setattr(self, k, v)
'''
# m3_bar_v10.py lines 283-283
PINS['bar:Prep.stage_u:N2'] = r'''
        N2 = lambda P, lab: self.norm_any(P, 'u', 2, lab)
'''
# m3_bar_v10.py lines 300-300
PINS['bar:Prep.stage_u:nE'] = r'''
        self.nE = [iv.mpf(1)] + [N2(self.Ej[j], 'nE%d' % j) for j in (1, 2, 3)]
'''
# m3_bar_v10.py lines 301-306
PINS['bar:Prep.stage_u:nE4'] = r'''
        self.nE4 = [iv.mpf(1)]
        for j in (1, 2, 3):
            if 4 * deg(self.Ej[j]) <= self.dmaxH:
                self.nE4.append(self.norm_any(self.Ej[j], 'u', 4, 'nE4_%d' % j))
            else:
                self.nE4.append(S.ipow(iv.mpf(3), deg(self.Ej[j])) * self.nE[j])
'''
# m3_bar_v10.py lines 311-311
PINS['bar:Prep.stage_c:nh2_6'] = r'''
        nh2_6 = self.norm_any(h2, 'c', 6, 'h2 p6')                # degree 18 first
'''
# m3_bar_v10.py lines 314-314
PINS['bar:Prep.stage_c:n_'] = r'''
        n_ = g.n
'''
# m3_bar_v10.py lines 315-315
PINS['bar:Prep.stage_c:Pout'] = r'''
        self.Pout = S.isum(S.chi_tail_up(self.J * S.I(a) / gv, n_) for a, gv in zip(self.a_v, g.Gvv))
'''
# m3_bar_v10.py lines 316-316
PINS['bar:Prep.stage_c:Pout_p'] = r'''
        self.Pout_p = S.isum(S.chi_tail_up(self.J * S.I(a) / gv, n_) for a, gv in zip(self.a_v, self.tilt_p['Gvv']))
'''
# m3_bar_v10.py lines 318-318
PINS['bar:Prep.stage_c:farbase'] = r'''
        self.farbase = S.far_base(self.J, S.I(self.theta0), S.I(self.ap), g.Gvv, self.tree, g.N, g.V, g.log_tau)
'''
# m3_bar_v10.py lines 319-319
PINS['bar:Prep.stage_c:alpha_lo'] = r'''
        self.alpha_lo = min((S.I(self.theta0) * S.I(self.ap) / (2 * gv)).a for gv in g.Gvv)
'''
# m3_bar_v10.py lines 400-406
PINS['bar:Prep.norm_any'] = r'''
    def norm_any(self, P, which, p, label=None):
        t0 = time.process_time()
        v = self.lp_norm(P, which, p, self.dmaxH, prep=True)
        v = v if v is not None else self.holder_mono(P, which, p)
        if label:
            self.log('NORM %s %s p %d: %.2f s' % (which, label, p, time.process_time() - t0))
        return v
'''
# m3_bar_v10.py lines 513-513
PINS['bar:Prep.bound:nF0'] = r'''
        nF0 = S.sqrt_nn(m0u)
'''
# m3_bar_v10.py lines 514-514
PINS['bar:Prep.bound:nF0c'] = r'''
        nF0c = S.sqrt_nn(m0c)
'''
# m3_bar_v10.py lines 518-523
PINS['bar:Prep.bound:gn'] = r'''
        def gn(gi, what, i, p, which):
            key = 'g|%d|%s|%d|%d|%s' % (gi, what, i, p, which)
            d = gds[gi]
            if (what, i, p, which) in d['norm']:
                return self.ustate['vals'].setdefault(key, d['norm'][(what, i, p, which)])
            return self._unit(key, lambda: self.gnorm(d, what, i, p, which))
'''
# m3_bar_v10.py lines 525-527
PINS['bar:Prep.bound:fnorm'] = r'''
        def fnorm(i, which, p=2):
            return abs(S.I(scal)) * S.isum(math.prod((gn(gi, 'ser', ig, p * G_, which) for gi, ig in enumerate(c)),
                                                     start=iv.mpf(1)) for c in comps(i, len(groups)))
'''
# m3_bar_v10.py lines 529-529
PINS['bar:Prep.bound:nF'] = r'''
        nF = [nF0] + [fnorm(i, 'u') for i in (1, 2, 3)]
'''
# m3_bar_v10.py lines 530-530
PINS['bar:Prep.bound:nFc'] = r'''
        nFc = [nF0c] + [fnorm(i, 'c') for i in (1, 2, 3)]
'''
# m3_bar_v10.py lines 533-533
PINS['bar:Prep.bound:three'] = r'''
        three = iv.mpf(3)
'''
# m3_bar_v10.py lines 535-539
PINS['bar:Prep.bound:EF4'] = r'''
        EF4 = iv.mpf(0)
        for c in comps(4, len(groups)):
            EF4 = EF4 + S.I(Fraction(24, math.prod(math.factorial(x) for x in c))) * math.prod(
                (gn(gi, 'bar', jg, G_, 'c') for gi, jg in enumerate(c)), start=iv.mpf(1))
        EF4 = abs(S.I(scal)) * EF4
'''
# m3_bar_v10.py lines 541-541
PINS['bar:Prep.bound:Nc'] = r'''
        Nc = self.tilt_c['N']
'''
# m3_bar_v10.py lines 546-546
PINS['bar:Prep.bound:hc'] = r'''
        hc = lambda i: S.ipow(three, deg(Fi[i])) * nF[i] if not is_zero(Fi[i]) else iv.mpf(0)
'''
# m3_bar_v10.py lines 547-548
PINS['bar:Prep.bound:l2'] = r'''
        l2 = nF0 + S.isum(T(k) * S.isum((hc(i) if i > 0 else S.ipow(three, deg(Fi[0])) * nF0) * self.nE4[k - i] for i in range(k + 1))
                          for k in range(1, 4))
'''
# m3_bar_v10.py lines 549-549
PINS['bar:Prep.bound:B_tail'] = r'''
        B_tail = l2 * S.sqrt_nn(self.Pout)
'''
# m3_bar_v10.py lines 550-550
PINS['bar:Prep.bound:nF0p'] = r'''
        nF0p = abs(S.I(scal)) * math.prod((gn(gi, 'barp', 0, 2 * G_, 'p') for gi in range(len(gds))), start=iv.mpf(1))
'''
# m3_bar_v10.py lines 551-551
PINS['bar:Prep.bound:B_ann'] = r'''
        B_ann = self.tilt_p['N'] * nF0p * S.sqrt_nn(self.Pout_p)
'''
# m3_bar_v10.py lines 552-552
PINS['bar:Prep.bound:supF'] = r'''
        supF, mF = sup_F(factors, J)
'''
# m3_bar_v10.py lines 553-553
PINS['bar:Prep.bound:B_far'] = r'''
        B_far = supF * self.farbase
'''
# m3_bar_v10.py lines 557-557
PINS['bar:Prep.bound:return'] = r'''
        return ak, {'rem': B_rem, 'tail': B_tail, 'ann': B_ann, 'far': B_far}, info
'''
# m3_scal_v2.py lines 123-136
PINS['scal:chi_tail_up'] = r'''
def chi_tail_up(s, n):
    """[0, U] with U >= P(chi^2_n > s), n = 2 or 3 (riglap2.chi_tail): exp(-s/2) for n = 2; for n = 3, erfc(x) + sqrt(2s/pi) exp(-s/2)
    with x = sqrt(s/2) > 0 asserted and erfc(x) <= exp(-x^2)/(x sqrt pi)."""
    s = I(s)
    if n == 2:
        u = iv.exp(-s / 2)
    elif n == 3:
        x = iv.sqrt(s / 2)
        if not x.a > 0:
            raise ValueError('chi_tail: s/2 not certainly > 0: %r' % (s,))
        u = iv.exp(-(x * x)) / (x * iv.sqrt(iv.pi)) + iv.sqrt(2 * s / iv.pi) * iv.exp(-s / 2)
    else:
        raise ValueError('n = %r' % n)
    return finite(iv.mpf([iv.mpf(0), finite(u).b]))
'''
# m3_scal_v2.py lines 139-163
PINS['scal:ive1'] = r'''
def ive1(x):
    """I_1(x) e^-x for x > 0 (x an interval; x <= 0 raises): the positive series sum_k t_k, t_k = (x/2)^(2k+1)/(k! (k+1)!), summed until
    the step ratio r_k = (x/2)^2/((k+1)(k+2)) at the upper end of x is below 1/2 AND the next term is below 1e-35 of the sum. The ratios
    decrease in k, so the omitted tail sum_{j>k} t_j <= t_k r_k/(1 - r_k) (r_k taken at the first omitted index), then times e^-x."""
    x = I(x)
    if not x.a > 0:
        raise ValueError('ive1 needs x > 0: %r' % (x,))
    h = x / 2
    h2 = h * h
    hb2 = h.b * h.b
    term = h
    acc = iv.mpf(0)
    k = 0
    while True:
        acc = acc + term
        r = hb2 / ((k + 1) * (k + 2))
        nxt = term * h2 / ((k + 1) * (k + 2))
        if r.b < iv.mpf(0.5) and nxt.b < acc.a * iv.mpf(1e-35):
            break
        term = nxt
        k += 1
        if k > 200000:
            raise ArithmeticError('ive1 series did not settle')
    tail = iv.mpf([iv.mpf(0), (term * r / (1 - r)).b])
    return finite((acc + tail) * iv.exp(-x))
'''
# m3_scal_v2.py lines 166-178
PINS['scal:logtree'] = r'''
def logtree(Jp, tree, N):
    """log of the tree bound for Z (riglap2.bound's logtree): N = 4: sum log(2 ive1(Jp c)/(Jp c)); N = 3: sum log((1 - e^(-2 Jp c))/(2 Jp c))."""
    Jp = I(Jp)
    out = iv.mpf(0)
    for c in tree:
        x = Jp * I(c)
        if N == 4:
            out = out + iv.log(2 * ive1(x) / x)
        elif N == 3:
            out = out + iv.log((1 - iv.exp(-2 * x)) / (2 * x))
        else:
            raise ValueError('N = %r' % N)
    return finite(out)
'''
# m3_scal_v2.py lines 181-187
PINS['scal:logmain'] = r'''
def logmain(J, V, N, log_tau):
    """riglap2.Graph.logmain: -(V-1) log(area) + (n/2)(V-1) log(2 pi/J) - (n/2) log tau, tau = det(Lsub)/V = det of the reduced Laplacian
    (matrix-tree), area = 2 pi^2 (N = 4) or 4 pi (N = 3), n = N - 1."""
    n = N - 1
    area = 2 * iv.pi * iv.pi if N == 4 else 4 * iv.pi
    J = I(J)
    return finite(-(V - 1) * iv.log(area) + iv.mpf(n) / 2 * (V - 1) * iv.log(2 * iv.pi / J) - iv.mpf(n) / 2 * I(log_tau))
'''
# m3_scal_v2.py lines 190-195
PINS['scal:far_base'] = r'''
def far_base(J, theta, ap, Gdiag, tree, N, V, log_tau):
    """exp of the far exponent at one theta (riglap2.bound l.374-376, riglap5b.Prep5): sum_v exp(-theta J ap/(2 G_vv)) times the tree bound at
    (1 - theta) J over main(J). Any theta in (0, 1) gives a valid bound."""
    J, th, ap = I(J), I(theta), I(ap)
    s = isum(iv.exp(-th * J * ap / (2 * I(g))) for g in Gdiag)
    return finite(iv.exp(iv.log(s) + logtree((1 - th) * J, tree, N) - logmain(J, V, N, log_tau)))
'''
# m3_run_v1_8.py lines 433-440
PINS['run:laws_of'] = r'''
def laws_of(pr, mF):
    """U3's laws (PLAN_M3_CODE_v1_2 sect. C) and Lemma U's far rate (lower end) for an entry with J-degree m_F."""
    g = pr.g
    cF = mF + Fraction(g.n * (g.V - 1), 2)
    rate = pr.alpha_lo - S.I(cF) / 300
    return {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, g.Gvv)]},
            'ann': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, pr.tilt_p['Gvv'])]},
            'far_rate': S.down(rate), 'far_cF': str(cF)}, rate
'''
# m3_run_v1_8.py lines 459-463
PINS['run:compute_entry:laws'] = r'''
    ak, bars, info = pr.bound(facs, e.get('grouping', 'std'), entry=name, state=state)
    laws, rate = laws_of(pr, info['mF'])
    gate('C-MONO-FAR', rate.a > 0, '%s: far rate alpha_min - (m_F + n(V-1)/2)/J_REF = %.4e > 0 (m_F %d)' % (name, S.down(rate), info['mF']))
    a0 = 1 if all(f[0] == 'p' for f in facs) else None
    rec = REC.entry_record(ak, bars, T_REF, 'free', a0_exact=a0, laws=laws)
'''
# m3_record_v4.py lines 37-59
PINS['rec:entry_record'] = r'''
def entry_record(ak_iv, bars, t_ref, parity='free', a0_exact=None, laws=None, alias_of=None):
    """one 'entry' item; bars: {rem, tail, ann, far} as intervals with valid upper ends."""
    if parity == 'zero':
        z = {'rem': 0.0, 'tail': 0.0, 'ann': 0.0, 'far': 0.0}
        return {'kind': 'entry', 'ak': [0.0] * 4, 'ak_rad': [0.0] * 4, 'B': dict(z, rnd=0.0), 'Bp': z, 'err': 0.0, 'parity': 'zero',
                'alias_of': alias_of, 'a0_exact': '0', 'laws': laws, 'value_ref': 0.0}
    ak = [mid_float(x) for x in ak_iv]
    rad = [rad_around(x, f) for x, f in zip(ak_iv, ak)]
    if a0_exact is not None:
        c = Fraction(a0_exact)
        if not (ak_iv[0].a <= S.I(c) <= ak_iv[0].b):
            raise ArithmeticError('a0_exact %s is outside the computed a_0 enclosure %r' % (a0_exact, ak_iv[0]))
        ak[0], rad[0] = float(c), 0.0
        if Fraction(ak[0]) != c:
            raise ValueError('a0_exact must be a binary64 value')
    t = S.I(t_ref)
    rnd = S.up(S.isum(S.I(r) * S.ipow(t, k) for k, r in enumerate(rad)))
    Bp = {p: S.up(S.nonneg(bars[p])) for p in ('rem', 'tail', 'ann', 'far')}
    B = dict(Bp, rnd=rnd)
    err = S.up(S.isum(S.I(v) for v in B.values()))
    vref = S.isum(S.I(a) * S.ipow(t, k) for k, a in enumerate(ak))
    return {'kind': 'entry', 'ak': ak, 'ak_rad': rad, 'B': B, 'Bp': Bp, 'err': err, 'parity': 'free', 'alias_of': alias_of,
            'a0_exact': None if a0_exact is None else str(Fraction(a0_exact)), 'laws': laws, 'value_ref': mid_float(vref)}
'''
