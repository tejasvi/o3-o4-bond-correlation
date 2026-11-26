#!/usr/bin/env python3
"""make_kt_s9h_asm_v1_3.py (pk25, C6a v3, main row 4363): make_kt_s9h_asm_v1_2.py with the template asm/src/kt_s9h_asm_v1_4b.py.in; v1_2: v1_1 with
asm/src/kt_s9h_asm_v1_4.py.in (the law-based computation intersected with v2's) and the law-certificate inputs pinned. Its text follows.
make_kt_s9h_asm_v1_1.py (pk25, G5 item C6a): make_kt_s9h_asm_v1.py (frozen) with the template asm/src/kt_s9h_asm_v1_3.py.in (the
canonical orientation of the P0_LOG line 4089) and output names kt_s9h_asm_v1_3 and up. make_kt_s9h_asm_v1.py's text follows.
make_kt_s9h_asm_v1.py (pk25, G5 item C6a): builds asm/kt_s9h_asm_v1.py from asm/src/kt_s9h_asm_v1.py.in and R4
(pk15/kt_p2_assembly_v1_37_1.py, read only, sha256 prefix f40a0d1e checked). It copies, by ast source segment, R4's defs in the
dependency closure of ROOTS (in R4's order) and the module-level constants CONSTS; checks that every free module-level name of the copied
defs is a copied constant, a name the template defines (PROVIDED) or an import (IMPORTS); computes the pins of every input from the live
files and requires the files R4 also pins to carry R4's pins; writes the engine with open(..., 'x') and prints its sha256. No compute."""
import ast
import hashlib
import os
import re
import sys

W = '/mnt/g2/release/root/code'
R4 = W + '/pk15/kt_p2_assembly_v1_37_1.py'
R4_PREFIX = 'e92342b0'
SRC = W + '/pk25/asm/src/kt_s9h_asm_v1_8.py.in'   # make_kt_s9h_asm_v1_8: the C6a v1_8 template (jobs/job137); pins as make_kt_s9h_asm_v1_3 with the M1 engine v1_8_4 and the mr/v3 records
DST = None   # main(): pk25/asm/<argv[1]>, kt_s9h_asm_v1[_<n>].py, a new file
ROOTS = ('Refused', 'read_grid', 'tball', 'grid_j', 't_ends', 'q2arb', 'load_ritz', 'entry_piece', 'mhat_ball', 'ritz_piece', 'lemma_a_cbar',
         'load_m2b', 'm2b_eps', 'm2b_call', 'm2b_mhat_coeffs', 'load_m4', 'm4_law', 'dec_hi', 'dec_lo', 'sha_file', 'lines_of', 'gate', 'plant',
         'out', 'check_s9_trial', 'load_m3', 'check_tau_trial')
CONSTS = ('CODEDIR', 'GRID', 'G00_CLAIM', 'VACRES', 'C1_CLAIM', 'M2B', 'M2B_READER_PATH', 'M2B_PREC', 'M4', 'M4_READER_PATH', 'M4_PREC', 'S67',
          'S67_READER_PATH', 'S67_SCRIPT', 'REVEN,RPE', 'RITZ_KEYS', 'S9_RECORDS', 'TS_FILES', 'M3_READER_PATH', 'KERNEL_SHA', 'KERNEL_LINE',
          'M3_READER_SHA', 'BADWORDS')
PROVIDED = ('FH', 'PINS', 'M_RITZ')
IMPORTS = ('Fraction', 'arb', 'arb_mat', 'ctx', 'hashlib', 'json', 'math', 'os', 're')
NEW_INPUTS = ('/pk15/kt_p2_assembly_v1_37_1.py', '/pk24/mr_engine/kt_mr_assembly_v1_8_4.py', '/pk25/mr/v3/MR_SPECTRAL.kv',
              '/pk25/mr/v3/MR_LEMMAP.kv', '/pk21/p2/s4c/S4C_TIGHT_RECORD_v1_1.md',
              '/pk21/p2/s4c/MANIFEST_S4C_TIGHT_RECORD_v1_1.sha256', '/pk21/p2/s4c/out/tau4_kt_s9h_tau4_pk21_v1_N4.tsv',
              '/pk21/p2/s4c/out/tau4_kt_s9h_tau4_pk21_v1_N3.tsv', '/pk03/out/m3_s8v3_E2_N4_J300_v1_8_1.json',
              '/pk03/out/m3_s8v3_E2_N3_J300_v1_8_1.json', '/pk03/out/m3_s8v3_FF_N4_J300_v1_8_1.json',
              '/pk03/out/m3_s8v3_FF_N3_J300_v1_8_1.json', '/pk03/out/m3_endw_N4_J300_v1_7.json', '/pk03/out/m3_endw_N3_J300_v1_7.json',
              '/pk25/m3/m3_reader_s9h_v1.py', '/pk03/out/m3_s8v3_E3_N4_J300_v1_8_1.json', '/pk03/out/m3_s8v3_E3_N3_J300_v1_8_1.json',
              '/pk03/out/m3_lawcert_v1_1_N4.json', '/pk03/out/m3_lawcert_v1_1_4.out', '/pk03/out/m3_lawcert_v1_1_N3.json',
              '/pk03/out/m3_lawcert_v1_1_3.out', '/pk03/out/m3_lawcert_v1_2_N4.json', '/pk03/out/m3_lawcert_v1_2_4.out',
              '/pk03/out/m3_lawcert_v1_2_N3.json', '/pk03/out/m3_lawcert_v1_2_3.out')
SHARED_INPUTS = ('/pk07/out/export_kt_s67_cert_v2_2_sweep.kv', '/pk03/m3_reader_v4_4.py', '/pk11/out/vacres_K3_N4_sym_v1.json',
                 '/pk11/out/vacres_K3_N3_sym_v1.json', '/pk02/M2B_KV_v1.txt', '/pk02/out/out_m2b_asm_v1.out', '/pk02/m2b_reader_v1.py',
                 '/pk15/mocks/mock_ritz_entries_v1.kv', '/pk11/out/ts_N4_J170_D_S_z9sym_v1.json', '/pk11/out/ts_N3_S_z9sym_v1.json',
                 '/pk03/out/m3_s9_N4_J300_v1_8_3.json', '/pk03/out/m3_run_v1_8_3_asm9.4.out', '/pk03/out/m3_s9_N3_J300_v1_8_3.json',
                 '/pk03/out/m3_run_v1_8_3_asm9.3.out', '/pk15/M4_KV_v1.txt', '/pk15/out/out_m4_asm_v1.out', '/pk15/m4_reader_v1.py',
                 '/pk07/out/export_kt_s9h_v1_2_vsweep.kv', '/pk07/out/out_kt_s9h_v1_2_vsweep.out', '/pk07/kt_s67_export_reader_v2_1.py',
                 '/pk07/kt_s9h_v1_2.py', '/pk03/out/m3_run_v1_8_1_asmP.4.out', '/pk03/out/m3_run_v1_8_1_asmP.3.out',
                 '/pk03/out/m3_s8v3_D_N4_J300_v1_8_1.json', '/pk03/out/m3_s8v3_D_N3_J300_v1_8_1.json',
                 '/pk03/out/m3_s8v3_N_N4_J300_v1_8_2.json', '/pk03/out/m3_run_v1_8_2_asmN.4.out',
                 '/pk03/out/m3_s8v3_N_N3_J300_v1_8_2.json', '/pk03/out/m3_run_v1_8_2_asmN.3.out')


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    global DST
    if len(sys.argv) != 2 or not re.fullmatch(r'kt_s9h_asm_v1_([3-9]|[1-9][0-9])\.py', sys.argv[1]):
        print('usage: make_kt_s9h_asm_v1_3.py kt_s9h_asm_v1_<n>.py (n >= 3)')
        return 2
    DST = W + '/pk25/asm/' + sys.argv[1]
    if os.path.exists(DST):
        print('STOP: %s exists' % DST)
        return 6
    r4sha = sha(R4)
    if not r4sha.startswith(R4_PREFIX):
        print('STOP: R4 sha256 %s' % r4sha[:8])
        return 6
    src = open(R4).read()
    tree = ast.parse(src)
    defs, assigns, imports, count = {}, {}, set(), {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            defs[n.name] = n
            count[n.name] = count.get(n.name, 0) + 1
        elif isinstance(n, ast.Assign):
            names = []
            for t in n.targets:
                for x in ast.walk(t):
                    if isinstance(x, ast.Name):
                        names.append(x.id)
            key = ','.join(names)
            assigns[key] = n
            count['=' + key] = count.get('=' + key, 0) + 1
            for x in names:
                count['name:' + x] = count.get('name:' + x, 0) + 1
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                imports.add((a.asname or a.name).split('.')[0])
    seen, stack, free = set(), list(ROOTS), set()
    while stack:
        f = stack.pop()
        if f in seen:
            continue
        if f not in defs:
            print('STOP: root or callee %s is not a module-level def of R4' % f)
            return 6
        seen.add(f)
        for x in ast.walk(defs[f]):
            if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load):
                if x.id in defs:
                    stack.append(x.id)
                elif any(x.id in k.split(',') for k in assigns) or x.id in imports:
                    free.add(x.id)
    order = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in seen]
    dupd = [f for f in order if count[f] != 1]
    cnames = set(x for c in CONSTS for x in c.split(','))
    dupc = [c for c in CONSTS if count.get('=' + c) != 1 or any(count.get('name:' + x) != 1 for x in c.split(','))]
    missing = sorted(free - cnames - set(PROVIDED) - set(IMPORTS))
    if dupd or dupc or missing or any(c not in assigns for c in CONSTS):
        print('STOP: duplicated defs %s, duplicated or missing constants %s, uncovered free names %s' % (dupd, dupc, missing))
        return 6
    cseg = [ast.get_source_segment(src, assigns[c]) for c in sorted(CONSTS, key=lambda c: assigns[c].lineno)]
    dseg = [ast.get_source_segment(src, defs[f]) for f in order]
    r4pins = None
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'PINS':
            r4pins = ast.literal_eval(n.value)
    pins = {}
    for rel in SHARED_INPUTS:
        p = W + rel
        h = sha(p)
        if r4pins.get(p) != h:
            print('STOP: %s sha256 %s is not R4\'s pin %s' % (rel, h[:8], str(r4pins.get(p))[:8]))
            return 6
        pins[p] = h
    for rel in NEW_INPUTS:
        pins[W + rel] = sha(W + rel)
    pin_lines = '\n'.join("    '%s': '%s'," % (p, pins[p]) for p in sorted(pins))
    tmpl = open(SRC).read()
    marks = ('# @@CORE_CONSTS@@', '@@R4_SHA@@', '@@CORE_DEFS@@', '@@CORE_CONSTS_NAMES@@', '# @@PINS@@', '# @@CORE_DEFS_BLOCK@@')
    for m in marks:
        if tmpl.count(m) != 1:
            print('STOP: template mark %s appears %d times' % (m, tmpl.count(m)))
            return 6
    const_names = tuple(sorted(CONSTS, key=lambda c: assigns[c].lineno))
    text = (tmpl.replace('# @@CORE_DEFS_BLOCK@@', '\n\n'.join(dseg)).replace('# @@CORE_CONSTS@@', '\n'.join(cseg))
            .replace('@@CORE_CONSTS_NAMES@@', repr(const_names)).replace('@@CORE_DEFS@@', repr(tuple(order)))
            .replace('@@R4_SHA@@', r4sha).replace('# @@PINS@@', pin_lines).replace('@@NAME@@', sys.argv[1]))
    if '@@' in text.replace("'@@'", ''):
        print('STOP: a template mark is left')
        return 6
    ast.parse(text)
    with open(DST, 'x') as fh:
        fh.write(text)
    print('MAKER %s sha256 %s' % (os.path.basename(__file__), sha(os.path.abspath(__file__))))
    print('TEMPLATE %s sha256 %s' % (os.path.relpath(SRC, W), sha(SRC)))
    print('R4 %s sha256 %s' % (os.path.relpath(R4, W), r4sha))
    print('CORE defs %d (%d lines): %s' % (len(order), sum(defs[f].end_lineno - defs[f].lineno + 1 for f in order), ' '.join(order)))
    print('CORE constants %d: %s' % (len(const_names), ' '.join(const_names)))
    print('FREE names of the defs %d: %s' % (len(free), ' '.join(sorted(free))))
    print('PINS %d (%d shared with R4, equal to R4\'s pins)' % (len(pins), len(SHARED_INPUTS)))
    print('ENGINE %s sha256 %s lines %d' % (os.path.relpath(DST, W), sha(DST), text.count('\n')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
