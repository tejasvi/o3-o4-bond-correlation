#!/usr/bin/env python3
"""m3_run_es_v1_3.py -- pk04 (code/pk04/; outputs in code/pk03/out, hand-offs in code/pk03/hand). The certified E_semi
near-end windows (pk12 21:26:29Z, 21:52:20Z, 22:47:31Z
2414bd75 sect. 1). REVISION of m3_run_es_v1_2.py (fd2229db; one finding, no value changed), split as v1_2 into
this runner and two parts executed in its namespace after C-HASH has checked their bytes against PARTS (m3_run_es_v1_3_ent.py,
m3_run_es_v1_3_asm.py); this file's sha256 with PARTS is the program. Changes from v1_2:
- asm checks every P12 family graph (ES12A, ES12B, ES12C) against its pairs-free prep graph: make_prep on the foreign scalars and
  prep_same (C-PREP-GRAPH with PLANT-PREP-EDGE, -TAG, -GAUGE and -ULP), as v1_1 did at P12 stage u, so the output the records bind holds it.
- C-PREP-FOREIGN-C4 in asm and at a P12 smoke: Pout, Pout_p, farbase and alpha_lo recomputed on the family graph (prep_view's C-4
  values from this run's radii, rho'^2, theta0, J and N) equal the foreign scal_c end for end; PLANT-PREP-FOREIGN-C4 (a_v[0] one ulp up).
- C-PREP-FOREIGN also needs the S8 H record's dmaxH equal to DMAXH['P12']; PLANT-PREP-FOREIGN-SRC (the record's a_v[0] one ulp
  up, H's columns [vac, int, int, vac], dmaxH 18: each refused).
- records are written by jexact, every float as the exact decimal value of its binary64, so a reader of the
  written decimals as exact rationals sees the binary64 values and every relation holds exactly; C-DEC-EXACT checks it on each record
  (parse_float=Fraction), PLANT-DEC-EXACT.
- the script's names in one place: SNAME (outputs, hand-offs, their header format, the piece-state line, the engine key) and RECV (records
  m3_es_<class>_dL<m1|0>_N<N>_J300[_MOCK]_v1_3.json).
- ESm exports MOCK records for all six (class, d_L) of RECDEF (D4M and D3 too; v1_2's ESm made D4 only).
v1_2's changes from v1_1 stand: P12 takes S8's D16 H prep through the foreign reader (C-PREP-FOREIGN, PLANT-PREP-FOREIGN,
PLANT-HANDOFF-FOREIGN; no P12 items; DMAXH P9 18, P12 16); C-SMOKE-AK of ES9 and ES12A against S8's f,0 and h,0, finite balls for ES12B and
ES12C, PLANT-SMOKE-PATH on the rebuilt partition, PLANT-PART-MOVE's merge fallback; asm's C-S8-SAME and PLANT-S8-SAME on E3 and H; ESm in
the certified entry form (C-MOCK-FMT, PLANT-MOCK-CERT, PLANT-MOCK-FMT, RECORD lines).
Arguments: ITEM LIM (5..1500). Output: stdout (out/m3_run_es_v1_3_<ITEM>.out). Run as run_chain_m3_run_es_v1_3.sh's run_item does.
"""
import resource, sys, time, math, hashlib, signal, os, json, re, traceback

SNAME, RECV = 'm3_run_es_v1_3', 'v1_3'   # the script's names (outputs, hand-offs, the engine key) and the records' suffix
FAMRE = 'ES9|ES12A|ES12B|ES12C'
ITEM_RE = r'(P9[uc]|ES(9|12A|12B|12C)(a|k([1-9]|[1-5][0-9]|60)|r[12])|ESm|asm)\.(4|3)'
if len(sys.argv) != 3 or not re.fullmatch(ITEM_RE, sys.argv[1]):
    print('usage: %s.py ITEM LIM   (ITEM = P9u|P9c|<X>a|<X>k1..<X>k60|ES9r1|ES9r2|ESm|asm . 4|3, X = ES9|ES12A|ES12B|ES12C; '
          'LIM = RLIMIT_CPU soft limit in s, 5..1500)' % SNAME)
    sys.exit(2)
ITEM = sys.argv[1]
FAM, NN = ITEM.split('.')[0], int(ITEM.split('.')[1])
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,4}', sys.argv[2]) else -1
if not (5 <= LIM <= 1500):
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
SDIR = CODEDIR + '/pk04'   # this runner and its parts
C2B = CODEDIR + '/pk02'
INP = CODEDIR + '/pk10/scratch'
W4 = CODEDIR + '/pk11/out'
OUTD = OWN + '/out'
HANDD = OWN + '/hand'
LISTD = OWN + '/tmp/r16'
PARTS = {   # executed in this namespace, in this order, after C-HASH (they only define)
    'm3_run_es_v1_3_ent.py': 'd54c8be0c33c34a63dfd1f5e17b017b94b9cbd086634b8a4c1cfaebf9c81fbc7',
    'm3_run_es_v1_3_asm.py': 'e5f675a0fcc32569a845010e767b29165d56bb11b33aa802bc59fe52eeb4f38f',
}
KERNEL = 'arbeng_ma_v1_4_1'   # m3_run_v1_9: the layer of every table, prep and entry here
ARBK = 'arbeng_ma_stub_v1_1'
ARBB = 'arbeng_c2b_v2'   # the arb base under ARBK (pinned in KFILES)
KFILES = {
    'arbeng_ma_v1_4_1.py': '1f58ad80ceb1c0992f08f894c0f6af26ef18d397627020a5a5fe7130818375d9',
    'arbeng_ma_stub_v1_1.py': '794fabc7111555db2f6390a144d3f5af6deeb358d02da8b5705cf3ceaefd0af1',
    'arbeng_c2b_v2.py': '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0',
}
VALREC = [   # m3_run_v1_9: arbeng_ma_v1_4_1's validation records and the two closes, in order
    (C2B, 'MANIFEST_ARBENG_MA_v1_4_1.sha256', 'c172e15f42cad0278bdea3343ddea084327dbf89a4eef2561df7e5d23140f5fc'),
    (C2B, 'MANIFEST_KT_MA_VAL_v1_6_RUN.sha256', '7ec00dc5d98d64c06e345d80b4a0959e7ec6805239a4d03ba7be006882186314'),
    (C2B + '/out', 'out_kt_ma_val_v1_6_1_d.out', 'af1e3f66a88c27b0593b31e23f936986ecd04c813854ed4001cc601f7a6bef12'),
    (CODEDIR + '/rv01', 'REVIEW_CODE_ARBENG_MA_V1_4_rv01.md', '8afbb958904ab2067d75b6876b2b6496dda7286ba99d4d00428e3cd7a4485335'),
    (CODEDIR + '/rv01', 'DELTA_ARBENG_MA_V1_4_1_rv01.md', '3fd1bfa7dc00d4600aa3ff1d413807cb75e9ab9d910600d580ab48bd6b36fc4f'),
]
VALIDATED = {('arbeng_ma_v1_4_1.py', '1f58ad80ceb1c0992f08f894c0f6af26ef18d397627020a5a5fe7130818375d9', tuple(v[2] for v in VALREC))}
DENY = {('arbeng_ma_v1_1.py', '81f7fb89f863343149b1558bfc3c8ba3e09b3e6c36ec00db4c12197b11158e7f'),
        ('arbeng_ma_v1_2.py', '935f2ca77dbcb7de0670d43505044f9c12c086f69de2a30f7b8133522ffcec80'),
        ('arbeng_ma_v1_4.py', '9870e7f8d5dc33f0edca029f9945de4774a1eb572114aa385dd7b75d7506e017'),   # m3_run_v1_9: the unpinned predecessor
        ('mock_arbeng_v1_4.py', '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e')}   # pk03's mock (tmp/r16)


def tag_for(kfile, ksha, vshas, validated=None):
    """as m3_run_v1_10_4 l.76-81."""
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
    'm3_bar_v16_1.py': '475184d4d4545ff0448fed553782c969bbaf6bd13a542605d83be73dc8154f47',
    'm3_entries_v3.py': '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    'm3_record_v4.py': '2c8a53efb5170d6c6e320bd814c824e69d2ccdd73c57cf87a9130b796109e30f',
    'm3_reader_v6_3.py': '539b613f6a9c07a9bef3d0cbb408c1d41de276a6a59aede8b03149204ce28661',
    'm3_handoff_v3.py': 'e4f5bf0b111197d87e9659c89265c68fcfe39e564860c6e6b6eb91c9c48feb21',
}
FSCRIPT = '34abe3743035bd709e202eb4de2bdc752fef8a8abc6ebd5d0e4963050caa1dbb'   # m3_run_v1_9_3.py, the producer of S8's D16 H prep
INPUTS = {
    (LISTD, 'esemi_windows_v2.json'): '1658bb73a21094e66c42896dd698e30054fcb2fbf0b175d05cc97076e17b48c7',   # t_esemi_list_v2 f5f0381b
    (C2B, 'M2B_KV_v1.txt'): '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',   # G-PHI's PIN_TRIAL tokens
    (W4, 'ts_N4_J170_D_S_z9sym_v1.json'): 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    (W4, 'ts_N3_S_z9sym_v1.json'): 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    (W4, 'vacres_K3_N4_sym_v1.json'): 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    (W4, 'vacres_K3_N3_sym_v1.json'): 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    (INP, 'm2_N4_J170.json.b'): '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    (INP, 'm2_N3_J170.json.b'): '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    (OUTD, 'm3ref_v1_10_V3E3.4.all_z9sym.out'): '5cf7ab639fbc53f3ae694e6d073276946a07d82aa71a80e5cc54219f37205cc1',
    (OUTD, 'm3ref_v1_10_V3E3.3.all_z9sym.out'): '10509eb7880bab08f9012527d5e0fd5e46f75942925c3562d780996a0361946b',
    (OUTD, 'm3_s8v3_E3_N4_J300_v1_8_1.json'): 'd1df7d4fc1b8e25f266f34c32180ccb771bc1719cc0fa730f240a33179feff0d',
    (OUTD, 'm3_s8v3_E3_N3_J300_v1_8_1.json'): '6cd3dffbc6fac0845d05aa4b88f135c28a8091eb9623b779d874dace550a078a',
    (OUTD, 'm3_run_v1_8_1_asmP.4.out'): '08c8fab3f4b9080424a40c8cb61b7932f557852520e8d49c5915092a8963a127',
    (OUTD, 'm3_run_v1_8_1_asmP.3.out'): 'b6e9c2dd6a6308f6dc8d72124ba37326156983ec3444625d152ab46f28e927ed',
    (OWN + '/tmp/r16', 'mock_arbeng_v1_4.py'): '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e',   # PLANT-MOCK's file
    (OUTD, 'm3ref_v1_14_P16H.4.p6_z9sym.out'): 'df052bb8e868d03c6ca08cbd5cd4da288e5ab2e82e92e6eee805429b3200703a',   # v1_2: P12's radii
    (OUTD, 'm3ref_v1_14_P16H.3.p6_z9sym.out'): '5029d364ccc4786b5e973cf216ca11677b71169c9cf1da3289fab7bf9d945781',
    (OUTD, 'm3_s8v2_H_N4_J300_v1_9_3.json'): 'cec396204778d2835cc06bef10964928daad9d81ead35987c2762f26bc2d3b7a',   # S8's H records
    (OUTD, 'm3_s8v2_H_N3_J300_v1_9_3.json'): '083797ea6b4ef0452f2d8f42f994db58df2093a499281eca336a772316a23308',
    (OUTD, 'm3_run_v1_9_3_asm.4.out'): 'd028879d269d03888d98707f7e9220bc5cc0623ada99d4507c7751afa3f66dd3',
    (OUTD, 'm3_run_v1_9_3_asm.3.out'): '78f2863f957244472033c34163bcaced0e5a19041d776d7b58b4efc0db5ee59f',
    (OWN, 'm3_run_v1_9_3.py'): FSCRIPT,
    (HANDD, 'm3_run_v1_9_3_Hp10.4.json'): '35c7b6cae2fdc3f44df66481939aebd6aa2efeb1745c83bac139555ed30cec13',   # the finished H preps
    (HANDD, 'm3_run_v1_9_3_Hp14.3.json'): 'b997821c9d35a757c144dd583ddbe0245b161d0cf184f8aa59ed9bbda83ca621',
    (OUTD, 'm3_run_v1_9_3_Hp10.4.out'): 'a4f771084bfcdd54121a8b5fc611055aeec5d1fe7ee0f18e3b2f5072e5a0fa19',
    (OUTD, 'm3_run_v1_9_3_Hp14.3.out'): '2736f1642e239833eb4425301e7cdae3346e1bfcef6ba585e66f7275af4466d5',
    (W4, 'S8_ENTRY_LIST_v2.json'): 'c3830f588dbaa2ef4de558659ab742caa7b231e91810dfd2ec036d66d9cdce5e',   # H's columns (FCOLS)
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
    return hashlib.sha256(text.encode()).hexdigest()


def flip(h):
    """h with its last hex digit changed (plants)."""
    return h[:-1] + ('0' if h[-1] != '0' else '1')


def stage(name):
    STAGE[0] = name
    out('STAGE-CPU %s start %.2f s' % (name, cpu()))


SELF_SHA = sha(os.path.abspath(__file__)); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_SELF = '3d638b75548a2a64ccceaed5b8a558b71bb0d014686c2dcc57529b17a0f99a88'; ORIG_FSCRIPT = '57991eb011023ae9a185423c375d42660eabe88607d207b1a535153a5d94ce5b'; ORIG_K8 = {'arbeng_ma_v1_4_1': '4126e83e', 'arbeng_ma_stub_v1_1': '4fc7e49d'}  # G-ORIG: option (C), acc2 two-producer acceptance
out('%s item %s LIM %d; script sha256 %s; python %s' % (SNAME, ITEM, LIM, SELF_SHA, sys.version.split()[0]))
stage('C-HASH')
PSRC = {}
for f_ in PARTS:   # each part's bytes read once: C-HASH checks them and the dispatch executes exactly these bytes
    try:
        with open(os.path.join(SDIR, f_), 'rb') as fh:
            PSRC[f_] = fh.read()
    except OSError:
        PSRC[f_] = None
bad = [f for f, h in OWNMOD.items() if sha(os.path.join(OWN, f)) != h]
bad += [f for f, h in KFILES.items() if sha(os.path.join(C2B, f)) != h]
bad += [f for f, h in PARTS.items() if PSRC[f] is not None and hashlib.sha256(PSRC[f]).hexdigest() != h]
bad += [f for (d, f), h in INPUTS.items() if os.path.exists(os.path.join(d, f)) and sha(os.path.join(d, f)) != h]
missing = [f for (d, f), h in INPUTS.items() if not os.path.exists(os.path.join(d, f))] + [f for f in PARTS if PSRC[f] is None]
gate('C-HASH', not bad and not missing, '(%d modules, the kernel files, %d parts of this script, %d inputs)%s%s' % (len(OWNMOD), len(PARTS),
     len(INPUTS), (': changed ' + ', '.join(bad)) if bad else '', (': missing ' + ', '.join(missing)) if missing else ''))
plant('PLANT-HASH', sha(os.path.join(OWN, 'm3_scal_v2.py')) != OWNMOD['m3_scal_v2.py'][:-1] + ('0' if OWNMOD['m3_scal_v2.py'][-1] != '0' else '1'),
      '(m3_scal_v2 against a sha with its last digit changed)')
if FAILS:
    finish()
    sys.exit(1)
from fractions import Fraction
import importlib.util
GENERIC = [('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_major', 'm3_major_v2.py'),
           ('m3_bar', 'm3_bar_v16_1.py'), ('m3_entries', 'm3_entries_v3.py'), ('m3_record', 'm3_record_v4.py'), ('m3_reader', 'm3_reader_v6_3.py'),
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
import arbeng_ma_v1_4_1 as K
import arbeng_ma_stub_v1_1 as A
_to_arb0 = {'layer': K.to_arb, 'arb': A.to_arb}


def _guard(which):
    def conv(v):
        """the kernel's own converter, refusing mp.iv values: M3 passes arb balls only."""
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
RUNMAN = [v for v in VALREC if v[1] == 'MANIFEST_KT_MA_VAL_v1_6_RUN.sha256'][0]
rbad, nrun, nvo = [], 0, 0
with open(os.path.join(RUNMAN[0], RUNMAN[1])) as fh:
    for ln in fh:
        h_, p_ = ln.split()
        nrun += 1
        if not os.path.exists(p_) or sha(p_) != h_:
            rbad.append('%s missing or changed' % os.path.basename(p_))
        elif os.path.basename(p_).startswith('out_kt_ma_val') and p_.endswith('.out'):
            nvo += 1
            with open(p_) as fo:
                vl = [x.rstrip('\n') for x in fo if x.startswith('VERDICT')]
            if vl != ['VERDICT VALID']:
                rbad.append('%s: VERDICT lines %r' % (os.path.basename(p_), vl))
gate('C-VALREC-RUN', not rbad and nrun > 0 and nvo > 0, '(%s: %d files re-hashed, %d validation outputs with exactly ["VERDICT VALID"])%s' % (
    RUNMAN[1], nrun, nvo, (': ' + '; '.join(rbad)) if rbad else ''))
MOCK = os.path.join(OWN, 'tmp', 'r16', 'mock_arbeng_v1_4.py')
msha = sha(MOCK)
plant('PLANT-MOCK', tag_for(KERNEL + '.py', msha, [v[2] for v in VALREC]) != '' and tag_for('mock_arbeng_v1_4.py', msha, [v[2] for v in VALREC]) != '',
      '(the mock %s, offered as %s.py and under its own name, must be refused the certified tag)' % (msha[:8], KERNEL))
NFB = ('E2_ma', 'lp_moment_ma', 'lp_ma', 'pos_ma', 'E2_ball', 'e2')   # m3_run_v1_10_3: the bar's defs whose layer calls pass fallback=False


def caller_scan(text):
    """as m3_run_v1_10_4 l.292-311 (its docstring)."""
    bad, fn, nfb = [], '', 0
    for i, ln in enumerate(text.split('\n')):
        code = ln.split('#')[0]
        m = re.match(r'\s*def (\w+)\(', code)
        fn = m.group(1) if m else fn
        if re.search(r'\.E2_combine\(', code) and not ('plan=' in code and 'fallback=False' in code):
            bad.append('l.%d E2_combine' % (i + 1))
        if re.search(r'\.load_view\(', code) and not re.search(r'\.load_view\([^,()]+,\s*[^)\s]', code):
            bad.append('l.%d load_view' % (i + 1))
        if re.search(r'\.MomTableU\(', code) and 'block=' not in code:
            bad.append('l.%d MomTableU' % (i + 1))
        if fn in NFB and re.search(r'\.tab\.E2?\(', code):
            nfb += 1
            if 'fallback=False' not in code:
                bad.append('l.%d %s' % (i + 1, fn))
    return bad, nfb


with open(os.path.join(OWN, 'm3_bar_v16_1.py')) as fh:
    BARSRC = fh.read()
ncall = len(re.findall(r'\.E2_combine\(|\.load_view\(|\.MomTableU\(', '\n'.join(ln.split('#')[0] for ln in BARSRC.split('\n'))))
cbad, nfb = caller_scan(BARSRC)
gate('C-CALLER', ncall >= 3 and nfb == 6 and not cbad, '(m3_bar_v16_1: %d kernel calls, %d layer calls in %s with fallback=False, 6 wanted)%s' % (
    ncall, nfb, '/'.join(NFB), (': ' + ', '.join(cbad)) if cbad else ''))
cmut = BARSRC.replace('E2_combine(parts, plan=plan, fallback=False)', 'E2_combine(parts, fallback=False)', 1)
plant('PLANT-CALLER', cmut != BARSRC and bool(caller_scan(cmut)[0]), '(m3_bar_v16_1 with one E2_combine call\'s plan= removed)')
fmut = BARSRC.replace('return self.tab.E(P.power(p), fallback=False)', 'return self.tab.E(P.power(p))', 1)
plant('PLANT-CALLER-FLAG', fmut != BARSRC and bool(caller_scan(fmut)[0]), '(m3_bar_v16_1 with pos_ma\'s fallback=False dropped)')
SER_RE = re.compile(r'[A-Za-z0-9]' + '_series' + r'\s*\(')
ser_hits = []
for p_ in [os.path.join(OWN, f) for f in OWNMOD] + [os.path.join(C2B, f) for f in KFILES] + [os.path.abspath(__file__)]:
    with open(p_) as fh:
        ser_hits += ['%s:%d' % (os.path.basename(p_), i + 1) for i, ln in enumerate(fh) if SER_RE.search(ln)]
for f_ in PARTS:
    ser_hits += ['%s:%d' % (f_, i + 1) for i, ln in enumerate(PSRC[f_].decode('utf-8').split('\n')) if SER_RE.search(ln)]
gate('C-SERIES', not ser_hits, '(no *_series( call in %d modules, the kernel files, this script and its %d parts)%s' % (
    len(OWNMOD), len(PARTS), (': ' + ', '.join(ser_hits)) if ser_hits else ''))
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
    """as m3_run_v1_10_4 l.373-402: C-FALLBACK-PATH and PLANT-FALLBACK-ONLY."""
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
    out('FALLBACKS %d (MAFallback recomputes in arb, INFO)%s' % (len(BAR.FALLBACKS), (': ' + '; '.join(BAR.FALLBACKS[:20])) if BAR.FALLBACKS else ''))
    return list(BAR.FALLBACKS)


fallback_tests()
T_REF = Fraction(1, 300)


def read_lines(path, tag):
    with open(path) as fh:
        return [json.loads(ln[len(tag) + 1:]) for ln in fh if ln.startswith(tag + ' ')]


# ------------------------------------------------------------------ the E_semi window list, its class rules and the records
LF = 'esemi_windows_v2.json'
with open(os.path.join(LISTD, LF)) as fh:
    LDOC = json.load(fh)
FAMS = ('ES9', 'ES12A', 'ES12B', 'ES12C')
GRAPHS = {g: {'columns': LDOC['graphs'][g]['columns'], 'pairs': LDOC['graphs'][g]['pairs'], 'K': 3, 'q_degree': 6, 'D': 10,
              'F': 3 * len(LDOC['graphs'][g]['columns']) + len(LDOC['graphs'][g]['pairs']),
              'F_ak': 3 * len(LDOC['graphs'][g]['columns']) + 5} for g in FAMS}   # F_ak: the vertex forms and at most 5 pair forms per window
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]
TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)
TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)])}
SHAPE = {'ES9': 'V9', 'ES12A': 'V12', 'ES12B': 'V12', 'ES12C': 'V12'}
VG = {'ES9': 'P9', 'ES12A': 'P12', 'ES12B': 'P12', 'ES12C': 'P12'}
SPLIT = (('ES12A', {(3, 6), (4, 5), (7, 8)}), ('ES12B', {(2, 5), (3, 6)}), ('ES12C', {(5, 8), (6, 9)}))   # t_esemi_list_v2's V 12 families
EDGES = {g: 'N' for g in FAMS}   # m3_entries_v3.factor reads the graph name only for named columns, which these lists do not use
COUNTS = {'ES9': (24, 0), 'ES12A': (24, 0), 'ES12B': (8, 0), 'ES12C': (12, 0)}
EMPTY = {'ES9': 'W1,0', 'ES12A': 'W1,0', 'ES12B': None, 'ES12C': None}   # a shape's norm twin [cp, 0, 0] alone (V 12's in ES12A)
SMOKE_KEY = {'ES9': 'W1,0', 'ES12A': 'W1,0', 'ES12B': 'x2_5,0', 'ES12C': 'x5_8,0'}   # C-SMOKE-AK's window (its first factor is p)
ZERO = {'ES9': ['W1,2'], 'ES12A': ['W1,2'], 'ES12B': [], 'ES12C': []}
ALIASES = {g: {} for g in FAMS}
QCAP0 = {g: int(GRAPHS[g]['q_degree']) for g in FAMS}
REFVG = {'P9': {4: 'm3ref_v1_10_V3E3.4.all_z9sym.out', 3: 'm3ref_v1_10_V3E3.3.all_z9sym.out'},
         'P12': {4: 'm3ref_v1_14_P16H.4.p6_z9sym.out', 3: 'm3ref_v1_14_P16H.3.p6_z9sym.out'}}   # v1_2: P12's radii are S8's D16 H prep's
VGFAM = {'P9': 'V3E3', 'P12': 'P16H'}
DMAXH = {'P9': 18, 'P12': 16}   # the entry Prep's dmaxH (P12 as m3_run_v1_9_3's entries; the stages are its Prep16's)
FOREIGN = {4: ('m3_run_v1_9_3_Hp10.4.json', 'm3_run_v1_9_3_Hp10.4.out', 'Hp10.4'),   # (hand-off, producer output, item): m3_run_v1_9_3's
           3: ('m3_run_v1_9_3_Hp14.3.json', 'm3_run_v1_9_3_Hp14.3.out', 'Hp14.3')}   # finished H prep pieces (done True)
FCOLS = ['vac', 'int', 'int', 'free']   # H's columns, the V12 shape's
RULE = (80.0, 0.6, 0.7)   # the radii sqrt(min(80 G_vv/J, 0.6)) and rho' (m3ref_v1_10's default)
PFX = {g: g for g in FAMS}
MAXP = {g: 60 for g in FAMS}
RULE_A = {g: (None, None, None) for g in FAMS}
RULE_TAB = {}   # no bonded window leaves col (C-RULE-SIZE)
TMAX = 12000000   # the largest col table a bonded key keeps (C-RULE-SIZE)
INFL_CAP = 0.10   # the per-norm inflation cap of a big-rule norm (the review 051e1a64 (c))
AKRATE = 1.8e-5   # a_k-table CPU in s per moment (m3_run_v1_10_4 NTBk1.4: u forms 0..16, D 8, caps {1: 6}, 1040820 moments, 18.0 s)
RESUME_FAMS = ('ES9',)
RESUME_KEY = {'ES9': 'x3_6x7_8,1'}
CLAIM_BALL = ('for every J >= J_REF, t = 1/J, t = 0 included: I(J)/main(J) lies in sum_k [ak_k - ak_rad_k, ak_k + ak_rad_k] t^k + '
              '[-sum Bp, sum Bp] (Lemma U: PLAN_M3_CODE_v1 l.125, v1_2 U4)')   # 
S8E3 = {4: ('m3_s8v3_E3_N4_J300_v1_8_1.json', 'm3_run_v1_8_1_asmP.4.out'), 3: ('m3_s8v3_E3_N3_J300_v1_8_1.json', 'm3_run_v1_8_1_asmP.3.out')}
S8H = {4: ('m3_s8v2_H_N4_J300_v1_9_3.json', 'm3_run_v1_9_3_asm.4.out'), 3: ('m3_s8v2_H_N3_J300_v1_9_3.json', 'm3_run_v1_9_3_asm.3.out')}
S8REF = {'E3': (S8E3, 'f', 'ES9'), 'H': (S8H, 'h', 'ES12A')}   # (records, key prefix, the family whose W1,k meet them)
S8OF = {'ES9': 'E3', 'ES12A': 'H'}   # C-SMOKE-AK's reference per family
MONO = {'D4': {'E000': '1', 'E100': 'e', 'E001': 'f', 'E101': 'ef'}, 'D4M': {'S0000': '1', 'S1000': 'e', 'S0100': 'f', 'S1100': 'ef'},
        'D3': {'1': '1', 'xi_t': 'e', 'xi_bb': 'f', 'xi_t xi_bb': 'ef'}}
RECDEF = [('D4', -1, 'V9'), ('D4M', -1, 'V9'), ('D4', 0, 'V12'), ('D4M', 0, 'V12'), ('D3', -1, 'V12'), ('D3', 0, 'V12')]
MOCK_RECS = [x[:2] for x in RECDEF]   # pk12 21:26:29Z (D4 first); 2026-11-09 00:24:40Z (D4M and D3 too)
ES_NOTE = 'raw monomial windows I(J)/main(J), no centres; the keys of one record share one vertex graph and so one main(J) (2414bd75 sect. 1)'
ORIENT = 'S8 E3 orientation: vac column 0 with [cp, k, 0], the free end last; free-left vertex 3c + r is 3(ncols - 1 - c) + r here'


def class_windows(bb_row=2):
    """the windows by t_esemi_list_v2's class rules (f5f0381b): {(family, factors json): window}; bb_row moves D3's bb bond."""
    top = lambda c: (3 * c, 3 * (c + 1))
    bot = lambda c: (3 * c + bb_row, 3 * (c + 1) + bb_row)
    mb = lambda c: (3 * c + 1, 3 * c + 2)
    cls = []
    for dl, nc in ((-1, 3), (0, 4)):
        w = 0 if dl == -1 else 1
        cls.append(('D4', dl, nc, {'E000': [], 'E100': [top(w)], 'E001': [mb(w)], 'E101': [top(w), mb(w)]}))
        cls.append(('D4M', dl, nc, {'S0000': [], 'S1000': [top(w)], 'S0100': [mb(w + 1)], 'S1100': [top(w), mb(w + 1)]}))
    for dl in (-1, 0):
        w = 0 if dl == -1 else 1
        cls.append(('D3', dl, 4, {'1': [], 'xi_t': [top(w)], 'xi_bb': [bot(w + 1)], 'xi_t xi_bb': [top(w), bot(w + 1)]}))
    wins = {}
    for c_, dl, nc, monos in cls:
        for mname, bonds in monos.items():
            for k in range(4):
                mb_ = sorted(tuple(sorted((ENT.mirror(u, nc), ENT.mirror(v, nc)))) for (u, v) in bonds)
                facs = [['cp', k, 0]] + [['xi', [u, v]] for (u, v) in mb_]
                g = 'ES9' if nc == 3 else ([f for f, s in SPLIT if set(mb_) <= s] + ['ES12?'])[0]
                w_ = wins.setdefault((g, json.dumps(facs)), {'key': ('W1' if not mb_ else ''.join('x%d_%d' % uv for uv in mb_)) + ',%d' % k,
                                                             'graph': g, 'factors': facs, 'uses': []})
                w_['uses'].append('%s d_L %d %s cp_%d' % (c_, dl, mname, k))
    return wins


V3 = [{'id': '%s:%s' % (d['graph'], d['key']), 'key': d['key'], 'graph': d['graph'], 'shape': d['shape'], 'factors': d['factors'],
       'role': 'certify', 'parity': 'free', 'uses': d['uses'], 'list_zero': d['parity_zero'], 'ak_float': None} for d in LDOC['entries']]


def parse_use(u):
    """'D3 d_L 0 xi_t xi_bb cp_2' -> ('D3', 0, 'xi_t xi_bb', 2)."""
    c_, rest = u.split(' d_L ', 1)
    dl, rest = rest.split(' ', 1)
    mname, k = rest.rsplit(' cp_', 1)
    return c_, int(dl), mname, int(k)


def rec_keys():
    """{(class, d_L): {ES,<mono>,<k>: (family, window key)}} from the list's uses; every window's shape is its record's."""
    res = {(c_, dl): {} for c_, dl, s in RECDEF}
    sof = {(c_, dl): s for c_, dl, s in RECDEF}
    for e in V3:
        for u in e['uses']:
            c_, dl, mname, k = parse_use(u)
            if sof.get((c_, dl)) != e['shape'] or SHAPE[e['graph']] != e['shape']:
                raise ValueError('use %r of %s outside its record\'s shape' % (u, e['id']))
            key = 'ES,%s,%d' % (MONO[c_][mname], k)
            if key in res[(c_, dl)]:
                raise ValueError('record %s %d: key %s twice' % (c_, dl, key))
            res[(c_, dl)][key] = (e['graph'], e['key'])
    return res


def name_of(e):
    return e['key']


def entries_of(graph, names=None):
    out_ = [e for e in V3 if e['graph'] == graph and (names is None or name_of(e) in names)]
    if names is not None and sorted(name_of(e) for e in out_) != sorted(names):
        raise ValueError('%s: keys %s, found %s' % (graph, names, [name_of(e) for e in out_]))
    return out_


def enc_of(enc):
    """a list encoding as m3_entries_v3.factor reads it (C-ENC), as m3_run_r0m_v1_1."""
    k = enc[0]
    if k == 'p' and len(enc) == 2:
        return ['pv', int(enc[1])]
    if k == 'st' and len(enc) == 3 and 1 <= int(enc[1]) <= 9:
        return ['cp', int(enc[1]), int(enc[2])]
    if k == 'xi' and len(enc) == 2 and len(enc[1]) == 2:
        return ['xia', [int(enc[1][0]), int(enc[1][1]), int(enc[1][1])]]
    if k == 'cp' and len(enc) == 3 and 0 <= int(enc[1]) <= 9:
        return ['cp', int(enc[1]), int(enc[2])]
    raise ValueError('list encoding %r' % (enc,))


def facs_of(e, ts=None):
    return [ENT.factor(TS if ts is None else ts, EDGES[e['graph']], enc_of(enc)) for enc in e['factors']]


def is_column(f):
    T, M, B = f[1]
    return M == T + 1 and B == T + 2 and T % 3 == 0


def parity_h(f):
    """as m3_run_v1_10_4 l.610-617."""
    if is_column(f):
        return ENT.parity_class(f)
    if f[0] == 'xi' and all({ENT.sigma(u), ENT.sigma(v)} == {u, v} for u, v in ENT.pairs_of(f)):
        return 'even'
    return None


def c_odd_h(graph, facs):
    """C-ODD on the family's own graph (as m3_run_v1_10_4 l.620-631, the columns from the family's list). Returns (ok, reason)."""
    V, E = GR.strip(GRAPHS[graph]['columns'])
    if not ENT.edges_map_onto(E, ENT.sigma):
        return False, 'T <-> B is not an automorphism of the couplings of %s' % graph
    cls = [parity_h(f) for f in facs]
    if any(c is None for c in cls):
        return False, 'a factor is neither exactly even nor exactly odd: %s' % cls
    if cls.count('odd') != 1:
        return False, '%d odd factors' % cls.count('odd')
    return True, 'one exactly odd factor, the rest exactly even (%s), T <-> B an automorphism of %s' % (cls, graph)


for e_ in V3:
    if c_odd_h(e_['graph'], facs_of(e_))[0]:
        e_['parity'] = 'zero'


def canon(f):
    """a factor tuple with a bond (u, v, v) written as (min, max, max), so that a mirrored bond compares equal."""
    if f[0] == 'xi' and f[1][1] == f[1][2] and not is_column(f):
        u, v = f[1][0], f[1][1]
        return (f[0], (min(u, v), max(u, v), max(u, v))) + tuple(f[2:])
    return f


def mkey(facs):
    return tuple(sorted(repr(canon(f)) for f in facs))


def alias_all(ts=None):
    """identity aliases among the certify windows (m3_run_r0b_v1_2's rule, empty key first); the list has no check keys."""
    res = {}
    for g in FAMS:
        es = entries_of(g)
        seen, res[g] = {}, {}
        for i in sorted(range(len(es)), key=lambda i: (name_of(es[i]) != EMPTY[g], i)):
            mk = mkey(facs_of(es[i], ts))
            if mk in seen:
                res[g][name_of(es[i])] = (seen[mk], 'identity')
            else:
                seen[mk] = name_of(es[i])
    return res


ALIAS = alias_all()


def use_sig(e):
    """the pair forms an entry's factors use, sorted (the family's Ej uses none, so this fixes its a_k table's forms)."""
    return tuple(sorted(set(tuple(sorted(p)) for f in facs_of(e) for p in ENT.pairs_of(f))))


def order_of(graph):
    """a family's computed keys (its aliases out) in pair-use order: by use_sig, then the most factors first, then the list's order."""
    es = [(i, e) for i, e in enumerate(entries_of(graph)) if name_of(e) not in ALIAS[graph]]
    return [name_of(e) for i, e in sorted(es, key=lambda ie: (use_sig(ie[1]), -len(ie[1]['factors']), ie[0]))]


try:
    for f_ in PARTS:   # the parts' bytes as C-HASH checked them, executed in this namespace (they only define)
        exec(compile(PSRC[f_], os.path.join(SDIR, f_), 'exec'), globals())
    if FAM == 'asm':
        run_asm()
    elif FAM == 'ESm':
        run_mock()
    elif FAM in ('P9u', 'P9c'):
        run_prep_stage('P9', FAM[-1])
    else:
        m_ = re.fullmatch(r'(%s)(a|k|r)([0-9]*)' % FAMRE, FAM)
        if m_.group(2) == 'a':
            run_smoke(m_.group(1))
        elif m_.group(2) == 'r':
            run_resume(m_.group(1), int(m_.group(3)))
        else:
            run_nk(m_.group(1), int(m_.group(3)))
    finish()
except SystemExit:
    raise
except BaseException:
    out('EXCEPTION in stage %s:' % STAGE[0])
    for ln in traceback.format_exc().rstrip().split('\n'):
        out('  ' + ln)
    out('VERDICT INVALID (EXCEPTION)')
    sys.exit(1)
