#!/usr/bin/env python3
"""m3_reader_v6_3.py -- pk03 (code/pk03/). REVISION of m3_reader_v6_2.py (854b6a87) for the D16 H and S4 records of route (b)
(m3_run_v1_9, the approval 2026-11-08; pk11 01:14Z: the consumer reads them through this reader, one certified M3 path):
- a certified record's kernel fields (kernel_file, kernel_sha256, kernel_prec, validation) must equal one of VALIDATED_LAYERS
  exactly: v6_2's arbeng_ma_v1_3 (075e3586, its five validation records) or pk02's arbeng_ma_v1_4_1 (4126e83e; its five: the
  bundle manifest 368d6f1d, the kt_ma_val_v1_6 run manifest 6e951721, the delta validation output af1e3f66
  86a1abf9 and 01d03cea). A record naming one layer with another's validation list, or any other layer, is refused;
- the ball-form claim: a certified record on
  arbeng_ma_v1_4_1, and any certified record that carries the field, must have claim_ball equal to CLAIM_BALL exactly; it states
  the box entry_ball returns (the a_k balls and the bar without rnd), which Lemma U certifies (PLAN_M3_CODE_v1 l.125, v1_2 U4).
Everything else is v6_2's.
m3_reader_v6_2's docstring follows.
m3_reader_v6_2.py -- pk03 (code/pk03/). REVISION of m3_reader_v6_1.py (28b1b0b6) for the N record on route B's scope (
option 3): the producer allow-list gains m3_lawcert_v1_2 (da6e286d), which certifies exactly the one record m3_s8v3_N_N<N>_J300_v1_8_2.json
(family N; m3_run_v1_8_2's asmN). Everything else is m3_reader_v6_1's: the first-line producer pin, FORMAT, one VERDICT VALID line, the
RECORD sha and the exact record set of each producer. Its docstring follows.
m3_reader_v6_1: REVISION of m3_reader_v6.py (5e25df73) for the producer pin of law certificates
(the check 395b3cda, item (d); the 21:59Z: nothing S8 consumes reads laws through v6):
- load_lawcert and loads_lawcert also require the writing job's first line to be exactly
  '<producer> N <N> LIM <lim>; script sha256 <sha256>; python <version>' with <producer> on the allow-list PRODUCERS, <sha256> its
  full sha256 there and <N> the consumer's expected N. A look-alike job (another script, another sha, another N) is refused, as
  before is any VERDICT other than exactly one 'VERDICT VALID' line (PRECERT, INFO, two lines) and any RECORD line that is not the
  certificate's sha256.
- The producer fixes what the certificate may bind (PRODUCER_RECORDS): m3_lawcert_v1 the five m3_run_v1_8 records
  (m3_s8v3_<F>_N<N>_J300_v1_8.json, F in D, N, E2, E3, FF); m3_lawcert_v1_1 the four partial-asm records
  (m3_s8v3_<F>_N<N>_J300_v1_8_1.json, F in D, E2, E3, FF). The consumer passes every record of that set as {family: record from
  load}; the records map must equal them exactly (as v6). The certificate's 'asm' field is only shape-checked: the records'
  own binding to their asm output is load's.
- The checked certificate carries its producer ('producer'). Everything else is m3_reader_v6's. Its docstring follows.
m3_reader_v6: REVISION of m3_reader_v5.py (57d17d7b) for the certified J-laws of M3's records
(PLAN_M3_LAWCERT_v1 255a9d70 sect. 5; the pre-check of 20:38Z, item 2):
- every free entry's 'laws' is parsed and checked: exactly rem_tpow, tail, ann, far_rate and far_cF; rem_tpow the int 4; tail and ann
  exactly {n, J_REF, a_G} with n the int N - 1 (2 or 3), J_REF the consumer's expected J_REF and a_G a non-empty list of pairs [a, G]
  of finite binary64 values > 0; far_rate a finite value > 0 (C-MONO-FAR); far_cF the exact string of a rational > 0. A parity
  zero carries laws None. load keeps each entry's checked law, its parts and ak_rad (exact rationals), and the record's base name and
  sha256, for the binding below;
- load_lawcert(path, out_path, expected_J_REF, expected_N, recs) reads an M3_LAWCERT_v1 certificate (m3_lawcert_v1). out_path is the
  output of the job that wrote it: VERDICT lines exactly ['VERDICT VALID'] and exactly one 'RECORD <file name> <sha256>' line for it,
  the binding records have. recs = {family: record from load} are the records the consumer loaded; the certificate's records map must
  equal their (base name, sha256) exactly, no family more or fewer; its entries must be exactly the records' entries ('family:key'),
  with the same parity; every free entry needs law_claim = LAWCERT_CLAIM and laws equal to its record's laws exactly, every number
  written as the canonical exact string of the record's binary64 value. loads_lawcert does the same in memory (the producer's
  C-LAWCERT-RT and plants);
- entry_law(cert, family, key) returns the checked law with the entry's parts, ak, ak_rad and err as exact rationals. A consumer
  evaluates LAWCERT_CLAIM's right side with its own outward rounding (Prob(chi^2_2 > s) = e^(-s/2); Prob(chi^2_3 > s) =
  erfc(sqrt(s/2)) + sqrt(2s/pi) e^(-s/2); numerator rounded up, denominator down). Every term is non-increasing in J, so its value at a
  piece's J_lo bounds the piece; the minimum of it and the record's err is valid. Use either the midpoints ak with the term
  sum_k ak_rad[k] t^k (LAWCERT_CLAIM's form), or entry_ball's ak -+ ak_rad with the four parts and no ak_rad term, never both.
This reader computes nothing transcendental. Everything else is m3_reader_v5's.
m3_reader_v5: REVISION of m3_reader_v4_4.py (a5ba5c80) for M2's vacuum records (PLAN_M3_CODE_v1_2_ADD4;
ADD5_1 sect. 9; ADD5_2 sect. 7; the schema agreed with pk02, SPEC_M2B_CERT_v1_ADD2 48d5fa54 sect. 1):
- a key starting 'VAC_OF_' must have kind 'outer_far', and every other key kind 'entry'. An outer_far item has exactly the fields kind,
  value, chart, far, lam_star, theta_star, law_claim, law and r_parts; chart >= 0, far >= 0 and value >= chart + far exactly;
  law_claim is the certified text; law is exactly {a_m, lam_star, r, mF, J_REF}, with a_m the exact string 'p/q' equal to
  Fraction(0.55)**2, mF 2, J_REF the consumer's expected J_REF, lam_star equal to the item's lam_star and >= 0.5, and
  Fraction(r) >= Fraction(1, 2) Fraction(a_m) exactly (pk02's two additions);
- outer_far(rec, key) returns the checked item;
- check_text becomes _check_text: the writer's C-FMT before the write, never a consumer entry point.
Everything else is m3_reader_v4_4's: load(path, asm_out, expected_J_REF, expected_N) is the only certified entry point.
m3_reader_v4_4: REVISION of m3_reader_v4_3.py (adf51038, never run or cited) for the review
ad0ceca7 of m3_run_v1_5_1 (and its ADD1 18a634fa): the bound loader is the only certified entry point.
- load(path, asm_out, expected_J_REF, expected_N): asm_out is the output of the asm run that wrote the record. Its VERDICT lines must
  be exactly ['VERDICT VALID'], and it must name the file with the sha256 of its bytes on exactly one 'RECORD <file name> <sha256>'
  line; then every check of the certified parse. loads(text, out_text, expected_J_REF, expected_N, name) does the same in memory.
- load_noncert and loads_noncert read PRECERT and STUB records, as before.
m3_reader_v4_3 .. m3_reader_v4: the allow-listed FORMAT and claim, expected_N beside expected_J_REF, the validated layer (kernel_file,
kernel_sha256, kernel_prec 512, validation list), the pinned arb recompute engine and arb base, kind 'entry' for every non-outer_far
item; entry items (ak, ak_rad, B, Bp, err, parity) with rnd >= sum_k ak_rad_k Fraction(1, J_REF)^k exactly; entry_ball(rec, key)
returns (LO list, HI list, err_b). The independent reader of M3's records (PLAN_M3_CODE_v1 sect. 4), sha-pinned by every consumer for
its C-FMT; it shares no code with the writers. No compute of its own.
"""
import hashlib
import json
import os
import math
from decimal import Decimal
from fractions import Fraction
import re

PARTS = ('rem', 'tail', 'ann', 'far', 'rnd')
CERT_FORMAT = 'M3_RECORD_v1'
NONCERT = {'M3_RECORD_v1_PRECERT': 'NOT CERTIFIED (PRECERT): ', 'M3_RECORD_v1_STUB': 'NOT CERTIFIED (STUB): '}
CERT_CLAIM = 'for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err (Lemma U: PLAN_M3_CODE_v1 sect. 5, v1_2 sect. C)'
CLAIM_BALL = ('for every J >= J_REF, t = 1/J, t = 0 included: I(J)/main(J) lies in sum_k [ak_k - ak_rad_k, ak_k + ak_rad_k] t^k + '   # m3_reader_v6_3
              '[-sum Bp, sum Bp] (Lemma U: PLAN_M3_CODE_v1 l.125, v1_2 U4)')
KERNEL_PREC = 512   # the layer runs at ctx.prec 512
VALIDATED_LAYER = ('arbeng_ma_v1_3.py', '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be',   # 
                   ('5ccbb6d006f5365f219eb6221b7e66b76e7e7799e977148df94f34b0c3d86216',   # kt_ma_val_v1_5 v1
                    'a61d893e6424b9ea524d944e40f625c934de04a2faeaa741e3fd333e97f48817',   # v2
                    'd613fe804a030be397fefa46ed1424063f794400b7d9618e12db8af046e09d93',   # v3
                    '2ad13ec3cac14ef919f5e34fa19664f70eece05c3c3f208dcfec36a93cdd4473',   # v4
                    'a8a5e8d020d2d1e1127c3ee8f400496011ddbd022af83180025ac3185ba22f95'))  # CLOSE_ARBENG_MA_V1_3_rv01.md
VALIDATED_LAYER_V141 = ('arbeng_ma_v1_4_1.py', '1f58ad80ceb1c0992f08f894c0f6af26ef18d397627020a5a5fe7130818375d9',   # m3_reader_v6_3
                        ('c172e15f42cad0278bdea3343ddea084327dbf89a4eef2561df7e5d23140f5fc',   # MANIFEST_ARBENG_MA_v1_4_1.sha256
                         '7ec00dc5d98d64c06e345d80b4a0959e7ec6805239a4d03ba7be006882186314',   # MANIFEST_KT_MA_VAL_v1_6_RUN.sha256
                         'af1e3f66a88c27b0593b31e23f936986ecd04c813854ed4001cc601f7a6bef12',   # out_kt_ma_val_v1_6_1_d.out
                         '8afbb958904ab2067d75b6876b2b6496dda7286ba99d4d00428e3cd7a4485335',   # REVIEW_CODE_ARBENG_MA_V1_4_rv01.md
                         '3fd1bfa7dc00d4600aa3ff1d413807cb75e9ab9d910600d580ab48bd6b36fc4f'))  # DELTA_ARBENG_MA_V1_4_1_rv01.md
VALIDATED_LAYERS = (VALIDATED_LAYER, VALIDATED_LAYER_V141)   # m3_reader_v6_3: a certified record names one of these exactly
ARB_KERNEL = ('arbeng_ma_stub_v1_1.py', '794fabc7111555db2f6390a144d3f5af6deeb358d02da8b5705cf3ceaefd0af1')   # the arb recompute engine of MAFallback (close condition (ii))
ARB_BASE = ('arbeng_c2b_v2.py', '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0')   # the arb base under ARB_KERNEL
LAW_CLAIM = ('for every J >= J_REF: the outer-far integral over its graph\'s main term is at most value (J/J_REF)^2 e^(-0.5 a_m (J - J_REF)) '
             '(PLAN_M3_CODE_v1_2_ADD4 sect. 4, C-LAW-OF: lam_star >= 0.5 and r >= 0.5 a_m)')
A_M = Fraction(0.55) ** 2   # the shared region boundary a_m, exactly (agreed with pk02)
OF_KEYS = {'kind', 'value', 'chart', 'far', 'lam_star', 'theta_star', 'law_claim', 'law', 'r_parts'}; import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_LAYERS = [('arbeng_ma_v1_3.py', '075e35864a272e29014d2259e0bfc37eaf7a1d0b5a9a101ae78ee9d4ed8f6a15', KERNEL_PREC, tuple(VALIDATED_LAYER[2])), ('arbeng_ma_v1_4_1.py', '4126e83eae5785c4b9f6e816091f4a592896456d87169429598deae62448f3e7', KERNEL_PREC, tuple(VALIDATED_LAYER_V141[2]))]; ORIG_ARB = ('arbeng_ma_stub_v1_1.py', '4fc7e49d72e589055f79249d435ae3abb827db0a769b80397fa09c6170190ce7'); ORIG_BASE = ('arbeng_c2b_v2.py', 'fb8cd1b5162930b1e9ff83c35fb652575a9f2ff1649f733c5d45bdf7f7762993')  # G-ORIG: option (C), acc2 two-producer acceptance
LAW_KEYS = {'a_m', 'lam_star', 'r', 'mF', 'J_REF'}
LAWS_KEYS = {'rem_tpow', 'tail', 'ann', 'far_rate', 'far_cF'}
LAWG_KEYS = {'n', 'J_REF', 'a_G'}
LAWCERT_FORMAT = 'M3_LAWCERT_v1'
LAWCERT_CLAIM = ('for every J >= J_REF, t = 1/J: |I(J)/main(J) - sum_k ak[k] t^k| <= rem (J_REF/J)^4 + tail (P(J; tail)/P(J_REF; tail))^(1/2) '
                 '+ ann (P(J; ann)/P(J_REF; ann))^(1/2) + far exp(-far_rate (J - J_REF)) + sum_k ak_rad[k] t^k, where rem, tail, ann, far are '
                 'the entry\'s B parts, P(J; x) = sum over the pairs [a, G] of laws.x.a_G of Prob(chi^2_n > J a / G) with n = laws.x.n, and '
                 'far_rate = laws.far_rate (Lemma U, U3: PLAN_M3_CODE_v1_2 sect. C; PLAN_M3_LAWCERT_v1 sect. 3)')
LAWCERT_KEYS = {'format', 'claim', 'J_REF', 'N', 'records', 'asm', 'entries'}
PRODUCERS = {'m3_lawcert_v1.py': '316124742fad4dd1976a90d38187c6ebf1f1d527875389c1a3662da5eee4ec87',     # 
             'm3_lawcert_v1_1.py': '981f0c12166561f74eb90ddea636c0f2a614bbd46f29d845f083a0a5b17b8920',   # the partial asm's records
             'm3_lawcert_v1_2.py': '79ff6ca2e350cf8b033427633b29e907a64e8d7b04599b5b44299afde3d6d63a'}   # the N record on route B's scope
PRODUCER_RECORDS = {'m3_lawcert_v1.py': ('_J300_v1_8.json', ('D', 'N', 'E2', 'E3', 'FF')),
                    'm3_lawcert_v1_1.py': ('_J300_v1_8_1.json', ('D', 'E2', 'E3', 'FF')),
                    'm3_lawcert_v1_2.py': ('_J300_v1_8_2.json', ('N',))}
PRODUCER_RE = re.compile(r'(m3_lawcert_v1|m3_lawcert_v1_1|m3_lawcert_v1_2) N ([0-9]+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)')
CERT_ENTRY_KEYS = {'parity', 'law_claim', 'laws'}
HEX64 = re.compile('[0-9a-f]{64}')
RAT = re.compile('-?[0-9]+(/[0-9]+)?')


def _num(x, what):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(float(x)):
        raise ValueError('%s: not a finite number: %r' % (what, x))
    return float(x)


def _int(x, what):
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError('%s must be an int, not %r' % (what, x))
    return x


def _laws(key, laws, j_ref, n_want):
    """a free entry's 'laws', checked and returned with exact rationals."""
    if not isinstance(laws, dict) or set(laws) != LAWS_KEYS:
        raise ValueError('%s: laws must hold exactly %s' % (key, sorted(LAWS_KEYS)))
    if _int(laws['rem_tpow'], key + ' laws.rem_tpow') != 4:
        raise ValueError('%s: laws.rem_tpow %r, expected 4' % (key, laws['rem_tpow']))
    out = {'rem_tpow': 4}
    for part in ('tail', 'ann'):
        g = laws[part]
        if not isinstance(g, dict) or set(g) != LAWG_KEYS:
            raise ValueError('%s: laws.%s must hold exactly %s' % (key, part, sorted(LAWG_KEYS)))
        if _int(g['n'], key + ' laws.%s.n' % part) != n_want:
            raise ValueError('%s: laws.%s.n %r, expected N - 1 = %r' % (key, part, g['n'], n_want))
        if _int(g['J_REF'], key + ' laws.%s.J_REF' % part) != j_ref:
            raise ValueError('%s: laws.%s.J_REF %r, expected %r' % (key, part, g['J_REF'], j_ref))
        ag = g['a_G']
        if not isinstance(ag, list) or not ag or any(not isinstance(p, list) or len(p) != 2 for p in ag):
            raise ValueError('%s: laws.%s.a_G must be a non-empty list of pairs [a, G]' % (key, part))
        pairs = [(Fraction(_num(a, key + ' a')), Fraction(_num(G, key + ' G'))) for a, G in ag]
        if any(a <= 0 or G <= 0 for a, G in pairs):
            raise ValueError('%s: laws.%s.a_G has an entry <= 0' % (key, part))
        out[part] = {'n': n_want, 'J_REF': j_ref, 'a_G': pairs}
    rate = Fraction(_num(laws['far_rate'], key + ' laws.far_rate'))
    if rate <= 0:
        raise ValueError('%s: laws.far_rate %r is not > 0 (C-MONO-FAR)' % (key, laws['far_rate']))
    cf = laws['far_cF']
    if not isinstance(cf, str) or not RAT.fullmatch(cf) or str(Fraction(cf)) != cf or Fraction(cf) <= 0:
        raise ValueError('%s: laws.far_cF %r is not the exact string of a rational > 0' % (key, cf))
    out['far_rate'] = rate
    out['far_cF'] = Fraction(cf)
    return out


def _entry(key, d, j_ref, n_want):
    ak = d.get('ak')
    if not isinstance(ak, list) or len(ak) != 4:
        raise ValueError('%s: ak must be a list of 4 numbers' % key)
    ak = [_num(a, key + ' ak') for a in ak]
    B = d.get('B')
    if not isinstance(B, dict) or set(B) != set(PARTS):
        raise ValueError('%s: B must hold exactly %s' % (key, PARTS))
    Bv = {p: _num(B[p], key + ' B.' + p) for p in PARTS}
    if any(v < 0 for v in Bv.values()):
        raise ValueError('%s: a negative bar part' % key)
    err = _num(d.get('err'), key + ' err')
    if Fraction(err) < sum(Fraction(v) for v in Bv.values()):
        raise ValueError('%s: err below the sum of its bar parts' % key)
    Bp = d.get('Bp')
    if not isinstance(Bp, dict) or set(Bp) != set(PARTS[:4]) or any(_num(Bp[p], key) != Bv[p] for p in PARTS[:4]):
        raise ValueError('%s: Bp must equal B without rnd' % key)
    if d.get('parity') == 'zero':
        if any(a != 0.0 for a in ak) or any(v != 0.0 for v in Bv.values()) or err != 0.0:
            raise ValueError('%s: a parity zero must be exactly zero' % key)
        if d.get('laws') is not None:
            raise ValueError('%s: a parity zero carries laws None' % key)
        laws = None
    elif d.get('parity') == 'free':
        laws = _laws(key, d.get('laws'), j_ref, n_want)
    else:
        raise ValueError('%s: parity must be zero or free' % key)
    rad = d.get('ak_rad')
    if not isinstance(rad, list) or len(rad) != 4:
        raise ValueError('%s: ak_rad must be a list of 4 numbers' % key)
    rad = [_num(r, key + ' ak_rad') for r in rad]
    if any(r < 0 for r in rad) or (d.get('parity') == 'zero' and any(r != 0.0 for r in rad)):
        raise ValueError('%s: ak_rad must be >= 0, and 0 for a parity zero' % key)
    if d.get('parity') == 'free' and Fraction(Bv['rnd']) < sum(Fraction(r) * Fraction(1, j_ref) ** k for k, r in enumerate(rad)):
        raise ValueError('%s: rnd below sum_k ak_rad_k (1/J_REF)^k' % key)
    return ak, err, rad, laws, Bv, d.get('parity')


def _outer_far(key, d, j_ref):
    """an 'outer_far' item (ADD4 sects. 3-5; ADD5_1 sect. 9; the schema agreed with pk02, SPEC_M2B_CERT_v1_ADD2 sect. 1)."""
    if set(d) != OF_KEYS:
        raise ValueError('%s: outer_far fields %s, expected exactly %s' % (key, sorted(d), sorted(OF_KEYS)))
    value, chart, far = (_num(d[x], key + ' ' + x) for x in ('value', 'chart', 'far'))
    if chart < 0 or far < 0:
        raise ValueError('%s: chart and far must both be >= 0' % key)
    if Fraction(value) < Fraction(chart) + Fraction(far):
        raise ValueError('%s: value below chart + far' % key)
    lam = _num(d['lam_star'], key + ' lam_star')
    _num(d['theta_star'], key + ' theta_star')
    if d['law_claim'] != LAW_CLAIM:
        raise ValueError('%s: the law claim is not the certified text' % key)
    law = d['law']
    if not isinstance(law, dict) or set(law) != LAW_KEYS:
        raise ValueError('%s: the law fields must be exactly %s' % (key, sorted(LAW_KEYS)))
    am = law['a_m']
    if not isinstance(am, str) or not re.fullmatch('[0-9]+/[0-9]+', am) or Fraction(am) != A_M:
        raise ValueError('%s: law.a_m must be the exact string of Fraction(0.55)**2' % key)
    for x in ('mF', 'J_REF'):
        if isinstance(law[x], bool) or not isinstance(law[x], int):
            raise ValueError('%s: law.%s must be an int' % (key, x))
    if law['mF'] != 2 or law['J_REF'] != j_ref:
        raise ValueError('%s: law.mF %r (expected 2) or law.J_REF %r (expected %r)' % (key, law['mF'], law['J_REF'], j_ref))
    if _num(law['lam_star'], key + ' law.lam_star') != lam or Fraction(lam) < Fraction(1, 2):
        raise ValueError('%s: lam_star must equal law.lam_star and be >= 0.5' % key)
    r = Fraction(_num(law['r'], key + ' law.r'))
    if r < Fraction(1, 2) * A_M:
        raise ValueError('%s: law.r is below 0.5 a_m (exact comparison)' % key)
    return {'value': value, 'chart': chart, 'far': far, 'lam_star': lam, 'r': r, 'a_m': A_M}


def _items(rec, path, j_ref, n_want):
    items = dict(rec.get('items', {}))
    if 'I_N' in rec:
        items['I_N'] = rec['I_N']
    if not items:
        raise ValueError('%s: no items' % path)
    ents, ofs = {}, {}
    for k, d in items.items():
        kind = d.get('kind') if isinstance(d, dict) else None
        if k.startswith('VAC_OF_'):
            if kind != 'outer_far':
                raise ValueError('%s: item %s is an outer_far key with kind %r' % (path, k, kind))
            ofs[k] = _outer_far(k, d, j_ref)
            continue
        if kind != 'entry':
            raise ValueError('%s: item %s has kind %r, expected entry' % (path, k, kind))
        ents[k] = _entry(k, d, j_ref, n_want)
    return items, ents, ofs


def _expect(v, what):
    if isinstance(v, bool) or not isinstance(v, int) or v <= 0:
        raise ValueError('the consumer must pass expected %s as a positive int, not %r' % (what, v))
    return v


def _parse(rec, path, expected_J_REF, expected_N, certified):
    if rec.get('J_REF') != _expect(expected_J_REF, 'J_REF'):
        raise ValueError('%s: J_REF %r, expected %r' % (path, rec.get('J_REF'), expected_J_REF))
    if rec.get('N') != _expect(expected_N, 'N'):
        raise ValueError('%s: N %r, expected %r' % (path, rec.get('N'), expected_N))
    fmt, claim = rec.get('format'), rec.get('claim')
    if not isinstance(claim, str):
        raise ValueError('%s: the claim is missing' % path)
    if certified:
        if fmt != CERT_FORMAT or claim != CERT_CLAIM:
            raise ValueError('%s: not a certified M3 record (format %r; the claim must be the certified text exactly)' % (path, fmt))
        if (rec.get('kernel_file'), rec.get('kernel_sha256'), rec.get('kernel_prec'), tuple(rec.get('validation') or ())) not in [   # v6_3
                (L_[0], L_[1], KERNEL_PREC, tuple(L_[2])) for L_ in VALIDATED_LAYERS]:
            ACC.fail_unless(ACC.carried(path) and (rec.get('kernel_file'), rec.get('kernel_sha256'), rec.get('kernel_prec'), tuple(rec.get('validation') or ())) in ORIG_LAYERS, ValueError('%s: kernel %r (prec %r) is not a validated layer this reader pins' % (path, rec.get('kernel_file'), rec.get('kernel_prec'))))
        if (rec.get('arb_kernel_file'), rec.get('arb_kernel_sha256')) != ARB_KERNEL:
            ACC.fail_unless(ACC.carried(path) and (rec.get('arb_kernel_file'), rec.get('arb_kernel_sha256')) == ORIG_ARB, ValueError('%s: arb kernel %r is not the arb recompute engine this reader pins' % (path, rec.get('arb_kernel_file'))))
        if (rec.get('arb_base_file'), rec.get('arb_base_sha256')) != ARB_BASE:
            ACC.fail_unless(ACC.carried(path) and (rec.get('arb_base_file'), rec.get('arb_base_sha256')) == ORIG_BASE, ValueError('%s: arb base %r is not the one this reader pins' % (path, rec.get('arb_base_file'))))
        if (rec.get('kernel_file') == VALIDATED_LAYER_V141[0] or 'claim_ball' in rec) and rec.get('claim_ball') != CLAIM_BALL:   # v6_3
            raise ValueError('%s: claim_ball must be the ball-form claim text exactly (required on arbeng_ma_v1_4_1)' % path)
    elif fmt not in NONCERT or claim != NONCERT[fmt] + CERT_CLAIM:
        raise ValueError('%s: not a PRECERT or STUB record with its claim prefix (format %r)' % (path, fmt))
    items, ents, ofs = _items(rec, path, expected_J_REF, expected_N - 1)
    balls = {k: ([Fraction(a) - Fraction(r) for a, r in zip(v[0], v[2])], [Fraction(a) + Fraction(r) for a, r in zip(v[0], v[2])],
                 sum(Fraction(x) for x in items[k]['Bp'].values())) for k, v in ents.items()}
    laws = {k: {'parity': v[5], 'laws': v[3], 'parts': {p: Fraction(x) for p, x in v[4].items()}, 'ak': [Fraction(a) for a in v[0]],
                'ak_rad': [Fraction(r) for r in v[2]], 'err': Fraction(v[1]), 'J_REF': expected_J_REF} for k, v in ents.items()}
    return {'top': {k: v for k, v in rec.items() if k not in ('items', 'I_N')}, 'entries': {k: (v[0], v[1]) for k, v in ents.items()},
            'balls': balls, 'outer_far': ofs, 'laws': laws}


def _check_text(text, expected_J_REF, expected_N, name='<text>'):
    """the writer's C-FMT and plants on a record text before any file is written. It does not bind the text to a run output, so it
    is not an entry point for consumers: they call load."""
    return _parse(json.loads(text), name, expected_J_REF, expected_N, True)


def _bound(name, data, out_text):
    """the review dfdc53da sect. 1 (B): the writing job's output must have VERDICT lines exactly ['VERDICT VALID'] and name this file (its
    base name) with the sha256 of its bytes on exactly one RECORD line."""
    lines = out_text.split('\n')
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise ValueError("%s: the writing job's VERDICT lines are not exactly ['VERDICT VALID']" % name)
    hit = [ln.split() for ln in lines if ln.startswith('RECORD ') and len(ln.split()) == 3 and ln.split()[1] == name]
    if len(hit) != 1 or hit[0][2] != hashlib.sha256(data).hexdigest():
        raise ValueError('%s: the writing job does not name this file with its sha256 on exactly one RECORD line' % name)


def load(path, asm_out, expected_J_REF, expected_N):
    """the only certified entry point for a record file; asm_out is the output of the asm run that wrote it."""
    with open(path, 'rb') as fh:
        data = fh.read()
    with open(asm_out) as fh:
        out_text = fh.read()
    _bound(os.path.basename(path), data, out_text)
    rec = _parse(json.loads(data.decode()), path, expected_J_REF, expected_N, True)
    rec['name'], rec['sha256'] = os.path.basename(path), hashlib.sha256(data).hexdigest()
    return rec


def loads(text, out_text, expected_J_REF, expected_N, name):
    """load in memory: text is the record file's content, out_text its asm output's, name the record file's base name."""
    _bound(name, text.encode(), out_text)
    rec = _parse(json.loads(text), name, expected_J_REF, expected_N, True)
    rec['name'], rec['sha256'] = name, hashlib.sha256(text.encode()).hexdigest()
    return rec


def loads_noncert(text, expected_J_REF, expected_N, name='<text>'):
    return _parse(json.loads(text), name, expected_J_REF, expected_N, False)


def load_noncert(path, expected_J_REF, expected_N):
    with open(path) as fh:
        return _parse(json.load(fh), path, expected_J_REF, expected_N, False)


def entry(rec, key):
    return rec['entries'][key]


def entry_ball(rec, key):
    """(LO list, HI list, err_b): exact rational ends ak -+ ak_rad of a_0..a_3 and err_b = the exact sum of Bp (the bar without rnd);
    for t in [0, 1/J_REF] the integral lies in sum_k [LO_k, HI_k] t^k + [-err_b, err_b] (and in sum_k ak_k t^k + [-err, err])."""
    return rec['balls'][key]


def outer_far(rec, key):
    """the checked 'outer_far' item: value, chart, far, lam_star, r (a Fraction) and a_m (a Fraction)."""
    return rec['outer_far'][key]


def _exact(s, what):
    """a certificate number: the canonical exact string of a rational."""
    if not isinstance(s, str) or not RAT.fullmatch(s) or str(Fraction(s)) != s:
        raise ValueError('%s: %r is not the canonical exact string of a rational' % (what, s))
    return Fraction(s)


def _cert_laws(eid, laws, j_ref, n_want):
    """a certificate entry's laws: the record's form with every number an exact string (rem_tpow, n, J_REF stay ints)."""
    if not isinstance(laws, dict) or set(laws) != LAWS_KEYS:
        raise ValueError('%s: certificate laws must hold exactly %s' % (eid, sorted(LAWS_KEYS)))
    if _int(laws['rem_tpow'], eid + ' rem_tpow') != 4:
        raise ValueError('%s: certificate rem_tpow %r, expected 4' % (eid, laws['rem_tpow']))
    out = {'rem_tpow': 4}
    for part in ('tail', 'ann'):
        g = laws[part]
        if not isinstance(g, dict) or set(g) != LAWG_KEYS:
            raise ValueError('%s: certificate %s must hold exactly %s' % (eid, part, sorted(LAWG_KEYS)))
        if _int(g['n'], eid + ' n') != n_want or _int(g['J_REF'], eid + ' J_REF') != j_ref:
            raise ValueError('%s: certificate %s n %r / J_REF %r, expected %r / %r' % (eid, part, g['n'], g['J_REF'], n_want, j_ref))
        ag = g['a_G']
        if not isinstance(ag, list) or not ag or any(not isinstance(p, list) or len(p) != 2 for p in ag):
            raise ValueError('%s: certificate %s.a_G must be a non-empty list of pairs' % (eid, part))
        pairs = [(_exact(a, eid + ' a'), _exact(G, eid + ' G')) for a, G in ag]
        if any(a <= 0 or G <= 0 for a, G in pairs):
            raise ValueError('%s: certificate %s.a_G has an entry <= 0' % (eid, part))
        out[part] = {'n': n_want, 'J_REF': j_ref, 'a_G': pairs}
    out['far_rate'] = _exact(laws['far_rate'], eid + ' far_rate')
    if out['far_rate'] <= 0:
        raise ValueError('%s: certificate far_rate is not > 0 (C-MONO-FAR)' % eid)
    out['far_cF'] = _exact(laws['far_cF'], eid + ' far_cF')
    if out['far_cF'] <= 0:
        raise ValueError('%s: certificate far_cF is not > 0' % eid)
    return out


def _parse_lawcert(cert, name, expected_J_REF, expected_N, recs):
    if not isinstance(cert, dict) or set(cert) != LAWCERT_KEYS:
        raise ValueError('%s: a law certificate holds exactly %s' % (name, sorted(LAWCERT_KEYS)))
    if cert['format'] != LAWCERT_FORMAT or cert['claim'] != LAWCERT_CLAIM:
        raise ValueError('%s: not an M3_LAWCERT_v1 certificate with the certified claim text' % name)
    if cert['J_REF'] != _expect(expected_J_REF, 'J_REF') or cert['N'] != _expect(expected_N, 'N'):
        raise ValueError('%s: J_REF %r / N %r, expected %r / %r' % (name, cert['J_REF'], cert['N'], expected_J_REF, expected_N))
    if not isinstance(recs, dict) or not recs:
        raise ValueError('the consumer must pass the loaded records as {family: record}')
    for f, r in recs.items():
        if not isinstance(r, dict) or 'sha256' not in r or r['top'].get('graph') != f:
            raise ValueError('%s: the record passed as family %r is not a loaded record of graph %r' % (name, f, f))
    want = {f: {'file': r['name'], 'sha256': r['sha256']} for f, r in recs.items()}
    got = cert['records']
    if not isinstance(got, dict) or got != want:
        raise ValueError('%s: the records map %r is not exactly the loaded records %r' % (name, got, want))
    a = cert['asm']
    if not isinstance(a, dict) or set(a) != {'file', 'sha256'} or not isinstance(a['sha256'], str) or not HEX64.fullmatch(a['sha256']):
        raise ValueError('%s: asm must be {file, sha256} with a full sha256' % name)
    ents = cert['entries']
    keys_want = {'%s:%s' % (f, k) for f, r in recs.items() for k in r['laws']}
    if not isinstance(ents, dict) or set(ents) != keys_want:
        raise ValueError('%s: the entries are not exactly the loaded records\' entries (%d against %d)' % (
            name, len(ents) if isinstance(ents, dict) else -1, len(keys_want)))
    out = {}
    for eid, d in ents.items():
        f, k = eid.split(':', 1)
        rl = recs[f]['laws'][k]
        if not isinstance(d, dict) or set(d) != CERT_ENTRY_KEYS or d['parity'] != rl['parity']:
            raise ValueError('%s: entry %s must hold exactly %s with the record\'s parity' % (name, eid, sorted(CERT_ENTRY_KEYS)))
        if rl['parity'] == 'zero':
            if d['law_claim'] is not None or d['laws'] is not None:
                raise ValueError('%s: the parity zero %s carries law_claim and laws None' % (name, eid))
            out[eid] = dict(rl)
            continue
        if d['law_claim'] != LAWCERT_CLAIM:
            raise ValueError('%s: entry %s: the law claim is not the certified text' % (name, eid))
        cl = _cert_laws(eid, d['laws'], expected_J_REF, expected_N - 1)
        if cl != rl['laws']:
            raise ValueError('%s: entry %s: the certificate laws differ from the record\'s' % (name, eid))
        out[eid] = dict(rl)
    return {'records': want, 'asm': dict(a), 'entries': out, 'J_REF': expected_J_REF, 'N': expected_N}


def _producer(name, out_text, expected_N, cert):
    """the producer pin: the writing job's first line names an allow-listed producer with its full sha256 and the expected N, and
    the certificate binds exactly that producer's record set (names and families)."""
    m = PRODUCER_RE.fullmatch(out_text.split('\n', 1)[0])
    if not m:
        raise ValueError("%s: the writing job's first line does not name an allowed law-certificate producer" % name)
    prod = m.group(1) + '.py'
    if prod not in PRODUCERS or m.group(4) != PRODUCERS[prod] or int(m.group(2)) != _expect(expected_N, 'N'):
        raise ValueError('%s: %s (sha256 %s, N %s) is not an allowed producer of N %r certificates' % (name, prod, m.group(4)[:8], m.group(2), expected_N))
    suffix, fams = PRODUCER_RECORDS[prod]
    got = cert.get('records') if isinstance(cert, dict) else None
    if (not isinstance(got, dict) or set(got) != set(fams)
            or any(not isinstance(v, dict) or v.get('file') != 'm3_s8v3_%s_N%d%s' % (f, expected_N, suffix) for f, v in got.items())):
        raise ValueError('%s: %s certifies exactly the records m3_s8v3_<F>_N%d%s, F in %s' % (name, prod, expected_N, suffix, fams))
    return prod


def load_lawcert(path, out_path, expected_J_REF, expected_N, recs):
    """the certified entry point for an M3_LAWCERT_v1 certificate; out_path is the output of the m3_lawcert job that wrote it and recs
    the records the consumer loaded with load, as {family: record}."""
    with open(path, 'rb') as fh:
        data = fh.read()
    with open(out_path) as fh:
        out_text = fh.read()
    _bound(os.path.basename(path), data, out_text)
    cert = json.loads(data.decode())
    prod = _producer(os.path.basename(path), out_text, expected_N, cert)
    out = _parse_lawcert(cert, path, expected_J_REF, expected_N, recs)
    out['producer'] = prod
    return out


def loads_lawcert(text, out_text, expected_J_REF, expected_N, recs, name):
    """load_lawcert in memory (the producer's C-LAWCERT-RT and plants)."""
    _bound(name, text.encode(), out_text)
    cert = json.loads(text)
    prod = _producer(name, out_text, expected_N, cert)
    out = _parse_lawcert(cert, name, expected_J_REF, expected_N, recs)
    out['producer'] = prod
    return out


def entry_law(cert, family, key):
    """the checked law of entry family:key: {parity, laws (exact rationals; None for a parity zero), parts {rem, tail, ann, far, rnd},
    ak, ak_rad, err, J_REF}. The consumer evaluates LAWCERT_CLAIM's right side at a piece's J_lo >= J_REF with outward rounding.
    either the midpoints ak with sum_k ak_rad[k] t^k (this form), or entry_ball's ak -+ ak_rad with the four parts and no ak_rad
    term; never both, and never neither."""
    return cert['entries']['%s:%s' % (family, key)]
