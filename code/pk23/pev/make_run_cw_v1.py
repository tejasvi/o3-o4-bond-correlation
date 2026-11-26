#!/usr/bin/env python3
"""make_run_cw_v1.py (pk23, C_w variant B; the P0_LOG row 4589, pk25's D2_DESIGN_v1_3): writes pk23/pev/m3_run_v1_9_3_cw_v1.py from
pk23's frozen Pev runner m3_run_v1_9_3_hl_v1.py (2c81e6bc), for the family LC of pk23/pev/HL_CW_ENTRY_LIST_v1.json (the (1,1) block of
|S M_c u~_x|^2 on S8's L graph with the pairs (0,2), (9,11), (1,4), (7,10)). Changes, each an exact string or line with an asserted count:
the list; FAMS (LC); EDGES (also L, for PLANT-ODD on L); PREPOF LC -> L, read from the certified L prep pieces Lp1.. that m3_run_v1_9_3_hl_v1
produced (item_sha names it for the Lp items, pinned in INPUTS as HL1_SHA); FAMREF, KEYFAM, KEYREF (rtwin_cw_v1's outputs, pinned); PFX;
ITEM_RE, usage and dispatch (items LCa, LCk1.., LCr1, LCr2, asmc, so no name meets the frozen Pev outputs); RESUME on LC's Cx1,1,1;
C-SMOKE-AK and C-REP texts; PLANT-SCOPE and the reader plants on LC; records m3_cw_<G>_N<N>_J300_cw.json; the docstring's new head.
The hand-off module copy m3_handoff_v3_hl.py and the folders (pk23/pev/out, pk23/pev/hand) stay hl_v1's. The output is a new file
(mode 'x'). Usage: make_run_cw_v1.py (after rtwin_cw_v1's two outputs exist). Prints the shas."""
import hashlib, os, re, sys
W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
SRC, DST = HLD + '/m3_run_v1_9_3_hl_v1.py', HLD + '/m3_run_v1_9_3_cw_v1.py'
LISTF = 'HL_CW_ENTRY_LIST_v1.json'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sha_path(p):
    with open(p, 'rb') as fh:
        return sha(fh.read())


def rep(t, old, new, count, label):
    n = t.count(old)
    assert n == count, 'replacement %s: %d occurrences, expected %d' % (label, n, count)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    return t.replace(old, new)


def rep_line(t, prefix, new, label):
    lines = t.split('\n')
    idx = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
    assert len(idx) == 1, 'line %s: %d lines start with %r' % (label, len(idx), prefix)
    lines[idx[0]] = new
    print('REPLACE-LINE %s: line %d' % (label, idx[0] + 1))
    return '\n'.join(lines)


assert len(sys.argv) == 1, 'usage: make_run_cw_v1.py'
assert os.path.dirname(os.path.abspath(DST)) == HLD and not os.path.exists(DST), DST
b = open(SRC, 'rb').read()
assert sha(b).startswith('57f73e77'), sha(b)
print('SOURCE %s %s' % (sha(b), SRC))
mine = [('HLD', LISTF), ('HLD', 'rtwin_cw_v1.py'), ('HLD', 'm3_run_v1_9_3_hl_v1.py'),
        ('OUTD', 'rtwin_cw_v1_LC.4_z9sym.out'), ('OUTD', 'rtwin_cw_v1_LC.3_z9sym.out')]
pins = []
for root, name in mine:
    path = os.path.join(HLD if root == 'HLD' else HLD + '/out', name)
    h = sha_path(path)
    pins.append("    (%s, %r): %r,   # pk23 cw_v1" % (root, name, h))
    print('PIN %s %s' % (h, path))
assert sha_path(os.path.join(HLD, LISTF)).startswith('93b417e7')
assert sha_path(os.path.join(HLD, 'rtwin_cw_v1.py')).startswith('f4958e47')

t = b.decode('utf-8')
t = rep(t, '"""m3_run_v1_9_3_hl_v1.py -- pk23 (code/pk23/pev/): a COPY of', (
    '"""m3_run_v1_9_3_cw_v1.py -- pk23 (code/pk23/pev/): pk23\'s Pev runner m3_run_v1_9_3_hl_v1.py (sha256 %s) made over by\n'
    'pk23\'s make_run_cw_v1.py for C_w variant B (the P0_LOG row 4589, pk25\'s D2_DESIGN_v1_3): the list HL_CW_ENTRY_LIST_v1.json, one\n'
    'family LC (S8\'s L graph with the pairs (0,2), (9,11), (1,4), (7,10); the (1,1) block Cxx,1,1, Cx1,1,1, C1x,1,1, C11,1,1 of |S M_c u~_x|^2),\n'
    'which reads the certified L prep pieces Lp1.. that m3_run_v1_9_3_hl_v1 produced (item_sha; HL1_SHA pinned); references rtwin_cw_v1 (restored\n'
    'prep); items LCa, LCk1.., LCr1, LCr2 (C-RESUME on Cx1,1,1) and asmc; PLANT-ODD on L; PLANT-SCOPE and the reader plants on LC\'s record;\n'
    'records m3_cw_<G>_N<N>_J300_cw.json; written paths in pk23/pev/out and pk23/pev/hand, as hl_v1.\n'
    'm3_run_v1_9_3_hl_v1.py was: a COPY of') % sha(b), 1, 'R1 docstring')
t = rep_line(t, "ITEM_RE = r'((L|LH|LT)a|Lp(",
             "ITEM_RE = r'(LCa|LCk[1-9]|LCr[12]|asmc)\\.(4|3)'   # pk23 cw_v1: LC's smoke, entry pieces, resume items and asmc (L's prep pieces are hl_v1's)", 'R2 ITEM_RE')
t = rep_line(t, "    print('usage: m3_run_v1_9_3_hl_v1.py ITEM LIM",
             "    print('usage: m3_run_v1_9_3_cw_v1.py ITEM LIM   (ITEM = LCa|LCk1..LCk9|LCr1|LCr2|asmc . 4|3; LIM = RLIMIT_CPU soft limit in s, 5..540)')", 'R3 usage')
last = "    (OUTD, 'rtwin_hl_v1_LT.3_z9sym.out'): '838d442af63ed6857361347c190271ef5a7a52fb5994029ce6bed1f961e9d70f',   # pk23 hl_v1\n"
t = rep(t, last, last + '\n'.join(pins) + '\n', 1, 'R4 INPUTS')
t = rep_line(t, "LISTF = 'HL_ENTRY_LIST_v1.json'", "LISTF = '%s'   # pk23 cw_v1: pk23's C_w list (pinned in INPUTS under HLD)" % LISTF, 'R5 LISTF')
t = rep_line(t, "FAMS = ('L', 'LH', 'LT')", "FAMS = ('LC',)   # pk23 cw_v1: the C_w list's one computed family", 'R6 FAMS')
t = rep_line(t, "EDGES = {g: 'N' for g in FAMS}", "EDGES = {g: 'N' for g in FAMS + ('L',)}   # pk23 cw_v1: L too, for PLANT-ODD on L (m3_entries_v3.factor's column lookup)", 'R7 EDGES')
t = rep_line(t, "PREPOF = {'L': 'L', 'LH': 'L', 'LT': 'L'}", "PREPOF = {'LC': 'L'}   # pk23 cw_v1: LC reads L's certified prep (pieces Lp1.. of m3_run_v1_9_3_hl_v1)", 'R8 PREPOF')
t = rep_line(t, "FAMREF = {'L': 'P16L', 'LH': 'P16L', 'LT': 'P16L'}", "FAMREF = {'LC': 'P16L'}   # pk23 cw_v1: the twin m3ref_hl_v1's P16L PREPJSON", 'R9 FAMREF')
t = rep_line(t, "KEYFAM = {'L': 'P16L', 'LH': 'P16LH', 'LT': 'P16LT'}", "KEYFAM = {'LC': 'P16LC'}   # pk23 cw_v1: the family name of rtwin_cw_v1's KEYJSON", 'R10 KEYFAM')
t = rep_line(t, "KEYREF = dict((g, 'rtwin_hl_v1_%s.%d_z9sym.out' % (g, NN)) for g in FAMS)",
             "KEYREF = dict((g, 'rtwin_cw_v1_%s.%d_z9sym.out' % (g, NN)) for g in FAMS)   # pk23 cw_v1: rtwin_cw_v1's references (restored prep; pinned)", 'R11 KEYREF')
t = rep_line(t, "PFX = {'L': 'L', 'LH': 'LH', 'LT': 'LT',", "PFX = {'L': 'L', 'LC': 'LC', 'CE3': 'CE3', 'S4': 'S4', 'H': 'H'}   # item prefixes (pk23 cw_v1: L for the prep pieces, LC)", 'R12 PFX')
t = rep_line(t, "RESUME_FAMS = ('LH',)", "RESUME_FAMS = ('LC',)   # pk23 cw_v1: the family with the items LCr1, LCr2", 'R13 RESUME_FAMS')
t = rep_line(t, "RESUME_KEY = {'LH': 'Mh,0,0'}", "RESUME_KEY = {'LC': 'Cx1,1,1'}   # C-RESUME's entry (pk23 cw_v1)", 'R14 RESUME_KEY')
t = rep(t, "C31_SHA = INPUTS[(MYD, 'm3_run_v1_9_3_px22_c3_1.py')]",
        "HL1_SHA = INPUTS[(HLD, 'm3_run_v1_9_3_hl_v1.py')]   # pk23 cw_v1: the producer of L's prep pieces Lp1..\n"
        "C31_SHA = INPUTS[(MYD, 'm3_run_v1_9_3_px22_c3_1.py')]", 1, 'R15 HL1_SHA')
t = rep(t, "    if re.fullmatch(r'CE3p[0-9]+\\.[34]', item):\n        return C31_SHA\n    return SELF_SHA\n",
        "    if re.fullmatch(r'CE3p[0-9]+\\.[34]', item):\n        return C31_SHA\n"
        "    if re.fullmatch(r'Lp[0-9]+\\.[34]', item):   # pk23 cw_v1: L's prep pieces are m3_run_v1_9_3_hl_v1's\n        return HL1_SHA\n"
        "    return SELF_SHA\n", 1, 'R16 item_sha')
t = rep(t, 'against rtwin_hl_v1 %s (restored prep)', 'against rtwin_cw_v1 %s (restored prep)', 1, 'R17 C-SMOKE-AK text')
t = rep(t, 'against rtwin_hl_v1 (restored prep) z9sym', 'against rtwin_cw_v1 (restored prep) z9sym', 2, 'R18 C-REP texts')
t = rep(t, "plant('PLANT-SCOPE', not (set(list(files['LH'])[1:]) == want['LH']), '(LH without one key)')   # pk23 hl_v1",
        "plant('PLANT-SCOPE', not (set(list(files['LC'])[1:]) == want['LC']), '(LC without one key)')   # pk23 cw_v1", 1, 'R19 PLANT-SCOPE')
t = rep(t, "paths[g] = os.path.join(OUTD, 'm3_hl_%s_N%d_J300%s_hl.json' % (g, NN, tag))   # pk23 hl_v1",
        "paths[g] = os.path.join(OUTD, 'm3_cw_%s_N%d_J300%s_cw.json' % (g, NN, tag))   # pk23 cw_v1", 1, 'R20 record paths')
t = rep(t, "reader_plants(texts['LH'], os.path.basename(paths['LH']))   # pk23 hl_v1",
        "reader_plants(texts['LC'], os.path.basename(paths['LC']))   # pk23 cw_v1", 1, 'R21 reader plants')
t = rep(t, "    m_ = re.fullmatch(r'(L|LH|LT)(a|p|k|r)([0-9]*)', FAM)   # pk23 hl_v1\n    if FAM == 'asm':\n",
        "    m_ = re.fullmatch(r'(LC)(a|k|r)([0-9]*)', FAM)   # pk23 cw_v1\n    if FAM == 'asmc':   # pk23 cw_v1\n", 1, 'R22 dispatch')
code = t.split('"""', 2)[2]   # the code after the module docstring
for bad in ("'LH'", "'LT'", "files['L']", "m3_hl_%s", "FAM == 'asm':"):
    assert bad not in code, bad
tb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(tb)
print('COPY %s %s' % (sha(tb), DST))
