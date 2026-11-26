

def family_extra(SP, F, A):
    """vectors for the Delta bounds: RU_e_a = (R_e - alpha_e) u_a (horizontal) (the vertical products XU are in family_common),
    and the centred end vectors W'_A for the same-column end column"""
    gT, gmax, al, step = A['gT'], A['gmax'], A['al'], A['step']
    L = SP['L']
    for a in range(NCERT):
        ua = C.fv_trunc(SP['modes'][a]['u'], K_F)
        for e in HORIZ:
            F['RU_%s_%d' % (e, a)] = C.fv_comb(1.0, C.fv_diag(gT[e], ua, gmax[e], L, K_F), -al[e], ua)
    a1, a3 = al['tv'], al['bv']
    # Wc_* below are left over from the earlier same-column scope: computed, never read (not in names, no effect on rho)
    F['Wc_tv'] = C.fv_comb(1.0, F['W_tv'], -a1, F['J0'])
    F['Wc_bv'] = C.fv_comb(1.0, F['W_bv'], -a3, F['J0'])
    t = C.fv_comb(1.0, F['W_tb'], -a1, F['W_bv'])
    t = C.fv_comb(1.0, t, -a3, F['W_tv'])
    F['Wc_tb'] = C.fv_comb(1.0, t, a1 * a3, F['J0'])
    return F


def objects():
    """(e, p, J name, I' name, T~J name, T~I' name); p = None is the infinity object (p >= PE[e])"""
    obs = []
    for e in TYPES:
        for p in range(PE[e]):
            obs.append((e, p, 'J%d' % p, 'I_%s_%d' % (e, p), 'J%d' % (p + 1), 'P_%s_%d' % (e, p)))
        obs.append((e, None, 'u1', 'Y_' + e, 'Tu1', 'TY_' + e))
    return obs


def modecoef(ips, SB, v, tb, ti, ext=None):
    """<chi_a, v> for the certified a: <u_a, v>/|u_a| +- sqrt2 s_a |v|; ext: plant data replacing mode 1 (P-VEC). (PAR): exactly 0 for an
    odd mode a and a rho-even object v (chi_a is rho-odd, v is rho-even)"""
    res = []
    for a in SB['cert']:
        if MODEPAR[0][a] < 0 and rho_even(v):
            res.append(arb(0))
            continue
        if ext is not None and a == 1:
            ip, nu, s = ext(v, tb, ti)
        else:
            ua = 'U%d' % a
            ip, nu, s = ips.val(ua, v, tb, ti), ips.val(ua, ua, tb, ti).sqrt(), SB['s'][a]
        res.append(ip / nu + arb(0, E.fup_arb(SQ2 * s * ips.norm(v))))
    return res


def objdata(ips, SB, ob, tb, ti, ext=None):
    """Lambda^2 data of an object: X_ab = j_a i_b - j_b i_a (certified a < b), |X^perp| <= |J_C||I_perp| + |J_perp||I|, |X| <= |J||I|"""
    e, p, Jn, In = ob[:4]
    j, i = modecoef(ips, SB, Jn, tb, ti, ext), modecoef(ips, SB, In, tb, ti, ext)
    nc = len(j)
    X = {(a, b): j[a] * i[b] - j[b] * i[a] for a in range(nc) for b in range(a + 1, nc)}
    nJ2, nI2 = ips.val(Jn, Jn, tb, ti).upper(), ips.val(In, In, tb, ti).upper()
    jp2 = amax(arb(0), (nJ2 - sum(((x * x).lower() for x in j), arb(0))).upper())
    ip2 = amax(arb(0), (nI2 - sum(((x * x).lower() for x in i), arb(0))).upper())
    perp = (nJ2.sqrt() * ip2.sqrt() + jp2.sqrt() * nI2.sqrt()).upper()
    return dict(X=X, perp=perp, nl=(nJ2 * nI2).sqrt().upper(), j=j, i=i)
