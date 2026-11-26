#!/usr/bin/env python3
"""make_m3ref_px22_v1_5.py (pk22, phase (iii) step A2): writes the float twin m3ref_px22_v1_5.py from m3ref_px22_v1_4.py (sha256
e78b0b67...). One change: the CPU estimate of a new disk-cached table (degree >= 13) before its budget check is 5 s plus 9e-6 s per
moment, the moment count C(D + F, F) of AllMom2 for F = the table's forms (the D-16 F-12 vertex table's rate: 262 s for 30421755
moments, rounded up), instead of v1_4's estimate by the degree alone (30, 80, 160, 320 s for D 13..16 and 900 s from D 17 on). Under
v1_4 every piece of P16CE3 at N = 4 stopped before a D-18 table on 2 forms (190 moments) with PREP-PARTIAL, 'needs about 900 s and 491 s
are left', so the family could not progress. Piece outputs m3ref_px22_v1_5_<family>.<N>.p<k>_z9sym.out. Exact replacements with asserted
counts; a new file (mode 'x'). Usage: make_m3ref_px22_v1_5.py."""
import hashlib, os
MYD = '/mnt/g2/release/root/code/pk22/m3'
SRC, DST = MYD + '/m3ref_px22_v1_4.py', MYD + '/m3ref_px22_v1_5.py'


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
assert ssha.startswith('e78b0b67'), ssha
t = b.decode('utf-8')
t = rep(t, '"""m3ref_px22_v1_4.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.',
        '"""m3ref_px22_v1_5.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.\n'
        'A REVISION of m3ref_px22_v1_4.py (sha256 %s) by make_m3ref_px22_v1_5.py: a new table\'s CPU estimate is 5 s + 9e-6 s per\n'
        'moment, C(D + F, F) moments (v1_4 estimated by D alone, 900 s from D 17 on, which stopped every piece of P16CE3 at N = 4 before a\n'
        'D-18 table on 2 forms); piece outputs m3ref_px22_v1_5_*. v1_4\'s docstring follows.\n'
        'm3ref_px22_v1_4.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.' % ssha,
        1, 'L1 docstring')
t = rep(t, "        _budget({13: 30, 14: 80, 15: 160, 16: 320}.get(D, 900), 'the D-%d table on %d forms' % (D, len(idx)))\n",
        "        _budget(5.0 + 9e-6 * math.comb(D + len(idx), len(idx)), 'the D-%d table on %d forms' % (D, len(idx)))   # pk22 v1_5: by moments\n",
        1, 'L2 table estimate')
t = rep(t, "        prev = 'm3ref_px22_v1_4_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 v1_4: its own piece outputs\n",
        "        prev = 'm3ref_px22_v1_5_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 v1_5: its own piece outputs\n", 1, 'L3 prev piece')
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (sha(nb), DST))
