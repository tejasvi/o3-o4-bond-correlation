#!/usr/bin/env python3
"""make_mrx_v1_10_r2.py (pk22; item (4), the maker's revision after try 1, whose C-WAYA-T0 showed that X1(0), X2(0) are not 0 separately, the P0_LOG rows 4558 and 4738): writes midrow/g4/mrc/src/mrx_cert_v1_10.py from mrx_cert_v1_9.py
(26e77686, frozen in MANIFEST_MRX_CERT_v1_9) by exact replacements with asserted counts, as a new file (mode 'x'): Way A for h-1 and h0 on the last
piece (variant C), from pk25's P2 table (MR_LEMMAP_V3F 47cef0dd), P1's C10 record and C13's C-BH0, on the pattern of pk25's P4 (kt_s9h_ins_v2_7's
waya_last). Pins are computed here from the files and checked against the sha8s the hands published. Also writes the diff. Usage: make_mrx_v1_10_r2.py"""
import ast, difflib, hashlib, os

W = '/mnt/g2/release/root/code'
D = W + '/pk22/midrow/g4/mrc/src'
SRC, DST, DIFF = D + '/mrx_cert_v1_9.py', D + '/mrx_cert_v1_10.py', D + '/diff_mrx_cert_v1_9_to_v1_10.txt'
PINS = {'P2': (W + '/pk25/p2/v3f2/MR_LEMMAP_V3F.kv', '9ef6abaf'), 'P2MAN': (W + '/pk25/p2/MANIFEST_P2_V2_3_CERT_c1.sha256', 'a0dd0699'),
        'C10': (W + '/pk25/c10/C10_RECORD_v1.kv', '29a4f3c6'), 'C10MAN': (W + '/pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256', 'bf8df397'),
        'C13': (W + '/pk25/c13/C13_RECORD_v1_1.kv', '1ff7fcef'), 'C13MAN': (W + '/pk25/c13/MANIFEST_C13_V1_1_CERT_c2.sha256', '14aeb741')}
CHANGED = ('amps', 'h0_end', 'x_cols')


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def rep(t, old, new, count, label):
    n = t.count(old)
    assert n == count, 'replacement %s: %d occurrences, expected %d' % (label, n, count)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    return t.replace(old, new)


def core_defs(text):
    tree = ast.parse(text)
    return {n.name: ast.get_source_segment(text, n) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


for p in (DST, DIFF):
    assert os.path.dirname(p) == D and not os.path.exists(p), p
ssha = sha(SRC)
assert ssha.startswith('3725a2d0'), ssha
print('SOURCE %s %s' % (ssha, SRC))
full = {}
for k, (p, s8) in PINS.items():
    full[k] = sha(p)
    assert full[k].startswith(s8), (k, full[k])
    print('PIN %s %s %s' % (k, full[k], p))
with open(SRC) as fh:
    t = fh.read()
old = t

HEAD = '''"""mrx_cert_v1_10.py (pk22; item (4), the P0_LOG rows 4558 and 4738): mrx_cert_v1_9.py (sha256 %s) with Way A for h-1 and h0
on the last piece, variant C (made by make_mrx_v1_10_r2.py; diff_mrx_cert_v1_9_to_v1_10.txt). v1_9 wrote the last piece of h-1 and h0 by Way B
(Axc 0 0 and a J-free floor Axf); G6's M2 needs Way A there (v1_6_9 sect. 0f item 3, sect. 6: Axf_hi = 0 and Axc enclosing A_x/t at every J of the
piece, t -> 0 included). On the pattern of pk25's P4 (kt_s9h_ins_v2_7, waya_last):
- The x amplitude of each exact end is A_x = F / (P0 s_x) with F = <u_x, w1 - r* w2>, r* = <u, w1>/<u, w2> and P0 = <u, w2>: h-1 with w1, w2 the
  CE3H fH,b and E3 f,b vectors (amps' r and P0 enclose r* and P0 on the piece); h0 with the H4TH hH,b and h0,b vectors (r* in r0 +- Dr, P0 in
  [P0_lo, P0_hi], h0_end's balls).
- F(0) = 0: at t^0 the end vector w1 - r* w2 has no x amplitude (X_POWER 'h-1 1, h0 1'; the order-0 states and the free end factor over the mode
  coordinates, C13's C-GAMMA, and M_c u_x^(0) = h_y^(0) u_xy^(0), C13's C-BH0, with u_x^(0) orthogonal to u^(0) and u_xy^(0), P1's C-SPAN). Lemma A's
  errors vanish at t^0, so F(0) = X1(0) - r*(0) X2(0) with X_i = A~_x(w_i) = sum_b c_xb v_b and r*(0) = N0/D0, N0 = A~_0(w1)(0), D0 = A~_0(w2)(0);
  C-WAYA-T0 checks that the coefficient balls hold T0 = X1(0) D0 - N0 X2(0) = 0. The separate X_i(0) are not 0 (try 1 of this file showed it).
- Hence F/t = X1d - r* X2d - rd X2(0) +- (dx(w1) + |r*| dx(w2))/t, X_id = (X_i(t) - X_i(0))/t, rd = (r*(t) - r*(0))/t = (Nd D0 - N0 Dd)/(P0 D0)
  with Nd and Dd the level-0 differences over t, each +- Lemma A's level-0 error over t; and A_x/t = (F/t)/(P0 s_x).
- Each difference over t at level k: (sum_b c_kb v_b(t) - sum_b c0_kb v_b(0))/t = sum_b dc_kb v_b(t) + sum_b c0_kb (v_b(t) - v_b(0))/t, with
  c_kb = uhat_kb / G_bb^1/2, c0_kb = uhat_kb(0) / G0_bb^1/2 exact (C10's UHAT0 and GT0_W; uhat_0(0) = (1, 0, 0)), dc_kb = du_kb/g_b - u0_kb G1_bb /
  (g_b g0_b (g_b + g0_b)), du_kb P2's (uhat_kb - uhat_kb(0))/t, g_b = G_bb^1/2 on the piece, g0_b = G0_bb^1/2, G1_bb and (v_b(t) - v_b(0))/t from
  the reader's coefficient balls, sum_(k=1..3) [LO_k, HI_k] t^(k-1) + [-R/t, R/t], R the law's four parts without the ak_rad term (entry_law's
  N-1), R/t <= rem 300^4 t_hi^3 + J_lo (tail + ann + far)(J_lo) (C-MONO-TAIL, C-MONO-FAR); C-A0: C10's exact G0_bb lies in G_bb's t^0 ball.
- Lemma A's error at level a over t, from P2's /t fields: qat |Q_W w| + sum_(k != a) eps_kat |A~_k(w)| + (q_a qat + sum_(k != a) eps_ka eps_kat)
  |A~_a(w)|, with |Q_W w_i| for h-1 amps' qw1, qw2 (the norm entries) and for h0 |Q_W w2| <= P0_hi qq, |Q_W w1| <= P0_hi (X + (|r0| + Dr) qq)
  (w1 = P0 (w + r l_3), |Q_W l_3| <= qq, h0_end's fixed point X >= |Q_W w|).
- The written row: Axc = A_x/t rounded outward, Axf 0, and the Ax columns the hull of v1_9's direct Ax ball, 0 and t_1 Axc (t_1 = 1/jlo), so
  G-FACTX holds by construction and C-ROUND still covers the direct ball. Variant U keeps Way B (no J-law there); mrx_combine writes variant C.
New inputs (C-WAYA-IN): P2's MR_LEMMAP_V3F (CERTIFIED; SOURCE naming this run's MR_LEMMAP v3 and C10), P1's C10 record and C13's record, each a
row of its pk25 manifest. New gates: C-WAYA-IN, C-WAYA-RUN (no refusal: C-A0, C-MONO-TAIL, C-MONO-FAR), C-WAYA-T0 (both ends' T0 hold 0),
C-WAYA-CONT (a control of the formula: on the piece before the last, Way A's A_x/t overlaps v1_9's direct Ax/T), C-WAYA-JOIN (the continuity
control: the last piece's Way A Axc overlaps the direct Ax/T of the piece before it), C-WAYA (the last piece's h-1 and h0 rows carry Axf 0 and a
finite Axc); plants PLANT-WAYA-ZERO (u_y(0) in place of u_x(0): h-1's T0 must leave 0) and PLANT-WAYA-PIN (a wrong P2 pin must
be refused). Parts MR_EXACT_PART_v1_10_<V>_N<N>.kv. Usage: mrx_cert_v1_10.py cert N
---- mrx_cert_v1_9.py's docstring:
mrx_cert_v1_9.py (pk22): mrx_cert_v1_8.py with H4TH's certified J-laws''' % ssha
t = rep(t, '"""mrx_cert_v1_9.py (pk22): mrx_cert_v1_8.py with H4TH\'s certified J-laws', HEAD, 1, 'M0 docstring head')
t = rep(t, "    print('usage: mrx_cert_v1_9.py cert N   (N = 4 or 3; certified parts for mrx_combine_v1_9)')",
        "    print('usage: mrx_cert_v1_10.py cert N   (N = 4 or 3; certified parts for mrx_combine_v1_10)')", 1, 'M1 usage')

WAYA_BLOCK = r'''

# ---- mrx_cert_v1_10: Way A on the last piece for h-1 and h0 (see the docstring)
WAYA_SRC = {'P2': (W + '/pk25/p2/v3f2/MR_LEMMAP_V3F.kv', '@@P2@@'), 'P2MAN': (W + '/pk25/p2/MANIFEST_P2_V2_3_CERT_c1.sha256', '@@P2MAN@@'),
            'C10': (W + '/pk25/c10/C10_RECORD_v1.kv', '@@C10@@'), 'C10MAN': (W + '/pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256', '@@C10MAN@@'),
            'C13': (W + '/pk25/c13/C13_RECORD_v1_1.kv', '@@C13@@'), 'C13MAN': (W + '/pk25/c13/MANIFEST_C13_V1_1_CERT_c2.sha256', '@@C13MAN@@')}
WAYA_KEYS = (keysN[-1], keysN[-2])          # the last piece (Way A) and the piece before it (C-WAYA-CONT's control)
WAYA_BAD, WAYA_LOG = [], {}


class WayaRefused(ValueError):
    pass


def waya_arb(e):
    """an exact sympy number (rationals, square roots, sums, products, integer powers) as an arb ball (pk25's waya_arb, kt_s9h_ins_v2_7)."""
    import sympy as sp
    if e.is_Rational:
        return arb(int(e.p)) / arb(int(e.q))
    if e.is_Add:
        s = arb(0)
        for x in e.args:
            s += waya_arb(x)
        return s
    if e.is_Mul:
        s = arb(1)
        for x in e.args:
            s *= waya_arb(x)
        return s
    if e.is_Pow:
        b, x = e.args
        if x == sp.Rational(1, 2):
            return waya_arb(b).sqrt()
        if x == -sp.Rational(1, 2):
            return 1 / waya_arb(b).sqrt()
        if x.is_Integer:
            return waya_arb(b) ** int(x)
    raise WayaRefused('C-WAYA-IN: waya_arb cannot convert %s' % e)


def waya_kv(path):
    head, rows, ix = {}, {}, None
    for ln in open(path).read().splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        if ' = ' not in ln:
            raise WayaRefused('C-WAYA-IN: a line without " = " in %s' % os.path.basename(path))
        k, v = ln.split(' = ', 1)
        if k == 'FIELDS':
            ix = dict((f, i) for i, f in enumerate(v.split()))
        elif re.fullmatch(r'N[34]_P[0-9]+', k):
            rows[k] = v.split()
        elif k in head:
            raise WayaRefused('C-WAYA-IN: the header key %s twice in %s' % (k, os.path.basename(path)))
        else:
            head[k] = v
    return head, rows, ix


def waya_load(src=None):
    """C-WAYA-IN: P2's MR_LEMMAP_V3F (the /t table), P1's C10 record (exact uhat(0), the t^0 Gram G0 on W) and C13's record (C-BH0), each
    pinned and a row of its pk25 manifest (paths relative to pk25/). P2: FORMAT MR_LEMMAP_KV_v3F, RECORD MR_LEMMAP_F, STATUS CERTIFIED,
    RUN_VERDICT VALID, SOURCE naming this run's MR_LEMMAP v3 and the pinned C10, ORIENTATION as MR_LEMMAP v3; C10: certified, valid, N<N>_UHAT0
    equal to P2's, uhat_0(0) = (1, 0, 0), G0_00 = 1; C13: a certified C13_KV_v1 whose CLAIM states C-BH0 exactly."""
    import sympy as sp
    src = WAYA_SRC if src is None else src
    for k, (p, h) in src.items():
        if sha(p) != h:
            raise WayaRefused('C-WAYA-IN: %s does not match its pin' % os.path.basename(p))
    for f, m in (('P2', 'P2MAN'), ('C10', 'C10MAN'), ('C13', 'C13MAN')):
        mrows = dict((ln.split()[1], ln.split()[0]) for ln in open(src[m][0]).read().splitlines() if len(ln.split()) == 2)
        if mrows.get(os.path.relpath(src[f][0], W + '/pk25')) != src[f][1]:
            raise WayaRefused('C-WAYA-IN: %s is not a row of %s' % (os.path.basename(src[f][0]), os.path.basename(src[m][0])))
    h2, rows2, ix2 = waya_kv(src['P2'][0])
    hc = waya_kv(src['C10'][0])[0]
    h13 = waya_kv(src['C13'][0])[0]
    if (h2.get('FORMAT'), h2.get('RECORD'), h2.get('STATUS'), h2.get('RUN_VERDICT')) != ('MR_LEMMAP_KV_v3F', 'MR_LEMMAP_F', 'CERTIFIED', 'VALID') or ix2 is None:
        raise WayaRefused('C-WAYA-IN: the P2 record is not a certified valid MR_LEMMAP_KV_v3F record')
    if ('MR_LEMMAP v3 %s;' % lem_sha[:8]) not in h2.get('SOURCE', '') or ('C10 %s;' % src['C10'][1][:8]) not in h2.get('SOURCE', ''):
        raise WayaRefused('C-WAYA-IN: the P2 record SOURCE does not name this run\'s MR_LEMMAP v3 and the pinned C10 record')
    if not h2.get('ORIENTATION', '').startswith('u_x along e1, u_y along e3'):
        raise WayaRefused('C-WAYA-IN: the P2 record ORIENTATION is not MR_LEMMAP v3\'s')
    if (hc.get('FORMAT'), hc.get('STATUS'), hc.get('RUN_VERDICT')) != ('C10_KV_v1', 'CERTIFIED', 'VALID'):
        raise WayaRefused('C-WAYA-IN: the C10 record is not a certified valid C10_KV_v1')
    if (h13.get('FORMAT'), h13.get('STATUS')) != ('C13_KV_v1', 'CERTIFIED') or 'C-BH0 holds exactly' not in h13.get('CLAIM', ''):
        raise WayaRefused('C-WAYA-IN: the C13 record is not a certified C13_KV_v1 stating C-BH0 exactly')
    raw = hc.get('N%d_UHAT0' % N)
    if raw is None or h2.get('N%d_UHAT0' % N) != raw:
        raise WayaRefused('C-WAYA-IN: N%d_UHAT0 differs between the P2 and C10 records' % N)
    u = {}
    for part in raw.split('; '):
        nm, ex = part.split(' ', 1)
        mt = re.fullmatch(r'u([0xy])([p13])', nm)
        if mt is None or (mt.group(1), mt.group(2)) in u:
            raise WayaRefused('C-WAYA-IN: N%d uhat name %r' % (N, nm))
        u[(mt.group(1), mt.group(2))] = sp.sympify(ex)
    if len(u) != 9 or [u[('0', b)] for b in 'p13'] != [1, 0, 0]:
        raise WayaRefused('C-WAYA-IN: N%d_UHAT0 is not nine values with uhat_0(0) = (1, 0, 0)' % N)
    mg = re.fullmatch(r'G \[(.+)\]; T \[(.+)\] \(psi-hat, s1, s3 unnormalised, t\^0\)', hc.get('N%d_GT0_W' % N, ''))
    if mg is None:
        raise WayaRefused('C-WAYA-IN: N%d_GT0_W does not parse' % N)
    G0 = [sp.sympify(e) for e in mg.group(1).split(', ')]
    if len(G0) != 9 or G0[0] != 1:
        raise WayaRefused('C-WAYA-IN: N%d G0 is not 3 x 3 with G0_00 = 1' % N)
    return dict(rows=rows2, ix=ix2, ux0=[waya_arb(u[('x', b)]) for b in 'p13'], uy0=[waya_arb(u[('y', b)]) for b in 'p13'],
                G0d=[waya_arb(G0[0]), waya_arb(G0[4]), waya_arb(G0[8])])


def waya_ent(e):
    """(record, certificate, family, key) of Ent e for the reader's entry_ball and entry_law: CE3H and H4TH from c3h's records and certificate,
    E3 from S8's, S9's G entries through their alias in S8's D record (file name and sha256 checked), as cert_law takes them."""
    rk, key = e.name.split(':', 1)
    if rk in ('CE3H', 'H4TH') and CERTS.get('c3h') is not None:
        return CERT_RECS['c3h'][rk], CERTS['c3h'], rk, key
    if rk == 'E3' and CERTS.get('s8') is not None:
        return CERT_RECS['s8']['E3'], CERTS['s8'], 'E3', key
    if rk == 'S9' and CERTS.get('s8') is not None:
        fn, k2, h = RJ['S9']['items'][key]['alias_of'].split()
        d = CERT_RECS['s8']['D']
        if os.path.basename(fn) == d['name'] and h == d['sha256']:
            return d, CERTS['s8'], 'D', k2
    raise WayaRefused('C-WAYA-IN: no certified law for %s' % e.name)


def waya_rt(law, J_lo, t_hi):
    """R/t over a piece starting at J_lo (t <= t_hi): rem 300^4 t_hi^3 + J_lo (tail (P(J_lo)/P(300))^1/2 + ann (P(J_lo)/P(300))^1/2 +
    far e^(-far_rate (J_lo - 300))), the law's four parts without the ak_rad term (entry_law's N-1), with C-MONO-TAIL (J_lo a/G > 5 for every
    chi-square pair, so J^2 P(J) decreases) and C-MONO-FAR (J_lo far_rate > 1, so J e^(-far_rate J) decreases); pk25's waya_rt."""
    L, parts = law['laws'], law['parts']
    if L is None:
        return arb(0)
    J = ab(Fr(J_lo))
    tot = ab(parts['rem']) * arb(300) ** 4 * t_hi ** 3
    for part in ('tail', 'ann'):
        g = L[part]
        for a, G in g['a_G']:
            if not (J * ab(a) / ab(G) > 5):
                raise WayaRefused('C-MONO-TAIL: J_lo a/G is not above 5 for a %s pair' % part)
        tot = tot + J * ab(parts[part]) * (p_lawq(g, Fr(J_lo)).upper() / p_lawq(g, Fr(300)).lower()).sqrt()
    fr = ab(L['far_rate'])
    if not (J * fr > 1):
        raise WayaRefused('C-MONO-FAR: J_lo far_rate is not above 1')
    tot = tot + J * ab(parts['far']) * (-fr * (J - 300)).exp()
    return tot.upper()


def waya_x1(e, x0, J_lo, t_hi, tb):
    """(X(t) - X(0))/t over the piece in the reader's coefficient-ball form (pk25's waya_x1): the true a_k lie in [LO_k, HI_k] (entry_ball) and
    the rest of the law is at most R(J), so X1 lies in sum_(k=1..3) [LO_k, HI_k] t^(k-1) + [-R/t, R/t] with X(0) = a_0 in [LO_0, HI_0]. x0 (an
    exact arb value, or None) must lie in [LO_0, HI_0] (C-A0). Returns (X1, [LO_0, HI_0])."""
    rec, cert, fam, key = waya_ent(e)
    LO, HI, _eb = RDR.entry_ball(rec, key)
    if len(LO) != 4 or len(HI) != 4:
        raise WayaRefused('C-A0: %s has %d coefficient balls, expected 4' % (e.name, len(LO)))
    ball = lambda k: ab(Fr(LO[k])).union(ab(Fr(HI[k])))
    if x0 is not None and not (ab(Fr(LO[0])) <= x0 and x0 <= ab(Fr(HI[0]))):
        raise WayaRefused('C-A0: P1\'s exact %s(0) is outside [LO_0, HI_0]' % e.name)
    s = arb(0)
    for k in (3, 2, 1):
        s = s * tb + ball(k)
    return s + arb(0, 1) * waya_rt(RDR.entry_law(cert, fam, key), J_lo, t_hi), ball(0)


def waya_piece(key, W0):
    """P2's row of the piece (the same jlo and jhi as LR's), its J_lo and t_hi = 1/J_lo."""
    pr = W0['rows'].get(key)
    if pr is None or pr[W0['ix']['jlo']] != LR[key][0] or pr[W0['ix']['jhi']] != LR[key][1]:
        raise WayaRefused('C-WAYA-IN: P2 has no row %s with jlo %s and jhi %s' % (key, LR[key][0], LR[key][1]))
    return pr, Fr(LR[key][0]), (1 / ab(Fr(LR[key][0]))).upper()


def waya_coefs(pr, nrm, W0, J_lo, t_hi, tb):
    """the Ritz coefficients c_kb = uhat_kb / G_bb^1/2 (amps' U[k][b] / nrm[b]) and their parts on the piece: c0[k]_b = uhat_kb(0) / G0_bb^1/2
    exact (C10; uhat_0(0) = (1, 0, 0)) for k = 0, x, y, and dc[k]_b = (c_kb - c0[k]_b)/t = du_kb/g_b - u0_kb G1_bb/(g_b g0_b (g_b + g0_b)) for
    k = 0, x, with du_kb P2's (uhat_kb - uhat_kb(0))/t, g_b = nrm[b], g0_b = G0_bb^1/2, G1_bb by waya_x1 on S9's G,b,b (C-A0). Returns (c0, dc)."""
    hv = lambda f: ab(Fr(pr[W0['ix'][f + '_lo']])).union(ab(Fr(pr[W0['ix'][f + '_hi']])))
    G1 = [waya_x1(S9G[(b, b)], W0['G0d'][i], J_lo, t_hi, tb)[0] for i, b in enumerate(ST)]
    g0 = [W0['G0d'][i].sqrt() for i in range(3)]
    u0 = {'0': [arb(1), arb(0), arb(0)], 'x': W0['ux0'], 'y': W0['uy0']}
    c0 = dict((k, [u0[k][i] / g0[i] for i in range(3)]) for k in ('0', 'x', 'y'))
    dc = dict((k, [hv('u%s%st' % (k, BV[i])) / nrm[i] - u0[k][i] * G1[i] / (nrm[i] * g0[i] * (nrm[i] + g0[i])) for i in range(3)]) for k in ('0', 'x'))
    return c0, dc


def waya_xt(ents, c0, dc, T, jlo, laws, J_lo, t_hi):
    """(X(t) - X(0))/t for X = sum_b c_kb v_b(t) at one level: sum_b dc_b v_b(t) + sum_b c0_b (v_b(t) - v_b(0))/t, and X(0)'s ball
    sum_b c0_b [LO_0, HI_0]."""
    xt, z0 = arb(0), arb(0)
    for i in range(3):
        x1, a0 = waya_x1(ents[i], None, J_lo, t_hi, T)
        xt = xt + dc[i] * ents[i].ball(T, jlo, laws) + c0[i] * x1
        z0 = z0 + c0[i] * a0
    return xt, z0


def waya_t0(ents, c, J_lo, t_hi, T):
    """X(0)'s ball sum_b c_b [LO_0, HI_0] alone (PLANT-WAYA-ZERO's level y)."""
    return sum((c[i] * waya_x1(ents[i], None, J_lo, t_hi, T)[1] for i in range(3)), arb(0))


def waya_dt(pr, W0, a, q, eps, qw, A):
    """Lemma A's error at level a over t, from P2's /t fields: qat qw + sum_(k != a) eps_kat |A_k| + (q_a qat + sum_(k != a) eps_ka eps_kat) |A_a|,
    for a vector w with |Q_W w| <= qw and Ritz amplitude balls A (levels 0, x, y), q_a and eps_ka MR_LEMMAP v3's."""
    fv = lambda f: ab(Fr(pr[W0['ix'][f]]))
    qat = fv('q%st_hi' % a)
    oth = [k for k in LV if k != a]
    et = dict((k, fv('eps_%s%st_hi' % (k, a))) for k in oth)
    qwb = qw if isinstance(qw, arb) else ab(qw)
    return (qat * qwb + sum((et[k] * ab(absup(A[k])) for k in oth), arb(0)) +
            (ab(q[a]) * qat + sum((ab(eps[(k, a)]) * et[k] for k in oth), arb(0))) * ab(absup(A[a]))).upper()


def waya_end(key, w1e, w2e, T, jlo, laws, nrm, q, eps, S, rb, Dt, qw1, qw2, A1, A2, W0):
    """Way A for an exact end, A_x = F / (Dt s_x) with F = <u_x, w1 - r* w2>, r* = <u, w1>/<u, w2> in the ball rb and Dt = <u, w2> on the piece (h-1:
    amps' r and P0; h0: r0 +- Dr and P0's interval). F(0) = X1(0) - r*(0) X2(0) = 0 (X_i = A~_x(w_i), r*(0) = N0/D0, N0 = A~_0(w1)(0), D0 = A~_0(w2)(0);
    Lemma A's errors vanish at t^0), so F/t = X1d - r* X2d - rd X2(0) +- (dx(w1) + |r*| dx(w2))/t with X_id = (X_i(t) - X_i(0))/t and
    rd = (r*(t) - r*(0))/t = (Nd D0 - N0 Dd)/(Dt D0), Nd, Dd the level-0 differences over t, each +- Lemma A's level-0 error over t. Returns the
    A_x/t ball with its parts, T0 = X1(0) D0 - N0 X2(0) (C-WAYA-T0) and T0y, the same with u_y(0) in place of u_x(0) (PLANT-WAYA-ZERO)."""
    pr, J_lo, t_hi = waya_piece(key, W0)
    c0, dc = waya_coefs(pr, nrm, W0, J_lo, t_hi, T)
    X1d, X10 = waya_xt(w1e, c0['x'], dc['x'], T, jlo, laws, J_lo, t_hi)
    X2d, X20 = waya_xt(w2e, c0['x'], dc['x'], T, jlo, laws, J_lo, t_hi)
    N1d, N0 = waya_xt(w1e, c0['0'], dc['0'], T, jlo, laws, J_lo, t_hi)
    D1d, D0 = waya_xt(w2e, c0['0'], dc['0'], T, jlo, laws, J_lo, t_hi)
    X1y0, X2y0 = waya_t0(w1e, c0['y'], J_lo, t_hi, T), waya_t0(w2e, c0['y'], J_lo, t_hi, T)
    d01, d02 = waya_dt(pr, W0, '0', q, eps, qw1, A1), waya_dt(pr, W0, '0', q, eps, qw2, A2)
    dx1, dx2 = waya_dt(pr, W0, 'x', q, eps, qw1, A1), waya_dt(pr, W0, 'x', q, eps, qw2, A2)
    rd = ((N1d + arb(0, d01)) * D0 - N0 * (D1d + arb(0, d02))) / (Dt * D0)
    Ft = X1d - rb * X2d - rd * X20 + arb(0, (dx1 + ab(absup(rb)) * dx2).upper())
    return dict(Axc=Ft / (Dt * S['x']), T0=X10 * D0 - N0 * X20, T0y=X1y0 * D0 - N0 * X2y0, Ft=Ft, rd=rd, X10=X10, X20=X20, N0=N0, D0=D0,
                err=(dx1 + ab(absup(rb)) * dx2).upper())


try:
    WAYA = waya_load()
    okw, whyw = True, 'loaded'
except WayaRefused as ex:
    WAYA, okw, whyw = None, False, str(ex)[:200]
gate('C-WAYA-IN', okw, '(P2\'s MR_LEMMAP_V3F %s, C10 %s, C13 %s, each a row of its pk25 manifest; P2 CERTIFIED, its SOURCE naming MR_LEMMAP v3 %s and C10; '
     'UHAT0 equal; C13 states C-BH0 exactly: %s)' % (WAYA_SRC['P2'][1][:8], WAYA_SRC['C10'][1][:8], WAYA_SRC['C13'][1][:8], lem_sha[:8], whyw))
try:
    waya_load(dict(WAYA_SRC, P2=(WAYA_SRC['P2'][0], '0' * 64)))
    fired = False
except WayaRefused:
    fired = True
plant('PLANT-WAYA-PIN', fired, '(a wrong pin for P2\'s record must be refused)')
'''
for k in PINS:
    assert WAYA_BLOCK.count('@@%s@@' % k) == 1, k
    WAYA_BLOCK = WAYA_BLOCK.replace('@@%s@@' % k, full[k])
assert '@@' not in WAYA_BLOCK
H0V_LINE = "H0V = ([Ent('H4TH', 'hH,%d' % b) for b in ST], [Ent('H4TH', 'h0,%d' % b) for b in ST])   # mrx_cert_v1_8: w1 = S M_h l_2, w2 = S l_2 (c3h's H4TH)\n"
t = rep(t, H0V_LINE, H0V_LINE + WAYA_BLOCK, 1, 'M2 Way A block')
t = rep(t, "                    'qw1': qw1, 'qw2': qw2, 'qwsa': qwsa, 'parts': parts, 'r': r, 'lp': lp}   # mrx_cert_v1_7: r and Lemma P's bound kept\n",
        "                    'qw1': qw1, 'qw2': qw2, 'qwsa': qwsa, 'parts': parts, 'r': r, 'lp': lp}   # mrx_cert_v1_7: r and Lemma P's bound kept\n"
        "        if end == 'h-1' and laws == 'C' and key in WAYA_KEYS and WAYA is not None:   # mrx_cert_v1_10: Way A (last piece) and its control\n"
        "            try:\n"
        "                res[end]['waya'] = waya_end(key, v1e, v2e, T, jlo, laws, nrm, q, eps, S, r, P0, qw1, qw2, A1, A2, WAYA)\n"
        "            except WayaRefused as ex:\n"
        "                WAYA_BAD.append((key, end, str(ex)[:160]))\n"
        "                res[end]['waya'] = None\n"
        "            WAYA_LOG[(key, end)] = res[end]\n"
        "            if tlo == 0 and res[end]['waya'] is not None:\n"
        "                res[end]['Axc'] = res[end]['waya']['Axc']\n", 1, 'M3 amps hook (h-1)')
t = rep(t, "    return {'Ay': amp['y'], 'Ax': amp['x'], 'Np': rW, 'Axc': (amp['x'] / T) if tlo > 0 else None, 'P0': P0b, 'qw1': float('nan'),\n"
           "            'qw2': float(qq), 'qwsa': float(X), 'parts': parts, 'Pe': pe, 'pe_float': float(pe), 'X': X, 'Dr': Dr}\n",
        "    wy = None\n"
        "    if laws == 'C' and key in WAYA_KEYS and WAYA is not None:   # mrx_cert_v1_10: Way A for h0 (last piece) and its control\n"
        "        try:\n"
        "            A1w = dict((k, sum((U[k][i] * w1[i] / nrm[i] for i in range(3)), arb(0))) for k in LV)\n"
        "            wy = waya_end(key, H0V[0], H0V[1], T, jlo, laws, nrm, q, eps, S, r0 + arb(0, ab(Dr).upper()), P0b,\n"
        "                          P0hi * (X + (absup(r0) + Dr) * qq), P0hi * qq, A1w, A2, WAYA)\n"
        "        except WayaRefused as ex:\n"
        "            WAYA_BAD.append((key, 'h0', str(ex)[:160]))\n"
        "    d0 = {'Ay': amp['y'], 'Ax': amp['x'], 'Np': rW, 'Axc': (amp['x'] / T) if tlo > 0 else (wy['Axc'] if wy is not None else None), 'P0': P0b,\n"
        "          'qw1': float('nan'), 'qw2': float(qq), 'qwsa': float(X), 'parts': parts, 'Pe': pe, 'pe_float': float(pe), 'X': X, 'Dr': Dr, 'waya': wy}\n"
        "    if laws == 'C' and key in WAYA_KEYS:\n"
        "        WAYA_LOG[(key, 'h0')] = d0\n"
        "    return d0\n", 1, 'M4 h0_end hook')
t = rep(t, "    if jhi_s == 'inf':\n        f = dec(max(abs(lo_of(d['Ax'])), abs(hi_of(d['Ax']))), True)\n",
        "    if jhi_s == 'inf' and d.get('waya') is not None:   # mrx_cert_v1_10: Way A, Axf 0, Ax the hull of the direct ball, 0 and t_1 Axc\n"
        "        c_lo, c_hi = dec(lo_of(d['waya']['Axc']), False), dec(hi_of(d['waya']['Axc']), True)\n"
        "        t1 = 1 / Fr(jlo_s)\n"
        "        return (dec(min(lo_of(d['Ax']), Fr(0), t1 * Fr(c_lo)), False), dec(max(hi_of(d['Ax']), Fr(0), t1 * Fr(c_hi)), True), c_lo, c_hi, '0')\n"
        "    if jhi_s == 'inf':\n        f = dec(max(abs(lo_of(d['Ax'])), abs(hi_of(d['Ax']))), True)\n", 1, 'M5 x_cols Way A')
GATES = r'''
# ---- mrx_cert_v1_10: the Way A gates (variant C)
gate('C-WAYA-RUN', WAYA is not None and not WAYA_BAD, '(Way A on %s and %s for h-1 and h0: no refusal (C-WAYA-IN at use, C-A0, C-MONO-TAIL, C-MONO-FAR); '
     'failures %s)' % (keysN[-1], keysN[-2], WAYA_BAD[:3]))
t0_lines, t0_ok = [], WAYA is not None and not WAYA_BAD
for end in ('h-1', 'h0'):
    dW = WAYA_LOG.get((keysN[-1], end), {}).get('waya')
    if dW is None:
        t0_ok = False
        continue
    t0_ok = t0_ok and dW['T0'].overlaps(arb(0))
    t0_lines.append('%s: T0 %s (X1(0) %s, X2(0) %s, N0 %s, D0 %s)' % (end, dW['T0'].str(6, radius=True), dW['X10'].str(6, radius=True),
                                                                  dW['X20'].str(6, radius=True), dW['N0'].str(6, radius=True), dW['D0'].str(6, radius=True)))
gate('C-WAYA-T0', t0_ok, '(T0 = X1(0) D0 - N0 X2(0) holds 0 for both ends; F(0) = 0 exactly by C13\'s C-GAMMA and C-BH0 with P1\'s C-SPAN: %s)' % (
    '; '.join(t0_lines)))
dZ = WAYA_LOG.get((keysN[-1], 'h-1'), {}).get('waya')
plant('PLANT-WAYA-ZERO', dZ is not None and not dZ['T0y'].overlaps(arb(0)), '(u_y(0) in place of u_x(0) in h-1\'s T0: %s must leave 0)' % (
    dZ['T0y'].str(6, radius=True) if dZ is not None else 'not computed'))
ct_lines, ct_ok = [], WAYA is not None and not WAYA_BAD
for end in ('h-1', 'h0'):
    dC = WAYA_LOG.get((keysN[-2], end))
    if dC is None or dC.get('waya') is None or dC.get('Axc') is None:
        ct_ok = False
        continue
    ok1 = dC['waya']['Axc'].overlaps(dC['Axc'])
    ct_ok = ct_ok and ok1
    ct_lines.append('%s: Way A %s, direct Ax/T %s%s' % (end, dC['waya']['Axc'].str(8, radius=True), dC['Axc'].str(8, radius=True), '' if ok1 else ' (NO OVERLAP)'))
gate('C-WAYA-CONT', ct_ok, '(the control on %s [%s, %s], a piece with t_lo > 0: Way A\'s A_x/t overlaps v1_9\'s direct Ax/T (P2\'s /t fields are '
     'crude there, X_hi jhi): %s)' % (keysN[-2], LR[keysN[-2]][0], LR[keysN[-2]][1], '; '.join(ct_lines)))
jn_lines, jn_ok = [], WAYA is not None and not WAYA_BAD
for end in ('h-1', 'h0'):
    dL, dC = WAYA_LOG.get((keysN[-1], end)), WAYA_LOG.get((keysN[-2], end))
    if dL is None or dL.get('waya') is None or dC is None or dC.get('Axc') is None:
        jn_ok = False
        continue
    ok1 = dL['waya']['Axc'].overlaps(dC['Axc'])
    jn_ok = jn_ok and ok1
    jn_lines.append('%s: last piece Way A [%.6f, %.6f], the piece before, direct Ax/T [%.6f, %.6f]%s' % (
        end, float(lo_of(dL['waya']['Axc'])), float(hi_of(dL['waya']['Axc'])), float(lo_of(dC['Axc'])), float(hi_of(dC['Axc'])), '' if ok1 else ' (NO OVERLAP)'))
gate('C-WAYA-JOIN', jn_ok, '(A_x/t is continuous at J = %s: the last piece\'s Way A Axc overlaps the direct Ax/T of the piece before it: %s)' % (
    LR[keysN[-1]][0], '; '.join(jn_lines)))
wl_lines, wl_ok = [], True
for ln, d in rows['C']:
    k_, e_ = ln.split(' = ')[0].rsplit('_', 1)
    if k_ == keysN[-1] and e_ in ('h-1', 'h0'):
        f = ln.split(' = ')[1].split()
        okr = f[10] == '0' and d.get('waya') is not None and d['waya']['Axc'].is_finite()
        wl_ok = wl_ok and okr
        sg = 'positive' if Fr(f[8]) > 0 else ('negative' if Fr(f[9]) < 0 else 'open')
        wl_lines.append('%s: Axc [%s, %s] (%s), Axf %s, Ax [%s, %s]' % (e_, f[8], f[9], sg, f[10], f[4], f[5]))
gate('C-WAYA', wl_ok and len(wl_lines) == 2, '(the last piece %s of variant C: h-1 and h0 rows with Axf 0 and a finite Way A Axc: %s)' % (
    keysN[-1], '; '.join(wl_lines)))
'''
ANCHOR = "gate('C-ROUND', bad_round == 0, '(every written Ay_lo, Ax_lo and h-1 Axc_lo off the last piece <= the exact lower ends; Ay_hi, Ax_hi, Axc_hi, Np_hi '\n     '>= the upper ends; failures %d)' % bad_round)\n"
t = rep(t, ANCHOR, ANCHOR + GATES, 1, 'M6 Way A gates')
t = rep(t, "    path = os.path.join(OUTD, 'MR_EXACT_PART_v1_9_%s_N%d.kv' % (V, N))\n", "    path = os.path.join(OUTD, 'MR_EXACT_PART_v1_10_%s_N%d.kv' % (V, N))\n", 1,
        'M7 part name')
t = rep(t, "    head = ['# MR_EXACT PART (N = %d) of pk22 mrx_cert_v1_9 on mr/v4 MR_SPECTRAL and MR_INSERT with mr/v3 MR_LEMMAP (mrx_combine_v1_9 joins '",
        "    head = ['# MR_EXACT PART (N = %d) of pk22 mrx_cert_v1_10 on mr/v4 MR_SPECTRAL and MR_INSERT with mr/v3 MR_LEMMAP (mrx_combine_v1_10 joins '", 1,
        'M8 part comment')
t = rep(t, "'PRODUCER = pk22 mrx_cert_v1_9 CERT_%s' % V,", "'PRODUCER = pk22 mrx_cert_v1_10 CERT_%s' % V,", 1, 'M9 producer')
t = rep(t, "'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py:%s' % code_sha[:8]", "'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py:%s' % code_sha[:8]", 1,
        'M10 code line')
t = rep(t, "' MR_LEMMAP.kv:%s MR_SPECTRAL.kv:%s MR_INSERT.kv:%s' % (\n                lem_sha[:8], spe_sha[:8], ins_sha[:8]),",
        "' MR_LEMMAP.kv:%s MR_SPECTRAL.kv:%s MR_INSERT.kv:%s MR_LEMMAP_V3F.kv:%s C10_RECORD_v1.kv:%s C13_RECORD_v1_1.kv:%s' % (\n"
        "                lem_sha[:8], spe_sha[:8], ins_sha[:8], WAYA_SRC['P2'][1][:8], WAYA_SRC['C10'][1][:8], WAYA_SRC['C13'][1][:8]),", 1, 'M11 SOURCE line')
od, nd = core_defs(old), core_defs(t)
chg = sorted(k for k in od if k in nd and od[k] != nd[k])
new = sorted(k for k in nd if k not in od)
gone = sorted(k for k in od if k not in nd)
print('DEFS identical %d, changed %s, added %s, dropped %s' % (len([k for k in od if k in nd and od[k] == nd[k]]), chg, new, gone))
assert chg == sorted(CHANGED) and not gone, (chg, gone)
assert new == sorted(['WayaRefused', 'waya_arb', 'waya_kv', 'waya_load', 'waya_ent', 'waya_rt', 'waya_x1', 'waya_piece', 'waya_coefs', 'waya_xt',
                      'waya_t0', 'waya_dt', 'waya_end']), new
with open(DST, 'x') as fh:
    fh.write(t)
with open(DIFF, 'x') as fh:
    fh.writelines(difflib.unified_diff(old.splitlines(True), t.splitlines(True), 'mrx_cert_v1_9.py', 'mrx_cert_v1_10.py'))
print('WROTE %s %s (%d lines)' % (sha(DST), DST, t.count('\n')))
print('WROTE %s %s' % (sha(DIFF), DIFF))
