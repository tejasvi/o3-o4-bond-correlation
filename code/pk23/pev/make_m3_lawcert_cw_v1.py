#!/usr/bin/env python3
"""make_m3_lawcert_cw_v1.py (pk23; C_w variant B, the P0_LOG rows 4589 and 4598): writes (mode 'x') pk23/pev/m3_lawcert_cw_v1.py, the
law certificate of pk23's C_w record LC (runner m3_run_v1_9_3_cw_v1, asmc.N), from pk23's m3_lawcert_hl_v1_1.py (8d5fe3c7) by exact
replacements of asserted counts and two block replacements (the configuration and pin block; the C-NO-RESUME block's family names, item
grammar and gap plant). What differs in substance from hl_v1_1: the entry runner cw_v1 read the L prep that m3_run_v1_9_3_hl_v1 produced, so
PRODF names hl_v1 (a foreign prep producer, as pk22's m3_lawcert_c3h_v1_1 did for H4TH): C-PINS asks the runner's INPUTS for the list and
hl_v1; RUN_PRODUCERS holds both runners (C-PREP16 (c) reads both); PRUN is hl_v1's source; and the asm item is asmc. The run manifest is
pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 (absolute paths; written after the cw chains). Every new pin is copied from the runner cw_v1's own
OWNMOD and INPUTS (read by ast) and checked against the file, or computed from the file; no hash is typed in full. The gap plant drops the first
LC piece line that completes at least one entry and has a later piece line after it (then the asm walk must report LC:asm-gap); if there is no
such line, it drops the last line that completes an entry (then LC:asm-end). Usage: make_m3_lawcert_cw_v1.py. Prints the output's sha256."""
import ast, hashlib, os

W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
SRC, DST = HLD + '/m3_lawcert_hl_v1_1.py', HLD + '/m3_lawcert_cw_v1.py'
RUNF, PRODR = HLD + '/m3_run_v1_9_3_cw_v1.py', HLD + '/m3_run_v1_9_3_hl_v1.py'
SIDE = HLD + '/MANIFEST_CW_RUN_ABS_v1.sha256'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


assert os.path.dirname(DST) == os.path.dirname(os.path.abspath(__file__)) and not os.path.exists(DST), DST
s0, sr, sp, ss = sha(SRC), sha(RUNF), sha(PRODR), sha(SIDE)
print('SOURCE %s %s\nRUNNER %s %s\nPRODUCER %s %s\nSIDE %s %s' % (s0, SRC, sr, RUNF, sp, PRODR, ss, SIDE))
assert s0.startswith('fda54b63') and sr.startswith('2b755696') and sp.startswith('57f73e77'), (s0, sr, sp)
rtree = ast.parse(open(RUNF).read())
ns = {'__builtins__': {}}
for nm in ('CODEDIR', 'OWN', 'C2B', 'INP', 'W4', 'MYD', 'HLD', 'OUTD', 'OUTD_IN', 'HANDD', 'PSX', 'OWNMOD', 'INPUTS'):
    top = [st for st in rtree.body if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) and st.targets[0].id == nm]
    assert len(top) == 1, nm
    exec(compile(ast.Module(body=[top[0]], type_ignores=[]), 'runner:%s' % nm, 'exec'), ns)
RIN, ROWN = ns['INPUTS'], ns['OWNMOD']
OUTDd, W4d, INPd, HLDd = ns['OUTD'], ns['W4'], ns['INP'], ns['HLD']
NEED = [(HLDd, 'HL_CW_ENTRY_LIST_v1.json'), (HLDd, 'm3_run_v1_9_3_hl_v1.py'), (W4d, 'ts_N4_J170_D_S_z9sym_v1.json'), (W4d, 'ts_N3_S_z9sym_v1.json'),
        (W4d, 'vacres_K3_N4_sym_v1.json'), (W4d, 'vacres_K3_N3_sym_v1.json'), (INPd, 'm2_N4_J170.json.b'), (INPd, 'm2_N3_J170.json.b'),
        (OUTDd, 'm3ref_hl_v1_P16L.4.p5_z9sym.out'), (OUTDd, 'm3ref_hl_v1_P16L.3.p5_z9sym.out')]
PIN = {}
for key in NEED:
    h = RIN.get(key)
    assert h is not None and sha(os.path.join(*key)) == h, (key, h)
    PIN[key] = h
    print('PIN %s %s (the runner cw_v1 pins it so in INPUTS; the file agrees)' % (h, os.path.join(*key)))
with open(SRC) as fh:
    T = fh.read()
NREP = [0]


def rep(lab, old, new, cnt=1):
    global T
    n = T.count(old)
    assert n == cnt, (lab, n)
    T = T.replace(old, new)
    NREP[0] += 1
    print('REPLACE %s: %d occurrence(s)' % (lab, n))


DOC = '''"""m3_lawcert_cw_v1.py -- pk23 (code/pk23/pev/). pk23's m3_lawcert_hl_v1_1.py (sha256 %(src)s) retargeted to pk23's C_w record LC
(runner m3_run_v1_9_3_cw_v1 %(run)s, asmc.N; the (1,1) block of |S M_c u~_x|^2 on S8's L graph with the pairs (0,2), (9,11), (1,4), (7,10);
the P0_LOG rows 4589, 4598), made by pk23/pev/make_m3_lawcert_cw_v1.py. What changes, and nothing else:
- FAMS = (LC,), RUNF = cw_v1, the list HL_CW_ENTRY_LIST_v1.json, the run manifest pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 (%(side)s, absolute
  paths), the record m3_cw_LC_N<N>_J300_cw.json against m3_run_v1_9_3_asmc.<N>.out (the asm item is asmc).
- The L prep was produced by m3_run_v1_9_3_hl_v1 (%(prod)s), not by the entry runner: PREPOF LC -> L, PRODF LC -> hl_v1 (a foreign prep producer,
  as pk22's m3_lawcert_c3h_v1_1 for H4TH); C-PINS asks the runner's INPUTS for the list and hl_v1; RUN_PRODUCERS holds both runners, so
  C-PREP16 (c) reads both; PRUN is hl_v1's source; C-PRODUCER compares the record's prep16 prep_script with hl_v1's pin.
- C-NO-RESUME: the runner's item grammar and its resume items LCr1 and LCr2 (RESUME_FAMS (LC,)); the plants act on LC; the gap plant drops the
  first LC piece line that completes an entry and has a later piece line (LC:asm-gap), else the last line that completes an entry (LC:asm-end).
- The certificate is out/m3_lawcert_cw_v1_N<N>.json and the banner names m3_lawcert_cw_v1. The other gates, plants, the pins texts and the
  claim are hl_v1_1's.
---- m3_lawcert_hl_v1_1.py's docstring:
m3_lawcert_hl_v1_1.py -- pk23 (code/pk23/pev/). pk22's m3_lawcert_c3k_v1.py (sha256''' % dict(src=s0[:8], run=sr[:8], side=ss[:8], prod=sp[:8])
rep('doc', '''"""m3_lawcert_hl_v1_1.py -- pk23 (code/pk23/pev/). pk22's m3_lawcert_c3k_v1.py (sha256''', DOC)
rep('usage', "    print('usage: m3_lawcert_hl_v1_1.py ITEM LIM", "    print('usage: m3_lawcert_cw_v1.py ITEM LIM")
rep('banner', "out('m3_lawcert_hl_v1_1 N %s LIM", "out('m3_lawcert_cw_v1 N %s LIM")
rep('name', "NAME = 'm3_lawcert_hl_v1_1_N%d.json' % NN", "NAME = 'm3_lawcert_cw_v1_N%d.json' % NN")
oldcfg = T[T.index("FAMS = ('L', 'LH', 'LT')"):T.index("FORMAT = 'M3_LAWCERT_v1'")]
mods = [ln for ln in oldcfg.split('\n') if ln.startswith("    (OWN, 'm3_")]
assert len(mods) == 8, len(mods)
for ln in mods:
    f = ln.split("'")[1]
    assert ROWN.get(f) and ("'%s'" % ROWN[f]) in ln, f
pinln = [ln for ln in oldcfg.split('\n') if ln.startswith("    (MYD, 'm3_lawcert_c3h_v1_pins.py'): '")]
assert len(pinln) == 1
NEWCFG = ("FAMS = ('LC',)   # m3_lawcert_cw_v1: pk23's C_w record (variant B; the rows 4589, 4598)\n"
          "RUNF = 'm3_run_v1_9_3_cw_v1.py'   # m3_lawcert_cw_v1: the runner whose entry pieces and asmc wrote the record\n"
          "PRODR = 'm3_run_v1_9_3_hl_v1.py'   # m3_lawcert_cw_v1: the runner that produced the L prep (pieces Lp1..)\n"
          "PREPOF = {'LC': 'L'}   # m3_lawcert_cw_v1: LC read L's prep (the runner's PREPOF)\n"
          "PRODF = {'LC': (HLD, PRODR)}   # m3_lawcert_cw_v1: a foreign prep producer, hl_v1\n"
          "FAMREF = {'LC': 'P16L'}   # m3_lawcert_cw_v1: the float family of the PREPJSON whose radii the prep took\n"
          "PREPREF = {'LC': (OUTD, 'm3ref_hl_v1_P16L.%d.p5_z9sym.out')}   # the runner's PREPREF\n"
          "LISTF = 'HL_CW_ENTRY_LIST_v1.json'   # m3_lawcert_cw_v1: the C_w list\n"
          "SIDEF = (HLD, 'MANIFEST_CW_RUN_ABS_v1.sha256')   # m3_lawcert_cw_v1: the run manifest (absolute paths)\n"
          "PINS_STATIC = {   # m3_lawcert_s9h_v1: (folder, file) -> sha256, read by every item\n" + '\n'.join(mods) + '\n'
          "    (HLD, RUNF): '%s',   # m3_lawcert_cw_v1: the runner cw_v1\n" % sr +
          "    (HLD, PRODR): '%s',   # m3_lawcert_cw_v1: the prep producer hl_v1\n" % sp + pinln[0] + '\n'
          "    (HLD, LISTF): '%s',\n" % PIN[(HLDd, 'HL_CW_ENTRY_LIST_v1.json')] +
          "    SIDEF: '%s',\n}\n" % ss +
          "INPUTS = {   # m3_lawcert_s9h_v1: read by the items 4 and 3 (C-LAWFIELDS); m3_lawcert_cw_v1: z9sym and the P16L twins\n" +
          ''.join("    (%s, '%s'): '%s',\n" % ({W4d: 'W4', INPd: 'INP', OUTDd: 'OUTD'}[d], f, PIN[(d, f)]) for (d, f) in NEED[2:]) + "}\n")
i0, i1 = T.index("FAMS = ('L', 'LH', 'LT')"), T.index("FORMAT = 'M3_LAWCERT_v1'")
T = T[:i0] + NEWCFG + T[i1:]
NREP[0] += 1
print('BLOCK config')
rep('want-inp', "want_inp.update({k: PINS_STATIC[k] for k in ((HLD, LISTF),)})   # m3_lawcert_c3k_v1: the list (the runner made its own preps)",
    "want_inp.update({k: PINS_STATIC[k] for k in ((HLD, LISTF), (HLD, PRODR))})   # m3_lawcert_cw_v1: the list and the prep producer hl_v1")
rep('asm', "ASM = os.path.join(OUTD, 'm3_run_v1_9_3_asm.%d.out' % NN)", "ASM = os.path.join(OUTD, 'm3_run_v1_9_3_asmc.%d.out' % NN)")
rep('asm-first', "ASM_FIRST.startswith('m3_run_v1_9_3 item asm.%d LIM ' % NN)", "ASM_FIRST.startswith('m3_run_v1_9_3 item asmc.%d LIM ' % NN)")
rep('recs', "RECS[f] = RDR.load(os.path.join(OUTD, 'm3_hl_%s_N%d_J300_hl.json' % (f, NN)), ASM, J_REF, NN)",
    "RECS[f] = RDR.load(os.path.join(OUTD, 'm3_cw_%s_N%d_J300_cw.json' % (f, NN)), ASM, J_REF, NN)")
rep('bind-msg', "'(the hl records through m3_reader_v6_3.load against %s;", "'(the cw record through m3_reader_v6_3.load against %s;")
rep('runprod', "RUN_PRODUCERS = ((HLD, RUNF),)", "RUN_PRODUCERS = ((HLD, RUNF), (HLD, PRODR))")
rep('prun', "PRUN = RSRC16[(HLD, RUNF)]", "PRUN = RSRC16[(HLD, PRODR)]")
rep('prep16-msg', "the runner (%s), which made its own preps, builds", "the runner and the prep producer (%s) build")
rep('rt-msg', "against the three loaded records: %s;", "against the one loaded record: %s;")
rep('cp-sha', "c['records']['LH'].__setitem__('sha256', flip(c['records']['LH']['sha256']))", "c['records']['LC'].__setitem__('sha256', flip(c['records']['LC']['sha256']))")
rep('cp-add', "c['entries'].__setitem__('LH:ZZZ', copy.deepcopy(c['entries'][F0]))", "c['entries'].__setitem__('LC:ZZZ', copy.deepcopy(c['entries'][F0]))")
rep('cp-pop', "c['records'].pop('LH')", "c['records'].pop('LC')")
# ---- C-NO-RESUME: the runner's grammar, its resume family LC, the plants on LC
i0, i1 = T.index("ITEM_RE_WANT = "), T.index("stage('C-LAWFIELDS')")
nr = T[i0:i1]
rtre = [st for st in rtree.body if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) and st.targets[0].id == 'ITEM_RE']
assert len(rtre) == 1
lines = nr.split('\n')
assert lines[0].startswith('ITEM_RE_WANT = ')
lines[0] = "ITEM_RE_WANT = %r   # m3_lawcert_cw_v1: the runner's item grammar" % rtre[0].value.value
nr = '\n'.join(lines)
old_gap = "gap_lines = [ln for ln in ASM_LINES if ln != mid[0]]"
assert nr.count(old_gap) == 1
new_gap = ("_AP = [AP_RE.fullmatch(ln) for ln in mid]\n"
           "_ne = [i for i, m_ in enumerate(_AP) if m_ is not None and int(m_.group(5)) >= int(m_.group(4))]   # lines that complete an entry\n"
           "_gi = next((i for i in _ne if i < len(mid) - 1), _ne[-1] if _ne else None)   # m3_lawcert_cw_v1: a line with a later line, else the last\n"
           "GAP_WANT = 'LC:asm-gap' if _gi is not None and _gi < len(mid) - 1 else 'LC:asm-end'\n"
           "gap_lines = [ln for ln in ASM_LINES if _gi is None or ln != mid[_gi]]")
nr = nr.replace(old_gap, new_gap)
nr = nr.replace("res[('LH', 'Mh,0,0')] = None", "res[('LC', 'Cx1,1,1')] = None")
nr = nr.replace("'LH:asm-gap'", "GAP_WANT")
nr = nr.replace('LHr1 and LHr2', 'LCr1 and LCr2').replace("'LT'", "'L'").replace("'LH'", "'LC'").replace('LH', 'LC')
assert 'LH' not in nr and 'Mh,0,0' not in nr, 'leftover'
T = T[:i0] + nr + T[i1:]
NREP[0] += 1
print('BLOCK no-resume')
CODE_ = T[T.index('"""', T.index('"""') + 3) + 3:]
for bad_txt in ("'m3_hl_%s", "asm.%d.out'", "'LH'", "'LT'", "HL_ENTRY_LIST_v1.json'"):
    assert bad_txt not in CODE_, bad_txt
with open(DST, 'x') as fh:
    fh.write(T)
print('REPLACEMENTS %d' % NREP[0])
print('WROTE %s %s' % (hashlib.sha256(T.encode('utf-8')).hexdigest(), DST))
