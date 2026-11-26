#!/usr/bin/env python3
"""mrx_combine_v1_9.py (pk22): mrx_combine_v1_8.py for mrx_cert_v1_9's certified parts (H4TH's certified J-laws through
m3_lawcert_c3h_v1_1; made by make_mrx_v1_9.py); the record is MR_EXACT_CERT_v1_9_C.kv. mrx_combine_v1_8's docstring follows.
mrx_combine_v1_8.py (pk22): mrx_combine_v1_7.py for mrx_cert_v1_8's certified parts (h-1, h0, t-1 and a0 on every piece; made by
make_mrx_v1_8.py). It writes one CERTIFIED MR_EXACT record, variant C (min of the uniform claim and the certified J-law where a law certificate
covers the entry), with STATUS and EXPORT_STATUS CERTIFIED and RUN_VERDICT VALID (engine v1_8_4's CERTIFIED mode), PRODUCER pk22, the
ORIENT_CHECK and X_DEFINITION texts copied by tool from G6 v1_6_2 sect. 6, and two descriptive header lines (H0_FORM, PE_FORM). TRIAL_SET is
checked against pk25's certified mr/v4 MR_SPECTRAL through MANIFEST_MR_V4_CERT_v1 (6ac308d7); the parts must carry STATUS CERTIFIED and
RUN_VERDICT VALID; four ends per piece. mrx_combine_v1_7's docstring follows.
mrx_combine_v1_7.py (pk22): mrx_combine_v1_6.py (22fa06bc) for mrx_cert_v1_7's parts, whose FIELDS end with Pe_hi (engine v1_8_4 accepts
FIELDS4[MR_EXACT] + Pe_hi); made by make_mrx_v1_7.py. mrx_combine_v1_6's docstring follows.
mrx_combine_v1_6.py (pk22): joins mrx_cert_v1_6's per-N parts into one MR_EXACT record per variant (V = U, C), the form engine v1_8_4
reads (one MR_EXACT.kv with both N's rows on R4's grid), and writes the header lines G6 v1_6_2 sect. 6 asks for, copied by tool from
pk24/MIDROW_G6_SPEC_v1_6_2.md (pinned): X_DEFINITION (the MR_EXACT text) and ORIENT_CHECK (the template with the record's piece counts per
N). Each is checked against engine v1_8_4's constants XDEF['MR_EXACT'], ORIENT_RX, XPOW['MR_EXACT'] and FIELDS4['MR_EXACT'] (the engine file
pinned; its module-level literals read by ast, nothing run). ORIENT_CHECK is written only if both N's runs end VERDICT VALID (DRY), print
C-ORIENT ... -> PASS on all of their pieces and PLANT-ORIENT ... -> FIRES, and name the part files with their sha256s on RECORD lines.
Gates: C-SRC (pins), C-RUNS, C-PARTS (the parts carry mrx_cert_v1_6's sha8 on their CODE lines, the same FIELDS, X_POWER, TRIAL_SET,
LEMMAP_SHA256 and ORIENTATION; TRIAL_SET equal to pk25's certified MR_SPECTRAL's, read by tool through MANIFEST_C6A_CERT_v3; the base keys
and their jlo, jhi strings exactly MR_SPECTRAL's for both N, each with h-1, t-1 and a0), C-TEXT; plants PLANT-TEXT (one character of
X_DEFINITION changed must fail C-TEXT) and PLANT-COUNT (ORIENT_CHECK with N4 one piece fewer must fail the engine's count rule).
Outputs (mode 'x'): midrow/g4/mrc/out/dry/MR_EXACT_DRY_v1_6_<V>.kv. Usage: mrx_combine_v1_6.py"""
import ast, hashlib, os, re, sys

W = '/mnt/g2/release/root/code'
E = W + '/pk22/midrow/g4/mrc'
OUTD = E + '/out/cert'   # mrx_combine_v1_8
SPEC = (W + '/pk24/MIDROW_G6_SPEC_v1_6_2.md', '1e570ab7476927dcd3238f347b744c223209d417084f8b756e259d97f68f8b01')
ENG = (W + '/pk24/mr_engine/kt_mr_assembly_v1_8_4.py', '28a340e7b38b0f37a40b4eb2df4c0f03b58dedf0b80755a659c0157c1094a56c')
MAN = (W + '/pk25/mr/MANIFEST_MR_V4_CERT_v1.sha256', '9cf8e6d238d89eb2bb67964f1ed206a4b9b1e4fd1461b69c02d568d013817615')   # mrx_combine_v1_8: mr/v4
SPEF = W + '/pk25/mr/v4/MR_SPECTRAL.kv'
CERTF = E + '/src/mrx_cert_v1_9.py'
RUNS = {4: E + '/out/mrx_cert_v1_9_cert_n4.out', 3: E + '/out/mrx_cert_v1_9_cert_n3.out'}
ENDS = ('h-1', 'h0', 't-1', 'a0')   # mrx_combine_v1_8: + h0
FAILS, NOFIRE = [], []


def out(line):
    print(line, flush=True)


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read_kv(path):
    head, rows, order = {}, {}, []
    for ln in open(path):
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#'):
            continue
        k, sep, v = ln.partition(' = ')
        assert sep, ln[:80]
        if re.fullmatch(r'N[34]_P[0-9]{4}(_(h-1|h0|t-1|a0))?', k):
            assert k not in rows, k
            rows[k] = v
            order.append(k)
        else:
            assert k not in head, k
            head[k] = v
    return head, rows, order


SELF = sha(os.path.abspath(__file__))
CSHA = sha(CERTF)
out('mrx_combine_v1_9; script sha256 %s; mrx_cert_v1_9 sha256 %s; python %s' % (SELF, CSHA, sys.version.split()[0]))
pins = [SPEC, ENG, MAN]
gate('C-SRC', all(sha(p) == h for p, h in pins), '(%s)' % ', '.join('%s %s' % (os.path.basename(p), sha(p)[:8]) for p, h in pins))
man = dict((ln.split()[1], ln.split()[0]) for ln in open(MAN[0]) if ln.strip())
spe_sha = sha(SPEF)
SH, SR, _ = read_kv(SPEF)
gate('C-SPECTRAL-PIN', man.get('mr/v4/MR_SPECTRAL.kv') == spe_sha, '(mr/v4 MR_SPECTRAL.kv %s as MANIFEST_MR_V4_CERT_v1 lists it)' % spe_sha[:16])
# ---- C-RUNS: both N's runs, their orientation check and plant, their RECORD lines
parts, rec_ok, run_why = {}, True, []
for N, rp in RUNS.items():
    txt = open(rp).read()
    lines = txt.split('\n')
    verd = [ln for ln in lines if ln.startswith('VERDICT')]
    co = [ln for ln in lines if ln.startswith('C-ORIENT (on all ')]
    po = [ln for ln in lines if ln.startswith('PLANT-ORIENT (u~_x negated: C-ORIENT fails on ')]
    mco = re.fullmatch(r'C-ORIENT \(on all ([0-9]+) pieces: .* -> PASS', co[0]) if len(co) == 1 else None
    mpo = re.fullmatch(r'PLANT-ORIENT \(u~_x negated: C-ORIENT fails on ([0-9]+) of ([0-9]+) pieces\) -> FIRES', po[0]) if len(po) == 1 else None
    okN = verd == ['VERDICT VALID'] and mco is not None and mpo is not None and mco.group(1) == mpo.group(1) == mpo.group(2)
    for V in ('U', 'C'):
        pp = os.path.join(OUTD, 'MR_EXACT_PART_v1_9_%s_N%d.kv' % (V, N))
        hit = [ln for ln in lines if ln.startswith('RECORD %s sha256 ' % pp)]
        okN = okN and len(hit) == 1 and hit[0].split()[3] == sha(pp)
        parts[(V, N)] = pp
    rec_ok = rec_ok and okN
    run_why.append('N%d %s %s: %s, C-ORIENT on %s pieces, PLANT-ORIENT %s' % (N, os.path.basename(rp), sha(rp)[:8], verd, mco.group(1) if mco else '?',
                                                                            'fired' if mpo else 'missing'))
    if mco:
        parts[('n', N)] = int(mco.group(1))
gate('C-RUNS', rec_ok, '(%s; each names its two part files with their sha256s on RECORD lines)' % '; '.join(run_why))
# ---- the texts from the spec, checked against the engine's constants
spec = open(SPEC[0]).read()
xd = re.findall(r'^  - MR_EXACT: "([^"]+)"$', spec, re.M)
oc = re.findall(r'\*\*ORIENT_CHECK\*\*, exactly[^\n]*\n\s*"([^"]+)"', spec)
XDEF_T = xd[0] if len(xd) == 1 else None
OC_T = ' '.join(oc[0].split()) if len(oc) == 1 else None
etree = ast.parse(open(ENG[0]).read())


def eng_const(name):
    top = [n for n in etree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name]
    assert len(top) == 1, name
    return top[0].value


EXDEF = ast.literal_eval(eng_const('XDEF'))['MR_EXACT']
EXPOW = ast.literal_eval(eng_const('XPOW'))['MR_EXACT']
ORX = ast.literal_eval(eng_const('ORIENT_RX'))
EF = ast.literal_eval(eng_const('FIELDS'))['MR_EXACT']
f4 = eng_const('FIELDS4')
kw = [k for k in f4.keywords if k.arg == 'MR_EXACT']
assert isinstance(f4, ast.Call) and len(kw) == 1 and isinstance(kw[0].value, ast.BinOp) and isinstance(kw[0].value.right, ast.Constant)
EFIELDS4 = EF + kw[0].value.right.value


def text_ok(xdef, ochk, n4, n3, fields, xpow):
    m = re.match(ORX, ochk or '')
    return xdef == EXDEF and m is not None and (int(m.group(1)), int(m.group(2))) == (n4, n3) and fields == EFIELDS4 + ' Pe_hi' and xpow == EXPOW


n4, n3 = parts.get(('n', 4)), parts.get(('n', 3))
OCHK = OC_T.replace('<n4>', str(n4)).replace('<n3>', str(n3)) if (OC_T and OC_T.count('<n4>') == 1 and OC_T.count('<n3>') == 1) else None
# ---- C-PARTS
heads, rowsets, pbad = {}, {}, []
for (V, N), pp in [(k, v) for k, v in parts.items() if k[0] in ('U', 'C')]:
    h, r, o = read_kv(pp)
    heads[(V, N)], rowsets[(V, N)] = h, (r, o)
    if h.get('RECORD') != 'MR_EXACT_PART' or h.get('FORMAT') != 'MR_INPUT_KV_v4' or h.get('CODE') != 'pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py:%s' % CSHA[:8] \
            or h.get('STATUS') != 'CERTIFIED' or h.get('RUN_VERDICT') != 'VALID':
        pbad.append('%s N%d header' % (V, N))
    base = sorted(set(k.rsplit('_', 1)[0] for k in r))
    want = sorted(k for k in SR if k.startswith('N%d_' % N))
    if base != want or any(r['%s_%s' % (b, e)].split()[:2] != SR[b].split()[:2] for b in base for e in ENDS if '%s_%s' % (b, e) in r) \
            or len(r) != 4 * len(want) or (parts.get(('n', N)) != len(want)):
        pbad.append('%s N%d rows' % (V, N))
for k in ('FIELDS', 'X_POWER', 'TRIAL_SET', 'LEMMAP_SHA256', 'ORIENTATION', 'J_UNIFORMITY', 'FORMAT'):
    if len(set(h.get(k) for h in heads.values())) != 1:
        pbad.append('header %s differs' % k)
trial = heads[('U', 4)].get('TRIAL_SET') if ('U', 4) in heads else None
gate('C-PARTS', not pbad and trial == SH.get('TRIAL_SET'), '(4 parts: RECORD MR_EXACT_PART, STATUS CERTIFIED, RUN_VERDICT VALID, CODE mrx_cert_v1_9 %s; FIELDS, X_POWER, TRIAL_SET, '
     'LEMMAP_SHA256, ORIENTATION equal; TRIAL_SET equal to MR_SPECTRAL\'s; rows: each base key and its jlo, jhi exactly MR_SPECTRAL\'s, N4 %s '
     'and N3 %s pieces, four ends each)%s' % (CSHA[:8], n4, n3, (': ' + ', '.join(pbad)) if pbad else ''))
hU = heads.get(('U', 4), {})
gate('C-TEXT', XDEF_T is not None and OCHK is not None and text_ok(XDEF_T, OCHK, n4, n3, hU.get('FIELDS'), hU.get('X_POWER')),
     '(X_DEFINITION and ORIENT_CHECK copied from %s sect. 6: X_DEFINITION equals engine v1_8_4\'s XDEF[MR_EXACT]; ORIENT_CHECK matches its '
     'ORIENT_RX with N4 %s, N3 %s, the record grid\'s counts; FIELDS equal its FIELDS4[MR_EXACT] + Pe_hi, X_POWER its XPOW[MR_EXACT])' % (
         os.path.basename(SPEC[0]), n4, n3))
plant('PLANT-TEXT', XDEF_T is not None and not text_ok(XDEF_T.replace('<=', '<', 1), OCHK, n4, n3, hU.get('FIELDS'), hU.get('X_POWER')),
      '(X_DEFINITION with its first <= changed to < must fail C-TEXT)')
plant('PLANT-COUNT', OCHK is not None and not text_ok(XDEF_T, OCHK.replace('(N4 %s,' % n4, '(N4 %s,' % (n4 - 1), 1), n4, n3, hU.get('FIELDS'),
                                                     hU.get('X_POWER')), '(ORIENT_CHECK with N4 %s - 1 pieces must fail the engine\'s count rule)' % n4)
if FAILS or NOFIRE:
    out('VERDICT INVALID (fails %s, plants not firing %s); no record written' % (FAILS, NOFIRE))
    sys.exit(3)
for V in ('C',):   # mrx_combine_v1_8: the certified record is variant C
    h4, h3 = heads[(V, 4)], heads[(V, 3)]
    path = os.path.join(OUTD, 'MR_EXACT_CERT_v1_9_%s.kv' % V)
    head = ['# MR_EXACT: CERTIFIED record of pk22 on pk25\'s mr/v4 MR_SPECTRAL and MR_INSERT with mr/v3 MR_LEMMAP (mrx_cert_v1_9 parts N = 4 and 3, '
            'joined by mrx_combine_v1_9; h-1, h0, t-1, a0; with Pe_hi); errors: %s' % ('each record\'s uniform claim' if V == 'U' else 'min of the uniform claim and the certified J-law '
                                                  'where m3_lawcert_c3h_v1_1 or m3_lawcert_v1_1 covers the entry, else the uniform claim'),
            'FORMAT = MR_INPUT_KV_v4', 'RECORD = MR_EXACT', 'PRODUCER = pk22 mrx_cert_v1_9 CERT_%s' % V,
            'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py:%s' % CSHA[:8],
            'JOINED_BY = pk22/midrow/g4/mrc/src/mrx_combine_v1_9.py:%s' % SELF[:8], 'STATUS = CERTIFIED', 'EXPORT_STATUS = CERTIFIED', 'RUN_VERDICT = VALID',
            'SOURCE = N4: %s ; N3: %s' % (h4.get('SOURCE'), h3.get('SOURCE')), 'J_UNIFORMITY = %s' % h4.get('J_UNIFORMITY'),
            'ORIENTATION = %s' % h4.get('ORIENTATION'), 'ORIENT_CHECK = %s' % OCHK, 'TRIAL_SET = %s' % h4.get('TRIAL_SET'),
            'LEMMAP_SHA256 = %s' % h4.get('LEMMAP_SHA256'), 'X_POWER = %s' % h4.get('X_POWER'), 'X_DEFINITION = %s' % XDEF_T,
            'H0_FORM = h0 (G6 v1_6_2 sect. 4.1, d = 0, no norm entry): Lemma A on w = S a(0) from the H4TH components, X = |Q_W w| by sect. 0d item 2\'s '
            'fixed point on r_W (the windowed Lemma 3 bound from MR_INSERT\'s h row and MR_SPECTRAL), N\' = r_W; <u, w2> and r by Lemma A at level 0 with '
            '|Q_W l_3| <= q_0 + R_w rho_1^2',
            'PE_FORM = Pe_hi >= |P_e a|: h-1 and t-1 the free-end bound |a| (FFH, S8 E2 overlaps); a0 Lemma P on a; h0 G6 sect. 4.3\'s m = 1 form at d = 0 '
            'from MR_INSERT (Pev_hi = C), a valid filler that keeps FIELDS uniform',
            'FIELDS = %s' % h4.get('FIELDS')]
    body = []
    for N in (4, 3):
        r, o = rowsets[(V, N)]
        body += ['%s = %s' % (k, r[k]) for k in o]
    assert os.path.dirname(path) == OUTD
    with open(path, 'x') as fh:
        fh.write('\n'.join(head + body) + '\n')
    out('RECORD %s sha256 %s rows %d' % (path, sha(path), len(body)))
out('VERDICT VALID')
