#!/usr/bin/env python3
"""make_m3ref_px22_v1_4.py (pk22, phase (iii)): writes the float twin m3ref_px22_v1_4.py from m3ref_px22_v1_3.py
(sha256 6ee3148d...), adding four P16 families that read pk22's C3_ENTRY_LIST_v2.json (list version c) as the B list is read:
P16CS4 (graph CS4 = S4's vertex graph with T1MN and W1a's joint windows JA, JD), P16CE3 (CE3 = E3T's vertex graph with fT and the joint
windows' trial components), P16CH4T (H4T) and P16CE2T (E2T); every key, dmaxH 16, qcap 6. npoly bases are the largest B with
B**F < 2**63 for the family's F: CS4 11 (F 18), CE3 15 (F 16), H4T 13 (F 17), E2T 16 (F 10). The dmaxH-12 base names (P16FAM) are
C3CS4, C3CE3, C3H4T, C3E2T, which have no base record (P16-PART none). Piece outputs m3ref_px22_v1_4_<family>.<N>.p<k>_z9sym.out in
pk22/m3/out; the P16 cache stays pk22/m3/out/tab16 (tables adopted under their keys, as v1_3). Every replacement is an exact
string with an asserted count; the output is a new file (mode 'x'). Usage: make_m3ref_px22_v1_4.py. Prints the shas."""
import hashlib, os
MYD = '/mnt/g2/release/root/code/pk22/m3'
SRC, DST, LST = MYD + '/m3ref_px22_v1_3.py', MYD + '/m3ref_px22_v1_4.py', MYD + '/C3_ENTRY_LIST_v2.json'


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
assert ssha.startswith('6ee3148d'), ssha
assert lsha.startswith('e877d12f'), lsha
FAMS = [('P16CS4', 'CS4', 11, 'C3CS4'), ('P16CE3', 'CE3', 15, 'C3CE3'), ('P16CH4T', 'H4T', 13, 'C3H4T'), ('P16CE2T', 'E2T', 16, 'C3E2T')]
names = '|'.join(f for f, g, n, p in FAMS)
t = b.decode('utf-8')
t = rep(t, '"""m3ref_px22_v1_3.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.',
        '"""m3ref_px22_v1_4.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.\n'
        'A REVISION of m3ref_px22_v1_3.py (sha256 %s) by make_m3ref_px22_v1_4.py: four families read pk22\'s\n'
        'C3_ENTRY_LIST_v2.json (sha256 %s, pinned in INPUTS_W1A, list version c): %s, at dmaxH 16 and qcap 6;\n'
        'npoly bases CS4 11, CE3 15, H4T 13, E2T 16 (the largest B with B**F < 2**63); piece outputs m3ref_px22_v1_4_*. v1_3\'s docstring follows.\n'
        'm3ref_px22_v1_3.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.'
        % (ssha, lsha, ', '.join(f for f, g, n, p in FAMS)), 1, 'K1 docstring')
t = rep(t, '|P16BN2T|P16BT1MN)\\.(4|3)\\.(all|', '|P16BN2T|P16BT1MN|%s)\\.(4|3)\\.(all|' % names, 1, 'K2 ITEM_RE')
t = rep(t, "INPUTS_W1A = {   # pk22 copy: the W1a list (pk22/m3/); v1_2: and B's list\n",
        "INPUTS_W1A = {   # pk22 copy: the W1a list (pk22/m3/); v1_2: and B's list; v1_4: and c3's list\n"
        "    'C3_ENTRY_LIST_v2.json': '%s',\n" % lsha, 1, 'K3 INPUTS_W1A')
t = rep(t, "'P16BN2T': 6, 'P16BT1MN': 6}", "'P16BN2T': 6, 'P16BT1MN': 6, %s}" % ', '.join("'%s': 6" % f for f, g, n, p in FAMS), 1, 'K4 QCAP')
t = rep(t, "'P16BN2T': 16, 'P16BT1MN': 16}", "'P16BN2T': 16, 'P16BT1MN': 16, %s}" % ', '.join("'%s': 16" % f for f, g, n, p in FAMS), 1,
        'K5 DMAXH')
t = rep(t, "'P16BT1MN': ('b', 'T1MN', r'')}   # pk22 v1_2: B\n",
        "'P16BT1MN': ('b', 'T1MN', r''),   # pk22 v1_2: B\n"
        "         %s}   # pk22 v1_4: c3\n" % ', '.join("'%s': ('c', '%s', r'')" % (f, g) for f, g, n, p in FAMS), 1, 'K6 S8FAM')
t = rep(t, "'P16BN2T': 12, 'P16BT1MN': 16}", "'P16BN2T': 12, 'P16BT1MN': 16, %s}" % ', '.join("'%s': %d" % (f, n) for f, g, n, p in FAMS), 1,
        'K7 NPB4')
t = rep(t, "            S8LIST['b'] = json.load(fh)\n",
        "            S8LIST['b'] = json.load(fh)\n"
        "        with open(os.path.join(MYD, 'C3_ENTRY_LIST_v2.json')) as fh:   # pk22 v1_4: c3's list\n"
        "            S8LIST['c'] = json.load(fh)\n", 1, 'K8 s8_lists')
t = rep(t, "'P16BT1MN': 'BT1MN'}   # pk22 v1_2: B\n",
        "'P16BT1MN': 'BT1MN',   # pk22 v1_2: B\n"
        "          %s}   # pk22 v1_4: c3\n" % ', '.join("'%s': '%s'" % (f, p) for f, g, n, p in FAMS), 1, 'K9 P16FAM')
t = rep(t, "        prev = 'm3ref_px22_v1_3_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 v1_3: its own piece outputs\n",
        "        prev = 'm3ref_px22_v1_4_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 v1_4: its own piece outputs\n", 1, 'K10 prev piece')
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (sha(nb), DST))
