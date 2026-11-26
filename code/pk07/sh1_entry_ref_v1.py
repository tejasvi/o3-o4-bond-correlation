"""sh1_entry_ref_v1.py -- pk07 (code/pk07/). The C-FMT reference reader of kt_sh1_v1's ENTRY lines (pk15's float SH1/SH2
t entries), for kt_s9h_v1's FLOAT t provider. Not a script: the fork executes it in a fresh namespace only after its sha256 matches the
pin, and calls read_entries on the same text its own reader parses. It shares no code with that reader.
An ENTRY line reads: ENTRY N=<N> <name> (graph <graph>, Dn <d>, Q-degree <q>; series <x> s, sums <y> s): ak=[<a_0>, <a_1>, ...]
with <name> free of spaces (it may hold commas and |). read_entries returns {(N, name): (graph, [coefficient strings])} and raises
ValueError on a repeated (N, name) or an ENTRY line whose shape differs."""


def read_entries(text):
    found = {}
    for line in text.splitlines():
        if not line.startswith('ENTRY N='):
            continue
        head, sep, tail = line.partition('): ak=[')
        if sep == '' or not tail.endswith(']'):
            raise ValueError('kt_sh1_v1 reference reader: ENTRY line without "): ak=[...]": %r' % line[:80])
        words = head.split(' ')
        if len(words) < 4 or not words[1][2:].isdigit() or words[3] != '(graph':
            raise ValueError('kt_sh1_v1 reference reader: ENTRY head not "ENTRY N=<N> <name> (graph ...": %r' % head[:80])
        n, name, graph = int(words[1][2:]), words[2], words[4].rstrip(',')
        coefficients = [c.strip() for c in tail[:-1].split(',')]
        if (n, name) in found:
            raise ValueError('kt_sh1_v1 reference reader: ENTRY N=%d %s repeated' % (n, name))
        found[(n, name)] = (graph, coefficients)
    return found
