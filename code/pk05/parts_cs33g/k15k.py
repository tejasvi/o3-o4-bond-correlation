

def _fe(v):
    return '-' if v is None else '%.3e' % v


def _fc(c):
    return '-' if c is None else '(' + ','.join(('%.3e' % x) if isinstance(x, float) else str(x) for x in c) + ')'


def interval(N, b0, h, part, out):
    """one interval, one part ('A', 'B', 'Bh', 'Bv' or 'AB'): returns (status, info, SP, SBs, pack); status CERTIFIED / FAILED / CONFLICT"""
    t1 = time.process_time()
    L = int(math.ceil(math.sqrt(60.0 * (b0 + h)))) + 8
    tc = C.trunc_consts(N, b0, h, L)
    eT = tc[0]
    SP = spectral(N, b0, h, L, out)
    MODEPAR[0] = [1 if m['par'] > 0 else -1 for m in SP['modes']]
    SBs = [sb_spectral(SP, tb, eT) for tb in E.subballs(h, NSUB)]
    par_ok = all(abs(abs(m['par']) - 1.0) <= 1e-6 for m in SP['modes'])
    ctl = dict(cas=SP['qmax'] <= QGATE, node=SP['cnode'] <= NODEGATE, par=par_ok)
    spec_ok = all(sb['ok'] for sb in SBs)
    gaps = []
    for j in range(NCERT):
        gaps.append('%.3e' % min(E.fdn_arb(sb['gam'][j] / sb['I'][0][2]) for sb in SBs) if all(j in sb['gam'] for sb in SBs) else '-')
    out('SPEC N=%d b0=%r part %s: identification %s%s; eps_T %.3e eps_e %.3e; min gap/nu1 %s; u_rem/nu2 <= %.6f; mode sha8 (diagnostic) %s' % (
        N, b0, part, spec_ok, '' if spec_ok else ' ' + str([sb['why'] for sb in SBs if not sb['ok']][:2]), tc[0], tc[1], ' '.join(gaps),
        max(E.fup_arb(sb['urem'] / sb['I'][1][1]) for sb in SBs),
        ' '.join(hashlib.sha256(b''.join(np.ascontiguousarray(x).tobytes() for x in m['u'].c)).hexdigest()[:8] for m in SP['modes'])))
    res = dict(L=L, ctl=ctl, spec=spec_ok, tc=tc)
    if not spec_ok:
        return ('FAILED', res, SP, SBs, None)
    nu1up = max(E.fup_arb(sb['I'][0][2]) for sb in SBs)
    F, A = family_base(SP, nu1up, out)
    ctl['pos'] = A['plo'] > 0
    F = family_common(SP, F, A, out)
    F = family_part(SP, F, A, part, out)
    F = family_extra(SP, F, A)
    A['trho'] = [C.fv_trunc(SP['modes'][a]['u'], K_F).rho for a in range(NCERT)]
    F = xc_vectors(SP, F, A)
    NS = None
    obs = objects()
    names = ['J0'] + ['U%d' % a for a in range(NCERT)]
    for ob in obs:
        names += [ob[2], ob[3]] + ([ob[4], ob[5]] if 'B' in part else [])
    slack, trd = tr_slack(N, b0, h, L, SP, SBs, F, A, names, tc)               # v1_5: the proved slack (R9 TR5)
    A['epsW'], A['eT'] = trd['epsW'], tc[0]
    ctl['slack'] = slack < float('inf')
    out('TRUNC N=%d b0=%r part %s: eps_T %.3e eps_e %.3e eps_W %.3e kappa %.4g rho %.4g (%s) c %.6g slack_f %.3e | rho by type %s' % (
        N, b0, part, tc[0], tc[1], trd['epsW'], trd['kappa'], trd['rho'], trd['arg'], trd['c'], slack,
        ' '.join('%s %.4g' % kv for kv in sorted(trd['rt'].items()))))
    tg = time.process_time()
    ips = GIPS(F, slack, names)
    tgram = time.process_time() - tg
    tot = checks_all(ips, SP, A, SBs, obs, NS, h, part)
    ctl['fin'] = all(math.isfinite(v.rho) for v in F.values()) and all(math.isfinite(m['eps']) for m in SP['modes'])
    ok = all(ctl.values()) and not tot['fails']
    status = 'CERTIFIED' if ok else ('CONFLICT' if tot['negs'] else 'FAILED')
    out('CHECKS N=%d b0=%r part %s: NEAR %d min %s at %s | FAR %d k* <= %d min %s at %s | fails %d %s | negatives %d %s | slack %.2e | '
        'controls %s | gram rows %d, per-pair %d, inner products %d (gram %.1f s, checks %.1f s)' % (
            N, b0, part, tot['near'][0], _fe(tot['near'][1]), _fc(tot['near'][2]), tot['far'][0], tot['far'][1], _fe(tot['far'][2]),
            _fc(tot['far'][3]), len(tot['fails']), tot['fails'][:3], len(tot['negs']), tot['negs'][:3], slack, ctl, len(ips.row), ips.nfall,
            len(ips.cache), tgram, time.process_time() - tg - tgram))
    res.update(tot=tot, status=status, sec=time.process_time() - t1)
    return (status, res, SP, SBs, (F, A, ips, obs, NS))
