#!/usr/bin/env python3
"""make_g37_v1.py (pk23, CODEDIR team): writes pk23/o5/kt_lbu_g37_v1.py, the CANDIDATE certificate copy of pk21's whole-graph
engine pk21/p2/kt_lbu_g35_pk21_v1.py (pinned by full sha256) for O5 on a large-memory box (P_3 x P_6 and P_3 x P_7, N = 4), by exact
string replacements, each required to match exactly once:
  R1 the first docstring line gains a pk23 banner in front of pk21's (the copy, its base sha8, the four changes; no run counts before
     the review of this copy and the approval);
  R2 grid COLS up to 7 (was 5), in the argument check and its comment;
  R3 TAU_GRID gains (3, 6) and (3, 7), the spanning-tree counts computed here by the matrix-tree theorem in exact rational arithmetic (the
     same computation must reproduce the five existing entries);
  R4 grid mode's LIM range (RLIMIT_CPU soft limit, s) becomes 30..43200 (was 30..3600): one P_3 x P_7 orbit needs hours of CPU.
Nothing else changes; kt_lbu_g36_pk23_v1.py (the memory-probe copy, R1-R3 with a probe banner) stays as it is. The output is written
with open(..., 'x') (never overwritten); a unified diff goes to stdout. Usage: make_g37_v1.py"""
import difflib, hashlib, os, sys
from fractions import Fraction

SRC = '/mnt/g2/release/root/code/pk21/p2/kt_lbu_g35_pk21_v1.py'
SRC_SHA = '6c3afd8f0a5ceff396ac8115d5a6bbde69d85b520b327a37578c55a8bfdec13f'
DST = '/mnt/g2/release/root/code/pk23/o5/kt_lbu_g37_v1.py'


def tau_grid(R, C):
    """spanning trees of P_R x P_C: det of the Laplacian with vertex 0's row and column removed, exact."""
    V = R * C
    L = [[Fraction(0)] * V for _ in range(V)]
    for r in range(R):
        for c in range(C):
            u = r * C + c
            for (rr, cc) in ((r + 1, c), (r, c + 1)):
                if rr < R and cc < C:
                    w = rr * C + cc
                    L[u][u] += 1
                    L[w][w] += 1
                    L[u][w] -= 1
                    L[w][u] -= 1
    M = [row[1:] for row in L[1:]]
    n, det = len(M), Fraction(1)
    for j in range(n):
        p = next(i for i in range(j, n) if M[i][j] != 0)
        if p != j:
            M[j], M[p] = M[p], M[j]
            det = -det
        det *= M[j][j]
        for i in range(j + 1, n):
            if M[i][j] != 0:
                f = M[i][j] / M[j][j]
                M[i] = [a - f * b for a, b in zip(M[i], M[j])]
    assert det.denominator == 1
    return int(det)


def main():
    with open(SRC, 'rb') as fh:
        b = fh.read()
    h = hashlib.sha256(b).hexdigest()
    if h != SRC_SHA:
        print('SOURCE sha256 %s differs from the pin %s' % (h, SRC_SHA))
        sys.exit(1)
    old = {(2, 3): 15, (2, 4): 56, (3, 3): 192, (3, 4): 2415, (3, 5): 30305}
    got = {k: tau_grid(*k) for k in old}
    print('TAU check of the existing entries: %s -> %s' % (got, 'PASS' if got == old else 'FAIL'))
    if got != old:
        sys.exit(1)
    t6, t7 = tau_grid(3, 6), tau_grid(3, 7)
    print('TAU (3, 6) = %d, (3, 7) = %d' % (t6, t7))
    s = b.decode('utf-8')
    reps = [
        ('"""kt_lbu_g35_pk21_v1.py -- pk21 (code/pk21/p2/), Phase 2 item 2 pilot (P_3 x P_5). A copy of',
         '"""kt_lbu_g37_v1.py -- pk23 (code/pk23/o5/): the CANDIDATE certificate copy for O5 (P_3 x P_6, P_3 x P_7, N = 4) on a\n'
         'large-memory box; no run of it counts before the review of this copy and the approval. A copy of pk21/p2/kt_lbu_g35_pk21_v1.py\n'
         '(sha8 9231dcbb) with four PK23 CHANGES only, made by pk23/o5/make_g37_v1.py: this banner, grid COLS up to 7 (was 5),\n'
         'TAU_GRID[(3, 6)] = %d and TAU_GRID[(3, 7)] = %d (matrix-tree counts computed by the maker, which reproduces the five existing\n'
         'entries), and grid LIM up to 43200 s (was 3600). pk21 docstring:\n'
         'kt_lbu_g35_pk21_v1.py -- pk21 (code/pk21/p2/), Phase 2 item 2 pilot (P_3 x P_5). A copy of' % (t6, t7)),
        ('3 <= G_COLS <= 5 and G_N in (3, 4) and 50 <= G_J1 <= 2000  # PK21 COLS <= 5',
         '3 <= G_COLS <= 7 and G_N in (3, 4) and 50 <= G_J1 <= 2000  # PK23 COLS <= 7 (PK21 5)'),
        ('TAU_GRID = {(2, 3): 15, (2, 4): 56, (3, 3): 192, (3, 4): 2415, (3, 5): 30305}  # PK21 (3, 5)',
         'TAU_GRID = {(2, 3): 15, (2, 4): 56, (3, 3): 192, (3, 4): 2415, (3, 5): 30305, (3, 6): %d, (3, 7): %d}  # PK21 (3, 5); PK23 (3, 6), (3, 7)' % (t6, t7)),
        ("MODES = {'v1': (20, 300), 'v2': (60, 900), 'cert': (60, 3000), 'grid': (30, 3600)}",
         "MODES = {'v1': (20, 300), 'v2': (60, 900), 'cert': (60, 3000), 'grid': (30, 43200)}   # PK23 grid LIM up to 43200 (was 3600)"),
    ]
    for i, (a, c) in enumerate(reps, start=1):
        n = s.count(a)
        print('R%d: %d match(es)' % (i, n))
        if n != 1:
            sys.exit(1)
        s = s.replace(a, c, 1)
    if not os.path.abspath(DST).startswith('/mnt/g2/release/root/code/pk23/'):
        sys.exit(1)
    with open(DST, 'x') as fh:
        fh.write(s)
    with open(DST, 'rb') as fh:
        print('WROTE %s sha256 %s' % (DST, hashlib.sha256(fh.read()).hexdigest()))
    for ln in difflib.unified_diff(b.decode('utf-8').splitlines(), s.splitlines(), 'kt_lbu_g35_pk21_v1.py', 'kt_lbu_g37_v1.py', lineterm='', n=0):
        print(ln[:240])
    print('VERDICT DONE')


if __name__ == '__main__':
    main()
