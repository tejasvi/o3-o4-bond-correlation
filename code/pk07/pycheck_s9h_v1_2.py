"""pycheck_s9h_v1_2.py -- pk07 (code/pk07/). Compile-only check of kt_s9h_v1_2.py: compile() of its source, nothing executed,
nothing written (stdout only). Run through the wrapper only (the standing approval; it reads no certified input)."""
import sys

P = '/mnt/g2/release/root/code/pk07/'
ok = True
for name in ('kt_s9h_v1_2.py',):
    try:
        with open(P + name) as fh:
            compile(fh.read(), P + name, 'exec')
        print('COMPILE OK %s' % name)
    except SyntaxError as e:
        ok = False
        print('COMPILE ERROR %s: %r' % (name, e))
print('RESULT %s' % ('PASS' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
