

def make_iv(ell, q):
    """floats (b0, h): [b0 - h, b0 + h] starts at ell (exactly contained) and has relative width about q"""
    b0 = ell / (1.0 - 0.5 * q)
    h = b0 - ell
    while not (arb(b0) - arb(h) <= arb(ell)):
        h = float(np.nextafter(h, np.inf))
    return b0, h


def top_iv(J, f):
    """floats (b0, h) with [b0 - h, b0 + h] containing [J/f, J] exactly"""
    lo = arb(J) / arb(f)
    b0, h = 0.5 * (J / f + J), 0.5 * (J - J / f)
    while not ((arb(b0) - arb(h) <= lo.lower()) and (arb(b0) + arb(h) >= arb(J))):
        h = float(np.nextafter(h, np.inf))
    return b0, h


def ledger(out, N, b0, h, st, part):
    lo, hi = arb(b0) - arb(h), arb(b0) + arb(h)
    out('IV N=%d part %s K=%d b0=%r h=%r L=%d status %s (%.1f s)' % (N, part, KDEG, b0, h, st['L'], st.get('status', 'FAILED'),
                                                                   st.get('sec', 0.0)))
    if st.get('status') == 'CERTIFIED':
        out('LEDGER %s N=%d lo=%s hi=%s b0hex=%s hhex=%s K=%d' % (part, N, lo.str(25, radius=False), hi.str(25, radius=False), b0.hex(),
                                                                   h.hex(), KDEG))
    return hi


def run_item(item, out):
    if item == 'smoke':
        plan, part = [(3, make_iv(20.2, 0.01))], 'AB'
        N, a, b, q = 3, None, None, None
    elif item in ('pilotA', 'pilotB', 'pilotBh', 'pilotBv'):
        plan, part = [(4, top_iv(300.0, 1.01))], item[5:]
        N, a, b, q = 4, None, None, None
    else:
        kind, Ns, As, Bs, Qs = item.split(':')
        if kind not in ('coverA', 'coverB', 'coverBh', 'coverBv'):
            raise SystemExit('unknown item %s' % item)
        part = kind[5:]
        N, a, b, q = int(Ns), float(As), float(Bs), float(Qs)
        plan = None
    valid, allcert, ell, idx, last, hi, stopped = True, True, a, 0, 0.0, None, False
    while True:
        if plan is not None:
            if idx >= len(plan):
                break
            N, (b0, h) = plan[idx]
        else:
            if hi is not None and not (hi < arb(b)):
                break
            if time.process_time() - T0 + 1.5 * last > 0.9 * CAP_S:
                out('COVER_STOP N=%d part %s next_left=%r (time)' % (N, part, ell))
                stopped = True
                break
            b0, h = make_iv(ell, q)
        t1 = time.process_time()
        status, st, SP, SBs, pack = interval(N, b0, h, part, out)
        if idx == 0:
            if pack is None:
                valid = False
                out('PLANTS not run: the first interval failed before the checks')
            else:
                fired = plants(N, b0, h, SP, SBs, pack, part, out)
                cp = c_probe(N, SP, out)
                valid = valid and all(fired.values()) and cp
        hi = ledger(out, N, b0, h, st, part)
        allcert = allcert and status == 'CERTIFIED'
        if status == 'CONFLICT':
            out('CONFLICT at N=%d b0=%r part %s: report first; stopping' % (N, b0, part))
            break
        del SP, SBs, pack
        last = time.process_time() - t1
        idx += 1
        if plan is None:
            ell = float(np.nextafter(float(hi.lower()), -np.inf))
    return valid, allcert, a, hi, stopped, part
