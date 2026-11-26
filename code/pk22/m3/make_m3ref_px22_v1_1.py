#!/usr/bin/env python3
"""make_m3ref_px22_v1_1.py (pk22, W1a): writes pk22's float twin m3ref_px22_v1_1.py from pk03's m3ref_v1_15.py (read only):
the P16 staged probe (m3ref_v1_14) with the xia factor (m3ref_v1_15), plus four families P16T1, P16T1N, P16T2, P16T2N that read
pk22's W1A_ENTRY_LIST_v2.json as S8's lists are read (graphs T1, T1n, T2, T2n; dmaxH 16, qcap 6, npoly base 16). The P16 cache
(out/tab16, the s16memo files) and the chain of piece outputs move to pk22/m3/out; p16_done skips the dmaxH-12 comparison for a
family without a base record. Every other path (the pinned riglap stack in pk03/pin, the lists, the records) is read where
m3ref_v1_15 reads it. Every replacement is an exact string with an asserted count; the output is a new file (mode 'x') in pk22/m3/.
Usage: make_m3ref_px22_v1_1.py (no arguments). Prints the source and output sha256 and the list's sha256."""
import hashlib, os
CODEDIR = '/mnt/g2/release/root/code'
SRC = CODEDIR + '/pk03/m3ref_v1_15.py'
MYD = CODEDIR + '/pk22/m3'
DST = MYD + '/m3ref_px22_v1_1.py'
LST = MYD + '/W1A_ENTRY_LIST_v2.json'


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
assert ssha.startswith('12a445c8'), ssha   # the sha8 that m3ref_v1_16's docstring cites for m3ref_v1_15
t = b.decode('utf-8')
t = rep(t, '"""m3ref_v1_15.py -- pk03 (code/pk03/). FLOAT reference for M3. Nothing here is certified.',
        '"""m3ref_px22_v1_1.py -- pk22 (code/pk22/m3/). FLOAT reference for W1a\'s M3 windows. Nothing here is certified.\n'
        'A COPY of pk03/m3ref_v1_15.py (sha256 %s), made by pk22/m3/make_m3ref_px22_v1_1.py, with four families added:\n'
        '  P16T1, P16T1N, P16T2, P16T2N  the graphs T1 [vac|free], T1n [free|free], T2 [vac|int|free] and T2n [free|int|int|free] of\n'
        '  pk22\'s W1A_ENTRY_LIST_v2.json (sha256 %s, pinned in INPUTS_W1A and read as list version w1a), every key of each graph,\n'
        '  as m3ref_v1_14\'s staged P16 probe at dmaxH 16 (qcap 6, npoly base 16; [xia, [u, v, v]] is m3ref_v1_15\'s xia factor);\n'
        'the P16 disk cache (out/tab16), the E2 memos (out/s16memo_<family>_N<N>.jsonl) and the chain of piece outputs\n'
        '(out/m3ref_px22_v1_1_<family>.<N>.p<k>_z9sym.out) are in pk22/m3/out; p16_done prints P16-PART none for a family without a\n'
        'dmaxH-12 base record. Every other input is read where m3ref_v1_15 reads it. pk03\'s docstring follows.\n'
        'm3ref_v1_15.py -- pk03 (code/pk03/). FLOAT reference for M3. Nothing here is certified.' % (ssha, lsha), 1, 'F1 docstring')
t = rep(t, 'V4F3|V9I)\\.(4|3)\\.(all|', 'V4F3|V9I|P16T1|P16T1N|P16T2|P16T2N)\\.(4|3)\\.(all|', 1, 'F2 ITEM_RE')
t = rep(t, "OWN = '/mnt/g2/release/root/code/pk03'\n",
        "OWN = '/mnt/g2/release/root/code/pk03'\n"
        "MYD = '/mnt/g2/release/root/code/pk22/m3'   # pk22 copy: its list and the P16 cache and outputs\n", 1, 'F3 MYD')
t = rep(t, "    'S9_ENTRY_LIST_v1.json': '50beb53e74fe42aab6d5c889734fd91a04570ea69b2188fdd8ddf2379107de4e',\n}\n",
        "    'S9_ENTRY_LIST_v1.json': '50beb53e74fe42aab6d5c889734fd91a04570ea69b2188fdd8ddf2379107de4e',\n}\n"
        "INPUTS_W1A = {   # pk22 copy: the W1a list (pk22/m3/)\n    'W1A_ENTRY_LIST_v2.json': '%s',\n}\n" % lsha, 1, 'F4 INPUTS_W1A')
t = rep(t, "bad += [f for f, h in INPUTS_S9.items() if sha(read_bytes(os.path.join(OWN, f))) != h]\n",
        "bad += [f for f, h in INPUTS_S9.items() if sha(read_bytes(os.path.join(OWN, f))) != h]\n"
        "bad += [f for f, h in INPUTS_W1A.items() if sha(read_bytes(os.path.join(MYD, f))) != h]   # pk22 copy\n", 1, 'F5 C-HASH')
t = rep(t, "        'V4NK': 6, 'V4E3K': 6, 'V4F3': 6, 'V9I': 6}",
        "        'V4NK': 6, 'V4E3K': 6, 'V4F3': 6, 'V9I': 6, 'P16T1': 6, 'P16T1N': 6, 'P16T2': 6, 'P16T2N': 6}", 1, 'F6 QCAP')
t = rep(t, "'P16H': 16, 'P16S4': 16, 'S8Hc': 12, 'S8S4c': 12}",
        "'P16H': 16, 'P16S4': 16, 'S8Hc': 12, 'S8S4c': 12, 'P16T1': 16, 'P16T1N': 16, 'P16T2': 16, 'P16T2N': 16}", 1, 'F7 DMAXH')
t = rep(t, "         'V9I': ('s9', 'I9', r'')}\n",
        "         'V9I': ('s9', 'I9', r''),\n"
        "         'P16T1': ('w1a', 'T1', r''), 'P16T1N': ('w1a', 'T1n', r''), 'P16T2': ('w1a', 'T2', r''), 'P16T2N': ('w1a', 'T2n', r'')}   # pk22\n",
        1, 'F8 S8FAM')
t = rep(t, "'V4F3': 16, 'V9I': 15}", "'V4F3': 16, 'V9I': 15, 'P16T1': 16, 'P16T1N': 16, 'P16T2': 16, 'P16T2N': 16}", 1, 'F9 NPB4')
t = rep(t, "            S8LIST['s9'] = json.load(fh)\n",
        "            S8LIST['s9'] = json.load(fh)\n"
        "        with open(os.path.join(MYD, 'W1A_ENTRY_LIST_v2.json')) as fh:   # pk22 copy\n"
        "            S8LIST['w1a'] = json.load(fh)\n", 1, 'F10 s8_lists')
t = rep(t, "P16FAM = {'P16H': 'S8H', 'P16S4': 'S8S4'}\nTABD = os.path.join(OWN, 'out', 'tab16')\n",
        "P16FAM = {'P16H': 'S8H', 'P16S4': 'S8S4', 'P16T1': 'T1', 'P16T1N': 'T1n', 'P16T2': 'T2', 'P16T2N': 'T2n'}   # pk22: + W1a\n"
        "TABD = os.path.join(MYD, 'out', 'tab16')   # pk22 copy\n", 1, 'F11 P16FAM TABD')
t = rep(t, "    P16['memo_path'] = os.path.join(OWN, 'out', 's16memo_%s_N%d.jsonl' % (FAM, NN))\n",
        "    P16['memo_path'] = os.path.join(MYD, 'out', 's16memo_%s_N%d.jsonl' % (FAM, NN))   # pk22 copy\n", 1, 'F12 memo')
t = rep(t, "        prev = 'm3ref_v1_14_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)\n"
           "        lines = read_bytes(os.path.join(OWN, 'out', prev)).decode('utf-8').split('\\n')\n",
        "        prev = 'm3ref_px22_v1_1_%s.%d.p%d_z9sym.out' % (FAM, NN, k - 1)   # pk22 copy: its own piece outputs\n"
        "        lines = read_bytes(os.path.join(MYD, 'out', prev)).decode('utf-8').split('\\n')\n", 1, 'F13 prev piece')
t = rep(t, "    fn = '%s.%d.all_z9sym.out' % (REF16BASE[FAM], NN)\n"
           "    text = read_bytes(os.path.join(OWN, 'out', fn))\n"
           "    if sha(text) == REF16BASE_SHA[fn]:\n",
        "    fn = ('%s.%d.all_z9sym.out' % (REF16BASE[FAM], NN)) if FAM in REF16BASE else None   # pk22 copy\n"
        "    text = read_bytes(os.path.join(OWN, 'out', fn)) if fn else b''\n"
        "    if fn is None:\n"
        "        out('P16-PART none (%s has no dmaxH-12 base record)' % FAM)\n"
        "    elif sha(text) == REF16BASE_SHA[fn]:\n", 1, 'F14 p16_done')
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (sha(nb), DST))
