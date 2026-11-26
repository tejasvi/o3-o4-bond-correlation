#!/usr/bin/env python3
"""SCRATCH (pk02, hand): MomTableU performance probe (F = 12, D given) on a random positive-definite Gam: per-unit CPU, terms, ns per
term, and the peak RSS from the caller's /usr/bin/time. argv: kernel path, scratch dir (new), D, block, unit_pairs."""
import sys, os, importlib.util, time, resource
import numpy as np

kpath, sdir, D, block, unit_pairs = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(float(sys.argv[5]))
if os.path.exists(sdir):
    raise SystemExit('scratch dir exists')
os.makedirs(sdir)
spec = importlib.util.spec_from_file_location('ma14', kpath)
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)
from flint import arb, arb_mat, ctx
ctx.prec = 512
rng = np.random.default_rng(20261109)
F = 12
W = rng.integers(-3, 4, size=(F, F))
G = W.T @ W + np.eye(F, dtype=np.int64) * F
Gam = arb_mat(F, F)
for i in range(F):
    for j in range(F):
        Gam[i, j] = arb(int(G[i, j])) / 7
t0 = time.process_time()
U = ma.MomTableU(Gam, 3, D, block=block)
U.start(sdir)
t1 = time.process_time()
units = U.plan(sdir, unit_pairs)
t2 = time.process_time()
print('init+minors %.1f s; plan %.1f s: %d units, pairs %d' % (t1 - t0, t2 - t1, len(units), sum(u[3] for u in units)), flush=True)
tot_terms, tot_cpu = 0, 0.0
for u in units:
    rep = U.run_unit(sdir, u)
    tot_terms += rep['terms']
    tot_cpu += rep['cpu']
    if u[0] >= D - 3:
        print('unit %s: terms %d, cpu %.1f s (%.0f ns/term), k_max %d, rss %.0f MiB' % (rep['unit'], rep['terms'], rep['cpu'],
              1e9 * rep['cpu'] / max(rep['terms'], 1), rep['k_max'], resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024), flush=True)
t3 = time.process_time()
U.finish(sdir)
t4 = time.process_time()
print('units: terms %d, cpu %.1f s (%.0f ns/term overall); finish %.1f s; total %.1f s; peak rss %.0f MiB' % (
    tot_terms, tot_cpu, 1e9 * tot_cpu / max(tot_terms, 1), t4 - t3, t4 - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
