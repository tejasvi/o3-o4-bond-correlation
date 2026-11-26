# m3_run_r0b_v1_4_b.py -- pk04: the second part of m3_run_r0b_v1_4.py, executed in its namespace (it only defines). m3_run_r0b_v1_3.py's
# lines 1191-1531 with header(), write_handoff() and read_handoff() under item_src's names and shas (item_src and read_as new here).
def akest_s(graph):
    """a family's a_k-table CPU estimate: AKRATE x its table at the list's F, D and q_degree (m3_bar_v16_1.table_moments)."""
    sp = GRAPHS[graph]
    return AKRATE * BAR.table_moments(int(sp['F']), int(sp['D']), 3 * len(sp['columns']), QCAP0[graph])


def compute_entry(pr, e, state=None):
    """as m3_run_r0b_v1_2 (one computed key under its partition: checks, qcap, a_k, bars, C-PART-EXP, C-AK-SAME off std, C-MONO-FAR,
    C-BUDGET, C-BIGCAP, C-AK-LIST)."""
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
        gate('C-AK-LIST', ak_dev(ak, e['ak_float']) <= 1e-9, '%s: certified a_k mids against the list\'s ak_float %s: %.2e (tol 1e-9)' % (
            name, e['ak_float'], ak_dev(ak, e['ak_float'])))
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
    dv = ak_dev(ak, e['ak_float'])
    gate('C-AK-LIST', dv <= 1e-9, '%s: certified a_k mids against the list\'s ak_float: largest |mid - float| / max(1, |float|) %.2e (tol 1e-9)' % (name, dv))
    out('AKRAD-INFO %s: largest relative radius of an a_k %.2e' % (name, info.get('ak_relrad', 0.0)))
    out('ENTRY %s ak %s err %.9e parts rem %.9e tail %.9e ann %.9e far %.9e rnd %.3e groups %d Dn %d forms %d' % (
        name, ['%.12g' % x for x in rec['ak']], rec['err'], rec['B']['rem'], rec['B']['tail'], rec['B']['ann'], rec['B']['far'], rec['B']['rnd'],
        info['groups'], info['Dn'], len(info['forms'])))
    out('STAGE-CPU entry %s %.2f s%s' % (name, cpu() - t0, resumed(state)))
    return dict({'name': name, 'parity': 'free', 'ak': ak, 'bars': bars, 'a0_exact': a0, 'laws': laws, 'maxrel': pr.maxrel, 'big': info['big'],
                 'cpu': cpu() - t0, 'forms': info['forms']}, **pf)


def keep_ak(pr, r):
    """as m3_run_r0b_v1_2 (the entry's a_k table stays for the next entry with the same forms and qcap; other tables are dropped)."""
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
            'arb_kernel': '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), 'trial': TRIAL, 'format': '%s hand-off' % SNAME}


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
    """as m3_run_r0b_v1_3 under this script's name; an item item_src gives to m3_run_r0b_v1_3 is refused before anything is written."""
    if item_src(ITEM) != (SNAME, SELF_SHA):
        raise ValueError('%s is %s\'s item; this script writes the pieces above k%d only' % (ITEM, item_src(ITEM)[0], V13_PIECES))
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


def item_src(item):
    """(name, sha256) of an item's producer: this script for a family's pieces above k40 (V13_PIECES); m3_run_r0b_v1_3 under its pinned
    V13_SHA for every other item this script reads (VNu, VNc, VDu, VDc, W2r1, W2r2 and the pieces k1..k40)."""
    m = re.fullmatch(r'(%s)k([0-9]+)\.[34]' % FAMRE, item)
    return (SNAME, SELF_SHA) if m and int(m.group(2)) > V13_PIECES else (V13_NAME, V13_SHA)


def read_as(nm, item, fam):
    """item's hand-off read under the producer name nm: refused before any file is opened unless nm is item_src's name; then as
    m3_run_r0b_v1_3's read_handoff with item_src's sha as the header's script. Returns (name, sha, body)."""
    src, ssha = item_src(item)
    if nm != src:
        raise ValueError('%s_%s: %s is %s\'s item, not %s\'s' % (nm, item, item, src, nm))
    name = '%s_%s.json' % (nm, item)
    hdr, body = HO.read(name, ACC.out(os.path.join(OUTD, '%s_%s.out' % (nm, item)), ssha, ORIG_OF[ssha]), {'script': ACC.expect(os.path.join(HANDD, name), ssha, ORIG_OF[ssha]), 'item': item, 'N': NN, 'family': fam},
                        valid_verdict())
    return name, ssha, body


def read_handoff(item, fam):
    name, ssha, body = read_as(item_src(item)[0], item, fam)
    gate('C-HANDOFF', True, '(%s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header with script %s)' % (
        name, valid_verdict(), ssha[:8]))
    return body


def read_handoff_v18(item):
    """m3_run_v1_8_3's reader of m3_run_v1_8's N prep hand-offs (C-PREP-SAME), bound to V18_SHA and to its producer output."""
    name = 'm3_run_v1_8_%s.json' % item
    hdr, body = HO.read(name, ACC.out(os.path.join(OUTD, 'm3_run_v1_8_%s.out' % item), V18_SHA, ORIG_V18), {'script': ACC.expect(os.path.join(HANDD, name), V18_SHA, ORIG_V18), 'item': item, 'N': NN, 'family': 'N'},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: m3_run_v1_8\'s producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (
        name, valid_verdict()))
    return body


def iv_leaves(v, lab=''):
    if isinstance(v, dict):
        return sum((iv_leaves(v[k], '%s[%s]' % (lab, k)) for k in sorted(v, key=str)), [])
    if isinstance(v, (list, tuple)):
        return sum((iv_leaves(x, '%s[%d]' % (lab, i)) for i, x in enumerate(v)), [])
    return [(lab, v)]


def prep_cross(stg, scal):
    """as m3_run_v1_10_4 l.1182-1199: C-PREP-SAME (VN only) and PLANT-PREP-SAME."""
    ref = read_handoff_v18('N%s.%d' % (stg, NN))['scal']
    la, lb = iv_leaves(scal), iv_leaves(ref)
    labs = [k for k, _ in la] == [k for k, _ in lb]
    ok, nsame, worst = labs, 0, (0.0, '-')
    if labs:
        for (k, x), (_, y) in zip(la, lb):
            ok = ok and meets(x, y)
            nsame += x._mpi_ == y._mpi_
            worst = max(worst, (abs(float(x.mid) - float(y.mid)) / max(abs(float(y.mid)), 1e-300), k))
    gate('C-PREP-SAME', ok, '(VN stage %s against m3_run_v1_8\'s N%s.%d: %d scalars, labels %s, every one overlapping: %s; %d bit-identical; '
         'largest relative mid difference %.1e at %s)' % (stg, stg, NN, len(la), 'equal' if labs else 'DIFFERENT', ok, nsame, worst[0], worst[1]))
    (k0, x0), (_, y0) = la[0], lb[0]
    y1 = y0 + 10 * ((x0.b - x0.a) + (y0.b - y0.a)) + abs(y0.mid) * iv.mpf('1e-12') + iv.mpf('1e-300')
    plant('PLANT-PREP-SAME', not meets(x0, y1), '(%s: N\'s value moved by ten times both widths plus 1e-12 of its size)' % k0)


def prep_rep(vg, pr, rp, stg):
    """as m3_run_v1_10_4 l.1202-1218: PREP-REP (INFO)."""
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
    gate('C-PREP-GRAPH', ok, '(%s: the prep graph has V %d, F %d and pairs %r (the family graph: F %d); against the family graph, V, N, '
         'S_gauge and the %d edges with tags in order equal, and exactly (equal _mpi_ tuples) the %d x %d vertex block of Gam, %d G_vv, '
         'log_tau, log_det_Lr, W_int\'s vertex columns and tilted()\'s vertex Gam, G_vv and N at both rate vectors (C-1), and Pout, Pout_p, '
         'tree(), farbase and alpha_lo (C-4)%s%s)' % (graph, gp.V, gp.F, gp.pairs, g.F, len(g.edges), g.V, g.V, len(g.Gvv),
                                                      ('; differ: ' + ', '.join(d0)) if d0 else '',
                                                      '' if formed else '; C-4 values of the family and prep graphs: %r, %r' % (
                                                          vg[2] if not isinstance(vg[2], dict) else 'formed',
                                                          vp[2] if not isinstance(vp[2], dict) else 'formed')))
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
    plant('PLANT-PREP-ULP', bool(dx) and lap, '(%s: a copy of the prep graph\'s view with its vertex-block entry [0][1] moved up by one unit '
          'of each end\'s last bit (overlapping the original: %s), against the family graph: differs in %s)' % (graph, lap, ', '.join(dx) or 'nothing'))


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
    gate('C-PACK-PLAN', bool(plans) and not bad, '(%s: the bound of all %d computed keys asks the kernel for %d table requests, distinct within '
         'each key; the largest code range (D + 1)^forms is %d^%d = %.3e (%s, %s), below %.1e; the largest lp-norm D is %d (<= 64))%s' % (
             graph, len(set(x[0] for x in plans)), len(plans), r[2] + 1, r[1], float(r[2] + 1) ** r[1], nm, r[0], PACK_LIM, lpm,
             (': refused ' + '; '.join('%s %s D %d over %d forms' % (x[0], x[1][0], x[1][2], x[1][1]) for x in bad[:10])) if bad else ''))
    plant('PLANT-PACK-PLAN', not pack_ok(16, 16, False) and pack_ok(16, 14, False), '(a request of D 16 over 16 forms, 17^16 = %.3e, must '
          'be refused, and the control D 14 over 16 forms, 15^16 = %.3e, accepted)' % (17.0 ** 16, 15.0 ** 16))


def run_prep_stage(vg, stg):
    """as m3_run_v1_10_4 l.1364-1389 over this script's families: VGu.N / VGc.N, one prep stage, its hand-off."""
    stage('%s prep stage %s' % (vg, stg))
    fams = [f for f in FAMS if VG[f] == vg]
    gs = {f: family_graph(f) for f in fams}
    gp = prep_graph(gs[fams[0]])
    pr, rp = make_prep(vg, gp, (stg,))
    if stg == 'u':
        for f in fams:
            prep_same(f, gs[f], gp, pr)
    prep_rep(vg, pr, rp, stg)
    body = {'vgraph': vg, 'stage': stg, 'families': fams, 'scal': pr.scalars_out(stg)}
    if stg == 'c':
        plant_mono(pr)
        out('PREP %s N=%d stage c: V %d, F %d; nC8 %.6e nC6 %.6e farbase %.6e alpha_lo %.6e' % (
            vg, NN, gp.V, gp.F, float(pr.nC8.mid), float(pr.nC6.mid), float(pr.farbase.b), float(pr.alpha_lo)))
    else:
        out('PREP %s N=%d stage u: V %d, F %d, radii from %s, theta0 %r; rE %.6e nE %s nE4 %s' % (
            vg, NN, gp.V, gp.F, REFVG[vg][NN], rp['theta0'], float(pr.rE.mid), ['%.6e' % float(x.mid) for x in pr.nE],
            ['%.6e' % float(x.mid) for x in pr.nE4]))
    if vg == 'VN':
        prep_cross(stg, body['scal'])   # C-PREP-SAME against m3_run_v1_8's N stage
    body['fallbacks'] = fb_info()
    write_handoff(vg, body)


def prep_scalars(vg):
    """as m3_run_v1_10_4 l.1392-1401: C-PREP-STAGES; both stages' scalars."""
    su = read_handoff('%su.%d' % (vg, NN), vg)
    sc = read_handoff('%sc.%d' % (vg, NN), vg)
    ok = (su['vgraph'] == vg and sc['vgraph'] == vg and su['stage'] == 'u' and sc['stage'] == 'c' and set(su['scal']) == set(BAR.Prep.UK)
          and set(sc['scal']) == set(BAR.Prep.CK))
    gate('C-PREP-STAGES', ok, '(%s: %su.%d and %sc.%d, of %s and %s, scalars %s and %s)' % (vg, vg, NN, vg, NN, su['vgraph'], sc['vgraph'],
                                                                                         sorted(su['scal']), sorted(sc['scal'])))
    return dict(su['scal'], **sc['scal'])
