def walk_done(graph, res):
    """asmN: the VALID pieces of a family in order, each advancing (C-PIECES as m3_run_v1_8's walk_pieces, capped pieces skipped), without
    requiring them to cover the family; their completed entries go into res. Returns (the next entry index, units carried)."""
    order, nxt, piece, nin = order_of(graph), 0, 1, 0
    while nxt < len(order) and piece <= MAXP[graph]:
        st = piece_state(graph, piece)
        if st == 'missing':
            break
        if st == 'capped':
            out('PIECE-CAPPED %sk%d.%d: a clean CAP-STOP of m3_run_v1_8, no hand-off; skipped and kept' % (PFX[graph], piece, NN))
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
    out('PIECES-DONE %s: entries 0..%d of %d complete in VALID pieces%s' % (
        graph, nxt - 1, len(order), (', %d units of %s carried and not used' % (nin, order[nxt])) if nin else ''))
    return nxt, nin


def scope_n():
    """route B's N-family keys (option 3, from pk11's kt_s8_cert_v1_11 l.487-492 and s8core_v1_8_2 l.1120-1147): every
    T,a,b of the list's N graph and the TX,a,b with max(a, b) <= 3, in the list's order."""
    keys = []
    for e in LIST['entries']:
        if e['graph'] != 'N':
            continue
        kind, a, b = e['key'].split(',')
        if kind == 'T' or (kind == 'TX' and max(int(a), int(b)) <= 3):
            keys.append(e['key'])
    return keys


def run_asm():
    stage('asm N, route B scope')
    res = {}
    nxt, nin = walk_done('N', res)
    order = order_of('N')
    scope = scope_n()
    done = set(name for gr, name in res if gr == 'N')
    nT = sum(1 for k in scope if k.startswith('T,'))
    nX = sum(1 for k in scope if k.startswith('TX,'))
    gate('C-SCOPE-N', len(scope) == 65 and nT == 55 and nX == 10 and set(scope) <= set(order) and set(scope) <= done,
         '(route B scope: %d keys of the list\'s N family, %d T,a,b and %d TX,a,b with max(a, b) <= 3, every one complete in a VALID '
         'piece; %d of %d N entries complete)' % (len(scope), nT, nX, len(done), len(order)))
    plant('PLANT-SCOPE-N', not (set(scope + [order[-1]]) <= done), '(the scope with %s, the family\'s last entry, added must not be complete)' % order[-1])
    if not set(scope) <= done:
        return
    refs = {'N': {}}
    for p in ref_files('N'):
        with open(p) as fh:
            lines = fh.read().split('\n')
        okv = HO.verdict_ok(lines, 'VERDICT VALID') and [ln for ln in lines if ln.startswith('TRIAL')] == ['TRIAL z9sym']
        gate('C-HASH-REF', okv, '(%s, sha256 %s: VERDICT lines exactly [VERDICT VALID], TRIAL lines exactly [TRIAL z9sym])' % (
            os.path.basename(p), sha(p)))
        for d in read_lines(p, 'KEYJSON'):
            refs['N'][d['key']] = d
    sel = [x for x in V3 if x['graph'] == 'N' and name_of(x) in set(scope)]
    files = {'N': {}}
    for e in sel:
        r = res[('N', name_of(e))]
        if r['parity'] == 'zero':
            files['N'][name_of(e)] = REC.entry_record(None, None, T_REF, 'zero')
        else:
            files['N'][name_of(e)] = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=r['a0_exact'], laws=r['laws'])
    gate('C-SCOPE', set(files['N']) == set(scope), '(the N record holds exactly the %d route-B keys, %d of them parity zeros)' % (
        len(files['N']), sum(1 for v in files['N'].values() if v['parity'] == 'zero')))
    plant('PLANT-SCOPE', not (set(list(files['N'])[1:]) == set(scope)), '(the N record without one key)')
    rep, rak = [], []
    for e in sel:
        r = res[('N', name_of(e))]
        if r['parity'] == 'zero':
            continue
        it = files['N'][name_of(e)]
        d = refs['N'][name_of(e)]
        for p in ('rem', 'tail', 'ann', 'far'):
            if d['B'][p] > 0:
                rep.append((it['B'][p] / d['B'][p], name_of(e), p))
        for k, (a, fa) in enumerate(zip(r['ak'], d['ak'])):
            rak.append((abs(float(a.mid) - fa) / max(1.0, abs(fa)), name_of(e), k))
    lo_, hi_ = min(rep), max(rep)
    gate('C-REP-B', 1 - 1e-6 <= lo_[0] and hi_[0] <= 1.15, '(%d bar parts against m3ref_v1_10 z9sym: certified/float in [%.9f (%s %s), %.6f (%s %s)])' % (
        len(rep), lo_[0], lo_[1], lo_[2], hi_[0], hi_[1], hi_[2]))
    plant('PLANT-REPB', not (1 - 1e-6 <= lo_[0] * 0.5), '(the smallest ratio times 0.5)')
    wr = max(rak)
    gate('C-REP-AK', wr[0] <= 1e-9, '(%d a_k against m3ref_v1_10 z9sym: largest |certified mid - float| / max(1, |float|) %.2e at %s a_%d)' % (
        len(rak), wr[0], wr[1], wr[2]))
    plant('PLANT-REPAK', not (wr[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')
    # the text, C-FMT on the text, the plants, and only then the write
    tag = TAG
    eng = {'m3_run_v1_8_2': SELF_SHA, 'entries_by': 'm3_run_v1_8.py:' + V18_SHA, 'modules': dict(OWNMOD)}
    kern = {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}
    fams = {'N': {k: ref_prep('N')[k] for k in ('a_v', 'ap', 'theta0')}}
    extra = {'entry_list': 'S8_ENTRY_LIST_v3.json:%s' % INPUTS[(W4, 'S8_ENTRY_LIST_v3.json')], 'graph': 'N', 'graph_m3': GMAP['N'],
             'scope': ('NARROWED to route B (option 3): the 55 T,a,b and the 10 TX,a,b with max(a, b) <= 3 of '
                       'S8_ENTRY_LIST_v3\'s N family; the 45 TX,a,b with a state >= 4 are not in this record, and nothing here certifies them'),
             'scope_keys': sorted(scope)}
    top = REC.top_level(NN, 300, fams, TRIAL, eng, tag, kern, extra=extra)
    texts = {'N': json.dumps(dict(top, items=files['N']))}
    paths = {'N': os.path.join(OUTD, 'm3_s8v3_N_N%d_J300%s_v1_8_2.json' % (NN, tag))}
    rd = RDR.check_text(texts['N'], 300, NN, name=os.path.basename(paths['N']))
    okf = all(rd['entries'][k] == (files['N'][k]['ak'], files['N'][k]['err']) for k in files['N'])
    gate('C-FMT', okf, '(%s: %d keys read back exactly from the text by m3_reader_v4_4; %d bytes; sha256 %s)' % (
        os.path.basename(paths['N']), len(files['N']), len(texts['N']), tsha(texts['N'])))
    dd = json.loads(texts['N'])
    k0 = sorted(k for k in dd['items'] if dd['items'][k]['parity'] == 'free')[0]
    dd['items'][k0]['B'].pop('rnd')
    try:
        RDR.check_text(json.dumps(dd), 300, NN)
        plant('PLANT-FMT', False, '(N copy without one rnd)')
    except ValueError:
        plant('PLANT-FMT', True, '(N copy without one rnd)')
    dd2 = json.loads(texts['N'])
    kr = max((k for k in dd2['items'] if dd2['items'][k]['parity'] == 'free'), key=lambda k: sum(dd2['items'][k]['ak_rad']))
    dd2['items'][kr]['B']['rnd'] = 0.0
    try:
        RDR.check_text(json.dumps(dd2), 300, NN)
        plant('PLANT-RND', False, '(N copy with %s rnd = 0)' % kr)
    except ValueError:
        plant('PLANT-RND', sum(dd2['items'][kr]['ak_rad']) > 0, '(N copy with %s rnd = 0; its ak_rad sum %.1e)' % (kr, sum(dd2['items'][kr]['ak_rad'])))
    deny = dict(DENY)
    nx = 3 if NN == 4 else 4
    for lab, mut, jref, nexp in (('PLANT-READER-PRECERT', 'precert', 300, NN), ('PLANT-READER-KERNEL', 'kernel', 300, NN),
                                 ('PLANT-READER-PREC', 'prec', 300, NN), ('PLANT-LAYER-V1_1', 'arbeng_ma_v1_1.py', 300, NN),
                                 ('PLANT-LAYER-V1_2', 'arbeng_ma_v1_2.py', 300, NN), ('PLANT-CLAIM', 'claim', 300, NN),
                                 ('PLANT-ARBK', 'arbk', 300, NN), ('PLANT-ARBB', 'arbb', 300, NN), ('PLANT-JREF', None, 150, NN),
                                 ('PLANT-N', None, 300, nx), ('PLANT-KIND', 'kind', 300, NN)):
        dd3 = json.loads(texts['N'])
        if mut == 'precert':
            dd3['format'] = 'M3_RECORD_v1_PRECERT'
            dd3['claim'] = 'NOT CERTIFIED (PRECERT): ' + dd3['claim']
        elif mut == 'kernel':
            dd3['kernel_sha256'] = dd3['kernel_sha256'][:-1] + ('0' if dd3['kernel_sha256'][-1] != '0' else '1')
        elif mut == 'prec':
            dd3['kernel_prec'] = 256
        elif mut in deny:
            dd3['kernel_file'], dd3['kernel_sha256'] = mut, deny[mut]
        elif mut == 'claim':
            dd3['claim'] = dd3['claim'] + ' '
        elif mut == 'arbk':
            dd3['arb_kernel_sha256'] = dd3['arb_kernel_sha256'][:-1] + ('0' if dd3['arb_kernel_sha256'][-1] != '0' else '1')
        elif mut == 'arbb':
            dd3['arb_base_sha256'] = flip(dd3['arb_base_sha256'])
        elif mut == 'kind':
            dd3['items'][sorted(dd3['items'])[0]].pop('kind')
        what = mut or ('expected J_REF %d' % jref if jref != 300 else 'expected N %d' % nexp)
        try:
            RDR.check_text(json.dumps(dd3), jref, nexp)
            plant(lab, False, '(m3_reader_v4_4 must refuse the mutated N copy: %s)' % what)
        except ValueError:
            plant(lab, True, '(m3_reader_v4_4 refuses the mutated N copy: %s)' % what)
    # the bound load's checks, in memory: the consumers bind a record to the asm output that names it
    dn, dh = os.path.basename(paths['N']), tsha(texts['N'])
    try:
        RDR.loads(texts['N'], 'RECORD %s %s\nVERDICT VALID\n' % (dn, dh), 300, NN, dn)
        gate('C-BOUND-RT', True, '(m3_reader_v4_4.loads accepts the N text under an output that names it and ends VALID)')
    except ValueError as ex:
        gate('C-BOUND-RT', False, '(refused: %s)' % ex)
    for lab, otext in (('PLANT-BOUND-VERDICT', 'RECORD %s %s\nVERDICT VALID-PRECERT\n' % (dn, dh)),
                       ('PLANT-BOUND-INVALID', 'RECORD %s %s\nVERDICT INVALID (C-REP-B)\n' % (dn, dh)),
                       ('PLANT-BOUND-TWO', 'RECORD %s %s\nVERDICT VALID\nVERDICT VALID\n' % (dn, dh)),
                       ('PLANT-BOUND-SHA', 'RECORD %s %s\nVERDICT VALID\n' % (dn, flip(dh))),
                       ('PLANT-BOUND-NONE', 'VERDICT VALID\n')):
        try:
            RDR.loads(texts['N'], otext, 300, NN, dn)
            plant(lab, False, '(m3_reader_v4_4.loads must refuse this asm output)')
        except ValueError:
            plant(lab, True, '(m3_reader_v4_4.loads refuses this asm output)')
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
    gate('C-ONLY-N', set(texts) == set(FILES) == {'N'} and os.path.basename(paths['N']) == 'm3_s8v3_N_N%d_J300_v1_8_2.json' % NN,
         '(asmN writes the N record only: %s)' % os.path.basename(paths['N']))
    try:
        write_records(dict(texts, D=texts['N']), dict(paths, D=os.path.join(OUTD, 'm3_s8v3_D_N%d_J300_v1_8_2.json' % NN)), [], [], '', opener=no_open)
        plant('PLANT-ONLY-N', False, '(write_records with a D record added must raise before opening any file)')
    except ValueError:
        plant('PLANT-ONLY-N', not opened, '(write_records with a D record added raises before opening any file)')
    written = write_records(texts, paths, FAILS, NOFIRE, tag)
    if not written:
        out('RECORDS NOT WRITTEN (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE] + ([] if tag == '' else ['TAG %r' % (tag,)])))
    for f, path in written:
        gate('C-WRITE', sha(path) == tsha(texts[f]), '(%s holds exactly its C-FMT text)' % os.path.basename(path))
        out('RECORD %s %s' % (os.path.basename(path), sha(path)))
