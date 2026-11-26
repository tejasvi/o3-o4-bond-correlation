#!/usr/bin/env python3
"""make_m3ref_hl_v1.py (pk23, option B Pev entries on S8's L graph; the P0_LOG rows 4409, 4422, 4435; pk22's handover
HANDOVER_PEV_pk23_v1.md 13d4039c): writes the float twin pk23/pev/m3ref_hl_v1.py from pk22's m3ref_px22_v1_7.py (a7e471f2,
read-only), adding one P16 family, P16L: S8's L graph [vac, int, int, vac] as pk23's HL_ENTRY_LIST_v1.json gives it (graph L, its only
key TT,0,0), dmaxH 16, qcap 6, npoly base 11 (F 18: the largest B with B**18 < 2**63), dmaxH-12 base name HLL (no base record). The list
is read from pk23/pev and pinned in a new INPUTS_HL that C-HASH checks; every written path moves to pk23/pev/out (the P16 disk
cache out/tab16, the E2 memos, and the earlier pieces a piece reads); pk22's lists stay read where they are. Every replacement is an
exact string with an asserted count; the output is a new file (mode 'x'). Usage: make_m3ref_hl_v1.py. Prints the shas."""
import hashlib, json, os
SRCD = '/mnt/g2/release/root/code/pk22/m3'
HLD = '/mnt/g2/release/root/code/pk23/pev'
SRC, DST, LST = SRCD + '/m3ref_px22_v1_7.py', HLD + '/m3ref_hl_v1.py', HLD + '/HL_ENTRY_LIST_v1.json'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rep(t, old, new, count, label):
    n = t.count(old)
    assert n == count, 'replacement %s: %d occurrences, expected %d' % (label, n, count)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    return t.replace(old, new)


def npb(F):
    B = 2
    while (B + 1) ** F < 2 ** 63:
        B += 1
    assert B ** F < 2 ** 63 <= (B + 1) ** F
    return B


assert os.path.dirname(os.path.abspath(DST)) == HLD and not os.path.exists(DST), DST
with open(SRC, 'rb') as fh:
    b = fh.read()
with open(LST, 'rb') as fh:
    lraw = fh.read()
ssha, lsha = sha(b), sha(lraw)
print('SOURCE %s %s' % (ssha, SRC))
print('LIST %s %s' % (lsha, LST))
assert ssha.startswith('a7e471f2'), ssha
lst = json.loads(lraw)
V, E, F = lst['graphs']['L']['shape_V_edges_F']
NPB = npb(F)
assert (V, E, F, NPB) == (12, 19, 18, 11), (V, E, F, NPB)
keys = [e['key'] for e in lst['entries'] if e['graph'] == 'L']
assert keys == ['TT,0,0'], keys
print('FAMILY P16L graph L V %d edges %d F %d npoly base %d keys %s' % (V, E, F, NPB, keys))
t = b.decode('utf-8')
t = rep(t, '"""m3ref_px22_v1_7.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.\n',
        '"""m3ref_hl_v1.py -- pk23 (code/pk23/pev/). FLOAT twin for the option B Pev entries on S8\'s L graph. Nothing here is certified.\n'
        'A COPY of pk22\'s m3ref_px22_v1_7.py (sha256 %s) by pk23\'s make_m3ref_hl_v1.py: one P16 family P16L (graph L of\n'
        'pk23/pev/HL_ENTRY_LIST_v1.json, sha256 %s, pinned in INPUTS_HL, list version hl; key TT,0,0; dmaxH 16, qcap 6, npoly base %d);\n'
        'every written path in pk23/pev/out (the P16 cache out/tab16, the E2 memos, the earlier pieces); piece outputs m3ref_hl_v1_*.\n'
        'm3ref_px22_v1_7\'s docstring follows.\n'
        'm3ref_px22_v1_7.py -- pk22 (code/pk22/m3/). FLOAT reference for B\'s and W1a\'s M3 windows. Nothing here is certified.\n'
        % (ssha, lsha, NPB), 1, 'H1 docstring')
t = rep(t, '|P16E4D|P16E4N)\\.(4|3)\\.(all|', '|P16E4D|P16E4N|P16L)\\.(4|3)\\.(all|', 1, 'H2 ITEM_RE')
t = rep(t, "MYD = '/mnt/g2/release/root/code/pk22/m3'   # pk22 copy: its list and the P16 cache and outputs\n",
        "MYD = '/mnt/g2/release/root/code/pk22/m3'   # pk22 copy: its list and the P16 cache and outputs\n"
        "HLD = '/mnt/g2/release/root/code/pk23/pev'   # pk23 hl_v1: the L list, the P16 cache, the memos, the pieces\n",
        1, 'H3 HLD')
t = rep(t, "INPUTS_S8 = {\n",
        "INPUTS_HL = {   # pk23 hl_v1: the L list (pk23/pev/)\n    'HL_ENTRY_LIST_v1.json': '%s',\n}\nINPUTS_S8 = {\n" % lsha,
        1, 'H4 INPUTS_HL')
t = rep(t, "bad += [f for f, h in INPUTS_PSX.items() if sha(read_bytes(os.path.join(os.path.dirname(MYD), 'midrow', 'psixy', f))) != h]   # pk22 v1_7\n",
        "bad += [f for f, h in INPUTS_PSX.items() if sha(read_bytes(os.path.join(os.path.dirname(MYD), 'midrow', 'psixy', f))) != h]   # pk22 v1_7\n"
        "bad += [f for f, h in INPUTS_HL.items() if sha(read_bytes(os.path.join(HLD, f))) != h]   # pk23 hl_v1\n", 1, 'H5 C-HASH')
t = rep(t, "'P16E4D': 6, 'P16E4N': 6}", "'P16E4D': 6, 'P16E4N': 6, 'P16L': 6}", 1, 'H6 QCAP')
t = rep(t, "'P16E4D': 16, 'P16E4N': 16}", "'P16E4D': 16, 'P16E4N': 16, 'P16L': 16}", 1, 'H7 DMAXH')
t = rep(t, "'P16E4D': ('c3k', 'E4D', r''), 'P16E4N': ('c3k', 'E4N', r'')}   # pk22 v1_7: c3k\n",
        "'P16E4D': ('c3k', 'E4D', r''), 'P16E4N': ('c3k', 'E4N', r''),   # pk22 v1_7: c3k\n"
        "         'P16L': ('hl', 'L', r'')}   # pk23 hl_v1: S8's L graph from pk23's list\n", 1, 'H8 S8FAM')
t = rep(t, "'P16E4D': 28, 'P16E4N': 13}", "'P16E4D': 28, 'P16E4N': 13, 'P16L': %d}" % NPB, 1, 'H9 NPB4')
t = rep(t, "'P16E4D': 'C3KE4D', 'P16E4N': 'C3KE4N'}   # pk22 v1_7: c3k\n",
        "'P16E4D': 'C3KE4D', 'P16E4N': 'C3KE4N',   # pk22 v1_7: c3k\n          'P16L': 'HLL'}   # pk23 hl_v1\n", 1, 'H10 P16FAM')
t = rep(t, "            S8LIST['c3k'] = json.load(fh)\n",
        "            S8LIST['c3k'] = json.load(fh)\n"
        "        with open(os.path.join(HLD, 'HL_ENTRY_LIST_v1.json')) as fh:   # pk23 hl_v1: the L list\n"
        "            S8LIST['hl'] = json.load(fh)\n", 1, 'H11 s8_lists')
t = rep(t, "TABD = os.path.join(MYD, 'out', 'tab16')   # pk22 copy\n",
        "TABD = os.path.join(HLD, 'out', 'tab16')   # pk23 hl_v1\n", 1, 'H12 TABD')
t = rep(t, "    P16['memo_path'] = os.path.join(MYD, 'out', 's16memo_%s_N%d.jsonl' % (FAM, NN))   # pk22 copy\n",
        "    P16['memo_path'] = os.path.join(HLD, 'out', 's16memo_%s_N%d.jsonl' % (FAM, NN))   # pk23 hl_v1\n", 1, 'H13 memo path')
t = rep(t, "        prev = 'm3ref_px22_v1_7_%s.%d.p%d_%s.out' % (FAM, NN, k - 1, TRIAL)   # pk22 v1_7: its own piece outputs, same TRIAL\n",
        "        prev = 'm3ref_hl_v1_%s.%d.p%d_%s.out' % (FAM, NN, k - 1, TRIAL)   # pk23 hl_v1: its own piece outputs, same TRIAL\n",
        1, 'H14 prev piece name')
t = rep(t, "        lines = read_bytes(os.path.join(MYD, 'out', prev)).decode('utf-8').split('\\n')\n",
        "        lines = read_bytes(os.path.join(HLD, 'out', prev)).decode('utf-8').split('\\n')   # pk23 hl_v1\n", 1, 'H15 prev piece path')
assert "os.path.join(MYD, 'out'" not in t, 'a written path still under MYD'
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (sha(nb), DST))
