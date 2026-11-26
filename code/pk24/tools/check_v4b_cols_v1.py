#!/usr/bin/env python3
"""check_v4b_cols_v1.py (pk24; the P0_LOG rows 4526, 4534, 4536): compares a supplied MR_INSERT (pk25's mr/v4b, or a stand-in) with
pk25/mr/v4/MR_INSERT.kv (pin 21e88843), on which MR_EXACT v1_9, MR_CRUDEX eb4d7511 and MR_JOINT 80bc8d81 were built, before M1's certified
run. Every comparison is of the field strings, row by row:
  STRUCT  FIELDS and the row keys agree;
  C11     the six h-row columns MR_CRUDEX reads (vx, vy, mxx, mxy as lo/hi pairs, Pevw_hi, PeBwux_hi) on every h row (row 4526);
  CHI     C_hi on every h and t row, which MR_JOINT reads (row 4534; the N1 on MR_JOINT);
  NONPEV  every field but Pev_hi and vp_hi on every row (row 4536: the supplied record is v4 with only Pev_hi and vp_hi changed);
  PEV     INFO: the rows whose Pev_hi or vp_hi changed, and whether each is at or below v4's (v4b tightens the same enclosures);
  HEADER  INFO: the header keys whose lines differ (the engine's G-PIN judges the header).
Exit 9 on STRUCT, 8 on C11 (C11 reruns first), 10 on CHI (MR_JOINT reruns first), 9 on any other NONPEV field; else 0.
PLANT (optional) changes one supplied field in memory and must be stopped: C11 (an h row's mxy_hi), CHI (a t row's C_hi), OTHER (an a row's
myy_lo), PEVUP (an h row's Pev_hi raised; INFO only, exit 0).
Usage: check_v4b_cols_v1.py V4 V4B [PLANT]"""
import hashlib, sys
from decimal import Decimal

C11 = ('vx_lo', 'vx_hi', 'vy_lo', 'vy_hi', 'mxx_lo', 'mxx_hi', 'mxy_lo', 'mxy_hi', 'Pevw_hi', 'PeBwux_hi')


def parse(text):
    head, fields, rows = {}, None, {}
    for ln in text.splitlines():
        if ln.startswith('#') or ' = ' not in ln:
            continue
        k, v = ln.split(' = ', 1)
        k = k.strip()
        if k == 'FIELDS':
            fields = v.split()
        elif fields is None:
            head[k] = v.strip()
        else:
            assert k not in rows, ('repeated row key', k)
            rows[k] = v.split()
    return head, fields, rows


def main():
    p4, pb = sys.argv[1], sys.argv[2]
    plant = sys.argv[3] if len(sys.argv) > 3 else None
    assert plant in (None, 'C11', 'CHI', 'OTHER', 'PEVUP'), plant
    b4, bb = open(p4, 'rb').read(), open(pb, 'rb').read()
    s4, sb = hashlib.sha256(b4).hexdigest(), hashlib.sha256(bb).hexdigest()
    assert s4.startswith('e372a2a6'), ('mr/v4 MR_INSERT pin', s4[:8])
    print('V4B PIN mr/v4 MR_INSERT %s (pin 21e88843 OK); supplied %s %s' % (s4, sb, pb))
    h4, f4, r4 = parse(b4.decode())
    hb, fb, rb = parse(bb.decode())
    if plant:
        kh = sorted(k for k in rb if k.endswith('_h'))[0]
        kt = sorted(k for k in rb if k.endswith('_t'))[0]
        ka = sorted(k for k in rb if k.endswith('_a'))[0]
        k_, f_ = {'C11': (kh, 'mxy_hi'), 'CHI': (kt, 'C_hi'), 'OTHER': (ka, 'myy_lo'), 'PEVUP': (kh, 'Pev_hi')}[plant]
        i_ = fb.index(f_)
        rb[k_] = list(rb[k_])
        rb[k_][i_] = str(Decimal(rb[k_][i_]) * 2 + 1) if plant != 'PEVUP' else str(Decimal(r4[k_][i_]) * 2)
        print('V4B PLANT %s: %s %s set to %s' % (plant, k_, f_, rb[k_][i_]))
    struct_ok = f4 == fb and sorted(r4) == sorted(rb) and all(len(r4[k]) == len(f4) for k in r4) and all(len(rb[k]) == len(fb) for k in rb)
    print('V4B STRUCT FIELDS %s; rows v4 %d, supplied %d, missing %d, extra %d; %s' % (
        'identical' if f4 == fb else 'DIFFER', len(r4), len(rb), len(set(r4) - set(rb)), len(set(rb) - set(r4)), 'OK' if struct_ok else 'STOP'))
    if not struct_ok:
        return 9
    ix = dict((f, i) for i, f in enumerate(f4))
    res = {}
    for name, sel, cols in (('C11', ('h',), C11), ('CHI', ('h', 't'), ('C_hi',)),
                            ('NONPEV', ('h', 't', 'a'), tuple(f for f in f4 if f not in ('Pev_hi', 'vp_hi')))):
        n = d = 0
        dfields, ex = {}, []
        for k in sorted(r4):
            if k.rsplit('_', 1)[1] not in sel:
                continue
            n += 1
            bad = [f for f in cols if r4[k][ix[f]] != rb[k][ix[f]]]
            if bad:
                d += 1
                for f in bad:
                    dfields[f] = dfields.get(f, 0) + 1
                if len(ex) < 3:
                    ex.append('%s %s' % (k, ','.join(bad)))
        res[name] = d
        print('V4B %s rows %d (%s rows; %d fields each): %d differ%s%s' % (name, n, '/'.join(sel), len(cols), d,
                                                                          ('; by field ' + ', '.join('%s %d' % kv for kv in sorted(dfields.items()))) if d else '',
                                                                          ('; e.g. ' + '; '.join(ex)) if ex else ''))
    for f in ('Pev_hi', 'vp_hi'):
        ch, up, byx = 0, [], {}
        for k in sorted(r4):
            a, b = r4[k][ix[f]], rb[k][ix[f]]
            if a != b:
                ch += 1
                x = k.rsplit('_', 1)[1]
                byx[x] = byx.get(x, 0) + 1
                if Decimal(b) > Decimal(a):
                    up.append(k)
        print('V4B PEV %s changed on %d rows (%s); above v4 on %d rows%s (INFO)' % (f, ch, ', '.join('%s %d' % kv for kv in sorted(byx.items())) or 'none',
                                                                                  len(up), (': ' + ', '.join(up[:3])) if up else ''))
    hd = sorted(k for k in set(h4) | set(hb) if h4.get(k) != hb.get(k))
    print('V4B HEADER keys whose lines differ (INFO; G-PIN judges them): %s' % (', '.join(hd) or 'none'))
    if res['C11']:
        print('V4B STOP: C11 columns differ from mr/v4; C11 reruns first (main row 4526)')
        return 8
    if res['CHI']:
        print('V4B STOP: C_hi differs from mr/v4 on h or t rows; MR_JOINT reruns first (main row 4534)')
        return 10
    if res['NONPEV']:
        print('V4B STOP: fields other than Pev_hi and vp_hi differ from mr/v4 (main row 4536)')
        return 9
    print('V4B OK: the supplied MR_INSERT is mr/v4 with only Pev_hi and vp_hi changed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
