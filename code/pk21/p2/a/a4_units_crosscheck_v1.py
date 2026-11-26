#!/usr/bin/env python3
"""a4_units_crosscheck_v1.py (pk21, piece A record, note N-b of the review's review c3bd0d38): the units cross-check between the two
exports. R5's certified mixed-kind slack at its threshold (export_c2a_kt_s9h_v1_3_2_sweep.kv, field 'mixed <dmin> <slack_lo>' per
piece) against the e = 0 value f0R of a3_bulk_checks_v1 (R5's mixed kind at e = 0 from R4's t export and the S_V export; a3 row TSVs).
The slack does not increase in e = R_w rho1^d, so on every piece the ratio slack / f0R must lie in (0, 1]; a ratio above 1 would mean
the two forms disagree in units. Prints per N the smallest and largest ratio, the pieces above 1, and that the piece grids agree.
Inputs are pinned by sha256 (prefix) and checked at start.
"""
import hashlib, os, sys
W = '/mnt/g2/release/root/code'
PINS = {
    'R5': (W + '/pk07/out/export_c2a_kt_s9h_v1_3_2_sweep.kv', '089db1ef'),
    'A3N4': (W + '/pk21/p2/a/out/a3_rows_N4_v1.tsv', '32623d2d'),
    'A3N3': (W + '/pk21/p2/a/out/a3_rows_N3_v1.tsv', '31ea1900'),
}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    print('a4_units_crosscheck_v1 sha256 %s' % sha(os.path.abspath(__file__)))
    bad = False
    for k, (p, s8) in PINS.items():
        h = sha(p)
        ok = h.startswith(s8)
        bad = bad or not ok
        print('INPUT %s %s sha256 %s -> %s' % (k, p.replace(W + '/', ''), h, 'PIN OK' if ok else 'PIN MISMATCH'))
    if bad:
        print('VERDICT INVALID (pin)')
        return 1
    r5 = {}
    for line in open(PINS['R5'][0]):
        if not (line.startswith('N4_P') or line.startswith('N3_P')):
            continue
        key, rest = line.split(' = ', 1)
        head, kinds = rest.split('|', 1)
        jlo, jhi = head.split()[:2]
        for part in kinds.split(';'):
            f = part.split()
            if f and f[0] == 'mixed':
                r5[key] = (jlo, jhi, int(f[1]), float(f[2]))
    allok = True
    for N, tag in ((4, 'A3N4'), (3, 'A3N3')):
        rows = [l.rstrip('\n').split('\t') for l in open(PINS[tag][0])]
        hdr, rows = rows[0], rows[1:]
        ip, ijlo, ijhi, if0r = hdr.index('piece'), hdr.index('jlo'), hdr.index('jhi'), hdr.index('f0R')
        ratios, above, gridbad, dmins = [], [], 0, set()
        for r in rows:
            key = r[ip]
            if key not in r5:
                gridbad += 1
                continue
            jlo, jhi, dmin, slack = r5[key]
            if (jlo, jhi) != (r[ijlo], r[ijhi]):
                gridbad += 1
            dmins.add(dmin)
            q = slack / float(r[if0r])
            ratios.append((q, key))
            if q > 1.0 or q <= 0.0:
                above.append(key)
        ok = gridbad == 0 and not above and len(ratios) == len(rows)
        allok = allok and ok
        print('N=%d: %d pieces; grids agree: %s; mixed-kind thresholds dmin %s; ratio slack/f0R from %.4f (%s) to %.4f (%s); outside (0, 1]: '
              '%d -> %s' % (N, len(ratios), 'yes' if gridbad == 0 else 'NO (%d)' % gridbad, sorted(dmins), min(ratios)[0],
                            min(ratios)[1], max(ratios)[0], max(ratios)[1], len(above), 'PASS' if ok else 'FAIL'))
    print('VERDICT %s' % ('VALID' if allok else 'INVALID'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
