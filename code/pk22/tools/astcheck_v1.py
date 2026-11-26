#!/usr/bin/env python3
"""astcheck_v1.py (pk22): syntax check of each Python file named on the command line by ast.parse (writes nothing; never
py_compile). Prints one line per file with its sha256 and 'AST OK' or the error; exit 1 if any file fails."""
import ast, hashlib, sys
bad = 0
for p in sys.argv[1:]:
    with open(p, 'rb') as fh:
        b = fh.read()
    try:
        ast.parse(b.decode('utf-8'), p)
        print('AST OK %s %s' % (hashlib.sha256(b).hexdigest(), p))
    except SyntaxError as e:
        bad += 1
        print('AST FAIL %s %s: %s' % (hashlib.sha256(b).hexdigest(), p, e))
sys.exit(1 if bad else 0)
