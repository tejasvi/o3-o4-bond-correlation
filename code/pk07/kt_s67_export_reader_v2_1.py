"""kt_s67_export_reader_v2_1.py -- pk07 (code/pk07/). REVISION of kt_s67_export_reader_v2.py (1b19d393, frozen, never run) after
the V1 item: (a) the V1 note below, on why jlo and jhi may be returned as floats; (b) two read checks that make the note hold for every
accepted file: a grid token must be the shortest repr of its float, and the pieces of each N must chain. Everything else is v2.
The bound reader of EXPORT_KT_S67_v1 for S8's certified path (pk11, kt_s8_cert_v1), in the style of m3_reader_v4_4, so that the
producer's C-EXPORT and the consumer share one check. Not a script: consumers execute it sha-pinned.
- load(export_path, run_out_path): the only certified entry point. The run output (the producing sweep's .out) must have VERDICT lines
  exactly ['VERDICT VALID'] and exactly one line 'EXPORT <path> sha256 <hex> ...' whose <path> has this export's base name, and <hex>
  must be the sha256 of the export's bytes (rule V2: pin only a sha printed on an EXPORT line of a VALID run). Then parse_export, and
  the export must read EXPORT_STATUS = CERTIFIED and RUN_VERDICT = VALID. Anything else raises ValueError.
- loads(text, out_text, name): load in memory (the producer's C-EXPORT and plants); name is the export's base name.
- load_noncert(export_path) and loads_noncert(text): exports whose EXPORT_STATUS is not CERTIFIED (FLOAT-PASS, MOCK, ...), without the
  binding, for hand work on mocks. A CERTIFIED export is refused there, so the two paths cannot be confused.
- parse_export(text): v1's parse with rule V1: jlo and jhi read as floats (float(token); the last piece's 'inf' reads as math.inf);
  every other field reads exactly (Fraction), and 'inf' is refused there.
V1, why jlo and jhi may be floats. The producer's pieces are binary64 numbers: kt_s9h's pieces() makes them by a float recurrence from
300.0, its certified evaluations take them exactly (iv.mpf of a float is exact; t then runs over [(1/jhi).a, (1/jlo).b], rounded
outward), and export_row writes repr(J). float() of a repr string returns the same double, and this reader refuses a grid token that is
not the shortest repr of its float, so the value returned is the very double the producer certified on, with nothing rounded on the
way. Consumers use it as that double: match pieces by == against their own float grid (or by the token strings), and wherever a grid
end enters a bound, convert the float exactly (Fraction(x), iv.mpf(x), arb(x)); never re-read the token as a decimal, since
Fraction(token) differs from the double for most grid ends (301.501875 is not dyadic). 'inf' (math.inf) is only the last piece's jhi,
the open end J -> infinity (t down to 0). The reader also checks that the pieces of each N chain: jlo < jhi, and the jhi of piece i
equals the jlo of piece i + 1 (exact float equality), so no J between piece 0's jlo and infinity is skipped; where the grid starts
(300.0 here) stays the consumer's grid check. Every other field is a bound and reads exactly, as the Fraction of its decimal.
EXPORT_KT_S67_v1 is an S4U_KV_v1 file: one "KEY = value" per line, KEY of [A-Z][A-Z0-9_]*, lines starting with # are comments, blank
lines carry nothing.
- Header keys: FORMAT = S4U_KV_v1, RECORD = EXPORT_KT_S67_v1 and END = EXPORT_KT_S67_v1; FIELDS and PAIR_FIELDS name the values of the
  piece lines, space-separated; N<N>_PIECES counts the piece lines of N; RUN_VERDICT and EXPORT_STATUS as written by the producer.
- Piece lines: N<N>_P<index, 4 digits> = <FIELDS values> | <one group per claimed pair, " ; "-separated, each the PAIR_FIELDS values>;
  the pieces of each N are numbered 0..N<N>_PIECES - 1.
- Pair values: kind is "flip" or "same", d, m_checked and k_mode are integers, holds is "yes" or "no".
parse_export returns {'header': {KEY: value}, 'fields': [...], 'pair_fields': [...], 'pieces': {N: {index: {name: value}}}}."""
import hashlib
import math
import os
import re
from fractions import Fraction

_KEYLINE = re.compile(r'([A-Z][A-Z0-9_]*) = (.*)')
_PIECE = re.compile(r'N([34])_P([0-9]{4})')
_NUMBER = re.compile(r'-?[0-9]+(\.[0-9]+)?(e[+-]?[0-9]+)?')
_FLOAT_FIELDS = ('jlo', 'jhi')


def _exact(token):
    if _NUMBER.fullmatch(token) is None:
        raise ValueError('EXPORT_KT_S67_v1 reader: %r is not a decimal' % token)
    return Fraction(token)


def _grid(token):
    if token == 'inf':
        return math.inf
    if _NUMBER.fullmatch(token) is None:
        raise ValueError('EXPORT_KT_S67_v1 reader: %r is not a grid float' % token)
    v = float(token)
    if math.isnan(v) or math.isinf(v) or repr(v) != token:
        raise ValueError('EXPORT_KT_S67_v1 reader: grid token %r is not the shortest repr of a finite float (V1)' % token)
    return v


def parse_export(text):
    header, raw_pieces = {}, []
    for number, line in enumerate(text.splitlines(), start=1):
        if line[:1] == '#' or line.strip() == '':
            continue
        hit = _KEYLINE.fullmatch(line)
        if hit is None:
            raise ValueError('EXPORT_KT_S67_v1 reader: line %d is not KEY = value' % number)
        key, value = hit.groups()
        if key in header:
            raise ValueError('EXPORT_KT_S67_v1 reader: line %d repeats %s' % (number, key))
        header[key] = value
        piece = _PIECE.fullmatch(key)
        if piece is not None:
            raw_pieces.append((int(piece.group(1)), int(piece.group(2)), value))
    for key, want in (('FORMAT', 'S4U_KV_v1'), ('RECORD', 'EXPORT_KT_S67_v1'), ('END', 'EXPORT_KT_S67_v1')):
        if header.get(key) != want:
            raise ValueError('EXPORT_KT_S67_v1 reader: %s is %r, not %r' % (key, header.get(key), want))
    fields = header.get('FIELDS', '').split()
    pair_fields = header.get('PAIR_FIELDS', '').split()
    if fields[:2] != list(_FLOAT_FIELDS) or pair_fields != ['kind', 'd', 'm_checked', 'k_mode', 'holds']:
        raise ValueError('EXPORT_KT_S67_v1 reader: FIELDS (starting jlo jhi) or PAIR_FIELDS missing or not as specified')
    pieces = {}
    for n, index, value in raw_pieces:
        left, bar, right = value.partition(' | ')
        tokens = left.split(' ')
        if bar != ' | ' or len(tokens) != len(fields):
            raise ValueError('EXPORT_KT_S67_v1 reader: piece N%d_P%04d does not have the FIELDS values and a pair part' % (n, index))
        entry = {name: (_grid(token) if name in _FLOAT_FIELDS else _exact(token)) for name, token in zip(fields, tokens)}
        pairs = []
        for group in right.split(' ; '):
            parts = group.split(' ')
            if (len(parts) != 5 or parts[0] not in ('flip', 'same') or parts[4] not in ('yes', 'no')
                    or not all(p.isdigit() for p in parts[1:4])):
                raise ValueError('EXPORT_KT_S67_v1 reader: piece N%d_P%04d has a malformed pair %r' % (n, index, group))
            pairs.append(dict(kind=parts[0], d=int(parts[1]), m_checked=int(parts[2]), k_mode=int(parts[3]), holds=parts[4]))
        entry['pairs'] = pairs
        pieces.setdefault(n, {})[index] = entry
    for n in pieces:
        if header.get('N%d_PIECES' % n) != str(len(pieces[n])) or sorted(pieces[n]) != list(range(len(pieces[n]))):
            raise ValueError('EXPORT_KT_S67_v1 reader: the N = %d piece lines are not numbered 0..N%d_PIECES - 1' % (n, n))
        last = len(pieces[n]) - 1
        for i in range(last + 1):
            e = pieces[n][i]
            nxt = pieces[n][i + 1]['jlo'] if i < last else math.inf
            if not (e['jlo'] < e['jhi'] and e['jhi'] == nxt):
                raise ValueError('EXPORT_KT_S67_v1 reader: the N = %d pieces do not chain at piece %d (jlo < jhi = next jlo, the last '
                                 'jhi inf; V1)' % (n, i))
    return {'header': header, 'fields': fields, 'pair_fields': pair_fields, 'pieces': pieces}


def _bound(name, data, out_text):
    """V2: the run output's VERDICT lines are exactly ['VERDICT VALID'], and exactly one EXPORT line names this export (its base name)
    with the sha256 of its bytes."""
    lines = out_text.split('\n')
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise ValueError("%s: the run output's VERDICT lines are not exactly ['VERDICT VALID']" % name)
    hits = [ln.split() for ln in lines if ln.startswith('EXPORT ')]
    hits = [h for h in hits if len(h) >= 4 and h[2] == 'sha256' and os.path.basename(h[1]) == name]
    if len(hits) != 1 or hits[0][3] != hashlib.sha256(data).hexdigest():
        raise ValueError('%s: the run output does not name this export with its sha256 on exactly one EXPORT line' % name)


def _certified(parsed, name):
    h = parsed['header']
    if h.get('EXPORT_STATUS') != 'CERTIFIED' or h.get('RUN_VERDICT') != 'VALID':
        raise ValueError('%s: not a certified export (EXPORT_STATUS %r, RUN_VERDICT %r)' % (
            name, h.get('EXPORT_STATUS'), h.get('RUN_VERDICT')))
    return parsed


def load(export_path, run_out_path):
    """the only certified entry point (rule V2)."""
    with open(export_path, 'rb') as fh:
        data = fh.read()
    with open(run_out_path) as fh:
        out_text = fh.read()
    name = os.path.basename(export_path)
    _bound(name, data, out_text)
    return _certified(parse_export(data.decode('utf-8')), name)


def loads(text, out_text, name):
    """load in memory: text is the export's content, out_text the producing run's output, name the export's base name."""
    _bound(name, text.encode('utf-8'), out_text)
    return _certified(parse_export(text), name)


def loads_noncert(text):
    """an export that is not CERTIFIED (FLOAT-PASS, MOCK, ...), without the binding; a CERTIFIED export is refused."""
    parsed = parse_export(text)
    if parsed['header'].get('EXPORT_STATUS') == 'CERTIFIED':
        raise ValueError('a CERTIFIED export is read only through load or loads')
    return parsed


def load_noncert(export_path):
    with open(export_path) as fh:
        return loads_noncert(fh.read())
