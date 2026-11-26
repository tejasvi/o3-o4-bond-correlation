#!/usr/bin/env python3
"""mrasm2lean_v1_1.py (read-only): turns M1's assembly record (MR_ASSEMBLY_KV_v1, engine kt_mr_assembly_v1_8_4) into the body of
StripIIIM1.M1List's list `m1List`: one entry (n, e, f) per class row, the row's representative as Lean edge codes, from the 1-based names
h_i = hor 1 (i-1), t_j = hor 0 (j-1), bb_j = hor 2 (j-1), a_j = ver 0 (j-1), b_j = ver 1 (j-1). Rows: "N<N>_n<nn>_h<i>-<T><j> = route d k
dp m Lmin piece verdict Hmin".
v1_1 over v1 (the N-2 on the dry build): the third argument is the record's MR_SPECTRAL input, which holds the J grid. Its sha256
must equal the record's INPUT_PINS pin of MR_SPECTRAL.kv; at each N the pieces of the record's PIECES_N<N> line must be consecutive rows
N<N>_P<k> of it that join without a gap (each jhi is the next jlo), the last running to J = inf, and the first starting at or below
jLow N (350 at N = 4, 300 at N = 3), which hM1's J >= jLow N relies on; every row's piece must be one of its N's pieces. A second comment
line prints the grid.
Checks in both modes: FORMAT = MR_ASSEMBLY_KV_v1; the same class set at N = 4 and N = 3; the header's NMAX is the largest n of the rows;
the COUNT line matches the rows; for every row: the pair is a to-do pair (valid, distinct, a middle-row edge, no common vertex, not a
left-right mirror pair), not the end same-bond orbit, n = d + m + dp + 4, and no two rows share an orbit (the key of StripIIIM1.HCore's
`canonKey`); the grid above. CERTIFIED mode also requires MODE = CERTIFIED, PLANT = none, RUN_VERDICT = VALID and every row PASS, and the
spectral record's STATUS = CERTIFIED; DRY mode reads a rehearsal record and marks its source line DRY.
Prints the fragment: a source line, a grid line, per n a comment line (class counts by route at N = 4, least Hmin at each N) and the
entries in the record's row order, a total line. Usage: mrasm2lean_v1_1.py CERTIFIED|DRY RECORD SPECTRAL"""
import hashlib
import re
import sys

JLOW = {4: 350.0, 3: 300.0}


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
    mode, path, spath = sys.argv[1], sys.argv[2], sys.argv[3]
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
    nmax = int(head['NMAX'])
    fails = [k for k, v in rows.items() if v[7] != 'PASS']
    assert all(v[7] in ('PASS', 'FAIL') for v in rows.values()), 'verdict not PASS or FAIL'
    cnt_line = 'rows %d pass %d fail %d' % (len(rows), len(rows) - len(fails), len(fails))
    assert head.get('COUNT') == cnt_line, ('COUNT', head.get('COUNT'), cnt_line)
    if mode == 'CERTIFIED':
        assert head.get('MODE') == 'CERTIFIED' and head.get('PLANT') == 'none' and head.get('RUN_VERDICT') == 'VALID', (
            head.get('MODE'), head.get('PLANT'), head.get('RUN_VERDICT'))
        assert not fails, ('rows not PASS', len(fails))
    pins = dict(t.rsplit(':', 1) for t in head['INPUT_PINS'].split())
    spec_raw = open(spath, 'rb').read()
    spec_sha = hashlib.sha256(spec_raw).hexdigest()
    assert pins.get('MR_SPECTRAL.kv') == spec_sha, ('MR_SPECTRAL pin', pins.get('MR_SPECTRAL.kv'), spec_sha)
    pieces = {N: [int(x) for x in head['PIECES_N%d' % N].split()] for N in (4, 3)}
    g = grid(spec_raw, pieces, mode)
    for (N, n, i, t), v in rows.items():
        assert int(v[6]) in pieces[N], ('row piece not in PIECES', N, n, i, t, v[6])
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
        key = (n, canon(e, f, n))
        assert key not in seen, ('two rows in one orbit', n, i, t, seen.get(key))
        seen[key] = (i, t)
        out.append((n, e, f, v[0], i, t))
    code_pin = head.get('CODE', '').rsplit(':', 1)[-1][:8]
    print('-- source %s sha256 %s; %smode %s; code %s; NMAX %d; run verdict %s; rows N4 %d N3 %d; fail rows %d' % (
        path, hashlib.sha256(raw).hexdigest(), 'DRY ' if mode == 'DRY' else '', head.get('MODE'), code_pin, nmax,
        head.get('RUN_VERDICT'), len(sets[4]), len(sets[3]), len(fails)))
    print('-- J grid: MR_SPECTRAL.kv sha256 %s; N4 pieces %d..%d (%d) from J %s to inf (jLow 350); N3 pieces %d..%d (%d) from J %s to inf'
          ' (jLow 300)' % ((spec_sha,) + g[4] + g[3]))
    lines = []
    for n in sorted({x[0] for x in out}):
        sel = [x for x in out if x[0] == n]
        cnt = {r: sum(1 for x in sel if x[3] == r) for r in ('chan-exact', 'chan-crude', 'same-bond')}
        assert sum(cnt.values()) == len(sel), ('unknown route at n', n)
        hmin = {N: min(float(rows[(N, n, x[4], x[5])][8]) for x in sel) for N in (4, 3)}
        lines.append('  -- n=%d: %d classes (routes at N4: chan-exact %d, chan-crude %d, same-bond %d); least Hmin N4 %.6g N3 %.6g' % (
            n, len(sel), cnt['chan-exact'], cnt['chan-crude'], cnt['same-bond'], hmin[4], hmin[3]))
        for x in sel:
            lines.append('  (%d, %s, %s),' % (x[0], lean(x[1]), lean(x[2])))
    last = max(j for j, s in enumerate(lines) if not s.startswith('  --'))
    lines[last] = lines[last][:-1]
    print('\n'.join(lines))
    print('-- total %d classes' % len(out))


if __name__ == '__main__':
    main()
