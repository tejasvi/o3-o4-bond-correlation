#!/usr/bin/env python3
"""make_o5_record_table_v3.py (pk23; = make_o5_record_table_v2.py fa51f1b3 with the g37fs v1_1 07ef4b51 added to the engines, for kit v7b; v2 is = v1 1b1fe167 for kits v5 to v7): the record table of one pulled O5 box run
folder, one TSV row per engine output o5_<TAG>.out, every field read from the run's own files by this tool. Changes from v1:
  - job lists of kit v5 (14 columns), kit v6 (16: ENGINE and REF after LIM) and kit v7 (17: NCELL at the end) are read; args_match
    compares the output's ARGS line, its first line (LIM) and its SCAN line (NCELL, 64 when absent) with the job's line;
  - engine_ok checks the first line's sha256 against the job's ENGINE file (g37 8677a368, g37lzd a87bf335, g37fs 013b521b);
  - a job whose tag starts with "c" is in group control (kit v6 and v7 controls), others by label as in v1 (O5, required, cross-check,
    small-c2, D1);
  - new columns: engine, ncell, cells_failing and cells_digest (from a CELLS line, g37fs with NCELL > 64), cmp (the job's .cmp line),
    and the sigma of the R-CERT line.
Lines starting with # follow the table: FLAG lines (certified not True or L <= 0, a verdict not VALID, rc not 0, no C-H line, an ARGS,
NCELL or engine mismatch, a CHECK line without PASS, an R-CERT c2 that differs from the ORBIT line, a .cmp file not at 0 lines) and
COUNT lines per group. Reads only the run folder and the job lists; writes stdout. Usage: make_o5_record_table_v2.py RUN_FOLDER JOBLIST..."""
import hashlib, os, re, sys
from decimal import Decimal
from fractions import Fraction

ENGINES = {'kt_lbu_g37_v1.py': '8677a368f47e8c25b2924ac8f4927a537afbdb0c233e369dff2133c79268f2a3',   # G-ORIG: the sha256 this engine printed of itself as it ran
           'kt_lbu_g37lzd_v1.py': 'a87bf3359413f5832fdc898d7410cc9e2b33b9a6ff33653fd9a586859d79a3bc',   # G-ORIG: the sha256 this engine printed of itself as it ran
           'kt_lbu_g37fs_v1.py': '013b521bf7e2c93eca637147a7ed2425bbfbe15ad2d50b62c2c32cb5a339c1d4',   # G-ORIG: the sha256 this engine printed of itself as it ran
           'kt_lbu_g37fs_v1_1.py': '07ef4b512e3d2b8de46df4334c435075d51c975f40e91974c018dd7edcceb2f8'}   # G-ORIG: the sha256 this engine printed of itself as it ran
GROUPS = {'O5': ['n6_G27', 'n6_G46', 'n7_G55'],
          'required': ['n5_G12', 'n5_G13', 'n5_G26', 'n5_G27', 'n5_G06', 'n5_G21'],
          'cross-check': ['n5_G%s' % g for g in ('01', '07', '09', '10', '14', '22', '23', '24', '25', '28', '29')],
          'small-c2': ['n5_G%s' % g for g in ('08', '11', '15', '16')],
          'D1': ['n5_G%s' % g for g in ('02', '03', '04', '05', '17', '18', '19', '20', '30', '31', '32', '33', '34', '35', '36')]}
GROUP_OF = {lab: g for g, labs in GROUPS.items() for lab in labs}
COLS = ['label', 'N', 'K', 'group', 'job', 'list', 'engine', 'ncell', 'orbit', 'size', 'middle_row', 'distance', 'members', 'c2_exact',
        'c2', 'J1', 'sigma', 'certified', 'L', 'L_over_c2', 'headroom', 'status', 'checks', 'plants', 'verdict', 'cpu_s', 'wall_s',
        'peak_RSS_MB', 'CH_PASS', 'CHECK_not_PASS', 'cells_failing', 'cells_digest', 'rc', 'rc_time', 'cmp', 'guard_coreh', 'args_match',
        'engine_ok', 'out_sha256', 'out_lines', 'line_ORBIT', 'line_RCERT', 'line_CCELLS', 'line_SUMMARY']


def job_fields(f):
    """(LIM, ENGINE, K ROWS COLS N J1 ORBIT SIGMA CONTROLS MEMSTOP, NCELL) from a job-list line of 14, 16 or 17 columns."""
    if len(f) == 14:
        return f[4], 'kt_lbu_g37_v1.py', f[5:14], '64'
    if len(f) == 16:
        return f[4], f[5], f[7:16], '64'
    if len(f) == 17:
        return f[4], f[5], f[7:16], f[16]
    return None


d = sys.argv[1]
jobs = {}
for jl in sys.argv[2:]:
    for ln in open(jl):
        f = ln.split()
        if f and not ln.startswith('#') and job_fields(f):
            jobs[f[1]] = (os.path.basename(jl), job_fields(f))
rows, flags = [], []
for fn in sorted(os.listdir(d)):
    m = re.fullmatch(r'o5_(.+)\.out', fn)
    if not m:
        continue
    tag = m.group(1)
    raw = open(os.path.join(d, fn), 'rb').read()
    txt = raw.decode(errors='replace').splitlines()
    r = dict.fromkeys(COLS, '-')
    r['job'], r['out_sha256'], r['out_lines'] = tag, hashlib.sha256(raw).hexdigest(), str(len(txt))
    lst, jf = jobs.get(tag, ('-', None))
    r['list'] = lst
    if jf:
        r['engine'] = jf[1]
    first = txt[0] if txt else ''
    sm = re.search(r' LIM (\d+) .*sha256 ([0-9a-f]{64})$', first)
    r['engine_ok'] = str(bool(sm and jf and ENGINES.get(jf[1]) == sm.group(2)))
    args = next((l for l in txt if l.startswith('ARGS grid: ')), '')
    am = re.match(r'ARGS grid: K (\d+), P_(\d+) x P_(\d+), N (\d+), J1 (\d+) \(.*\), ORBS (\S+), SIGS (\S+), CONTROLS (\S+), MEMSTOP (\d+) MB$', args)
    scan = next((l for l in txt if l.startswith('SCAN ncell ')), '')
    r['ncell'] = scan.split()[2] if scan else '64'
    if am:
        r['K'], r['N'], r['J1'] = am.group(1), am.group(4), am.group(5)
        r['label'] = 'n%s_%s' % (am.group(3), am.group(6))
        r['group'] = 'control' if tag.startswith('c') else GROUP_OF.get(r['label'], '-')
    ok = bool(am and sm and jf)
    if ok:
        ok = (sm.group(1) == jf[0] and [am.group(i) for i in range(1, 10)] == list(jf[2]) and r['ncell'] == jf[3])
    r['args_match'] = str(ok)
    c2x = None
    for i, l in enumerate(txt, 1):
        if am and l.startswith('ORBIT %s ' % am.group(6)):
            om = re.match(r'ORBIT \S+ (\(\S+ \S+\)): size (\d+), middle-row (\S+), distance (\d+), .*c2\(N=(\d)\) (-?\d+)/(\d+) \(([-0-9.e+]+)\); members (.*)$', l)
            if om:
                r['orbit'], r['size'], r['middle_row'], r['distance'] = om.group(1), om.group(2), om.group(3), om.group(4)
                c2x = Fraction(int(om.group(6)), int(om.group(7)))
                r['c2_exact'], r['c2'], r['members'], r['line_ORBIT'] = '%s/%s' % (om.group(6), om.group(7)), om.group(8), om.group(9), str(i)
                if om.group(5) != r['N']:
                    flags.append('FLAG %s: ORBIT line c2 is for N=%s, the run has N=%s' % (tag, om.group(5), r['N']))
        elif l.startswith('R-CERT '):
            rm = re.search(r': certified (\S+); sigma (\S+); L ([-0-9.e+]+); c2 ([-0-9.e+]+); L / c2 ([-0-9.e+]+|inf);', l)
            if rm:
                r['certified'], r['sigma'], r['L'], r['L_over_c2'], r['line_RCERT'] = rm.group(1), rm.group(2), rm.group(3), rm.group(5), str(i)
                if r['c2'] != '-' and rm.group(4) != r['c2']:
                    flags.append('FLAG %s: R-CERT c2 %s differs from the ORBIT line c2 %s' % (tag, rm.group(4), r['c2']))
        elif l.startswith('CHECK C-CELLS '):
            r['line_CCELLS'] = str(i)
        elif l.startswith('CELLS '):
            cm = re.search(r'digest sha256 ([0-9a-f]{64}) .*failing cells (\d+)', l)
            if cm:
                r['cells_digest'], r['cells_failing'] = cm.group(1)[:16], cm.group(2)
        elif l.startswith('SUMMARY '):
            um = re.search(r'status (.+?); checks (\d+/\d+); plants (\d+/\d+); VERDICT (\S+); cpu ([0-9.]+) s; wall ([0-9.]+) s; peak RSS (\d+) MB', l)
            if um:
                r['status'], r['checks'], r['plants'], r['verdict'], r['cpu_s'], r['wall_s'], r['peak_RSS_MB'] = um.groups()
                r['line_SUMMARY'] = str(i)
    r['CH_PASS'] = str(sum(1 for l in txt if l.startswith('CHECK C-H ') and ' PASS ' in l))
    r['CHECK_not_PASS'] = str(sum(1 for l in txt if l.startswith('CHECK ') and not re.match(r'CHECK \S+.* PASS( |$)', l)))
    if c2x is not None and r['L'] != '-':
        Lx = Fraction(Decimal(r['L']))
        r['headroom'] = '%.4f' % float(c2x / (c2x - Lx)) if c2x > Lx else 'inf'
    rcf = os.path.join(d, tag + '.rc')
    if os.path.exists(rcf):
        rcs = open(rcf).read().split()
        r['rc'], r['rc_time'] = (rcs + ['-', '-'])[:2]
    cmf = os.path.join(d, tag + '.cmp')
    if os.path.exists(cmf):
        r['cmp'] = open(cmf).read().strip().replace('\t', ' ')
    gf = os.path.join(d, 'GUARD_%s.log' % tag)
    if os.path.exists(gf):
        gm = re.findall(r'total ([0-9.]+) core-h', open(gf).read())
        r['guard_coreh'] = gm[-1] if gm else 'no-total'
    rows.append(r)
    if r['certified'] != 'True' or (r['L'] != '-' and Fraction(Decimal(r['L'])) <= 0):
        flags.append('FLAG %s: certified %s, L %s' % (tag, r['certified'], r['L']))
    if r['verdict'] != 'VALID':
        flags.append('FLAG %s: verdict %s (status %s)' % (tag, r['verdict'], r['status']))
    if r['rc'] != '0':
        flags.append('FLAG %s: rc %s' % (tag, r['rc']))
    if r['CH_PASS'] == '0':
        flags.append('FLAG %s: no CHECK C-H PASS line' % tag)
    if r['args_match'] != 'True' or r['engine_ok'] != 'True':
        flags.append('FLAG %s: args_match %s, engine_ok %s' % (tag, r['args_match'], r['engine_ok']))
    if r['CHECK_not_PASS'] != '0':
        flags.append('FLAG %s: %s CHECK lines without PASS' % (tag, r['CHECK_not_PASS']))
    if r['cmp'] != '-' and not (re.search(r'control compare: 0 differing lines', r['cmp']) and re.search(r'cmp-rc 0(;|$)', r['cmp'])):
        flags.append('FLAG %s: .cmp not at 0 lines: %s' % (tag, r['cmp'][:120]))
print('\t'.join(COLS))
for r in rows:
    print('\t'.join(r[c] for c in COLS))
for f in flags:
    print('# ' + f)
for g in ['control'] + list(GROUPS) + ['-']:
    rs = [r for r in rows if r['group'] == g]
    if rs:
        print('# COUNT group %s: outputs %d, certified True %d, verdict VALID %d, rc 0 %d, headroom >= 2: %d' % (
            g, len(rs), sum(r['certified'] == 'True' for r in rs), sum(r['verdict'] == 'VALID' for r in rs), sum(r['rc'] == '0' for r in rs),
            sum(r['headroom'] not in ('-', 'inf') and float(r['headroom']) >= 2 or r['headroom'] == 'inf' for r in rs)))
print('# COUNT all: outputs %d, flags %d' % (len(rows), len(flags)))
