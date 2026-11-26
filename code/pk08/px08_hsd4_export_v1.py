#!/usr/bin/env python3
"""px08_hsd4_export_v1.py -- pk08: the combined normX_HS record (shape (ii) of SPEC_HS_INV_NORMX_v1_2_ADD1, f2ad58c9): every D3 and shared
header line of HS_INV_NORMX_v1.kv (6b82dc63) token for token, plus the lemma-form D4 and D4M rows under Lemma D4/D4m of HS_NORMX_LEMMA_NOTE_v1
(1340a52c, reading A: X_c carries 1/lambda_0^w once, with the true lambda_0):
  HS2(D4) = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^1,  COEF = (A + max|c_t|)^2 (A2 + max(c_b)^2 A0)  (c_b >= 0 on the box),
with A = (N-1)/2; A2 the certified upper end of tr_H(K^(1/2) V xi_b^2 K^(1/2))/lambda_h for every J >= 300 (px08_a2cert_v1's asm READING line);
A0 = N*_RTR mhat(1/300) >= tr_H(T)/lambda_h for every J >= 300 (S4_RTR_CERTIFIED_v1: tr_H(T)/(lambda_h mhat(t)) <= N*_RTR, and mhat increases on
(0, 1/300] since m1, m2, m3 > 0). D4M rows equal the D4 rows token for token (X_c(D4m) = X_c(D4)*, the same HS norm on H).
Only exact rational arithmetic on literals read from pinned files (the sha256 is of the bytes that are parsed). Checks, each with a plant that
must fail:
  C-SRC     every input's sha256 equals its pin;
  C-D3-SAME the D3 record's run output has exactly ['VERDICT VALID'] and one RECORD line naming the D3 record's sha256, and every line of the D3
            record other than comments, CODE and END is copied in order and unchanged;
  C-A2      each A2 asm output has a header naming the frozen px08_a2cert_v1.py sha256 and ITEM=n<N> asm, exactly one READING line
            'A2_<N> <= x', a C-A2T PASS line and exactly ['VERDICT VALID']; x is that N's A2 literal;
  C-RTR     N*_RTR and N*_MHAT_M1..M3 from S4_RTR_CERTIFIED_v1 equal the stated literals and m1, m2, m3 > 0;
  C-OPSTR   OPERATOR_D4 and OPERATOR_D4M equal ADD1's lines verbatim, and the boxes are ADD1's;
  C-CBOX0   every box lower end is >= 0 (Lemma D4's step needs c_b >= 0);
  C-ARITH   each COEF is an upper end of its exact rational within 1e-9, and an 80-digit Decimal recomputation agrees;
  C-MIRROR  the D4M row tokens equal the D4 row tokens;
  C-NEED    COEF <= 9.3^2 per N (the D4/D4M (1,1) rows' need; the (0,2) needs are larger);
  C-SPOT    INFO control: the lemma at c_b = 0, harmonic c_t and A2 -> the lower end of its lead I[GE0] (a value below the harmonic one, since
            COEF grows with c_b >= 0) is >= 2 Cov_LH + Cov^2 from kt_s8rf_v1's D4 and D4M LH lines.
Usage: px08_hsd4_export_v1.py run
"""
import sys, os, re, math, hashlib, resource, signal, time
from fractions import Fraction
from decimal import Decimal, localcontext

if len(sys.argv) != 2 or sys.argv[1] != 'run':
    print('usage: px08_hsd4_export_v1.py run')
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (60, 65))

CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk08'
OUTD = OWN + '/out'
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(OUTD, '%s_run.out' % LABEL)
REC_NAME = 'HS_INV_NORMX_v1_d3d4.kv'
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

D3REC = 'pk08/out/HS_INV_NORMX_v1.kv'
D3RUN = 'pk08/out/px08_hsd3_export_v1_run.out'
ADD1 = 'pk15/SPEC_HS_INV_NORMX_v1_2_ADD1.md'
SPEC = 'pk15/SPEC_HS_INV_NORMX_v1_2.md'
LEMMA = 'pk08/HS_NORMX_LEMMA_NOTE_v1.md'
REVIEW = 'rv01/lemma_note_check.md'
A2CODE = 'pk08/px08_a2cert_v1.py'
A2ASM = {4: 'pk08/out/px08_a2cert_v1_n4_asm.out', 3: 'pk08/out/px08_a2cert_v1_n3_asm.out'}
A2REV = 'rv01/a2_chain_check.md'
RTR = 'pk08/S4_RTR_CERTIFIED_v1.md'
HB_NOTE = 'pk08/H_BESSEL_NOTE_v1.md'
S8RF = {4: 'pk11/out/s8hf_v1/out_kt_s8rf_v1_n4.out', 3: 'pk11/out/s8hf_v1/out_kt_s8rf_v1_n3.out'}
PINS = {
    D3REC: '90bbc6f2eaa35cee6b01a77c77995d35659028c9806d5e21278f1899a6c2e67e',
    D3RUN: 'e12440402124d07d7e5795d431b0e1d19073a7e6ae844e4235c650f4e452dea8',
    ADD1: 'b289d61e4df0b7345db63843d3ac15d414723810982702bb3316d07e318a797c',
    SPEC: '84f6a3e02cb19bedab4f7ba7b585002058b6dea3fd72b733b4bf4770c12bdf7f',
    LEMMA: 'ffd98fc1946714e36e86359c338c38a6b89af31eb7f707306a0a59f3f281493b',
    REVIEW: '969321c8e3ebd467233a0cd282303ef11d0be0dad4ead4fcf15ec2fb4cde4035',
    A2CODE: '5eb405ef26b892d461e6d43b57d9e70afe9878d72ed0bbc14566a4f90a56b446',
    A2ASM[4]: '62cb0dcdd70d8a1b8122fb42cc818e7fe34c82c828937c3a10aec59c833ced7d',
    A2ASM[3]: '460298bc7e4904d9f7f5552bfe4dd15a817f65c76029f0c87943da4765d287d2',
    A2REV: '5b90e8ce84b643eb1359e99412f6fe8f1093dd503b2b91c0d0ab3e5583ae7ca5',
    RTR: 'a2b08d873bc88b1fcdb2e64db91070ce0b204eedef725d9bf45ad15074c7a430',
    HB_NOTE: '3c543e3c28d67ba9f763c420c9ff3fc1d2f88b73249ed143b884078177cfb00c',
    S8RF[4]: 'a8644832e801ba75e25222df9070c3a494a7e16bd64b0832071564e14b95394f',
    S8RF[3]: 'cc9cd98cfa466749593ff2de1e2e8deae4a435d15eacb6845d48e6a9e000caea',
}
OPERATOR_D4 = ('Z = K^(1/2) V^(1/2); M = (xi_b - c_b) on column 0, xi_b = J(1 - s_M.s_B); G_t = V^(1/2) (K_t - c_t K) V^(1/2); '
               'lambda_0^2 X_c = Z M G_t Z*; w = 2; t = gap-0 top horizontal, b = column-0 MB vertical; '
               'HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^1, lambda_0 by its certified lower end')
OPERATOR_D4M = ('Z = K^(1/2) V^(1/2); M = (xi_b - c_b) on column 1, xi_b = J(1 - s_M.s_B); G_t = V^(1/2) (K_t - c_t K) V^(1/2); '
                'lambda_0^2 X_c = Z G_t M Z*, the adjoint of D4\'s; w = 2; t = gap-0 top horizontal, b = column-1 MB vertical; '
                'HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^1, lambda_0 by its certified lower end')
BOX = {4: ('0.94', '1.06', '0.77', '0.89'), 3: ('0.62', '0.72', '0.50', '0.60')}
BOX_TEXT = {4: 'N4_D4_R000 = 300 inf 0.94 1.06 0.77 0.89 <COEF>', 3: '(the same keys for N3, with the boxes 0.62 0.72 and 0.50 0.60)'}
RTRLIT = {'N4_RTR': '1.33103977243e+0', 'N3_RTR': '1.33071322604e+0',
          'N4_MHAT_M1': '0.4110342096146122', 'N4_MHAT_M2': '0.21439445218778858', 'N4_MHAT_M3': '0.13250737666638984',
          'N3_MHAT_M1': '0.3639110188717423', 'N3_MHAT_M2': '0.19020873542681713', 'N3_MHAT_M3': '0.1312176314326442'}
HB_LINE = '  - Harmonic margins (N-1)/2 - c_e: 0.3327 and 0.4364 (t, h; N = 3); 0.4991 and 0.6547 (N = 4).'
MARGIN_T = {4: '0.4991', 3: '0.3327'}
NEED11 = Fraction('9.3')
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


def d3_lines():
    """the D3 record's lines to copy: every line except comments, CODE, END and blanks, in order"""
    return [ln for ln in lines_of(D3REC) if ln and not ln.startswith('#') and not ln.startswith('CODE = ') and not ln.startswith('END = ')]


def c_d3run(rec_sha):
    ls = lines_of(D3RUN)
    return [x for x in ls if x.startswith('VERDICT')] == ['VERDICT VALID'] and ls.count('RECORD HS_INV_NORMX_v1.kv %s' % rec_sha) == 1


def c_a2(N, code_sha):
    """(ok, A2 literal, lead-lower-end literal or None) from the N asm output"""
    ls = lines_of(A2ASM[N])
    hd = ls[0].split()
    ok = (len(hd) >= 7 and hd[0] == 'px08_a2cert_v1' and hd[2] == code_sha and hd[3] == 'ITEM=n%d' % N and hd[4] == 'asm'
          and [x for x in ls if x.startswith('VERDICT')] == ['VERDICT VALID']
          and sum(x.startswith('C-A2T N=%d ' % N) and ': PASS;' in x for x in ls) == 1)
    rd = [re.match(r'^READING N=%d \(.*\): A2_%d <= ([0-9.e+-]+); main' % (N, N), x) for x in ls]
    rd = [m.group(1) for m in rd if m]
    ld = [re.match(r'^  N=%d I\[GE0\] = \[([0-9.e+-]+) \+/- ([0-9.e+-]+)\]' % N, x) for x in ls]
    ld = [(m.group(1), m.group(2)) for m in ld if m]
    if len(rd) != 1 or len(ld) != 1:
        return False, None, None
    return ok, rd[0], Fraction(ld[0][0]) - Fraction(ld[0][1])


def c_rtr(expect):
    ok = all(key_once(RTR, k) == v for k, v in expect.items())
    return ok and all(Fraction(expect['N%d_MHAT_M%d' % (N, j)]) > 0 for N in (4, 3) for j in (1, 2, 3))


def c_opstr(op4, op4m, box_text):
    ad = lines_of(ADD1)
    return (ad.count('OPERATOR_D4 = ' + op4) == 1 and ad.count('OPERATOR_D4M = ' + op4m) == 1
            and ad.count(box_text[4]) == 1 and ad.count(box_text[3]) == 1)


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
    q = x * 10 ** (2 * digits)
    m = ceil_div(q.numerator, q.denominator)
    r = math.isqrt(m)
    if r * r < m:
        r += 1
    return Fraction(r, 10 ** digits)


def mhat300(N):
    t = Fraction(1, 300)
    return 1 + Fraction(RTRLIT['N%d_MHAT_M1' % N]) * t + Fraction(RTRLIT['N%d_MHAT_M2' % N]) * t ** 2 + Fraction(RTRLIT['N%d_MHAT_M3' % N]) * t ** 3


def coef(N, ct_hi, cb_hi, a2, a0):
    A = Fraction(N - 1, 2)
    return (A + ct_hi) ** 2 * (a2 + cb_hi ** 2 * a0)


def dec80(N, ct_s, cb_s, a2_s, rtr_s, mh):
    with localcontext() as ctx:
        ctx.prec = 80
        A = Decimal(N - 1) / Decimal(2)
        a0 = Decimal(rtr_s) * (Decimal(mh.numerator) / Decimal(mh.denominator))
        return (A + Decimal(ct_s)) ** 2 * (Decimal(a2_s) + Decimal(cb_s) ** 2 * a0)


def spot_rhs(N, cls):
    pat = re.compile(r'^JH N%d %s LH: \|\|Q0 X u\|\|\^2 ([0-9.eE+-]+) \(0q ([0-9.eE+-]+),' % (N, cls))
    hits = [h for h in (pat.match(ln) for ln in lines_of(S8RF[N])) if h]
    if len(hits) != 1:
        return None
    return hits[0].group(1), hits[0].group(2), 2 * Fraction(hits[0].group(1)) + Fraction(hits[0].group(2))


def main():
    t0 = time.time()
    with open(os.path.abspath(__file__), 'rb') as fh:
        code_sha = hashlib.sha256(fh.read()).hexdigest()
    out('px08_hsd4_export_v1 start; code sha256 %s' % code_sha)
    res, plants = {}, {}
    res['C-SRC'] = c_src(PINS)
    out('C-SRC: %d pinned inputs, sha256 of the parsed bytes -> %s' % (len(PINS), 'PASS' if res['C-SRC'] else 'FAIL'))
    if not res['C-SRC']:
        out('VERDICT INVALID')
        return 1
    good = dict(DATA)
    bad = dict(PINS)
    bad[A2CODE] = bad[A2CODE][:-1] + ('0' if bad[A2CODE][-1] != '0' else '1')
    plants['PLANT-SRC'] = not c_src(bad)
    DATA.clear()
    DATA.update(good)
    res['C-D3-SAME'] = c_d3run(PINS[D3REC]) and len(d3_lines()) > 20
    plants['PLANT-D3-SAME'] = not c_d3run(PINS[D3REC][:-1] + 'x')
    a2, lead = {}, {}
    okA = True
    for N in (4, 3):
        ok, x, lo = c_a2(N, PINS[A2CODE])
        okA = okA and ok and x is not None
        a2[N], lead[N] = x, lo
    res['C-A2'] = okA
    plants['PLANT-A2'] = not c_a2(4, PINS[A2CODE][:-1] + 'x')[0]
    res['C-RTR'] = c_rtr(RTRLIT)
    plants['PLANT-RTR'] = not c_rtr(dict(RTRLIT, N4_RTR='1.33103977244e+0'))
    res['C-OPSTR'] = c_opstr(OPERATOR_D4, OPERATOR_D4M, BOX_TEXT)
    plants['PLANT-OPSTR'] = not c_opstr(OPERATOR_D4.replace('w = 2', 'w = 3'), OPERATOR_D4M, BOX_TEXT)
    res['C-CBOX0'] = all(Fraction(BOX[N][0]) >= 0 and Fraction(BOX[N][2]) >= 0 for N in (4, 3))
    plants['PLANT-CBOX0'] = not (Fraction('-0.01') >= 0)
    for k in ('C-D3-SAME', 'C-A2', 'C-RTR', 'C-OPSTR', 'C-CBOX0'):
        out('%s -> %s' % (k, 'PASS' if res[k] else 'FAIL'))
    if not res['C-A2']:
        out('VERDICT INVALID')
        return 1
    rows = {}
    arith = need_ok = spot_ok = mirror_ok = True
    arith_plant = need_plant = spot_plant = True
    for N in (4, 3):
        ct_lo, ct_hi, cb_lo, cb_hi = BOX[N]
        mh = mhat300(N)
        a0 = Fraction(RTRLIT['N%d_RTR' % N]) * mh
        cf = coef(N, Fraction(ct_hi), Fraction(cb_hi), Fraction(a2[N]), a0)
        cf_s = updec(cf)
        cfF = Fraction(cf_s)
        d80 = dec80(N, ct_hi, cb_hi, a2[N], RTRLIT['N%d_RTR' % N], mh)
        arith = arith and cfF >= cf and cfF - cf < Fraction(1, 10 ** 9) and Decimal(cf_s) >= d80
        arith_plant = arith_plant and not (cfF - Fraction(1, 10 ** 9) >= cf)
        need_ok = need_ok and cfF <= NEED11 * NEED11
        need_plant = need_plant and not (cfF <= Fraction(2) ** 2)
        r4 = '300 inf %s %s %s %s %s' % (ct_lo, ct_hi, cb_lo, cb_hi, cf_s)
        r4m = '300 inf %s %s %s %s %s' % (ct_lo, ct_hi, cb_lo, cb_hi, cf_s)
        mirror_ok = mirror_ok and r4.split() == r4m.split()
        A = Fraction(N - 1, 2)
        c_h = A - Fraction(MARGIN_T[N])
        spot = (A + c_h) ** 2 * lead[N]
        sp = {}
        for cls in ('D4', 'D4M'):
            rr = spot_rhs(N, cls)
            okc = rr is not None and spot >= rr[2]
            spot_ok = spot_ok and okc
            spot_plant = spot_plant and not (rr is not None and spot * Fraction(1, 10 ** 7) >= rr[2])
            sp[cls] = rr
        nx = sqrt_up(cfF)
        rows[N] = dict(r4=r4, r4m=r4m, coef=cf_s, a0=updec(a0), mh=updec(mh, 16), normx=nx, spot=updec(spot), sp=sp, c_h=c_h)
        out('N%d: A2 <= %s, A0 = N*_RTR mhat(1/300) <= %s, COEF = (A + %s)^2 (A2 + %s^2 A0) = %s, normX at r = 1 <= %s (need 9.3: margin %.3f); '
            'spot %s vs D4 %s, D4M %s' % (N, a2[N], rows[N]['a0'], ct_hi, cb_hi, cf_s, updec(nx, 10), float(NEED11 / nx), rows[N]['spot'],
                                          '%.6e' % float(sp['D4'][2]) if sp['D4'] else 'NONE', '%.6e' % float(sp['D4M'][2]) if sp['D4M'] else 'NONE'))
    plants['PLANT-MIRROR'] = not ('300 inf 0.94 1.06 0.77 0.89 1'.split() == rows[4]['r4'].split())
    res['C-ARITH'], res['C-NEED'], res['C-SPOT'], res['C-MIRROR'] = arith, need_ok, spot_ok, mirror_ok
    plants['PLANT-ARITH'], plants['PLANT-NEED'], plants['PLANT-SPOT'] = arith_plant, need_plant, spot_plant
    for k in ('C-ARITH', 'C-NEED', 'C-SPOT', 'C-MIRROR'):
        out('%s -> %s' % (k, 'PASS' if res[k] else 'FAIL'))
    for k in sorted(plants):
        out('%s -> %s' % (k, 'FIRED' if plants[k] else 'MISSED'))
    if not (all(res.values()) and all(plants.values())):
        out('VERDICT INVALID')
        return 1

    def p(rel):
        return '%s:%s' % (rel, PINS[rel])
    copied = d3_lines()
    R = ['# HS_INV_NORMX_v1 (combined, SPEC v1_2 ADD1 shape (ii)): the D3 lines of HS_INV_NORMX_v1.kv (6b82dc63) token for token, then the',
         '# lemma-form D4 and D4M rows (pk08). Format S4U_KV_v1; lines starting with # are comments. Decimals are exact; COEF is rounded up.']
    R += copied[:4] + ['CODE = pk08/%s.py:%s' % (LABEL, code_sha[:8])] + copied[4:]
    R += ['# D4 and D4M (Lemma D4/D4m of LEMMA_NOTE, reading A; ADD1 sect. 1-3)',
          'OPERATOR_D4 = ' + OPERATOR_D4, 'OPERATOR_D4M = ' + OPERATOR_D4M, 'LAMBDA_POWER_D4 = 1', 'LAMBDA_POWER_D4M = 1',
          'MIRROR_D4M = ADJOINT_OF_D4']
    for N in (4, 3):
        r = rows[N]
        R += ['N%d_D4_ROWS = 1' % N, 'N%d_D4_R000 = %s' % (N, r['r4']), 'N%d_D4_METHOD = LEMMA' % N,
              'N%d_D4M_ROWS = 1' % N, 'N%d_D4M_R000 = %s' % (N, r['r4m']), 'N%d_D4M_METHOD = LEMMA' % N]
    R += ['# D4 binding and INFO keys (not read by the gates)',
          'SPEC_ADD1 = ' + p(ADD1),
          'A2_SOURCE = ' + p(A2ASM[4]) + ' ; ' + p(A2ASM[3]) + ' ; ' + p(A2CODE) + ' ; ' + p(A2REV),
          'N4_A2 = ' + a2[4], 'N3_A2 = ' + a2[3],
          'A2_DEF = A2 = tr_H(K^(1/2) V xi_b^2 K^(1/2))/lambda_h for every J >= 300 (xi_b the MB vertical; equal to the xi_TM value by the T <-> B '
          'mirror), certified by px08_a2cert_v1 (READING line, VERDICT VALID)',
          'A0_SOURCE = ' + p(RTR),
          'N4_RTR = ' + RTRLIT['N4_RTR'], 'N3_RTR = ' + RTRLIT['N3_RTR'],
          'N4_A0_HI = ' + rows[4]['a0'], 'N3_A0_HI = ' + rows[3]['a0'],
          'A0_DEF = A0 = tr_H(T)/lambda_h <= N*_RTR mhat(1/300), mhat(t) = 1 + m1 t + m2 t^2 + m3 t^3 increasing on (0, 1/300] (m1..m3 > 0, '
          'S4_RTR_CERTIFIED_v1 keys N*_MHAT_M1..M3); A0_HI is that product rounded up',
          'FORMULA_D4 = Lemma D4 of LEMMA_NOTE, reading A: HS2 = tr_H(X_c* X_c) <= (A + |c_t|)^2 (A2 + c_b^2 A0) (lambda_h/lambda_0)^1 for every '
          'J >= 300 and every c with c_b >= 0; COEF is its sup over the row\'s box; D4M by the adjoint',
          'OUTWARD_D4 = A2 and A0_HI are decimal upper ends; COEF is exact from them and rounded up; the reader applies the upper end of '
          'lambda_h/lambda_0,lo to the power LAMBDA_POWER_D4',
          '# INFO: normX at r = 1, the needs ((1,1): 9.3; (0,2): 18.5-30.5, plan l.28) and the spot control (the lemma at c_b = 0, harmonic '
          'c_t and A2 -> the lower end of its lead I[GE0]; 2 Cov(X_c, theta X_c) + Cov^2 at the half-step plane)']
    for N in (4, 3):
        r = rows[N]
        R += ['N%d_D4_NORMX_R1 = %s' % (N, updec(r['normx'], 10)), 'N%d_D4_NEED_11 = 9.3' % N]
        for cls in ('D4', 'D4M'):
            rr = r['sp'][cls]
            R.append('N%d_%s_SPOT = %s %s ; c_t harmonic %s ; c_b 0 ; A2 lead lower end ; Cov_LH %s ; Cov^2 %s ; source %s' % (
                N, cls, r['spot'], updec(rr[2], 8), updec(r['c_h'], 6), rr[0], rr[1], p(S8RF[N])))
    R.append('END = HS_INV_NORMX_v1')
    body = '\n'.join(R) + '\n'
    newl = body.split('\n')
    same = [ln for ln in newl if ln in copied]
    if same != copied:
        out('C-D3-SAME (written record) -> FAIL')
        out('VERDICT INVALID')
        return 1
    out('C-D3-SAME (written record: the %d copied lines present in order) -> PASS' % len(copied))
    with open(REC_PATH, 'x') as fh:
        fh.write(body)
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
