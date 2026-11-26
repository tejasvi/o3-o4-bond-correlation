#!/usr/bin/env python3
"""make_c3_1_v1.py (pk22, phase (iii) step A3): writes m3_run_v1_9_3_px22_c3_1.py from m3_run_v1_9_3_px22_c3.py (sha256 505f5a61...)
by exact replacements with asserted counts, as a new file (mode 'x'). One change: CS4's smoke runs in four parts, CS4a1..CS4a4, each on
a fixed slice of CS4's entries in list order (1: entries 0..4, Z x xr xx A.JJ; 2: 5..11, A.Jx..A.Jxr; 3: 12, D.JJ; 4: 13..19,
D.Jx..D.Jxr), because the whole smoke needs about 1000 s of CPU (A.JJ and D.JJ, four insertions, about 350 s each) and an item may use
540 s. Each part runs every family-level check of the smoke (C-PARITY-SET, C-GRAPH-LIST, C-RULE, C-TILT, C-PREP-REF, C-PREP-GRAPH,
C-PREP-SHARE and their plants) and C-SMOKE-AK, PLANT-SMOKE-AK, PLANT-SMOKE-PATH, C-PACK-PLAN on its slice; the four slices cover CS4's
entries once (C-SMOKE-PARTS, checked in each part). The other families keep one smoke item. asm's C-REP-AK and C-REP-B cover every
entry as before. Prints the sha256 of the source and the output. Usage: make_c3_1_v1.py."""
import hashlib, os
D = '/mnt/g2/release/root/code/pk22/m3'
SRC, DST = D + '/m3_run_v1_9_3_px22_c3.py', D + '/m3_run_v1_9_3_px22_c3_1.py'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rep(t, old, new, count, label):
    n = t.count(old)
    assert n == count, 'replacement %s: %d occurrences, expected %d' % (label, n, count)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    return t.replace(old, new)


assert os.path.dirname(os.path.abspath(DST)) == D and not os.path.exists(DST), DST
with open(SRC, 'rb') as fh:
    b = fh.read()
ssha = sha(b)
print('SOURCE %s %s' % (ssha, SRC))
assert ssha.startswith('6df29a35'), ssha
t = b.decode('utf-8')
t = rep(t, '"""m3_run_v1_9_3_px22_c3.py -- pk22 (code/pk22/m3/). REVISION of',
        '"""m3_run_v1_9_3_px22_c3_1.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c3.py (sha256 %s) by make_c3_1_v1.py:\n'
        'CS4\'s smoke in four parts CS4a1..CS4a4 on fixed slices of its entries (SMOKE_PARTS; C-SMOKE-PARTS), since the whole smoke needs\n'
        'about 1000 s of CPU and an item may use 540 s; everything else is c3\'s. c3\'s docstring follows.\n'
        'm3_run_v1_9_3_px22_c3.py -- pk22 (code/pk22/m3/). REVISION of' % ssha, 1, 'E0 docstring')
t = rep(t, "ITEM_RE = r'((CS4|CE3|H4T|E2T)a|(CE3|E2T)p([1-9]|1[0-9])|(CS4|CE3|H4T|E2T)k[1-9]|CS4r[12]|asm)\\.(4|3)'   # c3: the c3 families\n",
        "ITEM_RE = r'(CS4a[1-4]|(CE3|H4T|E2T)a|(CE3|E2T)p([1-9]|1[0-9])|(CS4|CE3|H4T|E2T)k[1-9]|CS4r[12]|asm)\\.(4|3)'   # c3_1: CS4's smoke parts\n",
        1, 'E1 ITEM_RE')
t = rep(t, "    print('usage: m3_run_v1_9_3_px22_c3.py ITEM LIM   (ITEM = <X>a|<Y>p1..<Y>p19|<X>k1..<X>k9|CS4r1|CS4r2|asm . 4|3, X = CS4|CE3|H4T|E2T, Y = CE3|E2T; LIM = RLIMIT_CPU soft limit in s, 5..540)')\n",
        "    print('usage: m3_run_v1_9_3_px22_c3_1.py ITEM LIM   (ITEM = CS4a1..CS4a4|<Z>a|<Y>p1..<Y>p19|<X>k1..<X>k9|CS4r1|CS4r2|asm . 4|3, X = CS4|CE3|H4T|E2T, Y = CE3|E2T, Z = CE3|H4T|E2T; LIM = RLIMIT_CPU soft limit in s, 5..540)')\n",
        1, 'E2 usage')
t = rep(t, "def run_smoke(graph):\n",
        "SMOKE_PARTS = {'CS4': {1: (0, 5), 2: (5, 12), 3: (12, 13), 4: (13, 20)}}   # c3_1: entry slices [a, b) of the smoke parts\n\n\n"
        "def run_smoke(graph, part=None):\n", 1, 'E3 run_smoke head')
t = rep(t, "    refs = {d['key']: d for d in read_lines(ref_files(graph)[0], 'KEYJSON')}\n"
           "    worst, n, path, plans = (0.0, '-', 0), 0, None, []\n"
           "    for e in entries_of(graph):\n",
        "    refs = {d['key']: d for d in read_lines(ref_files(graph)[0], 'KEYJSON')}\n"
        "    worst, n, path, plans = (0.0, '-', 0), 0, None, []\n"
        "    sl = entries_of(graph)   # c3_1: the part's slice (C-SMOKE-PARTS: the parts cover the family's entries once, in order)\n"
        "    if graph in SMOKE_PARTS or part is not None:\n"
        "        cuts = sorted(SMOKE_PARTS.get(graph, {}).values())\n"
        "        okp = (part in SMOKE_PARTS.get(graph, {}) and cuts[0][0] == 0 and cuts[-1][1] == len(sl) and\n"
        "               all(cuts[j][1] == cuts[j + 1][0] for j in range(len(cuts) - 1)) and all(a_ < b_ for a_, b_ in cuts))\n"
        "        gate('C-SMOKE-PARTS', okp, '(%s smoke part %s of %s on entries [%s): the slices cover the %d entries once, in order)' % (\n"
        "            graph, part, sorted(SMOKE_PARTS.get(graph, {})), ', '.join('%d, %d' % c_ for c_ in cuts), len(sl)))\n"
        "        if not okp:\n"
        "            raise ValueError('%s smoke part %r is not a part of SMOKE_PARTS' % (graph, part))\n"
        "        a_, b_ = SMOKE_PARTS[graph][part]\n"
        "        sl = sl[a_:b_]\n"
        "    for e in sl:\n", 1, 'E4 slice')
t = rep(t, "    gate('C-SMOKE-AK', n == len(entries_of(graph)) and n > 0 and worst[0] <= 1e-9,",
        "    gate('C-SMOKE-AK', n == len(sl) and n > 0 and worst[0] <= 1e-9,", 1, 'E5 C-SMOKE-AK count')
t = rep(t, "        run_smoke(m_.group(1))\n", "        run_smoke(m_.group(1), int(m_.group(3)) if m_.group(3) else None)   # c3_1\n", 1, 'E6 dispatch')
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (sha(nb), DST))
