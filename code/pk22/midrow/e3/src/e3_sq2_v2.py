#!/usr/bin/env python3
"""e3_sq2_v2.py (pk22; item (3) part (6), the P0_LOG rows 4558, 4642, 4662 and 4690), made from the template e3_sq2_v2.tmpl.py by
make_e3_sq2_v2.py, which fills the pins by tool. e3_sq2_v1 (6b5eb72c, dry, on S9(b)'s laws of e1 and e3) for the kind xy: per R4 piece it turns
the certified M4 law of kt_cert_v1_9_xy's R_xy (pk23's M4XY_KV_v1 through its one sha-pinned reader m4xy_reader_v1_1, bound to m4xy_asm_v1_1's
output; the MOCK build: m4xy_reader_v1 on m4xy_asm_v1's mock output) into the second-order form of D2_DESIGN_v1_1 (pk25 e00fff5f
e03f2f79):
  R_xy(t) <= t R_hat,   R_xy(t)^2 <= t^2 c2_hi   (X = R_xy^2: X(0) = X_1 = 0),   for every J of the piece (t = 1/J; t = 0 on the last piece).
- R_xy's g piece is kt_cert_v1_9_xy_1's (it differs from kt_cert_v1_9_xy in C-REP-FIX's nR0 tolerance and the names only; the same values).
- The law (the reader's law_balls; s = 300/J; J >= J_MIN(N), the record's N<N>_XY_JMIN): L = (sqrt(near^2 + far) + gB)/D,
  near = sum_{k=0..3} s^k M_k + nD + nR0 + tailX + tailB + ann.
- The t^0 term s^0 M_0 bounds the order-0 residual over the m0 ball. kt_cert_v1_8_xy carries m0 = m0* as the arb ball solution of the B0 Gram
  system (the x records come from its fork kt_cert_v1_8_xy_2, whose deltas from it touch
  only C-REP-X and the C-T0ZERO radius gate), and at m0 = m0* the order-0 residual is exactly 0: the xy source lies in the
  order-0 span of (psi, e1, e3, xy) (pk25's certified C10_RECORD_v1: C-SPAN, C-PURE10). Every other term encloses its value at m0*. So
  near' = near - M_0 bounds R_xy at m0*: R_xy(t) <= L'(J) = (sqrt(near'^2 + far) + gB)/D, with no bridge term (no beta, no nu_g).
- R_hat per piece = jlo L'(jlo): J L'(J) = (sqrt((J near')^2 + J^2 far) + J gB)/D is nonincreasing on J >= 300 under C-MONO-J (each term:
  300^k M_k J^(1-k) for k >= 1; J s^4 ~ J^-3; J e^(-c (J - 300)) once 1/c <= 300 for the tail rates c; J^2 far's items J^(2 + w + p) e^(-c (J - 300))
  once (2 + w + p)/c <= 300; J gB ~ J^(d + 1) e^(-rho_G J) once (d_max + 1)/rho_G <= 300), so its sup over a piece is its value at jlo, and at
  t -> 0 it tends to 300 M_1/D (C-LIMIT). c2_hi = R_hat^2 from the written R_hat (C-ROUND).
- R_hat_full per finite piece = jhi L(jlo), lemma-free (L nonincreasing); on the last piece it is unbounded ('inf').
Gates: C-SRC, C-MANIFEST (the M4XY files are rows of pk23's manifest), C-LOAD (the reader's load: binding, check, C-PINS), C-GRID,
C-JMIN-GRID (the first piece's jlo is the record's J_MIN(N) exactly), C-L300 (law_balls' L(300) equals the record's L300 within 1e-9),
C-MONO-J with PLANT-MONO-J, C-LIMIT, C-ROUND, C-LEMMA (C10_RECORD_v1 CERTIFIED with C-SPAN and C-PURE10, a row of its manifest; the x records
of kt_cert_v1_8_xy_2 VALID with C-T0ZERO PASS and PLANT-T0ZERO FIRES, rows of their run manifest). Writes midrow/e3/out/e3_sq2_v2_N<N>.json
(mode 'x'). A MOCK build (make_e3_sq2_v2.py --mock, on pk23's MOCK M4XY record) skips C-MANIFEST and C-LEMMA's x part and writes a MOCK
record (SCRATCH_mock_e3_sq2_v2_N<N>.json), never a certified one. Usage: e3_sq2_v2.py N"""
import hashlib
import importlib.util
import json
import os
import re
import sys
from fractions import Fraction as Fr
import flint

flint.ctx.prec = 256
arb, fmpq = flint.arb, flint.fmpq
if len(sys.argv) != 2 or sys.argv[1] not in ('4', '3'):
    print('usage: e3_sq2_v2.py N')
    sys.exit(2)
N = int(sys.argv[1])
W = '/mnt/g2/release/root/code'
MOCK = False
OUT = W + '/pk22/midrow/e3/out/%s_N%d.json' % ('SCRATCH_mock_e3_sq2_v2' if MOCK else 'e3_sq2_v2', N)
SRC = {
    'c10': ('/mnt/g2/release/root/code/pk25/c10/C10_RECORD_v1.kv',
        '29a4f3c67afc2b3e2611e37e3026def71d6ae819bcc2ee5ed34f678734bebb98'),
    'c10man': ('/mnt/g2/release/root/code/pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256',
        'bf8df39779ec0d3a797f13a67d73fd83a01ff27b437add8f84d7ab0c9884c183'),
    'm4asm_out': ('/mnt/g2/release/root/code/pk23/it3/m4xy/out/m4xy_asm_v1_1_cert.out',
        '3680f37d6c21ba66676f58d0b4ddb780920ae40115061b96b0464328d904cae9'),
    'm4kv': ('/mnt/g2/release/root/code/pk23/it3/m4xy/M4XY_KV_v1.txt',
        'f697229931f7e8b9de870c9438a1fc94719e6784af9b996248d99e82c436e631'),
    'm4man': ('/mnt/g2/release/root/code/pk23/it3/m4xy/MANIFEST_M4XY_V1_1_v1.sha256',
        '770f3f4d97ae8a56886a84320a4669caff24522ba30ca019ee76778614f64015'),
    'm4reader': ('/mnt/g2/release/root/code/pk23/it3/m4xy/m4xy_reader_v1_1.py',
        '52004e3da4f520cf7aa03ac9fe21358653aa1413035ee739ee86b9dadf6e9952'),
    'spectral': ('/mnt/g2/release/root/code/pk25/mr/v4/MR_SPECTRAL.kv',
        '4a609ccf717c0aedd9504ee4db47e7c98a679bc25df2ca2a187b415011470937'),
    'v18': ('/mnt/g2/release/root/code/pk22/midrow/e3/kt/kt_cert_v1_8_xy_2.py',
        '7f6d0e0f799618285cbf66dd91b698971f6e4b797128bb4603a91773a8e0328a'),
    'v18man': ('/mnt/g2/release/root/code/pk22/midrow/e3/kt/MANIFEST_V1_8_XY_2_X_v1.sha256',
        '522f9bbf029f9bae1acaa6f01d371c9e4896bfaca84f55c1d3feab4b337a6fd7'),
    'x3': ('/mnt/g2/release/root/code/pk22/midrow/e3/kt/out_kt_cert_v1_8_xy_2_x.xyn3.out',
        'ce8160d9f080a417c03774eadc01b36079d0e849d5ad29f593742163e632d392'),
    'x4': ('/mnt/g2/release/root/code/pk22/midrow/e3/kt/out_kt_cert_v1_8_xy_2_x.xyn4.out',
        'f79fa36e7cec4cf7e2113a11a425994c0dbc338190d5a6577c2a2a3c90d5d8f0'),
}
KINDS = ('xy',)
FAILS, NOFIRE = [], []


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def gate(name, ok, line):
    print('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'), flush=True)
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    print('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'), flush=True)
    if not fired:
        NOFIRE.append(name)


def fr_of(x):
    m, e = x.man_exp()
    m, e = int(m), int(e)
    return Fr(m) * (Fr(2) ** e) if e >= 0 else Fr(m, 2 ** (-e))


def ab(q):
    q = Fr(q)
    return arb(fmpq(q.numerator, q.denominator))


def hi_of(x):
    return fr_of(x.upper())


def dec_up(q):
    """the 17-significant-digit decimal at or above q >= 0, from exact integers."""
    q = Fr(q)
    if q <= 0:
        return '0'
    e = len(str(q.numerator)) - len(str(q.denominator))
    while Fr(10) ** e > q:
        e -= 1
    while Fr(10) ** (e + 1) <= q:
        e += 1
    v = q * Fr(10) ** (16 - e)
    n = (v.numerator + v.denominator - 1) // v.denominator
    if n >= 10 ** 17:
        n, e = (n + 9) // 10, e + 1
    s = str(n)
    txt = '%s.%se%s%02d' % (s[0], s[1:], '-' if e < 0 else '+', abs(e))
    assert Fr(txt) >= q, (txt, q)
    return txt


def man_rows(path):
    rows = {}
    for ln in open(path):
        if ln.strip():
            h_, p_ = ln.rstrip('\n').split('  ', 1)
            rows[p_] = h_
    return rows


shas = dict((k, sha(p)) for k, (p, _) in SRC.items())
gate('C-SRC', all(shas[k] == pin for k, (_, pin) in SRC.items()), '(%s)' % ', '.join('%s %s' % (os.path.basename(SRC[k][0]), shas[k][:16]) for k in SRC))
if FAILS:
    print('VERDICT INVALID (fails %s); no record written' % FAILS)
    sys.exit(3)
if MOCK:
    print('C-MANIFEST MOCK: pk23\'s MOCK record is not in a release manifest; not checked (this build writes a MOCK record only)')
else:
    man = man_rows(SRC['m4man'][0])
    rel = lambda k: os.path.relpath(SRC[k][0], os.path.dirname(SRC['m4man'][0]))
    relh = lambda k: os.path.relpath(SRC[k][0], W + '/pk23')     # pk23's release manifests list paths relative to pk23/
    gate('C-MANIFEST', all(man.get(SRC[k][0], man.get(rel(k), man.get(relh(k)))) == shas[k] for k in ('m4kv', 'm4reader', 'm4asm_out')),
         '(M4XY_KV_v1, %s and the asm output are rows of %s with these sha256s)' % (os.path.basename(SRC['m4reader'][0]),
                                                                                   os.path.basename(SRC['m4man'][0])))
RDN = os.path.splitext(os.path.basename(SRC['m4reader'][0]))[0]   # the reader's module name: m4xy_reader_v1_1 (m4xy_reader_v1 for MOCK)
spec = importlib.util.spec_from_file_location(RDN, SRC['m4reader'][0])
RD = importlib.util.module_from_spec(spec)
sys.modules[RDN] = RD
spec.loader.exec_module(RD)
if MOCK:                                                      # m4xy_reader_v1's script mode 'mock': FORMAT and CLAIM of the MOCK record
    RD.FIXED['FORMAT'], RD.CLAIM = RD.FIXED['FORMAT'] + ' MOCK', 'MOCK ' + RD.CLAIM
try:
    REC = RD.load(SRC['m4kv'][0], SRC['m4asm_out'][0], expected_sha256=shas['m4kv'], reader_sha256=shas['m4reader'])
    okl, why = True, 'load passed'
except ValueError as ex:
    REC, okl, why = None, False, 'refused: %s' % str(ex)[:200]
gate('C-LOAD', okl, '(M4XY_KV_v1 through %s.load bound to its asm output, expected sha256 and the reader\'s own sha256 given: %s)' % (RDN, why))
if FAILS:
    print('VERDICT INVALID (fails %s); no record written' % FAILS)
    sys.exit(3)
# ---- C-LEMMA: the t^0 zero of R_xy at m0* (C10_RECORD_v1) and the ball m0 (kt_cert_v1_8_xy's x records)
c10 = dict(ln.rstrip('\n').split(' = ', 1) for ln in open(SRC['c10'][0]) if ' = ' in ln and not ln.startswith('#'))
c10man = man_rows(SRC['c10man'][0])                          # its rows are relative to pk25/
okc10 = (c10.get('FORMAT') == 'C10_KV_v1' and c10.get('STATUS') == 'CERTIFIED' and 'C-SPAN' in c10.get('CLAIM', '') and
         'C-PURE10' in c10.get('CLAIM', '') and c10man.get(os.path.relpath(SRC['c10'][0], W + '/pk25')) == shas['c10'])
xlines = []
if not MOCK:
    v18man = man_rows(SRC['v18man'][0])
    for n in (4, 3):
        txt = open(SRC['x%d' % n][0]).read().splitlines()
        okx = (txt[0].startswith('kt_cert_v1_8_xy_2 sha256 %s ITEM=x.xyn%d ' % (SRC['v18'][1], n)) and
               [ln for ln in txt if ln.startswith('VERDICT')] == ['VERDICT VALID'] and
               len([ln for ln in txt if ln.startswith('C-T0ZERO N=%d xy: ' % n) and ln.endswith('-> PASS')]) == 1 and
               len([ln for ln in txt if ln.startswith('PLANT-T0ZERO N=%d xy: ' % n) and ln.endswith('-> FIRES')]) == 1 and
               v18man.get(SRC['x%d' % n][0]) == shas['x%d' % n])
        xlines.append('x.xyn%d %s' % (n, 'ok' if okx else 'NOT ok'))
        okc10 = okc10 and okx
gate('C-LEMMA', okc10, '(%s: FORMAT C10_KV_v1, STATUS CERTIFIED, CLAIM with C-SPAN and C-PURE10, a row of %s; %s)' % (
    os.path.basename(SRC['c10'][0]), os.path.basename(SRC['c10man'][0]),
    'MOCK: the x records of kt_cert_v1_8_xy_2 are not checked' if MOCK else
    'kt_cert_v1_8_xy_2 x records (first line naming %s, VERDICT VALID, C-T0ZERO PASS, PLANT-T0ZERO FIRES, rows of %s): %s' % (
        SRC['v18'][1][:8], os.path.basename(SRC['v18man'][0]), ', '.join(xlines))))
SH = {}
for ln in open(SRC['spectral'][0]):
    k, sep, v = ln.rstrip('\n').partition(' = ')
    if sep and re.fullmatch(r'N%d_P[0-9]{4}' % N, k):
        SH[k] = v.split()[:2]
keys = sorted(SH)
gate('C-GRID', len(keys) > 0 and SH[keys[-1]][1] == 'inf' and all(Fr(SH[keys[i]][1]) == Fr(SH[keys[i + 1]][0]) for i in range(len(keys) - 1))
     and Fr(SH[keys[0]][0]) >= 300, '(MR_SPECTRAL v4\'s N = %d keys: %d pieces from J %s to inf, contiguous, J >= 300)' % (N, len(keys), SH[keys[0]][0]))
p_xy = REC['N%d' % N]['xy']
jmin_tok = REC['kv']['N%d_XY_JMIN' % N]
gate('C-JMIN-GRID', Fr(SH[keys[0]][0]) == Fr(jmin_tok) == p_xy['JMIN'], '(the first piece\'s jlo %s equals the record\'s N%d_XY_JMIN %s exactly: the law '
     'holds on every piece)' % (SH[keys[0]][0], N, jmin_tok))
if FAILS:
    print('VERDICT INVALID (fails %s); no record written' % FAILS)
    sys.exit(3)


def mono_j(p, kind, far_c_override=None):
    """C-MONO-J: the conditions under which J L'(J) is nonincreasing on J >= 300 (see the docstring); returns (ok, why)."""
    why = []
    cx = RD.LAM_CH * arb(RD.A_E_F) / 2
    cb = RD.LAM_CH * RD.kappa_b() / 2
    for nm, c in (('tailX', cx), ('tailB', cb)):
        if not (c > 0 and 1 / c <= 300):
            why.append('%s rate' % nm)
    for name in RD.far_names(kind):
        x300, pw, c = p['FAR'][name]
        c = Fr(c) if far_c_override is None or name != far_c_override[0] else far_c_override[1]
        w = RD.far_wpow(kind, name)
        if not (c > 0 and (2 + w + Fr(pw)) / c <= 300):
            why.append('far %s' % name)
    dmax = max(d for d, v in p['SUPF'].items() if Fr(v) != 0) if any(Fr(v) != 0 for v in p['SUPF'].values()) else 0
    if not (RD.RHO_G > 0 and (dmax + 1) / RD.RHO_G <= 300):
        why.append('gB degree %d' % dmax)
    return not why, why


def lemma_hat(kind, J):
    """J L'(J) with the order-0 term removed (the lemma), and the parts used, as arb balls."""
    b = RD.law_balls(REC, kind, N, J)
    p = REC['N%d' % N][kind]
    Ja = ab(Fr(J))
    nearp = b['near'] - RD.farb(p['M0'])
    val = ((Ja * nearp) ** 2 + Ja * Ja * b['far']).sqrt() / b['D'] + Ja * b['gB'] / b['D']
    return val, b


rows, consts = {}, {}
for kind in KINDS:
    p = REC['N%d' % N][kind]
    okm, whym = mono_j(p, kind)
    gate('C-MONO-J', okm, '(%s: the tail rates, the far items\' (2 + w + p)/c <= 300 and gB\'s (d_max + 1)/rho_G <= 300, so J L\'(J) is nonincreasing on '
         'J >= 300; failures %s)' % (kind, whym))
    l300 = RD.law_balls(REC, kind, N, 300, below_jmin=True)['L']
    gate('C-L300', abs(float(l300.mid()) / float(p['L300']) - 1) <= 1e-9, '(%s: law_balls\' formula at J = 300, %.12e, against the record\'s L300 %s%s)' % (
        kind, float(l300.mid()), REC['kv']['N%d_XY_L300' % N], '; J = 300 is below J_MIN(4), so this checks the formula only' if N == 4 else ''))
    D = RD.law_balls(REC, kind, N, 300, below_jmin=True)['D']
    c0 = 300 * RD.farb(p['M1']) / D
    consts[kind] = {'C0_limit': dec_up(hi_of(c0)), 'M0_over_D': dec_up(hi_of(RD.farb(p['M0']) / D)), 'D_lower': repr(float(D.lower())),
                    'J_MIN': jmin_tok}
    rk = {}
    lim_ok = True
    for key in keys:
        jlo_s, jhi_s = SH[key]
        jlo = Fr(jlo_s)
        val, b = lemma_hat(kind, jlo)
        rh = hi_of(val)
        rw = dec_up(rh)
        row = {'jlo': jlo_s, 'jhi': jhi_s, 'R_hat': rw, 'c2_hi': dec_up(Fr(rw) ** 2)}   # c2 from the written R_hat
        if jhi_s == 'inf':
            row['R_hat_full'] = 'inf'
            lim_ok = lim_ok and rh >= hi_of(c0) * (1 - Fr(1, 10 ** 12))
        else:
            row['R_hat_full'] = dec_up(Fr(jhi_s) * hi_of(b['L']))
        rk[key] = row
    gate('C-LIMIT', lim_ok, '(%s: the last piece\'s R_hat %s is at least the t -> 0 limit 300 M_1/D = %s)' % (
        kind, rk[keys[-1]]['R_hat'], consts[kind]['C0_limit']))
    rows[kind] = rk
    print('ROWS N=%d %s: first piece R_hat %s (full %s), last piece R_hat %s; C0 = 300 M_1/D %s; engine t^0 M_0/D %s; J_MIN %s' % (
        N, kind, rk[keys[0]]['R_hat'], rk[keys[0]]['R_hat_full'], rk[keys[-1]]['R_hat'], consts[kind]['C0_limit'], consts[kind]['M0_over_D'], jmin_tok))
nm0 = RD.far_names('xy')[0]
x300, pw0, c0f = p_xy['FAR'][nm0]
w0 = RD.far_wpow('xy', nm0)
plant('PLANT-MONO-J', not mono_j(p_xy, 'xy', far_c_override=(nm0, (2 + w0 + Fr(pw0)) / 300 * Fr(999, 1000)))[0],
      '(xy\'s far item %s with its rate just below (2 + w + p)/300 must fail)' % nm0)
try:
    RD.law_balls(REC, 'xy', N, Fr(jmin_tok) - Fr(1, 10 ** 6))
    fired = False
except ValueError:
    fired = True
plant('PLANT-JMIN', fired, '(the law just below J_MIN(%d) = %s must be refused by %s.law_balls)' % (N, jmin_tok, RDN))
bad_round = sum(1 for kind in KINDS for key in keys if Fr(rows[kind][key]['c2_hi']) < Fr(rows[kind][key]['R_hat']) ** 2)
gate('C-ROUND', bad_round == 0, '(every written c2_hi >= the written R_hat squared; failures %d)' % bad_round)
if FAILS or NOFIRE:
    print('VERDICT INVALID (fails %s, plants not firing %s); no record written' % (FAILS, NOFIRE))
    sys.exit(3)
record = {'format': 'pk22 E3 second-order record v2' + (' MOCK' if MOCK else ''), 'tool': os.path.basename(__file__),
          'tool_sha256': sha(os.path.abspath(__file__)), 'N': N, 'kinds': list(KINDS),
          'claim': ('MOCK (pk23\'s MOCK M4XY record; certifies nothing): ' if MOCK else '') +
                   'for the kind xy and each piece, for every J in [jlo, jhi] (t = 1/J; t = 0 included on the last piece): R_xy(t) <= t R_hat and '
                   'R_xy(t)^2 <= t^2 c2_hi, i.e. X = R_xy^2 has X(0) = X_1 = 0 (the t^0 zero at m0 = m0*: C10_RECORD_v1\'s C-SPAN and C-PURE10, '
                   'kt_cert_v1_8_xy_2\'s x records: the ball m0 with C-T0ZERO); lemma-free: R_xy(t) <= t R_hat_full on every finite piece. '
                   'R_xy = engine bound/(lambda~_0 Z_xy^1/2) as kt_cert_v1_9_xy bounds it; J >= J_MIN(N) on every piece',
          'law': '%s.law_balls with near\' = near - M_0; J L\'(J) at jlo under C-MONO-J' % RDN,
          'constants': consts, 'sources': dict((k, {'file': os.path.relpath(p, W), 'sha256': shas[k]}) for k, (p, _) in SRC.items()),
          'pieces': rows}
assert os.path.dirname(OUT) == W + '/pk22/midrow/e3/out'
with open(OUT, 'x') as fh:
    json.dump(record, fh, indent=1, sort_keys=True)
    fh.write('\n')
print('RECORD %s sha256 %s pieces %d kinds %s' % (OUT, sha(OUT), len(keys), list(KINDS)))
print('VERDICT VALID%s' % (' (MOCK)' if MOCK else ''))
