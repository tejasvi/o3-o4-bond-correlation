#!/usr/bin/env python3
"""mrasm2lean_m2_v1.py (read-only): checks M2's certified assembly record (MR_ASSEMBLY_KV_v1, engine kt_mr_assembly_v1_8_4,
factored mode with the tail) with its tail record (MR_TAIL_KV_v1) and prints the body of StripIIIM2.M2List's control list `m2Rows`: one
entry (n, e, f, d + 1, m, d' + 1) per finite class row, the row's representative as Lean edge codes (1-based names h_i = hor 1 (i-1),
t_j = hor 0 (j-1), bb_j = hor 2 (j-1), a_j = ver 0 (j-1), b_j = ver 1 (j-1)) with the row's d, m, dp fields; StripIIIM2.M2Check checks
them against `classOf` by decide. The Lean M2 theorem (n >= 12) reads only the tail: TAIL = D0 M0 n0 fills D0_M2 and M0_M2.
Assembly record: FORMAT, FIELDS and COUNT; XMODE factored; TAIL = D0 M0 n0 with n0 = 2 D0 + M0 + 1 and NMAX >= n0; the same class set at
N = 4 and N = 3; every row a to-do pair outside the end orbit with n = d + m + dp + 4, its d, m, dp equal to the class function of
StripIIIM2.M2Core (both orders), no two rows in one orbit, its piece in its N's PIECES line; the J grid of the pinned MR_SPECTRAL (as
mrasm2lean_v1_1.py: consecutive pieces joining without a gap, the last to inf, the first at or below jLow N).
Tail record: FORMAT MR_TAIL_KV_v1 and its FIELDS; CODE, INPUT_PINS, MODE, PLANT, TAIL, PIECES_N4 and PIECES_N3 equal to the assembly
record's; one row per piece of each N; every row's D0 and M0 equal to TAIL's.
CERTIFIED mode also requires MODE = CERTIFIED, PLANT = none, RUN_VERDICT = VALID, TAIL_VERDICT = PASS in both records, every finite row
PASS, the tail COUNT with fail 0, and every tail row with envfail 0, LJfail 0, sign OK, verdict PASS, envL > 0, mtail_t, mtail_a and
mtail_h > 0, qR < 1, qT < 1 and LJmin > 0, and the spectral record's STATUS = CERTIFIED; DRY mode prints the counts of rows that fail
these and marks its source line DRY. Run as python3 -I -B (the gates are asserts; never -O).
Usage: mrasm2lean_m2_v1.py CERTIFIED|DRY RECORD TAILRECORD SPECTRAL"""
import hashlib
import re
import sys

JLOW = {4: 350.0, 3: 300.0}
TAIL_FIELDS = 'D0 M0 nenv envfail envL envclass mtail_t mtail_a mtail_h qR qT sign LJmin LJdR LJfail verdict'


def code(name):
    m = re.fullmatch(r'(h|t|bb|a|b)(\d+)', name)
    assert m, name
    k, i = m.group(1), int(m.group(2)) - 1
    assert i >= 0, name
    return {'h': ('hor', 1, i), 't': ('hor', 0, i), 'bb': ('hor', 2, i), 'a': ('ver', 0, i), 'b': ('ver', 1, i)}[k]


def valid(c, n):
    return (c[1] < 3 and c[2] + 1 < n) if c[0] == 'hor' else (c[1] < 2 and c[2] < n)


def verts(c):
    k, a, b = c
    return {(a, b), (a, b + 1)} if k == 'hor' else {(a, b), (a + 1, b)}


def lr(c, n):
    k, a, b = c
    return (k, a, n - 2 - b) if k == 'hor' else (k, a, n - 1 - b)


def flip(c):
    k, a, b = c
    return (k, 2 - a, b) if k == 'hor' else (k, 1 - a, b)


def num(c):
    k, a, b = c
    return 5 * b + a if k == 'hor' else 5 * b + 3 + a


def pair_num(a, b):
    return min(num(a), num(b)) * 1000 + max(num(a), num(b))


def canon(e, f, n):
    return min(pair_num(e, f), pair_num(flip(e), flip(f)), pair_num(lr(e, n), lr(f, n)), pair_num(lr(flip(e), n), lr(flip(f), n)))


def todo(e, f, n):
    mid = (e[0] == 'hor' and e[1] == 1) or (f[0] == 'hor' and f[1] == 1)
    return valid(e, n) and valid(f, n) and e != f and mid and not (verts(e) & verts(f)) and lr(e, n) != f and lr(f, n) != e


def end_samebond(e, f, n):
    for x, y in ((e, f), (f, e)):
        if x[0] == 'hor' and x[1] == 1 and x[2] in (0, n - 2) and y[0] == 'hor' and y[1] in (0, 2) and y[2] == x[2]:
            return True
    return False


def class_of(n, e, f):
    """StripIIIM2.M2Core.classOf, as (d, m, d')"""
    emid, fmid = e[0] == 'hor' and e[1] == 1, f[0] == 'hor' and f[1] == 1
    h, p = (e, f) if emid and (not fmid or e[2] <= f[2]) else (f, e)
    i, j = h[2], p[2]
    if p[0] == 'ver':
        return (i - 1, j - i - 1, n - j - 2) if j >= i else (n - 3 - i, i - j, j - 1)
    return (i - 1, j - i, n - j - 3) if j >= i else (n - 3 - i, i - j, j - 1)


def lean(c):
    return '.%s %d %d' % c


def read_kv(raw):
    rows = []
    for ln in raw.decode('utf-8').splitlines():
        if ln.startswith('#') or ' = ' not in ln:
            continue
        k, v = ln.split(' = ', 1)
        rows.append((k, v))
    return rows


def grid(spec_raw, pieces, mode):
    head, prow = {}, {}
    for k, v in read_kv(spec_raw):
        m = re.fullmatch(r'N([34])_P(\d+)', k)
        if m:
            key = (int(m.group(1)), int(m.group(2)))
            assert key not in prow, ('spectral row twice', k)
            prow[key] = v.split()
        else:
            head[k] = v
    assert head.get('FORMAT') == 'MR_INPUT_KV_v4' and head.get('RECORD') == 'MR_SPECTRAL', (head.get('FORMAT'), head.get('RECORD'))
    assert head.get('RUN_VERDICT') == 'VALID', head.get('RUN_VERDICT')
    assert head.get('FIELDS', '').split()[:2] == ['jlo', 'jhi'], head.get('FIELDS')
    assert head.get('J_UNIFORMITY', '').startswith('PER-PIECE'), head.get('J_UNIFORMITY')
    if mode == 'CERTIFIED':
        assert head.get('STATUS') == 'CERTIFIED', head.get('STATUS')
    out = {}
    for N in (4, 3):
        ps = pieces[N]
        assert ps and ps == list(range(ps[0], ps[-1] + 1)), ('pieces not consecutive', N)
        for p in ps:
            assert (N, p) in prow, ('no spectral row', N, p)
        for p, q in zip(ps, ps[1:]):
            assert prow[(N, p)][1] == prow[(N, q)][0], ('grid gap', N, p, q)
        assert prow[(N, ps[-1])][1] == 'inf', ('last piece not to inf', N, ps[-1])
        first = float(prow[(N, ps[0])][0])
        assert first <= JLOW[N], ('grid starts above jLow', N, first)
        out[N] = (ps[0], ps[-1], len(ps), prow[(N, ps[0])][0])
    return out


def main():
    mode, path, tpath, spath = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    assert mode in ('CERTIFIED', 'DRY'), mode
    raw = open(path, 'rb').read()
    head, rows, order = {}, {}, []
    for k, v in read_kv(raw):
        m = re.fullmatch(r'N([34])_n(\d+)_(h\d+)-([a-z]+\d+)', k)
        if m:
            key = (int(m.group(1)), int(m.group(2)), m.group(3), m.group(4))
            assert key not in rows, ('row twice', k)
            rows[key] = v.split()
            assert len(rows[key]) == 9, ('fields', k)
            if key[0] == 4:
                order.append(key[1:])
        else:
            assert k not in head, ('header line twice', k)
            head[k] = v
    assert head.get('FORMAT') == 'MR_ASSEMBLY_KV_v1', head.get('FORMAT')
    assert head.get('FIELDS') == 'route d k dp m Lmin piece verdict Hmin', head.get('FIELDS')
    assert head.get('XMODE') == 'factored', head.get('XMODE')
    d0, m0, n0 = (int(x) for x in head['TAIL'].split())
    assert n0 == 2 * d0 + m0 + 1, ('n0 != 2 D0 + M0 + 1', d0, m0, n0)
    nmax = int(head['NMAX'])
    assert nmax >= n0, ('NMAX below n0', nmax, n0)
    fails = [k for k, v in rows.items() if v[7] != 'PASS']
    assert all(v[7] in ('PASS', 'FAIL') for v in rows.values()), 'verdict not PASS or FAIL'
    cnt_line = 'rows %d pass %d fail %d' % (len(rows), len(rows) - len(fails), len(fails))
    assert head.get('COUNT') == cnt_line, ('COUNT', head.get('COUNT'), cnt_line)
    if mode == 'CERTIFIED':
        assert head.get('MODE') == 'CERTIFIED' and head.get('PLANT') == 'none' and head.get('RUN_VERDICT') == 'VALID', (
            head.get('MODE'), head.get('PLANT'), head.get('RUN_VERDICT'))
        assert head.get('TAIL_VERDICT') == 'PASS', head.get('TAIL_VERDICT')
        assert not fails, ('rows not PASS', len(fails))
    pins = dict(t.rsplit(':', 1) for t in head['INPUT_PINS'].split())
    spec_raw = open(spath, 'rb').read()
    spec_sha = hashlib.sha256(spec_raw).hexdigest()
    assert pins.get('MR_SPECTRAL.kv') == spec_sha, ('MR_SPECTRAL pin', pins.get('MR_SPECTRAL.kv'), spec_sha)
    pieces = {N: [int(x) for x in head['PIECES_N%d' % N].split()] for N in (4, 3)}
    g = grid(spec_raw, pieces, mode)
    for (N, n, i, t), v in rows.items():
        assert int(v[6]) in pieces[N], ('row piece not in PIECES', N, n, i, t, v[6])
    # the tail record
    traw = open(tpath, 'rb').read()
    thead, trows = {}, {}
    for k, v in read_kv(traw):
        m = re.fullmatch(r'N([34])_P(\d+)', k)
        if m:
            key = (int(m.group(1)), int(m.group(2)))
            assert key not in trows, ('tail row twice', k)
            trows[key] = v.split()
            assert len(trows[key]) == 16, ('tail fields', k)
        else:
            assert k not in thead, ('tail header line twice', k)
            thead[k] = v
    assert thead.get('FORMAT') == 'MR_TAIL_KV_v1', thead.get('FORMAT')
    assert thead.get('FIELDS') == TAIL_FIELDS, thead.get('FIELDS')
    for k in ('CODE', 'INPUT_PINS', 'MODE', 'PLANT', 'TAIL', 'PIECES_N4', 'PIECES_N3'):
        assert thead.get(k) == head.get(k), ('tail header differs', k)
    assert thead.get('TAIL_VERDICT') == head.get('TAIL_VERDICT'), ('TAIL_VERDICT differs', thead.get('TAIL_VERDICT'))
    for N in (4, 3):
        assert sorted(p for (NN, p) in trows if NN == N) == pieces[N], ('tail rows are not the pieces', N)
    tbad = {}
    for (N, p), v in trows.items():
        assert int(v[0]) == d0 and int(v[1]) == m0, ('tail row D0 M0', N, p)
        checks = {'envfail': v[3] == '0', 'LJfail': v[14] == '0', 'sign': v[11] == 'OK', 'verdict': v[15] == 'PASS',
                  'envL': float(v[4]) > 0, 'mtail': min(float(v[6]), float(v[7]), float(v[8])) > 0,
                  'qR': float(v[9]) < 1, 'qT': float(v[10]) < 1, 'LJmin': float(v[12]) > 0}
        for c, ok in checks.items():
            if not ok:
                tbad[c] = tbad.get(c, 0) + 1
    tfail = sum(1 for v in trows.values() if v[15] != 'PASS')
    tcnt = 'rows %d pass %d fail %d' % (len(trows), len(trows) - tfail, tfail)
    assert thead.get('COUNT') == tcnt, ('tail COUNT', thead.get('COUNT'), tcnt)
    if mode == 'CERTIFIED':
        assert thead.get('TAIL_VERDICT') == 'PASS' and not tbad, ('tail gates', thead.get('TAIL_VERDICT'), tbad)
    # the finite rows
    sets = {N: sorted(k[1:] for k in rows if k[0] == N) for N in (4, 3)}
    assert sets[4] == sets[3], 'class sets differ between N = 4 and N = 3'
    assert max(n for n, _, _ in sets[4]) == nmax, 'NMAX differs from the rows'
    seen = {}
    out = []
    for n, i, t in order:
        e, f = code(i), code(t)
        v = rows[(4, n, i, t)]
        d, dp, m = int(v[1]), int(v[3]), int(v[4])
        assert todo(e, f, n), ('not a to-do pair', n, i, t)
        assert not end_samebond(e, f, n), ('the end orbit', n, i, t)
        assert n == d + m + dp + 4, ('n != d + m + dp + 4', n, i, t)
        assert class_of(n, e, f) == (d, m, dp) and class_of(n, f, e) == (d, m, dp), ('class function', n, i, t)
        key = (n, canon(e, f, n))
        assert key not in seen, ('two rows in one orbit', n, i, t, seen.get(key))
        seen[key] = (i, t)
        out.append((n, e, f, d, m, dp))
    code_pin = head.get('CODE', '').rsplit(':', 1)[-1][:8]
    tl = {N: [v for (NN, _), v in trows.items() if NN == N] for N in (4, 3)}
    print('-- source %s sha256 %s; tail %s sha256 %s; %smode %s; code %s; XMODE factored; TAIL D0 %d M0 %d n0 %d; NMAX %d; run verdict %s;'
          ' tail verdict %s; rows N4 %d N3 %d; fail rows %d; tail rows N4 %d N3 %d' % (
              path, hashlib.sha256(raw).hexdigest(), tpath, hashlib.sha256(traw).hexdigest(), 'DRY ' if mode == 'DRY' else '',
              head.get('MODE'), code_pin, d0, m0, n0, nmax, head.get('RUN_VERDICT'), head.get('TAIL_VERDICT'), len(sets[4]),
              len(sets[3]), len(fails), len(tl[4]), len(tl[3])))
    print('-- J grid: MR_SPECTRAL.kv sha256 %s; N4 pieces %d..%d (%d) from J %s to inf (jLow 350); N3 pieces %d..%d (%d) from J %s to inf'
          ' (jLow 300)' % ((spec_sha,) + g[4] + g[3]))
    print('-- tail: least envL N4 %.6g N3 %.6g; least mtail N4 %.6g N3 %.6g; largest qR %.6g, qT %.6g; least LJmin N4 %.6g N3 %.6g;'
          ' rows failing a gate: %s' % (
              min(float(v[4]) for v in tl[4]), min(float(v[4]) for v in tl[3]),
              min(min(float(x) for x in v[6:9]) for v in tl[4]), min(min(float(x) for x in v[6:9]) for v in tl[3]),
              max(float(v[9]) for v in trows.values()), max(float(v[10]) for v in trows.values()),
              min(float(v[12]) for v in tl[4]), min(float(v[12]) for v in tl[3]),
              ', '.join('%s %d' % kv for kv in sorted(tbad.items())) or 'none'))
    lines = []
    for n in sorted({x[0] for x in out}):
        sel = [x for x in out if x[0] == n]
        lines.append('  -- n=%d: %d classes' % (n, len(sel)))
        for x in sel:
            lines.append('  (%d, %s, %s, %d, %d, %d),' % (x[0], lean(x[1]), lean(x[2]), x[3] + 1, x[4], x[5] + 1))
    last = max(j for j, s in enumerate(lines) if not s.startswith('  --'))
    lines[last] = lines[last][:-1]
    print('\n'.join(lines))
    print('-- total %d classes' % len(out))


if __name__ == '__main__':
    main()
