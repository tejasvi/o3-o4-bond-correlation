"""m2b_reader_v1_mock.py -- pk11 (code/pk11/mocks/). A MOCK of pk02's m2b_reader_v1 (not frozen yet), with the interface agreed
on 2026-11-07, for kt_s8_cert's stage C mock runs only. Not a script: kt_s8_cert imports it by its pinned sha256 on its MOCK path.
It reads only MOCK records (FORMAT and RECORD 'M2B_KV_v1_MOCK', CLAIM starting 'MOCK '), so no certified record passes it, and its law
is a mock: every quantity is q(J) = q_300 (300/J)^MOCK_RATE, strictly decreasing in J, so a consumer that evaluates the law anywhere but
at a piece's J_lo is caught by its C-UNIF-LAW gate.
  load(path, asm_out, expected_sha256=None) -> rec          the binding to the (mock) asm output, then check()
  loads(record_text, record_name, asm_out_text, expected_sha256=None) -> rec     the same on texts
  check(record_text) -> rec                                  the record's own checks, without the binding
  law_v1(rec, N, J) -> {'eps_r', 's', 'eps_a', 'eps_ds5', 'eps_w', 'eps_d'}: decimal strings at or above the mock law's values, for
      J >= 300 (an int, a Fraction or a decimal string); s is 'inf' when the mock s is not below 1
rec = {'record': name, 'sha256': hex, 'const': {key: (value, end)}, 'N3': {key: (value, end)}, 'N4': {key: (value, end)}}, the values
the record's own strings, end 'upper' or 'exact'. Every refusal raises ValueError.
Format S4U_KV_v1 style: one 'KEY = value' per line, KEY matching [A-Z][A-Z0-9_]*; lines starting with # are comments; blank lines carry
nothing; any other line is refused. Exactly the keys of KEYS_CONST and N3_/N4_ + KEYS_N, each once.
The binding (load, loads): the asm output's VERDICT lines equal exactly ['VERDICT VALID']; its first line is
'm2b_asm_v1_MOCK sha256 <S> ...' with S the record's ASM_SHA256; it holds exactly one 'RECORD <name> <sha256>' line, equal to the
record's base name and the sha256 of its bytes (and to expected_sha256 when given)."""
import os
import re
import hashlib
from fractions import Fraction

KEYS_N = {'EPS_R_300': 'upper', 'S_300': 'upper', 'EPS_A_300': 'upper', 'EPS_DS5_300': 'upper', 'EPS_W_300': 'upper',
          'EPS_D_300': 'upper'}
KEYS_CONST = {'FORMAT': 'exact', 'RECORD': 'exact', 'AUTHOR': 'exact', 'CLAIM': 'exact', 'LAW': 'exact', 'J_MIN': 'exact',
              'MOCK_RATE': 'exact', 'ASM_SHA256': 'exact', 'VERDICT': 'exact'}
FIXED = {'FORMAT': 'M2B_KV_v1_MOCK', 'RECORD': 'M2B_KV_v1_MOCK', 'AUTHOR': 'pk11', 'LAW': 'mock_v1', 'J_MIN': '300',
         'VERDICT': 'VALID'}
OUTS = (('eps_r', 'EPS_R_300'), ('s', 'S_300'), ('eps_a', 'EPS_A_300'), ('eps_ds5', 'EPS_DS5_300'), ('eps_w', 'EPS_W_300'),
        ('eps_d', 'EPS_D_300'))
DEC = re.compile(r'[0-9]+(\.[0-9]+)?(e[-+]?[0-9]+)?')
HEX64 = re.compile(r'[0-9a-f]{64}')


def parse(text):
    d = {}
    for i, ln in enumerate(text.split('\n')):
        if not ln.strip() or ln.startswith('#'):
            continue
        m = re.fullmatch(r'([A-Z][A-Z0-9_]*) = (\S.*)', ln)
        if m is None or m.group(2) != m.group(2).rstrip():
            raise ValueError('mock M2(b): line %d is not KEY = value' % (i + 1))
        if m.group(1) in d:
            raise ValueError('mock M2(b): line %d repeats %s' % (i + 1, m.group(1)))
        d[m.group(1)] = m.group(2)
    return d


def check(record_text):
    d = parse(record_text)
    allowed = set(KEYS_CONST) | {'N%d_%s' % (n, k) for n in (3, 4) for k in KEYS_N}
    if set(d) != allowed:
        raise ValueError('mock M2(b): keys missing %s, extra %s' % (sorted(allowed - set(d)), sorted(set(d) - allowed)))
    for k, v in FIXED.items():
        if d[k] != v:
            raise ValueError('mock M2(b): %s is %r, not %r' % (k, d[k], v))
    if not d['CLAIM'].startswith('MOCK '):
        raise ValueError('mock M2(b): CLAIM does not start with MOCK')
    if HEX64.fullmatch(d['ASM_SHA256']) is None:
        raise ValueError('mock M2(b): ASM_SHA256 is not 64 hex digits')
    if re.fullmatch(r'[1-9]', d['MOCK_RATE']) is None:
        raise ValueError('mock M2(b): MOCK_RATE is not one digit 1-9')
    rec = {'const': {k: (d[k], end) for k, end in KEYS_CONST.items()}}
    for n in (3, 4):
        rec['N%d' % n] = {}
        for k, end in KEYS_N.items():
            v = d['N%d_%s' % (n, k)]
            if DEC.fullmatch(v) is None:
                raise ValueError('mock M2(b): N%d_%s is not a nonnegative decimal' % (n, k))
            rec['N%d' % n][k] = (v, end)
    return rec


def loads(record_text, record_name, asm_out_text, expected_sha256=None):
    rec = check(record_text)
    sha = hashlib.sha256(record_text.encode('utf-8')).hexdigest()
    lines = asm_out_text.split('\n')
    verdicts = [ln for ln in lines if ln.startswith('VERDICT')]
    if verdicts != ['VERDICT VALID']:
        raise ValueError("mock M2(b): the asm output's VERDICT lines are not exactly ['VERDICT VALID']: %r" % verdicts[:3])
    m = re.fullmatch(r'm2b_asm_v1_MOCK sha256 ([0-9a-f]{64})( .*)?', lines[0])
    if m is None or m.group(1) != rec['const']['ASM_SHA256'][0]:
        raise ValueError("mock M2(b): the asm output's first line does not name the record's ASM_SHA256")
    if [ln for ln in lines if ln.startswith('RECORD')] != ['RECORD %s %s' % (record_name, sha)]:
        raise ValueError('mock M2(b): the asm output does not name %s with its sha256 exactly once' % record_name)
    if expected_sha256 is not None and expected_sha256 != sha:
        raise ValueError('mock M2(b): %s is not the expected record' % record_name)
    rec['record'], rec['sha256'] = record_name, sha
    return rec


def load(path, asm_out, expected_sha256=None):
    with open(path, 'rb') as fh:
        rb = fh.read()
    with open(asm_out, 'rb') as fh:
        ab = fh.read()
    return loads(rb.decode('utf-8'), os.path.basename(path), ab.decode('utf-8'), expected_sha256)


def _dec_up(q, digits=17):
    """a decimal string at or above the nonnegative rational q, with `digits` significant digits."""
    q = Fraction(q)
    if q < 0:
        raise ValueError('mock M2(b): a negative law value')
    if q == 0:
        return '0'
    e = 0
    while q >= Fraction(10) ** (e + 1):
        e += 1
    while q < Fraction(10) ** e:
        e -= 1
    x = q * Fraction(10) ** (digits - 1 - e)
    m = -((-x.numerator) // x.denominator)
    return '%de%d' % (m, e - digits + 1)


def law_v1(rec, N, J):
    if N not in (3, 4):
        raise ValueError('mock M2(b): N must be 3 or 4')
    if isinstance(J, str):
        if DEC.fullmatch(J) is None:
            raise ValueError('mock M2(b): J is not a decimal string')
        Jq = Fraction(J)
    elif isinstance(J, (int, Fraction)) and not isinstance(J, bool):
        Jq = Fraction(J)
    else:
        raise ValueError('mock M2(b): J must be an int, a Fraction or a decimal string')
    if Jq < 300:
        raise ValueError('mock M2(b): J below 300')
    f = (Fraction(300) / Jq) ** int(rec['const']['MOCK_RATE'][0])
    res = {}
    for name, key in OUTS:
        q = Fraction(rec['N%d' % N][key][0]) * f
        res[name] = 'inf' if (name == 's' and q >= 1) else _dec_up(q)
    return res
