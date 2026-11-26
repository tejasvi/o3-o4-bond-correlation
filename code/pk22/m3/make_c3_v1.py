#!/usr/bin/env python3
"""make_c3_v1.py (pk22, phase (iii) step A3): writes m3_run_v1_9_3_px22_c3.py, the revision of pk22's copy
m3_run_v1_9_3_px22_c1.py for runner c3's four M3 families of C3_ENTRY_LIST_v2.json: CS4 (T1MN and W1a's joint Gram windows JA, JD at
pJ = 2, on S4's vertex graph), CE3 (E3T's fT entries and the joint windows' trial components, on E3T's vertex graph), H4T and E2T (NE's
one-vac chain entries hT and the controls eT). It follows make_c2_v1.py (written for the families T1, T1n, T2, T2n; never run): every
replacement is an exact string with an asserted count; the pinned input shas are computed here from the files, which must exist: the
float twin outputs of pk22's m3ref_px22_v1_5 with P16-DONE (one piece per family and N), c1's S4 prep pieces that end DONE, and
pk03's H prep pieces that end DONE as copied into pk22 (jobs/copy_h_prep_items_v1.sh, manifest
m3/MANIFEST_H_PREP_ITEMS_COPY_v1.sha256). The output is a new file (mode 'x') in pk22/m3/. Prints the sha256 of the source, every pin
and the output."""
import hashlib, os, re
CODEDIR = '/mnt/g2/release/root/code'
MYD = CODEDIR + '/pk22/m3'
OUT = MYD + '/out'
HAND = MYD + '/hand'
OWN = CODEDIR + '/pk03'
SRC = MYD + '/m3_run_v1_9_3_px22_c1.py'
DST = MYD + '/m3_run_v1_9_3_px22_c3.py'
LISTF = 'C3_ENTRY_LIST_v2.json'
TWIN = 'm3ref_px22_v1_5'


def fsha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def rep(t, old, new, count, label):
    n = t.count(old)
    assert n == count, 'replacement %s: %d occurrences, expected %d' % (label, n, count)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    return t.replace(old, new)


def lines_of(p):
    with open(p) as fh:
        return fh.read().split('\n')


assert os.path.dirname(os.path.abspath(DST)) == MYD and not os.path.exists(DST), DST
csha = fsha(SRC)
print('SOURCE %s %s' % (csha, SRC))
assert csha.startswith('af6ce85c'), csha
lsha = fsha(os.path.join(MYD, LISTF))
print('PIN %s %s' % (lsha, LISTF))
assert lsha.startswith('e877d12f'), lsha
hsha = fsha(os.path.join(OWN, 'm3_run_v1_9_3.py'))
print('PIN %s pk03/m3_run_v1_9_3.py (the producer of the H prep pieces)' % hsha)
assert hsha.startswith('34abe374'), hsha
# the float twin pieces with P16-DONE, one per family and N
KEYREF = {4: {}, 3: {}}
FAMF = {'CS4': 'P16CS4', 'CE3': 'P16CE3', 'H4T': 'P16CH4T', 'E2T': 'P16CE2T'}
pins = []
for nn in (4, 3):
    for g, ff in FAMF.items():
        done = []
        for k in range(1, 10):
            fn = '%s_%s.%d.p%d_z9sym.out' % (TWIN, ff, nn, k)
            p = os.path.join(OUT, fn)
            if not os.path.exists(p):
                continue
            ls = lines_of(p)
            if [x for x in ls if x.startswith('VERDICT')] == ['VERDICT VALID'] and any(x.startswith('P16-DONE') for x in ls):
                done.append(fn)
        assert len(done) == 1, (g, nn, done)
        KEYREF[nn][g] = done[0]
        pins.append(('OUTD', done[0], fsha(os.path.join(OUT, done[0])), 'the float twin %s at N = %d (P16-DONE)' % (ff, nn)))
# the shared preps' pieces that end DONE, one per N and prep family: c1's S4 prep (its own outputs) and pk03's H prep (copies)
for fam, rex in (('S4', r'PREP16 S4 piece %d: DONE;'), ('H', r'PREP16 H piece %d: DONE;')):
    for nn in (4, 3):
        done = []
        for k in range(1, 20):
            fn = 'm3_run_v1_9_3_%sp%d.%d.out' % (fam, k, nn)
            p = os.path.join(OUT, fn)
            if not os.path.exists(p):
                continue
            ls = lines_of(p)
            if [x for x in ls if x.startswith('VERDICT')] == ['VERDICT VALID'] and any(re.match(rex % k, x) for x in ls):
                done.append((k, fn))
        assert len(done) == 1, (fam, nn, done)
        k, fn = done[0]
        hj = 'm3_run_v1_9_3_%sp%d.%d.json' % (fam, k, nn)
        who = 'c1\'s S4 prep' if fam == 'S4' else 'pk03\'s H prep (copied)'
        pins.append(('OUTD', fn, fsha(os.path.join(OUT, fn)), '%s piece %d at N = %d, done' % (who, k, nn)))
        pins.append(('HANDD', hj, fsha(os.path.join(HAND, hj)), 'its hand-off'))
for d, fn, h, why in pins:
    print('PIN %s %s/%s (%s)' % (h, d, fn, why))
with open(SRC, 'rb') as fh:
    t = fh.read().decode('utf-8')

# 0. the docstring head
t = rep(t, '"""m3_run_v1_9_3_px22_c1.py -- pk22 (code/pk22/m3/): a COPY of pk03/m3_run_v1_9_3.py',
        '"""m3_run_v1_9_3_px22_c3.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c1.py (sha256 %s) for runner\n'
        'c3: the families CS4, CE3, H4T and E2T of pk22\'s C3_ENTRY_LIST_v2.json (sha256 %s), one family per\n'
        'vertex graph: CS4 [free|int|int|free] holds T1MN\'s Z, x, xr, xx and W1a\'s joint Gram windows at pJ = 2 (orbit A: A.JJ, A.Jx, A.Jy,\n'
        'A.Jl, A.xy, A.yy, A.yl, the control A.Jxr; orbit D likewise); CE3 [vac|int|free] holds E3T\'s fT,a and fT2,a and the joint windows\'\n'
        'trial components A.J,a, A.y,a, D.J,a, D.y,a; H4T [vac|int|int|free] holds NE\'s hT,a and hT1,a; E2T [vac|free] the controls eT,a. A\n'
        'horizontal or vertical xi is m3_entries_v3\'s xia factor on the triple (u, v, v). The machinery, gates and plants are c1\'s\n'
        '(pk03\'s m3_run_v1_9_3). What changes:\n'
        '- the list: LIST is the c3 list (pinned); FAMS = (CS4, CE3, H4T, E2T); S8_ENTRY_LIST_v2 stays pinned as LISTS8 (the S4 and H graphs);\n'
        '- items: <X>a (smoke), <Y>p1..<Y>p19 (Prep16 pieces of CE3 and E2T on their own vertex graphs), <X>k1..<X>k9 (entry pieces), CS4r1,\n'
        '  CS4r2 (C-RESUME), asm. CS4 and H4T have no prep pieces: CS4 reads the S4 prep pieces that c1 ran, H4T the H prep pieces that\n'
        '  pk03\'s m3_run_v1_9_3 ran (sha256 %s; outputs, hand-offs and memos copied into pk22 by manifest, the tables by\n'
        '  copy_h_prep_v1.sh) (PREPOF; item_sha: their outputs and hand-offs carry their producer\'s sha256, pinned in INPUTS with the done\n'
        '  pieces and their hand-offs); C-PREP-SHARE (with PLANT-PREP-SHARE): the family\'s prep graph equals LISTS8\'s graph of its prep\n'
        '  family in V, N, S_gauge, edges with tags and pairs, and the float twins (the family\'s own m3ref_px22_v1_5 piece and pk03\'s\n'
        '  P16S4 or P16H, the radii the shared prep took) agree: radii, rho\'^2, theta0 exactly, prep scalars to 1e-12 relative;\n'
        '- float references: pk22\'s m3ref_px22_v1_5 (families P16CS4, P16CE3, P16CH4T, P16CE2T): KEYREF (the piece with P16-DONE,\n'
        '  pinned) gives the KEYJSON of C-SMOKE-AK, C-REP-B and C-REP-AK; PREPREF the PREPJSON of the prep radii and theta0 (C-RULE,\n'
        '  C-PREP-REF): the family\'s own twin, and for CS4 and H4T pk03\'s P16S4 and P16H (as the shared preps took them);\n'
        '- parity: the c3 list has no parity zero (PARITY_ZERO empty; C-PARITY-SET checks that no entry passes C-ODD); PLANT-ODD runs on the\n'
        '  factor set [cp, 2, 0] alone on E2T (odd state 2 on a T <-> B symmetric graph, which passes C-ODD), with S[1][2] + 1e-12; the\n'
        '  reader\'s PLANT-PARZERO marks a free item zero (its a_k are not zero, so the reader must refuse); PLANT-SCOPE and the reader plants\n'
        '  on CS4\'s record;\n'
        '- RESUME_FAMS (CS4,) on CS4\'s x; records m3_c3_<G>_N<N>_J300_c3.json with entry_list C3_ENTRY_LIST_v2 and the prep\'s family and\n'
        '  script in prep16.\n'
        'Made by pk22/m3/make_c3_v1.py. c1\'s docstring follows.\n'
        'm3_run_v1_9_3_px22_c1.py -- pk22 (code/pk22/m3/): a COPY of pk03/m3_run_v1_9_3.py' % (csha, lsha, hsha), 1, 'D0 docstring')
# 1. items
t = rep(t, "ITEM_RE = r'(Ha|S4a|Hp[1-9]|Hp1[0-9]|S4p[1-9]|S4p1[0-9]|Hk[1-9]|S4k[1-9]|Hr[12]|S4r[12]|asm)\\.(4|3)'\n",
        "ITEM_RE = r'((CS4|CE3|H4T|E2T)a|(CE3|E2T)p([1-9]|1[0-9])|(CS4|CE3|H4T|E2T)k[1-9]|CS4r[12]|asm)\\.(4|3)'   # c3: the c3 families\n",
        1, 'D1 ITEM_RE')
t = rep(t, "    print('usage: m3_run_v1_9_3.py ITEM LIM   (ITEM = Ha|S4a|Hp1..Hp19|S4p1..S4p19|Hk1..Hk9|S4k1..S4k9|Hr1|Hr2|S4r1|S4r2|asm . 4|3; LIM = RLIMIT_CPU soft limit in s, 5..540)')\n",
        "    print('usage: m3_run_v1_9_3_px22_c3.py ITEM LIM   (ITEM = <X>a|<Y>p1..<Y>p19|<X>k1..<X>k9|CS4r1|CS4r2|asm . 4|3, X = CS4|CE3|H4T|E2T, Y = CE3|E2T; LIM = RLIMIT_CPU soft limit in s, 5..540)')\n",
        1, 'D2 usage')
# 2. the pins
anchor = "    (OWN + '/tmp/r16', 'mock_arbeng_v1_4.py'): '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e',   # PLANT-MOCK's file\n"
new_p = anchor + ("    (MYD, '%s'): '%s',   # c3: the c3 list\n"
                  "    (MYD, 'm3_run_v1_9_3_px22_c1.py'): '%s',   # c3: c1, the producer of the S4 prep pieces CS4 reads\n"
                  "    (OWN, 'm3_run_v1_9_3.py'): '%s',   # c3: pk03's runner, the producer of the H prep pieces H4T reads\n" % (LISTF, lsha, csha, hsha))
for d, fn, h, why in pins:
    new_p += "    (%s, '%s'): '%s',   # c3: %s\n" % (d, fn, h, why)
t = rep(t, anchor, new_p, 1, 'D3 INPUTS')
t = rep(t, "REFP16 = [('H', 4, 6), ('S4', 4, 6), ('H', 3, 6), ('S4', 3, 6)]   # the float twins' pieces with P16-DONE (family, N, piece)\n",
        "# c3: REFP16, REFPIECE and REFOUT give way to KEYREF and PREPREF (the configuration below)\n", 1, 'D4 REFP16')
# 3. the configuration
a = t.index("with open(os.path.join(W4, 'S8_ENTRY_LIST_v2.json')) as fh:            # m3_run_v1_9: the H and S4 entries of list v2\n")
z_mark = "RESUME_KEY = {'H': 'h,1', 'S4': 'S4,x,1,MB'}   # C-RESUME's entry\n"
assert t.count(z_mark) == 1 and t.count("with open(os.path.join(W4, 'S8_ENTRY_LIST_v2.json')) as fh:            # m3_run_v1_9") == 1
z = t.index(z_mark) + len(z_mark)
old_cfg = t[a:z]
keyref_txt = '{4: {%s}, 3: {%s}}[NN]' % (', '.join("'%s': '%s'" % (g, KEYREF[4][g]) for g in FAMF), ', '.join("'%s': '%s'" % (g, KEYREF[3][g]) for g in FAMF))
new_cfg = ("LISTF = '%s'   # c3: pk22's c3 list (pinned in INPUTS)\n"
           "with open(os.path.join(MYD, LISTF)) as fh:\n"
           "    LIST = json.load(fh)\n"
           "with open(os.path.join(W4, 'S8_ENTRY_LIST_v2.json')) as fh:   # c3: S8's list v2, for the S4 and H graphs of the shared preps (C-PREP-SHARE)\n"
           "    LISTS8 = json.load(fh)\n"
           "with open(os.path.join(INP, 'm2_N%%d_J170.json.b' %% NN)) as fh:\n"
           "    KBAR = json.load(fh)['kbar']\n"
           "TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]\n"
           "TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%%d_sym_v1.json' %% NN), KBAR)\n"
           "TRIAL = {'ts': '%%s:%%s' %% (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%%d_sym_v1.json:%%s' %% (NN, INPUTS[(W4, 'vacres_K3_N%%d_sym_v1.json' %% NN)])}\n"
           "FAMS = ('CS4', 'CE3', 'H4T', 'E2T')   # c3: the c3 list's graphs computed here\n"
           "EDGES = {g: 'N' for g in FAMS}   # only for m3_entries_v3.factor's column lookup: every factor here names its column by index or triple\n"
           "PARITY_ZERO = set()   # c3: no parity zero in the c3 list (C-PARITY-SET checks that no entry passes C-ODD)\n"
           "V3 = [{'id': '%%s:%%s' %% (e['graph'], e['key']), 'key': e['key'], 'graph': e['graph'], 'factors': e['factors'],\n"
           "       'parity': 'zero' if (e.get('parity_zero') or '%%s:%%s' %% (e['graph'], e['key']) in PARITY_ZERO) else 'free', 'grouping': 'std'}\n"
           "      for e in LIST['entries'] if e['graph'] in FAMS]\n"
           "PREPOF = {'CS4': 'S4', 'CE3': 'CE3', 'H4T': 'H', 'E2T': 'E2T'}   # c3: whose prep pieces a family reads (CS4: c1's S4 prep; H4T: pk03's H prep)\n"
           "FAMREF = {'CS4': 'P16S4', 'CE3': 'P16CE3', 'H4T': 'P16H', 'E2T': 'P16CE2T'}   # c3: the float family of the PREPJSON each prep's radii come from\n"
           "KEYFAM = {'CS4': 'P16CS4', 'CE3': 'P16CE3', 'H4T': 'P16CH4T', 'E2T': 'P16CE2T'}   # c3: the float family of each family's KEYJSON\n"
           "KEYREF = %s   # c3: pk22's float twin pieces with P16-DONE (pinned)\n"
           "PREPREF = {g: os.path.join(OUTD, KEYREF[g]) for g in ('CE3', 'E2T')}   # c3: the PREPJSON of each prep's radii and theta0\n"
           "PREPREF['CS4'] = os.path.join(OUTD_IN, 'm3ref_v1_14_P16S4.%%d.p6_z9sym.out' %% NN)   # c3: c1's S4 prep took these (pinned)\n"
           "PREPREF['H4T'] = os.path.join(OUTD_IN, 'm3ref_v1_14_P16H.%%d.p6_z9sym.out' %% NN)   # c3: pk03's H prep took these (pinned)\n"
           "RULE = (80.0, 0.6, 0.7)   # the float references' radii sqrt(min(80 G_vv/J, 0.6)) and rho' (m3ref_v1_14's default for every P16 family)\n"
           "PFX = {'CS4': 'CS4', 'CE3': 'CE3', 'H4T': 'H4T', 'E2T': 'E2T', 'S4': 'S4', 'H': 'H'}   # item prefixes (S4, H: the shared preps' pieces)\n"
           "MAXP = {g: 9 for g in FAMS}   # entry pieces\n"
           "MAXPP = 19   # prep pieces\n"
           "RESUME_FAMS = ('CS4',)   # c3: the families with the items Xr1, Xr2 (CS4: the shared D16 prep)\n"
           "RESUME_KEY = {'CS4': 'x'}   # C-RESUME's entry\n"
           "C1_SHA = INPUTS[(MYD, 'm3_run_v1_9_3_px22_c1.py')]   # c3: the producer of the S4 prep pieces CS4 reads\n"
           "H_SHA = INPUTS[(OWN, 'm3_run_v1_9_3.py')]   # c3: the producer of the H prep pieces H4T reads (pk03's runner)\n"
           "\n\n"
           "def item_sha(item):\n"
           "    \"\"\"c3: the script sha256 an item's output and hand-off carry: c1's for the S4 prep pieces, pk03's runner's for the H prep\n"
           "    pieces, this script's for every other item.\"\"\"\n"
           "    if re.fullmatch(r'S4p[0-9]+\\.[34]', item):\n"
           "        return C1_SHA\n"
           "    if re.fullmatch(r'Hp[0-9]+\\.[34]', item):\n"
           "        return H_SHA\n"
           "    return SELF_SHA\n") % (LISTF, keyref_txt)
t = t[:a] + new_cfg + t[z:]
print('REPLACE D5 configuration block: 1 occurrence (%d chars for %d)' % (len(new_cfg), len(old_cfg)))
# 4. the float references
t = rep(t, "def ref_files(graph):\n    return [os.path.join(OUTD_IN, fn) for fn in REFOUT[graph]]\n\n\ndef ref_prep(graph):\n    return read_lines(ref_files(graph)[0], 'PREPJSON')[0]\n",
        "def ref_files(graph):\n"
        "    \"\"\"c3: the family's float twin output with its KEYJSON lines (pk22's m3ref_px22_v1_5, the piece with P16-DONE).\"\"\"\n"
        "    return [os.path.join(OUTD, KEYREF[graph])]\n\n\n"
        "def ref_prep(graph):\n"
        "    \"\"\"c3: the PREPJSON whose radii and theta0 the family's prep takes: its own twin's; CS4 and H4T pk03's P16S4 and P16H.\"\"\"\n"
        "    return read_lines(PREPREF[graph], 'PREPJSON')[0]\n", 1, 'D6 ref_files ref_prep')
t = rep(t, "        graph, REFOUT[graph][0], rp['family'], rp['N'], rp['J']))\n",
        "        graph, os.path.basename(PREPREF[graph]), rp['family'], rp['N'], rp['J']))\n", 1, 'D7 C-PREP-REF')
t = rep(t, "            graph, NN, gp.V, gp.F, REFOUT[graph][0], rp['theta0'],", "            graph, NN, gp.V, gp.F, os.path.basename(PREPREF[graph]), rp['theta0'],",
        1, 'D8 PREP line')
t = rep(t, "entries against m3ref_v1_14 %s: largest '", "entries against m3ref_px22_v1_5 %s: largest '", 1, 'D9 C-SMOKE-AK text')
t = rep(t, "(n, graph, FAMREF[graph], worst[0], worst[1], worst[2]))", "(n, graph, KEYFAM[graph], worst[0], worst[1], worst[2]))", 1,
        'D10 C-SMOKE-AK family')
t = rep(t, "against m3ref_v1_14 P16 z9sym", "against m3ref_px22_v1_5 P16 z9sym", 2, 'D11 C-REP texts')
# 5. parity
old_par = t[t.index('def parity_set():\n'):t.index('def laws_of(pr, mF):\n')]
assert t.count('def parity_set():\n') == 1 and t.count('def laws_of(pr, mF):\n') == 1
new_par = ('def parity_set():\n'
           '    """c3, C-PARITY-SET by entry id (family:key): the entries whose factors pass c_odd16 are exactly PARITY_ZERO (empty in the c3\n'
           '    list), and V3 marks exactly those \'zero\'. PLANT-ODD: the factor set [cp, 2, 0] alone on E2T (the odd trial state on a T <-> B\n'
           '    symmetric graph) passes c_odd16, and from a copy of the trial set with S[1][2] + 1e-12 it must fail."""\n'
           '    import copy\n'
           '    passing = sorted(e[\'id\'] for e in V3 if c_odd16(e[\'graph\'], [ENT.factor(TS, EDGES[e[\'graph\']], enc) for enc in e[\'factors\']])[0])\n'
           '    marked = sorted(e[\'id\'] for e in V3 if e[\'parity\'] == \'zero\')\n'
           '    gate(\'C-PARITY-SET\', passing == sorted(PARITY_ZERO) and marked == sorted(PARITY_ZERO), \'(the entries whose factors pass C-ODD on their own \'\n'
           '         \'graph: %s; marked zero: %s; PARITY_ZERO %s)\' % (passing, marked, sorted(PARITY_ZERO)))\n'
           '    ok0, why0 = c_odd16(\'E2T\', [ENT.factor(TS, EDGES[\'E2T\'], [\'cp\', 2, 0])])\n'
           '    gate(\'C-ODD-PLANT-BASE\', ok0, \'(c3: [cp, 2, 0] alone on E2T passes C-ODD: %s)\' % why0)\n'
           '    ts2 = copy.deepcopy(TS)\n'
           '    ts2.S[1][2] = ts2.S[1][2] + 1e-12\n'
           '    ok, why = c_odd16(\'E2T\', [ENT.factor(ts2, EDGES[\'E2T\'], [\'cp\', 2, 0])])\n'
           '    plant(\'PLANT-ODD\', not ok, \'([cp, 2, 0] on E2T with S[1][2] + 1e-12: %s)\' % why)\n\n\n')
t = t.replace(old_par, new_par)
print('REPLACE D12 parity_set: 1 occurrence')
# 6. hand-offs of other scripts' items (c1's S4 prep pieces, pk03's H prep pieces)
t = rep(t, "{'script': SELF_SHA, 'item': item, 'N': NN, 'family': fam},", "{'script': item_sha(item), 'item': item, 'N': NN, 'family': fam},", 1, 'D13 read_handoff')
t = rep(t, "    if m and m.group(1) == item and m.group(3) == SELF_SHA and HO.verdict_ok(lines, CAPPED):\n        return 'capped'\n"
           "    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)\n\n\ndef memo_head(",
        "    if m and m.group(1) == item and m.group(3) == item_sha(item) and HO.verdict_ok(lines, CAPPED):   # c3: item_sha\n        return 'capped'\n"
        "    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)\n\n\ndef memo_head(", 1, 'D14 item_state')
t = rep(t, "item_state('%sp%d.%d' % (PFX[graph], k, NN))", "item_state('%sp%d.%d' % (PFX[PREPOF[graph]], k, NN))", 2, 'D15 prep_final prep_info states')
t = rep(t, "        body = read_handoff('%sp%d.%d' % (PFX[graph], k, NN), graph)\n",
        "        body = read_handoff('%sp%d.%d' % (PFX[PREPOF[graph]], k, NN), PREPOF[graph])   # c3: PREPOF\n", 1, 'D16 prep_final read')
t = rep(t, "        info = read_handoff('%sp%d.%d' % (PFX[graph], k, NN), graph)['info']\n",
        "        info = read_handoff('%sp%d.%d' % (PFX[PREPOF[graph]], k, NN), PREPOF[graph])['info']   # c3: PREPOF\n", 1, 'D17 prep_info read')
# 7. C-PREP-SHARE
t = rep(t, "\n\nPACK_LIM = 9 * 10 ** 18",
        "\n\ndef prep_share(graph):\n"
        "    \"\"\"c3, C-PREP-SHARE: a family whose prep is another family's (PREPOF; CS4 reads c1's S4 prep, H4T pk03's H prep) has that\n"
        "    family's prep graph: the vertex-only graphs (prep_graph) of its own graph and of LISTS8's graph of that family agree in V, N,\n"
        "    S_gauge, the edges with their tags in order and the (empty) pairs; and the float twins' PREPJSON lines, the family's own (ref_files)\n"
        "    and the one the shared prep took (ref_prep), agree: radii, rho'^2 and theta0 exactly, rE, nC8, nC6, Pout, Pout_p and farbase to\n"
        "    1e-12 relative. PLANT-PREP-SHARE: the family's prep graph with its first edge dropped must differ. A family with its own prep:\n"
        "    nothing.\"\"\"\n"
        "    pf = PREPOF[graph]\n"
        "    if pf == graph:\n"
        "        return\n"
        "    spec = LISTS8['graphs'][pf]\n"
        "    V0, E0 = GR.strip(spec['columns'])\n"
        "    p0 = prep_graph(GR.GraphIV(V0, E0, sorted(tuple(sorted(p)) for p in spec['pairs']), NN))\n"
        "    p1 = prep_graph(family_graph(graph))\n"
        "    ins = lambda G: (G.V, G.N, list(G.S_gauge), [(tuple(e), c) for e, c in G.edges], list(G.pairs))\n"
        "    okg = ins(p0) == ins(p1)\n"
        "    a = read_lines(ref_files(graph)[0], 'PREPJSON')[0]\n"
        "    b = ref_prep(graph)\n"
        "    ex = all(a[k] == b[k] for k in ('a_v', 'ap', 'theta0'))\n"
        "    rel = max(abs(a[k] - b[k]) / abs(b[k]) for k in ('rE', 'nC8', 'nC6', 'Pout', 'Pout_p', 'farbase'))\n"
        "    gate('C-PREP-SHARE', okg and ex and rel <= 1e-12, '(%s reads %s\\'s prep (pinned): the prep graphs of %s and of S8_ENTRY_LIST_v2\\'s %s '\n"
        "         'agree in V, N, S_gauge, edges with tags and pairs: %s; float twins %s and %s: radii, rho\\'^2 and theta0 equal: %s, prep scalars '\n"
        "         'within %.1e relative)' % (graph, pf, graph, pf, okg, os.path.basename(ref_files(graph)[0]), os.path.basename(PREPREF[graph]), ex, rel))\n"
        "    pb = GR.GraphIV(p1.V, list(p1.edges)[1:], [], p1.N, list(p1.S_gauge))\n"
        "    plant('PLANT-PREP-SHARE', ins(pb) != ins(p0), '(%s\\'s prep graph with its first edge dropped, against %s\\'s)' % (graph, pf))\n"
        "\n\nPACK_LIM = 9 * 10 ** 18", 1, 'D18 prep_share')
t = rep(t, "    prep_same(graph, g, prep_graph(g), pr)   # m3_run_v1_9_2\n",
        "    prep_same(graph, g, prep_graph(g), pr)   # m3_run_v1_9_2\n    prep_share(graph)   # c3\n", 1, 'D19 smoke share')
t = rep(t, "    pr, rp = make_prep(graph, g, scalars=dict(su, **sc))   # m3_run_v1_9: v10's Prep on the restored scalars\n",
        "    pr, rp = make_prep(graph, g, scalars=dict(su, **sc))   # m3_run_v1_9: v10's Prep on the restored scalars\n    prep_share(graph)   # c3\n",
        1, 'D20 pieces share')
t = rep(t, "    pr, rp = make_prep(graph, g, scalars=dict(fin['scal_u'], **fin['scal_c']))\n",
        "    pr, rp = make_prep(graph, g, scalars=dict(fin['scal_u'], **fin['scal_c']))\n    prep_share(graph)   # c3\n", 1, 'D21 resume share')
t = rep(t, "        fins[graph] = prep_final(graph)\n", "        fins[graph] = prep_final(graph)\n        prep_share(graph)   # c3\n", 1, 'D22 asm share')
# 8. asm and the reader plants
t = rep(t, "            dd3['items']['h,2']['ak'][1] = 1e-30\n",
        "            k0_ = sorted(k for k in dd3['items'] if dd3['items'][k]['parity'] == 'free')[0]   # c3: no parity zero in the c3 records\n"
        "            dd3['items'][k0_]['parity'] = 'zero'   # c3: a free item marked zero (its a_k are not zero)\n", 1, 'D23 PLANT-PARZERO')
t = rep(t, "    plant('PLANT-SCOPE', not (set(list(files['H'])[1:]) == want['H']), '(H without one key)')\n",
        "    plant('PLANT-SCOPE', not (set(list(files['CS4'])[1:]) == want['CS4']), '(CS4 without one key)')   # c3\n", 1, 'D24 PLANT-SCOPE')
t = rep(t, "'(the two records hold exactly the list\\'s keys of their graphs: %s)'", "'(the c3 records hold exactly the list\\'s keys of their graphs: %s)'", 1,
        'D25 C-SCOPE text')
t = rep(t, "        extra = {'entry_list': 'S8_ENTRY_LIST_v2.json:%s' % INPUTS[(W4, 'S8_ENTRY_LIST_v2.json')], 'graph': g, 'dmaxH': 16, 'claim_ball': CLAIM_BALL,\n"
           "                 'prep16': dict({'tables': tabs, 'block': BLOCK16, 'memo': os.path.basename(memo_path(g)), 'memo_lines': fins[g]['memo_lines'],\n"
           "                                 'memo_head_sha256': fins[g]['memo_head_sha'], 'prep_piece': fins[g]['piece']}, **pinfo)}\n",
        "        extra = {'entry_list': '%s:%s' % (LISTF, INPUTS[(MYD, LISTF)]), 'graph': g, 'dmaxH': 16, 'claim_ball': CLAIM_BALL,   # c3\n"
        "                 'prep16': dict({'tables': tabs, 'block': BLOCK16, 'memo': os.path.basename(memo_path(PREPOF[g])), 'memo_lines': fins[g]['memo_lines'],\n"
        "                                 'memo_head_sha256': fins[g]['memo_head_sha'], 'prep_piece': fins[g]['piece'], 'prep_family': PREPOF[g],\n"
        "                                 'prep_script': item_sha('%sp1.%d' % (PFX[PREPOF[g]], NN))}, **pinfo)}\n", 1, 'D26 record extra')
t = rep(t, "        paths[g] = os.path.join(OUTD, 'm3_s8v2_%s_N%d_J300%s_v1_9_3.json' % (g, NN, tag))\n",
        "        paths[g] = os.path.join(OUTD, 'm3_c3_%s_N%d_J300%s_c3.json' % (g, NN, tag))   # c3\n", 1, 'D27 record names')
t = rep(t, "    reader_plants(texts['H'], os.path.basename(paths['H']))\n", "    reader_plants(texts['CS4'], os.path.basename(paths['CS4']))   # c3\n", 1,
        'D28 reader plants')
# 9. the dispatch
t = rep(t, "    m_ = re.fullmatch(r'(H|S4)(a|p|k|r)([0-9]*)', FAM)\n", "    m_ = re.fullmatch(r'(CS4|CE3|H4T|E2T)(a|p|k|r)([0-9]*)', FAM)   # c3\n", 1, 'D29 dispatch')
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (hashlib.sha256(nb).hexdigest(), DST))
