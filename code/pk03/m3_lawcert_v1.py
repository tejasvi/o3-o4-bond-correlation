#!/usr/bin/env python3
"""m3_lawcert_v1.py -- pk03 (code/pk03/). Certified J-laws for M3's S8 records without a rerun (PLAN_M3_LAWCERT_v1 255a9d70;
SOUND, the AST gate's conditions 1-5 with two additions, banded
<= uniform err as a sanity gate and arb chi-square tails rounded outward). One item per N. It reads the five m3_run_v1_8 records of that
N, checks their binding and the producer's pins, checks the bar's term structure on the exact pinned files, recomputes every law
parameter, and after every gate and plant writes out/m3_lawcert_v1_N<N>.json (FORMAT M3_LAWCERT_v1, read by m3_reader_v6.load_lawcert)
with a per-entry LAW_CLAIM, named on a RECORD line. No entry is recomputed.
  C-HASH        every pinned file has its full sha256: this folder's modules, m3_run_v1_8 and its manifest, m3_reader_v6, the pins
                module m3_lawcert_v1_pins (exact source texts) and the run's inputs (PLANT-HASH).
  C-PINS        MANIFEST_m3_run_v1_8 (5b5b7861) lists the run, bar, scal, graph, series, major, entries and record modules and the
                run's inputs with this script's full sha256s; the asm output's first line names m3_run_v1_8's full sha256 (PLANT-PINS).
  C-BIND        each record through m3_reader_v6.load (asm VERDICT exactly VALID, its RECORD line and sha; laws parsed and checked on
                every free entry); MANIFEST_m3_run_v1_8_asm.N names exactly the asm output and the five records with their sha256s;
                each record's entries are the list's keys of its graph, with the list's parity.
  C-LAW-REM     the item 3, structural: a t-valuation interpreter over the AST of m3_bar_v10's Prep.bound, stage_u and stage_c
                (TVal below). It refuses by default; every name in B_rem's four terms resolves to exactly one binding, a direct
                statement with a value; allow-listed atoms (nonnegative, fixed at J_REF by Lemma U) are pinned by their exact source
                texts (m3_lawcert_v1_pins), each binding of the atom in its function is one of them, and none mentions t, T or J;
                the stage results self.rE, self.nC8, self.nC6 and self.nE have one assignment in the module (the restore from
                hand-offs takes the same names, Prep.UK/CK, pinned in C-LAW-SHAPE). Each term must be a polynomial in t with
                nonnegative fixed coefficients and valuation >= 4, and l2 (the tail factor) one of valuation >= 0. Positive
                control, then nine plants that must each refuse: six of the plan, a second binding (condition 2), and two
                allow-list plants (a pin that is not the name's definition; a t-dependent name with its own definition, condition 4).
  C-LAW-SHAPE   the tail, ann and far statements, sup_F, norm_any, chi_tail_up, ive1, logtree, logmain, far_base, the bound's
                return, Prep.UK/CK, __init__'s t, rates, tilts and restore, laws_of, the entry lines that write laws, and the record
                writer equal their pinned source texts as ASTs, each in its named place (three plants).
  C-LAWFIELDS   each free entry's laws equal an independent recompute from the pinned inputs: rem_tpow 4; tail = {n: g.n,
                J_REF: 300, a_G: [[a_v, up(G_vv)]]} with the graph's G_vv and m3ref_v1_10's a_v (the run's manifest l.17-27); ann the
                same with tilt_p's G_vv (rates from ap); far_cF = m_F + n(V-1)/2 with m_F from the pinned sup_F, which must be >= this
                script's own exponent max(d - i) over the nonzero coefficients (negative values allowed, with the constant term's 0;
                ); far_rate = down(alpha_lo - c_F/300).
  C-MONO-FAR    every recomputed far rate has its lower end > 0.
  C-BAND        sanity: LAWCERT_CLAIM's right side in arb (prec 128; P2(s) = e^(-s/2), P3(s) = erfc(sqrt(s/2)) + sqrt(2s/pi) e^(-s/2),
                ratio upper ends) at J = 300, 600, 1000 and 3000: <= err (1 + 2^-30) at 300, <= err beyond, and non-increasing.
  C-LAWCERT-RT  the certificate parses through m3_reader_v6.loads_lawcert against the loaded records; twelve plants each refused
                (the plan's nine, the records map without one loaded record, a non-canonical exact string, and a writing
                job whose VERDICT line is VERDICT VALID-PRECERT).
Arguments: N LIM (N = 3 or 4; LIM = RLIMIT_CPU soft limit in s, 5..540).
Run: D=/mnt/g2/release/root/code/pk03; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/m3_lawcert_v1.py N LIM > $D/out/m3_lawcert_v1_N.out 2> $D/out/m3_lawcert_v1_N.err
"""
import resource, sys, time, hashlib, signal, os, json, re, copy, ast, textwrap

if len(sys.argv) != 3 or sys.argv[1] not in ('3', '4'):
    print('usage: m3_lawcert_v1.py N LIM   (N = 3 or 4; LIM = RLIMIT_CPU soft limit in s, 5..540)')
    sys.exit(2)
NN = int(sys.argv[1])
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
STAGE = ['start']


def cpu():
    return time.process_time()


def out(line):
    print(line, flush=True)


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    sys.stdout.flush()
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk03'
OUTD = OWN + '/out'
INP = CODEDIR + '/pk10/scratch'
W4 = CODEDIR + '/pk11/out'
J_REF = 300
FAMS = ('D', 'N', 'E2', 'E3', 'FF')
GMAP = {'D': 'D', 'N': 'N', 'E2': 'mix', 'E3': 'E3', 'FF': 'free2'}   # the list's graph name -> m3_entries_v3's
OWNMOD = {
    'm3_scal_v2.py': 'd22d3ad696074d4235f0fd31b026477e87f96f5d4b5331e29ab8d399e1e8f054',
    'm3_graph_v3.py': '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    'm3_series_v2.py': '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    'm3_major_v2.py': '89dd5a2184a511d4dea39fb3c558501e9738af118be9d41f2ac4b2d4b8d7b016',
    'm3_bar_v10.py': '9a4de5dd54faff8aa3c1c047f870d198d27d12646fbff0c973ce0aff7903a0d5',
    'm3_entries_v3.py': '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    'm3_record_v4.py': '2c8a53efb5170d6c6e320bd814c824e69d2ccdd73c57cf87a9130b796109e30f',
    'm3_run_v1_8.py': 'be0c1be3eadabf2f14f40d84f7a2482f2b75aada522b0e267146008cd700da3b',
    'MANIFEST_m3_run_v1_8.sha256': '3abab2c1b4da2966af3cd12c1644970360616bd0dcae94882af5ef9d5979f1cc',
    'm3_reader_v6.py': 'e2360f2ac362151456d6b28ad199e8f220537bfbe86c3bedcb315c6a8504d5dd',
    'm3_lawcert_v1_pins.py': 'a6abde93a8a263ad536f96675f4fce97bd30341d016109d9deeb16f607336862',
}
INPUTS = {
    (W4, 'S8_ENTRY_LIST_v3.json'): 'aa7cc0c938c23fcf4ba3510fdc0333055d3059b71a4147cc8f0de49c2b04cf00',
    (W4, 'ts_N4_J170_D_S_z9sym_v1.json'): 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    (W4, 'ts_N3_S_z9sym_v1.json'): 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    (W4, 'vacres_K3_N4_sym_v1.json'): 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    (W4, 'vacres_K3_N3_sym_v1.json'): 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    (INP, 'm2_N4_J170.json.b'): '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    (INP, 'm2_N3_J170.json.b'): '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    (OUTD, 'm3ref_v1_10_V3D.4.0-32_z9sym.out'): '7540647500f6c4368ad47967308b872224e08cbcaa645a1cf20acb469d9c5307',
    (OUTD, 'm3ref_v1_10_V3D.4.33-65_z9sym.out'): '0b4c99038b245432b71e66e0ad88903b374f68b3d9b5a6521049b4c5d2098362',
    (OUTD, 'm3ref_v1_10_V3D.3.all_z9sym.out'): '8a045f0bb2579e91f5a937761bacf0b54af6632b6e2a5b5307d3a652af74bc9a',
    (OUTD, 'm3ref_v1_10_V3N.4.all_z9sym.out'): '65a8145b6f2ce35aa3692ab3f89447aa52c4420220408f3c028ee67bf7fdf0c2',
    (OUTD, 'm3ref_v1_10_V3N.3.all_z9sym.out'): 'd12836039cc0390feed5435486459530a781cc75865f1ecf8b95f497a0421945',
    (OUTD, 'm3ref_v1_10_V3E2.4.all_z9sym.out'): 'de30ea911622306cc88b231f9dbfd17808a9495c150e16f71b7a5f50451b9469',
    (OUTD, 'm3ref_v1_10_V3E2.3.all_z9sym.out'): '6615ba0adaa496be3c1fb5658b9955b5edc7659b7aeb82ef72ef9c722edc335f',
    (OUTD, 'm3ref_v1_10_V3E3.4.all_z9sym.out'): '5cf7ab639fbc53f3ae694e6d073276946a07d82aa71a80e5cc54219f37205cc1',
    (OUTD, 'm3ref_v1_10_V3E3.3.all_z9sym.out'): '10509eb7880bab08f9012527d5e0fd5e46f75942925c3562d780996a0361946b',
    (OUTD, 'm3ref_v1_10_V3FF.4.all_z9sym.out'): 'fe8059a32c1b382355f2429b04efea37812555db5f444f2285b2208e8c6f1ffe',
    (OUTD, 'm3ref_v1_10_V3FF.3.all_z9sym.out'): '47564e4f68cff3569c549676df85c05c30ffa2c6dd888122c8aee41158ee21c4',
}
REFOUT = {'D': (['m3ref_v1_10_V3D.4.0-32_z9sym.out', 'm3ref_v1_10_V3D.4.33-65_z9sym.out'] if NN == 4 else ['m3ref_v1_10_V3D.3.all_z9sym.out']),
          'N': ['m3ref_v1_10_V3N.%d.all_z9sym.out' % NN], 'E2': ['m3ref_v1_10_V3E2.%d.all_z9sym.out' % NN],
          'E3': ['m3ref_v1_10_V3E3.%d.all_z9sym.out' % NN], 'FF': ['m3ref_v1_10_V3FF.%d.all_z9sym.out' % NN]}
FORMAT = 'M3_LAWCERT_v1'
CLAIM = ('for every J >= J_REF, t = 1/J: |I(J)/main(J) - sum_k ak[k] t^k| <= rem (J_REF/J)^4 + tail (P(J; tail)/P(J_REF; tail))^(1/2) '
         '+ ann (P(J; ann)/P(J_REF; ann))^(1/2) + far exp(-far_rate (J - J_REF)) + sum_k ak_rad[k] t^k, where rem, tail, ann, far are '
         'the entry\'s B parts, P(J; x) = sum over the pairs [a, G] of laws.x.a_G of Prob(chi^2_n > J a / G) with n = laws.x.n, and '
         'far_rate = laws.far_rate (Lemma U, U3: PLAN_M3_CODE_v1_2 sect. C; PLAN_M3_LAWCERT_v1 sect. 3)')
FAILS, NOFIRE = [], []


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def finish():
    out('STAGE-CPU total %.2f s' % cpu())
    if FAILS or NOFIRE:
        out('VERDICT INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE]))
    else:
        out('VERDICT VALID')


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tsha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def flip(h):
    return h[:-1] + ('0' if h[-1] != '0' else '1')


def stage(name):
    STAGE[0] = name
    out('STAGE-CPU %s start %.2f s' % (name, cpu()))


SELF_SHA = sha(os.path.abspath(__file__))
out('m3_lawcert_v1 N %d LIM %d; script sha256 %s; python %s' % (NN, LIM, SELF_SHA, sys.version.split()[0]))
stage('C-HASH')
bad = [f for f, h in OWNMOD.items() if not os.path.exists(os.path.join(OWN, f)) or sha(os.path.join(OWN, f)) != h]
bad += [f for (d, f), h in INPUTS.items() if not os.path.exists(os.path.join(d, f)) or sha(os.path.join(d, f)) != h]
gate('C-HASH', not bad, '(%d own files, %d inputs)%s' % (len(OWNMOD), len(INPUTS), (': changed or missing ' + ', '.join(bad)) if bad else ''))
plant('PLANT-HASH', sha(os.path.join(OWN, 'm3_bar_v10.py')) != flip(OWNMOD['m3_bar_v10.py']), '(m3_bar_v10 against its sha256 with the last digit changed)')
if FAILS:
    finish()
    sys.exit(1)

stage('C-PINS')
MAN = {}
with open(os.path.join(OWN, 'MANIFEST_m3_run_v1_8.sha256')) as fh:
    for ln in fh:
        h_, p_ = ln.rstrip('\n').split('  ', 1)
        MAN[p_] = h_
want_man = {f: OWNMOD[f] for f in ('m3_run_v1_8.py', 'm3_scal_v2.py', 'm3_graph_v3.py', 'm3_series_v2.py', 'm3_major_v2.py', 'm3_bar_v10.py',
                                   'm3_entries_v3.py', 'm3_record_v4.py')}
want_man.update({('out/' + f if d == OUTD else os.path.join(d, f)): h for (d, f), h in INPUTS.items()})
miss = [p for p, h in want_man.items() if MAN.get(p) != h]
ASM = os.path.join(OUTD, 'm3_run_v1_8_asm.%d.out' % NN)
with open(ASM) as fh:
    ASM_FIRST = fh.readline().rstrip('\n')
asm_ok = ASM_FIRST.startswith('m3_run_v1_8 item asm.%d ' % NN) and ('; script sha256 %s;' % OWNMOD['m3_run_v1_8.py']) in ASM_FIRST
gate('C-PINS', not miss and asm_ok, '(MANIFEST_m3_run_v1_8 lists %d of this script\'s pins with their full sha256s; the asm output\'s first line '
     'names m3_run_v1_8 %s)%s' % (len(want_man), OWNMOD['m3_run_v1_8.py'][:8], (': not listed ' + ', '.join(miss)) if miss else ''))
plant('PLANT-PINS', ('; script sha256 %s;' % flip(OWNMOD['m3_run_v1_8.py'])) not in ASM_FIRST,
      '(the asm output\'s first line against m3_run_v1_8\'s sha256 with the last digit changed)')

from fractions import Fraction
import importlib.util


def load_as(name, fname):
    """a pinned file of pk03/ loaded under the given module name (dependencies first)."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(OWN, fname))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


GENERIC = [('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_major', 'm3_major_v2.py'),
           ('m3_bar', 'm3_bar_v10.py'), ('m3_entries', 'm3_entries_v3.py')]
MODS = {name: load_as(name, fname) for name, fname in GENERIC}
S, SER, BAR, ENT = (MODS[k] for k in ('m3_scal', 'm3_series', 'm3_bar', 'm3_entries'))
RDR = load_as('m3_reader_v6', 'm3_reader_v6.py')
PINS = load_as('m3_lawcert_v1_pins', 'm3_lawcert_v1_pins.py').PINS
from mpmath import iv
import flint
S.setup()
out('PRECISION iv.prec %d (m3_scal_v2.setup, as the run)' % iv.prec)

# ------------------------------------------------------------------ C-BIND
stage('C-BIND')
RECS = {}
for f in FAMS:
    RECS[f] = RDR.load(os.path.join(OUTD, 'm3_s8v3_%s_N%d_J300_v1_8.json' % (f, NN)), ASM, J_REF, NN)
SIDE = os.path.join(OWN, 'MANIFEST_m3_run_v1_8_asm.%d.sha256' % NN)
side = {}
with open(SIDE) as fh:
    for ln in fh:
        h_, p_ = ln.rstrip('\n').split('  ', 1)
        side[p_] = h_
want_side = {'out/' + os.path.basename(ASM): sha(ASM)}
want_side.update({'out/' + RECS[f]['name']: RECS[f]['sha256'] for f in FAMS})
with open(os.path.join(W4, 'S8_ENTRY_LIST_v3.json')) as fh:
    LIST = json.load(fh)
LKEYS = {f: {e['key']: bool(e['parity_zero']) for e in LIST['entries'] if e['graph'] == f} for f in FAMS}
scope = [f for f in FAMS if set(RECS[f]['laws']) != set(LKEYS[f])
         or any((RECS[f]['laws'][k]['parity'] == 'zero') != z for k, z in LKEYS[f].items())]
nfree = sum(1 for f in FAMS for d in RECS[f]['laws'].values() if d['parity'] == 'free')
gate('C-BIND', side == want_side and not scope, '(five records through m3_reader_v6.load against %s; %s names exactly the asm output and '
     'the five records with their sha256s; entries = the list\'s keys and parity per graph: %s; %d free, %d parity zeros)%s' % (
         os.path.basename(ASM), os.path.basename(SIDE), ', '.join('%s %d' % (f, len(RECS[f]['laws'])) for f in FAMS), nfree,
         sum(len(RECS[f]['laws']) for f in FAMS) - nfree, (': scope differs for ' + ', '.join(scope)) if scope else ''))
if FAILS:
    finish()
    sys.exit(1)


# ------------------------------------------------------------------ C-LAW-REM and C-LAW-SHAPE: the AST checks
class Refuse(Exception):
    pass


def find_node(tree, path):
    """the FunctionDef or ClassDef at path ('name' or 'Class.name') of a parsed module, defined exactly once."""
    body, node = tree.body, None
    for p in path.split('.'):
        hits = [n for n in body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == p]
        if len(hits) != 1:
            raise Refuse('%s: %d definitions of %s' % (path, len(hits), p))
        node = hits[0]
        body = node.body
    return node


def stmts_in(node):
    """every statement under node, nested blocks included, nested function and class bodies excluded."""
    acc = []

    def visit(stmts):
        for st in stmts:
            acc.append(st)
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            for fld in ('body', 'orelse', 'finalbody'):
                sub = getattr(st, fld, None)
                if isinstance(sub, list):
                    visit([s for s in sub if isinstance(s, ast.stmt)])
            for h in getattr(st, 'handlers', None) or []:
                visit(h.body)
    visit(node.body)
    return acc


def bindings(fn):
    """name -> [(value or None, top)] for every binding of a plain name in fn's own scope; top: a direct statement of fn's body."""
    acc = {}
    tops = set(id(s) for s in fn.body)

    def add(nm, val, top):
        acc.setdefault(nm, []).append((val, top))

    def bind(tg, val, top):
        if isinstance(tg, ast.Name):
            add(tg.id, val, top)
        elif isinstance(tg, (ast.Tuple, ast.List)):
            if isinstance(val, (ast.Tuple, ast.List)) and len(val.elts) == len(tg.elts):
                for a, b in zip(tg.elts, val.elts):
                    bind(a, b, top)
            else:
                for nd in ast.walk(tg):
                    if isinstance(nd, ast.Name):
                        add(nd.id, None, top)
        elif isinstance(tg, ast.Starred):
            bind(tg.value, None, top)
    for st in stmts_in(fn):
        top = id(st) in tops
        if isinstance(st, ast.Assign):
            for tg in st.targets:
                bind(tg, st.value, top)
        elif isinstance(st, (ast.AugAssign, ast.AnnAssign)):
            bind(st.target, None, top)
        elif isinstance(st, (ast.For, ast.AsyncFor)):
            bind(st.target, None, False)
        elif isinstance(st, (ast.With, ast.AsyncWith)):
            for it in st.items:
                if it.optional_vars is not None:
                    bind(it.optional_vars, None, False)
        elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            add(st.name, st, top)
        elif isinstance(st, (ast.Import, ast.ImportFrom)):
            for a in st.names:
                add((a.asname or a.name).split('.')[0], None, top)
        elif isinstance(st, ast.Try):
            for h in st.handlers:
                if h.name:
                    add(h.name, None, False)
    for nd in ast.walk(fn):
        if isinstance(nd, ast.NamedExpr):
            add(nd.target.id, None, False)
    return acc


def pin_stmts(key):
    return ast.parse(textwrap.dedent(PINS[key])).body


def is_attr(e, base, attr):
    return isinstance(e, ast.Attribute) and isinstance(e.value, ast.Name) and e.value.id == base and e.attr == attr


def mentions_t(nodes):
    """an allow-listed definition may not mention t, T or J (plain or as self.t / self.J)."""
    for st in nodes:
        for nd in ast.walk(st):
            if isinstance(nd, ast.Name) and nd.id in ('t', 'T', 'J'):
                return nd.id
            if isinstance(nd, ast.Attribute) and isinstance(nd.value, ast.Name) and nd.value.id == 'self' and nd.attr in ('t', 'J'):
                return 'self.' + nd.attr
    return None


def self_assigns(tree, attr):
    """the methods of class Prep that assign self.<attr>, one entry per assignment, anywhere in the module."""
    acc = []
    for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
        for fn in [n for n in cls.body if isinstance(n, ast.FunctionDef)]:
            for nd in ast.walk(fn):
                tgs = nd.targets if isinstance(nd, ast.Assign) else ([nd.target] if isinstance(nd, (ast.AugAssign, ast.AnnAssign)) else [])
                for tg in tgs:
                    for x in ast.walk(tg):
                        if is_attr(x, 'self', attr) and isinstance(x.ctx, ast.Store):
                            acc.append('%s.%s' % (cls.name, fn.name))
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        for nd in ast.walk(fn):
            if isinstance(nd, ast.Assign):
                for tg in nd.targets:
                    for x in ast.walk(tg):
                        if is_attr(x, 'self', attr) and isinstance(x.ctx, ast.Store):
                            acc.append(fn.name)
    return acc


class TVal:
    """t-valuation of the expressions of one Prep method. An accepted expression is a polynomial in t with
    nonnegative coefficients fixed at J_REF, and v(e) is a lower bound of its t-adic valuation:
      a + b -> min; a * b -> sum; a / (positive literal) -> v(a); T(k) and S.ipow(t, k) -> k; S.ipow(x, k), k a literal -> k v(x);
      t -> 1; the form iv.mpf([iv.mpf(0), X.b if X.b < Y.b else Y.b]) -> min(v(X), v(Y)); S.isum over a comprehension -> the minimum over
      its enumerated indices (arithmetic filters evaluated, the fixed filter 'not is_zero(Fi[...])' kept as a superset); S.isum over the
      values of a dict built by one literal and single-key stores -> the minimum over them; an index-only branch -> its branch;
      allow-listed atoms, atom calls, self.norm_any calls, subscripts of atom lists, iv.mpf of a positive literal,
      S.ipow(atom, data-dependent power) and abs(S.I(scal)) -> 0.
    Anything else refuses: subtraction, negation, an unknown name or call, division by anything but a positive literal, a name with
    more than one binding or bound under a branch."""

    def __init__(self, tree, path, atoms, attr_atoms, attrs):
        self.tree, self.path = tree, path
        self.fn = find_node(tree, path)
        self.b = bindings(self.fn)
        self.stm = set(ast.dump(s) for s in stmts_in(self.fn))
        self.atoms, self.attr_atoms, self.attrs = atoms, attr_atoms, attrs
        self.memo, self.okatoms = {}, set()

    def fail(self, why):
        raise Refuse('%s: %s' % (self.path, why))

    def one(self, name):
        bs = self.b.get(name, [])
        if len(bs) != 1 or not bs[0][1] or bs[0][0] is None:
            self.fail('%s must have exactly one binding, a direct statement with a value (bindings %d)' % (name, len(bs)))
        return bs[0][0]

    def atom(self, name):
        """an allow-listed atom: each pinned statement is a statement of this function, the atom has exactly as many bindings here as
        in its pinned statements, and no pinned statement mentions t, T or J."""
        if name in self.okatoms:
            return 0
        nodes = [s for key in self.atoms[name] for s in pin_stmts(key)]
        bad = mentions_t(nodes)
        if bad:
            self.fail('allow-listed %s mentions %s' % (name, bad))
        if any(ast.dump(s) not in self.stm for s in nodes):
            self.fail('a pinned definition of %s is not a statement of this function' % name)
        fake = ast.parse('def _pinned():\n    pass\n').body[0]
        fake.body = nodes
        if len(bindings(fake).get(name, [])) != len(self.b.get(name, [])):
            self.fail('%s has bindings outside its pinned definition' % name)
        self.okatoms.add(name)
        return 0

    def attr_atom(self, attr):
        key, where = self.attr_atoms[attr]
        nodes = pin_stmts(key)
        bad = mentions_t(nodes)
        if bad:
            self.fail('allow-listed self.%s mentions %s' % (attr, bad))
        fnw = find_node(self.tree, where)
        if any(ast.dump(s) not in set(ast.dump(x) for x in stmts_in(fnw)) for s in nodes):
            self.fail('the pinned definition of self.%s is not a statement of %s' % (attr, where))
        if self_assigns(self.tree, attr) != [where]:
            self.fail('self.%s is assigned in %s, expected once in %s' % (attr, self_assigns(self.tree, attr), where))
        return 0

    def is_tref(self, x):
        if is_attr(x, 'self', 't'):
            return True
        if isinstance(x, ast.Name) and x.id == 't':
            return is_attr(self.one('t'), 'self', 't')
        return False

    def check_T(self):
        lam = self.one('T')
        ok = (isinstance(lam, ast.Lambda) and len(lam.args.args) == 1 and not lam.args.vararg and not lam.args.kwarg and not lam.args.defaults
              and isinstance(lam.body, ast.Call) and is_attr(lam.body.func, 'S', 'ipow') and len(lam.body.args) == 2 and not lam.body.keywords
              and self.is_tref(lam.body.args[0]) and isinstance(lam.body.args[1], ast.Name) and lam.body.args[1].id == lam.args.args[0].arg)
        if not ok:
            self.fail('T is not lambda k: S.ipow(t, k) with t = self.t')

    def ival(self, e, env):
        """an exact int: literals, comprehension indices and +, -, * of them."""
        if isinstance(e, ast.Constant) and type(e.value) is int:
            return e.value
        if isinstance(e, ast.Name) and e.id in env:
            return env[e.id]
        if isinstance(e, ast.BinOp) and isinstance(e.op, (ast.Add, ast.Sub, ast.Mult)):
            a, b = self.ival(e.left, env), self.ival(e.right, env)
            return a + b if isinstance(e.op, ast.Add) else (a - b if isinstance(e.op, ast.Sub) else a * b)
        self.fail('not an exact int: %s' % ast.dump(e)[:80])

    def itest(self, e, env):
        if isinstance(e, ast.Compare) and len(e.ops) == 1:
            a, b = self.ival(e.left, env), self.ival(e.comparators[0], env)
            op = type(e.ops[0])
            table = {ast.GtE: a >= b, ast.Gt: a > b, ast.LtE: a <= b, ast.Lt: a < b, ast.Eq: a == b, ast.NotEq: a != b}
            if op in table:
                return table[op]
        self.fail('not an index test: %s' % ast.dump(e)[:80])

    @staticmethod
    def fixed_filter(e):
        """'not is_zero(Fi[...])': a filter fixed at J_REF; keeping every index is a superset, so the minimum stays a lower bound."""
        return (isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.Not) and isinstance(e.operand, ast.Call)
                and isinstance(e.operand.func, ast.Name) and e.operand.func.id == 'is_zero' and len(e.operand.args) == 1
                and isinstance(e.operand.args[0], ast.Subscript) and isinstance(e.operand.args[0].value, ast.Name)
                and e.operand.args[0].value.id == 'Fi')

    def enum(self, gens, env):
        envs = [dict(env)]
        for g in gens:
            if not isinstance(g.target, ast.Name) or g.is_async:
                self.fail('comprehension target')
            nxt = []
            for en in envs:
                it = g.iter
                if isinstance(it, ast.Call) and isinstance(it.func, ast.Name) and it.func.id == 'range' and 1 <= len(it.args) <= 2 and not it.keywords:
                    lo, hi = (0, self.ival(it.args[0], en)) if len(it.args) == 1 else (self.ival(it.args[0], en), self.ival(it.args[1], en))
                    vals = list(range(lo, hi))
                elif isinstance(it, (ast.Tuple, ast.List)):
                    vals = [self.ival(x, en) for x in it.elts]
                else:
                    self.fail('comprehension over %s' % ast.dump(it)[:80])
                for v_ in vals:
                    e2 = dict(en)
                    e2[g.target.id] = v_
                    if all(self.fixed_filter(c) or self.itest(c, e2) for c in g.ifs):
                        nxt.append(e2)
            envs = nxt
        return envs

    def dict_values(self, name):
        lit = self.one(name)
        if not isinstance(lit, ast.Dict) or any(k is None or not isinstance(k, ast.Constant) or not isinstance(k.value, str) for k in lit.keys):
            self.fail('%s is not one dict literal with string keys' % name)
        keys = [k.value for k in lit.keys]
        vals = list(lit.values)
        for nd in ast.walk(self.fn):
            if isinstance(nd, ast.Subscript) and isinstance(nd.value, ast.Name) and nd.value.id == name and not isinstance(nd.ctx, ast.Load):
                self.fail('%s[...] is stored or deleted outside a single-key assignment' % name) if not isinstance(nd.ctx, ast.Store) else None
            if isinstance(nd, ast.Attribute) and isinstance(nd.value, ast.Name) and nd.value.id == name and nd.attr != 'values':
                self.fail('%s.%s may change the dict' % (name, nd.attr))
            if isinstance(nd, ast.AugAssign) and isinstance(nd.target, ast.Subscript) and isinstance(nd.target.value, ast.Name) and nd.target.value.id == name:
                self.fail('%s[...] is updated in place' % name)
        for st in stmts_in(self.fn):
            if isinstance(st, ast.Assign) and any(isinstance(tg, ast.Subscript) and isinstance(tg.value, ast.Name) and tg.value.id == name for tg in st.targets):
                tg = st.targets[0]
                if len(st.targets) != 1 or id(st) not in set(id(s) for s in self.fn.body) or not isinstance(tg.slice, ast.Constant) or not isinstance(tg.slice.value, str):
                    self.fail('%s[...] must be stored by direct single-key statements' % name)
                keys.append(tg.slice.value)
                vals.append(st.value)
        if len(set(keys)) != len(keys):
            self.fail('%s has a key stored twice' % name)
        return vals

    @staticmethod
    def zero_min(e):
        """iv.mpf([iv.mpf(0), X.b if X.b < Y.b else Y.b]) -> (X, Y), else None."""
        if not (isinstance(e, ast.Call) and is_attr(e.func, 'iv', 'mpf') and len(e.args) == 1 and not e.keywords
                and isinstance(e.args[0], ast.List) and len(e.args[0].elts) == 2):
            return None
        z, m = e.args[0].elts
        if not (isinstance(z, ast.Call) and is_attr(z.func, 'iv', 'mpf') and len(z.args) == 1 and isinstance(z.args[0], ast.Constant)
                and z.args[0].value == 0 and isinstance(m, ast.IfExp) and isinstance(m.test, ast.Compare) and len(m.test.ops) == 1
                and isinstance(m.test.ops[0], ast.Lt)):
            return None
        a, b, x, y = m.test.left, m.test.comparators[0], m.body, m.orelse
        if all(isinstance(q, ast.Attribute) and q.attr == 'b' for q in (a, b, x, y)) and ast.dump(a) == ast.dump(x) and ast.dump(b) == ast.dump(y):
            return a.value, b.value
        return None

    def v(self, e, env):
        if isinstance(e, ast.Constant) and type(e.value) in (int, float) and e.value > 0:
            return 0
        if isinstance(e, ast.Name):
            n = e.id
            if n in env:
                self.fail('the index %s used as a value' % n)
            if n in self.atoms:
                return self.atom(n)
            if n == 't':
                if not self.is_tref(e):
                    self.fail('t is not self.t')
                return 1
            if n not in self.memo:
                self.memo[n] = None
                self.memo[n] = self.v(self.one(n), {})
            if self.memo[n] is None:
                self.fail('%s is defined through itself' % n)
            return self.memo[n]
        if is_attr(e, 'self', 't'):
            return 1
        if isinstance(e, ast.Attribute) and isinstance(e.value, ast.Name) and e.value.id == 'self' and e.attr in self.attrs:
            return self.attrs[e.attr]()
        if isinstance(e, ast.BinOp):
            if isinstance(e.op, ast.Add):
                return min(self.v(e.left, env), self.v(e.right, env))
            if isinstance(e.op, ast.Mult):
                return self.v(e.left, env) + self.v(e.right, env)
            if isinstance(e.op, ast.Div) and isinstance(e.right, ast.Constant) and type(e.right.value) in (int, float) and e.right.value > 0:
                return self.v(e.left, env)
            self.fail('operator %s refused' % type(e.op).__name__)
        if isinstance(e, ast.IfExp):
            return self.v(e.body if self.itest(e.test, env) else e.orelse, env)
        if isinstance(e, ast.Subscript):
            base = e.value
            if isinstance(base, ast.Name) and base.id in self.atoms:
                self.ival(e.slice, env)
                return self.atom(base.id)
            if isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name) and base.value.id == 'self' and base.attr in self.attr_atoms:
                self.ival(e.slice, env)
                return self.attr_atom(base.attr)
            self.fail('subscript of %s refused' % ast.dump(base)[:60])
        if isinstance(e, ast.Call):
            f = e.func
            zm = self.zero_min(e)
            if zm is not None:
                return min(self.v(zm[0], env), self.v(zm[1], env))
            if e.keywords:
                self.fail('call with keywords refused')
            if isinstance(f, ast.Name) and f.id == 'T' and len(e.args) == 1:
                self.check_T()
                k = self.ival(e.args[0], env)
                if k < 0:
                    self.fail('negative t power')
                return k
            if is_attr(f, 'S', 'ipow') and len(e.args) == 2:
                x, k = e.args
                if self.is_tref(x):
                    kk = self.ival(k, env)
                    if kk < 0:
                        self.fail('negative t power')
                    return kk
                if isinstance(k, ast.Constant) and type(k.value) is int and k.value >= 0:
                    return k.value * self.v(x, env)
                if isinstance(x, ast.Name) and x.id in self.atoms:
                    return self.atom(x.id)
                self.fail('S.ipow form refused')
            if is_attr(f, 'S', 'isum') and len(e.args) == 1:
                a = e.args[0]
                if isinstance(a, ast.GeneratorExp):
                    vals = [self.v(a.elt, en) for en in self.enum(a.generators, env)]
                    if not vals:
                        self.fail('empty sum')
                    return min(vals)
                if (isinstance(a, ast.Call) and not a.args and isinstance(a.func, ast.Attribute) and a.func.attr == 'values'
                        and isinstance(a.func.value, ast.Name)):
                    return min(self.v(x, {}) for x in self.dict_values(a.func.value.id))
                self.fail('S.isum form refused')
            if isinstance(f, ast.Name) and f.id in self.atoms:
                return self.atom(f.id)
            if is_attr(f, 'self', 'norm_any'):
                return 0
            if is_attr(f, 'iv', 'mpf') and len(e.args) == 1 and isinstance(e.args[0], ast.Constant) and type(e.args[0].value) is int and e.args[0].value > 0:
                return 0
            if (isinstance(f, ast.Name) and f.id == 'abs' and len(e.args) == 1 and isinstance(e.args[0], ast.Call)
                    and is_attr(e.args[0].func, 'S', 'I') and len(e.args[0].args) == 1 and isinstance(e.args[0].args[0], ast.Name)
                    and e.args[0].args[0].id == 'scal'):
                return 0
            self.fail('call %s refused' % ast.dump(f)[:80])
        self.fail('%s refused' % type(e).__name__)


def terms(e):
    """the operands of a chain of + (left-nested)."""
    if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add):
        return terms(e.left) + terms(e.right)
    return [e]


BOUND_ATOMS = {'nF0': ['bar:Prep.bound:nF0'], 'nF0c': ['bar:Prep.bound:nF0c'], 'nF': ['bar:Prep.bound:nF'], 'nFc': ['bar:Prep.bound:nFc'],
               'three': ['bar:Prep.bound:three'], 'EF4': ['bar:Prep.bound:EF4'], 'Nc': ['bar:Prep.bound:Nc'], 'fnorm': ['bar:Prep.bound:fnorm'],
               'gn': ['bar:Prep.bound:gn'], 'hc': ['bar:Prep.bound:hc']}
U_ATOMS = {'N2': ['bar:Prep.stage_u:N2']}
C_ATOMS = {'nh2_6': ['bar:Prep.stage_c:nh2_6']}
ATTR_ATOMS = {'nE': ('bar:Prep.stage_u:nE', 'Prep.stage_u'), 'nE4': ('bar:Prep.stage_u:nE4', 'Prep.stage_u')}


def stage_attr(tv, tree, where, attr):
    """the valuation of the stage result self.<attr>: its one assignment, in the method where."""
    if self_assigns(tree, attr) != [where]:
        raise Refuse('self.%s is assigned in %s, expected once in %s' % (attr, self_assigns(tree, attr), where))
    hits = [st for st in tv.fn.body if isinstance(st, ast.Assign) and len(st.targets) == 1 and is_attr(st.targets[0], 'self', attr)]
    if len(hits) != 1:
        raise Refuse('self.%s is not assigned by one direct statement of %s' % (attr, where))
    return tv.v(hits[0].value, {})


def law_rem(src, bound_atoms=None):
    """C-LAW-REM on a bar source text: the valuations of B_rem's terms (Refuse on any refusal)."""
    tree = ast.parse(src)
    tu = TVal(tree, 'Prep.stage_u', U_ATOMS, {}, {})
    tc = TVal(tree, 'Prep.stage_c', C_ATOMS, {}, {})
    attrs = {'rE': lambda: stage_attr(tu, tree, 'Prep.stage_u', 'rE'), 'nC8': lambda: stage_attr(tc, tree, 'Prep.stage_c', 'nC8'),
             'nC6': lambda: stage_attr(tc, tree, 'Prep.stage_c', 'nC6')}
    tb = TVal(tree, 'Prep.bound', bound_atoms or BOUND_ATOMS, ATTR_ATOMS, attrs)
    if self_assigns(tree, 't') != ['Prep.__init__']:
        raise Refuse('self.t is assigned in %s, expected once in Prep.__init__' % self_assigns(tree, 't'))
    vs = [tb.v(x, {}) for x in terms(tb.one('B_rem'))]
    l2 = tb.v(tb.one('l2'), {})
    return vs, l2


stage('C-LAW-REM')
with open(os.path.join(OWN, 'm3_bar_v10.py')) as fh:
    BARSRC = fh.read()
try:
    VS, L2V = law_rem(BARSRC)
    rem_ok, rem_why = len(VS) == 4 and min(VS) >= 4 and L2V >= 0, 'term valuations %s, l2 valuation %d' % (VS, L2V)
except Refuse as ex:
    rem_ok, rem_why = False, 'refused: %s' % ex
gate('C-LAW-REM', rem_ok, '(m3_bar_v10 Prep.bound: B_rem = overflow + nFle3 rE + rho4 + t^4 Nc EF4/24, each term a polynomial in t with '
     'nonnegative coefficients fixed at J_REF and valuation >= 4; l2 a polynomial of valuation >= 0; %s)' % rem_why)
REM_PLANTS = [
    ('T(4) -> T(3) in the EF4 term', 'B_rem = overflow + nFle3 * self.rE + rho4 + T(4) / 24 * Nc * EF4',
     'B_rem = overflow + nFle3 * self.rE + rho4 + T(3) / 24 * Nc * EF4'),
    ('the overflow filter >= 3', 'for i in range(4) for j in range(4) if i + j >= 4)', 'for i in range(4) for j in range(4) if i + j >= 3)'),
    ('nC8 without its factor t', 'self.nC8 = t * (self.norm_any(H1', 'self.nC8 = (self.norm_any(H1'),
    ("rE's 't4|H4|' part with T(3)", "'t4|H4|': T(4) * N2(H4", "'t4|H4|': T(3) * N2(H4"),
    ("a '- nF0' term in B_rem", 'B_rem = overflow + nFle3', 'B_rem = overflow - nF0 + nFle3'),
    ('an unknown name in rho4', 'rho4 = Nc / 24 * iv.mpf(', 'rho4 = Nc / 24 * zeta * iv.mpf('),
    ('a second binding of overflow (condition 2)', '        overflow = S.isum(', '        overflow = nF0\n        overflow = S.isum('),
]
for lab, old, new in REM_PLANTS:
    if BARSRC.count(old) != 1:
        plant('PLANT-LAW-REM', False, '(%s: the text to change occurs %d times, expected once)' % (lab, BARSRC.count(old)))
        continue
    try:
        vs_, l2_ = law_rem(BARSRC.replace(old, new))
        fired, why = not (len(vs_) == 4 and min(vs_) >= 4 and l2_ >= 0), 'valuations %s' % vs_
    except Refuse as ex:
        fired, why = True, 'refused: %s' % str(ex)[:120]
    plant('PLANT-LAW-REM', fired, '(%s: %s)' % (lab, why))
try:
    law_rem(BARSRC, dict(BOUND_ATOMS, nFle3=['bar:Prep.bound:nF0']))
    fired, why = False, 'accepted'
except Refuse as ex:
    fired, why = True, 'refused: %s' % str(ex)[:120]
plant('PLANT-LAW-REM', fired, '(nFle3 allow-listed with a pinned text that is not its definition: %s)' % why)
PINS['plant:nFle3'] = '        nFle3 = S.isum(T(i) * nF[i] for i in range(4))\n'
try:
    law_rem(BARSRC, dict(BOUND_ATOMS, nFle3=['plant:nFle3']))
    fired, why = False, 'accepted'
except Refuse as ex:
    fired, why = True, 'refused: %s' % str(ex)[:120]
plant('PLANT-LAW-REM', fired, '(a t-dependent name allow-listed with its own definition: %s)' % why)
del PINS['plant:nFle3']

stage('C-LAW-SHAPE')
SRC = {'bar': BARSRC}
for k_, f_ in (('scal', 'm3_scal_v2.py'), ('run', 'm3_run_v1_8.py'), ('rec', 'm3_record_v4.py')):
    with open(os.path.join(OWN, f_)) as fh:
        SRC[k_] = fh.read()
SHAPES = [('bar:sup_F', 'bar', 'sup_F', 'fn'), ('bar:Prep.norm_any', 'bar', 'Prep.norm_any', 'fn'),
          ('scal:chi_tail_up', 'scal', 'chi_tail_up', 'fn'), ('scal:ive1', 'scal', 'ive1', 'fn'), ('scal:logtree', 'scal', 'logtree', 'fn'),
          ('scal:logmain', 'scal', 'logmain', 'fn'), ('scal:far_base', 'scal', 'far_base', 'fn'), ('run:laws_of', 'run', 'laws_of', 'fn'),
          ('rec:entry_record', 'rec', 'entry_record', 'fn'), ('bar:Prep.UK', 'bar', 'Prep', 'cls'), ('bar:Prep.CK', 'bar', 'Prep', 'cls'),
          ('run:compute_entry:laws', 'run', 'compute_entry', 'st')]
SHAPES += [(k, 'bar', 'Prep.__init__', 'st') for k in ('bar:Prep.__init__:t', 'bar:Prep.__init__:ratesp', 'bar:Prep.__init__:tilt_c',
                                                        'bar:Prep.__init__:tilt_p', 'bar:Prep.__init__:restore')]
SHAPES += [(k, 'bar', 'Prep.stage_c', 'st') for k in ('bar:Prep.stage_c:n_', 'bar:Prep.stage_c:Pout', 'bar:Prep.stage_c:Pout_p',
                                                       'bar:Prep.stage_c:farbase', 'bar:Prep.stage_c:alpha_lo')]
SHAPES += [(k, 'bar', 'Prep.bound', 'st') for k in ('bar:Prep.bound:l2', 'bar:Prep.bound:B_tail', 'bar:Prep.bound:nF0p', 'bar:Prep.bound:B_ann',
                                                     'bar:Prep.bound:supF', 'bar:Prep.bound:B_far', 'bar:Prep.bound:return')]


def shape_misses(srcs):
    """the pins of SHAPES that are not, as ASTs, in their named places of the given source texts."""
    trees = {k: ast.parse(v) for k, v in srcs.items()}
    miss_ = []
    for key, fk, place, kind in SHAPES:
        try:
            node = find_node(trees[fk], place)
        except Refuse:
            miss_.append(key)
            continue
        pins_ = pin_stmts(key)
        if kind == 'fn':
            ok_ = len(pins_) == 1 and ast.dump(pins_[0]) == ast.dump(node)
        else:
            have = set(ast.dump(s) for s in (node.body if kind == 'cls' else stmts_in(node)))
            ok_ = all(ast.dump(s) in have for s in pins_)
        if not ok_:
            miss_.append(key)
    return miss_


sm = shape_misses(SRC)
gate('C-LAW-SHAPE', not sm, '(%d pinned texts of m3_lawcert_v1_pins, as ASTs, in their places: the tail, ann and far statements, sup_F, '
     'norm_any, chi_tail_up, ive1, logtree, logmain, far_base, the bound\'s return, Prep.UK/CK, __init__\'s t, rates, tilts and restore, '
     'laws_of, compute_entry\'s law lines, entry_record)%s' % (len(SHAPES), (': missing ' + ', '.join(sm)) if sm else ''))
for lab, fk, old, new in (('B_tail without sqrt_nn', 'bar', 'B_tail = l2 * S.sqrt_nn(self.Pout)', 'B_tail = l2 * self.Pout'),
                          ('alpha_lo taking .b', 'bar', '/ (2 * gv)).a for gv in g.Gvv)', '/ (2 * gv)).b for gv in g.Gvv)'),
                          ("sup_F's m_F without '- i'", 'bar', 'mx = max(mx, len(mono) - i)', 'mx = max(mx, len(mono))')):
    if SRC[fk].count(old) != 1:
        plant('PLANT-LAW-SHAPE', False, '(%s: the text to change occurs %d times, expected once)' % (lab, SRC[fk].count(old)))
        continue
    plant('PLANT-LAW-SHAPE', bool(shape_misses(dict(SRC, **{fk: SRC[fk].replace(old, new)}))), '(%s must be missed)' % lab)

# ------------------------------------------------------------------ C-LAWFIELDS and C-MONO-FAR: the independent recompute
stage('C-LAWFIELDS')
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]
TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)


def prepjson(f):
    with open(os.path.join(OUTD, REFOUT[f][0])) as fh:
        hits = [json.loads(ln[len('PREPJSON '):]) for ln in fh if ln.startswith('PREPJSON ')]
    if len(hits) != 1:
        raise ValueError('%s: %d PREPJSON lines' % (REFOUT[f][0], len(hits)))
    return hits[0]


def own_mF(facs):
    """this script's own J-exponent of sup_F: per factor the largest exponent over its terms, the constant term counting 0 ('p' and a
    nonzero xi constant) and a coefficient of degree d at t^i counting d - i, negative values allowed."""
    m = 0
    for f in facs:
        if f[0] == 'const':
            continue
        if f[0] == 'p':
            ex = [0] + [len(mono) - i for i, coef in ((1, f[2]), (2, f[3]), (3, f[4])) for cb, mono in zip(coef, SER.BASIS9) if cb != 0.0]
        elif f[0] == 'xi':
            ex = ([0] if f[2] != 0.0 else []) + [len(mono) for cb, mono in zip(f[3], SER.BASIS9) if cb != 0.0]
            ex = ex or [0]
        else:
            raise ValueError('factor kind %r' % (f[0],))
        m += max(ex)
    return m


T300 = 1 / S.I(J_REF)
fld_bad, rates, nchk = [], [], 0
for f in FAMS:
    gm = GMAP[f]
    ents = [e for e in LIST['entries'] if e['graph'] == f]
    fls = [[ENT.factor(TS, gm, enc) for enc in e['factors']] for e in ents]
    g = ENT.build_graph(gm, NN, fls)
    rp = prepjson(f)
    if rp['family'] != 'V3' + f or rp['N'] != NN or rp['J'] != J_REF:
        fld_bad.append('%s: PREPJSON family %r N %r J %r' % (f, rp['family'], rp['N'], rp['J']))
        continue
    ratesp = [S.up(-iv.log(1 - S.I(rp['ap'])) / (2 * S.I(rp['ap'])) * T300)] * g.V
    tp = g.tilted(ratesp)
    if tp is None:
        fld_bad.append('%s: tilt_p not certainly positive definite' % f)
        continue
    tail = [(Fraction(a), Fraction(S.up(gv))) for a, gv in zip(rp['a_v'], g.Gvv)]
    ann = [(Fraction(a), Fraction(S.up(gv))) for a, gv in zip(rp['a_v'], tp['Gvv'])]
    alpha_lo = min((S.I(rp['theta0']) * S.I(rp['ap']) / (2 * gv)).a for gv in g.Gvv)
    for e, facs in zip(ents, fls):
        if e['parity_zero']:
            continue
        nchk += 1
        _, mF = BAR.sup_F(facs, J_REF)
        mo = own_mF(facs)
        cF = mF + Fraction(g.n * (g.V - 1), 2)
        rate = alpha_lo - S.I(cF) / J_REF
        rates.append((S.down(rate), rate.a > 0, '%s:%s' % (f, e['key'])))
        want = {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': J_REF, 'a_G': tail}, 'ann': {'n': g.n, 'J_REF': J_REF, 'a_G': ann},
                'far_rate': Fraction(S.down(rate)), 'far_cF': cF}
        if RECS[f]['laws'][e['key']]['laws'] != want or not mo <= mF:
            fld_bad.append('%s:%s%s' % (f, e['key'], '' if mo <= mF else ' (own m_F %d > %d)' % (mo, mF)))
gate('C-LAWFIELDS', not fld_bad and nchk == nfree, '(%d free entries: rem_tpow 4; tail and ann n, J_REF and a_G from the graphs\' G_vv, tilt_p\'s G_vv '
     'and m3ref_v1_10\'s a_v; far_cF from the pinned sup_F\'s m_F, never below this script\'s own exponent; far_rate = down(alpha_lo - '
     'c_F/300); all exactly equal)%s' % (nchk, (': differ ' + ', '.join(fld_bad[:12])) if fld_bad else ''))
rmin = min(rates) if rates else (0.0, False, '-')
gate('C-MONO-FAR', bool(rates) and all(r[1] for r in rates), '(every recomputed far rate certainly > 0; smallest %.4e at %s)' % (rmin[0], rmin[2]))

# ------------------------------------------------------------------ C-BAND: the banded bound against the uniform err, in arb
stage('C-BAND')
flint.ctx.prec = 128
A = flint.arb


def fa(x):
    x = Fraction(x)
    return A(x.numerator) / A(x.denominator)


def ptail(n, s):
    if n == 2:
        return (-s / 2).exp()
    if n == 3:
        return (s / 2).sqrt().erfc() + (2 * s / A.pi()).sqrt() * (-s / 2).exp()
    raise ValueError('n %r' % n)


def psum(J, part):
    return sum((ptail(part['n'], A(J) * fa(a) / fa(G)) for a, G in part['a_G']), A(0))


def banded(d, J):
    L, P = d['laws'], d['parts']
    q = A(J_REF) / A(J)
    t = A(1) / A(J)
    out_ = fa(P['rem']) * q * q * q * q
    out_ += fa(P['tail']) * (psum(J, L['tail']) / psum(J_REF, L['tail'])).sqrt()
    out_ += fa(P['ann']) * (psum(J, L['ann']) / psum(J_REF, L['ann'])).sqrt()
    out_ += fa(P['far']) * (-fa(L['far_rate']) * (J - J_REF)).exp()
    tk = A(1)
    for r in d['ak_rad']:
        out_ += fa(r) * tk
        tk = tk * t
    return out_.upper()


JS = (300, 600, 1000, 3000)
band_bad, worst = [], {J: 0.0 for J in JS}
for f in FAMS:
    for k, d in RECS[f]['laws'].items():
        if d['parity'] != 'free':
            continue
        bs = [banded(d, J) for J in JS]
        err = fa(d['err'])
        okb = bool(bs[0] <= err * (1 + A(1) / A(2 ** 30))) and all(bool(b <= err) for b in bs[1:]) and all(bool(bs[i + 1] <= bs[i]) for i in range(len(bs) - 1))
        if not okb:
            band_bad.append('%s:%s' % (f, k))
        for J, b in zip(JS, bs):
            worst[J] = max(worst[J], float(b / err))
gate('C-BAND', not band_bad, '(sanity, %d free entries: the banded bound in arb at J = %s is <= err (1 + 2^-30) at 300, <= err beyond and '
     'non-increasing; largest banded/err: %s)%s' % (nfree, ', '.join(map(str, JS)), ', '.join('J %d %.4f' % (J, worst[J]) for J in JS),
                                                   (': ' + ', '.join(band_bad[:12])) if band_bad else ''))
for f in FAMS:
    fr_ = [d for d in RECS[f]['laws'].values() if d['parity'] == 'free']
    if fr_:
        out('BAND-INFO %s: %d free entries; largest banded/err at J = 600 %.4f, at J = 1000 %.4f' % (
            f, len(fr_), max(float(banded(d, 600) / fa(d['err'])) for d in fr_), max(float(banded(d, 1000) / fa(d['err'])) for d in fr_)))

# ------------------------------------------------------------------ the certificate, C-LAWCERT-RT and its plants
stage('C-LAWCERT-RT')
NAME = 'm3_lawcert_v1_N%d.json' % NN


def exact_laws(L):
    return {'rem_tpow': 4, 'tail': {'n': L['tail']['n'], 'J_REF': J_REF, 'a_G': [[str(a), str(G)] for a, G in L['tail']['a_G']]},
            'ann': {'n': L['ann']['n'], 'J_REF': J_REF, 'a_G': [[str(a), str(G)] for a, G in L['ann']['a_G']]},
            'far_rate': str(L['far_rate']), 'far_cF': str(L['far_cF'])}


CERT = {'format': FORMAT, 'claim': CLAIM, 'J_REF': J_REF, 'N': NN,
        'records': {f: {'file': RECS[f]['name'], 'sha256': RECS[f]['sha256']} for f in FAMS},
        'asm': {'file': os.path.basename(ASM), 'sha256': sha(ASM)}, 'entries': {}}
for f in FAMS:
    for k, d in RECS[f]['laws'].items():
        CERT['entries']['%s:%s' % (f, k)] = ({'parity': 'zero', 'law_claim': None, 'laws': None} if d['parity'] == 'zero' else
                                            {'parity': 'free', 'law_claim': CLAIM, 'laws': exact_laws(d['laws'])})


def dumps(c):
    return json.dumps(c, sort_keys=True, indent=1) + '\n'


def sim_out(text, verdict='VERDICT VALID'):
    return '%s\nRECORD %s %s\n' % (verdict, NAME, tsha(text))


TEXT = dumps(CERT)
try:
    back = RDR.loads_lawcert(TEXT, sim_out(TEXT), J_REF, NN, RECS, NAME)
    rt_ok = len(back['entries']) == len(CERT['entries']) and all(back['entries']['%s:%s' % (f, k)]['laws'] == d['laws']
                                                                for f in FAMS for k, d in RECS[f]['laws'].items())
    rt_why = '%d entries back with the records\' laws' % len(back['entries'])
except ValueError as ex:
    rt_ok, rt_why = False, 'refused: %s' % str(ex)[:200]
gate('C-LAWCERT-RT', rt_ok and CLAIM == RDR.LAWCERT_CLAIM and FORMAT == RDR.LAWCERT_FORMAT,
     '(the certificate through m3_reader_v6.loads_lawcert against the five loaded records: %s; claim and format equal the reader\'s)' % rt_why)
F0 = [eid for eid in sorted(CERT['entries']) if CERT['entries'][eid]['parity'] == 'free'][0]


def refused(mut, verdict='VERDICT VALID'):
    c2 = copy.deepcopy(CERT)
    mut(c2)
    t2 = dumps(c2)
    try:
        RDR.loads_lawcert(t2, sim_out(t2, verdict), J_REF, NN, RECS, NAME)
        return False
    except ValueError:
        return True


def setl(path, val):
    def mut(c):
        node = c['entries'][F0]['laws']
        for p in path[:-1]:
            node = node[p]
        node[path[-1]] = val
    return mut


CERT_PLANTS = [('rem_tpow 3', setl(['rem_tpow'], 3)), ('far_rate 0', setl(['far_rate'], '0')),
               ('an a_G entry 0', lambda c: c['entries'][F0]['laws']['tail']['a_G'][0].__setitem__(0, '0')),
               ('J_REF 299', lambda c: c.__setitem__('J_REF', 299)), ('n 4', setl(['tail', 'n'], 4)),
               ('a record sha changed', lambda c: c['records']['N'].__setitem__('sha256', flip(c['records']['N']['sha256']))),
               ('an entry dropped', lambda c: c['entries'].pop(F0)),
               ('an entry added', lambda c: c['entries'].__setitem__('N:ZZZ', copy.deepcopy(c['entries'][F0]))),
               ("law_claim + ' '", lambda c: c['entries'][F0].__setitem__('law_claim', CLAIM + ' ')),
               ('a records map without one loaded record', lambda c: c['records'].pop('E2')),
               ('a non-canonical exact string', setl(['far_rate'], str(Fraction(CERT['entries'][F0]['laws']['far_rate'])) + '0/10'))]
for lab, mut in CERT_PLANTS:
    plant('PLANT-LAWCERT', refused(mut), '(%s must be refused)' % lab)
plant('PLANT-LAWCERT', refused(lambda c: None, 'VERDICT VALID-PRECERT'), '(a writing job whose VERDICT line is VERDICT VALID-PRECERT must be refused)')

# ------------------------------------------------------------------ the write, after every gate and plant
if FAILS or NOFIRE:
    out('NO-WRITE %s: a gate failed or a plant did not fire' % NAME)
else:
    path = os.path.join(OUTD, NAME)
    with open(path, 'x') as fh:
        fh.write(TEXT)
    with open(path, 'rb') as fh:
        gate('C-WRITE', fh.read() == TEXT.encode(), '(%s re-read byte for byte)' % NAME)
    out('RECORD %s %s' % (NAME, tsha(TEXT)))
finish()
