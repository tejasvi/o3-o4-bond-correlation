# Exact check that the CERTIFIED intervals of cover3 ledgers cover [A, B] (rational endpoints of the float data).
# usage: checkcover.py A B ledger1 [ledger2 ...]      (A, B rationals such as 1/100 and 3)
import sys
from fractions import Fraction
A, B = Fraction(sys.argv[1]), Fraction(sys.argv[2])
iv = []
for fn in sys.argv[3:]:
    for line in open(fn):
        f = line.split()
        if len(f) >= 5 and f[4] == 'CERT':
            J0, h = Fraction(float(f[0])), Fraction(float(f[1]))
            iv.append((J0 - h, J0 + h, int(f[2]), int(f[3])))
iv.sort()
reach = A
gaps = []
used = 0
for lo, hi, L, I in iv:
    if lo > reach:
        gaps.append((reach, lo))
    if hi > reach:
        reach = hi; used += 1
    if reach >= B:
        break
covered = reach >= B and not gaps and (iv and iv[0][0] <= A)
print('%d certified intervals read, %d used; covered [%s, %s]: %s; reach %.12g; first lower end %.12g; gaps %s'
      % (len(iv), used, A, B, covered, float(reach), float(iv[0][0]) if iv else float('nan'),
         ', '.join('[%.12g, %.12g]' % (float(a), float(b)) for a, b in gaps[:5]) or 'none'))
