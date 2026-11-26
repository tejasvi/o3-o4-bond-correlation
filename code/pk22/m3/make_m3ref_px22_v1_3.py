#!/usr/bin/env python3
"""make_m3ref_px22_v1_3.py (pk22, B): writes m3ref_px22_v1_3.py from m3ref_px22_v1_2.py (sha256 f0b36284...). One change: the P16 disk
cache adopts a table file that already exists under the table's own key (_tab_id: the graph, n, the forms and the degree) but is not yet
in this family's memo chain, after recording its sha256 and size, instead of failing on the 'xb' save. Such a file was built by the same
code under the same key, by another family on the same vertex graph (B's E2T, E3T and T1MN share T1's, T2's and T2n's graphs) or copied
from pk03's cache (the same m3ref_v1_15 code). The memo chain then checks it like any recorded table. Piece outputs are named
m3ref_px22_v1_3_<family>.<N>.p<k>_z9sym.out. Exact replacements with asserted counts; a new file (mode 'x')."""
import hashlib, os
MYD = '/mnt/g2/release/root/code/pk22/m3'
SRC, DST = MYD + '/m3ref_px22_v1_2.py', MYD + '/m3ref_px22_v1_3.py'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rep(t, old, new, count, label):
    n = t.count(old)
    assert n == count, 'replacement %s: %d occurrences, expected %d' % (label, n, count)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    return t.replace(old, new)


assert os.path.dirname(os.path.abspath(DST)) == MYD and not os.path.exists(DST), DST
with open(SRC, 'rb') as fh:
    b = fh.read()
ssha = sha(b)
print('SOURCE %s %s' % (ssha, SRC))
assert ssha.startswith('f0b36284'), ssha
t = b.decode('utf-8')
t = rep(t, '"""m3ref_px22_v1_2.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.',
        '"""m3ref_px22_v1_3.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.\n'
        'A REVISION of m3ref_px22_v1_2.py (sha256 %s) by make_m3ref_px22_v1_3.py: the P16 disk cache adopts an existing table file under\n'
        'its own key (TABLE-ADOPTED, sha256 and size recorded in the memo chain); piece outputs m3ref_px22_v1_3_*. v1_2\'s docstring follows.\n'
        'm3ref_px22_v1_2.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.' % ssha,
        1, 'H1 docstring')
t = rep(t, "    tid = _tab_id(G, n, Wi, D, None, None)\n    if tid in P16['tables']:\n        am = _load_table(tid)\n",
        "    tid = _tab_id(G, n, Wi, D, None, None)\n"
        "    pth_ = os.path.join(TABD, tid + '.npz')\n"
        "    if tid not in P16['tables'] and os.path.exists(pth_):   # v1_3: adopt the file built under the same key (another family, or a copy)\n"
        "        P16['tables'][tid] = [os.path.basename(pth_), _file_sha(pth_), os.path.getsize(pth_)]\n"
        "        out('TABLE-ADOPTED %s: sha256 %s, %d bytes (the same key; built by another family or copied)' % (\n"
        "            os.path.basename(pth_), P16['tables'][tid][1], P16['tables'][tid][2]))\n"
        "    if tid in P16['tables']:\n        am = _load_table(tid)\n", 1, 'H2 adopt')
t = rep(t, "        prev = 'm3ref_px22_v1_2_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 v1_2: its own piece outputs\n",
        "        prev = 'm3ref_px22_v1_3_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 v1_3: its own piece outputs\n", 1, 'H3 prev piece')
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (sha(nb), DST))
