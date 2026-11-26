#!/usr/bin/env python3
"""make_cw_summary_v1.py (pk23, C_w variant B; the P0_LOG rows 4589, 4598, 4610): writes pk23/pev/CW_LC_RECORDS_v1.md, the summary
of the certified C_w records m3_cw_LC_N<N>_J300_cw.json (N = 4, 3) in pk23/pev/out, of their law certificates and of the reader fork that
consumers use. Every number in the summary is read from the records, certificates and job outputs, or computed from them here, in exact rational
arithmetic on the records' floats, rounded outward (lower ends down, upper ends up). Checks by tool: each record's trial set equals the
TRIAL_SET of pk25/mr/v3/MR_LEMMAP.kv for its N; its entry list is HL_CW_ENTRY_LIST_v1.json by name and sha256; its runner sha is
m3_run_v1_9_3_cw_v1.py's; its keys are the list's keys; J_REF, N, graph and format as expected; the asm output names the record with its sha256
on a RECORD line and ends VERDICT VALID; each certificate job's first line names m3_lawcert_cw_v1 with the script's sha256 and its VERDICT is
VALID; the reader check's VERDICT is VALID; the run manifest's rows all match. Usage: make_cw_summary_v1.py STAMP (STAMP = the date -u time of
the run, for the text)."""
import hashlib, json, math, os, re, subprocess, sys
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as Q
W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
OUTD = HLD + '/out'
DST = HLD + '/CW_LC_RECORDS_v1.md'
LISTF = 'HL_CW_ENTRY_LIST_v1.json'
RUNF = 'm3_run_v1_9_3_cw_v1.py'
LAWF = 'm3_lawcert_cw_v1.py'
RDRF, CHKO = 'm3_reader_cw_v1.py', 'out/m3_reader_cw_check_v1_1.out'
RUNMAN = 'MANIFEST_CW_RUN_ABS_v1.sha256'
MRL = W18 + '/pk25/mr/v3/MR_LEMMAP.kv'
KEYS = ('Cxx,1,1', 'Cx1,1,1', 'C1x,1,1', 'C11,1,1')
TMAX = Q(1, 300)
getcontext().prec = 80


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def dec(q, mode, sig=12):
    getcontext().rounding = mode
    d = Decimal(q.numerator) / Decimal(q.denominator)
    if d == 0:
        return '0'
    e = d.adjusted() - (sig - 1)
    return str(d.quantize(Decimal(1).scaleb(e), rounding=mode))


def lo(q):
    return dec(q, ROUND_FLOOR)


def hi(q):
    return dec(q, ROUND_CEILING)


def exact0(key, N):
    """rtwin_cw_v1's C-T0 closed forms (Gaussian free field of the infinite 3-row strip, N - 1 components), in float."""
    lam1, lam2 = (3 - math.sqrt(5)) / 2, (5 - math.sqrt(21)) / 2
    sx0, sy0 = lam1 * lam1, lam2 * lam2
    ch0 = (N - 1) * (1 - 2 * math.sqrt(3.0 / 7) / 3) / 2
    chh = -(2.0 / 3) * (1 - lam2) ** 2 / math.sqrt(21)
    my2sy0 = (N - 1) * chh * chh / 2
    return {'Cxx,1,1': sx0 * sx0 * (ch0 * ch0 + my2sy0 * sy0), 'Cx1,1,1': ch0 * sx0 * sx0, 'C1x,1,1': ch0 * sx0 * sx0, 'C11,1,1': sx0 * sx0}[key]


assert len(sys.argv) == 2 and re.fullmatch(r'20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', sys.argv[1]), 'usage: make_cw_summary_v1.py STAMP'
assert os.path.dirname(os.path.abspath(DST)) == HLD and not os.path.exists(DST), DST
LK = json.load(open(os.path.join(HLD, LISTF)))
NOTE = dict((e['key'], e.get('note', '')) for e in LK['entries'] if e['graph'] == 'LC')
lsha, rsha, lawsha, rdrsha = (sha(os.path.join(HLD, f)) for f in (LISTF, RUNF, LAWF, RDRF))
mm = re.search(r'^TRIAL_SET = N4 (\S+):([0-9a-f]{64}), N3 (\S+):([0-9a-f]{64})', open(MRL).read(), re.M)
want_ts = {4: '%s:%s' % (mm.group(1), mm.group(2)), 3: '%s:%s' % (mm.group(3), mm.group(4))}
recs, checks, claim, certs = {}, [], set(), {}
for N in (4, 3):
    p = os.path.join(OUTD, 'm3_cw_LC_N%d_J300_cw.json' % N)
    d = json.load(open(p))
    h = sha(p)
    recs[N] = (p, h, d)
    asm = open(os.path.join(OUTD, 'm3_run_v1_9_3_asmc.%d.out' % N)).read().split('\n')
    ok = (d['trial_set']['ts'] == want_ts[N] and d['entry_list'] == '%s:%s' % (LISTF, lsha) and d['engine']['m3_run_v1_9_3'] == rsha and
          sorted(d['items']) == sorted(KEYS) and d['J_REF'] == 300 and d['N'] == N and d['graph'] == 'LC' and d['format'] == 'M3_RECORD_v1' and
          ('RECORD %s %s' % (os.path.basename(p), h)) in asm and [x for x in asm if x.startswith('VERDICT')] == ['VERDICT VALID'])
    checks.append((os.path.basename(p), ok))
    claim.add(d['claim_ball'])
    cp, op = os.path.join(OUTD, 'm3_lawcert_cw_v1_N%d.json' % N), os.path.join(OUTD, 'm3_lawcert_cw_v1_%d.out' % N)
    ot = open(op).read().split('\n')
    cj = json.load(open(cp))
    okc = (ot[0].startswith('m3_lawcert_cw_v1 N %d LIM ' % N) and ('; script sha256 %s;' % lawsha) in ot[0] and
           [x for x in ot if x.startswith('VERDICT')] == ['VERDICT VALID'] and ('RECORD %s %s' % (os.path.basename(cp), sha(cp))) in ot and
           cj['records'] == {'LC': {'file': os.path.basename(p), 'sha256': h}})
    checks.append((os.path.basename(cp), okc))
    nf = sum(1 for x in ot if x.startswith('PLANT') and x.endswith('-> FIRES'))
    nn = sum(1 for x in ot if x.startswith('PLANT') and not x.endswith('-> FIRES'))
    ng = sum(1 for x in ot if x.startswith('C-') and x.endswith('-> PASS'))
    certs[N] = (cp, sha(cp), op, sha(op), ng, nf, nn, cj)
so = open(os.path.join(OUTD, 'm3_lawcert_cw_v1_static.out')).read().split('\n')
checks.append(('m3_lawcert_cw_v1_static.out', [x for x in so if x.startswith('VERDICT')] == ['VERDICT VALID'] and ('; script sha256 %s;' % lawsha) in so[0]))
ck = open(os.path.join(HLD, CHKO)).read().split('\n')
checks.append((os.path.basename(CHKO), [x for x in ck if x.startswith('VERDICT')] == ['VERDICT VALID'] and ('fork %s' % rdrsha[:16]) in ck[0]))
mc = subprocess.run(['sha256sum', '-c', os.path.join(HLD, RUNMAN)], capture_output=True, text=True)
mrows = [x for x in mc.stdout.split('\n') if x]
mok = mc.returncode == 0 and mrows and all(x.endswith(': OK') for x in mrows)
checks.append((RUNMAN, mok))
L = []
L.append('# CW_LC_RECORDS_v1: certified C_w entries on the LC graph (variant B of pk25\'s D2_DESIGN_v1_3; the P0_LOG rows 4589, 4598, 4610)')
L.append('')
L.append('Written by pk23 at %s (date -u) with pk23/pev/make_cw_summary_v1.py (sha256 %s). Every number below is read from the two '
         'records, their certificates and job outputs, or computed from them by that script in exact rational arithmetic, rounded outward.'
         % (sys.argv[1], sha(os.path.abspath(__file__))[:16]))
L.append('')
L.append('## 1. What the records certify')
L.append('- The entries of the (1,1) block of |Q S M_c u~_x|^2 (variant B): on the LC graph, which is S8\'s L graph [vac|int|int|vac] with only the')
L.append('  pairs its entries use, (0,2), (9,11), (1,4), (7,10); trial state 1 of the z9sym trial set (the TRIAL_SET of pk25/mr/v3/MR_LEMMAP.kv) on')
L.append('  both vac columns; xi on the outer middle-row bonds (1,4) and (7,10). The prep is L\'s certified D16 prep of m3_run_v1_9_3_hl_v1 (the Pev')
L.append('  release), shared by C-PREP-SHARE. The entry list\'s notes:')
for k in KEYS:
    L.append('  - %s: %s' % (k, NOTE[k]))
L.append('- The records\' claim (one text in both): "%s". Here t = 1/J and J_REF = 300.' % ' | '.join(sorted(claim)))
L.append('')
L.append('## 2. Records, certificates, reader')
L.append('')
L.append('| file | sha256 | N | what |')
L.append('|---|---|---|---|')
for N in (4, 3):
    p, h, d = recs[N]
    L.append('| out/%s | %s | %d | record; keys %s |' % (os.path.basename(p), h, N, ', '.join(sorted(d['items']))))
for N in (4, 3):
    cp, ch, op, oh, ng, nf, nn, cj = certs[N]
    L.append('| out/%s | %s | %d | law certificate (M3_LAWCERT_v1; asm %s %s) |' % (os.path.basename(cp), ch, N, cj['asm']['file'], cj['asm']['sha256'][:16]))
    L.append('| out/%s | %s | %d | its job output: %d gates PASS, %d plants FIRES, %d not firing |' % (os.path.basename(op), oh, N, ng, nf, nn))
L.append('')
L.append('Runner pk23/pev/%s (sha256 %s); entry list pk23/pev/%s (sha256 %s); law-certificate producer pk23/pev/%s (sha256 %s); reader '
         'fork pk23/pev/%s (sha256 %s), check job output pk23/pev/%s (sha256 %s); run manifest pk23/pev/%s (sha256 %s, %d rows).'
         % (RUNF, rsha, LISTF, lsha, LAWF, lawsha, RDRF, rdrsha, CHKO, sha(os.path.join(HLD, CHKO)), RUNMAN, sha(os.path.join(HLD, RUNMAN)), len(mrows)))
L.append('')
L.append('Checks by this script (trial set = MR_LEMMAP.kv TRIAL_SET for N; entry list and runner by sha256; keys = the list\'s keys; J_REF 300, N, '
         'graph and format; the asm output\'s RECORD line and VERDICT; each certificate job\'s producer line, RECORD line, VERDICT and records map; '
         'the static job\'s and the reader check\'s VERDICT; sha256sum -c of the run manifest): %s.'
         % ', '.join('%s %s' % (f, 'PASS' if ok else 'FAIL') for f, ok in checks))
L.append('')
L.append('Consumers load the records with m3_reader_cw_v1.load (bound to m3_run_v1_9_3_asmc.<N>.out) and the laws with load_lawcert (bound to '
         'm3_lawcert_cw_v1_<N>.out), then entry_law(cert, \'LC\', key).')
L.append('')
for N in (4, 3):
    L.append('## %d. Values at N = %d' % (3 if N == 4 else 4, N))
    L.append('')
    L.append('Columns: a_k as mid +- rad; sum Bp; the enclosure of I(J)/main(J) at J = 300; the enclosure for every J >= 300 (t in [0, 1/300], '
             'each a_k t^k between 0 and its value at t = 1/300); the exact order-0 value (rtwin_cw_v1\'s C-T0 closed forms) and a_0 minus it (float).')
    L.append('')
    L.append('| key | a_0 | a_1 | a_2 | a_3 | sum Bp | at J = 300 | every J >= 300 | exact a_0 | a_0 - exact |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    d = recs[N][2]
    for key in KEYS:
        it = d['items'][key]
        ak, rk = [Q(x) for x in it['ak']], [Q(x) for x in it['ak_rad']]
        bp = sum(Q(it['Bp'][p_]) for p_ in ('rem', 'tail', 'ann', 'far'))
        l300 = sum((a - r) * TMAX ** k for k, (a, r) in enumerate(zip(ak, rk))) - bp
        h300 = sum((a + r) * TMAX ** k for k, (a, r) in enumerate(zip(ak, rk))) + bp
        lall = ak[0] - rk[0] + sum(min(Q(0), (a - r) * TMAX ** k) for k, (a, r) in enumerate(zip(ak, rk)) if k >= 1) - bp
        hall = ak[0] + rk[0] + sum(max(Q(0), (a + r) * TMAX ** k) for k, (a, r) in enumerate(zip(ak, rk)) if k >= 1) + bp
        ex = exact0(key, N)
        L.append('| %s | %s | %s | %s | %s | %s | [%s, %s] | [%s, %s] | %.13f | %.2e |' % (
            key, *['%.13g +- %.1e' % (float(a), float(r)) for a, r in zip(ak, rk)], hi(bp), lo(l300), hi(h300), lo(lall), hi(hall), ex,
            float(ak[0]) - ex))
    L.append('')
    L.append('Bar parts at J = 300 (B, from the record) and the certificate\'s far rate:')
    L.append('')
    L.append('| key | rem | tail | ann | far | rnd | far_rate |')
    L.append('|---|---|---|---|---|---|---|')
    cj = certs[N][7]
    for key in KEYS:
        B = d['items'][key]['B']
        fr = Q(cj['entries']['LC:' + key]['laws']['far_rate'])
        L.append('| %s | %s | %s | %s | %s | %s | %s |' % (key, *[hi(Q(B[p_])) for p_ in ('rem', 'tail', 'ann', 'far', 'rnd')], lo(fr)))
    L.append('')
text = '\n'.join(L) + '\n'
with open(DST, 'x') as fh:
    fh.write(text)
print('SUMMARY %s %s; checks %s' % (hashlib.sha256(text.encode('utf-8')).hexdigest(), DST, 'PASS' if all(ok for _, ok in checks) else 'FAIL'))
for f, ok in checks:
    print('CHECK %s %s' % (f, 'PASS' if ok else 'FAIL'))
