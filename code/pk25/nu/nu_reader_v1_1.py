#!/usr/bin/env python3
"""nu_reader_v1_1 -- pk25 (code/pk25/nu/): the reader of pk24's certified NU record NU_G_RECORD_v1 (pk24/nu/NU_G_RECORD_v1.kv, producer
pk24/nu/kt_nu_g_v1_2.py; pk24/NU_G_NOTE_v1.md; the rows 4637, 4639, 4657, 4659) for
the option (b) bridge of P2 (kt_p2_v2_2) and later P3/P4's A_h bridge:
  nu_g >= ||(B_g(t) - b0_g) 1_near||_t / t for g in (psi, e1, e3) and every t in (0, 1/J_LO_CHECK], in engine A's chart and nP norm, the
  series remainder included (no truncation); the far part enters the consumer's far term at |m_g(t)| + |delta_g| (note sect. 3).
v1_1 = nu_reader_v1 (never cited) for the record's actual form: FORMAT NU_G_RECORD_v1, RECORD NU_G_RECORD, PRODUCER 'pk24 ...', no BASIS
line. The value order of N<N>_NU = nu_psi nu_e1 nu_e3 is the producer's (kt_nu_g_v1_2 docstring l.19-20 and its writer; nu_e2 sits on
N<N>_NU_E2), so the CODE line must name the producer file with the sha256 the caller pins.
load(path, sha, ts, code): checks the file's sha256 against the caller's pin; FORMAT, RECORD, STATUS CERTIFIED, RUN_VERDICT VALID, PRODUCER's
first word pk24; CODE equal to code = (path relative to code/, sha256); TRIAL_SET against ts = {N: (file name, sha256)}, the caller's
trial pins; the CLAIM's first words 'for N in {3, 4}, g in {psi, e1, e2, e3}'; J_LO_CHECK a positive decimal, T1 (when present) equal to
1/J_LO_CHECK exactly; N<N>_NU three positive decimals (exact Fractions). nu_bounds(rec, N, J_lo): the three values at N, refused unless
J_LO_CHECK <= J_lo exactly (the record covers t_hi = 1/J_lo). Every refusal raises NuError. No compute beyond parsing."""
import hashlib
import re
from fractions import Fraction

FORMAT = 'NU_G_RECORD_v1'
RECORD = 'NU_G_RECORD'
CLAIM_HEAD = 'for N in {3, 4}, g in {psi, e1, e2, e3}'
NS = (4, 3)
DEC = re.compile(r'[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?')


class NuError(Exception):
    pass


def _sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _dec(s, what):
    if not DEC.fullmatch(s):
        raise NuError('%s: %r is not a plain decimal' % (what, s))
    x = Fraction(s)
    if x <= 0:
        raise NuError('%s: %r is not positive' % (what, s))
    return x


def load(path, sha, ts, code):
    if _sha(path) != sha:
        raise NuError('the NU record does not match its pin')
    head = {}
    for ln in open(path).read().splitlines():
        if not ln.strip() or ln.startswith('#'):
            continue
        if ' = ' not in ln:
            raise NuError('a line without " = ": %r' % ln[:60])
        k, v = ln.split(' = ', 1)
        if k in head:
            raise NuError('the line %s appears twice' % k)
        head[k] = v.strip()
    for k, want in (('FORMAT', FORMAT), ('RECORD', RECORD), ('STATUS', 'CERTIFIED'), ('RUN_VERDICT', 'VALID')):
        if head.get(k) != want:
            raise NuError('%s is %r, not %r' % (k, head.get(k), want))
    if head.get('PRODUCER', '').split()[:1] != ['pk24']:
        raise NuError('PRODUCER is %r, not pk24' % head.get('PRODUCER'))
    if head.get('CODE') != '%s:%s' % code:
        raise NuError('CODE is %r, not the pinned producer %s:%s' % (head.get('CODE'), code[0], code[1][:8]))
    trial = head.get('TRIAL_SET', '')
    for N in NS:
        name, h = ts[N]
        got = re.findall(r'\bN%d ([A-Za-z0-9_.]+):([0-9a-f]{64})\b' % N, trial)
        if got != [(name, h)]:
            raise NuError('TRIAL_SET at N = %d gives %r, not %s:%s' % (N, got, name, h[:8]))
    if not head.get('CLAIM', '').startswith(CLAIM_HEAD):
        raise NuError('the CLAIM does not start with %r' % CLAIM_HEAD)
    if 'J_LO_CHECK' not in head:
        raise NuError('no J_LO_CHECK line')
    jlo = _dec(head['J_LO_CHECK'], 'J_LO_CHECK')
    if 'T1' in head:
        if not re.fullmatch(r'[0-9]+(/[0-9]+)?', head['T1']) or Fraction(head['T1']) * jlo != 1:
            raise NuError('T1 = %r is not 1/J_LO_CHECK' % head['T1'])
    rec = {'J_LO': jlo, 'SHA': sha}
    for N in NS:
        toks = head.get('N%d_NU' % N, '').split()
        if len(toks) != 3:
            raise NuError('N%d_NU has %d values, not 3' % (N, len(toks)))
        rec[N] = [_dec(x, 'N%d_NU' % N) for x in toks]
    return rec


def nu_bounds(rec, N, J_lo):
    J_lo = Fraction(J_lo)
    if not rec['J_LO'] <= J_lo:
        raise NuError('the record covers J >= %s only, not J >= %s' % (rec['J_LO'], J_lo))
    return list(rec[N])
