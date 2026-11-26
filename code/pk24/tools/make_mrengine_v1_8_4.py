#!/usr/bin/env python3
"""make_mrengine_v1_8_4.py (pk24): makes pk24/mr_engine/kt_mr_assembly_v1_8_4.py from pk24/mr_engine/src/kt_mr_assembly_v1_8_4.py.in, then
pk24/mr_engine/mr_merge_v1_8_4.py from pk24/mr_engine/src/mr_merge_v1_8_4.py.in (in this order: the merge pins the engine), as
make_mrengine_v1_7_1.py does for v1_7_1. Each {{SHA256:relpath}} is filled with the file's sha256 (paths relative to code/). The products must
hold no placeholder. Mode 'x'. Prints the products' sha256 and each pin."""
import hashlib, os, re, sys

W18 = '/mnt/g2/release/root/code/'
JOBS = [(W18 + 'pk24/mr_engine/src/kt_mr_assembly_v1_8_4.py.in', W18 + 'pk24/mr_engine/kt_mr_assembly_v1_8_4.py'),
        (W18 + 'pk24/mr_engine/src/mr_merge_v1_8_4.py.in', W18 + 'pk24/mr_engine/mr_merge_v1_8_4.py')]


def h(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


for SRC, DST in JOBS:
    src = open(SRC).read()
    pins = {}

    def fill(m):
        p = m.group(1)
        assert os.path.isfile(W18 + p), p
        pins[p] = h(W18 + p)
        return pins[p]

    out = re.sub(r'\{\{SHA256:([^}]+)\}\}', fill, src)
    assert '{{' not in out, 'unfilled placeholder'
    with open(DST, 'x') as fh:
        fh.write(out)
    for p in sorted(pins):
        print('PIN %s %s' % (pins[p], p))
    print('SRC %s %s' % (h(SRC), SRC))
    print('DST %s %s' % (h(DST), DST))
sys.exit(0)
