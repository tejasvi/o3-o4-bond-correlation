#!/usr/bin/env python3
"""make_mrx_combine_v1_10.py (pk22; item (4), MR_EXACT v1_10): writes midrow/g4/mrc/src/mrx_combine_v1_10.py from mrx_combine_v1_9.py
(the frozen file listed in MANIFEST_MRX_CERT_v1_9.sha256, every row of which is verified first) by literal replacements, each with its count
checked, and the unified diff src/diff_mrx_combine_v1_9_to_v1_10.txt (both mode 'x'). Changes: the names v1_9 -> v1_10 (CERTF, RUNS, the part
and record names, CODE, PRODUCER, JOINED_BY); C-RUNS also needs each run's Way A gate lines (6 PASS) and plant lines (2 FIRES); new gates
C-WAYA-ROWS (with PLANT-WAYA-ROWS) and C-SAME-V1_9 on the C parts, the latter pinned to MANIFEST_MRX_CERT_v1_9 (its sha256 written in by this
maker); the record's comment line and a WAYA_FORM header line name Way A. Top-level defs: one added (waya_row_ok), none changed.
Usage: make_mrx_combine_v1_10.py"""
import ast, difflib, hashlib

E = '/mnt/g2/release/root/code/pk22/midrow/g4/mrc'
SRC = E + '/src/mrx_combine_v1_9.py'
DST = E + '/src/mrx_combine_v1_10.py'
DIFF = E + '/src/diff_mrx_combine_v1_9_to_v1_10.txt'
V19MAN = E + '/MANIFEST_MRX_CERT_v1_9.sha256'


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def rep(t, old, new, count, label):
    n = t.count(old)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    assert n == count, (label, n, count)
    return t.replace(old, new)


def defs(t):
    return dict((n.name, ast.dump(n)) for n in ast.parse(t).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)))


man = dict((ln.split()[1], ln.split()[0]) for ln in open(V19MAN) if ln.strip())
for p, h in man.items():
    assert sha(p) == h, p
assert man.get(SRC) == sha(SRC), 'mrx_combine_v1_9 is not its manifest row'
for N in (4, 3):
    assert (E + '/out/cert/MR_EXACT_PART_v1_9_C_N%d.kv' % N) in man, N
V19SHA = sha(V19MAN)
print('PIN V19 %s %s (%d rows verified)' % (V19SHA, V19MAN, len(man)))
print('SOURCE %s %s' % (sha(SRC), SRC))
old = open(SRC).read()
t = old
HEAD = ('"""mrx_combine_v1_10.py (pk22): mrx_combine_v1_9.py for mrx_cert_v1_10\'s certified parts (variant C: Way A for h-1 and h0 on the\n'
        'last piece, Axf 0 and a finite Axc there, from pk25\'s P2 MR_LEMMAP_V3F; made by make_mrx_combine_v1_10.py). New: C-RUNS also needs each\n'
        'run\'s Way A lines (C-WAYA-IN, C-WAYA-RUN, C-WAYA-T0, C-WAYA-CONT, C-WAYA-JOIN, C-WAYA -> PASS; PLANT-WAYA-PIN, PLANT-WAYA-ZERO -> FIRES).\n'
        'C-WAYA-ROWS: on each N\'s last piece the C part\'s h-1 and h0 rows carry Axf 0 and Axc_lo <= Axc_hi with t Axc inside [Ax_lo, Ax_hi] at\n'
        't = 0 and t = 1/jlo (engine v1_8_4\'s G-FACTX with floor 0), with PLANT-WAYA-ROWS (Axc_hi = 2 jlo Ax_hi there must fail). C-SAME-V1_9:\n'
        'every other row of the C parts equals the row of v1_9\'s certified C part (MANIFEST_MRX_CERT_v1_9 pinned, the part its row), in the same\n'
        'order. The record is MR_EXACT_CERT_v1_10_C.kv, with a WAYA_FORM header line. mrx_combine_v1_9\'s docstring follows.\n'
        'mrx_combine_v1_9.py (pk22): ')
t = rep(t, '"""mrx_combine_v1_9.py (pk22): ', HEAD, 1, 'R1 docstring head')
t = rep(t, 'import ast, hashlib, os, re, sys\n', 'import ast, hashlib, os, re, sys\nfrom fractions import Fraction as Fr   # mrx_combine_v1_10\n', 1, 'R2 import')
t = rep(t, "SPEF = W + '/pk25/mr/v4/MR_SPECTRAL.kv'\n",
        "V19 = (E + '/MANIFEST_MRX_CERT_v1_9.sha256', '%s')   # mrx_combine_v1_10: v1_9's certified parts, for C-SAME-V1_9\n"
        "SPEF = W + '/pk25/mr/v4/MR_SPECTRAL.kv'\n" % V19SHA, 1, 'R3 V19 pin')
t = rep(t, "CERTF = E + '/src/mrx_cert_v1_9.py'\n", "CERTF = E + '/src/mrx_cert_v1_10.py'\n", 1, 'R4 CERTF')
t = rep(t, "RUNS = {4: E + '/out/mrx_cert_v1_9_cert_n4.out', 3: E + '/out/mrx_cert_v1_9_cert_n3.out'}\n",
        "RUNS = {4: E + '/out/mrx_cert_v1_10_cert_n4.out', 3: E + '/out/mrx_cert_v1_10_cert_n3.out'}\n", 1, 'R5 RUNS')
t = rep(t, "ENDS = ('h-1', 'h0', 't-1', 'a0')   # mrx_combine_v1_8: + h0\n",
        "ENDS = ('h-1', 'h0', 't-1', 'a0')   # mrx_combine_v1_8: + h0\n"
        "WAYA_GATES = ('C-WAYA-IN', 'C-WAYA-RUN', 'C-WAYA-T0', 'C-WAYA-CONT', 'C-WAYA-JOIN', 'C-WAYA')   # mrx_combine_v1_10: each run's Way A lines\n"
        "WAYA_PLANTS = ('PLANT-WAYA-PIN', 'PLANT-WAYA-ZERO')\n"
        "WAYA_FORM = ('WAYA_FORM = h-1 and h0 on the last piece (t = 1/J in [0, 1/jlo]): Way A, A_x = F / (<u_0, w2> s_x) with F = <u_x, w1 - r* w2> and '\n"
        "             'r* = <u_0, w1>/<u_0, w2>; F(0) = 0 (C13 C-GAMMA and C-BH0 with P1 C-SPAN; gated in the runs as C-WAYA-T0); Axc encloses A_x/t = '\n"
        "             '(F/t) / (<u_0, w2> s_x), from pk25\\'s P2 MR_LEMMAP_V3F /t fields, C10\\'s UHAT0 and the certified J-laws with their remainders over t; '\n"
        "             'Axf 0; Ax the hull of the direct ball, 0 and Axc/jlo')\n", 1, 'R6 Way A constants')
t = rep(t, "out('mrx_combine_v1_9; script sha256 %s; mrx_cert_v1_9 sha256 %s; python %s' % (SELF, CSHA, sys.version.split()[0]))\n",
        "out('mrx_combine_v1_10; script sha256 %s; mrx_cert_v1_10 sha256 %s; python %s' % (SELF, CSHA, sys.version.split()[0]))\n", 1, 'R7 head line')
t = rep(t, "pins = [SPEC, ENG, MAN]\n", "pins = [SPEC, ENG, MAN, V19]   # mrx_combine_v1_10: + V19\n", 1, 'R8 pins')
t = rep(t, "    okN = verd == ['VERDICT VALID'] and mco is not None and mpo is not None and mco.group(1) == mpo.group(1) == mpo.group(2)\n",
        "    okN = verd == ['VERDICT VALID'] and mco is not None and mpo is not None and mco.group(1) == mpo.group(1) == mpo.group(2)\n"
        "    wg = sorted(ln.split(' ')[0] for ln in lines if re.fullmatch(r'(C-WAYA-IN|C-WAYA-RUN|C-WAYA-T0|C-WAYA-CONT|C-WAYA-JOIN|C-WAYA) \\(.*\\) -> PASS', ln))\n"
        "    wp = sorted(ln.split(' ')[0] for ln in lines if re.fullmatch(r'(PLANT-WAYA-PIN|PLANT-WAYA-ZERO) \\(.*\\) -> FIRES', ln))\n"
        "    okN = okN and wg == sorted(WAYA_GATES) and wp == sorted(WAYA_PLANTS)   # mrx_combine_v1_10\n", 1, 'R9 Way A lines')
t = rep(t, "        pp = os.path.join(OUTD, 'MR_EXACT_PART_v1_9_%s_N%d.kv' % (V, N))\n", "        pp = os.path.join(OUTD, 'MR_EXACT_PART_v1_10_%s_N%d.kv' % (V, N))\n", 1,
        'R10 part names')
t = rep(t, "    run_why.append('N%d %s %s: %s, C-ORIENT on %s pieces, PLANT-ORIENT %s' % (N, os.path.basename(rp), sha(rp)[:8], verd, mco.group(1) if mco else '?',\n"
           "                                                                            'fired' if mpo else 'missing'))\n",
        "    run_why.append('N%d %s %s: %s, C-ORIENT on %s pieces, PLANT-ORIENT %s, Way A gates %d of %d PASS, plants %d of %d FIRE' % (\n"
        "        N, os.path.basename(rp), sha(rp)[:8], verd, mco.group(1) if mco else '?', 'fired' if mpo else 'missing', len(wg), len(WAYA_GATES), len(wp),\n"
        "        len(WAYA_PLANTS)))\n", 1, 'R11 run line')
t = rep(t, "h.get('CODE') != 'pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py:%s' % CSHA[:8]", "h.get('CODE') != 'pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py:%s' % CSHA[:8]",
        1, 'R12 CODE check')
t = rep(t, "CODE mrx_cert_v1_9 %s; FIELDS", "CODE mrx_cert_v1_10 %s; FIELDS", 1, 'R13 C-PARTS text')
GATES = r'''# ---- mrx_combine_v1_10: the Way A rows of the C parts, and the rows they share with v1_9's certified C parts
def waya_row_ok(f):
    """engine v1_8_4's G-FACTX with floor 0 on a last-piece h row (fields as FIELDS): Axf 0, Axc_lo <= Axc_hi, t Axc inside [Ax_lo, Ax_hi]
    at t = 0 and t = 1/jlo"""
    if f[1] != 'inf' or f[10] != '0':
        return False
    alo, ahi, clo, chi = Fr(f[4]), Fr(f[5]), Fr(f[8]), Fr(f[9])
    return clo <= chi and all(alo <= t * clo and t * chi <= ahi for t in (Fr(0), 1 / Fr(f[0])))


v19 = dict((ln.split()[1], ln.split()[0]) for ln in open(V19[0]) if ln.strip())
wa_bad, wa_lines, same_bad, nsame, nwant, wa_plant = [], [], [], 0, 0, None
for N in (4, 3):
    r, o = rowsets.get(('C', N), ({}, []))
    nwant += len(o) - 2
    last = sorted(set(k.rsplit('_', 1)[0] for k in r if r[k].split()[1] == 'inf'))
    if len(last) != 1:
        wa_bad.append('N%d: %d last pieces' % (N, len(last)))
        continue
    for e in ('h-1', 'h0'):
        f = r['%s_%s' % (last[0], e)].split()
        if not waya_row_ok(f):
            wa_bad.append('%s_%s' % (last[0], e))
        wa_lines.append('%s_%s Axc [%s, %s] Axf %s' % (last[0], e, f[8], f[9], f[10]))
        if wa_plant is None:
            wa_plant = waya_row_ok(f[:9] + [str(2 * Fr(f[0]) * Fr(f[5]))] + f[10:])
    p19 = E + '/out/cert/MR_EXACT_PART_v1_9_C_N%d.kv' % N
    if v19.get(p19) != sha(p19):
        same_bad.append('N%d: the v1_9 part is not its manifest row' % N)
        continue
    _, r19, o19 = read_kv(p19)
    skip = set('%s_%s' % (last[0], e) for e in ('h-1', 'h0'))
    if [k for k in o19 if k not in skip] != [k for k in o if k not in skip]:
        same_bad.append('N%d: row keys or order' % N)
    for k in o19:
        if k not in skip:
            nsame += 1
            if r.get(k) != r19[k]:
                same_bad.append(k)
gate('C-WAYA-ROWS', not wa_bad and len(wa_lines) == 4, '(the last piece of each N, variant C: h-1 and h0 rows with Axf 0, Axc_lo <= Axc_hi and t Axc '
     'inside [Ax_lo, Ax_hi] at t = 0 and 1/jlo: %s%s)' % ('; '.join(wa_lines), ('; failures ' + ', '.join(wa_bad)) if wa_bad else ''))
plant('PLANT-WAYA-ROWS', wa_plant is False, '(the first such row with Axc_hi = 2 jlo Ax_hi, so that t Axc_hi leaves the amplitude at t = 1/jlo, '
      'must fail the row test)')
gate('C-SAME-V1_9', not same_bad and nsame == nwant and nsame > 0, '(every row of the C parts but the last piece\'s h-1 and h0 equals the row of '
     'v1_9\'s certified C part (MANIFEST_MRX_CERT_v1_9 %s), with the same keys in the same order: %d rows of %d%s)' % (
         V19[1][:8], nsame, nwant, ('; failures ' + ', '.join(same_bad[:5])) if same_bad else ''))
'''
t = rep(t, "hU = heads.get(('U', 4), {})\n", GATES + "hU = heads.get(('U', 4), {})\n", 1, 'R14 C-WAYA-ROWS, C-SAME-V1_9')
t = rep(t, "    path = os.path.join(OUTD, 'MR_EXACT_CERT_v1_9_%s.kv' % V)\n", "    path = os.path.join(OUTD, 'MR_EXACT_CERT_v1_10_%s.kv' % V)\n", 1, 'R15 record name')
t = rep(t, "MR_LEMMAP (mrx_cert_v1_9 parts N = 4 and 3, '\n            'joined by mrx_combine_v1_9; h-1, h0, t-1, a0; with Pe_hi); errors: %s'",
        "MR_LEMMAP (mrx_cert_v1_10 parts N = 4 and 3, '\n            'joined by mrx_combine_v1_10; h-1, h0, t-1, a0; with Pe_hi; Way A for h-1 and h0 on the last piece); errors: %s'", 1,
        'R16 comment line')
t = rep(t, "'PRODUCER = pk22 mrx_cert_v1_9 CERT_%s' % V,", "'PRODUCER = pk22 mrx_cert_v1_10 CERT_%s' % V,", 1, 'R17 producer')
t = rep(t, "'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_9.py:%s' % CSHA[:8],", "'CODE = pk22/midrow/g4/mrc/src/mrx_cert_v1_10.py:%s' % CSHA[:8],", 1,
        'R18 code line')
t = rep(t, "'JOINED_BY = pk22/midrow/g4/mrc/src/mrx_combine_v1_9.py:%s' % SELF[:8]", "'JOINED_BY = pk22/midrow/g4/mrc/src/mrx_combine_v1_10.py:%s' % SELF[:8]",
        1, 'R19 joined-by line')
t = rep(t, "            'FIELDS = %s' % h4.get('FIELDS')]\n", "            WAYA_FORM,   # mrx_combine_v1_10\n            'FIELDS = %s' % h4.get('FIELDS')]\n", 1,
        'R20 WAYA_FORM line')
od, nd = defs(old), defs(t)
chg = sorted(k for k in od if k in nd and od[k] != nd[k])
new = sorted(k for k in nd if k not in od)
gone = sorted(k for k in od if k not in nd)
print('DEFS identical %d, changed %s, added %s, dropped %s' % (len([k for k in od if k in nd and od[k] == nd[k]]), chg, new, gone))
assert not chg and not gone and new == ['waya_row_ok'], (chg, new, gone)
left = [ln for ln in t.splitlines() if 'v1_9' in ln]
print('LINES still naming v1_9: %d' % len(left))
with open(DST, 'x') as fh:
    fh.write(t)
with open(DIFF, 'x') as fh:
    fh.writelines(difflib.unified_diff(old.splitlines(True), t.splitlines(True), 'mrx_combine_v1_9.py', 'mrx_combine_v1_10.py'))
print('WROTE %s %s (%d lines)' % (sha(DST), DST, t.count('\n')))
print('WROTE %s %s' % (sha(DIFF), DIFF))
