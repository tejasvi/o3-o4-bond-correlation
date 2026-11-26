#!/usr/bin/env python3
"""m3_run_r0m_v1_2.py -- pk03 (code/pk03/). REVISION of m3_run_r0m_v1_1.py (df8680fc; the review 360c11e9: clear) by the decision
2026-11-08 22:03:08Z (option B): v1_1's colh keys cost about 1000 s each per N and its chains stopped at their caps. Changes:
- XB,b (b = 0..3) are exact T <-> B aliases of XT,b (alias kind 'tb'): C-TB-MAP proves I(XB,b) = I(XT,b) exactly, so the pieces compute
  XT,0..3, Z and M,1..3 only and asm copies XT,b's item to XB,b with alias_of; C-ALIAS expects these four aliases and no identity alias;
  C-SYM-TB becomes structural (the four tb aliases, C-TB-MAP passed in the item, the copies equal; PLANT-SYM-TB as before); RULE_TAB
  keeps XT,1..3 (colh) only;
- the resume test runs on M,1 (std) in place of XB,1;
- names m3_run_r0m_v1_2 (outputs, hand-offs); the record keeps the name m3_r0m_W2M_N<N>_J300_v1.json.
v1_1's changes and r0m_v1's design are in those files' docstrings. Arguments: ITEM LIM (5..1500). Output: stdout
(out/m3_run_r0m_v1_2_<ITEM>.out); hand-offs in hand/; records in out/ (m3_r0m_W2M_N<N>_J300_v1.json). Run as run_chain_m3_run_r0m_v1_2.sh's
run_item does.
"""
import resource, sys, time, math, hashlib, signal, os, json, re, traceback

FAMRE = 'W2M'
ITEM_RE = r'(VD[uc]|W2M(a|k([1-9]|[1-3][0-9]|40)|r[12])|asm)\.(4|3)'
if len(sys.argv) != 3 or not re.fullmatch(ITEM_RE, sys.argv[1]):
    print('usage: m3_run_r0m_v1_2.py ITEM LIM   (ITEM = VDu|VDc|W2Ma|W2Mk1..W2Mk40|W2Mr1|W2Mr2|asm . 4|3; LIM = RLIMIT_CPU soft limit in s, '
          '5..1500, above 540 only for the chain\'s long piece)')
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
OUTD = OWN + '/out'
HANDD = OWN + '/hand'
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
INPUTS = {
    (W4R, 'ROUTE0B_ENTRY_LIST_v1.json'): 'e26dab2b95867801eb8b6a9dcef891af98aab6e931a6eedb77db4a59a2cfa994',
    (C2B, 'M2B_KV_v1.txt'): '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',   # G-PHI's PIN_TRIAL tokens
    (W4, 'ts_N4_J170_D_S_z9sym_v1.json'): 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    (W4, 'ts_N3_S_z9sym_v1.json'): 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    (W4, 'vacres_K3_N4_sym_v1.json'): 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    (W4, 'vacres_K3_N3_sym_v1.json'): 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    (INP, 'm2_N4_J170.json.b'): '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    (INP, 'm2_N3_J170.json.b'): '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    (OUTD, 'm3ref_v1_10_V3D.4.0-32_z9sym.out'): '7540647500f6c4368ad47967308b872224e08cbcaa645a1cf20acb469d9c5307',
    (OUTD, 'm3ref_v1_10_V3D.3.all_z9sym.out'): '8a045f0bb2579e91f5a937761bacf0b54af6632b6e2a5b5307d3a652af74bc9a',
    (OWN + '/tmp/r16', 'mock_arbeng_v1_4.py'): '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e',   # PLANT-MOCK's file
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


SELF_SHA = sha(os.path.abspath(__file__))
out('m3_run_r0m_v1_2 item %s LIM %d; script sha256 %s; python %s' % (ITEM, LIM, SELF_SHA, sys.version.split()[0]))
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


# ------------------------------------------------------------------ W2's list and the twelve mirror windows built from it
with open(os.path.join(W4R, 'ROUTE0B_ENTRY_LIST_v1.json')) as fh:
    LDOC = json.load(fh)
LF = 'ROUTE0B_ENTRY_LIST_v1.json'
FAMS = ('W2M',)
GRAPHS = {'W2M': LDOC['graphs']['W2']}
W2KEYS = [(id_.split(':', 1)[1], d) for id_, d in LDOC['entries'].items() if d.get('graph') == 'W2' and d.get('role') == 'certify']
W2SKIP = ('K1,2',)   # W2's parity zero off the G keys (hand test tmp/r16/t_r0b_static_v1 65a8d91e); the G keys take the k = 1 model
MIRROR_ENDS = (28, 20)   # W2's modelled ends with a rest, and its bond ends (t_mirror_plan_v1_2 e6078491)
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]
TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)
TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)])}
VG = {'W2M': 'VD'}
EDGES = {'W2M': 'N'}
COUNTS = {'W2M': (12, 0)}
EMPTY = {'W2M': 'Z'}
EA_ID = 'e_a = f_a psi_u, site form (pk08 HS_UHAT_WORLD_LEMMA_NOTE_v1_1_ADD2 effefc23)'
EA = {'W2M': EA_ID}
ZERO = {'W2M': []}
TBA = {'XB,%d' % b: ('XT,%d' % b, 'tb') for b in range(4)}   # exact T <-> B aliases (C-TB-MAP)
ALIASES = {'W2M': dict(TBA)}
QCAP0 = {'W2M': int(GRAPHS['W2M']['q_degree'])}
REFVG = {'VD': {4: 'm3ref_v1_10_V3D.4.0-32_z9sym.out', 3: 'm3ref_v1_10_V3D.3.all_z9sym.out'}}   # the prep's radii, rho'^2 and theta0
VGFAM = {'VD': 'V3D'}
RULE = (80.0, 0.6, 0.7)   # the float references' radii sqrt(min(80 G_vv/J, 0.6)) and rho' (m3ref_v1_10's default for V3N and V3D)
PFX = {'W2M': 'W2M'}
MAXP = {'W2M': 40}
RULE_A = {'W2M': (None, None, None)}
RULE_TAB = {'W2M': {k_: 'colh' for k_ in ('XT,1', 'XT,2', 'XT,3')}}   # the computed bonded windows off col (t_rule_sizes_w2m_v1 b70751e8)
TMAX = 12000000   # the largest col table a bonded key keeps (C-RULE-SIZE)
INFL_CAP = 0.10   # the per-norm inflation cap of a big-rule norm (the review 051e1a64 (c))
AKRATE = 1.8e-5   # a_k-table CPU in s per moment (m3_run_v1_10_4 NTBk1.4: u forms 0..16, D 8, caps {1: 6}, 1040820 moments, 18.0 s)
RESUME_FAMS = ('W2M',)
RESUME_KEY = {'W2M': 'M,1'}   # v1_2: a std key (v1_1: XB,1, now an alias)
CLAIM_BALL = ('for every J >= J_REF, t = 1/J, t = 0 included: I(J)/main(J) lies in sum_k [ak_k - ak_rad_k, ak_k + ak_rad_k] t^k + '
              '[-sum Bp, sum Bp] (Lemma U: PLAN_M3_CODE_v1 l.125, v1_2 U4)')   # 
GC_NOTE = ('c-free: every entry is one coefficient of its list\'s c-polynomial (the list\'s assembly); the assembler applies the centres '
           'over its one certified means ball')
GN_NOTE = ('R = I/main of this window over its empty twin %s:%s, the same graph with the same k V columns and K steps; the assembler '
           'applies F_k (the review c72d3c3d (a))')
MIRROR_NOTE = ('W[mirror] of a W2 key\'s end: the end\'s rest (its factors off the end column) on both columns; W_xi[mirror]: the same with xi '
               'on the end bond\'s row edge (r, 3 + r) between the two columns (route R rest factor m_c W[mirror] - W_xi[mirror]); W2\'s G keys '
               'and K1,2 left out')


def cols_of(x):
    return {int(x[-1])} if x[0] in ('p', 'st', 'cp') else {int(x[1][0]) // 3, int(x[1][1]) // 3}


def mirror_rest(factors, end):
    """a W2 key's rest at end column `end`: its factors off that column (p and at most one st, on the other column), and the rows of its
    horizontal bonds at the end's K step (at most one)."""
    bonds, rest = [], []
    for x in factors:
        cs = cols_of(x)
        if end in cs:
            if x[0] == 'xi' and len(cs) == 2:
                bonds.append(int(x[1][0]) % 3)
            continue
        rest.append(x)
    if sorted(x[0] for x in rest) not in (['p'], ['p', 'st']) or any(int(x[-1]) != 1 - end for x in rest) or len(bonds) > 1:
        raise ValueError('mirror rule: rest %r, bonds %r at end %d' % (rest, bonds, end))
    return rest, bonds


def mirror_windows():
    """{name: (encodings, sources)} by MIRROR_NOTE's rule over W2KEYS (off the G keys and W2SKIP) and each end column carrying p:
    Z = [p0, p1], M,b = [p0, st_b 0, p1, st_b 1], XT,b / XB,b = Z or M,b with xi (0, 3) / (2, 5)."""
    win = {}
    for key, d in W2KEYS:
        if key.startswith('G,') or key in W2SKIP:
            continue
        for end in (0, 1):
            if ['p', end] not in d['factors']:
                continue
            rest, bonds = mirror_rest(d['factors'], end)
            b = ([int(x[1]) for x in rest if x[0] == 'st'] or [0])[0]
            base = [['p', 0]] + ([['st', b, 0]] if b else []) + [['p', 1]] + ([['st', b, 1]] if b else [])
            for row in [None] + bonds:
                name = ('M,%d' % b if b else 'Z') if row is None else 'X%s,%d' % ('TMB'[row], b)
                encs = base if row is None else base + [['xi', [row, 3 + row]]]
                w = win.setdefault(name, (encs, []))
                if w[0] != encs:
                    raise ValueError('mirror rule: %s built with two factor lists' % name)
                w[1].append('W2:%s/e%d' % (key, end))
    return win


def enc_key(encs):
    return tuple(sorted(json.dumps(x if x[0] != 'xi' else ['xi', sorted(x[1])]) for x in encs))


WIN = mirror_windows()
W2BY = {}
for key_, d_ in W2KEYS:
    W2BY.setdefault(enc_key(d_['factors']), []).append(key_)
REF = {}
for name_, (encs_, srcs_) in WIN.items():
    hits = W2BY.get(enc_key(encs_), [])
    if hits:
        REF[name_] = name_ if name_ in hits else hits[0]
V3 = [{'id': 'W2M:' + n, 'key': n, 'graph': 'W2M', 'factors': encs, 'role': 'certify', 'srcs': srcs, 'parity': 'free',
       'ak_float': dict(W2KEYS)[REF[n]]['ak_float']['N%d' % NN] if n in REF else None} for n, (encs, srcs) in WIN.items()]


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
    """as m3_run_r0b_v1_2 (identity aliases among certify keys; check keys by identity or mirror)."""
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


IDENT = alias_all()   # identity aliases (none among the twelve windows)
ALIAS = {g: dict(IDENT[g], **(TBA if g == 'W2M' else {})) for g in FAMS}   # v1_2: plus the four T <-> B aliases
TBOK = [False]   # set by tb_map_check when C-TB-MAP passes in this item


def use_sig(e):
    """the pair forms an entry's factors use, sorted (the family's Ej uses none, so this fixes its a_k table's forms)."""
    return tuple(sorted(set(tuple(sorted(p)) for f in facs_of(e) for p in ENT.pairs_of(f))))


def order_of(graph):
    """a family's computed keys (its aliases out) in pair-use order: by use_sig, then the most factors first, then the list's order."""
    es = [(i, e) for i, e in enumerate(entries_of(graph)) if name_of(e) not in ALIAS[graph]]
    return [name_of(e) for i, e in sorted(es, key=lambda ie: (use_sig(ie[1]), -len(ie[1]['factors']), ie[0]))]


def list_check():
    """C-LIST: 12 certify windows, ids 'W2M:key', the empty key Z, K 3. C-MIRROR: every window invariant under the column swap; the
    sources cover W2's modelled ends exactly (MIRROR_ENDS: 28, 20 at a bond), each source's rest on column 0 equal to its window's column-0
    factors and its bond row equal to the window's junction row; the windows equal to a W2 key are exactly Z, XT,0 and XB,0 (W2's Z, CE,
    CF), and only those carry a list float. PLANT-LIST: W2M without its first key; PLANT-MIRROR: M,1 without st_1 on column 1."""
    es = entries_of('W2M')
    ok = (len(es) == COUNTS['W2M'][0] and all(e['role'] == 'certify' and e['id'] == 'W2M:' + name_of(e) for e in es)
          and any(name_of(e) == EMPTY['W2M'] for e in es) and GRAPHS['W2M'].get('K') == 3)
    gate('C-LIST', ok, '(W2M: %d windows from ROUTE0B 55dfd958\'s W2 keys: %s)' % (len(es), [name_of(e) for e in es]))
    plant('PLANT-LIST', len(es[1:]) != COUNTS['W2M'][0], '(W2M without its first key)')
    fm, bad, nw, nx = mirror_map('W2M'), [], 0, 0
    for e in es:
        fx = facs_of(e)
        if mkey([ENT.map_factor(f, fm) for f in fx]) != mkey(fx):
            bad.append('%s swap' % name_of(e))
        jb = [x for x in e['factors'] if x[0] == 'xi']
        half = sorted(json.dumps(x) for x in e['factors'] if x[0] != 'xi' and int(x[-1]) == 0)
        for s in e['srcs']:
            key, end = s[3:].rsplit('/e', 1)
            rest, bonds = mirror_rest(dict(W2KEYS)[key]['factors'], int(end))
            if sorted(json.dumps(x[:-1] + [0]) for x in rest) != half or (jb and bonds != [int(jb[0][1][0]) % 3]):
                bad.append('%s source %s' % (name_of(e), s))
        nw += 0 if jb else len(e['srcs'])
        nx += len(e['srcs']) if jb else 0
    refs = sorted((n, r) for n, r in REF.items())
    okr = refs == [('XB,0', 'CF'), ('XT,0', 'CE'), ('Z', 'Z')] and all((e['ak_float'] is not None) == (name_of(e) in REF) for e in es)
    gate('C-MIRROR', not bad and (nw, nx) == MIRROR_ENDS and okr, '(every window swap-invariant, each source\'s rest and bond row match: '
         'failing %s; ends %d, bond ends %d (%d, %d wanted); W2 keys equal to a window: %s)' % (bad or 'none', nw, nx, MIRROR_ENDS[0],
                                                                                          MIRROR_ENDS[1], refs))
    e2 = dict(entries_of('W2M', ['M,1'])[0])
    e2['factors'] = [x for x in e2['factors'] if x != ['st', 1, 1]]
    fx2 = facs_of(e2)
    plant('PLANT-MIRROR', mkey([ENT.map_factor(f, fm) for f in fx2]) != mkey(fx2), '(M,1 without st_1 on column 1 must not be swap-invariant)')


def beside_p(e):
    """every st factor of the entry sits beside a p factor on its column (the list's convention: st multiplies p, never replaces it)."""
    return all(any(y[0] == 'p' and int(y[1]) == int(x[2]) for y in e['factors']) for x in e['factors'] if x[0] == 'st')


def enc_check():
    """as m3_run_r0b_v1_2 (C-ENC); PLANT-ENC: [st, 0, 0] must raise, and M,1 without its [p, 0] must fail beside_p."""
    e1 = [1.0] + [0.0] * 8
    pv = lambda c: ('p', (3 * c, 3 * c + 1, 3 * c + 2), list(TS.q[0]), list(TS.q[1]), list(TS.q[2]))
    got = [ENT.factor(TS, 'N', enc_of(x)) for x in (['st', 1, 0], ['p', 2], ['xi', [0, 3]], ['cp', 0, 0])]
    want = [('xi', (0, 1, 2), float(TS.S[0][1]), [float(TS.S[r][1]) for r in range(1, 10)]), pv(2), ('xi', (0, 3, 3), 0.0, e1), pv(0)]
    outp = []
    for e in V3:
        prs = set(tuple(sorted(p)) for p in GRAPHS[e['graph']]['pairs'])
        for f in facs_of(e):
            outp += ['%s %s' % (e['id'], p) for p in ENT.pairs_of(f) if tuple(sorted(p)) not in prs]
    bes = all(beside_p(e) for e in V3)
    gate('C-ENC', got == want and bes and not outp, '(the four sample encodings give the conventions\' tuples: %s; every st beside p: %s; pair '
         'forms outside the list pairs: %s)' % (got == want, bes, outp[:5] or 'none'))
    try:
        enc_of(['st', 0, 0])
        r0 = False
    except ValueError:
        r0 = True
    e2 = dict(entries_of('W2M', ['M,1'])[0])
    e2['factors'] = [x for x in e2['factors'] if x != ['p', 0]]
    plant('PLANT-ENC', r0 and not beside_p(e2), '([st, 0, 0] refused: %s; M,1 without [p, 0]: beside_p %s)' % (r0, beside_p(e2)))


def parity_set():
    """C-PARITY-SET: no window passes c_odd_h (ZERO is empty) and none is marked 'zero'. PLANT-ODD: [st_2 0, p0, p1] on the W2M graph
    passes c_odd_h, and with S[1][2] + 1e-12 (st_2 no longer exactly odd) it must fail."""
    import copy
    got = {g: sorted(name_of(e) for e in entries_of(g) if c_odd_h(g, facs_of(e))[0]) for g in FAMS}
    marked = {g: sorted(name_of(e) for e in entries_of(g) if e['parity'] == 'zero') for g in FAMS}
    gate('C-PARITY-SET', all(got[g] == sorted(ZERO[g]) == marked[g] for g in FAMS), '(windows passing C-ODD: %s; marked zero: %s)' % (got, marked))
    ts2 = copy.deepcopy(TS)
    ts2.S[1][2] = ts2.S[1][2] + 1e-12
    e = {'graph': 'W2M', 'factors': [['st', 2, 0], ['p', 0], ['p', 1]]}
    ok1, _ = c_odd_h('W2M', facs_of(e))
    ok2, why = c_odd_h('W2M', facs_of(e, ts2))
    plant('PLANT-ODD', ok1 and not ok2, '([st_2 0, p0, p1]: passes %s; with S[1][2] + 1e-12: %s)' % (ok1, why))


def alias_check():
    """C-ALIAS: alias_all finds no identity alias among the twelve windows, and ALIAS holds exactly the four T <-> B aliases XB,b -> XT,b
    (ALIASES; C-TB-MAP proves them). PLANT-ALIAS: XT,0 with its bond moved to (2, 5) has XB,0's multiset, and XT,0 itself does not."""
    ok = all(IDENT[g] == {} for g in FAMS) and ALIAS == ALIASES
    gate('C-ALIAS', ok, '(identity aliases recomputed from the factor tuples: none; the T <-> B aliases %s: %s)' % (sorted(TBA.items()), ok))
    e = dict(entries_of('W2M', ['XT,0'])[0])
    e2 = dict(e, factors=[['xi', [2, 5]] if x == ['xi', [0, 3]] else x for x in e['factors']])
    xb = mkey(facs_of(entries_of('W2M', ['XB,0'])[0]))
    plant('PLANT-ALIAS', mkey(facs_of(e2)) == xb and mkey(facs_of(e)) != xb, '(XT,0 with its bond moved to (2, 5) matches XB,0; XT,0 itself '
          'must not)')


def tb_even(facs):
    """every column factor exactly even or odd under T <-> B, with an even number of odd ones."""
    cls = [ENT.parity_class(f) for f in facs if is_column(f)]
    return all(c in ('even', 'odd') for c in cls) and cls.count('odd') % 2 == 0


def tb_map_check():
    """C-TB-MAP: T <-> B maps the W2M couplings onto themselves; for b = 0..3, XB,b's factors are XT,b's with the junction bond (0, 3)
    moved to its image (2, 5), and every column factor is exactly even or odd with an even number of odd ones, so I(XB,b) = I(XT,b)
    exactly: v1_2 makes XB,b an alias of XT,b on this gate (TBOK). PLANT-TB-MAP: XT,2 with S[1][2] + 1e-12 must fail the exact parity test."""
    import copy
    V, E = GR.strip(GRAPHS['W2M']['columns'])
    bad = [] if ENT.edges_map_onto(E, ENT.sigma) else ['couplings']
    for b in range(4):
        t, u = entries_of('W2M', ['XT,%d' % b])[0], entries_of('W2M', ['XB,%d' % b])[0]
        if (['xi', [0, 3]] not in t['factors'] or ['xi', [2, 5]] not in u['factors']
                or [x for x in t['factors'] if x != ['xi', [0, 3]]] != [x for x in u['factors'] if x != ['xi', [2, 5]]]):
            bad.append('XT,%d / XB,%d factors' % (b, b))
        if not tb_even(facs_of(t)):
            bad.append('XT,%d parity' % b)
    gate('C-TB-MAP', not bad, '(T <-> B on the W2M couplings, XT,b / XB,b factors and exact column parities, b = 0..3: failing %s)' % (bad or 'none'))
    TBOK[0] = not bad
    ts2 = copy.deepcopy(TS)
    ts2.S[1][2] = ts2.S[1][2] + 1e-12
    plant('PLANT-TB-MAP', not tb_even(facs_of(entries_of('W2M', ['XT,2'])[0], ts2)), '(XT,2 with S[1][2] + 1e-12: st_2 no longer exactly odd)')


def rule_of(e):
    """the partition rule (as m3_run_r0b_v1_3): std without a bond; with one, RULE_TAB's colh for its three
    computed windows, else col."""
    if not any(x[0] == 'xi' for x in e['factors']):
        return 'std'
    return RULE_TAB.get(e['graph'], {}).get(name_of(e), 'col')


RULES = ('std', 'col', 'colb', 'colh', 'colxh')


def rule_of_check():
    """C-RULE-OF: the computed keys take std exactly when they have no bond, and every RULE_TAB key is a bonded computed key of its family;
    PLANT-RULE-OF: Z with [xi, [0, 3]] added must take a bonded rule, and Z itself std."""
    ks = [entries_of(g, [k])[0] for g in FAMS for k in order_of(g)]
    vals = [rule_of(e) for e in ks]
    comp = {(e['graph'], name_of(e)) for e in ks if any(x[0] == 'xi' for x in e['factors'])}
    tab = [(g, k) for g in RULE_TAB for k in RULE_TAB[g]]
    ok = (set(vals) <= set(RULES) and all((v == 'std') == (not any(x[0] == 'xi' for x in e['factors'])) for v, e in zip(vals, ks))
          and all(t in comp for t in tab))
    gate('C-RULE-OF', ok, '(%d computed keys: std %d, col %d, colh %d, colb %d; RULE_TAB keys %d, all bonded computed keys: %s)' % (
        len(ks), vals.count('std'), vals.count('col'), vals.count('colh'), vals.count('colb'), len(tab), all(t in comp for t in tab)))
    z = dict(entries_of('W2M', ['Z'])[0])
    z2 = dict(z, factors=z['factors'] + [['xi', [0, 3]]])
    plant('PLANT-RULE-OF', rule_of(z2) != 'std' and rule_of(z) == 'std', '(Z with [xi, [0, 3]] added: %s; Z: %s)' % (rule_of(z2), rule_of(z)))


def size_choice(pr, facs):
    """the size criterion behind RULE_TAB: declare_big's largest table under col, colh and colb; col when col's is <= TMAX, else colh at
    G <= 3 and <= TMAX, else colb likewise, else colh. Returns (rule, {rule: (G, largest)})."""
    res = {}
    for r in ('col', 'colh', 'colb'):
        scal, idx = part_idx(r, facs)
        rows = pr.declare_big([[facs[i] for i in gp] for gp in idx], scal, None, None, None)
        res[r] = (len(idx), max(x[3] for x in rows))
    if res['col'][1] <= TMAX:
        return 'col', res
    for r in ('colh', 'colb'):
        if res[r][0] <= 3 and res[r][1] <= TMAX:
            return r, res
    return 'colh', res


def rule_size_check(graph, pr):
    """C-RULE-SIZE: for every bonded computed key of the family, size_choice equals rule_of. PLANT-RULE-SIZE: one key moved across (a
    RULE_TAB key offered as col, or a col key as colh) must disagree with size_choice."""
    bad, ch = [], {}
    for k in order_of(graph):
        e = entries_of(graph, [k])[0]
        if not any(x[0] == 'xi' for x in e['factors']):
            continue
        facs = facs_of(e)
        pr.qcap = qcap_of(pr, partition_of(e, facs), graph)[0]
        ch[k] = size_choice(pr, facs)
        if ch[k][0] != rule_of(e):
            bad.append('%s (size %s %s, pinned %s)' % (k, ch[k][0], ch[k][1], rule_of(e)))
    gate('C-RULE-SIZE', bool(ch) and not bad, '(%s: %d bonded computed keys, the size choice (col if its largest table <= %d moments, else colh '
         'or colb at G <= 3, else colh) equals RULE_TAB; failing %s)' % (graph, len(ch), TMAX, bad or 'none'))
    k = next((k for k in ch if rule_of(entries_of(graph, [k])[0]) != 'col'), next(iter(ch), None))
    moved = 'col' if k is not None and rule_of(entries_of(graph, [k])[0]) != 'col' else 'colh'
    plant('PLANT-RULE-SIZE', k is not None and ch[k][0] != moved, '(%s: %s moved to %s must disagree with its size choice %s)' % (
        graph, k, moved, ch[k][0] if k is not None else '-'))


def ab_ident(a, b):
    """C-AB's test: idok, (6a - 3)^2 holds 21 and (12b + 6a - 3)^2 holds 45, widths below 1e-15; sg, the lower ends of 6a - 3, 12b + 6a - 3,
    a and b above 0. Returns (idok and all(sg), idok, (6a - 3)^2, (12b + 6a - 3)^2, sg)."""
    u, w = 6 * a - 3, 12 * b + 6 * a - 3
    x, y = u ** 2, w ** 2
    idok = S.down(x) <= 21 <= S.up(x) and S.down(y) <= 45 <= S.up(y) and float(x.delta) < 1e-15 and float(y.delta) < 1e-15
    sg = (S.down(u) > 0, S.down(w) > 0, S.down(a) > 0, S.down(b) > 0)
    return idok and all(sg), idok, x, y, sg


def ab_check(graph):
    """as m3_run_r0b_v1_2 (C-AB, PLANT-AB, PLANT-AB-ROOT-A, PLANT-AB-ROOT-B)."""
    V, E = GR.strip(GRAPHS[graph]['columns'])
    tags = dict(((min(u, v), max(u, v)), t) for (u, v), t in E)
    vac = [c for c, ty in enumerate(GRAPHS[graph]['columns']) if ty == 'vac']
    okt = bool(vac) and all(tags.get((3 * c, 3 * c + 1)) == 'A' and tags.get((3 * c + 1, 3 * c + 2)) == 'A' and tags.get((3 * c, 3 * c + 2)) == 'B'
                            for c in vac)
    a, b = GR.coupling('A'), GR.coupling('B')
    ok, idok, x, y, sg = ab_ident(a, b)
    gate('C-AB', okt and ok, '(%s: vac columns %s tagged A, A, B: %s; (6A - 3)^2 in [%r, %r], (12B + 6A - 3)^2 in [%r, %r], widths %.1e, %.1e: '
         'identities %s; A in [%r, %r], B in [%r, %r]; 6A - 3 > 0, 12B + 6A - 3 > 0, A > 0, B > 0: %s)' % (
             graph, vac, okt, S.down(x), S.up(x), S.down(y), S.up(y), float(x.delta), float(y.delta), idok, S.down(a), S.up(a), S.down(b),
             S.up(b), sg))
    p1 = not ab_ident(GR.coupling(1), b)[0]
    plant('PLANT-AB', p1, '(coupling 1 in place of A: refused %s)' % p1)
    ra = ab_ident((3 - iv.sqrt(21)) / 6, (iv.sqrt(21) + 3 * iv.sqrt(5)) / 12)
    plant('PLANT-AB-ROOT-A', ra[1] and not ra[0], '(the other A root (3 - sqrt 21)/6 with B (sqrt 21 + 3 sqrt 5)/12: both identities hold %s; '
          'sign tests %s; refused %s)' % (ra[1], ra[4], not ra[0]))
    rb = ab_ident(a, -(3 * iv.sqrt(5) + iv.sqrt(21)) / 12)
    plant('PLANT-AB-ROOT-B', rb[1] and not rb[0], '(A right with the other B root -(3 sqrt 5 + sqrt 21)/12: both identities hold %s; sign tests '
          '%s; refused %s)' % (rb[1], rb[4], not rb[0]))


def family_graph(graph):
    """the family's GraphIV and C-GRAPH-LIST with its plant (as m3_run_v1_10_4 l.530-548, from the family's list)."""
    spec = GRAPHS[graph]
    V, E = GR.strip(spec['columns'])
    want = sorted(tuple(sorted(p)) for p in spec['pairs'])
    used = set()
    for e in entries_of(graph):
        for f in facs_of(e):
            used |= {tuple(sorted(p)) for p in ENT.pairs_of(f)}
    g = GR.GraphIV(V, E, want, NN)
    ok = V == 3 * len(spec['columns']) and g.F == spec['F'] and g.F == V + len(want) and len(set(want)) == len(want) and bool(used) and used <= set(want)
    gate('C-GRAPH-LIST', ok, '(%s: the columns %s give V %d and %d edges; the list\'s %d pairs %s, F %d (the list: %d); the entries use %d of them%s)' % (
        graph, spec['columns'], V, len(E), len(want), want, g.F, spec['F'], len(used & set(want)),
        '' if used <= set(want) else ('; NOT in the list: %s' % sorted(used - set(want)))))
    first = sorted(used)[0] if used else None
    plant('PLANT-GRAPH-LIST', first is not None and not (used <= set(want) - {first}), '(%s: the list\'s pairs without %r, a pair an entry uses)' % (graph, first))
    return g


def ref_prep_vg(vg):
    return read_lines(os.path.join(OUTD, REFVG[vg][NN]), 'PREPJSON')[0]


def make_prep(vg, g, stages, scalars=None):
    """as m3_run_v1_10_4 l.570-588: C-RULE (PLANT-RULE), the Prep, C-TILT and C-PREP-REF."""
    rp = ref_prep_vg(vg)
    mid = [(S.up(gv) + S.down(gv)) / 2 for gv in g.Gvv]
    want = [min(RULE[0] * m / 300, RULE[1]) for m in mid]
    drule = max([abs(a - w) / w for a, w in zip(rp['a_v'], want)] + [abs(rp['ap'] - RULE[2] ** 2) / RULE[2] ** 2])
    gate('C-RULE', len(want) == len(rp['a_v']) and drule <= 1e-12, '(%s: the reference radii^2 = min(%g G_vv/300, %g) and rho\'^2 = %g^2, '
         'G_vv the certified mids: max relative difference %.1e (tol 1e-12))' % (vg, RULE[0], RULE[1], RULE[2], drule))
    bad = [min(1.01 * RULE[0] * m / 300, 1.01 * RULE[1]) for m in mid]
    plant('PLANT-RULE', not (max(abs(a - w) / w for a, w in zip(rp['a_v'], bad)) <= 1e-12), '(%s: 80 and 0.6 times 1.01)' % vg)
    pr = BAR.Prep(K, g, 300, rp['a_v'], rp['ap'], rp['theta0'], 6, log=out, dmaxH=18, stages=stages, scalars=scalars)
    encl = [-iv.log(1 - S.I(a)) / (2 * S.I(a)) * (1 / S.I(300)) for a in rp['a_v']]
    gate('C-TILT', pr.ok and all(S.I(r) >= x.b for r, x in zip(pr.rates, encl)),
         '(a) %d tilt rates rounded up from their mp.iv enclosures; (b) both tilts certainly positive definite (lowest pivots %s, %s)' % (
             len(pr.rates), None if not pr.tilt_c else S.down(pr.tilt_c['low']), None if not pr.tilt_p else S.down(pr.tilt_p['low'])))
    gate('C-PREP-REF', rp['family'] == VGFAM[vg] and rp['N'] == NN and rp['J'] == 300, '(%s: %s PREPJSON of family %s, N %r, J %r)' % (
        vg, REFVG[vg][NN], rp['family'], rp['N'], rp['J']))
    return pr, rp


# ------------------------------------------------------------------ partitions per entry (R1's machinery; rules std, col, colb, colh)
def qcap_of(pr, p, graph):
    """(qcap, qmax): qmax the largest pair degree of the entry's F_i, qcap = max(the family's QCAP0, qmax)."""
    gds = [pr.gdata(gf) for gf in p['groups']]
    if not gds:
        return QCAP0[graph], 0
    Fi = pr.series_product([d['ser'] for d in gds], p['scal'], 3)
    qmax = max(BAR.qdeg(P, pr.g.V) for P in Fi)
    return max(QCAP0[graph], qmax), qmax


def ak_plan(pr, facs, grouping):
    """bound's a_k table request without a table: Dn and forms from the groups' series and the prep's Ej (m3_bar_v16_1 bound's own
    expressions, l.669-690)."""
    if grouping == 'std':
        scal, groups = BAR.group_factors(facs)
    else:
        scal, groups = grouping[1], [list(gf) for gf in grouping[2]]
    gds = [pr.gdata(gf) for gf in groups]
    Fi = pr.series_product([d['ser'] for d in gds], scal, 3)
    Dn = max(BAR.deg(Fi[i]) + BAR.deg(pr.Ej[k - i]) for k in range(4) for i in range(k + 1) if not BAR.is_zero(Fi[i]))
    use = sorted(set(sum((BAR.support(P) for P in Fi + pr.Ej), [])))
    return {'Dn': Dn, 'forms': use}


def col_key(rule, c, colt, vert):
    """a factor's group key under col, colxh, colb or colh: c its column (first vertex // 3), colt a column factor, vert a bond within c."""
    if rule == 'col':
        return (c, 0)
    if rule == 'colxh':
        return (c, 0 if colt else 1)
    if rule == 'colb':
        return (c, 0) if colt else (99, 1)
    return (c, 0) if colt or vert else (99, 1)


def part_idx(rule, facs):
    """as m3_run_v1_10_4 l.672-695 (std, col, colxh), with colb and colh (col_key)."""
    if rule == 'std':
        scal, groups = BAR.group_factors(facs)
        used, idx = set(), []
        for gf in groups:
            gi = []
            for f in gf:
                i = next(j for j in range(len(facs)) if facs[j] is f and j not in used)
                used.add(i)
                gi.append(i)
            idx.append(gi)
        return scal, idx
    if rule not in ('col', 'colxh', 'colb', 'colh'):
        raise ValueError('partition rule %r' % (rule,))
    if any(f[0] not in ('p', 'xi') for f in facs):
        raise ValueError('rule %s places only p and xi factors, not %s' % (rule, sorted(set(f[0] for f in facs))))
    grp = {}
    for i, f in enumerate(facs):
        c = f[1][0] // 3
        grp.setdefault(col_key(rule, c, is_column(f), f[1][1] // 3 == c), []).append(i)
    return 1, [grp[k] for k in sorted(grp)]


def part_enc(rule, encs):
    """C-PART-RULE's recomputation from the list's encodings alone: [p, c], [st, a, c], [cp, a, c] -> (3c, 3c + 1, 3c + 2), [xi, [u, v]] ->
    (u, v, v); std merges overlapping vertex sets in riglap4's order; col, colxh, colb and colh key by col_key. Returns the groups."""
    def trip(enc):
        if enc[0] in ('p', 'st', 'cp'):
            c = int(enc[-1])
            return (3 * c, 3 * c + 1, 3 * c + 2)
        if enc[0] == 'xi' and isinstance(enc[1], list) and len(enc[1]) == 2:
            return (int(enc[1][0]), int(enc[1][1]), int(enc[1][1]))
        raise ValueError('factor encoding %r' % (enc,))
    ts = [trip(x) for x in encs]
    if rule == 'std':
        groups = []
        for i, t in enumerate(ts):
            vs = set(t)
            hit = [gi for gi, (gv, gl) in enumerate(groups) if gv & vs]
            if not hit:
                groups.append((vs, [i]))
                continue
            gv, gl = groups[hit[0]]
            gv |= vs
            gl.append(i)
            for gi in sorted(hit[1:], reverse=True):
                gv |= groups[gi][0]
                gl.extend(groups[gi][1])
                groups.pop(gi)
        idx = [gl for gv, gl in groups]
    elif rule in ('col', 'colxh', 'colb', 'colh'):
        grp = {}
        for i, t in enumerate(ts):
            colt = t[1] == t[0] + 1 and t[2] == t[0] + 2 and t[0] % 3 == 0
            grp.setdefault(col_key(rule, t[0] // 3, colt, t[1] // 3 == t[0] // 3), []).append(i)
        idx = [grp[k] for k in sorted(grp)]
    else:
        raise ValueError('partition rule %r' % (rule,))
    return [[encs[i] for i in gp] for gp in idx]


def part_ok(idx, n):
    return bool(idx) and sorted(i for gp in idx for i in gp) == list(range(n)) and all(len(gp) > 0 for gp in idx)


def part_id(groups, facs):
    from collections import Counter
    return bool(groups) and all(len(gp) > 0 for gp in groups) and Counter(repr(f) for f in facs) == Counter(repr(f) for gp in groups for f in gp)


def partition_of(e, facs=None):
    """an entry's partition under rule_of (fields as m3_run_v1_10_4 l.753-761)."""
    facs = facs_of(e) if facs is None else facs
    rule = rule_of(e)
    scal, idx = part_idx(rule, facs)
    groups = [[facs[i] for i in gp] for gp in idx]
    return {'rule': rule, 'G': len(idx), 'idx': idx, 'groups': groups, 'enc': [[e['factors'][i] for i in gp] for gp in idx], 'scal': scal,
            'grouping': 'std' if rule == 'std' else ('partition', scal, groups)}


def part_line(name, p):
    return 'PARTITION %s rule %s: G %d: %s' % (name, p['rule'], p['G'], ' | '.join('{' + ', '.join(json.dumps(x) for x in gp) + '}' for gp in p['enc']))


def part_checks(e, facs, p):
    """the PARTITION line, C-PART-ID and C-PART-RULE (the groups against part_enc on the list's encodings) for one entry."""
    name = name_of(e)
    out(part_line(name, p))
    gate('C-PART-ID', part_ok(p['idx'], len(facs)) and part_id(p['groups'], facs) and p['G'] == len(p['groups']) == len(p['enc']),
         '(%s rule %s: the %d groups hold exactly the entry\'s %d factors as a multiset, none empty; G %d)' % (
             name, p['rule'], len(p['groups']), len(facs), p['G']))
    ind = part_enc(p['rule'], e['factors'])
    gate('C-PART-RULE', ind == p['enc'], '(%s: the groups against the rule %s recomputed from the list\'s encodings: %s)' % (
        name, p['rule'], 'equal' if ind == p['enc'] else 'DIFFERENT'))


def part_plants(graph, parts):
    """PLANT-PART-DROP, PLANT-PART-DUP and PLANT-PART-MOVE, once per item (m3_run_v1_10_4 l.783-820's generic cases)."""
    names = list(parts)
    e, facs, p = parts[names[0]]
    gd = [list(gp) for gp in p['groups']]
    gd[0] = gd[0][1:]
    plant('PLANT-PART-DROP', not part_id(gd, facs), '(%s: its first group without its first factor %s)' % (names[0], p['enc'][0][0]))
    gd = [list(gp) for gp in p['groups']]
    gd[0].append(gd[0][0])
    plant('PLANT-PART-DUP', not part_id(gd, facs), '(%s with its first factor %s doubled)' % (names[0], p['enc'][0][0]))
    name, s = next((n, gi) for n in names for gi, gp in enumerate(parts[n][2]['idx']) if parts[n][2]['G'] >= 2 and len(gp) >= 2)
    e, facs, p = parts[name]
    t = (s + 1) % p['G']
    idx2 = [list(gp) for gp in p['idx']]
    i0 = idx2[s].pop(0)
    idx2[t].append(i0)
    g2 = [[facs[i] for i in gp] for gp in idx2]
    enc2 = [[e['factors'][i] for i in gp] for gp in idx2]
    idok = part_ok(idx2, len(facs)) and part_id(g2, facs)
    plant('PLANT-PART-MOVE', idok and enc2 != part_enc(p['rule'], e['factors']), '(%s with %s moved from group %d to group %d: C-PART-ID %s, '
          'C-PART-RULE must fail)' % (name, e['factors'][i0], s, t, 'passes' if idok else 'FAILS'))


EXP_TARGET = {'ser': (Fraction(1, 2), Fraction(1, 4)), 'bar': (Fraction(1),), 'barp': (Fraction(1, 2),)}


def exp_ok(keys, G):
    """as m3_run_v1_10_4 l.826-842."""
    if G < 1:
        return False
    bp = set()
    for k in keys:
        if not k.startswith('g|'):
            continue
        _, gi, what, i, q, which = k.split('|')
        gi, q = int(gi), int(q)
        if gi >= G or what not in EXP_TARGET or q <= 0 or Fraction(G, q) not in EXP_TARGET[what]:
            return False
        if what == 'barp':
            bp.add(gi)
    return bp == set(range(G))


def exp_from(keys, G, H):
    """as m3_run_v1_10_4 l.845-854."""
    res = []
    for k in keys:
        if not k.startswith('g|'):
            res.append(k)
            continue
        _, gi, what, i, q, which = k.split('|')
        res.append('g|%s|%s|%s|%d|%s' % (gi, what, i, (int(q) // G) * H, which))
    return res


PPL = {'exp': True, 'akdrop': True}   # PLANT-PART-EXP and PLANT-AK-DROP, each once per item


def part_exp_check(name, p, keys):
    """as m3_run_v1_10_4 l.857-866: C-PART-EXP, PLANT-PART-EXP once per item."""
    G = p['G']
    gk = [k for k in keys if k.startswith('g|')]
    kinds = sorted(set((k.split('|')[2], int(k.split('|')[4])) for k in gk))
    gate('C-PART-EXP', exp_ok(keys, G), '(%s: G %d; %d group norms at (kind, exponent) %s; G x 1/q exactly 1/2, 1/4, 1 and 1/2 for ser 2G, ser '
         '4G, bar G and barp 2G, every group with its barp)' % (name, G, len(gk), kinds))
    if PPL['exp']:
        PPL['exp'] = False
        plant('PLANT-PART-EXP', not exp_ok(exp_from(keys, G, G - 1), G), '(%s: the same norms with exponents from G - 1 = %d)' % (name, G - 1))


def ak_only(pr, facs, grouping, label):
    """as m3_run_v1_10_4 l.869-881 (the a_k table may be a kept one)."""
    keep = (pr.ok, getattr(pr, 'gcache', {}), pr.ustate, pr.ubudget, pr.unit_done)
    pr.ok, pr.gcache, pr.ubudget, pr.unit_done = False, {}, None, None
    t0 = cpu()
    try:
        ak, _, info = pr.bound(facs, grouping, bars=False, entry=label)
    finally:
        pr.ok, pr.gcache, pr.ustate, pr.ubudget, pr.unit_done = keep
    return ak, info, cpu() - t0


def meets(x, y):
    return x.a <= y.b and y.a <= x.b


def ak_same(pr, name, p, ak, info, facs):
    """as m3_run_v1_10_4 l.889-901: C-AK-SAME and AK-ONLY-INFO; returns the standard a_k."""
    nt0 = len(pr.tables)
    akstd, inf2, dt = ak_only(pr, facs, 'std', name + ' (standard grouping, series only)')
    out('AK-ONLY-INFO %s: forms %s the partition run\'s, Dn %d (the partition run: %d), tables %d -> %d, %.2f s' % (
        name, 'equal to' if inf2['forms'] == info['forms'] else 'DIFFERENT from', inf2['Dn'], info['Dn'], nt0, len(pr.tables), dt))
    ov = [meets(x, y) for x, y in zip(ak, akstd)]
    w = max(abs(float(x.mid) - float(y.mid)) / max(1.0, abs(float(y.mid))) for x, y in zip(ak, akstd))
    gate('C-AK-SAME', len(ak) == len(akstd) == 4 and all(ov), '(%s rule %s: its a_k balls against the standard grouping\'s series-only a_k: '
         'overlap %s; largest mid difference / max(1, |a_k|) %.2e, INFO)' % (name, p['rule'], ov, w))
    return akstd


def ak_drop_plant(pr, e, facs, p, akstd):
    """PLANT-AK-DROP once per item (m3_run_v1_10_4 l.904-916): the partition without one xi factor, an st beside a p on its column when
    there is one (the entry's forms stay, so its kept a_k table serves), must give a_k that miss the standard a_k at some k."""
    if not PPL['akdrop']:
        return
    PPL['akdrop'] = False
    pcols = {f[1] for gp in p['groups'] for f in gp if f[0] == 'p'}
    cand = [(gi, j) for gi, gp in enumerate(p['groups']) for j, f in enumerate(gp) if f[0] == 'xi']
    gi, j = next(((gi, j) for gi, j in cand if p['groups'][gi][j][1] in pcols), cand[0])
    enc0 = p['enc'][gi][j]
    gd = [list(gp) for gp in p['groups']]
    gd[gi].pop(j)
    gd = [gp for gp in gd if gp]
    ak2, _, dt = ak_only(pr, facs, ('partition', p['scal'], gd), name_of(e) + ' (planted: %s dropped)' % enc0)
    ov = [meets(x, y) for x, y in zip(ak2, akstd)]
    plant('PLANT-AK-DROP', not all(ov), '(%s: its partition without the factor %s: overlap with the standard a_k %s; %.2f s)' % (name_of(e), enc0, ov, dt))


def gcache_ok(gc, grs, pairs):
    """as m3_run_v1_10_4 l.919-927."""
    keys = {repr(gf) for _, _, gf in grs}
    if not keys or not all(k in gc for k in keys):
        return False
    if len({id(gc[k]) for k in keys}) != len(keys):
        return False
    return all(repr(a) != repr(b) and gc[repr(a)] is not gc[repr(b)] for a, b in pairs)


def gcache_check(graph, pr, parts):
    """C-GCACHE, PLANT-GCACHE and PLANT-GCACHE-RUN (m3_run_v1_10_4 l.930-961's generic cases)."""
    gc = getattr(pr, 'gcache', {})
    grs = [(n, gi, gf) for n, (e, facs, p) in parts.items() for gi, gf in enumerate(p['groups'])]
    keys = sorted({repr(gf) for _, _, gf in grs})
    gate('C-GCACHE', gcache_ok(gc, grs, []), '(%s: %d groups of %d entries, %d distinct factor-tuple lists, each with its own entry under '
         'its repr)' % (graph, len(grs), len(parts), len(keys)))
    colkey = lambda gf: gf[0][1][0] // 3
    a = grs[0][2]
    f = a[0]
    f2 = (f[0], f[1], f[2] + 1.0, f[3]) if f[0] == 'xi' else (f[0], f[1], [x + 1e-3 for x in f[2]], f[3], f[4])
    b = [f2] + list(a[1:])
    plant('PLANT-GCACHE', colkey(a) == colkey(b) and repr(a) != repr(b), '(%s group %d and a copy with its first factor moved: one column key '
          '%r, different factor tuples)' % (grs[0][0], grs[0][1], colkey(a)))
    bad1 = dict(gc)
    bad1[keys[1]] = gc.get(keys[0])
    bad2 = {k: v for k, v in gc.items() if k != keys[0]}
    r1, r2 = gcache_ok(bad1, grs, []), gcache_ok(bad2, grs, [])
    plant('PLANT-GCACHE-RUN', not r1 and not r2, '(%s: the gate\'s test on the cache with two different tuple lists sharing one entry: %s; '
          'without one list\'s entry: %s)' % (graph, 'accepted' if r1 else 'refused', 'accepted' if r2 else 'refused'))


BARPOS_PTS = ('X = 0', 'X = 1', 'X_f = 1 + (f mod 3)', 'X_f = 0 (f even), 2 (f odd)')


def barpos_points(nv):
    return [[0] * nv, [1] * nv, [1 + f % 3 for f in range(nv)], [0 if f % 2 == 0 else 2 for f in range(nv)]]


def poly_at(items, x):
    tot = iv.mpf(0)
    for ex_, c in items:
        t = c
        for i, k in enumerate(ex_):
            if k:
                t = t * (x[i] ** k)
        tot = tot + t
    return tot


def barpos_info(graph, pr, parts):
    """as m3_run_v1_10_4 l.984-1014: C-BARPOS-INFO and PLANT-BARPOS."""
    seen, nev, flagged, nneg, ncoef, t0 = set(), 0, [], 0, 0, cpu()
    for n, (e, facs, p) in parts.items():
        if p['G'] % 2 == 0:
            continue
        for gi, gf in enumerate(p['groups']):
            if repr(gf) in seen:
                continue
            seen.add(repr(gf))
            for j, P in enumerate(pr.gdata(gf)['bar']):
                if BAR.is_zero(P):
                    continue
                items = list(S.spoly_iv(P).items())
                ncoef += len(items)
                nneg += sum(1 for ex_, c in items if c.a < 0)
                for lab, x in zip(BARPOS_PTS, barpos_points(P.nv)):
                    nev += 1
                    v = poly_at(items, x)
                    if v.b < 0:
                        flagged.append('%s group %d Fbar_%d at %s: upper end %s' % (n, gi, j, lab, v.b))
    out('C-BARPOS-INFO %s: %d distinct groups of odd-G entries, %d evaluations of Fbar_0..4 at %s; certainly negative: %s; coefficients with '
        'a negative lower end %d of %d (%.2f s)' % (graph, len(seen), nev, list(BARPOS_PTS), '; '.join(flagged[:10]) if flagged else 'none',
                                                   nneg, ncoef, cpu() - t0))
    nv = pr.g.F
    e0, e1 = [0] * nv, [0] * nv
    e0[0], e1[1] = 1, 1
    pm = list(S.spoly_iv(S.spoly(K, {tuple(e0): 1, tuple(e1): -1}, nv)).items())
    neg = [lab for lab, x in zip(BARPOS_PTS, barpos_points(nv)) if poly_at(pm, x).b < 0]
    plant('PLANT-BARPOS', bool(neg), '(X_0 - X_1 flagged at %s)' % neg)


def laws_of(pr, mF):
    """as m3_run_v1_10_4 l.1017-1024."""
    g = pr.g
    cF = mF + Fraction(g.n * (g.V - 1), 2)
    rate = pr.alpha_lo - S.I(cF) / 300
    return {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, g.Gvv)]},
            'ann': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, pr.tilt_p['Gvv'])]},
            'far_rate': S.down(rate), 'far_cF': str(cF)}, rate


def has0(ak):
    return all(a.a <= 0 <= a.b for a in ak)


def ak_total_plants():
    """as m3_run_v1_10_4 l.1032-1040: PLANT-AK-TOTAL and PLANT-AK-ZERO."""
    bad = BAR.ak_failing([iv.mpf(['0.997', '1.003']), iv.mpf(['-1e-9', '1e-9']), iv.mpf(['0.9999999', '1.0000001'])], K.FALLBACK_REL)
    plant('PLANT-AK-TOTAL', bad == [0, 1], '(ak_failing at FALLBACK_REL %g on totals of radius 3e-3 |mid|, midpoint 0 and radius 1e-7 |mid|: '
          'refused %s, [0, 1] wanted)' % (K.FALLBACK_REL, bad))
    plant('PLANT-AK-ZERO', not has0([iv.mpf(['1e-9', '2e-9'])]) and has0([iv.mpf(['-1e-9', '2e-9'])]), '(has0 on [1e-9, 2e-9] must fail and '
          'on [-1e-9, 2e-9] pass)')


def norm_rel_plants():
    for n_, f_, l_ in BAR.rule_plants(K):
        plant(n_, f_, l_)


def ak_dev(ak, fa):
    """the largest |certified a_k mid - the list's ak_float| / max(1, |ak_float|) over k = 0..3."""
    return max(abs(float(a.mid) - x) / max(1.0, abs(x)) for a, x in zip(ak, fa))


def ak_list(name, ak, fa):
    """C-AK-LIST against the coinciding W2 key's list float, or AK-LIST-INFO for a window W2's list does not hold."""
    if fa is None:
        out('AK-LIST-INFO %s: no list float (a window W2\'s list does not hold; C-TB-MAP and C-SYM-TB check the XT/XB pairs)' % name)
        return
    dv = ak_dev(ak, fa)
    gate('C-AK-LIST', dv <= 1e-9, '%s: certified a_k mids against W2 %s\'s ak_float: largest |mid - float| / max(1, |float|) %.2e (tol 1e-9)' % (
        name, REF[name], dv))


def akest_s(graph):
    """a family's a_k-table CPU estimate: AKRATE x its table at the list's F, D and q_degree (m3_bar_v16_1.table_moments)."""
    sp = GRAPHS[graph]
    return AKRATE * BAR.table_moments(int(sp['F']), int(sp['D']), 3 * len(sp['columns']), QCAP0[graph])


def compute_entry(pr, e, state=None):
    """as m3_run_r0b_v1_2, with ak_list in place of C-AK-LIST."""
    name, graph = name_of(e), e['graph']
    t0 = cpu()
    STAGE[0] = 'entry %s' % name
    facs = facs_of(e)
    p = partition_of(e, facs)
    part_checks(e, facs, p)
    tq = cpu()
    pr.qcap, qmax = qcap_of(pr, p, graph)
    dq = cpu() - tq
    if pr.unit_done is not None:
        pr.unit_done(dq, False)
    out('QCAP %s: the largest pair degree of its F_i %d; qcap %d (the list\'s q_degree %d); qcap_of %.2f s' % (name, qmax, pr.qcap, QCAP0[graph], dq))
    pf = {'rule': p['rule'], 'G': p['G'], 'groups': p['enc'], 'qcap': pr.qcap}
    pr.maxrel = 0.0
    if e['parity'] == 'zero':
        ok, why = c_odd_h(graph, facs)
        gate('C-ODD', ok, '%s: %s' % (name, why))
        ak, _, info = pr.bound(facs, p['grouping'], bars=False, entry=name, state=state, ak_zero=True)
        gate('C-ODD-AK', has0(ak), '%s: every a_k ball contains 0 (widest %.1e)' % (name, max(float((a.b - a.a).b) for a in ak)))
        ak_list(name, ak, e['ak_float'])
        out('STAGE-CPU entry %s %.2f s (parity zero)%s' % (name, cpu() - t0, resumed(state)))
        return dict({'name': name, 'parity': 'zero', 'ak': ak, 'cpu': cpu() - t0, 'forms': info['forms']}, **pf)
    rows = pr.declare_big(p['groups'], p['scal'], *RULE_A[graph])
    out('BIGRULE-SET %s: %d norms declared; the big set %s' % (name, len(rows), ['%s forms %d D %d moments %d' % r[:4] for r in rows if r[4]]))
    ak, bars, info = pr.bound(facs, p['grouping'], entry=name, state=state)
    part_exp_check(name, p, list(pr.ustate['vals']))
    if p['rule'] != 'std':
        if pr.ubudget is not None and not pr.ubudget():   # every unit is done: the next piece restores them all and starts here
            pr.ustate['maxrel'] = pr.maxrel
            raise BAR.Checkpoint(pr.ustate)
        if state is not None and 'ak' in state['vals'] and getattr(pr, 'akest', None) is not None and not pr.akest(akest_s(graph)):
            pr.ustate['maxrel'] = pr.maxrel   # ak_only builds the restored 'ak' table afresh; the next piece starts here
            raise BAR.Checkpoint(pr.ustate)
        akstd = ak_same(pr, name, p, ak, info, facs)
        ak_drop_plant(pr, e, facs, p, akstd)
    laws, rate = laws_of(pr, info['mF'])
    gate('C-MONO-FAR', rate.a > 0, '%s: far rate alpha_min - (m_F + n(V-1)/2)/J_REF = %.4e > 0 (m_F %d)' % (name, S.down(rate), info['mF']))
    a0 = 1 if all(f[0] == 'p' for f in facs) else None
    rec = REC.entry_record(ak, bars, T_REF, 'free', a0_exact=a0, laws=laws)
    barsum = rec['Bp']['rem'] + rec['Bp']['tail'] + rec['Bp']['ann'] + rec['Bp']['far']
    okb = BAR.budget_ok(pr.maxrel, rec['B']['rnd'], barsum)
    gate('C-BUDGET', okb, '%s: largest relative radius of a norm %.3e (<= NORM_REL %g; big-rule norms out), rnd %.2e <= 0.1 x bar %.3e' % (
        name, pr.maxrel, BAR.NORM_REL, rec['B']['rnd'], barsum))
    over = BAR.cap_over(info['big'], INFL_CAP)
    gate('C-BIGCAP', not over, '%s: big-rule inflations at most %g (no exemption): over %s' % (name, INFL_CAP, over))
    out('BIGRULE-INFO %s: %d norms by the big-table rule, largest inflation %s' % (name, len(info['big']), BAR.infl_str(info['big_max'])))
    ak_list(name, ak, e['ak_float'])
    out('AKRAD-INFO %s: largest relative radius of an a_k %.2e' % (name, info.get('ak_relrad', 0.0)))
    out('ENTRY %s ak %s err %.9e parts rem %.9e tail %.9e ann %.9e far %.9e rnd %.3e groups %d Dn %d forms %d' % (
        name, ['%.12g' % x for x in rec['ak']], rec['err'], rec['B']['rem'], rec['B']['tail'], rec['B']['ann'], rec['B']['far'], rec['B']['rnd'],
        info['groups'], info['Dn'], len(info['forms'])))
    out('STAGE-CPU entry %s %.2f s%s' % (name, cpu() - t0, resumed(state)))
    return dict({'name': name, 'parity': 'free', 'ak': ak, 'bars': bars, 'a0_exact': a0, 'laws': laws, 'maxrel': pr.maxrel, 'big': info['big'],
                 'cpu': cpu() - t0, 'forms': info['forms']}, **pf)


def keep_ak(pr, r):
    """after an entry: its a_k table (key ('u', forms, True, ((1, qcap),)), as m3_bar_v16_1's bound requests it) stays for the next entry
    with the same forms and qcap; every other table is dropped (memory)."""
    key = ('u', tuple(r['forms']), True, ((1, r['qcap']),))
    hit = pr.tables.get(key)
    pr.tables.clear()
    if hit is not None:
        pr.tables[key] = hit


def plant_mono(pr):
    """PLANT-MONO: with theta0 = 1e-3 the far rate must not be certainly positive."""
    g = pr.g
    alpha = min((S.I(1e-3) * S.I(pr.ap) / (2 * gv)).a for gv in g.Gvv)
    rate = alpha - S.I(Fraction(g.n * (g.V - 1), 2)) / 300
    plant('PLANT-MONO', not (rate.a > 0), '(theta0 = 1e-3: far rate %.3e)' % S.down(rate))


def header(fam):
    return {'script': SELF_SHA, 'item': ITEM, 'family': fam, 'N': NN, 'kernel': '%s:%s' % (KERNEL, KFILES[KERNEL + '.py'][:8]),
            'arb_kernel': '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), 'trial': TRIAL, 'format': 'm3_run_r0m_v1_2 hand-off'}


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
    name = 'm3_run_r0m_v1_2_%s.json' % ITEM
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
    name = 'm3_run_r0m_v1_2_%s.json' % item
    hdr, body = HO.read(name, os.path.join(OUTD, 'm3_run_r0m_v1_2_%s.out' % item), {'script': SELF_SHA, 'item': item, 'N': NN, 'family': fam},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (name, valid_verdict()))
    return body


def iv_leaves(v, lab=''):
    if isinstance(v, dict):
        return sum((iv_leaves(v[k], '%s[%s]' % (lab, k)) for k in sorted(v, key=str)), [])
    if isinstance(v, (list, tuple)):
        return sum((iv_leaves(x, '%s[%d]' % (lab, i)) for i, x in enumerate(v)), [])
    return [(lab, v)]


def prep_rep(vg, pr, rp, stg):
    """as m3_run_v1_10_4 l.1202-1218: PREP-REP (INFO)."""
    keys = {'u': ('rE', 'rE_parts', 'nE', 'nE4'), 'c': ('nC8', 'nC6', 'Pout', 'Pout_p', 'farbase')}[stg]
    rows = []
    for k in keys:
        for lab, x in iv_leaves(getattr(pr, k)):
            f = rp[k]
            for part in [p for p in re.findall(r'\[([^\]]*)\]', lab)]:
                f = f[int(part)] if isinstance(f, list) else f[part]
            if isinstance(f, (int, float)) and f > 0:
                rows.append((S.up(x) / f, k + lab))
    rows.sort()
    if not rows:
        out('PREP-REP %s stage %s: no scalar with a positive float value' % (vg, stg))
        return
    out('PREP-REP %s stage %s: %d scalars, certified upper end / float in [%.6f (%s), %.6f (%s)]; %s' % (
        vg, stg, len(rows), rows[0][0], rows[0][1], rows[-1][0], rows[-1][1], '; '.join('%s %.6f' % (lab, r) for r, lab in rows)))


def prep_graph(g):
    """as m3_run_v1_10_4 l.1221-1224: the prep graph, F = V (C-PREP-GRAPH)."""
    return GR.GraphIV(g.V, list(g.edges), [], g.N, list(g.S_gauge))


def prep_view(G, pr):
    """as m3_run_v1_10_4 l.1227-1250: what the prep reads of a graph object (inputs, C-1 values, C-4 values)."""
    V = G.V
    vb = lambda M: [list(r[:V]) for r in M[:V]]
    tl = lambda T: None if T is None else {'Gam': vb(T['Gam']), 'Gvv': list(T['Gvv']), 'N': T['N']}
    tc, tp = G.tilted(pr.rates), G.tilted(pr.ratesp)
    ins = {'V': G.V, 'N': G.N, 'S_gauge': list(G.S_gauge), 'edges': [(tuple(e), c) for e, c in G.edges]}
    c1 = {'Gam': vb(G.Gam), 'Gvv': list(G.Gvv), 'log_tau': G.log_tau, 'log_det_Lr': G.log_det_Lr, 'W_int': [list(r[:V]) for r in G.W_int],
          'tilt_c': tl(tc), 'tilt_p': tl(tp)}
    c4 = None
    if tp is not None:
        th, ap = S.I(pr.theta0), S.I(pr.ap)
        try:
            tree = G.tree()
            c4 = {'Pout': S.isum(S.chi_tail_up(pr.J * S.I(a) / gv, G.n) for a, gv in zip(pr.a_v, G.Gvv)),
                  'Pout_p': S.isum(S.chi_tail_up(pr.J * S.I(a) / gv, G.n) for a, gv in zip(pr.a_v, tp['Gvv'])),
                  'tree': tree, 'farbase': S.far_base(pr.J, th, ap, G.Gvv, tree, G.N, G.V, G.log_tau),
                  'alpha_lo': min((th * ap / (2 * gv)).a for gv in G.Gvv)}
        except (ArithmeticError, ValueError) as ex:
            c4 = 'not formed (%s)' % type(ex).__name__
    return ins, c1, c4


VIEW_PARTS = ('inputs', 'C-1 values', 'C-4 values')


def view_diff(a, b):
    return [n_ for n_, x, y in zip(VIEW_PARTS, a, b) if not same(x, y)]


def prep_same(graph, g, gp, pr):
    """as m3_run_v1_10_4 l.1261-1295: C-PREP-GRAPH and its plants PLANT-PREP-EDGE, -TAG, -GAUGE and -ULP."""
    import types
    vg, vp = prep_view(g, pr), prep_view(gp, pr)
    d0 = view_diff(vg, vp)
    formed = isinstance(vg[2], dict) and isinstance(vp[2], dict)
    ok = gp.pairs == [] and gp.F == gp.V and formed and not d0
    gate('C-PREP-GRAPH', ok, '(%s: the prep graph has V %d, F %d and pairs %r (the family graph: F %d); against the family graph, V, N, '
         'S_gauge and the %d edges with tags in order equal, and exactly (equal _mpi_ tuples) the %d x %d vertex block of Gam, %d G_vv, '
         'log_tau, log_det_Lr, W_int\'s vertex columns and tilted()\'s vertex Gam, G_vv and N at both rate vectors (C-1), and Pout, Pout_p, '
         'tree(), farbase and alpha_lo (C-4)%s%s)' % (graph, gp.V, gp.F, gp.pairs, g.F, len(g.edges), g.V, g.V, len(g.Gvv),
                                                      ('; differ: ' + ', '.join(d0)) if d0 else '',
                                                      '' if formed else '; C-4 values of the family and prep graphs: %r, %r' % (
                                                          vg[2] if not isinstance(vg[2], dict) else 'formed',
                                                          vp[2] if not isinstance(vp[2], dict) else 'formed')))
    E, S0 = list(g.edges), list(g.S_gauge)
    t1 = 'B' if E[0][1] == 'A' else 'A'
    for lab, what, gx in (('PLANT-PREP-EDGE', 'its first edge %r dropped' % (E[0],), GR.GraphIV(g.V, E[1:], [], g.N, S0)),
                          ('PLANT-PREP-TAG', 'its first edge\'s tag %r changed to %r' % (E[0][1], t1),
                           GR.GraphIV(g.V, [(E[0][0], t1)] + E[1:], [], g.N, S0)),
                          ('PLANT-PREP-GAUGE', 'S_gauge [0]', GR.GraphIV(g.V, E, [], g.N, [0]))):
        dx = view_diff(vg, prep_view(gx, pr))
        plant(lab, bool(dx), '(%s: the prep graph with %s, against the family graph: differs in %s)' % (graph, what, ', '.join(dx) or 'nothing'))
    x = vp[1]['Gam'][0][1]
    mv = types.SimpleNamespace(_mpi_=tuple(libmp.mpf_add(r, libmp.from_man_exp(1, r[2]), 0) for r in x._mpi_))
    (a0, b0), (a1, b1) = [_ef(r) for r in x._mpi_], [_ef(r) for r in mv._mpi_]
    c1m = dict(vp[1], Gam=[list(r) for r in vp[1]['Gam']])
    c1m['Gam'][0][1] = mv
    dx = view_diff(vg, (vp[0], c1m, vp[2]))
    lap = a1 <= b0 and a0 <= b1
    plant('PLANT-PREP-ULP', bool(dx) and lap, '(%s: a copy of the prep graph\'s view with its vertex-block entry [0][1] moved up by one unit '
          'of each end\'s last bit (overlapping the original: %s), against the family graph: differs in %s)' % (graph, lap, ', '.join(dx) or 'nothing'))


PACK_LIM = 9 * 10 ** 18   # the strictest table encoder: arbeng_c2b_v2's AllMom2A asserts float(D + 1)^F < 9.0e18 (the layer's _code_guard: 2^63)


def pack_ok(forms, D, lp):
    return (D + 1) ** forms < PACK_LIM and (not lp or D <= 64)


def pack_plan(pr, facs, grouping, info, bars):
    """as m3_run_v1_10_4 l.1306-1347: C-PACK-PLAN's requests for one entry, (what, forms, D, lp), from its polynomials (no table)."""
    import numpy as np
    use = info['forms']
    reqs = [('a_k', len(use), max(info['Dn'], 1), False)]
    if not bars:
        return reqs
    if isinstance(grouping, tuple) and len(grouping) == 3 and grouping[0] == 'partition':
        scal, groups = grouping[1], [list(gf) for gf in grouping[2]]
    elif grouping == 'std':
        scal, groups = BAR.group_factors(facs)
    else:
        raise ValueError('grouping %r' % (grouping,))
    G_ = max(len(groups), 1)
    gds = [pr.gdata(gf) for gf in groups]
    d0 = 2 * BAR.deg(pr.series_product([d['ser'] for d in gds], scal, 0)[0]) if groups else 0
    reqs.append(('m0u m0c', len(use), max(d0, 1), False))
    shape = {}

    def req(lab, P, p, pos):
        if id(P) not in shape:
            shape[id(P)] = (int(np.count_nonzero(P.ex.any(axis=0))), int(P.ex.sum(axis=1).max())) if len(P.ex) else (0, 0)
        nf, dq = shape[id(P)]
        r = (lab, nf, dq * p if pos else 2 * dq * (p // 2), not pos)
        if nf and r not in reqs:
            reqs.append(r)
    for i in (1, 2, 3):
        for c in BAR.comps(i, len(groups)):
            for gi, ig in enumerate(c):
                req('group %d ser %d p %d' % (gi, ig, 2 * G_), gds[gi]['ser'][ig], 2 * G_, False)
    for c in BAR.comps(0, len(groups)):
        for gi, ig in enumerate(c):
            req('group %d ser %d p %d' % (gi, ig, 4 * G_), gds[gi]['ser'][ig], 4 * G_, False)
    for c in BAR.comps(4, len(groups)):
        for gi, jg in enumerate(c):
            req('group %d bar %d p %d' % (gi, jg, G_), gds[gi]['bar'][jg], G_, True)
    for gi in range(len(gds)):
        req('group %d barp p %d' % (gi, 2 * G_), gds[gi]['barp'], 2 * G_, False)
    return reqs


def pack_gate(graph, plans):
    """as m3_run_v1_10_4 l.1350-1361: C-PACK-PLAN and PLANT-PACK-PLAN."""
    bad = [(nm, r) for nm, r in plans if not pack_ok(r[1], r[2], r[3])]
    nm, r = max(plans, key=lambda x: x[1][1] * math.log(x[1][2] + 1))
    lpm = max([x[1][2] for x in plans if x[1][3]] + [0])
    gate('C-PACK-PLAN', bool(plans) and not bad, '(%s: the bound of all %d computed keys asks the kernel for %d table requests, distinct within '
         'each key; the largest code range (D + 1)^forms is %d^%d = %.3e (%s, %s), below %.1e; the largest lp-norm D is %d (<= 64))%s' % (
             graph, len(set(x[0] for x in plans)), len(plans), r[2] + 1, r[1], float(r[2] + 1) ** r[1], nm, r[0], PACK_LIM, lpm,
             (': refused ' + '; '.join('%s %s D %d over %d forms' % (x[0], x[1][0], x[1][2], x[1][1]) for x in bad[:10])) if bad else ''))
    plant('PLANT-PACK-PLAN', not pack_ok(16, 16, False) and pack_ok(16, 14, False), '(a request of D 16 over 16 forms, 17^16 = %.3e, must '
          'be refused, and the control D 14 over 16 forms, 15^16 = %.3e, accepted)' % (17.0 ** 16, 15.0 ** 16))


def run_prep_stage(vg, stg):
    """as m3_run_r0b_v1_2 for VD alone (no VN, so no C-PREP-SAME)."""
    stage('%s prep stage %s' % (vg, stg))
    fams = [f for f in FAMS if VG[f] == vg]
    gs = {f: family_graph(f) for f in fams}
    gp = prep_graph(gs[fams[0]])
    pr, rp = make_prep(vg, gp, (stg,))
    if stg == 'u':
        for f in fams:
            prep_same(f, gs[f], gp, pr)
    prep_rep(vg, pr, rp, stg)
    body = {'vgraph': vg, 'stage': stg, 'families': fams, 'scal': pr.scalars_out(stg)}
    if stg == 'c':
        plant_mono(pr)
        out('PREP %s N=%d stage c: V %d, F %d; nC8 %.6e nC6 %.6e farbase %.6e alpha_lo %.6e' % (
            vg, NN, gp.V, gp.F, float(pr.nC8.mid), float(pr.nC6.mid), float(pr.farbase.b), float(pr.alpha_lo)))
    else:
        out('PREP %s N=%d stage u: V %d, F %d, radii from %s, theta0 %r; rE %.6e nE %s nE4 %s' % (
            vg, NN, gp.V, gp.F, REFVG[vg][NN], rp['theta0'], float(pr.rE.mid), ['%.6e' % float(x.mid) for x in pr.nE],
            ['%.6e' % float(x.mid) for x in pr.nE4]))
    body['fallbacks'] = fb_info()
    write_handoff(vg, body)


def prep_scalars(vg):
    """as m3_run_v1_10_4 l.1392-1401: C-PREP-STAGES; both stages' scalars."""
    su = read_handoff('%su.%d' % (vg, NN), vg)
    sc = read_handoff('%sc.%d' % (vg, NN), vg)
    ok = (su['vgraph'] == vg and sc['vgraph'] == vg and su['stage'] == 'u' and sc['stage'] == 'c' and set(su['scal']) == set(BAR.Prep.UK)
          and set(sc['scal']) == set(BAR.Prep.CK))
    gate('C-PREP-STAGES', ok, '(%s: %su.%d and %sc.%d, of %s and %s, scalars %s and %s)' % (vg, vg, NN, vg, NN, su['vgraph'], sc['vgraph'],
                                                                                         sorted(su['scal']), sorted(sc['scal'])))
    return dict(su['scal'], **sc['scal'])


CAPPED = 'VERDICT INCOMPLETE (CAP-STOP)'


def piece_state(graph, piece):
    """as m3_run_v1_10_4 l.1412-1429 with this script's names: 'valid', 'capped' or 'missing'; anything else raises ValueError."""
    item = '%sk%d.%d' % (PFX[graph], piece, NN)
    po = os.path.join(OUTD, 'm3_run_r0m_v1_2_%s.out' % item)
    ho = os.path.join(HANDD, 'm3_run_r0m_v1_2_%s.json' % item)
    if not os.path.exists(po):
        if os.path.exists(ho):
            raise ValueError('%s: a hand-off without its producer output' % item)
        return 'missing'
    if os.path.exists(ho):
        return 'valid'
    with open(po) as fh:
        lines = fh.read().split('\n')
    m = re.fullmatch(r'm3_run_r0m_v1_2 item (\S+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)', lines[0])
    if m and m.group(1) == item and m.group(3) == SELF_SHA and HO.verdict_ok(lines, CAPPED):
        return 'capped'
    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)


def resumed(state):
    return (' (this piece; %d units of the entry restored)' % len(state['vals'])) if state else ''


def family_parts(graph):
    """the family's computed keys' partitions, name -> (entry, factors, partition), in order_of's order."""
    res = {}
    for name in order_of(graph):
        e = entries_of(graph, [name])[0]
        facs = facs_of(e)
        res[name] = (e, facs, partition_of(e, facs))
    return res


def run_nk(graph, piece):
    stage('%s keys piece %d' % (graph, piece))
    order = order_of(graph)
    g = family_graph(graph)
    scal = prep_scalars(VG[graph])   # the scalars of the family's vertex graph (C-PREP-STAGES)
    part_plants(graph, family_parts(graph))
    norm_rel_plants()
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
    out('PIECE-START %s piece %d resumes at entry %d of %d%s after %d capped piece(s); stop factor %.1f; LIM %d' % (
        graph, piece, start, len(order), (' with %d units of %s restored' % (nin, partial['entry'])) if partial else '', caps, factor, LIM))
    pr, rp = make_prep(VG[graph], g, (), scalars=scal)   # v10's Prep on the restored scalars
    slow, units = [60.0], [0]

    def budget():
        return units[0] == 0 or cpu() + factor * slow[0] <= LIM - 20

    def akest(est):
        """budget() with the slow estimate raised to est (an a_k table the piece has not built yet)."""
        return units[0] == 0 or cpu() + factor * max(slow[0], est) <= LIM - 20

    def done(dt, progress):
        """a unit's CPU raises the slow estimate, except an 'ak' unit (pr.cur_unit, set by m3_bar_v16_1._unit): its table is built once
        per piece and key, and akest covers a fresh one before each entry."""
        if not (progress and pr.cur_unit == 'ak'):
            slow[0] = max(slow[0], dt)
        if progress:
            units[0] += 1
    pr.ubudget, pr.unit_done, pr.akest = budget, done, akest
    res, i, part, prev_sig, est = [], start, None, None, akest_s(graph)
    while i < len(order):
        e = entries_of(graph, [order[i]])[0]
        sig = use_sig(e)
        if i > start and not akest(0.0 if sig == prev_sig else est):   # a fresh table's estimate, else none
            break
        try:
            r = compute_entry(pr, e, state=partial)
        except BAR.Checkpoint as cp:
            part = cp.state
            break
        res.append(r)
        partial, prev_sig = None, sig
        keep_ak(pr, r)
        i += 1
    pr.ubudget = pr.unit_done = pr.akest = None
    nout = len(part['vals']) if part else 0
    prog = i > start or (part is not None and nout > nin)
    gate('C-PIECE', prog, '(%s piece %d: entries %d..%d done, next %d of %d; %d units computed%s)' % (
        graph, piece, start, i - 1, i, len(order), units[0], (', %d units of %s carried' % (nout, part['entry'])) if part else ''))
    write_handoff(graph, {'family': graph, 'piece': piece, 'start': start, 'next': i, 'partial': part, 'stop_factor': factor,
                          'entries': res, 'fallbacks': fb_info()})


def write_records(texts, paths, fails, nofire, tag, opener=open):
    """as m3_run_v1_10_4 l.1504-1517."""
    if fails or nofire or tag != '':
        return []
    for f in paths:
        if os.path.dirname(os.path.abspath(paths[f])) != OUTD or os.path.exists(paths[f]):
            raise ValueError('record path %s: outside out/ or already there' % paths[f])
    done = []
    for f in sorted(paths):
        with opener(paths[f], 'x') as fh:
            fh.write(texts[f])
        done.append((f, paths[f]))
    return done


def walk_pieces(graph, res):
    """C-PIECES: the pieces of a family cover its computed keys in order, each advancing, none left in progress; their entries go into
    res."""
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
    gate('C-PIECES', nxt == len(order) and nin == 0, '(the %s pieces cover all %d computed %s keys, in order, none left in progress)' % (
        graph, len(order), graph))


def run_smoke(graph):
    """as m3_run_r0b_v1_2, with C-MIRROR (in list_check) and C-TB-MAP in place of C-SYM-MAP, and C-RULE-SIZE after the prep (as
    m3_run_r0b_v1_3)."""
    stage('smoke %s' % graph)
    list_check()
    enc_check()
    parity_set()
    tb_map_check()
    alias_check()
    rule_of_check()
    ab_check(graph)
    g = family_graph(graph)
    pr, rp = make_prep(VG[graph], g, ())
    prep_same(graph, g, prep_graph(g), pr)
    STAGE[0] = 'smoke C-RULE-SIZE'
    rule_size_check(graph, pr)
    parts = family_parts(graph)
    plans, tabs = [], {}
    for name, (e, facs, p) in parts.items():
        STAGE[0] = 'smoke %s' % name
        part_checks(e, facs, p)
        t0 = cpu()
        pr.qcap, qmax = qcap_of(pr, p, graph)
        info = ak_plan(pr, facs, p['grouping'])
        key = (tuple(info['forms']), pr.qcap)
        tabs[key] = max(tabs.get(key, 0), info['Dn'])
        pl = pack_plan(pr, facs, p['grouping'], info, e['parity'] == 'free')
        top = max(pl, key=lambda r: r[1] * math.log(r[2] + 1))
        plans += [(name, r) for r in pl]
        line = 'PLAN %s: parity %s, rule %s, G %d, qcap %d (pair degree %d), a_k Dn %d over %d forms; %d table requests, the largest %d^%d (%s)' % (
            name, e['parity'], p['rule'], p['G'], pr.qcap, qmax, info['Dn'], len(info['forms']), len(pl), top[2] + 1, top[1], top[0])
        if e['parity'] == 'free':
            rows = pr.declare_big(p['groups'], p['scal'], *RULE_A[graph])
            risk = ['%s %d moments' % (r[0], r[3]) for r in rows if not r[4] and r[3] * 1.2e-4 > 300]
            line += '; big set %s; arb risk (moments x 1.2e-4 s > 300 s, arb) %s' % ([r[0] for r in rows if r[4]], risk or 'none')
        out(line + '; %.2f s' % (cpu() - t0))
    nvx = 3 * len(GRAPHS[graph]['columns'])
    tot = 0
    for (forms, q), Dm in sorted(tabs.items()):
        m = BAR.table_moments(len(forms), Dm, sum(1 for f in forms if f < nvx), q)
        tot += m
        out('AK-TABLE-PLAN %s: forms %d (%d pairs), D %d, qcap %d: %d moments, about %.0f s' % (graph, len(forms), sum(1 for f in forms if f >= nvx),
                                                                                          Dm, q, m, m * AKRATE))
    out('AK-TABLE-PLAN %s: %d distinct a_k tables, %d moments, about %.0f s if each is built once' % (graph, len(tabs), tot, tot * AKRATE))
    STAGE[0] = 'smoke C-SMOKE-AK'
    e, facs, p = parts[EMPTY[graph]]
    pr.qcap = qcap_of(pr, p, graph)[0]
    t0 = cpu()
    ak, _, info = pr.bound(facs, p['grouping'], bars=False, entry=EMPTY[graph])
    w = ak_dev(ak, e['ak_float'])
    gate('C-SMOKE-AK', w <= 1e-9, '(%s %s: a_k %s against the list\'s ak_float %s: largest |mid - float| / max(1, |float|) %.2e; %.2f s)' % (
        graph, EMPTY[graph], ['%.12g' % float(a.mid) for a in ak], e['ak_float'], w, cpu() - t0))
    f0 = facs[0]
    facs2 = [(f0[0], f0[1], [x * (1 + 1e-6) for x in f0[2]], f0[3], f0[4])] + list(facs[1:])
    ak2, _, _ = pr.bound(facs2, 'std', bars=False, entry=EMPTY[graph] + ' (planted)')
    w2 = ak_dev(ak2, e['ak_float'])
    plant('PLANT-SMOKE-PATH', f0[0] == 'p' and not (w2 <= 1e-9), '(%s with its first p factor\'s q1 times 1 + 1e-6: largest difference %.2e)' % (
        EMPTY[graph], w2))
    STAGE[0] = 'smoke plants'
    part_plants(graph, parts)
    gcache_check(graph, pr, parts)
    barpos_info(graph, pr, parts)
    ak_total_plants()
    norm_rel_plants()
    pack_gate(graph, plans)
    fb_info()


def part_rec_ok(field, graph):
    """C-PART-REC's test of one record's partition field: exactly the family's computed keys, each with rule_of's rule, the groups part_enc
    recomputes from the list's encodings, G = len(groups) and an int qcap >= the family's QCAP0."""
    if set(field) != set(order_of(graph)):
        return False
    for k, v in field.items():
        e = entries_of(graph, [k])[0]
        q = v.get('qcap')
        if (v.get('rule') != rule_of(e) or v.get('groups') != part_enc(rule_of(e), e['factors']) or v.get('G') != len(v.get('groups') or [])
                or isinstance(q, bool) or not isinstance(q, int) or q < QCAP0[graph]):
            return False
    return True


def reader_plants(text, name):
    """the reader plants of m3_run_v1_10_4 l.1688-1771 on the W2M record's text; PLANT-PARZERO marks XT,1 a parity zero."""
    dd = json.loads(text)
    k0 = sorted(k for k in dd['items'] if dd['items'][k]['parity'] == 'free')[0]
    dd['items'][k0]['B'].pop('rnd')
    try:
        RDR._check_text(json.dumps(dd), 300, NN)
        plant('PLANT-FMT', False, '(W2M copy without one rnd)')
    except ValueError:
        plant('PLANT-FMT', True, '(W2M copy without one rnd)')
    dd2 = json.loads(text)
    kr = max((k for k in dd2['items'] if dd2['items'][k]['parity'] == 'free'), key=lambda k: sum(dd2['items'][k]['ak_rad']))
    dd2['items'][kr]['B']['rnd'] = 0.0
    try:
        RDR._check_text(json.dumps(dd2), 300, NN)
        plant('PLANT-RND', False, '(W2M copy with %s rnd = 0)' % kr)
    except ValueError:
        plant('PLANT-RND', sum(dd2['items'][kr]['ak_rad']) > 0, '(W2M copy with %s rnd = 0; its ak_rad sum %.1e)' % (kr, sum(dd2['items'][kr]['ak_rad'])))
    deny = dict(DENY)
    nx = 3 if NN == 4 else 4
    for lab, mut, jref, nexp in (('PLANT-READER-PRECERT', 'precert', 300, NN), ('PLANT-READER-KERNEL', 'kernel', 300, NN),
                                 ('PLANT-READER-PREC', 'prec', 300, NN), ('PLANT-LAYER-V1_1', 'arbeng_ma_v1_1.py', 300, NN),
                                 ('PLANT-LAYER-V1_2', 'arbeng_ma_v1_2.py', 300, NN), ('PLANT-LAYER-V1_4', 'arbeng_ma_v1_4.py', 300, NN),
                                 ('PLANT-READER-MOCK', 'mock_arbeng_v1_4.py', 300, NN), ('PLANT-LAYER-MIX', 'mix', 300, NN),
                                 ('PLANT-VALREC', 'valrec', 300, NN), ('PLANT-CLAIM', 'claim', 300, NN), ('PLANT-ARBK', 'arbk', 300, NN),
                                 ('PLANT-ARBB', 'arbb', 300, NN), ('PLANT-JREF', None, 150, NN), ('PLANT-N', None, 300, nx),
                                 ('PLANT-KIND', 'kind', 300, NN), ('PLANT-CLAIM-BALL', 'claimball', 300, NN),
                                 ('PLANT-CLAIM-BALL-MISSING', 'noclaimball', 300, NN)):
        dd3 = json.loads(text)
        if mut == 'precert':
            dd3['format'] = 'M3_RECORD_v1_PRECERT'
            dd3['claim'] = 'NOT CERTIFIED (PRECERT): ' + dd3['claim']
        elif mut == 'kernel':
            dd3['kernel_sha256'] = flip(dd3['kernel_sha256'])
        elif mut == 'prec':
            dd3['kernel_prec'] = 256
        elif mut in deny:
            dd3['kernel_file'], dd3['kernel_sha256'] = mut, deny[mut]
        elif mut == 'mix':
            dd3['kernel_file'], dd3['kernel_sha256'] = 'arbeng_ma_v1_3.py', '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be'
        elif mut == 'valrec':
            dd3['validation'] = dd3['validation'][:-1] + [flip(dd3['validation'][-1])]
        elif mut == 'claim':
            dd3['claim'] = dd3['claim'] + ' '
        elif mut == 'arbk':
            dd3['arb_kernel_sha256'] = flip(dd3['arb_kernel_sha256'])
        elif mut == 'arbb':
            dd3['arb_base_sha256'] = flip(dd3['arb_base_sha256'])
        elif mut == 'kind':
            dd3['items'][sorted(dd3['items'])[0]].pop('kind')
        elif mut == 'claimball':
            dd3['claim_ball'] = dd3['claim_ball'] + ' '
        elif mut == 'noclaimball':
            dd3.pop('claim_ball')
        what = mut or ('expected J_REF %d' % jref if jref != 300 else 'expected N %d' % nexp)
        try:
            RDR._check_text(json.dumps(dd3), jref, nexp)
            plant(lab, False, '(m3_reader_v6_3 must refuse the mutated W2M copy: %s)' % what)
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3 refuses the mutated W2M copy: %s)' % what)
    dz = json.loads(text)
    dz['items']['XT,1']['parity'] = 'zero'
    try:
        RDR._check_text(json.dumps(dz), 300, NN)
        plant('PLANT-PARZERO', False, '(m3_reader_v6_3 must refuse the W2M copy with XT,1 marked a parity zero)')
    except ValueError:
        plant('PLANT-PARZERO', True, '(m3_reader_v6_3 refuses the W2M copy with XT,1 marked a parity zero)')
    dh = tsha(text)
    try:
        RDR.loads(text, 'RECORD %s %s\nVERDICT VALID\n' % (name, dh), 300, NN, name)
        gate('C-BOUND-RT', True, '(m3_reader_v6_3.loads accepts the W2M text under an output that names it and ends VALID)')
    except ValueError as ex:
        gate('C-BOUND-RT', False, '(refused: %s)' % ex)
    for lab, otext in (('PLANT-BOUND-VERDICT', 'RECORD %s %s\nVERDICT VALID-PRECERT\n' % (name, dh)),
                       ('PLANT-BOUND-INVALID', 'RECORD %s %s\nVERDICT INVALID (C-REP-AK)\n' % (name, dh)),
                       ('PLANT-BOUND-TWO', 'RECORD %s %s\nVERDICT VALID\nVERDICT VALID\n' % (name, dh)),
                       ('PLANT-BOUND-SHA', 'RECORD %s %s\nVERDICT VALID\n' % (name, flip(dh))),
                       ('PLANT-BOUND-NONE', 'VERDICT VALID\n')):
        try:
            RDR.loads(text, otext, 300, NN, name)
            plant(lab, False, '(m3_reader_v6_3.loads must refuse this asm output)')
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3.loads refuses this asm output)')


def resume_chain():
    """as m3_run_v1_10_4 l.1774-1784: C-RESUME-CHAIN."""
    ok, why = True, []
    for graph in RESUME_FAMS:
        b1 = read_handoff('%sr1.%d' % (PFX[graph], NN), graph)
        b2 = read_handoff('%sr2.%d' % (PFX[graph], NN), graph)
        ok = ok and b1['resume_ok'] is True and b1['plant_fired'] is True and b2['resume_ok'] is True and b1['entry'] == b2['entry'] == RESUME_KEY[graph]
        why.append('%s on %s: part 1 cut %s resumed %s, PLANT-RESUME %s; part 2 cut after %d of %d units resumed %s' % (
            graph, b1['entry'], b1['cut'], 'identical' if b1['resume_ok'] else 'DIFFERENT', 'FIRES' if b1['plant_fired'] else 'DOES NOT FIRE',
            b2['cut'], b2['units'], 'identical' if b2['resume_ok'] else 'DIFFERENT'))
    gate('C-RESUME-CHAIN', ok, '(%s)' % '; '.join(why))


def run_resume(graph, part):
    """as m3_run_v1_10_4 l.1787-1856 (C-RESUME, PLANT-RESUME, C-RESUME-SAME) against the key's piece result."""
    stage('%s resume part %d' % (graph, part))
    if graph not in RESUME_FAMS:
        raise ValueError('%s is not in RESUME_FAMS %s' % (graph, RESUME_FAMS))
    res = {}
    walk_pieces(graph, res)
    scal = prep_scalars(VG[graph])
    g = family_graph(graph)
    pr, rp = make_prep(VG[graph], g, (), scalars=scal)
    e = entries_of(graph, [RESUME_KEY[graph]])[0]
    name = name_of(e)
    src = res[(graph, name)]
    facs = facs_of(e)
    p = partition_of(e, facs)
    gr = p['grouping']
    pr.qcap = qcap_of(pr, p, graph)[0]
    pr.declare_big(p['groups'], p['scal'], *RULE_A[graph])

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
    body = {'family': graph, 'part': part, 'entry': name}
    if part == 1:
        t0 = cpu()
        _, st = run(cut=3)
        keys = list(st['vals']) if st else []
        r1, _ = run(state=st) if st else (None, None)
        ok = keys == ['ak', 'm0u', 'm0c'] and r1 is not None and same(src['ak'], r1[0]) and same(src['bars'], r1[1])
        gate('C-RESUME', ok, '(%s part 1: cut after stage a, units %s, resumed with fresh caches: a_k and bars %s the piece result\'s; %.2f s)' % (
            name, keys, 'identical to' if ok else 'NOT identical to', cpu() - t0))
        r2 = None
        if st:
            bad = dict(st, vals=dict(st['vals']))
            bad['vals']['m0u'] = 2 * bad['vals']['m0u']
            r2, _ = run(state=bad)
        fired = r2 is not None and not same(src['bars'], r2[1])
        plant('PLANT-RESUME', fired, '(%s: the stage-a state with m0u doubled must change the bars; rem %s -> %s)' % (
            name, '%.9e' % S.up(src['bars']['rem']), ('%.9e' % S.up(r2[1]['rem'])) if r2 else 'no result'))
        body.update({'cut': keys, 'resume_ok': ok, 'plant_fired': fired})
    else:
        t0 = cpu()
        (ak0, b0, _), _ = run()
        seq = list(pr.ustate['vals'])
        oks = same(src['ak'], ak0) and same(src['bars'], b0)
        gate('C-RESUME-SAME', oks, '(%s straight, %d units, %.2f s: a_k and bars %s the piece result\'s)' % (
            name, len(seq), cpu() - t0, 'identical to' if oks else 'NOT identical to'))
        cutb = next(i for i, k in enumerate(seq) if k.endswith('|c'))
        t0 = cpu()
        _, st = run(cut=cutb)
        r3, _ = run(state=st) if st else (None, None)
        ok = st is not None and len(st['vals']) == cutb and r3 is not None and same(src['ak'], r3[0]) and same(src['bars'], r3[1])
        gate('C-RESUME', ok, '(%s part 2: cut after %d of %d units, before the first stage-c unit, resumed with fresh caches: a_k and bars %s '
             'the piece result\'s; %.2f s)' % (name, cutb, len(seq), 'identical to' if ok else 'NOT identical to', cpu() - t0))
        body.update({'cut': cutb, 'units': len(seq), 'resume_ok': ok and oks})
    pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0
    body['fallbacks'] = fb_info()
    write_handoff(graph, body)


def phi_tokens():
    """M2B_KV_v1's PIN_TRIAL tokens of this N (path under code/ : sha256), the trial vacuum's files."""
    with open(os.path.join(C2B, 'M2B_KV_v1.txt')) as fh:
        for ln in fh:
            if ln.startswith('PIN_TRIAL = '):
                return [t for t in ln[len('PIN_TRIAL = '):].strip().split(' ; ') if ('_N%d_' % NN) in t]
    return []


def phi_ok(toks):
    """C-G-PHI's test: two tokens, each 'path:sha256' whose file under code/ hashes to it and equals this run's own input pin."""
    if len(toks) != 2:
        return False
    for t in toks:
        p_, h_ = t.rsplit(':', 1)
        full = os.path.join(CODEDIR, p_)
        if not os.path.exists(full) or sha(full) != h_ or INPUTS.get((os.path.dirname(full), os.path.basename(full))) != h_:
            return False
    return True


UHAT_KEYS = ('role', 'k', 'e_a', 'empty', 'factors', 'alias_kind', 'mirror_of')


def uhat_ok(items, graph):
    """C-UHAT's test (as m3_run_r0b_v1_2) with mirror_of: each window's W2 sources."""
    es = {name_of(e): e for e in entries_of(graph)}
    if set(items) != set(es):
        return False
    for k, it in items.items():
        a = ALIAS[graph].get(k, (None, None))
        if (any(f not in it for f in UHAT_KEYS) or it['role'] != es[k]['role'] or it['factors'] != es[k]['factors']
                or it['k'] != len(GRAPHS[graph]['columns']) or it['e_a'] != EA[graph] or it['empty'] != EMPTY[graph]
                or it['alias_kind'] != a[1] or it.get('alias_of') != a[0] or it['mirror_of'] != es[k]['srcs']):
            return False
    return True


def sym_ok(files, g, c, t, shift=0.0):
    """C-SYM-TB's test of one pair: every a_k ball [ak - ak_rad, ak + ak_rad] of c (its ak moved by shift) overlaps t's, in exact
    rationals, and the parities agree."""
    a, b = files[g][c], files[g][t]
    for k in range(4):
        x0 = Fraction(a['ak'][k]) + Fraction(shift) - Fraction(a['ak_rad'][k])
        x1 = Fraction(a['ak'][k]) + Fraction(shift) + Fraction(a['ak_rad'][k])
        y0, y1 = Fraction(b['ak'][k]) - Fraction(b['ak_rad'][k]), Fraction(b['ak'][k]) + Fraction(b['ak_rad'][k])
        if not (x0 <= y1 and y0 <= x1):
            return False
    return a['parity'] == b['parity']


def run_asm():
    stage('asm')
    list_check()
    enc_check()
    parity_set()
    tb_map_check()
    alias_check()
    rule_of_check()
    res = {}
    for graph in FAMS:
        walk_pieces(graph, res)
    resume_chain()
    scals = {vg: prep_scalars(vg) for vg in ('VD',)}   # C-PREP-STAGES: the hand-offs the record names
    toks = phi_tokens()
    gate('C-G-PHI', phi_ok(toks), '(M2B_KV_v1 13cc0d9a PIN_TRIAL tokens of N%d: %s; each file under code/ hashes to its token and to this '
         'run\'s pin)' % (NN, toks))
    plant('PLANT-G-PHI', not phi_ok(toks[:1] + [flip(toks[1])] if len(toks) == 2 else []), '(the second token with its sha256\'s last digit changed)')
    files, pfield, rak = {g: {} for g in FAMS}, {g: {} for g in FAMS}, []
    for graph in FAMS:
        for name in order_of(graph):
            e = entries_of(graph, [name])[0]
            r = res[(graph, name)]
            pfield[graph][name] = {'rule': r['rule'], 'G': r['G'], 'groups': r['groups'], 'qcap': r['qcap']}
            if e['parity'] == 'zero':
                if r['parity'] != 'zero':
                    raise ValueError('%s %s: marked zero, computed %s' % (graph, name, r['parity']))
                it = REC.entry_record(None, None, T_REF, 'zero')
            else:
                it = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=r['a0_exact'], laws=r['laws'])
            files[graph][name] = it
            if e['ak_float'] is not None:
                rak.append((ak_dev(r['ak'], e['ak_float']), graph, name))
        for name, (src, kind) in ALIAS[graph].items():
            files[graph][name] = dict(files[graph][src], alias_of=src)
        for name, it in files[graph].items():
            e = entries_of(graph, [name])[0]
            it.update({'role': e['role'], 'k': len(GRAPHS[graph]['columns']), 'e_a': EA[graph], 'empty': EMPTY[graph], 'factors': e['factors'],
                       'alias_kind': ALIAS[graph].get(name, (None, None))[1], 'mirror_of': e['srcs'], 'w2_ref': REF.get(name)})
    wr = max(rak)
    gate('C-REP-AK', wr[0] <= 1e-9, '(%d windows equal to a W2 key, a_k against its list float: largest |certified mid - float| / max(1, |float|) '
         '%.2e at %s %s)' % (len(rak), wr[0], wr[1], wr[2]))
    plant('PLANT-REPAK', not (wr[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')
    okal = all(files[g][n]['ak'] == files[g][s]['ak'] and files[g][n]['B'] == files[g][s]['B'] and files[g][n]['parity'] == files[g][s]['parity']
               and s in order_of(g) for g in FAMS for n, (s, kind) in ALIAS[g].items())
    gate('C-ALIAS-ASM', okal, '(%d alias items carry their computed source\'s a_k, bars and parity exactly)' % sum(len(ALIAS[g]) for g in FAMS))
    pairs = [('W2M', 'XT,%d' % b, 'XB,%d' % b) for b in range(4)]
    wsym = max(abs(files[g][c]['ak'][k] - files[g][t]['ak'][k]) for g, c, t in pairs for k in range(4))
    gate('C-SYM-TB', TBOK[0] and all(ALIAS[g].get(t) == (c, 'tb') for g, c, t in pairs) and all(sym_ok(files, g, c, t) for g, c, t in pairs),
         '(structural, v1_2: XB,b, b = 0..3, are T <-> B aliases of XT,b with C-TB-MAP passed in this item (%s), and the copies carry XT,b\'s a_k '
         'balls and parity; largest |mid difference| %.2e)' % (TBOK[0], wsym))
    g, c, t = pairs[1]
    sh = 10 * (files[g][c]['ak_rad'][0] + files[g][t]['ak_rad'][0]) + 1e-12 * max(1.0, abs(files[g][t]['ak'][0]))
    plant('PLANT-SYM-TB', not sym_ok(files, g, c, t, sh), '(%s with its a_k moved by ten times both a_0 radii plus 1e-12: must miss %s)' % (c, t))
    gate('C-SCOPE', all(set(files[g]) == set(name_of(e) for e in entries_of(g)) for g in FAMS), '(the record holds exactly the twelve windows: '
         '%s)' % ', '.join('%s %d' % (g, len(files[g])) for g in FAMS))
    plant('PLANT-SCOPE', not (set(list(files['W2M'])[1:]) == set(name_of(e) for e in entries_of('W2M'))), '(W2M without one key)')
    gate('C-UHAT', all(uhat_ok(files[g], g) for g in FAMS), '(every item carries role, factors, k, e_a, empty, alias_kind and mirror_of as the '
         'rule gives them: %s)' % ', '.join('%s %s' % (g, uhat_ok(files[g], g)) for g in FAMS))
    badu = {k: dict(v) for k, v in files['W2M'].items()}
    k0 = sorted(badu)[0]
    badu[k0]['k'] = 3
    plant('PLANT-UHAT', not uhat_ok(badu, 'W2M'), '(W2M with %s carrying k 3)' % k0)
    gate('C-PART-REC', all(part_rec_ok(pfield[g], g) for g in FAMS), '(the partition field: every computed key with rule_of\'s rule, the '
         'groups recomputed from the encodings, G = len(groups), qcap >= QCAP0: %s)' % (', '.join('%s %s' % (g, part_rec_ok(pfield[g], g)) for g in FAMS)))
    kx = next(k for k, v in pfield['W2M'].items() if v['G'] >= 2)
    badf = dict(pfield['W2M'])
    badf[kx] = dict(badf[kx], groups=[badf[kx]['groups'][1], badf[kx]['groups'][0]] + badf[kx]['groups'][2:])
    plant('PLANT-PART-REC', not part_rec_ok(badf, 'W2M'), '(W2M\'s field with %s\'s groups 0 and 1 swapped)' % kx)
    tag = TAG
    eng = {'m3_run_r0m_v1_2': SELF_SHA, 'modules': dict(OWNMOD)}
    kern = {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}
    radii = lambda d: {k: d[k] for k in ('a_v', 'ap', 'theta0')}
    fsrc = 'pk11/out/%s:%s' % (TSF, INPUTS[(W4, TSF)])
    absrc = ('pk03/m3_graph_v3.py:%s: vac columns carry the tags A, A, B with A = (3 + sqrt 21)/6 and B = (3 sqrt 5 - sqrt 21)/12 exactly '
             '(m3_graph_v3.coupling; C-AB by (6A - 3)^2 = 21 and (12B + 6A - 3)^2 = 45 with 6A - 3, 12B + 6A - 3, A and B positive)' % OWNMOD['m3_graph_v3.py'])
    texts, paths = {}, {}
    for g in FAMS:
        vg = VG[g]
        hs = {s: 'm3_run_r0m_v1_2_%s%s.%d.json' % (vg, s, NN) for s in ('u', 'c')}
        prep = {'vgraph': vg, 'radii_from': '%s:%s' % (REFVG[vg][NN], INPUTS[(OUTD, REFVG[vg][NN])]),
                'stages': {s: '%s:%s' % (h, sha(os.path.join(HANDD, h))) for s, h in hs.items()}, 'dmaxH': 18}
        extra = {'entry_list': '%s:%s (W2\'s certify keys, by mirror rule)' % (LF, INPUTS[(W4R, LF)]), 'graph': g, 'columns': GRAPHS[g]['columns'],
                 'pairs': GRAPHS[g]['pairs'], 'k': len(GRAPHS[g]['columns']), 'dmaxH': 18, 'claim_ball': CLAIM_BALL, 'prep': prep,
                 'partition': pfield[g], 'aliases': {n: list(v) for n, v in ALIAS[g].items()}, 'mirror_rule': MIRROR_NOTE, 'w2_refs': dict(REF),
                 'parity_zero': ZERO[g], 'g_phi': toks, 'f_source': fsrc, 'ab_source': absrc, 'g_c': GC_NOTE, 'g_norm': GN_NOTE % (g, EMPTY[g]),
                 'e_a': EA[g]}
        top = REC.top_level(NN, 300, {g: radii(ref_prep_vg(vg))}, TRIAL, eng, tag, kern, extra=extra)
        texts[g] = json.dumps(dict(top, items=files[g]))
        paths[g] = os.path.join(OUTD, 'm3_r0m_%s_N%d_J300%s_v1.json' % (g, NN, tag))
        rd = RDR._check_text(texts[g], 300, NN, name=os.path.basename(paths[g]))
        okf = (all(rd['entries'][k] == (files[g][k]['ak'], files[g][k]['err']) for k in files[g]) and set(rd['entries']) == set(files[g])
               and rd['top'].get('partition') == pfield[g] and uhat_ok(json.loads(texts[g])['items'], g))
        gate('C-FMT', okf, '(%s: %d keys read back exactly from the text by m3_reader_v6_3, the partition and u-hat fields with them; %d bytes; '
             'sha256 %s)' % (os.path.basename(paths[g]), len(files[g]), len(texts[g]), tsha(texts[g])))
    reader_plants(texts['W2M'], os.path.basename(paths['W2M']))
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
    written = write_records(texts, paths, FAILS, NOFIRE, tag)
    if not written:
        out('RECORDS NOT WRITTEN (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE] + ([] if tag == '' else ['TAG %r' % (tag,)])))
    for b, path in written:
        gate('C-WRITE', sha(path) == tsha(texts[b]), '(%s holds exactly its C-FMT text)' % os.path.basename(path))
        out('RECORD %s %s' % (os.path.basename(path), sha(path)))


try:
    if FAM == 'asm':
        run_asm()
    elif re.fullmatch(r'VD[uc]', FAM):
        run_prep_stage(FAM[:2], FAM[2])
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
