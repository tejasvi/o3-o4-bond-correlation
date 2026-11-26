#!/usr/bin/env python3
# union_check_v1.py: exact union of the cover intervals from hubcert LEDGER lines (the d1: exact arithmetic on the
# b0hex/hhex fields, never the decimal fields).  Usage: union_check_v1.py <engine_sha256> <a> <b> <out files...>
# For each N in {3, 4}: the intervals [b0 - h, b0 + h] (exact rationals), sorted by left end, must have no gap, start at
# or below a and reach b.  Each file must carry the engine's full sha256 in its header and end with VERDICT VALID.
import sys
import hashlib
from fractions import Fraction


def main():
    sha, a, b = sys.argv[1], Fraction(sys.argv[2]), Fraction(sys.argv[3])
    files = sys.argv[4:]
    with open(__file__, 'rb') as fh:
        me = hashlib.sha256(fh.read()).hexdigest()
    print('union_check_v1 sha256 %s engine %s a %s b %s files %d' % (me, sha, a, b, len(files)))
    ivs = {3: [], 4: []}
    ok = True
    for f in files:
        with open(f) as fh:
            txt = fh.read().splitlines()
        hdr = txt[0].split() if txt else []
        engine_ok = len(hdr) > 2 and hdr[1] == 'sha256' and hdr[2] == sha
        v_ok = [l for l in txt if l.startswith('VERDICT')] == ['VERDICT VALID']
        n_led = 0
        for l in txt:
            if l.startswith('LEDGER '):
                d = dict(kv.split('=', 1) for kv in l.split()[1:] if '=' in kv)
                N = int(d['N'])
                b0 = Fraction(float.fromhex(d['b0hex']))
                h = Fraction(float.fromhex(d['hhex']))
                ivs[N].append((b0 - h, b0 + h))
                n_led += 1
        print('FILE %s engine_ok %s verdict_ok %s ledger_lines %d' % (f, engine_ok, v_ok, n_led))
        ok = ok and engine_ok and v_ok
    for N in (3, 4):
        L = sorted(ivs[N])
        if not L:
            print('UNION N=%d EMPTY' % N)
            ok = False
            continue
        gaps, reach = 0, L[0][1]
        for lo, hi in L[1:]:
            if lo > reach:
                gaps += 1
                print('GAP N=%d from %r to %r' % (N, float(reach), float(lo)))
            reach = max(reach, hi)
        cov = (L[0][0] <= a) and (reach >= b) and gaps == 0
        print('UNION N=%d intervals %d first_lo %r (<= a: %s) reach %r (>= b: %s) gaps %d -> %s' % (
            N, len(L), float(L[0][0]), L[0][0] <= a, float(reach), reach >= b, gaps, 'COVERS' if cov else 'FAILS'))
        ok = ok and cov
    print('VERDICT %s' % ('VALID' if ok else 'NOT VALID'))


if __name__ == '__main__':
    main()
