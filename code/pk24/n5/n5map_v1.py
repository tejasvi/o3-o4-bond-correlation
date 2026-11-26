#!/usr/bin/env python3
"""n5map_v1.py (pk24): the per-pair table behind N5_ROUTES_v1_1 (83d76197) sect. 2, for its review. For each D0 pair of class O1
at n = 5 (pk21's variant rows, N4 d5741c8e, N3 ec8c0113): its orbit (T <-> B flip and left-right reflection; img and key verbatim
from n5_orbits_c2_v1.py fad02a32), the number m of bonds between its two edges (m <= 0: joint), the NE n = 5 two-sided classes that
one of its four images is (the maps of pk22's C-REPRO-H and C-REPRO-M: H2 (dL, dR, kind, m) = {t(dL+1), bb(4-dR)} (flip) or
{t(dL+1), t(4-dR)} (same); HV (iH, dV, kind, m) = {t(iH+1), a(4-dV)} (same) or {t(iH+1), b(4-dV)} (flip)), each class's N5ROW
headroom in the rcm6 outputs at both N and every bar, and the box status from n5_orbits_c2_v1.out (cautious headroom >= 2 at both
N). Prints only. FLOAT DATA."""
import re, ast
CODEDIR = '/mnt/g2/release/root/code'
O = CODEDIR + '/pk24'
VR = {4: CODEDIR + '/pk21/p2/w1/out/w1s8_variant_rows_N4_b350_v1_9.tsv', 3: CODEDIR + '/pk21/p2/w1/out/w1s8_variant_rows_N3_b300_v1_9.tsv'}
R6 = {4: O + '/ne/out/out_kt_s8hf_rcm6_n4_scan.out', 3: O + '/ne/out/out_kt_s8hf_rcm6_n3_scan.out'}
ORBF = O + '/n5/out/n5_orbits_c2_v1.out'
GAPC = {4: 3.2e-4, 3: 1.9e-4}   # pk23's cautious gaps (its plan v2, sect. 1)
NC = 5
N5HV = ((0, 1, 1), (1, 0, 1), (2, -1, 1), (0, 0, 2), (1, -1, 2), (0, -1, 3))
N5H2 = ((0, 0, 2), (0, 1, 1), (1, 0, 1))
BARS = [('0.0001', '5e-05'), ('3e-05', '2e-05'), ('0.0003', '0.0001'), ('0.001', '0.0003'), ('0', '0')]


def img(nm, flip, lr):
    ty, i = nm.rstrip('0123456789'), int(nm[len(nm.rstrip('0123456789')):])
    if flip:
        ty = {'t': 'bb', 'bb': 't', 'h': 'h', 'a': 'b', 'b': 'a'}[ty]
    if lr:
        i = (NC - i) if ty in ('t', 'h', 'bb') else (NC + 1 - i)
    return '%s%d' % (ty, i)


def key(p):
    return tuple(sorted(p))


def split(nm):
    ty = nm.rstrip('0123456789')
    return ty, int(nm[len(ty):])


def bonds(p):
    """horizontal bonds strictly between the two edges' columns (horizontal edge j spans columns j and j + 1, vertical edge c sits at
    column c); m <= 0: the two edges share a column (joint)."""
    (t1, i1), (t2, i2) = split(p[0]), split(p[1])
    hz = ('t', 'h', 'bb')
    s1 = (i1, i1 + 1) if t1 in hz else (i1, i1)
    s2 = (i2, i2 + 1) if t2 in hz else (i2, i2)
    if s1 > s2:
        s1, s2 = s2, s1
    return s2[0] - s1[1]


CLS = {}
for kind in ('same', 'flip'):
    for (iH, dV, m) in N5HV:
        nm = frozenset(('t%d' % (iH + 1), '%s%d' % ('a' if kind == 'same' else 'b', 4 - dV)))
        CLS.setdefault(nm, []).append(('M2', ('HV', iH, dV, kind, m)))
for kind in ('flip', 'same'):
    for (dL, dR, m) in N5H2:
        nm = frozenset(('t%d' % (dL + 1), '%s%d' % ('bb' if kind == 'flip' else 't', 4 - dR)))
        CLS.setdefault(nm, []).append(('H2', (dL, dR, kind, m)))
assert len(CLS) == 18 and all(len(v) == 1 for v in CLS.values())

pairs = set()
for N in (4, 3):
    for ln in open(VR[N]).read().split('\n')[1:]:
        f = ln.split('\t')
        if len(f) > 4 and f[0] == 'O1:n=5':
            a, b = f[1].split(',')
            pairs.add(key((a, b)))
d0 = sorted(p for p in pairs if not any(x.startswith('h') for x in p))

RX = re.compile(r'^N5ROW bar \(fT/hT (\S+), S4 HT (\S+)\) (M2|H2) (\(.*?\)) \(P2-13 (\S+)\): (\d+) pieces, failing (\d+), smallest '
                r'headroom (\S+) at piece (\d+)')
RN = re.compile(r'^N5ROW bar \(fT/hT (\S+), S4 HT (\S+)\) (M2|H2) (\(.*?\)) \(P2-13 (\S+)\): no row on any piece')
hr, rc5, absl = {}, {}, {}
for N in (4, 3):
    for ln in open(R6[N]).read().split('\n'):
        mm = RX.match(ln)
        if mm:
            hr[(N, (mm.group(1), mm.group(2)), mm.group(3), ast.literal_eval(mm.group(4)))] = (
                float(mm.group(8)), int(mm.group(7)), int(mm.group(6)), int(mm.group(9)))
            continue
        mm = RN.match(ln)
        if mm:
            hr[(N, (mm.group(1), mm.group(2)), mm.group(3), ast.literal_eval(mm.group(4)))] = None
        if ln.startswith('C-REPRO-RC5') or ln.startswith('N5ABSENT') or ln.startswith('VERDICT') or ln.startswith('  N5REPRO'):
            rc5.setdefault(N, []).append(ln.strip())

box = {}
for ln in open(ORBF).read().split('\n'):
    if ln.startswith('ORB D0 | '):
        f = ln.split(' | ')
        c4, c3 = float(f[3]), float(f[4])
        h4, h3 = float(f[7].split('-')[0]), float(f[8].split('-')[0])
        assert abs(c4 / GAPC[4] - h4) < 0.01 and abs(c3 / GAPC[3] - h3) < 0.01, ln   # the first number is the cautious headroom
        box[f[1]] = (h4 >= 2 and h3 >= 2, h4, h3)

print('n = 5, class O1, D0: %d pairs; rcm6 outputs %s, %s; orbit file %s' % (len(d0), R6[4], R6[3], ORBF))
print('cols: pair | orbit | m | box (cautious headroom N4/N3) | NE n = 5 class(es) | N4 headroom (failing pieces / pieces) at the '
      'primary bar | N3 same | N4 at bars 3e-5, 3e-4, 1e-3, 0 | N3 at the same')
orbit_of, seen = {}, set()
for p in d0:
    if p in seen:
        continue
    orb = sorted(set(key((img(p[0], fl, lr), img(p[1], fl, lr))) for fl in (0, 1) for lr in (0, 1)))
    for q in orb:
        seen.add(q)
        orbit_of[q] = ','.join(orb[0])
tot = {'sep': 0, 'joint': 0, 'cls': 0, 'row2': 0, 'fail': 0, 'mism': 0}
mins = {}
orbrows = {}
for p in sorted(d0, key=lambda q: (orbit_of[q], q)):
    rep_ = orbit_of[p]
    ims = set(key((img(p[0], fl, lr), img(p[1], fl, lr))) for fl in (0, 1) for lr in (0, 1))
    mg = bonds(p)
    assert all(bonds(q) == mg for q in ims)
    cl = sorted(set(c for q in ims for c in CLS.get(frozenset(q), [])), key=str)
    bx = box[rep_]
    if mg <= 0:
        tot['joint'] += 1
    else:
        tot['sep'] += 1
    if cl:
        tot['cls'] += 1
    if any(c[1][-1] != mg for c in cl):
        tot['mism'] += 1
    c0 = cl[0] if cl else None
    hs = {}
    for N in (4, 3):
        for bar in BARS:
            v = [hr.get((N, bar, c[0], c[1])) for c in cl]
            v = [x for x in v if x is not None]
            hs[(N, bar)] = min(v) if v else None
    if c0 is not None and hs[(4, BARS[0])] is not None and hs[(3, BARS[0])] is not None:
        tot['row2'] += 1
        if hs[(4, BARS[0])][1] or hs[(3, BARS[0])][1]:
            tot['fail'] += 1
        for N in (4, 3):
            g = 'box' if bx[0] else 'non-box'
            if (N, g) not in mins or hs[(N, BARS[0])][0] < mins[(N, g)][0]:
                mins[(N, g)] = (hs[(N, BARS[0])][0], p, c0)
    fh = lambda x: ('%.4g (%d/%d)' % (x[0], x[1], x[2])) if x else '-'
    fs = lambda x: ('%.4g' % x[0]) if x else '-'
    print('PAIR %s | %s | m %d | %s (%.2f/%.2f) | %s | %s | %s | %s | %s' % (
        ','.join(p), rep_, mg, 'box' if bx[0] else 'NON-BOX', bx[1], bx[2], ' '.join('%s %s' % (c[0], c[1]) for c in cl) or 'none (joint)',
        fh(hs[(4, BARS[0])]), fh(hs[(3, BARS[0])]), ' '.join(fs(hs[(4, b_)]) for b_ in BARS[1:]),
        ' '.join(fs(hs[(3, b_)]) for b_ in BARS[1:])))
    orbrows.setdefault(rep_, []).append((p, mg, cl, hs, bx))
for rep_ in sorted(orbrows, key=lambda r: (orbrows[r][0][1] <= 0, r)):
    rs = orbrows[rep_]
    h4 = [r[3][(4, BARS[0])][0] for r in rs if r[3][(4, BARS[0])]]
    h3 = [r[3][(3, BARS[0])][0] for r in rs if r[3][(3, BARS[0])]]
    print('ORBIT %s | %d pairs | m %d | %s | %s | N4 smallest %s | N3 smallest %s' % (
        rep_, len(rs), rs[0][1], 'box' if rs[0][4][0] else 'NON-BOX', ' '.join('%s %s' % (c[0], c[1]) for c in rs[0][2]) or 'joint',
        ('%.4g' % min(h4)) if h4 else '-', ('%.4g' % min(h3)) if h3 else '-'))
print('TOTAL D0 pairs %d: separated (m >= 1) %d, joint (m <= 0) %d; pairs with an n = 5 class %d; class m differs from the pair\'s m: %d; '
      'separated pairs with a row at both N (primary bar) %d; of these with a failing piece %d' % (
          len(d0), tot['sep'], tot['joint'], tot['cls'], tot['mism'], tot['row2'], tot['fail']))
for k_ in sorted(mins, key=str):
    v = mins[k_]
    print('SMALLEST N%d %s: %.4g at %s (%s %s)' % (k_[0], k_[1], v[0], ','.join(v[1]), v[2][0], v[2][1]))
for N in (4, 3):
    for ln in rc5.get(N, []):
        print('N%d %s' % (N, ln))
