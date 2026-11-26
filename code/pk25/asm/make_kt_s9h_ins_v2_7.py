#!/usr/bin/env python3
"""make_kt_s9h_ins_v2_7.py (pk25; P4, the rows 4640, 4644, 4672; make_kt_s9h_ins_v2_5.py with the names moved to v2_7): builds
asm/<argv[1]> from asm/src/kt_s9h_ins_v2_7.py.in (v2_5's template with C-MAIN-N; v2_4's with route (B) way A on the last h row),the paths file argv[2] (asm/src/pevb_paths_*.txt: six lines 'N FAMILY RECORD ASM_OUTPUT', paths relative
to code, N in {4, 3}, FAMILY in {L, LH, LT}, every path under pk23/pev/), and P2's record argv[3] with its manifest argv[4] (relative to
code; the record under pk25/p2/). It fills @@NAME@@, the PEVB dict, @@P2REC@@, the '# @@PINS_B@@' line (the twelve pk23 files and
pk25/rho/RHO_RECORD_v1.kv) and the '# @@PINS_C@@' line (P2's record, pk25/c10/C10_RECORD_v1.kv, pk25/P4_LEMMA_NOTE_v1_1.md), each pin
computed from the live file; the rho record, the C10 record, the lemma note and P2's record must carry the sha256 their manifests list.
kt_s9h_ins_v2_7.py (the cert engine) takes a P2 record with STATUS = CERTIFIED only; a numbered build kt_s9h_ins_v2_7_<n>.py may take a
DRY one (its cert mode then refuses at C-WAYA-IN). Parses the result with ast and writes it with open(..., 'x'). No compute."""
import ast
import hashlib
import os
import re
import sys

W = '/mnt/g2/release/root/code'
SRC = W + '/pk25/asm/src/kt_s9h_ins_v2_7.py.in'
RHOREC = W + '/pk25/rho/RHO_RECORD_v1.kv'
RHOMANI = W + '/pk25/rho/MANIFEST_RHO_V1_1.sha256'
C10REC = W + '/pk25/c10/C10_RECORD_v1.kv'
C10MANI = W + '/pk25/c10/MANIFEST_C10_V1_3_CERT_c1.sha256'
P4NOTE = W + '/pk25/P4_LEMMA_NOTE_v1_1.md'
P4MANI = W + '/pk25/MANIFEST_P4_LEMMA_NOTE_v1_1.sha256'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def listed(path, mani):
    """the sha256 an pk25 manifest lists for path (pk25's manifests list paths relative to pk25/)."""
    m = dict((ln.split()[1], ln.split()[0]) for ln in open(mani).read().splitlines() if ln.strip())
    return m.get(os.path.relpath(path, W + '/pk25'))


def main():
    if len(sys.argv) != 5 or not re.fullmatch(r'kt_s9h_ins_v2_7(_[1-9][0-9]?)?\.py', sys.argv[1]):
        print('usage: make_kt_s9h_ins_v2_7.py kt_s9h_ins_v2_7[_<n>].py PATHS_FILE P2_RECORD P2_MANIFEST')
        return 2
    dst = W + '/pk25/asm/' + sys.argv[1]
    if os.path.exists(dst):
        print('STOP: %s exists' % dst)
        return 6
    root = W + '/pk23/pev/'
    pevb = {4: {}, 3: {}}
    for ln in open(sys.argv[2]).read().splitlines():
        if not ln.strip() or ln.startswith('#'):
            continue
        f = ln.split()
        if len(f) != 4 or f[0] not in ('4', '3') or f[1] not in ('L', 'LH', 'LT'):
            print('STOP: paths line %r' % ln)
            return 6
        rp, ap = W + '/' + f[2], W + '/' + f[3]
        for p in (rp, ap):
            if not (os.path.isfile(p) and os.path.realpath(p).startswith(os.path.realpath(root))):
                print('STOP: %s is not a file under %s' % (p, root))
                return 6
        if f[1] in pevb[int(f[0])]:
            print('STOP: N %s family %s given twice' % (f[0], f[1]))
            return 6
        pevb[int(f[0])][f[1]] = (rp, ap)
    if any(sorted(pevb[N]) != ['L', 'LH', 'LT'] for N in (4, 3)):
        print('STOP: the paths file must give L, LH and LT for N = 4 and 3')
        return 6
    p2, p2m = os.path.normpath(W + '/' + sys.argv[3]), os.path.normpath(W + '/' + sys.argv[4])
    if not (os.path.isfile(p2) and os.path.isfile(p2m) and os.path.realpath(p2).startswith(os.path.realpath(W + '/pk25/p2') + '/')):
        print('STOP: the P2 record or its manifest is missing, or the record is not under pk25/p2/')
        return 6
    for path, mani in ((RHOREC, RHOMANI), (C10REC, C10MANI), (P4NOTE, P4MANI), (p2, p2m)):
        if listed(path, mani) != sha(path):
            print('STOP: %s does not carry the sha256 its manifest %s lists' % (os.path.relpath(path, W), os.path.basename(mani)))
            return 6
    st = [ln.split(' = ', 1)[1] for ln in open(p2).read().splitlines() if ln.startswith('STATUS = ')]
    if len(st) != 1:
        print('STOP: the P2 record has %d STATUS lines' % len(st))
        return 6
    if sys.argv[1] == 'kt_s9h_ins_v2_7.py' and st[0] != 'CERTIFIED':
        print('STOP: the cert engine kt_s9h_ins_v2_7.py takes a CERTIFIED P2 record only (STATUS %s)' % st[0])
        return 6
    tmpl = open(SRC).read()
    for mk in ('@@NAME@@', '@@PEVB@@', '@@P2REC@@', '# @@PINS_B@@', '# @@PINS_C@@'):
        if mk not in tmpl:
            print('STOP: template mark %s missing' % mk)
            return 6
    if any(tmpl.count(mk) != 1 for mk in ('# @@PINS_B@@', '# @@PINS_C@@', '@@PEVB@@', '@@P2REC@@')):
        print('STOP: a single-use mark appears more than once')
        return 6
    lit = '{%s}' % ', '.join('%d: {%s}' % (N, ', '.join("'%s': ('%s', '%s')" % (fam, pevb[N][fam][0], pevb[N][fam][1]) for fam in ('L', 'LH', 'LT')))
                              for N in (4, 3))
    files = []
    for p in [p for N in (4, 3) for fam in ('L', 'LH', 'LT') for p in pevb[N][fam]] + [RHOREC]:
        if p not in files:   # one asm output may name several records
            files.append(p)
    files_c = [p2, C10REC, P4NOTE]
    pins_b = '\n'.join("    '%s': '%s'," % (p, sha(p)) for p in files)
    pins_c = '\n'.join("    '%s': '%s'," % (p, sha(p)) for p in files_c)
    text = tmpl.replace('@@PEVB@@', lit).replace('# @@PINS_B@@', pins_b).replace('# @@PINS_C@@', pins_c)
    text = text.replace('@@P2REC@@', "CODEDIR + '/%s'" % os.path.relpath(p2, W)).replace('@@NAME@@', sys.argv[1])
    if '@@' in text:
        print('STOP: a template mark is left')
        return 6
    ast.parse(text)
    with open(dst, 'x') as fh:
        fh.write(text)
    print('MAKER %s sha256 %s' % (os.path.basename(__file__), sha(os.path.abspath(__file__))))
    print('TEMPLATE %s sha256 %s' % (os.path.relpath(SRC, W), sha(SRC)))
    print('PATHS %s sha256 %s' % (os.path.relpath(os.path.abspath(sys.argv[2]), W), sha(sys.argv[2])))
    print('P2 %s sha256 %s STATUS %s (manifest %s %s)' % (os.path.relpath(p2, W), sha(p2), st[0], os.path.relpath(p2m, W), sha(p2m)[:8]))
    print('PINS_B %d: %s' % (len(files), ', '.join('%s %s' % (os.path.relpath(p, W), sha(p)[:8]) for p in files)))
    print('PINS_C %d: %s' % (len(files_c), ', '.join('%s %s' % (os.path.relpath(p, W), sha(p)[:8]) for p in files_c)))
    print('ENGINE %s sha256 %s lines %d' % (os.path.relpath(dst, W), sha(dst), text.count('\n')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
