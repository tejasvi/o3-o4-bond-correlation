#!/usr/bin/env python3
"""make_kt_s9h_p3_v7.py (pk25; P3 v7 for the cert, the rows 4768, 4770, 4772, the rows 4686, 4697, 4718): builds asm/<argv[1]> (kt_s9h_p3_v7[_<n>].py, a new file) from
asm/src/kt_s9h_p3_v7.py.in: the name and the pins of the inputs it reads, computed from the live files. v1's twelve inputs, and for the
Lemma D rows: P2's certified table (p2/v3f2), P1's C13 record, pk22's E4 (e4_comb_v2) and E6 (e6_comb_v3) records with the c3k entry
list and the E4N records E4 names, and the S8 law records, job outputs and law certificates with pk25's reader fork, VACRES and the trial
files. Each certified pk25 record must carry the sha256 its certification manifest lists (paths relative to pk25/); the 10' trial files,
MR_JOINT, E4 and E6 the sha256 their owners' manifests list (absolute paths there); the S8 files, the reader and VACRES the sha256 that
P2's certified engine (p2/kt_p2_v2_3.py, read by ast) pins; v3 adds pk25's NIH, NHT, DH records with their job output and certificate
m3_lawcert_s9h_v1_1 (the sha256 P4's certified engine asm/kt_s9h_ins_v2_7.py pins) and P4's certified run output (the mu tool's MU lines),
both engine and output as MR_INSERT v5b's certification manifest lists; the E4N records the sha256 that E4 names in its sources, and the entry list
the one each E4N record names. Parses the result with ast and writes it with open(..., 'x'). No compute."""
import ast
import hashlib
import json
import os
import re
import sys

W = '/mnt/g2/release/root/code'
SRC = W + '/pk25/asm/src/kt_s9h_p3_v7.py.in'
P2ENG = W + '/pk25/p2/kt_p2_v2_3.py'
M3O = W + '/pk03/out/'
E4J = dict((N, W + '/pk22/midrow/e4/out/e4_comb_v2_N%d.json' % N) for N in (4, 3))
E6J = dict((N, W + '/pk22/midrow/e6/out/e6_comb_v3_N%d.json' % N) for N in (4, 3))
E4NR = dict((N, W + '/pk22/m3/out/m3_c3kp_E4N_N%d_J300_c3kp.json' % N) for N in (4, 3))
C3KL = W + '/pk22/m3/C3K_ENTRY_LIST_v1_2.json'
S8 = []
for _N in (4, 3):
    S8 += [M3O + 'm3_s8v3_%s_N%d_J300_v1_8_1.json' % (F, _N) for F in ('D', 'E2', 'E3', 'FF')]
    S8 += [M3O + 'm3_run_v1_8_1_asmP.%d.out' % _N, M3O + 'm3_s8v3_N_N%d_J300_v1_8_2.json' % _N, M3O + 'm3_run_v1_8_2_asmN.%d.out' % _N]
    S8 += [M3O + 'm3_lawcert_v1_1_N%d.json' % _N, M3O + 'm3_lawcert_v1_1_%d.out' % _N, M3O + 'm3_lawcert_v1_2_N%d.json' % _N,
           M3O + 'm3_lawcert_v1_2_%d.out' % _N]
    S8 += [W + '/pk11/out/vacres_K3_N%d_sym_v1.json' % _N]
S8 += [W + '/pk25/m3/m3_reader_s9h_v1.py']
P4ENG = W + '/pk25/asm/kt_s9h_ins_v2_7.py'   # P4's certified engine (MR_INSERT v5b): its PINS name the h records and certificates
INSOUT = W + '/pk25/asm/out/out_kt_s9h_ins_v2_7_cert_c1.out'
HL = []
for _N in (4, 3):
    HL += [W + '/pk25/m3/out/m3_s9h_%s_N%d_J300_v1.json' % (F, _N) for F in ('NIH', 'NHT', 'DH')]
    HL += [W + '/pk25/m3/out/m3_run_s9h_v1_1_asm.%d.out' % _N, W + '/pk25/m3/out/m3_lawcert_s9h_v1_1_N%d.json' % _N,
           W + '/pk25/m3/out/m3_lawcert_s9h_v1_1_%d.out' % _N]
M4HF = [W + '/pk25/m4h/M4H_KV_v1.txt', W + '/pk25/m4h/out/out_m4h_asm_v1_1.out', W + '/pk25/m4h/m4h_reader_v1_1.py']   # P4's engine pins these
P2F = [W + '/pk02/M2B_KV_v1.txt', W + '/pk02/out/out_m2b_asm_v1.out', W + '/pk02/m2b_reader_v1.py', W + '/pk24/nu/NU_G_RECORD_v1.kv',
       W + '/pk24/nu/kt_nu_g_v1_2.py', W + '/pk25/nu/nu_reader_v1_1.py']   # P2's certified engine pins these
XRH = [W + '/pk02/out_kt_cert_v1_6_x.hn4.out', W + '/pk02/out_kt_cert_v1_6_x.hn3.out']   # M4H's PIN_X names these
E3F = [W + '/pk22/midrow/e3/out/e3_sq2_v2_N4.json', W + '/pk22/midrow/e3/out/e3_sq2_v2_N3.json']   # pk22's certified E3 v2 (frozen by job305)
PV = M4HF + P2F + XRH + E3F
INPUTS = [W + '/pk25/mr/v4/MR_SPECTRAL.kv', W + '/pk25/mr/v5b/MR_INSERT.kv', W + '/pk25/mr/v4/MR_CRUDEX.kv',
          W + '/pk24/mr_engine/kt_mr_assembly_v1_8_4.py', W + '/pk25/mr/v3/MR_LEMMAP.kv', W + '/pk25/c10/C10_RECORD_v1.kv',
          W + '/pk11/out/ts_N4_J170_D_S_z9sym_v1.json', W + '/pk11/out/ts_N3_S_z9sym_v1.json',
          W + '/pk22/midrow/psixy/ts_N4_J170_D_S_z9symxyp_v1.json', W + '/pk22/midrow/psixy/ts_N3_S_z9symxyp_v1.json',
          W + '/pk22/midrow/g4/mrc/out/cert/MR_JOINT_CERT_v1.kv', W + '/pk23/cw/out/CW_X11_v2_2.kv',
          W + '/pk25/p2/v3f2/MR_LEMMAP_V3F.kv', W + '/pk25/c13/C13_RECORD_v1_1.kv', E4J[4], E4J[3], E6J[4], E6J[3], E4NR[4], E4NR[3], C3KL] + S8 + HL + [INSOUT] + PV
CERTS = [(W + '/pk25/mr/v4/MR_SPECTRAL.kv', W + '/pk25/mr/MANIFEST_MR_V4_CERT_v1.sha256', W + '/pk25'),
         (W + '/pk25/mr/v5b/MR_INSERT.kv', W + '/pk25/mr/MANIFEST_MR_V5B_CERT_v1.sha256', W + '/pk25'),
         (W + '/pk25/mr/v4/MR_CRUDEX.kv', W + '/pk25/mr/MANIFEST_MR_V4_CRUDEX_CERT_v1.sha256', W + '/pk25'),
         (W + '/pk25/mr/v3/MR_LEMMAP.kv', W + '/pk25/mr/MANIFEST_C6A_CERT_v3.sha256', W + '/pk25'),
         (W + '/pk25/c10/C10_RECORD_v1.kv', W + '/pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256', W + '/pk25'),
         (W + '/pk25/p2/v3f2/MR_LEMMAP_V3F.kv', W + '/pk25/p2/MANIFEST_P2_V2_3_CERT_c1.sha256', W + '/pk25'),
         (W + '/pk25/c13/C13_RECORD_v1_1.kv', W + '/pk25/c13/MANIFEST_C13_V1_1_CERT_c2.sha256', W + '/pk25'),
         (W + '/pk22/midrow/psixy/ts_N4_J170_D_S_z9symxyp_v1.json', W + '/pk22/midrow/psixy/MANIFEST_PSIXY_10P_v1.sha256', None),
         (W + '/pk22/midrow/psixy/ts_N3_S_z9symxyp_v1.json', W + '/pk22/midrow/psixy/MANIFEST_PSIXY_10P_v1.sha256', None),
         (W + '/pk22/midrow/g4/mrc/out/cert/MR_JOINT_CERT_v1.kv', W + '/pk22/midrow/g4/mrc/MANIFEST_MRJ_CERT_v1.sha256', None),
         (E4J[4], W + '/pk22/midrow/e4/MANIFEST_E4_COMB_v2.sha256', None), (E4J[3], W + '/pk22/midrow/e4/MANIFEST_E4_COMB_v2.sha256', None),
         (E6J[4], W + '/pk22/midrow/e6/MANIFEST_E6_v3.sha256', None), (E6J[3], W + '/pk22/midrow/e6/MANIFEST_E6_v3.sha256', None),
         (W + '/pk23/cw/out/CW_X11_v2_2.kv', W + '/pk23/cw/MANIFEST_CW_COMB_V2_2_v1.sha256', W + '/pk23'),
         (W + '/pk22/midrow/e3/out/e3_sq2_v2_N4.json', W + '/pk22/midrow/e3/MANIFEST_E3_SQ2_v2.sha256', None),
         (W + '/pk22/midrow/e3/out/e3_sq2_v2_N3.json', W + '/pk22/midrow/e3/MANIFEST_E3_SQ2_v2.sha256', None)]


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def p2_pins(path=None):
    """the PINS dict of a certified engine read by ast: P2's (the S8 files, the reader and VACRES P2 certified with) or the given one."""
    for node in ast.parse(open(P2ENG if path is None else path).read()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and getattr(node.targets[0], 'id', None) == 'PINS':
            return ast.literal_eval(node.value)
    return None


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r'kt_s9h_p3_v7(_[1-9][0-9]?)?\.py', sys.argv[1]):
        print('usage: make_kt_s9h_p3_v7.py kt_s9h_p3_v7[_<n>].py')
        return 2
    dst = W + '/pk25/asm/' + sys.argv[1]
    if os.path.exists(dst):
        print('STOP: %s exists' % dst)
        return 6
    if len(set(INPUTS)) != len(INPUTS):
        print('STOP: an input is listed twice')
        return 6
    for p, m, base in CERTS:
        mani = dict((ln.split()[1], ln.split()[0]) for ln in open(m).read().splitlines() if ln.strip())
        rel = p if base is None else os.path.relpath(p, base)
        if mani.get(rel) != sha(p):
            print('STOP: %s does not carry the sha256 its manifest %s lists' % (rel, os.path.basename(m)))
            return 6
    m2 = dict((ln.split()[1], ln.split()[0]) for ln in open(W + '/pk25/p2/MANIFEST_P2_V2_3_CERT_c1.sha256').read().splitlines() if ln.strip())
    if m2.get('p2/kt_p2_v2_3.py') != sha(P2ENG):
        print('STOP: P2\'s engine does not carry the sha256 its certification manifest lists')
        return 6
    m5 = dict((ln.split()[1], ln.split()[0]) for ln in open(W + '/pk25/mr/MANIFEST_MR_V5B_CERT_v1.sha256').read().splitlines() if ln.strip())
    if m5.get('asm/kt_s9h_ins_v2_7.py') != sha(P4ENG) or m5.get('asm/out/out_kt_s9h_ins_v2_7_cert_c1.out') != sha(INSOUT):
        print('STOP: P4\'s engine or certified run output does not carry the sha256 MR_INSERT v5b\'s certification manifest lists')
        return 6
    p4p = p2_pins(P4ENG)
    if p4p is None or any(p4p.get(p) != sha(p) for p in HL):
        print('STOP: an h record, job output or certificate is not the file P4\'s certified engine pins')
        return 6
    pp = p2_pins()
    if pp is None:
        print('STOP: no PINS in P2\'s engine')
        return 6
    for p in S8 + P2F:
        if pp.get(p) != sha(p):
            print('STOP: %s is not the file P2\'s certified engine pins' % os.path.relpath(p, W))
            return 6
    if any(p4p.get(p) != sha(p) for p in M4HF):
        print('STOP: an M4H file is not the file P4\'s certified engine pins')
        return 6
    pinx = [ln.split(' = ', 1)[1] for ln in open(M4HF[0]).read().splitlines() if ln.startswith('PIN_X = ')]
    pinx = dict(x.strip().rsplit(':', 1) for x in pinx[0].split(';')) if len(pinx) == 1 else {}
    if any(pinx.get(os.path.relpath(p, W)) != sha(p) for p in XRH):
        print('STOP: an h x record is not the file M4H_KV_v1\'s PIN_X names')
        return 6
    for N in (4, 3):
        with open(E4J[N]) as fh:
            e4 = json.load(fh)
        src = e4.get('sources', {}).get('E4N', {})
        if src.get('file') != os.path.relpath(E4NR[N], W) or src.get('sha256') != sha(E4NR[N]):
            print('STOP: E4 N%d does not name the E4N record %s with its sha256' % (N, os.path.basename(E4NR[N])))
            return 6
        with open(E4NR[N]) as fh:
            rn = json.load(fh)
        if rn.get('entry_list') != '%s:%s' % (os.path.basename(C3KL), sha(C3KL)):
            print('STOP: the E4N record N%d does not name the entry list with its sha256' % N)
            return 6
    tmpl = open(SRC).read()
    for mk in ('# @@PINS@@', '@@NAME@@'):
        if mk not in tmpl:
            print('STOP: template mark %s missing' % mk)
            return 6
    if tmpl.count('# @@PINS@@') != 1:
        print('STOP: the PINS mark appears more than once')
        return 6
    text = tmpl.replace('# @@PINS@@', '\n'.join("    '%s': '%s'," % (p, sha(p)) for p in INPUTS)).replace('@@NAME@@', sys.argv[1])
    if '@@' in text:
        print('STOP: a template mark is left')
        return 6
    ast.parse(text)
    with open(dst, 'x') as fh:
        fh.write(text)
    print('MAKER %s sha256 %s' % (os.path.basename(__file__), sha(os.path.abspath(__file__))))
    print('TEMPLATE %s sha256 %s' % (os.path.relpath(SRC, W), sha(SRC)))
    print('PINS %d: %s' % (len(INPUTS), ', '.join('%s %s' % (os.path.relpath(p, W), sha(p)[:8]) for p in INPUTS)))
    print('ENGINE %s sha256 %s lines %d' % (os.path.relpath(dst, W), sha(dst), text.count('\n')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
