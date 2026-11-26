#!/usr/bin/env python3
"""make_m3ref_px22_v1_2.py (pk22, B under the row 3701): writes pk22's float twin m3ref_px22_v1_2.py from its
m3ref_px22_v1_1.py (sha256 a7ba24e9...), adding seven P16 families that read pk22's B_ENTRY_LIST_v1.json (list version b) as S8's
lists are read: P16BD2T, P16BE2T, P16BE3T, P16BH4T, P16BL, P16BN2T, P16BT1MN (graphs D2T, E2T, E3T, H4T, L, N2T, T1MN; every key; dmaxH
16, qcap 6). npoly bases follow the vertex graphs' precedents: T1MN 16 (as P16T2N on S4's graph), H4T 15 (as P16H), L 11 (as S8L16),
N2T 12 (L's graph with one xi), E3T 16 (as P16T2, the same columns), E2T 16 (as P16T1), D2T 16. Piece outputs are
m3ref_px22_v1_2_<family>.<N>.p<k>_z9sym.out in pk22/m3/out, the P16 cache stays pk22/m3/out/tab16. Every replacement is an
exact string with an asserted count; the output is a new file (mode 'x'). Usage: make_m3ref_px22_v1_2.py. Prints the shas."""
import hashlib, os
MYD = '/mnt/g2/release/root/code/pk22/m3'
SRC, DST, LST = MYD + '/m3ref_px22_v1_1.py', MYD + '/m3ref_px22_v1_2.py', MYD + '/B_ENTRY_LIST_v1.json'


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
with open(LST, 'rb') as fh:
    lsha = sha(fh.read())
ssha = sha(b)
print('SOURCE %s %s' % (ssha, SRC))
print('LIST %s %s' % (lsha, LST))
assert ssha.startswith('a7ba24e9'), ssha
assert lsha.startswith('efc0b7cb'), lsha
FAMS = [('P16BD2T', 'D2T', 16), ('P16BE2T', 'E2T', 16), ('P16BE3T', 'E3T', 16), ('P16BH4T', 'H4T', 15), ('P16BL', 'L', 11),
        ('P16BN2T', 'N2T', 12), ('P16BT1MN', 'T1MN', 16)]
names = '|'.join(f for f, g, n in FAMS)
t = b.decode('utf-8')
t = rep(t, '"""m3ref_px22_v1_1.py -- pk22 (code/pk22/m3/). FLOAT reference for W1a\'s M3 windows. Nothing here is certified.',
        '"""m3ref_px22_v1_2.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.\n'
        'A REVISION of m3ref_px22_v1_1.py (sha256 %s), made by pk22/m3/make_m3ref_px22_v1_2.py: seven families read pk22\'s\n'
        'B_ENTRY_LIST_v1.json (sha256 %s, pinned in INPUTS_W1A, list version b): %s, at dmaxH 16 and qcap 6, as\n'
        'm3ref_v1_14\'s staged P16 probe; piece outputs m3ref_px22_v1_2_<family>.<N>.p<k>_z9sym.out. v1_1\'s docstring follows.\n'
        'm3ref_px22_v1_1.py -- pk22 (code/pk22/m3/). FLOAT reference for W1a\'s M3 windows. Nothing here is certified.'
        % (ssha, lsha, ', '.join(f for f, g, n in FAMS)), 1, 'G1 docstring')
t = rep(t, 'V4F3|V9I|P16T1|P16T1N|P16T2|P16T2N)\\.(4|3)\\.(all|', 'V4F3|V9I|P16T1|P16T1N|P16T2|P16T2N|%s)\\.(4|3)\\.(all|' % names, 1,
        'G2 ITEM_RE')
t = rep(t, "INPUTS_W1A = {   # pk22 copy: the W1a list (pk22/m3/)\n",
        "INPUTS_W1A = {   # pk22 copy: the W1a list (pk22/m3/); v1_2: and B's list\n"
        "    'B_ENTRY_LIST_v1.json': '%s',\n" % lsha, 1, 'G3 INPUTS_W1A')
t = rep(t, "'V4F3': 6, 'V9I': 6, 'P16T1': 6, 'P16T1N': 6, 'P16T2': 6, 'P16T2N': 6}",
        "'V4F3': 6, 'V9I': 6, 'P16T1': 6, 'P16T1N': 6, 'P16T2': 6, 'P16T2N': 6, %s}" % ', '.join("'%s': 6" % f for f, g, n in FAMS), 1,
        'G4 QCAP')
t = rep(t, "'S8Hc': 12, 'S8S4c': 12, 'P16T1': 16, 'P16T1N': 16, 'P16T2': 16, 'P16T2N': 16}",
        "'S8Hc': 12, 'S8S4c': 12, 'P16T1': 16, 'P16T1N': 16, 'P16T2': 16, 'P16T2N': 16, %s}" % ', '.join("'%s': 16" % f for f, g, n in FAMS),
        1, 'G5 DMAXH')
t = rep(t, "'P16T2': ('w1a', 'T2', r''), 'P16T2N': ('w1a', 'T2n', r'')}   # pk22\n",
        "'P16T2': ('w1a', 'T2', r''), 'P16T2N': ('w1a', 'T2n', r''),   # pk22\n"
        "         %s}   # pk22 v1_2: B\n" % ', '.join("'%s': ('b', '%s', r'')" % (f, g) for f, g, n in FAMS), 1, 'G6 S8FAM')
t = rep(t, "'V4F3': 16, 'V9I': 15, 'P16T1': 16, 'P16T1N': 16, 'P16T2': 16, 'P16T2N': 16}",
        "'V4F3': 16, 'V9I': 15, 'P16T1': 16, 'P16T1N': 16, 'P16T2': 16, 'P16T2N': 16, %s}" % ', '.join("'%s': %d" % (f, n) for f, g, n in FAMS),
        1, 'G7 NPB4')
t = rep(t, "            S8LIST['w1a'] = json.load(fh)\n",
        "            S8LIST['w1a'] = json.load(fh)\n"
        "        with open(os.path.join(MYD, 'B_ENTRY_LIST_v1.json')) as fh:   # pk22 v1_2: B's list\n"
        "            S8LIST['b'] = json.load(fh)\n", 1, 'G8 s8_lists')
t = rep(t, "P16FAM = {'P16H': 'S8H', 'P16S4': 'S8S4', 'P16T1': 'T1', 'P16T1N': 'T1n', 'P16T2': 'T2', 'P16T2N': 'T2n'}   # pk22: + W1a\n",
        "P16FAM = {'P16H': 'S8H', 'P16S4': 'S8S4', 'P16T1': 'T1', 'P16T1N': 'T1n', 'P16T2': 'T2', 'P16T2N': 'T2n',   # pk22: + W1a\n"
        "          %s}   # pk22 v1_2: B\n" % ', '.join("'%s': 'B%s'" % (f, g) for f, g, n in FAMS), 1, 'G9 P16FAM')
t = rep(t, "        prev = 'm3ref_px22_v1_1_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 copy: its own piece outputs\n",
        "        prev = 'm3ref_px22_v1_2_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 v1_2: its own piece outputs\n", 1, 'G10 prev piece')
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (sha(nb), DST))
