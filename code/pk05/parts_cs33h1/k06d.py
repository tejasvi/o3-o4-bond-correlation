

def lmin(a, b):
    """v1_8: a safe lower bound of min(a, b) for balls: the smaller of the two lower ends, as an exact ball"""
    la, lb = a.lower(), b.lower()
    return la if la < lb else lb


def sb_spectral(SP, tb, eT, drop=None):
    """one subball: KW intervals (widened by eps_T); per sector a maximal set of pairwise disjoint intervals is subtracted in the trace
    bound tau (an interval overlapping an earlier one may hold the same eigenvalue: not subtracted, never certified); certified modes need a
    positive Davis-Kahan gap inside their sector; sines s_j (KW part plus the T-frame Davis-Kahan part times sqrt(nu0/nu_j), R9 TR4), u_rem;
    drop: a mode left out of the trace bound (plant P-TR)."""
    modes = SP['modes']
    I = []
    for m in modes:
        mu = E.ev(m['mu'], arb(0), tb)
        w = arb(m['eps']) + arb(eT)
        I.append((mu, (mu - w).lower(), (mu + w).upper()))
    disj = lambda a, b: I[a][1] > I[b][2] or I[b][1] > I[a][2]
    ok, why, tau, subt = True, [], {}, set()
    for sg in (1.0, -1.0):
        ids = [j for j, m in enumerate(modes) if m['sg'] == sg]
        for j in ids:
            if j != drop and all(disj(j, i) for i in subt if modes[i]['sg'] == sg):
                subt.add(j)
        t = E.ev(SP['trs'][sg][0], SP['trs'][sg][1], tb).upper()
        for j in ids:
            t = t + (arb(modes[j]['eps']) if j in subt else I[j][0].upper())
        tau[sg] = (t + arb(eT)).upper()
    cert, gam_, s = [], {}, {}
    for j, m in enumerate(modes):
        sg = m['sg']
        g = I[j][0].lower() - tau[sg]
        for i, mi in enumerate(modes):
            if i != j and mi['sg'] == sg:
                if I[j][0].lower() > I[i][2]:
                    d = I[j][0].lower() - I[i][2]
                elif I[i][1] > I[j][0].upper():
                    d = I[i][1] - I[j][0].upper()
                else:
                    d = arb(-1)
                g = lmin(g, d)                                         # v1_8 (Z4): lower ends, never the undecided side
        gD = g - arb(m['eps'])                                   # v1_8 (Z1): R4 (iii)'s gap around the eigenvalue is >= g - eps_j
        if j in subt and gD > 2 * arb(eT):
            cert.append(j)
            gam_[j] = g
            fr = (I[0][2] / I[j][1]).sqrt()                         # v1_5 (R9 TR4): the T-frame Davis-Kahan term carries sqrt(nu0/nu_j)
            s[j] = (arb(m['eps']) / g + fr * (SQ2 * arb(eT) / (gD - arb(eT)) + arb(eT) / (2 * I[j][1]))).upper()
    if not all(j in cert for j in range(NCERT)):
        ok = False
        why.append('certified %s' % cert)
    cert = [j for j in cert if j < NCERT]
    urem = {sg: tau[sg] for sg in (1.0, -1.0)}
    for j, m in enumerate(modes):
        if j not in cert:
            urem[m['sg']] = amax(urem[m['sg']], I[j][2])
    ur = amax(urem[1.0], urem[-1.0])
    top1 = ur
    for j in range(1, NMODE):
        top1 = amax(top1, I[j][2])
    if not (I[0][1] > top1):
        ok = False
        why.append('nu1 not top')
    top2 = ur
    for j in range(2, NMODE):
        top2 = amax(top2, I[j][2])
    if not (I[1][1] > top2) or modes[1]['sg'] < 0:
        ok = False
        why.append('nu2 not isolated')
    return dict(I=I, tau=tau, cert=cert, gam=gam_, s=s, urem=ur, ok=ok, why=why, subt=sorted(subt))
