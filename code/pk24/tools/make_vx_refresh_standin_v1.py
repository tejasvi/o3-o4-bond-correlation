#!/usr/bin/env python3
"""make_vx_refresh_standin_v1.py (pk24): TEST STAND-INS for check_m2_cols_v2.py, from a rehearsal MR_INSERT (Way A xc on the last piece's h
rows). Not records. Writes, each as OUTDIR/<variant>/MR_INSERT.kv, mode 'x', OUTDIR new and under pk24:
  vxref        on each last-piece h row (jhi = inf): vx_lo, vx_hi := the floor-free hull [min(0, xc_lo/jlo), max(0, xc_hi/jlo)] of pk25's P4,
               in exact rationals of the printed decimals, printed with 17 significant digits rounded outward (vx_lo down, vx_hi up);
  plant_other  vxref plus vx_hi of the first non-last h row of N = 4 scaled by 3/2 (check_m2_cols_v2 must stop with rc 9);
  plant_low    vxref with vx_hi of N4's last-piece h row set to the hull's upper end rounded DOWN to 6 digits (the VXHULL INFO line must
               read 'misses on the high side').
Line 1 becomes a comment that names the source; every other line is verbatim except the changed rows. Usage: SRC_INSERT OUTDIR"""
import hashlib, os, sys
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction

W = '/mnt/g2/release/root/code/'


def dec(q, digits, rounding):
    c = Context(prec=digits, rounding=rounding)
    return str(c.divide(Decimal(q.numerator), Decimal(q.denominator)))


def main():
    src, out = sys.argv[1], sys.argv[2]
    assert os.path.realpath(out).startswith(W + 'pk24/') and not os.path.exists(out), out
    raw = open(src, 'rb').read()
    lines = raw.decode().splitlines()
    fields = None
    for ln in lines:
        if ln.startswith('FIELDS = '):
            fields = ln.split(' = ', 1)[1].split()
            break
    ix = dict((f, i) for i, f in enumerate(fields))
    rows = {}
    for n, ln in enumerate(lines):
        if ' = ' in ln and not ln.startswith('#'):
            k, v = ln.split(' = ', 1)
            if k.strip() in ('FIELDS',) or len(v.split()) != len(fields):
                continue
            rows[k.strip()] = (n, v.split())
    last = sorted(k for k, (n, v) in rows.items() if k.endswith('_h') and v[ix['jhi']] == 'inf')
    other = sorted(k for k, (n, v) in rows.items() if k.endswith('_h') and k.startswith('N4_') and v[ix['jhi']] != 'inf')[0]
    assert len(last) == 2, last
    hull = {}
    for k in last:
        v = rows[k][1]
        jlo, xlo, xhi = Fraction(v[ix['jlo']]), Fraction(v[ix['xc_lo']]), Fraction(v[ix['xc_hi']])
        hull[k] = (min(Fraction(0), xlo / jlo), max(Fraction(0), xhi / jlo))
    os.mkdir(out)
    sh = hashlib.sha256(raw).hexdigest()
    for var in ('vxref', 'plant_other', 'plant_low'):
        new = list(lines)
        new[0] = '# MR_INSERT TEST STAND-IN %s (pk24, make_vx_refresh_standin_v1) from %s (sha8 %s); not a record' % (var, src.replace(W, ''), sh[:8])
        for k in last:
            n, v = rows[k]
            v = list(v)
            lo, hi = hull[k]
            v[ix['vx_lo']] = dec(lo, 17, ROUND_FLOOR) if lo != 0 else '0'
            v[ix['vx_hi']] = dec(hi, 17, ROUND_CEILING) if hi != 0 else '0'
            if var == 'plant_low' and k.startswith('N4_'):
                v[ix['vx_hi']] = dec(hi, 6, ROUND_FLOOR)
            new[n] = '%s = %s' % (k, ' '.join(v))
            print('VXREF %s %s: vx [%s, %s] (hull of xc [%s, %s] at jlo %s)' % (var, k, v[ix['vx_lo']], v[ix['vx_hi']], v[ix['xc_lo']], v[ix['xc_hi']],
                                                                             v[ix['jlo']]))
        if var == 'plant_other':
            n, v = rows[other]
            v = list(v)
            v[ix['vx_hi']] = repr(float(Fraction(v[ix['vx_hi']]) * 3 / 2))
            new[n] = '%s = %s' % (other, ' '.join(v))
            print('VXREF plant_other %s: vx_hi -> %s' % (other, v[ix['vx_hi']]))
        os.mkdir(os.path.join(out, var))
        dst = os.path.join(out, var, 'MR_INSERT.kv')
        with open(dst, 'x') as fh:
            fh.write('\n'.join(new) + '\n')
        print('VXREF FILE %s %s' % (hashlib.sha256(open(dst, 'rb').read()).hexdigest(), dst.replace(W, '')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
