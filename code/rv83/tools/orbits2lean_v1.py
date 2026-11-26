#!/usr/bin/env python3
"""orbits2lean_v1.py: reads the ORBIT lines of an O5 engine output (kt_lbu_g3x grid mode: "ORBIT Gxx (e, f): ... members (a, b)
(c, d) ...") and prints, for the orbits named, every member pair as a Lean term of StripIII.Core's edge codes: the engine's h<r><c>
(row r, columns c and c + 1) is ECode.hor r c and v<r><c> (rows r and r + 1, column c) is ECode.ver r c. With TAG = n it prints
(n, e, f) triples for o5List, with TAG = - plain pairs for box5List. It also prints the source path, its sha256 and the member counts.
Usage: orbits2lean_v1.py OUTPUT TAG G1[,G2...]"""
import hashlib
import re
import sys


def code(name):
    m = re.fullmatch(r'([hv])(\d)(\d+)', name)
    assert m, name
    kind, r, c = m.group(1), int(m.group(2)), int(m.group(3))
    return ('.hor %d %d' if kind == 'h' else '.ver %d %d') % (r, c)


def main():
    path, tag, names = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
    with open(path, 'rb') as fh:
        raw = fh.read()
    found = {}
    for line in raw.decode('utf-8').splitlines():
        m = re.match(r'ORBIT (G\d+) \(', line)
        if m and m.group(1) in names:
            assert m.group(1) not in found, 'orbit twice: %s' % m.group(1)
            mem = line.split('members', 1)[1]
            found[m.group(1)] = re.findall(r'\((\w+), (\w+)\)', mem)
    missing = [g for g in names if g not in found]
    assert not missing, 'missing orbits %s' % missing
    terms = []
    for g in names:
        for a, b in found[g]:
            t = '(%s, %s)' % (code(a), code(b))
            terms.append(t if tag == '-' else '(%s, %s, %s)' % (tag, code(a), code(b)))
    print('-- source %s sha256 %s; orbits %s; members %s; total %d' % (
        path, hashlib.sha256(raw).hexdigest(), ','.join(names), ','.join(str(len(found[g])) for g in names), len(terms)))
    print(',\n'.join('  ' + t for t in terms))


if __name__ == '__main__':
    main()
