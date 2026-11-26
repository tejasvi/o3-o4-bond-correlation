#!/usr/bin/env python3
"""px08_tau_d3b_v1_1.py -- pk08: the certified upper end tau_hi of Lemma B's tau (HS_TYPEB_LEMMA_NOTE_v1_1 6d0864e5, B6
3684b492, closed ba362538) for N in {3, 4}, uniform over J >= 300, written as TAU_D3B_v1.kv, the TAU_SOURCE of SPEC_HS_INV_NORMX_v1_2_ADD2_1
(2ad2cc4c). Revises the unrun, unfrozen draft px08_tau_d3b_v1.py (never hashed or cited).
  1 + tau^2 = lambda_0 v_0^2/<u,w>^2 = (1 + R_w^2)/RQ (B6), RQ = ||w||^2/(lambda_0 v_0^2) = I_free RQ_h/(lambda~_0 I_1col), where
  I_free = ||w||^2/main_free, lambda~_0 = lambda_0/lambda_h, I_1col = v_0^2/main_1col and RQ_h = main_free/(lambda_h main_1col) =
  PR/15^((N-1)/2). Since I_1col < 1: 1 + tau^2 <= (1 + R_w,hi^2)/RQ_lo, RQ_lo = I_free,lo RQ_h,lo/lambda~_0,hi.
Inputs, each pinned by the full sha256 of the bytes parsed (C-SRC):
  - I_free from pk03's certified endw records (|I_free(J) - sum_k a_k t^k| <= err for every J >= 300), bound by the m3_run_v1_7 asm
    outputs (RECORD line, VERDICT VALID); its definition from pk10 endw.py l.4 and the free grid of l.17-19 (C-DEF);
  - U_N from S4_U_CERTIFIED_v3 (tr_H T^2/lambda_h^2 <= U_N for every J >= 300), so lambda~_0 <= U_N^(1/2);
  - PR = pref_arb(N) from the strip graphs (px08_m2bc4 l.448-484, a COPY block, C-COPY), checked against the TRB record (C-PREF);
  - R_w,hi = the largest Rw_hi over the 904 pieces per N of pk07's certified export (bound by its run output), which tile [300, inf).
The written chain: N*_I_FREE_LO and N*_RQH_LO lie below the arb lower ends; N*_LAMBDA0T_HI^2 >= N*_U_USED; N*_RQ_LO <= I_FREE_LO RQH_LO/
LAMBDA0T_HI; N*_ONE_PLUS_TAU2_HI >= (1 + RW_HI^2)/RQ_LO; N*_TAU_HI^2 >= ONE_PLUS_TAU2_HI - 1; the last four in exact rationals (C-ROUND).
Checks with plants that must fire: C-SRC, C-BIND, C-COPY, C-DEF, C-FREE15, C-PREF, C-ULIT, C-S9FIELDS, C-ENDW, C-COVER (plants: the maximum
over a strict subset of the pieces, a piece replaced), C-ROUND (plants: each step's direction flipped), C-RQ1, C-I1COL (a control).
Usage: px08_tau_d3b_v1_1.py run
"""
import sys, os, json, hashlib, resource, signal, time
from fractions import Fraction

if len(sys.argv) != 2 or sys.argv[1] != 'run':
    print('usage: px08_tau_d3b_v1_1.py run')
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (60, 65))

CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk08'
OUTD = OWN + '/out'
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(OUTD, '%s_run.out' % LABEL)
REC_NAME = 'TAU_D3B_v1.kv'
REC_PATH = os.path.join(OUTD, REC_NAME)
for p_ in (OUT_PATH, REC_PATH):
    if not (os.path.isdir(OUTD) and os.path.realpath(os.path.dirname(p_)) == os.path.realpath(OUTD)
            and os.path.realpath(OUTD).startswith(os.path.realpath(OWN) + os.sep)):
        print('output directory check failed for %s' % p_)
        sys.exit(2)
FH = open(OUT_PATH, 'x')


def out(line):
    FH.write(line + '\n')
    FH.flush()


def _on_xcpu(signum, frame):
    out('CPU-STOP (SIGXCPU)')
    out('VERDICT INVALID')
    FH.close()
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
from flint import arb, arb_mat, ctx
ctx.prec = 128

# ==== COPY px08_m2bc4.py:6527d21b l.448-484 BEGIN ====
AEX = (3 + arb(21).sqrt()) / 6
BEX = (3 * arb(5).sqrt() - arb(21).sqrt()) / 12


def strip_graph(ncols, a, b):
    E = {}
    for j in range(ncols):
        T, Mv, B = 3 * j, 3 * j + 1, 3 * j + 2
        if j == 0 or j == ncols - 1:
            E[(T, Mv)] = a
            E[(Mv, B)] = a
            if b > 0:
                E[(T, B)] = b
        else:
            E[(T, Mv)] = arb(1)
            E[(Mv, B)] = arb(1)
        if j < ncols - 1:
            for r in range(3):
                E[(3 * j + r, 3 * (j + 1) + r)] = arb(1)
    return 3 * ncols, E


def pref_arb(N):
    def detred(ncols):
        V, Ed = strip_graph(ncols, AEX, BEX)
        L = arb_mat(V, V)
        for (u, v), c in Ed.items():
            L[u, u] += c
            L[v, v] += c
            L[u, v] -= c
            L[v, u] -= c
        S = arb_mat(V - 1, V - 1)
        for i in range(V - 1):
            for j in range(V - 1):
                S[i, j] = L[i + 1, j + 1]
        return S.det()
    return (detred(3) / detred(2)) ** (arb(N - 1) / 2)
# ==== COPY END ====

ENDW = {4: 'pk03/out/m3_endw_N4_J300_v1_7.json', 3: 'pk03/out/m3_endw_N3_J300_v1_7.json'}
M3ASM = {4: 'pk03/out/m3_run_v1_7_asm.4.out', 3: 'pk03/out/m3_run_v1_7_asm.3.out'}
U_REC = 'pk08/S4_U_CERTIFIED_v3.md'
S9EXP = 'pk07/out/export_kt_s9h_v1_2_vsweep.kv'
S9RUN = 'pk07/out/out_kt_s9h_v1_2_vsweep.out'
M2BC4 = 'pk08/px08_m2bc4.py'
ENDWPY = 'pk10/scripts/endw.py'
TRB = 'pk08/S4_TRB_CERTIFIED_v1.md'
NOTE = 'pk08/HS_TYPEB_LEMMA_NOTE_v1_1.md'
ADD2 = 'pk15/SPEC_HS_INV_NORMX_v1_2_ADD2_1.md'
S8SPEC = 'pk11/SPEC_S8_CERT_v1.md'
HSREC = 'pk08/out/HS_INV_NORMX_v1_d3d4.kv'
PINS = {
    ENDW[4]: '436a143918fa2ebaa68ee3d16fab632c27bd29b822d4c7052c92dc257eaf88af',
    ENDW[3]: '5e94d11eea2e6f55e7db781e02c197649ec6f10d8ab15a8f3508805642ed7885',
    M3ASM[4]: 'a5b294f364f9399b9d12f89af6ce1a1e598b8b424bc6e60d35e122ebd1391b97',
    M3ASM[3]: '18964e97c320395f44b5923d132b1ac65c95b935cc8708a50e197076cc24e0dc',
    U_REC: 'eb98948365fa35498206c9f1b80c6d98d421f69b9dca6c245f3f2d1198112751',
    S9EXP: '10f3c3d9a18b9c7a596121a8dbec7d2b82afb366704845a7c00e066c8bf6d4f6',
    S9RUN: '58814f7f59dd0d8e9d16b73084b3cc5072f94fb1138300a112e0e49ff017835f',
    M2BC4: '6527d21b7661a355c6534cc055f1fb8f3ae74be9256dbd6a3c65067ca6a34a17',
    ENDWPY: '1c4efd9409470625309a8100bcb207165ee2732031c145f340068d79003af073',
    TRB: '2c17c287c0affbfe0e0fcbd8097edff2258ea1109d91381d6206a11d4efdd694',
    NOTE: '801099463aa4dff112c1bc2078c943f8aff15ecdcf9738aed1a7d9f2f03f0e53',
    ADD2: '89216d7961dc7df87110c96fd4776993b646270cc26e3e0e2ccc439046de2c7e',
    S8SPEC: '3d4276002e175d5db717cbfed07deab5b9f779b791972b9b95b0a17bc851ffc1',
    HSREC: '45a2ab00dcbe47cf6873e5b12db69a1ff8ae3171c84abbc57c5ee43f8a39b343',
}
ULIT = {4: '1.033200684443', 3: '1.032809143879'}
PRLIT = {4: '4.44264196945e+1', 3: '1.25437544346e+1'}
S9_FIELDS = 'jlo jhi c5_lo vSv_p_lo vSv_m_hi rp_lo rho_hi rho1_hi vp2_lo vp2_hi vm2_hi Bp_hi Bm_hi cx_lo r2_hi ro_hi Rw_hi c_lo c_hi'
ENDW_L4 = 'I_free = <V 1, K V 1>/main_free (both columns free ends)'
ENDW_H = 'H = {(0, 3): 1.0, (1, 4): 1.0, (2, 5): 1.0}'
ENDW_EF = 'Efree = dict(H); Efree.update({(0, 1): 1.0, (1, 2): 1.0, (3, 4): 1.0, (4, 5): 1.0})'
EDGES_FREE = {(0, 3), (1, 4), (2, 5), (0, 1), (1, 2), (3, 4), (4, 5)}
S8_L106 = 'w = K^{1/2} V 1, w-hat = w / <u, w>, eps_d = S^d Q0 w-hat, with |eps_0| = R_w.'
S8_L398 = 'FIELDS = ' + S9_FIELDS + '.'
NOTE_L78 = ('With R_w = ||Q0 w-hat|| (S8), <u,w>^2 = ||w||^2/(1 + R_w^2), so tau^2 = (1 + R_w^2)/RQ - 1 with RQ = ||w||^2/(lambda_0 v_0^2) '
            'in (0, 1].')
LHDEF = "S4-U's lambda_h equals SPEC v1_2's lambda_h := exp(logmain_N(J) - logmain_D(J)) at the same J:"
JS = (300, 1000, 10 ** 4, 10 ** 6)
DATA = {}


def c_src(pins):
    ok = True
    for rel, want in sorted(pins.items()):
        try:
            with open(os.path.join(CODEDIR, rel), 'rb') as fh:
                b = fh.read()
        except OSError:
            b = None
        if b is None or hashlib.sha256(b).hexdigest() != want:
            ok = False
        DATA[rel] = b
    return ok


def lines_of(rel):
    return DATA[rel].decode('utf-8').split('\n')


def key_once(rel, key):
    vals = [ln[len(key) + 3:] for ln in lines_of(rel) if ln.startswith(key + ' = ')]
    return vals[0] if len(vals) == 1 else None


def fa(F):
    return arb(F.numerator) / arb(F.denominator)


def to_fr(x):
    """an exact arb point (an endpoint) as a Fraction"""
    m, e = x.man_exp()
    m, e = int(m), int(e)
    return Fraction(m) * (Fraction(2) ** e if e >= 0 else Fraction(1, 2 ** (-e)))


def dec(x, sig, up):
    """the decimal with sig significant digits next to x (a positive Fraction): the smallest >= x if up, else the largest <= x"""
    k = 0
    while Fraction(10) ** (k + 1) <= x:
        k += 1
    while Fraction(10) ** k > x:
        k -= 1
    e = sig - 1 - k
    q = x * Fraction(10) ** e
    n = -((-q.numerator) // q.denominator) if up else q.numerator // q.denominator
    s = str(n)
    if e <= 0:
        return s + '0' * (-e)
    if len(s) <= e:
        s = '0' * (e - len(s) + 1) + s
    return s[:-e] + '.' + s[-e:]


def within(x, y, tol):
    d = x - y
    return to_fr(d.upper()) < tol and to_fr(d.lower()) > -tol


def c_bind(endw_sha, exp_sha):
    ok = True
    for N in (4, 3):
        ls = lines_of(M3ASM[N])
        ok = ok and [x for x in ls if x.startswith('VERDICT')] == ['VERDICT VALID']
        ok = ok and ls.count('RECORD %s %s' % (os.path.basename(ENDW[N]), endw_sha[N])) == 1
    rs = lines_of(S9RUN)
    ok = ok and [x for x in rs if x.startswith('VERDICT')] == ['VERDICT VALID']
    ok = ok and sum(x.startswith('EXPORT %s sha256 %s (' % (S9EXP, exp_sha)) for x in rs) == 1
    g = [x for x in rs if x.startswith('C-GRID-ALL:')]
    ok = ok and len(g) == 1 and 'both N, 904 pieces each' in g[0] and ' -> PASS; PLANT-GRID-ALL ' in g[0] and g[0].rstrip().endswith('-> FIRES')
    ok = ok and key_once(S9EXP, 'RUN_VERDICT') == 'VALID' and key_once(S9EXP, 'EXPORT_STATUS') == 'CERTIFIED'
    return ok


def c_copy(plant=False):
    with open(os.path.abspath(__file__), 'rb') as fh:
        mine = fh.read().split(b'\n')
    tag = b'# ==== COPY px08_m2bc4.py:6527d21b l.448-484 BEGIN ===='
    if mine.count(tag) != 1:
        return False
    b = mine.index(tag)
    e = mine.index(b'# ==== COPY END ====', b)
    blk = mine[b + 1:e]
    if plant:
        blk = blk[:-1] + [blk[-1] + b'#']
    return blk == DATA[M2BC4].split(b'\n')[447:484]


def c_def(edges):
    el, s8, nt = lines_of(ENDWPY), lines_of(S8SPEC), lines_of(NOTE)
    ok = (len(el) > 19 and ENDW_L4 in el[3] and el.count(ENDW_H) == 1 and el.count(ENDW_EF) == 1 and el[16] == ENDW_H
          and el[18] == ENDW_EF and edges == EDGES_FREE)
    ok = ok and len(s8) > 398 and S8_L106 in s8[105] and S8_L398 in s8[397] and len(nt) > 78 and NOTE_L78 in nt[77]
    lh = key_once(HSREC, 'LAMBDA_H_DEF')
    return ok and lh is not None and lh.startswith(LHDEF) and 'pref_arb(N) = (detred(3)/detred(2))^((N-1)/2)' in lh


def detred_g(V, E):
    L = arb_mat(V, V)
    for (u, v), c in E.items():
        L[u, u] += c
        L[v, v] += c
        L[u, v] -= c
        L[v, u] -= c
    S = arb_mat(V - 1, V - 1)
    for i in range(V - 1):
        for j in range(V - 1):
            S[i, j] = L[i + 1, j + 1]
    return S.det()


def c_ulit(lits):
    return all(key_once(U_REC, 'N%d_U' % N) == lits[N] for N in (4, 3))


def c_s9fields(fields):
    return key_once(S9EXP, 'FIELDS') == fields and fields.split()[16] == 'Rw_hi'


def endw_check(d, N):
    it = d.get('items', {}).get('I_free', {})
    try:
        ok = (d.get('format') == 'M3_RECORD_v1' and d.get('N') == N and d.get('J_REF') == 300
              and 'for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err' in d.get('claim', '')
              and it.get('kind') == 'entry' and it.get('alias_of') is None and it.get('parity') == 'free' and it.get('a0_exact') == '1'
              and len(it['ak']) == 4 and len(it['ak_rad']) == 4 and it['ak'][0] == 1.0 and it['ak_rad'][0] == 0.0
              and all(isinstance(x, float) for x in it['ak'] + it['ak_rad']) and isinstance(it['err'], float) and it['err'] > 0
              and all(x >= 0 for x in it['ak_rad']))
    except (KeyError, TypeError):
        ok = False
    return ok


def ifree_end(a, r, err, sgn):
    """sgn = -1: the lower end of sum_k (a_k - r_k) t^k - err over the ball t in [0, 1/300] (t^k by multiplication);
    sgn = +1: the upper end of sum_k (a_k + r_k) t^k + err (the flipped direction, for PLANT-ROUND)"""
    t = arb(0).union(arb(1) / 300)
    p, tk = arb(0), arb(1)
    for k in range(4):
        p = p + (arb(a[k]) + sgn * arb(r[k])) * tk
        tk = tk * t
    return (p - arb(err)).lower() if sgn < 0 else (p + arb(err)).upper()


def s9_pieces(N):
    """[(index, jlo, jhi, Rw_hi)] of N's piece lines in file order, as the export's strings"""
    pre = 'N%d_P' % N
    res = []
    for ln in lines_of(S9EXP):
        if ln.startswith(pre) and ' = ' in ln:
            key, val = ln.split(' = ', 1)
            if len(key) == len(pre) + 4 and key[len(pre):].isdigit():
                f = val.split(' | ')[0].split()
                res.append((int(key[len(pre):]), f[0], f[1], f[16] if len(f) == 19 else None))
    return res


def c_cover(pcs, N):
    """the pieces tile [300, inf): N*_PIECES = 904 lines, indices 0..903 in order, the first jlo 300.0, each jhi the next jlo, jlo < jhi,
    the last jhi inf"""
    if key_once(S9EXP, 'N%d_PIECES' % N) != '904' or len(pcs) != 904 or any(p[3] is None for p in pcs):
        return False
    if [p[0] for p in pcs] != list(range(904)) or pcs[0][1] != '300.0' or pcs[-1][2] != 'inf':
        return False
    return all(pcs[i][2] == pcs[i + 1][1] for i in range(903)) and all(float(p[1]) < float(p[2]) for p in pcs)


def rw_max(pcs, N):
    """(ok, the largest Rw_hi as a Fraction, its index, its string): refused unless the pieces pass C-COVER"""
    if not c_cover(pcs, N):
        return False, None, None, None
    m, at, s = None, None, None
    for idx, jl, jh, rw in pcs:
        v = Fraction(rw)
        if v <= 0:
            return False, None, None, None
        if m is None or v > m:
            m, at, s = v, idx, rw
    return True, m, at, s


def rho(nu2, J):
    """sqrt(2 pi J) e^-J I_(nu2/2)(J), arb"""
    return (2 * arb.pi() * J).sqrt() * arb(J).bessel_i(arb(nu2) / 2, scaled=True)


def overlap(x, y):
    return x.lower() <= y.upper() and y.lower() <= x.upper()


def i1col_id(nu2):
    return all(overlap(rho(nu2, J), 1 - arb(-2 * J).exp()) for J in JS)


def i1col_lt1(nu2):
    return all(rho(nu2, J).upper() < 1 for J in JS)


def i1col_mono(nu2):
    return all(rho(nu2, J).upper() < rho(1, J).lower() for J in JS)


def main():
    t0 = time.time()
    with open(os.path.abspath(__file__), 'rb') as fh:
        code_sha = hashlib.sha256(fh.read()).hexdigest()
    out('%s start; code sha256 %s' % (LABEL, code_sha))
    res, plants = {}, {}
    res['C-SRC'] = c_src(PINS)
    out('C-SRC: %d pinned inputs, sha256 of the bytes parsed -> %s' % (len(PINS), 'PASS' if res['C-SRC'] else 'FAIL'))
    if not res['C-SRC']:
        out('VERDICT INVALID')
        return 1
    good = dict(DATA)
    bad = dict(PINS)
    bad[U_REC] = bad[U_REC][:-1] + ('0' if bad[U_REC][-1] != '0' else '1')
    plants['PLANT-SRC'] = not c_src(bad)
    DATA.clear()
    DATA.update(good)
    esha = {N: PINS[ENDW[N]] for N in (4, 3)}
    res['C-BIND'] = c_bind(esha, PINS[S9EXP])
    plants['PLANT-BIND'] = not c_bind({4: esha[4][:-1] + ('0' if esha[4][-1] != '0' else '1'), 3: esha[3]}, PINS[S9EXP])
    res['C-COPY'] = c_copy()
    plants['PLANT-COPY'] = not c_copy(True)
    edges = set(strip_graph(2, arb(1), arb(0))[1])
    res['C-DEF'] = c_def(edges)
    plants['PLANT-DEF'] = not c_def(edges | {(0, 2)})
    res['C-FREE15'] = within(detred_g(*strip_graph(2, arb(1), arb(0))), arb(15), Fraction(1, 10 ** 30))
    plants['PLANT-FREE15'] = not within(detred_g(*strip_graph(2, arb(1), arb(1))), arb(15), Fraction(1, 10 ** 30))
    pref = {N: pref_arb(N) for N in (4, 3)}
    res['C-PREF'] = (all(within(pref[N], fa(Fraction(PRLIT[N])), Fraction(1, 10 ** 9)) for N in (4, 3))
                     and all(key_once(TRB, 'N%d_PR' % N) == PRLIT[N] for N in (4, 3)))
    plants['PLANT-PREF'] = not within(pref[4], fa(Fraction(PRLIT[4]) * (1 + Fraction(1, 10 ** 6))), Fraction(1, 10 ** 9))
    res['C-ULIT'] = c_ulit(ULIT)
    plants['PLANT-ULIT'] = not c_ulit({4: '1.033200684444', 3: ULIT[3]})
    res['C-S9FIELDS'] = c_s9fields(S9_FIELDS)
    plants['PLANT-S9FIELDS'] = not c_s9fields(S9_FIELDS.replace('Rw_hi', 'Rw'))
    res['C-I1COL'] = i1col_id(1) and i1col_lt1(2) and i1col_mono(2)
    plants['PLANT-I1COL'] = not i1col_id(0) and not i1col_lt1(0) and not i1col_mono(0)
    for k in ('C-BIND', 'C-COPY', 'C-DEF', 'C-FREE15', 'C-PREF', 'C-ULIT', 'C-S9FIELDS', 'C-I1COL'):
        out('%s -> %s' % (k, 'PASS' if res[k] else 'FAIL'))
    out('INFO C-I1COL control (the bound uses I_1col < 1, proved in the record text): sqrt(2 pi J) e^-J I_nu(J) at J = %s: nu = 1/2: %s; '
        'nu = 1: %s' % (', '.join(str(J) for J in JS), ', '.join(rho(1, J).str(12) for J in JS), ', '.join(rho(2, J).str(12) for J in JS)))
    rows = {}
    okE = okC = okR = okQ = True
    plE = plC = plR = plQ = True
    for N in (4, 3):
        d = json.loads(DATA[ENDW[N]].decode('utf-8'))
        e_ok = endw_check(d, N)
        d_bad = dict(d)
        d_bad['J_REF'] = 301
        plE = plE and not endw_check(d_bad, N)
        pcs = s9_pieces(N)
        c_ok, rw, at, rws = rw_max(pcs, N)
        if at is not None:
            sub = [p for p in pcs if p[0] != at]
            dup = list(pcs)
            dup[at] = pcs[at - 1] if at > 0 else pcs[at + 1]
        else:
            sub, dup = pcs[:-1], pcs
        plC = plC and not rw_max(sub, N)[0] and not rw_max(dup, N)[0]
        okE, okC = okE and e_ok, okC and c_ok
        if not (e_ok and c_ok):
            okR = okQ = False
            continue
        it = d['items']['I_free']
        a, r, err = it['ak'], it['ak_rad'], it['err']
        I_lo = ifree_end(a, r, err, -1)
        I_hi = ifree_end(a, r, err, +1)
        lamb = fa(Fraction(ULIT[N])).sqrt()
        RQh = pref[N] / (arb(15) ** (arb(N - 1) / 2))
        U = Fraction(ULIT[N])
        rwF = Fraction(rw)

        def chain(Iw, Lw, Hw, qup=False, oup=True, tup=True):
            Q = dec(Fraction(Iw) * Fraction(Hw) / Fraction(Lw), 15, qup)
            O = dec((1 + rwF * rwF) / Fraction(Q), 12, oup)
            tb = (fa(Fraction(O)) - 1).sqrt()
            T = dec(to_fr(tb.upper() if tup else tb.lower()), 12, tup)
            return dict(I=Iw, L=Lw, H=Hw, Q=Q, O=O, T=T)

        def c_round(w):
            I_, L_, H_, Q_, O_, T_ = (Fraction(w[k]) for k in 'ILHQOT')
            return (I_ <= to_fr(I_lo) and L_ * L_ >= U and L_ > 0 and H_ <= to_fr(RQh.lower()) and 0 < Q_ <= I_ * H_ / L_
                    and O_ >= (1 + rwF * rwF) / Q_ and T_ >= 0 and T_ * T_ >= O_ - 1)

        Iw = dec(to_fr(I_lo), 15, False)
        Lw = dec(to_fr(lamb.upper()), 15, True)
        Hw = dec(to_fr(RQh.lower()), 15, False)
        W = chain(Iw, Lw, Hw)
        r_ok = c_round(W)
        flips = [c_round(chain(dec(to_fr(I_hi), 15, True), Lw, Hw)),
                 c_round(chain(Iw, dec(to_fr(lamb.lower()), 15, False), Hw)),
                 c_round(chain(Iw, Lw, dec(to_fr(RQh.upper()), 15, True))),
                 c_round(chain(Iw, Lw, Hw, qup=True)),
                 c_round(chain(Iw, Lw, Hw, oup=False)),
                 c_round(chain(Iw, Lw, Hw, tup=False))]
        p_r = not any(flips)
        q_ok = 0 < Fraction(W['Q']) < 1
        p_q = not (0 < 2 * Fraction(W['Q']) < 1)
        okR, plR, okQ, plQ = okR and r_ok, plR and p_r, okQ and q_ok, plQ and p_q
        rows[N] = dict(W, rws=rws, at=at)
        out('N%d: I_free,lo %s; lambda~_0,hi %s (U_N %s); RQ_h in %s, RQ_h,lo %s; R_w,hi %s (N%d_P%04d of %d pieces); RQ_lo %s; '
            '1 + tau^2 <= %s; tau_hi %s; flipped steps refused %d of 6' % (N, W['I'], W['L'], ULIT[N], RQh.str(15), W['H'], rws, N, at,
                                                                         len(pcs), W['Q'], W['O'], W['T'], 6 - sum(flips)))
    res['C-ENDW'], res['C-COVER'], res['C-ROUND'], res['C-RQ1'] = okE, okC, okR, okQ
    plants['PLANT-ENDW'], plants['PLANT-COVER'], plants['PLANT-ROUND'], plants['PLANT-RQ1'] = plE, plC, plR, plQ
    for k in ('C-ENDW', 'C-COVER', 'C-ROUND', 'C-RQ1'):
        out('%s -> %s' % (k, 'PASS' if res[k] else 'FAIL'))
    for k in sorted(plants):
        out('%s -> %s' % (k, 'FIRED' if plants[k] else 'MISSED'))
    if not (all(res.values()) and all(plants.values()) and len(rows) == 2):
        out('VERDICT INVALID')
        return 1

    def p(rel):
        return '%s:%s' % (rel, PINS[rel])
    R = ['# TAU_D3B_v1: the certified upper end of Lemma B\'s tau (the type-B rows of D3 at d_L = -1) for N in {3, 4} and every J >= 300;',
         '# the TAU_SOURCE of SPEC_HS_INV_NORMX_v1_2_ADD2_1. Format S4U_KV_v1 ("KEY = value"; lines starting with # are comments). Values',
         '# named _HI are upper ends rounded up, _LO lower ends rounded down; N*_RW_HI is the export\'s own decimal.',
         'RECORD = TAU_D3B_v1', 'FORMAT = S4U_KV_v1', 'EXPORT_STATUS = CERTIFIED', 'PRODUCER = pk08',
         'CODE = pk08/%s.py:%s' % (LABEL, code_sha),
         'LEMMA_NOTE_D3B = ' + p(NOTE), 'SPEC_ADD2_1 = ' + p(ADD2),
         'CLAIM = for N in {3, 4} and every J >= 300: tau(J) <= N*_TAU_HI and 1 + tau(J)^2 <= N*_ONE_PLUS_TAU2_HI, where tau^2 = lambda_0 '
         'v_0^2/<u,w>^2 - 1 is Lemma B\'s tau (LEMMA_NOTE_D3B sect. 0 and B6; OPERATOR_D3B of SPEC_ADD2_1)',
         'CHAIN = 1 + tau^2 = (1 + R_w^2)/RQ (B6), RQ = ||w||^2/(lambda_0 v_0^2) = I_free RQ_h/(lambda~_0 I_1col), with I_free = ||w||^2/main_free, '
         'lambda~_0 = lambda_0/lambda_h, I_1col = v_0^2/main_1col and RQ_h = main_free/(lambda_h main_1col); since I_1col < 1 (I1COL_DEF), '
         '1 + tau^2 <= (1 + R_w,hi^2)/RQ_lo with RQ_lo = I_free,lo RQ_h,lo/lambda~_0,hi',
         'MAIN_TERMS = each main term is the Gaussian (matrix-tree) term of its graph G (V vertices, edge weights c_e, normalized measure on '
         'S^(N-1)): main(G) = |S^(N-1)|^-(V-1) (2 pi/J)^((N-1)(V-1)/2) det_red(L_G)^-((N-1)/2). The ratios I_free, lambda~_0, I_1col and RQ do '
         'not depend on the measure normalization, and in RQ_h the area and 2 pi/J powers cancel (V - 1: 5 = (8 - 5) + 2)',
         'I_FREE_DEF = ||w||^2 = <V 1, K V 1> (w = K^(1/2) V 1) and I_free = <V 1, K V 1>/main_free (pk10 endw.py l.4; the free 2 x 3 grid of '
         'l.17-19 is strip_graph(2, 1, 0), C-DEF; its det_red is 15, C-FREE15); the endw records claim |I_free(J) - sum_k a_k t^k| <= err for '
         'every J >= 300, t = 1/J, t = 0 included',
         'I_FREE_SOURCE = ' + ' ; '.join(p(x) for x in (ENDW[4], ENDW[3], M3ASM[4], M3ASM[3], ENDWPY)),
         'I_FREE_LO_RULE = N*_I_FREE_LO <= the arb lower end of sum_k (a_k - ak_rad_k) t^k - err over the ball t in [0, 1/300] (t^k by '
         'multiplication)',
         'LAMBDA0_DEF = lambda_0 = the top eigenvalue of T = Z Z* >= 0 on H, so lambda_0^2 <= tr_H T^2 <= U_N lambda_h^2 (S4_U_CERTIFIED_v3 '
         'CLAIM, every J >= 300) and lambda~_0 <= U_N^(1/2) <= N*_LAMBDA0T_HI (N*_LAMBDA0T_HI^2 >= N*_U_USED exactly); lambda_h is the one of '
         'HS_INV_NORMX_v1\'s LAMBDA_H_DEF (the 3- and 2-column strips with the ends (A_EX, B_EX))',
         'U_SOURCE = ' + p(U_REC) + ' ; ' + p(HSREC),
         'I1COL_DEF = v_0 = int e^(J(s.e - 1)) dsigma(s) over S^(N-1) (LEMMA_NOTE_D3B l.76-77) = Gamma(N/2) (2/J)^nu e^-J I_nu(J) with nu = '
         '(N-2)/2 (DLMF 10.32.2), and int V = v_0^2 (B6); main_1col = v_0,main^2 with v_0,main = (2 pi/J)^((N-1)/2)/|S^(N-1)|, so I_1col = '
         '(sqrt(2 pi J) e^-J I_nu(J))^2. N = 3: sqrt(2 pi J) e^-J I_1/2(J) = 1 - e^-2J < 1 (DLMF 10.39.1: I_1/2(z) = (2/(pi z))^(1/2) sinh z). '
         'N = 4: I_nu(J) decreases in nu >= 0 at fixed J > 0 (DLMF 10.37), so sqrt(2 pi J) e^-J I_1(J) < 1 - e^-2J; directly, by DLMF 10.32.2 '
         'at nu = 1, sqrt(2 pi J) e^-J I_1(J) = (2 J^3/pi)^(1/2) int_0^2 e^-Js (s (2 - s))^(1/2) ds < (2 J^3/pi)^(1/2) int_0^inf e^-Js '
         '(2 s)^(1/2) ds = 1. So I_1col < 1 for every J > 0 at N = 3 and 4, and the bound uses 1; C-I1COL is a numerical control at J = 300, '
         '1e3, 1e4, 1e6 (the N = 3 identity, the N = 4 value below 1, and I_1 < I_1/2)',
         'RQH_DEF = RQ_h = (d3/(15 d2))^((N-1)/2) = PR/15^((N-1)/2), d3/d2 = detred(3)/detred(2) of strip_graph(ncols, A_EX, B_EX) (the COPY '
         'block of px08_m2bc4 l.448-484, C-COPY; PR checked against the TRB record\'s N*_PR, C-PREF); det_red of the 1-column path is 1; the '
         'half-integer power in arb, N*_RQH_LO <= its lower end',
         'STRIP_SOURCE = ' + p(M2BC4) + ' ; ' + p(TRB),
         'RW_DEF = R_w = ||Q0 w-hat||, w-hat = w/<u,w> (SPEC_S8_CERT_v1 l.106), so <u,w>^2 = ||w||^2/(1 + R_w^2) (B6); N*_RW_HI = the largest '
         'Rw_hi (field 17 of the export\'s FIELDS) over the 904 pieces per N, which tile [300, inf) with no gap (C-COVER; pk07\'s '
         'C-GRID-ALL PASS)',
         'RW_SOURCE = ' + p(S9EXP) + ' ; ' + p(S9RUN) + ' ; ' + p(S8SPEC),
         'TAU_RULE = N*_RQ_LO <= N*_I_FREE_LO N*_RQH_LO/N*_LAMBDA0T_HI, N*_ONE_PLUS_TAU2_HI >= (1 + N*_RW_HI^2)/N*_RQ_LO and N*_TAU_HI^2 >= '
         'N*_ONE_PLUS_TAU2_HI - 1, each in exact rationals (C-ROUND)']
    for N in (4, 3):
        w = rows[N]
        R += ['N%d_I_FREE_LO = %s' % (N, w['I']),
              'N%d_U_USED = %s' % (N, ULIT[N]),
              'N%d_LAMBDA0T_HI = %s' % (N, w['L']),
              'N%d_RQH_LO = %s' % (N, w['H']),
              'N%d_RW_HI = %s' % (N, w['rws']),
              'N%d_RW_HI_PIECE = N%d_P%04d' % (N, N, w['at']),
              'N%d_RQ_LO = %s' % (N, w['Q']),
              'N%d_ONE_PLUS_TAU2_HI = %s' % (N, w['O']),
              'N%d_TAU_HI = %s' % (N, w['T'])]
    R.append('END = TAU_D3B_v1')
    with open(REC_PATH, 'x') as fh:
        fh.write('\n'.join(R) + '\n')
    with open(REC_PATH, 'rb') as fh:
        rsha = hashlib.sha256(fh.read()).hexdigest()
    ru = resource.getrusage(resource.RUSAGE_SELF)
    out('CPU %.2f s, wall %.2f s' % (ru.ru_utime + ru.ru_stime, time.time() - t0))
    out('VERDICT VALID')
    out('RECORD %s %s' % (REC_NAME, rsha))
    return 0


if __name__ == '__main__':
    rc = main()
    FH.close()
    sys.exit(rc)
