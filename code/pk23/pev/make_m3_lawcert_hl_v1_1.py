#!/usr/bin/env python3
"""make_m3_lawcert_hl_v1_1.py (pk23; C_w variant B, the P0_LOG row 4589: the second-order comb needs the certified J-laws of pk23's Pev
records TT,0,0 and Mh,0,0): writes (mode 'x') pk23/pev/m3_lawcert_hl_v1_1.py from pk22's m3_lawcert_c3k_v1.py (8b96d81a, read-only;
The review-checked pattern) by exact replacements of asserted counts and two block replacements between unique markers (the configuration and pin
block; the C-NO-RESUME block's family names and item grammar). Every new pin is copied from the runner m3_run_v1_9_3_hl_v1's own OWNMOD and
INPUTS (read by ast) and checked against the file, or computed from the file and checked against the sha8 the producer's tool outputs gave; no hash
is typed in full. Usage: make_m3_lawcert_hl_v1_1.py. Prints the replacements and the output's sha256."""
import ast, hashlib, os

W18 = '/mnt/g2/release/root/code'
SMD = W18 + '/pk22/m3'
HLD = W18 + '/pk23/pev'
SRC, DST = SMD + '/m3_lawcert_c3k_v1.py', HLD + '/m3_lawcert_hl_v1_1.py'
RUNF = HLD + '/m3_run_v1_9_3_hl_v1.py'
SIDE = (HLD + '/MANIFEST_PEV_RUN_ABS_v1.sha256', 'b70eeb85')


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


assert os.path.dirname(DST) == os.path.dirname(os.path.abspath(__file__)) and not os.path.exists(DST), DST
s0, sr, ss = sha(SRC), sha(RUNF), sha(SIDE[0])
print('SOURCE %s %s\nRUNNER %s %s\nSIDE %s %s' % (s0, SRC, sr, RUNF, ss, SIDE[0]))
assert s0.startswith('8b96d81a') and sr.startswith('57f73e77') and ss.startswith(SIDE[1]), (s0, sr, ss)
rtree = ast.parse(open(RUNF).read())
ns = {'__builtins__': {}}
for nm in ('CODEDIR', 'OWN', 'C2B', 'INP', 'W4', 'MYD', 'HLD', 'OUTD', 'OUTD_IN', 'HANDD', 'PSX', 'OWNMOD', 'INPUTS'):
    top = [st for st in rtree.body if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) and st.targets[0].id == nm]
    assert len(top) == 1, nm
    exec(compile(ast.Module(body=[top[0]], type_ignores=[]), 'runner:%s' % nm, 'exec'), ns)
RIN, ROWN = ns['INPUTS'], ns['OWNMOD']
OUTDd, W4d, INPd, HLDd = ns['OUTD'], ns['W4'], ns['INP'], ns['HLD']
assert HLDd == HLD and OUTDd == HLD + '/out', (HLDd, OUTDd)
NEED = [(HLDd, 'HL_ENTRY_LIST_v1.json'), (W4d, 'ts_N4_J170_D_S_z9sym_v1.json'), (W4d, 'ts_N3_S_z9sym_v1.json'),
        (W4d, 'vacres_K3_N4_sym_v1.json'), (W4d, 'vacres_K3_N3_sym_v1.json'), (INPd, 'm2_N4_J170.json.b'), (INPd, 'm2_N3_J170.json.b'),
        (OUTDd, 'm3ref_hl_v1_P16L.4.p5_z9sym.out'), (OUTDd, 'm3ref_hl_v1_P16L.3.p5_z9sym.out')]
PIN = {}
for key in NEED:
    h = RIN.get(key)
    assert h is not None and sha(os.path.join(*key)) == h, (key, h)
    PIN[key] = h
    print('PIN %s %s (the runner hl_v1 pins it so in INPUTS; the file agrees)' % (h, os.path.join(*key)))
with open(SRC) as fh:
    T = fh.read()
NREP = [0]


def rep(lab, old, new, cnt=1):
    global T
    n = T.count(old)
    assert n == cnt, (lab, n)
    T = T.replace(old, new)
    NREP[0] += 1
    print('REPLACE %s: %d occurrence(s), %d -> %d chars' % (lab, n, len(old), len(new)))


def block(lab, start, end, new):
    """replace the text from the unique start marker up to (not including) the unique end marker."""
    global T
    assert T.count(start) == 1 and T.count(end) == 1, (lab, T.count(start), T.count(end))
    i, j = T.index(start), T.index(end)
    assert i < j, lab
    old = T[i:j]
    T = T[:i] + new + T[j:]
    NREP[0] += 1
    print('BLOCK %s: %d -> %d chars' % (lab, len(old), len(new)))
    return old


DOC = '''"""m3_lawcert_hl_v1_1.py -- pk23 (code/pk23/pev/). pk22's m3_lawcert_c3k_v1.py (sha256 %(src)s) retargeted to pk23's Pev
records L, LH and LT (runner m3_run_v1_9_3_hl_v1 %(run)s, asm.N; S8's L graph [vac, int, int, vac] with one prep family L read by LH and LT;
the P0_LOG row 4589: C_w's second-order comb needs the certified J-laws of TT,0,0 and Mh,0,0), made by pk23/pev/make_m3_lawcert_hl_v1_1.py.
What changes, and nothing else:
- FAMS = (L, LH, LT), RUNF = hl_v1, the list HL_ENTRY_LIST_v1.json, the run manifest pk23/pev/MANIFEST_PEV_RUN_ABS_v1.sha256 (%(side)s; the
  frozen MANIFEST_PEV_L_RECORDS_v1_1's out/ and hand/ rows with absolute paths), the records m3_hl_<F>_N<N>_J300_hl.json against
  m3_run_v1_9_3_asm.<N>.out. The runner made the one prep L itself (PREPOF L for all three; PRODF the runner); FAMREF P16L; PREPREF the twin
  pieces m3ref_hl_v1_P16L.<N>.p5 on z9sym. The runner's folder is HLD = pk23/pev (PIN_NAMES gains HLD); pk22's pins module stays in MYD.
- The trial set is z9sym (pk11/out, W4), as the runner's: C-LAWFIELDS loads it from W4 and INPUTS pins it.
- C-NO-RESUME: the runner's item grammar and its resume items LHr1 and LHr2 (RESUME_FAMS (LH,)); the plants act on LH. The gap plant drops
  LH's first piece line, since LH's middle piece lines (k2..k4) carry units of Mhh,0,0 and complete no entry, so dropping one of them makes no
  entry gap (v1, set aside as SCRATCH_m3_lawcert_hl_v1_gapplant.py, dropped the middle line and its plant did not fire).
- The certificate is out/m3_lawcert_hl_v1_1_N<N>.json and the banner names m3_lawcert_hl_v1_1. The other gates, plants, the pins texts and the
  claim are c3k_v1's.
---- m3_lawcert_c3k_v1.py's docstring:
m3_lawcert_c3k_v1.py -- pk22 (code/pk22/m3/). m3_lawcert_c3h_v1_1.py (sha256 554fa9d3; the v1_9 delta check d7074f53:''' % dict(
    src=s0[:8], run=sr[:8], side=ss[:8])
rep('doc', '''"""m3_lawcert_c3k_v1.py -- pk22 (code/pk22/m3/). m3_lawcert_c3h_v1_1.py (sha256 554fa9d3; the v1_9 delta check d7074f53:''', DOC)
rep('usage', "    print('usage: m3_lawcert_c3k_v1.py ITEM LIM", "    print('usage: m3_lawcert_hl_v1_1.py ITEM LIM")
rep('banner', "out('m3_lawcert_c3k_v1 N %s LIM %d; script sha256 %s; python %s'", "out('m3_lawcert_hl_v1_1 N %s LIM %d; script sha256 %s; python %s'")
rep('folders', "OUTD = MYD + '/out'\nHANDD = MYD + '/hand'   # m3_lawcert_c3h_v1: the c3h hand-offs (C-NO-RESUME)\n",
    "HLD = CODEDIR + '/pk23/pev'   # m3_lawcert_hl_v1: pk23's Pev runner folder (its records, asm outputs, hand-offs; this certificate)\n"
    "OUTD = HLD + '/out'   # m3_lawcert_hl_v1\nHANDD = HLD + '/hand'   # m3_lawcert_hl_v1: the hl_v1 hand-offs (C-NO-RESUME)\n")

# ---- the configuration and pin block (PSX .. the end of INPUTS)
oldcfg = T[T.index("PSX = CODEDIR + '/pk22/midrow/psixy'"):T.index("FORMAT = 'M3_LAWCERT_v1'")]
mods = [ln for ln in oldcfg.split('\n') if ln.startswith("    (OWN, 'm3_")]
assert len(mods) == 8, len(mods)
for ln in mods:
    f = ln.split("'")[1]
    assert ROWN.get(f) and ("'%s'" % ROWN[f]) in ln, f   # the same module pins as the runner's OWNMOD
pinln = [ln for ln in oldcfg.split('\n') if ln.startswith("    (MYD, 'm3_lawcert_c3h_v1_pins.py'): '")]
assert len(pinln) == 1
NEWCFG = ("PSX = CODEDIR + '/pk22/midrow/psixy'   # the runner's PSX (no input of this certificate)\n"
          "FAMS = ('L', 'LH', 'LT')   # m3_lawcert_hl_v1: pk23's three Pev records (option B; the rows 4409, 4435)\n"
          "RUNF = 'm3_run_v1_9_3_hl_v1.py'   # m3_lawcert_hl_v1: the runner whose prep, entry pieces and asm wrote the records\n"
          "PREPOF = {'L': 'L', 'LH': 'L', 'LT': 'L'}   # m3_lawcert_hl_v1: one prep family L (the runner's PREPOF)\n"
          "PRODF = {'L': (HLD, RUNF), 'LH': (HLD, RUNF), 'LT': (HLD, RUNF)}   # m3_lawcert_hl_v1: the runner produced the L prep\n"
          "FAMREF = {'L': 'P16L', 'LH': 'P16L', 'LT': 'P16L'}   # m3_lawcert_hl_v1: the float family of the PREPJSON whose radii the prep took\n"
          "PREPREF = {'L': (OUTD, 'm3ref_hl_v1_P16L.%d.p5_z9sym.out'), 'LH': (OUTD, 'm3ref_hl_v1_P16L.%d.p5_z9sym.out'), "
          "'LT': (OUTD, 'm3ref_hl_v1_P16L.%d.p5_z9sym.out')}   # the runner's PREPREF\n"
          "LISTF = 'HL_ENTRY_LIST_v1.json'   # m3_lawcert_hl_v1: the Pev list\n"
          "SIDEF = (HLD, 'MANIFEST_PEV_RUN_ABS_v1.sha256')   # m3_lawcert_hl_v1: the run manifest (absolute paths)\n"
          "PINS_STATIC = {   # m3_lawcert_s9h_v1: (folder, file) -> sha256, read by every item\n" + '\n'.join(mods) + '\n'
          "    (HLD, RUNF): '%s',   # m3_lawcert_hl_v1: the runner hl_v1\n" % sr + pinln[0] + '\n'
          "    (HLD, LISTF): '%s',\n" % PIN[(HLDd, 'HL_ENTRY_LIST_v1.json')] +
          "    SIDEF: '%s',\n}\n" % ss +
          "INPUTS = {   # m3_lawcert_s9h_v1: read by the items 4 and 3 (C-LAWFIELDS); m3_lawcert_hl_v1: z9sym and the P16L twins\n" +
          ''.join("    (%s, '%s'): '%s',\n" % ({W4d: 'W4', INPd: 'INP', OUTDd: 'OUTD'}[d], f, PIN[(d, f)]) for (d, f) in NEED[1:]) + "}\n")
block('config', "PSX = CODEDIR + '/pk22/midrow/psixy'", "FORMAT = 'M3_LAWCERT_v1'", NEWCFG)
rep('pin-names', "PIN_NAMES = ('CODEDIR', 'OWN', 'C2B', 'INP', 'W4', 'MYD', 'OUTD', 'OUTD_IN', 'HANDD', 'PSX', 'OWNMOD', 'INPUTS')   # m3_lawcert_c3k_v1: + PSX",
    "PIN_NAMES = ('CODEDIR', 'OWN', 'C2B', 'INP', 'W4', 'MYD', 'HLD', 'OUTD', 'OUTD_IN', 'HANDD', 'PSX', 'OWNMOD', 'INPUTS')   # m3_lawcert_hl_v1: + HLD")
rep('myd-runf', "(MYD, RUNF)", "(HLD, RUNF)", T.count("(MYD, RUNF)"))
rep('myd-join-runf', "os.path.join(MYD, RUNF)", "os.path.join(HLD, RUNF)", T.count("os.path.join(MYD, RUNF)"))
rep('myd-listf', "(MYD, LISTF)", "(HLD, LISTF)", T.count("(MYD, LISTF)"))
rep('myd-join-listf', "os.path.join(MYD, LISTF)", "os.path.join(HLD, LISTF)", T.count("os.path.join(MYD, LISTF)"))
rep('asm', "ASM = os.path.join(OUTD, 'm3_run_v1_9_3_asm.%d_c3k.out' % NN)", "ASM = os.path.join(OUTD, 'm3_run_v1_9_3_asm.%d.out' % NN)")
rep('recs', "RECS[f] = RDR.load(os.path.join(OUTD, 'm3_c3k_%s_N%d_J300_c3k.json' % (f, NN)), ASM, J_REF, NN)",
    "RECS[f] = RDR.load(os.path.join(OUTD, 'm3_hl_%s_N%d_J300_hl.json' % (f, NN)), ASM, J_REF, NN)")
rep('side', "    SIDE = os.path.join(*SIDEF)   # m3_lawcert_c3k_v1: the c3k run manifest (absolute paths), pinned in PINS_STATIC",
    "    SIDE = os.path.join(*SIDEF)   # m3_lawcert_hl_v1: the hl run manifest (absolute paths), pinned in PINS_STATIC")
rep('bind-msg', "'(the c3k records through m3_reader_v6_3.load against %s;", "'(the hl records through m3_reader_v6_3.load against %s;")
rep('tsf', "TSF = {4: 'ts_N4_J170_D_S_z9symxy_v1.json', 3: 'ts_N3_S_z9symxy_v1.json'}[NN]   # m3_lawcert_c3k_v1: z9symxy, the runner's trial set\n"
    "TS = ENT.load_trial(os.path.join(PSX, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)",
    "TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]   # m3_lawcert_hl_v1: z9sym, the runner's trial set\n"
    "TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)")
rep('name', "NAME = 'm3_lawcert_c3k_v1_N%d.json' % NN", "NAME = 'm3_lawcert_hl_v1_1_N%d.json' % NN")
rep('rt-msg', "against the two loaded records: %s;", "against the three loaded records: %s;")
rep('cp-sha', "c['records']['E4N'].__setitem__('sha256', flip(c['records']['E4N']['sha256']))", "c['records']['LH'].__setitem__('sha256', flip(c['records']['LH']['sha256']))")
rep('cp-add', "c['entries'].__setitem__('E4N:ZZZ', copy.deepcopy(c['entries'][F0]))", "c['entries'].__setitem__('LH:ZZZ', copy.deepcopy(c['entries'][F0]))")
rep('cp-pop', "c['records'].pop('E4N')", "c['records'].pop('LH')")

# ---- C-NO-RESUME: the runner's item grammar, its resume family LH, and the plants on LH
i0, i1 = T.index("ITEM_RE_WANT = r'(E4Da"), T.index("stage('C-LAWFIELDS')")
nr = T[i0:i1]
old_re = "ITEM_RE_WANT = r'(E4Da|E4Na[1-4]|(E4D|E4N)p([1-9]|1[0-9])|(E4D|E4N)k[1-9]|E4Nr[12]|asm)\\.(4|3)'   # m3_lawcert_c3k_v1: the runner's item grammar"
assert nr.count(old_re) == 1, 'item grammar'
rtre = [st for st in rtree.body if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) and st.targets[0].id == 'ITEM_RE']
assert len(rtre) == 1
want_re = rtre[0].value.value
nr = nr.replace(old_re, "ITEM_RE_WANT = %r   # m3_lawcert_hl_v1: the runner's item grammar" % want_re)
nr = nr.replace('E4Nr1 and E4Nr2', 'LHr1 and LHr2').replace("'E4D'", "'LT'").replace("'E4N'", "'LH'").replace('E4N', 'LH')
nr = nr.replace("res[('LH', 'IhR,10,0')] = None", "res[('LH', 'Mh,0,0')] = None")
old_gap = "gap_lines = [ln for ln in ASM_LINES if ln != mid[len(mid) // 2]]"
assert nr.count(old_gap) == 1, 'gap plant'
nr = nr.replace(old_gap, "gap_lines = [ln for ln in ASM_LINES if ln != mid[0]]   # m3_lawcert_hl_v1_1: LH's middle piece lines cover no entry (units "
                "carried), so the gap plant drops LH's first piece line")
assert 'E4' not in nr and 'IhR' not in nr, 'leftover'
T = T[:i0] + nr + T[i1:]
NREP[0] += 1
print('BLOCK no-resume: family names and item grammar (%d chars)' % len(nr))
CODE_ = T[T.index('"""', T.index('"""') + 3) + 3:]   # the code after the module docstring (the docstrings keep their history)
for bad_txt in ("'C3K_ENTRY_LIST_v1_1.json'", "MANIFEST_E4_C3K_v1", "'m3_c3k_%s", "_c3k.out", "z9symxy", "E4D", "E4N", "(MYD, RUNF)", "E4M"):
    assert bad_txt not in CODE_, bad_txt
with open(DST, 'x') as fh:
    fh.write(T)
print('REPLACEMENTS %d' % NREP[0])
print('WROTE %s %s' % (hashlib.sha256(T.encode('utf-8')).hexdigest(), DST))
