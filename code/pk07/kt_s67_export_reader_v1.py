"""kt_s67_export_reader_v1.py -- pk07 (code/pk07/). The producer's reader of EXPORT_KT_S67_v1, the per-piece export that the
sweep of kt_s67_cert_v2_2 (and later revisions) writes for S8 (pk11). Not a script: the port executes it, sha-pinned, to read back
what it wrote (C-EXPORT), and an importer can pin it as the producer's reader for its own C-FMT.
EXPORT_KT_S67_v1 is an S4U_KV_v1 file: one "KEY = value" per line, lines starting with # are comments, blank lines carry nothing.
- Header keys: FORMAT = S4U_KV_v1, RECORD = EXPORT_KT_S67_v1 and END = EXPORT_KT_S67_v1; FIELDS and PAIR_FIELDS name the values of the
  piece lines, space-separated; CLAIM_N<N> lists the claimed pairs as "kind d ; kind d"; N<N>_PIECES counts the piece lines of N.
- Piece lines: N<N>_P<index, 4 digits> = <FIELDS values> | <one group per claimed pair, " ; "-separated, each the PAIR_FIELDS values>.
- Numbers are decimal strings and are read exactly (Fraction); "inf" (the last piece's open end) reads as None. Fields named *_lo are
  lower bounds rounded down when written, *_hi upper bounds rounded up; jlo and jhi are the grid's float J ends (repr).
- Pair values: kind is "flip" or "same", d, m_checked and k_mode are integers, holds is "yes" or "no".
parse_export(text) returns {'header': {KEY: value}, 'fields': [...], 'pair_fields': [...], 'pieces': {N: {index: {name: value}}}}
and raises ValueError on any line or value that does not fit."""
import re
from fractions import Fraction

_KEYLINE = re.compile(r'([A-Z][A-Z0-9_]*) = (.*)')
_PIECE = re.compile(r'N([34])_P([0-9]{4})')
_NUMBER = re.compile(r'-?[0-9]+(\.[0-9]+)?(e[+-]?[0-9]+)?')


def _number(token):
    if token == 'inf':
        return None
    if _NUMBER.fullmatch(token) is None:
        raise ValueError('EXPORT_KT_S67_v1 reader: %r is not a decimal' % token)
    return Fraction(token)


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
    if not fields or pair_fields != ['kind', 'd', 'm_checked', 'k_mode', 'holds']:
        raise ValueError('EXPORT_KT_S67_v1 reader: FIELDS or PAIR_FIELDS missing or not as specified')
    pieces = {}
    for n, index, value in raw_pieces:
        left, bar, right = value.partition(' | ')
        tokens = left.split(' ')
        if bar != ' | ' or len(tokens) != len(fields):
            raise ValueError('EXPORT_KT_S67_v1 reader: piece N%d_P%04d does not have the FIELDS values and a pair part' % (n, index))
        entry = {name: _number(token) for name, token in zip(fields, tokens)}
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
    return {'header': header, 'fields': fields, 'pair_fields': pair_fields, 'pieces': pieces}
