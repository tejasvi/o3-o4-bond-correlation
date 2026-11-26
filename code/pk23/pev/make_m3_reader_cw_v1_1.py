#!/usr/bin/env python3
"""make_m3_reader_cw_v1_1.py (pk23, C_w variant B; pk22's 10' note: "your reader needs the same producer entry"): makes
pk23/pev/m3_reader_cw_v1_1.py, the reader fork m3_reader_cw_v1.py (876b6184) with one more producer, pk22's m3_lawcert_c3k_v2 (the law
certificate of the c3k rerun on state 10', records m3_c3kp_E4D/E4N_N<N>_J300_c3kp.json), by exact replacements with asserted counts, and writes
the diff. The producer's sha256 is read from pk22/m3/m3_lawcert_c3k_v2.py and checked against the first line of both certificate jobs'
outputs (pk22/m3/out/m3_lawcert_c3k_v2_<N>.out) and against the expected prefix given on the command line (from pk22's frozen manifest
or message). Every function and class of the parent stays byte-identical in the AST. Usage: make_m3_reader_cw_v1_1.py C3K2_SHA_PREFIX."""
import ast, difflib, hashlib, os, re, sys
W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
SRC = HLD + '/m3_reader_cw_v1.py'
DST, DIFF = HLD + '/m3_reader_cw_v1_1.py', HLD + '/diff_m3_reader_cw_v1_to_v1_1.txt'
LCP = W18 + '/pk22/m3/m3_lawcert_c3k_v2.py'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


assert len(sys.argv) == 2 and re.fullmatch('[0-9a-f]{8,64}', sys.argv[1]), 'usage: make_m3_reader_cw_v1_1.py C3K2_SHA_PREFIX'
for p in (DST, DIFF):
    if os.path.exists(p):
        sys.exit('STOP exists %s' % p)
PS = sha(SRC)
assert PS.startswith('aff9ad90'), PS
LC = sha(LCP)
assert LC.startswith(sys.argv[1]), 'm3_lawcert_c3k_v2.py sha256 %s does not start with %s' % (LC, sys.argv[1])
for n in (4, 3):
    with open(W18 + '/pk22/m3/out/m3_lawcert_c3k_v2_%d.out' % n) as fh:
        first = fh.readline()
    assert first.startswith('m3_lawcert_c3k_v2 N %d LIM ' % n) and ('; script sha256 %s;' % LC) in first, 'certificate job %d' % n
print('PARENT m3_reader_cw_v1 %s; producer m3_lawcert_c3k_v2 %s' % (PS, LC))


def apply(src, repl):
    new = src
    for lab, old, rep, cnt in repl:
        n_ = new.count(old)
        assert n_ == cnt, '%s: %d occurrences, expected %d' % (lab, n_, cnt)
        new = new.replace(old, rep)
        print('REPL %s: %d replaced' % (lab, n_))
    return new


src = open(SRC).read()
HEAD = ('m3_reader_cw_v1_1.py -- pk23 (code/pk23/pev/). pk23\'s m3_reader_cw_v1.py (sha256 %s) with one more producer (pk22\'s 10\'\n'
        'note to pk23: the certified J-laws of IhR,10\',b for C_w\'s comb), made by pk23/pev/make_m3_reader_cw_v1_1.py with exact replacements of\n'
        'asserted counts. What changes, and nothing else (pk23/pev/diff_m3_reader_cw_v1_to_v1_1.txt):\n'
        '- the producer allow-list PRODUCERS gains pk22\'s m3_lawcert_c3k_v2 (sha256 %s), which certifies exactly the two records\n'
        '  m3_c3kp_<F>_N<N>_J300_c3kp.json, F in E4D, E4N (the c3k rerun on state 10\'); PRODUCER_RE names it; PRODUCER_RECORDS gives it the prefix\n'
        '  m3_c3kp_, the suffix _J300_c3kp.json and the two families.\n'
        'Every earlier producer stays as it is. m3_reader_cw_v1\'s docstring follows.\n') % (PS, LC)
new = apply(src, [
    ('docstring head', '"""m3_reader_cw_v1.py -- pk23 (code/pk23/pev/). pk23\'s m3_reader_hl_v1.py (sha256 ',
     '"""' + HEAD + 'm3_reader_cw_v1.py -- pk23 (code/pk23/pev/). pk23\'s m3_reader_hl_v1.py (sha256 ', 1),
    ('PRODUCERS gains the c3k_v2 producer', "'}   # m3_reader_cw_v1: pk23's C_w record LC\n",
     "',   # m3_reader_cw_v1: pk23's C_w record LC\n             'm3_lawcert_c3k_v2.py': '" + LC + "'}   # m3_reader_cw_v1_1: pk22's c3kp records\n", 1),
    ('PRODUCER_RECORDS the c3k_v2 row', "'m3_lawcert_cw_v1.py': ('m3_cw_', '_J300_cw.json', ('LC',))}   # m3_reader_cw_v1",
     "'m3_lawcert_cw_v1.py': ('m3_cw_', '_J300_cw.json', ('LC',)),   # m3_reader_cw_v1\n"
     "                    'm3_lawcert_c3k_v2.py': ('m3_c3kp_', '_J300_c3kp.json', ('E4D', 'E4N'))}   # m3_reader_cw_v1_1", 1),
    ('PRODUCER_RE', "|m3_lawcert_hl_v1_1|m3_lawcert_cw_v1) N ([0-9]+) LIM", "|m3_lawcert_hl_v1_1|m3_lawcert_cw_v1|m3_lawcert_c3k_v2) N ([0-9]+) LIM", 1),
])


def defs(t):
    return {n.name: ast.dump(n) for n in t.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


d0, d1 = defs(ast.parse(src)), defs(ast.parse(new))
assert d0 == d1, 'a function or class changed'
print('DEFS identical: %d' % len(d0))
with open(DST, 'x') as fh:
    fh.write(new)
with open(DIFF, 'x') as fh:
    fh.writelines(difflib.unified_diff(src.splitlines(True), new.splitlines(True), 'm3_reader_cw_v1.py', 'm3_reader_cw_v1_1.py'))
print('WROTE %s %s' % (sha(DST), DST))
print('WROTE %s %s' % (sha(DIFF), DIFF))
