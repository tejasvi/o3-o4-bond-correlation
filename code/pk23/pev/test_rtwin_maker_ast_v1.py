#!/usr/bin/env python3
"""test_rtwin_maker_ast_v1.py (pk23, Pev entries): ast.parse of the file make_rtwin_hl_v1.py would write, before the twin pieces exist.
Takes HEAD and TAIL from the maker's AST (string constants), puts in placeholder piece names and one placeholder pin, adds the C-COPY
block (pk22's rtwin_c3h_v1.py l.105-204, read-only) as the maker does, and parses the result; writes nothing.
Usage: test_rtwin_maker_ast_v1.py MAKER"""
import ast, hashlib, sys
src = open(sys.argv[1]).read()
consts = {}
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('HEAD', 'TAIL'):
        consts[node.targets[0].id] = node.value.value
c3h = open('/mnt/g2/release/root/code/pk22/m3/rtwin_c3h_v1.py', 'rb').read().split(b'\n')
block = c3h[104:204]
head = consts['HEAD'].replace('@@P4@@', 'm3ref_hl_v1_P16L.4.p9_z9sym.out').replace('@@P3@@', 'm3ref_hl_v1_P16L.3.p9_z9sym.out')
text = head.encode('utf-8') + b"    '/x': 'y'," + b'\n# C-COPY block: rtwin_c3h_v1.py l.105-204\n' + b'\n'.join(block) + b'\n# C-COPY end\n' + consts['TAIL'].encode('utf-8')
try:
    ast.parse(text.decode('utf-8'))
    print('GENERATED AST OK (%d bytes, sha256 %s of the test text; maker %s)' % (len(text), hashlib.sha256(text).hexdigest()[:8],
                                                                              hashlib.sha256(src.encode('utf-8')).hexdigest()[:8]))
except SyntaxError as e:
    print('GENERATED AST FAIL: %s' % e)
    sys.exit(1)
