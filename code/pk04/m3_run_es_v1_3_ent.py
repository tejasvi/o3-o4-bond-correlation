"""m3_run_es_v1_3_ent.py -- pk04 (code/pk04/). A part of m3_run_es_v1_3.py, executed in the runner's namespace after its C-HASH
has checked these bytes against PARTS: the list, rule, partition, prep and entry machinery, the smoke Xa and the entry pieces.
m3_run_es_v1_2_ent.py (fcef5819) with the script's names taken from the runner (SNAME) and C-PREP-FOREIGN-C4 at a P12 smoke. Defines
only."""


def list_check():
    """C-LIST: counts, ids, shapes, distinct factor lists, K 3, uses (96, each once), 16 keys per record. C-LIST-RULE: class_windows equals
    the list (family, factor list, key, uses). PLANT-LIST: ES9 without a window; PLANT-LIST-RULE: D3's bb on the top row."""
    bad = [g for g in FAMS if len(entries_of(g)) != COUNTS[g][0] or len({json.dumps(e['factors']) for e in entries_of(g)}) != COUNTS[g][0]
           or any(not e['uses'] or e['id'] != '%s:%s' % (g, name_of(e)) or e['shape'] != SHAPE[g] for e in entries_of(g))]
    uses = [u for e in V3 for u in e['uses']]
    rk = rec_keys()
    want = {'ES,%s,%d' % (m, k) for m in ('1', 'e', 'f', 'ef') for k in range(4)}
    okr = len(rk) == len(RECDEF) and all(set(v) == want for v in rk.values())
    gate('C-LIST', not bad and len(uses) == 96 and len(set(uses)) == 96 and okr and all(GRAPHS[g]['K'] == 3 for g in FAMS),
         '(%s %s: %s windows; %d uses, %d distinct; %d records of 16 keys: %s; failing %s)' % (LF, INPUTS[(LISTD, LF)][:8], '/'.join(
             str(len(entries_of(g))) for g in FAMS), len(uses), len(set(uses)), len(rk), okr, bad or 'none'))
    plant('PLANT-LIST', len(entries_of('ES9')[1:]) != COUNTS['ES9'][0], '(ES9 without its first window)')
    mine = {(e['graph'], json.dumps(e['factors'])): (name_of(e), sorted(e['uses'])) for e in V3}
    rule = {k: (v['key'], sorted(v['uses'])) for k, v in class_windows().items()}
    gate('C-LIST-RULE', mine == rule, '(the class rules give %d windows, the list %d: %s)' % (len(rule), len(mine), 'equal' if mine == rule else 'DIFFERENT'))
    rule2 = {k: (v['key'], sorted(v['uses'])) for k, v in class_windows(bb_row=0).items()}
    plant('PLANT-LIST-RULE', rule2 != mine, '(D3\'s bb bond on the top row: %s)' % ('differs' if rule2 != mine else 'EQUAL'))


def enc_check():
    """C-ENC: three sample encodings and every used pair form among the list pairs. PLANT-ENC: [st, 0, 0] and [cp, 10, 0] must raise."""
    e1 = [1.0] + [0.0] * 8
    pv = lambda c: ('p', (3 * c, 3 * c + 1, 3 * c + 2), list(TS.q[0]), list(TS.q[1]), list(TS.q[2]))
    got = [ENT.factor(TS, 'N', enc_of(x)) for x in (['cp', 1, 0], ['cp', 0, 0], ['xi', [3, 6]])]
    want = [('xi', (0, 1, 2), float(TS.S[0][1]), [float(TS.S[r][1]) for r in range(1, 10)]), pv(0), ('xi', (3, 6, 6), 0.0, e1)]
    outp = []
    for e in V3:
        prs = set(tuple(sorted(p)) for p in GRAPHS[e['graph']]['pairs'])
        for f in facs_of(e):
            outp += ['%s %s' % (e['id'], p) for p in ENT.pairs_of(f) if tuple(sorted(p)) not in prs]
    gate('C-ENC', got == want and not outp, '([cp, 1, 0], [cp, 0, 0], [xi, [3, 6]] give the conventions\' tuples: %s; pair forms outside the '
         'list pairs: %s)' % (got == want, outp[:5] or 'none'))
    r0 = []
    for x in (['st', 0, 0], ['cp', 10, 0]):
        try:
            enc_of(x)
            r0.append(False)
        except ValueError:
            r0.append(True)
    plant('PLANT-ENC', all(r0), '([st, 0, 0] and [cp, 10, 0] refused: %s)' % r0)


def parity_set():
    """C-PARITY-SET: the windows passing c_odd_h = ZERO = marked = the list's parity zeros (W1,2 in ES9 and ES12A). PLANT-ODD: ES9 W1,2 with
    S[1][2] + 1e-12 must fail c_odd_h."""
    import copy
    got = {g: sorted(name_of(e) for e in entries_of(g) if c_odd_h(g, facs_of(e))[0]) for g in FAMS}
    marked = {g: sorted(name_of(e) for e in entries_of(g) if e['parity'] == 'zero') for g in FAMS}
    listed = {g: sorted(name_of(e) for e in entries_of(g) if e['list_zero']) for g in FAMS}
    gate('C-PARITY-SET', all(got[g] == sorted(ZERO[g]) == marked[g] == listed[g] for g in FAMS), '(windows passing C-ODD: %s; marked zero: %s; '
         'the list\'s parity zeros: %s)' % (got, marked, listed))
    ts2 = copy.deepcopy(TS)
    ts2.S[1][2] = ts2.S[1][2] + 1e-12
    e = entries_of('ES9', ['W1,2'])[0]
    ok1, _ = c_odd_h('ES9', facs_of(e))
    ok2, why = c_odd_h('ES9', facs_of(e, ts2))
    plant('PLANT-ODD', ok1 and not ok2, '(ES9 W1,2: passes %s; with S[1][2] + 1e-12: %s)' % (ok1, why))


def alias_check():
    """C-ALIAS: no alias among the windows. PLANT-ALIAS: ES9 x3_6,0 with its bond moved to (4, 5) has x4_5,0's multiset."""
    ok = all(ALIAS[g] == ALIASES[g] for g in FAMS)
    gate('C-ALIAS', ok, '(aliases recomputed from the factor tuples equal ALIASES (none): %s)' % ok)
    e = dict(entries_of('ES9', ['x3_6,0'])[0])
    e2 = dict(e, factors=[['xi', [4, 5]] if x == ['xi', [3, 6]] else x for x in e['factors']])
    xb = mkey(facs_of(entries_of('ES9', ['x4_5,0'])[0]))
    plant('PLANT-ALIAS', mkey(facs_of(e2)) == xb and mkey(facs_of(e)) != xb, '(ES9 x3_6,0 with its bond moved to (4, 5) matches x4_5,0; '
          'x3_6,0 itself must not)')


def rule_of(e):
    """the partition rule (as m3_run_r0b_v1_3): std without a bond; with one, RULE_TAB's rule (none here), else col."""
    if not any(x[0] == 'xi' for x in e['factors']):
        return 'std'
    return RULE_TAB.get(e['graph'], {}).get(name_of(e), 'col')


RULES = ('std', 'col', 'colb', 'colh', 'colxh')


def rule_of_check():
    """C-RULE-OF as m3_run_r0b_v1_3; PLANT-RULE-OF: ES9 W1,0 with [xi, [3, 6]] added must take a bonded rule, W1,0 itself std."""
    ks = [entries_of(g, [k])[0] for g in FAMS for k in order_of(g)]
    vals = [rule_of(e) for e in ks]
    comp = {(e['graph'], name_of(e)) for e in ks if any(x[0] == 'xi' for x in e['factors'])}
    tab = [(g, k) for g in RULE_TAB for k in RULE_TAB[g]]
    ok = (set(vals) <= set(RULES) and all((v == 'std') == (not any(x[0] == 'xi' for x in e['factors'])) for v, e in zip(vals, ks))
          and all(t in comp for t in tab))
    gate('C-RULE-OF', ok, '(%d computed keys: std %d, col %d, colh %d, colb %d; RULE_TAB keys %d, all bonded computed keys: %s)' % (
        len(ks), vals.count('std'), vals.count('col'), vals.count('colh'), vals.count('colb'), len(tab), all(t in comp for t in tab)))
    z = dict(entries_of('ES9', ['W1,0'])[0])
    z2 = dict(z, factors=z['factors'] + [['xi', [3, 6]]])
    plant('PLANT-RULE-OF', rule_of(z2) != 'std' and rule_of(z) == 'std', '(W1,0 with [xi, [3, 6]] added: %s; W1,0: %s)' % (rule_of(z2), rule_of(z)))


def size_choice(pr, facs):
    """the size criterion behind RULE_TAB: declare_big's largest table under col, colh and colb; col when col's is <= TMAX, else colh at
    G <= 3 and <= TMAX, else colb likewise, else colh. Returns (rule, {rule: (G, largest)})."""
    res = {}
    for r in ('col', 'colh', 'colb'):
        scal, idx = part_idx(r, facs)
        rows = pr.declare_big([[facs[i] for i in gp] for gp in idx], scal, None, None, None)
        res[r] = (len(idx), max(x[3] for x in rows))
    if res['col'][1] <= TMAX:
        return 'col', res
    for r in ('colh', 'colb'):
        if res[r][0] <= 3 and res[r][1] <= TMAX:
            return r, res
    return 'colh', res


def rule_size_check(graph, pr):
    """C-RULE-SIZE: for every bonded computed key of the family, size_choice equals rule_of. PLANT-RULE-SIZE: one key moved across (a
    RULE_TAB key offered as col, or a col key as colh) must disagree with size_choice."""
    bad, ch = [], {}
    for k in order_of(graph):
        e = entries_of(graph, [k])[0]
        if not any(x[0] == 'xi' for x in e['factors']):
            continue
        facs = facs_of(e)
        pr.qcap = qcap_of(pr, partition_of(e, facs), graph)[0]
        ch[k] = size_choice(pr, facs)
        if ch[k][0] != rule_of(e):
            bad.append('%s (size %s %s, pinned %s)' % (k, ch[k][0], ch[k][1], rule_of(e)))
    gate('C-RULE-SIZE', bool(ch) and not bad, '(%s: %d bonded computed keys, the size choice (col if its largest table <= %d moments, else colh '
         'or colb at G <= 3, else colh) equals RULE_TAB; failing %s)' % (graph, len(ch), TMAX, bad or 'none'))
    k = next((k for k in ch if rule_of(entries_of(graph, [k])[0]) != 'col'), next(iter(ch), None))
    moved = 'col' if k is not None and rule_of(entries_of(graph, [k])[0]) != 'col' else 'colh'
    plant('PLANT-RULE-SIZE', k is not None and ch[k][0] != moved, '(%s: %s moved to %s must disagree with its size choice %s)' % (
        graph, k, moved, ch[k][0] if k is not None else '-'))


def ab_ident(a, b):
    """C-AB's test: idok, (6a - 3)^2 holds 21 and (12b + 6a - 3)^2 holds 45, widths below 1e-15; sg, the lower ends of 6a - 3, 12b + 6a - 3,
    a and b above 0. Returns (idok and all(sg), idok, (6a - 3)^2, (12b + 6a - 3)^2, sg)."""
    u, w = 6 * a - 3, 12 * b + 6 * a - 3
    x, y = u ** 2, w ** 2
    idok = S.down(x) <= 21 <= S.up(x) and S.down(y) <= 45 <= S.up(y) and float(x.delta) < 1e-15 and float(y.delta) < 1e-15
    sg = (S.down(u) > 0, S.down(w) > 0, S.down(a) > 0, S.down(b) > 0)
    return idok and all(sg), idok, x, y, sg


def ab_check(graph):
    """as m3_run_r0b_v1_2 (C-AB, PLANT-AB, PLANT-AB-ROOT-A, PLANT-AB-ROOT-B)."""
    V, E = GR.strip(GRAPHS[graph]['columns'])
    tags = dict(((min(u, v), max(u, v)), t) for (u, v), t in E)
    vac = [c for c, ty in enumerate(GRAPHS[graph]['columns']) if ty == 'vac']
    okt = bool(vac) and all(tags.get((3 * c, 3 * c + 1)) == 'A' and tags.get((3 * c + 1, 3 * c + 2)) == 'A' and tags.get((3 * c, 3 * c + 2)) == 'B'
                            for c in vac)
    a, b = GR.coupling('A'), GR.coupling('B')
    ok, idok, x, y, sg = ab_ident(a, b)
    gate('C-AB', okt and ok, '(%s: vac columns %s tagged A, A, B: %s; identities %s (widths %.1e, %.1e); 6A - 3, 12B + 6A - 3, A, B > 0: %s)' % (
        graph, vac, okt, idok, float(x.delta), float(y.delta), sg))
    p1 = not ab_ident(GR.coupling(1), b)[0]
    plant('PLANT-AB', p1, '(coupling 1 in place of A: refused %s)' % p1)
    ra = ab_ident((3 - iv.sqrt(21)) / 6, (iv.sqrt(21) + 3 * iv.sqrt(5)) / 12)
    plant('PLANT-AB-ROOT-A', ra[1] and not ra[0], '(the other A root (3 - sqrt 21)/6 with B (sqrt 21 + 3 sqrt 5)/12: both identities hold %s; '
          'sign tests %s; refused %s)' % (ra[1], ra[4], not ra[0]))
    rb = ab_ident(a, -(3 * iv.sqrt(5) + iv.sqrt(21)) / 12)
    plant('PLANT-AB-ROOT-B', rb[1] and not rb[0], '(A right with the other B root -(3 sqrt 5 + sqrt 21)/12: both identities hold %s; sign tests '
          '%s; refused %s)' % (rb[1], rb[4], not rb[0]))


def family_graph(graph):
    """the family's GraphIV and C-GRAPH-LIST with its plant (as m3_run_v1_10_4 l.530-548, from the family's list)."""
    spec = GRAPHS[graph]
    V, E = GR.strip(spec['columns'])
    want = sorted(tuple(sorted(p)) for p in spec['pairs'])
    used = set()
    for e in entries_of(graph):
        for f in facs_of(e):
            used |= {tuple(sorted(p)) for p in ENT.pairs_of(f)}
    g = GR.GraphIV(V, E, want, NN)
    ok = V == 3 * len(spec['columns']) and g.F == spec['F'] and g.F == V + len(want) and len(set(want)) == len(want) and bool(used) and used <= set(want)
    gate('C-GRAPH-LIST', ok, '(%s: the columns %s give V %d and %d edges; the list\'s %d pairs %s, F %d (the list: %d); the entries use %d of them%s)' % (
        graph, spec['columns'], V, len(E), len(want), want, g.F, spec['F'], len(used & set(want)),
        '' if used <= set(want) else ('; NOT in the list: %s' % sorted(used - set(want)))))
    first = sorted(used)[0] if used else None
    plant('PLANT-GRAPH-LIST', first is not None and not (used <= set(want) - {first}), '(%s: the list\'s pairs without %r, a pair an entry uses)' % (graph, first))
    return g


def prep_params(g, s_rad=None):
    """m3ref_v1_15's prep rules on the certified graph: a_v = min(80 G_vv/300, 0.6) on the G_vv mids, ap = 0.7^2, theta0 the first argmin
    over np.linspace(0.01, 0.99, 197) of far_base's midpoint (m3ref_v1_15 l.918-929; any theta in (0, 1) is valid, m3_scal_v2.far_base)."""
    import numpy as np
    sr = RULE[0] if s_rad is None else s_rad
    mid = [(S.up(gv) + S.down(gv)) / 2 for gv in g.Gvv]
    a_v = [min(sr * m / 300, RULE[1]) for m in mid]
    ap = RULE[2] ** 2
    tree = g.tree()
    ths = np.linspace(0.01, 0.99, 197)
    vals = []
    for th in ths:
        fbv = S.far_base(300, float(th), ap, g.Gvv, tree, g.N, g.V, g.log_tau)
        vals.append((S.up(fbv) + S.down(fbv)) / 2)
    i0 = min(range(len(vals)), key=lambda i: vals[i])
    return {'a_v': a_v, 'ap': ap, 'theta0': float(ths[i0])}


def ref_prep_vg(vg, g=None):
    """the vertex graph's float reference PREPJSON: P9 m3ref_v1_10's V3E3, P12 m3ref_v1_14's P16H (the radii of S8's D16 H prep)."""
    return read_lines(os.path.join(OUTD, REFVG[vg][NN]), 'PREPJSON')[0]


def make_prep(vg, g, stages, scalars=None):
    """as m3_run_v1_10_4 l.570-588: C-RULE (PLANT-RULE), the Prep at dmaxH DMAXH[vg], C-TILT and C-PREP-REF."""
    rp = ref_prep_vg(vg, g)
    mid = [(S.up(gv) + S.down(gv)) / 2 for gv in g.Gvv]
    want = [min(RULE[0] * m / 300, RULE[1]) for m in mid]
    drule = max([abs(a - w) / w for a, w in zip(rp['a_v'], want)] + [abs(rp['ap'] - RULE[2] ** 2) / RULE[2] ** 2])
    gate('C-RULE', len(want) == len(rp['a_v']) and drule <= 1e-12, '(%s: the reference radii^2 = min(%g G_vv/300, %g) and rho\'^2 = %g^2, '
         'G_vv the certified mids: max relative difference %.1e (tol 1e-12))' % (vg, RULE[0], RULE[1], RULE[2], drule))
    bad = [min(1.01 * RULE[0] * m / 300, 1.01 * RULE[1]) for m in mid]
    plant('PLANT-RULE', not (max(abs(a - w) / w for a, w in zip(rp['a_v'], bad)) <= 1e-12), '(%s: 80 and 0.6 times 1.01)' % vg)
    pr = BAR.Prep(K, g, 300, rp['a_v'], rp['ap'], rp['theta0'], 6, log=out, dmaxH=DMAXH[vg], stages=stages, scalars=scalars)
    encl = [-iv.log(1 - S.I(a)) / (2 * S.I(a)) * (1 / S.I(300)) for a in rp['a_v']]
    gate('C-TILT', pr.ok and all(S.I(r) >= x.b for r, x in zip(pr.rates, encl)),
         '(a) %d tilt rates rounded up from their mp.iv enclosures; (b) both tilts certainly positive definite (lowest pivots %s, %s)' % (
             len(pr.rates), None if not pr.tilt_c else S.down(pr.tilt_c['low']), None if not pr.tilt_p else S.down(pr.tilt_p['low'])))
    gate('C-PREP-REF', rp['family'] == VGFAM[vg] and rp['N'] == NN and rp['J'] == 300, '(%s: %s PREPJSON of family %s, N %r, J %r, theta0 %r; '
         'dmaxH %d)' % (vg, REFVG[vg][NN], rp['family'], rp['N'], rp['J'], rp['theta0'], DMAXH[vg]))
    return pr, rp


def prep_param_check(vg, gp, rp):
    """C-PREP-PARAM: prep_params reproduces V3E3's PREPJSON (radii^2 1e-12, rho'^2 1e-15, theta0 exactly); PLANT-PREP-PARAM: 81 for 80."""
    pp = prep_params(gp)
    da = max(abs(a - b) / b for a, b in zip(pp['a_v'], rp['a_v']))
    gate('C-PREP-PARAM', len(pp['a_v']) == len(rp['a_v']) and da <= 1e-12 and abs(pp['ap'] - rp['ap']) <= 1e-15 and pp['theta0'] == rp['theta0'],
         '(%s: prep_params against %s: radii^2 max relative difference %.1e, rho\'^2 %r and %r, theta0 %r and %r)' % (
             vg, REFVG[vg][NN], da, pp['ap'], rp['ap'], pp['theta0'], rp['theta0']))
    p2 = prep_params(gp, s_rad=81.0)
    plant('PLANT-PREP-PARAM', max(abs(a - b) / b for a, b in zip(p2['a_v'], rp['a_v'])) > 1e-12, '(%s: radii by 81 G_vv/300)' % vg)


# ------------------------------------------------------------------ partitions per entry (R1's machinery; rules std, col, colb, colh)
def qcap_of(pr, p, graph):
    """(qcap, qmax): qmax the largest pair degree of the entry's F_i, qcap = max(the family's QCAP0, qmax)."""
    gds = [pr.gdata(gf) for gf in p['groups']]
    if not gds:
        return QCAP0[graph], 0
    Fi = pr.series_product([d['ser'] for d in gds], p['scal'], 3)
    qmax = max(BAR.qdeg(P, pr.g.V) for P in Fi)
    return max(QCAP0[graph], qmax), qmax


def ak_plan(pr, facs, grouping):
    """bound's a_k table request without a table: Dn and forms from the groups' series and the prep's Ej (m3_bar_v16_1 bound's own
    expressions, l.669-690)."""
    if grouping == 'std':
        scal, groups = BAR.group_factors(facs)
    else:
        scal, groups = grouping[1], [list(gf) for gf in grouping[2]]
    gds = [pr.gdata(gf) for gf in groups]
    Fi = pr.series_product([d['ser'] for d in gds], scal, 3)
    Dn = max(BAR.deg(Fi[i]) + BAR.deg(pr.Ej[k - i]) for k in range(4) for i in range(k + 1) if not BAR.is_zero(Fi[i]))
    use = sorted(set(sum((BAR.support(P) for P in Fi + pr.Ej), [])))
    return {'Dn': Dn, 'forms': use}


def col_key(rule, c, colt, vert):
    """a factor's group key under col, colxh, colb or colh: c its column (first vertex // 3), colt a column factor, vert a bond within c."""
    if rule == 'col':
        return (c, 0)
    if rule == 'colxh':
        return (c, 0 if colt else 1)
    if rule == 'colb':
        return (c, 0) if colt else (99, 1)
    return (c, 0) if colt or vert else (99, 1)


def part_idx(rule, facs):
    """as m3_run_v1_10_4 l.672-695 (std, col, colxh), with colb and colh (col_key)."""
    if rule == 'std':
        scal, groups = BAR.group_factors(facs)
        used, idx = set(), []
        for gf in groups:
            gi = []
            for f in gf:
                i = next(j for j in range(len(facs)) if facs[j] is f and j not in used)
                used.add(i)
                gi.append(i)
            idx.append(gi)
        return scal, idx
    if rule not in ('col', 'colxh', 'colb', 'colh'):
        raise ValueError('partition rule %r' % (rule,))
    if any(f[0] not in ('p', 'xi') for f in facs):
        raise ValueError('rule %s places only p and xi factors, not %s' % (rule, sorted(set(f[0] for f in facs))))
    grp = {}
    for i, f in enumerate(facs):
        c = f[1][0] // 3
        grp.setdefault(col_key(rule, c, is_column(f), f[1][1] // 3 == c), []).append(i)
    return 1, [grp[k] for k in sorted(grp)]


def part_enc(rule, encs):
    """C-PART-RULE's recomputation from the list's encodings alone: [p, c], [st, a, c], [cp, a, c] -> (3c, 3c + 1, 3c + 2), [xi, [u, v]] ->
    (u, v, v); std merges overlapping vertex sets in riglap4's order; col, colxh, colb and colh key by col_key. Returns the groups."""
    def trip(enc):
        if enc[0] in ('p', 'st', 'cp'):
            c = int(enc[-1])
            return (3 * c, 3 * c + 1, 3 * c + 2)
        if enc[0] == 'xi' and isinstance(enc[1], list) and len(enc[1]) == 2:
            return (int(enc[1][0]), int(enc[1][1]), int(enc[1][1]))
        raise ValueError('factor encoding %r' % (enc,))
    ts = [trip(x) for x in encs]
    if rule == 'std':
        groups = []
        for i, t in enumerate(ts):
            vs = set(t)
            hit = [gi for gi, (gv, gl) in enumerate(groups) if gv & vs]
            if not hit:
                groups.append((vs, [i]))
                continue
            gv, gl = groups[hit[0]]
            gv |= vs
            gl.append(i)
            for gi in sorted(hit[1:], reverse=True):
                gv |= groups[gi][0]
                gl.extend(groups[gi][1])
                groups.pop(gi)
        idx = [gl for gv, gl in groups]
    elif rule in ('col', 'colxh', 'colb', 'colh'):
        grp = {}
        for i, t in enumerate(ts):
            colt = t[1] == t[0] + 1 and t[2] == t[0] + 2 and t[0] % 3 == 0
            grp.setdefault(col_key(rule, t[0] // 3, colt, t[1] // 3 == t[0] // 3), []).append(i)
        idx = [grp[k] for k in sorted(grp)]
    else:
        raise ValueError('partition rule %r' % (rule,))
    return [[encs[i] for i in gp] for gp in idx]


def part_ok(idx, n):
    return bool(idx) and sorted(i for gp in idx for i in gp) == list(range(n)) and all(len(gp) > 0 for gp in idx)


def part_id(groups, facs):
    from collections import Counter
    return bool(groups) and all(len(gp) > 0 for gp in groups) and Counter(repr(f) for f in facs) == Counter(repr(f) for gp in groups for f in gp)


def partition_of(e, facs=None):
    """an entry's partition under rule_of (fields as m3_run_v1_10_4 l.753-761)."""
    facs = facs_of(e) if facs is None else facs
    rule = rule_of(e)
    scal, idx = part_idx(rule, facs)
    groups = [[facs[i] for i in gp] for gp in idx]
    return {'rule': rule, 'G': len(idx), 'idx': idx, 'groups': groups, 'enc': [[e['factors'][i] for i in gp] for gp in idx], 'scal': scal,
            'grouping': 'std' if rule == 'std' else ('partition', scal, groups)}


def part_line(name, p):
    return 'PARTITION %s rule %s: G %d: %s' % (name, p['rule'], p['G'], ' | '.join('{' + ', '.join(json.dumps(x) for x in gp) + '}' for gp in p['enc']))


def part_checks(e, facs, p):
    """the PARTITION line, C-PART-ID and C-PART-RULE (the groups against part_enc on the list's encodings) for one entry."""
    name = name_of(e)
    out(part_line(name, p))
    gate('C-PART-ID', part_ok(p['idx'], len(facs)) and part_id(p['groups'], facs) and p['G'] == len(p['groups']) == len(p['enc']),
         '(%s rule %s: the %d groups hold exactly the entry\'s %d factors as a multiset, none empty; G %d)' % (
             name, p['rule'], len(p['groups']), len(facs), p['G']))
    ind = part_enc(p['rule'], e['factors'])
    gate('C-PART-RULE', ind == p['enc'], '(%s: the groups against the rule %s recomputed from the list\'s encodings: %s)' % (
        name, p['rule'], 'equal' if ind == p['enc'] else 'DIFFERENT'))


def part_plants(graph, parts):
    """PLANT-PART-DROP, PLANT-PART-DUP and PLANT-PART-MOVE, once per item (m3_run_v1_10_4 l.783-820's generic cases). v1_2: when no group of
    any entry holds two factors (ES12C), PLANT-PART-MOVE merges groups 0 and 1 of the first entry with G >= 2."""
    names = list(parts)
    e, facs, p = parts[names[0]]
    gd = [list(gp) for gp in p['groups']]
    gd[0] = gd[0][1:]
    plant('PLANT-PART-DROP', not part_id(gd, facs), '(%s: its first group without its first factor %s)' % (names[0], p['enc'][0][0]))
    gd = [list(gp) for gp in p['groups']]
    gd[0].append(gd[0][0])
    plant('PLANT-PART-DUP', not part_id(gd, facs), '(%s with its first factor %s doubled)' % (names[0], p['enc'][0][0]))
    mv = next(((n, gi) for n in names for gi, gp in enumerate(parts[n][2]['idx']) if parts[n][2]['G'] >= 2 and len(gp) >= 2), None)
    if mv is not None:
        name, s = mv
        e, facs, p = parts[name]
        t = (s + 1) % p['G']
        idx2 = [list(gp) for gp in p['idx']]
        i0 = idx2[s].pop(0)
        idx2[t].append(i0)
        what = '%s moved from group %d to group %d' % (e['factors'][i0], s, t)
    else:
        name = next((n for n in names if parts[n][2]['G'] >= 2), None)
        if name is None:
            plant('PLANT-PART-MOVE', False, '(%s: no entry with G >= 2)' % graph)
            return
        e, facs, p = parts[name]
        idx2 = [list(p['idx'][0]) + list(p['idx'][1])] + [list(gp) for gp in p['idx'][2:]]
        what = 'its groups 0 and 1 merged (no group holds two factors)'
    g2 = [[facs[i] for i in gp] for gp in idx2]
    enc2 = [[e['factors'][i] for i in gp] for gp in idx2]
    idok = part_ok(idx2, len(facs)) and part_id(g2, facs)
    plant('PLANT-PART-MOVE', idok and enc2 != part_enc(p['rule'], e['factors']), '(%s with %s: C-PART-ID %s, C-PART-RULE must fail)' % (
        name, what, 'passes' if idok else 'FAILS'))


EXP_TARGET = {'ser': (Fraction(1, 2), Fraction(1, 4)), 'bar': (Fraction(1),), 'barp': (Fraction(1, 2),)}


def exp_ok(keys, G):
    """as m3_run_v1_10_4 l.826-842."""
    if G < 1:
        return False
    bp = set()
    for k in keys:
        if not k.startswith('g|'):
            continue
        _, gi, what, i, q, which = k.split('|')
        gi, q = int(gi), int(q)
        if gi >= G or what not in EXP_TARGET or q <= 0 or Fraction(G, q) not in EXP_TARGET[what]:
            return False
        if what == 'barp':
            bp.add(gi)
    return bp == set(range(G))


def exp_from(keys, G, H):
    """as m3_run_v1_10_4 l.845-854."""
    res = []
    for k in keys:
        if not k.startswith('g|'):
            res.append(k)
            continue
        _, gi, what, i, q, which = k.split('|')
        res.append('g|%s|%s|%s|%d|%s' % (gi, what, i, (int(q) // G) * H, which))
    return res


PPL = {'exp': True, 'akdrop': True}   # PLANT-PART-EXP and PLANT-AK-DROP, each once per item


def part_exp_check(name, p, keys):
    """as m3_run_v1_10_4 l.857-866: C-PART-EXP, PLANT-PART-EXP once per item."""
    G = p['G']
    gk = [k for k in keys if k.startswith('g|')]
    kinds = sorted(set((k.split('|')[2], int(k.split('|')[4])) for k in gk))
    gate('C-PART-EXP', exp_ok(keys, G), '(%s: G %d; %d group norms at (kind, exponent) %s; ser 2G and 4G, bar G, barp 2G for every group)' % (
        name, G, len(gk), kinds))
    if PPL['exp']:
        PPL['exp'] = False
        plant('PLANT-PART-EXP', not exp_ok(exp_from(keys, G, G - 1), G), '(%s: the same norms with exponents from G - 1 = %d)' % (name, G - 1))


def ak_only(pr, facs, grouping, label):
    """as m3_run_v1_10_4 l.869-881 (the a_k table may be a kept one)."""
    keep = (pr.ok, getattr(pr, 'gcache', {}), pr.ustate, pr.ubudget, pr.unit_done)
    pr.ok, pr.gcache, pr.ubudget, pr.unit_done = False, {}, None, None
    t0 = cpu()
    try:
        ak, _, info = pr.bound(facs, grouping, bars=False, entry=label)
    finally:
        pr.ok, pr.gcache, pr.ustate, pr.ubudget, pr.unit_done = keep
    return ak, info, cpu() - t0


def meets(x, y):
    return x.a <= y.b and y.a <= x.b


def ak_same(pr, name, p, ak, info, facs):
    """as m3_run_v1_10_4 l.889-901: C-AK-SAME and AK-ONLY-INFO; returns the standard a_k."""
    nt0 = len(pr.tables)
    akstd, inf2, dt = ak_only(pr, facs, 'std', name + ' (standard grouping, series only)')
    out('AK-ONLY-INFO %s: forms %s the partition run\'s, Dn %d (the partition run: %d), tables %d -> %d, %.2f s' % (
        name, 'equal to' if inf2['forms'] == info['forms'] else 'DIFFERENT from', inf2['Dn'], info['Dn'], nt0, len(pr.tables), dt))
    ov = [meets(x, y) for x, y in zip(ak, akstd)]
    w = max(abs(float(x.mid) - float(y.mid)) / max(1.0, abs(float(y.mid))) for x, y in zip(ak, akstd))
    gate('C-AK-SAME', len(ak) == len(akstd) == 4 and all(ov), '(%s rule %s: its a_k balls against the standard grouping\'s series-only a_k: '
         'overlap %s; largest mid difference / max(1, |a_k|) %.2e, INFO)' % (name, p['rule'], ov, w))
    return akstd


def ak_drop_plant(pr, e, facs, p, akstd):
    """PLANT-AK-DROP once per item (m3_run_v1_10_4 l.904-916): the partition without one xi factor, an st beside a p on its column when
    there is one (the entry's forms stay, so its kept a_k table serves), must give a_k that miss the standard a_k at some k."""
    if not PPL['akdrop']:
        return
    PPL['akdrop'] = False
    pcols = {f[1] for gp in p['groups'] for f in gp if f[0] == 'p'}
    cand = [(gi, j) for gi, gp in enumerate(p['groups']) for j, f in enumerate(gp) if f[0] == 'xi']
    gi, j = next(((gi, j) for gi, j in cand if p['groups'][gi][j][1] in pcols), cand[0])
    enc0 = p['enc'][gi][j]
    gd = [list(gp) for gp in p['groups']]
    gd[gi].pop(j)
    gd = [gp for gp in gd if gp]
    ak2, _, dt = ak_only(pr, facs, ('partition', p['scal'], gd), name_of(e) + ' (planted: %s dropped)' % enc0)
    ov = [meets(x, y) for x, y in zip(ak2, akstd)]
    plant('PLANT-AK-DROP', not all(ov), '(%s: its partition without the factor %s: overlap with the standard a_k %s; %.2f s)' % (name_of(e), enc0, ov, dt))


def gcache_ok(gc, grs, pairs):
    """as m3_run_v1_10_4 l.919-927."""
    keys = {repr(gf) for _, _, gf in grs}
    if not keys or not all(k in gc for k in keys):
        return False
    if len({id(gc[k]) for k in keys}) != len(keys):
        return False
    return all(repr(a) != repr(b) and gc[repr(a)] is not gc[repr(b)] for a, b in pairs)


def gcache_check(graph, pr, parts):
    """C-GCACHE, PLANT-GCACHE and PLANT-GCACHE-RUN (m3_run_v1_10_4 l.930-961's generic cases)."""
    gc = getattr(pr, 'gcache', {})
    grs = [(n, gi, gf) for n, (e, facs, p) in parts.items() for gi, gf in enumerate(p['groups'])]
    keys = sorted({repr(gf) for _, _, gf in grs})
    gate('C-GCACHE', gcache_ok(gc, grs, []), '(%s: %d groups of %d entries, %d distinct factor-tuple lists, each with its own entry under '
         'its repr)' % (graph, len(grs), len(parts), len(keys)))
    colkey = lambda gf: gf[0][1][0] // 3
    a = grs[0][2]
    f = a[0]
    f2 = (f[0], f[1], f[2] + 1.0, f[3]) if f[0] == 'xi' else (f[0], f[1], [x + 1e-3 for x in f[2]], f[3], f[4])
    b = [f2] + list(a[1:])
    plant('PLANT-GCACHE', colkey(a) == colkey(b) and repr(a) != repr(b), '(%s group %d and a copy with its first factor moved: one column key '
          '%r, different factor tuples)' % (grs[0][0], grs[0][1], colkey(a)))
    bad1 = dict(gc)
    bad1[keys[1]] = gc.get(keys[0])
    bad2 = {k: v for k, v in gc.items() if k != keys[0]}
    r1, r2 = gcache_ok(bad1, grs, []), gcache_ok(bad2, grs, [])
    plant('PLANT-GCACHE-RUN', not r1 and not r2, '(%s: the gate\'s test on the cache with two different tuple lists sharing one entry: %s; '
          'without one list\'s entry: %s)' % (graph, 'accepted' if r1 else 'refused', 'accepted' if r2 else 'refused'))


def laws_of(pr, mF):
    """as m3_run_v1_10_4 l.1017-1024."""
    g = pr.g
    cF = mF + Fraction(g.n * (g.V - 1), 2)
    rate = pr.alpha_lo - S.I(cF) / 300
    return {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, g.Gvv)]},
            'ann': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, pr.tilt_p['Gvv'])]},
            'far_rate': S.down(rate), 'far_cF': str(cF)}, rate


def has0(ak):
    return all(a.a <= 0 <= a.b for a in ak)


def ak_total_plants():
    """as m3_run_v1_10_4 l.1032-1040: PLANT-AK-TOTAL and PLANT-AK-ZERO."""
    bad = BAR.ak_failing([iv.mpf(['0.997', '1.003']), iv.mpf(['-1e-9', '1e-9']), iv.mpf(['0.9999999', '1.0000001'])], K.FALLBACK_REL)
    plant('PLANT-AK-TOTAL', bad == [0, 1], '(ak_failing at FALLBACK_REL %g on totals of radius 3e-3 |mid|, midpoint 0 and radius 1e-7 |mid|: '
          'refused %s, [0, 1] wanted)' % (K.FALLBACK_REL, bad))
    plant('PLANT-AK-ZERO', not has0([iv.mpf(['1e-9', '2e-9'])]) and has0([iv.mpf(['-1e-9', '2e-9'])]), '(has0 on [1e-9, 2e-9] must fail and '
          'on [-1e-9, 2e-9] pass)')


def norm_rel_plants():
    for n_, f_, l_ in BAR.rule_plants(K):
        plant(n_, f_, l_)


def ak_list(name, ak, fa):
    """AK-LIST-INFO: no list float (S8's E3 f,k meet ES9's W1,k in C-SMOKE-AK and C-S8-SAME)."""
    out('AK-LIST-INFO %s: no list float' % name)


def akest_s(graph):
    """a family's a_k-table CPU estimate: AKRATE x a table at F_ak forms (m3_bar_v16_1.table_moments)."""
    sp = GRAPHS[graph]
    return AKRATE * BAR.table_moments(int(sp['F_ak']), int(sp['D']), 3 * len(sp['columns']), QCAP0[graph])


def compute_entry(pr, e, state=None):
    """as m3_run_r0b_v1_2, with ak_list's INFO in place of C-AK-LIST."""
    name, graph = name_of(e), e['graph']
    t0 = cpu()
    STAGE[0] = 'entry %s' % name
    facs = facs_of(e)
    p = partition_of(e, facs)
    part_checks(e, facs, p)
    tq = cpu()
    pr.qcap, qmax = qcap_of(pr, p, graph)
    dq = cpu() - tq
    if pr.unit_done is not None:
        pr.unit_done(dq, False)
    out('QCAP %s: the largest pair degree of its F_i %d; qcap %d (the list\'s q_degree %d); qcap_of %.2f s' % (name, qmax, pr.qcap, QCAP0[graph], dq))
    pf = {'rule': p['rule'], 'G': p['G'], 'groups': p['enc'], 'qcap': pr.qcap}
    pr.maxrel = 0.0
    if e['parity'] == 'zero':
        ok, why = c_odd_h(graph, facs)
        gate('C-ODD', ok, '%s: %s' % (name, why))
        ak, _, info = pr.bound(facs, p['grouping'], bars=False, entry=name, state=state, ak_zero=True)
        gate('C-ODD-AK', has0(ak), '%s: every a_k ball contains 0 (widest %.1e)' % (name, max(float((a.b - a.a).b) for a in ak)))
        ak_list(name, ak, e['ak_float'])
        out('STAGE-CPU entry %s %.2f s (parity zero)%s' % (name, cpu() - t0, resumed(state)))
        return dict({'name': name, 'parity': 'zero', 'ak': ak, 'cpu': cpu() - t0, 'forms': info['forms']}, **pf)
    rows = pr.declare_big(p['groups'], p['scal'], *RULE_A[graph])
    out('BIGRULE-SET %s: %d norms declared; the big set %s' % (name, len(rows), ['%s forms %d D %d moments %d' % r[:4] for r in rows if r[4]]))
    ak, bars, info = pr.bound(facs, p['grouping'], entry=name, state=state)
    part_exp_check(name, p, list(pr.ustate['vals']))
    if p['rule'] != 'std':
        if pr.ubudget is not None and not pr.ubudget():   # every unit is done: the next piece restores them all and starts here
            pr.ustate['maxrel'] = pr.maxrel
            raise BAR.Checkpoint(pr.ustate)
        if state is not None and 'ak' in state['vals'] and getattr(pr, 'akest', None) is not None and not pr.akest(akest_s(graph)):
            pr.ustate['maxrel'] = pr.maxrel   # ak_only builds the restored 'ak' table afresh; the next piece starts here
            raise BAR.Checkpoint(pr.ustate)
        akstd = ak_same(pr, name, p, ak, info, facs)
        ak_drop_plant(pr, e, facs, p, akstd)
    laws, rate = laws_of(pr, info['mF'])
    gate('C-MONO-FAR', rate.a > 0, '%s: far rate alpha_min - (m_F + n(V-1)/2)/J_REF = %.4e > 0 (m_F %d)' % (name, S.down(rate), info['mF']))
    a0 = 1 if all(f[0] == 'p' for f in facs) else None
    rec = REC.entry_record(ak, bars, T_REF, 'free', a0_exact=a0, laws=laws)
    barsum = rec['Bp']['rem'] + rec['Bp']['tail'] + rec['Bp']['ann'] + rec['Bp']['far']
    okb = BAR.budget_ok(pr.maxrel, rec['B']['rnd'], barsum)
    gate('C-BUDGET', okb, '%s: largest relative radius of a norm %.3e (<= NORM_REL %g; big-rule norms out), rnd %.2e <= 0.1 x bar %.3e' % (
        name, pr.maxrel, BAR.NORM_REL, rec['B']['rnd'], barsum))
    over = BAR.cap_over(info['big'], INFL_CAP)
    gate('C-BIGCAP', not over, '%s: big-rule inflations at most %g (no exemption): over %s' % (name, INFL_CAP, over))
    out('BIGRULE-INFO %s: %d norms by the big-table rule, largest inflation %s' % (name, len(info['big']), BAR.infl_str(info['big_max'])))
    ak_list(name, ak, e['ak_float'])
    out('AKRAD-INFO %s: largest relative radius of an a_k %.2e' % (name, info.get('ak_relrad', 0.0)))
    out('ENTRY %s ak %s err %.9e parts rem %.9e tail %.9e ann %.9e far %.9e rnd %.3e groups %d Dn %d forms %d' % (
        name, ['%.12g' % x for x in rec['ak']], rec['err'], rec['B']['rem'], rec['B']['tail'], rec['B']['ann'], rec['B']['far'], rec['B']['rnd'],
        info['groups'], info['Dn'], len(info['forms'])))
    out('STAGE-CPU entry %s %.2f s%s' % (name, cpu() - t0, resumed(state)))
    return dict({'name': name, 'parity': 'free', 'ak': ak, 'bars': bars, 'a0_exact': a0, 'laws': laws, 'maxrel': pr.maxrel, 'big': info['big'],
                 'cpu': cpu() - t0, 'forms': info['forms']}, **pf)


def keep_ak(pr, r):
    """after an entry: its a_k table (key ('u', forms, True, ((1, qcap),)), as m3_bar_v16_1's bound requests it) stays for the next entry
    with the same forms and qcap; every other table is dropped (memory)."""
    key = ('u', tuple(r['forms']), True, ((1, r['qcap']),))
    hit = pr.tables.get(key)
    pr.tables.clear()
    if hit is not None:
        pr.tables[key] = hit


def plant_mono(pr):
    """PLANT-MONO: with theta0 = 1e-3 the far rate must not be certainly positive."""
    g = pr.g
    alpha = min((S.I(1e-3) * S.I(pr.ap) / (2 * gv)).a for gv in g.Gvv)
    rate = alpha - S.I(Fraction(g.n * (g.V - 1), 2)) / 300
    plant('PLANT-MONO', not (rate.a > 0), '(theta0 = 1e-3: far rate %.3e)' % S.down(rate))


def header(fam):
    return {'script': SELF_SHA, 'item': ITEM, 'family': fam, 'N': NN, 'kernel': '%s:%s' % (KERNEL, KFILES[KERNEL + '.py'][:8]),
            'arb_kernel': '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), 'trial': TRIAL, 'format': SNAME + ' hand-off'}


def same(x, y):
    """exact equality of hand-off values: intervals by their raw ends, containers recursively."""
    if hasattr(x, '_mpi_') or hasattr(y, '_mpi_'):
        return hasattr(x, '_mpi_') and hasattr(y, '_mpi_') and x._mpi_ == y._mpi_
    if isinstance(x, dict) and isinstance(y, dict):
        return set(map(str, x)) == set(map(str, y)) and all(same(x[k], y[str(k)] if str(k) in y else y[k]) for k in x)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        return len(x) == len(y) and all(same(a, b) for a, b in zip(x, y))
    return x == y


def write_handoff(fam, body):
    name = '%s_%s.json' % (SNAME, ITEM)
    path, hsha = HO.write(name, header(fam), body)
    out('HANDOFF %s %s' % (name, hsha))
    with open(path) as fh:
        text = fh.read()
    hdr_rt, body_rt = HO.read_text(text, {'script': SELF_SHA, 'item': ITEM, 'N': NN})
    gate('C-HANDOFF-RT', same(body, body_rt), '(the hand-off decodes to exactly the values written)')
    for lab, refused in HO.plant_handoff(text, {'script': SELF_SHA, 'item': ITEM, 'N': NN}):
        plant('PLANT-HANDOFF', refused, '(%s tampered in memory)' % lab)
    plant('PLANT-VERDICT', HO.plant_verdict(valid_verdict()), '(a producer record whose VERDICT line extends %r must be refused)' % valid_verdict())


def read_handoff(item, fam):
    name = '%s_%s.json' % (SNAME, item)
    hdr, body = HO.read(name, ACC.out(os.path.join(OUTD, '%s_%s.out' % (SNAME, item)), SELF_SHA, ORIG_SELF), {'script': ACC.expect(os.path.join(HANDD, name), SELF_SHA, ORIG_SELF), 'item': item, 'N': NN, 'family': fam},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (name, valid_verdict()))
    return body


def iv_leaves(v, lab=''):
    if isinstance(v, dict):
        return sum((iv_leaves(v[k], '%s[%s]' % (lab, k)) for k in sorted(v, key=str)), [])
    if isinstance(v, (list, tuple)):
        return sum((iv_leaves(x, '%s[%d]' % (lab, i)) for i, x in enumerate(v)), [])
    return [(lab, v)]


def prep_rep(vg, pr, rp, stg):
    """as m3_run_v1_10_4 l.1202-1218: PREP-REP (INFO; only P9 is staged here)."""
    if vg not in REFVG:
        out('PREP-REP %s stage %s: no float reference (prep_params, theta0 %r)' % (vg, stg, rp['theta0']))
        return
    keys = {'u': ('rE', 'rE_parts', 'nE', 'nE4'), 'c': ('nC8', 'nC6', 'Pout', 'Pout_p', 'farbase')}[stg]
    rows = []
    for k in keys:
        for lab, x in iv_leaves(getattr(pr, k)):
            f = rp[k]
            for part in [p for p in re.findall(r'\[([^\]]*)\]', lab)]:
                f = f[int(part)] if isinstance(f, list) else f[part]
            if isinstance(f, (int, float)) and f > 0:
                rows.append((S.up(x) / f, k + lab))
    rows.sort()
    if not rows:
        out('PREP-REP %s stage %s: no scalar with a positive float value' % (vg, stg))
        return
    out('PREP-REP %s stage %s: %d scalars, certified upper end / float in [%.6f (%s), %.6f (%s)]; %s' % (
        vg, stg, len(rows), rows[0][0], rows[0][1], rows[-1][0], rows[-1][1], '; '.join('%s %.6f' % (lab, r) for r, lab in rows)))


def prep_graph(g):
    """as m3_run_v1_10_4 l.1221-1224: the prep graph, F = V (C-PREP-GRAPH)."""
    return GR.GraphIV(g.V, list(g.edges), [], g.N, list(g.S_gauge))


def prep_view(G, pr):
    """as m3_run_v1_10_4 l.1227-1250: what the prep reads of a graph object (inputs, C-1 values, C-4 values)."""
    V = G.V
    vb = lambda M: [list(r[:V]) for r in M[:V]]
    tl = lambda T: None if T is None else {'Gam': vb(T['Gam']), 'Gvv': list(T['Gvv']), 'N': T['N']}
    tc, tp = G.tilted(pr.rates), G.tilted(pr.ratesp)
    ins = {'V': G.V, 'N': G.N, 'S_gauge': list(G.S_gauge), 'edges': [(tuple(e), c) for e, c in G.edges]}
    c1 = {'Gam': vb(G.Gam), 'Gvv': list(G.Gvv), 'log_tau': G.log_tau, 'log_det_Lr': G.log_det_Lr, 'W_int': [list(r[:V]) for r in G.W_int],
          'tilt_c': tl(tc), 'tilt_p': tl(tp)}
    c4 = None
    if tp is not None:
        th, ap = S.I(pr.theta0), S.I(pr.ap)
        try:
            tree = G.tree()
            c4 = {'Pout': S.isum(S.chi_tail_up(pr.J * S.I(a) / gv, G.n) for a, gv in zip(pr.a_v, G.Gvv)),
                  'Pout_p': S.isum(S.chi_tail_up(pr.J * S.I(a) / gv, G.n) for a, gv in zip(pr.a_v, tp['Gvv'])),
                  'tree': tree, 'farbase': S.far_base(pr.J, th, ap, G.Gvv, tree, G.N, G.V, G.log_tau),
                  'alpha_lo': min((th * ap / (2 * gv)).a for gv in G.Gvv)}
        except (ArithmeticError, ValueError) as ex:
            c4 = 'not formed (%s)' % type(ex).__name__
    return ins, c1, c4


VIEW_PARTS = ('inputs', 'C-1 values', 'C-4 values')


def view_diff(a, b):
    return [n_ for n_, x, y in zip(VIEW_PARTS, a, b) if not same(x, y)]


def prep_same(graph, g, gp, pr):
    """as m3_run_v1_10_4 l.1261-1295: C-PREP-GRAPH and its plants PLANT-PREP-EDGE, -TAG, -GAUGE and -ULP."""
    import types
    vg, vp = prep_view(g, pr), prep_view(gp, pr)
    d0 = view_diff(vg, vp)
    formed = isinstance(vg[2], dict) and isinstance(vp[2], dict)
    ok = gp.pairs == [] and gp.F == gp.V and formed and not d0
    gate('C-PREP-GRAPH', ok, '(%s: the prep graph (V %d, F %d, no pairs; the family graph F %d) against the family graph: inputs, C-1 and C-4 '
         'values exactly equal%s%s)' % (graph, gp.V, gp.F, g.F, ('; differ: ' + ', '.join(d0)) if d0 else '', '' if formed else '; C-4 not formed'))
    E, S0 = list(g.edges), list(g.S_gauge)
    t1 = 'B' if E[0][1] == 'A' else 'A'
    for lab, what, gx in (('PLANT-PREP-EDGE', 'its first edge %r dropped' % (E[0],), GR.GraphIV(g.V, E[1:], [], g.N, S0)),
                          ('PLANT-PREP-TAG', 'its first edge\'s tag %r changed to %r' % (E[0][1], t1),
                           GR.GraphIV(g.V, [(E[0][0], t1)] + E[1:], [], g.N, S0)),
                          ('PLANT-PREP-GAUGE', 'S_gauge [0]', GR.GraphIV(g.V, E, [], g.N, [0]))):
        dx = view_diff(vg, prep_view(gx, pr))
        plant(lab, bool(dx), '(%s: the prep graph with %s, against the family graph: differs in %s)' % (graph, what, ', '.join(dx) or 'nothing'))
    x = vp[1]['Gam'][0][1]
    mv = types.SimpleNamespace(_mpi_=tuple(libmp.mpf_add(r, libmp.from_man_exp(1, r[2]), 0) for r in x._mpi_))
    (a0, b0), (a1, b1) = [_ef(r) for r in x._mpi_], [_ef(r) for r in mv._mpi_]
    c1m = dict(vp[1], Gam=[list(r) for r in vp[1]['Gam']])
    c1m['Gam'][0][1] = mv
    dx = view_diff(vg, (vp[0], c1m, vp[2]))
    lap = a1 <= b0 and a0 <= b1
    plant('PLANT-PREP-ULP', bool(dx) and lap, '(%s: the prep view with Gam[0][1] moved up by one ulp of each end (overlapping: %s): differs in %s)' % (
        graph, lap, ', '.join(dx) or 'nothing'))


PACK_LIM = 9 * 10 ** 18   # the strictest table encoder: arbeng_c2b_v2's AllMom2A asserts float(D + 1)^F < 9.0e18 (the layer's _code_guard: 2^63)


def pack_ok(forms, D, lp):
    return (D + 1) ** forms < PACK_LIM and (not lp or D <= 64)


def pack_plan(pr, facs, grouping, info, bars):
    """as m3_run_v1_10_4 l.1306-1347: C-PACK-PLAN's requests for one entry, (what, forms, D, lp), from its polynomials (no table)."""
    import numpy as np
    use = info['forms']
    reqs = [('a_k', len(use), max(info['Dn'], 1), False)]
    if not bars:
        return reqs
    if isinstance(grouping, tuple) and len(grouping) == 3 and grouping[0] == 'partition':
        scal, groups = grouping[1], [list(gf) for gf in grouping[2]]
    elif grouping == 'std':
        scal, groups = BAR.group_factors(facs)
    else:
        raise ValueError('grouping %r' % (grouping,))
    G_ = max(len(groups), 1)
    gds = [pr.gdata(gf) for gf in groups]
    d0 = 2 * BAR.deg(pr.series_product([d['ser'] for d in gds], scal, 0)[0]) if groups else 0
    reqs.append(('m0u m0c', len(use), max(d0, 1), False))
    shape = {}

    def req(lab, P, p, pos):
        if id(P) not in shape:
            shape[id(P)] = (int(np.count_nonzero(P.ex.any(axis=0))), int(P.ex.sum(axis=1).max())) if len(P.ex) else (0, 0)
        nf, dq = shape[id(P)]
        r = (lab, nf, dq * p if pos else 2 * dq * (p // 2), not pos)
        if nf and r not in reqs:
            reqs.append(r)
    for i in (1, 2, 3):
        for c in BAR.comps(i, len(groups)):
            for gi, ig in enumerate(c):
                req('group %d ser %d p %d' % (gi, ig, 2 * G_), gds[gi]['ser'][ig], 2 * G_, False)
    for c in BAR.comps(0, len(groups)):
        for gi, ig in enumerate(c):
            req('group %d ser %d p %d' % (gi, ig, 4 * G_), gds[gi]['ser'][ig], 4 * G_, False)
    for c in BAR.comps(4, len(groups)):
        for gi, jg in enumerate(c):
            req('group %d bar %d p %d' % (gi, jg, G_), gds[gi]['bar'][jg], G_, True)
    for gi in range(len(gds)):
        req('group %d barp p %d' % (gi, 2 * G_), gds[gi]['barp'], 2 * G_, False)
    return reqs


def pack_gate(graph, plans):
    """as m3_run_v1_10_4 l.1350-1361: C-PACK-PLAN and PLANT-PACK-PLAN."""
    bad = [(nm, r) for nm, r in plans if not pack_ok(r[1], r[2], r[3])]
    nm, r = max(plans, key=lambda x: x[1][1] * math.log(x[1][2] + 1))
    lpm = max([x[1][2] for x in plans if x[1][3]] + [0])
    gate('C-PACK-PLAN', bool(plans) and not bad, '(%s: %d table requests of %d keys; the largest (D + 1)^forms %d^%d = %.3e (%s, %s) below %.1e; '
         'largest lp-norm D %d (<= 64))%s' % (graph, len(plans), len(set(x[0] for x in plans)), r[2] + 1, r[1], float(r[2] + 1) ** r[1], nm, r[0],
                                             PACK_LIM, lpm, (': refused ' + '; '.join('%s %s D %d over %d forms' % (x[0], x[1][0], x[1][2], x[1][1])
                                                                                     for x in bad[:10])) if bad else ''))
    plant('PLANT-PACK-PLAN', not pack_ok(16, 16, False) and pack_ok(16, 14, False), '(D 16 over 16 forms refused, D 14 over 16 forms accepted)')


def run_prep_stage(vg, stg):
    """as m3_run_r0b_v1_2 for P9 only (P12 reads S8's D16 H prep through foreign_scalars); C-PREP-PARAM at stage u."""
    if vg != 'P9':
        raise ValueError('only P9 is staged here, not %r' % (vg,))
    stage('%s prep stage %s' % (vg, stg))
    fams = [f for f in FAMS if VG[f] == vg]
    gs = {f: family_graph(f) for f in fams}
    gp = prep_graph(gs[fams[0]])
    pr, rp = make_prep(vg, gp, (stg,))
    if stg == 'u':
        for f in fams:
            prep_same(f, gs[f], gp, pr)
        prep_param_check(vg, gp, rp)
    prep_rep(vg, pr, rp, stg)
    body = {'vgraph': vg, 'stage': stg, 'families': fams, 'scal': pr.scalars_out(stg)}
    if stg == 'c':
        plant_mono(pr)
        out('PREP %s N=%d stage c: V %d, F %d; nC8 %.6e nC6 %.6e farbase %.6e alpha_lo %.6e' % (
            vg, NN, gp.V, gp.F, float(pr.nC8.mid), float(pr.nC6.mid), float(pr.farbase.b), float(pr.alpha_lo)))
    else:
        out('PREP %s N=%d stage u: V %d, F %d, theta0 %r; rE %.6e nE %s nE4 %s' % (vg, NN, gp.V, gp.F, rp['theta0'], float(pr.rE.mid),
                                                                              ['%.6e' % float(x.mid) for x in pr.nE], ['%.6e' % float(x.mid) for x in pr.nE4]))
    body['fallbacks'] = fb_info()
    write_handoff(vg, body)


def prep_scalars(vg):
    """as m3_run_v1_10_4 l.1392-1401 for P9: C-PREP-STAGES, both stages' scalars; P12: foreign_scalars (C-PREP-FOREIGN)."""
    if vg == 'P12':
        return foreign_scalars()
    su = read_handoff('%su.%d' % (vg, NN), vg)
    sc = read_handoff('%sc.%d' % (vg, NN), vg)
    ok = (su['vgraph'] == vg and sc['vgraph'] == vg and su['stage'] == 'u' and sc['stage'] == 'c' and set(su['scal']) == set(BAR.Prep.UK)
          and set(sc['scal']) == set(BAR.Prep.CK))
    gate('C-PREP-STAGES', ok, '(%s: %su.%d and %sc.%d, of %s and %s, scalars %s and %s)' % (vg, vg, NN, vg, NN, su['vgraph'], sc['vgraph'],
                                                                                         sorted(su['scal']), sorted(sc['scal'])))
    return dict(su['scal'], **sc['scal'])


CAPPED = 'VERDICT INCOMPLETE (CAP-STOP)'


def piece_state(graph, piece):
    """as m3_run_v1_10_4 l.1412-1429 with this script's names: 'valid', 'capped' or 'missing'; anything else raises ValueError."""
    item = '%sk%d.%d' % (PFX[graph], piece, NN)
    po = os.path.join(OUTD, '%s_%s.out' % (SNAME, item))
    ho = os.path.join(HANDD, '%s_%s.json' % (SNAME, item))
    if not os.path.exists(po):
        if os.path.exists(ho):
            raise ValueError('%s: a hand-off without its producer output' % item)
        return 'missing'
    if os.path.exists(ho):
        return 'valid'
    with open(po) as fh:
        lines = fh.read().split('\n')
    m = re.fullmatch(re.escape(SNAME) + r' item (\S+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)', lines[0])
    if m and m.group(1) == item and ACC.ok(po, m.group(3), SELF_SHA, ORIG_SELF) and HO.verdict_ok(lines, CAPPED):
        return 'capped'
    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)


def resumed(state):
    return (' (this piece; %d units of the entry restored)' % len(state['vals'])) if state else ''


def family_parts(graph):
    """the family's computed keys' partitions, name -> (entry, factors, partition), in order_of's order."""
    res = {}
    for name in order_of(graph):
        e = entries_of(graph, [name])[0]
        facs = facs_of(e)
        res[name] = (e, facs, partition_of(e, facs))
    return res


def run_nk(graph, piece):
    stage('%s keys piece %d' % (graph, piece))
    order = order_of(graph)
    g = family_graph(graph)
    scal = prep_scalars(VG[graph])   # the scalars of the family's vertex graph (C-PREP-STAGES; P12: C-PREP-FOREIGN)
    part_plants(graph, family_parts(graph))
    norm_rel_plants()
    start, caps, partial = 0, 0, None
    for j in range(piece - 1, 0, -1):
        st = piece_state(graph, j)
        if st == 'capped':
            caps += 1
            continue
        if st != 'valid':
            raise ValueError('%sk%d.%d is %s, so piece %d cannot start' % (PFX[graph], j, NN, st, piece))
        prev = read_handoff('%sk%d.%d' % (PFX[graph], j, NN), graph)
        start, partial = prev['next'], prev['partial']
        break
    factor = 1.5 * 2 ** caps
    nin = len(partial['vals']) if partial else 0
    out('PIECE-START %s piece %d resumes at entry %d of %d%s after %d capped piece(s); stop factor %.1f; LIM %d' % (
        graph, piece, start, len(order), (' with %d units of %s restored' % (nin, partial['entry'])) if partial else '', caps, factor, LIM))
    pr, rp = make_prep(VG[graph], g, (), scalars=scal)   # v10's Prep on the restored scalars
    slow, units = [60.0], [0]

    def budget():
        return units[0] == 0 or cpu() + factor * slow[0] <= LIM - 20

    def akest(est):
        """budget() with the slow estimate raised to est (an a_k table the piece has not built yet)."""
        return units[0] == 0 or cpu() + factor * max(slow[0], est) <= LIM - 20

    def done(dt, progress):
        """a unit's CPU raises the slow estimate, except an 'ak' unit (pr.cur_unit, set by m3_bar_v16_1._unit): its table is built once
        per piece and key, and akest covers a fresh one before each entry."""
        if not (progress and pr.cur_unit == 'ak'):
            slow[0] = max(slow[0], dt)
        if progress:
            units[0] += 1
    pr.ubudget, pr.unit_done, pr.akest = budget, done, akest
    res, i, part, prev_sig, est = [], start, None, None, akest_s(graph)
    while i < len(order):
        e = entries_of(graph, [order[i]])[0]
        sig = use_sig(e)
        if i > start and not akest(0.0 if sig == prev_sig else est):   # a fresh table's estimate, else none
            break
        try:
            r = compute_entry(pr, e, state=partial)
        except BAR.Checkpoint as cp:
            part = cp.state
            break
        res.append(r)
        partial, prev_sig = None, sig
        keep_ak(pr, r)
        i += 1
    pr.ubudget = pr.unit_done = pr.akest = None
    nout = len(part['vals']) if part else 0
    prog = i > start or (part is not None and nout > nin)
    gate('C-PIECE', prog, '(%s piece %d: entries %d..%d done, next %d of %d; %d units computed%s)' % (
        graph, piece, start, i - 1, i, len(order), units[0], (', %d units of %s carried' % (nout, part['entry'])) if part else ''))
    write_handoff(graph, {'family': graph, 'piece': piece, 'start': start, 'next': i, 'partial': part, 'stop_factor': factor,
                          'entries': res, 'fallbacks': fb_info()})


def run_smoke(graph):
    """as m3_run_es_v1_1 (Xa: the list checks, C-RULE-SIZE, the PLAN lines, AK-TABLE-PLAN) with v1_2's C-SMOKE-AK on SMOKE_KEY: ES9 and
    ES12A W1,0 against S8's E3 f,0 and H h,0 (every ball overlaps), ES12B and ES12C finite balls (relative widths INFO); PLANT-SMOKE-PATH:
    the p factor's q1 times 1 + 1e-6 on the partition rebuilt from the planted factors must miss S8's ball (ES9, ES12A) or move an a_k by
    more than 1e-9 (ES12B, ES12C). A P12 family reads the foreign prep first (C-PREP-FOREIGN and its plants) and runs v1_3's
    C-PREP-FOREIGN-C4 after C-PREP-GRAPH."""
    stage('smoke %s' % graph)
    list_check()
    enc_check()
    parity_set()
    alias_check()
    rule_of_check()
    ab_check(graph)
    g = family_graph(graph)
    scal = foreign_scalars() if VG[graph] == 'P12' else None
    pr, rp = make_prep(VG[graph], g, (), scalars=scal)
    prep_same(graph, g, prep_graph(g), pr)
    if VG[graph] == 'P12':
        foreign_c4_check(graph, g, pr, scal)
    STAGE[0] = 'smoke C-RULE-SIZE'
    rule_size_check(graph, pr)
    parts = family_parts(graph)
    plans, tabs = [], {}
    for name, (e, facs, p) in parts.items():
        STAGE[0] = 'smoke %s' % name
        part_checks(e, facs, p)
        t0 = cpu()
        pr.qcap, qmax = qcap_of(pr, p, graph)
        info = ak_plan(pr, facs, p['grouping'])
        key = (tuple(info['forms']), pr.qcap)
        tabs[key] = max(tabs.get(key, 0), info['Dn'])
        pl = pack_plan(pr, facs, p['grouping'], info, e['parity'] == 'free')
        top = max(pl, key=lambda r: r[1] * math.log(r[2] + 1))
        plans += [(name, r) for r in pl]
        line = 'PLAN %s: parity %s, rule %s, G %d, qcap %d (pair degree %d), a_k Dn %d over %d forms; %d table requests, the largest %d^%d (%s)' % (
            name, e['parity'], p['rule'], p['G'], pr.qcap, qmax, info['Dn'], len(info['forms']), len(pl), top[2] + 1, top[1], top[0])
        if e['parity'] == 'free':
            rows = pr.declare_big(p['groups'], p['scal'], *RULE_A[graph])
            risk = ['%s %d moments' % (r[0], r[3]) for r in rows if not r[4] and r[3] * 1.2e-4 > 300]
            line += '; big set %s; arb risk (moments x 1.2e-4 s > 300 s, arb) %s' % ([r[0] for r in rows if r[4]], risk or 'none')
        out(line + '; %.2f s' % (cpu() - t0))
    nvx = 3 * len(GRAPHS[graph]['columns'])
    tot = 0
    for (forms, q), Dm in sorted(tabs.items()):
        m = BAR.table_moments(len(forms), Dm, sum(1 for f in forms if f < nvx), q)
        tot += m
        out('AK-TABLE-PLAN %s: forms %d (%d pairs), D %d, qcap %d: %d moments, about %.0f s' % (graph, len(forms), sum(1 for f in forms if f >= nvx),
                                                                                          Dm, q, m, m * AKRATE))
    out('AK-TABLE-PLAN %s: %d distinct a_k tables, %d moments, about %.0f s if each is built once' % (graph, len(tabs), tot, tot * AKRATE))
    STAGE[0] = 'smoke C-SMOKE-AK'
    e, facs, p = parts[SMOKE_KEY[graph]]
    pr.qcap = qcap_of(pr, p, graph)[0]
    t0 = cpu()
    ak, _, info = pr.bound(facs, p['grouping'], bars=False, entry=SMOKE_KEY[graph])
    f0 = facs[0]
    facs2 = [(f0[0], f0[1], [x * (1 + 1e-6) for x in f0[2]], f0[3], f0[4])] + list(facs[1:])
    gr2 = 'std' if p['rule'] == 'std' else ('partition', p['scal'], [[facs2[i] for i in gp] for gp in p['idx']])
    ak2, _, _ = pr.bound(facs2, gr2, bars=False, entry=SMOKE_KEY[graph] + ' (planted)')
    dv = max(abs(float(x.mid) - float(y.mid)) / max(1.0, abs(float(y.mid))) for x, y in zip(ak2, ak))
    akl = ['%.12g' % float(a.mid) for a in ak]
    wid = ['%.1e' % (float((a.b - a.a).b) / max(1.0, abs(float(a.mid)))) for a in ak]
    if graph in S8OF:
        which = S8OF[graph]
        sb, ssha = s8_balls(which)
        pfx = S8REF[which][1]
        ov, ov2 = iv_meets(ak, sb[0][0], sb[0][1]), iv_meets(ak2, sb[0][0], sb[0][1])
        gate('C-SMOKE-AK', all(ov), '(%s %s: a_k %s against S8 %s %s,0 (%s %s): every ball overlaps: %s; widths / max(1, |a_k|) %s; %.2f s)' % (
            graph, SMOKE_KEY[graph], akl, which, pfx, S8REF[which][0][NN][0], ssha[:8], ov, wid, cpu() - t0))
        plant('PLANT-SMOKE-PATH', f0[0] == 'p' and not all(ov2), '(%s with its p factor\'s q1 times 1 + 1e-6 must miss S8\'s %s,0: overlap %s)' % (
            SMOKE_KEY[graph], pfx, ov2))
    else:
        fin = all(math.isfinite(float(a.a)) and math.isfinite(float(a.b)) for a in ak)
        gate('C-SMOKE-AK', fin, '(%s %s: a_k %s; every ball finite: %s; widths / max(1, |a_k|) %s (INFO); %.2f s)' % (
            graph, SMOKE_KEY[graph], akl, fin, wid, cpu() - t0))
        plant('PLANT-SMOKE-PATH', f0[0] == 'p' and dv > 1e-9, '(%s with its p factor\'s q1 times 1 + 1e-6 on the rebuilt partition: largest a_k '
              'change %.2e)' % (SMOKE_KEY[graph], dv))
    STAGE[0] = 'smoke plants'
    part_plants(graph, parts)
    gcache_check(graph, pr, parts)
    ak_total_plants()
    norm_rel_plants()
    pack_gate(graph, plans)
    fb_info()
