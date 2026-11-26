#!/usr/bin/env python3
"""m3_handoff_v3_hl.py -- pk23 (code/pk23/pev/): pk22's m3_handoff_v3_px22.py (sha256 92bdfee1da111163c1f32e5bdc8e62f2b59cf4e377be23235964d2ff86801d58) with HAND moved to pk23/pev/hand
(pk23's make_run_hl_v1.py; the only change). m3_handoff_v3_px22.py was: a COPY of pk03/m3_handoff_v3.py (sha256 e4f5bf0b111197d87e9659c89265c68fcfe39e564860c6e6b6eb91c9c48feb21) with HAND moved to
pk22/m3/hand, the only change (write() asserts that folder; read() reads there). Made by pk22/m3/make_copy_c1_v1.py.
pk03's docstring follows.
m3_handoff_v3.py -- pk03 (code/pk03/). Hand-offs between the pieces of m3_run (PLAN_M3_CODE_v1 sect. 7, kt_cert_v1_5 part 6):
REVISION of m3_handoff_v2.py (847f3aa6), for the T48 rule 2 (PLAN_M3_CODE_v1_2_ADD5 sect. 4.2): read() takes the producer's expected
verdict line and requires the record's VERDICT lines to equal exactly [that line]; no substring or prefix test remains.
verdict_ok() is the same test on a list of lines, and plant_verdict() feeds it a record whose verdict differs from the expected one.
REVISION of m3_handoff_v1.py (04babdf4, never run): iv_enc stores SIGNED mantissas (libmp.to_man_exp drops the sign; the sign is raw[0]).
a JSON file in pk03/hand/, under 2 MB, holding a header (producer script sha256, item, family, N, kernel name and sha, module shas,
trial set) and a body (named mp.iv intervals stored exactly as [man, exp] pairs of both ends, binary64 numbers, ints, strings, lists), then
an END line with the body's sha256. The producing piece prints 'HANDOFF <file> <sha256 of the file>' and its VERDICT; the reader requires
VERDICT VALID in the producer's record, the file's sha256 equal to the printed one, the END checksum, and the header fields it expects.
plant_handoff() makes three tampered in-memory copies (a body byte, the header's script sha, the END checksum) that read_text must refuse.
No compute of its own.
"""
import hashlib
import json
import os
from mpmath import iv, libmp

HAND = '/mnt/g2/release/root/code/pk23/pev/hand'   # pk23 hl_v1 copy: hand-offs in pk23/pev/hand
MAXB = 2 * 1024 * 1024


def iv_enc(x):
    """an interval as {'iv': [[man, exp], [man, exp]]}, exact."""
    a, b = x._mpi_
    for r in (a, b):
        if r in (libmp.finf, libmp.fninf, libmp.fnan):
            raise FloatingPointError('non-finite interval end in a hand-off')
    sm = lambda r: [(-r[1] if r[0] else r[1]), r[2]]
    return {'iv': [sm(a), sm(b)]}


def iv_dec(d):
    (ma, ea), (mb, eb) = d['iv']
    return iv.make_mpf((libmp.from_man_exp(int(ma), int(ea)), libmp.from_man_exp(int(mb), int(eb))))


def enc(v):
    if hasattr(v, '_mpi_'):
        return iv_enc(v)
    if isinstance(v, dict):
        return {str(k): enc(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [enc(x) for x in v]
    if isinstance(v, (bool, int, float, str)) or v is None:
        return v
    raise TypeError('cannot hand off %r' % type(v))


def dec(v):
    if isinstance(v, dict):
        if set(v) == {'iv'}:
            return iv_dec(v)
        return {k: dec(x) for k, x in v.items()}
    if isinstance(v, list):
        return [dec(x) for x in v]
    return v


def _sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def make_text(header, body):
    btxt = json.dumps(enc(body), sort_keys=True)
    return json.dumps(header, sort_keys=True) + '\n' + btxt + '\nEND ' + _sha(btxt) + '\n'


def write(name, header, body):
    """writes hand/<name> (new file, own folder asserted); returns (path, sha256 of the file)."""
    path = os.path.join(HAND, name)
    assert os.path.dirname(os.path.abspath(path)) == HAND and '/' not in name and not os.path.exists(path), path
    text = make_text(header, body)
    if len(text.encode('utf-8')) > MAXB:
        raise ValueError('hand-off over 2 MB: %d bytes' % len(text))
    with open(path, 'x') as fh:
        fh.write(text)
    return path, _sha(text)


def read_text(text, expect):
    """(header, body) after the END checksum and the expected header fields; ValueError otherwise."""
    lines = text.split('\n')
    if len(lines) != 4 or lines[3] != '' or not lines[2].startswith('END '):
        raise ValueError('hand-off layout')
    if _sha(lines[1]) != lines[2][4:]:
        raise ValueError('hand-off END checksum')
    header = json.loads(lines[0])
    for k, v in expect.items():
        if header.get(k) != v:
            raise ValueError('hand-off header %s: %r, expected %r' % (k, header.get(k), v))
    return header, dec(json.loads(lines[1]))


def verdict_ok(rec_lines, verdict):
    """True iff the record's VERDICT lines are exactly [verdict]."""
    return [ln for ln in rec_lines if ln.startswith('VERDICT')] == [verdict]


def read(name, producer_out, expect, verdict):
    """reads hand/<name> after checking the producer's record: VERDICT lines exactly [verdict] and 'HANDOFF <name> <sha>' with the file's sha256."""
    path = os.path.join(HAND, name)
    with open(path) as fh:
        text = fh.read()
    with open(producer_out) as fh:
        rec = fh.read().split('\n')
    if not verdict_ok(rec, verdict):
        raise ValueError('producer record %s: VERDICT lines are not exactly [%r]' % (producer_out, verdict))
    want = [ln.split()[2] for ln in rec if ln.startswith('HANDOFF ') and len(ln.split()) == 3 and ln.split()[1] == name]
    if len(want) != 1 or want[0] != _sha(text):
        raise ValueError('hand-off %s: sha256 does not match the producer record' % name)
    return read_text(text, expect)


def plant_handoff(text, expect):
    """three tampered copies; returns the list of (label, refused)."""
    lines = text.split('\n')
    body = lines[1]
    i = body.find('1')
    c1 = '\n'.join([lines[0], body[:i] + ('2' if i >= 0 else '') + body[i + 1:], lines[2], lines[3]])
    h = json.loads(lines[0])
    h['script'] = (h.get('script') or '0' * 64)[:-1] + ('0' if (h.get('script') or '0')[-1] != '0' else '1')
    c2 = '\n'.join([json.dumps(h, sort_keys=True), lines[1], lines[2], lines[3]])
    c3 = '\n'.join([lines[0], lines[1], 'END ' + '0' * 64, lines[3]])
    out = []
    for lab, t in (('body byte', c1), ('header script sha', c2), ('END checksum', c3)):
        try:
            read_text(t, expect)
            out.append((lab, False))
        except ValueError:
            out.append((lab, True))
    return out


def plant_verdict(verdict):
    """a record whose only verdict line is the expected one with '-PRECERT ...' appended (a superstring) must fail verdict_ok."""
    return not verdict_ok(['HANDOFF x 0', verdict + '-PRECERT (planted)'], verdict)
