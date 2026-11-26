#!/usr/bin/env python3
"""map_pk24_labels_v1.py (pk23): maps pk24's n = 5 edge labels to the engine's orbit names, for the note N1 on the box run
record. pk24's labels (pk24/n5/n5map_v1.py l.2-8 and l.22-46): t<j>, h<j>, bb<j> are the horizontal bonds j = 1..4 of the top,
middle and bottom rows; a<c>, b<c> are the vertical edges at columns c = 1..5, with a on the t side ("same" kind {t, a}, "flip" kind
{t, b}, l.5-6; the T <-> B flip swaps t <-> bb and a <-> b, l.25). The engine's names (kt_lbu_g37 grid_build): h<r><c> is row r, bond c,
and v<r><c> the vertical from row r in column c, all 0-based. Convention A: t_j = h0(j-1), h_j = h1(j-1), bb_j = h2(j-1), a_c = v0(c-1),
b_c = v1(c-1). Convention B swaps a and b. For each label pair it finds the engine orbit whose ORBIT line lists the pair among its
members (the orbit is closed under both reflections, so the choice of top row does not matter), and compares the orbit's c2(N=4) with
pk24's value. Reads one engine output; writes stdout. Usage: map_pk24_labels_v1.py ENGINE_OUTPUT LABEL,LABEL=C2 ..."""
import re, sys


def eng(lbl, conv):
    ty, i = re.fullmatch(r'([a-z]+)(\d+)', lbl).groups()
    i = int(i)
    if ty in ('t', 'h', 'bb'):
        return 'h%d%d' % ({'t': 0, 'h': 1, 'bb': 2}[ty], i - 1)
    row = {'a': 0, 'b': 1}[ty] if conv == 'A' else {'a': 1, 'b': 0}[ty]
    return 'v%d%d' % (row, i - 1)


orbits = []
for ln in open(sys.argv[1]):
    m = re.match(r'ORBIT (G\d+) .*: size (\d+), .*c2\(N=4\) \S+ \(([-0-9.e+]+)\); members (.*)$', ln)
    if m:
        mem = {frozenset(x.split(', ')) for x in re.findall(r'\(([^)]+)\)', m.group(4))}
        orbits.append((m.group(1), int(m.group(2)), float(m.group(3)), mem))
print('engine orbits read: %d' % len(orbits))
for arg in sys.argv[2:]:
    pair, c2o = arg.split('=')
    l1, l2 = pair.split(',')
    for conv in ('A', 'B'):
        key = frozenset((eng(l1, conv), eng(l2, conv)))
        hit = [o for o in orbits if key in o[3]]
        if hit:
            g, size, c2, _ = hit[0]
            print('%s (convention %s: %s): engine orbit %s, size %d, c2(N=4) %.6e; pk24 c2 %s; ratio %.4f' % (
                pair, conv, ', '.join(sorted(key)), g, size, c2, c2o, c2 / float(c2o)))
        else:
            print('%s (convention %s: %s): no engine orbit lists this pair' % (pair, conv, ', '.join(sorted(key))))
