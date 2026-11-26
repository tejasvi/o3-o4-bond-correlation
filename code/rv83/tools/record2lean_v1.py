#!/usr/bin/env python3
"""record2lean_v1.py: turns rows of an O5 record table (O5_RECORD_TABLE_*.tsv) into Lean code-pair terms for
StripIII.Core's box5List / o5List. For each LABEL it requires a row at every N given, each with certified True, verdict VALID, status DONE,
rc 0, args_match True and engine_g37 True, and the same members at every N; it then prints every member pair as Lean edge codes (the
engine's h<r><c> is ECode.hor r c and v<r><c> is ECode.ver r c), as plain pairs (TAG -) or as (TAG, e, f) triples, and one comment line
per label with N, J1, L, c2 and out_sha256 prefixes. It prints the table's path and sha256 first. Usage: record2lean_v1.py TABLE TAG NS LABELS
(NS like 3,4 or 4; LABELS like n5_G06,n5_G12)"""
import hashlib
import re
import sys


def code(name):
    m = re.fullmatch(r'([hv])(\d)(\d+)', name)
    assert m, name
    return ('.hor %d %d' if m.group(1) == 'h' else '.ver %d %d') % (int(m.group(2)), int(m.group(3)))


def main():
    path, tag, ns, labels = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')], sys.argv[4].split(',')
    with open(path, 'rb') as fh:
        raw = fh.read()
    rows = [ln.split('\t') for ln in raw.decode('utf-8').splitlines()]
    head = rows[0]
    ix = {k: i for i, k in enumerate(head)}
    data = rows[1:]
    print('-- source %s sha256 %s; labels %s; N %s' % (path, hashlib.sha256(raw).hexdigest(), ','.join(labels), ','.join(map(str, ns))))
    terms = []
    for lab in labels:
        mem = None
        notes = []
        for N in ns:
            rr = [r for r in data if r[ix['label']] == lab and int(r[ix['N']]) == N]
            assert len(rr) == 1, (lab, N, len(rr))
            r = rr[0]
            ok = (r[ix['certified']] == 'True' and r[ix['verdict']] == 'VALID' and r[ix['status']] == 'DONE' and r[ix['rc']] == '0'
                  and r[ix['args_match']] == 'True' and r[ix['engine_g37']] == 'True')
            assert ok, (lab, N, 'not certified/valid')
            m = re.findall(r'\((\w+), (\w+)\)', r[ix['members']])
            assert mem is None or m == mem, (lab, 'members differ across N')
            mem = m
            notes.append('N=%d J1 %s L %s c2 %s out %s' % (N, r[ix['J1']], r[ix['L']], r[ix['c2']], r[ix['out_sha256']][:8]))
        terms.append('  -- %s (%d members): %s' % (lab, len(mem), '; '.join(notes)))
        for a, b in mem:
            t = '(%s, %s)' % (code(a), code(b))
            terms.append('  ' + (t if tag == '-' else '(%s, %s, %s)' % (tag, code(a), code(b))) + ',')
    body = '\n'.join(terms)
    i = body.rfind(',')
    print(body[:i] + body[i + 1:])
    print('-- total %d pairs' % sum(1 for t in terms if not t.strip().startswith('--')))


if __name__ == '__main__':
    main()
