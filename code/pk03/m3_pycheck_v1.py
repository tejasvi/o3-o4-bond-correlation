#!/usr/bin/env python3
"""m3_pycheck_v1.py -- pk03 (code/pk03/). Compile-only check of this folder's scripts: reads each FILE argument (it must lie in
pk03/), compiles its text with compile(..., 'exec') (no import, no execution, no .pyc), and scans it for a *_series( call (the
python-flint rule). Writes nothing. PLANT-COMPILE: the first file's text with an unmatched '(' appended must fail to compile;
PLANT-SERIES: that text with 'x = acb_series(1)' appended must be flagged. Prints one line per file and VERDICT VALID or INVALID.
Run: OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B m3_pycheck_v1.py FILE...
"""
import os, re, sys

OWN = '/mnt/g2/release/root/code/pk03'
SER = re.compile(r'[A-Za-z0-9]_series\s*\(')


def check(path, text):
    try:
        compile(text, path, 'exec')
        comp = 'compiles'
    except SyntaxError as e:
        comp = 'SyntaxError line %s: %s' % (e.lineno, e.msg)
    hits = [i + 1 for i, ln in enumerate(text.split('\n')) if SER.search(ln)]
    return comp, hits


if len(sys.argv) < 2:
    print('usage: m3_pycheck_v1.py FILE...')
    sys.exit(2)
bad, first = [], None
for p in sys.argv[1:]:
    ap = os.path.realpath(p)
    if os.path.dirname(ap) != os.path.realpath(OWN):
        print('%s: outside %s -> REFUSED' % (p, OWN))
        bad.append(p)
        continue
    with open(ap, encoding='utf-8') as fh:
        text = fh.read()
    if first is None:
        first = (ap, text)
    comp, hits = check(ap, text)
    ok = comp == 'compiles' and not hits
    print('%s: %d lines, %s, *_series( calls at lines %s -> %s' % (os.path.basename(ap), text.count('\n'), comp, hits or 'none',
                                                                   'PASS' if ok else 'FAIL'))
    if not ok:
        bad.append(p)
nofire = []
if first is not None:
    c1, _ = check(first[0], first[1] + '\nzz = (\n')
    print('PLANT-COMPILE (an unmatched parenthesis appended): %s -> %s' % (c1, 'FIRES' if c1 != 'compiles' else 'DOES NOT FIRE'))
    if c1 == 'compiles':
        nofire.append('PLANT-COMPILE')
    _, h2 = check(first[0], first[1] + '\nx = acb_series(1)\n')
    print('PLANT-SERIES (a *_series( call appended): flagged at %s -> %s' % (h2 or 'none', 'FIRES' if h2 else 'DOES NOT FIRE'))
    if not h2:
        nofire.append('PLANT-SERIES')
print('VERDICT %s' % ('VALID' if not bad and not nofire and first is not None else
                      'INVALID (%s)' % ', '.join(bad + ['%s did not fire' % x for x in nofire] + ([] if first else ['no file']))))
