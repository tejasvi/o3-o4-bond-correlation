#!/usr/bin/env python3
"""px08_hsd3_export_v1.py -- pk08: the lemma-form D3 rows of HS_INV_NORMX_v1 for pk15's normX_HS reader (SPEC_HS_INV_NORMX_v1_2).
Lemma D3 of HS_NORMX_LEMMA_NOTE_v1, reading A:
  HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^2,  COEF = (A + max|c_t|)^2 (A + max|c_bb|)^2 U_N,  A = (N-1)/2,
with X_c carrying 1/lambda_0^w once (the true lambda_0); the reader's (lambda_h/lambda_0,lo)^2 makes it an upper end.
Outward: U_N's decimal is an upper end, COEF is exact from it and rounded up. Only exact rational arithmetic on literals read
from pinned files (the sha256 is of the bytes that are parsed). Checks, each with a plant that must fail:
  C-SRC   every input's sha256 equals its pin;
  C-ULIT  N4_U, N3_U, N*_LEAD_HI read from S4_U_CERTIFIED_v3 equal the stated literals, each key exactly once;
  C-HARM  H_BESSEL_NOTE_v1's harmonic-margin line is present verbatim (harmonic c = A - the row-T margin);
  C-OPSTR OPERATOR_D3 and the gate keys are v1_2's template lines verbatim, the boxes are v1_1's, the needs are the plan's;
  C-ARITH each written COEF is an upper end of its exact rational, within 1e-9, and an 80-digit Decimal recomputation agrees;
  C-SPOT  the lemma at harmonic inputs (c harmonic, U -> LEAD_HI, lambda_h/lambda_0 -> 1) >= 2 Cov_LH + Cov^2 (kt_s8rf_v1, LH lines);
  C-NEED  COEF <= need^2 for each of the six D3 classes (the margin and the largest r = lambda_h/lambda_0,lo are printed).
Usage: px08_hsd3_export_v1.py run
"""
import sys, os, re, math, hashlib, resource, signal, time
from fractions import Fraction
from decimal import Decimal, localcontext

if len(sys.argv) != 2 or sys.argv[1] != 'run':
    print('usage: px08_hsd3_export_v1.py run')
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (60, 65))

CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk08'
OUTD = OWN + '/out'
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(OUTD, '%s_run.out' % LABEL)
REC_NAME = 'HS_INV_NORMX_v1.kv'
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

SPEC_NEW = 'pk15/SPEC_HS_INV_NORMX_v1_2.md'
LEMMA = 'pk08/HS_NORMX_LEMMA_NOTE_v1.md'
REVIEW = 'rv01/lemma_note_check.md'
DELTA = 'rv01/spec_delta.md'
LEMMA_FORM = 'rv01/lemma_form_source.md'
U_REC = 'pk08/S4_U_CERTIFIED_v3.md'
HB_NOTE = 'pk08/H_BESSEL_NOTE_v1.md'
SPEC_V11 = 'pk15/SPEC_HS_INV_NORMX_v1_1.md'
PLAN = 'pk15/NOTE_STB_OPTION2_PLAN_v1_2.md'
S8RF = {4: 'pk11/out/s8hf_v1/out_kt_s8rf_v1_n4.out', 3: 'pk11/out/s8hf_v1/out_kt_s8rf_v1_n3.out'}
PINS = {
    SPEC_NEW: '84f6a3e02cb19bedab4f7ba7b585002058b6dea3fd72b733b4bf4770c12bdf7f',
    LEMMA: 'ffd98fc1946714e36e86359c338c38a6b89af31eb7f707306a0a59f3f281493b',
    REVIEW: '969321c8e3ebd467233a0cd282303ef11d0be0dad4ead4fcf15ec2fb4cde4035',
    DELTA: '93c32c910c84fa7cf6e2a67c80d3e14a1e28efb3d0db5eb3c0061f49527cb547',
    LEMMA_FORM: 'd0cc9120dae530429747379bb883d993be3351c1faa16d32648d4f28f582a94f',
    U_REC: 'eb98948365fa35498206c9f1b80c6d98d421f69b9dca6c245f3f2d1198112751',
    HB_NOTE: '3c543e3c28d67ba9f763c420c9ff3fc1d2f88b73249ed143b884078177cfb00c',
    SPEC_V11: '8043f94a77923d2f58e532b9d677b5de9fb6c656e832b8228b42390e826a653f',
    PLAN: '0a686ada4026e6a10df85364a6e9c5e2faddd082e66cea0ce22ebe0e9c881d8e',
    S8RF[4]: 'a8644832e801ba75e25222df9070c3a494a7e16bd64b0832071564e14b95394f',
    S8RF[3]: 'cc9cd98cfa466749593ff2de1e2e8deae4a435d15eacb6845d48e6a9e000caea',
}
OPERATOR_D3 = ('Z = K^(1/2) V^(1/2); G_t = V^(1/2) (K_t - c_t K) V^(1/2); G_bb = V^(1/2) (K_bb - c_bb K) V^(1/2); '
               'lambda_0^3 X_c = Z G_t G_bb Z*; w = 3; t = gap-0 top horizontal, bb = gap-1 bottom horizontal; '
               'HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^2, lambda_0 by its certified lower end')
LAMBDA_POWER_D3 = 2
TEMPLATE = ['RECORD = HS_INV_NORMX_v1', 'INTERFACE = CENTRED_HS2_BOX', 'TRACE = HAAR_TWISTED_ON_H',
            'NORMALIZATION = HS2_TR_XC_STAR_XC', 'LAMBDA_POWER_D3 = %d' % LAMBDA_POWER_D3,
            'J_CLAIM = UNIFORM-J PER-ROW: every row holds for every J in [jlo, jhi]; jhi = inf includes t = 0',
            'FIELDS = jlo jhi ce_lo ce_hi cf_lo cf_hi COEF', 'N4_D3_METHOD = LEMMA']
ULIT = {'N4_U': '1.033200684443', 'N3_U': '1.032809143879',
        'N4_LEAD_HI': '1.03023930410320116', 'N3_LEAD_HI': '1.03023930410320116'}
HB_LINE = '  - Harmonic margins (N-1)/2 - c_e: 0.3327 and 0.4364 (t, h; N = 3); 0.4991 and 0.6547 (N = 4).'
MARGIN_T = {4: '0.4991', 3: '0.3327'}
BOX_TEXT = 'N4 c_t and c_bb [0.94, 1.06], c_b [0.77, 0.89]; N3 c_t and c_bb [0.62, 0.72]'
BOX = {4: ('0.94', '1.06'), 3: ('0.62', '0.72')}
NEEDS = {4: [('(1,1)', '15.5'), ('(1,2)', '20.3'), ('(0,2)', '18.5'), ('(0,3)', '173.7')],
         3: [('(1,1)', '15.0'), ('(0,2)', '18.5')]}
NEED_TEXT = ['(0,2) for N4 D3, D4, D4m, N3 D3 and N3 D4m (Route A; need 18.5-30.5)', 'N4 D3 (0,3) (Route A; need 173.7)',
             'N4 D3 (1,2) (plain; need 20.3)', 'the six (1,1) classes (route 0; need 15.5 for N4 D3, 15.0 for N3 D3']
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


def c_ulit(expect):
    return all(key_once(U_REC, k) == v for k, v in expect.items())


def c_harm(line):
    return lines_of(HB_NOTE).count(line) == 1


def c_opstr(op, template, box_text, need_text):
    sp = lines_of(SPEC_NEW)
    return (sp.count('OPERATOR_D3 = ' + op) == 1 and all(sp.count(t) == 1 for t in template)
            and sum(box_text in ln for ln in lines_of(SPEC_V11)) == 1
            and all(DATA[PLAN].decode('utf-8').count(t) == 1 for t in need_text))


def ceil_div(p, q):
    return -((-p) // q)


def updec(x, sig=12):
    """the smallest decimal with sig significant digits that is >= x (x a positive Fraction), as an exact string"""
    k = 0
    while Fraction(10) ** (k + 1) <= x:
        k += 1
    while Fraction(10) ** k > x:
        k -= 1
    e = sig - 1 - k
    q = x * Fraction(10) ** e
    s = str(ceil_div(q.numerator, q.denominator))
    if e <= 0:
        return s + '0' * (-e)
    if len(s) <= e:
        s = '0' * (e - len(s) + 1) + s
    return s[:-e] + '.' + s[-e:]


def sqrt_up(x, digits=10):
    """an upper end of sqrt(x) on the 10^-digits grid, as a Fraction"""
    q = x * 10 ** (2 * digits)
    m = ceil_div(q.numerator, q.denominator)
    r = math.isqrt(m)
    if r * r < m:
        r += 1
    return Fraction(r, 10 ** digits)


def coef(N, c_abs, U):
    A = Fraction(N - 1, 2)
    return (A + c_abs) ** 4 * U


def dec80(N, c_abs_s, U_s):
    with localcontext() as ctx:
        ctx.prec = 80
        A = Decimal(N - 1) / Decimal(2)
        return (A + Decimal(c_abs_s)) ** 4 * Decimal(U_s)


def spot_rhs(N):
    pat = re.compile(r'^JH N%d D3 LH: \|\|Q0 X u\|\|\^2 ([0-9.eE+-]+) \(0q ([0-9.eE+-]+),' % N)
    hits = [h for h in (pat.match(ln) for ln in lines_of(S8RF[N])) if h]
    if len(hits) != 1:
        return None
    return hits[0].group(1), hits[0].group(2), 2 * Fraction(hits[0].group(1)) + Fraction(hits[0].group(2))


def main():
    t0 = time.time()
    with open(os.path.abspath(__file__), 'rb') as fh:
        code_sha = hashlib.sha256(fh.read()).hexdigest()
    out('px08_hsd3_export_v1 start; code sha256 %s' % code_sha)
    res, plants = {}, {}
    res['C-SRC'] = c_src(PINS)
    out('C-SRC: %d pinned inputs, sha256 of the parsed bytes -> %s' % (len(PINS), 'PASS' if res['C-SRC'] else 'FAIL'))
    if not res['C-SRC']:
        out('VERDICT INVALID')
        return 1
    good = dict(DATA)
    bad = dict(PINS)
    bad[U_REC] = bad[U_REC][:-1] + ('0' if bad[U_REC][-1] != '0' else '1')
    plants['PLANT-SRC'] = not c_src(bad)
    DATA.clear()
    DATA.update(good)
    res['C-ULIT'] = c_ulit(ULIT)
    plants['PLANT-ULIT'] = not c_ulit(dict(ULIT, N4_U='1.033200684444'))
    res['C-HARM'] = c_harm(HB_LINE)
    plants['PLANT-HARM'] = not c_harm(HB_LINE.replace('0.4991', '0.4992'))
    res['C-OPSTR'] = c_opstr(OPERATOR_D3, TEMPLATE, BOX_TEXT, NEED_TEXT)
    plants['PLANT-OPSTR'] = not c_opstr(OPERATOR_D3.replace('w = 3', 'w = 2'), TEMPLATE, BOX_TEXT, NEED_TEXT)
    for k in ('C-ULIT', 'C-HARM', 'C-OPSTR'):
        out('%s -> %s' % (k, 'PASS' if res[k] else 'FAIL'))
    U = {4: Fraction(ULIT['N4_U']), 3: Fraction(ULIT['N3_U'])}
    LEAD = {4: Fraction(ULIT['N4_LEAD_HI']), 3: Fraction(ULIT['N3_LEAD_HI'])}
    rows = {}
    arith = need_ok = spot_ok = True
    arith_plant = need_plant = spot_plant = True
    for N in (4, 3):
        lo_s, hi_s = BOX[N]
        cf = coef(N, Fraction(hi_s), U[N])
        cf_s = updec(cf)
        cfF = Fraction(cf_s)
        d80 = dec80(N, hi_s, ULIT['N%d_U' % N])
        arith = arith and cfF >= cf and cfF - cf < Fraction(1, 10 ** 9) and Decimal(cf_s) >= d80
        arith_plant = arith_plant and not (cfF - Fraction(1, 10 ** 9) >= cf)
        nx = sqrt_up(cfF)
        info = []
        for cls, need_s in NEEDS[N]:
            need = Fraction(need_s)
            ok = cfF <= need * need
            need_ok = need_ok and ok
            info.append('%s need %s margin %.3f largest r %.4f %s' % (cls, need_s, float(need / nx), float(need / nx),
                                                                     'PASS' if ok else 'FAIL'))
        need_plant = need_plant and not (cfF <= Fraction(2) ** 2)
        A = Fraction(N - 1, 2)
        c_h = A - Fraction(MARGIN_T[N])
        spot = (A + c_h) ** 4 * LEAD[N]
        rr = spot_rhs(N)
        sp_ok = rr is not None and spot >= rr[2]
        spot_ok = spot_ok and sp_ok
        spot_plant = spot_plant and not (rr is not None and spot * Fraction(1, 10 ** 7) >= rr[2])
        rows[N] = dict(lo=lo_s, hi=hi_s, coef=cf_s, normx=nx, c_h=c_h, spot=updec(spot), rr=rr)
        out('N%d: COEF = (A + %s)^4 U = %s (float %.12g), normX at r = 1 <= %s; spot %s vs 2 Cov_LH + Cov^2 %s -> %s' % (
            N, hi_s, cf_s, float(cf), updec(nx, 10), rows[N]['spot'], ('%.6e' % float(rr[2])) if rr else 'NONE',
            'PASS' if sp_ok else 'FAIL'))
        for ln in info:
            out('  N%d D3 %s' % (N, ln))
    res['C-ARITH'], res['C-NEED'], res['C-SPOT'] = arith, need_ok, spot_ok
    plants['PLANT-ARITH'], plants['PLANT-NEED'], plants['PLANT-SPOT'] = arith_plant, need_plant, spot_plant
    for k in ('C-ARITH', 'C-NEED', 'C-SPOT'):
        out('%s -> %s' % (k, 'PASS' if res[k] else 'FAIL'))
    for k in sorted(plants):
        out('%s -> %s' % (k, 'FIRED' if plants[k] else 'MISSED'))
    if not (all(res.values()) and all(plants.values())):
        out('VERDICT INVALID')
        return 1

    def p(rel):
        return '%s:%s' % (rel, PINS[rel])
    R = ['# HS_INV_NORMX_v1: the lemma-form D3 rows of the normX_HS record (pk08), for pk15\'s reader (SPEC_HS_INV_NORMX_v1_2).',
         '# Format S4U_KV_v1: one "KEY = value" per line; lines starting with # are comments. Decimals are exact; COEF is rounded up.',
         TEMPLATE[0], 'FORMAT = S4U_KV_v1', 'EXPORT_STATUS = CERTIFIED', 'PRODUCER = pk08',
         'CODE = pk08/%s.py:%s' % (LABEL, code_sha[:8]), TEMPLATE[1], TEMPLATE[2], TEMPLATE[3],
         'LEMMA_NOTE = ' + p(LEMMA), 'OPERATOR_D3 = ' + OPERATOR_D3, TEMPLATE[4], TEMPLATE[5], TEMPLATE[6]]
    for N in (4, 3):
        r = rows[N]
        R += ['N%d_D3_ROWS = 1' % N, 'N%d_D3_R000 = 300 inf %s %s %s %s %s' % (N, r['lo'], r['hi'], r['lo'], r['hi'], r['coef']),
              'N%d_D3_METHOD = LEMMA' % N]
    R += ['# binding and INFO keys (not read by the gates)',
          'LEMMA_REVIEW = ' + p(REVIEW), 'DELTA = ' + p(DELTA), 'LEMMA_FORM_SOURCE = ' + p(LEMMA_FORM),
          'SPEC = ' + p(SPEC_NEW) + ' ; ' + p(SPEC_V11), 'PLAN = ' + p(PLAN),
          'FORMULA_D3 = Lemma D3 of LEMMA_NOTE, reading A: HS2 = tr_H(X_c* X_c) <= (A + |c_t|)^2 (A + |c_bb|)^2 U (lambda_h/lambda_0)^2 '
          'for every J >= 300 and every c; COEF is its sup over the row\'s box (|c| at the box\'s largest)',
          'OUTWARD = U\'s decimal is an upper end; COEF is exact from it and rounded up; the reader applies the upper end of '
          'lambda_h/lambda_0,lo to the power LAMBDA_POWER_D3',
          'N4_A = 3/2', 'N3_A = 1', 'N4_U = ' + ULIT['N4_U'], 'N3_U = ' + ULIT['N3_U'], 'U_SOURCE = ' + p(U_REC),
          'T_DEF = T = K^(1/2) V K^(1/2) on L^2((S^(N-1))^3) with normalized measures; V = e^{J(s_T.s_M - 1)} e^{J(s_M.s_B - 1)}; '
          'K = K_T (x) K_M (x) K_B with K_r(s, s\') = e^{J(s.s\' - 1)}',
          'H_DEF = H = the O(N)-invariant subspace; P_H = int_O(N) U_g dg (Haar); lambda_0 = max spec(T), attained on H',
          'LAMBDA_H_DEF = S4-U\'s lambda_h equals SPEC v1_2\'s lambda_h := exp(logmain_N(J) - logmain_D(J)) at the same J ('
          'the delta, sect. 3): the 3- and 2-column strips with the ends (A_EX, B_EX) = ((3 + sqrt 21)/6, (3 sqrt 5 - sqrt 21)/12), '
          'whose matrix-tree determinant factor is S4\'s PR = pref_arb(N) = (detred(3)/detred(2))^((N-1)/2)',
          'U_T_H_BINDING = S4-U\'s T and H (S4_U_CERTIFIED_v3\'s CLAIM) are T_DEF and H_DEF; S4-U\'s lambda_h is LAMBDA_H_DEF\'s (PR = '
          'pref_arb(N) on strip_graph(ncols, AEX, BEX), copied into px08_m2bc4); the consumer\'s S8 identity (SPEC_S8_CERT_v1 19.6.2) '
          'and the port kt_s67_cert_v1_1\'s Ctx.U use the same objects',
          '# INFO: normX at r = lambda_h/lambda_0,lo = 1, the needs (plan l.28-31) and the spot control (the lemma at harmonic inputs; '
          '2 Cov(X_c, theta X_c) + Cov^2 at the half-step plane)']
    for N in (4, 3):
        r = rows[N]
        R += ['N%d_D3_NORMX_R1 = %s' % (N, updec(r['normx'], 10)),
              'N%d_D3_NEEDS = %s' % (N, ' ; '.join('%s %s' % cn for cn in NEEDS[N])),
              'N%d_D3_SPOT = %s %s ; c_harm %s ; LEAD_HI %s ; Cov_LH %s ; Cov^2 %s ; source %s' % (
                  N, r['spot'], updec(r['rr'][2], 8), updec(r['c_h'], 6), ULIT['N%d_LEAD_HI' % N], r['rr'][0], r['rr'][1],
                  p(S8RF[N]))]
    R.append('END = HS_INV_NORMX_v1')
    with open(REC_PATH, 'x') as fh:
        fh.write('\n'.join(R) + '\n')
    with open(REC_PATH, 'rb') as fh:
        rsha = hashlib.sha256(fh.read()).hexdigest()
    out('CPU %.2f s, wall %.2f s' % (resource.getrusage(resource.RUSAGE_SELF).ru_utime, time.time() - t0))
    out('VERDICT VALID')
    out('RECORD %s %s' % (REC_NAME, rsha))
    return 0


if __name__ == '__main__':
    rc = main()
    FH.close()
    sys.exit(rc)
