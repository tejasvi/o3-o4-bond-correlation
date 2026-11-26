#!/usr/bin/env python3
"""make_mrx_v1_9.py (pk22; the P0_LOG row 4485: MR_EXACT v1_9 with H4TH's certified J-laws): writes (mode 'x')
midrow/g4/mrc/src/mrx_cert_v1_9.py from mrx_cert_v1_8.py and mrx_combine_v1_9.py from mrx_combine_v1_8.py by exact replacements of
asserted counts, and line-prefix edits for the CERTSRC rows that carry pins (no hash is typed here). The new pins come from the frozen
manifests MANIFEST_m3_reader_c3h_v1_1 (the reader fork v1_1) and MANIFEST_C3H_LAWCERT_v1_1 (the certificates and their jobs' outputs), each
checked against its file and against the sha8 the producer's tool outputs gave."""
import hashlib, os

W = '/mnt/g2/release/root/code'
D = W + '/pk22/midrow/g4/mrc/src'
G4 = W + '/pk22/midrow/g4'
M3 = W + '/pk22/m3'
SRCF, SRCC = D + '/mrx_cert_v1_8.py', D + '/mrx_combine_v1_8.py'
DST, DSTC = D + '/mrx_cert_v1_9.py', D + '/mrx_combine_v1_9.py'
RMAN, LMAN = (G4 + '/MANIFEST_m3_reader_c3h_v1_1.sha256', '5202b515'), (G4 + '/MANIFEST_C3H_LAWCERT_v1_1.sha256', 'bce72571')
WANT = {'READER': (M3 + '/m3_reader_c3h_v1_1.py', 'febfafab', RMAN), 'C4': (M3 + '/out/m3_lawcert_c3h_v1_1_N4.json', '75eb63eb', LMAN),
        'C3': (M3 + '/out/m3_lawcert_c3h_v1_1_N3.json', '05ee268c', LMAN), 'O4': (M3 + '/out/m3_lawcert_c3h_v1_1_4.out', '3ef6e59b', LMAN),
        'O3': (M3 + '/out/m3_lawcert_c3h_v1_1_3.out', '05473438', LMAN)}


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def manifest(p):
    acc = {}
    with open(p) as fh:
        for ln in fh:
            h_, p_ = ln.rstrip('\n').split('  ', 1)
            acc[p_] = h_
    return acc


for p in (DST, DSTC):
    assert os.path.dirname(p) == os.path.dirname(os.path.abspath(__file__)) and not os.path.exists(p), p
s0, sc = sha(SRCF), sha(SRCC)
print('SOURCE %s %s\nSOURCE %s %s' % (s0, SRCF, sc, SRCC))
assert s0.startswith('85915d00') and sc.startswith('932aefbf'), (s0, sc)
for mp, m8 in (RMAN, LMAN):
    assert sha(mp).startswith(m8), mp
PIN = {}
for k, (p, s8, (mp, m8)) in WANT.items():
    h = sha(p)
    assert h.startswith(s8) and manifest(mp).get(p) == h, (k, h)
    PIN[k] = (p, h)
    print('PIN %s %s %s (listed so in %s %s)' % (k, h, p, os.path.basename(mp), m8))
with open(SRCF) as fh:
    T = fh.read()
NREP = [0]


def rep(lab, old, new):
    global T
    n = T.count(old)
    assert n == 1, (lab, n)
    T = T.replace(old, new)
    NREP[0] += 1
    print('REPLACE %s: 1 occurrence, %d -> %d chars' % (lab, len(old), len(new)))


def line_set(lab, prefix, new):
    global T
    ls = T.split('\n')
    hit = [i for i, ln in enumerate(ls) if ln.startswith(prefix)]
    assert len(hit) == 1, (lab, len(hit))
    old = ls[hit[0]]
    ls[hit[0]] = new
    T = '\n'.join(ls)
    NREP[0] += 1
    print('LINE %s: line %d, %d -> %d chars' % (lab, hit[0] + 1, len(old), len(new)))


DOC = '''"""mrx_cert_v1_9.py (pk22): mrx_cert_v1_8.py with H4TH's certified J-laws (the P0_LOG row 4485). v1_8's h0 rows took the uniform claims
of c3h's H4TH entries, which have no law certificate in m3_lawcert_c3h_v1, so h0's x sign held only to J 484 (N4) and 854 (N3). Now variant C
reads the c3h certificates of m3_lawcert_c3h_v1_1 (%(c4)s, %(c3)s; frozen in MANIFEST_C3H_LAWCERT_v1_1 %(lm)s), which certify CE3H, CS4H
and H4TH, through the reader fork m3_reader_c3h_v1_1 (%(rd)s; frozen in MANIFEST_m3_reader_c3h_v1_1 %(rm)s): CERTDEF's c3h row names that
producer with the three families, cert_law gives H4TH's entries their certified laws, and C-CERT-SAME now covers them too. Nothing else changes.
Usage: mrx_cert_v1_9.py cert N
---- mrx_cert_v1_8.py's docstring:
mrx_cert_v1_8.py (pk22): the certified v4 MR_EXACT writer (the P0_LOG rows 4430, 4446, 4453)''' % dict(
    c4=PIN['C4'][1][:8], c3=PIN['C3'][1][:8], lm=sha(LMAN[0])[:8], rd=PIN['READER'][1][:8], rm=sha(RMAN[0])[:8])
rep('doc', '''"""mrx_cert_v1_8.py (pk22): the certified v4 MR_EXACT writer (the P0_LOG rows 4430, 4446, 4453)''', DOC)
rep('usage', "    print('usage: mrx_cert_v1_8.py cert N   (N = 4 or 3; certified parts for mrx_combine_v1_8)')",
    "    print('usage: mrx_cert_v1_9.py cert N   (N = 4 or 3; certified parts for mrx_combine_v1_9)')")


def row(key, p4, h4, p3, h3, note):
    return "    '%s': ({4: '%s', 3: '%s'}[N], {4: '%s', 3: '%s'}[N]),   # mrx_cert_v1_9: %s" % (key, p4, p3, h4, h3, note)


line_set('reader', "    'READER': (", row('READER', PIN['READER'][0], PIN['READER'][1], PIN['READER'][0], PIN['READER'][1], 'the reader fork v1_1'))
line_set('c_c3h', "    'C_c3h': (", row('C_c3h', PIN['C4'][0], PIN['C4'][1], PIN['C3'][0], PIN['C3'][1], "m3_lawcert_c3h_v1_1's certificates"))
line_set('o_c3h', "    'O_c3h': (", row('O_c3h', PIN['O4'][0], PIN['O4'][1], PIN['O3'][0], PIN['O3'][1], "their jobs' outputs"))
rep('certdef', "CERTDEF = {'c3h': ('m3_lawcert_c3h_v1.py', ('CE3H', 'CS4H'), MYO + '/m3_c3h_%%s_N%d_J300_c3h.json' % N, 'A_c3h', 'C_c3h', 'O_c3h'),",
    "CERTDEF = {'c3h': ('m3_lawcert_c3h_v1_1.py', ('CE3H', 'CS4H', 'H4TH'), MYO + '/m3_c3h_%%s_N%d_J300_c3h.json' % N, 'A_c3h', 'C_c3h', 'O_c3h'),   # v1_9")
rep('rdr', "RDR = load_as('m3_reader_c3h_v1', CERTSRC['READER'][0])", "RDR = load_as('m3_reader_c3h_v1_1', CERTSRC['READER'][0])   # mrx_cert_v1_9")
rep('lawcert-msg', "'(%s: %s through m3_reader_c3h_v1.load_lawcert bound to %s; its records %s through load bound to %s: %s)'",
    "'(%s: %s through m3_reader_c3h_v1_1.load_lawcert bound to %s; its records %s through load bound to %s: %s)'")
rep('certlaw', "    if rk in ('CE3H', 'CS4H') and CERTS.get('c3h') is not None:",
    "    if rk in ('CE3H', 'CS4H', 'H4TH') and CERTS.get('c3h') is not None:   # mrx_cert_v1_9: + H4TH (m3_lawcert_c3h_v1_1)")
rep('count-h0', "out('CERT-COUNT N=%d h0: %d of %d entries take a certified law (H4TH has no law certificate: its uniform claims); the S9 Gram entries: %d of 9' % (",
    "out('CERT-COUNT N=%d h0: %d of %d entries take a certified law (H4TH through m3_lawcert_c3h_v1_1); the S9 Gram entries: %d of 9' % (")
rep('part-path', "'MR_EXACT_PART_v1_8_%s_N%d.kv' % (V, N))", "'MR_EXACT_PART_v1_9_%s_N%d.kv' % (V, N))")
rep('part-head', "'# MR_EXACT PART (N = %d) of pk22 mrx_cert_v1_8 on mr/v4 MR_SPECTRAL and MR_INSERT with mr/v3 MR_LEMMAP (mrx_combine_v1_8 joins '",
    "'# MR_EXACT PART (N = %d) of pk22 mrx_cert_v1_9 on mr/v4 MR_SPECTRAL and MR_INSERT with mr/v3 MR_LEMMAP (mrx_combine_v1_9 joins '")
rep('part-err1', "'certified J-law where m3_lawcert_c3h_v1 or m3_lawcert_v1_1 covers the entry (all of h-1; '",
    "'certified J-law where m3_lawcert_c3h_v1_1 or m3_lawcert_v1_1 covers the entry (all of h-1 and h0; '")
rep('part-err2', "'E3 and S9 G entries of t-1 and a0), else the uniform claim (h0\\'s H4TH entries; the c3, c3j, c3l and c3n entries)'),",
    "'E3 and S9 G entries of t-1 and a0), else the uniform claim (the c3, c3j, c3l and c3n entries)'),")
rep('part-prod', "'PRODUCER = pk22 mrx_cert_v1_8 CERT_%s' % V,", "'PRODUCER = pk22 mrx_cert_v1_9 CERT_%s' % V,")
rep('part-code', "'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_8.py:%s' % code_sha[:8],", "'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py:%s' % code_sha[:8],")
assert "('m3_lawcert_c3h_v1.py'," not in T and "'m3_reader_c3h_v1'" not in T and "m3_lawcert_c3h_v1_N" not in T and "m3_lawcert_c3h_v1_4.out" not in T
with open(DST, 'x') as fh:
    fh.write(T)
print('REPLACEMENTS (cert) %d' % NREP[0])
print('WROTE %s %s' % (hashlib.sha256(T.encode('utf-8')).hexdigest(), DST))

# ---- the combine
with open(SRCC) as fh:
    T = fh.read()
NREP[0] = 0
rep('cdoc', '''"""mrx_combine_v1_8.py (pk22): mrx_combine_v1_7.py for mrx_cert_v1_8's certified parts''',
    '''"""mrx_combine_v1_9.py (pk22): mrx_combine_v1_8.py for mrx_cert_v1_9's certified parts (H4TH's certified J-laws through
m3_lawcert_c3h_v1_1; made by make_mrx_v1_9.py); the record is MR_EXACT_CERT_v1_9_C.kv. mrx_combine_v1_8's docstring follows.
mrx_combine_v1_8.py (pk22): mrx_combine_v1_7.py for mrx_cert_v1_8's certified parts''')
rep('c-certf', "CERTF = E + '/src/mrx_cert_v1_8.py'", "CERTF = E + '/src/mrx_cert_v1_9.py'")
rep('c-runs', "RUNS = {4: E + '/out/mrx_cert_v1_8_cert_n4.out', 3: E + '/out/mrx_cert_v1_8_cert_n3.out'}",
    "RUNS = {4: E + '/out/mrx_cert_v1_9_cert_n4.out', 3: E + '/out/mrx_cert_v1_9_cert_n3.out'}")
rep('c-banner', "out('mrx_combine_v1_8; script sha256 %s; mrx_cert_v1_8 sha256 %s; python %s'", "out('mrx_combine_v1_9; script sha256 %s; mrx_cert_v1_9 sha256 %s; python %s'")
rep('c-pp', "pp = os.path.join(OUTD, 'MR_EXACT_PART_v1_8_%s_N%d.kv' % (V, N))", "pp = os.path.join(OUTD, 'MR_EXACT_PART_v1_9_%s_N%d.kv' % (V, N))")
rep('c-code', "h.get('CODE') != 'pk22/midrow/g4/mrc/src/mrx_cert_v1_8.py:%s' % CSHA[:8] \\", "h.get('CODE') != 'pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py:%s' % CSHA[:8] \\")
rep('c-msg', "RUN_VERDICT VALID, CODE mrx_cert_v1_8 %s;", "RUN_VERDICT VALID, CODE mrx_cert_v1_9 %s;")
rep('c-path', "path = os.path.join(OUTD, 'MR_EXACT_CERT_v1_8_%s.kv' % V)", "path = os.path.join(OUTD, 'MR_EXACT_CERT_v1_9_%s.kv' % V)")
rep('c-head1', "with mr/v3 MR_LEMMAP (mrx_cert_v1_8 parts N = 4 and 3, '", "with mr/v3 MR_LEMMAP (mrx_cert_v1_9 parts N = 4 and 3, '")
rep('c-head2', "'joined by mrx_combine_v1_8; h-1, h0, t-1, a0; with Pe_hi); errors: %s'", "'joined by mrx_combine_v1_9; h-1, h0, t-1, a0; with Pe_hi); errors: %s'")
rep('c-err', "'where m3_lawcert_c3h_v1 or m3_lawcert_v1_1 covers the entry, else the uniform claim'",
    "'where m3_lawcert_c3h_v1_1 or m3_lawcert_v1_1 covers the entry, else the uniform claim'")
rep('c-prod', "'PRODUCER = pk22 mrx_cert_v1_8 CERT_%s' % V,", "'PRODUCER = pk22 mrx_cert_v1_9 CERT_%s' % V,")
rep('c-codeh', "'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_8.py:%s' % CSHA[:8],", "'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py:%s' % CSHA[:8],")
rep('c-joined', "'JOINED_BY = pk22/midrow/g4/mrc/src/mrx_combine_v1_8.py:%s' % SELF[:8],", "'JOINED_BY = pk22/midrow/g4/mrc/src/mrx_combine_v1_9.py:%s' % SELF[:8],")
with open(DSTC, 'x') as fh:
    fh.write(T)
print('REPLACEMENTS (combine) %d' % NREP[0])
print('WROTE %s %s' % (hashlib.sha256(T.encode('utf-8')).hexdigest(), DSTC))
