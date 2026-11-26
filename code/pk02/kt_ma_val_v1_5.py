#!/usr/bin/env python3
"""kt_ma_val_v1_5.py -- pk02 (code/pk02/). REVISION of kt_ma_val_v1_4.py (7a513d3e), the validation of record of arbeng_ma_v1_3
(075e3586), whose first piece v3 (out/out_kt_ma_val_v1_4_v3.out a692e736) stopped with ERROR:
its new C-ZMID case 'E2 two parts' asked E2 for (0 +- 0.25) Y0 + 1 against Y0 with the default fallback, and the layer raised
MAFallback('E2: M-a error 5.00e-01 of 1.00e+00'), its designed signal for a relative M-a error above FALLBACK_REL = 1e-3 (a test-design
error: every earlier v3 gate had passed, C-CROSS, PLANT-SIGN, C-TINY, PLANT-TINY). Changes, and nothing else:
  v3  C-ZMID 'E2 two parts' calls E2 with fallback=False (the ball itself is compared); new gate C-FALLBACK: the same call with the
      default fallback must raise MAFallback. The T-a: the cases E2, E2 two parts and lp_norm (p = 4)
      also need endpoint containment, the stub's value with zb replaced by the exact +0.25 and -0.25 inside M-a's ball (an overlap alone
      passes a dropped term whose true value may be 0); under arbeng_ma_v1_1 these cases now fail too (PLANT-ZMID).
  Count check (the rule (a), unchanged from v1_4): PLANT-MA-COUNT stays an INFO line, since with every count 0 the radius still
  keeps the formula's own margin 4u (A + B + C), about 8u times the shadow, which covers a well-conditioned table's actual rounding
  (kt_ma_val_v1_2 v1: 7,677,098 Dc 10 entries, every one overlapping arb); count correctness is carried by C-TREE (a sum of 2^m + 1 terms
  must report k = m + 1, and m + 2 merged with 3 terms) and the need for the rounding allowance by PLANT-MA-ROUND.
kt_ma_val_v1_4 was the REVISION of kt_ma_val_v1_3.py (b3f860d5; its v3 c2957746 and v4 3a548aa2 VALID on
arbeng_ma_v1_2 as an early signal), for arbeng_ma_v1_3 (SPEC_MA_LAYER_v1_2_ADD3b) and after kt_ma_val_v1_2's run (v3
e66324b2 and v4 0d59313b VALID; v1 3d8200e2 INVALID only because PLANT-MA-COUNT did not fire, every gate passing). Changes, and nothing
else:
  pins and loads arbeng_ma_v1_3 in place of arbeng_ma_v1_2;
  v1  PLANT-MA-COUNT becomes an INFO line: with every count set to 0 the radius still keeps the formula's own margin 4u (A + B + C), about
      8u times the shadow, which covers a well-conditioned table's actual errors, so a count-only plant cannot fire; PLANT-MA-ROUND stays;
      C-UF also prints Smax;
  v3  C-ZMID adds an E2 case whose zero-midpoint part is a whole degree group (the D-1 count case); new C-COUNT (ma_add of a normal and an
      error-only operand counts max + 1) with PLANT-COUNT (arbeng_ma_v1_1 does not), and C-FLOOR (npoly_mul of (1e-200 +- 1e-210)^2,
      whose 1e-400 underflows, contains the arb product) with PLANT-FLOOR (the rule without its floor, TWO_TINY := 0, must fail).
kt_ma_val_v1_3 was the REVISION of kt_ma_val_v1_2.py (a193f9f1, frozen and never run), on the review's
REVIEW_MA_LAYER_v1_1 (6b5961eb): it still validates arbeng_ma_v1_2 (da68ebcb). Changes, and nothing else:
  v3  C-ZMID replaces C-ZEROMID: the coefficient 0 +- 0.25 through npoly_mul, npoly_pow (k = 2), E2, lp_norm (p = 4), condE (a P12
      coefficient) and CondTable (one such entry of W^T M, on a generic SPD C), each against the arb stub (same keys, overlapping balls);
      PLANT-ZMID: under arbeng_ma_v1_1 the gate must fail. C-CROSS adds the symmetric straddling interval [-0.25, 0.25], two quotients at
      iv.dps = 40 checked against the raw-tuple exact ends, the zero-end ball -0.25 +- 0.25, arb -> mp.iv -> arb on the balls
      and runs on the arb stub as well.
  Not changed: to_arb's (mid, rad) path rejects no negative or nan radius, and the stub departures stay (no PREC check; its
  _root_ball returns 0 below 0) are left to the next layer revision: a nan radius is caught by ball_to_in's finiteness test, and the stub
  is the arb build target, not a certified path.
kt_ma_val_v1_2 was the REVISION of kt_ma_val_v1_1.py (297298a6; v3 e92cdca9 and v4 06b4c585 VALID, v1 6d991943
INVALID on v1_1's subnormal MAFallback): it validates arbeng_ma_v1_2 (SPEC_MA_LAYER_v1_2_ADD3 12091946), v1-v4 rerun as one bundle.
Changes, and nothing else:
  v1  runs through the tiny rule (C-TINY prints the number of terms made error-only, C-UF the largest einsum allowance); V1 (a) compares
      every entry both ways, and an entry present on one side only must contain 0;
  v3  adds C-TINY (a Dc 6 CondTable on the symmetric A with structural zeros against arb CondMomA, entry by entry, one-sided entries
      containing 0) with PLANT-TINY (the same table under arbeng_ma_v1_1 must raise MAFallback); C-ZEROMID (npoly_mul of [0 +- 1e-3] by 1
      keeps a ball containing [-1e-3, 1e-3]) with PLANT-ZEROMID (arbeng_ma_v1_1 drops it); C-INT64 (the guard passes 6^24 and raises
      ValueError on 7^24, and a MomTable with F = 24, D = 6 raises before any work) with PLANT-INT64 (numpy's int64 7^24 wraps);
  v4  C-ERRORS: the 1e-320 shadow product now goes through the tiny rule (a finite ball containing 1e-320) instead of MAFallback.
kt_ma_val_v1_1 was the REVISION of kt_ma_val_v1.py (fb865eb4, frozen and never run): it validates
arbeng_ma_v1_1 (the signed mpi_to_arb) against arbeng_ma_stub_v1_1, and piece v3 adds C-CROSS, round-trip containment of every crossing
(mpi_to_arb, arb_to_mpi, ball_to_in with its inverse) on intervals with both ends negative, straddling 0, with a zero end, and with large
and tiny exponents, and PLANT-SIGN (arbeng_ma_stub_v1's sign-dropping mpi_to_arb must fail C-CROSS). Everything else is kt_ma_val_v1's.
kt_ma_val_v1 was the validation C-MA of arbeng_ma_v1 (SPEC_MA_LAYER_v1_2 d8b05870 sect. 5, with the REVIEW
38130886 conditions as SPEC_MA_LAYER_v1_2_ADD1 states them), at e1n4 and on the references' own trial states: it loads kt_cert_v1_5.py
as a module (sha256 checked; argv tA.e1n4, so kt_cert_v1_5's OLD pinned trial set; its import-time checks run, its main does not),
the layer and its arb stub (sha256 checked). References: kt_cert_v1_5's arb engine (arbeng_c2b_v2); the hand-offs of its
VALID production pieces c, tX0, tX1, tX2 and tB of e1n4, read through kt_cert_v1_5's own reader (record VERDICT VALID, sha256, body
checksum, header); exact rational moments; kt_c_v2_3's printed values (C-REPRO).
Every piece prints env_probes (M-e, ctx.prec 512, ctx.cap, the static check) at start and end, and runs C-TREE (tree_check).
Pieces (argv[1]):
  v1  K2: CondTable at Dc = deg2 (10) on e1n4's c stage against arb CondMomA: every entry overlaps (V1 (a)); PLANT-MA-ROUND (the rounding
      term dropped) and PLANT-MA-COUNT (every count 0) must miss; condE (V1 (b): every ED coefficient overlaps); nD (V1 (c): it overlaps
      the arb nD and the c hand-off's nD, relative width <= 1e-5, the C-RAD-MA gate); C-REPRO nD against kt_c_v2_3's printed value;
      QC C-BUDGET nD.
  v2  K1 + K3: the Chernoff tables X0, X1, X2 (degree 16, cap 4) on M-a against the tX0-tX2 hand-offs (overlap, relative width <= 1e-5);
      C-SING per table; C-REPRO tailX from X0-X2 against kt_c_v2_3's printed value; QC C-BUDGET per table.
  v3  C-AK: K1 on an exact rational covariance (4 forms on 3 coordinates, so with exact zeros) at n = 2 and 3 to degree 8, and n = 2 to
      degree 12: every moment's enclosure contains the exact rational moment (exact recursion in Fractions). PLANT-MA-AK: every nonzero
      exact moment perturbed by 10 times the largest printed relative width must fall outside its enclosure.
  v4  K1 + K3: B0 on M-a against the tB hand-off; C-SING; PLANT-MA-SING (forms W = W_int with X0's column zeroed, consistent with each
      other but not with Gam: the exact-zero rule's det check must stop); PLANT-MA-W (W_int unequal to W, or W missing: ValueError);
      C-ERRORS (MAFallback is not an ArithmeticError; a ball outside binary64's range and a subnormal shadow product raise MAFallback); at
      degree 8 against arb: K3 E with caps, K5 lp_norm p = 2 and pos_norm p = 1, PLANT-MA-INPUT (one minor scaled by 1 + 1e-3 must leave
      the reference ball); K4 npoly_mul against the stub; pk03's interface (SPoly, AllMom2 in mp.iv) against the stub; QC C-BUDGET B0.
QC C-BUDGET lines are quality control, not gates (the balls already include the M-a error): the M-a part of an output is the radius
  difference of two arb assemblies, with the kernels' M-a radii and with them set to zero.
Run (own folder; outputs NEW paths): D=/mnt/g2/release/root/code/pk02; o=$D/out/out_kt_ma_val_v1_5_<piece>.out;
  [ ! -e "$o" ] && OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MALLOC_ARENA_MAX=2 OMP_NUM_THREADS=1 timeout 580 nice -n 10 /usr/bin/time -v
  prlimit --as=<AS> -- python3 -I -B $D/kt_ma_val_v1_5.py <v1|v2|v3|v4> 540 > "$o" 2> "${o%.out}.err"

"""
import sys, os, math, hashlib, importlib.util, time, itertools, resource, traceback
from fractions import Fraction

OWN = '/mnt/g2/release/root/code/pk02'
PINS = {'kt_cert_v1_5.py': '33423b592a1770ef9b7737c682187503a85840d193207771dda0a0c1f35c0495',
        'arbeng_ma_v1_3.py': '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be',
        'arbeng_ma_v1_1.py': '81f7fb89f863343149b1558bfc3c8ba3e09b3e6c36ec00db4c12197b11158e7f',
        'arbeng_ma_stub_v1_1.py': '794fabc7111555db2f6390a144d3f5af6deeb358d02da8b5705cf3ceaefd0af1',
        'arbeng_ma_stub_v1.py': '155da41ca05f093c028c3d50764a7efef65d753d2e200d6696030953c178523b'}
if os.path.dirname(os.path.abspath(__file__)) != OWN:
    print('kt_ma_val_v1_5 must run from its own folder')
    sys.exit(2)
PIECE = sys.argv[1] if len(sys.argv) > 1 else ''
LIM = sys.argv[2] if len(sys.argv) > 2 else '540'
if PIECE not in ('v1', 'v2', 'v3', 'v4') or not LIM.isdigit() or not (5 <= int(LIM) <= 540):
    print('usage: kt_ma_val_v1_5.py v1|v2|v3|v4 LIM')
    sys.exit(2)


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


print('kt_ma_val_v1_5 sha256 %s PIECE=%s LIM=%s' % (sha(os.path.abspath(__file__)), PIECE, LIM), flush=True)
for nm, want in PINS.items():
    if sha(os.path.join(OWN, nm)) != want:
        print('SHA MISMATCH %s' % nm)
        print('VERDICT INVALID (C-HASH)')
        sys.exit(2)


def load(name, path, argv=None):
    if argv is not None:
        sys.argv = argv
    sp = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


kt = load('ktc5', os.path.join(OWN, 'kt_cert_v1_5.py'), [os.path.join(OWN, 'kt_cert_v1_5.py'), 'tA.e1n4', LIM])
ma = load('arbeng_ma_v1_3', os.path.join(OWN, 'arbeng_ma_v1_3.py'))
ma_old = load('arbeng_ma_v1_1', os.path.join(OWN, 'arbeng_ma_v1_1.py'))           # PLANT-TINY and PLANT-ZEROMID only
stub = load('arbeng_ma_stub_v1_1', os.path.join(OWN, 'arbeng_ma_stub_v1_1.py'))
stub_old = load('arbeng_ma_stub_v1', os.path.join(OWN, 'arbeng_ma_stub_v1.py'))      # PLANT-SIGN only (its sign-dropping mpi_to_arb)
np, arb, arb_mat, out = kt.np, kt.arb, kt.arb_mat, kt.out
out('C-HASH PASS (kt_cert_v1_5, arbeng_ma_v1_3, arbeng_ma_v1_1, arbeng_ma_stub_v1_1, arbeng_ma_stub_v1)')
out(ma.env_probes())
FAILS, FIRES = [], []
GROUPS10 = [0] * 6 + [1] * 4


def gate(name, ok, line):
    out('%s: %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s: %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        FIRES.append(name)


def qc(name, line):
    out('QC %s (quality control, not a gate): %s' % (name, line))


def overlaps(mid, rad, ball):
    lo, hi = arb(float(mid)) - arb(float(rad)), arb(float(mid)) + arb(float(rad))
    return not (hi < ball.lower() or lo > ball.upper())


def rel(x):
    return float(x.rad()) / abs(float(x.mid())) if float(x.mid()) != 0 else float('inf')


def printed_v23(key):
    nm, line = kt.v23_line('e1')
    return kt.printed(line, key)


def v23_digits_ok(val, s):
    d = len(s.split('e')[0].split('.')[1]) if '.' in s.split('e')[0] else 0
    tol = 0.5 * 10.0 ** (int(s.split('e')[1]) - d) + 1e-9 * abs(float(s))
    return abs(val - float(s)) <= tol


def c_tree():
    ok, lines = ma.tree_check()
    gate('C-TREE', ok, '; '.join(lines))


def W_arb(Wi):
    W = arb_mat(len(Wi), len(Wi[0]))
    for i in range(len(Wi)):
        for j in range(len(Wi[0])):
            W[i, j] = int(Wi[i][j])
    return W


def handoff_rows(piece):
    return kt.read_handoff(piece)[0]


def handoff_term(piece, fam, idx):
    hit = [ln for ln in handoff_rows(piece) if ln.startswith('TAIL %s %d ' % (fam, idx))]
    if len(hit) != 1:
        raise ValueError('hand-off %s has %d rows for %s%d' % (piece, len(hit), fam, idx))
    return arb(hit[0].split(' ', 3)[3])


def table_compare(cmM, cmA, label):
    """every CondTable entry against arb CondMomA (kt_ma_val_v1_2): overlap where both have the entry; an entry on one side only must
    contain 0 (error-only entries of the tiny rule, or arb's structural-zero balls). Returns the PLANT-MA-ROUND and -COUNT miss counts."""
    seen = set()
    nent, bad, one_sided, worst_rel, miss_round, miss_count = 0, 0, 0, 0.0, 0, 0
    for e, (gd, A) in cmM.ent.items():
        tab = cmA.table.get(e, {})
        rad = A.radius()
        r_nor = A.sr - A.sa
        r_cnt = ma.MA(A.mid, A.sa, A.sr, np.zeros(len(A.k), dtype=np.int64)).radius()
        for i, row in enumerate(gd):
            key = tuple(int(x) for x in row)
            seen.add((e, key))
            ball = tab.get(key)
            nent += 1
            if ball is None:
                one_sided += 1
                bad += 0 if overlaps(A.mid[i], rad[i], arb(0)) else 1
                continue
            if not overlaps(A.mid[i], rad[i], ball):
                bad += 1
                continue
            if A.mid[i] != 0:
                worst_rel = max(worst_rel, float(rad[i]) / abs(float(A.mid[i])))
            miss_round += 0 if overlaps(A.mid[i], r_nor[i], ball) else 1
            miss_count += 0 if overlaps(A.mid[i], r_cnt[i], ball) else 1
    arb_only, bad_arb = 0, 0
    for e, rows in cmA.table.items():
        for key, ball in rows.items():
            if (e, tuple(int(x) for x in key)) not in seen:
                arb_only += 1
                bad_arb += 0 if ball.contains(0) else 1
    gate('%s table containment' % label, bad == 0 and bad_arb == 0, '%d M-a entries (%d without an arb entry), %d arb-only entries; '
         '%d M-a and %d arb entries fail (no overlap, or a one-sided entry not containing 0); largest M-a relative width %.2e' % (
             nent, one_sided, arb_only, bad, bad_arb, worst_rel))
    return miss_round, miss_count


def piece_v1():
    t = arb(1) / kt.J_MAIN
    hL = {k: kt.hk(k, [(v, kt.a_e) for v in kt.XD], kt.bondsL, kt.cf_rad) for k in range(1, 5)}
    D4 = kt.Dbar(4, hL, kt.source_pis('e1', t))
    ex4 = D4.exponents()
    deg2, qdeg, tot = int(ex4[:, 6:].sum(axis=1).max()), int(ex4[:, 9:].sum(axis=1).max()), int(ex4.sum(axis=1).max())
    Amat = kt.eye3() + kt.tri_laplacian()
    Ainv = Amat.inv()
    W2i = [[0] * 6 for _ in range(3)]
    for r in range(3):
        W2i[r][r] = 1
    for p_, (r, s) in enumerate(kt.PAIRS):
        W2i[r][3 + p_], W2i[s][3 + p_] = 1, -1
    W2 = W_arb(W2i)
    At = Amat - kt.eye3() * (2 * kt.c_e * t)
    Ati = At.inv()
    detf = ((Amat.det() / At.det()).log() * kt.nn / 2).exp()
    Delta = Ati - Ainv
    kw = dict(groups=[0, 0, 0, 1, 1, 1], caps={1: max(qdeg, 1)})
    c0 = time.process_time()
    t0c = ma.TINY_COUNT[0]
    cmM = ma.condmom(Ati, Ati, W2, W2i, kt.nn, deg2, **kw)
    out('V1 K2 CondTable Dc %d: %d entries, inner zeroed %d (cpu %.1f s); C-SHADOW %.2e' % (deg2, cmM.entries, cmM.am.zeroed,
                                                                                          time.process_time() - c0, cmM.shadow_max()))
    out('C-TINY V1: %d terms made error-only by the tiny rule; C-UF: largest einsum allowance %.3e, Smax %.3e' % (
        ma.TINY_COUNT[0] - t0c, cmM.uf_max, cmM.smax))
    c0 = time.process_time()
    cmA = kt.ae.CondMomA(Ati, Ati, W2, kt.nn, deg2, **kw)
    out('V1 arb CondMomA Dc %d (cpu %.1f s)' % (deg2, time.process_time() - c0))
    miss_round, miss_count = table_compare(cmM, cmA, 'V1 (a)')
    plant('PLANT-MA-ROUND', miss_round > 0, 'without the rounding term %d entries miss their arb ball' % miss_round)
    out('INFO count-0 radius (kt_ma_val_v1_4: no longer a plant): %d entries miss their arb ball; the formula margin 4u (A + B + C), '
        'about 8u times the shadow, covers this table\'s actual errors, so a count-only plant cannot fire on it' % miss_count)
    c0 = time.process_time()
    EDm, kmx = cmM.condE(D4.to_dict(), tot)
    out('V1 K2 condE: %d coefficients, largest count %d (cpu %.1f s)' % (len(EDm), kmx, time.process_time() - c0))
    cgT = kt.ae.CondGA(cmA, tot)
    EDa = cgT.out.to_dict(cgT.condE(D4.to_dict()))
    badE = sum(1 for g, b in EDa.items() if g not in EDm or not EDm[g].overlaps(b)) + sum(
        1 for g in EDm if g not in EDa and not EDm[g].contains(0))
    gate('V1 (b) ED containment', badE == 0, '%d arb coefficients, %d M-a, %d mismatches' % (len(EDa), len(EDm), badE))
    ext = arb_mat(6, 6)
    for i in range(3):
        for j in range(3):
            ext[i, j] = Delta[i, j]
    G2, n2 = kt.tilted_cov_a(kt.LD, kt.BD, [kt.c_m * t] * 6, extra=ext)

    def nD_of(ED):
        w2 = kt.ae.WishartA(kt.sub_mat(G2, [0, 1, 2]), kt.nn, 2 * max(sum(e) for e in ED))
        return (t ** 4 / 24) * detf * kt.nsqrt(n2 * w2.E2(ED, ED))
    nDa, nDm = nD_of(EDa), nD_of(EDm)
    nDm0 = nD_of({g: arb(b.mid()) for g, b in EDm.items()})
    got = dict(ln.split(' ', 1) for ln in handoff_rows('c'))
    nDh = arb(got['NDB'])
    relw = rel(nDm)
    gate('V1 (c) nD (C-RAD-MA)', bool(nDm.overlaps(nDa)) and bool(nDm.overlaps(nDh)) and relw <= 1e-5,
         'arb %s | c hand-off %s | M-a %s | relative width %.2e (<= 1e-5)' % (kt.bstr(nDa), kt.bstr(nDh), kt.bstr(nDm), relw))
    s = printed_v23('nD')
    gate('C-REPRO nD', v23_digits_ok(float(nDm.mid()), s), 'M-a midpoint %.6e against kt_c_v2_3 printed %s (old trial set)' % (
        float(nDm.mid()), s))
    part = float(nDm.rad()) - float(nDm0.rad())
    qc('C-BUDGET nD', 'M-a part %.2e = radius with the M-a radii %.2e minus without %.2e; relative %.2e' % (
        part, float(nDm.rad()), float(nDm0.rad()), part / float(nDm.mid())))


def tail_setup():
    t = arb(1) / kt.J_MAIN
    P, dP, qP = kt.tail_poly(kt.series_T3('e1'), t)
    return t, P, dP, max(2 * qP, 1)


def gram(fam, idx, t):
    """kt_cert_v1_5's joint_moments_a without its arb table: G9, N9 under the tilt, Gam = W10^T G6 W10, and the Chernoff factor."""
    lam = arb(kt.LAM_T)
    rates = [kt.c_m * t] * 6 + [arb(0)] * 3
    extra = None
    if fam == 'X':
        rates[6 + idx] = rates[6 + idx] + lam
        cexp = arb(kt.a_e)
    else:
        extra = arb_mat(9, 9)
        extra[idx, idx], extra[6 + idx, 6 + idx], extra[idx, 6 + idx], extra[6 + idx, idx] = lam, lam, -lam, -lam
        cexp = kt.kappa_B()
    G9, N9 = kt.tilted_cov_a(kt.L9, kt.B9, rates, extra=extra, label='val %s%d' % (fam, idx))
    if G9 is None:
        raise ValueError('the tilt %s%d is not certainly positive definite' % (fam, idx))
    Gam = kt.W10.transpose() * kt.sub_mat(G9, [0, 1, 2, 6, 7, 8]) * kt.W10
    return Gam, N9, (-lam * kt.J_MAIN * cexp).exp()


def c_sing(tab, qc_, label):
    """C-SING on an M-a table: every dropped subset is rank-deficient with a det ball containing 0, and kept plus dropped are all the
    subsets the caps allow (sizes up to min(F, D))."""
    okd = all(ma.int_rank(kt.W10_INT, A) < len(A) and d.contains(0) for A, d in tab.dropped)
    allowed = 0
    for j in range(1, min(tab.F, tab.D) + 1):
        for A in itertools.combinations(range(tab.F), j):
            if sum(1 for f in A if GROUPS10[f] == 1) <= qc_:
                allowed += 1
    kept = sum(len(tab.Dj[j][0]) for j in range(1, len(tab.Dj)) if tab.Dj[j] is not None)
    gate('C-SING %s' % label, okd and kept + tab.zeroed == allowed, '%d kept, %d dropped (all rank-deficient, det balls containing 0: %s), '
         '%d allowed' % (kept, tab.zeroed, okd, allowed))


def ma_term(fam, idx, t, P, dP, qc_):
    Gam, N9, fac = gram(fam, idx, t)
    c0 = time.process_time()
    tab = ma.allmom2(Gam, kt.nn, 2 * dP, groups=GROUPS10, caps={1: qc_}, W_int=kt.W10_INT, W=kt.W10)
    e2 = tab.E2(P, P)
    return fac * N9 * e2, fac * N9 * arb(e2.mid()), tab, Gam, N9, fac, time.process_time() - c0


def piece_v2():
    t, P, dP, qc_ = tail_setup()
    terms = {}
    for idx in range(3):
        termM, termM0, tab, Gam, N9, fac, tm = ma_term('X', idx, t, P, dP, qc_)
        termA = handoff_term('tX%d' % idx, 'X', idx)
        relw = rel(termM)
        gate('V2 X%d' % idx, bool(termM.overlaps(termA)) and relw <= 1e-5, 'hand-off %s | M-a %s (table degree %d, cpu %.1f s) | relative '
             'width %.2e; C-SHADOW %.2e' % (kt.bstr(termA), kt.bstr(termM), 2 * dP, tm, relw, tab.shadow_max()))
        c_sing(tab, qc_, 'X%d' % idx)
        part = float(termM.rad()) - float(termM0.rad())
        qc('C-BUDGET X%d' % idx, 'M-a part %.2e, relative %.2e' % (part, part / float(termM.mid())))
        terms[idx] = termM
    tailX = kt.nsqrt(terms[0] + terms[1] + terms[2])
    s = printed_v23('tailX')
    gate('C-REPRO tailX', v23_digits_ok(float(tailX.mid()), s), 'M-a %.4e against kt_c_v2_3 printed %s (old trial set)' % (
        float(tailX.mid()), s))


def exact_moments(Gq, n, D, W_int):
    """the AllMom2 recursion in Fractions: Gq an F x F list of Fractions (= W^T G W), exact minors, exact zeros; {exponent tuple: moment}."""
    F = len(Gq)

    def det(M):
        M = [row[:] for row in M]
        m = len(M)
        dt = Fraction(1)
        for c in range(m):
            piv = next((i for i in range(c, m) if M[i][c] != 0), None)
            if piv is None:
                return Fraction(0)
            if piv != c:
                M[c], M[piv] = M[piv], M[c]
                dt = -dt
            dt *= M[c][c]
            for i in range(c + 1, m):
                f = M[i][c] / M[c][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
        return dt
    Dj = {}
    for j in range(1, min(F, D) + 1):
        for A in itertools.combinations(range(F), j):
            if ma.int_rank(W_int, A) < j:
                continue
            Dj[A] = Fraction(-2) ** j * det([[Gq[a][b] for b in A] for a in A])
    M = {tuple([0] * F): Fraction(1)}
    by_deg = {0: [tuple([0] * F)]}
    for k in range(1, D + 1):
        by_deg[k] = sorted(set(tuple(e[i] + (1 if i == f else 0) for i in range(F)) for e in by_deg[k - 1] for f in range(F)))
        for e in by_deg[k]:
            acc = Fraction(0)
            for A, dv in Dj.items():
                j = len(A)
                if j > k:
                    continue
                prev = tuple(e[i] - (1 if i in A else 0) for i in range(F))
                if min(prev) < 0:
                    continue
                acc += (Fraction(2 - n, 2) * j - k) * dv * M.get(prev, Fraction(0))
            M[e] = acc / k
    return {e: v * math.prod(math.factorial(x) for x in e) for e, v in M.items()}


def exact_end(t):
    """an mp.iv endpoint's exact value from its raw tuple (sign, man, exp, bc), as an arb (a dyadic rational, so exact)."""
    sign, man, exp, bc = t
    q = Fraction(-int(man) if sign else int(man)) * Fraction(2) ** int(exp)
    return arb(q.numerator) / q.denominator


def contains_ends(A, I):
    return bool(A.contains(exact_end(I._mpi_[0]))) and bool(A.contains(exact_end(I._mpi_[1])))


def c_cross():
    """C-CROSS (kt_ma_val_v1_1; v1_3 adds four checks and the symmetric straddling
    interval). For the layer and for its arb stub: intervals with both ends negative, straddling 0 (also symmetrically, midpoint
    exactly 0), a zero end, large and tiny (subnormal) exponents, an mp.iv quotient, and two quotients at iv.dps = 40 (136-bit ends):
    (a) mpi_to_arb(I) contains both exact endpoints (from the raw tuples, never float()); (b) arb_to_mpi of it contains I; (c) mpi_to_arb
    of that contains the first ball. Balls (one with a zero end): ball_to_in and its inverse contain the source, and arb_to_mpi then
    mpi_to_arb contains it. PLANT-SIGN: arbeng_ma_stub_v1's mpi_to_arb (unsigned mantissas) must fail (a) on some case."""
    from mpmath import iv
    old_dps = iv.dps
    ivs = [iv.mpf([-3.25, -1.5]), iv.mpf([-0.75, 1.25]), iv.mpf([-0.25, 0.25]), iv.mpf([0.0, 2.5]), iv.mpf([-2.5, 0.0]),
           iv.mpf([-1.5 * 2.0 ** 1000, -2.0 ** 999]), iv.mpf([-2.0 ** -1050, -2.0 ** -1060]), iv.mpf([2.0 ** -1060, 3.0 * 2.0 ** -1040]),
           -(iv.mpf(1) / 3), iv.mpf([-2.0 ** 1020, 2.0 ** -1030])]
    try:
        iv.dps = 40
        ivs += [-(iv.mpf(1) / 3), iv.mpf(1) / 7 - iv.mpf(1) / 2]
        hi_prec = [I._mpi_[0][3] for I in ivs[-2:]]
    finally:
        iv.dps = old_dps
    balls = [arb('-0.1') + arb(0, 1e-20), arb(-3) * arb(2) ** -1000, -(arb(2) ** 900) + arb(0, 2.0 ** 880), arb(0, 1e-3), arb(-7) / 3,
             arb('-12345.678901234567890123'), arb('-0.25') + arb(0, 0.25)]
    for mod, label in ((ma, 'layer'), (stub, 'stub')):
        bad, lines = 0, []
        for I in ivs:
            A = mod.mpi_to_arb(I)
            I2 = mod.arb_to_mpi(A)
            A2 = mod.mpi_to_arb(I2)
            ok = contains_ends(A, I) and bool(I2.a <= I.a) and bool(I2.b >= I.b) and bool(A2.contains(A))
            bad += 0 if ok else 1
            lines.append('[%s, %s] %s' % (repr(float(I.a)), repr(float(I.b)), 'ok' if ok else 'MISS'))
        badb = 0
        for x in balls:
            m, r = mod.ball_to_in(x) if hasattr(mod, 'ball_to_in') else (None, None)
            ok1 = True if m is None else bool(mod._arb_of(m, r).contains(x))
            ok2 = bool(mod.mpi_to_arb(mod.arb_to_mpi(x)).contains(x))
            badb += 0 if (ok1 and ok2) else 1
        gate('C-CROSS (%s)' % label, bad == 0 and badb == 0, '%d intervals (two with %s-bit ends at iv.dps 40): %s; %d balls through '
             'ball_to_in and back and through mp.iv and back, %d not contained' % (len(ivs), '/'.join(str(b) for b in hi_prec),
                                                                                  '; '.join(lines), len(balls), badb))
    missed = sum(1 for I in ivs if not contains_ends(stub_old.mpi_to_arb(I), I))
    plant('PLANT-SIGN', missed > 0, 'arbeng_ma_stub_v1\'s unsigned mpi_to_arb misses the endpoints of %d of %d intervals' % (missed, len(ivs)))


def c_tiny():
    """C-TINY (kt_ma_val_v1_2): a Dc 6 CondTable on the symmetric A (the triangle couplings (a, a, b), whose 0 <-> 2 symmetry makes entries of
    P and Gm vanish exactly) against arb CondMomA, entry by entry; the rule must have fired. PLANT-TINY: the same table under arbeng_ma_v1_1
    must raise MAFallback."""
    t = arb(1) / kt.J_MAIN
    Amat = kt.eye3() + kt.tri_laplacian()
    Ati = (Amat - kt.eye3() * (2 * kt.c_e * t)).inv()
    W2i = [[0] * 6 for _ in range(3)]
    for r in range(3):
        W2i[r][r] = 1
    for p_, (r, s) in enumerate(kt.PAIRS):
        W2i[r][3 + p_], W2i[s][3 + p_] = 1, -1
    W2 = W_arb(W2i)
    kw = dict(groups=[0, 0, 0, 1, 1, 1], caps={1: 2})
    t0c = ma.TINY_COUNT[0]
    c0 = time.process_time()
    cmM = ma.condmom(Ati, Ati, W2, W2i, kt.nn, 6, **kw)
    ntiny = ma.TINY_COUNT[0] - t0c
    cmA = kt.ae.CondMomA(Ati, Ati, W2, kt.nn, 6, **kw)
    table_compare(cmM, cmA, 'C-TINY (Dc 6)')
    gate('C-TINY rule exercised', ntiny > 0, '%d terms made error-only; C-UF: largest einsum allowance %.3e, Smax %.3e; %d entries (cpu '
         '%.1f s)' % (ntiny, cmM.uf_max, cmM.smax, cmM.entries, time.process_time() - c0))
    try:
        ma_old.condmom(Ati, Ati, W2, W2i, kt.nn, 6, **kw)
        fired, why = False, 'built'
    except ma_old.MAFallback as e:
        fired, why = True, str(e)
    plant('PLANT-TINY', fired, 'the same table under arbeng_ma_v1_1: %s' % why)


def same_keys_overlap(Rm, Rs):
    return set(Rm) == set(Rs) and all(bool(Rm[k].overlaps(Rs[k])) for k in Rs)


def cond_tables(mod, zb):
    """a Dc 3 CondTable on a generic (non-symmetric) SPD C, with M = C except M[0, 0] = zb, so that P = W^T M has the entry P[X0, 0] = zb
    (midpoint exactly 0); returns (table, W, W_int)."""
    q = [[Fraction(1), Fraction(1, 5), Fraction(1, 10)], [Fraction(1, 5), Fraction(13, 10), Fraction(3, 10)],
         [Fraction(1, 10), Fraction(3, 10), Fraction(9, 10)]]
    C, M = arb_mat(3, 3), arb_mat(3, 3)
    for i in range(3):
        for j in range(3):
            C[i, j] = arb(q[i][j].numerator) / q[i][j].denominator
            M[i, j] = C[i, j]
    M[0, 0] = zb
    Wi = [[0] * 6 for _ in range(3)]
    for r in range(3):
        Wi[r][r] = 1
    for p_, (r, s) in enumerate(kt.PAIRS):
        Wi[r][3 + p_], Wi[s][3 + p_] = 1, -1
    return mod.condmom(M, C, W_arb(Wi), Wi, kt.nn, 3, groups=[0, 0, 0, 1, 1, 1], caps={1: 2})


def ends_inside(ball, f):
    """the T-a (kt_ma_val_v1_5): the stub's values f(+0.25) and f(-0.25), zb replaced by the exact ends, lie inside ball."""
    return all(bool(ball.contains(f(arb(s)))) for s in (0.25, -0.25))


def zmid_cases(mod, zb, tabs):
    """the zero-midpoint class through mod's npoly_mul, npoly_pow (k = 2), E2, lp_norm (p = 4), condE and CondTable, each against the arb
    stub: same keys and overlapping balls; E2, E2 two parts and lp_norm also need the stub's values at zb = +0.25 and
    -0.25 inside mod's ball (T-a, kt_ma_val_v1_5). Returns {case: ok}."""
    res = {}
    P1, Q1 = {(1,): zb}, {(0,): arb(1)}
    res['npoly_mul'] = same_keys_overlap(mod.npoly_mul(P1, Q1), stub.npoly_mul(P1, Q1))
    res['npoly_pow k=2'] = same_keys_overlap(mod.npoly_pow(P1, 2), stub.npoly_pow(P1, 2))
    tm, ts = tabs[mod.VERSION], tabs['stub']
    P4, Q4 = {(1, 0, 0, 0): zb}, {(1, 0, 0, 0): arb(1)}
    b = tm.E2(P4, Q4)
    res['E2'] = bool(b.overlaps(ts.E2(P4, Q4))) and ends_inside(b, lambda z: ts.E2({(1, 0, 0, 0): z}, Q4))
    P42 = {(1, 0, 0, 0): zb, (0, 0, 0, 0): arb(1)}                  # v1_4: a whole degree group zero-midpoint (the D-1 count case)
    b = tm.E2(P42, Q4, fallback=False)                              # v1_5: the ball itself (relative M-a error 0.5; see C-FALLBACK)
    res['E2 two parts'] = bool(b.overlaps(ts.E2(P42, Q4))) and ends_inside(b, lambda z: ts.E2({(1, 0, 0, 0): z, (0, 0, 0, 0): arb(1)}, Q4))
    b = mod.lp_norm(tm, P4, 4)
    res['lp_norm p=4'] = bool(b.overlaps(stub.lp_norm(ts, P4, 4))) and ends_inside(b, lambda z: stub.lp_norm(ts, {(1, 0, 0, 0): z}, 4))
    cm, cs = cond_tables(mod, zb), cond_tables(stub, zb)
    P12 = {(0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0): zb, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0): arb(1)}
    res['condE'] = same_keys_overlap(cm.condE(P12, 2)[0], cs.condE(P12, 2)[0])
    rows_m = {(e, tuple(int(x) for x in row)) for e, (gd, A) in cm.ent.items() for row in gd}
    rows_s = {(e, tuple(int(x) for x in key)) for e, tb in cs._cm.table.items() for key in tb}
    okc = rows_s <= rows_m
    if okc:
        for e, (gd, A) in cm.ent.items():
            rad = A.radius()
            tb = cs._cm.table.get(e, {})
            for i, row in enumerate(gd):
                b = tb.get(tuple(int(x) for x in row))
                okc = okc and (overlaps(A.mid[i], rad[i], b) if b is not None else overlaps(A.mid[i], rad[i], arb(0)))
    res['CondTable'] = okc
    return res


def c_zeromid():
    """C-ZMID (kt_ma_val_v1_3): the coefficient 0 +- 0.25 (midpoint exactly 0) through npoly_mul,
    npoly_pow (k = 2), E2, lp_norm (p = 4), condE (a P12 coefficient) and CondTable (one such entry of W^T M), each against the arb stub
    (same keys, overlapping balls; the stub keeps every nonzero ball), with endpoint containment for E2, E2 two parts and lp_norm (T-a,
    kt_ma_val_v1_5). C-FALLBACK (kt_ma_val_v1_5): E2 two parts with the default fallback must raise MAFallback (relative M-a error 0.5).
    PLANT-ZMID: under arbeng_ma_v1_1 (present() without sr) the gate must fail: npoly_mul, npoly_pow, E2, lp_norm, condE or CondTable
    loses the class."""
    zb = arb(0, 0.25)
    Wi = [[1, 0, 0, 1], [0, 1, 0, -1], [0, 0, 1, 0]]
    G = [[Fraction(2, 4), Fraction(1, 4), 0], [Fraction(1, 4), Fraction(2, 4), Fraction(1, 4)], [0, Fraction(1, 4), Fraction(2, 4)]]
    Gq = [[sum(Fraction(Wi[a][f]) * G[a][b] * Wi[b][g] for a in range(3) for b in range(3)) for g in range(4)] for f in range(4)]
    Garb = arb_mat(4, 4)
    for f in range(4):
        for g in range(4):
            Garb[f, g] = arb(Gq[f][g].numerator) / Gq[f][g].denominator
    tabs = {ma.VERSION: ma.allmom2(Garb, 2, 8, W_int=Wi, W=W_arb(Wi)), ma_old.VERSION: ma_old.allmom2(Garb, 2, 8, W_int=Wi, W=W_arb(Wi)),
            'stub': stub.allmom2(Garb, 2, 8, W_int=Wi, W=Wi)}
    res = zmid_cases(ma, zb, tabs)
    gate('C-ZMID', all(res.values()), '; '.join('%s %s' % (k, 'ok' if v else 'FAIL') for k, v in res.items()))
    try:
        tabs[ma.VERSION].E2({(1, 0, 0, 0): zb, (0, 0, 0, 0): arb(1)}, {(1, 0, 0, 0): arb(1)})
        fb, why = False, 'returned a ball'
    except ma.MAFallback as e:
        fb, why = True, 'MAFallback: %s' % e
    gate('C-FALLBACK', fb, 'E2 of (0 +- 0.25) Y0 + 1 against Y0 with the default fallback (relative M-a error 0.5 > FALLBACK_REL %.0e): %s' % (
        ma.FALLBACK_REL, why))
    try:
        res0 = zmid_cases(ma_old, zb, tabs)
        why = '; '.join('%s %s' % (k, 'ok' if v else 'lost') for k, v in res0.items())
        fired = not all(res0.values())
    except ma_old.MAFallback as e:
        fired, why = False, 'MAFallback: %s' % e
    plant('PLANT-ZMID', fired, 'arbeng_ma_v1_1: %s' % why)


def c_count_floor():
    """C-COUNT / PLANT-COUNT and C-FLOOR / PLANT-FLOOR (kt_ma_val_v1_4; the DELTA on ADD3). C-COUNT: ma_add of a normal operand
    (k 3) and an error-only one (mid 0, sa 0, sr 0.25, k 5) must count max + 1 = 6 and carry sr 1.25; PLANT-COUNT: arbeng_ma_v1_1's ma_add
    (present() without sr) keeps k 3. C-FLOOR: npoly_mul of x = y = 1e-200 +- 1e-210 must contain the arb product (about 1e-400, which
    underflows in binary64); PLANT-FLOOR: the same with the floor removed (TWO_TINY := 0 for the call) must fail containment."""
    x = ma.MA(np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([3], dtype=np.int64))
    y = ma.MA(np.array([0.0]), np.array([0.0]), np.array([0.25]), np.array([5], dtype=np.int64))
    s = ma.ma_add(x, y)
    gate('C-COUNT', int(s.k[0]) == 6 and float(s.sr[0]) == 1.25, 'ma_add(normal k 3, error-only k 5): k %d (want 6), sr %r (want 1.25)' % (
        int(s.k[0]), float(s.sr[0])))
    s0 = ma_old.ma_add(ma_old.MA(x.mid, x.sa, x.sr, x.k), ma_old.MA(y.mid, y.sa, y.sr, y.k))
    plant('PLANT-COUNT', int(s0.k[0]) != 6, 'arbeng_ma_v1_1: k %d' % int(s0.k[0]))
    xb = arb('1e-200') + arb(0, 1e-210)
    exact = xb * xb

    def contained(R):
        return (2,) in R and bool(R[(2,)].contains(exact))
    R = ma.npoly_mul({(1,): xb}, {(1,): xb})
    gate('C-FLOOR', contained(R), 'npoly_mul((1e-200 +- 1e-210) x, same) -> %s; arb product %s' % (
        {k: v.str(5) for k, v in R.items()}, exact.str(5)))
    keep = ma.TWO_TINY
    try:
        ma.TWO_TINY = 0.0
        Rp = ma.npoly_mul({(1,): xb}, {(1,): xb})
    finally:
        ma.TWO_TINY = keep
    plant('PLANT-FLOOR', not contained(Rp), 'without the floor (TWO_TINY := 0): %s' % ({k: v.str(5) for k, v in Rp.items()}))


def c_int64():
    """C-INT64 (kt_ma_val_v1_2): the code guard passes 6^24 < 2^63, raises ValueError on 7^24, and a MomTable with F = 24, D = 6 raises
    ValueError before any work. PLANT-INT64: numpy's int64 7^24 wraps silently, which the guard prevents."""
    try:
        ma._code_guard(6, 24, 'C-INT64')
        ok1 = True
    except ValueError:
        ok1 = False
    try:
        ma._code_guard(7, 24, 'C-INT64')
        ok2 = False
    except ValueError:
        ok2 = True
    G24 = arb_mat(24, 24)
    for i in range(24):
        G24[i, i] = 1
    c0 = time.process_time()
    try:
        ma.MomTable(G24, kt.nn, 6)
        ok3, why = False, 'built'
    except ValueError as e:
        ok3, why = 'int64' in str(e), str(e)
    gate('C-INT64', ok1 and ok2 and ok3, '6^24 passes: %s; 7^24 raises: %s; MomTable F = 24, D = 6: %s (cpu %.2f s)' % (
        ok1, ok2, why, time.process_time() - c0))
    with np.errstate(over='ignore'):
        wrapped = int(np.int64(7) ** 24)
    plant('PLANT-INT64', wrapped != 7 ** 24, 'numpy int64 7^24 = %d, exact %d' % (wrapped, 7 ** 24))


def piece_v3():
    c_cross()
    c_tiny()
    c_zeromid()
    c_count_floor()
    c_int64()
    Wi = [[1, 0, 0, 1], [0, 1, 0, -1], [0, 0, 1, 0]]            # 4 forms on 3 coordinates: X0, X1, X2, Q01
    G = [[Fraction(2, 4), Fraction(1, 4), 0], [Fraction(1, 4), Fraction(2, 4), Fraction(1, 4)], [0, Fraction(1, 4), Fraction(2, 4)]]
    F = 4
    Gq = [[sum(Fraction(Wi[a][f]) * G[a][b] * Wi[b][g] for a in range(3) for b in range(3)) for g in range(F)] for f in range(F)]
    Garb = arb_mat(F, F)
    for f in range(F):
        for g in range(F):
            Garb[f, g] = arb(Gq[f][g].numerator) / Gq[f][g].denominator
    Wm = W_arb(Wi)
    total, bad, maxw, cases = 0, 0, 0.0, []
    for n, D in ((2, 8), (3, 8), (2, 12)):
        c0 = time.process_time()
        ex = exact_moments(Gq, n, D, Wi)
        tab = ma.allmom2(Garb, n, D, W_int=Wi, W=Wm)
        rows = []
        for d in range(D + 1):
            dec = tab.decode(tab.codes[d])
            rad = tab.mom[d].radius()
            for i, row in enumerate(dec):
                e = tuple(int(x) for x in row)
                exact, mid, r = ex[e], Fraction(float(tab.mom[d].mid[i])), Fraction(float(rad[i]))
                total += 1
                if abs(mid - exact) > r:
                    bad += 1
                if exact != 0:
                    maxw = max(maxw, float(r / abs(exact)))
                    rows.append((mid, r, exact))
        cases.append(rows)
        out('V3 n = %d, degree %d: %d moments, zeroed %d, largest relative width so far %.2e (cpu %.1f s); C-SHADOW %.2e' % (
            n, D, sum(len(c) for c in tab.codes), tab.zeroed, maxw, time.process_time() - c0, tab.shadow_max()))
    gate('C-AK exact moments', bad == 0, '%d moments, %d not contained; largest printed relative width %.2e' % (total, bad, maxw))
    pert = Fraction(10 * maxw)
    flagged = sum(1 for rows in cases for (mid, r, exact) in rows if abs(mid - exact * (1 + pert)) > r)
    nz = sum(len(rows) for rows in cases)
    plant('PLANT-MA-AK', flagged == nz and nz > 0, '%d of %d nonzero exact moments perturbed by 10 x %.2e relative fall outside' % (
        flagged, nz, maxw))


def piece_v4():
    t, P, dP, qc_ = tail_setup()
    termM, termM0, tab, Gam, N9, fac, tm = ma_term('B', 0, t, P, dP, qc_)
    termA = handoff_term('tB', 'B', 0)
    relw = rel(termM)
    gate('V4 B0', bool(termM.overlaps(termA)) and relw <= 1e-5, 'hand-off %s | M-a %s (table degree %d, cpu %.1f s) | relative width '
         '%.2e; C-SHADOW %.2e' % (kt.bstr(termA), kt.bstr(termM), 2 * dP, tm, relw, tab.shadow_max()))
    c_sing(tab, qc_, 'B0')
    part = float(termM.rad()) - float(termM0.rad())
    qc('C-BUDGET B0', 'M-a part %.2e, relative %.2e' % (part, part / float(termM.mid())))
    kw = dict(groups=GROUPS10, caps={1: qc_})
    bad = [row[:] for row in kt.W10_INT]
    for i in range(6):
        bad[i][0] = 0
    try:
        ma.allmom2(Gam, kt.nn, 2, W_int=bad, W=W_arb(bad), **kw)
        fired, why = False, 'passes'
    except ValueError as e:
        fired, why = 'excludes 0' in str(e), str(e)
    plant('PLANT-MA-SING', fired, 'forms with X0\'s column zeroed (W = W_int, not the forms of Gam): %s' % why)
    msgs = []
    for label, kwW in (('W unequal to W_int', dict(W_int=kt.W10_INT, W=W_arb(bad))), ('W missing', dict(W_int=kt.W10_INT))):
        try:
            ma.allmom2(Gam, kt.nn, 2, **kwW, **kw)
            msgs.append('%s: passes' % label)
        except ValueError as e:
            msgs.append('%s: ValueError (%s)' % (label, str(e)[:60]))
    plant('PLANT-MA-W', all('ValueError' in m for m in msgs), '; '.join(msgs))
    okc = (not issubclass(ma.MAFallback, ArithmeticError)) and issubclass(ma.MAFallback, Exception)
    try:
        ma.ball_to_in(arb(2) ** 2000)
        r1 = False
    except ma.MAFallback:
        r1 = True
    tab8 = ma.allmom2(Gam, kt.nn, 8, W_int=kt.W10_INT, W=kt.W10, **kw)
    tiny = {tuple([0] * 10): arb('1e-160')}
    eT = tab8.E2(tiny, tiny)
    r2 = bool(eT.is_finite()) and bool(eT.contains(arb('1e-160') * arb('1e-160')))
    gate('C-ERRORS', okc and r1 and r2, 'MAFallback a plain Exception: %s; 2^2000 at conversion raises MAFallback: %s; the 1e-320 shadow '
         'product goes through the tiny rule (v1_2) to %s, which contains (1e-160)^2: %s' % (okc, r1, eT.str(5), r2))
    tabA8 = kt.ae.AllMom2A(Gam, kt.nn, 8, groups=GROUPS10, caps={1: qc_}, W_int=kt.W10_INT)
    Q4 = dict([(e, c) for e, c in P.items() if sum(e) <= 4][:200])
    if not Q4:
        raise ValueError('no terms of degree <= 4 in the tail polynomial')
    Em, Ea = tab8.E(Q4), tabA8.E(Q4)
    gate('K3 E with caps vs arb (degree 8)', bool(Em.overlaps(Ea)), 'M-a %s | arb %s' % (kt.bstr(Em), kt.bstr(Ea)))
    Lm, La = ma.lp_norm(tab8, Q4, 2), stub.lp_norm(tabA8, Q4, 2)
    gate('K5 lp_norm p = 2 vs arb', bool(Lm.overlaps(La)), 'M-a %s | arb %s' % (kt.bstr(Lm), kt.bstr(La)))
    Qp = dict([(e, abs(c)) for e, c in P.items() if sum(e[:6]) == 0 and sum(e) <= 8][:200])
    Pm_, Pa_ = ma.pos_norm(tab8, Qp, 1), stub.pos_norm(tabA8, Qp, 1)
    gate('K5 pos_norm p = 1 vs arb', bool(Pm_.overlaps(Pa_)), 'M-a %s | arb %s' % (kt.bstr(Pm_), kt.bstr(Pa_)))
    tabP = ma.MomTable(Gam, kt.nn, 8, W_int=kt.W10_INT, W=kt.W10, plant_scale=(1, 0, 1.001), **kw)
    eP = tabP.E2(Q4, Q4, fallback=False)
    eA = tabA8.E2(Q4, Q4)
    plant('PLANT-MA-INPUT', not eP.overlaps(eA), 'first minor of j = 1 scaled by 1 + 1e-3: M-a E2(Q4, Q4) %s against arb %s' % (
        kt.bstr(eP), kt.bstr(eA)))
    Q = dict(list(P.items())[:400])
    Rm, Ra = ma.npoly_mul(Q, Q), stub.npoly_mul(Q, Q)
    badR = sum(1 for e, b in Ra.items() if e not in Rm or not Rm[e].overlaps(b))
    gate('K4 npoly_mul vs arb stub', badR == 0 and len(Rm) == len(Ra), '%d product coefficients, %d mismatches' % (len(Ra), badR))
    Giv = [[ma.arb_to_mpi(Gam[i, j]) for j in range(Gam.ncols())] for i in range(Gam.nrows())]
    tabI = ma.AllMom2(Giv, kt.nn, 8, W_int=kt.W10_INT, W=kt.W10_INT, **kw)
    tabIs = stub.AllMom2(Giv, kt.nn, 8, W_int=kt.W10_INT, W=kt.W10_INT, **kw)
    SPm, SPs = ma.SPoly.from_dict(Q4), stub.SPoly.from_dict(Q4)
    e_m, e_s = ma.mpi_to_arb(tabI.E(SPm.mul(SPm))), ma.mpi_to_arb(tabIs.E(SPs.mul(SPs)))
    l_m, l_s = ma.mpi_to_arb(ma.lp_moment(tabI, SPm, 2)), ma.mpi_to_arb(stub.lp_moment(tabIs, SPs, 2))
    gate('SPoly + AllMom2 (mp.iv) vs arb stub', bool(e_m.overlaps(e_s)) and bool(l_m.overlaps(l_s)) and bool(e_m.overlaps(l_m)),
         'E[Q4 Q4] M-a %s | stub %s; lp_moment(Q4, 2) M-a %s | stub %s' % (kt.bstr(e_m), kt.bstr(e_s), kt.bstr(l_m), kt.bstr(l_s)))


def main():
    T0 = time.process_time()
    try:
        c_tree()
        {'v1': piece_v1, 'v2': piece_v2, 'v3': piece_v3, 'v4': piece_v4}[PIECE]()
        out(ma.env_probes())
    except Exception as e:
        traceback.print_exc()
        out('ERROR at cpu %.1f s: %r' % (time.process_time() - T0, e))
        out('VERDICT INVALID (ERROR)')
        return 1
    why = FAILS + ['%s did not fire' % x for x in FIRES]
    out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (PIECE, time.process_time() - T0,
                                                          resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
