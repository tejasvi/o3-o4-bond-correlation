"""s4u_kv_ref_v1.py -- pk07 (code/pk07/). The C-FMT reference reader of format S4U_KV_v1, for kt_s67_cert_v2.py.
Not a script: kt_s67_cert_v2 executes this file in a fresh namespace only after its sha256 equals the port's pin, and calls
parse_s4u_kv on the same text its own reader parses. It shares no code with that reader.
S4U_KV_v1, as pk08/S4_U_CERTIFIED_v2.md states it in its header (l.6): one "KEY = value" per line; lines starting with # are
comments; blank lines carry nothing. Read here as: KEY is [A-Z][A-Z0-9_]*, the separator is the first " = " after KEY, the value is the
rest of the line as it stands; a line that is none of these, or a KEY seen before, is an error."""
import re

_LINE = re.compile(r'([A-Z][A-Z0-9_]*) = (.*)')


def parse_s4u_kv(text):
    """{KEY: value string} of an S4U_KV_v1 text; ValueError on a malformed line or a repeated KEY."""
    found = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if line[:1] == '#' or line.strip() == '':
            continue
        hit = _LINE.fullmatch(line)
        if hit is None:
            raise ValueError('S4U_KV_v1 reference: line %d is not KEY = value' % number)
        key, value = hit.groups()
        if key in found:
            raise ValueError('S4U_KV_v1 reference: line %d repeats %s' % (number, key))
        found[key] = value
    return found
