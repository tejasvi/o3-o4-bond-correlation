

# ====================================================================================== pk24's part (nu/src/nu_main_v1_2.py)
CORE_FUNCS = ('up_float', 'nsqrt', 'lap_a', 'gauge_basis_a', 'surely_pd', 'tilted_cov_a', 'sub_mat', 'ser', 'zero', 'one', 'anh', 'xi_pair',
              'xis', 'mono_series', 'shift', 'vac_poly', 'state_poly', 'restrict6')
CORE_STMTS = ('SQ5, SQ21', 'A_', 'B_', 'TRI', 'PAIRS', 'BASIS', 'RHO_M, RHO_E', 'KX, NVX', 'XS, QS, XD, QD',
              'Series, padd, pscale, pmul, pconst, pvar', 'WX', 'a_m, a_e', 'c_m, c_e', 'ED_', 'LD', 'BD')
FAILS, UNFIRED = [], []


def segments(path):
    """module-level function sources and assignment statements by name (ast source segments, exact text)."""
    src = open(path, encoding='utf-8').read()
    tree = ast.parse(src)
    funcs, stmts = {}, {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            funcs.setdefault(node.name, []).append(ast.get_source_segment(src, node))
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            stmts.setdefault(ast.get_source_segment(src, node.targets[0]), []).append(ast.get_source_segment(src, node))
    return funcs, stmts


def c_core():
    fa, sa = segments(os.path.join(W18, KT))
    fb, sb = segments(os.path.abspath(__file__))
    bad = [n for n in CORE_FUNCS if not (len(fa.get(n, [])) == 1 and fb.get(n, []) == fa[n])]
    bad += [n for n in CORE_STMTS if not (len(sa.get(n, [])) == 1 and sb.get(n, []) == sa[n])]
    out('C-CORE %s: %d functions and %d statements of kt_cert_v1_9 (sha8 %s) copied verbatim (ast source segments, each defined once)%s' % (
        'PASS' if not bad else 'FAIL', len(CORE_FUNCS), len(CORE_STMTS), SHAS[KT][:8], (': differ ' + ', '.join(bad)) if bad else ''))
    if bad:
        FAILS.append('C-CORE')


TS = {4: ('pk11/out/ts_N4_J170_D_S_z9sym_v1.json', 'pk11/out/vacres_K3_N4_sym_v1.json'),
      3: ('pk11/out/ts_N3_S_z9sym_v1.json', 'pk11/out/vacres_K3_N3_sym_v1.json')}
STATES = (('psi', 0, 'vac'), ('e1', 0, 1), ('e2', 0, 2), ('e3', 0, 3))   # (name, TS index of S, b); v1_2 (2): engine A's basis states only
J_LO_CHECK = 300                                                         # v1_2 (3): the bound covers every t in (0, 1/J_LO_CHECK] = (0, T1]


def c_tri():
    """v1_2 (1), the |E0 - 1| <= t ebar needs TRI_p >= 0; every TRI_p must be certainly > 0."""
    ok = all(bool(c > 0) for c in TRI)
    out('C-TRI %s: TRI = (A, A, B) = %s, each certainly > 0 (so E0 = exp(-t sum_p TRI_p Delta_p) is in (0, 1] and |E0 - 1| <= t ebar)' % (
        'PASS' if ok else 'FAIL', ', '.join(c.str(15) for c in TRI)))
    if not ok:
        FAILS.append('C-TRI')


def trial_set_line():
    """v1_2 (3): MR_LEMMAP v3's TRIAL_SET line, verbatim (the reader compares it across records)."""
    hits = [ln for ln in open(os.path.join(W18, 'pk25/mr/v3/MR_LEMMAP.kv'), encoding='utf-8').read().splitlines() if ln.startswith('TRIAL_SET = ')]
    assert len(hits) == 1, len(hits)
    assert ':' + SHAS[TS[4][0]] in hits[0] and ':' + SHAS[TS[3][0]] in hits[0], 'TRIAL_SET does not name the trial files read here'
    return hits[0]


def setup(N, ts_idx):
    """engine A's per-item globals (nn, Smat, QV), as kt_cert_v1_9 reads them from its trial files."""
    global nn, Smat, QV
    nn = N - 1
    Smat = np.array(json.load(open(os.path.join(W18, TS[N][ts_idx])))['S'])
    R3 = json.load(open(os.path.join(W18, TS[N][1])))
    QV = [None, R3['q1'], R3['q2'], R3['q3']]


def coefs(b):
    """[(c_k const, [c_k,i over BASIS]) for k = 0..]: pS_g(xi; t) = sum_k t^k (c_k + sum_i c_k,i mu_i(xi)) (vac_poly, state_poly)."""
    if b == 'vac':
        return [(arb(1), [arb(0)] * 9)] + [(arb(0), [arb(float(x)) for x in QV[k]]) for k in (1, 2, 3)]
    return [(arb(float(Smat[0, b])), [arb(float(x)) for x in Smat[1:, b]])]


NV = 6
T1 = arb(1) / 300
A_BIG = max(a_m, a_e)
WBAR = 1 / (4 * (1 - arb(A_BIG)))
PX = [pvar(XS[r], NV) for r in range(3)]
PQ = [pvar(QS[p], NV) for p in range(3)]
DP = [pmul(padd(PX[r], pscale(PX[s], -1)), padd(PX[r], pscale(PX[s], -1))) for (r, s) in PAIRS]
DBAR = [pscale(d, WBAR / 2) for d in DP]
XIBAR = [padd(pscale(PQ[p], arb(1) / 2), pscale(DBAR[p], T1)) for p in range(3)]
EBAR = padd(*[pscale(DBAR[p], TRI[p]) for p in range(3)])


def mu_poly(i, xs):
    res = pconst(1, NV)
    for p in BASIS[i]:
        res = pmul(res, xs[p])
    return res


def dmu_bar(i):
    """0 <= mu_i(xi) - mu_i(Q/2) <= t dmu_bar_i: Dbar_p (degree 1); Dbar_p xibar_q + Dbar_q Q_p/2 (degree 2)."""
    m = BASIS[i]
    if len(m) == 1:
        return DBAR[m[0]]
    p, q = m
    return padd(pmul(DBAR[p], XIBAR[q]), pmul(DBAR[q], pscale(PQ[p], arb(1) / 2)))


def majorant(cf):
    """M_g = ebar Pbar_g + Dbar'_g (NU_G_NOTE_v1 sect. 4)."""
    def absterm(c0, cs):
        return padd(pconst(abs(c0), NV), *[pscale(mu_poly(i, XIBAR), abs(c)) for i, c in enumerate(cs) if not c.is_zero()])
    Pbar = padd(*[pscale(absterm(c0, cs), T1 ** k) for k, (c0, cs) in enumerate(cf)])
    Dp = padd(*[pscale(dmu_bar(i), abs(c)) for i, c in enumerate(cf[0][1]) if not c.is_zero()],
              *[pscale(absterm(c0, cs), T1 ** (k - 1)) for k, (c0, cs) in enumerate(cf) if k >= 1])
    return padd(pmul(EBAR, Pbar), Dp)


def pval(P, v):
    tot = arb(0)
    for e, c in P.items():
        term = c
        for i, k in enumerate(e):
            if k:
                term = term * v[i] ** k
        tot += term
    return tot


def mu_val(i, xv):
    res = arb(1)
    for p in BASIS[i]:
        res = res * xv[p]
    return res


def pS_val(cf, xv, t):
    tot = arb(0)
    for k, (c0, cs) in enumerate(cf):
        term = c0 + sum((c * mu_val(i, xv) for i, c in enumerate(cs) if not c.is_zero()), arb(0))
        tot += term if k == 0 else t ** k * term
    return tot


def closed(cf, X, Q, t, with_e0=True):
    """B_g(t) = E0 pS_g(xi; t) in closed form at a chart point (NU_G_NOTE_v1 sect. 2), and b0_g = pS_g(Q/2; 0)."""
    s = [(1 - t * X[v]).sqrt() for v in range(3)]
    Dl = [(X[r] - X[q]) ** 2 / (2 * (s[r] + s[q]) ** 2) for (r, q) in PAIRS]
    xi = [Q[p] / 2 + t * Dl[p] for p in range(3)]
    E0 = (-t * sum((TRI[p] * Dl[p] for p in range(3)), arb(0))).exp()
    B = (E0 if with_e0 else arb(1)) * pS_val(cf, xi, t)
    return B, pS_val(cf, [Q[p] / 2 for p in range(3)], arb(0))


def bas_series(b):
    """engine A's basis series: explicit_part's xiS, pS, H0, E0 and bas = restrict6(E0 * pS[g]) (kt_cert_v1_9), and restrict6(pS) for PLANT-ID."""
    xiS = xis(XS, QS)
    pS = vac_poly(xiS) if b == 'vac' else state_poly(xiS, b)
    H0 = zero()
    for p, (r, s) in enumerate(PAIRS):
        H0 = H0 + anh(XS[r], XS[s], TRI[p])
    E0 = H0.exp()
    return restrict6(E0 * pS), restrict6(pS)


def sval(sr, v, t):
    return sum((pval(P, v) * (t ** k if k else 1) for k, P in enumerate(sr)), arb(0))


def point(rng, scale, N, tX_max=None):
    """a chart point (X_0..2, Q_01, Q_12, Q_02) from three vectors in R^(N-1): Gaussian times scale, or (tX_max given) on random directions at
    X_v = f tX_max, f uniform in [0.8, 1]; exact balls of the binary64 coordinates."""
    if tX_max is None:
        ph = [[arb(float(x)) for x in rng.standard_normal(N - 1) * scale] for _ in range(3)]
    else:
        ph = []
        for _ in range(3):
            u = rng.standard_normal(N - 1)
            u = u / np.linalg.norm(u) * math.sqrt(float(rng.uniform(0.8, 1.0)) * tX_max)
            ph.append([arb(float(x)) for x in u])
    X = [sum((x * x for x in ph[v]), arb(0)) for v in range(3)]
    Q = [sum(((ph[r][i] - ph[q][i]) ** 2 for i in range(N - 1)), arb(0)) for (r, q) in PAIRS]
    return X, Q


def dec_up17(x):
    """a 17-significant-digit decimal >= every point of the ball x, checked in arb (kt_cert_v1_9 dec_out's upper side)."""
    hi = x.upper()
    fh = up_float(x)
    sh = '%.16e' % fh
    while not (arb(sh) >= hi):
        fh = math.nextafter(fh, math.inf)
        sh = '%.16e' % fh
    return sh


def run_N(N, rng, rows):
    setup(N, 0)
    out('N=%d: nn %d, T1 1/300, a_m %r, a_e %r, a %r, wbar %s, c_m %r' % (N, N - 1, a_m, a_e, A_BIG, WBAR.str(12), c_m))
    tabs = {}
    for tt in (T1 / 4, T1 / 2, T1):
        G1, n1 = tilted_cov_a(LD, BD, [c_m * tt] * 6)
        if G1 is None:
            raise ValueError('the tilt at t %s is not certainly positive definite' % tt.str(6))
        tabs[tt.str(20)] = (n1, sub_mat(G1, [0, 1, 2]))
    W = {}
    for name, ts_idx, b in STATES:
        setup(N, ts_idx)
        cf = coefs(b)
        M = majorant(cf)
        dM = max(sum(e) for e in M)
        assert dM <= 6, (name, dM)
        Mg = ae.sigma_to_g(M)
        vals = []
        for tt in (T1 / 4, T1 / 2, T1):
            n1, G3 = tabs[tt.str(20)]
            key = tt.str(20)
            if key not in W:
                W[key] = ae.WishartA(G3, nn, 12)
            vals.append(n1 * W[key].E2(Mg, Mg))
        mono = all(vals[i] < vals[i + 1] for i in range(2))
        out('C-MONO N=%d %s: n1 E[M^2] at T1/4, T1/2, T1 = %s -> %s' % (N, name, ', '.join(v.str(10) for v in vals), 'PASS' if mono else 'FAIL'))
        if not mono:
            FAILS.append('C-MONO N%d %s' % (N, name))
        nu = nsqrt(vals[2])
        # C-ID and PLANT-ID: engine A's series against the closed form (order >= 4 agreement; without E0 the agreement is order 1)
        bas, plain = bas_series(b)
        worst, worst_pl, o0 = 0.0, 1.0, 0.0
        for _ in range(12):
            X, Q = point(rng, 1.0, N)
            v = X + Q
            B0v = closed(cf, X, Q, arb(0))[1]
            o0 = max(o0, float((pval(bas[0], v) - B0v).abs_upper()))
            da = [(sval(bas, v, tt) - closed(cf, X, Q, tt)[0]).abs_upper() for tt in (arb(1) / 1000, arb(1) / 2000)]
            dp = [(sval(plain, v, tt) - closed(cf, X, Q, tt)[0]).abs_upper() for tt in (arb(1) / 1000, arb(1) / 2000)]
            worst = max(worst, float(da[1] / da[0]) if not da[0].is_zero() else 0.0)
            worst_pl = min(worst_pl, float(dp[1] / dp[0]) if not dp[0].is_zero() else 1.0)
        idok = worst <= 0.1 and o0 <= 1e-100
        plfire = worst_pl > 0.1
        out('C-ID N=%d %s: order 0 equal (max %.1e); |series - closed| ratio at t 1/2000 vs 1/1000 max %.4f (order 4 gives 1/16) -> %s; '
            'PLANT-ID (no E0) ratio min %.4f -> %s' % (N, name, o0, worst, 'PASS' if idok else 'FAIL', worst_pl, 'FIRED' if plfire else 'NOT FIRED'))
        if not idok:
            FAILS.append('C-ID N%d %s' % (N, name))
        if not plfire:
            UNFIRED.append('PLANT-ID N%d %s' % (N, name))
        # C-MAJ and PLANT-MAJ: M_g >= |B_g(t) - b0_g| / t on the near region (t X_v <= a_m)
        rmax, bad, unc, pfire = 0.0, 0, 0, False
        for tt in (T1, T1 / 10, arb(1) / 10 ** 6):
            for k in range(50):
                if k < 40:
                    while True:
                        X, Q = point(rng, (0.5, 1.0, 2.0, 4.0)[k % 4], N)
                        if all(bool(tt * X[v] <= a_m) for v in range(3)):
                            break
                else:
                    X, Q = point(rng, 1.0, N, float(a_m) / float(tt.mid()) * (1 - 1e-9))
                    if not all(bool(tt * X[v] <= a_m) for v in range(3)):
                        continue
                B, b0 = closed(cf, X, Q, tt)
                lhs = (B - b0).abs_upper() / tt
                Mv = pval(M, X + Q)
                if not (Mv >= lhs):
                    if Mv < lhs:
                        bad += 1
                    else:
                        unc += 1
                if Mv / 100 < lhs:
                    pfire = True
                if Mv > 0:
                    rmax = max(rmax, float((lhs / Mv).mid()))
        majok = bad == 0 and unc == 0
        out('C-MAJ N=%d %s: 150 near-region points (t in T1, T1/10, 1e-6; 30 at the boundary): violations %d, uncertain %d, max |B - b0|/(t M) '
            '%.4f -> %s; PLANT-MAJ (M/100) -> %s' % (N, name, bad, unc, rmax, 'PASS' if majok else 'FAIL', 'FIRED' if pfire else 'NOT FIRED'))
        if not majok:
            FAILS.append('C-MAJ N%d %s' % (N, name))
        if not pfire:
            UNFIRED.append('PLANT-MAJ N%d %s' % (N, name))
        src = TS[N][ts_idx] if b != 'vac' else TS[N][1]
        out('NU N=%d %s: deg M %d, %d terms; n1(T1) %s; E[M^2] %s; nu %s; nu_hi %s (source %s)' % (
            N, name, dM, len(M), tabs[T1.str(20)][0].str(12), (vals[2] / tabs[T1.str(20)][0]).str(12), nu.str(12), dec_up17(nu), src))
        rows.append((N, name, dec_up17(nu), src))


def main():
    c_core()
    c_tri()
    tline = trial_set_line()
    rng = np.random.default_rng(20261121)
    rows = []
    for N in (4, 3):
        run_N(N, rng, rows)
    verdict = 'VALID' if not FAILS and not UNFIRED else 'INVALID'
    out('GATES: fails %s; unfired plants %s' % (FAILS or 'none', UNFIRED or 'none'))
    nu = dict(((N, g), nh) for N, g, nh, src in rows)
    status = 'CERTIFIED' if MODE == 'record' and verdict == 'VALID' else 'DRY' if MODE == 'dry' else 'NOT CERTIFIED'
    lines = ['# NU_G_RECORD (pk24, kt_nu_g_v1_2 %s): certified nu_g for the delta bridge of pk24/NU_G_NOTE_v1.md sect. 3-4' % MODE,
             'FORMAT = NU_G_RECORD_v1', 'RECORD = NU_G_RECORD', 'PRODUCER = pk24 kt_nu_g_v1_2',
             'CODE = pk24/nu/kt_nu_g_v1_2.py:%s' % SELF_SHA, 'STATUS = %s' % status, 'RUN_VERDICT = %s' % verdict, tline,
             'J_LO_CHECK = %d' % J_LO_CHECK, 'T1 = 1/%d' % J_LO_CHECK,
             'CLAIM = for N in {3, 4}, g in {psi, e1, e2, e3} (engine A\'s basis states on the trial set above; psi from vac_poly with the vacres '
             'q1..q3) and every t in (0, 1/J_LO_CHECK]: nu_g >= ||(B_g(t) - b0_g) 1_near||_t / t, the near-region part of '
             '|psi_g(t) - iota_t(b0_g)| / t in engine A\'s norm (the norm of nP: ||F||_t = (n1(t) E_G1(t)[F^2])^1/2, G1, n1 = tilted_cov_a(LD, BD, '
             '[c_m t] * 6) of kt_cert_v1_9, Wishart on column 1); the far part enters through far_out at |m_g(t)| + |delta_g| (BRIDGE). '
             'B_g(t) = E0 pS_g(xi; t) is the full chart function (no truncation: the series remainder is included), b0_g = pS_g(Q/2; 0), '
             'near = t X_v <= a_m at every vertex; TRI_p > 0 (C-TRI). Sign flips of the stored states leave nu_g unchanged.',
             'BRIDGE = |Q_W(t) S e_k| <= [engine A bound with nP -> ||P - r0||_t and far_out at |m_g(t)| + |delta_g|] + t sum_g |delta_g| nu_g, '
             'the last term outside the square root (NU_G_NOTE_v1 sect. 3)',
             'INPUTS = ' + ', '.join('%s:%s' % (p, SHAS[p]) for p in sorted(SHAS)),
             'PARAMS = a_m %r, a_e %r, a = max(a_m, a_e) %r, wbar = 1/(4 (1 - a)), c_m %r, xibar_p = Q_p/2 + T1 wbar d_p/2' % (a_m, a_e, A_BIG, c_m),
             'GATES = C-HASH PASS; C-CORE, C-TRI, C-ID, C-MAJ, C-MONO %s; PLANT-ID, PLANT-MAJ %s' % (
                 'PASS' if not FAILS else 'FAIL (%s)' % ', '.join(FAILS), 'FIRED' if not UNFIRED else 'NOT ALL FIRED (%s)' % ', '.join(UNFIRED)),
             'ROUNDING = nu values are 17-significant-digit decimals rounded up (checked in arb)']
    for N in (4, 3):
        lines.append('N%d_NU = %s %s %s' % (N, nu[(N, 'psi')], nu[(N, 'e1')], nu[(N, 'e3')]))
        lines.append('N%d_NU_E2 = %s' % (N, nu[(N, 'e2')]))
    with open(OUTP, 'x') as fh:
        fh.write('\n'.join(lines) + '\n')
    out('RECORD %s %s (%d values)' % (sha_file(OUTP), OUTP.replace(W18 + '/', ''), len(rows)))
    out('RUN_VERDICT %s (cpu %.1f s)' % (verdict, time.process_time() - T0))
    return 0 if verdict == 'VALID' else 1


if __name__ == '__main__':
    sys.exit(main())
