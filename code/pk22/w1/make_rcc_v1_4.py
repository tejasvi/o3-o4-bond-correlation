#!/usr/bin/env python3
"""make_rcc_v1_4.py (pk22, phase (iii), NE's certified RC engine, revision v1_4): writes pk22/w1/rc_cert/kt_s8h_rcc_v1_4.py from
kt_s8h_rcc_v1_3.py (sha256 5aad7ad7...) as a new file (mode 'x'). One fix: the record writer. v1_3's run_record wrote 28 lines with the
same key PIN and the final and smoke lines without ' = ', so its record, though headed FORMAT = S4U_KV_v1, is refused by the strict
reader (pk07/s4u_kv_ref_v1.py's parse_s4u_kv: one KEY = value per line, KEY [A-Z][A-Z0-9_]*, no key twice). v1_4's run_record writes
every row under its own numbered key, checks the rendered text with that reader before it writes (C-KV-FORMAT) and plants a repeated key
(PLANT-KV-DUP). The function is replaced whole (its old ast source segment, asserted once, by NEW_RUN_RECORD below); the label, the usage
strings and the docstring's first line change, and one docstring line is added. Nothing else changes (the diff shows it). Prints every
sha256. Usage: make_rcc_v1_4.py."""
import ast, hashlib, os
TOP = '/mnt/g2/release/root/code/pk22/w1/rc_cert'
SRC, DST = TOP + '/kt_s8h_rcc_v1_3.py', TOP + '/kt_s8h_rcc_v1_4.py'
NEW_RUN_RECORD = r'''def run_record():
    """both N's smoke and final outputs (this script's sha256 and mode, VERDICT VALID); cert mode writes the record in S4U_KV_v1, one
    KEY = value per line, every key unique and of the form [A-Z][A-Z0-9_]* (v1_4; v1_3's writer repeated the key PIN and wrote output
    lines without ' = '): the claim, the code, the outputs by sha256, then under numbered keys the smokes' control lines, the chunks, per
    class and N the smallest headroom, the n = 5 keys, the coverage list, the pair map, the binding pieces and their C-PIECE-H lines,
    and every pin. C-KV-FORMAT: the rendered text parses with pk07's strict reader (s4u_kv_ref_v1.parse_s4u_kv, the S8 module's KVR,
    pinned there) into exactly its keys; PLANT-KV-DUP: the text with one key repeated must be refused. The record is written only when
    every gate has passed and every plant has fired."""
    own = sha_file(os.path.abspath(__file__))
    fin, smk = {}, {}
    for n in (4, 3):
        for it, dst in (('smoke', smk), ('final', fin)):
            p = os.path.join(OUTD, 'out_%s_%s_%s_n%d.out' % (LABEL, MODE, it, n))
            txt = open(p).read().split('\n') if os.path.exists(p) else []
            ok = bool(txt) and txt[0].startswith('%s sha256 %s MODE=%s ITEM=%s' % (LABEL, own, MODE, it)) and \
                [x for x in txt if x.startswith('VERDICT')] == ['VERDICT VALID']
            out('C-%s N=%d: %s with this script\'s sha256 and VERDICT VALID -> %s' % (it.upper(), n, os.path.basename(p),
                                                                                   gate('C-%s' % it.upper(), ok)))
            dst[n] = (p, sha_file(p), txt)
    if MODE != 'cert' or FAILS:
        return
    header = [('FORMAT', 'S4U_KV_v1'), ('RECORD', 'NE_RC_RECORD_v1'), ('EXPORT_STATUS', 'CERTIFIED'),
              ('CLAIM', 'for N = 4 and every J >= 350, and for N = 3 and every J >= 300: Cov(s_e, s_f) > 0 for every pair of a top-row or '
                        'bottom-row edge e with a horizontal or vertical edge f in NE\'s FLIP/SAME and MIXED classes on the horizontal chain: '
                        'every two-sided class with n >= 5 (the 58 separated D0 pairs of P_3 x P_5 among them) and every class at infinity and '
                        'far'),
              ('CODE', '%s:%s' % (LABEL, own)),
              ('COVERAGE', 'per N and piece, the class keys of the COVER rows: FLIP/SAME H2 (dL, dR, kind), Hinf (dL, inf, kind), H1 (dL, far, '
                           'kind) for dL, dR in DN = %s; MIXED M2 HV (iH, dV, kind), Minf HV (iH, inf, kind), M1 HV (iH, far, kind) for iH in '
                           '0..T_M, dV in -1..T_M - 1, and Minf VH (dV, inf, kind), M1 VH (dV, far, kind), T_M = 3 at N = 4 and 2 at N = 3; kinds '
                           'flip and same; rows for m < m0 with n >= 5 (n = dL + dR + m + 3 and iH + dV + m + 3), the top-mode form from m0 on, '
                           'every m0 <= %d (S8\'s KILL rule); the far rows by routes A and B; slots 0 and 1 from the exact entries, 2..7 and inf '
                           'by RC; the bottom row as the parity mirror (F-a); every slot of DN (F-b)' % (DN, M0MAX))]
    stags = ('BARS', 'C-REPRO-RC5', 'C-HARM-RCC', 'C-MIXED-REG', 'C-HARM-H', 'C-HARM-H-M', 'C-HARM-RC', 'C-REPRO-H', 'C-REPRO-M', 'C-UNIF-H',
             'C-MV-BAR-H', 'C-MV-SF-H')
    ftags = {'CHUNK': 'CHUNK', 'FINALCLASS': 'CLASS', 'FINALN5': 'N5', 'MIN': 'MIN', 'COVER': 'COVER', 'C-COVER-LIST': 'COVERLIST',
             'PAIRMAP': 'PAIRMAP', 'C-PAIRMAP': 'PAIRMAPGATE', 'BINDING': 'BINDING', 'C-PIECE-H': 'CPIECE'}
    rows = []
    for n in (4, 3):
        p, h, txt = smk[n]
        rows.append(('SMOKE_N%d' % n, '%s:%s' % (os.path.basename(p), h)))
        j = 0
        for x in txt:
            if x.split(' ')[0] in stags:
                j += 1
                rows.append(('N%d_SMOKE_%02d' % (n, j), x))
        p, h, txt = fin[n]
        rows.append(('FINAL_N%d' % n, '%s:%s' % (os.path.basename(p), h)))
        cnt = {}
        for x in txt:
            tg = ftags.get(x.split(' ')[0])
            if tg is None:
                continue
            cnt[tg] = cnt.get(tg, 0) + 1
            rows.append(('N%d_%s_%03d' % (n, tg, cnt[tg]), x))
    allp = dict(PINS)
    allp.update(CERT_PINS)
    for j, p in enumerate(sorted(allp), 1):
        rows.append(('PIN_%02d' % j, '%s:%s' % (os.path.relpath(p, CODEDIR), allp[p])))
    body = ''.join('%s = %s\n' % kv for kv in header + rows)
    txt = '# NE_RC_RECORD_v1: written by %s (cert mode; every gate passed).\n' % LABEL + body + 'END = NE_RC_RECORD_v1\n'
    keys = [k for k, v in header + rows] + ['END']
    try:
        d = mod.KVR.parse_s4u_kv(txt)
        okkv = sorted(d) == sorted(keys) and len(set(keys)) == len(keys)
    except ValueError as e:
        okkv = False
        out('C-KV-FORMAT: the strict reader refuses the record (%s)' % e)
    out('C-KV-FORMAT: the record parses with the strict S4U_KV_v1 reader (s4u_kv_ref_v1, pinned in the S8 module) into exactly its %d '
        'keys, each unique -> %s' % (len(keys), gate('C-KV-FORMAT', okkv)))
    try:
        mod.KVR.parse_s4u_kv(txt.replace('\nEND = ', '\n%s = %s\nEND = ' % rows[0]))
        fired = False
    except ValueError:
        fired = True
    plant('PLANT-KV-DUP', fired, '(the record text with its row key %s written twice)' % rows[0][0])
    if FAILS or NOFIRE:
        out('RECORD NOT WRITTEN (%s)' % ', '.join(FAILS + ['%s did not fire' % x for x in NOFIRE]))
        return
    with open(REC_PATH, 'x') as fh:
        fh.write(txt)
    out('RECORD %s %s' % (os.path.basename(REC_PATH), hashlib.sha256(txt.encode()).hexdigest()))'''


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rep(t, old, new, count, label):
    n = t.count(old)
    assert n == count, 'replacement %s: %d occurrences, expected %d' % (label, n, count)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    return t.replace(old, new)


assert os.path.dirname(os.path.abspath(DST)) == TOP and not os.path.exists(DST), DST
with open(SRC, 'rb') as fh:
    sb = fh.read()
print('SOURCE %s %s' % (sha(sb), SRC))
assert sha(sb).startswith('ba9bc621'), sha(sb)
t = sb.decode('utf-8')
old = [ast.get_source_segment(t, nd) for nd in ast.parse(t).body if isinstance(nd, ast.FunctionDef) and nd.name == 'run_record']
assert len(old) == 1, len(old)
print('OLD run_record %s; NEW run_record %s' % (sha(old[0].encode('utf-8')), sha(NEW_RUN_RECORD.encode('utf-8'))))
t = rep(t, old[0], NEW_RUN_RECORD, 1, 'run_record')
t = rep(t, '"""kt_s8h_rcc_v1_3.py -- pk22', '"""kt_s8h_rcc_v1_4.py -- pk22', 1, 'docstring name')
t = rep(t, 'v1_3 (the pins-only revision of v1_2, 1a04598f, by make_rcc_v1_3.py):',
        'v1_4 (this revision of v1_3, 5aad7ad7, by make_rcc_v1_4.py): the record writer writes strict S4U_KV_v1 (numbered keys, checked\n'
        'by the strict reader before it writes: C-KV-FORMAT, PLANT-KV-DUP); nothing else changes. v1_3 (the pins-only revision of v1_2,\n'
        '1a04598f, by make_rcc_v1_3.py):', 1, 'docstring v1_4 line')
t = rep(t, 'Usage: kt_s8h_rcc_v1_3.py cert|dev', 'Usage: kt_s8h_rcc_v1_4.py cert|dev', 1, 'docstring usage')
t = rep(t, "USAGE = 'usage: kt_s8h_rcc_v1_3.py", "USAGE = 'usage: kt_s8h_rcc_v1_4.py", 1, 'USAGE')
t = rep(t, "LABEL = 'kt_s8h_rcc_v1_3'", "LABEL = 'kt_s8h_rcc_v1_4'", 1, 'LABEL')
ast.parse(t)
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('ENGINE %s %s' % (sha(nb), DST))
