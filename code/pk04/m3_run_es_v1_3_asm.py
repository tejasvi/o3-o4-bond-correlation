"""m3_run_es_v1_3_asm.py -- pk04 (code/pk04/). A part of m3_run_es_v1_3.py, executed in the runner's namespace after its C-HASH
has checked these bytes against PARTS: the record writer and the piece walk, S8's reference balls, P12's foreign prep reader, the record
item checks and reader plants, resume, the MOCK export ESm and asm. m3_run_es_v1_2_asm.py (e03847bd) with the prep-graph check (a),
records written with exact decimals (jexact, C-DEC-EXACT), and the script's names
taken from the runner (SNAME, RECV); the runner's docstring has the detail. Defines only."""


def write_records(texts, paths, fails, nofire, tag, opener=open):
    """as m3_run_v1_10_4 l.1504-1517."""
    if fails or nofire or tag != '':
        return []
    for f in paths:
        if os.path.dirname(os.path.abspath(paths[f])) != OUTD or os.path.exists(paths[f]):
            raise ValueError('record path %s: outside out/ or already there' % paths[f])
    done = []
    for f in sorted(paths):
        with opener(paths[f], 'x') as fh:
            fh.write(texts[f])
        done.append((f, paths[f]))
    return done


def walk_pieces(graph, res):
    """C-PIECES: the pieces of a family cover its computed keys in order, each advancing, none left in progress; their entries go into
    res."""
    order, nxt, piece, nin = order_of(graph), 0, 1, 0
    while nxt < len(order) and piece <= MAXP[graph]:
        st = piece_state(graph, piece)
        if st == 'missing':
            break
        if st == 'capped':
            out('PIECE-CAPPED %sk%d.%d: a clean CAP-STOP of this script, no hand-off; skipped and kept' % (PFX[graph], piece, NN))
            piece += 1
            continue
        body = read_handoff('%sk%d.%d' % (PFX[graph], piece, NN), graph)
        pt = body['partial']
        nout = len(pt['vals']) if pt else 0
        okp = body['start'] == nxt and (body['next'] > nxt or nout > nin) and (pt is None or (body['next'] < len(order) and pt['entry'] == order[body['next']]))
        gate('C-PIECES', okp, '(%sk%d.%d: entries %d..%d complete%s)' % (PFX[graph], piece, NN, body['start'], body['next'] - 1,
                                                                          (', %d units of %s carried' % (nout, pt['entry'])) if pt else ''))
        for r in body['entries']:
            res[(graph, r['name'])] = r
        nxt, piece, nin = body['next'], piece + 1, nout
    gate('C-PIECES', nxt == len(order) and nin == 0, '(the %s pieces cover all %d computed %s keys, in order, none left in progress)' % (
        graph, len(order), graph))


def s8_balls(which):
    """S8's record of kind which, 'E3' or 'H' (m3_reader_v6_3.load under its asm output): {k: (lo, hi, parity, err)} of <x>,0..<x>,3 (x the
    record's prefix, f or h), and its sha256."""
    refs, pfx, _ = S8REF[which]
    rf, af = refs[NN]
    rec = RDR.load(os.path.join(OUTD, rf), os.path.join(OUTD, af), 300, NN)
    keys = ['%s,%d' % (pfx, k) for k in range(4)]
    return {k: (rec['balls'][x][0], rec['balls'][x][1], rec['laws'][x]['parity'], rec['laws'][x]['err']) for k, x in enumerate(keys)}, rec['sha256']


def iv_meets(ak, lo, hi):
    """per coefficient: the a_k interval (exact ends) meets [lo, hi]."""
    return [_ef(a._mpi_[0]) <= h and l <= _ef(a._mpi_[1]) for a, l, h in zip(ak, lo, hi)]


def item_meets(it, lo, hi, shift=Fraction(0)):
    """per coefficient: an item's [ak - ak_rad, ak + ak_rad] (exact; a_0 moved by shift) meets [lo, hi]."""
    res = []
    for k in range(4):
        a, r = Fraction(it['ak'][k]) + (shift if k == 0 else 0), Fraction(it['ak_rad'][k])
        res.append(a - r <= hi[k] and lo[k] <= a + r)
    return res


def foreign_ok(hdr, body, cols, item):
    """C-PREP-FOREIGN's test of one foreign prep hand-off: header script FSCRIPT, item, N, family H, this run's kernel and arb kernel,
    trial TRIAL; body done True, family H, the stage scalar sets BAR.Prep.UK and BAR.Prep.CK; cols, a consumer family's columns, FCOLS."""
    return (hdr.get('script') in ACC.pair(FSCRIPT, ORIG_FSCRIPT) and hdr.get('item') == item and hdr.get('N') == NN and hdr.get('family') == 'H'
            and hdr.get('kernel') in ACC.pair_if((FSCRIPT, ORIG_FSCRIPT), '%s:%s' % (KERNEL, KFILES[KERNEL + '.py'][:8]), '%s:%s' % (KERNEL, ORIG_K8[KERNEL])) and hdr.get('arb_kernel') in ACC.pair_if((FSCRIPT, ORIG_FSCRIPT), '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), '%s:%s' % (ARBK, ORIG_K8[ARBK]))
            and hdr.get('trial') == TRIAL and body.get('done') is True and body.get('family') == 'H' and isinstance(body.get('scal_u'), dict)
            and isinstance(body.get('scal_c'), dict) and set(body['scal_u']) == set(BAR.Prep.UK) and set(body['scal_c']) == set(BAR.Prep.CK)
            and list(cols) == FCOLS)


def foreign_src_ok(hcols, hrad, hdm, rp):
    """C-PREP-FOREIGN's source clauses: H's columns in S8_ENTRY_LIST_v2 (the producer's list) equal FCOLS; the radii of REFVG['P12'] equal
    the S8 H record's; the S8 H record's dmaxH equals DMAXH['P12']."""
    return hcols == FCOLS and all(rp[k] == hrad[k] for k in ('a_v', 'ap', 'theta0')) and hdm == DMAXH['P12']


def foreign_scalars():
    """P12's scalars, S8's D16 H prep: m3_run_v1_9_3's finished prep hand-off FOREIGN[NN], read by m3_handoff_v3.read under its producer
    output (VERDICT lines exactly ['VERDICT VALID'], the HANDOFF line's sha256, the END checksum, header script, item, N and family).
    C-PREP-FOREIGN: foreign_ok with every P12 family's columns, and foreign_src_ok. PLANT-PREP-FOREIGN: the trial ts sha256 flipped, done
    False and the L columns [vac, int, int, vac], each refused; PLANT-PREP-FOREIGN-SRC: the S8 H record's a_v[0] moved
    up by one ulp, H's columns [vac, int, int, vac] and dmaxH 18, each refused; PLANT-HANDOFF-FOREIGN: m3_handoff_v3.plant_handoff on its
    text. Returns dict(scal_u, **scal_c)."""
    fn, fo, item = FOREIGN[NN]
    expect = {'script': ACC.expect(os.path.join(HANDD, fn), FSCRIPT, ORIG_FSCRIPT), 'item': item, 'N': NN, 'family': 'H'}
    hdr, body = HO.read(fn, ACC.out(os.path.join(OUTD, fo), FSCRIPT, ORIG_FSCRIPT), expect, 'VERDICT VALID')
    with open(os.path.join(W4, 'S8_ENTRY_LIST_v2.json')) as fh:
        hcols = json.load(fh)['graphs']['H']['columns']
    with open(os.path.join(OUTD, S8H[NN][0])) as fh:
        hrec = json.load(fh)
    hrad, hdm = hrec['families']['H'], hrec.get('dmaxH')
    rp = ref_prep_vg('P12')
    srcok = foreign_src_ok(hcols, hrad, hdm, rp)
    fams = [g for g in FAMS if VG[g] == 'P12']
    ok = all(foreign_ok(hdr, body, GRAPHS[g]['columns'], item) for g in fams) and srcok
    gate('C-PREP-FOREIGN', ok, '(%s %s, producer %s: VERDICT lines exactly ["VERDICT VALID"], its HANDOFF sha256; header script %s, item %s, '
         'N %r, family %r, kernel %r, arb kernel %r, trial as this run %s; done %r, scalars %s and %s; columns of %s %s, FCOLS %s, H\'s columns '
         'in S8_ENTRY_LIST_v2 %s; radii of %s equal to %s\'s and its dmaxH %r = DMAXH %d: %s)' % (
             fn, INPUTS[(HANDD, fn)][:8], fo, str(hdr.get('script'))[:8], hdr.get('item'), hdr.get('N'), hdr.get('family'), hdr.get('kernel'),
             hdr.get('arb_kernel'), hdr.get('trial') == TRIAL, body.get('done'), sorted(body.get('scal_u') or []), sorted(body.get('scal_c') or []),
             '/'.join(fams), [GRAPHS[g]['columns'] for g in fams], FCOLS, hcols, REFVG['P12'][NN], S8H[NN][0], hdm, DMAXH['P12'], srcok))
    h2 = dict(hdr, trial=dict(hdr['trial'], ts=flip(hdr['trial']['ts'])))
    p1 = not foreign_ok(h2, body, FCOLS, item)
    p2 = not foreign_ok(hdr, dict(body, done=False), FCOLS, item)
    p3 = not foreign_ok(hdr, body, ['vac', 'int', 'int', 'vac'], item)
    plant('PLANT-PREP-FOREIGN', p1 and p2 and p3, '(the header\'s trial ts sha256 flipped: refused %s; done False: refused %s; the L columns '
          '[vac, int, int, vac]: refused %s)' % (p1, p2, p3))
    h3 = dict(hrad, a_v=[math.nextafter(hrad['a_v'][0], math.inf)] + list(hrad['a_v'][1:]))
    q1 = not foreign_src_ok(hcols, h3, hdm, rp)
    q2 = not foreign_src_ok(['vac', 'int', 'int', 'vac'], hrad, hdm, rp)
    q3 = not foreign_src_ok(hcols, hrad, 18, rp)
    plant('PLANT-PREP-FOREIGN-SRC', q1 and q2 and q3, '(the S8 H record\'s a_v[0] moved up by one ulp: refused %s; H\'s columns [vac, int, int, '
          'vac]: refused %s; the S8 H record\'s dmaxH 18: refused %s)' % (q1, q2, q3))
    with open(os.path.join(HANDD, fn)) as fh:
        text = fh.read()
    for lab, refused in HO.plant_handoff(text, expect):
        plant('PLANT-HANDOFF-FOREIGN', refused, '(%s: %s tampered in memory)' % (fn, lab))
    return dict(body['scal_u'], **body['scal_c'])


C4K = ('Pout', 'Pout_p', 'farbase', 'alpha_lo')   # the stage-c scalars prep_view recomputes on a graph (its C-4 values)


def foreign_c4_ok(gg, pr, scal):
    """The test: prep_view's C-4 values recomputed on the family graph gg with this run's radii, rho'^2, theta0, J and N equal the foreign
    stage-c scalars end for end (m3_bar_v16_1's Prep16.stage_c16 computes them with the same formulas, l.1309-1313)."""
    c4 = prep_view(gg, pr)[2]
    return isinstance(c4, dict) and all(same(c4[k], scal[k]) for k in C4K)


def foreign_c4_check(f, gg, pr, scal):
    """C-PREP-FOREIGN-C4 and PLANT-PREP-FOREIGN-C4: the prep with a_v[0] moved up by one ulp must break the equality."""
    import copy
    ok = foreign_c4_ok(gg, pr, scal)
    gate('C-PREP-FOREIGN-C4', ok, '(%s: %s recomputed on the family graph with this run\'s radii, rho\'^2, theta0, J and N equal the foreign '
         'hand-off\'s scal_c end for end: %s)' % (f, ', '.join(C4K), ok))
    p2 = copy.copy(pr)
    p2.a_v = [math.nextafter(pr.a_v[0], math.inf)] + list(pr.a_v[1:])
    plant('PLANT-PREP-FOREIGN-C4', not foreign_c4_ok(gg, p2, scal), '(%s: the prep with a_v[0] moved up by one ulp must break the equality)' % f)


def rec_part_ok(field, rk):
    """C-PART-REC's test of one record's field: its 16 keys with their windows' rule, part_enc groups, G and an int qcap >= QCAP0."""
    if set(field) != set(rk):
        return False
    for k, v in field.items():
        g, wk = rk[k]
        e = entries_of(g, [wk])[0]
        q = v.get('qcap')
        if (v.get('rule') != rule_of(e) or v.get('groups') != part_enc(rule_of(e), e['factors']) or v.get('G') != len(v.get('groups') or [])
                or isinstance(q, bool) or not isinstance(q, int) or q < QCAP0[g]):
            return False
    return True


ES_KEYS = ('class', 'd_L', 'mono', 'k', 'window', 'shape', 'factors', 'uses')


def es_items_ok(items, c_, dl, rk):
    """C-ES-ITEMS' test of one record's items: its 16 keys, the ES_KEYS fields as the list gives them, and each key's own use."""
    if set(items) != set(rk):
        return False
    for key, it in items.items():
        g, wk = rk[key]
        e = entries_of(g, [wk])[0]
        _, mono, k = key.split(',')
        mn = [m for m, s in MONO[c_].items() if s == mono]
        if (any(f not in it for f in ES_KEYS) or it['class'] != c_ or it['d_L'] != dl or it['mono'] != mono or it['k'] != int(k)
                or it['window'] != e['id'] or it['shape'] != e['shape'] or it['factors'] != e['factors'] or it['uses'] != e['uses'] or len(mn) != 1
                or '%s d_L %d %s cp_%d' % (c_, dl, mn[0], int(k)) not in e['uses']):
            return False
    return True


def reader_plants(text, name):
    """the reader plants of m3_run_v1_10_4 l.1688-1771 on one E_semi record's text; PLANT-PARZERO marks ES,e,1 a parity zero."""
    dd = json.loads(text)
    k0 = sorted(k for k in dd['items'] if dd['items'][k]['parity'] == 'free')[0]
    dd['items'][k0]['B'].pop('rnd')
    try:
        RDR._check_text(json.dumps(dd), 300, NN)
        plant('PLANT-FMT', False, '(record copy without one rnd)')
    except ValueError:
        plant('PLANT-FMT', True, '(record copy without one rnd)')
    dd2 = json.loads(text)
    kr = max((k for k in dd2['items'] if dd2['items'][k]['parity'] == 'free'), key=lambda k: sum(dd2['items'][k]['ak_rad']))
    dd2['items'][kr]['B']['rnd'] = 0.0
    try:
        RDR._check_text(json.dumps(dd2), 300, NN)
        plant('PLANT-RND', False, '(record copy with %s rnd = 0)' % kr)
    except ValueError:
        plant('PLANT-RND', sum(dd2['items'][kr]['ak_rad']) > 0, '(record copy with %s rnd = 0; its ak_rad sum %.1e)' % (kr, sum(dd2['items'][kr]['ak_rad'])))
    deny = dict(DENY)
    nx = 3 if NN == 4 else 4
    for lab, mut, jref, nexp in (('PLANT-READER-PRECERT', 'precert', 300, NN), ('PLANT-READER-KERNEL', 'kernel', 300, NN),
                                 ('PLANT-READER-PREC', 'prec', 300, NN), ('PLANT-LAYER-V1_1', 'arbeng_ma_v1_1.py', 300, NN),
                                 ('PLANT-LAYER-V1_2', 'arbeng_ma_v1_2.py', 300, NN), ('PLANT-LAYER-V1_4', 'arbeng_ma_v1_4.py', 300, NN),
                                 ('PLANT-READER-MOCK', 'mock_arbeng_v1_4.py', 300, NN), ('PLANT-LAYER-MIX', 'mix', 300, NN),
                                 ('PLANT-VALREC', 'valrec', 300, NN), ('PLANT-CLAIM', 'claim', 300, NN), ('PLANT-ARBK', 'arbk', 300, NN),
                                 ('PLANT-ARBB', 'arbb', 300, NN), ('PLANT-JREF', None, 150, NN), ('PLANT-N', None, 300, nx),
                                 ('PLANT-KIND', 'kind', 300, NN), ('PLANT-CLAIM-BALL', 'claimball', 300, NN),
                                 ('PLANT-CLAIM-BALL-MISSING', 'noclaimball', 300, NN)):
        dd3 = json.loads(text)
        if mut == 'precert':
            dd3['format'] = 'M3_RECORD_v1_PRECERT'
            dd3['claim'] = 'NOT CERTIFIED (PRECERT): ' + dd3['claim']
        elif mut == 'kernel':
            dd3['kernel_sha256'] = flip(dd3['kernel_sha256'])
        elif mut == 'prec':
            dd3['kernel_prec'] = 256
        elif mut in deny:
            dd3['kernel_file'], dd3['kernel_sha256'] = mut, deny[mut]
        elif mut == 'mix':
            dd3['kernel_file'], dd3['kernel_sha256'] = 'arbeng_ma_v1_3.py', '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be'
        elif mut == 'valrec':
            dd3['validation'] = dd3['validation'][:-1] + [flip(dd3['validation'][-1])]
        elif mut == 'claim':
            dd3['claim'] = dd3['claim'] + ' '
        elif mut == 'arbk':
            dd3['arb_kernel_sha256'] = flip(dd3['arb_kernel_sha256'])
        elif mut == 'arbb':
            dd3['arb_base_sha256'] = flip(dd3['arb_base_sha256'])
        elif mut == 'kind':
            dd3['items'][sorted(dd3['items'])[0]].pop('kind')
        elif mut == 'claimball':
            dd3['claim_ball'] = dd3['claim_ball'] + ' '
        elif mut == 'noclaimball':
            dd3.pop('claim_ball')
        what = mut or ('expected J_REF %d' % jref if jref != 300 else 'expected N %d' % nexp)
        try:
            RDR._check_text(json.dumps(dd3), jref, nexp)
            plant(lab, False, '(m3_reader_v6_3 must refuse the mutated record copy: %s)' % what)
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3 refuses the mutated record copy: %s)' % what)
    dz = json.loads(text)
    dz['items']['ES,e,1']['parity'] = 'zero'
    try:
        RDR._check_text(json.dumps(dz), 300, NN)
        plant('PLANT-PARZERO', False, '(m3_reader_v6_3 must refuse the record copy with ES,e,1 marked a parity zero)')
    except ValueError:
        plant('PLANT-PARZERO', True, '(m3_reader_v6_3 refuses the record copy with ES,e,1 marked a parity zero)')
    dh = tsha(text)
    try:
        RDR.loads(text, 'RECORD %s %s\nVERDICT VALID\n' % (name, dh), 300, NN, name)
        gate('C-BOUND-RT', True, '(m3_reader_v6_3.loads accepts the record text under an output that names it and ends VALID)')
    except ValueError as ex:
        gate('C-BOUND-RT', False, '(refused: %s)' % ex)
    for lab, otext in (('PLANT-BOUND-VERDICT', 'RECORD %s %s\nVERDICT VALID-PRECERT\n' % (name, dh)),
                       ('PLANT-BOUND-INVALID', 'RECORD %s %s\nVERDICT INVALID (C-REP-AK)\n' % (name, dh)),
                       ('PLANT-BOUND-TWO', 'RECORD %s %s\nVERDICT VALID\nVERDICT VALID\n' % (name, dh)),
                       ('PLANT-BOUND-SHA', 'RECORD %s %s\nVERDICT VALID\n' % (name, flip(dh))),
                       ('PLANT-BOUND-NONE', 'VERDICT VALID\n')):
        try:
            RDR.loads(text, otext, 300, NN, name)
            plant(lab, False, '(m3_reader_v6_3.loads must refuse this asm output)')
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3.loads refuses this asm output)')


def resume_chain():
    """as m3_run_v1_10_4 l.1774-1784: C-RESUME-CHAIN."""
    ok, why = True, []
    for graph in RESUME_FAMS:
        b1 = read_handoff('%sr1.%d' % (PFX[graph], NN), graph)
        b2 = read_handoff('%sr2.%d' % (PFX[graph], NN), graph)
        ok = ok and b1['resume_ok'] is True and b1['plant_fired'] is True and b2['resume_ok'] is True and b1['entry'] == b2['entry'] == RESUME_KEY[graph]
        why.append('%s on %s: part 1 cut %s resumed %s, PLANT-RESUME %s; part 2 cut after %d of %d units resumed %s' % (
            graph, b1['entry'], b1['cut'], 'identical' if b1['resume_ok'] else 'DIFFERENT', 'FIRES' if b1['plant_fired'] else 'DOES NOT FIRE',
            b2['cut'], b2['units'], 'identical' if b2['resume_ok'] else 'DIFFERENT'))
    gate('C-RESUME-CHAIN', ok, '(%s)' % '; '.join(why))


def run_resume(graph, part):
    """as m3_run_v1_10_4 l.1787-1856 (C-RESUME, PLANT-RESUME, C-RESUME-SAME) against the key's piece result."""
    stage('%s resume part %d' % (graph, part))
    if graph not in RESUME_FAMS:
        raise ValueError('%s is not in RESUME_FAMS %s' % (graph, RESUME_FAMS))
    res = {}
    walk_pieces(graph, res)
    scal = prep_scalars(VG[graph])
    g = family_graph(graph)
    pr, rp = make_prep(VG[graph], g, (), scalars=scal)
    e = entries_of(graph, [RESUME_KEY[graph]])[0]
    name = name_of(e)
    src = res[(graph, name)]
    facs = facs_of(e)
    p = partition_of(e, facs)
    gr = p['grouping']
    pr.qcap = qcap_of(pr, p, graph)[0]
    pr.declare_big(p['groups'], p['scal'], *RULE_A[graph])

    def run(state=None, cut=None):
        pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0
        cnt = [0]
        if cut is not None:
            pr.unit_done = lambda dt, prog: cnt.__setitem__(0, cnt[0] + (1 if prog else 0))
            pr.ubudget = lambda: cnt[0] < cut
        try:
            return pr.bound(facs, gr, entry=name, state=state), None
        except BAR.Checkpoint as cp:
            return None, HO.dec(json.loads(json.dumps(HO.enc(cp.state))))
        finally:
            pr.ubudget = pr.unit_done = None
    body = {'family': graph, 'part': part, 'entry': name}
    if part == 1:
        t0 = cpu()
        _, st = run(cut=3)
        keys = list(st['vals']) if st else []
        r1, _ = run(state=st) if st else (None, None)
        ok = keys == ['ak', 'm0u', 'm0c'] and r1 is not None and same(src['ak'], r1[0]) and same(src['bars'], r1[1])
        gate('C-RESUME', ok, '(%s part 1: cut after stage a, units %s, resumed with fresh caches: a_k and bars %s the piece result\'s; %.2f s)' % (
            name, keys, 'identical to' if ok else 'NOT identical to', cpu() - t0))
        r2 = None
        if st:
            bad = dict(st, vals=dict(st['vals']))
            bad['vals']['m0u'] = 2 * bad['vals']['m0u']
            r2, _ = run(state=bad)
        fired = r2 is not None and not same(src['bars'], r2[1])
        plant('PLANT-RESUME', fired, '(%s: the stage-a state with m0u doubled must change the bars; rem %s -> %s)' % (
            name, '%.9e' % S.up(src['bars']['rem']), ('%.9e' % S.up(r2[1]['rem'])) if r2 else 'no result'))
        body.update({'cut': keys, 'resume_ok': ok, 'plant_fired': fired})
    else:
        t0 = cpu()
        (ak0, b0, _), _ = run()
        seq = list(pr.ustate['vals'])
        oks = same(src['ak'], ak0) and same(src['bars'], b0)
        gate('C-RESUME-SAME', oks, '(%s straight, %d units, %.2f s: a_k and bars %s the piece result\'s)' % (
            name, len(seq), cpu() - t0, 'identical to' if oks else 'NOT identical to'))
        cutb = next(i for i, k in enumerate(seq) if k.endswith('|c'))
        t0 = cpu()
        _, st = run(cut=cutb)
        r3, _ = run(state=st) if st else (None, None)
        ok = st is not None and len(st['vals']) == cutb and r3 is not None and same(src['ak'], r3[0]) and same(src['bars'], r3[1])
        gate('C-RESUME', ok, '(%s part 2: cut after %d of %d units, before the first stage-c unit, resumed with fresh caches: a_k and bars %s '
             'the piece result\'s; %.2f s)' % (name, cutb, len(seq), 'identical to' if ok else 'NOT identical to', cpu() - t0))
        body.update({'cut': cutb, 'units': len(seq), 'resume_ok': ok and oks})
    pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0
    body['fallbacks'] = fb_info()
    write_handoff(graph, body)


def phi_tokens():
    """M2B_KV_v1's PIN_TRIAL tokens of this N (path under code/ : sha256), the trial vacuum's files."""
    with open(os.path.join(C2B, 'M2B_KV_v1.txt')) as fh:
        for ln in fh:
            if ln.startswith('PIN_TRIAL = '):
                return [t for t in ln[len('PIN_TRIAL = '):].strip().split(' ; ') if ('_N%d_' % NN) in t]
    return []


def phi_ok(toks):
    """C-G-PHI's test: two tokens, each 'path:sha256' whose file under code/ hashes to it and equals this run's own input pin."""
    if len(toks) != 2:
        return False
    for t in toks:
        p_, h_ = t.rsplit(':', 1)
        full = os.path.join(CODEDIR, p_)
        if not os.path.exists(full) or sha(full) != h_ or INPUTS.get((os.path.dirname(full), os.path.basename(full))) != h_:
            return False
    return True


def rec_name(c_, dl, tag=''):
    return 'm3_es_%s_dL%s_N%d_J300%s_%s.json' % (c_, 'm1' if dl == -1 else '0', NN, tag, RECV)


def shape_doc(s, fams):
    return {'name': s, 'V': 9 if s == 'V9' else 12, 'columns': GRAPHS[fams[0]]['columns'], 'families': {g: GRAPHS[g]['pairs'] for g in fams}}


def es_extra(c_, dl, s, fams, rk):
    """the top-level E_semi fields of a record, certified or MOCK (pk12's layout notes 21:26:29Z and 21:52:20Z)."""
    return {'entry_list': '%s:%s (t_esemi_list_v2 f5f0381b; C-LIST-RULE)' % (LF, INPUTS[(LISTD, LF)]), 'class': c_, 'd_L': dl,
            'shape': shape_doc(s, fams), 'orientation': ORIENT, 'norm_twin': 'ES,1,0', 'note': ES_NOTE,
            'monomials': dict((v, m) for m, v in MONO[c_].items()), 'windows': {key: '%s:%s' % gw for key, gw in rk[(c_, dl)].items()},
            'claim_ball': CLAIM_BALL, 'dmaxH': DMAXH[VG[fams[0]]]}


def es_item(base, c_, dl, key, e):
    """a record item: its window's entry item base with the E_semi fields of key ES,<mono>,<k> (C-ES-ITEMS reads them)."""
    _, mono, k = key.split(',')
    return dict(base, **{'class': c_, 'd_L': dl, 'mono': mono, 'k': int(k), 'window': e['id'], 'shape': e['shape'], 'factors': e['factors'],
                         'uses': e['uses']})


def kern_fields():
    return {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}


def engine_field():
    return {SNAME: SELF_SHA, 'parts': dict(PARTS), 'modules': dict(OWNMOD)}


def jexact(v):
    """the JSON text of v (json.dumps' separators and key order) with every float written as the exact decimal value of its binary64
    (decimal.Decimal(x), exponent form where Decimal uses one): a reader of the written decimals as exact rationals then sees the binary64
    values themselves, so every relation the writer rounded outward in binary64 holds for the decimals too."""
    from decimal import Decimal
    if v is None or isinstance(v, bool):
        return json.dumps(v)
    if isinstance(v, float):
        if not math.isfinite(v):
            raise ValueError('a non-finite float in a record: %r' % v)
        return str(Decimal(v))
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, dict):
        return '{' + ', '.join('%s: %s' % (json.dumps(str(k)), jexact(x)) for k, x in v.items()) + '}'
    if isinstance(v, (list, tuple)):
        return '[' + ', '.join(jexact(x) for x in v) + ']'
    raise TypeError('cannot write %r into a record' % type(v))


def dec_rel_ok(text):
    """C-DEC-EXACT's test: the record text's numbers read as exact rationals (json parse_float=Fraction) hold m3_reader_v6_3 _entry's
    relations exactly: every ak_rad and B part >= 0, Bp = B without rnd, rnd >= sum_k ak_rad_k 300^-k and err >= the sum of B for a free
    item, everything 0 for a parity zero. Returns (ok, smallest margin of the two inequalities, its key)."""
    d = json.loads(text, parse_float=Fraction)
    t = Fraction(1, 300)
    worst, wk = None, None
    for key, it in d['items'].items():
        B, Bp, rad = it['B'], it['Bp'], [Fraction(r) for r in it['ak_rad']]
        parts = [Fraction(B[p]) for p in ('rem', 'tail', 'ann', 'far', 'rnd')]
        if (set(B) != {'rem', 'tail', 'ann', 'far', 'rnd'} or set(Bp) != {'rem', 'tail', 'ann', 'far'} or any(x < 0 for x in parts)
                or any(r < 0 for r in rad) or any(Fraction(Bp[p]) != Fraction(B[p]) for p in ('rem', 'tail', 'ann', 'far'))):
            return False, None, key
        if it['parity'] == 'zero':
            if any(Fraction(x) != 0 for x in it['ak']) or any(r != 0 for r in rad) or any(x != 0 for x in parts) or Fraction(it['err']) != 0:
                return False, None, key
            continue
        m = min(Fraction(B['rnd']) - sum(r * t ** k for k, r in enumerate(rad)), Fraction(it['err']) - sum(parts))
        if worst is None or m < worst:
            worst, wk = m, key
        if m < 0:
            return False, m, key
    return True, worst, wk


def dec_check(named):
    """C-DEC-EXACT on each (name, text) and PLANT-DEC-EXACT once: the first text with the rnd of its free key of largest ak_rad sum set to 0
    (written by jexact) must fail the test."""
    for nm, text in named:
        ok, m, k = dec_rel_ok(text)
        gate('C-DEC-EXACT', ok, '(%s: its written decimals read as exact rationals hold rnd >= sum_k ak_rad_k 300^-k, err >= the sum of B, Bp = B '
             'without rnd, parity zeros exactly 0; smallest margin %s at %s)' % (nm, ('%.3e' % float(m)) if m is not None else '-', k))
    nm, text = named[0]
    d = json.loads(text)
    kr = max((k for k in d['items'] if d['items'][k]['parity'] == 'free'), key=lambda k: sum(d['items'][k]['ak_rad']))
    d['items'][kr]['B']['rnd'] = 0.0
    plant('PLANT-DEC-EXACT', not dec_rel_ok(jexact(d))[0], '(%s with %s rnd 0 must fail C-DEC-EXACT)' % (nm, kr))


def mock_laws(pr, facs):
    """a MOCK item's laws: laws_of on the mock prep, its alpha_lo by stage c's formula when the prep holds no scalars (the mock builds no
    stage), m_F from m3_bar_v16_1.sup_F."""
    if getattr(pr, 'alpha_lo', None) is None:
        pr.alpha_lo = min((S.I(pr.theta0) * S.I(pr.ap) / (2 * gv)).a for gv in pr.g.Gvv)
    return laws_of(pr, BAR.sup_F(facs, pr.J)[1])[0]


def mock_fmt_ok(text, name):
    """C-MOCK-FMT's test of one MOCK text (S8's MOCK path with m3_reader_v6_3): format M3_RECORD_v1_MOCK and the claim 'MOCK ' + the reader's
    certified claim, J_REF 300 and N, the kernel fields of one of the reader's validated layers with its arb kernel and base, and the
    reader's own item checks _items (the entry form, laws, rnd >= sum_k ak_rad_k 300^-k). Returns (ok, why)."""
    raw = json.loads(text)
    if raw.get('format') != 'M3_RECORD_v1_MOCK' or raw.get('claim') != 'MOCK ' + RDR.CERT_CLAIM:
        return False, 'format or claim'
    if raw.get('J_REF') != 300 or raw.get('N') != NN:
        return False, 'J_REF or N'
    if (raw.get('kernel_file'), raw.get('kernel_sha256'), raw.get('kernel_prec'), tuple(raw.get('validation') or ())) not in [
            (L_[0], L_[1], RDR.KERNEL_PREC, tuple(L_[2])) for L_ in RDR.VALIDATED_LAYERS]:
        return False, 'kernel fields'
    if (raw.get('arb_kernel_file'), raw.get('arb_kernel_sha256')) != RDR.ARB_KERNEL or (raw.get('arb_base_file'), raw.get('arb_base_sha256')) != RDR.ARB_BASE:
        return False, 'arb kernel or base'
    try:
        RDR._items(raw, name, 300, NN - 1)
    except ValueError as ex:
        return False, 'item check: %s' % ex
    return True, 'reads'


def run_mock():
    """ESm: MOCK records for MOCK_RECS in pk12's form (format M3_RECORD_v1_MOCK, claim 'MOCK ' + the certified claim, EXPORT_STATUS
    MOCK): the a_k balls by bound(bars=False), every bar part 0 (not computed); each item in the certified entry form (m3_record_v4's
    entry_record with zero bars: rnd and err the a_k rounding term, laws by mock_laws, alias_of null) with the E_semi fields; the top level
    as the certified records' (kernel fields, engine, es_extra, partition); texts by jexact. C-ES-ITEMS, C-SCOPE, C-MOCK-FMT and C-DEC-EXACT
    on every text, PLANT-MOCK-CERT (the certified parse must refuse it), PLANT-MOCK-FMT (v1_1's laws None must fail), PLANT-DEC-EXACT, then
    write_records and one line 'RECORD <name> <sha256>' per record (the binding the MOCK path reads, with VERDICT VALID)."""
    stage('mock export')
    list_check()
    enc_check()
    parity_set()
    rk = rec_keys()
    need = {}
    for c_, dl in MOCK_RECS:
        for g, wk in rk[(c_, dl)].values():
            need.setdefault(g, set()).add(wk)
    wins, pfield = {}, {}
    zb = {'rem': iv.mpf(0), 'tail': iv.mpf(0), 'ann': iv.mpf(0), 'far': iv.mpf(0)}
    for g in [f for f in FAMS if f in need]:
        pr, rp = make_prep(VG[g], family_graph(g), ())
        for name in [n for n in order_of(g) if n in need[g]]:
            e = entries_of(g, [name])[0]
            STAGE[0] = 'mock %s %s' % (g, name)
            facs = facs_of(e)
            p = partition_of(e, facs)
            pr.qcap = qcap_of(pr, p, g)[0]
            t0 = cpu()
            z = e['parity'] == 'zero'
            ak, _, info = pr.bound(facs, p['grouping'], bars=False, entry=name, ak_zero=z)
            if z:
                gate('C-ODD-AK', has0(ak), '%s %s: every a_k ball contains 0' % (g, name))
                wins[(g, name)] = REC.entry_record(None, None, T_REF, 'zero')
            else:
                a0 = 1 if all(f[0] == 'p' for f in facs) else None
                wins[(g, name)] = REC.entry_record(ak, zb, T_REF, 'free', a0_exact=a0, laws=mock_laws(pr, facs))
            pfield[(g, name)] = {'rule': p['rule'], 'G': p['G'], 'groups': p['enc'], 'qcap': pr.qcap}
            w = wins[(g, name)]
            out('MOCK-AK %s %s: a_k %s, radii %s, rnd %.2e; %.2f s' % (g, name, ['%.12g' % x for x in w['ak']], ['%.1e' % x for x in w['ak_rad']],
                                                                    w['B']['rnd'], cpu() - t0))
            keep_ak(pr, {'forms': info['forms'], 'qcap': pr.qcap})
    texts, paths, files = {}, {}, {}
    for c_, dl in MOCK_RECS:
        s = [x[2] for x in RECDEF if x[:2] == (c_, dl)][0]
        fams = sorted({rk[(c_, dl)][k][0] for k in rk[(c_, dl)]})
        items = {key: es_item(wins[(g, wk)], c_, dl, key, entries_of(g, [wk])[0]) for key, (g, wk) in sorted(rk[(c_, dl)].items())}
        files[(c_, dl)] = items
        extra = dict(es_extra(c_, dl, s, fams, rk), EXPORT_STATUS='MOCK', MOCK='TRUE',
                     partition={key: pfield[gw] for key, gw in sorted(rk[(c_, dl)].items())},
                     bars='not computed: every B and Bp part is 0, and rnd and err are the a_k rounding term only (no certified bar)')
        radii = {g: {k: ref_prep_vg(VG[g])[k] for k in ('a_v', 'ap', 'theta0')} for g in fams}
        top = REC.top_level(NN, 300, radii, TRIAL, engine_field(), TAG, kern_fields(), extra=extra)
        top['format'], top['claim'] = 'M3_RECORD_v1_MOCK', 'MOCK ' + RDR.CERT_CLAIM
        texts[(c_, dl)] = jexact(dict(top, items=items))
        paths[(c_, dl)] = os.path.join(OUTD, rec_name(c_, dl, '_MOCK'))
    gate('C-ES-ITEMS', all(es_items_ok(files[x], x[0], x[1], rk[x]) for x in MOCK_RECS), '(MOCK: every item carries class, d_L, mono, k, its '
         'window, shape, the window\'s factors and uses, and its own use among them)')
    gate('C-SCOPE', all(set(files[x]) == {'ES,%s,%d' % (m, k) for m in ('1', 'e', 'f', 'ef') for k in range(4)} for x in MOCK_RECS),
         '(MOCK: %d records, each with exactly the 16 keys ES,<mono>,<k>)' % len(MOCK_RECS))
    for x in MOCK_RECS:
        nm = os.path.basename(paths[x])
        ok, why = mock_fmt_ok(texts[x], nm)
        gate('C-MOCK-FMT', ok, '(%s: the MOCK path\'s checks and m3_reader_v6_3._items: %s; %d keys; %d bytes; sha256 %s)' % (
            nm, why, len(files[x]), len(texts[x]), tsha(texts[x])))
        try:
            RDR._check_text(texts[x], 300, NN, name=nm)
            plant('PLANT-MOCK-CERT', False, '(m3_reader_v6_3\'s certified parse must refuse %s)' % nm)
        except ValueError:
            plant('PLANT-MOCK-CERT', True, '(m3_reader_v6_3\'s certified parse refuses %s)' % nm)
    dec_check([(os.path.basename(paths[x]), texts[x]) for x in MOCK_RECS])
    x0 = MOCK_RECS[0]
    d0 = json.loads(texts[x0])
    k0 = sorted(k for k in d0['items'] if d0['items'][k]['parity'] == 'free')[0]
    d0['items'][k0]['laws'] = None
    okx = mock_fmt_ok(json.dumps(d0), 'planted')[0]
    plant('PLANT-MOCK-FMT', not okx, '(%s %d with %s\'s laws None, v1_1\'s MOCK form, must fail C-MOCK-FMT)' % (x0[0], x0[1], k0))
    written = write_records(texts, paths, FAILS, NOFIRE, TAG)
    if not written:
        out('MOCK NOT WRITTEN (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE] + ([] if TAG == '' else ['TAG %r' % (TAG,)])))
    for b, path in written:
        gate('C-WRITE', sha(path) == tsha(texts[b]), '(%s holds exactly its C-MOCK-FMT text)' % os.path.basename(path))
        out('RECORD %s %s' % (os.path.basename(path), sha(path)))
    fb_info()


def run_asm():
    stage('asm')
    list_check()
    enc_check()
    parity_set()
    alias_check()
    rule_of_check()
    res = {}
    for graph in FAMS:
        walk_pieces(graph, res)
    resume_chain()
    scals = {vg: prep_scalars(vg) for vg in ('P9', 'P12')}   # C-PREP-STAGES (P9's hand-offs) and C-PREP-FOREIGN (P12's), as the records name them
    for f in [g for g in FAMS if VG[g] == 'P12']:   # each P12 family graph against its prep graph, bound here
        STAGE[0] = 'asm prep graph %s' % f
        gg = family_graph(f)
        prp, _ = make_prep('P12', gg, (), scalars=scals['P12'])
        prep_same(f, gg, prep_graph(gg), prp)
        foreign_c4_check(f, gg, prp, scals['P12'])
    STAGE[0] = 'asm'
    toks = phi_tokens()
    gate('C-G-PHI', phi_ok(toks), '(M2B_KV_v1 13cc0d9a PIN_TRIAL tokens of N%d: %s; each file under code/ hashes to its token and to this '
         'run\'s pin)' % (NN, toks))
    plant('PLANT-G-PHI', not phi_ok(toks[:1] + [flip(toks[1])] if len(toks) == 2 else []), '(the second token with its sha256\'s last digit changed)')
    wins, pfield = {}, {}
    for graph in FAMS:
        for name in order_of(graph):
            e = entries_of(graph, [name])[0]
            r = res[(graph, name)]
            pfield[(graph, name)] = {'rule': r['rule'], 'G': r['G'], 'groups': r['groups'], 'qcap': r['qcap']}
            if e['parity'] == 'zero':
                if r['parity'] != 'zero':
                    raise ValueError('%s %s: marked zero, computed %s' % (graph, name, r['parity']))
                wins[(graph, name)] = REC.entry_record(None, None, T_REF, 'zero')
            else:
                wins[(graph, name)] = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=r['a0_exact'], laws=r['laws'])
    s8 = {}
    for which in ('E3', 'H'):
        refs, pfx, fam = S8REF[which]
        sb, ssha = s8_balls(which)
        s8[which] = ssha
        ws = [wins[(fam, 'W1,%d' % k)] for k in range(4)]
        ovs = {k: item_meets(ws[k], sb[k][0], sb[k][1]) for k in range(4)}
        okp = all(ws[k]['parity'] == sb[k][2] for k in range(4))
        er = ['%.3f' % (ws[k]['err'] / float(sb[k][3])) if sb[k][3] > 0 else '-' for k in range(4)]
        gate('C-S8-SAME', all(all(v) for v in ovs.values()) and okp, '(%s W1,k against S8 %s %s,k (%s %s), k = 0..3: every [ak - ak_rad, '
             'ak + ak_rad] meets S8\'s ball: %s; parities equal: %s; err / S8\'s err %s (INFO))' % (fam, which, pfx, refs[NN][0], ssha[:8], ovs,
                                                                                                   okp, er))
        w1 = ws[1]
        sh = 10 * (Fraction(w1['ak_rad'][0]) + (sb[1][1][0] - sb[1][0][0])) + Fraction(1, 10 ** 12)
        plant('PLANT-S8-SAME', not all(item_meets(w1, sb[1][0], sb[1][1], sh)), '(%s W1,1 with its a_0 moved by ten times both a_0 widths plus '
              '1e-12 must miss S8\'s %s,1)' % (fam, pfx))
    rk = rec_keys()
    tag = TAG
    eng = engine_field()
    kern = kern_fields()
    radii = lambda d: {k: d[k] for k in ('a_v', 'ap', 'theta0')}
    fsrc = 'pk11/out/%s:%s' % (TSF, INPUTS[(W4, TSF)])
    absrc = ('pk03/m3_graph_v3.py:%s: vac columns carry the tags A, A, B with A = (3 + sqrt 21)/6 and B = (3 sqrt 5 - sqrt 21)/12 exactly '
             '(m3_graph_v3.coupling; C-AB by (6A - 3)^2 = 21 and (12B + 6A - 3)^2 = 45 with 6A - 3, 12B + 6A - 3, A and B positive)' % OWNMOD['m3_graph_v3.py'])
    gs = {g: family_graph(g) for g in FAMS}
    texts, paths, files, okc = {}, {}, {}, []
    for c_, dl, s in RECDEF:
        fams = sorted({rk[(c_, dl)][k][0] for k in rk[(c_, dl)]})
        vg = VG[fams[0]]
        prep = {'vgraph': vg, 'radii_from': '%s:%s' % (REFVG[vg][NN], INPUTS[(OUTD, REFVG[vg][NN])]), 'dmaxH': DMAXH[vg]}
        if vg == 'P12':
            fn, fo, item = FOREIGN[NN]
            prep['foreign'] = {'handoff': '%s:%s' % (fn, INPUTS[(HANDD, fn)]), 'producer': '%s:%s' % (fo, INPUTS[(OUTD, fo)]),
                               'script': 'm3_run_v1_9_3.py:%s' % FSCRIPT, 'item': item, 'family': 'H',
                               'gates': 'C-PREP-FOREIGN, C-PREP-GRAPH and C-PREP-FOREIGN-C4 in this asm'}
        else:
            hs = {st: '%s_%s%s.%d.json' % (SNAME, vg, st, NN) for st in ('u', 'c')}
            prep['stages'] = {st: '%s:%s' % (h, sha(os.path.join(HANDD, h))) for st, h in hs.items()}
        items, field = {}, {}
        for key, (g, wk) in sorted(rk[(c_, dl)].items()):
            e = entries_of(g, [wk])[0]
            items[key] = es_item(wins[(g, wk)], c_, dl, key, e)
            field[key] = pfield[(g, wk)]
            okc.append(all(items[key][f] == wins[(g, wk)][f] for f in ('ak', 'ak_rad', 'B', 'Bp', 'err', 'parity', 'laws')))
        files[(c_, dl)] = (items, field)
        ws8 = 'E3' if s == 'V9' else 'H'
        extra = dict(es_extra(c_, dl, s, fams, rk), prep=prep, partition=field, g_phi=toks, f_source=fsrc, ab_source=absrc,
                     s8_same='%s:%s (C-S8-SAME on %s W1,k)' % (S8REF[ws8][0][NN][0], s8[ws8], S8REF[ws8][2]))
        top = REC.top_level(NN, 300, {g: radii(ref_prep_vg(VG[g], gs[g])) for g in fams}, TRIAL, eng, tag, kern, extra=extra)
        texts[(c_, dl)] = jexact(dict(top, items=items))
        paths[(c_, dl)] = os.path.join(OUTD, rec_name(c_, dl, tag))
    gate('C-COPY', all(okc) and len(okc) == 16 * len(RECDEF), '(%d record keys, each its window\'s computed item exactly)' % len(okc))
    r0 = RECDEF[0][:2]
    items0 = files[r0][0]
    bad0 = dict(items0)
    bad0['ES,e,1'] = dict(bad0['ES,e,1'], ak=[bad0['ES,e,1']['ak'][0] + 1e-9] + bad0['ES,e,1']['ak'][1:])
    plant('PLANT-COPY', bad0['ES,e,1']['ak'] != wins[rk[r0]['ES,e,1']]['ak'], '(%s %d ES,e,1 with its a_0 moved by 1e-9 must differ from its window)' % r0)
    gate('C-SCOPE', all(set(files[x[:2]][0]) == {'ES,%s,%d' % (m, k) for m in ('1', 'e', 'f', 'ef') for k in range(4)} for x in RECDEF),
         '(%d records, each with exactly the 16 keys ES,<mono>,<k>)' % len(RECDEF))
    plant('PLANT-SCOPE', not (set(list(items0)[1:]) == set(items0)), '(a record without one key)')
    gate('C-ES-ITEMS', all(es_items_ok(files[(c_, dl)][0], c_, dl, rk[(c_, dl)]) for c_, dl, s in RECDEF), '(every item carries class, d_L, mono, '
         'k, its window, shape, the window\'s factors and uses, and its own use among them)')
    bi = {k: dict(v) for k, v in items0.items()}
    bi['ES,f,2'] = dict(bi['ES,f,2'], k=1)
    plant('PLANT-ES-ITEMS', not es_items_ok(bi, r0[0], r0[1], rk[r0]), '(%s %d ES,f,2 carrying k 1)' % r0)
    gate('C-PART-REC', all(rec_part_ok(files[(c_, dl)][1], rk[(c_, dl)]) for c_, dl, s in RECDEF), '(each record\'s partition field: its 16 keys '
         'with their windows\' rules and groups, G, qcap >= QCAP0)')
    f0 = dict(files[r0][1])
    kx = next(k for k, v in f0.items() if v['G'] >= 2)
    f0[kx] = dict(f0[kx], groups=[f0[kx]['groups'][1], f0[kx]['groups'][0]] + f0[kx]['groups'][2:])
    plant('PLANT-PART-REC', not rec_part_ok(f0, rk[r0]), '(%s %d\'s field with %s\'s groups 0 and 1 swapped)' % (r0[0], r0[1], kx))
    for c_, dl, s in RECDEF:
        rd = RDR._check_text(texts[(c_, dl)], 300, NN, name=os.path.basename(paths[(c_, dl)]))
        it = files[(c_, dl)][0]
        okf = (all(rd['entries'][k] == (it[k]['ak'], it[k]['err']) for k in it) and set(rd['entries']) == set(it)
               and rd['top'].get('partition') == files[(c_, dl)][1] and es_items_ok(json.loads(texts[(c_, dl)])['items'], c_, dl, rk[(c_, dl)]))
        gate('C-FMT', okf, '(%s: %d keys read back exactly by m3_reader_v6_3 with the partition and item fields; %d bytes; sha256 %s)' % (
            os.path.basename(paths[(c_, dl)]), len(it), len(texts[(c_, dl)]), tsha(texts[(c_, dl)])))
    dec_check([(os.path.basename(paths[x[:2]]), texts[x[:2]]) for x in RECDEF])
    reader_plants(texts[r0], os.path.basename(paths[r0]))
    gate('C-PREC-ASM', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d before the write)' % flint.ctx.prec)
    opened = []

    def no_open(p, mode):
        opened.append(p)
        raise OSError('PLANT-NOWRITE: the writer opened %s' % p)
    refused = 0
    for fl, nf, tg in ((FAILS + ['PLANT-FORCED'], NOFIRE, tag), (FAILS, NOFIRE + ['PLANT-FORCED'], tag), (FAILS, NOFIRE, '_PRECERT')):
        try:
            if write_records(texts, paths, fl, nf, tg, opener=no_open) == []:
                refused += 1
        except OSError:
            pass
    plant('PLANT-NOWRITE', refused == 3 and not opened, '(write_records under a failed gate, an unfired plant and a PRECERT tag: %d of 3 refused, %d files opened)' % (
        refused, len(opened)))
    written = write_records(texts, paths, FAILS, NOFIRE, tag)
    if not written:
        out('RECORDS NOT WRITTEN (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE] + ([] if tag == '' else ['TAG %r' % (tag,)])))
    for b, path in written:
        gate('C-WRITE', sha(path) == tsha(texts[b]), '(%s holds exactly its C-FMT text)' % os.path.basename(path))
        out('RECORD %s %s' % (os.path.basename(path), sha(path)))
