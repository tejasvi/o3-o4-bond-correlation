#!/usr/bin/env python3
"""astcheck_v1.py (pk23): syntax check of the given python files by ast.parse only (never py_compile); prints one line per file
with its sha256 and OK or the SyntaxError, and exits 1 if any file fails. Usage: astcheck_v1.py FILE [FILE ...]"""
import ast, hashlib, sys

bad = 0
for p in sys.argv[1:]:
    with open(p, 'rb') as fh:
        b = fh.read()
    h = hashlib.sha256(b).hexdigest()
    try:
        ast.parse(b.decode('utf-8'), filename=p)
        print('AST OK %s %s' % (h[:8], p))
    except SyntaxError as e:
        bad += 1
        print('AST FAIL %s %s: %s' % (h[:8], p, e))
print('AST VERDICT %s (%d files, %d failing)' % ('PASS' if bad == 0 else 'FAIL', len(sys.argv) - 1, bad))
sys.exit(1 if bad else 0)
