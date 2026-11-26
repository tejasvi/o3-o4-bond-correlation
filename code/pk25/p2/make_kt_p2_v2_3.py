#!/usr/bin/env python3
"""make_kt_p2_v2_3.py (pk25, P2 the factored side table; the P0_LOG rows 4557, 4622, 4637, 4639, 4642, 4657, 4659): builds p2/<argv[1]>
(a new file) from p2/src/kt_p2_v2_3.py.in: the name; the NU record, its manifest and its producer (argv[2:5], relative to code/), or no NU
record when argv[2:] is absent (NU_PATH = NU_CODE = None, and any nonzero delta is refused); and the pins of the inputs it reads (v2_1's 40,
pk25/nu/nu_reader_v1_1.py, and the NU record with its producer when given) computed from the live files. MR_LEMMAP v3, the C10 record and
MR_SPECTRAL v4 must carry the sha256 their pk25 manifests list (paths relative to pk25/); the NU record and its producer must carry the
sha256 the NU manifest lists (pk24's form: paths relative to code/), and the record must sit under pk24/nu/. Parses the result with ast and
writes it with open(..., 'x'). No compute."""
import ast
import hashlib
import os
import re
import sys

W = '/mnt/g2/release/root/code'
SRC = W + '/pk25/p2/src/kt_p2_v2_3.py.in'
M3O = W + '/pk03/out/'
INPUTS = [W + '/pk25/mr/v3/MR_LEMMAP.kv', W + '/pk25/c10/C10_RECORD_v1.kv', W + '/pk25/m3/m3_reader_s9h_v1.py']
for N in (4, 3):
    INPUTS += [M3O + 'm3_s8v3_%s_N%d_J300_v1_8_1.json' % (F, N) for F in ('D', 'E2', 'E3', 'FF')]
    INPUTS += [M3O + 'm3_run_v1_8_1_asmP.%d.out' % N, M3O + 'm3_s8v3_N_N%d_J300_v1_8_2.json' % N, M3O + 'm3_run_v1_8_2_asmN.%d.out' % N]
    INPUTS += [M3O + 'm3_lawcert_v1_1_N%d.json' % N, M3O + 'm3_lawcert_v1_1_%d.out' % N, M3O + 'm3_lawcert_v1_2_N%d.json' % N,
               M3O + 'm3_lawcert_v1_2_%d.out' % N]
INPUTS += [W + '/pk11/out/ts_N4_J170_D_S_z9sym_v1.json', W + '/pk11/out/ts_N3_S_z9sym_v1.json',
           W + '/pk11/out/vacres_K3_N4_sym_v1.json', W + '/pk11/out/vacres_K3_N3_sym_v1.json']
INPUTS += [W + '/pk25/mr/v4/MR_SPECTRAL.kv', W + '/pk02/M2B_KV_v1.txt', W + '/pk02/out/out_m2b_asm_v1.out', W + '/pk02/m2b_reader_v1.py',
           W + '/pk15/M4_KV_v1.txt', W + '/pk15/out/out_m4_asm_v1.out', W + '/pk15/m4_reader_v1.py']
INPUTS += [W + '/pk02/out_kt_cert_v1_6_x.%sn%d.out' % (k, N) for N in (4, 3) for k in ('e1', 'e3')]
INPUTS += [W + '/pk25/nu/nu_reader_v1_1.py']
CERTS = [(W + '/pk25/mr/v3/MR_LEMMAP.kv', W + '/pk25/mr/MANIFEST_C6A_CERT_v3.sha256', W + '/pk25'),
         (W + '/pk25/c10/C10_RECORD_v1.kv', W + '/pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256', W + '/pk25'),
         (W + '/pk25/mr/v4/MR_SPECTRAL.kv', W + '/pk25/mr/MANIFEST_MR_V4_CERT_v1.sha256', W + '/pk25')]


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    if len(sys.argv) not in (2, 5) or not re.fullmatch(r'kt_p2_v2_3(_[1-9][0-9]?)?\.py', sys.argv[1]):
        print('usage: make_kt_p2_v2_3.py kt_p2_v2_3[_<n>].py [<NU record> <its manifest> <its producer>] (paths relative to code/)')
        return 2
    dst = W + '/pk25/p2/' + sys.argv[1]
    if os.path.exists(dst):
        print('STOP: %s exists' % dst)
        return 6
    if len(sys.argv) == 2:
        nu_rec = nu_mani = nu_code = None
        inputs, certs = list(INPUTS), list(CERTS)
    else:
        nu_rec, nu_mani, nu_code = (os.path.normpath(W + '/' + a) for a in sys.argv[2:5])
        for p in (nu_rec, nu_mani, nu_code):
            if not (p.startswith(W + '/') and os.path.isfile(p)):
                print('STOP: %s is not a file under code/' % p)
                return 6
        if not os.path.realpath(nu_rec).startswith(os.path.realpath(W + '/pk24/nu') + '/'):
            print('STOP: the NU record is not under pk24/nu/')
            return 6
        inputs = INPUTS + [nu_rec, nu_code]
        certs = CERTS + [(nu_rec, nu_mani, W), (nu_code, nu_mani, W)]
    if len(set(inputs)) != len(inputs):
        print('STOP: an input is listed twice')
        return 6
    for p, m, base in certs:
        mani = dict((ln.split()[1], ln.split()[0]) for ln in open(m).read().splitlines() if ln.strip())
        rel = os.path.relpath(p, base)
        if mani.get(rel) != sha(p):
            print('STOP: %s does not carry the sha256 its manifest %s lists' % (rel, os.path.basename(m)))
            return 6
    tmpl = open(SRC).read()
    for mk in ('# @@PINS@@', '@@NAME@@', '@@NU_PATH@@', '@@NU_CODE@@'):
        if mk not in tmpl:
            print('STOP: template mark %s missing' % mk)
            return 6
    if any(tmpl.count(mk) != 1 for mk in ('# @@PINS@@', '@@NU_PATH@@', '@@NU_CODE@@')):
        print('STOP: a single-use mark appears more than once')
        return 6
    text = tmpl.replace('# @@PINS@@', '\n'.join("    '%s': '%s'," % (p, sha(p)) for p in inputs)).replace('@@NAME@@', sys.argv[1])
    text = text.replace('@@NU_PATH@@', 'None' if nu_rec is None else "CODEDIR + '/%s'" % os.path.relpath(nu_rec, W))
    text = text.replace('@@NU_CODE@@', 'None' if nu_code is None else "CODEDIR + '/%s'" % os.path.relpath(nu_code, W))
    if '@@' in text:
        print('STOP: a template mark is left')
        return 6
    ast.parse(text)
    with open(dst, 'x') as fh:
        fh.write(text)
    print('MAKER %s sha256 %s' % (os.path.basename(__file__), sha(os.path.abspath(__file__))))
    print('TEMPLATE %s sha256 %s' % (os.path.relpath(SRC, W), sha(SRC)))
    if nu_rec is None:
        print('NU none: NU_PATH = NU_CODE = None (a nonzero delta is refused)')
    else:
        print('NU %s sha256 %s; producer %s sha256 %s (manifest %s %s)' % (os.path.relpath(nu_rec, W), sha(nu_rec), os.path.relpath(nu_code, W),
                                                                          sha(nu_code), os.path.relpath(nu_mani, W), sha(nu_mani)[:8]))
    print('PINS %d: %s' % (len(inputs), ', '.join('%s %s' % (os.path.relpath(p, W), sha(p)[:8]) for p in inputs)))
    print('ENGINE %s sha256 %s lines %d' % (os.path.relpath(dst, W), sha(dst), text.count('\n')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
