#!/usr/bin/env python3
"""m3_record_v5.py -- pk03 (code/pk03/). Writer of M3's records. REVISION of m3_record_v4.py (b2671d5a) for M2's vacuum records
(PLAN_M3_CODE_v1_2_ADD4 sects. 3-5; ADD5_1 sect. 9; ADD5_2 sect. 7; the schema agreed with pk02, SPEC_M2B_CERT_v1_ADD2 48d5fa54 sect. 1):
outer_far_record writes a VAC_OF_* item {kind 'outer_far', value, chart, far, lam_star, theta_star, law_claim, law {a_m, lam_star, r,
mF, J_REF}, r_parts}: chart and far are upper ends (>= 0) rounded up, value = chart + far rounded up, law.a_m the exact string 'p/q' of
Fraction(0.55)**2, mF 2, law.lam_star = lam_star, r a lower end rounded down; it raises ValueError unless lam_star >= 0.5 and
r >= 0.5 a_m exactly (C-LAW-OF; the run gates it first). Entries and top_level as v4.
m3_record_v4: Writer of M3's records.
dfdc53da sect. 4 item 5 and the M2(b) kernel fields (pk02's SPEC_M2B_CERT_v1_ADD1 sect. 4):
- top_level requires the kernel dict to hold exactly kernel_file, kernel_sha256, kernel_prec, validation, arb_kernel_file,
  arb_kernel_sha256, arb_base_file and arb_base_sha256: every sha256 64 lower-case hex digits, kernel_prec an int, and five validation
  sha256s (v1, v2, v3, v4, close) for a certified record. Extra fields may not replace a top-level field;
- entry_record raises ValueError, not an assert, when a0_exact is not a binary64 value;
- outer_far items leave this module: m3_record_v5 writes them with m3_vac_v1, in the schema agreed with pk02.
As v3: FORMAT 'M3_RECORD_v1' only for a certified TAG ''; 'M3_RECORD_v1_PRECERT' and 'M3_RECORD_v1_STUB' otherwise, with the claim
prefixed 'NOT CERTIFIED (PRECERT): ' or 'NOT CERTIFIED (STUB): '; every item carries kind 'entry'.
Entry items as v2: ak = nearest binary64 to each a_k's midpoint; ak_rad an upward radius covering the enclosure; B = {rem, tail, ann,
far} upper ends rounded up, rnd = sum_k ak_rad_k t_REF^k rounded up; Bp = B without rnd; err = sum of B rounded up; parity zeros all 0.
No compute of its own.
"""
import re
from decimal import Decimal
from fractions import Fraction
import m3_scal as S

FORMATS = {'': 'M3_RECORD_v1', '_PRECERT': 'M3_RECORD_v1_PRECERT', '_STUB': 'M3_RECORD_v1_STUB'}
PREFIX = {'': '', '_PRECERT': 'NOT CERTIFIED (PRECERT): ', '_STUB': 'NOT CERTIFIED (STUB): '}
CLAIM = 'for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err (Lemma U: PLAN_M3_CODE_v1 sect. 5, v1_2 sect. C)'
LAW_CLAIM = ('for every J >= J_REF: the outer-far integral over its graph\'s main term is at most value (J/J_REF)^2 e^(-0.5 a_m (J - J_REF)) '
             '(PLAN_M3_CODE_v1_2_ADD4 sect. 4, C-LAW-OF: lam_star >= 0.5 and r >= 0.5 a_m)')
A_M = Fraction(0.55) ** 2   # the shared region boundary a_m, exactly (agreed with pk02)
KERNEL_KEYS = ('kernel_file', 'kernel_sha256', 'kernel_prec', 'validation', 'arb_kernel_file', 'arb_kernel_sha256', 'arb_base_file',
               'arb_base_sha256')
HEX64 = re.compile('[0-9a-f]{64}')


def mid_float(x):
    return float(S.I(x).mid)


def rad_around(x, f):
    x = S.I(x)
    return max(S.up(x.b - f), S.up(f - x.a), 0.0)


def entry_record(ak_iv, bars, t_ref, parity='free', a0_exact=None, laws=None, alias_of=None):
    """one 'entry' item; bars: {rem, tail, ann, far} as intervals with valid upper ends."""
    if parity == 'zero':
        z = {'rem': 0.0, 'tail': 0.0, 'ann': 0.0, 'far': 0.0}
        return {'kind': 'entry', 'ak': [0.0] * 4, 'ak_rad': [0.0] * 4, 'B': dict(z, rnd=0.0), 'Bp': z, 'err': 0.0, 'parity': 'zero',
                'alias_of': alias_of, 'a0_exact': '0', 'laws': laws, 'value_ref': 0.0}
    ak = [mid_float(x) for x in ak_iv]
    rad = [rad_around(x, f) for x, f in zip(ak_iv, ak)]
    if a0_exact is not None:
        c = Fraction(a0_exact)
        if not (ak_iv[0].a <= S.I(c) <= ak_iv[0].b):
            raise ArithmeticError('a0_exact %s is outside the computed a_0 enclosure %r' % (a0_exact, ak_iv[0]))
        ak[0], rad[0] = float(c), 0.0
        if Fraction(ak[0]) != c:
            raise ValueError('a0_exact must be a binary64 value')
    t = S.I(t_ref)
    rnd = S.up(S.isum(S.I(r) * S.ipow(t, k) for k, r in enumerate(rad)))
    Bp = {p: S.up(S.nonneg(bars[p])) for p in ('rem', 'tail', 'ann', 'far')}
    B = dict(Bp, rnd=rnd)
    err = S.up(S.isum(S.I(v) for v in B.values()))
    vref = S.isum(S.I(a) * S.ipow(t, k) for k, a in enumerate(ak))
    return {'kind': 'entry', 'ak': ak, 'ak_rad': rad, 'B': B, 'Bp': Bp, 'err': err, 'parity': 'free', 'alias_of': alias_of,
            'a0_exact': None if a0_exact is None else str(Fraction(a0_exact)), 'laws': laws, 'value_ref': mid_float(vref)}


def outer_far_record(chart, far, lam_star, theta_star, r, j_ref, r_parts=None):
    """one VAC_OF_* item (ADD4 sects. 3-5): chart, far and r intervals; lam_star, theta_star binary64; j_ref an int."""
    ch, fa = S.up(S.nonneg(chart)), S.up(S.nonneg(far))
    rl = S.down(r)
    if Fraction(lam_star) < Fraction(1, 2) or Fraction(rl) < Fraction(1, 2) * A_M:
        raise ValueError('C-LAW-OF: lam_star %r and r %r must satisfy lam_star >= 0.5 and r >= 0.5 a_m' % (lam_star, rl))
    return {'kind': 'outer_far', 'value': S.up(S.isum([S.I(ch), S.I(fa)])), 'chart': ch, 'far': fa, 'lam_star': lam_star,
            'theta_star': theta_star, 'law_claim': LAW_CLAIM,
            'law': {'a_m': str(A_M), 'lam_star': lam_star, 'r': rl, 'mF': 2, 'J_REF': j_ref}, 'r_parts': r_parts}


def kbar_exact(kbar):
    """the exact decimal expansion of a binary64 value (pk07's condition (a))."""
    return format(Decimal(kbar), 'f')


def top_level(N, J_ref, families, trial_set, engine, tag, kernel, extra=None):
    """kernel: exactly KERNEL_KEYS (full sha256s; validation the list of validation-record sha256s, five for a certified TAG '')."""
    if tag not in FORMATS:
        raise ValueError('tag %r' % (tag,))
    if set(kernel) != set(KERNEL_KEYS):
        raise ValueError('kernel fields %s, expected exactly %s' % (sorted(kernel), list(KERNEL_KEYS)))
    shas = [kernel['kernel_sha256'], kernel['arb_kernel_sha256'], kernel['arb_base_sha256']] + list(kernel['validation'])
    if not all(isinstance(h, str) and HEX64.fullmatch(h) for h in shas):
        raise ValueError('kernel fields: every sha256 must be 64 lower-case hex digits')
    if isinstance(kernel['kernel_prec'], bool) or not isinstance(kernel['kernel_prec'], int):
        raise ValueError('kernel_prec must be an int, not %r' % (kernel['kernel_prec'],))
    if tag == '' and len(kernel['validation']) != 5:
        raise ValueError('a certified record names five validation records (v1, v2, v3, v4, close)')
    out = {'format': FORMATS[tag], 'N': N, 'J_REF': J_ref, 's_rad': 80.0, 'rho_p': 0.7, 'families': families, 'trial_set': trial_set,
           'engine': engine, 'claim': PREFIX[tag] + CLAIM}
    out.update(kernel)
    if extra:
        if set(extra) & set(out):
            raise ValueError('extra fields %s would replace top-level fields' % sorted(set(extra) & set(out)))
        out.update(extra)
    return out
