#!/usr/bin/env python3
"""m3_reader_v4_4.py -- pk03 (code/pk03/). REVISION of m3_reader_v4_3.py (adf51038, never run or cited) for the review
ad0ceca7 of m3_run_v1_5_1 (and its ADD1 18a634fa): the bound loader is the only certified entry point.
- load(path, asm_out, expected_J_REF, expected_N): asm_out is the output of the asm run that wrote the record. Its VERDICT lines must
  be exactly ['VERDICT VALID'], and it must name the file with the sha256 of its bytes on exactly one 'RECORD <file name> <sha256>'
  line; then every check of the certified parse. loads(text, out_text, expected_J_REF, expected_N, name) does the same in memory.
- check_text(text, expected_J_REF, expected_N, name) is the certified parse without the binding. It serves only the writer's C-FMT and
  plants before any file is written; it is not an entry point for consumers.
- load_noncert and loads_noncert read PRECERT and STUB records, as before.
m3_reader_v4_3: REVISION of m3_reader_v4_2.py (0dad53a3, never run) for the review dfdc53da
sect. 1 (B) and sect. 4 item 3, and the M2(b) kernel fields:
- load_bound(path, expected_J_REF, expected_N, asm_out) is the consumers' entry point. The asm output that wrote the record must have
  VERDICT lines exactly ['VERDICT VALID'] and exactly one line 'RECORD <file name> <sha256>' for this file, with the file's sha256;
  then every check of load. loads_bound(text, expected_J_REF, expected_N, out_text, name) does the same in memory (the writer's plants).
- the arb base under the arb recompute engine, (arb_base_file, arb_base_sha256), must equal ARB_BASE (arbeng_c2b_v2), beside ARB_KERNEL.
load and loads stay for the writer's C-FMT on the texts before any file is written.
m3_reader_v4_2: REVISION of m3_reader_v4_1.py (242bdff3, never run or cited), for the review c897cdd7
sect. 5 and pk02's SPEC_M2B_CERT_v1_ADD1 sect. 7 (the builder reads M3 records only through this reader):
- FORMAT and claim are accepted by an exact allow-list: a certified record's claim must equal CERT_CLAIM, a PRECERT or STUB record's
  claim its prefix + CERT_CLAIM; nothing is refused by a deny-list any more;
- load/loads take expected_N beside expected_J_REF, both positive ints from the consumer, compared exactly with the record's N and J_REF;
- the arb recompute engine named by the record (arb_kernel_file, arb_kernel_sha256) must be the pinned arbeng_ma_stub_v1_1.
m3_reader_v4_1: REVISION of m3_reader_v4.py (a9f26cb3), for the M2(b) s4 review (c897cdd7)
item 1: a certified record's kernel is matched as (kernel_file, kernel_sha256, kernel_prec) plus its validation list, and kernel_prec
must be 512 (the closed layer's PREC). m3_reader_v4: The independent reader of M3's records (PLAN_M3_CODE_v1 sect. 4), sha-pinned by every
consumer for its C-FMT; it shares no code with the writer.
REVISION of m3_reader_v3.py (63a190e6) for the T48 rule 1 and T50 (PLAN_M3_CODE_v1_2_ADD5 sect. 4, 6):
- load(path, expected_J_REF, expected_N) accepts only FORMAT 'M3_RECORD_v1' with the certified claim, J_REF == expected_J_REF and
  N == expected_N exactly, (kernel_file, kernel_sha256, kernel_prec, validation list) equal to this file's frozen VALIDATED_LAYER and
  KERNEL_PREC, and (arb_kernel_file, arb_kernel_sha256) equal to ARB_KERNEL; anything else raises ValueError.
  load_noncert(path, expected_J_REF, expected_N) reads PRECERT and STUB records (FORMAT and claim must agree) for producers' C-FMT.
- every item needs kind 'entry', and a key starting 'VAC_OF_' (ADD4's outer_far items) is refused: m3_reader_v5 adds those items once
  the vacuum region boundaries are agreed with pk02;
- entry items as v3 (ak, ak_rad, B, Bp, err, parity), with rnd >= sum_k ak_rad_k Fraction(1, J_REF)^k exactly;
entry_ball(rec, key) returns (LO list, HI list, err_b) for an entry item as v3. No compute of its own.
"""
import hashlib
import json
import os
import math
from decimal import Decimal
from fractions import Fraction

PARTS = ('rem', 'tail', 'ann', 'far', 'rnd')
CERT_FORMAT = 'M3_RECORD_v1'
NONCERT = {'M3_RECORD_v1_PRECERT': 'NOT CERTIFIED (PRECERT): ', 'M3_RECORD_v1_STUB': 'NOT CERTIFIED (STUB): '}
CERT_CLAIM = 'for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err (Lemma U: PLAN_M3_CODE_v1 sect. 5, v1_2 sect. C)'
KERNEL_PREC = 512   # the layer runs at ctx.prec 512
VALIDATED_LAYER = ('arbeng_ma_v1_3.py', '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be',   # 
                   ('5ccbb6d006f5365f219eb6221b7e66b76e7e7799e977148df94f34b0c3d86216',   # kt_ma_val_v1_5 v1
                    'a61d893e6424b9ea524d944e40f625c934de04a2faeaa741e3fd333e97f48817',   # v2
                    'd613fe804a030be397fefa46ed1424063f794400b7d9618e12db8af046e09d93',   # v3
                    '2ad13ec3cac14ef919f5e34fa19664f70eece05c3c3f208dcfec36a93cdd4473',   # v4
                    'a8a5e8d020d2d1e1127c3ee8f400496011ddbd022af83180025ac3185ba22f95'))  # CLOSE_ARBENG_MA_V1_3_rv01.md
ARB_KERNEL = ('arbeng_ma_stub_v1_1.py', '794fabc7111555db2f6390a144d3f5af6deeb358d02da8b5705cf3ceaefd0af1')   # the arb recompute engine of MAFallback (close condition (ii))
ARB_BASE = ('arbeng_c2b_v2.py', '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0')   # the arb base under ARB_KERNEL


def _num(x, what):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(float(x)):
        raise ValueError('%s: not a finite number: %r' % (what, x))
    return float(x)


def _entry(key, d, j_ref):
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
    elif d.get('parity') != 'free':
        raise ValueError('%s: parity must be zero or free' % key)
    rad = d.get('ak_rad')
    if not isinstance(rad, list) or len(rad) != 4:
        raise ValueError('%s: ak_rad must be a list of 4 numbers' % key)
    rad = [_num(r, key + ' ak_rad') for r in rad]
    if any(r < 0 for r in rad) or (d.get('parity') == 'zero' and any(r != 0.0 for r in rad)):
        raise ValueError('%s: ak_rad must be >= 0, and 0 for a parity zero' % key)
    if d.get('parity') == 'free' and Fraction(Bv['rnd']) < sum(Fraction(r) * Fraction(1, j_ref) ** k for k, r in enumerate(rad)):
        raise ValueError('%s: rnd below sum_k ak_rad_k (1/J_REF)^k' % key)
    return ak, err, rad


def _items(rec, path, j_ref):
    items = dict(rec.get('items', {}))
    if 'I_N' in rec:
        items['I_N'] = rec['I_N']
    if not items:
        raise ValueError('%s: no items' % path)
    ents, ofs = {}, {}
    for k, d in items.items():
        kind = d.get('kind') if isinstance(d, dict) else None
        if k.startswith('VAC_OF_'):
            raise ValueError('%s: item %s is an outer_far key; this reader version reads entries only' % (path, k))
        if kind != 'entry':
            raise ValueError('%s: item %s has kind %r, expected ''entry''' % (path, k, kind))
        ents[k] = _entry(k, d, j_ref)
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
        if (rec.get('kernel_file'), rec.get('kernel_sha256'), rec.get('kernel_prec'), tuple(rec.get('validation') or ())) != (
                VALIDATED_LAYER[0], VALIDATED_LAYER[1], KERNEL_PREC, tuple(VALIDATED_LAYER[2])):
            raise ValueError('%s: kernel %r (prec %r) is not the validated layer this reader pins' % (path, rec.get('kernel_file'), rec.get('kernel_prec')))
        if (rec.get('arb_kernel_file'), rec.get('arb_kernel_sha256')) != ARB_KERNEL:
            raise ValueError('%s: arb kernel %r is not the arb recompute engine this reader pins' % (path, rec.get('arb_kernel_file')))
        if (rec.get('arb_base_file'), rec.get('arb_base_sha256')) != ARB_BASE:
            raise ValueError('%s: arb base %r is not the one this reader pins' % (path, rec.get('arb_base_file')))
    elif fmt not in NONCERT or claim != NONCERT[fmt] + CERT_CLAIM:
        raise ValueError('%s: not a PRECERT or STUB record with its claim prefix (format %r)' % (path, fmt))
    items, ents, ofs = _items(rec, path, expected_J_REF)
    balls = {k: ([Fraction(a) - Fraction(r) for a, r in zip(v[0], v[2])], [Fraction(a) + Fraction(r) for a, r in zip(v[0], v[2])],
                 sum(Fraction(x) for x in items[k]['Bp'].values())) for k, v in ents.items()}
    return {'top': {k: v for k, v in rec.items() if k not in ('items', 'I_N')}, 'entries': {k: (v[0], v[1]) for k, v in ents.items()},
            'balls': balls, 'outer_far': ofs}


def check_text(text, expected_J_REF, expected_N, name='<text>'):
    """the writer's C-FMT and plants on a record text before any file is written. It does not bind the text to a run output, so it
    is not an entry point for consumers: they call load."""
    return _parse(json.loads(text), name, expected_J_REF, expected_N, True)


def _bound(name, data, out_text):
    """the review dfdc53da sect. 1 (B): the asm output must have VERDICT lines exactly ['VERDICT VALID'] and name this file (its base name)
    with the sha256 of its bytes on exactly one RECORD line."""
    lines = out_text.split('\n')
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise ValueError("%s: the asm output's VERDICT lines are not exactly ['VERDICT VALID']" % name)
    hit = [ln.split() for ln in lines if ln.startswith('RECORD ') and len(ln.split()) == 3 and ln.split()[1] == name]
    if len(hit) != 1 or hit[0][2] != hashlib.sha256(data).hexdigest():
        raise ValueError('%s: the asm output does not name this file with its sha256 on exactly one RECORD line' % name)


def load(path, asm_out, expected_J_REF, expected_N):
    """the only certified entry point for a record file; asm_out is the output of the asm run that wrote it."""
    with open(path, 'rb') as fh:
        data = fh.read()
    with open(asm_out) as fh:
        out_text = fh.read()
    _bound(os.path.basename(path), data, out_text)
    return _parse(json.loads(data.decode()), path, expected_J_REF, expected_N, True)


def loads(text, out_text, expected_J_REF, expected_N, name):
    """load in memory: text is the record file's content, out_text its asm output's, name the record file's base name."""
    _bound(name, text.encode(), out_text)
    return _parse(json.loads(text), name, expected_J_REF, expected_N, True)


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
