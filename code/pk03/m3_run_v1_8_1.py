#!/usr/bin/env python3
"""m3_run_v1_8_1.py -- pk03 (code/pk03/). REVISION of m3_run_v1_8.py (7d72fc7f) for option 5: one item,
asmP.N, the partial assembly of the families that are done (D, E2, FF and E3) while the N family's pieces still run. What changes:
- ITEM_RE accepts asmP.4 and asmP.3 only, so this script computes no entry and writes no hand-off.
- Every hand-off it reads is m3_run_v1_8's: read_handoff binds each to m3_run_v1_8's full sha256 (V18_SHA, put in OWNMOD so C-HASH
  checks the file), and walk_pieces' piece_state accepts a capped piece only as a clean CAP-STOP of m3_run_v1_8. Entries come only
  from VALID hand-offs, as in m3_run_v1_8's asm.
- FILES = (D, E2, E3, FF): the asm does not walk the N pieces, and write_records raises on any other key set, so no N record can be
  written (C-NO-N; PLANT-NO-N: an added N record must raise before any file is opened). C-SCOPE, C-REP-B and C-REP-AK run over the
  four families against m3ref_v1_10, as before.
- The records are m3_s8v3_<D|E2|E3|FF>_N<N>_J300_v1_8_1.json (m3_record_v4, read through m3_reader_v4_4 as before); eng names
  m3_run_v1_8_1 and, as entries_by, m3_run_v1_8 with its full sha256; the extra 'partial' says the N family is not assembled.
Everything else is m3_run_v1_8's. Its docstring follows.
m3_run_v1_8: The CERTIFIED entries of S8's route without 4-column entries: pk11's S8_ENTRY_LIST_v3
(12374013; U9's g,a,b and T,a,b for all ten z9sym states and the chain-on-B entries DY, DYY, TX, e, eX, f, fX, z, wXw, wXwX), 219 per N,
at J_REF = 300, K = 3, qcap 6, on the closed M-a layer. REVISION of m3_run_v1_7.py (e55c5de1), whose safeguards are kept as written:
C-HASH, C-IMPORT, C-VALIDATED with DENY, C-SERIES, C-PREC, C-CX, C-CX2, PLANT-GUARD, C-FALLBACK-PATH, verdict-bound hand-offs, resumable
entries (m3_bar's units, C-RESUME, the stop factor, capped pieces skipped), the write after every gate and plant, RECORD lines,
PLANT-NOWRITE, the bound reader and C-PREC-END. What changes:
- Entries come from the list, read by graph: D (strip_graph(2)), N ([vac|int|vac], pairs on L, R and (3,4)), E2 ([vac|free], m3_entries'
  'mix'), E3 ([vac|int|free]) and FF ([free|free], 'free2'). A key is the list's key exactly; parity zeros (parity_zero: true) are
  computed as balls holding 0 with C-ODD and C-ODD-AK, as S7's.
- C-GRAPH-LIST: each family's graph (m3_entries_v3.build_graph: the union of its entries' pair forms) has the couplings of the list's
  column spec (m3_graph_v3.strip, as a set) and exactly the list's pairs (PLANT-GRAPH-LIST: the pairs without one must fail).
- The float references are m3ref_v1_10's (4eb5113e; z9sym): C-PREP-REF (family, N, J), C-RULE (the radii^2 equal min(80 G_vv/300, 0.6)
  on the certified G_vv mids and rho'^2 = 0.7^2, to 1e-12; PLANT-RULE), and at asm C-REP-B and C-REP-AK against their KEYJSON lines.
- Items (N = 4 or 3): D.N, E2.N, FF.N (prep and entries); E3u.N, E3c.N (E3's prep stages) and E3k1.N .. E3k9.N (resumable pieces);
  Nu.N, Nc.N and Nk1.N .. Nk19.N; asm.N. C-RESUME and PLANT-RESUME run in D.N.
- asm writes five records, m3_s8v3_<D|N|E2|E3|FF>_N<N>_J300_v1_8.json (FORMAT 'M3_RECORD_v1', m3_record_v4; read through m3_reader_v4_4,
  as the consumers' loader), each with the list's keys of its graph (C-SCOPE, PLANT-SCOPE), trial_set in full sha256 and the list's pin.
  S7's C-KR4 (pk10's J = 170 records), C-KBAR and r_main have no counterpart here and are gone.
- Modules: m3_graph_v3 (020d4b54), m3_bar_v10 (b80f4e3b; dmaxH stays 18, no graph has more than 9 vertices), m3_entries_v3 (d9791822),
  with v1_7's m3_scal_v2, m3_series_v2, m3_major_v2, m3_record_v4, m3_reader_v4_4 and m3_handoff_v3.
Arguments: ITEM LIM (5..540). Output: stdout (the run line redirects it to out/m3_run_v1_8_<ITEM>.out); hand-offs in hand/; records in out/.
Run: D=/mnt/g2/release/root/code/pk03; OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=$D/tmp
  timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B $D/m3_run_v1_8.py ITEM LIM
  > $D/out/m3_run_v1_8_ITEM.out 2> $D/out/m3_run_v1_8_ITEM.err
m3_run_v1_7's own docstring (its history back to m3_run_v1_5) stays in that file.
"""
import resource, sys, time, math, hashlib, signal, os, json, re, traceback

ITEM_RE = r'(asmP)\.(4|3)'
if len(sys.argv) != 3 or not re.fullmatch(ITEM_RE, sys.argv[1]):
    print('usage: m3_run_v1_8_1.py ITEM LIM   (ITEM = asmP.4 or asmP.3; LIM = RLIMIT_CPU soft limit in s, 5..540)')
    sys.exit(2)
ITEM = sys.argv[1]
FAM, NN = ITEM.split('.')[0], int(ITEM.split('.')[1])
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
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk03'
C2B = CODEDIR + '/pk02'
INP = CODEDIR + '/pk10/scratch'
W4 = CODEDIR + '/pk11/out'
OUTD = OWN + '/out'
HANDD = OWN + '/hand'
KERNEL = 'arbeng_ma_v1_3'
ARBK = 'arbeng_ma_stub_v1_1'
ARBB = 'arbeng_c2b_v2'   # the arb base under ARBK (pinned in KFILES)
KFILES = {
    'arbeng_ma_v1_3.py': '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be',
    'arbeng_ma_stub_v1_1.py': '794fabc7111555db2f6390a144d3f5af6deeb358d02da8b5705cf3ceaefd0af1',
    'arbeng_c2b_v2.py': '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0',
}
VALREC = [   # the CLOSE_ARBENG_MA_V1_3 (9a290b50) conditions: kt_ma_val_v1_5's four outputs and the close itself
    (C2B + '/out', 'out_kt_ma_val_v1_5_v1.out', '5ccbb6d006f5365f219eb6221b7e66b76e7e7799e977148df94f34b0c3d86216'),
    (C2B + '/out', 'out_kt_ma_val_v1_5_v2.out', 'a61d893e6424b9ea524d944e40f625c934de04a2faeaa741e3fd333e97f48817'),
    (C2B + '/out', 'out_kt_ma_val_v1_5_v3.out', 'd613fe804a030be397fefa46ed1424063f794400b7d9618e12db8af046e09d93'),
    (C2B + '/out', 'out_kt_ma_val_v1_5_v4.out', '2ad13ec3cac14ef919f5e34fa19664f70eece05c3c3f208dcfec36a93cdd4473'),
    (CODEDIR + '/rv01', 'CLOSE_ARBENG_MA_V1_3_rv01.md', 'a8a5e8d020d2d1e1127c3ee8f400496011ddbd022af83180025ac3185ba22f95'),
]
VALIDATED = {('arbeng_ma_v1_3.py', '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be', tuple(v[2] for v in VALREC))}
DENY = {('arbeng_ma_v1_1.py', '81f7fb89f863343149b1558bfc3c8ba3e09b3e6c36ec00db4c12197b11158e7f'),
        ('arbeng_ma_v1_2.py', '935f2ca77dbcb7de0670d43505044f9c12c086f69de2a30f7b8133522ffcec80')}


def tag_for(kfile, ksha, vshas, validated=None):
    """'' (certified) only for a (file, full sha256, validation sha256s) in VALIDATED and never for a denied (file, sha256)."""
    if (kfile, ksha) in DENY:
        return '_PRECERT'
    return '' if (kfile, ksha, tuple(vshas)) in (VALIDATED if validated is None else validated) else (
        '_STUB' if 'stub' in kfile else '_PRECERT')


TAG = None   # set by C-VALIDATED after the imports
OWNMOD = {
    'm3_scal_v2.py': 'd22d3ad696074d4235f0fd31b026477e87f96f5d4b5331e29ab8d399e1e8f054',
    'm3_graph_v3.py': '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    'm3_series_v2.py': '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    'm3_major_v2.py': '89dd5a2184a511d4dea39fb3c558501e9738af118be9d41f2ac4b2d4b8d7b016',
    'm3_bar_v10.py': '9a4de5dd54faff8aa3c1c047f870d198d27d12646fbff0c973ce0aff7903a0d5',
    'm3_entries_v3.py': '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    'm3_record_v4.py': '2c8a53efb5170d6c6e320bd814c824e69d2ccdd73c57cf87a9130b796109e30f',
    'm3_reader_v4_4.py': 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0',
    'm3_handoff_v3.py': 'e4f5bf0b111197d87e9659c89265c68fcfe39e564860c6e6b6eb91c9c48feb21',
}
V18_SHA = 'be0c1be3eadabf2f14f40d84f7a2482f2b75aada522b0e267146008cd700da3b'   # m3_run_v1_8.py, the producer of every hand-off asmP reads
OWNMOD['m3_run_v1_8.py'] = V18_SHA
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

FAILS, NOFIRE = [], []


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def valid_verdict():
    """the exact verdict line of a valid run of this script (certified TAG '' is required, so 'VERDICT VALID')."""
    return 'VERDICT VALID'


def finish():
    if 'S' in globals():
        out('PRECISION end: %s' % S.precision_line())
    if 'K' in globals() and 'flint' in globals():
        gate('C-PREC-END', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d at the end of the item; C-PREC checked the start)' % flint.ctx.prec)
    out('STAGE-CPU total %.2f s' % cpu())
    if FAILS or NOFIRE:
        out('VERDICT INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE]))
    elif TAG != '':
        out('VERDICT INVALID (C-VALIDATED: TAG %r; this script writes certified records only)' % (TAG,))
    else:
        out(valid_verdict())


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tsha(text):
    """the sha256 of a text as written (json.dumps texts are ASCII)."""
    return hashlib.sha256(text.encode()).hexdigest()


def flip(h):
    """h with its last hex digit changed (plants)."""
    return h[:-1] + ('0' if h[-1] != '0' else '1')


def stage(name):
    STAGE[0] = name
    out('STAGE-CPU %s start %.2f s' % (name, cpu()))


SELF_SHA = sha(os.path.abspath(__file__)); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_V18 = '7d72fc7f7ae93b2ddad900ba02046ea7d66d69bcd669b3af865a6f1295140345'  # G-ORIG: option (C), acc2 two-producer acceptance
out('m3_run_v1_8_1 item %s LIM %d; script sha256 %s; python %s' % (ITEM, LIM, SELF_SHA, sys.version.split()[0]))
stage('C-HASH')
bad = [f for f, h in OWNMOD.items() if sha(os.path.join(OWN, f)) != h]
bad += [f for f, h in KFILES.items() if sha(os.path.join(C2B, f)) != h]
bad += [f for (d, f), h in INPUTS.items() if os.path.exists(os.path.join(d, f)) and sha(os.path.join(d, f)) != h]
missing = [f for (d, f), h in INPUTS.items() if not os.path.exists(os.path.join(d, f))]
gate('C-HASH', not bad and not missing, '(%d modules, the kernel files, %d inputs)%s%s' % (len(OWNMOD), len(INPUTS),
     (': changed ' + ', '.join(bad)) if bad else '', (': missing ' + ', '.join(missing)) if missing else ''))
plant('PLANT-HASH', sha(os.path.join(OWN, 'm3_scal_v2.py')) != OWNMOD['m3_scal_v2.py'][:-1] + ('0' if OWNMOD['m3_scal_v2.py'][-1] != '0' else '1'),
      '(m3_scal_v2 against a sha with its last digit changed)')
if FAILS:
    finish()
    sys.exit(1)
from fractions import Fraction
from decimal import Decimal
import importlib.util
GENERIC = [('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_major', 'm3_major_v2.py'),
           ('m3_bar', 'm3_bar_v10.py'), ('m3_entries', 'm3_entries_v3.py'), ('m3_record', 'm3_record_v4.py'), ('m3_reader', 'm3_reader_v4_4.py'),
           ('m3_handoff', 'm3_handoff_v3.py')]


def load_as(name, fname):
    """a pinned file of pk03/ loaded under its generic module name (dependencies first)."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(OWN, fname))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


MODS = {name: load_as(name, fname) for name, fname in GENERIC}
S, GR, SER, BAR, ENT, REC, RDR, HO = (MODS[k] for k in ('m3_scal', 'm3_graph', 'm3_series', 'm3_bar', 'm3_entries', 'm3_record', 'm3_reader',
                                                         'm3_handoff'))
sys.path.append(C2B)
import arbeng_ma_v1_3 as K
import arbeng_ma_stub_v1_1 as A
_to_arb0 = {'layer': K.to_arb, 'arb': A.to_arb}


def _guard(which):
    def conv(v):
        """the kernel's own converter, refusing mp.iv values: M3 passes arb balls only (a checked fact since m3_run_v1_3)."""
        if hasattr(v, '_mpi_'):
            raise TypeError('an mp.iv value reached the %s kernel converter; M3 passes arb only' % which)
        return _to_arb0[which](v)
    return conv


K.to_arb = _guard('layer')
A.to_arb = _guard('arb')
BAR.ARB['kern'] = A
import flint
from mpmath import iv
badw = [n for n, m in MODS.items() if os.path.abspath(m.__file__) != os.path.join(OWN, dict(GENERIC)[n])]
badw += [] if os.path.dirname(os.path.abspath(K.__file__)) == C2B else ['kernel']
badw += [] if os.path.dirname(os.path.abspath(A.__file__)) == C2B else ['arb kernel']
gate('C-IMPORT', not badw and K.VERSION == KERNEL and A.VERSION == ARBK, '(generic names from their pinned files in %s; kernel %s and arb kernel %s from %s)%s' % (
    OWN, K.VERSION, A.VERSION, C2B, (': ' + ', '.join(badw)) if badw else ''))
stage('C-VALIDATED')
vbad = []
if os.path.abspath(K.__file__) != os.path.join(C2B, KERNEL + '.py') or sha(os.path.abspath(K.__file__)) != KFILES[KERNEL + '.py']:
    vbad.append('the imported layer is not pk02/%s.py with the pinned sha256' % KERNEL)
for d_, f_, h_ in VALREC:
    p_ = os.path.join(d_, f_)
    if not os.path.exists(p_) or sha(p_) != h_:
        vbad.append('%s missing or changed' % f_)
    elif f_.startswith('out_kt_ma_val'):
        with open(p_) as fh:
            vl = [ln.rstrip('\n') for ln in fh if ln.startswith('VERDICT')]
        if vl != ['VERDICT VALID']:
            vbad.append('%s: VERDICT lines %r' % (f_, vl))
TAG = tag_for(KERNEL + '.py', KFILES[KERNEL + '.py'], [v[2] for v in VALREC])
gate('C-VALIDATED', not vbad and TAG == '', '(layer %s:%s; %d validation records with exactly ["VERDICT VALID"] and the close by sha256; TAG %r)%s' % (
    KERNEL, KFILES[KERNEL + '.py'][:8], len(VALREC), TAG, (': ' + '; '.join(vbad)) if vbad else ''))
d11 = [k for k in DENY if k[0] == 'arbeng_ma_v1_1.py'][0]
plant('PLANT-DENY', tag_for(d11[0], d11[1], [v[2] for v in VALREC], set(VALIDATED) | {(d11[0], d11[1], tuple(v[2] for v in VALREC))}) != '',
      '(arbeng_ma_v1_1 placed in a copy of VALIDATED must still be refused the certified tag)')
SER_RE = re.compile(r'[A-Za-z0-9]' + '_series' + r'\s*\(')
ser_hits = []
for p_ in [os.path.join(OWN, f) for f in OWNMOD] + [os.path.join(C2B, f) for f in KFILES] + [os.path.abspath(__file__)]:
    with open(p_) as fh:
        ser_hits += ['%s:%d' % (os.path.basename(p_), i + 1) for i, ln in enumerate(fh) if SER_RE.search(ln)]
gate('C-SERIES', not ser_hits, '(no *_series( call in %d modules, the kernel files and this script)%s' % (len(OWNMOD), (': ' + ', '.join(ser_hits)) if ser_hits else ''))
plant('PLANT-SERIES', bool(SER_RE.search('x = acb' + '_series(1)')), '(a planted *_series( call must be flagged)')
S.setup()
flint.ctx.prec = K.PREC
gate('C-PREC', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d = the layer\'s PREC %d)' % (flint.ctx.prec, K.PREC))
out('PRECISION start: %s; env %s' % (S.precision_line(), K.env_probes()))
cx_ok, cx_fired = S.crossings_test()
gate('C-CX', cx_ok, '(M3\'s own mp.iv <-> arb crossings: round trips contain their sources)')
plant('PLANT-CX', cx_fired, '(the unsigned to_man_exp form must lose -1/3)')


def _ef(raw):
    """an mp.iv end as an exact rational from its raw (sign, man, exp, bc); special values raise."""
    sign, man, exp, bc = raw
    if man == 0 and exp != 0:
        raise ValueError('special interval end %r' % (raw,))
    v = Fraction(man) * Fraction(2) ** exp
    return -v if sign else v


cx2 = []
for lo_, hi_ in (('-0.25', '0.75'), ('-0.75', '0.25'), ('-0.5', '0')):
    x_ = iv.mpf([lo_, hi_])
    a_ = S.iv_to_arb(x_)
    b_ = [_ef(r) for r in S.arb_to_iv(a_)._mpi_]
    cx2.append(a_.contains(flint.arb(lo_)) and a_.contains(flint.arb(hi_)) and b_[0] <= Fraction(lo_) and Fraction(hi_) <= b_[1])
gate('C-CX2', all(cx2), '(asymmetric straddling and zero-end intervals [-0.25, 0.75], [-0.75, 0.25], [-0.5, 0]: iv -> arb holds both ends, '
     'arb -> iv holds the source)')
from mpmath import libmp
x_ = iv.mpf(['-0.25', '0.75'])
um = [libmp.to_man_exp(r) for r in x_._mpi_]
uarb = (flint.arb(int(um[0][0])) * flint.arb(2) ** int(um[0][1])).union(flint.arb(int(um[1][0])) * flint.arb(2) ** int(um[1][1]))
plant('PLANT-CX2', not uarb.contains(flint.arb('-0.25')), '(the unsigned to_man_exp form of [-0.25, 0.75] must lose -0.25)')
gfired = []
for mod in (K, A):
    try:
        mod.to_arb(iv.mpf(1) / 3)
        gfired.append(False)
    except TypeError:
        gfired.append(True)
plant('PLANT-GUARD', all(gfired), '(an mp.iv value handed to either kernel converter must raise)')


def fallback_tests():
    """C-FALLBACK-PATH: a MAFallback forced at a 2-form table (Gam = [[2, 1], [1, 3]], W_int = I) is recomputed by the arb kernel, whose
    ball must overlap the layer's own for the same E2; PLANT-FALLBACK-ONLY: a ValueError in the layer's E2 must reach the caller."""
    tb = BAR.TableFB(K, S.arb_mat_of([[2, 1], [1, 3]]), NN - 1, 4, None, None, [[1, 0], [0, 1]], 'fallback test')
    P = S.spoly(K, {(1, 0): 1, (0, 1): -1}, 2)
    Q = S.spoly(K, {(1, 1): 1}, 2)
    v_ma = tb.E2(P, Q)
    real = tb.tab

    class Raise:
        def __init__(self, exc):
            self.exc = exc

        def E2(self, P_, Q_, fallback=True):
            raise self.exc

    n0 = len(BAR.FALLBACKS)
    tb.tab = Raise(K.MAFallback('forced by C-FALLBACK-PATH'))
    v_arb = tb.E2(P, Q)
    gate('C-FALLBACK-PATH', len(BAR.FALLBACKS) == n0 + 1 and v_ma.overlaps(v_arb),
         '(a forced MAFallback: the arb kernel\'s E2 %s overlaps the layer\'s %s)' % (v_arb.str(12), v_ma.str(12)))
    tb.tab = Raise(ValueError('planted'))
    try:
        tb.E2(P, Q)
        fired = False
    except ValueError:
        fired = True
    plant('PLANT-FALLBACK-ONLY', fired, '(a ValueError in the layer\'s E2 must reach the caller)')
    tb.tab = real
    del BAR.FALLBACKS[:]


def fb_info():
    """the item's MAFallback recomputes (INFO), printed and kept in its hand-off."""
    out('FALLBACKS %d (MAFallback recomputes in arb, INFO)%s' % (len(BAR.FALLBACKS), (': ' + '; '.join(BAR.FALLBACKS[:20])) if BAR.FALLBACKS else ''))
    return list(BAR.FALLBACKS)


fallback_tests()
T_REF = Fraction(1, 300)


def read_lines(path, tag):
    with open(path) as fh:
        return [json.loads(ln[len(tag) + 1:]) for ln in fh if ln.startswith(tag + ' ')]


with open(os.path.join(W4, 'S8_ENTRY_LIST_v3.json')) as fh:
    LIST = json.load(fh)
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]
TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)
TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)])}
GMAP = {'D': 'D', 'N': 'N', 'E2': 'mix', 'E3': 'E3', 'FF': 'free2'}   # the list's graph name -> m3_entries_v3's
VG = {v: k for k, v in GMAP.items()}
V3 = [{'id': '%s:%s' % (GMAP[e['graph']], e['key']), 'key': e['key'], 'graph': GMAP[e['graph']], 'factors': e['factors'],
       'parity': 'zero' if e['parity_zero'] else 'free', 'grouping': 'std'} for e in LIST['entries']]
REFOUT = {'D': (['m3ref_v1_10_V3D.4.0-32_z9sym.out', 'm3ref_v1_10_V3D.4.33-65_z9sym.out'] if NN == 4 else ['m3ref_v1_10_V3D.3.all_z9sym.out']),
          'N': ['m3ref_v1_10_V3N.%d.all_z9sym.out' % NN], 'mix': ['m3ref_v1_10_V3E2.%d.all_z9sym.out' % NN],
          'E3': ['m3ref_v1_10_V3E3.%d.all_z9sym.out' % NN], 'free2': ['m3ref_v1_10_V3FF.%d.all_z9sym.out' % NN]}
RULE = (80.0, 0.6, 0.7)   # the float references' radii sqrt(min(80 G_vv/J, 0.6)) and rho' (S8's 3-column conventions)
PFX = {'N': 'N', 'E3': 'E3'}   # item prefixes of the families run in prep stages and pieces
MAXP = {'N': 19, 'E3': 9}


def name_of(e):
    return e['key']


def qcap_of(e):
    """qcap 6 for every entry of the list (S8's convention; m3ref_v1_10 ran the same)."""
    return 6


def entries_of(graph, names=None):
    out_ = [e for e in V3 if e['graph'] == graph and (names is None or name_of(e) in names)]
    if names is not None:
        assert sorted(name_of(e) for e in out_) == sorted(names), (names, [name_of(e) for e in out_])
    return out_


def family_graph(graph):
    """the family's GraphIV with the union of the pair forms of all its entries (values do not depend on unused pairs), and C-GRAPH-LIST:
    its couplings equal the list's column spec (m3_graph_v3.strip) as a set and its pairs equal the list's (PLANT-GRAPH-LIST)."""
    fls = [[ENT.factor(TS, graph, enc) for enc in e['factors']] for e in V3 if e['graph'] == graph]
    g = ENT.build_graph(graph, NN, fls)
    spec = LIST['graphs'][VG[graph]]
    Vs, Es = GR.strip(spec['columns'])
    V0, E0 = ENT.graph_edges(graph, NN)
    want = sorted(tuple(sorted(p)) for p in spec['pairs'])
    got = sorted(tuple(sorted(p)) for p in g.pairs)
    edges = lambda E: set((tuple(sorted(e)), c) for e, c in E)
    gate('C-GRAPH-LIST', V0 == Vs and edges(E0) == edges(Es) and got == want, '(%s: couplings equal the list\'s columns %s as a set; '
         'pairs %s equal the list\'s)' % (graph, spec['columns'], got))
    plant('PLANT-GRAPH-LIST', got[1:] != want, '(%s: the pair list without its first pair)' % graph)
    return g


def ref_files(graph):
    return [os.path.join(OUTD, fn) for fn in REFOUT[graph]]


def ref_prep(graph):
    return read_lines(ref_files(graph)[0], 'PREPJSON')[0]


def make_prep(graph, g, stages, scalars=None):
    rp = ref_prep(graph)
    mid = [(S.up(gv) + S.down(gv)) / 2 for gv in g.Gvv]
    want = [min(RULE[0] * m / 300, RULE[1]) for m in mid]
    drule = max([abs(a - w) / w for a, w in zip(rp['a_v'], want)] + [abs(rp['ap'] - RULE[2] ** 2) / RULE[2] ** 2])
    gate('C-RULE', len(want) == len(rp['a_v']) and drule <= 1e-12, '(%s: the reference radii^2 = min(%g G_vv/300, %g) and rho\'^2 = %g^2, '
         'G_vv the certified mids: max relative difference %.1e (tol 1e-12))' % (graph, RULE[0], RULE[1], RULE[2], drule))
    bad = [min(1.01 * RULE[0] * m / 300, 1.01 * RULE[1]) for m in mid]
    plant('PLANT-RULE', not (max(abs(a - w) / w for a, w in zip(rp['a_v'], bad)) <= 1e-12), '(%s: 80 and 0.6 times 1.01)' % graph)
    pr = BAR.Prep(K, g, 300, rp['a_v'], rp['ap'], rp['theta0'], 6, log=out, stages=stages, scalars=scalars)
    encl = [-iv.log(1 - S.I(a)) / (2 * S.I(a)) * (1 / S.I(300)) for a in rp['a_v']]
    gate('C-TILT', pr.ok and all(S.I(r) >= x.b for r, x in zip(pr.rates, encl)),
         '(a) %d tilt rates rounded up from their mp.iv enclosures; (b) both tilts certainly positive definite (lowest pivots %s, %s)' % (
             len(pr.rates), None if not pr.tilt_c else S.down(pr.tilt_c['low']), None if not pr.tilt_p else S.down(pr.tilt_p['low'])))
    gate('C-PREP-REF', rp['family'] == 'V3' + VG[graph] and rp['N'] == NN and rp['J'] == 300, '(%s: %s PREPJSON of family %s, N %r, J %r)' % (
        graph, REFOUT[graph][0], rp['family'], rp['N'], rp['J']))
    return pr, rp


def laws_of(pr, mF):
    """U3's laws (PLAN_M3_CODE_v1_2 sect. C) and Lemma U's far rate (lower end) for an entry with J-degree m_F."""
    g = pr.g
    cF = mF + Fraction(g.n * (g.V - 1), 2)
    rate = pr.alpha_lo - S.I(cF) / 300
    return {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, g.Gvv)]},
            'ann': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, pr.tilt_p['Gvv'])]},
            'far_rate': S.down(rate), 'far_cF': str(cF)}, rate


def compute_entry(pr, e, state=None):
    """one entry: (result dict for the hand-off). Parity zeros: C-ODD and a_k balls containing 0, no bars."""
    name = name_of(e)
    facs = [ENT.factor(TS, e['graph'], enc) for enc in e['factors']]
    pr.qcap = qcap_of(e)
    pr.maxrel = 0.0
    t0 = cpu()
    STAGE[0] = 'entry %s' % name
    if e['parity'] == 'zero':
        ok, why = ENT.c_odd(e['graph'], NN, facs)
        gate('C-ODD', ok, '%s: %s' % (name, why))
        ak, _, info = pr.bound(facs, e.get('grouping', 'std'), bars=False, entry=name, state=state)
        has0 = all(a.a <= 0 <= a.b for a in ak)
        gate('C-ODD-AK', has0, '%s: every a_k ball contains 0 (widest %.1e)' % (name, max(float((a.b - a.a).b) for a in ak)))
        out('STAGE-CPU entry %s %.2f s (parity zero)%s' % (name, cpu() - t0, resumed(state)))
        return {'name': name, 'parity': 'zero', 'ak': ak, 'qcap': pr.qcap, 'cpu': cpu() - t0}
    ak, bars, info = pr.bound(facs, e.get('grouping', 'std'), entry=name, state=state)
    laws, rate = laws_of(pr, info['mF'])
    gate('C-MONO-FAR', rate.a > 0, '%s: far rate alpha_min - (m_F + n(V-1)/2)/J_REF = %.4e > 0 (m_F %d)' % (name, S.down(rate), info['mF']))
    a0 = 1 if all(f[0] == 'p' for f in facs) else None
    rec = REC.entry_record(ak, bars, T_REF, 'free', a0_exact=a0, laws=laws)
    barsum = rec['Bp']['rem'] + rec['Bp']['tail'] + rec['Bp']['ann'] + rec['Bp']['far']
    okb = pr.maxrel <= 1e-3 and rec['B']['rnd'] <= 0.1 * barsum
    gate('C-BUDGET', okb, '%s: largest relative radius of a norm %.1e (<= 1e-3), rnd %.2e <= 0.1 x bar %.3e' % (name, pr.maxrel, rec['B']['rnd'], barsum))
    out('AKRAD-INFO %s: largest relative radius of an a_k %.2e' % (name, info.get('ak_relrad', 0.0)))
    out('ENTRY %s ak %s err %.9e parts rem %.9e tail %.9e ann %.9e far %.9e rnd %.3e groups %d Dn %d forms %d' % (
        name, ['%.12g' % x for x in rec['ak']], rec['err'], rec['B']['rem'], rec['B']['tail'], rec['B']['ann'], rec['B']['far'], rec['B']['rnd'],
        info['groups'], info['Dn'], len(info['forms'])))
    out('STAGE-CPU entry %s %.2f s%s' % (name, cpu() - t0, resumed(state)))
    return {'name': name, 'parity': 'free', 'ak': ak, 'bars': bars, 'a0_exact': a0, 'laws': laws, 'qcap': pr.qcap,
            'maxrel': pr.maxrel, 'cpu': cpu() - t0}


def plant_mono(pr):
    """PLANT-MONO: with theta0 = 1e-3 the far rate must not be certainly positive."""
    g = pr.g
    alpha = min((S.I(1e-3) * S.I(pr.ap) / (2 * gv)).a for gv in g.Gvv)
    rate = alpha - S.I(Fraction(g.n * (g.V - 1), 2)) / 300
    plant('PLANT-MONO', not (rate.a > 0), '(theta0 = 1e-3: far rate %.3e)' % S.down(rate))


def plant_odd(graph):
    """PLANT-ODD: one odd-state S entry + 1e-12 in a copy of the trial set must make C-ODD refuse g,0,2's zero."""
    import copy
    ts2 = copy.deepcopy(TS)
    ts2.S[1][2] = ts2.S[1][2] + 1e-12
    e = [x for x in V3 if x['id'] == 'D:g,0,2'][0]
    ok, why = ENT.c_odd('D', NN, [ENT.factor(ts2, 'D', enc) for enc in e['factors']])
    plant('PLANT-ODD', not ok, '(S[1][2] + 1e-12: %s)' % why)


def header(fam):
    return {'script': SELF_SHA, 'item': ITEM, 'family': fam, 'N': NN, 'kernel': '%s:%s' % (KERNEL, KFILES[KERNEL + '.py'][:8]),
            'arb_kernel': '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), 'trial': TRIAL, 'format': 'm3_run_v1_8 hand-off'}


def same(x, y):
    """exact equality of hand-off values: intervals by their raw ends, containers recursively."""
    if hasattr(x, '_mpi_') or hasattr(y, '_mpi_'):
        return hasattr(x, '_mpi_') and hasattr(y, '_mpi_') and x._mpi_ == y._mpi_
    if isinstance(x, dict) and isinstance(y, dict):
        return set(map(str, x)) == set(map(str, y)) and all(same(x[k], y[str(k)] if str(k) in y else y[k]) for k in x)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        return len(x) == len(y) and all(same(a, b) for a, b in zip(x, y))
    return x == y


def write_handoff(fam, body):
    name = 'm3_run_v1_8_%s.json' % ITEM
    path, hsha = HO.write(name, header(fam), body)
    out('HANDOFF %s %s' % (name, hsha))
    with open(path) as fh:
        text = fh.read()
    hdr_rt, body_rt = HO.read_text(text, {'script': SELF_SHA, 'item': ITEM, 'N': NN})
    gate('C-HANDOFF-RT', same(body, body_rt), '(the hand-off decodes to exactly the values written)')
    for lab, refused in HO.plant_handoff(text, {'script': SELF_SHA, 'item': ITEM, 'N': NN}):
        plant('PLANT-HANDOFF', refused, '(%s tampered in memory)' % lab)
    plant('PLANT-VERDICT', HO.plant_verdict(valid_verdict()), '(a producer record whose VERDICT line extends %r must be refused)' % valid_verdict())


def read_handoff(item, fam):
    name = 'm3_run_v1_8_%s.json' % item
    hdr, body = HO.read(name, ACC.out(os.path.join(OUTD, 'm3_run_v1_8_%s.out' % item), V18_SHA, ORIG_V18), {'script': ACC.expect(os.path.join(HANDD, name), V18_SHA, ORIG_V18), 'item': item, 'N': NN, 'family': fam},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (name, valid_verdict()))
    return body


def resumed(state):
    return (' (this piece; %d units of the entry restored)' % len(state['vals'])) if state else ''


def check_resume(pr, e):
    """C-RESUME (m3_bar_v8): one free entry computed straight, then from forced checkpoints at the end of stage a (after 'm0c') and at
    the end of stage b (before the first 'c' unit), each state through a hand-off encode/decode round trip and resumed with fresh table
    and group caches; the a_k and the bars must be identical to the straight run's. PLANT-RESUME: the stage-a state with m0u doubled
    must change the bars."""
    name = name_of(e)
    facs = [ENT.factor(TS, e['graph'], enc) for enc in e['factors']]
    gr = e.get('grouping', 'std')
    pr.qcap = qcap_of(e)

    def run(state=None, cut=None):
        pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0
        cnt = [0]
        if cut is not None:
            pr.unit_done = lambda dt, prog: cnt.__setitem__(0, cnt[0] + (1 if prog else 0))
            pr.ubudget = lambda: cnt[0] < cut
        try:
            return pr.bound(facs, gr, entry=name, state=state), None
        except BAR.Checkpoint as cp:
            return None, HO.dec(json.loads(json.dumps(HO.enc(cp.state))))
        finally:
            pr.ubudget = pr.unit_done = None
    (ak0, b0, _), _ = run()
    seq = list(pr.ustate['vals'])
    cuts = [seq.index('m0c') + 1, next(i for i, k in enumerate(seq) if k.endswith('|c'))]
    ok, why, st_a = True, [], None
    for cut in cuts:
        _, st = run(cut=cut)
        st_a = st if st_a is None else st_a
        r1, _ = run(state=st)
        same_ = st is not None and len(st['vals']) == cut and r1 is not None and same(ak0, r1[0]) and same(b0, r1[1])
        ok = ok and same_
        why.append('cut after %d of %d units: %s' % (cut, len(seq), 'identical' if same_ else 'DIFFERENT'))
    gate('C-RESUME', ok, '(%s: %s)' % (name, '; '.join(why)))
    bad = dict(st_a, vals=dict(st_a['vals']))
    bad['vals']['m0u'] = 2 * bad['vals']['m0u']
    r2, _ = run(state=bad)
    plant('PLANT-RESUME', r2 is not None and not same(b0, r2[1]), '(%s: the stage-a state with m0u doubled must change the bars)' % name)
    pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0



def run_small(graph):
    stage('graph %s' % graph)
    g = family_graph(graph)
    pr, rp = make_prep(graph, g, ('u', 'c'))
    out('PREP %s N=%d: V %d, F %d, radii from %s, theta0 %r; rE %.6e nC8 %.6e nC6 %.6e farbase %.6e' % (
        graph, NN, g.V, g.F, REFOUT[graph][0], rp['theta0'], float(pr.rE.mid), float(pr.nC8.mid), float(pr.nC6.mid), float(pr.farbase.b)))
    plant_mono(pr)
    if graph == 'D':
        plant_odd(graph)
    res = [compute_entry(pr, e) for e in entries_of(graph)]
    if graph == 'D':
        check_resume(pr, [x for x in entries_of('D') if x['parity'] == 'free'][0])
    body = {'family': graph, 'entries': res, 'scal_u': pr.scalars_out('u'), 'scal_c': pr.scalars_out('c'), 'fallbacks': fb_info()}
    write_handoff(graph, body)


def run_prep_stage(graph, stg):
    stage('%s prep stage %s' % (graph, stg))
    g = family_graph(graph)
    pr, rp = make_prep(graph, g, (stg,))
    body = {'family': graph, 'stage': stg, 'scal': pr.scalars_out(stg)}
    if stg == 'c':
        plant_mono(pr)
    body['fallbacks'] = fb_info()
    write_handoff(graph, body)


def order_of(graph):
    """a piece family's entries in the list's order (the resumable pieces walk it)."""
    return [name_of(e) for e in entries_of(graph)]


CAPPED = 'VERDICT INCOMPLETE (CAP-STOP)'


def piece_state(graph, piece):
    """'valid' (its hand-off exists; read_handoff checks it), 'capped' (no hand-off; the output's first line names this script and
    item, and its VERDICT lines are exactly [CAPPED]) or 'missing' (no output); anything else raises ValueError."""
    item = '%sk%d.%d' % (PFX[graph], piece, NN)
    po = os.path.join(OUTD, 'm3_run_v1_8_%s.out' % item)
    ho = os.path.join(HANDD, 'm3_run_v1_8_%s.json' % item)
    if not os.path.exists(po):
        if os.path.exists(ho):
            raise ValueError('%s: a hand-off without its producer output' % item)
        return 'missing'
    if os.path.exists(ho):
        return 'valid'
    with open(po) as fh:
        lines = fh.read().split('\n')
    m = re.fullmatch(r'm3_run_v1_8 item (\S+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)', lines[0])
    if m and m.group(1) == item and ACC.ok(po, m.group(3), V18_SHA, ORIG_V18) and HO.verdict_ok(lines, CAPPED):
        return 'capped'
    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)


def run_nk(graph, piece):
    stage('%s keys piece %d' % (graph, piece))
    order = order_of(graph)
    g = family_graph(graph)
    su = read_handoff('%su.%d' % (PFX[graph], NN), graph)['scal']
    sc = read_handoff('%sc.%d' % (PFX[graph], NN), graph)['scal']
    start, caps, partial = 0, 0, None
    for j in range(piece - 1, 0, -1):
        st = piece_state(graph, j)
        if st == 'capped':
            caps += 1
            continue
        if st != 'valid':
            raise ValueError('%sk%d.%d is %s, so piece %d cannot start' % (PFX[graph], j, NN, st, piece))
        prev = read_handoff('%sk%d.%d' % (PFX[graph], j, NN), graph)
        start, partial = prev['next'], prev['partial']
        break
    factor = 1.5 * 2 ** caps
    nin = len(partial['vals']) if partial else 0
    out('PIECE-START %s piece %d resumes at entry %d%s after %d capped piece(s); stop factor %.1f' % (
        graph, piece, start, (' with %d units of %s restored' % (nin, partial['entry'])) if partial else '', caps, factor))
    pr, rp = make_prep(graph, g, (), scalars=dict(su, **sc))
    slow, units = [60.0], [0]

    def budget():
        return units[0] == 0 or cpu() + factor * slow[0] <= LIM - 20

    def done(dt, progress):
        slow[0] = max(slow[0], dt)
        if progress:
            units[0] += 1
    pr.ubudget, pr.unit_done = budget, done
    res, i, part = [], start, None
    while i < len(order):
        try:
            res.append(compute_entry(pr, entries_of(graph, [order[i]])[0], state=partial))
        except BAR.Checkpoint as cp:
            part = cp.state
            break
        partial = None
        i += 1
    pr.ubudget = pr.unit_done = None
    nout = len(part['vals']) if part else 0
    prog = i > start or (part is not None and nout > nin)
    gate('C-PIECE', prog, '(%s piece %d: entries %d..%d of %d done, next %d; %d units computed%s)' % (
        graph, piece, start, i - 1, len(order), i, units[0], (', %d units of %s carried' % (nout, part['entry'])) if part else ''))
    write_handoff(graph, {'family': graph, 'piece': piece, 'start': start, 'next': i, 'partial': part, 'stop_factor': factor,
                          'entries': res, 'fallbacks': fb_info()})


FILES = ('D', 'E2', 'E3', 'FF')   # asmP: the N family is not assembled


def write_records(texts, paths, fails, nofire, tag, opener=open):
    """writes the record texts (open 'x', inside out/, no file there yet) only when no gate has failed, every
    plant so far has fired and the TAG is certified; returns [(file key, path)] written, or [] when it refuses."""
    if set(texts) != set(FILES) or set(paths) != set(FILES):
        raise ValueError('asmP writes exactly the records of %s and never an N record, not %s' % (FILES, sorted(set(texts) | set(paths))))
    if fails or nofire or tag != '':
        return []
    for f in FILES:
        if os.path.dirname(os.path.abspath(paths[f])) != OUTD or os.path.exists(paths[f]):
            raise ValueError('record path %s: outside out/ or already there' % paths[f])
    done = []
    for f in FILES:
        with opener(paths[f], 'x') as fh:
            fh.write(texts[f])
        done.append((f, paths[f]))
    return done


def walk_pieces(graph, res):
    """C-PIECES: the pieces of a family cover its entries in order, each advancing, none left in progress; their entries go into res."""
    order, nxt, piece, nin = order_of(graph), 0, 1, 0
    while nxt < len(order) and piece <= MAXP[graph]:
        st = piece_state(graph, piece)
        if st == 'missing':
            break
        if st == 'capped':
            out('PIECE-CAPPED %sk%d.%d: a clean CAP-STOP of this script, no hand-off; skipped and kept' % (PFX[graph], piece, NN))
            piece += 1
            continue
        body = read_handoff('%sk%d.%d' % (PFX[graph], piece, NN), graph)
        pt = body['partial']
        nout = len(pt['vals']) if pt else 0
        okp = body['start'] == nxt and (body['next'] > nxt or nout > nin) and (pt is None or (body['next'] < len(order) and pt['entry'] == order[body['next']]))
        gate('C-PIECES', okp, '(%sk%d.%d: entries %d..%d complete%s)' % (PFX[graph], piece, NN, body['start'], body['next'] - 1,
                                                                          (', %d units of %s carried' % (nout, pt['entry'])) if pt else ''))
        for r in body['entries']:
            res[(graph, r['name'])] = r
        nxt, piece, nin = body['next'], piece + 1, nout
    gate('C-PIECES', nxt == len(order) and nin == 0, '(the %s pieces cover all %d %s entries, in order, none left in progress)' % (
        graph, len(order), graph))


def run_asm():
    stage('asm')
    res = {}
    for item, graph in (('D', 'D'), ('E2', 'mix'), ('FF', 'free2')):
        body = read_handoff('%s.%d' % (item, NN), graph)
        for r in body['entries']:
            res[(body['family'], r['name'])] = r
    walk_pieces('E3', res)
    # asmP: the N pieces are not walked (option 5)
    refs = {}
    for graph in [g_ for g_ in REFOUT if g_ != 'N']:
        refs[graph] = {}
        for p in ref_files(graph):
            with open(p) as fh:
                lines = fh.read().split('\n')
            okv = HO.verdict_ok(lines, 'VERDICT VALID') and [ln for ln in lines if ln.startswith('TRIAL')] == ['TRIAL z9sym']
            gate('C-HASH-REF', okv, '(%s, sha256 %s: VERDICT lines exactly [VERDICT VALID], TRIAL lines exactly [TRIAL z9sym])' % (
                os.path.basename(p), sha(p)))
            for d in read_lines(p, 'KEYJSON'):
                refs[graph][d['key']] = d
    files = {f: {} for f in FILES}
    for e in [x for x in V3 if x['graph'] != 'N']:
        r = res[(e['graph'], name_of(e))]
        if r['parity'] == 'zero':
            files[VG[e['graph']]][name_of(e)] = REC.entry_record(None, None, T_REF, 'zero')
        else:
            files[VG[e['graph']]][name_of(e)] = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=r['a0_exact'], laws=r['laws'])
    want = {f: set(e['key'] for e in LIST['entries'] if e['graph'] == f) for f in FILES}
    gate('C-SCOPE', all(set(files[f]) == want[f] for f in FILES), '(the four files hold exactly the list\'s keys of their graphs: %s)' % (
        ', '.join('%s %d' % (f, len(files[f])) for f in FILES)))
    plant('PLANT-SCOPE', not all(set(list(files[f])[1:] if f == 'D' else files[f]) == want[f] for f in FILES), '(D without one key)')
    rep, rak = [], []
    for e in [x for x in V3 if x['graph'] != 'N']:
        r = res[(e['graph'], name_of(e))]
        if r['parity'] == 'zero':
            continue
        it = files[VG[e['graph']]][name_of(e)]
        d = refs[e['graph']][name_of(e)]
        for p in ('rem', 'tail', 'ann', 'far'):
            if d['B'][p] > 0:
                rep.append((it['B'][p] / d['B'][p], name_of(e), p))
        for k, (a, fa) in enumerate(zip(r['ak'], d['ak'])):
            rak.append((abs(float(a.mid) - fa) / max(1.0, abs(fa)), name_of(e), k))
    lo_, hi_ = min(rep), max(rep)
    gate('C-REP-B', 1 - 1e-6 <= lo_[0] and hi_[0] <= 1.15, '(%d bar parts against m3ref_v1_10 z9sym: certified/float in [%.9f (%s %s), %.6f (%s %s)])' % (
        len(rep), lo_[0], lo_[1], lo_[2], hi_[0], hi_[1], hi_[2]))
    plant('PLANT-REPB', not (1 - 1e-6 <= lo_[0] * 0.5), '(the smallest ratio times 0.5)')
    wr = max(rak)
    gate('C-REP-AK', wr[0] <= 1e-9, '(%d a_k against m3ref_v1_10 z9sym: largest |certified mid - float| / max(1, |float|) %.2e at %s a_%d)' % (
        len(rak), wr[0], wr[1], wr[2]))
    plant('PLANT-REPAK', not (wr[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')
    # the texts, C-FMT on the texts, the plants, and only then the write
    tag = TAG
    eng = {'m3_run_v1_8_1': SELF_SHA, 'entries_by': 'm3_run_v1_8.py:' + V18_SHA, 'modules': dict(OWNMOD)}
    kern = {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}
    fams = {gr: {k: ref_prep(gr)[k] for k in ('a_v', 'ap', 'theta0')} for gr in ('D', 'mix', 'E3', 'free2')}
    texts, paths = {}, {}
    for f in FILES:
        extra = {'entry_list': 'S8_ENTRY_LIST_v3.json:%s' % INPUTS[(W4, 'S8_ENTRY_LIST_v3.json')], 'graph': f, 'graph_m3': GMAP[f],
                 'partial': 'asmP of m3_run_v1_8_1: the D, E2, E3 and FF records only; the N family is not assembled'}
        top = REC.top_level(NN, 300, fams, TRIAL, eng, tag, kern, extra=extra)
        texts[f] = json.dumps(dict(top, items=files[f]))
        paths[f] = os.path.join(OUTD, 'm3_s8v3_%s_N%d_J300%s_v1_8_1.json' % (f, NN, tag))
        rd = RDR.check_text(texts[f], 300, NN, name=os.path.basename(paths[f]))
        okf = all(rd['entries'][k] == (files[f][k]['ak'], files[f][k]['err']) for k in files[f])
        gate('C-FMT', okf, '(%s: %d keys read back exactly from the text by m3_reader_v4_4; %d bytes; sha256 %s)' % (
            os.path.basename(paths[f]), len(files[f]), len(texts[f]), tsha(texts[f])))
    dd = json.loads(texts['D'])
    k0 = sorted(k for k in dd['items'] if dd['items'][k]['parity'] == 'free')[0]
    dd['items'][k0]['B'].pop('rnd')
    try:
        RDR.check_text(json.dumps(dd), 300, NN)
        plant('PLANT-FMT', False, '(D copy without one rnd)')
    except ValueError:
        plant('PLANT-FMT', True, '(D copy without one rnd)')
    dd2 = json.loads(texts['D'])
    kr = max((k for k in dd2['items'] if dd2['items'][k]['parity'] == 'free'), key=lambda k: sum(dd2['items'][k]['ak_rad']))
    dd2['items'][kr]['B']['rnd'] = 0.0
    try:
        RDR.check_text(json.dumps(dd2), 300, NN)
        plant('PLANT-RND', False, '(D copy with %s rnd = 0)' % kr)
    except ValueError:
        plant('PLANT-RND', sum(dd2['items'][kr]['ak_rad']) > 0, '(D copy with %s rnd = 0; its ak_rad sum %.1e)' % (kr, sum(dd2['items'][kr]['ak_rad'])))
    deny = dict(DENY)
    nx = 3 if NN == 4 else 4
    for lab, mut, jref, nexp in (('PLANT-READER-PRECERT', 'precert', 300, NN), ('PLANT-READER-KERNEL', 'kernel', 300, NN),
                                 ('PLANT-READER-PREC', 'prec', 300, NN), ('PLANT-LAYER-V1_1', 'arbeng_ma_v1_1.py', 300, NN),
                                 ('PLANT-LAYER-V1_2', 'arbeng_ma_v1_2.py', 300, NN), ('PLANT-CLAIM', 'claim', 300, NN),
                                 ('PLANT-ARBK', 'arbk', 300, NN), ('PLANT-ARBB', 'arbb', 300, NN), ('PLANT-JREF', None, 150, NN),
                                 ('PLANT-N', None, 300, nx), ('PLANT-KIND', 'kind', 300, NN)):
        dd3 = json.loads(texts['D'])
        if mut == 'precert':
            dd3['format'] = 'M3_RECORD_v1_PRECERT'
            dd3['claim'] = 'NOT CERTIFIED (PRECERT): ' + dd3['claim']
        elif mut == 'kernel':
            dd3['kernel_sha256'] = dd3['kernel_sha256'][:-1] + ('0' if dd3['kernel_sha256'][-1] != '0' else '1')
        elif mut == 'prec':
            dd3['kernel_prec'] = 256
        elif mut in deny:
            dd3['kernel_file'], dd3['kernel_sha256'] = mut, deny[mut]
        elif mut == 'claim':
            dd3['claim'] = dd3['claim'] + ' '
        elif mut == 'arbk':
            dd3['arb_kernel_sha256'] = dd3['arb_kernel_sha256'][:-1] + ('0' if dd3['arb_kernel_sha256'][-1] != '0' else '1')
        elif mut == 'arbb':
            dd3['arb_base_sha256'] = flip(dd3['arb_base_sha256'])
        elif mut == 'kind':
            dd3['items'][sorted(dd3['items'])[0]].pop('kind')
        what = mut or ('expected J_REF %d' % jref if jref != 300 else 'expected N %d' % nexp)
        try:
            RDR.check_text(json.dumps(dd3), jref, nexp)
            plant(lab, False, '(m3_reader_v4_4 must refuse the mutated D copy: %s)' % what)
        except ValueError:
            plant(lab, True, '(m3_reader_v4_4 refuses the mutated D copy: %s)' % what)
    # the bound load's checks, in memory: the consumers bind a record to the asm output that names it
    dn, dh = os.path.basename(paths['D']), tsha(texts['D'])
    try:
        RDR.loads(texts['D'], 'RECORD %s %s\nVERDICT VALID\n' % (dn, dh), 300, NN, dn)
        gate('C-BOUND-RT', True, '(m3_reader_v4_4.loads accepts the D text under an output that names it and ends VALID)')
    except ValueError as ex:
        gate('C-BOUND-RT', False, '(refused: %s)' % ex)
    for lab, otext in (('PLANT-BOUND-VERDICT', 'RECORD %s %s\nVERDICT VALID-PRECERT\n' % (dn, dh)),
                       ('PLANT-BOUND-INVALID', 'RECORD %s %s\nVERDICT INVALID (C-REP-B)\n' % (dn, dh)),
                       ('PLANT-BOUND-TWO', 'RECORD %s %s\nVERDICT VALID\nVERDICT VALID\n' % (dn, dh)),
                       ('PLANT-BOUND-SHA', 'RECORD %s %s\nVERDICT VALID\n' % (dn, flip(dh))),
                       ('PLANT-BOUND-NONE', 'VERDICT VALID\n')):
        try:
            RDR.loads(texts['D'], otext, 300, NN, dn)
            plant(lab, False, '(m3_reader_v4_4.loads must refuse this asm output)')
        except ValueError:
            plant(lab, True, '(m3_reader_v4_4.loads refuses this asm output)')
    gate('C-PREC-ASM', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d before the write)' % flint.ctx.prec)
    opened = []

    def no_open(p, mode):
        opened.append(p)
        raise OSError('PLANT-NOWRITE: the writer opened %s' % p)
    refused = 0
    for fl, nf, tg in ((FAILS + ['PLANT-FORCED'], NOFIRE, tag), (FAILS, NOFIRE + ['PLANT-FORCED'], tag), (FAILS, NOFIRE, '_PRECERT')):
        try:
            if write_records(texts, paths, fl, nf, tg, opener=no_open) == []:
                refused += 1
        except OSError:
            pass
    plant('PLANT-NOWRITE', refused == 3 and not opened, '(write_records under a failed gate, an unfired plant and a PRECERT tag: %d of 3 refused, %d files opened)' % (
        refused, len(opened)))
    gate('C-NO-N', set(texts) == set(FILES) == {'D', 'E2', 'E3', 'FF'} and not any(os.path.basename(p).startswith('m3_s8v3_N_') for p in paths.values()),
         '(asmP writes the D, E2, E3 and FF records only: %s)' % ', '.join(os.path.basename(paths[f]) for f in FILES))
    try:
        write_records(dict(texts, N=texts['D']), dict(paths, N=os.path.join(OUTD, 'm3_s8v3_N_N%d_J300_v1_8_1.json' % NN)), [], [], '', opener=no_open)
        plant('PLANT-NO-N', False, '(write_records with an N record added must raise before opening any file)')
    except ValueError:
        plant('PLANT-NO-N', not opened, '(write_records with an N record added raises before opening any file)')
    written = write_records(texts, paths, FAILS, NOFIRE, tag)
    if not written:
        out('RECORDS NOT WRITTEN (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE] + ([] if tag == '' else ['TAG %r' % (tag,)])))
    for f, path in written:
        gate('C-WRITE', sha(path) == tsha(texts[f]), '(%s holds exactly its C-FMT text)' % os.path.basename(path))
        out('RECORD %s %s' % (os.path.basename(path), sha(path)))


try:
    if FAM in ('D', 'E2', 'FF'):
        run_small({'D': 'D', 'E2': 'mix', 'FF': 'free2'}[FAM])
    elif FAM in ('Nu', 'Nc'):
        run_prep_stage('N', FAM[1])
    elif FAM in ('E3u', 'E3c'):
        run_prep_stage('E3', FAM[2])
    elif FAM.startswith('Nk'):
        run_nk('N', int(FAM[2:]))
    elif FAM.startswith('E3k'):
        run_nk('E3', int(FAM[3:]))
    else:
        run_asm()
    finish()
except SystemExit:
    raise
except BaseException:
    out('EXCEPTION in stage %s:' % STAGE[0])
    for ln in traceback.format_exc().rstrip().split('\n'):
        out('  ' + ln)
    out('VERDICT INVALID (EXCEPTION)')
    sys.exit(1)
