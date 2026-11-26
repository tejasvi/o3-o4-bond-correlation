#!/usr/bin/env python3
"""make_m3_reader_hl_v1.py (pk23; C_w variant B, the P0_LOG row 4589): makes pk23/pev/m3_reader_hl_v1.py, the consumers' reader fork of
pk22's m3_reader_c3h_v1_2.py (bff8344c, read-only) that adds the producer m3_lawcert_hl_v1_1 (pk23's law certificate of the Pev records
L, LH, LT), by exact replacements with asserted counts, and writes the diff. The producer's sha256 is read from the file and checked against
the first line of both certificate jobs' outputs (pk23/pev/out/m3_lawcert_hl_v1_1_<N>.out). Every function and class of the parent stays
byte-identical in the AST. Usage: make_m3_reader_hl_v1.py. Prints the sha256s."""
import ast, difflib, hashlib, os, sys
W18 = '/mnt/g2/release/root/code'
SRC = W18 + '/pk22/m3/m3_reader_c3h_v1_2.py'
HLD = W18 + '/pk23/pev'
DST, DIFF = HLD + '/m3_reader_hl_v1.py', HLD + '/diff_m3_reader_c3h_v1_2_to_hl_v1.txt'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


for p in (DST, DIFF):
    if os.path.exists(p):
        sys.exit('STOP exists %s' % p)
PS = sha(SRC)
assert PS.startswith('bff8344c'), PS
LCP = HLD + '/m3_lawcert_hl_v1_1.py'
LC = sha(LCP)
assert LC.startswith('fda54b63'), LC
for n in (4, 3):
    with open(HLD + '/out/m3_lawcert_hl_v1_1_%d.out' % n) as fh:
        first = fh.readline()
    assert first.startswith('m3_lawcert_hl_v1_1 N %d LIM ' % n) and ('; script sha256 %s;' % LC) in first, 'certificate job %d' % n
print('PARENT m3_reader_c3h_v1_2 %s; producer m3_lawcert_hl_v1_1 %s' % (PS, LC))


def apply(src, repl):
    new = src
    for lab, old, rep, cnt in repl:
        n_ = new.count(old)
        assert n_ == cnt, '%s: %d occurrences, expected %d' % (lab, n_, cnt)
        new = new.replace(old, rep)
        print('REPL %s: %d replaced' % (lab, n_))
    return new


src = open(SRC).read()
HEAD = ('m3_reader_hl_v1.py -- pk23 (code/pk23/pev/). pk22\'s m3_reader_c3h_v1_2.py (sha256 %s) with one more producer (the\n'
        'P0_LOG row 4589: the certified J-laws of pk23\'s Pev records for C_w\'s second-order comb), made by pk23/pev/make_m3_reader_hl_v1.py with\n'
        'exact replacements of asserted counts. What changes, and nothing else (pk23/pev/diff_m3_reader_c3h_v1_2_to_hl_v1.txt):\n'
        '- the producer allow-list PRODUCERS gains m3_lawcert_hl_v1_1 (sha256 %s), which certifies exactly the three records\n'
        '  m3_hl_<F>_N<N>_J300_hl.json, F in L, LH, LT (m3_run_v1_9_3_hl_v1\'s asm.N); PRODUCER_RE names it; PRODUCER_RECORDS gives it the prefix\n'
        '  m3_hl_, the suffix _J300_hl.json and the three families.\n'
        'Every earlier producer stays as it is. Consumers call load and load_lawcert, never _bound or _parse_lawcert alone, and pass the certificate with\n'
        'its own job output m3_lawcert_hl_v1_1_<N>.out. The check job pk23/pev/m3_reader_hl_check_v1.py runs load_lawcert on both N, with plants.\n'
        'm3_reader_c3h_v1_2\'s docstring follows.\n') % (PS, LC)
new = apply(src, [
    ('docstring head', '"""m3_reader_c3h_v1_2.py -- pk22 (code/pk22/m3/). m3_reader_c3h_v1_1.py (sha256 ',
     '"""' + HEAD + 'm3_reader_c3h_v1_2.py -- pk22 (code/pk22/m3/). m3_reader_c3h_v1_1.py (sha256 ', 1),
    ('PRODUCERS gains the hl producer', "'}   # m3_reader_c3h_v1_2: the two c3k records\n",
     "',   # m3_reader_c3h_v1_2: the two c3k records\n             'm3_lawcert_hl_v1_1.py': '" + LC + "'}   # m3_reader_hl_v1: pk23's three Pev records\n", 1),
    ('PRODUCER_RECORDS the hl row', "'m3_lawcert_c3k_v1.py': ('m3_c3k_', '_J300_c3k.json', ('E4D', 'E4N'))}   # m3_reader_c3h_v1_2",
     "'m3_lawcert_c3k_v1.py': ('m3_c3k_', '_J300_c3k.json', ('E4D', 'E4N')),   # m3_reader_c3h_v1_2\n"
     "                    'm3_lawcert_hl_v1_1.py': ('m3_hl_', '_J300_hl.json', ('L', 'LH', 'LT'))}   # m3_reader_hl_v1", 1),
    ('PRODUCER_RE', "|m3_lawcert_c3h_v1_1|m3_lawcert_c3k_v1) N ([0-9]+) LIM", "|m3_lawcert_c3h_v1_1|m3_lawcert_c3k_v1|m3_lawcert_hl_v1_1) N ([0-9]+) LIM", 1),
])


def defs(t):
    return {n.name: ast.dump(n) for n in t.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


d0, d1 = defs(ast.parse(src)), defs(ast.parse(new))
assert d0 == d1, 'a function or class changed'
print('DEFS identical: %d' % len(d0))
with open(DST, 'x') as fh:
    fh.write(new)
with open(DIFF, 'x') as fh:
    fh.writelines(difflib.unified_diff(src.splitlines(True), new.splitlines(True), 'm3_reader_c3h_v1_2.py', 'm3_reader_hl_v1.py'))
print('WROTE %s %s' % (sha(DST), DST))
print('WROTE %s %s' % (sha(DIFF), DIFF))
