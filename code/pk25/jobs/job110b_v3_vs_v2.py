#!/usr/bin/env python3
"""job110 (pk25, C6a v3, the P0_LOG row 4363): compares a v3 record pair (MR_SPECTRAL.kv, MR_LEMMAP.kv in the folder argv[1]) with the
certified v2 pair (pk25/mr/v2) on every piece, exactly (Fractions of the written decimals). Per field: an enclosure pair (*_lo, *_hi) must
nest inside v2's (lo3 >= lo2 and hi3 <= hi2); a single *_hi must be <= v2's, a single *_lo >= v2's; tokens copied from inputs (tau_hi,
rho1_hi, Rw_hi) and jlo jhi must be equal. Prints, per record and field, the number of pieces that break this and the width ratio range
(v3 / v2), and the condition (no ux/uy coefficient or s width wider than v2's on any piece). Read only; exit 0 on PASS, 3 on FAIL."""
import sys
from fractions import Fraction

V2 = '/mnt/g2/release/root/code/pk25/mr/v2/'


def read(path):
    head, flds, rows = {}, None, {}
    with open(path) as fh:
        for ln in fh:
            ln = ln.rstrip('\n')
            if not ln.strip() or ln.startswith('#'):
                continue
            k, v = [x.strip() for x in ln.split('=', 1)]
            if k == 'FIELDS':
                flds = v.split()
            elif flds is None:
                head[k] = v
            else:
                rows[k] = dict(zip(flds, v.split()))
    return head, flds, rows


def main():
    if len(sys.argv) != 2:
        print('usage: job110_v3_vs_v2.py V3_FOLDER')
        return 2
    v3dir = sys.argv[1].rstrip('/') + '/'
    bad_total, cond_bad = 0, 0
    for rec in ('MR_SPECTRAL', 'MR_LEMMAP'):
        h2, f2, r2 = read(V2 + rec + '.kv')
        h3, f3, r3 = read(v3dir + rec + '.kv')
        if f2 != f3 or set(r2) != set(r3):
            print('%s: FIELDS or keys differ -> FAIL' % rec)
            return 3
        hd = sorted(k for k in set(h2) | set(h3) if h2.get(k) != h3.get(k))
        print('%s: %d rows, %d fields; header keys that differ from v2: %s' % (rec, len(r3), len(f3), ' '.join(hd)))
        pairs = sorted(set(f[:-3] for f in f3 if f.endswith('_lo') and f[:-3] + '_hi' in f3))
        singles = [f for f in f3 if f not in ('jlo', 'jhi') and f[:-3] not in pairs]
        for nm in pairs:
            nb, rat = 0, []
            for k in r3:
                lo2, hi2 = Fraction(r2[k][nm + '_lo']), Fraction(r2[k][nm + '_hi'])
                lo3, hi3 = Fraction(r3[k][nm + '_lo']), Fraction(r3[k][nm + '_hi'])
                if lo3 < lo2 or hi3 > hi2:
                    nb += 1
                    if nb <= 3:
                        print('    break %s %s: v2 [%s, %s] v3 [%s, %s]' % (k, nm, r2[k][nm + '_lo'], r2[k][nm + '_hi'], r3[k][nm + '_lo'], r3[k][nm + '_hi']))
                rat.append(float((hi3 - lo3) / (hi2 - lo2)) if hi2 > lo2 else 1.0)
            bad_total += nb
            if nm in ('sx', 'sy') or nm.startswith('ux') or nm.startswith('uy'):
                cond_bad += nb
            print('  %s: not nested in v2 on %d pieces; width v3/v2 from %.3e to %.3e' % (nm, nb, min(rat), max(rat)))
        for f in singles:
            nb, same = 0, 0
            for k in r3:
                a2, a3 = r2[k][f], r3[k][f]
                if f in ('tau_hi', 'rho1_hi', 'Rw_hi'):
                    nb += a2 != a3
                    continue
                x2, x3 = Fraction(a2), Fraction(a3)
                if (f.endswith('_hi') and x3 > x2) or (f.endswith('_lo') and x3 < x2):
                    nb += 1
                same += x2 == x3
            bad_total += nb
            print('  %s: %s on %d pieces%s' % (f, 'token differs' if f in ('tau_hi', 'rho1_hi', 'Rw_hi') else 'weaker than v2', nb,
                                               '' if f in ('tau_hi', 'rho1_hi', 'Rw_hi') else ' (equal on %d)' % same))
        for k in r3:
            if (r3[k]['jlo'], r3[k]['jhi']) != (r2[k]['jlo'], r2[k]['jhi']):
                bad_total += 1
    print('MAIN-CONDITION (no ux/uy coefficient or s width wider than v2 on any piece): %s (%d breaks)' % ('PASS' if cond_bad == 0 else 'FAIL', cond_bad))
    print('NESTING (every field inside or equal to v2 on every piece): %s (%d breaks)' % ('PASS' if bad_total == 0 else 'FAIL', bad_total))
    return 0 if (bad_total == 0 and cond_bad == 0) else 3


if __name__ == '__main__':
    sys.exit(main())
