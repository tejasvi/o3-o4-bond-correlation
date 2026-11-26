def use_sig(e):
    """the pair forms an entry's factors use, sorted (the family's Ej uses none, so this fixes its a_k table's forms)."""
    return tuple(sorted(set(tuple(sorted(p)) for f in facs_of(e) for p in ENT.pairs_of(f))))


def order_of(graph):
    """a family's computed keys (its aliases out) in pair-use order: by use_sig, then the most factors first, then the list's order."""
    es = [(i, e) for i, e in enumerate(entries_of(graph)) if name_of(e) not in ALIAS[graph]]
    return [name_of(e) for i, e in sorted(es, key=lambda ie: (use_sig(ie[1]), -len(ie[1]['factors']), ie[0]))]


def list_check():
    """as m3_run_r0b_v1_2 (C-LIST, PLANT-LIST)."""
    bad = []
    for g in FAMS:
        es = entries_of(g)
        keys = [name_of(e) for e in es]
        cnt = (sum(1 for e in es if e['role'] == 'certify'), sum(1 for e in es if e['role'] == 'check'))
        ok = (cnt == COUNTS[g] and len(set(keys)) == len(keys) and all(e['id'] == '%s:%s' % (g, name_of(e)) for e in es)
              and all(isinstance(e['ak_float'], list) and len(e['ak_float']) == 4 for e in es) and GRAPHS[g].get('K') == 3
              and any(name_of(e) == EMPTY[g] and e['role'] == 'certify' for e in es))
        if not ok:
            bad.append(g)
    gate('C-LIST', not bad, '(ROUTE0B 55dfd958, ROUTE0L0 44d4c44e, D4BULK 2633b1b9: certify + check keys %s; K 3; failing %s)' % (
        ', '.join('%s %d + %d' % (g, COUNTS[g][0], COUNTS[g][1]) for g in FAMS), bad or 'none'))
    plant('PLANT-LIST', sum(1 for e in entries_of('W2')[1:] if e['role'] == 'certify') != COUNTS['W2'][0], '(W2 without its first key)')


def beside_p(e):
    """every st factor of the entry sits beside a p factor on its column (the list's convention: st multiplies p, never replaces it)."""
    return all(any(y[0] == 'p' and int(y[1]) == int(x[2]) for y in e['factors']) for x in e['factors'] if x[0] == 'st')


def enc_check():
    """as m3_run_r0b_v1_2 (C-ENC, PLANT-ENC)."""
    e1 = [1.0] + [0.0] * 8
    pv = lambda c: ('p', (3 * c, 3 * c + 1, 3 * c + 2), list(TS.q[0]), list(TS.q[1]), list(TS.q[2]))
    got = [ENT.factor(TS, 'N', enc_of(x)) for x in (['st', 1, 0], ['p', 2], ['xi', [0, 3]], ['cp', 0, 0])]
    want = [('xi', (0, 1, 2), float(TS.S[0][1]), [float(TS.S[r][1]) for r in range(1, 10)]), pv(2), ('xi', (0, 3, 3), 0.0, e1), pv(0)]
    outp = []
    for e in V3:
        prs = set(tuple(sorted(p)) for p in GRAPHS[e['graph']]['pairs'])
        for f in facs_of(e):
            outp += ['%s %s' % (e['id'], p) for p in ENT.pairs_of(f) if tuple(sorted(p)) not in prs]
    bes = all(beside_p(e) for e in V3)
    gate('C-ENC', got == want and bes and not outp, '(the four sample encodings give the conventions\' tuples: %s; every st beside p: %s; pair '
         'forms outside the list pairs: %s)' % (got == want, bes, outp[:5] or 'none'))
    try:
        enc_of(['st', 0, 0])
        r0 = False
    except ValueError:
        r0 = True
    e2 = dict(entries_of('W2', ['G,0,1'])[0])
    e2['factors'] = [x for x in e2['factors'] if x != ['p', 0]]
    plant('PLANT-ENC', r0 and not beside_p(e2), '([st, 0, 0] refused: %s; W2 G,0,1 without [p, 0]: beside_p %s)' % (r0, beside_p(e2)))


def parity_set():
    """as m3_run_r0b_v1_2 (C-PARITY-SET, PLANT-ODD on W2 G,0,2 with S[1][2] + 1e-12)."""
    import copy
    got = {g: sorted(name_of(e) for e in entries_of(g) if c_odd_h(g, facs_of(e))[0]) for g in FAMS}
    marked = {g: sorted(name_of(e) for e in entries_of(g) if e['parity'] == 'zero') for g in FAMS}
    gate('C-PARITY-SET', all(got[g] == sorted(ZERO[g]) == marked[g] for g in FAMS), '(the keys whose factors pass C-ODD on their family '
         'graph: %s; ZERO and the marks equal: %s)' % ({g: v for g, v in got.items() if v}, all(sorted(ZERO[g]) == marked[g] for g in FAMS)))
    ts2 = copy.deepcopy(TS)
    ts2.S[1][2] = ts2.S[1][2] + 1e-12
    ok, why = c_odd_h('W2', facs_of(entries_of('W2', ['G,0,2'])[0], ts2))
    plant('PLANT-ODD', not ok, '(W2 G,0,2 with S[1][2] + 1e-12: %s)' % why)


def alias_check():
    """C-ALIAS: alias_all's result equals ALIASES, every check key has a source, no source is itself an alias, and W3e is mirror_ok.
    PLANT-ALIAS: W2 KE,0 is CE's identity twin, and with its bond moved to (2, 5) it must not be."""
    ok = (all(ALIAS[g] == ALIASES[g] for g in FAMS) and all(v[0] is not None for g in FAMS for v in ALIAS[g].values())
          and all(v[0] not in ALIAS[g] for g in FAMS for v in ALIAS[g].values()) and mirror_ok('W3e'))
    gate('C-ALIAS', ok, '(identity and mirror aliases recomputed from the factor tuples equal ALIASES: %s; not computed: %s)' % (
        all(ALIAS[g] == ALIASES[g] for g in FAMS), ', '.join('%s %d' % (g, len(ALIAS[g])) for g in FAMS)))
    e = dict(entries_of('W2', ['KE,0'])[0])
    e2 = dict(e, factors=[['xi', [2, 5]] if x == ['xi', [0, 3]] else x for x in e['factors']])
    ce = mkey(facs_of(entries_of('W2', ['CE'])[0]))
    plant('PLANT-ALIAS', mkey(facs_of(e)) == ce and mkey(facs_of(e2)) != ce, '(W2 KE,0 is CE\'s identity twin; with its bond moved to (2, 5) '
          'it must not be)')


def sym_map_check():
    """as m3_run_r0b_v1_2 (C-SYM-MAP, the structural test for the six mirror aliases; PLANT-SYM-MAP)."""
    import copy
    chk = {g: sorted(name_of(e) for e in entries_of(g) if e['role'] == 'check') for g in FAMS}
    bad = []
    for g in FAMS:
        mp = MIRRORS.get(g, {})
        if sorted(mp) != chk[g] or (mp and not mirror_ok(g)):
            bad.append(g)
            continue
        for c, t in mp.items():
            img = mkey([ENT.map_factor(f, mirror_map(g)) for f in facs_of(entries_of(g, [c])[0])])
            if img != mkey(facs_of(entries_of(g, [t])[0])):
                bad.append('%s %s' % (g, c))
    gate('C-SYM-MAP', not bad, '(the check keys %s mirror their MIRRORS keys exactly, couplings and list pairs mirror-invariant; failing %s)' % (
        {g: v for g, v in chk.items() if v}, bad or 'none'))
    ts2 = copy.deepcopy(TS)
    ts2.S[0][1] = ts2.S[0][1] + 1e-12
    img = mkey([ENT.map_factor(f, mirror_map('W3e')) for f in facs_of(entries_of('W3e', ['M,1,0,e2'])[0], ts2)])
    plant('PLANT-SYM-MAP', img != mkey(facs_of(entries_of('W3e', ['M,0,1,e1'])[0])), '(W3e M,1,0,e2 with S[0][1] + 1e-12: its mirror image '
          'must miss M,0,1,e1)')


def rule_of(e):
    """the partition rule: std without a bond; with one, RULE_TAB's colh or colb for its 34 keys, else col."""
    if not any(x[0] == 'xi' for x in e['factors']):
        return 'std'
    return RULE_TAB.get(e['graph'], {}).get(name_of(e), 'col')


RULES = ('std', 'col', 'colb', 'colh', 'colxh')


def rule_of_check():
    """C-RULE-OF: the computed keys take std exactly when they have no bond, and every RULE_TAB key is a bonded computed key of its family;
    PLANT-RULE-OF: W2 Z with [xi, [0, 3]] added must take a bonded rule, and Z itself std."""
    ks = [entries_of(g, [k])[0] for g in FAMS for k in order_of(g)]
    vals = [rule_of(e) for e in ks]
    comp = {(e['graph'], name_of(e)) for e in ks if any(x[0] == 'xi' for x in e['factors'])}
    tab = [(g, k) for g in RULE_TAB for k in RULE_TAB[g]]
    ok = (set(vals) <= set(RULES) and all((v == 'std') == (not any(x[0] == 'xi' for x in e['factors'])) for v, e in zip(vals, ks))
          and all(t in comp for t in tab))
    gate('C-RULE-OF', ok, '(%d computed keys: std %d, col %d, colh %d, colb %d; RULE_TAB keys %d, all bonded computed keys: %s)' % (
        len(ks), vals.count('std'), vals.count('col'), vals.count('colh'), vals.count('colb'), len(tab), all(t in comp for t in tab)))
    z = dict(entries_of('W2', ['Z'])[0])
    z2 = dict(z, factors=z['factors'] + [['xi', [0, 3]]])
    plant('PLANT-RULE-OF', rule_of(z2) != 'std' and rule_of(z) == 'std', '(W2 Z with [xi, [0, 3]] added: %s; Z: %s)' % (rule_of(z2), rule_of(z)))


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
    gate('C-AB', okt and ok, '(%s: vac columns %s tagged A, A, B: %s; (6A - 3)^2 in [%r, %r], (12B + 6A - 3)^2 in [%r, %r], widths %.1e, %.1e: '
         'identities %s; A in [%r, %r], B in [%r, %r]; 6A - 3 > 0, 12B + 6A - 3 > 0, A > 0, B > 0: %s)' % (
             graph, vac, okt, S.down(x), S.up(x), S.down(y), S.up(y), float(x.delta), float(y.delta), idok, S.down(a), S.up(a), S.down(b),
             S.up(b), sg))
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


def ref_prep_vg(vg):
    return read_lines(os.path.join(OUTD, REFVG[vg][NN]), 'PREPJSON')[0]


def make_prep(vg, g, stages, scalars=None):
    """as m3_run_v1_10_4 l.570-588: C-RULE (PLANT-RULE), the Prep, C-TILT and C-PREP-REF."""
    rp = ref_prep_vg(vg)
    mid = [(S.up(gv) + S.down(gv)) / 2 for gv in g.Gvv]
    want = [min(RULE[0] * m / 300, RULE[1]) for m in mid]
    drule = max([abs(a - w) / w for a, w in zip(rp['a_v'], want)] + [abs(rp['ap'] - RULE[2] ** 2) / RULE[2] ** 2])
    gate('C-RULE', len(want) == len(rp['a_v']) and drule <= 1e-12, '(%s: the reference radii^2 = min(%g G_vv/300, %g) and rho\'^2 = %g^2, '
         'G_vv the certified mids: max relative difference %.1e (tol 1e-12))' % (vg, RULE[0], RULE[1], RULE[2], drule))
    bad = [min(1.01 * RULE[0] * m / 300, 1.01 * RULE[1]) for m in mid]
    plant('PLANT-RULE', not (max(abs(a - w) / w for a, w in zip(rp['a_v'], bad)) <= 1e-12), '(%s: 80 and 0.6 times 1.01)' % vg)
    pr = BAR.Prep(K, g, 300, rp['a_v'], rp['ap'], rp['theta0'], 6, log=out, dmaxH=18, stages=stages, scalars=scalars)
    encl = [-iv.log(1 - S.I(a)) / (2 * S.I(a)) * (1 / S.I(300)) for a in rp['a_v']]
    gate('C-TILT', pr.ok and all(S.I(r) >= x.b for r, x in zip(pr.rates, encl)),
         '(a) %d tilt rates rounded up from their mp.iv enclosures; (b) both tilts certainly positive definite (lowest pivots %s, %s)' % (
             len(pr.rates), None if not pr.tilt_c else S.down(pr.tilt_c['low']), None if not pr.tilt_p else S.down(pr.tilt_p['low'])))
    gate('C-PREP-REF', rp['family'] == VGFAM[vg] and rp['N'] == NN and rp['J'] == 300, '(%s: %s PREPJSON of family %s, N %r, J %r)' % (
        vg, REFVG[vg][NN], rp['family'], rp['N'], rp['J']))
    return pr, rp


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
    """PLANT-PART-DROP, PLANT-PART-DUP and PLANT-PART-MOVE, once per item (m3_run_v1_10_4 l.783-820's generic cases)."""
    names = list(parts)
    e, facs, p = parts[names[0]]
    gd = [list(gp) for gp in p['groups']]
    gd[0] = gd[0][1:]
    plant('PLANT-PART-DROP', not part_id(gd, facs), '(%s: its first group without its first factor %s)' % (names[0], p['enc'][0][0]))
    gd = [list(gp) for gp in p['groups']]
    gd[0].append(gd[0][0])
    plant('PLANT-PART-DUP', not part_id(gd, facs), '(%s with its first factor %s doubled)' % (names[0], p['enc'][0][0]))
    name, s = next((n, gi) for n in names for gi, gp in enumerate(parts[n][2]['idx']) if parts[n][2]['G'] >= 2 and len(gp) >= 2)
    e, facs, p = parts[name]
    t = (s + 1) % p['G']
    idx2 = [list(gp) for gp in p['idx']]
    i0 = idx2[s].pop(0)
    idx2[t].append(i0)
    g2 = [[facs[i] for i in gp] for gp in idx2]
    enc2 = [[e['factors'][i] for i in gp] for gp in idx2]
    idok = part_ok(idx2, len(facs)) and part_id(g2, facs)
    plant('PLANT-PART-MOVE', idok and enc2 != part_enc(p['rule'], e['factors']), '(%s with %s moved from group %d to group %d: C-PART-ID %s, '
          'C-PART-RULE must fail)' % (name, e['factors'][i0], s, t, 'passes' if idok else 'FAILS'))


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
    gate('C-PART-EXP', exp_ok(keys, G), '(%s: G %d; %d group norms at (kind, exponent) %s; G x 1/q exactly 1/2, 1/4, 1 and 1/2 for ser 2G, ser '
         '4G, bar G and barp 2G, every group with its barp)' % (name, G, len(gk), kinds))
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
    """as m3_run_r0b_v1_2 (PLANT-AK-DROP once per item: the partition without one xi factor, an st beside a p when there is one)."""
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


BARPOS_PTS = ('X = 0', 'X = 1', 'X_f = 1 + (f mod 3)', 'X_f = 0 (f even), 2 (f odd)')


def barpos_points(nv):
    return [[0] * nv, [1] * nv, [1 + f % 3 for f in range(nv)], [0 if f % 2 == 0 else 2 for f in range(nv)]]


def poly_at(items, x):
    tot = iv.mpf(0)
    for ex_, c in items:
        t = c
        for i, k in enumerate(ex_):
            if k:
                t = t * (x[i] ** k)
        tot = tot + t
    return tot


def barpos_info(graph, pr, parts):
    """as m3_run_v1_10_4 l.984-1014: C-BARPOS-INFO and PLANT-BARPOS."""
    seen, nev, flagged, nneg, ncoef, t0 = set(), 0, [], 0, 0, cpu()
    for n, (e, facs, p) in parts.items():
        if p['G'] % 2 == 0:
            continue
        for gi, gf in enumerate(p['groups']):
            if repr(gf) in seen:
                continue
            seen.add(repr(gf))
            for j, P in enumerate(pr.gdata(gf)['bar']):
                if BAR.is_zero(P):
                    continue
                items = list(S.spoly_iv(P).items())
                ncoef += len(items)
                nneg += sum(1 for ex_, c in items if c.a < 0)
                for lab, x in zip(BARPOS_PTS, barpos_points(P.nv)):
                    nev += 1
                    v = poly_at(items, x)
                    if v.b < 0:
                        flagged.append('%s group %d Fbar_%d at %s: upper end %s' % (n, gi, j, lab, v.b))
    out('C-BARPOS-INFO %s: %d distinct groups of odd-G entries, %d evaluations of Fbar_0..4 at %s; certainly negative: %s; coefficients with '
        'a negative lower end %d of %d (%.2f s)' % (graph, len(seen), nev, list(BARPOS_PTS), '; '.join(flagged[:10]) if flagged else 'none',
                                                   nneg, ncoef, cpu() - t0))
    nv = pr.g.F
    e0, e1 = [0] * nv, [0] * nv
    e0[0], e1[1] = 1, 1
    pm = list(S.spoly_iv(S.spoly(K, {tuple(e0): 1, tuple(e1): -1}, nv)).items())
    neg = [lab for lab, x in zip(BARPOS_PTS, barpos_points(nv)) if poly_at(pm, x).b < 0]
    plant('PLANT-BARPOS', bool(neg), '(X_0 - X_1 flagged at %s)' % neg)


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


def ak_dev(ak, fa):
    """the largest |certified a_k mid - the list's ak_float| / max(1, |ak_float|) over k = 0..3."""
    return max(abs(float(a.mid) - x) / max(1.0, abs(x)) for a, x in zip(ak, fa))
