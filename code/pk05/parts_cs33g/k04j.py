

def fv_lower(v):
    """a lower bound of inf_{|t|<=h} |v(t)|_2: |c_0| (rounded down) minus sum_{d>=1} |c_d| h^d and the remainder (rounded up)"""
    n = v.c[0].size
    s0 = float(np.dot(v.c[0], v.c[0]))
    lo0 = float(dn(math.sqrt(max(0.0, float(dn(s0 * (1.0 - 4 * gam(n + 2))))))))
    rest = sum(C.vec_norm_ub(np.abs(x)) * float(up(v.h ** d * (1.0 + 1e-12))) for d, x in enumerate(v.c) if d > 0)
    return float(dn(lo0 - float(up((rest + v.rho) * (1.0 + 1e-12)))))


def tr_slack(N, b0, h, L, SP, SBs, F, A, names, tc):
    """(R9 TR1, TR5) eps_W, kappa, rho, c and the proved inner-product slack slack_f for one interval; inf when a lower bound fails"""
    eT, ee, A3 = tc
    lam = arb(N - 2) / 2
    b0a, bm, bp = arb(b0), arb(b0) - arb(h), arb(b0) + arb(h)
    Amax = arb(A3) ** (arb(1) / 3)
    a0lo = ((-arb(h)).exp() * (b0a / bp) ** lam * bp.bessel_i(lam) / b0a.bessel_i(lam)).lower()
    epsW = max(E.fup_arb(2 * Amax * arb(eT) / a0lo), E.fup_arb((1 + arb(L + 1) / bm) * arb(ee)))
    epss = max(eT, ee, epsW)
    n0lo = min(E.fdn_arb(sb['I'][0][1]) for sb in SBs)
    n0hi = max(E.fup_arb(sb['I'][0][2]) for sb in SBs)
    vnorm = float(np.max(C.tm_bounds(SP['B']['E'][0])[1][0, 0]))
    P, e = C.fv_inner(F['U0'], F['J0'])
    bt = E.ev(P, arb(0, e), arb(0, h))
    s0 = max(E.fup_arb(sb['s'][0]) for sb in SBs)
    b0lo = E.fdn_arb(abs(bt).lower() / arb(F['U0'].norm()) - SQ2 * arb(s0) * arb(F['J0'].norm()))
    if not (b0lo > 0 and n0lo > 0):
        return float('inf'), dict(epsW=epsW, kappa=float('inf'), rho=float('inf'), arg='-', c=float('inf'), rt={})
    kappa = E.fup_arb(arb(vnorm) * arb(n0hi).sqrt() / arb(b0lo))
    pmx = P_MAX + 1
    c = E.fup_arb(((arb(n0hi) / arb(n0lo)) * (1 + arb(eT) / arb(n0lo))) ** pmx)
    # insertion factors (R9 v1_1): max(Rop_e, 1) for every horizontal object (as in cs33f), 1 + |alpha_e| for vertical ones
    f = {e_: (max(float(up(max(A['gmax'][e_] - A['al'][e_], A['al'][e_]))), 1.0) if e_ in HORIZ else float(up(1.0 + abs(A['al'][e_]))))
         for e_ in TYPES}
    rho, arg = 1.0, '-'
    rt = {}                                                                  # v1_6: rho per object type, printed
    for x in dict.fromkeys(names):
        if x not in F:
            continue
        lo = fv_lower(F[x])
        if x[0] == 'U' and x[1:].isdigit():
            a = int(x[1:])
            r = E.fup_arb((arb(n0hi) / arb(min(E.fdn_arb(sb['I'][a][1]) for sb in SBs))).sqrt()) if a < NCERT else 1.0
        else:
            parts = x.split('_')
            if x[0] == 'J' or x in ('u1', 'Tu1'):
                sig = F[x].norm()
            elif parts[0] == 'I':
                sig = f[parts[1]] * F['J%s' % parts[2]].norm()
            elif parts[0] == 'P':
                sig = f[parts[1]] * F['J%d' % (int(parts[2]) + 1)].norm()
            elif parts[0] == 'Y':
                sig = f[parts[1]] * (F['u1'] if parts[1] in HORIZ else F['Tu1']).norm()
            elif parts[0] == 'TY':
                sig = f[parts[1]] * F['Tu1'].norm() * (1.0 if parts[1] in HORIZ else float(up(A['pmax'] * n0hi)))
            else:
                sig = F[x].norm()
            r = float(up(sig / lo)) if lo > 0 else float('inf')
        if x[0] == 'U' and x[1:].isdigit():
            tk = 'U'
        elif x[0] == 'J' or x in ('u1', 'Tu1'):
            tk = 'J' if x[0] == 'J' else 'seed'
        else:
            tk = '_'.join(x.split('_')[:2])
        rt[tk] = max(rt.get(tk, 0.0), r) if r == r else float('inf')
        if not (r < float('inf')):                                        # nan or inf: no finite slack
            r = float('inf')
        if r > rho:
            rho, arg = r, x
    slack = E.fup_arb(arb(epss) / arb(n0lo) * (2 * pmx * arb(c) * arb(kappa) * arb(rho) + (arb(c) * arb(kappa) * arb(rho)) ** 2)
                      * (1 + arb(1e-6)))
    if not (pmx ** 2 * epss / n0lo <= 1e-6):
        slack = float('inf')
    return slack, dict(epsW=epsW, kappa=kappa, rho=rho, arg=arg, c=c, rt=rt)
