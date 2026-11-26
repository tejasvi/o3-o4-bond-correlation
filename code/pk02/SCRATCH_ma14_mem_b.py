#!/usr/bin/env python3
"""SCRATCH (pk02, hand): the peak RSS of the heaviest level-16 block at a given block size (read-only use of the validation's D16 state).
After init and loading, the high-water mark is reset (/proc/self/clear_refs = 5) and VmHWM is read after the block. argv: kernel, block."""
import sys, os, importlib.util, time
import numpy as np

kpath, block = sys.argv[1], int(sys.argv[2])
spec = importlib.util.spec_from_file_location('ma14', kpath)
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)
from flint import arb, arb_mat, ctx
ctx.prec = 512


def vm(key):
    for ln in open('/proc/self/status'):
        if ln.startswith(key + ':'):
            return int(ln.split()[1]) // 1024
    return -1


rng = np.random.default_rng(701)
F = 12
Wn = rng.integers(-3, 4, size=(F, F))
G = Wn.T @ Wn + np.eye(F, dtype=np.int64) * F
Gam = arb_mat(F, F)
for i in range(F):
    for j in range(F):
        Gam[i, j] = arb(int(G[i, j])) / 7
U = ma.MomTableU(Gam, 3, 16, block=50000)
sd = '/mnt/g2/release/root/code/pk02/out/val16_state'
Dj = U._load_Dj(sd)
M = [None] * 17
for kk in range(4, 16):
    M[kk] = U._load_level(sd, kk)
U.block = block
nb = U.nblocks(16)
pairs = [U.block_pairs(16, b, Dj) for b in range(nb)]
bmax = int(np.argmax(pairs))
print('block %d: %d blocks at level 16; candidate pairs per block: max %d (block %d), mean %.0f; VmRSS before %d MiB' % (
    block, nb, max(pairs), bmax, np.mean(pairs), vm('VmRSS')), flush=True)
with open('/proc/self/clear_refs', 'w') as fh:
    fh.write('5')
base = vm('VmHWM')
t0 = time.process_time()
r, nt, cand, ratio = U._block(16, bmax, Dj, M)
print('heaviest block: %d terms, %.1f s; VmHWM after reset %d MiB (from %d), so the block adds about %d MiB' % (
    nt, time.process_time() - t0, vm('VmHWM'), base, vm('VmHWM') - base), flush=True)
