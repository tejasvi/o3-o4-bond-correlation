#!/usr/bin/env python3
"""job107 (pk25, C6a v3 pre-check): compares, on every piece, the widths of the law-based unit-basis Ritz coefficients of the C6b dry run
e7 (asm/out/uhat_kt_s9h_ins_v1_5_e7.tsv) with MR_LEMMAP v2's (mr/v2/MR_LEMMAP.kv), exactly (Fraction of the decimal strings). Prints, per
N and field, the number of pieces where the law-based width exceeds v2's, the largest such excess and the pieces. Read only; no record."""
import sys
from fractions import Fraction

D = '/mnt/g2/release/root/code/pk25/'
UH = D + 'asm/out/uhat_kt_s9h_ins_v1_5_e7.tsv'
LM = D + 'mr/v2/MR_LEMMAP.kv'


def main():
    rows = {}
    with open(UH) as fh:
        head = fh.readline().rstrip('\n').split('\t')
        for ln in fh:
            f = ln.rstrip('\n').split('\t')
            rows['N%s_P%s' % (f[0], f[1])] = dict(zip(head, f))
    v2, flds = {}, None
    with open(LM) as fh:
        for ln in fh:
            if ln.startswith('FIELDS = '):
                flds = ln.split(' = ', 1)[1].split()
            elif ln.startswith('N') and ' = ' in ln and flds is not None:
                k, v = ln.rstrip('\n').split(' = ', 1)
                v2[k] = dict(zip(flds, v.split()))
    names = [h[:-3] for h in head if h.endswith('_lo')]
    if set(rows) != set(v2):
        print('STOP: the piece keys differ (%d against %d)' % (len(rows), len(v2)))
        return 6
    for N in ('4', '3'):
        for nm in names:
            bad = []
            for k in sorted(r for r in rows if r.startswith('N%s_' % N)):
                w3 = Fraction(rows[k][nm + '_hi']) - Fraction(rows[k][nm + '_lo'])
                w2 = Fraction(v2[k][nm + '_hi']) - Fraction(v2[k][nm + '_lo'])
                if w3 > w2:
                    bad.append((k, float((w3 - w2) / w2)))
            print('N%s %s: law-based wider than v2 on %d pieces%s' % (N, nm, len(bad), (': largest relative excess %.3e; first %s' % (
                max(b[1] for b in bad), ', '.join(b[0] for b in bad[:6]))) if bad else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
