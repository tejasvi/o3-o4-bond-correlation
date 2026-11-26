# m3_run_r0b_v1_4_c1.py -- pk04: the third part of m3_run_r0b_v1_4.py, executed in its namespace (it only defines). m3_run_r0b_v1_3.py's
# lines 1534-2097 with piece_state(), run_nk(), walk_pieces() and run_asm() changed for the continuation and the segments, and new:
# capped_ok, segs_of, split_ok, split_gate, split_plants, claim, src_checks, piece_resume, walk_seg, run_walk.
CAPPED = 'VERDICT INCOMPLETE (CAP-STOP)'


def capped_ok(lines, item, path=None):
    """a clean CAP-STOP output of item's producer (item_src): its first line names that producer, the item and that sha, and its VERDICT
    lines are exactly [CAPPED]."""
    nm, ssha = item_src(item)
    m = re.fullmatch(r'(m3_run_r0b_v1_[34]) item (\S+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)', lines[0] if lines else '')
    return bool(m) and m.group(1) == nm and m.group(2) == item and ACC.ok(path, m.group(4), ssha, ORIG_OF.get(ssha)) and HO.verdict_ok(lines, CAPPED)


def piece_state(graph, piece):
    """as m3_run_r0b_v1_3 under the names and sha of the piece's producer (item_src): 'valid', 'capped' or 'missing'; anything else raises
    ValueError."""
    item = '%sk%d.%d' % (PFX[graph], piece, NN)
    nm = item_src(item)[0]
    po = os.path.join(OUTD, '%s_%s.out' % (nm, item))
    ho = os.path.join(HANDD, '%s_%s.json' % (nm, item))
    if not os.path.exists(po):
        if os.path.exists(ho):
            raise ValueError('%s: a hand-off without its producer output' % item)
        return 'missing'
    if os.path.exists(ho):
        return 'valid'
    with open(po) as fh:
        lines = fh.read().split('\n')
    if capped_ok(lines, item, po):
        return 'capped'
    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of %s' % (item, nm))


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


def segs_of(graph):
    """the family's segments (SEGS) as (first piece, last piece, first entry, end entry), None resolved to its computed key count."""
    n = len(order_of(graph))
    return [(f, l, lo, n if hi is None else hi) for f, l, lo, hi in SEGS[graph]]


def split_ok(segs, n):
    """C-SPLIT's test: every segment has 1 <= first <= last and 0 <= lo < hi <= n; the piece ranges are disjoint; every computed key
    0..n-1 is claimed by exactly one segment; the first segment holds pieces 1..V13_PIECES and starts at entry 0."""
    if not segs or not all(1 <= f <= l and 0 <= lo < hi <= n for f, l, lo, hi in segs):
        return False
    cnt = [0] * n
    for f, l, lo, hi in segs:
        for i in range(lo, hi):
            cnt[i] += 1
    prs = sorted((f, l) for f, l, lo, hi in segs)
    return (cnt == [1] * n and all(prs[i][1] < prs[i + 1][0] for i in range(len(prs) - 1)) and segs[0][0] == 1 and segs[0][1] >= V13_PIECES
            and segs[0][2] == 0)


def split_gate(graph, segs):
    """C-SPLIT on one family's segments."""
    n = len(order_of(graph))
    gate('C-SPLIT', split_ok(segs, n), '(%s: segments (pieces: entries) %s over its %d computed keys; the piece ranges disjoint, every key '
         'in exactly one segment, pieces 1..%d (m3_run_r0b_v1_3\'s) and entry 0 in the first)' % (
             graph, ', '.join('%d..%d: %d..%d' % (f, l, lo, hi - 1) for f, l, lo, hi in segs), n, V13_PIECES))


def claim(res, graph, r, dups):
    """an entry into res once (C-CLAIM): a key already there (two pieces or two segments with one key) is refused and listed in dups."""
    if (graph, r['name']) in res:
        dups.append('%s %s' % (graph, r['name']))
        return False
    res[(graph, r['name'])] = r
    return True


def split_plants():
    """once per item: PLANT-SPLIT and PLANT-SPLIT-GAP on W3e's segments (its second segment starting one key earlier, that key then claimed
    by two segments, or one key later, claimed by none, must fail C-SPLIT's test) and PLANT-CLAIM-TWICE (a key claimed a second time is
    refused and listed)."""
    segs, order = segs_of('W3e'), order_of('W3e')
    n = len(order)
    f, l, lo, hi = segs[1]
    two = [segs[0], (f, l, lo - 1, hi)] + segs[2:]
    gap = [segs[0], (f, l, lo + 1, hi)] + segs[2:]
    plant('PLANT-SPLIT', split_ok(segs, n) and not split_ok(two, n), '(W3e with its segment of pieces %d..%d starting at entry %d: %s claimed '
          'by two segments)' % (f, l, lo - 1, order[lo - 1]))
    plant('PLANT-SPLIT-GAP', split_ok(segs, n) and not split_ok(gap, n), '(W3e with its segment of pieces %d..%d starting at entry %d: %s '
          'claimed by none)' % (f, l, lo + 1, order[lo]))
    sc, sd = {}, []
    r0 = {'name': order[0]}
    pc = claim(sc, 'W3e', r0, sd) and not claim(sc, 'W3e', dict(r0), sd) and sd == ['W3e %s' % order[0]]
    plant('PLANT-CLAIM-TWICE', pc, '(W3e %s claimed a second time: refused and listed)' % order[0])


def src_checks():
    """once per item: PLANT-SRC-NAME (a v1_3-named piece above k40 and a v1_4-named one at k40 refused before any file is opened),
    PLANT-SRC-SHA (m3_run_r0b_v1_3's VNu hand-off with its header's script unpinned, V13_SHA flipped or this script's sha, refused;
    unchanged, read) and PLANT-SRC-CAPPED (clean CAP-STOP first lines under the wrong name or sha refused, the right ones accepted)."""
    k40, k41 = 'W3ek%d.%d' % (V13_PIECES, NN), 'W3ek%d.%d' % (V13_PIECES + 1, NN)
    rn = []
    for nm, it in ((V13_NAME, k41), (SNAME, k40)):
        try:
            read_as(nm, it, 'W3e')
            rn.append(False)
        except ValueError:
            rn.append(True)
    plant('PLANT-SRC-NAME', all(rn), '(the hand-offs %s_%s and %s_%s: refused %s)' % (V13_NAME, k41, SNAME, k40, rn))
    it = 'VNu.%d' % NN
    nm, ssha = item_src(it)
    with open(os.path.join(HANDD, '%s_%s.json' % (nm, it))) as fh:
        lines = fh.read().split('\n')
    want = {'script': ACC.expect(os.path.join(HANDD, '%s_%s.json' % (nm, it)), ssha, ORIG_OF[ssha]), 'item': it, 'N': NN, 'family': 'VN'}
    rs = []
    for bad in (flip(V13_SHA), SELF_SHA):
        h = json.loads(lines[0])
        h['script'] = bad
        try:
            HO.read_text('\n'.join([json.dumps(h, sort_keys=True)] + lines[1:]), want)
            rs.append(False)
        except ValueError:
            rs.append(True)
    try:
        HO.read_text('\n'.join(lines), want)
        ctl = True
    except ValueError:
        ctl = False
    plant('PLANT-SRC-SHA', all(rs) and ctl, '(%s_%s.json with its header\'s script %s (V13_SHA flipped) or %s (this script\'s) in place of '
          'the pinned %s: refused %s; unchanged: read %s)' % (nm, it, flip(V13_SHA)[:8], SELF_SHA[:8], V13_SHA[:8], rs, ctl))
    cl = lambda n, i, h: ['%s item %s LIM 540; script sha256 %s; python 3' % (n, i, h), CAPPED]
    cc = [capped_ok(cl(V13_NAME, k40, V13_SHA), k40), capped_ok(cl(SNAME, k41, SELF_SHA), k41), capped_ok(cl(V13_NAME, k40, flip(V13_SHA)), k40),
          capped_ok(cl(V13_NAME, k41, V13_SHA), k41), capped_ok(cl(SNAME, k40, SELF_SHA), k40), capped_ok(cl(SNAME, k41, flip(SELF_SHA)), k41)]
    plant('PLANT-SRC-CAPPED', cc == [True, True, False, False, False, False], '(clean CAP-STOP first lines: %s k40 under V13_SHA and %s k41 '
          'under this script\'s sha accepted; V13_SHA flipped at k40, %s at k41, %s at k40 and this script\'s sha flipped at k41 refused: %s)' % (
              V13_NAME, SNAME, V13_NAME, SNAME, cc))


def piece_resume(graph, piece, seg):
    """where piece resumes in its segment seg: (start, partial, caps) from the last valid piece before it in the segment, the clean
    CAP-STOPs after that one counted; with none, the segment's first entry and nothing carried (m3_run_r0b_v1_3's loop in run_nk)."""
    first, last, lo, hi = seg
    caps = 0
    for j in range(piece - 1, first - 1, -1):
        st = piece_state(graph, j)
        if st == 'capped':
            caps += 1
            continue
        if st != 'valid':
            raise ValueError('%sk%d.%d is %s, so piece %d cannot start' % (PFX[graph], j, NN, st, piece))
        prev = read_handoff('%sk%d.%d' % (PFX[graph], j, NN), graph)
        return prev['next'], prev['partial'], caps
    return lo, None, caps


def run_nk(graph, piece):
    """as m3_run_r0b_v1_3 inside the piece's segment (SEGS): only a piece above k40 inside a segment runs; it resumes where the last valid
    piece of its segment stopped, or at the segment's first entry (piece_resume), and stops at the segment's end entry; C-SPLIT and the
    split and source plants first; the hand-off carries the segment."""
    stage('%s keys piece %d' % (graph, piece))
    order = order_of(graph)
    segs = segs_of(graph)
    seg = next((s for s in segs if s[0] <= piece <= s[1]), None)
    if piece <= V13_PIECES or seg is None:
        raise ValueError('%sk%d.%d: this script runs only a piece above k%d inside a segment of %s (pieces %s)' % (
            PFX[graph], piece, NN, V13_PIECES, graph, ', '.join('%d..%d' % s[:2] for s in segs)))
    first, last, lo, hi = seg
    split_gate(graph, segs)
    split_plants()
    src_checks()
    g = family_graph(graph)
    scal = prep_scalars(VG[graph])   # the scalars of the family's vertex graph (C-PREP-STAGES)
    part_plants(graph, family_parts(graph))
    norm_rel_plants()
    start, partial, caps = piece_resume(graph, piece, seg)
    if not lo <= start < hi or (partial is not None and partial.get('entry') != order[start]):
        raise ValueError('%s piece %d: resumes at entry %d%s, outside its segment\'s entries %d..%d or not the entry carried' % (
            graph, piece, start, (' with units of %s' % partial.get('entry')) if partial else '', lo, hi - 1))
    factor = 1.5 * 2 ** caps
    nin = len(partial['vals']) if partial else 0
    out('PIECE-START %s piece %d resumes at entry %d of %d%s after %d capped piece(s); stop factor %.1f; LIM %d; segment pieces %d..%d, '
        'entries %d..%d' % (graph, piece, start, len(order), (' with %d units of %s restored' % (nin, partial['entry'])) if partial else '',
                            caps, factor, LIM, first, last, lo, hi - 1))
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
    while i < hi:
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
    gate('C-PIECE', prog, '(%s piece %d: entries %d..%d done, next %d of %d; segment entries %d..%d of %d computed keys; %d units computed%s)' % (
        graph, piece, start, i - 1, i, hi, lo, hi - 1, len(order), units[0], (', %d units of %s carried' % (nout, part['entry'])) if part else ''))
    write_handoff(graph, {'family': graph, 'piece': piece, 'start': start, 'next': i, 'partial': part, 'stop_factor': factor,
                          'entries': res, 'fallbacks': fb_info(), 'segment': [first, last, lo, hi]})


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


def walk_seg(graph, seg, res, dups, strict=True):
    """C-PIECES over one segment: its pieces from its first, each starting where the last valid one stopped (the first at the segment's
    first entry), advancing, ending at or before the segment's end entry with nothing carried past it, its entries exactly the keys from
    its start to its next, its segment field the segment's (a v1_3 piece: none), each entry claimed once (claim). Returns (next, units
    carried, the first piece not read). strict False (walk): a piece whose state or hand-off read raises ends the segment's walk with an
    INFO line."""
    order = order_of(graph)
    first, last, lo, hi = seg
    nxt, piece, nin = lo, first, 0
    while nxt < hi and piece <= last:
        item = '%sk%d.%d' % (PFX[graph], piece, NN)
        try:
            st = piece_state(graph, piece)
            body = read_handoff(item, graph) if st == 'valid' else None
        except ValueError as ex:
            if strict:
                raise
            out('WALK-STOP %s: %s (INFO; the asm would stop here)' % (item, ex))
            break
        if st == 'missing':
            break
        if st == 'capped':
            out('PIECE-CAPPED %s: a clean CAP-STOP of %s, no hand-off; skipped and kept' % (item, item_src(item)[0]))
            piece += 1
            continue
        pt = body['partial']
        nout = len(pt['vals']) if pt else 0
        names = [r['name'] for r in body['entries']]
        segok = body.get('segment') == list(seg) if item_src(item)[0] == SNAME else 'segment' not in body
        okp = (body['start'] == nxt and (body['next'] > nxt or nout > nin) and body['next'] <= hi and names == order[body['start']:body['next']]
               and segok and (pt is None or (body['next'] < hi and pt['entry'] == order[body['next']])))
        gate('C-PIECES', okp, '(%s: entries %d..%d complete%s; segment entries %d..%d)' % (item, body['start'], body['next'] - 1, (
            ', %d units of %s carried' % (nout, pt['entry'])) if pt else '', lo, hi - 1))
        for r in body['entries']:
            claim(res, graph, r, dups)
        nxt, piece, nin = body['next'], piece + 1, nout
    return nxt, nin, piece


def walk_pieces(graph, res):
    """C-SPLIT; per segment C-PIECES (walk_seg) and its cover: the segment's pieces cover its computed keys in order, none left in progress;
    C-CLAIM: each computed key of the family claimed by exactly one piece. The entries go into res."""
    order, segs, dups = order_of(graph), segs_of(graph), []
    split_gate(graph, segs)
    for seg in segs:
        nxt, nin, _ = walk_seg(graph, seg, res, dups)
        gate('C-PIECES', nxt == seg[3] and nin == 0, '(the %s pieces %d..%d cover its computed keys %d..%d, in order, none left in progress)' % (
            graph, seg[0], seg[1], seg[2], seg[3] - 1))
    got = sorted(k for g, k in res if g == graph)
    gate('C-CLAIM', not dups and got == sorted(order), '(%s: each of its %d computed keys claimed by exactly one piece: %d claimed; twice: %s)' % (
        graph, len(order), len(got), dups or 'none'))


def run_walk():
    """the walk (no hand-off, no record): the split and source plants; per family C-SPLIT and per segment how far its pieces reach
    (walk_seg with its gates, strict False) and, for a segment not finished, where its next piece resumes (piece_resume, INFO); C-CLAIM
    over the pieces read."""
    stage('walk')
    split_plants()
    src_checks()
    for graph in FAMS:
        order, segs, res, dups = order_of(graph), segs_of(graph), {}, []
        split_gate(graph, segs)
        for seg in segs:
            first, last, lo, hi = seg
            nxt, nin, piece = walk_seg(graph, seg, res, dups, strict=False)
            line = 'WALK %s pieces %d..%d, entries %d..%d: next %d%s' % (graph, first, last, lo, hi - 1, nxt,
                                                                       (' with %d units carried' % nin) if nin else '')
            if nxt == hi and nin == 0:
                line += '; complete'
            elif piece > last:
                line += '; no piece left in the segment'
            else:
                try:
                    st, pt, caps = piece_resume(graph, piece, seg)
                    line += '; piece %d resumes at entry %d (%s)%s after %d capped piece(s), stop factor %.1f' % (
                        piece, st, order[st] if st < len(order) else '-', (' with %d units of %s' % (len(pt['vals']), pt['entry'])) if pt else '',
                        caps, 1.5 * 2 ** caps)
                except ValueError as ex:
                    line += '; piece %d cannot resume: %s' % (piece, ex)
            out(line + ' (INFO)')
        gate('C-CLAIM', not dups, '(%s: no computed key claimed twice in the pieces read: %d claimed; twice: %s)' % (graph, len(res), dups or 'none'))


def run_smoke(graph):
    """as m3_run_r0b_v1_2 (Xa, the smoke piece), with C-RULE-SIZE after the prep."""
    stage('smoke %s' % graph)
    list_check()
    enc_check()
    parity_set()
    alias_check()
    sym_map_check()
    rule_of_check()
    ab_check(graph)
    g = family_graph(graph)
    pr, rp = make_prep(VG[graph], g, ())
    prep_same(graph, g, prep_graph(g), pr)
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
    e, facs, p = parts[EMPTY[graph]]
    pr.qcap = qcap_of(pr, p, graph)[0]
    t0 = cpu()
    ak, _, info = pr.bound(facs, p['grouping'], bars=False, entry=EMPTY[graph])
    w = ak_dev(ak, e['ak_float'])
    gate('C-SMOKE-AK', w <= 1e-9, '(%s %s: a_k %s against the list\'s ak_float %s: largest |mid - float| / max(1, |float|) %.2e; %.2f s)' % (
        graph, EMPTY[graph], ['%.12g' % float(a.mid) for a in ak], e['ak_float'], w, cpu() - t0))
    f0 = facs[0]
    facs2 = [(f0[0], f0[1], [x * (1 + 1e-6) for x in f0[2]], f0[3], f0[4])] + list(facs[1:])
    ak2, _, _ = pr.bound(facs2, 'std', bars=False, entry=EMPTY[graph] + ' (planted)')
    w2 = ak_dev(ak2, e['ak_float'])
    plant('PLANT-SMOKE-PATH', f0[0] == 'p' and not (w2 <= 1e-9), '(%s with its first p factor\'s q1 times 1 + 1e-6: largest difference %.2e)' % (
        EMPTY[graph], w2))
    STAGE[0] = 'smoke plants'
    part_plants(graph, parts)
    gcache_check(graph, pr, parts)
    barpos_info(graph, pr, parts)
    ak_total_plants()
    norm_rel_plants()
    pack_gate(graph, plans)
    fb_info()


def part_rec_ok(field, graph):
    """C-PART-REC's test of one record's partition field: exactly the family's computed keys, each with rule_of's rule, the groups part_enc
    recomputes from the list's encodings, G = len(groups) and an int qcap >= the family's QCAP0."""
    if set(field) != set(order_of(graph)):
        return False
    for k, v in field.items():
        e = entries_of(graph, [k])[0]
        q = v.get('qcap')
        if (v.get('rule') != rule_of(e) or v.get('groups') != part_enc(rule_of(e), e['factors']) or v.get('G') != len(v.get('groups') or [])
                or isinstance(q, bool) or not isinstance(q, int) or q < QCAP0[graph]):
            return False
    return True


def reader_plants(text, name):
    """the reader plants of m3_run_v1_10_4 l.1688-1771 on the W2 record's text; PLANT-PARZERO on W2's parity zero G,0,2."""
    dd = json.loads(text)
    k0 = sorted(k for k in dd['items'] if dd['items'][k]['parity'] == 'free')[0]
    dd['items'][k0]['B'].pop('rnd')
    try:
        RDR._check_text(json.dumps(dd), 300, NN)
        plant('PLANT-FMT', False, '(W2 copy without one rnd)')
    except ValueError:
        plant('PLANT-FMT', True, '(W2 copy without one rnd)')
    dd2 = json.loads(text)
    kr = max((k for k in dd2['items'] if dd2['items'][k]['parity'] == 'free'), key=lambda k: sum(dd2['items'][k]['ak_rad']))
    dd2['items'][kr]['B']['rnd'] = 0.0
    try:
        RDR._check_text(json.dumps(dd2), 300, NN)
        plant('PLANT-RND', False, '(W2 copy with %s rnd = 0)' % kr)
    except ValueError:
        plant('PLANT-RND', sum(dd2['items'][kr]['ak_rad']) > 0, '(W2 copy with %s rnd = 0; its ak_rad sum %.1e)' % (kr, sum(dd2['items'][kr]['ak_rad'])))
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
            plant(lab, False, '(m3_reader_v6_3 must refuse the mutated W2 copy: %s)' % what)
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3 refuses the mutated W2 copy: %s)' % what)
    dz = json.loads(text)
    dz['items']['G,0,2']['ak'][1] = 1e-30
    try:
        RDR._check_text(json.dumps(dz), 300, NN)
        plant('PLANT-PARZERO', False, '(m3_reader_v6_3 must refuse the W2 copy with G,0,2 a_1 = 1e-30)')
    except ValueError:
        plant('PLANT-PARZERO', True, '(m3_reader_v6_3 refuses the W2 copy with G,0,2 a_1 = 1e-30)')
    dh = tsha(text)
    try:
        RDR.loads(text, 'RECORD %s %s\nVERDICT VALID\n' % (name, dh), 300, NN, name)
        gate('C-BOUND-RT', True, '(m3_reader_v6_3.loads accepts the W2 text under an output that names it and ends VALID)')
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


UHAT_KEYS = ('role', 'k', 'e_a', 'empty', 'factors', 'alias_kind')


def uhat_ok(items, graph):
    """C-UHAT's test on one record's items: exactly the family's certify and check keys, each with role and factors as its list, k = the
    window's column count, e_a = EA, empty = EMPTY, alias_kind and alias_of as ALIAS (None for a computed key)."""
    es = {name_of(e): e for e in entries_of(graph)}
    if set(items) != set(es):
        return False
    for k, it in items.items():
        a = ALIAS[graph].get(k, (None, None))
        if (any(f not in it for f in UHAT_KEYS) or it['role'] != es[k]['role'] or it['factors'] != es[k]['factors']
                or it['k'] != len(GRAPHS[graph]['columns']) or it['e_a'] != EA[graph] or it['empty'] != EMPTY[graph]
                or it['alias_kind'] != a[1] or it.get('alias_of') != a[0]):
            return False
    return True


def sym_ok(files, g, c, t, shift=0.0):
    """C-SYM's test of one pair: every a_k ball [ak - ak_rad, ak + ak_rad] of the check key c (its ak moved by shift) overlaps its mirror
    key t's, in exact rationals, and the parities agree."""
    a, b = files[g][c], files[g][t]
    for k in range(4):
        x0 = Fraction(a['ak'][k]) + Fraction(shift) - Fraction(a['ak_rad'][k])
        x1 = Fraction(a['ak'][k]) + Fraction(shift) + Fraction(a['ak_rad'][k])
        y0, y1 = Fraction(b['ak'][k]) - Fraction(b['ak_rad'][k]), Fraction(b['ak'][k]) + Fraction(b['ak_rad'][k])
        if not (x0 <= y1 and y0 <= x1):
            return False
    return a['parity'] == b['parity']


def run_asm():
    stage('asm')
    list_check()
    enc_check()
    parity_set()
    alias_check()
    sym_map_check()
    rule_of_check()
    split_plants()
    src_checks()
    res = {}
    for graph in FAMS:
        walk_pieces(graph, res)
    resume_chain()
    scals = {vg: prep_scalars(vg) for vg in ('VN', 'VD')}   # C-PREP-STAGES: the hand-offs the records name
    toks = phi_tokens()
    gate('C-G-PHI', phi_ok(toks), '(M2B_KV_v1 13cc0d9a PIN_TRIAL tokens of N%d: %s; each file under code/ hashes to its token and to this '
         'run\'s pin)' % (NN, toks))
    plant('PLANT-G-PHI', not phi_ok(toks[:1] + [flip(toks[1])] if len(toks) == 2 else []), '(the second token with its sha256\'s last digit changed)')
    files, pfield, rak = {g: {} for g in FAMS}, {g: {} for g in FAMS}, []
    for graph in FAMS:
        for name in order_of(graph):
            e = entries_of(graph, [name])[0]
            r = res[(graph, name)]
            pfield[graph][name] = {'rule': r['rule'], 'G': r['G'], 'groups': r['groups'], 'qcap': r['qcap']}
            if e['parity'] == 'zero':
                if r['parity'] != 'zero':
                    raise ValueError('%s %s: marked zero, computed %s' % (graph, name, r['parity']))
                it = REC.entry_record(None, None, T_REF, 'zero')
            else:
                it = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=r['a0_exact'], laws=r['laws'])
            files[graph][name] = it
            rak.append((ak_dev(r['ak'], e['ak_float']), graph, name))
        for name, (src, kind) in ALIAS[graph].items():
            files[graph][name] = dict(files[graph][src], alias_of=src)
        for name, it in files[graph].items():
            e = entries_of(graph, [name])[0]
            it.update({'role': e['role'], 'k': len(GRAPHS[graph]['columns']), 'e_a': EA[graph], 'empty': EMPTY[graph], 'factors': e['factors'],
                       'alias_kind': ALIAS[graph].get(name, (None, None))[1]})
    out('PARITY-ZERO %s: written as exact zeros with parity zero (C-ODD and C-ODD-AK in their pieces)' % {g: ZERO[g] for g in FAMS if ZERO[g]})
    wr = max(rak)
    gate('C-REP-AK', wr[0] <= 1e-9, '(%d computed keys\' a_k against their lists\' ak_float: largest |certified mid - float| / max(1, |float|) '
         '%.2e at %s %s)' % (len(rak), wr[0], wr[1], wr[2]))
    plant('PLANT-REPAK', not (wr[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')
    okal = all(files[g][n]['ak'] == files[g][s]['ak'] and files[g][n]['B'] == files[g][s]['B'] and files[g][n]['parity'] == files[g][s]['parity']
               and s in order_of(g) for g in FAMS for n, (s, kind) in ALIAS[g].items())
    gate('C-ALIAS-ASM', okal, '(%d alias items carry their computed source\'s a_k, bars and parity exactly)' % sum(len(ALIAS[g]) for g in FAMS))
    mir = sorted('%s %s' % (g, c) for g in FAMS for c, (s, kind) in ALIAS[g].items() if kind == 'mirror')
    out('C-SYM-STRUCT: the lists\' numeric C-SYM is replaced, for the %d mirror check keys %s, by the exact structural test (C-SYM-MAP: '
        'couplings, tags, list pairs and factor data mirror-invariant; C-ALIAS-ASM: each item copied exactly from its mirror key); '
        'pk11 records the change in R6.5\'s list' % (len(mir), mir))
    pairs = [(g, c, t) for g in FAMS for c, t in MIRRORS.get(g, {}).items() if ALIAS[g].get(c, (None, None))[1] != 'mirror']
    wsym = max([abs(files[g][c]['ak'][k] - files[g][t]['ak'][k]) for g, c, t in pairs for k in range(4)] + [0.0])
    gate('C-SYM', bool(pairs) and all(sym_ok(files, g, c, t) for g, c, t in pairs), '(the check keys whose mirror pair has two computed '
         'sources, %s: every a_k ball overlaps its mirror key\'s, parities equal; largest |mid difference| %.2e)' % (
             ['%s %s / %s' % x for x in pairs], wsym))
    g, c, t = pairs[0]
    sh = 10 * (files[g][c]['ak_rad'][0] + files[g][t]['ak_rad'][0]) + 1e-12 * max(1.0, abs(files[g][t]['ak'][0]))
    plant('PLANT-SYM', not sym_ok(files, g, c, t, sh), '(%s %s with its a_k moved by ten times both a_0 radii plus 1e-12: must miss %s)' % (g, c, t))
    gate('C-SCOPE', all(set(files[g]) == set(name_of(e) for e in entries_of(g)) for g in FAMS), '(the six records hold exactly their lists\' '
         'certify and check keys: %s)' % ', '.join('%s %d' % (g, len(files[g])) for g in FAMS))
    plant('PLANT-SCOPE', not (set(list(files['W2'])[1:]) == set(name_of(e) for e in entries_of('W2'))), '(W2 without one key)')
    gate('C-UHAT', all(uhat_ok(files[g], g) for g in FAMS), '(every item carries role, factors, k, e_a, empty and alias_kind as the lists and '
         'ALIAS give them: %s)' % ', '.join('%s %s' % (g, uhat_ok(files[g], g)) for g in FAMS))
    badu = {k: dict(v) for k, v in files['W3e'].items()}
    k0 = sorted(badu)[0]
    badu[k0]['k'] = 2
    plant('PLANT-UHAT', not uhat_ok(badu, 'W3e'), '(W3e with %s carrying k 2)' % k0)
    gate('C-PART-REC', all(part_rec_ok(pfield[g], g) for g in FAMS), '(the partition fields of the six records: every computed key with '
         'rule_of\'s rule, the groups recomputed from the list\'s encodings, G = len(groups), qcap >= QCAP0: %s)' % (
             ', '.join('%s %s' % (g, part_rec_ok(pfield[g], g)) for g in FAMS)))
    kx = next(k for k, v in pfield['W3e'].items() if v['G'] >= 2)
    badf = dict(pfield['W3e'])
    badf[kx] = dict(badf[kx], groups=[badf[kx]['groups'][1], badf[kx]['groups'][0]] + badf[kx]['groups'][2:])
    plant('PLANT-PART-REC', not part_rec_ok(badf, 'W3e'), '(W3e\'s field with %s\'s groups 0 and 1 swapped)' % kx)
    tag = TAG
    eng = {SNAME: SELF_SHA, 'parts': dict(PARTS), V13_NAME: V13_SHA, 'modules': dict(OWNMOD)}
    kern = {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}
    radii = lambda d: {k: d[k] for k in ('a_v', 'ap', 'theta0')}
    fsrc = 'pk11/out/%s:%s' % (TSF, INPUTS[(W4, TSF)])
    absrc = ('pk03/m3_graph_v3.py:%s: vac columns carry the tags A, A, B with A = (3 + sqrt 21)/6 and B = (3 sqrt 5 - sqrt 21)/12 exactly '
             '(m3_graph_v3.coupling; C-AB by (6A - 3)^2 = 21 and (12B + 6A - 3)^2 = 45 with 6A - 3, 12B + 6A - 3, A and B positive)' % OWNMOD['m3_graph_v3.py'])
    texts, paths = {}, {}
    for g in FAMS:
        vg = VG[g]
        hs = {s: '%s_%s%s.%d.json' % (item_src('%s%s.%d' % (vg, s, NN))[0], vg, s, NN) for s in ('u', 'c')}
        prep = {'vgraph': vg, 'radii_from': '%s:%s' % (REFVG[vg][NN], INPUTS[(OUTD, REFVG[vg][NN])]),
                'stages': {s: '%s:%s' % (h, sha(os.path.join(HANDD, h))) for s, h in hs.items()}, 'dmaxH': 18}
        lnm, ld, lf = LOF[g]
        hasf = any(x[0] in ('st', 'cp') and int(x[1]) >= 1 for e in entries_of(g) for x in e['factors'])
        extra = {'entry_list': '%s:%s' % (lf, INPUTS[(ld, lf)]), 'graph': g, 'columns': GRAPHS[g]['columns'], 'pairs': GRAPHS[g]['pairs'],
                 'k': len(GRAPHS[g]['columns']), 'dmaxH': 18, 'claim_ball': CLAIM_BALL, 'prep': prep, 'partition': pfield[g],
                 'aliases': {k: list(v) for k, v in ALIAS[g].items()}, 'mirrors': MIRRORS.get(g, {}), 'parity_zero': ZERO[g], 'g_phi': toks,
                 'f_source': fsrc if hasf else None, 'ab_source': absrc, 'g_c': GC_NOTE, 'g_norm': GN_NOTE % (g, EMPTY[g]), 'e_a': EA[g]}
        top = REC.top_level(NN, 300, {g: radii(ref_prep_vg(vg))}, TRIAL, eng, tag, kern, extra=extra)
        texts[g] = json.dumps(dict(top, items=files[g]))
        paths[g] = os.path.join(OUTD, 'm3_r0b_%s_N%d_J300%s_v1.json' % (g, NN, tag))
        rd = RDR._check_text(texts[g], 300, NN, name=os.path.basename(paths[g]))
        okf = (all(rd['entries'][k] == (files[g][k]['ak'], files[g][k]['err']) for k in files[g]) and set(rd['entries']) == set(files[g])
               and rd['top'].get('partition') == pfield[g] and uhat_ok(json.loads(texts[g])['items'], g))
        gate('C-FMT', okf, '(%s: %d keys read back exactly from the text by m3_reader_v6_3, the partition and u-hat fields with them; %d bytes; '
             'sha256 %s)' % (os.path.basename(paths[g]), len(files[g]), len(texts[g]), tsha(texts[g])))
    reader_plants(texts['W2'], os.path.basename(paths['W2']))
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
