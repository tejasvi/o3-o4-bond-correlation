#!/usr/bin/env python3
"""make_m4h_v1_1.py -- pk25: makes m4h_reader_v1_1.py and m4h_asm_v1_1.py from the frozen m4h_reader_v1.py and m4h_asm_v1.py
(MANIFEST_C5_M4H_v1) after C5's first cert run (the approval, P0_LOG row 4263): every gate passed, but PLANT-SWAP did not fire. Its
exchange of N4 h's and N4 h1's M1 (1.47e-4 and 5.85e-4) moved h1's L(300) only from +1.40% to about +0.4% over Q, still inside
C-LAW300's band, so the plant's condition (both kinds fail) did not hold. The plant now exchanges M0 (4.4e-17 and 4.30e-2), which takes
both kinds out of the band, with the parent's condition unchanged. The names move to v1_1 (the reader's PIN_CODE names, the binding's
first-line producer, the asm's header). Exact replacements with asserted counts; writes both diffs."""
import ast, difflib, hashlib, os, sys
D = '/mnt/g2/release/root/code/pk25/m4h'
RS, AS_ = D + '/m4h_reader_v1.py', D + '/m4h_asm_v1.py'
RD, AD = D + '/m4h_reader_v1_1.py', D + '/m4h_asm_v1_1.py'
RDIFF, ADIFF = D + '/diff_m4h_reader_v1_to_v1_1.txt', D + '/diff_m4h_asm_v1_to_v1_1.txt'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


for p in (RD, AD, RDIFF, ADIFF):
    if os.path.exists(p):
        sys.exit('STOP exists %s' % p)
man = {}
with open(D + '/MANIFEST_C5_M4H_v1.sha256') as fh:
    for ln in fh:
        h_, p_ = ln.rstrip('\n').split('  ', 1)
        man[p_] = h_
assert man['pk25/m4h/m4h_reader_v1.py'] == sha(RS) and man['pk25/m4h/m4h_asm_v1.py'] == sha(AS_), 'v1 files differ from their manifest'


def apply(src, repl, what):
    new = src
    for lab, old, rep, cnt in repl:
        n_ = new.count(old)
        assert n_ == cnt, '%s %s: %d occurrences, expected %d' % (what, lab, n_, cnt)
        new = new.replace(old, rep)
        print('REPL %s %s: %d replaced' % (what, lab, n_))
    return new


def defs(t):
    return {n.name: ast.dump(n) for n in t.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


def changed_defs(a, b):
    da, db = defs(ast.parse(a)), defs(ast.parse(b))
    return sorted(k for k in da if k in db and da[k] != db[k]), sorted(set(db) - set(da)), sorted(set(da) - set(db))


with open(RS) as fh:
    rsrc = fh.read()
RHEAD = ('m4h_reader_v1_1.py -- pk25 (code/pk25/m4h/). REVISION of m4h_reader_v1.py (sha256 ' + sha(RS) + ') with m4h_asm_v1_1 (C5\'s\n'
         'first cert run: every gate passed, PLANT-SWAP did not fire; the asm\'s plant now exchanges M0): only the names move to v1_1, the\n'
         'PIN_CODE names (READER_REL, ASM_REL), the binding\'s first-line producer m4h_asm_v1_1 and the script-mode header and usage.\n'
         'm4h_reader_v1\'s docstring follows.\n')
RREPL = [
    ('docstring head', '"""m4h_reader_v1.py -- pk25 (code/pk25/m4h/). A FORK of', '"""' + RHEAD + 'm4h_reader_v1.py -- pk25 (code/pk25/m4h/). A FORK of', 1),
    ('PIN_CODE names', "READER_REL, ASM_REL = 'pk25/m4h/m4h_reader_v1.py', 'pk25/m4h/m4h_asm_v1.py'",
     "READER_REL, ASM_REL = 'pk25/m4h/m4h_reader_v1_1.py', 'pk25/m4h/m4h_asm_v1_1.py'", 1),
    ('binding', "    mt = re.match(r'm4h_asm_v1 sha256 ([0-9a-f]{64}) ', lines[0] if lines else '')",
     "    mt = re.match(r'm4h_asm_v1_1 sha256 ([0-9a-f]{64}) ', lines[0] if lines else '')", 1),
    ('PIN_CODE message', "        raise ValueError('C-PINS: PIN_CODE does not name m4h_asm_v1.py at ASM_SHA256')",
     "        raise ValueError('C-PINS: PIN_CODE does not name m4h_asm_v1_1.py at ASM_SHA256')", 1),
    ('usage', "        print('usage: m4h_reader_v1.py <record> <asm output> [expected sha256]')",
     "        print('usage: m4h_reader_v1_1.py <record> <asm output> [expected sha256]')", 1),
    ('script header', "        print('m4h_reader_v1 sha256 %s; record %s; asm output %s'", "        print('m4h_reader_v1_1 sha256 %s; record %s; asm output %s'", 1),
]
rnew = apply(rsrc, RREPL, 'reader')
ch, ad, dr = changed_defs(rsrc, rnew)
print('reader defs changed %s, added %s, dropped %s' % (ch, ad, dr))
assert ch == ['load', 'loads'] and not ad and not dr
with open(RD, 'x') as fh:
    fh.write(rnew)
with open(RDIFF, 'x') as fh:
    fh.writelines(difflib.unified_diff(rsrc.splitlines(True), rnew.splitlines(True), 'm4h_reader_v1.py', 'm4h_reader_v1_1.py'))
RSHA = sha(RD)
print('WROTE m4h_reader_v1_1.py sha256 %s; diff %s' % (RSHA, sha(RDIFF)))

with open(AS_) as fh:
    asrc = fh.read()
reader_line = [ln for ln in asrc.splitlines(True) if ln.startswith('READER, READER_SHA = ')]
assert len(reader_line) == 1
AHEAD = ('m4h_asm_v1_1.py -- pk25 (code/pk25/m4h/). REVISION of m4h_asm_v1.py (sha256 ' + sha(AS_) + ') after C5\'s first cert run\n'
         '(the approval, P0_LOG row 4263; output pk25/m4h/out/out_m4h_asm_v1.out): every gate passed and no record was written, because\n'
         'PLANT-SWAP did not fire. Its exchange of N4 h\'s and N4 h1\'s M1 (1.47e-4, 5.85e-4) moved h1\'s L(300) from +1.40% to about +0.4%\n'
         'over Q, inside C-LAW300\'s band, so the plant\'s condition (both kinds fail) did not hold. The plant now exchanges M0 (4.4e-17,\n'
         '4.30e-2); the condition is the parent\'s. Also: the reader is m4h_reader_v1_1 (sha256 ' + RSHA + '), and the header line\n'
         'and usage name m4h_asm_v1_1. Nothing else changes (diff_m4h_asm_v1_to_v1_1.txt).\n'
         'm4h_asm_v1\'s docstring follows.\n')
AREPL = [
    ('docstring head', '"""m4h_asm_v1.py -- pk25 (code/pk25/m4h/). A FORK of', '"""' + AHEAD + 'm4h_asm_v1.py -- pk25 (code/pk25/m4h/). A FORK of', 1),
    ('READER', reader_line[0], "READER, READER_SHA = 'pk25/m4h/m4h_reader_v1_1.py', '" + RSHA + "'   # m4h_asm_v1_1\n", 1),
    ('PLANT-SWAP keys', "    sw = R._sub(R._sub(text0, 'N4_H_M1', kvd['N4_H1_M1']), 'N4_H1_M1', kvd['N4_H_M1'])",
     "    sw = R._sub(R._sub(text0, 'N4_H_M0', kvd['N4_H1_M0']), 'N4_H1_M0', kvd['N4_H_M0'])   # m4h_asm_v1_1: M0 (v1's M1 swap stayed in band)", 1),
    ('PLANT-SWAP text', "               'N4 h\\'s and N4 h1\\'s M1 exchanged: C-LAW300 on h or on h1')",
     "               'N4 h\\'s and N4 h1\\'s M0 exchanged: C-LAW300 on h or on h1')", 1),
    ('usage', "        print('usage: m4h_asm_v1.py cert | mock <mock far kv under code/>')",
     "        print('usage: m4h_asm_v1_1.py cert | mock <mock far kv under code/>')", 1),
    ('header line', "    print('m4h_asm_v1 sha256 %s MODE=%s; file %s; python %s; ctx.prec %d'",
     "    print('m4h_asm_v1_1 sha256 %s MODE=%s; file %s; python %s; ctx.prec %d'", 1),
    ('reader module', "        R = module(READER, 'm4h_reader_v1')\n", "        R = module(READER, 'm4h_reader_v1_1')\n", 1),
]
anew = apply(asrc, AREPL, 'asm')
ch, ad, dr = changed_defs(asrc, anew)
print('asm defs changed %s, added %s, dropped %s' % (ch, ad, dr))
assert ch == ['main', 'plants'] and not ad and not dr
with open(AD, 'x') as fh:
    fh.write(anew)
with open(ADIFF, 'x') as fh:
    fh.writelines(difflib.unified_diff(asrc.splitlines(True), anew.splitlines(True), 'm4h_asm_v1.py', 'm4h_asm_v1_1.py'))
print('WROTE m4h_asm_v1_1.py sha256 %s; diff %s' % (sha(AD), sha(ADIFF)))
