#!/usr/bin/env python3
"""SCRATCH (pk02, hand): E2 speed on the D12 F12 probe table: v1_3's MomTable.E2 against E2_plan/E2_block/E2_combine (scalar_sum_fast),
ns per pair, and their agreement (one-block plan bit for bit). argv: kernel path, the probe's state dir, number of P terms."""
import sys, os, importlib.util, time
import numpy as np

kpath, sdir, nterms = sys.argv[1], sys.argv[2], int(sys.argv[3])
spec = importlib.util.spec_from_file_location('ma14', kpath)
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)
from flint import arb, arb_mat, ctx
ctx.prec = 512
rng = np.random.default_rng(20261109)
F, D = 12, 12
W = rng.integers(-3, 4, size=(F, F))
G = W.T @ W + np.eye(F, dtype=np.int64) * F
Gam = arb_mat(F, F)
for i in range(F):
    for j in range(F):
        Gam[i, j] = arb(int(G[i, j])) / 7
t0 = time.process_time()
V = ma.MomTableU.load(sdir, Gam, 3, D, block=50000)
t1 = time.process_time()
Pd = {}
while len(Pd) < nterms:
    e = rng.integers(0, 4, size=F)
    if e.sum() <= D // 2:
        Pd[tuple(int(x) for x in e)] = float(rng.normal())
P = ma.SPoly.from_dict(Pd)
pairs = len(P.ex) ** 2
t2 = time.process_time()
ref = V.E2(P, P, fallback=False)
t3 = time.process_time()
plan = ma.E2_plan(V, P, P, 10 ** 12)
one = ma.E2_combine([ma.E2_block(V, P, P, plan, b) for b in range(len(plan['blocks']))])
t4 = time.process_time()
plan4 = ma.E2_plan(V, P, P, pairs // 4 + 1)
four = ma.E2_combine([ma.E2_block(V, P, P, plan4, b) for b in range(len(plan4['blocks']))])
t5 = time.process_time()
same = (one.mid() == ref.mid()) and (one.rad() == ref.rad())
ovl = bool(abs(four.mid() - ref.mid()) <= four.rad() + ref.rad())
print('load %.1f s; P %d terms, %d pairs; v1_3 E2 %.2f s (%.0f ns/pair); blocked one-plan %.2f s (%.0f ns/pair), bit-identical %s; '
      '%d-block plan %.2f s, overlaps %s; E2 = %s' % (t1 - t0, len(P.ex), pairs, t3 - t2, 1e9 * (t3 - t2) / pairs, t4 - t3,
                                                       1e9 * (t4 - t3) / pairs, same, len(plan4['blocks']), t5 - t4, ovl, ref.str(5)))
