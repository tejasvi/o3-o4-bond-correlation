#!/usr/bin/env python3
"""m3_run_r0b_v1_4.py -- pk04 (code/pk04/). CONTINUATION of m3_run_r0b_v1_3.py (pk03/, 9fceb247) by the approval 2026-11-09
02:32:17Z: v1_3 allows 40 pieces per family, and W3e stopped at k40 at both N (N4 keys 0..11 done, N3 0..10). The computation is v1_3's,
unchanged. This runner and its three parts (PARTS, executed in its namespace after C-HASH has checked their bytes; m3_run_r0b_v1_4_a.py is
v1_3's lines 581-1188 byte for byte, m3_run_r0b_v1_4_b.py and m3_run_r0b_v1_4_c1.py its lines 1191-1531 and 1534-2097 with the changes
below) are the program. Changes:
- the items m3_run_r0b_v1_3 wrote (VNu, VNc, VDu, VDc, W2r1, W2r2 and every family's pieces k1..k40) are read under its names and its
  pinned sha V13_SHA (item_src; the file is pinned in INPUTS); the pieces above k40 and asm are this script's (names m3_run_r0b_v1_4,
  SELF_SHA). This script runs only W3ek41..W3ek399, walk and asm; write_handoff refuses an item of v1_3's. PLANT-SRC-NAME (a v1_3-named
  piece above k40, a v1_4-named one at k40), PLANT-SRC-SHA (a v1_3 hand-off whose header carries an unpinned sha) and PLANT-SRC-CAPPED;
- segments (SEGS, the W3e split): W3e's 40 computed keys in four disjoint segments, each with its own piece range and chain: pieces
  1..99 keys 0..14 (v1_3's k1..k40, then this script's k41..), 101..199 keys 15..19, 201..299 keys 20..23, 301..399 keys 24..39; every
  other family one segment, pieces 1..40 (v1_3's). A piece resumes where the last valid piece of its segment stopped (the key in progress
  at k40 resumes in segment 0 from k40's carried units) or at its segment's first key, stops at its segment's end key, and its hand-off
  carries the segment. C-SPLIT (disjoint piece ranges, every key in exactly one segment), PLANT-SPLIT (a key claimed by two segments
  refused), PLANT-SPLIT-GAP (by none), C-CLAIM and PLANT-CLAIM-TWICE (a key claimed by two pieces refused);
- asm walks every segment of every family (walk_seg: C-PIECES, each piece's entries exactly its keys and its segment field the segment's;
  C-CLAIM) and names both scripts in the records' engine field; the prep stages keep v1_3's names; records m3_r0b_<X>_N<N>_J300_v1.json;
- walk: the asm's walk with INFO lines where a segment is not finished (no hand-off, no record).
Arguments: ITEM LIM (5..1500). Output: stdout (pk03/out/m3_run_r0b_v1_4_<ITEM>.out); hand-offs in pk03/hand/; records in
pk03/out/. Run as run_chain_m3_run_r0b_v1_4.sh's run_item does.
"""
import resource, sys, time, math, hashlib, signal, os, json, re, traceback

FAMRE = 'W2|W3e|W3f|D4L0|D4ML0|FA'
ITEM_RE = r'(W3ek(4[1-9]|[5-9][0-9]|[1-3][0-9][0-9])|walk|asm)\.(4|3)'
if len(sys.argv) != 3 or not re.fullmatch(ITEM_RE, sys.argv[1]):
    print('usage: m3_run_r0b_v1_4.py ITEM LIM   (ITEM = W3ek41..W3ek399|walk|asm . 4|3, a W3e piece inside one of its segments SEGS; '
          'LIM = RLIMIT_CPU soft limit in s, 5..1500, above 540 only for the chain\'s long piece)')
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
C2B = CODEDIR + '/pk02'
INP = CODEDIR + '/pk10/scratch'
W4 = CODEDIR + '/pk11/out'
W4R = W4 + '/r64_v1'
W4B = W4 + '/b4c_v1'
OUTD = OWN + '/out'
HANDD = OWN + '/hand'
SDIR = CODEDIR + '/pk04'   # this runner and its parts
SNAME = 'm3_run_r0b_v1_4'   # this script's outputs and hand-offs: the pieces above k40, walk and asm
V13_NAME = 'm3_run_r0b_v1_3'   # the producer of VNu, VNc, VDu, VDc, W2r1, W2r2 and every family's pieces k1..k40 (read under its names)
V13_SHA = '73e3f46870584690e10ff75cda6f47e5963cdc1a3eeb69e5aa21c6f8cb25c460'   # pk03/m3_run_r0b_v1_3.py (in INPUTS): its hand-offs' script
V13_PIECES = 40   # its pieces per family (its ITEM_RE: k1..k40)
PARTS = {   # executed in this namespace, in this order, after C-HASH (they only define)
    'm3_run_r0b_v1_4_a.py': '644788b0ddacb4ea78aa9a8e681490bf39da4bab11ba1723ee9f493534a85c35',
    'm3_run_r0b_v1_4_b.py': '3863e8010fb886d2e078eb1219f0b69590c4f6b8426044804df0d28e4bcf38d2',
    'm3_run_r0b_v1_4_c1.py': 'd80a4fd25d6faa075efc186b6e365dc12378edce64a1b44a16cbeba4edec1a86',
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
V18_SHA = 'be0c1be3eadabf2f14f40d84f7a2482f2b75aada522b0e267146008cd700da3b'   # m3_run_v1_8.py, the producer of N's prep hand-offs (C-PREP-SAME)
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
    'm3_run_v1_8.py': V18_SHA,
}
INPUTS = {
    (W4R, 'ROUTE0B_ENTRY_LIST_v1.json'): 'e26dab2b95867801eb8b6a9dcef891af98aab6e931a6eedb77db4a59a2cfa994',
    (W4R, 'ROUTE0L0_ENTRY_LIST_v1.json'): '5b6c00afb19a69383fd669248bed8a152a8f7a1da9f75d279345beab0251849a',
    (W4B, 'D4BULK_ENTRY_LIST_v1.json'): '1e717d64c6206500897e187590a46e9cca069f0f67117153e9a635c33b62e29a',
    (C2B, 'M2B_KV_v1.txt'): '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',   # G-PHI's PIN_TRIAL tokens
    (W4, 'ts_N4_J170_D_S_z9sym_v1.json'): 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    (W4, 'ts_N3_S_z9sym_v1.json'): 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    (W4, 'vacres_K3_N4_sym_v1.json'): 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    (W4, 'vacres_K3_N3_sym_v1.json'): 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    (INP, 'm2_N4_J170.json.b'): '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    (INP, 'm2_N3_J170.json.b'): '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    (OUTD, 'm3ref_v1_10_V3N.4.all_z9sym.out'): '65a8145b6f2ce35aa3692ab3f89447aa52c4420220408f3c028ee67bf7fdf0c2',
    (OUTD, 'm3ref_v1_10_V3N.3.all_z9sym.out'): 'd12836039cc0390feed5435486459530a781cc75865f1ecf8b95f497a0421945',
    (OUTD, 'm3ref_v1_10_V3D.4.0-32_z9sym.out'): '7540647500f6c4368ad47967308b872224e08cbcaa645a1cf20acb469d9c5307',
    (OUTD, 'm3ref_v1_10_V3D.3.all_z9sym.out'): '8a045f0bb2579e91f5a937761bacf0b54af6632b6e2a5b5307d3a652af74bc9a',
    (HANDD, 'm3_run_v1_8_Nu.4.json'): 'c52047a361b4b82160d7fc2c2b52e198500db0c61040cf77bb1a3b8863219c6a',
    (HANDD, 'm3_run_v1_8_Nc.4.json'): 'a6fcc9d0436955b3573cb5150e65fd78686e9f65e9a5a1ea813a45d6ac8fd665',
    (HANDD, 'm3_run_v1_8_Nu.3.json'): 'b3b8801e4709fa8a5e56d232c2543838b276ba94c19d3c64b8b75b154d3afb23',
    (HANDD, 'm3_run_v1_8_Nc.3.json'): '26f8b56a0786d0012622ca15b7079f6a381106b6ba1f52a68cb1171ec6fabbf1',
    (OWN + '/tmp/r16', 'mock_arbeng_v1_4.py'): '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e',   # PLANT-MOCK's file
    (OWN, 'm3_run_r0b_v1_3.py'): V13_SHA,   # the producer of the items read under its names (item_src)
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


SELF_SHA = sha(os.path.abspath(__file__)); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_SELF = '8837ee03cee63988932fd90cc4c4d6b48a9bb75bebad834b7a8ca7d87d7ff7dc'; ORIG_V13 = '9fceb2477ba8c474ca0c517c94fcc21f9fe4a7b91d11071a4f0d6d076aeec5cf'; ORIG_V18 = '7d72fc7f7ae93b2ddad900ba02046ea7d66d69bcd669b3af865a6f1295140345'; ORIG_OF = {SELF_SHA: ORIG_SELF, V13_SHA: ORIG_V13}  # G-ORIG: option (C), acc2 two-producer acceptance
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
gate('C-VALREC-RUN', not rbad and nrun > 0 and nvo > 0, '(%s: %d files re-hashed against it, %d validation outputs with exactly ["VERDICT '
     'VALID"])%s' % (RUNMAN[1], nrun, nvo, (': ' + '; '.join(rbad)) if rbad else ''))
MOCK = os.path.join(OWN, 'tmp', 'r16', 'mock_arbeng_v1_4.py')
msha = sha(MOCK)
plant('PLANT-MOCK', tag_for(KERNEL + '.py', msha, [v[2] for v in VALREC]) != '' and tag_for('mock_arbeng_v1_4.py', msha, [v[2] for v in VALREC]) != '',
      '(pk03\'s mock tmp/r16/mock_arbeng_v1_4.py, sha256 %s, offered as %s.py and under its own name, must be refused the certified '
      'tag)' % (msha[:8], KERNEL))
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
gate('C-CALLER', ncall >= 3 and nfb == 6 and not cbad, '(m3_bar_v16_1: %d kernel calls; every E2_combine passes plan= and fallback=False, every '
     'load_view an expected sha256, every MomTableU block=; %d layer calls in %s, each with fallback=False, 6 wanted)%s' % (
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


# ------------------------------------------------------------------ the three lists, their families and entries
LISTS = (('ROUTE0B', W4R, 'ROUTE0B_ENTRY_LIST_v1.json', ('W2', 'W3e', 'W3f')), ('ROUTE0L0', W4R, 'ROUTE0L0_ENTRY_LIST_v1.json', ('D4L0', 'D4ML0')),
         ('D4BULK', W4B, 'D4BULK_ENTRY_LIST_v1.json', ('FA',)))
LDOC, LOF = {}, {}
for ln_, d_, f_, gs_ in LISTS:
    with open(os.path.join(d_, f_)) as fh:
        LDOC[ln_] = json.load(fh)
    for g_ in gs_:
        LOF[g_] = (ln_, d_, f_)
FAMS = ('W2', 'W3e', 'W3f', 'D4L0', 'D4ML0', 'FA')
GRAPHS = {g: LDOC[LOF[g][0]]['graphs'][g] for g in FAMS}
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]
TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)
TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)])}
VG = dict({g: 'VN' for g in FAMS}, W2='VD')   # the vertex graph whose prep serves a family
EDGES = {g: 'N' for g in FAMS}   # only for m3_entries_v3.factor's column lookup: every factor here names its column by index or triple
COUNTS = {'W2': (25, 0), 'W3e': (42, 7), 'W3f': (4, 0), 'D4L0': (12, 0), 'D4ML0': (16, 0), 'FA': (40, 0)}   # certify, check keys
EMPTY = {'W2': 'Z', 'W3e': 'Z', 'W3f': 'Z', 'D4L0': 'E000', 'D4ML0': 'S0000', 'FA': '1,0'}   # each window's empty twin (G-NORM's R)
EA_ID = 'e_a = f_a psi_u, site form (pk08 HS_UHAT_WORLD_LEMMA_NOTE_v1_1_ADD2 effefc23)'
EA = {'W2': EA_ID, 'W3e': EA_ID, 'W3f': EA_ID, 'D4L0': None, 'D4ML0': None, 'FA': None}
ZERO = {'W2': ['G,0,2', 'G,1,2', 'G,2,3', 'K1,2'], 'W3e': ['M,0,2,00', 'M,1,2,00', 'M,2,3,00'], 'W3f': [], 'D4L0': [], 'D4ML0': [],
        'FA': ['1,2', '1,5', '1,8']}   # exact parity zeros (hand test tmp/r16/t_r0b_static_v1 65a8d91e, both N); C-PARITY-SET recomputes them
ALIASES = {'W2': {'G,0,0': ('Z', 'identity'), 'K1,0': ('Z', 'identity'), 'KE,0': ('CE', 'identity'), 'V,0': ('CF', 'identity')},
           'W3e': {'M,0,0,00': ('Z', 'identity'), 'ME2': ('M,0,0,e2', 'identity'), 'ME1': ('M,0,0,e1', 'identity'),
                   'M,1,0,e2': ('M,0,1,e1', 'mirror'), 'M,2,0,e2': ('M,0,2,e1', 'mirror'), 'M,2,1,e2': ('M,1,2,e1', 'mirror'),
                   'M,3,0,e2': ('M,0,3,e1', 'mirror'), 'M,3,1,e2': ('M,1,3,e1', 'mirror'), 'M,3,2,e2': ('M,2,3,e1', 'mirror')},
           'W3f': {}, 'D4L0': {}, 'D4ML0': {}, 'FA': {}}   # the hand test's aliases (the mirror check keys stay aliases)
MIRRORS = {'W3e': {'M,1,0,e2': 'M,0,1,e1', 'M,2,0,e2': 'M,0,2,e1', 'M,2,1,e2': 'M,1,2,e1', 'M,3,0,e2': 'M,0,3,e1', 'M,3,1,e2': 'M,1,3,e1',
                   'M,3,2,e2': 'M,2,3,e1', 'ME1': 'ME2'}}   # the lists' check keys and the certify keys they mirror (C-SYM-MAP, C-SYM)
RULE_TAB = {}
for tok_ in ('W2:V,1:colh W2:V,2:colh W2:V,3:colh W3e:M,0,0,ee:colh W3e:M,0,1,e1:colh W3e:M,0,1,ee:colh W3e:M,0,2,e1:colh W3e:M,0,2,ee:colh '
             'W3e:M,0,3,e1:colh W3e:M,0,3,ee:colh W3e:M,1,1,e1:colh W3e:M,1,1,ee:colh W3e:M,1,2,e1:colh W3e:M,1,2,ee:colh W3e:M,1,3,e1:colh '
             'W3e:M,1,3,ee:colh W3e:M,2,2,e1:colh W3e:M,2,2,ee:colh W3e:M,2,3,e1:colh W3e:M,2,3,ee:colh W3e:M,3,3,e1:colh W3e:M,3,3,ee:colh '
             'W3f:FF:colh D4L0:E011:colb D4L0:E012:colb D4L0:E110:colh D4L0:E111:colh D4L0:E112:colh D4ML0:S0011:colh D4ML0:S0111:colh '
             'D4ML0:S1010:colh D4ML0:S1011:colh D4ML0:S1110:colh D4ML0:S1111:colh').split():
    g_, k_, r_ = tok_.split(':')
    RULE_TAB.setdefault(g_, {})[k_] = r_   # the 34 bonded keys off col (tmp/r16/rule_tab_v1_3.txt 0e139589)
TMAX = 12000000   # the largest col table a bonded key keeps (C-RULE-SIZE)
QCAP0 = {g: int(GRAPHS[g]['q_degree']) for g in FAMS}   # the lists' pair degrees: every entry's qcap is at least its family's
REFVG = {'VN': {4: 'm3ref_v1_10_V3N.4.all_z9sym.out', 3: 'm3ref_v1_10_V3N.3.all_z9sym.out'},
         'VD': {4: 'm3ref_v1_10_V3D.4.0-32_z9sym.out', 3: 'm3ref_v1_10_V3D.3.all_z9sym.out'}}   # the prep's radii, rho'^2 and theta0
VGFAM = {'VN': 'V3N', 'VD': 'V3D'}
RULE = (80.0, 0.6, 0.7)   # the float references' radii sqrt(min(80 G_vv/J, 0.6)) and rho' (m3ref_v1_10's default for V3N and V3D)
PFX = {g: g for g in FAMS}   # item prefixes of the families' pieces
SEGS = {g: ((1, V13_PIECES, 0, None),) for g in FAMS}   # per family its segments (first piece, last piece, first key, end key; None: the key count)
SEGS['W3e'] = ((1, 99, 0, 15), (101, 199, 15, 20), (201, 299, 20, 24), (301, 399, 24, 40))   # W3e in four chains
RULE_A = {g: (None, None, None) for g in FAMS}   # no big-table rule; every imprecise norm is recomputed in arb
INFL_CAP = 0.10   # the per-norm inflation cap of a big-rule norm (the review 051e1a64 (c))
AKRATE = 1.8e-5   # a_k-table CPU in s per moment (m3_run_v1_10_4 NTBk1.4: u forms 0..16, D 8, caps {1: 6}, 1040820 moments, 18.0 s)
RESUME_FAMS = ('W2',)   # the families with the items Xr1, Xr2
RESUME_KEY = {'W2': 'V,1'}   # C-RESUME's entry
CLAIM_BALL = ('for every J >= J_REF, t = 1/J, t = 0 included: I(J)/main(J) lies in sum_k [ak_k - ak_rad_k, ak_k + ak_rad_k] t^k + '
              '[-sum Bp, sum Bp] (Lemma U: PLAN_M3_CODE_v1 l.125, v1_2 U4)')   # 
GC_NOTE = ('c-free: every entry is one coefficient of its list\'s c-polynomial (the list\'s assembly); the assembler applies the centres '
           'over its one certified means ball')
GN_NOTE = ('R = I/main of this window over its empty twin %s:%s, the same graph with the same k V columns and K steps; the assembler '
           'applies F_k (the review c72d3c3d (a))')
V3 = []
for ln_, d_, f_, gs_ in LISTS:
    for id_, d in LDOC[ln_]['entries'].items():
        if d.get('graph') in gs_ and d.get('role') in ('certify', 'check'):
            V3.append({'id': id_, 'key': id_.split(':', 1)[1], 'graph': d['graph'], 'factors': d['factors'], 'role': d['role'],
                       'ak_float': d['ak_float']['N%d' % NN], 'parity': 'free'})


def name_of(e):
    return e['key']


def entries_of(graph, names=None):
    out_ = [e for e in V3 if e['graph'] == graph and (names is None or name_of(e) in names)]
    if names is not None and sorted(name_of(e) for e in out_) != sorted(names):
        raise ValueError('%s: keys %s, found %s' % (graph, names, [name_of(e) for e in out_]))
    return out_


def enc_of(enc):
    """a list encoding as m3_entries_v3.factor reads it (C-ENC): [p, c] -> [pv, c]; [st, a, c] -> [cp, a, c] with 1 <= a <= 9 (the trial
    polynomial beside p on its column, never in its place); [xi, [u, v]] -> [xia, [u, v, v]] (riglap3's bond form); [cp, a, c] as is."""
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


def mirror_map(graph):
    nc = len(GRAPHS[graph]['columns'])
    return lambda v: ENT.mirror(v, nc)


def mirror_ok(graph):
    """the left-right mirror maps the family's couplings onto themselves (tags included) and its list pairs onto its list pairs."""
    V, E = GR.strip(GRAPHS[graph]['columns'])
    fm = mirror_map(graph)
    prs = sorted(tuple(sorted(p)) for p in GRAPHS[graph]['pairs'])
    return ENT.edges_map_onto(E, fm) and sorted(tuple(sorted((fm(u), fm(v)))) for u, v in prs) == prs


def alias_all(ts=None):
    """as m3_run_r0b_v1_2 (identity aliases among certify keys, empty key first; check keys by identity, else by mirror)."""
    res = {}
    for g in FAMS:
        es = entries_of(g)
        seen, res[g] = {}, {}
        for i in sorted(range(len(es)), key=lambda i: (name_of(es[i]) != EMPTY[g], i)):
            e = es[i]
            if e['role'] != 'certify':
                continue
            mk = mkey(facs_of(e, ts))
            if mk in seen:
                res[g][name_of(e)] = (seen[mk], 'identity')
            else:
                seen[mk] = name_of(e)
        fm, msym = mirror_map(g), mirror_ok(g)
        for e in es:
            if e['role'] != 'check':
                continue
            fx = facs_of(e, ts)
            mk, img = mkey(fx), mkey([ENT.map_factor(f, fm) for f in fx])
            res[g][name_of(e)] = (seen[mk], 'identity') if mk in seen else ((seen[img], 'mirror') if msym and img in seen else (None, 'none'))
    return res


ALIAS = alias_all()


try:
    for f_ in PARTS:   # the parts' bytes as C-HASH checked them, executed in this namespace (they only define)
        exec(compile(PSRC[f_], os.path.join(SDIR, f_), 'exec'), globals())
    if FAM == 'asm':
        run_asm()
    elif FAM == 'walk':
        run_walk()
    else:
        m_ = re.fullmatch(r'(W3e)k([0-9]+)', FAM)
        run_nk(m_.group(1), int(m_.group(2)))
    finish()
except SystemExit:
    raise
except BaseException:
    out('EXCEPTION in stage %s:' % STAGE[0])
    for ln in traceback.format_exc().rstrip().split('\n'):
        out('  ' + ln)
    out('VERDICT INVALID (EXCEPTION)')
    sys.exit(1)
