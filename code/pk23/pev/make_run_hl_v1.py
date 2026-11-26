#!/usr/bin/env python3
"""make_run_hl_v1.py (pk23, option B Pev entries; the P0_LOG rows 4409, 4422, 4435; pk22's handover 13d4039c): writes
pk23/pev/m3_run_v1_9_3_hl_v1.py from pk22's runner m3_run_v1_9_3_px22_c3k_1.py (c76745bc, read-only), and the hand-off module
copy pk23/pev/m3_handoff_v3_hl.py from pk22's m3_handoff_v3_px22.py (eee54757) with HAND moved to pk23/pev/hand. Runner
changes: the list HL_ENTRY_LIST_v1.json (read from pk23/pev, pinned); FAMS L, LH, LT; one prep family L read by LH and LT (PREPOF);
FAMREF P16L; KEYFAM P16L, P16LH, P16LT; KEYREF pk23's rtwin_hl_v1 outputs; PREPREF the twin m3ref_hl_v1's P16L pieces with
P16-DONE; the trial set z9sym (pk11's files, pk25's mr/v3 TRIAL_SET); PFX; ITEM_RE and the dispatch; SMOKE_PARTS empty;
RESUME_FAMS LH on Mh,0,0; PLANT-ODD on L; C-HASH-REF's TRIAL z9sym; PLANT-SCOPE and the reader plants on LH's record; records
m3_hl_<G>_N<N>_J300_hl.json; written paths OUTD = pk23/pev/out and HANDD = pk23/pev/hand (MYD stays pk22/m3 for its pinned
inputs); INPUTS keeps every entry outside pk22's out/ and hand/ and the psixy folder, drops those, and adds pk23's. Every
replacement is an exact string or line with an asserted count; the outputs are new files (mode 'x').
Usage: make_run_hl_v1.py PIECE_N4 PIECE_N3 (the twin pieces with P16-DONE in pk23/pev/out). Prints the shas."""
import hashlib, os, re, sys
W18 = '/mnt/g2/release/root/code'
SRCD = W18 + '/pk22/m3'
HLD = W18 + '/pk23/pev'
SRC, HSRC = SRCD + '/m3_run_v1_9_3_px22_c3k_1.py', SRCD + '/m3_handoff_v3_px22.py'
DST, HDST = HLD + '/m3_run_v1_9_3_hl_v1.py', HLD + '/m3_handoff_v3_hl.py'
LISTF = 'HL_ENTRY_LIST_v1.json'


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


assert len(sys.argv) == 3, 'usage: make_run_hl_v1.py PIECE_N4 PIECE_N3'
P4, P3 = sys.argv[1], sys.argv[2]
assert re.fullmatch(r'm3ref_hl_v1_P16L\.4\.p[1-9]_z9sym\.out', P4) and re.fullmatch(r'm3ref_hl_v1_P16L\.3\.p[1-9]_z9sym\.out', P3), (P4, P3)
for p in (DST, HDST):
    assert os.path.dirname(os.path.abspath(p)) == HLD and not os.path.exists(p), p
b, hb = open(SRC, 'rb').read(), open(HSRC, 'rb').read()
assert sha(b).startswith('8876ba28'), sha(b)
assert sha(hb).startswith('92bdfee1'), sha(hb)
print('SOURCE %s %s' % (sha(b), SRC))
print('SOURCE %s %s' % (sha(hb), HSRC))

# the hand-off module copy
ht = hb.decode('utf-8')
ht = rep(ht, "HAND = '/mnt/g2/release/root/code/pk22/m3/hand'   # pk22 copy: hand-offs in pk22/m3/hand\n",
         "HAND = '/mnt/g2/release/root/code/pk23/pev/hand'   # pk23 hl_v1 copy: hand-offs in pk23/pev/hand\n", 1, 'HO1 HAND')
ht = rep(ht, '"""m3_handoff_v3_px22.py -- pk22 (code/pk22/m3/): a COPY of',
         '"""m3_handoff_v3_hl.py -- pk23 (code/pk23/pev/): pk22\'s m3_handoff_v3_px22.py (sha256 %s) with HAND moved to pk23/pev/hand\n'
         '(pk23\'s make_run_hl_v1.py; the only change). m3_handoff_v3_px22.py was: a COPY of' % sha(hb), 1, 'HO2 docstring')
hnb = ht.encode('utf-8')
HSHA = sha(hnb)

# pk23's pinned inputs
mine = [('HLD', LISTF), ('HLD', 'rtwin_hl_v1.py'), ('HLD', 'm3ref_hl_v1.py'), ('OUTD', P4), ('OUTD', P3)]
mine += [('OUTD', 'rtwin_hl_v1_%s.%d_z9sym.out' % (f, n)) for n in (4, 3) for f in ('L', 'LH', 'LT')]
pins = []
for root, name in mine:
    path = os.path.join(HLD if root == 'HLD' else HLD + '/out', name)
    h = sha_path(path)
    pins.append("    (%s, %r): %r,   # pk23 hl_v1" % (root, name, h))
    print('PIN %s %s' % (h, path))
assert sha_path(os.path.join(HLD, LISTF)).startswith('2d115b6d')

t = b.decode('utf-8')
t = t.replace('"""m3_run_v1_9_3_px22_c3k_1.py', '"""m3_run_v1_9_3_hl_v1.py -- pk23 (code/pk23/pev/): a COPY of pk22\'s m3_run_v1_9_3_px22_c3k_1.py (sha256 %s)\n'
              'by pk23\'s make_run_hl_v1.py for the option B Pev entries on S8\'s L graph (the P0_LOG rows 4409, 4422, 4435): the list\n'
              'HL_ENTRY_LIST_v1.json (families L: TT,0,0; LH: TTh,0,0, Mh,0,0, Mhh,0,0; LT: Mt,0,0, Mtt,0,0); one prep family L (items Lp1..) read by\n'
              'LH and LT (PREPOF, C-PREP-SHARE against S8_ENTRY_LIST_v2\'s L); the trial set z9sym (pk25\'s mr/v3 TRIAL_SET); references pk23\'s\n'
              'rtwin_hl_v1 (restored prep) and twin m3ref_hl_v1 (P16L); smoke items La, LHa, LTa; RESUME_FAMS LH on Mh,0,0; PLANT-ODD on L; records\n'
              'm3_hl_<G>_N<N>_J300_hl.json; PLANT-SCOPE and the reader plants on LH\'s record; written paths in pk23/pev/out and pk23/pev/hand.\n'
              'm3_run_v1_9_3_px22_c3k_1.py' % sha(b), 1) if t.count('"""m3_run_v1_9_3_px22_c3k_1.py') == 1 else None
assert t is not None, 'docstring head'
print('REPLACE R1 docstring: 1 occurrence(s)')
t = rep_line(t, "ITEM_RE = r'(E4Da|E4Na[1-4]|(E4D|E4N)p([1-9]|1[0-9])|(E4D|E4N)k[1-9]|E4Nr[12]|asm)",
             "ITEM_RE = r'((L|LH|LT)a|Lp([1-9]|1[0-9])|(L|LH|LT)k[1-9]|LHr[12]|asm)\\.(4|3)'   # pk23 hl_v1: L's prep pieces, one smoke item per family", 'R2 ITEM_RE')
t = rep_line(t, "    print('usage: m3_run_v1_9_3_px22_c3k_1.py ITEM LIM",
             "    print('usage: m3_run_v1_9_3_hl_v1.py ITEM LIM   (ITEM = La|LHa|LTa|Lp1..Lp19|<X>k1..<X>k9|LHr1|LHr2|asm . 4|3, X = L|LH|LT; LIM = RLIMIT_CPU soft limit in s, 5..540)')",
             'R3 usage')
t = rep(t, "OUTD = MYD + '/out'   # pk22 copy: written outputs, memos, records and out/tab16c here\n",
        "HLD = CODEDIR + '/pk23/pev'   # pk23 hl_v1: the list, the hand-off module copy, the references\n"
        "OUTD = HLD + '/out'   # pk23 hl_v1: written outputs, memos, records and out/tab16c here (MYD: pk22's pinned inputs, read-only)\n", 1, 'R4 OUTD')
t = rep(t, "HANDD = MYD + '/hand'   # pk22 copy: hand-offs here\n", "HANDD = HLD + '/hand'   # pk23 hl_v1: hand-offs here\n", 1, 'R5 HANDD')
t = rep(t, "MODDIR = {'m3_handoff_v3_px22.py': MYD}   # pk22 copy: the one module read from pk22/m3/\n",
        "MODDIR = {'m3_handoff_v3_hl.py': HLD}   # pk23 hl_v1: the one module read from pk23/pev/\n", 1, 'R6 MODDIR')
t = rep(t, "    'm3_handoff_v3_px22.py': '92bdfee1da111163c1f32e5bdc8e62f2b59cf4e377be23235964d2ff86801d58',   # pk22 copy of m3_handoff_v3.py (HAND moved)\n",
        "    'm3_handoff_v3_hl.py': '%s',   # pk23 hl_v1: pk22's copy with HAND moved to pk23/pev/hand\n" % HSHA, 1, 'R7 OWNMOD')
t = rep(t, "('m3_handoff', 'm3_handoff_v3_px22.py')", "('m3_handoff', 'm3_handoff_v3_hl.py')", 1, 'R8 GENERIC')
# INPUTS: drop pk22's out/, hand/ and psixy entries, keep the rest, add pk23's
lines = t.split('\n')
i0 = lines.index('INPUTS = {')
i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i] == '}')
body = lines[i0 + 1:i1]
keep = [ln for ln in body if not ln.lstrip().startswith(('(OUTD,', '(HANDD,', '(PSX,'))]
drop = [ln for ln in body if ln.lstrip().startswith(('(OUTD,', '(HANDD,', '(PSX,'))]
assert all(ln.lstrip().startswith(('(W4,', '(INP,', '(OUTD_IN,', '(OWN', '(MYD,')) for ln in keep), [ln for ln in keep][:3]
print('INPUTS: kept %d, dropped %d, added %d' % (len(keep), len(drop), len(pins)))
assert (len(keep), len(drop)) == (23, 42), (len(keep), len(drop))
lines[i0 + 1:i1] = keep + pins
t = '\n'.join(lines)
t = rep(t, "with open(os.path.join(MYD, LISTF)) as fh:\n", "with open(os.path.join(HLD, LISTF)) as fh:   # pk23 hl_v1\n", 1, 'R9 list path')
t = rep_line(t, "LISTF = 'C3K_ENTRY_LIST_v1_1.json'", "LISTF = '%s'   # pk23 hl_v1: pk23's L list (pinned in INPUTS under HLD)" % LISTF, 'R10 LISTF')
t = rep_line(t, "TSF = {4: 'ts_N4_J170_D_S_z9symxy_v1.json'",
             "TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]   # pk23 hl_v1: z9sym, pk25's mr/v3 TRIAL_SET (the row 4435)", 'R11 TSF')
t = rep_line(t, "TS = ENT.load_trial(os.path.join(PSX, TSF)", "TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)   # pk23 hl_v1", 'R12 TS')
t = rep_line(t, "TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(PSX, TSF)])",
             "TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)])}   # pk23 hl_v1", 'R13 TRIAL')
t = rep_line(t, "FAMS = ('E4D', 'E4N')", "FAMS = ('L', 'LH', 'LT')   # pk23 hl_v1: the L list's graphs computed here (LB is a float control only)", 'R14 FAMS')
t = rep_line(t, "PREPOF = {'E4D': 'E4D', 'E4N': 'E4N'}", "PREPOF = {'L': 'L', 'LH': 'L', 'LT': 'L'}   # pk23 hl_v1: one prep family L (12 vertices) read by LH and LT", 'R15 PREPOF')
t = rep_line(t, "FAMREF = {'E4D': 'P16E4D', 'E4N': 'P16E4N'}", "FAMREF = {'L': 'P16L', 'LH': 'P16L', 'LT': 'P16L'}   # pk23 hl_v1: the twin m3ref_hl_v1's P16L PREPJSON", 'R16 FAMREF')
t = rep_line(t, "KEYFAM = {'E4D': 'P16E4D', 'E4N': 'P16E4N'}", "KEYFAM = {'L': 'P16L', 'LH': 'P16LH', 'LT': 'P16LT'}   # pk23 hl_v1: the family names of rtwin_hl_v1's KEYJSON", 'R17 KEYFAM')
t = rep_line(t, "KEYREF = {4: {'E4D': 'rtwin_c3k_v1_1_E4D.4_z9symxy.out'",
             "KEYREF = dict((g, 'rtwin_hl_v1_%s.%d_z9sym.out' % (g, NN)) for g in FAMS)   # pk23 hl_v1: rtwin_hl_v1's references (restored prep; pinned)", 'R18 KEYREF')
t = rep_line(t, "PREPREF = {'E4D': os.path.join(OUTD,",
             "PREPREF = dict((g, os.path.join(OUTD, {4: %r, 3: %r}[NN])) for g in FAMS)   # pk23 hl_v1: the twin's P16L pieces with P16-DONE (pinned)" % (P4, P3), 'R19 PREPREF')
t = rep_line(t, "PFX = {'E4D': 'E4D', 'E4N': 'E4N', 'CE3': 'CE3', 'S4': 'S4', 'H': 'H'}",
             "PFX = {'L': 'L', 'LH': 'LH', 'LT': 'LT', 'CE3': 'CE3', 'S4': 'S4', 'H': 'H'}   # item prefixes (pk23 hl_v1: L, LH, LT)", 'R20 PFX')
t = rep_line(t, "RESUME_FAMS = ('E4N',)", "RESUME_FAMS = ('LH',)   # pk23 hl_v1: the family with the items Xr1, Xr2", 'R21 RESUME_FAMS')
t = rep_line(t, "RESUME_KEY = {'E4N': 'IhR,10,1'}", "RESUME_KEY = {'LH': 'Mh,0,0'}   # C-RESUME's entry (pk23 hl_v1)", 'R22 RESUME_KEY')
t = rep(t, "    ok0, why0 = c_odd16('E4D', [ENT.factor(TS, EDGES['E4D'], ['cp', 2, 0])])\n",
        "    ok0, why0 = c_odd16('L', [ENT.factor(TS, EDGES['L'], ['cp', 2, 0])])   # pk23 hl_v1: on L\n", 1, 'R23 PLANT-ODD base')
t = rep(t, "    gate('C-ODD-PLANT-BASE', ok0, '(c3k: [cp, 2, 0] alone on E4D passes C-ODD: %s)' % why0)\n",
        "    gate('C-ODD-PLANT-BASE', ok0, '(hl_v1: [cp, 2, 0] alone on L passes C-ODD: %s)' % why0)\n", 1, 'R24 PLANT-ODD base text')
t = rep(t, "    ok, why = c_odd16('E4D', [ENT.factor(ts2, EDGES['E4D'], ['cp', 2, 0])])\n",
        "    ok, why = c_odd16('L', [ENT.factor(ts2, EDGES['L'], ['cp', 2, 0])])   # pk23 hl_v1\n", 1, 'R25 PLANT-ODD')
t = rep(t, "    plant('PLANT-ODD', not ok, '([cp, 2, 0] on E4D with S[1][2] + 1e-12: %s)' % why)\n",
        "    plant('PLANT-ODD', not ok, '([cp, 2, 0] on L with S[1][2] + 1e-12: %s)' % why)\n", 1, 'R26 PLANT-ODD text')
t = rep_line(t, "SMOKE_PARTS = {'E4N':", "SMOKE_PARTS = {}   # pk23 hl_v1: every family's smoke is one item", 'R27 SMOKE_PARTS')
t = rep(t, "rtwin_c3k_v1_1 %s (restored prep)", "rtwin_hl_v1 %s (restored prep)", 1, 'R28 C-SMOKE-AK text')
t = rep(t, "against rtwin_c3k_v1_1 (restored prep) z9symxy:", "against rtwin_hl_v1 (restored prep) z9sym:", 2, 'R29 C-REP texts')
t = rep(t, "[ln for ln in lines if ln.startswith('TRIAL')] == ['TRIAL z9symxy']", "[ln for ln in lines if ln.startswith('TRIAL')] == ['TRIAL z9sym']", 1, 'R30 C-HASH-REF')
t = rep(t, "TRIAL lines exactly [TRIAL z9symxy])", "TRIAL lines exactly [TRIAL z9sym])", 1, 'R31 C-HASH-REF text')
t = rep(t, "'(the c3k records hold exactly the list\\'s keys of their graphs: %s)'", "'(the hl records hold exactly the list\\'s keys of their graphs: %s)'", 1, 'R32 C-SCOPE text')
t = rep(t, "    plant('PLANT-SCOPE', not (set(list(files['E4N'])[1:]) == want['E4N']), '(E4N without one key)')   # c3k\n",
        "    plant('PLANT-SCOPE', not (set(list(files['LH'])[1:]) == want['LH']), '(LH without one key)')   # pk23 hl_v1\n", 1, 'R33 PLANT-SCOPE')
t = rep(t, "        paths[g] = os.path.join(OUTD, 'm3_c3k_%s_N%d_J300%s_c3k.json' % (g, NN, tag))   # c3k\n",
        "        paths[g] = os.path.join(OUTD, 'm3_hl_%s_N%d_J300%s_hl.json' % (g, NN, tag))   # pk23 hl_v1\n", 1, 'R34 record paths')
t = rep(t, "    reader_plants(texts['E4N'], os.path.basename(paths['E4N']))   # c3k\n",
        "    reader_plants(texts['LH'], os.path.basename(paths['LH']))   # pk23 hl_v1\n", 1, 'R35 reader plants')
t = rep(t, "    m_ = re.fullmatch(r'(E4D|E4N)(a|p|k|r)([0-9]*)', FAM)   # c3k\n",
        "    m_ = re.fullmatch(r'(L|LH|LT)(a|p|k|r)([0-9]*)', FAM)   # pk23 hl_v1\n", 1, 'R36 dispatch')
t = rep(t, "'entry_list': '%s:%s' % (LISTF, INPUTS[(MYD, LISTF)])", "'entry_list': '%s:%s' % (LISTF, INPUTS[(HLD, LISTF)])", 1, 'R37 record entry_list')
rest = [ln for ln in t.split('\n') if re.search(r"'E4[DN]'|\(E4D\|E4N\)|z9symxy'|PSX, TSF", ln) and not ln.lstrip().startswith('#')]
assert not rest, rest[:3]
nb = t.encode('utf-8')
with open(HDST, 'xb') as fh:
    fh.write(hnb)
print('COPY %s %s' % (HSHA, HDST))
with open(DST, 'xb') as fh:
    fh.write(nb)
print('COPY %s %s' % (sha(nb), DST))
