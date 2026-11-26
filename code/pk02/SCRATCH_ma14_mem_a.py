#!/usr/bin/env python3
"""SCRATCH (pk02, hand): where the D16 peak RSS comes from. argv: kernel, stage, block. stage 'init': MomTableU(D16 F12) only; stage
'block': init, then load D_j and levels 4..15 from the validation's state (read only) and compute one level-16 block (U._block) at the given
block size, nothing written. Prints ru_maxrss after each step."""
import sys, os, importlib.util, resource, time
import numpy as np

kpath, stage, block = sys.argv[1], sys.argv[2], int(sys.argv[3])
spec = importlib.util.spec_from_file_location('ma14', kpath)
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)
from flint import arb, arb_mat, ctx
ctx.prec = 512


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024


rng = np.random.default_rng(701)
F = 12
Wn = rng.integers(-3, 4, size=(F, F))
G = Wn.T @ Wn + np.eye(F, dtype=np.int64) * F
Gam = arb_mat(F, F)
for i in range(F):
    for j in range(F):
        Gam[i, j] = arb(int(G[i, j])) / 7
print('after imports: %d MiB' % rss(), flush=True)
t0 = time.process_time()
U = ma.MomTableU(Gam, 3, 16, block=50000)
print('after init (codes, hashes): %d MiB, %.1f s' % (rss(), time.process_time() - t0), flush=True)
if stage == 'block':
    sd = '/mnt/g2/release/root/code/pk02/out/val16_state'
    Dj = U._load_Dj(sd)
    M = [None] * 17
    for kk in range(4, 16):
        M[kk] = U._load_level(sd, kk)
    print('after loading D_j and levels 4..15: %d MiB' % rss(), flush=True)
    U.block = block
    t1 = time.process_time()
    r, nt, cand, ratio = U._block(16, 3, Dj, M)
    print('after one level-16 block of %d destinations (%d terms, %.1f s): %d MiB' % (block, nt, time.process_time() - t1, rss()), flush=True)
