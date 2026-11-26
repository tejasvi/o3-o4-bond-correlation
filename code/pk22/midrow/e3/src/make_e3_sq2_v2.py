#!/usr/bin/env python3
"""make_e3_sq2_v2.py (pk22; item (3) part (6)): writes (mode 'x') midrow/e3/src/e3_sq2_v2.py from the template e3_sq2_v2.tmpl.py, filling
@@MOCK@@ and @@SRC@@ (paths and full sha256s computed here from the files). No hash is typed in full.
  --mock: pk23's MOCK M4XY record (pk23/it3/m4xy/mocks/out/M4XY_KV_v1_MOCK_m4xy_asm_v1.txt) with its mock asm output, for a test of
          the code path; writes SCRATCH_mock_e3_sq2_v2.py, whose runs write MOCK records only.
  --cert M4KV ASMOUT M4MAN V18MAN: pk23's certified M4XY record, its asm output (m4xy_asm_v1_1's) and release manifest, and the run
          manifest of the x records (kt_cert_v1_8_xy_2's, MANIFEST_V1_8_XY_2_X_v1) (paths under code); the reader is m4xy_reader_v1_1.py;
          writes e3_sq2_v2.py."""
import hashlib, os, sys

W = '/mnt/g2/release/root/code'
D = W + '/pk22/midrow/e3/src'
TPL = D + '/e3_sq2_v2.tmpl.py'
A = sys.argv[1:]
MOCK = A == ['--mock']
assert MOCK or (len(A) == 5 and A[0] == '--cert'), 'usage: --mock | --cert M4KV ASMOUT M4MAN V18MAN'
DST = D + ('/SCRATCH_mock_e3_sq2_v2.py' if MOCK else '/e3_sq2_v2.py')
M4 = 'pk23/it3/m4xy'
if MOCK:
    files = {'m4kv': M4 + '/mocks/out/M4XY_KV_v1_MOCK_m4xy_asm_v1.txt', 'm4reader': M4 + '/m4xy_reader_v1.py',
             'm4asm_out': M4 + '/out/out_m4xy_asm_v1_mock1.out'}
else:
    files = {'m4kv': A[1], 'm4reader': M4 + '/m4xy_reader_v1_1.py', 'm4asm_out': A[2], 'm4man': A[3], 'v18man': A[4],   # pk23's v1_1 reader
             'v18': 'pk22/midrow/e3/kt/kt_cert_v1_8_xy_2.py',
             'x4': 'pk22/midrow/e3/kt/out_kt_cert_v1_8_xy_2_x.xyn4.out', 'x3': 'pk22/midrow/e3/kt/out_kt_cert_v1_8_xy_2_x.xyn3.out'}
files.update({'spectral': 'pk25/mr/v4/MR_SPECTRAL.kv', 'c10': 'pk25/c10/C10_RECORD_v1.kv', 'c10man': 'pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256'})


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


assert os.path.dirname(DST) == os.path.dirname(os.path.abspath(__file__)) and not os.path.exists(DST), DST
print('TEMPLATE %s %s' % (sha(TPL), TPL))
src = {k: (W + '/' + p, sha(W + '/' + p)) for k, p in files.items()}
assert src['spectral'][1].startswith('4a609ccf') and src['c10'][1].startswith('29a4f3c6') and src['c10man'][1].startswith('bf8df397'), src
if not MOCK:
    assert src['v18'][1].startswith('7f6d0e0f'), src['v18']
for k in sorted(src):
    print('PIN %s %s %s' % (k, src[k][1], src[k][0]))
with open(TPL) as fh:
    T = fh.read()
assert T.count('@@MOCK@@') == 1 and T.count('@@SRC@@') == 1
T = T.replace('@@MOCK@@', repr(MOCK))
T = T.replace('@@SRC@@', '{\n' + ''.join("    '%s': ('%s',\n        '%s'),\n" % (k, p, h) for k, (p, h) in sorted(src.items())) + '}')
assert '@@' not in T
with open(DST, 'x') as fh:
    fh.write(T)
print('WROTE %s %s%s' % (hashlib.sha256(T.encode('utf-8')).hexdigest(), DST, ' (MOCK)' if MOCK else ''))
