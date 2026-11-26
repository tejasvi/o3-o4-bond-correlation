#!/usr/bin/env python3
"""make_kt_nu_g_v1_2.py (pk24; make_kt_nu_g_v1.py with the v1_2 head, main and output names): builds pk24/nu/kt_nu_g_v1_2.py from nu/src/nu_head_v1_2.py, the verbatim ast source segments of the pinned
pk02/kt_cert_v1_9.py (statements, then functions, then the statements that call them), and nu/src/nu_main_v1_2.py. The lists of copied
names must equal CORE_FUNCS and CORE_STMTS of the main part (the tool's C-CORE re-checks every segment at run time). Mode 'x'."""
import ast, hashlib, os, sys

W18 = '/mnt/g2/release/root/code'
KT = W18 + '/pk02/kt_cert_v1_9.py'
HEAD = W18 + '/pk24/nu/src/nu_head_v1_2.py'
MAIN = W18 + '/pk24/nu/src/nu_main_v1_2.py'
OUT = W18 + '/pk24/nu/kt_nu_g_v1_2.py'
STMTS1 = ('SQ5, SQ21', 'A_', 'B_', 'TRI', 'PAIRS', 'BASIS', 'RHO_M, RHO_E', 'KX, NVX', 'XS, QS, XD, QD', 'Series, padd, pscale, pmul, pconst, pvar',
          'WX')
FUNCS = ('up_float', 'nsqrt', 'lap_a', 'gauge_basis_a', 'surely_pd', 'tilted_cov_a', 'sub_mat', 'ser', 'zero', 'one', 'anh', 'xi_pair', 'xis',
         'mono_series', 'shift', 'vac_poly', 'state_poly', 'restrict6')
STMTS2 = ('a_m, a_e', 'c_m, c_e', 'ED_', 'LD', 'BD')


def sha(b):
    return hashlib.sha256(b).hexdigest()


kraw = open(KT, 'rb').read()
assert sha(kraw).startswith('6305ef1b'), sha(kraw)[:8]
src = kraw.decode('utf-8')
tree = ast.parse(src)
funcs, stmts = {}, {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        funcs.setdefault(node.name, []).append(ast.get_source_segment(src, node))
    elif isinstance(node, ast.Assign) and len(node.targets) == 1:
        stmts.setdefault(ast.get_source_segment(src, node.targets[0]), []).append(ast.get_source_segment(src, node))
for n in FUNCS:
    assert len(funcs.get(n, [])) == 1, ('function', n, len(funcs.get(n, [])))
for n in STMTS1 + STMTS2:
    assert len(stmts.get(n, [])) == 1, ('statement', n, len(stmts.get(n, [])))
main_txt = open(MAIN).read()
mtree = ast.parse(main_txt)
lists = {}
for node in mtree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('CORE_FUNCS',
                                                                                                                                    'CORE_STMTS'):
        lists[node.targets[0].id] = ast.literal_eval(node.value)
assert lists.get('CORE_FUNCS') == FUNCS, 'CORE_FUNCS differs'
assert lists.get('CORE_STMTS') == STMTS1 + STMTS2, 'CORE_STMTS differs'
head = open(HEAD).read()
body = (head.rstrip('\n') + '\n\n\n# ' + '=' * 86 + ' verbatim ast source segments of pk02/kt_cert_v1_9.py\n# (sha256 %s;\n'
        '# statements, functions, then the statements that call them; C-CORE re-checks each)\n' % sha(kraw)
        + '\n'.join(stmts[n][0] for n in STMTS1) + '\n\n\n' + '\n\n\n'.join(funcs[n][0] for n in FUNCS) + '\n\n\n'
        + '\n'.join(stmts[n][0] for n in STMTS2) + '\n' + main_txt)
ast.parse(body)
assert not os.path.exists(OUT)
with open(OUT, 'x') as fh:
    fh.write(body)
print('MADE %s %s (%d lines; %d functions, %d statements copied; head %s, main %s)' % (
    sha(body.encode()), OUT.replace(W18 + '/', ''), body.count('\n'), len(FUNCS), len(STMTS1 + STMTS2), sha(open(HEAD, 'rb').read())[:8],
    sha(open(MAIN, 'rb').read())[:8]))
