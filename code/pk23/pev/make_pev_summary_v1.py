#!/usr/bin/env python3
"""make_pev_summary_v1.py (pk23, option B Pev entries; the P0_LOG rows 4409, 4422, 4435): writes pk23/pev/PEV_L_RECORDS_v1.md,
the summary of the certified L-graph records m3_hl_<G>_N<N>_J300_hl.json (G = L, LH, LT; N = 4, 3) in pk23/pev/out. Every number in
the summary is read from the records or computed from them here, in exact rational arithmetic on the records' floats, rounded outward
(lower ends down, upper ends up). Checks by tool: each record's trial set equals the TRIAL_SET of pk25/mr/v3/MR_LEMMAP.kv for its N;
its entry list is HL_ENTRY_LIST_v1.json by name and sha256; its runner sha is m3_run_v1_9_3_hl_v1.py's; its keys are the list's keys of
its graph; J_REF, N and claim_ball as expected. Usage: make_pev_summary_v1.py STAMP (STAMP = the date -u time of the run, for the text)."""
import hashlib, json, math, os, re, sys
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as Q
W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
OUTD = HLD + '/out'
DST = HLD + '/PEV_L_RECORDS_v1.md'
LISTF = 'HL_ENTRY_LIST_v1.json'
RUNF = 'm3_run_v1_9_3_hl_v1.py'
MRL = W18 + '/pk25/mr/v3/MR_LEMMAP.kv'
GRAPHS = ('L', 'LH', 'LT')
BOND = {'TT,0,0': ('-', 0), 'TTh,0,0': ('- (control on LH)', 0), 'Mh,0,0': ('h (4,7)', 1), 'Mhh,0,0': ('h (4,7)', 2),
        'Mt,0,0': ('t (3,6)', 1), 'Mtt,0,0': ('t (3,6)', 2)}
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
    gh = 1 - 2 * math.sqrt(3.0 / 7) / 3
    gt = 1 - math.sqrt(0.2) / 2 - math.sqrt(3.0 / 7) / 6
    ch, ct = (N - 1) * gh / 2, (N - 1) * gt / 2
    return {'TT,0,0': 1.0, 'TTh,0,0': 1.0, 'Mh,0,0': ch, 'Mhh,0,0': ch * ch * (N + 1) / (N - 1), 'Mt,0,0': ct,
            'Mtt,0,0': ct * ct * (N + 1) / (N - 1)}[key]


assert len(sys.argv) == 2 and re.fullmatch(r'20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', sys.argv[1]), 'usage: make_pev_summary_v1.py STAMP'
assert os.path.dirname(os.path.abspath(DST)) == HLD and not os.path.exists(DST), DST
LK = json.load(open(os.path.join(HLD, LISTF)))
lsha, rsha = sha(os.path.join(HLD, LISTF)), sha(os.path.join(HLD, RUNF))
mm = re.search(r'^TRIAL_SET = N4 (\S+):([0-9a-f]{64}), N3 (\S+):([0-9a-f]{64})', open(MRL).read(), re.M)
want_ts = {4: '%s:%s' % (mm.group(1), mm.group(2)), 3: '%s:%s' % (mm.group(3), mm.group(4))}
recs, checks, claim = {}, [], set()
for N in (4, 3):
    for G in GRAPHS:
        p = os.path.join(OUTD, 'm3_hl_%s_N%d_J300_hl.json' % (G, N))
        d = json.load(open(p))
        recs[(N, G)] = (p, sha(p), d)
        keys = [e['key'] for e in LK['entries'] if e['graph'] == G]
        ok = (d['trial_set']['ts'] == want_ts[N] and d['entry_list'] == '%s:%s' % (LISTF, lsha) and d['engine']['m3_run_v1_9_3'] == rsha and
              sorted(d['items']) == sorted(keys) and d['J_REF'] == 300 and d['N'] == N and d['graph'] == G and d['format'] == 'M3_RECORD_v1')
        checks.append((os.path.basename(p), ok))
        claim.add(d['claim_ball'])
L = []
L.append('# PEV_L_RECORDS_v1: certified Pev entries on S8\'s L graph (option B; the P0_LOG rows 4409, 4422, 4435)')
L.append('')
L.append('Written by pk23 at %s (date -u) with pk23/pev/make_pev_summary_v1.py (sha256 %s). Every number below is read from the six '
         'records or computed from them by that script in exact rational arithmetic, rounded outward.' % (sys.argv[1], sha(os.path.abspath(__file__))[:16]))
L.append('')
L.append('## 1. What the records certify')
L.append('- The entries are <psi_0, T M_e^k T psi_0> / lambda_0^2 for k = 0, 1, 2, on S8\'s L graph [vac|int|int|vac] (12 vertices), with')
L.append('  xi^k on the middle bond: h = (4,7) (graph LH, keys Mh,0,0 and Mhh,0,0) and t = (3,6) (graph LT, keys Mt,0,0 and Mtt,0,0); k = 0 is')
L.append('  TT,0,0 on L. TTh,0,0 is TT on LH, a control. psi_0 is state 0 of the z9sym trial set, the TRIAL_SET of pk25/mr/v3/MR_LEMMAP.kv.')
L.append('- The records\' claim (one text in all six): "%s". Here t = 1/J and J_REF = 300.' % ' | '.join(sorted(claim)))
L.append('')
L.append('## 2. Records')
L.append('')
L.append('| record | sha256 | N | graph | keys |')
L.append('|---|---|---|---|---|')
for (N, G), (p, h, d) in recs.items():
    L.append('| %s | %s | %d | %s | %s |' % (os.path.basename(p), h, N, G, ', '.join(sorted(d['items']))))
L.append('')
L.append('Runner pk23/pev/%s (sha256 %s); entry list pk23/pev/%s (sha256 %s).' % (RUNF, rsha, LISTF, lsha))
L.append('')
L.append('Checks by this script (trial set = MR_LEMMAP.kv TRIAL_SET for N; entry list and runner by sha256; keys = the list\'s keys of the '
         'graph; J_REF 300, N, graph and format): %s.' % ', '.join('%s %s' % (f, 'PASS' if ok else 'FAIL') for f, ok in checks))
L.append('')
for N in (4, 3):
    L.append('## %d. Values at N = %d' % (3 if N == 4 else 4, N))
    L.append('')
    L.append('Columns: a_k as mid +- rad; sum Bp; the enclosure of I(J)/main(J) at J = 300; the enclosure for every J >= 300 (t in [0, 1/300], '
             'each a_k t^k between 0 and its value at t = 1/300); the exact order-0 value (Gaussian free field of the infinite 3-row strip, '
             'as in rtwin_hl_v1\'s C-T0) and a_0 minus it (float).')
    L.append('')
    L.append('| key | bond, k | a_0 | a_1 | a_2 | a_3 | sum Bp | at J = 300 | every J >= 300 | exact a_0 | a_0 - exact |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    at300 = {}
    for G in GRAPHS:
        d = recs[(N, G)][2]
        for key in sorted(d['items']):
            it = d['items'][key]
            ak, rk = [Q(x) for x in it['ak']], [Q(x) for x in it['ak_rad']]
            bp = sum(Q(it['Bp'][p_]) for p_ in ('rem', 'tail', 'ann', 'far'))
            l300 = sum((a - r) * TMAX ** k for k, (a, r) in enumerate(zip(ak, rk))) - bp
            h300 = sum((a + r) * TMAX ** k for k, (a, r) in enumerate(zip(ak, rk))) + bp
            lall = ak[0] - rk[0] + sum(min(Q(0), (a - r) * TMAX ** k) for k, (a, r) in enumerate(zip(ak, rk)) if k >= 1) - bp
            hall = ak[0] + rk[0] + sum(max(Q(0), (a + r) * TMAX ** k) for k, (a, r) in enumerate(zip(ak, rk)) if k >= 1) + bp
            at300[key] = (l300, h300)
            ex = exact0(key, N)
            L.append('| %s | %s, %d | %s | %s | %s | %s | %s | [%s, %s] | [%s, %s] | %.13f | %.2e |' % (
                key, BOND[key][0], BOND[key][1], *['%.13g +- %.1e' % (float(a), float(r)) for a, r in zip(ak, rk)], hi(bp),
                lo(l300), hi(h300), lo(lall), hi(hall), ex, float(ak[0]) - ex))
    L.append('')
    tl, th = at300['TT,0,0']
    if tl > 0:
        L.append('Ratios to TT,0,0 at J = 300 (enclosures from the J = 300 columns, all positive): %s.' % '; '.join(
            '%s / TT,0,0 in [%s, %s]' % (k, lo(at300[k][0] / th), hi(at300[k][1] / tl)) for k in ('TTh,0,0', 'Mh,0,0', 'Mhh,0,0', 'Mt,0,0', 'Mtt,0,0')
            if at300[k][0] > 0))
    L.append('')
text = '\n'.join(L) + '\n'
with open(DST, 'x') as fh:
    fh.write(text)
print('SUMMARY %s %s; checks %s' % (hashlib.sha256(text.encode('utf-8')).hexdigest(), DST, 'PASS' if all(ok for _, ok in checks) else 'FAIL'))
