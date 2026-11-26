#!/usr/bin/env python3
"""kt_ma_val_v1_6_1.py -- pk02 (code/pk02/). The delta validation of arbeng_ma_v1_4_1 over arbeng_ma_v1_4 (2c0a7338), whose validation
of record is kt_ma_val_v1_6 (e182d503; run side manifest MANIFEST_KT_MA_VAL_v1_6_RUN.sha256 6e951721, every piece VALID). v1_4_1 changes
E2_combine (a fallback flag) and the default BLOCK (50000 -> 5000), and nothing else; this script shows exactly that, in one piece:
  C-DIFF141  the line-level difference of the two kernel files is confined to the docstring header, VERSION, BLOCK and E2_combine (every
             other line identical);
  C-SAMETABLE  MomTableU tables (12, 8) and (8, 10), built with block 97 under v1_4 and under v1_4_1, have bit-identical moments;
  C-BLOCKDEF  v1_4_1's default block is 5000, and the (12, 8) table built with the default equals the block-97 build bit for bit;
  C-E2FB     on a (6, 10) table: E2_combine with the default fallback=True equals v1_4's E2_combine on the same parts (the same ball), and
             fallback=False returns the same ball; on the case of kt_ma_val_v1_5's C-FALLBACK (an E2 whose relative M-a error is 0.5),
             fallback=True raises MAFallback and fallback=False returns a ball that contains the exact value at both ends of the 0 +- 0.25
             coefficient (PLANT-E2FB: the same call with fallback=True must raise).
Every hash is pinned in PINS (filled at freeze from the files). Run (own folder, NEW output path): D=/mnt/g2/release/root/code/
pk02; o=$D/out/out_kt_ma_val_v1_6_1_d.out; [ ! -e "$o" ] && OMP_NUM_THREADS=1 timeout 580 nice -n 10 /usr/bin/time -v prlimit
--as=8589934592 -- python3 -I -B $D/kt_ma_val_v1_6_1.py d 540 > "$o" 2> "${o%.out}.err"

"""
import sys, os, math, hashlib, importlib.util, time, itertools, resource, traceback, shutil, difflib
from fractions import Fraction

OWN = '/mnt/g2/release/root/code/pk02'
PINS = {'arbeng_ma_v1_4.py': '9870e7f8d5dc33f0edca029f9945de4774a1eb572114aa385dd7b75d7506e017', 'arbeng_ma_v1_4_1.py': '1f58ad80ceb1c0992f08f894c0f6af26ef18d397627020a5a5fe7130818375d9'}
if os.path.dirname(os.path.abspath(__file__)) != OWN:
    print('kt_ma_val_v1_6_1 must run from its own folder')
    sys.exit(2)
PIECE = sys.argv[1] if len(sys.argv) > 1 else ''
LIM = sys.argv[2] if len(sys.argv) > 2 else '540'
if PIECE != 'd' or not LIM.isdigit() or not (5 <= int(LIM) <= 540):
    print('usage: kt_ma_val_v1_6_1.py d LIM')
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (int(LIM), int(LIM) + 5))


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def out(line):
    print(line, flush=True)


out('kt_ma_val_v1_6_1 sha256 %s PIECE=%s LIM=%s' % (sha(os.path.abspath(__file__)), PIECE, LIM))
for nm, want in PINS.items():
    if sha(os.path.join(OWN, nm)) != want:
        out('SHA MISMATCH %s' % nm)
        out('VERDICT INVALID (C-HASH)')
        sys.exit(2)
out('C-HASH PASS (arbeng_ma_v1_4, arbeng_ma_v1_4_1)')


def load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


m14 = load('arbeng_ma_v1_4', os.path.join(OWN, 'arbeng_ma_v1_4.py'))
m141 = load('arbeng_ma_v1_4_1', os.path.join(OWN, 'arbeng_ma_v1_4_1.py'))
import numpy as np
from flint import arb, arb_mat, ctx
ctx.prec = 512
out(m141.env_probes())
FAILS, FIRES = [], []
SD = os.path.join(OWN, 'out', 'val161_state')


def gate(name, ok, line):
    out('%s: %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s: %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        FIRES.append(name)


def spd_gam(F, seed):
    rng = np.random.default_rng(seed)
    Wn = rng.integers(-3, 4, size=(F, F))
    G = Wn.T @ Wn + np.eye(F, dtype=np.int64) * F
    M = arb_mat(F, F)
    for i in range(F):
        for j in range(F):
            M[i, j] = arb(int(G[i, j])) / 7
    return M


def build(ma, Gam, n, D, d, block=None):
    os.makedirs(d)
    U = ma.MomTableU(Gam, n, D) if block is None else ma.MomTableU(Gam, n, D, block=block)
    U.start(d)
    for u in U.plan(d, 10 ** 12):
        U.run_unit(d, u)
    U.finish(d)
    return U, U.load_view(d)


def same_mom(Va, Vb, D):
    return all(np.array_equal(getattr(Va.mom[d], f), getattr(Vb.mom[d], f)) for d in range(D + 1) for f in ('mid', 'sa', 'sr', 'k'))


def piece_d():
    a = open(os.path.join(OWN, 'arbeng_ma_v1_4.py')).read().splitlines()
    b = open(os.path.join(OWN, 'arbeng_ma_v1_4_1.py')).read().splitlines()
    ops = [op for op in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes() if op[0] != 'equal']
    allowed = []
    for tag, i1, i2, j1, j2 in ops:
        old = a[i1:i2]
        ok = (i1 == 1 and i2 == 2) or all(ln.startswith(('VERSION = ', 'BLOCK = ', 'def E2_combine(', '    the ball and the MAFallback test',
                                                          '    if float(one.mid[0]) != 0 and err > FALLBACK_REL')) for ln in old)
        allowed.append(ok)
    gate('C-DIFF141', ops and all(allowed) and len(ops) == 6, '%d changed regions (old lines %s), each the header, VERSION, BLOCK or '
         'E2_combine' % (len(ops), ', '.join('%d-%d' % (op[1] + 1, op[2]) for op in ops)))
    os.makedirs(SD)
    n = 3
    for (F, D, seed) in ((12, 8, 611), (8, 10, 612)):
        Gam = spd_gam(F, seed)
        _, Va = build(m14, Gam, n, D, os.path.join(SD, 'v14_%d_%d' % (F, D)), 97)
        _, Vb = build(m141, Gam, n, D, os.path.join(SD, 'v141_%d_%d' % (F, D)), 97)
        gate('C-SAMETABLE (%d, %d)' % (F, D), same_mom(Va, Vb, D), 'block 97 under v1_4 and v1_4_1: moments bit-identical')
        if F == 12:
            Ud, Vd = build(m141, Gam, n, D, os.path.join(SD, 'v141_%d_%d_default' % (F, D)))
            gate('C-BLOCKDEF', m141.BLOCK == 5000 and Ud.block == 5000 and same_mom(Vb, Vd, D),
                 'v1_4_1 default block %d; the default build equals the block-97 build bit for bit %s' % (Ud.block, same_mom(Vb, Vd, D)))
    F, D = 6, 10
    Gam = spd_gam(F, 613)
    U, V = build(m141, Gam, n, D, os.path.join(SD, 'e2_%d_%d' % (F, D)), 97)
    rng = np.random.default_rng(614)
    Pd = {}
    while len(Pd) < 60:
        e = tuple(int(x) for x in rng.integers(0, 3, size=F))
        if sum(e) <= D // 2:
            Pd[e] = float(rng.normal())
    P = m141.SPoly.from_dict(Pd)
    plan = m141.E2_plan(V, P, P, 5 * len(P.ex))
    parts = [m141.E2_block(V, P, P, plan, i) for i in range(len(plan['blocks']))]
    b1 = m141.E2_combine(parts, plan)
    b0 = m14.E2_combine(parts, plan)
    bf = m141.E2_combine(parts, plan, fallback=False)
    gate('C-E2FB (normal)', (b1.mid() == b0.mid()) and (b1.rad() == b0.rad()) and (bf.mid() == b1.mid()) and (bf.rad() == b1.rad()),
         '%d blocks: fallback=True equals v1_4\'s E2_combine and fallback=False returns the same ball' % len(plan['blocks']))
    # kt_ma_val_v1_5's C-FALLBACK case: (0 +- 0.25) Y0 + 1 against Y0, on a small table (relative M-a error 0.5)
    Gs = spd_gam(2, 615)
    T = m141.MomTable(Gs, n, 4)
    zb = arb(0, 0.25)
    Pz = m141.SPoly.from_dict({(1, 0): zb, (0, 0): arb(1)})
    Y0 = m141.SPoly.from_dict({(1, 0): arb(1)})
    pl = m141.E2_plan(T, Pz, Y0, 10 ** 9)
    pz = [m141.E2_block(T, Pz, Y0, pl, i) for i in range(len(pl['blocks']))]
    try:
        m141.E2_combine(pz, pl)
        raised = False
    except m141.MAFallback:
        raised = True
    plant('PLANT-E2FB', raised, 'the C-FALLBACK case with fallback=True raises MAFallback')
    ballz = m141.E2_combine(pz, pl, fallback=False)
    m2 = T.E(m141.SPoly.from_dict({(2, 0): arb(1)}), fallback=False)
    m1 = T.E(m141.SPoly.from_dict({(1, 0): arb(1)}), fallback=False)
    ends = [arb(c) * m2 + m1 for c in ('0.25', '-0.25')]
    cont = all(bool(ballz.contains(x)) for x in ends)
    gate('C-E2FB (fallback=False)', cont, 'the same case with fallback=False returns %s, which contains E2 at both ends of the 0 +- 0.25 '
         'coefficient (%s, %s)' % (ballz.str(5), ends[0].str(5), ends[1].str(5)))


def main():
    T0 = time.process_time()
    try:
        ok, lines = m141.tree_check()
        gate('C-TREE', ok, '; '.join(lines))
        piece_d()
        out(m141.env_probes())
    except Exception as e:
        traceback.print_exc()
        out('ERROR at cpu %.1f s: %r' % (time.process_time() - T0, e))
        out('VERDICT INVALID (ERROR)')
        return 1
    why = FAILS + ['%s did not fire' % x for x in FIRES]
    out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (PIECE, time.process_time() - T0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
