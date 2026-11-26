#!/usr/bin/env python3
"""make_kt_s9h_ins_v2_4.py (pk25; the rows 4426, 4491): builds asm/<argv[1]> from asm/src/kt_s9h_ins_v2_4.py.in (jobs/job151 from job148's splice of
the certified kt_s9h_ins_v2_2.py) and the paths file argv[2] (asm/src/pevb_paths_*.txt: six lines 'N FAMILY RECORD ASM_OUTPUT', paths relative
to code, N in {4, 3}, FAMILY in {L, LH, LT}). It fills @@NAME@@, the PEVB dict (absolute paths) and the '# @@PINS_B@@' line with the pins of
the twelve files and of pk25/rho/RHO_RECORD_v1.kv, computed from the live files; the rho record must carry the sha256 its manifest
rho/MANIFEST_RHO_V1_1.sha256 lists. kt_s9h_ins_v2_4[_<n>].py takes pk23's files only (every path under pk23/pev/); a
kt_s9h_ins_v2_4_mock<n>.py test build takes pk25's mock files only (every path under pk25/asm/mock_pevb/) and is never run in cert mode.
Parses the result with ast and writes it with open(..., 'x'). No compute."""
import ast
import hashlib
import os
import re
import sys

W = '/mnt/g2/release/root/code'
SRC = W + '/pk25/asm/src/kt_s9h_ins_v2_4.py.in'
RHOREC = W + '/pk25/rho/RHO_RECORD_v1.kv'
RHOMANI = W + '/pk25/rho/MANIFEST_RHO_V1_1.sha256'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    if len(sys.argv) != 3 or not re.fullmatch(r'kt_s9h_ins_v2_4(_[1-9][0-9]?|_mock[1-9])?\.py', sys.argv[1]):
        print('usage: make_kt_s9h_ins_v2_4.py kt_s9h_ins_v2_4[_<n>|_mock<n>].py PATHS_FILE')
        return 2
    mock = '_mock' in sys.argv[1]
    dst = W + '/pk25/asm/' + sys.argv[1]
    if os.path.exists(dst):
        print('STOP: %s exists' % dst)
        return 6
    root = W + ('/pk25/asm/mock_pevb/' if mock else '/pk23/pev/')
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
    mani = dict((ln.split()[1], ln.split()[0]) for ln in open(RHOMANI).read().splitlines() if ln.strip())
    if mani.get('rho/RHO_RECORD_v1.kv') != sha(RHOREC):
        print('STOP: the rho record does not carry the sha256 of %s' % os.path.basename(RHOMANI))
        return 6
    tmpl = open(SRC).read()
    for mk in ('@@NAME@@', '@@PEVB@@', '# @@PINS_B@@'):
        if mk not in tmpl:
            print('STOP: template mark %s missing' % mk)
            return 6
    if tmpl.count('# @@PINS_B@@') != 1 or tmpl.count('@@PEVB@@') != 1:
        print('STOP: a single-use mark appears more than once')
        return 6
    lit = '{%s}' % ', '.join('%d: {%s}' % (N, ', '.join("'%s': ('%s', '%s')" % (fam, pevb[N][fam][0], pevb[N][fam][1]) for fam in ('L', 'LH', 'LT')))
                              for N in (4, 3))
    files = []
    for p in [p for N in (4, 3) for fam in ('L', 'LH', 'LT') for p in pevb[N][fam]] + [RHOREC]:
        if p not in files:   # one asm output may name several records
            files.append(p)
    pins = '\n'.join("    '%s': '%s'," % (p, sha(p)) for p in files)
    text = tmpl.replace('@@PEVB@@', lit).replace('# @@PINS_B@@', pins).replace('@@NAME@@', sys.argv[1])
    if '@@' in text:
        print('STOP: a template mark is left')
        return 6
    ast.parse(text)
    with open(dst, 'x') as fh:
        fh.write(text)
    print('MAKER %s sha256 %s' % (os.path.basename(__file__), sha(os.path.abspath(__file__))))
    print('TEMPLATE %s sha256 %s' % (os.path.relpath(SRC, W), sha(SRC)))
    print('PATHS %s sha256 %s (%s)' % (os.path.relpath(os.path.abspath(sys.argv[2]), W), sha(sys.argv[2]), 'MOCK test build' if mock else "pk23's records"))
    print('PINS_B %d: %s' % (len(files), ', '.join('%s %s' % (os.path.relpath(p, W), sha(p)[:8]) for p in files)))
    print('ENGINE %s sha256 %s lines %d' % (os.path.relpath(dst, W), sha(dst), text.count('\n')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
