#!/usr/bin/env python3
"""px08_hsd3b_export_v1_1.py -- pk08: the combined HS record v2, HS_INV_NORMX_v1_d3d4b.kv (SPEC_HS_INV_NORMX_v1_2 ADD1 shape (ii), with
ADD2_1 2ad2cc4c). It copies every line of HS_INV_NORMX_v1_d3d4.kv (bf212cdc) token for token, except its two header comments, CODE and END;
the D3 lines there are those of HS_INV_NORMX_v1.kv (6b82dc63, C-D3-SAME). Then the type-B D3B keys and rows of ADD2_1 sect. 2:
  QB_CRUDE = the smallest 12-digit decimal with QB_CRUDE^2 >= (A + |c_t|)^2 (A + |c_bb|)^2 (1 + TAU_HI^2), and QB_SLOPE = the smallest 12-digit
  decimal >= (A + |c_t|)(A + |c_bb|) TAU_HI. A is the record's N*_A, |c| is at the box's largest, and TAU_HI is the TAU record's N*_TAU_HI
  (TAU_D3B_v1.kv 04dfc7af, bound by its run output cf1d4898). All in exact rationals.
N4 (-1,2) is one of R6's comparisons and stays open until route 0's certified L0 exists (ADD2_1 sect. 3); an INFO key states its need.
Checks with plants that must fire: C-SRC, C-BIND, C-D3-SAME, C-D4-SAME, C-OPSTR, C-KEYS, C-TAU, C-NA, C-NOTE94, C-ARITH, C-BODY (the written
record: both copies in order, the operator line byte for byte, every key once).
Revises the unrun, unfrozen draft px08_hsd3b_export_v1.py (never hashed or cited): the N4 (-1,2) need is printed for N4 only.
Usage: px08_hsd3b_export_v1_1.py run
"""
import sys, os, math, hashlib, resource, signal, time
from fractions import Fraction

if len(sys.argv) != 2 or sys.argv[1] != 'run':
    print('usage: px08_hsd3b_export_v1_1.py run')
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (60, 65))

CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk08'
OUTD = OWN + '/out'
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
OUT_PATH = os.path.join(OUTD, '%s_run.out' % LABEL)
REC_NAME = 'HS_INV_NORMX_v1_d3d4b.kv'
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
D4REC = 'pk08/out/HS_INV_NORMX_v1_d3d4.kv'
D4RUN = 'pk08/out/px08_hsd4_export_v1_run.out'
TAUREC = 'pk08/out/TAU_D3B_v1.kv'
TAURUN = 'pk08/out/px08_tau_d3b_v1_1_run.out'
ADD2 = 'pk15/SPEC_HS_INV_NORMX_v1_2_ADD2_1.md'
NOTE = 'pk08/HS_TYPEB_LEMMA_NOTE_v1_1.md'
PINS = {
    D3REC: '90bbc6f2eaa35cee6b01a77c77995d35659028c9806d5e21278f1899a6c2e67e',
    D3RUN: 'e12440402124d07d7e5795d431b0e1d19073a7e6ae844e4235c650f4e452dea8',
    D4REC: '45a2ab00dcbe47cf6873e5b12db69a1ff8ae3171c84abbc57c5ee43f8a39b343',
    D4RUN: '02122c7f140129bd2bf98e3f6330641eac840519c778f806af07764b3e071ada',
    TAUREC: '24aaccc0890421d5ba533b42067b182a3a1f8014a85c9ad2c04a9e2f99218b95',
    TAURUN: '5d4597327848bece99b270054bc510408b73068b314ce05cafd10ca21e8b0aec',
    ADD2: '89216d7961dc7df87110c96fd4776993b646270cc26e3e0e2ccc439046de2c7e',
    NOTE: '801099463aa4dff112c1bc2078c943f8aff15ecdcf9738aed1a7d9f2f03f0e53',
}
BOX = {4: ('0.94', '1.06', '0.94', '1.06'), 3: ('0.62', '0.72', '0.62', '0.72')}
HEAD4 = ['RECORD = HS_INV_NORMX_v1', 'FORMAT = S4U_KV_v1', 'EXPORT_STATUS = CERTIFIED', 'PRODUCER = pk08']
FIXED = ['LAMBDA_POWER_D3B = 0', 'FIELDS_D3B = jlo jhi ce_lo ce_hi cf_lo cf_hi QB_CRUDE QB_SLOPE', 'N4_D3B_ROWS = 1', 'N4_D3B_METHOD = LEMMA',
         'N3_D3B_ROWS = 1', 'N3_D3B_METHOD = LEMMA']
TEMPL = {N: 'N%d_D3B_R000 = 300 inf %s %s %s %s <QB_CRUDE> <QB_SLOPE>' % ((N,) + BOX[N]) for N in (4, 3)}
OP_HEAD = 'OPERATOR_D3B = X = Z G_t G_bb Z*/lambda_0^3 (OPERATOR_D3, true lambda_0); '
D3B_KEYS = ('LEMMA_NOTE_D3B', 'OPERATOR_D3B', 'LAMBDA_POWER_D3B', 'FIELDS_D3B', 'TAU_SOURCE', 'N4_TAU_HI', 'N3_TAU_HI', 'N4_D3B_ROWS',
            'N4_D3B_R000', 'N4_D3B_METHOD', 'N3_D3B_ROWS', 'N3_D3B_R000', 'N3_D3B_METHOD')
QNEED_N4_M12 = Fraction('5.89')
NOTE_L94 = 'N4 (-1,2) closes by the split form iff ||Q0 X* u||_hi <= 5.89 - 3.9008 = 1.9892.'
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


def rec_lines(rel):
    ls = lines_of(rel)
    return ls[:-1] if ls and ls[-1] == '' else ls


def key_once(rel, key):
    vals = [ln[len(key) + 3:] for ln in lines_of(rel) if ln.startswith(key + ' = ')]
    return vals[0] if len(vals) == 1 else None


def kv_lines(rel):
    """a record's lines to copy: every line except comments, CODE, END and blanks, in order"""
    return [ln for ln in rec_lines(rel) if ln and not ln.startswith('#') and not ln.startswith('CODE = ') and not ln.startswith('END = ')]


def subseq(sub, full):
    """sub appears in full in order, line for line"""
    i = 0
    for ln in full:
        if i < len(sub) and ln == sub[i]:
            i += 1
    return i == len(sub)


def c_bind(shas):
    ok = True
    for run, rec in ((D3RUN, D3REC), (D4RUN, D4REC), (TAURUN, TAUREC)):
        ls = lines_of(run)
        ok = ok and [x for x in ls if x.startswith('VERDICT')] == ['VERDICT VALID']
        ok = ok and [x for x in ls if x.startswith('RECORD')] == ['RECORD %s %s' % (os.path.basename(rec), shas[rec])]
    return ok


def c_d4shape(src):
    return (len(src) > 60 and src[0].startswith('# ') and src[1].startswith('# ') and src[2:6] == HEAD4 and src[6].startswith('CODE = ')
            and src[-1] == 'END = HS_INV_NORMX_v1' and all(not ln.startswith('CODE = ') for ln in src[7:]))


def c_opstr(line):
    ad = lines_of(ADD2)
    return (ad.count(line) == 1 and line.startswith(OP_HEAD) and 'with no lambda factor' in line
            and line.endswith('tau^2 = lambda_0 v_0^2/<u,w>^2 - 1 at tau\'s certified upper end'))


def c_keys(note_line, fixed, templ):
    ad = lines_of(ADD2)
    return (ad.count(note_line) == 1 and note_line == 'LEMMA_NOTE_D3B = %s:%s' % (NOTE, PINS[NOTE])
            and all(ad.count(x) == 1 for x in fixed) and all(ad.count(templ[N]) == 1 for N in (4, 3)))


def c_tau(tau_rec_sha):
    ok = (key_once(TAUREC, 'RECORD') == 'TAU_D3B_v1' and key_once(TAUREC, 'END') == 'TAU_D3B_v1'
          and key_once(TAUREC, 'EXPORT_STATUS') == 'CERTIFIED' and key_once(TAUREC, 'LEMMA_NOTE_D3B') == '%s:%s' % (NOTE, PINS[NOTE])
          and tau_rec_sha == PINS[TAUREC])
    tau = {}
    for N in (4, 3):
        s = key_once(TAUREC, 'N%d_TAU_HI' % N)
        try:
            ok = ok and s is not None and Fraction(s) > 0
        except ValueError:
            ok = False
        tau[N] = s
    return ok, tau


def c_na(lits):
    return all(key_once(D4REC, 'N%d_A' % N) == lits[N] and Fraction(lits[N]) == Fraction(N - 1, 2) for N in (4, 3))


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


def sqrt_up(X, sig=12):
    """the smallest decimal with sig significant digits whose square is >= X (a positive Fraction); exact integer square root"""
    k = sig - 1 - math.floor(math.log10(math.sqrt(float(X))))
    Y = X * Fraction(10) ** (2 * k)
    Yc = -((-Y.numerator) // Y.denominator)
    m = math.isqrt(Yc)
    if m * m < Yc:
        m += 1
    s = str(m)
    if k <= 0:
        return s + '0' * (-k)
    if len(s) <= k:
        s = '0' * (k - len(s) + 1) + s
    return s[:-k] + '.' + s[-k:]


def unit(s):
    return Fraction(1, 10 ** len(s.split('.')[1])) if '.' in s else Fraction(1)


def c_arith(crude, slope, X, S):
    c, s = Fraction(crude), Fraction(slope)
    return c > 0 and c * c >= X and (c - unit(crude)) ** 2 < X and s >= S and s - unit(slope) < S


def c_body(lines, d3, d4, opline):
    keys = [ln.split(' = ', 1)[0] for ln in lines if ln and not ln.startswith('#')]
    return (subseq(d3, lines) and subseq(d4, lines) and lines.count(opline) == 1 and len(keys) == len(set(keys))
            and all(keys.count(k) == 1 for k in D3B_KEYS) and lines[-1] == 'END = HS_INV_NORMX_v1'
            and sum(ln.startswith('CODE = ') for ln in lines) == 1)


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
    bad[TAUREC] = bad[TAUREC][:-1] + ('0' if bad[TAUREC][-1] != '0' else '1')
    plants['PLANT-SRC'] = not c_src(bad)
    DATA.clear()
    DATA.update(good)
    res['C-BIND'] = c_bind(PINS)
    plants['PLANT-BIND'] = not c_bind(dict(PINS, **{TAUREC: PINS[D3REC]}))
    src = rec_lines(D4REC)
    d3, d4 = kv_lines(D3REC), kv_lines(D4REC)
    res['C-D3-SAME'] = len(d3) == 40 and subseq(d3, d4) and c_bind(PINS)
    plants['PLANT-D3-SAME'] = not subseq(d3[:-1] + [d3[-1] + ' '], d4)
    res['C-D4-SAME'] = c_d4shape(src) and kv_lines(D4REC) == [ln for ln in src[2:6] + src[7:-1] if ln and not ln.startswith('#')]
    plants['PLANT-D4-SAME'] = not c_d4shape(src[:6] + src[7:])
    ops = [ln for ln in lines_of(ADD2) if ln.startswith('OPERATOR_D3B = X = ')]
    opline = ops[0] if len(ops) == 1 else ''
    res['C-OPSTR'] = len(ops) == 1 and c_opstr(opline)
    plants['PLANT-OPSTR'] = not c_opstr(opline.replace('with no lambda factor', 'with a lambda factor'))
    notes = [ln for ln in lines_of(ADD2) if ln.startswith('LEMMA_NOTE_D3B = ')]
    note_line = notes[0] if len(notes) == 1 else ''
    res['C-KEYS'] = len(notes) == 1 and c_keys(note_line, FIXED, TEMPL)
    plants['PLANT-KEYS'] = not c_keys(note_line, FIXED[:-1] + ['N3_D3B_METHOD = SCAN'], TEMPL)
    tau_ok, tau = c_tau(PINS[TAUREC])
    res['C-TAU'] = tau_ok and c_bind(PINS)
    plants['PLANT-TAU'] = not c_tau(PINS[D4REC])[0]
    A = {4: '3/2', 3: '1'}
    res['C-NA'] = c_na(A)
    plants['PLANT-NA'] = not c_na({4: '3/2', 3: '3/2'})
    nt = lines_of(NOTE)
    res['C-NOTE94'] = len(nt) > 94 and NOTE_L94 in nt[93]
    plants['PLANT-NOTE94'] = not (NOTE_L94.replace('5.89', '5.98') in nt[93])
    for k in ('C-BIND', 'C-D3-SAME', 'C-D4-SAME', 'C-OPSTR', 'C-KEYS', 'C-TAU', 'C-NA', 'C-NOTE94'):
        out('%s -> %s' % (k, 'PASS' if res[k] else 'FAIL'))
    if not (res['C-TAU'] and res['C-NA'] and res['C-OPSTR'] and res['C-KEYS']):
        out('VERDICT INVALID')
        return 1
    rows = {}
    ar_ok = ar_pl = True
    for N in (4, 3):
        ce_lo, ce_hi, cf_lo, cf_hi = (Fraction(x) for x in BOX[N])
        a = Fraction(A[N])
        ct, cb = max(abs(ce_lo), abs(ce_hi)), max(abs(cf_lo), abs(cf_hi))
        T = Fraction(tau[N])
        X = (a + ct) ** 2 * (a + cb) ** 2 * (1 + T * T)
        S = (a + ct) * (a + cb) * T
        crude, slope = sqrt_up(X), dec(S, 12, True)
        ar_ok = ar_ok and c_arith(crude, slope, X, S)
        ar_pl = (ar_pl and not c_arith(str(Fraction(crude) - unit(crude)), slope, X, S)
                 and not c_arith(crude, dec(S, 12, False), X, S))
        need = QNEED_N4_M12 - Fraction(slope) if N == 4 else None
        rows[N] = dict(crude=crude, slope=slope, row='300 inf %s %s %s %s %s %s' % (BOX[N] + (crude, slope)), need=need)
        tail = ('; N4 (-1,2) needs ||Q0 X* u||_hi <= 5.89 - QB_SLOPE = %s' % (dec(need, 12, False) if need > 0 else '(negative)')) if N == 4 else ''
        out('N%d: A %s, |c_t| <= %s, |c_bb| <= %s, TAU_HI %s: QB_CRUDE %s (^2 >= %s), QB_SLOPE %s (>= %s); row %s%s' % (
            N, A[N], BOX[N][1], BOX[N][3], tau[N], crude, dec(X, 15, False), slope, dec(S, 15, False), rows[N]['row'], tail))
    res['C-ARITH'] = ar_ok
    plants['PLANT-ARITH'] = ar_pl
    out('C-ARITH -> %s' % ('PASS' if ar_ok else 'FAIL'))
    if not (rows[4]['need'] > 0):
        out('VERDICT INVALID')
        return 1

    def p(rel):
        return '%s:%s' % (rel, PINS[rel])
    R = ['# HS_INV_NORMX_v1 (combined, SPEC v1_2 ADD1 shape (ii) with ADD2_1): the lines of HS_INV_NORMX_v1_d3d4.kv (bf212cdc) token for',
         '# token (its D3 lines are those of HS_INV_NORMX_v1.kv, 6b82dc63), then the type-B D3B rows (pk08). Format S4U_KV_v1; lines',
         '# starting with # are comments. Decimals are exact; COEF, QB_CRUDE and QB_SLOPE are rounded up.']
    R += src[2:6] + ['CODE = pk08/%s.py:%s' % (LABEL, code_sha[:8])] + src[7:-1]
    R += ['# D3B (Lemma B of LEMMA_NOTE_D3B, the type-B rows of D3 at d_L = -1; ADD2_1 sect. 1-2)',
          note_line, opline, 'LAMBDA_POWER_D3B = 0', 'FIELDS_D3B = jlo jhi ce_lo ce_hi cf_lo cf_hi QB_CRUDE QB_SLOPE',
          'TAU_SOURCE = ' + p(TAUREC), 'N4_TAU_HI = ' + tau[4], 'N3_TAU_HI = ' + tau[3]]
    for N in (4, 3):
        R += ['N%d_D3B_ROWS = 1' % N, 'N%d_D3B_R000 = %s' % (N, rows[N]['row']), 'N%d_D3B_METHOD = LEMMA' % N]
    R += ['# D3B binding and INFO keys (not read by the gates)',
          'SPEC_ADD2_1 = ' + p(ADD2),
          'TAU_RUN = ' + p(TAURUN),
          'FORMULA_D3B = Lemma B of LEMMA_NOTE_D3B: for every J >= 300 and every c, q = ||Q0 X* a|| <= (A + |c_t|)(A + |c_bb|)(1 + tau^2)^(1/2) '
          'and q <= ||Q0 X* u|| + (A + |c_t|)(A + |c_bb|) tau, with tau <= N*_TAU_HI (TAU_SOURCE); QB_CRUDE and QB_SLOPE are their sups over '
          'the row\'s box (|c| at the box\'s largest); no lambda factor (LAMBDA_POWER_D3B = 0)',
          'OUTWARD_D3B = N*_TAU_HI is the TAU record\'s upper end, copied; QB_CRUDE is the smallest 12-digit decimal with QB_CRUDE^2 >= '
          '(A + |c_t|)^2 (A + |c_bb|)^2 (1 + N*_TAU_HI^2), QB_SLOPE the smallest 12-digit decimal >= (A + |c_t|)(A + |c_bb|) N*_TAU_HI, both in '
          'exact rationals',
          'INFO_D3B_OPEN = N4 (d_L, d_R) = (-1, 2) stays open (ADD2_1 sect. 3): N4 QB_CRUDE %s is above its q_need 5.89 (LEMMA_NOTE_D3B l.94), '
          'and the split form needs ||Q0 X* u||_hi <= 5.89 - N4 QB_SLOPE = %s from route 0\'s certified L0 (R6.4), which does not exist yet. '
          'R6 compares the other near-end rows (d_R = 2..6, far, inf at both N) with its own q_need' % (rows[4]['crude'],
                                                                                                      dec(rows[4]['need'], 12, False))]
    R.append('END = HS_INV_NORMX_v1')
    res['C-BODY'] = c_body(R, d3, d4, opline)
    bad_body = list(R)
    bad_body[bad_body.index('N4_D3B_ROWS = 1')] = 'N4_D3B_ROWS = 2'
    bad_body.insert(len(bad_body) - 1, 'N4_D3B_ROWS = 1')
    plants['PLANT-BODY'] = (not c_body(bad_body, d3, d4, opline)
                            and not c_body([ln if not ln.startswith('N4_D3_R000 = ') else ln + '0' for ln in R], d3, d4, opline))
    out('C-BODY (written record: %d D3 lines and %d D4-record lines in order, the operator line once, every key once) -> %s' % (
        len(d3), len(d4), 'PASS' if res['C-BODY'] else 'FAIL'))
    for k in sorted(plants):
        out('%s -> %s' % (k, 'FIRED' if plants[k] else 'MISSED'))
    if not (all(res.values()) and all(plants.values())):
        out('VERDICT INVALID')
        return 1
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
