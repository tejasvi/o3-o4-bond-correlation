#!/usr/bin/env python3
"""make_kt_s9h_ins_v1.py (pk25, G5 item C6b): builds asm/<argv[1]> (kt_s9h_ins_v1[_<n>].py, a new file) from asm/src/kt_s9h_ins_v1.py.in, R4
(pk15/kt_p2_assembly_v1_37_1.py, sha256 prefix f40a0d1e) and pk25's C6a engine (asm/kt_s9h_asm_v1_5.py, prefix 1704af08), both read
only. It copies, by ast source segment, R4's defs in the dependency closure of ROOTS (R4's order) with R4's constants CONSTS, and the C6a
engine's defs C6A_ROOTS with its constants C6A_CONSTS; checks that every free module-level name of the copied defs is a copied constant, a
name the template defines (PROVIDED) or an import; computes the pins of every input from the live files, requiring the files R4 also pins to
carry R4's pins; writes the engine with open(..., 'x') and prints its sha256. No compute."""
import ast
import hashlib
import os
import re
import sys

W = '/mnt/g2/release/root/code'
R4 = W + '/pk15/kt_p2_assembly_v1_37_1.py'
C6A = W + '/pk25/asm/kt_s9h_asm_v1_5.py'
SRC = W + '/pk25/asm/src/kt_s9h_ins_v2_2s.py.in'   # make_kt_s9h_ins_v2_2: the MR_INSERT v4 producer template v2_2 (jobs/job139 splice); pins as make_kt_s9h_ins_v2_1
ROOTS = ('Refused', 'read_grid', 'tball', 'grid_j', 't_ends', 'q2arb', 'load_ritz', 'entry_piece', 'mhat_ball', 'ritz_piece', 'lemma_a_cbar',
         'lemma_a_amp', 'qv4', 'tail_h', 'gbad_p', 'abad_p', 'kappa_bound', 'phi_T', 's_eps', 'load_trial_q', 'load_g00', 'check_g00', 'lg_weights',
         'na_prime', 'trial_ab', 'load_m2b', 'm2b_eps', 'm2b_call', 'm2b_mhat_coeffs', 'load_m4', 'm4_law', 'm4_call', 'dec_hi', 'dec_lo',
         'sha_file', 'lines_of', 'gate', 'plant', 'out', 'check_s9_trial', 'load_m3', 'check_tau_trial')
CONSTS = ('CODEDIR', 'GRID', 'G00_MOCK', 'G00_CLAIM', 'S7G00', 'EPS_G,THETA_G', 'VACRES', 'C1_CLAIM', 'M2B', 'M2B_READER_PATH', 'M2B_PREC', 'M4',
          'M4_READER_PATH', 'M4_PREC', 'S67', 'S67_READER_PATH', 'S67_SCRIPT', 'REVEN,RPE', 'RITZ_KEYS', 'S9_RECORDS', 'TS_FILES',
          'LAM_T,LAM_A', 'M3_READER_PATH', 'BASIS', 'KERNEL_SHA', 'KERNEL_LINE', 'M3_READER_SHA', 'BADWORDS')
C6A_ROOTS = ('segments', 'check_grid', 'orient_signs', 'check_orient', 'l3_level')
C6A_CONSTS = ('JLOW', 'KNAME')
PROVIDED = ('FH', 'PINS', 'M_RITZ')
IMPORTS = ('Fraction', 'arb', 'arb_mat', 'ctx', 'hashlib', 'json', 'math', 'os', 're', 'ast')
NEW_INPUTS = ['/pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37_1.kv', '/pk25/mu/kt_mu_hw_v1.py', '/pk15/kt_p2_assembly_v1_37_1.py', '/pk15/out/out_kt_p2_assembly_v1_37_1_cert.out', '/pk25/asm/kt_s9h_asm_v1_5.py',
              '/pk25/m3/m3_reader_s9h_v1.py', '/pk25/m4h/M4H_KV_v1.txt', '/pk25/m4h/out/out_m4h_asm_v1_1.out', '/pk25/m4h/m4h_reader_v1_1.py',
              '/pk25/mr/v3/MR_LEMMAP.kv', '/pk25/mr/v3/MR_SPECTRAL.kv', '/pk24/mr_engine/kt_mr_assembly_v1_8_4.py',
              '/pk21/p2/s4c/S4C_TIGHT_RECORD_v1_1.md', '/pk25/mu/kt_mu_hw_v1_1.py']
for _N in (4, 3):
    NEW_INPUTS += ['/pk03/out/m3_s8v3_%s_N%d_J300_v1_8_1.json' % (F, _N) for F in ('E2', 'E3', 'FF')]
    NEW_INPUTS += ['/pk03/out/m3_lawcert_v1_1_N%d.json' % _N, '/pk03/out/m3_lawcert_v1_1_%d.out' % _N,
                   '/pk03/out/m3_lawcert_v1_2_N%d.json' % _N, '/pk03/out/m3_lawcert_v1_2_%d.out' % _N]
    NEW_INPUTS += ['/pk25/m3/out/m3_s9h_%s_N%d_J300_v1.json' % (F, _N) for F in ('NIH', 'NHT', 'DH')]
    NEW_INPUTS += ['/pk25/m3/out/m3_run_s9h_v1_1_asm.%d.out' % _N, '/pk25/m3/out/m3_lawcert_s9h_v1_1_N%d.json' % _N,
                   '/pk25/m3/out/m3_lawcert_s9h_v1_1_%d.out' % _N]
    NEW_INPUTS += ['/pk22/m3/out/m3_c3j_DJ_N%d_J300_c3j.json' % _N, '/pk22/m3/out/m3_run_v1_9_3_asm.%d_c3j.out' % _N]   # v1_5: pk22's DHT entries
    NEW_INPUTS += ['/pk01/out_kt_c_v2_3_e1n%d.out' % _N]   # S9C: engine A's EXPLICIT lines (m_bg)
SHARED_INPUTS = ['/pk07/out/export_kt_s67_cert_v2_2_sweep.kv', '/pk03/m3_reader_v4_4.py', '/pk11/out/vacres_K3_N4_sym_v1.json',
                 '/pk11/out/vacres_K3_N3_sym_v1.json', '/pk02/M2B_KV_v1.txt', '/pk02/out/out_m2b_asm_v1.out', '/pk02/m2b_reader_v1.py',
                 '/pk15/mocks/mock_ritz_entries_v1.kv', '/pk11/out/ts_N4_J170_D_S_z9sym_v1.json', '/pk11/out/ts_N3_S_z9sym_v1.json',
                 '/pk03/out/m3_s9_N4_J300_v1_8_3.json', '/pk03/out/m3_run_v1_8_3_asm9.4.out', '/pk03/out/m3_s9_N3_J300_v1_8_3.json',
                 '/pk03/out/m3_run_v1_8_3_asm9.3.out', '/pk15/M4_KV_v1.txt', '/pk15/out/out_m4_asm_v1.out', '/pk15/m4_reader_v1.py',
                 '/pk07/out/export_kt_s9h_v1_2_vsweep.kv', '/pk07/out/out_kt_s9h_v1_2_vsweep.out', '/pk07/kt_s67_export_reader_v2_1.py',
                 '/pk07/kt_s9h_v1_2.py', '/pk03/out/m3_run_v1_8_1_asmP.4.out', '/pk03/out/m3_run_v1_8_1_asmP.3.out',
                 '/pk03/out/m3_s8v3_D_N4_J300_v1_8_1.json', '/pk03/out/m3_s8v3_D_N3_J300_v1_8_1.json',
                 '/pk03/out/m3_s8v3_N_N4_J300_v1_8_2.json', '/pk03/out/m3_run_v1_8_2_asmN.4.out',
                 '/pk03/out/m3_s8v3_N_N3_J300_v1_8_2.json', '/pk03/out/m3_run_v1_8_2_asmN.3.out',
                 '/pk03/out/m3_b5_N4_J300_v1_7.json', '/pk03/out/m3_b5_N3_J300_v1_7.json', '/pk03/out/m3_run_v1_7_asm.4.out',
                 '/pk03/out/m3_run_v1_7_asm.3.out']


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def module_parts(src):
    tree = ast.parse(src)
    defs, assigns, imports, count = {}, {}, set(), {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            defs[n.name] = n
            count[n.name] = count.get(n.name, 0) + 1
        elif isinstance(n, ast.Assign):
            names = [x.id for t in n.targets for x in ast.walk(t) if isinstance(x, ast.Name)]
            key = ','.join(names)
            assigns[key] = n
            count['=' + key] = count.get('=' + key, 0) + 1
            for x in names:
                count['name:' + x] = count.get('name:' + x, 0) + 1
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                imports.add((a.asname or a.name).split('.')[0])
    return tree, defs, assigns, imports, count


def closure(defs, assigns, imports, roots, follow=True):
    seen, stack, free = set(), list(roots), set()
    while stack:
        f = stack.pop()
        if f in seen:
            continue
        if f not in defs:
            raise SystemExit('STOP: %s is not a module-level def' % f)
        seen.add(f)
        for x in ast.walk(defs[f]):
            if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load):
                if x.id in defs:
                    if follow:
                        stack.append(x.id)
                    else:
                        free.add(x.id)
                elif any(x.id in k.split(',') for k in assigns) or x.id in imports:
                    free.add(x.id)
    return seen, free


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r'kt_s9h_ins_v2_[1-9][0-9]?\.py', sys.argv[1]):
        print('usage: make_kt_s9h_ins_v2_1.py kt_s9h_ins_v2_<n>.py')
        return 2
    dst = W + '/pk25/asm/' + sys.argv[1]
    if os.path.exists(dst):
        print('STOP: %s exists' % dst)
        return 6
    r4sha, c6sha = sha(R4), sha(C6A)
    if not r4sha.startswith('e92342b0') or not c6sha.startswith('1704af08'):
        print('STOP: R4 or C6a sha256 prefix')
        return 6
    srcs = {}
    for name, path, roots, consts, follow in (('R4', R4, ROOTS, CONSTS, True), ('C6A', C6A, C6A_ROOTS, C6A_CONSTS, False)):
        src = open(path).read()
        tree, defs, assigns, imports, count = module_parts(src)
        seen, free = closure(defs, assigns, imports, roots, follow)
        order = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in seen]
        dupd = [f for f in order if count[f] != 1]
        dupc = [c for c in consts if count.get('=' + c) != 1 or any(count.get('name:' + x) != 1 for x in c.split(','))]
        if dupd or dupc or any(c not in assigns for c in consts):
            print('STOP %s: duplicated defs %s, duplicated or missing constants %s' % (name, dupd, dupc))
            return 6
        cseg = [ast.get_source_segment(src, assigns[c]) for c in sorted(consts, key=lambda c: assigns[c].lineno)]
        dseg = [ast.get_source_segment(src, defs[f]) for f in order]
        srcs[name] = dict(order=order, free=free, cseg=cseg, dseg=dseg, consts=tuple(sorted(consts, key=lambda c: assigns[c].lineno)),
                          tree=tree, defs=defs)
    covered = set(x for nm in srcs for c in srcs[nm]['consts'] for x in c.split(',')) | set(PROVIDED) | set(IMPORTS) | set(srcs['R4']['order']) | set(srcs['C6A']['order'])
    missing = sorted((srcs['R4']['free'] | srcs['C6A']['free']) - covered)
    if missing:
        print('STOP: uncovered free names %s' % missing)
        return 6
    r4pins = None
    for n in srcs['R4']['tree'].body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'PINS':
            r4pins = ast.literal_eval(n.value)
    pins = {}
    for rel in SHARED_INPUTS:
        p = W + rel
        if r4pins.get(p) != sha(p):
            print('STOP: %s is not R4\'s pin' % rel)
            return 6
        pins[p] = sha(p)
    for rel in NEW_INPUTS:
        pins[W + rel] = sha(W + rel)
    tmpl = open(SRC).read()
    marks = ('# @@CORE_CONSTS@@', '# @@C6A_CONSTS@@', '@@R4_SHA@@', '@@C6A_SHA@@', '@@CORE_DEFS@@', '@@CORE_CONSTS_NAMES@@', '@@C6A_DEFS@@',
             '@@C6A_CONSTS_NAMES@@', '# @@PINS@@', '# @@CORE_DEFS_BLOCK@@', '# @@C6A_DEFS_BLOCK@@')
    for mk in marks:
        if tmpl.count(mk) != 1:
            print('STOP: template mark %s appears %d times' % (mk, tmpl.count(mk)))
            return 6
    text = (tmpl.replace('# @@CORE_DEFS_BLOCK@@', '\n\n'.join(srcs['R4']['dseg'])).replace('# @@C6A_DEFS_BLOCK@@', '\n\n'.join(srcs['C6A']['dseg']))
            .replace('# @@CORE_CONSTS@@', '\n'.join(srcs['R4']['cseg'])).replace('# @@C6A_CONSTS@@', '\n'.join(srcs['C6A']['cseg']))
            .replace('@@CORE_CONSTS_NAMES@@', repr(srcs['R4']['consts'])).replace('@@C6A_CONSTS_NAMES@@', repr(srcs['C6A']['consts']))
            .replace('@@CORE_DEFS@@', repr(tuple(srcs['R4']['order']))).replace('@@C6A_DEFS@@', repr(tuple(srcs['C6A']['order'])))
            .replace('@@R4_SHA@@', r4sha).replace('@@C6A_SHA@@', c6sha)
            .replace('# @@PINS@@', '\n'.join("    '%s': '%s'," % (p, pins[p]) for p in sorted(pins))).replace('@@NAME@@', sys.argv[1]))
    if '@@' in text:
        print('STOP: a template mark is left')
        return 6
    ast.parse(text)
    with open(dst, 'x') as fh:
        fh.write(text)
    print('MAKER %s sha256 %s' % (os.path.basename(__file__), sha(os.path.abspath(__file__))))
    print('TEMPLATE %s sha256 %s' % (os.path.relpath(SRC, W), sha(SRC)))
    print('R4 %s; C6A %s' % (r4sha, c6sha))
    for nm in ('R4', 'C6A'):
        print('%s defs %d: %s' % (nm, len(srcs[nm]['order']), ' '.join(srcs[nm]['order'])))
        print('%s constants %d: %s' % (nm, len(srcs[nm]['consts']), ' '.join(srcs[nm]['consts'])))
    print('PINS %d (%d shared with R4)' % (len(pins), len(SHARED_INPUTS)))
    print('ENGINE %s sha256 %s lines %d' % (os.path.relpath(dst, W), sha(dst), text.count('\n')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
