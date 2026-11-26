#!/usr/bin/env python3
"""SCRATCH (pk02, hand): smoke b of the scratch kernel SCRATCH_arbeng_ma_v1_4_b.py (the review 53de1c0d's additions). argv: kernel, new dir.
(1) MomTableU against v1_3's MomTable, with one groups+caps table; C-PAIRS reported per build;
(2) block, unit and CPU-guard partition invariance (bit-identical moments);
(3) E2 blocks (one-block bit-identical, many-block overlap, E2_check_plan refusals) and C-FASTSUM on edge lengths, zeros and near-TINY values;
(4) plants: STATE-HASH, PARAM (n, one Gam entry), FLOATSTATE, CHAIN, CODES (a level file whose codes differ but whose hand-off sha256 was
    rewritten to match), PARTITION (overlapping unit ranges): each must be refused with ValueError."""
import sys, os, importlib.util, shutil, json, time, hashlib
import numpy as np

kpath, sdir = sys.argv[1], sys.argv[2]
if os.path.exists(sdir):
    raise SystemExit('scratch dir exists')
os.makedirs(sdir)
spec = importlib.util.spec_from_file_location('ma14', kpath)
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)
from flint import arb, arb_mat, ctx
ctx.prec = 512
print(ma.env_probes())
rng = np.random.default_rng(20261108)


def spd(F):
    W = rng.integers(-3, 4, size=(F, F))
    G = W.T @ W + np.eye(F, dtype=np.int64) * F
    M = arb_mat(F, F)
    for i in range(F):
        for j in range(F):
            M[i, j] = arb(int(G[i, j])) / 7
    return M


def build_u(Gam, n, D, d, block, unit_pairs, groups=None, caps=None, cpu_budget=None):
    os.makedirs(d)
    U = ma.MomTableU(Gam, n, D, groups=groups, caps=caps, block=block)
    U.start(d)
    units = U.plan(d, unit_pairs)
    reps = []
    for u in units:
        k, b0, b1 = u[0], u[1], u[2]
        while b0 < b1:
            rep = U.run_unit(d, (k, b0, b1), cpu_budget=cpu_budget)
            reps.append(rep)
            b0 = rep['end']
    U.finish(d)
    return U, units, reps


ok_all = True
GAMS = {}
CASES = ((5, 7, 3, None, None), (6, 8, 3, None, None), (4, 10, 2, None, None), (6, 9, 3, [0, 0, 1, 1, 2, 2], {0: 4, 1: 3}))
for (F, D, n, groups, caps) in CASES:
    t0 = time.process_time()
    Gam = spd(F)
    GAMS[(F, D)] = (Gam, n, groups, caps)
    T3 = ma.MomTable(Gam, n, D, groups=groups, caps=caps)
    tag = 'u_%d_%d' % (F, D)
    da, db, dc = (os.path.join(sdir, tag + s) for s in ('_a', '_b', '_c'))
    U, units, reps = build_u(Gam, n, D, da, 97, 4000, groups, caps)
    V = U.load_view(da)
    worst, ovl, kmax3, kmaxU, codes_ok = 0.0, True, 0, 0, True
    for d in range(D + 1):
        a, b = T3.mom[d], V.mom[d]
        codes_ok &= bool(np.array_equal(T3.codes[d], V.codes[d]))
        ovl &= bool(np.all(np.abs(a.mid - b.mid) <= a.radius() + b.radius()))
        nz = a.mid != 0
        if np.any(nz):
            worst = max(worst, float(np.max(np.abs(a.mid[nz] - b.mid[nz]) / np.abs(a.mid[nz]))))
        kmax3, kmaxU = max(kmax3, int(a.k.max())), max(kmaxU, int(b.k.max()))
    pairs_ok = all(r['cand'] == r['pairs'] for r in reps)
    ratio = max(r['max_terms_ratio'] for r in reps)
    U2, units2, reps2 = build_u(Gam, n, D, db, 31, 10 ** 9, groups, caps)
    U3, units3, reps3 = build_u(Gam, n, D, dc, 13, 10 ** 9, groups, caps, cpu_budget=1e-9)
    V2, V3 = U2.load_view(db), U3.load_view(dc)
    same = all(np.array_equal(getattr(V.mom[d], f), getattr(W.mom[d], f)) for W in (V2, V3) for d in range(D + 1) for f in ('mid', 'sa', 'sr', 'k'))
    ok = codes_ok and ovl and worst <= 1e-12 and same and pairs_ok and ratio <= 1.0
    ok_all &= ok
    print('(1)-(2) F=%d D=%d n=%d%s: units %d / %d / %d (CPU-guard stops, block 13); codes equal %s, overlap %s, worst rel mid diff %.2e, '
          'counts max v1_3 %d MomTableU %d; C-PAIRS cand = plan %s, max terms/(2^|supp|-1) %.3f; bit-identical across partitions %s -> %s '
          '(%.1f s)' % (F, D, n, ' groups+caps' if caps else '', len(reps), len(reps2), len(reps3), codes_ok, ovl, worst, kmax3, kmaxU,
                        pairs_ok, ratio, same, 'PASS' if ok else 'FAIL', time.process_time() - t0))
    Pd = {}
    while len(Pd) < 30:
        e = tuple(int(x) for x in rng.integers(0, 3, size=F))
        if sum(e) <= D // 2 and (not caps or all(sum(e[f] for f in range(F) if groups[f] == g) <= c // 2 for g, c in caps.items())):
            Pd[e] = float(rng.normal())
    P = ma.SPoly.from_dict(Pd)
    ref = T3.E2(P, P, fallback=False)
    refV = V.E2(P, P, fallback=False)
    plan1 = ma.E2_plan(V, P, P, 10 ** 12)
    one = ma.E2_combine([ma.E2_block(V, P, P, plan1, b) for b in range(len(plan1['blocks']))], plan1)
    planm = ma.E2_plan(V, P, P, 3 * len(P.ex))
    many = ma.E2_combine([ma.E2_block(V, P, P, planm, b) for b in range(len(planm['blocks']))], planm)
    same1 = (one.mid() == refV.mid()) and (one.rad() == refV.rad())
    ovl3 = bool(abs(many.mid() - ref.mid()) <= many.rad() + ref.rad())
    bad = dict(planm)
    bad['blocks'] = planm['blocks'][:-1]
    try:
        ma.E2_block(V, P, P, bad, 0)
        r1 = False
    except ValueError:
        r1 = True
    try:
        ma.E2_combine([ma.E2_block(V, P, P, planm, 0)], planm)
        r2 = len(planm['blocks']) == 1
    except ValueError:
        r2 = True
    ok3 = same1 and ovl3 and r1 and r2
    ok_all &= ok3
    print('(3) E2 F=%d D=%d: one-block bit-identical %s; %d-block overlaps v1_3 %s; plan without its last block refused %s; combine with '
          'missing parts refused %s -> %s' % (F, D, same1, len(planm['blocks']), ovl3, r1, r2, 'PASS' if ok3 else 'FAIL'))
okf = True
lens = [1, 2, 3] + [2 ** m + s for m in range(2, 13) for s in (-1, 0, 1)]
for L in lens:
    m = rng.normal(size=L)
    m[rng.random(L) < 0.2] = 0.0
    a = np.abs(m) * (1 + rng.random(L) * 1e-3)
    r = a * (1 + rng.random(L) * 1e-3)
    tiny = rng.random(L) < 0.1
    a[tiny], m[tiny], r[tiny] = 0.0, 0.0, ma.TWO_TINY
    near = rng.random(L) < 0.1
    m[near] = ma.TINY * (1 + rng.random(int(near.sum())))
    a[near], r[near] = np.abs(m[near]), np.abs(m[near]) * 2
    k = rng.integers(0, 9, size=L)
    s1, s2 = ma.scalar_sum(m, a, r, k), ma.scalar_sum_fast(m, a, r, k)
    okf &= all(np.array_equal(getattr(s1, f), getattr(s2, f)) for f in ('mid', 'sa', 'sr', 'k'))
ok_all &= okf
print('(3) C-FASTSUM: scalar_sum_fast == scalar_sum bit for bit on %d lengths (1, 2, 3, 2^m - 1, 2^m, 2^m + 1 for m = 2..12) with zeros, '
      'error-only and near-TINY terms -> %s' % (len(lens), 'PASS' if okf else 'FAIL'))
F, D = 6, 8
Gam, n, groups, caps = GAMS[(F, D)]
base = os.path.join(sdir, 'u_%d_%d_a' % (F, D))


def refused(fn):
    try:
        fn()
        return False
    except ValueError:
        return True


def copy_state(name, src=base):
    d = os.path.join(sdir, name)
    shutil.copytree(src, d)
    for f in os.listdir(d):
        os.chmod(os.path.join(d, f), 0o644)
    return d


def rewrite_npz(path, z):
    with open(path, 'wb') as fh:
        np.savez(fh, **z)


d1 = copy_state('plant_hash')
z = dict(np.load(os.path.join(d1, 'mom_k05.npz'), allow_pickle=False))
z['mid'] = z['mid'].copy()
z['mid'][3] = np.nextafter(z['mid'][3], np.inf)
rewrite_npz(os.path.join(d1, 'mom_k05.npz'), z)
p1 = refused(lambda: ma.MomTableU.load(d1, Gam, n, D, block=97))
p2 = refused(lambda: ma.MomTableU.load(base, Gam, n + 1, D, block=97))
Gam_b = arb_mat(Gam)
Gam_b[0, 0] = Gam[0, 0] + arb(2) ** -60
p3 = refused(lambda: ma.MomTableU.load(base, Gam_b, n, D, block=97))
d4 = copy_state('plant_float')
rewrite_npz(os.path.join(d4, 'level_k03.npz'), {'codes': np.arange(10, dtype=np.int64), 'moments': np.ones(10)})
U4 = ma.MomTableU(Gam, n, D, block=97)
p4 = refused(lambda: U4._load_level(d4, 3))
d5 = copy_state('plant_chain')
shutil.copyfile(os.path.join(sdir, 'u_5_7_a', 'handoff_level_k03.json'), os.path.join(d5, 'handoff_level_k03.json'))
p5 = refused(lambda: U4._load_level(d5, 3))
d6 = copy_state('plant_codes')
z = dict(np.load(os.path.join(d6, 'level_k03.npz'), allow_pickle=False))
z['codes'] = z['codes'].copy()
z['codes'][0] += 1
rewrite_npz(os.path.join(d6, 'level_k03.npz'), z)
h = json.load(open(os.path.join(d6, 'handoff_level_k03.json')))
h['files']['level_k03.npz'] = {'size': os.path.getsize(os.path.join(d6, 'level_k03.npz')),
                               'sha256': hashlib.sha256(open(os.path.join(d6, 'level_k03.npz'), 'rb').read()).hexdigest()}
with open(os.path.join(d6, 'handoff_level_k03.json'), 'w') as fh:
    json.dump(h, fh)
p6 = refused(lambda: U4._load_level(d6, 3))
d7 = copy_state('plant_partition', os.path.join(sdir, 'u_6_8_b'))
U7 = ma.MomTableU(Gam, n, D, block=31)
hs = sorted(f for f in os.listdir(d7) if f.startswith('handoff_unit_k08_'))
hh = json.load(open(os.path.join(d7, hs[-1])))
hh['blocks'] = [hh['blocks'][0] - 1, hh['blocks'][1]] if hh['blocks'][0] > 0 else hh['blocks']
with open(os.path.join(d7, 'handoff_unit_k08_overlap.json'), 'w') as fh:
    json.dump(hh, fh)
p7 = refused(lambda: U7._assemble(d7, 8)) if U7.nblocks(8) > 1 else True
okp = p1 and p2 and p3 and p4 and p5 and p6 and p7
ok_all &= okp
names = ('STATE-HASH', 'PARAM (n)', 'PARAM (Gam entry)', 'FLOATSTATE', 'CHAIN', 'CODES (sha rewritten)', 'PARTITION (overlap)')
print('(4) plants: %s -> %s' % (', '.join('PLANT-%s %s' % (nm, 'FIRES' if p else 'DOES NOT FIRE') for nm, p in zip(names, (p1, p2, p3, p4, p5, p6, p7))),
                                'PASS' if okp else 'FAIL'))
print('SMOKE %s' % ('PASS' if ok_all else 'FAIL'))
