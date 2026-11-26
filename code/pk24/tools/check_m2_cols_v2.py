#!/usr/bin/env python3
"""check_m2_cols_v2.py (pk24; M2's certified run, MIDROW_M2_PLAN_v1_3 sect. 1, G6 v1_7 sect. 6). REVISION of check_m2_cols_v1.py (d220d3a7)
for pk25's MR_INSERT v5 (P4): on the last piece's h row of each N, vx_lo and vx_hi are refreshed to the floor-free hull
[min(0, t_1 xc_lo), max(0, t_1 xc_hi)], t_1 = 1/jlo, so they join the allowed fields there. Changes, and nothing else:
  (1) INSERT's allowed fields on that row: xc_lo, xc_hi, xf_hi, vx_lo, vx_hi (v1: the first three);
  (2) an INFO line per such row: the supplied [vx_lo, vx_hi] against the floor-free hull, in exact rationals of the printed decimals (contains,
      or the side that misses). It stops nothing: the engine's G-FACTX is the binding check.
Compares M2's MR_INSERT v5 with the certified mr/v4b (pin 54691bc1) and M2's MR_EXACT v1_10 with the certified v1_9 (pin 98e4e01e), field
strings row by row, before the engine:
  STRUCT  FIELDS and row keys agree (exit 9 otherwise);
  INSERT  every field byte-identical except, on the last piece's h row (jhi = inf), xc_lo, xc_hi, xf_hi, vx_lo and vx_hi (exit 9 otherwise);
          that row has xf_hi = 0 (exit 11) and xc_lo > 0 (exit 12);
  EXACT   every field byte-identical except, on the last piece's h-1 and h0 rows, Ax_lo, Ax_hi, Axc_lo, Axc_hi and Axf_hi (exit 9 otherwise); those
          rows have Axf_hi = 0 (exit 11) and Axc_lo > 0, a certified sign (exit 12).
Prints the counts and the changed last-piece values. Usage: check_m2_cols_v2.py V4B V5 EXA19 EXA110"""
import hashlib, sys
from fractions import Fraction

PINS = {'v4b': '46d3aeb5', 'v19': '3f4d413b'}


def parse(text):
    fields, rows = None, {}
    for ln in text.splitlines():
        if ln.startswith('#') or ' = ' not in ln:
            continue
        k, v = ln.split(' = ', 1)
        k = k.strip()
        if k == 'FIELDS':
            fields = v.split()
        elif fields is not None:
            assert k not in rows, ('repeated row key', k)
            rows[k] = v.split()
    return fields, rows


def vxhull(name, k, row, ix):
    """v2 (2): INFO only. The floor-free hull of v_x on the last piece from xc (X_DEFINITION with xf_hi = 0, p = 1 for h)."""
    jlo, xlo, xhi = Fraction(row[ix['jlo']]), Fraction(row[ix['xc_lo']]), Fraction(row[ix['xc_hi']])
    vlo, vhi = Fraction(row[ix['vx_lo']]), Fraction(row[ix['vx_hi']])
    hlo, hhi = min(Fraction(0), xlo / jlo), max(Fraction(0), xhi / jlo)
    miss = [s for s, ok in (('low side', vlo <= hlo), ('high side', vhi >= hhi)) if not ok]
    print('M2COLS %s VXHULL %s (INFO): vx [%s, %s] against the floor-free hull [%.17g, %.17g] -> %s' % (
        name, k, row[ix['vx_lo']], row[ix['vx_hi']], float(hlo), float(hhi), 'contains' if not miss else 'misses on the ' + ' and '.join(miss)))


def cmp(name, fa, ra, fb, rb, allow_keys, allow_fields, floor_f, lo_f, hull=False):
    if fa != fb or sorted(ra) != sorted(rb):
        print('M2COLS %s STRUCT DIFFER (fields %s, rows %d vs %d)' % (name, fa == fb, len(ra), len(rb)))
        return 9
    ix = dict((f, i) for i, f in enumerate(fa))
    bad, changed, rc = [], [], 0
    for k in sorted(ra):
        allowed = allow_keys(k, ra[k][ix['jhi']])
        for f in fa:
            if ra[k][ix[f]] != rb[k][ix[f]]:
                if allowed and f in allow_fields:
                    changed.append((k, f, ra[k][ix[f]], rb[k][ix[f]]))
                else:
                    bad.append((k, f))
        if allowed:
            if rb[k][ix[floor_f]] != '0':
                print('M2COLS %s STOP: %s %s = %s, not 0 (Way A has no floor)' % (name, k, floor_f, rb[k][ix[floor_f]]))
                rc = rc or 11
            if not float(rb[k][ix[lo_f]]) > 0:
                print('M2COLS %s STOP: %s %s = %s, no certified sign' % (name, k, lo_f, rb[k][ix[lo_f]]))
                rc = rc or 12
            if hull:
                vxhull(name, k, rb[k], ix)
    print('M2COLS %s: rows %d, fields %d; outside the allowed last-piece fields %d differ%s; allowed changes %d' % (
        name, len(ra), len(fa), len(bad), (' (e.g. %s)' % ', '.join('%s %s' % b for b in bad[:3])) if bad else '', len(changed)))
    for c in changed:
        print('M2COLS %s CHANGED %s %s: %s -> %s' % (name, c[0], c[1], c[2], c[3]))
    if bad:
        return 9
    return rc


def main():
    p4b, p5, p19, p110 = sys.argv[1:5]
    b = dict((n, open(p, 'rb').read()) for n, p in (('v4b', p4b), ('v5', p5), ('v19', p19), ('v110', p110)))
    for n in ('v4b', 'v19'):
        s = hashlib.sha256(b[n]).hexdigest()
        assert s.startswith(PINS[n]), (n, s[:8], PINS[n])
    print('M2COLS PINS v4b %s, v1_9 %s; supplied v5 %s, v1_10 %s' % tuple(hashlib.sha256(b[n]).hexdigest()[:8] for n in ('v4b', 'v19', 'v5', 'v110')))
    fa, ra = parse(b['v4b'].decode())
    fb, rb = parse(b['v5'].decode())
    r1 = cmp('INSERT', fa, ra, fb, rb, lambda k, jhi: k.endswith('_h') and jhi == 'inf', ('xc_lo', 'xc_hi', 'xf_hi', 'vx_lo', 'vx_hi'), 'xf_hi',
             'xc_lo', hull=True)
    fa, ra = parse(b['v19'].decode())
    fb, rb = parse(b['v110'].decode())
    r2 = cmp('EXACT', fa, ra, fb, rb, lambda k, jhi: (k.endswith('_h-1') or k.endswith('_h0')) and jhi == 'inf',
             ('Ax_lo', 'Ax_hi', 'Axc_lo', 'Axc_hi', 'Axf_hi'), 'Axf_hi', 'Axc_lo')
    rc = r1 or r2
    print('M2COLS %s' % ('OK: v5 is v4b and v1_10 is v1_9 outside the last piece\'s Way A fields' if rc == 0 else 'STOP rc %d' % rc))
    return rc


if __name__ == '__main__':
    sys.exit(main())
