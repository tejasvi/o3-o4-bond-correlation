#!/usr/bin/env python3
"""m2b_reader_v1.py -- pk02 (code/pk02/). The one sha-pinned reader of the certified vacuum record M2B_KV_v1 (SPEC_M2B_CERT_v1
ffd842a2 sect. 3, 3a and 4, with ADD1 2c97391f and ADD2 48d5fa54), for both consumers (pk07's kt_s9h_v1 VERTICAL mode, pk11's
S8) and for m2b_asm_v1's read-back. Interface, as agreed with pk11 and pk07 (2026-11-07):
  load(path, asm_out, expected_sha256=None, reader_sha256=None) -> rec the certified entry: the binding to m2b_asm_v1's run output, check(), and C-PINS
  loads(record_text, record_name, asm_out_text, expected_sha256=None) -> rec    the same on texts, without C-PINS (for plants)
  check(record_text) -> rec      the record's own checks, without the binding (m2b_asm_v1's read-back, before its own VERDICT exists)
  law_v1(rec, N, J) -> {'eps_r', 's', 'eps_a', 'eps_ds5', 'eps_w', 'eps_d'}: decimal strings at or above the upper ends, for J >= 300
      (an int, a Fraction or a decimal string); s is 'inf' when 2 - Rtr - eps_r is not certainly positive
  law_balls(P, J) -> the same six quantities as arb balls, from a dict P of arb balls (the law m2b_asm_v1 evaluates)
rec = {'record': name, 'sha256': hex, 'const': {key: (value, end)}, 'N3': {key: (value, end)}, 'N4': {key: (value, end)}}: the values are
the record's own strings (decimals; ' ; '-separated lists for WT, DL and VQ; 'p/q' for A_M, A_E and A_PP; the hex of RHO_PP_HEX), end is
'upper', 'lower' or 'exact' (SPEC sect. 3a). Every refusal raises ValueError.
Format S4U_KV_v1 style: one 'KEY = value' per line with KEY matching [A-Z][A-Z0-9_]*, lines starting with # are comments, blank lines
carry nothing; any other line is refused.
Checks of the record (check):
  - exactly the allowed keys (KEYS_CONST, KEYS_N for N3_ and N4_, KEYS_PIN), each once (an allow-list; nothing else may appear);
  - FORMAT = M2B_KV_v1, RECORD = M2B_KV_v1, LAW = v1, VERDICT = VALID, and CLAIM equal to this reader's CLAIM text, by exact equality;
  - every number a finite nonnegative decimal; WT and DL three entries each;
  - the constants J1 150, J0 170, J_MIN 300, CXI 0.6594, VQ 0.66767 ; 0.56373, KAPPA 0.41729;
  - the boundaries A_M = Fraction(0.55)^2, A_E = Fraction(0.6)^2, A_PP = Fraction(float.fromhex(RHO_PP_HEX))^2, with
    arb(A_PP) >= sin^2(asin 0.55 + 40 deg); N*_AE <= A_E and KAPPA_B <= kappa_B = 2 (1 - cos 40 deg) - a^2/(4 (1 - a)), a = A_E (lower ends);
  - C-CXI: CXI >= 4 (1 - sqrt(1 - A_M));
  - C-MONO: every term of LAW v1 is nonincreasing in J on [300, oo): N*_AE >= 1/45 and KAPPA_B >= 2/135 (J e^{-0.15 AE J} and
    J e^{-0.225 KAPPA_B J}, in J near and cw J tails), the fixed rates of J^4 e^{-0.15125 J} and J^2 e^{-0.95 (1 - cos 40 deg) J/2}
    (the (wg J)^2 fJ and wg J g terms) at least 4/300 and 2/300, and 2 - N*_RTR - eps_r(300) > 0 (then s is nonincreasing as well);
  - C-FMT: LAW v1 at J = 300 on the keys at their safe ends; each N*_<EPS>_300 at or above the ball's upper end and within 1e-9 of it.
The binding (load, loads): asm_out's VERDICT lines equal exactly ['VERDICT VALID']; its first line is 'm2b_asm_v1 sha256 <S> ...' with
S = the record's ASM_SHA256; it holds exactly one 'RECORD <name> <sha256>' line, equal to the record's base name and sha256 (and to
expected_sha256 when given). C-PINS (load): every PIN_* token 'path:sha256' (paths relative to code/) names an existing file with that
sha256; the PIN_CODE token of m2b_reader_v1.py equals this file's sha256.
Script mode: argv = record, asm output[, expected sha256]: prints the checks, C-FMT, C-MONO and the plants (PLANT-SWAP: N4_NP and N4_D5
exchanged; PLANT-MOCK: FORMAT 'M2B_KV_v1 MOCK' and a 'MOCK ' claim prefix; PLANT-PRECERT: FORMAT 'M2B_KV_v1_PRECERT'; PLANT-VERDICT:
'VERDICT = VALID-PRECERT'; PLANT-BIND: the asm output's RECORD sha256 changed; PLANT-MONO: N4_AE = 0.02 < 1/45), each must be refused.
Run (own folder): D=/mnt/g2/release/root/code/pk02; OMP_NUM_THREADS=1 timeout 300 nice -n 10 prlimit --as=4294967296 --
  python3 -I -B $D/m2b_reader_v1.py <record> <asm output> > <out> 2> <err>
Also checked: N*_TX_LAMSTAR and N*_ANN_LAMSTAR are exactly one of 0.3, 0.45, 0.6 (LAW v1's dec rate needs lambda* >= 0.3); the
headroom quotes of SPEC sect. 4, agreed with pk07: N*_Z2_FLOAT (vac_float's Z2, vacmono's Z2low(J1)) and N*_RTR_FLOAT (S4's
TARGET_FLOAT), exact as quoted, and N*_Z2_FACTOR >= Z2_FLOAT / N*_Z2 and N*_RTR_FACTOR >= N*_RTR / RTR_FLOAT (upper ends: the part of
S7's headroom the certification itself used against FLOAT).
"""
import sys, os, re, hashlib
from fractions import Fraction
from flint import arb, ctx

ctx.prec = 256
CODEDIR = '/mnt/g2/release/root/code'
CLAIM = ('for N in {3, 4} and every J >= 300 (t = 1/J in (0, 1/300], t -> 0 included), the vacuum residual parameters of LAW v1 hold '
         'with the keys of this record at their stated safe ends (SPEC_M2B_CERT_v1 sect. 3a: lower for N*_Z2, N*_AE and KAPPA_B, exact for '
         'the constants, upper for every other key), in the |g| form: with g = VK phi - mhat phi and psihat = K^{1/2} phi the trial '
         'vacuum, ||K^{1/2} |g| || <= eps_r mhat ||psihat|| (hence ||(T - mhat) psihat|| <= eps_r mhat ||psihat||), and eps_a, eps_ds5, '
         'eps_w, eps_d bound ||K^{1/2} |w g| ||/(mhat ||psihat||) for their multipliers w (PK10_NOTES sect. 19.3.3 (v), Lemma 19.5w); '
         'eps_r, s, eps_a, eps_ds5, eps_w and eps_d of LAW v1 on these keys are nonincreasing in J on [300, oo) (C-MONO); and '
         'N*_EPS_R_300, N*_S_300, N*_EPS_A_300, N*_EPS_DS5_300, N*_EPS_W_300, N*_EPS_D_300 are upper ends of them at J = 300')
KEYS_N = {'NP': 'upper', 'R1': 'upper', 'D5': 'upper', 'R0': 'upper', 'TX': 'upper', 'TX_LAMSTAR': 'exact', 'TB': 'upper',
          'ANN': 'upper', 'ANN_LAMSTAR': 'exact', 'FAR': 'upper', 'MHAT_UP': 'upper', 'GB': 'upper', 'Z2': 'lower', 'RTR': 'upper',
          'AE': 'lower', 'WT': 'upper', 'DL': 'upper', 'WT_R1': 'upper', 'DL_R1': 'upper', 'EPS_R_300': 'upper', 'S_300': 'upper',
          'EPS_A_300': 'upper', 'EPS_DS5_300': 'upper', 'EPS_W_300': 'upper', 'EPS_D_300': 'upper', 'Z2_FLOAT': 'exact', 'Z2_FACTOR': 'upper',
          'RTR_FLOAT': 'exact', 'RTR_FACTOR': 'upper'}
LAMS = ('0.3', '0.45', '0.6')       # the tail pieces' lambdas; LAW v1's dec rate 0.3 needs lambda* >= 0.3
KEYS_CONST = {'FORMAT': 'exact', 'RECORD': 'exact', 'AUTHOR': 'exact', 'WRITTEN_UTC': 'exact', 'CLAIM': 'exact', 'LAW': 'exact',
              'J1': 'exact', 'J0': 'exact', 'J_MIN': 'exact', 'CXI': 'exact', 'VQ': 'exact', 'KAPPA': 'exact', 'KAPPA_B': 'lower',
              'A_M': 'exact', 'A_E': 'exact', 'A_PP': 'exact', 'RHO_PP_HEX': 'exact', 'ASM_SHA256': 'exact', 'VERDICT': 'exact'}
KEYS_PIN = ('PIN_CODE', 'PIN_LAYER', 'PIN_TRIAL', 'PIN_PIECES_N4', 'PIN_PIECES_N3', 'PIN_REP', 'PIN_M3_N4', 'PIN_M3_N3', 'PIN_M3_CODE',
            'PIN_S4')
FIXED = {'FORMAT': 'M2B_KV_v1', 'RECORD': 'M2B_KV_v1', 'AUTHOR': 'pk02', 'LAW': 'v1', 'J1': '150', 'J0': '170', 'J_MIN': '300',
         'CXI': '0.6594', 'VQ': '0.66767 ; 0.56373', 'KAPPA': '0.41729', 'VERDICT': 'VALID'}
FMT = (('EPS_R_300', 'eps_r'), ('S_300', 's'), ('EPS_A_300', 'eps_a'), ('EPS_DS5_300', 'eps_ds5'), ('EPS_W_300', 'eps_w'),
       ('EPS_D_300', 'eps_d'))
DEC = re.compile(r'[0-9]+(\.[0-9]+)?(e[-+]?[0-9]+)?')
HEX64 = re.compile(r'[0-9a-f]{64}')
A_M, A_E = Fraction(0.55) ** 2, Fraction(0.6) ** 2
# ---------------------------------------------------------------------------- LAW v1 in balls (SPEC_M2B_CERT_v1 sect. 3)
CXI = arb('0.6594')                 # vac_float's c_xi, >= 4 (1 - sqrt(1 - a_m)) (C-CXI)
A_M_LAW = arb('0.3025')             # fJ's rate (vac_float's form; the outer_far gate r >= 0.5 a_m with a_m = Fraction(0.55)^2 > 0.3025)
COS40 = (arb.pi() * 40 / 180).cos()


def farb(f):
    """an exact Fraction as an arb ball (exact when the denominator is a power of 2, else a containing ball)."""
    f = Fraction(f)
    return arb(f.numerator) / f.denominator


def law_balls(P, J):
    """LAW v1 at J (>= 300) from the balls P: NP, R1, D5, R0, TX, ANN, TB, FAR, GB, RTR, NPM_WT, R1_WT, D5W_WT, R0W_WT and the _DL set
    (upper ends), Z2, AE, KAPPA_B (lower ends). Returns {eps_r, s, eps_a, eps_ds5, eps_w, eps_d} as balls."""
    J = farb(J) if not isinstance(J, arb) else J
    sig, sig7 = 150 / J, 170 / J
    dec = (-arb('0.3') * P['AE'] * (J - 150) / 2).exp()
    tails = (P['TX'] + P['ANN']) * dec + P['TB'] * (-arb('0.45') * P['KAPPA_B'] * (J - 150) / 2).exp()
    near = P['NP'] * sig ** 2 + P['R1'] * sig + (P['D5'] + P['R0']) * sig ** 5 + tails
    fJ = P['FAR'] * (J / 150) ** 2 * (-arb('0.5') * A_M_LAW * (J - 150)).exp()
    g = P['GB'] * (J / 150) * (-arb('0.95') * (1 - COS40) * (J - 150) / 2).exp()
    rz = P['Z2'].sqrt()
    eps = ((near * near + fJ).sqrt() + g) / rz
    s = eps / (2 - P['RTR'] - eps)

    def wres(cw, wg):
        return (((cw * J * near) ** 2 + (wg * J) ** 2 * fJ).sqrt() + wg * J * g) / rz

    def ew(w, cw, wg):
        nw = P['NPM_' + w] * sig7 ** 2 + P['R1_' + w] * sig7 + (P['D5W_' + w] + P['R0W_' + w]) * sig7 ** 5 + cw * J * tails
        return ((nw * nw + (wg * J) ** 2 * fJ).sqrt() + wg * J * g) / rz
    return dict(eps_r=eps, s=s, eps_a=wres(CXI, arb(2)), eps_ds5=wres(CXI / 2, arb(1)), eps_w=ew('WT', CXI, arb(2)),
                eps_d=ew('DL', CXI / 2, arb(1)))


def balls_of(rec, n):
    """the law's balls from rec's N n keys (each a ball containing the record's decimal; the decimal is the key's safe end)."""
    kn = rec['N%d' % n]
    P = {k: arb(kn[k][0]) for k in ('NP', 'R1', 'D5', 'R0', 'TX', 'ANN', 'TB', 'FAR', 'GB', 'Z2', 'RTR', 'AE')}
    P['KAPPA_B'] = arb(rec['const']['KAPPA_B'][0])
    for w in ('WT', 'DL'):
        a, b, c = kn[w][0].split(' ; ')
        P.update({'NPM_' + w: arb(a), 'D5W_' + w: arb(b), 'R0W_' + w: arb(c), 'R1_' + w: arb(kn[w + '_R1'][0])})
    return P


def frac_upper(x):
    """the exact upper end of a ball as a Fraction."""
    m, e = x.upper().man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def dec_up(f, digits=17):
    """a decimal string at or above the Fraction f >= 0 (rounded up exactly to the given significant digits)."""
    if f < 0:
        raise ValueError('dec_up: negative value %r' % f)
    if f == 0:
        return '0'
    e = len(str(f.numerator)) - len(str(f.denominator))
    while Fraction(10) ** e > f:
        e -= 1
    while Fraction(10) ** (e + 1) <= f:
        e += 1
    k = digits - 1 - e
    sc = f * Fraction(10) ** k
    n = -((-sc.numerator) // sc.denominator)
    if n == 10 ** digits:
        n, e = 10 ** (digits - 1), e + 1
    s = str(n)
    return '%s.%se%+03d' % (s[0], s[1:], e)


def law_v1(rec, N, J):
    """the consumer's law: LAW v1 at J >= 300 on rec's N keys, each value a decimal string at or above its upper end ('inf' for s if
    2 - Rtr - eps_r is not certainly positive)."""
    if N not in (3, 4):
        raise ValueError('law_v1: N must be 3 or 4')
    Jf = Fraction(J)
    if Jf < 300:
        raise ValueError('law_v1: J = %s below J_MIN 300' % J)
    P = balls_of(rec, N)
    got = law_balls(P, farb(Jf))
    out = {}
    for k in ('eps_r', 's', 'eps_a', 'eps_ds5', 'eps_w', 'eps_d'):
        if k == 's' and not bool(2 - P['RTR'] - got['eps_r'] > 0):
            out[k] = 'inf'
        else:
            out[k] = dec_up(frac_upper(got[k]))
    return out


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(text):
    kv = {}
    for ln in text.splitlines():
        if not ln.strip() or ln.startswith('#'):
            continue
        mt = re.fullmatch(r'([A-Z][A-Z0-9_]*) = (.*)', ln)
        if mt is None:
            raise ValueError('not a KEY = value line: %r' % ln[:60])
        if mt.group(1) in kv:
            raise ValueError('key %s twice' % mt.group(1))
        kv[mt.group(1)] = mt.group(2)
    return kv


def dec(s, what):
    if not DEC.fullmatch(s):
        raise ValueError('%s: not a nonnegative finite decimal: %r' % (what, s[:40]))
    return Fraction(s)


def check(text):
    """the record's own checks (see the docstring); returns rec without 'record' and 'sha256'."""
    kv = parse(text)
    want = set(KEYS_CONST) | set(KEYS_PIN) | {'N%d_%s' % (n, k) for n in (3, 4) for k in KEYS_N}
    if set(kv) != want:
        raise ValueError('keys: missing %s; not allowed %s' % (sorted(want - set(kv))[:6], sorted(set(kv) - want)[:6]))
    for k, v in FIXED.items():
        if kv[k] != v:
            raise ValueError('%s = %r (must be %r)' % (k, kv[k][:40], v))
    if kv['CLAIM'] != CLAIM:
        raise ValueError('CLAIM differs from the certified text')
    if not HEX64.fullmatch(kv['ASM_SHA256']):
        raise ValueError('ASM_SHA256 is not a full sha256')
    if not re.fullmatch(r'20[0-9]{2}-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]Z', kv['WRITTEN_UTC']):
        raise ValueError('WRITTEN_UTC is not a UTC stamp')
    for k in KEYS_PIN:
        for tok in kv[k].split(' ; '):
            p, _, h = tok.rpartition(':')
            if not (p and HEX64.fullmatch(h) and not p.startswith('/') and '..' not in p.split('/')):
                raise ValueError('%s: bad token %r' % (k, tok[:60]))
    rho = float.fromhex(kv['RHO_PP_HEX'])
    if Fraction(kv['A_M']) != A_M or Fraction(kv['A_E']) != A_E or Fraction(kv['A_PP']) != Fraction(rho) ** 2 or \
            kv['RHO_PP_HEX'] != rho.hex():
        raise ValueError('boundaries differ from ADD1 sect. 1 / ADD2 sect. 2')
    if not bool(farb(Fraction(kv['A_PP'])) >= (arb('0.55').asin() + arb.pi() * 40 / 180).sin() ** 2):
        raise ValueError('A_PP below sin^2(asin rho_m + delta)')
    kap = 2 * (1 - COS40) - farb(A_E) ** 2 / (4 * (1 - farb(A_E)))
    kb = dec(kv['KAPPA_B'], 'KAPPA_B')
    if not bool(farb(kb) <= kap):
        raise ValueError('KAPPA_B is not a lower end of kappa_B')
    if not bool(CXI >= 4 * (1 - (1 - farb(A_M)).sqrt())):
        raise ValueError('C-CXI: CXI below 4 (1 - sqrt(1 - a_m))')
    rg = arb('0.95') * (1 - COS40) / 2
    if not (kb >= Fraction(2, 135) and bool(rg >= arb(2) / 300) and Fraction('0.15125') >= Fraction(4, 300)):
        raise ValueError('C-MONO: KAPPA_B or a fixed rate too small for J >= 300')
    rec = {'const': {k: (kv[k], KEYS_CONST[k]) for k in KEYS_CONST}}
    rec['const'].update({k: (kv[k], 'exact') for k in KEYS_PIN})
    for n in (3, 4):
        kn = {}
        for k, end in KEYS_N.items():
            v = kv['N%d_%s' % (n, k)]
            parts = v.split(' ; ')
            if len(parts) != (3 if k in ('WT', 'DL') else 1):
                raise ValueError('N%d_%s: %d entries' % (n, k, len(parts)))
            for i, x in enumerate(parts):
                dec(x, 'N%d_%s[%d]' % (n, k, i))
            kn[k] = (v, end)
        rec['N%d' % n] = kn
        if kn['TX_LAMSTAR'][0] not in LAMS or kn['ANN_LAMSTAR'][0] not in LAMS:
            raise ValueError('N%d: TX_LAMSTAR or ANN_LAMSTAR is not one of %s (LAW v1 needs lambda* >= 0.3)' % (n, ', '.join(LAMS)))
        if not (Fraction(kn['Z2_FACTOR'][0]) >= Fraction(kn['Z2_FLOAT'][0]) / Fraction(kn['Z2'][0]) and
                Fraction(kn['RTR_FACTOR'][0]) >= Fraction(kn['RTR'][0]) / Fraction(kn['RTR_FLOAT'][0])):
            raise ValueError('N%d: a headroom FACTOR is below its quotient (Z2_FLOAT / Z2, RTR / RTR_FLOAT)' % n)
        ae = Fraction(kn['AE'][0])
        if not (ae <= A_E and ae >= Fraction(1, 45)):
            raise ValueError('N%d_AE: not a lower end of a_e, or below C-MONO\'s 1/45' % n)
        P = balls_of(rec, n)
        got = law_balls(P, arb(300))
        if not bool(2 - P['RTR'] - got['eps_r'] > 0):
            raise ValueError('C-MONO N%d: 2 - RTR - eps_r(300) is not certainly positive' % n)
        for k, nm in FMT:
            v, u = Fraction(kn[k][0]), frac_upper(got[nm])
            if not (u <= v <= u * (1 + Fraction(1, 10 ** 9))):
                raise ValueError('C-FMT N%d_%s: record %s, LAW v1 upper end %s' % (n, k, kn[k][0], dec_up(u)))
    return rec


def loads(record_text, record_name, asm_out_text, expected_sha256=None):
    """the binding to m2b_asm_v1's run output, then check() (no C-PINS)."""
    h = sha(record_text.encode())
    if expected_sha256 is not None and h != expected_sha256:
        raise ValueError('sha256 %s differs from the pin' % h)
    lines = asm_out_text.splitlines()
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise ValueError('asm output: VERDICT lines are not exactly [VERDICT VALID]')
    kv = parse(record_text)
    mt = re.match(r'm2b_asm_v1 sha256 ([0-9a-f]{64}) ', lines[0] if lines else '')
    if mt is None or mt.group(1) != kv.get('ASM_SHA256'):
        raise ValueError('asm output: the header does not name the record\'s ASM_SHA256')
    rl = [ln for ln in lines if ln.startswith('RECORD ')]
    if rl != ['RECORD %s %s' % (record_name, h)]:
        raise ValueError('asm output: RECORD lines %r do not bind %s %s' % ([x[:80] for x in rl], record_name, h[:8]))
    rec = check(record_text)
    rec.update(record=record_name, sha256=h)
    return rec


def load(path, asm_out, expected_sha256=None, reader_sha256=None):
    """the certified entry: loads() on the files, then C-PINS. C-PINS needs this reader's own sha256: reader_sha256 (the sha256 of the
    bytes a consumer checked and exec()ed) or, when the reader runs as a file, the sha256 of __file__."""
    with open(path, 'rb') as fh:
        data = fh.read()
    with open(asm_out) as fh:
        atext = fh.read()
    rec = loads(data.decode(), os.path.basename(path), atext, expected_sha256)
    if reader_sha256 is not None:
        if not HEX64.fullmatch(str(reader_sha256)):
            raise ValueError('C-PINS: reader_sha256 is not a full sha256')
        own = reader_sha256
    elif '__file__' in globals():
        own = sha(open(os.path.abspath(globals()['__file__']), 'rb').read())
    else:
        raise ValueError('C-PINS: this reader runs without __file__ (exec); pass reader_sha256, the sha256 of the bytes you executed')
    seen_self = False
    for k in KEYS_PIN:
        for tok in rec['const'][k][0].split(' ; '):
            p, _, h = tok.rpartition(':')
            try:
                got = sha(open(os.path.join(CODEDIR, p), 'rb').read())
            except OSError:
                got = 'MISSING'
            if got != h:
                raise ValueError('C-PINS: %s %s (pinned %s)' % (p, got[:8], h[:8]))
            if p == 'pk02/m2b_reader_v1.py':
                seen_self = h == own
    if not seen_self:
        raise ValueError('C-PINS: PIN_CODE does not name this reader\'s sha256')
    return rec


def _refused(fn, *a):
    try:
        fn(*a)
        return False, ''
    except ValueError as e:
        return True, str(e)


def _sub(text, key, new):
    return '\n'.join(('%s = %s' % (key, new)) if ln.startswith(key + ' = ') else ln for ln in text.splitlines()) + '\n'


if __name__ == '__main__':
    path, aout = sys.argv[1], sys.argv[2]
    pin = sys.argv[3] if len(sys.argv) > 3 else None
    print('m2b_reader_v1 sha256 %s; record %s; asm output %s' % (sha(open(os.path.abspath(__file__), 'rb').read()), os.path.basename(path),
                                                               os.path.basename(aout)))
    fails = []
    try:
        rec = load(path, aout, pin)
        print('READ: binding, every record check, C-MONO, C-FMT and C-PINS PASS (%d keys per N)' % len(rec['N4']))
        for n in (4, 3):
            print('LAW N=%d J=300: %s' % (n, ' '.join('%s %s' % kv for kv in sorted(law_v1(rec, n, 300).items()))))
    except ValueError as e:
        print('READ: refused: %s' % e)
        fails.append('READ')
    text = open(path).read()
    atext = open(aout).read()
    kv = parse(text)
    name = os.path.basename(path)
    sw = _sub(_sub(text, 'N4_NP', kv['N4_D5']), 'N4_D5', kv['N4_NP'])
    plants = [('PLANT-SWAP', lambda: check(sw)),
              ('PLANT-MOCK', lambda: check(_sub(_sub(text, 'FORMAT', 'M2B_KV_v1 MOCK'), 'CLAIM', 'MOCK ' + kv['CLAIM']))),
              ('PLANT-PRECERT', lambda: check(_sub(text, 'FORMAT', 'M2B_KV_v1_PRECERT'))),
              ('PLANT-VERDICT', lambda: check(_sub(text, 'VERDICT', 'VALID-PRECERT'))),
              ('PLANT-BIND', lambda: loads(text, name, re.sub(r'^(RECORD \S+ )[0-9a-f]{64}$', r'\g<1>' + '0' * 64, atext, flags=re.M))),
              ('PLANT-MONO', lambda: check(_sub(text, 'N4_AE', '0.02')))]
    for nm, fn in plants:
        ok, why = _refused(fn)
        print('%s -> %s (%s)' % (nm, 'FIRES' if ok else 'DOES NOT FIRE', why[:100]))
        if not ok:
            fails.append('%s did not fire' % nm)
    print('VERDICT %s' % ('VALID' if not fails else 'INVALID (%s)' % ', '.join(fails)))
